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

[Laravel MCP](https://github.com/laravel/mcp)는 [Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro)을 통해 AI 클라이언트가 Laravel 애플리케이션과 상호작용할 수 있도록 단순하고 우아한 방식을 제공합니다. 서버, 툴, 리소스, 프롬프트 등을 정의할 수 있는 직관적이고 유연한 인터페이스를 제공하여 AI 기반 상호작용을 쉽게 구성할 수 있습니다.

<a name="installation"></a>
## 설치

Laravel MCP를 프로젝트에 설치하려면 Composer 패키지 관리자를 사용하세요:

```shell
composer require laravel/mcp
```

<a name="publishing-routes"></a>
### 라우트 퍼블리싱

Laravel MCP 설치 후, `vendor:publish` Artisan 명령어를 실행하여 MCP 서버를 정의할 `routes/ai.php` 파일을 퍼블리시하세요:

```shell
php artisan vendor:publish --tag=ai-routes
```

이 명령어는 애플리케이션의 `routes` 디렉터리에 `routes/ai.php` 파일을 생성합니다. 이 파일에서 MCP 서버를 등록하게 됩니다.

<a name="creating-servers"></a>
## 서버 생성

`make:mcp-server` Artisan 명령어를 사용해 MCP 서버를 생성할 수 있습니다. 서버는 MCP의 핵심 통신 지점으로, 툴, 리소스, 프롬프트 등 MCP 기능을 AI 클라이언트에 노출합니다:

```shell
php artisan make:mcp-server WeatherServer
```

이 명령어는 `app/Mcp/Servers` 디렉터리에 새 서버 클래스를 생성합니다. 생성된 서버 클래스는 Laravel MCP의 기본 `Laravel\Mcp\Server` 클래스를 확장하며, 툴, 리소스, 프롬프트 등록을 위한 속성을 제공합니다:

```php
<?php

namespace App\Mcp\Servers;

use Laravel\Mcp\Server;

class WeatherServer extends Server
{
    /**
     * MCP 서버의 이름
     */
    protected string $name = 'Weather Server';

    /**
     * MCP 서버의 버전
     */
    protected string $version = '1.0.0';

    /**
     * LLM에 전달할 MCP 서버의 안내문
     */
    protected string $instructions = 'This server provides weather information and forecasts.';

    /**
     * 이 MCP 서버에 등록된 툴
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Tool>>
     */
    protected array $tools = [
        // GetCurrentWeatherTool::class,
    ];

    /**
     * 이 MCP 서버에 등록된 리소스
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Resource>>
     */
    protected array $resources = [
        // WeatherGuidelinesResource::class,
    ];

    /**
     * 이 MCP 서버에 등록된 프롬프트
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

서버를 생성했다면, 이를 `routes/ai.php` 파일에 등록해 접근할 수 있도록 해야 합니다. Laravel MCP는 서버 등록을 위한 두 가지 메서드를 제공합니다: HTTP로 접근 가능한 웹 서버를 위한 `web` 메서드, 커맨드라인에서 동작하는 로컬 서버를 위한 `local` 메서드입니다.

<a name="web-servers"></a>
### 웹 서버

웹 서버는 가장 일반적인 유형으로, HTTP POST 요청을 통해 접근할 수 있습니다. 이는 원격 AI 클라이언트나 웹 기반 연동에 적합합니다. 웹 서버를 등록하려면 `web` 메서드를 사용하세요:

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

로컬 서버는 Artisan 명령어로 실행되며, [Laravel Boost](/docs/12.x/installation#installing-laravel-boost)처럼 로컬 AI 어시스턴트 연동에 적합합니다. 로컬 서버를 등록하려면 `local` 메서드를 사용하세요:

```php
use App\Mcp\Servers\WeatherServer;
use Laravel\Mcp\Facades\Mcp;

Mcp::local('weather', WeatherServer::class);
```

등록이 완료되면, 일반적으로 직접 `mcp:start` Artisan 명령어를 실행할 필요는 없습니다. MCP 클라이언트(AI 에이전트)가 서버를 시작하도록 설정하거나, [MCP Inspector](#mcp-inspector)를 사용할 수 있습니다.

<a name="tools"></a>
## 툴

툴을 사용하면 서버가 AI 클라이언트와 상호작용할 수 있는 기능을 노출할 수 있습니다. 툴은 언어 모델이 동작을 실행하거나, 코드를 실행하거나, 외부 시스템과 연동할 수 있도록 해줍니다:

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
     * 툴의 입력 스키마 반환
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

툴을 생성하려면 `make:mcp-tool` Artisan 명령어를 실행하세요:

```shell
php artisan make:mcp-tool CurrentWeatherTool
```

툴을 생성한 뒤, 서버의 `$tools` 속성에 등록해야 합니다:

```php
<?php

namespace App\Mcp\Servers;

use App\Mcp\Tools\CurrentWeatherTool;
use Laravel\Mcp\Server;

class WeatherServer extends Server
{
    /**
     * 이 MCP 서버에 등록된 툴
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Tool>>
     */
    protected array $tools = [
        CurrentWeatherTool::class,
    ];
}
```

#### 툴 이름, 타이틀, 설명

기본적으로 툴의 이름(name)과 타이틀(title)은 클래스명에서 파생됩니다. 예를 들어, `CurrentWeatherTool`의 이름은 `current-weather`, 타이틀은 `Current Weather Tool`이 됩니다. 필요에 따라 `$name`, `$title` 속성을 직접 지정할 수 있습니다:

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

툴 설명(description)은 자동으로 생성되지 않으므로, 항상 명확한 `$description` 속성을 지정해야 합니다:

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
> 설명은 툴의 메타데이터에서 매우 중요합니다. 이 설명을 통해 AI 모델이 언제 어떻게 툴을 사용하는지 효과적으로 이해할 수 있습니다.

<a name="tool-input-schemas"></a>
### 툴 입력 스키마

툴은 입력 스키마를 정의해 AI 클라이언트로부터 어떤 인수를 받을 수 있는지 명확하게 지정할 수 있습니다. Laravel의 `Illuminate\JsonSchema\JsonSchema` 빌더를 사용하여 입력 요구조건을 정의하세요:

```php
<?php

namespace App\Mcp\Tools;

use Illuminate\JsonSchema\JsonSchema;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * 툴의 입력 스키마 반환
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

<a name="validating-tool-arguments"></a>
### 툴 인수 유효성 검증

JSON Schema를 통해 기본적인 인수 구조를 정의할 수 있지만, 더 복잡한 검증 규칙이 필요할 수 있습니다.

Laravel MCP는 Laravel의 [유효성 검증 기능](/docs/12.x/validation)과 자연스럽게 연동됩니다. 툴의 `handle` 메서드 안에서 인수 유효성 검증을 직접 수행할 수 있습니다:

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

        // 유효성 검증된 인수를 활용해 날씨 데이터 조회...
    }
}
```

유효성 검증에 실패할 경우, AI 클라이언트는 제공된 에러 메시지에 따라 동작합니다. 따라서 명확하고 구체적인 에러 메시지를 제공하는 것이 중요합니다:

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

Laravel의 [서비스 컨테이너](/docs/12.x/container)는 모든 MCP 툴을 해결할 때 사용됩니다. 따라서 툴이 필요로 하는 의존성은 생성자에 타입힌트로 선언만 하면 자동 주입됩니다:

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

생성자 주입 외에도, 툴의 `handle()` 메서드에서 의존성을 타입힌트로 작성하면 서비스 컨테이너가 호출 시 자동 주입합니다:

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
### 툴 어노테이션

툴에 [어노테이션](https://modelcontextprotocol.io/specification/2025-06-18/schema#toolannotations)을 추가해 AI 클라이언트에 추가 메타데이터를 제공합니다. 어노테이션을 사용하면 AI 모델이 툴의 동작 가능성과 성격을 더 잘 이해할 수 있습니다. 어노테이션은 속성(Attribute)으로 툴에 부여합니다:

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

사용 가능한 어노테이션은 다음과 같습니다:

| 어노테이션          | 타입    | 설명                                                                  |
| ------------------ | ------- | --------------------------------------------------------------------- |
| `#[IsReadOnly]`    | boolean | 툴이 환경에 영향을 주지 않음을 나타냅니다.                            |
| `#[IsDestructive]` | boolean | 툴이 파괴적인 변경을 수행할 수 있음을 나타냅니다(읽기 전용이 아닐 때 의미 있음). |
| `#[IsIdempotent]`  | boolean | 동일한 인수로 반복 호출해도 추가 효과가 없음을 나타냅니다(읽기 전용이 아닐 때 의미 있음). |
| `#[IsOpenWorld]`   | boolean | 툴이 외부 엔티티와 상호작용할 수 있음을 나타냅니다.                   |

<a name="conditional-tool-registration"></a>
### 툴 조건부 등록

툴 클래스에서 `shouldRegister` 메서드를 구현하여 런타임 조건에 따라 툴의 등록 여부를 동적으로 결정할 수 있습니다. 애플리케이션 상태, 설정, 요청 파라미터 등 다양한 조건에 대응 가능합니다:

```php
<?php

namespace App\Mcp\Tools;

use Laravel\Mcp\Request;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * 툴을 등록할지 여부 결정
     */
    public function shouldRegister(Request $request): bool
    {
        return $request?->user()?->subscribed() ?? false;
    }
}
```

이 메서드가 `false`를 반환하면 해당 툴은 사용 가능 목록에 표시되지 않으며, AI 클라이언트가 호출할 수 없습니다.

<a name="tool-responses"></a>
### 툴 응답

툴은 반드시 `Laravel\Mcp\Response` 인스턴스를 반환해야 합니다. Response 클래스는 다양한 형식의 응답 생성을 위한 여러 메서드를 제공합니다.

단순 텍스트 응답은 `text` 메서드로 반환할 수 있습니다:

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

툴 실행 중 오류가 발생했음을 알릴 때는 `error` 메서드를 사용하세요:

```php
return Response::error('Unable to fetch weather data. Please try again.');
```

#### 다중 콘텐츠 응답

툴이 여러 응답 콘텐츠를 반환해야 할 경우, `Response` 인스턴스 배열을 반환할 수 있습니다:

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

#### 스트리밍 응답

장시간 실행되는 작업이거나 실시간 데이터 스트림이 필요한 경우, `handle` 메서드에서 [제너레이터](https://www.php.net/manual/en/language.generators.overview.php)를 반환할 수 있습니다. 이 방식은 최종 응답 전 중간 상태 업데이트를 실시간으로 클라이언트에 보낼 수 있습니다:

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

웹 서버를 사용할 경우 스트리밍 응답은 자동으로 SSE(Server-Sent Events) 스트림을 열어 각 메시지를 클라이언트에 이벤트로 전송합니다.

<a name="prompts"></a>
## 프롬프트

[프롬프트](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts)는 언어 모델과의 상호작용을 위한 재사용 가능한 프롬프트 템플릿을 서버가 AI 클라이언트에 공유할 수 있도록 해줍니다. 프롬프트를 통해 표준화된 질의 및 상호작용 구조를 정의할 수 있습니다.

<a name="creating-prompts"></a>
### 프롬프트 생성

프롬프트를 생성하려면 `make:mcp-prompt` Artisan 명령어를 실행하세요:

```shell
php artisan make:mcp-prompt DescribeWeatherPrompt
```

프롬프트를 생성한 뒤, 서버의 `$prompts` 속성에 등록하세요:

```php
<?php

namespace App\Mcp\Servers;

use App\Mcp\Prompts\DescribeWeatherPrompt;
use Laravel\Mcp\Server;

class WeatherServer extends Server
{
    /**
     * 이 MCP 서버에 등록된 프롬프트
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Prompt>>
     */
    protected array $prompts = [
        DescribeWeatherPrompt::class,
    ];
}
```

#### 프롬프트 이름, 타이틀, 설명

기본적으로 프롬프트의 이름(name)과 타이틀(title)은 클래스명에서 파생됩니다. 예를 들어, `DescribeWeatherPrompt`의 이름은 `describe-weather`, 타이틀은 `Describe Weather Prompt`가 됩니다. 필요할 경우 `$name`, `$title` 속성을 직접 지정할 수 있습니다:

```php
class DescribeWeatherPrompt extends Prompt
{
    /**
     * 프롬프트의 이름
     */
    protected string $name = 'weather-assistant';

    /**
     * 프롬프트의 타이틀
     */
    protected string $title = 'Weather Assistant Prompt';

    // ...
}
```

프롬프트의 설명(description)은 자동으로 생성되지 않습니다. 항상 의도를 명확히 설명하는 `$description` 속성을 지정해야 합니다:

```php
class DescribeWeatherPrompt extends Prompt
{
    /**
     * 프롬프트의 설명
     */
    protected string $description = 'Generates a natural-language explanation of the weather for a given location.';

    //
}
```

> [!NOTE]
> 설명은 프롬프트 메타데이터에서 매우 중요한 역할을 합니다. AI 모델이 언제, 어떻게 해당 프롬프트를 활용해야 최적의 결과를 받을 수 있는지 이해하도록 도와줍니다.

<a name="prompt-arguments"></a>
### 프롬프트 인수

프롬프트는 AI 클라이언트가 프롬프트 템플릿을 특정 값으로 맞춤화할 수 있도록 인수를 정의할 수 있습니다. 프롬프트에서 인수를 정의하려면 `arguments` 메서드를 활용하세요:

```php
<?php

namespace App\Mcp\Prompts;

use Laravel\Mcp\Server\Prompt;
use Laravel\Mcp\Server\Prompts\Argument;

class DescribeWeatherPrompt extends Prompt
{
    /**
     * 프롬프트의 인수 반환
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

프롬프트 인수는 정의에 따라 자동으로 유효성 검증됩니다. 더 복잡한 검증이 필요하다면, 프롬프트의 `handle` 메서드 내에서 Laravel의 [유효성 검증 기능](/docs/12.x/validation)을 사용할 수 있습니다:

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

        // 주어진 어조로 프롬프트 응답 생성...
    }
}
```

유효성 검증에 실패할 경우 제공한 에러 메시지에 따라 AI 클라이언트의 동작이 달라집니다. 따라서 명확한 메시지를 제공해야 합니다:

```php
$validated = $request->validate([
    'tone' => ['required','string','max:50'],
],[
    'tone.*' => 'You must specify a tone for the weather description. Examples include "formal", "casual", or "humorous".',
]);
```

<a name="prompt-dependency-injection"></a>
### 프롬프트 의존성 주입

모든 프롬프트 역시 Laravel [서비스 컨테이너](/docs/12.x/container)를 통해 해결됩니다. 생성자에 타입힌트로 의존성을 명시하면 자동으로 주입받을 수 있습니다:

```php
<?php

namespace App\Mcp\Prompts;

use App\Repositories\WeatherRepository;
use Laravel\Mcp\Server\Prompt;

class DescribeWeatherPrompt extends Prompt
{
    /**
     * 프롬프트 인스턴스 생성자
     */
    public function __construct(
        protected WeatherRepository $weather,
    ) {}

    //
}
```

또한, 프롬프트의 `handle` 메서드에서도 의존성 타입힌트를 사용해 의존성을 주입받을 수 있습니다:

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

프롬프트 클래스에서 `shouldRegister` 메서드를 구현해 런타임 조건에 따라 프롬프트 등록 여부를 동적으로 제어할 수 있습니다:

```php
<?php

namespace App\Mcp\Prompts;

use Laravel\Mcp\Request;
use Laravel\Mcp\Server\Prompt;

class CurrentWeatherPrompt extends Prompt
{
    /**
     * 프롬프트를 등록할지 여부 결정
     */
    public function shouldRegister(Request $request): bool
    {
        return $request?->user()?->subscribed() ?? false;
    }
}
```

이 메서드가 `false`를 반환하면 해당 프롬프트는 사용 가능 목록에 표시되지 않으며, AI 클라이언트가 호출할 수 없습니다.

<a name="prompt-responses"></a>
### 프롬프트 응답

프롬프트는 단일 `Laravel\Mcp\Response` 또는 여러 `Laravel\Mcp\Response` 인스턴스를 반복자로 반환할 수 있습니다. 이러한 응답은 AI 클라이언트에 전송될 내용을 캡슐화합니다:

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

`asAssistant()` 메서드를 사용하면, 해당 응답 메시지가 AI 어시스턴트로부터 온 것으로 처리되며, 일반 메시지는 사용자 입력으로 취급됩니다.

<a name="resources"></a>
## 리소스

[리소스](https://modelcontextprotocol.io/specification/2025-06-18/server/resources)는 서버가 AI 클라이언트에 읽기 및 컨텍스트 용도로 데이터와 콘텐츠를 노출할 수 있게 합니다. 이는 문서, 구성, 그 외 AI 응답에 참고될 수 있는 정적·동적 정보를 공유하는 방법을 제공합니다.

<a name="creating-resources"></a>
## 리소스 생성

리소스를 생성하려면 `make:mcp-resource` Artisan 명령어를 실행하세요:

```shell
php artisan make:mcp-resource WeatherGuidelinesResource
```

생성 후, 서버의 `$resources` 속성에 리소스를 등록하세요:

```php
<?php

namespace App\Mcp\Servers;

use App\Mcp\Resources\WeatherGuidelinesResource;
use Laravel\Mcp\Server;

class WeatherServer extends Server
{
    /**
     * 이 MCP 서버에 등록된 리소스
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Resource>>
     */
    protected array $resources = [
        WeatherGuidelinesResource::class,
    ];
}
```

#### 리소스 이름, 타이틀, 설명

기본적으로 리소스의 이름(name)과 타이틀(title)은 클래스명에서 파생됩니다. 예를 들어, `WeatherGuidelinesResource`는 이름이 `weather-guidelines`, 타이틀이 `Weather Guidelines Resource`가 됩니다. 필요에 따라 `$name`, `$title` 속성으로 지정할 수 있습니다:

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

리소스의 설명(description) 역시 자동 생성되지 않으므로 직접 `$description` 속성을 정의해야 합니다:

```php
class WeatherGuidelinesResource extends Resource
{
    /**
     * 리소스의 설명
     */
    protected string $description = 'Comprehensive guidelines for using the Weather API.';

    //
}
```

> [!NOTE]
> 리소스 메타데이터의 설명은 AI 모델이 언제, 어떻게 해당 리소스를 활용할지 이해하는 데 매우 중요한 역할을 합니다.

<a name="resource-uri-and-mime-type"></a>
### 리소스 URI 및 MIME 타입

각 리소스는 고유한 URI로 식별되며, AI 클라이언트가 리소스 형식을 이해하는 데 사용할 MIME 타입이 지정됩니다.

기본적으로 리소스의 URI는 이름을 기반으로 생성되므로, 예를 들어 `WeatherGuidelinesResource`는 `weather://resources/weather-guidelines` URI를 가지며, MIME 타입은 기본값이 `text/plain`입니다.

이 값을 변경하려면 `$uri` 및 `$mimeType` 속성을 지정하세요:

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
     * 리소스의 MIME 타입
     */
    protected string $mimeType = 'application/pdf';
}
```

URI와 MIME 타입은 AI 클라이언트가 리소스를 적절히 처리하고 해석하는 데 사용됩니다.

<a name="resource-request"></a>
### 리소스 요청

툴이나 프롬프트와는 달리, 리소스는 입력 스키마나 인수를 정의할 수 없습니다. 하지만 `handle` 메서드 내에서 요청(Request) 객체를 활용할 수 있습니다:

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

모든 리소스 역시 Laravel [서비스 컨테이너](/docs/12.x/container)를 통해 해결됩니다. 생성자의 타입힌트로 필요한 의존성을 선언하면 자동으로 주입받을 수 있습니다:

```php
<?php

namespace App\Mcp\Resources;

use App\Repositories\WeatherRepository;
use Laravel\Mcp\Server\Resource;

class WeatherGuidelinesResource extends Resource
{
    /**
     * 리소스 인스턴스 생성자
     */
    public function __construct(
        protected WeatherRepository $weather,
    ) {}

    // ...
}
```

`handle` 메서드에서도 의존성 타입힌트를 사용할 수 있습니다:

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
### 리소스 조건부 등록

`shouldRegister` 메서드를 리소스 클래스에 구현하면, 런타임에 리소스 등록 여부를 동적으로 제어할 수 있습니다:

```php
<?php

namespace App\Mcp\Resources;

use Laravel\Mcp\Request;
use Laravel\Mcp\Server\Resource;

class WeatherGuidelinesResource extends Resource
{
    /**
     * 리소스를 등록할지 여부 결정
     */
    public function shouldRegister(Request $request): bool
    {
        return $request?->user()?->subscribed() ?? false;
    }
}
```

이 메서드가 `false`를 반환하면, 해당 리소스는 사용 가능 목록에 보여지지 않으며 AI 클라이언트가 접근할 수 없습니다.

<a name="resource-responses"></a>
### 리소스 응답

리소스는 반드시 `Laravel\Mcp\Response` 인스턴스를 반환해야 합니다. Response 클래스는 다양한 응답 타입 생성을 위한 여러 메서드를 제공합니다.

단순 텍스트 콘텐츠는 `text` 메서드를 사용하세요:

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

#### Blob 응답

바이너리(blob) 콘텐츠를 반환하려면, `blob` 메서드를 사용해 바이너리 내용을 전달하세요:

```php
return Response::blob(file_get_contents(storage_path('weather/radar.png')));
```

이때 MIME 타입은 리소스 클래스의 `$mimeType` 속성 값으로 결정됩니다:

```php
<?php

namespace App\Mcp\Resources;

use Laravel\Mcp\Server\Resource;

class WeatherGuidelinesResource extends Resource
{
    /**
     * 리소스의 MIME 타입
     */
    protected string $mimeType = 'image/png';

    //
}
```

#### 오류 응답

리소스 요청 처리 중 오류가 발생했다면, `error()` 메서드를 사용하세요:

```php
return Response::error('Unable to fetch weather data for the specified location.');
```

<a name="authentication"></a>
## 인증

웹 MCP 서버는 라우트와 동일하게 미들웨어로 인증을 적용할 수 있습니다. 즉, MCP 서버의 모든 기능을 사용하려면 사용자가 인증되어야 합니다.

MCP 서버 접근을 인증하는 방법은 크게 두 가지가 있습니다. [Laravel Sanctum](/docs/12.x/sanctum)을 통한 간단한 토큰 기반 인증, 또는 `Authorization` HTTP 헤더를 사용한 직접적인 API 토큰 인증입니다. 또한, [Laravel Passport](/docs/12.x/passport)를 활용해 OAuth 방식 인증도 가능합니다.

<a name="oauth"></a>
### OAuth 2.1

웹 기반 MCP 서버를 보호하는 가장 강력한 방법은 [Laravel Passport](/docs/12.x/passport)를 통한 OAuth 인증입니다.

MCP 서버를 OAuth로 인증하려면, `routes/ai.php` 파일에서 `Mcp::oauthRoutes` 메서드로 필요한 OAuth2 디스커버리 및 클라이언트 등록 라우트를 추가해야 합니다. 이후, `Mcp::web` 라우트에 Passport의 `auth:api` 미들웨어를 적용합니다:

```php
use App\Mcp\Servers\WeatherExample;
use Laravel\Mcp\Facades\Mcp;

Mcp::oauthRoutes();

Mcp::web('/mcp/weather', WeatherExample::class)
    ->middleware('auth:api');
```

#### 신규 Passport 설치

애플리케이션에 아직 Laravel Passport가 설치되어 있지 않다면, Passport의 [설치 및 배포 문서](/docs/12.x/passport#installation)를 따라야 합니다. `OAuthenticatable` 모델, 새로운 인증 가드, passport 키 등을 설정해야 합니다.

다음으로, MCP에서 제공하는 Passport 인가 뷰를 퍼블리시하세요:

```shell
php artisan vendor:publish --tag=mcp-views
```

그 후, Passport에게 이 뷰를 사용하도록 알려야 합니다. 보통 `AppServiceProvider`의 `boot` 메서드에서 아래처럼 작성합니다:

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

이 뷰는 최종 사용자에게 AI 에이전트 인증 시 표시되며, 인증 요청을 승인 또는 거부할 수 있도록 합니다.

![Authorization screen example](data:image/png;base64,iVBORw0KGgo...)

> [!NOTE]
> 이 경우, OAuth는 기본적으로 인증 가능한 모델과의 매핑(translation layer)로만 사용합니다. OAuth의 스코프 등 여러 고급 개념은 따로 다루지 않습니다.

#### 기존 Passport 설치 환경

이미 Passport를 사용 중이라면, MCP는 별도 추가 설정 없이 잘 동작합니다. 단, 커스텀 스코프는 현재 지원하지 않으며, OAuth는 기본적으로 인증 가능한 모델과의 매핑 용도로 사용됩니다.

MCP의 `Mcp::oauthRoutes()` 메서드를 통해 단일 `mcp:use` 스코프만 추가되고 사용됩니다.

#### Passport와 Sanctum 비교

Model Context Protocol 명세에서 공식적으로 표준 인증 방식은 OAuth2.1이며, MCP 클라이언트와 가장 폭넓게 호환됩니다. 가능하다면 Passport 사용을 권장합니다.

한편, 이미 [Sanctum](/docs/12.x/sanctum) 환경이라면 굳이 Passport를 추가하지 않아도 됩니다. 이 경우, 추후 OAuth 전용 MCP 클라이언트를 도입해야 할 필요가 생기기 전까지는 Sanctum만으로 충분합니다.

<a name="sanctum"></a>
### Sanctum

[Sanctum](/docs/12.x/sanctum)으로 MCP 서버를 보호하려면, MCP 서버 라우트에 Sanctum 인증 미들웨어를 추가하세요. MCP 클라이언트는 반드시 `Authorization: Bearer <token>` 헤더를 포함시켜야 인증에 성공합니다:

```php
use App\Mcp\Servers\WeatherExample;
use Laravel\Mcp\Facades\Mcp;

Mcp::web('/mcp/demo', WeatherExample::class)
    ->middleware('auth:sanctum');
```

#### 커스텀 MCP 인증

애플리케이션 자체적으로 커스텀 API 토큰을 발급한다면, `Mcp::web` 라우트에 원하는 미들웨어를 자유롭게 지정해 MCP 서버 인증에 쓰면 됩니다. 커스텀 미들웨어에서는 직접 `Authorization` 헤더를 분석해 인증 처리를 할 수 있습니다.

<a name="authorization"></a>
## 인가

`$request->user()` 메서드로 현재 인증된 사용자를 조회할 수 있습니다. 이를 이용해 MCP 툴이나 리소스에서 [인가(authorization) 검사](/docs/12.x/authorization)를 할 수 있습니다:

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

MCP 서버는 내장 MCP 인스펙터 또는 유닛 테스트로 검증할 수 있습니다.

<a name="mcp-inspector"></a>
### MCP 인스펙터

[MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector)는 MCP 서버 테스트 및 디버깅을 위한 인터랙티브 도구입니다. 인증 설정 검증, 툴/리소스/프롬프트 실행 등을 편리하게 실험할 수 있습니다.

등록된 서버에 대해 인스펙터를 실행하려면:

```shell
# 웹 서버 예시
php artisan mcp:inspector mcp/weather

# "weather"라는 이름의 로컬 서버
php artisan mcp:inspector weather
```

이 명령어는 MCP Inspector를 실행하고, MCP 클라이언트에 연동에 필요한 설정 정보를 제공합니다. 인증 미들웨어가 적용된 경우에는 `Authorization` 토큰 등 필요한 헤더도 함께 전달해야 합니다.

<a name="unit-tests"></a>
### 유닛 테스트

MCP 서버, 툴, 리소스, 프롬프트 모두 유닛 테스트를 작성할 수 있습니다.

먼저 새로운 테스트 케이스를 생성한 후, 테스트 대상 서버에서 원하는 기능을 호출하세요. 예를 들어, `WeatherServer`의 툴을 테스트하는 예시는 아래와 같습니다:

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

마찬가지로 프롬프트, 리소스도 테스트할 수 있습니다:

```php
$response = WeatherServer::prompt(...);
$response = WeatherServer::resource(...);
```

테스트 중 인증된 사용자로 동작하려면, primitive 호출 전에 `actingAs` 메서드를 체이닝하세요:

```php
$response = WeatherServer::actingAs($user)->tool(...);
```

응답을 받은 후에는 다양한 assertion 메서드로 응답의 내용과 상태를 검증할 수 있습니다.

응답이 성공적임을 확인하려면 `assertOk` 메서드를 사용하세요. 이 메서드는 오류가 없는 경우를 확인합니다:

```php
$response->assertOk();
```

응답에 특정 텍스트가 포함되어 있는지 검증하려면 `assertSee` 메서드를 사용하세요:

```php
$response->assertSee('The current weather in New York City is 72°F and sunny.');
```

응답에 오류가 포함되어 있는지 확인하려면 `assertHasErrors` 메서드를 사용하세요:

```php
$response->assertHasErrors();

$response->assertHasErrors([
    'Something went wrong.',
]);
```

응답에 오류가 없음을 검증하려면 `assertHasNoErrors`를 사용하세요:

```php
$response->assertHasNoErrors();
```

특정 메타데이터가 포함되어 있는지도 검증할 수 있습니다:

```php
$response->assertName('current-weather');
$response->assertTitle('Current Weather Tool');
$response->assertDescription('Fetches the current weather forecast for a specified location.');
```

알림(Notification)이 전송됐는지 `assertSentNotification`, 개수를 `assertNotificationCount`로 검증할 수 있습니다:

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

마지막으로 원시 응답을 살펴보고 싶으면, `dd` 또는 `dump` 메서드로 내용을 출력해 디버깅할 수 있습니다:

```php
$response->dd();
$response->dump();
```
