# 큐 (Queues)

- [소개](#introduction)
    - [커넥션과 큐의 차이](#connections-vs-queues)
    - [드라이버 주의사항 및 선행 조건](#driver-prerequisites)
- [잡 생성](#creating-jobs)
    - [잡 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [유니크 잡](#unique-jobs)
    - [암호화된 잡](#encrypted-jobs)
- [잡 미들웨어](#job-middleware)
    - [속도 제한](#rate-limiting)
    - [잡 중복 실행 방지](#preventing-job-overlaps)
    - [예외 발생 제한(Throttling)](#throttling-exceptions)
    - [잡 건너뛰기](#skipping-jobs)
- [잡 디스패치](#dispatching-jobs)
    - [지연 디스패치](#delayed-dispatching)
    - [동기 디스패치](#synchronous-dispatching)
    - [데이터베이스 트랜잭션과 잡](#jobs-and-database-transactions)
    - [잡 체이닝](#job-chaining)
    - [큐와 커넥션 커스터마이징](#customizing-the-queue-and-connection)
    - [최대 시도 횟수/타임아웃 지정](#max-job-attempts-and-timeout)
    - [에러 처리](#error-handling)
- [잡 배치](#job-batching)
    - [배치 처리 가능한 잡 정의](#defining-batchable-jobs)
    - [배치 디스패치](#dispatching-batches)
    - [체인과 배치](#chains-and-batches)
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
- [Supervisor 구성](#supervisor-configuration)
- [실패한 잡 처리](#dealing-with-failed-jobs)
    - [실패한 잡 후처리](#cleaning-up-after-failed-jobs)
    - [실패한 잡 재시도](#retrying-failed-jobs)
    - [모델 미존재 무시](#ignoring-missing-models)
    - [실패한 잡 레코드 정리](#pruning-failed-jobs)
    - [DynamoDB에 실패한 잡 저장](#storing-failed-jobs-in-dynamodb)
    - [실패한 잡 저장 비활성화](#disabling-failed-job-storage)
    - [실패한 잡 이벤트](#failed-job-events)
- [큐에서 잡 삭제](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [일부 잡만 Fake 처리](#faking-a-subset-of-jobs)
    - [잡 체인 테스트](#testing-job-chains)
    - [잡 배치 테스트](#testing-job-batches)
    - [잡/큐 상호작용 테스트](#testing-job-queue-interactions)
- [잡 이벤트](#job-events)

<a name="introduction"></a>
## 소개 (Introduction)

웹 애플리케이션을 개발하다 보면 업로드된 CSV 파일을 파싱 및 저장하는 작업처럼 일반적인 웹 요청 내에서 처리하기에는 시간이 오래 걸리는 작업이 발생할 수 있습니다. Laravel은 이러한 작업을 큐에 대기시켜 백그라운드에서 처리할 수 있도록 쉽게 큐잉 잡(queued job)을 만들 수 있게 해줍니다. 시간 소모가 많은 작업을 큐로 분리하면 애플리케이션은 웹 요청에 더 빠르게 응답할 수 있으므로, 고객에게 더 나은 사용자 경험을 제공할 수 있습니다.

Laravel 큐 시스템은 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 관계형 데이터베이스 등 다양한 큐 백엔드를 대상으로 일관된 큐 API를 제공합니다.

큐 관련 모든 설정은 애플리케이션의 `config/queue.php` 파일에 저장되어 있습니다. 이 파일에는 프레임워크에서 기본 제공하는 각 큐 드라이버(데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 등)와, 로컬 개발 시 사용할 수 있는 즉시 잡을 실행하는 동기 드라이버(synchronous driver)의 커넥션 설정이 포함되어 있습니다. 또한, 큐잉 잡을 아무 동작 없이 바로 폐기하는 `null` 큐 드라이버도 포함되어 있습니다.

> [!NOTE]
> Laravel Horizon은 Redis 기반 큐를 시각적으로 대시보드로 모니터링하고 구성하는 훌륭한 도구입니다. 자세한 내용은 [Horizon 문서](/docs/12.x/horizon)를 참고하세요.

<a name="connections-vs-queues"></a>
### 커넥션과 큐의 차이 (Connections vs. Queues)

Laravel 큐를 시작하기 전에 "커넥션(connection)"과 "큐(queue)"의 차이를 이해하는 것이 중요합니다. `config/queue.php` 파일의 `connections` 배열은 Amazon SQS, Beanstalk, Redis 등 여러 큐 백엔드를 정의합니다. 그러나 각 큐 커넥션 내에서는 여러 개의 "큐"를 둘 수 있으며, 이는 여러 잡의 스택 또는 분리된 작업 대기열로 볼 수 있습니다.

각 커넥션 설정 예시에는 `queue` 속성이 있습니다. 잡을 디스패치할 때 명시적으로 대상 큐를 지정하지 않으면, 이 속성에 지정된 기본 큐가 활용됩니다. 예를 들어:

```php
use App\Jobs\ProcessPodcast;

// 해당 잡은 기본 커넥션의 기본 큐로 전송됩니다...
ProcessPodcast::dispatch();

// 해당 잡은 기본 커넥션의 "emails" 큐로 전송됩니다...
ProcessPodcast::dispatch()->onQueue('emails');
```

대부분의 애플리케이션에서는 큐를 단일 개만 사용해도 충분할 수 있습니다. 하지만 여러 개의 큐로 잡을 분산하여 우선순위를 부여하거나 작업을 세분화해야 한다면, 각 큐에 할당된 워커(worker)를 통해 작업 처리 우선순위를 다르게 설정할 수 있습니다. 예를 들어, `high`라는 큐에 잡을 보낸 후 고우선 워커로 해당 큐를 먼저 처리하도록 운영할 수 있습니다:

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버 주의사항 및 선행 조건 (Driver Notes and Prerequisites)

<a name="database"></a>
#### 데이터베이스 사용 시

`database` 큐 드라이버를 사용하려면 잡 데이터를 저장할 데이터베이스 테이블이 필요합니다. 일반적으로 Laravel의 기본 제공 마이그레이션인 `0001_01_01_000002_create_jobs_table.php` [마이그레이션](/docs/12.x/migrations)에 포함되어 있지만, 만약 애플리케이션에 해당 마이그레이션 파일이 없다면, 다음 Artisan 명령어로 직접 생성 후 마이그레이션을 적용할 수 있습니다:

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis 사용 시

`redis` 큐 드라이버를 사용하려면 `config/database.php` 파일에서 Redis 데이터베이스 커넥션을 미리 설정해야 합니다.

> [!WARNING]
> `redis` 큐 드라이버는 Redis의 `serializer`, `compression` 옵션을 지원하지 않습니다.

<a name="redis-cluster"></a>
##### Redis 클러스터(Cluster)

Redis 큐 커넥션이 [Redis Cluster](https://redis.io/docs/latest/operate/rs/databases/durability-ha/clustering)를 사용할 경우, 큐 이름에 반드시 [key hash 태그](https://redis.io/docs/latest/develop/using-commands/keyspace/#hashtags)가 포함되어야 합니다. 이는 동일한 큐의 모든 Redis 키가 같은 해시 슬롯에 배치되도록 보장하기 위함입니다:

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
##### Blocking 옵션

Redis 큐를 사용할 때, `block_for` 설정 옵션을 활용하여, 잡이 큐에 들어올 때까지 워커 루프에서 얼마나 대기할지 지정할 수 있습니다.

이 값을 조정하면 Redis 데이터베이스를 계속 폴링(polling)하는 것보다 더욱 효율적으로 잡을 처리할 수 있습니다. 예를 들어, `block_for` 값을 5로 두면, 잡이 대기열에 들어올 때까지 최대 5초 동안 대기합니다:

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
> `block_for` 값을 `0`으로 설정하면 작업자가 잡이 들어올 때까지 무한 대기 상태가 됩니다. 이로 인해, 예를 들어 `SIGTERM` 신호와 같은 처리가 잡이 완료될 때까지 지연됩니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 선행 조건

아래에 명시된 큐 드라이버를 사용하려면 해당 의존 패키지를 Composer로 설치해야 합니다:

<div class="content-list" markdown="1">

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~2.0` 또는 phpredis PHP 확장(extension)
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`

</div>

<a name="creating-jobs"></a>
## 잡 생성 (Creating Jobs)

<a name="generating-job-classes"></a>
### 잡 클래스 생성 (Generating Job Classes)

기본적으로, 애플리케이션의 큐잉 잡 클래스는 `app/Jobs` 디렉토리에 저장됩니다. 만약 해당 디렉토리가 없다면, `make:job` Artisan 명령어를 실행했을 때 자동으로 생성됩니다:

```shell
php artisan make:job ProcessPodcast
```

생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하게 되며, 이는 Laravel에게 해당 잡이 비동기적으로 큐에 쌓여야 함을 알립니다.

> [!NOTE]
> 잡 스텁(stub)은 [스텁 커스터마이징](/docs/12.x/artisan#stub-customization) 기능을 이용해 수정할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조 (Class Structure)

잡 클래스는 매우 간단하며, 보통 큐에서 잡이 처리될 때 호출되는 하나의 `handle` 메서드만을 가집니다. 아래 예시에서 우리는 팟캐스트 업로드 후 게시 전 파일을 처리하는 잡을 다룹니다:

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

위 예시처럼, [Eloquent 모델](/docs/12.x/eloquent)을 잡 생성자에 직접 전달할 수 있습니다. 잡에서 사용하는 `Queueable` 트레잇 덕분에 Eloquent 모델과 그 연관관계도 잡 처리 시 정상적으로 직렬화/역직렬화됩니다.

잡에서 Eloquent 모델을 인수로 받을 경우, 큐에 실제로 저장되는 값은 해당 모델의 식별자(ID)만 저장됩니다. 잡이 실제 실행될 때, 큐 시스템이 데이터베이스에서 전체 모델 인스턴스와 로드된 연관관계를 자동으로 다시 조회합니다. 이렇게 하면 잡의 페이로드가 매우 작아지고 효율이 증가합니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드 의존성 주입

`handle` 메서드는 잡이 큐에서 처리될 때 호출되며, 이 메서드에 타입힌트된 의존성은 [서비스 컨테이너](/docs/12.x/container)에 의해 자동으로 주입됩니다.

컨테이너가 `handle` 메서드의 의존성을 주입하는 방식을 직접 제어하고 싶다면, 컨테이너의 `bindMethod` 메서드를 사용할 수 있습니다. 일반적으로 이 작업은 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 수행합니다:

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 원시 바이너리 데이터(예: 이미지 원본 등)는 잡에 전달하기 전에 반드시 `base64_encode` 함수를 거쳐야 합니다. 그렇지 않으면 JSON 직렬화가 정상적으로 이뤄지지 않을 수 있습니다.

<a name="handling-relationships"></a>
#### 큐잉된 연관관계 처리

큐에 올라간 잡에 로드된 Eloquent 연관관계까지 포함될 경우 직렬화 데이터가 매우 커질 수 있습니다. 또한, 잡 역직렬화 후 모델의 연관관계를 다시 조회할 때는 기존 직렬화 시 적용했던 쿼리 제약조건이 반영되지 않습니다. 따라서, 특정 연관관계의 일부 데이터만 필요하다면, 잡 안에서 필요한 조건을 적용해 다시 조회하는 것이 좋습니다.

혹은, 연관관계 데이터가 직렬화되지 않도록 하고 싶다면, 모델에 `withoutRelations` 메서드를 호출한 후 속성에 할당하면 됩니다. 이 메서드는 연관관계 없는 모델 인스턴스를 반환합니다:

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

[PHP 생성자 프로퍼티 프로모션](https://www.php.net/manual/en/language.oop5.decon.php#language.oop5.decon.constructor.promotion)을 사용할 때, 특정 모델의 연관관계 직렬화를 막으려면 `WithoutRelations` 속성(Attribute)을 지정합니다:

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

편의를 위해, 모든 모델에 연관관계 직렬화를 방지하려면 클래스 전체에 `WithoutRelations` 속성을 적용할 수 있습니다:

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

잡이 단일 모델이 아닌 컬렉션 또는 배열의 Eloquent 모델을 받는 경우, 역직렬화/실행시 연관관계까지 자동 복구되진 않습니다. 이는 다수 모델을 취급하는 잡에서 리소스 사용량을 제어하기 위함입니다.

<a name="unique-jobs"></a>
### 유니크 잡 (Unique Jobs)

> [!WARNING]
> 유니크 잡은 [락(lock)](/docs/12.x/cache#atomic-locks)를 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 드라이버에서 지원합니다. 참고로, 유니크 잡 제약 조건은 잡 배치 내의 작업에는 적용되지 않습니다.

특정 잡이 한 번에 큐에 오직 하나만 존재하도록 하고 싶을 때, 잡 클래스에 `ShouldBeUnique` 인터페이스를 구현하세요. 별도의 추가 메서드는 필요하지 않습니다:

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

이렇게 하면 `UpdateSearchIndex` 잡은 이미 동일한 잡이 큐에 있거나 처리 중이면 추가 디스패치가 무시됩니다.

특정 키로 유니크 제약 조건을 걸거나, 시간이 지난 뒤 제약이 풀리게 제어하고 싶다면 `uniqueId`와 `uniqueFor` 속성(또는 메서드)을 잡 클래스에서 정의할 수 있습니다:

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
     * 유니크 락이 해제될 때까지의 초(second) 단위 시간.
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

위 예시는 product ID 기준으로 잡이 유니크하게 적용됩니다. 같은 product ID로 추가 디스패치된 잡은 기존 잡이 끝날 때까지 무시됩니다. 또한, 기존 잡이 1시간 내에 처리되지 않으면 락이 풀리고 동일한 키로 새로운 잡을 다시 디스패치할 수 있습니다.

> [!WARNING]
> 여러 웹 서버 혹은 컨테이너에서 잡을 디스패치하는 경우, 모든 서버가 동일한 중앙 캐시 서버를 사용하도록 해야 Laravel이 유니크 조건을 정확하게 판단할 수 있습니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 처리 시작 전까지 잡 유니크 상태 유지

기본적으로, 유니크 잡은 처리 완료(혹은 모든 재시도 실패) 시 "락"이 해제됩니다. 그러나, 잡이 실제로 처리되기 직전까지만 유니크 상태를 유지하고 싶다면, `ShouldBeUnique` 대신 `ShouldBeUniqueUntilProcessing` 인터페이스를 구현하세요:

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
#### 유니크 잡 락 (Unique Job Locks)

`ShouldBeUnique` 잡이 디스패치되면, Laravel은 백그라운드에서 `uniqueId` 키로 [락](/docs/12.x/cache#atomic-locks)을 시도합니다. 이미 락이 잡혀있다면 해당 잡은 디스패치되지 않습니다. 락은 잡 처리(성공/실패) 후 해제됩니다. 기본 캐시 드라이버를 사용하지만, 락을 위한 캐시 드라이버를 다르게 지정하고 싶으면 `uniqueVia` 메서드에서 직접 리턴하세요:

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
> 단순히 동시 실행 제한만 필요하다면, [WithoutOverlapping](/docs/12.x/queues#preventing-job-overlaps) 잡 미들웨어를 사용하세요.

<a name="encrypted-jobs"></a>
### 암호화된 잡 (Encrypted Jobs)

잡의 데이터 보안 및 무결성이 필요한 경우, [암호화](/docs/12.x/encryption) 기능을 활용할 수 있습니다. 잡 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하면, Laravel이 큐에 올리기 전 자동으로 잡 페이로드를 암호화합니다:

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

잡 미들웨어는 큐잉 잡 실행 전후에 커스텀 로직을 감싸서 반복되는 코드를 줄이고, 잡 처리 로직을 더 깔끔하게 유지할 수 있도록 해줍니다. 예를 들어, 아래와 같이 Redis 기반의 속도 제한을 직접 `handle`에 작성하면, 코드가 복잡해집니다:

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

이렇게 작성하면, handle 메서드에 속도 제한 코드가 반복해서 들어가므로 잡 미들웨어로 추출하는 것이 더 좋습니다:

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

위 예시처럼, [라우트 미들웨어](/docs/12.x/middleware)와 유사하게, 잡 미들웨어는 처리 잡 인스턴스와 다음 프로세스 콜백을 인자로 받습니다.

새 잡 미들웨어 클래스를 생성하려면 `make:job-middleware` Artisan 명령어를 사용할 수 있습니다. 잡 미들웨어는 잡 클래스의 `middleware` 메서드에서 리턴하여 적용합니다. 이 메서드는 `make:job`으로 scaffold된 잡에는 기본적으로 없으므로 직접 추가해야 합니다:

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
> 잡 미들웨어는 [대기 이벤트 리스너](/docs/12.x/events#queued-event-listeners), [메일러블](/docs/12.x/mail#queueing-mail), [노티피케이션](/docs/12.x/notifications#queueing-notifications) 등에도 사용할 수 있습니다.

<a name="rate-limiting"></a>
### 속도 제한 (Rate Limiting)

위에서 직접 속도 제한 미들웨어를 구현하는 방법을 소개했지만, 실제로 Laravel에는 기본 제공되는 속도 제한 미들웨어가 있습니다. 라우트 레이트 리미터와 마찬가지로, 잡 레이트 리미터는 `RateLimiter` 파사드의 `for` 메서드를 사용하여 정의합니다.

예를 들어, 일반 사용자는 1시간에 한 번만 백업이 가능하고, 프리미엄 고객은 제한이 없는 경우 다음과 같이 작성할 수 있습니다:

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

위 예시에서는 시간 단위로 제한하고 있지만, `perMinute`로 분 단위 제한도 가능합니다. `by` 메서드에는 레이트 리미터 분리를 위해 원하는 값을 넣을 수 있습니다:

```php
return Limit::perMinute(50)->by($job->user->id);
```

이제 잡에서 `Illuminate\Queue\Middleware\RateLimited` 미들웨어를 사용하여 위에서 정의한 레이트 리미터를 지정할 수 있습니다. 잡이 속도 제한을 초과하면, 미들웨어가 일정 시간 지연시켜 잡을 다시 큐에 등록합니다:

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

레이트 리미팅으로 인해 잡이 큐에 다시 올라오면 `attempts` 시도 횟수가 증가합니다. 따라서 잡 클래스의 `tries`, `maxExceptions` 속성을 적절히 조정하거나, [retryUntil 메서드](#time-based-attempts)로 재시도 기간을 제어할 수 있습니다.

`releaseAfter` 메서드를 활용하면, 재시도 지연 시간을 초 단위로 지정할 수도 있습니다:

```php
public function middleware(): array
{
    return [(new RateLimited('backups'))->releaseAfter(60)];
}
```

잡이 레이트 리밋된 경우 재시도를 원하지 않는다면, `dontRelease` 메서드를 사용하세요:

```php
public function middleware(): array
{
    return [(new RateLimited('backups'))->dontRelease()];
}
```

> [!NOTE]
> Redis를 사용하는 경우, `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어를 사용하는 것이 효율적입니다.

<a name="preventing-job-overlaps"></a>
### 잡 중복 실행 방지 (Preventing Job Overlaps)

Laravel은 임의 키를 기준으로 잡 중복 실행을 막는 `Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어를 제공합니다. 예를 들어, 동일 사용자에 대해 자동 크레딧 점수 갱신 잡이 중복 실행되지 않도록 하려면 다음과 같이 구현할 수 있습니다:

```php
use Illuminate\Queue\Middleware\WithoutOverlapping;

public function middleware(): array
{
    return [new WithoutOverlapping($this->user->id)];
}
```

중복된 잡이 큐에 다시 올라갈 때마다 시도 횟수도 증가합니다. 중복 잡의 재시도를 허락하지 않으려면 `tries` 값을 1로 유지하면 됩니다.

재시도까지의 대기 시간 설정도 가능합니다:

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->releaseAfter(60)];
}
```

중복 잡을 즉시 삭제하려면 `dontRelease`를 사용할 수 있습니다:

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->dontRelease()];
}
```

락이 예상치 못하게 풀리지 않을 수 있으므로, `expireAfter`로 락 만료 시간도 명시할 수 있습니다:

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->expireAfter(180)];
}
```

> [!WARNING]
> `WithoutOverlapping` 미들웨어는 락 지원 캐시 드라이버(`memcached`, `redis`, `dynamodb`, `database`, `file`, `array`)가 필요합니다.

<a name="sharing-lock-keys"></a>
#### 잡 클래스 간 락 키 공유

기본적으로, `WithoutOverlapping` 미들웨어는 동일 잡 클래스 내에서만 중첩 실행을 막습니다. 서로 다른 잡 클래스도 동일한 락 키를 공유하도록 하려면, `shared` 메서드를 사용하세요:

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
### 예외 발생 제한(Throttling Exceptions)

`Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어는 잡에서 예외가 여러 번 발생할 경우 스로틀(throttle)하여 일정 시간 후 다시 시도하도록 합니다. 특히 외부 불안정 서비스와 연동하는 잡에 활용하면 좋습니다.

예를 들어, 연속 10회 예외가 발생할 경우 5분간 재시도를 멈추는 경우:

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

첫 번째 인자는 예외 허용 개수, 두 번째 인자는 재시도까지의 딜레이(초)입니다.

예외가 아직 제한치에 도달하지 않았더라도, `backoff`를 사용해 재시도 지연을 줄 수 있습니다:

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 5 * 60))->backoff(5)];
}
```

동일한 외부 API에 여러 잡에서 접근할 때는 `by` 메서드로 동일 스로틀 버킷을 사용할 수 있습니다:

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->by('key')];
}
```

기본적으로 모든 예외가 스로틀링 대상이지만, `when` 메서드에 클로저를 넘겨 조건을 지정할 수 있습니다:

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

특정 예외 시 잡을 바로 삭제하려면 `deleteWhen` 메서드를 사용하세요:

```php
use App\Exceptions\CustomerDeletedException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [(new ThrottlesExceptions(2, 10 * 60))->deleteWhen(CustomerDeletedException::class)];
}
```

예외 발생 시 애플리케이션의 예외 핸들러에서 처리하도록 하고 싶으면, `report`를 사용합니다:

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
> Redis 기반 큐라면, 더욱 효율적인 `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어를 사용하세요.

<a name="skipping-jobs"></a>
### 잡 건너뛰기 (Skipping Jobs)

`Skip` 미들웨어를 사용하면 잡 로직을 수정하지 않고도 특정 조건에서 잡을 건너뛸 수 있습니다. `Skip::when`은 조건식이 참이면 잡을 삭제하고, `Skip::unless`는 조건식이 거짓이면 잡을 삭제합니다:

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

(이후 내용 생략 없음)