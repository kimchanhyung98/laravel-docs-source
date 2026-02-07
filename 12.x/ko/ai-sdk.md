# Laravel AI SDK (Laravel AI SDK)

- [소개](#introduction)
- [설치](#installation)
    - [설정](#configuration)
    - [커스텀 베이스 URL](#custom-base-urls)
    - [프로바이더 지원](#provider-support)
- [에이전트](#agents)
    - [프롬프트 전달](#prompting)
    - [대화 컨텍스트](#conversation-context)
    - [구조화된 출력](#structured-output)
    - [첨부파일](#attachments)
    - [스트리밍](#streaming)
    - [브로드캐스팅](#broadcasting)
    - [큐 처리](#queueing)
    - [툴](#tools)
    - [프로바이더 툴](#provider-tools)
    - [미들웨어](#middleware)
    - [익명 에이전트](#anonymous-agents)
    - [에이전트 설정](#agent-configuration)
- [이미지](#images)
- [오디오(TTS)](#audio)
- [트랜스크립션(STT)](#transcription)
- [임베딩](#embeddings)
    - [임베딩 질의](#querying-embeddings)
    - [임베딩 캐싱](#caching-embeddings)
- [리랭킹](#reranking)
- [파일](#files)
- [벡터 스토어](#vector-stores)
    - [스토어에 파일 추가](#adding-files-to-stores)
- [페일오버](#failover)
- [테스트](#testing)
    - [에이전트](#testing-agents)
    - [이미지](#testing-images)
    - [오디오](#testing-audio)
    - [트랜스크립션](#testing-transcriptions)
    - [임베딩](#testing-embeddings)
    - [리랭킹](#testing-reranking)
    - [파일](#testing-files)
    - [벡터 스토어](#testing-vector-stores)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

[Laravel AI SDK](https://github.com/laravel/ai)는 OpenAI, Anthropic, Gemini 등 다양한 AI 프로바이더와 상호작용할 수 있는 통합적이고 표현력이 뛰어난 API를 제공합니다. AI SDK를 활용하면 도구와 구조화된 출력을 갖춘 지능형 에이전트 개발, 이미지 생성, 오디오 합성 및 트랜스크립션, 벡터 임베딩 생성 등 다양한 기능을 일관적이고 Laravel 친화적인 인터페이스로 구현할 수 있습니다.

<a name="installation"></a>
## 설치

Composer를 사용하여 Laravel AI SDK를 설치할 수 있습니다:

```shell
composer require laravel/ai
```

그 다음, `vendor:publish` Artisan 명령어를 사용하여 AI SDK의 설정 파일과 마이그레이션 파일을 배포하십시오:

```shell
php artisan vendor:publish --provider="Laravel\Ai\AiServiceProvider"
```

마지막으로, 애플리케이션의 데이터베이스 마이그레이션을 실행합니다. 이를 통해 AI SDK가 대화 저장을 위해 사용하는 `agent_conversations` 및 `agent_conversation_messages` 테이블이 생성됩니다:

```shell
php artisan migrate
```

<a name="configuration"></a>
### 설정

애플리케이션의 `config/ai.php` 설정 파일 혹은 `.env` 파일의 환경 변수로 AI 프로바이더 자격 증명을 정의할 수 있습니다:

```ini
ANTHROPIC_API_KEY=
COHERE_API_KEY=
ELEVENLABS_API_KEY=
GEMINI_API_KEY=
MISTRAL_API_KEY=
OLLAMA_API_KEY=
OPENAI_API_KEY=
JINA_API_KEY=
VOYAGEAI_API_KEY=
XAI_API_KEY=
```

텍스트, 이미지, 오디오, 트랜스크립션, 임베딩에 사용되는 기본 모델은 `config/ai.php` 설정 파일에서 변경할 수 있습니다.

<a name="custom-base-urls"></a>
### 커스텀 베이스 URL

기본적으로 Laravel AI SDK는 각 프로바이더의 공개 API 엔드포인트에 직접 연결합니다. 다만, API 키 관리의 중앙화, 레이트 리미트 구현, 또는 사내 게이트웨이 통과 등과 같이 다른 엔드포인트를 통해 요청을 처리해야 할 수도 있습니다.

이 경우, 프로바이더 설정에 `url` 파라미터를 추가하여 커스텀 베이스 URL을 지정할 수 있습니다:

```php
'providers' => [
    'openai' => [
        'driver' => 'openai',
        'key' => env('OPENAI_API_KEY'),
        'url' => env('OPENAI_BASE_URL'),
    ],

    'anthropic' => [
        'driver' => 'anthropic',
        'key' => env('ANTHROPIC_API_KEY'),
        'url' => env('ANTHROPIC_BASE_URL'),
    ],
],
```

이는 LiteLLM이나 Azure OpenAI Gateway와 같은 프록시 서비스를 사용할 때 또는 대체 엔드포인트를 사용할 때 유용합니다.

커스텀 베이스 URL은 다음 프로바이더에서 지원됩니다: OpenAI, Anthropic, Gemini, Groq, Cohere, DeepSeek, xAI, OpenRouter.

<a name="provider-support"></a>
### 프로바이더 지원

AI SDK는 각 기능별로 다양한 프로바이더를 지원합니다. 아래 표는 기능별 지원 프로바이더를 요약한 것입니다:

| 기능         | 프로바이더 |
|--------------|-----------|
| 텍스트       | OpenAI, Anthropic, Gemini, Groq, xAI, DeepSeek, Mistral, Ollama |
| 이미지       | OpenAI, Gemini, xAI |
| TTS          | OpenAI, ElevenLabs |
| STT          | OpenAI, ElevenLabs, Mistral |
| 임베딩       | OpenAI, Gemini, Cohere, Mistral, Jina, VoyageAI |
| 리랭킹       | Cohere, Jina |
| 파일         | OpenAI, Anthropic, Gemini |

<a name="agents"></a>
## 에이전트

에이전트는 Laravel AI SDK에서 AI 프로바이더와 상호작용할 때의 기본 단위입니다. 각 에이전트는 PHP 클래스로, 대형 언어 모델과 상호작용하기 위해 필요한 지침, 대화 컨텍스트, 도구, 출력 스키마 등을 캡슐화합니다. 쉽게 말해, 한 번 구성해두면 애플리케이션 전체에 걸쳐 반복적으로 활용 가능한 "전문 상담사" 또는 "특화된 조수"와 같습니다. 예를 들어, 영업 코치, 문서 분석가, 고객 지원 봇 등이 될 수 있습니다.

에이전트는 `make:agent` Artisan 명령어로 생성할 수 있습니다:

```shell
php artisan make:agent SalesCoach

php artisan make:agent SalesCoach --structured
```

생성된 에이전트 클래스 내에서는 시스템 프롬프트/지침, 메시지 컨텍스트, 사용 가능한 도구, (필요하다면) 출력 스키마 등을 정의할 수 있습니다:

```php
<?php

namespace App\Ai\Agents;

use App\Ai\Tools\RetrievePreviousTranscripts;
use App\Models\History;
use App\Models\User;
use Illuminate\Contracts\JsonSchema\JsonSchema;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Contracts\Conversational;
use Laravel\Ai\Contracts\HasStructuredOutput;
use Laravel\Ai\Contracts\HasTools;
use Laravel\Ai\Promptable;
use Stringable;

class SalesCoach implements Agent, Conversational, HasTools, HasStructuredOutput
{
    use Promptable;

    public function __construct(public User $user) {}

    /**
     * 에이전트가 따라야 할 지침 반환
     */
    public function instructions(): Stringable|string
    {
        return 'You are a sales coach, analyzing transcripts and providing feedback and an overall sales strength score.';
    }

    /**
     * 현재까지의 대화 메시지 목록 반환
     */
    public function messages(): iterable
    {
        return History::where('user_id', $this->user->id)
            ->latest()
            ->limit(50)
            ->get()
            ->reverse()
            ->map(function ($message) {
                return new Message($message->role, $message->content);
            })->all();
    }

    /**
     * 에이전트가 사용할 수 있는 도구 목록 반환
     *
     * @return Tool[]
     */
    public function tools(): iterable
    {
        return [
            new RetrievePreviousTranscripts,
        ];
    }

    /**
     * 에이전트의 구조화된 출력 스키마 반환
     */
    public function schema(JsonSchema $schema): array
    {
        return [
            'feedback' => $schema->string()->required(),
            'score' => $schema->integer()->min(1)->max(10)->required(),
        ];
    }
}
```

<a name="prompting"></a>
### 프롬프트 전달

에이전트를 프롬프트할 때에는, `make` 메서드나 일반 인스턴스 생성을 이용하여 객체를 생성한 뒤 `prompt`를 호출하면 됩니다:

```php
$response = (new SalesCoach)
    ->prompt('Analyze this sales transcript...');

$response = SalesCoach::make()
    ->prompt('Analyze this sales transcript...');

return (string) $response;
```

`make` 메서드는 에이전트를 컨테이너에서 해석하여 자동 의존성 주입을 적용합니다. 생성자의 인자를 함께 전달할 수도 있습니다:

```php
$agent = SalesCoach::make(user: $user);
```

또한, `prompt` 메서드에 추가 인수를 전달하여 프롬프트할 때 기본 프로바이더, 모델, HTTP 타임아웃을 오버라이드할 수 있습니다:

```php
$response = (new SalesCoach)->prompt(
    'Analyze this sales transcript...',
    provider: 'anthropic',
    model: 'claude-haiku-4-5-20251001',
    timeout: 120,
);
```

<a name="conversation-context"></a>
### 대화 컨텍스트

에이전트가 `Conversational` 인터페이스를 구현하는 경우, `messages` 메서드를 사용하여 이전 대화 컨텍스트(대화 이력)를 반환할 수 있습니다:

```php
use App\Models\History;
use Laravel\Ai\Messages\Message;

/**
 * 현재까지의 대화 메시지 목록 반환
 */
public function messages(): iterable
{
    return History::where('user_id', $this->user->id)
        ->latest()
        ->limit(50)
        ->get()
        ->reverse()
        ->map(function ($message) {
            return new Message($message->role, $message->content);
        })->all();
}
```

<a name="remembering-conversations"></a>
#### 대화 내용 자동 저장

> **Note:** `RemembersConversations` 트레잇을 사용하기 전에, `vendor:publish` Artisan 명령으로 AI SDK 마이그레이션을 실행해야 합니다. 이 과정에서 필요한 데이터베이스 테이블이 생성됩니다.

Laravel이 에이전트의 대화 이력을 자동으로 저장 및 불러오도록 하려면 `RemembersConversations` 트레잇을 사용할 수 있습니다. 이 트레잇은 `Conversational` 인터페이스를 직접 구현하지 않아도 대화 메시지를 데이터베이스에 간편하게 저장할 수 있게 해줍니다:

```php
<?php

namespace App\Ai\Agents;

use Laravel\Ai\Concerns\RemembersConversations;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Contracts\Conversational;
use Laravel\Ai\Promptable;

class SalesCoach implements Agent, Conversational
{
    use Promptable, RemembersConversations;

    /**
     * 에이전트가 따라야 할 지침 반환
     */
    public function instructions(): string
    {
        return 'You are a sales coach...';
    }
}
```

사용자별로 새 대화를 시작하려면, 프롬프트 전에 `forUser` 메서드를 호출하세요:

```php
$response = (new SalesCoach)->forUser($user)->prompt('Hello!');

$conversationId = $response->conversationId;
```

대화 ID는 응답에 포함되어 반환되며, 이를 저장해 두거나 `agent_conversations` 테이블에서 특정 사용자의 모든 대화를 직접 조회할 수 있습니다.

기존 대화를 이어가려면 `continue` 메서드를 사용합니다:

```php
$response = (new SalesCoach)
    ->continue($conversationId, as: $user)
    ->prompt('Tell me more about that.');
```

`RemembersConversations` 트레잇을 사용할 경우, 이전 메시지가 자동으로 불러와져 대화 컨텍스트에 포함되며, 각 상호작용마다 새로운 메시지가 자동으로 저장됩니다.

<a name="structured-output"></a>
### 구조화된 출력

에이전트가 구조화된 출력을 반환하도록 하려면, `HasStructuredOutput` 인터페이스를 구현하여 `schema` 메서드를 정의해야 합니다:

```php
<?php

namespace App\Ai\Agents;

use Illuminate\Contracts\JsonSchema\JsonSchema;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Contracts\HasStructuredOutput;
use Laravel\Ai\Promptable;

class SalesCoach implements Agent, HasStructuredOutput
{
    use Promptable;

    // ...

    /**
     * 에이전트의 구조화된 출력 스키마 반환
     */
    public function schema(JsonSchema $schema): array
    {
        return [
            'score' => $schema->integer()->required(),
        ];
    }
}
```

구조화된 출력을 반환하는 에이전트에 프롬프트를 전달하면, 반환되는 `StructuredAgentResponse`를 배열처럼 접근할 수 있습니다:

```php
$response = (new SalesCoach)->prompt('Analyze this sales transcript...');

return $response['score'];
```

<a name="attachments"></a>
### 첨부파일

프롬프트할 때 이미지나 문서 등 첨부파일을 함께 전달할 수 있습니다. 이를 통해 모델이 첨부된 파일을 분석하도록 할 수 있습니다:

```php
use App\Ai\Agents\SalesCoach;
use Laravel\Ai\Files;

$response = (new SalesCoach)->prompt(
    'Analyze the attached sales transcript...',
    attachments: [
        Files\Document::fromStorage('transcript.pdf'), // 파일시스템에 저장된 문서 첨부
        Files\Document::fromPath('/home/laravel/transcript.md'), // 로컬 경로 첨부
        $request->file('transcript'), // 업로드된 파일 첨부
    ]
);
```

마찬가지로, `Laravel\Ai\Files\Image` 클래스를 사용하여 프롬프트에 이미지를 첨부할 수 있습니다:

```php
use App\Ai\Agents\ImageAnalyzer;
use Laravel\Ai\Files;

$response = (new ImageAnalyzer)->prompt(
    'What is in this image?',
    attachments: [
        Files\Image::fromStorage('photo.jpg'),
        Files\Image::fromPath('/home/laravel/photo.jpg'),
        $request->file('photo'),
    ]
);
```

<a name="streaming"></a>
### 스트리밍

에이전트의 응답을 스트리밍 방식으로 처리하려면 `stream` 메서드를 호출할 수 있습니다. 반환되는 `StreamableAgentResponse`를 라우트에서 직접 반환하면 SSE(서버 전송 이벤트) 방식 스트리밍이 자동 처리됩니다:

```php
use App\Ai\Agents\SalesCoach;

Route::get('/coach', function () {
    return (new SalesCoach)->stream('Analyze this sales transcript...');
});
```

응답이 모두 스트리밍된 후 추가 작업을 하려면 `then` 메서드를 사용할 수 있습니다:

```php
use App\Ai\Agents\SalesCoach;
use Laravel\Ai\Responses\StreamedAgentResponse;

Route::get('/coach', function () {
    return (new SalesCoach)
        ->stream('Analyze this sales transcript...')
        ->then(function (StreamedAgentResponse $response) {
            // $response->text, $response->events, $response->usage 등 사용 가능
        });
});
```

또는, 스트림에서 각 이벤트를 수동으로 순회할 수도 있습니다:

```php
$stream = (new SalesCoach)->stream('Analyze this sales transcript...');

foreach ($stream as $event) {
    // ...
}
```

<a name="streaming-using-the-vercel-ai-sdk-protocol"></a>
#### Vercel AI SDK 프로토콜 스트리밍

[Vercel AI SDK 스트림 프로토콜](https://ai-sdk.dev/docs/ai-sdk-ui/stream-protocol)을 사용해 이벤트를 스트리밍하려면, 스트림 응답에 `usingVercelDataProtocol` 메서드를 호출하십시오:

```php
use App\Ai\Agents\SalesCoach;

Route::get('/coach', function () {
    return (new SalesCoach)
        ->stream('Analyze this sales transcript...')
        ->usingVercelDataProtocol();
});
```

<a name="broadcasting"></a>
### 브로드캐스팅

스트리밍 이벤트는 여러 가지 방법으로 브로드캐스트할 수 있습니다. 먼저, 스트림 이벤트 인스턴스에서 `broadcast` 또는 `broadcastNow` 메서드를 호출할 수 있습니다:

```php
use App\Ai\Agents\SalesCoach;
use Illuminate\Broadcasting\Channel;

$stream = (new SalesCoach)->stream('Analyze this sales transcript...');

foreach ($stream as $event) {
    $event->broadcast(new Channel('channel-name'));
}
```

혹은 에이전트의 `broadcastOnQueue` 메서드를 호출하여, 에이전트 작업을 큐잉하고 스트리밍 이벤트를 큐 처리하면서 브로드캐스트하도록 할 수도 있습니다:

```php
(new SalesCoach)->broadcastOnQueue(
    'Analyze this sales transcript...',
    new Channel('channel-name'),
);
```

<a name="queueing"></a>
### 큐 처리

에이전트의 `queue` 메서드를 이용하면, 에이전트를 프롬프트하되 응답 처리를 백그라운드로 넘겨 애플리케이션의 응답성을 높일 수 있습니다. 응답이 준비되었을 때(`then`)나 예외가 발생했을 때(`catch`) 실행할 클로저를 등록할 수 있습니다:

```php
use Illuminate\Http\Request;
use Laravel\Ai\Responses\AgentResponse;
use Throwable;

Route::post('/coach', function (Request $request) {
    return (new SalesCoach)
        ->queue($request->input('transcript'))
        ->then(function (AgentResponse $response) {
            // ...
        })
        ->catch(function (Throwable $e) {
            // ...
        });

    return back();
});
```

<a name="tools"></a>
### 툴

툴을 통해 에이전트가 프롬프트에 응답하는 과정에서 추가 기능을 사용할 수 있게 할 수 있습니다. `make:tool` Artisan 명령어를 사용하여 툴을 생성하세요:

```shell
php artisan make:tool RandomNumberGenerator
```

생성된 툴은 `app/Ai/Tools` 디렉터리에 위치하게 되며, 각각의 툴은 필요할 때 에이전트에 의해 호출되는 `handle` 메서드를 포함합니다:

```php
<?php

namespace App\Ai\Tools;

use Illuminate\Contracts\JsonSchema\JsonSchema;
use Laravel\Ai\Contracts\Tool;
use Laravel\Ai\Tools\Request;
use Stringable;

class RandomNumberGenerator implements Tool
{
    /**
     * 툴 목적에 대한 설명 반환
     */
    public function description(): Stringable|string
    {
        return 'This tool may be used to generate cryptographically secure random numbers.';
    }

    /**
     * 툴 실행
     */
    public function handle(Request $request): Stringable|string
    {
        return (string) random_int($request['min'], $request['max']);
    }

    /**
     * 툴 스키마 정의 반환
     */
    public function schema(JsonSchema $schema): array
    {
        return [
            'min' => $schema->integer()->min(0)->required(),
            'max' => $schema->integer()->required(),
        ];
    }
}
```

툴을 정의한 후에는, 에이전트의 `tools` 메서드를 통해 등록할 수 있습니다:

```php
use App\Ai\Tools\RandomNumberGenerator;

/**
 * 에이전트가 사용할 수 있는 툴 반환
 *
 * @return Tool[]
 */
public function tools(): iterable
{
    return [
        new RandomNumberGenerator,
    ];
}
```

<a name="similarity-search"></a>
#### 유사도 검색

`SimilaritySearch` 툴은 에이전트가 데이터베이스에 저장된 벡터 임베딩을 사용해 주어진 쿼리와 유사한 문서를 검색하도록 해줍니다. 이는 RAG(Retrieval-Augmented Generation)와 같이 AI 에이전트가 애플리케이션의 데이터를 탐색할 수 있게 할 때 유용합니다.

가장 간단한 방법은 임베딩 컬럼이 존재하는 Eloquent 모델과 함께 `usingModel` 메서드를 사용하는 것입니다:

```php
use App\Models\Document;
use Laravel\Ai\Tools\SimilaritySearch;

public function tools(): iterable
{
    return [
        SimilaritySearch::usingModel(Document::class, 'embedding'),
    ];
}
```

첫 번째 인자는 Eloquent 모델 클래스이며, 두 번째 인자는 벡터 임베딩을 저장한 컬럼명입니다.

유사도 임계값(0.0~1.0), 최대 결과 수, 쿼리 커스터마이징 클로저도 전달할 수 있습니다:

```php
SimilaritySearch::usingModel(
    model: Document::class,
    column: 'embedding',
    minSimilarity: 0.7,
    limit: 10,
    query: fn ($query) => $query->where('published', true),
),
```

더 세밀한 제어가 필요하다면, 검색 결과를 반환하는 커스텀 클로저로 SimilaritySearch 툴을 생성할 수 있습니다:

```php
use App\Models\Document;
use Laravel\Ai\Tools\SimilaritySearch;

public function tools(): iterable
{
    return [
        new SimilaritySearch(using: function (string $query) {
            return Document::query()
                ->where('user_id', $this->user->id)
                ->whereVectorSimilarTo('embedding', $query)
                ->limit(10)
                ->get();
        }),
    ];
}
```

툴의 설명을 `withDescription` 메서드로 커스터마이징할 수도 있습니다:

```php
SimilaritySearch::usingModel(Document::class, 'embedding')
    ->withDescription('Search the knowledge base for relevant articles.'),
```

<a name="provider-tools"></a>
### 프로바이더 툴

프로바이더 툴은 웹 검색, URL 읽기, 파일 탐색 등과 같이 프로바이더 자체적으로 구현한 특수 기능을 제공합니다. 일반 툴과 달리, 프로바이더 툴은 직접 애플리케이션에서 실행하는 것이 아니라 AI 프로바이더가 수행합니다.

프로바이더 툴 역시 에이전트의 `tools` 메서드에서 반환할 수 있습니다.

<a name="web-search"></a>
#### 웹 검색

`WebSearch` 프로바이더 툴은 에이전트가 웹에서 실시간 정보를 검색하도록 해줍니다. 최신 이벤트, 최신 데이터, 훈련 시점 이후 정보 등 검색이 필요한 경우에 유용합니다.

**지원 프로바이더:** Anthropic, OpenAI, Gemini

```php
use Laravel\Ai\Providers\Tools\WebSearch;

public function tools(): iterable
{
    return [
        new WebSearch,
    ];
}
```

검색 최대 횟수나 특정 도메인 결과만 허용하도록 커스터마이징할 수 있습니다:

```php
(new WebSearch)->max(5)->allow(['laravel.com', 'php.net']),
```

사용자 위치를 기준으로 검색 결과를 보정하려면 `location` 메서드를 사용하세요:

```php
(new WebSearch)->location(
    city: 'New York',
    region: 'NY',
    country: 'US'
);
```

<a name="web-fetch"></a>
#### 웹 페이지 내용 읽기

`WebFetch` 프로바이더 툴은 에이전트가 웹 페이지의 내용을 직접 읽거나 분석할 수 있도록 합니다. 특정 URL의 분석이나, 특정 웹 페이지에서의 정보 추출에 적합합니다.

**지원 프로바이더:** Anthropic, Gemini

```php
use Laravel\Ai\Providers\Tools\WebFetch;

public function tools(): iterable
{
    return [
        new WebFetch,
    ];
}
```

마찬가지로, 최대 요청 수 제한이나 도메인 제한을 적용할 수 있습니다:

```php
(new WebFetch)->max(3)->allow(['docs.laravel.com']),
```

<a name="file-search"></a>
#### 파일 검색

`FileSearch` 프로바이더 툴은 [벡터 스토어](#vector-stores)에 저장된 [파일](#files) 중에서 관련된 정보를 검색할 수 있도록 해줍니다. 즉, 에이전트가 업로드된 문서에서 적합한 정보를 찾을 수 있어 RAG(Retrieval-Augmented Generation)가 가능합니다.

**지원 프로바이더:** OpenAI, Gemini

```php
use Laravel\Ai\Providers\Tools\FileSearch;

public function tools(): iterable
{
    return [
        new FileSearch(stores: ['store_id']),
    ];
}
```

여러 개의 벡터 스토어 ID를 전달해 여러 스토어를 대상으로 검색할 수도 있습니다:

```php
new FileSearch(stores: ['store_1', 'store_2']);
```

파일에 [메타데이터](#adding-files-to-stores)가 있다면 `where` 인자로 검색 필터를 전달할 수 있습니다:

```php
new FileSearch(stores: ['store_id'], where: [
    'author' => 'Taylor Otwell',
    'year' => 2026,
]);
```

더 복잡한 필터링이 필요하다면, `FileSearchQuery` 인스턴스를 받는 클로저 형태로 조건을 지정할 수도 있습니다:

```php
use Laravel\Ai\Providers\Tools\FileSearchQuery;

new FileSearch(stores: ['store_id'], where: fn (FileSearchQuery $query) =>
    $query->where('author', 'Taylor Otwell')
        ->whereNot('status', 'draft')
        ->whereIn('category', ['news', 'updates'])
);
```

<a name="middleware"></a>
### 미들웨어

에이전트는 미들웨어를 지원하여, 프로바이더에게 프롬프트가 전달되기 전 내용을 수정하거나 감시할 수 있습니다. 에이전트에 미들웨어를 추가하려면 `HasMiddleware` 인터페이스를 구현하고, 미들웨어 클래스를 배열로 반환하는 `middleware` 메서드를 정의하세요:

```php
<?php

namespace App\Ai\Agents;

use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Contracts\HasMiddleware;
use Laravel\Ai\Promptable;

class SalesCoach implements Agent, HasMiddleware
{
    use Promptable;

    // ...

    /**
     * 에이전트의 미들웨어 반환
     */
    public function middleware(): array
    {
        return [
            new LogPrompts,
        ];
    }
}
```

각 미들웨어 클래스는 `AgentPrompt`와 다음 미들웨어를 호출하는 `Closure`를 받는 `handle` 메서드를 구현해야 합니다:

```php
<?php

namespace App\Ai\Middleware;

use Closure;
use Laravel\Ai\Prompts\AgentPrompt;

class LogPrompts
{
    /**
     * 인입된 프롬프트 처리
     */
    public function handle(AgentPrompt $prompt, Closure $next)
    {
        Log::info('Prompting agent', ['prompt' => $prompt->prompt]);

        return $next($prompt);
    }
}
```

응답 처리 이후 코드 실행이 필요하면, 응답의 `then` 메서드를 사용할 수 있습니다. 이는 동기/스트리밍 모두 적용됩니다:

```php
public function handle(AgentPrompt $prompt, Closure $next)
{
    return $next($prompt)->then(function (AgentResponse $response) {
        Log::info('Agent responded', ['text' => $response->text]);
    });
}
```

<a name="anonymous-agents"></a>
### 익명 에이전트

별도 에이전트 클래스를 만들지 않고 간단히 모델과 상호작용하고 싶다면, `agent` 함수를 사용해 임시(익명) 에이전트를 만들 수 있습니다:

```php
use function Laravel\Ai\{agent};

$response = agent(
    instructions: 'You are an expert at software development.',
    messages: [],
    tools: [],
)->prompt('Tell me about Laravel');
```

익명 에이전트도 구조화된 출력을 생성할 수 있습니다:

```php
use Illuminate\Contracts\JsonSchema\JsonSchema;

use function Laravel\Ai\{agent};

$response = agent(
    schema: fn (JsonSchema $schema) => [
        'number' => $schema->integer()->required(),
    ],
)->prompt('Generate a random number less than 100');
```

<a name="agent-configuration"></a>
### 에이전트 설정

PHP 속성을 이용해 에이전트의 텍스트 생성 옵션을 세밀하게 설정할 수 있습니다. 사용 가능한 속성은 다음과 같습니다:

- `MaxSteps`: 툴 사용 시 에이전트가 수행할 수 있는 최대 단계 수
- `MaxTokens`: 모델이 생성할 수 있는 최대 토큰 수
- `Model`: 사용할 모델 지정
- `Provider`: 에이전트에 사용할 AI 프로바이더(복수 지정 시 페일오버)
- `Temperature`: 생성 시 사용할 샘플링 온도(0.0~1.0)
- `Timeout`: 에이전트 요청의 HTTP 타임아웃(기본값 60초)
- `UseCheapestModel`: 프로바이더의 가장 저렴한 텍스트 모델 사용
- `UseSmartestModel`: 프로바이더의 가장 성능 좋은 텍스트 모델 사용

```php
<?php

namespace App\Ai\Agents;

use Laravel\Ai\Attributes\MaxSteps;
use Laravel\Ai\Attributes\MaxTokens;
use Laravel\Ai\Attributes\Model;
use Laravel\Ai\Attributes\Provider;
use Laravel\Ai\Attributes\Temperature;
use Laravel\Ai\Attributes\Timeout;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Promptable;

#[Provider('anthropic')]
#[Model('claude-haiku-4-5-20251001')]
#[MaxSteps(10)]
#[MaxTokens(4096)]
#[Temperature(0.7)]
#[Timeout(120)]
class SalesCoach implements Agent
{
    use Promptable;

    // ...
}
```

`UseCheapestModel`, `UseSmartestModel` 속성을 사용하면 직접 모델명을 지정하지 않고도 각각 가장 비용 효율적이거나, 가장 뛰어난 성능의 모델로 자동 선택할 수 있습니다:

```php
use Laravel\Ai\Attributes\UseCheapestModel;
use Laravel\Ai\Attributes\UseSmartestModel;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Promptable;

#[UseCheapestModel]
class SimpleSummarizer implements Agent
{
    use Promptable;

    // 가장 저렴한 모델(예: Haiku) 사용
}

#[UseSmartestModel]
class ComplexReasoner implements Agent
{
    use Promptable;

    // 가장 성능 좋은 모델(예: Opus) 사용
}
```

<a name="images"></a>
## 이미지

`Laravel\Ai\Image` 클래스를 사용해 `openai`, `gemini`, `xai` 프로바이더로 이미지를 생성할 수 있습니다:

```php
use Laravel\Ai\Image;

$image = Image::of('A donut sitting on the kitchen counter')->generate();

$rawContent = (string) $image;
```

`square`, `portrait`, `landscape` 메서드는 이미지의 가로세로 비율을 지정하며, `quality`로 최종 이미지 품질(`high`, `medium`, `low`)을 제어할 수 있습니다. `timeout`으로 HTTP 타임아웃(초)도 지정 가능합니다:

```php
use Laravel\Ai\Image;

$image = Image::of('A donut sitting on the kitchen counter')
    ->quality('high')
    ->landscape()
    ->timeout(120)
    ->generate();
```

참조 이미지를 첨부하고 싶다면 `attachments`를 사용할 수 있습니다:

```php
use Laravel\Ai\Files;
use Laravel\Ai\Image;

$image = Image::of('Update this photo of me to be in the style of a impressionist painting.')
    ->attachments([
        Files\Image::fromStorage('photo.jpg'),
        // Files\Image::fromPath('/home/laravel/photo.jpg'),
        // Files\Image::fromUrl('https://example.com/photo.jpg'),
        // $request->file('photo'),
    ])
    ->landscape()
    ->generate();
```

생성된 이미지는 기본 파일시스템 디스크에 간편하게 저장할 수 있습니다:

```php
$image = Image::of('A donut sitting on the kitchen counter');

$path = $image->store();
$path = $image->storeAs('image.jpg');
$path = $image->storePublicly();
$path = $image->storePubliclyAs('image.jpg');
```

이미지 생성을 큐로 비동기 처리할 수도 있습니다:

```php
use Laravel\Ai\Image;
use Laravel\Ai\Responses\ImageResponse;

Image::of('A donut sitting on the kitchen counter')
    ->portrait()
    ->queue()
    ->then(function (ImageResponse $image) {
        $path = $image->store();

        // ...
    });
```

<a name="audio"></a>
## 오디오

`Laravel\Ai\Audio` 클래스를 사용해 입력 텍스트로 오디오를 생성할 수 있습니다:

```php
use Laravel\Ai\Audio;

$audio = Audio::of('I love coding with Laravel.')->generate();

$rawContent = (string) $audio;
```

생성되는 오디오의 성별(`male`, `female`)이나 특정 목소리를 선택하려면 다음처럼 호출합니다:

```php
$audio = Audio::of('I love coding with Laravel.')
    ->female()
    ->generate();

$audio = Audio::of('I love coding with Laravel.')
    ->voice('voice-id-or-name')
    ->generate();
```

`instructions` 메서드로 생성되는 오디오의 발음 스타일 등을 동적으로 제시할 수도 있습니다:

```php
$audio = Audio::of('I love coding with Laravel.')
    ->female()
    ->instructions('Said like a pirate')
    ->generate();
```

생성된 오디오는 파일시스템에 저장할 수 있습니다:

```php
$audio = Audio::of('I love coding with Laravel.')->generate();

$path = $audio->store();
$path = $audio->storeAs('audio.mp3');
$path = $audio->storePublicly();
$path = $audio->storePubliclyAs('audio.mp3');
```

오디오 생성 역시 큐로 비동기 처리할 수 있습니다:

```php
use Laravel\Ai\Audio;
use Laravel\Ai\Responses\AudioResponse;

Audio::of('I love coding with Laravel.')
    ->queue()
    ->then(function (AudioResponse $audio) {
        $path = $audio->store();

        // ...
    });
```

<a name="transcription"></a>
## 트랜스크립션

`Laravel\Ai\Transcription` 클래스를 사용해 오디오의 문자 트랜스크립트를 생성할 수 있습니다:

```php
use Laravel\Ai\Transcription;

$transcript = Transcription::fromPath('/home/laravel/audio.mp3')->generate();
$transcript = Transcription::fromStorage('audio.mp3')->generate();
$transcript = Transcription::fromUpload($request->file('audio'))->generate();

return (string) $transcript;
```

`diarize` 메서드를 사용하면, 응답에 각 화자의 분절된 대화 스크립트도 포함시킬 수 있습니다(화자 구분):

```php
$transcript = Transcription::fromStorage('audio.mp3')
    ->diarize()
    ->generate();
```

트랜스크립션 생성도 큐로 처리할 수 있습니다:

```php
use Laravel\Ai\Transcription;
use Laravel\Ai\Responses\TranscriptionResponse;

Transcription::fromStorage('audio.mp3')
    ->queue()
    ->then(function (TranscriptionResponse $transcript) {
        // ...
    });
```

<a name="embeddings"></a>
## 임베딩

`Stringable` 클래스의 `toEmbeddings` 메서드를 통해, 문자열에 대한 벡터 임베딩을 쉽고 빠르게 생성할 수 있습니다:

```php
use Illuminate\Support\Str;

$embeddings = Str::of('Napa Valley has great wine.')->toEmbeddings();
```

또는, `Embeddings` 클래스를 사용해 여러 입력에 대한 임베딩을 한 번에 생성할 수 있습니다:

```php
use Laravel\Ai\Embeddings;

$response = Embeddings::for([
    'Napa Valley has great wine.',
    'Laravel is a PHP framework.',
])->generate();

$response->embeddings; // [[0.123, 0.456, ...], [0.789, 0.012, ...]]
```

임베딩의 차원 수와 프로바이더를 지정할 수도 있습니다:

```php
$response = Embeddings::for(['Napa Valley has great wine.'])
    ->dimensions(1536)
    ->generate('openai', 'text-embedding-3-small');
```

<a name="querying-embeddings"></a>
### 임베딩 질의

임베딩을 생성한 후에는, 보통 데이터베이스의 벡터 컬럼에 저장해 두고 검색 시 활용합니다. Laravel은 PostgreSQL에서 `pgvector` 확장을 사용해 벡터 컬럼을 기본적으로 지원합니다. 우선, 마이그레이션에서 벡터 컬럼을 차원 수와 함께 정의합니다:

```php
Schema::ensureVectorExtensionExists();

Schema::create('documents', function (Blueprint $table) {
    $table->id();
    $table->string('title');
    $table->text('content');
    $table->vector('embedding', dimensions: 1536);
    $table->timestamps();
});
```

유사도 검색 속도를 높이기 위해 벡터 컬럼에 인덱스를 추가할 수도 있습니다. `index`를 호출하면 Laravel이 자동으로 cosign 거리 기반의 HNSW 인덱스를 생성합니다:

```php
$table->vector('embedding', dimensions: 1536)->index();
```

Eloquent 모델에서는 해당 벡터 컬럼을 `array`로 캐스팅해야 합니다:

```php
protected function casts(): array
{
    return [
        'embedding' => 'array',
    ];
}
```

유사한 레코드를 검색하려면 `whereVectorSimilarTo` 메서드를 사용하세요. 이 메서드는 최소 코사인 유사도(0.0~1.0, 1.0은 완전 동일)를 기준으로 필터링 및 유사도 순 정렬을 합니다:

```php
use App\Models\Document;

$documents = Document::query()
    ->whereVectorSimilarTo('embedding', $queryEmbedding, minSimilarity: 0.4)
    ->limit(10)
    ->get();
```

`$queryEmbedding`에는 float 배열이나 일반 문자열을 전달할 수 있습니다. 문자열을 주면, Laravel이 자동으로 임베딩을 생성합니다:

```php
$documents = Document::query()
    ->whereVectorSimilarTo('embedding', 'best wineries in Napa Valley')
    ->limit(10)
    ->get();
```

더 세밀한 제어가 필요한 경우, `whereVectorDistanceLessThan`, `selectVectorDistance`, `orderByVectorDistance` 같은 하위 메서드를 활용할 수 있습니다:

```php
$documents = Document::query()
    ->select('*')
    ->selectVectorDistance('embedding', $queryEmbedding, as: 'distance')
    ->whereVectorDistanceLessThan('embedding', $queryEmbedding, maxDistance: 0.3)
    ->orderByVectorDistance('embedding', $queryEmbedding)
    ->limit(10)
    ->get();
```

에이전트에게 유사도 검색 기능을 툴로 제공하려면 [유사도 검색](#similarity-search) 문서를 참고하세요.

> [!NOTE]
> 벡터 쿼리는 현재 PostgreSQL에서 `pgvector` 확장을 사용할 때만 지원됩니다.

<a name="caching-embeddings"></a>
### 임베딩 캐싱

동일 입력에 대한 중복 API 호출을 방지하기 위해 임베딩 생성 결과를 캐시할 수 있습니다. 설정 파일의 `ai.caching.embeddings.cache` 옵션을 `true`로 지정하여 캐시를 활성화할 수 있습니다:

```php
'caching' => [
    'embeddings' => [
        'cache' => true,
        'store' => env('CACHE_STORE', 'database'),
        // ...
    ],
],
```

캐시가 활성화되면 임베딩은 30일간 저장됩니다. 캐시 키는 프로바이더, 모델, 차원, 입력값을 기반으로 하여 동일한 요청에 대해 캐시된 결과를, 설정이 다를 경우에는 새 임베딩을 생성합니다.

글로벌 캐싱이 비활성화되어 있어도, 개별 요청마다 `cache` 메서드로 임베딩 생성 결과를 캐시할 수 있습니다:

```php
$response = Embeddings::for(['Napa Valley has great wine.'])
    ->cache()
    ->generate();
```

캐시 지속 시간을 초 단위로 지정할 수도 있습니다:

```php
$response = Embeddings::for(['Napa Valley has great wine.'])
    ->cache(seconds: 3600) // 1시간 캐시
    ->generate();
```

`toEmbeddings`에도 `cache` 인자를 사용할 수 있습니다:

```php
// 기본 기간으로 캐시
$embeddings = Str::of('Napa Valley has great wine.')->toEmbeddings(cache: true);

// 특정 기간 캐시
$embeddings = Str::of('Napa Valley has great wine.')->toEmbeddings(cache: 3600);
```

<a name="reranking"></a>
## 리랭킹

리랭킹은 쿼리의 관련성에 따라 문서 목록의 순서를 재조정할 수 있게 해줍니다. 이는 시맨틱 검색의 검색 결과를 개선하는 데 유용합니다.

`Laravel\Ai\Reranking` 클래스를 사용해 문서 리랭킹이 가능합니다:

```php
use Laravel\Ai\Reranking;

$response = Reranking::of([
    'Django is a Python web framework.',
    'Laravel is a PHP web application framework.',
    'React is a JavaScript library for building user interfaces.',
])->rerank('PHP frameworks');

// 상위 결과 접근 예시
$response->first()->document; // "Laravel is a PHP web application framework."
$response->first()->score;    // 0.95
$response->first()->index;    // 1 (원본 인덱스)
```

`limit` 메서드로 결과 개수를 제한할 수 있습니다:

```php
$response = Reranking::of($documents)
    ->limit(5)
    ->rerank('search query');
```

<a name="reranking-collections"></a>
### 컬렉션 리랭킹

Laravel 컬렉션에서도 `rerank` 매크로를 활용해 손쉽게 리랭킹이 가능합니다. 첫 번째 인자는 기준 필드이며, 두 번째 인자는 쿼리입니다:

```php
// 단일 필드 기준 리랭킹
$posts = Post::all()
    ->rerank('body', 'Laravel tutorials');

// 여러 필드 기준 리랭킹(필드는 JSON으로 전달됨)
$reranked = $posts->rerank(['title', 'body'], 'Laravel tutorials');

// 클로저로 문서 형식 지정
$reranked = $posts->rerank(
    fn ($post) => $post->title.': '.$post->body,
    'Laravel tutorials'
);
```

결과 개수 제한, 프로바이더 지정 등도 가능합니다:

```php
$reranked = $posts->rerank(
    by: 'content',
    query: 'Laravel tutorials',
    limit: 10,
    provider: 'cohere'
);
```

<a name="files"></a>
## 파일

`Laravel\Ai\Files` 클래스 및 개별 파일 클래스를 통해 AI 프로바이더에 파일을 저장하고, 이후 반복 참고할 수 있습니다. 이는 여러 번 참조해야 하는 대용량 문서 업로드, 대화 등에서 유용합니다:

```php
use Laravel\Ai\Files\Document;
use Laravel\Ai\Files\Image;

// 로컬 경로에서 파일 저장
$response = Document::fromPath('/home/laravel/document.pdf')->put();
$response = Image::fromPath('/home/laravel/photo.jpg')->put();

// 파일시스템에 저장된 파일 저장
$response = Document::fromStorage('document.pdf', disk: 'local')->put();
$response = Image::fromStorage('photo.jpg', disk: 'local')->put();

// 원격 URL에 위치한 파일 저장
$response = Document::fromUrl('https://example.com/document.pdf')->put();
$response = Image::fromUrl('https://example.com/photo.jpg')->put();

return $response->id;
```

원시 데이터, 업로드 파일 저장도 지원합니다:

```php
use Laravel\Ai\Files;
use Laravel\Ai\Files\Document;

// 원시 문자열 저장
$stored = Document::fromString('Hello, World!', 'text/plain')->put();

// 업로드 파일 저장
$stored = Document::fromUpload($request->file('document'))->put();
```

저장된 파일은 에이전트 프롬프트에서 `fromId`로 간편하게 참조할 수 있으며, 재업로드 없이 사용할 수 있습니다:

```php
use App\Ai\Agents\SalesCoach;
use Laravel\Ai\Files;

$response = (new SalesCoach)->prompt(
    'Analyze the attached sales transcript...',
    attachments: [
        Files\Document::fromId('file-id') // 저장된 문서 첨부
    ]
);
```

기존에 저장된 파일을 불러올 때는, 파일 인스턴스에서 `get`을 호출합니다:

```php
use Laravel\Ai\Files\Document;

$file = Document::fromId('file-id')->get();

$file->id;
$file->mimeType();
```

파일 삭제는 `delete`로 처리합니다:

```php
Document::fromId('file-id')->delete();
```

파일 업로드 및 기타 동작의 경우, `Files` 클래스는 기본적으로 `config/ai.php`에서 설정한 AI 프로바이더를 사용합니다. 필요에 따라 `provider` 인자로 다른 프로바이더를 지정할 수 있습니다:

```php
$response = Document::fromPath(
    '/home/laravel/document.pdf'
)->put(provider: 'anthropic');
```

<a name="using-stored-files-in-conversations"></a>
### 대화에서 저장된 파일 사용

프로바이더에 파일을 저장한 후에는, `Document` 또는 `Image` 클래스의 `fromId`로 참조해 에이전트 대화에 활용할 수 있습니다:

```php
use App\Ai\Agents\DocumentAnalyzer;
use Laravel\Ai\Files;
use Laravel\Ai\Files\Document;

$stored = Document::fromPath('/path/to/report.pdf')->put();

$response = (new DocumentAnalyzer)->prompt(
    'Summarize this document.',
    attachments: [
        Document::fromId($stored->id),
    ],
);
```

이미지도 마찬가지로 `Image` 클래스로 저장하여 프롬프트에 첨부할 수 있습니다:

```php
use Laravel\Ai\Files;
use Laravel\Ai\Files\Image;

$stored = Image::fromPath('/path/to/photo.jpg')->put();

$response = (new ImageAnalyzer)->prompt(
    'What is in this image?',
    attachments: [
        Image::fromId($stored->id),
    ],
);
```

<a name="vector-stores"></a>
## 벡터 스토어

벡터 스토어는 검색 가능한 파일 컬렉션을 만들어, RAG(Retrieval-Augmented Generation) 등에서 활용할 수 있게 해줍니다. `Laravel\Ai\Stores` 클래스는 벡터 스토어 생성, 조회, 삭제 등의 메서드를 제공합니다:

```php
use Laravel\Ai\Stores;

// 새 벡터 스토어 생성
$store = Stores::create('Knowledge Base');

// 추가 옵션과 함께 생성
$store = Stores::create(
    name: 'Knowledge Base',
    description: 'Documentation and reference materials.',
    expiresWhenIdleFor: days(30),
);

return $store->id;
```

기존 벡터 스토어를 ID로 조회하려면 `get`을 사용합니다:

```php
use Laravel\Ai\Stores;

$store = Stores::get('store_id');

$store->id;
$store->name;
$store->fileCounts;
$store->ready;
```

스토어 삭제는 ID로 혹은 인스턴스에서 `delete`로 처리합니다:

```php
use Laravel\Ai\Stores;

// ID로 삭제
Stores::delete('store_id');

// 인스턴스로 삭제
$store = Stores::get('store_id');

$store->delete();
```

<a name="adding-files-to-stores"></a>
### 스토어에 파일 추가

벡터 스토어가 준비되었다면, `add` 메서드를 통해 [파일](#files)을 스토어에 추가할 수 있습니다. 추가된 파일은 [파일 검색 프로바이더 툴](#file-search)을 통한 시맨틱 검색에 자동으로 인덱싱됩니다:

```php
use Laravel\Ai\Files\Document;
use Laravel\Ai\Stores;

$store = Stores::get('store_id');

// 프로바이더에 이미 저장된 파일 추가
$document = $store->add('file_id');
$document = $store->add(Document::fromId('file_id'));

// 저장과 동시에 스토어에 추가
$document = $store->add(Document::fromPath('/path/to/document.pdf'));
$document = $store->add(Document::fromStorage('manual.pdf'));
$document = $store->add($request->file('document'));

$document->id;
$document->fileId;
```

> **Note:** 기존에 저장된 파일을 벡터 스토어에 추가할 때 반환되는 document ID가 기존 파일 ID와 같을 수도 있지만, 스토리지 제공자에 따라 새로운 document ID가 부여될 수 있습니다. 따라서 두 ID 모두 데이터베이스에 저장해 두는 것을 권장합니다.

스토어에 파일을 추가할 때 메타데이터를 첨부할 수 있으며, 이후 [파일 검색 프로바이더 툴](#file-search)에서 검색 필터로 활용할 수 있습니다:

```php
$store->add(Document::fromPath('/path/to/document.pdf'), metadata: [
    'author' => 'Taylor Otwell',
    'department' => 'Engineering',
    'year' => 2026,
]);
```

스토어에서 파일을 제거하려면, `remove` 메서드를 사용하세요:

```php
$store->remove('file_id');
```

스토어에서 파일을 삭제하더라도, 파일 자체가 [프로바이더 파일 스토리지](#files)에서 제거되지는 않습니다. 완전히 삭제하려면 `deleteFile` 인자를 `true`로 전달하세요:

```php
$store->remove('file_abc123', deleteFile: true);
```

<a name="failover"></a>
## 페일오버

프롬프트 전달 또는 기타 미디어 생성 시, 서비스 장애나 레이트리미트가 발생하면 예비 프로바이더/모델로 자동 페일오버하도록 프로바이더/모델 배열을 지정할 수 있습니다:

```php
use App\Ai\Agents\SalesCoach;
use Laravel\Ai\Image;

$response = (new SalesCoach)->prompt(
    'Analyze this sales transcript...',
    provider: ['openai', 'anthropic'],
);

$image = Image::of('A donut sitting on the kitchen counter')
    ->generate(provider: ['gemini', 'xai']);
```

<a name="testing"></a>
## 테스트

<a name="testing-agents"></a>
### 에이전트

테스트 중 에이전트 응답을 임의로 지정하려면, 에이전트 클래스의 `fake` 메서드를 사용하세요. 응답 배열 또는 클로저를 전달할 수 있습니다:

```php
use App\Ai\Agents\SalesCoach;
use Laravel\Ai\Prompts\AgentPrompt;

// 모든 프롬프트에 대해 고정 응답 반환
SalesCoach::fake();

// 프롬프트별 응답 목록 제공
SalesCoach::fake([
    'First response',
    'Second response',
]);

// 인입 프롬프트에 따라 동적 응답 처리
SalesCoach::fake(function (AgentPrompt $prompt) {
    return 'Response for: '.$prompt->prompt;
});
```

> **Note:** 구조화된 출력을 반환하는 에이전트에서 `Agent::fake()`를 호출하면, agent에서 정의한 출력 스키마에 맞는 더미 데이터가 자동 생성됩니다.

에이전트 프롬프트 기록에 대해 아래와 같이 다양한 assertion을 할 수 있습니다:

```php
use Laravel\Ai\Prompts\AgentPrompt;

SalesCoach::assertPrompted('Analyze this...');

SalesCoach::assertPrompted(function (AgentPrompt $prompt) {
    return $prompt->contains('Analyze');
});

SalesCoach::assertNotPrompted('Missing prompt');

SalesCoach::assertNeverPrompted();
```

큐로 처리되는 에이전트 호출의 경우, 큐에 대한 assertion 메서드를 사용하세요:

```php
use Laravel\Ai\QueuedAgentPrompt;

SalesCoach::assertQueued('Analyze this...');

SalesCoach::assertQueued(function (QueuedAgentPrompt $prompt) {
    return $prompt->contains('Analyze');
});

SalesCoach::assertNotQueued('Missing prompt');

SalesCoach::assertNeverQueued();
```

정의되지 않은 페이크 응답이 발생하면 예외를 발생시키려면 `preventStrayPrompts`를 사용하세요:

```php
SalesCoach::fake()->preventStrayPrompts();
```

<a name="testing-images"></a>
### 이미지

`Image` 클래스의 `fake` 메서드로 이미지 생성을 임의로 지정해 테스트할 수 있습니다. 이후 기록된 생성 프롬프트에 대한 다양한 assertion이 가능합니다:

```php
use Laravel\Ai\Image;
use Laravel\Ai\Prompts\ImagePrompt;
use Laravel\Ai\Prompts\QueuedImagePrompt;

// 모든 프롬프트에 대해 고정 응답 반환
Image::fake();

// 프롬프트별 응답
Image::fake([
    base64_encode($firstImage),
    base64_encode($secondImage),
]);

// 동적 응답 생성
Image::fake(function (ImagePrompt $prompt) {
    return base64_encode('...');
});
```

이미지 생성 프롬프트에 대한 assertion 예시:

```php
Image::assertGenerated(function (ImagePrompt $prompt) {
    return $prompt->contains('sunset') && $prompt->isLandscape();
});

Image::assertNotGenerated('Missing prompt');

Image::assertNothingGenerated();
```

큐에서 처리된 요청에 대해서는 아래와 같이 assertion:

```php
Image::assertQueued(
    fn (QueuedImagePrompt $prompt) => $prompt->contains('sunset')
);

Image::assertNotQueued('Missing prompt');

Image::assertNothingQueued();
```

미정의 이미지 생성 발생 시 예외 발생 옵션:

```php
Image::fake()->preventStrayImages();
```

<a name="testing-audio"></a>
### 오디오

`Audio` 클래스의 `fake` 메서드로 오디오 생성을 테스트 환경에서 임의 지정할 수 있고, 기록에 대한 assertion도 다양하게 제공됩니다:

```php
use Laravel\Ai\Audio;
use Laravel\Ai\Prompts\AudioPrompt;
use Laravel\Ai\Prompts\QueuedAudioPrompt;

// 모든 프롬프트에 대해 고정 응답 반환
Audio::fake();

// 개별 응답 지정
Audio::fake([
    base64_encode($firstAudio),
    base64_encode($secondAudio),
]);

// 동적 생성
Audio::fake(function (AudioPrompt $prompt) {
    return base64_encode('...');
});
```

오디오 생성 프롬프트 assertion 예시:

```php
Audio::assertGenerated(function (AudioPrompt $prompt) {
    return $prompt->contains('Hello') && $prompt->isFemale();
});

Audio::assertNotGenerated('Missing prompt');

Audio::assertNothingGenerated();
```

큐 요청에 대한 assertion:

```php
Audio::assertQueued(
    fn (QueuedAudioPrompt $prompt) => $prompt->contains('Hello')
);

Audio::assertNotQueued('Missing prompt');

Audio::assertNothingQueued();
```

예상치 못한 fake 오디오 생성을 차단:

```php
Audio::fake()->preventStrayAudio();
```

<a name="testing-transcriptions"></a>
### 트랜스크립션

`Transcription` 클래스의 `fake` 메서드로 트랜스크립션을 임의 응답하도록 하고, 다양한 assertion을 지원합니다:

```php
use Laravel\Ai\Transcription;
use Laravel\Ai\Prompts\TranscriptionPrompt;
use Laravel\Ai\Prompts\QueuedTranscriptionPrompt;

// 모든 프롬프트에 대해 고정 응답
Transcription::fake();

// 응답 목록 지정
Transcription::fake([
    'First transcription text.',
    'Second transcription text.',
]);

// 동적으로 생성
Transcription::fake(function (TranscriptionPrompt $prompt) {
    return 'Transcribed text...';
});
```

트랜스크립션 프롬프트에 대한 assertion:

```php
Transcription::assertGenerated(function (TranscriptionPrompt $prompt) {
    return $prompt->language === 'en' && $prompt->isDiarized();
});

Transcription::assertNotGenerated(
    fn (TranscriptionPrompt $prompt) => $prompt->language === 'fr'
);

Transcription::assertNothingGenerated();
```

큐에 대해서도 assertion 지원:

```php
Transcription::assertQueued(
    fn (QueuedTranscriptionPrompt $prompt) => $prompt->isDiarized()
);

Transcription::assertNotQueued(
    fn (QueuedTranscriptionPrompt $prompt) => $prompt->language === 'fr'
);

Transcription::assertNothingQueued();
```

미정의 fake 트랜스크립션 생성 차단:

```php
Transcription::fake()->preventStrayTranscriptions();
```

<a name="testing-embeddings"></a>
### 임베딩

`Embeddings` 클래스의 `fake` 메서드를 이용해 임베딩 생성을 테스트할 수 있고, 임베딩 생성 프롬프트 기록에 대한 assertion도 지원합니다:

```php
use Laravel\Ai\Embeddings;
use Laravel\Ai\Prompts\EmbeddingsPrompt;
use Laravel\Ai\Prompts\QueuedEmbeddingsPrompt;

// 모든 프롬프트에 대해 올바른 차원의 fake 임베딩 반환
Embeddings::fake();

// 응답 목록 지정
Embeddings::fake([
    [$firstEmbeddingVector],
    [$secondEmbeddingVector],
]);

// 동적 응답 반환
Embeddings::fake(function (EmbeddingsPrompt $prompt) {
    return array_map(
        fn () => Embeddings::fakeEmbedding($prompt->dimensions),
        $prompt->inputs
    );
});
```

임베딩 생성 프롬프트 assertion 예시:

```php
Embeddings::assertGenerated(function (EmbeddingsPrompt $prompt) {
    return $prompt->contains('Laravel') && $prompt->dimensions === 1536;
});

Embeddings::assertNotGenerated(
    fn (EmbeddingsPrompt $prompt) => $prompt->contains('Other')
);

Embeddings::assertNothingGenerated();
```

큐에서의 요청도 assertion 지원:

```php
Embeddings::assertQueued(
    fn (QueuedEmbeddingsPrompt $prompt) => $prompt->contains('Laravel')
);

Embeddings::assertNotQueued(
    fn (QueuedEmbeddingsPrompt $prompt) => $prompt->contains('Other')
);

Embeddings::assertNothingQueued();
```

미정의 fake 임베딩 생성 차단:

```php
Embeddings::fake()->preventStrayEmbeddings();
```

<a name="testing-reranking"></a>
### 리랭킹

`Reranking` 클래스의 `fake` 메서드로 리랭킹 작업을 임의로 대체할 수 있습니다:

```php
use Laravel\Ai\Reranking;
use Laravel\Ai\Prompts\RerankingPrompt;
use Laravel\Ai\Responses\Data\RankedDocument;

// 자동으로 fake 리랭킹 응답 반환
Reranking::fake();

// 커스텀 응답 지정
Reranking::fake([
    [
        new RankedDocument(index: 0, document: 'First', score: 0.95),
        new RankedDocument(index: 1, document: 'Second', score: 0.80),
    ],
]);
```

리랭킹 작업에 대한 assertion:

```php
Reranking::assertReranked(function (RerankingPrompt $prompt) {
    return $prompt->contains('Laravel') && $prompt->limit === 5;
});

Reranking::assertNotReranked(
    fn (RerankingPrompt $prompt) => $prompt->contains('Django')
);

Reranking::assertNothingReranked();
```

<a name="testing-files"></a>
### 파일

`Files` 클래스의 `fake` 메서드를 통해 파일 작업을 모킹할 수 있습니다:

```php
use Laravel\Ai\Files;

Files::fake();
```

이후 파일 업로드 및 삭제 작업에 대한 assertion이 가능합니다:

```php
use Laravel\Ai\Contracts\Files\StorableFile;
use Laravel\Ai\Files\Document;

// 파일 저장
Document::fromString('Hello, Laravel!', mime: 'text/plain')
    ->as('hello.txt')
    ->put();

// assertion
Files::assertStored(fn (StorableFile $file) =>
    (string) $file === 'Hello, Laravel!' &&
        $file->mimeType() === 'text/plain';
);

Files::assertNotStored(fn (StorableFile $file) =>
    (string) $file === 'Hello, World!'
);

Files::assertNothingStored();
```

파일 삭제에 대해서도 ID로 assertion 가능:

```php
Files::assertDeleted('file-id');
Files::assertNotDeleted('file-id');
Files::assertNothingDeleted();
```

<a name="testing-vector-stores"></a>
### 벡터 스토어

`Stores` 클래스의 `fake` 메서드로 벡터 스토어 작업을 전부 모킹할 수 있으며, 이때 [파일 작업](#files)도 함께 모킹됩니다:

```php
use Laravel\Ai\Stores;

Stores::fake();
```

스토어 생성/삭제에 대한 assertion도 지원합니다:

```php
use Laravel\Ai\Stores;

// 저장소 생성
$store = Stores::create('Knowledge Base');

// 생성 assertion
Stores::assertCreated('Knowledge Base');

Stores::assertCreated(fn (string $name, ?string $description) =>
    $name === 'Knowledge Base'
);

Stores::assertNotCreated('Other Store');

Stores::assertNothingCreated();
```

삭제에 대해서는 스토어 ID로 assertion:

```php
Stores::assertDeleted('store_id');
Stores::assertNotDeleted('other_store_id');
Stores::assertNothingDeleted();
```

파일이 스토어에 추가/제거되었는지 개별 `Store` 인스턴스에서 assertion:

```php
Stores::fake();

$store = Stores::get('store_id');

// 파일 추가/삭제
$store->add('added_id');
$store->remove('removed_id');

// assertion
$store->assertAdded('added_id');
$store->assertRemoved('removed_id');

$store->assertNotAdded('other_file_id');
$store->assertNotRemoved('other_file_id');
```

파일이 프로바이더 [파일 스토리지](#files)와 벡터 스토어 모두에 동시에 저장될 경우, 파일의 프로바이더 ID를 알 수 없으므로, 아래처럼 파일 내용 기준으로 assertion을 할 수 있습니다:

```php
use Laravel\Ai\Contracts\Files\StorableFile;
use Laravel\Ai\Files\Document;

$store->add(Document::fromString('Hello, World!', 'text/plain')->as('hello.txt'));

$store->assertAdded(fn (StorableFile $file) => $file->name() === 'hello.txt');
$store->assertAdded(fn (StorableFile $file) => $file->content() === 'Hello, World!');
```

<a name="events"></a>
## 이벤트

Laravel AI SDK는 다양한 [이벤트](/docs/12.x/events)를 발생시킵니다. 다음 이벤트들을 통해 AI SDK 사용 내역을 로깅하거나 별도의 처리를 할 수 있습니다:

- `AddingFileToStore`
- `AgentPrompted`
- `AgentStreamed`
- `AudioGenerated`
- `CreatingStore`
- `EmbeddingsGenerated`
- `FileAddedToStore`
- `FileDeleted`
- `FileRemovedFromStore`
- `FileStored`
- `GeneratingAudio`
- `GeneratingEmbeddings`
- `GeneratingImage`
- `GeneratingTranscription`
- `ImageGenerated`
- `InvokingTool`
- `PromptingAgent`
- `RemovingFileFromStore`
- `Reranked`
- `Reranking`
- `StoreCreated`
- `StoringFile`
- `StreamingAgent`
- `ToolInvoked`
- `TranscriptionGenerated`

이러한 이벤트를 활용하여 AI SDK의 사용 내역을 로깅하거나 별도의 처리를 수행할 수 있습니다.