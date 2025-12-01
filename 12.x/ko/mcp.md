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
    - [툴 애노테이션](#tool-annotations)
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
    - [리소스 URI와 MIME 타입](#resource-uri-and-mime-type)
    - [리소스 요청](#resource-request)
    - [리소스 의존성 주입](#resource-dependency-injection)
    - [리소스 애노테이션](#resource-annotations)
    - [조건부 리소스 등록](#conditional-resource-registration)
    - [리소스 응답](#resource-responses)
- [메타데이터](#metadata)
- [인증(Authentication)](#authentication)
    - [OAuth 2.1](#oauth)
    - [Sanctum](#sanctum)
- [인가(Authorization)](#authorization)
- [서버 테스트](#testing-servers)
    - [MCP 인스펙터](#mcp-inspector)
    - [유닛 테스트](#unit-tests)

<a name="introduction"></a>
## 소개

[Laravel MCP](https://github.com/laravel/mcp)는 [Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro)을 통해 AI 클라이언트가 여러분의 Laravel 애플리케이션과 상호작용할 수 있도록 간단하고 우아한 방식을 제공합니다. 이 패키지는 서버, 툴, 리소스, 프롬프트를 정의할 수 있는 직관적이고 유연한 인터페이스를 제공하며, 이를 통해 AI 기반 상호작용을 쉽게 구현할 수 있습니다.

<a name="installation"></a>
## 설치

먼저, Composer 패키지 매니저를 사용하여 프로젝트에 Laravel MCP를 설치합니다:

```shell
composer require laravel/mcp
```

<a name="publishing-routes"></a>
### 라우트 퍼블리싱

Laravel MCP 설치 후, `vendor:publish` 아티즌 명령어를 실행하여 MCP 서버를 정의할 `routes/ai.php` 파일을 퍼블리시합니다:

```shell
php artisan vendor:publish --tag=ai-routes
```

이 명령어를 실행하면 애플리케이션의 `routes` 디렉토리에 `routes/ai.php` 파일이 생성되며, 이 파일에서 MCP 서버를 등록할 수 있습니다.

<a name="creating-servers"></a>
## 서버 생성

`make:mcp-server` 아티즌 명령어를 사용하여 MCP 서버를 생성할 수 있습니다. 서버는 툴, 리소스, 프롬프트 등 MCP 기능을 AI 클라이언트에 노출하는 중심 역할을 합니다:

```shell
php artisan make:mcp-server WeatherServer
```

이 명령어를 실행하면 `app/Mcp/Servers` 디렉토리에 새로운 서버 클래스가 생성됩니다. 생성된 서버 클래스는 MCP의 기본 `Laravel\Mcp\Server` 클래스를 상속하며, 툴, 리소스, 프롬프트를 등록하는 속성을 제공합니다:

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
     * LLM을 위한 MCP 서버의 안내문
     */
    protected string $instructions = 'This server provides weather information and forecasts.';

    /**
     * 이 MCP 서버에 등록된 툴 목록
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Tool>>
     */
    protected array $tools = [
        // GetCurrentWeatherTool::class,
    ];

    /**
     * 이 MCP 서버에 등록된 리소스 목록
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Resource>>
     */
    protected array $resources = [
        // WeatherGuidelinesResource::class,
    ];

    /**
     * 이 MCP 서버에 등록된 프롬프트 목록
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

서버를 생성한 후에는, 해당 서버를 `routes/ai.php` 파일에 등록해 접근할 수 있도록 해야 합니다. 서버 등록에는 HTTP로 접근 가능한 `web` 방식과, 커맨드 라인 환경에 적합한 `local` 방식 두 가지가 있습니다.

<a name="web-servers"></a>
### 웹 서버

웹 서버는 가장 일반적으로 쓰이며, HTTP POST 요청을 통해 접근할 수 있어 원격 AI 클라이언트나 웹 통합에 적합합니다. 웹 서버는 `web` 메서드를 이용해 등록합니다:

```php
use App\Mcp\Servers\WeatherServer;
use Laravel\Mcp\Facades\Mcp;

Mcp::web('/mcp/weather', WeatherServer::class);
```

일반 라우트와 마찬가지로, 미들웨어를 적용하여 웹 서버를 보호할 수 있습니다:

```php
Mcp::web('/mcp/weather', WeatherServer::class)
    ->middleware(['throttle:mcp']);
```

<a name="local-servers"></a>
### 로컬 서버

로컬 서버는 아티즌 명령어로 동작하며, [Laravel Boost](/docs/12.x/installation#installing-laravel-boost)와 같은 로컬 AI 어시스턴트 연동에 이상적입니다. 로컬 서버는 `local` 메서드를 사용해 등록합니다:

```php
use App\Mcp\Servers\WeatherServer;
use Laravel\Mcp\Facades\Mcp;

Mcp::local('weather', WeatherServer::class);
```

로컬 서버를 등록한 후, 보통 `mcp:start` 아티즌 명령어를 직접 실행할 필요는 없습니다. 대신, MCP 클라이언트(AI 에이전트)에서 서버를 시작하거나 [MCP 인스펙터](#mcp-inspector)를 사용할 수 있습니다.

<a name="tools"></a>
## 툴

툴은 서버가 AI 클라이언트에 기능을 노출할 수 있도록 해줍니다. 툴을 통해 언어 모델이 특정 작업을 실행하거나 코드 실행, 외부 시스템과의 연동이 가능해집니다:

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
     * 툴 설명
     */
    protected string $description = 'Fetches the current weather forecast for a specified location.';

    /**
     * 툴 요청 핸들러
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
     * @return array<string, \Illuminate\Contracts\JsonSchema\JsonSchema>
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

툴을 생성하려면 `make:mcp-tool` 아티즌 명령어를 실행합니다:

```shell
php artisan make:mcp-tool CurrentWeatherTool
```

툴을 생성한 후에는 서버의 `$tools` 속성에 등록해야 합니다:

```php
<?php

namespace App\Mcp\Servers;

use App\Mcp\Tools\CurrentWeatherTool;
use Laravel\Mcp\Server;

class WeatherServer extends Server
{
    /**
     * 이 MCP 서버에 등록된 툴 목록
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

기본적으로, 툴의 이름(name)과 타이틀(title)은 클래스명에서 파생됩니다. 예를 들어, `CurrentWeatherTool`은 이름이 `current-weather`, 타이틀이 `Current Weather Tool`이 됩니다. `$name`과 `$title` 속성을 정의하여 직접 지정할 수 있습니다:

```php
class CurrentWeatherTool extends Tool
{
    /**
     * 툴 이름
     */
    protected string $name = 'get-optimistic-weather';

    /**
     * 툴 타이틀
     */
    protected string $title = 'Get Optimistic Weather Forecast';

    // ...
}
```

설명(description)은 자동 생성되지 않으니, 반드시 의미 있는 내용을 `$description` 속성으로 제공해야 합니다:

```php
class CurrentWeatherTool extends Tool
{
    /**
     * 툴 설명
     */
    protected string $description = 'Fetches the current weather forecast for a specified location.';

    //
}
```

> [!NOTE]
> 설명은 AI 모델이 툴을 언제, 어떻게 효과적으로 사용할지 이해하는 데 매우 중요한 메타데이터입니다.

<a name="tool-input-schemas"></a>
### 툴 입력 스키마

툴은 AI 클라이언트가 전달하는 인수를 명확하게 정의하기 위해 입력 스키마를 선언할 수 있습니다. Laravel의 `Illuminate\Contracts\JsonSchema\JsonSchema` 빌더를 사용해 툴의 입력 요구사항을 명확히 할 수 있습니다:

```php
<?php

namespace App\Mcp\Tools;

use Illuminate\Contracts\JsonSchema\JsonSchema;
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

툴은 [출력 스키마](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#output-schema)를 정의하여 반환 데이터의 구조를 명시할 수 있습니다. 이는 AI 클라이언트가 툴 결과를 더 잘 파싱할 수 있도록 도와줍니다. `outputSchema` 메서드로 출력 구조를 작성할 수 있습니다:

```php
<?php

namespace App\Mcp\Tools;

use Illuminate\Contracts\JsonSchema\JsonSchema;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * 툴 출력 스키마 반환
     *
     * @return array<string, JsonSchema>
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

JSON Schema만으로는 기본적인 구조만 제공하므로, 더 복잡한 유효성 검증이 필요한 경우도 있습니다.

Laravel MCP는 Laravel의 [유효성 검증 기능](/docs/12.x/validation)과 긴밀하게 연동합니다. 툴의 `handle` 메서드에서 들어온 인수를 다음과 같이 검증할 수 있습니다:

```php
<?php

namespace App\Mcp\Tools;

use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * 툴 요청 핸들러
     */
    public function handle(Request $request): Response
    {
        $validated = $request->validate([
            'location' => 'required|string|max:100',
            'units' => 'in:celsius,fahrenheit',
        ]);

        // 검증된 인수로 날씨 데이터 조회 ...
    }
}
```

유효성 검증이 실패할 경우, AI 클라이언트는 에러 메시지에 따라 동작하므로, 명확하고 구체적인 메시지를 제공하는 것이 중요합니다:

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

Laravel의 [서비스 컨테이너](/docs/12.x/container)를 통해 모든 MCP 툴은 자동으로 의존성 주입이 적용됩니다. 따라서, 생성자에서 필요한 의존성을 타입힌트로 선언하면 자동으로 인스턴스가 주입됩니다:

```php
<?php

namespace App\Mcp\Tools;

use App\Repositories\WeatherRepository;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * 새 툴 인스턴스 생성자
     */
    public function __construct(
        protected WeatherRepository $weather,
    ) {}

    // ...
}
```

생성자 외에도, `handle()` 메서드에서도 의존성을 타입힌트로 명시하면 서비스 컨테이너가 알아서 주입해줍니다:

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
     * 툴 요청 핸들러
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

툴에 [애노테이션](https://modelcontextprotocol.io/specification/2025-06-18/schema#toolannotations)을 추가하면 AI 클라이언트에 부가적 메타데이터를 제공할 수 있습니다. 애노테이션은 툴의 동작 방식과 특성을 설명하며, 속성(Attribute)으로 툴 클래스에 추가할 수 있습니다:

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

사용 가능한 애노테이션은 다음과 같습니다:

| 애노테이션            | 타입    | 설명                                                                                     |
| ------------------- | ------- | ------------------------------------------------------------------------------------- |
| `#[IsReadOnly]`     | boolean | 환경을 변경하지 않는 툴임을 나타냅니다.                                               |
| `#[IsDestructive]`  | boolean | (읽기 전용이 아닐 경우) 환경에 파괴적 변경 가능성이 있음을 나타냅니다.                   |
| `#[IsIdempotent]`   | boolean | 동일 인수로 반복 호출 시 추가 효과가 없음을 명시합니다(읽기 전용이 아닐 때만 의미).      |
| `#[IsOpenWorld]`    | boolean | 외부 엔터티와 상호작용할 수 있음을 명시합니다.                                         |

<a name="conditional-tool-registration"></a>
### 조건부 툴 등록

툴 클래스에 `shouldRegister` 메서드를 구현하면, 애플리케이션 상태, 설정, 요청 정보에 따라 툴의 등록 여부를 동적으로 제어할 수 있습니다:

```php
<?php

namespace App\Mcp\Tools;

use Laravel\Mcp\Request;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * 툴 등록 여부 결정
     */
    public function shouldRegister(Request $request): bool
    {
        return $request?->user()?->subscribed() ?? false;
    }
}
```

`shouldRegister`가 `false`를 반환하면 해당 툴은 목록에 나타나지 않으며, AI 클라이언트가 호출할 수 없습니다.

<a name="tool-responses"></a>
### 툴 응답

툴은 반드시 `Laravel\Mcp\Response` 인스턴스를 반환해야 합니다. Response 클래스는 여러 유형의 응답을 만들 수 있는 편리한 메서드를 제공합니다.

간단한 텍스트 응답은 `text` 메서드를 사용합니다:

```php
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;

/**
 * 툴 요청 핸들러
 */
public function handle(Request $request): Response
{
    // ...

    return Response::text('Weather Summary: Sunny, 72°F');
}
```

툴 실행 중 오류를 알리려면 `error` 메서드를 사용합니다:

```php
return Response::error('Unable to fetch weather data. Please try again.');
```

<a name="multiple-content-responses"></a>
#### 다중 콘텐츠 응답

툴은 여러 개의 Response 인스턴스 배열을 반환해 다양한 내용의 응답을 제공할 수 있습니다:

```php
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;

/**
 * 툴 요청 핸들러
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

<a name="structured-responses"></a>
#### 구조화된 응답

툴은 [구조화된 콘텐츠](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#structured-content)를 `structured` 메서드로 반환하여, AI 클라이언트가 쉽게 파싱할 수 있도록 지원합니다. 이 방식은 JSON 인코딩된 텍스트와의 호환성도 유지합니다:

```php
return Response::structured([
    'temperature' => 22.5,
    'conditions' => 'Partly cloudy',
    'humidity' => 65,
]);
```

구조화된 내용과 함께 커스텀 텍스트를 함께 제공하고 싶다면, `withStructuredContent`를 사용할 수 있습니다:

```php
return Response::make(
    Response::text('Weather is 22.5°C and sunny')
)->withStructuredContent([
    'temperature' => 22.5,
    'conditions' => 'Sunny',
]);
```

<a name="streaming-responses"></a>
#### 스트리밍 응답

장기 실행 작업이나 실시간 데이터 스트림을 위해, 툴의 `handle` 메서드에서 [제너레이터](https://www.php.net/manual/en/language.generators.overview.php)를 반환할 수 있습니다. 이를 통해 중간 진행상황 등 여러 메시지를 순차적으로 전송할 수 있습니다:

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
     * 툴 요청 핸들러
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

웹 기반 서버에서 스트리밍 응답을 사용할 경우, 자동으로 SSE(Server-Sent Events) 스트림으로 변환되어 각 메시지가 클라이언트에 실시간으로 전송됩니다.

<a name="prompts"></a>
## 프롬프트

[프롬프트](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts)는 서버가 재사용 가능한 프롬프트 템플릿을 AI 클라이언트에 제공하도록 하여, LLM과의 질의와 상호작용을 표준화합니다.

<a name="creating-prompts"></a>
### 프롬프트 생성

프롬프트를 생성하려면 `make:mcp-prompt` 아티즌 명령어를 실행합니다:

```shell
php artisan make:mcp-prompt DescribeWeatherPrompt
```

프롬프트를 만든 후, 서버의 `$prompts` 속성에 등록해야 합니다:

```php
<?php

namespace App\Mcp\Servers;

use App\Mcp\Prompts\DescribeWeatherPrompt;
use Laravel\Mcp\Server;

class WeatherServer extends Server
{
    /**
     * 이 MCP 서버에 등록된 프롬프트 목록
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

기본적으로 프롬프트의 이름과 타이틀은 클래스명에서 파생됩니다. 예를 들어 `DescribeWeatherPrompt`는 이름이 `describe-weather`, 타이틀이 `Describe Weather Prompt`가 됩니다. `$name`, `$title` 속성으로 직접 지정할 수 있습니다:

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

설명은 자동으로 생성되지 않으니, 모든 프롬프트에 의미 있는 설명을 `$description` 속성으로 제공하는 것이 좋습니다:

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
> 설명은 프롬프트의 메타데이터 중 핵심으로, AI 모델이 프롬프트를 최대한 잘 활용할 수 있게 도와줍니다.

<a name="prompt-arguments"></a>
### 프롬프트 인수

프롬프트는 AI 클라이언트가 프롬프트 템플릿을 맞춤값으로 채울 수 있도록 인수를 정의할 수 있습니다. `arguments` 메서드에서 인수를 선언하세요:

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

프롬프트 인수는 정의에 따라 자동으로 유효성 검증이 적용되지만, 더 복잡한 검증이 필요하다면 `handle` 메서드에서 Laravel 유효성 검사를 사용하면 됩니다:

```php
<?php

namespace App\Mcp\Prompts;

use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Prompt;

class DescribeWeatherPrompt extends Prompt
{
    /**
     * 프롬프트 요청 핸들러
     */
    public function handle(Request $request): Response
    {
        $validated = $request->validate([
            'tone' => 'required|string|max:50',
        ]);

        $tone = $validated['tone'];

        // tone 인자를 사용해 프롬프트 응답 생성 ...
    }
}
```

마찬가지로 명확한 유효성 검증 메시지를 제공해야 클라이언트가 올바르게 반응할 수 있습니다:

```php
$validated = $request->validate([
    'tone' => ['required','string','max:50'],
],[
    'tone.*' => 'You must specify a tone for the weather description. Examples include "formal", "casual", or "humorous".',
]);
```

<a name="prompt-dependency-injection"></a>
### 프롬프트 의존성 주입

모든 프롬프트 역시 [서비스 컨테이너](/docs/12.x/container)에서 자동으로 의존성이 주입됩니다. 즉, 생성자에 타입힌트를 선언하면 인스턴스가 주입됩니다:

```php
<?php

namespace App\Mcp\Prompts;

use App\Repositories\WeatherRepository;
use Laravel\Mcp\Server\Prompt;

class DescribeWeatherPrompt extends Prompt
{
    /**
     * 새 프롬프트 인스턴스 생성자
     */
    public function __construct(
        protected WeatherRepository $weather,
    ) {}

    //
}
```

생성자 뿐 아니라 `handle` 메서드 내에 의존성을 타입힌트로 선언해도 컨테이너가 자동 주입합니다:

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
     * 프롬프트 요청 핸들러
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

프롬프트 클래스의 `shouldRegister` 메서드를 구현하면, 애플리케이션 상태나 설정, 요청 정보를 바탕으로 등록 여부를 제어할 수 있습니다:

```php
<?php

namespace App\Mcp\Prompts;

use Laravel\Mcp\Request;
use Laravel\Mcp\Server\Prompt;

class CurrentWeatherPrompt extends Prompt
{
    /**
     * 프롬프트 등록 여부 결정
     */
    public function shouldRegister(Request $request): bool
    {
        return $request?->user()?->subscribed() ?? false;
    }
}
```

`shouldRegister`가 `false`면 해당 프롬프트는 목록에 보이지 않으며 호출할 수 없습니다.

<a name="prompt-responses"></a>
### 프롬프트 응답

프롬프트는 하나의 `Laravel\Mcp\Response` 또는 여러 Response 인스턴스(iterable)를 반환할 수 있습니다. 응답은 AI 클라이언트에 전달될 내용을 캡슐화합니다:

```php
<?php

namespace App\Mcp\Prompts;

use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Prompt;

class DescribeWeatherPrompt extends Prompt
{
    /**
     * 프롬프트 요청 핸들러
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

`asAssistant()` 메서드를 사용하면 해당 메시지가 AI 어시스턴트가 보낸 것으로 인식되며, 일반 메시지는 사용자 입력으로 처리됩니다.

<a name="resources"></a>
## 리소스

[리소스](https://modelcontextprotocol.io/specification/2025-06-18/server/resources)는 서버가 AI 클라이언트에 데이터 또는 콘텐츠를 제공하는 수단입니다. AI가 언어 모델 상호작용 시 참고할 수 있는 문서/설정 등 정적 또는 동적 데이터를 전달할 수 있습니다.

<a name="creating-resources"></a>
## 리소스 생성

리소스를 생성하려면 `make:mcp-resource` 아티즌 명령어를 실행합니다:

```shell
php artisan make:mcp-resource WeatherGuidelinesResource
```

생성한 후, 서버의 `$resources` 속성에 등록합니다:

```php
<?php

namespace App\Mcp\Servers;

use App\Mcp\Resources\WeatherGuidelinesResource;
use Laravel\Mcp\Server;

class WeatherServer extends Server
{
    /**
     * 이 MCP 서버에 등록된 리소스 목록
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

리소스의 이름과 타이틀 역시 기본적으로 클래스명에서 파생됩니다. 예: `WeatherGuidelinesResource` → 이름: `weather-guidelines`, 타이틀: `Weather Guidelines Resource`. `$name`, `$title` 속성으로 직접 지정할 수도 있습니다:

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

설명은 자동 생성되지 않으니, `$description` 속성에 명확하게 정의하는 것이 바람직합니다:

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
> 설명은 AI 모델이 리소스를 효과적으로 활용할 시점을 이해하는 데 매우 중요한 메타데이터입니다.

<a name="resource-uri-and-mime-type"></a>
### 리소스 URI와 MIME 타입

모든 리소스는 고유 URI로 구분되며, 데이터 포맷을 설명하는 MIME 타입을 가집니다.

기본적으로 이름을 기반으로 URI가 생성되어, `WeatherGuidelinesResource`는 `weather://resources/weather-guidelines`라는 URI와 `text/plain` 타입을 갖습니다.

원한다면 `$uri`, `$mimeType` 속성으로 값을 변경할 수 있습니다:

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

URI와 MIME 타입은 AI 클라이언트가 리소스 데이터를 정확히 해석・처리하는 데 도움을 줍니다.

<a name="resource-request"></a>
### 리소스 요청

툴/프롬프트와 달리, 리소스에는 입력 스키마나 인수 개념이 없습니다. 다만 `handle` 메서드 내에서 요청에 접근할 수 있습니다:

```php
<?php

namespace App\Mcp\Resources;

use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Resource;

class WeatherGuidelinesResource extends Resource
{
    /**
     * 리소스 요청 핸들러
     */
    public function handle(Request $request): Response
    {
        // ...
    }
}
```

<a name="resource-dependency-injection"></a>
### 리소스 의존성 주입

모든 리소스 역시 [서비스 컨테이너](/docs/12.x/container)로부터 의존성을 주입받을 수 있습니다:

```php
<?php

namespace App\Mcp\Resources;

use App\Repositories\WeatherRepository;
use Laravel\Mcp\Server\Resource;

class WeatherGuidelinesResource extends Resource
{
    /**
     * 새 리소스 인스턴스 생성
     */
    public function __construct(
        protected WeatherRepository $weather,
    ) {}

    // ...
}
```

`handle` 메서드에서도 동일하게 의존성 타입힌트로 자동 주입이 가능합니다:

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
     * 리소스 요청 핸들러
     */
    public function handle(WeatherRepository $weather): Response
    {
        $guidelines = $weather->guidelines();

        return Response::text($guidelines);
    }
}
```

<a name="resource-annotations"></a>
### 리소스 애노테이션

리소스에 [애노테이션](https://modelcontextprotocol.io/specification/2025-06-18/schema#resourceannotations)을 추가해, AI 클라이언트에 부가적 메타데이터를 제공할 수 있습니다. 이는 속성(Attribute)으로 클래스에 선언합니다:

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

사용 가능한 애노테이션 설명은 다음과 같습니다:

| 애노테이션         | 타입         | 설명                                                                                   |
| ----------------- | ------------ | ------------------------------------------------------------------------------------- |
| `#[Audience]`     | Role/배열    | 대상 오디언스 명시 (`Role::User`, `Role::Assistant` 등)                               |
| `#[Priority]`     | float        | 0.0~1.0 사이의 중요도 점수                                                            |
| `#[LastModified]` | string       | 리소스 마지막 수정이력(ISO 8601 타임스탬프)                                           |

<a name="conditional-resource-registration"></a>
### 조건부 리소스 등록

리소스 클래스의 `shouldRegister` 메서드를 통해, 애플리케이션 상태나 요청 정보를 기반으로 리소스의 등록 여부를 동적으로 제어할 수 있습니다:

```php
<?php

namespace App\Mcp\Resources;

use Laravel\Mcp\Request;
use Laravel\Mcp\Server\Resource;

class WeatherGuidelinesResource extends Resource
{
    /**
     * 리소스 등록 여부 결정
     */
    public function shouldRegister(Request $request): bool
    {
        return $request?->user()?->subscribed() ?? false;
    }
}
```

`shouldRegister`가 `false`일 경우, 해당 리소스는 목록 및 클라이언트 호출 대상에서 제외됩니다.

<a name="resource-responses"></a>
### 리소스 응답

리소스는 반드시 `Laravel\Mcp\Response` 인스턴스를 반환해야 하며, 다양한 유형의 응답 생성이 가능합니다.

단순 텍스트 응답을 위해서는 `text` 메서드를 사용합니다:

```php
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;

/**
 * 리소스 요청 핸들러
 */
public function handle(Request $request): Response
{
    // ...

    return Response::text($weatherData);
}
```

<a name="resource-blob-responses"></a>
#### Blob 응답

바이너리 데이터를 반환하려면 `blob` 메서드와 실제 바이너리 콘텐츠를 사용하세요:

```php
return Response::blob(file_get_contents(storage_path('weather/radar.png')));
```

이때 MIME 타입은 리소스 클래스의 `$mimeType` 속성값이 사용됩니다:

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
#### 오류 응답

리소스 조회 중 에러가 발생한 경우, `error()` 메서드로 오류 메시지를 반환할 수 있습니다:

```php
return Response::error('Unable to fetch weather data for the specified location.');
```

<a name="metadata"></a>
## 메타데이터

Laravel MCP는 [MCP 스펙](https://modelcontextprotocol.io/specification/2025-06-18/basic#meta)에서 정의하는 `_meta` 필드를 지원합니다. 이 필드는 MCP 클라이언트나 통합 시스템에서 필요할 수 있으며, 툴, 리소스, 프롬프트 및 응답 콘텐츠에 모두 적용할 수 있습니다.

개별 응답 콘텐츠에 메타데이터를 추가하고자 할 때는, `withMeta` 메서드를 사용합니다:

```php
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;

/**
 * 툴 요청 핸들러
 */
public function handle(Request $request): Response
{
    return Response::text('The weather is sunny.')
        ->withMeta(['source' => 'weather-api', 'cached' => true]);
}
```

응답 전체 레벨의 메타데이터를 부여하려면 `Response::make`로 감싼 뒤 `.withMeta`를 호출합니다:

```php
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\ResponseFactory;

/**
 * 툴 요청 핸들러
 */
public function handle(Request $request): ResponseFactory
{
    return Response::make(
        Response::text('The weather is sunny.')
    )->withMeta(['request_id' => '12345']);
}
```

툴, 리소스, 프롬프트 클래스 자체에 메타데이터를 추가하고자 할 땐, 클래스에 `$meta` 속성을 선언합니다:

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

일반 라우트와 마찬가지로, 웹 MCP 서버에 미들웨어를 적용하여 인증을 처리할 수 있습니다. 인증이 걸린 MCP 서버에서는 사용자가 인증을 마쳐야 서버의 모든 기능을 사용할 수 있습니다.

MCP 서버 인증 방식은 두 가지가 있습니다:
1. [Sanctum](/docs/12.x/sanctum) 또는 HTTP 헤더의 임의 토큰을 이용한 간단한 토큰 기반 인증
2. [Laravel Passport](/docs/12.x/passport)를 통한 OAuth 인증

<a name="oauth"></a>
### OAuth 2.1

웹 기반 MCP 서버를 보호하는 가장 강력한 방법은 [Laravel Passport](/docs/12.x/passport)를 사용하는 OAuth입니다.

OAuth 인증을 적용할 땐, `routes/ai.php`에서 `Mcp::oauthRoutes` 메서드로 필요한 OAuth2 디스커버리/클라이언트 등록 라우트를 추가하세요. 이후, `Mcp::web` 라우트에 Passport의 `auth:api` 미들웨어를 적용합니다:

```php
use App\Mcp\Servers\WeatherExample;
use Laravel\Mcp\Facades\Mcp;

Mcp::oauthRoutes();

Mcp::web('/mcp/weather', WeatherExample::class)
    ->middleware('auth:api');
```

#### Passport 신규 설치

아직 Laravel Passport를 사용하고 있지 않다면, [Passport 설치 및 배포 가이드](/docs/12.x/passport#installation)를 따라 환경을 세팅해야 합니다. (OAuthenticatable 모델, 인증 가드, Passport 키 필요)

다음으로 MCP가 제공하는 Passport 인증 뷰를 퍼블리시하세요:

```shell
php artisan vendor:publish --tag=mcp-views
```

그 후, `AppServiceProvider`의 `boot` 메서드에서 `Passport::authorizationView`를 호출해 이 뷰를 사용하도록 설정합니다:

```php
use Laravel\Passport\Passport;

/**
 * 부트스트랩 서비스
 */
public function boot(): void
{
    Passport::authorizationView(function ($parameters) {
        return view('mcp.authorize', $parameters);
    });
}
```

이 뷰는 유저가 AI 에이전트 인증 요청을 승인·거부하는 화면으로 표시됩니다.

![Authorization screen example](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABOAAAAROCAMAAABKc73cAAAA81BMVEX...)

> [!NOTE]
> 이 상황에서는 OAuth를 인증 가능한 모델로의 단순 매핑 계층으로만 사용하며, scope 등 OAuth의 다양한 기능은 무시합니다.

#### 기존 Passport 설치와 연동

이미 Laravel Passport를 사용 중이라면 MCP도 별다른 문제 없이 함께 동작합니다. 다만, 현재는 OAuth를 단순 매핑 계층으로만 사용하므로 커스텀 scope 등은 지원하지 않습니다.

`Mcp::oauthRoutes` 메서드를 통해 `mcp:use` scope 하나만 추가, 광고, 사용됩니다.

#### Passport vs. Sanctum

Model Context Protocol 스펙에서 공식적으로 인정하는 인증 메커니즘은 OAuth2.1이며, MCP 클라이언트 사이에서 가장 폭넓게 지원됩니다. 가능한 경우 Passport 사용을 권장합니다.

애플리케이션에서 [Sanctum](/docs/12.x/sanctum)만 쓰는 경우 Passport 추가가 번거롭다면 우선은 Sanctum만 사용하는 것이 좋습니다. MCP 클라이언트가 OAuth만 지원하는 등 명확하게 필요하지 않다면 굳이 Passport를 추가하지 않아도 됩니다.

<a name="sanctum"></a>
### Sanctum

[Sanctum](/docs/12.x/sanctum)으로 MCP 서버를 보호하려면, `routes/ai.php`에서 미들웨어로 `auth:sanctum`을 추가하면 됩니다. MCP 클라이언트는 반드시 `Authorization: Bearer <token>` 헤더를 추가해야 인증이 완료됩니다:

```php
use App\Mcp\Servers\WeatherExample;
use Laravel\Mcp\Facades\Mcp;

Mcp::web('/mcp/demo', WeatherExample::class)
    ->middleware('auth:sanctum');
```

<a name="custom-mcp-authentication"></a>
#### 커스텀 MCP 인증

애플리케이션에서 자체 커스텀 API 토큰을 발급한다면, 원하는 미들웨어를 MCP 웹 라우트에 직접 할당해 인증을 처리할 수 있습니다. 직접 `Authorization` 헤더를 확인해 인증 로직을 구현하면 됩니다.

<a name="authorization"></a>
## 인가(Authorization)

현재 인증된 사용자를 `$request->user()` 메서드로 가져올 수 있으므로, MCP 툴/리소스 내부에서 [인가 체크](/docs/12.x/authorization)를 수행할 수 있습니다:

```php
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;

/**
 * 툴 요청 핸들러
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

MCP 서버는 기본 제공 MCP 인스펙터(MCP Inspector) 또는 유닛 테스트 작성으로 테스트할 수 있습니다.

<a name="mcp-inspector"></a>
### MCP 인스펙터

[MCP 인스펙터](https://modelcontextprotocol.io/docs/tools/inspector)는 MCP 서버 테스트·디버깅을 돕는 대화형 툴입니다. 서버 연결, 인증 확인, 툴/리소스/프롬프트 동작 테스트가 가능합니다.

모든 등록된 서버에 대해 다음과 같이 인스펙터를 실행할 수 있습니다:

```shell
# 웹 서버일 때...
php artisan mcp:inspector mcp/weather

# "weather"라는 로컬 서버일 때...
php artisan mcp:inspector weather
```

이 명령어를 실행하면 MCP 인스펙터가 시작되며, 클라이언트에 복사해 사용할 수 있는 설정을 안내합니다. 웹 서버가 인증 미들웨어로 보호되는 경우, 접속 시 올바른 헤더(예: Authorization Bearer 토큰)를 반드시 포함해야 합니다.

<a name="unit-tests"></a>
### 유닛 테스트

MCP 서버, 툴, 리소스, 프롬프트 각각에 대한 유닛 테스트를 작성할 수 있습니다.

예를 들어, `WeatherServer`에서 툴을 테스트하려면 테스트 케이스를 만들고 해당 툴을 호출하면 됩니다:

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

프롬프트, 리소스도 유사하게 테스트할 수 있습니다:

```php
$response = WeatherServer::prompt(...);
$response = WeatherServer::resource(...);
```

인증된 사용자로 시나리오를 테스트하려면, `actingAs`를 앞에 체이닝하여 사용할 수 있습니다:

```php
$response = WeatherServer::actingAs($user)->tool(...);
```

응답을 받은 후에는 다양한 assertion 메서드로 응답의 내용과 상태를 검증할 수 있습니다.

응답이 성공적임을 확인하려면 `assertOk`를 사용하세요:

```php
$response->assertOk();
```

응답에 특정 텍스트가 포함되어 있는지 확인하려면 `assertSee`를 사용합니다:

```php
$response->assertSee('The current weather in New York City is 72°F and sunny.');
```

에러가 포함되어 있는지 확인하려면 `assertHasErrors`를 사용합니다:

```php
$response->assertHasErrors();

$response->assertHasErrors([
    'Something went wrong.',
]);
```

에러가 없는지 체크하려면 `assertHasNoErrors`를 사용하세요:

```php
$response->assertHasNoErrors();
```

응답의 이름, 타이틀, 설명 등 메타데이터를 체크하려면:

```php
$response->assertName('current-weather');
$response->assertTitle('Current Weather Tool');
$response->assertDescription('Fetches the current weather forecast for a specified location.');
```

Notification이 전송되었는지 테스트하려면 `assertSentNotification`, 총 개수를 확인하려면 `assertNotificationCount`를 사용합니다:

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

마지막으로, 디버깅 목적으로 응답의 원본 내용을 확인하려면 `dd` 또는 `dump`를 호출할 수 있습니다:

```php
$response->dd();
$response->dump();
```
