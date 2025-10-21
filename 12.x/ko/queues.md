# 큐 (Queues)

- [소개](#introduction)
    - [커넥션과 큐의 차이](#connections-vs-queues)
    - [드라이버 관련 주의사항 및 사전 준비](#driver-prerequisites)
- [잡 생성](#creating-jobs)
    - [잡 클래스 생성하기](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [유니크 잡](#unique-jobs)
    - [암호화된 잡](#encrypted-jobs)
- [잡 미들웨어](#job-middleware)
    - [속도 제한](#rate-limiting)
    - [잡 중복 실행 방지](#preventing-job-overlaps)
    - [예외 제한(Throttling Exceptions)](#throttling-exceptions)
    - [잡 스킵(건너뛰기)](#skipping-jobs)
- [잡 디스패치](#dispatching-jobs)
    - [딜레이 디스패치](#delayed-dispatching)
    - [동기식 디스패치](#synchronous-dispatching)
    - [잡과 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [잡 체이닝](#job-chaining)
    - [큐와 커넥션 커스터마이즈](#customizing-the-queue-and-connection)
    - [잡 최대 시도 횟수/타임아웃 지정](#max-job-attempts-and-timeout)
    - [SQS FIFO 및 페어 큐](#sqs-fifo-and-fair-queues)
    - [큐 페일오버](#queue-failover)
    - [에러 핸들링](#error-handling)
- [잡 배치 처리](#job-batching)
    - [배치 가능한 잡 정의](#defining-batchable-jobs)
    - [배치 디스패치](#dispatching-batches)
    - [체인과 배치](#chains-and-batches)
    - [배치에 잡 추가](#adding-jobs-to-batches)
    - [배치 상태 조회](#inspecting-batches)
    - [배치 취소](#cancelling-batches)
    - [배치 실패](#batch-failures)
    - [배치 레코드 정리(Pruning)](#pruning-batches)
    - [DynamoDB에 배치 저장](#storing-batches-in-dynamodb)
- [클로저 큐잉](#queueing-closures)
- [큐 워커 실행](#running-the-queue-worker)
    - [`queue:work` 명령어](#the-queue-work-command)
    - [큐 우선순위 지정](#queue-priorities)
    - [큐 워커와 배포](#queue-workers-and-deployment)
    - [잡 만료 및 타임아웃](#job-expirations-and-timeouts)
- [Supervisor 설정](#supervisor-configuration)
- [실패한 잡 처리](#dealing-with-failed-jobs)
    - [실패한 잡 정리](#cleaning-up-after-failed-jobs)
    - [실패한 잡 재시도](#retrying-failed-jobs)
    - [모델 누락 무시하기](#ignoring-missing-models)
    - [실패한 잡 레코드 정리](#pruning-failed-jobs)
    - [DynamoDB에 실패한 잡 저장](#storing-failed-jobs-in-dynamodb)
    - [실패한 잡 저장 비활성화](#disabling-failed-job-storage)
    - [실패한 잡 이벤트](#failed-job-events)
- [큐에서 잡 삭제](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [특정 잡만 페이크하기](#faking-a-subset-of-jobs)
    - [잡 체인 테스트](#testing-job-chains)
    - [잡 배치 테스트](#testing-job-batches)
    - [잡/큐 상호작용 테스트](#testing-job-queue-interactions)
- [잡 이벤트](#job-events)

<a name="introduction"></a>
## 소개 (Introduction)

웹 애플리케이션을 개발하면서 업로드된 CSV 파일을 파싱해서 저장하는 작업 등, 일반적인 웹 요청 처리 시간 내에 완료되기 힘든 작업들이 있을 수 있습니다. 다행히도, Laravel은 이러한 작업을 백그라운드에서 실행할 수 있도록 큐(Job Queue)를 쉽게 정의할 수 있도록 지원합니다. 시간 소모가 많은 작업을 큐로 분리함으로써, 애플리케이션은 웹 요청에 빠르게 반응하고 사용자에게 더 나은 경험을 제공할 수 있습니다.

Laravel의 큐는 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 관계형 데이터베이스 등 다양한 큐 백엔드에서 공통적인 큐잉 API를 제공합니다.

큐 관련 설정은 애플리케이션의 `config/queue.php` 파일에 저장되어 있습니다. 이 파일에는 데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 등 프레임워크에서 지원하는 각 드라이버별 커넥션 설정이 있습니다. 또한, 개발이나 테스트 시 사용할 수 있는 동기식(synchronous) 드라이버, 그리고 잡을 단순히 폐기하는 `null` 드라이버도 포함되어 있습니다.

> [!NOTE]
> Laravel Horizon은 Redis 기반 큐를 위한 강력한 대시보드 및 설정 시스템입니다. 자세한 내용은 [Horizon 공식 문서](/docs/12.x/horizon)를 참고하세요.

<a name="connections-vs-queues"></a>
### 커넥션과 큐의 차이 (Connections vs. Queues)

Laravel 큐를 사용하기 전에 "커넥션(connection)"과 "큐(queue)"의 차이를 이해하는 것이 중요합니다. `config/queue.php` 파일에는 `connections`라는 설정 배열이 있습니다. 이 옵션은 Amazon SQS, Beanstalk, Redis와 같은 큐 백엔드 서비스로의 연결(커넥션)을 정의합니다. 하지만 하나의 커넥션 아래에 여러 개의 "큐"를 둘 수 있으며, 각각은 별개의 잡 스택처럼 생각할 수 있습니다.

`queue` 설정 파일의 각 커넥션 예시에는 `queue` 속성이 있습니다. 이 속성은 해당 커넥션에서 잡이 디폴트로 디스패치되는 큐를 지정합니다. 즉, 특별히 큐를 지정하지 않고 잡을 디스패치할 경우, 커넥션 설정의 `queue` 속성에 명시된 큐에 잡이 저장됩니다.

```php
use App\Jobs\ProcessPodcast;

// 이 잡은 디폴트 커넥션의 디폴트 큐로 보내집니다...
ProcessPodcast::dispatch();

// 이 잡은 디폴트 커넥션의 "emails" 큐로 보내집니다...
ProcessPodcast::dispatch()->onQueue('emails');
```

대부분의 애플리케이션에서는 큐가 하나만 있어도 충분하지만, 여러 큐로 잡을 분류해서 우선순위 처리 등을 할 때 유용합니다. Laravel 큐 워커는 처리할 큐의 우선순위를 지정할 수 있으므로, `high` 큐에 우선 처리 작업을 넣고, 워커에서 높은 우선순위 큐를 먼저 처리하게 할 수 있습니다.

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버 관련 주의사항 및 사전 준비 (Driver Notes and Prerequisites)

<a name="database"></a>
#### 데이터베이스 (Database)

`database` 큐 드라이버를 사용하려면 잡 정보를 저장할 데이터베이스 테이블이 필요합니다. Laravel 기본 마이그레이션인 `0001_01_01_000002_create_jobs_table.php`에 포함되어 있지만, 없다면 `make:queue-table` Artisan 명령어로 생성할 수 있습니다.

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면 `config/database.php` 파일에서 Redis 데이터베이스 커넥션을 설정해야 합니다.

> [!WARNING]
> `serializer` 및 `compression` Redis 옵션은 `redis` 큐 드라이버에서 지원되지 않습니다.

<a name="redis-cluster"></a>
##### Redis 클러스터

Redis 큐 커넥션이 [Redis Cluster](https://redis.io/docs/latest/operate/rs/databases/durability-ha/clustering)를 사용하는 경우, 큐 이름에 [키 해시 태그](https://redis.io/docs/latest/develop/using-commands/keyspace/#hashtags)를 포함해야 합니다. 이를 통해 동일한 큐의 모든 Redis 키가 같은 해시 슬롯에 저장됩니다.

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
##### 블로킹(Blocking)

Redis 큐 사용 시, `block_for` 설정값으로 잡이 대기열에 나타날 때까지 대기할 최대 시간을 지정할 수 있습니다. 이 값을 조정하면 Redis를 계속 폴링하는 것보다 리소스를 효율적으로 사용할 수 있습니다. 예를 들어, 5초로 지정하면 잡이 없으면 5초간 대기하다가 워커 루프를 반복합니다.

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
> `block_for` 값을 `0`으로 설정하면 잡이 생길 때까지 무한정 대기합니다. 이 경우, `SIGTERM` 같은 신호가 처리되지 않고, 다음 잡을 처리할 때까지 워커가 아무런 반응을 하지 않을 수 있습니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 사전 준비

아래 큐 드라이버에는 다음 의존성이 필요하며, Composer로 설치할 수 있습니다.

<div class="content-list" markdown="1">

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~2.0` 또는 phpredis PHP 확장
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`

</div>

<a name="creating-jobs"></a>
## 잡 생성 (Creating Jobs)

<a name="generating-job-classes"></a>
### 잡 클래스 생성하기 (Generating Job Classes)

애플리케이션의 모든 큐잉 가능한 잡은 기본적으로 `app/Jobs` 디렉토리에 저장됩니다. 해당 디렉토리가 없다면 `make:job` Artisan 명령어를 실행할 때 자동으로 생성됩니다.

```shell
php artisan make:job ProcessPodcast
```

생성된 클래스에는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스가 구현되어 있습니다. 이로 인해 Laravel은 해당 잡을 큐에 넣어 비동기적으로 실행해야 함을 인식합니다.

> [!NOTE]
> 잡 스텁(stub)은 [스텁 퍼블리싱](/docs/12.x/artisan#stub-customization) 기능으로 커스터마이즈할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조 (Class Structure)

잡 클래스는 매우 단순하며, 보통 큐가 작업을 처리할 때 호출하는 `handle` 메서드만 포함합니다. 예시로, 팟캐스트 파일을 게시 전 처리하는 서비스가 있다고 가정하고, 잡 클래스를 만들어 보겠습니다.

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

이 예제에서는 [Eloquent 모델](/docs/12.x/eloquent)을 바로 잡의 생성자에 전달했습니다. 잡에 `Queueable` 트레이트가 포함되어 있으므로, Eloquent 모델 및 로드된 연관관계는 잡이 큐에 저장·처리될 때 자동으로 직렬화 및 역직렬화됩니다.

Eloquent 모델을 잡 생성자로 전달하면, 큐에는 오직 모델 식별자만 직렬화됩니다. 실제 잡이 처리될 때 큐 시스템이 데이터베이스에서 모델 인스턴스 및 관련 연관관계를 다시 조회합니다. 이 방식 덕분에 큐에 실리는 데이터량이 크게 줄어듭니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드의 의존성 주입

잡의 `handle` 메서드는 큐에서 잡을 처리할 때 호출되며, 해당 메서드에 타입힌트로 선언된 의존성은 Laravel [서비스 컨테이너](/docs/12.x/container)를 통해 자동으로 주입됩니다.

의존성 주입 방식을 세밀하게 제어하고 싶다면 서비스 컨테이너의 `bindMethod` 메서드를 사용할 수 있습니다. 이 메서드는 잡과 컨테이너를 인수로 받아서 원하는 방식으로 `handle` 메서드를 호출하도록 할 수 있습니다. 일반적으로 이 코드는 `App\Providers\AppServiceProvider`의 `boot` 메서드에 작성합니다.

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 바이너리 데이터(예: 이미지 원본 데이터)는 잡에 전달하기 전에 반드시 `base64_encode`로 인코딩해야 합니다. 그렇지 않으면 큐에 잡이 JSON으로 직렬화될 때 문제가 발생할 수 있습니다.

<a name="handling-relationships"></a>
#### 큐잉된 연관관계 처리

잡을 큐에 저장할 때 불러온 모든 Eloquent 연관관계도 직렬화되므로, 큐의 직렬화 문자열이 커질 수 있습니다. 또한 잡이 역직렬화되고 모델 연관관계를 DB에서 다시 조회할 때, 원래 직렬화 전 적용됐던 쿼리 제한 조건이 모두 적용되지 않습니다. 원하는 하위집합만 다루고 싶다면 잡 내에서 직접 연관관계 쿼리 제한을 다시 적용해야 합니다.

연관관계를 아예 직렬화하지 않으려면, 속성을 설정할 때 `withoutRelations` 메서드를 호출하면 됩니다. 이 메서드는 연관관계가 제거된 모델 인스턴스를 반환합니다.

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

[PHP 생성자 속성 프로모션](https://www.php.net/manual/en/language.oop5.decon.php#language.oop5.decon.constructor.promotion)을 사용할 때, 모델의 연관관계 직렬화를 방지하려면 `WithoutRelations` 속성을 사용할 수 있습니다.

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

여러 모델 모두 연관관계를 직렬화하지 않으려면, 클래스 전체에 `WithoutRelations` 속성을 적용할 수 있습니다.

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

잡이 단일 모델이 아니라 모델의 컬렉션 또는 배열을 전달받는 경우, 각 모델의 연관관계는 역직렬화 시 복원되지 않습니다. 이는 대량의 모델을 다루는 잡에서 리소스 사용량을 줄이기 위함입니다.

<a name="unique-jobs"></a>
### 유니크 잡 (Unique Jobs)

> [!WARNING]
> 유니크 잡 기능은 [락(atomic lock)](/docs/12.x/cache#atomic-locks)을 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 드라이버가 지원합니다.

> [!WARNING]
> 유니크 잡 제한은 배치 내부의 잡에는 적용되지 않습니다.

특정 잡이 한 번에 큐에 한 인스턴스만 존재하도록 보장하고 싶을 때가 있습니다. 이럴 때 잡 클래스에 `ShouldBeUnique` 인터페이스를 구현하면 됩니다. 추가로 구현해야 할 메서드는 없습니다.

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

위 예시에서, `UpdateSearchIndex` 잡은 유니크합니다. 동일한 잡이 큐에 이미 존재하고 아직 실행이 끝나지 않았다면, 새로운 잡은 디스패치되지 않습니다.

잡의 고유성을 특정 "키"로 지정하거나, 유니크 제한이 해제되는 시간을 지정하고 싶으면 잡 클래스에서 `uniqueId`와 `uniqueFor` 속성(또는 메서드)을 정의할 수 있습니다.

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

위 예시에서는 특정 상품(product)의 ID로 잡의 고유성이 결정됩니다. 같은 product ID로 잡을 여러 번 디스패치하면, 이전 잡 처리 전까진 새 잡이 무시됩니다. 또, 기존 잡이 1시간 내 처리되지 않으면 락이 풀려 동일 키의 새 잡을 다시 디스패치할 수 있습니다.

> [!WARNING]
> 여러 웹 서버/컨테이너 환경에서 잡을 디스패치한다면, 반드시 모든 서버가 동일한 중앙 캐시 서버를 사용하게 하세요. 그래야 유니크 조건이 정확히 유지됩니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 처리 시작 전까지 유니크 유지

기본적으로 유니크 잡은 처리가 끝나거나 모든 재시도 기회를 소진하면 "락"이 해제됩니다. 하지만 잡 실행 직전에 락을 해제하려면 `ShouldBeUnique` 대신 `ShouldBeUniqueUntilProcessing` 인터페이스를 구현하세요.

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
#### 유니크 잡 락

내부적으로 `ShouldBeUnique` 잡이 디스패치될 때 Laravel은 `uniqueId` 값으로 [락](/docs/12.x/cache#atomic-locks)을 시도합니다. 이미 락이 있다면 잡이 디스패치되지 않습니다. 락은 잡이 처리되거나 재시도가 끝나면 풀립니다. 기본적으로 디폴트 캐시 드라이버를 사용하지만, 사용할 드라이버를 바꾸려면 `uniqueVia` 메서드를 구현하세요.

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
> 단순 동시 실행 제한이 필요하다면 [WithoutOverlapping](/docs/12.x/queues#preventing-job-overlaps) 잡 미들웨어를 사용하세요.

<a name="encrypted-jobs"></a>
### 암호화된 잡 (Encrypted Jobs)

Laravel은 [암호화](/docs/12.x/encryption)를 통해 잡의 데이터 기밀성과 무결성을 보장할 수 있습니다. 잡 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하면, 해당 잡은 자동으로 암호화되어 큐에 저장됩니다.

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

잡 미들웨어는 큐잉 잡 실행 시 사용자 정의 로직을 감쌀 수 있도록 하며, 잡 자체 내부 코드를 간결하게 유지할 수 있습니다. 예를 들어, Redis의 속도 제한 기능을 잡의 `handle` 메서드 안에서 직접 사용하는 경우 다음과 같을 수 있습니다.

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

이렇게 하면 `handle` 코드가 길어집니다. 보다 좋은 방법은 별도의 잡 미들웨어로 rate limit 처리를 분리하는 것입니다.

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

라우트 미들웨어처럼, 잡 미들웨어도 처리할 job과 다음 처리를 위한 콜백을 받습니다.

새 잡 미들웨어 클래스는 `make:job-middleware` Artisan 명령어로 생성할 수 있습니다. 미들웨어를 만든 후, 잡의 `middleware` 메서드에서 반환하면 해당 잡에 미들웨어가 적용됩니다. 이 메서드는 기본 잡 스텁에 없으므로 직접 추가해야 합니다.

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
> 잡 미들웨어는 [큐잉 이벤트 리스너](/docs/12.x/events#queued-event-listeners), [메일러블](/docs/12.x/mail#queueing-mail), [노티피케이션](/docs/12.x/notifications#queueing-notifications)에도 적용할 수 있습니다.

<a name="rate-limiting"></a>
### 속도 제한 (Rate Limiting)

직접 작성할 수도 있지만, Laravel에는 잡 속도 제한용 미들웨어가 내장되어 있습니다. [라우트의 rate limiter](/docs/12.x/routing#defining-rate-limiters)와 유사하게, `RateLimiter` 파사드의 `for` 메서드로 정의합니다.

예를 들어, 일반 사용자는 시간당 1회 백업만 허용, 프리미엄 고객은 제한 없음으로 정의할 수 있습니다.

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

분 단위 제한은 `perMinute` 메서드를 사용하면 됩니다. 이때 `by`에는 rate limit을 구별할 값(대개 고객 ID)이 들어갑니다.

```php
return Limit::perMinute(50)->by($job->user->id);
```

정의한 rate limiter를 잡에 적용하려면 `Illuminate\Queue\Middleware\RateLimited` 미들웨어를 사용합니다. rate limit에 걸리면 잡은 정해진 시간 만큼 지연되어 큐에 재삽입됩니다.

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

rate limited로 인해 잡이 지연될 때마다 잡의 `attempts`(시도 횟수)가 증가하므로, 잡 클래스의 `tries`, `maxExceptions` 속성을 적절히 조정해야 합니다. 또는 [retryUntil 메서드](#time-based-attempts)로 시도 제한 시간을 정의할 수 있습니다.

`releaseAfter` 메서드를 사용하면 잡을 다시 시도하기 전까지 대기할 초 단위를 지정할 수 있습니다.

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

rate limit에 걸렸을 때 잡을 아예 재시도하지 않으려면 `dontRelease`를 사용하세요.

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
> Redis를 사용하는 경우, 성능에 최적화된 `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어를 사용할 수 있습니다.

<a name="preventing-job-overlaps"></a>
### 잡 중복 실행 방지 (Preventing Job Overlaps)

`Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어는 임의의 키를 기준으로 동일한 리소스를 여러 잡이 동시에 수정하는 것을 방지할 수 있습니다.

예를 들어, 사용자 신용점수를 업데이트하는 잡이 있다면, 같은 사용자 ID에 대한 잡이 동시에 실행되지 않도록 할 수 있습니다.

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

중복 잡이 큐에 다시 삽입되면, 잡의 시도 횟수(`attempts`)가 증가합니다. 여러 번 시도하게 하려면 클래스의 `tries`, `maxExceptions` 값을 알맞게 조정해야 합니다. 기본값 1로 두면 중복된 잡은 아예 재시도되지 않습니다.

재시도 지연 시간은 `releaseAfter`로 지정할 수 있으며, 즉시 삭제하고 싶다면 `dontRelease`를 사용할 수 있습니다.

```php
// 60초 후 재시도
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->releaseAfter(60)];
}

// 아예 중복 잡 삭제
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->dontRelease()];
}
```

락이 풀리지 않아 중복 방지가 무한정 지속되는 상황을 방지하려면, `expireAfter`로 락 만료시간(초)을 지정할 수 있습니다.

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->expireAfter(180)];
}
```

> [!WARNING]
> 해당 미들웨어는 [락](/docs/12.x/cache#atomic-locks)을 지원하는 캐시 드라이버에서만 작동합니다. `memcached`, `redis`, `dynamodb`, `database`, `file`, `array`가 지원합니다.

<a name="sharing-lock-keys"></a>
#### 여러 잡 클래스에서 락 키 공유

기본적으로, `WithoutOverlapping` 미들웨어는 같은 클래스의 잡들에만 중복 방지를 적용합니다. 여러 잡 클래스가 같은 락 키를 써도 기본적으로는 중복 방지 적용되지 않습니다. 모든 잡 클래스간 락 키를 공유하려면 `shared` 메서드를 사용하세요.

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
### 예외 제한 (Throttling Exceptions)

`Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어를 사용하면 잡 실행 시 반복적으로 발생하는 예외의 개수를 제한해서, 일정 횟수 이상 예외가 발생하면 잡 실행을 지연시킬 수 있습니다. 주로 외부 API 등 불안정한 서비스와 통신 시 유용합니다.

예를 들어, 10회 연속 예외 발생 시 5분간 대기하다가 재시도하도록 할 수 있습니다.

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
    return now()->addMinutes(30);
}
```

`ThrottlesExceptions` 미들웨어의 첫 번째 인수는 허용할 예외 발생 횟수, 두 번째는 제한 시 대기할 초(seconds) 단위 시간입니다.

예외 임계치에 도달하지 않은 예외가 발생하면, 기본적으로 즉시 다시 시도합니다. 이때 지연을 주고 싶으면 `backoff` 메서드로 분 단위 지연시간을 지정하세요.

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 5 * 60))->backoff(5)];
}
```

잡 클래스명으로 캐시 키가 생성되는데, 여러 잡 클래스가 동일 외부 서비스와 통신한다면, `by` 메서드로 동일한 키를 직접 정의할 수 있습니다.

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->by('key')];
}
```

모든 예외를 제한하지 않고, 특정 조건의 예외만 제한하려면 `when` 메서드를 사용합니다.

```php
use Illuminate\Http\Client\HttpClientException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->when(
        fn (Throwable $throwable) => $throwable instanceof HttpClientException
    )];
}
```

특정 예외가 발생하면 해당 잡을 아예 삭제하고 싶다면 `deleteWhen` 메서드를 사용하세요.

```php
use App\Exceptions\CustomerDeletedException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [(new ThrottlesExceptions(2, 10 * 60))->deleteWhen(CustomerDeletedException::class)];
}
```

예외 리미트에 걸렸을 때만 예외를 애플리케이션 예외 핸들러에 보고하려면, `report` 메서드에 조건을 전달하세요.

```php
use Illuminate\Http\Client\HttpClientException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->report(
        fn (Throwable $throwable) => $throwable instanceof HttpClientException
    )];
}
```

> [!NOTE]
> Redis를 사용하는 경우, `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어가 더 효율적입니다.

<a name="skipping-jobs"></a>
### 잡 스킵(건너뛰기) (Skipping Jobs)

`Skip` 미들웨어는 별도의 로직 없이, 특정 조건에 따라 잡을 건너뛰고 삭제할 수 있습니다. `Skip::when`은 조건이 true이면 잡을 삭제하며, `Skip::unless`는 false일 때 잡을 삭제합니다.

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

더 복잡한 조건식이 필요하다면, 클로저를 사용할 수도 있습니다.

```php
use Illuminate\Queue\Middleware\Skip;

public function middleware(): array
{
    return [
        Skip::when(function (): bool {
            return $this->shouldSkip();
        }),
    ];
}
```
(이후 내용은 요청 시 추가로 번역해 드릴 수 있습니다)
