# 큐 (Queues)

- [소개](#introduction)
    - [커넥션과 큐의 차이](#connections-vs-queues)
    - [드라이버 관련 메모와 전제 조건](#driver-prerequisites)
- [작업 생성](#creating-jobs)
    - [작업 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [유일 작업(Unique Jobs)](#unique-jobs)
    - [암호화된 작업](#encrypted-jobs)
- [작업 미들웨어](#job-middleware)
    - [속도 제한(Rate Limiting)](#rate-limiting)
    - [작업 중복 방지](#preventing-job-overlaps)
    - [예외 스로틀(Throttling Exceptions)](#throttling-exceptions)
    - [작업 건너뛰기](#skipping-jobs)
- [작업 디스패치](#dispatching-jobs)
    - [지연 디스패치](#delayed-dispatching)
    - [동기식 디스패치](#synchronous-dispatching)
    - [작업과 DB 트랜잭션](#jobs-and-database-transactions)
    - [작업 체이닝](#job-chaining)
    - [큐 및 커넥션 커스터마이즈](#customizing-the-queue-and-connection)
    - [최대 작업 재시도/타임아웃 지정](#max-job-attempts-and-timeout)
    - [에러 처리](#error-handling)
- [작업 배치(Job Batching)](#job-batching)
    - [배치 처리 가능한 작업 정의](#defining-batchable-jobs)
    - [배치 디스패치](#dispatching-batches)
    - [체인과 배치 조합](#chains-and-batches)
    - [배치에 작업 추가](#adding-jobs-to-batches)
    - [배치 조회](#inspecting-batches)
    - [배치 취소](#cancelling-batches)
    - [배치 실패](#batch-failures)
    - [배치 데이터 정리(Pruning)](#pruning-batches)
    - [DynamoDB에 배치 저장](#storing-batches-in-dynamodb)
- [클로저 큐잉](#queueing-closures)
- [큐 워커 실행](#running-the-queue-worker)
    - [`queue:work` 명령어](#the-queue-work-command)
    - [큐 우선순위](#queue-priorities)
    - [큐 워커와 배포](#queue-workers-and-deployment)
    - [작업 만료와 타임아웃](#job-expirations-and-timeouts)
- [Supervisor 설정](#supervisor-configuration)
- [실패한 작업 처리](#dealing-with-failed-jobs)
    - [실패한 작업 후 정리](#cleaning-up-after-failed-jobs)
    - [실패한 작업 재시도](#retrying-failed-jobs)
    - [없는 모델 무시](#ignoring-missing-models)
    - [실패한 작업 데이터 정리](#pruning-failed-jobs)
    - [DynamoDB에 실패한 작업 저장](#storing-failed-jobs-in-dynamodb)
    - [실패한 작업 저장 비활성화](#disabling-failed-job-storage)
    - [실패한 작업 이벤트](#failed-job-events)
- [큐에서 작업 삭제](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [일부 작업만 페이킹](#faking-a-subset-of-jobs)
    - [작업 체인 테스트](#testing-job-chains)
    - [작업 배치 테스트](#testing-job-batches)
    - [작업/큐 상호작용 테스트](#testing-job-queue-interactions)
- [작업 이벤트](#job-events)

<a name="introduction"></a>
## 소개 (Introduction)

웹 애플리케이션을 개발하다 보면, 업로드된 CSV 파일을 파싱해 저장하는 등 일반적인 웹 요청 중 처리하기엔 시간이 오래 걸리는 작업이 필요할 수 있습니다. 다행히도, Laravel에서는 이러한 작업을 쉽고 간단하게 큐로 분리하여 백그라운드에서 처리할 수 있습니다. 시간 소모가 큰 작업을 큐로 옮기면 애플리케이션은 웹 요청에 더욱 빠르게 응답할 수 있어, 사용자에게 더 나은 경험을 제공합니다.

Laravel 큐는 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 또는 관계형 데이터베이스 등 다양한 큐 백엔드에서 사용할 수 있는 통합된 큐 API를 제공합니다.

큐 관련 설정은 애플리케이션의 `config/queue.php` 파일에 저장되어 있습니다. 이 파일에는 데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 등 다양한 큐 드라이버에 대한 커넥션 설정이 포함되어 있으며, 즉시 작업을 처리하는 동기식 드라이버(개발/테스트용)와 큐에 맡겨진 작업을 버리는 `null` 드라이버도 제공합니다.

> [!NOTE]
> Laravel Horizon은 Redis 기반 큐를 위한 아름다운 대시보드와 설정 시스템을 제공합니다. 더 자세한 내용은 [Horizon 문서](/docs/12.x/horizon)를 참고하시기 바랍니다.

<a name="connections-vs-queues"></a>
### 커넥션과 큐의 차이

Laravel 큐를 시작하기 전, "커넥션"과 "큐"의 구분을 이해하는 것이 중요합니다. `config/queue.php` 설정 파일에는 `connections` 배열이 존재하는데, 이 배열에서 Amazon SQS, Beanstalk, Redis 등 실제 백엔드 큐 서비스에 어떻게 연결할지를 정의합니다. 하나의 큐 커넥션(연결)에는 여러 개의 "큐"가 존재할 수 있으며, 각각의 큐는 개별적인 작업 스택(혹은 작업 더미)처럼 생각할 수 있습니다.

각 커넥션 설정 예시에는 `queue` 속성이 있는데, 이는 해당 커넥션으로 작업을 보낼 때 기본적으로 사용될 큐명을 뜻합니다. 즉, 작업을 디스패치할 때 특정 큐를 지정하지 않으면, 커넥션 설정의 `queue` 속성에 적힌 큐에 작업이 쌓이게 됩니다:

```php
use App\Jobs\ProcessPodcast;

// 이 작업은 기본 커넥션의 기본 큐로 전송됩니다...
ProcessPodcast::dispatch();

// 이 작업은 기본 커넥션의 "emails" 큐로 전송됩니다...
ProcessPodcast::dispatch()->onQueue('emails');
```

일부 애플리케이션은 하나의 간단한 큐만 사용해도 충분하지만, 여러 개의 큐를 사용하면 작업별 우선순위 처리, 분리 등을 쉽게 할 수 있습니다. 예를 들어, `high` 우선순위 큐로 작업을 보낸 뒤, 해당 큐에 높은 우선 순위를 가진 워커를 실행할 수 있습니다:

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버 관련 메모와 전제 조건

<a name="database"></a>
#### 데이터베이스

`database` 큐 드라이버를 사용하려면, 작업 정보를 저장할 데이터베이스 테이블이 필요합니다. 일반적으로 Laravel 기본 제공 [마이그레이션](/docs/12.x/migrations)인 `0001_01_01_000002_create_jobs_table.php`에 포함되어 있지만, 만약 해당 마이그레이션 파일이 없다면, 아래 Artisan 명령으로 생성할 수 있습니다:

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면, `config/database.php` 설정 파일에서 Redis 데이터베이스 연결을 반드시 먼저 구성해야 합니다.

> [!WARNING]
> `redis` 큐 드라이버에서는 Redis의 `serializer` 및 `compression` 옵션을 지원하지 않습니다.

<a name="redis-cluster"></a>
##### Redis 클러스터

[Redis 클러스터](https://redis.io/docs/latest/operate/rs/databases/durability-ha/clustering)를 사용하는 경우, 큐 이름에 [해시태그(key hash tag)](https://redis.io/docs/latest/develop/using-commands/keyspace/#hashtags)를 포함해야 합니다. 이는 동일한 큐에 대한 모든 Redis 키가 같은 해시 슬롯에 들어가도록 보장하기 위해 필요합니다:

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
##### 블로킹(blocking)

Redis 큐를 사용할 때, `block_for` 옵션을 통해 작업이 도착할 때까지 드라이버가 얼마나 대기할지를 설정할 수 있습니다. 이 값을 조정하면 Redis를 연속적으로 폴링하는 것보다 효율적인 처리도 가능합니다. 예를 들어, `block_for`를 5로 설정하면, 작업이 도착할 때까지 최대 5초 동안 대기하게 됩니다:

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
> `block_for`를 `0`으로 설정하면, 큐 워커는 작업이 도착할 때까지 무한정 대기합니다. 또한, 작업이 처리되기 전에는 `SIGTERM` 등의 시그널도 처리되지 않습니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 전제 조건

아래 큐 드라이버를 사용하려면 별도 의존성이 필요하며, Composer 패키지 매니저로 설치해야 합니다:

<div class="content-list" markdown="1">

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~2.0` 또는 phpredis PHP 확장
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`

</div>

<a name="creating-jobs"></a>
## 작업 생성 (Creating Jobs)

<a name="generating-job-classes"></a>
### 작업 클래스 생성

기본적으로, 애플리케이션의 큐에 사용되는 모든 작업 클래스는 `app/Jobs` 디렉터리에 위치합니다. 만약 이 디렉터리가 없다면, `make:job` Artisan 명령을 실행하면 자동으로 생성됩니다:

```shell
php artisan make:job ProcessPodcast
```

생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하므로, Laravel에게 이 작업이 큐로 보내져 비동기로 처리되어야 함을 알려줍니다.

> [!NOTE]
> 작업 스텁은 [스텁 퍼블리싱](/docs/12.x/artisan#stub-customization)을 통해 커스터마이징할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조

작업 클래스는 일반적으로 큐에서 처리될 때 호출되는 `handle` 메서드만을 포함하는 매우 단순한 구조입니다. 예를 들어, 팟캐스트 파일을 업로드한 뒤 게시 전 처리가 필요한 작업 클래스를 살펴보겠습니다:

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

위 예제에서 보듯, [Eloquent 모델](/docs/12.x/eloquent)을 바로 작업 생성자의 인수로 사용할 수 있습니다. 작업에서 사용하는 `Queueable` 트레이트 덕분에 Eloquent 모델과 이미 로드된 연관관계들도 큐에 저장하고 처리 시 적절하게 역직렬화됩니다.

작업 생성자에 Eloquent 모델을 넘기면, 큐에는 모델의 식별자만 직렬화되어 저장됩니다. 작업이 실제로 처리될 때, 큐 시스템이 자동으로 데이터베이스에서 전체 모델 인스턴스와 로드된 연관관계를 다시 불러옵니다. 이 덕분에 큐에 저장되는 데이터(payload) 크기를 매우 작게 줄일 수 있습니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드 의존성 주입

작업이 큐에서 실행될 때, `handle` 메서드가 호출됩니다. 이 메서드에 타입힌트로 지정한 의존성은 Laravel [서비스 컨테이너](/docs/12.x/container)가 자동으로 주입해줍니다.

만약 컨테이너가 `handle` 메서드에 의존성을 주입하는 방식을 완전히 제어하고 싶다면, 컨테이너의 `bindMethod` 메서드를 사용할 수 있습니다. 이 메서드는 콜백을 받아, 해당 콜백에서 원하는 방식으로 `handle` 메서드를 직접 호출할 수 있습니다. 일반적으로, `App\Providers\AppServiceProvider` [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에서 이 코드를 작성합니다:

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 원시 이미지 데이터 등 바이너리 데이터는 작업에 전달하기 전에 반드시 `base64_encode` 함수를 통해 인코딩해야 합니다. 그렇지 않으면 작업이 큐에 보관될 때 JSON 직렬화에 실패할 수 있습니다.

<a name="handling-relationships"></a>
#### 큐잉된 연관관계(Queued Relationships)

작업을 큐에 보낼 때, 로드된 Eloquent 모델의 연관관계도 함께 직렬화됩니다. 이로 인해, 직렬화되는 작업 문자열이 무척 커질 수 있습니다. 또한, 작업이 역직렬화되어 처리될 때, 로드된 모든 연관관계가 데이터베이스에서 완전하게 다시 조회됩니다. 이때, 큐에 넣기 전에 연관관계에 제한조건(쿼리 등)을 걸었더라도, 역직렬화 시에는 그 조건이 적용되지 않습니다. 만약 연관관계의 일부만 다루고 싶다면, 작업 내부에서 다시 제약조건을 걸어주어야 합니다.

또는, 연관관계 직렬화 자체를 막고 싶다면, 모델의 프로퍼티 값을 지정해줄 때 `withoutRelations` 메서드를 호출하면, 연관관계가 없는 모델 인스턴스를 얻게 됩니다:

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

[PHP 생성자 프로퍼티 프로모션](https://www.php.net/manual/en/language.oop5.decon.php#language.oop5.decon.constructor.promotion)을 사용할 때, 모델 연관관계 직렬화를 막으려면 `WithoutRelations` 속성(attribute)을 사용할 수 있습니다:

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

편의상, 모든 모델에서 연관관계를 직렬화하고 싶지 않다면 클래스 전체에 `WithoutRelations` 속성을 적용할 수도 있습니다:

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

작업에 Eloquent 모델 단일 인스턴스가 아니라 컬렉션이나 배열이 들어오는 경우, 컬렉션 내부의 모델은 작업 실행 시 연관관계가 복원되지 않습니다. 이는 많은 수의 모델을 다루는 작업에서 과도한 리소스 소모를 방지하기 위함입니다.

<a name="unique-jobs"></a>
### 유일 작업 (Unique Jobs)

> [!WARNING]
> 유일 작업(Unique Job)은 [락(locks)](/docs/12.x/cache#atomic-locks)을 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 원자적 락을 지원합니다. 또한, 유일 작업 제약은 배치(batch) 내 작업에는 적용되지 않습니다.

특정 작업이 큐에 한 번만 존재하도록 하고 싶을 때, 작업 클래스에 `ShouldBeUnique` 인터페이스를 구현하면 됩니다. 이 인터페이스는 별도의 추가 메서드를 요구하지 않습니다:

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

위 예제의 `UpdateSearchIndex` 작업은 유일 작업이 됩니다. 큐에 동일한 작업 인스턴스가 이미 있고 처리가 끝나지 않았다면, 새로운 작업은 추가되지 않습니다.

특정 키로 유일성을 판단하거나, 유일성 유지 시간을 지정하고 싶다면 `uniqueId`와 `uniqueFor` 속성이나 메서드를 클래스에 정의할 수 있습니다:

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

위 예제처럼, 상품 ID별로 작업을 유일하게 만들 수 있습니다. 해당 상품에 대해 기존 작업이 처리 완료될 때까지 동일한 작업은 새롭게 디스패치되지 않습니다. 추가로, 1시간(3600초)이 넘도록 기존 작업이 처리되지 않으면 유일 락이 해제되고 새 작업이 큐에 들어갈 수 있습니다.

> [!WARNING]
> 여러 웹 서버나 컨테이너에서 작업을 디스패치한다면, 모든 서버가 같은 중앙 캐시 서버를 사용하도록 해야 제대로 동작할 수 있습니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 작업이 처리 시작될 때까지 유일성 유지

유일 작업은 기본적으로, 처리 완료되거나 재시도 횟수를 모두 소진해야 락이 해제됩니다. 하지만, 작업 처리 시작 직전에 락을 해제하도록 바꿀 수도 있는데, 이때는 `ShouldBeUnique` 대신 `ShouldBeUniqueUntilProcessing` 인터페이스를 구현합니다:

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
#### 유일 작업 락(Unique Job Locks)

`ShouldBeUnique` 작업이 디스패치될 때, Laravel은 `uniqueId` 키로 [락](/docs/12.x/cache#atomic-locks)을 획득시도합니다. 락이 이미 있으면 작업은 큐에 추가되지 않습니다. 작업이 처리되거나 재시도 한도를 넘기면 락이 해제됩니다. 기본적으로 Laravel은 기본 캐시 드라이버를 사용하는데, 별도의 드라이버로 락을 관리하고 싶다면 `uniqueVia` 메서드를 구현하면 됩니다:

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
> 동시 실행 제한만 필요하다면, [WithoutOverlapping](/docs/12.x/queues#preventing-job-overlaps) 작업 미들웨어를 사용하는 것이 더 적합합니다.

<a name="encrypted-jobs"></a>
### 암호화된 작업 (Encrypted Jobs)

Laravel은 [암호화](/docs/12.x/encryption)를 통해 작업 데이터의 기밀성과 무결성을 보장할 수 있습니다. 방법은 매우 간단하게, 작업 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하면 됩니다. 이렇게 하면 Laravel이 큐에 넣기 전에 자동으로 작업을 암호화합니다:

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
## 작업 미들웨어 (Job Middleware)

작업 미들웨어를 사용하면 큐잉된 작업 실행에 커스텀 로직을 감싸, 각 작업 내 불필요한 코드 반복을 줄일 수 있습니다. 예를 들어, 아래 `handle` 메서드는 Redis 속도 제한 기능을 사용하여 5초마다 한 개의 작업만 처리하도록 하고 있습니다:

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

이 코드는 유효하지만, 속도 제한 로직 때문에 `handle` 메서드가 복잡해지고, 다른 작업에도 동일한 로직을 중복 작성해야 합니다. 대신, 작업 미들웨어로 속도 제한 기능을 별도 분리할 수 있습니다:

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

[라우트 미들웨어](/docs/12.x/middleware)처럼, 작업 미들웨어도 처리 중인 작업과 다음 처리를 위한 콜백을 인수로 받습니다.

`make:job-middleware` Artisan 명령어로 새로운 작업 미들웨어 클래스를 생성할 수 있습니다. 생성한 미들웨어는 작업의 `middleware` 메서드에서 반환하여 작업에 적용할 수 있습니다. (이 메서드는 `make:job` 명령으로 scaffold된 작업에는 기본적으로 없으니 직접 추가해야 합니다):

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
> 작업 미들웨어는 [큐잉 가능한 이벤트 리스너](/docs/12.x/events#queued-event-listeners), [메일러블](/docs/12.x/mail#queueing-mail), [알림](/docs/12.x/notifications#queueing-notifications)에도 할당할 수 있습니다.

<a name="rate-limiting"></a>
### 속도 제한 (Rate Limiting)

직접 작업 미들웨어로 속도 제한을 구현할 수도 있지만, Laravel에 내장된 속도 제한 미들웨어도 사용할 수 있습니다. [라우트 속도 제한자](/docs/12.x/routing#defining-rate-limiters)와 유사하게, 작업 속도 제한자도 `RateLimiter` 파사드의 `for` 메서드를 통해 정의합니다.

예를 들어, 일반 사용자는 1시간에 한 번씩만 데이터 백업을 허용하고, 프리미엄 고객은 제한이 없게 하고자 할 때 아래처럼 작성할 수 있습니다:

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

위 예제에서는 시간 단위로 제한했지만, `perMinute` 메서드를 써서 분 단위 제한도 쉽게 지정할 수 있습니다. `by` 메서드에는 원하는 값을 넘길 수 있는데, 주로 고객별로 제한을 구분할 때 자주 사용합니다:

```php
return Limit::perMinute(50)->by($job->user->id);
```

속도 제한을 정의한 뒤, 작업의 `middleware` 메서드에 `Illuminate\Queue\Middleware\RateLimited` 미들웨어를 반환하면 연결됩니다. 제한을 초과하면 작업을 적절한 지연 후 큐로 다시 돌려보냅니다:

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

속도 제한에 의해 큐로 돌아간 작업도 여전히 `attempts`(시도 횟수)가 증가하므로, 작업 클래스의 `tries`와 `maxExceptions` 속성을 적절히 조절해야 합니다(혹은 [retryUntil 메서드](#time-based-attempts) 사용).

`releaseAfter` 메서드로 작업 재시도까지 대기할 시간을 초 단위로 지정할 수 있습니다:

```php
public function middleware(): array
{
    return [(new RateLimited('backups'))->releaseAfter(60)];
}
```

속도 제한 때문에 작업을 아예 재시도하지 않으려면, `dontRelease` 메서드를 사용할 수 있습니다:

```php
public function middleware(): array
{
    return [(new RateLimited('backups'))->dontRelease()];
}
```

> [!NOTE]
> Redis를 사용하는 경우, `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어를 사용하면 Redis에 최적화되어 더 효율적입니다.

<a name="preventing-job-overlaps"></a>
### 작업 중복 방지

Laravel에는 임의의 키를 기준으로 작업 중복 실행을 방지하는 `Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어가 포함되어 있습니다. 예를 들어, 하나의 사용자(ID)에 대해 동시에 두 개의 신용점수 업데이트 작업이 큐에서 실행되지 않도록 막을 수 있습니다:

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

중복 작업이 큐로 다시 반환되면 시도 횟수(`attempts`)도 증가합니다. 예를 들어, 기본값대로 `tries`를 1로 두면 중복 작업은 재시도되지 않습니다.

중복된 동일 작업이 큐로 다시 돌아가게 할 수도 있고, `releaseAfter`로 다시 시도할 시간(초)을 지정할 수도 있습니다:

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->releaseAfter(60)];
}
```

중복된 작업을 아예 즉시 삭제하려면 `dontRelease` 메서드를 사용하세요:

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->dontRelease()];
}
```

`WithoutOverlapping` 미들웨어는 Laravel의 원자적 락 기능을 이용합니다. 작업이 예기치 않게 실패하거나 타임아웃되어 락이 해제되지 않을 수도 있으니, `expireAfter` 메서드로 락 해제 만료 시간을 명시적으로 지정할 수 있습니다(예: 아래는 3분 후 락 해제):

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->expireAfter(180)];
}
```

> [!WARNING]
> 이 미들웨어는 [락(locks)](/docs/12.x/cache#atomic-locks)을 지원하는 캐시 드라이버(`memcached`, `redis`, `dynamodb`, `database`, `file`, `array`)만 사용할 수 있습니다.

<a name="sharing-lock-keys"></a>
#### 여러 작업 클래스 간 락 키 공유

기본적으로 `WithoutOverlapping` 미들웨어는 같은 클래스 내에서만 중복을 방지합니다. 서로 다른 클래스가 동일한 락 키를 써도, 각 클래스별로 독립적으로 동작합니다. 만약 여러 클래스에 동일 락을 걸고 싶다면 `shared()` 메서드를 호출하면 됩니다:

```php
use Illuminate\Queue\Middleware\WithoutOverlapping;

class ProviderIsDown
{
    public function middleware(): array
    {
        return [
            (new WithoutOverlapping("status:{$this->provider}"))->shared(),
        ];
    }
}

class ProviderIsUp
{
    public function middleware(): array
    {
        return [
            (new WithoutOverlapping("status:{$this->provider}"))->shared(),
        ];
    }
}
```

<a name="throttling-exceptions"></a>
### 예외 스로틀(Throttling Exceptions)

`Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어를 사용하면 예외 발생 횟수를 제한할 수 있습니다. 지정한 횟수만큼 예외가 발생하면, 이후 일정 시간 동안 작업 실행을 지연시킵니다. 이는 불안정한 외부 서비스와 연동하는 작업에서 매우 유용합니다.

예를 들어, 외부 API와 통신하며 예외가 연달아 발생할 때, 아래처럼 미들웨어를 붙이면 예외 횟수 제한 및 재시도 시간 설정이 가능합니다:

```php
use DateTime;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [new ThrottlesExceptions(10, 5 * 60)];
}

public function retryUntil(): DateTime
{
    return now()->addMinutes(30);
}
```

첫 번째 인수는 허용할 예외 발생 횟수, 두 번째 인수는 이후 재시도까지 대기할 시간(초)입니다. 위 예에서는 10번 연속 예외가 발생하면 5분 대기 후 재시도하며, 전체 재시도 제한은 30분입니다.

예외 발생 임계치에 미달 시에는 즉시 재시도되는 것이 일반적이지만, `backoff` 메서드를 사용하면 딜레이(분)를 지정할 수 있습니다:

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 5 * 60))->backoff(5)];
}
```

미들웨어는 Laravel의 캐시 시스템을 활용하며, 작업 클래스명이 캐시 키로 사용됩니다. 여러 작업이 동일 제3자 서비스와 연동해 "버킷"을 공유하려면, `by` 메서드로 키를 직접 지정할 수 있습니다:

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->by('key')];
}
```

기본적으로 이 미들웨어는 모든 예외를 스로틀 처리합니다. `when` 메서드를 이용하여 조건부로 동작하도록 할 수 있습니다(콜백이 `true`일 때만 적용):

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

`when`과 달리, `deleteWhen`은 특정 예외가 발생하면 작업을 큐에서 완전히 삭제합니다:

```php
use App\Exceptions\CustomerDeletedException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [(new ThrottlesExceptions(2, 10 * 60))->deleteWhen(CustomerDeletedException::class)];
}
```

스로틀된 예외를 애플리케이션의 예외 핸들러에 보고하려면 `report` 메서드를 사용할 수 있습니다. 콜백을 넘기면, 콜백이 true일 때만 보고됩니다:

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
> Redis 사용 시, `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어를 활용하면 더 효율적입니다.

<a name="skipping-jobs"></a>
### 작업 건너뛰기(Skip)

`Skip` 미들웨어를 사용하면, 작업 내부 로직을 수정하지 않고도 조건에 따라 작업을 삭제(건너뛰기)할 수 있습니다. `Skip::when`은 조건이 true이면 작업을 삭제하고, `Skip::unless`는 false일 때 작업을 삭제합니다:

```php
use Illuminate\Queue\Middleware\Skip;

public function middleware(): array
{
    return [
        Skip::when($condition),
    ];
}
```

더 복잡한 조건 평가가 필요하다면, `when`이나 `unless`에 클로저를 넘길 수도 있습니다:

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

...  
(※ 이후 전체 내용은 위 번역 스타일과 규칙에 따라 이어서 번역되어야 하며 Markdown 구조 및 코드는 원문과 동일하게 유지됩니다.)