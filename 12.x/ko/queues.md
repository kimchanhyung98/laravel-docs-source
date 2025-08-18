# 큐 (Queues)

- [소개](#introduction)
    - [커넥션과 큐의 차이](#connections-vs-queues)
    - [드라이버별 참고사항 및 사전 요구사항](#driver-prerequisites)
- [잡 생성하기](#creating-jobs)
    - [잡 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [유니크 잡(Unique Jobs)](#unique-jobs)
    - [암호화된 잡(Encrypted Jobs)](#encrypted-jobs)
- [잡 미들웨어(Job Middleware)](#job-middleware)
    - [레이트 리미팅](#rate-limiting)
    - [잡 중복 처리 방지](#preventing-job-overlaps)
    - [예외 쓰로틀링(Throttling Exceptions)](#throttling-exceptions)
    - [잡 스킵(건너뛰기)](#skipping-jobs)
- [잡 디스패치(Dispatching Jobs)](#dispatching-jobs)
    - [지연 디스패치(Delayed Dispatching)](#delayed-dispatching)
    - [동기 디스패치(Synchronous Dispatching)](#synchronous-dispatching)
    - [잡과 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [잡 체이닝(Job Chaining)](#job-chaining)
    - [큐와 커넥션 커스터마이징](#customizing-the-queue-and-connection)
    - [최대 시도 횟수/타임아웃 값 지정](#max-job-attempts-and-timeout)
    - [에러 처리](#error-handling)
- [잡 배치(Job Batching)](#job-batching)
    - [배치 처리 잡 정의](#defining-batchable-jobs)
    - [배치 디스패치(Dispatching Batches)](#dispatching-batches)
    - [체인과 배치 활용](#chains-and-batches)
    - [배치에 잡 추가하기](#adding-jobs-to-batches)
    - [배치 조회](#inspecting-batches)
    - [배치 취소](#cancelling-batches)
    - [배치 실패](#batch-failures)
    - [배치 데이터 정리(Pruning)](#pruning-batches)
    - [DynamoDB에 배치 저장하기](#storing-batches-in-dynamodb)
- [클로저 큐잉(Queueing Closures)](#queueing-closures)
- [큐 워커 실행하기(Running the Queue Worker)](#running-the-queue-worker)
    - [`queue:work` 명령어](#the-queue-work-command)
    - [큐 우선순위](#queue-priorities)
    - [큐 워커와 배포](#queue-workers-and-deployment)
    - [잡 만료 및 타임아웃](#job-expirations-and-timeouts)
- [Supervisor 설정](#supervisor-configuration)
- [실패한 잡 처리](#dealing-with-failed-jobs)
    - [실패한 잡 후처리](#cleaning-up-after-failed-jobs)
    - [실패한 잡 재시도](#retrying-failed-jobs)
    - [존재하지 않는 모델 무시](#ignoring-missing-models)
    - [실패한 잡 데이터 정리(Pruning)](#pruning-failed-jobs)
    - [DynamoDB에 실패한 잡 저장](#storing-failed-jobs-in-dynamodb)
    - [실패한 잡 저장 비활성화](#disabling-failed-job-storage)
    - [실패한 잡 이벤트](#failed-job-events)
- [큐에서 잡 삭제하기](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [일부 잡만 페이크로 처리하기](#faking-a-subset-of-jobs)
    - [잡 체인 테스트](#testing-job-chains)
    - [잡 배치 테스트](#testing-job-batches)
    - [잡/큐 상호작용 테스트](#testing-job-queue-interactions)
- [잡 이벤트](#job-events)

<a name="introduction"></a>
## 소개 (Introduction)

웹 애플리케이션을 개발하다 보면 업로드된 CSV 파일을 파싱해 저장하는 등 일반적인 웹 요청보다 시간이 오래 걸리는 작업이 생길 수 있습니다. Laravel은 이러한 작업을 쉽게 백그라운드에서 처리할 수 있는 큐 잡(queued job)으로 구현할 수 있도록 해줍니다. 시간이 오래 걸리는 작업을 큐로 옮겨 처리하면, 애플리케이션의 응답 속도와 사용자 경험이 크게 향상됩니다.

Laravel 큐는 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 일반 관계형 데이터베이스 등 다양한 큐 백엔드를 한 번에 다룰 수 있는 통합 API를 제공합니다.

큐와 관련된 설정은 애플리케이션의 `config/queue.php` 파일에 저장되어 있습니다. 이 파일에서는 프레임워크에서 제공하는 각 큐 드라이버(데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 등), 그리고 잡을 즉시 실행하는 동기 드라이버(로컬 개발용), 큐에 들어온 잡을 그대로 폐기하는 `null` 드라이버까지도 설정할 수 있습니다.

> [!NOTE]
> Laravel은 Redis 기반 큐 전용 대시보드 및 설정 시스템인 Horizon을 제공합니다. 자세한 내용은 [Horizon 문서](/docs/12.x/horizon)를 참고하세요.

<a name="connections-vs-queues"></a>
### 커넥션과 큐의 차이 (Connections vs. Queues)

Laravel 큐를 본격적으로 사용하기 전 반드시 “커넥션(connection)”과 “큐(queue)”의 차이점을 이해해야 합니다. `config/queue.php` 파일의 `connections` 배열에는 Amazon SQS, Beanstalk, Redis와 같은 백엔드 큐 서비스에 대한 연결 정보가 들어 있습니다. 하나의 큐 커넥션에는 여러 개의 “큐”를 가질 수 있으며, 이것은 큐에 쌓인 서로 다른 작업 묶음으로 생각할 수 있습니다.

각 커넥션 설정 예시에는 `queue` 속성이 포함되어 있습니다. 이것은 해당 커넥션으로 보낼 때 기본적으로 사용하는 큐 이름입니다. 즉, 잡을 디스패치할 때 별도로 큐를 지정하지 않으면 이 속성에 지정된 큐로 들어가게 됩니다.

```php
use App\Jobs\ProcessPodcast;

// 이 잡은 기본 커넥션의 기본 큐로 전송됩니다.
ProcessPodcast::dispatch();

// 이 잡은 기본 커넥션의 "emails" 큐로 전송됩니다.
ProcessPodcast::dispatch()->onQueue('emails');
```

일부 애플리케이션에서는 단일 큐만으로 충분할 수 있지만, 작업의 우선순위나 분리 처리가 필요한 경우 여러 큐를 활용하는 것이 유용합니다. 왜냐하면 Laravel 큐 워커에서 어떤 큐를 어떤 우선순위로 처리할지 지정할 수 있기 때문입니다. 예를 들어, `high` 큐에 작업을 넣고 그 큐를 먼저 처리하도록 워커를 실행할 수 있습니다.

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버별 참고사항 및 사전 요구사항 (Driver Notes and Prerequisites)

<a name="database"></a>
#### 데이터베이스 드라이버

`database` 큐 드라이버를 사용하려면 잡 데이터를 저장할 데이터베이스 테이블이 필요합니다. 이 테이블은 Laravel의 기본 [데이터베이스 마이그레이션](/docs/12.x/migrations)인 `0001_01_01_000002_create_jobs_table.php`에 포함되어 있습니다. 만약 해당 마이그레이션이 없다면, `make:queue-table` Artisan 명령어로 새로 생성할 수 있습니다.

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis 드라이버

`redis` 큐 드라이버를 사용하려면, `config/database.php` 파일에서 Redis 데이터베이스 연결을 반드시 설정해야 합니다.

> [!WARNING]
> `redis` 큐 드라이버는 Redis의 `serializer`와 `compression` 옵션을 지원하지 않습니다.

<a name="redis-cluster"></a>
##### Redis 클러스터 사용 시

Redis 큐 커넥션이 [Redis Cluster](https://redis.io/docs/latest/operate/rs/databases/durability-ha/clustering)를 사용할 때는 큐 이름에 반드시 [키 해시 태그(key hash tag)](https://redis.io/docs/latest/develop/using-commands/keyspace/#hashtags)를 포함해야 합니다. 이렇게 하면 특정 큐에 속한 모든 Redis 키가 동일한 해시 슬롯에 배치되어 데이터 일관성을 유지할 수 있습니다.

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
##### 블로킹(Blocking) 옵션

Redis 큐를 사용할 때, `block_for` 설정을 통해 워커가 새 잡이 큐에 들어올 때까지 대기하는 시간을 지정할 수 있습니다. 이 값을 조정하면 계속해서 Redis를 폴링하는 것보다 효율적으로 동작할 수 있습니다. 예를 들어, `block_for`를 `5`로 설정하면 5초 동안 잡을 기다렸다가 없으면 한 번 루프를 돌고, 다시 대기하게 됩니다.

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
> `block_for`를 `0`으로 설정하면 새 잡이 들어올 때까지 무한정 블로킹합니다. 이 경우 워커가 SIGTERM 등 시그널을 즉시 처리하지 못하고, 잡이 처리된 이후에야 시그널을 감지하게 됩니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 사전 요구사항

아래 큐 드라이버를 사용하려면 다음 의존성 패키지를 Composer로 설치해야 합니다.

<div class="content-list" markdown="1">

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~2.0` 또는 phpredis PHP 확장
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`

</div>

<a name="creating-jobs"></a>
## 잡 생성하기 (Creating Jobs)

<a name="generating-job-classes"></a>
### 잡 클래스 생성 (Generating Job Classes)

기본적으로, 애플리케이션의 모든 큐 잇은 `app/Jobs` 디렉터리에 저장합니다. 만약 해당 디렉터리가 없다면, `make:job` Artisan 명령어를 실행할 때 자동으로 생성됩니다.

```shell
php artisan make:job ProcessPodcast
```

생성된 클래스를 보면 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하고 있는데, 이는 해당 잡이 큐로 비동기적으로 실행되어야 함을 Laravel에 알려주는 역할을 합니다.

> [!NOTE]
> 잡 스텁(stub) 파일은 [스텁 퍼블리싱](/docs/12.x/artisan#stub-customization)을 통해 커스터마이징할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조 (Class Structure)

잡 클래스는 보통 매우 간단하며, 잡이 처리될 때 호출되는 `handle` 메서드 하나만 포함하고 있습니다. 예시로, 팟캐스트 파일을 업로드 후 게시 전에 처리하는 잡 클래스를 살펴보겠습니다.

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

이 예제에서 볼 수 있듯이, [Eloquent 모델](/docs/12.x/eloquent) 객체를 잡 생성자에 바로 주입하는 것이 가능합니다. `Queueable` 트레이트를 사용하면, Eloquent 모델과 불러온 연관관계 역시 잡이 큐에 들어갈 때 안전하게 직렬화·역직렬화 처리가 됩니다.

만약 잡 생성자에 Eloquent 모델을 넣는 경우, 큐에는 모델의 식별자만 직렬화되어 저장되고, 실제로 잡이 처리될 때 데이터베이스에서 모델 전체와 불러온 연관관계를 다시 로딩합니다. 이처럼 모델 직렬화 방식을 사용하면 큐 페이로드의 크기가 줄어듭니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드의 의존성 주입

`handle` 메서드는 큐가 잡을 처리할 때 호출됩니다. 이때, 의존성 타입 힌트를 통해 필요한 서비스 객체를 주입받을 수 있으며, Laravel [서비스 컨테이너](/docs/12.x/container)가 자동으로 이를 해결해 줍니다.

더 세밀하게 의존성 주입 방식을 제어하고 싶다면, 컨테이너의 `bindMethod` 메서드를 사용할 수 있습니다. 이 메서드는 콜백을 인자로 받아, 그 안에서 직접 `handle` 메서드 호출 방식을 자유롭게 지정할 수 있습니다. 보통 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 등록합니다.

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 이진 데이터(예: 원시 이미지 데이터)는 잡에 전달하기 전에 반드시 `base64_encode`로 인코딩해야 합니다. 그렇지 않으면 잡이 큐에 저장될 때 JSON 직렬화가 올바르게 이뤄지지 않습니다.

<a name="handling-relationships"></a>
#### 큐 잡에서 연관관계(relationships) 다루기

큐에 잡을 넣을 때 로드된 모든 Eloquent 모델 연관관계도 함께 직렬화되어 저장됩니다. 페이로드 크기가 커질 수 있으며, 잡이 복원될 때 연관관계는 별도의 제약 없이 모두 다시 조회됩니다. 즉, 잡 추가 시점에 걸었던 관계의 제한 조건(조건, where 등)은 복원 시에는 적용되지 않으니, 필요하다면 잡 내에서 관계 제한을 다시 지정해주어야 합니다.

또는, 모델의 연관관계를 직렬화에서 제외하고 싶다면, 모델의 속성을 지정할 때 `withoutRelations` 메서드를 사용하면 해당 인스턴스는 관계 정보 없이 저장됩니다.

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

[PHP 생성자 속성 프로모션](https://www.php.net/manual/en/language.oop5.decon.php#language.oop5.decon.constructor.promotion)을 사용하는 경우, Eloquent 모델의 연관관계 직렬화를 막고 싶다면 `WithoutRelations` 속성을 사용할 수 있습니다.

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

모든 모델의 연관관계를 직렬화하지 않으려면, 클래스 전체에 `WithoutRelations` 속성을 적용할 수도 있습니다.

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

또한, 하나의 Eloquent 모델이 아닌 컬렉션이나 배열로 여러 모델을 받는 경우, 잡 역직렬화 시 각 모델의 연관관계는 복원되지 않습니다. 이는 대량의 모델 처리에서 리소스 과다 사용을 막기 위한 조치입니다.

<a name="unique-jobs"></a>
### 유니크 잡(Unique Jobs)

> [!WARNING]
> 유니크 잡 기능을 사용하려면 [락(locks)](/docs/12.x/cache#atomic-locks)을 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 이를 지원합니다. 또, 유니크 잡 제약은 배치 잡(batch)에는 적용되지 않습니다.

특정 잡 인스턴스 하나만 큐에 쌓일 수 있도록 보장하고 싶을 때가 있습니다. 이를 위해 잡 클래스에 `ShouldBeUnique` 인터페이스를 구현하면 됩니다. 별도 메서드를 추가할 필요는 없습니다.

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

위 예시처럼 `UpdateSearchIndex` 잡이 유니크 잡이 되면, 동일한 잡이 큐에 처리 중인 상태라면 추가로 디스패치되지 않습니다.

특정 조건(고유 key 등)으로 유니크를 지정하거나, 잡의 유니크 제한 유지 시간을 설정하고 싶다면, `uniqueId`와 `uniqueFor` 속성 또는 메서드를 정의하면 됩니다.

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    /**
     * 제품 인스턴스.
     *
     * @var \App\Models\Product
     */
    public $product;

    /**
     * 잡 유니크 락이 해제되는 초 단위 시간.
     *
     * @var int
     */
    public $uniqueFor = 3600;

    /**
     * 잡의 고유 ID를 반환.
     */
    public function uniqueId(): string
    {
        return $this->product->id;
    }
}
```

위 예시에서는 제품 ID로 잡의 유니크 여부를 지정합니다. 동일한 제품 ID로 잡을 디스패치하려 해도, 기존 잡이 처리되기 전까지는 새로 들어가지 않습니다. 또, 1시간 이내에 기존 잡 처리가 안 되면 유니크 락이 해제되어 재디스패치가 가능합니다.

> [!WARNING]
> 여러 웹 서버나 컨테이너에서 잡을 디스패치한다면, 모든 서버가 동일한 중앙 캐시 서버를 사용하고 있는지 반드시 확인해야 Laravel에서 잡 중복 여부를 올바르게 판단할 수 있습니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 잡 처리 시작 직전까지 유니크 유지

기본적으로, 유니크 잡은 처리 완료 또는 허용 재시도 횟수 모두 실패 시 락이 해제되어 다른 잡이 디스패치될 수 있습니다. 하지만, 잡이 처리 *시작 직전*에 즉시 락이 풀리도록 하려면 `ShouldBeUnique` 대신 `ShouldBeUniqueUntilProcessing` 인터페이스를 구현합니다.

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

내부적으로 `ShouldBeUnique` 잡이 디스패치되면, Laravel은 [락](/docs/12.x/cache#atomic-locks)을 잡으려 시도합니다. 해당 락이 이미 잡혀 있으면, 잡은 디스패치되지 않습니다. 락은 잡이 완료되거나, 재시도 횟수 모두 실패 시 해제됩니다. Laravel은 기본적으로 기본 캐시 드라이버를 사용해 락을 잡습니다. 다른 캐시 드라이버를 사용하려면, `uniqueVia` 메서드를 정의하면 됩니다.

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
> 동시에 처리하는 잡 수만 제한하고 싶다면 [WithoutOverlapping](#preventing-job-overlaps) 잡 미들웨어 사용을 권장합니다.

<a name="encrypted-jobs"></a>
### 암호화된 잡(Encrypted Jobs)

Laravel에서는 잡 데이터의 프라이버시와 무결성을 [암호화](/docs/12.x/encryption)를 통해 보호할 수 있습니다. 잡 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하면, Laravel이 해당 잡을 큐에 넣기 전에 자동으로 암호화하여 저장합니다.

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

잡 미들웨어를 활용하면, 잡 코드 내에 반복되는 로직(예: 레이트 리미팅 등)을 별도의 클래스에 따로 구현해 잡 코드가 더 간결해집니다. 예를 들어, 아래와 같이 Redis의 레이트 리미터를 활용해 5초마다 한 번씩만 실행되게 할 수 있습니다.

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

이처럼 직접 구현할 수도 있지만, 기능별로 잡 미들웨어 클래스를 만들어 재활용하면 훨씬 깔끔해집니다. Laravel에서는 미들웨어 클래스를 어떤 경로에도 둘 수 있으며, 예시로 `app/Jobs/Middleware` 디렉터리를 사용해보겠습니다.

```php
<?php

namespace App\Jobs\Middleware;

use Closure;
use Illuminate\Support\Facades\Redis;

class RateLimited
{
    /**
     * 큐 잡 처리.
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

라우트 미들웨어처럼, 잡 미들웨어도 잡 객체와 이후 처리를 위한 콜백을 인자로 받습니다.

새 잡 미들웨어 생성은 `make:job-middleware` Artisan 명령어로 가능합니다. 미들웨어를 잡에 적용하려면, 잡 클래스에 `middleware` 메서드를 직접 작성해 미들웨어 객체를 반환해야 합니다. (이 메서드는 기본 잡 스텁에 포함되어 있지 않으니 직접 추가해야 합니다.)

```php
use App\Jobs\Middleware\RateLimited;

/**
 * 잡이 통과해야 하는 미들웨어를 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited];
}
```

> [!NOTE]
> 잡 미들웨어는 [큐 잇 이벤트 리스너](/docs/12.x/events#queued-event-listeners), [메일러블](/docs/12.x/mail#queueing-mail), [노티피케이션](/docs/12.x/notifications#queueing-notifications)에도 적용할 수 있습니다.

<a name="rate-limiting"></a>
### 레이트 리미팅 (Rate Limiting)

직접 미들웨어를 만들 수도 있지만, Laravel에는 이미 레이트 리미팅 미들웨어가 내장되어 있습니다. [라우트 레이트 리미터](/docs/12.x/routing#defining-rate-limiters)를 정의하는 방식과 동일하게 `RateLimiter` 파사드의 `for` 메서드로 잡 제한 규칙을 정의합니다.

특정 일반 사용자는 1시간에 1번, 프리미엄 사용자에게는 제한이 없도록 예시를 들어봅니다.

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Support\Facades\RateLimiter;

/**
 * 애플리케이션 서비스 부트스트랩.
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

`perMinute` 등도 활용해 분 단위 제한이 가능합니다. `by` 메서드에는 보통 고객 식별자를 넣어 각 고객에 대한 제한을 쉽게 구분합니다.

```php
return Limit::perMinute(50)->by($job->user->id);
```

레이트 리미터를 잡에 연결하려면 `Illuminate\Queue\Middleware\RateLimited` 미들웨어를 사용합니다. 잡이 제한을 초과하면 적절한 지연시간을 적용해 다시 큐에 넣어집니다.

```php
use Illuminate\Queue\Middleware\RateLimited;

/**
 * 잡이 통과해야 하는 미들웨어를 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited('backups')];
}
```

지연 처리가 반복되면 시도 횟수(`attempts`)도 함께 증가합니다. 따라서 잡 클래스의 `tries`나 `maxExceptions` 값을 조절하거나, [retryUntil 메서드](#time-based-attempts)로 전체 유효시간을 설정할 수 있습니다.

`releaseAfter` 메서드를 활용하면, 잡을 다시 시도까지 기다릴 초 단위 시간을 직접 지정할 수도 있습니다.

```php
/**
 * 잡이 통과해야 하는 미들웨어를 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new RateLimited('backups'))->releaseAfter(60)];
}
```

레이트 리미트에 걸렸을 때 잡을 재시도하지 않고 아예 버리려면 `dontRelease` 메서드를 사용하세요.

```php
/**
 * 잡이 통과해야 하는 미들웨어를 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new RateLimited('backups'))->dontRelease()];
}
```

> [!NOTE]
> Redis를 사용할 경우 `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어를 활용하면 성능적으로 더욱 최적화되어 있습니다.

<a name="preventing-job-overlaps"></a>
### 잡 중복 처리 방지 (Preventing Job Overlaps)

잡이 동시에 중복 실행되지 않도록 하려면 `Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어를 사용합니다. 이는 특정 리소스를 하나의 잡만 수정할 수 있도록 보장하고자 할 때 유용합니다.

예를 들어, 사용자 한 명의 신용점수 갱신 잡이 동시에 실행되지 않도록 아래처럼 미들웨어를 지정할 수 있습니다.

```php
use Illuminate\Queue\Middleware\WithoutOverlapping;

/**
 * 잡이 통과해야 하는 미들웨어를 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new WithoutOverlapping($this->user->id)];
}
```

중복 잡이 큐에 추가되면 자동으로 재시도 횟수가 증가하므로, `tries` 값 관리에 유의해야 합니다. 기본값 1로 둔 경우, 중복 잡은 한 번만 재시도 후 더 이상 처리되지 않습니다.

몇 초 뒤에 재시도하도록 하려면 `releaseAfter` 메서드를 사용할 수 있습니다.

```php
/**
 * 잡이 통과해야 하는 미들웨어를 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->releaseAfter(60)];
}
```

즉시 중복 잡을 삭제하려면 `dontRelease`도 사용할 수 있습니다.

```php
/**
 * 잡이 통과해야 하는 미들웨어를 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->dontRelease()];
}
```

`WithoutOverlapping` 미들웨어는 Laravel의 아토믹 락(atomic lock) 기능을 활용합니다. 가끔 예기치 않은 실패나 타임아웃으로 락이 해제되지 않을 수도 있으니, 락 만료 시간을 `expireAfter`로 명시해줄 수 있습니다.

```php
/**
 * 잡이 통과해야 하는 미들웨어를 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->expireAfter(180)];
}
```

> [!WARNING]
> `WithoutOverlapping` 미들웨어는 [락 지원 캐시 드라이버](/docs/12.x/cache#atomic-locks)가 반드시 필요합니다.

<a name="sharing-lock-keys"></a>
#### 여러 잡 클래스 간 락 키 공유하기

기본적으로 `WithoutOverlapping` 미들웨어는 같은 클래스의 중복만 방지합니다. 서로 다른 잡 클래스가 동일한 락 키를 사용해도 방지되지 않습니다. 클래스 종류에 상관없이 락 키가 겹치면 중복을 막으려면, `shared` 메서드를 사용하세요.

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
### 예외 쓰로틀링(Throttling Exceptions)

`Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어는 잡이 반복적으로 예외를 던질 때, 설정된 횟수 이상 예외가 발생하면 일정 시간 동안 더 이상 반복 처리를 지연시켜줄 수 있습니다. 이는 외부 API와 같은 불안정한 서비스 통신 시 유용하게 활용할 수 있습니다.

아래는 예외가 연달아 발생할 경우 일정 시간 후 재시도하도록 하는 예시입니다.

```php
use DateTime;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡이 통과해야 하는 미들웨어를 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new ThrottlesExceptions(10, 5 * 60)];
}

/**
 * 잡 실패시 타임아웃 시간 계산.
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(30);
}
```

생성자의 첫 번째 인자는 예외 허용 개수, 두 번째 인자는 쓰로틀링 시 대기할 초 단위 시간입니다. 위 예시에서는 잡이 10번 연속 예외를 던지면 5분 대기 후 재시도하나, 최대 30분까지만 재시도하도록 제한한 형태입니다.

쓰로틀링 전 예외가 발생할 때마다 바로 재시도하지 않고, 몇 분간 대기하도록 하려면 `backoff` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡이 통과해야 하는 미들웨어를 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 5 * 60))->backoff(5)];
}
```

이 미들웨어는 잡 클래스명을 캐시 키로 활용하여 동작합니다. 여러 잡이 동일한 외부 서비스와 통신한다면, `by` 메서드로 공통 키를 주어 쓰로틀링 버킷을 공유할 수 있습니다.

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡이 통과해야 하는 미들웨어를 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->by('key')];
}
```

기본적으로 모든 예외를 쓰로틀링하지만, `when` 메서드로 특정 예외에만 적용할 수도 있습니다.

```php
use Illuminate\Http\Client\HttpClientException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡이 통과해야 하는 미들웨어를 반환.
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

특정 예외 발생 시 잡을 아예 삭제하려면 `deleteWhen` 메서드를 사용하세요.

```php
use App\Exceptions\CustomerDeletedException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡이 통과해야 하는 미들웨어를 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(2, 10 * 60))->deleteWhen(CustomerDeletedException::class)];
}
```

예외가 쓰로틀된 경우에도 예외를 리포트(로깅 등)하려면 `report` 메서드를 활용하세요. 여기엔 클로저를 전달해 특정 조건일 때만 리포트하도록 만들 수도 있습니다.

```php
use Illuminate\Http\Client\HttpClientException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡이 통과해야 하는 미들웨어를 반환.
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
> Redis를 사용할 때는 `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어를 써서 더욱 효율적으로 예외 쓰로틀링이 가능합니다.

<a name="skipping-jobs"></a>
### 잡 스킵(건너뛰기) (Skipping Jobs)

`Skip` 미들웨어를 사용하면 잡 자체 로직을 바꾸지 않고도 조건에 따라 잡을 건너뛰고 삭제할 수 있습니다. `Skip::when`은 조건이 true일 때 잡을 삭제하고, `Skip::unless`는 조건이 false면 삭제합니다.

```php
use Illuminate\Queue\Middleware\Skip;

/**
 * 잡이 통과해야 하는 미들웨어를 반환.
 */
public function middleware(): array
{
    return [
        Skip::when($condition),
    ];
}
```

더 복잡한 조건식이 필요하다면, 클로저로 전달해 사용할 수 있습니다.

```php
use Illuminate\Queue\Middleware\Skip;

/**
 * 잡이 통과해야 하는 미들웨어를 반환.
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

---  
(이후 부분은 질문 길이 한계로 인해 여기서 답변을 마칩니다. 이후 요청 시 남은 부분을 이어 번역해드릴 수 있습니다.)