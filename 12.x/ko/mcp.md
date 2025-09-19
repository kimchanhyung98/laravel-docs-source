# Laravel MCP (Laravel MCP)

- [소개](#introduction)
- [설치](#installation)
    - [라우트 퍼블리싱](#publishing-routes)
- [서버 생성](#creating-servers)
    - [서버 등록](#server-registration)
    - [웹 서버](#web-servers)
    - [로컬 서버](#local-servers)
- [툴 (Tools)](#tools)
    - [툴 생성](#creating-tools)
    - [툴 입력 스키마](#tool-input-schemas)
    - [툴 인수 유효성 검증](#validating-tool-arguments)
    - [툴 의존성 주입 (Dependency Injection)](#tool-dependency-injection)
    - [툴 애노테이션](#tool-annotations)
    - [조건부 툴 등록](#conditional-tool-registration)
    - [툴 응답](#tool-responses)
- [프롬프트 (Prompts)](#prompts)
    - [프롬프트 생성](#creating-prompts)
    - [프롬프트 인수](#prompt-arguments)
    - [프롬프트 인수 유효성 검증](#validating-prompt-arguments)
    - [프롬프트 의존성 주입](#prompt-dependency-injection)
    - [조건부 프롬프트 등록](#conditional-prompt-registration)
    - [프롬프트 응답](#prompt-responses)
- [리소스 (Resources)](#creating-resources)
    - [리소스 생성](#creating-resources)
    - [리소스 URI 및 MIME 타입](#resource-uri-and-mime-type)
    - [리소스 요청](#resource-request)
    - [리소스 의존성 주입](#resource-dependency-injection)
    - [조건부 리소스 등록](#conditional-resource-registration)
    - [리소스 응답](#resource-responses)
- [인증](#authentication)
    - [OAuth 2.1](#oauth)
    - [Sanctum](#sanctum)
- [인가](#authorization)
- [서버 테스트](#testing-servers)
    - [MCP 인스펙터](#mcp-inspector)
    - [유닛 테스트](#unit-tests)

<a name="introduction"></a>
## 소개

[Laravel MCP](https://github.com/laravel/mcp)는 [Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro)을 통해 AI 클라이언트가 여러분의 Laravel 애플리케이션과 상호작용할 수 있도록 간결하면서도 우아한 방식을 제공합니다. 이 패키지는 서버, 툴, 리소스, 프롬프트를 정의할 수 있는 표현력 있고 유연한 인터페이스를 제공하며, 이를 통해 AI 기반 상호작용을 실현할 수 있습니다.

<a name="installation"></a>
## 설치

먼저 Composer 패키지 매니저를 사용해 Laravel MCP를 프로젝트에 설치합니다:

```shell
composer require laravel/mcp
```

<a name="publishing-routes"></a>
### 라우트 퍼블리싱

Laravel MCP 설치 후, MCP 서버를 정의하는 `routes/ai.php` 파일을 퍼블리시하려면 `vendor:publish` 아티즌 명령어를 실행하세요:

```shell
php artisan vendor:publish --tag=ai-routes
```

이 명령어는 애플리케이션의 `routes` 디렉토리에 `routes/ai.php` 파일을 생성하며, 이 파일에서 MCP 서버를 등록하게 됩니다.

<a name="creating-servers"></a>
## 서버 생성

`make:mcp-server` 아티즌 명령어를 사용해 MCP 서버를 생성할 수 있습니다. 서버는 툴, 리소스, 프롬프트와 같은 MCP 기능들을 AI 클라이언트에 노출하는 중앙 통신 지점 역할을 합니다:

```shell
php artisan make:mcp-server WeatherServer
```

이 명령어를 실행하면 `app/Mcp/Servers` 디렉토리에 새로운 서버 클래스가 생성됩니다. 생성된 서버 클래스는 Laravel MCP의 기본 `Laravel\Mcp\Server` 클래스를 확장하며, 툴, 리소스, 프롬프트 등록용 속성을 제공합니다:

```php
<?php

namespace App\Mcp\Servers;

use Laravel\Mcp\Server;

class WeatherServer extends Server
{
    /**
     * MCP 서버 이름
     */
    protected string $name = 'Weather Server';

    /**
     * MCP 서버 버전
     */
    protected string $version = '1.0.0';

    /**
     * LLM에 대한 MCP 서버 안내문.
     */
    protected string $instructions = 'This server provides weather information and forecasts.';

    /**
     * 이 MCP 서버에 등록된 툴 목록.
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Tool>>
     */
    protected array $tools = [
        // GetCurrentWeatherTool::class,
    ];

    /**
     * 이 MCP 서버에 등록된 리소스 목록.
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Resource>>
     */
    protected array $resources = [
        // WeatherGuidelinesResource::class,
    ];

    /**
     * 이 MCP 서버에 등록된 프롬프트 목록.
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

서버를 생성한 후에는 `routes/ai.php` 파일에서 서버를 등록해야 사용할 수 있습니다. Laravel MCP는 서버 등록 시 HTTP 접근용 `web` 방식과 커맨드라인용 `local` 방식을 제공합니다.

<a name="web-servers"></a>
### 웹 서버

웹 서버는 가장 일반적으로 사용되는 서버 유형으로, HTTP POST 요청을 통해 접근할 수 있습니다. 이 방식은 원격 AI 클라이언트나 웹 기반 통합에 이상적입니다. `web` 메서드를 사용해 웹 서버를 등록하세요:

```php
use App\Mcp\Servers\WeatherServer;
use Laravel\Mcp\Facades\Mcp;

Mcp::web('/mcp/weather', WeatherServer::class);
```

일반 라우트처럼 미들웨어를 적용해 웹 서버를 보호할 수 있습니다:

```php
Mcp::web('/mcp/weather', WeatherServer::class)
    ->middleware(['throttle:mcp']);
```

<a name="local-servers"></a>
### 로컬 서버

로컬 서버는 아티즌 명령어로 동작하며, [Laravel Boost](/docs/12.x/installation#installing-laravel-boost)와 같은 로컬 AI 어시스턴트 통합에 적합합니다. `local` 메서드를 사용해 로컬 서버를 등록할 수 있습니다:

```php
use App\Mcp\Servers\WeatherServer;
use Laravel\Mcp\Facades\Mcp;

Mcp::local('weather', WeatherServer::class);
```

등록 후에는, 직접 `mcp:start` 아티즌 명령어를 수동으로 실행할 필요가 없습니다. 대신 MCP 클라이언트(AI 에이전트)에서 서버 시작을 트리거하거나, [MCP 인스펙터](#mcp-inspector)를 사용할 수 있습니다.

<a name="tools"></a>
## 툴 (Tools)

툴은 서버가 AI 클라이언트에서 호출할 수 있는 기능을 외부에 공개할 수 있게 합니다. 이를 통해 언어 모델이 실제 코드를 실행하거나 외부 시스템과 상호작용하는 등 다양한 작업을 수행할 수 있습니다:

```php
<?php

namespace App\Mcp\Tools;

use Illuminate\JsonSchema\JsonSchema;
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * 툴의 설명
     */
    protected string $description = 'Fetches the current weather forecast for a specified location.';

    /**
     * 툴 요청 처리
     */
    public function handle(Request $request): Response
    {
        $location = $request->get('location');

        // Get weather...

        return Response::text('The weather is...');
    }

    /**
     * 툴 입력 스키마 반환
     *
     * @return array<string, \Illuminate\JsonSchema\JsonSchema>
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

툴을 생성하려면 `make:mcp-tool` 아티즌 명령어를 실행하세요:

```shell
php artisan make:mcp-tool CurrentWeatherTool
```

툴을 생성한 뒤에는 서버의 `$tools` 속성에 등록해야 합니다:

```php
<?php

namespace App\Mcp\Servers;

use App\Mcp\Tools\CurrentWeatherTool;
use Laravel\Mcp\Server;

class WeatherServer extends Server
{
    /**
     * 이 MCP 서버에 등록된 툴 목록.
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Tool>>
     */
    protected array $tools = [
        CurrentWeatherTool::class,
    ];
}
```

<a name="tool-name-title-description"></a>
#### 툴 이름, 타이틀, 설명

기본적으로 툴의 이름(name)과 타이틀(title)은 클래스명을 기준으로 자동 지정됩니다. 예를 들어 `CurrentWeatherTool` 클래스는 이름이 `current-weather`, 타이틀이 `Current Weather Tool`이 됩니다. `$name`, `$title` 속성을 정의하여 원하는 값으로 커스텀할 수 있습니다:

```php
class CurrentWeatherTool extends Tool
{
    /**
     * 툴의 이름
     */
    protected string $name = 'get-optimistic-weather';

    /**
     * 툴의 타이틀
     */
    protected string $title = 'Get Optimistic Weather Forecast';

    // ...
}
```

툴 설명은 자동 생성되지 않으므로, 항상 의미 있는 설명을 `$description` 속성에 직접 작성해야 합니다:

```php
class CurrentWeatherTool extends Tool
{
    /**
     * 툴의 설명
     */
    protected string $description = 'Fetches the current weather forecast for a specified location.';

    //
}
```

> [!NOTE]
> 설명은 툴 메타데이터의 핵심 요소로, AI 모델이 해당 툴을 효과적으로 사용할 시점과 방법을 이해하는 데 도움이 됩니다.

<a name="tool-input-schemas"></a>
### 툴 입력 스키마

툴은 입력 스키마를 정의해 AI 클라이언트로부터 어떤 인수를 받을지 명확히 할 수 있습니다. Laravel의 `Illuminate\JsonSchema\JsonSchema` 빌더를 사용해 입력 요구사항을 정의하세요:

```php
<?php

namespace App\Mcp\Tools;

use Illuminate\JsonSchema\JsonSchema;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * 툴 입력 스키마 반환
     *
     * @return array<string, JsonSchema>
     */
    public function schema(JsonSchema $schema): array
    {
        return [
            'location' => $schema->string()
                ->description('The location to get the weather for.')
                ->required(),

            'units' => $schema->enum(['celsius', 'fahrenheit'])
                ->description('The temperature units to use.')
                ->default('celsius'),
        ];
    }
}
```

<a name="validating-tool-arguments"></a>
### 툴 인수 유효성 검증

JSON Schema 정의는 기본적인 구조와 타입 제약만 제공하므로, 더 복잡한 유효성 검증이 필요한 경우도 있습니다.

Laravel MCP는 Laravel의 [유효성 검증 기능](/docs/12.x/validation)과 자연스럽게 연동됩니다. 툴의 `handle` 메서드 내에서 인수 유효성 검증을 할 수 있습니다:

```php
<?php

namespace App\Mcp\Tools;

use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * 툴 요청 처리
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

유효성 검증 실패 시 AI 클라이언트는 반환된 에러 메시지에 따라 동작하므로, 명확하고 구체적인 에러 메시지를 제공하는 것이 중요합니다:

```php
$validated = $request->validate([
    'location' => ['required','string','max:100'],
    'units' => 'in:celsius,fahrenheit',
],[
    'location.required' => 'You must specify a location to get the weather for. For example, "New York City" or "Tokyo".',
    'units.in' => 'You must specify either "celsius" or "fahrenheit" for the units.',
]);
```

<a name="tool-dependency-injection"></a>
#### 툴 의존성 주입 (Dependency Injection)

모든 MCP 툴은 Laravel [서비스 컨테이너](/docs/12.x/container)에 의해 해석되므로, 생성자에서 타입힌트로 의존성을 선언하면 자동으로 인스턴스가 주입됩니다:

```php
<?php

namespace App\Mcp\Tools;

use App\Repositories\WeatherRepository;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * 새로운 툴 인스턴스 생성자
     */
    public function __construct(
        protected WeatherRepository $weather,
    ) {}

    // ...
}
```

생성자 외에도, 툴의 `handle()` 메서드의 인자로도 타입힌트 선언을 통해 의존성 주입을 받을 수 있습니다:

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
     * 툴 요청 처리
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
### 툴 애노테이션

툴에 [애노테이션](https://modelcontextprotocol.io/specification/2025-06-18/schema#toolannotations)을 추가해 AI 클라이언트에 추가 메타데이터를 제공할 수 있습니다. 애노테이션은 툴의 동작이나 특성을 AI 모델이 더 정확하게 이해하도록 돕습니다. 애노테이션은 속성(Attribute)을 통해 선언합니다:

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

사용 가능한 애노테이션에는 다음이 있습니다:

| 애노테이션            | 타입    | 설명                                                                                         |
|-----------------------|---------|---------------------------------------------------------------------------------------------|
| `#[IsReadOnly]`       | boolean | 툴이 환경을 변경하지 않음을 나타냅니다.                                                      |
| `#[IsDestructive]`    | boolean | 툴이 파괴적인(Destructive) 업데이트를 할 수 있음을 나타냅니다. (읽기 전용이 아닐 때 의미가 있습니다.) |
| `#[IsIdempotent]`     | boolean | 동일 인수로 반복 호출해도 추가 효과가 없음을 나타냅니다. (읽기 전용이 아닐 때 의미가 있습니다.)   |
| `#[IsOpenWorld]`      | boolean | 툴이 외부 엔티티와 상호작용할 수 있음을 의미합니다.                                         |

<a name="conditional-tool-registration"></a>
### 조건부 툴 등록

`shouldRegister` 메서드를 구현해 애플리케이션 상태, 설정, 요청 파라미터 등에 따라 툴 등록 여부를 동적으로 제어할 수 있습니다:

```php
<?php

namespace App\Mcp\Tools;

use Laravel\Mcp\Request;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * 툴 등록 여부 판단
     */
    public function shouldRegister(Request $request): bool
    {
        return $request?->user()?->subscribed() ?? false;
    }
}
```

`shouldRegister`가 `false`를 반환하면 해당 툴은 등록 목록에 나타나지 않고 AI 클라이언트가 호출할 수 없습니다.

<a name="tool-responses"></a>
### 툴 응답

툴은 반드시 `Laravel\Mcp\Response` 인스턴스를 반환해야 합니다. Response 클래스는 다양한 응답 타입을 쉽게 생성할 수 있는 여러 메서드를 제공합니다:

간단한 텍스트 응답은 `text` 메서드를 사용하세요:

```php
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;

/**
 * 툴 요청 처리
 */
public function handle(Request $request): Response
{
    // ...

    return Response::text('Weather Summary: Sunny, 72°F');
}
```

툴 실행 중 오류를 알리고 싶다면 `error` 메서드를 사용하세요:

```php
return Response::error('Unable to fetch weather data. Please try again.');
```

<a name="multiple-content-responses"></a>
#### 다중 콘텐츠 응답

여러 개의 콘텐츠를 반환하려면 `Response` 인스턴스의 배열을 반환할 수 있습니다:

```php
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;

/**
 * 툴 요청 처리
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

<a name="streaming-responses"></a>
#### 스트리밍 응답

시간이 오래 걸리는 작업이나 실시간 데이터 스트리밍이 필요하다면 `handle` 메서드에서 [제너레이터(Generator)](https://www.php.net/manual/en/language.generators.overview.php)를 반환할 수 있습니다. 각 응답은 클라이언트로 순차적으로 전송됩니다:

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
     * 툴 요청 처리
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

웹 서버 사용 시, 스트리밍 응답은 SSE(Server-Sent Events) 스트림을 자동으로 열어, 각 메시지를 이벤트로 전송합니다.

<a name="prompts"></a>
## 프롬프트 (Prompts)

[프롬프트](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts)는 서버가 재사용 가능한 프롬프트 템플릿을 AI 클라이언트에 제공할 수 있게 하며, 언어 모델과의 상호작용을 표준화된 방식으로 구조화할 수 있습니다.

<a name="creating-prompts"></a>
### 프롬프트 생성

프롬프트를 생성하려면 `make:mcp-prompt` 아티즌 명령어를 실행하세요:

```shell
php artisan make:mcp-prompt DescribeWeatherPrompt
```

프롬프트를 생성한 후에는 서버의 `$prompts` 속성에 등록해야 합니다:

```php
<?php

namespace App\Mcp\Servers;

use App\Mcp\Prompts\DescribeWeatherPrompt;
use Laravel\Mcp\Server;

class WeatherServer extends Server
{
    /**
     * 이 MCP 서버에 등록된 프롬프트 목록.
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Prompt>>
     */
    protected array $prompts = [
        DescribeWeatherPrompt::class,
    ];
}
```

<a name="prompt-name-title-and-description"></a>
#### 프롬프트 이름, 타이틀, 설명

기본적으로 프롬프트 이름(name)과 타이틀(title)은 클래스 이름에서 자동으로 파생됩니다. 예를 들어 `DescribeWeatherPrompt`는 이름이 `describe-weather`, 타이틀이 `Describe Weather Prompt`가 됩니다. `$name`, `$title` 속성으로 커스텀할 수 있습니다:

```php
class DescribeWeatherPrompt extends Prompt
{
    /**
     * 프롬프트 이름
     */
    protected string $name = 'weather-assistant';

    /**
     * 프롬프트 타이틀
     */
    protected string $title = 'Weather Assistant Prompt';

    // ...
}
```

프롬프트 설명은 자동 생성되지 않으므로, 의미 있는 설명을 `$description` 속성에 정의해야 합니다:

```php
class DescribeWeatherPrompt extends Prompt
{
    /**
     * 프롬프트 설명
     */
    protected string $description = 'Generates a natural-language explanation of the weather for a given location.';

    //
}
```

> [!NOTE]
> 설명은 프롬프트 메타데이터의 핵심 요소로, AI 모델이 해당 프롬프트를 효과적으로 사용할 수 있는 방법과 상황을 이해하는 데 도움을 줍니다.

<a name="prompt-arguments"></a>
### 프롬프트 인수

프롬프트는 인수(argument)를 정의해 AI 클라이언트가 프롬프트 템플릿에 특정 값을 전달할 수 있습니다. `arguments` 메서드를 사용해 인수 정의가 가능합니다:

```php
<?php

namespace App\Mcp\Prompts;

use Laravel\Mcp\Server\Prompt;
use Laravel\Mcp\Server\Prompts\Argument;

class DescribeWeatherPrompt extends Prompt
{
    /**
     * 프롬프트 인수 반환
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

프롬프트 인수는 정의에 따라 자동으로 기본 유효성 검증이 적용됩니다. 더 복잡한 유효성 검증이 필요한 경우, Laravel MCP의 [유효성 검증 기능](/docs/12.x/validation)과 연동해 `handle` 메서드 내에서 직접 검증할 수 있습니다:

```php
<?php

namespace App\Mcp\Prompts;

use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Prompt;

class DescribeWeatherPrompt extends Prompt
{
    /**
     * 프롬프트 요청 처리
     */
    public function handle(Request $request): Response
    {
        $validated = $request->validate([
            'tone' => 'required|string|max:50',
        ]);

        $tone = $validated['tone'];

        // 인수로 받은 tone을 이용해 프롬프트 응답 생성...
    }
}
```

검증 실패 시 AI 클라이언트는 반환 메시지로 동작하므로, 반드시 명확하고 구체적인 에러 메시지를 제공해야 합니다:

```php
$validated = $request->validate([
    'tone' => ['required','string','max:50'],
],[
    'tone.*' => 'You must specify a tone for the weather description. Examples include "formal", "casual", or "humorous".',
]);
```

<a name="prompt-dependency-injection"></a>
### 프롬프트 의존성 주입

프롬프트도 Laravel [서비스 컨테이너](/docs/12.x/container)에 의해 해석되며, 생성자나 `handle` 메서드를 통해 타입힌트로 의존성을 선언할 수 있습니다:

```php
<?php

namespace App\Mcp\Prompts;

use App\Repositories\WeatherRepository;
use Laravel\Mcp\Server\Prompt;

class DescribeWeatherPrompt extends Prompt
{
    /**
     * 새로운 프롬프트 인스턴스 생성자
     */
    public function __construct(
        protected WeatherRepository $weather,
    ) {}

    //
}
```

생성자 외에도, `handle` 메서드에서 타입힌트로 직접 의존성을 주입받아 사용할 수도 있습니다:

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
     * 프롬프트 요청 처리
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

`shouldRegister` 메서드를 구현해 런타임 시 프롬프트가 등록될지 여부를 제어할 수 있습니다. 이는 애플리케이션 상태, 설정값, 요청 파라미터 등에 따른 동적 제어에 유용합니다:

```php
<?php

namespace App\Mcp\Prompts;

use Laravel\Mcp\Request;
use Laravel\Mcp\Server\Prompt;

class CurrentWeatherPrompt extends Prompt
{
    /**
     * 프롬프트 등록 조건
     */
    public function shouldRegister(Request $request): bool
    {
        return $request?->user()?->subscribed() ?? false;
    }
}
```

`shouldRegister`가 `false`를 반환하면 해당 프롬프트는 목록에 보이지 않으며 AI 클라이언트가 사용할 수 없습니다.

<a name="prompt-responses"></a>
### 프롬프트 응답

프롬프트는 단일 `Laravel\Mcp\Response` 또는 반복 가능한 `Laravel\Mcp\Response` 인스턴스 배열을 반환할 수 있습니다. 이 응답들은 AI 클라이언트로 전달되는 실제 컨텐츠를 포함합니다:

```php
<?php

namespace App\Mcp\Prompts;

use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Prompt;

class DescribeWeatherPrompt extends Prompt
{
    /**
     * 프롬프트 요청 처리
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

`asAssistant()` 메서드를 사용하면 해당 응답 메시지가 AI 어시스턴트가 보낸 것으로 처리되며, 일반 메시지는 사용자 입력으로 간주됩니다.

<a name="resources"></a>
## 리소스 (Resources)

[리소스](https://modelcontextprotocol.io/specification/2025-06-18/server/resources)는 서버가 데이터나 컨텐츠를 AI 클라이언트에 읽기 전용 형태로 제공할 수 있도록 해줍니다. 이를 통해 설명서, 설정, 또는 AI 응답을 구성하는 데 도움이 될 수 있는 다양한 정적 또는 동적 정보를 공유할 수 있습니다.

<a name="creating-resources"></a>
## 리소스 생성

리소스를 생성하려면 `make:mcp-resource` 아티즌 명령어를 실행하세요:

```shell
php artisan make:mcp-resource WeatherGuidelinesResource
```

생성 후에는 서버의 `$resources` 속성에 등록해야 합니다:

```php
<?php

namespace App\Mcp\Servers;

use App\Mcp\Resources\WeatherGuidelinesResource;
use Laravel\Mcp\Server;

class WeatherServer extends Server
{
    /**
     * 이 MCP 서버에 등록된 리소스 목록.
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Resource>>
     */
    protected array $resources = [
        WeatherGuidelinesResource::class,
    ];
}
```

<a name="resource-name-title-and-description"></a>
#### 리소스 이름, 타이틀, 설명

기본적으로 리소스의 이름(name)과 타이틀(title)은 클래스명에서 자동 추출됩니다. 예를 들어 `WeatherGuidelinesResource`의 경우 이름은 `weather-guidelines`, 타이틀은 `Weather Guidelines Resource`가 됩니다. `$name`, `$title` 속성으로 원하는 값으로 커스텀할 수 있습니다:

```php
class WeatherGuidelinesResource extends Resource
{
    /**
     * 리소스 이름
     */
    protected string $name = 'weather-api-docs';

    /**
     * 리소스 타이틀
     */
    protected string $title = 'Weather API Documentation';

    // ...
}
```

리소스 설명도 자동 생성되지 않으므로, `$description` 속성에 명확한 설명을 반드시 작성해야 합니다:

```php
class WeatherGuidelinesResource extends Resource
{
    /**
     * 리소스 설명
     */
    protected string $description = 'Comprehensive guidelines for using the Weather API.';

    //
}
```

> [!NOTE]
> 설명은 리소스 메타데이터의 핵심 부분으로, AI 모델이 해당 리소스의 효과적인 활용 시점을 파악하도록 돕습니다.

<a name="resource-uri-and-mime-type"></a>
### 리소스 URI 및 MIME 타입

각 리소스는 고유한 URI와 MIME 타입을 갖습니다. 이를 통해 AI 클라이언트가 리소스의 형식과 정보를 적절히 파악할 수 있습니다.

기본적으로 리소스 URI는 이름을 기반으로 생성되며, 예를 들어 `WeatherGuidelinesResource`는 URI `weather://resources/weather-guidelines`를 갖고, MIME 타입은 `text/plain`입니다.

원하는 경우 `$uri`, `$mimeType` 속성을 오버라이드해 값 변경이 가능합니다:

```php
<?php

namespace App\Mcp\Resources;

use Laravel\Mcp\Server\Resource;

class WeatherGuidelinesResource extends Resource
{
    /**
     * 리소스 URI
     */
    protected string $uri = 'weather://resources/guidelines';

    /**
     * 리소스 MIME 타입
     */
    protected string $mimeType = 'application/pdf';
}
```

URI와 MIME 타입을 통해 AI 클라이언트가 리소스 내용을 적절히 처리할 수 있게 됩니다.

<a name="resource-request"></a>
### 리소스 요청

툴이나 프롬프트와 달리, 리소스는 입력 스키마나 인수를 정의하지 않습니다. 그러나 `handle` 메서드에서 요청 객체를 이용해 요청 정보를 활용할 수 있습니다:

```php
<?php

namespace App\Mcp\Resources;

use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Resource;

class WeatherGuidelinesResource extends Resource
{
    /**
     * 리소스 요청 처리
     */
    public function handle(Request $request): Response
    {
        // ...
    }
}
```

<a name="resource-dependency-injection"></a>
### 리소스 의존성 주입

Laravel [서비스 컨테이너](/docs/12.x/container)는 모든 리소스도 해석하므로, 생성자나 `handle` 메서드에서 타입힌트로 의존성을 주입받을 수 있습니다:

```php
<?php

namespace App\Mcp\Resources;

use App\Repositories\WeatherRepository;
use Laravel\Mcp\Server\Resource;

class WeatherGuidelinesResource extends Resource
{
    /**
     * 새로운 리소스 인스턴스 생성자
     */
    public function __construct(
        protected WeatherRepository $weather,
    ) {}

    // ...
}
```

메서드 인자에도 의존성을 선언하면 자동 주입이 지원됩니다:

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
     * 리소스 요청 처리
     */
    public function handle(WeatherRepository $weather): Response
    {
        $guidelines = $weather->guidelines();

        return Response::text($guidelines);
    }
}
```

<a name="conditional-resource-registration"></a>
### 조건부 리소스 등록

런타임 시 애플리케이션 상태나 요청값 등에 따라 `shouldRegister` 메서드를 구현해 리소스의 등록 여부를 동적으로 결정할 수 있습니다:

```php
<?php

namespace App\Mcp\Resources;

use Laravel\Mcp\Request;
use Laravel\Mcp\Server\Resource;

class WeatherGuidelinesResource extends Resource
{
    /**
     * 리소스 등록 조건
     */
    public function shouldRegister(Request $request): bool
    {
        return $request?->user()?->subscribed() ?? false;
    }
}
```

`shouldRegister`가 `false`이면 해당 리소스는 등록 목록에 나타나지 않고, AI 클라이언트가 접근할 수 없습니다.

<a name="resource-responses"></a>
### 리소스 응답

모든 리소스는 반드시 `Laravel\Mcp\Response` 인스턴스를 반환해야 하며, Response 클래스는 다양한 응답 타입 생성을 지원합니다:

텍스트 콘텐츠를 반환하려면 `text` 메서드를 사용하세요:

```php
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;

/**
 * 리소스 요청 처리
 */
public function handle(Request $request): Response
{
    // ...

    return Response::text($weatherData);
}
```

<a name="resource-blob-responses"></a>
#### Blob 응답

바이너리(Blob) 콘텐츠의 경우 `blob` 메서드를 사용해 반환하세요:

```php
return Response::blob(file_get_contents(storage_path('weather/radar.png')));
```

이 경우 MIME 타입은 리소스 클래스의 `$mimeType` 속성값에 지정합니다:

```php
<?php

namespace App\Mcp\Resources;

use Laravel\Mcp\Server\Resource;

class WeatherGuidelinesResource extends Resource
{
    /**
     * 리소스 MIME 타입
     */
    protected string $mimeType = 'image/png';

    //
}
```

<a name="resource-error-responses"></a>
#### 에러 응답

리소스 조회 중 오류가 발생했다면 `error()` 메서드로 응답할 수 있습니다:

```php
return Response::error('Unable to fetch weather data for the specified location.');
```

<a name="authentication"></a>
## 인증

웹 MCP 서버에 일반적인 라우트처럼 미들웨어를 적용해 인증을 처리할 수 있습니다. MCP 서버 접근을 인증하려면, [Laravel Sanctum](/docs/12.x/sanctum)을 통한 토큰 인증, `Authorization` HTTP 헤더로 임의 API 토큰 전달, 혹은 [Laravel Passport](/docs/12.x/passport)를 통한 OAuth 방식을 사용할 수 있습니다.

<a name="oauth"></a>
### OAuth 2.1

웹 기반 MCP 서버를 보호하는 가장 강력한 방법은 [Laravel Passport](/docs/12.x/passport)를 사용한 OAuth입니다.

OAuth 인증을 적용하려면, `routes/ai.php` 파일에 `Mcp::oauthRoutes` 메서드로 필요한 OAuth2 디스커버리 및 클라이언트 등록 라우트를 추가합니다. 그리고 서버 라우트에 Passport의 `auth:api` 미들웨어를 지정하세요:

```php
use App\Mcp\Servers\WeatherExample;
use Laravel\Mcp\Facades\Mcp;

Mcp::oauthRoutes();

Mcp::web('/mcp/weather', WeatherExample::class)
    ->middleware('auth:api');
```

#### Passport 신규 설치

Laravel Passport를 아직 사용하지 않는다면, [Passport 설치/배포 가이드](/docs/12.x/passport#installation)를 먼저 참고해 설치하세요. 설치 후 `OAuthenticatable` 모델, 인증 가드, 키 설정이 필요합니다.

다음으로, MCP에서 제공하는 Passport 인가 뷰를 퍼블리시합니다:

```shell
php artisan vendor:publish --tag=mcp-views
```

그리고, `AppServiceProvider`의 `boot` 메서드에서 `Passport::authorizationView` 메서드로 이 뷰를 사용하도록 지시합니다:

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

이 뷰는 최종 사용자가 AI 에이전트의 인증 시도에 대해 승인 또는 거부할 때 표시됩니다.

![Authorization screen example](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...)

> [!NOTE]
> 이 경우 OAuth를 단순히 인증 가능 모델로의 변환 계층으로 사용합니다. OAuth의 scope 등 다양한 측면은 생략합니다.

#### 기존 Passport 설치 환경

이미 Laravel Passport를 사용 중이라면 MCP도 별다른 추가 설정 없이 연동됩니다. 단, OAuth의 목적은 인증 가능 모델로의 변환이므로 커스텀 스코프는 현재 지원되지 않습니다.

`Mcp::oauthRoutes()`를 통해 `mcp:use`라는 단일 스코프만 추가, 광고, 사용됩니다.

#### Passport와 Sanctum의 차이

Model Context Protocol 명세의 공식 인증 메커니즘이 OAuth2.1이고, MCP 클라이언트에게 가장 널리 지원되는 방식이므로 Passport 사용을 권장합니다.

이미 [Sanctum](/docs/12.x/sanctum)을 사용하는 경우 Passport 도입이 부담스러울 수 있으므로, 필요 시까지는 Passport 없이 Sanctum만 사용하는 것이 좋습니다.

<a name="sanctum"></a>
### Sanctum

[Sanctum](/docs/12.x/sanctum)으로 MCP 서버를 보호하려면, `routes/ai.php` 파일의 서버에 Sanctum 인증 미들웨어를 적용하세요. 이후 MCP 클라이언트가 `Authorization: Bearer <token>` 헤더를 전달해야 인증에 성공할 수 있습니다:

```php
use App\Mcp\Servers\WeatherExample;
use Laravel\Mcp\Facades\Mcp;

Mcp::web('/mcp/demo', WeatherExample::class)
    ->middleware('auth:sanctum');
```

<a name="custom-mcp-authentication"></a>
#### 커스텀 MCP 인증

애플리케이션에서 자체 API 토큰을 발급한다면 `Mcp::web` 라우트에 원하는 모든 미들웨어를 적용해 MCP 요청의 `Authorization` 헤더를 직접 검사할 수 있습니다.

<a name="authorization"></a>
## 인가

현재 인증된 사용자는 `$request->user()` 메서드로 접근할 수 있습니다. 이를 활용해 MCP 툴이나 리소스 내에서 [인가 체크](/docs/12.x/authorization)가 가능합니다:

```php
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;

/**
 * 툴 요청 처리
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

내장 MCP 인스펙터나 유닛 테스트를 통해 MCP 서버를 검증할 수 있습니다.

<a name="mcp-inspector"></a>
### MCP 인스펙터

[MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector)는 MCP 서버를 테스트/디버깅할 수 있는 대화형 툴입니다. 이 툴을 사용해 서버에 접속하고 인증 검증, 각종 툴, 리소스, 프롬프트 테스트가 가능합니다.

등록된 서버마다 다음 명령어로 인스펙터를 실행할 수 있습니다:

```shell
# 웹 서버의 경우...
php artisan mcp:inspector /mcp/weather

# "weather"라는 로컬 서버의 경우...
php artisan mcp:inspector weather
```

이 명령어는 MCP 인스펙터를 실행하고, 클라이언트에 적용할 수 있는 연결 설정 정보를 출력해줍니다. 웹 서버가 인증 미들웨어로 보호되고 있다면, MCP 인스펙터 연결 시 `Authorization` Bearer 토큰 등 필요한 헤더를 꼭 포함해야 합니다.

<a name="unit-tests"></a>
### 유닛 테스트

MCP 서버와 툴, 리소스, 프롬프트에 대한 유닛 테스트도 작성할 수 있습니다.

테스트를 작성하려면 새 테스트 케이스에서 해당 서버의 원하는 기능을 호출하면 됩니다. 예를 들어 `WeatherServer`의 툴 테스트:

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
 * 툴 테스트
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

이와 비슷하게, 프롬프트와 리소스도 테스트할 수 있습니다:

```php
$response = WeatherServer::prompt(...);
$response = WeatherServer::resource(...);
```

테스트 중 인증된 사용자로 동작하려면 `actingAs` 메서드를 체이닝하세요:

```php
$response = WeatherServer::actingAs($user)->tool(...);
```

응답 객체가 생성된 후에는 다양한 assertion 메서드로 결과를 검증할 수 있습니다.

응답이 성공적인지 검증하려면 `assertOk` 메서드를 사용합니다. 이는 응답에 오류가 없는지 확인합니다:

```php
$response->assertOk();
```

특정 텍스트가 포함되었는지 확인하려면 `assertSee`를 활용하세요:

```php
$response->assertSee('The current weather in New York City is 72°F and sunny.');
```

응답에 에러가 포함되어 있는지 확인하려면 `assertHasErrors`를 사용합니다:

```php
$response->assertHasErrors();

$response->assertHasErrors([
    'Something went wrong.',
]);
```

응답에 에러가 없어야 함을 검증하려면 `assertHasNoErrors`로 검증할 수 있습니다:

```php
$response->assertHasNoErrors();
```

응답의 메타데이터가 정확한지 검증하려면 `assertName()`, `assertTitle()`, `assertDescription()` 메서드를 사용할 수 있습니다:

```php
$response->assertName('current-weather');
$response->assertTitle('Current Weather Tool');
$response->assertDescription('Fetches the current weather forecast for a specified location.');
```

알림(Notification) 이벤트 전송을 검증하려면 `assertSentNotification`, `assertNotificationCount` 등의 메서드를 활용할 수 있습니다:

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

마지막으로, 응답 객체의 원본 내용을 직접 출력하고 싶다면 `dd` 또는 `dump` 메서드를 사용할 수 있습니다:

```php
$response->dd();
$response->dump();
```
