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
    - [조건부 툴 등록](#conditional-tool-registration)
    - [툴 응답](#tool-responses)
- [프롬프트](#prompts)
    - [프롬프트 생성](#creating-prompts)
    - [프롬프트 인수](#prompt-arguments)
    - [프롬프트 인수 유효성 검증](#validating-prompt-arguments)
    - [프롬프트 의존성 주입](#prompt-dependency-injection)
    - [조건부 프롬프트 등록](#conditional-prompt-registration)
    - [프롬프트 응답](#prompt-responses)
- [리소스](#creating-resources)
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
    - [단위 테스트](#unit-tests)

<a name="introduction"></a>
## 소개

[Laravel MCP](https://github.com/laravel/mcp)는 [Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro)을 통해 AI 클라이언트가 여러분의 Laravel 애플리케이션과 간단하고 우아하게 상호작용할 수 있는 기능을 제공합니다. MCP는 서버, 툴, 리소스, 프롬프트 등을 명확하고 직관적인 인터페이스로 정의할 수 있게 하여, AI 기반의 다양한 애플리케이션 통합을 손쉽게 구현할 수 있습니다.

<a name="installation"></a>
## 설치

Composer 패키지 매니저를 사용해 Laravel MCP를 프로젝트에 설치합니다.

```shell
composer require laravel/mcp
```

<a name="publishing-routes"></a>
### 라우트 퍼블리싱

Laravel MCP를 설치한 후, MCP 서버를 정의할 `routes/ai.php` 파일을 퍼블리시하기 위해 `vendor:publish` Artisan 명령어를 실행합니다.

```shell
php artisan vendor:publish --tag=ai-routes
```

이 명령어는 애플리케이션의 `routes` 디렉터리에 `routes/ai.php` 파일을 생성합니다. 이 파일에서 MCP 서버를 등록하게 됩니다.

<a name="creating-servers"></a>
## 서버 생성

`make:mcp-server` Artisan 명령어를 사용하면 MCP 서버를 생성할 수 있습니다. MCP 서버는 툴, 리소스, 프롬프트 등 MCP 기능을 AI 클라이언트에 노출하는 중앙 커뮤니케이션 포인트 역할을 합니다.

```shell
php artisan make:mcp-server WeatherServer
```

이 명령어는 `app/Mcp/Servers` 디렉터리에 새로운 서버 클래스를 생성합니다. 생성된 서버 클래스는 Laravel MCP의 기본 `Laravel\Mcp\Server` 클래스를 확장하며, 툴, 리소스, 프롬프트를 등록할 수 있는 속성을 제공합니다.

```php
<?php

namespace App\Mcp\Servers;

use Laravel\Mcp\Server;

class WeatherServer extends Server
{
    /**
     * 이 MCP 서버에 등록된 툴.
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Tool>>
     */
    protected array $tools = [
        // ExampleTool::class,
    ];

    /**
     * 이 MCP 서버에 등록된 리소스.
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Resource>>
     */
    protected array $resources = [
        // ExampleResource::class,
    ];

    /**
     * 이 MCP 서버에 등록된 프롬프트.
     *
     * @var array<int, class-string<\Laravel\Mcp\Server\Prompt>>
     */
    protected array $prompts = [
        // ExamplePrompt::class,
    ];
}
```

<a name="server-registration"></a>
### 서버 등록

서버를 생성했다면 `routes/ai.php` 파일에서 해당 서버를 등록해 사용 가능하도록 해야 합니다. Laravel MCP는 서버 등록 방법으로 `web`(HTTP로 접근 가능한 서버)과 `local`(명령줄에서 접근하는 서버)를 제공합니다.

<a name="web-servers"></a>
### 웹 서버

웹 서버는 HTTP POST 요청을 통해 접근할 수 있는 가장 일반적인 타입의 서버로, 원격 AI 클라이언트나 웹 기반 통합에 적합합니다. `web` 메서드를 사용해 웹 서버를 등록할 수 있습니다.

```php
use App\Mcp\Servers\WeatherServer;
use Laravel\Mcp\Facades\Mcp;

Mcp::web('/mcp/weather', WeatherServer::class);
```

일반 라우트와 마찬가지로 미들웨어를 적용해 웹 서버를 보호할 수 있습니다.

```php
Mcp::web('/mcp/weather', WeatherServer::class)
    ->middleware(['throttle:mcp']);
```

<a name="local-servers"></a>
### 로컬 서버

로컬 서버는 Artisan 명령어로 실행되는 서버로, 개발, 테스트 또는 로컬 AI 어시스턴트 통합 등에 적합합니다. `local` 메서드를 사용해 로컬 서버를 등록할 수 있습니다.

```php
use App\Mcp\Servers\WeatherServer;
use Laravel\Mcp\Facades\Mcp;

Mcp::local('weather', WeatherServer::class);
```

등록 후에는 일반적으로 직접 `mcp:start`를 실행할 필요 없이, MCP 클라이언트(AI 에이전트)가 서버를 시작하도록 구성해야 합니다. `mcp:start` 명령어는 MCP 클라이언트가 서버의 시작과 종료를 관리하기 위해 사용합니다.

```shell
php artisan mcp:start weather
```

<a name="tools"></a>
## 툴

툴을 통해 서버는 AI 클라이언트가 호출할 수 있는 기능을 제공합니다. 툴을 활용하면 언어 모델이 특정 동작을 실행하거나, 코드 실행, 외부 시스템과의 상호작용을 수행할 수 있습니다.

<a name="creating-tools"></a>
### 툴 생성

툴을 생성하려면 `make:mcp-tool` Artisan 명령어를 사용하세요.

```shell
php artisan make:mcp-tool CurrentWeatherTool
```

툴 생성 후에는 서버의 `$tools` 속성에 등록해야 합니다.

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

#### 툴 이름, 제목, 설명

기본적으로 툴의 이름과 제목은 클래스명을 기반으로 자동 지정됩니다. 예를 들어 `CurrentWeatherTool` 클래스의 이름은 `current-weather`, 제목은 `Current Weather Tool`이 됩니다. 직접 이름과 제목을 지정하려면 `$name`, `$title` 속성을 정의하세요.

```php
class CurrentWeatherTool extends Tool
{
    /**
     * 툴 이름.
     */
    protected string $name = 'get-optimistic-weather';

    /**
     * 툴 제목.
     */
    protected string $title = 'Get Optimistic Weather Forecast';

    // ...
}
```

설명은 자동 생성되지 않으므로, 항상 `$description` 속성에 의미 있는 설명을 입력해야 합니다.

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
> 설명은 툴의 메타데이터에서 매우 중요한 부분이며, AI 모델이 해당 툴의 용도와 사용 시기를 이해하는 데 도움을 줍니다.

<a name="tool-input-schemas"></a>
### 툴 입력 스키마

툴은 입력 스키마(input schema)를 정의해, AI 클라이언트가 전달할 인수의 데이터를 명확하게 규정할 수 있습니다. Laravel의 `Illuminate\JsonSchema\JsonSchema` 빌더를 사용해 툴의 입력 요구사항을 정의합니다.

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

            'units' => $schema->enum(['celsius', 'fahrenheit'])
                ->description('The temperature units to use.')
                ->default('celsius'),
        ];
    }
}
```

<a name="validating-tool-arguments"></a>
### 툴 인수 유효성 검증

JSON 스키마는 인수의 기본 구조만 규정할 뿐, 복잡한 유효성 검증이 필요한 경우가 많습니다.

Laravel MCP는 Laravel의 [유효성 검증 기능](/docs/11.x/validation)과 완벽히 호환됩니다. 툴의 `handle` 메서드 내에서 `validate` 메서드를 사용해 전달된 인수를 검증할 수 있습니다.

```php
<?php

namespace App\Mcp\Tools;

use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * 툴 요청 핸들러.
     */
    public function handle(Request $request): Response
    {
        $validated = $request->validate([
            'location' => 'required|string|max:100',
            'units' => 'in:celsius,fahrenheit',
        ]);

        // 유효성 검증된 인수를 활용해 날씨 데이터를 조회 처리...
    }
}
```

유효성 검증 실패 시, AI 클라이언트는 여러분이 제공한 에러 메시지를 기준으로 행동합니다. 따라서, 명확하고 행동 지침이 포함된 에러 메시지를 작성하는 것이 매우 중요합니다.

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

Laravel의 [서비스 컨테이너](/docs/11.x/container)를 활용하여, 툴에서 필요한 클래스 의존성(예: 리포지토리 등)을 생성자에 타입힌트로 선언하면 자동으로 인스턴스가 주입됩니다.

```php
<?php

namespace App\Mcp\Tools;

use App\Repositories\WeatherRepository;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * 새 툴 인스턴스 생성자.
     */
    public function __construct(
        protected WeatherRepository $weather,
    ) {}

    // ...
}
```

생성자 주입뿐만 아니라, `handle()` 메서드의 인자로도 의존성을 타입힌트로 선언할 수 있습니다. 서비스 컨테이너가 해당 의존성을 자동으로 주입합니다.

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
     * 툴 요청 핸들러.
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

툴 클래스에 [어노테이션](https://modelcontextprotocol.io/specification/2025-06-18/schema#toolannotations)을 지정하여 AI 클라이언트에게 추가적인 메타데이터를 제공할 수 있습니다. 어노테이션은 attribute 형태로 툴 클래스에 부착합니다.

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

사용 가능한 어노테이션 예시는 아래와 같습니다:

| 어노테이션            | 타입    | 설명                                                                               |
| --------------------- | ------- | ---------------------------------------------------------------------------------- |
| `#[IsReadOnly]`       | boolean | 툴이 환경을 변경하지 않음을 나타냅니다.                                             |
| `#[IsDestructive]`    | boolean | 툴이 파괴적인 업데이트를 수행할 수 있음을 나타내며, 읽기 전용이 아닐 때만 의미가 있습니다. |
| `#[IsIdempotent]`     | boolean | 동일한 인수로 반복 호출해도 추가적인 효과가 없는 경우(읽기 전용이 아닐 때 적용).        |
| `#[IsOpenWorld]`      | boolean | 툴이 외부 엔티티와 상호작용할 수 있음을 나타냅니다.                                 |

<a name="conditional-tool-registration"></a>
### 조건부 툴 등록

툴 클래스에서 `shouldRegister` 메서드를 구현하면, 애플리케이션 상태, 설정, 또는 요청 파라미터값에 따라 툴을 동적으로 등록할 수 있습니다.

```php
<?php

namespace App\Mcp\Tools;

use Laravel\Mcp\Request;
use Laravel\Mcp\Server\Tool;

class CurrentWeatherTool extends Tool
{
    /**
     * 툴이 등록되어야 할지 판별.
     */
    public function shouldRegister(Request $request): bool
    {
        return $request?->user()?->subscribed() ?? false;
    }
}
```

`shouldRegister`가 `false`를 반환하면 해당 툴은 AI 클라이언트에 노출되지 않으며 호출도 불가합니다.

<a name="tool-responses"></a>
### 툴 응답

모든 툴은 반드시 `Laravel\Mcp\Response` 인스턴스를 반환해야 합니다. Response 클래스는 다양한 타입의 응답을 생성할 수 있는 여러 메서드를 제공합니다.

텍스트 응답은 `text` 메서드를 사용합니다.

```php
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;

/**
 * 툴 요청 핸들러.
 */
public function handle(Request $request): Response
{
    // ...

    return Response::text('Weather Summary: Sunny, 72°F');
}
```

툴 실행 중 오류가 발생한 경우 `error` 메서드를 사용합니다.

```php
return Response::error('Unable to fetch weather data. Please try again.');
```

#### 다중 콘텐츠 응답

여러 개의 응답을 반환하려면 `Response` 인스턴스의 배열을 반환할 수 있습니다.

```php
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;

/**
 * 툴 요청 핸들러.
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

장시간 소요되거나 실시간 데이터 스트리밍이 필요한 경우, `handle` 메서드에서 [제너레이터](https://www.php.net/manual/en/language.generators.overview.php)를 반환하여 중간 진행 상황이나 결과를 순차적으로 클라이언트에 전송할 수 있습니다.

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
     * 툴 요청 핸들러.
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

웹 기반 서버에서는 스트리밍 응답 시 SSE(Server-Sent Events) 스트림이 자동으로 열려, 각 메시지가 이벤트로 전송됩니다.

<a name="prompts"></a>
## 프롬프트

[프롬프트](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts)는 서버가 AI 클라이언트에게 재사용 가능한 템플릿을 제공하여, 일관된 쿼리와 상호작용 구조를 제공합니다.

<a name="creating-prompts"></a>
### 프롬프트 생성

프롬프트를 생성하려면 `make:mcp-prompt` Artisan 명령어를 사용합니다.

```shell
php artisan make:mcp-prompt DescribeWeatherPrompt
```

생성 후에는 해당 프롬프트를 서버의 `$prompts` 속성에 등록해야 합니다.

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

#### 프롬프트 이름, 제목, 설명

프롬프트의 이름과 제목도 기본적으로 클래스명을 기반으로 자동 생성됩니다(`DescribeWeatherPrompt` → `describe-weather`, `Describe Weather Prompt`). 직접 지정하려면, 프롬프트 클래스의 `$name`, `$title` 속성을 설정하세요.

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

프롬프트 설명도 수동으로 `$description` 속성에 입력해야 하며, 항상 명확한 설명을 제공하는 것이 좋습니다.

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
> 설명은 프롬프트의 메타데이터에서 매우 중요한 역할을 하며, AI 모델이 프롬프트의 용도와 최적 사용 상황을 이해하는 데 도움을 줍니다.

<a name="prompt-arguments"></a>
### 프롬프트 인수

프롬프트는 인수를 정의하여 AI 클라이언트가 템플릿을 원하는 값으로 커스터마이즈할 수 있도록 합니다. `arguments` 메서드를 통해 사용할 인수를 정의합니다.

```php
<?php

namespace App\Mcp\Prompts;

use Laravel\Mcp\Server\Prompt;
use Laravel\Mcp\Server\Prompts\Argument;

class DescribeWeatherPrompt extends Prompt
{
    /**
     * 프롬프트가 받는 인수 정의.
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

프롬프트 인수는 정의한 대로 기본적인 자동 유효성 검증이 실행되지만, 더 복잡한 검증이 필요할 수 있습니다.

Laravel MCP는 Laravel의 [유효성 검증 기능](/docs/11.x/validation)과 연동되므로, 프롬프트의 `handle` 메서드 내에서 추가로 validate할 수 있습니다.

```php
<?php

namespace App\Mcp\Prompts;

use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Prompt;

class DescribeWeatherPrompt extends Prompt
{
    /**
     * 프롬프트 요청 핸들러.
     */
    public function handle(Request $request): Response
    {
        $validated = $request->validate([
            'tone' => 'required|string|max:50',
        ]);

        $tone = $validated['tone'];

        // tone 값을 활용해 프롬프트 응답 생성 ...
    }
}
```

마찬가지로, 명확한 에러 메시지를 별도 지정할 수 있습니다.

```php
$validated = $request->validate([
    'tone' => ['required','string','max:50'],
],[
    'tone.*' => 'You must specify a tone for the weather description. Examples include "formal", "casual", or "humorous".',
]);
```

<a name="prompt-dependency-injection"></a>
### 프롬프트 의존성 주입

프롬프트 인스턴스도 [서비스 컨테이너](/docs/11.x/container)를 통해 생성되므로, 생성자나 메서드 인자에 타입힌트로 의존성을 선언할 수 있습니다.

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

또는 handle 메서드에서 주입 받을 수도 있습니다.

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
     * 프롬프트 요청 핸들러.
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

프롬프트 클래스에서 `shouldRegister` 메서드를 구현해, 애플리케이션 상태, 설정, 요청 파라미터에 따라 프롬프트를 동적으로 등록할 수 있습니다.

```php
<?php

namespace App\Mcp\Prompts;

use Laravel\Mcp\Request;
use Laravel\Mcp\Server\Prompt;

class CurrentWeatherPrompt extends Prompt
{
    /**
     * 프롬프트가 등록되어야 할지 판별.
     */
    public function shouldRegister(Request $request): bool
    {
        return $request?->user()?->subscribed() ?? false;
    }
}
```

`shouldRegister`가 `false`를 반환하면 해당 프롬프트는 AI 클라이언트에 목록으로 표시되지 않고 호출할 수 없습니다.

<a name="prompt-responses"></a>
### 프롬프트 응답

프롬프트는 단일 `Laravel\Mcp\Response` 또는 여러 Response의 iterable을 반환할 수 있습니다. 이 응답에 실제 AI 클라이언트에 전달될 콘텐츠가 담깁니다.

```php
<?php

namespace App\Mcp\Prompts;

use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Prompt;

class DescribeWeatherPrompt extends Prompt
{
    /**
     * 프롬프트 요청 핸들러.
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

`asAssistant()` 메서드는 해당 응답 메시지가 AI 어시스턴트(모델) 메시지임을 나타냅니다. 일반 메시지는 사용자 입력으로 처리됩니다.

<a name="resources"></a>
## 리소스

[리소스](https://modelcontextprotocol.io/specification/2025-06-18/server/resources)는 서버가 데이터와 콘텐츠를 AI 클라이언트에게 제공하여, 언어 모델 상호작용에 컨텍스트로 활용하도록 할 수 있습니다. 이는 문서, 설정, 다양한 데이터를 공유하는 데 활용됩니다.

<a name="creating-resources"></a>
## 리소스 생성

리소스 생성을 위해 `make:mcp-resource` Artisan 명령어를 실행합니다.

```shell
php artisan make:mcp-resource WeatherGuidelinesResource
```

만든 리소스 클래스를 서버의 `$resources` 속성에 등록하세요.

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

#### 리소스 이름, 제목, 설명

리소스의 이름과 제목도 클래스명 기반으로 자동 생성됩니다(`WeatherGuidelinesResource` → `weather-guidelines`, `Weather Guidelines Resource`). 임의로 지정하려면 `$name`, `$title` 속성을 설정하세요.

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

설명은 반드시 `$description` 속성에 의미 있는 내용을 작성하세요.

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
> 설명은 리소스의 메타데이터에서 중요한 역할을 하며, AI 모델이 언제, 어떻게 이 리소스를 활용할지 파악하는 데 도움이 됩니다.

<a name="resource-uri-and-mime-type"></a>
### 리소스 URI 및 MIME 타입

각 리소스는 고유 URI와 MIME 타입을 가집니다. 이를 통해 AI 클라이언트는 해당 리소스가 어떤 포맷의 데이터인지 알 수 있습니다.

기본적으로 URI는 리소스 이름을 기반으로 `weather://resources/weather-guidelines`와 같은 형태로 생성되며, MIME 타입은 `text/plain`입니다.

직접 지정하려면 `$uri`, `$mimeType` 속성을 사용하세요.

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

URI와 MIME 타입은 AI 클라이언트가 리소스 내용을 적절히 해석하고 처리할 수 있도록 도와줍니다.

<a name="resource-request"></a>
### 리소스 요청

툴, 프롬프트와 달리 리소스는 입력 스키마나 인수를 정의할 수 없습니다. 하지만, 리소스의 `handle` 메서드 내에서 요청 객체를 사용해 클라이언트로부터의 정보에 접근 가능한 점은 동일합니다.

```php
<?php

namespace App\Mcp\Resources;

use Laravel\Mcp\Request;
use Laravel\Mcp\Response;
use Laravel\Mcp\Server\Resource;

class WeatherGuidelinesResource extends Resource
{
    /**
     * 리소스 요청 핸들러.
     */
    public function handle(Request $request): Response
    {
        // ...
    }
}
```

<a name="resource-dependency-injection"></a>
### 리소스 의존성 주입

리소스 클래스도 [서비스 컨테이너](/docs/11.x/container)로 생성되기 때문에, 생성자나 메서드에서 타입힌트로 의존성을 선언하여 주입 받을 수 있습니다.

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

handle 메서드의 인자로도 의존성 주입이 가능합니다.

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
     * 리소스 요청 핸들러.
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

리소스 클래스에서 `shouldRegister` 메서드를 구현해, 상태나 설정, 요청값에 따라 리소스를 조건부로 노출할 수 있습니다.

```php
<?php

namespace App\Mcp\Resources;

use Laravel\Mcp\Request;
use Laravel\Mcp\Server\Resource;

class WeatherGuidelinesResource extends Resource
{
    /**
     * 리소스가 등록되어야 할지 판별.
     */
    public function shouldRegister(Request $request): bool
    {
        return $request?->user()?->subscribed() ?? false;
    }
}
```

이 메서드가 `false`를 반환하면 해당 리소스는 AI 클라이언트에 표시되지 않고 호출할 수 없습니다.

<a name="resource-responses"></a>
### 리소스 응답

모든 리소스는 반드시 `Laravel\Mcp\Response` 인스턴스를 반환해야 합니다. Response 클래스의 여러 메서드를 통해 다양한 응답 타입을 지원합니다.

텍스트 콘텐츠는 `text` 메서드를 사용합니다.

```php
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;

/**
 * 리소스 요청 핸들러.
 */
public function handle(Request $request): Response
{
    // ...

    return Response::text($weatherData);
}
```

#### Blob 응답

블롭(이진) 데이터를 전송하려면 `blob` 메서드를 사용해 파일 내용을 전달할 수 있습니다.

```php
return Response::blob(file_get_contents(storage_path('weather/radar.png')));
```

블롭 데이터를 반환할 경우, MIME 타입은 리소스 클래스의 `$mimeType` 값이 사용됩니다.

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

#### 에러 응답

리소스 조회 과정에서 오류가 발생했다면 `error()` 메서드를 사용하세요.

```php
return Response::error('Unable to fetch weather data for the specified location.');
```

<a name="authentication"></a>
## 인증

웹 MCP 서버는 일반적인 라우트와 동일하게 미들웨어를 통해 인증을 적용할 수 있습니다. 서버의 모든 기능 사용 전 인증을 강제할 수 있습니다.

MCP 서버 인증 방법은 두 가지가 있습니다:
1. [Laravel Sanctum](/docs/11.x/sanctum)을 활용한 간단한 토큰 기반 인증
2. `Authorization` HTTP 헤더에 API 토큰을 담는 커스텀 인증, 또는 [Laravel Passport](/docs/11.x/passport)를 활용한 OAuth 인증

<a name="oauth"></a>
### OAuth 2.1

가장 강력하게 MCP 웹 서버를 보호하는 방법은 [Laravel Passport](/docs/11.x/passport)의 OAuth입니다.

OAuth로 서버를 인증하려면, `routes/ai.php`에서 `Mcp::oauthRoutes` 메서드를 호출해 필요한 OAuth2 discovery 및 클라이언트 등록 라우트를 등록하세요. 그런 뒤, `Mcp::web` 라우트에 Passport의 `auth:api` 미들웨어(가드)를 지정합니다.

```php
use App\Mcp\Servers\WeatherExample;
use Laravel\Mcp\Facades\Mcp;

Mcp::oauthRoutes();

Mcp::web('/mcp/weather', WeatherExample::class)
    ->middleware('auth:api');
```

#### Passport 신규 설치

아직 [Laravel Passport](/docs/11.x/passport#installation)를 사용하고 있지 않다면, 공식 문서의 설치 및 배포 과정을 먼저 따라야 합니다. `OAuthenticatable` 모델, 인증 가드 및 Passport 키 파일 등의 세팅이 완료되어야 합니다.

다음으로, Laravel MCP가 제공하는 Passport 인증 뷰를 퍼블리시해야 합니다.

```shell
php artisan vendor:publish --tag=mcp-views
```

이후, `Passport::authorizationView` 메서드를 사용해 Passport에서 이 뷰를 사용하도록 지정합니다. 보통 `AppServiceProvider`의 `boot` 메서드에 입력합니다.

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

이 뷰는 AI 에이전트가 인증을 시도할 때 사용자가 액세스를 승인/거부하는 화면으로 표시됩니다.

![Authorization screen example](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABOAAAAROCAMAAABKc73cAAAA81BMVEX////7+/v4+PgXFxfl5eUKCgr9/f1... (생략))

> [!NOTE]
> 이 시나리오에서는 OAuth를 인증 가능한 모델과의 중계 계층으로만 활용합니다. OAuth의 scope 등 여러 기능은 사용하지 않습니다.

#### 기존 Passport 설치 활용

이미 Laravel Passport를 사용하고 있다면, 별도의 설정 없이 MCP 서버를 기존 환경에 연동할 수 있습니다. 다만, 현재 OAuth는 커스텀 스코프를 지원하지 않으며, 오직 인증 가능한 모델과의 번역 계층으로만 사용됩니다.

Laravel MCP는 위에서 언급한 `Mcp::oauthRoutes()`를 통해 단일 `mcp:use` 스코프만 사용 및 광고합니다.

#### Passport vs. Sanctum

Model Context Protocol에서 공식적으로 권장되는 인증 방식은 OAuth2.1이며, 대부분의 MCP 클라이언트가 지원합니다. 따라서, 가능하다면 Passport 사용을 권장합니다.

이미 [Sanctum](/docs/11.x/sanctum)을 쓰고 있고, Passport 추가가 부담스러운 경우에는 MCP 클라이언트가 OAuth만 지원할 필요성이 명확하지 않다면 당분간 Sanctum만 사용하셔도 무방합니다.

<a name="sanctum"></a>
### Sanctum

[Sanctum](/docs/11.x/sanctum)을 사용해 MCP 서버를 보호하고 싶다면, `routes/ai.php`에서 서버에 Sanctum의 인증 미들웨어를 추가하세요. MCP 클라이언트는 인증 시 반드시 `Authorization: Bearer <token>` 형태의 헤더를 포함해야 합니다.

```php
use App\Mcp\Servers\WeatherExample;
use Laravel\Mcp\Facades\Mcp;

Mcp::web('/mcp/demo', WeatherExample::class)
    ->middleware('auth:sanctum');
```

#### 커스텀 MCP 인증

자체적으로 API 토큰을 발급해 사용하는 애플리케이션의 경우, 원하는 미들웨어를 `Mcp::web` 라우트에 자유롭게 지정할 수 있습니다. 커스텀 미들웨어에서 `Authorization` 헤더를 직접 검사해 인증 처리를 하세요.

<a name="authorization"></a>
## 인가

현재 인증된 사용자는 `$request->user()` 메서드로 가져올 수 있습니다. 이를 활용해 MCP 툴이나 리소스에서 [인가(Authorization) 체크](/docs/11.x/authorization)를 할 수 있습니다.

```php
use Laravel\Mcp\Request;
use Laravel\Mcp\Response;

/**
 * 툴 요청 핸들러.
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

내장된 MCP Inspector 또는 단위 테스트 작성을 통해 MCP 서버를 검증할 수 있습니다.

<a name="mcp-inspector"></a>
### MCP 인스펙터

[MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector)는 MCP 서버의 동작을 테스트하고 디버깅할 수 있는 인터랙티브 도구입니다. 서버에 연결하여 인증을 확인하고, 다양한 툴, 리소스, 프롬프트 기능을 직접 실험할 수 있습니다.

등록된 서버(예: "weather"라는 로컬 서버)에 대해 MCP Inspector를 실행하려면:

```shell
php artisan mcp:inspector weather
```

이 명령어로 MCP Inspector가 실행되며, MCP 클라이언트에 입력 가능한 연결 설정 정보도 표시됩니다. 만약 서버에 인증 미들웨어가 있다면 Authorization 헤더 등 필요한 값을 반드시 포함해 연결해야 합니다.

<a name="unit-tests"></a>
### 단위 테스트

MCP 서버, 툴, 리소스, 프롬프트 등은 모두 단위 테스트를 작성할 수 있습니다.

새 테스트 케이스를 만들고, 해당 MCP 서버에 원하는 프리미티브(tool, prompt, resource 등)를 직접 호출해 결과를 검증할 수 있습니다. 예를 들어 WeatherServer에 등록된 툴을 테스트 하려면 아래와 같이 작성합니다.

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

프롬프트와 리소스도 유사하게 테스트할 수 있습니다.

```php
$response = WeatherServer::prompt(...);
$response = WeatherServer::resource(...);
```

인증된 사용자로 행동하고 싶다면 `actingAs` 체이닝 후 프리미티브를 호출하세요.

```php
$response = WeatherServer::actingAs($user)->tool(...);
```

응답을 받았다면 다음과 같은 다양한 assertion 메서드로 응답 내용과 상태를 검증할 수 있습니다.

- 응답이 성공적인지 확인: `assertOk`
```php
$response->assertOk();
```

- 특정 텍스트가 포함되어 있는지 확인: `assertSee`
```php
$response->assertSee('The current weather in New York City is 72°F and sunny.');
```

- 에러가 포함되어 있는지 확인: `assertHasErrors`
```php
$response->assertHasErrors();

$response->assertHasErrors([
    'Something went wrong.',
]);
```

- 에러가 없음을 확인: `assertHasNoErrors`
```php
$response->assertHasNoErrors();
```

- 응답 메타데이터(이름, 제목, 설명 등) 확인:
```php
$response->assertName('current-weather');
$response->assertTitle('Current Weather Tool');
$response->assertDescription('Fetches the current weather forecast for a specified location.');
```

- 알림(notification)이 전송되었는지 확인:
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

- 원시 응답 내용을 확인하려면 `dd`, `dump` 메서드를 사용해 디버깅할 수 있습니다:
```php
$response->dd();
$response->dump();
```
