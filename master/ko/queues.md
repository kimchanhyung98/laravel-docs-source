# 큐 (Queues)

- [소개](#introduction)
    - [연결 vs. 큐](#connections-vs-queues)
    - [드라이버 안내 및 사전 요구사항](#driver-prerequisites)
- [잡 생성](#creating-jobs)
    - [잡 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [유니크 잡](#unique-jobs)
    - [암호화된 잡](#encrypted-jobs)
- [잡 미들웨어](#job-middleware)
    - [속도 제한](#rate-limiting)
    - [잡 중첩 방지](#preventing-job-overlaps)
    - [예외 제한](#throttling-exceptions)
    - [잡 건너뛰기](#skipping-jobs)
- [잡 디스패치하기](#dispatching-jobs)
    - [지연 디스패치](#delayed-dispatching)
    - [동기식 디스패치](#synchronous-dispatching)
    - [잡과 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [잡 체이닝](#job-chaining)
    - [큐 및 연결 커스터마이징](#customizing-the-queue-and-connection)
    - [최대 시도 횟수 / 타임아웃 값 지정](#max-job-attempts-and-timeout)
    - [SQS FIFO 및 페어 큐](#sqs-fifo-and-fair-queues)
    - [큐 장애 조치](#queue-failover)
    - [에러 핸들링](#error-handling)
- [잡 배치](#job-batching)
    - [배치 가능한 잡 정의](#defining-batchable-jobs)
    - [배치 디스패치](#dispatching-batches)
    - [체인과 배치](#chains-and-batches)
    - [배치에 잡 추가](#adding-jobs-to-batches)
    - [배치 확인](#inspecting-batches)
    - [배치 취소](#cancelling-batches)
    - [배치 실패](#batch-failures)
    - [배치 정리](#pruning-batches)
    - [DynamoDB에 배치 저장](#storing-batches-in-dynamodb)
- [클로저 큐 처리](#queueing-closures)
- [큐 워커 실행](#running-the-queue-worker)
    - [`queue:work` 명령어](#the-queue-work-command)
    - [큐 우선순위](#queue-priorities)
    - [큐 워커와 배포](#queue-workers-and-deployment)
    - [잡 만료 및 타임아웃](#job-expirations-and-timeouts)
    - [큐 워커 일시정지 및 재개](#pausing-and-resuming-queue-workers)
- [Supervisor 설정](#supervisor-configuration)
- [실패한 잡 처리](#dealing-with-failed-jobs)
    - [실패한 잡 처리 후 정리](#cleaning-up-after-failed-jobs)
    - [실패한 잡 재시도](#retrying-failed-jobs)
    - [누락된 모델 무시](#ignoring-missing-models)
    - [실패한 잡 정리](#pruning-failed-jobs)
    - [DynamoDB에 실패한 잡 저장](#storing-failed-jobs-in-dynamodb)
    - [실패한 잡 저장 비활성화](#disabling-failed-job-storage)
    - [실패한 잡 이벤트](#failed-job-events)
- [큐에서 잡 비우기](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [일부 잡만 페이크하기](#faking-a-subset-of-jobs)
    - [잡 체인 테스트](#testing-job-chains)
    - [잡 배치 테스트](#testing-job-batches)
    - [잡 / 큐 상호작용 테스트](#testing-job-queue-interactions)
- [잡 이벤트](#job-events)

<a name="introduction"></a>
## 소개 (Introduction)

웹 애플리케이션을 개발하다 보면, 업로드된 CSV 파일을 파싱하고 저장하는 등 일반적인 웹 요청 내에서 처리하기에는 시간이 오래 걸리는 작업이 생길 수 있습니다. Laravel은 이러한 무거운 작업을 별도의 큐에 잡으로 등록해 백그라운드에서 처리할 수 있게 도와줍니다. 시간이 많이 소요되는 작업을 큐로 옮기면, 애플리케이션이 웹 요청에 더 빠르게 응답할 수 있어 사용자 경험이 크게 향상됩니다.

Laravel 큐는 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 관계형 데이터베이스 등 다양한 큐 백엔드를 지원하며, 일관된 큐 API를 제공합니다.

큐 설정은 애플리케이션의 `config/queue.php` 설정 파일에 보관되어 있습니다. 이 파일에는 프레임워크가 제공하는 각 큐 드라이버(데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 등)를 위한 연결 설정이 정의되어 있습니다. 개발 및 테스트 환경에서는 잡을 즉시 실행하는 동기식 드라이버도 포함되어 있습니다. 잡을 무시하고 버리는 `null` 큐 드라이버도 제공됩니다.

> [!NOTE]
> Laravel Horizon은 Redis 기반 큐를 위한 아름다운 대시보드이자 관리 도구입니다. 자세한 정보는 [Horizon 문서](/docs/master/horizon)를 참고하세요.

<a name="connections-vs-queues"></a>
### 연결 vs. 큐

Laravel 큐를 시작하기 전에 "연결(connection)"과 "큐(queue)"의 차이를 반드시 이해해야 합니다. `config/queue.php` 파일의 `connections` 설정 배열은 Amazon SQS, Beanstalk, Redis와 같은 큐 백엔드 서비스와의 연결을 정의합니다. 하지만 하나의 큐 연결에는 여러 개의 "큐(queues)"를 둘 수 있습니다. 각 큐는 서로 다른 잡 스택 또는 분리된 잡 모음으로 생각할 수 있습니다.

각 연결 설정 예제에는 `queue` 속성이 포함되어 있습니다. 이는 해당 연결에 잡이 전송될 때 디폴트로 사용될 큐입니다. 즉, 잡을 디스패치할 때 순서대로 어느 큐에 보낼지 명시하지 않으면 해당 연결 설정의 `queue` 속성에 지정된 큐에 잡이 들어가게 됩니다.

```php
use App\Jobs\ProcessPodcast;

// 이 잡은 기본 연결의 기본 큐에 전송됩니다...
ProcessPodcast::dispatch();

// 이 잡은 기본 연결의 "emails" 큐에 전송됩니다...
ProcessPodcast::dispatch()->onQueue('emails');
```

간단한 애플리케이션의 경우, 여러 큐를 사용하지 않고 단일 큐만으로 운영할 수 있습니다. 하지만 잡을 우선순위로 처리하거나 잡을 분류하고 싶을 때는 여러 큐에 분산할 수 있습니다. Laravel 큐 워커는 어떤 큐를 우선적으로 처리할지 지정할 수 있으므로, 예를 들어 `high` 큐에 집어넣은 잡을 먼저 처리하도록 워커를 실행할 수 있습니다.

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버 안내 및 사전 요구사항

<a name="database"></a>
#### 데이터베이스

`database` 큐 드라이버를 사용하려면, 잡 정보를 저장할 데이터베이스 테이블이 필요합니다. 보통 `0001_01_01_000002_create_jobs_table.php` [마이그레이션](/docs/master/migrations)이 포함되어 있습니다. 만약 해당 마이그레이션이 없다면, `make:queue-table` Artisan 명령어로 직접 생성할 수 있습니다.

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면, `config/database.php` 파일에 Redis 데이터베이스 연결 정보를 설정해야 합니다.

> [!WARNING]
> `redis` 큐 드라이버에서는 Redis의 `serializer` 및 `compression` 옵션이 지원되지 않습니다.

<a name="redis-cluster"></a>
##### Redis 클러스터

Redis 큐 연결에 [Redis 클러스터](https://redis.io/docs/latest/operate/rs/databases/durability-ha/clustering)를 사용할 경우, 큐 이름에 [키 해시태그](https://redis.io/docs/latest/develop/using-commands/keyspace/#hashtags)를 반드시 포함해야 합니다. 이렇게 하면 주어진 큐의 모든 Redis 키가 동일한 해시 슬롯에 배치됩니다.

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

Redis 큐를 사용할 때, `block_for` 옵션으로 잡이 대기열에 들어올 때까지 드라이버가 대기할 초를 지정할 수 있습니다. 이 옵션을 잘 설정하면 Redis 데이터베이스를 계속 폴링하는 것보다 더 효율적으로 운용할 수 있습니다. 예를 들어, `block_for`에 `5`를 설정하면 잡이 들어오기 전까지 5초간 대기합니다.

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
> `block_for`를 `0`으로 설정하면, 워커가 잡이 들어올 때까지 무한 대기(block)하게 됩니다. 이럴 경우, 잡이 처리되기 전까지 `SIGTERM`과 같은 신호가 전달될 수 없습니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 사전 요구 사항

아래 큐 드라이버별로 필요한 Composer 패키지를 설치해야 합니다.

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

기본적으로 큐잉 가능한 잡 클래스는 `app/Jobs` 디렉터리에 저장됩니다. 만약 이 디렉터리가 없으면 `make:job` Artisan 명령어를 실행할 때 자동으로 생성됩니다.

```shell
php artisan make:job ProcessPodcast
```

생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하며, 이 인터페이스를 통해 Laravel이 잡을 큐에 비동기로 등록해야 함을 알 수 있습니다.

> [!NOTE]
> 잡 스텁(stub)은 [스텁 퍼블리싱](/docs/master/artisan#stub-customization)을 사용해 커스터마이징할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조

잡 클래스는 매우 단순하게 구성되어 있으며, 보통 큐에서 잡을 처리할 때 호출되는 `handle` 메서드만 가집니다. 예시로 팟캐스트 퍼블리싱 서비스를 만든다고 가정하고, 업로드된 팟캐스트 파일을 퍼블리싱 전 가공하는 잡 클래스를 살펴보겠습니다.

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

이 예시에서, [Eloquent 모델](/docs/master/eloquent)을 잡 생성자에 직접 전달할 수 있습니다. `Queueable` 트레이트가 사용되어 있을 때, Eloquent 모델 및 해당 모델의 연관관계들도 잡이 처리될 때 안전하게 직렬화되고 복원됩니다.

만약 잡 생성자에 Eloquent 모델을 전달하면, 모델 식별자만 큐에 직렬화하여 저장됩니다. 실제로 잡이 실행될 때, 큐 시스템이 데이터베이스에서 모델 인스턴스와 로드된 연관관계를 자동으로 다시 불러옵니다. 이렇게 하면 큐에 전송하는 잡의 페이로드 크기를 상당히 줄일 수 있습니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드 의존성 주입

`handle` 메서드는 큐에서 잡을 처리할 때 호출됩니다. 잡의 `handle` 메서드에 타입힌트된 의존성을 선언하면, Laravel [서비스 컨테이너](/docs/master/container)가 해당 의존성을 자동으로 주입합니다.

컨테이너가 `handle` 메서드에 의존성을 주입하는 방식을 완전히 커스터마이즈하고 싶다면, 컨테이너의 `bindMethod` 메서드를 사용할 수 있습니다. 이 메서드는 잡과 컨테이너를 매개변수로 받는 콜백을 등록할 수 있으며, 주로 `App\Providers\AppServiceProvider` [서비스 프로바이더](/docs/master/providers)의 `boot` 메서드에서 호출합니다.

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 원시 바이너리 데이터(예: 이미지 파일 내용)는 잡으로 전달하기 전에 반드시 `base64_encode` 함수를 거쳐 인코딩해야 합니다. 그렇지 않으면 잡이 JSON으로 직렬화될 때 문제가 발생할 수 있습니다.

<a name="handling-relationships"></a>
#### 큐잉된 연관관계

큐잉된 잡에 로드된 모든 Eloquent 연관관계도 직렬화되기 때문에, 직렬화된 잡 문자열이 상당히 커질 수 있습니다. 또한, 잡이 역직렬화되어 모델 연관관계를 다시 읽어올 때, 큐잉 시점에 적용된 제약 조건 없이 전체 연관관계가 불러와집니다. 따라서 특정 연관관계의 일부만 사용하려면, 잡 내부에서 다시 제약 조건을 걸어 사용해야 합니다.

또는, 모델 속성 값을 설정할 때 `withoutRelations` 메서드를 호출해, 모델이 로드된 연관관계를 직렬화하지 않게 할 수 있습니다. 이 메서드는 연관관계가 없는 새로운 인스턴스를 반환합니다.

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

[PHP 생성자 프로퍼티 프로모션](https://www.php.net/manual/en/language.oop5.decon.php#language.oop5.decon.constructor.promotion)을 적용한 경우, Eloquent 모델이 연관관계를 직렬화하지 않도록 하려면 `WithoutRelations` 속성을 사용하십시오.

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

모든 모델을 연관관계 없이 직렬화하고 싶다면, 각 모델에 속성을 적용하는 대신 클래스 전체에 `WithoutRelations` 속성을 부여할 수 있습니다.

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

잡이 모델 단일 인스턴스가 아니라 Eloquent 모델의 컬렉션 또는 배열을 받는 경우, 잡이 역직렬화되어 처리될 때 컬렉션 내의 모델들은 연관관계가 복원되지 않습니다. 이는 다수의 모델 작업에서 과도한 리소스 사용을 방지하기 위함입니다.

<a name="unique-jobs"></a>
### 유니크 잡 (Unique Jobs)

> [!WARNING]
> 유니크 잡은 [락 기능](/docs/master/cache#atomic-locks)을 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 원자적 락을 지원합니다.

> [!WARNING]
> 유니크 잡 제약은 배치 내의 잡에는 적용되지 않습니다.

같은 잡이 동시에 큐에 두 개 이상 올라가지 않게 하고 싶을 때는, 잡 클래스에 `ShouldBeUnique` 인터페이스를 구현하면 됩니다. 별도 메서드 추가 없이 인터페이스만 구현하면 됩니다.

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

위 예시에서 `UpdateSearchIndex` 잡은 유니크하므로, 동일한 잡이 큐에 이미 등록되어 처리 중이면 새로 등록되지 않습니다.

특정 "키"로 잡의 유니크 조건을 지정하거나, 유니크 상태 유지를 위한 제한 시간을 지정하고 싶다면, 잡 클래스에서 `uniqueId` 및 `uniqueFor` 속성이나 메서드를 정의하세요.

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

예를 들어 위 코드에서, `UpdateSearchIndex` 잡은 상품 ID 기준으로 유니크하므로, 같은 상품 ID로 잡을 여러 번 디스패치해도 하나만 큐에 등록되고 기존 잡이 완전히 처리되어야만 다음 등록이 가능합니다. 또한, 잡이 1시간 정도 처리되지 않으면 락이 해제되고 동일한 키의 잡이 다시 큐에 올라갈 수 있습니다.

> [!WARNING]
> 여러 웹 서버나 컨테이너에서 동시에 잡을 디스패치한다면, 모든 서버가 동일한 중앙 캐시 서버를 사용하도록 반드시 설정해야 Laravel이 잡의 유니크 조건을 정확하게 판단할 수 있습니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 잡 처리 직전까지 유니크 유지

기본적으로 유니크 잡은 잡 처리가 성공적으로 끝나거나, 재시도 횟수를 모두 소진한 뒤 락이 해제됩니다. 하지만 처리 직전, 즉 잡 실행 시작 전에 바로 락을 해제하고 싶을 때, 잡에 `ShouldBeUniqueUntilProcessing` 인터페이스를 구현하면 됩니다.

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

내부적으로, `ShouldBeUnique` 잡을 디스패치할 때 Laravel은 `uniqueId` 키로 [락](/docs/master/cache#atomic-locks)을 획득하려 시도합니다. 이미 락이 점유 중이면 잡은 디스패치되지 않습니다. 이 락은 잡이 성공적으로 끝나거나 모든 재시도를 소진했을 때 해제됩니다. 기본적으로 Laravel은 디폴트 캐시 드라이버를 사용해 락을 획득하지만, 다른 드라이버를 사용하려면 `uniqueVia` 메서드를 정의해 원하는 캐시 드라이버를 지정할 수 있습니다.

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
> 단순히 동시에 처리되는 잡의 최대 개수만 제한하고 싶을 때는 [WithoutOverlapping](/docs/master/queues#preventing-job-overlaps) 잡 미들웨어를 사용하는 것이 더 적합합니다.

<a name="encrypted-jobs"></a>
### 암호화된 잡 (Encrypted Jobs)

잡 데이터의 프라이버시와 무결성을 [암호화](/docs/master/encryption)를 이용해 보장할 수 있습니다. 이를 위해 잡 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하면, Laravel이 해당 잡을 큐에 등록하기 전 자동으로 암호화합니다.

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

잡 미들웨어는 큐잉된 잡 실행 전후에 커스텀 로직을 감싸서 실행할 수 있도록 도와줍니다. 이를 통해 반복적으로 필요한 로직을 잡 내보다는 미들웨어에서 처리해 코드의 중복을 줄일 수 있습니다. 예를 들어, 아래는 Redis의 속도 제한(rate limiting) 기능을 통해 5초에 한 번씩만 잡을 처리하는 예시 코드입니다.

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

이처럼 `handle` 메서드 내부에 Redis 속도 제한 로직이 들어가면 코드가 복잡해지고, 같은 방식으로 제한하고자 하는 다른 잡에도 중복 코드가 늘어납니다. 이럴 때 미들웨어를 별도로 만들고, 해당 미들웨어에서 속도 제한을 처리하면 코드가 훨씬 간결해집니다.

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

[라우트 미들웨어](/docs/master/middleware)처럼, 잡 미들웨어도 현재 처리 중인 잡 객체와 처리 흐름을 이어주는 콜백을 파라미터로 받습니다.

`make:job-middleware` Artisan 명령어로 새 잡 미들웨어 클래스를 생성할 수 있습니다. 생성 후, 잡 클래스에 `middleware` 메서드를 추가해 해당 잡이 사용할 미들웨어를 배열로 반환하도록 하면 됩니다. 이 메서드는 `make:job` Artisan 명령어로 scaffold된 잡에는 기본적으로 포함되어 있지 않기 때문에, 직접 추가해야 합니다.

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
> 잡 미들웨어는 [큐잉된 이벤트 리스너](/docs/master/events#queued-event-listeners), [메일러블](/docs/master/mail#queueing-mail), [알림](/docs/master/notifications#queueing-notifications)에도 적용할 수 있습니다.

<a name="rate-limiting"></a>
### 속도 제한

직접 잡 미들웨어로 속도 제한을 구현하지 않아도, Laravel에서 제공하는 속도 제한 미들웨어를 사용할 수 있습니다. [라우트 속도 제한자](/docs/master/routing#defining-rate-limiters)처럼, 잡을 위한 속도 제한자도 `RateLimiter` 파사드의 `for` 메서드로 정의합니다.

예를 들어, 사용자가 데이터를 시간당 1번만 백업하도록 제한(프리미엄 고객 제외)하려면, `AppServiceProvider`의 `boot` 메서드에서 아래처럼 속도 제한자를 정의하면 됩니다.

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

`perMinute` 메서드로 분 단위 제한도 쉽게 설정할 수 있고, `by` 메서드에는 원하는 값을 전달해 고객별로 제한을 둘 수도 있습니다.

```php
return Limit::perMinute(50)->by($job->user->id);
```

정의한 속도 제한자는 `Illuminate\Queue\Middleware\RateLimited` 미들웨어를 잡의 `middleware`에 추가하면 적용됩니다. 잡이 속도 제한에 걸리면, 미들웨어가 정해진 시간 후에 큐에 다시 잡을 등록합니다.

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

속도 제한으로 릴리즈된 잡도 전체 시도 횟수(`attempts`)는 증가합니다. 잡 클래스에서 `tries`, `maxExceptions` 속성이나 [retryUntil 메서드](#time-based-attempts)를 적절히 조정하세요.

`releaseAfter` 메서드로 재시도 대기 시간을 직접 지정할 수도 있습니다.

```php
public function middleware(): array
{
    return [(new RateLimited('backups'))->releaseAfter(60)];
}
```

속도 제한에 걸린 잡을 아예 다시 시도하지 않으려면, `dontRelease` 메서드를 사용하세요.

```php
public function middleware(): array
{
    return [(new RateLimited('backups'))->dontRelease()];
}
```

> [!NOTE]
> Redis를 사용하는 경우, 더 효율적인 `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어를 사용할 수 있습니다.

<a name="preventing-job-overlaps"></a>
### 잡 중첩 방지 (Preventing Job Overlaps)

Laravel은 특정 키값 기준으로 잡 간 중첩을 방지할 수 있는 `Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어를 제공합니다. 이는 리소스 수정이 한 번에 하나의 잡에서만 일어나야 할 때 유용합니다.

예를 들어, 사용자 신용 점수를 업데이트하는 잡이 사용자별로 동시에 실행되지 않게 하려면 아래와 같이 미들웨어를 추가하면 됩니다.

```php
use Illuminate\Queue\Middleware\WithoutOverlapping;

public function middleware(): array
{
    return [new WithoutOverlapping($this->user->id)];
}
```

중첩 잡을 큐에 다시 릴리즈하면 시도 횟수가 증가합니다. 기본값(`tries`)이 1이면 중첩 잡은 재시도되지 않습니다.

또한, 잡을 다시 릴리즈하는 간격도 지정할 수 있습니다.

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->releaseAfter(60)];
}
```

중첩 잡을 아예 즉시 삭제(재시도 불가)하고 싶다면 `dontRelease` 메서드를 사용합니다.

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->dontRelease()];
}
```

`expireAfter` 메서드로 락 만료 시간을 직접 설정할 수도 있습니다. 아래는 잡이 시작된 후 3분이 지나면 락이 자동 해제됩니다.

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->expireAfter(180)];
}
```

> [!WARNING]
> `WithoutOverlapping` 미들웨어는 [락 기능](/docs/master/cache#atomic-locks)을 지원하는 캐시 드라이버가 필요합니다(현재 memcached, redis, dynamodb, database, file, array 지원).

<a name="sharing-lock-keys"></a>
#### 여러 잡 클래스간 락 키 공유

기본적으로, `WithoutOverlapping` 미들웨어는 같은 클래스에 대해서만 잡 중첩을 막아줍니다. 만약 서로 다른 잡 클래스끼리도 같은 락 키를 공유하면서 중첩을 방지하고 싶다면, `shared` 메서드를 사용하세요.

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

Laravel의 `Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어를 사용하면, 잡이 설정한 횟수만큼 예외를 던지면 일정 시간 동안 해당 잡의 실행을 지연시킬 수 있습니다. 주로 외부 불안정 API 등과 상호작용하는 잡에 효과적입니다.

예를 들어, 제3자 API와 통신 시 예외가 잦으면 아래처럼 미들웨어를 추가해 제어할 수 있습니다. 주로 [시간 기반 시도 제한](#time-based-attempts)과 결합해 사용합니다.

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

첫 번째 파라미터는 몇 번 예외가 발생하면 제한할지, 두 번째 파라미터는 제한 시 기다리는 시간을 의미합니다. 만약 예외 기준 미달이면 기본적으로 즉시 재시도 합니다.

`backoff` 메서드로 재시도 대기 시간을 직접 지정할 수도 있습니다.

```php
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 5 * 60))->backoff(5)];
}
```

같은 서비스와 상호작용하는 여러 잡에 "버킷 공유"처럼 공통 제한을 적용하고 싶으면, `by` 메서드로 캐시 키를 오버라이드 하세요.

```php
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->by('key')];
}
```

특정 예외에서만 제한하고 싶다면, `when` 메서드에 클로저를 전달하세요.

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

`deleteWhen`을 사용하면, 특정 예외 발생 시 잡을 아예 삭제할 수 있습니다.

```php
use App\Exceptions\CustomerDeletedException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [(new ThrottlesExceptions(2, 10 * 60))->deleteWhen(CustomerDeletedException::class)];
}
```

예외를 앱의 예외 핸들러에 보고하려면, `report`를 사용하세요. 옵션으로, 클로저를 넘기면 조건에 따라 예외만 보고할 수 있습니다.

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
> Redis를 사용할 경우, 보다 효과적인 `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어를 사용할 수 있습니다.

<a name="skipping-jobs"></a>
### 잡 건너뛰기 (Skipping Jobs)

`Skip` 미들웨어를 사용하면, 잡 로직을 수정하지 않고 특정 조건 시 잡을 스킵(삭제)할 수 있습니다. `Skip::when`은 조건이 참일 때, `Skip::unless`는 조건이 거짓일 때 잡을 삭제합니다.

```php
use Illuminate\Queue\Middleware\Skip;

public function middleware(): array
{
    return [
        Skip::when($condition),
    ];
}
```

더 복잡한 조건을 위해 클로저도 사용할 수 있습니다.

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

<a name="dispatching-jobs"></a>
## 잡 디스패치하기 (Dispatching Jobs)

잡 클래스를 작성했다면, 잡의 `dispatch` 메서드로 큐에 디스패치할 수 있습니다. `dispatch` 메서드에 전달된 파라미터는 잡 생성자의 인수로 넘겨집니다.

```php
<?php

namespace App\Http\Controllers;

use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    /**
     * Store a new podcast.
     */
    public function store(Request $request): RedirectResponse
    {
        $podcast = Podcast::create(/* ... */);

        // ...

        ProcessPodcast::dispatch($podcast);

        return redirect('/podcasts');
    }
}
```

잡 디스패치 여부를 조건적으로 결정하려면 `dispatchIf`, `dispatchUnless` 메서드를 사용할 수 있습니다.

```php
ProcessPodcast::dispatchIf($accountActive, $podcast);

ProcessPodcast::dispatchUnless($accountSuspended, $podcast);
```

Laravel 신규 앱에서는 기본적으로 `database` 연결이 디폴트 큐로 설정되어 있습니다. 다른 연결로 변경하려면 `.env` 파일의 `QUEUE_CONNECTION` 환경 변수를 수정하세요.

<a name="delayed-dispatching"></a>
### 지연 디스패치 (Delayed Dispatching)

잡을 즉시 처리하지 않고, 일정 시간 후에 처리하도록 하려면 디스패치 시 `delay` 메서드를 체이닝하면 됩니다. 예를 들어, 10분 후에 잡을 처리하도록 하려면 다음과 같이 작성합니다.

```php
ProcessPodcast::dispatch($podcast)
    ->delay(now()->plus(minutes: 10));
```

일부 잡에 기본 지연이 걸려 있지만, 바로 처리해야 하는 경우 `withoutDelay`를 사용할 수 있습니다.

```php
ProcessPodcast::dispatch($podcast)->withoutDelay();
```

> [!WARNING]
> Amazon SQS 큐 서비스는 최대 지연 가능 시간이 15분입니다.

<a name="synchronous-dispatching"></a>
### 동기식 디스패치 (Synchronous Dispatching)

잡을 바로(동기적으로) 처리하려면 `dispatchSync` 메서드를 사용합니다. 이 방법으로 디스패치된 잡은 큐에 등록되지 않고 현재 프로세스에서 즉시 처리됩니다.

```php
ProcessPodcast::dispatchSync($podcast);
```

<a name="deferred-dispatching"></a>
#### 지연 동기식 디스패치

지연 동기식 디스패치를 이용하면, 현재 프로세스에서 잡을 처리하되 HTTP 응답이 전송된 후에 실행합니다. 즉 사용자 경험을 저하시키지 않고도 큐잉된 잡을 동기적으로 처리할 수 있습니다. 이를 위해 잡을 `deferred` 연결로 디스패치하세요.

```php
RecordDelivery::dispatch($order)->onConnection('deferred');
```

`deferred` 연결은 [장애 조치](#queue-failover) 기본 큐로도 활용됩니다.

비슷하게, `background` 연결을 사용하면, HTTP 응답 후 별도의 PHP 프로세스에서 잡을 처리해 PHP-FPM/애플리케이션 워커의 부하를 줄일 수 있습니다.

```php
RecordDelivery::dispatch($order)->onConnection('background');
```

<a name="jobs-and-database-transactions"></a>
### 잡과 데이터베이스 트랜잭션 (Jobs & Database Transactions)

데이터베이스 트랜잭션 내에서도 잡을 디스패치할 수 있지만, 주의를 기울여야 합니다. 잡이 트랜잭션 커밋 전에 워커에 의해 처리될 가능성이 있고, 이 경우 트랜잭션 내 변경사항이 데이터베이스에 반영되지 않았을 수 있습니다. 따라서 트랜잭션 내에서 잡을 디스패치하는 경우, 잡이 실제로 언제 실행될지 안전하게 관리하려면 다음 방법을 사용하세요.

큐 연결 설정에 `after_commit` 옵션을 추가하면, 트랜잭션이 커밋된 후 잡을 실제로 디스패치하게 됩니다.

```php
'redis' => [
    'driver' => 'redis',
    // ...
    'after_commit' => true,
],
```

`after_commit`이 `true`면, 트랜잭션이 열려 있으면 잡 디스패치가 커밋 이후로 미뤄지며, 트랜잭션이 없다면 즉시 디스패치됩니다.

트랜잭션 안에서 예외 등으로 롤백되면, 해당 트랜잭션 내에서 디스패치된 잡은 폐기됩니다.

> [!NOTE]
> `after_commit`을 켜면, 큐잉된 이벤트 리스너·메일러블·알림·브로드캐스트 이벤트도 모두 열려 있는 데이터베이스 트랜잭션이 커밋된 이후에 디스패치됩니다.

<a name="specifying-commit-dispatch-behavior-inline"></a>
#### 인라인 커밋 디스패치 제어

큐 연결의 `after_commit` 옵션을 켜지 않은 상황에서도, 특정 잡의 디스패치 행동만 따로 제어할 수 있습니다. 디스패치할 때 `afterCommit`을 체이닝하면, 해당 잡만 트랜잭션 커밋 후 디스패치됩니다.

```php
ProcessPodcast::dispatch($podcast)->afterCommit();
```

반대로, `after_commit`이 켜져 있을 때 즉시(커밋 전에) 디스패치하고 싶으면 `beforeCommit`을 체이닝하면 됩니다.

```php
ProcessPodcast::dispatch($podcast)->beforeCommit();
```

<a name="job-chaining"></a>
### 잡 체이닝 (Job Chaining)

잡 체이닝을 사용하면, 한 잡이 완료된 뒤 지정한 순서대로 추가 잡을 연속 실행할 수 있습니다. 중간에 하나라도 실패하면 이후 잡은 실행되지 않습니다. 잡 체인은 `Bus` 파사드의 `chain` 메서드로 설정하며, Laravel의 커맨드 버스 위에서 잡 큐잉이 동작합니다.

```php
use App\Jobs\OptimizePodcast;
use App\Jobs\ProcessPodcast;
use App\Jobs\ReleasePodcast;
use Illuminate\Support\Facades\Bus;

Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->dispatch();
```

클래스 인스턴스뿐 아니라, 클로저도 체인에 넣을 수 있습니다.

```php
Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    function () {
        Podcast::update(/* ... */);
    },
])->dispatch();
```

> [!WARNING]
> 잡 내부에서 `$this->delete()`로 잡을 삭제해도 체인 다음 잡의 처리에는 영향을 주지 않습니다. 체인 잡 실행은 중간에 실패(예외)한 잡이 있을 때만 중단됩니다.

<a name="chain-connection-queue"></a>
#### 체인 연결 및 큐 지정

체인으로 실행되는 잡들의 큐 연결 및 큐 이름을 별도로 지정하려면, `onConnection`, `onQueue` 메서드를 체인에 사용할 수 있습니다.

```php
Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->onConnection('redis')->onQueue('podcasts')->dispatch();
```

<a name="adding-jobs-to-the-chain"></a>
#### 체인에 잡 추가

잡이 실행되는 과정에서 기존 체인 앞 또는 뒤에 추가 잡을 붙일 수 있습니다. `prependToChain`(앞에), `appendToChain`(뒤에) 메서드를 사용하세요.

```php
public function handle(): void
{
    // 현재 체인 앞에 추가, 즉시 실행됨
    $this->prependToChain(new TranscribePodcast);

    // 현재 체인 맨 뒤에 추가, 마지막에 실행됨
    $this->appendToChain(new TranscribePodcast);
}
```

<a name="chain-failures"></a>
#### 체인 실패 처리

체인 잡 중 하나라도 실패하면, `catch` 메서드로 등록한 콜백이 호출됩니다. 콜백에는 실패를 발생시킨 `Throwable` 인스턴스가 전달됩니다.

```php
use Illuminate\Support\Facades\Bus;
use Throwable;

Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->catch(function (Throwable $e) {
    // 체인 잡 중 하나가 실패했습니다.
})->dispatch();
```

> [!WARNING]
> 체인 콜백은 나중에 큐에서 직렬화되어 실행되므로, 콜백 내부에서 `$this`를 사용하면 안 됩니다.

<a name="customizing-the-queue-and-connection"></a>
### 큐 및 연결 커스터마이징

<a name="dispatching-to-a-particular-queue"></a>
#### 특정 큐로 디스패치

잡을 여러 큐에 분산해, 작업을 "카테고리화"하거나, 각 잡 그룹의 작업자 수를 조절하고 싶다면, `onQueue` 메서드로 잡을 지정 큐에 보낼 수 있습니다. 이는 연결(connection)이 아닌 큐 이름(queue)만 바꾸는 것입니다.

```php
ProcessPodcast::dispatch($podcast)->onQueue('processing');
```

잡 생성자에서 `onQueue`를 호출해도 동일하게 적용됩니다.

```php
public function __construct()
{
    $this->onQueue('processing');
}
```

<a name="dispatching-to-a-particular-connection"></a>
#### 특정 연결로 디스패치

여러 큐 연결(connection)을 사용할 때, 특정 연결로 잡을 보내려면 `onConnection` 메서드를 쓰면 됩니다.

```php
ProcessPodcast::dispatch($podcast)->onConnection('sqs');
```

`onConnection`, `onQueue`를 체이닝해 동시에 지정할 수도 있습니다.

```php
ProcessPodcast::dispatch($podcast)
    ->onConnection('sqs')
    ->onQueue('processing');
```

잡 생성자에서 `onConnection`을 호출할 수도 있습니다.

```php
public function __construct()
{
    $this->onConnection('sqs');
}
```

<a name="queue-routing"></a>
#### 큐 라우팅

`Queue` 파사드의 `route` 메서드를 사용하면, 특정 잡 클래스(또는 인터페이스, 트레이트, 부모 클래스)에 기본 연결 및 큐를 정의할 수 있습니다. 이는 각 잡에서 연결·큐를 지정하지 않아도 특정 잡이 항상 정해진 큐로 보내지도록 할 때 유용합니다.

보통 서비스 프로바이더의 `boot` 메서드에서 호출합니다.

```php
Queue::route(ProcessPodcast::class, connection: 'redis', queue: 'podcasts');
Queue::route(RequiresVideo::class, queue: 'video');
```

연결만 지정하면, 잡은 연결의 기본 큐로 갑니다.

```php
Queue::route(ProcessPodcast::class, connection: 'redis');
```

여러 잡 클래스를 한 번에 라우팅할 수도 있습니다.

```php
Queue::route([
    ProcessPodcast::class => ['podcasts', 'redis'],
    ProcessVideo::class => 'videos',
]);
```

> [!NOTE]
> 해당 잡에서 개별적으로 연결·큐를 지정하면 라우팅 설정을 오버라이드할 수 있습니다.

<a name="max-job-attempts-and-timeout"></a>
### 최대 시도 횟수 / 타임아웃 값 지정

<a name="max-attempts"></a>
#### 최대 시도 횟수

잡 시도 횟수(Attempts)는 Laravel 큐 시스템의 핵심 개념입니다. 잡이 큐에 올라가고, 워커가 이를 가져가며 "시도"하게 됩니다. 단, 이 "시도"가 항상 `handle` 메서드 실행을 의미하지는 않습니다.

시도가 카운트되는 경우:

<div class="content-list" markdown="1">

- 실행 중 처리되지 않은 예외 발생
- `$this->release()`로 잡을 수동 릴리즈
- `WithoutOverlapping`, `RateLimited` 등의 미들웨어로 잡 릴리즈
- 잡 타임아웃 발생
- 잡이 정상적으로 실행되어 예외없이 완료

</div>

무한대로 잡을 계속 시도하고 싶지 않으므로, 여러 방법으로 시도 횟수를 제한합니다.

> [!NOTE]
> 기본값으로, 잡은 한 번만 시도합니다. 미들웨어 또는 수동 릴리즈, 혹은 특별한 상황이 있다면 `tries` 옵션으로 허용 시도 횟수를 높여야 합니다.

잡 시도 최대 횟수는 Artisan 명령어의 `--tries` 스위치로 전체 워커에 대해 적용할 수 있습니다. (잡 클래스에 개별 지정된 시도 횟수가 우선시 됩니다.)

```shell
php artisan queue:work --tries=3
```

최대 시도 횟수를 넘기면, 잡은 "실패(failed)"로 간주됩니다. [실패 잡 처리](#dealing-with-failed-jobs) 문서를 참고하세요. `--tries=0`으로 설정하면 무한 재시도 됩니다.

잡 클래스에 속성이나 메서드로 개별 시도 횟수를 지정할 수 있습니다.

```php
public $tries = 5;
```

메서드 오버라이드로 동적 제어도 가능합니다.

```php
public function tries(): int
{
    return 5;
}
```

<a name="time-based-attempts"></a>
#### 시간 기반 시도 제한

횟수 대신, 정해진 시간 내에 잡이 더 시도되지 않도록 할 수도 있습니다. 잡 클래스에 `retryUntil` 메서드를 추가하면 됩니다. 이 메서드는 `DateTime` 인스턴스를 반환해야 합니다.

```php
public function retryUntil(): DateTime
{
    return now()->plus(minutes: 10);
}
```

`retryUntil`과 `tries`가 모두 정의된 경우, `retryUntil`이 우선합니다.

> [!NOTE]
> [큐잉된 이벤트 리스너](/docs/master/events#queued-event-listeners), [큐잉된 알림](/docs/master/notifications#queueing-notifications)에도 이 속성·메서드를 정의할 수 있습니다.

<a name="max-exceptions"></a>
#### 최대 예외 횟수

잡이 여러 번 재시도되게 하더라도, 미처 처리하지 못한 예외가 일정 횟수 이상 발생하면 실패로 간주하고 싶은 경우가 있을 수 있습니다. 이럴 때는 잡 클래스에 `maxExceptions` 속성을 정의하세요.

```php
public $tries = 25;
public $maxExceptions = 3;
```

이렇게 하면, 예외가 3번 발생할 때까지 최대 25번까지 시도가 가능합니다.

<a name="timeout"></a>
#### 타임아웃

잡의 처리 기대 시간에 맞춰, 잡이 실행 가능한 최대 시간을 제한할 수 있습니다. 기본값은 60초입니다. 잡 처리 시간이 이 시간을 넘기면 워커는 에러와 함께 종료되며(과정은 [프로세스 매니저](#supervisor-configuration)가 관리), 잡은 재시도됩니다.

아티즌 명령어의 `--timeout` 스위치로 전체 워커의 타임아웃을 설정할 수 있습니다.

```shell
php artisan queue:work --timeout=30
```

잡 클래스에 `$timeout` 속성을 둬 개별 잡에 지정하면 이 값이 우선 적용됩니다.

```php
public $timeout = 120;
```

단, 소켓/HTTP 등 블로킹 IO 프로세스는 PHP 레벨 타임아웃을 반드시 명시해야 합니다. [Guzzle](https://docs.guzzlephp.org) 사용 시에도 연결 및 요청 타임아웃 설정을 권장합니다.

> [!WARNING]
> [PCNTL](https://www.php.net/manual/en/book.pcntl.php) PHP 확장이 설치되어 있어야 타임아웃 지정을 지원합니다. 또한, 잡의 타임아웃 값은 ["retry_after"](#job-expiration) 값보다 항상 작아야 합니다. 그렇지 않으면 잡 실행 완료 전 재시도가 발생할 수 있습니다.

<a name="failing-on-timeout"></a>
#### 타임아웃 시 실패 처리

잡이 타임아웃되면, 자동으로 실패(`failed`) 처리하고 싶다면 `$failOnTimeout` 속성을 true로 지정하세요.

```php
public $failOnTimeout = true;
```

> [!NOTE]
> 기본적으로 잡 타임아웃 시에는 한 번의 시도만 소진되고 큐에 다시 릴리즈됩니다(재시도가 허용된 경우). `$failOnTimeout`을 사용하면 시도 횟수와 상관없이 곧바로 실패 처리됩니다.

<a name="sqs-fifo-and-fair-queues"></a>
### SQS FIFO 및 페어 큐 (SQS FIFO and Fair Queues)

Laravel은 [Amazon SQS FIFO(First-In-First-Out)](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-fifo-queues.html) 큐를 지원하며, 정확한 순서로 처리 및 메시지 중복 제거에 따른 단 한 번만 처리 보장까지 제공합니다.

FIFO 큐는 메시지 그룹 ID가 필요하며, 같은 그룹 ID의 잡은 순차적으로, 다른 그룹 ID의 메시지는 병렬로 처리됩니다.

잡을 디스패치할 때 `onGroup` 메서드로 그룹 ID를 지정하세요.

```php
ProcessOrder::dispatch($order)
    ->onGroup("customer-{$order->customer_id}");
```

메시지 중복 제거를 위해 잡 클래스에 `deduplicationId` 메서드를 구현하면, 직접 ID 기준을 커스터마이징할 수 있습니다.

```php
public function deduplicationId(): string
{
    return "renewal-{$this->subscription->id}";
}
```

<a name="fifo-listeners-mail-and-notifications"></a>
#### FIFO 리스너, 메일, 알림

FIFO 큐 사용 시, 이벤트 리스너, 메일, 알림에도 메시지 그룹 지정을 해줘야 하며, 또는 이런 작업들을 FIFO 큐가 아닌 일반 큐로 디스패치할 수도 있습니다.

[이벤트 리스너](/docs/master/events#queued-event-listeners)의 경우, `messageGroup` 메서드를 추가하면 그룹을 지정할 수 있습니다. `deduplicationId`도 함께 구현할 수 있습니다.

```php
public function messageGroup(): string
{
    return 'shipments';
}

public function deduplicationId(): string
{
    return "shipment-notification-{$this->shipment->id}";
}
```

[메시지 큐잉 메일](/docs/master/mail)에서도 `onGroup`(필수), `withDeduplicator`(선택)를 호출할 수 있습니다.

```php
$invoicePaid = (new InvoicePaid($invoice))
    ->onGroup('invoices')
    ->withDeduplicator(fn () => 'invoices-'.$invoice->id);

Mail::to($request->user())->send($invoicePaid);
```

[알림](/docs/master/notifications)도 메일과 동일합니다.

```php
$invoicePaid = (new InvoicePaid($invoice))
    ->onGroup('invoices')
    ->withDeduplicator(fn () => 'invoices-'.$invoice->id);

$user->notify($invoicePaid);
```

<a name="queue-failover"></a>
### 큐 장애 조치 (Queue Failover)

`failover` 큐 드라이버는 큐에 잡을 등록할 때 여러 연결을 순차로 대체해 장애 조치 기능을 제공합니다. 첫 번째 연결이 실패하면, 다음 연결로 자동 대체되며, 안정성을 극대화할 수 있습니다.

설정 예시는 다음과 같습니다.

```php
'failover' => [
    'driver' => 'failover',
    'connections' => [
        'redis',
        'database',
        'sync',
    ],
],
```

`.env` 파일의 기본 큐 연결을 `failover`로 설정해야 기능을 사용할 수 있습니다.

```ini
QUEUE_CONNECTION=failover
```

장애 조치 연결 리스트에 포함된 각 연결별로 최소 하나의 워커를 기동해야 합니다.

```bash
php artisan queue:work redis
php artisan queue:work database
```

> [!NOTE]
> `sync`, `background`, `deferred` 드라이버에는 별도의 워커가 필요하지 않습니다(동기적 처리).

장애 조치가 발생하면, Laravel은 `Illuminate\Queue\Events\QueueFailedOver` 이벤트를 발생시켜 로그나 알림 처리를 할 수 있습니다.

> [!NOTE]
> Laravel Horizon은 오직 Redis 큐만 관리합니다. 장애 조치 리스트에 `database`가 있다면, 별도로 `php artisan queue:work database`를 실행해야 합니다.

<a name="error-handling"></a>
### 에러 핸들링 (Error Handling)

잡 처리 중 예외가 발생하면, 잡은 큐에 다시 릴리즈되어 재시도됩니다. 설정된 최대 시도 횟수까지 계속 반복되며, 최대 횟수는 `queue:work` 명령의 `--tries` 스위치나 잡 클래스에 개별 지정할 수 있습니다. 자세한 내용은 [아래 설명](#running-the-queue-worker)을 참고하세요.

<a name="manually-releasing-a-job"></a>
#### 잡 수동 릴리즈

잡을 수동으로 다시 큐에 넣고 싶을 때는 `release` 메서드를 사용합니다.

```php
public function handle(): void
{
    // ...

    $this->release();
}
```

기본적으로 `release`는 즉시 잡을 다시 사용 가능하게 만듭니다. 정해진 시간 후에만 처리되게 하려면 정수(초)나 날짜 인스턴스를 넘길 수 있습니다.

```php
$this->release(10);

$this->release(now()->plus(seconds: 10));
```

<a name="manually-failing-a-job"></a>
#### 잡 수동 실패 처리

잡을 수동으로 "실패(failed)" 처리하고 싶으면 `fail` 메서드를 사용합니다.

```php
public function handle(): void
{
    // ...

    $this->fail();
}
```

예외 객체나 문자열 메시지로 실패 사유를 남길 수도 있습니다.

```php
$this->fail($exception);

$this->fail('Something went wrong.');
```

> [!NOTE]
> 실패 잡에 대한 자세한 처리법은 [실패 잡 처리 문서](#dealing-with-failed-jobs)를 참고하세요.

<a name="fail-jobs-on-exceptions"></a>
#### 특정 예외에서 잡 실패 처리

`FailOnException` [잡 미들웨어](#job-middleware)를 적용하면, 특정 예외 발생 시 자동으로 잡을 실패 처리할 수 있습니다. 예를 들어, 일시적인 API 에러는 재시도하고, 사용 권한이 박탈된 경우에는 즉시 실패로 처리할 때 유용합니다.

```php
public function middleware(): array
{
    return [
        new FailOnException([AuthorizationException::class])
    ];
}
```

아래 이후 번역 본은 너무 길기 때문에, 필요시 이어서 제공합니다.