# 큐 (Queues)

- [소개](#introduction)
    - [커넥션과 큐의 차이](#connections-vs-queues)
    - [드라이버 주의사항 및 사전 준비](#driver-prerequisites)
- [잡 생성](#creating-jobs)
    - [잡 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [고유 잡](#unique-jobs)
    - [암호화된 잡](#encrypted-jobs)
- [잡 미들웨어](#job-middleware)
    - [속도 제한](#rate-limiting)
    - [잡 중복 실행 방지](#preventing-job-overlaps)
    - [예외 처리 제한(Throttling)](#throttling-exceptions)
    - [잡 건너뛰기](#skipping-jobs)
- [잡 디스패치](#dispatching-jobs)
    - [지연 디스패치](#delayed-dispatching)
    - [동기식 디스패치](#synchronous-dispatching)
    - [잡과 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [잡 체이닝](#job-chaining)
    - [큐/커넥션 커스터마이징](#customizing-the-queue-and-connection)
    - [잡 최대 시도/타임아웃 값 지정](#max-job-attempts-and-timeout)
    - [SQS FIFO 및 공정 큐](#sqs-fifo-and-fair-queues)
    - [큐 페일오버](#queue-failover)
    - [에러 핸들링](#error-handling)
- [잡 배치 처리](#job-batching)
    - [배치 가능한 잡 정의](#defining-batchable-jobs)
    - [배치 디스패치](#dispatching-batches)
    - [체인과 배치](#chains-and-batches)
    - [배치에 잡 추가](#adding-jobs-to-batches)
    - [배치 확인](#inspecting-batches)
    - [배치 취소](#cancelling-batches)
    - [배치 실패](#batch-failures)
    - [배치 정리(Pruning)](#pruning-batches)
    - [DynamoDB에 배치 저장](#storing-batches-in-dynamodb)
- [클로저 큐잉](#queueing-closures)
- [큐 워커 실행](#running-the-queue-worker)
    - [`queue:work` 명령어](#the-queue-work-command)
    - [큐 우선순위](#queue-priorities)
    - [큐 워커와 배포](#queue-workers-and-deployment)
    - [잡 만료 및 타임아웃](#job-expirations-and-timeouts)
    - [큐 워커 일시정지 및 재개](#pausing-and-resuming-queue-workers)
- [Supervisor 설정](#supervisor-configuration)
- [실패한 잡 처리](#dealing-with-failed-jobs)
    - [실패한 잡 정리](#cleaning-up-after-failed-jobs)
    - [실패한 잡 재시도](#retrying-failed-jobs)
    - [누락된 모델 무시](#ignoring-missing-models)
    - [실패한 잡 정리(Pruning)](#pruning-failed-jobs)
    - [DynamoDB에 실패 잡 저장](#storing-failed-jobs-in-dynamodb)
    - [실패 잡 저장 비활성화](#disabling-failed-job-storage)
    - [실패한 잡 이벤트](#failed-job-events)
- [큐에서 잡 비우기](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [일부 잡만 페이크로 처리하기](#faking-a-subset-of-jobs)
    - [잡 체인 테스트](#testing-job-chains)
    - [잡 배치 테스트](#testing-job-batches)
    - [잡/큐 상호작용 테스트](#testing-job-queue-interactions)
- [잡 이벤트](#job-events)

<a name="introduction"></a>
## 소개 (Introduction)

웹 애플리케이션을 개발하다 보면, 업로드된 CSV 파일을 파싱해 저장하는 것처럼 일반 웹 요청 중 처리하기에는 너무 시간이 오래 걸리는 작업들이 발생합니다. 다행히도, Laravel에서는 이러한 시간 소요가 큰 작업을 쉽게 백그라운드에서 처리할 수 있도록 큐에 잡을 생성할 수 있습니다. 이렇게 무거운 작업을 큐로 분리하면, 애플리케이션이 웹 요청에 훨씬 더 빠르게 응답할 수 있어 사용자에게 더 나은 경험을 제공합니다.

Laravel의 큐 시스템은 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 또는 관계형 데이터베이스 등 다양한 큐 백엔드에 대해 통일된 큐 API를 제공합니다.

큐 관련 설정은 애플리케이션의 `config/queue.php` 설정 파일에 저장되어 있습니다. 이 파일에서는 데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 같은 프레임워크 기본 큐 드라이버의 커넥션 설정을 볼 수 있으며, 즉시 잡을 실행하는 동기식 드라이버(개발/테스트 용도)와 큐에 쌓인 잡을 버리는 `null` 드라이버도 포함되어 있습니다.

> [!NOTE]
> Laravel Horizon은 Redis 기반 큐를 위한 아름다운 대시보드 및 설정 도구입니다. 더 자세한 정보는 [Horizon 문서](/docs/master/horizon)를 참고하세요.

<a name="connections-vs-queues"></a>
### 커넥션과 큐의 차이

Laravel 큐를 시작하기 전, "커넥션(connection)"과 "큐(queue)"의 차이를 이해하는 것이 중요합니다. `config/queue.php` 파일의 `connections` 배열은 Amazon SQS, Beanstalk, Redis처럼 백엔드 큐 서비스를 정의합니다. 단, 하나의 큐 커넥션에 여러 개의 "큐"가 존재할 수 있는데, 이는 쌓여있는 잡들의 묶음 또는 스택처럼 생각하시면 됩니다.

각 커넥션 예제에는 `queue` 속성이 포함되어 있는데, 이는 해당 커넥션으로 전송되는 잡의 기본 큐를 의미합니다. 즉, 디스패치 시 특정 큐를 명시하지 않으면, 해당 커넥션 설정의 `queue`에 정의된 큐로 잡이 쌓입니다:

```php
use App\Jobs\ProcessPodcast;

// 이 잡은 기본 커넥션의 기본 큐로 전송됩니다.
ProcessPodcast::dispatch();

// 이 잡은 기본 커넥션의 "emails" 큐로 전송됩니다.
ProcessPodcast::dispatch()->onQueue('emails');
```

어떤 애플리케이션은 큐를 분리할 필요 없이 하나의 큐만 사용해도 충분합니다. 하지만 여러 개의 큐를 활용해 다양한 작업을 우선순위 별로 처리하고 싶을 때, Laravel 큐 워커가 우선순위별로 큐를 처리할 수 있도록 지원합니다. 예를 들어, `high`라는 높은 우선순위 큐가 있다면, 아래와 같이 워커를 실행할 수 있습니다:

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버 주의사항 및 사전 준비 (Driver Notes and Prerequisites)

<a name="database"></a>
#### 데이터베이스

`database` 큐 드라이버를 사용하려면 잡을 저장할 데이터베이스 테이블이 필요합니다. 일반적으로 Laravel의 기본 `0001_01_01_000002_create_jobs_table.php` [마이그레이션](/docs/master/migrations)에 포함되어 있습니다. 만약 이 마이그레이션이 없다면, `make:queue-table` Artisan 명령어로 직접 생성하고 마이그레이션을 적용하시기 바랍니다:

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면, `config/database.php` 파일에서 Redis 데이터베이스 커넥션을 설정해야 합니다.

> [!WARNING]
> `redis` 큐 드라이버는 Redis의 `serializer`와 `compression` 옵션을 지원하지 않습니다.

<a name="redis-cluster"></a>
##### Redis 클러스터

Redis 큐 커넥션이 [Redis 클러스터](https://redis.io/docs/latest/operate/rs/databases/durability-ha/clustering)를 사용하는 경우, [key hash tag](https://redis.io/docs/latest/develop/using-commands/keyspace/#hashtags)를 큐 이름에 포함시켜야 합니다. 그래야 한 큐의 모든 키들이 동일한 해시 슬롯에 배치됩니다:

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

Redis 큐를 사용할 때 `block_for` 설정을 통해 잡이 나올 때까지 워커가 대기하는 시간을 지정할 수 있습니다. 이 값에 따라 Redis를 불필요하게 반복 조회하는 비효율을 줄일 수 있습니다. 예를 들어, `5`로 설정하면, 잡이 생길 때까지 5초 동안 대기하게 됩니다:

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
> `block_for`를 `0`으로 설정하면 워커는 잡이 생길 때까지 무한히 대기하게 됩니다. 이 경우, 다음 잡이 처리될 때까지 `SIGTERM` 같은 시그널이 전달되지 않습니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 사전 준비

아래 큐 드라이버를 사용하려면 해당 의존성을 Composer로 설치해야 합니다:

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

기본적으로 애플리케이션의 큐 가능한(jobable) 잡들은 `app/Jobs` 디렉토리에 저장됩니다. 만약 이 디렉토리가 없다면, `make:job` Artisan 명령어를 실행할 때 자동으로 생성됩니다:

```shell
php artisan make:job ProcessPodcast
```

이렇게 생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하며, 이로써 Laravel은 해당 잡이 큐에서 비동기적으로 처리되어야 함을 인식합니다.

> [!NOTE]
> 잡 스텁(Stubs)은 [스텁 퍼블리싱](/docs/master/artisan#stub-customization) 기능으로 커스터마이즈할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조

잡 클래스는 매우 단순하며, 큐에서 잡이 처리될 때 호출되는 `handle` 메서드만 포함하는 경우가 일반적입니다. 예시로, 팟캐스트 발행 서비스를 만든다고 가정하고, 업로드된 팟캐스트 파일을 발행 전에 처리해야 할 때의 잡 클래스를 살펴보겠습니다:

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
     * 새로운 잡 인스턴스 생성자.
     */
    public function __construct(
        public Podcast $podcast,
    ) {}

    /**
     * 잡 실행.
     */
    public function handle(AudioProcessor $processor): void
    {
        // 업로드된 팟캐스트 처리...
    }
}
```

위 예시처럼, [Eloquent 모델](/docs/master/eloquent)을 잡의 생성자에 직접 주입할 수 있습니다. 잡에서 사용하는 `Queueable` 트레잇 덕분에, Eloquent 모델과 로드된 연관관계 데이터도 큐에 직렬화/역직렬화가 자연스럽게 처리됩니다.

큐에 Eloquent 모델이 주입될 경우, 큐에는 실제 모델 전체가 아니라 해당 모델의 식별자만 직렬화됩니다. 잡이 처리될 때는 잡 시스템이 데이터베이스에서 모델 전체와 연관관계를 다시 가져옵니다. 이런 모델 직렬화 접근 방식은 큐 드라이버로 전송되는 잡의 페이로드를 최소화할 수 있게 해줍니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드의 의존성 주입

`handle` 메서드는 큐에서 잡이 처리될 때 호출됩니다. 이 메서드에서 의존성을 타입 힌트로 선언하면, Laravel [서비스 컨테이너](/docs/master/container)가 자동으로 주입해 줍니다.

만약 컨테이너의 의존성 주입 방식을 완전히 제어하고 싶다면, `bindMethod` 메서드를 사용할 수 있습니다. 이 메서드는 잡과 컨테이너를 콜백으로 받아 직접 `handle` 메서드를 호출할 수 있도록 해줍니다. 보통은 `App\Providers\AppServiceProvider`의 `boot`에서 아래처럼 설정합니다:

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 이진 데이터(원시 이미지 데이터 등)는 잡에 전달하기 전에 반드시 `base64_encode` 함수로 인코딩해야 합니다. 그러지 않으면 큐에 잡을 JSON으로 직렬화하는 과정에서 문제가 발생할 수 있습니다.

<a name="handling-relationships"></a>
#### 큐잉된 연관관계(Queued Relationships)

Eloquent 모델의 연관관계도 모두 함께 직렬화되기 때문에, 잡의 직렬 문자열이 클 수 있습니다. 또한 잡이 역직렬화되어 다시 데이터베이스에서 모델과 연관관계를 가져올 때, 직렬화 이전에 적용했던 연관관계 조건은 무시되고 전체가 로드됩니다. 따라서 연관관계의 일부만 필요하다면 잡 내에서 직접 재제한(필터)해야 합니다.

또는, 직렬화 시 연관관계가 저장되지 않도록 모델의 속성에 값을 대입할 때 `withoutRelations` 메서드를 사용할 수 있습니다. 이 메서드는 연관관계가 제거된 모델 인스턴스를 반환합니다:

```php
/**
 * 새로운 잡 인스턴스 생성자.
 */
public function __construct(
    Podcast $podcast,
) {
    $this->podcast = $podcast->withoutRelations();
}
```

[PHP 생성자 프로퍼티 프로모션](https://www.php.net/manual/en/language.oop5.decon.php#language.oop5.decon.constructor.promotion)을 사용하는 경우, Eloquent 모델의 연관관계를 직렬화하지 않으려면 `WithoutRelations` 속성을 사용할 수 있습니다:

```php
use Illuminate\Queue\Attributes\WithoutRelations;

/**
 * 새로운 잡 인스턴스 생성자.
 */
public function __construct(
    #[WithoutRelations]
    public Podcast $podcast,
) {}
```

모든 모델의 연관관계를 직렬화하지 않으려면, 개별 속성마다가 아니라 클래스 전체에 `WithoutRelations` 속성을 붙이면 됩니다:

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
     * 새로운 잡 인스턴스 생성자.
     */
    public function __construct(
        public Podcast $podcast,
        public DistributionPlatform $platform,
    ) {}
}
```

단, 단일 모델이 아닌 Eloquent 모델 컬렉션 또는 배열을 잡에 주입하면, 해당 컬렉션 내의 모델은 잡 실행 시 역직렬화되어도 연관관계가 복원되지 않습니다. 이는 대량의 모델을 다루는 잡의 리소스 낭비를 막기 위한 조치입니다.

<a name="unique-jobs"></a>
### 고유 잡 (Unique Jobs)

> [!WARNING]
> 고유 잡은 [락 지원](/docs/master/cache#atomic-locks)이 가능한 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 드라이버가 atomic lock을 지원합니다.

> [!WARNING]
> 고유 잡 제약 조건은 배치 잡 내에서는 적용되지 않습니다.

특정 잡이 큐에 한 번만 쌓이도록 보장하려면, 잡 클래스에 `ShouldBeUnique` 인터페이스를 구현하면 됩니다. 별도의 추가 메서드는 필요 없습니다:

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

위 예시의 `UpdateSearchIndex` 잡은 고유 잡입니다. 동일한 잡이 이미 큐에 있고 아직 처리 중이라면, 새로운 잡은 디스패치되지 않습니다.

잡의 고유성을 특정 "키"로 구분하거나, 고유성이 일정 시간 후 해제되도록 하려면, 잡 클래스에 `uniqueId`와 `uniqueFor` 프로퍼티/메서드를 정의합니다:

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
     * 잡의 고유 락이 해제되는 시간(초).
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

위 예시에서는 상품 ID 기준으로 잡이 고유합니다. 그래서 동일한 상품 ID의 잡이 큐에 있으면 추가로 디스패치되지 않습니다. 기존 잡이 1시간 안에 처리되지 않으면 락이 해제되고, 이후 같은 키의 잡이 디스패치될 수 있습니다.

> [!WARNING]
> 여러 대의 웹 서버나 컨테이너에서 잡을 디스패치한다면, 모든 서버가 동일한 캐시 서버를 사용하도록 해야 Laravel이 정확하게 잡의 고유성을 판단할 수 있습니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 잡 처리 시작까지 고유성 유지하기

기본적으로 고유 잡은 처리 완료 또는 재시도 횟수 초과 시 "언락"됩니다. 잡이 실제로 처리되기 직전에 바로 언락되도록 하려면, `ShouldBeUnique` 대신 `ShouldBeUniqueUntilProcessing` 인터페이스를 구현하세요:

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
#### 고유 잡 락

내부적으로, `ShouldBeUnique` 잡 디스패치 시 Laravel은 `uniqueId` 키로 [락](/docs/master/cache#atomic-locks)을 시도합니다. 이미 락이 잡힌 경우 잡은 디스패치되지 않습니다. 락은 잡이 성공하거나 재시도를 모두 소진하면 해제됩니다. Laravel은 기본적으로 기본 캐시 드라이버를 사용하지만, 별도 드라이버로 락을 잡으려면 아래처럼 `uniqueVia` 메서드를 정의하면 됩니다:

```php
use Illuminate\Contracts\Cache\Repository;
use Illuminate\Support\Facades\Cache;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...

    /**
     * 고유 잡 락에 사용할 캐시 드라이버 반환.
     */
    public function uniqueVia(): Repository
    {
        return Cache::driver('redis');
    }
}
```

> [!NOTE]
> 잡의 동시 실행만 제한하려면 [WithoutOverlapping](/docs/master/queues#preventing-job-overlaps) 잡 미들웨어를 사용하세요.

<a name="encrypted-jobs"></a>
### 암호화된 잡 (Encrypted Jobs)

Laravel은 잡의 데이터 개인정보와 무결성을 [암호화](/docs/master/encryption)로 보장할 수 있습니다. 설정은 간단하게 `ShouldBeEncrypted` 인터페이스를 잡 클래스에 적용하면 됩니다. 이렇게 하면 잡이 큐에 올라가기 전 자동으로 암호화됩니다:

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

잡 미들웨어는 큐잉된 잡 실행 시 커스텀 로직을 감싸서, 잡 클래스 내부의 반복되는 코드(보일러플레이트)를 줄여줍니다. 예를 들어, 아래는 Laravel의 Redis 속도 제한 기능으로 5초마다 잡 하나씩만 처리하도록 `handle` 메서드에서 직접 제어한 예입니다:

```php
use Illuminate\Support\Facades\Redis;

/**
 * 잡 실행.
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

위 방식은 작동하지만, 잡의 비즈니스 로직과 속도 제한 코드가 뒤섞이며 지저분해집니다. 이런 중복을 없애고자 잡 미들웨어를 별도로 정의할 수 있습니다:

```php
<?php

namespace App\Jobs\Middleware;

use Closure;
use Illuminate\Support\Facades\Redis;

class RateLimited
{
    /**
     * 큐잉된 잡을 처리.
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

이처럼 [라우트 미들웨어](/docs/master/middleware)와 같이, 잡 미들웨어도 처리 중인 잡과 다음 처리를 위한 콜백을 인자로 받습니다.

`make:job-middleware` Artisan 명령어로 새 잡 미들웨어 클래스를 생성할 수 있습니다. 생성된 미들웨어는 잡의 `middleware` 메서드에서 반환하면 잡에 할당됩니다. 이 메서드는 기본적으로 `make:job` 명령어로 생성된 잡에 포함되어 있지 않으니, 직접 추가해야 합니다:

```php
use App\Jobs\Middleware\RateLimited;

/**
 * 잡이 통과해야 하는 미들웨어 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited];
}
```

> [!NOTE]
> 잡 미들웨어는 [큐잉된 이벤트 리스너](/docs/master/events#queued-event-listeners), [메일 발송](/docs/master/mail#queueing-mail), [알림](/docs/master/notifications#queueing-notifications)에도 할당할 수 있습니다.

<a name="rate-limiting"></a>
### 속도 제한 (Rate Limiting)

직접 속도 제한 잡 미들웨어를 작성하는 것 외에도, Laravel은 사용 가능한 속도 제한 미들웨어를 제공합니다. [라우트 속도 제한자](/docs/master/routing#defining-rate-limiters)와 유사하게, 잡 속도 제한기는 `RateLimiter` 파사드의 `for` 메서드로 정의합니다.

예를 들어, 일반 사용자는 한 시간에 한 번 데이터 백업만 가능하고, 프리미엄 고객은 무제한인 속도 제한을 구현할 수 있습니다. 아래는 `AppServiceProvider`의 `boot`에 해당 제한을 정의하는 예시입니다:

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

위에서 시간 단위 제한을 설정했습니다. 물론, `perMinute`로 분 단위 설정도 가능합니다. `by` 메서드에는 고객별로 속도 제한을 구분할 수 있도록 원하는 값을 넣을 수 있습니다:

```php
return Limit::perMinute(50)->by($job->user->id);
```

이제 속도 제한기를 잡에 `Illuminate\Queue\Middleware\RateLimited` 미들웨어로 할당해 사용할 수 있습니다. 속도 제한에 걸릴 때마다 이 미들웨어는 제한 시간만큼 잡을 다시 큐에 넣습니다:

```php
use Illuminate\Queue\Middleware\RateLimited;

/**
 * 잡이 통과해야 하는 미들웨어 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited('backups')];
}
```

잡이 재시도될 때마다 `attempts` 값이 증가하므로, 잡 클래스의 `tries`나 `maxExceptions` 설정을 조정해야 할 때가 많습니다. [retryUntil 메서드](#time-based-attempts)를 사용해 잡이 더 이상 재시도되지 않을 때까지의 시간을 정할 수도 있습니다.

`releaseAfter` 메서드로, 잡이 다시 시도될 때까지의 지연(초 단위)도 설정할 수 있습니다:

```php
/**
 * 잡이 통과해야 하는 미들웨어 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new RateLimited('backups'))->releaseAfter(60)];
}
```

만약 속도 제한에 걸렸을 때 잡을 재시도하지 않게 하려면, `dontRelease` 메서드를 사용할 수 있습니다:

```php
/**
 * 잡이 통과해야 하는 미들웨어 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new RateLimited('backups'))->dontRelease()];
}
```

<a name="rate-limiting-with-redis"></a>
#### Redis를 이용한 속도 제한

Redis 사용 시, `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어를 사용할 수 있습니다. 이 미들웨어는 Redis에 최적화되어 있습니다:

```php
use Illuminate\Queue\Middleware\RateLimitedWithRedis;

public function middleware(): array
{
    return [new RateLimitedWithRedis('backups')];
}
```

`connection` 메서드로 사용할 Redis 커넥션을 지정할 수도 있습니다:

```php
return [(new RateLimitedWithRedis('backups'))->connection('limiter')];
```

<a name="preventing-job-overlaps"></a>
### 잡 중복 실행 방지 (Preventing Job Overlaps)

Laravel은 `Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어를 통해 임의의 키 기준으로 잡의 중복 실행을 막을 수 있습니다. 예를 들어, 사용자 ID 기준으로 신용점수 업데이트 잡이 동시에 실행되지 않도록 하려면 아래처럼 미들웨어를 반환하세요:

```php
use Illuminate\Queue\Middleware\WithoutOverlapping;

/**
 * 잡이 통과해야 하는 미들웨어 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new WithoutOverlapping($this->user->id)];
}
```

중복 잡이 release 될 때마다 시도 횟수(`attempts`)가 늘어나니, `tries` 또는 `maxExceptions` 값을 상황에 맞게 조정하세요. 기본값 1로 두면, 중복 잡은 재시도되지 않습니다.

동일 타입의 중복 잡은 모두 다시 큐에 넣습니다. 딜레이를 줄 수도 있습니다:

```php
/**
 * 잡이 통과해야 하는 미들웨어 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->releaseAfter(60)];
}
```

중복 잡을 즉시 삭제하여 재시도 자체를 하지 않게 할 수도 있습니다:

```php
/**
 * 잡이 통과해야 하는 미들웨어 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->dontRelease()];
}
```

`WithoutOverlapping` 미들웨어는 Laravel의 atomic lock을 사용합니다. 잡이 갑자기 실패하거나 타임아웃으로 락 해제가 되지 않을 수도 있으니, `expireAfter`로 명시적으로 락 만료시간(예: 180초)을 설정할 수 있습니다:

```php
/**
 * 잡이 통과해야 하는 미들웨어 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->expireAfter(180)];
}
```

> [!WARNING]
> `WithoutOverlapping` 미들웨어는 락 지원이 되는 캐시 드라이버(`memcached`, `redis`, `dynamodb`, `database`, `file`, `array`)가 필요합니다.

<a name="sharing-lock-keys"></a>
#### 다른 잡 클래스 간 락 키 공유

기본적으로 `WithoutOverlapping` 미들웨어는 같은 클래스의 잡만 중복 방지합니다. 두 잡 클래스가 같은 락 키를 사용하더라도, 기본 상태에서는 서로 중복을 막지 않습니다. 클래스 간 잡이 동일 락 키로 동작하도록 하려면 `shared` 메서드를 호출하세요:

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
### 예외 처리 제한(Throttling Exceptions)

`Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어는 특정 개수 이상의 예외가 발생하면, 잡의 재시도를 일정 시간 동안 지연(throttle)할 수 있게 합니다. 이는 외부 API와 같이 불안정한 서비스와 연동하는 잡에 특히 유용합니다.

예를 들어 아래는 외부 API와 연동하는 잡에서 10번 예외가 발생할 때마다 5분간 재시도를 지연하고, 30분 안에 모두 완료되어야 하는 예시입니다:

```php
use DateTime;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡이 통과해야 하는 미들웨어 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new ThrottlesExceptions(10, 5 * 60)];
}

/**
 * 잡의 타임아웃 시각 결정.
 */
public function retryUntil(): DateTime
{
    return now()->plus(minutes: 30);
}
```

생성자의 첫 인자는 예외 발생 허용 횟수, 두 번째 인자는 일단 제한되었을 때 재시도까지 대기할 시간(초)입니다.

예외가 발생했지만 제한 횟수 미만일 때는 바로 재시도합니다. `backoff` 메서드로 예외 발생 후 딜레이(분)를 줄 수 있습니다:

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡이 통과해야 하는 미들웨어 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 5 * 60))->backoff(5)];
}
```

기본적으로 잡 클래스명으로 캐시 키를 사용합니다. 여러 잡이 같은 externo 서비스와 연동한다면, `by` 메서드로 동일 버킷에서 제한하도록 할 수 있습니다:

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡이 통과해야 하는 미들웨어 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->by('key')];
}
```

기본적으로 모든 예외가 제한됩니다. `when` 메서드를 사용해 특정 상황에서만 제한할 수 있습니다:

```php
use Illuminate\Http\Client\HttpClientException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡이 통과해야 하는 미들웨어 반환.
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

`when`과 달리, `deleteWhen` 메서드는 특정 예외 발생 시 잡을 큐에서 완전히 삭제합니다:

```php
use App\Exceptions\CustomerDeletedException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡이 통과해야 하는 미들웨어 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(2, 10 * 60))->deleteWhen(CustomerDeletedException::class)];
}
```

예외 쓰로틀 상황도 애플리케이션 예외 핸들러로 리포트하려면, `report` 메서드로 지정하세요. 클로저를 사용하면 특정 조건에서만 리포트할 수 있습니다:

```php
use Illuminate\Http\Client\HttpClientException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡이 통과해야 하는 미들웨어 반환.
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

<a name="throttling-exceptions-with-redis"></a>
#### Redis에서 Throttling Exceptions

Redis를 쓰는 경우, `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어가 Redis 환경에 최적화되어 있습니다:

```php
use Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis;

public function middleware(): array
{
    return [new ThrottlesExceptionsWithRedis(10, 10 * 60)];
}
```

`connection` 메서드로 사용할 Redis 커넥션을 지정할 수 있습니다:

```php
return [(new ThrottlesExceptionsWithRedis(10, 10 * 60))->connection('limiter')];
```

<a name="skipping-jobs"></a>
### 잡 건너뛰기 (Skipping Jobs)

`Skip` 미들웨어로 별도의 코드 변경 없이 특정 조건에서 잡을 건너뛰거나 삭제할 수 있습니다. `Skip::when`은 조건이 참일 때 잡을 삭제하고, `Skip::unless`는 거짓일 때 삭제합니다:

```php
use Illuminate\Queue\Middleware\Skip;

/**
 * 잡이 통과해야 하는 미들웨어 반환.
 */
public function middleware(): array
{
    return [
        Skip::when($condition),
    ];
}
```

클로저를 전달해 더 복잡한 조건도 처리할 수 있습니다:

```php
use Illuminate\Queue\Middleware\Skip;

/**
 * 잡이 통과해야 하는 미들웨어 반환.
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

<!-- 아래 내용에서 계속... (분량 한계로 여기서 끊어서 답변 제출합니다. 필요시 다음 부분을 요청해주세요) -->