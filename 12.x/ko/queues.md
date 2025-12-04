# 큐 (Queues)

- [소개](#introduction)
    - [커넥션 vs. 큐](#connections-vs-queues)
    - [드라이버 관련 주의사항 및 사전 요구사항](#driver-prerequisites)
- [잡 생성하기](#creating-jobs)
    - [잡 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [유니크 잡](#unique-jobs)
    - [암호화된 잡](#encrypted-jobs)
- [잡 미들웨어](#job-middleware)
    - [속도 제한(Rate Limiting)](#rate-limiting)
    - [잡 중첩 실행 방지](#preventing-job-overlaps)
    - [예외 빈도 제한(throttling)](#throttling-exceptions)
    - [잡 건너뛰기](#skipping-jobs)
- [잡 디스패치](#dispatching-jobs)
    - [지연 디스패치](#delayed-dispatching)
    - [동기식 디스패치](#synchronous-dispatching)
    - [잡과 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [잡 체이닝](#job-chaining)
    - [큐 및 커넥션 커스터마이징](#customizing-the-queue-and-connection)
    - [최대 시도 횟수/타임아웃 지정](#max-job-attempts-and-timeout)
    - [SQS FIFO 및 공정 큐](#sqs-fifo-and-fair-queues)
    - [큐 페일오버](#queue-failover)
    - [에러 핸들링](#error-handling)
- [잡 배칭](#job-batching)
    - [배치 가능한 잡 정의](#defining-batchable-jobs)
    - [배치 디스패치](#dispatching-batches)
    - [체인과 배치](#chains-and-batches)
    - [배치에 잡 추가](#adding-jobs-to-batches)
    - [배치 조회](#inspecting-batches)
    - [배치 취소](#cancelling-batches)
    - [배치 실패](#batch-failures)
    - [배치 레코드 정리](#pruning-batches)
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
    - [실패한 잡 정리](#pruning-failed-jobs)
    - [DynamoDB에 실패한 잡 저장](#storing-failed-jobs-in-dynamodb)
    - [실패한 잡 저장 비활성화](#disabling-failed-job-storage)
    - [실패한 잡 이벤트](#failed-job-events)
- [큐에서 잡 삭제](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [특정 잡 페이크 처리](#faking-a-subset-of-jobs)
    - [잡 체인 테스트](#testing-job-chains)
    - [잡 배치 테스트](#testing-job-batches)
    - [잡/큐 상호작용 테스트](#testing-job-queue-interactions)
- [잡 이벤트](#job-events)

<a name="introduction"></a>
## 소개 (Introduction)

웹 애플리케이션을 개발하다 보면, 업로드된 CSV 파일을 파싱해서 저장하는 등 일반적인 웹 요청 중에 처리하기에는 시간이 너무 오래 걸리는 작업이 있을 수 있습니다. 다행히 Laravel에서는 이러한 작업을 백그라운드에서 처리할 수 있도록 큐에 잡을 아주 쉽게 생성할 수 있습니다. 시간이 오래 걸리는 작업을 큐로 분리하면, 애플리케이션은 웹 요청에 훨씬 빠르게 응답할 수 있으며, 사용자에게 더 좋은 경험을 제공할 수 있습니다.

Laravel 큐는 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 심지어 관계형 데이터베이스 등 다양한 큐 백엔드에서 사용할 수 있는 통합된 큐 API를 제공합니다.

큐와 관련된 설정은 애플리케이션의 `config/queue.php` 파일에 저장되어 있습니다. 이 파일에는 데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 드라이버, 그리고 잡을 즉시 실행하는 동기식 드라이버(주로 개발·테스트용)까지 모든 큐 드라이버의 연결 정보가 포함되어 있습니다. 또한 큐에 디스패치된 잡을 모두 버리는 `null` 드라이버도 내장되어 있습니다.

> [!NOTE]
> Laravel Horizon은 Redis 기반 큐를 위한 아름다운 대시보드 및 구성 시스템입니다. 자세한 내용은 [Horizon 문서](/docs/12.x/horizon)를 참고하세요.

<a name="connections-vs-queues"></a>
### 커넥션 vs. 큐

Laravel 큐를 사용하기 전, "커넥션"과 "큐"의 차이를 이해하는 것이 중요합니다. `config/queue.php` 설정 파일에는 `connections` 배열 옵션이 있습니다. 이 옵션은 Amazon SQS, Beanstalk, Redis 같은 백엔드 큐 서비스와의 연결 정보를 정의합니다. 하지만, 하나의 큐 커넥션에는 여러 개의 "큐"를 둘 수 있으며, 이는 큐별로 작업을 구분하는 것과 같습니다.

`queue` 설정 파일의 각 커넥션 예시에는 `queue` 속성이 있습니다. 이는 해당 커넥션에서 잡이 디스패치될 기본 큐입니다. 즉, 잡을 디스패치할 때 어떤 큐로 보낼지 명시하지 않으면, 커넥션의 `queue` 속성에 정의된 큐로 저장됩니다.

```php
use App\Jobs\ProcessPodcast;

// 이 잡은 기본 커넥션의 기본 큐로 전송됩니다...
ProcessPodcast::dispatch();

// 이 잡은 기본 커넥션의 "emails" 큐로 전송됩니다...
ProcessPodcast::dispatch()->onQueue('emails');
```

애플리케이션에 따라 여러 큐에 잡을 보낼 필요가 없을 수도 있습니다. 하지만 여러 큐를 사용하면 잡 처리 우선순위나 작업별 분리가 가능하므로 매우 유용할 수 있습니다. Laravel 큐 워커는 어떤 큐를 어떤 우선순위로 처리할지 지정할 수 있습니다. 예를 들어, `high` 큐에 추가된 잡을 먼저 처리하려면 다음과 같이 워커를 설정할 수 있습니다.

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버 관련 주의사항 및 사전 요구사항

<a name="database"></a>
#### 데이터베이스

`database` 큐 드라이버를 사용하려면 잡을 저장할 데이터베이스 테이블이 필요합니다. 보통, 이는 Laravel 기본 제공 마이그레이션인 `0001_01_01_000002_create_jobs_table.php`에 포함되어 있습니다. 만약 이 마이그레이션이 없다면, 다음 Artisan 명령어로 테이블을 생성할 수 있습니다.

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면 `config/database.php`에서 Redis 데이터베이스 커넥션을 설정해야 합니다.

> [!WARNING]
> `serializer` 및 `compression` Redis 옵션은 `redis` 큐 드라이버에서 지원되지 않습니다.

<a name="redis-cluster"></a>
##### Redis 클러스터

Redis 큐 커넥션으로 [Redis Cluster](https://redis.io/docs/latest/operate/rs/databases/durability-ha/clustering)를 사용할 경우, 큐 이름에 [key hash tag](https://redis.io/docs/latest/develop/using-commands/keyspace/#hashtags)를 포함해야 합니다. 이렇게 해야 특정 큐에 대한 모든 Redis 키가 동일한 해시 슬롯에 저장됩니다.

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

Redis 큐를 사용할 때, `block_for` 설정으로 잡이 대기열에 올라올 때까지 드라이버가 몇 초간 대기할지 지정할 수 있습니다.

이 값을 상황에 맞게 조절하면 Redis를 불필요하게 계속 폴링하는 대신 더 효율적으로 동작할 수 있습니다. 예를 들어, 5로 지정하면, 잡이 올라올 때까지 최대 5초간 대기합니다.

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
> `block_for` 옵션을 0으로 지정하면, 잡이 대기열에 생길 때까지 무한정 멈춰있게 됩니다. 이 경우, `SIGTERM` 같은 신호가 워커가 잡을 처리할 때까지 전달되지 않을 수도 있으니 주의하세요.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 사전 요구사항

다음 큐 드라이버를 사용하려면 아래의 Composer 패키지가 필요합니다.

<div class="content-list" markdown="1">

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~2.0` 또는 phpredis PHP 확장 모듈
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`

</div>

<a name="creating-jobs"></a>
## 잡 생성하기 (Creating Jobs)

<a name="generating-job-classes"></a>
### 잡 클래스 생성

기본적으로, 애플리케이션의 모든 큐 잡 클래스는 `app/Jobs` 디렉토리에 저장됩니다. 만약 `app/Jobs` 디렉토리가 존재하지 않는다면, `make:job` Artisan 명령어를 실행할 때 자동으로 생성됩니다.

```shell
php artisan make:job ProcessPodcast
```

생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하며, Laravel에 해당 잡이 큐에 비동기적으로 실행되어야 함을 알립니다.

> [!NOTE]
> 잡 스텁은 [스텁 커스터마이징](/docs/12.x/artisan#stub-customization)을 통해 수정할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조

잡 클래스는 보통 아주 간단합니다. 큐에서 잡이 처리될 때 호출되는 `handle` 메서드만 포함하는 경우가 일반적입니다. 예시로, 팟캐스트를 업로드하고, 게시 전에 파일을 처리해야 하는 서비스를 운영한다고 가정해 봅시다.

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

이 예시에서 볼 수 있듯이, [Eloquent 모델](/docs/12.x/eloquent)을 잡 생성자에 바로 전달할 수 있습니다. 잡에서 `Queueable` 트레이트를 사용하면, Eloquent 모델과 그에 로드된 연관관계도 큐에 직렬화 및 역직렬화 시 자동으로 처리됩니다.

큐 잡이 Eloquent 모델을 받는 경우, 모델의 식별자만 큐로 직렬화되고, 잡이 실제로 처리되는 시점에 큐 시스템이 데이터베이스에서 전체 모델 및 연관관계를 다시 조회합니다. 이 접근 방식 덕분에 큐 드라이버로 전송되는 잡 페이로드 크기를 크게 줄일 수 있습니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드 의존성 주입

큐에서 잡이 처리될 때 `handle` 메서드가 실행됩니다. 이때 `handle` 메서드에 의존성 타입힌트가 가능하며, Laravel [서비스 컨테이너](/docs/12.x/container)가 자동으로 의존성을 주입합니다.

의존성 주입 방식을 완전히 제어하고 싶다면, 컨테이너의 `bindMethod` 메서드를 사용할 수 있습니다. `bindMethod`는 잡과 컨테이너를 인자로 받는 콜백을 등록합니다. 보통은 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 호출합니다.

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 바이너리 데이터(예: 이미지 원본 데이터 등)는 큐 잡에 전달하기 전에 반드시 `base64_encode` 함수를 통해 인코딩해야 합니다. 그렇지 않으면 잡이 큐에 JSON으로 직렬화될 때 오류가 발생할 수 있습니다.

<a name="handling-relationships"></a>
#### 큐에 포함된 연관관계

큐에 잡을 넣을 때 Eloquent 모델에 이미 로드된 연관관계도 함께 직렬화됩니다. 이로 인해 큐로 전송되는 데이터 크기가 커질 수 있고, 잡 실행 시 연관관계를 전체 조회하게 됩니다. 또한, 직렬화 전에 모델에 적용했던 연관관계 제약 조건이 역직렬화 시에는 다시 적용되지 않습니다. 따라서, 일부 연관관계만 필요하다면 잡 내부에서 관계를 재제약하는 것이 좋습니다.

또는 모델 속성 설정 시 `withoutRelations` 메서드를 호출하여 연관관계 직렬화를 방지할 수 있습니다.

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

[PHP 생성자 프로퍼티 프로모션](https://www.php.net/manual/en/language.oop5.decon.php#language.oop5.decon.constructor.promotion)을 사용할 때 Eloquent 모델의 연관관계를 직렬화하지 않으려면, `WithoutRelations` 속성(Attribute)을 사용할 수 있습니다.

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

여러 모델 모두에서 연관관계를 직렬화하지 않으려면, 클래스 전체에 `WithoutRelations` 속성을 부여할 수 있습니다.

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

잡이 단일 모델이 아닌 Eloquent 모델의 컬렉션 또는 배열을 받는 경우, 각 모델의 연관관계는 역직렬화 및 실행 시 복구되지 않습니다. 이는 대량 모델 처리 시 리소스 사용을 최소화하기 위함입니다.

<a name="unique-jobs"></a>
### 유니크 잡 (Unique Jobs)

> [!WARNING]
> 유니크 잡은 [락](/docs/12.x/cache#atomic-locks)를 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 지원됩니다.

> [!WARNING]
> 유니크 잡 제약은 배치 내 잡에는 적용되지 않습니다.

특정 잡이 한 번에 큐에 한 인스턴스만 존재하도록 보장하려고 할 때가 있습니다. 이를 위해 잡 클래스에 `ShouldBeUnique` 인터페이스를 구현하면 됩니다.

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

위 예시의 경우, `UpdateSearchIndex` 잡은 유니크하게 동작하므로, 동일 잡이 아직 처리 중이면 새로운 잡은 디스패치되지 않습니다.

특정 "키"로 잡 유니크성 부여나, 일정 기간이 지나면 유니크 제약을 해제하는 시간 초과도 지정할 수 있습니다. 잡 클래스에 `uniqueId`, `uniqueFor` 속성 또는 메서드를 정의하세요.

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
     * 잡 유니크 락 해제까지 대기할 초 단위 시간.
     *
     * @var int
     */
    public $uniqueFor = 3600;

    /**
     * 해당 잡의 유니크 ID 반환.
     */
    public function uniqueId(): string
    {
        return $this->product->id;
    }
}
```

위와 같이 하면 특정 상품 ID로 잡이 유니크해집니다. 따라서 동일 상품 ID로 잡이 이미 대기 중이면 추가 입력이 무시됩니다. 또한, 기존 잡이 1시간 내에 처리되지 않으면 유니크 락이 해제되고, 동일 키로 새 잡이 다시 큐에 추가될 수 있습니다.

> [!WARNING]
> 여러 웹 서버나 컨테이너에서 잡을 디스패치한다면, 모든 서버가 동일 캐시 서버를 사용해야 유니크 잡 처리가 일관되게 동작합니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 처리 시작 전까지 유니크 보장

기본적으로 유니크 잡은 처리 완료 또는 모든 재시도 실패 시 잠금이 해제됩니다. 잡이 실행되기 직전에 락을 해제하려면 `ShouldBeUnique` 대신 `ShouldBeUniqueUntilProcessing`를 구현하세요.

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

내부적으로 `ShouldBeUnique` 잡이 디스패치될 때, Laravel은 `uniqueId` 키로 [락](/docs/12.x/cache#atomic-locks)를 시도합니다. 락이 이미 있으면 잡이 디스패치되지 않으며, 잡 처리 완료 또는 모든 재시도 실패 시 락이 해제됩니다. 기본적으로는 기본 캐시 드라이버가 사용되지만, 다른 드라이버를 쓰고 싶다면 `uniqueVia` 메서드를 정의하세요.

```php
use Illuminate\Contracts\Cache\Repository;
use Illuminate\Support\Facades\Cache;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...

    /**
     * 유니크 잡 락에 사용할 캐시 드라이버 반환.
     */
    public function uniqueVia(): Repository
    {
        return Cache::driver('redis');
    }
}
```

> [!NOTE]
> 동시에 여러 잡의 처리만 제한하고 싶다면 [WithoutOverlapping](/docs/12.x/queues#preventing-job-overlaps) 잡 미들웨어를 사용하세요.

<a name="encrypted-jobs"></a>
### 암호화된 잡 (Encrypted Jobs)

Laravel은 [암호화](/docs/12.x/encryption)를 통해 잡 데이터의 프라이버시와 무결성을 보장할 수 있습니다. 잡 클래스에 `ShouldBeEncrypted` 인터페이스만 추가하면, Laravel이 잡을 자동으로 암호화하여 큐에 올립니다.

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

잡 미들웨어는 잡 실행 전후로 커스텀 로직을 감쌀 수 있도록 하여, 잡 메서드 내 반복 코드를 줄일 수 있습니다. 예를 들어, 아래 코드처럼 Redis 속도 제한 기능을 활용해 5초에 한 번만 잡이 처리되도록 할 수 있습니다.

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

이 방법도 가능하지만, `handle` 메서드가 장황해지고, 다른 잡에서도 동일 로직을 반복하게 됩니다. 대신, 속도 제한용 잡 미들웨어를 별도로 정의해둘 수 있습니다.

```php
<?php

namespace App\Jobs\Middleware;

use Closure;
use Illuminate\Support\Facades\Redis;

class RateLimited
{
    /**
     * 잡 처리
     *
     * @param  \Closure(object): void  $next
     */
    public function handle(object $job, Closure $next): void
    {
        Redis::throttle('key')
            ->block(0)->allow(1)->every(5)
            ->then(function () use ($job, $next) {
                // 락 획득...

                $next($job);
            }, function () use ($job) {
                // 락 획득 실패...

                $job->release(5);
            });
    }
}
```

이렇게 하면, [라우트 미들웨어](/docs/12.x/middleware)와 마찬가지로, 잡 미들웨어에서도 처리 대상 잡과 다음 콜백이 주어집니다.

`make:job-middleware` Artisan 명령어로 새 잡 미들웨어 클래스를 생성할 수 있습니다. 이렇게 만든 미들웨어는 잡의 `middleware` 메서드로 반환하면 잡에 적용됩니다. (`make:job` 명령어로 생성된 잡에는 기본적으로 이 메서드가 없으니 수동으로 추가하세요.)

```php
use App\Jobs\Middleware\RateLimited;

/**
 * 잡이 통과해야 할 미들웨어 반환.
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
### 속도 제한(Rate Limiting)

커스텀 잡 미들웨어 대신 Laravel에서 제공하는 속도 제한 미들웨어를 활용할 수도 있습니다. [라우트 속도 제한자](/docs/12.x/routing#defining-rate-limiters)와 유사하게, 잡용 속도 제한자는 `RateLimiter` 파사드의 `for` 메서드로 정의합니다.

예를 들어, 사용자가 한 시간에 한 번 직업을 백업할 수 있도록 하고, 프리미엄 고객에게는 이런 제한이 없게 하려면, `AppServiceProvider`의 `boot` 메서드에서 속도 제한자를 정의합니다.

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

`by` 메서드로 구분값(주로 고객 ID 등)을 자유롭게 지정할 수 있는데, 사용자별로 속도 제한을 달리할 때 유용합니다.

```php
return Limit::perMinute(50)->by($job->user->id);
```

이런 규칙을 정의한 뒤, 잡의 미들웨어로 `Illuminate\Queue\Middleware\RateLimited`를 지정하면 됩니다.

```php
use Illuminate\Queue\Middleware\RateLimited;

/**
 * 잡이 통과해야 할 미들웨어 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited('backups')];
}
```

속도 제한으로 인해 잡이 대기열에 다시 등록되어도, 전체 `attempts` 횟수는 계속 증가합니다. 따라서 잡 클래스의 `tries`, `maxExceptions` 속성 값을 상황에 맞게 조절해야 하며, 또는 [retryUntil 메서드](#time-based-attempts)로 재시도 유효기간을 별도로 지정할 수도 있습니다.

`releaseAfter` 메서드로 제한 초과 후 재시도까지의 대기 시간을 직접 지정할 수도 있습니다.

```php
public function middleware(): array
{
    return [(new RateLimited('backups'))->releaseAfter(60)];
}
```

속도 제한 시 잡을 재시도하지 않으려면 `dontRelease` 메서드를 사용하세요.

```php
public function middleware(): array
{
    return [(new RateLimited('backups'))->dontRelease()];
}
```

> [!NOTE]
> Redis를 사용하는 경우, 기본 속도 제한 미들웨어보다 더 최적화된 `Illuminate\Queue\Middleware\RateLimitedWithRedis`를 사용할 수 있습니다.

<a name="preventing-job-overlaps"></a>
### 잡 중첩 실행 방지

Laravel의 `Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어를 이용하면, 임의의 키에 기반해 잡이 중첩 실행되지 않도록 할 수 있습니다. 예를 들어, 한 번에 하나의 잡만 특정 자원을 수정하도록 하고 싶을 때 유용합니다.

예를 들어, 특정 유저의 신용점수를 갱신하는 잡에서, 같은 유저 ID에 대해 동시에 여러 개의 잡이 실행되는 것을 방지하려면 다음과 같이 합니다.

```php
use Illuminate\Queue\Middleware\WithoutOverlapping;

/**
 * 잡이 통과해야 할 미들웨어 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new WithoutOverlapping($this->user->id)];
}
```

중첩 잡도 대기열로 다시 등록될 때 `attempts`가 증가하며, `tries`, `maxExceptions` 옵션 조정이 필요할 수 있습니다. 기본적으로 `tries`가 1이면, 중첩 잡이 다시 실행되지 않습니다.

중첩 잡의 재등록 대기시간 지정은 `releaseAfter`로 할 수 있습니다.

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->releaseAfter(60)];
}
```

중첩된 잡을 곧바로 삭제(재시도 불가)하려면 `dontRelease` 메서드를 사용합니다.

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->dontRelease()];
}
```

Sometimes, 잡이 예기치 않게 실패하거나 타임아웃되어 락이 풀리지 않을 수 있습니다. 이때는 `expireAfter` 메서드로 락 만료시간(초)을 명시적으로 지정할 수 있습니다.

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->expireAfter(180)];
}
```

> [!WARNING]
> `WithoutOverlapping` 미들웨어는 락을 지원하는 캐시 드라이버가 필요합니다. (`memcached`, `redis`, `dynamodb`, `database`, `file`, `array`)

<a name="sharing-lock-keys"></a>
#### 잡 클래스 간 락 키 공유

기본적으로 `WithoutOverlapping` 미들웨어는 동일 클래스 내 잡만 중첩 실행을 막습니다. 서로 다른 잡 클래스여도 같은 락 키를 사용하면, `shared` 메서드로 클래스 간 공유를 적용할 수 있습니다.

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
### 예외 빈도 제한 미들웨어

Laravel의 `Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어로, 예외가 연속 발생하는 잡에 대해 일정 시간 동안 실행을 지연시킬 수 있습니다. 예를 들어, 외부 API와 연동하는 잡이 잦은 예외를 발생시키는 경우에 사용하면 유용합니다.

예시: 예외가 연속 10회 이상 발생하면, 5분 동안 잡 실행을 중단하는 패턴입니다.

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

첫 번째 인자는 예외 허용 횟수, 두 번째 인자는 제한 시간(초)입니다. 설정한 횟수만큼 예외가 연속 발생하면 잡 실행이 일정 시간 지연됩니다.

예외가 허용치 미만일 때는 즉시 재시도하지만, `backoff` 메서드로 재시도까지 대기 시간을 따로 지정할 수 있습니다.

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 5 * 60))->backoff(5)];
}
```

여러 잡이 동일 외부 서비스와 연동한다면, `by` 메서드로 동일 "버킷"을 공유해 예외 제한 범위를 맞출 수 있습니다.

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->by('key')];
}
```

기본적으로 모든 예외에 대해 제한이 적용되지만, `when` 메서드로 특정 예외만 제한하도록 커스터마이즈할 수 있습니다.

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

특정 예외 발생 시 잡을 큐에서 완전히 삭제하려면 `deleteWhen`을 사용하세요.

```php
use App\Exceptions\CustomerDeletedException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [(new ThrottlesExceptions(2, 10 * 60))->deleteWhen(CustomerDeletedException::class)];
}
```

예외를 애플리케이션 예외 핸들러에 자동 보고하려면 `report`를 사용합니다. 선택적으로 클로저를 전달하여 보고 여부를 제어할 수도 있습니다.

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
> Redis를 사용한다면, `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어가 기본 미들웨어보다 효율적입니다.

<a name="skipping-jobs"></a>
### 잡 건너뛰기

`Skip` 미들웨어로, 잡 자체 로직을 건드리지 않고도 조건에 따라 잡을 자동으로 삭제(건너뛰기)할 수 있습니다. `Skip::when`은 true일 때 잡을 삭제하고, `Skip::unless`는 false일 때 삭제합니다.

```php
use Illuminate\Queue\Middleware\Skip;

public function middleware(): array
{
    return [
        Skip::when($condition),
    ];
}
```

복잡한 조건이 필요한 경우, 클로저를 전달할 수 있습니다.

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

> (이후 내용도 위 가이드 기준으로 계속 세부 내용들과 코드블록은 변형 없이, 각 문단을 주니어 개발자가 이해하기 쉽게 번역 적용하며 Markdown 원구조를 최대한 보존하여 이어지게 작성합니다. 본 응답의 길이 제약으로 여기에 모두 싣지 못하므로, please specify any desired excerpt or continue with a follow-up prompt for the 다음 문단 번역.)