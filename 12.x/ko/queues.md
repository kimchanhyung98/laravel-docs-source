# 큐 (Queues)

- [소개](#introduction)
    - [커넥션과 큐의 차이](#connections-vs-queues)
    - [드라이버별 참고사항 및 선행조건](#driver-prerequisites)
- [잡 생성](#creating-jobs)
    - [잡 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [유니크 잡](#unique-jobs)
    - [암호화된 잡](#encrypted-jobs)
- [잡 미들웨어](#job-middleware)
    - [속도 제한(Rate Limiting)](#rate-limiting)
    - [잡 중첩 방지](#preventing-job-overlaps)
    - [예외 처리 제한(Throttle)](#throttling-exceptions)
    - [잡 건너뛰기](#skipping-jobs)
- [잡 디스패치](#dispatching-jobs)
    - [지연 디스패치](#delayed-dispatching)
    - [동기식 디스패치](#synchronous-dispatching)
    - [잡과 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [잡 체이닝](#job-chaining)
    - [큐와 커넥션 커스터마이징](#customizing-the-queue-and-connection)
    - [최대 시도 횟수/타임아웃 지정](#max-job-attempts-and-timeout)
    - [SQS FIFO 및 페어 큐](#sqs-fifo-and-fair-queues)
    - [큐 장애 조치(Failover)](#queue-failover)
    - [에러 핸들링](#error-handling)
- [잡 배치 처리](#job-batching)
    - [배치 처리 가능한 잡 정의](#defining-batchable-jobs)
    - [배치 디스패치](#dispatching-batches)
    - [체이닝과 배치](#chains-and-batches)
    - [배치에 잡 추가](#adding-jobs-to-batches)
    - [배치 조회](#inspecting-batches)
    - [배치 취소](#cancelling-batches)
    - [배치 실패](#batch-failures)
    - [배치 데이터 정리(Pruning)](#pruning-batches)
    - [DynamoDB에 배치 저장](#storing-batches-in-dynamodb)
- [클로저의 큐 처리](#queueing-closures)
- [큐 워커 실행](#running-the-queue-worker)
    - [`queue:work` 명령어](#the-queue-work-command)
    - [큐 우선순위](#queue-priorities)
    - [큐 워커와 배포](#queue-workers-and-deployment)
    - [잡 만료 및 타임아웃](#job-expirations-and-timeouts)
- [Supervisor 설정](#supervisor-configuration)
- [실패한 잡 처리](#dealing-with-failed-jobs)
    - [실패한 잡 후처리](#cleaning-up-after-failed-jobs)
    - [실패한 잡 재시도](#retrying-failed-jobs)
    - [존재하지 않는 모델 무시](#ignoring-missing-models)
    - [실패한 잡 정리(Pruning)](#pruning-failed-jobs)
    - [DynamoDB에 실패한 잡 저장](#storing-failed-jobs-in-dynamodb)
    - [실패 잡 저장 비활성화](#disabling-failed-job-storage)
    - [실패한 잡 이벤트](#failed-job-events)
- [큐에서 잡 삭제](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [일부 잡만 페이크](#faking-a-subset-of-jobs)
    - [잡 체인 테스트](#testing-job-chains)
    - [잡 배치 테스트](#testing-job-batches)
    - [잡/큐 상호작용 테스트](#testing-job-queue-interactions)
- [잡 이벤트](#job-events)

<a name="introduction"></a>
## 소개 (Introduction)

웹 애플리케이션을 개발하다 보면, 업로드된 CSV 파일을 파싱해 저장하는 등 일반적인 웹 요청 내에서 처리하기에는 시간이 오래 걸리는 작업이 있을 수 있습니다. 다행히도 Laravel은 이러한 오랜 시간이 소요되는 작업을 백그라운드에서 처리할 수 있도록 큐에 잡을 생성하는 기능을 쉽게 제공합니다. 시간 소모가 큰 작업을 큐로 옮김으로써 애플리케이션은 웹 요청에 매우 빠르게 응답할 수 있고, 사용자 경험도 좋아집니다.

Laravel의 큐는 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 또는 관계형 데이터베이스 등 여러 큐 백엔드를 아우르는 통합된 큐 API를 제공합니다.

큐 관련 설정 옵션은 애플리케이션의 `config/queue.php` 파일에 저장되어 있습니다. 이 파일에는 데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 등 프레임워크가 기본 제공하는 각 큐 드라이버별 커넥션 설정이 있습니다. 또한, 잡을 즉시 실행하는 동기(sync) 드라이버(개발/테스트용)와 큐에 적재된 잡을 버리는 null 드라이버도 포함되어 있습니다.

> [!NOTE]
> Laravel Horizon은 Redis 기반 큐를 위한 뛰어난 대시보드 및 설정 시스템입니다. 더 자세한 정보는 [Horizon 공식 문서](/docs/12.x/horizon)를 참고하세요.

<a name="connections-vs-queues"></a>
### 커넥션과 큐의 차이

Laravel 큐를 본격적으로 사용하기 전에, "커넥션(connection)"과 "큐(queue)"의 차이를 이해하는 것이 중요합니다. `config/queue.php` 파일에는 `connections` 설정 배열이 있습니다. 이 옵션은 Amazon SQS, Beanstalk, Redis 등 백엔드 큐 서비스와의 연결을 정의합니다. 단, 하나의 큐 커넥션 안에서도 여러 개의 "큐"를 둘 수 있는데, 각각은 다른 잡의 스택(stack) 혹은 묶음으로 생각할 수 있습니다.

각 커넥션 설정 예시에는 `queue` 속성이 포함되어 있는데, 이는 해당 커넥션으로 잡을 보낼 때 기본적으로 디스패치되는 큐의 이름입니다. 즉, 잡을 보낼 때 큐를 명시적으로 지정하지 않으면 이 기본 큐에 할당됩니다:

```php
use App\Jobs\ProcessPodcast;

// 이 잡은 기본 커넥션의 기본 큐로 전송됩니다.
ProcessPodcast::dispatch();

// 이 잡은 기본 커넥션의 "emails" 큐로 전송됩니다.
ProcessPodcast::dispatch()->onQueue('emails');
```

한 큐만 사용하는 간단한 애플리케이션도 많지만, 여러 큐에 잡을 분산하는 것은 잡 처리의 우선순위를 세우거나 작업의 처리를 분리하고 싶을 때 특히 유용합니다. Laravel 큐 워커는 처리할 큐의 우선순위도 설정할 수 있습니다. 예를 들어, `high` 큐에 잡을 보내고, 그 큐의 우선처리를 원한다면 아래와 같이 할 수 있습니다:

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버별 참고사항 및 선행조건

<a name="database"></a>
#### 데이터베이스

`database` 큐 드라이버를 사용하려면, 잡을 저장할 데이터베이스 테이블이 필요합니다. 일반적으로 Laravel에 기본 포함된 `0001_01_01_000002_create_jobs_table.php` [마이그레이션](/docs/12.x/migrations)에 이 테이블이 들어있으나, 만약 해당 마이그레이션이 없다면 `make:queue-table` Artisan 명령어로 생성할 수 있습니다:

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면, `config/database.php` 파일에서 Redis 데이터베이스 커넥션을 먼저 설정해야 합니다.

> [!WARNING]
> `serializer` 및 `compression` Redis 옵션은 `redis` 큐 드라이버에서 지원되지 않습니다.

<a name="redis-cluster"></a>
##### Redis 클러스터

Redis 큐 커넥션이 [Redis 클러스터](https://redis.io/docs/latest/operate/rs/databases/durability-ha/clustering)를 사용할 경우, 큐 이름에 [키 해시 태그(hashtags)](https://redis.io/docs/latest/develop/using-commands/keyspace/#hashtags)를 꼭 포함해야 합니다. 그래야 주어진 큐의 모든 Redis 키가 동일한 해시 슬롯에 저장됩니다.

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

Redis 큐에서 `block_for` 설정으로 워커가 새 잡이 들어올 때까지 얼마나 오래 기다릴지 지정할 수 있습니다. 이 값을 적절히 조절하면 Redis 데이터베이스를 반복적으로 폴링하는 것보다 효율적일 수 있습니다. 예를 들어, `5`로 설정하면 잡이 들어올 때까지 5초간 대기합니다.

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
> `block_for`를 `0`으로 설정하면, 워커는 잡이 나올 때까지 무한정 대기합니다. 이 경우 `SIGTERM` 등의 신호를 다음 잡이 처리될 때까지 받을 수 없습니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 선행조건

아래 큐 드라이버를 사용하려면 다음 의존성을 Composer로 설치해야 합니다.

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~2.0` 또는 phpredis PHP 확장
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`

<a name="creating-jobs"></a>
## 잡 생성 (Creating Jobs)

<a name="generating-job-classes"></a>
### 잡 클래스 생성

기본적으로 애플리케이션의 큐 처리 가능한 모든 잡은 `app/Jobs` 디렉터리에 저장됩니다. 해당 디렉터리가 없으면 `make:job` Artisan 명령어 실행 시 자동 생성됩니다.

```shell
php artisan make:job ProcessPodcast
```

생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현합니다. 이 인터페이스는 해당 잡이 큐에서 비동기적으로 실행되어야 함을 Laravel에 알려줍니다.

> [!NOTE]
> 잡 스텁(stub, 뼈대 파일)은 [stub 퍼블리싱](/docs/12.x/artisan#stub-customization) 기능으로 커스터마이징할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조

잡 클래스는 매우 단순하여 보통 큐가 처리할 때 호출되는 `handle` 메서드만 포함합니다. 예시로 팟캐스트 퍼블리싱 서비스에서 업로드된 파일을 처리하는 잡 클래스를 살펴보겠습니다.

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

이 예제에서 보듯이, [Eloquent 모델](/docs/12.x/eloquent)을 큐에 넣을 잡의 생성자에 직접 전달할 수 있습니다. 잡이 `Queueable` 트레이트를 사용하고 있기 때문에, Eloquent 모델과 이미 로딩된 관계 데이터(relationship) 역시 직렬화/역직렬화가 잘 처리됩니다.

큐에 잡을 보낼 때 Eloquent 모델을 받으면, 모델의 식별자만 직렬화된 후 큐에 저장됩니다. 잡이 실제로 처리될 때, 큐 시스템이 데이터베이스에서 모델과 그 연관관계를 자동으로 다시 가져옵니다. 이런 직렬화 방식 덕분에 잡 페이로드가 큐 드라이버에 전달될 때 매우 가볍게 전송됩니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드의 의존성 주입

큐에서 잡을 처리할 때 `handle` 메서드가 호출됩니다. 이 때, `handle` 메서드에 원하는 의존성을 타입힌트로 명시할 수 있으며, [서비스 컨테이너](/docs/12.x/container)가 자동으로 의존성을 주입합니다.

의존성 주입 과정을 직접 커스터마이즈하고 싶으면, 서비스 컨테이너의 `bindMethod` 메서드를 사용할 수 있습니다. 이 메서드는 잡과 컨테이너를 인자로 받아 원하는 방식으로 `handle` 메서드를 호출할 수 있습니다. 보통은 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 호출합니다.

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 바이너리 데이터(예: 원본 이미지 데이터 등)는 잡에 전달하기 전에 반드시 `base64_encode`로 인코딩해야 합니다. 그렇지 않으면 잡 직렬화 과정에서 JSON 변환이 실패할 수 있습니다.

<a name="handling-relationships"></a>
#### 큐잉된 연관관계

모든 로딩된 Eloquent 연관관계도 큐에 잡이 직렬화될 때 저장됩니다. 이 때문에 잡 직렬화 문자열이 매우 커질 수 있으니 주의해야 합니다. 또한, 잡이 역직렬화되어 다시 모델을 읽어올 때 모든 관계가 완전히 로드됩니다. 즉, 잡 큐잉 시 모델에 적용된 전제 조건(쿼리 제약 등)은 잡이 역직렬화될 때 반영되지 않습니다. 따라서, 잡 안에서는 관계를 부분적으로 사용하려면 직접 쿼리 제약을 추가해야 합니다.

관계 데이터 직렬화를 방지하려면, 모델 속성을 설정할 때 `withoutRelations` 메서드를 사용할 수 있습니다. 이 메서드는 관계를 제외한 모델 인스턴스를 반환합니다.

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

[PHP 생성자 속성 승격(Constructor Property Promotion)](https://www.php.net/manual/en/language.oop5.decon.php#language.oop5.decon.constructor.promotion)을 사용한다면, Eloquent 모델의 관계를 직렬화하지 않도록 `WithoutRelations` 속성을 활용할 수 있습니다.

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

여러 모델에 관계 제외 속성을 일일이 붙이기 번거롭다면 클래스 전체에 `WithoutRelations` 속성을 적용할 수도 있습니다.

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

잡이 단일 모델 대신 모델의 컬렉션 또는 배열을 생성자로 받을 경우, 잡이 역직렬화 및 처리될 때 컬렉션 내 모델들은 연관관계가 복원되지 않습니다. 이는 수많은 모델을 처리하는 잡에서 과도한 리소스 사용을 방지하기 위함입니다.

<a name="unique-jobs"></a>
### 유니크 잡

> [!WARNING]
> 유니크 잡은 [락을 지원하는 캐시 드라이버](/docs/12.x/cache#atomic-locks)가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 원자적 락(atomic lock)을 지원합니다.

> [!WARNING]
> 유니크 잡 제한은 배치 내 잡에는 적용되지 않습니다.

특정 잡이 큐에 동시에 한 번만 존재하도록 보장하고 싶을 때는, 잡 클래스에 `ShouldBeUnique` 인터페이스를 구현하면 됩니다. 별도의 메서드를 추가로 정의할 필요는 없습니다.

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

위 예시에서는 `UpdateSearchIndex` 잡이 유니크합니다. 따라서 동일한 잡이 큐에 존재하면서 처리되지 않았다면 중복 디스패치되지 않습니다.

특정 "키"로 유니크함을 판별하거나, 유니크함이 유지되는 최대 시간을 정하고 싶다면 `uniqueId` 및 `uniqueFor` 속성 또는 메서드를 정의할 수 있습니다.

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

이렇게 하면, 동일한 product ID로 새 잡이 디스패치되어도 기존 잡이 끝나기 전까지 무시됩니다. 또, 유니크 락이 1시간 이내 해제되지 않으면 해당 key로 새로운 잡을 다시 큐에 넣을 수 있습니다.

> [!WARNING]
> 잡을 여러 웹 서버나 컨테이너에서 디스패치할 경우, Laravel에서 잡의 유니크함을 정확히 판별하려면 모든 서버가 같은 중앙 캐시 서버를 사용해야 합니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 잡 처리 시작 전까지만 유니크하게 유지

기본적으로 유니크 잡은 처리 완료 또는 모든 재시도 소진 시 "락"이 해제됩니다. 하지만 잡이 처리 시작 직전에 락을 해제하길 원한다면, `ShouldBeUnique` 대신 `ShouldBeUniqueUntilProcessing` 인터페이스를 구현하세요.

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
#### 유니크 잡의 락 처리

내부적으로 `ShouldBeUnique` 잡이 디스패치되면, Laravel은 `uniqueId`를 키로 [락](/docs/12.x/cache#atomic-locks)을 획득하려 시도합니다. 이미 락이 잡혀 있으면 잡은 디스패치되지 않습니다. 락은 잡이 처리 완료되거나 모든 재시도를 소진할 때 해제됩니다. Laravel은 기본 캐시 드라이버를 사용해 락을 관리하지만, 특정 드라이버로 락을 관리하고 싶으면 `uniqueVia` 메서드를 추가하세요.

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
> 단순히 동시 실행을 제한하고 싶을 땐 [WithoutOverlapping](/docs/12.x/queues#preventing-job-overlaps) 잡 미들웨어를 사용하는 것이 더 적합합니다.

<a name="encrypted-jobs"></a>
### 암호화된 잡

잡의 데이터 프라이버시와 무결성을 [암호화](/docs/12.x/encryption)로 보장할 수 있습니다. 잡 클래스에 `ShouldBeEncrypted` 인터페이스만 추가하면, 잡이 큐에 들어가기 전 Laravel이 자동으로 잡을 암호화합니다.

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

잡 미들웨어는 큐잉된 잡의 실행을 감쌀 수 있는 커스텀 로직을 제공합니다. 이를 통해 잡 내부의 반복되는 로직을 줄일 수 있습니다. 예를 들어, Redis 기반 속도 제한을 통해 5초에 한 번씩만 잡을 처리하도록 할 경우:

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

위와 같이 작성할 수도 있지만, `handle` 메서드가 너무 많아지고, 유사한 잡이 있을 때마다 중복 구현해야 합니다. 대신 rate limiting 관련 로직을 별도의 잡 미들웨어로 분리할 수 있습니다.

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

이렇게 경로 미들웨어와 마찬가지로 잡 미들웨어는 현재 처리 중인 잡과 이어서 실행할 콜백을 받습니다.

새 잡 미들웨어 클래스는 `make:job-middleware` Artisan 명령어를 통해 생성할 수 있습니다. 잡에 미들웨어를 적용하려면 잡 클래스에 `middleware` 메서드를 직접 추가하고 배열로 반환하면 됩니다.

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
> 잡 미들웨어는 [큐잉 이벤트 리스너](/docs/12.x/events#queued-event-listeners), [메일](/docs/12.x/mail#queueing-mail), [알림](/docs/12.x/notifications#queueing-notifications) 등에도 적용할 수 있습니다.

<a name="rate-limiting"></a>
### 속도 제한(Rate Limiting)

잡에 대한 속도 제한 미들웨어를 직접 작성할 수도 있지만, Laravel에는 이미 제공되는 미들웨어가 있습니다. [라우트 속도 제한자](/docs/12.x/routing#defining-rate-limiters)와 유사하게, `RateLimiter` 파사드의 `for` 메서드로 잡 속도 제한자를 정의합니다.

예를 들어, 일반 사용자는 시간당 1회만 백업을 허용하고, 프리미엄 고객은 제한을 두지 않을 경우:

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

`perMinute` 메서드로 분 단위 제한도 정의할 수 있습니다. `by` 메서드에는 원하는 값을 넘길 수 있지만, 일반적으로 고객별로 제한하는데 사용됩니다.

```php
return Limit::perMinute(50)->by($job->user->id);
```

속도 제한자를 정의했다면, `Illuminate\Queue\Middleware\RateLimited` 미들웨어로 잡에 적용하면 됩니다. 잡이 속도 제한을 초과하면 미들웨어가 적정 시간(지연 시간) 뒤 다시 잡을 큐에 넣어줍니다.

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

속도 제한으로 잡이 다시 큐에 올라가더라도 총 시도 횟수(`attempts`)는 증가합니다. 필요에 따라 `tries`, `maxExceptions` 속성을 조절하거나 [retryUntil 메서드](#time-based-attempts)로 제한 시간을 별도로 정의할 수 있습니다.

`releaseAfter` 메서드로 잡이 재시도되기까지 대기할 초(sec)를 지정할 수도 있습니다.

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

잡을 속도 제한 시에 재시도하지 않게 하려면 `dontRelease` 메서드를 사용하세요.

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
> Redis를 사용할 때는 `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어를 사용하면, 일반 미들웨어보다 더 효율적으로 동작합니다.

<a name="preventing-job-overlaps"></a>
### 잡 중첩 방지

Laravel의 `Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어를 사용하면, 임의의 키를 기준으로 잡 중첩 실행을 방지할 수 있습니다. 예를 들어, 같은 사용자의 신용점수 업데이트가 중복으로 실행되지 않게 하려면, 잡의 `middleware` 메서드에서 이렇게 작성할 수 있습니다.

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

중복된 잡이 큐에 다시 올라가더라도 시도 횟수는 증가합니다. 디폴트로 `tries`를 1로 두면 중복 잡이 재시도되지 않습니다.

지연을 줄 수도 있습니다:

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

즉시 중복 잡을 삭제하고 싶다면 `dontRelease` 메서드를 사용하세요.

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

`WithoutOverlapping` 미들웨어는 Laravel의 원자적 락 기능을 기반으로 동작합니다. 잡이 비정상적으로 실패하거나 타임아웃이 발생해 락이 풀리지 않을 경우에는, `expireAfter` 메서드로 만료 시간을 명시할 수 있습니다. 예를 들어, 처리 시작 후 3분이 지나면 락 해제를 보장하게 하려면:

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
> `WithoutOverlapping` 미들웨어는 [락을 지원하는 캐시 드라이버](/docs/12.x/cache#atomic-locks)에서만 사용 가능합니다. `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 드라이버가 지원합니다.

<a name="sharing-lock-keys"></a>
#### 잡 클래스 간 락 키 공유

기본적으로, `WithoutOverlapping` 미들웨어는 같은 클래스 내 잡만 중첩을 막습니다. 잡 클래스가 달라도 같은 락 키를 사용하면 중첩을 막고 싶을 때는 `shared` 메서드를 호출하세요.

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
### 예외 처리 제한(Throttle)

`Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어는 잡 실행 중 예외가 일정 횟수 이상 발생하면 잡 재시도를 일정 시간 지연시킵니다. 이는 외부 서비스와 연동되는 불안정한 작업에 유용합니다.

예를 들어, 외부 API와 연동되는 잡에서 예외가 10회 연속 발생하면 5분 대기 후 다시 시도하도록 할 수 있습니다.

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

생성자 첫 번째 인자는 예외 허용 횟수, 두 번째 인자는 제한이 걸렸을 때 기다릴 초 단위 시간입니다.

잡 처리는 예외가 설정치에 도달하기 전까지 즉시 재시도됩니다. 이를 지연시키려면 `backoff` 메서드를 사용하세요.

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

미들웨어는 잡 클래스명을 캐시 "키"로 사용합니다. 여러 잡이 동일 외부 서비스와 연동된다면 `by` 메서드로 동일 제한 버킷을 공유할 수 있습니다.

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

기본적으로 모든 예외가 throttle 처리됩니다. 특정 예외만 throttle 하려면, `when` 메서드에 클로저를 넘기세요.

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

`when`과 다르게, 해당 예외 발생 시 잡을 즉시 삭제하고 싶다면 `deleteWhen` 메서드를 사용합니다.

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

예외를 애플리케이션의 예외 핸들러에 보고(debug)하려면, `report` 메서드를 사용하세요. 클로저를 넘기면 조건부로 예외를 보고할 수 있습니다.

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
> Redis 환경에서는 `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어를 사용하면 성능이 더 좋습니다.

<a name="skipping-jobs"></a>
### 잡 건너뛰기

`Skip` 미들웨어를 사용하면 잡의 내부 로직을 수정하지 않고도 조건에 따라 잡을 건너뛰거나 삭제할 수 있습니다. `Skip::when`(조건이 true면 삭제), `Skip::unless`(조건이 false면 삭제) 메서드를 사용합니다.

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

보다 복잡한 조건이 필요하다면 클로저를 사용할 수도 있습니다.

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

<!-- 나머지 번역은 다음 메시지에서 이어집니다. -->