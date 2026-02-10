# Laravel AI SDK (Laravel AI SDK)

- [소개](#introduction)
- [설치](#installation)
    - [구성](#configuration)
    - [커스텀 베이스 URL](#custom-base-urls)
    - [제공자 지원](#provider-support)
- [에이전트](#agents)
    - [프롬프트 작성](#prompting)
    - [대화 컨텍스트](#conversation-context)
    - [구조화 출력](#structured-output)
    - [첨부 파일](#attachments)
    - [스트리밍](#streaming)
    - [브로드캐스팅](#broadcasting)
    - [큐잉](#queueing)
    - [툴](#tools)
    - [제공자 툴](#provider-tools)
    - [미들웨어](#middleware)
    - [익명 에이전트](#anonymous-agents)
    - [에이전트 설정](#agent-configuration)
- [이미지](#images)
- [오디오 (TTS)](#audio)
- [트랜스크립션 (STT)](#transcription)
- [임베딩](#embeddings)
    - [임베딩 질의](#querying-embeddings)
    - [임베딩 캐싱](#caching-embeddings)
- [리랭킹](#reranking)
- [파일](#files)
- [벡터 스토어](#vector-stores)
    - [스토어에 파일 추가하기](#adding-files-to-stores)
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
## 소개 (Introduction)

[Laravel AI SDK](https://github.com/laravel/ai)는 OpenAI, Anthropic, Gemini 등과 같은 AI 제공자들과 상호작용할 수 있도록 통일되고 표현력이 풍부한 API를 제공합니다. AI SDK를 사용하면 도구와 구조화 출력을 가진 지능형 에이전트를 생성하고, 이미지를 만들고, 오디오를 합성 및 트랜스크립션하며, 벡터 임베딩을 생성하는 등 다양한 AI 기능을 일관되고 Laravel 친화적인 인터페이스로 사용할 수 있습니다.

<a name="installation"></a>
## 설치 (Installation)

Composer를 사용하여 Laravel AI SDK를 설치할 수 있습니다:

```shell
composer require laravel/ai
```

이후, `vendor:publish` Artisan 명령어를 통해 AI SDK 설정 및 마이그레이션 파일을 퍼블리시해 주세요:

```shell
php artisan vendor:publish --provider="Laravel\Ai\AiServiceProvider"
```

마지막으로 애플리케이션의 데이터베이스 마이그레이션을 실행해야 합니다. 이 과정에서 AI SDK가 대화 저장을 위해 사용하는 `agent_conversations` 및 `agent_conversation_messages` 테이블이 생성됩니다:

```shell
php artisan migrate
```

<a name="configuration"></a>
### 구성 (Configuration)

AI 제공자 인증 정보를 애플리케이션의 `config/ai.php` 설정 파일 또는 `.env` 환경 변수 파일에 정의할 수 있습니다:

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

텍스트, 이미지, 오디오, 트랜스크립션, 임베딩에 사용되는 기본 모델도 `config/ai.php` 파일에서 설정할 수 있습니다.

<a name="custom-base-urls"></a>
### 커스텀 베이스 URL (Custom Base URLs)

기본적으로 Laravel AI SDK는 각 제공자의 공개 API 엔드포인트에 직접 연결합니다. 하지만 API 키 관리를 중앙화하거나, 레이트 리미팅(요청 수 제한) 구현, 기업용 게이트웨이 경유 요청 등 다양한 사유로 다른 엔드포인트를 통해 요청을 전달해야 할 수도 있습니다.

이런 경우, 제공자 설정에 `url` 파라미터를 추가하여 커스텀 베이스 URL을 지정할 수 있습니다:

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

이 방식은 LiteLLM 또는 Azure OpenAI Gateway와 같은 프록시 서비스를 이용하거나, 대체 엔드포인트를 통해 요청할 때 유용합니다.

커스텀 베이스 URL은 다음 제공자에서 지원됩니다: OpenAI, Anthropic, Gemini, Groq, Cohere, DeepSeek, xAI, OpenRouter.

<a name="provider-support"></a>
### 제공자 지원 (Provider Support)

AI SDK는 다양한 기능에 대해 여러 제공자를 지원합니다. 다음 표는 각 기능별로 지원되는 제공자를 요약한 것입니다:

| 기능 | 지원 제공자 |
|---|---|
| 텍스트 | OpenAI, Anthropic, Gemini, Groq, xAI, DeepSeek, Mistral, Ollama |
| 이미지 | OpenAI, Gemini, xAI |
| TTS | OpenAI, ElevenLabs |
| STT | OpenAI, ElevenLabs, Mistral |
| 임베딩 | OpenAI, Gemini, Cohere, Mistral, Jina, VoyageAI |
| 리랭킹 | Cohere, Jina |
| 파일 | OpenAI, Anthropic, Gemini |

<a name="agents"></a>
## 에이전트 (Agents)

에이전트는 Laravel AI SDK에서 AI 제공자와 상호작용하기 위한 핵심 단위입니다. 각 에이전트는 명령어, 대화 컨텍스트, 사용할 수 있는 도구, 출력 스키마를 캡슐화하는 전용 PHP 클래스로, 대형 언어 모델과의 상호작용을 좀 더 명확하게 설계할 수 있습니다. 에이전트는 한 번만 설정해두면, 필요할 때마다 프롬프트를 주고받으며, 판매 코치, 문서 분석가, 지원 챗봇 등 다양한 역할에 맞춘 “특화된” 조수로 볼 수 있습니다.

다음 Artisan 명령어로 에이전트를 생성할 수 있습니다:

```shell
php artisan make:agent SalesCoach

php artisan make:agent SalesCoach --structured
```

생성된 클래스 내에서는 시스템 프롬프트·명령어, 메시지 컨텍스트, 사용할 수 있는 도구, 출력 스키마(적용할 경우) 등을 정의할 수 있습니다:

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
     * 에이전트가 따라야 할 명령어를 반환합니다.
     */
    public function instructions(): Stringable|string
    {
        return 'You are a sales coach, analyzing transcripts and providing feedback and an overall sales strength score.';
    }

    /**
     * 지금까지의 대화를 이루는 메시지 목록을 반환합니다.
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
     * 에이전트가 사용할 수 있는 도구 목록을 반환합니다.
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
     * 에이전트의 구조화 출력 스키마 정의를 반환합니다.
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
### 프롬프트 작성 (Prompting)

에이전트에게 프롬프트를 전달하려면, 먼저 `make` 메서드 또는 일반적인 인스턴스 생성을 통해 인스턴스를 생성한 후 `prompt` 메서드를 호출합니다:

```php
$response = (new SalesCoach)
    ->prompt('Analyze this sales transcript...');

$response = SalesCoach::make()
    ->prompt('Analyze this sales transcript...');

return (string) $response;
```

`make` 메서드는 에이전트를 컨테이너에서 해결하여 자동 의존성 주입을 지원합니다. 또한 생성자 인수도 전달할 수 있습니다:

```php
$agent = SalesCoach::make(user: $user);
```

추가 인수를 `prompt` 메서드에 전달하면, 프롬프트 시 기본 제공자, 모델, HTTP 타임아웃 등을 오버라이드할 수 있습니다:

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

에이전트가 `Conversational` 인터페이스를 구현한 경우, `messages` 메서드를 사용하여 이전 대화 컨텍스트를 반환할 수 있습니다:

```php
use App\Models\History;
use Laravel\Ai\Messages\Message;

/**
 * 지금까지 대화를 이루는 메시지 목록을 반환합니다.
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

> **Note:** `RemembersConversations` 트레이트를 사용하기 전에, 반드시 `vendor:publish` Artisan 명령어로 AI SDK 마이그레이션을 퍼블리시하고 실행해야 합니다. 마이그레이션을 실행하면 대화 저장에 필요한 데이터베이스 테이블이 만들어집니다.

Laravel이 에이전트의 대화 기록을 자동으로 저장·복원하도록 하려면, `RemembersConversations` 트레이트를 사용하면 됩니다. 이 트레이트는 직접 `Conversational` 인터페이스 구현 없이 대화 메시지를 데이터베이스에 쉽게 영속화할 수 있도록 도와줍니다:

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
     * 에이전트가 따라야 할 명령어를 반환합니다.
     */
    public function instructions(): string
    {
        return 'You are a sales coach...';
    }
}
```

대화를 새로 시작할 때는 프롬프트 전에 `forUser` 메서드를 호출하세요:

```php
$response = (new SalesCoach)->forUser($user)->prompt('Hello!');

$conversationId = $response->conversationId;
```

대화 ID는 응답에서 반환되며, 추후 참조를 위해 저장하거나, 직접 `agent_conversations` 테이블에서 특정 사용자의 모든 대화를 조회할 수 있습니다.

기존 대화를 이어가려면 `continue` 메서드를 사용하세요:

```php
$response = (new SalesCoach)
    ->continue($conversationId, as: $user)
    ->prompt('Tell me more about that.');
```

`RemembersConversations` 트레이트를 사용할 때는 이전 메시지가 자동으로 로딩되어 프롬프트 컨텍스트에 포함되며, 새로운 메시지(사용자 및 어시스턴트 메시지)는 매 상호작용 이후 자동으로 저장됩니다.

<a name="structured-output"></a>
### 구조화 출력 (Structured Output)

에이전트가 구조화 된 출력을 반환하도록 하고 싶다면, `HasStructuredOutput` 인터페이스를 구현하고 에이전트의 `schema` 메서드를 정의해 주세요:

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
     * 에이전트의 구조화 출력 스키마 정의를 반환합니다.
     */
    public function schema(JsonSchema $schema): array
    {
        return [
            'score' => $schema->integer()->required(),
        ];
    }
}
```

구조화 출력을 반환하는 에이전트에 프롬프트를 보낼 경우, 반환된 `StructuredAgentResponse` 객체를 배열처럼 접근할 수 있습니다:

```php
$response = (new SalesCoach)->prompt('Analyze this sales transcript...');

return $response['score'];
```

<a name="attachments"></a>
### 첨부 파일 (Attachments)

프롬프트 전달 시, 이미지나 문서 등 첨부 파일을 함께 전달할 수 있습니다. 이를 통해 모델이 첨부된 자료를 분석할 수 있습니다:

```php
use App\Ai\Agents\SalesCoach;
use Laravel\Ai\Files;

$response = (new SalesCoach)->prompt(
    'Analyze the attached sales transcript...',
    attachments: [
        Files\Document::fromStorage('transcript.pdf') // 파일 시스템 디스크에서 첨부...
        Files\Document::fromPath('/home/laravel/transcript.md') // 로컬 경로에서 첨부...
        $request->file('transcript'), // 업로드된 파일 첨부...
    ]
);
```

마찬가지로 `Laravel\Ai\Files\Image` 클래스를 사용하여 이미지도 첨부할 수 있습니다:

```php
use App\Ai\Agents\ImageAnalyzer;
use Laravel\Ai\Files;

$response = (new ImageAnalyzer)->prompt(
    'What is in this image?',
    attachments: [
        Files\Image::fromStorage('photo.jpg') // 파일 시스템 디스크에서 첨부...
        Files\Image::fromPath('/home/laravel/photo.jpg') // 로컬 경로에서 첨부...
        $request->file('photo'), // 업로드된 파일 첨부...
    ]
);
```

<a name="streaming"></a>
### 스트리밍 (Streaming)

에이전트의 응답을 스트리밍 방식으로 받으려면 `stream` 메서드를 호출하세요. 반환된 `StreamableAgentResponse`는 라우트에서 그대로 반환할 수 있으며, 클라이언트에 스트리밍 응답(SSE)이 전송됩니다:

```php
use App\Ai\Agents\SalesCoach;

Route::get('/coach', function () {
    return (new SalesCoach)->stream('Analyze this sales transcript...');
});
```

전체 응답 스트림 완료 시 호출될 클로저를 `then` 메서드로 등록할 수 있습니다:

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

또는 스트림 이벤트를 직접 이터레이션 처리할 수도 있습니다:

```php
$stream = (new SalesCoach)->stream('Analyze this sales transcript...');

foreach ($stream as $event) {
    // ...
}
```

<a name="streaming-using-the-vercel-ai-sdk-protocol"></a>
#### Vercel AI SDK 프로토콜을 이용한 스트리밍

[Vercel AI SDK 스트림 프로토콜](https://ai-sdk.dev/docs/ai-sdk-ui/stream-protocol)을 활용하려면 `usingVercelDataProtocol` 메서드를 스트림 응답에서 호출하세요:

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

스트리밍되는 이벤트는 여러 방식으로 브로드캐스트할 수 있습니다. 먼저, 각 스트림 이벤트에서 `broadcast` 또는 `broadcastNow` 메서드를 호출해 채널로 브로드캐스트할 수 있습니다:

```php
use App\Ai\Agents\SalesCoach;
use Illuminate\Broadcasting\Channel;

$stream = (new SalesCoach)->stream('Analyze this sales transcript...');

foreach ($stream as $event) {
    $event->broadcast(new Channel('channel-name'));
}
```

또는, 에이전트의 `broadcastOnQueue` 메서드를 통해 에이전트 작업을 큐에 등록하고, 사용 가능한 스트림 이벤트가 발생할 때마다 브로드캐스트할 수 있습니다:

```php
(new SalesCoach)->broadcastOnQueue(
    'Analyze this sales transcript...'
    new Channel('channel-name'),
);
```

<a name="queueing"></a>
### 큐잉 (Queueing)

에이전트의 `queue` 메서드를 사용하면 프롬프트 처리를 백그라운드에서 수행할 수 있어, 애플리케이션의 응답성을 유지할 수 있습니다. 응답이 준비되거나 예외가 발생할 때 실행될 클로저는 `then` 및 `catch` 메서드로 등록합니다:

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

툴은 에이전트가 프롬프트에 응답할 때 추가적인 기능을 사용할 수 있게 해줍니다. 툴은 다음 Artisan 명령어로 생성할 수 있습니다:

```shell
php artisan make:tool RandomNumberGenerator
```

생성된 툴 클래스는 `app/Ai/Tools` 디렉터리에 위치합니다. 각 툴은 에이전트가 도구를 사용해야 할 때 호출되는 `handle` 메서드를 정의합니다:

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
     * 툴의 목적 설명을 반환합니다.
     */
    public function description(): Stringable|string
    {
        return 'This tool may be used to generate cryptographically secure random numbers.';
    }

    /**
     * 툴을 실행합니다.
     */
    public function handle(Request $request): Stringable|string
    {
        return (string) random_int($request['min'], $request['max']);
    }

    /**
     * 툴의 스키마 정의를 반환합니다.
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

툴을 정의한 후 에이전트의 `tools` 메서드에서 반환하면 됩니다:

```php
use App\Ai\Tools\RandomNumberGenerator;

/**
 * 에이전트가 사용할 수 있는 도구 목록을 반환합니다.
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

`SimilaritySearch` 툴을 사용하면, 데이터베이스에 저장된 벡터 임베딩을 기반으로 쿼리에 유사한 문서를 검색할 수 있습니다. 이는 RAG(검색 기반 생성)와 같이 에이전트에게 애플리케이션의 데이터 검색 기능을 부여할 때 유용합니다.

가장 간단하게는 `usingModel` 메서드에 벡터 임베딩 컬럼을 가진 Eloquent 모델을 지정하여 유사도 검색 툴을 만들 수 있습니다:

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

첫 번째 인자는 Eloquent 모델 클래스, 두 번째 인자는 벡터 임베딩이 저장된 컬럼명입니다.

`minSimilarity`(0.0~1.0), 커스텀 쿼리 클로저 등 추가 옵션도 지원합니다:

```php
SimilaritySearch::usingModel(
    model: Document::class,
    column: 'embedding',
    minSimilarity: 0.7,
    limit: 10,
    query: fn ($query) => $query->where('published', true),
),
```

더 세밀한 제어가 필요하다면 결과 반환용 클로저로 직접 유사도 검색 툴을 생성할 수 있습니다:

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

툴의 설명은 `withDescription` 메서드로 커스텀할 수 있습니다:

```php
SimilaritySearch::usingModel(Document::class, 'embedding')
    ->withDescription('Search the knowledge base for relevant articles.'),
```

<a name="provider-tools"></a>
### 제공자 툴 (Provider Tools)

제공자 툴은 웹 검색, URL 패칭, 파일 검색 등 AI 제공자가 자체적으로 지원하는 기능입니다. 일반 툴과 달리, 제공자 툴의 실행은 애플리케이션이 아니라 해당 AI 제공자에서 이루어집니다.

제공자 툴 역시 에이전트의 `tools` 메서드에서 반환하면 됩니다.

<a name="web-search"></a>
#### 웹 검색 (Web Search)

`WebSearch` 제공자 툴은 에이전트가 웹에서 실시간 정보를 검색할 수 있도록 해줍니다. 최근 이슈나 학습 시점 이후 변경된 데이터 등 현재성 있는 질의에 적합합니다.

**지원 제공자:** Anthropic, OpenAI, Gemini

```php
use Laravel\Ai\Providers\Tools\WebSearch;

public function tools(): iterable
{
    return [
        new WebSearch,
    ];
}
```

검색 횟수 제한이나 도메인 제한도 설정할 수 있습니다:

```php
(new WebSearch)->max(5)->allow(['laravel.com', 'php.net']),
```

사용자 위치에 따라 결과를 세분화하려면 `location` 메서드를 사용하세요:

```php
(new WebSearch)->location(
    city: 'New York',
    region: 'NY',
    country: 'US'
);
```

<a name="web-fetch"></a>
#### 웹 패치(Web Fetch)

`WebFetch` 제공자 툴로 에이전트가 특정 웹페이지의 내용을 가져와서 분석할 수 있습니다. 알려진 URL을 지정 분석하거나, 정밀한 정보 취득이 필요한 경우에 유용합니다.

**지원 제공자:** Anthropic, Gemini

```php
use Laravel\Ai\Providers\Tools\WebFetch;

public function tools(): iterable
{
    return [
        new WebFetch,
    ];
}
```

최대 호출 수나 허용 도메인 제한을 둘 수 있습니다:

```php
(new WebFetch)->max(3)->allow(['docs.laravel.com']),
```

<a name="file-search"></a>
#### 파일 검색 (File Search)

`FileSearch` 제공자 툴은 [벡터 스토어](#vector-stores)에 저장된 [파일](#files)들을 검색할 수 있도록 해줍니다. 이 기능을 통해 Agent가 업로드 문서에서 관련 정보를 찾아오는 RAG(검색 기반 생성)를 활용할 수 있습니다.

**지원 제공자:** OpenAI, Gemini

```php
use Laravel\Ai\Providers\Tools\FileSearch;

public function tools(): iterable
{
    return [
        new FileSearch(stores: ['store_id']),
    ];
}
```

복수 벡터 스토어 ID도 지정할 수 있습니다:

```php
new FileSearch(stores: ['store_1', 'store_2']);
```

파일에 [메타데이터](#adding-files-to-stores)가 있다면, `where`로 검색 결과를 필터링할 수 있습니다. 간단한 조건은 배열로 전달합니다:

```php
new FileSearch(stores: ['store_id'], where: [
    'author' => 'Taylor Otwell',
    'year' => 2026,
]);
```

더 복잡한 필터는 클로저로 처리할 수 있습니다:

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

에이전트는 미들웨어를 지원하여, 프롬프트가 제공자에게 전송되기 전에 가로채거나 수정할 수 있습니다. 에이전트에 미들웨어를 추가하려면 `HasMiddleware` 인터페이스를 구현하고, 미들웨어 클래스 배열을 반환하는 `middleware` 메서드를 정의하십시오:

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
     * 에이전트의 미들웨어 배열을 반환합니다.
     */
    public function middleware(): array
    {
        return [
            new LogPrompts,
        ];
    }
}
```

각 미들웨어 클래스는 `AgentPrompt`와 다음 미들웨어로 전달하는 `Closure`를 받는 `handle` 메서드를 구현해야 합니다:

```php
<?php

namespace App\Ai\Middleware;

use Closure;
use Laravel\Ai\Prompts\AgentPrompt;

class LogPrompts
{
    /**
     * 들어오는 프롬프트를 처리합니다.
     */
    public function handle(AgentPrompt $prompt, Closure $next)
    {
        Log::info('Prompting agent', ['prompt' => $prompt->prompt]);

        return $next($prompt);
    }
}
```

응답 처리가 끝난 뒤 실행할 코드는 `then` 메서드로 연결할 수 있습니다(동기, 스트리밍 모두 사용 가능):

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

간단히 임시 테스트나 여러 번 쓸 일이 없는 경우, 별도의 에이전트 클래스를 만들지 않고 `agent` 함수를 통해 익명(Ad-hoc) 에이전트를 즉시 생성할 수 있습니다:

```php
use function Laravel\Ai\{agent};

$response = agent(
    instructions: 'You are an expert at software development.',
    messages: [],
    tools: [],
)->prompt('Tell me about Laravel')
```

익명 에이전트도 구조화 출력을 생성할 수 있습니다:

```php
use Illuminate\Contracts\JsonSchema\JsonSchema;

use function Laravel\Ai\{agent};

$response = agent(
    schema: fn (JsonSchema $schema) => [
        'number' => $schema->integer()->required(),
    ],
)->prompt('Generate a random number less than 100')
```

<a name="agent-configuration"></a>
### 에이전트 설정 (Agent Configuration)

에이전트에서 PHP 속성(Attribute)을 사용해 텍스트 생성 옵션을 손쉽게 지정할 수 있습니다. 사용할 수 있는 주요 Attribute는 다음과 같습니다:

- `MaxSteps`: 툴 활용 시 에이전트가 수행할 최대 단계 수
- `MaxTokens`: 모델이 생성할 수 있는 토큰 최대값
- `Model`: 사용할 모델명
- `Provider`: 에이전트가 사용할 AI 제공자(여러 개 지정 시 페일오버 가능)
- `Temperature`: 생성 시 사용할 샘플링 온도(0.0 ~ 1.0)
- `Timeout`: 에이전트 요청의 HTTP 타임아웃(초, 기본값 60)
- `UseCheapestModel`: 제공자의 가장 저렴한 텍스트 모델 사용
- `UseSmartestModel`: 제공자의 가장 우수한 텍스트 모델 사용

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

`UseCheapestModel`, `UseSmartestModel` 속성을 이용하면 모델명을 직접 명시하지 않아도, 상황에 맞게 자동으로 가장 저렴하거나 성능이 우수한 모델을 선택할 수 있습니다:

```php
use Laravel\Ai\Attributes\UseCheapestModel;
use Laravel\Ai\Attributes\UseSmartestModel;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Promptable;

#[UseCheapestModel]
class SimpleSummarizer implements Agent
{
    use Promptable;

    // 가장 저렴한 모델(예: Haiku)이 자동 선택됨
}

#[UseSmartestModel]
class ComplexReasoner implements Agent
{
    use Promptable;

    // 가장 능력 있는 모델(예: Opus)이 자동 선택됨
}
```

<a name="images"></a>
## 이미지 (Images)

`Laravel\Ai\Image` 클래스를 사용해 `openai`, `gemini`, `xai` 제공자로 이미지를 생성할 수 있습니다:

```php
use Laravel\Ai\Image;

$image = Image::of('A donut sitting on the kitchen counter')->generate();

$rawContent = (string) $image;
```

`square`, `portrait`, `landscape` 메서드로 이미지 비율을, `quality` 메서드로 (`high`, `medium`, `low`) 등 품질을, `timeout`으로 HTTP 타임아웃(초 단위)을 각각 지정할 수 있습니다:

```php
use Laravel\Ai\Image;

$image = Image::of('A donut sitting on the kitchen counter')
    ->quality('high')
    ->landscape()
    ->timeout(120)
    ->generate();
```

참고 이미지는 `attachments` 메서드로 첨부할 수 있습니다:

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

생성된 이미지는 설정된 기본 디스크(예: `config/filesystems.php`)에 손쉽게 저장할 수 있습니다:

```php
$image = Image::of('A donut sitting on the kitchen counter');

$path = $image->store();
$path = $image->storeAs('image.jpg');
$path = $image->storePublicly();
$path = $image->storePubliclyAs('image.jpg');
```

이미지 생성 또한 큐잉 처리가 가능합니다:

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

`Laravel\Ai\Audio` 클래스를 사용하면 주어진 텍스트로부터 오디오를 생성할 수 있습니다:

```php
use Laravel\Ai\Audio;

$audio = Audio::of('I love coding with Laravel.')->generate();

$rawContent = (string) $audio;
```

`male`, `female`, `voice` 메서드로 목소리 성별 또는 특성을 지정할 수 있습니다:

```php
$audio = Audio::of('I love coding with Laravel.')
    ->female()
    ->generate();

$audio = Audio::of('I love coding with Laravel.')
    ->voice('voice-id-or-name')
    ->generate();
```

더 세부적으로, 합성된 오디오의 전반적 톤이나 스타일은 `instructions`로 안내 가능합니다:

```php
$audio = Audio::of('I love coding with Laravel.')
    ->female()
    ->instructions('Said like a pirate')
    ->generate();
```

생성된 오디오는 파일 시스템의 기본 디스크에 쉽게 저장할 수 있습니다:

```php
$audio = Audio::of('I love coding with Laravel.')->generate();

$path = $audio->store();
$path = $audio->storeAs('audio.mp3');
$path = $audio->storePublicly();
$path = $audio->storePubliclyAs('audio.mp3');
```

오디오 생성 또한 큐로 처리할 수 있습니다:

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

`Laravel\Ai\Transcription` 클래스를 사용해 오디오에 대한 트랜스크립트를 생성할 수 있습니다:

```php
use Laravel\Ai\Transcription;

$transcript = Transcription::fromPath('/home/laravel/audio.mp3')->generate();
$transcript = Transcription::fromStorage('audio.mp3')->generate();
$transcript = Transcription::fromUpload($request->file('audio'))->generate();

return (string) $transcript;
```

`diarize` 메서드는 응답에 단순 텍스트 외에 화자 구분된(transcript by speaker) 트랜스크립트를 포함하고자 할 때 사용합니다:

```php
$transcript = Transcription::fromStorage('audio.mp3')
    ->diarize()
    ->generate();
```

트랜스크립션 역시 큐 처리할 수 있습니다:

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

문자열의 벡터 임베딩을 쉽게 생성하기 위해, Laravel의 `Stringable`에 추가된 `toEmbeddings` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Support\Str;

$embeddings = Str::of('Napa Valley has great wine.')->toEmbeddings();
```

여러 입력에 대한 임베딩을 생성하려면 `Embeddings` 클래스를 사용하세요:

```php
use Laravel\Ai\Embeddings;

$response = Embeddings::for([
    'Napa Valley has great wine.',
    'Laravel is a PHP framework.',
])->generate();

$response->embeddings; // [[0.123, 0.456, ...], [0.789, 0.012, ...]]
```

임베딩 차원 및 제공자도 지정할 수 있습니다:

```php
$response = Embeddings::for(['Napa Valley has great wine.'])
    ->dimensions(1536)
    ->generate('openai', 'text-embedding-3-small');
```

<a name="querying-embeddings"></a>
### 임베딩 질의 (Querying Embeddings)

임베딩을 생성한 후에는, 보통 이를 데이터베이스의 `vector` 컬럼에 저장하여 후속 질의에 활용합니다. Laravel은 PostgreSQL의 `pgvector` 확장을 통한 벡터 컬럼을 기본 지원합니다. 마이그레이션에서 벡터 컬럼을 정의할 때 차원을 지정하세요:

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

유사도 검색 속도를 높이기 위해 벡터 컬럼에 인덱스를 생성할 수 있습니다. `index` 호출 시 Laravel은 코사인 거리 기반 HNSW 인덱스를 자동 생성합니다:

```php
$table->vector('embedding', dimensions: 1536)->index();
```

Eloquent 모델에서는 벡터 컬럼을 `array`로 캐스팅하세요:

```php
protected function casts(): array
{
    return [
        'embedding' => 'array',
    ];
}
```

유사 레코드 질의는 `whereVectorSimilarTo`로 할 수 있습니다. minSimilarity(0.0~1.0, 1.0은 완전히 동일)와 함께 결과가 유사도 기준으로 정렬됩니다:

```php
use App\Models\Document;

$documents = Document::query()
    ->whereVectorSimilarTo('embedding', $queryEmbedding, minSimilarity: 0.4)
    ->limit(10)
    ->get();
```

`$queryEmbedding`에 float 배열 또는 문자열을 전달할 수 있으며, 문자열 전달 시 Laravel이 임베딩을 자동 생성합니다:

```php
$documents = Document::query()
    ->whereVectorSimilarTo('embedding', 'best wineries in Napa Valley')
    ->limit(10)
    ->get();
```

추가적인 제어가 필요하다면 `whereVectorDistanceLessThan`, `selectVectorDistance`, `orderByVectorDistance` 등을 사용할 수 있습니다:

```php
$documents = Document::query()
    ->select('*')
    ->selectVectorDistance('embedding', $queryEmbedding, as: 'distance')
    ->whereVectorDistanceLessThan('embedding', $queryEmbedding, maxDistance: 0.3)
    ->orderByVectorDistance('embedding', $queryEmbedding)
    ->limit(10)
    ->get();
```

에이전트가 유사도 검색을 툴로 사용할 수 있도록 하려면 [유사도 검색 툴](#similarity-search) 문서를 참고하세요.

> [!NOTE]
> 벡터 쿼리는 현재 PostgreSQL의 `pgvector` 확장으로 연결된 경우에만 지원됩니다.

<a name="caching-embeddings"></a>
### 임베딩 캐싱 (Caching Embeddings)

동일한 입력에 대해 API 호출을 반복하지 않도록 임베딩 생성을 캐시할 수 있습니다. 캐시는 `ai.caching.embeddings.cache` 옵션을 `true`로 설정해 활성화합니다:

```php
'caching' => [
    'embeddings' => [
        'cache' => true,
        'store' => env('CACHE_STORE', 'database'),
        // ...
    ],
],
```

캐시 활성화 시 임베딩은 30일간 저장됩니다. 캐시 키는 제공자, 모델, 차원, 입력 내용에 기반하므로, 동일 요청은 캐시된 결과를, 설정이 다르면 새롭게 생성된 결과를 반환합니다.

전역 캐시 비활성화 시에도, 요청별로 `cache` 메서드로 개별 캐시 사용이 가능합니다:

```php
$response = Embeddings::for(['Napa Valley has great wine.'])
    ->cache()
    ->generate();
```

초 단위로 캐시 지속시간을 지정할 수도 있습니다:

```php
$response = Embeddings::for(['Napa Valley has great wine.'])
    ->cache(seconds: 3600) // 1시간 캐시
    ->generate();
```

`toEmbeddings` 메서드도 `cache` 인수를 받을 수 있습니다:

```php
// 기본 캐시 지속시간
$embeddings = Str::of('Napa Valley has great wine.')->toEmbeddings(cache: true);

// 특정 기간만 캐싱
$embeddings = Str::of('Napa Valley has great wine.')->toEmbeddings(cache: 3600);
```

<a name="reranking"></a>
## 리랭킹 (Reranking)

리랭킹은 주어진 쿼리에 대해 문서 리스트를 의미적 관련도 기준으로 재정렬하는 기능입니다. 이는 검색 결과의 품질 향상에 유용합니다.

`Laravel\Ai\Reranking` 클래스를 사용해 문서를 리랭킹할 수 있습니다:

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
$response->first()->index;    // 1 (원래 순서)
```

`limit` 메서드로 결과 수 제한도 가능합니다:

```php
$response = Reranking::of($documents)
    ->limit(5)
    ->rerank('search query');
```

<a name="reranking-collections"></a>
### 컬렉션 리랭킹 (Reranking Collections)

Laravel 컬렉션은 `rerank` 매크로로 리랭킹할 수 있습니다. 첫 번째 인자는 리랭킹할 컬럼명(단일, 복수 또는 클로저), 두 번째 인자는 쿼리입니다:

```php
// 단일 컬럼 기준 리랭킹
$posts = Post::all()
    ->rerank('body', 'Laravel tutorials');

// 복수 컬럼 기준(JSON으로 묶어서 전송)
$reranked = $posts->rerank(['title', 'body'], 'Laravel tutorials');

// 클로저를 통한 문서 작성
$reranked = $posts->rerank(
    fn ($post) => $post->title.': '.$post->body,
    'Laravel tutorials'
);
```

결과 수 제한 및 제공자 지정도 가능합니다:

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

`Laravel\Ai\Files` 클래스 또는 개별 파일 클래스를 사용하여, AI 제공자에 파일을 저장할 수 있습니다. 이는 큰 문서나 여러 번 참조해야 할 파일을 중복 업로드 없이 사용할 때 유용합니다:

```php
use Laravel\Ai\Files\Document;
use Laravel\Ai\Files\Image;

// 로컬 경로에서 파일 저장
$response = Document::fromPath('/home/laravel/document.pdf')->put();
$response = Image::fromPath('/home/laravel/photo.jpg')->put();

// 파일 시스템 디스크에서 저장
$response = Document::fromStorage('document.pdf', disk: 'local')->put();
$response = Image::fromStorage('photo.jpg', disk: 'local')->put();

// 원격 URL에서 저장
$response = Document::fromUrl('https://example.com/document.pdf')->put();
$response = Image::fromUrl('https://example.com/photo.jpg')->put();

return $response->id;
```

순수 컨텐츠 혹은 업로드 파일 저장도 지원합니다:

```php
use Laravel\Ai\Files;
use Laravel\Ai\Files\Document;

// 문자열 데이터 저장
$stored = Document::fromString('Hello, World!', 'text/plain')->put();

// 업로드 파일 저장
$stored = Document::fromUpload($request->file('document'))->put();
```

한 번 저장된 파일은, 매번 재업로드하지 않고 에이전트 프롬프트에서 참조할 수 있습니다:

```php
use App\Ai\Agents\SalesCoach;
use Laravel\Ai\Files;

$response = (new SalesCoach)->prompt(
    'Analyze the attached sales transcript...'
    attachments: [
        Files\Document::fromId('file-id') // 저장된 문서 첨부
    ]
);
```

저장된 파일을 조회할 때는, 파일 인스턴스의 `get` 메서드를 사용하세요:

```php
use Laravel\Ai\Files\Document;

$file = Document::fromId('file-id')->get();

$file->id;
$file->mimeType();
```

파일을 제공자에서 삭제하려면 `delete` 메서드를 사용합니다:

```php
Document::fromId('file-id')->delete();
```

파일 업로드 등 대부분의 작업에서, 기본 AI 제공자 설정을 따르나 필요에 따라 `provider` 인수로 다른 제공자를 지정할 수 있습니다:

```php
$response = Document::fromPath(
    '/home/laravel/document.pdf'
)->put(provider: 'anthropic');
```

<a name="using-stored-files-in-conversations"></a>
### 저장된 파일을 대화에서 사용하기

제공자에 파일을 저장했다면, `Document`, `Image` 클래스의 `fromId`를 이용해 에이전트 프롬프트 첨부로 활용할 수 있습니다:

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

이미지 역시 `Image::fromId`로 참조할 수 있습니다:

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

벡터 스토어는 검색 가능한 파일 컬렉션을 구성해, RAG(검색 기반 생성) 시 활용할 수 있는 저장소입니다. `Laravel\Ai\Stores` 클래스는 벡터 스토어 생성, 조회, 삭제 메서드를 제공합니다:

```php
use Laravel\Ai\Stores;

// 새 벡터 스토어 생성
$store = Stores::create('Knowledge Base');

// 추가 옵션 포함 생성
$store = Stores::create(
    name: 'Knowledge Base',
    description: 'Documentation and reference materials.',
    expiresWhenIdleFor: days(30),
);

return $store->id;
```

기존 벡터 스토어 조회는 `get` 메서드로 할 수 있습니다:

```php
use Laravel\Ai\Stores;

$store = Stores::get('store_id');

$store->id;
$store->name;
$store->fileCounts;
$store->ready;
```

스토어 삭제는 클래스 혹은 인스턴스 모두로 호출 가능합니다:

```php
use Laravel\Ai\Stores;

// ID로 삭제
Stores::delete('store_id');

// 인스턴스에서 삭제
$store = Stores::get('store_id');

$store->delete();
```

<a name="adding-files-to-stores"></a>
### 스토어에 파일 추가하기 (Adding Files to Stores)

벡터 스토어가 있다면, `add` 메서드로 [파일](#files)을 추가할 수 있습니다. 추가된 파일은 자동으로 인덱싱되어, [파일 검색 제공자 툴](#file-search)로 검색할 수 있습니다:

```php
use Laravel\Ai\Files\Document;
use Laravel\Ai\Stores;

$store = Stores::get('store_id');

// 이미 저장된 파일 추가
$document = $store->add('file_id');
$document = $store->add(Document::fromId('file_id'));

// 저장과 추가를 한 번에 수행할 수도 있습니다
$document = $store->add(Document::fromPath('/path/to/document.pdf'));
$document = $store->add(Document::fromStorage('manual.pdf'));
$document = $store->add($request->file('document'));

$document->id;
$document->fileId;
```

> **Note:** 이미 저장된 파일을 벡터 스토어에 추가하는 경우, 반환되는 document ID는 기존 file ID와 일치할 수 있으나, 일부 벡터 스토리지 제공자는 새로운 "document ID"를 반환할 수 있습니다. 따라서 두 ID를 모두 데이터베이스에 저장하는 것을 권장합니다.

파일 추가 시 메타데이터를 첨부하면, 이후 [파일 검색 제공자 툴](#file-search)의 검색 결과 필터로 활용할 수 있습니다:

```php
$store->add(Document::fromPath('/path/to/document.pdf'), metadata: [
    'author' => 'Taylor Otwell',
    'department' => 'Engineering',
    'year' => 2026,
]);
```

스토어에서 파일을 제거하려면 `remove` 메서드를 사용하세요:

```php
$store->remove('file_id');
```

스토어에서만 제거하고 파일 자체는 그대로 두지만, 완전히 삭제하려면 `deleteFile`을 true로 지정하세요:

```php
$store->remove('file_abc123', deleteFile: true);
```

<a name="failover"></a>
## 페일오버 (Failover)

프롬프트 요청 또는 기타 미디어 생성 시, 여러 제공자/모델 배열을 지정하면 1차 제공자/모델의 장애나 레이트 리밋 발생 시, 자동으로 백업 제공자/모델로 페일오버됩니다:

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

테스트에서 에이전트 응답을 모킹하려면, 해당 에이전트에 `fake` 메서드를 호출합니다. 응답 배열이나 클로저도 지정할 수 있습니다:

```php
use App\Ai\Agents\SalesCoach;
use Laravel\Ai\Prompts\AgentPrompt;

// 모든 프롬프트에 고정 응답값 사용
SalesCoach::fake();

// 각 프롬프트 응답 배열 제공
SalesCoach::fake([
    'First response',
    'Second response',
]);

// 프롬프트 내용에 따라 다르게 응답
SalesCoach::fake(function (AgentPrompt $prompt) {
    return 'Response for: '.$prompt->prompt;
});
```

> **Note:** 구조화 출력 에이전트에서 `Agent::fake()`를 호출하면, 정의한 출력 스키마에 부합하는 데이터를 자동으로 생성합니다.

프롬프트 후에는 발송된 프롬프트에 대해 다양한 assertion을 할 수 있습니다:

```php
use Laravel\Ai\Prompts\AgentPrompt;

SalesCoach::assertPrompted('Analyze this...');

SalesCoach::assertPrompted(function (AgentPrompt $prompt) {
    return $prompt->contains('Analyze');
});

SalesCoach::assertNotPrompted('Missing prompt');

SalesCoach::assertNeverPrompted();
```

큐잉된 에이전트 호출은 큐전용 assertion을 사용하세요:

```php
use Laravel\Ai\QueuedAgentPrompt;

SalesCoach::assertQueued('Analyze this...');

SalesCoach::assertQueued(function (QueuedAgentPrompt $prompt) {
    return $prompt->contains('Analyze');
});

SalesCoach::assertNotQueued('Missing prompt');

SalesCoach::assertNeverQueued();
```

정의하지 않은 프롬프트에 실수로 에이전트가 호출되는 것을 막으려면 `preventStrayPrompts`를 사용하세요. 미정의 프롬프트 호출 시 예외가 발생합니다:

```php
SalesCoach::fake()->preventStrayPrompts();
```

<a name="testing-images"></a>
### 이미지 (Images)

이미지 생성을 모킹하려면 `Image` 클래스의 `fake` 메서드를 호출하세요. 모킹 후에는 다양한 프롬프트 기록에 대해 assertion할 수 있습니다:

```php
use Laravel\Ai\Image;
use Laravel\Ai\Prompts\ImagePrompt;
use Laravel\Ai\Prompts\QueuedImagePrompt;

// 모든 프롬프트에 고정 응답값 사용
Image::fake();

// 응답 이미지 배열 지정
Image::fake([
    base64_encode($firstImage),
    base64_encode($secondImage),
]);

// 프롬프트에 따라 동적 응답
Image::fake(function (ImagePrompt $prompt) {
    return base64_encode('...');
});
```

생성된 이미지에 대한 assertion 예시입니다:

```php
Image::assertGenerated(function (ImagePrompt $prompt) {
    return $prompt->contains('sunset') && $prompt->isLandscape();
});

Image::assertNotGenerated('Missing prompt');

Image::assertNothingGenerated();
```

큐잉된 이미지 처리에는 큐전용 assertion을 활용하세요:

```php
Image::assertQueued(
    fn (QueuedImagePrompt $prompt) => $prompt->contains('sunset')
);

Image::assertNotQueued('Missing prompt');

Image::assertNothingQueued();
```

정의하지 않은 이미지가 생성되는 것을 막으려면:

```php
Image::fake()->preventStrayImages();
```

<a name="testing-audio"></a>
### 오디오 (Audio)

오디오 생성 모킹도 `Audio` 클래스의 `fake`를 활용하세요. 프롬프트에 대한 assertion 예시입니다:

```php
use Laravel\Ai\Audio;
use Laravel\Ai\Prompts\AudioPrompt;
use Laravel\Ai\Prompts\QueuedAudioPrompt;

// 모든 프롬프트에 고정 응답값 사용
Audio::fake();

// 오디오 배열 지정
Audio::fake([
    base64_encode($firstAudio),
    base64_encode($secondAudio),
]);

// 프롬프트에 따라 동적 응답
Audio::fake(function (AudioPrompt $prompt) {
    return base64_encode('...');
});
```

생성된 오디오에 대한 assertion:

```php
Audio::assertGenerated(function (AudioPrompt $prompt) {
    return $prompt->contains('Hello') && $prompt->isFemale();
});

Audio::assertNotGenerated('Missing prompt');

Audio::assertNothingGenerated();
```

큐잉된 오디오 처리도 지원합니다:

```php
Audio::assertQueued(
    fn (QueuedAudioPrompt $prompt) => $prompt->contains('Hello')
);

Audio::assertNotQueued('Missing prompt');

Audio::assertNothingQueued();
```

오디오 모킹시 stray audio 방지:

```php
Audio::fake()->preventStrayAudio();
```

<a name="testing-transcriptions"></a>
### 트랜스크립션 (Transcriptions)

트랜스크립션 모킹도 `Transcription` 클래스의 `fake`를 사용합니다:

```php
use Laravel\Ai\Transcription;
use Laravel\Ai\Prompts\TranscriptionPrompt;
use Laravel\Ai\Prompts\QueuedTranscriptionPrompt;

// 모든 프롬프트에 고정 응답 사용
Transcription::fake();

// 응답 텍스트 배열 제공
Transcription::fake([
    'First transcription text.',
    'Second transcription text.',
]);

// 프롬프트 따라 동적 응답
Transcription::fake(function (TranscriptionPrompt $prompt) {
    return 'Transcribed text...';
});
```

assertion 예시:

```php
Transcription::assertGenerated(function (TranscriptionPrompt $prompt) {
    return $prompt->language === 'en' && $prompt->isDiarized();
});

Transcription::assertNotGenerated(
    fn (TranscriptionPrompt $prompt) => $prompt->language === 'fr'
);

Transcription::assertNothingGenerated();
```

큐잉 트랜스크립션 assertion:

```php
Transcription::assertQueued(
    fn (QueuedTranscriptionPrompt $prompt) => $prompt->isDiarized()
);

Transcription::assertNotQueued(
    fn (QueuedTranscriptionPrompt $prompt) => $prompt->language === 'fr'
);

Transcription::assertNothingQueued();
```

stray transcription 방지 설정:

```php
Transcription::fake()->preventStrayTranscriptions();
```

<a name="testing-embeddings"></a>
### 임베딩 (Embeddings)

임베딩 모킹은 `Embeddings` 클래스의 `fake` 메서드로 합니다. assertion 방법은 다음과 같습니다:

```php
use Laravel\Ai\Embeddings;
use Laravel\Ai\Prompts\EmbeddingsPrompt;
use Laravel\Ai\Prompts\QueuedEmbeddingsPrompt;

// 정해진 차원에 맞는 임베딩 자동 생성
Embeddings::fake();

// 특정 벡터 배열 지정
Embeddings::fake([
    [$firstEmbeddingVector],
    [$secondEmbeddingVector],
]);

// 프롬프트 따라 동적 응답
Embeddings::fake(function (EmbeddingsPrompt $prompt) {
    return array_map(
        fn () => Embeddings::fakeEmbedding($prompt->dimensions),
        $prompt->inputs
    );
});
```

assertion 예시:

```php
Embeddings::assertGenerated(function (EmbeddingsPrompt $prompt) {
    return $prompt->contains('Laravel') && $prompt->dimensions === 1536;
});

Embeddings::assertNotGenerated(
    fn (EmbeddingsPrompt $prompt) => $prompt->contains('Other')
);

Embeddings::assertNothingGenerated();
```

큐잉 임베딩 assertion:

```php
Embeddings::assertQueued(
    fn (QueuedEmbeddingsPrompt $prompt) => $prompt->contains('Laravel')
);

Embeddings::assertNotQueued(
    fn (QueuedEmbeddingsPrompt $prompt) => $prompt->contains('Other')
);

Embeddings::assertNothingQueued();
```

stray 임베딩 방지:

```php
Embeddings::fake()->preventStrayEmbeddings();
```

<a name="testing-reranking"></a>
### 리랭킹 (Reranking)

리랭킹 작업도 `Reranking` 클래스의 `fake` 메서드로 모킹할 수 있습니다:

```php
use Laravel\Ai\Reranking;
use Laravel\Ai\Prompts\RerankingPrompt;
use Laravel\Ai\Responses\Data\RankedDocument;

// 자동 리랭킹 응답 생성
Reranking::fake();

// 커스텀 응답 지정
Reranking::fake([
    [
        new RankedDocument(index: 0, document: 'First', score: 0.95),
        new RankedDocument(index: 1, document: 'Second', score: 0.80),
    ],
]);
```

리랭킹 assertion 예시:

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

파일 작업 모킹은 `Files::fake()`를 호출하세요:

```php
use Laravel\Ai\Files;

Files::fake();
```

업로드 및 삭제 이벤트에 대한 assertion 예시:

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

파일 삭제도 검증할 수 있습니다:

```php
Files::assertDeleted('file-id');
Files::assertNotDeleted('file-id');
Files::assertNothingDeleted();
```

<a name="testing-vector-stores"></a>
### 벡터 스토어 (Vector Stores)

벡터 스토어 작업 모킹은 `Stores::fake()`로 가능합니다. 이때 파일 작업 모킹 역시 자동으로 적용됩니다:

```php
use Laravel\Ai\Stores;

Stores::fake();
```

스토어 생성·삭제 등에 대한 assertion 예시:

```php
use Laravel\Ai\Stores;

// 스토어 생성
$store = Stores::create('Knowledge Base');

// assertion
Stores::assertCreated('Knowledge Base');

Stores::assertCreated(fn (string $name, ?string $description) =>
    $name === 'Knowledge Base'
);

Stores::assertNotCreated('Other Store');

Stores::assertNothingCreated();
```

스토어 삭제 검증 예시:

```php
Stores::assertDeleted('store_id');
Stores::assertNotDeleted('other_store_id');
Stores::assertNothingDeleted();
```

스토어별 파일 추가, 제거 이벤트는 스토어 인스턴스의 assertion 메서드를 사용하세요:

```php
Stores::fake();

$store = Stores::get('store_id');

// 파일 추가/제거
$store->add('added_id');
$store->remove('removed_id');

// assertion
$store->assertAdded('added_id');
$store->assertRemoved('removed_id');

$store->assertNotAdded('other_file_id');
$store->assertNotRemoved('other_file_id');
```

파일이 [파일 스토리지](#files)에 저장되면서 동시에 벡터 스토어에 추가되는 경우, 제공자 ID를 알 수 없으므로 `assertAdded`에 클로저로 파일 컨텐츠 검증식을 전달할 수 있습니다:

```php
use Laravel\Ai\Contracts\Files\StorableFile;
use Laravel\Ai\Files\Document;

$store->add(Document::fromString('Hello, World!', 'text/plain')->as('hello.txt'));

$store->assertAdded(fn (StorableFile $file) => $file->name() === 'hello.txt');
$store->assertAdded(fn (StorableFile $file) => $file->content() === 'Hello, World!');
```

<a name="events"></a>
## 이벤트 (Events)

Laravel AI SDK는 다양한 [이벤트](/docs/12.x/events)를 디스패치합니다. 예시는 다음과 같습니다:

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

이벤트를 리슨하여 AI SDK 사용정보 기록 또는 기타 작업에 활용할 수 있습니다.

