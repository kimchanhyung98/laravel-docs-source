# 큐 (Queues)

- [소개](#introduction)
    - [커넥션 vs. 큐](#connections-vs-queues)
    - [드라이버 참고사항 및 사전 준비](#driver-prerequisites)
- [잡 생성](#creating-jobs)
    - [잡 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [유니크 잡](#unique-jobs)
    - [암호화된 잡](#encrypted-jobs)
- [잡 미들웨어](#job-middleware)
    - [속도 제한](#rate-limiting)
    - [잡 중복 실행 방지](#preventing-job-overlaps)
    - [예외 제한](#throttling-exceptions)
    - [잡 건너뛰기](#skipping-jobs)
- [잡 디스패치](#dispatching-jobs)
    - [지연 디스패치](#delayed-dispatching)
    - [동기 디스패치](#synchronous-dispatching)
    - [잡 & 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [잡 체이닝](#job-chaining)
    - [큐 및 커넥션 커스터마이즈](#customizing-the-queue-and-connection)
    - [최대 재시도 횟수 / 타임아웃 지정](#max-job-attempts-and-timeout)
    - [에러 핸들링](#error-handling)
- [잡 배치](#job-batching)
    - [배치 처리 가능한 잡 정의](#defining-batchable-jobs)
    - [배치 디스패치](#dispatching-batches)
    - [체인과 배치](#chains-and-batches)
    - [배치에 잡 추가](#adding-jobs-to-batches)
    - [배치 확인](#inspecting-batches)
    - [배치 취소](#cancelling-batches)
    - [배치 실패](#batch-failures)
    - [배치 정리](#pruning-batches)
    - [DynamoDB에 배치 저장](#storing-batches-in-dynamodb)
- [클로저 큐잉](#queueing-closures)
- [큐 워커 실행](#running-the-queue-worker)
    - [`queue:work` 명령어](#the-queue-work-command)
    - [큐 우선순위](#queue-priorities)
    - [큐 워커와 배포](#queue-workers-and-deployment)
    - [잡 만료 & 타임아웃](#job-expirations-and-timeouts)
- [Supervisor 설정](#supervisor-configuration)
- [실패한 잡 처리](#dealing-with-failed-jobs)
    - [실패 잡 정리](#cleaning-up-after-failed-jobs)
    - [실패 잡 재시도](#retrying-failed-jobs)
    - [누락된 모델 무시](#ignoring-missing-models)
    - [실패 잡 가지치기](#pruning-failed-jobs)
    - [실패 잡 DynamoDB에 저장](#storing-failed-jobs-in-dynamodb)
    - [실패 잡 저장 비활성화](#disabling-failed-job-storage)
    - [실패 잡 이벤트](#failed-job-events)
- [큐에서 잡 삭제](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [잡 일부 페이크 처리](#faking-a-subset-of-jobs)
    - [잡 체인 테스트](#testing-job-chains)
    - [잡 배치 테스트](#testing-job-batches)
    - [잡/큐 상호작용 테스트](#testing-job-queue-interactions)
- [잡 이벤트](#job-events)

<a name="introduction"></a>
## 소개

웹 애플리케이션을 개발하다 보면 파일 업로드 후 CSV 파싱 및 저장과 같이 일반적인 웹 요청 내에서 처리하기엔 시간이 오래 걸리는 작업이 있을 수 있습니다. 다행히 라라벨은 이런 작업을 쉽게 백그라운드에서 처리할 수 있는 큐 잡(queued job)으로 만들 수 있도록 도와줍니다. 복잡하고 시간이 많이 걸리는 작업을 큐로 옮김으로써, 여러분의 애플리케이션은 웹 요청에 매우 빠르게 응답할 수 있고, 사용자에게 더 좋은 경험을 제공할 수 있습니다.

라라벨의 큐 기능은 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 관계형 데이터베이스 등 다양한 큐 백엔드 시스템에 대해 일관된 API를 제공합니다.

큐 관련 라라벨의 설정은 애플리케이션의 `config/queue.php` 설정 파일에 저장됩니다. 이 파일 안에는 프레임워크에 포함된 각 큐 드라이버(데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 등)와 즉시 잡을 실행하는 동기 드라이버(로컬 개발 환경 활용용)까지 모든 커넥션 설정이 담겨 있습니다. 또한, 잡을 버리지 않고 버려지는 `null` 큐 드라이버도 포함되어 있습니다.

> [!NOTE]
> 라라벨은 이제 Redis 기반 큐를 위한 아름다운 대시보드 및 설정 관리 도구인 Horizon을 제공합니다. 자세한 내용은 [Horizon 공식 문서](/docs/12.x/horizon)를 참고하시기 바랍니다.

<a name="connections-vs-queues"></a>
### 커넥션 vs. 큐

라라벨 큐를 시작하기 전에 "커넥션(connection)"과 "큐(queue)"의 차이점을 이해하는 것이 중요합니다. `config/queue.php` 설정 파일을 보면 `connections`라는 설정 배열이 있습니다. 이 옵션은 Amazon SQS, Beanstalk, Redis와 같은 백엔드 큐 서비스에 대한 커넥션을 정의합니다. 하나의 큐 커넥션은 여러 개의 "큐"를 가질 수 있으며, 각 큐는 각각의 잡 쌓는 공간(스택) 정도로 생각하면 됩니다.

각 커넥션 설정 예시에는 `queue`라는 속성이 포함되어 있습니다. 이 속성은 해당 커넥션에서 잡을 디스패치할 때 기본적으로 사용되는 큐를 지정합니다. 즉, 어떤 잡을 디스패치할 때 특별히 대상을 지정하지 않으면, 커넥션 설정에 정의된 `queue` 속성 값으로 잡이 들어가게 됩니다.

```php
use App\Jobs\ProcessPodcast;

// 이 잡은 기본 커넥션의 기본 큐로 전송됩니다...
ProcessPodcast::dispatch();

// 이 잡은 기본 커넥션의 "emails" 큐로 전송됩니다...
ProcessPodcast::dispatch()->onQueue('emails');
```

어떤 애플리케이션에서는 큐를 여러 개로 나눌 필요가 없이 단일 큐만 사용할 수도 있습니다. 반면, 여러 큐에 잡을 나눠 넣는 것은 작업 방식에 따라 우선순위를 부여하거나 유형별로 분리해야 할 때 유용합니다. 라라벨 큐 워커는 처리할 큐의 우선순위를 지정할 수 있으니, 예를 들어 잡을 `high`라는 큐에 넣었다면 이에 더 높은 처리 우선순위를 둔 워커를 실행할 수 있습니다.

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버 참고사항 및 사전 준비

<a name="database"></a>
#### 데이터베이스

`database` 큐 드라이버를 사용하려면 잡을 저장할 테이블이 필요합니다. 이 테이블은 기본적으로 라라벨의 `0001_01_01_000002_create_jobs_table.php` [데이터베이스 마이그레이션](/docs/12.x/migrations)에 포함되어 있습니다. 만약 이 마이그레이션이 없다면, `make:queue-table` 아티즌 명령어로 직접 생성할 수 있습니다.

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면, `config/database.php` 설정 파일에 Redis 데이터베이스 커넥션을 구성해야 합니다.

> [!WARNING]
> `serializer` 및 `compression`은 `redis` 큐 드라이버에서 지원되지 않습니다.

**Redis 클러스터 사용 시**

만약 Redis 큐 커넥션이 Redis 클러스터를 사용한다면, 큐 이름에 [키 해시태그(key hash tag)](https://redis.io/docs/reference/cluster-spec/#hash-tags)를 반드시 포함해야 합니다. 이를 통해 같은 큐에 해당하는 모든 Redis 키가 동일한 해시 슬롯에 저장되도록 할 수 있습니다.

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

Redis 큐 사용 시, `block_for` 설정 옵션을 사용해 워커 루프가 잡을 다시 찾으러 Redis를 폴링하기 전, 잡이 대기하기를 얼마 동안 계속할지 지정할 수 있습니다.

이 값을 조절하면 Redis를 잦은 폴링 없이도 효율적으로 사용할 수 있습니다. 예를 들어, 값이 `5`라면, 잡이 대기할 때 5초간 대기 후 다음 루프로 넘어갑니다.

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
> `block_for` 값을 `0`으로 지정하면 잡이 생길 때까지 워커가 무한 대기합니다. 이 경우, 다음 잡이 처리될 때까지는 `SIGTERM` 등의 신호를 처리하지 못하니 유의하세요.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 사전 준비 사항

다음 큐 드라이버를 이용하려면 명시된 의존성 패키지가 필요합니다. 이들 패키지는 Composer를 통해 설치할 수 있습니다.

<div class="content-list" markdown="1">

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~2.0` 또는 phpredis PHP 확장 모듈
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`

</div>

<a name="creating-jobs"></a>
## 잡 생성

<a name="generating-job-classes"></a>
### 잡 클래스 생성

기본적으로 애플리케이션의 큐잉 가능한 모든 잡은 `app/Jobs` 디렉터리에 저장됩니다. 만약 `app/Jobs` 디렉터리가 존재하지 않는다면, `make:job` 아티즌 명령어를 실행하면 자동으로 생성됩니다.

```shell
php artisan make:job ProcessPodcast
```

생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하며, 이 덕분에 라라벨은 해당 잡이 비동기적으로 큐에 넣어져야 함을 인식하게 됩니다.

> [!NOTE]
> 잡의 기본 스텁(stub) 파일은 [스텁 퍼블리싱](/docs/12.x/artisan#stub-customization) 기능을 통해 커스터마이즈할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조

잡 클래스는 매우 단순하며 보통 큐가 잡을 처리할 때 호출되는 `handle` 메서드만을 포함합니다. 예시를 들어, 팟캐스트 게시 서비스를 운영하며 업로드된 팟캐스트 파일을 게시 전 처리하는 상황을 살펴보겠습니다.

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

이 예제에서는 [Eloquent 모델](/docs/12.x/eloquent)을 직접 큐잉 잡의 생성자에 전달하는 것이 가능합니다. 잡 클래스에서 사용 중인 `Queueable` 트레이트 덕분에 Eloquent 모델 인스턴스와 함께 로드된 연관관계들도 큐에 직렬화/역직렬화되며 안정적으로 처리됩니다.

큐잉 잡의 생성자에서 Eloquent 모델을 받을 경우, 큐에는 해당 모델의 식별자만 직렬화되어 저장됩니다. 잡이 실제로 실행될 때는 큐 시스템이 데이터베이스에서 전체 모델 인스턴스와 로드된 연관관계를 자동으로 다시 조회해줍니다. 이러한 모델 직렬화 방식은 큐로 전달되는 잡의 데이터 용량을 최소화할 수 있게 해줍니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드 의존성 주입

큐에서 잡이 실행되면 `handle` 메서드가 호출됩니다. 이때 `handle` 메서드에서 의존성 타입힌트가 가능하며, 라라벨의 [서비스 컨테이너](/docs/12.x/container)가 자동으로 이 의존성을 주입해줍니다.

서비스 컨테이너가 의존성을 어떻게 주입할지 완전히 직접 제어하고 싶다면, 컨테이너의 `bindMethod` 메서드를 사용할 수 있습니다. `bindMethod`는 잡과 컨테이너를 인자로 받는 콜백을 전달받습니다. 보통 이 코드는 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 호출해주는 것이 좋습니다.

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 원시 바이너리 데이터(예: 이미지 파일 등)는 잡에 전달하기 전에 `base64_encode` 함수를 사용해 인코딩해야 큐에 JSON으로 제대로 직렬화될 수 있습니다. 그렇지 않으면 잡이 정상적으로 큐에 저장되지 않을 수 있습니다.

<a name="handling-relationships"></a>
#### 큐잉된 연관관계

큐잉 잡에 Eloquent 모델의 연관관계가 함께 포함되면 큐에 직렬화되는 잡 데이터가 매우 커질 수 있습니다. 또한, 잡이 역직렬화되어 처리될 때 연관관계들은 전체 데이터셋이 모두 데이터베이스에서 재조회됩니다. 즉, 잡이 큐에 들어갈 때 연관관계에 제약 조건이 걸렸더라도, 큐에서 로드될 때는 그런 제약이 적용되지 않습니다. 따라서, 특정 연관관계의 일부분만 사용하고 싶다면 잡 안에서 다시 쿼리 제한을 걸어주어야 합니다.

혹은 잡에 포함되는 모델에서 연관관계를 아예 직렬화하지 않으려면, 값을 세팅할 때 모델의 `withoutRelations` 메서드를 호출하면 됩니다. 이 메서드는 연관관계가 포함되지 않은 모델 인스턴스를 반환합니다.

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

만약 PHP 생성자 프로퍼티 프로모션을 쓰는 경우, Eloquent 모델의 연관관계를 직렬화하지 않게 하려면 `WithoutRelations` 속성을 사용할 수 있습니다.

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

만약 단일 모델이 아니라 여러 Eloquent 모델을 담은 컬렉션(Collection)이나 배열을 잡에 전달하면, 잡 처리 시 해당 컬렉션 내 각 모델의 연관관계는 복원되지 않습니다. 이는 다량의 모델을 다루는 잡에서 과도한 리소스 사용을 방지하기 위한 조치입니다.

<a name="unique-jobs"></a>
### 유니크 잡

> [!WARNING]
> 유니크 잡은 [락(lock)](/docs/12.x/cache#atomic-locks)을 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 원자적 락(atomic lock)을 지원합니다. 또한, 유니크 잡 제약은 잡 배치(batch) 안의 잡에는 적용되지 않습니다.

특정 잡이 항상 한 번만 큐에 올라가도록 제한하고 싶을 때가 있습니다. 잡 클래스에 `ShouldBeUnique` 인터페이스를 구현하면 이 기능을 사용할 수 있습니다. 해당 인터페이스를 구현하기만 하면 추가 메서드를 정의할 필요는 없습니다.

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

위 예제에서는 `UpdateSearchIndex` 잡이 유니크하므로, 동일한 잡이 큐에 아직 처리되지 않은 상태로 이미 올라가 있다면, 새로운 잡은 디스패치되지 않습니다.

잡마다 유니크를 판별하는 "키(key)"를 직접 지정하거나, 유니크 상태를 유지할 최대 시간을 정하고 싶다면 잡 클래스에 `uniqueId` 및 `uniqueFor` 속성 또는 메서드를 정의할 수 있습니다.

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

위 코드는 `UpdateSearchIndex` 잡이 상품 ID를 유니크 키로 사용하기 때문에, 동일한 상품 ID로 잡이 디스패치될 경우 기존 작업이 완료될 때까지 새로운 디스패치는 무시됩니다. 또한 기존 작업이 한 시간 내에 처리가 완료되지 않으면 유니크 락이 해제되고, 같은 키로 새 잡을 큐에 넣을 수 있습니다.

> [!WARNING]
> 애플리케이션이 여러 웹 서버나 컨테이너에서 잡을 디스패치하는 경우, 모든 서버가 동일한 중앙 캐시 서버를 사용해야 유니크 잡 판별이 정확히 동작합니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 잡을 처리 시작 전까지 유니크 상태 유지

기본적으로 유니크 잡은 잡 처리가 완료되거나 모든 재시도 횟수 실패 시 "언락(unlock)"됩니다. 그런데 처리 직전에만 잡을 언락하고 싶을 때는 잡에 `ShouldBeUniqueUntilProcessing` 인터페이스를 구현하면 됩니다.

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

내부적으로 `ShouldBeUnique` 잡이 디스패치되면 라라벨은 `uniqueId` 키로 [락(lock)](/docs/12.x/cache#atomic-locks)을 획득하려 시도합니다. 락을 획득하지 못하면 잡이 디스패치되지 않습니다. 이 락은 잡 처리가 끝나거나 모든 재시도가 실패할 때 해제됩니다. 기본적으로는 기본 캐시 드라이버를 사용하여 락을 관리하지만, 다른 드라이버를 직접 명시할 수도 있습니다. 이를 위해 잡 클래스에 `uniqueVia` 메서드를 정의하여 사용할 캐시 드라이버를 반환하게 할 수 있습니다.

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
> 동시 실행만 제한하고 싶다면 [WithoutOverlapping](/docs/12.x/queues#preventing-job-overlaps) 잡 미들웨어를 대신 사용하는 것이 좋습니다.

<a name="encrypted-jobs"></a>
### 암호화된 잡

라라벨은 [암호화](/docs/12.x/encryption)를 통해 잡 데이터의 개인정보 및 무결성을 보장할 수 있도록 도와줍니다. 사용 방법은 간단히 잡 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하면 됩니다. 이렇게 하면 라라벨이 잡을 큐에 넣기 전에 자동으로 암호화해줍니다.

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

잡 미들웨어(job middleware)를 사용하면 큐잉 잡 실행 전후에 커스텀 로직을 래핑 할 수 있어, 각 잡 내부에서 반복되는 코드를 줄여줄 수 있습니다. 예를 들어, 라라벨의 Redis 속도 제한(rate limiting) 기능을 활용해 5초에 한 번씩만 작업이 실행되도록 제한하려는 경우 아래와 같은 `handle` 메서드를 작성하게 됩니다.

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

이 코드는 올바르게 동작하지만, 작업마다 Redis 관련 코드를 계속 반복해서 쓸 필요가 있어 잡 클래스가 너무 복잡해집니다. 게다가 앞으로 이런 제한이 필요한 모든 잡에 동일한 코드를 한 번씩 더 작성해야 하죠.

이럴 때는 `handle` 메서드에서 직접 속도 제한을 거는 대신, 별도의 잡 미들웨어를 만들면 잡 코드가 훨씬 깔끔해집니다. 라라벨은 잡 미들웨어를 저장할 디렉터리를 별도로 정하지 않았으니, 애플리케이션 구조에 맞게 원하는 곳에 만들면 됩니다. 예시는 `app/Jobs/Middleware` 디렉터리에 두었습니다.

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

이처럼 [라우트 미들웨어](/docs/12.x/middleware)와 같이, 잡 미들웨어도 처리 대상 잡과 실행될 콜백을 전달받아 그 이후의 잡 처리를 이어나갑니다.

`make:job-middleware` 아티즌 명령어로 새로운 잡 미들웨어 클래스를 생성할 수 있습니다. 잡 미들웨어를 만들었다면, 잡 클래스의 `middleware` 메서드에서 반환하여 잡에 적용할 수 있습니다. 이 메서드는 기본적으로 `make:job` 명령어로 생성한 잡에 포함되어 있지 않으니 직접 추가해야 합니다.

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
> 잡 미들웨어는 [큐잉 이벤트 리스너](/docs/12.x/events#queued-event-listeners), [메일](/docs/12.x/mail#queueing-mail), [알림](/docs/12.x/notifications#queueing-notifications)에도 적용할 수 있습니다.

<a name="rate-limiting"></a>
### 속도 제한

방금 미들웨어로 직접 잡 속도 제한을 구현한 예시를 보았지만, 라라벨에는 이미 기본적인 잡 속도 제한 미들웨어가 포함되어 있습니다. [라우트 속도 제한자](/docs/12.x/routing#defining-rate-limiters)와 마찬가지로, 잡 속도 제한도 `RateLimiter` 파사드의 `for` 메서드를 이용해 선언적으로 정의할 수 있습니다.

예를 들어, 일반 사용자는 한 시간에 한 번씩만 백업하게 제한하고, 프리미엄 고객에게는 제한을 두지 않고 싶다고 가정합니다. 이를 위해 아래와 같이 `AppServiceProvider`의 `boot` 메서드에 `RateLimiter`를 정의할 수 있습니다.

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

위 예제는 한 시간 기준 제한이지만, `perMinute` 메서드를 사용하면 분 단위로 제한도 가능합니다. `by` 메서드에는 원하는 어떤 값을 넣어 제한 구분 기준을 정할 수 있는데, 보통 고객별로 제한하려고 해당 사용자의 ID를 넣습니다.

```php
return Limit::perMinute(50)->by($job->user->id);
```

속도 제한자를 정의했다면, `Illuminate\Queue\Middleware\RateLimited` 미들웨어를 붙여 잡에 실제로 속도 제한을 적용할 수 있습니다. 이 미들웨어는 잡이 속도 제한을 초과하면 자동으로 적절한 시간만큼 대기시켜 큐에 다시 넣어 줍니다.

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

이렇게 재시도 시에도 잡의 시도 횟수(`attempts`)는 계속 증가합니다. 따라서 잡 클래스의 `tries`와 `maxExceptions` 속성을 잘 조절하거나, 혹은 [retryUntil 메서드](#time-based-attempts)로 잡의 유효 시도 기한을 제한할 수 있습니다.

`releaseAfter` 메서드로는 잡이 속도 제한이 걸렸을 때 다음 시도를 할 수까지 대기할(지연시킬) 초(second) 단위 시간을 지정할 수 있습니다.

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

잡이 속도 제한 사유로 큐에 재시도되지 않길 원한다면, `dontRelease` 메서드를 사용할 수 있습니다.

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
> Redis를 사용한다면, Redis에 최적화된 `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어를 사용하실 것을 권장합니다. 기본 미들웨어보다 더욱 효율적입니다.

<a name="preventing-job-overlaps"></a>
### 잡 중복 실행 방지

라라벨에는 임의의 키(key)를 기준으로 잡의 중복 실행을 막는 `Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어가 포함되어 있습니다. 예를 들어, 한 번에 하나의 잡만 리소스를 수정하게 하고 싶을 때 유용합니다.

예를 들어, 사용자의 신용 점수를 업데이트하는 잡이 큐에 여러 번 올라갔을 때, 동일한 사용자 ID에 대해 중복 실행을 방지하고 싶다고 가정해 봅시다. 이를 위해서는 잡 클래스의 `middleware` 메서드에서 `WithoutOverlapping` 미들웨어를 반환하면 됩니다.

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

이렇게 하면 동일한 타입 중복 잡은 큐에 다시 대기시켜(릴리즈) 처리합니다. 다시 시도까지 기다릴 지연 시간(초 단위)이 필요하다면 다음과 같이 지정할 수 있습니다.

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

중복 잡을 바로 삭제해서 재시도되지 않게 하고 싶다면, `dontRelease` 메서드를 사용할 수 있습니다.

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

`WithoutOverlapping` 미들웨어는 라라벨의 원자적 락(atomic lock) 기능으로 동작합니다. 잡이 예기치 않게 실패하거나 타임아웃되는 등 락이 해제되지 않는 일이 생길 수 있으므로, 미들웨어를 붙일 때 `expireAfter` 메서드를 이용해 락 만료 시간을 명시할 수 있습니다. 아래 예시는 잡 실행 시작 3분(180초) 뒤 락이 자동 해제되게 합니다.

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
#### 잡 클래스 간 락 키 공유

기본적으로 `WithoutOverlapping` 미들웨어는 같은 잡 클래스 내에서만 중복을 막습니다. 즉, 두 개의 서로 다른 잡 클래스가 같은 락 키를 사용해도 중복 처리를 방지하지는 않습니다. 여러 잡 클래스 간에도 동일 키로 중복을 막고 싶다면 `shared` 메서드를 호출하면 됩니다.

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

라라벨에는 정해진 횟수 이상 예외가 발생하면, 지정한 시간 동안 잡 실행을 미루는 `Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어가 있습니다. 외부 서비스 등 불안정한 곳과 연동될 때 유용합니다.

예를 들어, 외부 API와 연동하는 잡이 있고 예외가 계속 발생한다면, 미들웨어를 이용해 지정한 횟수 이상 예외가 쌓일 때 일정 시간 대기시켰다가 재시도할 수 있습니다. 이 미들웨어는 보통 [시간 기반 재시도](#time-based-attempts)를 구현하는 잡과 함께 사용합니다.

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

첫 번째 인자는 허용할 최대 예외 발생 횟수, 두 번째 인자는 잡이 제한(쓰로틀)되었을 때 다음 시도까지 대기할(초 단위) 시간입니다. 위 코드에서는 잡이 10번 연속 예외를 던지면 5분 후에 다시 시도되며, 30분 제한 내에만 시도됩니다.

특정 예외 횟수에 도달하지 않은 경우에는 잡을 즉시 재시도하게 됩니다. 이때, `backoff` 메서드를 사용해 곧바로 재시도하지 않고 몇 분(분 단위) 뒤에 재시도하도록 지정할 수 있습니다.

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

이 미들웨어는 내부적으로 캐시 시스템을 이용하며, 잡의 클래스명이 캐시 "키(key)"로 쓰입니다. 여러 잡이 같은 외부 서비스와 상호작용하며 똑같이 제한 받길 원한다면, `by` 메서드 호출로 공유 키를 직접 지정할 수 있습니다.

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

기본적으로는 모든 예외에 대해 제한이 걸리지만, 특정 예외에만 제한을 적용하고 싶다면 `when` 메서드에 클로저를 전달할 수 있습니다. 클로저가 `true`를 반환할 때만 제한합니다.

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

`when`과 달리 예외가 발생했을 때 아예 잡을 삭제하고 싶다면 `deleteWhen` 메서드를 사용할 수 있습니다.

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

잡에서 발생한 예외를 애플리케이션의 예외 핸들러에 리포트하고 싶다면 `report` 메서드를 호출하면 됩니다. 클로저를 전달하면 조건에 맞을 때만 예외를 리포트합니다.

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
> Redis를 사용하는 경우에는, Redis 환경에 최적화된 `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어를 사용하는 것이 더 효율적입니다.

<a name="skipping-jobs"></a>

### 작업 건너뛰기

`Skip` 미들웨어를 사용하면 작업의 로직을 수정하지 않고도 작업을 건너뛰거나 삭제하도록 지정할 수 있습니다. `Skip::when` 메서드는 주어진 조건이 `true`로 평가되면 작업을 삭제하고, `Skip::unless` 메서드는 조건이 `false`로 평가될 때 작업을 삭제합니다.

```php
use Illuminate\Queue\Middleware\Skip;

/**
 * 작업이 통과해야 할 미들웨어를 반환합니다.
 */
public function middleware(): array
{
    return [
        Skip::when($someCondition),
    ];
}
```

보다 복잡한 조건을 평가하고자 한다면, `when` 및 `unless` 메서드에 `Closure`(클로저)를 전달할 수도 있습니다.

```php
use Illuminate\Queue\Middleware\Skip;

/**
 * 작업이 통과해야 할 미들웨어를 반환합니다.
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
## 작업 디스패치하기

작업 클래스를 작성한 후에는, 해당 작업의 `dispatch` 메서드를 사용해서 작업을 디스패치할 수 있습니다. `dispatch` 메서드에 전달된 인수들은 작업의 생성자에 그대로 전달됩니다.

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
     * 새로운 팟캐스트 저장
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

조건에 따라 작업을 디스패치하고 싶을 때는 `dispatchIf` 및 `dispatchUnless` 메서드를 사용할 수 있습니다.

```php
ProcessPodcast::dispatchIf($accountActive, $podcast);

ProcessPodcast::dispatchUnless($accountSuspended, $podcast);
```

새로운 라라벨 애플리케이션에서는 기본 큐 드라이버로 `sync`가 설정되어 있습니다. 이 드라이버는 현재 요청의 포그라운드에서 동기적으로 작업을 실행하며, 로컬 개발 환경에서 자주 사용하기에 편리합니다. 실제로 작업을 백그라운드에서 큐잉하여 처리하고 싶다면, 애플리케이션의 `config/queue.php` 설정 파일에서 다른 큐 드라이버를 지정해야 합니다.

<a name="delayed-dispatching"></a>
### 작업의 디스패치 지연시키기

작업을 바로 큐 워커가 처리할 수 없도록 지연시키고 싶을 때는, 작업을 디스패치할 때 `delay` 메서드를 사용하면 됩니다. 예를 들어, 작업을 디스패치한 후 10분이 지난 후에 처리되도록 하려면 다음과 같이 할 수 있습니다.

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
     * 새로운 팟캐스트 저장
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

경우에 따라, 작업에 기본 지연값이 설정되어 있을 수 있습니다. 이 기본 지연을 무시하고 즉시 작업을 실행하고 싶을 때는 `withoutDelay` 메서드를 사용할 수 있습니다.

```php
ProcessPodcast::dispatch($podcast)->withoutDelay();
```

> [!WARNING]
> Amazon SQS 큐 서비스는 최대 지연 시간이 15분으로 제한되어 있습니다.

<a name="dispatching-after-the-response-is-sent-to-browser"></a>
#### 응답 전송 후 작업 디스패치하기

또는, `dispatchAfterResponse` 메서드를 사용하여 웹 서버가 FastCGI를 사용할 경우 HTTP 응답이 브라우저로 전송된 이후에 작업을 디스패치할 수 있습니다. 이를 통해 큐에 등록된 작업이 실행 중이어도 사용자는 애플리케이션을 바로 이용할 수 있습니다. 이 방법은 이메일 발송처럼 약 1초 내에 끝날 수 있는 작업에 사용하기 적합합니다. 이러한 방식으로 디스패치된 작업은 현재 HTTP 요청 내에서 실행되므로, 별도의 큐 워커가 실행 중이지 않아도 처리가 가능합니다.

```php
use App\Jobs\SendNotification;

SendNotification::dispatchAfterResponse();
```

클로저(익명 함수)를 `dispatch`한 후, `afterResponse` 메서드를 체이닝해 HTTP 응답 전송 이후에 실행될 수 있습니다.

```php
use App\Mail\WelcomeMessage;
use Illuminate\Support\Facades\Mail;

dispatch(function () {
    Mail::to('taylor@example.com')->send(new WelcomeMessage);
})->afterResponse();
```

<a name="synchronous-dispatching"></a>
### 동기식 디스패치

작업을 즉시(동기적으로) 실행하고 싶을 때는 `dispatchSync` 메서드를 사용할 수 있습니다. 이 방법을 사용하면 작업이 큐에 들어가지 않고, 현재 프로세스에서 곧바로 실행됩니다.

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
     * 새로운 팟캐스트 저장
     */
    public function store(Request $request): RedirectResponse
    {
        $podcast = Podcast::create(/* ... */);

        // 팟캐스트 생성 등...

        ProcessPodcast::dispatchSync($podcast);

        return redirect('/podcasts');
    }
}
```

<a name="jobs-and-database-transactions"></a>
### 작업과 데이터베이스 트랜잭션

데이터베이스 트랜잭션 내부에서 작업을 디스패치해도 문제는 없지만, 작업이 실제로 올바르게 실행될 수 있도록 특별히 주의해야 합니다. 트랜잭션 내에서 작업을 디스패치할 경우, 부모 트랜잭션이 커밋되기 전에 큐 워커가 작업을 처리할 수도 있습니다. 이때, 트랜잭션 내에서 모델이나 데이터베이스 레코드를 수정했다면, 그 변경 내용이 아직 데이터베이스에 반영되지 않았을 수 있습니다. 또한, 트랜잭션 내에서 생성한 모델이나 레코드가 데이터베이스에 존재하지 않을 수도 있습니다.

다행히, 라라벨에서는 이런 문제를 우회하는 여러 방법을 제공합니다. 첫 번째로, 큐 연결 설정 배열에 `after_commit` 옵션을 설정할 수 있습니다.

```php
'redis' => [
    'driver' => 'redis',
    // ...
    'after_commit' => true,
],
```

`after_commit` 옵션이 `true`일 경우, 트랜잭션 내에서 작업을 디스패치하더라도 라라벨은 부모 데이터베이스 트랜잭션이 모두 커밋될 때까지 실제로 작업을 디스패치하지 않습니다. 트랜잭션이 열려 있지 않으면 작업이 즉시 디스패치됩니다.

만약 트랜잭션 도중 예외로 인해 롤백된다면, 해당 트랜잭션 동안 디스패치된 모든 작업은 버려집니다.

> [!NOTE]
> `after_commit` 옵션을 `true`로 설정하면, 큐에 등록된 이벤트 리스너, 메일러블, 알림, 브로드캐스트 이벤트도 모든 데이터베이스 트랜잭션이 커밋된 이후에 디스패치됩니다.

<a name="specifying-commit-dispatch-behavior-inline"></a>
#### 커밋 후 디스패치 동작을 인라인으로 지정

큐 연결 설정에서 `after_commit` 옵션을 `true`로 지정하지 않더라도, 특정 작업만 커밋 후에 디스패치되도록 할 수 있습니다. 이 경우, 디스패치 연산에 `afterCommit` 메서드를 체이닝하면 됩니다.

```php
use App\Jobs\ProcessPodcast;

ProcessPodcast::dispatch($podcast)->afterCommit();
```

반대로, `after_commit` 옵션이 `true`로 설정되어 있는 상태에서 해당 작업만 커밋을 기다리지 않고 즉시 실행하고 싶을 때는 `beforeCommit` 메서드를 체이닝하면 됩니다.

```php
ProcessPodcast::dispatch($podcast)->beforeCommit();
```

<a name="job-chaining"></a>
### 작업 체이닝

작업 체이닝을 사용하면, 주 작업이 성공적으로 실행된 후 순차적으로 실행되어야 할 큐 작업 목록을 지정할 수 있습니다. 체인 내의 한 작업이 실패하면, 남은 작업들은 실행되지 않습니다. 체인 작업을 실행하려면 `Bus` 파사드가 제공하는 `chain` 메서드를 사용할 수 있습니다. (역자주: 라라벨의 커맨드 버스(command bus)는 큐 작업 디스패칭의 기반이 되는 하위 컴포넌트입니다.)

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

작업 클래스 인스턴스뿐만 아니라, 클로저도 체인에 추가할 수 있습니다.

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
> 작업 내에서 `$this->delete()` 메서드로 작업을 삭제해도 체인 작업의 실행은 멈추지 않습니다. 체인 작업 중 하나가 실패해야만 체인의 나머지 작업이 중단됩니다.

<a name="chain-connection-queue"></a>
#### 체인 연결 및 큐 지정

체인 작업에 사용할 연결(connection)과 큐(queue)를 지정하고 싶을 때는 `onConnection` 및 `onQueue` 메서드를 사용하면 됩니다. 이 메서드들은 각 작업이 별도로 연결/큐를 지정하지 않은 경우에 적용됩니다.

```php
Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->onConnection('redis')->onQueue('podcasts')->dispatch();
```

<a name="adding-jobs-to-the-chain"></a>
#### 체인에 작업 추가하기

가끔 기존 체인 내 다른 작업에서 현재 체인의 앞이나 뒤에 작업을 추가할 필요가 있을 수 있습니다. 이럴 때는 `prependToChain` 및 `appendToChain` 메서드를 사용할 수 있습니다.

```php
/**
 * 작업 실행
 */
public function handle(): void
{
    // ...

    // 현재 체인 앞에 추가. 현재 작업 바로 다음에 실행됨...
    $this->prependToChain(new TranscribePodcast);

    // 현재 체인 마지막에 추가. 체인 마지막에 실행됨...
    $this->appendToChain(new TranscribePodcast);
}
```

<a name="chain-failures"></a>
#### 체인 실패 처리

체인 작업 실행 시, `catch` 메서드를 사용해 체인 내 작업이 실패했을 때 호출될 클로저를 지정할 수 있습니다. 전달된 콜백에는 작업 실패를 유발한 `Throwable` 인스턴스가 전달됩니다.

```php
use Illuminate\Support\Facades\Bus;
use Throwable;

Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->catch(function (Throwable $e) {
    // 체인 내 작업이 실패했을 때 실행...
})->dispatch();
```

> [!WARNING]
> 체인 콜백은 직렬화되어 훗날 라라벨 큐에서 실행되므로, 체인 콜백 내에서 `$this` 변수를 사용해서는 안 됩니다.

<a name="customizing-the-queue-and-connection"></a>
### 큐와 연결 커스터마이징

<a name="dispatching-to-a-particular-queue"></a>
#### 특정 큐에 디스패치하기

작업을 다양한 큐에 밀어 넣으면 작업을 "분류"할 수 있을 뿐만 아니라, 각 큐에 할당하는 워커 수를 조정하여 작업 우선순위를 적용할 수 있습니다. 이 방법은 큐 설정 파일에 정의된 큐 "연결(connection)"을 다르게 하는 것이 아니라, 하나의 연결 안에서 서로 다른 큐를 지정하는 것입니다. 특정 큐를 지정하려면 작업 디스패치 시 `onQueue` 메서드를 사용하면 됩니다.

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
     * 새로운 팟캐스트 저장
     */
    public function store(Request $request): RedirectResponse
    {
        $podcast = Podcast::create(/* ... */);

        // 팟캐스트 생성 등...

        ProcessPodcast::dispatch($podcast)->onQueue('processing');

        return redirect('/podcasts');
    }
}
```

다른 방법으로, 작업 생성자 내에서 `onQueue` 메서드를 호출해 작업의 큐를 지정할 수 있습니다.

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    /**
     * 새 작업 인스턴스 생성
     */
    public function __construct()
    {
        $this->onQueue('processing');
    }
}
```

<a name="dispatching-to-a-particular-connection"></a>
#### 특정 연결에 디스패치하기

애플리케이션이 여러 큐 연결(connection)과 상호작용해야 할 경우, `onConnection` 메서드를 사용해서 어떤 연결에 작업을 넣을지 지정할 수 있습니다.

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
     * 새로운 팟캐스트 저장
     */
    public function store(Request $request): RedirectResponse
    {
        $podcast = Podcast::create(/* ... */);

        // 팟캐스트 생성 등...

        ProcessPodcast::dispatch($podcast)->onConnection('sqs');

        return redirect('/podcasts');
    }
}
```

`onConnection`과 `onQueue` 메서드를 함께 체이닝하여 작업의 연결과 큐 둘 다 지정할 수도 있습니다.

```php
ProcessPodcast::dispatch($podcast)
    ->onConnection('sqs')
    ->onQueue('processing');
```

또는, 작업 생성자 내에서 `onConnection` 메서드를 호출해 연결을 지정할 수도 있습니다.

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    /**
     * 새 작업 인스턴스 생성
     */
    public function __construct()
    {
        $this->onConnection('sqs');
    }
}
```

<a name="max-job-attempts-and-timeout"></a>
### 최대 시도 횟수 / 타임아웃 값 지정

<a name="max-attempts"></a>
#### 최대 시도 횟수

큐에 등록된 작업 중 하나가 오류를 일으킨다면, 무한히 재시도되는 것을 원하지 않을 수 있습니다. 라라벨은 작업을 몇 번 또는 얼마 동안 재시도할지 지정할 다양한 방법을 제공합니다.

가장 기본적인 방법은 Artisan 커맨드라인에서 `--tries` 옵션을 사용하는 것입니다. 이 옵션은 워커가 처리하는 모든 작업에 적용되며, 해당 작업이 별도로 시도 횟수를 지정하지 않은 경우에만 적용됩니다.

```shell
php artisan queue:work --tries=3
```

작업이 지정된 최대 시도 횟수를 초과하면 "실패"로 간주됩니다. 실패한 작업 처리 방법에 대해서는 [실패한 작업 문서](#dealing-with-failed-jobs)를 참고하세요. 만약 `queue:work` 명령에 `--tries=0`을 지정하면, 작업은 무한히 재시도됩니다.

더 세밀하게 작업마다 최대 시도 횟수를 지정하고 싶을 때는, 작업 클래스에 시도 횟수를 지정할 수 있습니다. 작업에 명시적인 시도 횟수가 있다면, 명령줄에서 지정한 `--tries` 값보다 작업 클래스의 값이 우선 적용됩니다.

```php
<?php

namespace App\Jobs;

class ProcessPodcast implements ShouldQueue
{
    /**
     * 작업의 최대 시도 횟수
     *
     * @var int
     */
    public $tries = 5;
}
```

특정 작업의 최대 시도 횟수를 동적으로 제어해야 한다면, 작업 클래스에 `tries` 메서드를 정의할 수 있습니다.

```php
/**
 * 작업의 최대 시도 횟수를 반환
 */
public function tries(): int
{
    return 5;
}
```

<a name="time-based-attempts"></a>
#### 시간 기반 재시도 제한

작업이 실패하기 전 몇 번 시도할지 대신, 얼마의 시간까지 시도할지를 정의할 수도 있습니다. 이 방법은 정해진 시간 동안은 몇 번이든 재시도할 수 있게 해줍니다. 특정 시간 이후에는 더 이상 시도하지 않도록 하려면, 작업 클래스에 `retryUntil` 메서드를 추가하면 됩니다. 이 메서드는 `DateTime` 인스턴스를 반환해야 합니다.

```php
use DateTime;

/**
 * 작업의 타임아웃 시점을 반환
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(10);
}
```

`retryUntil`과 `tries`가 모두 정의되어 있다면, 라라벨은 `retryUntil` 메서드의 결과를 우선 적용합니다.

> [!NOTE]
> [큐잉되는 이벤트 리스너](/docs/12.x/events#queued-event-listeners)와 [큐잉되는 알림](/docs/12.x/notifications#queueing-notifications)에도 `tries` 속성이나 `retryUntil` 메서드를 정의할 수 있습니다.

<a name="max-exceptions"></a>
#### 최대 예외 발생 횟수

특정 작업을 여러 번 시도할 수 있지만, 재시도가 직접 `release` 메서드로 인한 것이 아니라 미처리 예외로 인해 발생했을 때 일정 횟수까지 허용하고 초과 시 작업을 실패 처리하고 싶을 수 있습니다. 이럴 때는 작업 클래스에 `maxExceptions` 속성을 지정할 수 있습니다.

```php
<?php

namespace App\Jobs;

use Illuminate\Support\Facades\Redis;

class ProcessPodcast implements ShouldQueue
{
    /**
     * 작업의 최대 시도 횟수
     *
     * @var int
     */
    public $tries = 25;

    /**
     * 실패로 처리되기 전 허용할 미처리 예외의 최대 수
     *
     * @var int
     */
    public $maxExceptions = 3;

    /**
     * 작업 실행
     */
    public function handle(): void
    {
        Redis::throttle('key')->allow(10)->every(60)->then(function () {
            // 락을 획득하면, 팟캐스트를 처리...
        }, function () {
            // 락을 획득할 수 없으면...
            return $this->release(10);
        });
    }
}
```

위 예시에서, 만약 애플리케이션이 Redis 락을 획득하지 못하면 작업은 10초 후 다시 시도하고, 최대 25회까지 재시도합니다. 하지만 작업에서 미처리 예외가 3번 발생하면 바로 실패 처리됩니다.

<a name="timeout"></a>
#### 타임아웃

대부분의 경우, 큐 작업이 어느 정도 시간 내에 끝나야 할지 예상 가능합니다. 그래서 라라벨에서는 "타임아웃" 값을 지정할 수 있습니다. 기본값은 60초이며, 작업이 설정한 타임아웃을 초과하면 해당 작업을 처리하던 워커가 에러와 함께 종료됩니다. 일반적으로, 워커는 [서버에 구성된 프로세스 매니저](#supervisor-configuration)에 의해 자동으로 재시작됩니다.

작업의 최대 실행 시간을 지정하려면, Artisan 명령줄에서 `--timeout` 옵션을 사용할 수 있습니다.

```shell
php artisan queue:work --timeout=30
```

작업이 타임아웃으로 인해 계속 실패하고 최대 시도 횟수도 초과하면, 해당 작업은 실패 상태로 표시됩니다.

작업 클래스 내에서 최대 실행 시간을 직접 지정할 수도 있습니다. 이 값은 명령줄에서 지정한 값을 덮어씁니다.

```php
<?php

namespace App\Jobs;

class ProcessPodcast implements ShouldQueue
{
    /**
     * 타임아웃 전 작업이 실행될 수 있는 최대 초
     *
     * @var int
     */
    public $timeout = 120;
}
```

소켓이나 외부 HTTP 연결과 같이 IO 블로킹이 발생할 수 있는 상황에서는 지정한 타임아웃으로 제어되지 않을 수 있으니, 해당 API에서도 타임아웃 값을 직접 지정해야 합니다. 예를 들어, Guzzle을 사용할 때는 반드시 연결 타임아웃 및 요청 타임아웃을 적용해야 합니다.

> [!WARNING]
> 작업 타임아웃을 지정하려면 [PCNTL](https://www.php.net/manual/en/book.pcntl.php) PHP 익스텐션이 설치되어 있어야 합니다. 또한, 작업의 "타임아웃" 값은 ["retry after"](#job-expiration) 값보다 항상 작아야 합니다. 그렇지 않으면, 작업이 실제로 완료되거나 타임아웃되기 전에 다시 시도될 수 있습니다.

<a name="failing-on-timeout"></a>
#### 타임아웃 시 작업을 실패 처리하기

작업이 [실패](#dealing-with-failed-jobs) 상태로 표시되기를 원할 때는, 작업 클래스에 `$failOnTimeout` 속성을 정의하면 됩니다.

```php
/**
 * 타임아웃 시 작업을 실패 처리할지 여부 지정
 *
 * @var bool
 */
public $failOnTimeout = true;
```

<a name="error-handling"></a>
### 에러 처리

작업 처리 중 예외가 발생하면, 해당 작업은 자동으로 큐에 다시 올라가 재시도됩니다. 이 과정은 최대 시도 횟수에 도달할 때까지 반복됩니다. 최대 시도 횟수는 `queue:work` Artisan 명령의 `--tries` 값 또는 작업 클래스에서 개별적으로 설정할 수 있습니다. 큐 워커 실행에 대한 자세한 내용은 [아래에서 더 확인](#running-the-queue-worker)할 수 있습니다.

<a name="manually-releasing-a-job"></a>
#### 작업을 직접 다시 큐에 올리기

특정 작업을 직접 다시 큐에 올려 나중에 다시 실행하고 싶을 때가 있습니다. 이럴 때는 `release` 메서드를 호출하면 됩니다.

```php
/**
 * 작업 실행
 */
public function handle(): void
{
    // ...

    $this->release();
}
```

기본적으로, `release` 메서드는 작업을 즉시 처리 가능한 상태로 큐에 올립니다. 하지만, 특정 초 단위로 지연을 주거나 날짜 인스턴스를 전달할 수도 있습니다.

```php
$this->release(10);

$this->release(now()->addSeconds(10));
```

<a name="manually-failing-a-job"></a>
#### 작업을 직접 실패 처리하기

특정 상황에서 작업을 직접 "실패"로 표시해야 할 수도 있습니다. 이 경우 `fail` 메서드를 호출하면 됩니다.

```php
/**
 * 작업 실행
 */
public function handle(): void
{
    // ...

    $this->fail();
}
```

예외를 직접 포착해서 작업을 실패 처리하고 싶으면, 해당 예외를 `fail` 메서드에 전달하면 됩니다. 또는, 간단히 에러 메시지 문자열을 전달해도 예외로 변환되어 처리됩니다.

```php
$this->fail($exception);

$this->fail('Something went wrong.');
```

> [!NOTE]
> 실패한 작업에 대한 더 자세한 내용은 [작업 실패 처리 문서](#dealing-with-failed-jobs)를 참고하세요.

<a name="fail-jobs-on-exceptions"></a>
#### 특정 예외에서 작업을 실패 처리하기

`FailOnException` [작업 미들웨어](#job-middleware)를 사용하면, 특정 예외가 발생했을 때 추가적인 재시도를 중단하고 즉시 작업을 실패로 처리할 수 있습니다. 이를 통해 외부 API 오류 등 일시적인(Transient) 예외는 재시도를 허용하고, 예를 들어 사용자의 권한이 박탈되는 등 영구적(Exception: Persistent)인 예외에서는 즉시 실패로 처리할 수 있습니다.

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
     * 새 작업 인스턴스 생성
     */
    public function __construct(
        public User $user,
    ) {}

    /**
     * 작업 실행
     */
    public function handle(): void
    {
        $user->authorize('sync-chat-history');

        $response = Http::throw()->get(
            "https://chat.laravel.test/?user={$user->uuid}"
        );

        // ...
    }

    /**
     * 작업이 통과해야 할 미들웨어 반환
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

## 잡 배치 처리 (Job Batching)

라라벨의 잡 배치 기능은 여러 개의 잡(job)을 한 번에 실행하고, 이 배치 내 잡들이 모두 완료된 후 특정 작업을 손쉽게 수행할 수 있게 해줍니다. 먼저, 잡 배치의 진행률 등 메타데이터를 저장할 수 있는 테이블을 위한 데이터베이스 마이그레이션을 생성해야 합니다. 이 마이그레이션은 `make:queue-batches-table` 아티즌 명령어로 생성할 수 있습니다.

```shell
php artisan make:queue-batches-table

php artisan migrate
```

<a name="defining-batchable-jobs"></a>
### 배치 처리 가능한 잡 정의하기

배치 처리 가능한 잡을 정의하려면 [일반적인 큐잉 가능한 잡 생성 방법](#creating-jobs)에 따라 잡 클래스를 만든 후, 여기에 `Illuminate\Bus\Batchable` 트레이트를 추가하면 됩니다. 이 트레이트는 현재 잡이 속한 배치 객체를 반환하는 `batch` 메서드를 제공합니다.

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
     * Execute the job.
     */
    public function handle(): void
    {
        if ($this->batch()->cancelled()) {
            // 배치가 취소되었는지 확인합니다...

            return;
        }

        // CSV 파일의 일부를 임포트합니다...
    }
}
```

<a name="dispatching-batches"></a>
### 배치 디스패치(실행)하기

잡의 배치를 디스패치하려면 `Bus` 파사드의 `batch` 메서드를 사용합니다. 보통 배치의 실용성은 완료 콜백과 함께 사용될 때 극대화됩니다. `then`, `catch`, `finally`와 같은 메서드를 이용해 배치가 완료되거나 실패/종료 시 실행할 콜백을 정의할 수 있습니다. 각각의 콜백은 호출 시 `Illuminate\Bus\Batch` 인스턴스를 전달받습니다. 아래 예시에서는 여러 개의 CSV 행을 처리하는 배치 잡들을 큐에 넣는 상황을 가정합니다.

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
    // 배치가 생성되었지만 아직 잡이 추가되지 않았습니다...
})->progress(function (Batch $batch) {
    // 개별 잡이 성공적으로 완료되었습니다...
})->then(function (Batch $batch) {
    // 모든 잡이 성공적으로 완료되었습니다...
})->catch(function (Batch $batch, Throwable $e) {
    // 첫 번째 잡이 실패했을 때 실행됩니다...
})->finally(function (Batch $batch) {
    // 배치 실행이 모두 끝났을 때 실행됩니다...
})->dispatch();

return $batch->id;
```

배치의 ID(즉, `$batch->id` 프로퍼티로 접근 가능)는, 배치가 디스패치된 후 [라라벨 커맨드 버스](#inspecting-batches)에서 해당 배치 정보를 조회하는 데 사용할 수 있습니다.

> [!WARNING]
> 배치 콜백은 직렬화되어 나중에 큐에서 실행되므로, 콜백 내부에서는 `$this` 변수를 사용하면 안 됩니다. 또한, 배치된 잡들은 데이터베이스 트랜잭션 안에서 실행되므로, 암묵적으로 커밋되는 데이터베이스 구문을 잡 내부에서 실행해서는 안 됩니다.

<a name="naming-batches"></a>
#### 배치 이름 지정하기

Laravel Horizon, Laravel Telescope등 일부 도구는 배치에 이름을 지정할 경우 더 읽기 쉬운 디버깅 정보를 제공합니다. 배치에 임의의 이름을 부여하려면 배치 정의 시 `name` 메서드를 호출하면 됩니다.

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // 모든 잡이 성공적으로 완료되었습니다...
})->name('Import CSV')->dispatch();
```

<a name="batch-connection-queue"></a>
#### 배치의 커넥션 및 큐 지정

배치 잡이 사용할 커넥션과 큐를 지정하려면 `onConnection` 및 `onQueue` 메서드를 사용하면 됩니다. 모든 배치 잡은 동일한 커넥션과 큐에서 실행되어야 합니다.

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // 모든 잡이 성공적으로 완료되었습니다...
})->onConnection('redis')->onQueue('imports')->dispatch();
```

<a name="chains-and-batches"></a>
### 체인과 배치

배치 내에 [체인된 잡](#job-chaining) 집합을 정의할 수 있습니다. 체인된 잡들을 배열로 묶어서 배치에 포함시키면 됩니다. 예를 들어 아래처럼 두 개의 잡 체인을 동시에 실행하고, 두 체인이 모두 끝났을 때 콜백을 수행할 수 있습니다.

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

반대로, [체인](#job-chaining) 안에 여러 개의 배치를 정의하는 방식도 가능합니다. 예를 들어, 여러 팟캐스트를 배포하는 배치를 먼저 실행한 뒤, 알림을 보내는 배치 잡을 실행할 수도 있습니다.

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
### 배치에 잡 추가하기

때로는 배치 잡 실행 중에 추가적으로 잡을 더 넣어야 할 때가 있습니다. 예를 들어, 수천 개의 잡을 한 번에 배치로 디스패치하기 어려울 경우 "로더" 잡을 먼저 배치해 놓고, 이 잡이 실행 중 추가 잡을 배치로 하이드레이트(추가)하도록 하면 효율적입니다.

```php
$batch = Bus::batch([
    new LoadImportBatch,
    new LoadImportBatch,
    new LoadImportBatch,
])->then(function (Batch $batch) {
    // 모든 잡이 성공적으로 완료되었습니다...
})->name('Import Contacts')->dispatch();
```

이 예시에서는 `LoadImportBatch` 잡을 이용해 배치에 잡을 추가합니다. 이를 위해서는 job 내에서 `batch` 메서드로 가져온 배치 인스턴스의 `add` 메서드를 사용할 수 있습니다.

```php
use App\Jobs\ImportContacts;
use Illuminate\Support\Collection;

/**
 * Execute the job.
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
> 동일한 배치에 속한 잡에서만 새로운 잡을 그 배치에 추가할 수 있습니다.

<a name="inspecting-batches"></a>
### 배치 정보 조회하기

배치 완료 콜백에 전달되는 `Illuminate\Bus\Batch` 인스턴스는, 해당 배치 잡과 상호 작용하거나 상태를 조회할 수 있게 여러 속성과 메서드를 제공합니다.

```php
// 배치의 UUID...
$batch->id;

// 배치의 이름(있을 경우)...
$batch->name;

// 배치에 할당된 잡 개수...
$batch->totalJobs;

// 아직 큐에서 처리되지 않은 잡 개수...
$batch->pendingJobs;

// 실패한 잡 개수...
$batch->failedJobs;

// 지금까지 처리한 잡 수...
$batch->processedJobs();

// 배치 완료율(0~100)...
$batch->progress();

// 배치 실행이 끝났는지 확인...
$batch->finished();

// 배치 실행 중지...
$batch->cancel();

// 배치가 취소되었는지 확인...
$batch->cancelled();
```

<a name="returning-batches-from-routes"></a>
#### 라우트에서 배치 반환하기

모든 `Illuminate\Bus\Batch` 인스턴스는 JSON 직렬화가 가능하므로, 애플리케이션의 라우트에서 바로 반환해 배치의 완료 진행률 등 정보를 포함한 JSON 페이로드를 받을 수 있습니다. 이를 통해 애플리케이션 UI에서 배치 진행 상황을 쉽게 표시할 수 있습니다.

ID로 배치를 조회하려면, `Bus` 파사드의 `findBatch` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Support\Facades\Bus;
use Illuminate\Support\Facades\Route;

Route::get('/batch/{batchId}', function (string $batchId) {
    return Bus::findBatch($batchId);
});
```

<a name="cancelling-batches"></a>
### 배치 취소하기

특정 배치의 실행을 중단해야 할 때가 있습니다. 이럴 때는 `Illuminate\Bus\Batch` 인스턴스의 `cancel` 메서드를 호출하시면 됩니다.

```php
/**
 * Execute the job.
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

앞선 예시에서처럼, 보통 배치에 속한 잡은 실행 도중 자신의 배치가 취소되었는지 먼저 확인해야 합니다. 그러나 보다 편하게 처리하려면 [미들웨어](#job-middleware)인 `SkipIfBatchCancelled`를 해당 잡에 적용하면 됩니다. 이 미들웨어를 사용하면, 배치가 취소된 경우 잡이 자동으로 처리되지 않습니다.

```php
use Illuminate\Queue\Middleware\SkipIfBatchCancelled;

/**
 * Get the middleware the job should pass through.
 */
public function middleware(): array
{
    return [new SkipIfBatchCancelled];
}
```

<a name="batch-failures"></a>
### 배치 실패 처리

배치에 속한 잡 중 하나가 실패할 경우, `catch` 콜백(지정된 경우)이 실행됩니다. 이 콜백은 배치 내 실패한 첫 번째 잡에서만 한 번 호출됩니다.

<a name="allowing-failures"></a>
#### 실패 허용 설정

배치 내에서 잡이 실패하면 라라벨은 자동으로 해당 배치를 "취소됨"으로 표시합니다. 만약 잡 실패가 곧바로 배치의 취소로 이어지지 않도록 하고 싶다면, 배치 실행 시 `allowFailures` 메서드를 사용하여 이를 비활성화할 수 있습니다.

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // 모든 잡이 성공적으로 완료되었습니다...
})->allowFailures()->dispatch();
```

<a name="retrying-failed-batch-jobs"></a>
#### 실패한 배치 잡 재시도

라라벨은 특정 배치 내 실패한 모든 잡을 쉽게 재시도할 수 있도록 `queue:retry-batch` 아티즌 명령어를 제공합니다. 이 `queue:retry-batch` 명령어는 재시도할 배치의 UUID를 인자로 받습니다.

```shell
php artisan queue:retry-batch 32dbc76c-4f82-4749-b610-a639fe0099b5
```

<a name="pruning-batches"></a>
### 배치 데이터 정리(Pruning)

별도의 정리 작업을 수행하지 않으면, `job_batches` 테이블에 기록이 빠르게 누적될 수 있습니다. 이를 방지하려면 `queue:prune-batches` 아티즌 명령어를 [스케줄링](/docs/12.x/scheduling)하여 하루에 한 번씩 정리할 것을 권장합니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches')->daily();
```

기본값으로, 완료된 지 24시간이 지난 모든 배치는 정리(삭제)됩니다. 보유 기간을 조정하려면 명령어에 `hours` 옵션을 추가해 사용할 수 있습니다. 아래 예시는 48시간이 지난 배치를 삭제합니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48')->daily();
```

경우에 따라, `jobs_batches` 테이블에는 성공적으로 완료되지 않은 배치의 기록도 누적될 수 있습니다. 예를 들어, 잡이 실패한 후 재시도되지 않았던 경우 등입니다. 이런 미완료 배치도 `unfinished` 옵션을 통해 함께 정리할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48 --unfinished=72')->daily();
```

마찬가지로, 취소된 배치 기록이 누적될 수도 있는데, 이 경우 `cancelled` 옵션을 사용해 정리할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48 --cancelled=72')->daily();
```

<a name="storing-batches-in-dynamodb"></a>
### DynamoDB에 배치 정보 저장

라라벨은 [DynamoDB](https://aws.amazon.com/dynamodb)에 배치 메타 정보를 저장하는 것도 지원합니다. 단, 이 경우 배치 기록들을 저장할 DynamoDB 테이블을 직접 생성해야 합니다.

일반적으로 테이블 이름은 `job_batches`로 지정하지만, 애플리케이션의 `queue` 설정 파일 내 `queue.batching.table` 값에 따라 이름을 달리 설정할 수도 있습니다.

<a name="dynamodb-batch-table-configuration"></a>
#### DynamoDB 배치 테이블 설정

`job_batches` 테이블에는 string 타입의 파티션 키 `application`과 string 타입의 정렬 키 `id`가 필요합니다. 여기서 `application` 키 값에는 애플리케이션의 `app` 설정 파일 내 `name` 설정값이 저장됩니다. 즉, 이 테이블 하나로 여러 라라벨 애플리케이션의 잡 배치를 함께 관리할 수 있습니다.

추가적으로, [자동 배치 데이터 정리](#pruning-batches-in-dynamodb)를 사용하려면 테이블에 `ttl` 속성을 정의할 수 있습니다.

<a name="dynamodb-configuration"></a>
#### DynamoDB 설정

다음으로 라라벨 애플리케이션이 Amazon DynamoDB와 통신할 수 있도록 AWS SDK 패키지를 설치해야 합니다.

```shell
composer require aws/aws-sdk-php
```

그 다음, `queue.batching.driver` 설정 항목을 `dynamodb`로 변경합니다. 또한, `batching` 설정 배열 내에 `key`, `secret`, `region` 항목을 추가해야 하며, 이 값들은 AWS 인증에 사용됩니다. `dynamodb` 드라이버 사용 시에는 `queue.batching.database` 설정값은 필요하지 않습니다.

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
#### DynamoDB에서 배치 데이터 정리

[ DynamoDB ](https://aws.amazon.com/dynamodb)에 잡 배치 정보를 저장하는 경우, 기존 관계형 데이터베이스용 배치 정리 명령어는 동작하지 않습니다. 대신 [DynamoDB의 고유 TTL 기능](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html)을 활용해 오래된 배치 기록을 자동 삭제할 수 있습니다.

테이블에 `ttl` 속성을 정의했다면, 라라벨에 배치 레코드 정리 시 사용할 설정 파라미터를 추가할 수도 있습니다. `queue.batching.ttl_attribute` 설정은 TTL 정보를 저장하는 속성명을, `queue.batching.ttl` 설정은 레코드가 최종 갱신된 뒤 삭제되기까지의(초 단위) 시간을 지정합니다.

```php
'batching' => [
    'driver' => env('QUEUE_FAILED_DRIVER', 'dynamodb'),
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'table' => 'job_batches',
    'ttl_attribute' => 'ttl',
    'ttl' => 60 * 60 * 24 * 7, // 7일
],
```

<a name="queueing-closures"></a>
## 클로저(Closure) 큐 작업 처리

잡 클래스를 큐에 디스패치하는 대신, 클로저를 큐에 바로 디스패치할 수도 있습니다. 이는 단순하고 빠르게 별도의 요청 사이클 밖에서 실행해야 하는 작업에 적합합니다. 클로저를 큐에 디스패치하면, 클로저의 코드 내용은 암호화 서명되어 전송 도중 변경될 수 없습니다.

```php
$podcast = App\Podcast::find(1);

dispatch(function () use ($podcast) {
    $podcast->publish();
});
```

클로저 작업에 이름을 부여해서 큐 대시보드나 `queue:work` 명령어에서 확인하고자 할 때는 `name` 메서드를 사용할 수 있습니다.

```php
dispatch(function () {
    // ...
})->name('Publish Podcast');
```

또한, `catch` 메서드를 이용하여, 큐 작업 재시도 횟수까지 소진해도 클로저가 정상적으로 완료되지 않을 경우 실행할 클로저를 지정할 수 있습니다. (재시도 횟수 설정은 [여기서](#max-job-attempts-and-timeout) 확인하세요.)

```php
use Throwable;

dispatch(function () use ($podcast) {
    $podcast->publish();
})->catch(function (Throwable $e) {
    // 이 잡이 실패하였습니다...
});
```

> [!WARNING]
> `catch` 콜백 또한 직렬화되어 나중에 큐에서 실행되므로, 콜백 내에서는 `$this` 변수를 사용하시면 안 됩니다.

<a name="running-the-queue-worker"></a>
## 큐 워커 실행하기

<a name="the-queue-work-command"></a>
### `queue:work` 명령어

라라벨은 큐에 새 잡이 추가되면 이를 처리하는 워커를 실행할 수 있는 아티즌 명령어를 제공합니다. `queue:work` 명령어로 워커를 실행할 수 있습니다. 한 번 워커가 시작되면, 사용자가 강제로 정지시키거나 터미널을 닫기 전까지 계속 실행됩니다.

```shell
php artisan queue:work
```

> [!NOTE]
> `queue:work` 프로세스를 백그라운드에서 항상 실행되게 하려면 [Supervisor](#supervisor-configuration)와 같은 프로세스 관리자를 사용하여 워커가 중단 없이 계속 실행될 수 있도록 해야 합니다.

처리한 잡의 ID, 커넥션 명, 큐 이름 등을 커맨드 출력에 함께 표시하려면 `-v` 플래그를 붙여서 명령어를 실행하면 됩니다.

```shell
php artisan queue:work -v
```

참고로, 큐 워커는 앱의 실행 상태를 메모리에 저장하는 장기 실행 프로세스입니다. 즉, 워커 실행 후 코드에 변경사항이 있어도 감지할 수 없습니다. 따라서 코드 배포 시 [큐 워커 재시작](#queue-workers-and-deployment)을 반드시 해주셔야 하며, 잡 간에 생성된 정적 상태 등도 자동으로 초기화되지 않는다는 점을 유념하세요.

대신 `queue:listen` 명령어를 사용할 수도 있습니다. 이 명령어는 코드가 갱신되거나 앱 상태를 리로드해야 할 때 워커를 수동으로 재시작할 필요가 없습니다. 단, 이 명령어는 `queue:work` 명령어 대비 현저히 비효율적입니다.

```shell
php artisan queue:listen
```

<a name="running-multiple-queue-workers"></a>
#### 여러 큐 워커 동시 실행

하나의 큐에 여러 워커를 할당해 동시에 잡을 처리하려면 `queue:work` 프로세스를 여러 개 실행하면 됩니다. 로컬 환경에서는 터미널 탭을 여러 개 열어 실행해도 되고, 운영 서버에서는 프로세스 관리자의 설정을 이용하면 됩니다. [Supervisor 사용 시](#supervisor-configuration) `numprocs` 설정을 참조하세요.

<a name="specifying-the-connection-queue"></a>
#### 커넥션 및 큐 지정

워커가 사용할 큐 커넥션을 명시하고자 할 경우, `work` 명령어의 인수로 지정하면 됩니다. 인수로 전달하는 커넥션 이름은 `config/queue.php`의 커넥션 중 하나여야 합니다.

```shell
php artisan queue:work redis
```

기본적으로 `queue:work` 명령어는 해당 커넥션의 기본 큐 잡만 처리합니다. 그러나 `--queue` 옵션을 이용해 특정 큐의 잡만 처리하도록 워커를 설정할 수도 있습니다. 예를 들어, 모든 이메일 잡이 `redis` 커넥션의 `emails` 큐에 쌓여 있다면 아래와 같이 실행해 해당 큐만 처리하도록 할 수 있습니다.

```shell
php artisan queue:work redis --queue=emails
```

<a name="processing-a-specified-number-of-jobs"></a>
#### 지정한 개수만큼의 잡 처리

`--once` 옵션을 사용하면 워커가 큐에서 잡 한 개만 처리하고 종료하도록 할 수 있습니다.

```shell
php artisan queue:work --once
```

`--max-jobs` 옵션은 워커가 지정한 잡 개수만큼 처리한 후 종료하도록 만듭니다. 이 옵션은 [Supervisor](#supervisor-configuration)와 함께 사용할 때 유용하며, 일정 개수 이상 잡을 처리한 후 워커를 자동 재시작해 누적된 메모리를 해제할 수 있습니다.

```shell
php artisan queue:work --max-jobs=1000
```

<a name="processing-all-queued-jobs-then-exiting"></a>
#### 대기 중인 모든 잡 처리 후 종료

`--stop-when-empty` 옵션을 사용하면, 워커가 모든 잡을 처리한 뒤 graceful하게 종료합니다. Docker 컨테이너에서 라라벨 큐를 사용할 때, 큐가 모두 비워지면 컨테이너를 종료하고자 할 때 유용합니다.

```shell
php artisan queue:work --stop-when-empty
```

<a name="processing-jobs-for-a-given-number-of-seconds"></a>
#### 지정 시간 동안만 잡 처리하기

`--max-time` 옵션을 사용하면, 워커가 일정 시간(초 단위)동안 잡을 처리하고 종료할 수 있습니다. 이 역시 [Supervisor](#supervisor-configuration)와 함께 사용해, 잡을 처리한 시간이 일정 시간에 도달하면 워커를 재시작하도록 만들 수 있습니다.

```shell
# 한 시간(3600초)동안 잡 처리 후 종료
php artisan queue:work --max-time=3600
```

<a name="worker-sleep-duration"></a>
#### 워커의 대기 시간 설정

큐에 잡이 있으면 워커는 지연없이 계속 잡을 처리합니다. 하지만 잡이 없을 때는 `--sleep` 옵션으로 설정한 시간(초)만큼 "잠시 대기"하게 됩니다. 대기 중에는 새로운 잡도 처리되지 않습니다.

```shell
php artisan queue:work --sleep=3
```

<a name="maintenance-mode-queues"></a>
#### 유지보수 모드와 큐

애플리케이션이 [유지보수 모드](/docs/12.x/configuration#maintenance-mode)에 들어가면 큐에 쌓인 잡은 처리되지 않습니다. 정상 모드로 전환하면 대기 중이던 잡이 다시 정상적으로 처리됩니다.

유지보수 모드에서도 강제로 잡을 처리하려면 `--force` 옵션을 사용하세요.

```shell
php artisan queue:work --force
```

<a name="resource-considerations"></a>
#### 리소스 관리 주의사항

데몬 워커는 잡 하나를 처리할 때마다 프레임워크를 '재부팅'하지 않습니다. 따라서 잡 처리 후 GD 라이브러리 등으로 사용한 리소스는 `imagedestroy`처럼 수동으로 반드시 해제해주셔야 합니다.

<a name="queue-priorities"></a>
### 큐 우선순위 지정하기

작업 큐 처리 우선순위를 정하고자 할 때가 있습니다. 예를 들어 `config/queue.php`에서 `redis` 커넥션의 기본 큐를 `low`로 지정할 수 있습니다. 하지만 중요한 잡은 다음과 같이 `high` 큐로 보낼 수 있습니다.

```php
dispatch((new Job)->onQueue('high'));
```

그런 다음, 워커를 아래처럼 실행해 `high` 큐를 모두 처리한 뒤에만 `low` 큐를 처리하도록 할 수 있습니다. 큐 이름은 콤마로 구분해서 나열합니다.

```shell
php artisan queue:work --queue=high,low
```

<a name="queue-workers-and-deployment"></a>
### 큐 워커와 배포

큐 워커는 장기 실행 프로세스이기 때문에 앱 코드가 수정되어도 자동으로 감지하지 못합니다. 따라서 가장 간단한 배포 방법은 배포 도중 워커를 재시작하는 것입니다. 전체 워커를 graceful하게 재시작하려면 아래 명령어를 사용하세요.

```shell
php artisan queue:restart
```

이 명령은 각 워커에게 현재 실행 중인 잡만 끝내고 종료한 뒤, Supervisor 등 프로세스 매니저가 워커를 자동으로 다시 실행하게 합니다.

> [!NOTE]
> 큐는 [캐시](/docs/12.x/cache)를 통해 재시작 신호를 저장하므로, 이 기능을 사용하기 전에 애플리케이션의 캐시 드라이버가 적절히 설정되었는지 확인하세요.

<a name="job-expirations-and-timeouts"></a>
### 잡 만료 및 타임아웃

<a name="job-expiration"></a>
#### 잡 만료

`config/queue.php` 설정 파일에서 각 큐 커넥션은 `retry_after` 옵션을 가집니다. 이 옵션은 잡이 처리 중일 때 몇 초(초 단위) 후에 재시도를 시작할지 결정합니다. 예를 들어 `retry_after` 값을 90으로 설정하면, 잡이 90초 동안 처리됐는데 여전히 완료/삭제되지 않았다면 큐에서 나온 잡이 다시 대기열로 되돌아갑니다. 일반적으로 이 값은 잡이 어떤 경우든 예상 최대 처리 시간을 기준으로 설정해야 합니다.

> [!WARNING]
> Amazon SQS 커넥션은 유일하게 `retry_after` 값을 따로 두지 않습니다. SQS는 [디폴트 Visibility Timeout](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/AboutVT.html) 설정에 따라 재시도가 이루어지며, 이 값은 AWS 콘솔에서 관리합니다.

<a name="worker-timeouts"></a>
#### 워커 타임아웃

`queue:work` 아티즌 명령어에는 `--timeout` 옵션이 있습니다. 기본값은 60초입니다. 잡 한 건 처리에 이 시간을 초과하면, 해당 잡을 처리 중인 워커는 에러와 함께 종료됩니다. 일반적으로 이 경우 서버에 설정된 [프로세스 매니저](#supervisor-configuration)가 워커를 자동으로 재실행합니다.

```shell
php artisan queue:work --timeout=60
```

`retry_after` 설정과 `--timeout` 옵션은 서로 다르지만, 함께 병행해 설정해야 잡이 유실되지 않고, 한 번만 실행됨을 보장할 수 있습니다.

> [!WARNING]
> `--timeout` 값은 항상 `retry_after` 값보다 "몇 초 정도" 작게 주어야 합니다. 이렇게 하면, 워커가 중단된 잡을 처리하려다 멈추기 전에, 잡이 미리 '재처리 대기열'로 넘어가서 잡이 중복 실행될 위험을 줄일 수 있습니다. 만약 `--timeout`이 `retry_after` 보다 크다면, 잡이 두 번 처리될 수도 있습니다.

<a name="supervisor-configuration"></a>
## Supervisor 설정

운영 환경에서는 반드시 `queue:work` 프로세스를 항상 실행되게 유지할 필요가 있습니다. 워커 프로세스는 여러 이유(워커 타임아웃 초과, `queue:restart` 명령 실행 등)로 중단될 수 있습니다.

따라서, 워커가 종료될 때(에러 등이 원인일 수도 있음) 이를 감지해 자동으로 다시 실행시킬 수 있는 프로세스 관리자 설정이 꼭 필요합니다. 또한, 이어서 설명할 Supervisor 등의 도구는 동시에 몇 개의 워커를 동작시킬지 지정할 수도 있습니다. Supervisor는 Linux 환경에서 많이 사용되는 프로세스 관리 툴이며, 아래에서 설정 방법을 안내합니다.

<a name="installing-supervisor"></a>
#### Supervisor 설치

Supervisor는 리눅스 시스템에서 돌아가는 프로세스 관리 도구로, 워커가 실패하면 자동으로 재시작합니다. Ubuntu 환경에서는 아래 명령어로 설치할 수 있습니다.

```shell
sudo apt-get install supervisor
```

> [!NOTE]
> Supervisor 직접 설치/관리가 어렵다고 느껴진다면, [Laravel Cloud](https://cloud.laravel.com) 사용을 고려해보세요. 완전히 관리되는 라라벨 큐 워커 실행 플랫폼을 제공합니다.

<a name="configuring-supervisor"></a>
#### Supervisor 설정

Supervisor의 설정 파일은 일반적으로 `/etc/supervisor/conf.d` 디렉터리에 저장됩니다. 이 디렉터리 아래에 원하는 만큼 설정 파일을 만들어, Supervisor가 각 프로세스를 어떻게 관리할지 정의할 수 있습니다. 예를 들어, `laravel-worker.conf` 파일을 만들어 `queue:work` 프로세스를 시작/감시하도록 할 수 있습니다.

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

이 예시에서, `numprocs` 설정값은 Supervisor가 8개의 `queue:work` 프로세스를 동시에 실행하고, 각각을 자동으로 재시작하도록 합니다. `command` 설정은 원하는 큐 커넥션/옵션에 맞게 수정해야 합니다.

> [!WARNING]
> `stopwaitsecs` 값은 가장 오래 걸리는 잡의 실행 시간보다 커야 합니다. 그렇지 않으면 Supervisor가 잡 완료 전에 해당 프로세스를 강제로 종료시킬 수 있습니다.

<a name="starting-supervisor"></a>
#### Supervisor 시작하기

설정 파일을 작성했다면, Supervisor 설정을 갱신하고 프로세스를 실행하기 위해 아래 명령어를 실행하면 됩니다.

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start "laravel-worker:*"
```

Supervisor에 대한 더 자세한 내용은 [Supervisor 공식 문서](http://supervisord.org/index.html)를 참고하세요.

<a name="dealing-with-failed-jobs"></a>
## 실패한 잡 처리

큐잉된 잡이 실패할 수 있습니다. 걱정 마세요, 모든 게 계획대로 흘러가진 않으니까요! 라라벨은 [잡의 최대 시도 횟수 설정](#max-job-attempts-and-timeout)을 간편하게 할 수 있도록 해줍니다. 비동기 잡이 이 횟수만큼 재시도해도 실패한다면, 해당 잡은 `failed_jobs` 데이터베이스 테이블에 저장됩니다. [동기식으로 디스패치된 잡](/docs/12.x/queues#synchronous-dispatching)은 이 테이블에 저장되지 않고, 예외가 즉시 앱에서 처리됩니다.

신규 라라벨 프로젝트에는 `failed_jobs` 테이블을 생성하는 마이그레이션이 기본으로 포함되어 있습니다. 만약 해당 마이그레이션이 없다면, 아래처럼 `make:queue-failed-table` 명령어로 생성할 수 있습니다.

```shell
php artisan make:queue-failed-table

php artisan migrate
```

[큐 워커](#running-the-queue-worker) 실행 시, `queue:work` 명령어의 `--tries` 옵션으로 잡의 최대 재시도 횟수를 설정할 수 있습니다. 이 옵션을 지정하지 않으면, 잡 클래스의 `$tries` 프로퍼티에 지정된 횟수 또는 기본 1회만 시도됩니다.

```shell
php artisan queue:work redis --tries=3
```

`--backoff` 옵션을 이용하면, 잡이 예외를 만나 실패했을 때 다음 시도 전 대기할 시간을(초 단위로) 지정할 수 있습니다. 기본적으로는 잡이 즉시 다시 대기열에 올라갑니다.

```shell
php artisan queue:work redis --tries=3 --backoff=3
```

좀 더 세밀하게, 잡 별로 재시도 전에 기다릴 시간을 지정하고 싶다면, 잡 클래스에 `backoff` 프로퍼티를 추가할 수 있습니다.

```php
/**
 * The number of seconds to wait before retrying the job.
 *
 * @var int
 */
public $backoff = 3;
```

잡의 backoff 시간을 동적으로 계산하려면, 잡 클래스에 `backoff` 메서드를 정의할 수도 있습니다.

```php
/**
 * Calculate the number of seconds to wait before retrying the job.
 */
public function backoff(): int
{
    return 3;
}
```

더 복잡한 '지수 backoff' 로직이 필요하다면, `backoff` 메서드에서 배열을 반환하면 됩니다. 아래 예시에서는 첫 번째 재시도는 1초, 두 번째는 5초, 세 번째는 10초, 그 이후부터는 계속 10초씩 대기합니다.

```php
/**
 * Calculate the number of seconds to wait before retrying the job.
 *
 * @return array<int, int>
 */
public function backoff(): array
{
    return [1, 5, 10];
}
```

<a name="cleaning-up-after-failed-jobs"></a>

### 작업 실패 후 정리 작업

특정 작업이 실패한 경우, 사용자에게 알림을 보내거나 작업 중 일부만 완료된 상태를 되돌리고 싶을 수 있습니다. 이를 위해 작업 클래스에 `failed` 메서드를 정의할 수 있습니다. 실패의 원인이 된 `Throwable` 인스턴스가 `failed` 메서드에 전달됩니다.

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

    /**
     * Handle a job failure.
     */
    public function failed(?Throwable $exception): void
    {
        // Send user notification of failure, etc...
    }
}
```

> [!WARNING]
> `failed` 메서드가 실행되기 전에 작업의 새 인스턴스가 생성됩니다. 따라서 `handle` 메서드 내에서 변경된 클래스 속성 값은 모두 사라집니다.

<a name="retrying-failed-jobs"></a>
### 실패한 작업 재시도하기

`failed_jobs` 데이터베이스 테이블에 저장된 모든 실패 작업을 확인하려면 `queue:failed` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan queue:failed
```

`queue:failed` 명령어는 작업 ID, 연결 정보, 큐 이름, 실패 시각 등 작업에 대한 여러 정보를 표시합니다. 작업 ID는 해당 실패 작업을 재시도하는 데 사용할 수 있습니다. 예를 들어, ID가 `ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece`인 실패 작업을 재시도하려면 다음 명령어를 실행합니다.

```shell
php artisan queue:retry ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece
```

필요하다면, 여러 작업 ID를 한 번에 전달할 수도 있습니다.

```shell
php artisan queue:retry ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece 91401d2c-0784-4f43-824c-34f94a33c24d
```

특정 큐의 모든 실패 작업을 재시도할 수도 있습니다.

```shell
php artisan queue:retry --queue=name
```

모든 실패 작업을 한꺼번에 재시도하려면 ID에 `all`을 전달하여 실행합니다.

```shell
php artisan queue:retry all
```

실패한 작업을 삭제하려면 `queue:forget` 명령어를 사용할 수 있습니다.

```shell
php artisan queue:forget 91401d2c-0784-4f43-824c-34f94a33c24d
```

> [!NOTE]
> [Horizon](/docs/12.x/horizon)을 사용할 경우, 실패 작업 삭제에는 `queue:forget` 대신 `horizon:forget` 명령어를 사용해야 합니다.

`failed_jobs` 테이블에서 모든 실패 작업을 삭제하려면 `queue:flush` 명령어를 실행하세요.

```shell
php artisan queue:flush
```

<a name="ignoring-missing-models"></a>
### 누락된 모델 무시하기

작업에 Eloquent 모델을 주입하면, 해당 모델이 직렬화된 후 큐에 저장되고 작업 처리 시 데이터베이스에서 다시 조회됩니다. 하지만 작업이 처리가 시작되기 전에 해당 모델이 삭제된다면, 작업이 `ModelNotFoundException`과 함께 실패할 수 있습니다.

이런 경우를 편리하게 처리하려면, 작업 클래스의 `deleteWhenMissingModels` 속성을 `true`로 설정하면 됩니다. 이 속성이 `true`인 경우, 해당 모델이 존재하지 않을 때 Laravel은 예외를 발생시키지 않고 조용히 작업을 버립니다.

```php
/**
 * Delete the job if its models no longer exist.
 *
 * @var bool
 */
public $deleteWhenMissingModels = true;
```

<a name="pruning-failed-jobs"></a>
### 실패한 작업 기록 정리하기

애플리케이션의 `failed_jobs` 테이블의 기록을 정리(prune)하려면 `queue:prune-failed` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan queue:prune-failed
```

기본적으로 24시간이 지난 모든 실패 작업 기록이 삭제됩니다. `--hours` 옵션을 명령어에 추가하면 최근 N시간 이내에 추가된 실패 작업만 남기고 나머지를 삭제할 수 있습니다. 예를 들어, 48시간이 지난 기록을 삭제하려면 다음과 같이 실행하십시오.

```shell
php artisan queue:prune-failed --hours=48
```

<a name="storing-failed-jobs-in-dynamodb"></a>
### 실패한 작업을 DynamoDB에 저장하기

Laravel은 관계형 데이터베이스 테이블 대신 [DynamoDB](https://aws.amazon.com/dynamodb)에 실패 작업 기록을 저장하는 기능도 지원합니다. 그러나 모든 실패 작업 기록을 저장할 DynamoDB 테이블을 직접 생성해야 합니다. 일반적으로 이 테이블 이름은 `failed_jobs`로 지정하지만, 애플리케이션의 `queue` 설정 파일에서 `queue.failed.table` 설정 값에 맞춰 이름을 지정해야 합니다.

`failed_jobs` 테이블에는 문자열 타입의 파티션 키 `application`과, 문자열 타입의 정렬 키 `uuid`가 있어야 합니다. 키의 `application` 부분에는 애플리케이션의 `app` 설정 파일의 `name`에 정의된 값이 들어갑니다. 따라서 같은 DynamoDB 테이블을 여러 라라벨 애플리케이션의 실패 작업 저장소로 사용할 수 있습니다.

또한, Laravel 애플리케이션이 Amazon DynamoDB와 통신할 수 있도록 AWS SDK를 반드시 설치해야 합니다.

```shell
composer require aws/aws-sdk-php
```

그 다음, `queue.failed.driver` 환경설정 값을 `dynamodb`로 지정하십시오. 또한 실패 작업 설정 배열에 `key`, `secret`, `region` 값을 반드시 지정해야 하며, 이는 인증에 사용됩니다. `dynamodb` 드라이버를 사용하면 `queue.failed.database` 설정 옵션은 필요하지 않습니다.

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
### 실패 작업 저장 비활성화

실패한 작업이 저장되지 않고 바로 폐기되도록 하려면, `queue.failed.driver` 설정 값을 `null`로 지정하면 됩니다. 일반적으로 `QUEUE_FAILED_DRIVER` 환경 변수로 이 설정을 할 수 있습니다.

```ini
QUEUE_FAILED_DRIVER=null
```

<a name="failed-job-events"></a>
### 실패 작업 이벤트

작업이 실패했을 때 실행되는 이벤트 리스너를 등록하고 싶다면, `Queue` 파사드의 `failing` 메서드를 사용할 수 있습니다. 예를 들어, Laravel에 기본 포함된 `AppServiceProvider`의 `boot` 메서드에서 이 이벤트에 클로저를 첨부할 수 있습니다.

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
## 큐에서 작업 삭제하기

> [!NOTE]
> [Horizon](/docs/12.x/horizon)을 사용할 경우, 큐에서 작업을 삭제하려면 `queue:clear` 대신 `horizon:clear` 명령어를 사용해야 합니다.

기본 연결의 기본 큐에서 모든 작업을 삭제하고 싶다면 `queue:clear` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan queue:clear
```

특정 연결 및 큐에서 작업을 삭제하려면 `connection` 인수와 `queue` 옵션을 사용할 수 있습니다.

```shell
php artisan queue:clear redis --queue=emails
```

> [!WARNING]
> 큐에서 작업 삭제 기능은 SQS, Redis, 데이터베이스 큐 드라이버에서만 지원됩니다. 또한 SQS 메시지 삭제에는 최대 60초가 걸릴 수 있으므로, 큐를 비운 이후 60초 이내에 해당 SQS 큐로 전송된 작업도 함께 삭제될 수 있습니다.

<a name="monitoring-your-queues"></a>
## 큐 모니터링

큐에 갑자기 대량의 작업이 몰리면 큐 처리 속도가 느려질 수 있고, 대기 시간이 길어질 수 있습니다. 원한다면, 큐의 작업 수가 지정한 임계값을 초과할 때 Laravel이 알림을 보낼 수 있습니다.

우선, [매분 실행되도록 스케줄링](/docs/12.x/scheduling)하여 `queue:monitor` 명령어를 동작시켜야 합니다. 이 명령어는 모니터링하고자 하는 큐 이름들과 최대 작업 개수 임계값을 매개변수로 받습니다.

```shell
php artisan queue:monitor redis:default,redis:deployments --max=100
```

이 명령어를 스케줄링하는 것만으로는 큐가 과부하 상태일 때 알림이 발생하지 않습니다. 명령어 실행 시 큐의 작업 수가 임계값을 초과하면, `Illuminate\Queue\Events\QueueBusy` 이벤트가 발생합니다. 이 이벤트를 애플리케이션의 `AppServiceProvider` 등에서 리스닝하여, 개발팀 또는 자신에게 알림을 발송할 수 있습니다.

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

작업을 디스패치하는 코드를 테스트할 때, 실제로 작업을 실행하지 않도록 Laravel에 지시하고 싶을 경우가 있습니다. (작업 자체의 코드는 별도의 테스트에서 직접 인스턴스를 생성하고 `handle` 메서드를 직접 호출하여 테스트할 수 있습니다.)  
`Queue` 파사드의 `fake` 메서드를 사용하면 작업이 실제 큐에 추가되지 않도록 만들 수 있습니다. 이 메서드 호출 후, 애플리케이션이 작업을 큐에 넣으려 시도하였는지 다양한 방식을 통해 assert(확인)할 수 있습니다.

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

    // Assert that a closure was pushed to the queue...
    Queue::assertClosurePushed();

    // Assert that a closure was not pushed...
    Queue::assertClosureNotPushed();

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

        // Assert that a closure was pushed to the queue...
        Queue::assertClosurePushed();

        // Assert that a closure was not pushed...
        Queue::assertClosureNotPushed();

        // Assert the total number of jobs that were pushed...
        Queue::assertCount(3);
    }
}
```

`assertPushed`, `assertNotPushed`, `assertClosurePushed`, `assertClosureNotPushed` 메서드에 클로저를 전달하여, 주어진 "조건을 만족하는" 작업이 큐에 추가되었는지 직접 검사할 수도 있습니다. 조건을 만족하는 작업이 하나라도 있으면, assert는 통과합니다.

```php
use Illuminate\Queue\CallQueuedClosure;

Queue::assertPushed(function (ShipOrder $job) use ($order) {
    return $job->order->id === $order->id;
});

Queue::assertClosurePushed(function (CallQueuedClosure $job) {
    return $job->name === 'validate-order';
});
```

<a name="faking-a-subset-of-jobs"></a>
### 일부 작업만 가짜(fake)로 처리하기

특정 작업만 가짜로 처리하고, 나머지 작업은 실제로 실행하고 싶을 때는 `fake` 메서드에 가짜로 처리할 작업 클래스명을 배열로 전달하세요.

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

반대로, 지정한 작업만 빼고 나머지 모든 작업을 fake로 처리하고 싶다면 `except` 메서드를 사용할 수 있습니다.

```php
Queue::fake()->except([
    ShipOrder::class,
]);
```

<a name="testing-job-chains"></a>
### 잡 체인(Chain) 테스트

잡 체인(여러 작업을 순차적으로 연결한 것)을 테스트하려면, `Bus` 파사드의 fake 기능을 활용해야 합니다.  
`Bus` 파사드의 `assertChained` 메서드는 [작업 체인](/docs/12.x/queues#job-chaining)이 디스패치되었는지 확인할 수 있습니다.  
`assertChained` 메서드에는 연결된 잡들의 클래스명을 배열로 넘길 수 있습니다.

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

위의 예시처럼, 체인으로 연결된 작업 배열은 클래스명 배열로 줄 수도 있고, 실제 작업 인스턴스들의 배열로도 전달할 수 있습니다.  
이 경우, Laravel은 인스턴스의 클래스 및 속성 값까지도 실제 디스패치된 잡과 일치하는지 검사합니다.

```php
Bus::assertChained([
    new ShipOrder,
    new RecordShipment,
    new UpdateInventory,
]);
```

`assertDispatchedWithoutChain` 메서드를 이용하면, 특정 작업이 체인 없이 단독 디스패치되었는지 확인할 수 있습니다.

```php
Bus::assertDispatchedWithoutChain(ShipOrder::class);
```

<a name="testing-chain-modifications"></a>
#### 체인 수정 테스트

체인에 연결된 잡이 기존 체인의 앞이나 뒤에 작업을 추가하는 경우([체인에 작업 추가](#adding-jobs-to-the-chain) 참고), 작업의 `assertHasChain` 메서드를 사용해 기대한 작업 체인 배열이 남아 있는지 확인할 수 있습니다.

```php
$job = new ProcessPodcast;

$job->handle();

$job->assertHasChain([
    new TranscribePodcast,
    new OptimizePodcast,
    new ReleasePodcast,
]);
```

`assertDoesntHaveChain` 메서드로 작업의 남은 체인이 비어 있는지도 확인할 수 있습니다.

```php
$job->assertDoesntHaveChain();
```

<a name="testing-chained-batches"></a>
#### 체인에 포함된 배치 테스트

체인 내에 [여러 작업의 배치(batch)](#chains-and-batches)가 포함되어 있다면, 체인이 예상대로 배치와 함께 디스패치되었는지 `Bus::chainedBatch` 구문을 chain 확인용 배열에 넣어 assert할 수 있습니다.

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

`Bus` 파사드의 `assertBatched` 메서드를 사용하면 [여러 작업의 배치](/docs/12.x/queues#job-batching)가 디스패치되었는지 검사할 수 있습니다.  
이 메서드는 `Illuminate\Bus\PendingBatch` 인스턴스를 인수로 받는 클로저를 통해 배치 내 작업들을 확인하게 해줍니다.

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

`assertBatchCount` 메서드를 사용해서 주어진 개수만큼 배치가 디스패치되었는지 확인할 수 있습니다.

```php
Bus::assertBatchCount(3);
```

`assertNothingBatched`를 사용하면 디스패치된 배치가 하나도 없는지 확인할 수 있습니다.

```php
Bus::assertNothingBatched();
```

<a name="testing-job-batch-interaction"></a>
#### 작업과 배치의 상호작용 테스트

개별 작업이 자신의 배치와 상호작용하는(예: 작업이 배치의 추가 처리를 중단시키는) 경우를 테스트해야 할 수도 있습니다.  
이때는 `withFakeBatch` 메서드로 작업에 가짜(fake) 배치를 할당합니다. 이 메서드는 작업 인스턴스와 가짜 배치를 튜플로 반환합니다.

```php
[$job, $batch] = (new ShipOrder)->withFakeBatch();

$job->handle();

$this->assertTrue($batch->cancelled());
$this->assertEmpty($batch->added);
```

<a name="testing-job-queue-interactions"></a>
### 작업과 큐 상호작용 테스트

종종, 큐에 올라간 작업이 [스스로 다시 큐에 등록(release)](#manually-releasing-a-job)되거나, 스스로 삭제되었는지 등을 테스트하고 싶을 수 있습니다.  
이럴 때는 작업 인스턴스를 만들고 `withFakeQueueInteractions` 메서드를 호출합니다.

큐와의 상호작용이 가짜로 처리된 후, 작업의 `handle` 메서드를 직접 호출하세요.  
작업 실행 뒤에는 `assertReleased`, `assertDeleted`, `assertNotDeleted`, `assertFailed`, `assertFailedWith`, `assertNotFailed` 등의 메서드를 이용해 큐로의 상호작용을 assert(검증)할 수 있습니다.

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
## 잡(Job) 이벤트

`Queue` [파사드](/docs/12.x/facades)의 `before` 및 `after` 메서드를 사용하면, 큐 작업이 처리되기 전후에 실행될 콜백을 등록할 수 있습니다.  
이 콜백을 이용해 추가 로그를 남기거나 대시보드 용 통계 수치를 올리는 등의 추가 처리를 할 수 있습니다.  
일반적으로 [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에서 이 메서드를 호출합니다.  
아래는 Laravel에 포함된 `AppServiceProvider`를 활용한 예시입니다.

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

`Queue` [파사드](/docs/12.x/facades)의 `looping` 메서드를 써서, 워커가 큐에서 작업을 가져오기 전에 실행할 콜백을 지정할 수도 있습니다.  
예를 들어, 이전에 실패한 작업 때문에 남아 있던 트랜잭션을 롤백하도록 클로저를 등록할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Queue;

Queue::looping(function () {
    while (DB::transactionLevel() > 0) {
        DB::rollBack();
    }
});
```