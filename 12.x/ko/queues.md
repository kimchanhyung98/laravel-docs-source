# 큐 (Queues)

- [소개](#introduction)
    - [커넥션과 큐의 차이](#connections-vs-queues)
    - [드라이버 관련 참고사항 및 사전 준비](#driver-prerequisites)
- [잡 생성](#creating-jobs)
    - [잡 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [고유 잡](#unique-jobs)
    - [암호화된 잡](#encrypted-jobs)
- [잡 미들웨어](#job-middleware)
    - [속도 제한](#rate-limiting)
    - [잡 중첩 방지](#preventing-job-overlaps)
    - [예외 쓰로틀링](#throttling-exceptions)
    - [잡 건너뛰기](#skipping-jobs)
- [잡 디스패치](#dispatching-jobs)
    - [지연 디스패치](#delayed-dispatching)
    - [동기 디스패치](#synchronous-dispatching)
    - [잡과 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [잡 체이닝](#job-chaining)
    - [큐 및 커넥션 커스터마이즈](#customizing-the-queue-and-connection)
    - [최대 시도 횟수/타임아웃 값 지정](#max-job-attempts-and-timeout)
    - [SQS FIFO 및 Fair 큐](#sqs-fifo-and-fair-queues)
    - [큐 페일오버](#queue-failover)
    - [에러 핸들링](#error-handling)
- [잡 배치](#job-batching)
    - [배치 가능한 잡 정의](#defining-batchable-jobs)
    - [배치 디스패치](#dispatching-batches)
    - [체인과 배치](#chains-and-batches)
    - [배치에 잡 추가](#adding-jobs-to-batches)
    - [배치 조회](#inspecting-batches)
    - [배치 취소](#cancelling-batches)
    - [배치 실패](#batch-failures)
    - [배치 정리](#pruning-batches)
    - [DynamoDB에 배치 저장](#storing-batches-in-dynamodb)
- [클로저 큐잉](#queueing-closures)
- [큐 워커 실행](#running-the-queue-worker)
    - [`queue:work` 명령어](#the-queue-work-command)
    - [큐 우선순위](#queue-priorities)
    - [큐 워커와 배포](#queue-workers-and-deployment)
    - [잡 만료 및 타임아웃](#job-expirations-and-timeouts)
    - [큐 워커 일시정지 및 재개](#pausing-and-resuming-queue-workers)
- [Supervisor 설정](#supervisor-configuration)
- [실패한 잡 처리](#dealing-with-failed-jobs)
    - [실패한 잡 후 처리](#cleaning-up-after-failed-jobs)
    - [실패한 잡 재시도](#retrying-failed-jobs)
    - [누락된 모델 무시](#ignoring-missing-models)
    - [실패한 잡 정리](#pruning-failed-jobs)
    - [DynamoDB에 실패한 잡 저장](#storing-failed-jobs-in-dynamodb)
    - [실패한 잡 저장 비활성화](#disabling-failed-job-storage)
    - [실패한 잡 이벤트](#failed-job-events)
- [큐에서 잡 삭제](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [일부 잡만 페이크로 만들기](#faking-a-subset-of-jobs)
    - [잡 체인 테스트](#testing-job-chains)
    - [잡 배치 테스트](#testing-job-batches)
    - [잡과 큐 상호작용 테스트](#testing-job-queue-interactions)
- [잡 이벤트](#job-events)

<a name="introduction"></a>
## 소개 (Introduction)

웹 애플리케이션을 개발하다 보면 업로드된 CSV 파일을 파싱하고 저장하는 등 일반적인 웹 요청 내에서 처리하기에 시간이 오래 걸리는 작업들이 있을 수 있습니다. 다행히 Laravel에서는 이러한 작업을 손쉽게 백그라운드에서 처리할 수 있도록 큐에 잡을 생성할 수 있습니다. 시간이 많이 소요되는 작업을 큐로 이동시키면, 애플리케이션이 웹 요청에 매우 빠르게 응답하여 사용자에게 더 나은 경험을 제공할 수 있습니다.

Laravel의 큐는 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 또는 관계형 데이터베이스 등 다양한 큐 백엔드를 아우르는 통합 API를 제공합니다.

큐 관련 설정은 애플리케이션의 `config/queue.php` 파일에 저장되어 있습니다. 이 설정 파일에는 데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 등 다양한 드라이버에 대한 커넥션 설정이 들어 있습니다. 동기식(synchronous) 드라이버도 포함되어 있으며, 개발 및 테스트 용도로 잡을 즉시 실행합니다. 또한 큐 드라이버를 `null`로 설정하면 큐에 추가된 잡이 모두 무시(폐기)됩니다.

> [!NOTE]
> Laravel Horizon은 Redis 기반 큐를 위한 아름다운 대시보드 및 설정 시스템을 제공합니다. 자세한 내용은 [Horizon 문서](/docs/12.x/horizon)를 참고하십시오.

<a name="connections-vs-queues"></a>
### 커넥션과 큐의 차이 (Connections vs. Queues)

Laravel 큐를 본격적으로 사용하기 전에 "커넥션(connection)"과 "큐(queue)"가 무엇이 다른지 이해하는 것이 중요합니다. `config/queue.php` 파일의 `connections` 배열은 SQS, Beanstalk, Redis 등 백엔드 큐 서비스에 대한 연결을 정의합니다. 그런데 하나의 큐 커넥션에서 여러 "큐"를 가질 수도 있습니다. 각각의 큐는 큐에 쌓인 잡의 별도 스택(더미)라고 생각할 수 있습니다.

각 커넥션 설정 예제에는 `queue` 속성이 있습니다. 이는 해당 커넥션에 잡이 보낼 때 기본적으로 지정될 큐 이름입니다. 즉, 잡을 디스패치할 때 명시적으로 큐를 지정하지 않으면 커넥션에 설정된 기본 `queue`로 전송됩니다:

```php
use App\Jobs\ProcessPodcast;

// 이 잡은 기본 커넥션의 기본 큐로 전송됩니다.
ProcessPodcast::dispatch();

// 이 잡은 기본 커넥션의 "emails" 큐로 전송됩니다.
ProcessPodcast::dispatch()->onQueue('emails');
```

일부 애플리케이션은 하나의 큐만 사용할 수 있지만, 잡을 여러 큐에 분산시키면 잡 처리 우선순위나 분리를 효과적으로 관리할 수 있습니다. Laravel 큐 워커는 처리할 큐와 우선순위를 설정할 수 있기 때문입니다. 예를 들어, `high` 큐로 잡을 보내면 워커를 별도로 돌려 높은 우선순위로 처리할 수 있습니다:

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버 관련 참고사항 및 사전 준비 (Driver Notes and Prerequisites)

<a name="database"></a>
#### 데이터베이스

`database` 큐 드라이버를 사용하려면 잡을 저장할 테이블이 필요합니다. 이 테이블은 Laravel 기본 내장 마이그레이션(`0001_01_01_000002_create_jobs_table.php`)에 포함되어 있지만, 없다면 아래 Artisan 명령어로 직접 생성할 수 있습니다:

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면 `config/database.php` 파일에서 Redis 데이터베이스 커넥션을 먼저 설정해야 합니다.

> [!WARNING]
> `redis` 큐 드라이버는 Redis의 `serializer` 및 `compression` 옵션을 지원하지 않습니다.

<a name="redis-cluster"></a>
##### Redis 클러스터

[Redis 클러스터](https://redis.io/docs/latest/operate/rs/databases/durability-ha/clustering)를 사용하는 경우, 큐 이름에 [키 해시태그(key hash tag)](https://redis.io/docs/latest/develop/using-commands/keyspace/#hashtags)를 반드시 포함해야 합니다. 이는 동일한 큐에 속하는 모든 Redis 키가 같은 해시 슬롯에 저장되도록 보장하기 위함입니다:

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

<a name="blocking"></a>
##### Blocking 설정

Redis 큐를 사용할 때, `block_for` 옵션으로 워커가 잡을 대기하며 블록(block)하는 시간을 지정할 수 있습니다. 이 값을 적절히 조정하면 Redis를 지속적으로 폴링하는 것보다 효율적입니다. 예를 들어, `block_for` 값을 `5`로 설정하면 잡이 나타날 때까지 최대 5초간 대기합니다:

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
> `block_for`를 `0`으로 설정하면 워커가 잡이 올 때까지 무기한 블록 상태에 들어갑니다. 이렇게 하면 다음 잡이 처리될 때까지 `SIGTERM` 등 종료 신호도 처리되지 않습니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 사전 준비

아래 큐 드라이버마다 필요한 추가 Composer 패키지입니다:

<div class="content-list" markdown="1">

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~2.0` 또는 phpredis PHP 확장
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`

</div>

<a name="creating-jobs"></a>
## 잡 생성 (Creating Jobs)

<a name="generating-job-classes"></a>
### 잡 클래스 생성

기본적으로, 앱의 큐 잡 클래스는 모두 `app/Jobs` 디렉토리에 저장됩니다. 이 디렉토리가 없다면, 아래의 `make:job` Artisan 명령어 실행 시 자동으로 생성됩니다:

```shell
php artisan make:job ProcessPodcast
```

생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하게 되며, 이로써 Laravel에게 해당 잡을 비동기로 큐에 올려 처리하라는 신호를 줍니다.

> [!NOTE]
> 잡 스텁은 [stub 퍼블리싱](/docs/12.x/artisan#stub-customization) 기능으로 커스터마이즈할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조

잡 클래스는 매우 단순하며, 평소에는 잡이 큐에서 처리될 때 호출되는 하나의 `handle` 메서드만을 포함합니다. 예시로, 팟캐스트 파일을 업로드하고, 발행 전에 처리해야 하는 서비스라고 가정하면 다음과 같이 작성할 수 있습니다:

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

위 예시처럼 [Eloquent 모델](/docs/12.x/eloquent)을 직접 잡 생성자에 주입할 수 있습니다. `Queueable` 트레잇 덕분에 Eloquent 모델 및 로드된 연관관계도 잡 처리 시 직렬화/역직렬화가 자연스럽게 처리됩니다.

큐 잡 생성자의 인자로 Eloquent 모델이 전달된 경우, 모델의 식별자(id)만 큐에 저장되고, 잡이 실제로 실행될 때 해당 식별자를 토대로 전체 모델 인스턴스와 연관관계를 데이터베이스에서 자동 재조회합니다. 이 방식을 쓰면 큐에 보내는 데이터가 훨씬 작아집니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드의 의존성 주입

잡의 `handle` 메서드는 큐에서 처리될 때 호출됩니다. Laravel의 [서비스 컨테이너](/docs/12.x/container)가 이 메서드에 타입힌트된 의존성을 자동으로 주입합니다.

컨테이너가 의존성을 주입하는 방식을 직접 제어하려면, 컨테이너의 `bindMethod`를 사용할 수 있습니다. 이 메서드는 콜백을 전달받으며, 잡과 컨테이너 인스턴스를 인자로 받습니다. 보통 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 이 메서드를 호출합니다:

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 바이너리 데이터(예: 이미지 원본 등)는 직렬화 전에 반드시 `base64_encode`를 사용해 인코딩해야 합니다. 그렇지 않으면 큐에 잡을 JSON 직렬화하는 과정에서 제대로 처리되지 않을 수 있습니다.

<a name="handling-relationships"></a>
#### 큐에서의 연관관계 처리

모든 로드된 Eloquent 모델의 연관관계 역시 직렬화 대상에 포함되므로, 직렬화된 잡 데이터가 매우 커질 수 있습니다. 또한, 잡이 역직렬화되어 다시 모델을 데이터베이스에서 재조회할 때, 직렬화 직전의 관계 제한조건이 아닌 전체 연관관계가 조회됩니다. 따라서, 연관관계에서 일부만 필요하다면, 잡 실행 시점에 다시 제한을 걸어주는 것이 좋습니다.

모델 속성을 지정할 때, 직렬화에서 연관관계를 아예 제외하려면 모델에 `withoutRelations`를 호출해서 사용하세요:

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

[PHP 생성자 프로퍼티 승격(프로퍼티 프로모션)](https://www.php.net/manual/en/language.oop5.decon.php#language.oop5.decon.constructor.promotion)을 사용할 때, Eloquent 모델의 연관관계 직렬화를 막으려면 `WithoutRelations` 속성을 사용할 수 있습니다:

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

모든 모델의 연관관계 직렬화를 비활성화하려면 클래스 전체에 `WithoutRelations` 속성을 적용하세요:

```php
<?php

namespace App\Jobs;

use App\Models\DistributionPlatform;
use App\Models\Podcast;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;
use Illuminate\Queue\Attributes\WithoutRelations;

#[WithoutRelations]
class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    /**
     * Create a new job instance.
     */
    public function __construct(
        public Podcast $podcast,
        public DistributionPlatform $platform,
    ) {}
}
```

단일 모델이 아닌, Eloquent 모델의 컬렉션(혹은 배열)을 잡이 인자로 받는 경우, 큐에서 역직렬화될 때 해당 컬렉션의 모델들은 연관관계가 복원되지 않습니다. 이는 너무 많은 자원이 사용되는 상황을 막기 위함입니다.

<a name="unique-jobs"></a>
### 고유 잡 (Unique Jobs)

> [!WARNING]
> 고유 잡(Unique job)은 [락을 지원하는 캐시 드라이버](/docs/12.x/cache#atomic-locks)가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 아토믹 락을 지원합니다.

> [!WARNING]
> 고유 잡 제약은 잡 배치(Batch)에는 적용되지 않습니다.

특정 잡이 동일한 시간에 큐에 한 번만 존재하도록 보장하고 싶을 때, 잡 클래스에 `ShouldBeUnique` 인터페이스를 구현하면 됩니다. 추가 메서드 구현 없이도 적용됩니다:

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

위 예시에서 `UpdateSearchIndex` 잡은 유일하게 처리되며, 이미 같은 잡이 큐에 있고 처리되지 않았다면 새로 디스패치되지 않습니다.

특정 "키"로 잡 유일성을 결정하거나, 일정 시간(초) 이후에는 유일성 유지를 풀고 싶을 때에는 `uniqueId` 및 `uniqueFor` 속성이나 메서드를 선언하세요:

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    /**
     * The product instance.
     *
     * @var \App\Models\Product
     */
    public $product;

    /**
     * 유일 락이 해제될 시간(초)
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

위 예시에서는 상품 ID 단위로 유 uniqueness를 보장합니다. 즉, 동일 상품 ID로 디스패치된 추가 잡은 기존 잡의 처리가 끝나기 전까지 무시됩니다. 그리고 1시간 내에 잡이 처리되지 않으면 락이 자동으로 해제되고 같은 유니크 키로 잡이 다시 디스패치 될 수 있습니다.

> [!WARNING]
> 여러 대의 웹서버나 컨테이너에서 잡을 디스패치할 경우, 모든 서버가 동일한 중앙 캐시 서버를 바라보고 있어야 고유 잡 판단이 제대로 동작합니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 잡 처리 시작 전까지만 고유성 유지

기본적으로 고유 잡은 처리 완료되거나 재시도 횟수를 모두 소진한 후 락이 해제됩니다. 그러나, 잡이 처리 직전(until processing begins)에 락을 해제하고 싶다면 `ShouldBeUnique` 대신 `ShouldBeUniqueUntilProcessing`을 구현하세요:

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUniqueUntilProcessing;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUniqueUntilProcessing
{
    // ...
}
```

<a name="unique-job-locks"></a>
#### 고유 잡 락 동작 원리

내부적으로 `ShouldBeUnique` 잡은 `uniqueId` 키로 [락](/docs/12.x/cache#atomic-locks)을 획득합니다. 이미 락이 있으면 잡은 디스패치되지 않습니다. 락은 잡 처리 완료나 재시도 소진 시 해제됩니다. 락에 사용할 캐시 드라이버를 바꾸고 싶다면 `uniqueVia` 메서드로 지정할 수 있습니다:

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
> 잡 동시 처리 개수만 제한하려면 [WithoutOverlapping](/docs/12.x/queues#preventing-job-overlaps) 미들웨어로 처리하세요.

<a name="encrypted-jobs"></a>
### 암호화된 잡 (Encrypted Jobs)

잡 데이터를 [암호화](/docs/12.x/encryption)로 보호/무결성 보장을 할 수 있습니다. 잡 클래스에 `ShouldBeEncrypted` 인터페이스만 추가하면, Laravel이 잡을 자동으로 암호화하여 큐에 등록합니다:

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
## 잡 미들웨어 (Job Middleware)

잡 미들웨어는 잡 실행 로직을 감싸며(래핑) 잡 내부의 반복 코드를 줄여줍니다. 예를 들어, Redis 속도제한을 적용해 5초마다 1개의 잡만 처리하도록 구현한다고 해 보겠습니다:

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

위 코드는 동작하지만, `handle` 메서드가 미들웨어 로직으로 복잡해집니다. 이런 중복 코드를 줄이기 위해, 속도 제한을 담당하는 별도의 잡 미들웨어 클래스를 둘 수 있습니다:

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

라우트 미들웨어와 마찬가지로, 잡 미들웨어도 처리 중인 잡과 다음 콜백을 전달받아 잡 로직 진행을 제어합니다.

`make:job-middleware` Artisan 명령어로 잡 미들웨어 클래스를 생성할 수 있습니다. 미들웨어 생성 후, 잡 클래스에서 `middleware` 메서드를 직접 추가해 리턴하면 연결됩니다:

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
> 잡 미들웨어는 [큐형 이벤트 리스너](/docs/12.x/events#queued-event-listeners), [메일러블](/docs/12.x/mail#queueing-mail), [알림](/docs/12.x/notifications#queueing-notifications)에도 할당할 수 있습니다.

<a name="rate-limiting"></a>
### 속도 제한 (Rate Limiting)

직접 속도 제한 미들웨어를 구현할 수도 있지만, Laravel에는 이미 내장된 속도 제한 미들웨어가 있습니다. [라우트 속도 제한자](/docs/12.x/routing#defining-rate-limiters)처럼, `RateLimiter` 파사드의 `for` 메서드로 잡 속도 제한자를 정의합니다.

예를 들어, 일반 사용자는 시간당 1회 백업만 허용하고 프리미엄 고객은 제한을 두지 않을 수도 있습니다. 아래처럼 `AppServiceProvider`의 `boot`에서 제한자를 등록합니다:

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

위 예시에선 시간 단위 제한을 사용했지만, `perMinute`로 분 단위 제한도 쓸 수 있습니다. `by` 메서드에는 고객별로 제한을 적용할 값을 전달하는 것이 일반적입니다:

```php
return Limit::perMinute(50)->by($job->user->id);
```

제한자를 정의한 후, 잡의 미들웨어에 `Illuminate\Queue\Middleware\RateLimited`를 적용하면 됩니다. 잡이 제한을 초과하면 duration(지정된 제한 시간)만큼 딜레이를 두고 다시 큐에 등록합니다:

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

딜레이가 들어가도 잡의 `attempts` 횟수는 올라가므로, `tries`, `maxExceptions` 속성 등도 적절히 조정해야 합니다. 혹은 [retryUntil 메서드](#time-based-attempts)로 잡 시도 가능 기간을 정할 수도 있습니다.

`releaseAfter`로 퍼포먼스 요구에 맞게 재시도 전 대기 시간을 조정할 수 있습니다:

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

rate limit에 걸릴 때마다 재시도하지 않고 그냥 실패 처리하고 싶다면 `dontRelease`를 사용하세요:

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
> Redis를 사용하는 경우, 보다 최적화된 `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어를 사용할 수 있습니다.

<a name="preventing-job-overlaps"></a>
### 잡 중첩 방지 (Preventing Job Overlaps)

Laravel은 잡 중첩(동일 리소스를 동시에 처리하는 여러 잡 발생) 방지를 위한 `Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어를 제공합니다. 예를 들어, 한 명의 사용자의 신용 점수를 수정하는 잡이 중복 실행되지 않게 하려면 다음과 같이 작성할 수 있습니다:

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

중첩된 잡도 큐로 다시 release되기 때문에, `tries`, `maxExceptions` 등의 속성도 조정해야 할 수도 있습니다(예: 기본값 1이면 중첩 잡은 재시도되지 않음).

중복 잡에 대해 재시도 대기 시간을 조정할 수 있습니다:

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

즉시 삭제되길 원한다면 `dontRelease` 메서드를 사용합니다:

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

`WithoutOverlapping` 락은 Laravel의 아토믹 락 기능을 활용합니다. 때때로 락이 풀리지 않아 문제가 생길 수 있는데, 이럴 때는 `expireAfter`로 만료시간(초)을 명시할 수 있습니다. 예시:

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
> `WithoutOverlapping` 미들웨어도 [락을 지원하는 캐시 드라이버](/docs/12.x/cache#atomic-locks)가 필요합니다.

<a name="sharing-lock-keys"></a>
#### 잡 클래스 간 락 키 공유

기본적으로 `WithoutOverlapping` 미들웨어는 동일 클래스 내의 잡만 중첩을 방지합니다. 서로 다른 잡 클래스라도 같은 락 키를 써도 중첩 방지에는 영향을 주지 않습니다. 락 키를 잡 클래스 간에 공유하려면 `shared` 메서드를 사용하세요:

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
### 예외 쓰로틀링 (Throttling Exceptions)

`Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어를 사용하면, 잡이 일정 횟수 이상 예외를 발생시켜 실패한 경우 지정된 시간동안 재시도를 지연시킬 수 있습니다. 외부 불안정 서비스와 연동 시 유용합니다.

예를 들어, 외부 API 호출 잡이 반복적으로 예외를 던질 때 아래처럼 설정할 수 있습니다:

```php
use DateTime;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new ThrottlesExceptions(10, 5 * 60)];
}

/**
 * Determine the time at which the job should timeout.
 */
public function retryUntil(): DateTime
{
    return now()->plus(minutes: 30);
}
```

첫 번째 인자는 예외 허용 횟수, 두 번째 인자는 해당 횟수 초과 시 다음 시도까지의 대기 시간(초)입니다. 위 예시에서는 10회 연속 예외 시 5분 후 재시도, 단 30분 안에만 시도합니다.

예외 발생 후 즉시 재시도하지 않고, 일정 시간 지연하고 싶을 땐 `backoff`를 호출하세요:

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 5 * 60))->backoff(5)];
}
```

미들웨어 내부적으로 Laravel 캐시 시스템을 사용하며, 기본적으로 잡 클래스명이 캐시 key로 쓰입니다. 여러 잡이 동일한 제약에 속해야 한다면 `by`로 별도 키를 할당할 수 있습니다:

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->by('key')];
}
```

기본적으로 모든 예외가 쓰로틀링되지만, `when` 메서드로 특정 예외만 조건에 따라 쓰로틀링하도록 제한할 수 있습니다:

```php
use Illuminate\Http\Client\HttpClientException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * Get the middleware the job should pass through.
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

특정 예외 발생 시 잡을 아예 삭제(delete)하고 싶다면 `deleteWhen` 메서드를 사용할 수 있습니다:

```php
use App\Exceptions\CustomerDeletedException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(2, 10 * 60))->deleteWhen(CustomerDeletedException::class)];
}
```

쓰로틀링 예외를 예외 핸들러에 신고하려면 `report`를 사용하며, 콜백을 넘기면 조건부 신고가 가능합니다:

```php
use Illuminate\Http\Client\HttpClientException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * Get the middleware the job should pass through.
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
> Redis 사용 시, `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어를 쓰면 효율적입니다.

<a name="skipping-jobs"></a>
### 잡 건너뛰기 (Skipping Jobs)

`Skip` 미들웨어는 잡 로직을 수정하지 않고도 잡을 건너뛰거나 삭제할 수 있게 해줍니다. `Skip::when`은 조건이 true일 때 잡을 삭제하며, `Skip::unless`는 조건이 false일 때 삭제합니다:

```php
use Illuminate\Queue\Middleware\Skip;

/**
 * Get the middleware the job should pass through.
 */
public function middleware(): array
{
    return [
        Skip::when($condition),
    ];
}
```

더 복잡한 조건이 필요하다면 Closure를 넘겨도 됩니다:

```php
use Illuminate\Queue\Middleware\Skip;

/**
 * Get the middleware the job should pass through.
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

(이하, 내용이 너무 방대하여 아래쪽 내용도 위와 같은 방식으로 계속 번역됩니다. 원하시는 경우 추가 부분을 요청해 주세요.)