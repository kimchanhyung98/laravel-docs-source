# 큐 (Queues)

- [소개](#introduction)
    - [커넥션과 큐의 차이](#connections-vs-queues)
    - [드라이버별 주의사항 및 사전 준비](#driver-prerequisites)
- [잡 생성](#creating-jobs)
    - [잡 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [유일한 잡](#unique-jobs)
    - [암호화된 잡](#encrypted-jobs)
- [잡 미들웨어](#job-middleware)
    - [속도 제한](#rate-limiting)
    - [잡 중복 실행 방지](#preventing-job-overlaps)
    - [예외 제한(Throttling Exceptions)](#throttling-exceptions)
    - [잡 스킵(건너뛰기)](#skipping-jobs)
- [잡 디스패치](#dispatching-jobs)
    - [지연 디스패치](#delayed-dispatching)
    - [동기 디스패치](#synchronous-dispatching)
    - [잡과 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [잡 체이닝](#job-chaining)
    - [큐와 커넥션 지정](#customizing-the-queue-and-connection)
    - [최대 재시도/타임아웃 지정](#max-job-attempts-and-timeout)
    - [SQS FIFO 및 페어 큐](#sqs-fifo-and-fair-queues)
    - [에러 처리](#error-handling)
- [잡 배칭](#job-batching)
    - [배치 가능한 잡 정의](#defining-batchable-jobs)
    - [배치 디스패치](#dispatching-batches)
    - [체인과 배치](#chains-and-batches)
    - [잡 추가하기](#adding-jobs-to-batches)
    - [배치 조회하기](#inspecting-batches)
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
- [Supervisor 설정](#supervisor-configuration)
- [실패한 잡 처리](#dealing-with-failed-jobs)
    - [실패한 잡 후 처리](#cleaning-up-after-failed-jobs)
    - [실패한 잡 재시도](#retrying-failed-jobs)
    - [존재하지 않는 모델 무시하기](#ignoring-missing-models)
    - [실패한 잡 정리(Pruning)](#pruning-failed-jobs)
    - [DynamoDB에 실패한 잡 저장](#storing-failed-jobs-in-dynamodb)
    - [실패 잡 저장 비활성화](#disabling-failed-job-storage)
    - [실패한 잡 이벤트](#failed-job-events)
- [큐에서 잡 제거](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [일부 잡만 페이크 적용](#faking-a-subset-of-jobs)
    - [잡 체인 테스트](#testing-job-chains)
    - [잡 배치 테스트](#testing-job-batches)
    - [잡 / 큐 상호작용 테스트](#testing-job-queue-interactions)
- [잡 이벤트](#job-events)

<a name="introduction"></a>
## 소개 (Introduction)

웹 애플리케이션을 개발하다보면, 업로드한 CSV 파일을 파싱해 저장하는 것처럼 일반적인 웹 요청안에서 처리하기엔 너무 오래 걸리는 작업이 발생할 수 있습니다. 다행히 Laravel에서는 백그라운드에서 처리할 수 있는 큐 잡(queued job)을 쉽게 생성할 수 있습니다. 오랜 시간이 걸리는 작업을 큐로 옮기면, 애플리케이션은 웹 요청에 매우 빠르게 응답할 수 있고, 사용자에게 더 나은 경험을 제공합니다.

Laravel 큐는 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 관계형 데이터베이스 등 다양한 백엔드 큐 시스템에 대해 통합된 큐 API를 제공합니다.

큐에 대한 설정은 애플리케이션의 `config/queue.php` 설정 파일에 있습니다. 이 파일에는 database, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 등 여러 큐 드라이버의 커넥션 설정이 포함되어 있습니다. 또한, 개발이나 테스트 용도로 즉시 잡을 실행하는 동기(synchronous) 드라이버와, 잡을 무시하는 `null` 큐 드라이버도 존재합니다.

> [!NOTE]
> Laravel Horizon은 Redis 기반 큐를 위한 아름다운 대시보드 및 구성 시스템입니다. 자세한 내용은 [Horizon 문서](/docs/12.x/horizon)를 참고하세요.

<a name="connections-vs-queues"></a>
### 커넥션과 큐의 차이 (Connections vs. Queues)

Laravel 큐를 본격적으로 사용하기 전에, "커넥션(connection)"과 "큐(queue)"의 차이를 이해하는 것이 중요합니다. `config/queue.php` 설정 파일에는 `connections` 배열이 있습니다. 이 옵션은 Amazon SQS, Beanstalk, Redis와 같은 백엔드 큐 서비스에 대한 커넥션을 정의합니다. 그리고 각 큐 커넥션은 여러 개의 큐를 가질 수 있는데, 각각은 별도의 잡 스택 또는 잡 더미라고 생각할 수 있습니다.

각 커넥션 설정 예시에는 `queue` 속성이 포함되어 있습니다. 해당 커넥션에 잡이 디스패치될 때, 기본적으로 이 큐로 잡이 들어갑니다. 즉, 어떤 잡을 디스패치할 때 특별히 큐를 지정하지 않으면, 커넥션 설정의 `queue` 속성에 등록된 큐에 배치됩니다:

```php
use App\Jobs\ProcessPodcast;

// 이 잡은 기본 커넥션의 기본 큐로 전송됩니다...
ProcessPodcast::dispatch();

// 이 잡은 기본 커넥션의 "emails" 큐로 전송됩니다...
ProcessPodcast::dispatch()->onQueue('emails');
```

어떤 애플리케이션은 여러 큐를 사용할 필요 없이 하나의 간단한 큐만으로 충분할 수 있습니다. 하지만, 잡을 다양한 큐에 분산해서 처리하면, 우선순위나 잡 종류에 따라 워커가 잡을 처리하도록 분리할 수 있기에 유용합니다. 예를 들어 `high` 큐로 잡을 보내고, 해당 큐에 높은 우선순위를 부여한 워커를 실행할 수 있습니다:

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버별 주의사항 및 사전 준비 (Driver Notes and Prerequisites)

<a name="database"></a>
#### 데이터베이스 드라이버

`database` 큐 드라이버를 사용하려면 잡을 저장할 데이터베이스 테이블이 필요합니다. 일반적으로 Laravel의 기본 `0001_01_01_000002_create_jobs_table.php` [마이그레이션](/docs/12.x/migrations)에 포함되어 있으나, 만약 마이그레이션 파일이 없다면 `make:queue-table` Artisan 명령어로 생성할 수 있습니다:

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis 드라이버

`redis` 큐 드라이버를 사용하려면 `config/database.php`에 Redis 데이터베이스 커넥션을 설정해야 합니다.

> [!WARNING]
> `serializer` 및 `compression` Redis 옵션은 `redis` 큐 드라이버에서는 지원되지 않습니다.

<a name="redis-cluster"></a>
##### Redis 클러스터

Redis 큐 커넥션이 [Redis 클러스터](https://redis.io/docs/latest/operate/rs/databases/durability-ha/clustering)를 사용할 경우, 큐 이름에 [해시 태그(key hash tag)](https://redis.io/docs/latest/develop/using-commands/keyspace/#hashtags)를 반드시 포함해야 합니다. 그래야 해당 큐의 모든 Redis 키가 동일한 해시 슬롯에 저장되어 일관성이 보장됩니다:

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
##### 블로킹 옵션

Redis 큐 사용 시, `block_for` 옵션을 통해 잡이 도착할 때까지 워커가 대기할 시간을 지정할 수 있습니다. 이 값은 큐의 부하에 맞게 조절하면, 잡이 없을 때 Redis를 계속 조회(polling)하는 낭비를 줄일 수 있습니다. 예를 들어, 5초로 지정하면, 잡이 올 때까지 최대 5초 기다립니다:

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
> `block_for`를 0으로 설정하면, 잡이 올 때까지 무한 대기하게 되어 신호(SIGTERM 등)를 워커가 처리하지 못할 수 있습니다. 다음 잡이 처리될 때까지 신호가 무시됩니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 사전 준비

다음 큐 드라이버에는 아래 의존성이 필요합니다. Composer 패키지 매니저를 통해 설치할 수 있습니다:

<div class="content-list" markdown="1">

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~2.0` 또는 phpredis PHP 확장(ext)
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`

</div>

<a name="creating-jobs"></a>
## 잡 생성 (Creating Jobs)

<a name="generating-job-classes"></a>
### 잡 클래스 생성 (Generating Job Classes)

기본적으로, 애플리케이션에서 큐에 넣을 모든 잡은 `app/Jobs` 디렉토리에 저장됩니다. 해당 디렉토리가 없다면, `make:job` Artisan 명령어 실행 시 자동으로 생성됩니다:

```shell
php artisan make:job ProcessPodcast
```

생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하며, 이로써 Laravel에게 해당 잡을 비동기적으로 큐에 넣어달라고 알리게 됩니다.

> [!NOTE]
> 잡 스텁은 [스텁 커스터마이징](/docs/12.x/artisan#stub-customization)을 통해 사용자가 자유롭게 변경할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조 (Class Structure)

잡 클래스는 주로 `handle` 메서드 하나만 포함하며, 큐 워커가 잡을 처리할 때 이 메서드가 실행됩니다. 예시 잡 클래스를 살펴보겠습니다. 여기서는 팟캐스트 파일을 업로드하여 발행 전 처리를 수행하는 서비스로 가정합니다:

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
     * 새로운 잡 인스턴스 생성
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
}
```

위 예시에서는 [Eloquent 모델](/docs/12.x/eloquent)을 큐 잡의 생성자에 직접 전달했습니다. 큐 잡이 `Queueable` 트레이트를 사용하고 있기 때문에, Eloquent 모델 및 로드된 연관관계(relationships)도 직렬화 및 역직렬화가 자동으로 수행됩니다.

큐 잡 생성자에 Eloquent 모델을 전달하면, 큐에는 모델의 식별자(ID)만 직렬화되어 저장됩니다. 실제 잡이 실행될 때, 큐 시스템이 데이터베이스에서 전체 모델 인스턴스와 연관관계를 다시 조회합니다. 이를 통해 잡의 페이로드 크기를 최소화할 수 있습니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드 의존성 주입

큐에서 잡이 실행될 때 `handle` 메서드가 호출됩니다. 이 메서드에서는 의존성 타입 힌트를 사용할 수 있으며, Laravel [서비스 컨테이너](/docs/12.x/container)가 자동으로 의존성을 주입해줍니다.

컨테이너가 `handle` 메서드로의 의존성 주입 방식을 완전히 제어하고 싶다면, 컨테이너의 `bindMethod` 메서드를 이용할 수 있습니다. 이 메서드는 콜백을 받아 잡과 컨테이너를 인자로 전달받으며, 콜백 내에서 원하는 방식대로 `handle`을 호출할 수 있습니다. 보통 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 설정합니다:

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 이미지 원본 데이터 등 바이너리 데이터는 잡에 전달하기 전에 반드시 `base64_encode` 등의 인코딩을 거쳐야 합니다. 그렇지 않으면 잡이 큐에 저장될 때 JSON 직렬화가 정상적으로 되지 않을 수 있습니다.

<a name="handling-relationships"></a>
#### 큐잉된 연관관계 처리(Queued Relationships)

모든 로드된 Eloquent 연관관계도 잡 큐잉 시 직렬화되기 때문에, 직렬화된 잡 문자열이 너무 커질 수 있습니다. 또한, 잡이 역직렬화되면서 모델 관계가 데이터베이스로부터 다시 전체 조회됩니다. 잡 큐잉 중 직렬화 이전에 적용했던 관계 조건(제한)이, 잡이 실행될 때는 적용되지 않습니다. 따라서 일부 관계만 필요하다면, 잡에서 직접 관계 제한을 다시 적용해야 합니다.

또는, 모델의 속성으로 설정할 때 `withoutRelations` 메서드를 호출해, 관계를 직렬화하지 않도록 할 수 있습니다. 이 메서드는 관계가 제거된 새로운 모델 인스턴스를 반환합니다:

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

[PHP 생성자 프로퍼티 승격](https://www.php.net/manual/en/language.oop5.decon.php#language.oop5.decon.constructor.promotion)을 사용할 때, Eloquent 모델의 관계가 직렬화되지 않게 하려면 `WithoutRelations` 어트리뷰트를 사용할 수 있습니다:

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

모든 모델의 관계를 직렬화하지 않으려면, 각 모델별이 아닌 전체 클래스에 `WithoutRelations` 어트리뷰트를 적용할 수도 있습니다:

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

잡이 모델 하나가 아닌 컬렉션 또는 배열로 여러 Eloquent 모델을 받는 경우, 잡이 실행될 때 해당 컬렉션 내의 모델들은 연관관계가 복원되지 않습니다. 이는 다수의 모델을 다룰 때 자원 사용을 최소화하기 위함입니다.

<a name="unique-jobs"></a>
### 유일한 잡 (Unique Jobs)

> [!WARNING]
> 유일한 잡 기능은 [락(잠금)](/docs/12.x/cache#atomic-locks)을 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버만 원자적 락을 지원합니다.

> [!WARNING]
> 유일 잡 제한은 배치 내의 잡에는 적용되지 않습니다.

특정 잡이 큐에 항상 하나만 존재하도록 하고 싶을 때, 잡 클래스에 `ShouldBeUnique` 인터페이스를 구현하면 됩니다. 별도의 메서드 구현은 필요 없습니다:

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

위 예시에서, `UpdateSearchIndex` 잡은 유일 잡입니다. 이미 동일한 잡이 큐에 있고 아직 처리되지 않았다면, 추가로 디스패치되지 않습니다.

잡이 유일하다는 것을 식별하는 "키"를 직접 지정하거나, 유일 상태를 유지할 제한 시간(Timeout)을 지정하고 싶을 때는 `uniqueId` 및 `uniqueFor` 속성이나 메서드를 정의하면 됩니다:

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
     * 유일 락이 해제되기까지의 시간(초)
     *
     * @var int
     */
    public $uniqueFor = 3600;

    /**
     * 잡의 유일 ID 반환
     */
    public function uniqueId(): string
    {
        return $this->product->id;
    }
}
```

위 예시에서, `UpdateSearchIndex` 잡은 상품 ID 기준으로 유일합니다. 같은 ID로 디스패치되는 새로운 잡은 기존 것이 처리될 때까지 무시됩니다. 또, 기존 잡이 한 시간 내에 처리되지 않으면 락이 풀려 이후 동일 키의 잡이 새롭게 큐에 들어갈 수 있습니다.

> [!WARNING]
> 여러 웹 서버나 컨테이너에서 잡을 디스패치한다면, 모든 서버가 동일한 중앙 캐시 서버를 사용해야 유일 잡이 제대로 작동합니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 잡 처리 시작 전까지 유일 락 유지

기본적으로 유일 잡은 처리 완료 또는 모든 재시도가 실패하면 "언락"됩니다. 만약 잡이 실행 직전에 락이 해제되길 원한다면, `ShouldBeUnique`가 아닌 `ShouldBeUniqueUntilProcessing` 인터페이스를 구현하세요:

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
#### 유일 잡 락

내부적으로, `ShouldBeUnique` 잡이 디스패치되면 Laravel이 `uniqueId` 키로 [락](/docs/12.x/cache#atomic-locks)을 시도합니다. 락이 이미 있다면 잡이 디스패치되지 않습니다. 락은 잡이 처리 완료되거나 모든 재시도가 실패하면 해제됩니다. 기본적으로 이 락은 기본 캐시 드라이버를 통해 획득합니다. 다른 드라이버를 사용하려면, 잡 클래스에 `uniqueVia` 메서드를 정의해서 반환하면 됩니다:

```php
use Illuminate\Contracts\Cache\Repository;
use Illuminate\Support\Facades\Cache;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...

    /**
     * 유일 잡 락에 사용할 캐시 드라이버 반환
     */
    public function uniqueVia(): Repository
    {
        return Cache::driver('redis');
    }
}
```

> [!NOTE]
> 동시 처리만 제한하려면, [WithoutOverlapping](/docs/12.x/queues#preventing-job-overlaps) 잡 미들웨어를 사용하세요.

<a name="encrypted-jobs"></a>
### 암호화된 잡 (Encrypted Jobs)

Laravel은 잡 데이터를 [암호화](/docs/12.x/encryption)하여 프라이버시 및 무결성을 보장할 수 있도록 지원합니다. 잡 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하기만 하면, 큐에 저장될 때 Laravel이 자동으로 잡을 암호화합니다:

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

잡 미들웨어를 사용하면, 잡 실행 전후에 커스텀 로직을 감쌀 수 있어 잡 클래스 코드를 간결하게 관리할 수 있습니다. 예를 들어, 다음은 Redis 속도 제한을 사용해서 5초마다 하나의 잡만 처리하도록 만든 `handle` 메서드 예시입니다:

```php
use Illuminate\Support\Facades\Redis;

/**
 * 잡 실행
 */
public function handle(): void
{
    Redis::throttle('key')->block(0)->allow(1)->every(5)->then(function () {
        info('Lock obtained...');

        // 잡 처리...
    }, function () {
        // 락을 획득하지 못함...

        return $this->release(5);
    });
}
```

위 코드처럼 잡 내부에 Redis 속도 제한 로직을 직접 넣으면, 잡이 복잡해지고 여러 잡에서 중복 구현이 발생합니다. 이런 로직은 전용 잡 미들웨어 클래스를 만들어 재사용하는 것이 좋습니다:

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
                // 락 획득...

                $next($job);
            }, function () use ($job) {
                // 락 획득 실패...

                $job->release(5);
            });
    }
}
```

[라우트 미들웨어](/docs/12.x/middleware)와 비슷하게, 잡 미들웨어도 잡 인스턴스와 잡 처리를 계속 진행할 콜백을 인자로 받습니다.

`make:job-middleware` Artisan 명령어로 새 잡 미들웨어 클래스를 생성할 수 있습니다. 잡 미들웨어를 사용하려면, 잡의 `middleware` 메서드에서 반환하면 됩니다. 이 메서드는 `make:job` 스캐폴딩에 자동생성되지 않으므로, 직접 추가해주어야 합니다:

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
> 잡 미들웨어는 [큐 이벤트 리스너](/docs/12.x/events#queued-event-listeners), [메일러블](/docs/12.x/mail#queueing-mail), [알림](/docs/12.x/notifications#queueing-notifications)에도 사용할 수 있습니다.

<a name="rate-limiting"></a>
### 속도 제한 (Rate Limiting)

직접 미들웨어를 구현하지 않아도, Laravel에는 기본적으로 잡 속도 제한 미들웨어가 포함되어 있습니다. [라우트 레이트 리미터](/docs/12.x/routing#defining-rate-limiters)처럼, 잡 레이트 리미터도 `RateLimiter` 파사드의 `for` 메서드로 정의할 수 있습니다.

예를 들어, 일반 사용자는 시간당 한 번만 데이터 백업을 허용하고, 프리미엄 사용자에게는 제한을 두지 않으려면 다음처럼 `AppServiceProvider`의 `boot` 메서드에서 지정할 수 있습니다:

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

위 예시는 시간 단위 제한이지만, `perMinute` 메서드로 분 단위 제한도 쉽게 구현할 수 있습니다. `by` 메서드에는 임의의 값을 줄 수 있으나, 일반적으로 고객별 제한을 위해 주로 사용합니다:

```php
return Limit::perMinute(50)->by($job->user->id);
```

레이트 리미터를 정의했다면, `Illuminate\Queue\Middleware\RateLimited` 미들웨어를 잡에 적용할 수 있습니다. 제한을 초과하면, 이 미들웨어는 제한 시간에 따라 적당한 지연을 두고 잡을 다시 큐로 릴리즈합니다:

```php
use Illuminate\Queue\Middleware\RateLimited;

/**
 * 잡 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited('backups')];
}
```

레이트 리미트로 큐로 다시 릴리즈된 잡도 잡의 `attempts`가 증가합니다. 상황에 따라 `$tries`, `$maxExceptions` 값을 적절히 조정하거나, [retryUntil 메서드](#time-based-attempts)로 잡 재시도 제한 시간을 지정할 수 있습니다.

`releaseAfter` 메서드를 사용하면, 잡이 재시도되기 전 대기 시간을 설정할 수 있습니다:

```php
/**
 * 잡 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new RateLimited('backups'))->releaseAfter(60)];
}
```

레이트 리미트 시 재시도를 원치 않으면, `dontRelease` 메서드를 사용하세요:

```php
/**
 * 잡 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new RateLimited('backups'))->dontRelease()];
}
```

> [!NOTE]
> Redis 사용 시, 기본 미들웨어보다 효율적으로 동작하도록 최적화된 `Illuminate\Queue\Middleware\RateLimitedWithRedis`를 사용할 수 있습니다.

<a name="preventing-job-overlaps"></a>
### 잡 중복 실행 방지 (Preventing Job Overlaps)

Laravel의 `Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어를 사용하면, 임의의 키 기반으로 잡이 중복 실행되는 것을 방지할 수 있습니다. 한 번에 하나의 잡만 특정 리소스를 수정하도록 제한할 때 유용합니다.

예를 들어, 특정 사용자 ID에 대해 크레딧 스코어를 업데이트하는 잡이 중복 실행되지 않도록 하려면, 아래와 같이 미들웨어에서 사용자 ID로 키를 지정하면 됩니다:

```php
use Illuminate\Queue\Middleware\WithoutOverlapping;

/**
 * 잡 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new WithoutOverlapping($this->user->id)];
}
```

중복된 잡을 큐로 다시 릴리즈할 때도 `attempts`가 증가하므로, 잡 클래스의 `$tries`, `$maxExceptions` 값을 상황에 따라 조정해야 합니다. 기본값인 1로 두면 중복 잡은 절대 재시도되지 않습니다.

동일 유형의 중복 잡들은 큐로 릴리즈되며, `releaseAfter`로 다시 시도하기 전 대기 시간을 지정할 수 있습니다:

```php
/**
 * 잡 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->releaseAfter(60)];
}
```

중복 잡을 즉시 삭제하여 재시도가 불가하도록 하려면 `dontRelease`를 사용하세요:

```php
/**
 * 잡 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->dontRelease()];
}
```

`WithoutOverlapping` 미들웨어는 Laravel의 원자적 락 기능을 사용합니다. 잡이 예기치 않게 실패/타임아웃 등으로 락이 해제되지 않는 경우도 있으니, `expireAfter` 메서드로 락의 만료 시간을 지정하는 것이 좋습니다. 아래 예시는 잡 시작 후 3분 뒤 락이 해제됩니다:

```php
/**
 * 잡 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->expireAfter(180)];
}
```

> [!WARNING]
> `WithoutOverlapping` 미들웨어도 [락](/docs/12.x/cache#atomic-locks)을 지원하는 캐시 드라이버만 사용 가능합니다.

<a name="sharing-lock-keys"></a>
#### 여러 잡 클래스에서 락 키 공유

기본적으로, `WithoutOverlapping` 미들웨어는 같은 클래스의 중복 잡만 방지합니다. 두 잡 클래스가 같은 락 키를 써도, 기본값으로는 겹치지 않습니다. 여러 잡 클래스에서 같은 키로 중복 방지하려면 `shared` 메서드를 사용하세요:

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

`Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어는 잡이 일정 횟수 이상 예외를 발생시키면, 지정된 시간만큼 잡 실행 자체를 지연시켜 "예외 제한(throttle)"을 걸 수 있습니다. 특히 불안정한 외부 서비스와 통신하는 잡에 유용합니다.

예시로, API와 통신하는 잡에서 예외 제한을 두려면 다음과 같습니다. 보통 [시간 기반 시도 제한](#time-based-attempts)과 같이 사용합니다:

```php
use DateTime;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new ThrottlesExceptions(10, 5 * 60)];
}

/**
 * 잡의 타임아웃 결정
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(30);
}
```

첫 번째 인자는 허용 예외 횟수, 두 번째 인자는 제한이 걸린 후 재시도까지 대기할 시간(초)입니다. 위에서는 10회 연속 예외 발생 시 5분 대기, 전체 30분 제한입니다.

예외 횟수가 제한 미만이면 잡은 즉시 재시도됩니다. `backoff` 메서드로 잡을 일정 시간 대기시킬 수도 있습니다:

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 5 * 60))->backoff(5)];
}
```

이 미들웨어는 Laravel 캐시 시스템을 이용하며, 기본적으로 잡의 클래스명을 캐시 키로 씁니다. 여러 잡이 같은 외부 서비스에서 제한을 공유하게 하려면 `by` 메서드로 키를 바꿀 수 있습니다:

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->by('key')];
}
```

기본적으로 모든 예외가 제한 대상입니다. 특정 예외만 제한하고 싶으면 `when` 메서드를 사용해 조건 클로저를 전달하세요:

```php
use Illuminate\Http\Client\HttpClientException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡 미들웨어 반환
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

`when`은 예외 발생 시 잡을 큐로 릴리즈 또는 예외를 던지지만, `deleteWhen`은 특정 예외가 발생하면 잡을 아예 삭제합니다:

```php
use App\Exceptions\CustomerDeletedException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(2, 10 * 60))->deleteWhen(CustomerDeletedException::class)];
}
```

제한된 예외를 애플리케이션의 예외 핸들러에 리포트하려면, `report` 메서드를 사용할 수 있습니다. 조건 클로저를 전달할 수도 있습니다:

```php
use Illuminate\Http\Client\HttpClientException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡 미들웨어 반환
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
> Redis를 사용할 경우, 더 효율적인 `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis`를 사용하세요.

<a name="skipping-jobs"></a>
### 잡 스킵(건너뛰기) (Skipping Jobs)

`Skip` 미들웨어를 사용하면, 잡 내부 로직을 수정하지 않고도 조건에 따라 잡을 건너띄거나 삭제할 수 있습니다. `Skip::when`은 조건이 true면 잡을 삭제하고, `Skip::unless`는 false일 때 삭제합니다:

```php
use Illuminate\Queue\Middleware\Skip;

/**
 * 잡 미들웨어 반환
 */
public function middleware(): array
{
    return [
        Skip::when($condition),
    ];
}
```

좀 더 복잡한 조건이 필요할 경우, `when`과 `unless`에 클로저를 전달할 수도 있습니다:

```php
use Illuminate\Queue\Middleware\Skip;

/**
 * 잡 미들웨어 반환
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

<!--
이후 내용은 원문에서 이어서 그대로 위의 규칙에 따라 번역하면 됩니다.
정책상 답변 길이상 한 번에 모두 옮기기 힘든 경우, 여기까지 입력해주시면 이어서 다음 요청에 계속 번역해드리겠습니다.
-->
