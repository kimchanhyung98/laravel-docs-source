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
    - [툴 주석](#tool-annotations)
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
    - [리소스 주석](#resource-annotations)
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

[Laravel MCP](https://github.com/laravel/mcp)는 [Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro)을 통해 AI 클라이언트가 Laravel 애플리케이션과 상호작용할 수 있는 간단하고 우아한 방법을 제공합니다. 서버, 툴, 리소스, 프롬프트를 유연하고 직관적으로 정의할 수 있게 하여, 애플리케이션에서 AI 기반 상호작용을 손쉽게 지원합니다.

<a name="installation"></a>
## 설치

시작하려면, Composer 패키지 매니저를 사용해 Laravel MCP를 프로젝트에 설치합니다:

```shell
composer require laravel/mcp
```

<a name="publishing-routes"></a>
### 라우트 퍼블리싱

Laravel MCP 설치 후 `vendor:publish` Artisan 명령어를 실행해 `routes/ai.php` 파일을 퍼블리시합니다. 이 파일에서 MCP 서버를 정의하게 됩니다:

```shell
php artisan vendor:publish --tag=ai-routes
```

이 명령어는 애플리케이션의 `routes` 디렉터리에 `routes/ai.php` 파일을 생성하며, MCP 서버 등록에 사용합니다.

<a name="creating-servers"></a>
## 서버 생성

`make:mcp-server` Artisan 명령어를 사용해 MCP 서버를 생성할 수 있습니다. 서버는 MCP의 중심 역할을 하며, 툴, 리소스, 프롬프트 등 MCP 기능을 AI 클라이언트에 노출하는 지점입니다:

```shell
php artisan make:mcp-server WeatherServer
```

이 명령으로 `app/Mcp/Servers` 디렉터리에 서버 클래스가 생성됩니다. 생성된 서버 클래스는 MCP의 기본 `Laravel\Mcp\Server` 클래스를 확장하며, 서버 구성과 툴/리소스/프롬프트 등록을 위한 속성을 제공합니다:

```php
<?php

namespace App\Mcp\Servers;

use Laravel\Mcp\Server\Attributes\Instructions;
use Laravel\Mcp\Server\Attributes\Name;
use Laravel\Mcp\Server\Attributes\Version;
use Laravel\Mcp\Server;

#[Name('Weather Server')]
#[Version('1.0.0')]
#[Instructions('This server provides weather information and forecasts.')]
class WeatherServer extends Server
{
    /**
     * MCP 서버에 등록된 툴 배열입니다.
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Tool>>
     */
    protected array $tools = [
        // GetCurrentWeatherTool::class,
    ];

    /**
     * MCP 서버에 등록된 리소스 배열입니다.
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Resource>>
     */
    protected array $resources = [
        // WeatherGuidelinesResource::class,
    ];

    /**
     * MCP 서버에 등록된 프롬프트 배열입니다.
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

서버를 생성했다면, 반드시 `routes/ai.php` 파일에 등록하여 외부에서 접근 가능하도록 해야 합니다. 서버는 `web`(HTTP로 접근 가능한 서버) 또는 `local`(커맨드라인 서버) 방식으로 등록할 수 있습니다.

<a name="web-servers"></a>
### 웹 서버

웹 서버는 HTTP POST 요청으로 접근하는 가장 일반적인 유형의 서버로, 원격 AI 클라이언트나 웹 기반 연동에 적합합니다. 웹 서버는 `web` 메서드를 사용해 등록합니다:

```php
use App\Mcp\Servers\WeatherServer;
use Laravel\Mcp\Facades\Mcp;

Mcp::web('/mcp/weather', WeatherServer::class);
```

일반 라우트처럼, 미들웨어를 적용하여 보안 처리가 가능합니다:

```php
Mcp::web('/mcp/weather', WeatherServer::class)
    ->middleware(['throttle:mcp']);
```

<a name="local-servers"></a>
### 로컬 서버

로컬 서버는 Artisan 명령어로 동작하며, [Laravel Boost](/docs/12.x/installation#installing-laravel-boost)와 같이 로컬 AI 도우미 통합 등에 적합합니다. `local` 메서드로 등록할 수 있습니다:

```php
use App\Mcp\Servers\WeatherServer;
use Laravel\Mcp\Facades\Mcp;

Mcp::local('weather', WeatherServer::class);
```

로컬 서버 등록 후에는 일반적으로 직접 `mcp:start` Artisan 명령어를 실행할 필요는 없습니다. 대신 MCP 클라이언트(AI 에이전트)를 통해 서버를 시작하거나, [MCP Inspector](#mcp-inspector)를 사용할 수 있습니다.

<a name="tools"></a>
## 툴

툴은 서버가 AI 클라이언트에 기능을 제공하는 방식입니다. 툴을 통해 언어 모델이 직접 코드 실행, 외부 시스템 연동 등 다양한 작업을 할 수 있습니다:

```php
<?php

namespace App\Mcp\Tools;

use Illuminate\Contracts\JsonSchema\JsonSchema;
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Attributes\Description;
use Laravel\Mcp\Server\Tool;

#[Description('Fetches the current weather forecast for a specified location.')]
class CurrentWeatherTool extends Tool
{
    /**
     * 툴 요청을 처리합니다.
     */
    public function handle(Request $request): Response
    {
        $location = $request->get('location');

        // Get weather...

        return Response::text('The weather is...');
    }

    /**
     * 툴의 입력(인수) 스키마를 반환합니다.
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

툴을 생성한 후, 해당 서버의 `$tools` 속성에 등록해야 합니다:

```php
<?php

namespace App\Mcp\Servers;

use App\Mcp\Tools\CurrentWeatherTool;
use Laravel\Mcp\Server;

class WeatherServer extends Server
{
    /**
     * MCP 서버에 등록된 툴 배열입니다.
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Tool>>
     */
    protected array $tools = [
        CurrentWeatherTool::class,
    ];
}
```

#### 툴 이름, 타이틀, 설명

기본적으로 툴의 이름과 타이틀은 클래스명에서 파생됩니다. 예를 들어, `CurrentWeatherTool`은 이름이 `current-weather`, 타이틀이 `Current Weather Tool`이 됩니다. `Name`과 `Title` 속성 어트리뷰트를 사용하여 값을 직접 지정할 수 있습니다:

```php
use Laravel\Mcp\Server\Attributes\Name;
use Laravel\Mcp\Server\Attributes\Title;

#[Name('get-optimistic-weather')]
#[Title('Get Optimistic Weather Forecast')]
class CurrentWeatherTool extends Tool
{
    // ...
}
```

툴 설명은 자동 생성되지 않으니, `Description` 어트리뷰트를 사용해 반드시 명확하게 작성해 주세요:

```php
use Laravel\Mcp\Server\Attributes\Description;

#[Description('Fetches the current weather forecast for a specified location.')]
class CurrentWeatherTool extends Tool
{
    //
}
```

> [!NOTE]
> 설명은 AI 모델이 해당 툴의 용도와 동작 방식을 이해하는 데 매우 중요하므로, 언제나 신경 써서 작성해야 합니다.

<a name="tool-input-schemas"></a>
### 툴 입력 스키마

툴은 AI 클라이언트로부터 어떤 인수(argument)를 받을지 입력 스키마를 정의할 수 있습니다. Laravel의 `Illuminate\Contracts\JsonSchema\JsonSchema` 빌더를 사용합니다:

```php
<?php

namespace App\Mcp\Tools;

use Illuminate\Contracts\JsonSchema\JsonSchema;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * 툴 입력 스키마를 반환합니다.
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

툴은 [출력 스키마](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#output-schema)를 정의하여 응답의 구조를 지정할 수 있습니다. AI 클라이언트가 결과를 파싱하기 쉽게 도와줍니다. `outputSchema` 메서드를 사용해 정의할 수 있습니다:

```php
<?php

namespace App\Mcp\Tools;

use Illuminate\Contracts\JsonSchema\JsonSchema;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * 툴 출력 스키마를 반환합니다.
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

JSON 스키마는 툴 인수의 기본 구조만 정의합니다. 더 복잡한 유효성 검증이 필요하다면 Laravel의 [유효성 검증 기능](/docs/12.x/validation)과 자연스럽게 연동할 수 있습니다. 툴의 `handle` 메서드 안에서 인수 검증을 수행하세요:

```php
<?php

namespace App\Mcp\Tools;

use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * 툴 요청을 처리합니다.
     */
    public function handle(Request $request): Response
    {
        $validated = $request->validate([
            'location' => 'required|string|max:100',
            'units' => 'in:celsius,fahrenheit',
        ]);

        // 유효성 검증된 인수로 날씨 조회...
    }
}
```

유효성 검증에 실패하면, AI 클라이언트는 제공한 메시지에 따라 행동합니다. 따라서 명확하고 구체적인 오류 메시지를 제공하는 것이 중요합니다:

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

Laravel의 [서비스 컨테이너](/docs/12.x/container)를 통해 모든 MCP 툴을 해석합니다. 따라서, 필요로 하는 의존성은 생성자 타입힌트로 선언하면 자동으로 주입됩니다:

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

생성자 외에도, `handle()` 메서드의 매개변수로 타입힌트를 지정하면 서비스 컨테이너가 자동으로 주입해줍니다:

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
     * 툴 요청을 처리합니다.
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
### 툴 주석

툴에 [주석(annotation)](https://modelcontextprotocol.io/specification/2025-06-18/schema#toolannotations)을 추가하여 AI 클라이언트에 추가적인 메타데이터를 제공할 수 있습니다. 주석은 툴의 동작과 특성을 AI 모델이 이해하는 데 도움을 줍니다. 어트리뷰트 방식으로 주석을 추가할 수 있습니다:

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

사용 가능한 주석과 설명:

| 주석(Annotation)    | 타입     | 설명                                                                                     |
| ------------------ | ------- | --------------------------------------------------------------------------------------- |
| `#[IsReadOnly]`    | boolean | 툴이 환경을 변경하지 않음을 나타냅니다.                                               |
| `#[IsDestructive]` | boolean | 툴이 파괴적인(비가역적) 작업을 할 수 있음을 나타냅니다.                               |
| `#[IsIdempotent]`  | boolean | 동일 인수로 여러 번 호출해도 추가 효과가 없음을 의미합니다(읽기 전용이 아닐 때만 의미). |
| `#[IsOpenWorld]`   | boolean | 툴이 외부 엔티티와 상호작용할 수 있는지 여부를 나타냅니다.                           |

주석 값은 명시적으로 boolean 인자 전달로 지정할 수 있습니다:

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

툴 클래스로 `shouldRegister` 메서드를 구현하면, 런타임에서 툴의 노출 여부를 동적으로 결정할 수 있습니다. 애플리케이션 상태, 설정, 요청 파라미터 등에 따라 동작할 수 있습니다:

```php
<?php

namespace App\Mcp\Tools;

use Laravel\Mcp\Request;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * 툴 등록 여부를 결정합니다.
     */
    public function shouldRegister(Request $request): bool
    {
        return $request?->user()?->subscribed() ?? false;
    }
}
```

`shouldRegister`가 `false`를 반환하면 해당 툴은 노출되지 않으며 AI 클라이언트가 호출할 수 없습니다.

<a name="tool-responses"></a>
### 툴 응답

툴은 반드시 `Laravel\Mcp\Response` 인스턴스를 반환해야 합니다. Response 클래스는 여러 가지 편리한 응답 생성 메서드를 제공합니다.

간단한 텍스트 응답 생성에는 `text` 메서드를 사용합니다:

```php
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;

/**
 * 툴 요청을 처리합니다.
 */
public function handle(Request $request): Response
{
    // ...

    return Response::text('Weather Summary: Sunny, 72°F');
}
```

툴 실행 중 오류를 알릴 때는 `error` 메서드를 사용합니다:

```php
return Response::error('Unable to fetch weather data. Please try again.');
```

#### 다중 콘텐츠 응답

여러 개의 콘텐츠를 반환하고 싶을 때는 `Response` 인스턴스 배열을 반환할 수 있습니다:

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

#### 구조화된 응답

[구조화된 콘텐츠](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#structured-content)는 `structured` 메서드를 통해 반환할 수 있습니다. 이는 AI 클라이언트가 데이터를 쉽게 파싱할 수 있게 하면서 JSON 인코딩된 텍스트 호환성도 보장합니다:

```php
return Response::structured([
    'temperature' => 22.5,
    'conditions' => 'Partly cloudy',
    'humidity' => 65,
]);
```

구조화된 콘텐츠와 함께 텍스트를 추가하고 싶을 때는 `withStructuredContent` 메서드를 사용하세요:

```php
return Response::make(
    Response::text('Weather is 22.5°C and sunny')
)->withStructuredContent([
    'temperature' => 22.5,
    'conditions' => 'Sunny',
]);
```

#### 스트리밍 응답

장시간 실행되거나 실시간 데이터 스트림이 필요한 경우, `handle` 메서드에서 [generator](https://www.php.net/manual/en/language.generators.overview.php)를 리턴하여 중간 상태를 AI 클라이언트에 실시간으로 전달할 수 있습니다:

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

웹 서버에서 사용할 경우, 스트리밍 응답은 자동으로 SSE(Server-Sent Events) 스트림을 오픈하여 각 메시지를 클라이언트로 전송합니다.

<a name="prompts"></a>
## 프롬프트

[프롬프트](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts)는 서버가 AI 클라이언트에 재사용 가능한 프롬프트 템플릿을 제공할 수 있게 합니다. 이를 통해 주요 질문 및 상호작용 흐름을 표준화할 수 있습니다.

<a name="creating-prompts"></a>
### 프롬프트 생성

`make:mcp-prompt` Artisan 명령어로 프롬프트를 생성합니다:

```shell
php artisan make:mcp-prompt DescribeWeatherPrompt
```

프롬프트를 생성한 후, 해당 서버의 `$prompts` 속성에 등록하세요:

```php
<?php

namespace App\Mcp\Servers;

use App\Mcp\Prompts\DescribeWeatherPrompt;
use Laravel\Mcp\Server;

class WeatherServer extends Server
{
    /**
     * MCP 서버에 등록된 프롬프트 배열입니다.
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Prompt>>
     */
    protected array $prompts = [
        DescribeWeatherPrompt::class,
    ];
}
```

#### 프롬프트 이름, 타이틀, 설명

기본적으로 프롬프트의 이름과 타이틀은 클래스명에서 파생됩니다. 예를 들면 `DescribeWeatherPrompt`는 이름이 `describe-weather`, 타이틀이 `Describe Weather Prompt`가 됩니다. 필요시 `Name`, `Title` 어트리뷰트로 값을 커스터마이즈 할 수 있습니다:

```php
use Laravel\Mcp\Server\Attributes\Name;
use Laravel\Mcp\Server\Attributes\Title;

#[Name('weather-assistant')]
#[Title('Weather Assistant Prompt')]
class DescribeWeatherPrompt extends Prompt
{
    // ...
}
```

설명은 자동 생성되지 않으므로, `Description` 어트리뷰트를 사용하여 꼭 작성하세요:

```php
use Laravel\Mcp\Server\Attributes\Description;

#[Description('Generates a natural-language explanation of the weather for a given location.')]
class DescribeWeatherPrompt extends Prompt
{
    //
}
```

> [!NOTE]
> 설명은 AI 모델이 프롬프트를 언제 어떻게 활용해야 하는지 이해하는 데 매우 중요합니다.

<a name="prompt-arguments"></a>
### 프롬프트 인수

프롬프트는 AI 클라이언트가 프롬프트 템플릿을 맞춤화할 수 있도록 인수를 정의할 수 있습니다. `arguments` 메서드에서 받아들일 인수를 배열로 정의하세요:

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

프롬프트 인수는 기본적으로 정의에 따라 자동 검증됩니다. 그러나 더 복잡한 검증이 필요한 경우 Laravel의 [유효성 검증](/docs/12.x/validation) 기능을 프롬프트의 `handle` 메서드에서 사용할 수 있습니다:

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

        // 주어진 톤으로 프롬프트 응답 생성...
    }
}
```

명확한 오류 메시지 제공 또한 중요합니다:

```php
$validated = $request->validate([
    'tone' => ['required','string','max:50'],
],[
    'tone.*' => 'You must specify a tone for the weather description. Examples include "formal", "casual", or "humorous".',
]);
```

<a name="prompt-dependency-injection"></a>
### 프롬프트 의존성 주입

모든 프롬프트 역시 [서비스 컨테이너](/docs/12.x/container)로 해석되므로, 생성자 또는 `handle` 메서드에서 타입힌트로 의존성을 선언하면 자동 주입됩니다:

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

또는 handle 메서드에서도 자동 주입 가능합니다:

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

프롬프트 클래스에서 `shouldRegister` 메서드를 정의하여 런타임 상태나 설정, 요청 값에 따라 노출 여부를 결정할 수 있습니다:

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

`shouldRegister`가 `false` 반환 시 해당 프롬프트는 목록에 나타나지 않고 AI 클라이언트가 호출할 수 없습니다.

<a name="prompt-responses"></a>
### 프롬프트 응답

프롬프트는 `Laravel\Mcp\Response` 또는 반복 가능한(Response 배열) 인스턴스를 반환할 수 있습니다. 각 응답은 AI 클라이언트로 전송될 콘텐츠를 캡슐화합니다:

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

`asAssistant()` 메서드는 해당 응답이 AI 어시스턴트의 메시지임을 나타낼 수 있습니다.

<a name="resources"></a>
## 리소스

[리소스](https://modelcontextprotocol.io/specification/2025-06-18/server/resources)는 서버가 AI 클라이언트에 데이터를 제공할 수 있도록 해줍니다. 문서, 설정, 각종 동적/정적 데이터 등 AI가 더 나은 답변을 만드는 데 도움이 되는 정보를 노출합니다.

<a name="creating-resources"></a>
## 리소스 생성

`make:mcp-resource` Artisan 명령어로 리소스를 생성합니다:

```shell
php artisan make:mcp-resource WeatherGuidelinesResource
```

리소스 생성 후, 해당 서버의 `$resources` 속성에 등록하세요:

```php
<?php

namespace App\Mcp\Servers;

use App\Mcp\Resources\WeatherGuidelinesResource;
use Laravel\Mcp\Server;

class WeatherServer extends Server
{
    /**
     * MCP 서버에 등록된 리소스 배열입니다.
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Resource>>
     */
    protected array $resources = [
        WeatherGuidelinesResource::class,
    ];
}
```

#### 리소스 이름, 타이틀, 설명

클래스명에서 이름과 타이틀이 파생됩니다. 예) `WeatherGuidelinesResource` → `weather-guidelines`, `Weather Guidelines Resource`. `Name` 및 `Title` 어트리뷰트로 변경 가능합니다:

```php
use Laravel\Mcp\Server\Attributes\Name;
use Laravel\Mcp\Server\Attributes\Title;

#[Name('weather-api-docs')]
#[Title('Weather API Documentation')]
class WeatherGuidelinesResource extends Resource
{
    // ...
}
```

설명은 반드시 직접 작성해야 하며, `Description` 어트리뷰트를 사용하세요:

```php
use Laravel\Mcp\Server\Attributes\Description;

#[Description('Comprehensive guidelines for using the Weather API.')]
class WeatherGuidelinesResource extends Resource
{
    //
}
```

> [!NOTE]
> 설명은 AI 모델이 리소스의 용도와 사용 시점을 이해하는 데 중요합니다.

<a name="resource-templates"></a>
### 리소스 템플릿

[리소스 템플릿](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#resource-templates)은 변수를 포함한 URI 패턴을 통해 동적으로 여러 리소스를 정의할 수 있는 기능입니다. 정적 URI 대신 템플릿 패턴을 사용하여 다양한 리소스에 대응할 수 있습니다.

#### 리소스 템플릿 생성

리소스 클래스에 `HasUriTemplate` 인터페이스를 구현하고, `uriTemplate` 메서드에서 `UriTemplate` 인스턴스를 반환하면 됩니다:

```php
<?php

namespace App\Mcp\Resources;

use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Attributes\Description;
use Laravel\Mcp\Server\Attributes\MimeType;
use Laravel\Mcp\Server\Contracts\HasUriTemplate;
use Laravel\Mcp\Server\Resource;
use Laravel\Mcp\Support\UriTemplate;

#[Description('Access user files by ID')]
#[MimeType('text/plain')]
class UserFileResource extends Resource implements HasUriTemplate
{
    /**
     * 리소스의 URI 템플릿 반환.
     */
    public function uriTemplate(): UriTemplate
    {
        return new UriTemplate('file://users/{userId}/files/{fileId}');
    }

    /**
     * 리소스 요청을 처리합니다.
     */
    public function handle(Request $request): Response
    {
        $userId = $request->get('userId');
        $fileId = $request->get('fileId');

        // 파일 내용 조회 및 반환...

        return Response::text($content);
    }
}
```

템플릿에 맞는 URI로 요청이 오면, 변수값이 자동 추출되어 `handle`의 Request에서 바로 사용할 수 있습니다.

#### URI 템플릿 문법

URI 템플릿에는 중괄호({})로 감싼 변수를 사용합니다:

```php
new UriTemplate('file://users/{userId}');
new UriTemplate('file://users/{userId}/files/{fileId}');
new UriTemplate('https://api.example.com/{version}/{resource}/{id}');
```

#### 템플릿 변수 접근

요청 URI에서 추출된 변수는 Request의 `get` 메서드로 접근할 수 있습니다:

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
        // 추출된 변수 사용
        $userId = $request->get('userId');

        // 전체 URI 접근
        $uri = $request->uri();

        // 유저 프로필 조회...

        return Response::text("Profile for user {$userId}");
    }
}
```

Request 객체를 통해 변수 및 요청 URI 모두 쉽게 사용할 수 있습니다.

<a name="resource-uri-and-mime-type"></a>
### 리소스 URI 및 MIME 타입

각 리소스는 고유한 URI와 MIME 타입을 가집니다. 기본적으로 클래스명 기반의 URI(`weather://resources/weather-guidelines`)와 `text/plain` MIME 타입이 사용됩니다.

직접 지정하려면 `Uri`, `MimeType` 어트리뷰트 사용:

```php
<?php

namespace App\Mcp\Resources;

use Laravel\Mcp\Server\Attributes\MimeType;
use Laravel\Mcp\Server\Attributes\Uri;
use Laravel\Mcp\Server\Resource;

#[Uri('weather://resources/guidelines')]
#[MimeType('application/pdf')]
class WeatherGuidelinesResource extends Resource
{
}
```

URI와 MIME 타입은 AI 클라이언트가 리소스 콘텐츠 형식을 판별하는 데 활용됩니다.

<a name="resource-request"></a>
### 리소스 요청

툴이나 프롬프트와 달리, 리소스는 입력 스키마나 인수를 정의할 수 없습니다. 그러나 `handle` 메서드 내에서 `Request` 객체를 자유롭게 활용할 수 있습니다:

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

리소스 역시 확장된 [서비스 컨테이너](/docs/12.x/container)를 통해 생성되므로, 생성자나 `handle` 메서드에서 타입힌트로 의존성을 선언하면 자동 주입됩니다:

```php
<?php

namespace App\Mcp\Resources;

use App\Repositories\WeatherRepository;
use Laravel\Mcp\Server\Resource;

class WeatherGuidelinesResource extends Resource
{
    /**
     * 새로운 리소스 인스턴스 생성.
     */
    public function __construct(
        protected WeatherRepository $weather,
    ) {}

    // ...
}
```

또는 handle 메서드에서 의존성 주입:

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
### 리소스 주석

리소스에도 [주석(annotation)](https://modelcontextprotocol.io/specification/2025-06-18/schema#resourceannotations)을 추가해 AI 클라이언트로 추가 정보를 제공할 수 있습니다. 어트리뷰트를 사용해 주석을 추가하세요:

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

사용 가능한 주석과 설명:

| 주석(Annotation)     | 타입              | 설명                                                                      |
| ------------------- | ---------------- | ------------------------------------------------------------------------- |
| `#[Audience]`       | Role/Role[]      | 대상 청중 지정(`Role::User`, `Role::Assistant` 또는 둘 다)                  |
| `#[Priority]`       | float            | 0.0~1.0 사이의 점수로 리소스 중요도 표시                                  |
| `#[LastModified]`   | string           | ISO 8601 형식의 리소스 최종 수정 시각                                      |

<a name="conditional-resource-registration"></a>
### 조건부 리소스 등록

리소스 클래스에서 `shouldRegister` 메서드를 구현하여 노출 여부를 동적으로 결정할 수 있습니다:

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

이 메서드가 `false`를 반환하면 해당 리소스는 AI 클라이언트에 노출되지 않습니다.

<a name="resource-responses"></a>
### 리소스 응답

리소스는 반드시 `Laravel\Mcp\Response` 인스턴스를 반환해야 합니다. Response 클래스는 여러 응답 타입 생성을 지원합니다.

단순 텍스트 반환:

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

Blob(바이너리 데이터) 콘텐츠 반환에는 `blob` 메서드 사용:

```php
return Response::blob(file_get_contents(storage_path('weather/radar.png')));
```

이 경우 MIME 타입은 리소스의 설정에 따릅니다:

```php
<?php

namespace App\Mcp\Resources;

use Laravel\Mcp\Server\Attributes\MimeType;
use Laravel\Mcp\Server\Resource;

#[MimeType('image/png')]
class WeatherGuidelinesResource extends Resource
{
    //
}
```

#### 오류 응답

리소스 조회 오류 상황에서는 `error()` 메서드를 사용하세요:

```php
return Response::error('Unable to fetch weather data for the specified location.');
```

<a name="metadata"></a>
## 메타데이터

Laravel MCP는 [MCP 명세](https://modelcontextprotocol.io/specification/2025-06-18/basic#meta)의 `_meta` 필드를 지원합니다. 이는 MCP 클라이언트 또는 연동의 요구에 따라 필수일 수 있습니다. 메타데이터는 MCP의 모든 기본 요소(툴, 리소스, 프롬프트 및 각 응답)에 적용할 수 있습니다.

개별 응답에 메타데이터를 부여하려면 `withMeta` 메서드를 사용하세요:

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

전체 응답(envelope)에 메타데이터를 추가하려면, `Response::make`로 감싸고 `withMeta`를 호출하세요:

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

개별 툴, 리소스, 프롬프트 자체에 메타데이터를 부여하려면 클래스의 `$meta` 속성을 선언하면 됩니다:

```php
use Laravel\Mcp\Server\Attributes\Description;
use Laravel\Mcp\Server\Tool;

#[Description('Fetches the current weather forecast.')]
class CurrentWeatherTool extends Tool
{
    protected ?array $meta = [
        'version' => '2.0',
        'author' => 'Weather Team',
    ];

    // ...
}
```

<a name="authentication"></a>
## 인증(Authentication)

일반 라우트처럼, MCP 웹 서버에도 미들웨어를 활용하여 인증 기능을 추가할 수 있습니다. 인증이 적용된 MCP 서버는 서버의 모든 기능 사용 시 인증된 사용자만 접근할 수 있습니다.

인증 방식은 두 가지입니다. [Laravel Sanctum](/docs/12.x/sanctum)을 이용한 간단한 토큰 기반 인증 또는  `Authorization` HTTP 헤더를 직접 사용하는 방식, 그리고 [Laravel Passport](/docs/12.x/passport) 기반의 OAuth 인증입니다.

<a name="oauth"></a>
### OAuth 2.1

가장 강력한 웹 MCP 서버 보호 방식은 [Laravel Passport](/docs/12.x/passport)를 이용한 OAuth 인증입니다.

OAuth로 MCP 서버를 보호하려면, `routes/ai.php` 파일에서 `Mcp::oauthRoutes`를 호출해 필요한 OAuth2 디스커버리 라우트를 등록합니다. 이후, 서버 등록 라우트에 Passport의 `auth:api` 미들웨어를 반드시 적용하세요:

```php
use App\Mcp\Servers\WeatherExample;
use Laravel\Mcp\Facades\Mcp;

Mcp::oauthRoutes();

Mcp::web('/mcp/weather', WeatherExample::class)
    ->middleware('auth:api');
```

#### 새 Passport 설치

프로젝트에 Passport가 없다면 [Passport 설치 가이드](/docs/12.x/passport#installation)를 따라 설치하십시오.

다음으로, MCP에서 제공하는 Passport 인증 뷰를 퍼블리시합니다:

```shell
php artisan vendor:publish --tag=mcp-views
```

그리고 `AppServiceProvider`의 `boot` 메서드에서 Passport에 해당 뷰를 적용하도록 합니다:

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

이 뷰는 사용자에게 AI 에이전트의 접근 시 인증 허용/거부 인터페이스를 보여줍니다.

> [!NOTE]
> 이 방식에서는 OAuth를 실제 인증 가능한 모델로의 변환(transalation)에 이용하며, 스코프 등 OAuth의 복잡한 부분은 무시합니다.

#### 기존 Passport 연동

이미 Passport가 설치되어 있다면, MCP도 별다른 추가 설정 없이 연동 가능합니다. 현재 OAuth 스코프 커스터마이징은 지원하지 않으며, MCP에서는 항상 `mcp:use` 스코프만을 사용합니다.

#### Passport vs Sanctum

Model Context Protocol 명세에는 OAuth2.1이 공식으로 기술되어 있으며, 많은 MCP 클라이언트가 이를 기본으로 지원합니다. 따라서 가능하면 Passport 사용을 권장합니다.

이미 [Sanctum](/docs/12.x/sanctum)을 사용하는 프로젝트라면 굳이 Passport를 추가할 필요 없이 자체적으로 인증 미들웨어만 적용해도 무방합니다.

<a name="sanctum"></a>
### Sanctum

[Sanctum](/docs/12.x/sanctum)을 이용해 MCP 서버를 보호하려면, `routes/ai.php`에서 서버에 Sanctum 인증 미들웨어를 적용하세요. MCP 클라이언트는 반드시 `Authorization: Bearer <token>` 헤더를 전송해야 합니다.

```php
use App\Mcp\Servers\WeatherExample;
use Laravel\Mcp\Facades\Mcp;

Mcp::web('/mcp/demo', WeatherExample::class)
    ->middleware('auth:sanctum');
```

#### 커스텀 MCP 인증

애플리케이션이 별도의 API 토큰 인증을 갖춘 경우, MCP 서버에 원하는 미들웨어를 지정할 수 있습니다. 직접 `Authorization` 헤더를 검사하는 미들웨어로 구현 가능합니다.

<a name="authorization"></a>
## 인가(Authorization)

현재 인증된 사용자는 `$request->user()`로 접근할 수 있으며, MCP의 툴/리소스 내부에서 [인가 체크](/docs/12.x/authorization)를 수행할 수 있습니다:

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

MCP 서버는 내장 MCP Inspector 혹은 유닛 테스트로 쉽게 테스트할 수 있습니다.

<a name="mcp-inspector"></a>
### MCP 인스펙터

[MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector)는 MCP 서버를 실시간으로 테스트하고 디버깅할 수 있는 툴입니다. 접속, 인증, 툴/리소스/프롬프트 실행을 모두 지원합니다.

등록된 서버에 대해 다음과 같이 Inspector를 실행할 수 있습니다:

```shell
# 웹 서버용...
php artisan mcp:inspector mcp/weather

# 로컬 서버(weather 명)...
php artisan mcp:inspector weather
```

Inspector 실행 시, MCP 클라이언트에 필요한 환경설정 정보(인증 헤더 등)도 안내해줍니다.

<a name="unit-tests"></a>
### 유닛 테스트

MCP 서버, 툴, 리소스, 프롬프트는 모두 유닛 테스트로 확실히 검증할 수 있습니다.

새 테스트 케이스를 만들고, 테스트할 MCP 엔티티를 직접 실행하면 됩니다. 예를 들어, `WeatherServer`의 툴을 테스트하려면:

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

프롬프트, 리소스도 동일하게 테스트할 수 있습니다:

```php
$response = WeatherServer::prompt(...);
$response = WeatherServer::resource(...);
```

특정 사용자로 인증된 상태에서 테스트하려면 `actingAs` 체이닝을 사용하세요:

```php
$response = WeatherServer::actingAs($user)->tool(...);
```

응답을 받은 후, 다양한 assertion 메서드로 결과와 상태를 검증할 수 있습니다.

- 응답 성공 여부는 `assertOk`로 판단:

```php
$response->assertOk();
```

- 특정 텍스트 포함 여부 확인은 `assertSee`:

```php
$response->assertSee('The current weather in New York City is 72°F and sunny.');
```

- 오류 여부는 `assertHasErrors`, 구체적 메시지는 아래와 같이:

```php
$response->assertHasErrors();

$response->assertHasErrors([
    'Something went wrong.',
]);
```

- 오류가 없는지 확인하려면 `assertHasNoErrors` 사용:

```php
$response->assertHasNoErrors();
```

- 메타데이터에 대한 검사도 지원합니다: `assertName()`, `assertTitle()`, `assertDescription()` 등

```php
$response->assertName('current-weather');
$response->assertTitle('Current Weather Tool');
$response->assertDescription('Fetches the current weather forecast for a specified location.');
```

- 노티피케이션 전송 여부도 검증할 수 있습니다:

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

- 응답의 원시 content를 확인하려면 `dd` 또는 `dump` 메서드를 활용하세요:

```php
$response->dd();
$response->dump();
```