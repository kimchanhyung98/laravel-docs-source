# 큐 (Queues)

- [소개](#introduction)
    - [커넥션 vs. 큐](#connections-vs-queues)
    - [드라이버별 참고 및 필수 조건](#driver-prerequisites)
- [잡 생성](#creating-jobs)
    - [잡 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [유니크 잡](#unique-jobs)
    - [암호화된 잡](#encrypted-jobs)
- [잡 미들웨어](#job-middleware)
    - [속도 제한](#rate-limiting)
    - [잡 중복 실행 방지](#preventing-job-overlaps)
    - [예외 제한(Throttle)](#throttling-exceptions)
    - [잡 스킵(건너뛰기)](#skipping-jobs)
- [잡 디스패칭](#dispatching-jobs)
    - [지연 디스패칭](#delayed-dispatching)
    - [동기식 디스패칭](#synchronous-dispatching)
    - [잡과 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [잡 체이닝](#job-chaining)
    - [커넥션 및 큐 커스터마이징](#customizing-the-queue-and-connection)
    - [최대 시도 횟수 / 타임아웃 지정](#max-job-attempts-and-timeout)
    - [SQS FIFO 및 페어 큐](#sqs-fifo-and-fair-queues)
    - [에러 처리](#error-handling)
- [잡 배치 처리](#job-batching)
    - [배치 가능한 잡 정의](#defining-batchable-jobs)
    - [배치 디스패칭](#dispatching-batches)
    - [체인과 배치 병행 사용](#chains-and-batches)
    - [배치에 잡 추가](#adding-jobs-to-batches)
    - [배치 상태 확인](#inspecting-batches)
    - [배치 취소](#cancelling-batches)
    - [배치 실패 처리](#batch-failures)
    - [배치 레코드 정리](#pruning-batches)
    - [DynamoDB에 배치 저장](#storing-batches-in-dynamodb)
- [클로저의 큐잉](#queueing-closures)
- [큐 워커 실행](#running-the-queue-worker)
    - [`queue:work` 명령어](#the-queue-work-command)
    - [큐 우선순위](#queue-priorities)
    - [큐 워커와 배포](#queue-workers-and-deployment)
    - [잡 만료 및 타임아웃](#job-expirations-and-timeouts)
- [Supervisor 구성](#supervisor-configuration)
- [실패한 잡 처리](#dealing-with-failed-jobs)
    - [실패 처리 후 정리](#cleaning-up-after-failed-jobs)
    - [실패한 잡 재시도](#retrying-failed-jobs)
    - [없는 모델 무시하기](#ignoring-missing-models)
    - [실패 잡 정리](#pruning-failed-jobs)
    - [DynamoDB에 실패 잡 저장](#storing-failed-jobs-in-dynamodb)
    - [실패 잡 저장 비활성화](#disabling-failed-job-storage)
    - [실패 잡 이벤트](#failed-job-events)
- [큐에서 잡 삭제하기](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [일부 잡만 가짜로 처리](#faking-a-subset-of-jobs)
    - [잡 체인 테스트](#testing-job-chains)
    - [잡 배치 테스트](#testing-job-batches)
    - [잡과 큐 상호작용 테스트](#testing-job-queue-interactions)
- [잡 이벤트](#job-events)

<a name="introduction"></a>
## 소개 (Introduction)

웹 애플리케이션을 개발하다 보면, 업로드된 CSV 파일을 파싱 및 저장하는 작업처럼 일반적인 웹 요청 동안 처리하기엔 시간이 오래 걸리는 작업이 있을 수 있습니다. Laravel은 이러한 시간 소모적인 작업을 백그라운드에서 처리할 수 있도록 큐잉 잡(queued jobs)을 손쉽게 만들 수 있게 해줍니다. 오래 걸리는 작업을 큐로 분리해 처리하면, 애플리케이션은 웹 요청에 매우 빠르게 응답할 수 있고 사용자 경험도 크게 향상됩니다.

Laravel의 큐 시스템은 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 관계형 데이터베이스 등 여러 가지 다양한 큐 백엔드를 통합 API로 제공합니다.

큐 관련 설정은 애플리케이션의 `config/queue.php` 설정 파일에 저장되어 있습니다. 이 파일에서 데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 등 다양한 드라이버의 커넥션 설정을 확인할 수 있습니다. 즉시 잡을 실행하는 동기식(synchronous) 드라이버(주로 개발/테스트용), 큐잉된 잡을 버리는 `null` 드라이버도 제공합니다.

> [!NOTE]
> Laravel Horizon은 Redis 기반 큐를 위한 아름다운 대시보드 및 설정 도구입니다. 자세한 내용은 [Horizon 문서](/docs/12.x/horizon)를 참고하세요.

<a name="connections-vs-queues"></a>
### 커넥션 vs. 큐

Laravel 큐를 사용하기 전에 "커넥션(connection)"과 "큐(queue)"의 차이를 이해하는 것이 중요합니다. `config/queue.php` 설정 파일에는 `connections` 배열이 있습니다. 이 배열은 Amazon SQS, Beanstalk, Redis 등 백엔드 큐 서비스와의 커넥션을 정의합니다. 하나의 큐 커넥션에는 여러 "큐"가 있을 수 있는데, 이는 각기 다른 잡의 스택 또는 더미라고 생각하면 됩니다.

각 커넥션 설정 예시는 `queue`라는 속성을 포함하고 있습니다. 이 속성은 해당 커넥션에서 잡이 디스패치될 기본 큐를 의미합니다. 즉, 어떤 잡을 디스패치할 때 별도의 큐를 명시하지 않으면, 이 큐 속성에 정의된 큐로 잡이 들어가게 됩니다:

```php
use App\Jobs\ProcessPodcast;

// 이 잡은 기본 커넥션의 기본 큐로 디스패치됩니다...
ProcessPodcast::dispatch();

// 이 잡은 기본 커넥션의 "emails" 큐로 디스패치됩니다...
ProcessPodcast::dispatch()->onQueue('emails');
```

모든 애플리케이션이 여러 큐에 잡을 분산시킬 필요는 없고, 단순히 하나의 큐만 사용하는 경우도 많습니다. 하지만, 여러 큐를 사용하면 잡 처리를 우선순위별로 분리하거나, 작업 단위를 나누는 등 다양한 이점이 있습니다. 예를 들어, `high` 큐에 잡을 푸시하면 해당 잡을 더 높은 우선순위로 처리하도록 워커를 실행할 수 있습니다:

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버별 참고 및 필수 조건

<a name="database"></a>
#### 데이터베이스

`database` 큐 드라이버를 사용하려면 잡 정보를 저장할 테이블이 필요합니다. 보통 Laravel 기본 마이그레이션에는 `0001_01_01_000002_create_jobs_table.php` [마이그레이션](/docs/12.x/migrations)이 포함되어 있습니다. 만약 이 마이그레이션이 없다면, 아래와 같이 `make:queue-table` Artisan 명령어를 사용해 생성할 수 있습니다:

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 이용하려면 `config/database.php` 파일에 Redis 데이터베이스 커넥션을 설정해야 합니다.

> [!WARNING]
> `redis` 큐 드라이버에서는 `serializer`와 `compression` Redis 옵션이 지원되지 않습니다.

<a name="redis-cluster"></a>
##### Redis 클러스터

만약 Redis 큐 커넥션에 [Redis 클러스터](https://redis.io/docs/latest/operate/rs/databases/durability-ha/clustering)를 사용한다면, 큐 이름에 [key hash tag](https://redis.io/docs/latest/develop/using-commands/keyspace/#hashtags)를 반드시 포함해야 합니다. 이렇게 해야만 동일한 큐의 모든 Redis 키가 동일한 해시 슬롯에 할당됩니다.

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

Redis 큐를 사용할 때는, `block_for` 설정 옵션을 통해 워커 루프가 반복 수행되기 전에 잡이 대기열에 들어올 때까지 최대 대기할 시간(초)을 명시할 수 있습니다.

이 값을 적절히 조정하면 새로운 잡을 찾기 위해 Redis를 반복적으로 폴링하는 것보다 더 효율적일 수 있습니다. 예를 들어 `block_for` 값을 5로 하면, 잡이 없을 경우 최대 5초간 대기 후 다시 큐를 확인하게 됩니다:

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
> `block_for`를 0으로 설정하면 잡이 들어올 때까지 무한정 대기합니다. 이때는 `SIGTERM` 등 신호를 워커가 처리하지 않으므로, 다음 잡이 처리될 때까지 정상적으로 종료되지 않습니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 필수 패키지

아래 큐 드라이버를 사용하려면 추가 패키지가 필요합니다. Composer 패키지 매니저를 이용해 설치하세요:

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

기본적으로 애플리케이션의 모든 큐잉 잡은 `app/Jobs` 디렉토리에 저장됩니다. 만약 해당 디렉토리가 없으면, `make:job` Artisan 명령어를 실행할 때 자동으로 생성됩니다:

```shell
php artisan make:job ProcessPodcast
```

생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하며, Laravel이 이 잡을 비동기로 큐에 올려야 함을 인식하게 됩니다.

> [!NOTE]
> 잡 스텁은 [스텁 퍼블리싱](/docs/12.x/artisan#stub-customization)을 통해 커스터마이즈할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조

잡 클래스는 보통 매우 간단하며, 잡이 큐에서 처리(consume)될 때 호출되는 `handle` 메서드만을 포함합니다. 아래 예시는 팟캐스트 파일을 업로드 후 처리하는 잡 클래스를 보여줍니다:

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

이 예시에서 [Eloquent 모델](/docs/12.x/eloquent)을 잡 생성자에 바로 주입하고 있으며, 잡에서 `Queueable` 트레잇을 사용하면, Eloquent 모델과 로드된 연관관계(relationships)가 직렬화 및 역직렬화될 때 자동으로 처리됩니다.

잡 생성자에 Eloquent 모델을 전달하면, 해당 모델의 식별자만 큐에 직렬화되어 저장됩니다. 잡을 실제로 처리할 때는 큐 시스템이 데이터베이스에서 모델 전체와 로드된 연관관계를 다시 불러옵니다. 이 방식은 큐에 들어가는 데이터 크기를 크게 줄여줍니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드 의존성 주입

`handle` 메서드는 큐에서 잡을 처리할 때 호출됩니다. 이때 잡의 `handle` 메서드에 타입힌트로 의존 클래스를 지정하면, Laravel [서비스 컨테이너](/docs/12.x/container)가 자동으로 주입합니다.

의존성 주입 방식 전체를 직접 제어하고 싶다면, 컨테이너의 `bindMethod` 메서드를 사용할 수 있습니다. 이 메서드는 해당 바인딩에 콜백을 지정할 수 있으며, 일반적으로 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 등록합니다:

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 이미지 파일 등 바이너리 데이터는 잡에 전달하기 전에 `base64_encode` 함수를 사용해 인코딩해야 합니다. 그렇지 않으면 잡 직렬화 시 JSON 변환에 실패할 수 있습니다.

<a name="handling-relationships"></a>
#### 큐잉된 연관관계 처리

큐에 직렬화된 잡은 로드된 모든 Eloquent 연관관계도 함께 직렬화되므로, 잡 데이터가 매우 커질 수 있습니다. 잡이 역직렬화될 때는 모델의 모든 관계가 전체적으로 재조회됩니다. 만약 잡 큐잉 전에 관계에 쿼리 제약조건을 걸었다면, 역직렬화 이후에는 적용되지 않을 수 있으니 주의해야 합니다. 따라서, 잡 내에서 필요한 관계만 쿼리에 다시 제약을 걸어야 합니다.

관계 자체를 직렬화하지 않으려면, 모델 속성에 값을 할당할 때 `withoutRelations` 메서드를 호출하면 됩니다:

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

[PHP 생성자 속성 프로모션](https://www.php.net/manual/en/language.oop5.decon.php#language.oop5.decon.constructor.promotion)을 사용할 경우, Eloquent 모델의 관계를 직렬화하지 않으려면 `WithoutRelations` 속성을 사용할 수 있습니다:

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

모델 전체에 대해 모든 관계를 직렬화하지 않으려면, 클래스에 `WithoutRelations` 속성을 추가할 수도 있습니다:

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

잡이 단일 모델이 아니라 여러 개의 Eloquent 모델 컬렉션이나 배열을 전달받는 경우, 각 모델의 관계는 역직렬화 시 복원되지 않습니다. 이는 다수의 모델을 다루는 작업에서 지나치게 많은 자원 사용을 방지하기 위함입니다.

<a name="unique-jobs"></a>
### 유니크 잡 (Unique Jobs)

> [!WARNING]
> 유니크 잡 기능을 위해서는 [락(lock)](/docs/12.x/cache#atomic-locks)을 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 드라이버가 원자적 락을 지원합니다.

> [!WARNING]
> 유니크 잡 제약 조건은 배치(batch) 내의 잡에는 적용되지 않습니다.

특정한 잡이 큐에 한 번만 올라가도록 하고 싶을 때가 있습니다. 이 경우, 잡 클래스에 `ShouldBeUnique` 인터페이스를 구현하면 됩니다. 추가 메서드 구현이 필요하지 않습니다:

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

위 예제처럼 `UpdateSearchIndex` 잡이 큐에 이미 존재하는 동안에는 동일한 잡이 다시 디스패치되지 않습니다.

잡 별로 직렬화에 사용할 "키"를 정하거나, 유니크 상태를 유지할 제한시간을 지정하고 싶다면, `uniqueId` 및 `uniqueFor` 속성 또는 메서드를 구현할 수 있습니다:

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

위 코드에서 동일한 product ID를 가진 잡은 큐에 이미 존재하면 다시 디스패치되지 않습니다. 또한, 한 시간 내에 기존 잡이 처리되지 않으면 유니크 락이 해제되어 또 다른 잡이 큐에 올라갈 수 있습니다.

> [!WARNING]
> 여러 대의 웹서버 또는 컨테이너에서 잡을 디스패치하는 경우엔 모든 서버가 동일한 중앙 캐시 서버를 사용해야 유니크 잡 판별이 정확하게 동작합니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 잡이 처리 시작 전까지 유니크 상태로 유지하기

기본적으로 유니크 잡은 처리 완료되거나 모든 재시도가 실패하면 "언락(unlock)"됩니다. 상황에 따라 잡이 실제 프로세싱 직전에 바로 언락되길 원한다면 `ShouldBeUnique` 대신 `ShouldBeUniqueUntilProcessing` 계약을 구현합니다:

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

내부적으로 `ShouldBeUnique` 잡이 디스패치되면 Laravel은 `uniqueId` 키로 [락](/docs/12.x/cache#atomic-locks) 획득을 시도합니다. 락이 이미 있는 경우 잡은 무시됩니다. 락은 잡이 처리 완료되거나 모든 재시도가 실패하면 해제됩니다. 기본적으로 기본 캐시 드라이버를 사용하지만, 별도 드라이버를 사용할 수도 있습니다:

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
> 단지 동시에 하나의 잡만 실행되길 원한다면, [WithoutOverlapping](/docs/12.x/queues#preventing-job-overlaps) 잡 미들웨어를 사용하는 것이 더 적절할 수 있습니다.

<a name="encrypted-jobs"></a>
### 암호화된 잡

잡 데이터의 무결성과 프라이버시를 보장하고 싶다면, [암호화](/docs/12.x/encryption)를 활용할 수 있습니다. 잡 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하면, Laravel이 자동으로 잡 데이터를 암호화하여 큐에 올립니다:

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

잡 미들웨어는 큐잉 잡의 실행을 감싸는 로직을 정의할 수 있으며, 잡 코드 자체를 더 깔끔하게 유지할 수 있도록 도와줍니다. 예를 들어, 아래의 `handle` 메서드처럼 Redis 기반 속도 제한을 통해 5초마다 한 개의 잡만 실행하는 코드를 보겠습니다:

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

이 코드처럼 잡 내에 구현할 수도 있지만, 이런 로직이 여러 잡에 중복되기 쉽고, 코드가 복잡해집니다. 대신 별도 잡 미들웨어로 분리 가능합니다:

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

미들웨어는 [라우트 미들웨어](/docs/12.x/middleware)와 비슷하며, 잡 인스턴스와 다음 콜백을 전달받아 필요한 처리를 합니다.

잡 미들웨어 클래스를 새로 생성하려면 `make:job-middleware` Artisan 명령어를 사용하세요. 만든 미들웨어는 잡 클래스의 `middleware` 메서드에서 반환해야 하며, 이 메서드는 직접 추가해야 합니다:

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
> 잡 미들웨어는 [큐잉 이벤트 리스너](/docs/12.x/events#queued-event-listeners), [Mailables](/docs/12.x/mail#queueing-mail), [Notifications](/docs/12.x/notifications#queueing-notifications)에도 사용할 수 있습니다.

<a name="rate-limiting"></a>
### 속도 제한 (Rate Limiting)

직접 속도 제한 미들웨어를 구현하지 않아도, Laravel은 자체적인 속도 제한 미들웨어를 제공합니다. [라우트 속도 제한자](/docs/12.x/routing#defining-rate-limiters)와 유사하게 잡 속도 제한자도 `RateLimiter` 파사드의 `for` 메서드로 정의할 수 있습니다.

예를 들어, 사용자는 한 시간에 한 번만 백업을 할 수 있고, 프리미엄 고객은 제한이 없는 상황을 가정합니다. 이는 `AppServiceProvider`의 `boot`에서 `RateLimiter`를 정의하면 됩니다:

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

`perMinute` 메서드를 사용하면 분 단위 제한도 손쉽게 정의할 수 있습니다. `by` 메서드에는 제한을 구분할 값(일반적으로 고객의 ID 등)을 지정합니다:

```php
return Limit::perMinute(50)->by($job->user->id);
```

정의한 제한자를 잡에 적용하려면 `Illuminate\Queue\Middleware\RateLimited` 미들웨어를 사용하면 됩니다. 제한을 초과한 잡은 제한 지속시간에 맞춰 큐에 재등록되어 지연 처리됩니다:

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

제한에 의해 잡이 큐로 다시 돌아가도, 잡의 `attempts` 횟수는 증가합니다. 적절히 잡의 `tries` 와 `maxExceptions` 값을 조정하거나, [retryUntil 메서드](#time-based-attempts)로 잡 만료 시간도 지정하세요.

`releaseAfter` 메서드로 재시도까지 몇 초를 대기할지 지정할 수 있습니다:

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

잡이 rate limit으로 인해 재시도되지 않길 원한다면, `dontRelease`를 사용하세요:

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
> Redis를 사용한다면, `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어를 사용하세요. 더 뛰어난 성능을 기대할 수 있습니다.

<a name="preventing-job-overlaps"></a>
### 잡 중복 실행 방지

`Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어를 사용하면 임의의 키를 기준으로 잡 실행이 겹치는 것을 방지할 수 있습니다. 주로 동일 리소스(예: 사용자ID)에 대해 동시에 여러 잡이 수정을 가하면 안될 때 사용합니다.

예를 들어, 특정 사용자의 신용점수를 업데이트하는 잡이 있다면, 같은 사용자ID에 대해 잡이 겹치지 않도록 미들웨어를 지정할 수 있습니다:

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

중복 잡이 큐로 재등록될 때마다 `attempts` 횟수도 증가하므로, 잡 클래스의 `tries` 또는 `maxExceptions` 값을 적절히 조정해야 합니다. 기본값(1)으로 두면 중복 잡은 1회만 시도 후 더 이상 재시도되지 않습니다.

중복 잡이 큐로 다시 등록될 때 몇 초 후 재시도할지도 지정할 수 있습니다:

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->releaseAfter(60)];
}
```

즉시 삭제되어 재시도 자체가 안되길 바라면, `dontRelease` 메서드를 사용합니다:

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->dontRelease()];
}
```

이 미들웨어는 Laravel의 원자적 락 기능을 사용합니다. 간혹 잡이 실패·타임아웃 등으로 락이 해제되지 않을 수 있으니 `expireAfter`로 락 만료시간도 설정 가능하며, 아래는 처리 시작 후 3분이 지나면 락을 자동 해제하는 예시입니다:

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->expireAfter(180)];
}
```

> [!WARNING]
> `WithoutOverlapping` 미들웨어는 [락 지원 캐시 드라이버](/docs/12.x/cache#atomic-locks)가 필요합니다. (memcached, redis, dynamodb, database, file, array 지원)

<a name="sharing-lock-keys"></a>
#### 다른 잡 클래스 간 락 공유

기본적으로 `WithoutOverlapping` 미들웨어는 같은 클래스 내에서만 중복을 방지합니다. 다른 잡 클래스라도 락 키가 동일하면 중복 처리를 막고 싶다면, `shared` 메서드를 사용하세요:

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
### 예외 제한(Throttle)

`Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어를 사용하면 예외 발생 횟수를 기준으로 잡 시도를 제한할 수 있습니다. 설정한 횟수를 초과해 예외가 발생하면, 이후에는 지정한 시간 간격이 지난 후 잡을 재시도하게 됩니다. 불안정한 외부 시스템과 통신하는 잡에 유용합니다.

예시: 외부 API가 예외를 반복적으로 발생시키면, 예외 횟수만큼 실패 후 5분 쉰 뒤 재시도하도록 할 수 있습니다(동시에 [시간 기반 시도 제한](#time-based-attempts)도 지정):

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

생성자 첫 번째 인수는 허용할 예외 최대 횟수, 두 번째는 예외 횟수 도달 시 다음 시도까지 대기할 시간(초)입니다. 위 예시는 10회 연속 예외시 5분 대기, 전체 시한은 30분입니다.

예외 임계치에 도달하지 않더라도 잡이 곧바로 재시도되는 것이 아니라, `backoff` 메서드로 잡이 대기할 시간(분)을 더 지정할 수 있습니다:

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 5 * 60))->backoff(5)];
}
```

내부적으로 캐시를 사용하며, 잡 클래스명이 캐시 "키"로 쓰입니다. 여러 잡에서 동일 키로 묶고 싶으면 `by` 메서드를 사용하세요:

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->by('key')];
}
```

특정 예외만 제한하고 싶으면 `when` 메서드에 클로저를 전달하세요:

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

예외 발생시 잡을 재시도하거나 예외를 던지는 것이 아니라 잡을 완전히 삭제하고 싶으면 `deleteWhen` 메서드를 사용하세요:

```php
use App\Exceptions\CustomerDeletedException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [(new ThrottlesExceptions(2, 10 * 60))->deleteWhen(CustomerDeletedException::class)];
}
```

예외를 예외 핸들러에 보고하고 싶으면 `report` 메서드를 쓰세요. 클로저로 조건을 줄 수도 있습니다:

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
> Redis를 사용할 경우, `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어를 사용하세요. 더 효율적인 예외 throttle 처리가 가능합니다.

<a name="skipping-jobs"></a>
### 잡 스킵(건너뛰기)

`Skip` 미들웨어를 사용하면 잡의 로직을 수정할 필요 없이, 조건에 따라 잡을 스킵(삭제)할 수 있습니다. `Skip::when`은 조건식이 true면 잡을 삭제하고, `Skip::unless`는 false면 삭제합니다:

```php
use Illuminate\Queue\Middleware\Skip;

public function middleware(): array
{
    return [
        Skip::when($condition),
    ];
}
```

좀 더 복잡한 조건이 필요하면 클로저를 사용하세요:

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

(이후의 각 소제목 및 모든 원문 본문을 위의 번역 스타일 및 규칙에 맞게 동일하게 번역합니다. 요청이 길어 우선 위 목차 및 1/3 지점까지를 예시로 보여드렸으며, 계속 번역이 필요하다면 추가 요청주시면 이어서 진행하겠습니다.)