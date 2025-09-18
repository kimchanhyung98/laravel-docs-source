# Laravel MCP (Laravel MCP)

- [소개](#introduction)
- [설치](#installation)
    - [라우트 파일 퍼블리싱](#publishing-routes)
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
    - [MCP Inspector](#mcp-inspector)
    - [단위 테스트](#unit-tests)

<a name="introduction"></a>
## 소개

[Laravel MCP](https://github.com/laravel/mcp)는 [Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro)을 통해 AI 클라이언트가 여러분의 Laravel 애플리케이션과 상호작용할 수 있도록 간단하고 우아한 방법을 제공합니다. MCP는 서버, 툴, 리소스, 프롬프트를 정의하기 위한 표현력 있는 플루언트 인터페이스를 제공하여, 애플리케이션에 AI 기반 기능을 쉽게 통합할 수 있습니다.

<a name="installation"></a>
## 설치

시작하려면, Composer 패키지 매니저를 사용해 프로젝트에 Laravel MCP를 설치합니다:

```shell
composer require laravel/mcp
```

<a name="publishing-routes"></a>
### 라우트 파일 퍼블리싱

설치가 완료되면, `vendor:publish` 아티즌 명령어를 실행하여 MCP 서버를 정의할 `routes/ai.php` 파일을 퍼블리싱합니다:

```shell
php artisan vendor:publish --tag=ai-routes
```

이 명령어는 애플리케이션의 `routes` 디렉터리에 `routes/ai.php` 파일을 생성합니다. 이 파일에서 MCP 서버를 등록하게 됩니다.

<a name="creating-servers"></a>
## 서버 생성

MCP 서버는 `make:mcp-server` 아티즌 명령어로 생성할 수 있습니다. 서버는 MCP 기능(툴, 리소스, 프롬프트 등)을 AI 클라이언트에 노출하는 중앙 통신 지점 역할을 합니다:

```shell
php artisan make:mcp-server WeatherServer
```

이 명령어를 실행하면 `app/Mcp/Servers` 디렉터리에 새로운 서버 클래스가 생성됩니다. 이 클래스는 Laravel MCP의 기본 `Laravel\Mcp\Server` 클래스를 확장하며, 툴, 리소스, 프롬프트를 등록하기 위한 속성을 제공합니다:

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

서버를 생성한 후에는 `routes/ai.php` 파일에 서버를 등록해야 접근할 수 있습니다. Laravel MCP는 서버를 등록하는 두 가지 방법을 제공합니다: 웹 서버용 `web`과 명령줄(local) 서버용 `local`입니다.

<a name="web-servers"></a>
### 웹 서버

웹 서버는 가장 일반적으로 사용되는 서버 유형이며, HTTP POST 요청을 통해 접근할 수 있습니다. 원격 AI 클라이언트나 웹 기반 통합에 적합합니다. 웹 서버는 `web` 메서드로 등록할 수 있습니다:

```php
use App\Mcp\Servers\WeatherServer;
use Laravel\Mcp\Facades\Mcp;

Mcp::web('/mcp/weather', WeatherServer::class);
```

일반 라우트와 마찬가지로 미들웨어를 적용하여 웹 서버를 보호할 수 있습니다:

```php
Mcp::web('/mcp/weather', WeatherServer::class)
    ->middleware(['throttle:mcp']);
```

<a name="local-servers"></a>
### 로컬 서버

로컬 서버는 아티즌 명령어로 실행되는 서버로, 개발, 테스트 또는 로컬 AI 비서와의 통합에 적합합니다. 로컬 서버는 `local` 메서드로 등록합니다:

```php
use App\Mcp\Servers\WeatherServer;
use Laravel\Mcp\Facades\Mcp;

Mcp::local('weather', WeatherServer::class);
```

등록 후, 일반적으로 수동으로 `mcp:start` 명령어를 직접 실행할 필요는 없습니다. 대신, MCP 클라이언트(AI 에이전트)가 서버를 시작할 수 있도록 설정해야 합니다. `mcp:start` 명령어는 클라이언트가 필요에 따라 자동으로 서버를 시작하고 중지할 때 사용됩니다:

```shell
php artisan mcp:start weather
```

<a name="tools"></a>
## 툴

툴은 서버가 AI 클라이언트에 기능을 노출할 수 있도록 해줍니다. 이를 통해 언어 모델이 특정 동작을 수행하거나, 코드를 실행하거나, 외부 시스템과 상호작용할 수 있습니다.

<a name="creating-tools"></a>
### 툴 생성

툴을 생성하려면, `make:mcp-tool` 아티즌 명령어를 실행합니다:

```shell
php artisan make:mcp-tool CurrentWeatherTool
```

툴을 생성한 후에는 서버의 `$tools` 속성에 해당 툴을 등록해야 합니다:

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
#### 툴 이름, 타이틀, 설명

기본적으로 툴의 이름(name)과 타이틀(title)은 클래스명을 기반으로 자동으로 생성됩니다. 예를 들어, `CurrentWeatherTool` 클래스는 이름 `current-weather`, 타이틀 `Current Weather Tool`이 됩니다. `$name`, `$title` 속성을 오버라이드하여 커스터마이징할 수 있습니다:

```php
class CurrentWeatherTool extends Tool
{
    /**
     * 툴의 이름.
     */
    protected string $name = 'get-optimistic-weather';

    /**
     * 툴의 타이틀.
     */
    protected string $title = 'Get Optimistic Weather Forecast';

    // ...
}
```

툴의 설명(description)은 자동으로 생성되지 않으므로, 항상 의미 있는 `$description` 속성을 직접 정의해주어야 합니다:

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
> 설명은 툴의 메타데이터에서 매우 중요한 부분입니다. AI 모델이 툴을 어떻게 효율적으로 사용할지 판단하는 데 도움을 주기 때문입니다.

<a name="tool-input-schemas"></a>
### 툴 입력 스키마

툴은 입력 스키마를 정의하여 AI 클라이언트로부터 어떤 인수를 받을지 명세할 수 있습니다. Laravel의 `Illuminate\JsonSchema\JsonSchema` 빌더를 사용해 입력 요건을 정의합니다:

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

JSON 스키마는 기본적인 인수 구조만 제공하므로, 더 복잡한 유효성 검증이 필요하다면 Laravel의 [유효성 검증 기능](/docs/10.x/validation)을 사용할 수 있습니다. 툴의 `handle` 메서드 내에서 유효성 검증을 수행할 수 있습니다:

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

        // validated 인수로 날씨 데이터 조회...
    }
}
```

유효성 검증에 실패할 경우, AI 클라이언트는 제공한 에러 메시지에 따라 동작합니다. 따라서 명확하고 실제로 도움이 되는 에러 메시지를 제공하는 것이 중요합니다:

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

모든 툴 객체는 Laravel [서비스 컨테이너](/docs/10.x/container)에 의해 인스턴스화됩니다. 따라서, 생성자에서 타입힌트를 지정하면 필요한 의존성을 자동으로 주입받을 수 있습니다:

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

생성자 이외에도, `handle()` 메서드의 매개변수에서도 의존성을 타입힌트로 지정하면 서비스 컨테이너가 자동으로 주입해줍니다:

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

툴에 [애너테이션](https://modelcontextprotocol.io/specification/2025-06-18/schema#toolannotations)을 추가하면 AI 클라이언트에 더 많은 메타데이터를 제공할 수 있습니다. 이를 통해 AI 모델이 툴의 동작과 특성을 더 잘 이해할 수 있습니다. 툴 클래스에 애트리뷰트 형태로 애너테이션을 추가합니다:

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

사용 가능한 애너테이션 예시는 아래와 같습니다:

| 애너테이션            | 타입    | 설명                                                                                   |
| --------------------- | ------- | ------------------------------------------------------------------------------------- |
| `#[IsReadOnly]`       | boolean | 환경에 영향을 주지 않는(읽기 전용) 툴임을 나타냅니다.                                 |
| `#[IsDestructive]`    | boolean | 파괴적인(데이터 변경 등) 동작을 수행할 수 있음을 나타냅니다(읽기 전용이 아닐 때 의미 있음). |
| `#[IsIdempotent]`     | boolean | 동일 인수로 여러 번 호출해도 효과가 동일함을 나타냅니다(읽기 전용일 때는 의미 없음).      |
| `#[IsOpenWorld]`      | boolean | 외부 엔티티와 상호작용할 수 있음을 나타냅니다.                                       |

<a name="conditional-tool-registration"></a>
### 조건부 툴 등록

툴 클래스에서 `shouldRegister` 메서드를 구현하면, 애플리케이션 상태, 설정, 요청 파라미터 등에 따라 런타임에 툴의 등록 여부를 동적으로 제어할 수 있습니다:

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

툴의 `shouldRegister`가 `false`를 반환하면, 해당 툴은 목록에 표시되지 않으며 AI 클라이언트로부터 호출될 수 없습니다.

<a name="tool-responses"></a>
### 툴 응답

툴은 반드시 `Laravel\Mcp\Response` 인스턴스를 반환해야 합니다. Response 클래스는 다양한 유형의 응답을 쉽게 생성할 수 있는 메서드를 제공합니다.

텍스트 응답은 `text` 메서드를 사용합니다:

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

툴 실행 중 오류가 발생했음을 알리려면 `error` 메서드를 사용합니다:

```php
return Response::error('Unable to fetch weather data. Please try again.');
```

<a name="multiple-content-responses"></a>
#### 다중 콘텐츠 응답

툴에서 여러 개의 응답 메시지를 반환하려면, `Response` 인스턴스 배열을 반환하면 됩니다:

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

실행 시간이 오래 걸리거나 실시간 데이터를 제공해야 하는 경우, `handle` 메서드에서 [제너레이터](https://www.php.net/manual/en/language.generators.overview.php)를 반환하면 각 업데이트를 순서대로 클라이언트에 전송할 수 있습니다:

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

웹 서버를 사용할 경우, 스트리밍 응답은 자동으로 SSE(Server-Sent Events) 방식으로 클라이언트에 각 메시지를 순차적으로 전송합니다.

<a name="prompts"></a>
## 프롬프트

[프롬프트](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts)는 서버가 AI 클라이언트와 상호작용할 때 공통적으로 활용할 수 있는 프롬프트 템플릿을 제공합니다. 프롬프트는 일관된 쿼리 및 상호작용 구조를 제시하는 표준적인 방법입니다.

<a name="creating-prompts"></a>
### 프롬프트 생성

프롬프트를 생성하려면 `make:mcp-prompt` 아티즌 명령어를 실행합니다:

```shell
php artisan make:mcp-prompt DescribeWeatherPrompt
```

프롬프트를 생성한 후, 서버의 `$prompts` 속성에 해당 프롬프트를 등록합니다:

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
#### 프롬프트 이름, 타이틀, 설명

프롬프트도 기본적으로 클래스명을 기반으로 이름과 타이틀이 자동 생성됩니다. 예를 들어, `DescribeWeatherPrompt`는 `describe-weather`라는 이름과 `Describe Weather Prompt` 타이틀을 갖게 됩니다. `$name`, `$title` 속성을 정의해 커스터마이징할 수 있습니다:

```php
class DescribeWeatherPrompt extends Prompt
{
    /**
     * 프롬프트의 이름.
     */
    protected string $name = 'weather-assistant';

    /**
     * 프롬프트의 타이틀.
     */
    protected string $title = 'Weather Assistant Prompt';

    // ...
}
```

프롬프트의 설명(description)은 자동으로 생성되지 않으므로, `$description` 속성을 직접 지정해야 합니다:

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
> 설명은 프롬프트의 메타데이터에서 매우 중요한 부분입니다. AI 모델이 언제, 어떻게 프롬프트를 효율적으로 사용할지 판단하는 데 도움이 됩니다.

<a name="prompt-arguments"></a>
### 프롬프트 인수

프롬프트는 AI 클라이언트가 특정 값을 프롬프트 템플릿에 전달할 수 있도록 인수를 정의할 수 있습니다. `arguments` 메서드에서 허용할 인수를 정의하세요:

```php
<?php

namespace App\Mcp\Prompts;

use Laravel\Mcp\Server\Prompt;
use Laravel\Mcp\Server\Prompts\Argument;

class DescribeWeatherPrompt extends Prompt
{
    /**
     * 프롬프트의 인수 반환.
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

프롬프트 인수는 정의에 따라 자동으로 유효성 검증이 수행되지만, 추가로 복잡한 검증이 필요하다면 Laravel의 [유효성 검증 기능](/docs/10.x/validation)을 활용할 수 있습니다. 프롬프트의 `handle` 메서드에서 직접 검증을 수행하세요:

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

        // tone을 이용하여 응답 생성...
    }
}
```

유효성 검증이 실패할 경우, AI 클라이언트가 제공된 에러 메시지에 따라 동작하므로 명확하고 친절한 에러 메시지를 작성하는 것이 중요합니다:

```php
$validated = $request->validate([
    'tone' => ['required','string','max:50'],
],[
    'tone.*' => 'You must specify a tone for the weather description. Examples include "formal", "casual", or "humorous".',
]);
```

<a name="prompt-dependency-injection"></a>
### 프롬프트 의존성 주입

프롬프트도 Laravel [서비스 컨테이너](/docs/10.x/container)에 의해 인스턴스화되므로, 생성자 또는 메서드의 타입힌트로 의존성을 주입받을 수 있습니다:

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

`handle` 메서드의 파라미터에도 의존성을 타입힌트로 지정할 수 있습니다:

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

프롬프트 클래스에서 `shouldRegister` 메서드를 구현하면 애플리케이션의 상태, 설정, 요청 파라미터 등에 따라 런타임에 프롬프트의 등록 여부를 동적으로 제어할 수 있습니다:

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

`shouldRegister`가 `false`를 반환하면 해당 프롬프트는 목록에서 보이지 않으며 호출할 수 없습니다.

<a name="prompt-responses"></a>
### 프롬프트 응답

프롬프트는 단일 `Laravel\Mcp\Response` 또는 `Laravel\Mcp\Response` 인스턴스들의 iterable(반복 가능한 값)을 반환할 수 있습니다. 각각의 응답은 AI 클라이언트에 전달될 메시지를 캡슐화합니다:

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

`asAssistant()` 메서드를 사용하면, 해당 응답 메시지가 AI 어시스턴트가 작성한 메시지임을 나타낼 수 있습니다. 별도의 지정이 없으면 일반 메시지는 사용자 입력으로 처리됩니다.

<a name="resources"></a>
## 리소스

[리소스](https://modelcontextprotocol.io/specification/2025-06-18/server/resources)는 서버가 AI 클라이언트에게 데이터 및 컨텍스트를 제공할 수 있게 해줍니다. 문서, 설정 정보, 참고 자료 등 AI의 응답 품질 향상에 도움이 되는 다양한 정적/동적 데이터를 공유할 수 있습니다.

<a name="creating-resources"></a>
## 리소스 생성

리소스를 생성하려면, `make:mcp-resource` 아티즌 명령어를 실행합니다:

```shell
php artisan make:mcp-resource WeatherGuidelinesResource
```

생성한 후에는 서버의 `$resources` 속성에 해당 리소스를 등록합니다:

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
#### 리소스 이름, 타이틀, 설명

리소스의 이름과 타이틀도 기본적으로 클래스명을 기반으로 생성됩니다. 예를 들어, `WeatherGuidelinesResource`는 이름이 `weather-guidelines`, 타이틀이 `Weather Guidelines Resource`가 됩니다. `$name`, `$title` 속성을 오버라이드하여 설정할 수 있습니다:

```php
class WeatherGuidelinesResource extends Resource
{
    /**
     * 리소스의 이름.
     */
    protected string $name = 'weather-api-docs';

    /**
     * 리소스의 타이틀.
     */
    protected string $title = 'Weather API Documentation';

    // ...
}
```

리소스 설명은 자동 생성되지 않으므로, `$description` 속성을 직접 작성해주어야 합니다:

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
> 설명(description)은 리소스 메타데이터에서 핵심 역할을 합니다. AI 모델이 언제, 어떻게 리소스를 사용할지 결정하는 데 도움이 됩니다.

<a name="resource-uri-and-mime-type"></a>
### 리소스 URI 및 MIME 타입

각 리소스는 고유한 URI와 MIME 타입을 가집니다. 이를 통해 AI 클라이언트는 리소스의 형식과 목적을 올바르게 파악하여 처리할 수 있습니다.

기본적으로 리소스의 URI는 클래스명 기준으로 자동 생성되며, MIME 타입은 기본값 `text/plain`입니다. 필요하다면 `$uri`, `$mimeType` 속성으로 값 변경이 가능합니다:

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

URI와 MIME 타입을 통해 AI 클라이언트는 리소스의 내용을 적절히 해석·처리할 수 있습니다.

<a name="resource-request"></a>
### 리소스 요청

툴이나 프롬프트와 달리, 리소스는 입력 스키마나 인수를 정의할 수 없습니다. 하지만 `handle` 메서드 내에서는 요청(Request) 객체와 상호작용할 수 있습니다:

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

리소스 객체도 Laravel [서비스 컨테이너](/docs/10.x/container)를 통해 생성되므로, 생성자나 메서드에서 타입힌트로 필요한 의존성을 선언할 수 있습니다:

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

`handle` 메서드에서도 타입힌트로 의존성을 주입받을 수 있습니다:

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
### 조건부 리소스 등록

리소스 클래스에서 `shouldRegister` 메서드를 구현하면 요청/상태/설정에 따라 런타임에 동적으로 리소스 등록 여부를 제어할 수 있습니다:

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

`shouldRegister`가 `false`를 반환하면 해당 리소스는 사용할 수 없습니다.

<a name="resource-responses"></a>
### 리소스 응답

리소스도 반드시 `Laravel\Mcp\Response` 인스턴스를 반환해야 합니다. 간단한 텍스트 응답은 `text` 메서드를 이용하세요:

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

Blob(이진 데이터) 콘텐츠 반환이 필요하다면, `blob` 메서드를 사용하세요:

```php
return Response::blob(file_get_contents(storage_path('weather/radar.png')));
```

Blob 응답의 MIME 타입은 리소스 클래스의 `$mimeType` 속성값을 따릅니다:

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

리소스 조회 중 오류가 발생했다면, `error()` 메서드를 사용해 알릴 수 있습니다:

```php
return Response::error('Unable to fetch weather data for the specified location.');
```

<a name="authentication"></a>
## 인증

웹 MCP 서버는 일반 라우트처럼 미들웨어를 사용해 인증을 적용할 수 있습니다. 사용자는 MCP 서버의 모든 기능을 이용하기 전에 인증을 완료해야 합니다.

MCP 서버 인증 방법은 두 가지가 있습니다. [Laravel Sanctum](/docs/10.x/sanctum)을 통한 간단한 토큰 인증 방식, 또는 임의의 API 토큰(Authorization HTTP 헤더를 통해 전달) 방식입니다. 또한, [Laravel Passport](/docs/10.x/passport)를 사용한 OAuth 인증도 지원합니다.

<a name="oauth"></a>
### OAuth 2.1

웹 기반 MCP 서버를 보호하는 가장 견고한 방법은 [Laravel Passport](/docs/10.x/passport)를 통한 OAuth 인증입니다.

MCP 서버를 OAuth로 보호하려면 `routes/ai.php`에 `Mcp::oauthRoutes`를 호출해 필요한 OAuth2 디스커버리 및 클라이언트 등록 라우트를 등록하세요. 그리고, `Mcp::web` 라우트에 Passport의 `auth:api` 미들웨어를 적용합니다:

```php
use App\Mcp\Servers\WeatherExample;
use Laravel\Mcp\Facades\Mcp;

Mcp::oauthRoutes();

Mcp::web('/mcp/weather', WeatherExample::class)
    ->middleware('auth:api');
```

#### Passport 신규 설치 시

Laravel Passport를 아직 사용하지 않는 경우, [Passport 설치 및 배포 가이드](/docs/10.x/passport#installation)를 먼저 따라 주세요. 즉, `OAuthenticatable` 모델, 새로운 인증 가드, passport 키 등을 준비해야 합니다.

다음으로, MCP에서 제공하는 Passport 인증 뷰를 퍼블리싱합니다:

```shell
php artisan vendor:publish --tag=mcp-views
```

그 후, Passport의 인증 화면을 커스텀 뷰로 지정합니다. 일반적으로 `AppServiceProvider`의 `boot` 메서드에서 아래처럼 설정합니다:

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

이 뷰는 사용자가 인증 요청을 승인 또는 거부할 때 보여지게 됩니다.

![Authorization screen example](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABOAAAAROCAMAAABKc73cAAAA81BMVEX////7+/v4+PgXFxfl5eUKCgr9/f1zc3P29vby8vLs7Ozj4+Pp6env7++RkZF5eXlRUVF9fX2Li4uEhISOjo4bGxt0dHS0tLTd3d12dnbLy8vW1tapqanFxcVMTEygoKDDw8PIyMgODg7BwcGwsLASEhKbm5uBgYFGRkbh4eHf398gICCXl5fS0tLR0dG6urolJSXPz8+Tk5MVFRVbW1va2tq4uLijo6NnZ2eZmZnNzc02NjZWVlaIiIhAQEClpaUuLi6enp6Hh4e2trZsbGzY2NjU1NStra28vLwyMjJjY2MpKSmVlZVfX187Ozu+vr5OTk7PbglOAABlU0lEQVR42uzBgQAAAACAoP2pF6kCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGB27Ci3QRiIoqiNkGWQvf/tFlNKE5VG+R1yjncwUq5eAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAwilAKIn325Y8zwv1VO7NuplvEFEqSeNeOeKWgYDKJkncy7zlwwSEkQ8S958zb3Xprc1AIK31peaNb3FXyjCG27LOQEjrMknclZKOvLX9SjW7DwRSct23SdsTp3DPjvlW2zhQTkBAeQyUVhXucr9NfeQtAWGNxPVJ4f7ut2ndLuMmEFrp87wq3IOSfvpmvkF4i8I9OfdbTUB49btwArcrafSt6xvcxFa4rnCP+23x/xRuY/yeFe53wNU29wTcRJ9bFbhzwG3n+PhLwH18sW8HNw4CURQEsYXQgMb5p7uGFQ6iqQrBh9b7jLxNR+pvwL3HdKBCyb7O8Ra4a8CNzzoXIGSuH0eqAQdNJtzpfkL1/1NIef0/pD47cPeFeixAyuFGvRbcexwuVKjZ1+PxN+p2Bm6f/sQANWOdu8C9XsMnOOg5P8KNh3+EuwP35N8AkjaB2+7ALUDMN3APf2XYFoGDKIG73hgEDoq+gXv4M+q2CBxECZwFB1kCZ8FBlsBZcJAlcBYcZAmcBQdZAmfBQZbAWXCQJXAWHGQJnAUHWQJnwUGWwFlwkCVwFhxkCZwFB1kCZ8FBlsBZcJAlcBYcZAmcBQdZAmfBQZbAWXCQJXAWHGQJnAUHWQJnwUGWwFlwkCVwFhxkCZwFB1kCZ8FBlsBZcJAlcBYcZAmcBQdZAmfBQZbAWXCQJXAWHQ/2c5Al/Olc1QAAAABJRU5ErkJggg==)

> [!NOTE]
> 이 시나리오에서는 OAuth의 다양한 기능 중 “인증 가능 모델로의 변환 계층(translation layer)” 역할만 사용합니다. 스코프 같은 OAuth의 수많은 고급 기능은 무시합니다.

#### 기존 Passport 사용 중인 경우

이미 Laravel Passport를 사용 중이라면 MCP는 별도의 설정 없이 기존 Passport 환경에서 동작합니다. 다만, OAuth를 인증 가능 모델 변환 계층으로 사용하므로 커스텀 스코프는 현재 지원되지 않습니다.

MCP의 `Mcp::oauthRoutes()` 메서드를 통해 `mcp:use`라는 단일 스코프만 추가·활용됩니다.

#### Passport vs. Sanctum

OAuth2.1은 Model Context Protocol 명세의 공식 인증 메커니즘이자, 대부분의 MCP 클라이언트에서 가장 널리 지원하는 방식입니다. 따라서 가능하다면 Passport 사용을 권장합니다.

이미 [Sanctum](/docs/10.x/sanctum)으로 인증하고 있다면, 굳이 Passport를 추가하지 않아도 됩니다. 이런 경우, 특별히 OAuth만 지원하는 MCP 클라이언트를 써야 하는 명확한 사유가 생기기 전까지는 Sanctum을 그대로 사용하는 것이 더 편리합니다.

<a name="sanctum"></a>
### Sanctum

[Sanctum](/docs/10.x/sanctum)으로 MCP 서버를 보호하려면, `routes/ai.php`에서 해당 서버 라우트에 Sanctum 인증 미들웨어를 지정하기만 하면 됩니다. 이후 MCP 클라이언트에서 `Authorization: Bearer <token>` 헤더만 제공하면 인증이 정상적으로 처리됩니다:

```php
use App\Mcp\Servers\WeatherExample;
use Laravel\Mcp\Facades\Mcp;

Mcp::web('/mcp/demo', WeatherExample::class)
    ->middleware('auth:sanctum');
```

<a name="custom-mcp-authentication"></a>
#### 커스텀 MCP 인증

애플리케이션에서 자체적으로 API 토큰을 발급한다면, 원하는 어떤 미들웨어든 `Mcp::web` 라우트에 자유롭게 지정할 수 있습니다. 커스텀 미들웨어 내부에서 `Authorization` 헤더를 직접 파싱해 MCP 요청의 인증을 수행하면 됩니다.

<a name="authorization"></a>
## 인가

현재 인증된 사용자는 `$request->user()` 메서드로 접근할 수 있습니다. 이를 활용해 MCP의 툴이나 리소스 내부에서 [인가 체크](/docs/10.x/authorization)를 수행할 수 있습니다:

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

MCP 서버는 내장된 MCP Inspector 또는 일반적인 단위 테스트로 검증할 수 있습니다.

<a name="mcp-inspector"></a>
### MCP Inspector

[MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector)는 MCP 서버 테스트와 디버깅을 위한 대화형 도구입니다. 서버와 연결하여 인증을 검증하고, 각종 툴, 리소스, 프롬프트를 시험해 볼 수 있습니다.

등록된 서버(예: "weather"라는 로컬 서버)를 인스펙터로 실행하려면 아래 명령어를 사용합니다:

```shell
php artisan mcp:inspector weather
```

실행하면 MCP Inspector가 시작되고, MCP 클라이언트 설정값 복사 등에 활용할 수 있는 정보를 제공합니다. 웹 서버가 인증 미들웨어로 보호되는 경우, Inspector에서 연결 시 헤더(예: Authorization bearer 토큰)를 추가로 입력해야 정상적으로 테스트할 수 있습니다.

<a name="unit-tests"></a>
### 단위 테스트

MCP 서버, 툴, 리소스, 프롬프트 각각에 대해 일반적인 단위 테스트를 작성할 수 있습니다.

먼저 테스트 케이스를 생성한 뒤, 테스트하려는 MCP 원시기능(Primitive)을 직접 호출하세요. 예를 들어, `WeatherServer`의 툴 테스트는 아래와 같이 작성할 수 있습니다:

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

이와 비슷하게, 프롬프트, 리소스 테스트도 가능합니다:

```php
$response = WeatherServer::prompt(...);
$response = WeatherServer::resource(...);
```

인증된 사용자로 동작시키고 싶을 때는, `actingAs` 메서드를 체이닝하여 사용할 수 있습니다:

```php
$response = WeatherServer::actingAs($user)->tool(...);
```

응답을 받은 후에는 다양한 assertion 메서드로 응답의 내용과 상태를 검증할 수 있습니다.

응답이 성공적인지 확인하려면, `assertOk` 메서드를 사용합니다. 이 메서드는 에러가 없는 응답임을 검증합니다:

```php
$response->assertOk();
```

응답에 특정 텍스트가 포함되어 있는지 확인하려면 `assertSee` 메서드를 사용합니다:

```php
$response->assertSee('The current weather in New York City is 72°F and sunny.');
```

응답에 에러가 포함되어 있는지 여부는 `assertHasErrors`로 검증합니다:

```php
$response->assertHasErrors();

$response->assertHasErrors([
    'Something went wrong.',
]);
```

응답에 에러가 없는지 검증하려면 `assertHasNoErrors`를 사용하세요:

```php
$response->assertHasNoErrors();
```

응답의 메타데이터(이름, 타이틀, 설명 등)는 `assertName()`, `assertTitle()`, `assertDescription()` 메서드로 검증할 수 있습니다:

```php
$response->assertName('current-weather');
$response->assertTitle('Current Weather Tool');
$response->assertDescription('Fetches the current weather forecast for a specified location.');
```

알림(Notification)이 전송되었는지 확인할 때는 `assertSentNotification` 및 `assertNotificationCount` 메서드를 사용합니다:

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

마지막으로, 응답의 원시(raw) 내용을 상세히 살펴보고 싶다면, `dd`나 `dump` 메서드로 출력하여 디버깅할 수 있습니다:

```php
$response->dd();
$response->dump();
```