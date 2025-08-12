# 큐(Queues)

- [소개](#introduction)
    - [커넥션과 큐의 차이](#connections-vs-queues)
    - [드라이버별 참고사항 및 선행 조건](#driver-prerequisites)
- [작업(Job) 생성](#creating-jobs)
    - [작업 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [고유 작업(Unique Jobs)](#unique-jobs)
    - [암호화된 작업(Encrypted Jobs)](#encrypted-jobs)
- [작업 미들웨어](#job-middleware)
    - [속도 제한(Rate Limiting)](#rate-limiting)
    - [작업 중복 방지](#preventing-job-overlaps)
    - [예외 스로틀링(Throttling Exceptions)](#throttling-exceptions)
    - [작업 건너뛰기(Skipping Jobs)](#skipping-jobs)
- [작업 디스패치(Dispatching Jobs)](#dispatching-jobs)
    - [지연 디스패치](#delayed-dispatching)
    - [동기식 디스패치](#synchronous-dispatching)
    - [작업과 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [작업 체이닝](#job-chaining)
    - [큐와 커넥션 커스터마이징](#customizing-the-queue-and-connection)
    - [최대 시도 횟수 및 타임아웃 값 지정](#max-job-attempts-and-timeout)
    - [에러 핸들링](#error-handling)
- [작업 배치(Job Batching)](#job-batching)
    - [배치 가능한 작업 정의](#defining-batchable-jobs)
    - [배치 디스패치](#dispatching-batches)
    - [체인과 배치](#chains-and-batches)
    - [배치에 작업 추가](#adding-jobs-to-batches)
    - [배치 조회](#inspecting-batches)
    - [배치 취소](#cancelling-batches)
    - [배치 실패](#batch-failures)
    - [배치 레코드 정리](#pruning-batches)
    - [DynamoDB에 배치 저장](#storing-batches-in-dynamodb)
- [클로저를 큐에 넣기](#queueing-closures)
- [큐 워커 실행](#running-the-queue-worker)
    - [`queue:work` 명령어](#the-queue-work-command)
    - [큐 우선순위](#queue-priorities)
    - [큐 워커와 배포](#queue-workers-and-deployment)
    - [작업 만료 및 타임아웃](#job-expirations-and-timeouts)
- [Supervisor 설정](#supervisor-configuration)
- [실패한 작업 처리](#dealing-with-failed-jobs)
    - [실패한 작업 후 정리 작업](#cleaning-up-after-failed-jobs)
    - [실패한 작업 재시도](#retrying-failed-jobs)
    - [누락된 모델 무시](#ignoring-missing-models)
    - [실패한 작업 레코드 정리](#pruning-failed-jobs)
    - [DynamoDB에 실패한 작업 저장](#storing-failed-jobs-in-dynamodb)
    - [실패한 작업 저장 비활성화](#disabling-failed-job-storage)
    - [실패한 작업 이벤트](#failed-job-events)
- [큐에서 작업 제거](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [특정 작업만 페이크 처리](#faking-a-subset-of-jobs)
    - [작업 체인 테스트](#testing-job-chains)
    - [작업 배치 테스트](#testing-job-batches)
    - [작업/큐 상호작용 테스트](#testing-job-queue-interactions)
- [작업 이벤트](#job-events)

<a name="introduction"></a>
## 소개

웹 애플리케이션을 개발하다 보면 업로드된 CSV 파일을 파싱해서 저장하는 작업처럼, 일반적인 웹 요청 중에 처리하기에는 너무 오래 걸리는 작업이 있을 수 있습니다. Laravel은 이러한 작업을 쉽게 백그라운드로 처리할 수 있는 큐 작업(Queued Job)으로 만들 수 있게 도와줍니다. 시간이 오래 걸리는 작업을 큐로 옮기면, 애플리케이션은 웹 요청에 빠르게 응답할 수 있어 사용자 경험이 크게 향상됩니다.

Laravel의 큐 시스템은 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 또는 관계형 데이터베이스와 같은 다양한 큐 백엔드에서 통합된 큐 API를 제공합니다.

큐에 대한 설정은 애플리케이션의 `config/queue.php` 설정 파일에 저장되어 있습니다. 이 파일에는 데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 등 다양한 큐 드라이버의 커넥션 설정과, 즉시 작업을 실행하는 동기 드라이버(로컬 개발용), 그리고 큐에 넣은 작업을 버리는 `null` 드라이버가 포함되어 있습니다.

> [!NOTE]
> Laravel은 이제 Redis 기반 큐를 위한 아름다운 대시보드 및 설정 시스템인 Horizon을 제공합니다. 자세한 내용은 [Horizon 공식 문서](/docs/12.x/horizon)를 참고하세요.

<a name="connections-vs-queues"></a>
### 커넥션과 큐의 차이

Laravel 큐를 사용하기 전에 "커넥션(connection)"과 "큐(queue)"의 차이를 이해하는 것이 중요합니다. `config/queue.php` 파일에는 `connections`라는 배열이 있는데, 이것은 Amazon SQS, Beanstalk, Redis와 같은 백엔드 큐 서비스로의 연결 설정을 정의합니다. 한 개의 큐 커넥션도 여러 "큐"를 가질 수 있는데, 이는 여러 개의 큐 작업 스택 혹은 작업 더미로 이해할 수 있습니다.

각 커넥션 설정 예시에는 `queue` 속성이 있습니다. 이는 작업이 해당 커넥션으로 보낼 때 기본적으로 들어갈 큐 이름을 의미합니다. 즉, 큐 이름을 명시적으로 지정하지 않으면 이 `queue` 속성에 지정된 큐에 작업이 들어가게 됩니다.

```php
use App\Jobs\ProcessPodcast;

// 이 작업은 기본 커넥션의 기본 큐로 전송됩니다...
ProcessPodcast::dispatch();

// 이 작업은 기본 커넥션의 "emails" 큐로 전송됩니다...
ProcessPodcast::dispatch()->onQueue('emails');
```

대부분의 애플리케이션은 큐를 하나만 사용해도 충분하지만, 여러 개의 큐를 사용하면 큐 작업의 우선순위나 처리 방식을 구분할 수 있어 더 효율적으로 처리할 수 있습니다. Laravel의 큐 워커에게 어떤 큐부터 처리할지 우선순위를 지정할 수도 있습니다. 예를 들어 `high` 큐에 작업을 넣었다면 아래와 같이 해당 큐를 우선적으로 처리하도록 워커를 실행할 수 있습니다.

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버별 참고사항 및 선행 조건

<a name="database"></a>
#### 데이터베이스

`database` 큐 드라이버를 사용하려면 작업 정보를 저장할 데이터베이스 테이블이 필요합니다. Laravel에서는 기본적으로 `0001_01_01_000002_create_jobs_table.php` [마이그레이션](/docs/12.x/migrations)이 포함되어 있습니다. 만약 이 마이그레이션이 없다면 `make:queue-table` Artisan 명령어로 쉽게 생성할 수 있습니다.

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면 `config/database.php` 파일에서 Redis 데이터베이스 커넥션을 미리 설정해야 합니다.

> [!WARNING]
> `redis` 큐 드라이버에서는 Redis의 `serializer` 및 `compression` 옵션을 지원하지 않습니다.

<a name="redis-cluster"></a>
##### Redis 클러스터

Redis 큐 커넥션에서 [Redis 클러스터](https://redis.io/docs/latest/operate/rs/databases/durability-ha/clustering)를 사용할 경우, 큐 이름에 반드시 [키 해시 태그(key hash tag)](https://redis.io/docs/latest/develop/using-commands/keyspace/#hashtags)를 포함해야 합니다. 이는 동일한 큐에 대한 Redis 키들이 하나의 해시 슬롯에 저장되도록 보장합니다.

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

Redis 큐를 사용할 때, `block_for` 설정값을 사용하면 워커가 큐에서 작업이 나올 때까지 최대 몇 초까지 대기할지 지정할 수 있습니다. 이 값을 적절히 조절하면 계속해서 Redis를 폴링하는 방식보다 리소스 효율이 좋아집니다. 예를 들어, 5초로 설정하면 새로운 작업이 나타날 때까지 최대 5초간 대기합니다.

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
> `block_for`를 `0`으로 설정하면 큐 워커가 작업이 나올 때까지 무한히 대기합니다. 이 경우 `SIGTERM`과 같은 신호를 잡아 처리하지 못하고, 새 작업이 들어와야만 처리됩니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 선행 조건

아래 큐 드라이버를 사용하려면 Composer로 종속 패키지를 반드시 설치해야 합니다.

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~2.0` 또는 phpredis PHP 확장
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`

<a name="creating-jobs"></a>
## 작업(Job) 생성

<a name="generating-job-classes"></a>
### 작업 클래스 생성

애플리케이션의 작업(Queueable Job) 클래스들은 기본적으로 `app/Jobs` 디렉토리에 저장됩니다. 만약 이 디렉토리가 없다면, `make:job` Artisan 명령어를 실행할 때 자동으로 생성됩니다.

```shell
php artisan make:job ProcessPodcast
```

생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현합니다. 이 인터페이스를 통해 Laravel이 작업을 큐에 넣어 비동기로 처리해야 함을 인식합니다.

> [!NOTE]
> 작업용 스텁은 [stub 커스터마이징](/docs/12.x/artisan#stub-customization) 기능을 통해 직접 수정해 사용할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조

작업 클래스는 주로 `handle` 메서드만 담고 있을 정도로 단순할 수 있습니다. 이 메서드는 큐가 작업을 처리할 때 실행됩니다. 예를 들어, 팟캐스트 서비스에서 업로드된 파일을 처리/배포하는 작업 클래스를 살펴보겠습니다.

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

위 예제처럼, 큐 작업에 [Eloquent 모델](/docs/12.x/eloquent)을 직접 주입해서 사용할 수도 있습니다. 작업에 `Queueable` 트레이트가 사용된 덕분에, Eloquent 모델과 그에 연결된 연관관계 데이터도 안전하게 직렬화/역직렬화 됩니다.

작업의 생성자에서 Eloquent 모델을 받으면, 큐에 실릴 때는 해당 모델의 식별자만 저장됩니다. 작업이 실행될 때 큐 시스템이 데이터베이스에서 모델 및 연관관계 데이터를 자동으로 다시 불러오므로, 작업 페이로드가 더 작아집니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드의 의존성 주입

`handle` 메서드는 큐에서 작업이 실제로 처리될 때 호출됩니다. 이 메서드의 파라미터에 타입힌트를 지정하면, Laravel의 [서비스 컨테이너](/docs/12.x/container)가 해당 의존성을 자동으로 주입해줍니다.

만약 컨테이너의 의존성 주입 과정을 직접 제어하고 싶다면, `bindMethod` 메서드를 사용할 수 있습니다. 이 메서드에 콜백을 전달하면 handle 메서드를 원하는 방식으로 호출할 수 있습니다. 보통은 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 등록합니다.

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 바이너리 데이터(예: 원시 이미지/파일 데이터)는 큐에 전달하기 전 `base64_encode`로 인코딩해야 합니다. 그렇지 않으면 작업이 JSON으로 직렬화되지 않아 큐에 정상적으로 저장되지 않을 수 있습니다.

<a name="handling-relationships"></a>
#### 큐 작업의 연관관계 처리

큐에 직렬화될 때 Eloquent 모델의 연관관계까지 모두 포함되면, 직렬화된 문자열이 매우 커질 수 있습니다. 또한 큐에서 역직렬화 후 모델의 연관관계가 데이터베이스에서 다시 로드될 때, 직렬화 전에 지정한 쿼리 제약 조건이 무시되고 전체 연관관계 데이터가 불러와집니다. 따라서, 연관관계의 일부분만 다루고 싶다면, 작업 내에서 직접 제약 조건을 다시 지정해야 합니다.

또는, 모델의 연관관계 자체를 아예 직렬화에서 제외하려면, 값을 할당할 때 `withoutRelations` 메서드를 사용하세요. 이 메서드는 연관관계 없이 모델 인스턴스를 반환합니다.

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

[PHP 생성자 프로퍼티 프로모션](https://www.php.net/manual/en/language.oop5.decon.php#language.oop5.decon.constructor.promotion)을 사용할 경우, 모델에 `WithoutRelations` 속성을 지정해서 연관관계 직렬화를 막을 수도 있습니다.

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

여러 모델 속성에 대해 일일이 속성을 반복 지정하는 대신, 클래스 전체에 `WithoutRelations` 속성을 부여하여 모든 모델에서 연관관계를 제외할 수도 있습니다.

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

작업이 Eloquent 모델의 컬렉션 혹은 배열 전체를 받는 경우, 역직렬화 및 실행 과정에서 그 안의 모델들은 연관관계가 복원되지 않습니다. 이는 대량의 모델을 처리하는 작업에서 과도한 리소스 사용을 막기 위한 것입니다.

<a name="unique-jobs"></a>
### 고유 작업(Unique Jobs)

> [!WARNING]
> 고유 작업(`ShouldBeUnique`)은 [락(locks)](/docs/12.x/cache#atomic-locks)를 지원하는 캐시 드라이버가 필요합니다. 사용 가능한 드라이버는 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array`입니다. 또한, 배치 안의 작업에는 고유 제약이 적용되지 않습니다.

특정 작업이 한 번에 큐에 중복적으로 여러 번 쌓이지 않도록 하고 싶을 때, 작업 클래스에 `ShouldBeUnique` 인터페이스를 구현하면 됩니다. 별도의 메서드 구현 없이도 작동합니다.

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

위 예시에서 `UpdateSearchIndex` 작업은 고유 작업이므로, 동일한 작업이 큐에 이미 올라가 처리 중이라면 새로 디스패치되지 않습니다.

작업의 고유성을 판단하는 "키"를 특정 값으로 지정하거나, 고유 상태의 유지 시간을 지정하고 싶을 때는 `uniqueId` 및 `uniqueFor` 프로퍼티(또는 메서드)를 클래스에 추가합니다.

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
     * 고유 락의 유지 시간(초)
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

이처럼 특정 상품 ID로 고유성을 부여하면, 해당 상품 ID로 이미 큐에 진행 중인 작업이 있다면 새로 디스패치 되는 작업은 무시됩니다. 또한, 1시간 이내로 기존 작업이 완료되지 않으면 고유 락이 해제되어 동일 키의 새로운 작업이 큐에 올라갈 수 있습니다.

> [!WARNING]
> 여러 웹서버나 컨테이너에서 큐를 디스패치한다면, 모든 서버가 같은 중앙 캐시 서버를 이용해야 고유 작업 조건이 제대로 적용됩니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 작업이 처리 시작 전까지 고유성 유지

기본적으로 고유 작업은 작업이 성공적으로 처리 완료(혹은 모든 재시도 실패)될 때 락이 해제됩니다. 작업이 실제 처리 직전에 즉시 락이 해제되길 원한다면, `ShouldBeUnique` 대신 `ShouldBeUniqueUntilProcessing` 인터페이스를 구현하게 하세요.

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
#### 고유 작업 락(Unique Job Locks)

내부적으로 `ShouldBeUnique` 작업이 디스패치 되면, Laravel은 `uniqueId`로 [락(atomic lock)](/docs/12.x/cache#atomic-locks)을 시도합니다. 락이 이미 점유되어 있으면 작업을 큐에 추가하지 않습니다. 이 락은 작업이 처리 종료되거나 모든 재시도에 실패할 때 해제됩니다. 락 획득에 사용할 캐시 드라이버를 바꾸려면 `uniqueVia` 메서드를 추가하세요.

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
> 단순히 동시에 여러 작업 처리 제한만 원한다면, [WithoutOverlapping](/docs/12.x/queues#preventing-job-overlaps) 작업 미들웨어를 사용하는 것이 좋습니다.

<a name="encrypted-jobs"></a>
### 암호화된 작업(Encrypted Jobs)

작업 데이터의 보안(기밀성과 무결성)을 보장해야 할 때, [암호화](/docs/12.x/encryption)를 통해 처리할 수 있습니다. 작업 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하면, Laravel이 해당 작업 페이로드를 자동으로 암호화하여 큐에 넣어줍니다.

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
## 작업 미들웨어

작업 미들웨어는 큐 작업 실행 전후로 사용자 로직을 간단히 추가할 수 있도록 해주며, 개별 작업의 핸들 메서드에서 반복되는 코드를 줄여줍니다. 예를 들어, Redis 기반 속도 제한을 적용해 5초마다 1개 작업만 처리하도록 만드는 코드를 생각해보세요.

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

이처럼 핸들 메서드 안에 직접 속도 제한 코드를 넣으면 코드가 지저분해지고, 여러 작업에서 동일 코드를 반복하게 됩니다.

핸들 메서드가 아닌 별도의 미들웨어 클래스를 만들고, 여기에 속도 제한 기능을 분리하는 것이 더 좋습니다. Laravel은 작업 미들웨어의 위치에 제한을 두지 않지만, 예시에서는 `app/Jobs/Middleware`에 두었습니다.

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

미들웨어는 [라우트 미들웨어](/docs/12.x/middleware)와 마찬가지로, 처리 중인 작업과 다음 콜백(`$next`)을 전달받아 흐름을 제어합니다.

새로운 작업 미들웨어 클래스를 추가할 때는 `make:job-middleware` Artisan 명령어를 사용할 수 있습니다. 이렇게 만든 미들웨어는 작업의 `middleware` 메서드에서 배열로 반환해야 하며, 이 메서드는 직접 추가해 줘야 합니다.

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
> 작업 미들웨어는 [큐 처리가 되는 이벤트 리스너](/docs/12.x/events#queued-event-listeners), [메일(Mailable)](/docs/12.x/mail#queueing-mail), [알림(Notification)](/docs/12.x/notifications#queueing-notifications)에도 지정할 수 있습니다.

<a name="rate-limiting"></a>
### 속도 제한(Rate Limiting)

직접 속도 제한 미들웨어를 만들 수도 있지만, Laravel에는 내장된 속도 제한 미들웨어가 있습니다. [라우트 속도 제한자](/docs/12.x/routing#defining-rate-limiters)와 유사하게, `RateLimiter` 파사드의 `for` 메서드로 정의할 수 있습니다.

예를 들어, 무료 회원은 한 시간에 1번만 백업을 허용하고, 프리미엄 회원은 무제한으로 허용한다고 가정합니다.

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

또는, 분 단위 제한은 `perMinute`를, 유저 구분값은 `by`에 원하는 값을 넘길 수 있습니다.

```php
return Limit::perMinute(50)->by($job->user->id);
```

정의된 속도 제한을 실제 작업에 적용하려면, `Illuminate\Queue\Middleware\RateLimited` 미들웨어를 사용하면 됩니다. 제한을 초과하면, 미들웨어가 작업을 적절한 지연 시간과 함께 큐에 다시 올려 보냅니다.

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

속도 제한으로 인해 큐에 다시 올라간 작업도 시도 횟수(`attempts`)가 증가하므로, 클래스의 `$tries`나 `$maxExceptions` 값을 적절히 조정하는 것이 좋습니다. 혹은 [retryUntil 메서드](#time-based-attempts)로 시도 제한 시간을 정할 수도 있습니다.

`releaseAfter`로 작업이 다시 시도되기까지 대기할 초 단위를 지정할 수 있습니다.

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

속도 제한에 걸린 작업을 큐에 다시 올리지 않고 아예 재시도하지 않으려면 `dontRelease` 메서드를 사용하세요.

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
> Redis를 사용하는 경우, 더 최적화된 `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어를 사용할 수 있습니다.

<a name="preventing-job-overlaps"></a>
### 작업 중복 방지

`Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어는 특정 키를 기준으로 중복된 작업이 동시에 처리되는 것을 막아줍니다. 리소스를 동시에 수정할 수 있는 작업에 유용합니다.

예를 들어, 한 유저의 신용 등급을 업데이트하는 작업이 중복 실행되는 것을 막고 싶다면 아래처럼 미들웨어를 추가해줍니다.

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

중복된 작업을 큐에 다시 올리고 싶을 때는 대기 시간을 `releaseAfter`로 지정합니다.

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

중복된 작업을 즉시 삭제해서 재시도하지 않으려면 `dontRelease`를 사용합니다.

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

미들웨어는 Laravel의 atomic lock 기능을 이용합니다. 그러나 작업이 비정상적으로 종료되어 락이 해제되지 않는 상황을 대비해, `expireAfter`로 락의 만료 시간을 지정할 수도 있습니다.

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
> 이 미들웨어는 [락(locks)](/docs/12.x/cache#atomic-locks)가 지원되는 캐시 드라이버(`memcached`, `redis`, `dynamodb`, `database`, `file`, `array`)가 필요합니다.

<a name="sharing-lock-keys"></a>
#### 여러 작업 클래스에서 락 키 공유

기본적으로 `WithoutOverlapping` 미들웨어는 같은 클래스 내에서만 중복을 방지합니다. 서로 다른 작업 클래스가 같은 락 키를 써도 중복 처리가 되지 않습니다. 여러 작업 클래스에서 락을 공유하려면 `shared` 메서드를 사용하세요.

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
### 예외 스로틀링(Throttling Exceptions)

`Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어는 예외 발생 횟수를 일정 횟수 초과할 경우, 이후 재시도를 일정 시간 동안 지연시킵니다. 외부 API처럼 불안정한 작업 등에 유용합니다.

예를 들어, 외부 API 호출에서 예외가 계속 발생하는 경우, 다음과 같이 미들웨어를 지정해 예외를 "스로틀" 할 수 있습니다. (보통 [시간 기반 시도 제한](#time-based-attempts)과 함께 사용합니다.)

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

생성자의 첫 번째 인자는 예외 허용 횟수, 두 번째는 예외 발생 시 재시도까지 대기할 초 단위입니다. 위 코드는 예외가 10회 발생하면 5분 후 다시 시도하며, 전체 제한 시간은 30분입니다.

예외가 `임계값`에 도달하지 않은 경우 기본적으로 즉시 재시도합니다. `backoff`로 딜레이를 조절할 수 있습니다.

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

이 미들웨어는 작업 클래스명을 캐시 키로 삼아 율 제한을 적용합니다. 여러 작업에서 동일 키로 묶으려면 `by`를 사용하세요.

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

기본적으로는 모든 예외에 대해 스로틀이 동작합니다. 특정 예외만 대상으로 하려면 `when`에 클로저를 넣으세요.

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

`when` 대신, 특정 예외 발생 시 작업을 바로 삭제하고 싶다면 `deleteWhen`을 사용하세요.

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

스로틀된 예외를 애플리케이션 예외 핸들러에 보고하려면 `report`로 지정하세요. 클로저를 넘길 수도 있습니다.

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
> Redis 사용 시에는 더 효율적인 `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어를 사용할 수 있습니다.

<a name="skipping-jobs"></a>
### 작업 건너뛰기(Skipping Jobs)

`Skip` 미들웨어는 복잡한 조건에 따라 작업을 "건너뛰고"(삭제) 싶을 때, 작업 코드 수정 없이 미들웨어만으로 처리할 수 있게 합니다. `Skip::when`은 주어진 조건이 `true`면 작업을 삭제, `Skip::unless`는 `false`면 작업을 삭제합니다.

```php
use Illuminate\Queue\Middleware\Skip;

/**
 * Get the middleware the job should pass through.
 */
public function middleware(): array
{
    return [
        Skip::when($condition),
    ];
}
```

좀 더 복잡한 조건은 클로저로 전달하세요.

```php
use Illuminate\Queue\Middleware\Skip;

/**
 * Get the middleware the job should pass through.
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

(이하 내용 계속...)