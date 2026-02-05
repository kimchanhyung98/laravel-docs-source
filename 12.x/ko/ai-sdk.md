# Laravel AI SDK (Laravel AI SDK)

- [소개](#introduction)
- [설치](#installation)
    - [설정](#configuration)
    - [지원 제공자](#provider-support)
- [에이전트](#agents)
    - [프롬프트 입력](#prompting)
    - [대화 컨텍스트](#conversation-context)
    - [구조화된 출력](#structured-output)
    - [첨부파일](#attachments)
    - [스트리밍](#streaming)
    - [브로드캐스팅](#broadcasting)
    - [큐잉](#queueing)
    - [툴](#tools)
    - [제공자 도구](#provider-tools)
    - [미들웨어](#middleware)
    - [익명 에이전트](#anonymous-agents)
    - [에이전트 설정](#agent-configuration)
- [이미지](#images)
- [오디오 (TTS)](#audio)
- [트랜스크립션 (STT)](#transcription)
- [임베딩](#embeddings)
    - [임베딩 조회](#querying-embeddings)
    - [임베딩 캐싱](#caching-embeddings)
- [리랭킹](#reranking)
- [파일](#files)
- [벡터 스토어](#vector-stores)
    - [스토어에 파일 추가](#adding-files-to-stores)
- [장애 조치](#failover)
- [테스트](#testing)
    - [에이전트](#testing-agents)
    - [이미지](#testing-images)
    - [오디오](#testing-audio)
    - [트랜스크립션](#testing-transcriptions)
    - [임베딩](#testing-embeddings)
    - [리랭킹](#testing-reranking)
    - [파일](#testing-files)
    - [벡터스토어](#testing-vector-stores)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel AI SDK](https://github.com/laravel/ai)는 OpenAI, Anthropic, Gemini 등 다양한 AI 제공자와 상호작용할 수 있는 통합적이고 표현력 있는 API를 제공합니다. AI SDK를 사용하면 도구 및 구조화된 출력을 지원하는 지능형 에이전트 생성, 이미지 생성, 오디오 합성 및 트랜스크립션, 벡터 임베딩 생성 등 다양한 기능을 Laravel다운 일관된 인터페이스로 사용할 수 있습니다.

<a name="installation"></a>
## 설치 (Installation)

Composer를 통해 Laravel AI SDK를 설치할 수 있습니다:

```shell
composer require laravel/ai
```

다음으로, `vendor:publish` Artisan 명령어를 사용해 AI SDK의 설정과 마이그레이션 파일을 퍼블리시해야 합니다:

```shell
php artisan vendor:publish --provider="Laravel\Ai\AiServiceProvider"
```

마지막으로 애플리케이션의 데이터베이스 마이그레이션을 실행해야 합니다. 이를 통해 AI SDK가 대화 내용 저장에 사용하는 `agent_conversations`와 `agent_conversation_messages` 테이블이 생성됩니다:

```shell
php artisan migrate
```

<a name="configuration"></a>
### 설정 (Configuration)

애플리케이션의 `config/ai.php` 설정 파일 또는 `.env` 환경 변수 파일에 AI 제공자의 인증 정보를 입력할 수 있습니다:

```ini
ANTHROPIC_API_KEY=
COHERE_API_KEY=
ELEVENLABS_API_KEY=
GEMINI_API_KEY=
OPENAI_API_KEY=
JINA_API_KEY=
XAI_API_KEY=
```

텍스트, 이미지, 오디오, 트랜스크립션, 임베딩에 사용되는 기본 모델 역시 애플리케이션의 `config/ai.php` 파일에서 설정할 수 있습니다.

<a name="provider-support"></a>
### 지원 제공자 (Provider Support)

AI SDK는 각 기능별로 다양한 제공자를 지원합니다. 아래 표는 기능별 지원 제공자를 요약한 것입니다:

| 기능 | 지원 제공자 |
|---|---|
| 텍스트 | OpenAI, Anthropic, Gemini, Groq, xAI |
| 이미지 | OpenAI, Gemini, xAI |
| TTS | OpenAI, ElevenLabs |
| STT | OpenAI, ElevenLabs |
| 임베딩 | OpenAI, Gemini, Cohere, Jina |
| 리랭킹 | Cohere, Jina |
| 파일 | OpenAI, Anthropic, Gemini |

<a name="agents"></a>
## 에이전트 (Agents)

에이전트는 Laravel AI SDK에서 AI 제공자와 상호작용할 때 기본이 되는 구성 요소입니다. 각 에이전트는 명령어, 대화 컨텍스트, 도구, 출력 스키마를 모두 하나의 PHP 클래스로 감싸 대형 언어 모델과의 상호작용에 필요한 설정을 관리합니다. 에이전트는 일종의 특화된 조력자(예: 영업 코치, 문서 분석기, 고객 지원 봇 등)로, 한 번 설정한 뒤 애플리케이션 전체에서 프롬프트 할 수 있습니다.

`make:agent` Artisan 명령어로 에이전트를 생성할 수 있습니다:

```shell
php artisan make:agent SalesCoach

php artisan make:agent SalesCoach --structured
```

생성된 에이전트 클래스에서 시스템 프롬프트/명령어, 메시지 컨텍스트, 도구, 출력 스키마(해당 시)를 정의할 수 있습니다:

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
     * 에이전트가 따라야 할 명령어를 반환합니다.
     */
    public function instructions(): Stringable|string
    {
        return 'You are a sales coach, analyzing transcripts and providing feedback and an overall sales strength score .';
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

에이전트에 프롬프트를 입력하려면 먼저 `make` 메서드나 일반적인 인스턴스 생성을 통해 객체를 만든 뒤, `prompt`를 호출합니다:

```php
$response = (new SalesCoach)
    ->prompt('Analyze this sales transcript...');

$response = SalesCoach::make()
    ->prompt('Analyze this sales transcript...');

return (string) $response;
```

`make` 메서드는 의존성 주입을 활용해 에이전트를 컨테이너에서 자동으로 해석합니다. 또한 생성자 인수도 전달할 수 있습니다:

```php
$agent = SalesCoach::make(user: $user);
```

프롬프트 입력 시 추가 인수를 넘기면, 기본 제공자나 모델, HTTP 타임아웃을 즉시 오버라이드할 수 있습니다:

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

에이전트가 `Conversational` 인터페이스를 구현하고 있다면, `messages` 메서드를 이용해 이전 대화 컨텍스트를 반환할 수 있습니다:

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
#### 대화 내용 저장 (Remembering Conversations)

> **Note:** `RemembersConversations` 트레이트를 사용하기 전에, `vendor:publish` Artisan 명령어로 AI SDK 마이그레이션을 퍼블리시 및 실행해야 합니다. 해당 마이그레이션은 대화 내용을 저장할 데이터베이스 테이블을 생성합니다.

Laravel이 에이전트의 대화 이력을 자동으로 저장 및 불러오도록 하려면, `RemembersConversations` 트레이트를 사용할 수 있습니다. 이 트레이트를 사용하면 `Conversational` 인터페이스를 직접 구현할 필요 없이, 대화 메시지가 데이터베이스에 간단하게 저장됩니다:

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

사용자별로 새로운 대화를 시작하려면, 프롬프트 입력 전에 `forUser` 메서드를 호출하십시오:

```php
$response = (new SalesCoach)->forUser($user)->prompt('Hello!');

$conversationId = $response->conversationId;
```

대화 ID는 응답 객체에 반환되므로, 이후 참조를 위해 저장하거나, `agent_conversations` 테이블에서 직접 모든 사용자의 대화를 조회할 수 있습니다.

기존 대화 이어서 진행 시에는 `continue` 메서드를 사용하세요:

```php
$response = (new SalesCoach)
    ->continue($conversationId, as: $user)
    ->prompt('Tell me more about that.');
```

`RemembersConversations` 트레이트를 사용하면 이전 메시지가 자동으로 대화 컨텍스트에 포함되어 프롬프트 시 전달되며, 새 메시지(사용자/도우미 모두)는 매 상호작용 후 자동으로 저장됩니다.

<a name="structured-output"></a>
### 구조화된 출력 (Structured Output)

에이전트가 구조화된 출력을 반환하도록 하려면, `HasStructuredOutput` 인터페이스를 구현해 `schema` 메서드를 정의해야 합니다:

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

구조화된 출력을 반환하는 에이전트에 프롬프트를 입력하면, 반환된 `StructuredAgentResponse`를 배열처럼 접근할 수 있습니다:

```php
$response = (new SalesCoach)->prompt('Analyze this sales transcript...');

return $response['score'];
```

<a name="attachments"></a>
### 첨부파일 (Attachments)

프롬프트를 입력할 때 이미지나 문서 등 첨부파일을 함께 전달할 수도 있습니다. 이를 통해 모델이 해당 파일까지 참고할 수 있습니다:

```php
use App\Ai\Agents\SalesCoach;
use Laravel\Ai\Files;

$response = (new SalesCoach)->prompt(
    'Analyze the attached sales transcript...',
    attachments: [
        Files\Document::fromStorage('transcript.pdf'), // 파일시스템에 있는 문서 첨부
        Files\Document::fromPath('/home/laravel/transcript.md'), // 로컬 경로에서 문서 첨부
        $request->file('transcript'), // 업로드된 파일 첨부
    ]
);
```

`Laravel\Ai\Files\Image` 클래스를 사용하면 이미지도 첨부할 수 있습니다:

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
### 스트리밍 (Streaming)

에이전트의 응답을 실시간 스트리밍하려면 `stream` 메서드를 사용하세요. 반환된 `StreamableAgentResponse`는 라우트에서 리턴하면 클라이언트로 스트리밍 응답(SSE)이 자동 전송됩니다:

```php
use App\Ai\Agents\SalesCoach;

Route::get('/coach', function () {
    return (new SalesCoach)->stream('Analyze this sales transcript...');
});
```

`then` 메서드를 이용하면 스트리밍 전체가 완료된 후 실행될 콜백을 등록할 수 있습니다:

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

스트리밍 이벤트를 직접 반복(iterate)하며 처리할 수도 있습니다:

```php
$stream = (new SalesCoach)->stream('Analyze this sales transcript...');

foreach ($stream as $event) {
    // ...
}
```

<a name="streaming-using-the-vercel-ai-sdk-protocol"></a>
#### Vercel AI SDK 프로토콜로 스트리밍하기

[Vercel AI SDK 스트림 프로토콜](https://ai-sdk.dev/docs/ai-sdk-ui/stream-protocol)을 사용할 경우, 스트림 응답의 `usingVercelDataProtocol` 메서드를 호출하면 됩니다:

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

스트리밍 이벤트는 여러 방법으로 브로드캐스트할 수 있습니다. 먼저, 스트리밍된 각 이벤트의 `broadcast` 또는 `broadcastNow` 메서드를 호출할 수 있습니다:

```php
use App\Ai\Agents\SalesCoach;
use Illuminate\Broadcasting\Channel;

$stream = (new SalesCoach)->stream('Analyze this sales transcript...');

foreach ($stream as $event) {
    $event->broadcast(new Channel('channel-name'));
}
```

또는 에이전트의 `broadcastOnQueue` 메서드를 사용해 에이전트 작업을 큐에 넣고, 가능한 즉시 스트리밍 이벤트를 브로드캐스팅할 수 있습니다:

```php
(new SalesCoach)->broadcastOnQueue(
    'Analyze this sales transcript...',
    new Channel('channel-name'),
);
```

<a name="queueing"></a>
### 큐잉 (Queueing)

에이전트의 `queue` 메서드를 사용하면, 프롬프트를 백그라운드에서 처리해 애플리케이션의 빠른 응답성을 유지할 수 있습니다. 응답이 준비되었을 때 혹은 예외가 발생했을 때 실행될 콜백은 각각 `then`, `catch` 메서드로 등록합니다:

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

툴을 사용하면 에이전트가 프롬프트에 응답하는 동안 추가적인 기능을 활용할 수 있게 할 수 있습니다. 툴은 `make:tool` Artisan 명령어로 생성할 수 있습니다:

```shell
php artisan make:tool RandomNumberGenerator
```

생성된 툴 파일은 `app/Ai/Tools` 디렉터리에 위치합니다. 각 툴은 `handle` 메서드를 가지고 있으며, 에이전트가 해당 기능을 사용할 필요가 있을 때 호출됩니다:

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
     * 툴의 목적을 설명하는 설명문을 반환합니다.
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

정의한 툴을 에이전트의 `tools` 메서드에서 반환하면 사용할 수 있습니다:

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

`SimilaritySearch` 툴을 통해 에이전트가 데이터베이스에 저장된 벡터 임베딩을 사용해 쿼리와 유사한 문서를 검색할 수 있습니다. 이는 RAG(Retrieval Augmented Generation) 등, 에이전트가 애플리케이션의 데이터를 검색해 활용하는 데 유용합니다.

가장 간단하게는, 벡터 임베딩을 가진 Eloquent 모델과 함께 `usingModel` 메서드를 사용하여 생성할 수 있습니다:

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

첫 번째 인수는 Eloquent 모델 클래스, 두 번째는 벡터 임베딩 컬럼명입니다.

최소 유사도 기준(0.0~1.0)과 쿼리 커스터마이즈를 위한 클로저도 전달할 수 있습니다:

```php
SimilaritySearch::usingModel(
    model: Document::class,
    column: 'embedding',
    minSimilarity: 0.7,
    limit: 10,
    query: fn ($query) => $query->where('published', true),
),
```

더 세밀하게 제어하려면, 결과를 반환하는 커스텀 클로저로 툴을 생성합니다:

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

툴의 설명문은 `withDescription` 메서드로 커스터마이즈 할 수 있습니다:

```php
SimilaritySearch::usingModel(Document::class, 'embedding')
    ->withDescription('Search the knowledge base for relevant articles.'),
```

<a name="provider-tools"></a>
### 제공자 도구 (Provider Tools)

제공자 도구는 웹 검색, URL 읽기, 파일 검색 등, AI 제공자가 네이티브하게 제공하는 특수 기능으로, 일반 툴과 달리 해당 기능이 AI 제공자 쪽에서 실행됩니다.

제공자 도구도 에이전트의 `tools` 메서드에서 반환하면 사용할 수 있습니다.

<a name="web-search"></a>
#### 웹 검색 (Web Search)

`WebSearch` 제공자 도구는 에이전트가 실시간 정보에 접근해 웹을 검색할 수 있게 해줍니다. 최근 데이터나 시의성 있는 정보가 필요할 때 유용합니다.

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

검색 횟수 제한, 특정 도메인으로 제한 등 옵션도 설정할 수 있습니다:

```php
(new WebSearch)->max(5)->allow(['laravel.com', 'php.net']),
```

사용자 위치에 따라 검색 결과를 좁히고 싶다면 `location` 메서드를 사용하세요:

```php
(new WebSearch)->location(
    city: 'New York',
    region: 'NY',
    country: 'US'
);
```

<a name="web-fetch"></a>
#### 웹 읽기 (Web Fetch)

`WebFetch` 제공자 도구를 사용하면 에이전트가 웹 페이지의 내용을 가져와 분석할 수 있습니다. 특정 URL의 상세 분석이나 정보 가져오기에 유용합니다.

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

검색 횟수 제한, 허용 도메인 제한 등도 설정할 수 있습니다:

```php
(new WebFetch)->max(3)->allow(['docs.laravel.com']),
```

<a name="file-search"></a>
#### 파일 검색 (File Search)

`FileSearch` 제공자 도구는 [벡터 스토어](#vector-stores)에 저장된 [파일](#files) 내에서 검색할 수 있도록 해줍니다. 이를 통해 에이전트가 업로드된 문서에서 정보 검색(RAG 등)을 할 수 있습니다.

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

여러 벡터스토어 ID를 전달해 여러 스토어에서 한 번에 검색할 수 있습니다:

```php
new FileSearch(stores: ['store_1', 'store_2']);
```

파일에 [메타데이터](#adding-files-to-stores)가 있다면, 검색 결과를 필터링할 수 있습니다. 간단한 동등 비교는 배열로 전달합니다:

```php
new FileSearch(stores: ['store_id'], where: [
    'author' => 'Taylor Otwell',
    'year' => 2026,
]);
```

더 복잡한 필터는 `FileSearchQuery` 인스턴스를 받는 클로저로 전달합니다:

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

에이전트는 미들웨어를 지원해, 프롬프트가 AI 제공자에게 전달되기 전에 가로채거나 수정할 수 있습니다. 미들웨어를 추가하려면 `HasMiddleware` 인터페이스를 구현하고, 미들웨어 클래스의 배열을 반환하는 `middleware` 메서드를 정의하세요:

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

각 미들웨어 클래스는 `AgentPrompt`와 다음 미들웨어를 호출하는 `Closure`를 인자로 받는 `handle` 메서드를 정의해야 합니다:

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

응답 처리 후 코드를 실행하려면, 응답의 `then` 메서드를 사용할 수 있습니다(동기/스트리밍 모두 지원):

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

별도의 에이전트 클래스를 만들지 않고, 빠르게 모델과 상호작용하고 싶다면 `agent` 함수를 사용해 임시(익명) 에이전트를 만들 수 있습니다:

```php
use function Laravel\Ai\{agent};

$response = agent(
    instructions: 'You are an expert at software development.',
    messages: [],
    tools: [],
)->prompt('Tell me about Laravel')
```

익명 에이전트 역시 구조화된 출력을 지원합니다:

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

에이전트의 텍스트 생성 옵션은 PHP 속성(Attribute)으로 구성할 수 있습니다. 사용 가능한 속성은 다음과 같습니다:

- `MaxSteps`: 에이전트가 도구 사용시 허용되는 최대 단계 수
- `MaxTokens`: 모델이 생성할 최대 토큰 수
- `Provider`: 에이전트가 사용할 AI 제공자(장애 조치 시 복수 지정 가능)
- `Temperature`: 생성시 사용할 샘플링 온도(0.0~1.0)
- `Timeout`: 에이전트 요청의 HTTP 타임아웃(초, 기본 60)
- `UseCheapestModel`: 비용 최적화를 위해 제공자의 가장 저렴한 텍스트 모델 사용
- `UseSmartestModel`: 복잡한 작업을 위해 제공자의 가장 강력한 텍스트 모델 사용

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

`UseCheapestModel`과 `UseSmartestModel` 속성을 통해 모델명을 명시하지 않아도, 각 제공자에서 가장 저렴하거나 가장 우수한 모델을 자동으로 선택할 수 있습니다. 비용이나 성능 최적화가 필요할 때 유용합니다:

```php
use Laravel\Ai\Attributes\UseCheapestModel;
use Laravel\Ai\Attributes\UseSmartestModel;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Promptable;

#[UseCheapestModel]
class SimpleSummarizer implements Agent
{
    use Promptable;

    // 가장 저렴한 모델(예: Haiku)을 사용합니다
}

#[UseSmartestModel]
class ComplexReasoner implements Agent
{
    use Promptable;

    // 가장 강력한 모델(예: Opus)을 사용합니다
}
```

<a name="images"></a>
## 이미지 (Images)

`Laravel\Ai\Image` 클래스를 사용하면 `openai`, `gemini`, `xai` 제공자를 통해 이미지를 생성할 수 있습니다:

```php
use Laravel\Ai\Image;

$image = Image::of('A donut sitting on the kitchen counter')->generate();

$rawContent = (string) $image;
```

`square`, `portrait`, `landscape` 메서드로 이미지의 종횡비를, `quality`로 품질(`high`, `medium`, `low`)을, `timeout`으로 HTTP 타임아웃(초)을 지정할 수 있습니다:

```php
use Laravel\Ai\Image;

$image = Image::of('A donut sitting on the kitchen counter')
    ->quality('high')
    ->landscape()
    ->timeout(120)
    ->generate();
```

참조 이미지는 `attachments`로 추가할 수 있습니다:

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

생성한 이미지는 애플리케이션의 `config/filesystems.php`에서 지정한 기본 디스크로 쉽게 저장할 수 있습니다:

```php
$image = Image::of('A donut sitting on the kitchen counter');

$path = $image->store();
$path = $image->storeAs('image.jpg');
$path = $image->storePublicly();
$path = $image->storePubliclyAs('image.jpg');
```

이미지 생성도 큐로 처리할 수 있습니다:

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

`Laravel\Ai\Audio` 클래스를 통해 주어진 텍스트를 오디오로 변환할 수 있습니다:

```php
use Laravel\Ai\Audio;

$audio = Audio::of('I love coding with Laravel.')->generate();

$rawContent = (string) $audio;
```

`male`, `female`, `voice` 메서드로 목소리 종류를, `instructions`로 음성의 톤이나 연출법을 지정할 수 있습니다:

```php
$audio = Audio::of('I love coding with Laravel.')
    ->female()
    ->generate();

$audio = Audio::of('I love coding with Laravel.')
    ->voice('voice-id-or-name')
    ->generate();
```

음성 스타일을 조정할 수도 있습니다:

```php
$audio = Audio::of('I love coding with Laravel.')
    ->female()
    ->instructions('Said like a pirate')
    ->generate();
```

생성된 오디오는 파일시스템의 기본 디스크에 저장할 수 있습니다:

```php
$audio = Audio::of('I love coding with Laravel.')->generate();

$path = $audio->store();
$path = $audio->storeAs('audio.mp3');
$path = $audio->storePublicly();
$path = $audio->storePubliclyAs('audio.mp3');
```

오디오 생성도 큐잉할 수 있습니다:

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

`Laravel\Ai\Transcription` 클래스를 사용해 오디오 파일의 트랜스크립트를 생성할 수 있습니다:

```php
use Laravel\Ai\Transcription;

$transcript = Transcription::fromPath('/home/laravel/audio.mp3')->generate();
$transcript = Transcription::fromStorage('audio.mp3')->generate();
$transcript = Transcription::fromUpload($request->file('audio'))->generate();

return (string) $transcript;
```

`diarize` 메서드를 사용하면, 단순 텍스트 외에 화자 구분이 포함된 트랜스크립트도 요청할 수 있습니다:

```php
$transcript = Transcription::fromStorage('audio.mp3')
    ->diarize()
    ->generate();
```

트랜스크립션도 큐잉 처리할 수 있습니다:

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

Laravel의 `Stringable` 클래스에 새롭게 추가된 `toEmbeddings` 메서드로 손쉽게 문자열에 대한 벡터 임베딩을 생성할 수 있습니다:

```php
use Illuminate\Support\Str;

$embeddings = Str::of('Napa Valley has great wine.')->toEmbeddings();
```

또는 `Embeddings` 클래스를 사용해 여러 입력을 한 번에 임베딩 생성할 수 있습니다:

```php
use Laravel\Ai\Embeddings;

$response = Embeddings::for([
    'Napa Valley has great wine.',
    'Laravel is a PHP framework.',
])->generate();

$response->embeddings; // [[0.123, 0.456, ...], [0.789, 0.012, ...]]
```

임베딩의 차원이나 제공자도 직접 지정할 수 있습니다:

```php
$response = Embeddings::for(['Napa Valley has great wine.'])
    ->dimensions(1536)
    ->generate('openai', 'text-embedding-3-small');
```

<a name="querying-embeddings"></a>
### 임베딩 조회 (Querying Embeddings)

생성한 임베딩은 주로 데이터베이스의 `vector` 컬럼에 저장하고, 이후 벡터 쿼리에 사용합니다. Laravel은 PostgreSQL의 `pgvector` 확장을 통한 벡터 컬럼을 기본 지원하며, 마이그레이션에서 벡터 컬럼(차원도 지정)을 선언할 수 있습니다:

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

벡터 컬럼에 인덱스를 추가해 유사도 검색 성능을 높일 수도 있습니다. `index` 호출 시 코사인 거리 기반 HNSW 인덱스가 생성됩니다:

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

유사한 레코드를 조회하려면 `whereVectorSimilarTo` 메서드를 사용하세요. 이 메서드는 미니멈 코사인 유사도(0.0~1.0, 1.0은 완전 동일)로 필터링하고, 유사도 순으로 정렬합니다:

```php
use App\Models\Document;

$documents = Document::query()
    ->whereVectorSimilarTo('embedding', $queryEmbedding, minSimilarity: 0.4)
    ->limit(10)
    ->get();
```

`$queryEmbedding`은 float 배열 혹은 일반 문자열 모두 허용합니다. 문자열을 넘기면 Laravel이 자동으로 임베딩을 생성해줍니다:

```php
$documents = Document::query()
    ->whereVectorSimilarTo('embedding', 'best wineries in Napa Valley')
    ->limit(10)
    ->get();
```

더 낮은 수준의 제어가 필요하면 `whereVectorDistanceLessThan`, `selectVectorDistance`, `orderByVectorDistance` 메서드도 사용할 수 있습니다:

```php
$documents = Document::query()
    ->select('*')
    ->selectVectorDistance('embedding', $queryEmbedding, as: 'distance')
    ->whereVectorDistanceLessThan('embedding', $queryEmbedding, maxDistance: 0.3)
    ->orderByVectorDistance('embedding', $queryEmbedding)
    ->limit(10)
    ->get();
```

에이전트가 유사도 검색 도구를 사용할 수 있게 하려면, [유사도 검색 툴](#similarity-search)도 참고해보세요.

> [!NOTE]  
> 벡터 쿼리는 현재 PostgreSQL의 `pgvector` 확장을 사용하는 커넥션에서만 지원됩니다.

<a name="caching-embeddings"></a>
### 임베딩 캐싱 (Caching Embeddings)

동일한 입력에 대해 중복된 API 호출을 방지하려면, 임베딩 생성을 캐싱할 수 있습니다. 활성화하려면 `ai.caching.embeddings.cache` 설정을 `true`로 변경하세요:

```php
'caching' => [
    'embeddings' => [
        'cache' => true,
        'store' => env('CACHE_STORE', 'database'),
        // ...
    ],
],
```

캐싱을 활성화하면 임베딩 결과가 최대 30일간 캐시됩니다. 캐시 키는 제공자, 모델, 차원, 입력 내용에 따라 결정되어, 완전히 동일한 요청만 캐시된 결과를 공유합니다.

글로벌 캐싱이 비활성화된 경우라도, `cache` 메서드를 호출하면 해당 요청에만 임베딩 캐싱을 사용할 수 있습니다:

```php
$response = Embeddings::for(['Napa Valley has great wine.'])
    ->cache()
    ->generate();
```

캐시 시간(초 단위)도 직접 지정할 수 있습니다:

```php
$response = Embeddings::for(['Napa Valley has great wine.'])
    ->cache(seconds: 3600) // 1시간 캐시
    ->generate();
```

`toEmbeddings` 인스턴스 메서드 역시 `cache` 인자를 지원합니다:

```php
// 기본 기간으로 캐시
$embeddings = Str::of('Napa Valley has great wine.')->toEmbeddings(cache: true);

// 특정 기간으로 캐시
$embeddings = Str::of('Napa Valley has great wine.')->toEmbeddings(cache: 3600);
```

<a name="reranking"></a>
## 리랭킹 (Reranking)

리랭킹은 주어진 쿼리에 대해 여러 문서의 관련도에 따라 순위를 다시 매기는 기능입니다. 의미 기반으로 검색 결과를 개선하는 데 유용합니다.

`Laravel\Ai\Reranking` 클래스를 사용하면 문서 리랭킹을 할 수 있습니다:

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

`limit` 메서드를 사용해 반환되는 결과 개수를 제한할 수도 있습니다:

```php
$response = Reranking::of($documents)
    ->limit(5)
    ->rerank('search query');
```

<a name="reranking-collections"></a>
### 컬렉션 리랭킹 (Reranking Collections)

Laravel 컬렉션에서도 `rerank` 매크로로 리랭킹을 쉽게 수행할 수 있습니다. 첫 번째 인자는 리랭킹에 사용할 필드(들), 두 번째는 쿼리입니다:

```php
// 단일 필드로 리랭킹
$posts = Post::all()
    ->rerank('body', 'Laravel tutorials');

// 복수 필드(=JSON으로 묶음)로 리랭킹
$reranked = $posts->rerank(['title', 'body'], 'Laravel tutorials');

// 클로저로 문서를 만들어 리랭킹
$reranked = $posts->rerank(
    fn ($post) => $post->title.': '.$post->body,
    'Laravel tutorials'
);
```

응답 개수 제한, 제공자 지정 등도 가능합니다:

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

`Laravel\Ai\Files` 클래스 혹은 각 개별 파일 클래스를 통해 파일을 AI 제공자에 저장할 수 있으며, 반복하여 대화에 활용할 문서 등 크기가 큰 파일에 적합합니다:

```php
use Laravel\Ai\Files\Document;
use Laravel\Ai\Files\Image;

// 로컬 경로에서 파일 저장
$response = Document::fromPath('/home/laravel/document.pdf')->put();
$response = Image::fromPath('/home/laravel/photo.jpg')->put();

// 파일시스템의 파일 저장
$response = Document::fromStorage('document.pdf', disk: 'local')->put();
$response = Image::fromStorage('photo.jpg', disk: 'local')->put();

// 원격 URL의 파일 저장
$response = Document::fromUrl('https://example.com/document.pdf')->put();
$response = Image::fromUrl('https://example.com/photo.jpg')->put();

return $response->id;
```

Raw 문자열이나 업로드된 파일도 저장할 수 있습니다:

```php
use Laravel\Ai\Files;
use Laravel\Ai\Files\Document;

// Raw 컨텐츠 저장
$stored = Document::fromString('Hello, World!', 'text/plain')->put();

// 업로드 파일 저장
$stored = Document::fromUpload($request->file('document'))->put();
```

파일을 저장한 후에는, 이후 에이전트의 프롬프트에서 이 파일을 반복 참조하면 재업로드 없이 사용할 수 있습니다:

```php
use App\Ai\Agents\SalesCoach;
use Laravel\Ai\Files;

$response = (new SalesCoach)->prompt(
    'Analyze the attached sales transcript...',
    attachments: [
        Files\Document::fromId('file-id'), // 저장된 문서 첨부
    ]
);
```

이미 저장된 파일은 `get` 메서드로 불러올 수 있습니다:

```php
use Laravel\Ai\Files\Document;

$file = Document::fromId('file-id')->get();

$file->id;
$file->mimeType();
```

파일을 삭제하려면 `delete` 메서드를 사용하세요:

```php
Document::fromId('file-id')->delete();
```

`Files` 클래스는 기본적으로 `config/ai.php` 설정의 기본 제공자를 사용하지만, 메서드의 `provider` 인자를 통해 별도 지정도 가능합니다:

```php
$response = Document::fromPath(
    '/home/laravel/document.pdf'
)->put(provider: 'anthropic');
```

<a name="using-stored-files-in-conversations"></a>
### 대화에서 저장된 파일 사용하기 (Using Stored Files in Conversations)

파일을 제공자에 저장한 후, `Document`나 `Image` 클래스의 `fromId` 메서드로 이를 에이전트 대화의 첨부파일로 참조할 수 있습니다:

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

이미지도 마찬가지로 사용할 수 있습니다:

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

벡터 스토어를 사용하면, 검색이 가능한 파일 집합을 만들어 RAG(검색 기반 생성 등) 시 활용할 수 있습니다. `Laravel\Ai\Stores` 클래스는 벡터스토어 생성, 조회, 삭제 등 기능을 제공합니다:

```php
use Laravel\Ai\Stores;

// 새로운 벡터스토어 생성
$store = Stores::create('Knowledge Base');

// 추가 옵션과 함께 스토어 생성
$store = Stores::create(
    name: 'Knowledge Base',
    description: 'Documentation and reference materials.',
    expiresWhenIdleFor: days(30),
);

return $store->id;
```

기존 스토어를 ID로 조회하기:

```php
use Laravel\Ai\Stores;

$store = Stores::get('store_id');

$store->id;
$store->name;
$store->fileCounts;
$store->ready;
```

스토어 삭제는 ID 또는 인스턴스에서 모두 가능합니다:

```php
use Laravel\Ai\Stores;

// ID로 삭제
Stores::delete('store_id');

// 인스턴스에서 삭제
$store = Stores::get('store_id');

$store->delete();
```

<a name="adding-files-to-stores"></a>
### 스토어에 파일 추가 (Adding Files to Stores)

벡터스토어를 만든 후 [파일](#files)을 `add`로 추가할 수 있습니다. 추가된 파일은 자동으로 인덱싱되어 [파일 검색 도구](#file-search) 및 RAG에서 활용됩니다:

```php
use Laravel\Ai\Files\Document;
use Laravel\Ai\Stores;

$store = Stores::get('store_id');

// 이미 저장된 파일 추가
$document = $store->add('file_id');
$document = $store->add(Document::fromId('file_id'));

// 저장과 동시에 추가
$document = $store->add(Document::fromPath('/path/to/document.pdf'));
$document = $store->add(Document::fromStorage('manual.pdf'));
$document = $store->add($request->file('document'));

$document->id;
$document->fileId;
```

> **Note:**  
> 기존에 저장된 파일을 벡터스토어에 추가하면 반환되는 문서 ID가 파일의 기존 ID와 동일할 수 있지만, 제공자에 따라 새 ID가 생길 수도 있습니다. 미래 참조를 위해 항상 두 ID를 모두 데이터베이스에 저장하는 것이 좋습니다.

파일 추가 시 메타데이터도 첨부할 수 있습니다. 이는 [파일 검색 도구](#file-search) 사용시 결과 필터링에 활용됩니다:

```php
$store->add(Document::fromPath('/path/to/document.pdf'), metadata: [
    'author' => 'Taylor Otwell',
    'department' => 'Engineering',
    'year' => 2026,
]);
```

스토어에서 파일 제거는 `remove`로 할 수 있습니다:

```php
$store->remove('file_id');
```

스토어에서 파일을 제거해도, 해당 파일이 AI 제공자의 [파일 스토리지](#files)에서 완전히 삭제되는 것은 아닙니다. 함께 삭제하려면 `deleteFile` 옵션을 사용하세요:

```php
$store->remove('file_abc123', deleteFile: true);
```

<a name="failover"></a>
## 장애 조치 (Failover)

프롬프트 또는 기타 미디어 생성 시, 여러 제공자/모델의 배열을 전달하면, 주 제공자가 중단되거나 제한 지연이 발생할 때 대체 제공자/모델로 자동 전환됩니다:

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
### 에이전트

테스트 중 에이전트의 응답을 가짜로 만들려면 해당 에이전트 클래스의 `fake` 메서드를 호출하세요. 응답 배열이나 클로저도 전달할 수 있습니다:

```php
use App\Ai\Agents\SalesCoach;
use Laravel\Ai\Prompts\AgentPrompt;

// 모든 프롬프트에 대해 고정 응답 반환
SalesCoach::fake();

// 프롬프트 응답 리스트 지정
SalesCoach::fake([
    'First response',
    'Second response',
]);

// 프롬프트에 따라 동적 응답 제공
SalesCoach::fake(function (AgentPrompt $prompt) {
    return 'Response for: '.$prompt->prompt;
});
```

> **Note:**  
> 구조화된 출력을 반환하는 에이전트에서 `Agent::fake()`를 호출하면, Laravel이 자동으로 아웃풋 스키마에 따라 가짜 데이터를 생성합니다.

에이전트에 프롬프트를 입력한 후, 받은 프롬프트에 대한 다양한 어서션도 할 수 있습니다:

```php
use Laravel\Ai\Prompts\AgentPrompt;

SalesCoach::assertPrompted('Analyze this...');

SalesCoach::assertPrompted(function (AgentPrompt $prompt) {
    return $prompt->contains('Analyze');
});

SalesCoach::assertNotPrompted('Missing prompt');

SalesCoach::assertNeverPrompted();
```

큐잉된(비동기) 에이전트 호출은 별도 어서션을 사용하세요:

```php
use Laravel\Ai\QueuedAgentPrompt;

SalesCoach::assertQueued('Analyze this...');

SalesCoach::assertQueued(function (QueuedAgentPrompt $prompt) {
    return $prompt->contains('Analyze');
});

SalesCoach::assertNotQueued('Missing prompt');

SalesCoach::assertNeverQueued();
```

에이전트 호출이 모두 가짜 응답을 받도록 강제하려면 `preventStrayPrompts`를 사용하세요. 응답이 정의되지 않은 요청이 오면 예외가 발생합니다:

```php
SalesCoach::fake()->preventStrayPrompts();
```

<a name="testing-images"></a>
### 이미지

이미지 생성을 가짜로 처리하려면 `Image` 클래스의 `fake` 메서드를 사용합니다. 이후 받은 프롬프트나 생성 요청에 대한 다양한 어서션도 지원됩니다:

```php
use Laravel\Ai\Image;
use Laravel\Ai\Prompts\ImagePrompt;
use Laravel\Ai\Prompts\QueuedImagePrompt;

// 모든 프롬프트에 대해 고정 응답 반환
Image::fake();

// 프롬프트 응답 리스트 지정(base64 인코딩)
Image::fake([
    base64_encode($firstImage),
    base64_encode($secondImage),
]);

// 프롬프트에 따라 동적 응답 제공
Image::fake(function (ImagePrompt $prompt) {
    return base64_encode('...');
});
```

이미지 생성 후 프롬프트 기록에 대한 어서션:

```php
Image::assertGenerated(function (ImagePrompt $prompt) {
    return $prompt->contains('sunset') && $prompt->isLandscape();
});

Image::assertNotGenerated('Missing prompt');

Image::assertNothingGenerated();
```

큐잉 이미지 생성 어서션도 제공합니다:

```php
Image::assertQueued(
    fn (QueuedImagePrompt $prompt) => $prompt->contains('sunset')
);

Image::assertNotQueued('Missing prompt');

Image::assertNothingQueued();
```

모든 요청에 가짜 응답이 반드시 존재하도록 강제하려면 `preventStrayImages`를 사용하세요:

```php
Image::fake()->preventStrayImages();
```

<a name="testing-audio"></a>
### 오디오

오디오 생성도 위와 동일하게 `Audio` 클래스의 `fake` 메서드로 처리합니다. 어서션 방식도 유사합니다:

```php
use Laravel\Ai\Audio;
use Laravel\Ai\Prompts\AudioPrompt;
use Laravel\Ai\Prompts\QueuedAudioPrompt;

// 모든 프롬프트에 대해 고정 응답 반환
Audio::fake();

// 프롬프트 리스트 지정
Audio::fake([
    base64_encode($firstAudio),
    base64_encode($secondAudio),
]);

// 프롬프트에 따라 동적 응답 제공
Audio::fake(function (AudioPrompt $prompt) {
    return base64_encode('...');
});
```

오디오 생성 후 어서션:

```php
Audio::assertGenerated(function (AudioPrompt $prompt) {
    return $prompt->contains('Hello') && $prompt->isFemale();
});

Audio::assertNotGenerated('Missing prompt');

Audio::assertNothingGenerated();
```

큐잉 오디오 생성도 지원:

```php
Audio::assertQueued(
    fn (QueuedAudioPrompt $prompt) => $prompt->contains('Hello')
);

Audio::assertNotQueued('Missing prompt');

Audio::assertNothingQueued();
```

모든 요청에 가짜 응답 필수화:

```php
Audio::fake()->preventStrayAudio();
```

<a name="testing-transcriptions"></a>
### 트랜스크립션

트랜스크립션 테스트도 위와 유사하게 `fake`, 어서션 메서드를 지원합니다:

```php
use Laravel\Ai\Transcription;
use Laravel\Ai\Prompts\TranscriptionPrompt;
use Laravel\Ai\Prompts\QueuedTranscriptionPrompt;

// 모든 요청에 대해 고정 응답
Transcription::fake();

// 프롬프트 리스트
Transcription::fake([
    'First transcription text.',
    'Second transcription text.',
]);

// 프롬프트별 동적 응답
Transcription::fake(function (TranscriptionPrompt $prompt) {
    return 'Transcribed text...';
});
```

테스트 어서션 예시:

```php
Transcription::assertGenerated(function (TranscriptionPrompt $prompt) {
    return $prompt->language === 'en' && $prompt->isDiarized();
});

Transcription::assertNotGenerated(
    fn (TranscriptionPrompt $prompt) => $prompt->language === 'fr'
);

Transcription::assertNothingGenerated();
```

큐 요청 어서션:

```php
Transcription::assertQueued(
    fn (QueuedTranscriptionPrompt $prompt) => $prompt->isDiarized()
);

Transcription::assertNotQueued(
    fn (QueuedTranscriptionPrompt $prompt) => $prompt->language === 'fr'
);

Transcription::assertNothingQueued();
```

가짜 응답 필수화:

```php
Transcription::fake()->preventStrayTranscriptions();
```

<a name="testing-embeddings"></a>
### 임베딩

임베딩 생성(및 큐잉)도 같은 방식으로 `fake`, 어서션 메서드를 지원합니다:

```php
use Laravel\Ai\Embeddings;
use Laravel\Ai\Prompts\EmbeddingsPrompt;
use Laravel\Ai\Prompts\QueuedEmbeddingsPrompt;

// 자동 임베딩, 지정 응답, 동적 응답 모두 지원
Embeddings::fake();

// 응답 배열 지정
Embeddings::fake([
    [$firstEmbeddingVector],
    [$secondEmbeddingVector],
]);

// 프롬프트에 따라 동적 응답
Embeddings::fake(function (EmbeddingsPrompt $prompt) {
    return array_map(
        fn () => Embeddings::fakeEmbedding($prompt->dimensions),
        $prompt->inputs
    );
});
```

테스트 어서션 예시:

```php
Embeddings::assertGenerated(function (EmbeddingsPrompt $prompt) {
    return $prompt->contains('Laravel') && $prompt->dimensions === 1536;
});

Embeddings::assertNotGenerated(
    fn (EmbeddingsPrompt $prompt) => $prompt->contains('Other')
);

Embeddings::assertNothingGenerated();
```

큐 어서션:

```php
Embeddings::assertQueued(
    fn (QueuedEmbeddingsPrompt $prompt) => $prompt->contains('Laravel')
);

Embeddings::assertNotQueued(
    fn (QueuedEmbeddingsPrompt $prompt) => $prompt->contains('Other')
);

Embeddings::assertNothingQueued();
```

가짜 응답 필수화:

```php
Embeddings::fake()->preventStrayEmbeddings();
```

<a name="testing-reranking"></a>
### 리랭킹

리랭킹도 `fake`, 어서션 메서드 사용이 가능합니다:

```php
use Laravel\Ai\Reranking;
use Laravel\Ai\Prompts\RerankingPrompt;
use Laravel\Ai\Responses\Data\RankedDocument;

// 기본값, 사용자 지정 응답 등 지원
Reranking::fake();

Reranking::fake([
    [
        new RankedDocument(index: 0, document: 'First', score: 0.95),
        new RankedDocument(index: 1, document: 'Second', score: 0.80),
    ],
]);
```

어서션 예시:

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

파일 업로드/삭제 동작 테스트를 위해 `Files::fake()`를 사용합니다:

```php
use Laravel\Ai\Files;

Files::fake();
```

파일 저장/삭제에 대한 어서션 예시:

```php
use Laravel\Ai\Contracts\Files\StorableFile;
use Laravel\Ai\Files\Document;

// 파일 저장
Document::fromString('Hello, Laravel!', mime: 'text/plain')
    ->as('hello.txt')
    ->put();

// 저장된 파일 어서션
Files::assertStored(fn (StorableFile $file) =>
    (string) $file === 'Hello, Laravel!' &&
        $file->mimeType() === 'text/plain';
);

Files::assertNotStored(fn (StorableFile $file) =>
    (string) $file === 'Hello, World!'
);

Files::assertNothingStored();
```

파일 삭제 어서션은 파일 ID 사용:

```php
Files::assertDeleted('file-id');
Files::assertNotDeleted('file-id');
Files::assertNothingDeleted();
```

<a name="testing-vector-stores"></a>
### 벡터스토어

벡터스토어 작업도 `Stores::fake()`로 가짜 처리하며, 이 경우 [파일 작업](#files)도 자동으로 가짜 처리됩니다:

```php
use Laravel\Ai\Stores;

Stores::fake();
```

벡터스토어 생성/삭제에 대한 어서션 예시:

```php
use Laravel\Ai\Stores;

$store = Stores::create('Knowledge Base');

Stores::assertCreated('Knowledge Base');

Stores::assertCreated(fn (string $name, ?string $description) =>
    $name === 'Knowledge Base'
);

Stores::assertNotCreated('Other Store');

Stores::assertNothingCreated();
```

스토어 삭제 어서션:

```php
Stores::assertDeleted('store_id');
Stores::assertNotDeleted('other_store_id');
Stores::assertNothingDeleted();
```

스토어 인스턴스별 파일 추가/제거 어서션도 가능합니다:

```php
Stores::fake();

$store = Stores::get('store_id');

// 파일 추가/제거
$store->add('added_id');
$store->remove('removed_id');

// 어서션
$store->assertAdded('added_id');
$store->assertRemoved('removed_id');

$store->assertNotAdded('other_file_id');
$store->assertNotRemoved('other_file_id');
```

파일의 제공자 ID를 알지 못할 때는, 클로저를 활용해 내용 기반 어서션을 할 수 있습니다:

```php
use Laravel\Ai\Contracts\Files\StorableFile;
use Laravel\Ai\Files\Document;

$store->add(Document::fromString('Hello, World!', 'text/plain')->as('hello.txt'));

$store->assertAdded(fn (StorableFile $file) => $file->name() === 'hello.txt');
$store->assertAdded(fn (StorableFile $file) => $file->content() === 'Hello, World!');
```

<a name="events"></a>
## 이벤트 (Events)

Laravel AI SDK는 [이벤트](/docs/12.x/events)를 다양하게 디스패치합니다. 대표적으로 아래와 같은 이벤트가 있습니다:

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

이러한 이벤트를 리스닝하여 AI SDK의 사용 내역을 로깅하거나 저장하는 등 활용할 수 있습니다.
