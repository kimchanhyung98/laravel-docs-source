# Laravel AI SDK (Laravel AI SDK)

- [소개](#introduction)
- [설치](#installation)
    - [설정](#configuration)
    - [사용자 지정 기본 URL](#custom-base-urls)
    - [지원하는 공급자](#provider-support)
- [에이전트](#agents)
    - [프롬프트 입력](#prompting)
    - [대화 컨텍스트](#conversation-context)
    - [구조화된 출력](#structured-output)
    - [첨부 파일](#attachments)
    - [스트리밍](#streaming)
    - [브로드캐스팅](#broadcasting)
    - [큐잉](#queueing)
    - [툴](#tools)
    - [공급자 툴](#provider-tools)
    - [미들웨어](#middleware)
    - [익명 에이전트](#anonymous-agents)
    - [에이전트 설정](#agent-configuration)
- [이미지](#images)
- [오디오 (TTS)](#audio)
- [트랜스크립션 (STT)](#transcription)
- [임베딩](#embeddings)
    - [임베딩 쿼리](#querying-embeddings)
    - [임베딩 캐싱](#caching-embeddings)
- [재정렬(Reranking)](#reranking)
- [파일](#files)
- [벡터 스토어](#vector-stores)
    - [스토어에 파일 추가](#adding-files-to-stores)
- [장애 조치(Failover)](#failover)
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

[Laravel AI SDK](https://github.com/laravel/ai)는 OpenAI, Anthropic, Gemini 등과 같은 다양한 AI 공급자와 상호작용할 수 있는 통합적이고 표현력 있는 API를 제공합니다. AI SDK를 사용하면 도구 및 구조화된 출력이 포함된 지능형 에이전트 구축, 이미지 생성, 오디오 합성 및 트랜스크립션, 벡터 임베딩 생성 등 모든 작업을 일관되고 Laravel 친화적인 인터페이스로 구현할 수 있습니다.

<a name="installation"></a>
## 설치 (Installation)

Laravel AI SDK는 Composer를 통해 설치할 수 있습니다:

```shell
composer require laravel/ai
```

다음으로, `vendor:publish` Artisan 명령어를 사용하여 AI SDK 설정 파일 및 마이그레이션 파일을 게시해야 합니다:

```shell
php artisan vendor:publish --provider="Laravel\Ai\AiServiceProvider"
```

마지막으로, 애플리케이션의 데이터베이스 마이그레이션을 실행하세요. 이는 AI SDK가 대화 저장에 사용하는 `agent_conversations` 및 `agent_conversation_messages` 테이블을 생성합니다:

```shell
php artisan migrate
```

<a name="configuration"></a>
### 설정 (Configuration)

AI 공급자 인증 정보를 애플리케이션의 `config/ai.php` 설정 파일이나, 환경 변수 파일(`.env`)에 정의할 수 있습니다:

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

텍스트, 이미지, 오디오, 트랜스크립션, 임베딩에 대한 기본 모델도 `config/ai.php` 파일에서 설정할 수 있습니다.

<a name="custom-base-urls"></a>
### 사용자 지정 기본 URL (Custom Base URLs)

기본적으로 Laravel AI SDK는 각 공급자의 공개 API 엔드포인트에 직접 연결합니다. 그러나 프록시 서비스를 통하거나, API 키 관리를 중앙화하거나, 레이트 리밋 적용, 혹은 사내 게이트웨이를 거쳐야 하는 경우, 요청을 다른 엔드포인트로 라우팅해야 할 수 있습니다.

공급자 설정에 `url` 파라미터를 추가하여 사용자 지정 기본 URL을 구성할 수 있습니다:

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

이 기능은 LiteLLM 또는 Azure OpenAI Gateway와 같은 프록시 서비스를 사용할 때, 또는 대체 엔드포인트에 연결해야 할 때 유용합니다.

사용자 지정 기본 URL은 OpenAI, Anthropic, Gemini, Groq, Cohere, DeepSeek, xAI, OpenRouter 공급자에서 지원됩니다.

<a name="provider-support"></a>
### 지원하는 공급자 (Provider Support)

AI SDK는 기능별로 다양한 공급자를 지원합니다. 아래 표는 각 기능별로 지원되는 공급자를 요약합니다:

| 기능    | 지원 공급자 |
|---|---|
| 텍스트 | OpenAI, Anthropic, Gemini, Groq, xAI, DeepSeek, Mistral, Ollama |
| 이미지 | OpenAI, Gemini, xAI |
| TTS    | OpenAI, ElevenLabs |
| STT    | OpenAI, ElevenLabs, Mistral |
| 임베딩 | OpenAI, Gemini, Cohere, Mistral, Jina, VoyageAI |
| 재정렬 | Cohere, Jina |
| 파일   | OpenAI, Anthropic, Gemini |

<a name="agents"></a>
## 에이전트 (Agents)

에이전트는 Laravel AI SDK에서 AI 공급자와 상호작용할 때 사용하는 기본 빌딩 블록입니다. 각각의 에이전트는 프롬프트, 대화 컨텍스트, 도구, 출력 스키마를 캡슐화한 전용 PHP 클래스입니다. 에이전트를 전문적인 어시스턴트(예: 영업 코치, 문서 분석기, 지원 챗봇 등)로 생각하면 이해하기 쉽습니다. 한 번 설정해두고 애플리케이션 전반에서 필요할 때마다 프롬프트 할 수 있습니다.

에이전트는 `make:agent` Artisan 명령어로 생성할 수 있습니다:

```shell
php artisan make:agent SalesCoach

php artisan make:agent SalesCoach --structured
```

생성된 에이전트 클래스 내에서 시스템 프롬프트/지침, 메시지 컨텍스트, 사용 가능한 도구, (필요한 경우) 출력 스키마를 정의할 수 있습니다:

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
     * 에이전트가 사용할 수 있는 도구를 반환합니다.
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
### 프롬프트 입력 (Prompting)

에이전트에 프롬프트를 입력하려면, 먼저 `make` 메서드를 사용하거나 직접 인스턴스를 생성한 후 `prompt`를 호출하면 됩니다:

```php
$response = (new SalesCoach)
    ->prompt('Analyze this sales transcript...');

$response = SalesCoach::make()
    ->prompt('Analyze this sales transcript...');

return (string) $response;
```

`make` 메서드는 에이전트를 컨테이너에서 자동으로 의존성 주입한 후 반환합니다. 생성자에 인수를 넣어 에이전트에 전달할 수도 있습니다:

```php
$agent = SalesCoach::make(user: $user);
```

추가적으로 `prompt` 메서드에 인자를 전달하여 기본 공급자, 모델 또는 HTTP 타임아웃을 임시로 변경할 수 있습니다:

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

에이전트가 `Conversational` 인터페이스를 구현했다면, `messages` 메서드를 통해 이전 대화 컨텍스트를 반환할 수 있습니다:

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
#### 대화 기억하기 (Remembering Conversations)

> **Note:** `RemembersConversations` 트레이트를 사용하기 전에, `vendor:publish` Artisan 명령어로 AI SDK 마이그레이션을 게시 및 실행해야 합니다. 이 마이그레이션은 대화 저장에 필요한 데이터베이스 테이블을 생성합니다.

Laravel에서 에이전트의 대화 내역을 자동으로 저장/불러오고 싶다면, `RemembersConversations` 트레이트를 사용할 수 있습니다. 이 트레이트를 적용하면 `Conversational` 인터페이스를 수동으로 구현하지 않아도 대화 메시지를 데이터베이스에 간단히 영구 저장할 수 있습니다:

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

새로운 사용자별 대화를 시작하려면 프롬프트 전에 `forUser` 메서드를 사용하세요:

```php
$response = (new SalesCoach)->forUser($user)->prompt('Hello!');

$conversationId = $response->conversationId;
```

대화 ID는 응답에서 반환되며, 추후 참조를 위해 저장할 수 있습니다. 아니면 직접 `agent_conversations` 테이블에서 사용자의 모든 대화를 조회할 수도 있습니다.

기존 대화를 이어가려면 `continue` 메서드를 사용합니다:

```php
$response = (new SalesCoach)
    ->continue($conversationId, as: $user)
    ->prompt('Tell me more about that.');
```

`RemembersConversations` 트레이트를 사용할 때는 이전 메시지가 자동으로 컨텍스트에 포함되고, 새 메시지(사용자/어시스턴트 모두)도 매 상호작용 후 자동 저장됩니다.

<a name="structured-output"></a>
### 구조화된 출력 (Structured Output)

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

구조화된 출력을 반환하는 에이전트에 프롬프트를 입력하면, 반환되는 `StructuredAgentResponse`를 배열처럼 사용할 수 있습니다:

```php
$response = (new SalesCoach)->prompt('Analyze this sales transcript...');

return $response['score'];
```

<a name="attachments"></a>
### 첨부 파일 (Attachments)

프롬프트 입력 시, 이미지나 문서 첨부를 통해 모델이 해당 파일을 분석할 수 있도록 할 수 있습니다:

```php
use App\Ai\Agents\SalesCoach;
use Laravel\Ai\Files;

$response = (new SalesCoach)->prompt(
    'Analyze the attached sales transcript...',
    attachments: [
        Files\Document::fromStorage('transcript.pdf'), // 파일 시스템 디스크에서 첨부...
        Files\Document::fromPath('/home/laravel/transcript.md'), // 로컬 경로에서 첨부...
        $request->file('transcript'), // 업로드된 파일 첨부...
    ]
);
```

마찬가지로 `Laravel\Ai\Files\Image` 클래스를 사용해 이미지를 첨부할 수 있습니다:

```php
use App\Ai\Agents\ImageAnalyzer;
use Laravel\Ai\Files;

$response = (new ImageAnalyzer)->prompt(
    'What is in this image?',
    attachments: [
        Files\Image::fromStorage('photo.jpg'), // 파일 시스템에서 이미지 첨부...
        Files\Image::fromPath('/home/laravel/photo.jpg'), // 로컬 경로 첨부...
        $request->file('photo'), // 업로드된 파일 첨부...
    ]
);
```

<a name="streaming"></a>
### 스트리밍 (Streaming)

에이전트의 응답을 스트리밍하려면 `stream` 메서드를 사용하세요. 반환된 `StreamableAgentResponse`는 라우트에서 반환하여 클라이언트에 스트리밍 응답(SSE)으로 전송할 수 있습니다:

```php
use App\Ai\Agents\SalesCoach;

Route::get('/coach', function () {
    return (new SalesCoach)->stream('Analyze this sales transcript...');
});
```

`then` 메서드를 사용하면 전체 응답이 클라이언트로 스트리밍된 뒤 실행할 콜백(클로저)을 지정할 수 있습니다:

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

또는 스트림 이벤트를 직접 반복(iterate)해서 처리할 수도 있습니다:

```php
$stream = (new SalesCoach)->stream('Analyze this sales transcript...');

foreach ($stream as $event) {
    // ...
}
```

<a name="streaming-using-the-vercel-ai-sdk-protocol"></a>
#### Vercel AI SDK 프로토콜을 사용한 스트리밍

[Vercel AI SDK 스트림 프로토콜](https://ai-sdk.dev/docs/ai-sdk-ui/stream-protocol)을 이용해 이벤트를 스트리밍하려면, 스트리밍 응답에서 `usingVercelDataProtocol` 메서드를 사용하세요:

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

스트리밍된 이벤트를 여러 방식으로 브로드캐스트할 수 있습니다. 가장 간단하게는, 스트리밍 이벤트에서 `broadcast` 또는 `broadcastNow` 메서드를 호출하면 됩니다:

```php
use App\Ai\Agents\SalesCoach;
use Illuminate\Broadcasting\Channel;

$stream = (new SalesCoach)->stream('Analyze this sales transcript...');

foreach ($stream as $event) {
    $event->broadcast(new Channel('channel-name'));
}
```

또는, 에이전트의 `broadcastOnQueue` 메서드를 통해 에이전트 작업을 큐로 처리하고, 실시간으로 스트리밍 이벤트를 브로드캐스팅할 수도 있습니다:

```php
(new SalesCoach)->broadcastOnQueue(
    'Analyze this sales transcript...',
    new Channel('channel-name'),
);
```

<a name="queueing"></a>
### 큐잉 (Queueing)

에이전트의 `queue` 메서드를 사용하면, 응답 처리를 백그라운드에서 수행해 애플리케이션의 반응 속도를 높일 수 있습니다. 작업 완료(응답 반환) 시 혹은 예외 발생 시 실행할 콜백은 `then`/`catch` 메서드를 이용해 등록할 수 있습니다:

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

툴을 통해 에이전트가 프롬프트에 응답하는 과정에서 추가 기능을 활용할 수 있습니다. `make:tool` Artisan 명령어로 툴 클래스를 만들 수 있습니다:

```shell
php artisan make:tool RandomNumberGenerator
```

만들어진 툴은 `app/Ai/Tools` 디렉터리에 저장됩니다. 각각의 툴에는 에이전트가 툴을 사용할 때 호출되는 `handle` 메서드가 포함됩니다:

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
     * 툴의 목적에 대한 설명을 반환합니다.
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

툴을 정의한 후, 에이전트의 `tools` 메서드에서 반환하면 해당 에이전트에서 툴을 사용할 수 있습니다:

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
#### 유사도 검색 (Similarity Search)

`SimilaritySearch` 툴을 이용하면, 데이터베이스에 저장된 벡터 임베딩을 활용해 쿼리와 유사한 문서를 검색할 수 있습니다. 이는 애플리케이션 데이터 검색이 필요한 RAG(검색 증강 생성) 구현에 유용합니다.

가장 간단하게, 임베딩이 저장된 Eloquent 모델을 `usingModel` 메서드에 지정해서 유사도 검색 툴을 만들 수 있습니다:

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

첫 번째 인자는 Eloquent 모델 클래스이고, 두 번째 인자는 벡터 임베딩이 저장된 컬럼입니다.

유사도 임계값(0.0~1.0) 및 쿼리를 커스터마이징하는 클로저도 추가할 수 있습니다:

```php
SimilaritySearch::usingModel(
    model: Document::class,
    column: 'embedding',
    minSimilarity: 0.7,
    limit: 10,
    query: fn ($query) => $query->where('published', true),
),
```

더 세밀하게 제어하려면, 검색 결과를 반환하는 커스텀 클로저로 툴을 생성할 수 있습니다:

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

툴의 설명은 `withDescription` 메서드로 변경할 수 있습니다:

```php
SimilaritySearch::usingModel(Document::class, 'embedding')
    ->withDescription('Search the knowledge base for relevant articles.'),
```

<a name="provider-tools"></a>
### 공급자 툴 (Provider Tools)

공급자 툴은 웹 검색, URL 가져오기, 파일 검색 등과 같이 AI 공급자 자체가 네이티브하게 제공하는 특수 기능입니다. 일반 툴과 달리, 공급자 툴은 사용자의 애플리케이션 서버가 아닌, 공급자 자체에서 실행됩니다.

공급자 툴도 에이전트의 `tools` 메서드에서 반환할 수 있습니다.

<a name="web-search"></a>
#### 웹 검색 (Web Search)

`WebSearch` 공급자 툴을 사용하면 실시간 정보 검색이 가능하며, 최근 데이터, 이슈, 모델 학습 시점 이후 변화한 주제 등에 대한 질문에 답할 때 유용합니다.

**지원 공급자:** Anthropic, OpenAI, Gemini

```php
use Laravel\Ai\Providers\Tools\WebSearch;

public function tools(): iterable
{
    return [
        new WebSearch,
    ];
}
```

웹 검색 툴은 검색 횟수 제한 또는 특정 도메인으로만 결과를 제한하도록 구성할 수 있습니다:

```php
(new WebSearch)->max(5)->allow(['laravel.com', 'php.net']),
```

사용자 위치 기반으로 검색을 세분화하려면 `location` 메서드를 사용하세요:

```php
(new WebSearch)->location(
    city: 'New York',
    region: 'NY',
    country: 'US'
);
```

<a name="web-fetch"></a>
#### 웹 가져오기 (Web Fetch)

`WebFetch` 공급자 툴은 웹 페이지의 내용을 읽어오도록 에이전트에 명령할 수 있습니다. 특정 URL 분석이나 상세 정보 추출이 필요할 때 유용합니다.

**지원 공급자:** Anthropic, Gemini

```php
use Laravel\Ai\Providers\Tools\WebFetch;

public function tools(): iterable
{
    return [
        new WebFetch,
    ];
}
```

웹 가져오기 툴도 검색 횟수 제한이나 특정 도메인 허용 등으로 설정할 수 있습니다:

```php
(new WebFetch)->max(3)->allow(['docs.laravel.com']),
```

<a name="file-search"></a>
#### 파일 검색 (File Search)

`FileSearch` 공급자 툴을 사용하면 [벡터 스토어](#vector-stores)에 저장된 [파일](#files)을 검색할 수 있습니다. 이를 통해 에이전트가 업로드된 문서 내에서 관련 정보를 검색하며, RAG(검색 증강 생성) 구현이 가능합니다.

**지원 공급자:** OpenAI, Gemini

```php
use Laravel\Ai\Providers\Tools\FileSearch;

public function tools(): iterable
{
    return [
        new FileSearch(stores: ['store_id']),
    ];
}
```

여러 벡터 스토어 ID를 제공해 여러 스토어에서 동시에 검색할 수도 있습니다:

```php
new FileSearch(stores: ['store_1', 'store_2']);
```

파일에 [메타데이터](#adding-files-to-stores)가 있다면, `where` 파라미터로 검색 결과를 필터링할 수 있습니다. 단순 동등 조건이라면 배열로 전달하면 됩니다:

```php
new FileSearch(stores: ['store_id'], where: [
    'author' => 'Taylor Otwell',
    'year' => 2026,
]);
```

좀 더 복잡한 필터를 적용하려면, `FileSearchQuery` 인스턴스를 받는 클로저를 사용할 수 있습니다:

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

에이전트에서는 미들웨어를 지원하므로, 프롬프트가 공급자에 전달되기 전 가로채어 수정할 수 있습니다. 에이전트에 미들웨어를 추가하려면, `HasMiddleware` 인터페이스를 구현하고, 미들웨어 클래스 배열을 반환하는 `middleware` 메서드를 정의합니다:

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

각 미들웨어 클래스는 `AgentPrompt`와 다음 미들웨어로 프롬프트를 전달할 수 있는 `Closure`를 받는 `handle` 메서드를 정의해야 합니다:

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

응답이 완료된 후 추가 작업이 필요하다면, 응답 객체의 `then` 메서드로 콜백을 지정할 수 있습니다(동기, 스트리밍 모두 사용 가능):

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

간단하게 테스트하거나 임시로 모델에 프롬프트하고 싶을 때, 전용 에이전트 클래스를 만들지 않고 `agent` 함수를 사용할 수 있습니다:

```php
use function Laravel\Ai\{agent};

$response = agent(
    instructions: 'You are an expert at software development.',
    messages: [],
    tools: [],
)->prompt('Tell me about Laravel');
```

익명 에이전트도 구조화된 출력을 반환할 수 있습니다:

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

에이전트에서 텍스트 생성 옵션을 PHP 속성(Attribute)으로 설정할 수 있습니다. 사용 가능한 속성은 다음과 같습니다:

- `MaxSteps`: 툴 사용 시, 에이전트가 수행할 수 있는 최대 단계 수.
- `MaxTokens`: 모델이 생성할 수 있는 최대 토큰 수.
- `Provider`: 에이전트에서 사용할 AI 공급자(또는 장애 조치용 복수 공급자).
- `Temperature`: 생성 온도(0.0~1.0).
- `Timeout`: 에이전트 요청 시의 HTTP 타임아웃 초(default: 60).
- `UseCheapestModel`: 비용 최적화를 위해 공급자의 가장 저렴한 텍스트 모델을 사용.
- `UseSmartestModel`: 복잡한 작업을 위해 공급자의 가장 높은 성능의 텍스트 모델을 사용.

```php
<?php

namespace App\Ai\Agents;

use Laravel\Ai\Attributes\MaxSteps;
use Laravel\Ai\Attributes\MaxTokens;
use Laravel\Ai\Attributes\Provider;
use Laravel\Ai\Attributes\Temperature;
use Laravel\Ai\Attributes\Timeout;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Promptable;

#[MaxSteps(10)]
#[MaxTokens(4096)]
#[Provider('anthropic')]
#[Temperature(0.7)]
#[Timeout(120)]
class SalesCoach implements Agent
{
    use Promptable;

    // ...
}
```

`UseCheapestModel` 및 `UseSmartestModel` 속성을 사용하면, 모델명을 별도로 지정하지 않고도 가장 저렴하거나, 가장 뛰어난 모델이 자동으로 선택됩니다. 이는 공급자별로 비용 또는 성능 최적화가 필요할 때 유용합니다:

```php
use Laravel\Ai\Attributes\UseCheapestModel;
use Laravel\Ai\Attributes\UseSmartestModel;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Promptable;

#[UseCheapestModel]
class SimpleSummarizer implements Agent
{
    use Promptable;

    // 가장 저렴한 모델(e.g., Haiku) 사용
}

#[UseSmartestModel]
class ComplexReasoner implements Agent
{
    use Promptable;

    // 가장 성능이 뛰어난 모델(e.g., Opus) 사용
}
```

<a name="images"></a>
## 이미지 (Images)

`Laravel\Ai\Image` 클래스를 사용해 `openai`, `gemini`, `xai` 공급자로 이미지를 생성할 수 있습니다:

```php
use Laravel\Ai\Image;

$image = Image::of('A donut sitting on the kitchen counter')->generate();

$rawContent = (string) $image;
```

`square`, `portrait`, `landscape` 메서드는 이미지의 가로세로 비율을 설정하고, `quality` 메서드는 모델에게 이미지 품질(`high`, `medium`, `low`)을 지정하게 합니다. `timeout`으로 HTTP 타임아웃(초)도 지정할 수 있습니다:

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

생성된 이미지는 `config/filesystems.php`에서 설정한 기본 디스크에 쉽게 저장할 수 있습니다:

```php
$image = Image::of('A donut sitting on the kitchen counter');

$path = $image->store();
$path = $image->storeAs('image.jpg');
$path = $image->storePublicly();
$path = $image->storePubliclyAs('image.jpg');
```

이미지 생성 또한 큐잉 처리할 수 있습니다:

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

`Laravel\Ai\Audio` 클래스를 사용해 입력 텍스트로부터 오디오를 생성할 수 있습니다:

```php
use Laravel\Ai\Audio;

$audio = Audio::of('I love coding with Laravel.')->generate();

$rawContent = (string) $audio;
```

`male`, `female`, `voice` 메서드는 생성할 목소리 유형을 지정할 수 있습니다:

```php
$audio = Audio::of('I love coding with Laravel.')
    ->female()
    ->generate();

$audio = Audio::of('I love coding with Laravel.')
    ->voice('voice-id-or-name')
    ->generate();
```

`instructions` 메서드로 생성될 오디오의 발화 스타일에 대한 안내도 할 수 있습니다:

```php
$audio = Audio::of('I love coding with Laravel.')
    ->female()
    ->instructions('Said like a pirate')
    ->generate();
```

생성된 오디오는 기본 파일시스템 디스크에 쉽게 저장할 수 있습니다:

```php
$audio = Audio::of('I love coding with Laravel.')->generate();

$path = $audio->store();
$path = $audio->storeAs('audio.mp3');
$path = $audio->storePublicly();
$path = $audio->storePubliclyAs('audio.mp3');
```

오디오 생성도 큐잉 처리할 수 있습니다:

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

`Laravel\Ai\Transcription` 클래스를 사용해 오디오 파일에서 트랜스크립션(텍스트 변환 결과)을 생성할 수 있습니다:

```php
use Laravel\Ai\Transcription;

$transcript = Transcription::fromPath('/home/laravel/audio.mp3')->generate();
$transcript = Transcription::fromStorage('audio.mp3')->generate();
$transcript = Transcription::fromUpload($request->file('audio'))->generate();

return (string) $transcript;
```

`diarize` 메서드를 이용해, 단순 텍스트 외에 화자별로 구분된(diarized) 스크립트도 포함시킬 수 있습니다:

```php
$transcript = Transcription::fromStorage('audio.mp3')
    ->diarize()
    ->generate();
```

트랜스크립션 생성도 큐잉 처리할 수 있습니다:

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

Laravel의 `Stringable` 클래스의 `toEmbeddings` 메서드를 활용해 간단히 텍스트의 벡터 임베딩을 생성할 수 있습니다:

```php
use Illuminate\Support\Str;

$embeddings = Str::of('Napa Valley has great wine.')->toEmbeddings();
```

또는, 여러 입력값에 대해 임베딩을 생성하려면 `Embeddings` 클래스를 사용할 수 있습니다:

```php
use Laravel\Ai\Embeddings;

$response = Embeddings::for([
    'Napa Valley has great wine.',
    'Laravel is a PHP framework.',
])->generate();

$response->embeddings; // [[0.123, 0.456, ...], [0.789, 0.012, ...]]
```

임베딩의 차원 수나 공급자를 지정할 수도 있습니다:

```php
$response = Embeddings::for(['Napa Valley has great wine.'])
    ->dimensions(1536)
    ->generate('openai', 'text-embedding-3-small');
```

<a name="querying-embeddings"></a>
### 임베딩 쿼리 (Querying Embeddings)

임베딩을 생성한 후, 주로 데이터베이스의 `vector` 컬럼에 저장하여 검색에 활용합니다. Laravel은 PostgreSQL의 `pgvector` 확장으로 벡터 컬럼을 네이티브로 지원합니다.

먼저, 마이그레이션에서 벡터 컬럼을 정의합니다:

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

검색 속도를 높이기 위해 벡터 인덱스를 추가할 수 있으며, `index`를 호출하면 HNSW 인덱스와 코사인 거리 기반으로 생성됩니다:

```php
$table->vector('embedding', dimensions: 1536)->index();
```

Eloquent 모델의 `$casts` 속성에는 해당 벡터 컬럼을 `array`로 지정해야 합니다:

```php
protected function casts(): array
{
    return [
        'embedding' => 'array',
    ];
}
```

유사도 기반 검색은 `whereVectorSimilarTo` 메서드를 사용합니다. 이 메서드는 최소 코사인 유사도(0.0~1.0, 1.0일 때 완전히 동일)를 기준으로 결과를 필터링하고, 유사도 순으로 정렬합니다:

```php
use App\Models\Document;

$documents = Document::query()
    ->whereVectorSimilarTo('embedding', $queryEmbedding, minSimilarity: 0.4)
    ->limit(10)
    ->get();
```

`$queryEmbedding`에는 실수 배열 또는 일반 문자열을 사용할 수 있습니다. 문자열일 경우, Laravel이 자동으로 임베딩을 생성해줍니다:

```php
$documents = Document::query()
    ->whereVectorSimilarTo('embedding', 'best wineries in Napa Valley')
    ->limit(10)
    ->get();
```

좀 더 세밀하게 제어하려면, `whereVectorDistanceLessThan`, `selectVectorDistance`, `orderByVectorDistance` 등의 저수준 메서드를 사용할 수도 있습니다:

```php
$documents = Document::query()
    ->select('*')
    ->selectVectorDistance('embedding', $queryEmbedding, as: 'distance')
    ->whereVectorDistanceLessThan('embedding', $queryEmbedding, maxDistance: 0.3)
    ->orderByVectorDistance('embedding', $queryEmbedding)
    ->limit(10)
    ->get();
```

에이전트에 유사도 검색 기능을 툴로 제공하려면, [유사도 검색 툴](#similarity-search) 문서를 참고하세요.

> [!NOTE]
> 벡터 쿼리는 현재 PostgreSQL 연결에서 `pgvector` 확장을 사용할 때만 지원됩니다.

<a name="caching-embeddings"></a>
### 임베딩 캐싱 (Caching Embeddings)

동일한 입력에 대해 중복 API 호출을 방지하려면 임베딩 생성을 캐싱할 수 있습니다. 이를 위해 `ai.caching.embeddings.cache` 설정을 `true`로 변경하세요:

```php
'caching' => [
    'embeddings' => [
        'cache' => true,
        'store' => env('CACHE_STORE', 'database'),
        // ...
    ],
],
```

캐싱이 활성화되면, 임베딩은 30일간 캐시에 저장됩니다. 캐시 키는 공급자, 모델, 차원, 입력값에 기반하므로 완전히 같은 요청에 대해서만 캐시된 결과가 반환됩니다.

전역 캐싱이 비활성인 경우에도, 개별 요청에 대해 `cache` 메서드를 사용해 임베딩을 캐시할 수 있습니다:

```php
$response = Embeddings::for(['Napa Valley has great wine.'])
    ->cache()
    ->generate();
```

캐시 유지 시간을 초 단위로 커스텀 지정할 수도 있습니다:

```php
$response = Embeddings::for(['Napa Valley has great wine.'])
    ->cache(seconds: 3600) // 1시간 캐시
    ->generate();
```

`toEmbeddings` 메서드도 `cache` 파라미터를 지원합니다:

```php
// 기본 유지 시간으로 캐시
$embeddings = Str::of('Napa Valley has great wine.')->toEmbeddings(cache: true);

// 특정 시간 동안 캐시
$embeddings = Str::of('Napa Valley has great wine.')->toEmbeddings(cache: 3600);
```

<a name="reranking"></a>
## 재정렬(Reranking) (Reranking)

재정렬은 주어진 쿼리에 대해 문서 목록의 순서를 의미 기반으로 새롭게 평가하고 정렬하는 기능입니다. 이는 검색 결과의 품질을 향상하는 데 유리합니다.

`Laravel\Ai\Reranking` 클래스를 사용해 문서를 재정렬할 수 있습니다:

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
$response->first()->index;    // 1 (원래 위치)
```

`limit` 메서드로 반환 결과 개수를 제한할 수 있습니다:

```php
$response = Reranking::of($documents)
    ->limit(5)
    ->rerank('search query');
```

<a name="reranking-collections"></a>
### 컬렉션 재정렬 (Reranking Collections)

Laravel 컬렉션에 내장된 `rerank` 매크로로도 재정렬을 간편하게 할 수 있습니다. 첫 번째 인자는 기준 필드(혹은 여러 필드), 두 번째는 쿼리입니다:

```php
// 단일 컬럼 기준으로 재정렬
$posts = Post::all()
    ->rerank('body', 'Laravel tutorials');

// 복수 필드 기준(자동 JSON 변환 후 전송)
$reranked = $posts->rerank(['title', 'body'], 'Laravel tutorials');

// 클로저로 문서 조합
$reranked = $posts->rerank(
    fn ($post) => $post->title.': '.$post->body,
    'Laravel tutorials'
);
```

결과 개수 제한, 공급자 지정 등도 가능합니다:

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

`Laravel\Ai\Files` 클래스 혹은 개별 파일 클래스를 사용해, AI 공급자에 파일을 업로드하여 대화에서 반복 활용할 수 있습니다. 대용량 문서나 여러 차례 참조가 필요한 파일에 유리합니다:

```php
use Laravel\Ai\Files\Document;
use Laravel\Ai\Files\Image;

// 로컬 경로에서 파일 저장
$response = Document::fromPath('/home/laravel/document.pdf')->put();
$response = Image::fromPath('/home/laravel/photo.jpg')->put();

// 파일시스템 디스크에 저장된 파일 저장
$response = Document::fromStorage('document.pdf', disk: 'local')->put();
$response = Image::fromStorage('photo.jpg', disk: 'local')->put();

// 원격 URL에서 파일 저장
$response = Document::fromUrl('https://example.com/document.pdf')->put();
$response = Image::fromUrl('https://example.com/photo.jpg')->put();

return $response->id;
```

원시 데이터나 업로드된 파일 저장도 지원합니다:

```php
use Laravel\Ai\Files;
use Laravel\Ai\Files\Document;

// 원시 데이터 저장
$stored = Document::fromString('Hello, World!', 'text/plain')->put();

// 업로드 파일 저장
$stored = Document::fromUpload($request->file('document'))->put();
```

저장한 파일은 에이전트 프롬프트 입력 시 재업로드 없이 파일 ID로 참조할 수 있습니다:

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

저장한 파일을 불러오려면, 파일 인스턴스의 `get` 메서드를 사용하세요:

```php
use Laravel\Ai\Files\Document;

$file = Document::fromId('file-id')->get();

$file->id;
$file->mimeType();
```

파일 삭제는 `delete` 메서드를 활용합니다:

```php
Document::fromId('file-id')->delete();
```

`Files` 클래스는 기본적으로 `config/ai.php`에서 지정한 기본 AI 공급자를 사용합니다. 대부분의 작업에서는 `provider` 인자를 통해 공급자를 바꿀 수 있습니다:

```php
$response = Document::fromPath(
    '/home/laravel/document.pdf'
)->put(provider: 'anthropic');
```

<a name="using-stored-files-in-conversations"></a>
### 저장 파일을 대화에 사용하기

공급자에 저장된 파일은 `Document`나 `Image` 클래스의 `fromId` 메서드로 에이전트 대화에서 참조할 수 있습니다:

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

이미지도 마찬가지로 사용 가능합니다:

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

벡터 스토어는 검색 가능한 파일 모음을 생성하여, RAG(검색 증강 생성) 등에 활용할 수 있습니다. `Laravel\Ai\Stores` 클래스에서 벡터 스토어의 생성/조회/삭제를 지원합니다:

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

기존 벡터 스토어 조회는 `get` 메서드를 사용합니다:

```php
use Laravel\Ai\Stores;

$store = Stores::get('store_id');

$store->id;
$store->name;
$store->fileCounts;
$store->ready;
```

벡터 스토어 삭제는 클래스 메서드 또는 인스턴스 메서드로 할 수 있습니다:

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

벡터 스토어를 만들었으면, `add` 메서드로 [파일](#files)을 추가할 수 있습니다. 스토어에 추가된 파일은 [파일 검색 공급자 툴](#file-search)로 자동 인덱싱되어 의미 기반 검색이 가능합니다:

```php
use Laravel\Ai\Files\Document;
use Laravel\Ai\Stores;

$store = Stores::get('store_id');

// 이미 공급자에 저장된 파일 추가
$document = $store->add('file_id');
$document = $store->add(Document::fromId('file_id'));

// 또는 파일 저장과 추가를 동시에
$document = $store->add(Document::fromPath('/path/to/document.pdf'));
$document = $store->add(Document::fromStorage('manual.pdf'));
$document = $store->add($request->file('document'));

$document->id;
$document->fileId;
```

> **Note:** 기존에 저장한 파일을 벡터 스토어에 추가하면, 반환된 document ID가 기존 file ID와 동일한 것이 일반적입니다. 하지만 일부 벡터 저장 공급자는 새로운 "문서 ID"를 반환할 수 있으니, 두 값 모두 데이터베이스에 저장해두는 것이 안전합니다.

파일을 스토어에 추가할 때 메타데이터를 첨부할 수 있으며, 추후 [파일 검색 공급자 툴](#file-search)에서 검색 필터로 사용할 수 있습니다:

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

벡터 스토어에서 파일을 삭제해도 공급자의 [파일 스토리지](#files)에서는 삭제되지 않습니다. 두 곳 모두에서 완전 삭제하려면 `deleteFile` 인자를 사용하세요:

```php
$store->remove('file_abc123', deleteFile: true);
```

<a name="failover"></a>
## 장애 조치(Failover) (Failover)

프롬프트 입력이나 이미지 생성 등 미디어 생성 시, 공급자 또는 모델의 배열을 제공하면, 주 공급자가 장애나 레이트리밋(제한)에 걸릴 경우 자동으로 백업 공급자/모델로 장애 조치합니다:

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

테스트 환경에서 에이전트의 응답을 가짜로 처리하려면, 에이전트 클래스에서 `fake` 메서드를 호출하세요. 응답 배열이나 클로저를 제공할 수 있습니다:

```php
use App\Ai\Agents\SalesCoach;
use Laravel\Ai\Prompts\AgentPrompt;

// 모든 프롬프트에 고정 응답 반환
SalesCoach::fake();

// 프롬프트별 응답 리스트 제공
SalesCoach::fake([
    'First response',
    'Second response',
]);

// 프롬프트 내용에 따라 동적으로 응답
SalesCoach::fake(function (AgentPrompt $prompt) {
    return 'Response for: '.$prompt->prompt;
});
```

> **Note:** 구조화된 출력을 반환하는 에이전트에서 `Agent::fake()`를 호출하면, 정의된 출력 스키마에 맞는 가짜 데이터가 자동 생성됩니다.

프롬프트 후, 입력된 프롬프트에 대한 다양한 검증(assertion)이 가능합니다:

```php
use Laravel\Ai\Prompts\AgentPrompt;

SalesCoach::assertPrompted('Analyze this...');

SalesCoach::assertPrompted(function (AgentPrompt $prompt) {
    return $prompt->contains('Analyze');
});

SalesCoach::assertNotPrompted('Missing prompt');

SalesCoach::assertNeverPrompted();
```

큐잉된 에이전트 작업에 대해서는 별도의 검증 메서드를 사용하세요:

```php
use Laravel\Ai\QueuedAgentPrompt;

SalesCoach::assertQueued('Analyze this...');

SalesCoach::assertQueued(function (QueuedAgentPrompt $prompt) {
    return $prompt->contains('Analyze');
});

SalesCoach::assertNotQueued('Missing prompt');

SalesCoach::assertNeverQueued();
```

모든 에이전트 호출이 가짜 응답과 매칭되는지 보장하려면 `preventStrayPrompts`를 사용하세요. 가짜 응답이 없는 호출 시 예외가 발생합니다:

```php
SalesCoach::fake()->preventStrayPrompts();
```

<a name="testing-images"></a>
### 이미지 (Images)

`Image` 클래스의 `fake` 메서드로 이미지 생성을 가짜로 처리할 수 있습니다. 이후 다양한 검증을 진행할 수 있습니다:

```php
use Laravel\Ai\Image;
use Laravel\Ai\Prompts\ImagePrompt;
use Laravel\Ai\Prompts\QueuedImagePrompt;

// 모든 프롬프트에 고정 응답 반환
Image::fake();

// 프롬프트별 응답 리스트 제공
Image::fake([
    base64_encode($firstImage),
    base64_encode($secondImage),
]);

// 프롬프트 내용에 따라 동적으로 응답
Image::fake(function (ImagePrompt $prompt) {
    return base64_encode('...');
});
```

이미지 생성을 검증할 수 있습니다:

```php
Image::assertGenerated(function (ImagePrompt $prompt) {
    return $prompt->contains('sunset') && $prompt->isLandscape();
});

Image::assertNotGenerated('Missing prompt');

Image::assertNothingGenerated();
```

큐잉 이미지 생성 검증은 다음과 같이 합니다:

```php
Image::assertQueued(
    fn (QueuedImagePrompt $prompt) => $prompt->contains('sunset')
);

Image::assertNotQueued('Missing prompt');

Image::assertNothingQueued();
```

모든 이미지 생성이 가짜 응답과 매칭되는지 보장하려면 `preventStrayImages`를 사용하세요. 미정의 응답 발생 시 예외가 발생합니다:

```php
Image::fake()->preventStrayImages();
```

<a name="testing-audio"></a>
### 오디오 (Audio)

`Audio` 클래스의 `fake` 메서드를 통해 오디오 생성을 가짜로 처리할 수 있습니다. 이후 생성 프롬프트 등에 대해 검증할 수 있습니다:

```php
use Laravel\Ai\Audio;
use Laravel\Ai\Prompts\AudioPrompt;
use Laravel\Ai\Prompts\QueuedAudioPrompt;

// 모든 프롬프트에 고정 응답 반환
Audio::fake();

// 응답 배열 제공
Audio::fake([
    base64_encode($firstAudio),
    base64_encode($secondAudio),
]);

// 프롬프트 내용에 따라 동적 응답
Audio::fake(function (AudioPrompt $prompt) {
    return base64_encode('...');
});
```

오디오 생성 검증:

```php
Audio::assertGenerated(function (AudioPrompt $prompt) {
    return $prompt->contains('Hello') && $prompt->isFemale();
});

Audio::assertNotGenerated('Missing prompt');

Audio::assertNothingGenerated();
```

큐잉 오디오 생성 검증:

```php
Audio::assertQueued(
    fn (QueuedAudioPrompt $prompt) => $prompt->contains('Hello')
);

Audio::assertNotQueued('Missing prompt');

Audio::assertNothingQueued();
```

가짜 응답 없이 오디오가 생성되지 않도록 하려면:

```php
Audio::fake()->preventStrayAudio();
```

<a name="testing-transcriptions"></a>
### 트랜스크립션 (Transcriptions)

`Transcription` 클래스의 `fake` 메서드로 트랜스크립션 생성을 가짜로 처리할 수 있습니다:

```php
use Laravel\Ai\Transcription;
use Laravel\Ai\Prompts\TranscriptionPrompt;
use Laravel\Ai\Prompts\QueuedTranscriptionPrompt;

// 모든 프롬프트에 고정 응답 반환
Transcription::fake();

// 응답 배열 제공
Transcription::fake([
    'First transcription text.',
    'Second transcription text.',
]);

// 프롬프트 내용에 따라 동적 응답
Transcription::fake(function (TranscriptionPrompt $prompt) {
    return 'Transcribed text...';
});
```

생성된 트랜스크립션에 대한 검증:

```php
Transcription::assertGenerated(function (TranscriptionPrompt $prompt) {
    return $prompt->language === 'en' && $prompt->isDiarized();
});

Transcription::assertNotGenerated(
    fn (TranscriptionPrompt $prompt) => $prompt->language === 'fr'
);

Transcription::assertNothingGenerated();
```

큐잉 트랜스크립션 생성 검증:

```php
Transcription::assertQueued(
    fn (QueuedTranscriptionPrompt $prompt) => $prompt->isDiarized()
);

Transcription::assertNotQueued(
    fn (QueuedTranscriptionPrompt $prompt) => $prompt->language === 'fr'
);

Transcription::assertNothingQueued();
```

가짜 응답 없이 트랜스크립션이 생성되지 않도록 하려면:

```php
Transcription::fake()->preventStrayTranscriptions();
```

<a name="testing-embeddings"></a>
### 임베딩 (Embeddings)

`Embeddings` 클래스의 `fake` 메서드로 임베딩 생성을 가짜로 처리할 수 있습니다:

```php
use Laravel\Ai\Embeddings;
use Laravel\Ai\Prompts\EmbeddingsPrompt;
use Laravel\Ai\Prompts\QueuedEmbeddingsPrompt;

// 지정된 차원의 임베딩을 자동으로 생성
Embeddings::fake();

// 응답 배열 제공
Embeddings::fake([
    [$firstEmbeddingVector],
    [$secondEmbeddingVector],
]);

// 프롬프트 내용에 따라 동적 응답
Embeddings::fake(function (EmbeddingsPrompt $prompt) {
    return array_map(
        fn () => Embeddings::fakeEmbedding($prompt->dimensions),
        $prompt->inputs
    );
});
```

생성된 임베딩에 대한 검증:

```php
Embeddings::assertGenerated(function (EmbeddingsPrompt $prompt) {
    return $prompt->contains('Laravel') && $prompt->dimensions === 1536;
});

Embeddings::assertNotGenerated(
    fn (EmbeddingsPrompt $prompt) => $prompt->contains('Other')
);

Embeddings::assertNothingGenerated();
```

큐잉 임베딩 생성 검증:

```php
Embeddings::assertQueued(
    fn (QueuedEmbeddingsPrompt $prompt) => $prompt->contains('Laravel')
);

Embeddings::assertNotQueued(
    fn (QueuedEmbeddingsPrompt $prompt) => $prompt->contains('Other')
);

Embeddings::assertNothingQueued();
```

가짜 응답 없이 임베딩이 생성되지 않도록 하려면:

```php
Embeddings::fake()->preventStrayEmbeddings();
```

<a name="testing-reranking"></a>
### 재정렬 (Reranking)

`Reranking` 클래스의 `fake` 메서드로 재정렬 작업을 가짜 처리할 수 있습니다:

```php
use Laravel\Ai\Reranking;
use Laravel\Ai\Prompts\RerankingPrompt;
use Laravel\Ai\Responses\Data\RankedDocument;

// 자동으로 가짜 결과 생성
Reranking::fake();

// 커스텀 응답 제공
Reranking::fake([
    [
        new RankedDocument(index: 0, document: 'First', score: 0.95),
        new RankedDocument(index: 1, document: 'Second', score: 0.80),
    ],
]);
```

재정렬 작업에 대한 검증:

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

`Files` 클래스의 `fake` 메서드로 파일 작업을 가짜 처리할 수 있습니다:

```php
use Laravel\Ai\Files;

Files::fake();
```

파일 업로드/삭제 등에 대한 검증:

```php
use Laravel\Ai\Contracts\Files\StorableFile;
use Laravel\Ai\Files\Document;

// 파일 저장
Document::fromString('Hello, Laravel!', mime: 'text/plain')
    ->as('hello.txt')
    ->put();

// 검증
Files::assertStored(fn (StorableFile $file) =>
    (string) $file === 'Hello, Laravel!' &&
        $file->mimeType() === 'text/plain'
);

Files::assertNotStored(fn (StorableFile $file) =>
    (string) $file === 'Hello, World!'
);

Files::assertNothingStored();
```

파일 삭제 검증:

```php
Files::assertDeleted('file-id');
Files::assertNotDeleted('file-id');
Files::assertNothingDeleted();
```

<a name="testing-vector-stores"></a>
### 벡터 스토어 (Vector Stores)

`Stores` 클래스의 `fake` 메서드로 벡터 스토어 작업을 가짜 처리할 수 있습니다. 벡터 스토어 작업을 가짜로 처리하면, [파일 작업](#files) 또한 자동으로 가짜 처리됩니다:

```php
use Laravel\Ai\Stores;

Stores::fake();
```

스토어 생성/삭제 등의 검증도 가능합니다:

```php
use Laravel\Ai\Stores;

// 스토어 생성
$store = Stores::create('Knowledge Base');

// 검증
Stores::assertCreated('Knowledge Base');

Stores::assertCreated(fn (string $name, ?string $description) =>
    $name === 'Knowledge Base'
);

Stores::assertNotCreated('Other Store');

Stores::assertNothingCreated();
```

스토어 삭제는 ID로 검증합니다:

```php
Stores::assertDeleted('store_id');
Stores::assertNotDeleted('other_store_id');
Stores::assertNothingDeleted();
```

특정 스토어 인스턴스에서 파일 추가/제거 검증:

```php
Stores::fake();

$store = Stores::get('store_id');

// 파일 추가/제거
$store->add('added_id');
$store->remove('removed_id');

// 검증
$store->assertAdded('added_id');
$store->assertRemoved('removed_id');

$store->assertNotAdded('other_file_id');
$store->assertNotRemoved('other_file_id');
```

파일이 [파일 스토리지](#files)에 저장된 뒤 바로 벡터 스토어에 추가된다면, 파일 ID를 정확히 모를 수 있습니다. 이 경우, `assertAdded` 메서드에 클로저를 전달해 저장된 파일 내용을 기준으로 검증할 수 있습니다:

```php
use Laravel\Ai\Contracts\Files\StorableFile;
use Laravel\Ai\Files\Document;

$store->add(Document::fromString('Hello, World!', 'text/plain')->as('hello.txt'));

$store->assertAdded(fn (StorableFile $file) => $file->name() === 'hello.txt');
$store->assertAdded(fn (StorableFile $file) => $file->content() === 'Hello, World!');
```

<a name="events"></a>
## 이벤트 (Events)

Laravel AI SDK는 다양한 [이벤트](/docs/12.x/events)를 발생시킵니다. 이벤트는 다음과 같습니다:

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

이 이벤트를 리스닝하여 AI SDK 사용 정보를 로그에 남기거나 저장하는 등의 작업을 할 수 있습니다.
