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
    - [리소스 템플릿](#resource-templates)
    - [리소스 URI 및 MIME 타입](#resource-uri-and-mime-type)
    - [리소스 요청](#resource-request)
    - [리소스 의존성 주입](#resource-dependency-injection)
    - [리소스 애노테이션](#resource-annotations)
    - [조건부 리소스 등록](#conditional-resource-registration)
    - [리소스 응답](#resource-responses)
- [메타데이터](#metadata)
- [인증](#authentication)
    - [OAuth 2.1](#oauth)
    - [Sanctum](#sanctum)
- [인가](#authorization)
- [서버 테스트](#testing-servers)
    - [MCP 인스펙터](#mcp-inspector)
    - [유닛 테스트](#unit-tests)

<a name="introduction"></a>
## 소개

[Laravel MCP](https://github.com/laravel/mcp)는 [Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro)을 통해 AI 클라이언트가 여러분의 Laravel 애플리케이션과 상호작용할 수 있게 해주는 간단하고 우아한 방식을 제공합니다. 서버, 툴, 리소스, 프롬프트 등 MCP 기능을 명확하고 유연하게 정의할 수 있어, 애플리케이션에 AI 기반 상호작용을 손쉽게 도입할 수 있습니다.

<a name="installation"></a>
## 설치

먼저, Composer 패키지 관리자를 사용하여 프로젝트에 Laravel MCP를 설치합니다:

```shell
composer require laravel/mcp
```

<a name="publishing-routes"></a>
### 라우트 퍼블리싱

Laravel MCP를 설치한 후, MCP 서버를 정의할 `routes/ai.php` 파일을 퍼블리시하려면 `vendor:publish` Artisan 명령어를 실행하세요:

```shell
php artisan vendor:publish --tag=ai-routes
```

이 명령어는 애플리케이션의 `routes` 디렉터리에 `routes/ai.php` 파일을 생성합니다. 이 파일에서 MCP 서버를 등록하게 됩니다.

<a name="creating-servers"></a>
## 서버 생성

`make:mcp-server` Artisan 명령어를 사용해 MCP 서버를 생성할 수 있습니다. 서버는 툴, 리소스, 프롬프트 등 MCP 기능을 AI 클라이언트에게 노출하는 중심 통신 지점 역할을 합니다:

```shell
php artisan make:mcp-server WeatherServer
```

이 명령어는 `app/Mcp/Servers` 디렉터리에 새로운 서버 클래스를 생성합니다. 생성된 서버 클래스는 기본 `Laravel\Mcp\Server` 클래스를 확장하며, 여기에 MCP 서버의 이름, 버전, LLM 지침, 그리고 툴·리소스·프롬프트 등록을 위한 속성을 정의할 수 있습니다:

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
     * LLM을 위한 MCP 서버 사용 지침.
     */
    protected string $instructions = 'This server provides weather information and forecasts.';

    /**
     * MCP 서버에 등록된 툴 목록.
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Tool>>
     */
    protected array $tools = [
        // GetCurrentWeatherTool::class,
    ];

    /**
     * MCP 서버에 등록된 리소스 목록.
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Resource>>
     */
    protected array $resources = [
        // WeatherGuidelinesResource::class,
    ];

    /**
     * MCP 서버에 등록된 프롬프트 목록.
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

서버를 생성한 뒤에는 `routes/ai.php` 파일에 서버를 등록하여 외부에서 접근할 수 있게 해야 합니다. 서버 등록 방식은 HTTP로 접근 가능한 `web` 방식과, 콘솔에서 사용할 수 있는 `local` 방식 두 가지가 있습니다.

<a name="web-servers"></a>
### 웹 서버

웹 서버는 HTTP POST 요청을 통해 접근할 수 있는 가장 일반적인 형태로, 원격 AI 클라이언트나 웹 기반 통합에 적합합니다. `web` 메서드를 사용하여 웹 서버를 등록하세요:

```php
use App\Mcp\Servers\WeatherServer;
use Laravel\Mcp\Facades\Mcp;

Mcp::web('/mcp/weather', WeatherServer::class);
```

일반 라우트와 마찬가지로, 미들웨어를 적용해서 웹 서버를 보호할 수도 있습니다:

```php
Mcp::web('/mcp/weather', WeatherServer::class)
    ->middleware(['throttle:mcp']);
```

<a name="local-servers"></a>
### 로컬 서버

로컬 서버는 Artisan 명령어로 동작하며, [Laravel Boost](/docs/12.x/installation#installing-laravel-boost)와 같은 로컬 AI 어시스턴트 통합에 적합합니다. `local` 메서드를 사용하여 로컬 서버를 등록합니다:

```php
use App\Mcp\Servers\WeatherServer;
use Laravel\Mcp\Facades\Mcp;

Mcp::local('weather', WeatherServer::class);
```

로컬 서버를 등록한 후에는 일반적으로 직접 `mcp:start` Artisan 명령어를 실행할 필요가 없습니다. MCP 클라이언트(AI 에이전트)가 서버를 직접 실행하도록 하거나, [MCP 인스펙터](#mcp-inspector)를 사용할 수 있습니다.

<a name="tools"></a>
## 툴

툴을 통해 서버에서 AI 클라이언트가 호출할 수 있는 기능을 제공할 수 있습니다. 툴은 언어 모델이 실제 작업을 수행하거나, 코드를 실행하거나, 외부 시스템과 연동할 수 있게 해줍니다:

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
     * 툴의 설명입니다.
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
     * @return array<string, \Illuminate\JsonSchema\Type\Type>
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

`make:mcp-tool` Artisan 명령어로 새로운 MCP 툴 클래스를 생성할 수 있습니다:

```shell
php artisan make:mcp-tool CurrentWeatherTool
```

툴을 생성한 후에는, 서버의 `$tools` 속성에 툴 클래스를 등록하세요:

```php
<?php

namespace App\Mcp\Servers;

use App\Mcp\Tools\CurrentWeatherTool;
use Laravel\Mcp\Server;

class WeatherServer extends Server
{
    /**
     * MCP 서버에 등록할 툴 목록.
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Tool>>
     */
    protected array $tools = [
        CurrentWeatherTool::class,
    ];
}
```

#### 툴 이름, 제목, 설명

기본적으로 툴의 이름(name)과 제목(title)은 클래스명에서 자동으로 생성됩니다. 예를 들어, `CurrentWeatherTool`의 이름은 `current-weather`이고 제목은 `Current Weather Tool`이 됩니다. `$name`, `$title` 속성을 정의하여 직접 지정할 수도 있습니다:

```php
class CurrentWeatherTool extends Tool
{
    /**
     * 툴의 이름입니다.
     */
    protected string $name = 'get-optimistic-weather';

    /**
     * 툴의 제목입니다.
     */
    protected string $title = 'Get Optimistic Weather Forecast';

    // ...
}
```

툴의 설명(description)은 자동 생성되지 않으므로, 반드시 의미 있는 설명을 `$description` 속성으로 정의해주어야 합니다:

```php
class CurrentWeatherTool extends Tool
{
    /**
     * 툴의 설명입니다.
     */
    protected string $description = 'Fetches the current weather forecast for a specified location.';

    //
}
```

> [!NOTE]
> 설명(description)은 툴의 메타데이터에서 매우 중요한 요소입니다. AI 모델이 해당 툴을 언제, 어떻게 활용할 수 있는지 이해하는 데 설명이 핵심 역할을 합니다.

<a name="tool-input-schemas"></a>
### 툴 입력 스키마

툴은 AI 클라이언트가 전달하는 인수(파라미터)를 명확하게 정의하기 위해 입력 스키마(input schema)를 만들 수 있습니다. 이는 Laravel의 `Illuminate\Contracts\JsonSchema\JsonSchema` 빌더를 활용하여 작성합니다:

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

툴의 응답 데이터 구조를 명확하게 정의하고 싶다면, [출력 스키마](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#output-schema)를 사용할 수 있습니다. 이는 AI 클라이언트가 응답을 구조적으로 파싱하는 데 도움을 줍니다. `outputSchema` 메서드를 통해 정의하세요:

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

JSON 스키마는 툴 인수의 기본 구조만 검증할 수 있습니다. 보다 복잡한 유효성 검사 규칙이 필요할 경우, Laravel MCP는 Laravel의 [유효성 검증 기능](/docs/12.x/validation)과 완벽하게 연동됩니다. `handle` 메서드 내에서 `$request->validate()`로 추가 검증을 할 수 있습니다:

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

        // 검증된 인수를 사용하여 날씨 데이터를 조회...
    }
}
```

유효성 검사 실패시, AI 클라이언트는 여러분이 제공하는 오류 메시지에 따라 동작합니다. 따라서, 이해하기 쉽고 명확한 오류 메시지를 작성하는 것이 매우 중요합니다:

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

모든 MCP 툴 클래스는 Laravel의 [서비스 컨테이너](/docs/12.x/container)를 통해 로드됩니다. 따라서 툴이 의존하는 객체(서비스, 리포지토리 등)를 생성자에서 타입힌트로 선언하면, 자동으로 인스턴스가 주입됩니다:

```php
<?php

namespace App\Mcp\Tools;

use App\Repositories\WeatherRepository;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * 새 툴 인스턴스 생성.
     */
    public function __construct(
        protected WeatherRepository $weather,
    ) {}

    // ...
}
```

생성자 뿐만 아니라, 툴의 `handle()` 메서드에서도 의존 객체를 타입힌트로 명시할 수 있습니다. 서비스 컨테이너는 메서드 호출 시 알아서 주입해줍니다:

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

툴에 [애노테이션](https://modelcontextprotocol.io/specification/2025-06-18/schema#toolannotations)을 부여하여 AI 클라이언트에 추가 메타데이터를 전달할 수 있습니다. 애노테이션은 AI 모델이 툴의 특성을 더 잘 이해하는 데 도움이 됩니다. 클래스 위에 속성 형태로 적용합니다:

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

| 애노테이션              | 타입     | 설명                                                                          |
| ------------------ | ------- | -------------------------------------------------------------------------- |
| `#[IsReadOnly]`    | boolean | 툴이 환경에 변화를 주지 않음을 나타냅니다.                                   |
| `#[IsDestructive]` | boolean | 툴이 파괴적 업데이트를 수행할 수 있음을 나타냅니다(읽기 전용이 아닌 경우에만 의미 있음).|
| `#[IsIdempotent]`  | boolean | 같은 인수로 반복 호출 시 추가적인 효과가 없음을 나타냅니다(읽기 전용이 아닌 경우).  |
| `#[IsOpenWorld]`   | boolean | 툴이 외부 엔티티와 상호작용할 가능성이 있음을 나타냅니다.                       |

애노테이션은 인자를 통해 명시적으로 값을 지정할 수 있습니다:

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

툴 클래스에서 `shouldRegister` 메서드를 구현하면, 애플리케이션 상태, 설정, 요청 파라미터 등에 따라 런타임 시 툴의 등록 여부를 동적으로 판단할 수 있습니다:

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

`shouldRegister`가 `false`를 반환하면 해당 툴은 사용 가능한 목록에 나타나지 않고, AI 클라이언트가 호출할 수도 없습니다.

<a name="tool-responses"></a>
### 툴 응답

툴은 반드시 `Laravel\Mcp\Response` 인스턴스를 반환해야 합니다. Response 클래스는 여러 종류의 응답을 손쉽게 생성할 수 있도록 다양한 메서드를 제공합니다.

간단한 텍스트 응답은 `text` 메서드를 사용합니다:

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

툴 실행 도중 오류가 발생했음을 나타내려면 `error` 메서드를 사용하세요:

```php
return Response::error('Unable to fetch weather data. Please try again.');
```

#### 여러 응답 콘텐츠 반환

여러 개의 응답 콘텐츠를 반환해야 할 경우, `Response` 인스턴스의 배열을 반환할 수 있습니다:

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

툴이 [구조화된 콘텐츠](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#structured-content)가 필요한 경우, `structured` 메서드를 사용하여 파싱 가능한 데이터를 AI 클라이언트에 제공합니다. 이 응답은 기존의 JSON 문자열도 제공합니다:

```php
return Response::structured([
    'temperature' => 22.5,
    'conditions' => 'Partly cloudy',
    'humidity' => 65,
]);
```

구조화된 콘텐츠와 텍스트 설명을 함께 제공하려면 `withStructuredContent`를 활용하세요:

```php
return Response::make(
    Response::text('Weather is 22.5°C and sunny')
)->withStructuredContent([
    'temperature' => 22.5,
    'conditions' => 'Sunny',
]);
```

#### 스트리밍 응답

실행 시간이 긴 작업이나 실시간 데이터 스트리밍이 필요한 경우, `handle` 메서드에서 [generator](https://www.php.net/manual/en/language.generators.overview.php)를 반환하면 됩니다. 이 방식은 중간 처리 결과를 단계별로 클라이언트에 스트리밍 전송할 수 있게 해줍니다:

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

웹 기반 서버에서 스트리밍 응답을 사용할 경우, 자동으로 SSE(Server-Sent Events) 스트림이 열려 각 메시지가 이벤트로 전송됩니다.

<a name="prompts"></a>
## 프롬프트

[프롬프트](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts)는 서버에서 AI 클라이언트가 언어 모델과 상호작용할 때 활용할 수 있는 재사용 가능한 프롬프트 템플릿을 제공하는 기능입니다. 이를 통해 흔히 반복되는 질문이나 상호작용을 표준화하여 구조적으로 사용할 수 있습니다.

<a name="creating-prompts"></a>
### 프롬프트 생성

`make:mcp-prompt` Artisan 명령어로 프롬프트 클래스를 생성할 수 있습니다:

```shell
php artisan make:mcp-prompt DescribeWeatherPrompt
```

프롬프트를 생성한 후에는, 서버의 `$prompts` 속성에 프롬프트 클래스를 등록하세요:

```php
<?php

namespace App\Mcp\Servers;

use App\Mcp\Prompts\DescribeWeatherPrompt;
use Laravel\Mcp\Server;

class WeatherServer extends Server
{
    /**
     * MCP 서버에 등록할 프롬프트 목록.
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Prompt>>
     */
    protected array $prompts = [
        DescribeWeatherPrompt::class,
    ];
}
```

#### 프롬프트 이름, 제목, 설명

프롬프트의 이름(name)과 제목(title)은 기본적으로 클래스명에서 유추되어 생성됩니다. 예를 들어, `DescribeWeatherPrompt`는 이름이 `describe-weather`, 제목이 `Describe Weather Prompt`가 됩니다. 필요에 따라 `$name`, `$title` 속성으로 직접 지정할 수 있습니다:

```php
class DescribeWeatherPrompt extends Prompt
{
    /**
     * 프롬프트의 이름입니다.
     */
    protected string $name = 'weather-assistant';

    /**
     * 프롬프트의 제목입니다.
     */
    protected string $title = 'Weather Assistant Prompt';

    // ...
}
```

프롬프트의 설명(description) 역시 자동으로 생성되지 않습니다. 반드시 의미 있는 설명을 `$description` 속성에 정의하세요:

```php
class DescribeWeatherPrompt extends Prompt
{
    /**
     * 프롬프트의 설명입니다.
     */
    protected string $description = 'Generates a natural-language explanation of the weather for a given location.';

    //
}
```

> [!NOTE]
> 프롬프트 설명(description)은 AI 모델이 해당 프롬프트를 언제, 어떻게 활용할 수 있는지 판단하는 데 매우 중요합니다.

<a name="prompt-arguments"></a>
### 프롬프트 인수

프롬프트는 AI 클라이언트가 지정값을 넘겨 템플릿을 더욱 유연하게 사용할 수 있도록 인수를 정의할 수 있습니다. `arguments` 메서드를 통해 어떤 인수를 받는지 명시하세요:

```php
<?php

namespace App\Mcp\Prompts;

use Laravel\Mcp\Server\Prompt;
use Laravel\Mcp\Server\Prompts\Argument;

class DescribeWeatherPrompt extends Prompt
{
    /**
     * 프롬프트가 받을 인수 반환.
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

프롬프트 인수는 정의에 따라 기본적인 검증이 자동으로 진행됩니다. 필요하다면 복잡한 유효성 검증도 가능하며, MCP는 Laravel의 [유효성 검증 기능](/docs/12.x/validation)과 완벽하게 연동됩니다. `handle` 메서드 내에서 `$request->validate()`를 이용하세요:

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

        // tone에 따른 설명 생성...
    }
}
```

마찬가지로, 유효성 검사 실패시 AI 클라이언트가 이해하기 쉽고 명확한 오류 메시지를 작성하는 것이 중요합니다:

```php
$validated = $request->validate([
    'tone' => ['required','string','max:50'],
],[
    'tone.*' => 'You must specify a tone for the weather description. Examples include "formal", "casual", or "humorous".',
]);
```

<a name="prompt-dependency-injection"></a>
### 프롬프트 의존성 주입

모든 MCP 프롬프트 클래스는 Laravel [서비스 컨테이너](/docs/12.x/container)로부터 주입됩니다. 따라서 생성자에서 타입힌트로 의존성을 선언하면 자동으로 주입됩니다:

```php
<?php

namespace App\Mcp\Prompts;

use App\Repositories\WeatherRepository;
use Laravel\Mcp\Server\Prompt;

class DescribeWeatherPrompt extends Prompt
{
    /**
     * 새 프롬프트 인스턴스 생성.
     */
    public function __construct(
        protected WeatherRepository $weather,
    ) {}

    //
}
```

생성자 외에도, 프롬프트의 `handle` 메서드에서도 타입힌트를 사용할 수 있습니다:

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

프롬프트 클래스에서 `shouldRegister` 메서드를 구현하면, 애플리케이션의 상태, 설정, 요청 정보 등을 바탕으로 동적으로 등록 여부를 결정할 수 있습니다:

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

`shouldRegister`가 `false`를 반환하면 해당 프롬프트는 AI 클라이언트가 사용할 수 없습니다.

<a name="prompt-responses"></a>
### 프롬프트 응답

프롬프트는 `Laravel\Mcp\Response` 인스턴스 한 개 또는 여러 개(이터러블 형태)로 응답할 수 있습니다. 이 응답 객체들은 AI 클라이언트에 전송될 내용을 캡슐화합니다:

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

`asAssistant()` 메서드를 사용하면, 해당 응답 메시지가 AI 어시스턴트가 보낸 메시지로 처리됩니다. 일반 응답은 사용자 입력으로 간주됩니다.

<a name="resources"></a>
## 리소스

[리소스](https://modelcontextprotocol.io/specification/2025-06-18/server/resources)는 서버가 AI 클라이언트에게 문서, 구성, 데이터 등 다양한 정보를 공유하여, 언어 모델이 더 나은 응답을 생성하도록 컨텍스트를 제공하는 수단입니다. 정적 또는 동적 데이터 모두 노출할 수 있습니다.

<a name="creating-resources"></a>
## 리소스 생성

`make:mcp-resource` Artisan 명령어로 MCP 리소스 클래스를 생성할 수 있습니다:

```shell
php artisan make:mcp-resource WeatherGuidelinesResource
```

리소스를 생성한 후에는 서버의 `$resources` 속성에 등록하세요:

```php
<?php

namespace App\Mcp\Servers;

use App\Mcp\Resources\WeatherGuidelinesResource;
use Laravel\Mcp\Server;

class WeatherServer extends Server
{
    /**
     * MCP 서버에 등록할 리소스 목록.
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Resource>>
     */
    protected array $resources = [
        WeatherGuidelinesResource::class,
    ];
}
```

#### 리소스 이름, 제목, 설명

리소스의 이름(name)과 제목(title)은 기본적으로 클래스명에서 유추되어 자동으로 생성됩니다. 예를 들어, `WeatherGuidelinesResource`는 이름이 `weather-guidelines`, 제목이 `Weather Guidelines Resource`가 됩니다. `$name`, `$title`로 직접 지정할 수 있습니다:

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

마찬가지로, 리소스 설명(description)은 자동 생성되지 않으므로, 의미 있는 설명을 `$description`에 정의하세요:

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
> 설명(description)은 리소스의 메타데이터에서 매우 중요한 부분입니다. AI 모델이 언제, 어떻게 리소스를 활용해야 할지 이해하는 데에 큰 역할을 합니다.

<a name="resource-templates"></a>
### 리소스 템플릿

[리소스 템플릿](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#resource-templates)을 사용하면, 고정된 URI 대신 변수 패턴을 포함한 URI와 매칭되는 동적 리소스를 한 번에 정의할 수 있습니다.

#### 리소스 템플릿 생성

리소스 템플릿을 생성하려면, 리소스 클래스에서 `HasUriTemplate` 인터페이스를 구현하고, `uriTemplate` 메서드를 정의하여 `UriTemplate` 인스턴스를 반환하세요:

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
     * 리소스 설명.
     */
    protected string $description = 'Access user files by ID';

    /**
     * 리소스 MIME 타입.
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

        // 파일 내용 조회 및 반환...

        return Response::text($content);
    }
}
```

`HasUriTemplate` 인터페이스를 구현하면, 해당 리소스는 고정 리소스가 아닌 리소스 템플릿으로 등록됩니다. 클라이언트가 템플릿 패턴과 매칭되는 URI로 요청하면, 변수들이 자동 추출되어 `handle` 메서드에서 사용할 수 있습니다.

#### URI 템플릿 문법

URI 템플릿은 중괄호 `{}`를 사용해 변수 세그먼트를 정의합니다:

```php
new UriTemplate('file://users/{userId}');
new UriTemplate('file://users/{userId}/files/{fileId}');
new UriTemplate('https://api.example.com/{version}/{resource}/{id}');
```

#### 템플릿 변수 접근

해당 URI가 리소스 템플릿과 매칭되면, 추출된 변수들은 request의 `get` 메서드로 접근할 수 있습니다:

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

        // 전체 URI가 필요하다면
        $uri = $request->uri();

        // 사용자 프로필 조회...

        return Response::text("Profile for user {$userId}");
    }
}
```

Request 객체를 통해 추출된 변수들과, 원래 요청된 URI 모두 사용할 수 있습니다.

<a name="resource-uri-and-mime-type"></a>
### 리소스 URI 및 MIME 타입

각 리소스는 고유 URI와 MIME 타입을 가지며, 이는 AI 클라이언트가 리소스 포맷을 이해하는 데 도움을 줍니다.

기본적으로 URI는 리소스의 이름을 기준으로 자동 생성되며, 예를 들어 `WeatherGuidelinesResource`의 URI는 `weather://resources/weather-guidelines`가 됩니다. 기본 MIME 타입은 `text/plain`입니다.

필요하다면, `$uri`와 `$mimeType` 속성을 정의하여 값을 직접 설정할 수도 있습니다:

```php
<?php

namespace App\Mcp\Resources;

use Laravel\Mcp\Server\Resource;

class WeatherGuidelinesResource extends Resource
{
    /**
     * 리소스 URI.
     */
    protected string $uri = 'weather://resources/guidelines';

    /**
     * 리소스 MIME 타입.
     */
    protected string $mimeType = 'application/pdf';
}
```

URI와 MIME 타입은 AI 클라이언트가 리소스 콘텐츠를 어떻게 해석/처리할지 결정하는 데 중요한 정보입니다.

<a name="resource-request"></a>
### 리소스 요청

툴 및 프롬프트와 달리, 리소스는 입력 스키마나 인수를 정의하지 않습니다. 그러나 `handle` 메서드 내에서 요청 객체(Request)를 사용할 수 있습니다:

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

리소스 클래스 역시 Laravel [서비스 컨테이너](/docs/12.x/container)를 통해 주입됩니다. 생성자 또는 `handle` 메서드에서 타입힌트 선언 시, 자동으로 인스턴스가 주입됩니다:

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

생성자 외에도, `handle` 메서드에서 타입힌트로 의존성을 주입받을 수 있습니다:

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
### 리소스 애노테이션

리소스에도 [애노테이션](https://modelcontextprotocol.io/specification/2025-06-18/schema#resourceannotations)을 적용하여 AI 클라이언트에 추가적인 메타데이터를 제공할 수 있습니다. 속성(Abstract Attribute)으로 적용하세요:

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

사용 가능한 애노테이션 목록:

| 애노테이션        | 타입            | 설명                                                         |
| ----------------- | --------------- | ------------------------------------------------------------ |
| `#[Audience]`     | Role 또는 배열   | 해당 리소스의 대상(`Role::User`, `Role::Assistant` 등)을 지정 |
| `#[Priority]`     | float           | 0.0 ~ 1.0 사이의 수치로 리소스의 중요도                      |
| `#[LastModified]` | string          | ISO 8601 형식의 마지막 수정 일시                             |

<a name="conditional-resource-registration"></a>
### 조건부 리소스 등록

리소스 클래스에서 `shouldRegister` 메서드를 구현하면, 설정, 요청, 애플리케이션 상태에 따라 리소스를 런타임에 등록할지 동적으로 결정할 수 있습니다:

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

`shouldRegister`가 `false`를 반환하면 해당 리소스는 AI 클라이언트가 접근할 수 없습니다.

<a name="resource-responses"></a>
### 리소스 응답

리소스 역시 `Laravel\Mcp\Response` 인스턴스를 반환해야 하며, 여러 편리한 응답 메서드를 제공합니다.

일반적인 텍스트 데이터는 `text` 메서드를 사용하여 반환하세요:

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

바이너리 데이터(이미지, PDF 등)를 반환하려면 `blob` 메서드로 데이터를 넘겨주면 됩니다:

```php
return Response::blob(file_get_contents(storage_path('weather/radar.png')));
```

이 때 응답의 MIME 타입은 리소스 클래스의 `$mimeType` 속성값에 따라 결정됩니다:

```php
<?php

namespace App\Mcp\Resources;

use Laravel\Mcp\Server\Resource;

class WeatherGuidelinesResource extends Resource
{
    /**
     * 리소스 MIME 타입.
     */
    protected string $mimeType = 'image/png';

    //
}
```

#### 오류 응답

리소스 조회 등에서 오류가 발생한 경우, `error()` 메서드로 에러 내용을 반환할 수 있습니다:

```php
return Response::error('Unable to fetch weather data for the specified location.');
```

<a name="metadata"></a>
## 메타데이터

Laravel MCP는 [MCP 사양](https://modelcontextprotocol.io/specification/2025-06-18/basic#meta)에서 정의한 `_meta` 필드를 지원합니다. 이는 일부 MCP 클라이언트나 통합환경에서 필수일 수 있습니다. 메타데이터는 툴, 리소스, 프롬프트와 각 응답에 모두 적용할 수 있습니다.

응답별 메타데이터는 `withMeta` 메서드로 부착할 수 있습니다:

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

결과 전체에 적용할 메타데이터는 `Response::make`로 래핑한 뒤 `withMeta`를 호출하면 됩니다:

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

툴, 리소스, 프롬프트 자체에 메타데이터를 적용하려면, 클래스에 `$meta` 속성을 정의하세요:

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
## 인증

라우트와 마찬가지로, 웹 MCP 서버에 미들웨어를 적용하여 인증 처리를 할 수 있습니다. 인증된 사용자만 MCP 서버의 기능을 사용할 수 있도록 설정할 수 있습니다.

MCP 서버 인증 방식은 두 가지가 대표적입니다. [Laravel Sanctum](/docs/12.x/sanctum)을 통한 토큰 기반 인증(Authorization 헤더 사용) 또는 [Laravel Passport](/docs/12.x/passport)를 활용한 OAuth 인증 방식이 있습니다.

<a name="oauth"></a>
### OAuth 2.1

웹 기반 MCP 서버를 가장 견고하게 보호하려면 [Laravel Passport](/docs/12.x/passport)를 통한 OAuth 방식을 사용하세요.

OAuth 방식으로 MCP 서버 인증 시, 먼저 `routes/ai.php`에서 `Mcp::oauthRoutes`를 호출하여 필요한 OAuth2 디스커버리 및 클라이언트 등록 라우트를 추가합니다. 그 후, `Mcp::web` 라우트에 Passport의 `auth:api` 미들웨어를 적용하세요:

```php
use App\Mcp\Servers\WeatherExample;
use Laravel\Mcp\Facades\Mcp;

Mcp::oauthRoutes();

Mcp::web('/mcp/weather', WeatherExample::class)
    ->middleware('auth:api');
```

#### Passport 신규 설치

애플리케이션에 Laravel Passport가 설치되어 있지 않다면, [Passport 설치 및 배포 가이드](/docs/12.x/passport#installation)를 참고하여 모델 구현, 가드 설정, 키 발급 등을 진행하세요.

이후, Laravel MCP가 제공하는 Passport 인증 뷰를 퍼블리시합니다:

```shell
php artisan vendor:publish --tag=mcp-views
```

그리고 `AppServiceProvider`의 `boot` 메서드에서 `Passport::authorizationView`를 사용해 MCP의 인증 뷰를 지정해야 합니다:

```php
use Laravel\Passport\Passport;

/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Passport::authorizationView(function ($parameters) {
        return view('mcp.authorize', $parameters);
    });
}
```

이 뷰는 인증 시점에 최종 사용자에게 AI 에이전트의 인증 요청을 승인/거절할 수 있게 보여주는 화면입니다.

![Authorization screen example](data:image/png;base64,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)

> [!NOTE]
> 이 단계에서는 실제 OAuth 동작의 일부만 번역 계층으로 사용하며, 스코프 등 OAuth의 모든 요소를 활용하지는 않습니다.

#### 기존 Passport 설치 환경에서 사용

Laravel Passport를 이미 사용 중이라면, MCP 역시 기존 Passport 환경 내에서 정상적으로 동작합니다. 단, 현재(2025년 기준) 커스텀 스코프는 지원되지 않으며, MCP 내부적으로는 인증 가능한 모델 변환만을 목적으로 OAuth를 사용합니다.

`Mcp::oauthRoutes` 호출 시 MCP가 내부적으로 단일 `mcp:use` 스코프만을 추가, 광고, 사용합니다.

#### Passport vs. Sanctum

OAuth2.1은 Model Context Protocol 사양에서 공식적으로 문서화된 인증 방식이며, MCP 클라이언트 중 가장 널리 지원됩니다. 따라서 가능하다면 Passport를 사용하는 것이 권장됩니다.

만약 기존에 [Sanctum](/docs/12.x/sanctum)을 사용하고 있고, Passport 추가가 번거롭다면, 필요에 따라 우선은 Passport 없이 Sanctum만 사용해도 무방합니다. 단, 특정 MCP 클라이언트가 OAuth만 지원한다면 그때 Passport 적용을 추가로 고려하세요.

<a name="sanctum"></a>
### Sanctum

[Sanctum](/docs/12.x/sanctum)으로 MCP 서버를 보호하려면, `routes/ai.php` 파일 내에서 Sanctum 인증 미들웨어를 MCP 서버에 추가하세요. MCP 클라이언트가 `Authorization: Bearer <token>` 헤더를 포함하면 인증이 성공적으로 동작합니다:

```php
use App\Mcp\Servers\WeatherExample;
use Laravel\Mcp\Facades\Mcp;

Mcp::web('/mcp/demo', WeatherExample::class)
    ->middleware('auth:sanctum');
```

#### 커스텀 MCP 인증

애플리케이션이 자체 커스텀 API 토큰 방식을 사용하는 경우에도, MCP 서버 라우트에 원하는 미들웨어를 할당하여 인증 처리를 구현할 수 있습니다. 커스텀 미들웨어 내에서 직접 `Authorization` 헤더 값을 파싱하여 인증 로직을 작성하실 수 있습니다.

<a name="authorization"></a>
## 인가

현재 인증된 사용자는 `$request->user()` 메서드로 접근할 수 있습니다. 이를 활용해 [인가 체크](/docs/12.x/authorization)를 MCP 툴과 리소스에서 수행할 수 있습니다:

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

MCP 서버는 내장 MCP 인스펙터 도구 또는 유닛 테스트를 통해 테스트할 수 있습니다.

<a name="mcp-inspector"></a>
### MCP 인스펙터

[MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector)는 MCP 서버를 테스트하고 디버깅할 수 있는 대화형 도구입니다. 인증 확인, 툴/리소스/프롬프트 호출 등 다양한 테스트 기능을 제공합니다.

등록된 서버에 대해 인스펙터를 실행하려면:

```shell
# 웹 서버...
php artisan mcp:inspector mcp/weather

# "weather"라는 로컬 서버...
php artisan mcp:inspector weather
```

이 명령어는 MCP Inspector를 실행하고, MCP 클라이언트에 복사해서 사용할 수 있는 클라이언트 설정 정보를 제공합니다. 웹 서버가 인증 미들웨어로 보호되는 경우, MCP Inspector에 접속할 때 필요한 헤더(예: Authorization Bearer 토큰 등)를 반드시 제공해야 합니다.

<a name="unit-tests"></a>
### 유닛 테스트

MCP 서버, 툴, 리소스, 프롬프트에 대한 유닛 테스트도 작성할 수 있습니다.

먼저 새 테스트 케이스를 만들고, 해당 MCP 서버의 프리미티브(Primitive)를 호출하세요. 예를 들어, `WeatherServer`의 툴을 테스트하는 코드는 다음과 같습니다:

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

프롬프트와 리소스도 아래와 같이 테스트할 수 있습니다:

```php
$response = WeatherServer::prompt(...);
$response = WeatherServer::resource(...);
```

테스트 전 `actingAs`를 체이닝해 인증된 사용자의 역할로 MCP 프리미티브를 호출할 수도 있습니다:

```php
$response = WeatherServer::actingAs($user)->tool(...);
```

응답을 받은 후에는 다양한 assertion 메서드로 응답의 내용과 상태를 검증할 수 있습니다.

응답이 성공적인지를 확인하려면 `assertOk`를, 특정 텍스트가 포함되어 있는지 확인하려면 `assertSee`를 사용하세요:

```php
$response->assertOk();
$response->assertSee('The current weather in New York City is 72°F and sunny.');
```

응답에 에러가 포함되어 있는 지는 `assertHasErrors`, 없는 지는 `assertHasNoErrors`를 사용해 검증할 수 있습니다:

```php
$response->assertHasErrors();

$response->assertHasErrors([
    'Something went wrong.',
]);
```

응답에 특정 메타데이터가 제대로 포함되어 있는지 검증하려면, `assertName()`, `assertTitle()`, `assertDescription()` 등의 메서드를 사용할 수 있습니다:

```php
$response->assertName('current-weather');
$response->assertTitle('Current Weather Tool');
$response->assertDescription('Fetches the current weather forecast for a specified location.');
```

알림이 정상적으로 발송되었는지는 `assertSentNotification`, `assertNotificationCount` 등을 활용해 검증하세요:

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

마지막으로, 응답의 원시 데이터나 내용을 직접 확인하고 싶다면, `dd`나 `dump` 메서드를 활용하여 디버깅할 수 있습니다:

```php
$response->dd();
$response->dump();
```