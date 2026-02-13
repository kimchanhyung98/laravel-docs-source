# 큐 (Queues)

- [소개](#introduction)
    - [커넥션과 큐의 차이](#connections-vs-queues)
    - [드라이버별 참고 사항 및 사전 조건](#driver-prerequisites)
- [잡 생성하기](#creating-jobs)
    - [잡 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [유일 잡(Unique Jobs)](#unique-jobs)
    - [암호화된 잡](#encrypted-jobs)
- [잡 미들웨어](#job-middleware)
    - [속도 제한(Rate Limiting)](#rate-limiting)
    - [잡 중복 실행 방지](#preventing-job-overlaps)
    - [예외 제한(Throttling Exceptions)](#throttling-exceptions)
    - [잡 건너뛰기](#skipping-jobs)
- [잡 디스패치(Dispatch)](#dispatching-jobs)
    - [지연 디스패치(Delayed Dispatching)](#delayed-dispatching)
    - [동기 디스패치(Synchronous Dispatching)](#synchronous-dispatching)
    - [잡과 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [잡 체이닝(Chaining)](#job-chaining)
    - [큐/커넥션 커스터마이징](#customizing-the-queue-and-connection)
    - [최대 시도/타임아웃 지정](#max-job-attempts-and-timeout)
    - [SQS FIFO 및 공정 큐](#sqs-fifo-and-fair-queues)
    - [큐 페일오버](#queue-failover)
    - [에러 핸들링](#error-handling)
- [잡 배치(Batching)](#job-batching)
    - [배치 가능한 잡 정의](#defining-batchable-jobs)
    - [배치 디스패치](#dispatching-batches)
    - [체인과 배치](#chains-and-batches)
    - [배치에 잡 추가](#adding-jobs-to-batches)
    - [배치 조회](#inspecting-batches)
    - [배치 취소](#cancelling-batches)
    - [배치 실패](#batch-failures)
    - [배치 정리(Pruning)](#pruning-batches)
    - [DynamoDB에 배치 저장](#storing-batches-in-dynamodb)
- [클로저 큐잉](#queueing-closures)
- [큐 워커 실행](#running-the-queue-worker)
    - [`queue:work` 명령어](#the-queue-work-command)
    - [큐 우선순위](#queue-priorities)
    - [큐 워커와 배포](#queue-workers-and-deployment)
    - [잡 만료/타임아웃](#job-expirations-and-timeouts)
    - [큐 워커 일시정지 및 재개](#pausing-and-resuming-queue-workers)
- [Supervisor 구성](#supervisor-configuration)
- [실패한 잡 처리](#dealing-with-failed-jobs)
    - [실패 잡 후처리](#cleaning-up-after-failed-jobs)
    - [실패 잡 재시도](#retrying-failed-jobs)
    - [누락된 모델 무시](#ignoring-missing-models)
    - [실패 잡 정리(Pruning)](#pruning-failed-jobs)
    - [DynamoDB에 실패 잡 저장](#storing-failed-jobs-in-dynamodb)
    - [실패 잡 저장 비활성화](#disabling-failed-job-storage)
    - [실패 잡 이벤트](#failed-job-events)
- [큐에서 잡 삭제](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [일부 잡만 페이크로 처리](#faking-a-subset-of-jobs)
    - [잡 체인 테스트](#testing-job-chains)
    - [잡 배치 테스트](#testing-job-batches)
    - [잡/큐 상호작용 테스트](#testing-job-queue-interactions)
- [잡 이벤트](#job-events)

<a name="introduction"></a>
## 소개 (Introduction)

웹 애플리케이션을 개발하다 보면, 업로드한 CSV 파일을 파싱하고 저장하는 것처럼 일반적인 웹 요청 중 처리하기에는 시간이 오래 걸리는 작업이 있을 수 있습니다. Laravel은 이러한 작업을 큐에 넣어 백그라운드에서 실행할 수 있는 큐어블(큐잉 가능한) 잡을 손쉽게 만들 수 있도록 지원합니다. 시간이 많이 소요되는 작업을 큐로 옮기면, 애플리케이션은 훨씬 빠른 응답을 제공할 수 있고 사용자 경험도 크게 향상됩니다.

Laravel 큐는 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 또는 관계형 데이터베이스 등 다양한 큐 백엔드에서 사용할 수 있도록 통합 큐 API를 제공합니다.

큐 관련 설정은 애플리케이션의 `config/queue.php` 구성 파일에 저장됩니다. 이 파일에는 데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 등 다양한 큐 드라이버용 커넥션 설정이 포함되어 있습니다. 즉시 잡을 실행하는 동기(synchronous) 드라이버(개발/테스트용)와, 큐에 추가된 잡을 모두 폐기하는 `null` 큐 드라이버도 제공합니다.

> [!NOTE]
> Laravel Horizon은 Redis 기반 큐를 위한 아름다운 대시보드와 설정 시스템입니다. 자세한 내용은 [Horizon 문서](/docs/master/horizon)를 참고하세요.

<a name="connections-vs-queues"></a>
### 커넥션과 큐의 차이

Laravel 큐를 시작하기 전에, "커넥션(connection)"과 "큐(queue)"의 차이를 이해하는 것이 중요합니다. `config/queue.php` 파일에는 `connections`라는 배열이 있으며, 이 옵션에서 Amazon SQS, Beanstalk, Redis와 같은 백엔드 큐 서비스의 커넥션을 정의합니다. 한 큐 커넥션에는 여러 개의 "큐"가 있을 수 있으며, 이것은 여러 개의 잡 스택 혹은 작업 더미로 생각할 수 있습니다.

각 커넥션 설정 예제마다 `queue` 속성이 있습니다. 이는 해당 커넥션으로 잡을 보낼 때 기본적으로 사용될 큐 이름입니다. 즉, 디스패치할 때 큐를 명시하지 않으면 커넥션 설정의 `queue` 속성에 정의된 큐에 잡이 쌓입니다.

```php
use App\Jobs\ProcessPodcast;

// 이 잡은 기본 커넥션의 기본 큐로 전송됩니다...
ProcessPodcast::dispatch();

// 이 잡은 기본 커넥션의 "emails" 큐로 전송됩니다...
ProcessPodcast::dispatch()->onQueue('emails');
```

어떤 애플리케이션은 하나의 단순한 큐만 사용할 수도 있지만, 잡을 여러 개의 큐에 나눠 넣는 것은 작업 우선순위나 작업 구분을 하고 싶을 때 매우 유용합니다. Laravel 큐 워커는 우선순위에 따라 특정 큐만 처리하도록 설정할 수 있습니다. 예를 들어, `high` 큐로 잡을 보내고, 해당 큐를 우선적으로 처리하는 워커를 다음과 같이 실행할 수 있습니다.

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버별 참고 사항 및 사전 조건

<a name="database"></a>
#### 데이터베이스

`database` 큐 드라이버를 사용하려면 잡을 저장할 데이터베이스 테이블이 필요합니다. Laravel에서는 기본적으로 제공되는 `0001_01_01_000002_create_jobs_table.php` [마이그레이션](/docs/master/migrations)에 포함되어 있습니다. 만약 해당 마이그레이션이 없다면, 아래와 같이 `make:queue-table` Artisan 명령어로 생성할 수 있습니다.

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면, `config/database.php` 파일에 Redis 데이터베이스 커넥션을 설정해야 합니다.

> [!WARNING]
> Redis의 `serializer` 및 `compression` 옵션은 큐 드라이버에서는 지원되지 않습니다.

<a name="redis-cluster"></a>
##### Redis 클러스터

[Redis 클러스터](https://redis.io/docs/latest/operate/rs/databases/durability-ha/clustering)를 사용하는 경우, 큐 이름에는 [키 해시 태그](https://redis.io/docs/latest/develop/using-commands/keyspace/#hashtags)를 포함해야 합니다. 이는 하나의 큐에 대한 모든 Redis 키가 동일한 해시 슬롯에 배치되도록 보장하기 위함입니다.

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

Redis 큐를 사용할 때 `block_for` 옵션을 통해, 잡이 준비될 때까지 드라이버가 얼마나 대기해야 하는지 지정할 수 있습니다. 이 값을 조정하면 Redis 데이터베이스를 계속 폴링하는 것보다 더 효율적으로 큐를 관리할 수 있습니다. 예를 들어, 5로 설정하면 잡이 준비될 때까지 최대 5초간 대기하게 됩니다.

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
> `block_for` 값을 `0`으로 설정하면, 잡이 도착할 때까지 무한히 대기하게 됩니다. 이때, `SIGTERM`과 같은 시그널은 다음 잡이 처리될 때까지 반영되지 않습니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 사전 조건

아래 큐 드라이버들은 반드시 필요한 Composer 패키지를 설치해야 사용 가능합니다.

<div class="content-list" markdown="1">

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~2.0` 또는 phpredis PHP 확장
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`

</div>

<a name="creating-jobs"></a>
## 잡 생성하기 (Creating Jobs)

<a name="generating-job-classes"></a>
### 잡 클래스 생성

애플리케이션의 모든 큐어블 잡은 기본적으로 `app/Jobs` 디렉터리에 저장됩니다. 만약 이 디렉터리가 없다면, `make:job` Artisan 명령어를 실행할 때 자동으로 생성됩니다.

```shell
php artisan make:job ProcessPodcast
```

생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하여, Laravel에게 해당 잡이 비동기적으로 큐에 올라가야 함을 알립니다.

> [!NOTE]
> 잡 스텁(stub)은 [스텁 퍼블리싱](/docs/master/artisan#stub-customization)을 사용해 커스터마이즈할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조

잡 클래스는 대체로 간단하며, 큐가 잡을 처리할 때 실행되는 `handle` 메서드가 핵심입니다. 다음은 업로드된 팟캐스트 파일을 처리하는 가상의 잡 클래스 예시입니다.

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

이 예시처럼, 잡의 생성자에 [Eloquent 모델](/docs/master/eloquent)을 직접 전달할 수 있습니다. `Queueable` 트레이트 때문에, Eloquent 모델과 로드된 연관관계 정보가 잡 직렬화/역직렬화 시 안전하게 처리됩니다.

잡 생성자에 Eloquent 모델이 들어가면, 해당 모델의 식별자만 큐에 직렬화되고, 잡이 실제로 실행될 때 데이터베이스에서 모델 인스턴스와 연관관계가 재조회됩니다. 이렇게 하면 큐에 실리는 데이터가 최소화됩니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드 의존성 주입

`handle` 메서드는 큐가 잡을 처리할 때 호출됩니다. 이때 메서드의 타입힌트에 지정한 의존성은 Laravel [서비스 컨테이너](/docs/master/container)를 통해 자동 주입됩니다.

컨테이너가 `handle` 메서드에 의존성을 주입하는 방식을 완전히 제어하고 싶다면, 컨테이너의 `bindMethod` 메서드를 사용할 수 있습니다. 이 메서드에 콜백을 전달하여 원하는 방식으로 `handle`을 호출할 수 있습니다. 주로 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 호출합니다.

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 바이너리 데이터(예: 원본 이미지 데이터)는 잡에 전달하기 전에 반드시 `base64_encode` 등의 처리를 해주어야 합니다. 그렇지 않으면 잡이 큐에 직렬화될 때 JSON 변환이 제대로 동작하지 않을 수 있습니다.

<a name="handling-relationships"></a>
#### 큐잉된 연관관계 처리

큐에 직렬화될 때, 로드된 모든 Eloquent 모델의 연관관계도 같이 직렬화됩니다. 이로 인해 직렬화 문자열이 커질 수 있습니다. 또한, 잡이 역직렬화되어 모델의 연관관계가 데이터베이스에서 다시 로드될 때는 모든 관계가 제약 없이 전부 불러와집니다. 잡 큐잉 전에 관계에 제약을 줬더라도, 이 제약은 복원 시에는 적용되지 않습니다. 따라서, 특정 연관관계의 일부만 조회하고자 한다면 잡 내부에서 관계 쿼리를 다시 제한해야 합니다.

혹은, 직렬화 시에 관계 포함을 원하지 않는다면, 모델 속성 설정 시 `withoutRelations` 메서드를 호출할 수 있습니다. 이 메서드는 관계가 모두 비워진 모델 인스턴스를 반환합니다.

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

[PHP 생성자 속성 프로모션](https://www.php.net/manual/en/language.oop5.decon.php#language.oop5.decon.constructor.promotion)을 활용한다면, Eloquent 모델의 관계 직렬화를 방지하기 위해 `WithoutRelations` 속성을 사용할 수 있습니다.

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

모든 모델의 관계 직렬화를 방지하고 싶다면, 클래스 전체에 `WithoutRelations` 속성을 적용하면 됩니다.

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

여러 모델을 배열이나 컬렉션으로 받아서 큐에 전달하면, 큐에서 잡을 복원 및 실행할 때는 해당 컬렉션 내 모델들의 연관관계 정보는 복원되지 않습니다. 이는 많은 수의 모델을 큐에서 다룰 때 자원 사용을 최소화하기 위한 장치입니다.

<a name="unique-jobs"></a>
### 유일 잡(Unique Jobs)

> [!WARNING]
> 유일 잡은 atomic lock을 지원하는 [락 기능이 있는 캐시 드라이버](/docs/master/cache#atomic-locks)가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 드라이버가 atomic lock을 지원합니다.

> [!WARNING]
> 유일 잡 제약조건은 배치 내부의 잡에는 적용되지 않습니다.

특정 잡의 인스턴스가 단 한 번만 큐에 올라가도록 보장하고 싶을 때가 있습니다. 잡 클래스에 `ShouldBeUnique` 인터페이스를 구현하면 됩니다. 이 인터페이스는 추가 메서드 구현 없이 사용할 수 있습니다.

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

위 예시에서 `UpdateSearchIndex` 잡은 유일하게 취급되며, 동일한 잡이 큐에 이미 남아있고 아직 처리가 완료되지 않았다면, 새로 디스패치하지 않습니다.

특정 "키"로 유일성을 결정하거나, 유일성 유지 시간(타임아웃)을 지정하려면 `UniqueFor` 속성과 `uniqueId` 메서드를 사용할 수 있습니다.

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;
use Illuminate\Queue\Attributes\UniqueFor;

#[UniqueFor(3600)]
class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    /**
     * The product instance.
     *
     * @var \App\Models\Product
     */
    public $product;

    /**
     * Get the unique ID for the job.
     */
    public function uniqueId(): string
    {
        return $this->product->id;
    }
}
```
위의 예시에서, product ID 별로 유일성이 결정되며, 동일한 product ID로 잡을 또 디스패치하면 앞선 작업이 끝날 때까지(혹은 1시간 내에는) 큐에 쌓이지 않습니다.

> [!WARNING]
> 여러 웹서버나 컨테이너에서 잡을 디스패치한다면, 모든 서버가 동일한 캐시 서버를 사용하도록 해야 유일 잡 정책이 정확히 적용됩니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 잡 실행 시작 전까지 유일성 유지

기본적으로 유일 잡은 실행 완료 또는 모든 재시도 실패 후 "락"이 해제됩니다. 만약 잡 실행 시작 전에 곧바로 락을 해제하고 싶다면, `ShouldBeUnique` 대신 `ShouldBeUniqueUntilProcessing` 인터페이스를 구현하세요.

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

실제로는, `ShouldBeUnique` 잡 디스패치 시 Laravel은 `uniqueId`를 사용하여 [락](/docs/master/cache#atomic-locks)을 획득하려 시도합니다. 이미 락이 있다면 잡은 큐에 올라가지 않습니다. 락은 잡이 완료되거나 최종 시도에서 실패하면 해제됩니다. 별도의 캐시 드라이버로 락을 관리하려면 `uniqueVia` 메서드를 정의하면 됩니다.

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
> 동시 실행 제한만 필요한 경우 [WithoutOverlapping](/docs/master/queues#preventing-job-overlaps) 잡 미들웨어를 사용하세요.

<a name="encrypted-jobs"></a>
### 암호화된 잡(Encrypted Jobs)

잡의 데이터 프라이버시와 무결성을 보장하고 싶다면, [암호화](/docs/master/encryption) 기능을 활용할 수 있습니다. 잡 클래스에 `ShouldBeEncrypted` 인터페이스만 추가하면, Laravel이 큐에 넣기 전 자동으로 데이터를 암호화합니다.

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
## 잡 미들웨어(Job Middleware)

잡 미들웨어를 사용하면 큐잉된 잡 실행 흐름에 맞춤 로직을 쉽게 추가할 수 있으며, 반복적인 코드도 줄일 수 있습니다. 예를 들어, Redis의 속도제한 기능으로 5초마다 한 잡만 실행하도록 handle 메서드를 작성했다면 아래와 같이 구현할 수 있습니다.

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

하지만 이 방식은 handle이 복잡해지고, 여러 잡에서 중복 구현해야 하므로 번거롭습니다. 따라서 미들웨어로 별도 분리하는 것이 더 낫습니다.

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

미들웨어는 [라우트 미들웨어](/docs/master/middleware)와 비슷하게, 잡과 다음 처리 콜백을 인자로 받습니다.

새 잡 미들웨어 클래스는 `make:job-middleware` Artisan 명령어로 생성할 수 있습니다. 만든 미들웨어는 잡의 `middleware` 메서드에서 반환해 적용합니다(메서드는 수동으로 추가해야 합니다).

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
> 잡 미들웨어는 [큐잉 이벤트 리스너](/docs/master/events#queued-event-listeners), [메일러블](/docs/master/mail#queueing-mail), [알림](/docs/master/notifications#queueing-notifications)에도 적용할 수 있습니다.

<a name="rate-limiting"></a>
### 속도 제한(Rate Limiting)

직접 속도 제한 미들웨어를 작성하는 대신, Laravel 내장 속도 제한 미들웨어도 사용할 수 있습니다. [라우트 속도 제한자](/docs/master/routing#defining-rate-limiters)와 유사하게, 잡 속도 제한자도 `RateLimiter` 파사드의 `for` 메서드로 정의합니다.

예를 들어, 일반 사용자는 한 시간에 한 번, 프리미엄 사용자는 무제한 백업을 허용하고 싶다면 다음과 같이 설정할 수 있습니다.

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

`perMinute` 등 다양한 주기에도 적용할 수 있습니다. `by` 메서드는 대개 사용자별 제한을 위해 사용됩니다.

```php
return Limit::perMinute(50)->by($job->user->id);
```

설정한 제한자는 `Illuminate\Queue\Middleware\RateLimited` 미들웨어로 잡에 적용합니다.

```php
use Illuminate\Queue\Middleware\RateLimited;

public function middleware(): array
{
    return [new RateLimited('backups')];
}
```

속도 제한으로 잡이 지연될 때마다 `attempts` 횟수가 증가하므로, `Tries`, `MaxExceptions` 등을 적절히 조정하거나, [retryUntil 메서드](#time-based-attempts)로 재시도 제한 시간을 지정하세요.

`releaseAfter` 메서드로 재시도까지 대기할 초도 지정할 수 있습니다.

```php
public function middleware(): array
{
    return [(new RateLimited('backups'))->releaseAfter(60)];
}
```

재시도를 원치 않으면 `dontRelease`를 사용하세요.

```php
public function middleware(): array
{
    return [(new RateLimited('backups'))->dontRelease()];
}
```

<a name="rate-limiting-with-redis"></a>
#### Redis로 속도 제한

Redis를 사용할 때는 `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어를 쓰면 보다 최적화된 속도 제한을 구현할 수 있습니다.

```php
use Illuminate\Queue\Middleware\RateLimitedWithRedis;

public function middleware(): array
{
    return [new RateLimitedWithRedis('backups')];
}
```

특정 Redis 연결을 사용하려면 `connection` 메서드로 지정할 수 있습니다.

```php
return [(new RateLimitedWithRedis('backups'))->connection('limiter')];
```

<a name="preventing-job-overlaps"></a>
### 잡 중복 실행 방지

`Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어를 사용하면, 특정 키를 기준으로 잡의 동시 실행(중복 실행)을 방지할 수 있습니다. 예를 들어, 동일 사용자 ID 기준으로 신용점수 갱신 잡의 중복 처리를 막을 수 있습니다.

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

중첩 잡을 다시 큐로 보낼 때도 `attempts` 횟수가 증가합니다. 즉, 기본값인 1이라면 재시도가 없으니 적절히 직접 설정하세요.

`releaseAfter`로 대기 시간을, `dontRelease()`로 재시도 방지 역시 가능합니다.

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->releaseAfter(60)];
}
```

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->dontRelease()];
}
```

동시에, 예상치 못한 실패로 락이 해제되지 않을 수도 있으니, `expireAfter`로 락 만료 시간을 설정할 수 있습니다.

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->expireAfter(180)];
}
```

> [!WARNING]
> `WithoutOverlapping` 미들웨어는 lock을 지원하는 캐시 드라이버(`memcached`, `redis`, `dynamodb`, `database`, `file`, `array`)가 필요합니다.

<a name="sharing-lock-keys"></a>
#### 잡 클래스 간 락 키 공유

기본적으로 `WithoutOverlapping` 미들웨어는 동일한 클래스의 중첩 잡만 방지합니다. 서로 다른 잡 클래스가 같은 락 키를 사용해도, 클래스가 다르면 중첩 방지 효과가 없습니다. `shared` 메서드를 사용하면 클래스 간에도 락 키를 공유할 수 있습니다.

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

`Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어를 사용하면 잡이 특정 횟수 이상 예외를 발생시키면, 이후 일정 시간 동안 실행이 지연됩니다. 주로 불안정한 외부 서비스와 통신할 때 유용합니다.

잡 실행 시 예외가 반복되면, 지정한 threshold 이상이면 일정 시간 이후에만 잡을 다시 실행하게 합니다.

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

첫 번째 인자는 허용할 예외 횟수, 두 번째는 예외 threshold 도달 시 대기할 시간(초)입니다. threshold 미만 예외는 즉시 재시도되지만, `backoff`로 딜레이를 지정할 수도 있습니다.

```php
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 5 * 60))->backoff(5)];
}
```

`by`로 여러 잡이 같은 제한 "버킷"을 공유하도록 할 수도 있습니다.

```php
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->by('key')];
}
```

기본적으로 모든 예외를 제한하지만, `when` 메서드에 클로저를 넘겨 특정 상황에서만 예외 제한을 적용할 수 있습니다.

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

`deleteWhen`으로 특정 예외 발생 시 잡을 완전히 제거할 수 있습니다.

```php
use App\Exceptions\CustomerDeletedException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [(new ThrottlesExceptions(2, 10 * 60))->deleteWhen(CustomerDeletedException::class)];
}
```

예외를 Exception Handler에 리포팅하고 싶다면, `report` 메서드나 클로저를 함께 사용할 수 있습니다.

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
#### Redis로 예외 제한

Redis를 활용하는 경우, `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어를 사용해 더욱 효율적으로 제한할 수 있습니다.

```php
use Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis;

public function middleware(): array
{
    return [new ThrottlesExceptionsWithRedis(10, 10 * 60)];
}
```

특정 Redis 연결을 사용하려면 `connection` 메서드로 설정할 수 있습니다.

```php
return [(new ThrottlesExceptionsWithRedis(10, 10 * 60))->connection('limiter')];
```

<a name="skipping-jobs"></a>
### 잡 건너뛰기

`Skip` 미들웨어를 활용하면 잡 내부 로직을 수정하지 않고도 잡을 삭제(건너뛰기)할 수 있습니다. `Skip::when`은 조건이 true면 잡을 삭제, `Skip::unless`는 false면 삭제합니다.

```php
use Illuminate\Queue\Middleware\Skip;

public function middleware(): array
{
    return [
        Skip::when($condition),
    ];
}
```

더 복잡한 조건이 있다면 클로저를 전달할 수도 있습니다.

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

---

(중간 이후 문서도 본문 안내 방식, 용어, 마크다운 구조 등이 지금과 동일하게 계속 번역해 나가면 됩니다.)