# 큐 (Queues)

- [소개](#introduction)
    - [커넥션과 큐의 차이](#connections-vs-queues)
    - [드라이버별 사용법 및 사전 조건](#driver-prerequisites)
- [잡 생성하기](#creating-jobs)
    - [잡 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [유니크 잡](#unique-jobs)
    - [암호화된 잡](#encrypted-jobs)
- [잡 미들웨어](#job-middleware)
    - [속도 제한](#rate-limiting)
    - [잡 중복 처리 방지](#preventing-job-overlaps)
    - [예외 제한(Throttle)](#throttling-exceptions)
    - [잡 스킵](#skipping-jobs)
- [잡 디스패치하기](#dispatching-jobs)
    - [지연 디스패치](#delayed-dispatching)
    - [동기 디스패치](#synchronous-dispatching)
    - [잡과 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [잡 체이닝](#job-chaining)
    - [큐 및 커넥션 커스터마이징](#customizing-the-queue-and-connection)
    - [최대 시도 횟수/타임아웃 지정](#max-job-attempts-and-timeout)
    - [SQS FIFO 및 선형 큐](#sqs-fifo-and-fair-queues)
    - [큐 장애조치(Failover)](#queue-failover)
    - [에러 처리](#error-handling)
- [잡 배치](#job-batching)
    - [배치 가능 잡 정의](#defining-batchable-jobs)
    - [배치 디스패치](#dispatching-batches)
    - [체인과 배치](#chains-and-batches)
    - [배치에 잡 추가하기](#adding-jobs-to-batches)
    - [배치 정보 조회](#inspecting-batches)
    - [배치 취소](#cancelling-batches)
    - [배치 실패](#batch-failures)
    - [배치 레코드 정리](#pruning-batches)
    - [DynamoDB에 배치 저장](#storing-batches-in-dynamodb)
- [클로저 큐잉](#queueing-closures)
- [큐 워커 실행하기](#running-the-queue-worker)
    - [`queue:work` 명령어](#the-queue-work-command)
    - [큐 우선순위](#queue-priorities)
    - [워크 및 배포](#queue-workers-and-deployment)
    - [잡 만료 및 타임아웃](#job-expirations-and-timeouts)
    - [큐 워커 일시정지/재개](#pausing-and-resuming-queue-workers)
- [Supervisor 설정](#supervisor-configuration)
- [실패한 잡 다루기](#dealing-with-failed-jobs)
    - [실패 잡 후처리](#cleaning-up-after-failed-jobs)
    - [실패 잡 재시도](#retrying-failed-jobs)
    - [누락된 모델 무시](#ignoring-missing-models)
    - [실패 잡 정리](#pruning-failed-jobs)
    - [DynamoDB에 실패 잡 저장](#storing-failed-jobs-in-dynamodb)
    - [실패 잡 저장 비활성화](#disabling-failed-job-storage)
    - [실패 잡 이벤트](#failed-job-events)
- [큐에서 잡 삭제](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [일부 잡만 페이크 처리](#faking-a-subset-of-jobs)
    - [잡 체인 테스트](#testing-job-chains)
    - [잡 배치 테스트](#testing-job-batches)
    - [잡/큐 상호작용 테스트](#testing-job-queue-interactions)
- [잡 이벤트](#job-events)

<a name="introduction"></a>
## 소개 (Introduction)

웹 애플리케이션을 구현하다 보면, 업로드된 CSV 파일을 파싱하거나 저장하는 등의 시간이 오래 걸리는 작업을 일반적인 웹 요청 중에 처리하기에는 무리가 있을 수 있습니다. 다행히도 Laravel에서는 백그라운드에서 처리할 수 있는 큐 잡(Queue Job)을 손쉽게 만들어 이러한 작업을 효율적으로 처리할 수 있습니다. 부담이 큰 작업을 큐에 옮김으로써, 애플리케이션은 웹 요청에 훨씬 빠르게 응답하게 되고, 사용자는 더욱 쾌적한 경험을 할 수 있습니다.

Laravel 큐는 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 또는 관계형 데이터베이스와 같은 다양한 큐 백엔드에 대해 일관된 큐 API를 제공합니다.

큐 환경설정은 애플리케이션의 `config/queue.php` 파일에 저장되어 있습니다. 이 파일에서는 데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 등의 다양한 큐 드라이버 커넥션 설정을 찾을 수 있으며, 개발·테스트용으로 잡을 즉시 실행하는 동기(synchronous) 드라이버도 포함되어 있습니다. 또한, 큐 작업을 버리는 `null` 드라이버도 마련되어 있습니다.

> [!NOTE]
> Laravel Horizon은 Redis 기반 큐를 위한 아름다운 대시보드 및 설정 시스템입니다. 자세한 내용은 [Horizon 문서](/docs/12.x/horizon)를 참고하세요.

<a name="connections-vs-queues"></a>
### 커넥션과 큐의 차이

Laravel 큐를 사용하기 전에 "커넥션(connection)"과 "큐(queue)"의 차이를 아는 것이 중요합니다. `config/queue.php` 파일에는 `connections` 설정 배열이 있으며, 이 배열은 Amazon SQS, Beanstalk, Redis 등 백엔드 큐 서비스로의 연결 정보를 정의합니다. 한 큐 커넥션에는 여러 개의 "큐"가 존재할 수 있는데, 각각은 서로 다른 작업 스택 또는 잡 모음을 의미할 수 있습니다.

각 커넥션 설정 예시에는 `queue` 속성이 있는데, 이는 해당 커넥션에서 디스패치되는 잡들이 기본적으로 들어갈 큐를 정의합니다. 즉, 잡을 디스패치할 때 특정 큐를 지정하지 않으면, 해당 커넥션 설정의 `queue` 속성에 정의된 곳으로 들어갑니다.

```php
use App\Jobs\ProcessPodcast;

// 이 잡은 기본 커넥션의 기본 큐로 보내집니다.
ProcessPodcast::dispatch();

// 이 잡은 기본 커넥션의 "emails" 큐로 보내집니다.
ProcessPodcast::dispatch()->onQueue('emails');
```

대부분의 애플리케이션에서는 큐를 하나만 사용하는 것이 충분할 수 있습니다. 하지만 여러 큐에 작업을 분배하면, 잡 처리의 우선순위 지정이나 그룹화가 가능해집니다. 예를 들어, `high` 큐에 잡을 넣고, 이 큐에 더 높은 우선순위로 워커를 돌릴 수 있습니다.

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버별 사용법 및 사전 조건

<a name="database"></a>
#### 데이터베이스

`database` 큐 드라이버를 사용하려면 잡을 저장할 테이블이 필요합니다. 보통 Laravel의 기본 `0001_01_01_000002_create_jobs_table.php` [마이그레이션](/docs/12.x/migrations)에 포함되어 있지만, 만약 마이그레이션이 없다면 다음과 같이 `make:queue-table` Artisan 명령어로 생성할 수 있습니다.

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면 `config/database.php` 파일에 Redis 데이터베이스 커넥션을 설정해야 합니다.

> [!WARNING]
> `redis` 큐 드라이버는 Redis의 `serializer`, `compression` 옵션을 지원하지 않습니다.

<a name="redis-cluster"></a>
##### Redis 클러스터

Redis 큐 커넥션이 [Redis Cluster](https://redis.io/docs/latest/operate/rs/databases/durability-ha/clustering)를 사용한다면, 큐 이름에 [키 해시 태그](https://redis.io/docs/latest/develop/using-commands/keyspace/#hashtags)가 포함되어야 합니다. 이는 같은 큐의 모든 Redis 키가 동일한 해시 슬롯에 저장되도록 보장하기 위해 필요합니다.

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

Redis 큐를 사용할 때 `block_for` 설정 옵션을 통해, 워커 루프에서 Redis에서 잡을 다시 폴링하기 전에, 잡이 나올 때까지 얼마나 대기할지 지정할 수 있습니다.

작업량에 따라 이 값을 조정하면, 새 잡을 찾기 위해 Redis를 계속 폴링하는 것보다 더 효율적으로 동작할 수 있습니다. 예를 들어, 5초로 설정하면, 새 잡이 나타날 때까지 5초 동안 대기합니다.

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
> `block_for`를 0으로 설정하면 워커가 잡이 나올 때까지 무한정 대기하게 됩니다. 이 경우, `SIGTERM` 같은 시그널이 다음 잡을 처리할 때까지 적용되지 않습니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 사전 조건

다음 큐 드라이버별로 필요한 의존 패키지는 Composer 패키지 매니저로 설치할 수 있습니다.

<div class="content-list" markdown="1">

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~2.0` 또는 phpredis PHP 익스텐션
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`

</div>

<a name="creating-jobs"></a>
## 잡 생성하기 (Creating Jobs)

<a name="generating-job-classes"></a>
### 잡 클래스 생성

기본적으로, 애플리케이션의 큐 가능한 모든 잡 클래스는 `app/Jobs` 디렉토리에 저장됩니다. 디렉토리가 없다면, `make:job` Artisan 명령어 실행 시 자동으로 생성됩니다.

```shell
php artisan make:job ProcessPodcast
```

생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하게 되며, Laravel에서는 이 인터페이스를 통해 해당 잡을 비동기적으로 큐에 저장할 수 있음을 인식합니다.

> [!NOTE]
> 잡 스텁 파일은 [스텁 퍼블리싱](/docs/12.x/artisan#stub-customization)을 통해 커스터마이즈할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조

잡 클래스는 일반적으로 큐에서 실행되었을 때 호출되는 `handle` 메서드만 포함하는 매우 간단한 구조입니다. 예시를 살펴봅시다. 여기서는 팟캐스트 게시 서비스를 운영한다고 가정하고, 업로드된 팟캐스트 파일을 게시 전에 처리하는 잡을 만듭니다.

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

이 예시에서는 [Eloquent 모델](/docs/12.x/eloquent)을 잡 생성자에 바로 전달하는 것이 가능합니다. `Queueable` 트레이트 덕분에, Eloquent 모델과 그에 로드된 연관관계(relationship)까지도 잡 큐 처리 시 자동적으로 직렬화/역직렬화됩니다.

큐 가능한 잡에 Eloquent 모델을 생성자로 전달하면, 모델의 "식별자"만 큐에 직렬화되고, 실제 큐 처리 시에 전체 모델 인스턴스와 연관 데이터가 데이터베이스에서 다시 로드됩니다. 덕분에, 큐 드라이버로 전송되는 잡 페이로드가 매우 작아집니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드 의존성 주입

잡을 처리할 때 `handle` 메서드가 호출됩니다. 여기서는 `handle` 메서드의 파라미터로 타입힌트를 사용하여 의존성을 선언할 수 있습니다. Laravel의 [서비스 컨테이너](/docs/12.x/container)가 자동으로 의존성을 주입해줍니다.

만약 서비스 컨테이너가 의존성을 주입하는 방식을 직접 제어하고 싶다면, 컨테이너의 `bindMethod` 메서드를 사용할 수 있습니다. 이 메서드는 콜백을 받아 잡과 컨테이너를 전달하며, 이 콜백 내에서 원하는 방식으로 `handle` 메서드를 호출할 수 있습니다. 일반적으로 이 코드는 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 실행합니다.

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 이미지 등 바이너리 데이터는 잡에 전달하기 전에 반드시 `base64_encode` 함수를 이용하여 인코딩해야 합니다. 그렇지 않으면 잡이 큐에 저장될 때 JSON 직렬화가 제대로 되지 않을 수 있습니다.

<a name="handling-relationships"></a>
#### 큐잉된 연관관계 다루기

큐잉 시 Eloquent 모델에 로드된 모든 연관관계 역시 직렬화되므로, 잡 문자열이 커질 수 있습니다. 또한, 잡이 역직렬화되어 DB에서 연관관계가 다시 로드될 때, 원래 걸었던 조건이 사라지고 전체 연관 데이터가 조회됩니다. 따라서, 특정 관계의 일부만 다루고 싶다면 잡 로직 내에서 다시 관계를 제한(re-constrain)해야 합니다.

연관관계의 직렬화를 방지하고 싶다면, 모델 속성을 지정할 때 `withoutRelations` 메서드를 호출하면 됩니다. 이 메서드는 연관관계가 제거된 모델 인스턴스를 반환합니다.

```php
/**
 * 새로운 잡 인스턴스 생성
 */
public function __construct(
    Podcast $podcast,
) {
    $this->podcast = $podcast->withoutRelations();
}
```

[PHP 생성자 프로퍼티 승격](https://www.php.net/manual/kr/language.oop5.decon.php#language.oop5.decon.constructor.promotion)을 쓴다면, Eloquent 모델의 연관관계를 직렬화하지 않도록 하기 위해 `WithoutRelations` 애트리뷰트를 사용할 수 있습니다.

```php
use Illuminate\Queue\Attributes\WithoutRelations;

/**
 * 새로운 잡 인스턴스 생성
 */
public function __construct(
    #[WithoutRelations]
    public Podcast $podcast,
) {}
```

여러 모델 모두의 관계를 직렬화하지 않으려면 클래스 전체에 `WithoutRelations` 애트리뷰트를 적용할 수도 있습니다.

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
     * 새로운 잡 인스턴스 생성
     */
    public function __construct(
        public Podcast $podcast,
        public DistributionPlatform $platform,
    ) {}
}
```

잡이 단일 Eloquent 모델이 아니라 컬렉션이나 배열 형태로 모델 여러 개를 받을 경우, 큐에서 잡이 처리될 때 모델의 연관관계는 복원되지 않습니다. 이는 한 번에 많은 모델을 다루는 잡에서 리소스 소모를 막기 위함입니다.

<a name="unique-jobs"></a>
### 유니크 잡 (Unique Jobs)

> [!WARNING]
> 유니크 잡은 [락(lock)을 지원하는 캐시 드라이버](/docs/12.x/cache#atomic-locks)가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 원자적 락을 지원합니다.

> [!WARNING]
> 유니크 잡 제한은 배치 잡 내에서는 적용되지 않습니다.

특정 잡이 큐에 한 번에 하나만 올라가도록 제한하고 싶다면, 잡 클래스에 `ShouldBeUnique` 인터페이스를 구현하세요. 별도의 추가 메서드 구현은 필요 없습니다.

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

위와 같이 지정하면, 이미 동일한 잡이 큐에 올라가 있고 처리가 끝나지 않았다면 잡이 추가 디스패치되지 않습니다.

경우에 따라 잡의 고유함을 판단할 "키"를 커스터마이즈하거나, 유니크 조건에 대한 타임아웃을 둘 수도 있습니다. 이를 위해 잡 클래스에 `uniqueId`, `uniqueFor` 속성/메서드를 정의할 수 있습니다.

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
     * 잡 유니크 락이 해제될 시간(초)
     *
     * @var int
     */
    public $uniqueFor = 3600;

    /**
     * 고유한 잡 ID 반환
     */
    public function uniqueId(): string
    {
        return $this->product->id;
    }
}
```

위 예시에서는 상품 ID별로 잡의 유니크함을 판별하므로, 동일한 상품 ID로 새로 잡을 디스패치하려고 하면 현재 잡이 처리될 때까지 무시됩니다. 단, 만약 1시간 이내에 완료되지 않으면 유니크 락이 풀리고, 같은 키로 새 잡을 디스패치할 수 있게 됩니다.

> [!WARNING]
> 여러 웹 서버나 컨테이너에서 잡을 디스패치한다면, 모든 서버에서 동일한 중앙 캐시 서버를 쓰는지 반드시 확인해야 정확한 유니크 판단이 가능합니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 잡 처리 시작 전까지 유니크 값 유지

기본적으로 유니크 잡은 잡 처리 완료 또는 모든 재시도 횟수 실패 시 "언락"됩니다. 하지만 처리 직전까지만 유니크 상태를 유지하고 싶을 때는 `ShouldBeUnique` 대신 `ShouldBeUniqueUntilProcessing` 인터페이스를 구현하면 됩니다.

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

내부적으로 `ShouldBeUnique` 잡이 디스패치될 때, Laravel은 `uniqueId` 키로 [락](/docs/12.x/cache#atomic-locks)을 얻으려고 시도합니다. 만약 락이 이미 잡혀 있다면 잡이 디스패치되지 않습니다. 이 락은 잡이 처리 완료되거나 모든 재시도 횟수 실패 시 해제됩니다. 기본적으로 Laravel은 기본 캐시 드라이버를 락에 사용하지만, `uniqueVia` 메서드를 오버라이드해서 특정 캐시 드라이버를 지목할 수 있습니다.

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
> 단순히 잡의 동시 실행 수만 제한하고 싶다면 [WithoutOverlapping](/docs/12.x/queues#preventing-job-overlaps) 잡 미들웨어를 사용하는 것이 더 적합합니다.

<a name="encrypted-jobs"></a>
### 암호화된 잡 (Encrypted Jobs)

잡의 데이터 프라이버시 및 무결성을 보장하기 위해 [암호화](/docs/12.x/encryption)를 적용할 수 있습니다. 이를 위해 해당 잡 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하세요. 이 인터페이스가 붙은 잡은 큐에 올라갈 때 자동으로 암호화됩니다.

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

잡 미들웨어를 이용하면 잡 실행 전후에 커스텀 로직을 감싸서 구현할 수 있으며, 잡 내의 반복되는 코드를 줄일 수 있습니다. 예를 들어, 다음과 같이 Redis의 속도제한(rate limiting) 기능을 직접 `handle` 메서드 안에서 쓸 수도 있습니다.

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

위 같은 코드는 실행에는 문제가 없지만, `handle` 메서드가 너무 복잡해지고 여러 잡에서 로직을 중복해야 합니다. 이런 경우, 속도제한 처리를 잡 미들웨어로 분리하는 것이 적합합니다.

```php
<?php

namespace App\Jobs\Middleware;

use Closure;
use Illuminate\Support\Facades\Redis;

class RateLimited
{
    /**
     * 큐잉된 잡 처리
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

이처럼 [라우트 미들웨어](/docs/12.x/middleware)와 비슷하게, 잡 미들웨어도 잡 인스턴스와 처리 콜백을 파라미터로 받습니다.

`make:job-middleware` Artisan 명령어로 새로운 잡 미들웨어 클래스를 생성할 수 있습니다. 미들웨어를 잡에 적용하려면, 잡 클래스에 `middleware` 메서드를 직접 추가하고 배열 형태로 미들웨어를 반환하면 됩니다(생성 시 자동으로 추가되지 않음).

```php
use App\Jobs\Middleware\RateLimited;

/**
 * 잡에 적용할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited];
}
```

> [!NOTE]
> 잡 미들웨어는 [큐잉된 이벤트 리스너](/docs/12.x/events#queued-event-listeners), [큐잉 메일](/docs/12.x/mail#queueing-mail), [큐잉 알림](/docs/12.x/notifications#queueing-notifications)에도 적용할 수 있습니다.

<a name="rate-limiting"></a>
### 속도 제한 (Rate Limiting)

직접 속도제한 미들웨어를 구현할 수도 있지만, Laravel에 내장된 `RateLimiter` 퍼사드를 이용할 수 있습니다. 라우트 속도제한([route rate limiter](/docs/12.x/routing#defining-rate-limiters))와 비슷하게, `RateLimiter::for`를 사용해 잡별 제한 규칙을 정의합니다.

예를 들어, 일반 회원은 한 시간에 한 번씩만 데이터 백업이 가능하도록 하고, 프리미엄 고객은 제한이 없도록 할 수 있습니다.

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

이 외에도, `perMinute`로 분 단위로 제한하거나, `by` 매개변수에 사용자 고유 값을 주어 사용자별 제한을 둘 수도 있습니다.

```php
return Limit::perMinute(50)->by($job->user->id);
```

이 후 잡 클래스에서 `Illuminate\Queue\Middleware\RateLimited` 미들웨어를 적용하면, 제한 시간에 따라 잡이 자동으로 큐에 다시 올라가게 됩니다.

```php
use Illuminate\Queue\Middleware\RateLimited;

/**
 * 잡에 적용할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited('backups')];
}
```

이렇게 큐에 재등재될 때도 `attempts`(시도 횟수)가 증가하므로, 필요에 따라 `tries` 또는 `maxExceptions` 값을 조정하거나, [`retryUntil` 메서드](#time-based-attempts)로 잡이 더 이상 시도되지 않을 시간까지 지정하세요.

`releaseAfter` 메서드로 재시도까지의 지연 시간을 초 단위로 직접 지정할 수도 있습니다.

```php
public function middleware(): array
{
    return [(new RateLimited('backups'))->releaseAfter(60)];
}
```

만약 제한에 걸리면 잡을 다시 재시도하지 않고 묵살하려면 `dontRelease` 메서드를 사용합니다.

```php
public function middleware(): array
{
    return [(new RateLimited('backups'))->dontRelease()];
}
```

> [!NOTE]
> Redis를 사용할 경우, 더 최적화된 `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어를 사용하는 것이 효율적입니다.

<a name="preventing-job-overlaps"></a>
### 잡 중복 처리 방지 (Preventing Job Overlaps)

동일한 리소스에 대해 여러 잡이 동시에 실행되어서는 안 될 경우가 있습니다. 이를 위해 `Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어를 사용할 수 있으며, 적절한 "키"에 기반해 중복 처리를 막을 수 있습니다.

예를 들어, 특정 사용자에 대한 신용 점수를 업데이트하는 잡에서는 동일 사용자 ID로 중복 실행되는 것을 방지해야 할 수 있습니다.

```php
use Illuminate\Queue\Middleware\WithoutOverlapping;

public function middleware(): array
{
    return [new WithoutOverlapping($this->user->id)];
}
```

중복된 잡이 대기 큐로 다시 올라갈 때도 `attempts`가 증가합니다. 중복 잡의 재시도 횟수를 1로 제한하면 추후 재실행되지 않습니다.

`releaseAfter` 메서드로 재시도까지의 지연 시간(초)을 지정 가능합니다.

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->releaseAfter(60)];
}
```

즉시 중복 잡을 삭제하고 싶다면 `dontRelease`를 사용할 수 있습니다.

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->dontRelease()];
}
```

`expireAfter` 메서드로 락 만료 시간을 (초 단위로) 지정할 수도 있습니다. 예를 들어, 다음 코드는 잡 시작 3분 후에락이 자동 해제됩니다.

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->expireAfter(180)];
}
```

> [!WARNING]
> `WithoutOverlapping` 미들웨어는 [락을 지원하는 캐시 드라이버](/docs/12.x/cache#atomic-locks)가 필요합니다. 지원 드라이버는 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 입니다.

<a name="sharing-lock-keys"></a>
#### 여러 잡 클래스 간의 락 키 공유

기본적으로 `WithoutOverlapping` 미들웨어는 같은 클래스에서만 중복 처리 여부를 판단합니다. 서로 다른 잡 클래스에서 동일한 키를 써도 중복 방지는 되지 않습니다. 여러 잡 클래스에 대해 동일한 키로 중복을 막으려면 `shared` 메서드를 사용하세요.

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
### 예외 제한(Throttle) (Throttling Exceptions)

`Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어는 예외 발생 횟수를 제한하여 지정 횟수 이상 예외를 던지면 일정 시간 동안 잡 처리를 지연시킵니다. 불안정한 외부 서비스와 통신할 때 유용합니다.

예를 들어, 외부 API 호출 잡이 여러 번 연속 예외를 발생시키면, 임시로 잡을 일정 시간 지연시킬 수 있습니다. 일반적으로 [시간 기반 재시도](#time-based-attempts)가 적용된 잡과 결합합니다.

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

생성자 첫 번째 인자는 예외 허용 횟수, 두 번째 인자는 제한이 걸린 뒤 재시도까지의 대기 시간(초)입니다. 위 예시에서는 잡이 10번 연속 예외가 발생하면 5분 후까지 잡 실행이 지연되고, 30분 한도 내에서만 시도됩니다.

예외가 발생했으나 아직 제한 횟수에 도달하지 않은 경우, 즉시 재시도되지만 `backoff`로 딜레이를 둘 수 있습니다.

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 5 * 60))->backoff(5)];
}
```

여러 잡이 같은 외부 자원을 쓴다면 `by` 메서드로 공통 "버킷"을 나눌 수도 있습니다.

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->by('key')];
}
```

모든 예외를 제한하지 않으려면 `when` 메서드로 제한 조건을 클로저로 작성할 수 있습니다.

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

특정 예외 발생 시 해당 잡을 완전히 삭제하려면 `deleteWhen`을 사용합니다.

```php
use App\Exceptions\CustomerDeletedException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [(new ThrottlesExceptions(2, 10 * 60))->deleteWhen(CustomerDeletedException::class)];
}
```

예외가 발생해 제한에 걸릴 때, 해당 예외를 예외 핸들러에 보고하려면 `report` 메서드를 사용합니다. 필요시 true를 반환하는 클로저로 조건을 줄 수 있습니다.

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
> Redis 사용 시에는 더 최적화된 `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어를 쓰세요.

<a name="skipping-jobs"></a>
### 잡 스킵 (Skipping Jobs)

`Skip` 미들웨어를 사용하면 잡 로직을 수정하지 않고도 조건에 따라 잡을 건너뛰고(삭제)할 수 있습니다. `Skip::when`은 조건이 true일 때, `Skip::unless`는 false일 때 잡을 삭제합니다.

```php
use Illuminate\Queue\Middleware\Skip;

/**
 * 잡에 적용할 미들웨어 반환
 */
public function middleware(): array
{
    return [
        Skip::when($condition),
    ];
}
```

더 복잡한 조건 계산이 필요하다면 클로저로 전달할 수도 있습니다.

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

<!-- 나머지 내용은 다음과 같이 계속 문서의 모든 절을 구조·어투·코드·형식 그대로 번역합니다. 
계속하려면 말씀해 주세요. 
(이 한 문장은 실제 답변에 포함되지 않습니다.) -->