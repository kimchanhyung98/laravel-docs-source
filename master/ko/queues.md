# 큐 (Queues)

- [소개](#introduction)
    - [커넥션과 큐의 차이](#connections-vs-queues)
    - [드라이버별 주의사항 및 사전 준비](#driver-prerequisites)
- [잡 생성하기](#creating-jobs)
    - [잡 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [고유 잡(Unique Jobs)](#unique-jobs)
    - [암호화된 잡(Encrypted Jobs)](#encrypted-jobs)
- [잡 미들웨어](#job-middleware)
    - [속도 제한(Rate Limiting)](#rate-limiting)
    - [잡 중복 처리 방지](#preventing-job-overlaps)
    - [예외 쓰로틀링(Throttling Exceptions)](#throttling-exceptions)
    - [잡 건너뛰기](#skipping-jobs)
- [잡 디스패치(Dispatching)](#dispatching-jobs)
    - [지연 디스패치](#delayed-dispatching)
    - [동기 디스패치](#synchronous-dispatching)
    - [잡과 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [잡 체이닝(Job Chaining)](#job-chaining)
    - [큐와 커넥션 커스터마이징](#customizing-the-queue-and-connection)
    - [잡 최대 시도 횟수 / 타임아웃 지정](#max-job-attempts-and-timeout)
    - [에러 처리](#error-handling)
- [잡 배치 실행(Job Batching)](#job-batching)
    - [배치 처리 가능한 잡 정의](#defining-batchable-jobs)
    - [잡 배치 디스패치](#dispatching-batches)
    - [체인과 배치](#chains-and-batches)
    - [배치에 잡 추가](#adding-jobs-to-batches)
    - [배치 검사](#inspecting-batches)
    - [배치 취소](#cancelling-batches)
    - [배치 실패](#batch-failures)
    - [배치 정리(Pruning)](#pruning-batches)
    - [DynamoDB에 배치 저장](#storing-batches-in-dynamodb)
- [클로저 큐잉](#queueing-closures)
- [큐 워커 실행](#running-the-queue-worker)
    - [`queue:work` 명령어](#the-queue-work-command)
    - [큐 우선순위](#queue-priorities)
    - [큐 워커와 배포](#queue-workers-and-deployment)
    - [작업 만료 및 타임아웃](#job-expirations-and-timeouts)
- [Supervisor 설정](#supervisor-configuration)
- [실패한 잡 처리](#dealing-with-failed-jobs)
    - [실패한 잡 후처리](#cleaning-up-after-failed-jobs)
    - [실패한 잡 재시도](#retrying-failed-jobs)
    - [존재하지 않는 모델 무시](#ignoring-missing-models)
    - [실패한 잡 정리](#pruning-failed-jobs)
    - [DynamoDB에 실패한 잡 저장](#storing-failed-jobs-in-dynamodb)
    - [실패한 잡 저장 비활성화](#disabling-failed-job-storage)
    - [실패한 잡 이벤트](#failed-job-events)
- [큐에서 잡 삭제(Clearing)](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [일부 잡만 페이크 처리](#faking-a-subset-of-jobs)
    - [잡 체인 테스트](#testing-job-chains)
    - [잡 배치 테스트](#testing-job-batches)
    - [잡/큐 상호작용 테스트](#testing-job-queue-interactions)
- [잡 이벤트](#job-events)

<a name="introduction"></a>
## 소개 (Introduction)

웹 애플리케이션을 개발하다 보면, 업로드된 CSV 파일을 파싱하고 저장하는 등, 일반적인 웹 요청 중에 처리하기에는 시간이 많이 소요되는 작업들이 있을 수 있습니다. 다행히도, Laravel은 이러한 작업을 백그라운드에서 처리할 수 있는 큐 잡을 손쉽게 생성할 수 있게 해줍니다. 시간이 오래 걸리는 작업을 큐로 분리하면, 애플리케이션이 웹 요청에 훨씬 빠르게 응답할 수 있어 사용자 경험이 크게 향상됩니다.

Laravel의 큐 시스템은 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 또는 관계형 데이터베이스 등 다양한 큐 백엔드를 하나의 통일된 API로 사용할 수 있도록 제공합니다.

큐 관련 설정은 애플리케이션의 `config/queue.php` 설정 파일에 저장되어 있습니다. 이 파일에는 데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 등 프레임워크에 포함된 각 큐 드라이버에 대한 커넥션 설정이 담겨 있습니다. 또한, 잡을 즉시 실행하는 동기(synchronous) 드라이버(로컬 개발용)와 큐에 넣은 잡을 버리는 `null` 큐 드라이버도 제공됩니다.

> [!NOTE]
> Laravel에서는 Redis 기반 큐를 관리할 수 있는 아름다운 대시보드인 Horizon도 제공합니다. 자세한 내용은 [Horizon 문서](/docs/master/horizon)를 참고하세요.

<a name="connections-vs-queues"></a>
### 커넥션과 큐의 차이

Laravel 큐를 사용하기 전에 "커넥션(connection)"과 "큐(queue)"의 차이를 이해하는 것이 중요합니다. `config/queue.php` 설정 파일에는 `connections` 배열이 있습니다. 이 배열은 Amazon SQS, Beanstalk, Redis 등 백엔드 큐 서비스에 대한 커넥션을 정의합니다. 한 큐 커넥션에는 여러 개의 "큐"를 둘 수 있는데, 이는 일종의 잡이 쌓이는 스택 혹은 덩어리로 볼 수 있습니다.

각 커넥션 설정 예제에는 `queue` 속성이 포함되어 있는데, 이는 해당 커넥션에서 잡이 디스패치될 기본 큐를 의미합니다. 즉, 어떤 큐를 지정하지 않고 잡을 디스패치하면, 해당 커넥션 설정의 `queue` 속성에 설정된 큐에 잡이 쌓이게 됩니다:

```php
use App\Jobs\ProcessPodcast;

// 이 잡은 기본 커넥션의 기본 큐로 전송됩니다...
ProcessPodcast::dispatch();

// 이 잡은 기본 커넥션의 "emails" 큐로 전송됩니다...
ProcessPodcast::dispatch()->onQueue('emails');
```

모든 애플리케이션이 여러 큐를 사용할 필요는 없으며, 단일 큐만을 사용하는 것이 더 단순한 경우도 많습니다. 하지만 여러 큐에 작업을 분산하여 작업의 우선순위나 종류에 따라 큐 워커가 다르게 처리하도록 할 수도 있습니다. 예를 들어, `high`라는 큐에 중요한 작업을 보내고, 워커가 `high` 큐를 우선적으로 처리하게 할 수 있습니다:

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버별 주의사항 및 사전 준비

<a name="database"></a>
#### 데이터베이스

`database` 큐 드라이버를 사용하려면, 잡을 저장할 데이터베이스 테이블이 필요합니다. 이 테이블은 일반적으로 Laravel 기본 마이그레이션 파일 `0001_01_01_000002_create_jobs_table.php`에 포함되어 있습니다. 만약 해당 마이그레이션이 없다면, 다음 Artisan 명령어로 생성할 수 있습니다:

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면, 먼저 `config/database.php` 설정 파일에 Redis 데이터베이스 커넥션을 등록해야 합니다.

> [!WARNING]
> `redis` 큐 드라이버는 Redis의 `serializer` 및 `compression` 옵션을 지원하지 않습니다.

**Redis 클러스터**

Redis 큐 커넥션이 Redis 클러스터를 사용하는 경우, 큐 이름에 [키 해시 태그(key hash tag)](https://redis.io/docs/reference/cluster-spec/#hash-tags)를 사용해야 합니다. 이를 통해 동일한 큐에 속한 모든 Redis 키가 같은 해시 슬롯에 저장되도록 해야 합니다:

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

**블로킹(Blocking)**

Redis 큐를 사용할 때, `block_for` 설정 옵션으로 큐 워커가 잡이 대기할 때 얼마나 블로킹(대기)할지 지정할 수 있습니다. 이 값을 큐의 부하에 맞게 조절하면, 지속적으로 Redis를 폴링하지 않고 더 효율적으로 잡을 처리할 수 있습니다. 예를 들어, 5초로 설정하면 잡이 생길 때까지 5초 동안 대기합니다:

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
> `block_for`를 `0`으로 설정하면 잡이 대기열에 나타날 때까지 큐 워커가 무한정 블로킹됩니다. 이 경우, `SIGTERM` 등 시스템 신호가 다음 잡이 실행되기 전까지는 처리되지 않을 수 있습니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 사전 준비

다음 드라이버들은 아래의 Composer 패키지 의존성이 필요합니다:

<div class="content-list" markdown="1">

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~2.0` 또는 phpredis PHP 확장
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`

</div>

<a name="creating-jobs"></a>
## 잡 생성하기

<a name="generating-job-classes"></a>
### 잡 클래스 생성

기본적으로, 애플리케이션의 큐에 넣을 수 있는 모든 잡 클래스는 `app/Jobs` 디렉토리에 위치합니다. 만약 이 디렉토리가 없다면, `make:job` Artisan 명령어를 실행할 때 자동으로 생성됩니다:

```shell
php artisan make:job ProcessPodcast
```

생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하며, Laravel이 해당 잡을 큐에 넣어 비동기적으로 실행해야 한다는 것을 인식하게 해줍니다.

> [!NOTE]
> 잡 스텁(stub)은 [스텁 퍼블리싱](/docs/master/artisan#stub-customization)을 통해 커스터마이즈할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조

잡 클래스는 보통 매우 단순하며, 큐에서 잡이 실행될 때 호출되는 `handle` 메서드만 포함합니다. 아래의 예제를 살펴봅시다. 여기서는 팟캐스트 업로드 파일을 처리하는 잡을 가정합니다:

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

여기에서 볼 수 있듯, [Eloquent 모델](/docs/master/eloquent)을 잡 생성자에 직접 전달할 수 있습니다. 잡이 사용하는 `Queueable` 트레이트 덕분에, Eloquent 모델과 이미 로딩된 연관관계 데이터가 직렬화 및 역직렬화될 때 자동으로 처리됩니다.

만약 잡 생성자의 인자로 Eloquent 모델을 전달하면, 모델의 식별자만 큐에 직렬화됩니다. 이후 실제 잡이 처리될 때, 큐 시스템이 데이터베이스에서 모델 인스턴스와 연관관계들을 다시 로딩합니다. 이렇게 하면 큐에 저장되는 잡 페이로드가 작아지고 효율적으로 관리할 수 있습니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드 의존성 주입(Dependency Injection)

큐 잡이 처리될 때 `handle` 메서드가 호출됩니다. `handle` 메서드의 인자로 의존성을 타입 힌트하여 지정할 수 있고, Laravel [서비스 컨테이너](/docs/master/container)가 이를 자동으로 주입해줍니다.

만약 `handle` 메서드에 대한 의존성 주입을 완전히 제어하고 싶다면, 컨테이너의 `bindMethod` 메서드를 사용할 수 있습니다. 아래 예제처럼, `App\Providers\AppServiceProvider` [서비스 프로바이더](/docs/master/providers)의 `boot` 메서드에서 이 메서드를 호출하는 것이 일반적입니다:

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 원시 이미지 데이터 등 바이너리 데이터는 잡에 전달하기 전에 반드시 `base64_encode` 함수를 통과시켜야 합니다. 그렇지 않으면 큐에 JSON으로 직렬화할 때 오류가 발생할 수 있습니다.

<a name="handling-relationships"></a>
#### 큐잉된 연관관계(Relationships) 처리

잡이 큐에 들어갈 때, Eloquent 모델의 로딩된 모든 연관관계도 같이 직렬화됩니다. 이로 인해 잡 직렬화 문자열이 매우 커질 수 있습니다. 또, 잡이 역직렬화될 때 연관관계들은 완전히 새로 조회됩니다. 따라서 큐잉 전 모델에 제한(컨스트레인트)이 걸렸더라도, 잡이 실행될 때에는 제한이 걸리지 않은 전체 데이터가 조회됩니다. 일부 연관관계만 다루고 싶다면, 잡 내부에서 직접 연관관계를 재설정해야 합니다.

또는, 직렬화 시 연관관계 데이터를 포함하지 않으려면, 모델에 `withoutRelations` 메서드를 사용해 속성을 지정하세요. 이 방법은 해당 속성에 연관관계가 포함되지 않은 모델 인스턴스를 반환합니다:

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

PHP 생성자 프로퍼티 프로모션(Constructor Property Promotion)과 함께 Eloquent 모델의 연관관계 직렬화를 비활성화하려면, `WithoutRelations` 속성을 사용할 수 있습니다:

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

잡이 Eloquent 모델의 컬렉션이나 배열을 받았다면, 잡이 역직렬화 및 실행될 때 컬렉션 내 각 모델의 연관관계는 복구되지 않습니다. 이는 한 번에 많은 모델을 다루는 잡의 리소스 사용량을 제어하기 위함입니다.

<a name="unique-jobs"></a>
### 고유 잡(Unique Jobs)

> [!WARNING]
> 고유 잡 기능을 사용하려면 [락(lock)](/docs/master/cache#atomic-locks)을 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 원자적 락을 지원합니다. 또한 고유 잡 제약 조건은 배치 내의 잡에는 적용되지 않습니다.

특정 잡 인스턴스가 한 번에 큐에 한 개만 존재하도록 보장하고 싶을 때가 있습니다. 이를 위해 잡 클래스에 `ShouldBeUnique` 인터페이스를 구현하면 됩니다. 해당 인터페이스를 구현해도 추가적인 메서드를 작성할 필요는 없습니다:

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

위 예제에서 `UpdateSearchIndex` 잡은 고유합니다. 그렇기 때문에, 동일한 잡 인스턴스가 이미 큐에 있고 처리가 완료되지 않았다면 신규 잡은 큐에 등록되지 않습니다.

잡 고유성을 판별하는 "키"를 지정하거나, 고유 락의 만료시간을 지정하고 싶다면, `uniqueId` 및 `uniqueFor` 프로퍼티나 메서드를 클래스에 정의할 수 있습니다:

```php
<?php

use App\Models\Product;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    /**
     * 상품 인스턴스
     *
     * @var \App\Product
     */
    public $product;

    /**
     * 잡 고유 락 만료 시간(초).
     *
     * @var int
     */
    public $uniqueFor = 3600;

    /**
     * 잡의 고유 ID 반환
     */
    public function uniqueId(): string
    {
        return $this->product->id;
    }
}
```

위처럼, 잡은 상품 ID 기준으로 고유하게 구분됩니다. 같은 상품 ID로 잡을 디스패치해도 기존 잡의 처리가 끝나기 전까지는 무시됩니다. 또, 기존 잡이 1시간 내에 처리되지 않으면 고유 락이 해제되고 같은 키로 새 잡을 큐에 넣을 수 있습니다.

> [!WARNING]
> 애플리케이션에서 여러 웹 서버 또는 컨테이너에서 잡을 디스패치한다면, 고유 잡 판별을 위해 모든 서버가 동일한 중앙 캐시 서버를 이용해야 합니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 처리 시작 전까지 잡 고유 락 유지

기본적으로 고유 잡은 잡 처리 완료 또는 모든 재시도 실패 후에 "락이 풀립니다". 하지만, 잡이 처리되기 '직전'에 락을 해제하고 싶다면, `ShouldBeUnique` 대신 `ShouldBeUniqueUntilProcessing` 인터페이스를 구현하세요:

```php
<?php

use App\Models\Product;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUniqueUntilProcessing;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUniqueUntilProcessing
{
    // ...
}
```

<a name="unique-job-locks"></a>
#### 고유 잡 락

실제로 `ShouldBeUnique` 잡이 디스패치될 때, Laravel은 내부적으로 [락](/docs/master/cache#atomic-locks)을 `uniqueId` 키로 획득합니다. 락을 얻지 못하면 잡이 큐에 디스패치되지 않습니다. 락은 잡이 처리 완료되거나 모든 재시도가 실패했을 때 해제됩니다. 기본적으로는 기본 캐시 드라이버를 이용하지만, 별도의 드라이버를 사용하고 싶다면 `uniqueVia` 메서드를 정의하세요:

```php
use Illuminate\Contracts\Cache\Repository;
use Illuminate\Support\Facades\Cache;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...

    /**
     * 고유 잡 락을 위한 캐시 드라이버 반환
     */
    public function uniqueVia(): Repository
    {
        return Cache::driver('redis');
    }
}
```

> [!NOTE]
> 단순히 잡의 동시 실행만 제한하려면, [`WithoutOverlapping`](/docs/master/queues#preventing-job-overlaps) 잡 미들웨어를 사용하는 것이 더 적절합니다.

<a name="encrypted-jobs"></a>
### 암호화된 잡(Encrypted Jobs)

Laravel은 잡 데이터의 기밀성과 무결성을 [암호화](/docs/master/encryption)로 보장할 수 있습니다. 잡 클래스에 `ShouldBeEncrypted` 인터페이스를 추가만 하면, 잡이 큐에 들어가기 전에 자동으로 암호화됩니다:

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

잡 미들웨어를 사용하면 큐에 등록된 잡의 실행 전후로 사용자 정의 로직을 덧붙일 수 있어, 잡 코드 내 보일러플레이트를 줄일 수 있습니다. 예를 들어, Laravel의 Redis 기반 속도 제한 기능을 활용하여 5초에 한 번만 잡을 처리하도록 할 수 있습니다:

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

위 코드는 유효하지만, 속도 제한 로직이 `handle` 메서드를 복잡하게 만듭니다. 그리고 동일한 패턴을 여러 잡에 반복적으로 구현해야 한다는 단점도 있습니다.

이런 경우, 속도 제한 로직을 별도의 잡 미들웨어로 분리할 수 있습니다. Laravel에서는 잡 미들웨어의 기본 위치가 별도로 정해져 있지 않으므로, 예시에서는 `app/Jobs/Middleware` 디렉토리에 생성하겠습니다:

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

라우트 미들웨어처럼, 잡 미들웨어도 현재 처리 중인 잡과 다음 콜백을 인자로 받아, 체이닝 방식으로 처리할 수 있습니다.

잡 미들웨어를 추가하려면, 잡 클래스에 `middleware` 메서드를 구현하고 해당 미들웨어 인스턴스를 반환하면 됩니다. `make:job` Artisan 명령어로 생성한 기본 잡 클래스에는 `middleware` 메서드가 없으니 직접 추가해야 합니다:

```php
use App\Jobs\Middleware\RateLimited;

/**
 * 이 잡이 통과해야 할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited];
}
```

> [!NOTE]
> 잡 미들웨어는 큐에 들어가는 이벤트 리스너, 메일 발송, 알림 등에도 지정할 수 있습니다.

<a name="rate-limiting"></a>
### 속도 제한(Rate Limiting)

Laravel에는 자체적으로 잡 속도 제한 미들웨어도 포함되어 있습니다. 라우트 속도 제한과 [유사하게](/docs/master/routing#defining-rate-limiters), 잡 속도 제한기는 `RateLimiter` 파사드의 `for` 메서드로 정의할 수 있습니다.

예를 들어, 일반 사용자에게는 시간당 한 번만 백업을 허용하고, 프리미엄 고객에게는 제한을 두지 않으려면 다음과 같이 작성할 수 있습니다. 이는 일반적으로 `AppServiceProvider`의 `boot` 메서드에 작성합니다:

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

위에서는 시간당 1회를 제한했지만, `perMinute` 메서드를 사용하면 분 단위도 쉽게 지정할 수 있습니다. `by` 메서드로 사용자별 등 특정 단위별로 구분할 수도 있습니다:

```php
return Limit::perMinute(50)->by($job->user->id);
```

정의한 속도 제한을 잡에 적용하려면, `Illuminate\Queue\Middleware\RateLimited` 미들웨어를 사용하면 됩니다. 제한에 걸릴 경우, 잡은 적절한 지연과 함께 다시 큐에 올라가며, 이 과정에서 `attempts`(시도 횟수)가 증가하므로, 잡 클래스의 `tries`와 `maxExceptions`를 적절히 조정해야 할 수도 있습니다. 아니면, [`retryUntil` 메서드](#time-based-attempts)로 잡의 만료 시간을 설정할 수도 있습니다.

재시도를 원하지 않을 때는 `dontRelease` 메서드를 사용합니다:

```php
/**
 * 이 잡이 통과해야 할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new RateLimited('backups'))->dontRelease()];
}
```

> [!NOTE]
> Redis를 사용할 경우, `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어를 활용하면 더 효율적인 동작이 가능합니다.

<a name="preventing-job-overlaps"></a>
### 잡 중복 처리 방지

Laravel은 `Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어로, 임의의 키를 기준으로 잡의 중복 실행을 막을 수 있습니다. 예를 들어, 동일 사용자 ID에 대해 신용 등급 계산 잡이 동시에 여러 개 처리되지 않도록 하려면 다음과 같이 지정할 수 있습니다:

```php
use Illuminate\Queue\Middleware\WithoutOverlapping;

/**
 * 이 잡이 통과해야 할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new WithoutOverlapping($this->user->id)];
}
```

중복 잡은 다시 큐에 올려지며(릴리즈), 지연 시간을 지정할 수도 있습니다:

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->releaseAfter(60)];
}
```

다시 큐에 올리지 않고 즉시 삭제하려면 `dontRelease` 메서드를 사용하세요:

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->dontRelease()];
}
```

이 미들웨어는 Laravel의 원자적 락 기능을 이용합니다. 예기치 않게 잡이 실패하거나 타임아웃 날 경우 락이 남아있을 수도 있는데, `expireAfter` 메서드로 락 만료시간을 지정할 수 있습니다. 아래는 3분 후 락이 해제되도록 지정한 예시입니다:

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->expireAfter(180)];
}
```

> [!WARNING]
> `WithoutOverlapping` 미들웨어는 [락을 지원하는 캐시 드라이버](/docs/master/cache#atomic-locks)이어야만 동작합니다.

<a name="sharing-lock-keys"></a>
#### 잡 클래스 간 락 키 공유

기본적으로, `WithoutOverlapping` 미들웨어는 같은 클래스의 잡에만 적용됩니다. 만약 서로 다른 잡 클래스여도 동일한 락 키로 중복 실행을 막으려면, `shared` 메서드를 사용합니다:

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

Laravel의 `Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어를 사용하면, 잡이 예외를 반복해서 발생시킬 경우 일정 횟수 이후부터 지정된 시간 동안 대기시킬 수 있습니다. 이는 불안정한 외부 서비스와 통신하는 잡에 유용합니다.

예를 들어, 외부 API와 통신하는 잡이 10회 연속 예외를 던질 경우, 5분간 대기하도록 다음과 같이 지정할 수 있습니다:

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

첫 번째 인자는 예외 허용 횟수, 두 번째는 쓰로틀링 시 대기 시간(초)입니다. 예외 허용 횟수에 도달하지 않은 실패에 대해서는 바로 재시도되며, `backoff` 메서드로 실패 시 대기 시간도 커스터마이즈할 수 있습니다:

```php
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 5 * 60))->backoff(5)];
}
```

미들웨어 내부에서 잡 클래스명이 캐시 키로 사용됩니다. 여러 잡이 동일한 백엔드와 통신한다면 `by` 메서드로 동일한 버킷을 공유할 수도 있습니다:

```php
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->by('key')];
}
```

예외 종류에 따라 쓰로틀링 동작을 제한하려면 `when` 메서드에 조건을 클로저로 전달하세요:

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

잡에서 발생한 예외를 앱의 예외 핸들러로 리포트하려면, `report` 메서드도 사용할 수 있습니다:

```php
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->report(
        fn (Throwable $throwable) => $throwable instanceof HttpClientException
    )];
}
```

> [!NOTE]
> Redis 사용 시는 `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어가 더 효율적입니다.

<a name="skipping-jobs"></a>
### 잡 건너뛰기(Skip)

`Skip` 미들웨어를 사용하면 잡의 비즈니스 로직을 수정하지 않고도, 조건에 따라 잡을 건너뛰거나 삭제할 수 있습니다. `Skip::when`은 조건이 true이면 잡을 삭제하고, `Skip::unless`는 false일 때 잡을 삭제합니다:

```php
use Illuminate\Queue\Middleware\Skip;

public function middleware(): array
{
    return [
        Skip::when($someCondition),
    ];
}
```

더 복잡한 조건이 필요하다면, 클로저를 이용할 수도 있습니다:

```php
public function middleware(): array
{
    return [
        Skip::when(function (): bool {
            return $this->shouldSkip();
        }),
    ];
}
```

<!-- 이하 내용은 동일한 방식으로 계속 번역되어야 하며, 이후 요청 시 이어서 제공됩니다. -->