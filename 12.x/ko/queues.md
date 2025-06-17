# 큐 (Queues)

- [소개](#introduction)
    - [커넥션과 큐 비교](#connections-vs-queues)
    - [드라이버 주의사항 및 필수 조건](#driver-prerequisites)
- [잡 생성하기](#creating-jobs)
    - [잡 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [유니크 잡](#unique-jobs)
    - [암호화된 잡](#encrypted-jobs)
- [잡 미들웨어](#job-middleware)
    - [속도 제한(Rate Limiting)](#rate-limiting)
    - [잡 중첩 방지](#preventing-job-overlaps)
    - [예외 처리 스로틀링](#throttling-exceptions)
    - [잡 건너뛰기](#skipping-jobs)
- [잡 디스패치](#dispatching-jobs)
    - [지연 디스패치](#delayed-dispatching)
    - [동기식 디스패치](#synchronous-dispatching)
    - [잡과 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [잡 체이닝](#job-chaining)
    - [큐 및 커넥션 커스터마이징](#customizing-the-queue-and-connection)
    - [최대 시도 횟수 / 타임아웃 값 지정](#max-job-attempts-and-timeout)
    - [에러 처리](#error-handling)
- [잡 배치 작업](#job-batching)
    - [배치 가능한 잡 정의](#defining-batchable-jobs)
    - [배치 디스패치](#dispatching-batches)
    - [체인과 배치](#chains-and-batches)
    - [배치에 잡 추가](#adding-jobs-to-batches)
    - [배치 상태 확인](#inspecting-batches)
    - [배치 취소](#cancelling-batches)
    - [배치 실패 처리](#batch-failures)
    - [배치 정리](#pruning-batches)
    - [DynamoDB에 배치 저장](#storing-batches-in-dynamodb)
- [클로저 큐잉](#queueing-closures)
- [큐 워커 실행](#running-the-queue-worker)
    - [`queue:work` 명령어](#the-queue-work-command)
    - [큐 우선순위](#queue-priorities)
    - [큐 워커와 배포](#queue-workers-and-deployment)
    - [잡 만료 및 타임아웃](#job-expirations-and-timeouts)
- [Supervisor 설정](#supervisor-configuration)
- [실패한 잡 처리하기](#dealing-with-failed-jobs)
    - [실패한 잡 정리](#cleaning-up-after-failed-jobs)
    - [실패한 잡 재시도](#retrying-failed-jobs)
    - [누락된 모델 무시](#ignoring-missing-models)
    - [실패한 잡 정리(Pruning)](#pruning-failed-jobs)
    - [DynamoDB에 실패한 잡 저장](#storing-failed-jobs-in-dynamodb)
    - [실패한 잡 저장 비활성화](#disabling-failed-job-storage)
    - [실패한 잡 이벤트](#failed-job-events)
- [큐에서 잡 삭제](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [일부 잡 가짜(faking) 처리](#faking-a-subset-of-jobs)
    - [잡 체인 테스트](#testing-job-chains)
    - [잡 배치 테스트](#testing-job-batches)
    - [잡/큐 상호작용 테스트](#testing-job-queue-interactions)
- [잡 이벤트](#job-events)

<a name="introduction"></a>
## 소개

웹 애플리케이션을 개발하는 동안 업로드된 CSV 파일을 파싱하고 저장하는 작업처럼, 일반적인 웹 요청 중에 처리하기에는 시간이 오래 걸리는 작업들이 있을 수 있습니다. 라라벨은 이러한 작업을 백그라운드에서 처리할 수 있도록 큐에 잡을 손쉽게 생성하는 기능을 제공합니다. 시간이 많이 소요되는 작업들을 큐로 분산시키면, 애플리케이션은 웹 요청에 아주 빠르게 응답할 수 있어 사용자 경험이 크게 향상됩니다.

라라벨 큐는 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 또는 관계형 데이터베이스 등 다양한 큐 백엔드에 대해 일관된 큐잉 API를 제공합니다.

라라벨의 큐 설정 옵션들은 애플리케이션의 `config/queue.php` 설정 파일에 저장됩니다. 이 파일에는 프레임워크에서 지원하는 각 큐 드라이버에 대한 커넥션 설정이 포함되어 있습니다. 예를 들어 데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 드라이버 등이 있으며, 잡을 즉시 실행하는 동기식(synchronous) 드라이버(로컬 개발용)도 제공합니다. 또한, 큐에 쌓인 잡을 모두 무시하는 `null` 큐 드라이버도 포함되어 있습니다.

> [!NOTE]
> 라라벨은 이제 Redis 기반 큐를 위한 매우 직관적인 대시보드와 설정 시스템인 Horizon을 제공합니다. 더 자세한 내용은 [Horizon 공식 문서](/docs/12.x/horizon)를 참고하세요.

<a name="connections-vs-queues"></a>
### 커넥션과 큐 비교

라라벨의 큐를 활용하기 전에 "커넥션(connection)"과 "큐(queue)"의 개념을 구분하는 것이 중요합니다. `config/queue.php` 설정 파일에는 `connections`라는 배열 옵션이 있습니다. 이 옵션은 Amazon SQS, Beanstalk, Redis 같은 백엔드 큐 서비스에 연결하기 위한 커넥션을 정의합니다. 그러나 각각의 큐 커넥션마다 여러 개의 "큐"를 둘 수 있습니다. 큐는 각각 잡이 쌓이는 별도의 스택 또는 공간으로 생각할 수 있습니다.

각 커넥션 설정 예제에는 `queue` 속성이 있음을 참고하시기 바랍니다. 이 속성은 해당 커넥션으로 잡을 보낼 때 기본적으로 사용되는 큐를 지정합니다. 즉, 잡을 디스패치할 때 명시적으로 어느 큐에 보낼지 지정하지 않으면 해당 커넥션의 `queue` 속성에 지정된 큐에 잡이 쌓이게 됩니다.

```php
use App\Jobs\ProcessPodcast;

// 이 잡은 기본 커넥션의 기본 큐로 디스패치됩니다...
ProcessPodcast::dispatch();

// 이 잡은 기본 커넥션의 "emails" 큐로 디스패치됩니다...
ProcessPodcast::dispatch()->onQueue('emails');
```

일부 애플리케이션에서는 굳이 여러 큐를 두지 않고 간단하게 하나의 큐만 사용할 수 있습니다. 하지만 잡을 여러 큐에 분산하면, 작업의 우선순위를 다르게 지정하거나 잡의 처리 방식을 구분하고 싶은 애플리케이션에서 특히 유용합니다. 라라벨 큐 워커는 어떤 큐를 어떤 우선순위로 처리할지 지정할 수 있도록 해줍니다. 예를 들어, `high` 큐에 잡을 쌓은 뒤 해당 큐에 더 높은 우선순위를 주고 싶다면 다음과 같이 워커를 실행할 수 있습니다:

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버 주의사항 및 필수 조건

<a name="database"></a>
#### 데이터베이스 (Database)

`database` 큐 드라이버를 사용하려면, 잡 정보를 저장할 데이터베이스 테이블이 필요합니다. 일반적으로 라라벨의 기본 마이그레이션인 `0001_01_01_000002_create_jobs_table.php` [마이그레이션](/docs/12.x/migrations)에 이 내용이 포함되어 있습니다. 만약 애플리케이션에 해당 마이그레이션 파일이 없다면, 아래 Artisan 명령어를 이용해 새로 생성할 수 있습니다:

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 이용하려면, `config/database.php` 설정 파일에서 Redis 데이터베이스 커넥션을 구성해야 합니다.

> [!WARNING]
> `redis` 큐 드라이버는 Redis의 `serializer` 및 `compression` 옵션을 지원하지 않습니다.

**Redis 클러스터**

Redis 큐 커넥션이 Redis Cluster 환경에서 동작한다면 큐 이름에 [key hash tag](https://redis.io/docs/reference/cluster-spec/#hash-tags)가 반드시 포함되어야 합니다. 이렇게 하면 동일한 큐에 해당하는 모든 Redis 키가 동일한 해시 슬롯에 배치됩니다.

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

**Blocking(블로킹)**

Redis 큐 사용 시 `block_for` 설정 옵션을 통해 워커가 큐에 잡이 나타날 때까지 대기할 최대 시간을 지정할 수 있습니다. 이렇게 하면 워커 루프가 실행될 때마다 Redis에서 새로운 잡을 계속 폴링하는 것보다 더 효율적으로 동작할 수 있습니다. 예를 들어, 값을 `5`로 지정하면 잡이 나타날 때까지 5초 동안 대기하게 됩니다:

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
> `block_for` 값을 `0`으로 설정하면 잡이 등장할 때까지 무한정(block indefinitely) 대기하게 됩니다. 이 경우 SIGTERM과 같은 신호 처리가 잡이 완료될 때까지 이루어지지 않을 수 있습니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 필수 조건

아래 큐 드라이버 별로 필요한 의존성 패키지들이 있습니다. 이 의존성들은 Composer 패키지 매니저를 통해 설치할 수 있습니다.

<div class="content-list" markdown="1">

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~2.0` 또는 phpredis PHP 확장 모듈
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`

</div>

<a name="creating-jobs"></a>
## 잡 생성하기

<a name="generating-job-classes"></a>
### 잡 클래스 생성

기본적으로 애플리케이션에 생성하는 모든 큐 잡 클래스는 `app/Jobs` 디렉터리에 위치합니다. 만약 `app/Jobs` 디렉터리가 없다면, `make:job` Artisan 명령어를 실행할 때 자동으로 만들어집니다.

```shell
php artisan make:job ProcessPodcast
```

생성된 잡 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하게 되며, 이를 통해 라라벨은 이 잡을 큐에 올려 비동기적으로 실행해야 함을 인식합니다.

> [!NOTE]
> 잡 스텁은 [스터브 퍼블리싱(Stub Publishing)](/docs/12.x/artisan#stub-customization) 기능을 통해 커스터마이즈할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조

잡 클래스는 매우 간단한 구조로, 잡이 큐에서 처리될 때 호출되는 `handle` 메서드 하나만을 보유하는 것이 일반적입니다. 아래 예시 잡 클래스를 살펴보겠습니다. 이 예시에서는 팟캐스트 파일을 업로드하여 발행하기 전, 해당 파일을 처리해주는 기능을 가정합니다.

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

이 예시에서 볼 수 있듯, [Eloquent 모델](/docs/12.x/eloquent)을 큐 잡의 생성자에 직접 전달할 수 있습니다. 잡 클래스에서 사용하는 `Queueable` 트레이트 덕분에, Eloquent 모델과 이미 로드된 연관관계도 잡이 처리되는 동안 자동으로 직렬화 및 역직렬화됩니다.

큐 잡 생성자에 Eloquent 모델을 전달할 경우, 실제로 큐에 저장되는 내용은 모델의 식별자만 직렬화됩니다. 잡이 처리될 때는 큐 시스템이 알아서 전체 모델 인스턴스와 연관관계를 데이터베이스에서 다시 조회해줍니다. 이런 모델 직렬화 방식 덕분에 큐 드라이버로 전송되는 잡 데이터(payload) 크기가 훨씬 작아집니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드의 의존성 주입

큐에서 잡이 처리될 때 `handle` 메서드가 호출됩니다. 이때 잡의 `handle` 메서드에 타입힌트로 의존성을 선언하면, 라라벨 [서비스 컨테이너](/docs/12.x/container)가 해당 의존성을 자동으로 주입해줍니다.

핸들 메서드에 의존성 주입 방식을 완전히 직접 제어하고 싶다면, 컨테이너의 `bindMethod` 메서드를 사용할 수 있습니다. `bindMethod`는 콜백을 인자로 받아, 이 콜백에 잡과 컨테이너가 전달됩니다. 해당 콜백 내에서는 원하는 방식대로 `handle` 메서드를 호출할 수 있습니다. 이 방법은 일반적으로 `App\Providers\AppServiceProvider` [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에서 사용합니다.

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 이미지 원본 데이터 등과 같은 이진 데이터는 큐 잡에 전달하기 전에 반드시 `base64_encode` 함수로 인코딩해야 합니다. 그렇지 않으면 잡이 큐에 저장될 때 JSON 직렬화가 제대로 이루어지지 않을 수 있습니다.

<a name="handling-relationships"></a>
#### 큐 잡의 연관관계

큐에 잡을 쌓는 경우, 로드된 모든 Eloquent 연관관계들도 직렬화되어 함께 저장됩니다. 이로 인해 잡 문자열 크기가 꽤 커질 수 있습니다. 또한, 잡이 역직렬화되어 모델의 연관관계가 다시 조회될 때, 그 관계는 이전에 적용된 조건 없이 전체 데이터가 조회됩니다. 즉, 잡 대기 중에 모델에 제한조건을 걸었던 경우에도 역직렬화 시에는 적용되지 않습니다. 만약 특정 연관관계의 일부만 다루고 싶다면, 잡 내부에서 다시 제한조건을 걸어주는 것이 좋습니다.

또는 아예 연관관계 데이터까지 직렬화하지 않으려면, 모델에 속성 값을 지정할 때 `withoutRelations` 메서드를 호출하면 됩니다. 이 메서드를 사용하면 연관관계가 로드되지 않은 모델 인스턴스를 반환합니다.

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

PHP 생성자 프로퍼티 프로모션 문법을 사용할 때 Eloquent 모델의 연관관계 직렬화를 방지하고 싶다면, `WithoutRelations` 속성(attribute)을 사용할 수 있습니다.

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

만약 잡이 단일 모델 대신 Eloquent 모델의 컬렉션이나 배열을 전달받는 경우, 해당 컬렉션 내 모델들은 잡 실행 시 연관관계가 복구되지 않습니다. 이렇게 함으로써 한 번에 대량의 모델을 처리하는 잡이 자원을 과도하게 사용하는 것을 방지할 수 있습니다.

<a name="unique-jobs"></a>
### 유니크 잡

> [!WARNING]
> 유니크 잡을 사용하려면 [락](/docs/12.x/cache#atomic-locks)을 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 atomic lock을 지원합니다. 또한, 유니크 잡 제약 조건은 배치(batch) 내 잡에는 적용되지 않습니다.

특정 잡이 한 번에 하나만 큐에 존재하도록 보장하고 싶을 때가 있습니다. 이 경우, 잡 클래스에서 `ShouldBeUnique` 인터페이스를 구현하면 됩니다. 해당 인터페이스는 별도의 메서드 구현이 필요하지 않습니다.

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

위의 예시처럼, `UpdateSearchIndex` 잡이 유니크 잡이 되면 동일한 잡이 큐에 존재하거나 아직 처리되지 않았다면 새로운 잡은 디스패치되지 않습니다.

경우에 따라 잡이 유니크한지 판별할 고유 “키”를 정의하거나, 일정 시간(타임아웃)이 지나면 유니크 상태를 해제하고 싶을 수 있습니다. 이럴 땐 잡 클래스 내에 `uniqueId`와 `uniqueFor` 속성 혹은 메서드를 정의하면 됩니다.

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

위 예시에서는 `UpdateSearchIndex` 잡이 상품 ID별로 유니크해집니다. 즉, 동일한 상품 ID로 잡을 디스패치할 경우 기존에 큐에 올라간 잡이 완료되기 전까지는 새로운 잡이 무시됩니다. 또한 기존 잡이 1시간 내에 처리되지 않으면 유니크 락이 해제되고 동일한 키로 잡을 다시 큐에 등록할 수 있습니다.

> [!WARNING]
> 여러 대의 웹 서버나 컨테이너에서 잡을 디스패치하는 경우, 모든 서버가 동일한 중앙 캐시 서버를 사용하도록 해야 라라벨이 유니크 잡 여부를 정확히 판단할 수 있습니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 잡이 처리 시작 전까지 유니크 보장

기본적으로 유니크 잡은 잡 처리가 완료되거나 재시도 모두 실패한 후 "잠금(lock)이 해제"됩니다. 하지만 처리가 시작되기 직전에 바로 잠금을 해제하고 싶은 경우에는 `ShouldBeUnique` 대신 `ShouldBeUniqueUntilProcessing` 인터페이스를 구현하면 됩니다.

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
#### 유니크 잡 락

내부적으로 `ShouldBeUnique` 잡이 디스패치될 때 라라벨은 `uniqueId` 키로 [락](/docs/12.x/cache#atomic-locks)을 획득하려 시도합니다. 만약 락을 획득하지 못하면 잡은 디스패치되지 않습니다. 이 락은 잡 처리가 완료되거나 재시도 모두 실패하면 해제됩니다. 기본적으로 라라벨은 캐시 시스템의 기본 드라이버를 이용해 락을 획득합니다. 다른 드라이버를 사용하고 싶다면 잡 클래스에 `uniqueVia` 메서드를 정의하면 됩니다.

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
> 만약 단순히 동시에 처리되는 잡 개수만 제한하고 싶으면, [WithoutOverlapping](/docs/12.x/queues#preventing-job-overlaps) 잡 미들웨어를 사용하는 것이 더 적합합니다.

<a name="encrypted-jobs"></a>
### 암호화된 잡

라라벨은 [암호화](/docs/12.x/encryption) 기능을 통해 큐 잡 데이터의 보안성과 무결성을 보장할 수 있습니다. 시작하려면, 잡 클래스에 `ShouldBeEncrypted` 인터페이스만 추가하면 됩니다. 이렇게 하면 해당 잡은 큐에 쌓이기 전에 자동으로 암호화됩니다.

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
## 잡 미들웨어

잡 미들웨어를 활용하면, 커스텀 로직을 큐에 쌓인 잡의 실행 흐름에 감쌀 수 있어 잡 클래스 내에 중복 코드를 줄일 수 있습니다. 예를 들어 다음의 `handle` 메서드는 라라벨의 Redis 속도 제한(rate limiting) 기능을 이용해, 5초에 한 잡만 처리하도록 설정한 예시입니다.

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

이 코드는 실제로 동작하지만, Redis 속도 제한 코드로 인해 `handle` 메서드가 복잡해 보일 뿐 아니라, 동일한 속도 제한 논리를 다른 잡에서도 반복해야 하는 문제가 있습니다.

이런 경우, `handle` 메서드 내부에 직접 제한 코드를 넣는 대신 별도의 잡 미들웨어로 정의할 수 있습니다. 라라벨은 잡 미들웨어의 위치를 강제하지 않으므로, 애플리케이션 내 어디서든 자유롭게 정의할 수 있습니다. 이 예시에서는 `app/Jobs/Middleware` 디렉터리에 미들웨어를 만듭니다.

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

이처럼 [라우트 미들웨어](/docs/12.x/middleware)와 마찬가지로, 잡 미들웨어는 처리 대상 잡 인스턴스와 처리 흐름을 이어주는 콜백을 매개변수로 받습니다.

새 잡 미들웨어 클래스를 만들 때는 `make:job-middleware` Artisan 명령어를 사용할 수 있습니다. 잡 미들웨어를 만든 뒤에는 잡 클래스의 `middleware` 메서드에서 리턴해 붙여주면 적용됩니다. `make:job` Artisan 명령어로 만든 기본 잡 클래스에는 `middleware` 메서드가 없으므로, 직접 추가해주어야 합니다.

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
> 잡 미들웨어는 [큐잉되는 이벤트 리스너](/docs/12.x/events#queued-event-listeners), [메일러블](/docs/12.x/mail#queueing-mail), [알림](/docs/12.x/notifications#queueing-notifications) 등에도 적용할 수 있습니다.

<a name="rate-limiting"></a>
### 속도 제한(Rate Limiting)

방금 자신만의 속도 제한 잡 미들웨어를 만드는 방법을 소개했지만, 라라벨에는 이미 사용할 수 있는 기본 속도 제한 미들웨어가 포함되어 있습니다. [라우트 속도 제한자](/docs/12.x/routing#defining-rate-limiters)와 마찬가지로, 잡 속도 제한자는 `RateLimiter` 퍼사드의 `for` 메서드를 사용해 정의할 수 있습니다.

예를 들어, 무료 사용자는 1시간에 한 번만 데이터 백업 잡을 허용하고, 프리미엄 고객은 제한을 두지 않으면 좋겠다고 할 때, `AppServiceProvider`의 `boot` 메서드에서 이렇게 정의할 수 있습니다.

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

위 예제에서는 시간 단위로 제한을 두었지만, `perMinute` 메서드를 이용하면 분 단위 제한도 가능합니다. `by` 메서드에는 원하는 구분값을 전달할 수 있으나, 보통 고객별로 제한을 적용할 때 사용합니다.

```php
return Limit::perMinute(50)->by($job->user->id);
```

이제 이렇게 정의한 제한자를 라라벨의 `Illuminate\Queue\Middleware\RateLimited` 미들웨어에 연결해 잡에서 사용할 수 있습니다. 잡이 속도 제한을 초과할 때마다, 미들웨어는 해당 잡을 제한 시간만큼 대기하게 하고 큐에 다시 올립니다.

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

속도 제한으로 인해 잡이 대기할 때에도 해당 잡의 전체 `attempts`(시도 횟수)는 계속 증가합니다. 따라서 잡 클래스의 `tries` 및 `maxExceptions` 값을 조절하거나, [retryUntil 메서드](#time-based-attempts)를 사용해 언제까지 잡을 재시도할지 명확하게 지정해줄 수 있습니다.

또한 `releaseAfter` 메서드를 통해 잡을 다시 시도하기 전까지의 대기 시간을 초 단위로 지정할 수도 있습니다.

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

잡이 속도 제한에 걸렸을 때 재시도를 아예 원하지 않는다면, `dontRelease` 메서드를 사용할 수 있습니다.

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
> Redis를 사용하는 경우 `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어를 사용할 수 있습니다. 이 미들웨어는 Redis에 최적화되어 있어 기본 속도 제한 미들웨어보다 더 효율적입니다.

<a name="preventing-job-overlaps"></a>
### 잡 중첩 방지

라라벨에는 임의의 키를 기준으로 잡이 동시에 겹치지 않게 해주는 `Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어가 내장되어 있습니다. 이는 한 번에 하나의 잡만 특정 자원을 수정하도록 제한하고 싶을 때 유용합니다.

예를 들어 어떤 잡이 사용자의 신용점수를 업데이트한다면, 동일 사용자 ID로 여러 잡이 중첩되어 실행되지 않게 하고 싶을 때 이 미들웨어를 적용할 수 있습니다.

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

동일 타입의 중첩 잡들은 큐에 다시 릴리즈(release)됩니다. 또한, 다음 잡을 시도할 때까지 대기할 시간을 초 단위로 지정하려면 아래와 같이 작성하면 됩니다.

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

중복 잡을 아예 즉시 삭제하고, 재시도를 막고 싶다면 `dontRelease` 메서드를 사용할 수 있습니다.

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

`WithoutOverlapping` 미들웨어는 라라벨의 atomic lock 기능을 기반으로 동작합니다. 때로는 잡이 예기치 않게 실패하거나 타임아웃이 발생해 락이 해제되지 않을 수 있습니다. 이런 경우를 대비해, `expireAfter` 메서드를 통해 락 만료 시간을 명시적으로 정할 수 있습니다. 예를 들어 아래는 잡이 시작된 뒤 3분(180초) 후 락을 자동 해제하도록 설정한 예제입니다.

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
> `WithoutOverlapping` 미들웨어를 사용하려면 [락](/docs/12.x/cache#atomic-locks)을 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 드라이버가 지원합니다.

<a name="sharing-lock-keys"></a>

#### 여러 잡 클래스 간의 Lock 키 공유

기본적으로 `WithoutOverlapping` 미들웨어는 동일한 클래스의 잡(작업)이 겹쳐 실행되는 것만 막아줍니다. 따라서 서로 다른 두 잡 클래스가 같은 lock 키를 사용하더라도, 이 미들웨어만으로는 해당 잡의 중복 실행이 막히지 않습니다. 그러나 `shared` 메서드를 사용하면, 라라벨에게 잡 클래스 간에도 lock 키를 공유하여 동작하도록 지시할 수 있습니다.

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
### 예외 발생률 제한(Throttling Exceptions)

라라벨에는 예외 발생을 제한(throttle)할 수 있는 `Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어가 포함되어 있습니다. 이 미들웨어를 사용하면 잡이 일정 횟수 이상 예외를 발생시키면, 정해진 시간 간격이 지나기 전까지 해당 잡의 실행을 지연시킬 수 있습니다. 이 기능은 외부 서비스와 연동하는 잡에서 장애가 반복적으로 발생하는 상황에 유용합니다.

예를 들어, 어떤 잡이 외부 API와 통신하다가 예외를 발생시키기 시작했다고 가정해봅시다. 예외 제한을 두고 싶다면, 해당 잡의 `middleware` 메서드에서 `ThrottlesExceptions` 미들웨어를 반환하면 됩니다. 보통 이 미들웨어는 [시간 기반 재시도](#time-based-attempts)와 함께 사용하는 것이 좋습니다.

```php
use DateTime;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡이 통과해야 할 미들웨어를 반환합니다.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new ThrottlesExceptions(10, 5 * 60)];
}

/**
 * 잡이 타임아웃 처리될 시간을 반환합니다.
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(30);
}
```

위 코드에서 미들웨어 생성자의 첫 번째 인수는 예외가 몇 번 연속 발생하면 제한(throttle)할지를 의미하고, 두 번째 인수는 제한이 걸린 뒤 얼마 후에 다시 잡의 시도를 허용할지를 초 단위로 지정합니다. 예시에서는 잡이 10번 연속 예외를 발생시키면, 5분(5 * 60초) 동안 잡의 실행이 지연되며, 전체 30분의 제한 내에서만 재시도가 이뤄집니다.

잡이 예외를 던졌지만 아직 예외 횟수 임계값에 도달하지 않았다면, 기본적으로 잡은 즉시 다시 시도됩니다. 하지만 미들웨어에 `backoff` 메서드를 사용해 지연시킬 시간을 분 단위로 지정할 수도 있습니다.

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡이 통과해야 할 미들웨어를 반환합니다.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 5 * 60))->backoff(5)];
}
```

이 미들웨어는 내부적으로 라라벨의 캐시 시스템을 활용해 Rate Limiting을 구현합니다. 기본적으로 잡의 클래스명이 캐시 "키(key)"로 사용됩니다. 만약 여러 잡이 동일한 외부 서비스를 사용하고, 이들에 대해 공통적으로 예외 제한을 적용하고 싶다면, 미들웨어를 추가할 때 `by` 메서드로 원하는 키를 지정할 수 있습니다.

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡이 통과해야 할 미들웨어를 반환합니다.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->by('key')];
}
```

기본적으로 이 미들웨어는 모든 예외를 제한(throttle)합니다. 특정 예외만 제한하고 싶다면, `when` 메서드에 클로저를 전달해 그 함수가 `true`를 반환할 때만 제한이 적용되도록 할 수 있습니다.

```php
use Illuminate\Http\Client\HttpClientException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡이 통과해야 할 미들웨어를 반환합니다.
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

`when` 메서드와 달리, `deleteWhen` 메서드는 특정 예외가 발생했을 때 잡을 큐에서 즉시 삭제하도록 합니다.

```php
use App\Exceptions\CustomerDeletedException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡이 통과해야 할 미들웨어를 반환합니다.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(2, 10 * 60))->deleteWhen(CustomerDeletedException::class)];
}
```

예외 제한이 발생했을 때 해당 예외를 애플리케이션의 예외 핸들러로 보고하려면, 미들웨어를 추가할 때 `report` 메서드를 사용할 수 있습니다. 클로저를 전달해서, 특정 상황에만 예외를 보고하도록 제어할 수도 있습니다.

```php
use Illuminate\Http\Client\HttpClientException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡이 통과해야 할 미들웨어를 반환합니다.
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
> Redis를 사용한다면, `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어를 이용할 수 있습니다. 이 미들웨어는 Redis에 맞게 최적화되어 있으며, 기본 예외 제한 미들웨어보다 더 효율적으로 동작합니다.

<a name="skipping-jobs"></a>
### 잡 건너뛰기(Skipping Jobs)

`Skip` 미들웨어를 사용하면 잡의 내부 로직을 변경하지 않고도, 조건에 따라 잡을 건너뛰거나 삭제할 수 있습니다. `Skip::when` 메서드는 주어진 조건이 `true`일 때 잡을 삭제하고, `Skip::unless` 메서드는 `false`일 때 삭제합니다.

```php
use Illuminate\Queue\Middleware\Skip;

/**
 * 잡이 통과해야 할 미들웨어를 반환합니다.
 */
public function middleware(): array
{
    return [
        Skip::when($someCondition),
    ];
}
```

더 복잡한 조건식이 필요하다면, `when`과 `unless` 메서드에 `Closure`(익명 함수)를 전달할 수 있습니다.

```php
use Illuminate\Queue\Middleware\Skip;

/**
 * 잡이 통과해야 할 미들웨어를 반환합니다.
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
## 잡 디스패치(Dispatching Jobs)

잡 클래스를 작성했다면, 해당 잡 클래스의 `dispatch` 메서드를 사용해 큐에 등록(디스패치)할 수 있습니다. `dispatch` 메서드에 전달된 인수들은 잡의 생성자로 전달됩니다.

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
     * 새로운 팟캐스트를 저장합니다.
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

조건부로 잡을 디스패치하고 싶다면, `dispatchIf`와 `dispatchUnless` 메서드를 사용할 수 있습니다.

```php
ProcessPodcast::dispatchIf($accountActive, $podcast);

ProcessPodcast::dispatchUnless($accountSuspended, $podcast);
```

최신 라라벨 애플리케이션에서는, 기본 큐 드라이버가 `sync`로 설정되어 있습니다. 이 드라이버는 잡을 큐로 보내는 대신, 현재 요청에서 동기적으로 바로 실행합니다. 로컬 개발 환경에서는 편리할 수 있지만, 실제로 잡을 백그라운드에서 비동기로 실행하려면 `config/queue.php` 설정 파일에서 다른 큐 드라이버를 지정해야 합니다.

<a name="delayed-dispatching"></a>
### 잡 디스패치 지연하기(Delayed Dispatching)

잡을 바로 처리하지 않고 일정 시간 이후에 큐 워커가 처리할 수 있도록 하고 싶을 때는, 디스패치 시점에 `delay` 메서드를 사용할 수 있습니다. 예를 들어, 잡이 디스패치된 후 10분 뒤에 처리되도록 하려면 아래와 같이 작성합니다.

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
     * 새로운 팟캐스트를 저장합니다.
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

잡 클래스에 기본 delay가 설정된 경우도 있습니다. 이런 경우 delay를 무시하고 즉시 잡을 처리하고 싶다면, `withoutDelay` 메서드를 사용할 수 있습니다.

```php
ProcessPodcast::dispatch($podcast)->withoutDelay();
```

> [!WARNING]
> Amazon SQS 큐 서비스의 경우, 최대 지연 시간은 15분입니다.

<a name="dispatching-after-the-response-is-sent-to-browser"></a>
#### HTTP 응답 전송 후 잡 디스패치하기

또 다른 방법으로, 웹 서버가 FastCGI를 사용할 경우 `dispatchAfterResponse` 메서드를 이용해, HTTP 응답이 사용자 브라우저로 전송된 이후에 잡을 디스패치할 수 있습니다. 이렇게 하면 사용자 입장에서는 빠르게 응답을 받고, 잡이 백그라운드에서 실행되는 동안 애플리케이션을 사용할 수 있습니다. 이 방식은 이메일 전송처럼 1초 내외로 끝나는 짧은 작업에 사용하는 것이 좋습니다. 이 잡들은 현재 HTTP 요청 내에서 처리되므로 별도의 큐 워커가 동작할 필요가 없습니다.

```php
use App\Jobs\SendNotification;

SendNotification::dispatchAfterResponse();
```

또는 `dispatch` 헬퍼로 클로저(익명 함수)를 큐에 추가하고, `afterResponse`를 체이닝하여 HTTP 응답이 전송된 후 클로저가 실행되도록 할 수도 있습니다.

```php
use App\Mail\WelcomeMessage;
use Illuminate\Support\Facades\Mail;

dispatch(function () {
    Mail::to('taylor@example.com')->send(new WelcomeMessage);
})->afterResponse();
```

<a name="synchronous-dispatching"></a>
### 동기적 디스패치(Synchronous Dispatching)

잡을 큐에 넣지 않고, 즉시(동기적)으로 실행하고 싶다면 `dispatchSync` 메서드를 사용합니다. 이 메서드는 잡을 큐에 넣지 않고, 현재 프로세스에서 바로 처리합니다.

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
     * 새로운 팟캐스트를 저장합니다.
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
### 잡과 데이터베이스 트랜잭션(Jobs & Database Transactions)

데이터베이스 트랜잭션 내에서 잡을 디스패치하는 것도 가능합니다. 다만 잡이 정상적으로 실행될 수 있도록 주의해야 합니다. 트랜잭션 내에서 잡을 디스패치할 경우, 잡이 실제로 실행되기 전에 부모 트랜잭션의 커밋이 완료되지 않는다면, 해당 트랜잭션에서 작업한 모델이나 레코드의 변경 내용이 아직 데이터베이스에 반영되어 있지 않을 수 있습니다. 또한 트랜잭션에서 새로 생성된 모델이나 레코드는 데이터베이스에 아직 존재하지 않을 수 있습니다.

다행히도, 라라벨에서는 이런 문제를 해결할 여러 방법을 지원합니다. 먼저, 큐 연결 설정 배열에 `after_commit` 옵션을 지정하면 됩니다.

```php
'redis' => [
    'driver' => 'redis',
    // ...
    'after_commit' => true,
],
```

`after_commit` 옵션이 `true`로 설정된 경우, 트랜잭션 내에서 잡을 디스패치하면, 라라벨은 부모 트랜잭션의 커밋이 완료될 때까지 잡을 실제로 큐에 넣지 않고 기다립니다. 물론 트랜잭션이 열려 있지 않다면 즉시 잡을 디스패치합니다.

만약 트랜잭션이 예외로 인해 롤백된다면, 해당 트랜잭션 중에 디스패치된 잡들은 모두 폐기(discard)됩니다.

> [!NOTE]
> `after_commit` 설정을 `true`로 하면, 큐에 등록되는 이벤트 리스너, 메일, 알림, 브로드캐스트 이벤트도 모두 DB 트랜잭션이 모두 커밋된 후에 디스패치됩니다.

<a name="specifying-commit-dispatch-behavior-inline"></a>
#### 인라인으로 커밋(Commit) 이후 디스패치 지정

`after_commit` 옵션을 전역적으로 `true`로 하지 않더라도, 개별 잡에 대해 DB 트랜잭션 커밋 이후에 디스패치하도록 지정할 수 있습니다. 이때는 디스패치할 때 `afterCommit` 메서드를 체이닝하여 사용합니다.

```php
use App\Jobs\ProcessPodcast;

ProcessPodcast::dispatch($podcast)->afterCommit();
```

반대로, 이미 `after_commit` 옵션이 `true`로 되어 있다면, 개별 잡에 대해 트랜잭션 커밋을 기다리지 않고 곧바로 디스패치하려면 `beforeCommit` 메서드를 사용할 수 있습니다.

```php
ProcessPodcast::dispatch($podcast)->beforeCommit();
```

<a name="job-chaining"></a>
### 잡 체이닝(Job Chaining)

잡 체이닝은, 하나의 잡이 성공적으로 실행된 후 이어서 차례로 실행되어야 할 잡 목록을 지정할 수 있는 기능입니다. 체인에 포함된 잡 중 하나라도 실패하면, 뒤따르는 잡들은 실행되지 않습니다. 잡 체인을 실행하려면, `Bus` 파사드의 `chain` 메서드를 사용할 수 있습니다. 라라벨의 커맨드 버스(command bus)는 잡 디스패치의 하위 레벨 컴포넌트입니다.

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

체인에는 잡 클래스 인스턴스뿐만 아니라 클로저(익명 함수)도 추가할 수 있습니다.

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
> 잡 내부에서 `$this->delete()` 메서드를 사용해 잡을 삭제하더라도, 체이닝된 다음 잡이 실행되는 것을 막지 못합니다. 잡 체인은 오직 체인 내에서 잡이 실패했을 때만 중단됩니다.

<a name="chain-connection-queue"></a>
#### 체인에 사용할 연결(Connection) 및 큐(Queue) 지정

체인에 포함된 잡들이 사용할 큐 연결 및 큐 이름을 지정하고 싶다면, `onConnection`과 `onQueue` 메서드를 각각 체이닝하면 됩니다. 만약 잡 인스턴스가 별도로 연결/큐를 지정하지 않는다면, 여기서 지정한 설정이 적용됩니다.

```php
Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->onConnection('redis')->onQueue('podcasts')->dispatch();
```

<a name="adding-jobs-to-the-chain"></a>
#### 잡 체인에 잡 추가하기

때때로 체인 내부에서, 체인에 잡을 앞이나 뒤에 추가해야 하는 경우가 있습니다. 이럴 때는 `prependToChain` 또는 `appendToChain` 메서드를 사용할 수 있습니다.

```php
/**
 * 잡 실행
 */
public function handle(): void
{
    // ...

    // 현재 체인 앞에 추가: 지금 잡 실행 직후 실행
    $this->prependToChain(new TranscribePodcast);

    // 현재 체인 맨 뒤에 추가: 체인의 마지막에 실행
    $this->appendToChain(new TranscribePodcast);
}
```

<a name="chain-failures"></a>
#### 체인 내 실패 처리

체인 내부에서 잡이 실패했을 때 실행할 콜백을 지정하려면, `catch` 메서드를 사용할 수 있습니다. 이 콜백은 실패를 유발한 `Throwable` 인스턴스를 인자로 받습니다.

```php
use Illuminate\Support\Facades\Bus;
use Throwable;

Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->catch(function (Throwable $e) {
    // 체인 내 잡이 실패했을 때 실행되는 로직
})->dispatch();
```

> [!WARNING]
> 체인 콜백은 직렬화되어 나중에 큐 워커에 의해 실행되기 때문에, 콜백 내부에서 `$this` 변수를 사용하면 안 됩니다.

<a name="customizing-the-queue-and-connection"></a>
### 큐와 연결 커스터마이징

<a name="dispatching-to-a-particular-queue"></a>
#### 특정 큐로 잡 보내기

여러 개의 큐를 사용하면 잡을 유형별로 구분하거나, 각 큐마다 워커 수를 조절하여 우선순위를 설정할 수도 있습니다. 참고로, 이는 큐 설정 파일에서 지정하는 다른 "연결(connection)"이 아닌, 하나의 연결 내에서 큐 이름별로만 분리하는 것입니다. 잡을 디스패치할 때 `onQueue` 메서드를 사용해 큐 이름을 지정할 수 있습니다.

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
     * 새로운 팟캐스트를 저장합니다.
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

또한, 잡 클래스의 생성자 내부에서 미리 `onQueue` 메서드로 큐를 지정할 수도 있습니다.

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    /**
     * 새 잡 인스턴스를 생성합니다.
     */
    public function __construct()
    {
        $this->onQueue('processing');
    }
}
```

<a name="dispatching-to-a-particular-connection"></a>
#### 특정 연결로 잡 보내기

애플리케이션이 여러 큐 연결(connection)을 사용하는 경우, `onConnection` 메서드를 통해 잡을 특정 연결로 보낼 수 있습니다.

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
     * 새로운 팟캐스트를 저장합니다.
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

또한, `onConnection`과 `onQueue` 메서드를 함께 체이닝해서 잡을 특정 연결의 특정 큐로 동시에 보낼 수 있습니다.

```php
ProcessPodcast::dispatch($podcast)
    ->onConnection('sqs')
    ->onQueue('processing');
```

또는 잡 생성자에서 직접 연결을 지정할 수도 있습니다.

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    /**
     * 새 잡 인스턴스를 생성합니다.
     */
    public function __construct()
    {
        $this->onConnection('sqs');
    }
}
```

<a name="max-job-attempts-and-timeout"></a>

### 최대 시도 횟수 및 타임아웃 값 지정하기

<a name="max-attempts"></a>
#### 최대 시도 횟수

큐에 등록된 작업(Job) 중 오류가 발생하는 경우, 해당 작업이 무한정 반복 실행되는 것을 막고 싶을 때가 많습니다. 라라벨은 작업이 시도될 수 있는 횟수나 시간을 지정할 수 있는 다양한 방법을 제공합니다.

작업이 최대 몇 번까지 시도될 수 있는지를 지정하는 한 가지 방법은, Artisan 명령어에서 `--tries` 옵션을 사용하는 것입니다. 이 값은 워커가 처리하는 모든 작업에 적용되며, 개별 작업(class)에서 별도의 최대 시도 횟수를 지정하지 않은 경우에만 적용됩니다.

```shell
php artisan queue:work --tries=3
```

작업이 최대 시도 횟수를 초과하면, 해당 작업은 "실패"한 작업으로 간주됩니다. 실패한 작업 처리에 대한 자세한 내용은 [실패한 작업 문서](#dealing-with-failed-jobs)를 참고하시기 바랍니다. 만약 `--tries=0`을 `queue:work` 명령어에 지정하면, 작업은 무한정 재시도됩니다.

좀 더 세밀하게 제어하려면, 작업 클래스 자체에 최대 시도 횟수를 정의할 수 있습니다. 작업 클래스에 최대 시도 횟수가 지정되어 있다면, 이 값이 명령행에서 지정한 `--tries` 값보다 우선 적용됩니다.

```php
<?php

namespace App\Jobs;

class ProcessPodcast implements ShouldQueue
{
    /**
     * 이 작업이 시도될 수 있는 횟수입니다.
     *
     * @var int
     */
    public $tries = 5;
}
```

특정 작업의 최대 시도 횟수를 동적으로 제어해야 한다면, 작업 클래스에 `tries` 메서드를 정의할 수도 있습니다.

```php
/**
 * 작업이 시도될 수 있는 횟수를 반환합니다.
 */
public function tries(): int
{
    return 5;
}
```

<a name="time-based-attempts"></a>
#### 시간 기반 시도 제한

작업이 실패 전에 몇 번이나 시도될 수 있는지를 지정하는 대신, 일정 시간이 지난 후에는 더 이상 작업이 시도되지 않도록 할 수도 있습니다. 이 방법을 사용하면, 주어진 시간 내라면 몇 번이고 작업이 시도될 수 있습니다. 작업이 더 이상 시도되지 않아야 하는 시점을 정의하려면, 작업 클래스에 `retryUntil` 메서드를 추가하면 됩니다. 이 메서드는 `DateTime` 인스턴스를 반환해야 합니다.

```php
use DateTime;

/**
 * 작업의 시도 제한 시간을 반환합니다.
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(10);
}
```

만약 `retryUntil`과 `tries`를 모두 정의했다면, 라라벨은 `retryUntil` 메서드를 우선 적용합니다.

> [!NOTE]
> [큐잉된 이벤트 리스너](/docs/12.x/events#queued-event-listeners)나 [큐잉된 알림](/docs/12.x/notifications#queueing-notifications)에도 `tries` 속성이나 `retryUntil` 메서드를 정의할 수 있습니다.

<a name="max-exceptions"></a>
#### 최대 예외 횟수

때로는 작업을 여러 번 시도하되, 특정 횟수의 처리되지 않은 예외가 발생하면(즉, 단순히 `release` 메서드로 릴리즈된 경우가 아니라 실제로 예외가 발생한 경우) 작업을 실패 처리하고 싶을 때가 있습니다. 이런 경우, 작업 클래스에 `maxExceptions` 속성을 정의할 수 있습니다.

```php
<?php

namespace App\Jobs;

use Illuminate\Support\Facades\Redis;

class ProcessPodcast implements ShouldQueue
{
    /**
     * 작업이 시도될 수 있는 횟수입니다.
     *
     * @var int
     */
    public $tries = 25;

    /**
     * 실패로 간주되기 전 허용할 최대 예외 횟수입니다.
     *
     * @var int
     */
    public $maxExceptions = 3;

    /**
     * 작업 실행 메서드입니다.
     */
    public function handle(): void
    {
        Redis::throttle('key')->allow(10)->every(60)->then(function () {
            // 락을 획득했으니, 팟캐스트 작업을 처리합니다...
        }, function () {
            // 락을 획득하지 못했습니다...
            return $this->release(10);
        });
    }
}
```

위 예시에서는, 어플리케이션이 Redis 락을 획득하지 못하면 작업이 10초 동안 릴리즈되며, 최대 25회까지 재시도될 수 있습니다. 그러나 만약 처리되지 않은 예외가 3회 발생하면, 해당 작업은 실패로 간주됩니다.

<a name="timeout"></a>
#### 타임아웃

대부분, 큐에 등록된 작업이 어느 정도의 시간 동안 실행될지 예측할 수 있습니다. 이런 이유로, 라라벨은 "타임아웃" 값을 지정할 수 있게 합니다. 기본적으로 타임아웃 값은 60초입니다. 작업이 타임아웃 값보다 더 오래 처리되는 경우, 해당 작업을 처리하는 워커는 에러와 함께 종료됩니다. 보통 워커 프로세스는 [서버에서 설정한 프로세스 매니저](#supervisor-configuration)에 의해 자동으로 재시작됩니다.

작업이 실행될 수 있는 최대 시간을 지정하려면, Artisan 명령어에서 `--timeout` 옵션을 사용할 수 있습니다.

```shell
php artisan queue:work --timeout=30
```

작업이 타임아웃 때문에 반복적으로 최대 시도 횟수를 초과한다면, 해당 작업은 실패로 기록됩니다.

작업 클래스 자체에서 개별 작업의 최대 실행 시간을 초 단위로 지정할 수도 있습니다. 클래스에 타임아웃 값을 지정하면, 명령행 옵션보다 더 우선 적용됩니다.

```php
<?php

namespace App\Jobs;

class ProcessPodcast implements ShouldQueue
{
    /**
     * 작업 타임아웃(초) 값입니다.
     *
     * @var int
     */
    public $timeout = 120;
}
```

가끔, 소켓이나 외부 HTTP 연결 등 I/O 블로킹 처리를 사용하는 경우, 지정한 타임아웃이 제대로 적용되지 않을 수 있습니다. 따라서 이런 기능을 사용할 때는 해당 라이브러리의 API에서도 별도로 타임아웃을 지정하는 것이 좋습니다. 예를 들어, Guzzle을 사용할 때는 반드시 연결 및 요청 타임아웃 값을 명시적으로 지정해야 합니다.

> [!WARNING]
> 작업 타임아웃을 적용하려면 `pcntl` PHP 확장이 서버에 설치되어 있어야 합니다. 또한, 작업의 "타임아웃" 값은 ["retry after" 값](#job-expiration)보다 항상 작아야 합니다. 그렇지 않으면, 실제로 작업이 끝나거나 타임아웃 되기 전에 재시도가 중첩되어 실행될 수 있습니다.

<a name="failing-on-timeout"></a>
#### 타임아웃 시 작업을 실패 처리하기

작업이 [실패](#dealing-with-failed-jobs)하도록 타임아웃 시 표시하고 싶다면, 작업 클래스에 `$failOnTimeout` 속성을 정의하면 됩니다.

```php
/**
 * 타임아웃 시 작업을 실패로 처리할지 여부입니다.
 *
 * @var bool
 */
public $failOnTimeout = true;
```

<a name="error-handling"></a>
### 에러 처리

작업이 처리되는 중에 예외가 발생하면, 해당 작업은 자동으로 다시 큐에 릴리즈되어 재시도됩니다. 작업은 어플리케이션에서 허용한 최대 시도 횟수까지 계속해서 릴리즈되어 재시도됩니다. 최대 시도 횟수는 `queue:work` Artisan 명령어에서 사용하는 `--tries` 옵션이나, 작업 클래스에 지정된 값 중 더 우선하는 쪽에 의해 결정됩니다. 큐 워커 실행 방법에 대한 자세한 내용은 [아래에서 확인할 수 있습니다](#running-the-queue-worker).

<a name="manually-releasing-a-job"></a>
#### 작업을 수동으로 릴리즈하기

때때로 작업을 직접 큐에 다시 릴리즈해서, 이후에 재시도되도록 하고 싶을 때가 있습니다. 이럴 때는 `release` 메서드를 호출하면 됩니다.

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

기본적으로 `release` 메서드는 작업을 즉시 큐에 다시 등록하여 바로 처리되도록 합니다. 하지만, 정수나 날짜 인스턴스를 인자로 전달하면 지정한 시간(초) 후까지는 작업이 처리되지 않도록 지연시킬 수 있습니다.

```php
$this->release(10);

$this->release(now()->addSeconds(10));
```

<a name="manually-failing-a-job"></a>
#### 작업을 수동으로 실패 처리하기

작업을 직접 "실패"로 처리해야 하는 경우도 있습니다. 이럴 때는 `fail` 메서드를 호출하면 됩니다.

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

예외를 발생시킨 뒤 작업을 실패 처리하고 싶다면, 예외 인스턴스를 `fail` 메서드에 전달하면 됩니다. 또는, 편의를 위해 단순히 문자열 에러 메시지를 전달할 수도 있는데, 이 경우 메시지가 예외로 변환되어 처리됩니다.

```php
$this->fail($exception);

$this->fail('Something went wrong.');
```

> [!NOTE]
> 실패한 작업에 대한 정보는 [작업 실패 처리 문서](#dealing-with-failed-jobs)를 참고하세요.

<a name="fail-jobs-on-exceptions"></a>
#### 특정 예외 발생 시 작업 즉시 실패 처리하기

`FailOnException` [작업 미들웨어](#job-middleware)를 사용하면, 특정 예외가 발생할 경우 재시도를 즉시 중단하고 작업을 실패 처리할 수 있습니다. 이 방법을 사용하면 외부 API 오류와 같은 일시적 예외일 경우에는 재시도를 계속하고, 사용자의 권한이 철회된 것처럼 영구적인 예외일 때는 작업을 바로 실패 처리할 수 있습니다.

```php
<?php

namespace App\Jobs;

use App\Models\User;
use Illuminate\Auth\Access\AuthorizationException;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\Middleware\FailOnException;
use Illuminate\Support\Facades\Http;

class SyncChatHistory implements ShouldQueue
{
    use InteractsWithQueue;

    public $tries = 3;

    /**
     * 새 작업 인스턴스를 생성합니다.
     */
    public function __construct(
        public User $user,
    ) {}

    /**
     * 작업 실행.
     */
    public function handle(): void
    {
        $user->authorize('sync-chat-history');

        $response = Http::throw()->get(
            "https://chat.laravel.test/?user={$user->uuid}
        ");

        // ...
    }

    /**
     * 작업이 거쳐야 하는 미들웨어를 반환합니다.
     */
    public function middleware(): array
    {
        return [
            new FailOnException([AuthorizationException::class])
        ];
    }
}
```

<a name="job-batching"></a>
## 작업 배치(Job Batching)

라라벨의 작업 배치 기능을 이용하면 여러 개의 작업을 한꺼번에 실행하고, 그 배치가 모두 완료되었을 때 후속 동작을 쉽게 수행할 수 있습니다. 시작에 앞서, 작업 배치에 대한 메타 정보를 저장할 데이터베이스 테이블을 만드는 마이그레이션을 생성해야 합니다. 이 마이그레이션은 `make:queue-batches-table` Artisan 명령어로 생성할 수 있습니다.

```shell
php artisan make:queue-batches-table

php artisan migrate
```

<a name="defining-batchable-jobs"></a>
### 배치로 실행 가능한 작업 정의하기

배치로 실행할 작업을 정의하려면, 일반적으로 [큐 작업을 생성](#creating-jobs)하는 것과 같이 작업을 작성하되, 작업 클래스에 `Illuminate\Bus\Batchable` 트레잇을 추가해야 합니다. 이 트레잇을 사용하면, `batch` 메서드를 통해 현재 실행 중인 배치에 대한 정보를 조회할 수 있습니다.

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
     * 작업 실행.
     */
    public function handle(): void
    {
        if ($this->batch()->cancelled()) {
            // 배치가 취소되었는지 확인...

            return;
        }

        // CSV 파일 일부 가져오기 등의 처리...
    }
}
```

<a name="dispatching-batches"></a>
### 배치 작업 디스패치하기

배치 작업을 큐에 등록하려면, `Bus` 파사드의 `batch` 메서드를 사용하면 됩니다. 보통 배치는 "완료 콜백"과 함께 사용될 때 가장 유용합니다. 콜백은 `then`, `catch`, `finally` 메서드로 지정할 수 있으며, 각 콜백이 호출될 때 `Illuminate\Bus\Batch` 인스턴스가 전달됩니다. 아래 예시에서는, 여러 작업이 각각 CSV의 일부 행을 처리하도록 배치 작업을 큐잉 합니다.

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
    // 배치가 생성되었지만 아직 작업이 추가되기 전...
})->progress(function (Batch $batch) {
    // 개별 작업이 성공적으로 완료됨...
})->then(function (Batch $batch) {
    // 모든 작업이 성공적으로 끝남...
})->catch(function (Batch $batch, Throwable $e) {
    // 첫 번째 배치 작업에서 실패 발생 감지...
})->finally(function (Batch $batch) {
    // 배치 실행이 모두 끝남...
})->dispatch();

return $batch->id;
```

배치의 ID는 `$batch->id` 속성으로 접근할 수 있고, [라라벨 커맨드 버스](#inspecting-batches)에서 배치 작업의 상태를 조회할 때 사용할 수 있습니다.

> [!WARNING]
> 배치 콜백은 직렬화되어 나중에 라라벨 큐에 의해 실행되므로, 콜백 내부에서 `$this` 변수를 사용하지 않아야 합니다. 또한, 배치로 묶인 작업은 데이터베이스 트랜잭션 내에서 실행되기 때문에, 암묵적으로 커밋을 유발하는 데이터베이스 쿼리는 작업 내에서 실행하지 않아야 합니다.

<a name="naming-batches"></a>
#### 배치 이름 지정하기

Laravel Horizon, Laravel Telescope와 같은 도구들은 배치에 이름이 있을 경우, 좀 더 읽기 쉬운 디버그 정보를 제공합니다. 배치에 임의로 이름을 부여하려면, 배치를 정의할 때 `name` 메서드를 호출하면 됩니다.

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // 모든 작업이 성공적으로 끝남...
})->name('Import CSV')->dispatch();
```

<a name="batch-connection-queue"></a>
#### 배치의 커넥션 및 큐 지정하기

배치 작업이 사용할 큐 커넥션과 큐를 지정하려면 `onConnection`, `onQueue` 메서드를 사용할 수 있습니다. 모든 배치 작업은 동일한 커넥션과 큐에서 실행되어야 합니다.

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // 모든 작업이 성공적으로 끝남...
})->onConnection('redis')->onQueue('imports')->dispatch();
```

<a name="chains-and-batches"></a>
### 체인과 배치(Chains and Batches)

[체인 작업](#job-chaining) 집합을 배열로 배치에 포함시켜줄 수도 있습니다. 예를 들어, 두 개의 작업 체인을 병렬로 실행하고, 두 체인이 모두 끝난 후 콜백을 실행할 수 있습니다.

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

반대로, [체인](#job-chaining) 내부에 배치를 정의하여, 여러 작업 배치를 순차적으로 실행할 수도 있습니다. 예를 들어, 여러 팟캐스트를 발행하는 작업 배치를 먼저 실행한 후, 알림을 보내는 작업 배치를 차례로 실행할 수 있습니다.

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
### 배치에 작업 추가하기

배치로 처리되는 작업 내부에서, 추가 작업을 동적으로 배치에 넣는 것이 유용할 때가 있습니다. 예를 들어, 수천 개의 작업을 한꺼번에 웹 요청에서 배치로 넣기에는 성능 문제가 있을 수 있으므로, 우선 "로더(Loader)" 역할의 작업만 일부 배치한 뒤, 이 작업이 실제 작업들을 추가하도록 하는 방식이 가능합니다.

```php
$batch = Bus::batch([
    new LoadImportBatch,
    new LoadImportBatch,
    new LoadImportBatch,
])->then(function (Batch $batch) {
    // 모든 작업이 성공적으로 끝남...
})->name('Import Contacts')->dispatch();
```

이 예시에서는 `LoadImportBatch` 작업이 배치 내부에서 추가 작업을 배치에 계속해서 담아줍니다. 이를 위해, 작업에서 `batch` 메서드로 접근 가능한 배치 인스턴스의 `add` 메서드를 사용합니다.

```php
use App\Jobs\ImportContacts;
use Illuminate\Support\Collection;

/**
 * 작업 실행.
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
> 작업이 속한 동일한 배치 내부에서만 새 작업을 배치에 추가할 수 있습니다.

<a name="inspecting-batches"></a>
### 배치 상태 조회하기

배치 완료 콜백에 전달되는 `Illuminate\Bus\Batch` 인스턴스는 다양한 속성 및 메서드를 제공하여, 해당 배치의 상태를 확인하고 제어할 수 있습니다.

```php
// 배치의 UUID
$batch->id;

// 배치명(지정한 경우)
$batch->name;

// 배치에 등록된 작업 개수
$batch->totalJobs;

// 아직 처리되지 않은 작업 수
$batch->pendingJobs;

// 실패한 작업 수
$batch->failedJobs;

// 지금까지 처리된 작업 수
$batch->processedJobs();

// 배치 진행도(0~100%)
$batch->progress();

// 배치가 실행 완료되었는지 여부
$batch->finished();

// 배치 실행 취소
$batch->cancel();

// 배치가 취소 상태인지 여부
$batch->cancelled();
```

<a name="returning-batches-from-routes"></a>
#### 라우트에서 배치 정보 반환하기

모든 `Illuminate\Bus\Batch` 인스턴스는 JSON 직렬화가 가능하므로, 라우트에서 직접 반환하면 배치의 진행 상태 등 정보가 담긴 JSON 데이터를 손쉽게 응답할 수 있습니다. 이를 활용해, 어플리케이션 UI에서 배치 작업의 진행 상황을 표시할 수 있습니다.

배치 ID로 배치를 조회하려면, `Bus` 파사드의 `findBatch` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Support\Facades\Bus;
use Illuminate\Support\Facades\Route;

Route::get('/batch/{batchId}', function (string $batchId) {
    return Bus::findBatch($batchId);
});
```

<a name="cancelling-batches"></a>
### 배치 취소하기

경우에 따라, 실행 중인 배치 전체를 취소해야 할 때가 있습니다. 이럴 땐, `Illuminate\Bus\Batch` 인스턴스의 `cancel` 메서드를 호출하면 배치가 취소됩니다.

```php
/**
 * 작업 실행.
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

앞선 예시들에서 볼 수 있듯이, 배치 작업 내부에서는 주로 배치가 취소되었는지 체크한 후 실행을 계속할지 결정합니다. 그러나, 좀 더 편리하게 처리하려면 작업에 `SkipIfBatchCancelled` [미들웨어](#job-middleware)를 지정할 수도 있습니다. 이 미들웨어는 해당 배치가 취소된 경우 작업이 실행되지 않도록 라라벨에 알립니다.

```php
use Illuminate\Queue\Middleware\SkipIfBatchCancelled;

/**
 * 작업이 거쳐야 하는 미들웨어를 반환합니다.
 */
public function middleware(): array
{
    return [new SkipIfBatchCancelled];
}
```

<a name="batch-failures"></a>

### 배치 실패

배치 작업 중 하나가 실패하면, `catch` 콜백(지정된 경우)이 호출됩니다. 이 콜백은 배치 내에서 처음 실패한 작업에 대해서만 호출됩니다.

<a name="allowing-failures"></a>
#### 실패 허용하기

배치에 포함된 작업이 실패하면 라라벨은 자동으로 해당 배치를 "취소됨" 상태로 표시합니다. 필요에 따라 작업이 실패해도 배치를 자동으로 취소로 표시하지 않도록 이 동작을 비활성화할 수 있습니다. 배치 디스패치 시 `allowFailures` 메서드를 호출하면 됩니다.

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // 모든 작업이 성공적으로 완료됨...
})->allowFailures()->dispatch();
```

<a name="retrying-failed-batch-jobs"></a>
#### 배치 내 실패한 작업 재시도하기

라라벨은 지정한 배치의 실패한 모든 작업을 쉽게 재시도할 수 있도록 `queue:retry-batch` Artisan 명령어를 제공합니다. `queue:retry-batch` 명령어에는 재시도할 배치의 UUID를 전달하면 됩니다.

```shell
php artisan queue:retry-batch 32dbc76c-4f82-4749-b610-a639fe0099b5
```

<a name="pruning-batches"></a>
### 배치 기록 정리(Pruning Batches)

정리를 하지 않으면 `job_batches` 테이블에 레코드가 빠르게 누적될 수 있습니다. 이를 방지하기 위해서, [스케줄러](/docs/12.x/scheduling)를 이용해 `queue:prune-batches` Artisan 명령어가 매일 실행되도록 예약하는 것이 좋습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches')->daily();
```

기본적으로, 종료된 후 24시간이 지난 모든 배치가 정리됩니다. 명령어 실행 시 `hours` 옵션을 사용하여 배치 데이터를 얼마나 오래 보관할지 지정할 수 있습니다. 예를 들어, 아래 명령어는 종료된 지 48시간이 지난 배치를 모두 삭제합니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48')->daily();
```

때때로, `jobs_batches` 테이블에는 정상적으로 완료되지 못한 배치 기록이 누적될 수 있습니다. 예를 들어, 작업이 실패했고 해당 작업이 성공적으로 재시도되지 않은 경우가 여기에 해당합니다. 이런 미완성 배치 기록을 정리하려면 `queue:prune-batches` 명령어에 `unfinished` 옵션을 사용할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48 --unfinished=72')->daily();
```

마찬가지로, `jobs_batches` 테이블에 취소된 배치 기록이 남을 수도 있습니다. 이럴 때는 `queue:prune-batches` 명령어에 `cancelled` 옵션을 사용해 취소된 배치 기록을 정리할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48 --cancelled=72')->daily();
```

<a name="storing-batches-in-dynamodb"></a>
### DynamoDB에 배치 정보 저장하기

라라벨은 [DynamoDB](https://aws.amazon.com/dynamodb)에 배치 메타 정보를 저장하는 기능도 제공합니다. 다만, 모든 배치 기록을 저장할 DynamoDB 테이블을 직접 생성해야 합니다.

일반적으로 이 테이블의 이름은 `job_batches`여야 하나, 애플리케이션의 `queue` 설정 파일에서 `queue.batching.table` 옵션에 지정된 값에 맞춰 테이블명을 정해야 합니다.

<a name="dynamodb-batch-table-configuration"></a>
#### DynamoDB 배치 테이블 구성

`job_batches` 테이블에는 문자열 타입의 기본 파티션 키 `application`과 문자열 타입의 기본 정렬 키 `id`가 있어야 합니다. `application` 키에는 해당 애플리케이션의 이름이 들어가며, 이 이름은 애플리케이션의 `app` 설정 파일에 정의된 `name` 값입니다. 애플리케이션 이름이 DynamoDB 테이블의 키 일부이기 때문에, 하나의 테이블에 여러 라라벨 애플리케이션의 작업 배치 정보를 저장할 수 있습니다.

또한, [자동 배치 정리](#pruning-batches-in-dynamodb) 기능을 활용하려면 테이블에 `ttl` 속성을 정의할 수도 있습니다.

<a name="dynamodb-configuration"></a>
#### DynamoDB 설정

먼저, 라라벨 애플리케이션이 Amazon DynamoDB와 통신할 수 있도록 AWS SDK를 설치해야 합니다.

```shell
composer require aws/aws-sdk-php
```

그 다음, `queue.batching.driver` 설정값을 `dynamodb`로 지정하세요. 또한, 인증에 필요한 `key`, `secret`, `region` 옵션을 `batching` 설정 배열에 추가해야 합니다. 이 옵션들은 AWS 인증에 사용됩니다. `dynamodb` 드라이버 사용 시 `queue.batching.database` 설정은 필요하지 않습니다.

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

[DynamoDB](https://aws.amazon.com/dynamodb)에 작업 배치 정보를 저장할 때는 기존의 관계형 데이터베이스용 배치 정리 명령어는 동작하지 않습니다. 대신 [DynamoDB의 기본 TTL 기능](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html)을 사용해서 오래된 배치 레코드를 자동으로 삭제할 수 있습니다.

DynamoDB 테이블에 `ttl` 속성을 정의했다면, 해당 배치 레코드를 어떻게 정리할지 라라벨에 알려주는 설정값을 추가할 수 있습니다. `queue.batching.ttl_attribute` 설정값에는 TTL을 저장할 속성의 이름을, `queue.batching.ttl`에는 해당 레코드를 마지막으로 업데이트하고 나서 몇 초가 지나면 삭제할지(초 단위)를 지정합니다.

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
## 클로저를 큐에 디스패치하기

작업 클래스 대신 클로저를 큐에 디스패치할 수도 있습니다. 이는 현재 요청 사이클 바깥에서 빠르고 간단하게 실행해야 하는 작업에 유용합니다. 클로저를 큐에 디스패치할 때는 클로저의 코드 내용이 암호화되어 서명되므로, 전송 중에 변경될 수 없습니다.

```php
$podcast = App\Podcast::find(1);

dispatch(function () use ($podcast) {
    $podcast->publish();
});
```

큐에 디스패치된 클로저에 이름을 지정하고 싶다면, `name` 메서드를 사용할 수 있습니다. 지정한 이름은 큐 리포팅 대시보드나 `queue:work` 명령어에서 표시됩니다.

```php
dispatch(function () {
    // ...
})->name('Publish Podcast');
```

`catch` 메서드를 사용하여, 큐에 디스패치된 클로저가 [설정된 재시도 횟수](#max-job-attempts-and-timeout)를 모두 소진한 후에도 성공적으로 완료되지 않을 경우 실행할 클로저를 지정할 수 있습니다.

```php
use Throwable;

dispatch(function () use ($podcast) {
    $podcast->publish();
})->catch(function (Throwable $e) {
    // 이 작업이 실패했습니다...
});
```

> [!WARNING]
> `catch` 콜백은 직렬화되어 이후에 라라벨 큐에서 실행됩니다. 따라서 `catch` 콜백 내부에서는 `$this` 변수를 사용해서는 안 됩니다.

<a name="running-the-queue-worker"></a>
## 큐 워커 실행하기

<a name="the-queue-work-command"></a>
### `queue:work` 명령어

라라벨은 Artisan 명령어를 통해 큐 워커를 시작하고, 큐에 새 작업이 푸시될 때마다 처리할 수 있습니다. `queue:work` Artisan 명령어로 워커를 실행할 수 있습니다. 이 명령어가 시작되면 터미널을 닫거나 직접 중단하기 전까지 계속 실행됩니다.

```shell
php artisan queue:work
```

> [!NOTE]
> `queue:work` 프로세스를 백그라운드에서 항상 실행하려면, [Supervisor](#supervisor-configuration)와 같은 프로세스 모니터를 이용해 워커가 중단되지 않도록 해야 합니다.

처리된 작업의 ID를 명령어 출력에 표시하고 싶으면 `-v` 플래그를 붙여 실행하면 됩니다.

```shell
php artisan queue:work -v
```

큐 워커는 장시간 실행되는 프로세스이며, 부팅된 애플리케이션 상태를 메모리에 저장합니다. 따라서 워커가 시작된 이후 코드 베이스가 변경되어도 이를 감지하지 못합니다. 배포 과정에서는 반드시 [큐 워커를 재시작](#queue-workers-and-deployment)해 주세요. 또한, 애플리케이션에서 생성하거나 수정한 정적 상태는 작업마다 자동으로 초기화되지 않으니 주의해야 합니다.

혹은, `queue:listen` 명령어를 사용할 수도 있습니다. 이 명령어를 사용하면 코드가 업데이트되거나 애플리케이션 상태를 재설정할 때마다 워커를 수동으로 재시작할 필요가 없습니다. 하지만, `queue:work` 명령어에 비해 비효율적이라는 점에 유의하세요.

```shell
php artisan queue:listen
```

<a name="running-multiple-queue-workers"></a>
#### 여러 큐 워커 실행하기

여러 워커를 큐에 할당해서 작업을 동시에 처리하고 싶으면, 단순히 여러 개의 `queue:work` 프로세스를 실행하면 됩니다. 이는 로컬에서는 터미널의 여러 탭을 사용하는 방식이나, 운영 환경에서는 프로세스 관리자의 설정으로 구현할 수 있습니다. [Supervisor 사용 시](#supervisor-configuration)는 `numprocs` 설정값을 활용하면 됩니다.

<a name="specifying-the-connection-queue"></a>
#### 연결(Connection) 및 큐(Queue) 지정하기

워커가 사용할 큐 연결을 지정할 수도 있습니다. `work` 명령어에 전달하는 연결 이름은 `config/queue.php` 설정 파일에 정의된 연결 중 하나와 일치해야 합니다.

```shell
php artisan queue:work redis
```

기본적으로, `queue:work` 명령어는 지정한 연결의 기본 큐에 있는 작업만 처리합니다. 그러나, 특정 큐만 처리하도록 워커를 더 세밀하게 커스터마이즈할 수도 있습니다. 예를 들어, 모든 이메일 작업을 `redis` 연결의 `emails` 큐에서 처리한다면, 다음과 같이 해당 큐만 처리하는 워커를 시작할 수 있습니다.

```shell
php artisan queue:work redis --queue=emails
```

<a name="processing-a-specified-number-of-jobs"></a>
#### 지정한 개수만큼 작업 처리하기

`--once` 옵션을 사용하면 큐에서 단 한 개의 작업만 처리하도록 워커에 지시할 수 있습니다.

```shell
php artisan queue:work --once
```

`--max-jobs` 옵션을 사용하면 워커가 지정한 개수만큼 작업을 처리한 후 종료하게 할 수 있습니다. 이 옵션은 [Supervisor](#supervisor-configuration)와 함께 사용하면 유용합니다. 지정한 작업 수만큼 처리한 후 워커를 자동으로 재시작하여 누적된 메모리를 해제할 수 있습니다.

```shell
php artisan queue:work --max-jobs=1000
```

<a name="processing-all-queued-jobs-then-exiting"></a>
#### 모든 큐 작업 처리 후 종료하기

`--stop-when-empty` 옵션을 사용하면 워커가 큐에 남은 모든 작업을 처리한 후 정상적으로 종료하도록 할 수 있습니다. 예를 들어, Docker 컨테이너에서 라라벨 큐를 처리하는 경우 컨테이너 종료 시 이 옵션이 유용합니다.

```shell
php artisan queue:work --stop-when-empty
```

<a name="processing-jobs-for-a-given-number-of-seconds"></a>
#### 지정한 시간만큼 작업 처리하기

`--max-time` 옵션을 사용하면 워커가 정해진 시간(초 단위) 동안만 작업을 처리한 후 종료하게 할 수 있습니다. 이 옵션도 [Supervisor](#supervisor-configuration)와 함께 사용하면 유용합니다.

```shell
# 1시간 동안 작업을 처리한 후 종료...
php artisan queue:work --max-time=3600
```

<a name="worker-sleep-duration"></a>
#### 워커의 대기(sleep) 시간 조정

큐에 작업이 있으면 워커는 작업 간에 딜레이 없이 계속 처리합니다. 하지만, 큐에 작업이 없으면 `sleep` 옵션에 지정된 시간(초)만큼 "잠자기" 상태가 됩니다. 대기 중에는 새로운 작업을 처리하지 않습니다.

```shell
php artisan queue:work --sleep=3
```

<a name="maintenance-mode-queues"></a>
#### 유지보수 모드와 큐

애플리케이션이 [유지보수 모드](/docs/12.x/configuration#maintenance-mode)일 때, 큐에 쌓인 작업은 처리되지 않습니다. 유지보수 모드가 해제되면 정상적으로 작업 처리가 재개됩니다.

그래도 유지보수 모드 중에 큐 워커가 작업을 계속 처리하게 하려면 `--force` 옵션을 사용할 수 있습니다.

```shell
php artisan queue:work --force
```

<a name="resource-considerations"></a>
#### 리소스 사용 주의사항

데몬 큐 워커는 각 작업을 처리하기 전에 프레임워크를 "재부팅"하지 않습니다. 따라서 각 작업이 끝날 때마다 무거운 리소스를 반드시 해제해야 합니다. 예를 들어 GD 라이브러리로 이미지 처리를 했다면, 작업이 끝난 후 `imagedestroy`로 메모리를 해제해야 합니다.

<a name="queue-priorities"></a>
### 큐 우선순위 설정

큐 처리를 우선순위에 따라 조정하고 싶은 경우가 있습니다. 예를 들어, `config/queue.php` 설정 파일에서 `redis` 연결의 기본 큐를 `low`로 지정했다고 해봅시다. 그런데, 어떤 작업은 `high` 우선순위 큐에 넣고 싶을 수도 있습니다.

```php
dispatch((new Job)->onQueue('high'));
```

`high` 큐의 작업이 모두 처리된 후에만 `low` 큐의 작업이 처리되도록 하려면, 큐 이름을 콤마로 구분하여 `work` 명령어에 전달하세요.

```shell
php artisan queue:work --queue=high,low
```

<a name="queue-workers-and-deployment"></a>
### 큐 워커와 배포

큐 워커는 장시간 실행되는 프로세스이므로, 코드가 변경되어도 자동으로 이를 인식하지 않습니다. 따라서 큐 워커를 사용하는 애플리케이션을 배포할 때는 항상 배포 과정 중 워커를 재시작해야 합니다. 모든 워커를 정상적으로 차례로 종료하도록 하려면 `queue:restart` 명령어를 실행하세요.

```shell
php artisan queue:restart
```

이 명령어는 큐 워커들에게 현재 작업을 마친 후 정상적으로 종료하라고 지시합니다. 이 명령어 실행 후에는 반드시 [Supervisor](#supervisor-configuration)와 같은 프로세스 관리자를 사용해서 워커가 자동으로 재시작되도록 해야 합니다.

> [!NOTE]
> 큐는 [캐시](/docs/12.x/cache)를 사용해 재시작 신호를 저장하므로, 이 기능을 사용하기 전에 애플리케이션에 적절한 캐시 드라이버가 설정되어 있는지 확인해야 합니다.

<a name="job-expirations-and-timeouts"></a>
### 작업 만료와 타임아웃

<a name="job-expiration"></a>
#### 작업 만료

`config/queue.php` 설정 파일에서 각 큐 연결은 `retry_after` 옵션을 지정합니다. 이 옵션은 처리 중인 작업이 얼마나 오래 처리되었는지 감시하다가, 지정된 초만큼 시간이 지나도 완료되지 않으면 해당 작업을 다시 큐에 넣어 재시도하도록 만듭니다. 예를 들어 `retry_after` 값이 90이면, 90초 동안 작업이 릴리스 또는 삭제되지 않고 처리만 계속된다면 다시 큐로 반환(release)됩니다. 이 값은 작업이 정상적으로 완료될 때까지 대략적으로 필요한 최대 시간을 고려해서 설정하세요.

> [!WARNING]
> Amazon SQS 연결만 유일하게 `retry_after` 값을 사용하지 않습니다. SQS는 [기본 Visibility Timeout](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/AboutVT.html)을 사용하며, 이 값은 AWS 콘솔에서 관리합니다.

<a name="worker-timeouts"></a>
#### 워커 타임아웃

`queue:work` Artisan 명령어는 `--timeout` 옵션을 제공합니다. 기본적으로 이 값은 60초입니다. 작업이 이 값 이상 처리되고 있으면 해당 작업을 처리하던 워커가 에러와 함께 종료됩니다. 보통 [서버에 구성된 프로세스 관리자](#supervisor-configuration)에 의해 워커가 자동으로 다시 시작됩니다.

```shell
php artisan queue:work --timeout=60
```

`retry_after` 설정과 `--timeout` CLI 옵션은 개념적으로 다르지만, 작업이 중복 처리되거나 유실되지 않도록 같이 동작합니다.

> [!WARNING]
> `--timeout` 값은 항상 `retry_after` 설정값보다 몇 초 짧게 설정해야 합니다. 그래야 작업이 중단(frozen)되었을 때 워커가 먼저 종료고, 이후 작업이 재시도됩니다. `--timeout`이 `retry_after`보다 크면, 한 작업이 두 번 처리될 수 있습니다.

<a name="supervisor-configuration"></a>
## Supervisor 설정

운영 환경에서는 `queue:work` 프로세스가 항상 실행되고 있어야 합니다. 작업자 프로세스가 워커 타임아웃이나 `queue:restart` 실행 등의 이유로 중단될 수 있으므로, 자동으로 이를 감지해 재시작하는 프로세스 관리자가 필요합니다. 또한, 여러 개의 `queue:work` 프로세스를 동시 실행하도록 지정할 수 있습니다. Supervisor는 리눅스 환경에서 널리 사용되는 프로세스 관리자로, 아래 문서에서 Supervisor 설정을 설명합니다.

<a name="installing-supervisor"></a>
#### Supervisor 설치

Supervisor는 리눅스 운영체제용 프로세스 관리자로, `queue:work` 프로세스가 비정상적으로 중단될 경우 자동으로 재시작시켜줍니다. Ubuntu 리눅스에서 Supervisor를 설치하려면, 아래 명령어를 사용하세요.

```shell
sudo apt-get install supervisor
```

> [!NOTE]
> Supervisor 설치 및 관리가 부담스럽게 느껴진다면, [Laravel Cloud](https://cloud.laravel.com)와 같이 라라벨 큐 워커 실행을 완전히 관리해주는 플랫폼을 사용하는 것을 고려해보세요.

<a name="configuring-supervisor"></a>
#### Supervisor 설정

Supervisor 설정 파일은 보통 `/etc/supervisor/conf.d` 디렉터리에 저장됩니다. 이 디렉터리 안에 여러 개의 설정 파일을 생성해서 각 프로세스의 모니터링 방법을 명시할 수 있습니다. 예를 들어, `laravel-worker.conf` 파일을 생성하여 `queue:work` 프로세스를 시작 및 모니터링하도록 설정할 수 있습니다.

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

위 예제에서 `numprocs` 지시어는 Supervisor가 8개의 `queue:work` 프로세스를 실행하고 모니터링하도록 합니다. 그리고 각 프로세스는 실패 시 자동으로 재시작됩니다. 설정의 `command` 항목은 사용하는 큐 연결 및 워커 옵션에 맞게 바꿔야 합니다.

> [!WARNING]
> `stopwaitsecs` 값이 가장 오래 처리되는 작업 소요 시간보다 크도록 설정해야 합니다. 그렇지 않으면 Supervisor가 작업이 완료되기 전에 강제로 종료할 수 있습니다.

<a name="starting-supervisor"></a>
#### Supervisor 시작하기

설정 파일을 작성한 후에는 아래 명령어로 Supervisor 설정을 갱신하고 프로세스를 시작하세요.

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start "laravel-worker:*"
```

Supervisor에 대한 더 자세한 정보는 [Supervisor 공식 문서](http://supervisord.org/index.html)를 참고하시기 바랍니다.

<a name="dealing-with-failed-jobs"></a>
## 실패한 작업 처리하기

때때로 큐에 있던 작업이 실패할 수 있습니다. 걱정하지 마세요. 모든 일이 항상 계획대로 흘러가진 않습니다! 라라벨은 [최대 재시도 횟수 지정](#max-job-attempts-and-timeout) 기능을 제공하며, 비동기 작업이 이 횟수를 초과하면 `failed_jobs` 데이터베이스 테이블에 저장됩니다. [동기 방식으로 디스패치하는 작업](/docs/12.x/queues#synchronous-dispatching)이 실패한 경우에는 이 테이블에 저장되지 않고, 해당 예외는 즉시 애플리케이션에서 처리됩니다.

신규 라라벨 프로젝트에는 보통 `failed_jobs` 테이블용 마이그레이션 파일이 미리 포함되어 있습니다. 만약 없다면, 아래와 같이 `make:queue-failed-table` 명령어로 만들 수 있습니다.

```shell
php artisan make:queue-failed-table

php artisan migrate
```

[큐 워커](#running-the-queue-worker) 프로세스를 실행할 때, `queue:work` 명령어에 `--tries` 옵션을 붙여 작업의 최대 재시도 횟수를 지정할 수 있습니다. 별도로 값을 지정하지 않으면 한 번만 시도하거나, 작업 클래스의 `$tries` 속성에 지정된 횟수만큼 재시도합니다.

```shell
php artisan queue:work redis --tries=3
```

`--backoff` 옵션을 사용하면 작업에 예외가 발생했을 때 몇 초 기다렸다가 재시도할지 지정할 수 있습니다. 기본값으로는 실패한 작업이 즉시 다시 큐에 들어갑니다.

```shell
php artisan queue:work redis --tries=3 --backoff=3
```

작업별로 예외 발생 시 얼마의 시간 후에 재시도할지 더 세밀하게 지정하려면, 작업 클래스에 `backoff` 속성을 지정할 수 있습니다.

```php
/**
 * 작업 재시도 전 대기할 시간(초).
 *
 * @var int
 */
public $backoff = 3;
```

좀 더 복잡한 로직으로 대기 시간을 계산하고 싶으면, 작업 클래스에 `backoff` 메서드를 직접 정의할 수도 있습니다.

```php
/**
 * 작업 재시도 전 대기할 시간(초)을 계산.
 */
public function backoff(): int
{
    return 3;
}
```

"지수(backoff)" 방식을 쉽게 설정하고 싶다면, `backoff` 메서드에서 배열을 반환하면 됩니다. 아래 예에서는 첫 번째는 1초, 두 번째는 5초, 세 번째는 10초, 네 번째 이후는 계속 10초를 대기하고 재시도합니다.

```php
/**
 * 작업 재시도 전 대기할 시간(초) 배열을 계산합니다.
 *
 * @return array<int, int>
 */
public function backoff(): array
{
    return [1, 5, 10];
}
```

<a name="cleaning-up-after-failed-jobs"></a>
### 실패한 작업 후 정리 작업

특정 작업이 실패했을 때 사용자에게 알림을 보내거나, 작업이 일부만 완료된 경우 취소 처리를 하고 싶을 수 있습니다. 이를 위해 작업 클래스에 `failed` 메서드를 정의할 수 있습니다. 작업이 실패한 원인이 된 `Throwable` 인스턴스가 `failed` 메서드에 인자로 전달됩니다.

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
     * 새로운 작업 인스턴스 생성자.
     */
    public function __construct(
        public Podcast $podcast,
    ) {}

    /**
     * 작업 실행 메서드.
     */
    public function handle(AudioProcessor $processor): void
    {
        // 업로드된 팟캐스트 처리...
    }

    /**
     * 작업 실패 처리 메서드.
     */
    public function failed(?Throwable $exception): void
    {
        // 사용자에게 실패 알림 전송 등...
    }
}
```

> [!WARNING]
> `failed` 메서드가 호출되기 전에 새로운 작업 인스턴스가 생성됩니다. 따라서 `handle` 메서드 내에서 변경한 클래스 속성 값은 사라지니 주의하세요.

<a name="retrying-failed-jobs"></a>
### 실패한 작업 재시도하기

실패한 작업들은 모두 `failed_jobs` 데이터베이스 테이블에 저장됩니다. 저장된 모든 실패 작업을 확인하려면 `queue:failed` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan queue:failed
```

`queue:failed` 명령어는 작업 ID, 연결, 큐 이름, 실패 시각 등 다양한 정보를 보여줍니다. 작업 ID를 사용해 실패한 작업을 다시 재시도할 수 있습니다. 예를 들어, ID가 `ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece`인 실패 작업을 재시도하려면 다음 명령어를 입력하세요.

```shell
php artisan queue:retry ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece
```

필요하다면 여러 개의 ID를 한 번에 전달할 수도 있습니다.

```shell
php artisan queue:retry ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece 91401d2c-0784-4f43-824c-34f94a33c24d
```

특정 큐에 속한 모든 실패 작업을 재시도하려면 다음과 같이 명령을 실행하세요.

```shell
php artisan queue:retry --queue=name
```

모든 실패 작업을 재시도하려면 `queue:retry` 명령어에 `all`을 ID로 전달하세요.

```shell
php artisan queue:retry all
```

실패한 작업을 삭제하려면 `queue:forget` 명령어를 사용할 수 있습니다.

```shell
php artisan queue:forget 91401d2c-0784-4f43-824c-34f94a33c24d
```

> [!NOTE]
> [Horizon](/docs/12.x/horizon)을 사용하는 경우, 실패한 작업을 삭제할 때는 `queue:forget` 대신 `horizon:forget` 명령어를 사용해야 합니다.

`failed_jobs` 테이블의 모든 실패 작업을 삭제하려면 `queue:flush` 명령어를 실행하세요.

```shell
php artisan queue:flush
```

<a name="ignoring-missing-models"></a>
### 누락된 모델 무시하기

작업에 Eloquent 모델을 주입하면, 작업이 큐에 들어갈 때 해당 모델이 자동으로 직렬화되고, 작업 처리 시 데이터베이스에서 다시 조회됩니다. 하지만 큐에서 대기하는 동안 모델이 삭제된다면, 해당 작업은 `ModelNotFoundException` 예외로 실패할 수 있습니다.

이럴 때, 작업 클래스의 `deleteWhenMissingModels` 속성을 `true`로 설정하면 누락된 모델이 있는 작업은 예외 없이 자동으로 삭제됩니다.

```php
/**
 * 모델이 존재하지 않을 경우 작업을 삭제함.
 *
 * @var bool
 */
public $deleteWhenMissingModels = true;
```

<a name="pruning-failed-jobs"></a>
### 실패한 작업 기록 정리(Pruning Failed Jobs)

애플리케이션의 `failed_jobs` 테이블에 있는 기록을 정리하려면 `queue:prune-failed` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan queue:prune-failed
```

기본적으로, 24시간이 지난 모든 실패 작업 기록이 정리됩니다. `--hours` 옵션을 사용하면 최근 N시간 이내에 추가된 실패 작업만 보존하고 그 이전 기록은 삭제됩니다. 예를 들어, 아래 명령어는 48시간 이상 지난 실패 작업 기록들을 삭제합니다.

```shell
php artisan queue:prune-failed --hours=48
```

<a name="storing-failed-jobs-in-dynamodb"></a>

### 실패한 작업을 DynamoDB에 저장하기

라라벨에서는 [DynamoDB](https://aws.amazon.com/dynamodb)에 실패한 작업 레코드를 저장하는 기능도 제공합니다. 하지만, 모든 실패한 작업 레코드를 저장할 DynamoDB 테이블을 직접 생성해야 합니다. 일반적으로 이 테이블의 이름은 `failed_jobs`로 지정하지만, 애플리케이션의 `queue` 설정 파일 내 `queue.failed.table` 설정값에 따라 적절한 테이블명을 지정해야 합니다.

`failed_jobs` 테이블에는 문자열 타입의 파티션 키 `application`과 문자열 타입의 소트 키 `uuid`가 있어야 합니다. 이때 `application` 키에는 애플리케이션의 `app` 설정 파일의 `name` 설정값이 들어갑니다. 이렇게 하면 애플리케이션 이름이 DynamoDB 테이블 키의 일부가 되므로, 여러 라라벨 애플리케이션의 실패한 작업들을 하나의 테이블에 함께 저장할 수 있습니다.

또한, 라라벨 애플리케이션이 Amazon DynamoDB와 통신할 수 있도록 AWS SDK 설치가 필요합니다.

```shell
composer require aws/aws-sdk-php
```

그 다음, `queue.failed.driver` 설정 옵션 값을 `dynamodb`로 지정합니다. 그리고 `failed` 작업 설정 배열 내에 `key`, `secret`, `region` 옵션도 함께 지정해야 합니다. 이 값들은 AWS 인증에 사용됩니다. `dynamodb` 드라이버를 사용할 때는 `queue.failed.database` 설정 옵션이 필요하지 않습니다.

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
### 실패한 작업 저장 비활성화

실패한 작업을 저장하지 않고 즉시 폐기하려면, `queue.failed.driver` 설정 옵션의 값을 `null`로 지정하면 됩니다. 일반적으로는 `QUEUE_FAILED_DRIVER` 환경 변수로도 쉽게 설정할 수 있습니다.

```ini
QUEUE_FAILED_DRIVER=null
```

<a name="failed-job-events"></a>
### 실패한 작업 이벤트

작업이 실패했을 때 호출되는 이벤트 리스너를 등록하고 싶다면, `Queue` 파사드의 `failing` 메서드를 사용할 수 있습니다. 예를 들어, 라라벨에 포함되어 있는 `AppServiceProvider`의 `boot` 메서드에서 이 이벤트에 클로저를 연결할 수 있습니다.

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Queue;
use Illuminate\Support\ServiceProvider;
use Illuminate\Queue\Events\JobFailed;

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
        Queue::failing(function (JobFailed $event) {
            // $event->connectionName
            // $event->job
            // $event->exception
        });
    }
}
```

<a name="clearing-jobs-from-queues"></a>
## 큐에서 작업 비우기

> [!NOTE]
> [Horizon](/docs/12.x/horizon)을 사용하는 경우, 큐에서 작업을 비울 때는 `queue:clear` 명령어 대신 `horizon:clear` 명령어를 사용해야 합니다.

기본 연결의 기본 큐에 있는 모든 작업을 삭제하고 싶다면, 다음과 같이 `queue:clear` 아티즌 명령어를 사용할 수 있습니다.

```shell
php artisan queue:clear
```

특정 연결이나 큐에서 작업을 삭제하고자 한다면, `connection` 인수와 `queue` 옵션을 함께 지정할 수 있습니다.

```shell
php artisan queue:clear redis --queue=emails
```

> [!WARNING]
> 큐에서 작업을 비우는 기능은 SQS, Redis, 데이터베이스 큐 드라이버만 지원합니다. 또한, SQS 메시지 삭제 과정에는 최대 60초가 걸릴 수 있으므로, 큐를 비운 후 60초 이내에 SQS 큐로 보낸 작업도 삭제될 수 있습니다.

<a name="monitoring-your-queues"></a>
## 큐 모니터링

큐에 갑작스럽게 많은 작업이 몰리면 과부하되어 작업 완료까지 대기 시간이 길어질 수 있습니다. 이런 상황을 대비해, 큐 대기 작업 개수가 지정한 임계값을 초과하면 라라벨에서 알림을 보낼 수 있습니다.

우선 [매 분마다 실행](https://laravel.kr/docs/12.x/scheduling)되도록 `queue:monitor` 명령어를 스케줄링해야 합니다. 이 명령어에는 모니터링할 큐 이름과 원하는 작업 수 임계값을 지정할 수 있습니다.

```shell
php artisan queue:monitor redis:default,redis:deployments --max=100
```

이 명령어를 스케줄링 만으로는 큐가 과부하 상태일 때 알림이 전송되지 않습니다. 지정한 임계값을 초과하는 큐가 발견되면 `Illuminate\Queue\Events\QueueBusy` 이벤트가 발생합니다. 이 이벤트를 애플리케이션의 `AppServiceProvider`에서 리스닝하여 알림을 받을 수 있습니다.

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

작업(Job)을 디스패치하는 코드를 테스트할 때, 실제로 작업을 큐에 넣어 실행하지 않고, 작업 코드는 개별적으로 테스트하고 싶을 수 있습니다. 실제 작업 자체를 테스트할 때는, 작업 인스턴스를 직접 만들어 테스트 내에서 `handle` 메서드를 호출하면 됩니다.

큐에 작업이 실제로 푸시되지 않게 하려면 `Queue` 파사드의 `fake` 메서드를 사용할 수 있습니다. 이 메서드를 사용한 후에는, 애플리케이션이 큐에 작업을 푸시하려 했는지 다양한 검증 메서드로 확인할 수 있습니다.

```php tab=Pest
<?php

use App\Jobs\AnotherJob;
use App\Jobs\FinalJob;
use App\Jobs\ShipOrder;
use Illuminate\Support\Facades\Queue;

test('orders can be shipped', function () {
    Queue::fake();

    // Perform order shipping...

    // Assert that no jobs were pushed...
    Queue::assertNothingPushed();

    // Assert a job was pushed to a given queue...
    Queue::assertPushedOn('queue-name', ShipOrder::class);

    // Assert a job was pushed twice...
    Queue::assertPushed(ShipOrder::class, 2);

    // Assert a job was not pushed...
    Queue::assertNotPushed(AnotherJob::class);

    // Assert that a Closure was pushed to the queue...
    Queue::assertClosurePushed();

    // Assert the total number of jobs that were pushed...
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

        // Perform order shipping...

        // Assert that no jobs were pushed...
        Queue::assertNothingPushed();

        // Assert a job was pushed to a given queue...
        Queue::assertPushedOn('queue-name', ShipOrder::class);

        // Assert a job was pushed twice...
        Queue::assertPushed(ShipOrder::class, 2);

        // Assert a job was not pushed...
        Queue::assertNotPushed(AnotherJob::class);

        // Assert that a Closure was pushed to the queue...
        Queue::assertClosurePushed();

        // Assert the total number of jobs that were pushed...
        Queue::assertCount(3);
    }
}
```

`assertPushed` 또는 `assertNotPushed` 메서드에 클로저를 전달하면, 특정 조건을 만족하는 작업이 푸시됐는지 확인할 수 있습니다. 조건을 만족하는 작업이 한 개라도 푸시된다면 검증에 통과합니다.

```php
Queue::assertPushed(function (ShipOrder $job) use ($order) {
    return $job->order->id === $order->id;
});
```

<a name="faking-a-subset-of-jobs"></a>
### 일부 작업만 페이크하기

특정 작업만 큐에 페이크로 감싸고, 나머지 작업은 평소처럼 정상 실행되도록 하고 싶을 때는 `fake` 메서드에 페이크 처리할 작업의 클래스명을 지정하여 전달하면 됩니다.

```php tab=Pest
test('orders can be shipped', function () {
    Queue::fake([
        ShipOrder::class,
    ]);

    // Perform order shipping...

    // Assert a job was pushed twice...
    Queue::assertPushed(ShipOrder::class, 2);
});
```

```php tab=PHPUnit
public function test_orders_can_be_shipped(): void
{
    Queue::fake([
        ShipOrder::class,
    ]);

    // Perform order shipping...

    // Assert a job was pushed twice...
    Queue::assertPushed(ShipOrder::class, 2);
}
```

특정 작업만 제외하고 나머지 모든 작업을 페이크로 감싸고 싶다면, `except` 메서드를 사용할 수 있습니다.

```php
Queue::fake()->except([
    ShipOrder::class,
]);
```

<a name="testing-job-chains"></a>
### 작업 체인 테스트하기

작업 체인 기능을 테스트하려면 `Bus` 파사드의 페이크 기능을 활용해야 합니다. `Bus` 파사드의 `assertChained` 메서드를 사용하면 [작업 체인](https://laravel.kr/docs/12.x/queues#job-chaining)이 제대로 디스패치됐는지 확인할 수 있습니다. `assertChained` 메서드에는 체인에 들어갈 작업 클래스를 배열로 전달합니다.

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

위 예시처럼, 체인 배열에는 작업 클래스명을 나열할 수도 있고, 실제 작업 인스턴스를 전달할 수도 있습니다. 실제 인스턴스를 전달할 경우, 라라벨은 작업 인스턴스의 클래스와 속성 값이 실제 디스패치된 작업 체인과 동일한지 확인합니다.

```php
Bus::assertChained([
    new ShipOrder,
    new RecordShipment,
    new UpdateInventory,
]);
```

`assertDispatchedWithoutChain` 메서드를 사용하면, 체인 없이 푸시된 단일 작업이 있는지 확인할 수 있습니다.

```php
Bus::assertDispatchedWithoutChain(ShipOrder::class);
```

<a name="testing-chain-modifications"></a>
#### 체인 수정 테스트하기

체인에 연결된 작업에서 [기존 체인에 작업을 추가하거나 앞에 덧붙이는 경우](#adding-jobs-to-the-chain), 해당 작업의 `assertHasChain` 메서드로 남은 체인 작업이 기대한 대로 구성되어 있는지 검증할 수 있습니다.

```php
$job = new ProcessPodcast;

$job->handle();

$job->assertHasChain([
    new TranscribePodcast,
    new OptimizePodcast,
    new ReleasePodcast,
]);
```

`assertDoesntHaveChain` 메서드를 사용하면, 작업에 남은 체인이 비어있는지(없음)를 확인할 수 있습니다.

```php
$job->assertDoesntHaveChain();
```

<a name="testing-chained-batches"></a>
#### 체인 내 배치 작업 테스트

작업 체인에 [배치 작업이 포함되어 있다면](#chains-and-batches), 체인 검증 코드 내에 `Bus::chainedBatch` 정의를 삽입해 체인에 배치가 기대한 대로 포함되어 있는지 확인할 수 있습니다.

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
### 배치 작업 테스트

[배치 작업](https://laravel.kr/docs/12.x/queues#job-batching)이 제대로 디스패치됐는지 확인하려면, `Bus` 파사드의 `assertBatched` 메서드를 사용하면 됩니다. 이 메서드에 전달하는 클로저에는 `Illuminate\Bus\PendingBatch` 인스턴스가 주어지며, 이를 통해 배치 내 작업을 검사할 수 있습니다.

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

디스패치된 배치 개수가 지정한 개수와 일치하는지 확인하려면 `assertBatchCount` 메서드를 사용할 수 있습니다.

```php
Bus::assertBatchCount(3);
```

배치가 아무것도 디스패치되지 않았는지 검증하려면 `assertNothingBatched`를 사용합니다.

```php
Bus::assertNothingBatched();
```

<a name="testing-job-batch-interaction"></a>
#### 작업과 배치의 상호작용 테스트

특정 작업이 배치와 상호작용했는지 개별적으로 테스트하고 싶을 때도 있습니다. 예를 들어, 작업이 배치의 진행을 취소하는 지점을 테스트하고 싶을 수 있습니다. 이를 위해 `withFakeBatch` 메서드로 작업에 페이크 배치를 할당할 수 있습니다. 이 메서드는 작업 인스턴스와 페이크 배치 인스턴스를 포함한 튜플을 반환합니다.

```php
[$job, $batch] = (new ShipOrder)->withFakeBatch();

$job->handle();

$this->assertTrue($batch->cancelled());
$this->assertEmpty($batch->added);
```

<a name="testing-job-queue-interactions"></a>
### 작업과 큐의 상호작용 테스트

때때로, 큐에 푸시된 작업이 [자신을 큐에 되돌려 놓았는지](#manually-releasing-a-job) 또는 삭제했는지 등을 테스트해야 할 수 있습니다. 이럴 때는 작업 인스턴스를 생성한 뒤 `withFakeQueueInteractions` 메서드를 호출하여 큐 상호작용을 페이크 처리합니다.

이렇게 큐 상호작용을 페이크로 만든 다음, 작업의 `handle` 메서드를 호출합니다. 이후에는 `assertReleased`, `assertDeleted`, `assertNotDeleted`, `assertFailed`, `assertFailedWith`, `assertNotFailed` 등의 메서드로 큐 상호작용 결과를 검증할 수 있습니다.

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
## 작업 이벤트

`Queue` [파사드](/docs/12.x/facades)의 `before`, `after` 메서드를 사용하면, 큐 작업이 처리되기 전/후에 실행할 콜백을 지정할 수 있습니다. 이 콜백을 활용하면 추가 로그를 남기거나 대시보드 통계를 갱신할 수 있습니다. 주로 [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에서 이 메서드들을 호출하게 됩니다. 예를 들어, 라라벨에 포함된 `AppServiceProvider`에서 다음과 같이 사용할 수 있습니다.

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

`Queue` [파사드](/docs/12.x/facades)의 `looping` 메서드를 활용하여, 워커가 큐에서 작업을 꺼내기 전에 실행될 콜백을 지정할 수 있습니다. 예를 들어, 이전에 실패한 작업으로 인해 남은 트랜잭션이 있다면 롤백 처리를 하고자 이런 콜백을 등록할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Queue;

Queue::looping(function () {
    while (DB::transactionLevel() > 0) {
        DB::rollBack();
    }
});
```