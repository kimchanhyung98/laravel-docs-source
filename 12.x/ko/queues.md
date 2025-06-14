# 큐 (Queues)

- [소개](#introduction)
    - [커넥션과 큐의 차이](#connections-vs-queues)
    - [드라이버별 안내 및 사전 준비사항](#driver-prerequisites)
- [Job 생성](#creating-jobs)
    - [Job 클래스 생성하기](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [고유 Job](#unique-jobs)
    - [암호화된 Job](#encrypted-jobs)
- [Job 미들웨어](#job-middleware)
    - [요청 제한(Rate Limiting)](#rate-limiting)
    - [Job 중복 처리 방지](#preventing-job-overlaps)
    - [예외 제한(Throttling Exceptions)](#throttling-exceptions)
    - [Job 건너뛰기](#skipping-jobs)
- [Job 디스패치](#dispatching-jobs)
    - [지연 디스패치](#delayed-dispatching)
    - [동기 디스패치](#synchronous-dispatching)
    - [Job과 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [Job 체이닝](#job-chaining)
    - [큐 및 커넥션 커스터마이징](#customizing-the-queue-and-connection)
    - [최대 시도 횟수/타임아웃 값 지정](#max-job-attempts-and-timeout)
    - [에러 처리](#error-handling)
- [Job 배치](#job-batching)
    - [배치 가능한 Job 정의하기](#defining-batchable-jobs)
    - [배치 디스패치](#dispatching-batches)
    - [체인과 배치](#chains-and-batches)
    - [배치에 Job 추가](#adding-jobs-to-batches)
    - [배치 점검](#inspecting-batches)
    - [배치 취소](#cancelling-batches)
    - [배치 실패 처리](#batch-failures)
    - [배치 정리](#pruning-batches)
    - [DynamoDB에 배치 저장](#storing-batches-in-dynamodb)
- [클로저 큐잉](#queueing-closures)
- [큐 워커 실행하기](#running-the-queue-worker)
    - [`queue:work` 명령어](#the-queue-work-command)
    - [큐 우선순위](#queue-priorities)
    - [큐 워커와 배포](#queue-workers-and-deployment)
    - [Job 만료 및 타임아웃](#job-expirations-and-timeouts)
- [Supervisor 설정](#supervisor-configuration)
- [실패한 Job 처리](#dealing-with-failed-jobs)
    - [실패한 Job 정리](#cleaning-up-after-failed-jobs)
    - [실패한 Job 재시도](#retrying-failed-jobs)
    - [누락된 모델 무시](#ignoring-missing-models)
    - [실패한 Job 삭제(정리)](#pruning-failed-jobs)
    - [DynamoDB에 실패 Job 저장](#storing-failed-jobs-in-dynamodb)
    - [실패한 Job 저장 비활성화](#disabling-failed-job-storage)
    - [실패한 Job 이벤트](#failed-job-events)
- [큐에서 Job 삭제](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [일부 Job 페이크](#faking-a-subset-of-jobs)
    - [Job 체인 테스트](#testing-job-chains)
    - [Job 배치 테스트](#testing-job-batches)
    - [Job/큐 상호작용 테스트](#testing-job-queue-interactions)
- [Job 이벤트](#job-events)

<a name="introduction"></a>
## 소개

웹 애플리케이션을 개발하다 보면, 업로드된 CSV 파일을 처리하고 저장하는 작업처럼 일반적인 웹 요청 중에 처리하기에는 너무 오래 걸리는 작업이 있을 수 있습니다. 다행히 라라벨에서는 이러한 작업을 손쉽게 비동기로 처리할 수 있도록 큐에 Job을 생성할 수 있습니다. 시간 소모가 큰 작업을 큐로 분리하여 처리하면, 애플리케이션은 웹 요청에 훨씬 빠르게 응답할 수 있어 고객에게 더 나은 사용자 경험을 제공합니다.

라라벨 큐는 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 또는 관계형 데이터베이스 등 다양한 큐 백엔드에서 일관된 큐 API를 제공합니다.

라라벨의 큐 설정 옵션은 애플리케이션의 `config/queue.php` 설정 파일에 저장되어 있습니다. 이 파일에서는 프레임워크에 포함된 각 큐 드라이버별 연결 설정을 확인할 수 있습니다. 여기에는 데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 드라이버뿐만 아니라, 즉시 Job을 실행하는 동기 드라이버(로컬 개발용)도 포함됩니다. 큐에 담긴 Job을 무시하는 `null` 큐 드라이버도 존재합니다.

> [!NOTE]
> 이제 라라벨은 Horizon이라는 강력한 대시보드 및 설정 시스템을 통해 Redis 기반 큐를 더욱 편리하게 관리할 수 있습니다. 자세한 내용은 [Horizon 공식 문서](/docs/12.x/horizon)를 참고하세요.

<a name="connections-vs-queues"></a>
### 커넥션과 큐의 차이

라라벨 큐를 시작하기 전에 "커넥션(connection)"과 "큐(queue)"의 개념 차이를 이해하는 것이 중요합니다. `config/queue.php` 설정 파일에는 `connections`라는 설정 배열이 있습니다. 이 옵션은 Amazon SQS, Beanstalk, Redis와 같은 백엔드 큐 서비스에 대한 연결 정보를 정의합니다. 하지만 하나의 큐 커넥션(connection)은 여러 개의 "큐(queue)"를 가질 수 있으며, 이는 큐에 쌓인 작업(Job)들을 서로 다른 스택 또는 무더기로 생각하면 됩니다.

각 커넥션 설정 예시에는 반드시 `queue` 속성이 포함되어 있습니다. 이 속성은 해당 커넥션으로 Job이 전송될 때 기본적으로 쌓이는 큐의 이름을 의미합니다. 즉, Job을 디스패치할 때 별도로 큐를 지정하지 않는 경우, 해당 커넥션 설정의 `queue` 속성에 정의된 큐에 Job이 쌓이게 됩니다.

```php
use App\Jobs\ProcessPodcast;

// 이 Job은 기본 커넥션의 기본 큐로 전송됩니다...
ProcessPodcast::dispatch();

// 이 Job은 기본 커넥션의 "emails" 큐로 전송됩니다...
ProcessPodcast::dispatch()->onQueue('emails');
```

일부 애플리케이션에서는 여러 큐를 따로 사용할 필요 없이 단일 큐만으로 충분할 수 있습니다. 하지만 Job을 여러 큐로 분리해 전송하면, 큐가 처리되는 우선순위나 그룹별로 세분화하고 싶을 때 매우 유용합니다. 라라벨 큐 워커는 어떤 큐를 어떤 우선순위로 처리할지 지정할 수 있으므로, 예를 들어 `high`라는 큐로 Job을 전송했다면, 우선순위가 높은 큐를 먼저 처리하도록 지정할 수 있습니다.

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버별 안내 및 사전 준비사항

<a name="database"></a>
#### 데이터베이스

`database` 큐 드라이버를 사용하려면 Job을 보관할 데이터베이스 테이블이 필요합니다. 일반적으로 라라벨의 기본 마이그레이션 파일인 `0001_01_01_000002_create_jobs_table.php`에 포함되어 있습니다. 만약 프로젝트에 해당 마이그레이션이 없다면, `make:queue-table` 아티즌 명령어로 생성할 수 있습니다.

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면, `config/database.php` 설정 파일 내에 Redis 데이터베이스 연결을 별도로 구성해야 합니다.

> [!WARNING]
> `redis` 큐 드라이버는 Redis의 `serializer` 및 `compression` 옵션을 지원하지 않습니다.

**Redis 클러스터**

Redis 큐 커넥션에서 Redis 클러스터를 사용하는 경우, 큐 이름에 반드시 [키 해시 태그](https://redis.io/docs/reference/cluster-spec/#hash-tags)를 포함시켜야 합니다. 해시 태그를 사용하면 해당 큐에 대한 모든 Redis 키가 동일한 해시 슬롯에 저장되어야 하기 때문입니다.

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

**블로킹(blocking)**

Redis 큐를 사용할 때 `block_for` 설정 옵션을 통해, 워커 루프가 반복하며 새 Job을 대기하면서 검사하기 전에 드라이버가 Job을 기다리는 시간을 지정할 수 있습니다.

큐의 부하 상황에 따라 이 값을 조절하면 Redis에서 계속해서 Job을 반복적으로 폴링하는 것보다 훨씬 효율적으로 운용할 수 있습니다. 예를 들어, 아래처럼 값을 `5`로 설정하면, 새로운 Job을 대기하는 동안 드라이버가 5초 동안 차단 상태로 대기합니다.

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
> `block_for` 값을 `0`으로 지정하면 워커가 새 Job이 나올 때까지 무한정 차단(blocking)됩니다. 이 경우, 다음 Job이 처리되기 전까지는 `SIGTERM` 등과 같은 종료 시그널도 처리되지 않으니 주의하세요.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 의존성

아래 큐 드라이버를 사용하려면, 다음과 같은 의존 패키지가 필요합니다. 각 의존성은 Composer 패키지 매니저로 설치할 수 있습니다.

<div class="content-list" markdown="1">

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~2.0` 또는 phpredis PHP 확장 모듈
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`

</div>

<a name="creating-jobs"></a>
## Job 생성

<a name="generating-job-classes"></a>
### Job 클래스 생성하기

기본적으로, 애플리케이션에서 큐에 연결할 Job은 모두 `app/Jobs` 디렉터리에 저장됩니다. 만약 이 디렉터리가 없다면, `make:job` 아티즌 명령어를 실행할 때 자동으로 생성됩니다.

```shell
php artisan make:job ProcessPodcast
```

생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현합니다. 이 인터페이스는 라라벨에 해당 Job을 큐에 비동기적으로 처리하도록 알려줍니다.

> [!NOTE]
> Job 스텁(stub)은 [스텁 퍼블리싱](/docs/12.x/artisan#stub-customization) 기능을 통해 커스터마이즈할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조

Job 클래스는 매우 단순한 구조를 가지고 있으며, 보통 큐에서 Job이 처리될 때 호출되는 `handle` 메서드만을 포함합니다. 먼저 예시 Job 클래스를 살펴보겠습니다. 여기서는 팟캐스트 발행 서비스를 운영한다고 가정하고, 업로드된 팟캐스트 파일을 발행 전에 처리하는 Job의 예시입니다.

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

이 예시에서 보듯, [Eloquent 모델](/docs/12.x/eloquent)을 큐 Job의 생성자에 바로 전달할 수 있습니다. Job이 사용하는 `Queueable` 트레이트 덕분에, Eloquent 모델 및 로드된 연관관계 데이터도 Job 처리 시 자동으로 직렬화/역직렬화가 이뤄집니다.

만약 큐 Job의 생성자에서 Eloquent 모델을 받는다면, 큐에 저장될 때는 해당 모델의 식별자만이 직렬화됩니다. Job이 실제로 실행될 때 큐 시스템이 자동으로 데이터베이스에서 해당 모델 인스턴스와 연관관계를 다시 가져옵니다. 이렇게 하면 큐 드라이버에 전송되는 Job 데이터(payload)가 훨씬 가벼워집니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드 의존성 주입

`handle` 메서드는 Job이 큐에서 처리될 때 호출됩니다. 이때, 해당 메서드에 타입힌트를 사용해 의존성을 선언할 수 있습니다. 라라벨 [서비스 컨테이너](/docs/12.x/container)가 이러한 의존성을 자동으로 주입해줍니다.

서비스 컨테이너가 `handle` 메서드의 의존성을 주입하는 방식을 완전히 직접 제어하고 싶다면, 컨테이너의 `bindMethod` 메서드를 사용할 수도 있습니다. `bindMethod`는 Job과 컨테이너를 인자로 받아 콜백에서 원하는 방법으로 `handle` 메서드를 호출할 수 있습니다. 일반적으로 이 메서드는 `App\Providers\AppServiceProvider` [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드 안에서 호출합니다.

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 이미지의 원본 데이터 등 바이너리 데이터는 큐 Job에 전달하기 전에 반드시 `base64_encode`를 사용해 인코딩해야 합니다. 그렇지 않으면 Job이 큐에 저장될 때 JSON 직렬화에 실패할 수 있습니다.

<a name="handling-relationships"></a>
#### 큐 Job에서 Eloquent 연관관계 다루기

큐에 Job을 등록할 때 로드된 모든 Eloquent 모델의 연관관계도 직렬화됩니다. 이렇게 될 경우, 직렬화된 Job 문자열이 상당히 커질 수 있습니다. 또한 Job이 역직렬화되어 실행될 때, 모델의 연관관계 데이터는 원본 전체를 데이터베이스에서 다시 가져오게 되며, Job을 등록할 때 일시적으로 적용한 관계 제약조건은 복원되지 않습니다. 따라서, 특정 관계의 일부만 필요로 한다면, Job 내에서 다시 제약조건을 적용해야 합니다.

또는, 모델의 로드된 관계가 직렬화되지 않도록 하려면, 속성 값을 지정할 때 모델에서 `withoutRelations` 메서드를 호출하면 됩니다. 이 메서드는 로드된 관계가 제외된 모델 인스턴스를 반환합니다.

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

PHP의 생성자 프로퍼티 프로모션을 사용하는 경우, Eloquent 모델의 관계 직렬화를 방지하려면 `WithoutRelations` 속성(attribute)을 사용할 수 있습니다.

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

만약 Job이 단일 모델이 아니라 Eloquent 모델의 컬렉션이나 배열을 받는 경우, 각 모델의 관계 데이터는 Job이 실행될 때 자동으로 복원되지 않습니다. 이는 대량의 모델을 사용하는 Job에서 과도한 리소스 사용을 방지하기 위한 조치입니다.

<a name="unique-jobs"></a>
### 고유 Job

> [!WARNING]
> 고유 Job(Unique Job)은 [락(lock)](/docs/12.x/cache#atomic-locks)을 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 원자적 락을 지원합니다. 또한, 고유 제약은 배치 내의 Job에는 적용되지 않습니다.

특정 Job이 한 번에 하나만 큐에 존재하도록 보장하고 싶을 때가 있습니다. 이럴 때는 Job 클래스에 `ShouldBeUnique` 인터페이스를 구현하면 됩니다. 이 인터페이스는 별도의 메서드 구현이 필요하지 않습니다.

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

위 예시에서 `UpdateSearchIndex` Job은 고유하게 처리됩니다. 즉, 동일한 Job이 큐에 이미 존재하고 아직 처리되지 않았다면, 새 Job은 전송되지 않습니다.

특정 "키(key)"로 Job의 고유성을 제어하거나, Job이 고유한 상태를 유지할 제한 시간을 별도로 지정하고 싶을 수도 있습니다. 이를 위해 클래스에 `uniqueId` 및 `uniqueFor` 속성 또는 메서드를 정의할 수 있습니다.

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

위 예시에서 `UpdateSearchIndex` Job은 상품 ID로 고유성이 부여됩니다. 따라서 동일한 상품 ID로 전송되는 새 Job은 기존 Job이 처리될 때까지 무시됩니다. 또한 기존 Job이 한 시간(3600초) 내에 처리되지 않으면, 고유 락이 해제되어 같은 고유 키로 새 Job이 전송될 수 있습니다.

> [!WARNING]
> 여러 웹 서버나 컨테이너에서 Job을 디스패치하는 경우, 모든 서버가 동일한 중앙 캐시 서버를 사용하도록 구성해야 라라벨이 Job의 고유성을 정확하게 판단할 수 있습니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### Job을 처리 시작 직전까지 고유하게 유지하기

기본적으로 고유 Job은 처리 완료되거나 모든 재시도 횟수에서 실패할 때 "락"이 해제됩니다. 하지만 Job이 처리되기 바로 직전에 락이 풀리도록 하고 싶을 때가 있습니다. 이 경우 `ShouldBeUnique` 대신 `ShouldBeUniqueUntilProcessing` 인터페이스를 구현하면 됩니다.

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
#### 고유 Job 락

내부적으로 `ShouldBeUnique` Job이 큐에 전송될 때마다, 라라벨은 `uniqueId` 키를 사용해 [락](/docs/12.x/cache#atomic-locks)을 획득하려 시도합니다. 이 락을 획득할 수 없다면, 해당 Job은 큐에 전송되지 않습니다. 락은 Job이 처리 완료되거나 모든 재시도에서 실패하면 해제됩니다. 라라벨은 기본 캐시 드라이버를 사용하여 이 락을 만들지만, 다른 드라이버로 락을 관리하고 싶다면 `uniqueVia` 메서드를 정의해서 사용할 캐시 드라이버를 반환하면 됩니다.

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
> 단순히 Job의 동시 처리 수를 제한하고 싶다면, [WithoutOverlapping 미들웨어](/docs/12.x/queues#preventing-job-overlaps)를 사용하는 것이 더 적합합니다.

<a name="encrypted-jobs"></a>
### 암호화된 Job

라라벨은 Job 데이터를 [암호화](/docs/12.x/encryption)하여 개인정보 보호와 데이터 무결성을 보장할 수 있도록 지원합니다. 사용 방법은 매우 간단하며, Job 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하면 됩니다. 이 인터페이스를 추가하면 라라벨이 해당 Job을 큐에 올릴 때 자동으로 암호화합니다.

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
## Job 미들웨어

Job 미들웨어를 사용하면 큐에 올라가는 Job 처리 과정에 커스텀 로직을 감쌀 수 있어, 반복적인 코드 작성을 줄일 수 있습니다. 예를 들어, 아래와 같이 라라벨의 Redis 요청 제한 기능을 활용해 일정 간격마다 하나의 Job만 처리하도록 할 수도 있습니다.

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

이처럼 구현하면 `handle` 메서드 내부가 Redis 기반의 요청 제한(logic) 코드로 다소 복잡해집니다. 또한 다른 Job에 요청 제한 기능을 적용하려면 매번 동일한 코드를 복사/붙여넣기 해야 하므로 번거롭습니다.

이런 경우에는 handle 메서드 내에서 직접 제한하지 않고, 요청 제한 처리를 전담하는 Job 미들웨어를 전체에 적용할 수 있습니다. 라라벨은 Job 미들웨어를 위한 특별한 디렉터리 위치를 정해놓지 않았으므로, 원하는 곳에 자유롭게 작성할 수 있습니다. 아래 예시에서는 `app/Jobs/Middleware` 디렉터리에 미들웨어 클래스를 추가했습니다.

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

보시는 것처럼 [라우트 미들웨어](/docs/12.x/middleware)와 유사하게, Job 미들웨어도 처리 중인 Job 객체와 다음 단계로 넘길 콜백을 인자로 받습니다.

새로운 Job 미들웨어 클래스를 생성할 때는 `make:job-middleware` 아티즌 명령어를 사용할 수 있습니다. 미들웨어를 작성한 뒤에는, 해당 Job의 `middleware` 메서드에서 반환하게끔 추가로 구현해야 합니다. 이 메서드는 scaffold된 Job 클래스에 기본적으로 포함되어 있지 않으므로 직접 추가해주셔야 합니다.

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
> Job 미들웨어는 [큐에 등록되는 이벤트 리스너](/docs/12.x/events#queued-event-listeners), [메일 발송](/docs/12.x/mail#queueing-mail), [알림](/docs/12.x/notifications#queueing-notifications)에도 동일하게 적용할 수 있습니다.

<a name="rate-limiting"></a>
### 요청 제한(Rate Limiting)

앞서 직접 요청 제한 미들웨어를 작성하는 방법을 살펴보았습니다. 하지만 라라벨에는 이미 Job의 제한 처리에 사용할 수 있는 요청 제한 미들웨어가 기본으로 포함되어 있습니다. [라우트 요청 제한자](/docs/12.x/routing#defining-rate-limiters)처럼, Job 제한자도 `RateLimiter` 파사드의 `for` 메서드로 정의할 수 있습니다.

예를 들어, 일반 사용자는 1시간에 한 번씩만 백업 Job을 허용하고, 프리미엄 고객은 제한을 두지 않으려면, `AppServiceProvider`의 `boot` 메서드에서 다음과 같이 RateLimiter를 정의할 수 있습니다.

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

위 예시에서는 시간 단위로 제한했지만, 필요에 따라 `perMinute`로 분 단위 제한도 손쉽게 지정할 수 있습니다. 또한 `by` 메서드에는 보통 고객 단위 기준값을 지정하지만, 원하는 값을 자유롭게 지정할 수 있습니다.

```php
return Limit::perMinute(50)->by($job->user->id);
```

요청 제한자를 정의한 후에는, Job의 미들웨어에서 `Illuminate\Queue\Middleware\RateLimited` 미들웨어를 사용해 RateLimiter를 적용할 수 있습니다. 제한을 초과할 때마다 이 미들웨어가 Job을 적절한 지연 시간과 함께 큐로 다시 반환해줍니다.

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

요청 제한에 걸려 큐로 되돌려진 Job도 전체 시도(`attempts`) 횟수가 증가합니다. 따라서 Job 클래스의 `tries` 및 `maxExceptions` 속성 값을 상황에 맞게 조정하거나, [retryUntil 메서드](#time-based-attempts)를 사용해 Job이 시도될 수 있는 최대 시간을 직접 설정할 수도 있습니다.

또한 `releaseAfter` 메서드를 활용하면 Job이 다시 시도되기까지 대기할 초(seconds)를 직접 지정할 수 있습니다.

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

반대로, 요청 제한에 걸렸을 때 Job을 다시 시도하지 않으려면 `dontRelease` 메서드를 사용할 수 있습니다.

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
> Redis를 사용 중이라면, `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어를 사용할 수 있습니다. 이 미들웨어는 Redis에 최적화되어 있어, 일반적인 RateLimited 미들웨어보다 더 효율적으로 동작합니다.

<a name="preventing-job-overlaps"></a>
### Job 중복 처리 방지

라라벨에는 임의의 키 값을 기준으로 Job의 중복 실행을 방지하는 `Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어가 포함되어 있습니다. 하나의 리소스가 동시에 여러 Job에서 변경되면 안 되는 경우에 유용하게 사용할 수 있습니다.

예를 들어, 사용자의 신용점수를 업데이트하는 Job이 있다고 가정하고, 특정 사용자 ID에 대한 중복 실행을 막고 싶다면, 해당 Job의 `middleware` 메서드에서 다음처럼 반환하면 됩니다.

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

동일 타입의 중복된 Job은 큐로 다시 반환(release)됩니다. 또한 리턴 시, 몇 초 후에 다시 시도할지 `releaseAfter`로 지정할 수 있습니다.

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

바로 중복된 Job을 삭제(재시도하지 않음)하려면 `dontRelease` 메서드를 사용할 수 있습니다.

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

`WithoutOverlapping` 미들웨어는 라라벨의 원자적 락 기능을 기반으로 동작합니다. 때로는 Job이 예기치 않게 실패하거나 타임아웃되어 락이 제대로 해제되지 않을 수도 있으므로, `expireAfter` 메서드로 락의 만료 시간을 명시적으로 지정할 수 있습니다. 예를 들어, 아래처럼 하면 Job이 실행 시작 후 3분이 지나면 락이 자동으로 해제됩니다.

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
> `WithoutOverlapping` 미들웨어는 [락(lock)](/docs/12.x/cache#atomic-locks)을 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 원자적 락을 지원합니다.

<a name="sharing-lock-keys"></a>

#### 작업 클래스 간 락 키 공유

기본적으로 `WithoutOverlapping` 미들웨어는 동일한 클래스의 중복된 작업 실행만 방지합니다. 따라서 서로 다른 두 작업 클래스가 같은 락 키를 사용하더라도 중복 실행이 방지되지는 않습니다. 하지만, `shared` 메서드를 사용하면 라라벨이 해당 락 키를 작업 클래스 전체에 적용하도록 설정할 수 있습니다.

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

라라벨은 예외 제한을 지원하는 `Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어를 제공합니다. 이 미들웨어를 사용하면, 작업에서 일정 횟수 이상의 예외가 발생할 경우, 지정된 시간만큼 추가 실행 시도를 지연시킬 수 있습니다. 이 기능은 특히 불안정한 외부 서비스와 상호작용하는 작업에 유용합니다.

예를 들어, 외부 API와 통신하는 작업에서 연속적으로 예외가 발생한다고 가정해 보겠습니다. 예외 제한을 적용하려면, 해당 작업의 `middleware` 메서드에서 `ThrottlesExceptions` 미들웨어를 반환하면 됩니다. 보통 이 미들웨어는 [시간 기반의 실행 재시도](#time-based-attempts)와 함께 사용해야 합니다.

```php
use DateTime;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 작업이 거칠 미들웨어를 반환합니다.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new ThrottlesExceptions(10, 5 * 60)];
}

/**
 * 작업의 타임아웃 시점을 반환합니다.
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(30);
}
```

미들웨어의 첫 번째 생성자 인자는 예외가 몇 번 발생할 때까지 실행을 허용할지를 나타내며, 두 번째 인자는 제한(Throttling) 상태에 진입한 뒤 다시 실행을 시도하기 전까지 대기할 시간(초 단위)입니다. 위 코드 예시에서는 작업이 10번 연속 예외를 발생시키면, 30분의 제한시간 내에서 5분간 대기 후 재시도하게 됩니다.

예외가 발생하더라도 제한 횟수에 도달하지 않았다면, 작업은 보통 즉시 재시도됩니다. 다만, 미들웨어를 붙일 때 `backoff` 메서드를 사용하여, 예외 발생 시 작업의 재시도를 지연시킬 시간을 (분 단위로) 지정할 수 있습니다.

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 작업이 거칠 미들웨어를 반환합니다.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 5 * 60))->backoff(5)];
}
```

이 미들웨어는 내부적으로 라라벨의 캐시 시스템을 활용하여 rate limiting(속도 제한)을 구현하며, 작업의 클래스명이 캐시의 "키"로 사용됩니다. 동일 외부 서비스를 사용하는 여러 작업이 하나의 제한 "버킷"을 공유하도록 하고 싶다면, 미들웨어를 붙일 때 `by` 메서드로 키를 직접 지정할 수 있습니다.

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 작업이 거칠 미들웨어를 반환합니다.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->by('key')];
}
```

기본적으로 이 미들웨어는 모든 예외에 제한을 적용합니다. 미들웨어를 붙일 때 `when` 메서드를 활용하면, 전달한 클로저가 `true`를 반환하는 경우에만 해당 예외에 제한을 적용하도록 조정할 수 있습니다.

```php
use Illuminate\Http\Client\HttpClientException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 작업이 거칠 미들웨어를 반환합니다.
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

`when` 메서드는 작업을 큐에 다시 재등록하거나 예외를 throw하지만, `deleteWhen` 메서드는 특정 예외가 발생하면 해당 작업을 아예 삭제하도록 해줍니다.

```php
use App\Exceptions\CustomerDeletedException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 작업이 거칠 미들웨어를 반환합니다.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(2, 10 * 60))->deleteWhen(CustomerDeletedException::class)];
}
```

제한된(throttled) 예외도 애플리케이션의 예외 핸들러에 보고하도록 하려면, 미들웨어를 붙일 때 `report` 메서드를 사용할 수 있습니다. 선택적으로 `report` 메서드에 클로저를 전달하면, 해당 클로저가 `true`를 반환할 때에만 예외가 보고됩니다.

```php
use Illuminate\Http\Client\HttpClientException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 작업이 거칠 미들웨어를 반환합니다.
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
> Redis를 사용 중이라면, Redis에 특화되어 더 효율적인 `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어를 사용할 수 있습니다.

<a name="skipping-jobs"></a>
### 작업 건너뛰기(Skipping Jobs)

`Skip` 미들웨어를 사용하면 작업의 로직을 변경하지 않고도, 해당 작업을 건너뛰거나 삭제할 수 있습니다. `Skip::when` 메서드는 주어진 조건이 `true`일 때 작업을 삭제하며, `Skip::unless` 메서드는 조건이 `false`일 때 작업을 삭제합니다.

```php
use Illuminate\Queue\Middleware\Skip;

/**
 * 작업이 거칠 미들웨어를 반환합니다.
 */
public function middleware(): array
{
    return [
        Skip::when($someCondition),
    ];
}
```

`when` 및 `unless` 메서드에 클로저(Closure)를 전달하면, 좀 더 복잡한 조건으로도 작업 건너뛰기가 가능합니다.

```php
use Illuminate\Queue\Middleware\Skip;

/**
 * 작업이 거칠 미들웨어를 반환합니다.
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

<a name="dispatching-jobs"></a>
## 작업 디스패치(Dispatching Jobs)

작업 클래스를 작성했다면, 해당 클래스의 `dispatch` 메서드를 사용하여 작업을 디스패치할 수 있습니다. `dispatch` 메서드에 전달된 인수들은 작업의 생성자(constructor)로 전달됩니다.

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
     * 새 팟캐스트를 저장합니다.
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

조건에 따라 작업을 디스패치하고 싶다면, `dispatchIf` 와 `dispatchUnless` 메서드를 사용할 수 있습니다.

```php
ProcessPodcast::dispatchIf($accountActive, $podcast);

ProcessPodcast::dispatchUnless($accountSuspended, $podcast);
```

새로운 라라벨 애플리케이션에서는 `sync` 드라이버가 기본 큐 드라이버입니다. 이 드라이버는 작업을 현재 요청의 프로세스에서 바로 동기적으로 실행하므로, 로컬 개발 환경에서 편리하게 사용할 수 있습니다. 실제로 백그라운드에서 작업이 큐잉되도록 하려면, 애플리케이션의 `config/queue.php` 설정 파일에서 다른 큐 드라이버를 지정하십시오.

<a name="delayed-dispatching"></a>
### 지연 디스패치(Delayed Dispatching)

작업이 바로 큐워커에 의해 처리되지 않고, 일정 시간이 지난 후에 처리되도록 하려면, 작업을 디스패치할 때 `delay` 메서드를 사용할 수 있습니다. 예를 들어, 작업이 디스패치된 후 10분이 지나야 처리되도록 만들고 싶다면 다음과 같이 작성합니다.

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
     * 새 팟캐스트를 저장합니다.
     */
    public function store(Request $request): RedirectResponse
    {
        $podcast = Podcast::create(/* ... */);

        // ...

        ProcessPodcast::dispatch($podcast)
            ->delay(now()->addMinutes(10));

        return redirect('/podcasts');
    }
}
```

특정 작업에 이미 기본 지연(delay)이 설정되어 있을 수도 있습니다. 만약 이 지연을 무시하고 즉시 작업을 처리하고 싶다면, `withoutDelay` 메서드를 사용할 수 있습니다.

```php
ProcessPodcast::dispatch($podcast)->withoutDelay();
```

> [!WARNING]
> Amazon SQS 큐 서비스에서는 최대 지연 시간이 15분입니다.

<a name="dispatching-after-the-response-is-sent-to-browser"></a>
#### 브라우저에 응답을 보낸 후 작업 디스패치

또 다른 방법으로, `dispatchAfterResponse` 메서드는 웹 서버가 FastCGI를 사용하는 경우 HTTP 응답이 사용자 브라우저로 전송된 후에 작업을 디스패치합니다. 이 방식을 사용하면 큐 작업이 백그라운드에서 실행되는 동안에도 사용자가 애플리케이션을 바로 사용할 수 있습니다. 이 기능은 이메일 전송 등 약 1초 이내의 비교적 빠른 작업에 사용하는 것이 적합합니다. 현재 HTTP 요청 내에서 처리되기 때문에, 이런 방식으로 디스패치된 작업은 별도의 큐 워커가 실행 중일 필요가 없습니다.

```php
use App\Jobs\SendNotification;

SendNotification::dispatchAfterResponse();
```

또한 클로저를 `dispatch`한 뒤 `afterResponse` 메서드를 체이닝하여, HTTP 응답이 브라우저로 전송된 후 클로저를 실행할 수도 있습니다.

```php
use App\Mail\WelcomeMessage;
use Illuminate\Support\Facades\Mail;

dispatch(function () {
    Mail::to('taylor@example.com')->send(new WelcomeMessage);
})->afterResponse();
```

<a name="synchronous-dispatching"></a>
### 동기 디스패치(Synchronous Dispatching)

작업을 즉시(동기적으로) 실행하고 싶을 경우 `dispatchSync` 메서드를 사용할 수 있습니다. 이 방법을 사용하면, 작업이 큐잉되지 않고 현재 프로세스에서 곧바로 실행됩니다.

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
     * 새 팟캐스트를 저장합니다.
     */
    public function store(Request $request): RedirectResponse
    {
        $podcast = Podcast::create(/* ... */);

        // Create podcast...

        ProcessPodcast::dispatchSync($podcast);

        return redirect('/podcasts');
    }
}
```

<a name="jobs-and-database-transactions"></a>
### 작업과 데이터베이스 트랜잭션

데이터베이스 트랜잭션 내에서 작업을 디스패치하는 것은 전혀 문제가 없으나, 해당 작업이 실제로 성공적으로 실행될 수 있는지 주의를 기울여야 합니다. 트랜잭션 내에서 작업을 디스패치하는 경우, 작업보다 먼저 부모 트랜잭션이 커밋되지 않을 수 있습니다. 이 경우, 트랜잭션 중에 변경한 모델이나 레코드가 데이터베이스에 실제 반영되지 않았을 수 있습니다. 또한, 트랜잭션에서 생성된 모델이나 레코드가 아직 데이터베이스에 존재하지 않을 수도 있습니다.

이 문제를 해결하기 위해, 라라벨은 몇 가지 방법을 제공합니다. 첫 번째로, 큐 연결의 설정 배열에서 `after_commit` 옵션을 사용할 수 있습니다.

```php
'redis' => [
    'driver' => 'redis',
    // ...
    'after_commit' => true,
],
```

`after_commit` 옵션이 `true`이면, 데이터베이스 트랜잭션 내에서 작업을 디스패치할 수 있지만, 라라벨은 트랜잭션이 커밋될 때까지 해당 작업의 실제 디스패치를 지연시킵니다. 만약 열린 트랜잭션이 없다면, 작업은 즉시 디스패치됩니다.

트랜잭션 도중 예외 발생으로 인해 롤백되는 경우, 트랜잭션 내에서 디스패치된 작업들은 모두 폐기(discard)됩니다.

> [!NOTE]
> `after_commit` 옵션을 `true`로 설정하면, 큐잉된 이벤트 리스너, 메일, 알림, 브로드캐스트 이벤트 등도 모두 트랜잭션 커밋 후에만 디스패치됩니다.

<a name="specifying-commit-dispatch-behavior-inline"></a>
#### 커밋 후 디스패치 동작을 인라인으로 지정하기

만약 큐 연결의 `after_commit` 옵션을 `true`로 두지 않은 경우에도, 특정 작업 단위로만 트랜잭션 커밋 후 작업이 디스패치되도록 지정할 수 있습니다. 이를 위해, 디스패치할 때 `afterCommit` 메서드를 체이닝하면 됩니다.

```php
use App\Jobs\ProcessPodcast;

ProcessPodcast::dispatch($podcast)->afterCommit();
```

반대로, 큐 연결의 `after_commit` 옵션이 이미 `true`일 경우, 특정 작업만 트랜잭션 커밋을 기다리지 않고 바로 디스패치하고 싶다면, `beforeCommit` 메서드를 사용할 수 있습니다.

```php
ProcessPodcast::dispatch($podcast)->beforeCommit();
```

<a name="job-chaining"></a>
### 작업 체이닝(Job Chaining)

작업 체이닝을 사용하면, 주 작업이 성공적으로 실행된 후 순차적으로 실행될 작업 목록을 지정할 수 있습니다. 체인 내 어떤 작업이 실패하면, 나머지 작업은 더 이상 실행되지 않습니다. 체이닝을 실행하려면, `Bus` 파사드의 `chain` 메서드를 활용하면 됩니다. 라라벨의 커맨드 버스(command bus)는 큐 작업 디스패칭의 기반이 되는 하위 레벨 컴포넌트입니다.

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

작업 클래스 인스턴스뿐 아니라, 클로저도 체이닝할 수 있습니다.

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
> 작업 내에서 `$this->delete()` 메서드를 사용해 작업을 삭제해도, 체이닝된 작업의 실행은 방지되지 않습니다. 체인 내부의 작업에서 실패가 발생할 때에만 실행이 중단됩니다.

<a name="chain-connection-queue"></a>
#### 체인 연결(Connection) 및 큐(Queue) 지정

체이닝된 작업에 사용할 연결(connection)과 큐(queue)를 지정하고 싶다면, `onConnection` 과 `onQueue` 메서드를 사용할 수 있습니다. 이 메서드들은 큐 작업에 별도로 연결이나 큐 지정이 없는 경우에만 기본 값을 정합니다.

```php
Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->onConnection('redis')->onQueue('podcasts')->dispatch();
```

<a name="adding-jobs-to-the-chain"></a>
#### 체인에 작업 추가하기

경우에 따라, 이미 실행 중인 체인 내부에서 앞쪽 또는 뒤쪽에 작업을 추가해야 할 때가 있습니다. 이런 경우 `prependToChain`과 `appendToChain` 메서드를 사용할 수 있습니다.

```php
/**
 * 작업을 실행합니다.
 */
public function handle(): void
{
    // ...

    // 현재 체인의 앞에 추가하여, 이 작업 직후 곧바로 실행...
    $this->prependToChain(new TranscribePodcast);

    // 현재 체인의 뒤에 추가하여, 체인 마지막에 실행...
    $this->appendToChain(new TranscribePodcast);
}
```

<a name="chain-failures"></a>
#### 체인 실패(Chain Failures)

체이닝 시, `catch` 메서드를 사용하여 체인 내 작업 중 하나가 실패할 경우 호출될 클로저를 지정할 수 있습니다. 해당 콜백은 작업 실패의 원인이 된 `Throwable` 인스턴스를 전달받습니다.

```php
use Illuminate\Support\Facades\Bus;
use Throwable;

Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->catch(function (Throwable $e) {
    // 체인 내 작업 중 하나가 실패했습니다...
})->dispatch();
```

> [!WARNING]
> 체인 콜백은 직렬화되어 나중에 라라벨 큐에 의해 실행되므로, 체인 콜백에서는 `$this` 변수를 사용해서는 안 됩니다.

<a name="customizing-the-queue-and-connection"></a>
### 큐 및 연결 커스터마이징

<a name="dispatching-to-a-particular-queue"></a>
#### 특정 큐로 작업 디스패치

작업을 서로 다른 큐로 분류(push)하면, 큐 작업들을 카테고리화하거나 각 큐에 할당할 워커의 우선순위를 조정할 수 있습니다. 이 방식은 큐 설정 파일에서 정의한 "큐 연결(connection)" 을 바꾸는 것이 아니라, 하나의 연결에서 큐 이름별로 작업을 분류하는 것입니다. 디스패치 시 `onQueue` 메서드를 사용하여 큐를 지정할 수 있습니다.

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
     * 새 팟캐스트를 저장합니다.
     */
    public function store(Request $request): RedirectResponse
    {
        $podcast = Podcast::create(/* ... */);

        // Create podcast...

        ProcessPodcast::dispatch($podcast)->onQueue('processing');

        return redirect('/podcasts');
    }
}
```

또 다른 방법으로, 작업 클래스 생성자 내부에서 `onQueue` 메서드를 호출하여 큐 이름을 지정할 수도 있습니다.

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    /**
     * 새 작업 인스턴스를 생성합니다.
     */
    public function __construct()
    {
        $this->onQueue('processing');
    }
}
```

<a name="dispatching-to-a-particular-connection"></a>
#### 특정 연결로 작업 디스패치

애플리케이션이 여러 큐 연결(connection)과 통신해야 하는 경우, `onConnection` 메서드로 디스패치할 큐 연결을 지정할 수 있습니다.

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
     * 새 팟캐스트를 저장합니다.
     */
    public function store(Request $request): RedirectResponse
    {
        $podcast = Podcast::create(/* ... */);

        // Create podcast...

        ProcessPodcast::dispatch($podcast)->onConnection('sqs');

        return redirect('/podcasts');
    }
}
```

`onConnection`과 `onQueue` 메서드는 체이닝하여, 작업의 연결과 큐를 함께 지정할 수도 있습니다.

```php
ProcessPodcast::dispatch($podcast)
    ->onConnection('sqs')
    ->onQueue('processing');
```

또한, 작업 클래스 생성자에서 `onConnection` 메서드로 연결을 직접 지정할 수도 있습니다.

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    /**
     * 새 작업 인스턴스를 생성합니다.
     */
    public function __construct()
    {
        $this->onConnection('sqs');
    }
}
```

<a name="max-job-attempts-and-timeout"></a>

### 최대 작업 시도 횟수 / 타임아웃 값 지정

<a name="max-attempts"></a>
#### 최대 시도 횟수(Max Attempts)

큐에 등록된 작업 중 하나에서 에러가 발생할 경우, 무한정 계속 재시도되기를 바라지는 않을 것입니다. 그래서 라라벨은 한 작업이 시도될 수 있는 횟수나 기간을 지정할 수 있는 여러 방법을 제공합니다.

가장 간단하게 작업의 최대 시도 횟수를 지정하는 방법은 Artisan 명령줄에서 `--tries` 옵션을 사용하는 것입니다. 이 값은 워커가 처리하는 모든 작업에 적용되며, 개별 작업에서 별도로 최대 시도 횟수를 지정하지 않은 경우에만 해당됩니다.

```shell
php artisan queue:work --tries=3
```

작업이 최대 시도 횟수를 초과하면, 해당 작업은 "실패"한 작업으로 간주됩니다. 실패한 작업의 처리 방법에 대해서는 [실패한 작업 관련 문서](#dealing-with-failed-jobs)를 참고하십시오. 만약 `queue:work` 명령에 `--tries=0`을 지정하면, 작업은 무한정 재시도됩니다.

보다 세밀하게 제어하고 싶다면, 작업 클래스 자체에 최대 시도 횟수를 정의할 수 있습니다. 작업에서 별도로 이 값을 지정하면, 명령줄의 `--tries` 옵션 값보다 우선 적용됩니다.

```php
<?php

namespace App\Jobs;

class ProcessPodcast implements ShouldQueue
{
    /**
     * 작업이 시도될 수 있는 최대 횟수입니다.
     *
     * @var int
     */
    public $tries = 5;
}
```

특정 작업의 최대 시도 횟수를 동적으로 제어해야 하는 경우, 작업 클래스에 `tries` 메서드를 정의할 수 있습니다.

```php
/**
 * 작업이 시도될 수 있는 최대 횟수를 반환합니다.
 */
public function tries(): int
{
    return 5;
}
```

<a name="time-based-attempts"></a>
#### 시도 제한 시간 지정(Time Based Attempts)

실패 전까지 작업이 몇 번 시도될지를 정하는 대신, 특정 시점까지 작업 재시도를 제한할 수도 있습니다. 이렇게 하면 일정 기간 동안은 얼마든지 재시도가 가능하도록 할 수 있습니다. 이를 위해 작업 클래스에 `retryUntil` 메서드를 추가하면 됩니다. 이 메서드는 `DateTime` 인스턴스를 반환해야 합니다.

```php
use DateTime;

/**
 * 작업의 타임아웃 시점을 반환합니다.
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(10);
}
```

`retryUntil`과 `tries`가 모두 정의되어 있다면, 라라벨은 `retryUntil` 메서드를 우선적으로 적용합니다.

> [!NOTE]
> [큐 이벤트 리스너](/docs/12.x/events#queued-event-listeners)나 [큐 알림](/docs/12.x/notifications#queueing-notifications)에 대해서도 `tries` 필드 및 `retryUntil` 메서드를 정의할 수 있습니다.

<a name="max-exceptions"></a>
#### 최대 예외 횟수(Max Exceptions)

작업을 여러 번 재시도하는 것은 허용하되, 처리 중에 특정 횟수 이상 미처리(uncaught) 예외가 발생하면 실패로 간주하고 싶은 경우가 있을 수 있습니다(단순히 `release` 메서드로 재시도 가능한 경우와는 다릅니다). 이럴 때 작업 클래스에 `maxExceptions` 속성을 정의할 수 있습니다.

```php
<?php

namespace App\Jobs;

use Illuminate\Support\Facades\Redis;

class ProcessPodcast implements ShouldQueue
{
    /**
     * 작업이 시도될 수 있는 최대 횟수입니다.
     *
     * @var int
     */
    public $tries = 25;

    /**
     * 실패로 간주하기 전 허용할 미처리 예외 최대 횟수입니다.
     *
     * @var int
     */
    public $maxExceptions = 3;

    /**
     * 작업 실행.
     */
    public function handle(): void
    {
        Redis::throttle('key')->allow(10)->every(60)->then(function () {
            // 락을 획득한 경우, 팟캐스트를 처리...
        }, function () {
            // 락을 얻을 수 없는 경우...
            return $this->release(10);
        });
    }
}
```

이 예시에서, 애플리케이션이 Redis 락을 획득하지 못하면 10초 후에 작업을 다시 큐에 등록하여 재시도합니다. 이 작업은 최대 25회까지 반복될 수 있습니다. 하지만 작업 중 3회 미처리 예외가 발생하면 작업은 실패합니다.

<a name="timeout"></a>
#### 타임아웃(Timeout)

작업이 대략 얼마만큼의 시간 안에 끝날지 예상할 수 있는 경우가 많습니다. 라라벨은 이런 경우를 위해 "타임아웃" 값을 설정할 수 있도록 지원합니다. 기본 타임아웃 값은 60초입니다. 만약 작업이 타임아웃 값(초 단위)보다 오래 처리되면, 해당 작업을 처리하던 워커는 에러와 함께 종료되고, 일반적으로는 [서버에 구성된 프로세스 관리자](#supervisor-configuration)에 의해 자동으로 재시작됩니다.

작업이 실행될 수 있는 최대 초 단위 시간은 Artisan 명령줄의 `--timeout` 옵션으로 지정할 수 있습니다.

```shell
php artisan queue:work --timeout=30
```

작업이 반복적으로 타임아웃으로 인해 최대 시도 횟수를 초과하면, 해당 작업은 실패한 것으로 간주됩니다.

또한 작업 클래스 자체에 작업별 최대 실행 시간을 명시할 수도 있습니다. 이 경우에는 작업에 지정한 값이 명령줄 옵션보다 우선합니다.

```php
<?php

namespace App\Jobs;

class ProcessPodcast implements ShouldQueue
{
    /**
     * 타임아웃까지 허용되는 최대 초입니다.
     *
     * @var int
     */
    public $timeout = 120;
}
```

소켓, 외부 HTTP 연결 등 IO가 블로킹되는 프로세스의 경우, 위의 타임아웃 설정이 항상 적용되지 않을 수 있습니다. 이런 경우에는 해당 라이브러리의 API에서 직접 타임아웃을 반드시 별도로 지정해야 합니다. 예를 들어, Guzzle을 사용할 때는 연결 및 요청 타임아웃 값을 직접 설정해야 합니다.

> [!WARNING]
> 작업 타임아웃을 지정하려면 `pcntl` PHP 확장 모듈이 설치되어 있어야 합니다. 또한, 작업의 "타임아웃" 값은 ["retry after"](#job-expiration) 값보다 항상 작아야 합니다. 그렇지 않으면, 해당 작업이 실제로 완료되거나 타임아웃 되기도 전에 재시도가 일어날 수 있습니다.

<a name="failing-on-timeout"></a>
#### 타임아웃 시 실패 처리(Failing on Timeout)

타임아웃이 발생할 경우, 작업을 [실패](#dealing-with-failed-jobs)로 처리하고 싶다면, 작업 클래스에서 `$failOnTimeout` 속성을 정의합니다.

```php
/**
 * 타임아웃 시 작업을 실패로 표시할지 여부.
 *
 * @var bool
 */
public $failOnTimeout = true;
```

<a name="error-handling"></a>
### 에러 처리(Error Handling)

작업 처리 중 예외가 발생하면, 해당 작업은 자동으로 큐에 다시 등록(release)되어 재시도됩니다. 작업은 애플리케이션이 허용하는 최대 시도 횟수에 도달할 때까지 계속해서 release 및 재시도됩니다. 최대 시도 횟수는 `queue:work` Artisan 명령의 `--tries` 옵션이나, 작업 클래스의 설정 값에 따라 결정됩니다. 큐 워커 실행 방식에 대한 자세한 내용은 [아래 섹션](#running-the-queue-worker)을 참고하세요.

<a name="manually-releasing-a-job"></a>
#### 작업 수동 재등록(Manually Releasing a Job)

필요에 따라 작업을 직접 큐에 다시 등록하여 나중에 다시 시도하고 싶을 때가 있습니다. 이 때는 `release` 메서드를 호출하면 됩니다.

```php
/**
 * 작업 실행.
 */
public function handle(): void
{
    // ...

    $this->release();
}
```

기본적으로 `release` 메서드는 작업을 즉시 큐에 다시 등록합니다. 하지만 정수 값(초 단위)이나 날짜 객체를 인자로 넘기면 지정한 시간이 지난 후에만 작업이 다시 처리 가능하도록 할 수 있습니다.

```php
$this->release(10);

$this->release(now()->addSeconds(10));
```

<a name="manually-failing-a-job"></a>
#### 작업 수동 실패 처리(Manually Failing a Job)

경우에 따라 작업을 코드 상에서 직접 "실패"로 표시해야 할 수도 있습니다. 이때는 `fail` 메서드를 호출하면 됩니다.

```php
/**
 * 작업 실행.
 */
public function handle(): void
{
    // ...

    $this->fail();
}
```

예외를 직접 잡아서, 그 예외로 인해 작업을 실패 처리하고 싶다면, `fail` 메서드에 해당 예외를 넘기면 됩니다. 또는 간단하게 오류 메시지(문자열)를 넘기면, 라라벨에서 자동으로 예외 객체로 변환해서 처리해줍니다.

```php
$this->fail($exception);

$this->fail('Something went wrong.');
```

> [!NOTE]
> 실패한 작업에 대한 더 자세한 정보는 [작업 실패 처리 문서](#dealing-with-failed-jobs)를 참고하십시오.

<a name="job-batching"></a>
## 작업 배치(Job Batching)

라라벨의 작업 배치 기능을 사용하면 여러 개의 작업(Job)을 한 번에 처리하고, 모든 작업이 완료될 때 특정 동작을 수행할 수 있습니다. 먼저, 각 작업 배치에 대한 메타 정보를 저장할 데이터베이스 테이블을 생성해야 합니다. 이 테이블에는 작업 배치의 진행률 등 메타데이터가 저장됩니다. Artisan의 `make:queue-batches-table` 명령으로 마이그레이션을 생성할 수 있습니다.

```shell
php artisan make:queue-batches-table

php artisan migrate
```

<a name="defining-batchable-jobs"></a>
### 배치 가능한 작업 정의하기

배치에 포함시킬 작업을 정의하려면, 일반적으로 [큐 작업을 생성](#creating-jobs)하는 것과 동일하지만, 작업 클래스에 `Illuminate\Bus\Batchable` 트레잇(trait)을 추가해야 합니다. 이 트레잇은 현재 작업이 속해 있는 배치 인스턴스를 반환하는 `batch` 메서드에 접근할 수 있게 해줍니다.

```php
<?php

namespace App\Jobs;

use Illuminate\Bus\Batchable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ImportCsv implements ShouldQueue
{
    use Batchable, Queueable;

    /**
     * 작업 실행
     */
    public function handle(): void
    {
        if ($this->batch()->cancelled()) {
            // 해당 배치가 취소되었는지 확인...

            return;
        }

        // CSV 파일 일부를 가져오기...
    }
}
```

<a name="dispatching-batches"></a>
### 배치 작업 디스패치(Dispatching Batches)

여러 개의 작업을 배치로 디스패치하려면 `Bus` 퍼사드의 `batch` 메서드를 사용합니다. 배치는 보통 완료 콜백과 결합해 사용할 때 가장 유용합니다. 콜백은 `then`, `catch`, `finally` 메서드로 지정할 수 있으며, 호출 시 각 콜백에는 `Illuminate\Bus\Batch` 인스턴스가 전달됩니다. 예를 들어, CSV 파일의 여러 행을 분할해 각각의 배치 작업으로 처리하는 상황을 상상해보겠습니다.

```php
use App\Jobs\ImportCsv;
use Illuminate\Bus\Batch;
use Illuminate\Support\Facades\Bus;
use Throwable;

$batch = Bus::batch([
    new ImportCsv(1, 100),
    new ImportCsv(101, 200),
    new ImportCsv(201, 300),
    new ImportCsv(301, 400),
    new ImportCsv(401, 500),
])->before(function (Batch $batch) {
    // 배치가 생성되었으나 아직 작업이 추가되지 않은 상태...
})->progress(function (Batch $batch) {
    // 하나의 작업이 성공적으로 완료됨...
})->then(function (Batch $batch) {
    // 모든 작업이 성공적으로 완료됨...
})->catch(function (Batch $batch, Throwable $e) {
    // 배치 중 하나의 작업에서 처음으로 실패가 감지됨...
})->finally(function (Batch $batch) {
    // 배치 내 모든 작업의 실행이 완료됨...
})->dispatch();

return $batch->id;
```

배치 ID는 `$batch->id` 프로퍼티로 접근할 수 있으며, [라라벨 커맨드 버스에서](#inspecting-batches) 배치 상태 확인 등에 사용할 수 있습니다.

> [!WARNING]
> 배치 콜백 함수들은 직렬화되었다가 라라벨 큐에 의해 나중에 실행되므로, 콜백 내에서 `$this` 변수를 사용하지 마십시오. 또한, 배치 작업은 데이터베이스 트랜잭션 내에서 실행되므로, 암묵적으로 커밋되는 데이터베이스 문을 작업 중에 실행해서는 안 됩니다.

<a name="naming-batches"></a>
#### 배치 이름 지정(Naming Batches)

Laravel Horizon, Laravel Telescope 등 일부 도구는 배치 작업에 이름이 지정되어 있으면 더 읽기 쉬운 디버그 정보를 제공할 수 있습니다. 배치에 이름을 지정하려면, 배치 정의 시 `name` 메서드를 호출하면 됩니다.

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // 모든 작업이 성공적으로 완료됨...
})->name('Import CSV')->dispatch();
```

<a name="batch-connection-queue"></a>
#### 배치 커넥션 및 큐 지정(Batch Connection and Queue)

배치 작업에서 사용할 커넥션과 큐를 지정하려면, `onConnection`, `onQueue` 메서드를 사용합니다. 배치에 포함된 모든 작업은 동일한 커넥션, 동일한 큐에서 실행되어야 합니다.

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // 모든 작업이 성공적으로 완료됨...
})->onConnection('redis')->onQueue('imports')->dispatch();
```

<a name="chains-and-batches"></a>
### 체인과 배치(Chains and Batches)

[체인 작업](#job-chaining)을 여러 개 모아 하나의 배치에 포함시킬 수도 있습니다. 아래는 2개의 체인 작업을 병렬로 배치 처리한 뒤, 두 체인 모두 처리가 끝나면 콜백을 실행하는 예시입니다.

```php
use App\Jobs\ReleasePodcast;
use App\Jobs\SendPodcastReleaseNotification;
use Illuminate\Bus\Batch;
use Illuminate\Support\Facades\Bus;

Bus::batch([
    [
        new ReleasePodcast(1),
        new SendPodcastReleaseNotification(1),
    ],
    [
        new ReleasePodcast(2),
        new SendPodcastReleaseNotification(2),
    ],
])->then(function (Batch $batch) {
    // ...
})->dispatch();
```

반대로, 체인 안에서 배치를 실행할 수도 있습니다. 예를 들어, 여러 개의 팟캐스트를 먼저 한 번에 배치로 공개하고, 그 다음 각 팟캐스트 공개 알림을 배치로 보낼 수 있습니다.

```php
use App\Jobs\FlushPodcastCache;
use App\Jobs\ReleasePodcast;
use App\Jobs\SendPodcastReleaseNotification;
use Illuminate\Support\Facades\Bus;

Bus::chain([
    new FlushPodcastCache,
    Bus::batch([
        new ReleasePodcast(1),
        new ReleasePodcast(2),
    ]),
    Bus::batch([
        new SendPodcastReleaseNotification(1),
        new SendPodcastReleaseNotification(2),
    ]),
])->dispatch();
```

<a name="adding-jobs-to-batches"></a>
### 배치에 작업 추가하기(Adding Jobs to Batches)

때로는 배치 작업 안에서 추가로 작업을 배치에 넣어야 할 때가 있습니다. 예를 들어, 수천 개의 작업을 웹 요청 중 한꺼번에 디스패치하기에는 시간이 너무 오래 걸릴 수 있습니다. 이때 "로더" 작업을 처음에 소수로 배치에 넣고, 실행되면서 배치를 더 많은 작업으로 확장할 수 있습니다.

```php
$batch = Bus::batch([
    new LoadImportBatch,
    new LoadImportBatch,
    new LoadImportBatch,
])->then(function (Batch $batch) {
    // 모든 작업이 성공적으로 완료됨...
})->name('Import Contacts')->dispatch();
```

이 예시에서, `LoadImportBatch` 작업이 추가 작업들을 배치에 포함시키는 역할을 합니다. 이를 위해 작업의 `batch` 메서드를 통해 접근할 수 있는 배치 인스턴스의 `add` 메서드를 사용합니다.

```php
use App\Jobs\ImportContacts;
use Illuminate\Support\Collection;

/**
 * 작업 실행
 */
public function handle(): void
{
    if ($this->batch()->cancelled()) {
        return;
    }

    $this->batch()->add(Collection::times(1000, function () {
        return new ImportContacts;
    }));
}
```

> [!WARNING]
> 동일한 배치에 속한 작업 내부에서만 해당 배치에 작업을 추가할 수 있습니다.

<a name="inspecting-batches"></a>
### 배치 정보 확인(Inspecting Batches)

배치 완료 콜백에 전달되는 `Illuminate\Bus\Batch` 인스턴스에는, 해당 배치와 관련된 다양한 속성과 메서드가 제공되어 배치를 편리하게 조회하고 조작할 수 있습니다.

```php
// 배치의 UUID
$batch->id;

// 배치의 이름(있을 경우)
$batch->name;

// 배치에 할당된 작업 개수
$batch->totalJobs;

// 아직 큐에서 처리되지 않은 작업 개수
$batch->pendingJobs;

// 실패한 작업 개수
$batch->failedJobs;

// 지금까지 처리된 작업 개수
$batch->processedJobs();

// 배치의 진행률(0~100)
$batch->progress();

// 배치 실행이 모두 끝났는지 여부
$batch->finished();

// 배치 실행 취소
$batch->cancel();

// 배치가 취소되었는지 여부
$batch->cancelled();
```

<a name="returning-batches-from-routes"></a>
#### 라우트에서 배치 반환하기

모든 `Illuminate\Bus\Batch` 인스턴스는 JSON으로 직렬화할 수 있으므로, 라라벨 애플리케이션의 라우트에서 직접 반환해 배치 진행상황 등의 정보를 JSON으로 쉽게 조회할 수 있습니다. 이를 활용하면 프론트엔드 UI에서 배치 진행률 등의 정보를 표시하기에 매우 편리합니다.

특정 배치 ID로 배치 인스턴스를 조회하려면, `Bus` 퍼사드의 `findBatch` 메서드를 사용합니다.

```php
use Illuminate\Support\Facades\Bus;
use Illuminate\Support\Facades\Route;

Route::get('/batch/{batchId}', function (string $batchId) {
    return Bus::findBatch($batchId);
});
```

<a name="cancelling-batches"></a>
### 배치 취소(Cancelling Batches)

배치 실행을 중간에 취소해야 할 때, `Illuminate\Bus\Batch` 인스턴스의 `cancel` 메서드를 호출하면 됩니다.

```php
/**
 * 작업 실행
 */
public function handle(): void
{
    if ($this->user->exceedsImportLimit()) {
        return $this->batch()->cancel();
    }

    if ($this->batch()->cancelled()) {
        return;
    }
}
```

앞선 예제들에서 확인했듯, 일반적으로 배치에 포함된 작업이라면, 실행을 계속하기 전에 해당 배치가 취소됐는지 `cancelled()`로 확인하는 것을 권장합니다. 하지만, 더 간편하게 처리하려면 [미들웨어](#job-middleware)인 `SkipIfBatchCancelled`를 해당 작업에 등록할 수도 있습니다. 이 미들웨어는 해당 배치가 취소된 경우 작업을 실행하지 않도록 합니다.

```php
use Illuminate\Queue\Middleware\SkipIfBatchCancelled;

/**
 * 작업이 통과해야 하는 미들웨어를 반환
 */
public function middleware(): array
{
    return [new SkipIfBatchCancelled];
}
```

<a name="batch-failures"></a>
### 배치 실패 처리(Batch Failures)

배치에 포함된 작업이 실패(에러 발생)할 경우, `catch` 콜백이 할당되어 있으면 해당 콜백이 호출됩니다. 이 콜백은 배치 내에서 **처음으로** 실패한 작업에 한 번만 호출됩니다.

<a name="allowing-failures"></a>
#### 실패 허용(Allowing Failures)

배치 내 작업이 실패하면, 라라벨은 자동으로 해당 배치를 "취소됨" 상태로 표시합니다. 배치 작업의 실패가 배치 전체를 즉시 취소 처리하는 것을 원치 않는 경우, `allowFailures` 메서드를 호출하여 이 동작을 비활성화할 수 있습니다.

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // 모든 작업이 성공적으로 완료됨...
})->allowFailures()->dispatch();
```

<a name="retrying-failed-batch-jobs"></a>
#### 실패한 배치 작업 재시도(Retrying Failed Batch Jobs)

라라벨에서는 실패한 배치 작업을 간단하게 다시 시도할 수 있도록 `queue:retry-batch` Artisan 명령을 제공합니다. 이 명령은 재시도하려는 배치의 UUID를 인자로 받습니다.

```shell
php artisan queue:retry-batch 32dbc76c-4f82-4749-b610-a639fe0099b5
```

<a name="pruning-batches"></a>
### 배치 데이터 청소(Pruning Batches)

별도의 청소작업 없이 두면, `job_batches` 테이블이 매우 빠르게 커질 수 있습니다. 이를 방지하려면 [예약 작업](/docs/12.x/scheduling)에 `queue:prune-batches` Artisan 명령을 등록해 하루 한 번 실행할 것을 권장합니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches')->daily();
```

기본적으로는 24시간이 지난 완료된 모든 배치가 삭제(prune)됩니다. 오래된 배치 데이터를 얼마나 보관할지 지정하려면, 명령 호출 시 `hours` 옵션을 사용할 수 있습니다. 아래 예시는 48시간이 지난 완료 배치를 삭제합니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48')->daily();
```

경우에 따라서는, 작업이 실패한 뒤 재시도가 이뤄지지 않아 "미완료"로 남은 배치 데이터가 `jobs_batches` 테이블에 남을 수 있습니다. 이런 미완료 배치도 `unfinished` 옵션을 사용해 자동으로 정리할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48 --unfinished=72')->daily();
```

또한, 취소된 배치에 대해서도 데이터가 남아 있을 수 있는데, 이때는 `cancelled` 옵션을 사용해 관리할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48 --cancelled=72')->daily();
```

<a name="storing-batches-in-dynamodb"></a>

### DynamoDB에 배치 정보 저장

라라벨은 [DynamoDB](https://aws.amazon.com/dynamodb)를 사용하여 배치 메타 정보를 관계형 데이터베이스 대신 저장할 수 있도록 지원합니다. 그러나 배치 레코드를 저장할 DynamoDB 테이블은 직접 생성해야 합니다.

일반적으로 이 테이블의 이름은 `job_batches`여야 하지만, 애플리케이션의 `queue` 설정 파일 내 `queue.batching.table` 설정 값에 따라 테이블 이름을 정해야 합니다.

<a name="dynamodb-batch-table-configuration"></a>
#### DynamoDB 배치 테이블 구성

`job_batches` 테이블에는 문자열 타입의 파티션 키인 `application`과 문자열 타입의 정렬 키인 `id`가 기본 키로 있어야 합니다. `application` 키에는 애플리케이션의 `app` 설정 파일 내 `name` 설정 값이 들어갑니다. 애플리케이션 이름이 DynamoDB 테이블의 키에 포함되므로, 여러 라라벨 애플리케이션의 잡 배치를 동일한 테이블에 저장할 수 있습니다.

또한, [자동 배치 정리](#pruning-batches-in-dynamodb) 기능을 사용하려면 테이블에 `ttl` 속성을 추가로 정의할 수 있습니다.

<a name="dynamodb-configuration"></a>
#### DynamoDB 설정

다음으로, 라라벨 애플리케이션이 Amazon DynamoDB와 통신할 수 있도록 AWS SDK를 설치해야 합니다.

```shell
composer require aws/aws-sdk-php
```

그리고 `queue.batching.driver` 설정 값을 `dynamodb`로 지정합니다. 또한 `batching` 설정 배열 안에 `key`, `secret`, `region` 옵션을 정의해야 하며, 이는 AWS 인증에 사용됩니다. `dynamodb` 드라이버를 사용할 때는 `queue.batching.database` 설정은 필요하지 않습니다.

```php
'batching' => [
    'driver' => env('QUEUE_BATCHING_DRIVER', 'dynamodb'),
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'table' => 'job_batches',
],
```

<a name="pruning-batches-in-dynamodb"></a>
#### DynamoDB에서 배치 정리

[ DynamoDB](https://aws.amazon.com/dynamodb)에 잡 배치 정보를 저장할 때, 관계형 데이터베이스에 저장된 배치를 정리할 때 사용하는 일반적인 정리 명령어는 작동하지 않습니다. 대신, [DynamoDB의 네이티브 TTL 기능](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html)을 활용하여 오래된 배치 레코드를 자동으로 삭제할 수 있습니다.

DynamoDB 테이블에 `ttl` 속성을 정의했다면, 라라벨에 배치 레코드를 어떻게 정리할지 안내하는 설정 값을 추가로 지정할 수 있습니다. `queue.batching.ttl_attribute` 설정 값은 TTL을 저장하는 속성명을 지정하고, `queue.batching.ttl` 값은 마지막 업데이트 시점을 기준으로 배치 레코드를 DynamoDB 테이블에서 삭제할 수 있는 초 단위의 시간(만료시간)을 지정합니다.

```php
'batching' => [
    'driver' => env('QUEUE_FAILED_DRIVER', 'dynamodb'),
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'table' => 'job_batches',
    'ttl_attribute' => 'ttl',
    'ttl' => 60 * 60 * 24 * 7, // 7일...
],
```

<a name="queueing-closures"></a>
## 클로저를 큐잉하기

잡 클래스를 큐에 디스패치하는 대신, 클로저(익명 함수)를 큐에 전달할 수도 있습니다. 이 방법은 현재 요청 사이클 밖에서 실행해야 하는 간단하고 빠른 작업에 적합합니다. 클로저를 큐에 디스패치하면, 클로저 코드 내용이 암호화 서명되어 전송 중 변조되지 않도록 보장합니다.

```php
$podcast = App\Podcast::find(1);

dispatch(function () use ($podcast) {
    $podcast->publish();
});
```

큐에 삽입된 클로저에 이름을 지정해, 큐 대시보드에서 확인하거나 `queue:work` 명령에서 표시하도록 하려면 `name` 메서드를 사용할 수 있습니다.

```php
dispatch(function () {
    // ...
})->name('Publish Podcast');
```

`catch` 메서드를 이용하면, 큐에 들어간 클로저가 모든 [재시도 횟수](#max-job-attempts-and-timeout)를 소진하고도 실패했을 때 실행할 콜백 클로저를 지정할 수 있습니다.

```php
use Throwable;

dispatch(function () use ($podcast) {
    $podcast->publish();
})->catch(function (Throwable $e) {
    // 이 잡은 실패했습니다...
});
```

> [!WARNING]
> `catch` 콜백은 라라벨 큐에서 직렬화되어 나중에 실행되므로, `catch` 콜백 내에서는 `$this` 변수를 사용하지 마십시오.

<a name="running-the-queue-worker"></a>
## 큐 워커 실행하기

<a name="the-queue-work-command"></a>
### `queue:work` 명령어

라라벨은 큐 워커를 시작하고 큐에 들어온 새로운 잡을 처리하는 Artisan 명령어를 포함하고 있습니다. `queue:work` Artisan 명령어를 사용하여 워커를 실행할 수 있습니다. 이 명령어가 시작되면, 수동으로 중지하거나 터미널을 닫을 때까지 계속 실행됩니다.

```shell
php artisan queue:work
```

> [!NOTE]
> `queue:work` 프로세스를 백그라운드에서 계속 실행하려면, [Supervisor](#supervisor-configuration) 같은 프로세스 모니터를 사용해 워커가 멈추지 않고 동작하도록 설정해야 합니다.

명령어 실행 시 `-v` 플래그를 추가하면, 실행된 잡 ID를 명령어 출력에 표시할 수 있습니다.

```shell
php artisan queue:work -v
```

큐 워커는 장시간 실행되는 프로세스이며, 실행 도중 부팅된 애플리케이션 상태를 메모리에 보존합니다. 따라서 워커가 실행을 시작한 이후에는 코드 변경 사항이 반영되지 않습니다. 따라서 배포 과정에서 반드시 [큐 워커를 재시작](#queue-workers-and-deployment)해야 합니다. 또한, 애플리케이션에서 생성되거나 수정된 모든 static 상태(state)는 잡별로 자동 초기화되지 않는 점도 기억하십시오.

대안으로, `queue:listen` 명령어를 사용할 수 있습니다. 이 명령어는 코드가 업데이트되거나 애플리케이션 상태를 재설정하고 싶을 때 워커를 수동으로 재시작할 필요가 없습니다. 하지만 `queue:work` 명령어에 비해 현저히 비효율적임을 유의하십시오.

```shell
php artisan queue:listen
```

<a name="running-multiple-queue-workers"></a>
#### 여러 큐 워커 실행하기

하나의 큐에 여러 워커를 할당해 병렬로 잡을 처리하려면 단순히 여러 개의 `queue:work` 프로세스를 시작하면 됩니다. 로컬에서는 터미널의 여러 탭을 사용하거나, 운영 환경에서는 프로세스 매니저의 설정을 통해 이를 구현할 수 있습니다. [Supervisor 사용 시](#supervisor-configuration) `numprocs` 설정 값을 활용할 수 있습니다.

<a name="specifying-the-connection-queue"></a>
#### 커넥션 및 큐 지정하기

워커가 사용할 큐 커넥션을 지정할 수도 있습니다. `work` 명령에 전달하는 커넥션 이름은 `config/queue.php` 설정 파일에 정의된 커넥션 중 하나여야 합니다.

```shell
php artisan queue:work redis
```

기본적으로 `queue:work` 명령어는 지정한 커넥션의 기본 큐에만 있는 잡을 처리합니다. 그러나, 특정 큐만 처리하도록 워커를 더 구체적으로 설정할 수 있습니다. 예를 들어, 모든 이메일 작업이 `redis` 큐 커넥션의 `emails` 큐에서 처리된다면, 해당 큐만 담당하는 워커를 다음과 같이 실행할 수 있습니다.

```shell
php artisan queue:work redis --queue=emails
```

<a name="processing-a-specified-number-of-jobs"></a>
#### 지정된 개수의 잡만 처리하기

`--once` 옵션을 사용하면, 워커가 큐에서 단 하나의 잡만 처리하도록 지시할 수 있습니다.

```shell
php artisan queue:work --once
```

`--max-jobs` 옵션을 사용하면, 해당 개수만큼만 잡을 처리한 후 종료됩니다. 이 옵션은 [Supervisor](#supervisor-configuration)와 함께 사용하면, 워커가 일정한 잡 수를 처리할 때마다 자동으로 재시작되어 누적된 메모리가 해제될 수 있도록 하는 데 유용합니다.

```shell
php artisan queue:work --max-jobs=1000
```

<a name="processing-all-queued-jobs-then-exiting"></a>
#### 큐에 쌓인 모든 잡을 처리한 후 종료하기

`--stop-when-empty` 옵션을 사용하면, 워커가 남아있는 모든 잡을 처리한 뒤 정상적으로 종료합니다. 이 옵션은 예를 들어 도커 컨테이너 내에서 라라벨 큐를 처리할 때, 큐가 비면 컨테이너를 종료하고 싶은 경우에 유용합니다.

```shell
php artisan queue:work --stop-when-empty
```

<a name="processing-jobs-for-a-given-number-of-seconds"></a>
#### 지정된 시간 동안 잡 처리하기

`--max-time` 옵션을 사용하면, 정해진 시간(초 단위) 동안 잡을 처리한 뒤 워커가 종료하도록 할 수 있습니다. 이 역시 [Supervisor](#supervisor-configuration)와 조합하여 워커가 일정 시간마다 재시작되도록 하고, 메모리 누수를 해소하는 데 유용합니다.

```shell
# 한 시간 동안 잡을 처리한 후 종료...
php artisan queue:work --max-time=3600
```

<a name="worker-sleep-duration"></a>
#### 워커 대기 시간

큐에 잡이 있으면 워커는 지연 없이 계속해서 잡을 처리합니다. 그러나 `sleep` 옵션을 지정하면, 큐에 잡이 없을 때 워커가 몇 초간 대기(수면)할지 정할 수 있습니다. 대기 중에는 워커가 새로운 잡을 처리하지 않습니다.

```shell
php artisan queue:work --sleep=3
```

<a name="maintenance-mode-queues"></a>
#### 유지보수 모드와 큐

애플리케이션이 [유지보수 모드](/docs/12.x/configuration#maintenance-mode)일 때는 큐 잡이 처리되지 않습니다. 유지보수 모드가 해제되면 잡 처리가 정상적으로 재개됩니다.

유지보수 모드에서도 큐 워커가 계속 잡을 처리하도록 강제하려면, `--force` 옵션을 사용하십시오.

```shell
php artisan queue:work --force
```

<a name="resource-considerations"></a>
#### 리소스 관리 유의사항

데몬 큐 워커는 잡을 처리할 때마다 프레임워크를 “재부팅”하지 않습니다. 따라서, 각 잡 처리가 끝난 후 무거운 리소스(예: GD 라이브러리를 사용한 이미지 처리 등)는 반드시 해제해야 합니다. 예를 들면 이미지를 처리한 뒤에는 `imagedestroy`로 메모리를 해제하세요.

<a name="queue-priorities"></a>
### 큐 우선순위

경우에 따라 큐 작업의 우선순위를 지정하고 싶을 수 있습니다. 예를 들어, `config/queue.php` 설정 파일에서 `redis` 커넥션의 기본 `queue` 값을 `low`로 지정했다고 합시다. 하지만 때로는 잡을 `high` 우선순위 큐에 삽입하고 싶을 수 있습니다.

```php
dispatch((new Job)->onQueue('high'));
```

`high` 큐의 잡을 모두 처리한 뒤 `low` 큐의 잡을 처리하도록 워커를 시작하려면, `work` 명령어에 쉼표로 구분한 큐 이름 목록을 전달합니다.

```shell
php artisan queue:work --queue=high,low
```

<a name="queue-workers-and-deployment"></a>
### 큐 워커와 배포

워커는 장시간 동작하는 프로세스이므로, 코드 변경 사항을 감지하지 않습니다. 따라서, 가장 간단한 배포 방법은 배포 과정에서 워커를 재시작하는 것입니다. `queue:restart` 명령어를 실행하면 모든 워커가 처리 중인 현재 잡을 끝낸 뒤 정상적으로 종료합니다.

```shell
php artisan queue:restart
```

이 명령은 모든 큐 워커에게 현재 잡을 마친 후 정상적으로 종료하라고 지시합니다. 잡의 손실 없이 안전하게 워커를 재시작할 수 있습니다. 해당 명령이 실행되어 워커가 종료되면, 반드시 [Supervisor](#supervisor-configuration) 같은 프로세스 매니저가 워커를 자동으로 다시 시작하게 만들어야 합니다.

> [!NOTE]
> 큐는 [캐시](/docs/12.x/cache)에 재시작 신호를 저장하므로, 이 기능을 사용하기 전에 적절한 캐시 드라이버가 애플리케이션에 제대로 설정되어 있는지 확인해야 합니다.

<a name="job-expirations-and-timeouts"></a>
### 잡 만료와 타임아웃

<a name="job-expiration"></a>
#### 잡 만료

`config/queue.php` 설정 파일에서 각 큐 커넥션에는 `retry_after` 옵션이 있습니다. 이 옵션은 한 잡이 처리 중일 때, 몇 초간 대기한 후 다시 처리할지 여부를 결정합니다. 예를 들어, `retry_after` 값이 90이라면 잡이 90초 동안 처리되고도 아직 release 또는 삭제되지는 않았을 때, 잡은 큐로 다시 돌아가 재시도를 하게 됩니다. 보통, `retry_after` 값은 잡이 충분히 완수될 수 있는 최대시간(초)으로 설정합니다.

> [!WARNING]
> `retry_after` 옵션이 없는 유일한 큐 커넥션은 Amazon SQS입니다. SQS의 경우, [기본 가시성 타임아웃(Default Visibility Timeout)](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/AboutVT.html)이 AWS 콘솔 내에서 관리되므로 해당 옵션이 적용되지 않습니다.

<a name="worker-timeouts"></a>
#### 워커 타임아웃

`queue:work` Artisan 명령어는 `--timeout` 옵션을 제공합니다. 기본값은 60초입니다. 잡이 이 값(초)보다 더 오래 처리된다면, 해당 잡을 수행하던 워커는 에러와 함께 종료됩니다. 보통 [서버에 구성된 프로세스 매니저](#supervisor-configuration)가 자동으로 워커를 재시작하도록 설정합니다.

```shell
php artisan queue:work --timeout=60
```

`retry_after` 설정 옵션과 `--timeout` CLI 옵션은 서로 다르지만, 잡이 손실되지 않고 딱 한 번만 제대로 처리되도록 협업합니다.

> [!WARNING]
> `--timeout` 값은 항상 `retry_after`값보다 몇 초 짧게 지정해야 합니다. 그래야 워커가 멈춘 잡을 재시도하기 전에 해당 워커가 종료되어, 한 잡이 중복 처리되는 문제가 발생하지 않습니다. 만약 `--timeout` 값이 `retry_after` 설정 값보다 더 길면, 특정 잡이 두 번 이상 처리될 수 있습니다.

<a name="supervisor-configuration"></a>
## Supervisor 구성

운영 환경에서는 `queue:work` 프로세스가 항상 계속 동작하도록 하는 관리가 필요합니다. `queue:work` 프로세스는 워커 타임아웃 초과나 `queue:restart` 명령 등 여러 이유로 중단될 수 있습니다.

따라서, 워커 프로세스가 종료될 경우를 감지해 자동으로 재시작해 주는 프로세스 모니터를 구성해야 합니다. 또한, 프로세스 모니터를 통해 동시에 몇 개의 `queue:work` 프로세스를 실행할지 지정할 수도 있습니다. Supervisor는 리눅스 환경에서 자주 사용되는 대표적인 프로세스 모니터이며, 다음 문서에서는 Supervisor 설정 방법을 안내합니다.

<a name="installing-supervisor"></a>
#### Supervisor 설치

Supervisor는 리눅스 운영 체제용 프로세스 모니터로, `queue:work` 프로세스를 자동으로 재시작해줍니다. Ubuntu 에서는 다음 명령으로 Supervisor를 설치할 수 있습니다.

```shell
sudo apt-get install supervisor
```

> [!NOTE]
> Supervisor 직접 설정 및 관리를 복잡하게 느끼신다면, 라라벨 큐 워커 실행에 최적화된 완전관리형 플랫폼인 [Laravel Cloud](https://cloud.laravel.com) 사용을 고려해보세요.

<a name="configuring-supervisor"></a>
#### Supervisor 설정

Supervisor 설정 파일은 보통 `/etc/supervisor/conf.d` 디렉터리에 저장됩니다. 이 디렉터리 내에 감시할 프로세스를 정의한 여러 개의 설정 파일을 만들 수 있습니다. 예를 들어, `laravel-worker.conf` 파일을 하나 만들어서 아래처럼 `queue:work` 프로세스를 시작 및 모니터링하도록 설정할 수 있습니다.

```ini
[program:laravel-worker]
process_name=%(program_name)s_%(process_num)02d
command=php /home/forge/app.com/artisan queue:work sqs --sleep=3 --tries=3 --max-time=3600
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
user=forge
numprocs=8
redirect_stderr=true
stdout_logfile=/home/forge/app.com/worker.log
stopwaitsecs=3600
```

이 예시에서 `numprocs`는 Supervisor가 8개의 `queue:work` 프로세스를 실행하면서 모두 감시하도록 지시합니다. 설정에서 `command` 지시어는 원하는 큐 커넥션과 워커 옵션에 맞게 수정해야 합니다.

> [!WARNING]
> `stopwaitsecs` 값은 가장 오래 실행되는 잡이 소요하는 시간보다 크게 설정해야 합니다. 그렇지 않으면 Supervisor가 잡이 완료되기 전에 해당 잡을 강제로 종료시킬 수 있습니다.

<a name="starting-supervisor"></a>
#### Supervisor 시작하기

설정 파일을 만든 뒤에는 다음 명령어를 차례로 실행해 Supervisor 설정을 갱신하고 프로세스를 시작할 수 있습니다.

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start "laravel-worker:*"
```

Supervisor에 대한 자세한 내용은 [Supervisor 공식 문서](http://supervisord.org/index.html)를 참고하십시오.

<a name="dealing-with-failed-jobs"></a>
## 실패한 잡 처리하기

때로는 큐에 등록된 잡이 실패할 수도 있습니다. 너무 걱정하지 마세요! 라라벨은 [잡 최대 시도 횟수](#max-job-attempts-and-timeout)를 지정하고, 비동기 잡이 이 횟수를 초과하여 실패했을 때 `failed_jobs` 데이터베이스 테이블에 자동으로 기록하는 편리한 방법을 제공합니다. [동기적으로 디스패치된 잡](/docs/12.x/queues#synchronous-dispatching)이 실패한 경우 이 테이블에 저장되지 않고, 예외가 애플리케이션에서 바로 처리됩니다.

`failed_jobs` 테이블을 생성하는 마이그레이션은 신규 라라벨 애플리케이션에는 기본으로 포함되어 있습니다. 만약 애플리케이션에 해당 마이그레이션이 없다면, 아래 명령들로 마이그레이션을 생성할 수 있습니다.

```shell
php artisan make:queue-failed-table

php artisan migrate
```

[큐 워커](#running-the-queue-worker) 프로세스를 실행할 때 `queue:work` 명령어의 `--tries` 옵션을 통해 잡을 시도할 최대 횟수를 지정할 수 있습니다. 별도의 값을 지정하지 않으면 잡은 한 번만 시도되거나, 잡 클래스의 `$tries` 프로퍼티에 정의된 횟수만큼 시도됩니다.

```shell
php artisan queue:work redis --tries=3
```

`--backoff` 옵션을 사용하면, 예외가 발생해 잡이 재시도될 때 라라벨이 몇 초를 대기할지 지정할 수 있습니다. 기본적으로는 잡이 즉시 다시 큐에 등록됩니다.

```shell
php artisan queue:work redis --tries=3 --backoff=3
```

잡 클래스에서 개별적으로 예외 발생 후 재시도까지의 대기 시간을 지정하고 싶다면, `backoff` 프로퍼티를 정의하면 됩니다.

```php
/**
 * 잡을 재시도하기 전 대기할 초 수
 *
 * @var int
 */
public $backoff = 3;
```

보다 복잡하게 잡 별 재시도 대기 시간을 계산하려면, 잡 클래스에 `backoff` 메서드를 정의할 수 있습니다.

```php
/**
 * 잡을 재시도하기 전 대기할 초 수 계산
 */
public function backoff(): int
{
    return 3;
}
```

배열을 반환하도록 하면 "지수(backoff) 증가"도 쉽게 구현할 수 있습니다. 아래 예시에서, 첫 번째 재시도는 1초, 두 번째는 5초, 세 번째는 10초, 그 이상은 매번 10초로 대기합니다.

```php
/**
 * 잡을 재시도하기 전 대기할 초 수 계산
 *
 * @return array<int, int>
 */
public function backoff(): array
{
    return [1, 5, 10];
}
```

<a name="cleaning-up-after-failed-jobs"></a>
### 실패한 잡 후처리

특정 잡이 실패했을 때 사용자에게 알림을 보내거나, 잡이 부분적으로 진행한 작업을 되돌리고 싶을 수 있습니다. 이를 위해 잡 클래스 내에 `failed` 메서드를 정의할 수 있습니다. 실패를 유발한 `Throwable` 인스턴스가 `failed` 메서드에 전달됩니다.

```php
<?php

namespace App\Jobs;

use App\Models\Podcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;
use Throwable;

class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    /**
     * 새로운 잡 인스턴스 생성자
     */
    public function __construct(
        public Podcast $podcast,
    ) {}

    /**
     * 잡 실행
     */
    public function handle(AudioProcessor $processor): void
    {
        // 업로드된 팟캐스트 처리...
    }

    /**
     * 잡 실패 처리
     */
    public function failed(?Throwable $exception): void
    {
        // 실패 알림 전송 등...
    }
}
```

> [!WARNING]
> `failed` 메서드가 호출되기 전에 잡의 새 인스턴스가 만들어지므로, `handle` 메서드 안에서 변경된 어떤 클래스 속성 값도 손실됩니다.

<a name="retrying-failed-jobs"></a>
### 실패한 잡 재시도

`failed_jobs` 데이터베이스 테이블에 기록된 모든 실패한 잡을 확인하려면 `queue:failed` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan queue:failed
```

`queue:failed` 명령어는 잡 ID, 커넥션, 큐, 실패 시각 등의 정보를 표시합니다. 각각의 잡 ID는 실패한 잡을 재시도할 때 사용됩니다. 예를 들어, ID가 `ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece`인 잡을 재시도하려면 아래와 같이 명령을 입력합니다.

```shell
php artisan queue:retry ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece
```

필요하다면 여러 개의 ID를 한꺼번에 전달할 수도 있습니다.

```shell
php artisan queue:retry ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece 91401d2c-0784-4f43-824c-34f94a33c24d
```

특정 큐에 있는 모든 실패 잡을 재시도하려면:

```shell
php artisan queue:retry --queue=name
```

모든 실패 잡을 한 번에 재시도하려면 ID로 `all`을 전달하세요.

```shell
php artisan queue:retry all
```

실패한 잡 하나를 삭제하고 싶다면 `queue:forget` 명령을 쓸 수 있습니다.

```shell
php artisan queue:forget 91401d2c-0784-4f43-824c-34f94a33c24d
```

> [!NOTE]
> [Horizon](/docs/12.x/horizon)을 사용할 경우, 실패한 잡을 삭제할 때는 `queue:forget` 대신 `horizon:forget` 명령을 사용해야 합니다.

`failed_jobs` 테이블에 있는 모든 실패 잡을 삭제하려면 `queue:flush` 명령어를 사용하세요.

```shell
php artisan queue:flush
```

<a name="ignoring-missing-models"></a>
### 존재하지 않는 모델 무시하기

잡에 Eloquent 모델을 주입할 때, 모델은 큐에 넣기 전에 자동으로 직렬화되고, 큐 워커에서 처리할 때 데이터베이스에서 다시 조회됩니다. 그런데, 잡이 처리되기 전에 모델이 삭제된다면 잡은 `ModelNotFoundException`으로 실패하게 될 수 있습니다.

간편하게, 잡 클래스의 `deleteWhenMissingModels` 속성을 `true`로 설정하면, 없는 모델이 필요한 잡은 조용히 삭제되고 예외가 발생하지 않습니다.

```php
/**
 * 모델이 더 이상 존재하지 않으면 잡을 삭제할지 여부
 *
 * @var bool
 */
public $deleteWhenMissingModels = true;
```

<a name="pruning-failed-jobs"></a>
### 실패한 잡 정리

애플리케이션의 `failed_jobs` 테이블 내 오래된 기록을 삭제하려면 `queue:prune-failed` Artisan 명령어를 실행하세요.

```shell
php artisan queue:prune-failed
```

기본적으로, 24시간이 지난 모든 실패 잡 기록은 삭제됩니다. `--hours` 옵션을 제공하면 최근 N시간 이내에 추가된 실패 기록만 남기고 그 이전의 기록은 삭제됩니다. 예를 들어 아래 명령은 48시간 이전에 추가된 모든 실패 기록을 제거합니다.

```shell
php artisan queue:prune-failed --hours=48
```

<a name="storing-failed-jobs-in-dynamodb"></a>
### 실패한 잡을 DynamoDB에 저장하기

라라벨은 [DynamoDB](https://aws.amazon.com/dynamodb)를 사용해 실패한 잡 기록 역시 관계형 데이터베이스 테이블 대신 저장하는 기능을 지원합니다. 마찬가지로 모든 실패 잡 기록을 저장할 DynamoDB 테이블을 직접 생성해야 합니다. 일반적으로 테이블 이름은 `failed_jobs`가 되지만, 실제 테이블 이름은 애플리케이션의 `queue` 설정 파일 내 `queue.failed.table` 설정 값을 따릅니다.

`failed_jobs` 테이블에는 문자열 타입의 기본 파티션 키 `application`과 문자열 타입의 기본 정렬 키 `uuid`가 있어야 합니다. `application`에는 애플리케이션의 `app` 설정 파일 내 `name` 값이 들어갑니다. 이 키 구조 덕분에 여러 라라벨 애플리케이션의 실패 잡을 하나의 테이블에 저장할 수 있습니다.

AWS SDK를 꼭 설치해, 라라벨 애플리케이션이 Amazon DynamoDB와 통신할 수 있도록 하십시오.

```shell
composer require aws/aws-sdk-php
```

그 다음, `queue.failed.driver` 설정 값을 `dynamodb`로 지정합니다. 또한 실패 잡 설정 배열 안에 `key`, `secret`, `region` 옵션을 정의해야 하며, AWS 인증에 사용됩니다. `dynamodb` 드라이버를 사용할 때는 `queue.failed.database` 옵션은 필요하지 않습니다.

```php
'failed' => [
    'driver' => env('QUEUE_FAILED_DRIVER', 'dynamodb'),
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'table' => 'failed_jobs',
],
```

<a name="disabling-failed-job-storage"></a>
### 실패한 잡 저장 비활성화

실패한 잡을 저장하지 않고 그냥 무시하려면 `queue.failed.driver` 설정 값을 `null`로 지정하면 됩니다. 보통 `QUEUE_FAILED_DRIVER` 환경 변수로 손쉽게 설정할 수 있습니다.

```ini
QUEUE_FAILED_DRIVER=null
```

<a name="failed-job-events"></a>
### 실패한 잡 이벤트

잡이 실패할 때 호출되는 이벤트 리스너를 등록하려면, `Queue` 파사드의 `failing` 메서드를 사용할 수 있습니다. 예를 들어, 라라벨에 포함된 `AppServiceProvider`의 `boot` 메서드에서 이벤트에 클로저를 이렇게 연결할 수 있습니다.

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Queue;
use Illuminate\Support\ServiceProvider;
use Illuminate\Queue\Events\JobFailed;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 등록
     */
    public function register(): void
    {
        // ...
    }

    /**
     * 애플리케이션 서비스 부트스트랩
     */
    public function boot(): void
    {
        Queue::failing(function (JobFailed $event) {
            // $event->connectionName
            // $event->job
            // $event->exception
        });
    }
}
```

<a name="clearing-jobs-from-queues"></a>

## 큐에서 작업 삭제하기

> [!NOTE]
> [Horizon](/docs/12.x/horizon)을 사용하는 경우에는 `queue:clear` 명령어 대신 `horizon:clear` 명령어를 사용하여 큐의 작업을 삭제해야 합니다.

기본 연결의 기본 큐에 있는 모든 작업을 삭제하고 싶다면, `queue:clear` 아티즌 명령어를 사용할 수 있습니다.

```shell
php artisan queue:clear
```

특정 연결 및 큐에서 작업을 삭제하고 싶다면, `connection` 인수와 `queue` 옵션을 함께 사용할 수 있습니다.

```shell
php artisan queue:clear redis --queue=emails
```

> [!WARNING]
> 큐에서 작업 삭제 기능은 SQS, Redis, 데이터베이스 큐 드라이버에서만 사용할 수 있습니다. 또한 SQS의 메시지 삭제는 최대 60초가 소요되므로, 큐를 비운 뒤 최대 60초 이내에 SQS 큐로 전송된 작업 역시 삭제될 수 있습니다.

<a name="monitoring-your-queues"></a>
## 큐 모니터링

만약 큐에 갑작스럽게 작업이 몰릴 경우, 큐가 과부하되어 작업이 완료되기까지 오랜 대기 시간이 발생할 수 있습니다. 원한다면, 큐에 쌓인 작업 수가 지정한 임계값을 초과할 때 라라벨에서 알림을 보낼 수 있습니다.

이를 위해 먼저 `queue:monitor` 명령어를 [매 분마다 실행](/docs/12.x/scheduling)되도록 스케줄해야 합니다. 이 명령어는 모니터링할 큐 이름 및 원하는 작업 수 임계값을 인자로 받을 수 있습니다.

```shell
php artisan queue:monitor redis:default,redis:deployments --max=100
```

이 명령어를 스케줄하는 것만으로는 큐가 과부하 상태일 때 알림이 전송되지는 않습니다. 명령어 실행 중, 큐에 쌓인 작업 수가 설정한 임계값을 넘기는 상태가 감지되면 `Illuminate\Queue\Events\QueueBusy` 이벤트가 발생합니다. 이 이벤트를 애플리케이션의 `AppServiceProvider` 안에서 리스닝하여, 개발팀 또는 본인에게 적절한 알림을 보낼 수 있습니다.

```php
use App\Notifications\QueueHasLongWaitTime;
use Illuminate\Queue\Events\QueueBusy;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\Facades\Notification;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Event::listen(function (QueueBusy $event) {
        Notification::route('mail', 'dev@example.com')
            ->notify(new QueueHasLongWaitTime(
                $event->connection,
                $event->queue,
                $event->size
            ));
    });
}
```

<a name="testing"></a>
## 테스트

작업(잡)을 디스패치(dispatch)하는 코드를 테스트할 때, 실제로 작업을 실행하지 않도록 라라벨에 지시하고 싶을 수 있습니다. 작업의 코드 자체는 별도로 직접 테스트할 수 있기 때문에, 잡을 디스패치하는 코드와 분리해서 검증하는 것이 좋습니다. 물론, 작업 코드 자체를 테스트하려면 테스트에서 작업 인스턴스를 생성하고 `handle` 메서드를 직접 호출하면 됩니다.

큐에 실제로 작업이 추가되지 않도록 하려면, `Queue` 파사드의 `fake` 메서드를 사용할 수 있습니다. 이 메서드로 큐를 가짜로 지정한 뒤, 애플리케이션에서 잡이 큐에 추가 시도가 이루어졌는지 확인(assert)할 수 있습니다.

```php tab=Pest
<?php

use App\Jobs\AnotherJob;
use App\Jobs\FinalJob;
use App\Jobs\ShipOrder;
use Illuminate\Support\Facades\Queue;

test('orders can be shipped', function () {
    Queue::fake();

    // 주문 배송 작업 수행...

    // 아무 작업도 큐에 추가되지 않았는지 확인...
    Queue::assertNothingPushed();

    // 특정 큐에 잡이 추가되었는지 확인...
    Queue::assertPushedOn('queue-name', ShipOrder::class);

    // 잡이 두 번 추가되었는지 확인...
    Queue::assertPushed(ShipOrder::class, 2);

    // 잡이 추가되지 않았는지 확인...
    Queue::assertNotPushed(AnotherJob::class);

    // Closure가 큐에 추가되었는지 확인...
    Queue::assertClosurePushed();

    // 총 몇 개의 잡이 추가되었는지 확인...
    Queue::assertCount(3);
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use App\Jobs\AnotherJob;
use App\Jobs\FinalJob;
use App\Jobs\ShipOrder;
use Illuminate\Support\Facades\Queue;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_orders_can_be_shipped(): void
    {
        Queue::fake();

        // 주문 배송 작업 수행...

        // 아무 작업도 큐에 추가되지 않았는지 확인...
        Queue::assertNothingPushed();

        // 특정 큐에 잡이 추가되었는지 확인...
        Queue::assertPushedOn('queue-name', ShipOrder::class);

        // 잡이 두 번 추가되었는지 확인...
        Queue::assertPushed(ShipOrder::class, 2);

        // 잡이 추가되지 않았는지 확인...
        Queue::assertNotPushed(AnotherJob::class);

        // Closure가 큐에 추가되었는지 확인...
        Queue::assertClosurePushed();

        // 총 몇 개의 잡이 추가되었는지 확인...
        Queue::assertCount(3);
    }
}
```

`assertPushed` 또는 `assertNotPushed` 메서드에 클로저를 전달하여, 주어진 조건(참/거짓 테스트)을 만족하는 잡이 실제로 큐에 추가되었는지 검증할 수 있습니다. 전달된 테스트에서 하나라도 참이 되면 해당 검증(assertion)은 성공합니다.

```php
Queue::assertPushed(function (ShipOrder $job) use ($order) {
    return $job->order->id === $order->id;
});
```

<a name="faking-a-subset-of-jobs"></a>
### 일부 잡만 가짜로 처리하기

특정 잡만 가짜로 처리(fake)하고, 나머지 잡들은 실제로 실행되도록 하고 싶을 수도 있습니다. 이럴 경우에는, `fake` 메서드에 가짜로 만들고 싶은 잡의 클래스명을 전달하면 됩니다.

```php tab=Pest
test('orders can be shipped', function () {
    Queue::fake([
        ShipOrder::class,
    ]);

    // 주문 배송 작업 수행...

    // 잡이 두 번 추가되었는지 확인...
    Queue::assertPushed(ShipOrder::class, 2);
});
```

```php tab=PHPUnit
public function test_orders_can_be_shipped(): void
{
    Queue::fake([
        ShipOrder::class,
    ]);

    // 주문 배송 작업 수행...

    // 잡이 두 번 추가되었는지 확인...
    Queue::assertPushed(ShipOrder::class, 2);
}
```

특정 잡들을 제외한 나머지 모든 잡을 가짜로 만들고 싶다면, `except` 메서드를 사용할 수 있습니다.

```php
Queue::fake()->except([
    ShipOrder::class,
]);
```

<a name="testing-job-chains"></a>
### 잡 체인 테스트

작업(잡) 체인을 테스트하려면, `Bus` 파사드의 fake 기능을 활용해야 합니다. `Bus` 파사드의 `assertChained` 메서드를 사용하면 [잡 체인](/docs/12.x/queues#job-chaining)이 정상적으로 디스패치 되었는지 확인할 수 있습니다. `assertChained` 메서드는 체인에 포함된 잡들의 배열을 첫 번째 인자로 받습니다.

```php
use App\Jobs\RecordShipment;
use App\Jobs\ShipOrder;
use App\Jobs\UpdateInventory;
use Illuminate\Support\Facades\Bus;

Bus::fake();

// ...

Bus::assertChained([
    ShipOrder::class,
    RecordShipment::class,
    UpdateInventory::class
]);
```

위 예시처럼, 잡 체인은 해당 잡의 클래스명 배열로도 지정할 수 있습니다. 또한, 실제 잡 인스턴스로 배열을 구성할 수도 있습니다. 이 경우, 라라벨은 잡 인스턴스의 클래스와 속성 값이 실제 애플리케이션 코드에서 체인으로 디스패치된 것과 동일한지까지 검사합니다.

```php
Bus::assertChained([
    new ShipOrder,
    new RecordShipment,
    new UpdateInventory,
]);
```

잡이 체인이 아닌 상태로 디스패치되었는지 확인하려면, `assertDispatchedWithoutChain` 메서드를 사용할 수 있습니다.

```php
Bus::assertDispatchedWithoutChain(ShipOrder::class);
```

<a name="testing-chain-modifications"></a>
#### 체인 수정 테스트

체인에 포함된 잡에서 [기존 체인에 잡을 앞이나 뒤에 추가](#adding-jobs-to-the-chain)하는 경우, 해당 잡의 `assertHasChain` 메서드를 이용해 남아있는 체인 잡들이 예상한 대로 추가되었는지 검증할 수 있습니다.

```php
$job = new ProcessPodcast;

$job->handle();

$job->assertHasChain([
    new TranscribePodcast,
    new OptimizePodcast,
    new ReleasePodcast,
]);
```

체인에 남아있는 잡 목록이 비어 있는지 검증하려면, `assertDoesntHaveChain` 메서드를 사용할 수 있습니다.

```php
$job->assertDoesntHaveChain();
```

<a name="testing-chained-batches"></a>
#### 체인에 포함된 배치 테스트

잡 체인에 [하나의 잡 배치가 포함](#chains-and-batches)되어 있는 경우, 체인 안에 실제로 원하는 배치가 있는지 확인하려면 체인 검증에서 `Bus::chainedBatch` 정의를 함께 사용하면 됩니다.

```php
use App\Jobs\ShipOrder;
use App\Jobs\UpdateInventory;
use Illuminate\Bus\PendingBatch;
use Illuminate\Support\Facades\Bus;

Bus::assertChained([
    new ShipOrder,
    Bus::chainedBatch(function (PendingBatch $batch) {
        return $batch->jobs->count() === 3;
    }),
    new UpdateInventory,
]);
```

<a name="testing-job-batches"></a>
### 잡 배치 테스트

`Bus` 파사드의 `assertBatched` 메서드는 [잡 배치](/docs/12.x/queues#job-batching)가 실제로 디스패치 되었는지 검증할 때 사용합니다. 이 메서드에 전달되는 클로저는 `Illuminate\Bus\PendingBatch` 인스턴스를 받아, 해당 배치 안의 잡 목록 등을 검사할 수 있습니다.

```php
use Illuminate\Bus\PendingBatch;
use Illuminate\Support\Facades\Bus;

Bus::fake();

// ...

Bus::assertBatched(function (PendingBatch $batch) {
    return $batch->name == 'import-csv' &&
           $batch->jobs->count() === 10;
});
```

`assertBatchCount` 메서드를 사용하면 디스패치된 배치의 개수를 검증할 수 있습니다.

```php
Bus::assertBatchCount(3);
```

`assertNothingBatched`를 사용하면 아무런 배치도 디스패치되지 않았는지 검사할 수 있습니다.

```php
Bus::assertNothingBatched();
```

<a name="testing-job-batch-interaction"></a>
#### 잡과 배치 간 상호작용 테스트

때로는 개별 잡이 자신과 연결된 배치와 어떻게 상호작용하는지 테스트해야 하는 경우도 있을 수 있습니다. (예: 잡이 자신의 배치에 대한 처리를 중단(취소)시켰는지 검증해야 할 때 등) 이럴 때는 `withFakeBatch` 메서드로 잡 인스턴스에 가짜 배치를 할당하세요. 이 메서드는 잡 인스턴스와 가짜 배치가 담긴 튜플을 반환합니다.

```php
[$job, $batch] = (new ShipOrder)->withFakeBatch();

$job->handle();

$this->assertTrue($batch->cancelled());
$this->assertEmpty($batch->added);
```

<a name="testing-job-queue-interactions"></a>
### 잡과 큐 간 상호작용 테스트

가끔은 큐에 들어간 잡이 [자기 자신을 큐로 다시 되돌리는 동작](#manually-releasing-a-job), 또는 자기 자신을 큐에서 삭제하는 동작을 테스트해야 할 수도 있습니다. 이런 큐 상호작용을 테스트하고 싶다면, 잡 인스턴스에 `withFakeQueueInteractions` 메서드를 호출하여 큐 관련 동작을 가짜로 설정할 수 있습니다.

큐 상호작용을 가짜로 만든 다음에는 잡의 `handle` 메서드를 호출하세요. 처리 후에는 잡 인스턴스를 이용해 큐와의 다양한 상호작용(`assertReleased`, `assertDeleted`, `assertNotDeleted`, `assertFailed`, `assertFailedWith`, `assertNotFailed` 등)에 대한 검증을 할 수 있습니다.

```php
use App\Exceptions\CorruptedAudioException;
use App\Jobs\ProcessPodcast;

$job = (new ProcessPodcast)->withFakeQueueInteractions();

$job->handle();

$job->assertReleased(delay: 30);
$job->assertDeleted();
$job->assertNotDeleted();
$job->assertFailed();
$job->assertFailedWith(CorruptedAudioException::class);
$job->assertNotFailed();
```

<a name="job-events"></a>
## 잡 이벤트

`Queue` [파사드](/docs/12.x/facades)의 `before`와 `after` 메서드를 사용하면, 큐에 쌓인 잡이 처리되기 전이나 후에 실행할 콜백을 지정할 수 있습니다. 이 콜백에서는 추가 로그를 남기거나, 대시보드를 위한 통계를 올리는 등의 부가 작업을 할 수 있습니다. 일반적으로 이러한 메서드는 [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에서 사용합니다. 예를 들어, 라라벨이 기본으로 제공하는 `AppServiceProvider`에서 다음과 같이 쓸 수 있습니다.

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Queue;
use Illuminate\Support\ServiceProvider;
use Illuminate\Queue\Events\JobProcessed;
use Illuminate\Queue\Events\JobProcessing;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Queue::before(function (JobProcessing $event) {
            // $event->connectionName
            // $event->job
            // $event->job->payload()
        });

        Queue::after(function (JobProcessed $event) {
            // $event->connectionName
            // $event->job
            // $event->job->payload()
        });
    }
}
```

`Queue` [파사드](/docs/12.x/facades)의 `looping` 메서드를 사용하면, 워커가 큐에서 작업을 가져오기 전에 실행되는 콜백을 등록할 수 있습니다. 예를 들어, 이전에 실패한 잡이 트랜잭션을 남긴 경우, 이를 롤백하는 Closure를 등록할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Queue;

Queue::looping(function () {
    while (DB::transactionLevel() > 0) {
        DB::rollBack();
    }
});
```