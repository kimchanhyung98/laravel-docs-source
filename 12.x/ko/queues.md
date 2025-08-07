# 큐 (Queues)

- [소개](#introduction)
    - [커넥션과 큐의 차이](#connections-vs-queues)
    - [드라이버별 주의 사항 및 필요 조건](#driver-prerequisites)
- [잡 생성하기](#creating-jobs)
    - [잡 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [고유 잡(Unique Jobs)](#unique-jobs)
    - [암호화된 잡](#encrypted-jobs)
- [잡 미들웨어](#job-middleware)
    - [속도 제한(Rate Limiting)](#rate-limiting)
    - [잡 중복 실행 방지](#preventing-job-overlaps)
    - [예외의 제어적 제한(Throttling Exceptions)](#throttling-exceptions)
    - [잡 건너뛰기](#skipping-jobs)
- [잡 디스패치(Dispatch)하기](#dispatching-jobs)
    - [딜레이(Delayed) 디스패치](#delayed-dispatching)
    - [동기적(Synchronous) 디스패치](#synchronous-dispatching)
    - [잡 & 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [잡 체이닝(Chaining)](#job-chaining)
    - [큐와 커넥션 커스터마이징](#customizing-the-queue-and-connection)
    - [최대 시도 횟수 / 타임아웃 값 지정](#max-job-attempts-and-timeout)
    - [에러 핸들링](#error-handling)
- [잡 배치(Job Batching)](#job-batching)
    - [배치 가능한 잡 정의](#defining-batchable-jobs)
    - [배치 디스패치](#dispatching-batches)
    - [체인과 배치](#chains-and-batches)
    - [잡을 배치에 추가](#adding-jobs-to-batches)
    - [배치 조회](#inspecting-batches)
    - [배치 취소](#cancelling-batches)
    - [배치 실패](#batch-failures)
    - [배치 레코드 정리(Pruning)](#pruning-batches)
    - [DynamoDB에 배치 저장](#storing-batches-in-dynamodb)
- [클로저 큐잉](#queueing-closures)
- [큐 워커 실행](#running-the-queue-worker)
    - [`queue:work` 명령어](#the-queue-work-command)
    - [큐 우선순위(Priority)](#queue-priorities)
    - [큐 워커와 배포](#queue-workers-and-deployment)
    - [잡 만료와 타임아웃](#job-expirations-and-timeouts)
- [Supervisor 설정](#supervisor-configuration)
- [실패한 잡 처리](#dealing-with-failed-jobs)
    - [실패한 잡 후 처리](#cleaning-up-after-failed-jobs)
    - [실패한 잡 재시도](#retrying-failed-jobs)
    - [누락된 모델 무시](#ignoring-missing-models)
    - [실패한 잡 레코드 정리(Pruning)](#pruning-failed-jobs)
    - [DynamoDB에 실패한 잡 저장](#storing-failed-jobs-in-dynamodb)
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

웹 애플리케이션을 개발하다 보면, 업로드된 CSV 파일을 파싱하고 저장하는 작업과 같이 일반적인 웹 요청 도중 처리하기에는 너무 오래 걸리는 작업이 있을 수 있습니다. 다행히 Laravel에서는 백그라운드에서 처리될 수 있는 큐 잡(Queue Job)을 간편하게 만들 수 있습니다. 시간 소모가 많은 작업을 큐로 옮기면, 애플리케이션이 웹 요청에 매우 빠르게 응답할 수 있고, 사용자에게 더 나은 경험을 제공할 수 있습니다.

Laravel 큐는 다양한 큐 백엔드(예: [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 관계형 데이터베이스 등)에서 사용할 수 있는 통합 큐 API를 제공합니다.

큐와 관련된 설정은 애플리케이션의 `config/queue.php` 설정 파일에 저장됩니다. 이 파일에는 데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 등 여러 큐 드라이버에 대한 커넥션 설정 예시가 포함되어 있으며, 잡을 즉시(동기적으로) 실행하는 개발용 동기(synchronous) 드라이버도 있습니다. 또한, 큐 잡을 모두 폐기하는 `null` 드라이버도 포함되어 있습니다.

> [!NOTE]
> Laravel은 이제 Redis 기반 큐에 사용할 수 있는 아름다운 대시보드와 설정 시스템인 Horizon을 제공합니다. 자세한 내용은 [Horizon 문서](/docs/12.x/horizon)를 참고하세요.

<a name="connections-vs-queues"></a>
### 커넥션과 큐의 차이

Laravel 큐를 사용하기 전에 "커넥션(Connection)"과 "큐(Queue)"의 차이를 이해하는 것이 중요합니다. `config/queue.php` 파일의 `connections` 배열은 Amazon SQS, Beanstalk, Redis와 같은 백엔드 큐 서비스에 대한 커넥션을 정의합니다. 하지만 하나의 큐 커넥션에는 여러 "큐"가 존재할 수 있고, 이들은 일종의 잡 스택 또는 분리된 작업 대기열로 생각할 수 있습니다.

각 커넥션 설정 예시에는 `queue` 속성이 포함되어 있는데, 이는 해당 커넥션에서 기본적으로 사용될 큐를 의미합니다. 즉, 어떤 잡을 큐를 명시적으로 지정하지 않고 디스패치하면, 해당 커넥션 설정의 `queue` 속성에 정의된 큐에 잡이 추가됩니다:

```php
use App\Jobs\ProcessPodcast;

// 이 잡은 기본 커넥션의 기본 큐에 전송됩니다.
ProcessPodcast::dispatch();

// 이 잡은 기본 커넥션의 "emails" 큐에 전송됩니다.
ProcessPodcast::dispatch()->onQueue('emails');
```

일부 애플리케이션은 단순히 하나의 큐만 사용할 수도 있지만, 여러 큐를 활용하면 잡의 처리 방법을 우선순위나 용도에 따라 나누고 조절할 수 있습니다. 예를 들어, `high` 큐에 삽입된 잡을 우선 처리하려면, 워커를 아래와 같이 실행할 수 있습니다:

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버별 주의 사항 및 필요 조건

<a name="database"></a>
#### 데이터베이스(Database)

`database` 큐 드라이버를 사용하려면 잡을 저장할 데이터베이스 테이블이 필요합니다. Laravel의 `0001_01_01_000002_create_jobs_table.php` [마이그레이션](/docs/12.x/migrations)에 기본적으로 포함되어 있지만, 만약 해당 마이그레이션이 없다면, 아래 Artisan 명령어로 생성할 수 있습니다:

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면, 먼저 `config/database.php` 파일에서 Redis 데이터베이스 커넥션을 설정해야 합니다.

> [!WARNING]
> `redis` 큐 드라이버에서는 `serializer` 및 `compression` Redis 옵션이 지원되지 않습니다.

**Redis 클러스터**

만약 Redis 큐 커넥션이 [Redis 클러스터](https://redis.io/docs/latest/operate/rs/databases/durability-ha/clustering)를 사용한다면, 큐 이름에 반드시 [키 해시 태그(key hash tag)](https://redis.io/docs/latest/develop/using-commands/keyspace/#hashtags)를 포함해야 합니다. 이를 통해 해당 큐의 모든 Redis 키를 동일한 해시 슬롯에 할당할 수 있습니다:

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

Redis 큐 사용 시, `block_for` 옵션 값을 통해 잡이 도착할 때까지 드라이버가 얼마나 대기할지 지정할 수 있습니다. 이 값을 조정하면 불필요하게 계속 Redis 데이터베이스를 폴링하는 것보다 효율적으로 큐를 처리할 수 있습니다. 예를 들어, 값을 `5`로 설정하면, 새로운 잡이 도착하기를 5초 동안 블로킹합니다:

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
> `block_for` 값을 `0`으로 설정하면, 워커는 잡이 도착할 때까지 무한정 블로킹합니다. 이 경우, `SIGTERM`와 같은 시스템 신호도 잡이 처리될 때까지 반영되지 않습니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 필요 조건

아래는 각 큐 드라이버에서 필요한 의존성 패키지입니다. Composer 패키지 관리자를 통해 설치할 수 있습니다:

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

기본적으로 애플리케이션의 모든 큐 잡 클래스는 `app/Jobs` 디렉토리에 저장됩니다. 만약 해당 디렉토리가 없다면, `make:job` Artisan 명령어를 실행할 때 자동으로 생성됩니다:

```shell
php artisan make:job ProcessPodcast
```

생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하며, 이는 Laravel에게 해당 잡을 비동기적으로 큐에 삽입해야 함을 알립니다.

> [!NOTE]
> 잡 스텁(stub)은 [스텁 퍼블리싱](/docs/12.x/artisan#stub-customization)을 통해 커스터마이즈 할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조

잡 클래스는 일반적으로 매우 단순하며, 큐에서 잡이 처리될 때 호출되는 `handle` 메서드만 포함합니다. 예시로 팟캐스트 퍼블리싱 서비스를 운영하며, 업로드된 팟캐스트 파일을 퍼블리싱 이전에 처리하는 잡 클래스를 보겠습니다:

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

위 예시에서는 [Eloquent 모델](/docs/12.x/eloquent)을 큐 잡의 생성자에서 직접 받아올 수 있음을 볼 수 있습니다. 잡에서 사용하는 `Queueable` 트레잇 덕분에, Eloquent 모델과 해당 관계 데이터도 직렬화/역직렬화가 자동으로 처리됩니다.

큐 잡이 생성자에서 Eloquent 모델을 받는 경우, 모델 식별자만 큐에 직렬화되어 저장됩니다. 잡이 실제로 처리될 때, 큐 시스템은 데이터베이스에서 전체 모델 인스턴스 및 관계 데이터를 다시 불러옵니다. 이 방식을 통해 큐 드라이버로 전송되는 페이로드 크기를 크게 줄일 수 있습니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드 의존성 주입

큐에서 잡이 처리될 때 `handle` 메서드가 실행되며, 해당 메서드의 인자로 타입힌트한 경우 Laravel [서비스 컨테이너](/docs/12.x/container)가 자동으로 의존성을 주입합니다.

`handle` 메서드에 의존성 주입이 어떻게 이루어지는지 완전히 제어하려면 컨테이너의 `bindMethod` 메서드를 사용할 수 있습니다. 이 메서드는 일반적으로 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 호출하는 것이 좋습니다:

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 원시 바이너리 데이터(예: 이미지 등)는 큐에 삽입하기 전에 반드시 `base64_encode` 함수를 거쳐서 전달해야 합니다. 그렇지 않으면 잡이 JSON으로 올바르게 직렬화되지 않을 수 있습니다.

<a name="handling-relationships"></a>
#### 큐잉된 모델 관계(Queued Relationships)

큐에 잡을 삽입할 때 Eloquent 모델의 관계까지 직렬화되기 때문에, 직렬화된 잡 문자열이 매우 커질 수 있습니다. 또한, 잡이 역직렬화될 때 관계가 데이터베이스에서 전체로 다시 불러와집니다. 이때 큐잉 과정에서 관계에 적용한 제약 조건(쿼리 스코프 등)은 복원되지 않습니다. 특정 관계의 일부만 사용하려면 잡 내부에서 직접 관계에 제약을 다시 걸어야 합니다.

또는, 직렬화 시 관계를 제외하려면, 속성을 설정할 때 모델의 `withoutRelations` 메서드를 호출하면 됩니다. 이 메서드는 관계가 없는 모델 인스턴스를 반환합니다:

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

PHP 생성자 프로퍼티 프로모션을 사용하는 경우 Eloquent 모델의 관계를 직렬화하지 않으려면 `WithoutRelations` 어트리뷰트를 사용할 수 있습니다:

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

잡이 하나의 모델이 아닌 여러 Eloquent 모델 컬렉션이나 배열을 받는 경우, 역직렬화 및 실행 시 각 모델의 관계는 복원되지 않습니다. 이는 대량 모델 처리 시 리소스 과다 사용을 방지하기 위함입니다.

<a name="unique-jobs"></a>
### 고유 잡(Unique Jobs)

> [!WARNING]
> 고유 잡은 [락(lock)](/docs/12.x/cache#atomic-locks) 기능을 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 원자적 락을 지원합니다. 그리고 고유 잡 제약은 배치 내의 잡에는 적용되지 않습니다.

특정 잡이 한 번에 하나만 큐에 존재하도록 강제하고 싶을 때가 있습니다. 이를 위해 잡 클래스에 `ShouldBeUnique` 인터페이스를 구현합니다. 별도의 메서드를 추가로 구현할 필요는 없습니다:

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

위 예시에서 `UpdateSearchIndex` 잡은 고유 잡이므로, 동일한 잡 인스턴스가 아직 처리 중이라면 추가로 디스패치되지 않습니다.

특정한 "키"를 사용해 잡의 고유성을 부여하거나, 특정 시간 이후 고유성이 해제되도록 하고 싶다면, 잡 클래스에 `uniqueId` 및 `uniqueFor` 속성이나 메서드를 정의할 수 있습니다:

```php
<?php

use App\Models\Product;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    /**
     * The product instance.
     *
     * @var \App\Product
     */
    public $product;

    /**
     * 잡의 고유 락 해제까지 대기할 초(second) 수
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

위 예시에서는 `UpdateSearchIndex` 잡이 product ID 기준으로 고유하게 됩니다. 즉, 동일한 product ID로 잡을 디스패치하면 기존 잡이 완료될 때까지 무시됩니다. 또한, 기존 잡이 1시간(3600초) 이내에 처리되지 않으면 고유 락이 해제되어, 동일 키로 새 잡을 큐에 올릴 수 있습니다.

> [!WARNING]
> 여러 웹 서버 혹은 컨테이너에서 잡을 디스패치하는 경우, 모든 서버가 동일한 중앙 캐시 서버를 사용해야 Laravel이 잡의 고유 여부를 정확히 판단할 수 있습니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 처리 시작 전까지 잡 고유성 유지

기본적으로 고유 잡은 처리 완료 또는 재시도 횟수 초과 시 "언락"됩니다. 하지만 잡이 실제로 처리되기 전까지만 잠시 고유해야 하는 경우 `ShouldBeUniqueUntilProcessing` 인터페이스를 구현하세요:

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
#### 고유 잡 락(Unique Job Locks)

내부적으로 `ShouldBeUnique` 잡이 디스패치되면, Laravel은 `uniqueId` 키로 [락(lock)](/docs/12.x/cache#atomic-locks)을 획득하려고 시도합니다. 락을 획득하지 못하면 잡은 디스패치되지 않습니다. 이 락은 잡이 처리 완료하거나 재시도 횟수를 모두 소진하면 해제됩니다. Laravel은 기본적으로 기본 캐시 드라이버를 사용해 락을 획득합니다. 특정 캐시 드라이버를 사용하고 싶다면 `uniqueVia` 메서드를 잡 클래스에 정의하면 됩니다:

```php
use Illuminate\Contracts\Cache\Repository;
use Illuminate\Support\Facades\Cache;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...

    /**
     * 고유 잡 락에 사용할 캐시 드라이버 반환
     */
    public function uniqueVia(): Repository
    {
        return Cache::driver('redis');
    }
}
```

> [!NOTE]
> 단순히 잡 동시 실행 제한만 필요하다면 [WithoutOverlapping](/docs/12.x/queues#preventing-job-overlaps) 잡 미들웨어를 사용하세요.

<a name="encrypted-jobs"></a>
### 암호화된 잡(Encrypted Jobs)

Laravel에서는 잡 데이터의 프라이버시와 무결성을 [암호화](/docs/12.x/encryption)를 통해 보장할 수 있습니다. 사용 방법은 잡 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하면 됩니다. 이렇게 하면 Laravel이 큐에 올리기 전에 잡을 자동으로 암호화합니다:

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

잡 미들웨어를 통해 큐 잡의 실행을 감싸는 커스텀 로직을 정의할 수 있으며, 각 잡의 코드에 반복적인 로직을 줄일 수 있습니다. 예를 들어, 아래처럼 Redis 속도 제한 기능을 활용해 5초에 한 번씩만 잡을 처리할 수 있도록 할 수도 있습니다:

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

이 코드는 작동하긴 하지만 `handle` 메서드가 Redis 속도 제한 코드로 인해 복잡해집니다. 또한, 비슷한 패턴의 잡이 많아질수록 중복 코드가 늘어납니다.

대신 속도 제한 처리를 별도 잡 미들웨어에 분리할 수 있습니다. Laravel은 잡 미들웨어의 위치에 제한을 두지 않으므로 자유롭게 원하는 위치에 정의할 수 있습니다. 예시에서는 `app/Jobs/Middleware` 디렉토리에 둘 수 있습니다:

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
                // Lock obtained...

                $next($job);
            }, function () use ($job) {
                // Could not obtain lock...

                $job->release(5);
            });
    }
}
```

라우트 미들웨어와 유사하게 잡 미들웨어도 잡 인스턴스와 다음 동작을 호출하는 콜백을 인자로 받습니다.

`make:job-middleware` Artisan 명령어로 새로운 잡 미들웨어 클래스를 생성할 수 있습니다. 잡 미들웨어는 잡 클래스의 `middleware` 메서드에 배열로 반환하여 적용합니다. 기본 잡 스캐폴딩에는 `middleware` 메서드가 없으므로 수동으로 추가해야 합니다:

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
> 잡 미들웨어는 [큐잉 이벤트 리스너](/docs/12.x/events#queued-event-listeners), [메일러블](/docs/12.x/mail#queueing-mail), [알림](/docs/12.x/notifications#queueing-notifications)에도 사용할 수 있습니다.

<a name="rate-limiting"></a>
### 속도 제한(Rate Limiting)

직접 잡 미들웨어로 속도 제한을 구현할 수도 있지만, Laravel에서 제공하는 기본 속도 제한 미들웨어가 있습니다. [라우트 속도 제한자](/docs/12.x/routing#defining-rate-limiters)와 비슷하게, 잡 용도도 `RateLimiter` 파사드의 `for` 메서드로 정의할 수 있습니다.

예를 들어, 일반 사용자는 1시간에 한 번 백업을 허용하고, 프리미엄 고객은 제한을 두지 않는 예제를 살펴보겠습니다:

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

위에서는 시간 단위 예시였지만, `perMinute` 메서드로 분 단위로도 제한할 수 있습니다. `by` 메서드에는 고객 식별자 등 원하는 값을 전달해 사용자별로 제한을 둘 수 있습니다:

```php
return Limit::perMinute(50)->by($job->user->id);
```

속도 제한자 정의 후, 잡의 `middleware`에서 `Illuminate\Queue\Middleware\RateLimited` 미들웨어를 사용할 수 있습니다. 잡이 속도 제한을 초과하면, 제한 지속 시간만큼 지연 후 큐에 다시 반환됩니다.

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

속도 제한으로 인해 잡이 반복해서 큐에 재투입될 경우, 시도 횟수(`attempts`)도 함께 증가합니다. `tries` 또는 `maxExceptions` 속성, 또는 [retryUntil 메서드](#time-based-attempts)를 적절히 조정하세요.

`releaseAfter` 메서드를 사용해 잡이 다시 시도될 때까지 대기할 초(second) 수를 지정할 수 있습니다:

```php
public function middleware(): array
{
    return [(new RateLimited('backups'))->releaseAfter(60)];
}
```

잡이 속도 제한에 걸리면 재시도하지 않도록 하려면 `dontRelease` 메서드를 사용하세요:

```php
public function middleware(): array
{
    return [(new RateLimited('backups'))->dontRelease()];
}
```

> [!NOTE]
> Redis를 사용한다면, 더 효율적인 `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어를 사용할 수 있습니다.

<a name="preventing-job-overlaps"></a>
### 잡 중복 실행 방지

Laravel에는 특정 키를 기준으로 잡이 중복 실행되지 않도록 막아주는 `Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어도 있습니다. 예를 들어, 사용자의 신용점수를 갱신하는 잡에서, 같은 사용자 ID에 대해 잡이 동시에 실행되지 않도록 할 수 있습니다:

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

동일 잡 타입이 중복되어 있으면 자동으로 잡이 큐에 다시 반환됩니다. `releaseAfter` 메서드로 재시도까지 기다릴 시간을 지정할 수 있습니다:

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->releaseAfter(60)];
}
```

중복된 잡이 아예 재시도되지 않도록 하려면 `dontRelease` 메서드를 사용하세요:

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->dontRelease()];
}
```

이 미들웨어는 Laravel의 원자적 락 기능으로 동작합니다. 가끔 잡이 예상치 못하게 실패하거나 타임아웃이 발생해 락이 해제되지 않는 경우도 있으므로, `expireAfter` 메서드로 락 만료 시간을 명시할 수 있습니다. 아래는 3분(180초) 후 락을 자동 해제하도록 설정한 예시입니다:

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->expireAfter(180)];
}
```

> [!WARNING]
> `WithoutOverlapping` 미들웨어는 [락(lock)](/docs/12.x/cache#atomic-locks) 기능을 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 드라이버에서만 지원됩니다.

<a name="sharing-lock-keys"></a>
#### 잡 클래스 간 락 키 공유

기본적으로 `WithoutOverlapping` 미들웨어는 동일 클래스의 잡만 중복 실행을 막습니다. 두 개의 서로 다른 잡 클래스가 동일 락 키를 사용하더라도 중복이 방지되지 않습니다. 여러 잡 클래스에도 키를 공유하도록 하려면 `shared` 메서드를 사용하세요:

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
### 예외의 제어적 제한(Throttling Exceptions)

`Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어를 사용하면, 잡이 반복적으로 예외를 던질 때 실행을 제한(Throttle)할 수 있습니다. 예외가 일정 횟수를 초과하면, 지정한 시간 동안 잡 실행이 지연됩니다. 이는 외부 서비스가 불안정한 경우 유용합니다.

예를 들어, 외부 API와 통신하는 잡이 연속적으로 예외를 던지는 경우 아래처럼 사용할 수 있습니다. 이때 [시간 기반 재시도](#time-based-attempts) 기능과 함께 사용하는 것이 일반적입니다.

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

첫 번째 인자는 연속 예외 허용 횟수, 두 번째는 제한(Throttle)되었을 때 재시도까지 기다릴 초(second) 수입니다. 위 예제에서는 10연속 예외 발생 시 5분 대기, 단 30분 이내만 실행됩니다.

예외 허용 횟수 이하에서는 즉시 재시도되지만, `backoff` 메서드로 해당 상황에서도 지연을 추가할 수 있습니다:

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 5 * 60))->backoff(5)];
}
```

이 미들웨어는 Laravel의 캐시 시스템을 활용해 제한을 구현하며, 잡 클래스명이 캐시 키로 사용됩니다. 동일한 외부 서비스에 여러 잡이 접근할 때, `by` 메서드로 공유 제한 버킷을 지정할 수 있습니다:

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->by('key')];
}
```

기본적으로는 모든 예외가 제한 대상입니다. `when` 메서드를 사용해 특정 예외일 때만 제한하도록 할 수 있습니다:

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

특정 예외 발생 시 잡을 완전히 삭제하려면 `deleteWhen` 메서드를 사용하세요:

```php
use App\Exceptions\CustomerDeletedException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [(new ThrottlesExceptions(2, 10 * 60))->deleteWhen(CustomerDeletedException::class)];
}
```

제한된 예외를 애플리케이션의 예외 핸들러에도 보고하려면 `report` 메서드를 사용하세요. 클로저를 인자로 전달하면, true 반환 시에만 보고합니다:

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
> Redis 사용 시에는 최적화된 `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어를 추천합니다.

<a name="skipping-jobs"></a>
### 잡 건너뛰기

`Skip` 미들웨어를 사용하면 잡의 로직을 수정하지 않고도 잡을 건너뛰거나 삭제할 수 있습니다. `Skip::when` 메서드는 조건이 참이면 잡을 삭제하고, `Skip::unless` 메서드는 조건이 거짓일 때 삭제합니다:

```php
use Illuminate\Queue\Middleware\Skip;

public function middleware(): array
{
    return [
        Skip::when($someCondition),
    ];
}
```

더 복잡한 조건이라면 클로저도 전달할 수 있습니다:

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

<!-- 이하 문서도 동일한 방식으로 번역 및 마크다운 유지 -->

(※ 답변 분량 한계로 인해 여기까지 번역합니다. 추가 요청 시 다음 부분을 이어서 제공해 드릴 수 있습니다.)