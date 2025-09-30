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
    - [툴 인수 유효성 검증](#validating-tool-arguments)
    - [툴 의존성 주입](#tool-dependency-injection)
    - [툴 애너테이션](#tool-annotations)
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

[Laravel MCP](https://github.com/laravel/mcp)는 [Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro)을 통해 AI 클라이언트가 Laravel 애플리케이션과 상호작용할 수 있는 간결하고 우아한 방식을 제공합니다. 이 패키지는 서버, 툴, 리소스, 프롬프트를 정의할 수 있는 직관적이며 유연한 인터페이스를 제공하여, AI 기반 상호작용을 애플리케이션에 쉽게 구현할 수 있도록 지원합니다.

<a name="installation"></a>
## 설치

먼저, Composer 패키지 매니저를 사용하여 프로젝트에 Laravel MCP를 설치합니다:

```shell
composer require laravel/mcp
```

<a name="publishing-routes"></a>
### 라우트 퍼블리싱

Laravel MCP를 설치한 후, `vendor:publish` 아티즌 명령어를 실행하여 MCP 서버를 등록할 `routes/ai.php` 파일을 퍼블리시합니다:

```shell
php artisan vendor:publish --tag=ai-routes
```

이 명령어는 애플리케이션의 `routes` 디렉터리에 `routes/ai.php` 파일을 생성하며, 이 파일에서 MCP 서버를 등록할 수 있습니다.

<a name="creating-servers"></a>
## 서버 생성

`make:mcp-server` 아티즌 명령어를 사용하여 MCP 서버를 생성할 수 있습니다. 서버는 AI 클라이언트에 툴, 리소스, 프롬프트 등의 MCP 기능을 제공하는 중심 역할을 합니다:

```shell
php artisan make:mcp-server WeatherServer
```

이 명령어를 실행하면 `app/Mcp/Servers` 디렉터리에 새 서버 클래스가 생성됩니다. 생성된 서버 클래스는 Laravel MCP의 기본 `Laravel\Mcp\Server` 클래스를 확장하며, 툴, 리소스, 프롬프트 등록용 속성을 제공합니다:

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
     * LLM을 위한 MCP 서버의 안내 메시지.
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

서버를 생성한 후에는 `routes/ai.php` 파일에서 서버를 반드시 등록해야 접근할 수 있습니다. MCP 서버 등록에는 HTTP 접근이 가능한 `web` 방식과 커맨드 라인에서 사용하는 `local` 방식이 있습니다.

<a name="web-servers"></a>
### 웹 서버

웹 서버는 가장 흔하게 사용되는 방식으로, HTTP POST 요청을 통해 접근할 수 있습니다. 이는 원격 AI 클라이언트 또는 웹 기반 연동에 적합합니다. `web` 메서드로 웹 서버를 등록할 수 있습니다:

```php
use App\Mcp\Servers\WeatherServer;
use Laravel\Mcp\Facades\Mcp;

Mcp::web('/mcp/weather', WeatherServer::class);
```

일반 라우트와 마찬가지로, 미들웨어를 적용해 웹 서버를 보호할 수 있습니다:

```php
Mcp::web('/mcp/weather', WeatherServer::class)
    ->middleware(['throttle:mcp']);
```

<a name="local-servers"></a>
### 로컬 서버

로컬 서버는 아티즌 명령어로 실행하며, [Laravel Boost](/docs/12.x/installation#installing-laravel-boost)와 같이 로컬 AI 어시스턴트 통합에 적합합니다. `local` 메서드를 사용하여 등록합니다:

```php
use App\Mcp\Servers\WeatherServer;
use Laravel\Mcp\Facades\Mcp;

Mcp::local('weather', WeatherServer::class);
```

등록 후에는 일반적으로 직접 `mcp:start` 아티즌 명령어를 실행할 필요가 없습니다. 대신 MCP 클라이언트(AI 에이전트)가 서버를 시작하거나, [MCP 인스펙터](#mcp-inspector)를 사용할 수 있습니다.

<a name="tools"></a>
## 툴

툴을 통해 서버에서 AI 클라이언트가 호출 가능한 기능을 제공할 수 있으며, 언어 모델이 코드 실행, 외부 시스템 연동 등의 동작을 수행할 수 있도록 합니다:

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

기본적으로 툴의 이름과 제목은 클래스명에서 자동으로 유추됩니다. 예를 들어, `CurrentWeatherTool`의 이름은 `current-weather`, 제목은 `Current Weather Tool`이 됩니다. `$name`과 `$title` 속성을 직접 정의해 커스터마이즈할 수 있습니다:

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

툴의 설명은 자동으로 생성되지 않으므로, 항상 의미 있는 설명을 `$description` 속성으로 작성해야 합니다:

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
> 설명은 툴의 메타데이터에서 매우 중요한 부분입니다. AI 모델이 툴을 언제, 어떻게 사용해야 유용할지 이해하는 데 도움을 줍니다.

<a name="tool-input-schemas"></a>
### 툴 입력 스키마

툴은 입력 스키마를 정의해 AI 클라이언트로부터 받는 인수의 형식을 명확히 할 수 있습니다. Laravel의 `Illuminate\JsonSchema\JsonSchema` 빌더를 활용해 입력 요구 사항을 정의하세요:

```php
<?php

namespace App\Mcp\Tools;

use Illuminate\JsonSchema\JsonSchema;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * 툴의 입력 스키마 반환.
     *
     * @return array<string, JsonSchema>
     */
    public function schema(JsonSchema $schema): array
    {
        return [
            'location' => $schema->string()
                ->description('The location to get the weather for.')
                ->required(),

            'units' => $schema->array()
                ->enum(['celsius', 'fahrenheit'])
                ->description('The temperature units to use.')
                ->default('celsius'),
        ];
    }
}
```

<a name="validating-tool-arguments"></a>
### 툴 인수 유효성 검증

JSON Schema는 인수의 기본 구조를 정의하지만, 더 복잡한 유효성 검증도 적용할 수 있습니다.

Laravel MCP는 Laravel의 [유효성 검증 기능](/docs/12.x/validation)과 완벽하게 연동됩니다. 툴의 `handle` 메서드 안에서 들어오는 인수에 대해 검증 규칙을 정의할 수 있습니다:

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

        // 검증된 인수를 활용하여 날씨 정보 조회 ...
    }
}
```

유효성 검증 실패 시, AI 클라이언트가 제공된 오류 메시지에 따라 동작하므로, 명확하고 실행 가능한 오류 메시지를 작성하는 것이 중요합니다:

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

모든 툴은 Laravel [서비스 컨테이너](/docs/12.x/container)로 해석되어 생성됩니다. 따라서, 생성자에서 필요한 의존성을 타입힌트로 선언하면 자동으로 주입됩니다:

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

생성자 이외에도, 툴의 `handle()` 메서드에서도 타입힌트로 의존성을 주입받을 수 있습니다. 서비스 컨테이너는 해당 메서드 호출 시점에 의존성을 자동으로 해석 및 주입합니다:

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

툴에 [애너테이션](https://modelcontextprotocol.io/specification/2025-06-18/schema#toolannotations)을 추가해 AI 클라이언트에게 추가적인 메타데이터를 제공할 수 있습니다. 애너테이션은 툴의 동작과 특성을 AI 모델이 더 잘 이해할 수 있도록 돕습니다. PHP 어트리뷰트 형태로 애너테이션을 추가할 수 있습니다:

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

| 애너테이션         | 타입    | 설명                                                                            |
| ------------------ | ------- | ------------------------------------------------------------------------------- |
| `#[IsReadOnly]`    | boolean | 툴이 환경을 변경하지 않음을 나타냅니다.                                         |
| `#[IsDestructive]` | boolean | 툴이 파괴적인 업데이트를 수행할 수 있음을 나타냅니다(읽기 전용일 때는 의미 없음). |
| `#[IsIdempotent]`  | boolean | 동일한 인수로 여러 번 호출해도 추가 변화가 없음을 나타냅니다(읽기 전용 아님일 때).|
| `#[IsOpenWorld]`   | boolean | 툴이 외부 엔터티와 상호작용할 수 있음을 나타냅니다.                             |

<a name="conditional-tool-registration"></a>
### 툴 조건부 등록

툴 클래스에 `shouldRegister` 메서드를 구현하면 런타임에 동적으로 툴 등록 여부를 결정할 수 있습니다. 이 메서드는 애플리케이션 상태, 설정, 요청 파라미터에 따라 툴의 노출 여부를 제어합니다:

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

`shouldRegister` 메서드가 `false`를 반환하면, 해당 툴은 사용 가능한 목록에 나타나지 않으며 AI 클라이언트가 호출할 수 없습니다.

<a name="tool-responses"></a>
### 툴 응답

툴은 반드시 `Laravel\Mcp\Response` 인스턴스를 반환해야 합니다. Response 클래스에는 다양한 유형의 응답을 생성할 수 있는 메서드가 준비되어 있습니다.

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

툴 실행 중 에러를 나타내려면 `error` 메서드를 사용합니다:

```php
return Response::error('Unable to fetch weather data. Please try again.');
```

<a name="multiple-content-responses"></a>
#### 다중 콘텐츠 응답

툴은 여러 개의 응답을 배열로 반환할 수도 있습니다:

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

실행 시간이 길거나 실시간 데이터 스트리밍이 필요한 경우, 툴의 `handle` 메서드에서 [generator](https://www.php.net/manual/en/language.generators.overview.php)를 반환하면, 중간 업데이트를 클라이언트에 실시간 전송할 수 있습니다:

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

[프롬프트](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts)는 서버가 AI 클라이언트에 재사용 가능한 프롬프트 템플릿을 제공할 수 있게 해줍니다. 이를 통해 자주 사용하는 질의나 상호작용을 표준화할 수 있습니다.

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

프롬프트도 클래스명에서 이름과 제목을 자동으로 도출합니다. 예를 들어, `DescribeWeatherPrompt` 클래스는 `describe-weather` 이름과 `Describe Weather Prompt` 제목을 갖게 됩니다. `$name`, `$title` 속성으로 값을 직접 지정할 수 있습니다:

```php
class DescribeWeatherPrompt extends Prompt
{
    /**
     * 프롬프트 이름.
     */
    protected string $name = 'weather-assistant';

    /**
     * 프롬프트 제목.
     */
    protected string $title = 'Weather Assistant Prompt';

    // ...
}
```

프롬프트 설명은 자동 생성되지 않으므로 꼭 의미 있는 설명을 `$description` 속성으로 작성하세요:

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
> 설명은 프롬프트의 메타데이터에서 매우 중요한 역할을 하며, AI 모델이 어떤 상황에서 프롬프트를 잘 활용할 수 있는지 판단하는 데 도움이 됩니다.

<a name="prompt-arguments"></a>
### 프롬프트 인수

프롬프트는 인수 정의를 통해 AI 클라이언트가 템플릿 내용을 원하는 값으로 커스터마이즈할 수 있습니다. `arguments` 메서드를 사용하여 인수 목록을 정의하세요:

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

프롬프트 인수는 정의에 따라 자동 유효성 검증이 수행되지만, 필요하다면 더 복잡한 검증 규칙도 적용할 수 있습니다.

Laravel MCP는 Laravel의 [유효성 검증 기능](/docs/12.x/validation)과 연동됩니다. 프롬프트의 `handle` 메서드 안에서 인수에 대한 검증을 추가할 수 있습니다:

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

        // 주어진 tone을 활용해 프롬프트 응답 생성...
    }
}
```

유효성 검증 실패 시에도 명확한 오류 메시지를 제공해야 하므로, 적절한 메시지를 작성하세요:

```php
$validated = $request->validate([
    'tone' => ['required','string','max:50'],
],[
    'tone.*' => 'You must specify a tone for the weather description. Examples include "formal", "casual", or "humorous".',
]);
```

<a name="prompt-dependency-injection"></a>
### 프롬프트 의존성 주입

모든 프롬프트 클래스는 Laravel [서비스 컨테이너](/docs/12.x/container)로 생성됩니다. 생성자에서 필요한 의존성을 타입힌트로 선언하면 자동 주입됩니다:

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

뿐만 아니라, 프롬프트의 `handle` 메서드에서도 의존성을 타입힌트로 주입받을 수 있습니다:

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

프롬프트 클래스에 `shouldRegister` 메서드를 구현하면 런타임 상황에 따라 프롬프트 표출 여부를 동적으로 결정할 수 있습니다:

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

`shouldRegister`가 `false`를 반환할 경우, 해당 프롬프트는 사용 목록에 나타나지 않으며 AI 클라이언트는 호출할 수 없습니다.

<a name="prompt-responses"></a>
### 프롬프트 응답

프롬프트는 단일 `Laravel\Mcp\Response` 또는 이터러블 형태의 여러 Response 인스턴스를 반환할 수 있습니다. 이 응답들은 AI 클라이언트에 전달되는 최종 내용을 포함합니다:

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

`asAssistant()` 메서드를 사용하면 해당 메시지가 AI 어시스턴트에서 발신된 응답임을 나타낼 수 있습니다. 일반 메시지는 사용자 입력으로 처리됩니다.

<a name="resources"></a>
## 리소스

[리소스](https://modelcontextprotocol.io/specification/2025-06-18/server/resources)를 통해 서버는 AI 클라이언트에게 읽기 전용 데이터 또는 콘텐츠를 제공합니다. 이는 문서, 설정, 다양한 데이터 등, AI 응답의 맥락 정보를 제공하기 위해 사용할 수 있습니다.

<a name="creating-resources"></a>
## 리소스 생성

리소스를 생성하려면 `make:mcp-resource` 아티즌 명령어를 실행하세요:

```shell
php artisan make:mcp-resource WeatherGuidelinesResource
```

생성한 후에는 서버의 `$resources` 속성에 해당 리소스를 등록해야 합니다:

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

리소스 이름과 제목도 클래스명에서 자동으로 도출됩니다. 예를 들어, `WeatherGuidelinesResource`는 `weather-guidelines`라는 이름과 `Weather Guidelines Resource`라는 제목을 가지게 됩니다. `$name`, `$title` 속성으로 직접 지정할 수 있습니다:

```php
class WeatherGuidelinesResource extends Resource
{
    /**
     * 리소스 이름.
     */
    protected string $name = 'weather-api-docs';

    /**
     * 리소스 제목.
     */
    protected string $title = 'Weather API Documentation';

    // ...
}
```

설명도 자동 생성되지 않으므로, 의미 있는 설명을 `$description` 속성에 작성하세요:

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
> 설명은 메타데이터의 중요한 일부로, AI 모델이 언제 이 리소스를 활용해야 하는지 이해하는 데 필수적입니다.

<a name="resource-uri-and-mime-type"></a>
### 리소스 URI 및 MIME 타입

각 리소스는 고유한 URI와, 해당 리소스의 포맷을 나타내는 MIME 타입을 가집니다.

기본적으로 URI는 이름에서 자동 생성되며, 예를 들어 `WeatherGuidelinesResource` 의 URI는 `weather://resources/weather-guidelines`가 됩니다. MIME 타입의 기본값은 `text/plain`입니다.

이 값을 `$uri`, `$mimeType` 속성으로 직접 지정해 커스터마이즈할 수 있습니다:

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

URI와 MIME 타입을 명확히 지정하면, AI 클라이언트가 리소스 콘텐츠의 형식에 맞춰 적절히 처리할 수 있습니다.

<a name="resource-request"></a>
### 리소스 요청

툴이나 프롬프트와 달리 리소스는 입력 스키마나 인수를 정의하지 않습니다. 그러나 `handle` 메서드 내에서 요청 객체와 상호작용할 수 있습니다:

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

모든 리소스 클래스도 Laravel [서비스 컨테이너](/docs/12.x/container)를 통해 생성됩니다. 필요한 의존성은 생성자에서 타입힌트로 선언하면 자동 주입됩니다:

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

또한, `handle` 메서드에서 추가 의존성 주입도 가능합니다:

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

리소스 클래스에 `shouldRegister` 메서드를 구현하면, 애플리케이션 상태나 환경에 따라 리소스 노출 여부를 동적으로 제어할 수 있습니다:

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

`shouldRegister`가 `false`를 반환하면, 해당 리소스는 목록에 나타나지 않으며, AI 클라이언트가 접근할 수 없습니다.

<a name="resource-responses"></a>
### 리소스 응답

리소스도 반드시 `Laravel\Mcp\Response` 인스턴스를 반환해야 합니다. 간단한 텍스트 데이터의 경우 `text` 메서드를 사용하세요:

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

블롭(blob) 데이터를 반환하려면, `blob` 메서드에 파일 내용을 전달합니다:

```php
return Response::blob(file_get_contents(storage_path('weather/radar.png')));
```

블롭 반환 시, MIME 타입은 클래스의 `$mimeType` 속성값을 따릅니다:

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

리소스 조회 중 에러를 알리려면 `error()` 메서드를 사용하세요:

```php
return Response::error('Unable to fetch weather data for the specified location.');
```

<a name="authentication"></a>
## 인증

웹 MCP 서버는 일반 라우트와 동일하게 미들웨어를 이용해 인증을 적용할 수 있습니다. 사용자는 서버의 모든 기능을 사용하기 전 인증이 요구됩니다.

MCP 서버 인증 방식은 [Laravel Sanctum](/docs/12.x/sanctum)을 이용한 간단한 토큰 방식, 또는 `Authorization` HTTP 헤더를 통해 전달되는 임의의 API 토큰, 혹은 [Laravel Passport](/docs/12.x/passport)를 사용한 OAuth 인증 방식 등이 있습니다.

<a name="oauth"></a>
### OAuth 2.1

웹 기반 MCP 서버를 보호하는 가장 강력한 방법은 [Laravel Passport](/docs/12.x/passport)를 통한 OAuth 방식입니다.

OAuth로 서버를 인증하려면, `routes/ai.php` 파일에서 `Mcp::oauthRoutes` 메서드를 호출해 필요한 OAuth2 디스커버리 및 클라이언트 등록 라우트를 등록해야 합니다. 이후, 해당 서버의 `Mcp::web` 라우트에 Passport의 `auth:api` 미들웨어도 적용합니다:

```php
use App\Mcp\Servers\WeatherExample;
use Laravel\Mcp\Facades\Mcp;

Mcp::oauthRoutes();

Mcp::web('/mcp/weather', WeatherExample::class)
    ->middleware('auth:api');
```

#### Passport 신규 설치

애플리케이션에서 Laravel Passport를 미사용 중이라면, 우선 [Passport 설치 및 배포 문서](/docs/12.x/passport#installation)를 따라 `OAuthenticatable` 모델과 인증 가드, 키를 준비하세요.

이후, MCP에서 제공하는 Passport 인증 뷰를 퍼블리시합니다:

```shell
php artisan vendor:publish --tag=mcp-views
```

그리고, Passport가 이 뷰를 사용하도록 `Passport::authorizationView` 메서드를 호출합니다. 보통 `AppServiceProvider`의 `boot` 메서드 내에 아래처럼 추가합니다:

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

이 뷰는 인증 시도 중 최종 사용자에게 AI 에이전트 접근 승인/거부 화면으로 표시됩니다.

![Authorization screen example](data:image/png;base64,iVBORw...)

> [!NOTE]
> 이 예시에서는 인증 가능한 모델에 대한 "중계"로서 OAuth만 사용하며, OAuth의 scope 등 많은 기능은 생략하고 있습니다.

#### 기존 Passport 설치 활용

이미 Passport를 사용 중이라면, MCP는 별다른 추가 설정 없이 기존 환경과 문제없이 연동됩니다. 단, 현재는 OAuth가 인증 모델의 translation 용도로만 사용되므로 커스텀 스코프는 지원되지 않습니다.

MCP에서는 `Mcp::oauthRoutes()` 메서드를 이용해 단일 `mcp:use` 스코프만 사용·광고합니다.

#### Passport vs. Sanctum

Model Context Protocol 명세에서는 OAuth2.1을 공식 인증 방식으로 정의하고 있으며, 대부분의 MCP 클라이언트도 이 방식을 기본 지원합니다. 따라서 가능하다면 Passport를 사용하는 것이 권장됩니다.

만약 기존에 [Sanctum](/docs/12.x/sanctum)을 이미 사용 중이라면, Passport를 추가로 도입해야만 하는 특별한 필요가 생기기 전까지는 Sanctum만으로 MCP 서버를 보호할 수도 있습니다.

<a name="sanctum"></a>
### Sanctum

MCP 서버를 [Sanctum](/docs/12.x/sanctum)으로 보호하려면, 단순히 서버에 Sanctum 인증 미들웨어를 접목하세요. 클라이언트는 `Authorization: Bearer <token>` 헤더를 통해 인증 토큰을 반드시 전달해야 합니다:

```php
use App\Mcp\Servers\WeatherExample;
use Laravel\Mcp\Facades\Mcp;

Mcp::web('/mcp/demo', WeatherExample::class)
    ->middleware('auth:sanctum');
```

<a name="custom-mcp-authentication"></a>
#### 커스텀 MCP 인증

애플리케이션에서 자체적으로 API 토큰을 발급하고 있다면, 원하는 미들웨어를 MCP 서버의 `Mcp::web` 라우트에 직접 적용하여 인증처리를 하면 됩니다. 커스텀 미들웨어에서 `Authorization` 헤더를 직접 검사해 요청을 인증할 수 있습니다.

<a name="authorization"></a>
## 인가

현재 인증된 사용자를 `$request->user()` 메서드로 가져올 수 있으므로, MCP 툴이나 리소스 내부에서 [인가(authorization) 검사](/docs/12.x/authorization)를 수행할 수 있습니다:

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

내장된 MCP 인스펙터 또는 유닛 테스트를 작성해 MCP 서버의 동작을 검증할 수 있습니다.

<a name="mcp-inspector"></a>
### MCP 인스펙터

[MCP 인스펙터](https://modelcontextprotocol.io/docs/tools/inspector)는 MCP 서버의 테스트와 디버깅을 위한 인터랙티브 도구입니다. 이를 활용해 서버와 직접 연결하고 인증을 검증하거나 툴, 리소스, 프롬프트 기능을 실험할 수 있습니다.

등록된 서버에 대해 인스펙터를 실행하려면 다음과 같이 명령어를 입력합니다:

```shell
# 웹 서버 ...
php artisan mcp:inspector mcp/weather

# "weather" 라는 이름의 로컬 서버 ...
php artisan mcp:inspector weather
```

해당 명령을 실행하면 MCP 인스펙터가 실행되어, 클라이언트 설정 정보를 출력합니다. 이 정보를 MCP 클라이언트에 복사해 올바른 연결 설정을 할 수 있습니다. 만약 웹 서버가 인증 미들웨어로 보호되어 있다면, `Authorization` 헤더 등 필요한 인증 정보를 꼭 추가해야 합니다.

<a name="unit-tests"></a>
### 유닛 테스트

MCP 서버, 툴, 리소스, 프롬프트에 대한 유닛 테스트를 작성할 수 있습니다.

먼저 테스트 케이스를 만들고, 테스트할 MCP 프리미티브(툴, 프롬프트, 리소스)를 포함하는 서버에서 해당 액션을 직접 호출하면 됩니다. 예를 들어, `WeatherServer`의 툴을 테스트하려면:

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

프롬프트와 리소스에 대한 테스트도 마찬가지로 작성할 수 있습니다:

```php
$response = WeatherServer::prompt(...);
$response = WeatherServer::resource(...);
```

인증된 사용자로 동작하고 싶다면, 프리미티브 호출 전에 `actingAs` 메서드를 체이닝할 수 있습니다:

```php
$response = WeatherServer::actingAs($user)->tool(...);
```

응답을 받은 후 다양한 assertion 메서드를 활용해 응답의 내용과 상태를 검증할 수 있습니다.

`assertOk` 메서드를 사용해 응답이 정상임을(오류가 없음을) 확인할 수 있습니다:

```php
$response->assertOk();
```

`assertSee` 메서드를 사용해 응답에 특정 텍스트가 포함되어 있는지 검사할 수 있습니다:

```php
$response->assertSee('The current weather in New York City is 72°F and sunny.');
```

`assertHasErrors` 메서드를 사용해 응답에 에러가 포함되어 있는지 확인할 수 있습니다:

```php
$response->assertHasErrors();

$response->assertHasErrors([
    'Something went wrong.',
]);
```

`assertHasNoErrors` 메서드로 에러가 포함되지 않았음을 검증할 수 있습니다:

```php
$response->assertHasNoErrors();
```

응답의 메타데이터가 특정 값을 가지는지도 검증할 수 있습니다(`assertName()`, `assertTitle()`, `assertDescription()`):

```php
$response->assertName('current-weather');
$response->assertTitle('Current Weather Tool');
$response->assertDescription('Fetches the current weather forecast for a specified location.');
```

특정 알림이 전송되었는지도 `assertSentNotification`, `assertNotificationCount`를 통해 검증 가능합니다:

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

마지막으로, 응답 내용을 직접 확인하고 싶다면 `dd` 또는 `dump` 메서드를 사용할 수 있습니다:

```php
$response->dd();
$response->dump();
```
