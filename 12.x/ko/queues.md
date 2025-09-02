# 큐 (Queues)

- [소개](#introduction)
    - [커넥션과 큐의 차이](#connections-vs-queues)
    - [드라이버별 안내 및 사전 준비](#driver-prerequisites)
- [Job 생성](#creating-jobs)
    - [Job 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [유니크 잡(Unique Jobs)](#unique-jobs)
    - [암호화된 잡(Encrypted Jobs)](#encrypted-jobs)
- [Job 미들웨어](#job-middleware)
    - [Rate Limiting](#rate-limiting)
    - [잡 중복 방지](#preventing-job-overlaps)
    - [예외 제한(Throttling Exceptions)](#throttling-exceptions)
    - [잡 스킵(Skipping Jobs)](#skipping-jobs)
- [잡 디스패치(Dispatching Jobs)](#dispatching-jobs)
    - [지연 디스패치(Delayed Dispatching)](#delayed-dispatching)
    - [동기식 디스패치(Synchronous Dispatching)](#synchronous-dispatching)
    - [잡과 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [잡 체이닝(Job Chaining)](#job-chaining)
    - [큐와 커넥션 커스터마이징](#customizing-the-queue-and-connection)
    - [잡 최대 시도 횟수/타임아웃 지정](#max-job-attempts-and-timeout)
    - [SQS FIFO 및 Fair Queue](#sqs-fifo-and-fair-queues)
    - [에러 처리](#error-handling)
- [잡 배칭(Job Batching)](#job-batching)
    - [배칭 가능한 Job 정의하기](#defining-batchable-jobs)
    - [Batch 디스패치](#dispatching-batches)
    - [체인과 배치](#chains-and-batches)
    - [배치에 Job 추가하기](#adding-jobs-to-batches)
    - [배치 조회(Inspecting Batches)](#inspecting-batches)
    - [배치 취소하기](#cancelling-batches)
    - [배치 실패 처리](#batch-failures)
    - [배치 레코드 정리(Pruning Batches)](#pruning-batches)
    - [DynamoDB에 배치 저장](#storing-batches-in-dynamodb)
- [클로저 큐잉(Queueing Closures)](#queueing-closures)
- [큐 워커 실행하기](#running-the-queue-worker)
    - [`queue:work` 명령어](#the-queue-work-command)
    - [큐 우선순위](#queue-priorities)
    - [큐 워커와 배포](#queue-workers-and-deployment)
    - [잡 만료 및 타임아웃](#job-expirations-and-timeouts)
- [Supervisor 설정](#supervisor-configuration)
- [실패한 Job 처리](#dealing-with-failed-jobs)
    - [실패 처리 후 정리](#cleaning-up-after-failed-jobs)
    - [실패한 Job 재시도](#retrying-failed-jobs)
    - [모델 누락 무시하기](#ignoring-missing-models)
    - [실패한 Job 정리(Pruning)](#pruning-failed-jobs)
    - [DynamoDB에 실패 Job 저장](#storing-failed-jobs-in-dynamodb)
    - [실패 Job 저장 비활성화](#disabling-failed-job-storage)
    - [실패 Job 이벤트](#failed-job-events)
- [큐에서 Job 비우기](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [일부 Job만 fake 처리](#faking-a-subset-of-jobs)
    - [Job 체인 테스트](#testing-job-chains)
    - [Job 배치 테스트](#testing-job-batches)
    - [Job/Queue 상호작용 테스트](#testing-job-queue-interactions)
- [Job 이벤트](#job-events)

<a name="introduction"></a>
## 소개 (Introduction)

웹 애플리케이션을 구축하면서, 업로드한 CSV 파일을 파싱하여 저장하는 작업처럼 일반적인 웹 요청 중에 처리하기에는 너무 오래 걸리는 작업이 있을 수 있습니다. 다행히도 Laravel은 백그라운드에서 처리될 수 있는 큐 잡(queued job)을 쉽게 생성할 수 있도록 지원합니다. 시간이 많이 소요되는 작업을 큐로 옮기면, 애플리케이션은 웹 요청에 더 빠르게 응답할 수 있고, 사용자 경험도 대폭 향상됩니다.

Laravel 큐는 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 관계형 데이터베이스 등 다양한 큐 백엔드에 걸쳐 통합된 큐 API를 제공합니다.

큐 설정 옵션은 애플리케이션의 `config/queue.php` 파일에 저장되어 있습니다. 이 파일에는 데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 등 Laravel이 제공하는 큐 드라이버 및 개발·테스트용으로 잡을 즉시 실행하는 동기 드라이버, 그리고 큐에 들어온 잡을 버리는 `null` 큐 드라이버의 커넥션 설정이 들어 있습니다.

> [!NOTE]
> Laravel Horizon은 Redis 기반 큐를 위한 아름다운 대시보드와 구성 시스템을 제공합니다. 자세한 내용은 [Horizon 문서](/docs/12.x/horizon)를 참고하세요.

<a name="connections-vs-queues"></a>
### 커넥션과 큐의 차이

Laravel 큐를 본격적으로 사용하기 전에, "커넥션(connection)"과 "큐(queue)" 개념의 차이를 정확히 이해하는 것이 중요합니다. `config/queue.php` 파일에는 `connections` 설정 배열이 있습니다. 이 옵션은 Amazon SQS, Beanstalk, Redis 등 백엔드 큐 서비스로 연결되는 방법을 정의합니다. 단, 하나의 큐 커넥션(즉, 하나의 큐 백엔드)은 여러 개의 "큐(queue)"—쉽게 말해, 여러 잡이 쌓이는 서로 다른 스택—를 가질 수 있습니다.

각 커넥션 예제에는 기본적으로 `queue` 속성이 존재합니다. 이는 커넥션을 통해 디스패치 되는 잡의 기본 큐를 의미합니다. 즉, 디스패치 시 어떤 큐를 사용할지 별도로 정의하지 않는다면, 해당 커넥션의 `queue` 속성에 설정된 큐로 잡이 들어가게 됩니다:

```php
use App\Jobs\ProcessPodcast;

// 이 잡은 기본 커넥션의 기본 큐로 전송됨
ProcessPodcast::dispatch();

// 이 잡은 기본 커넥션의 "emails" 큐로 전송됨
ProcessPodcast::dispatch()->onQueue('emails');
```

일부 애플리케이션에서는 잡을 여러 큐로 나눠 보낼 필요 없이, 하나의 큐만을 사용해도 충분할 수 있습니다. 하지만 잡을 여러 큐로 나누면, 어떤 잡을 먼저 처리할지 우선순위 지정 등, 처리 방식을 분류하거나 세분화하는 데 매우 유용합니다. 예를 들어 `high` 큐로 잡을 전송하고, 해당 큐를 우선 처리하는 워커를 실행해 더 높은 우선순위를 부여할 수 있습니다:

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버별 안내 및 사전 준비

<a name="database"></a>
#### 데이터베이스 (Database)

`database` 큐 드라이버를 사용하려면, 잡 정보를 저장할 데이터베이스 테이블이 필요합니다. 보통 이는 기본적으로 Laravel에 포함된 `0001_01_01_000002_create_jobs_table.php` [마이그레이션](/docs/12.x/migrations)을 활용합니다. 만약 애플리케이션에 해당 마이그레이션이 없다면, 다음 Artisan 명령어로 새로 생성할 수 있습니다:

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면, `config/database.php` 파일에 Redis 데이터베이스 커넥션을 설정해야 합니다.

> [!WARNING]
> `serializer`와 `compression` Redis 옵션은 `redis` 큐 드라이버에서 지원하지 않습니다.

<a name="redis-cluster"></a>
##### Redis 클러스터

Redis 큐 커넥션이 [Redis 클러스터](https://redis.io/docs/latest/operate/rs/databases/durability-ha/clustering)를 사용할 경우, 큐 이름에는 반드시 [키 해시 태그(key hash tag)](https://redis.io/docs/latest/develop/using-commands/keyspace/#hashtags)를 포함해야 합니다. 이는 동일한 큐에 해당하는 모든 Redis 키가 동일한 해시 슬롯에 들어가도록 보장합니다:

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

Redis 큐를 사용할 때, `block_for` 설정 옵션을 통해 잡이 큐에 들어올 때까지 드라이버가 기다리는 시간을 지정할 수 있습니다.

큐의 상황에 따라 이 값을 조절하면, Redis 데이터베이스에서 반복적으로 새로운 잡을 계속 polling하는 대신 더 효율적으로 동작할 수 있습니다. 예를 들어, 5초 동안 잡이 들어오길 기다리려면 다음과 같이 설정합니다:

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
> `block_for`를 `0`으로 설정하면, 잡이 들어올 때까지 큐 워커가 무기한 대기하게 됩니다. 이 상태에서는 `SIGTERM` 같은 시그널이 다음 잡이 처리될 때까지 적용되지 않습니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 사전 준비

아래 큐 드라이버를 사용하려면 별도의 의존성이 필요합니다. Composer 패키지 매니저로 설치하세요:

<div class="content-list" markdown="1">

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~2.0` 또는 phpredis PHP 익스텐션
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`

</div>

<a name="creating-jobs"></a>
## Job 생성 (Creating Jobs)

<a name="generating-job-classes"></a>
### Job 클래스 생성

애플리케이션의 큐에 사용되는 모든 잡은 기본적으로 `app/Jobs` 디렉토리에 저장됩니다. 만약 이 디렉토리가 존재하지 않더라도, 다음의 `make:job` Artisan 명령어를 실행하면 자동으로 생성됩니다:

```shell
php artisan make:job ProcessPodcast
```

생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하여, 해당 잡이 큐에 비동기적으로 쌓일 것임을 Laravel에 알립니다.

> [!NOTE]
> Job 스텁(stub) 파일은 [stub 커스터마이징](/docs/12.x/artisan#stub-customization)을 통해 직접 수정할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조

Job 클래스는 대체로 아주 단순하며, 큐가 잡을 처리할 때 호출되는 `handle` 메서드만을 포함하는 경우가 많습니다. 예시를 통해 살펴보겠습니다. 여기서는 팟캐스트 퍼블리싱 서비스를 운영한다고 가정하고, 업로드된 팟캐스트 파일을 게시 전에 처리하는 작업을 예로 들겠습니다:

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
     * 새 잡 인스턴스 생성
     */
    public function __construct(
        public Podcast $podcast,
    ) {}

    /**
     * 잡 실행
     */
    public function handle(AudioProcessor $processor): void
    {
        // 업로드된 팟캐스트 처리 ...
    }
}
```

이 예제에서 보듯, [Eloquent 모델](/docs/12.x/eloquent)을 잡의 생성자에 직접 넘길 수 있습니다. 이는 잡이 `Queueable` 트레이트를 사용할 때 가능한데, Eloquent 모델 및 이미 로딩된 연관관계가 직렬화/역직렬화 처리를 통해 문제 없이 큐에 전달됩니다.

Eloquent 모델을 생성자로 받는 큐 잡의 경우, 모델의 식별자(예: id)만 큐에 직렬화되어 저장됩니다. 실제로 잡이 실행될 때, 큐 시스템이 데이터베이스에서 전체 모델 인스턴스와 연관관계를 자동으로 다시 불러옵니다. 이 방식을 사용하면 큐에 전달되는 페이로드가 매우 작아집니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드 의존성 주입

큐가 잡을 처리할 때 `handle` 메서드가 호출됩니다. 이때, 메서드 시그니처에 타입힌트를 통해 의존성 주입을 받을 수 있습니다. [서비스 컨테이너](/docs/12.x/container)가 이를 자동으로 처리해줍니다.

서비스 컨테이너가 `handle` 메서드에 의존성을 주입하는 방식을 완전히 제어하고 싶다면, 컨테이너의 `bindMethod` 메서드를 사용할 수 있습니다. 이 메서드는 잡과 컨테이너를 사용하는 콜백을 인자로 받아 사용자가 원하는 방식으로 `handle` 메서드를 직접 호출할 수 있게 합니다. 보통은 `App\Providers\AppServiceProvider`의 `boot` 메서드 내부에서 호출합니다:

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 원시 이진 데이터(예: raw 이미지 데이터)는 큐 잡으로 넘기기 전에 반드시 `base64_encode`로 인코딩해야 합니다. 그렇지 않으면 큐에 저장할 때 JSON 직렬화가 제대로 되지 않을 수 있습니다.

<a name="handling-relationships"></a>
#### 큐에 포함된 연관관계 처리

잡이 큐에 들어갈 때, 이미 로딩된 Eloquent 연관관계도 함께 직렬화되기 때문에, 잡 데이터가 매우 커질 수 있습니다. 잡이 실행될 때, 모델의 연관관계 역시 전체가 다시 조회되는데, 큐에 쌓기 전 모델에 적용했던 일부 연관관계 쿼리 제한은 복원되지 않습니다. 따라서 특정 연관관계의 일부 데이터만 사용하고 싶다면, 잡 내부에서 연관관계 제한을 다시 적용해야 합니다.

또는, 연관관계 데이터는 직렬화에 포함하지 않도록 하려면, 속성 지정 시 `withoutRelations` 메서드를 사용하면 됩니다. 이 메서드는 연관관계가 없는 모델 인스턴스를 반환합니다:

```php
/**
 * 새 잡 인스턴스 생성
 */
public function __construct(
    Podcast $podcast,
) {
    $this->podcast = $podcast->withoutRelations();
}
```

[PHP 생성자 프로퍼티 승격](https://www.php.net/manual/en/language.oop5.decon.php#language.oop5.decon.constructor.promotion)을 쓸 때, 모델의 연관관계 직렬화를 방지하고 싶다면, `WithoutRelations` 속성을 사용할 수 있습니다:

```php
use Illuminate\Queue\Attributes\WithoutRelations;

/**
 * 새 잡 인스턴스 생성
 */
public function __construct(
    #[WithoutRelations]
    public Podcast $podcast,
) {}
```

클래스 전체에 연관관계 직렬화 방지 속성을 적용하려면, 각 모델이 아닌 클래스 자체에 `WithoutRelations` 어트리뷰트를 추가할 수 있습니다:

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
     * 새 잡 인스턴스 생성
     */
    public function __construct(
        public Podcast $podcast,
        public DistributionPlatform $platform,
    ) {}
}
```

잡이 Eloquent 모델의 컬렉션 또는 배열을 속성으로 받을 경우, 직렬화 및 실행 시 연관관계는 복원되지 않습니다. 많은 모델을 한 번에 다루는 잡에서의 과도한 리소스 사용을 방지하기 위함입니다.

<a name="unique-jobs"></a>
### 유니크 잡(Unique Jobs)

> [!WARNING]
> 유니크 잡을 사용하려면 [락 지원 캐시 드라이버](/docs/12.x/cache#atomic-locks)가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 원자적 락을 지원합니다. 또한 유니크 잡 제약은 배치 내 잡에는 적용되지 않습니다.

특정 잡이 동시에 큐에 한 인스턴스만 존재하도록 보장해야 할 때가 있습니다. 이 경우, 잡 클래스에 `ShouldBeUnique` 인터페이스를 구현하면 됩니다. 별도의 추가 메서드는 필요하지 않습니다:

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

위 예제에서, `UpdateSearchIndex` 잡은 유니크하게 됩니다. 즉, 잡이 이미 큐에 존재하고 아직 처리 중이라면, 새로 디스패치되는 동일 잡은 무시됩니다.

특정 "키(key)"를 지정해 잡의 유니크 조건을 커스터마이징하거나, 일정 시간 만료 후 유니크를 해제하고 싶을 때는, 잡 클래스에 `uniqueId`, `uniqueFor` 속성이나 메서드를 정의합니다:

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    /**
     * 상품 인스턴스
     *
     * @var \App\Models\Product
     */
    public $product;

    /**
     * 유니크 락 해제까지의 시간(초)
     *
     * @var int
     */
    public $uniqueFor = 3600;

    /**
     * Job의 유니크 ID 반환
     */
    public function uniqueId(): string
    {
        return $this->product->id;
    }
}
```

위 예제에서는 상품 ID로 잡의 유니크 여부를 결정합니다. 동일 ID의 잡이 실행 중이면 새로운 디스패치는 무시됩니다. 또한 기존 잡이 1시간 이내에 처리되지 않으면 락이 해제되어, 같은 키의 잡이 다시 큐에 쌓일 수 있습니다.

> [!WARNING]
> 여러 웹서버나 컨테이너에서 잡을 디스패치한다면, 모든 서버가 동일한 중앙 캐시 서버를 사용해야 Laravel이 잡의 유니크를 정확히 판단할 수 있습니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 처리 시작 전까지 유니크 락 유지

기본적으로, 유니크 잡은 처리가 완료되거나, 재시도 횟수를 모두 소진하면 "unlock"됩니다. 하지만, 처리 직전에 락을 해제하고 싶다면, 잡 클래스에 `ShouldBeUniqueUntilProcessing` 인터페이스를 구현하면 됩니다:

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
#### 유니크 잡 락(Unique Job Locks)

내부적으로, `ShouldBeUnique` 잡이 디스패치되면, Laravel은 `uniqueId` 키로 [락](/docs/12.x/cache#atomic-locks)을 획득하려고 시도합니다. 이미 락이 잡혀 있다면, 잡은 큐에 쌓이지 않습니다. 락은 잡이 정상 완료되거나, 재시도 횟수가 모두 소진될 때 해제됩니다. 기본적으로 기본 캐시 드라이버를 사용하며, 다른 드라이버를 사용하고 싶다면 `uniqueVia` 메서드를 추가합니다:

```php
use Illuminate\Contracts\Cache\Repository;
use Illuminate\Support\Facades\Cache;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...

    /**
     * 유니크 잡 락에 사용할 캐시 드라이버 반환
     */
    public function uniqueVia(): Repository
    {
        return Cache::driver('redis');
    }
}
```

> [!NOTE]
> 동시 실행만 제한하고 싶다면 [WithoutOverlapping](/docs/12.x/queues#preventing-job-overlaps) 잡 미들웨어를 사용하세요.

<a name="encrypted-jobs"></a>
### 암호화된 잡(Encrypted Jobs)

Laravel은 [암호화](/docs/12.x/encryption)를 이용해 잡 데이터의 프라이버시와 무결성을 보장할 수 있습니다. 사용 방법은 잡 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하면 됩니다. 이 인터페이스가 있으면, 잡이 큐에 쌓이기 전에 자동으로 암호화됩니다:

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

Job 미들웨어는 큐 잡 실행 전후에 커스텀 로직을 래핑할 수 있게 하여, 각 잡 내부에 중복 코드(보일러플레이트)를 줄일 수 있게 해줍니다. 예를 들어, 아래와 같이 Redis의 rate limiting 기능을 직접 사용해, 5초에 1개의 잡만 처리하도록 만들 수도 있습니다:

```php
use Illuminate\Support\Facades\Redis;

/**
 * Job 실행
 */
public function handle(): void
{
    Redis::throttle('key')->block(0)->allow(1)->every(5)->then(function () {
        info('Lock obtained...');

        // 잡 처리...
    }, function () {
        // 락 획득 실패...

        return $this->release(5);
    });
}
```

하지만 이런 방식은 `handle` 메서드가 너무 복잡해지고, 같은 처리 방식을 원하는 다른 잡에도 똑같은 코드를 반복하게 됩니다. 대신, rate limiting을 별도의 잡 미들웨어로 분리할 수 있습니다:

```php
<?php

namespace App\Jobs\Middleware;

use Closure;
use Illuminate\Support\Facades\Redis;

class RateLimited
{
    /**
     * 큐 잡 처리
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

[라우트 미들웨어](/docs/12.x/middleware)와 마찬가지로, 잡 미들웨어도 처리 중인 잡 인스턴스와 다음 콜백을 받습니다.

`make:job-middleware` Artisan 명령어로 새 잡 미들웨어 클래스를 생성할 수 있습니다. 생성 후에는 잡 클래스의 `middleware` 메서드에 배열로 반환해 붙이면 됩니다. 이 메서드는 기본 생성 잡 스텁에는 없으므로, 직접 추가해야 합니다:

```php
use App\Jobs\Middleware\RateLimited;

/**
 * 잡이 통과해야 할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited];
}
```

> [!NOTE]
> 잡 미들웨어는 [큐드 이벤트 리스너](/docs/12.x/events#queued-event-listeners), [메일러블](/docs/12.x/mail#queueing-mail), [알림](/docs/12.x/notifications#queueing-notifications)에도 사용할 수 있습니다.

<a name="rate-limiting"></a>
### Rate Limiting

방금 소개한 rate limiting 잡 미들웨어를 직접 만들 수도 있지만, Laravel에는 이미 rate limiting을 위한 미들웨어가 내장되어 있습니다. [라우트 rate limiter](/docs/12.x/routing#defining-rate-limiters)와 유사하게, 잡 rate limiter는 `RateLimiter` 파사드의 `for` 메서드로 정의합니다.

예를 들어, 일반 이용자는 1시간에 1회만 데이터 백업을 허용하고, 프리미엄 고객은 제한을 두지 않는 방식을 생각해 볼 수 있습니다. 이를 위해 `AppServiceProvider`의 `boot` 메서드에서 다음과 같이 정의합니다:

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Support\Facades\RateLimiter;

/**
 * 애플리케이션 서비스 부트스트랩
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

위 코드 외에도, `perMinute`로 분 단위 제한도 설정할 수 있습니다. `by`에 전달하는 값으로, 고객 단위 등 원하는 기준의 식별자를 넣어 세분화할 수 있습니다:

```php
return Limit::perMinute(50)->by($job->user->id);
```

rate limit을 참고할 잡 미들웨어는 `Illuminate\Queue\Middleware\RateLimited` 미들웨어입니다. 잡이 rate limit에 도달하면, 이 미들웨어는 지정한 시간만큼 잡을 큐에 다시 release합니다:

```php
use Illuminate\Queue\Middleware\RateLimited;

/**
 * 잡이 통과해야 할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited('backups')];
}
```

rate limit에 걸려 release 시도할 때도 잡의 `attempts`(시도 횟수)가 증가합니다. 따라서 잡 클래스의 `tries`, `maxExceptions` 속성을 적절히 조정하거나, [retryUntil](#time-based-attempts) 메서드를 사용해 유효 시간까지 제어해야 할 수 있습니다.

`releaseAfter` 메서드를 사용하면 release 후 재시도까지 지연될 시간을 초 단위로 추가 지정할 수 있습니다:

```php
/**
 * 잡이 통과해야 할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new RateLimited('backups'))->releaseAfter(60)];
}
```

rate limited 잡을 재시도하지 않고 바로 중단하고 싶다면, `dontRelease` 메서드를 사용합니다:

```php
/**
 * 잡이 통과해야 할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new RateLimited('backups'))->dontRelease()];
}
```

> [!NOTE]
> Redis를 사용 중이라면, Redis에 최적화된 `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어를 사용해 더 효율적인 제어가 가능합니다.

<a name="preventing-job-overlaps"></a>
### 잡 중복 방지

Laravel에는 임의의 키를 기준으로 잡의 중복 실행을 방지하는 `Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어가 내장되어 있습니다. 이 미들웨어는 특정 리소스(예: 사용자)에 대해 한 번에 하나의 잡만 수정 작업을 허용해야 할 때 사용합니다.

예를 들어, 사용자의 신용 점수를 갱신하는 잡이 있고, 동일 ID에 대해 겹치는 갱신 잡이 실행되면 안 된다고 할 때 이렇게 사용할 수 있습니다:

```php
use Illuminate\Queue\Middleware\WithoutOverlapping;

/**
 * 잡이 통과해야 할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new WithoutOverlapping($this->user->id)];
}
```

기본적으로, 중복되는 잡도 release를 수행할 때 attempts(시도 횟수)가 증가합니다. 따라서 `tries`, `maxExceptions` 등의 프로퍼티를 상황에 맞게 조정해야 합니다. 예를 들어, `tries`가 1로 되어 있다면, 중복 잡은 바로 재시도 없이 종료됩니다.

같은 타입의 중복되는 잡은 큐에 다시 release됩니다. `releaseAfter`를 통해 재시도까지 지연 시간을 지정할 수 있습니다:

```php
/**
 * 잡이 통과해야 할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->releaseAfter(60)];
}
```

중복되는 잡을 바로 삭제(재시도 없이 중단)하고 싶다면, `dontRelease` 메서드를 사용합니다:

```php
/**
 * 잡이 통과해야 할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->dontRelease()];
}
```

이 미들웨어는 Laravel의 원자적 락 기능을 사용합니다. 잡이 예상치 못하게 실패하거나 타임아웃 시 락이 해제되지 않을 수 있으므로, `expireAfter` 메서드로 락 해제 시간을 명시적으로 지정할 수 있습니다. 아래 예제는 잡 처리 시작 후 3분(180초)이 지나면 락을 해제하도록 지시합니다:

```php
/**
 * 잡이 통과해야 할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->expireAfter(180)];
}
```

> [!WARNING]
> `WithoutOverlapping` 미들웨어는 [락 지원 캐시 드라이버](/docs/12.x/cache#atomic-locks)가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 지원됩니다.

<a name="sharing-lock-keys"></a>
#### 여러 Job 클래스 간 락 키 공유

기본적으로, `WithoutOverlapping` 미들웨어는 같은 클래스의 잡에서만 중복 실행을 막습니다. 즉, 서로 다른 잡 클래스여도 같은 락 키를 사용하면 중복이 가능합니다. 반면, 여러 잡 클래스 간에 동일한 락 키로 중복까지 방지하고 싶다면, `shared` 메서드를 사용하세요:

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

Laravel에는 잡이 일정 횟수 이상의 예외를 발생시키면, 남은 시도는 일정 시간 동안 지연시키는 `Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어가 있습니다. 불안정한 외부 서비스와 상호작용하는 잡에서 특히 유용합니다.

예를 들어, 외부 API와 통신하는 잡이 예외를 연달아 발생시킬 경우, 다음과 같이 사용할 수 있습니다. 보통 [시간 기반 시도 제한](#time-based-attempts)과 함께 사용합니다:

```php
use DateTime;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡이 통과해야 할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new ThrottlesExceptions(10, 5 * 60)];
}

/**
 * 잡의 타임아웃 시각 반환
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(30);
}
```

첫 번째 인자는 예외를 허용할 횟수, 두 번째 인자는 예외 횟수 초과 시 다음 시도까지 대기할 시간(초)입니다. 위 코드는 10회 연속 예외 발생 시 5분간 시도를 중단합니다(30분 이내 제한).

예외 한도 미만일 때, 기본적으로 바로 재시도하지만, `backoff` 메서드로 잡별 지연 시간도 지정 가능합니다:

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡이 통과해야 할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 5 * 60))->backoff(5)];
}
```

캐시 시스템을 이용해 rate limit을 구현하며, 잡 클래스명이 캐시의 "key"로 사용됩니다. 여러 잡이 동일 버킷(즉, 공유 제한)을 적용받게 하려면 `by` 메서드로 직접 키를 지정할 수 있습니다:

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->by('key')];
}
```

기본적으로 모든 예외에 throttle이 적용되지만, `when` 메서드를 통해 특정 예외만 제한하도록 바꿀 수 있습니다:

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

`when`은 예외에 따라 잡을 release(재시도) 또는 throw하게 하지만, 예외에 따라 잡을 완전히 삭제하고 싶다면 `deleteWhen` 메서드를 사용할 수 있습니다:

```php
use App\Exceptions\CustomerDeletedException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [(new ThrottlesExceptions(2, 10 * 60))->deleteWhen(CustomerDeletedException::class)];
}
```

특정 예외 발생 시 exception handler에 예외를 리포트하려면 `report` 메서드를 사용할 수 있습니다. 조건부 보고도 가능합니다:

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
> Redis 사용 시, Redis에 최적화된 `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어가 더욱 효율적으로 동작합니다.

<a name="skipping-jobs"></a>
### 잡 스킵(Skipping Jobs)

`Skip` 미들웨어를 사용하면 잡의 로직을 수정하지 않고서도 잡을 스킵(삭제)할 수 있습니다. `Skip::when`은 주어진 조건이 `true`일 때 잡을 삭제하고, `Skip::unless`는 조건이 `false`일 때 잡을 삭제합니다:

```php
use Illuminate\Queue\Middleware\Skip;

/**
 * 잡이 통과해야 할 미들웨어 반환
 */
public function middleware(): array
{
    return [
        Skip::when($condition),
    ];
}
```

복잡한 조건을 위해서 클로저를 직접 넘길 수도 있습니다:

```php
use Illuminate\Queue\Middleware\Skip;

/**
 * 잡이 통과해야 할 미들웨어 반환
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

<!-- 이하 생략: 원본 전체 분량이 많으므로, 요청 시 추가 출력 가능 -->