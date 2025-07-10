# 큐(Queues) (Queues)

- [소개](#introduction)
    - [커넥션과 큐의 차이](#connections-vs-queues)
    - [드라이버별 참고사항 및 사전 준비](#driver-prerequisites)
- [잡(Job) 생성](#creating-jobs)
    - [잡 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [유일한 잡(Unique Jobs)](#unique-jobs)
    - [암호화된 잡(Encrypted Jobs)](#encrypted-jobs)
- [잡 미들웨어](#job-middleware)
    - [속도 제한(Rate Limiting)](#rate-limiting)
    - [잡 중복 실행 방지](#preventing-job-overlaps)
    - [예외 처리 제어(Throttling Exceptions)](#throttling-exceptions)
    - [잡 건너뛰기(Skipping Jobs)](#skipping-jobs)
- [잡 디스패치(Dispatching Jobs)](#dispatching-jobs)
    - [지연 디스패치(Delayed Dispatching)](#delayed-dispatching)
    - [동기 디스패치(Synchronous Dispatching)](#synchronous-dispatching)
    - [잡과 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [잡 체이닝(Job Chaining)](#job-chaining)
    - [큐 및 커넥션 커스터마이즈](#customizing-the-queue-and-connection)
    - [최대 시도 횟수/타임아웃 지정](#max-job-attempts-and-timeout)
    - [에러 처리](#error-handling)
- [잡 배치(Job Batching)](#job-batching)
    - [배치 가능한 잡 정의](#defining-batchable-jobs)
    - [배치 디스패치](#dispatching-batches)
    - [체인과 배치](#chains-and-batches)
    - [배치에 잡 추가](#adding-jobs-to-batches)
    - [배치 조회](#inspecting-batches)
    - [배치 취소](#cancelling-batches)
    - [배치 실패](#batch-failures)
    - [배치 정리(Pruning)](#pruning-batches)
    - [DynamoDB에 배치 저장](#storing-batches-in-dynamodb)
- [클로저 큐잉(Queueing Closures)](#queueing-closures)
- [큐 워커 실행(Running the Queue Worker)](#running-the-queue-worker)
    - [`queue:work` 명령어](#the-queue-work-command)
    - [큐 우선순위](#queue-priorities)
    - [큐 워커와 배포](#queue-workers-and-deployment)
    - [잡 만료 및 타임아웃](#job-expirations-and-timeouts)
- [Supervisor 설정](#supervisor-configuration)
- [실패한 잡 처리](#dealing-with-failed-jobs)
    - [실패한 잡 후처리](#cleaning-up-after-failed-jobs)
    - [실패한 잡 재시도](#retrying-failed-jobs)
    - [모델 없음 무시](#ignoring-missing-models)
    - [실패한 잡 정리](#pruning-failed-jobs)
    - [DynamoDB에 실패한 잡 저장](#storing-failed-jobs-in-dynamodb)
    - [실패한 잡 저장 비활성화](#disabling-failed-job-storage)
    - [실패한 잡 이벤트](#failed-job-events)
- [큐에서 잡 모두 삭제](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [일부 잡만 Fake하기](#faking-a-subset-of-jobs)
    - [잡 체인 테스트](#testing-job-chains)
    - [잡 배치 테스트](#testing-job-batches)
    - [잡/큐 상호작용 테스트](#testing-job-queue-interactions)
- [잡 이벤트](#job-events)

<a name="introduction"></a>
## 소개

웹 애플리케이션을 개발하다 보면, 업로드된 CSV 파일을 파싱하고 저장하는 작업처럼 일반적인 웹 요청 내에서는 처리 시간이 너무 오래 걸리는 작업이 있을 수 있습니다. 다행히도, 라라벨에서는 이러한 작업들을 백그라운드에서 처리할 수 있는 큐 잡을 쉽게 만들 수 있습니다. 리소스를 많이 소모하는 작업을 큐로 옮기면, 애플리케이션은 웹 요청에 훨씬 빠르게 반응하며 사용자에게 더 나은 경험을 제공합니다.

라라벨 큐 기능은 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 관계형 데이터베이스 등 다양한 큐 시스템 백엔드에 걸쳐 통합된 큐 API를 제공합니다.

라라벨의 큐 관련 설정 옵션들은 애플리케이션의 `config/queue.php` 설정 파일에 저장되어 있습니다. 이 파일에서는 프레임워크에서 지원하는 각 큐 드라이버별로 커넥션 설정을 확인할 수 있는데, 데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 드라이버는 물론, 개발 환경에서 즉시(job을 대기 없이) 실행하는 데 사용되는 동기(synchronous) 드라이버도 포함되어 있습니다. 큐에 넣은 잡을 단순히 폐기(discard)하는 목적으로 사용하는 `null` 드라이버 역시 제공됩니다.

> [!NOTE]
> 라라벨에서는 Redis 기반 큐를 위한 Horizon이라는 멋진 대시보드 및 설정 관리 도구도 제공합니다. 자세한 내용은 [Horizon 공식 문서](/docs/12.x/horizon)를 참고하세요.

<a name="connections-vs-queues"></a>
### 커넥션과 큐의 차이

라라벨 큐를 본격적으로 다루기 전에 "커넥션(connection)"과 "큐(queue)"의 차이점을 명확히 이해하는 것이 중요합니다. `config/queue.php` 설정 파일에는 `connections` 설정 배열이 있습니다. 이 옵션은 Amazon SQS, Beanstalk, Redis 등 다양한 큐 서비스에 대한 백엔드 연결 정보를 정의합니다. 그런데, 각각의 큐 커넥션 내에는 여러 개의 "큐"를 둘 수 있는데, 이는 각각을 별도의 작업 스택(stack) 혹은 잡 더미처럼 생각할 수 있습니다.

각 커넥션 설정 예시에는 `queue`라는 속성이 존재하며, 이는 해당 커넥션에 잡이 디스패치될 때 사용할 기본 큐 이름을 의미합니다. 즉, 잡을 디스패치할 때 큐를 명시적으로 지정하지 않으면 이 값에 정의된 큐에 잡이 들어가게 됩니다:

```php
use App\Jobs\ProcessPodcast;

// 이 잡은 기본 커넥션의 기본 큐로 전송됩니다...
ProcessPodcast::dispatch();

// 이 잡은 기본 커넥션의 "emails" 큐로 전송됩니다...
ProcessPodcast::dispatch()->onQueue('emails');
```

일부 애플리케이션에서는 굳이 잡을 여러 큐에 나눠 넣지 않고, 간단히 한 큐만 사용하는 것이 더 적합할 수 있습니다. 그러나 잡을 여러 큐로 분리하여 넣는 기능은, 잡을 우선순위별로 처리하거나 특정 잡 집합을 따로 관리하고 싶을 때 매우 유용합니다. 라라벨의 큐 워커는 어떤 큐를 어느 우선순위로 처리할지 지정할 수 있습니다. 예를 들어, `high` 큐로 잡을 보내고 이 큐에 높은 우선순위로 워커를 돌릴 수 있습니다:

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버별 참고사항 및 사전 준비

<a name="database"></a>
#### 데이터베이스

`database` 큐 드라이버를 사용하려면 잡 정보를 저장할 데이터베이스 테이블이 필요합니다. 일반적으로는, 라라벨의 기본 마이그레이션인 `0001_01_01_000002_create_jobs_table.php` [데이터베이스 마이그레이션](/docs/12.x/migrations)에 포함되어 있습니다. 만약 애플리케이션에 해당 마이그레이션이 없다면, `make:queue-table` 아티즌 명령어로 생성할 수 있습니다:

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### 레디스(Redis)

`redis` 큐 드라이버를 사용하려면, `config/database.php` 설정 파일에서 Redis 데이터베이스 커넥션을 먼저 설정해 주어야 합니다.

> [!WARNING]
> `serializer` 및 `compression` Redis 옵션은 `redis` 큐 드라이버에서 지원되지 않습니다.

**Redis 클러스터**

Redis 큐 커넥션이 Redis Cluster를 사용하는 경우, 큐 이름에 [키 해시 태그(key hash tag)](https://redis.io/docs/reference/cluster-spec/#hash-tags)를 반드시 포함해야 합니다. 그래야 하나의 큐에 속하는 모든 Redis 키가 동일한 해시 슬롯에 저장되어 큐가 올바르게 동작합니다:

```php
'redis' => [
    'driver' => 'redis',
    'connection' => env('REDIS_QUEUE_CONNECTION', 'default'),
    'queue' => env('REDIS_QUEUE', '{default}'),
    'retry_after' => env('REDIS_QUEUE_RETRY_AFTER', 90),
    'block_for' => null,
    'after_commit' => false,
],
```

**블로킹(Block For)**

Redis 큐를 사용할 때는, `block_for` 설정값으로 워커가 새 잡이 큐에 쌓일 때까지 대기할(블로킹할) 시간을 지정할 수 있습니다.

이 값을 조정하면, 계속해서 Redis를 폴링하는 것보다 훨씬 효율적으로 큐 대기열을 관리할 수 있습니다. 예를 들어, 5로 설정하면 잡이 들어올 때까지 5초 동안 대기(블로킹)하도록 드라이버에 지시할 수 있습니다:

```php
'redis' => [
    'driver' => 'redis',
    'connection' => env('REDIS_QUEUE_CONNECTION', 'default'),
    'queue' => env('REDIS_QUEUE', 'default'),
    'retry_after' => env('REDIS_QUEUE_RETRY_AFTER', 90),
    'block_for' => 5,
    'after_commit' => false,
],
```

> [!WARNING]
> `block_for` 옵션을 `0`으로 지정하면, 큐 워커는 새 잡이 대기열에 들어올 때까지 무한정(영구적으로) 블로킹 상태에 있게 됩니다. 이로 인해 `SIGTERM`과 같은 신호도 다음 잡이 처리 완료 전까지 처리되지 않을 수 있습니다.

<a name="other-driver-prerequisites"></a>
#### 그 외 드라이버 사전 준비

아래 드라이버를 사용하려면 다음과 같은 의존 패키지가 필요합니다. 이 패키지들은 Composer를 통해 설치할 수 있습니다:

<div class="content-list" markdown="1">

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~2.0` 또는 phpredis PHP 확장
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`

</div>

<a name="creating-jobs"></a>
## 잡(Job) 생성

<a name="generating-job-classes"></a>
### 잡 클래스 생성

기본적으로, 애플리케이션에서 큐로 처리할 잡 클래스들은 `app/Jobs` 디렉터리 내에 저장됩니다. 만약 `app/Jobs` 디렉터리가 없다면, `make:job` 아티즌 명령어를 실행하는 시점에 자동으로 생성됩니다:

```shell
php artisan make:job ProcessPodcast
```

생성된 잡 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하여, 이 잡이 비동기적으로 큐에 들어가 실행되어야 함을 라라벨에 알립니다.

> [!NOTE]
> 잡 클래스의 기본 틀(stub)은 [스텁 퍼블리싱](/docs/12.x/artisan#stub-customization)을 사용해 커스터마이즈할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조

잡 클래스는 매우 단순한 구조를 가지며, 일반적으로 큐에서 잡이 실행될 때 호출되는 `handle` 메서드만 포함하고 있습니다. 다음은 그 예시입니다. 여기서는 팟캐스트 파일 업로드와 게시 처리를 담당하는 서비스라고 가정해 보겠습니다:

```php
<?php

namespace App\Jobs;

use App\Models\Podcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    /**
     * Create a new job instance.
     */
    public function __construct(
        public Podcast $podcast,
    ) {}

    /**
     * Execute the job.
     */
    public function handle(AudioProcessor $processor): void
    {
        // Process uploaded podcast...
    }
}
```

위 예시를 보면, [Eloquent 모델](/docs/12.x/eloquent)을 잡 생성자에 직접 전달할 수 있다는 점을 알 수 있습니다. 잡이 사용하는 `Queueable` 트레잇 덕분에, Eloquent 모델과 미리 로드된 연관관계까지 잡 직렬화 및 역직렬화 과정에서 자연스럽게 처리됩니다.

잡 생성자에서 Eloquent 모델 인스턴스를 직접 받는 경우, 큐에는 모델의 고유 식별자(identifier)만 직렬화되어 저장됩니다. 실제로 잡이 실행될 때는 큐 시스템이 자동으로 데이터베이스에서 전체 모델과 연관관계 데이터를 다시 불러옵니다. 이러한 모델 직렬화 방식 덕분에 큐 드라이버에 보내는 잡 데이터(페이로드) 크기를 크게 줄일 수 있습니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드의 의존성 주입

`handle` 메서드는 큐에서 잡이 실행될 때 호출됩니다. 이때, `handle` 메서드의 매개변수 타입을 지정하면 라라벨 [서비스 컨테이너](/docs/12.x/container)가 자동으로 의존성을 주입해줍니다.

컨테이너가 `handle` 메서드에 의존성을 어떻게 주입하는지 완전히 직접 제어하고 싶다면, 컨테이너의 `bindMethod` 메서드를 사용할 수 있습니다. `bindMethod`는 콜백 함수를 받아 잡 객체와 컨테이너를 전달하며, 그 안에서 직접 `handle`을 원하는 방식으로 호출할 수 있습니다. 보통은 `App\Providers\AppServiceProvider` [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에서 아래처럼 설정합니다:

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 이미지 등과 같은 바이너리 데이터는 잡에 전달하기 전에 반드시 `base64_encode` 함수를 사용해 인코딩해야 합니다. 그렇지 않으면 큐에 잡을 넣을 때 JSON 직렬화가 제대로 동작하지 않을 수 있습니다.

<a name="handling-relationships"></a>
#### 큐 잡의 연관관계 처리

모든 Eloquent 모델의 연관관계가 큐에 잡으로 쌓이면서 함께 직렬화될 수 있으므로, 잡 문자열이 지나치게 커지는 일이 있을 수 있습니다. 그리고 잡이 역직렬화되어 실행될 때, 모델의 연관관계는(제약 조건 없이) 전체가 다시 조회됩니다. 즉, 큐에 잡을 넣기 전에 특별한 제약조건(filter, where 등)을 적용해 연관관계를 로드했더라도, 잡을 꺼낼 때에는 그 제약조건이 적용되지 않는다는 것입니다. 따라서, 잡에서 특정 연관관계의 일부만 다루고 싶으면, 필요에 따라 직접 관계를 다시 제약해야 합니다.

또는, 연관관계 데이터를 직렬화하지 않도록 하려면, 속성에 값을 설정할 때 모델의 `withoutRelations` 메서드를 호출하면 됩니다. 이렇게 하면 로드된 연관관계 정보 없이 모델 인스턴스가 저장됩니다:

```php
/**
 * Create a new job instance.
 */
public function __construct(
    Podcast $podcast,
) {
    $this->podcast = $podcast->withoutRelations();
}
```

PHP 생성자 프로퍼티 승격(property promotion)을 사용하는 경우라면, Eloquent 모델의 연관관계를 직렬화하지 않게 하기 위해 `WithoutRelations` 속성(attribute)을 사용할 수 있습니다:

```php
use Illuminate\Queue\Attributes\WithoutRelations;

/**
 * Create a new job instance.
 */
public function __construct(
    #[WithoutRelations]
    public Podcast $podcast,
) {}
```

잡이 한 개의 모델이 아니라 여러 개의 Eloquent 모델을 컬렉션 또는 배열 형태로 받을 경우, 잡이 역직렬화되어 실행될 때 이 컬렉션 내 각 모델들의 연관관계는 복원되지 않습니다. 이는 아주 많은 모델을 다루는 잡에서 리소스 사용량이 과도하게 늘어나는 것을 방지하기 위함입니다.

<a name="unique-jobs"></a>
### 유일한 잡(Unique Jobs)

> [!WARNING]
> 유일 잡(Unique job) 기능을 사용하려면 [락을 지원하는](/docs/12.x/cache#atomic-locks) 캐시 드라이버가 필요합니다. `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 원자적 락(atomic lock)을 지원합니다. 또한, 유일 잡 제한은 배치 내의 잡에는 적용되지 않습니다.

특정 잡이 한 번에 하나만 큐에 존재하도록 보장하고 싶을 때가 있습니다. 이를 위해서는 잡 클래스에서 `ShouldBeUnique` 인터페이스를 구현하면 됩니다. 이 인터페이스를 구현하는 것 외에 별도 메서드를 작성할 필요는 없습니다:

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

위 예시에서 `UpdateSearchIndex` 잡은 유일 잡입니다. 따라서 동일한 잡이 이미 큐에 존재해 처리 중이라면, 추가로 디스패치해도 큐에 쌓이지 않습니다.

경우에 따라 유일성 판단에 사용할 "키(key)"를 직접 지정하거나, 잡이 일정 시간이 지나면 유일성 제한이 풀리도록 타임아웃을 두고 싶을 수 있습니다. 이를 위해 잡 클래스에 `uniqueId` 및 `uniqueFor` 프로퍼티나 메서드를 정의할 수 있습니다:

```php
<?php

use App\Models\Product;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    /**
     * The product instance.
     *
     * @var \App\Product
     */
    public $product;

    /**
     * The number of seconds after which the job's unique lock will be released.
     *
     * @var int
     */
    public $uniqueFor = 3600;

    /**
     * Get the unique ID for the job.
     */
    public function uniqueId(): string
    {
        return $this->product->id;
    }
}
```

위 예시에서는 상품(product) ID별로 유일성을 보장하는 잡입니다. 즉, 동일한 상품 ID에 대해 이미 처리 중인 잡이 있다면, 그 동안에는 새로운 잡이 무시됩니다. 그리고 한 시간이 지나 잡이 여전히 처리되지 않을 경우 유일 락이 해제되어, 또다른 동일 키의 잡 디스패치가 가능해집니다.

> [!WARNING]
> 여러 대의 웹 서버나 컨테이너에서 잡을 디스패치하는 경우, 모든 서버가 동일한 중앙 캐시 서버와 반드시 연결되어 있어야 라라벨이 잡의 유일성을 정확하게 판단할 수 있습니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 잡 처리 시작 전까지 유일성 유지

기본적으로 유일 잡은 잡이 처리 완료되거나, 모두 재시도에 실패할 때 유일 락이 해제됩니다. 하지만 잡이 실제로 처리되기 '직전'에 유일 락을 해제하고 싶을 때도 있습니다. 이럴 때는, `ShouldBeUnique`가 아닌 `ShouldBeUniqueUntilProcessing` 인터페이스를 사용하면 됩니다:

```php
<?php

use App\Models\Product;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUniqueUntilProcessing;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUniqueUntilProcessing
{
    // ...
}
```

<a name="unique-job-locks"></a>
#### 유일 잡의 락 처리

내부적으로, `ShouldBeUnique` 잡이 디스패치될 때 라라벨은 `uniqueId` 키로[락(atomic lock)](/docs/12.x/cache#atomic-locks)을 획득하려 시도합니다. 락 획득에 실패하면 그 잡은 큐에 올라가지 않습니다. 이 락은 잡이 처리 완료되거나 재시도 횟수를 모두 소진하면 자동으로 해제됩니다. 기본적으로는 라라벨의 기본 캐시 드라이버를 통해 락을 획득하지만, 특정한 드라이버를 지정하고 싶다면, 잡 클래스에 `uniqueVia` 메서드를 정의해서 사용할 캐시 드라이버를 반환하면 됩니다:

```php
use Illuminate\Contracts\Cache\Repository;
use Illuminate\Support\Facades\Cache;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...

    /**
     * Get the cache driver for the unique job lock.
     */
    public function uniqueVia(): Repository
    {
        return Cache::driver('redis');
    }
}
```

> [!NOTE]
> 단순히 잡의 동시 처리 횟수만 제한하고 싶다면, [WithoutOverlapping](/docs/12.x/queues#preventing-job-overlaps) 잡 미들웨어 사용을 고려하세요.

<a name="encrypted-jobs"></a>
### 암호화된 잡(Encrypted Jobs)

라라벨에서는 [암호화](/docs/12.x/encryption) 기능을 통해 잡 데이터의 기밀성과 무결성을 쉽게 보장할 수 있습니다. 사용 방법은 간단히 잡 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하면 됩니다. 이 인터페이스가 추가된 클래스라면, 라라벨이 잡을 큐에 올릴 때 자동으로 암호화해 줍니다:

```php
<?php

use Illuminate\Contracts\Queue\ShouldBeEncrypted;
use Illuminate\Contracts\Queue\ShouldQueue;

class UpdateSearchIndex implements ShouldQueue, ShouldBeEncrypted
{
    // ...
}
```

<a name="job-middleware"></a>
## 잡 미들웨어

잡 미들웨어를 사용하면, 큐 잡 실행을 감싸는 커스텀 로직을 분리하여 잡 클래스 자체의 중복 코드를 줄일 수 있습니다. 예를 들어, 아래와 같이 라라벨의 Redis 속도 제한(rate limiting) 기능을 직접 활용해서 5초마다 잡 한 개만 처리할 수 있도록 `handle` 메서드를 작성할 수 있습니다:

```php
use Illuminate\Support\Facades\Redis;

/**
 * Execute the job.
 */
public function handle(): void
{
    Redis::throttle('key')->block(0)->allow(1)->every(5)->then(function () {
        info('Lock obtained...');

        // Handle job...
    }, function () {
        // Could not obtain lock...

        return $this->release(5);
    });
}
```

위 코드도 정상 작동하지만, `handle` 메서드가 Redis 속도 제한 코드로 어수선해지고, 다른 잡에도 동일한 속도 제한이 필요할 때 매번 중복 코드를 써야 하는 문제가 있습니다.

이런 경우, 직접 잡 미들웨어로 속도 제한 로직을 분리해 관리할 수 있습니다. 잡 미들웨어는 라라벨에서 기본 위치가 정해져 있지 않으므로 애플리케이션 원하는 곳에 위치시킬 수 있습니다. 여기서는 `app/Jobs/Middleware` 디렉터리에 두는 예시를 보여줍니다:

```php
<?php

namespace App\Jobs\Middleware;

use Closure;
use Illuminate\Support\Facades\Redis;

class RateLimited
{
    /**
     * Process the queued job.
     *
     * @param  \Closure(object): void  $next
     */
    public function handle(object $job, Closure $next): void
    {
        Redis::throttle('key')
            ->block(0)->allow(1)->every(5)
            ->then(function () use ($job, $next) {
                // Lock obtained...

                $next($job);
            }, function () use ($job) {
                // Could not obtain lock...

                $job->release(5);
            });
    }
}
```

이처럼 [라우트 미들웨어](/docs/12.x/middleware)처럼 잡 미들웨어 역시 현재 처리 중인 잡과, 잡 처리를 계속 진행할 때 호출할 콜백을 매개변수로 받습니다.

`make:job-middleware` 아티즌 명령어로 새 잡 미들웨어 클래스를 간편하게 생성할 수 있습니다. 미들웨어를 만든 뒤에는, 잡 클래스의 `middleware` 메서드에서 이 미들웨어를 반환하여 잡에 적용할 수 있습니다. 단, 이 메서드는 `make:job` 명령어로 생성한 잡 클래스에는 기본적으로 포함되어 있지 않으므로, 직접 추가해야 합니다:

```php
use App\Jobs\Middleware\RateLimited;

/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited];
}
```

> [!NOTE]
> 잡 미들웨어는 [큐 처리 이벤트 리스너](/docs/12.x/events#queued-event-listeners), [메일(mailable)의 큐잉](/docs/12.x/mail#queueing-mail), [알림(notifications)의 큐잉](/docs/12.x/notifications#queueing-notifications)에도 사용할 수 있습니다.

<a name="rate-limiting"></a>
### 속도 제한(Rate Limiting)

지금까지 속도 제한 잡 미들웨어를 직접 작성하는 방법을 살펴보았으나, 라라벨에는 이미 편리하게 사용할 수 있는 속도 제한 미들웨어가 내장되어 있습니다. [라우트 속도 제한자](/docs/12.x/routing#defining-rate-limiters)처럼, 잡 속도 제한자도 `RateLimiter` 파사드의 `for` 메서드로 정의할 수 있습니다.

예를 들어, 일반 사용자에 한해 백업은 1시간에 한 번만 가능하게 제한하고, 프리미엄 고객은 제한을 두지 않을 수 있습니다. 이런 정책을 적용하려면, `AppServiceProvider`의 `boot` 메서드에서 `RateLimiter`를 다음과 같이 정의합니다:

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Support\Facades\RateLimiter;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    RateLimiter::for('backups', function (object $job) {
        return $job->user->vipCustomer()
            ? Limit::none()
            : Limit::perHour(1)->by($job->user->id);
    });
}
```

위 예시에서는 1시간 단위의 속도 제한을 설정했지만, `perMinute` 메서드를 사용해 분 단위로도 손쉽게 만들 수 있습니다. 또한 `by` 메서드에는 원하는 값을 전달할 수 있지만, 일반적으로 고객 단위로 속도 제한을 구분할 때 자주 사용됩니다:

```php
return Limit::perMinute(50)->by($job->user->id);
```

속도 제한자 정의 후에는, 해당 잡에 `Illuminate\Queue\Middleware\RateLimited` 미들웨어를 적용해줄 수 있습니다. 잡이 정해진 속도 제한을 초과할 때마다, 이 미들웨어는 잡을 큐로 다시 되돌려 보내고, 제한 시간만큼 지연시킨 후 재시도합니다.

```php
use Illuminate\Queue\Middleware\RateLimited;

/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited('backups')];
}
```

속도 제한으로 인해 잡이 큐에 다시 반환되는 경우, 해당 잡의 전체 `attempts`(시도 횟수) 값은 계속 증가합니다. 필요하다면 잡 클래스의 `tries`, `maxExceptions` 프로퍼티를 적절히 조정하거나, [retryUntil 메서드](#time-based-attempts)로 잡 재시도 종료 조건을 지정할 수도 있습니다.

`releaseAfter` 메서드를 사용하면, 재시도하기 전에 잡을 다시 대기열에 넣을 때 얼마만큼의 시간이 경과해야 할지(초 단위) 직접 지정할 수도 있습니다:

```php
/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new RateLimited('backups'))->releaseAfter(60)];
}
```

속도 제한에 걸릴 경우 잡을 재시도하지 않도록 하려면, `dontRelease` 메서드를 사용할 수 있습니다:

```php
/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new RateLimited('backups'))->dontRelease()];
}
```

> [!NOTE]
> Redis를 사용할 경우, 일반 속도 제한 미들웨어보다 효율적으로 동작하는 `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어를 활용할 수 있습니다.

<a name="preventing-job-overlaps"></a>
### 잡 중복 실행 방지

라라벨은 임의의 키값에 기반해 잡의 중복 실행을 막아주는 `Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어를 내장하고 있습니다. 이는 한 번에 오직 하나의 잡만 리소스를 변경해야 할 때 유용하게 쓰입니다.

예를 들어, 사용자의 신용점수(credit score)를 업데이트하는 잡을 큐에 넣을 때, 같은 사용자 ID로 중복 업데이트가 동시에 실행되지 않게 하려면, 잡 클래스의 `middleware` 메서드에서 `WithoutOverlapping` 미들웨어를 반환하면 됩니다:

```php
use Illuminate\Queue\Middleware\WithoutOverlapping;

/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new WithoutOverlapping($this->user->id)];
}
```

동일한 키의 중복 잡들은 다시 큐에 되돌려집니다. 또한, `releaseAfter` 메서드로 잡을 다시 시도하기 전 대기시간(초)을 지정할 수 있습니다:

```php
/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->releaseAfter(60)];
}
```

즉시 중복 잡을 삭제하여 더 이상 재시도하지 않게 하고 싶다면, `dontRelease` 메서드를 사용할 수 있습니다:

```php
/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->dontRelease()];
}
```

`WithoutOverlapping` 미들웨어는 라라벨의 원자적 락(atomic lock) 기능을 기반으로 합니다. 잡이 예기치 않게 실패하거나 타임아웃이 발생하여 락이 풀리지 않을 수도 있으므로, `expireAfter` 메서드로 락의 만료 시간을 직접 지정할 수 있습니다. 아래 예시는 잡 실행 시작 후 3분(180초)가 지나면 락이 자동 해제되도록 지시합니다:

```php
/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->expireAfter(180)];
}
```

> [!WARNING]
> `WithoutOverlapping` 미들웨어는 [락을 지원하는](/docs/12.x/cache#atomic-locks) 캐시 드라이버가 필요합니다. `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 원자적 락을 지원합니다.

<a name="sharing-lock-keys"></a>

#### 서로 다른 작업 클래스 간의 Lock 키 공유

기본적으로 `WithoutOverlapping` 미들웨어는 동일한 작업 클래스 내에서만 중복 실행을 방지합니다. 따라서 두 개의 서로 다른 작업 클래스가 동일한 lock 키를 사용하더라도, 이들은 동시에 실행되는 것을 막지 않습니다. 하지만, `shared` 메서드를 사용하여 라라벨이 두 작업 클래스 전체에서 lock 키를 적용하도록 지시할 수 있습니다.

```php
use Illuminate\Queue\Middleware\WithoutOverlapping;

class ProviderIsDown
{
    // ...

    public function middleware(): array
    {
        return [
            (new WithoutOverlapping("status:{$this->provider}"))->shared(),
        ];
    }
}

class ProviderIsUp
{
    // ...

    public function middleware(): array
    {
        return [
            (new WithoutOverlapping("status:{$this->provider}"))->shared(),
        ];
    }
}
```

<a name="throttling-exceptions"></a>
### 예외 제한(Throttling Exceptions)

라라벨에는 예외 발생을 제한(throttle)할 수 있는 `Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어가 포함되어 있습니다. 이 미들웨어를 사용하면 특정 횟수만큼 예외가 발생한 후에는, 지정한 시간 간격이 지날 때까지 해당 작업의 실행 시도가 모두 지연됩니다. 이 방식은 주로 외부 서비스와 연동하는 작업에서 불안정한 상황을 제어할 때 유용합니다.

예를 들어, 외부 API와 상호작용하는 큐 작업에서 예외가 반복적으로 발생한다고 가정해 보겠습니다. 예외 제한 기능을 사용하려면 작업의 `middleware` 메서드에서 `ThrottlesExceptions` 미들웨어를 반환하면 됩니다. 보통 이 미들웨어는 [시간 기반 시도(time based attempts)](#time-based-attempts)를 구현하는 작업과 함께 사용해야 합니다.

```php
use DateTime;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 작업이 통과해야 할 미들웨어를 반환합니다.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new ThrottlesExceptions(10, 5 * 60)];
}

/**
 * 작업이 타임아웃될 시간을 결정합니다.
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(30);
}
```

위 예제에서 미들웨어의 첫 번째 생성자 인수는 예외가 제한되기(throttle 적용) 전까지 허용할 예외 횟수이고, 두 번째 인수는 throttle이 적용된 후 작업이 다시 시도되기 전에 대기해야 할(초 단위) 시간입니다. 예시에서는 작업이 연속 10번 예외를 발생시키면, 5분 동안 대기한 뒤, 30분 타임리밋 내에서 다시 시도하게 됩니다.

작업에서 예외가 발생했지만 아직 제한 임계치에 도달하지 않은 경우에는, 일반적으로 곧바로 재시도됩니다. 하지만 미들웨어를 작업에 추가할 때 `backoff` 메서드를 호출해 작업이 지연되는(몇 분 후 재시도) 시간을 명시할 수 있습니다.

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 작업이 통과해야 할 미들웨어를 반환합니다.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 5 * 60))->backoff(5)];
}
```

이 미들웨어는 내부적으로 라라벨의 캐시 시스템을 사용하여 속도 제한(rate limiting)을 구현하며, 작업의 클래스명이 캐시 "키"로 활용됩니다. 만약 동일한 외부 서비스를 여러 작업이 사용하는데 이들 모두 공통된 제한(버킷)을 공유하길 원한다면, 미들웨어를 추가할 때 `by` 메서드로 키를 오버라이드 할 수 있습니다.

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 작업이 통과해야 할 미들웨어를 반환합니다.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->by('key')];
}
```

기본적으로 이 미들웨어는 모든 예외를 제한합니다. 필요하다면 작업에 미들웨어를 추가할 때 `when` 메서드를 사용해 제한 대상이 될 예외를 선택적으로 지정할 수 있습니다. 이때, `when`에 전달한 클로저가 `true`를 반환하는 경우에만 예외가 제한 처리됩니다.

```php
use Illuminate\Http\Client\HttpClientException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 작업이 통과해야 할 미들웨어를 반환합니다.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->when(
        fn (Throwable $throwable) => $throwable instanceof HttpClientException
    )];
}
```

`when` 메서드와 다르게, `deleteWhen` 메서드는 특정 예외 발생 시 작업을 큐에서 되돌리거나 예외를 던지는 대신, 작업 자체를 즉시 삭제합니다.

```php
use App\Exceptions\CustomerDeletedException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 작업이 통과해야 할 미들웨어를 반환합니다.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(2, 10 * 60))->deleteWhen(CustomerDeletedException::class)];
}
```

제한(throttled)된 예외를 애플리케이션의 예외 핸들러에 보고하고 싶다면, 작업에 미들웨어를 추가할 때 `report` 메서드를 사용할 수 있습니다. 또한, `report` 메서드에 클로저를 전달해, 해당 클로저가 `true`를 반환할 때만 예외가 보고되도록 제어할 수 있습니다.

```php
use Illuminate\Http\Client\HttpClientException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 작업이 통과해야 할 미들웨어를 반환합니다.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->report(
        fn (Throwable $throwable) => $throwable instanceof HttpClientException
    )];
}
```

> [!NOTE]
> Redis를 사용하는 경우라면, Redis에 최적화되어 있고 기본 예외 제한 미들웨어보다 더 효율적인 `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어를 사용할 수 있습니다.

<a name="skipping-jobs"></a>
### 작업 건너뛰기

`Skip` 미들웨어를 이용하면 작업의 로직을 따로 수정하지 않고도 특정 작업을 건너뛰거나 삭제할 수 있습니다. `Skip::when` 메서드는 지정한 조건이 `true`로 평가되면 해당 작업을 삭제하며, `Skip::unless`는 조건이 `false`일 때 작업을 삭제합니다.

```php
use Illuminate\Queue\Middleware\Skip;

/**
 * 작업이 통과해야 할 미들웨어를 반환합니다.
 */
public function middleware(): array
{
    return [
        Skip::when($someCondition),
    ];
}
```

더 복잡한 조건 판단이 필요할 경우, `when`과 `unless`에 `Closure`를 전달할 수 있습니다.

```php
use Illuminate\Queue\Middleware\Skip;

/**
 * 작업이 통과해야 할 미들웨어를 반환합니다.
 */
public function middleware(): array
{
    return [
        Skip::when(function (): bool {
            return $this->shouldSkip();
        }),
    ];
}
```

<a name="dispatching-jobs"></a>
## 작업 디스패치(Dispatching Jobs)

작업 클래스를 작성한 후에는 해당 작업 클래스에서 `dispatch` 메서드를 통해 작업을 디스패치할 수 있습니다. `dispatch` 메서드에 전달된 인수들은 작업의 생성자에 전달됩니다.

```php
<?php

namespace App\Http\Controllers;

use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    /**
     * 새 팟캐스트 저장.
     */
    public function store(Request $request): RedirectResponse
    {
        $podcast = Podcast::create(/* ... */);

        // ...

        ProcessPodcast::dispatch($podcast);

        return redirect('/podcasts');
    }
}
```

작업을 조건적으로 디스패치하고 싶다면 `dispatchIf` 또는 `dispatchUnless` 메서드를 사용할 수 있습니다.

```php
ProcessPodcast::dispatchIf($accountActive, $podcast);

ProcessPodcast::dispatchUnless($accountSuspended, $podcast);
```

새로운 라라벨 애플리케이션에서는 기본 큐 드라이버로 `sync` 드라이버가 설정되어 있습니다. 이 드라이버는 큐 작업을 현재 요청의 포그라운드에서 동기적으로 실행하기 때문에, 로컬 개발 중에 유용하게 사용할 수 있습니다. 실제로 백그라운드 처리를 위해 큐를 사용하고 싶다면, 애플리케이션의 `config/queue.php` 설정 파일에서 다른 큐 드라이버를 지정해야 합니다.

<a name="delayed-dispatching"></a>
### 예약(딜레이) 디스패치

작업이 큐 워커에 의해 즉시 처리되지 않고 일정 시간이 지난 뒤에만 처리되길 원한다면, 작업을 디스패치할 때 `delay` 메서드를 사용할 수 있습니다. 예를 들어, 작업이 디스패치된 후 10분이 지나야 처리되도록 설정하고 싶다면 아래와 같이 작성합니다.

```php
<?php

namespace App\Http\Controllers;

use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    /**
     * 새 팟캐스트 저장.
     */
    public function store(Request $request): RedirectResponse
    {
        $podcast = Podcast::create(/* ... */);

        // ...

        ProcessPodcast::dispatch($podcast)
            ->delay(now()->addMinutes(10));

        return redirect('/podcasts');
    }
}
```

특정 작업에 기본 지연 시간이 이미 설정되어 있을 수 있습니다. 이 지연을 무시하고 즉시 작업을 디스패치하려면 `withoutDelay` 메서드를 사용할 수 있습니다.

```php
ProcessPodcast::dispatch($podcast)->withoutDelay();
```

> [!WARNING]
> Amazon SQS 큐 서비스는 딜레이 가능한 최대 시간이 15분입니다.

<a name="dispatching-after-the-response-is-sent-to-browser"></a>
#### 브라우저에 응답을 보낸 뒤 작업 디스패치

또는 서버가 FastCGI를 사용한다면, `dispatchAfterResponse` 메서드를 통해 HTTP 응답이 브라우저에 전송된 이후에야 작업이 디스패치되도록 할 수 있습니다. 이렇게 하면, 큐 작업이 실행 중이어도 사용자는 곧바로 애플리케이션을 이용할 수 있습니다. 이 방식은 보통 이메일 발송처럼 1초 내외로 완료되는 간단한 작업에 사용해야 하며, 이 경우 별도의 큐 워커가 실행 중이지 않더라도 작업이 현재 HTTP 요청 내에서 처리됩니다.

```php
use App\Jobs\SendNotification;

SendNotification::dispatchAfterResponse();
```

클로저를 `dispatch`로 디스패치한 뒤 `afterResponse` 메서드를 체이닝하여 HTTP 응답 후 실행할 수도 있습니다.

```php
use App\Mail\WelcomeMessage;
use Illuminate\Support\Facades\Mail;

dispatch(function () {
    Mail::to('taylor@example.com')->send(new WelcomeMessage);
})->afterResponse();
```

<a name="synchronous-dispatching"></a>
### 동기식 디스패치

작업을 즉시(동기 방식으로) 실행하고자 한다면 `dispatchSync` 메서드를 사용할 수 있습니다. 이 메서드를 사용하면 작업이 큐잉되지 않고, 현재 프로세스 내에서 즉시 실행됩니다.

```php
<?php

namespace App\Http\Controllers;

use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    /**
     * 새 팟캐스트 저장.
     */
    public function store(Request $request): RedirectResponse
    {
        $podcast = Podcast::create(/* ... */);

        // Create podcast...

        ProcessPodcast::dispatchSync($podcast);

        return redirect('/podcasts');
    }
}
```

<a name="jobs-and-database-transactions"></a>
### 작업과 데이터베이스 트랜잭션(Jobs & Database Transactions)

데이터베이스 트랜잭션 내에서 작업을 디스패치하는 것은 문제가 되지 않지만, 해당 작업이 실제로 성공적으로 실행될 수 있도록 특별히 신경 써야 합니다. 트랜잭션 내에서 작업을 디스패치하면, 부모 트랜잭션이 커밋되기 전에 작업이 워커에 의해 처리될 수 있습니다. 이렇게 되면 트랜잭션 내에서 업데이트 한 모델이나 데이터베이스 레코드가 실제 DB에는 아직 반영되지 않아, 작업에서 예상대로 조회되지 않을 수 있습니다. 또한, 트랜잭션 중에 새로 생성된 모델이나 레코드가 DB에 아직 존재하지 않을 수도 있습니다.

다행히, 라라벨은 이 문제에 대한 몇 가지 우회 방법을 제공합니다. 첫째, 큐 연결의 설정 배열에서 `after_commit` 옵션을 `true`로 지정할 수 있습니다.

```php
'redis' => [
    'driver' => 'redis',
    // ...
    'after_commit' => true,
],
```

`after_commit` 옵션이 `true`일 경우 트랜잭션 내에서 작업을 디스패치하면, 라라벨은 부모 데이터베이스 트랜잭션이 커밋될 때까지 작업을 실제로 디스패치하지 않고 대기합니다. 현재 열린 트랜잭션이 없다면 작업은 즉시 디스패치됩니다.

만약 트랜잭션 수행 중 예외로 인해 롤백된다면, 해당 트랜잭션 동안 디스패치했던 모든 작업은 삭제(discard)됩니다.

> [!NOTE]
> `after_commit` 설정을 `true`로 하면, 큐에 등록된 이벤트 리스너, 메일러블, 알림, 브로드캐스트 이벤트도 모두 데이터베이스 트랜잭션이 모두 커밋된 뒤에 실행됩니다.

<a name="specifying-commit-dispatch-behavior-inline"></a>
#### 커밋 시 디스패치 동작을 인라인으로 지정

큐 연결 설정의 `after_commit` 옵션을 `true`로 넣지 않아도, 특정 작업만 트랜잭션 커밋 후에 디스패치되도록 할 수 있습니다. 이를 위해서는 디스패치 시 `afterCommit` 메서드를 체이닝하면 됩니다.

```php
use App\Jobs\ProcessPodcast;

ProcessPodcast::dispatch($podcast)->afterCommit();
```

반대로, `after_commit` 설정값이 `true`인 경우 특정 작업을 트랜잭션 커밋을 기다리지 않고 바로 디스패치하고 싶다면 `beforeCommit` 메서드를 사용할 수 있습니다.

```php
ProcessPodcast::dispatch($podcast)->beforeCommit();
```

<a name="job-chaining"></a>
### 작업 체이닝(Job Chaining)

작업 체이닝 기능을 이용하면, 주요 작업이 성공적으로 실행된 뒤 순차적으로 실행되어야 하는 여러 개의 큐 작업 목록을 지정할 수 있습니다. 시퀀스 내 어느 한 작업이 실패하면, 이후 작업들은 실행되지 않습니다. 체이닝을 하려면, `Bus` 파사드의 `chain` 메서드를 이용하면 됩니다. 라라벨의 커맨드 버스는 큐 작업 디스패치의 저수준 컴포넌트입니다.

```php
use App\Jobs\OptimizePodcast;
use App\Jobs\ProcessPodcast;
use App\Jobs\ReleasePodcast;
use Illuminate\Support\Facades\Bus;

Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->dispatch();
```

클래스 인스턴스뿐만 아니라 클로저도 체인에 추가할 수 있습니다.

```php
Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    function () {
        Podcast::update(/* ... */);
    },
])->dispatch();
```

> [!WARNING]
> 작업 내에서 `$this->delete()` 메서드를 사용해 작업을 삭제하더라도, 체이닝된 나머지 작업이 처리되는 것을 막지 못합니다. 체인은 오직 체인 내 작업 중 하나라도 실패했을 때만 멈춥니다.

<a name="chain-connection-queue"></a>
#### 체인 작업용 연결 및 큐 지정

체인 작업을 실행할 때, 이 체인 내의 작업들이 사용할 연결(connection)과 큐(queue)를 지정하고 싶다면 `onConnection` 및 `onQueue` 메서드를 사용할 수 있습니다. 이 메서드들은 큐 작업에서 따로 연결 또는 큐를 명시하지 않는 한, 기본적으로 지정된 값이 쓰입니다.

```php
Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->onConnection('redis')->onQueue('podcasts')->dispatch();
```

<a name="adding-jobs-to-the-chain"></a>
#### 체인에 작업 추가하기

가끔, 체인에 이미 등록된 작업 실행 중에, 그 체인에 새 작업을 앞이나 뒤에 추가해야 할 때가 있습니다. 이런 경우, `prependToChain`(앞에 추가), `appendToChain`(뒤에 추가) 메서드를 사용할 수 있습니다.

```php
/**
 * 작업 실행.
 */
public function handle(): void
{
    // ...

    // 현재 체인 앞에 작업 추가, 현재 작업 직후에 실행...
    $this->prependToChain(new TranscribePodcast);

    // 현재 체인 맨 끝에 작업 추가, 체인 마지막에 실행...
    $this->appendToChain(new TranscribePodcast);
}
```

<a name="chain-failures"></a>
#### 체인 내 실패 처리

작업을 체이닝할 때, 체인 내의 어느 작업이라도 실패하면 호출할 클로저를 `catch` 메서드로 지정할 수 있습니다. 이 콜백은 실패를 유발한 `Throwable` 인스턴스를 전달받습니다.

```php
use Illuminate\Support\Facades\Bus;
use Throwable;

Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->catch(function (Throwable $e) {
    // 체인 내 작업 중 하나가 실패한 경우...
})->dispatch();
```

> [!WARNING]
> 체인 콜백은 직렬화되어 큐에 의해 나중에 실행되므로, 콜백 내부에서 `$this` 변수를 사용하면 안 됩니다.

<a name="customizing-the-queue-and-connection"></a>
### 큐와 연결 커스터마이징

<a name="dispatching-to-a-particular-queue"></a>
#### 특정 큐로 작업 디스패치

작업을 다양한 큐에 분산시키면, 큐 작업을 "카테고리화"할 수 있으며 각각의 큐에 할당하는 워커 수로 우선순위를 조절할 수도 있습니다. 주의할 점은, 이는 큐 설정 파일에 정의된 서로 다른 "큐 연결(connection)"로 작업을 푸시하는 것이 아니라, 하나의 연결 내에서 다른 큐(이름)에만 작업을 지정하는 것입니다. 큐를 지정하려면 작업을 디스패치할 때 `onQueue` 메서드를 사용하면 됩니다.

```php
<?php

namespace App\Http\Controllers;

use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    /**
     * 새 팟캐스트 저장.
     */
    public function store(Request $request): RedirectResponse
    {
        $podcast = Podcast::create(/* ... */);

        // Create podcast...

        ProcessPodcast::dispatch($podcast)->onQueue('processing');

        return redirect('/podcasts');
    }
}
```

또는, 작업 클래스의 생성자에서 `onQueue` 메서드를 호출해 작업의 기본 큐를 지정할 수도 있습니다.

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    /**
     * 새 작업 인스턴스 생성.
     */
    public function __construct()
    {
        $this->onQueue('processing');
    }
}
```

<a name="dispatching-to-a-particular-connection"></a>
#### 특정 연결로 작업 디스패치

애플리케이션이 여러 큐 연결을 사용하는 경우, `onConnection` 메서드를 사용하여 작업을 푸시할 연결을 지정할 수 있습니다.

```php
<?php

namespace App\Http\Controllers;

use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    /**
     * 새 팟캐스트 저장.
     */
    public function store(Request $request): RedirectResponse
    {
        $podcast = Podcast::create(/* ... */);

        // Create podcast...

        ProcessPodcast::dispatch($podcast)->onConnection('sqs');

        return redirect('/podcasts');
    }
}
```

`onConnection`과 `onQueue` 메서드를 연달아 사용하여, 동시에 연결과 큐 둘 다 지정할 수도 있습니다.

```php
ProcessPodcast::dispatch($podcast)
    ->onConnection('sqs')
    ->onQueue('processing');
```

또한, 작업 클래스 생성자에서 `onConnection`을 호출하여 작업의 연결을 지정하는 것도 가능합니다.

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    /**
     * 새 작업 인스턴스 생성.
     */
    public function __construct()
    {
        $this->onConnection('sqs');
    }
}
```

<a name="max-job-attempts-and-timeout"></a>

### 최대 작업 시도 횟수 / 타임아웃 값 지정하기

<a name="max-attempts"></a>
#### 최대 시도 횟수

대기열에 등록된 작업이 오류를 계속 발생시키는 경우, 해당 작업이 무한히 재시도되도록 두고 싶지는 않을 것입니다. 라라벨에서는 작업이 몇 번 또는 얼마 동안 시도될 수 있는지 지정하는 여러 방법을 제공합니다.

작업이 시도될 최대 횟수를 지정하는 한 가지 방법은 아티즌 명령어 실행 시 `--tries` 옵션을 사용하는 것입니다. 이 값을 지정하면, 별도로 작업 클래스에서 시도 횟수를 지정하지 않는 한 워커가 처리하는 모든 작업에 적용됩니다.

```shell
php artisan queue:work --tries=3
```

작업이 지정된 최대 시도 횟수를 초과하면, "실패"한 작업으로 간주됩니다. 실패한 작업 처리에 대한 자세한 내용은 [실패한 작업 문서](#dealing-with-failed-jobs)를 참고하십시오. 만약 `queue:work` 명령어에 `--tries=0`을 지정하면 작업은 무한히 재시도됩니다.

좀 더 세밀하게 제어하고 싶다면, 작업 클래스에서 최대 시도 횟수를 지정할 수도 있습니다. 만약 작업 클래스에서 최대 시도 횟수를 지정하면, 명령줄에서 지정한 `--tries` 값보다 우선 적용됩니다.

```php
<?php

namespace App\Jobs;

class ProcessPodcast implements ShouldQueue
{
    /**
     * 작업이 시도될 최대 횟수.
     *
     * @var int
     */
    public $tries = 5;
}
```

특정 작업의 최대 시도 횟수를 동적으로 제어해야 할 경우, 작업 클래스에 `tries` 메서드를 정의할 수 있습니다.

```php
/**
 * 이 작업이 시도될 최대 횟수를 반환합니다.
 */
public function tries(): int
{
    return 5;
}
```

<a name="time-based-attempts"></a>
#### 시간 기반 시도 제한

작업이 실패하기 전까지 시도할 횟수를 지정하는 대신, 일정 시간까지만 작업을 재시도하도록 정의할 수도 있습니다. 즉, 지정한 기간 내에서라면 횟수와 관계 없이 계속 시도하게 할 수 있습니다. 이를 위해 작업 클래스에 `retryUntil` 메서드를 추가하고, 이 메서드는 `DateTime` 인스턴스를 반환해야 합니다.

```php
use DateTime;

/**
 * 작업의 타임아웃 시점을 정의합니다.
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(10);
}
```

`retryUntil`과 `tries` 모두 정의되어 있을 경우, 라라벨은 `retryUntil` 메서드를 우선적으로 적용합니다.

> [!NOTE]
> [대기열에 등록된 이벤트 리스너](/docs/12.x/events#queued-event-listeners) 및 [대기열로 처리되는 알림](/docs/12.x/notifications#queueing-notifications)에서도 `tries` 속성이나 `retryUntil` 메서드를 정의할 수 있습니다.

<a name="max-exceptions"></a>
#### 최대 예외 허용 횟수

경우에 따라 작업의 시도 횟수는 많게 설정하되, 지정한 횟수만큼 "예상치 못한 예외"가 발생했다면 작업을 바로 실패로 처리하고 싶을 수 있습니다(명시적으로 `release` 메서드로 릴리즈된 경우는 제외). 이를 위해 작업 클래스에 `maxExceptions` 속성을 정의할 수 있습니다.

```php
<?php

namespace App\Jobs;

use Illuminate\Support\Facades\Redis;

class ProcessPodcast implements ShouldQueue
{
    /**
     * 작업이 시도될 최대 횟수.
     *
     * @var int
     */
    public $tries = 25;

    /**
     * 실패 처리 전 허용되는 예외의 최대 횟수.
     *
     * @var int
     */
    public $maxExceptions = 3;

    /**
     * 작업 실행.
     */
    public function handle(): void
    {
        Redis::throttle('key')->allow(10)->every(60)->then(function () {
            // 락을 획득했으므로 팟캐스트 처리...
        }, function () {
            // 락을 획득하지 못함...
            return $this->release(10);
        });
    }
}
```

위 예시에서 애플리케이션이 Redis 락을 얻지 못하면 10초 동안 작업이 릴리즈되고, 최대 25번까지 계속 재시도됩니다. 단, 작업 수행 중에 처리되지 않은 예외가 3번 발생하면 작업은 실패 처리됩니다.

<a name="timeout"></a>
#### 타임아웃 지정

보통 대기열 작업이 어느 정도 걸릴지 예측할 수 있습니다. 그래서 라라벨에서는 "타임아웃" 값을 지정할 수 있습니다. 기본적으로 타임아웃은 60초입니다. 만약 작업이 타임아웃으로 지정된 초수보다 더 오래 걸리면, 해당 작업을 처리하던 워커 프로세스는 오류와 함께 종료됩니다. 일반적으로 워커는 [서버에 구성된 프로세스 관리자](#supervisor-configuration)에 의해 자동으로 재시작됩니다.

작업이 실행될 최대 시간(초)은 아티즌 명령어에서 `--timeout` 옵션으로 지정할 수 있습니다.

```shell
php artisan queue:work --timeout=30
```

작업이 지속적으로 타임아웃되어 최대 시도 횟수를 초과하면, 실패한 작업으로 처리됩니다.

또한 작업 클래스에서 작업별로 최대 허용 시간을 정의할 수도 있습니다. 작업에 명시된 값이 있다면, 명령줄의 설정보다 우선 적용됩니다.

```php
<?php

namespace App\Jobs;

class ProcessPodcast implements ShouldQueue
{
    /**
     * 타임아웃될 때까지 실행 가능한 시간(초).
     *
     * @var int
     */
    public $timeout = 120;
}
```

소켓 등 입출력이 블로킹되는 프로세스나 외부 HTTP 연결과 같이, 작업 자체가 라라벨의 타임아웃 설정을 따르지 않을 수 있습니다. 이런 기능을 사용할 때는 각 API에서도 타임아웃 값을 반드시 설정해야 합니다. 예를 들어, Guzzle을 사용할 때는 항상 연결 및 요청의 타임아웃 값을 지정하는 것이 좋습니다.

> [!WARNING]
> 작업 타임아웃 값을 지정하려면 [PCNTL](https://www.php.net/manual/en/book.pcntl.php) PHP 확장이 설치되어 있어야 합니다. 또한, 작업의 "타임아웃" 값은 항상 ["retry after"](#job-expiration)값보다 작아야 합니다. 그렇지 않으면, 실제 작업이 실행되거나 종료되기도 전에 작업이 다시 시도될 수 있습니다.

<a name="failing-on-timeout"></a>
#### 타임아웃 시 작업 실패 처리

타임아웃이 발생할 때 해당 작업을 [실패한 작업](#dealing-with-failed-jobs)으로 표시하려면, 작업 클래스에 `$failOnTimeout` 속성을 정의하면 됩니다.

```php
/**
 * 타임아웃 시 작업을 실패로 처리할지 여부.
 *
 * @var bool
 */
public $failOnTimeout = true;
```

<a name="error-handling"></a>
### 오류 처리

작업 처리 중에 예외가 발생하면, 해당 작업은 자동으로 대기열에 다시 반환(release)되어 이후 재시도됩니다. 이는 애플리케이션에서 허용된 최대 시도 횟수만큼 반복됩니다. 최대 시도 횟수는 `queue:work` 아티즌 명령어의 `--tries` 옵션으로 지정하거나, 혹은 작업 클래스에서 직접 정의할 수 있습니다. 대기열 워커 실행에 관한 더 자세한 정보는 [아래에서 확인할 수 있습니다](#running-the-queue-worker).

<a name="manually-releasing-a-job"></a>
#### 작업을 수동으로 릴리즈하기

가끔, 작업을 수동으로 대기열에 다시 반환해서 나중에 재시도하도록 만들고 싶을 때가 있습니다. 이럴 때는 `release` 메서드를 호출하면 됩니다.

```php
/**
 * 작업 실행.
 */
public function handle(): void
{
    // ...

    $this->release();
}
```

기본적으로 `release` 메서드는 작업을 즉시 다시 대기열에 올려 바로 처리될 수 있게 합니다. 하지만, 정수 형태(초 단위)나 날짜 인스턴스를 전달해서 지정한 시간 이후에만 처리 가능하도록 할 수 있습니다.

```php
$this->release(10);

$this->release(now()->addSeconds(10));
```

<a name="manually-failing-a-job"></a>
#### 작업을 수동으로 실패 처리하기

때로는 작업을 직접 "실패"로 처리해야 할 때도 있습니다. 이때는 `fail` 메서드를 호출하면 됩니다.

```php
/**
 * 작업 실행.
 */
public function handle(): void
{
    // ...

    $this->fail();
}
```

작업이 예외 때문에 실패 처리되어야 한다면, 해당 예외를 `fail` 메서드에 전달하세요. 또는, 간편하게 에러 메시지 문자열을 전달해도 예외로 변환되어 처리됩니다.

```php
$this->fail($exception);

$this->fail('무언가 잘못되었습니다.');
```

> [!NOTE]
> 실패한 작업에 관한 자세한 정보는 [작업 실패 처리 문서](#dealing-with-failed-jobs)를 참고하십시오.

<a name="fail-jobs-on-exceptions"></a>
#### 특정 예외 발생 시 작업 실패 처리

`FailOnException` [작업 미들웨어](#job-middleware)를 사용하면, 특정 예외가 발생했을 때 곧바로 재시도를 중단(단락 처리)하고 작업을 실패로 기록할 수 있습니다. 외부 API 오류 등 일시적인(Transient) 예외는 계속 재시도하되, 사용자 권한 철회와 같은 지속적인 예외가 발생하면 작업을 영구적으로 실패 처리하도록 유용합니다.

```php
<?php

namespace App\Jobs;

use App\Models\User;
use Illuminate\Auth\Access\AuthorizationException;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\Middleware\FailOnException;
use Illuminate\Support\Facades\Http;

class SyncChatHistory implements ShouldQueue
{
    use InteractsWithQueue;

    public $tries = 3;

    /**
     * 새 작업 인스턴스 생성.
     */
    public function __construct(
        public User $user,
    ) {}

    /**
     * 작업 실행.
     */
    public function handle(): void
    {
        $user->authorize('sync-chat-history');

        $response = Http::throw()->get(
            "https://chat.laravel.test/?user={$user->uuid}"
        );

        // ...
    }

    /**
     * 작업이 통과해야 할 미들웨어 반환.
     */
    public function middleware(): array
    {
        return [
            new FailOnException([AuthorizationException::class])
        ];
    }
}
```

<a name="job-batching"></a>
## 작업 배치 처리

라라벨의 작업 배치(Job Batching) 기능을 사용하면 여러 작업을 묶어 한 번에 실행하고, 전체 배치가 완료되었을 때 특정 동작을 수행할 수 있습니다. 우선, 각 작업 배치의 진행률 등 메타 정보를 저장할 테이블을 생성하기 위해 데이터베이스 마이그레이션을 만들어야 합니다. 이 마이그레이션은 `make:queue-batches-table` 아티즌 명령어로 생성할 수 있습니다.

```shell
php artisan make:queue-batches-table

php artisan migrate
```

<a name="defining-batchable-jobs"></a>
### 배치로 실행 가능한 작업 정의하기

배치로 실행 가능한 작업을 정의하려면, 일반적인 [대기열 작업 생성](#creating-jobs) 방식으로 작업을 만들고, 여기에 `Illuminate\Bus\Batchable` 트레이트를 추가하십시오. 이 트레이트는 현재 작업이 속한 배치 정보를 확인할 수 있는 `batch` 메서드를 제공합니다.

```php
<?php

namespace App\Jobs;

use Illuminate\Bus\Batchable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ImportCsv implements ShouldQueue
{
    use Batchable, Queueable;

    /**
     * 작업 실행.
     */
    public function handle(): void
    {
        if ($this->batch()->cancelled()) {
            // 배치가 취소되었는지 확인...

            return;
        }

        // CSV 파일의 일부 데이터 가져오기 등...
    }
}
```

<a name="dispatching-batches"></a>
### 배치 작업 디스패치하기

여러 작업을 하나의 배치로 처리하려면, `Bus` 파사드의 `batch` 메서드를 사용하세요. 보통 배치 기능은 완료 콜백과 함께 사용하면 더욱 유용합니다. 따라서 `then`, `catch`, `finally` 등 메서드를 이용하여, 배치 완료 시 호출할 콜백을 정의할 수 있습니다. 각 콜백은 실행 시점에 `Illuminate\Bus\Batch` 인스턴스를 인자로 받습니다. 다음 예시는 CSV 파일 각 영역을 처리하는 여러 작업을 배치로 대기열에 등록하는 경우입니다.

```php
use App\Jobs\ImportCsv;
use Illuminate\Bus\Batch;
use Illuminate\Support\Facades\Bus;
use Throwable;

$batch = Bus::batch([
    new ImportCsv(1, 100),
    new ImportCsv(101, 200),
    new ImportCsv(201, 300),
    new ImportCsv(301, 400),
    new ImportCsv(401, 500),
])->before(function (Batch $batch) {
    // 배치 생성됨, 아직 작업 추가 전...
})->progress(function (Batch $batch) {
    // 개별 작업 하나가 성공적으로 완료됨...
})->then(function (Batch $batch) {
    // 모든 작업이 성공적으로 완료됨...
})->catch(function (Batch $batch, Throwable $e) {
    // 첫 번째 실패 작업 발생 시 처리...
})->finally(function (Batch $batch) {
    // 전체 배치 실행이 끝남...
})->dispatch();

return $batch->id;
```

배치의 ID는 `$batch->id` 속성으로 접근할 수 있으며, 배치 실행 후 [라라벨 명령 버스](#inspecting-batches)에서 추가 정보를 조회하는 데 사용할 수 있습니다.

> [!WARNING]
> 배치 콜백은 직렬화되어 나중에 라라벨 대기열에 의해 실행되기 때문에, 콜백 내에서 `$this` 변수를 사용해서는 안 됩니다. 또한, 배치 작업은 데이터베이스 트랜잭션 내에서 실행되므로, 암묵적으로 커밋을 발생시키는 데이터베이스 명령은 작업 내에서 사용하면 안 됩니다.

<a name="naming-batches"></a>
#### 배치 이름 지정

Laravel Horizon, Laravel Telescope와 같은 일부 도구에서는 배치에 이름을 지정하면 보다 읽기 쉬운 디버그 정보를 제공합니다. 배치에 임의의 이름을 부여하려면, 배치 정의 시 `name` 메서드를 사용하세요.

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // 모든 작업 완료 시 콜백...
})->name('Import CSV')->dispatch();
```

<a name="batch-connection-queue"></a>
#### 배치의 커넥션 및 대기열 지정

배치에 포함된 모든 작업들이 사용할 커넥션과 대기열을 지정하려면 `onConnection`, `onQueue` 메서드를 이용하세요. 모든 배치 작업은 동일한 커넥션과 대기열에서 실행되어야 합니다.

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // 모든 작업 완료 시 콜백...
})->onConnection('redis')->onQueue('imports')->dispatch();
```

<a name="chains-and-batches"></a>
### 체인과 배치의 결합

[체이닝된 작업](#job-chaining) 집합을 하나의 배치 배열에 넣어 병렬로 여러 체인을 실행하고, 모두 완료되었을 때 콜백을 실행할 수 있습니다.

```php
use App\Jobs\ReleasePodcast;
use App\Jobs\SendPodcastReleaseNotification;
use Illuminate\Bus\Batch;
use Illuminate\Support\Facades\Bus;

Bus::batch([
    [
        new ReleasePodcast(1),
        new SendPodcastReleaseNotification(1),
    ],
    [
        new ReleasePodcast(2),
        new SendPodcastReleaseNotification(2),
    ],
])->then(function (Batch $batch) {
    // ...
})->dispatch();
```

반대로, 체인 내부에 배치를 넣어서, 여러 팟캐스트를 먼저 배치로 발행한 다음, 다시 한번 배치로 발행 알림을 보내는 식으로 순차 실행하도록 할 수 있습니다.

```php
use App\Jobs\FlushPodcastCache;
use App\Jobs\ReleasePodcast;
use App\Jobs\SendPodcastReleaseNotification;
use Illuminate\Support\Facades\Bus;

Bus::chain([
    new FlushPodcastCache,
    Bus::batch([
        new ReleasePodcast(1),
        new ReleasePodcast(2),
    ]),
    Bus::batch([
        new SendPodcastReleaseNotification(1),
        new SendPodcastReleaseNotification(2),
    ]),
])->dispatch();
```

<a name="adding-jobs-to-batches"></a>
### 배치에 작업 추가하기

때에 따라, 배치 작업 중 하나에서 실행 중에 추가 작업을 배치에 더하는 것이 유용할 수 있습니다. 수천 개의 작업을 웹 요청에서 직접 한꺼번에 디스패치하는 것이 부담스러울 때, 먼저 "로더" 역할의 작업들을 배치로 등록한 뒤, 이들이 추가 작업을 배치에 하이드레이트(추가)하도록 할 수 있습니다.

```php
$batch = Bus::batch([
    new LoadImportBatch,
    new LoadImportBatch,
    new LoadImportBatch,
])->then(function (Batch $batch) {
    // 모든 작업 완료 시 콜백...
})->name('Import Contacts')->dispatch();
```

위 예시에서는, `LoadImportBatch` 작업을 통해 추가 작업들을 배치에 포함시킵니다. 이를 위해, 각 작업의 `batch` 메서드로 배치 인스턴스를 얻고, `add` 메서드를 이용해 새 작업을 추가할 수 있습니다.

```php
use App\Jobs\ImportContacts;
use Illuminate\Support\Collection;

/**
 * 작업 실행.
 */
public function handle(): void
{
    if ($this->batch()->cancelled()) {
        return;
    }

    $this->batch()->add(Collection::times(1000, function () {
        return new ImportContacts;
    }));
}
```

> [!WARNING]
> 배치에 작업을 추가할 수 있는 시점은, 반드시 해당 배치에 속한 작업 안에서만 가능합니다.

<a name="inspecting-batches"></a>
### 배치 정보 조회하기

배치 완료 콜백 등에서 전달받을 `Illuminate\Bus\Batch` 인스턴스에는, 배치 내 작업들을 조회하고 상호작용할 수 있는 다양한 속성과 메서드가 제공됩니다.

```php
// 배치의 UUID...
$batch->id;

// 배치의 이름(있을 경우)...
$batch->name;

// 배치에 할당된 작업 총 개수...
$batch->totalJobs;

// 아직 실행되지 않은 작업 개수...
$batch->pendingJobs;

// 실패한 작업 개수...
$batch->failedJobs;

// 현재까지 처리된 작업 개수...
$batch->processedJobs();

// 진행률(0-100)...
$batch->progress();

// 배치 실행이 완료됐는지 확인...
$batch->finished();

// 배치 실행 즉시 취소...
$batch->cancel();

// 배치가 취소됐는지 확인...
$batch->cancelled();
```

<a name="returning-batches-from-routes"></a>
#### 라우트에서 배치 정보 반환하기

모든 `Illuminate\Bus\Batch` 인스턴스는 JSON 직렬화가 가능하므로, 애플리케이션의 라우트에서 바로 반환하여 배치의 진행 상황 등 정보를 JSON으로 응답할 수 있습니다. 이를 통해 UI에서 진행률 등 배치의 상태를 쉽게 표시할 수 있습니다.

ID로 배치를 조회하려면, `Bus` 파사드의 `findBatch` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Support\Facades\Bus;
use Illuminate\Support\Facades\Route;

Route::get('/batch/{batchId}', function (string $batchId) {
    return Bus::findBatch($batchId);
});
```

<a name="cancelling-batches"></a>
### 배치 실행 취소하기

특정 배치 실행을 중단해야 할 때는, 해당 `Illuminate\Bus\Batch` 인스턴스의 `cancel` 메서드를 호출하면 됩니다.

```php
/**
 * 작업 실행.
 */
public function handle(): void
{
    if ($this->user->exceedsImportLimit()) {
        return $this->batch()->cancel();
    }

    if ($this->batch()->cancelled()) {
        return;
    }
}
```

이전 예시들에서 볼 수 있듯, 보통 배치 작업은 실행을 이어가기 전에 배치가 취소됐는지 확인하는 것이 좋습니다. 하지만 더 편리하게 사용하려면, 작업에 [SkipIfBatchCancelled 미들웨어](#job-middleware)를 할당할 수도 있습니다. 이름 그대로, 이 미들웨어를 지정하면 관련 배치가 취소된 경우 해당 작업은 실행되지 않습니다.

```php
use Illuminate\Queue\Middleware\SkipIfBatchCancelled;

/**
 * 작업이 통과해야 할 미들웨어 반환.
 */
public function middleware(): array
{
    return [new SkipIfBatchCancelled];
}
```

<a name="batch-failures"></a>
### 배치 실패 처리

배치 내 작업이 실패하면, 혹시 `catch` 콜백이 정의되어 있다면 호출됩니다. 이 콜백은 배치에서 처음으로 실패한 작업에 대해서만 호출됩니다.

<a name="allowing-failures"></a>

#### 실패 허용

일괄 처리(batch) 내에서 하나의 작업이 실패하면, 라라벨은 해당 배치를 자동으로 "취소됨" 상태로 표시합니다. 만약 이 동작을 비활성화하여 작업이 실패하더라도 배치가 자동으로 취소 상태로 전환되지 않게 하고 싶다면, 배치를 디스패치할 때 `allowFailures` 메서드를 호출하면 됩니다.

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // 모든 작업이 성공적으로 완료됨...
})->allowFailures()->dispatch();
```

<a name="retrying-failed-batch-jobs"></a>
#### 실패한 배치 작업 재시도하기

라라벨은 특정 배치의 실패한 작업들을 쉽게 재시도할 수 있도록 `queue:retry-batch` 아티즌 명령어를 제공합니다. 이 명령어는 재시도할 배치의 UUID를 인수로 받습니다.

```shell
php artisan queue:retry-batch 32dbc76c-4f82-4749-b610-a639fe0099b5
```

<a name="pruning-batches"></a>
### 배치 데이터 정리(Pruning)

배치를 정리하지 않으면, `job_batches` 테이블에는 레코드가 매우 빠르게 쌓일 수 있습니다. 이를 방지하려면, [스케줄러](/docs/12.x/scheduling)를 사용해 매일 `queue:prune-batches` 아티즌 명령어가 실행되도록 예약하는 것이 좋습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches')->daily();
```

기본적으로 24시간 이상 지난 모든 완료된 배치가 자동으로 정리됩니다. 이 명령어를 실행할 때 `hours` 옵션을 사용하면, 배치 데이터를 얼마나 오래 보관할지 지정할 수 있습니다. 예를 들어 다음 명령어는 완료된 지 48시간이 지난 모든 배치를 삭제합니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48')->daily();
```

때로는 실패한 작업이 다시 성공적으로 재시도되지 않아 영구적으로 완료되지 못한 배치 레코드가 `jobs_batches` 테이블에 쌓일 수 있습니다. 이럴 때에는 `unfinished` 옵션을 사용해서 해당 미완료 배치 레코드도 정리할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48 --unfinished=72')->daily();
```

마찬가지로, 취소된 배치 레코드 역시 누적될 수 있으므로, `cancelled` 옵션으로 이들 레코드도 별도로 정리할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48 --cancelled=72')->daily();
```

<a name="storing-batches-in-dynamodb"></a>
### DynamoDB에 배치 저장하기

라라벨은 [DynamoDB](https://aws.amazon.com/dynamodb) 내에 배치 메타 정보 저장도 지원합니다(관계형 데이터베이스 대신). 단, 모든 배치 레코드를 저장할 DynamoDB 테이블을 직접 생성해 주어야 합니다.

일반적으로 이 테이블의 이름은 `job_batches`로 설정하지만, 실제로는 애플리케이션의 `queue` 설정 파일 내 `queue.batching.table` 설정 값에 따라 이름을 지정해야 합니다.

<a name="dynamodb-batch-table-configuration"></a>
#### DynamoDB 배치 테이블 설정

`job_batches` 테이블에는 문자열 타입의 파티션 키(`application`)와 문자열 타입의 정렬 키(`id`)가 각각 존재해야 합니다. `application` 키에는 애플리케이션의 `app` 설정 파일 내 `name` 값이 들어가게 됩니다. 애플리케이션 이름이 테이블 키의 일부가 되기 때문에, 여러 라라벨 애플리케이션이 같은 테이블을 공유해도 문제가 없습니다.

또한, [자동 배치 정리](#pruning-batches-in-dynamodb) 기능을 활용하려면 `ttl` 속성(attribute)을 테이블에 추가로 정의할 수 있습니다.

<a name="dynamodb-configuration"></a>
#### DynamoDB 설정

다음으로, 라라벨 애플리케이션이 Amazon DynamoDB와 통신할 수 있도록 AWS SDK를 설치해야 합니다.

```shell
composer require aws/aws-sdk-php
```

그 후, `queue.batching.driver` 설정 값을 `dynamodb`로 지정합니다. 그리고 `batching` 설정 배열 내에 `key`, `secret`, `region` 옵션을 정의해야 하며, 이 값은 AWS와의 인증에 사용됩니다. `dynamodb` 드라이버를 사용하는 경우, `queue.batching.database` 옵션은 필요하지 않습니다.

```php
'batching' => [
    'driver' => env('QUEUE_BATCHING_DRIVER', 'dynamodb'),
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'table' => 'job_batches',
],
```

<a name="pruning-batches-in-dynamodb"></a>
#### DynamoDB에서 배치 정리

[job batch 정보를 DynamoDB에 저장](https://aws.amazon.com/dynamodb)할 경우, 관계형 데이터베이스에 저장된 배치를 정리할 때와 동일한 방식을 사용할 수는 없습니다. 대신 [DynamoDB의 기본 TTL 기능](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html)을 활용해 오래된 배치 레코드를 자동으로 삭제할 수 있습니다.

DynamoDB 테이블에 `ttl` 속성을 정의했다면, 라라벨에서 해당 배치 레코드의 정리 방법을 제어할 수 있는 설정 파라미터를 추가할 수 있습니다. `queue.batching.ttl_attribute`는 TTL이 저장되는 속성의 이름을 정의하며, `queue.batching.ttl`은 레코드가 최종 업데이트된 후 해당 초(seconds)가 지나면 테이블에서 삭제되도록 지정합니다.

```php
'batching' => [
    'driver' => env('QUEUE_FAILED_DRIVER', 'dynamodb'),
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'table' => 'job_batches',
    'ttl_attribute' => 'ttl',
    'ttl' => 60 * 60 * 24 * 7, // 7일...
],
```

<a name="queueing-closures"></a>
## 클로저(Closure) 작업 큐에 등록하기

잡 클래스 대신 클로저(익명 함수)를 큐에 디스패치할 수도 있습니다. 이 방법은 현재 요청 사이클과 별개로, 간단한 작업을 외부에서 빠르게 처리하고 싶을 때 유용합니다. 클로저를 큐에 디스패치할 경우, 클로저 코드의 내용이 암호화로 서명되어 전송 중에 변경될 수 없습니다.

```php
$podcast = App\Podcast::find(1);

dispatch(function () use ($podcast) {
    $podcast->publish();
});
```

작업 큐에 올라간 클로저에 이름을 지정하려면 `name` 메서드를 사용할 수 있습니다. 이 이름은 큐 리포팅 대시보드에서 사용되거나 `queue:work` 명령어의 출력에 표시됩니다.

```php
dispatch(function () {
    // ...
})->name('Publish Podcast');
```

또한, `catch` 메서드를 활용해, 큐에 올라간 클로저가 [설정한 최대 재시도 횟수](#max-job-attempts-and-timeout)만큼 모두 실패했을 때 실행될 클로저를 지정할 수 있습니다.

```php
use Throwable;

dispatch(function () use ($podcast) {
    $podcast->publish();
})->catch(function (Throwable $e) {
    // 이 작업은 실패함...
});
```

> [!WARNING]
> `catch` 콜백은 직렬화되어 나중에 라라벨 큐에서 실행되므로, `catch` 콜백 안에서 `$this` 변수를 사용하면 안 됩니다.

<a name="running-the-queue-worker"></a>
## 큐 워커 실행하기

<a name="the-queue-work-command"></a>
### `queue:work` 명령어

라라벨에는 큐 워커를 실행하여 큐에 새 작업이 들어올 때마다 처리할 수 있는 아티즌 명령어가 포함되어 있습니다. 이 워커는 `queue:work` 명령어로 실행할 수 있습니다. 한 번 시작된 `queue:work` 프로세스는 수동으로 정지시키거나 터미널을 닫기 전까지 계속 실행됩니다.

```shell
php artisan queue:work
```

> [!NOTE]
> `queue:work` 프로세스를 백그라운드에서 항상 실행 상태로 두려면, [Supervisor](#supervisor-configuration)와 같은 프로세스 관리자를 이용하여 큐 워커가 중단되지 않도록 해야 합니다.

실행 중에 `-v` 플래그를 추가하면, 처리되는 작업의 ID, 연결명, 큐 이름이 커맨드 출력에 포함됩니다.

```shell
php artisan queue:work -v
```

큐 워커는 수명(lifetime)이 긴 프로세스이기 때문에, 워커가 시작된 후에는 애플리케이션 코드를 수정해도 실시간 반영되지 않습니다. 따라서 배포(Deploy) 과정 중 [큐 워커를 재시작](#queue-workers-and-deployment)하는 절차가 반드시 포함되어야 합니다. 또한, 애플리케이션에서 만든 모든 static 상태는 작업 간에 자동으로 초기화되지 않는다는 점도 기억해야 합니다.

대신 `queue:listen` 명령어를 실행할 수도 있습니다. 이 명령어를 사용하면 코드 수정 또는 애플리케이션 상태를 재설정하고 싶을 때 워커를 수동으로 재시작할 필요가 없습니다(자동 감지). 그러나 이 방법은 `queue:work`에 비해 효율성이 크게 떨어집니다.

```shell
php artisan queue:listen
```

<a name="running-multiple-queue-workers"></a>
#### 여러 큐 워커 실행하기

하나의 큐에 여러 워커를 할당하여 동시에 작업을 처리하고 싶을 때는, `queue:work` 프로세스를 여러 개 실행하면 됩니다. 이는 터미널의 여러 탭을 통해 로컬에서 실행할 수도 있고, 프로덕션에서는 프로세스 관리자를 통해 설정할 수도 있습니다. [Supervisor를 사용하는 경우](#supervisor-configuration), `numprocs` 설정값을 활용하세요.

<a name="specifying-the-connection-queue"></a>
#### 연결(Connection) 및 큐 지정하기

워커가 사용할 큐 연결 이름도 지정할 수 있습니다. 명령어에 전달하는 연결 이름은 `config/queue.php` 설정 파일에 정의되어 있어야 합니다.

```shell
php artisan queue:work redis
```

`queue:work` 명령어는 기본적으로 해당 연결의 기본 큐에 대해서만 작업을 처리합니다. 다만, 특정 큐만 선택적으로 처리하려면 옵션을 추가로 지정할 수 있습니다. 예를 들어, 모든 이메일 작업이 `redis` 연결의 `emails` 큐에서만 처리된다면, 다음과 같이 입력하여 해당 큐만 처리하는 워커를 실행할 수 있습니다.

```shell
php artisan queue:work redis --queue=emails
```

<a name="processing-a-specified-number-of-jobs"></a>
#### 지정한 개수의 작업만 처리하기

`--once` 옵션을 사용하면 워커가 큐에서 단 하나의 작업만 처리하고 종료하게 할 수 있습니다.

```shell
php artisan queue:work --once
```

`--max-jobs` 옵션은 워커가 지정한 숫자만큼 작업을 완료한 후 종료하도록 합니다. 이 옵션은 [Supervisor](#supervisor-configuration)와 함께 사용하면, 워커가 일정량의 작업을 처리한 후 자동으로 재시작되면서 누적된 메모리를 해제할 수 있어 유용합니다.

```shell
php artisan queue:work --max-jobs=1000
```

<a name="processing-all-queued-jobs-then-exiting"></a>
#### 남아있는 모든 작업을 처리한 후 종료하기

`--stop-when-empty` 옵션은 워커가 남아있는 모든 작업을 처리한 후 정상적으로 종료하도록 합니다. 도커 컨테이너 안에서 라라벨 큐를 처리할 때, 큐가 비워진 후 컨테이너를 종료하고자 할 때 특히 유용합니다.

```shell
php artisan queue:work --stop-when-empty
```

<a name="processing-jobs-for-a-given-number-of-seconds"></a>
#### 지정 시간 동안 작업 처리

`--max-time` 옵션은 워커가 지정된 초(Seconds)만큼 작업을 처리한 후 종료하도록 합니다. 이 옵션도 [Supervisor](#supervisor-configuration)와 함께 사용하면, 워커가 일정 시간마다 자동으로 재시작되어 누적된 메모리 자원을 해제할 수 있습니다.

```shell
# 1시간(3600초) 동안 작업하고 종료...
php artisan queue:work --max-time=3600
```

<a name="worker-sleep-duration"></a>
#### 워커의 대기(Sleep) 시간

큐에 작업이 있을 경우 워커는 지체 없이 연속해서 작업을 처리합니다. 그러나 큐가 비어 있으면, `sleep` 옵션만큼 워커가 "대기"하게 됩니다. 이때 워커는 새로운 작업이 등록될 때까지 아무 작업도 하지 않습니다.

```shell
php artisan queue:work --sleep=3
```

<a name="maintenance-mode-queues"></a>
#### 유지보수 모드와 큐

애플리케이션이 [유지보수 모드](/docs/12.x/configuration#maintenance-mode)인 동안에는, 큐에 등록된 작업이 처리되지 않습니다. 유지보수 모드가 해제되면 작업 처리가 정상적으로 재개됩니다.

유지보수 모드 상태에서도 강제로 큐 작업을 처리하고 싶다면, `--force` 옵션을 사용할 수 있습니다.

```shell
php artisan queue:work --force
```

<a name="resource-considerations"></a>
#### 자원 관리 관련 주의사항

데몬 형태의 큐 워커는 각 작업을 처리하기 전에 프레임워크 자체를 "재부팅"하지 않습니다. 따라서 무거운 리소스를 사용하는 경우에는 각 작업 완료 뒤에 직접 자원을 해제해 주어야 합니다. 예를 들어 GD 라이브러리로 이미지를 처리한다면, 작업이 끝난 뒤에는 `imagedestroy`로 메모리를 반드시 해제해야 합니다.

<a name="queue-priorities"></a>
### 큐 우선순위

가끔 큐의 작업 처리 순위(priority)를 지정하고 싶을 수 있습니다. 예를 들어, `config/queue.php` 설정 파일에서 `redis` 연결의 기본 큐를 `low`로 지정할 수 있습니다. 하지만 특정 작업만 `high` 우선순위 큐에 넣고 싶다면 다음과 같이 지정합니다.

```php
dispatch((new Job)->onQueue('high'));
```

모든 `high` 큐 작업을 먼저 처리한 뒤 `low` 큐 작업을 처리하도록 하려면, 큐 이름을 쉼표로 구분해서 `work` 명령어에 전달할 수 있습니다.

```shell
php artisan queue:work --queue=high,low
```

<a name="queue-workers-and-deployment"></a>
### 큐 워커와 배포(Deployment)

큐 워커는 수명이 긴 프로세스이기 때문에, 코드가 변경되어도 재시작하지 않는 한 변경 사항을 인식하지 못합니다. 따라서 애플리케이션을 배포할 때는 반드시 워커들도 재시작해야 합니다. 모든 워커를 정상적으로 재시작하려면 다음과 같이 `queue:restart` 명령어를 실행하세요.

```shell
php artisan queue:restart
```

이 명령어는 모든 큐 워커에게 현재 진행 중인 작업만 마치고 정상적으로 종료하도록 지시합니다. 덕분에 기존 작업이 손실되지 않습니다. 워커가 종료되면, 프로세스 관리자인 [Supervisor](#supervisor-configuration)와 같은 도구를 이용해 자동으로 워커가 다시 시작되도록 해야 합니다.

> [!NOTE]
> 큐는 [캐시](/docs/12.x/cache)를 이용해 재시작 신호를 저장하므로, 이 기능을 사용하기 전에 애플리케이션에 캐시 드라이버가 제대로 설정되어 있는지 꼭 확인해야 합니다.

<a name="job-expirations-and-timeouts"></a>
### 작업 만료(Job Expiration) 및 타임아웃(Timeout)

<a name="job-expiration"></a>
#### 작업 만료

`config/queue.php` 파일의 각 큐 연결에는 `retry_after` 옵션이 있습니다. 이 값은 작업이 처리 중일 때, 몇 초 후에 다시 시도해야 하는지를 지정합니다. 예를 들어 `retry_after` 값이 90인 경우, 90초 동안 작업이 완료되지 않으면 해당 작업은 큐에서 해제되어 다시 대기열에 올라가게 됩니다. 일반적으로, 이 값은 작업 하나가 완료되기까지의 최대 소요 예상 시간을 기준으로 설정해야 합니다.

> [!WARNING]
> `retry_after` 옵션이 없는 유일한 큐 연결은 Amazon SQS입니다. SQS는 AWS 콘솔에서 설정된 [기본 Visibility Timeout](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/AboutVT.html)을 기준으로 작업을 재시도합니다.

<a name="worker-timeouts"></a>
#### 워커 타임아웃

`queue:work` 아티즌 명령어에는 `--timeout` 옵션이 있습니다. 기본값은 60초입니다. 만약 작업 처리 시간이 타임아웃 값보다 오래 걸리면, 해당 작업을 처리 중이던 워커 프로세스는 에러와 함께 종료됩니다. 보통 [서버에 설정된 프로세스 관리자](#supervisor-configuration)가 워커를 자동으로 재시작합니다.

```shell
php artisan queue:work --timeout=60
```

`retry_after` 설정 값과 CLI의 `--timeout` 옵션은 서로 다르지만, 서로 연동되어 작업이 유실되지 않고 작업이 성공적으로 1회만 처리될 수 있도록 합니다.

> [!WARNING]
> `--timeout` 값은 항상 `retry_after`보다 몇 초는 더 짧게 설정해야 합니다. 이렇게 해야 워커가 정지된 작업을 재시작 전에 safety하게 종료할 수 있습니다. 만약 `--timeout` 값이 `retry_after`보다 길면, 작업이 두 번 처리될 위험이 있습니다.

<a name="supervisor-configuration"></a>
## Supervisor 설정

프로덕션 환경에서는 `queue:work` 프로세스가 항상 실행되도록 해야 합니다. 이 프로세스는 워커 타임아웃이 초과되거나, `queue:restart` 명령어 실행 등 다양한 이유로 중단될 수 있습니다.

따라서, `queue:work`가 중단되었을 때 이를 감지하여 자동으로 재시작할 수 있는 프로세스 모니터(예: Supervisor)가 필요합니다. 프로세스 모니터를 통해 동시에 여러 개의 워커도 관리할 수 있습니다. Supervisor는 리눅스 환경에서 자주 사용되는 대표적인 프로세스 관리 도구이며, 아래에서 Supervisor 설정 방법을 다룹니다.

<a name="installing-supervisor"></a>
#### Supervisor 설치

Supervisor는 리눅스에서 동작하는 프로세스 관리 도구로, 큐 워커가 중단될 때마다 자동으로 재시작해줍니다. Ubuntu에서 Supervisor 설치는 다음과 같이 할 수 있습니다.

```shell
sudo apt-get install supervisor
```

> [!NOTE]
> Supervisor 직접 설치와 관리 과정이 부담스럽다면, 라라벨 큐 워커를 위한 완전 관리형 플랫폼인 [Laravel Cloud](https://cloud.laravel.com) 사용을 고려해볼 수 있습니다.

<a name="configuring-supervisor"></a>
#### Supervisor 설정

Supervisor 설정 파일은 일반적으로 `/etc/supervisor/conf.d` 디렉토리에 위치합니다. 이 폴더에 원하는 만큼 설정 파일을 만들어 다양한 프로세스 감시 방법을 Supervisor에 지시할 수 있습니다. 예를 들어, `laravel-worker.conf` 파일을 생성하여 `queue:work` 프로세스를 Supervisor가 감시하도록 설정하면 다음과 같습니다.

```ini
[program:laravel-worker]
process_name=%(program_name)s_%(process_num)02d
command=php /home/forge/app.com/artisan queue:work sqs --sleep=3 --tries=3 --max-time=3600
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
user=forge
numprocs=8
redirect_stderr=true
stdout_logfile=/home/forge/app.com/worker.log
stopwaitsecs=3600
```

위 예시에서, `numprocs` 값은 Supervisor가 총 8개의 `queue:work` 프로세스를 실행 및 감시하도록 지시합니다. `command` 값은 실제 처리할 큐 연결 및 워커 옵션에 따라 알맞게 수정하세요.

> [!WARNING]
> `stopwaitsecs` 값은 가장 오래 걸리는 작업 처리 예상 시간보다 충분히 커야 합니다. 그렇지 않으면, Supervisor가 작업이 끝나기도 전에 해당 프로세스를 강제로 종료할 수 있습니다.

<a name="starting-supervisor"></a>
#### Supervisor 시작하기

설정 파일을 만들었다면, 다음 명령어들로 Supervisor 설정을 반영하고 프로세스를 시작하세요.

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start "laravel-worker:*"
```

Supervisor에 대한 더 자세한 내용은 [Supervisor 공식 문서](http://supervisord.org/index.html)를 참고하세요.

<a name="dealing-with-failed-jobs"></a>
## 실패한 작업 처리하기

큐에 등록된 작업이 실패할 때도 있습니다. 걱정하지 마세요. 항상 모든 일이 계획대로 진행되는 것은 아닙니다! 라라벨은 [작업 최대 재시도 횟수](#max-job-attempts-and-timeout)를 손쉽게 지정할 수 있게 해주며, 비동기 작업이 이 횟수를 초과해 실패하면 `failed_jobs` 데이터베이스 테이블에 자동으로 기록됩니다. [동기적으로 디스패치한 작업](/docs/12.x/queues#synchronous-dispatching)은 실패 시 별도의 테이블에 저장되지 않고, 예외가 애플리케이션에서 바로 처리됩니다.

라라벨 신규 프로젝트에는 `failed_jobs` 테이블 생성을 위한 마이그레이션이 기본으로 제공됩니다. 만약 이 마이그레이션이 없다면, 다음 명령어로 직접 마이그레이션 파일을 생성할 수 있습니다.

```shell
php artisan make:queue-failed-table

php artisan migrate
```

[큐 워커](#running-the-queue-worker) 프로세스를 실행할 때 `queue:work` 명령어에 `--tries` 옵션을 주면 최대 재시도 횟수를 지정할 수 있습니다. 이 값을 생략하면, 작업 클래스의 `$tries` 속성이 지정한 만큼 또는 자동으로 한 번만 시도됩니다.

```shell
php artisan queue:work redis --tries=3
```

`--backoff` 옵션을 사용하여, 예외 발생 시 재시도 이전에 라라벨이 기다릴 초(seconds)를 지정할 수 있습니다. 기본적으로는 즉시 다시 큐에 올려 재시도합니다.

```shell
php artisan queue:work redis --tries=3 --backoff=3
```

작업별로 재시도 전 대기 시간을 지정하려면, 작업 클래스에 `backoff` 속성을 정의할 수 있습니다.

```php
/**
 * 작업 재시도 전 대기 시간(초)
 *
 * @var int
 */
public $backoff = 3;
```

더 복잡한 재시도 로직이 필요하다면, 작업 클래스 내에 `backoff` 메서드를 구현할 수도 있습니다.

```php
/**
 * 작업 재시도 전 대기 시간(초)을 동적으로 계산
 */
public function backoff(): int
{
    return 3;
}
```

"지수형(exponential)" 백오프(재시도 간격 증가)가 필요하다면, `backoff` 메서드에서 배열을 반환하면 됩니다. 아래 예시에서는 첫 번째 재시도 1초, 두 번째는 5초, 세 번째는 10초, 그 이후는 남은 시도마다 10초씩 대기하게 됩니다.

```php
/**
 * 작업 재시도 전 대기 시간(초), 다단계 지정 가능
 *
 * @return array<int, int>
 */
public function backoff(): array
{
    return [1, 5, 10];
}
```

<a name="cleaning-up-after-failed-jobs"></a>
### 실패한 작업 처리 후 정리

특정 작업이 실패했을 때, 사용자에게 알림을 보내거나, 작업 중 일부만 완료된 상태라면 해당 조치를 되돌리고 싶을 수 있습니다. 이를 위해 작업 클래스에 `failed` 메서드를 정의할 수 있습니다. 이 메서드에는 작업 실패의 원인이 된 `Throwable` 인스턴스가 전달됩니다.

```php
<?php

namespace App\Jobs;

use App\Models\Podcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;
use Throwable;

class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    /**
     * 새 작업 인스턴스를 생성합니다.
     */
    public function __construct(
        public Podcast $podcast,
    ) {}

    /**
     * 작업 실행 메서드.
     */
    public function handle(AudioProcessor $processor): void
    {
        // 업로드된 팟캐스트 처리...
    }

    /**
     * 작업 실패 시 처리 메서드.
     */
    public function failed(?Throwable $exception): void
    {
        // 실패 발생 시 사용자에게 알림 등 처리...
    }
}
```

> [!WARNING]
> `failed` 메서드가 호출되기 전에 작업 인스턴스가 새로 만들어지므로, 기존 `handle` 메서드에서 변경된 클래스 속성 값들은 복원되지 않습니다.

<a name="retrying-failed-jobs"></a>
### 실패한 작업 재시도하기

`failed_jobs` 테이블에 기록된 모든 실패 작업을 확인하려면, 다음과 같이 `queue:failed` 아티즌 명령어를 사용하세요.

```shell
php artisan queue:failed
```

`queue:failed` 명령어는 작업 ID, 연결, 큐 이름, 실패 시간 등 다양한 정보를 보여줍니다. 작업 ID를 활용해 개별 실패 작업을 재시도할 수 있습니다. 예를 들어, ID가 `ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece`인 작업을 재시도하려면 다음과 같이 입력합니다.

```shell
php artisan queue:retry ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece
```

필요하다면 여러 ID를 한 번에 전달할 수도 있습니다.

```shell
php artisan queue:retry ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece 91401d2c-0784-4f43-824c-34f94a33c24d
```

특정 큐의 모든 실패 작업을 재시도하려면 다음과 같이 합니다.

```shell
php artisan queue:retry --queue=name
```

모든 실패 작업을 한 번에 재시도하려면, `queue:retry` 명령어에 `all`을 인수로 사용하세요.

```shell
php artisan queue:retry all
```

개별 실패 작업을 삭제하려면, `queue:forget` 명령어를 사용할 수 있습니다.

```shell
php artisan queue:forget 91401d2c-0784-4f43-824c-34f94a33c24d
```

> [!NOTE]
> [Horizon](/docs/12.x/horizon)을 사용하는 경우, `queue:forget` 대신 `horizon:forget` 명령어를 사용해 실패 작업을 삭제해야 합니다.

`failed_jobs` 테이블의 모든 실패 작업을 삭제하려면, 다음과 같이 `queue:flush` 명령어를 수행합니다.

```shell
php artisan queue:flush
```

<a name="ignoring-missing-models"></a>
### 누락된 모델 무시하기

Eloquent 모델을 작업에 주입할 경우, 모델은 큐에 등록될 때 직렬화되고 작업 처리 시점에 데이터베이스에서 다시 조회됩니다. 하지만 작업이 대기 중인 사이에 해당 모델이 삭제되면, `ModelNotFoundException`과 함께 작업이 실패할 수 있습니다.

이런 경우, 작업 클래스의 `deleteWhenMissingModels` 속성을 `true`로 지정하면, 모델이 없을 경우 해당 작업을 예외 없이 조용히 삭제할 수 있습니다.

```php
/**
 * 모델이 존재하지 않으면 작업을 삭제합니다.
 *
 * @var bool
 */
public $deleteWhenMissingModels = true;
```

<a name="pruning-failed-jobs"></a>
### 실패한 작업 데이터 정리(Pruning Failed Jobs)

`failed_jobs` 테이블에 누적된 실패 기록을 정리하고 싶다면, 다음과 같이 `queue:prune-failed` 아티즌 명령어를 사용하세요.

```shell
php artisan queue:prune-failed
```

이 명령어는 기본적으로 24시간이 지난 실패 기록만 정리합니다. `--hours` 옵션을 지정하면 최근 N시간 내에 생성된 실패 기록만 남기고 그 이전 기록은 모두 삭제됩니다. 예를 들어, 아래 명령은 48시간 이전에 추가된 모든 실패 작업을 삭제합니다.

```shell
php artisan queue:prune-failed --hours=48
```

<a name="storing-failed-jobs-in-dynamodb"></a>
### DynamoDB에 실패 작업 저장하기

라라벨은 관계형 데이터베이스 테이블 대신 [DynamoDB](https://aws.amazon.com/dynamodb)에 실패 작업을 저장하는 것도 지원합니다. 단, 모든 실패 작업 레코드를 저장할 DynamoDB 테이블을 직접 생성해야 합니다. 보통 테이블 이름은 `failed_jobs`로 지정하지만, 실제로는 애플리케이션의 `queue` 설정 중 `queue.failed.table` 값에 이름을 맞추는 것이 좋습니다.

`failed_jobs` 테이블에는 문자열 타입의 파티션 키 `application`과 정렬 키 `uuid`가 각각 필요합니다. `application`에는 현재 애플리케이션의 `app` 설정 파일 내 `name` 값이 들어갑니다. 애플리케이션 이름이 테이블 키의 일부이므로, 여러 라라벨 애플리케이션이 같은 테이블을 공유할 수 있습니다.

추가로, 라라벨 애플리케이션이 Amazon DynamoDB와 통신할 수 있도록 AWS SDK를 설치해야 합니다.

```shell
composer require aws/aws-sdk-php
```

다음으로, `queue.failed.driver` 설정 값을 `dynamodb`로 지정하세요. 그리고 실패 작업 설정 배열 내에 인증용 `key`, `secret`, `region` 값을 지정해야 하며, 이는 AWS 인증에 사용됩니다. `dynamodb` 드라이버를 사용할 때는 `queue.failed.database` 옵션은 필요하지 않습니다.

```php
'failed' => [
    'driver' => env('QUEUE_FAILED_DRIVER', 'dynamodb'),
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'table' => 'failed_jobs',
],
```

<a name="disabling-failed-job-storage"></a>

### 실패한 작업 저장 비활성화

`queue.failed.driver` 설정 옵션 값을 `null`로 지정하면, 라라벨이 실패한 작업을 저장하지 않고 바로 폐기하도록 할 수 있습니다. 일반적으로는 `QUEUE_FAILED_DRIVER` 환경 변수를 통해 이 설정을 적용할 수 있습니다.

```ini
QUEUE_FAILED_DRIVER=null
```

<a name="failed-job-events"></a>
### 실패한 작업 이벤트

작업이 실패할 때 호출되는 이벤트 리스너를 등록하고 싶다면, `Queue` 파사드의 `failing` 메서드를 사용할 수 있습니다. 예를 들어, 라라벨과 함께 제공되는 `AppServiceProvider`의 `boot` 메서드에서 이 이벤트에 클로저를 연결할 수 있습니다.

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Queue;
use Illuminate\Support\ServiceProvider;
use Illuminate\Queue\Events\JobFailed;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Queue::failing(function (JobFailed $event) {
            // $event->connectionName
            // $event->job
            // $event->exception
        });
    }
}
```

<a name="clearing-jobs-from-queues"></a>
## 큐에서 작업 삭제하기

> [!NOTE]
> [Horizon](/docs/12.x/horizon)을 사용하는 경우, `queue:clear` 명령어 대신 `horizon:clear` 명령어를 사용하여 큐의 작업을 삭제해야 합니다.

기본 연결의 기본 큐에 있는 모든 작업을 삭제하려면, 아래와 같이 `queue:clear` Artisan 명령어를 실행하면 됩니다.

```shell
php artisan queue:clear
```

특정 연결 및 큐의 작업을 삭제하고 싶다면, `connection` 인수와 `queue` 옵션을 함께 지정할 수 있습니다.

```shell
php artisan queue:clear redis --queue=emails
```

> [!WARNING]
> 큐에서 작업을 삭제하는 기능은 SQS, Redis, 데이터베이스 큐 드라이버에서만 사용 가능합니다. 또한 SQS의 메시지 삭제는 최대 60초가 소요될 수 있으므로, 큐를 비운 후 60초 이내에 SQS 큐로 전송된 작업도 함께 삭제될 수 있습니다.

<a name="monitoring-your-queues"></a>
## 큐 모니터링하기

큐에 갑자기 많은 작업이 몰리면, 처리 대기 시간이 길어져 큐가 과부하될 수 있습니다. 이럴 때, 라라벨이 큐의 작업 개수가 지정한 임계값을 초과하면 알림을 보내도록 설정할 수 있습니다.

이를 위해 먼저 [매 분마다 실행하도록](/docs/12.x/scheduling) `queue:monitor` 명령어를 스케줄링해야 합니다. 이 명령어는 모니터링하려는 큐 목록과 원하는 작업 개수 임계값을 인수로 받습니다.

```shell
php artisan queue:monitor redis:default,redis:deployments --max=100
```

이 명령어를 스케줄하는 것만으로는 알림이 전송되지 않습니다. 명령어 실행 시 연관된 큐의 작업 개수가 임계값을 초과하면, `Illuminate\Queue\Events\QueueBusy` 이벤트가 발생합니다. 애플리케이션의 `AppServiceProvider`에서 이 이벤트를 리스닝하여, 자신이나 개발팀에 알림을 보낼 수 있습니다.

```php
use App\Notifications\QueueHasLongWaitTime;
use Illuminate\Queue\Events\QueueBusy;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\Facades\Notification;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Event::listen(function (QueueBusy $event) {
        Notification::route('mail', 'dev@example.com')
            ->notify(new QueueHasLongWaitTime(
                $event->connection,
                $event->queue,
                $event->size
            ));
    });
}
```

<a name="testing"></a>
## 테스트

작업을 디스패치하는 코드를 테스트할 때 실제로 작업을 실행하고 싶지 않은 경우가 있을 수 있습니다. 작업의 코드 자체는 별도로 직접 테스트할 수 있으므로, 디스패치 동작만 검증하는 것이 가능합니다. 실제로 작업을 테스트하려면, 테스트에서 해당 작업 인스턴스를 만들고 `handle` 메서드를 직접 호출하면 됩니다.

큐에 푸시되는 작업을 실제로 실행하지 않도록 하려면, `Queue` 파사드의 `fake` 메서드를 사용할 수 있습니다. 이 메서드를 호출한 후에는, 애플리케이션이 큐에 작업을 푸시했는지 등의 검증(assertion)이 가능합니다.

```php tab=Pest
<?php

use App\Jobs\AnotherJob;
use App\Jobs\FinalJob;
use App\Jobs\ShipOrder;
use Illuminate\Support\Facades\Queue;

test('orders can be shipped', function () {
    Queue::fake();

    // Perform order shipping...

    // Assert that no jobs were pushed...
    Queue::assertNothingPushed();

    // Assert a job was pushed to a given queue...
    Queue::assertPushedOn('queue-name', ShipOrder::class);

    // Assert a job was pushed twice...
    Queue::assertPushed(ShipOrder::class, 2);

    // Assert a job was not pushed...
    Queue::assertNotPushed(AnotherJob::class);

    // Assert that a Closure was pushed to the queue...
    Queue::assertClosurePushed();

    // Assert the total number of jobs that were pushed...
    Queue::assertCount(3);
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use App\Jobs\AnotherJob;
use App\Jobs\FinalJob;
use App\Jobs\ShipOrder;
use Illuminate\Support\Facades\Queue;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_orders_can_be_shipped(): void
    {
        Queue::fake();

        // Perform order shipping...

        // Assert that no jobs were pushed...
        Queue::assertNothingPushed();

        // Assert a job was pushed to a given queue...
        Queue::assertPushedOn('queue-name', ShipOrder::class);

        // Assert a job was pushed twice...
        Queue::assertPushed(ShipOrder::class, 2);

        // Assert a job was not pushed...
        Queue::assertNotPushed(AnotherJob::class);

        // Assert that a Closure was pushed to the queue...
        Queue::assertClosurePushed();

        // Assert the total number of jobs that were pushed...
        Queue::assertCount(3);
    }
}
```

`assertPushed` 또는 `assertNotPushed` 메서드에 클로저를 전달하여, 주어진 "참(진리값) 테스트"를 통과하는 작업이 푸시되었는지 검증할 수 있습니다. 테스트 조건을 만족하는 작업이 단 하나라도 있다면, 해당 검증은 성공하게 됩니다.

```php
Queue::assertPushed(function (ShipOrder $job) use ($order) {
    return $job->order->id === $order->id;
});
```

<a name="faking-a-subset-of-jobs"></a>
### 일부 작업만 페이크 처리하기

특정 작업만 페이크로 처리하고, 나머지 작업은 원래대로 실행되도록 하고 싶다면, `fake` 메서드에 페이크로 처리할 작업의 클래스명을 배열로 전달하면 됩니다.

```php tab=Pest
test('orders can be shipped', function () {
    Queue::fake([
        ShipOrder::class,
    ]);

    // Perform order shipping...

    // Assert a job was pushed twice...
    Queue::assertPushed(ShipOrder::class, 2);
});
```

```php tab=PHPUnit
public function test_orders_can_be_shipped(): void
{
    Queue::fake([
        ShipOrder::class,
    ]);

    // Perform order shipping...

    // Assert a job was pushed twice...
    Queue::assertPushed(ShipOrder::class, 2);
}
```

특정 작업을 제외한 모든 작업에 대해 페이크 처리가 필요하다면, `except` 메서드를 사용하면 됩니다.

```php
Queue::fake()->except([
    ShipOrder::class,
]);
```

<a name="testing-job-chains"></a>
### 작업 체인 테스트하기

작업 체인(여러 작업을 연쇄적으로 디스패치하는 기능)을 테스트하려면, `Bus` 파사드의 페이크 기능을 사용해야 합니다. `Bus` 파사드의 `assertChained` 메서드를 사용하면, [작업 체인](/docs/12.x/queues#job-chaining)이 정상적으로 디스패치됐는지 검증할 수 있습니다. `assertChained`는 연결된 작업 배열을 첫 번째 인수로 받습니다.

```php
use App\Jobs\RecordShipment;
use App\Jobs\ShipOrder;
use App\Jobs\UpdateInventory;
use Illuminate\Support\Facades\Bus;

Bus::fake();

// ...

Bus::assertChained([
    ShipOrder::class,
    RecordShipment::class,
    UpdateInventory::class
]);
```

위의 예시처럼 작업 체인 배열에 각 작업의 클래스명을 사용할 수 있습니다. 혹은 실제 작업 인스턴스를 배열로 줄 수도 있는데, 이럴 경우 라라벨은 실제로 디스패치된 작업 체인과 클래스 및 속성값이 일치하는지 확인합니다.

```php
Bus::assertChained([
    new ShipOrder,
    new RecordShipment,
    new UpdateInventory,
]);
```

특정 작업이 체인이 없는 상태(단독으로)로 푸시되는지 검증하려면, `assertDispatchedWithoutChain` 메서드를 사용할 수 있습니다.

```php
Bus::assertDispatchedWithoutChain(ShipOrder::class);
```

<a name="testing-chain-modifications"></a>
#### 체인 변경 사항 테스트하기

체인에 추가로 [작업을 앞쪽이나 뒤쪽에 추가](/docs/12.x/queues#adding-jobs-to-the-chain)하는 경우, 해당 작업에 대해 `assertHasChain` 메서드를 사용하여 남아 있는 작업 체인이 예상과 일치하는지 검증할 수 있습니다.

```php
$job = new ProcessPodcast;

$job->handle();

$job->assertHasChain([
    new TranscribePodcast,
    new OptimizePodcast,
    new ReleasePodcast,
]);
```

남아 있는 작업 체인이 비어 있는지 확인하려면, `assertDoesntHaveChain` 메서드를 사용할 수 있습니다.

```php
$job->assertDoesntHaveChain();
```

<a name="testing-chained-batches"></a>
#### 체인 안의 배치 테스트하기

작업 체인에 [여러 작업이 묶인 배치가 포함된 경우](#chains-and-batches), 체인 검증 코드에 `Bus::chainedBatch` 정의를 추가하여, 체인 내 배치 내용이 기대한 대로인지 검증할 수 있습니다.

```php
use App\Jobs\ShipOrder;
use App\Jobs\UpdateInventory;
use Illuminate\Bus\PendingBatch;
use Illuminate\Support\Facades\Bus;

Bus::assertChained([
    new ShipOrder,
    Bus::chainedBatch(function (PendingBatch $batch) {
        return $batch->jobs->count() === 3;
    }),
    new UpdateInventory,
]);
```

<a name="testing-job-batches"></a>
### 작업 배치 테스트하기

`Bus` 파사드의 `assertBatched` 메서드를 사용하면, [작업 배치](/docs/12.x/queues#job-batching)가 정상적으로 디스패치됐는지 검증할 수 있습니다. `assertBatched`에는 클로저를 인수로 줄 수 있으며, 클로저는 `Illuminate\Bus\PendingBatch` 인스턴스를 인자로 받아 배치 내부 작업을 검사하게 됩니다.

```php
use Illuminate\Bus\PendingBatch;
use Illuminate\Support\Facades\Bus;

Bus::fake();

// ...

Bus::assertBatched(function (PendingBatch $batch) {
    return $batch->name == 'import-csv' &&
           $batch->jobs->count() === 10;
});
```

디스패치된 배치의 개수를 검증하려면 `assertBatchCount` 메서드를 사용할 수 있습니다.

```php
Bus::assertBatchCount(3);
```

디스패치된 배치가 없는지 확인할 때는 `assertNothingBatched` 메서드를 사용합니다.

```php
Bus::assertNothingBatched();
```

<a name="testing-job-batch-interaction"></a>
#### 작업과 배치의 상호작용 테스트

작업이 속한 배치와 어떻게 상호작용하는지를 테스트해야 할 때도 있습니다. 예를 들어, 작업이 배치의 추가 처리를 취소하는 경우가 이에 해당합니다. 이런 경우 `withFakeBatch` 메서드를 통해 작업에 페이크 배치를 할당할 수 있습니다. 이 메서드는 작업 인스턴스와 페이크 배치가 담긴 튜플(배열)을 반환합니다.

```php
[$job, $batch] = (new ShipOrder)->withFakeBatch();

$job->handle();

$this->assertTrue($batch->cancelled());
$this->assertEmpty($batch->added);
```

<a name="testing-job-queue-interactions"></a>
### 작업과 큐 상호작용 테스트

가끔은 큐에 등록된 작업이 [스스로 다시 큐에 반환되는지](#manually-releasing-a-job) 또는 스스로 삭제되는지 등을 테스트하고 싶을 수 있습니다. 이럴 때는 작업 인스턴스를 생성한 후, `withFakeQueueInteractions` 메서드를 호출합니다.

이렇게 하면 큐와의 상호작용이 페이크 처리되며, 이후 해당 작업의 `handle` 메서드를 호출할 수 있습니다. 작업을 실행한 후에는 `assertReleased`, `assertDeleted`, `assertNotDeleted`, `assertFailed`, `assertFailedWith`, `assertNotFailed` 메서드를 사용해 작업과 큐의 상호작용 결과를 검증할 수 있습니다.

```php
use App\Exceptions\CorruptedAudioException;
use App\Jobs\ProcessPodcast;

$job = (new ProcessPodcast)->withFakeQueueInteractions();

$job->handle();

$job->assertReleased(delay: 30);
$job->assertDeleted();
$job->assertNotDeleted();
$job->assertFailed();
$job->assertFailedWith(CorruptedAudioException::class);
$job->assertNotFailed();
```

<a name="job-events"></a>
## 작업 이벤트

`Queue` [파사드](/docs/12.x/facades)의 `before`와 `after` 메서드를 사용해, 큐 작업이 처리되기 전후에 실행될 콜백을 지정할 수 있습니다. 이러한 콜백은 대시보드 통계 집계, 추가 로깅 등 부가 처리를 할 때 유용합니다. 일반적으로는 [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에서 이 메서드를 등록하는 것이 좋습니다. 예를 들어, 다음 예시는 라라벨이 제공하는 `AppServiceProvider`를 사용합니다.

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Queue;
use Illuminate\Support\ServiceProvider;
use Illuminate\Queue\Events\JobProcessed;
use Illuminate\Queue\Events\JobProcessing;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Queue::before(function (JobProcessing $event) {
            // $event->connectionName
            // $event->job
            // $event->job->payload()
        });

        Queue::after(function (JobProcessed $event) {
            // $event->connectionName
            // $event->job
            // $event->job->payload()
        });
    }
}
```

`Queue` [파사드](/docs/12.x/facades)의 `looping` 메서드를 사용하면 워커가 큐에서 작업을 가져오기 전에 실행될 콜백을 지정할 수 있습니다. 예를 들어, 이전에 실패한 작업으로 인해 열린 트랜잭션이 남아있을 경우, 클로저를 등록해 롤백하도록 할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Queue;

Queue::looping(function () {
    while (DB::transactionLevel() > 0) {
        DB::rollBack();
    }
});
```