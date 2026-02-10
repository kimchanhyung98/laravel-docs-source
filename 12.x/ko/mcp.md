# Laravel MCP (Laravel MCP)

- [소개](#introduction)
- [설치](#installation)
    - [라우트 퍼블리싱](#publishing-routes)
- [서버 생성](#creating-servers)
    - [서버 등록](#server-registration)
    - [웹 서버](#web-servers)
    - [로컬 서버](#local-servers)
- [툴](#tools)
    - [툴 생성](#creating-tools)
    - [툴 입력 스키마](#tool-input-schemas)
    - [툴 출력 스키마](#tool-output-schemas)
    - [툴 인수 유효성 검증](#validating-tool-arguments)
    - [툴 의존성 주입](#tool-dependency-injection)
    - [툴 애너테이션](#tool-annotations)
    - [조건부 툴 등록](#conditional-tool-registration)
    - [툴 응답](#tool-responses)
- [프롬프트](#prompts)
    - [프롬프트 생성](#creating-prompts)
    - [프롬프트 인수](#prompt-arguments)
    - [프롬프트 인수 유효성 검증](#validating-prompt-arguments)
    - [프롬프트 의존성 주입](#prompt-dependency-injection)
    - [조건부 프롬프트 등록](#conditional-prompt-registration)
    - [프롬프트 응답](#prompt-responses)
- [리소스](#resources)
    - [리소스 생성](#creating-resources)
    - [리소스 템플릿](#resource-templates)
    - [리소스 URI 및 MIME 타입](#resource-uri-and-mime-type)
    - [리소스 요청](#resource-request)
    - [리소스 의존성 주입](#resource-dependency-injection)
    - [리소스 애너테이션](#resource-annotations)
    - [조건부 리소스 등록](#conditional-resource-registration)
    - [리소스 응답](#resource-responses)
- [메타데이터](#metadata)
- [인증(Authentication)](#authentication)
    - [OAuth 2.1](#oauth)
    - [Sanctum](#sanctum)
- [인가(Authorization)](#authorization)
- [서버 테스트](#testing-servers)
    - [MCP Inspector](#mcp-inspector)
    - [단위 테스트](#unit-tests)

<a name="introduction"></a>
## 소개

[Laravel MCP](https://github.com/laravel/mcp)는 AI 클라이언트가 [Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro)을 통해 Laravel 애플리케이션과 상호작용할 수 있도록 간단하고 우아한 방법을 제공합니다. 이 패키지는 서버, 툴, 리소스, 프롬프트를 정의할 수 있는 명확하고 유연한 인터페이스를 제공하며, 이를 통해 AI 기반 상호작용이 가능합니다.

<a name="installation"></a>
## 설치

먼저 Composer 패키지 매니저를 사용하여 Laravel MCP를 프로젝트에 설치합니다:

```shell
composer require laravel/mcp
```

<a name="publishing-routes"></a>
### 라우트 퍼블리싱

Laravel MCP 설치 후, MCP 서버를 정의할 `routes/ai.php` 파일을 퍼블리시하려면 `vendor:publish` Artisan 명령어를 실행합니다:

```shell
php artisan vendor:publish --tag=ai-routes
```

이 명령어는 애플리케이션의 `routes` 디렉터리에 `routes/ai.php` 파일을 생성하며, 이 파일에서 MCP 서버를 등록하게 됩니다.

<a name="creating-servers"></a>
## 서버 생성

`make:mcp-server` Artisan 명령어를 사용하여 MCP 서버를 생성할 수 있습니다. 서버는 툴, 리소스, 프롬프트 등 MCP 기능을 AI 클라이언트에 노출하는 중앙 통신 지점 역할을 합니다:

```shell
php artisan make:mcp-server WeatherServer
```

이 명령어를 실행하면 `app/Mcp/Servers` 디렉터리에 새로운 서버 클래스가 생성됩니다. 생성된 서버 클래스는 Laravel MCP의 기본 `Laravel\Mcp\Server` 클래스를 확장하며, 툴, 리소스, 프롬프트 등록을 위한 속성이 포함되어 있습니다.

```php
<?php

namespace App\Mcp\Servers;

use Laravel\Mcp\Server;

class WeatherServer extends Server
{
    /**
     * MCP 서버의 이름.
     */
    protected string $name = 'Weather Server';

    /**
     * MCP 서버의 버전.
     */
    protected string $version = '1.0.0';

    /**
     * LLM을 위한 MCP 서버의 설명.
     */
    protected string $instructions = 'This server provides weather information and forecasts.';

    /**
     * 이 MCP 서버에 등록된 툴들.
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Tool>>
     */
    protected array $tools = [
        // GetCurrentWeatherTool::class,
    ];

    /**
     * 이 MCP 서버에 등록된 리소스들.
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Resource>>
     */
    protected array $resources = [
        // WeatherGuidelinesResource::class,
    ];

    /**
     * 이 MCP 서버에 등록된 프롬프트들.
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Prompt>>
     */
    protected array $prompts = [
        // DescribeWeatherPrompt::class,
    ];
}
```

<a name="server-registration"></a>
### 서버 등록

서버를 생성한 후에는, `routes/ai.php` 파일에 서버를 등록해야 외부에서 접근할 수 있습니다. Laravel MCP는 서버 등록을 위한 `web`(HTTP 접근)과 `local`(명령어 기반) 두 가지 방법을 제공합니다.

<a name="web-servers"></a>
### 웹 서버

웹 서버는 가장 일반적인 형태로, HTTP POST 요청을 통해 접근 가능합니다. 즉, 원격 AI 클라이언트 또는 웹 기반 통합에 적합합니다. `web` 메서드를 사용해 웹 서버를 등록할 수 있습니다.

```php
use App\Mcp\Servers\WeatherServer;
use Laravel\Mcp\Facades\Mcp;

Mcp::web('/mcp/weather', WeatherServer::class);
```

일반 라우트와 마찬가지로, 미들웨어를 적용해 웹 서버를 보호할 수도 있습니다:

```php
Mcp::web('/mcp/weather', WeatherServer::class)
    ->middleware(['throttle:mcp']);
```

<a name="local-servers"></a>
### 로컬 서버

로컬 서버는 Artisan 명령어로 실행되며, [Laravel Boost](/docs/12.x/installation#installing-laravel-boost) 같은 로컬 AI 어시스턴트 통합에 적합합니다. `local` 메서드를 통해 등록합니다:

```php
use App\Mcp\Servers\WeatherServer;
use Laravel\Mcp\Facades\Mcp;

Mcp::local('weather', WeatherServer::class);
```

로컬 서버를 등록하면 직접 `mcp:start` Artisan 명령어를 실행할 필요는 없습니다. 대신 MCP 클라이언트(AI 에이전트)에서 서버를 시작하거나, [MCP Inspector](#mcp-inspector)를 사용할 수 있습니다.

<a name="tools"></a>
## 툴

툴은 서버가 AI 클라이언트에게 노출하는 실제 기능 단위입니다. 즉, LLM이 액션을 수행하거나 코드 실행, 외부 시스템 연동이 가능하도록 만듭니다.

```php
<?php

namespace App\Mcp\Tools;

use Illuminate\Contracts\JsonSchema\JsonSchema;
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * 툴의 설명.
     */
    protected string $description = 'Fetches the current weather forecast for a specified location.';

    /**
     * 툴 요청 처리.
     */
    public function handle(Request $request): Response
    {
        $location = $request->get('location');

        // Get weather...

        return Response::text('The weather is...');
    }

    /**
     * 툴 입력 스키마 반환.
     *
     * @return array<string, \Illuminate\JsonSchema\Types\Type>
     */
    public function schema(JsonSchema $schema): array
    {
        return [
            'location' => $schema->string()
                ->description('The location to get the weather for.')
                ->required(),
        ];
    }
}
```

<a name="creating-tools"></a>
### 툴 생성

툴을 생성하려면 `make:mcp-tool` Artisan 명령어를 실행하세요:

```shell
php artisan make:mcp-tool CurrentWeatherTool
```

툴을 생성한 후에는 서버의 `$tools` 속성에 등록합니다:

```php
<?php

namespace App\Mcp\Servers;

use App\Mcp\Tools\CurrentWeatherTool;
use Laravel\Mcp\Server;

class WeatherServer extends Server
{
    /**
     * 이 MCP 서버에 등록된 툴들.
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Tool>>
     */
    protected array $tools = [
        CurrentWeatherTool::class,
    ];
}
```

#### 툴 이름, 타이틀, 설명

기본적으로, 툴의 이름과 타이틀은 클래스명에서 파생됩니다. 예를 들어, `CurrentWeatherTool` 클래스는 `current-weather`라는 이름과 `Current Weather Tool`이라는 타이틀을 갖게 됩니다. 이 값들은 `$name`, `$title` 속성을 정의하여 커스텀할 수 있습니다.

```php
class CurrentWeatherTool extends Tool
{
    /**
     * 툴의 이름.
     */
    protected string $name = 'get-optimistic-weather';

    /**
     * 툴의 타이틀.
     */
    protected string $title = 'Get Optimistic Weather Forecast';

    // ...
}
```

툴 설명은 자동 생성되지 않습니다. 항상 의미 있는 설명을 `$description` 속성으로 직접 작성해야 합니다.

```php
class CurrentWeatherTool extends Tool
{
    /**
     * 툴의 설명.
     */
    protected string $description = 'Fetches the current weather forecast for a specified location.';

    //
}
```

> [!NOTE]
> 설명은 툴 메타데이터에서 매우 중요한 부분으로, AI 모델이 툴을 언제, 어떻게 사용해야 할지 이해하는 데 도움이 됩니다.

<a name="tool-input-schemas"></a>
### 툴 입력 스키마

툴은 AI 클라이언트가 전달할 수 있는 인수의 타입과 형식을 JSON 스키마로 명확하게 정의할 수 있습니다. Laravel의 `Illuminate\Contracts\JsonSchema\JsonSchema` 빌더를 활용하여 입력 요건을 지정하세요:

```php
<?php

namespace App\Mcp\Tools;

use Illuminate\Contracts\JsonSchema\JsonSchema;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * 툴 입력 스키마 반환.
     *
     * @return array<string, \Illuminate\JsonSchema\Types\Type>
     */
    public function schema(JsonSchema $schema): array
    {
        return [
            'location' => $schema->string()
                ->description('The location to get the weather for.')
                ->required(),

            'units' => $schema->string()
                ->enum(['celsius', 'fahrenheit'])
                ->description('The temperature units to use.')
                ->default('celsius'),
        ];
    }
}
```

<a name="tool-output-schemas"></a>
### 툴 출력 스키마

툴은 [출력 스키마](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#output-schema)를 정의하여, AI 클라이언트가 반환값 구조를 파싱할 수 있도록 할 수 있습니다. `outputSchema` 메서드를 사용해 출력 구조를 정의하세요:

```php
<?php

namespace App\Mcp\Tools;

use Illuminate\Contracts\JsonSchema\JsonSchema;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * 툴 출력 스키마 반환.
     *
     * @return array<string, \Illuminate\JsonSchema\Types\Type>
     */
    public function outputSchema(JsonSchema $schema): array
    {
        return [
            'temperature' => $schema->number()
                ->description('Temperature in Celsius')
                ->required(),

            'conditions' => $schema->string()
                ->description('Weather conditions')
                ->required(),

            'humidity' => $schema->integer()
                ->description('Humidity percentage')
                ->required(),
        ];
    }
}
```

<a name="validating-tool-arguments"></a>
### 툴 인수 유효성 검증

JSON 스키마를 통해 기본적인 입력 구조를 정의할 수 있지만, 더 복잡한 유효성 검증이 필요한 경우도 많습니다.

Laravel MCP는 Laravel의 [유효성 검증 기능](/docs/12.x/validation)과 자연스럽게 통합됩니다. 툴의 `handle` 메서드 내에서 입력값을 검증할 수 있습니다.

```php
<?php

namespace App\Mcp\Tools;

use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * 툴 요청 처리.
     */
    public function handle(Request $request): Response
    {
        $validated = $request->validate([
            'location' => 'required|string|max:100',
            'units' => 'in:celsius,fahrenheit',
        ]);

        // 검증된 인수로 날씨 데이터 조회...
    }
}
```

유효성 검증 실패 시, AI 클라이언트는 반환된 에러 메시지를 바탕으로 동작합니다. 따라서 명확하고 구체적인 에러 메시지를 제공하는 것이 중요합니다:

```php
$validated = $request->validate([
    'location' => ['required','string','max:100'],
    'units' => 'in:celsius,fahrenheit',
],[
    'location.required' => 'You must specify a location to get the weather for. For example, "New York City" or "Tokyo".',
    'units.in' => 'You must specify either "celsius" or "fahrenheit" for the units.',
]);
```

#### 툴 의존성 주입

모든 MCP 툴은 Laravel [서비스 컨테이너](/docs/12.x/container)에서 해석됩니다. 따라서 툴의 생성자에 타입힌트를 사용하면 필요한 의존성이 자동으로 주입됩니다.

```php
<?php

namespace App\Mcp\Tools;

use App\Repositories\WeatherRepository;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * 생성자에서 의존성 주입.
     */
    public function __construct(
        protected WeatherRepository $weather,
    ) {}

    // ...
}
```

생성자뿐만 아니라, `handle()` 메서드의 인자로도 의존성을 타입힌트로 선언할 수 있습니다. 서비스 컨테이너가 자동으로 주입해줍니다:

```php
<?php

namespace App\Mcp\Tools;

use App\Repositories\WeatherRepository;
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * 툴 요청 처리.
     */
    public function handle(Request $request, WeatherRepository $weather): Response
    {
        $location = $request->get('location');

        $forecast = $weather->getForecastFor($location);

        // ...
    }
}
```

<a name="tool-annotations"></a>
### 툴 애너테이션

툴에 [애너테이션](https://modelcontextprotocol.io/specification/2025-06-18/schema#toolannotations)을 추가하면, AI 클라이언트에게 툴의 동작과 특징에 관한 추가 메타데이터를 제공할 수 있습니다. 애너테이션은 속성(Attribute) 방식으로 적용합니다:

```php
<?php

namespace App\Mcp\Tools;

use Laravel\Mcp\Server\Tools\Annotations\IsIdempotent;
use Laravel\Mcp\Server\Tools\Annotations\IsReadOnly;
use Laravel\Mcp\Server\Tool;

#[IsIdempotent]
#[IsReadOnly]
class CurrentWeatherTool extends Tool
{
    //
}
```

사용 가능한 애너테이션은 다음과 같습니다:

| 애너테이션            | 타입    | 설명                                                                              |
| --------------------- | ------- | --------------------------------------------------------------------------------- |
| `#[IsReadOnly]`       | boolean | 툴이 환경을 수정하지 않음을 나타냅니다.                                            |
| `#[IsDestructive]`    | boolean | 툴이 파괴적인(update, delete 등) 작업을 할 수도 있음을 나타냅니다(읽기 전용이 아닐 때 의미). |
| `#[IsIdempotent]`     | boolean | 동일한 인수로 여러 번 호출해도 추가 효과가 없음을 의미합니다(읽기 전용이 아닐 때).   |
| `#[IsOpenWorld]`      | boolean | 툴이 외부 엔터티와 상호작용할 수 있음을 가리킵니다.                               |

애너테이션 값은 boolean 인수로 명확하게 지정할 수 있습니다:

```php
use Laravel\Mcp\Server\Tools\Annotations\IsReadOnly;
use Laravel\Mcp\Server\Tools\Annotations\IsDestructive;
use Laravel\Mcp\Server\Tools\Annotations\IsOpenWorld;
use Laravel\Mcp\Server\Tools\Annotations\IsIdempotent;
use Laravel\Mcp\Server\Tool;

#[IsReadOnly(true)]
#[IsDestructive(false)]
#[IsOpenWorld(false)]
#[IsIdempotent(true)]
class CurrentWeatherTool extends Tool
{
    //
}
```

<a name="conditional-tool-registration"></a>
### 조건부 툴 등록

툴 클래스에 `shouldRegister` 메서드를 구현하면, 애플리케이션 상태, 설정, 요청 인수에 따라 특정 툴을 동적으로 등록할 수 있습니다:

```php
<?php

namespace App\Mcp\Tools;

use Laravel\Mcp\Request;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * 툴 등록 여부 결정.
     */
    public function shouldRegister(Request $request): bool
    {
        return $request?->user()?->subscribed() ?? false;
    }
}
```

`shouldRegister`가 `false`를 반환하면, 해당 툴은 사용할 수 있는 목록에 나타나지 않으며 AI 클라이언트가 호출할 수 없습니다.

<a name="tool-responses"></a>
### 툴 응답

툴은 반드시 `Laravel\Mcp\Response` 인스턴스를 반환해야 합니다. Response 클래스는 다양한 응답 타입을 생성할 수 있는 메서드를 제공합니다.

간단한 텍스트 응답일 경우 `text` 메서드를 사용하세요:

```php
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;

/**
 * 툴 요청 처리.
 */
public function handle(Request $request): Response
{
    // ...

    return Response::text('Weather Summary: Sunny, 72°F');
}
```

툴 실행 중 오류가 발생했다면 `error` 메서드를 사용할 수 있습니다:

```php
return Response::error('Unable to fetch weather data. Please try again.');
```

#### 멀티 콘텐츠 응답

툴은 여러 개의 `Response` 인스턴스 배열을 반환하여 다중 콘텐츠를 응답할 수 있습니다:

```php
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;

/**
 * 툴 요청 처리.
 *
 * @return array<int, \Laravel\Mcp\Response>
 */
public function handle(Request $request): array
{
    // ...

    return [
        Response::text('Weather Summary: Sunny, 72°F'),
        Response::text('**Detailed Forecast**\n- Morning: 65°F\n- Afternoon: 78°F\n- Evening: 70°F')
    ];
}
```

#### 구조화된(Structured) 응답

툴은 `structured` 메서드를 사용해 [구조화된 콘텐츠](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#structured-content)를 반환할 수 있습니다. 이는 AI 클라이언트가 쉽게 파싱할 수 있도록 데이터를 제공합니다.

```php
return Response::structured([
    'temperature' => 22.5,
    'conditions' => 'Partly cloudy',
    'humidity' => 65,
]);
```

텍스트와 구조화된 데이터를 함께 제공하려면 `withStructuredContent`를 사용하세요:

```php
return Response::make(
    Response::text('Weather is 22.5°C and sunny')
)->withStructuredContent([
    'temperature' => 22.5,
    'conditions' => 'Sunny',
]);
```

#### 스트리밍 응답

장시간 걸리거나 실시간 데이터가 필요한 경우, 툴의 `handle` 메서드에서 [generator](https://www.php.net/manual/en/language.generators.overview.php)를 반환하여 클라이언트에 중간 결과를 스트리밍할 수 있습니다:

```php
<?php

namespace App\Mcp\Tools;

use Generator;
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * 툴 요청 처리.
     *
     * @return \Generator<int, \Laravel\Mcp\Response>
     */
    public function handle(Request $request): Generator
    {
        $locations = $request->array('locations');

        foreach ($locations as $index => $location) {
            yield Response::notification('processing/progress', [
                'current' => $index + 1,
                'total' => count($locations),
                'location' => $location,
            ]);

            yield Response::text($this->forecastFor($location));
        }
    }
}
```

웹 기반 서버로 사용할 경우, 스트리밍 응답은 SSE(Server-Sent Events) 이벤트 스트림으로 자동 전송됩니다.

<a name="prompts"></a>
## 프롬프트

[프롬프트](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts)는 재사용 가능한 템플릿을 정의해 AI 클라이언트가 일관된 쿼리와 상호작용을 할 수 있도록 도와줍니다.

<a name="creating-prompts"></a>
### 프롬프트 생성

프롬프트를 생성하려면 `make:mcp-prompt` Artisan 명령어를 실행하세요:

```shell
php artisan make:mcp-prompt DescribeWeatherPrompt
```

프롬프트를 만든 후, 서버의 `$prompts` 속성에 등록하세요:

```php
<?php

namespace App\Mcp\Servers;

use App\Mcp\Prompts\DescribeWeatherPrompt;
use Laravel\Mcp\Server;

class WeatherServer extends Server
{
    /**
     * 이 MCP 서버에 등록된 프롬프트들.
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Prompt>>
     */
    protected array $prompts = [
        DescribeWeatherPrompt::class,
    ];
}
```

#### 프롬프트 이름, 타이틀, 설명

프롬프트의 이름과 타이틀도 클래스명에서 파생되며, `$name`, `$title` 속성을 직접 정의해 변경할 수 있습니다:

```php
class DescribeWeatherPrompt extends Prompt
{
    /**
     * 프롬프트의 이름.
     */
    protected string $name = 'weather-assistant';

    /**
     * 프롬프트의 타이틀.
     */
    protected string $title = 'Weather Assistant Prompt';

    // ...
}
```

프롬프트 설명 또한 자동 생성되지 않으므로, 의미 있는 설명을 `$description` 속성으로 정의하세요:

```php
class DescribeWeatherPrompt extends Prompt
{
    /**
     * 프롬프트의 설명.
     */
    protected string $description = 'Generates a natural-language explanation of the weather for a given location.';

    //
}
```

> [!NOTE]
> 설명은 프롬프트 메타데이터에서 매우 중요하며, AI 모델이 언제 어떤 상황에서 프롬프트를 최적으로 사용할지 판단하는 데 도움을 줍니다.

<a name="prompt-arguments"></a>
### 프롬프트 인수

프롬프트는 템플릿에서 값 대입을 위해 AI 클라이언트로부터 받아야 할 인수를 정의할 수 있습니다. `arguments` 메서드에서 인수를 반환합니다:

```php
<?php

namespace App\Mcp\Prompts;

use Laravel\Mcp\Server\Prompt;
use Laravel\Mcp\Server\Prompts\Argument;

class DescribeWeatherPrompt extends Prompt
{
    /**
     * 프롬프트 인수 반환.
     *
     * @return array<int, \Laravel\Mcp\Server\Prompts\Argument>
     */
    public function arguments(): array
    {
        return [
            new Argument(
                name: 'tone',
                description: 'The tone to use in the weather description (e.g., formal, casual, humorous).',
                required: true,
            ),
        ];
    }
}
```

<a name="validating-prompt-arguments"></a>
### 프롬프트 인수 유효성 검증

인수 정의만으로도 자동으로 기본 유효성 검증이 수행되나, 추가 검증이 필요하면 Laravel의 [유효성 검증 기능](/docs/12.x/validation)을 프롬프트의 `handle` 메서드 내부에서 사용할 수 있습니다:

```php
<?php

namespace App\Mcp\Prompts;

use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Prompt;

class DescribeWeatherPrompt extends Prompt
{
    /**
     * 프롬프트 요청 처리.
     */
    public function handle(Request $request): Response
    {
        $validated = $request->validate([
            'tone' => 'required|string|max:50',
        ]);

        $tone = $validated['tone'];

        // 받은 tone으로 프롬프트 응답 생성...
    }
}
```

유효성 검증 실패 시 명확한 에러 메시지를 제공해야 합니다:

```php
$validated = $request->validate([
    'tone' => ['required','string','max:50'],
],[
    'tone.*' => 'You must specify a tone for the weather description. Examples include "formal", "casual", or "humorous".',
]);
```

<a name="prompt-dependency-injection"></a>
### 프롬프트 의존성 주입

모든 MCP 프롬프트도 Laravel [서비스 컨테이너](/docs/12.x/container)를 통해 해석되어, 생성자와 메서드에 타입힌트된 의존성이 자동으로 주입됩니다.

```php
<?php

namespace App\Mcp\Prompts;

use App\Repositories\WeatherRepository;
use Laravel\Mcp\Server\Prompt;

class DescribeWeatherPrompt extends Prompt
{
    /**
     * 생성자에서 의존성 주입.
     */
    public function __construct(
        protected WeatherRepository $weather,
    ) {}

    //
}
```

메서드에서도 의존성을 타입힌트로 선언 가능하며, 컨테이너가 자동 주입합니다:

```php
<?php

namespace App\Mcp\Prompts;

use App\Repositories\WeatherRepository;
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Prompt;

class DescribeWeatherPrompt extends Prompt
{
    /**
     * 프롬프트 요청 처리.
     */
    public function handle(Request $request, WeatherRepository $weather): Response
    {
        $isAvailable = $weather->isServiceAvailable();

        // ...
    }
}
```

<a name="conditional-prompt-registration"></a>
### 조건부 프롬프트 등록

프롬프트 클래스에서 `shouldRegister` 메서드를 구현하면, 상황에 맞추어 프롬프트의 등록 여부를 제어할 수 있습니다:

```php
<?php

namespace App\Mcp\Prompts;

use Laravel\Mcp\Request;
use Laravel\Mcp\Server\Prompt;

class CurrentWeatherPrompt extends Prompt
{
    /**
     * 프롬프트 등록 여부 결정.
     */
    public function shouldRegister(Request $request): bool
    {
        return $request?->user()?->subscribed() ?? false;
    }
}
```

`shouldRegister`가 `false`면 해당 프롬프트는 목록에 나타나지 않으며 AI 클라이언트가 사용할 수 없습니다.

<a name="prompt-responses"></a>
### 프롬프트 응답

프롬프트는 단일 `Laravel\Mcp\Response` 또는 여러 개의 `Laravel\Mcp\Response` 인스턴스(이터러블)를 반환할 수 있습니다. 이는 AI 클라이언트로 전송될 콘텐츠를 캡슐화합니다:

```php
<?php

namespace App\Mcp\Prompts;

use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Prompt;

class DescribeWeatherPrompt extends Prompt
{
    /**
     * 프롬프트 요청 처리.
     *
     * @return array<int, \Laravel\Mcp\Response>
     */
    public function handle(Request $request): array
    {
        $tone = $request->string('tone');

        $systemMessage = "You are a helpful weather assistant. Please provide a weather description in a {$tone} tone.";

        $userMessage = "What is the current weather like in New York City?";

        return [
            Response::text($systemMessage)->asAssistant(),
            Response::text($userMessage),
        ];
    }
}
```

`asAssistant()`를 사용하면 해당 메시지가 AI 어시스턴트의 응답임을 표시할 수 있습니다. 일반 메시지는 사용자 입력으로 처리됩니다.

<a name="resources"></a>
## 리소스

[리소스](https://modelcontextprotocol.io/specification/2025-06-18/server/resources)는 AI 클라이언트가 언어 모델과 상호작용할 때 참조할 수 있는 데이터나 콘텐츠를 노출합니다. 즉, 정적 또는 동적 문서, 설정, 데이터 등 다양한 배경지식을 제공할 수 있습니다.

<a name="creating-resources"></a>
## 리소스 생성

리소스 생성은 `make:mcp-resource` Artisan 명령어로 시작합니다:

```shell
php artisan make:mcp-resource WeatherGuidelinesResource
```

생성한 리소스를 서버의 `$resources` 속성에 등록하세요:

```php
<?php

namespace App\Mcp\Servers;

use App\Mcp\Resources\WeatherGuidelinesResource;
use Laravel\Mcp\Server;

class WeatherServer extends Server
{
    /**
     * 이 MCP 서버에 등록된 리소스들.
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Resource>>
     */
    protected array $resources = [
        WeatherGuidelinesResource::class,
    ];
}
```

#### 리소스 이름, 타이틀, 설명

리소스의 이름, 타이틀도 클래스명에서 파생되며, `$name`, `$title` 속성으로 커스텀할 수 있습니다:

```php
class WeatherGuidelinesResource extends Resource
{
    /**
     * 리소스의 이름.
     */
    protected string $name = 'weather-api-docs';

    /**
     * 리소스의 타이틀.
     */
    protected string $title = 'Weather API Documentation';

    // ...
}
```

마찬가지로, 리소스 설명도 `$description` 속성을 이용해 명확하게 작성합니다:

```php
class WeatherGuidelinesResource extends Resource
{
    /**
     * 리소스의 설명.
     */
    protected string $description = 'Comprehensive guidelines for using the Weather API.';

    //
}
```

> [!NOTE]
> 설명은 리소스 메타데이터에서 매우 중요한 부분입니다. AI 모델이 해당 리소스를 어떤 때, 어떻게 활용해야 할지 판단하는 데 도움이 됩니다.

<a name="resource-templates"></a>
### 리소스 템플릿

[리소스 템플릿](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#resource-templates)을 사용하면 변수 영역을 포함하는 URI 패턴을 활용해 동적 리소스를 제공합니다. 정적 URI가 아니라 패턴 기반으로 여러 리소스를 효율적으로 처리할 수 있습니다.

#### 리소스 템플릿 생성

리소스 클래스에 `HasUriTemplate` 인터페이스를 구현하고, `uriTemplate` 메서드에서 `UriTemplate` 인스턴스를 반환하세요:

```php
<?php

namespace App\Mcp\Resources;

use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Contracts\HasUriTemplate;
use Laravel\Mcp\Server\Resource;
use Laravel\Mcp\Support\UriTemplate;

class UserFileResource extends Resource implements HasUriTemplate
{
    /**
     * 리소스의 설명.
     */
    protected string $description = 'Access user files by ID';

    /**
     * 리소스의 MIME 타입.
     */
    protected string $mimeType = 'text/plain';

    /**
     * 이 리소스의 URI 템플릿 반환.
     */
    public function uriTemplate(): UriTemplate
    {
        return new UriTemplate('file://users/{userId}/files/{fileId}');
    }

    /**
     * 리소스 요청 처리.
     */
    public function handle(Request $request): Response
    {
        $userId = $request->get('userId');
        $fileId = $request->get('fileId');

        // 파일 내용 반환...

        return Response::text($content);
    }
}
```

`HasUriTemplate`을 구현한 리소스는 템플릿으로 등록되어, AI 클라이언트가 패턴에 맞는 URI로 해당 리소스를 요청할 수 있습니다. URI에 포함된 변수는 `handle` 메서드 요청 객체에 자동으로 할당됩니다.

#### URI 템플릿 문법

URI 템플릿은 `{}`로 감싼 플레이스홀더로 변수 구간을 정의합니다:

```php
new UriTemplate('file://users/{userId}');
new UriTemplate('file://users/{userId}/files/{fileId}');
new UriTemplate('https://api.example.com/{version}/{resource}/{id}');
```

#### 템플릿 변수 접근

매칭된 URI 템플릿 변수는 요청 객체의 `get` 메서드로 조회할 수 있습니다:

```php
<?php

namespace App\Mcp\Resources;

use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Contracts\HasUriTemplate;
use Laravel\Mcp\Server\Resource;
use Laravel\Mcp\Support\UriTemplate;

class UserProfileResource extends Resource implements HasUriTemplate
{
    public function uriTemplate(): UriTemplate
    {
        return new UriTemplate('file://users/{userId}/profile');
    }

    public function handle(Request $request): Response
    {
        // 추출된 변수 접근
        $userId = $request->get('userId');

        // 전체 요청 URI 필요 시
        $uri = $request->uri();

        // 사용자 프로필 조회...

        return Response::text("Profile for user {$userId}");
    }
}
```

요청 객체는 추출된 각 변수와 원래 요청 URI를 모두 제공합니다.

<a name="resource-uri-and-mime-type"></a>
### 리소스 URI 및 MIME 타입

각 리소스는 고유한 URI와 MIME 타입을 가집니다. AI 클라이언트는 이를 통해 리소스의 포맷을 이해할 수 있습니다.

기본적으로 리소스 URI는 리소스 이름을 토대로 자동 생성되며, 예를 들어 `WeatherGuidelinesResource`는 `weather://resources/weather-guidelines` URI를 사용합니다. 기본 MIME 타입은 `text/plain`입니다.

직접 지정하려면 `$uri`, `$mimeType` 속성을 정의합니다:

```php
<?php

namespace App\Mcp\Resources;

use Laravel\Mcp\Server\Resource;

class WeatherGuidelinesResource extends Resource
{
    /**
     * 리소스의 URI.
     */
    protected string $uri = 'weather://resources/guidelines';

    /**
     * 리소스의 MIME 타입.
     */
    protected string $mimeType = 'application/pdf';
}
```

URI와 MIME 타입은 AI 클라이언트가 적절히 리소스를 처리하는 데 도움을 줍니다.

<a name="resource-request"></a>
### 리소스 요청

툴이나 프롬프트와 달리, 리소스는 입력 스키마나 인수 정의를 별도로 갖지 않습니다. 그러나 `handle` 메서드 안에서 요청 객체는 자유롭게 사용할 수 있습니다.

```php
<?php

namespace App\Mcp\Resources;

use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Resource;

class WeatherGuidelinesResource extends Resource
{
    /**
     * 리소스 요청 처리.
     */
    public function handle(Request $request): Response
    {
        // ...
    }
}
```

<a name="resource-dependency-injection"></a>
### 리소스 의존성 주입

모든 리소스는 Laravel [서비스 컨테이너](/docs/12.x/container)에서 해석되므로, 생성자나 메서드에 타입힌트하면 의존성이 자동으로 주입됩니다.

```php
<?php

namespace App\Mcp\Resources;

use App\Repositories\WeatherRepository;
use Laravel\Mcp\Server\Resource;

class WeatherGuidelinesResource extends Resource
{
    /**
     * 생성자에서 의존성 주입.
     */
    public function __construct(
        protected WeatherRepository $weather,
    ) {}

    // ...
}
```

메서드 의존성 주입도 가능합니다:

```php
<?php

namespace App\Mcp\Resources;

use App\Repositories\WeatherRepository;
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Resource;

class WeatherGuidelinesResource extends Resource
{
    /**
     * 리소스 요청 처리.
     */
    public function handle(WeatherRepository $weather): Response
    {
        $guidelines = $weather->guidelines();

        return Response::text($guidelines);
    }
}
```

<a name="resource-annotations"></a>
### 리소스 애너테이션

리소스 역시 [애너테이션](https://modelcontextprotocol.io/specification/2025-06-18/schema#resourceannotations)으로 AI 클라이언트에 추가 메타데이터를 보강할 수 있습니다. 애너테이션은 속성(Attribute) 방식으로 추가합니다:

```php
<?php

namespace App\Mcp\Resources;

use Laravel\Mcp\Enums\Role;
use Laravel\Mcp\Server\Annotations\Audience;
use Laravel\Mcp\Server\Annotations\LastModified;
use Laravel\Mcp\Server\Annotations\Priority;
use Laravel\Mcp\Server\Resource;

#[Audience(Role::User)]
#[LastModified('2025-01-12T15:00:58Z')]
#[Priority(0.9)]
class UserDashboardResource extends Resource
{
    //
}
```

사용 가능한 애너테이션은 다음과 같습니다:

| 애너테이션       | 타입          | 설명                                                                |
| ---------------- | ------------- | ------------------------------------------------------------------- |
| `#[Audience]`    | Role 또는 배열 | 의도된 오디언스(`Role::User`, `Role::Assistant` 등)를 지정           |
| `#[Priority]`    | float         | 0.0~1.0 사이의 리소스 중요도 점수                                    |
| `#[LastModified]`| string        | 리소스가 마지막으로 수정된 시점을 ISO 8601 형식으로 지정             |

<a name="conditional-resource-registration"></a>
### 조건부 리소스 등록

리소스에서도 `shouldRegister` 메서드 구현을 통해 동적으로 등록 여부를 제어할 수 있습니다:

```php
<?php

namespace App\Mcp\Resources;

use Laravel\Mcp\Request;
use Laravel\Mcp\Server\Resource;

class WeatherGuidelinesResource extends Resource
{
    /**
     * 리소스 등록 여부 결정.
     */
    public function shouldRegister(Request $request): bool
    {
        return $request?->user()?->subscribed() ?? false;
    }
}
```

`shouldRegister`가 `false`를 반환하면, 해당 리소스는 목록에 노출되지 않으며 AI 클라이언트가 사용할 수 없습니다.

<a name="resource-responses"></a>
### 리소스 응답

리소스는 반드시 `Laravel\Mcp\Response`를 반환해야 합니다. 간단한 텍스트를 반환할 땐 `text` 메서드를 사용하세요:

```php
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;

/**
 * 리소스 요청 처리.
 */
public function handle(Request $request): Response
{
    // ...

    return Response::text($weatherData);
}
```

#### Blob 응답

Blob(바이너리) 데이터를 반환하려면 `blob` 메서드를 사용하세요:

```php
return Response::blob(file_get_contents(storage_path('weather/radar.png')));
```

이 때 리소스 클래스의 `$mimeType` 속성이 MIME 타입으로 사용됩니다:

```php
<?php

namespace App\Mcp\Resources;

use Laravel\Mcp\Server\Resource;

class WeatherGuidelinesResource extends Resource
{
    /**
     * 리소스의 MIME 타입.
     */
    protected string $mimeType = 'image/png';

    //
}
```

#### 오류 응답

리소스 조회 중 오류가 발생하면 `error()` 메서드를 사용하세요:

```php
return Response::error('Unable to fetch weather data for the specified location.');
```

<a name="metadata"></a>
## 메타데이터

Laravel MCP는 [MCP 사양](https://modelcontextprotocol.io/specification/2025-06-18/basic#meta)에 정의된 `_meta` 필드를 지원합니다. 이는 MCP 클라이언트나 통합 환경에 따라 필요할 수 있습니다. 메타데이터는 MCP의 모든 프리미티브(툴, 리소스, 프롬프트) 및 그 응답에 적용할 수 있습니다.

개별 응답에 메타데이터를 첨부하려면 `withMeta` 메서드를 사용합니다:

```php
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;

/**
 * 툴 요청 처리.
 */
public function handle(Request $request): Response
{
    return Response::text('The weather is sunny.')
        ->withMeta(['source' => 'weather-api', 'cached' => true]);
}
```

응답 전체(envelope) 단위에 메타데이터를 적용하려면 `Response::make()`로 래핑한 후 `withMeta`를 사용하세요:

```php
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\ResponseFactory;

/**
 * 툴 요청 처리.
 */
public function handle(Request $request): ResponseFactory
{
    return Response::make(
        Response::text('The weather is sunny.')
    )->withMeta(['request_id' => '12345']);
}
```

툴, 리소스, 프롬프트 클래스 자체에 메타데이터를 적용하려면 `$meta` 속성을 정의하세요:

```php
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    protected string $description = 'Fetches the current weather forecast.';

    protected ?array $meta = [
        'version' => '2.0',
        'author' => 'Weather Team',
    ];

    // ...
}
```

<a name="authentication"></a>
## 인증(Authentication)

웹 MCP 서버_routes에 미들웨어를 추가해 인증을 적용할 수 있습니다. 즉, 서버의 모든 기능을 사용하기 위해 사용자는 반드시 인증을 거쳐야 합니다.

MCP 서버 접근 인증 방식은 크게 [Laravel Sanctum](/docs/12.x/sanctum)의 간단한 토큰 방식, 또는 `Authorization` HTTP 헤더로 토큰을 전달하는 방법, 그리고 [Laravel Passport](/docs/12.x/passport)를 활용한 OAuth 방식이 있습니다.

<a name="oauth"></a>
### OAuth 2.1

웹 MCP 서버를 보호하는 가장 강력한 방법은 [Laravel Passport](/docs/12.x/passport)를 통한 OAuth 인증입니다.

OAuth로 MCP 서버를 인증하려면 `Mcp::oauthRoutes` 메서드를 `routes/ai.php` 파일에서 호출해 필요한 OAuth2 라우트를 등록합니다. 이어서 `Mcp::web` 라우트에 Passport의 `auth:api` 미들웨어를 적용합니다:

```php
use App\Mcp\Servers\WeatherExample;
use Laravel\Mcp\Facades\Mcp;

Mcp::oauthRoutes();

Mcp::web('/mcp/weather', WeatherExample::class)
    ->middleware('auth:api');
```

#### Passport 새 설치 시

아직 Laravel Passport를 사용하지 않는다면, [Passport 설치 가이드](/docs/12.x/passport#installation)를 따라 진행해야 합니다. OAuthenticatable 모델, 인증 가드, 패스포트 키 등이 필요합니다.

그리고 Laravel MCP에서 제공하는 Passport 인가 뷰를 퍼블리시합니다:

```shell
php artisan vendor:publish --tag=mcp-views
```

그리고 `AppServiceProvider`의 `boot` 메서드에서 아래처럼 Passport에 커스텀 인가 뷰를 지정하세요:

```php
use Laravel\Passport\Passport;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::authorizationView(function ($parameters) {
        return view('mcp.authorize', $parameters);
    });
}
```

이 뷰는 사용자가 인증 과정에서, AI 에이전트의 인증 시도를 승인 또는 거부할 때 노출됩니다.

![Authorization screen example](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABOAAAAROCAMAAABKc73cAAAA81BMVEX...생략)

> [!NOTE]
> 이 시나리오에서는 OAuth를 기본 모델 인증에 대한 변환 계층으로 사용합니다. OAuth의 스코프 등 다양한 요소는 무시될 수 있습니다.

#### 기존 Passport 설치 환경

이미 Passport를 사용 중이라면, MCP는 기존 Passport 인프라 내에서 바로 동작합니다. 단, 커스텀 스코프는 현재 지원되지 않으며 OAuth가 모델 인증의 변환 계층 역할만 합니다.

`Mcp::oauthRoutes`는 `mcp:use`라는 단일 스코프만을 지원하며, 라우트 추가 및 사용을 처리합니다.

#### Passport vs. Sanctum

Model Context Protocol 사양상, OAuth2.1이 공식 인증 방식이며 MCP 클라이언트 호환성도 가장 넓습니다. 가급적 Passport 사용을 권장합니다.

이미 [Sanctum](/docs/12.x/sanctum)을 활용 중이라면, 꼭 필요하지 않다면 Passport 추가 없이 Sanctum으로 운영하는 것이 간편합니다.

<a name="sanctum"></a>
### Sanctum

[MCP 서버를 Sanctum](/docs/12.x/sanctum)으로 보호하려면, 해당 서버의 `routes/ai.php` 파일 라우트에 Sanctum 인증 미들웨어만 적용하면 됩니다. MCP 클라이언트에서는 `Authorization: Bearer <token>` 헤더를 요청에 포함해야 합니다:

```php
use App\Mcp\Servers\WeatherExample;
use Laravel\Mcp\Facades\Mcp;

Mcp::web('/mcp/demo', WeatherExample::class)
    ->middleware('auth:sanctum');
```

#### 커스텀 MCP 인증

자체 API 토큰을 사용하는 경우, 원하는 미들웨어를 MCP `web` 라우트에 할당하세요. 커스텀 미들웨어에서 `Authorization` 헤더를 직접 검사해 MCP 요청 인증을 처리할 수 있습니다.

<a name="authorization"></a>
## 인가(Authorization)

현재 인증된 사용자는 `$request->user()`로 접근할 수 있습니다. 이를 활용해 MCP 툴, 리소스에서 [인가(Authorization) 체크](/docs/12.x/authorization)를 할 수 있습니다:

```php
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;

/**
 * 툴 요청 처리.
 */
public function handle(Request $request): Response
{
    if (! $request->user()->can('read-weather')) {
        return Response::error('Permission denied.');
    }

    // ...
}
```

<a name="testing-servers"></a>
## 서버 테스트

MCP 서버는 내장된 MCP Inspector 또는 단위 테스트 코드로 직접 테스트할 수 있습니다.

<a name="mcp-inspector"></a>
### MCP Inspector

[MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector)는 MCP 서버를 상호작용적으로 테스트하고 디버깅할 수 있는 도구입니다. 서버 연결, 인증 체크, 툴/리소스/프롬프트의 동작 확인이 모두 가능합니다.

등록된 어떤 서버든 아래처럼 Inspector를 실행해볼 수 있습니다:

```shell
# 웹 서버 연결...
php artisan mcp:inspector mcp/weather

# "weather"라는 이름의 로컬 서버...
php artisan mcp:inspector weather
```

이 명령어는 MCP Inspector를 실행하고, 클라이언트에 복사해 쓸 수 있는 연결 정보를 제공합니다. 인증이 필요한 서버의 경우, 연결 시 반드시 `Authorization` 등의 헤더를 추가 입력해야 합니다.

<a name="unit-tests"></a>
### 단위 테스트

MCP 서버, 툴, 리소스, 프롬프트 모두에 대해 단위 테스트를 작성할 수 있습니다.

먼저 테스트 케이스를 생성한 후, 테스트 대상 프리미티브를 서버에 실행하세요. 예를 들어 `WeatherServer`의 툴을 테스트하려면:

```php tab=Pest
test('tool', function () {
    $response = WeatherServer::tool(CurrentWeatherTool::class, [
        'location' => 'New York City',
        'units' => 'fahrenheit',
    ]);

    $response
        ->assertOk()
        ->assertSee('The current weather in New York City is 72°F and sunny.');
});
```

```php tab=PHPUnit
/**
 * 툴 테스트.
 */
public function test_tool(): void
{
    $response = WeatherServer::tool(CurrentWeatherTool::class, [
        'location' => 'New York City',
        'units' => 'fahrenheit',
    ]);

    $response
        ->assertOk()
        ->assertSee('The current weather in New York City is 72°F and sunny.');
}
```

이와 동일하게 프롬프트나 리소스도 테스트할 수 있습니다:

```php
$response = WeatherServer::prompt(...);
$response = WeatherServer::resource(...);
```

또한, `actingAs`를 체이닝하면 인증된 사용자로 테스트할 수도 있습니다:

```php
$response = WeatherServer::actingAs($user)->tool(...);
```

응답 객체를 받은 후, 각종 assertion 메서드로 응답의 상태와 내용을 검증할 수 있습니다.

성공 응답 검증은 `assertOk`를 사용합니다. 오류가 없음을 확인합니다:

```php
$response->assertOk();
```

특정 텍스트가 포함되어 있는지 확인하려면 `assertSee`를 사용합니다:

```php
$response->assertSee('The current weather in New York City is 72°F and sunny.');
```

오류가 포함되어 있는지 검증할 땐 `assertHasErrors`, 포함되어 있지 않은 경우 `assertHasNoErrors`를 사용하세요:

```php
$response->assertHasErrors();

$response->assertHasErrors([
    'Something went wrong.',
]);

$response->assertHasNoErrors();
```

메타데이터가 올바른지 검증하려면 `assertName()`, `assertTitle()`, `assertDescription()`를 사용할 수 있습니다:

```php
$response->assertName('current-weather');
$response->assertTitle('Current Weather Tool');
$response->assertDescription('Fetches the current weather forecast for a specified location.');
```

노티피케이션 전송 검증은 `assertSentNotification`, `assertNotificationCount`를 사용합니다:

```php
$response->assertSentNotification('processing/progress', [
    'step' => 1,
    'total' => 5,
]);

$response->assertSentNotification('processing/progress', [
    'step' => 2,
    'total' => 5,
]);

$response->assertNotificationCount(5);
```

마지막으로, 원시 응답 내용을 직접 검사하려면 `dd` 또는 `dump` 메서드를 사용하세요:

```php
$response->dd();
$response->dump();
```