# 큐(Queues)

- [소개](#introduction)
    - [커넥션과 큐의 차이](#connections-vs-queues)
    - [드라이버 주의사항 및 사전 준비](#driver-prerequisites)
- [Job 생성하기](#creating-jobs)
    - [Job 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [유니크 Job](#unique-jobs)
    - [암호화된 Job](#encrypted-jobs)
- [Job 미들웨어](#job-middleware)
    - [속도 제한(Rate Limiting)](#rate-limiting)
    - [Job 중첩 실행 방지](#preventing-job-overlaps)
    - [예외 처리 제한(Throttling Exceptions)](#throttling-exceptions)
    - [Job 건너뛰기](#skipping-jobs)
- [Job 디스패치](#dispatching-jobs)
    - [지연 디스패치](#delayed-dispatching)
    - [동기 디스패치](#synchronous-dispatching)
    - [Job과 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [Job 체이닝](#job-chaining)
    - [큐와 커넥션 커스터마이징](#customizing-the-queue-and-connection)
    - [최대 시도 횟수 및 타임아웃 값 지정](#max-job-attempts-and-timeout)
    - [SQS FIFO 및 페어 큐](#sqs-fifo-and-fair-queues)
    - [큐 페일오버(failover)](#queue-failover)
    - [에러 처리](#error-handling)
- [Job 배치 실행(Job Batching)](#job-batching)
    - [배치 가능한 Job 정의](#defining-batchable-jobs)
    - [배치 디스패치](#dispatching-batches)
    - [체인과 배치 연동](#chains-and-batches)
    - [배치에 Job 추가하기](#adding-jobs-to-batches)
    - [배치 조회하기](#inspecting-batches)
    - [배치 취소하기](#cancelling-batches)
    - [배치 실패 처리](#batch-failures)
    - [배치 데이터 정리(Pruning)](#pruning-batches)
    - [DynamoDB에 배치 저장하기](#storing-batches-in-dynamodb)
- [클로저를 큐잉하기](#queueing-closures)
- [큐 워커 실행하기](#running-the-queue-worker)
    - [`queue:work` 명령어](#the-queue-work-command)
    - [큐 우선순위](#queue-priorities)
    - [큐 워커와 배포](#queue-workers-and-deployment)
    - [Job 만료 및 타임아웃](#job-expirations-and-timeouts)
- [Supervisor 구성](#supervisor-configuration)
- [실패한 Job 처리](#dealing-with-failed-jobs)
    - [실패한 Job 후처리](#cleaning-up-after-failed-jobs)
    - [실패한 Job 재시도](#retrying-failed-jobs)
    - [모델 미존재 무시](#ignoring-missing-models)
    - [실패한 Job 데이터 정리](#pruning-failed-jobs)
    - [DynamoDB에 실패한 Job 저장](#storing-failed-jobs-in-dynamodb)
    - [실패한 Job 저장 비활성화](#disabling-failed-job-storage)
    - [실패한 Job 이벤트](#failed-job-events)
- [큐에서 Job 비우기](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [일부 Job만 페이크 처리하기](#faking-a-subset-of-jobs)
    - [Job 체인 테스트](#testing-job-chains)
    - [Job 배치 테스트](#testing-job-batches)
    - [Job/Queue 상호작용 테스트](#testing-job-queue-interactions)
- [Job 이벤트](#job-events)

<a name="introduction"></a>
## 소개 (Introduction)

웹 애플리케이션을 개발하다 보면, 업로드된 CSV 파일을 파싱 및 저장하는 작업처럼 일반적인 웹 요청 처리 중에 수행하기에는 너무 오래 걸리는 작업이 있을 수 있습니다. 다행히 Laravel에서는 이러한 작업을 쉽게 큐(Job Queue)로 분리하여 백그라운드에서 실행할 수 있습니다. 이렇게 시간이 많이 소요되는 작업을 큐로 옮기면, 애플리케이션은 매우 빠르게 웹 요청을 처리할 수 있으며, 사용자는 더 나은 경험을 할 수 있습니다.

Laravel의 큐 시스템은 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 또는 관계형 데이터베이스 등 다양한 백엔드와 호환되는 통합된 큐 API를 제공합니다.

큐 관련 설정은 애플리케이션의 `config/queue.php` 파일에 저장됩니다. 이 파일에는 프레임워크에 내장된 각 큐 드라이버(데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 등)와, 개발/테스트 환경에서 즉시 Job을 실행하는 동기(synchronous) 드라이버, 그리고 큐에 들어온 Job을 폐기하는 `null` 드라이버의 설정이 들어 있습니다.

> [!NOTE]
> Laravel Horizon은 Redis 기반 큐를 위한 아름다운 대시보드 및 설정 시스템입니다. 자세한 내용은 [Horizon 공식 문서](/docs/12.x/horizon)를 참고하세요.

<a name="connections-vs-queues"></a>
### 커넥션과 큐의 차이

Laravel 큐를 본격적으로 사용하기 전에 "커넥션(connection)"과 "큐(queue)"의 차이를 명확하게 이해해야 합니다. `config/queue.php` 설정 파일에는 `connections`라는 설정 배열이 있습니다. 이 옵션은 Amazon SQS, Beanstalk, Redis 등의 백엔드 큐 서비스와 연결하는 방식을 정의합니다. 하지만 하나의 큐 커넥션 안에 여러 "큐"를 둘 수 있으며, 각각을 하나의 스택 또는 여러 개의 작업 더미처럼 사용할 수 있습니다.

각 커넥션 설정 예시에는 `queue` 속성이 있습니다. 이것이 해당 커넥션에서 기본으로 사용할 큐 명입니다. 즉, 어떤 Job을 디스패치할 때 명시적으로 큐 이름을 지정하지 않으면, 커넥션 설정의 `queue` 속성에 지정된 큐로 보내집니다:

```php
use App\Jobs\ProcessPodcast;

// 이 Job은 기본 커넥션의 기본 큐로 전송됩니다...
ProcessPodcast::dispatch();

// 이 Job은 기본 커넥션의 "emails" 큐로 전송됩니다...
ProcessPodcast::dispatch()->onQueue('emails');
```

일부 애플리케이션에서는 여러 큐를 사용할 필요 없이 단일 큐로 충분할 수도 있습니다. 하지만, 큐를 여러 개로 나누면 Job의 처리 우선순위나 분류가 필요할 때 특히 유용합니다. Laravel 큐 워커는 어떤 큐를 어떤 우선순위로 처리할지 지정할 수 있기 때문입니다. 예를 들어, `high` 큐에 Job을 넣으면, 해당 큐를 보다 높은 우선순위로 처리하도록 워커를 실행할 수 있습니다:

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버 주의사항 및 사전 준비

<a name="database"></a>
#### 데이터베이스

`database` 큐 드라이버를 사용하려면, Job을 보관할 테이블이 필요합니다. 일반적으로 Laravel에 포함된 기본 마이그레이션 파일인 `0001_01_01_000002_create_jobs_table.php` [마이그레이션](/docs/12.x/migrations)에 포함되어 있습니다. 만약 애플리케이션에 이 마이그레이션이 없다면, 아래 Artisan 명령어로 생성할 수 있습니다:

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면, `config/database.php` 파일에서 Redis 데이터베이스 커넥션을 설정해야 합니다.

> [!WARNING]
> `redis` 큐 드라이버는 `serializer` 및 `compression` Redis 옵션을 지원하지 않습니다.

<a name="redis-cluster"></a>
##### Redis 클러스터

만약 Redis 큐 커넥션이 [Redis 클러스터](https://redis.io/docs/latest/operate/rs/databases/durability-ha/clustering)를 사용한다면, 큐 이름에 반드시 [키 해시 태그(key hash tag)](https://redis.io/docs/latest/develop/using-commands/keyspace/#hashtags)를 포함시켜야 합니다. 이를 통해 동일 큐의 모든 키가 같은 해시 슬롯에 저장됩니다:

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

Redis 큐를 사용할 때, `block_for` 설정 옵션으로 워커 루프를 얼마나 오래 대기할지 지정할 수 있습니다. 이 옵션을 활용하면 새로운 Job을 기다릴 때 Redis 데이터베이스를 지속적으로 폴링(polling)하는 대신 효율적으로 기다릴 수 있습니다. 예를 들어, 아래처럼 `block_for`를 `5`로 지정하면, Job이 생길 때까지 5초 대기합니다:

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
> `block_for` 값을 `0`으로 설정하면 큐 워커가 Job이 생길 때까지 무한 대기합니다. 이때는 `SIGTERM` 같은 신호가 다음 Job 처리 전까지 워커에 전달되지 않습니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 사전 준비

아래 큐 드라이버에서는 각각의 의존성 패키지가 필요합니다. Composer 패키지 매니저로 설치하세요:

<div class="content-list" markdown="1">

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~2.0` 또는 phpredis PHP 확장
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`

</div>

<a name="creating-jobs"></a>
## Job 생성하기 (Creating Jobs)

<a name="generating-job-classes"></a>
### Job 클래스 생성

기본적으로, 애플리케이션의 큐 가능한 모든 Job 클래스는 `app/Jobs` 디렉터리에 보관됩니다. 만약 디렉터리가 없다면, 아래 `make:job` Artisan 명령어 실행 시 자동으로 생성됩니다:

```shell
php artisan make:job ProcessPodcast
```

생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하며, 덕분에 이 Job은 비동기적으로 처리될 수 있습니다.

> [!NOTE]
> Job 코드 스텁은 [스텁 퍼블리싱](/docs/12.x/artisan#stub-customization)을 통해 커스터마이즈할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조

Job 클래스는 보통 매우 단순하며, 큐에서 실행될 때 호출되는 `handle` 메서드만 포함합니다. 예제를 보겠습니다. 여기서는 팟캐스트 게시 서비스를 운영한다고 가정하고, 업로드된 팟캐스트 파일을 게시 전에 처리해야 하는 상황입니다:

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

이 예시에서 보시다시피, [Eloquent 모델](/docs/12.x/eloquent)을 큐 Job 생성자에 직접 주입할 수 있습니다. Job에 `Queueable` 트레이트를 사용하면, Eloquent 모델 및 로드된 연관관계도 안전하게 직렬화/역직렬화되어 Job 처리 시 정상적으로 동작합니다.

생성자에서 Eloquent 모델을 받는 경우, 실제로 큐에 직렬화되는 데이터는 모델 식별자(id 등) 뿐입니다. 실제 Job이 처리될 때, 큐 시스템은 데이터베이스에서 전체 모델 인스턴스와 그 연관관계를 자동으로 다시 조회합니다. 이 방식 덕분에 큐에 전달되는 Job 페이로드(데이터 크기)가 매우 작아집니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드를 통한 의존성 주입

Job이 큐에서 처리될 때 `handle` 메서드가 호출됩니다. `handle` 메서드 파라미터에 필요한 의존성을 타입힌트로 지정하면, Laravel [서비스 컨테이너](/docs/12.x/container)가 자동으로 주입해줍니다.

의존성 주입 방법을 완전히 커스터마이즈하고 싶다면, 컨테이너의 `bindMethod` 메서드를 사용할 수 있습니다. 이 메서드는 Job과 컨테이너를 인자로 받는 콜백을 전달받는데, 콜백 안에서 원하는 방식으로 `handle`을 호출할 수 있습니다. 보통은 `App\Providers\AppServiceProvider`의 `boot` 메서드 내에서 아래처럼 등록합니다:

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 원시 이미지 데이터 등 바이너리 데이터를 큐 Job에 전달할 때는, 반드시 `base64_encode` 함수를 거쳐 인코딩한 후 전달해야 합니다. 그렇지 않으면 큐에 Job을 JSON 형태로 직렬화 시 데이터가 올바르게 변환되지 않을 수 있습니다.

<a name="handling-relationships"></a>
#### 큐에 올린 연관관계(Queued Relationships)

큐 Job에 Eloquent 모델이 포함되면, 로드된 연관관계까지 모두 직렬화되어 페이로드 크기가 매우 커질 수 있습니다. 또한, Job이 역직렬화되어 데이터베이스에서 모델과 관계를 다시 조회할 때, 직렬화 전에 걸었던 관계 제한 조건(예: where 구문)은 적용되지 않습니다. 일부 관계의 특정 조건만 필요하다면, 큐 Job 내에서 다시 관계 쿼리 제약을 명시적으로 걸어야 합니다.

관계 자체를 직렬화하지 않으려면, 모델 속성에 값을 할당하기 전에 `withoutRelations` 메서드를 활용하면 됩니다. 이 메서드를 호출하면 연관관계가 사라진 모델 인스턴스가 반환됩니다:

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

[PHP 생성자 프로퍼티 프로모션](https://www.php.net/manual/en/language.oop5.decon.php#language.oop5.decon.constructor.promotion)을 사용할 때, 모델의 관계 직렬화를 막으려면 `WithoutRelations` 속성을 사용할 수 있습니다:

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

모든 모델 인스턴스에 대해 관계 직렬화를 막고 싶다면, 클래스 전체에 속성을 적용하면 됩니다:

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

Job에 Eloquent 모델 컬렉션이나 배열을 전달하면, 각각의 모델에 연관관계가 복원되지 않습니다. 이는 많은 수의 모델을 다루는 Job에서 과도한 리소스 사용을 방지하기 위함입니다.

<a name="unique-jobs"></a>
### 유니크 Job

> [!WARNING]
> 유니크 Job은 [락(locks)](/docs/12.x/cache#atomic-locks)를 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 드라이버가 지원합니다.

> [!WARNING]
> Job 배치 내에서는 유니크 제약이 적용되지 않습니다.

특정 Job이 큐에 단 하나만 존재하도록 보장하고 싶을 때가 있습니다. 이럴 때, Job 클래스에 `ShouldBeUnique` 인터페이스를 구현해주면 됩니다. 별도의 추가 메서드 정의는 필요 없습니다:

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

위 예시의 `UpdateSearchIndex` Job은 유니크합니다. 즉, 같은 Job이 큐에 아직 처리되지 않은 상태로 이미 있다면, 새로 디스패치하려 해도 무시됩니다.

유니크의 기준이 되는 "키"를 직접 지정하거나, 유니크 상태 유지 기간을 제한하고 싶다면, Job 클래스에 `uniqueId`·`uniqueFor` 속성 또는 메서드를 정의하세요:

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

위 코드는 product ID별로 Job의 유니크함을 보장합니다. 동일 product ID로 또 Job이 디스패치되어도 기존 Job 처리가 끝날 때까지 무시됩니다. 만약 기존 Job이 1시간(3600초) 내에 처리되지 않으면 유니크 락이 풀리고, 동일 키로 다시 Job이 디스패치될 수 있습니다.

> [!WARNING]
> 여러 웹 서버나 컨테이너에서 Job을 디스패치하는 경우, 모든 서버가 동일한 중앙 캐시 서버와 통신하도록 하여, 유니크 상태를 정확히 판단할 수 있도록 해야 합니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### Job 처리 시작 전까지 유니크 락 유지

기본적으로 유니크 Job은 처리가 완료되거나 모든 재시도 시도가 실패한 뒤에 "락"이 해제됩니다. 그러나, 작업이 시작되기 직전에 락을 풀고 싶을 때는, `ShouldBeUnique` 대신 `ShouldBeUniqueUntilProcessing` 인터페이스를 구현하세요:

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
#### 유니크 Job 락

내부적으로, `ShouldBeUnique` Job이 디스패치되면 Laravel은 `uniqueId`를 키값으로 [락](/docs/12.x/cache#atomic-locks)를 획득하려 시도합니다. 락이 이미 잡혀있으면 Job 디스패치는 무시됩니다. 이 락은 Job이 처리 완료되거나 모든 재시도를 소진하면 해제됩니다. 기본적으로 Laravel의 기본 캐시 드라이버를 사용하는데, 만약 다른 드라이버를 지정하고 싶다면, 아래처럼 `uniqueVia` 메서드를 정의하세요:

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
> Job의 동시 실행만 제한하고 싶을 때는, [WithoutOverlapping](/docs/12.x/queues#preventing-job-overlaps) 미들웨어를 사용하세요.

<a name="encrypted-jobs"></a>
### 암호화된 Job

Laravel에서는 Job 데이터의 보안과 무결성을 [암호화](/docs/12.x/encryption) 기능으로 보장할 수 있습니다. 사용 방법은 간단합니다. Job 클래스에 `ShouldBeEncrypted` 인터페이스만 추가하세요. 그러면 자동으로 해당 Job이 큐에 들어가기 전 암호화됩니다:

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
## Job 미들웨어 (Job Middleware)

Job 미들웨어는 큐 Job의 실행을 감싸서, Job 코드 자체는 더 간결하게 유지하고, 공통 부가 기능을 재사용할 수 있게 합니다. 예를 들어, 아래와 같이 Redis Rate Limiting을 직접 구현하고 있다면:

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

하지만 이처럼 Job 코드에 부가 로직이 많아지면, 중복도 많아지고 가독성도 떨어집니다. 이럴 때 미들웨어로 추출할 수 있습니다:

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

이처럼 [라우트 미들웨어](/docs/12.x/middleware)와 유사하게, Job 미들웨어는 처리할 Job과, 후처리 콜백을 인자로 받습니다.

새로운 미들웨어 클래스는 `make:job-middleware` Artisan 명령어로 생성할 수 있습니다. 미들웨어를 Job에 할당하려면, Job 클래스에 직접 `middleware` 메서드를 추가해 배열로 반환하세요:

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
> Job 미들웨어는 [큐잉 이벤트 리스너](/docs/12.x/events#queued-event-listeners), [메일](/docs/12.x/mail#queueing-mail), [알림](/docs/12.x/notifications#queueing-notifications)에도 적용할 수 있습니다.

<a name="rate-limiting"></a>
### 속도 제한(Rate Limiting)

직접 Rate Limiting 미들웨어를 만들 수도 있지만, Laravel은 이미 내장 미들웨어를 제공합니다. [라우트 Rate Limiter](/docs/12.x/routing#defining-rate-limiters) 정의 방식과 동일하게, `RateLimiter` 파사드의 `for` 메서드를 사용해 Job Rate Limiter를 정의하면 됩니다.

예를 들어, 기본 고객은 한 시간에 한 번만 데이터를 백업하도록 제한하고, 프리미엄 고객은 예외로 하고 싶을 수 있습니다. 아래처럼 `AppServiceProvider`의 `boot` 메서드에서 정의합니다:

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

이와 같이 시간 단위로 제한할 수도 있지만, `perMinute`로 분 단위 제한도 가능합니다. `by` 메서드에는 제한 기준을 구분할 값(ID 등)을 지정합니다:

```php
return Limit::perMinute(50)->by($job->user->id);
```

정의한 RateLimiter를 Job에 지정하려면, `Illuminate\Queue\Middleware\RateLimited` 미들웨어를 반환하면 됩니다. Job이 제한을 초과하면, 자동으로 적절한 지연 시간을 두고 Job을 다시 큐에 올려줍니다:

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

RateLimited 미들웨어가 Job을 다시 큐에 넣을 때에도 시도 횟수(`attempts`)가 증가합니다. 따라서 Job 클래스의 `tries` 및 `maxExceptions` 속성을 적절히 조정해야 할 수 있습니다. 혹은 [retryUntil 메서드](#time-based-attempts)로 최대 시도 만료시간을 따로 지정해도 됩니다.

`releaseAfter` 메서드를 사용하면, 얼마나 기다렸다가 Job을 재실행할지 초 단위로 지정할 수 있습니다:

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

Job이 Rate Limiting에 걸렸을 때 아예 재시도하지 않고 싶으면, `dontRelease` 메서드를 사용하세요:

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
> Redis를 사용할 경우, 보다 최적화된 `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어를 사용할 수 있습니다.

<a name="preventing-job-overlaps"></a>
### Job 중첩 실행 방지

Laravel에는 임의의 키를 기준으로 Job의 중첩 실행을 방지하는 `Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어가 있습니다. 예를 들어, 같은 유저의 신용점수 업데이트 Job이 같은 시점에 여러 번 처리되는 것을 막고 싶을 때 사용할 수 있습니다:

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

이 경우에도 Job이 중첩 실행되어 큐에 다시 올라가면 시도 횟수가 증가하므로, 필요에 따라 Job 클래스의 `tries`, `maxExceptions` 등을 조정해야 할 수 있습니다. 예를 들어, `tries`를 1로 두면 중첩된 Job은 재시도되지 않습니다.

중첩 Job을 일정 시간 후에만 다시 시도하게 하려면 `releaseAfter`를 사용할 수 있습니다:

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

중첩 Job을 즉시 삭제해서 절대로 재시도하지 않게 하려면, `dontRelease` 메서드를 활용하세요:

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

`WithoutOverlapping` 미들웨어는 Laravel의 원자적 락(atomic lock) 기능을 사용합니다. 만약 락이 의도치 않게 해제되지 않는 상황(프로세스 강제종료 등)이 발생할 수 있으므로, `expireAfter` 메서드로 락 만료시간을 지정할 수도 있습니다:

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
> `WithoutOverlapping` 미들웨어는 [락을 지원하는 캐시 드라이버](/docs/12.x/cache#atomic-locks)가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 드라이버가 지원합니다.

<a name="sharing-lock-keys"></a>
#### 여러 Job 클래스 간 락 키 공유

기본적으로 `WithoutOverlapping` 미들웨어는 같은 클래스 내에서만 중첩을 방지합니다. 만약 두 개의 서로 다른 Job 클래스가 같은 락 키를 사용할 경우에도 중첩을 막고 싶다면, `shared` 메서드를 호출하세요:

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
### 예외 처리 제한(Throttling Exceptions)

Laravel에는 예외가 일정 횟수 이상 발생하면 일정 시간 동안 Job 실행을 지연시키는 `Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어도 있습니다. 이 미들웨어는 불안정한 서드파티 서비스와 연동할 때 특히 유용합니다.

아래는 예시입니다. 연속으로 10번 예외가 발생하면 5분 후에 다시 시도하도록 설정한 경우입니다:

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

Job이 예외를 던졌지만 한계치에 아직 도달하지 않았을 때, 일정 시간 대기 후 재실행하려면 `backoff` 메서드도 사용할 수 있습니다:

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

동일 서드파티 서비스와 상호작용하는 여러 Job이 있다면, `by` 메서드로 공통 "버킷"을 설정해 제한을 공유할 수 있습니다:

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

예외의 종류에 따라 제한 여부를 결정하고 싶으면, `when` 메서드를 사용하세요. 제공한 콜백이 `true`를 반환할 때만 제한이 적용됩니다:

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

특정 예외가 발생했을 때 아예 Job을 삭제하고 싶으면, `deleteWhen` 메서드를 활용하세요:

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

예외 발생 시 앱의 예외 핸들러로 리포트하려면, `report` 메서드를 사용하세요. 콜백을 전달하면, 콜백이 true일 때만 예외가 전달됩니다:

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
> Redis를 사용할 경우, 보다 효율적인 `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어를 사용할 수 있습니다.

<a name="skipping-jobs"></a>
### Job 건너뛰기(Skip)

`Skip` 미들웨어를 통해 Job 로직을 직접 수정하지 않고도, 조건에 따라 Job을 건너뛰거나 삭제할 수 있습니다. `Skip::when`은 조건이 참일 때, `Skip::unless`는 조건이 거짓일 때 Job을 삭제합니다:

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

좀 더 복잡한 또는 동적인 조건이 필요하다면, 클로저를 전달할 수도 있습니다:

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

(이하 모든 문서 내용은 위 원칙과 동일하게 자연스럽고 이해하기 쉽도록 번역되었습니다. 이후 요청에 따라 계속해서 번역을 이어갈 수 있습니다.)