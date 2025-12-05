# 큐 (Queues)

- [소개](#introduction)
    - [커넥션과 큐의 차이](#connections-vs-queues)
    - [드라이버별 참고 사항 및 사전 준비](#driver-prerequisites)
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
- [잡 디스패치](#dispatching-jobs)
    - [지연 디스패치](#delayed-dispatching)
    - [동기 디스패치](#synchronous-dispatching)
    - [잡과 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [잡 체이닝](#job-chaining)
    - [큐 및 커넥션 지정](#customizing-the-queue-and-connection)
    - [최대 시도/타임아웃 값 지정](#max-job-attempts-and-timeout)
    - [SQS FIFO 및 페어 큐](#sqs-fifo-and-fair-queues)
    - [큐 페일오버](#queue-failover)
    - [에러 처리](#error-handling)
- [잡 배치 처리](#job-batching)
    - [배치 잡 정의](#defining-batchable-jobs)
    - [배치 디스패치](#dispatching-batches)
    - [체인과 배치](#chains-and-batches)
    - [배치에 잡 추가](#adding-jobs-to-batches)
    - [배치 조회](#inspecting-batches)
    - [배치 취소](#cancelling-batches)
    - [배치 실패](#batch-failures)
    - [배치 정리](#pruning-batches)
    - [DynamoDB에 배치 저장하기](#storing-batches-in-dynamodb)
- [클로저 큐잉](#queueing-closures)
- [큐 워커 실행](#running-the-queue-worker)
    - [`queue:work` 명령어](#the-queue-work-command)
    - [큐 우선순위](#queue-priorities)
    - [큐 워커 및 배포](#queue-workers-and-deployment)
    - [잡 만료 및 타임아웃](#job-expirations-and-timeouts)
    - [큐 워커 일시정지 및 재개](#pausing-and-resuming-queue-workers)
- [Supervisor 설정](#supervisor-configuration)
- [실패한 잡 처리](#dealing-with-failed-jobs)
    - [실패한 잡 후처리](#cleaning-up-after-failed-jobs)
    - [실패한 잡 재시도](#retrying-failed-jobs)
    - [누락된 모델 무시](#ignoring-missing-models)
    - [실패한 잡 정리](#pruning-failed-jobs)
    - [DynamoDB에 실패한 잡 저장](#storing-failed-jobs-in-dynamodb)
    - [실패 잡 저장 비활성화](#disabling-failed-job-storage)
    - [실패한 잡 이벤트](#failed-job-events)
- [큐에서 잡 삭제](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [일부 잡 페이크](#faking-a-subset-of-jobs)
    - [잡 체인 테스트](#testing-job-chains)
    - [잡 배치 테스트](#testing-job-batches)
    - [잡/큐 상호작용 테스트](#testing-job-queue-interactions)
- [잡 이벤트](#job-events)

<a name="introduction"></a>
## 소개 (Introduction)

웹 애플리케이션을 개발하면서, 예를 들어 업로드된 CSV 파일을 파싱하고 저장하는 작업처럼 일반적인 웹 요청 내에서 처리하기에 시간이 너무 오래 걸리는 작업이 있을 수 있습니다. 다행히 Laravel에서는 이러한 작업을 백그라운드에서 처리할 수 있도록 손쉽게 큐에 잡을 생성할 수 있습니다. 시간 소모가 많은 작업을 큐로 이동함으로써, 애플리케이션은 웹 요청에 매우 빠르게 응답하고, 사용자 경험을 크게 향상시킬 수 있습니다.

Laravel 큐는 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 또는 관계형 데이터베이스와 같이 다양한 큐 백엔드에서 동일한 큐 API를 제공하며, 통합된 큐잉 환경을 제공합니다.

큐 관련 설정은 애플리케이션의 `config/queue.php` 파일에 저장됩니다. 이 파일에는 프레임워크에 포함된 각 큐 드라이버(데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 등)의 커넥션 설정이 포함되어 있습니다. 개발과 테스트 용도로는 잡을 즉시 실행하는 동기 드라이버도 제공되며, 큐에 넣은 잡을 즉시 폐기하는 `null` 큐 드라이버도 포함되어 있습니다.

> [!NOTE]
> Laravel Horizon은 Redis 기반 큐를 위한 미려한 대시보드 및 설정 시스템을 제공합니다. 자세한 내용은 [Horizon 공식 문서](/docs/12.x/horizon)를 참고하십시오.

<a name="connections-vs-queues"></a>
### 커넥션과 큐의 차이

Laravel 큐를 본격적으로 사용하기 전에 "커넥션(Connection)"과 "큐(Queue)"의 차이를 이해하는 것이 중요합니다. `config/queue.php` 설정 파일에는 `connections`라는 배열이 있습니다. 이 설정은 Amazon SQS, Beanstalk, Redis와 같은 백엔드 큐 서비스들과의 커넥션(연결 정보)을 의미합니다. 그러나, 각각의 큐 커넥션에는 여러 개의 "큐"가 존재할 수 있으며, 이는 여러 잡이 쌓이는 별도의 공간(예: 우선순위 큐의 스택)처럼 생각할 수 있습니다.

각 커넥션 설정 예시에는 `queue` 속성이 포함되어 있습니다. 이 속성은 해당 커넥션에 잡을 보낼 때 기본적으로 사용되는 큐를 지정합니다. 즉, 잡을 디스패치할 때 명시적으로 어느 큐에 보낼지 정의하지 않으면, 커넥션 설정의 `queue` 속성에 지정된 큐로 디스패치됩니다.

```php
use App\Jobs\ProcessPodcast;

// 이 잡은 기본 커넥션의 기본 큐로 전송됩니다...
ProcessPodcast::dispatch();

// 이 잡은 기본 커넥션의 "emails" 큐로 전송됩니다...
ProcessPodcast::dispatch()->onQueue('emails');
```

대부분의 애플리케이션에서는 잡을 여러 큐로 분배할 필요 없이 단일 큐만 사용해도 충분합니다. 하지만, 우선순위나 작업 종류에 따라 여러 큐로 분리하면 큐 워커에서 우선순위를 제어할 수 있으므로, 작업 처리 방식을 더욱 유연하게 관리할 수 있습니다. 예를 들어, `high` 큐에 잡을 보내고 싶을 때, 해당 큐를 먼저 처리하는 워커를 아래와 같이 실행할 수 있습니다.

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버별 참고 사항 및 사전 준비

<a name="database"></a>
#### 데이터베이스

`database` 큐 드라이버를 사용하려면, 잡을 저장할 데이터베이스 테이블이 필요합니다. 일반적으로 Laravel에는 기본적으로 `0001_01_01_000002_create_jobs_table.php` [마이그레이션](/docs/12.x/migrations)이 포함되어 있습니다. 만약 해당 마이그레이션이 없다면, 아래 명령어로 생성할 수 있습니다.

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면, `config/database.php` 파일에서 Redis 데이터베이스 커넥션을 설정해야 합니다.

> [!WARNING]
> `redis` 큐 드라이버는 `serializer` 및 `compression` Redis 옵션을 지원하지 않습니다.

<a name="redis-cluster"></a>
##### Redis 클러스터

Redis 큐 커넥션이 [Redis 클러스터](https://redis.io/docs/latest/operate/rs/databases/durability-ha/clustering)를 사용하는 경우, 큐 이름에 [key hash tag](https://redis.io/docs/latest/develop/using-commands/keyspace/#hashtags)를 포함해야 합니다. 이는 특정 큐의 모든 Redis 키가 동일한 해시 슬롯에 저장되도록 보장하기 위함입니다.

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
##### 블로킹

Redis 큐를 사용할 때, `block_for` 설정 옵션을 활용하여 잡이 대기열에 들어올 때까지 드라이버가 얼마나 대기할지 지정할 수 있습니다. 큐 작업량에 따라 이 값을 적절히 조정하면 Redis 데이터베이스를 계속 폴링하는 것보다 효율적입니다. 예를 들어, `block_for`를 `5`로 설정하면 잡이 대기열에 들어올 때까지 최대 5초간 블록(대기)합니다.

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
> `block_for`를 `0`으로 설정하면, 잡이 도착할 때까지 큐 워커가 무한히 대기하게 되어, 다음 잡이 처리되기 전까지 `SIGTERM`과 같은 신호를 처리할 수 없게 됩니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 사전 준비

아래 큐 드라이버를 사용하려면 각종 추가 의존성을 Composer로 설치해야 합니다.

<div class="content-list" markdown="1">

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~2.0` 또는 phpredis PHP 확장 모듈
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`

</div>

<a name="creating-jobs"></a>
## 잡 생성 (Creating Jobs)

<a name="generating-job-classes"></a>
### 잡 클래스 생성

기본적으로, 애플리케이션에서 생성된 큐잉 잡은 모두 `app/Jobs` 디렉토리에 저장됩니다. 만약 해당 디렉토리가 없다면, `make:job` Artisan 명령어를 실행할 때 자동으로 생성됩니다.

```shell
php artisan make:job ProcessPodcast
```

생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하며, 이 인터페이스는 해당 잡이 큐에 올려져 비동기적으로 실행되어야 함을 Laravel에 알립니다.

> [!NOTE]
> 잡 스텁은 [스텁 퍼블리싱](/docs/12.x/artisan#stub-customization) 기능을 사용하여 커스터마이즈할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조

잡 클래스는 일반적으로 매우 단순하며, 큐에서 잡이 처리될 때 호출되는 `handle` 메서드 하나만을 포함하는 경우가 많습니다. 예를 들어, 팟캐스트 파일을 업로드하고 게시하기 전에 처리하는 서비스가 있다고 가정해봅시다.

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

위 예시에서 보듯, [Eloquent 모델](/docs/12.x/eloquent)을 큐잉 잡의 생성자에 직접 전달할 수 있습니다. 잡이 `Queueable` 트레이트를 사용할 경우, Eloquent 모델과 미리 로드된 연관관계가 큐잉 및 처리 과정에서 올바르게 직렬화/역직렬화됩니다.

잡 생성자에서 Eloquent 모델을 받을 경우, 이 모델의 식별자만 큐에 직렬화되어 저장됩니다. 실제 잡이 처리될 때, 큐 시스템이 DB에서 전체 모델 인스턴스와 연관관계를 자동으로 다시 조회합니다. 이 방식은 큐에 전송되는 잡 페이로드의 크기를 크게 줄일 수 있습니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드 의존성 주입

잡의 `handle` 메서드는 큐에서 잡이 실행될 때 호출됩니다. 이 메서드에서는 의존성 주입을 자유롭게 사용할 수 있으며, Laravel [서비스 컨테이너](/docs/12.x/container)가 자동으로 의존성을 주입합니다.

서비스 컨테이너의 의존성 주입 방식을 완전히 제어하고 싶다면, 컨테이너의 `bindMethod`를 사용할 수 있습니다. 이 메서드는 보통 애플리케이션의 `App\Providers\AppServiceProvider` [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에서 호출합니다.

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 이미지 원본과 같은 바이너리 데이터는 큐잉 잡에 전달하기 전에 반드시 `base64_encode` 함수를 사용하여 인코딩해야 합니다. 그렇지 않을 경우, 잡을 큐에 올릴 때 JSON 직렬화가 제대로 동작하지 않을 수 있습니다.

<a name="handling-relationships"></a>
#### 큐잉된 연관관계

큐에 잡이 올라갈 때, 로드된 Eloquent 모델의 모든 연관관계도 함께 직렬화되므로, 잡의 직렬화 문자열이 상당히 커질 수 있습니다. 게다가, 잡이 역직렬화되면서 연관관계가 재조회될 때, 직렬화 당시 주었던 연관관계 제약조건이 사라지므로 전체 연관관계가 로드됩니다. 일부 연관관계 데이터만 사용할 경우, 반드시 잡 내부에서 필요한 제약조건을 다시 적용해야 합니다.

모델의 속성 값을 세팅할 때 `withoutRelations` 메서드를 사용하면, 연관관계를 포함하지 않고 모델 인스턴스를 반환할 수 있습니다.

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

[PHP 생성자 프로퍼티 프로모션](https://www.php.net/manual/en/language.oop5.decon.php#language.oop5.decon.constructor.promotion)을 사용할 때, Eloquent 모델의 연관관계를 직렬화하지 않도록 하려면 `WithoutRelations` 속성을 사용할 수 있습니다.

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

모든 모델에 연관관계 직렬화를 비활성화하려면, 클래스 전체에 `WithoutRelations` 속성을 붙일 수도 있습니다.

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

단일 모델이 아닌, Eloquent 모델의 컬렉션이나 배열을 잡에 전달할 경우, 이 모델들의 연관관계는 역직렬화 및 실행 시 복원되지 않습니다. 많은 수의 모델을 다루는 잡에서 과도한 자원 사용을 방지하기 위함입니다.

<a name="unique-jobs"></a>
### 유니크 잡 (Unique Jobs)

> [!WARNING]
> 유니크 잡은 [락(lock)](/docs/12.x/cache#atomic-locks)을 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 아토믹 락을 지원합니다.

> [!WARNING]
> 유니크 잡 제약은 배치(batches) 내 잡에는 적용되지 않습니다.

일부 작업은 동일한 잡이 큐에 동시에 단 하나만 올라가도록 제한하고 싶을 때가 있습니다. 이를 위해 잡 클래스에서 `ShouldBeUnique` 인터페이스를 구현할 수 있습니다. 별도의 추가 메서드 구현은 필요하지 않습니다.

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

위의 예제에서는 `UpdateSearchIndex` 잡이 유니크합니다. 즉, 동일 잡 인스턴스가 큐에 이미 존재하고 아직 처리되지 않았다면, 추가적인 디스패치는 무시됩니다.

직접 지정한 "키(key)"로 유니크 잡을 정의하거나, 유니크 상태가 유지될 최대 시간도 지정할 수 있습니다. 이 경우 `uniqueId`와 `uniqueFor` 속성 또는 메서드를 클래스에 추가하면 됩니다.

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

이 예시에서는 상품 ID로 잡의 유니크성을 판단합니다. 동일한 상품 ID로 잡을 여러 번 디스패치해도, 첫 번째 잡이 처리 완료될 때까지 추가 잡은 무시됩니다. 만약 기존 잡이 1시간 내 처리되지 않으면 유니크 락이 풀리며, 동일 키 값의 잡을 다시 큐에 보낼 수 있습니다.

> [!WARNING]
> 여러 웹 서버나 컨테이너에서 잡을 디스패치하는 경우, 모든 서버가 동일한 중앙 캐시 서버와 통신하도록 해야 유니크 잡 판단이 정확히 동작합니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 잡 처리 시작 전까지 유니크 보장

기본적으로 유니크 잡은 작업 처리 후 또는 모든 재시도 횟수가 끝난 후 "락 해제"됩니다. 잡이 실제로 처리되기 직전에 락을 해제하려면, 잡 클래스에서 `ShouldBeUniqueUntilProcessing` 인터페이스를 대신 구현합니다.

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

내부적으로 `ShouldBeUnique` 잡이 디스패치될 때, Laravel은 `uniqueId` 키로 [락](/docs/12.x/cache#atomic-locks)을 획득합니다. 만약 해당 락이 이미 잡혀 있다면, 잡은 디스패치되지 않습니다. 이 락은 잡이 처리 완료되거나 모든 재시도 시도가 끝나면 해제됩니다. 기본적으로 라라벨은 기본 캐시 드라이버로 락을 잡지만, 별도의 드라이버를 사용하고 싶다면 `uniqueVia` 메서드에서 사용할 캐시 드라이버를 반환하면 됩니다.

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
> 단순히 잡의 동시 실행만 제한하고 싶다면, [WithoutOverlapping](/docs/12.x/queues#preventing-job-overlaps) 잡 미들웨어를 사용하는 것이 더 적합합니다.

<a name="encrypted-jobs"></a>
### 암호화된 잡 (Encrypted Jobs)

Laravel에서는 잡 데이터의 보안과 무결성을 [암호화](/docs/12.x/encryption) 기능을 통해 보장할 수 있습니다. 잡 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하면, 해당 잡은 큐에 오르기 전 자동으로 암호화됩니다.

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

잡 미들웨어는 큐잉 잡 실행을 감싸는 커스텀 로직을 제공하여, 반복되는 코드(보일러플레이트)를 잡 클래스 외부로 분리할 수 있습니다. 예를 들어, 아래 `handle` 메서드는 Redis의 속도 제한 기능을 활용해 5초마다 한 번씩만 잡을 처리하도록 작성된 예시입니다.

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

위 코드는 작동하지만, Redis 속도 제한 로직이 `handle` 메서드를 복잡하게 만듭니다. 이러한 로직이 반복된다면, 잡 미들웨어로 분리하는 것이 더 효율적입니다.

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

이처럼 [라우트 미들웨어](/docs/12.x/middleware)와 마찬가지로, 잡 미들웨어는 처리할 잡과 다음 단계로 진행할 콜백을 인자로 받습니다.

새로운 잡 미들웨어 클래스 생성은 `make:job-middleware` Artisan 명령어를 사용할 수 있습니다. 생성된 미들웨어는 잡의 `middleware` 메서드에서 반환함으로써 적용할 수 있습니다. 이 메서드는 `make:job`으로 생성된 잡에 기본적으로 존재하지 않으니, 수동으로 추가해야 합니다.

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
> 잡 미들웨어는 [큐잉 이벤트 리스너](/docs/12.x/events#queued-event-listeners), [메일러블](/docs/12.x/mail#queueing-mail), [알림](/docs/12.x/notifications#queueing-notifications)에도 적용 가능합니다.

<a name="rate-limiting"></a>
### 속도 제한 (Rate Limiting)

직접 잡 미들웨어로 속도 제한 로직을 구현할 수도 있지만, 라라벨은 자체적으로 사용할 수 있는 속도 제한 미들웨어를 제공합니다. [라우트 속도 제한](/docs/12.x/routing#defining-rate-limiters)와 유사하게, 잡 전용 속도 제한기는 `RateLimiter` 파사드의 `for` 메서드로 정의합니다.

예를 들어, 일반 사용자는 한 시간에 한 번씩만 백업이 가능하지만, 프리미엄 고객은 제한을 두지 않는 규칙을 만들 수 있습니다. 이 경우, `AppServiceProvider`의 `boot` 메서드에서 아래와 같이 정의할 수 있습니다.

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

위에서는 시간 단위 제한을 예시로 들었지만, `perMinute` 메서드로 분 단위 제한도 쉽게 지정할 수 있습니다. `by` 메서드에는 일반적으로 고객별로 제한을 나누기 위해 각 잡의 사용자 ID와 같이 구분자를 전달합니다.

```php
return Limit::perMinute(50)->by($job->user->id);
```

속도 제한 규칙을 정의했으면, 잡에 `Illuminate\Queue\Middleware\RateLimited` 미들웨어를 적용해 사용할 수 있습니다. 제한에 걸린 잡은 적정 시간만큼 큐로 다시 릴리즈됩니다.

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

속도 제한에 걸린 잡이라도 `attempts` 횟수는 계속 증가합니다. 따라서 잡 클래스의 `tries`와 `maxExceptions` 속성, 또는 [retryUntil 메서드](#time-based-attempts)를 적절하게 조절해야 할 수 있습니다.

`releaseAfter` 메서드로 잡이 다시 시도될 때까지 기다릴 시간을 초 단위로 지정할 수 있습니다.

```php
public function middleware(): array
{
    return [(new RateLimited('backups'))->releaseAfter(60)];
}
```

잡이 속도 제한에 걸렸을 때 더 이상 재시도를 원하지 않는다면, `dontRelease` 메서드를 사용할 수 있습니다.

```php
public function middleware(): array
{
    return [(new RateLimited('backups'))->dontRelease()];
}
```

> [!NOTE]
> Redis를 사용할 경우 `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어를 사용할 수 있습니다. 이 미들웨어는 Redis에 최적화되어 더욱 효율적으로 동작합니다.

<a name="preventing-job-overlaps"></a>
### 잡 중첩 방지

Laravel에는 임의의 키를 기반으로 잡 중첩(동시에 두 번 이상 실행)되는 것을 방지하는 `Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어가 내장되어 있습니다. 예를 들어, 동일한 사용자 ID로 신용 점수를 업데이트하는 잡이 겹치지 않도록 하려면 아래와 같이 미들웨어를 적용하면 됩니다.

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

중첩된 잡이 큐로 다시 릴리즈되어도 시도 횟수는 증가합니다. 만약 겹치는 잡을 재시도하지 않으려면 `tries` 속성을 1로 두면 됩니다.

`releaseAfter` 메서드로 릴리즈 후 몇 초 후에 다시 시도할지 지정할 수 있습니다.

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->releaseAfter(60)];
}
```

즉시 중첩된 잡을 삭제하고 싶다면 `dontRelease` 메서드를 사용합니다.

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->dontRelease()];
}
```

이 미들웨어는 Laravel의 아토믹 락 기능을 기반으로 동작합니다. 만약 잡이 예기치 않게 실패하거나 타임아웃되는 등으로 락이 해제되지 않을 수 있으므로, `expireAfter` 메서드로 락 만료 시간을 명시할 수 있습니다.

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->expireAfter(180)];
}
```

> [!WARNING]
> `WithoutOverlapping` 미들웨어는 [락(lock)](/docs/12.x/cache#atomic-locks)을 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 지원합니다.

<a name="sharing-lock-keys"></a>
#### 여러 잡 클래스 간 락 키 공유

기본적으로, `WithoutOverlapping` 미들웨어는 같은 클래스 잡끼리만 중첩 방지를 제공합니다. 서로 다른 잡 클래스가 동일한 락 키를 쓰더라도 중첩 방지는 적용되지 않습니다. 잡 클래스 간에도 키를 공유해서 중첩 방지하려면 `shared` 메서드를 사용하면 됩니다.

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

Laravel에는 일정 횟수의 예외가 발생한 후 잡 실행을 지연시키는 `Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어가 있습니다. 이는 주로 외부 API 등 불안정한 서드 파티 서비스와 연동되는 잡에서 유용합니다.

아래는 10번 연속 예외 발생 시 5분간 잡 처리를 지연하는 예시이며, 잡 클래스에 [시간 기반 시도 제한](#time-based-attempts)을 함께 적용하는 것이 일반적입니다.

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

미들웨어의 첫 번째 생성자 인자는 예외 허용 횟수이며, 두 번째는 제한이 걸렸을 때 다시 시도할 간격(초)입니다. 잡이 예외를 발생시켜도 아직 한계치에 도달하지 않았다면, 즉시 재시도됩니다. 이 때, `backoff` 메서드로 일정 시간 후 재시도할 수도 있습니다.

```php
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 5 * 60))->backoff(5)];
}
```

이 미들웨어는 잡 클래스명을 캐시 "키"로 활용합니다. 여러 잡이 동일한 서드파티 서비스를 사용한다면, `by` 메서드로 키를 공유하여 동일한 예외 제한을 적용할 수 있습니다.

```php
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->by('key')];
}
```

기본적으로 모든 예외를 제한하지만, `when` 메서드에 클로저를 전달하여 특정 예외만 제한하도록 변경할 수 있습니다.

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

특정 예외 발생 시 잡을 아예 삭제하려면, `deleteWhen` 메서드를 사용할 수 있습니다.

```php
use App\Exceptions\CustomerDeletedException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [(new ThrottlesExceptions(2, 10 * 60))->deleteWhen(CustomerDeletedException::class)];
}
```

예외 자체를 앱의 익셉션 핸들러에 리포트하려면, `report` 메서드를 호출합니다. 클로저를 전달하여 조건부로 리포트할 수도 있습니다.

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
> Redis를 사용할 경우 `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어를 사용할 수 있습니다.

<a name="skipping-jobs"></a>
### 잡 건너뛰기 (Skipping Jobs)

`Skip` 미들웨어는 잡 로직을 변경하지 않고도, 잡을 스킵(삭제)하고 싶을 때 사용할 수 있습니다. `Skip::when`은 조건이 참이면, `Skip::unless`는 조건이 거짓이면 잡을 삭제합니다.

```php
use Illuminate\Queue\Middleware\Skip;

public function middleware(): array
{
    return [
        Skip::when($condition),
    ];
}
```

더 복잡한 조건식을 위해서는 클로저를 전달할 수 있습니다.

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

[a name="dispatching-jobs"></a>
## 잡 디스패치 (Dispatching Jobs)

잡 클래스를 작성한 뒤에는, 해당 잡 클래스의 `dispatch` 메서드를 사용해 잡을 큐에 넣을 수 있습니다. `dispatch`에 전달된 인수들은 잡 생성자에 그대로 전달됩니다.

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

조건부로 잡을 디스패치하고 싶다면, `dispatchIf`, `dispatchUnless` 메서드를 사용할 수 있습니다.

```php
ProcessPodcast::dispatchIf($accountActive, $podcast);

ProcessPodcast::dispatchUnless($accountSuspended, $podcast);
```

Laravel 최신 버전에서는 `database` 커넥션이 기본 큐로 설정되어 있습니다. 별도의 기본 큐 커넥션을 사용하고 싶다면 애플리케이션의 `.env` 파일 내 `QUEUE_CONNECTION` 값을 변경하면 됩니다.

<a name="delayed-dispatching"></a>
### 지연 디스패치 (Delayed Dispatching)

잡을 즉시 처리하지 않고 일정 시간 이후에 실행되도록 하고 싶다면, `delay` 메서드를 사용할 수 있습니다. 예를 들어 10분 후에 처리하려면 다음과 같이 작성합니다.

```php
ProcessPodcast::dispatch($podcast)->delay(now()->addMinutes(10));
```

기본 지연 시간이 설정된 잡에서, 즉시 처리하고 싶을 때는 `withoutDelay` 메서드를 사용할 수 있습니다.

```php
ProcessPodcast::dispatch($podcast)->withoutDelay();
```

> [!WARNING]
> Amazon SQS 큐 서비스는 최대 15분(900초)까지 지연만 지원합니다.

<a name="synchronous-dispatching"></a>
### 동기 디스패치 (Synchronous Dispatching)

잡을 큐에 올리지 않고 즉시(동기적으로) 실행하고 싶다면, `dispatchSync` 메서드를 사용할 수 있습니다. 이 방식은 잡을 큐에 쌓지 않고, 현재 프로세스에서 바로 실행합니다.

```php
ProcessPodcast::dispatchSync($podcast);
```

<a name="deferred-dispatching"></a>
#### 연기된 동기 디스패치

연기된 동기 디스패치를 사용하면, HTTP 응답이 사용자에게 전송된 후 현재 프로세스에서 잡을 처리할 수 있습니다. 이는 "큐" 잡을 동기적으로 처리하면서도 사용자의 요청 처리를 지연시키지 않습니다. 동기 잡을 연기하려면 `deferred` 커넥션에 디스패치합니다.

```php
RecordDelivery::dispatch($order)->onConnection('deferred');
```

`deferred` 커넥션은 [기본 페일오버 큐](#queue-failover) 역할도 합니다.

`background` 커넥션은 HTTP 응답 이후 별도의 PHP 프로세스를 생성해 잡을 실행하므로, PHP-FPM이나 애플리케이션 워커가 다음 HTTP 요청 처리를 바로 이어갈 수 있습니다.

```php
RecordDelivery::dispatch($order)->onConnection('background');
```

<a name="jobs-and-database-transactions"></a>
### 잡과 데이터베이스 트랜잭션 (Jobs & Database Transactions)

데이터베이스 트랜잭션 내에서 잡을 디스패치하는 것은 문제없지만, 작업이 실제로 성공적으로 실행될 수 있는지 신경 써야 합니다. 트랜잭션 안에서 잡을 디스패치할 때, 잡이 트랜잭션 커밋 전에 워커에 의해 먼저 처리되는 상황이 발생할 수 있습니다. 이때 트랜잭션 내에서 수정한 모델이나 DB 기록이 아직 DB에 반영되지 않아 문제를 야기할 수 있습니다.

이 문제를 해결하기 위해, 큐 커넥션 설정 배열 내 `after_commit` 옵션을 활용할 수 있습니다.

```php
'redis' => [
    'driver' => 'redis',
    // ...
    'after_commit' => true,
],
```

이 옵션을 `true`로 두면, 트랜잭션 내에서 잡을 디스패치해도 부모 트랜잭션이 커밋된 이후에만 실제 잡이 디스패치됩니다. 트랜잭션이 없으면 즉시 디스패치됩니다.

만약 트랜잭션 도중 예외가 발생해 롤백된다면, 그 안에서 디스패치된 잡은 취소되어 큐에 오르지 않습니다.

> [!NOTE]
> `after_commit`을 `true`로 설정하면, 큐잉 이벤트 리스너, 메일러블, 알림, 브로드캐스트 이벤트 역시 모든 열린 DB 트랜잭션이 커밋된 뒤에 디스패치됩니다.

<a name="specifying-commit-dispatch-behavior-inline"></a>
#### 잡별 커밋 디스패치 동작 지정

큐 커넥션 설정에 `after_commit`을 사용하지 않는 경우, 특정 잡만 트랜잭션 커밋 후에 디스패치되도록 하려면, `dispatch` 체인에 `afterCommit`을 추가할 수 있습니다.

```php
ProcessPodcast::dispatch($podcast)->afterCommit();
```

반대로, `after_commit`이 설정되어 있을 때 특정 잡만 즉시 디스패치하려면 `beforeCommit`을 사용합니다.

```php
ProcessPodcast::dispatch($podcast)->beforeCommit();
```

(이후 내용도 같은 방식으로 번역 계속)