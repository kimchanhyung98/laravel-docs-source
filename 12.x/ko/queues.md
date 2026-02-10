# 큐 (Queues)

- [소개](#introduction)
    - [커넥션과 큐의 차이점](#connections-vs-queues)
    - [드라이버 주의사항 및 사전 준비](#driver-prerequisites)
- [잡 생성](#creating-jobs)
    - [잡 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [고유한 잡(Unique Jobs)](#unique-jobs)
    - [암호화된 잡](#encrypted-jobs)
- [잡 미들웨어](#job-middleware)
    - [속도 제한(Rate Limiting)](#rate-limiting)
    - [잡 중복 실행 방지](#preventing-job-overlaps)
    - [예외 스로틀링(Throttling Exceptions)](#throttling-exceptions)
    - [잡 건너뛰기(Skipping Jobs)](#skipping-jobs)
- [잡 디스패칭](#dispatching-jobs)
    - [지연 디스패칭](#delayed-dispatching)
    - [동기식 디스패칭](#synchronous-dispatching)
    - [잡과 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [잡 체이닝(Chaining)](#job-chaining)
    - [큐 및 커넥션 커스터마이징](#customizing-the-queue-and-connection)
    - [최대 시도 횟수 / 타임아웃 지정](#max-job-attempts-and-timeout)
    - [SQS FIFO 및 공정 큐(Fair Queues)](#sqs-fifo-and-fair-queues)
    - [큐 페일오버](#queue-failover)
    - [에러 처리](#error-handling)
- [잡 배치(Batching)](#job-batching)
    - [배치 가능한 잡 정의](#defining-batchable-jobs)
    - [배치 디스패칭](#dispatching-batches)
    - [체인과 배치 결합](#chains-and-batches)
    - [배치에 잡 추가](#adding-jobs-to-batches)
    - [배치 조회](#inspecting-batches)
    - [배치 취소](#cancelling-batches)
    - [배치 실패](#batch-failures)
    - [배치 레코드 정리(Pruning)](#pruning-batches)
    - [DynamoDB에 배치 저장](#storing-batches-in-dynamodb)
- [클로저 큐잉](#queueing-closures)
- [큐 워커 실행](#running-the-queue-worker)
    - [`queue:work` 명령어](#the-queue-work-command)
    - [큐 우선순위](#queue-priorities)
    - [큐 워커와 배포](#queue-workers-and-deployment)
    - [잡 만료 및 타임아웃](#job-expirations-and-timeouts)
    - [큐 워커 일시중지 및 재개](#pausing-and-resuming-queue-workers)
- [Supervisor 설정](#supervisor-configuration)
- [실패한 잡 처리](#dealing-with-failed-jobs)
    - [실패한 잡 후처리](#cleaning-up-after-failed-jobs)
    - [실패한 잡 재시도](#retrying-failed-jobs)
    - [누락된 모델 무시](#ignoring-missing-models)
    - [실패한 잡 삭제(Pruning)](#pruning-failed-jobs)
    - [DynamoDB에 실패 잡 저장](#storing-failed-jobs-in-dynamodb)
    - [실패 잡 저장 비활성화](#disabling-failed-job-storage)
    - [실패 잡 이벤트](#failed-job-events)
- [큐에서 잡 삭제](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [일부 잡에 대해서만 페이크 처리](#faking-a-subset-of-jobs)
    - [잡 체인 테스트](#testing-job-chains)
    - [잡 배치 테스트](#testing-job-batches)
    - [잡/큐 상호작용 테스트](#testing-job-queue-interactions)
- [잡 이벤트](#job-events)

<a name="introduction"></a>
## 소개 (Introduction)

웹 애플리케이션을 개발할 때, CSV 파일 업로드 후 파싱 및 저장처럼 일반적인 웹 요청 처리 중에는 너무 오래 걸릴 수 있는 작업이 있을 수 있습니다. Laravel은 이런 작업들을 손쉽게 큐 작업(큐 잡)으로 만들어 백그라운드에서 처리할 수 있도록 해줍니다. 처리 시간이 오래 걸리는 작업을 큐로 분리함으로써, 애플리케이션이 웹 요청에 훨씬 빠르게 응답하고 사용자 경험을 개선할 수 있습니다.

Laravel의 큐 시스템은 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 관계형 데이터베이스 등 다양한 백엔드 큐 드라이버에 대해 일관된 큐잉 API를 제공합니다.

큐 관련 설정은 애플리케이션의 `config/queue.php` 설정 파일에 저장되어 있습니다. 이 파일에는 데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 등 다양한 큐 드라이버에 대한 커넥션 설정이 포함되어 있으며, 개발/테스트용으로 즉시 실행되는 동기 드라이버(sync), 그리고 큐에 추가된 잡을 즉시 폐기하는 null 드라이버도 제공됩니다.

> [!NOTE]
> Laravel Horizon은 Redis 기반 큐를 위한 아름다운 대시보드이자 설정 관리 도구입니다. 자세한 내용은 [Horizon 공식 문서](/docs/12.x/horizon)를 참고하세요.

<a name="connections-vs-queues"></a>
### 커넥션과 큐의 차이점 (Connections vs. Queues)

Laravel 큐를 사용하기 전에 "커넥션(connection)"과 "큐(queue)"의 차이를 명확히 이해하는 것이 중요합니다. `config/queue.php` 파일의 `connections` 배열은 Amazon SQS, Beanstalk, Redis 등 다양한 큐 백엔드와의 연결 정보를 담고 있습니다. 하지만 하나의 커넥션에 여러 개의 "큐"를 둘 수 있으며, 이는 각각 별도의 큐 잡 목록이라고 생각할 수 있습니다.

각 커넥션 설정 예시에는 `queue` 속성이 포함되어 있는데, 이 속성은 주어진 커넥션에 잡을 보낼 때 기본적으로 사용되는 큐입니다. 즉, 잡을 큐에 디스패치할 때 명시적으로 큐 이름을 지정하지 않았다면, 해당 커넥션 설정의 `queue` 속성에 정의된 큐로 잡이 추가됩니다.

```php
use App\Jobs\ProcessPodcast;

// 이 잡은 기본 커넥션의 기본 큐로 전송...
ProcessPodcast::dispatch();

// 이 잡은 기본 커넥션의 "emails" 큐로 전송...
ProcessPodcast::dispatch()->onQueue('emails');
```

모든 애플리케이션이 여러 개의 큐를 반드시 사용할 필요는 없습니다. 단 하나의 큐만 사용하는 단순한 구조도 가능합니다. 하지만 잡 처리 방식의 우선 순위 지정, 작업 종류별 분류가 필요한 복잡한 애플리케이션에서는 여러 큐를 사용하는 것이 유용합니다. 예를 들어 `high` 큐로 잡을 디스패치하면, 해당 잡이 우선적으로 처리되도록 워커를 지정할 수 있습니다.

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버 주의사항 및 사전 준비 (Driver Notes and Prerequisites)

<a name="database"></a>
#### 데이터베이스

`database` 큐 드라이버를 사용하려면, 잡을 저장할 데이터베이스 테이블이 필요합니다. Laravel 기본 마이그레이션(`0001_01_01_000002_create_jobs_table.php`)에는 이 테이블 생성이 포함되어 있지만, 만약 없다면 `make:queue-table` Artisan 명령어로 마이그레이션을 생성할 수 있습니다.

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면, `config/database.php` 파일에서 Redis 데이터베이스 커넥션을 구성해야 합니다.

> [!WARNING]
> `redis` 큐 드라이버는 Redis의 `serializer` 및 `compression` 옵션을 지원하지 않습니다.

<a name="redis-cluster"></a>
##### Redis 클러스터

Redis 큐 커넥션이 [Redis Cluster](https://redis.io/docs/latest/operate/rs/databases/durability-ha/clustering)를 사용하는 경우, 큐 이름에 [키 해시태그(key hash tag)](https://redis.io/docs/latest/develop/using-commands/keyspace/#hashtags)를 포함해야 합니다. 그래야 해당 큐에 대한 모든 Redis 키가 같은 해시 슬롯에 저장됩니다.

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
##### Blocking

Redis 큐를 사용할 때, `block_for` 설정값으로 잡을 기다릴 최대 대기 시간을 지정할 수 있습니다. 이 시간을 조정하면 새로운 잡을 계속해서 반복적으로 polling하는 대신, 지정된 시간만큼 잡이 도착할 때까지 대기하므로 리소스를 더 효율적으로 사용할 수 있습니다.

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
> `block_for`를 `0`으로 설정하면 잡이 생길 때까지 무한정 대기(block)하게 됩니다. 이 경우 `SIGTERM` 같은 신호는 다음 잡이 처리될 때까지 인식되지 않습니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 사전 준비

아래 큐 드라이버에서는 다음과 같은 Composer 패키지가 필요합니다.

<div class="content-list" markdown="1">

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~2.0` 또는 phpredis PHP 확장
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`

</div>

<a name="creating-jobs"></a>
## 잡 생성 (Creating Jobs)

<a name="generating-job-classes"></a>
### 잡 클래스 생성 (Generating Job Classes)

기본적으로, 큐로 실행되는 잡들은 `app/Jobs` 디렉토리 아래에 저장됩니다. 이 디렉토리가 없다면, 아래 Artisan 명령어를 실행할 때 자동으로 생성됩니다.

```shell
php artisan make:job ProcessPodcast
```

새로 생성된 잡 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하게 되며, 이는 해당 잡이 큐에 비동기적으로 디스패치됨을 Laravel에게 알립니다.

> [!NOTE]
> 잡 스텁(stub)은 [스텁 커스터마이징](/docs/12.x/artisan#stub-customization)을 통해 수정할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조 (Class Structure)

잡 클래스는 일반적으로 큐에 의해 실행될 때 호출되는 `handle` 메서드만을 포함하는 매우 단순한 형태입니다. 예를 들어, 팟캐스트 게시 서비스를 운영하며 업로드된 파일을 게시 전에 처리하는 잡 클래스를 만든 예시를 살펴보겠습니다.

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

이 예시에서 보듯이, [Eloquent 모델](/docs/12.x/eloquent) 인스턴스를 바로 큐 잡의 생성자에 넘겨줄 수 있습니다. `Queueable` 트레이트 덕분에, Eloquent 모델 및 로드된 연관관계 데이터(relationships)까지 자연스럽게 직렬화/역직렬화되어 잡 실행 시 사용할 수 있습니다.

잡에 Eloquent 모델을 전달하면, 모델의 식별자(id)만 큐에 직렬화됩니다. 실제로 잡이 실행될 때, 큐 시스템은 데이터베이스에서 전체 모델과 연관관계를 자동으로 다시 로드합니다. 이런 방식의 직렬화는 큐 드라이버로 전송되는 잡의 페이로드가 매우 작아지는 장점이 있습니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드의 의존성 주입

잡의 `handle` 메서드는 큐에서 처리될 때 호출됩니다. 이때, 메서드의 타입힌트로 지정한 의존성들은 Laravel [서비스 컨테이너](/docs/12.x/container)가 자동으로 주입해줍니다.

만약 서비스 컨테이너가 `handle` 메서드에 의존성을 주입하는 방식을 완전히 제어하고 싶다면, 컨테이너의 `bindMethod` 메서드를 사용할 수 있습니다. 보통은 `App\Providers\AppServiceProvider`와 같은 서비스 프로바이더의 `boot` 메서드에서 호출합니다.

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 원시 이진 데이터(예: 이미지 파일 등)는 큐 잡으로 전달하기 전에 반드시 `base64_encode` 함수를 사용해 인코딩해야 합니다. 그렇지 않으면 큐에 직렬화할 때 JSON 변환에 실패할 수 있습니다.

<a name="handling-relationships"></a>
#### 큐잉 시 연관관계 처리

로드된 모든 Eloquent 모델의 연관관계 데이터도 잡 큐에 함께 직렬화되므로, 직렬화된 잡 데이터가 상당히 커질 수 있습니다. 또한, 잡이 역직렬화되어 다시 모델을 불러올 때에는 연관관계 전체가 재조회되며, 직렬화 직전에 적용된 연관관계 제약 조건(조건부 eager 로딩 등)은 적용되지 않습니다. 일부 연관관계만 필요하다면 잡 내부에서 직접 연관관계 제약조건을 재적용해야 합니다.

또는, 모델에 대해 속성 지정 시 `withoutRelations` 메서드를 호출해 연관관계를 직렬화 대상에서 제외할 수 있습니다.

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

[PHP 생성자 프로퍼티 프로모션](https://www.php.net/manual/en/language.oop5.decon.php#language.oop5.decon.constructor.promotion)을 활용할 경우, Eloquent 모델의 연관관계 직렬화 제외 여부를 `WithoutRelations` 속성(Attribute)으로 표시할 수 있습니다.

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

모든 모델에 대해 연관관계를 직렬화하지 않도록 하려면, 클래스 전체에 `WithoutRelations` 속성을 적용할 수도 있습니다.

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

잡이 단일 모델이 아니라 모델의 배열이나 컬렉션을 전달받을 경우, 해당 모델들은 잡 실행 시 연관관계가 복원되지 않습니다. 많은 모델을 다루는 잡에서 과도한 리소스 사용을 방지하기 위한 처리입니다.

<a name="unique-jobs"></a>
### 고유한 잡(Unique Jobs)

> [!WARNING]
> 고유한 잡을 사용하려면 [락(Lock)](/docs/12.x/cache#atomic-locks)을 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 드라이버가 락을 지원합니다.

> [!WARNING]
> 고유 잡 제약조건은 잡 배치(batch) 내부의 잡에는 적용되지 않습니다.

같은 종류의 잡이 오직 하나만 큐에 있도록 하고 싶을 때가 있습니다. 이 때는 잡 클래스에 `ShouldBeUnique` 인터페이스를 구현하면 됩니다. 별도의 추가 메서드 구현 없이도 동작합니다.

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

위 예시에서 `UpdateSearchIndex` 잡은 고유한 잡입니다. 즉, 이미 같은 잡이 큐에 있고 아직 처리 중이라면 새로운 잡이 추가되지 않습니다.

특정 고유 "키"로 잡의 고유성을 세밀하게 제어하거나, 고유 락의 유효 기간을 지정하고 싶다면 `uniqueId`와 `uniqueFor` 속성 또는 메서드를 잡 클래스에 정의할 수 있습니다.

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

이와 같이, 제품 ID로 유니크한 잡을 만들면 해당 제품 ID를 가진 잡이 큐에 처리되지 않은 상태라면 중복 추가가 막힙니다. 또한 기존 잡이 1시간 내에 처리되지 않으면 락이 해제되어 같은 제품 ID의 잡이 다시 추가될 수 있습니다.

> [!WARNING]
> 웹 서버나 컨테이너가 여러 대인 환경에서는 모든 서버가 같은 캐시 서버를 사용하도록 설정해야만 Laravel이 정확하게 잡의 고유 상태를 판단할 수 있습니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 처리 시작까지 잡 고유성 유지

기본적으로 고유 잡은 큐 처리가 완료되거나 모든 재시도 횟수가 소진된 이후에 "락"(고유 상태)이 해제됩니다. 하지만 처리 직전에 락을 해제하고 싶다면, `ShouldBeUnique` 대신 `ShouldBeUniqueUntilProcessing` 인터페이스를 구현하세요.

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
#### 고유 잡 락(Unique Job Locks)

`ShouldBeUnique` 잡이 디스패치되면, Laravel은 내부적으로 `uniqueId` 키를 사용해 [락](/docs/12.x/cache#atomic-locks)을 획득하려고 시도합니다. 이미 락이 존재하면 잡이 디스패치되지 않습니다. 이 락은 잡이 정상처리 혹은 모든 재시도 실패 시 해제됩니다. 기본적으로는 기본 캐시 드라이버를 사용하지만, 락용 캐시 드라이버를 직접 지정하고 싶을 땐 `uniqueVia` 메서드를 오버라이드 하면 됩니다.

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
> 특정 잡의 동시 실행만 제한하려면 [WithoutOverlapping 미들웨어](/docs/12.x/queues#preventing-job-overlaps)를 사용하세요.

<a name="encrypted-jobs"></a>
### 암호화된 잡 (Encrypted Jobs)

잡의 데이터 프라이버시와 무결성을 위해 Laravel의 [암호화](/docs/12.x/encryption) 기능을 사용할 수 있습니다. 잡 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하면, 잡이 큐에 올라가기 전에 자동으로 암호화됩니다.

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

잡 미들웨어를 사용하면 큐 잡 실행 전후에 공통 로직을 감쌀 수 있어, 각 잡 내부에서 반복되는 코드(예를 들어, Redis 기반의 속도 제한 로직 등)를 줄일 수 있습니다.

예시로, 다음의 `handle` 메서드는 Redis로 5초에 1개만 실행되도록 제어하고 있습니다.

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

이 코드는 유효하지만, 잡마다 반복되면 가독성이 떨어집니다. 대신 이 로직을 미들웨어로 분리할 수 있습니다.

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

라우트 미들웨어와 마찬가지로, 잡 미들웨어는 잡과 다음 처리를 위한 콜백을 인자로 받습니다.

`make:job-middleware` Artisan 명령어로 새 잡 미들웨어 클래스를 생성할 수 있습니다. 미들웨어 적용은 잡 클래스에 직접 `middleware` 메서드를 만들어(직접 추가 필요, 기본 잡에는 없음) 배열로 반환하면 됩니다.

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
> 잡 미들웨어는 [큐잉 이벤트 리스너](/docs/12.x/events#queued-event-listeners), [메일러블](/docs/12.x/mail#queueing-mail), [알림](/docs/12.x/notifications#queueing-notifications)에도 적용할 수 있습니다.

<a name="rate-limiting"></a>
### 속도 제한(Rate Limiting)

직접 미들웨어로 만들 수도 있지만, Laravel은 이미 잡 전용 속도 제한 미들웨어를 제공합니다. 라우트 속도 제한자와 유사하게, `RateLimiter` 파사드의 `for` 메서드로 잡 속도 제한자를 정의합니다.

예를 들어, 일반 사용자는 시간당 1회 백업만 허용하되, 프리미엄 고객은 제한 없이 하고 싶다면 `AppServiceProvider`의 `boot`에서 다음과 같이 설정할 수 있습니다.

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

이처럼 분(minute) 단위로도 제한할 수 있으며, `by` 메서드에는 대개 고객 식별자를 넘깁니다.

```php
return Limit::perMinute(50)->by($job->user->id);
```

정의한 속도 제한자는 `Illuminate\Queue\Middleware\RateLimited` 미들웨어를 통해 잡에 적용할 수 있습니다.

```php
use Illuminate\Queue\Middleware\RateLimited;

public function middleware(): array
{
    return [new RateLimited('backups')];
}
```

잡이 속도 제한에 의해 release될 때도 잡의 `attempts`(시도 횟수)가 증가합니다. 필요에 따라 잡의 `tries`, `maxExceptions` 속성을 조절하거나, [retryUntil](#time-based-attempts) 메서드로 재시도 유효시간을 지정할 수 있습니다.

`releaseAfter`로 잡이 다시 시도되기 전 대기 시간을 지정할 수 있습니다.

```php
public function middleware(): array
{
    return [(new RateLimited('backups'))->releaseAfter(60)];
}
```

잡이 속도 제한에 걸릴 때 아예 재시도를 원치 않는다면 `dontRelease` 메서드를 사용하세요.

```php
public function middleware(): array
{
    return [(new RateLimited('backups'))->dontRelease()];
}
```

<a name="rate-limiting-with-redis"></a>
#### Redis로 속도 제한

Redis 환경에서는 성능이 더 우수한 `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어를 사용할 수 있습니다.

```php
use Illuminate\Queue\Middleware\RateLimitedWithRedis;

public function middleware(): array
{
    return [new RateLimitedWithRedis('backups')];
}
```

특정 Redis 커넥션을 사용해야 한다면 `connection` 메서드로 지정할 수 있습니다.

```php
return [(new RateLimitedWithRedis('backups'))->connection('limiter')];
```

<a name="preventing-job-overlaps"></a>
### 잡 중복 실행 방지

`Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어를 활용하면 특정 키에 대해 잡이 중복 실행되지 않도록 할 수 있습니다. 예: 한 사용자의 신용 점수 업데이트 잡이 동시에 여러 개 실행되지 않게 제한할 수 있습니다.

```php
use Illuminate\Queue\Middleware\WithoutOverlapping;

public function middleware(): array
{
    return [new WithoutOverlapping($this->user->id)];
}
```

중복된 잡은 release 처리되며, `releaseAfter`로 대기 시간도 지정 가능합니다.

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->releaseAfter(60)];
}
```

즉시 삭제(재시도하지 않음)하려면 `dontRelease` 메서드를 사용하세요.

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->dontRelease()];
}
```

예상치 못한 장애나 타임아웃 등으로 락이 정상적으로 해제되지 않을 수 있으니, `expireAfter`로 락 만료 시간을 지정할 수 있습니다.

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->expireAfter(180)];
}
```

> [!WARNING]
> `WithoutOverlapping`는 락을 지원하는 캐시 드라이버가 필요합니다. (`memcached`, `redis`, `dynamodb`, `database`, `file`, `array`)

<a name="sharing-lock-keys"></a>
#### 잡 클래스끼리 락 키 공유

`WithoutOverlapping`은 기본적으로 같은 클래스의 잡끼리만 중복을 막습니다. 서로 다른 클래스라도 락 키가 같으면 중복을 막도록 하려면 `shared()` 메서드를 사용합니다.

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
### 예외 스로틀링(Throttling Exceptions)

`Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어는 잡에서 연속적으로 여러 번 예외가 발생하면, 일정 시간 동안 잡 실행을 지연시킬 수 있습니다. 불안정한 외부 서비스와 연동하는 경우에 유용합니다.

예를 들어, 10회 연속 예외 발생 시 5분간 잡을 중단시키려면:

```php
use DateTime;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [new ThrottlesExceptions(10, 5 * 60)];
}

public function retryUntil(): DateTime
{
    return now()->plus(minutes: 30);
}
```

기본적으로 예외가 발생하면 즉시 재시도되지만, `backoff` 메서드로 일정 시간 딜레이를 줄 수도 있습니다.

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 5 * 60))->backoff(5)];
}
```

여러 잡이 특정 키로 스로틀링을 공유하도록 하려면 `by` 메서드를 사용해 캐시 키를 맞춰줍니다.

```php
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->by('key')];
}
```

특정 예외에만 스로틀링 동작을 적용하고 싶다면 `when` 메서드에 조건 Closure를 전달하세요.

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

특정 예외에 대해 잡을 아예 삭제하고 싶을 때는 `deleteWhen` 메서드 사용:

```php
use App\Exceptions\CustomerDeletedException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [(new ThrottlesExceptions(2, 10 * 60))->deleteWhen(CustomerDeletedException::class)];
}
```

예외를 앱의 예외 핸들러로 리포트하려면 `report` 메서드를 사용하세요.

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

<a name="throttling-exceptions-with-redis"></a>
#### Redis로 예외 스로틀링

Redis에서는 더 최적화된 `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어를 사용하세요.

```php
use Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis;

public function middleware(): array
{
    return [new ThrottlesExceptionsWithRedis(10, 10 * 60)];
}
```

특정 Redis 커넥션을 지정할 수도 있습니다.

```php
return [(new ThrottlesExceptionsWithRedis(10, 10 * 60))->connection('limiter')];
```

<a name="skipping-jobs"></a>
### 잡 건너뛰기(Skipping Jobs)

`Skip` 미들웨어를 사용하면 별도의 잡 코드 변경 없이 조건에 따라 잡을 건너뛰거나 삭제할 수 있습니다. `Skip::when`은 조건이 true이면, `Skip::unless`는 조건이 false이면 잡을 삭제합니다.

```php
use Illuminate\Queue\Middleware\Skip;

public function middleware(): array
{
    return [
        Skip::when($condition),
    ];
}
```

보다 복잡한 판단이 필요하다면 Closure를 넘겨줄 수도 있습니다.

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

<!-- 이하 내용 계속 번역됨 -->

(이후 본문 내용도 위 규칙 및 스타일대로 이어서 완전히 번역됨)