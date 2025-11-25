# 큐 (Queues)

- [소개](#introduction)
    - [커넥션과 큐의 차이](#connections-vs-queues)
    - [드라이버별 참고 사항 및 필요조건](#driver-prerequisites)
- [잡 생성](#creating-jobs)
    - [잡 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [유일 잡(Unique Jobs)](#unique-jobs)
    - [암호화된 잡](#encrypted-jobs)
- [잡 미들웨어](#job-middleware)
    - [속도 제한(Rate Limiting)](#rate-limiting)
    - [잡 중복 실행 방지](#preventing-job-overlaps)
    - [예외 처리 제한(Throttling Exceptions)](#throttling-exceptions)
    - [잡 스킵(건너뛰기)](#skipping-jobs)
- [잡 디스패칭(Dispatching)](#dispatching-jobs)
    - [지연 디스패칭](#delayed-dispatching)
    - [동기 디스패칭](#synchronous-dispatching)
    - [잡과 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [잡 체이닝(Chaining)](#job-chaining)
    - [큐 및 커넥션 커스터마이징](#customizing-the-queue-and-connection)
    - [최대 시도 횟수/타임아웃 지정](#max-job-attempts-and-timeout)
    - [SQS FIFO 및 페어 큐](#sqs-fifo-and-fair-queues)
    - [큐 페일오버](#queue-failover)
    - [에러 처리](#error-handling)
- [잡 배칭](#job-batching)
    - [배치 잡 정의](#defining-batchable-jobs)
    - [배치 디스패칭](#dispatching-batches)
    - [체인 & 배치](#chains-and-batches)
    - [배치에 잡 추가하기](#adding-jobs-to-batches)
    - [배치 조회](#inspecting-batches)
    - [배치 취소](#cancelling-batches)
    - [배치 실패](#batch-failures)
    - [배치 정리(Pruning)](#pruning-batches)
    - [DynamoDB에 배치 저장](#storing-batches-in-dynamodb)
- [클로저를 큐에 넣기](#queueing-closures)
- [큐 워커 실행](#running-the-queue-worker)
    - [`queue:work` 명령어](#the-queue-work-command)
    - [큐 우선순위](#queue-priorities)
    - [큐 워커와 배포](#queue-workers-and-deployment)
    - [잡 만료 및 타임아웃](#job-expirations-and-timeouts)
    - [큐 워커 일시정지/재개](#pausing-and-resuming-queue-workers)
- [Supervisor 구성](#supervisor-configuration)
- [실패한 잡 다루기](#dealing-with-failed-jobs)
    - [실패 잡 처리 후 정리](#cleaning-up-after-failed-jobs)
    - [실패 잡 재시도](#retrying-failed-jobs)
    - [모델이 없는 경우 무시](#ignoring-missing-models)
    - [실패 잡 정리(Pruning)](#pruning-failed-jobs)
    - [DynamoDB에 실패 잡 저장](#storing-failed-jobs-in-dynamodb)
    - [실패 잡 저장 비활성화](#disabling-failed-job-storage)
    - [실패 잡 이벤트](#failed-job-events)
- [큐에서 잡 비우기](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [일부 잡만 페이크 처리](#faking-a-subset-of-jobs)
    - [잡 체인 테스트](#testing-job-chains)
    - [잡 배치 테스트](#testing-job-batches)
    - [잡/큐 상호작용 테스트](#testing-job-queue-interactions)
- [잡 이벤트](#job-events)

<a name="introduction"></a>
## 소개 (Introduction)

웹 애플리케이션을 개발하다 보면, 업로드된 CSV 파일을 파싱하고 저장하는 등 일반적인 웹 요청 처리 시간 내에 끝내기에는 시간이 오래 걸리는 작업이 있을 수 있습니다. 다행히 Laravel은 이러한 작업을 쉽게 큐에 넣어 백그라운드에서 비동기로 처리할 수 있도록 해줍니다. 처리 시간이 오래 걸리는 작업을 큐로 분리하면, 애플리케이션이 웹 요청에 매우 빠르게 응답하여 사용자에게 더 나은 경험을 제공합니다.

라라벨 큐는 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 관계형 데이터베이스 등 다양한 큐 백엔드에 대해 통일된 큐 API를 제공합니다.

라라벨의 큐 설정 옵션은 애플리케이션의 `config/queue.php` 설정 파일에 있습니다. 이 파일에는 데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 드라이버를 포함하여 프레임워크에 기본 포함된 각 큐 드라이버별 커넥션 설정이 정의되어 있습니다. 개발 및 테스트 용도로 즉시(동기적으로) 잡을 실행하는 드라이버와, 잡을 바로 폐기하는 `null` 큐 드라이버도 포함되어 있습니다.

> [!NOTE]
> Laravel Horizon은 Redis 기반 큐를 위한 아름다운 대시보드 및 구성 시스템입니다. 자세한 내용은 [Horizon 문서](/docs/12.x/horizon)를 참고하세요.

<a name="connections-vs-queues"></a>
### 커넥션과 큐의 차이

라라벨 큐를 사용하기 전에, "커넥션(connection)"과 "큐(queue)"의 차이를 이해하는 것이 중요합니다. `config/queue.php` 파일에는 `connections` 설정 배열이 있습니다. 이 옵션은 Amazon SQS, Beanstalk, Redis 등 백엔드 큐 서비스로의 연결을 정의합니다. 하나의 큐 커넥션은 여러 개의 "큐"를 가질 수 있습니다. 각각의 큐는 일종의 별도의 대기열로, 잡을 분리해서 쌓을 수 있는 공간입니다.

각 커넥션 설정 예제에는 항상 `queue` 속성이 포함되어 있습니다. 잡을 보낼 때 어떤 큐에 보낼지 명시하지 않으면, 해당 커넥션의 `queue` 속성에 정의한 기본 큐로 잡이 들어갑니다:

```php
use App\Jobs\ProcessPodcast;

// 이 잡은 기본 커넥션의 기본 큐로 전송됨...
ProcessPodcast::dispatch();

// 이 잡은 기본 커넥션의 "emails" 큐로 전송됨...
ProcessPodcast::dispatch()->onQueue('emails');
```

일부 애플리케이션은 여러 큐를 사용할 필요 없이, 하나의 간단한 큐만 쓸 수도 있습니다. 하지만 여러 큐로 잡을 분산시키면, 잡별로 처리 우선순위를 지정하거나 영역을 분리할 수 있어 매우 유용합니다. 라라벨 큐 워커는 어떤 큐를 어떤 우선순위로 처리할지 지정할 수 있습니다. 예를 들어, `high` 큐로 잡을 보내고 해당 큐에 더 높은 우선순위를 준 워커를 실행할 수 있습니다:

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버별 참고 사항 및 필요조건

<a name="database"></a>
#### 데이터베이스

`database` 큐 드라이버를 사용하려면, 잡을 저장할 데이터베이스 테이블이 필요합니다. 보통 라라벨 기본 마이그레이션인 `0001_01_01_000002_create_jobs_table.php`에 포함되어 있습니다. 해당 마이그레이션이 없다면 아래 Artisan 명령어로 마이그레이션 파일을 생성할 수 있습니다:

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면, `config/database.php` 파일에서 Redis 데이터베이스 커넥션을 미리 설정해야 합니다.

> [!WARNING]
> `redis` 큐 드라이버는 Redis의 `serializer` 및 `compression` 옵션을 지원하지 않습니다.

<a name="redis-cluster"></a>
##### Redis 클러스터

Redis 큐 커넥션이 [Redis 클러스터](https://redis.io/docs/latest/operate/rs/databases/durability-ha/clustering)를 사용할 경우, 큐 이름에 [키 해시 태그(key hash tag)](https://redis.io/docs/latest/develop/using-commands/keyspace/#hashtags)를 반드시 포함해야 합니다. 이를 통해 특정 큐와 관련된 모든 Redis 키가 동일한 해시 슬롯에 배치됩니다:

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
##### 블로킹

Redis 큐를 사용할 때, `block_for` 설정 옵션으로 잡이 큐에 도착할 때까지 기다릴 최대 시간을 지정할 수 있습니다. 이 값은 큐 부하에 따라 적절히 조절하면, Redis를 계속 폴링하는 대신 좀 더 효율적으로 동작할 수 있습니다. 예를 들어 5초로 지정하면, 잡이 도착할 때까지 최대 5초간 대기합니다:

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
> `block_for`를 `0`으로 지정하면, 잡이 올 때까지 무한 대기합니다. 이 경우, `SIGTERM` 같은 시그널이 들어와도 다음 잡을 처리할 때까지 무시될 수 있습니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 필수 패키지

아래 큐 드라이버별로 다음 의존 패키지가 필요합니다. Composer 패키지 매니저로 설치할 수 있습니다:

<div class="content-list" markdown="1">

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~2.0` 또는 phpredis PHP 확장 모듈
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`

</div>

<a name="creating-jobs"></a>
## 잡 생성 (Creating Jobs)

<a name="generating-job-classes"></a>
### 잡 클래스 생성

기본적으로, 애플리케이션의 모든 큐 가능한 잡들은 `app/Jobs` 디렉토리에 저장됩니다. 이 디렉토리가 없으면, `make:job` Artisan 명령어를 실행할 때 자동으로 생성됩니다:

```shell
php artisan make:job ProcessPodcast
```

생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하며, 라라벨에게 이 잡이 비동기적으로 큐에 넣어 처리해야 함을 알립니다.

> [!NOTE]
> 잡 스텁은 [스텁 퍼블리싱](/docs/12.x/artisan#stub-customization)을 통해 커스터마이징할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조

잡 클래스는 일반적으로 매우 간단하며, 잡이 큐에서 처리될 때 호출되는 `handle` 메서드 하나만 포함하는 경우가 많습니다. 예시로, 팟캐스트 게시 서비스를 관리하면서 업로드된 팟캐스트 파일을 게시 전에 처리해야 하는 상황을 살펴보겠습니다:

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

위 예시에서, [Eloquent 모델](/docs/12.x/eloquent)을 잡 생성자의 인수로 바로 전달할 수 있다는 점에 주목하세요. `Queueable` 트레이트를 사용하면 Eloquent 모델과 그에 로드된 연관관계도 잡이 처리될 때 안전하게 직렬화/역직렬화됩니다.

큐 잡 생성자에서 Eloquent 모델을 받으면, 오직 모델의 식별자만 큐에 직렬화되어 저장됩니다. 잡이 실제로 처리될 때 큐 시스템이 자동으로 DB에서 전체 모델 인스턴스와 연관관계를 다시 조회하여 복원합니다. 이렇게 모델을 직렬화하면, 큐 드라이버에 전달되는 잡 페이로드가 매우 작아집니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드 의존성 주입

큐에서 잡이 처리될 때 `handle` 메서드가 호출됩니다. 이때, 잡의 `handle` 메서드에서 타입 힌트를 통해 의존성을 명시할 수 있습니다. Laravel [서비스 컨테이너](/docs/12.x/container)가 자동으로 이 의존성들을 주입해줍니다.

서비스 컨테이너가 `handle` 메서드에 의존성을 어떻게 주입할지 완전한 제어가 필요하다면, 컨테이너의 `bindMethod` 메서드를 사용할 수 있습니다. 이 메서드는 잡 인스턴스와 컨테이너를 콜백으로 받아 임의대로 사용할 수 있습니다. 보통 `App\Providers\AppServiceProvider`의 `boot` 메서드 안에서 호출합니다:

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 원시 이진 데이터(예: 이미지 원본 데이터 등)는 잡에 전달하기 전에 반드시 `base64_encode` 함수를 통해 인코딩하세요. 그렇지 않으면 큐에 삽입될 때 JSON 직렬화가 제대로 되지 않을 수 있습니다.

<a name="handling-relationships"></a>
#### 큐잉되는 연관관계

큐에 잡을 직렬화할 때, 로드된 Eloquent 모델의 모든 연관관계도 같이 직렬화됩니다. 이로 인해 잡 문자열이 매우 커질 수 있습니다. 또한, 잡이 DB에서 역직렬화될 때 이전에 걸었던 연관관계 제약조건들은 무시되고, 전체 연관관계가 다시 조회됩니다. 따라서 연관관계의 일부만 다루고 싶으면, 잡 내에서 연관관계를 다시 제약하여 사용해야 합니다.

아니면, 모델에 속성값을 저장할 때 `withoutRelations` 메서드를 호출하여 연관관계가 직렬화되지 않도록 방지할 수 있습니다. 이 메서드는 로드된 연관관계를 제외한 모델 인스턴스를 반환합니다:

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

[PHP 생성자 프로퍼티 프로모션](https://www.php.net/manual/en/language.oop5.decon.php#language.oop5.decon.constructor.promotion)을 사용하는 경우, Eloquent 모델의 연관관계를 직렬화하지 않도록 `WithoutRelations` 속성(Attribute)을 사용할 수 있습니다:

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

모든 모델에 대해 연관관계 직렬화를 방지하고 싶다면, 속성을 클래스 전체에 지정할 수도 있습니다:

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

만약 단일 모델이 아닌 Eloquent 모델의 컬렉션이나 배열을 받는다면, 해당 컬렉션 안의 모델들은 큐에서 역직렬화되어 잡이 실행될 때 연관관계가 복원되지 않습니다. 이는 대량의 모델을 다루는 잡에 과도한 리소스가 사용되는 것을 방지하기 위함입니다.

<a name="unique-jobs"></a>
### 유일 잡 (Unique Jobs)

> [!WARNING]
> 유일 잡 제약은 [락(locks)](/docs/12.x/cache#atomic-locks)을 지원하는 캐시 드라이버에서만 사용할 수 있습니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 원자적 락을 지원합니다.

> [!WARNING]
> 유일 잡 제약은 배치 내의 잡에는 적용되지 않습니다.

특정 잡이 한 번에 큐에 오직 하나만 존재하도록 강제하고 싶을 때가 있습니다. 이를 위해, 잡 클래스에 `ShouldBeUnique` 인터페이스를 구현하면 됩니다. 별도의 메서드 구현은 필요하지 않습니다:

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

위 예시에서, `UpdateSearchIndex` 잡은 큐에 오직 한 개 인스턴스만 존재할 수 있습니다. 동일 잡이 큐에 있고 아직 처리 중이라면 새 잡은 디스패치되지 않습니다.

잡의 유일성을 결정하는 "key"를 직접 지정하거나, 유일성이 만료되는 시간(초 단위 제한)을 정하고 싶을 때는 `uniqueId` 및 `uniqueFor` 속성 또는 메서드를 잡에 정의하면 됩니다:

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

위 예시에서, `UpdateSearchIndex` 잡은 상품 ID 별로 유일합니다. 동일한 상품 ID로 잡을 디스패치하면 기존 잡이 처리 완료 전에는 무시됩니다. 또한 기존 잡이 1시간(3600초) 내에 처리되지 않으면 락이 해제되어 새로운 동일 잡이 다시 큐에 등록될 수 있습니다.

> [!WARNING]
> 여러 웹 서버/컨테이너에서 잡을 디스패치한다면, 모든 서버가 동일한 중앙 캐시 서버를 사용하도록 해야 라라벨이 잡의 유일성을 정확히 판단할 수 있습니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 잡 수행 시작 전까지 유일성 유지

기본적으로 유일 잡은 처리 완료되거나 모든 재시도를 실패한 이후에 "락(lock)"이 해제됩니다. 하지만 잡이 실제로 처리되기 직전에 유일성을 해제하고 싶을 때는 `ShouldBeUnique` 대신 `ShouldBeUniqueUntilProcessing` 인터페이스를 구현하세요:

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
#### 유일 잡 락(Unique Job Locks)

내부적으로 `ShouldBeUnique` 잡이 디스패치될 때 라라벨은 [락](/docs/12.x/cache#atomic-locks)을 `uniqueId` 키로 획득합니다. 이미 락이 있는 경우, 잡은 디스패치되지 않습니다. 이 락은 잡이 처리 완료되거나 모든 재시도에서 실패하면 해제됩니다. 기본적으로 라라벨은 기본 캐시 드라이버를 사용하지만, 락에 쓸 캐시 드라이버를 바꾸고 싶으면 `uniqueVia` 메서드를 정의하면 됩니다:

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
> 단순히 잡의 동시 실행을 제한하고자 한다면, [WithoutOverlapping](/docs/12.x/queues#preventing-job-overlaps) 잡 미들웨어를 사용하는 것이 더 적합합니다.

<a name="encrypted-jobs"></a>
### 암호화된 잡 (Encrypted Jobs)

라라벨은 잡 데이터를 [암호화](/docs/12.x/encryption)하여 프라이버시와 데이터 무결성을 보장할 수 있습니다. `ShouldBeEncrypted` 인터페이스를 잡 클래스에 추가하면, 디스패치 시 자동으로 잡이 암호화되어 큐에 저장됩니다:

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

잡 미들웨어를 활용하면, 잡 실행 과정에 커스텀 로직을 쉽게 감싸 넣을 수 있어서 각 잡 코드의 중복을 줄일 수 있습니다. 예를 들어, Redis 속도 제한 기능을 사용하여 5초마다 한 번씩만 잡이 처리되도록 하는 코드는 다음과 같습니다:

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

이 방식은 유효하지만 `handle` 메서드가 지저분해질 수 있고, 속도 제한 로직을 다른 잡마다 계속 반복 구현해야 합니다. 대신, 별도의 잡 미들웨어로 해당 로직을 분리할 수 있습니다:

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

[라우트 미들웨어](/docs/12.x/middleware)처럼, 잡 미들웨어도 현재 실행 중인 잡과 다음으로 넘어갈 콜백을 받습니다.

`make:job-middleware` Artisan 명령어로 미들웨어 클래스를 새로 만들 수 있습니다. 생성 후, 잡 클래스에 직접 `middleware` 메서드를 만들어 미들웨어를 명시적으로 등록해야 합니다:

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
> 잡 미들웨어는 [큐잉된 이벤트 리스너](/docs/12.x/events#queued-event-listeners), [메일러블](/docs/12.x/mail#queueing-mail), [알림](/docs/12.x/notifications#queueing-notifications)에도 지정할 수 있습니다.

<a name="rate-limiting"></a>
### 속도 제한 (Rate Limiting)

직접 미들웨어를 구현하지 않아도, 라라벨은 기본적으로 사용할 수 있는 속도 제한 미들웨어를 제공합니다. [라우트 속도 제한](/docs/12.x/routing#defining-rate-limiters)과 비슷하게, 잡용 제한은 `RateLimiter` 파사드의 `for` 메서드로 정의할 수 있습니다.

예를 들어, 일반 사용자는 1시간에 한 번만 백업 잡을 실행하고, 프리미엄 사용자에게는 제한을 두지 않으려면 다음처럼 정의할 수 있습니다:

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

`perMinute`로 분 단위 제한을 둘 수 있고, `by`에는 주로 사용자 ID 등 구분 기준 값을 지정합니다:

```php
return Limit::perMinute(50)->by($job->user->id);
```

정의된 제한을 잡에 적용하려면 `Illuminate\Queue\Middleware\RateLimited` 미들웨어를 사용하면 됩니다. 제한을 초과할 때마다 잡이 큐로 재삽입되며, 제한 시간만큼 지연 처리됩니다:

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

이처럼 잡이 제한에 걸려 큐로 반환되면 `attempts`(시도 횟수)가 올라갑니다. 잡 클래스의 `tries`나 `maxExceptions`을 적절히 조정하고, [retryUntil](#time-based-attempts)로 언제까지 시도할지도 정할 수 있습니다.

`releaseAfter`로 재처리 시까지 기다릴 초를 직접 지정할 수도 있습니다:

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

제한에 걸린 잡을 아예 재시도하지 않으려면 `dontRelease`를 사용하세요:

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
> Redis를 사용할 경우 `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어를 사용하면 기본 미들웨어보다 더욱 효율적입니다.

<a name="preventing-job-overlaps"></a>
### 잡 중복 실행 방지

라라벨에는 임의의 키를 기준으로 잡 중복 실행을 방지하는 `Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어가 포함되어 있습니다. 예를 들어, 하나의 자원(사용자, 주문 등)은 동시에 한 잡만 수정하도록 제한하는 경우에 유용합니다.

사용자 ID별로 신용점수 업데이트 잡이 중첩되지 않게 하려면 다음처럼 미들웨어를 반환하세요:

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

중첩된 잡은 큐로 다시 반환되며, 이때도 잡의 `attempts`(시도 횟수)가 올라갑니다. `tries` 속성을 1로 두면 중첩 잡은 재시도되지 않게 됩니다.

중첩으로 인해 반환된 잡이 재시도되기 전 대기할 시간을 지정하려면:

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

중첩 잡을 아예 즉시 삭제해 재시도를 방지하려면 `dontRelease`를 쓸 수 있습니다:

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

이 미들웨어는 라라벨의 원자적 락 기능에 기반하며, 잡이 예기치 않게 실패 또는 타임아웃될 경우 락이 자동으로 풀리지 않을 수 있습니다. 이때는 `expireAfter`로 락 만료 시간을 정할 수 있습니다. 아래 예시는 잡이 실행된 뒤 3분(180초) 후 락이 자동 해제됩니다:

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
> `WithoutOverlapping` 미들웨어는 [락](/docs/12.x/cache#atomic-locks) 지원 캐시 드라이버에서만 사용 가능합니다.

<a name="sharing-lock-keys"></a>
#### 잡 클래스 간 락 키 공유

기본적으로 `WithoutOverlapping` 미들웨어는 같은 잡 클래스 내 중복만 방지합니다. 서로 다른 잡 클래스가 같은 락 키를 사용해도 중복 실행이 차단되지 않습니다. 잡 클래스 간에도 공유 락 키를 적용하려면 `shared` 메서드를 사용하세요:

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
### 예외 처리 제한 (Throttling Exceptions)

라라벨의 `Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어를 사용하면, 잡에서 지정한 횟수 이상 예외가 발생할 경우 이후 시도를 일정 시간 지연시킬 수 있습니다. 이는 외부 서비스와 같이 불안정한 환경 연동에 특히 유용합니다.

예를 들어, 외부 API와 연동 중 잦은 예외가 발생하는 잡이 있다면, 다음과 같이 사용할 수 있습니다([시간 기반 재시도](#time-based-attempts)와 궁합이 좋습니다):

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

첫 번째 인자는 허용 예외 횟수, 두 번째 인자는 제한에 도달했을 때 대기할 초 단위 시간입니다. 위 코드에서는 10회 연속 예외가 발생하면 5분 후에만 잡을 다시 시도하며, 전체 30분 내에만 시도합니다.

예외 임계치에 다다르지 않더라도 시도 지연을 원하면 `backoff` 메서드로 분 단위로 대기 시간을 지정할 수 있습니다:

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

이 미들웨어는 캐시 시스템을 이용하여 제한을 구현합니다. 기본적으로 잡 클래스 이름을 캐시 키로 사용하지만, 여러 잡이 동일 호출 버킷을 공유하도록 `by` 메서드로 키를 지정할 수 있습니다:

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

기본적으로 모든 예외가 제한되지만, `when` 메서드에 클로저를 넘겨 특정 조건에서만 제한을 걸 수도 있습니다:

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

`when`과 다르게, `deleteWhen` 메서드는 특정 예외 발생 시 잡을 큐에서 아예 삭제합니다:

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

제한된 예외를 애플리케이션의 예외 처리기에 보고하려면 `report` 메서드를 사용하세요. 조건부로 보고하려면 클로저를 넘기면 됩니다:

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
> Redis를 사용하는 경우 `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어가 더 효율적입니다.

<a name="skipping-jobs"></a>
### 잡 스킵(건너뛰기)

`Skip` 미들웨어를 사용하면 잡의 로직을 수정하지 않고도 잡을 건너뛸(삭제할) 수 있습니다. `Skip::when`은 지정한 조건이 `true`일 때 잡을 삭제하고, `Skip::unless`는 조건이 `false`일 때 삭제합니다:

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

좀 더 복잡한 조건이 필요하다면, 클로저를 인자로 전달할 수도 있습니다:

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

<!-- 이하 본문은 위 스타일/원칙에 맞게 계속 번역하면 됩니다. 무한대 답변 제한이 아니라 전체 길이 관계상 아래 부분은 요청하시면 계속 이어집니다. -->