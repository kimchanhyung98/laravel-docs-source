# Laravel MCP (Laravel MCP)

- [소개](#introduction)
- [설치](#installation)
    - [라우트 출판하기](#publishing-routes)
- [서버 생성하기](#creating-servers)
    - [서버 등록](#server-registration)
    - [웹 서버](#web-servers)
    - [로컬 서버](#local-servers)
- [툴](#tools)
    - [툴 생성하기](#creating-tools)
    - [툴 입력 스키마](#tool-input-schemas)
    - [툴 인수 유효성 검증](#validating-tool-arguments)
    - [툴 의존성 주입](#tool-dependency-injection)
    - [툴 애노테이션](#tool-annotations)
    - [툴 조건부 등록](#conditional-tool-registration)
    - [툴 응답](#tool-responses)
- [프롬프트](#prompts)
    - [프롬프트 생성하기](#creating-prompts)
    - [프롬프트 인수](#prompt-arguments)
    - [프롬프트 인수 유효성 검증](#validating-prompt-arguments)
    - [프롬프트 의존성 주입](#prompt-dependency-injection)
    - [프롬프트 조건부 등록](#conditional-prompt-registration)
    - [프롬프트 응답](#prompt-responses)
- [리소스](#creating-resources)
    - [리소스 생성하기](#creating-resources)
    - [리소스 URI 및 MIME 타입](#resource-uri-and-mime-type)
    - [리소스 요청](#resource-request)
    - [리소스 의존성 주입](#resource-dependency-injection)
    - [리소스 조건부 등록](#conditional-resource-registration)
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

[Laravel MCP](https://github.com/laravel/mcp)는 AI 클라이언트가 [Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro)을 통해 Laravel 애플리케이션과 상호작용할 수 있게 해주는 간단하고 우아한 솔루션입니다. MCP는 서버, 툴, 리소스, 프롬프트를 정의할 때 표현력 있고 유연한 인터페이스를 제공하여, AI 기반의 다양한 상호작용을 애플리케이션에 쉽게 추가할 수 있습니다.

<a name="installation"></a>
## 설치

시작하려면 Composer 패키지 관리자를 사용해 Laravel MCP를 프로젝트에 설치합니다:

```shell
composer require laravel/mcp
```

<a name="publishing-routes"></a>
### 라우트 출판하기

Laravel MCP 설치 후, `vendor:publish` Artisan 명령어를 실행하여 MCP 서버를 정의하는 데 사용할 `routes/ai.php` 파일을 출판합니다:

```shell
php artisan vendor:publish --tag=ai-routes
```

이 명령어는 애플리케이션의 `routes` 디렉터리에 `routes/ai.php` 파일을 생성합니다. 이 파일에서 MCP 서버를 등록하게 됩니다.

<a name="creating-servers"></a>
## 서버 생성하기

`make:mcp-server` Artisan 명령어를 사용해 MCP 서버를 생성할 수 있습니다. MCP 서버는 AI 클라이언트에 툴, 리소스, 프롬프트 등 MCP의 다양한 기능을 제공하는 중심 역할을 합니다.

```shell
php artisan make:mcp-server WeatherServer
```

위 명령어는 `app/Mcp/Servers` 디렉터리에 새로운 서버 클래스를 생성합니다. 이 클래스는 Laravel MCP의 기본 `Laravel\Mcp\Server`를 확장하며, 툴, 리소스, 프롬프트를 등록할 수 있는 속성을 제공합니다.

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
     * LLM을 위한 MCP 서버의 안내문.
     */
    protected string $instructions = 'This server provides weather information and forecasts.';

    /**
     * 이 MCP 서버에 등록된 툴.
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Tool>>
     */
    protected array $tools = [
        // GetCurrentWeatherTool::class,
    ];

    /**
     * 이 MCP 서버에 등록된 리소스.
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Resource>>
     */
    protected array $resources = [
        // WeatherGuidelinesResource::class,
    ];

    /**
     * 이 MCP 서버에 등록된 프롬프트.
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

서버를 생성한 후에는, AI 클라이언트에서 접근할 수 있도록 `routes/ai.php` 파일에 서버를 등록해야 합니다. Laravel MCP는 서버 등록을 위해 `web`(HTTP 접근용)과 `local`(명령줄 접근용) 두 가지 방법을 제공합니다.

<a name="web-servers"></a>
### 웹 서버

웹 서버는 가장 일반적인 형태로, HTTP POST 요청을 통해 접근할 수 있습니다. 이는 원격 AI 클라이언트나 웹 통합에 적합합니다. `web` 메서드를 사용해 웹 서버를 등록할 수 있습니다:

```php
use App\Mcp\Servers\WeatherServer;
use Laravel\Mcp\Facades\Mcp;

Mcp::web('/mcp/weather', WeatherServer::class);
```

일반적인 라우트와 마찬가지로, 미들웨어를 적용하여 웹 서버의 접근을 보호할 수 있습니다:

```php
Mcp::web('/mcp/weather', WeatherServer::class)
    ->middleware(['throttle:mcp']);
```

<a name="local-servers"></a>
### 로컬 서버

로컬 서버는 Artisan 명령어로 실행되며, [Laravel Boost](/docs/12.x/installation#installing-laravel-boost)와 같이 로컬 AI 어시스턴트 통합에 적합합니다. `local` 메서드를 사용해 로컬 서버를 등록하세요:

```php
use App\Mcp\Servers\WeatherServer;
use Laravel\Mcp\Facades\Mcp;

Mcp::local('weather', WeatherServer::class);
```

서버를 등록한 후에는 일반적으로 `mcp:start` Artisan 명령어를 직접 실행할 필요가 없습니다. 대신 MCP 클라이언트(AI 에이전트)에서 서버를 시작하도록 하거나, [MCP Inspector](#mcp-inspector)를 활용할 수 있습니다.

<a name="tools"></a>
## 툴

툴은 AI 클라이언트가 호출할 수 있는 기능을 MCP 서버에서 외부로 노출하는 역할을 합니다. 이를 통해 언어 모델이 특정 작업을 수행하거나, 코드 실행, 외부 시스템과의 연동이 가능합니다.

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
     * 툴 설명.
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
     * 툴의 입력 스키마 반환.
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
### 툴 생성하기

툴을 생성하려면, 다음과 같이 `make:mcp-tool` Artisan 명령어를 실행합니다:

```shell
php artisan make:mcp-tool CurrentWeatherTool
```

툴 생성 후, 해당 툴을 서버의 `$tools` 속성에 등록하세요:

```php
<?php

namespace App\Mcp\Servers;

use App\Mcp\Tools\CurrentWeatherTool;
use Laravel\Mcp\Server;

class WeatherServer extends Server
{
    /**
     * 이 MCP 서버에 등록된 툴.
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Tool>>
     */
    protected array $tools = [
        CurrentWeatherTool::class,
    ];
}
```

<a name="tool-name-title-description"></a>
#### 툴 이름, 제목, 설명

기본적으로 툴의 이름(name)과 제목(title)은 클래스명에서 자동 유추됩니다. 예를 들어, `CurrentWeatherTool`은 이름이 `current-weather`, 제목이 `Current Weather Tool`이 됩니다. `$name`과 `$title` 속성을 직접 지정하여 원하는 대로 변경할 수 있습니다.

```php
class CurrentWeatherTool extends Tool
{
    /**
     * 툴의 이름.
     */
    protected string $name = 'get-optimistic-weather';

    /**
     * 툴의 제목.
     */
    protected string $title = 'Get Optimistic Weather Forecast';

    // ...
}
```

툴의 설명(description)은 자동 생성되지 않으므로, 항상 의미 있는 설명을 `$description` 속성으로 명시해주어야 합니다.

```php
class CurrentWeatherTool extends Tool
{
    /**
     * 툴 설명.
     */
    protected string $description = 'Fetches the current weather forecast for a specified location.';

    //
}
```

> [!NOTE]
> 설명(description)은 툴 메타데이터에서 매우 중요합니다. 이는 AI 모델이 언제, 어떻게 툴을 적절히 사용할지 이해하는 데 큰 도움을 줍니다.

<a name="tool-input-schemas"></a>
### 툴 입력 스키마

툴은 입력 스키마를 정의하여 AI 클라이언트에게 받을 인수를 명확하게 지정할 수 있습니다. Laravel의 `Illuminate\JsonSchema\JsonSchema` 빌더를 사용해 요구되는 입력값을 쉽게 정의할 수 있습니다.

```php
<?php

namespace App\Mcp\Tools;

use Illuminate\JsonSchema\JsonSchema;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * 툴 입력 스키마 반환.
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

JSON Schema는 툴 인수의 기본 구조를 정의하지만, 더 복잡한 유효성 검증이 필요한 경우도 있습니다.

Laravel MCP는 Laravel의 [유효성 검증 기능](/docs/12.x/validation)과 자연스럽게 연동됩니다. 툴의 `handle` 메서드 안에서 `$request->validate([])`를 활용하여 인수의 유효성을 검증할 수 있습니다.

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

        // 검증된 인수를 사용해 날씨 데이터 조회...
    }
}
```

만약 유효성 검증에 실패하면, AI 클라이언트는 제공한 에러 메시지에 따라 행동합니다. 그러므로 명확하고 실행 가능한 에러 메시지를 제공하는 것이 매우 중요합니다.

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
#### 툴 의존성 주입

모든 MCP 툴은 Laravel의 [서비스 컨테이너](/docs/12.x/container)를 통해 해석됩니다. 따라서 생성자에서 필요한 의존성을 타입힌트로 선언만 하면, 인스턴스에 자동으로 주입받을 수 있습니다.

```php
<?php

namespace App\Mcp\Tools;

use App\Repositories\WeatherRepository;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * 새로운 툴 인스턴스 생성.
     */
    public function __construct(
        protected WeatherRepository $weather,
    ) {}

    // ...
}
```

생성자 뿐 아니라, `handle()` 메서드에서도 의존성을 타입힌트로 지정하면 서비스 컨테이너가 자동으로 주입해줍니다.

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
### 툴 애노테이션

툴에 추가적인 메타데이터를 AI 클라이언트에 전달하고 싶을 때, [애노테이션](https://modelcontextprotocol.io/specification/2025-06-18/schema#toolannotations)을 사용할 수 있습니다. 이러한 애노테이션은 툴의 동작이나 특성을 모델에게 명확히 전달합니다. 툴 클래스 상단에 어트리뷰트 형태로 사용할 수 있습니다.

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

사용 가능한 애노테이션 종류는 다음과 같습니다:

| 애노테이션           | 타입    | 설명                                                                         |
| ------------------- | ------- | ---------------------------------------------------------------------------- |
| `#[IsReadOnly]`     | boolean | 툴이 환경을 변경하지 않음을 나타냅니다.                                      |
| `#[IsDestructive]`  | boolean | 툴이 파괴적인 변경을 할 수도 있음을 표시합니다. (읽기 전용이 아닐 때만 의미 있음)   |
| `#[IsIdempotent]`   | boolean | 동일 인수로 반복 호출해도 추가 효과가 없음을 나타냅니다. (읽기 전용이 아닐 때만)   |
| `#[IsOpenWorld]`    | boolean | 툴이 외부 엔티티와 상호작용할 수도 있음을 표시합니다.                           |

<a name="conditional-tool-registration"></a>
### 툴 조건부 등록

특정 상황에서만 툴을 노출하고 싶을 때, 툴 클래스에 `shouldRegister` 메서드를 구현하세요. 이 메서드는 애플리케이션의 상태, 설정, 요청 파라미터 등 다양한 조건에 따라 툴 등록 여부를 결정합니다.

```php
<?php

namespace App\Mcp\Tools;

use Laravel\Mcp\Request;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * 이 툴의 등록 여부 결정.
     */
    public function shouldRegister(Request $request): bool
    {
        return $request?->user()?->subscribed() ?? false;
    }
}
```

`shouldRegister`가 false를 반환하면, 이 툴은 MCP 서버의 기능 목록에 나타나지 않고 AI 클라이언트가 호출할 수 없습니다.

<a name="tool-responses"></a>
### 툴 응답

툴은 반드시 `Laravel\Mcp\Response` 인스턴스를 반환해야 합니다. 이 Response 클래스는 여러 타입의 응답을 간단히 생성할 수 있도록 다양한 메서드를 제공합니다.

간단한 텍스트 응답은 `text` 메서드를 사용하세요:

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

툴 실행 중 오류가 났을 경우, `error` 메서드를 사용해 에러 메시지를 전달할 수 있습니다:

```php
return Response::error('Unable to fetch weather data. Please try again.');
```

<a name="multiple-content-responses"></a>
#### 다중 콘텐츠 응답

여러 개의 응답을 한 번에 반환하려면, `Response` 인스턴스의 배열을 반환할 수 있습니다:

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

<a name="streaming-responses"></a>
#### 스트리밍 응답

실시간 데이터나 작업 진행 상황 등 장시간 소요되는 작업의 중간 상태를 전달하려면, `handle` 메서드에서 [제너레이터](https://www.php.net/manual/en/language.generators.overview.php)를 반환할 수 있습니다. 사용자는 각 단계별로 메시지를 받을 수 있습니다.

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

웹 서버에서는 스트리밍 응답이 자동으로 SSE(Server-Sent Events) 스트림을 열어, 각 메시지를 실시간으로 클라이언트에 전송합니다.

<a name="prompts"></a>
## 프롬프트

[프롬프트](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts)는 서버가 AI 클라이언트와의 상호작용에 활용할 수 있는, 재사용 가능한 프롬프트 템플릿을 제공합니다. 주로 공통적인 질의 구조나 상호작용 패턴을 표준화하는 용도로 사용됩니다.

<a name="creating-prompts"></a>
### 프롬프트 생성하기

프롬프트를 생성하려면 아래와 같이 `make:mcp-prompt` Artisan 명령어를 사용하세요:

```shell
php artisan make:mcp-prompt DescribeWeatherPrompt
```

프롬프트 생성 이후, 서버의 `$prompts` 속성에 등록해야 합니다:

```php
<?php

namespace App\Mcp\Servers;

use App\Mcp\Prompts\DescribeWeatherPrompt;
use Laravel\Mcp\Server;

class WeatherServer extends Server
{
    /**
     * 이 MCP 서버에 등록된 프롬프트.
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Prompt>>
     */
    protected array $prompts = [
        DescribeWeatherPrompt::class,
    ];
}
```

<a name="prompt-name-title-and-description"></a>
#### 프롬프트 이름, 제목, 설명

프롬프트의 이름과 제목도 기본적으로 클래스명에서 유추됩니다. 예를 들어, `DescribeWeatherPrompt`라면 이름은 `describe-weather`, 제목은 `Describe Weather Prompt`가 자동 설정됩니다. 필요에 따라 `$name`, `$title` 속성을 직접 지정할 수 있습니다:

```php
class DescribeWeatherPrompt extends Prompt
{
    /**
     * 프롬프트의 이름.
     */
    protected string $name = 'weather-assistant';

    /**
     * 프롬프트의 제목.
     */
    protected string $title = 'Weather Assistant Prompt';

    // ...
}
```

프롬프트 설명 역시 자동 생성되지 않으므로, 의미 있는 `$description`을 반드시 작성해야 합니다:

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
> 설명(description)은 프롬프트의 메타데이터에서 매우 중요합니다. AI 모델이 언제, 어떻게 프롬프트를 최적으로 사용할지 판단하는 데 도움이 됩니다.

<a name="prompt-arguments"></a>
### 프롬프트 인수

프롬프트는 AI 클라이언트가 특정 값을 전달하여 템플릿을 커스터마이즈할 수 있도록 인수를 정의할 수 있습니다. `arguments` 메서드로 어떤 인수를 받을지 지정하세요.

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

프롬프트 인수는 정의에 따라 자동 검증되지만, 더 상세한 규칙이 필요하면 Laravel의 [유효성 검증 기능](/docs/12.x/validation)을 활용하세요.

프롬프트의 `handle` 메서드에서 검증할 수 있습니다:

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

        // 전달받은 tone을 활용하여 프롬프트 응답 생성...
    }
}
```

에러 발생 시, AI 클라이언트가 활용할 수 있도록 명확한 에러 메시지를 작성하는 것이 중요합니다:

```php
$validated = $request->validate([
    'tone' => ['required','string','max:50'],
],[
    'tone.*' => 'You must specify a tone for the weather description. Examples include "formal", "casual", or "humorous".',
]);
```

<a name="prompt-dependency-injection"></a>
### 프롬프트 의존성 주입

프롬프트 역시 Laravel [서비스 컨테이너](/docs/12.x/container)를 통해 자동으로 의존성 주입이 이뤄집니다. 생성자 또는 `handle` 메서드에서 타입힌트로 지정하세요.

```php
<?php

namespace App\Mcp\Prompts;

use App\Repositories\WeatherRepository;
use Laravel\Mcp\Server\Prompt;

class DescribeWeatherPrompt extends Prompt
{
    /**
     * 새로운 프롬프트 인스턴스 생성.
     */
    public function __construct(
        protected WeatherRepository $weather,
    ) {}

    //
}
```

또는 메서드에서 타입힌트로 의존성을 받을 수 있습니다:

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
### 프롬프트 조건부 등록

프롬프트를 조건에 따라 노출하거나 숨기려면, `shouldRegister` 메서드를 구현하세요.

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

이 메서드가 false를 반환하면 해당 프롬프트는 외부에 노출되지 않습니다.

<a name="prompt-responses"></a>
### 프롬프트 응답

프롬프트는 `Laravel\Mcp\Response` 한 개 또는 여러 개(배열, 이터러블)를 반환할 수 있습니다. 각 응답은 AI 클라이언트로 전송됩니다.

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

`asAssistant()` 메서드를 사용하면 해당 메시지가 AI 어시스턴트의 답변임을 표시할 수 있습니다.

<a name="resources"></a>
## 리소스

[리소스](https://modelcontextprotocol.io/specification/2025-06-18/server/resources)는 서버가 AI 클라이언트에 데이터를 제공해, LLM의 응답을 풍부하게 만들고 배경 정보를 전달하는 데 사용됩니다. 문서, 설정 정보 등 다양한 데이터를 동적으로 또는 정적으로 전달할 수 있습니다.

<a name="creating-resources"></a>
## 리소스 생성하기

리소스를 생성하려면, 다음 Artisan 명령어를 실행하세요:

```shell
php artisan make:mcp-resource WeatherGuidelinesResource
```

생성 후, 해당 리소스를 서버의 `$resources` 속성에 등록해야 합니다:

```php
<?php

namespace App\Mcp\Servers;

use App\Mcp\Resources\WeatherGuidelinesResource;
use Laravel\Mcp\Server;

class WeatherServer extends Server
{
    /**
     * 이 MCP 서버에 등록된 리소스.
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Resource>>
     */
    protected array $resources = [
        WeatherGuidelinesResource::class,
    ];
}
```

<a name="resource-name-title-and-description"></a>
#### 리소스 이름, 제목, 설명

리소스 클래스의 이름과 제목은 클래스명에서 자동 생성됩니다. 예를 들어, `WeatherGuidelinesResource`는 이름이 `weather-guidelines`, 제목이 `Weather Guidelines Resource`로 설정됩니다. 필요하다면 `$name`, `$title` 속성으로 직접 지정할 수 있습니다:

```php
class WeatherGuidelinesResource extends Resource
{
    /**
     * 리소스의 이름.
     */
    protected string $name = 'weather-api-docs';

    /**
     * 리소스의 제목.
     */
    protected string $title = 'Weather API Documentation';

    // ...
}
```

리소스 설명 역시 자동 생성되지 않으니, 의미 있는 `$description`을 반드시 작성하세요:

```php
class WeatherGuidelinesResource extends Resource
{
    /**
     * 리소스 설명.
     */
    protected string $description = 'Comprehensive guidelines for using the Weather API.';

    //
}
```

> [!NOTE]
> 설명(description)은 리소스 메타데이터에서 매우 중요한 요소입니다. AI 모델이 언제, 어떻게 리소스를 어떤 목적으로 사용할지 파악하는 데 도움이 됩니다.

<a name="resource-uri-and-mime-type"></a>
### 리소스 URI 및 MIME 타입

각 리소스는 고유한 URI와 MIME 타입을 갖습니다. 기본적으로 URI는 리소스명으로 자동 생성되고, MIME 타입은 `text/plain`입니다.

필요에 따라 `$uri`, `$mimeType` 속성으로 값 변경이 가능합니다:

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

이 정보는 AI 클라이언트가 리소스의 포맷을 올바르게 해석하고 처리하는 데 도움을 줍니다.

<a name="resource-request"></a>
### 리소스 요청

툴 및 프롬프트와 달리, 리소스는 입력 스키마나 인수를 추가적으로 정의할 수 없습니다. 하지만 `handle` 메서드 내에서 요청 객체와 상호작용은 가능합니다.

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

리소스 또한 Laravel [서비스 컨테이너](/docs/12.x/container)를 통해 의존성을 자동으로 주입받을 수 있습니다. 생성자 또는 `handle` 메서드에서 타입힌트로 사용하세요.

```php
<?php

namespace App\Mcp\Resources;

use App\Repositories\WeatherRepository;
use Laravel\Mcp\Server\Resource;

class WeatherGuidelinesResource extends Resource
{
    /**
     * 새 리소스 인스턴스 생성.
     */
    public function __construct(
        protected WeatherRepository $weather,
    ) {}

    // ...
}
```

또는 메서드에 타입힌트로 지정해서 사용할 수도 있습니다:

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

<a name="conditional-resource-registration"></a>
### 리소스 조건부 등록

어떤 경우에만 리소스를 노출하고 싶다면, `shouldRegister` 메서드를 구현하세요.

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

이 메서드가 false를 반환하면, 리소스는 MCP 서버의 기능 목록에 나타나지 않고 AI 클라이언트에서 접근할 수 없습니다.

<a name="resource-responses"></a>
### 리소스 응답

리소스는 반드시 `Laravel\Mcp\Response` 인스턴스를 반환해 응답합니다. 여러 타입의 응답을 손쉽게 생성할 수 있습니다.

간단한 텍스트 응답은 `text` 메서드로 반환합니다:

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

<a name="resource-blob-responses"></a>
#### Blob 응답

Blob(바이너리) 콘텐츠를 반환하려면 `blob` 메서드를 사용해 파일 내용을 전달할 수 있습니다:

```php
return Response::blob(file_get_contents(storage_path('weather/radar.png')));
```

이 때 블롭의 MIME 타입은 리소스 클래스의 `$mimeType` 속성에 따라 결정됩니다:

```php
<?php

namespace App\Mcp\Resources;

use Laravel\Mcp\Server\Resource;

class WeatherGuidelinesResource extends Resource
{
    /**
     * 리소스의 MIME 타입 지정.
     */
    protected string $mimeType = 'image/png';

    //
}
```

<a name="resource-error-responses"></a>
#### 에러 응답

리소스 응답에 실패했다면 `error()` 메서드를 사용합니다:

```php
return Response::error('Unable to fetch weather data for the specified location.');
```

<a name="authentication"></a>
## 인증

웹 MCP 서버의 인증은 일반 라우트와 동일하게 미들웨어를 활용하여 처리할 수 있습니다. 즉, 서버의 모든 기능 사용 전에 인증을 요구할 수 있습니다.

MCP 서버 접근 인증 방법에는 두 가지가 있습니다: [Laravel Sanctum](/docs/12.x/sanctum)을 활용한 간단한 토큰 기반 인증, 또는 OAuth 인증([Laravel Passport](/docs/12.x/passport)와 연동) 등을 사용할 수 있습니다. 또한, 직접 발급한 커스텀 API 토큰을 `Authorization` 헤더로 전달해 검증할 수도 있습니다.

<a name="oauth"></a>
### OAuth 2.1

OAuth를 통한 인증이 가장 견고하며, 특히 [Laravel Passport](/docs/12.x/passport)로 쉽게 구현할 수 있습니다.

MCP 서버를 OAuth로 인증하려면 `routes/ai.php`에서 `Mcp::oauthRoutes` 메서드를 호출해 필요한 OAuth2 디스커버리 및 클라이언트 등록 라우트를 등록하세요. 그 후, `Mcp::web` 경로에 Passport의 `auth:api` 미들웨어를 적용합니다:

```php
use App\Mcp\Servers\WeatherExample;
use Laravel\Mcp\Facades\Mcp;

Mcp::oauthRoutes();

Mcp::web('/mcp/weather', WeatherExample::class)
    ->middleware('auth:api');
```

#### Passport 신규 설치

아직 Laravel Passport를 사용하지 않는 경우, [Passport 설치 및 배포 안내](/docs/12.x/passport#installation)를 따라 기본 환경 설정을 완료하세요(예: OAuthenticatable 모델, 인증가드, 키 등).

이후 MCP에서 제공하는 Passport 인가 뷰를 다음과 같이 출판합니다:

```shell
php artisan vendor:publish --tag=mcp-views
```

이제 `AppServiceProvider`의 `boot` 메서드에서 Passport가 이 뷰를 사용하도록 지정해야 합니다:

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

이 뷰는 AI 에이전트의 인증 요청 승인/거절 시 사용자에게 표시됩니다.

![Authorization screen example](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABOAAAAROCAMAAABKc73cAAAA81BMVEX...)

> [!NOTE]
> 이 경우 OAuth는 단순히 인증 가능한 모델로 번역하는 중간 계층 역할만 하며, OAuth 스코프 등 복잡한 기능은 활용하지 않습니다.

#### 기존 Passport 설치에 통합

이미 Passport를 사용하고 있다면, 별다른 추가 설정 없이 MCP를 연동할 수 있습니다. 다만 사용되는 스코프는 `mcp:use`로 한정됩니다.

#### Passport와 Sanctum 비교

Model Context Protocol 명세에서 공식적으로 명시된 인증 방식은 OAuth2.1이며, MCP 클라이언트 중에도 가장 널리 지원됩니다. 따라서 가능하다면 Passport를 우선 추천합니다.

이미 [Sanctum](/docs/12.x/sanctum)를 사용하는 경우, 굳이 Passport를 추가하지 않아도 됩니다. 특별히 OAuth만 지원하는 MCP 클라이언트를 사용하는 필요성이 있는 경우에만 Passport 도입을 고려하세요.

<a name="sanctum"></a>
### Sanctum

[Sanctum](/docs/12.x/sanctum)으로 MCP 서버를 보호하려면, MCP 서버에 Sanctum 인증 미들웨어를 적용하고, MCP 클라이언트에서 `Authorization: Bearer <token>` 헤더를 반드시 포함시켜 요청하세요:

```php
use App\Mcp\Servers\WeatherExample;
use Laravel\Mcp\Facades\Mcp;

Mcp::web('/mcp/demo', WeatherExample::class)
    ->middleware('auth:sanctum');
```

<a name="custom-mcp-authentication"></a>
#### 커스텀 MCP 인증

애플리케이션에서 별도 자체 API 토큰을 발급해서 쓴다면, 원하는 미들웨어를 MCP 서버 라우트에 자유롭게 지정하면 됩니다. 커스텀 미들웨어 내에서 `Authorization` 헤더를 해석해 MCP 요청을 직접 인증할 수 있습니다.

<a name="authorization"></a>
## 인가

현재 인증된 사용자는 `$request->user()`로 조회할 수 있습니다. 이를 통해 툴/리소스 내에서 [인가 체크](/docs/12.x/authorization)를 수행할 수 있습니다:

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

MCP 서버는 내장된 MCP Inspector 도구 또는 유닛 테스트를 통해 검증할 수 있습니다.

<a name="mcp-inspector"></a>
### MCP 인스펙터

[MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector)는 MCP 서버의 테스트 및 디버깅을 위한 대화형 도구입니다. 서버에 직접 연결하여 인증 상태를 확인하고, 제공되는 툴, 리소스, 프롬프트의 동작을 시험해볼 수 있습니다.

Inspector는 다음 명령어로 실행할 수 있습니다:

```shell
# 웹 서버...
php artisan mcp:inspector mcp/weather

# 로컬 서버(이름이 "weather"인 경우)...
php artisan mcp:inspector weather
```

Inspector 실행 시 MCP 클라이언트 설정 정보를 함께 안내받을 수 있으며, 인증이 필요한 경우 `Authorization` 헤더 등을 올바르게 입력해야 합니다.

<a name="unit-tests"></a>
### 유닛 테스트

MCP 서버, 툴, 리소스, 프롬프트는 일반적인 PHP 테스트 코드로 검증 가능합니다.

먼저 테스트 케이스에서 MCP 서버의 기능을 직접 호출하면 됩니다. 예를 들어, `WeatherServer`의 툴을 테스트할 때:

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

프롬프트, 리소스도 유사한 방식으로 호출하여 테스트할 수 있습니다:

```php
$response = WeatherServer::prompt(...);
$response = WeatherServer::resource(...);
```

인증된 사용자가 필요한 경우에는 `actingAs` 메서드를 체이닝해서 사용할 수 있습니다:

```php
$response = WeatherServer::actingAs($user)->tool(...);
```

응답 결과에 대해 다양한 assertion 메서드를 활용할 수 있습니다.

성공 응답 여부는 `assertOk`로, 응답 내 텍스트 포함 여부는 `assertSee`로 검증합니다:

```php
$response->assertOk();
$response->assertSee('The current weather in New York City is 72°F and sunny.');
```

에러 포함 여부는 `assertHasErrors`/`assertHasNoErrors`로 판별할 수 있습니다:

```php
$response->assertHasErrors();

$response->assertHasErrors([
    'Something went wrong.',
]);
```

반대로 에러가 없어야 함을 검증하려면:

```php
$response->assertHasNoErrors();
```

응답 메타데이터를 직접 검증하고 싶다면, 다음과 같은 메서드를 사용하세요:

```php
$response->assertName('current-weather');
$response->assertTitle('Current Weather Tool');
$response->assertDescription('Fetches the current weather forecast for a specified location.');
```

노티피케이션 전송 여부도 검증할 수 있습니다:

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

마지막으로, 디버깅 목적으로 응답의 원시 내용을 확인하려면 `dd` 또는 `dump` 메서드를 사용할 수 있습니다:

```php
$response->dd();
$response->dump();
```
