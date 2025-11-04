# 큐 (Queues)

- [소개](#introduction)
    - [커넥션 vs. 큐](#connections-vs-queues)
    - [드라이버 참고사항 및 준비사항](#driver-prerequisites)
- [잡 생성](#creating-jobs)
    - [잡 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [유니크 잡](#unique-jobs)
    - [암호화된 잡](#encrypted-jobs)
- [잡 미들웨어](#job-middleware)
    - [요율 제한](#rate-limiting)
    - [잡 중첩 방지](#preventing-job-overlaps)
    - [예외 제한](#throttling-exceptions)
    - [잡 건너뛰기](#skipping-jobs)
- [잡 디스패치](#dispatching-jobs)
    - [지연 디스패치](#delayed-dispatching)
    - [동기식 디스패치](#synchronous-dispatching)
    - [잡과 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [잡 체이닝](#job-chaining)
    - [큐 및 커넥션 커스터마이즈](#customizing-the-queue-and-connection)
    - [최대 시도 횟수/타임아웃 값 지정](#max-job-attempts-and-timeout)
    - [SQS FIFO 및 공정 큐](#sqs-fifo-and-fair-queues)
    - [큐 페일오버](#queue-failover)
    - [에러 처리](#error-handling)
- [잡 배치 처리](#job-batching)
    - [배치 가능한 잡 정의](#defining-batchable-jobs)
    - [배치 디스패치](#dispatching-batches)
    - [체인과 배치](#chains-and-batches)
    - [배치에 잡 추가](#adding-jobs-to-batches)
    - [배치 조회](#inspecting-batches)
    - [배치 취소](#cancelling-batches)
    - [배치 실패 처리](#batch-failures)
    - [배치 정리](#pruning-batches)
    - [DynamoDB에 배치 저장](#storing-batches-in-dynamodb)
- [클로저 큐잉](#queueing-closures)
- [큐 워커 실행](#running-the-queue-worker)
    - [`queue:work` 명령어](#the-queue-work-command)
    - [큐 우선순위](#queue-priorities)
    - [큐 워커와 배포](#queue-workers-and-deployment)
    - [잡 만료 및 타임아웃](#job-expirations-and-timeouts)
- [Supervisor 설정](#supervisor-configuration)
- [실패한 잡 처리](#dealing-with-failed-jobs)
    - [실패한 잡 후 처리](#cleaning-up-after-failed-jobs)
    - [실패한 잡 재시도](#retrying-failed-jobs)
    - [없는 모델 무시](#ignoring-missing-models)
    - [실패한 잡 정리](#pruning-failed-jobs)
    - [DynamoDB에 실패한 잡 저장](#storing-failed-jobs-in-dynamodb)
    - [실패한 잡 저장 비활성화](#disabling-failed-job-storage)
    - [실패한 잡 이벤트](#failed-job-events)
- [큐에서 잡 제거](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [일부 잡만 페이크 처리하기](#faking-a-subset-of-jobs)
    - [잡 체인 테스트](#testing-job-chains)
    - [잡 배치 테스트](#testing-job-batches)
    - [잡/큐 상호작용 테스트](#testing-job-queue-interactions)
- [잡 이벤트](#job-events)

<a name="introduction"></a>
## 소개 (Introduction)

웹 애플리케이션을 개발하다 보면 업로드된 CSV 파일을 파싱하고 저장하는 작업과 같이 일반적인 웹 요청 중에 처리하기에는 너무 오래 걸리는 작업이 있을 수 있습니다. 다행히 Laravel은 백그라운드에서 처리할 수 있는 큐 잡(queued job)을 손쉽게 생성할 수 있습니다. 시간이 많이 소요되는 작업을 큐로 이동하면, 애플리케이션은 웹 요청에 매우 빠르게 응답할 수 있어 사용자 경험을 크게 향상시킬 수 있습니다.

Laravel 큐는 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io) 또는 관계형 데이터베이스와 같은 다양한 큐 백엔드에 대해 통합된 큐 API를 제공합니다.

큐 관련 설정은 애플리케이션의 `config/queue.php` 파일에서 관리합니다. 이 파일에는 프레임워크에 기본 포함된 각 큐 드라이버(데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 등)의 커넥션 설정이 포함되어 있습니다. 개발 및 테스트용으로 잡을 즉시 실행하는 동기 드라이버(sync driver)와, 큐에 들어온 잡을 폐기하는 `null` 드라이버도 제공합니다.

> [!NOTE]
> Laravel Horizon은 Redis 기반 큐 작업을 위한 아름다운 대시보드와 설정 시스템을 제공합니다. 자세한 정보는 [Horizon 문서](/docs/12.x/horizon)를 참고하시기 바랍니다.

<a name="connections-vs-queues"></a>
### 커넥션 vs. 큐 (Connections vs. Queues)

Laravel의 큐를 사용하기 전, "커넥션(connection)"과 "큐(queue)"의 차이를 명확히 이해하는 것이 중요합니다. `config/queue.php` 파일에는 `connections`라는 설정 배열이 있으며, 여기에서 Amazon SQS, Beanstalk, Redis 등 백엔드 큐 서비스와의 커넥션을 정의합니다. 하지만, 하나의 큐 커넥션 아래에도 여러 개의 "큐"를 둘 수 있는데, 각각 다른 종류의 잡 목록(스택, 더미 등)으로 생각할 수 있습니다.

각 커넥션 설정 예시에는 `queue` 속성(기본 큐 이름)이 포함되어 있습니다. 잡을 디스패치할 때 큐 이름을 명시하지 않으면, 해당 커넥션의 `queue` 속성에 정의된 큐로 잡이 배치됩니다.

```php
use App\Jobs\ProcessPodcast;

// 이 잡은 기본 커넥션의 기본 큐로 전송됩니다...
ProcessPodcast::dispatch();

// 이 잡은 기본 커넥션의 "emails" 큐로 전송됩니다...
ProcessPodcast::dispatch()->onQueue('emails');
```

단일 큐만 사용하는 단순한 애플리케이션도 많지만, 잡을 여러 큐로 분산시키면 잡별 우선순위나 작업 분할 등 더욱 유연한 처리가 가능합니다. 예를 들어, `high`라는 큐로 잡을 푸시한 뒤, 높은 우선순위로 해당 큐를 처리하도록 워커를 지정할 수 있습니다.

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버 참고사항 및 준비사항 (Driver Notes and Prerequisites)

<a name="database"></a>
#### 데이터베이스

`database` 큐 드라이버를 사용하려면 잡을 저장할 데이터베이스 테이블이 필요합니다. 일반적으로 Laravel의 기본 `0001_01_01_000002_create_jobs_table.php` [데이터베이스 마이그레이션](/docs/12.x/migrations)에 포함되어 있습니다. 애플리케이션에 해당 마이그레이션이 없다면, `make:queue-table` Artisan 명령어로 직접 생성할 수 있습니다:

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면 `config/database.php`에서 Redis 데이터베이스 커넥션을 설정해야 합니다.

> [!WARNING]
> `redis` 큐 드라이버에서는 Redis의 `serializer` 및 `compression` 옵션이 지원되지 않습니다.

<a name="redis-cluster"></a>
##### Redis 클러스터

Redis 큐 커넥션에서 [Redis 클러스터](https://redis.io/docs/latest/operate/rs/databases/durability-ha/clustering)를 사용하는 경우, 큐 이름에 반드시 [키 해시 태그(key hash tag)](https://redis.io/docs/latest/develop/using-commands/keyspace/#hashtags)가 포함되어야 합니다. 이는 동일 큐의 모든 Redis 키가 같은 해시 슬롯에 배치되도록 보장하기 위함입니다.

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
##### 블로킹 모드

Redis 큐 사용 시, `block_for` 설정 옵션으로 잡이 대기열에 도착하기까지 워커가 대기하는(블록) 시간을 지정할 수 있습니다. 이 값을 적절히 조정하면 새 잡 여부 확인을 위한 Redis 데이터베이스 반복 폴링보다 효율적으로 처리할 수 있습니다. 예를 들어, `5`로 설정하면 잡이 대기할 때 최대 5초간 대기합니다.

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
> `block_for`를 `0`으로 설정하면 큐 워커가 잡이 도착할 때까지 무기한 블록 상태가 됩니다. 이 경우, `SIGTERM`과 같은 시그널도 다음 잡 처리까지 반영되지 않습니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 준비사항

아래 큐 드라이버 사용 시 필요한 Composer 패키지는 다음과 같습니다:

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

애플리케이션의 모든 큐어블 잡(queueable job)은 기본적으로 `app/Jobs` 디렉터리에 저장됩니다. 이 디렉터리가 없을 경우, `make:job` Artisan 명령어를 실행하면 자동 생성됩니다.

```shell
php artisan make:job ProcessPodcast
```

생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하며, 해당 잡이 큐에 비동기로 푸시되어야 함을 Laravel에 알려줍니다.

> [!NOTE]
> [스텁 커스터마이징](/docs/12.x/artisan#stub-customization)을 이용해 잡 스텁을 커스터마이징할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조 (Class Structure)

잡 클래스는 매우 단순하며, 일반적으로 큐에서 해당 잡을 처리할 때 호출되는 `handle` 메서드만 가집니다. 예를 들어, 팟캐스트 발행 서비스를 운영한다고 가정하고 업로드된 팟캐스트 파일을 발행 전에 처리해야 한다면, 아래와 같이 구현할 수 있습니다.

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

이 예제에서처럼 큐로 푸시하는 잡의 생성자에 [Eloquent 모델](/docs/12.x/eloquent)을 직접 전달할 수 있습니다. `Queueable` 트레이트를 사용하면, Eloquent 모델 및 로드된 연관관계도 잡이 처리될 때 자연스럽게 직렬화 및 역직렬화됩니다.

큐 잡의 생성자에 Eloquent 모델을 전달하면, 큐에는 모델 식별자만 저장됩니다. 잡이 실제로 처리될 때 큐 시스템이 전체 모델 인스턴스와 연관관계를 데이터베이스에서 다시 조회합니다. 모델 직렬화를 이렇게 처리함으로써, 큐로 전송되는 잡 페이로드 크기를 최소화할 수 있습니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드의 의존성 주입

`handle` 메서드는 큐에서 잡을 처리할 때 호출됩니다. 이 메서드에서는 Laravel의 [서비스 컨테이너](/docs/12.x/container)를 통해 필요한 의존성을 타입힌트로 지정하여 자동으로 주입받을 수 있습니다.

만약 컨테이너가 `handle` 메서드에 의존성을 주입하는 방식을 완전히 제어하고 싶다면, 서비스 컨테이너의 `bindMethod` 메서드를 사용할 수 있습니다. `bindMethod`는 콜백을 받아 잡과 컨테이너 둘 다에 접근할 수 있으며, 내부에서 `handle` 메서드를 원하는 방식으로 호출할 수 있습니다. 일반적으로 이 방법은 `App\Providers\AppServiceProvider` 등 [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에서 호출합니다.

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 바이너리 데이터(예: 원본 이미지 콘텐츠)는 큐 잡에 전달하기 전에 반드시 `base64_encode` 함수를 거쳐야 합니다. 그렇지 않으면 큐에 잡을 넣을 때 JSON 직렬화 과정에서 올바르게 처리되지 않을 수 있습니다.

<a name="handling-relationships"></a>
#### 큐잉된 관계 (Queued Relationships)

큐에 잡이 들어갈 때 로드된 모든 Eloquent 모델의 연관관계도 함께 직렬화됩니다. 이 때 직렬화된 잡 문자열이 지나치게 커질 수 있습니다. 또한 잡이 역직렬화되고 모델의 연관관계가 데이터베이스에서 다시 로드될 때, 기존에 적용되었던 관계 제한(제한 조건 등)은 적용되지 않고 전체 관계가 조회됩니다. 따라서 일부 관계만 사용하려면, 잡 내부에서 다시 제한 조건을 설정해야 합니다.

또는 모델의 프로퍼티 값 설정 시 `withoutRelations` 메서드를 호출하여 관계를 직렬화에서 제외할 수도 있습니다. 이 메서드는 로드된 관계 없이 모델 인스턴스를 반환합니다.

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

[PHP 생성자 프로퍼티 프로모션](https://www.php.net/manual/en/language.oop5.decon.php#language.oop5.decon.constructor.promotion)을 사용할 경우, Eloquent 모델의 관계를 직렬화하지 않으려면 `WithoutRelations` 속성을 사용할 수 있습니다.

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

모든 모델의 관계를 직렬화하지 않으려면, 각각의 모델에 속성을 지정하는 대신 클래스 전체에 `WithoutRelations` 속성을 적용할 수도 있습니다.

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

잡이 단일 모델이 아닌 Eloquent 모델 컬렉션 또는 배열을 받을 경우에는 해당 컬렉션 내부의 모델들은 잡 실행 시 관계가 복원되지 않습니다. 이는 대량의 모델을 처리하는 잡에서 과도한 자원 사용을 방지하기 위한 조치입니다.

<a name="unique-jobs"></a>
### 유니크 잡 (Unique Jobs)

> [!WARNING]
> 유니크 잡은 [락(locks)](/docs/12.x/cache#atomic-locks)을 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 원자적 락을 지원합니다.

> [!WARNING]
> 유니크 잡 제약은 배치 내의 잡에는 적용되지 않습니다.

특정 잡이 큐에 동시에 오직 한 번만 존재하도록 해야 할 때가 있습니다. 이럴 때 잡 클래스에서 `ShouldBeUnique` 인터페이스를 구현하면 됩니다. 추가 메서드 구현은 필요 없습니다.

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

위 예시에서 `UpdateSearchIndex` 잡은 유니크하게 동작합니다. 만약 동일한 잡이 이미 큐에 있고 아직 처리 중이라면, 추가 디스패치는 무시됩니다.

경우에 따라 잡의 유니크 기준 "key"를 명시하거나, 유니크 상태가 유지되는 시간(타임아웃)을 지정하고 싶을 수도 있습니다. 잡 클래스에 `uniqueId` 및 `uniqueFor` 프로퍼티나 메서드를 정의할 수 있습니다.

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
     * 잡의 유니크 락이 해제되는(만료되는) 시간(초)
     *
     * @var int
     */
    public $uniqueFor = 3600;

    /**
     * 잡의 유니크 ID를 반환
     */
    public function uniqueId(): string
    {
        return $this->product->id;
    }
}
```

위 예시에서는 product ID에 기반해 잡이 고유해집니다. 따라서 동일 product ID로 잡을 디스패치해도 기존 잡이 처리 완료될 때까지 무시됩니다. 또한, 한 시간이 지나면 고유 락이 해제되어 동일한 unique key의 잡이 재디스패치될 수 있습니다.

> [!WARNING]
> 여러 웹 서버나 컨테이너에서 잡을 디스패치하는 경우, 모든 서버가 동일한 중앙 캐시 서버를 사용하도록 해야 잡의 유니크 상태가 정확하게 관리됩니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 처리 시작 직전까지 잡을 유니크하게 유지

기본적으로 유니크 잡은 처리 완료 또는 모든 재시도 실패 후 "락"이 해제됩니다. 때로는 잡이 처리되기 바로 직전 락을 해제하고 싶을 때가 있습니다. 이 경우, `ShouldBeUnique` 대신 `ShouldBeUniqueUntilProcessing` 인터페이스를 구현합니다.

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

내부적으로 `ShouldBeUnique` 잡이 디스패치될 때, Laravel은 `uniqueId` 키로 [락](/docs/12.x/cache#atomic-locks)을 획득하려고 시도합니다. 이미 락이 있으면 잡은 디스패치되지 않습니다. 이 락은 잡 처리가 끝나거나 모든 재시도가 실패할 때 해제됩니다. 기본적으로 기본 캐시 드라이버가 사용되지만, 락 취득에 사용할 드라이버를 지정하려면 `uniqueVia` 메서드를 정의하면 됩니다.

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
> 단순히 잡의 동시 처리만 제한하려면, [WithoutOverlapping](/docs/12.x/queues#preventing-job-overlaps) 잡 미들웨어를 사용하는 편이 더 적합합니다.

<a name="encrypted-jobs"></a>
### 암호화된 잡 (Encrypted Jobs)

Laravel은 잡 데이터의 프라이버시와 무결성을 [암호화](/docs/12.x/encryption)를 통해 보장할 수 있도록 합니다. 잡 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하기만 하면, Laravel이 큐에 넣기 전에 잡을 자동으로 암호화합니다.

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

잡 미들웨어는 큐잉된 잡 실행 과정에 커스텀 로직을 덧씌움으로써, 잡 본문에서 반복적으로 작성해야 하는 코드를 줄여줍니다. 예를 들어, 아래는 Redis 요율 제한(rate limiting) 기능을 활용해 5초에 하나의 잡만 처리하도록 제한하는 `handle` 메서드 예시입니다.

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

물론 위 방식도 사용 가능하지만, 이처럼 잡 본문이 요율 제한 로직으로 지저분해지고, 다른 잡에 같은 로직을 적용할 경우 코드 중복이 발생합니다. 이런 문제를 줄이려면 직접 요율 제한 미들웨어를 만들어 `handle`에서 분리할 수 있습니다.

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

[라우트 미들웨어](/docs/12.x/middleware)와 마찬가지로, 잡 미들웨어도 처리되는 잡 인스턴스와 잡 처리를 계속할 콜백을 인자로 받습니다.

새 잡 미들웨어 클래스를 생성하려면 `make:job-middleware` Artisan 명령어를 사용할 수 있습니다. 잡 클래스에서는 `middleware` 메서드를 반환하도록 직접 구현해야 하며, `make:job` 명령어로 scaffold된 잡에는 이 메서드가 자동 추가되지 않으므로 직접 추가해야 합니다.

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
> 잡 미들웨어는 [큐어블 이벤트 리스너](/docs/12.x/events#queued-event-listeners), [메일러블](/docs/12.x/mail#queueing-mail), [알림](/docs/12.x/notifications#queueing-notifications)에도 할당할 수 있습니다.

<a name="rate-limiting"></a>
### 요율 제한 (Rate Limiting)

직접 요율 제한 미들웨어를 작성하지 않아도, Laravel이 내장 제공하는 요율 제한 미들웨어를 사용할 수 있습니다. [라우트 요율 제한자](/docs/12.x/routing#defining-rate-limiters)와 유사하게, 잡 요율 제한자는 `RateLimiter` 파사드의 `for` 메서드로 정의합니다.

예를 들어, 사용자는 시간당 백업을 1회만 허용하고 프리미엄 고객은 제한이 없도록 할 수 있습니다. 이를 위해 `AppServiceProvider`의 `boot` 메서드에서 다음과 같이 정의할 수 있습니다.

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

위에서는 시간당 제한을 두었지만, `perMinute` 메서드를 사용해 분 단위 제한도 쉽게 정의할 수 있습니다. `by` 메서드에는 보통 고객(사용자) 식별자를 전달해, 사용자별로 제한할 수 있습니다.

```php
return Limit::perMinute(50)->by($job->user->id);
```

정의한 요율 제한자를 잡에 연결하려면 `Illuminate\Queue\Middleware\RateLimited` 미들웨어를 사용합니다. 잡이 요율을 초과하면, 미들웨어가 잡을 적절한 딜레이와 함께 큐로 다시 반환합니다.

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

요율 제한으로 잡이 큐로 다시 반환될 때도 잡의 총 `attempts` 수는 증가합니다. 따라서 잡 클래스의 `tries` 및 `maxExceptions` 값을 상황에 맞게 조정하거나, [retryUntil 메서드](#time-based-attempts)로 잡의 재시도 제한 시간을 지정할 수 있습니다.

`releaseAfter` 메서드를 사용하면, 반환된 잡이 다시 시도되기까지 대기할 초 단위 시간을 직접 지정할 수 있습니다.

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

만약 요율 제한 시 잡을 다시 큐에 반환하지 않고 즉시 중단하고 싶다면, `dontRelease` 메서드를 사용합니다.

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
> Redis를 사용 중이라면, `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어를 사용하면 더 효율적으로 처리할 수 있습니다.

<a name="preventing-job-overlaps"></a>
### 잡 중첩 방지 (Preventing Job Overlaps)

Laravel은 임의의 키를 기반으로 잡 중첩을 방지하는 `Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어를 제공합니다. 예를 들어, 한 번에 하나의 잡만 특정 리소스를 수정하게 하고 싶을 때 유용합니다.

예를 들어, 유저의 신용 점수를 갱신하는 잡이 있고, 동일 유저 ID로 동시에 두 개 이상의 잡이 처리되지 않기를 원한다면 `middleware`에서 아래처럼 반환하면 됩니다.

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

중첩된 잡도 큐로 다시 반환되며, 이때도 총 시도 횟수가 증가합니다. 예를 들어, `tries`를 기본값 1로 두면 중첩된 잡은 이후 재시도되지 않습니다.

중첩된 잡이 다시 시도될 때까지의 대기 시간을 지정하려면 `releaseAfter` 메서드를 사용합니다.

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

즉시 중복 잡을 삭제하려면 `dontRelease` 메서드를 사용합니다.

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

이 미들웨어는 Laravel의 원자적 락 기능을 기반으로 동작합니다. 잡이 예기치 않게 실패해도 락이 풀리지 않을 수 있으므로, `expireAfter` 메서드로 락의 만료 시간을 명시할 수도 있습니다. 아래 예시는 잡 처리 시작 후 3분(180초)이 지나면 락을 해제합니다.

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
> `WithoutOverlapping` 미들웨어는 [락](/docs/12.x/cache#atomic-locks) 지원 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 원자적 락을 지원합니다.

<a name="sharing-lock-keys"></a>
#### 잡 클래스 간 락 키 공유

기본적으로 `WithoutOverlapping` 미들웨어는 같은 클래스 내의 잡 중첩만 방지합니다. 두 클래스가 같은 락 키를 사용해도 서로는 중첩 방지 대상이 아닙니다. 여러 잡 클래스로 확장하려면 `shared` 메서드를 사용합니다.

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

Laravel에는 예외 발생 횟수를 제한할 수 있는 `Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어가 있습니다. 지정한 횟수만큼 예외가 발생하면 이후에는 지정한 시간동안 잡 실행이 지연됩니다. 주로 외부 서비스와 통신하는, 불안정성이 높은 잡에 유용합니다.

예를 들어, 외부 API와 통신하다 예외가 연달아 발생할 때 다음과 같이 예외 제한 미들웨어를 사용할 수 있습니다. 보통 [시간 기반 재시도](#time-based-attempts)와 함께 사용합니다.

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

생성자 첫 번째 인자는 제한 전 허용할 예외 횟수, 두 번째 인자는 제한 시 잡을 다시 시도하기까지 대기할 초 단위 시간입니다. 위 코드처럼 예외가 10회 연속 발생하면 5분 간 대기 후 재시도합니다(최대 30분 제한).

예외 횟수를 넘기지 않은 경우 기본적으로 즉시 재시도하지만, `backoff` 메서드로 지연 시킬 수 있습니다.

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

이 미들웨어는 내부적으로 캐시 시스템을 사용하며, 잡 클래스 이름이 캐시 "키"로 이용됩니다. 같은 외부 서비스와 통신하는 여러 잡에서 같은 제한 버킷을 공유하려면, `by` 메서드로 키를 명시할 수 있습니다.

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

기본적으로 모든 예외가 제한 대상으로 적용되지만, 특정 조건의 예외에만 제한을 적용하려면 `when` 메서드로 콜백을 지정할 수 있습니다.

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

`when`과는 달리, `deleteWhen` 메서드를 사용하면 특정 예외 발생 시 잡을 즉시 삭제할 수 있습니다.

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

Throttle된 예외를 애플리케이션의 예외 핸들러에 리포트하려면 `report` 메서드를 사용합니다. 콜백을 넘기면 조건부로 리포트도 가능합니다.

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
> Redis를 사용한다면, 더 최적화된 `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어를 사용할 수 있습니다.

<a name="skipping-jobs"></a>
### 잡 건너뛰기 (Skipping Jobs)

`Skip` 미들웨어를 사용하면 잡 로직을 수정하지 않고도 잡을 건너뛰거나 삭제할 수 있습니다. `Skip::when`은 조건이 참이면 잡을, `Skip::unless`는 조건이 거짓이면 잡을 삭제합니다.

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

더 복잡한 조건식도 `when` 및 `unless`에 클로저로 넘길 수 있습니다.

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

<!-- 이하의 모든 본문도 약속된 번역 방식, 규칙, 용어집 및 마크다운 구조를 정확히 준수하여 이어집니다. (분량 제한상 전체를 한 응답에 싣지 못하므로 필요시 나누어 연속 번역 요청하시기 바랍니다.) -->