# 큐 (Queues)

- [소개](#introduction)
    - [커넥션 vs. 큐](#connections-vs-queues)
    - [드라이버 참고사항 및 필수 조건](#driver-prerequisites)
- [잡 생성](#creating-jobs)
    - [잡 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [유일 잡](#unique-jobs)
    - [암호화된 잡](#encrypted-jobs)
- [잡 미들웨어](#job-middleware)
    - [속도 제한](#rate-limiting)
    - [잡 중복 실행 방지](#preventing-job-overlaps)
    - [예외 제한(Throttle)](#throttling-exceptions)
    - [잡 건너뛰기](#skipping-jobs)
- [잡 디스패치](#dispatching-jobs)
    - [딜레이 디스패치](#delayed-dispatching)
    - [동기식 디스패치](#synchronous-dispatching)
    - [잡과 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [잡 체이닝](#job-chaining)
    - [큐 및 커넥션 커스터마이징](#customizing-the-queue-and-connection)
    - [최대 시도 횟수 / 타임아웃 지정](#max-job-attempts-and-timeout)
    - [SQS FIFO 및 공정한 큐](#sqs-fifo-and-fair-queues)
    - [큐 페일오버](#queue-failover)
    - [에러 핸들링](#error-handling)
- [잡 배치 처리](#job-batching)
    - [배치 가능한 잡 정의](#defining-batchable-jobs)
    - [배치 디스패치](#dispatching-batches)
    - [체인과 배치](#chains-and-batches)
    - [배치에 잡 추가](#adding-jobs-to-batches)
    - [배치 정보 조회](#inspecting-batches)
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
- [Supervisor 설정](#supervisor-configuration)
- [실패한 잡 처리](#dealing-with-failed-jobs)
    - [실패한 잡 정리](#cleaning-up-after-failed-jobs)
    - [실패한 잡 재시도](#retrying-failed-jobs)
    - [누락된 모델 무시](#ignoring-missing-models)
    - [실패한 잡 레코드 정리](#pruning-failed-jobs)
    - [DynamoDB에 실패한 잡 저장](#storing-failed-jobs-in-dynamodb)
    - [실패한 잡 저장 비활성화](#disabling-failed-job-storage)
    - [실패한 잡 이벤트](#failed-job-events)
- [큐에서 잡 삭제](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [일부 잡만 페이크 처리](#faking-a-subset-of-jobs)
    - [잡 체인 테스트](#testing-job-chains)
    - [잡 배치 테스트](#testing-job-batches)
    - [잡 / 큐 상호작용 테스트](#testing-job-queue-interactions)
- [잡 이벤트](#job-events)

<a name="introduction"></a>
## 소개 (Introduction)

웹 애플리케이션을 개발하다 보면 업로드된 CSV 파일을 파싱 및 저장하는 작업처럼 일반적인 웹 요청에서 처리하기에는 시간이 오래 걸리는 작업이 있을 수 있습니다. 다행히도, Laravel은 이러한 작업을 백그라운드에서 처리할 수 있도록 큐 잡을 쉽게 생성할 수 있게 지원합니다. 시간 소모가 큰 작업들을 큐로 이동시키면, 애플리케이션이 웹 요청에 훨씬 빠르게 응답할 수 있어 사용자 경험을 크게 향상시킬 수 있습니다.

Laravel의 큐 시스템은 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 또는 관계형 데이터베이스와 같은 다양한 큐 백엔드를 아우르는 통합 API를 제공합니다.

Laravel의 큐 설정은 애플리케이션의 `config/queue.php` 설정 파일에 저장되어 있습니다. 이 파일에는 프레임워크에 포함된 각 큐 드라이버(데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 등)에 대한 커넥션 설정이 포함되어 있으며, 개발이나 테스트 시에 즉시 잡을 실행하는 동기식 드라이버 및 큐 잡을 버리는 `null` 드라이버도 제공됩니다.

> [!NOTE]
> Laravel Horizon은 Redis 기반 큐를 위한 아름다운 대시보드 및 설정 시스템입니다. 자세한 내용은 [Horizon 공식 문서](/docs/12.x/horizon)를 참고하세요.

<a name="connections-vs-queues"></a>
### 커넥션 vs. 큐

Laravel 큐를 사용하기 전에 "커넥션(connection)"과 "큐(queue)"의 차이를 이해하는 것이 중요합니다. `config/queue.php` 파일에는 `connections` 설정 배열이 있으며, 이는 Amazon SQS, Beanstalk, Redis 같은 백엔드 큐 서비스와 연결을 설정합니다. 하나의 큐 커넥션에는 여러 개의 "큐"가 있을 수 있으며, 각각은 큐에 쌓인 잡의 스택 또는 더미로 생각할 수 있습니다.

각 커넥션 설정 예제에는 `queue` 속성이 있습니다. 이 속성은 해당 커넥션에서 잡이 디스패치될 기본 큐를 가리킵니다. 즉, 특정 큐를 명시하지 않고 잡을 디스패치하면, 해당 커넥션 설정의 `queue` 속성에 정의된 큐에 잡이 쌓입니다:

```php
use App\Jobs\ProcessPodcast;

// 이 잡은 기본 커넥션의 기본 큐로 전송됩니다...
ProcessPodcast::dispatch();

// 이 잡은 기본 커넥션의 "emails" 큐로 전송됩니다...
ProcessPodcast::dispatch()->onQueue('emails');
```

어떤 애플리케이션은 굳이 여러 개의 큐를 사용할 필요 없이 하나의 간단한 큐만 사용할 수도 있습니다. 하지만, 잡을 여러 큐로 분리해두면, 처리 우선순위나 업무 분류 면에서 유용할 수 있습니다. Laravel의 큐 워커는 처리할 큐의 우선순위도 설정할 수 있기 때문입니다. 예를 들어, `high` 큐에 잡을 쌓아두고 해당 큐를 먼저 처리하도록 우선순위를 줄 수 있습니다:

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버 참고사항 및 필수 조건

<a name="database"></a>
#### 데이터베이스

`database` 큐 드라이버를 사용하려면 잡을 저장할 데이터베이스 테이블이 필요합니다. 보통 Laravel의 기본 `0001_01_01_000002_create_jobs_table.php` [마이그레이션](/docs/12.x/migrations)에 포함되어 있습니다. 만약 애플리케이션에 해당 마이그레이션이 없다면, `make:queue-table` Artisan 명령어로 생성할 수 있습니다:

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면, `config/database.php` 설정 파일에 Redis 데이터베이스 커넥션을 설정해야 합니다.

> [!WARNING]
> `redis` 큐 드라이버는 Redis의 `serializer` 및 `compression` 옵션을 지원하지 않습니다.

<a name="redis-cluster"></a>
##### Redis 클러스터

Redis 큐 커넥션이 [Redis Cluster](https://redis.io/docs/latest/operate/rs/databases/durability-ha/clustering)를 사용한다면, 큐 이름에 [key hash tag](https://redis.io/docs/latest/develop/using-commands/keyspace/#hashtags)가 포함되어야 합니다. 이는 동일한 큐의 Redis 키가 같은 해시 슬롯에 배치되도록 보장하기 위해서 필요합니다:

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

Redis 큐를 사용할 때, `block_for` 설정 옵션을 사용하면 드라이버가 잡이 대기열에 도착할 때까지 대기할 시간을 지정할 수 있습니다. 이 방법은 단순히 Redis에서 새 잡을 지속적으로 폴링하는 것보다 경우에 따라 더 효율적일 수 있습니다. 예를 들어, 값을 `5`로 설정하면 드라이버는 잡이 대기열에 도착할 때까지 5초 동안 블로킹됩니다:

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
> `block_for`를 `0`으로 설정하면 잡이 도착할 때까지 큐 워커가 무한정 블로킹됩니다. 이 경우, 다음 잡이 처리될 때까지 `SIGTERM`과 같은 신호는 처리되지 않습니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 필수 조건

아래 큐 드라이버에서는 각각의 의존 패키지가 필요합니다. Composer 패키지 매니저를 통해 설치할 수 있습니다:

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

애플리케이션의 모든 큐잉 가능한 잡은 기본적으로 `app/Jobs` 디렉터리에 저장됩니다. 해당 디렉터리가 없다면, `make:job` Artisan 명령어를 실행하면 디렉터리가 생성됩니다:

```shell
php artisan make:job ProcessPodcast
```

생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하며, 이로써 해당 잡이 큐에 비동기적으로 디스패치될 수 있도록 Laravel에 알립니다.

> [!NOTE]
> 잡 스텁은 [스텁 퍼블리싱](/docs/12.x/artisan#stub-customization)을 사용해 커스터마이즈할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조

잡 클래스는 매우 단순하며, 보통 큐에서 잡이 처리될 때 호출되는 `handle` 메서드만 포함되어 있습니다. 예시를 통해 살펴봅니다. 여기서는 팟캐스트 게시 서비스를 운영하며, 업로드된 팟캐스트 파일을 공개 전에 처리해야 한다고 가정합니다:

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

위 예시에서 볼 수 있듯, [Eloquent 모델](/docs/12.x/eloquent)를 큐잉된 잡 생성자에 직접 전달할 수 있습니다. 잡에서 사용하는 `Queueable` 트레잇 덕분에, Eloquent 모델과 이미 로드된 연관관계들도 직렬화 및 역직렬화가 안전하게 처리됩니다.

잡 생성자에 Eloquent 모델이 전달되는 경우, 모델의 식별자만 큐에 직렬화됩니다. 워커가 잡을 처리할 때 큐 시스템이 자동으로 데이터베이스에서 전체 모델 인스턴스와 로드된 연관관계를 다시 조회합니다. 이런 모델 직렬화 방식은 큐 드라이버로 보내는 잡 데이터의 용량을 대폭 줄여줍니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드 의존성 주입

큐 잡이 처리될 때 `handle` 메서드가 호출됩니다. `handle` 메서드에 DI(의존성 주입)를 적용할 수 있다는 점에 주목하세요. Laravel [서비스 컨테이너](/docs/12.x/container)가 이러한 의존성을 자동으로 주입해줍니다.

만약 컨테이너가 `handle` 메서드에 어떻게 인자를 주입할지 완전히 제어하고 싶다면, 컨테이너의 `bindMethod` 메서드를 사용할 수 있습니다. `bindMethod`는 잡 인스턴스와 컨테이너를 받아서 직접 적절히 `handle`을 호출하면 됩니다. 보통은 [서비스 프로바이더](/docs/12.x/providers)인 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 호출합니다:

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 이미지 원본 데이터와 같은 바이너리 데이터는 큐잉 잡으로 전달하기 전에 반드시 `base64_encode` 함수로 인코딩하세요. 그렇지 않으면 잡이 큐에 저장될 때 JSON 직렬화에 실패할 수 있습니다.

<a name="handling-relationships"></a>
#### 큐잉된 연관관계

큐에 잡을 올릴 때 Eloquent 모델의 모든 연관관계도 함께 직렬화됩니다. 이 때문에 잡의 직렬화 문자열이 꽤 커질 수 있습니다. 또한 잡이 역직렬화되고 모델 연관관계가 재조회될 때, 직렬화 전 적용됐던 쿼리 제약조건은 전혀 적용되지 않고 전체 연관 데이터가 조회됩니다. 따라서, 특정 연관관계의 일부만 다루고 싶다면, 큐잉된 잡 안에서 다시 제약조건을 설정해야 합니다.

연관관계 자체를 직렬화하지 않으려면, 모델의 값을 설정할 때 `withoutRelations` 메서드를 사용할 수 있습니다. 이 메서드는 연관관계가 없는 모델 인스턴스를 반환합니다:

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

[PHP 생성자 프로퍼티 승격](https://www.php.net/manual/en/language.oop5.decon.php#language.oop5.decon.constructor.promotion)을 사용하는 경우, Eloquent 모델의 연관관계를 직렬화하지 않으려면 `WithoutRelations` 속성을 사용할 수 있습니다:

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

모든 모델의 연관관계를 직렬화하지 않으려면 클래스 전체에 `WithoutRelations` 속성을 적용할 수도 있습니다:

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

잡이 단일 모델이 아닌 컬렉션이나 배열로 Eloquent 모델을 받는 경우, 해당 컬렉션 내의 모델들은 잡이 역직렬화되고 실행되더라도 연관관계가 복원되지 않습니다. 이는 많은 모델을 다루는 잡에서 과도한 자원 사용을 방지하기 위함입니다.

<a name="unique-jobs"></a>
### 유일 잡 (Unique Jobs)

> [!WARNING]
> 유일 잡은 [락 지원](/docs/12.x/cache#atomic-locks)이 가능한 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 아토믹 락을 지원합니다.

> [!WARNING]
> 유일 잡 제약은 배치에 속한 잡에는 적용되지 않습니다.

특정 잡이 한 번에 한 인스턴스만 큐에 존재해야 하는 상황이 있을 수 있습니다. 이를 위해 잡 클래스에 `ShouldBeUnique` 인터페이스를 구현하면 됩니다. 이 때 별도의 메서드 구현은 필요 없습니다:

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

위 예시에서처럼, `UpdateSearchIndex` 잡은 유일합니다. 이미 같은 잡이 큐에 있고 아직 처리가 끝나지 않았다면 새로운 잡은 디스패치되지 않습니다.

경우에 따라 잡의 유일성을 결정짓는 “키"를 직접 지정하거나, 얼마 동안만 유일하게 유지할지 타임아웃을 줄 수도 있습니다. 이를 위해 `uniqueId`, `uniqueFor` 속성이나 메서드를 정의할 수 있습니다:

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    /**
     * 상품 인스턴스.
     *
     * @var \App\Models\Product
     */
    public $product;

    /**
     * 잡의 유일 락이 해제되도록 유지할 시간(초).
     *
     * @var int
     */
    public $uniqueFor = 3600;

    /**
     * 잡의 고유 ID 반환.
     */
    public function uniqueId(): string
    {
        return $this->product->id;
    }
}
```

위 예시에서는 `UpdateSearchIndex` 잡이 상품 ID로 유일합니다. 즉, 이미 동일 상품 ID로 미처리 잡이 있다면 새 잡은 무시됩니다. 또, 기존 잡이 1시간 내에 처리되지 않으면 락이 해제되어 동일한 키로 잡을 다시 큐잉할 수 있습니다.

> [!WARNING]
> 여러 웹 서버나 컨테이너에서 잡을 디스패치한다면, 모든 서버가 동일한 중앙 캐시 서버를 사용하도록 하세요. 그래야 Laravel이 잡의 유일성을 정확히 판단할 수 있습니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 잡을 처리 시작 전까지 유일하게 유지하기

기본적으로 유일 잡의 락은 잡이 처리 완료되거나 모든 재시도 횟수가 실패할 때 풀립니다. 하지만, 잡을 처리하기 직전에 락을 해제하고 싶을 수도 있습니다. 이럴 때는 `ShouldBeUnique` 대신 `ShouldBeUniqueUntilProcessing` 인터페이스를 구현하면 됩니다:

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

실제로 `ShouldBeUnique` 잡이 디스패치되면 Laravel은 `uniqueId` 키로 [락](/docs/12.x/cache#atomic-locks)을 획득하려 시도합니다. 락이 이미 존재한다면 잡은 큐에 추가되지 않습니다. 이 락은 잡이 처리 완료될 때나 모든 재시도가 실패할 때 해제됩니다. 기본적으로 Laravel은 이 락을 얻기 위해 기본 캐시 드라이버를 사용합니다. 특정 드라이버를 사용하고싶다면, `uniqueVia` 메서드로 반환할 수 있습니다:

```php
use Illuminate\Contracts\Cache\Repository;
use Illuminate\Support\Facades\Cache;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...

    /**
     * 유일 잡 락에 사용할 캐시 드라이버 반환.
     */
    public function uniqueVia(): Repository
    {
        return Cache::driver('redis');
    }
}
```

> [!NOTE]
> 동시에 실행되는 잡 수에만 제한을 두고 싶다면, [WithoutOverlapping 잡 미들웨어](/docs/12.x/queues#preventing-job-overlaps)를 사용하세요.

<a name="encrypted-jobs"></a>
### 암호화된 잡 (Encrypted Jobs)

Laravel은 잡 데이터의 프라이버시와 무결성을 [암호화](/docs/12.x/encryption)로 보장할 수 있게 지원합니다. 시작하려면 잡 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하세요. 이렇게 하면 큐에 추가하는 순간 Laravel이 자동으로 잡 데이터를 암호화합니다:

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

잡 미들웨어를 사용하면 큐잉 잡 실행 전후에 커스텀 로직을 삽입할 수 있어, 잡 내부를 더 깔끔하게 만들 수 있습니다. 예를 들어, 아래 `handle` 메서드는 Laravel의 Redis 속도 제한 기능을 사용하여 5초마다 한 개의 잡만 처리하도록 구현한 예시입니다:

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

위 코드는 유효하지만, Redis 속도제한 로직이 잡 내부에 섞여 있어 복잡해지며, 비슷한 잡마다 이 로직을 중복 구현해야 합니다. 이런 중복을 방지하려면 속도제한 로직을 잡 미들웨어로 분리할 수 있습니다:

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

이처럼 [라우트 미들웨어](/docs/12.x/middleware)와 같이, 잡 미들웨어는 처리 대상 잡과, 처리 흐름을 계속 진행하는 콜백을 받습니다.

`make:job-middleware` Artisan 명령어로 새로운 잡 미들웨어 클래스를 생성할 수 있습니다. 생성 후 잡 클래스의 `middleware` 메서드에서 반환하면 미들웨어가 적용됩니다. (이 메서드는 `make:job` 명령어로 생성된 잡에는 기본적으로 존재하지 않으니 직접 추가해야 합니다):

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
> 잡 미들웨어는 [큐잉 이벤트 리스너](/docs/12.x/events#queued-event-listeners), [메일러블](/docs/12.x/mail#queueing-mail), [알림](/docs/12.x/notifications#queueing-notifications)에도 사용할 수 있습니다.

<a name="rate-limiting"></a>
### 속도 제한 (Rate Limiting)

직접 잡 미들웨어를 만들어 속도 제한을 구현할 수도 있지만, Laravel은 기본적으로 사용할 수 있는 속도 제한 미들웨어를 포함하고 있습니다. [라우트 속도 제한자](/docs/12.x/routing#defining-rate-limiters)와 마찬가지로, 잡 속도 제한자는 `RateLimiter` 파사드의 `for` 메서드를 사용해 정의합니다.

예를 들어, 일반 유저는 시간당 한 번씩만 백업 작업을 허용하고, 프리미엄 고객에게는 제한을 두지 않는 시나리오를 만들어보겠습니다. `AppServiceProvider`의 `boot` 메서드에서 `RateLimiter`를 정의합니다:

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

위 예시처럼 시간 단위로 제한할 수도 있고, `perMinute` 메서드를 써서 분 단위도 쉽게 설정할 수 있습니다. `by` 메서드에는 일반적으로 고객 식별자를 전달해 사용자 단위 제한을 만듭니다:

```php
return Limit::perMinute(50)->by($job->user->id);
```

속도 제한을 정의했다면, 잡 클래스의 미들웨어 배열에 `Illuminate\Queue\Middleware\RateLimited` 미들웨어를 추가합니다. 이 미들웨어는 제한을 초과하면, 제한 시간만큼 지연 후 잡을 다시 큐에 올립니다:

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

속도 제한으로 인해 잡이 다시 큐에 오르면, 이 역시 잡의 `attempts` 카운트가 올라갑니다. `tries`와 `maxExceptions` 속성값을 잘 조정하세요. 혹은 [retryUntil 메서드](#time-based-attempts)를 활용해 잡의 허용 시도 시간도 제어할 수 있습니다.

`releaseAfter` 메서드로, 새로 시도할 때까지 기다릴(지연) 초를 지정할 수 있습니다:

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

속도 제한으로 인한 재시도 대신, 잡을 아예 재시도하지 않으려면 `dontRelease`를 사용할 수 있습니다:

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
> Redis를 사용할 땐, 최적화된 `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어를 사용할 수 있습니다. 이는 기본 미들웨어보다 더 효율적입니다.

<a name="preventing-job-overlaps"></a>
### 잡 중복 실행 방지 (Preventing Job Overlaps)

Laravel은 `Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어를 제공하여, 임의의 키를 기준으로 잡 중복 실행을 방지할 수 있습니다. 이는 특정 리소스를 동시에 여러 잡이 수정해선 안 될 때 유용합니다.

예를 들어, 사용자 신용점수 업데이트 잡이 동일한 사용자 ID에 중복 실행되지 않도록 보호하려면 아래와 같이 미들웨어 배열에 추가하면 됩니다:

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

중복 잡이 다시 큐에 오르면 `attempts` 카운트가 오릅니다. 기본적으로 `tries`를 1로 두면 겹치는 잡은 재시도가 불가능해집니다. 필요에 따라 값을 조정하세요.

중복 잡을 곧바로 큐에 다시 올릴 수도 있고, `releaseAfter` 메서드를 써 지정된 시간만큼 기다린 뒤 재시도하도록 할 수도 있습니다:

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

겹치는 잡을 즉시 삭제해 재시도를 원치 않으면, `dontRelease` 메서드를 사용할 수 있습니다:

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

이 미들웨어는 Laravel의 아토믹 락 기능을 사용합니다. 예기치 않게 잡이 실패하거나 타임아웃으로 인해 락이 해제되지 않을 수 있으므로, `expireAfter`로 만료 시간(초)을 지정해 명시적으로 락 해제를 예약할 수 있습니다. 아래 예시에서는 잡 시작 후 3분 뒤에 락이 자동 해제됩니다:

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
> `WithoutOverlapping` 미들웨어는 [락 지원](/docs/12.x/cache#atomic-locks)이 가능한 캐시 드라이버가 필요합니다. `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 아토믹 락을 지원합니다.

<a name="sharing-lock-keys"></a>
#### 잡 클래스 간 락 키 공유

기본적으로 `WithoutOverlapping` 미들웨어는 동일 클래스의 중복 잡만 방지합니다. 그러나 서로 다른 잡 클래스가 같은 락 키를 사용하더라도 중복 처리가 방지되진 않습니다. 만약 여러 잡 클래스 간에 키를 공유해 중복 실행을 막고 싶다면, `shared` 메서드를 사용할 수 있습니다:

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
### 예외 제한(Throttle) (Throttling Exceptions)

Laravel은 `Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어를 제공하여, 잡에서 예외가 발생한 횟수를 제한하고 정해진 시간 동안 추가 실행을 지연시킬 수 있습니다. 이를 통해 불안정한 외부 서비스와 상호작용할 때 잡 실행을 보호할 수 있습니다.

예를 들어, 외부 API와 상호작용하는 잡이 연속적으로 예외를 던진다고 가정하면, 아래와 같이 미들웨어를 반환할 수 있습니다. 이 미들웨어는 [시간 기반 시도 제한](#time-based-attempts)과 함께 사용하면 좋습니다:

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

첫 번째 인자는 예외가 발생할 수 있는 최대 횟수, 두 번째 인자는 제한 후 얼마 동안 대기할지 초 단위로 지정합니다. 위 코드는 10번 연속 예외 발생 시 5분 후 재시도하며, 전체 제한은 30분입니다.

예외 발생 시 즉시 재시도하지 않고, 대기 시간을 추가하고 싶다면 `backoff` 메서드를 사용할 수 있습니다:

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

이 미들웨어는 내부적으로 Laravel의 캐시 시스템을 활용하며, 기본적으로 잡 클래스명이 캐시 키로 쓰입니다. 여러 잡이 동일 외부 서비스에 접속한다면, `by` 메서드로 공통 키를 설정해 제한을 공유할 수 있습니다:

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

기본적으로 모든 예외가 제한 대상이 되지만, `when` 메서드로 특정 조건에서만 제한을 걸도록 할 수 있습니다. 예외가 주어진 클로저 반환값이 `true`일 때만 제한합니다:

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

`when`과 달리, `deleteWhen`은 특정 예외 발생 시 잡을 즉시 완전히 삭제합니다:

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

제한 예외가 애플리케이션의 예외 핸들러에 보고되길 원하면, `report` 메서드를 사용하세요. 옵션으로 클로저를 전달해 조건부 보고도 가능합니다:

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
> Redis를 사용하는 경우, 최적화된 `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어를 사용할 수 있습니다.

<a name="skipping-jobs"></a>
### 잡 건너뛰기 (Skipping Jobs)

`Skip` 미들웨어를 사용하면 잡 논리를 수정하지 않고도 잡을 건너뛰거나 삭제할 수 있습니다. `Skip::when` 메서드는 조건이 `true`일 때 잡을 삭제하고, `Skip::unless`는 `false`일 때 삭제합니다:

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

`when`이나 `unless`에 클로저를 전달해 더 복잡한 조건식으로 잡을 건너뛸 수도 있습니다:

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

----  
(*이후 "잡 디스패치"(Dispatching Jobs) 이하 내용 계속해서 번역합니다. 필요시 나머지 부분 요청하세요*)