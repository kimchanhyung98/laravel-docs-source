# Laravel MCP (Laravel MCP)

- [소개](#introduction)
- [설치](#installation)
    - [라우트 게시](#publishing-routes)
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
    - [툴 어노테이션](#tool-annotations)
    - [툴 조건부 등록](#conditional-tool-registration)
    - [툴 응답](#tool-responses)
- [프롬프트](#prompts)
    - [프롬프트 생성](#creating-prompts)
    - [프롬프트 인수](#prompt-arguments)
    - [프롬프트 인수 유효성 검증](#validating-prompt-arguments)
    - [프롬프트 의존성 주입](#prompt-dependency-injection)
    - [프롬프트 조건부 등록](#conditional-prompt-registration)
    - [프롬프트 응답](#prompt-responses)
- [리소스](#resources)
    - [리소스 생성](#creating-resources)
    - [리소스 템플릿](#resource-templates)
    - [리소스 URI 및 MIME 타입](#resource-uri-and-mime-type)
    - [리소스 요청](#resource-request)
    - [리소스 의존성 주입](#resource-dependency-injection)
    - [리소스 어노테이션](#resource-annotations)
    - [리소스 조건부 등록](#conditional-resource-registration)
    - [리소스 응답](#resource-responses)
- [메타데이터](#metadata)
- [인증](#authentication)
    - [OAuth 2.1](#oauth)
    - [Sanctum](#sanctum)
- [인가](#authorization)
- [서버 테스트](#testing-servers)
    - [MCP 인스펙터](#mcp-inspector)
    - [단위 테스트](#unit-tests)

<a name="introduction"></a>
## 소개

[Laravel MCP](https://github.com/laravel/mcp)는 [Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro)을 통해 AI 클라이언트가 여러분의 Laravel 애플리케이션과 상호작용할 수 있도록 쉽고 우아한 방법을 제공합니다. MCP는 서버, 툴, 리소스, 프롬프트를 정의할 때 사용할 수 있는 직관적이고 유연한 인터페이스를 제공하여, AI 기반 상호작용이 여러분의 애플리케이션에 쉽게 적용될 수 있도록 돕습니다.

<a name="installation"></a>
## 설치

먼저 Composer 패키지 관리자를 사용하여 프로젝트에 Laravel MCP를 설치하세요.

```shell
composer require laravel/mcp
```

<a name="publishing-routes"></a>
### 라우트 게시

Laravel MCP 설치 후, `vendor:publish` 아티즌 명령어를 실행하여 MCP 서버를 정의할 `routes/ai.php` 파일을 게시하세요.

```shell
php artisan vendor:publish --tag=ai-routes
```

이 명령어는 애플리케이션의 `routes` 디렉터리에 `routes/ai.php` 파일을 생성합니다. 이 파일에서 MCP 서버를 등록하게 됩니다.

<a name="creating-servers"></a>
## 서버 생성

`make:mcp-server` 아티즌 명령어를 사용하여 MCP 서버를 생성할 수 있습니다. MCP 서버는 툴, 리소스, 프롬프트 등 MCP의 다양한 기능을 AI 클라이언트에 공개하는 중심 역할을 수행합니다:

```shell
php artisan make:mcp-server WeatherServer
```

이 명령어는 `app/Mcp/Servers` 디렉터리에 새로운 서버 클래스를 생성합니다. 생성된 서버 클래스는 MCP의 기본 `Laravel\Mcp\Server` 클래스를 상속하며, 툴, 리소스, 프롬프트를 등록하는 속성을 제공합니다.

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
     * LLM에게 제공할 MCP 서버의 안내문.
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

서버를 생성하였다면, `routes/ai.php` 파일에서 서버를 등록해야만 접근이 가능해집니다. MCP 서버 등록은 HTTP로 접근할 수 있는 `web` 방식과, 콘솔 환경의 `local` 방식 두 가지로 구분됩니다.

<a name="web-servers"></a>
### 웹 서버

웹 서버는 HTTP POST 요청을 통해 접근할 수 있어 원격 AI 클라이언트, 또는 웹 기반 연동에 가장 일반적으로 사용됩니다. 웹 서버는 `web` 메서드로 등록합니다:

```php
use App\Mcp\Servers\WeatherServer;
use Laravel\Mcp\Facades\Mcp;

Mcp::web('/mcp/weather', WeatherServer::class);
```

일반 라우트처럼 미들웨어를 적용해 웹 서버의 접근을 보호할 수도 있습니다:

```php
Mcp::web('/mcp/weather', WeatherServer::class)
    ->middleware(['throttle:mcp']);
```

<a name="local-servers"></a>
### 로컬 서버

로컬 서버는 아티즌 명령어로 동작하며, [Laravel Boost](/docs/master/installation#installing-laravel-boost)와 같은 로컬 AI 어시스턴트 연동에 적합합니다. `local` 메서드를 사용해 등록할 수 있습니다:

```php
use App\Mcp\Servers\WeatherServer;
use Laravel\Mcp\Facades\Mcp;

Mcp::local('weather', WeatherServer::class);
```

등록 후에는 대개 직접 `mcp:start` 아티즌 명령어를 실행할 필요가 없습니다. 대신 MCP 클라이언트(AI 에이전트)가 서버를 시작하거나, [MCP 인스펙터](#mcp-inspector)를 이용할 수 있습니다.

<a name="tools"></a>
## 툴

툴은 서버가 AI 클라이언트에게 기능을 제공할 수 있도록 도와주는 구성요소로, 언어 모델이 특정 작업을 실행하거나, 코드를 수행하거나, 외부 시스템과 연동하도록 할 수 있습니다:

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
     * 툴 요청을 처리합니다.
     */
    public function handle(Request $request): Response
    {
        $location = $request->get('location');

        // Get weather...

        return Response::text('The weather is...');
    }

    /**
     * 툴 입력 스키마를 반환합니다.
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

툴을 생성하려면 `make:mcp-tool` 아티즌 명령어를 실행하세요.

```shell
php artisan make:mcp-tool CurrentWeatherTool
```

툴을 생성한 뒤, 서버 클래스의 `$tools` 속성에 등록해야 합니다.

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

기본적으로 툴의 이름과 제목은 클래스명을 기준으로 자동 생성됩니다. 예를 들어, `CurrentWeatherTool`은 이름이 `current-weather`이며, 제목은 `Current Weather Tool`이 됩니다. `$name`과 `$title` 속성을 정의하면 원하는 값으로 변경할 수 있습니다.

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

툴 설명은 자동으로 생성되지 않으므로, 항상 의미 있는 `$description` 속성을 반드시 직접 정의해야 합니다.

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
> 설명은 툴의 메타데이터에서 매우 중요한 부분으로, AI 모델이 툴을 언제 어떻게 활용할지 이해하는 데 도움을 줍니다.

<a name="tool-input-schemas"></a>
### 툴 입력 스키마

툴은 입력 스키마를 정의하여 AI 클라이언트가 어떤 인수를 제공해야 하는지 명시할 수 있습니다. Laravel의 `Illuminate\Contracts\JsonSchema\JsonSchema` 빌더를 사용해 툴의 입력 요구사항을 지정할 수 있습니다.

```php
<?php

namespace App\Mcp\Tools;

use Illuminate\Contracts\JsonSchema\JsonSchema;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * 툴의 입력 스키마 반환.
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

툴은 [출력 스키마](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#output-schema)를 정의하여 응답 구조를 명확하게 할 수 있습니다. AI 클라이언트가 데이터를 파싱하는 데 유용합니다. 출력 스키마는 `outputSchema` 메서드로 구현합니다.

```php
<?php

namespace App\Mcp\Tools;

use Illuminate\Contracts\JsonSchema\JsonSchema;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * 툴의 출력 스키마 반환.
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

JSON Schema는 툴 인수에 대한 기본 구조만 규정하므로, 수동으로 더 복잡한 유효성 검증이 필요할 수 있습니다.

Laravel MCP는 Laravel의 [유효성 검증 기능](/docs/master/validation)과 완벽하게 연동됩니다. 툴의 `handle` 메서드에서 인수의 유효성을 검증하세요.

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

유효성 검증 실패 시, AI 클라이언트는 제공한 에러 메시지에 따라 동작하기 때문에 명확하고 구체적인 메시지를 작성하는 것이 중요합니다.

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

Laravel의 [서비스 컨테이너](/docs/master/container)는 모든 툴을 자동으로 주입합니다. 생성자에 필요한 의존성을 타입힌트하면, 자동으로 인스턴스가 주입됩니다.

```php
<?php

namespace App\Mcp\Tools;

use App\Repositories\WeatherRepository;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * 새로운 툴 인스턴스 생성자.
     */
    public function __construct(
        protected WeatherRepository $weather,
    ) {}

    // ...
}
```

생성자 외에도, `handle` 메서드 인자에 의존성을 타입힌트하여 메서드 호출 시 자동으로 주입받을 수 있습니다.

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
### 툴 어노테이션

툴에 [어노테이션](https://modelcontextprotocol.io/specification/2025-06-18/schema#toolannotations)을 추가하여 AI 클라이언트가 해당 툴의 특성과 동작을 더 잘 이해할 수 있도록 메타데이터를 부여할 수 있습니다. 어노테이션은 속성(Attribute)으로 선언합니다.

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

사용 가능한 어노테이션 목록:

| 어노테이션               | 타입     | 설명                                                                                 |
| ----------------------- | -------- | ----------------------------------------------------------------------------------- |
| `#[IsReadOnly]`         | boolean  | 툴이 환경을 수정하지 않음을 나타냅니다.                                               |
| `#[IsDestructive]`      | boolean  | 툴이 파괴적인 변경을 수행할 수 있음을 나타냅니다(읽기 전용이 아닐 때 유의미).           |
| `#[IsIdempotent]`       | boolean  | 같은 인수로 여러 번 호출해도 추가 효과가 없음을 나타냅니다(읽기 전용이 아닐 때 유의미). |
| `#[IsOpenWorld]`        | boolean  | 툴이 외부 엔티티와 상호작용할 수 있음을 나타냅니다.                                   |

어노테이션 값은 인자(boolean)로 명시적으로 조정할 수 있습니다.

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
### 툴 조건부 등록

툴 클래스에 `shouldRegister` 메서드를 구현해서 실행 시점에 조건에 따라 툴을 등록할 수 있습니다. 예를 들어, 애플리케이션 상태, 설정, 요청 파라미터에 따라 툴을 동적으로 노출하지 않도록 할 수 있습니다.

```php
<?php

namespace App\Mcp\Tools;

use Laravel\Mcp\Request;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * 툴 등록 여부 판단.
     */
    public function shouldRegister(Request $request): bool
    {
        return $request?->user()?->subscribed() ?? false;
    }
}
```

`shouldRegister`가 `false`를 반환하면, 해당 툴은 이용 가능 목록에서 제외되며 AI 클라이언트가 호출할 수 없습니다.

<a name="tool-responses"></a>
### 툴 응답

툴은 반드시 `Laravel\Mcp\Response` 인스턴스를 반환해야 합니다. 이 클래스는 다양한 응답 타입 생성을 위한 여러 메서드를 제공합니다.

간단한 텍스트 응답의 경우, `text` 메서드를 사용하세요.

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

툴 실행 중 에러 발생 시에는 `error` 메서드를 사용하세요.

```php
return Response::error('Unable to fetch weather data. Please try again.');
```

<a name="multiple-content-responses"></a>
#### 다중 응답

툴은 여러 개의 `Response` 인스턴스를 배열로 반환할 수 있습니다.

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

<a name="structured-responses"></a>
#### 구조화된 응답

툴은 `structured` 메서드를 사용해서 [구조화된 콘텐츠](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#structured-content)를 반환할 수 있습니다. 이 방식은 AI 클라이언트가 데이터 파싱을 더욱 쉽게 할 수 있게 해줍니다.

```php
return Response::structured([
    'temperature' => 22.5,
    'conditions' => 'Partly cloudy',
    'humidity' => 65,
]);
```

구조화된 데이터와 함께 텍스트도 같이 제공하고 싶을 때는, 응답 팩토리의 `withStructuredContent` 메서드를 사용하세요.

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

오래 걸리는 작업 또는 실시간 데이터 스트리밍이 필요한 경우, `handle` 메서드에서 [제너레이터](https://www.php.net/manual/en/language.generators.overview.php)를 사용하여 중간 결과를 클라이언트에 순차적으로 보낼 수 있습니다.

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

웹 서버에서 스트리밍 응답을 사용할 경우, 자동으로 SSE(Server-Sent Events) 스트림이 열려 각 메시지가 순차적으로 전송됩니다.

<a name="prompts"></a>
## 프롬프트

[프롬프트](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts)는 서버가 AI 클라이언트에게 재사용 가능한 프롬프트 템플릿을 제공할 수 있도록 하며, AI 모델과의 상호작용을 구조화하는 표준 방식을 제공합니다.

<a name="creating-prompts"></a>
### 프롬프트 생성

프롬프트를 생성하려면 `make:mcp-prompt` 아티즌 명령어를 실행하세요.

```shell
php artisan make:mcp-prompt DescribeWeatherPrompt
```

생성한 프롬프트를 서버의 `$prompts` 속성에 등록하세요.

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
#### 프롬프트 이름, 제목, 설명

프롬프트의 이름과 제목 역시 기본적으로 클래스명에서 자동 생성됩니다. 예를 들어, `DescribeWeatherPrompt`는 이름이 `describe-weather`, 제목이 `Describe Weather Prompt`입니다. `$name`과 `$title` 속성으로 커스터마이징이 가능합니다.

```php
class DescribeWeatherPrompt extends Prompt
{
    /**
     * 프롬프트의 이름.
     */
    protected string $name = 'weather-assistant';

    /**
     * 프롬프트 제목.
     */
    protected string $title = 'Weather Assistant Prompt';

    // ...
}
```

프롬프트 설명도 반드시 의미 있게 `$description` 속성으로 정의해 주세요.

```php
class DescribeWeatherPrompt extends Prompt
{
    /**
     * 프롬프트 설명.
     */
    protected string $description = 'Generates a natural-language explanation of the weather for a given location.';

    //
}
```

> [!NOTE]
> 설명은 프롬프트의 메타데이터에서 매우 중요한 위치를 차지하며, AI 모델이 프롬프트를 언제 어떻게 잘 활용할 수 있는지 이해하게 해줍니다.

<a name="prompt-arguments"></a>
### 프롬프트 인수

프롬프트는 인수(Argument)를 정의해 AI 클라이언트가 템플릿 내 변수를 채울 수 있도록 지원합니다. `arguments` 메서드에 허용할 인수를 명시합니다.

```php
<?php

namespace App\Mcp\Prompts;

use Laravel\Mcp\Server\Prompt;
use Laravel\Mcp\Server\Prompts\Argument;

class DescribeWeatherPrompt extends Prompt
{
    /**
     * 프롬프트의 인수 목록 반환.
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

프롬프트 인수는 정의에 따라 기본 유효성 검증이 되지만, 더 복잡한 검증이 필요할 경우 아래처럼 직접 적용할 수 있습니다.

Laravel MCP는 Laravel의 [유효성 검증 기능](/docs/master/validation)과 연동됩니다. 프롬프트의 `handle` 메서드에서 요청 값을 검증할 수 있습니다.

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

        // tone 값으로 프롬프트 응답 생성...
    }
}
```

에러 메시지를 명확하게 작성하세요. AI 클라이언트는 해당 메시지에 따라 동작합니다.

```php
$validated = $request->validate([
    'tone' => ['required','string','max:50'],
],[
    'tone.*' => 'You must specify a tone for the weather description. Examples include "formal", "casual", or "humorous".',
]);
```

<a name="prompt-dependency-injection"></a>
### 프롬프트 의존성 주입

Laravel의 [서비스 컨테이너](/docs/master/container)는 모든 프롬프트를 주입 형태로 제공합니다. 생성자 혹은 `handle` 메서드 인수에 필요한 타입을 선언하시기만 하면 됩니다.

```php
<?php

namespace App\Mcp\Prompts;

use App\Repositories\WeatherRepository;
use Laravel\Mcp\Server\Prompt;

class DescribeWeatherPrompt extends Prompt
{
    /**
     * 새 프롬프트 인스턴스 생성자.
     */
    public function __construct(
        protected WeatherRepository $weather,
    ) {}

    //
}
```

또한 `handle` 메서드 내 인수에 타입힌트를 추가하면 자동 주입받을 수 있습니다.

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

프롬프트 클래스의 `shouldRegister` 메서드를 통해 런타임에 프롬프트의 등록 여부를 동적으로 판단할 수 있습니다.

```php
<?php

namespace App\Mcp\Prompts;

use Laravel\Mcp\Request;
use Laravel\Mcp\Server\Prompt;

class CurrentWeatherPrompt extends Prompt
{
    /**
     * 프롬프트 등록 여부 판단.
     */
    public function shouldRegister(Request $request): bool
    {
        return $request?->user()?->subscribed() ?? false;
    }
}
```

`shouldRegister`가 `false`를 반환하면, 해당 프롬프트는 목록에서 보이지 않으며 AI 클라이언트가 호출할 수 없습니다.

<a name="prompt-responses"></a>
### 프롬프트 응답

프롬프트는 단일 `Laravel\Mcp\Response` 또는 `Laravel\Mcp\Response`의 반복(iterable)값을 반환할 수 있습니다. 이 응답이 AI 클라이언트에 전달됩니다.

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

`asAssistant()` 메서드는 메시지가 AI 어시스턴트의 답변임을 표시하며, 일반 메시지는 사용자 입력으로 간주됩니다.

<a name="resources"></a>
## 리소스

[리소스](https://modelcontextprotocol.io/specification/2025-06-18/server/resources)는 서버가 AI 클라이언트에게 데이터를 제공하여, 언어 모델 상호작용에 컨텍스트를 부여할 수 있는 기능입니다. 문서, 설정, 각종 데이터 등 정적 또는 동적 정보를 AI와 공유할 수 있습니다.

<a name="creating-resources"></a>
## 리소스 생성

리소스를 생성하려면 다음 아티즌 명령어를 실행하세요.

```shell
php artisan make:mcp-resource WeatherGuidelinesResource
```

생성한 리소스를 서버 클래스의 `$resources` 속성에 등록하세요.

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
#### 리소스 이름, 제목, 설명

리소스의 이름과 제목도 기본적으로 클래스명에서 파생됩니다. 예를 들어, `WeatherGuidelinesResource`는 이름이 `weather-guidelines`, 제목이 `Weather Guidelines Resource`가 됩니다. `$name`과 `$title` 속성으로 커스터마이즈 가능합니다.

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

설명 역시 반드시 의미 있게 `$description` 속성을 작성하세요.

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
> 설명은 리소스의 메타데이터에서 매우 중요한 부분을 담당하며, AI 모델이 효과적으로 리소스를 활용할 수 있도록 하려면 반드시 작성해 주세요.

<a name="resource-templates"></a>
### 리소스 템플릿

[리소스 템플릿](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#resource-templates)을 사용하면, URI 패턴에 변수 구간을 지정해 여러 리소스를 동적으로 처리할 수 있습니다.

<a name="creating-resource-templates"></a>
#### 리소스 템플릿 생성

`HasUriTemplate` 인터페이스를 구현하고, `uriTemplate` 메서드에서 `UriTemplate` 인스턴스를 반환하세요.

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
     * 리소스 URI 템플릿 반환.
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

        // 파일 내용 조회...

        return Response::text($content);
    }
}
```

`HasUriTemplate` 구현 시, 정적 리소스가 아니라 템플릿 형태로 등록됩니다. 클라이언트가 URI 패턴에 맞게 요청하면 템플릿 변수는 요청 정보 내에서 자동으로 추출되어 `handle` 메서드에서 사용 가능합니다.

<a name="uri-template-syntax"></a>
#### URI 템플릿 문법

URI에 중괄호로 감싼 변수로 템플릿을 정의합니다.

```php
new UriTemplate('file://users/{userId}');
new UriTemplate('file://users/{userId}/files/{fileId}');
new UriTemplate('https://api.example.com/{version}/{resource}/{id}');
```

<a name="accessing-template-variables"></a>
#### 템플릿 변수 접근

URI가 리소스 템플릿과 일치하면, 추출된 변수는 요청 객체의 `get` 메서드로 읽을 수 있습니다.

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

        // 필요하다면 전체 URI도 조회 가능
        $uri = $request->uri();

        // 사용자 프로필 정보 조회...

        return Response::text("Profile for user {$userId}");
    }
}
```

`Request` 객체는 추출된 변수와 원본 URI 모두를 제공하므로, 리소스 요청의 모든 정보를 활용할 수 있습니다.

<a name="resource-uri-and-mime-type"></a>
### 리소스 URI 및 MIME 타입

각 리소스는 고유 URI와 MIME 타입을 가집니다. AI 클라이언트가 콘텐츠 형식과 구조를 이해하는 데 도움이 됩니다.

기본적으로 리소스의 URI는 이름을 기반으로 자동 생성되며, 예를 들어 `WeatherGuidelinesResource`는 `weather://resources/weather-guidelines`가 됩니다. 기본 MIME 타입은 `text/plain`입니다.

필요하다면 `$uri`와 `$mimeType` 속성으로 직접 지정할 수 있습니다.

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

이렇게 지정한 URI와 MIME 타입은 AI 클라이언트가 리소스를 적절히 해석 및 처리하는 기준이 됩니다.

<a name="resource-request"></a>
### 리소스 요청

툴·프롬프트와 달리 리소스는 입력 스키마나 인수를 정의할 수 없습니다. 대신, `handle` 메서드 내부에서 요청 객체를 적절히 활용해 처리합니다.

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

Laravel [서비스 컨테이너](/docs/master/container)는 모든 리소스도 자동 의존성 주입을 제공합니다. 생성자와 `handle` 메서드에 필요한 모든 의존성을 선언하면 자동으로 주입됩니다.

```php
<?php

namespace App\Mcp\Resources;

use App\Repositories\WeatherRepository;
use Laravel\Mcp\Server\Resource;

class WeatherGuidelinesResource extends Resource
{
    /**
     * 새 리소스 인스턴스 생성자.
     */
    public function __construct(
        protected WeatherRepository $weather,
    ) {}

    // ...
}
```

`handle` 메서드 내에서도 동일하게 의존성을 받을 수 있습니다.

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
### 리소스 어노테이션

리소스에도 [어노테이션](https://modelcontextprotocol.io/specification/2025-06-18/schema#resourceannotations)을 추가하여 AI 클라이언트에 추가 메타데이터를 노출할 수 있습니다. 어노테이션은 Attribute로 지정합니다.

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

사용 가능한 어노테이션은 다음과 같습니다.

| 어노테이션           | 타입            | 설명                                                            |
| ------------------- | --------------- | --------------------------------------------------------------- |
| `#[Audience]`       | Role 또는 배열   | 지정된 대상자(Role::User, Role::Assistant, 또는 둘 다)를 지정       |
| `#[Priority]`       | float           | 0.0~1.0 사이의 자원 중요도 점수                                |
| `#[LastModified]`   | string          | ISO 8601 포맷의 마지막 수정 일시                                 |

<a name="conditional-resource-registration"></a>
### 리소스 조건부 등록

리소스 클래스에 `shouldRegister` 메서드를 구현해 런타임 시점에 등록 여부를 동적으로 제어할 수 있습니다.

```php
<?php

namespace App\Mcp\Resources;

use Laravel\Mcp\Request;
use Laravel\Mcp\Server\Resource;

class WeatherGuidelinesResource extends Resource
{
    /**
     * 리소스 등록 여부 판단.
     */
    public function shouldRegister(Request $request): bool
    {
        return $request?->user()?->subscribed() ?? false;
    }
}
```

`shouldRegister`가 `false`를 반환하면, 해당 리소스는 목록에 표시되지 않으며 AI 클라이언트가 접근할 수 없습니다.

<a name="resource-responses"></a>
### 리소스 응답

리소스는 반드시 `Laravel\Mcp\Response` 인스턴스를 반환해야 합니다. 텍스트는 `text` 메서드로 반환할 수 있습니다.

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

바이너리 파일 등 Blob 응답은 `blob` 메서드로 제공합니다.

```php
return Response::blob(file_get_contents(storage_path('weather/radar.png')));
```

Blob 파일의 MIME 타입은 리소스 클래스의 `$mimeType` 속성에 따라 결정됩니다.

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

<a name="resource-error-responses"></a>
#### 에러 응답

리소스 조회 중 오류 발생 시 `error()` 메서드를 사용하세요.

```php
return Response::error('Unable to fetch weather data for the specified location.');
```

<a name="metadata"></a>
## 메타데이터

Laravel MCP는 [MCP 명세](https://modelcontextprotocol.io/specification/2025-06-18/basic#meta)에서 요구하는 `_meta` 필드도 지원합니다. 이 필드는 MCP 클라이언트 또는 연동환경에서 필요할 수 있습니다. 메타데이터는 툴, 리소스, 프롬프트 및 각각의 응답에 모두 추가할 수 있습니다.

응답 콘텐츠에 메타데이터를 추가하려면 `withMeta` 메서드를 사용하세요.

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

전체 응답에 메타데이터를 추가하려면, `Response::make`로 래핑하여 팩토리 인스턴스에 `withMeta`를 호출하세요.

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

툴, 리소스, 프롬프트 자체에 대한 메타데이터는 클래스 내 `$meta` 속성으로 지정합니다.

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

웹 MCP 서버는 일반 라우트처럼 미들웨어를 이용해 인증 처리가 가능합니다. 인증이 적용된 서버는 사용자가 기능 이용 전 인증을 반드시 완료해야 합니다.

인증 방식은 크게 두 가지입니다. [Laravel Sanctum](/docs/master/sanctum)을 통한 단순 토큰 인증 또는 `Authorization` HTTP 헤더에 토큰을 직접 전달하는 방법, 혹은 [Laravel Passport](/docs/master/passport)를 통한 OAuth 인증입니다.

<a name="oauth"></a>
### OAuth 2.1

가장 강력하며 권장되는 인증 방식은 [Laravel Passport](/docs/master/passport)를 활용한 OAuth 인증입니다.

MCP 서버를 OAuth로 보호하려면, `routes/ai.php` 파일에서 `Mcp::oauthRoutes` 메서드를 호출하여 필요한 OAuth2 디스커버리 및 클라이언트 등록 라우트를 등록하세요. 이후 MCP 서버 웹 라우트에 Passport의 `auth:api` 미들웨어를 적용합니다.

```php
use App\Mcp\Servers\WeatherExample;
use Laravel\Mcp\Facades\Mcp;

Mcp::oauthRoutes();

Mcp::web('/mcp/weather', WeatherExample::class)
    ->middleware('auth:api');
```

#### Passport 신규 설치

Laravel Passport를 아직 사용하지 않는다면, [Passport 설치 및 배포 가이드](/docs/master/passport#installation)에 따라 Passport를 애플리케이션에 추가하세요. OAuthenticatable 모델, 인증 가드, Passport 키 등이 준비되어 있어야 합니다.

이후, MCP에서 제공하는 Passport 권한 부여 뷰를 게시하세요.

```shell
php artisan vendor:publish --tag=mcp-views
```

`AppServiceProvider`의 `boot` 메서드에서 `Passport::authorizationView` 메서드를 호출하여 해당 뷰를 지정해야 합니다.

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

이 뷰는 최종 사용자가 AI 에이전트의 인증 시도에 대해 승인 또는 거부할 때 표시됩니다.

![Authorization screen example](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABOAAAAROCAMAAABKc73cAAAA81BMV...)

> [!NOTE]
> 이 시나리오에서는 OAuth를 인증 가능한 모델로 변환하는 허브로만 사용하며, 스코프 등의 기능은 사용하지 않습니다.

#### 기존 Passport 설치 이용

이미 Passport를 사용하는 경우, MCP는 기존 Passport 설치와 문제없이 연동됩니다. 단, OAuth가 인증 가능한 모델에 대한 변환 레이어 역할만 하므로 커스텀 스코프는 현재 지원되지 않습니다.

`Mcp::oauthRoutes` 메서드는 내부적으로 `mcp:use`라는 단일 스코프를 사용·광고합니다.

#### Passport vs. Sanctum

MCP 명세상 공식 인증 방식은 OAuth2.1이며, MCP 클라이언트 대부분에서 가장 널리 지원됩니다. 가능하다면 Passport 사용을 권장합니다.

그러나 이미 [Sanctum](/docs/master/sanctum)을 사용하는 경우, 추가로 Passport를 설치하는 것이 부담될 수 있습니다. 이럴 땐 반드시 필요한 경우가 아니라면 전체 MCP 기능을 Passport 없이도 Sanctum만으로 운영하는 것을 권장합니다.

<a name="sanctum"></a>
### Sanctum

[Sanctum](/docs/master/sanctum)으로 MCP 서버를 보호하려면, 서버에 Sanctum 인증 미들웨어를 추가하세요. MCP 클라이언트는 반드시 `Authorization: Bearer <token>` 헤더를 포함해야 인증이 정상적으로 처리됩니다.

```php
use App\Mcp\Servers\WeatherExample;
use Laravel\Mcp\Facades\Mcp;

Mcp::web('/mcp/demo', WeatherExample::class)
    ->middleware('auth:sanctum');
```

<a name="custom-mcp-authentication"></a>
#### 맞춤형 MCP 인증

애플리케이션에서 자체적으로 API 토큰을 발급하여 사용하는 경우, MCP 서버의 `Mcp::web` 라우트에 모든 커스텀 미들웨어를 자유롭게 적용할 수 있습니다. 이때 직접 `Authorization` 헤더를 검사하여 인증 처리를 할 수 있습니다.

<a name="authorization"></a>
## 인가

현재 인증된 사용자는 `$request->user()` 메서드로 접근할 수 있으며, 이를 활용해 MCP 툴 및 리소스 내에서 [인가(권한) 체크](/docs/master/authorization)를 수행할 수 있습니다.

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

MCP 서버는 내장 MCP 인스펙터 또는 단위 테스트로 테스트할 수 있습니다.

<a name="mcp-inspector"></a>
### MCP 인스펙터

[MCP 인스펙터](https://modelcontextprotocol.io/docs/tools/inspector)는 MCP 서버의 기능을 테스트하고 디버깅할 수 있는 인터랙티브 도구입니다. 서버에 연결해서 인증을 검증하고, 툴·리소스·프롬프트 기능을 직접 테스트해볼 수 있습니다.

등록된 서버라면 다음과 같이 인스펙터를 실행할 수 있습니다.

```shell
# 웹 서버 테스트...
php artisan mcp:inspector mcp/weather

# "weather"로 등록된 로컬 서버 테스트...
php artisan mcp:inspector weather
```

위 명령은 MCP 인스펙터를 실행하며, MCP 클라이언트 설정값도 함께 제공하므로 환경 구성에 참고할 수 있습니다. 웹 서버에 인증 미들웨어가 적용되어 있다면, 연결 시 반드시 `Authorization` 베어러 토큰과 같은 필수 헤더를 포함해야 합니다.

<a name="unit-tests"></a>
### 단위 테스트

MCP 서버, 툴, 리소스, 프롬프트에 대해 단위 테스트를 작성할 수 있습니다.

먼저 새로운 테스트 케이스를 만들고, 서버의 각 프리미티브(툴/프롬프트/리소스)를 호출하세요. 예를 들어, `WeatherServer`의 툴을 테스트하려면 아래와 같이 작성할 수 있습니다.

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

이와 동일하게 프롬프트와 리소스도 테스트할 수 있습니다.

```php
$response = WeatherServer::prompt(...);
$response = WeatherServer::resource(...);
```

`actingAs` 메서드로 인증된 유저로 동작하는 것도 가능합니다.

```php
$response = WeatherServer::actingAs($user)->tool(...);
```

응답이 도달하면, 다양한 assertion 메서드로 응답의 내용과 상태를 검증할 수 있습니다.

응답이 성공인지 확인하려면 `assertOk` 메서드를, 특정 텍스트를 포함하는지 검증하려면 `assertSee` 메서드를 사용할 수 있습니다.

```php
$response->assertOk();

$response->assertSee('The current weather in New York City is 72°F and sunny.');
```

에러 응답 여부는 `assertHasErrors`, 해당 에러 메시지 포함 여부는 배열을 넘기면 됩니다.

```php
$response->assertHasErrors();

$response->assertHasErrors([
    'Something went wrong.',
]);
```

에러가 없어야 하는 경우는 `assertHasNoErrors`를 사용하세요.

```php
$response->assertHasNoErrors();
```

응답에 포함된 메타데이터는 `assertName()`, `assertTitle()`, `assertDescription()` 등으로 검증 가능합니다.

```php
$response->assertName('current-weather');
$response->assertTitle('Current Weather Tool');
$response->assertDescription('Fetches the current weather forecast for a specified location.');
```

알림(Notification)이 실제 전송됐는지, 그리고 그 횟수는 `assertSentNotification`, `assertNotificationCount`로 검증 가능합니다.

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

마지막으로 원시 응답 내용을 디버깅 목적으로 출력하려면 `dd`나 `dump` 메서드를 사용할 수 있습니다.

```php
$response->dd();
$response->dump();
```