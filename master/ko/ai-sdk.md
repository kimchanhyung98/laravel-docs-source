# Laravel AI SDK (Laravel AI SDK)

- [소개](#introduction)
- [설치](#installation)
    - [설정](#configuration)
    - [커스텀 베이스 URL](#custom-base-urls)
    - [프로바이더 지원](#provider-support)
- [에이전트](#agents)
    - [프롬프트 실행](#prompting)
    - [대화 컨텍스트](#conversation-context)
    - [구조화된 출력](#structured-output)
    - [첨부파일](#attachments)
    - [스트리밍](#streaming)
    - [브로드캐스팅](#broadcasting)
    - [큐잉](#queueing)
    - [툴](#tools)
    - [프로바이더 툴](#provider-tools)
    - [미들웨어](#middleware)
    - [익명 에이전트](#anonymous-agents)
    - [에이전트 설정](#agent-configuration)
- [이미지](#images)
- [오디오 (TTS)](#audio)
- [트랜스크립션 (STT)](#transcription)
- [임베딩](#embeddings)
    - [임베딩 질의](#querying-embeddings)
    - [임베딩 캐싱](#caching-embeddings)
- [재정렬(Reranking)](#reranking)
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
    - [재정렬](#testing-reranking)
    - [파일](#testing-files)
    - [벡터 스토어](#testing-vector-stores)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel AI SDK](https://github.com/laravel/ai)는 OpenAI, Anthropic, Gemini 등 다양한 AI 프로바이더와 상호작용할 수 있는 통합적이고 표현력 있는 API를 제공합니다. AI SDK를 사용하면 도구와 구조화된 출력을 가진 지능형 에이전트 구성, 이미지 생성, 오디오 합성/음성 텍스트 변환, 벡터 임베딩 생성 등 다양한 작업을 일관되고 라라벨 친화적인 방식으로 수행할 수 있습니다.

<a name="installation"></a>
## 설치 (Installation)

Laravel AI SDK는 Composer를 통해 설치할 수 있습니다.

```shell
composer require laravel/ai
```

다음으로, `vendor:publish` Artisan 명령어를 사용하여 AI SDK의 설정 및 마이그레이션 파일을 퍼블리시해야 합니다.

```shell
php artisan vendor:publish --provider="Laravel\Ai\AiServiceProvider"
```

마지막으로 애플리케이션의 데이터베이스 마이그레이션을 실행해야 합니다. 이 과정에서 AI SDK의 대화 저장을 위해 사용되는 `agent_conversations` 및 `agent_conversation_messages` 테이블이 생성됩니다.

```shell
php artisan migrate
```

<a name="configuration"></a>
### 설정 (Configuration)

각 AI 프로바이더의 인증 정보를 애플리케이션의 `config/ai.php` 설정 파일 또는 `.env` 환경 변수 파일에 정의할 수 있습니다.

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

텍스트, 이미지, 오디오, 트랜스크립션, 임베딩 등에 사용되는 기본 모델도 `config/ai.php` 파일에서 설정할 수 있습니다.

<a name="custom-base-urls"></a>
### 커스텀 베이스 URL (Custom Base URLs)

기본적으로 Laravel AI SDK는 각 프로바이더의 공개 API 엔드포인트에 직접 연결합니다. 하지만 프록시 서비스를 통해 API 키 관리 통합, 레이트 리미팅 적용, 사내 게이트웨이 경유 등의 목적으로 별도 엔드포인트로 요청을 전달해야 할 수도 있습니다.

이 경우, 아래와 같이 프로바이더 설정에 `url` 파라미터를 추가하여 커스텀 베이스 URL을 지정할 수 있습니다.

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

이 방법은 LiteLLM, Azure OpenAI Gateway 등 프록시 서비스를 사용하거나, 대체 엔드포인트에 요청을 접속해야 할 경우 유용합니다.

커스텀 베이스 URL은 다음 프로바이더에서 지원됩니다: OpenAI, Anthropic, Gemini, Groq, Cohere, DeepSeek, xAI, OpenRouter.

<a name="provider-support"></a>
### 프로바이더 지원 (Provider Support)

AI SDK는 다양한 기능별로 여러 프로바이더를 지원합니다. 다음 표는 각 기능별 제공 프로바이더를 요약한 것입니다.

| 기능 | 지원 프로바이더 |
|---|---|
| 텍스트 | OpenAI, Anthropic, Gemini, Groq, xAI, DeepSeek, Mistral, Ollama |
| 이미지 | OpenAI, Gemini, xAI |
| TTS | OpenAI, ElevenLabs |
| STT | OpenAI, ElevenLabs, Mistral |
| 임베딩 | OpenAI, Gemini, Cohere, Mistral, Jina, VoyageAI |
| 재정렬(Reranking) | Cohere, Jina |
| 파일 | OpenAI, Anthropic, Gemini |

<a name="agents"></a>
## 에이전트 (Agents)

에이전트는 Laravel AI SDK에서 AI 프로바이더와 상호작용하기 위한 기본 단위입니다. 각 에이전트는 특정한 PHP 클래스로, 대형 언어 모델과의 상호작용에 필요한 지시문, 대화 컨텍스트, 사용 가능한 도구, 출력 스키마를 캡슐화합니다. 영업 코치, 문서 분석기, 지원 챗봇 등 에이전트는 다양하게 확장할 수 있으며, 한 번 구성 후 애플리케이션 전반에서 필요에 따라 재사용할 수 있습니다.

에이전트는 `make:agent` Artisan 명령어로 생성할 수 있습니다.

```shell
php artisan make:agent SalesCoach

php artisan make:agent SalesCoach --structured
```

생성된 에이전트 클래스 내에서 시스템 프롬프트(지시문), 메시지 컨텍스트, 사용 가능한 도구, 출력 스키마(필요 시)를 정의할 수 있습니다.

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
use Laravel\Ai\Messages\Message;
use Laravel\Ai\Promptable;
use Stringable;

class SalesCoach implements Agent, Conversational, HasTools, HasStructuredOutput
{
    use Promptable;

    public function __construct(public User $user) {}

    /**
     * Get the instructions that the agent should follow.
     */
    public function instructions(): Stringable|string
    {
        return 'You are a sales coach, analyzing transcripts and providing feedback and an overall sales strength score.';
    }

    /**
     * Get the list of messages comprising the conversation so far.
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
     * Get the tools available to the agent.
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
     * Get the agent's structured output schema definition.
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
### 프롬프트 실행 (Prompting)

에이전트에 프롬프트를 보내려면 `make` 메서드 또는 일반적인 인스턴스 생성을 사용해 에이전트 객체를 만든 뒤 `prompt` 메서드를 호출하면 됩니다.

```php
$response = (new SalesCoach)
    ->prompt('Analyze this sales transcript...');

$response = SalesCoach::make()
    ->prompt('Analyze this sales transcript...');

return (string) $response;
```

`make` 메서드는 의존성 주입을 통해 컨테이너에서 에이전트를 해석합니다. 에이전트의 생성자에 인수를 직접 전달할 수도 있습니다.

```php
$agent = SalesCoach::make(user: $user);
```

추가적으로, `prompt` 메서드에 인자를 전달하여 기본 프로바이더, 모델, HTTP 타임아웃도 프롬프트 실행 시 오버라이드할 수 있습니다.

```php
$response = (new SalesCoach)->prompt(
    'Analyze this sales transcript...',
    provider: 'anthropic',
    model: 'claude-haiku-4-5-20251001',
    timeout: 120,
);
```

<a name="conversation-context"></a>
### 대화 컨텍스트 (Conversation Context)

에이전트가 `Conversational` 인터페이스를 구현한 경우, `messages` 메서드를 통해 이전 대화 컨텍스트(메시지 기록)를 반환할 수 있습니다.

```php
use App\Models\History;
use Laravel\Ai\Messages\Message;

/**
 * Get the list of messages comprising the conversation so far.
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
#### 대화 기억하기 (Remembering Conversations)

> [!NOTE]
> `RemembersConversations` 트레이트를 사용하기 전에 `vendor:publish` Artisan 명령어로 AI SDK 마이그레이션을 퍼블리시 및 실행해야 합니다. 이 마이그레이션은 대화 저장에 필요한 데이터베이스 테이블을 생성합니다.

에이전트의 대화 기록을 자동으로 저장/불러오고 싶다면 `RemembersConversations` 트레이트를 사용할 수 있습니다. 이 트레이트는 `Conversational` 인터페이스를 직접 구현하지 않아도 대화 메시지를 데이터베이스에 저장하는 간단한 방법을 제공합니다.

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
     * Get the instructions that the agent should follow.
     */
    public function instructions(): string
    {
        return 'You are a sales coach...';
    }
}
```

사용자별로 새로운 대화를 시작하려면 프롬프트 실행 전에 `forUser` 메서드를 호출하면 됩니다.

```php
$response = (new SalesCoach)->forUser($user)->prompt('Hello!');

$conversationId = $response->conversationId;
```

대화 ID는 응답에서 반환되므로 향후 참조를 위해 저장하거나, 사용자의 모든 대화 목록을 `agent_conversations` 테이블에서 조회할 수 있습니다.

기존 대화를 이어가려면 `continue` 메서드를 사용하세요.

```php
$response = (new SalesCoach)
    ->continue($conversationId, as: $user)
    ->prompt('Tell me more about that.');
```

`RemembersConversations` 트레이트를 사용하면 이전 메시지들이 자동으로 불러와져 대화 컨텍스트에 포함되고, 사용자/에이전트의 새로운 메시지도 매 상호작용마다 자동으로 저장됩니다.

<a name="structured-output"></a>
### 구조화된 출력 (Structured Output)

에이전트가 구조화된 출력을 반환하게 하려면 `HasStructuredOutput` 인터페이스를 구현하고, `schema` 메서드를 정의해야 합니다.

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
     * Get the agent's structured output schema definition.
     */
    public function schema(JsonSchema $schema): array
    {
        return [
            'score' => $schema->integer()->required(),
        ];
    }
}
```

구조화된 출력을 반환하는 에이전트에 프롬프트를 보내면, 반환된 `StructuredAgentResponse` 객체를 배열처럼 접근할 수 있습니다.

```php
$response = (new SalesCoach)->prompt('Analyze this sales transcript...');

return $response['score'];
```

<a name="attachments"></a>
### 첨부파일 (Attachments)

프롬프트 실행 시 첨부파일을 함께 전달하여, 모델이 이미지나 문서를 분석하도록 할 수 있습니다.

```php
use App\Ai\Agents\SalesCoach;
use Laravel\Ai\Files;

$response = (new SalesCoach)->prompt(
    'Analyze the attached sales transcript...',
    attachments: [
        Files\Document::fromStorage('transcript.pdf'), // 파일 시스템의 문서 첨부
        Files\Document::fromPath('/home/laravel/transcript.md'), // 로컬 경로 첨부
        $request->file('transcript'), // 업로드 파일 첨부
    ]
);
```

마찬가지로 `Laravel\Ai\Files\Image` 클래스를 사용해 이미지를 첨부할 수 있습니다.

```php
use App\Ai\Agents\ImageAnalyzer;
use Laravel\Ai\Files;

$response = (new ImageAnalyzer)->prompt(
    'What is in this image?',
    attachments: [
        Files\Image::fromStorage('photo.jpg'), // 파일 시스템 이미지 첨부
        Files\Image::fromPath('/home/laravel/photo.jpg'), // 로컬 경로 이미지
        $request->file('photo'), // 업로드 파일 첨부
    ]
);
```

<a name="streaming"></a>
### 스트리밍 (Streaming)

에이전트의 응답을 실시간으로 스트리밍하려면 `stream` 메서드를 사용합니다. 이때 반환되는 `StreamableAgentResponse`는 라우트에서 반환하여 클라이언트에게 SSE(서버-센트 이벤트) 방식의 스트리밍 응답을 즉시 전달할 수 있습니다.

```php
use App\Ai\Agents\SalesCoach;

Route::get('/coach', function () {
    return (new SalesCoach)->stream('Analyze this sales transcript...');
});
```

`then` 메서드를 사용하면 전체 응답이 클라이언트에 스트리밍된 후 실행될 클로저를 지정할 수 있습니다.

```php
use App\Ai\Agents\SalesCoach;
use Laravel\Ai\Responses\StreamedAgentResponse;

Route::get('/coach', function () {
    return (new SalesCoach)
        ->stream('Analyze this sales transcript...')
        ->then(function (StreamedAgentResponse $response) {
            // $response->text, $response->events, $response->usage...
        });
});
```

또는 스트림 이벤트를 직접 순회(iterate)할 수도 있습니다.

```php
$stream = (new SalesCoach)->stream('Analyze this sales transcript...');

foreach ($stream as $event) {
    // ...
}
```

<a name="streaming-using-the-vercel-ai-sdk-protocol"></a>
#### Vercel AI SDK 프로토콜로 스트리밍하기

[Vercel AI SDK 스트림 프로토콜](https://ai-sdk.dev/docs/ai-sdk-ui/stream-protocol)을 사용하려면 스트리밍 응답 객체에서 `usingVercelDataProtocol` 메서드를 호출하십시오.

```php
use App\Ai\Agents\SalesCoach;

Route::get('/coach', function () {
    return (new SalesCoach)
        ->stream('Analyze this sales transcript...')
        ->usingVercelDataProtocol();
});
```

<a name="broadcasting"></a>
### 브로드캐스팅 (Broadcasting)

스트리밍 이벤트를 다양한 방식으로 브로드캐스트할 수 있습니다. 먼저, 스트림 이벤트에서 `broadcast` 또는 `broadcastNow` 메서드를 직접 호출할 수 있습니다.

```php
use App\Ai\Agents\SalesCoach;
use Illuminate\Broadcasting\Channel;

$stream = (new SalesCoach)->stream('Analyze this sales transcript...');

foreach ($stream as $event) {
    $event->broadcast(new Channel('channel-name'));
}
```

또는 에이전트의 `broadcastOnQueue` 메서드를 사용해, 해당 에이전트 작업을 큐에 넣고, 스트리밍 이벤트가 발생할 때마다 브로드캐스트할 수 있습니다.

```php
(new SalesCoach)->broadcastOnQueue(
    'Analyze this sales transcript...',
    new Channel('channel-name'),
);
```

<a name="queueing"></a>
### 큐잉 (Queueing)

에이전트의 `queue` 메서드를 사용하면 에이전트 프롬프트 처리를 백그라운드에서 실행시켜, 애플리케이션의 반응성을 높일 수 있습니다. 응답이 도착하거나 예외가 발생할 때 실행될 클로저를 `then`, `catch`로 지정할 수 있습니다.

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
### 툴 (Tools)

툴을 활용하면 에이전트에 추가적인 기능을 제공할 수 있습니다. 툴은 `make:tool` Artisan 명령어로 생성할 수 있습니다.

```shell
php artisan make:tool RandomNumberGenerator
```

생성된 툴은 `app/Ai/Tools` 디렉터리에 위치하며, 각 툴에는 필요 시 에이전트가 호출하는 `handle` 메서드가 있습니다.

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
     * Get the description of the tool's purpose.
     */
    public function description(): Stringable|string
    {
        return 'This tool may be used to generate cryptographically secure random numbers.';
    }

    /**
     * Execute the tool.
     */
    public function handle(Request $request): Stringable|string
    {
        return (string) random_int($request['min'], $request['max']);
    }

    /**
     * Get the tool's schema definition.
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

툴 정의가 완료되면, 에이전트의 `tools` 메서드에서 반환하도록 합니다.

```php
use App\Ai\Tools\RandomNumberGenerator;

/**
 * Get the tools available to the agent.
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
#### 유사도 검색 (Similarity Search)

`SimilaritySearch` 툴을 통해 에이전트는 데이터베이스 내 저장된 벡터 임베딩을 이용해, 질의(query)와 유사한 문서 검색을 수행할 수 있습니다. 이는 RAG(검색 기반 생성)에 유용합니다.

가장 간단하게는 벡터 임베딩이 포함된 Eloquent 모델과 함께 `usingModel` 메서드를 사용하면 됩니다.

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

첫 번째 인수는 Eloquent 모델, 두 번째 인수는 벡터 임베딩 컬럼명입니다.

최소 유사도 임계치(0.0~1.0)와 커스텀 쿼리 클로저도 전달할 수 있습니다.

```php
SimilaritySearch::usingModel(
    model: Document::class,
    column: 'embedding',
    minSimilarity: 0.7,
    limit: 10,
    query: fn ($query) => $query->where('published', true),
),
```

더 깊은 커스터마이징이 필요하다면, 직접 클로저로 유사도 검색 툴을 생성할 수 있습니다.

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

`withDescription` 메서드로 툴 설명도 커스터마이즈할 수 있습니다.

```php
SimilaritySearch::usingModel(Document::class, 'embedding')
    ->withDescription('Search the knowledge base for relevant articles.'),
```

<a name="provider-tools"></a>
### 프로바이더 툴 (Provider Tools)

프로바이더 툴은 웹 검색, URL 데이터 가져오기, 파일 검색 등과 같이 AI 프로바이더 자체적으로 구현되는 특별한 툴입니다. 일반 툴과 달리, 프로바이더 툴은 애플리케이션이 아니라 프로바이더 쪽에서 실행됩니다.

프로바이더 툴도 일반 툴과 마찬가지로 에이전트의 `tools` 메서드에서 반환할 수 있습니다.

<a name="web-search"></a>
#### 웹 검색 (Web Search)

`WebSearch` 프로바이더 툴은 에이전트가 실시간으로 웹 검색을 수행하도록 합니다. 최신 이슈, 최근 데이터, 모델 학습 시점 이후 변경된 이슈 등에 대해 질문 답변 시 유용합니다.

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

웹 검색 툴을 통해 검색 횟수나 허용 도메인을 제한할 수 있습니다.

```php
(new WebSearch)->max(5)->allow(['laravel.com', 'php.net']),
```

사용자 위치 정보에 따라 검색 결과를 다르게 하려면 `location` 메서드를 이용하십시오.

```php
(new WebSearch)->location(
    city: 'New York',
    region: 'NY',
    country: 'US'
);
```

<a name="web-fetch"></a>
#### 웹 페치(Web Fetch)

`WebFetch` 프로바이더 툴은 웹 페이지의 내용을 직접 가져와 읽도록 에이전트에게 허용합니다. 특정 URL의 세부 정보 분석, 데이터 수집 등에 활용할 수 있습니다.

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

검색과 마찬가지로, 허용 도메인과 최대 가져오기 횟수를 제한할 수 있습니다.

```php
(new WebFetch)->max(3)->allow(['docs.laravel.com']),
```

<a name="file-search"></a>
#### 파일 검색 (File Search)

`FileSearch` 프로바이더 툴은 [벡터 스토어](#vector-stores)에 저장된 [파일](#files) 검색을 지원합니다. 이를 통해 에이전트가 업로드된 문서 내에서 관련 정보를 검색(=RAG)할 수 있습니다.

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

복수의 벡터 스토어에서 동시에 검색하려면 여러 ID를 지정하여 전달하면 됩니다.

```php
new FileSearch(stores: ['store_1', 'store_2']);
```

파일에 [메타데이터](#adding-files-to-stores)가 포함된 경우, 결과 필터링이 가능합니다. 단순 equals 필터라면 배열로 전달할 수 있습니다.

```php
new FileSearch(stores: ['store_id'], where: [
    'author' => 'Taylor Otwell',
    'year' => 2026,
]);
```

복잡한 필터링이 필요하면 클로저로 `FileSearchQuery` 객체를 활용하세요.

```php
use Laravel\Ai\Providers\Tools\FileSearchQuery;

new FileSearch(stores: ['store_id'], where: fn (FileSearchQuery $query) =>
    $query->where('author', 'Taylor Otwell')
        ->whereNot('status', 'draft')
        ->whereIn('category', ['news', 'updates'])
);
```

<a name="middleware"></a>
### 미들웨어 (Middleware)

에이전트는 미들웨어를 지원합니다. 미들웨어를 통해 프롬프트가 프로바이더로 전송되기 전에 가로채거나 수정할 수 있습니다. 미들웨어를 추가하려면 `HasMiddleware` 인터페이스를 구현하고, `middleware` 메서드에서 미들웨어 클래스 배열을 반환하세요.

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
     * Get the agent's middleware.
     */
    public function middleware(): array
    {
        return [
            new LogPrompts,
        ];
    }
}
```

각 미들웨어 클래스는 `handle` 메서드를 구현해야 하며, `AgentPrompt`와 다음 미들웨어를 실행할 `Closure`를 인수로 받습니다.

```php
<?php

namespace App\Ai\Middleware;

use Closure;
use Laravel\Ai\Prompts\AgentPrompt;

class LogPrompts
{
    /**
     * Handle the incoming prompt.
     */
    public function handle(AgentPrompt $prompt, Closure $next)
    {
        Log::info('Prompting agent', ['prompt' => $prompt->prompt]);

        return $next($prompt);
    }
}
```

응답이 완료된 후 추가 동작을 하려면, 응답 객체의 `then` 메서드를 활용할 수 있습니다. 동기/스트리밍 응답 모두에서 사용 가능합니다.

```php
public function handle(AgentPrompt $prompt, Closure $next)
{
    return $next($prompt)->then(function (AgentResponse $response) {
        Log::info('Agent responded', ['text' => $response->text]);
    });
}
```

<a name="anonymous-agents"></a>
### 익명 에이전트 (Anonymous Agents)

별도의 에이전트 클래스를 만들지 않고 간단히 AI 모델과 상호작용하고 싶을 때, `agent` 함수를 사용하여 임시(익명) 에이전트를 만들 수 있습니다.

```php
use function Laravel\Ai\{agent};

$response = agent(
    instructions: 'You are an expert at software development.',
    messages: [],
    tools: [],
)->prompt('Tell me about Laravel');
```

익명 에이전트도 구조화된 출력을 지원합니다.

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
### 에이전트 설정 (Agent Configuration)

에이전트의 텍스트 생성 옵션은 PHP 속성(Attribute)으로 간단하게 지정할 수 있습니다. 지원되는 속성:

- `MaxSteps`: 툴 사용 시 에이전트가 수행할 최대 단계 수
- `MaxTokens`: 모델이 생성할 최대 토큰 수
- `Model`: 에이전트가 사용할 모델
- `Provider`: 사용할 AI 프로바이더(복수 지정 시 페일오버)
- `Temperature`: 생성 샘플링 온도(0.0~1.0)
- `Timeout`: 에이전트 요청의 HTTP 타임아웃(초, 기본 60)
- `UseCheapestModel`: 비용 최적화 시 프로바이더의 가장 저렴한 모델 사용
- `UseSmartestModel`: 고난도 작업에 프로바이더의 최고 성능 모델 자동 선택

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

`UseCheapestModel` 과 `UseSmartestModel` 속성을 통해, 모델명을 직접 지정하지 않고도 해당 프로바이더의 가장 저렴한 모델이나 최고 성능 모델을 자동으로 선택할 수 있습니다. 비용 또는 성능 기준 최적화에 활용할 수 있습니다.

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
## 이미지 (Images)

`Laravel\Ai\Image` 클래스를 사용해 `openai`, `gemini`, `xai` 프로바이더로 이미지를 생성할 수 있습니다.

```php
use Laravel\Ai\Image;

$image = Image::of('A donut sitting on the kitchen counter')->generate();

$rawContent = (string) $image;
```

`square`, `portrait`, `landscape` 메서드로 이미지 비율을, `quality` 메서드로 이미지 품질(`high`, `medium`, `low`)을 지정할 수 있습니다. `timeout` 으로 HTTP 타임아웃(초)도 조정 가능합니다.

```php
use Laravel\Ai\Image;

$image = Image::of('A donut sitting on the kitchen counter')
    ->quality('high')
    ->landscape()
    ->timeout(120)
    ->generate();
```

참조 이미지는 `attachments` 메서드로 첨부할 수 있습니다.

```php
use Laravel\Ai\Files;
use Laravel\Ai\Image;

$image = Image::of('Update this photo of me to be in the style of an impressionist painting.')
    ->attachments([
        Files\Image::fromStorage('photo.jpg'),
        // Files\Image::fromPath('/home/laravel/photo.jpg'),
        // Files\Image::fromUrl('https://example.com/photo.jpg'),
        // $request->file('photo'),
    ])
    ->landscape()
    ->generate();
```

생성된 이미지는 애플리케이션의 `config/filesystems.php` 파일에 설정된 기본 디스크에 손쉽게 저장할 수 있습니다.

```php
$image = Image::of('A donut sitting on the kitchen counter');

$path = $image->store();
$path = $image->storeAs('image.jpg');
$path = $image->storePublicly();
$path = $image->storePubliclyAs('image.jpg');
```

이미지 생성 역시 큐잉이 가능합니다.

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
## 오디오 (Audio)

`Laravel\Ai\Audio` 클래스로 주어진 텍스트에서 오디오를 생성할 수 있습니다.

```php
use Laravel\Ai\Audio;

$audio = Audio::of('I love coding with Laravel.')->generate();

$rawContent = (string) $audio;
```

`male`, `female`, `voice` 메서드로 생성 음성(성별/음성 ID 등)을 선택할 수 있습니다.

```php
$audio = Audio::of('I love coding with Laravel.')
    ->female()
    ->generate();

$audio = Audio::of('I love coding with Laravel.')
    ->voice('voice-id-or-name')
    ->generate();
```

`instructions` 메서드로 오디오의 톤, 말투 등을 조절할 수도 있습니다.

```php
$audio = Audio::of('I love coding with Laravel.')
    ->female()
    ->instructions('Said like a pirate')
    ->generate();
```

생성된 오디오는 파일 시스템에 바로 저장할 수 있습니다.

```php
$audio = Audio::of('I love coding with Laravel.')->generate();

$path = $audio->store();
$path = $audio->storeAs('audio.mp3');
$path = $audio->storePublicly();
$path = $audio->storePubliclyAs('audio.mp3');
```

오디오 생성도 큐잉 지원합니다.

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
## 트랜스크립션 (Transcriptions)

`Laravel\Ai\Transcription` 클래스를 사용해 오디오 파일의 전사(트랜스크립션)를 얻을 수 있습니다.

```php
use Laravel\Ai\Transcription;

$transcript = Transcription::fromPath('/home/laravel/audio.mp3')->generate();
$transcript = Transcription::fromStorage('audio.mp3')->generate();
$transcript = Transcription::fromUpload($request->file('audio'))->generate();

return (string) $transcript;
```

`diarize` 메서드로 화자별로 분할된(diarized) 트랜스크립트까지 요청할 수 있습니다.

```php
$transcript = Transcription::fromStorage('audio.mp3')
    ->diarize()
    ->generate();
```

트랜스크립션 생성도 비동기 큐잉이 가능합니다.

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
## 임베딩 (Embeddings)

`Stringable` 객체의 `toEmbeddings` 메서드를 사용해 문자열에 대한 벡터 임베딩을 손쉽게 생성할 수 있습니다.

```php
use Illuminate\Support\Str;

$embeddings = Str::of('Napa Valley has great wine.')->toEmbeddings();
```

또는 `Embeddings` 클래스를 활용해 한 번에 여러 입력값의 임베딩을 생성할 수도 있습니다.

```php
use Laravel\Ai\Embeddings;

$response = Embeddings::for([
    'Napa Valley has great wine.',
    'Laravel is a PHP framework.',
])->generate();

$response->embeddings; // [[0.123, 0.456, ...], [0.789, 0.012, ...]]
```

임베딩의 차원 수, 사용 프로바이더도 명시 가능하며,

```php
$response = Embeddings::for(['Napa Valley has great wine.'])
    ->dimensions(1536)
    ->generate('openai', 'text-embedding-3-small');
```

<a name="querying-embeddings"></a>
### 임베딩 질의 (Querying Embeddings)

생성된 임베딩은 데이터베이스의 `vector` 컬럼에 저장했다가, 추후 유사도 검색이 가능합니다. PostgreSQL의 `pgvector` 확장 기능을 활용해, 마이그레이션 작성 시 `vector` 컬럼을 다음과 같이 정의합니다.

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

벡터 컬럼에 인덱스를 추가하면, 유사도 검색이 더욱 빨라집니다. `index`를 호출할 경우, 코사인 거리 기반 HNSW 인덱스가 자동 생성됩니다.

```php
$table->vector('embedding', dimensions: 1536)->index();
```

모델에서 벡터 컬럼은 `array`로 캐스팅해야 합니다.

```php
protected function casts(): array
{
    return [
        'embedding' => 'array',
    ];
}
```

유사한 레코드를 조회할 때는 `whereVectorSimilarTo` 메서드를 사용합니다. 이 메서드는 최소 코사인 유사도를 기준으로 결과를 필터링 및 정렬합니다.

```php
use App\Models\Document;

$documents = Document::query()
    ->whereVectorSimilarTo('embedding', $queryEmbedding, minSimilarity: 0.4)
    ->limit(10)
    ->get();
```

`$queryEmbedding`은 `float` 배열 또는 문자열을 지원합니다. 문자열 전달 시, 내부적으로 임베딩이 자동 생성됩니다.

```php
$documents = Document::query()
    ->whereVectorSimilarTo('embedding', 'best wineries in Napa Valley')
    ->limit(10)
    ->get();
```

더 세부 제어가 필요한 경우 `whereVectorDistanceLessThan`, `selectVectorDistance`, `orderByVectorDistance` 등을 조합할 수 있습니다.

```php
$documents = Document::query()
    ->select('*')
    ->selectVectorDistance('embedding', $queryEmbedding, as: 'distance')
    ->whereVectorDistanceLessThan('embedding', $queryEmbedding, maxDistance: 0.3)
    ->orderByVectorDistance('embedding', $queryEmbedding)
    ->limit(10)
    ->get();
```

에이전트에게 유사도 검색 능력을 부여하려면 [Similarity Search](#similarity-search) 툴 문서를 참고하세요.

> [!NOTE]
> 벡터 질의는 현재 PostgreSQL의 `pgvector` 확장이 적용된 연결에서만 지원됩니다.

<a name="caching-embeddings"></a>
### 임베딩 캐싱 (Caching Embeddings)

같은 입력값에 대한 임베딩 생성을 캐싱하면, 중복된 API 요청을 줄일 수 있습니다. 캐싱을 활성화하려면 `ai.caching.embeddings.cache` 설정 값을 `true`로 지정하세요.

```php
'caching' => [
    'embeddings' => [
        'cache' => true,
        'store' => env('CACHE_STORE', 'database'),
        // ...
    ],
],
```

캐시가 활성화되면 임베딩은 30일간 저장됩니다. 캐시 키는 프로바이더, 모델, 차원, 입력 내용을 기준으로 생성되어, 동일한 요청은 캐시 결과를, 다른 설정은 새 임베딩을 반환합니다.

글로벌 캐싱이 비활성 상태여도, `cache` 메서드로 특별히 요청별 캐싱을 지정할 수 있습니다.

```php
$response = Embeddings::for(['Napa Valley has great wine.'])
    ->cache()
    ->generate();
```

캐시 유효기간(초 단위)도 지정할 수 있습니다.

```php
$response = Embeddings::for(['Napa Valley has great wine.'])
    ->cache(seconds: 3600) // 1시간 캐시
    ->generate();
```

`toEmbeddings` 메서드도 `cache` 인수를 사용할 수 있습니다.

```php
// 기본 캐시 기간 사용
$embeddings = Str::of('Napa Valley has great wine.')->toEmbeddings(cache: true);

// 특정 기간 캐싱
$embeddings = Str::of('Napa Valley has great wine.')->toEmbeddings(cache: 3600);
```

<a name="reranking"></a>
## 재정렬(Reranking) (Reranking)

재정렬 기능은 주어진 질의(query)에 대해 문서 목록의 순위를 의미적으로 재조정합니다. 이를 활용하면 검색 결과의 품질을 높일 수 있습니다.

`Laravel\Ai\Reranking` 클래스를 사용해 문서를 재정렬할 수 있습니다.

```php
use Laravel\Ai\Reranking;

$response = Reranking::of([
    'Django is a Python web framework.',
    'Laravel is a PHP web application framework.',
    'React is a JavaScript library for building user interfaces.',
])->rerank('PHP frameworks');

// 상위 결과 접근
$response->first()->document; // "Laravel is a PHP web application framework."
$response->first()->score;    // 0.95
$response->first()->index;    // 1 (원본 순서)
```

`limit` 메서드로 상위 몇 개만 반환할지 제한할 수 있습니다.

```php
$response = Reranking::of($documents)
    ->limit(5)
    ->rerank('search query');
```

<a name="reranking-collections"></a>
### 컬렉션 재정렬 (Reranking Collections)

라라벨 컬렉션 객체도 `rerank` 매크로로 간단히 재정렬할 수 있습니다. 첫 번째 인수는 랭킹 기준 필드(또는 필드 배열), 두 번째 인수는 질의입니다.

```php
// 필드 단일 기준으로 재정렬
$posts = Post::all()
    ->rerank('body', 'Laravel tutorials');

// 복수 필드 기준 (JSON으로 전송)
$reranked = $posts->rerank(['title', 'body'], 'Laravel tutorials');

// 클로저로 문서 내용 만듦
$reranked = $posts->rerank(
    fn ($post) => $post->title.': '.$post->body,
    'Laravel tutorials'
);
```

상위 개수 제한, 프로바이더 지정 등도 지원합니다.

```php
$reranked = $posts->rerank(
    by: 'content',
    query: 'Laravel tutorials',
    limit: 10,
    provider: 'cohere'
);
```

<a name="files"></a>
## 파일 (Files)

`Laravel\Ai\Files` 혹은 각 파일 클래스를 사용해, AI 프로바이더에 파일을 저장하고 여러 대화에서 참고할 수 있습니다. 이는 대용량 문서 등 여러 차례 참조할 파일을 매번 재업로드하지 않고 사용할 때 유용합니다.

```php
use Laravel\Ai\Files\Document;
use Laravel\Ai\Files\Image;

// 로컬 경로 파일 저장
$response = Document::fromPath('/home/laravel/document.pdf')->put();
$response = Image::fromPath('/home/laravel/photo.jpg')->put();

// 파일 시스템의 파일 저장
$response = Document::fromStorage('document.pdf', disk: 'local')->put();
$response = Image::fromStorage('photo.jpg', disk: 'local')->put();

// 원격 URL의 파일 저장
$response = Document::fromUrl('https://example.com/document.pdf')->put();
$response = Image::fromUrl('https://example.com/photo.jpg')->put();

return $response->id;
```

원시 데이터나 업로드 파일도 저장할 수 있습니다.

```php
use Laravel\Ai\Files;
use Laravel\Ai\Files\Document;

// 원시 데이터 저장
$stored = Document::fromString('Hello, World!', 'text/plain')->put();

// 업로드 파일 저장
$stored = Document::fromUpload($request->file('document'))->put();
```

파일을 저장한 뒤에는, 같은 파일을 재업로드하지 않고, 파일 ID로 에이전트에 첨부할 수 있습니다.

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

저장된 파일을 다시 조회하려면 `get` 메서드를 사용하세요.

```php
use Laravel\Ai\Files\Document;

$file = Document::fromId('file-id')->get();

$file->id;
$file->mimeType();
```

파일을 삭제하려면 `delete` 메서드를 호출합니다.

```php
Document::fromId('file-id')->delete();
```

기본적으로 `Files` 클래스는 `config/ai.php`의 기본 프로바이더를 사용합니다. 대부분의 메서드에서 `provider` 인수로 다른 프로바이더를 지정할 수도 있습니다.

```php
$response = Document::fromPath(
    '/home/laravel/document.pdf'
)->put(provider: 'anthropic');
```

<a name="using-stored-files-in-conversations"></a>
### 저장 파일을 대화에서 사용하기

AI 프로바이더에 파일을 저장했다면, `fromId` 메서드로 에이전트 프롬프트에 첨부하여 재사용할 수 있습니다.

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

이미지도 동일하게 `Image` 클래스로 첨부 가능합니다.

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
## 벡터 스토어 (Vector Stores)

벡터 스토어는 검색 및 RAG(검색 기반 생성)에 사용할 수 있는 파일 모음(컬렉션)을 만들어줍니다. `Laravel\Ai\Stores` 클래스에서 벡터 스토어 생성, 조회, 삭제 기능을 제공합니다.

```php
use Laravel\Ai\Stores;

// 새 벡터 스토어 생성
$store = Stores::create('Knowledge Base');

// 추가 옵션과 함께 스토어 생성
$store = Stores::create(
    name: 'Knowledge Base',
    description: 'Documentation and reference materials.',
    expiresWhenIdleFor: days(30),
);

return $store->id;
```

ID로 기존 벡터 스토어를 조회하려면 `get` 사용

```php
use Laravel\Ai\Stores;

$store = Stores::get('store_id');

$store->id;
$store->name;
$store->fileCounts;
$store->ready;
```

벡터 스토어 삭제는 ID로 또는 인스턴스에서 직접 할 수 있습니다.

```php
use Laravel\Ai\Stores;

// ID로 삭제
Stores::delete('store_id');

// 인스턴스로 삭제
$store = Stores::get('store_id');

$store->delete();
```

<a name="adding-files-to-stores"></a>
### 스토어에 파일 추가 (Adding Files to Stores)

벡터 스토어가 준비되면, `add` 메서드로 [파일](#files)을 추가할 수 있습니다. 추가된 파일은 자동으로 의미적 인덱싱이 적용되어 [파일 검색 툴](#file-search)로 검색할 수 있습니다.

```php
use Laravel\Ai\Files\Document;
use Laravel\Ai\Stores;

$store = Stores::get('store_id');

// 이미 프로바이더에 저장된 파일 추가
$document = $store->add('file_id');
$document = $store->add(Document::fromId('file_id'));

// 저장과 추가를 동시에
$document = $store->add(Document::fromPath('/path/to/document.pdf'));
$document = $store->add(Document::fromStorage('manual.pdf'));
$document = $store->add($request->file('document'));

$document->id;
$document->fileId;
```

> [!NOTE]
> 이미 저장된 파일을 벡터 스토어에 추가할 때, 반환되는 document ID가 기존 file ID와 항상 같지는 않습니다. 일부 벡터 프로바이더는 별도 document ID를 반환하므로, 두 ID를 모두 DB에 저장하길 권장합니다.

파일을 스토어에 추가할 때 메타데이터를 첨부하면, [파일 검색 툴](#file-search) 사용 시 결과 필터링에 활용할 수 있습니다.

```php
$store->add(Document::fromPath('/path/to/document.pdf'), metadata: [
    'author' => 'Taylor Otwell',
    'department' => 'Engineering',
    'year' => 2026,
]);
```

스토어에서 파일을 삭제하려면 `remove` 메서드를 사용하세요.

```php
$store->remove('file_id');
```

이때 파일 스토리지에서 지우지는 않으므로, 완전 삭제는 `deleteFile` 인수를 true로 전달합니다.

```php
$store->remove('file_abc123', deleteFile: true);
```

<a name="failover"></a>
## 페일오버 (Failover)

프롬프트 실행이나 미디어 생성 시, 프로바이더 또는 모델 배열을 지정하면, 기본 프로바이더에 장애나 과부하가 발생할 경우 자동으로 다음 프로바이더/모델로 페일오버할 수 있습니다.

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
## 테스트 (Testing)

<a name="testing-agents"></a>
### 에이전트 (Agents)

테스트 시 에이전트의 응답을 가짜로 처리하려면 `fake` 메서드를 호출하세요. 응답 목록, 또는 클로저로 커스텀이 가능합니다.

```php
use App\Ai\Agents\SalesCoach;
use Laravel\Ai\Prompts\AgentPrompt;

// 모든 프롬프트에 고정 응답
SalesCoach::fake();

// 프롬프트별 응답 목록 지정
SalesCoach::fake([
    'First response',
    'Second response',
]);

// 프롬프트에 따라 동적으로 응답
SalesCoach::fake(function (AgentPrompt $prompt) {
    return 'Response for: '.$prompt->prompt;
});
```

> [!NOTE]
> 구조화된 출력을 반환하는 에이전트에 대해 `Agent::fake()` 를 호출하면, 에이전트의 스키마에 맞는 더미 데이터가 자동 생성됩니다.

프롬프트 후, 실제 전달된 프롬프트에 대한 단언문 사용이 가능합니다.

```php
use Laravel\Ai\Prompts\AgentPrompt;

SalesCoach::assertPrompted('Analyze this...');

SalesCoach::assertPrompted(function (AgentPrompt $prompt) {
    return $prompt->contains('Analyze');
});

SalesCoach::assertNotPrompted('Missing prompt');

SalesCoach::assertNeverPrompted();
```

큐잉된 에이전트 호출은 별도의 큐 단언문을 사용합니다.

```php
use Laravel\Ai\QueuedAgentPrompt;

SalesCoach::assertQueued('Analyze this...');

SalesCoach::assertQueued(function (QueuedAgentPrompt $prompt) {
    return $prompt->contains('Analyze');
});

SalesCoach::assertNotQueued('Missing prompt');

SalesCoach::assertNeverQueued();
```

모든 호출에 대해 페이크 응답이 요구되도록 `preventStrayPrompts`를 사용할 수 있습니다. 페이크 응답 없는 호출 시 예외가 발생합니다.

```php
SalesCoach::fake()->preventStrayPrompts();
```

<a name="testing-images"></a>
### 이미지 (Images)

이미지 생성을 테스트에서 가짜로 처리하려면 `Image::fake()`를 호출하세요. 이후 다양한 단언문 사용이 가능합니다.

```php
use Laravel\Ai\Image;
use Laravel\Ai\Prompts\ImagePrompt;
use Laravel\Ai\Prompts\QueuedImagePrompt;

// 모든 프롬프트에 고정 응답
Image::fake();

// 응답 목록 지정
Image::fake([
    base64_encode($firstImage),
    base64_encode($secondImage),
]);

// 동적으로 응답
Image::fake(function (ImagePrompt $prompt) {
    return base64_encode('...');
});
```

프롬프트별 단언문

```php
Image::assertGenerated(function (ImagePrompt $prompt) {
    return $prompt->contains('sunset') && $prompt->isLandscape();
});

Image::assertNotGenerated('Missing prompt');

Image::assertNothingGenerated();
```

큐 이미지 생성 단언

```php
Image::assertQueued(
    fn (QueuedImagePrompt $prompt) => $prompt->contains('sunset')
);

Image::assertNotQueued('Missing prompt');

Image::assertNothingQueued();
```

모든 호출에 페이크 응답 강제 적용

```php
Image::fake()->preventStrayImages();
```

<a name="testing-audio"></a>
### 오디오 (Audio)

오디오 생성도 `Audio::fake()`로 페이크 처리 및 단언이 가능합니다.

```php
use Laravel\Ai\Audio;
use Laravel\Ai\Prompts\AudioPrompt;
use Laravel\Ai\Prompts\QueuedAudioPrompt;

// 모든 프롬프트에 고정 응답
Audio::fake();

// 응답 목록 지정
Audio::fake([
    base64_encode($firstAudio),
    base64_encode($secondAudio),
]);

// 동적으로 응답
Audio::fake(function (AudioPrompt $prompt) {
    return base64_encode('...');
});
```

단언문

```php
Audio::assertGenerated(function (AudioPrompt $prompt) {
    return $prompt->contains('Hello') && $prompt->isFemale();
});

Audio::assertNotGenerated('Missing prompt');

Audio::assertNothingGenerated();
```

큐 오디오 생성 단언

```php
Audio::assertQueued(
    fn (QueuedAudioPrompt $prompt) => $prompt->contains('Hello')
);

Audio::assertNotQueued('Missing prompt');

Audio::assertNothingQueued();
```

모든 호출에 페이크 응답 강제 적용

```php
Audio::fake()->preventStrayAudio();
```

<a name="testing-transcriptions"></a>
### 트랜스크립션 (Transcriptions)

트랜스크립션도 `Transcription::fake()`로 페이크 처리 및 단언이 가능합니다.

```php
use Laravel\Ai\Transcription;
use Laravel\Ai\Prompts\TranscriptionPrompt;
use Laravel\Ai\Prompts\QueuedTranscriptionPrompt;

// 기본 응답
Transcription::fake();

// 응답 목록
Transcription::fake([
    'First transcription text.',
    'Second transcription text.',
]);

// 동적 응답
Transcription::fake(function (TranscriptionPrompt $prompt) {
    return 'Transcribed text...';
});
```

단언문

```php
Transcription::assertGenerated(function (TranscriptionPrompt $prompt) {
    return $prompt->language === 'en' && $prompt->isDiarized();
});

Transcription::assertNotGenerated(
    fn (TranscriptionPrompt $prompt) => $prompt->language === 'fr'
);

Transcription::assertNothingGenerated();
```

큐 트랜스크립션 단언

```php
Transcription::assertQueued(
    fn (QueuedTranscriptionPrompt $prompt) => $prompt->isDiarized()
);

Transcription::assertNotQueued(
    fn (QueuedTranscriptionPrompt $prompt) => $prompt->language === 'fr'
);

Transcription::assertNothingQueued();
```

모든 호출에 페이크 응답 강제 적용

```php
Transcription::fake()->preventStrayTranscriptions();
```

<a name="testing-embeddings"></a>
### 임베딩 (Embeddings)

임베딩 생성도 `Embeddings::fake()`로 페이크 처리 및 단언 가능

```php
use Laravel\Ai\Embeddings;
use Laravel\Ai\Prompts\EmbeddingsPrompt;
use Laravel\Ai\Prompts\QueuedEmbeddingsPrompt;

// 기본 임베딩(지정 차원수 더미) 생성
Embeddings::fake();

// 응답 목록 전달
Embeddings::fake([
    [$firstEmbeddingVector],
    [$secondEmbeddingVector],
]);

// 동적 응답
Embeddings::fake(function (EmbeddingsPrompt $prompt) {
    return array_map(
        fn () => Embeddings::fakeEmbedding($prompt->dimensions),
        $prompt->inputs
    );
});
```

단언문

```php
Embeddings::assertGenerated(function (EmbeddingsPrompt $prompt) {
    return $prompt->contains('Laravel') && $prompt->dimensions === 1536;
});

Embeddings::assertNotGenerated(
    fn (EmbeddingsPrompt $prompt) => $prompt->contains('Other')
);

Embeddings::assertNothingGenerated();
```

큐 임베딩 단언

```php
Embeddings::assertQueued(
    fn (QueuedEmbeddingsPrompt $prompt) => $prompt->contains('Laravel')
);

Embeddings::assertNotQueued(
    fn (QueuedEmbeddingsPrompt $prompt) => $prompt->contains('Other')
);

Embeddings::assertNothingQueued();
```

모든 호출에 페이크 응답 강제 적용

```php
Embeddings::fake()->preventStrayEmbeddings();
```

<a name="testing-reranking"></a>
### 재정렬 (Reranking)

재정렬 작업도 `Reranking::fake()`로 페이크 처리

```php
use Laravel\Ai\Reranking;
use Laravel\Ai\Prompts\RerankingPrompt;
use Laravel\Ai\Responses\Data\RankedDocument;

// 기본 응답
Reranking::fake();

// 커스텀 응답 지정
Reranking::fake([
    [
        new RankedDocument(index: 0, document: 'First', score: 0.95),
        new RankedDocument(index: 1, document: 'Second', score: 0.80),
    ],
]);
```

단언문

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
### 파일 (Files)

파일 작업을 테스트에서 가짜로 처리하려면 `Files::fake()`를 호출하세요.

```php
use Laravel\Ai\Files;

Files::fake();
```

파일 업로드 및 삭제 단언도 지원

```php
use Laravel\Ai\Contracts\Files\StorableFile;
use Laravel\Ai\Files\Document;

// 파일 저장
Document::fromString('Hello, Laravel!', mime: 'text/plain')
    ->as('hello.txt')
    ->put();

// 저장 단언
Files::assertStored(fn (StorableFile $file) =>
    (string) $file === 'Hello, Laravel!' &&
        $file->mimeType() === 'text/plain';
);

Files::assertNotStored(fn (StorableFile $file) =>
    (string) $file === 'Hello, World!'
);

Files::assertNothingStored();
```

파일 삭제 단언문

```php
Files::assertDeleted('file-id');
Files::assertNotDeleted('file-id');
Files::assertNothingDeleted();
```

<a name="testing-vector-stores"></a>
### 벡터 스토어 (Vector Stores)

벡터 스토어 작업도 `Stores::fake()`로 가짜 처리(파일 작업도 자동으로 페이크)

```php
use Laravel\Ai\Stores;

Stores::fake();
```

스토어 생성/삭제 단언

```php
use Laravel\Ai\Stores;

// 스토어 생성
$store = Stores::create('Knowledge Base');

// 생성 단언
Stores::assertCreated('Knowledge Base');

Stores::assertCreated(fn (string $name, ?string $description) =>
    $name === 'Knowledge Base'
);

Stores::assertNotCreated('Other Store');

Stores::assertNothingCreated();
```

스토어 삭제 단언

```php
Stores::assertDeleted('store_id');
Stores::assertNotDeleted('other_store_id');
Stores::assertNothingDeleted();
```

스토어 인스턴스별 파일 추가/삭제 단언 사용

```php
Stores::fake();

$store = Stores::get('store_id');

// 파일 추가/삭제
$store->add('added_id');
$store->remove('removed_id');

// 단언
$store->assertAdded('added_id');
$store->assertRemoved('removed_id');

$store->assertNotAdded('other_file_id');
$store->assertNotRemoved('other_file_id');
```

파일 ID를 모를 경우(동시 스토리지+스토어 등록 시)는, 클로저로 파일 내용 단언

```php
use Laravel\Ai\Contracts\Files\StorableFile;
use Laravel\Ai\Files\Document;

$store->add(Document::fromString('Hello, World!', 'text/plain')->as('hello.txt'));

$store->assertAdded(fn (StorableFile $file) => $file->name() === 'hello.txt');
$store->assertAdded(fn (StorableFile $file) => $file->content() === 'Hello, World!');
```

<a name="events"></a>
## 이벤트 (Events)

Laravel AI SDK는 [이벤트](/docs/master/events)를 다양하게 디스패치합니다. 대표적인 이벤트는 다음과 같습니다.

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

이러한 이벤트들을 활용해 AI SDK 사용 내역을 기록하거나 별도의 로깅 로직을 구현할 수 있습니다.
