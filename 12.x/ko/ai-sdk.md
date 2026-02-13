# Laravel AI SDK (Laravel AI SDK)

- [소개](#introduction)
- [설치](#installation)
    - [설정](#configuration)
    - [커스텀 베이스 URL](#custom-base-urls)
    - [프로바이더 지원](#provider-support)
- [에이전트](#agents)
    - [프롬프트 사용하기](#prompting)
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
    - [임베딩 쿼리](#querying-embeddings)
    - [임베딩 캐싱](#caching-embeddings)
- [재정렬(reranking)](#reranking)
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
## 소개

[Laravel AI SDK](https://github.com/laravel/ai)는 OpenAI, Anthropic, Gemini 등 다양한 AI 프로바이더와 상호작용할 수 있도록 통일되고 표현력 있는 API를 제공합니다. 이 SDK를 사용하면, 툴(tool)과 구조화된 출력을 지원하는 지능형 에이전트 구축, 이미지 생성, 오디오 합성/트랜스크립션, 벡터 임베딩 생성 등 폭넓은 기능을 일관적이고 Laravel에 최적화된 인터페이스로 구현할 수 있습니다.

<a name="installation"></a>
## 설치

Laravel AI SDK는 Composer를 통해 설치할 수 있습니다:

```shell
composer require laravel/ai
```

다음으로, `vendor:publish` Artisan 명령어를 사용해 AI SDK 설정 및 마이그레이션 파일을 퍼블리시하세요:

```shell
php artisan vendor:publish --provider="Laravel\Ai\AiServiceProvider"
```

마지막으로 애플리케이션의 데이터베이스 마이그레이션을 실행해야 합니다. 이 작업을 통해 AI SDK에서 대화 저장을 위해 사용하는 `agent_conversations` 및 `agent_conversation_messages` 테이블이 생성됩니다:

```shell
php artisan migrate
```

<a name="configuration"></a>
### 설정

프로바이더의 API 키 등 인증 정보를 프로젝트의 `config/ai.php` 설정 파일이나, 애플리케이션의 `.env` 파일에서 환경변수로 정의할 수 있습니다:

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

텍스트, 이미지, 오디오, 트랜스크립션, 임베딩에 사용하는 기본 모델 역시 `config/ai.php` 설정 파일에서 지정할 수 있습니다.

<a name="custom-base-urls"></a>
### 커스텀 베이스 URL

기본적으로 Laravel AI SDK는 각 프로바이더의 공개된 API 엔드포인트에 직접 접속합니다. 하지만 프록시 서비스로 API 키 관리나 트래픽 우회, 레이트 리밋 적용 등을 위해 다른 엔드포인트로 요청을 라우팅해야 할 수도 있습니다.

이때는 설정에서 `url` 파라미터를 추가해 커스텀 베이스 URL을 지정할 수 있습니다:

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

이는 LiteLLM, Azure OpenAI Gateway와 같은 프록시를 이용하거나 대체 엔드포인트를 사용할 때 유용합니다.

커스텀 베이스 URL은 OpenAI, Anthropic, Gemini, Groq, Cohere, DeepSeek, xAI, OpenRouter 프로바이더에서 지원됩니다.

<a name="provider-support"></a>
### 프로바이더 지원

AI SDK는 다양한 기능별로 여러 프로바이더를 지원합니다. 아래 표는 각 기능별 지원되는 프로바이더의 목록입니다:

| 기능 | 지원 프로바이더 |
|---|---|
| Text | OpenAI, Anthropic, Gemini, Azure, Groq, xAI, DeepSeek, Mistral, Ollama |
| Images | OpenAI, Gemini, xAI |
| TTS | OpenAI, ElevenLabs |
| STT | OpenAI, ElevenLabs, Mistral |
| Embeddings | OpenAI, Gemini, Azure, Cohere, Mistral, Jina, VoyageAI |
| Reranking | Cohere, Jina |
| Files | OpenAI, Anthropic, Gemini |

코드에서 프로바이더를 문자열 대신 `Laravel\Ai\Enums\Lab` enum으로 참조할 수 있습니다:

```php
use Laravel\Ai\Enums\Lab;

Lab::Anthropic;
Lab::OpenAI;
Lab::Gemini;
// ...
```

<a name="agents"></a>
## 에이전트

에이전트는 Laravel AI SDK에서 AI 프로바이더와 상호작용하는 기본 단위입니다. 각 에이전트는 하나의 PHP 클래스에, 프롬프트 지침/대화 컨텍스트/사용 툴/출력 스키마 등 LLM과 통신에 필요한 모든 로직을 캡슐화합니다. 에이전트는, 판매 코치, 문서 분석기, 고객지원 챗봇과 같은 특정 역할을 가진 인공지능 비서로, 한 번 구성해두면 애플리케이션 전반에서 손쉽게 활용할 수 있습니다.

에이전트는 `make:agent` Artisan 명령어로 생성할 수 있습니다:

```shell
php artisan make:agent SalesCoach

php artisan make:agent SalesCoach --structured
```

생성된 에이전트 클래스에서는 시스템 프롬프트·지침, 메시지 컨텍스트, 사용 가능한 툴, 출력 스키마(필요할 경우)를 정의할 수 있습니다:

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
     * 에이전트가 따라야 할 지침을 반환합니다.
     */
    public function instructions(): Stringable|string
    {
        return 'You are a sales coach, analyzing transcripts and providing feedback and an overall sales strength score.';
    }

    /**
     * 지금까지의 대화 메시지 목록을 반환합니다.
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
     * 에이전트가 사용할 수 있는 툴을 반환합니다.
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
     * 에이전트의 구조화된 출력 스키마 정의를 반환합니다.
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
### 프롬프트 사용하기

에이전트에게 프롬프트를 전달하려면, 먼저 `make` 메서드 또는 인스턴스를 직접 생성한 뒤에 `prompt`를 호출합니다:

```php
$response = (new SalesCoach)
    ->prompt('Analyze this sales transcript...');

$response = SalesCoach::make()
    ->prompt('Analyze this sales transcript...');

return (string) $response;
```

`make` 메서드는 컨테이너에서 에이전트를 리졸브해주며, 자동 의존성 주입을 지원합니다. 또한 에이전트 생성자에 인수를 전달할 수도 있습니다:

```php
$agent = SalesCoach::make(user: $user);
```

추가 인자를 `prompt` 메서드에 전달해, 프롬프트 시 프로바이더·모델·HTTP 타임아웃 설정을 오버라이드할 수 있습니다:

```php
$response = (new SalesCoach)->prompt(
    'Analyze this sales transcript...',
    provider: Lab::Anthropic,
    model: 'claude-haiku-4-5-20251001',
    timeout: 120,
);
```

<a name="conversation-context"></a>
### 대화 컨텍스트

에이전트가 `Conversational` 인터페이스를 구현한다면, 이전 대화 컨텍스트를 `messages` 메서드를 통해 반환할 수 있습니다:

```php
use App\Models\History;
use Laravel\Ai\Messages\Message;

/**
 * 지금까지의 대화 메시지 목록을 반환합니다.
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
#### 대화 저장하기

> [!NOTE]  
> `RemembersConversations` 트레이트를 사용하기 전에, `vendor:publish` Artisan 명령어로 AI SDK 마이그레이션을 퍼블리시·실행해야 합니다. 해당 마이그레이션은 대화 내역 저장에 필요한 데이터베이스 테이블을 생성합니다.

Laravel에서 에이전트의 대화 이력을 자동 저장·복원하려면 `RemembersConversations` 트레이트를 사용할 수 있습니다. 이 트레이트는 별도의 `Conversational` 인터페이스 구현 없이 간단하게 대화 메시지를 DB에 영속화할 수 있게 해줍니다:

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
     * 에이전트가 따라야 할 지침을 반환합니다.
     */
    public function instructions(): string
    {
        return 'You are a sales coach...';
    }
}
```

새로운 대화를 시작하려면 프롬프트 전에 `forUser` 메서드를 호출하세요:

```php
$response = (new SalesCoach)->forUser($user)->prompt('Hello!');

$conversationId = $response->conversationId;
```

응답 값에 포함된 conversation ID를 저장해두거나, 직접 `agent_conversations` 테이블에서 유저의 모든 대화 목록을 조회할 수도 있습니다.

기존 대화 이어하기는 `continue` 메서드를 사용합니다:

```php
$response = (new SalesCoach)
    ->continue($conversationId, as: $user)
    ->prompt('Tell me more about that.');
```

`RemembersConversations` 트레이트를 사용하면, 이전 메시지가 자동으로 불러와져 대화 컨텍스트에 포함되고, 새 사용자/에이전트 메시지도 상호작용 이후 자동 저장됩니다.

<a name="structured-output"></a>
### 구조화된 출력

에이전트가 구조화된 출력을 반환하도록 하려면, `HasStructuredOutput` 인터페이스를 구현하고, `schema` 메서드를 정의해야 합니다:

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
     * 에이전트의 구조화된 출력 스키마 정의를 반환합니다.
     */
    public function schema(JsonSchema $schema): array
    {
        return [
            'score' => $schema->integer()->required(),
        ];
    }
}
```

구조화된 출력을 반환하는 에이전트를 프롬프트할 때, 반환된 `StructuredAgentResponse` 객체를 배열처럼 다룰 수 있습니다:

```php
$response = (new SalesCoach)->prompt('Analyze this sales transcript...');

return $response['score'];
```

<a name="attachments"></a>
### 첨부파일

프롬프트 시 첨부파일을 함께 전달하여, 모델이 이미지·문서 등 파일을 참고할 수 있게 할 수 있습니다:

```php
use App\Ai\Agents\SalesCoach;
use Laravel\Ai\Files;

$response = (new SalesCoach)->prompt(
    'Analyze the attached sales transcript...',
    attachments: [
        Files\Document::fromStorage('transcript.pdf'), // 파일시스템 디스크에서 문서 첨부
        Files\Document::fromPath('/home/laravel/transcript.md'), // 로컬 경로에서 첨부
        $request->file('transcript'), // 업로드된 파일 첨부
    ]
);
```

이미지는 `Laravel\Ai\Files\Image` 클래스를 사용해 첨부합니다:

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

에이전트 응답은 `stream` 메서드로 스트리밍할 수 있습니다. 반환된 `StreamableAgentResponse`는 라우트에서 반환해 클라이언트에 실시간(SSE)으로 스트리밍 전송할 수 있습니다:

```php
use App\Ai\Agents\SalesCoach;

Route::get('/coach', function () {
    return (new SalesCoach)->stream('Analyze this sales transcript...');
});
```

`then` 메서드를 사용해, 전체 응답이 스트리밍 완료된 시점에 콜백을 실행할 수 있습니다:

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

또는 스트림 이벤트를 for문으로 직접 순회해 처리할 수도 있습니다:

```php
$stream = (new SalesCoach)->stream('Analyze this sales transcript...');

foreach ($stream as $event) {
    // ...
}
```

<a name="streaming-using-the-vercel-ai-sdk-protocol"></a>
#### Vercel AI SDK 프로토콜로 스트리밍

[Vercel AI SDK 스트림 프로토콜](https://ai-sdk.dev/docs/ai-sdk-ui/stream-protocol)을 사용해서 이벤트를 스트리밍하려면 `usingVercelDataProtocol` 메서드를 chain 할 수 있습니다:

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

스트리밍 이벤트를 브로드캐스트하는 방법은 여러 가지가 있습니다. 스트림 이벤트에서 직접 `broadcast` 또는 `broadcastNow` 메서드를 호출할 수 있습니다:

```php
use App\Ai\Agents\SalesCoach;
use Illuminate\Broadcasting\Channel;

$stream = (new SalesCoach)->stream('Analyze this sales transcript...');

foreach ($stream as $event) {
    $event->broadcast(new Channel('channel-name'));
}
```

또는, 에이전트의 `broadcastOnQueue` 메서드를 사용하여 에이전트 작업을 큐에 등록하고, 처리가 되는 순서대로 스트리밍 이벤트를 브로드캐스트할 수 있습니다:

```php
(new SalesCoach)->broadcastOnQueue(
    'Analyze this sales transcript...',
    new Channel('channel-name'),
);
```

<a name="queueing"></a>
### 큐잉

에이전트의 `queue` 메서드를 이용하면, 프롬프트 실행을 백그라운드에서 처리하여 애플리케이션의 반응성을 높일 수 있습니다. 응답 처리/예외 처리용 클로저는 각각 `then`, `catch` 메서드로 등록합니다:

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

툴(Tool)은 에이전트가 프롬프트 응답 시 추가적인 기능을 사용할 수 있도록 해줍니다. `make:tool` Artisan 명령어로 툴 클래스를 생성할 수 있습니다:

```shell
php artisan make:tool RandomNumberGenerator
```

생성된 툴은 `app/Ai/Tools` 디렉터리에 위치하며, 각 툴은 에이전트가 해당 기능이 필요할 때 호출하는 `handle` 메서드를 제공합니다:

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
     * 툴의 목적을 설명합니다.
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

툴을 정의한 후에는, 에이전트의 `tools` 메서드에서 반환하면 됩니다:

```php
use App\Ai\Tools\RandomNumberGenerator;

/**
 * 에이전트가 사용할 수 있는 툴을 반환합니다.
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

`SimilaritySearch` 툴을 이용하면 에이전트가 벡터 임베딩이 저장된 데이터베이스에서 쿼리와 유사한 문서를 검색할 수 있습니다. 이는 RAG(Retrieval Augmented Generation)에서 애플리케이션 데이터를 검색하게 하고 싶은 경우에 유용합니다.

가장 간단한 방법은 Eloquent 모델(벡터 임베딩 컬럼 포함)과 함께 `usingModel` 메서드를 사용하는 것입니다:

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

첫 번째 인수는 Eloquent 모델 클래스, 두 번째는 벡터 임베딩이 저장된 컬럼명입니다.

`minSimilarity`(0.0~1.0)와 쿼리 customizing 클로저도 추가할 수 있습니다:

```php
SimilaritySearch::usingModel(
    model: Document::class,
    column: 'embedding',
    minSimilarity: 0.7,
    limit: 10,
    query: fn ($query) => $query->where('published', true),
),
```

더 세밀한 제어가 필요하다면, 커스텀 클로저를 받아 직접 검색 로직을 지정할 수도 있습니다:

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

툴의 설명은 `withDescription` 메서드로 커스터마이징할 수 있습니다:

```php
SimilaritySearch::usingModel(Document::class, 'embedding')
    ->withDescription('Search the knowledge base for relevant articles.'),
```

<a name="provider-tools"></a>
### 프로바이더 툴

프로바이더 툴은 웹 검색, URL 내용 가져오기, 파일 검색 등 AI 프로바이더가 네이티브로 구현한 특수 툴입니다. 일반 툴과는 달리, 프로바이더 툴은 애플리케이션이 아니라 프로바이더에서 실행됩니다.

프로바이더 툴은 에이전트의 `tools` 메서드에서 반환하면 됩니다.

<a name="web-search"></a>
#### 웹 검색

`WebSearch` 프로바이더 툴을 통해 에이전트가 실시간 웹 검색을 할 수 있습니다. 최신 정보나 시의성 있는 주제에 답변할 때 유용합니다.

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

검색 횟수 제한, 특정 도메인 결과만 허용 등도 설정 가능합니다:

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
#### 웹 페치

`WebFetch` 프로바이더 툴은 특정 웹페이지의 내용을 가져와서 분석하도록 에이전트에게 기능을 제공합니다. 특정 URL에서 세밀한 정보를 추출할 때 유용합니다.

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

검색 횟수나 허용 도메인 제한도 지정할 수 있습니다:

```php
(new WebFetch)->max(3)->allow(['docs.laravel.com']),
```

<a name="file-search"></a>
#### 파일 검색

`FileSearch` 프로바이더 툴을 사용하면 [벡터 스토어](#vector-stores)에 저장된 [파일](#files)에서 에이전트가 필요한 정보를 검색할 수 있습니다. 이를 통해 에이전트가 업로드된 문서에서 정보를 검색하는 RAG(Retrieval Augmented Generation)를 구현할 수 있습니다.

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

여러 벡터 스토어 ID를 넣어 여러 스토어를 동시에 검색할 수도 있습니다:

```php
new FileSearch(stores: ['store_1', 'store_2']);
```

파일에 [메타데이터](#adding-files-to-stores)가 있다면, `where` 인자로 검색 결과 필터링 가능합니다. 단순 조건은 배열로 전달합니다:

```php
new FileSearch(stores: ['store_id'], where: [
    'author' => 'Taylor Otwell',
    'year' => 2026,
]);
```

복잡한 조건은 `FileSearchQuery` 인스턴스를 받아 작성하세요:

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

에이전트는 미들웨어도 지원하며, 이를 통해 프롬프트를 프로바이더에 전달하기 전에 가로채어 수정하거나 추가 작업을 수행할 수 있습니다. 미들웨어를 추가하려면 `HasMiddleware` 인터페이스를 구현하고, 미들웨어 클래스 배열을 반환하는 `middleware` 메서드를 작성합니다:

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
     * 에이전트의 미들웨어를 반환합니다.
     */
    public function middleware(): array
    {
        return [
            new LogPrompts,
        ];
    }
}
```

각 미들웨어 클래스는 `handle` 메서드를 구현해야 하며, `AgentPrompt`와 다음 미들웨어로 프롬프트를 전달하는 `Closure`를 받습니다:

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

응답 처리 후 추가 로직은 `then` 메서드로 구현할 수 있습니다(동기, 스트리밍 모두 지원):

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

간단히 모델과 상호작용하고자 할 때, 별도의 에이전트 클래스 없이도 `agent` 함수를 통해 임시 익명 에이전트를 생성할 수 있습니다:

```php
use function Laravel\Ai\{agent};

$response = agent(
    instructions: 'You are an expert at software development.',
    messages: [],
    tools: [],
)->prompt('Tell me about Laravel')
```

익명 에이전트에서도 구조화된 출력을 반환할 수 있습니다:

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
### 에이전트 설정

에이전트 내에서는 PHP 속성(Attribute)을 통해 텍스트 생성 옵션을 세밀하게 제어할 수 있습니다. 사용 가능한 속성은 다음과 같습니다:

- `MaxSteps`: 툴 사용 시 에이전트가 수행할 최대 단계 수.
- `MaxTokens`: 모델이 생성할 수 있는 최대 토큰 수.
- `Model`: 사용할 모델명.
- `Provider`: 사용할 AI 프로바이더(또는 여러 개로 failover 사용 가능).
- `Temperature`: 생성 시 사용하는 샘플링 온도(0.0 ~ 1.0).
- `Timeout`: 에이전트 요청의 HTTP 타임아웃(초, 기본값: 60).
- `UseCheapestModel`: 비용 효율성이 가장 높은 모델을 사용.
- `UseSmartestModel`: 가장 강력한 모델을 사용(복잡한 과제에 적합).

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
use Laravel\Ai\Enums\Lab;
use Laravel\Ai\Promptable;

#[Provider(Lab::Anthropic)]
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

`UseCheapestModel`, `UseSmartestModel` 속성은 모델명을 별도로 지정하지 않더라도, 각 프로바이더의 최저가 모델 또는 최고성능 모델을 자동 선택하게 해줍니다. 비용 최적화, 성능 우선 전략에 모두 적합합니다.

```php
use Laravel\Ai\Attributes\UseCheapestModel;
use Laravel\Ai\Attributes\UseSmartestModel;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Promptable;

#[UseCheapestModel]
class SimpleSummarizer implements Agent
{
    use Promptable;

    // 예) Haiku 같이 가장 저렴한 모델 사용
}

#[UseSmartestModel]
class ComplexReasoner implements Agent
{
    use Promptable;

    // 예) Opus 등 최고의 모델 사용
}
```

<a name="images"></a>
## 이미지

`Laravel\Ai\Image` 클래스를 사용하여 `openai`, `gemini`, `xai` 프로바이더로 이미지를 생성할 수 있습니다:

```php
use Laravel\Ai\Image;

$image = Image::of('A donut sitting on the kitchen counter')->generate();

$rawContent = (string) $image;
```

`square`, `portrait`, `landscape` 메서드는 이미지의 가로세로 비율을 지정하며, `quality`(high, medium, low)는 품질, `timeout`은 HTTP 제한시간(초)을 설정합니다:

```php
use Laravel\Ai\Image;

$image = Image::of('A donut sitting on the kitchen counter')
    ->quality('high')
    ->landscape()
    ->timeout(120)
    ->generate();
```

참조 이미지 첨부는 `attachments` 메서드를 통해 지원됩니다:

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

생성된 이미지는 `config/filesystems.php`의 기본 디스크에 매우 간단히 저장할 수 있습니다:

```php
$image = Image::of('A donut sitting on the kitchen counter');

$path = $image->store();
$path = $image->storeAs('image.jpg');
$path = $image->storePublicly();
$path = $image->storePubliclyAs('image.jpg');
```

이미지 생성 작업도 큐잉이 가능합니다:

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

`Laravel\Ai\Audio` 클래스를 사용하여 텍스트를 음성으로 합성할 수 있습니다:

```php
use Laravel\Ai\Audio;

$audio = Audio::of('I love coding with Laravel.')->generate();

$rawContent = (string) $audio;
```

음성의 성별·스타일은 `male`, `female`, `voice` 메서드로 설정합니다:

```php
$audio = Audio::of('I love coding with Laravel.')
    ->female()
    ->generate();

$audio = Audio::of('I love coding with Laravel.')
    ->voice('voice-id-or-name')
    ->generate();
```

`instructions` 메서드는 합성 오디오에 원하는 톤을 지시할 수 있습니다:

```php
$audio = Audio::of('I love coding with Laravel.')
    ->female()
    ->instructions('Said like a pirate')
    ->generate();
```

생성된 오디오도 파일시스템의 기본 디스크에 쉽게 저장 가능합니다:

```php
$audio = Audio::of('I love coding with Laravel.')->generate();

$path = $audio->store();
$path = $audio->storeAs('audio.mp3');
$path = $audio->storePublicly();
$path = $audio->storePubliclyAs('audio.mp3');
```

오디오 합성 역시 큐잉 방식 지원:

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

`Laravel\Ai\Transcription` 클래스를 통해 오디오 파일의 텍스트 트랜스크립트(음성→문자 변환)를 생성할 수 있습니다:

```php
use Laravel\Ai\Transcription;

$transcript = Transcription::fromPath('/home/laravel/audio.mp3')->generate();
$transcript = Transcription::fromStorage('audio.mp3')->generate();
$transcript = Transcription::fromUpload($request->file('audio'))->generate();

return (string) $transcript;
```

응답에 화자(스피커)별로 세분화된 트랜스크립트를 원하면, `diarize` 메서드를 활용하세요:

```php
$transcript = Transcription::fromStorage('audio.mp3')
    ->diarize()
    ->generate();
```

트랜스크립션 역시 큐잉 가능합니다:

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

어떤 문자열이라도 손쉽게 벡터 임베딩으로 변환할 수 있습니다. Laravel의 `Stringable` 클래스에 추가된 `toEmbeddings` 메서드를 활용하세요:

```php
use Illuminate\Support\Str;

$embeddings = Str::of('Napa Valley has great wine.')->toEmbeddings();
```

또는 `Embeddings` 클래스를 이용해 여러 인풋을 한 번에 임베딩할 수도 있습니다:

```php
use Laravel\Ai\Embeddings;

$response = Embeddings::for([
    'Napa Valley has great wine.',
    'Laravel is a PHP framework.',
])->generate();

$response->embeddings; // [[0.123, 0.456, ...], [0.789, 0.012, ...]]
```

임베딩 차원, 프로바이더도 지정할 수 있습니다:

```php
$response = Embeddings::for(['Napa Valley has great wine.'])
    ->dimensions(1536)
    ->generate(Lab::OpenAI, 'text-embedding-3-small');
```

<a name="querying-embeddings"></a>
### 임베딩 쿼리

임베딩 생성 후, 보통은 향후 검색을 위해 임베딩을 데이터베이스의 `vector` 컬럼에 저장합니다. Laravel에서는 PostgreSQL의 `pgvector` 확장을 통해 벡터 컬럼을 지원합니다. 시작하려면 마이그레이션에서 벡터 컬럼과 차원을 지정하세요:

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

검색 속도 향상을 위해 벡터 인덱스를 추가할 수도 있습니다. `index` 메서드를 호출하면, cosine distance를 사용하는 HNSW 인덱스가 자동 생성됩니다:

```php
$table->vector('embedding', dimensions: 1536)->index();
```

Eloquent 모델에서는 해당 컬럼을 `array`로 캐스팅하세요:

```php
protected function casts(): array
{
    return [
        'embedding' => 'array',
    ];
}
```

유사 문서 쿼리는 `whereVectorSimilarTo` 메서드를 활용합니다. 최소 코사인 유사도(minSimilarity: 0.0 ~ 1.0, 1.0은 완전 동일)로 필터링하고, 유사도 순으로 정렬합니다:

```php
use App\Models\Document;

$documents = Document::query()
    ->whereVectorSimilarTo('embedding', $queryEmbedding, minSimilarity: 0.4)
    ->limit(10)
    ->get();
```

`$queryEmbedding`은 float 배열 또는 그냥 문자열도 가능합니다. 문자열이면 임베딩이 자동 생성됩니다:

```php
$documents = Document::query()
    ->whereVectorSimilarTo('embedding', 'best wineries in Napa Valley')
    ->limit(10)
    ->get();
```

보다 세부적인 조작은 `whereVectorDistanceLessThan`, `selectVectorDistance`, `orderByVectorDistance` 등의 메서드를 조합해서 사용할 수 있습니다:

```php
$documents = Document::query()
    ->select('*')
    ->selectVectorDistance('embedding', $queryEmbedding, as: 'distance')
    ->whereVectorDistanceLessThan('embedding', $queryEmbedding, maxDistance: 0.3)
    ->orderByVectorDistance('embedding', $queryEmbedding)
    ->limit(10)
    ->get();
```

에이전트에게 유사도 검색 툴을 제공하고 싶다면 [Similarity Search](#similarity-search) 툴 문서를 참고하세요.

> [!NOTE]
> 벡터 쿼리는 현재 PostgreSQL의 `pgvector` 확장 기능을 사용하는 커넥션에서만 지원합니다.

<a name="caching-embeddings"></a>
### 임베딩 캐싱

동일 인풋에 대한 임베딩 생성을 반복 호출하지 않으려면, 캐싱 기능을 사용할 수 있습니다. `ai.caching.embeddings.cache` 설정값을 `true`로 두면 임베딩이 자동 캐시됩니다:

```php
'caching' => [
    'embeddings' => [
        'cache' => true,
        'store' => env('CACHE_STORE', 'database'),
        // ...
    ],
],
```

캐싱이 활성화되면, 임베딩은 30일간 저장됩니다. 캐시 키는 프로바이더, 모델, 차원, 인풋 내용을 모두 반영해 구성되므로 동일 요청시 캐시 사용, 다르면 새로 임베딩이 생성됩니다.

글로벌 캐싱이 비활성화되어 있더라도, 특정 요청에서 `cache` 메서드로 캐싱을 개별 활성화할 수 있습니다:

```php
$response = Embeddings::for(['Napa Valley has great wine.'])
    ->cache()
    ->generate();
```

캐시 지속시간(초단위)을 지정할 수도 있습니다:

```php
$response = Embeddings::for(['Napa Valley has great wine.'])
    ->cache(seconds: 3600) // 1시간 캐시
    ->generate();
```

`toEmbeddings` Stringable 메서드에도 `cache` 인자를 사용할 수 있습니다:

```php
// 기본 유지기간으로 캐시
$embeddings = Str::of('Napa Valley has great wine.')->toEmbeddings(cache: true);

// 특정 기간 캐시
$embeddings = Str::of('Napa Valley has great wine.')->toEmbeddings(cache: 3600);
```

<a name="reranking"></a>
## 재정렬(reranking)

재정렬(Reranking)은 쿼리와의 관련성 기준으로 문서 리스트의 순서를 AI의 의미적 분석을 통해 개선하는 기능입니다. 이는 검색 결과에 의미적 랭킹을 부여할 때 유용합니다.

`Laravel\Ai\Reranking` 클래스를 통해 문서 리스트를 재정렬할 수 있습니다:

```php
use Laravel\Ai\Reranking;

$response = Reranking::of([
    'Django is a Python web framework.',
    'Laravel is a PHP web application framework.',
    'React is a JavaScript library for building user interfaces.',
])->rerank('PHP frameworks');

// 가장 관련성 높은 결과 접근
$response->first()->document; // "Laravel is a PHP web application framework."
$response->first()->score;    // 0.95
$response->first()->index;    // 1 (원래 위치)
```

결과 개수 제한은 `limit` 메서드로 지정할 수 있습니다:

```php
$response = Reranking::of($documents)
    ->limit(5)
    ->rerank('search query');
```

<a name="reranking-collections"></a>
### 컬렉션 재정렬

Laravel 컬렉션에서도 `rerank` 매크로로 손쉽게 의미적 랭킹을 적용할 수 있습니다. 첫 번째 인수는 평가할 필드, 두 번째는 쿼리입니다:

```php
// 단일 필드 기준 리랭킹
$posts = Post::all()
    ->rerank('body', 'Laravel tutorials');

// 여러 필드(multi-field)는 배열(JSON)로
$reranked = $posts->rerank(['title', 'body'], 'Laravel tutorials');

// 클로저로 문서 구조 지정도 가능
$reranked = $posts->rerank(
    fn ($post) => $post->title.': '.$post->body,
    'Laravel tutorials'
);
```

결과 개수 제한, 프로바이더 지정도 지원합니다:

```php
$reranked = $posts->rerank(
    by: 'content',
    query: 'Laravel tutorials',
    limit: 10,
    provider: Lab::Cohere
);
```

<a name="files"></a>
## 파일

`Laravel\Ai\Files` 또는 개별 파일 클래스를 이용해, AI 프로바이더에 파일 저장 후 대화에서 반복 참조할 수 있습니다. 대용량 문서나 여러 번 사용할 파일은 별도 업로드 없이 고유 ID로 참조가 가능합니다:

```php
use Laravel\Ai\Files\Document;
use Laravel\Ai\Files\Image;

// 로컬 경로 파일 저장
$response = Document::fromPath('/home/laravel/document.pdf')->put();
$response = Image::fromPath('/home/laravel/photo.jpg')->put();

// 파일시스템 디스크 파일 저장
$response = Document::fromStorage('document.pdf', disk: 'local')->put();
$response = Image::fromStorage('photo.jpg', disk: 'local')->put();

// 원격 URL에서 파일 저장
$response = Document::fromUrl('https://example.com/document.pdf')->put();
$response = Image::fromUrl('https://example.com/photo.jpg')->put();

return $response->id;
```

메모리(raw content)나 업로드 파일도 저장할 수 있습니다:

```php
use Laravel\Ai\Files;
use Laravel\Ai\Files\Document;

// 원본 내용 저장
$stored = Document::fromString('Hello, World!', 'text/plain')->put();

// 업로드 파일 저장
$stored = Document::fromUpload($request->file('document'))->put();
```

이미 저장된 파일은 에이전트 프롬프트에 재첨부할 수 있습니다. 이때 재전송 필요 없이 파일 ID만으로 참조가 가능합니다:

```php
use App\Ai\Agents\SalesCoach;
use Laravel\Ai\Files;

$response = (new SalesCoach)->prompt(
    'Analyze the attached sales transcript...',
    attachments: [
        Files\Document::fromId('file-id'), // 저장 파일 첨부
    ]
);
```

파일을 다시 가져오려면 인스턴스의 `get` 메서드를 사용합니다:

```php
use Laravel\Ai\Files\Document;

$file = Document::fromId('file-id')->get();

$file->id;
$file->mimeType();
```

프로바이더에서 파일을 삭제하려면 `delete`를 호출하세요:

```php
Document::fromId('file-id')->delete();
```

별도 지정이 없으면 `Files` 클래스는 `config/ai.php`의 기본 AI 프로바이더를 사용합니다. 연산별로 다른 프로바이더를 지정하는 것도 가능합니다:

```php
$response = Document::fromPath(
    '/home/laravel/document.pdf'
)->put(provider: Lab::Anthropic);
```

<a name="using-stored-files-in-conversations"></a>
### 대화에서 저장된 파일 사용

한 번 저장된 파일은 ID로 간단히 대화에 첨부할 수 있습니다. 아래는 `Document`/`Image` 클래스의 `fromId` 메서드를 이용하는 예시입니다:

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

이미지도 마찬가지로 `Image` 클래스를 활용해 참조할 수 있습니다:

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

벡터 스토어는 검색이 가능한 파일 컬렉션을 생성하여, RAG(Retrieval Augmented Generation)에 활용할 수 있습니다. `Laravel\Ai\Stores` 클래스를 사용하면 벡터 스토어 생성/조회/삭제가 가능합니다:

```php
use Laravel\Ai\Stores;

// 새 벡터 스토어 생성
$store = Stores::create('Knowledge Base');

// 추가 옵션 포함 스토어 생성
$store = Stores::create(
    name: 'Knowledge Base',
    description: 'Documentation and reference materials.',
    expiresWhenIdleFor: days(30),
);

return $store->id;
```

기존 벡터 스토어를 ID로 불러오려면 `get` 메서드를 사용합니다:

```php
use Laravel\Ai\Stores;

$store = Stores::get('store_id');

$store->id;
$store->name;
$store->fileCounts;
$store->ready;
```

스토어를 삭제하려면 `Stores` 클래스나 스토어 인스턴스에서 `delete`를 호출합니다:

```php
use Laravel\Ai\Stores;

// ID로 삭제
Stores::delete('store_id');

// 인스턴스에서 삭제
$store = Stores::get('store_id');
$store->delete();
```

<a name="adding-files-to-stores"></a>
### 스토어에 파일 추가

벡터 스토어가 준비되었다면, [파일](#files)을 `add` 메서드로 스토어에 추가할 수 있습니다. 추가된 파일은 [file search provider tool](#file-search)에서 바로 사용 가능한 형태로 자동 인덱싱됩니다:

```php
use Laravel\Ai\Files\Document;
use Laravel\Ai\Stores;

$store = Stores::get('store_id');

// 프로바이더에 이미 저장된 파일 추가
$document = $store->add('file_id');
$document = $store->add(Document::fromId('file_id'));

// 또는 저장·추가를 한 번에
$document = $store->add(Document::fromPath('/path/to/document.pdf'));
$document = $store->add(Document::fromStorage('manual.pdf'));
$document = $store->add($request->file('document'));

$document->id;
$document->fileId;
```

> [!NOTE]
> 기존에 저장된 파일을 벡터 스토어에 추가할 때, 반환되는 document ID는 파일의 이전 ID와 일치하는 것이 일반적이지만, 일부 벡터 스토리지 프로바이더에서는 새 ID가 부여될 수 있습니다. 따라서 DB에는 두 ID 모두 저장해두는 것이 안전합니다.

스토어에 파일을 추가할 때 메타데이터를 함께 저장할 수 있으며, 이를 [file search provider tool](#file-search)에서 검색시 필터로 사용할 수 있습니다:

```php
$store->add(Document::fromPath('/path/to/document.pdf'), metadata: [
    'author' => 'Taylor Otwell',
    'department' => 'Engineering',
    'year' => 2026,
]);
```

파일 삭제는 `remove` 메서드로 처리합니다:

```php
$store->remove('file_id');
```

벡터 스토어에서만 삭제할 뿐, 프로바이더의 [파일 저장소](#files)에선 그대로 유지됩니다. 완전히 삭제하려면 `deleteFile` 인자를 true로 전달합니다:

```php
$store->remove('file_abc123', deleteFile: true);
```

<a name="failover"></a>
## 페일오버

프롬프트 응답 또는 기타 미디어 생성 시, 프로바이더/모델을 배열로 전달해 서비스 중단이나 레이트 리밋 발생시 자동으로 백업 프로바이더/모델로 페일오버(자동 전환)할 수 있습니다:

```php
use App\Ai\Agents\SalesCoach;
use Laravel\Ai\Image;

$response = (new SalesCoach)->prompt(
    'Analyze this sales transcript...',
    provider: [Lab::OpenAI, Lab::Anthropic],
);

$image = Image::of('A donut sitting on the kitchen counter')
    ->generate(provider: [Lab::Gemini, Lab::xAI]);
```

<a name="testing"></a>
## 테스트

<a name="testing-agents"></a>
### 에이전트

테스트에서 에이전트의 응답을 강제로 반환하려면, 에이전트 클래스의 `fake` 메서드를 사용합니다. 응답값 배열 또는 클로저를 인자로 줄 수 있습니다:

```php
use App\Ai\Agents\SalesCoach;
use Laravel\Ai\Prompts\AgentPrompt;

// 모든 프롬프트에 정해진 응답 반환
SalesCoach::fake();

// 프롬프트별 응답 목록 등록
SalesCoach::fake([
    'First response',
    'Second response',
]);

// 프롬프트에 따라 동적 응답 처리
SalesCoach::fake(function (AgentPrompt $prompt) {
    return 'Response for: '.$prompt->prompt;
});
```

> [!NOTE]
> 구조화된 출력을 반환하는 에이전트에서 `Agent::fake()`를 호출하면, 정의된 출력 스키마에 맞는 가짜 데이터가 자동 생성됩니다.

프롬프트 이후 요청받은 프롬프트에 대해 어설션을 수행할 수 있습니다:

```php
use Laravel\Ai\Prompts\AgentPrompt;

SalesCoach::assertPrompted('Analyze this...');

SalesCoach::assertPrompted(function (AgentPrompt $prompt) {
    return $prompt->contains('Analyze');
});

SalesCoach::assertNotPrompted('Missing prompt');

SalesCoach::assertNeverPrompted();
```

큐잉된 에이전트는 별도의 큐드 어설션 메서드를 사용하세요:

```php
use Laravel\Ai\QueuedAgentPrompt;

SalesCoach::assertQueued('Analyze this...');

SalesCoach::assertQueued(function (QueuedAgentPrompt $prompt) {
    return $prompt->contains('Analyze');
});

SalesCoach::assertNotQueued('Missing prompt');

SalesCoach::assertNeverQueued();
```

모든 호출에 대해 가짜 응답이 있어야 하는 경우 `preventStrayPrompts`를 사용하세요. 정의된 fake 없이 에이전트가 호출되면 예외가 발생합니다:

```php
SalesCoach::fake()->preventStrayPrompts();
```

<a name="testing-images"></a>
### 이미지

이미지 생성도 `Image` 클래스의 `fake` 메서드로 모킹이 가능합니다. 모킹 이후에는 어설션을 다양하게 지원합니다:

```php
use Laravel\Ai\Image;
use Laravel\Ai\Prompts\ImagePrompt;
use Laravel\Ai\Prompts\QueuedImagePrompt;

// 모든 이미지 프롬프트에 고정 응답
Image::fake();

// 프롬프트별 이미지 결과 배열 등록
Image::fake([
    base64_encode($firstImage),
    base64_encode($secondImage),
]);

// 프롬프트에 맞게 동적으로 응답
Image::fake(function (ImagePrompt $prompt) {
    return base64_encode('...');
});
```

어설션 예시:

```php
Image::assertGenerated(function (ImagePrompt $prompt) {
    return $prompt->contains('sunset') && $prompt->isLandscape();
});

Image::assertNotGenerated('Missing prompt');

Image::assertNothingGenerated();
```

큐잉된 이미지 생성도 큐드 어설션으로 확인:

```php
Image::assertQueued(
    fn (QueuedImagePrompt $prompt) => $prompt->contains('sunset')
);

Image::assertNotQueued('Missing prompt');

Image::assertNothingQueued();
```

모든 이미지 생성이 가짜 응답을 갖도록 하려면 `preventStrayImages`를 사용합니다:

```php
Image::fake()->preventStrayImages();
```

<a name="testing-audio"></a>
### 오디오

오디오 역시 `Audio` 클래스의 `fake`로 모킹 및 어설션이 가능합니다:

```php
use Laravel\Ai\Audio;
use Laravel\Ai\Prompts\AudioPrompt;
use Laravel\Ai\Prompts\QueuedAudioPrompt;

// 모든 오디오 프롬프트에 고정 응답
Audio::fake();

// 별도 응답 배열 등록
Audio::fake([
    base64_encode($firstAudio),
    base64_encode($secondAudio),
]);

// 프롬프트에 따라 동적 응답
Audio::fake(function (AudioPrompt $prompt) {
    return base64_encode('...');
});
```

어설션 예시:

```php
Audio::assertGenerated(function (AudioPrompt $prompt) {
    return $prompt->contains('Hello') && $prompt->isFemale();
});

Audio::assertNotGenerated('Missing prompt');

Audio::assertNothingGenerated();
```

큐잉 오디오는 아래와 같이 어설션:

```php
Audio::assertQueued(
    fn (QueuedAudioPrompt $prompt) => $prompt->contains('Hello')
);

Audio::assertNotQueued('Missing prompt');

Audio::assertNothingQueued();
```

모든 오디오 생성에 가짜 응답이 필요하면 `preventStrayAudio` 사용:

```php
Audio::fake()->preventStrayAudio();
```

<a name="testing-transcriptions"></a>
### 트랜스크립션

트랜스크립션 생성도 `Transcription` 클래스의 `fake`로 처리할 수 있습니다:

```php
use Laravel\Ai\Transcription;
use Laravel\Ai\Prompts\TranscriptionPrompt;
use Laravel\Ai\Prompts\QueuedTranscriptionPrompt;

// 모든 트랜스크립트에 고정 응답
Transcription::fake();

// 응답 배열 등록
Transcription::fake([
    'First transcription text.',
    'Second transcription text.',
]);

// 프롬프트별 동적 응답
Transcription::fake(function (TranscriptionPrompt $prompt) {
    return 'Transcribed text...';
});
```

어설션 예시:

```php
Transcription::assertGenerated(function (TranscriptionPrompt $prompt) {
    return $prompt->language === 'en' && $prompt->isDiarized();
});

Transcription::assertNotGenerated(
    fn (TranscriptionPrompt $prompt) => $prompt->language === 'fr'
);

Transcription::assertNothingGenerated();
```

큐잉 트랜스크립션 어설션:

```php
Transcription::assertQueued(
    fn (QueuedTranscriptionPrompt $prompt) => $prompt->isDiarized()
);

Transcription::assertNotQueued(
    fn (QueuedTranscriptionPrompt $prompt) => $prompt->language === 'fr'
);

Transcription::assertNothingQueued();
```

모든 트랜스크립션 생성을 강제로 막으려면 `preventStrayTranscriptions`를 사용하세요:

```php
Transcription::fake()->preventStrayTranscriptions();
```

<a name="testing-embeddings"></a>
### 임베딩

임베딩 생성도 `Embeddings` 클래스의 `fake`로 모킹 가능하며, 이후 각종 어설션을 지원합니다:

```php
use Laravel\Ai\Embeddings;
use Laravel\Ai\Prompts\EmbeddingsPrompt;
use Laravel\Ai\Prompts\QueuedEmbeddingsPrompt;

// 적절한 차원의 가짜 임베딩 자동 생성
Embeddings::fake();

// 응답 배열 등록
Embeddings::fake([
    [$firstEmbeddingVector],
    [$secondEmbeddingVector],
]);

// 프롬프트에 따라 동적 응답 생성
Embeddings::fake(function (EmbeddingsPrompt $prompt) {
    return array_map(
        fn () => Embeddings::fakeEmbedding($prompt->dimensions),
        $prompt->inputs
    );
});
```

어설션 예시:

```php
Embeddings::assertGenerated(function (EmbeddingsPrompt $prompt) {
    return $prompt->contains('Laravel') && $prompt->dimensions === 1536;
});

Embeddings::assertNotGenerated(
    fn (EmbeddingsPrompt $prompt) => $prompt->contains('Other')
);

Embeddings::assertNothingGenerated();
```

큐잉 임베딩 어설션:

```php
Embeddings::assertQueued(
    fn (QueuedEmbeddingsPrompt $prompt) => $prompt->contains('Laravel')
);

Embeddings::assertNotQueued(
    fn (QueuedEmbeddingsPrompt $prompt) => $prompt->contains('Other')
);

Embeddings::assertNothingQueued();
```

모든 임베딩 생성 요청에 가짜 응답이 필요하면 `preventStrayEmbeddings` 사용:

```php
Embeddings::fake()->preventStrayEmbeddings();
```

<a name="testing-reranking"></a>
### 재정렬

재정렬 동작은 `Reranking` 클래스의 `fake`로 모킹할 수 있습니다:

```php
use Laravel\Ai\Reranking;
use Laravel\Ai\Prompts\RerankingPrompt;
use Laravel\Ai\Responses\Data\RankedDocument;

// 가짜 결과 자동 생성
Reranking::fake();

// 커스텀 응답 등록
Reranking::fake([
    [
        new RankedDocument(index: 0, document: 'First', score: 0.95),
        new RankedDocument(index: 1, document: 'Second', score: 0.80),
    ],
]);
```

어설션 예시:

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

파일 작업은 `Files` 클래스의 `fake`로 테스트 환경에서 모킹 가능:

```php
use Laravel\Ai\Files;

Files::fake();
```

파일 업로드·삭제 상황에 대해 어설션을 설정할 수 있습니다:

```php
use Laravel\Ai\Contracts\Files\StorableFile;
use Laravel\Ai\Files\Document;

// 파일 저장
Document::fromString('Hello, Laravel!', mime: 'text/plain')
    ->as('hello.txt')
    ->put();

// 어설션
Files::assertStored(fn (StorableFile $file) =>
    (string) $file === 'Hello, Laravel!' &&
        $file->mimeType() === 'text/plain';
);

Files::assertNotStored(fn (StorableFile $file) =>
    (string) $file === 'Hello, World!'
);

Files::assertNothingStored();
```

삭제에 대해서는 파일 ID를 넘겨서 어설션:

```php
Files::assertDeleted('file-id');
Files::assertNotDeleted('file-id');
Files::assertNothingDeleted();
```

<a name="testing-vector-stores"></a>
### 벡터 스토어

벡터 스토어 조작도 `Stores` 클래스의 `fake`로 완벽히 모킹할 수 있습니다. 벡터 스토어를 모킹하면 [파일 작업](#files)도 자동 모킹됩니다:

```php
use Laravel\Ai\Stores;

Stores::fake();
```

스토어 생성/삭제에 대한 어설션도 아래와 같습니다:

```php
use Laravel\Ai\Stores;

// 스토어 생성
$store = Stores::create('Knowledge Base');

// 어설션
Stores::assertCreated('Knowledge Base');

Stores::assertCreated(fn (string $name, ?string $description) =>
    $name === 'Knowledge Base'
);

Stores::assertNotCreated('Other Store');

Stores::assertNothingCreated();
```

삭제 어설션(스토어 ID 전달):

```php
Stores::assertDeleted('store_id');
Stores::assertNotDeleted('other_store_id');
Stores::assertNothingDeleted();
```

스토어 인스턴스 단위로 파일 추가/삭제도 어설션 제공:

```php
Stores::fake();

$store = Stores::get('store_id');

// 파일 추가/삭제 
$store->add('added_id');
$store->remove('removed_id');

// 어설션
$store->assertAdded('added_id');
$store->assertRemoved('removed_id');

$store->assertNotAdded('other_file_id');
$store->assertNotRemoved('other_file_id');
```

파일 저장과 벡터 스토어 추가가 한 번에 이뤄질 때처럼 파일의 ID를 명확히 알 수 없다면, `assertAdded`에 클로저로 파일 내용 기반 체크도 가능합니다:

```php
use Laravel\Ai\Contracts\Files\StorableFile;
use Laravel\Ai\Files\Document;

$store->add(Document::fromString('Hello, World!', 'text/plain')->as('hello.txt'));

$store->assertAdded(fn (StorableFile $file) => $file->name() === 'hello.txt');
$store->assertAdded(fn (StorableFile $file) => $file->content() === 'Hello, World!');
```

<a name="events"></a>
## 이벤트

Laravel AI SDK는 다양한 [이벤트](/docs/12.x/events)를 발생시킵니다. 예시로는 다음과 같습니다:

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

이러한 이벤트를 리스닝하여, AI SDK 사용 로그 기록이나 통계 수집 등에 활용할 수 있습니다.
