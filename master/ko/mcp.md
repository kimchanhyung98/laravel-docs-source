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
    - [리소스 애노테이션](#resource-annotations)
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

[Laravel MCP](https://github.com/laravel/mcp)는 [Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro)을 활용하여 AI 클라이언트가 Laravel 애플리케이션과 쉽고 우아하게 상호작용할 수 있는 방법을 제공합니다. MCP는 서버, 툴, 리소스, 프롬프트와 같은 기능을 선언적이고 유연하게 정의할 수 있는 플루언트 인터페이스를 제공하여, AI 기반 기능을 애플리케이션에 손쉽게 도입할 수 있도록 합니다.

<a name="installation"></a>
## 설치

시작하려면 Composer 패키지 관리자를 이용하여 Laravel MCP를 프로젝트에 설치합니다:

```shell
composer require laravel/mcp
```

<a name="publishing-routes"></a>
### 라우트 퍼블리싱

Laravel MCP 설치 후, MCP 서버를 정의할 `routes/ai.php` 파일을 퍼블리시하기 위해 `vendor:publish` Artisan 명령어를 실행하세요:

```shell
php artisan vendor:publish --tag=ai-routes
```

이 명령은 애플리케이션의 `routes` 디렉터리에 `routes/ai.php` 파일을 생성합니다. 이 파일에서 MCP 서버를 등록하게 됩니다.

<a name="creating-servers"></a>
## 서버 생성

MCP 서버는 `make:mcp-server` Artisan 명령어로 생성할 수 있습니다. 서버는 MCP 기능(툴, 리소스, 프롬프트 등)을 AI 클라이언트에 제공하는 중심 통신 지점 역할을 합니다.

```shell
php artisan make:mcp-server WeatherServer
```

이 명령은 `app/Mcp/Servers` 디렉터리에 새로운 서버 클래스를 생성합니다. 생성된 서버 클래스는 MCP의 기본 `Laravel\Mcp\Server` 클래스를 상속하며, 툴, 리소스, 프롬프트를 등록할 속성을 제공합니다:

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
     * LLM을 위한 MCP 서버 안내문
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

서버를 생성한 후에는 `routes/ai.php` 파일에 등록하여 접근 가능하도록 해야 합니다. MCP는 HTTP로 접근 가능한 서버인 `web`과 커맨드라인 전용 서버인 `local` 두 가지 등록 방식을 제공합니다.

<a name="web-servers"></a>
### 웹 서버

웹 서버는 HTTP POST 요청을 통해 접근할 수 있는 가장 일반적인 서버 유형이며, 원격 AI 클라이언트나 웹 기반 통합에 적합합니다. `web` 메서드로 등록할 수 있습니다:

```php
use App\Mcp\Servers\WeatherServer;
use Laravel\Mcp\Facades\Mcp;

Mcp::web('/mcp/weather', WeatherServer::class);
```

일반 라우트처럼, 미들웨어를 적용하여 웹 서버를 보호할 수도 있습니다:

```php
Mcp::web('/mcp/weather', WeatherServer::class)
    ->middleware(['throttle:mcp']);
```

<a name="local-servers"></a>
### 로컬 서버

로컬 서버는 Artisan 명령어로 실행되며, [Laravel Boost](/docs/master/installation#installing-laravel-boost) 등 로컬 AI 어시스턴트 통합에 적합합니다. `local` 메서드로 등록할 수 있습니다:

```php
use App\Mcp\Servers\WeatherServer;
use Laravel\Mcp\Facades\Mcp;

Mcp::local('weather', WeatherServer::class);
```

등록이 완료되면, 대개 직접 `mcp:start` Artisan 명령어를 실행할 필요는 없습니다. MCP 클라이언트(AI 에이전트)가 서버를 자동으로 시작하거나 [MCP 인스펙터](#mcp-inspector)를 이용할 수 있습니다.

<a name="tools"></a>
## 툴

툴은 서버가 AI 클라이언트에 호출 가능한 기능을 노출할 수 있도록 합니다. 이를 통해 언어 모델이 동작을 수행하거나, 코드를 실행하거나, 외부 시스템과 연동할 수 있습니다:

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

툴을 생성하려면 `make:mcp-tool` Artisan 명령어를 실행합니다:

```shell
php artisan make:mcp-tool CurrentWeatherTool
```

툴을 생성한 후, 서버 클래스의 `$tools` 속성에 등록해야 합니다:

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
#### 툴 이름, 제목, 설명

기본적으로 툴의 이름과 제목은 클래스명에서 파생됩니다. 예를 들어, `CurrentWeatherTool` 클래스는 이름이 `current-weather`, 제목이 `Current Weather Tool`로 지정됩니다. `$name` 및 `$title` 속성을 직접 정의해서 커스터마이징할 수도 있습니다:

```php
class CurrentWeatherTool extends Tool
{
    /**
     * 툴 이름
     */
    protected string $name = 'get-optimistic-weather';

    /**
     * 툴 제목
     */
    protected string $title = 'Get Optimistic Weather Forecast';

    // ...
}
```

툴 설명은 자동으로 생성되지 않으므로, 항상 `$description` 속성을 직접 정의하여 명확한 설명을 제공합니다:

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
> 설명은 툴의 메타데이터에서 핵심적인 부분이며, AI 모델이 툴을 언제 어떻게 활용할지 이해하는 데 매우 중요합니다.

<a name="tool-input-schemas"></a>
### 툴 입력 스키마

툴은 AI 클라이언트로부터 어떤 인수를 받을지 정의하는 입력 스키마를 선언할 수 있습니다. Laravel의 `Illuminate\Contracts\JsonSchema\JsonSchema` 빌더를 활용해 입력 요구사항을 선언합니다:

```php
<?php

namespace App\Mcp\Tools;

use Illuminate\Contracts\JsonSchema\JsonSchema;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * 툴 입력 스키마
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

툴은 [출력 스키마](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#output-schema)를 정의하여 응답 데이터의 구조를 명확하게 지정할 수 있습니다. 이는 AI 클라이언트가 툴 결과를 파싱할 때 유용합니다. `outputSchema` 메서드를 사용해 출력 구조를 정의하세요:

```php
<?php

namespace App\Mcp\Tools;

use Illuminate\Contracts\JsonSchema\JsonSchema;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * 툴 출력 스키마
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

JSON Schema 정의만으로는 기본적인 인수 구조만 지정할 수 있으나, 더 복잡한 유효성 검증 규칙이 필요할 때도 있습니다.

Laravel MCP는 Laravel의 [유효성 검증 기능](/docs/master/validation)과 자연스럽게 통합됩니다. 툴의 `handle` 메서드 내에서 들어오는 인수에 대해 유효성 검증을 실행할 수 있습니다:

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

        // 검증된 인수를 사용하여 날씨 데이터 조회...
    }
}
```

유효성 검증에 실패한 경우, AI 클라이언트는 제공된 에러 메시지에 따라 동작하게 됩니다. 따라서, 명확하고 구체적인 에러 메시지를 제공하는 것이 매우 중요합니다:

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

모든 툴은 Laravel [서비스 컨테이너](/docs/master/container)를 통해 해석되므로, 필요한 의존성을 생성자에 타입힌트로 지정할 수 있습니다. 선언된 의존성은 자동으로 주입됩니다:

```php
<?php

namespace App\Mcp\Tools;

use App\Repositories\WeatherRepository;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * 새 툴 인스턴스 생성
     */
    public function __construct(
        protected WeatherRepository $weather,
    ) {}

    // ...
}
```

생성자 주입 외에, `handle()` 메서드에도 의존성을 타입힌트로 지정할 수 있습니다. 서비스 컨테이너가 알아서 의존성을 주입합니다:

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

툴에 [애노테이션](https://modelcontextprotocol.io/specification/2025-06-18/schema#toolannotations)을 추가해 AI 클라이언트에 추가 메타데이터를 제공할 수 있습니다. 애노테이션은 툴의 동작과 특성을 AI 모델이 더 잘 이해하도록 돕습니다. 애노테이션은 속성(Attribute) 형태로 추가합니다:

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

사용 가능한 애노테이션 목록:

| 애노테이션          | 타입    | 설명                                                                                   |
| ------------------- | ------- | -------------------------------------------------------------------------------------- |
| `#[IsReadOnly]`     | boolean | 툴이 환경을 수정하지 않음을 나타냅니다.                                                |
| `#[IsDestructive]`  | boolean | 툴이 파괴적인 업데이트를 할 수 있음을 나타냅니다(읽기 전용이 아닐 때 의미가 있습니다). |
| `#[IsIdempotent]`   | boolean | 같은 인수로 여러 번 호출해도 추가 효과가 없는 경우(읽기 전용이 아닐 때)                 |
| `#[IsOpenWorld]`    | boolean | 툴이 외부 엔터티와 상호작용할 수 있음을 나타냅니다.                                   |

애노테이션 값은 boolean으로 명시적으로 설정할 수 있습니다:

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

툴 클래스를 정의할 때 `shouldRegister` 메서드를 구현하면, 실행 시점에 툴의 등록 여부를 조건적으로 제어할 수 있습니다. 애플리케이션의 상태, 설정, 요청 파라미터 등에 따라 툴을 활성화할 수 있습니다:

```php
<?php

namespace App\Mcp\Tools;

use Laravel\Mcp\Request;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * 툴 등록 가능 여부 결정
     */
    public function shouldRegister(Request $request): bool
    {
        return $request?->user()?->subscribed() ?? false;
    }
}
```

`shouldRegister`가 false를 반환하면, 해당 툴은 사용 가능한 목록에 나타나지 않으며 AI 클라이언트가 호출할 수 없습니다.

<a name="tool-responses"></a>
### 툴 응답

툴은 반드시 `Laravel\Mcp\Response` 인스턴스를 반환해야 합니다. Response 클래스는 여러 종류의 응답을 생성할 수 있는 편리한 메서드를 제공합니다.

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

툴 실행 중 오류를 알릴 때는 `error` 메서드를 사용합니다:

```php
return Response::error('Unable to fetch weather data. Please try again.');
```

<a name="multiple-content-responses"></a>
#### 여러 콘텐츠 응답

툴은 복수의 `Response` 인스턴스를 배열로 반환하여 여러 메시지를 한 번에 보낼 수 있습니다:

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

<a name="structured-responses"></a>
#### 구조화된 응답

툴은 `structured` 메서드를 사용해 [구조화된 콘텐츠](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#structured-content)를 반환할 수 있습니다. AI 클라이언트가 파싱 가능한 데이터를 제공합니다:

```php
return Response::structured([
    'temperature' => 22.5,
    'conditions' => 'Partly cloudy',
    'humidity' => 65,
]);
```

구조화된 데이터와 함께 커스텀 텍스트도 함께 제공해야 할 경우, 응답 팩토리의 `withStructuredContent` 메서드를 활용하세요:

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

시간이 오래 걸리거나 실시간 데이터가 필요한 경우, `handle` 메서드에서 [generator](https://www.php.net/manual/en/language.generators.overview.php)를 반환하면 각 단계별로 중간 업데이트를 클라이언트에 스트리밍할 수 있습니다:

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

웹 기반 서버에서 스트리밍 응답을 반환하면 자동으로 SSE(Server-Sent Events) 스트림이 열리며, 각 메시지가 이벤트로 전송됩니다.

<a name="prompts"></a>
## 프롬프트

[프롬프트](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts)는 서버에서 재사용 가능한 프롬프트 템플릿을 공유하여, AI 클라이언트가 언어 모델과의 상호작용을 표준화된 방식으로 구조화할 수 있도록 합니다.

<a name="creating-prompts"></a>
### 프롬프트 생성

프롬프트를 생성하려면 `make:mcp-prompt` Artisan 명령어를 실행하세요:

```shell
php artisan make:mcp-prompt DescribeWeatherPrompt
```

생성된 프롬프트를 서버 클래스의 `$prompts` 속성에 등록합니다:

```php
<?php

namespace App\Mcp\Servers;

use App\Mcp\Prompts\DescribeWeatherPrompt;
use Laravel\Mcp\Server;

class WeatherServer extends Server
{
    /**
     * MCP 서버에 등록된 프롬프트 목록
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

프롬프트 이름과 제목은 기본적으로 클래스명에서 파생됩니다. 예를 들어, `DescribeWeatherPrompt` 클래스의 이름은 `describe-weather`, 제목은 `Describe Weather Prompt`입니다. `$name`과 `$title` 속성을 직접 정의하여 변경할 수 있습니다:

```php
class DescribeWeatherPrompt extends Prompt
{
    /**
     * 프롬프트 이름
     */
    protected string $name = 'weather-assistant';

    /**
     * 프롬프트 제목
     */
    protected string $title = 'Weather Assistant Prompt';

    // ...
}
```

프롬프트 설명은 자동 생성되지 않으니, `$description` 속성에 구체적으로 작성하는 것이 좋습니다:

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
> 설명은 프롬프트 메타데이터에서 핵심 역할을 하며, AI 모델이 어떠한 상황에서 어떻게 프롬프트를 활용할지 파악하는 데 매우 중요합니다.

<a name="prompt-arguments"></a>
### 프롬프트 인수

프롬프트는 인수를 정의하여 AI 클라이언트가 템플릿을 원하는 값으로 커스터마이즈할 수 있습니다. `arguments` 메서드를 통해 입력받을 인수를 정의하세요:

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

프롬프트 인수는 정의에 따라 자동 유효성 검증이 실행되지만, 복잡한 검증이 필요한 경우도 있습니다.

Laravel MCP는 Laravel [유효성 검증 기능](/docs/master/validation)과 통합됩니다. 프롬프트의 `handle` 메서드에서 추가적인 검증을 진행할 수도 있습니다:

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

        // tone 값을 사용해서 프롬프트 응답 생성...
    }
}
```

유효성 검증 실패 시, AI 클라이언트가 이해하기 쉽도록 명확하고 구체적인 에러 메시지를 제공하세요:

```php
$validated = $request->validate([
    'tone' => ['required','string','max:50'],
],[
    'tone.*' => 'You must specify a tone for the weather description. Examples include "formal", "casual", or "humorous".',
]);
```

<a name="prompt-dependency-injection"></a>
### 프롬프트 의존성 주입

모든 프롬프트는 Laravel [서비스 컨테이너](/docs/master/container)를 통해 해석됩니다. 생성자의 타입힌트를 통해 필요한 의존성을 선언할 수 있습니다.

```php
<?php

namespace App\Mcp\Prompts;

use App\Repositories\WeatherRepository;
use Laravel\Mcp\Server\Prompt;

class DescribeWeatherPrompt extends Prompt
{
    /**
     * 프롬프트 인스턴스 생성
     */
    public function __construct(
        protected WeatherRepository $weather,
    ) {}

    //
}
```

생성자뿐 아니라, `handle` 메서드에도 타입힌트로 의존성을 선언해 자동 주입받을 수 있습니다:

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
### 프롬프트 조건부 등록

프롬프트 클래스에서 `shouldRegister` 메서드를 구현하면 실행 시점에 프롬프트의 등록 여부를 조건적으로 제어할 수 있습니다:

```php
<?php

namespace App\Mcp\Prompts;

use Laravel\Mcp\Request;
use Laravel\Mcp\Server\Prompt;

class CurrentWeatherPrompt extends Prompt
{
    /**
     * 프롬프트 등록 가능 여부 결정
     */
    public function shouldRegister(Request $request): bool
    {
        return $request?->user()?->subscribed() ?? false;
    }
}
```

`shouldRegister`가 false를 반환할 경우, 해당 프롬프트는 목록에 나타나지 않으며 호출할 수 없습니다.

<a name="prompt-responses"></a>
### 프롬프트 응답

프롬프트는 단일 `Laravel\Mcp\Response`나 복수의 `Laravel\Mcp\Response` 인스턴스를 반환할 수 있습니다. 응답 객체는 AI 클라이언트에 제공할 콘텐츠를 kapsel화합니다:

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

`asAssistant()` 메서드를 사용해 해당 메시지가 어시스턴트(assistant)의 답변임을 명시적으로 구분할 수 있습니다. 기본 메시지는 사용자 입력으로 간주됩니다.

<a name="resources"></a>
## 리소스

[리소스](https://modelcontextprotocol.io/specification/2025-06-18/server/resources)는 서버가 외부(AI 클라이언트)에 읽기 전용 데이터나 콘텐츠를 노출해, LLM이 참조할 수 있는 컨텍스트를 제공합니다. 예를 들어, 문서, 구성 정보 또는 참고할 데이터를 제공할 때 활용할 수 있습니다.

<a name="creating-resources"></a>
## 리소스 생성

리소스를 생성하려면 `make:mcp-resource` Artisan 명령어를 실행합니다:

```shell
php artisan make:mcp-resource WeatherGuidelinesResource
```

생성된 리소스를 서버 클래스의 `$resources` 속성에 등록하세요:

```php
<?php

namespace App\Mcp\Servers;

use App\Mcp\Resources\WeatherGuidelinesResource;
use Laravel\Mcp\Server;

class WeatherServer extends Server
{
    /**
     * MCP 서버에 등록된 리소스 목록
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

리소스의 이름, 제목은 기본적으로 클래스명에서 파생됩니다. 예를 들어, `WeatherGuidelinesResource`는 이름이 `weather-guidelines`, 제목이 `Weather Guidelines Resource`로 생성됩니다. `$name`과 `$title` 속성을 수정해서 변경할 수 있습니다:

```php
class WeatherGuidelinesResource extends Resource
{
    /**
     * 리소스 이름
     */
    protected string $name = 'weather-api-docs';

    /**
     * 리소스 제목
     */
    protected string $title = 'Weather API Documentation';

    // ...
}
```

리소스 설명은 자동 생성되지 않으니, `$description` 속성을 직접 설정해 주세요:

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
> 설명은 리소스의 메타데이터에서 매우 중요하며, AI 모델이 언제 어떻게 리소스를 활용할지 이해하는 데 도움이 됩니다.

<a name="resource-templates"></a>
### 리소스 템플릿

[리소스 템플릿](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#resource-templates)을 활용하면, 변수 URI 패턴을 사용하여 동적으로 리소스를 제공할 수 있습니다. 정적 URI 대신, 템플릿 패턴을 이용해 하나의 리소스로 여러 URI에 대응할 수 있습니다.

<a name="creating-resource-templates"></a>
#### 리소스 템플릿 생성

리소스 클래스에 `HasUriTemplate` 인터페이스를 구현하고, `uriTemplate` 메서드에서 `UriTemplate` 인스턴스를 반환하면 리소스 템플릿이 됩니다:

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
     * 리소스 설명
     */
    protected string $description = 'Access user files by ID';

    /**
     * MIME 타입
     */
    protected string $mimeType = 'text/plain';

    /**
     * 해당 리소스의 URI 템플릿
     */
    public function uriTemplate(): UriTemplate
    {
        return new UriTemplate('file://users/{userId}/files/{fileId}');
    }

    /**
     * 리소스 요청 처리
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

`HasUriTemplate`를 구현하면, 리소스가 정적 리소스가 아니라 템플릿 리소스로 등록됩니다. AI 클라이언트는 템플릿 패턴에 맞는 URI로 요청을 보내며, URI 변수는 `handle` 메서드에서 자동으로 사용할 수 있습니다.

<a name="uri-template-syntax"></a>
#### URI 템플릿 문법

중괄호`{}`로 변수 구간을 표시하여 가변적인 URI 세그먼트를 선언할 수 있습니다:

```php
new UriTemplate('file://users/{userId}');
new UriTemplate('file://users/{userId}/files/{fileId}');
new UriTemplate('https://api.example.com/{version}/{resource}/{id}');
```

<a name="accessing-template-variables"></a>
#### 템플릿 변수 접근

URI가 템플릿과 일치하는 경우, 변수는 자동으로 요청에 포함되며 `get` 메서드로 접근할 수 있습니다:

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
        // 변수 접근
        $userId = $request->get('userId');

        // 전체 URI 참조
        $uri = $request->uri();

        // 사용자 프로필 조회...

        return Response::text("Profile for user {$userId}");
    }
}
```

`Request` 객체는 추출된 변수와 요청된 원본 URI 모두를 제공합니다.

<a name="resource-uri-and-mime-type"></a>
### 리소스 URI 및 MIME 타입

각 리소스는 고유한 URI와 AI 클라이언트가 리소스의 형식을 이해할 수 있게 해주는 MIME 타입을 가집니다.

기본적으로, URI는 리소스 이름 기반으로 생성됩니다(`WeatherGuidelinesResource` → `weather://resources/weather-guidelines`). 기본 MIME 타입은 `text/plain`입니다.

필요하다면 `$uri`와 `$mimeType` 속성을 오버라이드해서 직접 지정할 수 있습니다:

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
     * MIME 타입
     */
    protected string $mimeType = 'application/pdf';
}
```

URI와 MIME 타입은 AI 클라이언트가 리소스 콘텐츠를 올바르게 해석하도록 돕습니다.

<a name="resource-request"></a>
### 리소스 요청

툴이나 프롬프트와 달리, 리소스는 입력 스키마나 인수를 정의할 수 없습니다. 하지만 `handle` 메서드 내에서 요청 객체를 자유롭게 활용할 수 있습니다:

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

리소스 역시 Laravel [서비스 컨테이너](/docs/master/container)를 통해 해석됩니다. 생성자에서 의존성을 타입힌트로 선언하세요:

```php
<?php

namespace App\Mcp\Resources;

use App\Repositories\WeatherRepository;
use Laravel\Mcp\Server\Resource;

class WeatherGuidelinesResource extends Resource
{
    /**
     * 생성자 의존성 주입
     */
    public function __construct(
        protected WeatherRepository $weather,
    ) {}

    // ...
}
```

`handle` 메서드에서도 의존성을 타입힌트로 받으면 자동 주입됩니다:

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

<a name="resource-annotations"></a>
### 리소스 애노테이션

리소스에도 [애노테이션](https://modelcontextprotocol.io/specification/2025-06-18/schema#resourceannotations)을 추가해 AI 클라이언트에 추가 메타데이터를 제공할 수 있습니다. 속성(Attribute) 형태로 추가합니다:

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

| 애노테이션          | 타입            | 설명                                                         |
| ------------------- | --------------- | ------------------------------------------------------------ |
| `#[Audience]`       | Role 또는 배열   | 의도된 이용자 역할(`Role::User`, `Role::Assistant` 등) 지정  |
| `#[Priority]`       | float           | 리소스 중요도를 나타내는 0.0~1.0 숫자                        |
| `#[LastModified]`   | string          | ISO 8601 포맷의 리소스 최종 수정 타임스탬프                  |

<a name="conditional-resource-registration"></a>
### 리소스 조건부 등록

`shouldRegister` 메서드를 구현하여 리소스의 조건부 등록도 가능합니다. 애플리케이션 상태, 설정, 요청 파라미터에 따라 리소스를 노출하거나 숨길 수 있습니다:

```php
<?php

namespace App\Mcp\Resources;

use Laravel\Mcp\Request;
use Laravel\Mcp\Server\Resource;

class WeatherGuidelinesResource extends Resource
{
    /**
     * 리소스 등록 가능 여부 결정
     */
    public function shouldRegister(Request $request): bool
    {
        return $request?->user()?->subscribed() ?? false;
    }
}
```

이 메서드가 false를 반환하면, 해당 리소스는 목록에 나타나지 않고 AI 클라이언트가 접근할 수 없습니다.

<a name="resource-responses"></a>
### 리소스 응답

리소스는 반드시 `Laravel\Mcp\Response` 인스턴스를 반환해야 합니다. 간단한 텍스트 응답은 `text` 메서드를 사용하세요:

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

바이너리(Blob) 콘텐츠를 반환하려면, `blob` 메서드를 사용하고 파일 내용을 전달하세요:

```php
return Response::blob(file_get_contents(storage_path('weather/radar.png')));
```

이때의 MIME 타입은 리소스 클래스의 `$mimeType` 속성 값에 따라 결정됩니다:

```php
<?php

namespace App\Mcp\Resources;

use Laravel\Mcp\Server\Resource;

class WeatherGuidelinesResource extends Resource
{
    /**
     * MIME 타입
     */
    protected string $mimeType = 'image/png';

    //
}
```

<a name="resource-error-responses"></a>
#### 에러 응답

리소스 조회 중 오류가 발생했을 때는 `error()` 메서드를 사용합니다:

```php
return Response::error('Unable to fetch weather data for the specified location.');
```

<a name="metadata"></a>
## 메타데이터

Laravel MCP는 MCP 명세서([MCP specification](https://modelcontextprotocol.io/specification/2025-06-18/basic#meta))에 정의된 `_meta` 필드를 지원합니다. 이 필드는 MCP 클라이언트 혹은 통합에서 필수로 요구될 수 있습니다. 메타데이터는 툴, 리소스, 프롬프트 그리고 각각의 응답에도 부착할 수 있습니다.

응답별 메타데이터는 `withMeta` 메서드를 통해 제공합니다:

```php
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;

/**
 * 툴 요청 처리
 */
public function handle(Request $request): Response
{
    return Response::text('The weather is sunny.')
        ->withMeta(['source' => 'weather-api', 'cached' => true]);
}
```

응답 전체에 적용할 메타데이터는 `Response::make`로 래핑하고, 반환된 팩토리 인스턴스에 `withMeta`를 호출하세요:

```php
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\ResponseFactory;

/**
 * 툴 요청 처리
 */
public function handle(Request $request): ResponseFactory
{
    return Response::make(
        Response::text('The weather is sunny.')
    )->withMeta(['request_id' => '12345']);
}
```

툴, 리소스, 프롬프트 자체에 메타데이터를 붙이고 싶다면, 클래스에 `$meta` 속성을 정의하세요:

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

라우트와 동일하게, 웹 MCP 서버에 미들웨어를 적용해 인증 기능을 구현할 수 있습니다. MCP 서버에 인증을 추가하면, 사용자가 서버의 어떤 기능도 사용하기 전에 인증을 마쳐야 합니다.

MCP 서버 인증 방법은 두 가지가 있습니다: [Laravel Sanctum](/docs/master/sanctum)를 이용한 간단한 토큰 기반 인증, 또는 `Authorization` HTTP 헤더에 전달되는 임의의 토큰 인증. OAuth를 통해 [Laravel Passport](/docs/master/passport)를 사용한 인증도 가능합니다.

<a name="oauth"></a>
### OAuth 2.1

웹 기반 MCP 서버를 가장 견고하게 보호할 수 있는 방법은 [Laravel Passport](/docs/master/passport)를 활용한 OAuth 방식입니다.

OAuth로 인증하려면, `routes/ai.php`에서 `Mcp::oauthRoutes`를 호출해 필요한 OAuth2 discovery 및 클라이언트 등록 라우트를 등록하세요. 그리고 `Mcp::web` 라우트에 Passport의 `auth:api` 미들웨어를 적용하세요:

```php
use App\Mcp\Servers\WeatherExample;
use Laravel\Mcp\Facades\Mcp;

Mcp::oauthRoutes();

Mcp::web('/mcp/weather', WeatherExample::class)
    ->middleware('auth:api');
```

#### Passport 신규 설치

앱에서 아직 Laravel Passport를 사용하고 있지 않다면, Passport의 [설치 및 배포 가이드](/docs/master/passport#installation)를 참고하여 도입하세요. OAuthenticatable 모델, 인증 가드, Passport 키 생성 등이 선행되어야 합니다.

다음으로, Laravel MCP가 제공하는 Passport 인가(authorization) 뷰를 퍼블리시하세요:

```shell
php artisan vendor:publish --tag=mcp-views
```

`AppServiceProvider`의 `boot` 메서드에서 Passport가 이 뷰를 사용하도록 지정하세요:

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

이 뷰는 최종 사용자가 인증 중 AI 에이전트의 인증 시도를 승인/거부할 때 보여집니다.

![Authorization screen example](data:image/png;base64,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)

> [!NOTE]
> 이 방식은 OAuth를 인증 가능한 기본 모델로 변환하는 트랜슬레이션 레이어 방식으로, 실제 OAuth 특성(스코프 등)은 대부분 무시됩니다.

#### 기존 Passport 설치와 함께 쓰기

이미 Laravel Passport를 사용 중이라면, 추가 설정 없이 MCP를 사용할 수 있습니다. 단, 현재는 커스텀 스코프를 지원하지 않습니다. OAuth는 MCP에서는 인증 가능한 기본 모델로의 매핑 역할만 수행합니다.

`Mcp::oauthRoutes`를 통해 MCP는 단일 `mcp:use` 스코프만 광고하고 사용합니다.

#### Passport vs. Sanctum

Model Context Protocol 명세에서 공식적으로 문서화된 인증 메커니즘은 OAuth2.1이며, 대부분의 MCP 클라이언트가 이를 우선 지원합니다. 가능하다면 Passport 사용을 권장합니다.

이미 [Sanctum](/docs/master/sanctum)을 도입한 애플리케이션이라면 Passport 추가가 번거로울 수 있습니다. 이 경우, 명확히 필요하지 않은 이상, 우선은 Passport 없이 Sanctum만으로 MCP를 활용할 수 있습니다.

<a name="sanctum"></a>
### Sanctum

[Sanctum](/docs/master/sanctum)으로 MCP 서버를 보호하려면, `routes/ai.php` 파일에서 Sanctum 인증 미들웨어를 서버에 추가하면 됩니다. 이후 MCP 클라이언트가 `Authorization: Bearer <token>` 헤더를 포함해야 인증이 성공합니다:

```php
use App\Mcp\Servers\WeatherExample;
use Laravel\Mcp\Facades\Mcp;

Mcp::web('/mcp/demo', WeatherExample::class)
    ->middleware('auth:sanctum');
```

<a name="custom-mcp-authentication"></a>
#### 사용자 지정 MCP 인증

만약 자체적으로 API 토큰을 발급한다면, 원하는 미들웨어를 `Mcp::web` 라우트에 할당하여 MCP 서버를 인증할 수 있습니다. 커스텀 미들웨어 내에서 `Authorization` 헤더를 직접 검사해 인증 처리를 구현할 수 있습니다.

<a name="authorization"></a>
## 인가

현재 인증된 사용자는 `$request->user()` 메서드로 접근할 수 있습니다. 이를 활용해 MCP 툴이나 리소스 내부에서 [인가(authorization) 검사](/docs/master/authorization)를 수행할 수 있습니다:

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

MCP 서버는 내장 MCP 인스펙터를 활용하거나 단위 테스트를 작성하여 검증할 수 있습니다.

<a name="mcp-inspector"></a>
### MCP 인스펙터

[MCP 인스펙터](https://modelcontextprotocol.io/docs/tools/inspector)는 MCP 서버를 테스트하고 디버깅할 수 있는 대화형 도구입니다. 서버 연결, 인증 검증, 툴·리소스·프롬프트 사용 등을 실시간으로 실험할 수 있습니다.

등록된 서버에서 인스펙터를 실행하려면:

```shell
# 웹 서버 테스트...
php artisan mcp:inspector mcp/weather

# "weather"라는 로컬 서버 테스트...
php artisan mcp:inspector weather
```

실행 시, MCP 인스펙터가 클라이언트 설정값을 출력해주므로, 이를 MCP 클라이언트에 적용하여 올바르게 연결되어 있는지 확인할 수 있습니다. 인증 미들웨어로 보호 중인 서버의 경우, 접속 시 반드시 `Authorization` 토큰 등 필요한 헤더를 포함시켜야 합니다.

<a name="unit-tests"></a>
### 단위 테스트

MCP 서버, 툴, 리소스, 프롬프트 각각에 대해 단위 테스트를 작성할 수 있습니다.

먼저 새 테스트 케이스를 만들고, 테스트하고자 하는 MCP 프리미티브를 등록되어 있는 서버에서 호출하면 됩니다. 예를 들어, `WeatherServer`의 툴 테스트:

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

프롬프트와 리소스도 동일하게 테스트할 수 있습니다:

```php
$response = WeatherServer::prompt(...);
$response = WeatherServer::resource(...);
```

또한, 테스트 중 사용자를 임의로 인증하려면 `actingAs`를 체이닝하세요:

```php
$response = WeatherServer::actingAs($user)->tool(...);
```

응답을 받은 후에는 다양한 어서션 메서드로 결과와 상태를 검증할 수 있습니다.

응답이 성공적인지 확인하려면 `assertOk` 메서드를 사용하세요. 이는 오류가 없는 응답임을 확인합니다:

```php
$response->assertOk();
```

특정 텍스트가 포함되어 있는지 확인하려면 `assertSee`를 사용합니다:

```php
$response->assertSee('The current weather in New York City is 72°F and sunny.');
```

오류가 포함되어 있는지 확인하려면 `assertHasErrors`를 사용합니다:

```php
$response->assertHasErrors();

$response->assertHasErrors([
    'Something went wrong.',
]);
```

오류가 전혀 없는 응답인지 확인하려면 `assertHasNoErrors`를 사용하세요:

```php
$response->assertHasNoErrors();
```

응답에 특정 메타데이터가 포함되어 있는지 `assertName()`, `assertTitle()`, `assertDescription()` 메서드로 검증할 수 있습니다:

```php
$response->assertName('current-weather');
$response->assertTitle('Current Weather Tool');
$response->assertDescription('Fetches the current weather forecast for a specified location.');
```

노티피케이션이 발송되었는지 `assertSentNotification` 및 `assertNotificationCount`로 확인할 수 있습니다:

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

마지막으로, 원시 응답 내용을 직접 확인하려면 `dd` 또는 `dump` 메서드로 응답을 출력할 수 있습니다:

```php
$response->dd();
$response->dump();
```
