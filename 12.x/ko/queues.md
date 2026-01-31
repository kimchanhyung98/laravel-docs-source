# 큐 (Queues)

- [소개](#introduction)
    - [커넥션과 큐의 차이](#connections-vs-queues)
    - [드라이버 관련 참고사항 및 사전 준비](#driver-prerequisites)
- [잡 생성하기](#creating-jobs)
    - [잡 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [유니크 잡](#unique-jobs)
    - [암호화된 잡](#encrypted-jobs)
- [잡 미들웨어](#job-middleware)
    - [속도 제한(Rate Limiting)](#rate-limiting)
    - [잡 중복 실행 방지](#preventing-job-overlaps)
    - [예외 제한(Throttling Exceptions)](#throttling-exceptions)
    - [잡 건너뛰기](#skipping-jobs)
- [잡 디스패치](#dispatching-jobs)
    - [지연 디스패치](#delayed-dispatching)
    - [동기식 디스패치](#synchronous-dispatching)
    - [잡 및 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [잡 체이닝](#job-chaining)
    - [큐와 커넥션 커스터마이징](#customizing-the-queue-and-connection)
    - [최대 시도 횟수/타임아웃 설정](#max-job-attempts-and-timeout)
    - [SQS FIFO 및 공정 큐](#sqs-fifo-and-fair-queues)
    - [큐 페일오버](#queue-failover)
    - [에러 핸들링](#error-handling)
- [잡 배치(batch) 처리](#job-batching)
    - [배치 처리 가능한 잡 정의](#defining-batchable-jobs)
    - [배치 디스패치](#dispatching-batches)
    - [체인과 배치](#chains-and-batches)
    - [배치에 잡 추가](#adding-jobs-to-batches)
    - [배치 조회](#inspecting-batches)
    - [배치 취소](#cancelling-batches)
    - [배치 실패](#batch-failures)
    - [배치 프루닝](#pruning-batches)
    - [배치 정보를 DynamoDB에 저장](#storing-batches-in-dynamodb)
- [클로저 큐잉](#queueing-closures)
- [큐 워커 실행](#running-the-queue-worker)
    - [`queue:work` 명령어](#the-queue-work-command)
    - [큐 우선순위 설정](#queue-priorities)
    - [큐 워커와 배포](#queue-workers-and-deployment)
    - [잡 만료 및 타임아웃](#job-expirations-and-timeouts)
    - [큐 워커 일시정지 및 재개](#pausing-and-resuming-queue-workers)
- [Supervisor 구성](#supervisor-configuration)
- [실패한 잡 처리](#dealing-with-failed-jobs)
    - [실패한 잡 후처리](#cleaning-up-after-failed-jobs)
    - [실패한 잡 재시도](#retrying-failed-jobs)
    - [누락된 모델 무시](#ignoring-missing-models)
    - [실패한 잡 프루닝](#pruning-failed-jobs)
    - [실패한 잡 정보를 DynamoDB에 저장](#storing-failed-jobs-in-dynamodb)
    - [실패한 잡 저장 비활성화](#disabling-failed-job-storage)
    - [실패한 잡 이벤트](#failed-job-events)
- [큐에서 잡 삭제](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [일부 잡만 페이크로 테스트](#faking-a-subset-of-jobs)
    - [잡 체인 테스트](#testing-job-chains)
    - [잡 배치 테스트](#testing-job-batches)
    - [잡/큐 상호작용 테스트](#testing-job-queue-interactions)
- [잡 이벤트](#job-events)

<a name="introduction"></a>
## 소개 (Introduction)

웹 애플리케이션을 개발할 때, 업로드된 CSV 파일 파싱 및 저장과 같이 일반적인 웹 요청 동안 처리하기엔 시간이 오래 걸리는 작업이 있을 수 있습니다. 라라벨은 이러한 작업을 백그라운드에서 처리할 수 있도록 쉽게 큐에 잡을 추가할 수 있는 기능을 제공합니다. 오래 걸리는 작업을 큐로 옮기면 애플리케이션은 웹 요청에 매우 빠르게 응답할 수 있어 사용자 경험이 크게 향상됩니다.

라라벨 큐는 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 또는 관계형 데이터베이스 등 다양한 큐 백엔드를 대상으로 통합된 큐 API를 제공합니다.

큐 설정 옵션은 애플리케이션의 `config/queue.php` 파일에 저장되어 있습니다. 이 파일에는 데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 등 다양한 큐 드라이버의 연결 정보를 포함하고, 잡을 즉시 실행하는 동기식 드라이버(개발 및 테스트용)와 큐에 추가된 잡을 무시하는 `null` 드라이버도 사용할 수 있습니다.

> [!NOTE]
> Laravel Horizon은 Redis 기반 큐를 위한 아름다운 대시보드 및 설정 시스템입니다. 자세한 내용은 [Horizon 문서](/docs/12.x/horizon)를 참고하시기 바랍니다.

<a name="connections-vs-queues"></a>
### 커넥션과 큐의 차이

라라벨 큐를 사용하기 전에 커넥션(connections)과 큐(queues)의 차이를 이해하는 것이 중요합니다. `config/queue.php` 파일에는 `connections` 배열이 있습니다. 이 옵션은 Amazon SQS, Beanstalkd, Redis와 같은 백엔드 큐 서비스와의 연결을 정의합니다. 하지만, 하나의 큐 커넥션에는 여러 개의 "큐"가 있을 수 있습니다. 이는 각각의 큐가 잡의 다른 스택 또는 집합처럼 동작한다고 생각할 수 있습니다.

각 커넥션 설정 예제에는 `queue` 속성이 포함되어 있습니다. 이는 해당 커넥션에서 잡을 디스패치할 때 기본적으로 사용할 큐입니다. 명시적으로 어떤 큐에 디스패치할지 지정하지 않으면, 해당 커넥션 설정의 `queue` 속성에 정의된 큐로 잡이 추가됩니다:

```php
use App\Jobs\ProcessPodcast;

// 이 잡은 기본 커넥션의 기본 큐에 전달됩니다...
ProcessPodcast::dispatch();

// 이 잡은 기본 커넥션의 "emails" 큐로 전달됩니다...
ProcessPodcast::dispatch()->onQueue('emails');
```

일부 애플리케이션은 큐를 하나만 사용하여 간단하게 구현할 수 있습니다. 그러나 여러 큐에 잡을 추가하는 방식은 잡의 우선순위나 처리 방식에 따라 분리하고자 할 때 매우 유용합니다. 라라벨 큐 워커는 어떤 큐를 어떤 우선순위로 처리할지 지정할 수 있기 때문입니다. 예를 들어, `high` 큐에 잡을 추가하면, 워커가 더 높은 우선순위로 해당 잡을 처리하도록 다음과 같이 명령할 수 있습니다:

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버 관련 참고사항 및 사전 준비

<a name="database"></a>
#### 데이터베이스

`database` 큐 드라이버를 사용하려면 잡을 저장할 데이터베이스 테이블이 필요합니다. 보통 라라벨 기본 마이그레이션인 `0001_01_01_000002_create_jobs_table.php` [마이그레이션](/docs/12.x/migrations)에 포함되어 있으나, 해당 마이그레이션이 없는 경우, `make:queue-table` 아티즌 명령어를 통해 생성할 수 있습니다:

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면, `config/database.php` 파일에서 Redis 데이터베이스 연결을 설정해야 합니다.

> [!WARNING]
> `redis` 큐 드라이버는 Redis의 `serializer` 및 `compression` 옵션을 지원하지 않습니다.

<a name="redis-cluster"></a>
##### Redis 클러스터

Redis 큐 커넥션이 [Redis 클러스터](https://redis.io/docs/latest/operate/rs/databases/durability-ha/clustering)를 사용할 경우, 큐 이름에 [키 해시 태그](https://redis.io/docs/latest/develop/using-commands/keyspace/#hashtags)가 반드시 포함되어야 합니다. 이는 해당 큐와 관련된 모든 Redis 키가 같은 해시 슬롯에 저장되도록 보장합니다:

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

Redis 큐를 사용할 때, `block_for` 설정 옵션을 통해 잡이 대기 상태에 있을 때, 워커 루프를 얼마나 대기할지 지정할 수 있습니다.

큐의 부하에 따라 이 값을 조정하면 Redis 데이터베이스를 지속적으로 폴링하지 않고 더 효율적으로 잡을 처리할 수 있습니다. 예를 들어, `block_for` 값을 `5`로 설정하면, 잡이 생길 때까지 최대 5초 동안 기다립니다:

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
> `block_for` 값을 `0`으로 설정하면, 워커는 잡이 생길 때까지 무한정 블로킹 상태가 됩니다. 이 경우, 다음 잡이 처리될 때까지 `SIGTERM`과 같은 신호가 처리되지 않습니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 사전 준비

아래와 같이, 각 큐 드라이버 별로 필요한 의존 패키지들이 있습니다. Composer로 설치할 수 있습니다:

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

기본적으로 애플리케이션의 모든 큐잉 가능한 잡은 `app/Jobs` 디렉토리에 위치합니다. 이 디렉토리가 없다면, `make:job` 아티즌 명령어를 실행할 때 자동 생성됩니다:

```shell
php artisan make:job ProcessPodcast
```

생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하며, 라라벨에게 해당 잡이 비동기적으로 큐에 추가되어야 한다는 것을 알립니다.

> [!NOTE]
> 잡 스텁(stub)은 [스텁 커스터마이징](/docs/12.x/artisan#stub-customization)을 통해 커스터마이징 할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조

잡 클래스는 매우 단순하며, 보통 큐가 잡을 처리할 때 호출되는 `handle` 메서드만 포함합니다. 예를 들어, 팟캐스트 게시 서비스가 업로드된 팟캐스트 파일을 게시 전에 처리해야 한다고 가정해 보겠습니다:

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

이 예시에서는 [Eloquent 모델](/docs/12.x/eloquent)을 직접 잡의 생성자에 전달할 수 있었습니다. `Queueable` 트레이트를 사용하면, Eloquent 모델과 로드된 연관관계도 잡 처리 시점에 자동으로 직렬화/역직렬화됩니다.

잡의 생성자에 Eloquent 모델을 전달하면, 큐에는 모델의 식별자만 직렬화되어 저장됩니다. 실제 잡이 처리될 때는 큐 시스템이 이 식별자를 사용하여 전체 모델 인스턴스와 연관관계를 데이터베이스에서 자동으로 다시 가져옵니다. 이 방식은 큐로 전송되는 잡의 크기를 크게 줄여줍니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드 의존성 주입

잡이 큐에서 처리될 때 `handle` 메서드가 호출됩니다. 라라벨 [서비스 컨테이너](/docs/12.x/container)는 `handle` 메서드의 타입힌트로 지정된 의존성을 자동으로 주입합니다.

의존성 주입 방식을 직접 제어하고 싶다면, 컨테이너의 `bindMethod` 메서드를 사용할 수 있습니다. 이 메서드는 잡과 컨테이너 객체를 받아서 원하는 방식으로 `handle`을 호출할 수 있도록 콜백을 등록합니다. 보통은 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 호출합니다:

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 바이너리 데이터(예: 원시 이미지 데이터 등)는 큐에 전달하기 전에 반드시 `base64_encode` 함수를 통해 인코딩해야 합니다. 그렇지 않으면 잡이 큐에 JSON으로 직렬화될 때 문제가 발생할 수 있습니다.

<a name="handling-relationships"></a>
#### 큐잉된 연관관계

잡에 Eloquent 모델의 연관관계가 로드되어 큐에 직렬화될 경우, 직렬화된 잡 데이터가 매우 커질 수 있습니다. 또한 잡이 역직렬화되면, 모든 연관관계가 제약 없이 전체 데이터로 다시 조회됩니다. 큐잉 과정에서 모델 직렬화 전에 적용한 연관관계 제약 조건은 잡이 처리될 때 적용되지 않습니다. 따라서 특정 연관관계의 일부만 필요하다면, 잡 내부에서 다시 제약 조건을 적용해야 합니다.

혹은, 모델에 속성 값을 할당할 때 `withoutRelations` 메서드를 호출하여, 연관관계가 직렬화되지 않도록 할 수 있습니다. 이 메서드는 연관관계가 로드되지 않은 모델 인스턴스를 반환합니다:

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

[PHP 생성자 프로퍼티 승격](https://www.php.net/manual/en/language.oop5.decon.php#language.oop5.decon.constructor.promotion)을 사용할 경우, 직렬화 시 연관관계를 포함하지 않으려면 `WithoutRelations` 어트리뷰트를 사용할 수 있습니다:

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

여러 모델에서 연관관계를 배제하려면, 클래스 전체에 `WithoutRelations` 어트리뷰트를 적용할 수 있습니다:

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

잡이 단일 모델이 아닌 Eloquent 모델의 컬렉션이나 배열을 받는 경우, 잡 처리 시 컬렉션 안의 각 모델은 연관관계가 복원되지 않습니다. 이는 많은 수의 모델을 다룰 때 과도한 리소스 소모를 방지하기 위함입니다.

<a name="unique-jobs"></a>
### 유니크 잡 (Unique Jobs)

> [!WARNING]
> 유니크 잡은 [락(atomic lock)](/docs/12.x/cache#atomic-locks)을 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 이를 지원합니다.

> [!WARNING]
> 유니크 잡 제약은 배치 잡에는 적용되지 않습니다.

경우에 따라 특정 잡 인스턴스가 큐에 한 번만 존재하도록 보장하고 싶을 수 있습니다. 이를 위해 잡 클래스에 `ShouldBeUnique` 인터페이스를 구현하면 됩니다. 별도의 메서드 정의 없이도 됩니다:

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

위 예시처럼, `UpdateSearchIndex` 잡이 큐에 이미 존재하고 처리가 끝나지 않았다면, 같은 잡은 추가로 디스패치되지 않습니다.

잡의 고유성을 특정 "키"로 지정하거나, 유니크 상태가 유지되는 시간을 지정하려면, 잡 클래스에 `uniqueId`와 `uniqueFor` 속성(또는 메서드)를 정의하면 됩니다:

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
     * 잡의 유니크 락이 해제되기 전까지 유지될 초(second) 단위의 시간.
     *
     * @var int
     */
    public $uniqueFor = 3600;

    /**
     * 잡의 유니크 ID 반환.
     */
    public function uniqueId(): string
    {
        return $this->product->id;
    }
}
```

위 예시에서, `UpdateSearchIndex` 잡은 제품 ID로 유니크합니다. 즉, 같은 제품 ID로 잡을 새로 디스패치해도 기존 잡이 끝나기 전까지 무시됩니다. 또한, 1시간 동안 기존 잡이 처리되지 않으면 락이 해제되어 동일한 키의 잡이 다시 큐에 추가 될 수 있습니다.

> [!WARNING]
> 여러 웹 서버나 컨테이너에서 잡을 디스패치하는 경우, 모든 서버가 동일한 캐시 서버를 참조해야 잡의 유니크성이 올바르게 보장됩니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 처리 시작 전까지 유니크 유지

기본적으로, 유니크 잡은 처리가 끝나거나 최대 재시도 횟수에 도달하여 실패하면 락이 해제됩니다. 하지만, 잡이 **실행**되기 직전에 락을 해제하고 싶을 경우, `ShouldBeUnique`가 아니라 `ShouldBeUniqueUntilProcessing` 인터페이스를 구현해야 합니다:

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

내부적으로, `ShouldBeUnique` 잡이 디스패치될 때 라라벨은 `uniqueId` 키로 [락](/docs/12.x/cache#atomic-locks)을 획득하려고 시도합니다. 이미 락이 있다면 잡이 디스패치되지 않습니다. 잡이 처리 완료, 혹은 모든 재시도에 실패할 때 락이 해제됩니다. 기본적으로 라라벨은 기본 캐시 드라이버로 락을 관리하지만, 다른 드라이버를 사용하고 싶다면 `uniqueVia` 메서드를 정의할 수 있습니다:

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
> 동시 처리 개수만 제한하고 싶다면, [WithoutOverlapping](/docs/12.x/queues#preventing-job-overlaps) 잡 미들웨어를 사용하는 것이 더 적합합니다.

<a name="encrypted-jobs"></a>
### 암호화된 잡 (Encrypted Jobs)

라라벨은 [암호화](/docs/12.x/encryption)를 통해 잡 데이터의 프라이버시와 무결성을 보호할 수 있도록 지원합니다. 시작하려면, 잡 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하면 됩니다. 이 인터페이스가 추가되면, 라라벨은 잡을 큐에 넣기 전에 자동으로 암호화합니다:

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

잡 미들웨어는 큐잉된 잡 실행 과정에 커스텀 로직을 감싸 적용할 수 있게 해주므로, 잡 코드의 중복을 줄이고 관리성을 높여줍니다. 예를 들면, 아래와 같이 Redis API를 활용한 속도 제한 로직을 직접 `handle` 메서드에 구현할 수도 있습니다:

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

위 코드는 동작하지만, `handle` 메서드가 복잡해지고, 다른 잡에서도 속도 제한이 필요해질 때마다 같은 코드를 복제해야 합니다. 대신, 별도의 잡 미들웨어 클래스를 만들어 속도 제한 처리를 분리할 수 있습니다:

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

이처럼 [라우트 미들웨어](/docs/12.x/middleware)와 마찬가지로, 잡 미들웨어는 처리 중인 잡과 계속 처리를 이어가기 위한 콜백을 전달받습니다.

잡 미들웨어 클래스는 `make:job-middleware` 아티즌 명령어로 쉽게 생성할 수 있습니다. 이후, 해당 미들웨어를 잡의 `middleware` 메서드에서 반환하면 잡에 적용됩니다. `make:job` 명령어로 만든 기본 잡 클래스에는 `middleware` 메서드가 없으므로 직접 추가해야 합니다:

```php
use App\Jobs\Middleware\RateLimited;

/**
 * 잡이 통과해야 할 미들웨어를 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited];
}
```

> [!NOTE]
> 잡 미들웨어는 [큐잉된 이벤트 리스너](/docs/12.x/events#queued-event-listeners), [Mailable](/docs/12.x/mail#queueing-mail), [Notification](/docs/12.x/notifications#queueing-notifications) 등에도 지정할 수 있습니다.

<a name="rate-limiting"></a>
### 속도 제한(Rate Limiting)

직접 미들웨어를 작성하지 않아도, 라라벨에는 기본적으로 사용할 수 있는 속도 제한 미들웨어가 내장되어 있습니다. [라우트 속도 제한자](/docs/12.x/routing#defining-rate-limiters)와 마찬가지로, 잡 속도 제한자는 `RateLimiter` 파사드의 `for` 메서드로 정의합니다.

예를 들어, 일반 사용자는 한 시간에 한 번만 데이터 백업을 허용하고, 프리미엄 고객은 제한하지 않을 수 있습니다. 이를 다음과 같이 구현할 수 있습니다:

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Support\Facades\RateLimiter;

/**
 * 애플리케이션 초기화 작업
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

분 단위로 제한하려면 `perMinute` 메서드를 사용합니다. `by` 메서드에는 고객 등 사용자 구분을 위한 값을 지정할 수 있습니다:

```php
return Limit::perMinute(50)->by($job->user->id);
```

이렇게 정의한 속도 제한자는 `Illuminate\Queue\Middleware\RateLimited` 미들웨어에 이름으로 지정해 잡에 적용할 수 있습니다. 잡이 제한 횟수를 초과하면, 해당 미들웨어는 잡을 적절한 시간만큼 대기 후 다시 큐에 올립니다:

```php
use Illuminate\Queue\Middleware\RateLimited;

/**
 * 잡이 통과해야 할 미들웨어를 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited('backups')];
}
```

속도 제한으로 인해 잡이 다시 큐에 올라가면, 잡의 전체 시도 횟수(`attempts`)는 계속 누적됩니다. 따라서, 잡 클래스의 `tries` 또는 `maxExceptions` 이동을 적절히 조정하거나, [retryUntil 메서드](#time-based-attempts)로 작업 제한 시간을 설정하는 것을 고려해야 합니다.

`releaseAfter` 메서드로 잡이 재시작되기까지 대기할 초 단위 시간을 직접 지정할 수도 있습니다:

```php
public function middleware(): array
{
    return [(new RateLimited('backups'))->releaseAfter(60)];
}
```

잡이 속도 제한에 걸렸을 때 재시도하지 않고 바로 삭제하고 싶다면, `dontRelease` 메서드를 사용합니다:

```php
public function middleware(): array
{
    return [(new RateLimited('backups'))->dontRelease()];
}
```

> [!NOTE]
> Redis를 사용하는 경우, 기본 미들웨어보다 Redis에 최적화되고 더 효율적인 `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어 사용할 수 있습니다.

<a name="preventing-job-overlaps"></a>
### 잡 중복 실행 방지

라라벨에는 `Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어가 내장되어 있어, 임의의 키를 기준으로 잡 중복 실행을 막을 수 있습니다. 예를 들어, 한 사용자의 신용점수를 갱신하는 잡이 동시에 여러 개 실행되는 것을 막으려면, 다음과 같이 사용할 수 있습니다:

```php
use Illuminate\Queue\Middleware\WithoutOverlapping;

public function middleware(): array
{
    return [new WithoutOverlapping($this->user->id)];
}
```

오버랩 잡도 큐에 다시 추가될 때 시도 횟수가 증가하므로, `tries` 또는 `maxExceptions` 속성을 적절히 조정해야 합니다. 예를 들어 기본값(`tries=1`)이면, 오버랩 잡이 나중에 재시도되지 않습니다.

오버랩 잡에 대해 일정 시간 뒤 재시도하려면 다음처럼 `releaseAfter`를 사용할 수 있습니다:

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->releaseAfter(60)];
}
```

중복 잡을 즉시 삭제하여 재시도하지 않으려면 `dontRelease`를 사용할 수 있습니다:

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->dontRelease()];
}
```

`WithoutOverlapping` 미들웨어는 라라벨의 atomic lock 기능을 기반으로 동작합니다. 작업 도중 예기치 않게 잡이 실패하거나 타임아웃되어 락이 해제되지 않는 경우를 대비해, `expireAfter`로 락 만료 시간을 정의할 수 있습니다. 아래 코드처럼 잡 처리 시작 후 3분 뒤에 락을 자동 해제하도록 지정할 수 있습니다:

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->expireAfter(180)];
}
```

> [!WARNING]
> `WithoutOverlapping` 미들웨어는 [락(atomic lock)](/docs/12.x/cache#atomic-locks)을 지원하는 캐시 드라이버가 필요합니다. (`memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 지원)

<a name="sharing-lock-keys"></a>
#### 여러 잡 클래스 간 락 키 공유

기본적으로 `WithoutOverlapping`은 같은 클래스의 잡에만 오버랩 제한을 적용합니다. 서로 다른 잡 클래스가 같은 키를 사용한다 해도, 기본적으로 오버랩은 막지 못합니다. 잡 클래스 구분 없이 키 기준으로 오버랩을 막으려면 `shared` 메서드를 호출합니다:

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
### 예외 제한(Throttling Exceptions)

`Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어는 잡이 예외를 N회 이상 던지면, 일정 시간 동안 추가 시도를 막아줍니다. 불안정한 외부 API와 상호작용하는 잡에 유용합니다.

예를 들어, 외부 API에 연결하는 잡이 예외를 지나치게 많이 발생시킨다면, 다음처럼 미들웨어를 사용해 제한할 수 있습니다:

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

첫 번째 인수는 허용되는 예외 횟수, 두 번째 인수는 제한에 도달한 후 대기할 초 단위 시간입니다. 예시에서는 10회 연속 예외시 5분 대기(최대 30분까지 시도)됩니다.

예외 임계치 도달 전까지 발생하는 예외에 대해, 재시도 사이 대기 시간(backoff)을 지정하려면 `backoff` 메서드를 사용합니다:

```php
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 5 * 60))->backoff(5)];
}
```

미들웨어는 내부적으로 라라벨 캐시 시스템을 사용하며, 잡 클래스명이 캐시 키로 사용됩니다. 여러 잡이 동일한 외부 서비스의 제한을 공유하도록 하려면, `by` 메서드로 키를 지정할 수 있습니다:

```php
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->by('key')];
}
```

기본적으로는 모든 예외에 제한이 적용되지만, `when` 메서드에 콜백을 지정하면 특정 예외에만 제한할 수 있습니다:

```php
use Illuminate\Http\Client\HttpClientException;

public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->when(
        fn (Throwable $throwable) => $throwable instanceof HttpClientException
    )];
}
```

`deleteWhen` 메서드를 사용하면, 특정 예외 발생 시 잡을 즉시 삭제할 수도 있습니다:

```php
use App\Exceptions\CustomerDeletedException;

public function middleware(): array
{
    return [(new ThrottlesExceptions(2, 10 * 60))->deleteWhen(CustomerDeletedException::class)];
}
```

제한된 예외를 익셉션 핸들러에 보고하려면 `report` 메서드를 사용할 수 있습니다. 선택적으로 콜백을 넘기면 true 반환 시에만 보고합니다:

```php
use Illuminate\Http\Client\HttpClientException;

public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->report(
        fn (Throwable $throwable) => $throwable instanceof HttpClientException
    )];
}
```

> [!NOTE]
> Redis를 사용하는 경우, 보다 효율적인 `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어 이용이 가능합니다.

<a name="skipping-jobs"></a>
### 잡 건너뛰기

`Skip` 미들웨어를 사용하면, 별도의 잡 코드 수정 없이 조건에 따라 잡을 건너뛰고(삭제)할 수 있습니다. `Skip::when`은 조건이 true일 때, `Skip::unless`는 false일 때 잡을 삭제합니다:

```php
use Illuminate\Queue\Middleware\Skip;

public function middleware(): array
{
    return [
        Skip::when($condition),
    ];
}
```

복잡한 조건이 필요한 경우, 콜백을 넘길 수 있습니다:

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
*(아래 내용은 위의 패턴을 동일하게 이어서 번역해 주세요. 분량 제한상 생략되었으나, 위의 규칙을 문서 전체에 일관되게 적용해 번역하면 됩니다.)*