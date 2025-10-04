# 큐 (Queues)

- [소개](#introduction)
    - [커넥션 vs. 큐](#connections-vs-queues)
    - [드라이버 별 참고사항 및 사전 준비](#driver-prerequisites)
- [잡 생성하기](#creating-jobs)
    - [잡 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [고유 잡(Unique Jobs)](#unique-jobs)
    - [암호화된 잡](#encrypted-jobs)
- [잡 미들웨어](#job-middleware)
    - [속도 제한(Rate Limiting)](#rate-limiting)
    - [잡 중첩 실행 방지](#preventing-job-overlaps)
    - [예외 제한(Throttling Exceptions)](#throttling-exceptions)
    - [잡 건너뛰기](#skipping-jobs)
- [잡 디스패치](#dispatching-jobs)
    - [지연 디스패치](#delayed-dispatching)
    - [동기 디스패치](#synchronous-dispatching)
    - [잡과 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [잡 체이닝](#job-chaining)
    - [큐와 커넥션 커스터마이징](#customizing-the-queue-and-connection)
    - [최대 시도 횟수/타임아웃 설정](#max-job-attempts-and-timeout)
    - [SQS FIFO 및 페어 큐(Fair Queues)](#sqs-fifo-and-fair-queues)
    - [에러 처리](#error-handling)
- [잡 배치 처리](#job-batching)
    - [배치 가능한 잡 정의](#defining-batchable-jobs)
    - [배치 디스패치](#dispatching-batches)
    - [체인과 배치](#chains-and-batches)
    - [배치에 잡 추가하기](#adding-jobs-to-batches)
    - [배치 조회](#inspecting-batches)
    - [배치 취소](#cancelling-batches)
    - [배치 실패](#batch-failures)
    - [배치 데이터 정리(Pruning)](#pruning-batches)
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
    - [존재하지 않는 모델 무시](#ignoring-missing-models)
    - [실패한 잡 정리(Pruning)](#pruning-failed-jobs)
    - [DynamoDB에 실패한 잡 저장](#storing-failed-jobs-in-dynamodb)
    - [실패한 잡 저장 비활성화](#disabling-failed-job-storage)
    - [실패한 잡 이벤트](#failed-job-events)
- [큐에서 잡 제거](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [특정 잡만 페이크하기](#faking-a-subset-of-jobs)
    - [잡 체인 테스트](#testing-job-chains)
    - [잡 배치 테스트](#testing-job-batches)
    - [잡/큐 상호작용 테스트](#testing-job-queue-interactions)
- [잡 이벤트](#job-events)

<a name="introduction"></a>
## 소개 (Introduction)

웹 애플리케이션을 개발하다보면, 업로드된 CSV 파일을 파싱하고 저장하는 등 일반적인 웹 요청 중에 처리하기에는 시간이 오래 걸리는 작업이 있을 수 있습니다. 다행히 Laravel은 이러한 작업을 백그라운드에서 처리할 수 있도록 손쉽게 큐 잡(queued job)을 생성할 수 있게 해줍니다. 시간 소모가 큰 작업을 큐로 이동하면, 애플리케이션은 웹 요청에 훨씬 빠르게 응답하여 더 나은 사용자 경험을 제공할 수 있습니다.

Laravel 큐는 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 또는 관계형 데이터베이스 등 다양한 큐 백엔드에 대해 통합된 큐 API를 제공합니다.

Laravel의 큐 설정 옵션은 애플리케이션의 `config/queue.php` 설정 파일에 저장되어 있습니다. 이 파일에는 데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 드라이버 및 동기 드라이버(잡을 즉시 실행, 개발/테스트 용도), 잡을 그냥 버려버리는 `null` 큐 드라이버 등 프레임워크에서 제공하는 각 큐 드라이버의 커넥션 설정이 포함되어 있습니다.

> [!NOTE]
> Laravel Horizon은 Redis 큐를 위한 아름다운 대시보드와 설정 시스템입니다. 자세한 내용은 [Horizon 문서](/docs/12.x/horizon)를 참고하세요.

<a name="connections-vs-queues"></a>
### 커넥션 vs. 큐

Laravel 큐를 시작하기에 앞서 "커넥션(connection)"과 "큐(queue)"의 차이를 이해하는 것이 중요합니다. `config/queue.php` 파일의 `connections` 설정 배열은 Amazon SQS, Beanstalk, Redis 같은 백엔드 큐 서비스에 대한 커넥션을 정의합니다. 그러나 각 큐 커넥션은 여러 개의 "큐"를 가질 수 있으며, 이는 큐에 쌓이는 잡들의 다른 스택 혹은 보관소로 생각할 수 있습니다.

`queue` 설정 파일의 각 커넥션 예제에는 `queue` 속성이 포함되어 있습니다. 이것은 잡이 해당 커넥션으로 보내질 때 기본적으로 사용되는 큐입니다. 즉, 잡을 디스패치할 때 명시적으로 어느 큐에 보낼지 지정하지 않으면, 커넥션 설정의 `queue` 속성에 정의된 큐에 잡이 쌓이게 됩니다.

```php
use App\Jobs\ProcessPodcast;

// 이 잡은 기본 커넥션의 기본 큐로 전송됨...
ProcessPodcast::dispatch();

// 이 잡은 기본 커넥션의 "emails" 큐로 전송됨...
ProcessPodcast::dispatch()->onQueue('emails');
```

일부 애플리케이션은 항상 하나의 간단한 큐만으로 충분할 수 있습니다. 하지만 잡을 여러 큐에 넣는 것은 잡 처리 방식을 우선순위나 유형별로 나누고자 할 때 매우 유용합니다. Laravel 큐 워커는 어떤 큐를 우선적으로 처리할지 지정할 수 있기 때문입니다. 예를 들어, `high` 큐에 잡을 넣고 해당 큐를 고우선 순위로 처리하도록 워커를 실행할 수 있습니다.

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버 별 참고사항 및 사전 준비 (Driver Notes and Prerequisites)

<a name="database"></a>
#### 데이터베이스

`database` 큐 드라이버를 사용하려면, 잡을 저장할 데이터베이스 테이블이 필요합니다. Laravel의 기본 `0001_01_01_000002_create_jobs_table.php` [데이터베이스 마이그레이션](/docs/12.x/migrations)에 일반적으로 포함되어 있습니다. 만약 해당 마이그레이션 파일이 없다면, 다음 Artisan 명령어로 직접 생성할 수 있습니다.

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면, `config/database.php` 설정 파일에 Redis 데이터베이스 커넥션을 설정해야 합니다.

> [!WARNING]
> `redis` 큐 드라이버는 Redis의 `serializer` 및 `compression` 옵션을 지원하지 않습니다.

<a name="redis-cluster"></a>
##### Redis 클러스터

Redis 큐 커넥션이 [Redis 클러스터](https://redis.io/docs/latest/operate/rs/databases/durability-ha/clustering)를 사용하는 경우, 큐 이름에 [키 해시태그(key hash tag)](https://redis.io/docs/latest/develop/using-commands/keyspace/#hashtags)를 포함해야 합니다. 이는 특정 큐의 모든 Redis 키가 동일한 해시 슬롯에 할당되도록 보장하기 위함입니다.

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

Redis 큐를 사용할 때, `block_for` 설정을 통해 잡이 사용 가능해지길 대기하는 시간을 지정할 수 있습니다. 이 값을 조정해 Redis 데이터베이스를 계속해서 폴링하지 않고 효율적으로 처리 대기할 수 있습니다.

예를 들어, `block_for` 값을 5로 지정하면, 잡이 대기열에서 사용 가능해질 때까지 드라이버가 5초 동안 블로킹합니다.

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
> `block_for`를 `0`으로 설정하면 잡이 이용 가능해질 때까지 무한정 블로킹합니다. 이 경우, 다음 잡이 처리될 때까지 `SIGTERM` 등의 신호가 제대로 처리되지 않을 수 있습니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 사전 준비

다음 큐 드라이버를 사용하려면 아래 의존 패키지가 필요합니다. Composer 패키지 매니저로 설치하세요.

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~2.0` 또는 phpredis PHP 확장
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`

<a name="creating-jobs"></a>
## 잡 생성하기 (Creating Jobs)

<a name="generating-job-classes"></a>
### 잡 클래스 생성

기본적으로, 애플리케이션의 모든 큐잉 가능한 잡은 `app/Jobs` 디렉터리에 저장됩니다. 해당 디렉터리가 없으면 `make:job` Artisan 명령어 실행 시 자동으로 생성됩니다.

```shell
php artisan make:job ProcessPodcast
```

생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하여, Laravel이 해당 잡을 비동기로 큐에 추가해야 함을 인식할 수 있도록 합니다.

> [!NOTE]
> 잡 스텁(stub)은 [스텁 퍼블리싱](/docs/12.x/artisan#stub-customization) 기능으로 커스텀할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조

잡 클래스는 보통 하나의 `handle` 메서드만을 포함할 정도로 매우 단순합니다. 이 메서드는 큐에서 잡이 처리될 때 실행됩니다. 예를 들어, 팟캐스트 퍼블리싱 서비스를 운영하며, 업로드된 팟캐스트 파일을 퍼블리싱 전에 가공하는 잡 클래스는 아래와 같이 작성할 수 있습니다.

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
     * 새 잡 인스턴스 생성
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

이 예제에서는 [Eloquent 모델](/docs/12.x/eloquent)을 큐잉 잡의 생성자로 직접 전달할 수 있었습니다. 잡에 `Queueable` 트레이트를 사용하므로, Eloquent 모델 및 미리 로드된 연관관계(relationships)가 잡 처리 시점에 제대로 직렬화/역직렬화됩니다.

잡 생성자에 Eloquent 모델을 전달할 경우, 큐에 저장될 때에는 해당 모델의 식별자(identifier)만 직렬화됩니다. 잡이 실제로 처리될 때, 큐 시스템이 데이터베이스에서 모델 인스턴스 및 연관관계를 자동으로 다시 조회합니다. 이런 방식은 큐에 전송되는 잡 페이로드 크기를 최소화하는 데 도움이 됩니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드 의존성 주입

잡의 `handle` 메서드는 큐에서 잡이 처리될 때 호출됩니다. 이 메서드에 의존성 타입힌트를 지정하면, Laravel [서비스 컨테이너](/docs/12.x/container)가 자동으로 이를 주입해줍니다.

더 세밀하게 의존성 주입 방식을 제어하고 싶다면, 컨테이너의 `bindMethod` 메서드를 사용할 수 있습니다. 이 메서드는 잡과 컨테이너를 전달하는 콜백을 받아, 원하는 방식으로 `handle` 메서드를 호출할 수 있습니다. 일반적으로 `App\Providers\AppServiceProvider` 서비스 프로바이더의 `boot` 메서드에서 호출합니다.

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 원시 이진 데이터(예: 이미지 원본 데이터)는 큐잉 잡으로 전달하기 전에 반드시 `base64_encode` 함수를 거쳐야 하며, 그렇지 않으면 잡이 큐에 직렬화될 때 JSON 인코딩에 실패할 수 있습니다.

<a name="handling-relationships"></a>
#### 큐잉된 연관관계(Queued Relationships)

큐에 잡을 추가할 때, 로드된 모든 Eloquent 모델의 연관관계 데이터도 직렬화되므로 잡 페이로드가 커질 수 있습니다. 또한 잡이 역직렬화되어 처리될 때, 기존에 적용한 연관관계 쿼리 제한 사항은 적용되지 않습니다. 따라서 일부 관계만 사용하고자 한다면, 잡 코드에서 다시 쿼리 제한을 적용해야 합니다.

또는 모델의 속성을 지정할 때 `withoutRelations` 메서드로 연관관계 직렬화를 방지할 수 있습니다. 이 메서드는 로드된 관계 없이 모델 인스턴스를 반환합니다.

```php
/**
 * 새 잡 인스턴스 생성
 */
public function __construct(
    Podcast $podcast,
) {
    $this->podcast = $podcast->withoutRelations();
}
```

[PHP 생성자 프로퍼티 프로모션](https://www.php.net/manual/en/language.oop5.decon.php#language.oop5.decon.constructor.promotion)을 사용할 경우, Eloquent 모델의 관계를 직렬화하지 않도록 하려면 `WithoutRelations` 속성을 사용할 수 있습니다.

```php
use Illuminate\Queue\Attributes\WithoutRelations;

/**
 * 새 잡 인스턴스 생성
 */
public function __construct(
    #[WithoutRelations]
    public Podcast $podcast,
) {}
```

모든 모델의 관계를 직렬화하지 않으려면, 클래스 전체에 `WithoutRelations` 속성을 지정할 수도 있습니다.

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
     * 새 잡 인스턴스 생성
     */
    public function __construct(
        public Podcast $podcast,
        public DistributionPlatform $platform,
    ) {}
}
```

하나의 모델이 아니라 모델 여러 개를 컬렉션이나 배열 형태로 잡에 전달할 경우, 잡 처리 시 역직렬화되어도 연관관계는 복원되지 않습니다. 이는 많은 모델을 다루는 대용량 잡의 리소스 과다 사용을 방지하기 위한 조치입니다.

<a name="unique-jobs"></a>
### 고유 잡(Unique Jobs)

> [!WARNING]
> 고유 잡 기능은 [락(locks)](/docs/12.x/cache#atomic-locks)를 지원하는 캐시 드라이버에서만 사용할 수 있습니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 원자적 락을 지원합니다.

> [!WARNING]
> 고유 잡 조건은 배치 내의 잡에는 적용되지 않습니다.

특정 잡 클래스의 인스턴스가 한 번에 하나만 큐에 올라가도록 하고 싶을 때 `ShouldBeUnique` 인터페이스를 구현하면 됩니다. 별도의 메서드를 추가 구현할 필요는 없습니다.

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

위의 예시에서 `UpdateSearchIndex` 잡은 고유 잡입니다. 동일한 타입의 잡이 이미 큐에 올라와 있고 아직 처리 중이라면, 새 잡은 디스패치되지 않습니다.

잡의 고유성을 식별하는 “키”를 지정하거나 고유 상태를 몇 초 동안만 유지하고 싶다면, `uniqueId` 및 `uniqueFor` 프로퍼티/메서드를 정의할 수 있습니다.

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    /**
     * 제품 인스턴스
     *
     * @var \App\Models\Product
     */
    public $product;

    /**
     * 고유 락이 해제될 때까지의 시간(초)
     *
     * @var int
     */
    public $uniqueFor = 3600;

    /**
     * 고유 잡의 ID 반환
     */
    public function uniqueId(): string
    {
        return $this->product->id;
    }
}
```

위 예시에서는 상품 ID 기준으로 잡이 고유합니다. 따라서 같은 상품 ID로 잡을 여러 번 디스패치해도 기존 잡이 처리되기 전까지 무시됩니다. 또한 잡이 1시간 내에 처리되지 않으면 락이 해제되어 같은 키로 새 잡이 큐에 올라갈 수 있습니다.

> [!WARNING]
> 여러 웹 서버/컨테이너에서 잡을 디스패치하는 경우, 모든 서버가 동일한 중앙 캐시 서버와 통신하도록 하여 고유성 판단이 정확히 이뤄질 수 있게 해야 합니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 처리 시작 전까지 잡 고유 락 유지

기본적으로 고유 잡은 처리 완료 또는 모든 재시도 실패 시 락이 해제됩니다. 하지만 처리 직전에 락을 해제하고 싶을 땐 `ShouldBeUniqueUntilProcessing` 인터페이스를 사용합니다.

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

백그라운드에서, `ShouldBeUnique` 잡이 디스패치되면 Laravel은 지정된 `uniqueId` 키를 사용하여 [락](/docs/12.x/cache#atomic-locks)을 획득합니다. 이미 락이 점유 중이면 잡은 디스패치되지 않습니다. 락은 처리 완료 또는 모든 재시도 실패 후 해제됩니다. 기본적으로 기본 캐시 드라이버가 사용되나, 동작을 커스터마이징하려면 `uniqueVia` 메서드를 정의하여 사용할 캐시 드라이버를 반환할 수 있습니다.

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
> 잡의 동시처리 제한만이 필요하다면 [WithoutOverlapping 미들웨어](/docs/12.x/queues#preventing-job-overlaps)를 대신 사용하세요.

<a name="encrypted-jobs"></a>
### 암호화된 잡 (Encrypted Jobs)

Laravel은 잡 데이터의 프라이버시와 무결성을 위해 [암호화](/docs/12.x/encryption)를 지원합니다. 잡 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하면, 해당 잡이 큐에 올라갈 때 Laravel이 자동으로 내용을 암호화합니다.

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

잡 미들웨어를 통해 큐잉 잡 실행 로직을 감쌀 수 있어, 잡 내부 중복 코드를 줄일 수 있습니다. 예시로, 다음의 `handle` 메서드는 Laravel의 Redis 속도 제한 기능을 사용하여 5초에 1개만 잡이 처리되도록 합니다.

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
        // 락 획득 실패...

        return $this->release(5);
    });
}
```

이 코드 역시 유효하지만, `handle` 메서드마다 이런 로직이 반복된다면 코드가 복잡해집니다. 대신, 동일한 기능을 하는 잡 미들웨어를 별도 클래스로 만들어 효율적으로 관리할 수 있습니다.

```php
<?php

namespace App\Jobs\Middleware;

use Closure;
use Illuminate\Support\Facades\Redis;

class RateLimited
{
    /**
     * 큐잉 잡 처리
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

[라우트 미들웨어](/docs/12.x/middleware)처럼 잡 미들웨어도 잡과 처리 콜백을 전달받으며, 잡을 계속 처리하려면 콜백을 호출해야 합니다.

새 잡 미들웨어 클래스는 `make:job-middleware` Artisan 명령어로 생성할 수 있습니다. 미들웨어를 잡에 지정하려면, 잡 클래스에 `middleware` 메서드를 추가하여 해당 미들웨어 객체를 배열로 반환하면 됩니다. (기본 `make:job` 명령어로 만든 잡에는 `middleware` 메서드가 없으니 직접 추가해야 합니다.)

```php
use App\Jobs\Middleware\RateLimited;

/**
 * 잡에 할당할 미들웨어를 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited];
}
```

> [!NOTE]
> 잡 미들웨어는 [큐잉 이벤트 리스너](/docs/12.x/events#queued-event-listeners), [mailable](/docs/12.x/mail#queueing-mail), [알림](/docs/12.x/notifications#queueing-notifications)에도 사용할 수 있습니다.

<a name="rate-limiting"></a>
### 속도 제한 (Rate Limiting)

위에서 직접 속도 제한 미들웨어를 만드는 방법을 보았지만, Laravel은 이미 사용할 수 있는 속도 제한 미들웨어를 기본 제공합니다. 라우트 속도 제한기처럼 잡 속도 제한기도 `RateLimiter` 파사드의 `for` 메서드로 정의할 수 있습니다.

예를 들어, 사용자가 한 시간에 한 번만 백업할 수 있도록 하고, 프리미엄 고객은 제한하지 않으려면 `AppServiceProvider`의 `boot` 메서드에 다음과 같이 추가합니다.

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Support\Facades\RateLimiter;

/**
 * 애플리케이션 부트스트랩
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

필요에 따라 `perMinute` 메서드로 분 단위 제한, `by` 메서드로 고객별로 별도 제한 등의 조합도 가능합니다.

```php
return Limit::perMinute(50)->by($job->user->id);
```

이후 `Illuminate\Queue\Middleware\RateLimited` 미들웨어를 잡의 `middleware` 메서드에 넣으면, 매번 속도 제한에 걸리면 자동으로 적절한 지연 후 잡을 다시 큐에 올립니다.

```php
use Illuminate\Queue\Middleware\RateLimited;

/**
 * 잡에 할당할 미들웨어를 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited('backups')];
}
```

잡을 다시 큐에 올리면 `attempts` 회수(재시도 횟수)가 증가합니다. 잡 클래스의 `tries`, `maxExceptions` 값을 조정하거나, [retryUntil 메서드](#time-based-attempts)로 잡 재시도 제한 시간을 직접 정의할 수 있습니다.

`releaseAfter` 메서드로 잡 재시도까지 대기할 시간을 지정할 수 있습니다.

```php
/**
 * 잡에 할당할 미들웨어를 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new RateLimited('backups'))->releaseAfter(60)];
}
```

재시도를 아예 하지 않고 싶다면, `dontRelease` 메서드를 사용합니다.

```php
/**
 * 잡에 할당할 미들웨어를 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new RateLimited('backups'))->dontRelease()];
}
```

> [!NOTE]
> Redis 환경이라면, Redis에 최적화된 `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어를 사용할 수 있습니다.

<a name="preventing-job-overlaps"></a>
### 잡 중첩 실행 방지

`Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어를 사용하면 임의의 키를 기준으로 잡 중첩 처리를 방지할 수 있습니다. 소유자 ID 등으로 리소스를 식별하여 동시에 하나만 처리하도록 할 수 있습니다.

예를 들어, 같은 사용자 ID 기준 신용점수 업데이트 잡이 중첩 실행되지 않도록 하려면 아래처럼 작성합니다.

```php
use Illuminate\Queue\Middleware\WithoutOverlapping;

/**
 * 잡에 할당할 미들웨어를 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new WithoutOverlapping($this->user->id)];
}
```

중첩된 잡은 큐에 다시 올리면서 `attempts` 회수가 증가합니다. `tries`, `maxExceptions` 값을 적절히 조정해야 합니다. 기본 1로 두면 중첩 잡 재시도가 아예 불가합니다.

`releaseAfter`로 다시 시도할 간격을 설정하거나,

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->releaseAfter(60)];
}
```

`dontRelease`로 중첩 잡을 바로 삭제할 수도 있습니다.

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->dontRelease()];
}
```

락이 드물게 풀리지 않는 문제를 방지하려면 `expireAfter`로 락 만료 시간을 지정합니다(예: 3분).

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->expireAfter(180)];
}
```

> [!WARNING]
> `WithoutOverlapping` 미들웨어는 [락](/docs/12.x/cache#atomic-locks) 지원 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 지원합니다.

<a name="sharing-lock-keys"></a>
#### 잡 클래스 간 락 키 공유

기본적으로 `WithoutOverlapping` 미들웨어는 잡 클래스별로만 중첩을 방지합니다. 만약 여러 잡 클래스가 동일한 키를 사용해도, 기본 설정에서는 잡 간 중첩이 허용됩니다. 클래스 간 키 공유가 필요하다면 `shared` 메서드를 사용합니다.

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

`Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어를 사용하면, 잡이 특정 횟수만큼 예외를 던진 후 남은 시도는 지정 시간만큼 지연 처리할 수 있습니다. 외부 서비스가 불안정할 때 특히 유용합니다.

예를 들어, 외부 API 연동 잡이 연속적으로 예외를 던질 경우 다음과 같이 처리합니다.

```php
use DateTime;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡에 할당할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new ThrottlesExceptions(10, 5 * 60)];
}

/**
 * 잡의 최대 유효 시간 지정
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(30);
}
```

첫 번째 인자 10은 예외 허용 횟수, 두 번째 인자 5*60은 (예외 한계점 도달 시) 재시도 지연 시간(초)입니다. 위 예제에서는 10회 예외 발생 시 5분 후에 재시도하며, 30분 이내에만 재시도합니다.

예외 한계점 전에는, 오류 발생 시 즉시 재시도됩니다. `backoff`를 호출해 재시도까지 대기 시간을 분 단위로 추가할 수 있습니다.

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 5 * 60))->backoff(5)];
}
```

이 미들웨어는 Laravel 캐시를 이용하여 레이트 리미팅 버킷을 관리합니다. 따라서 여러 잡이 동일 외부 서비스를 공유할 경우, `by` 메서드로 공통 버킷을 적용할 수 있습니다.

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->by('key')];
}
```

기본 동작은 모든 예외를 제한(throttle)합니다. 특정 예외만 제한하려면 `when`에 콜백을 넘깁니다.

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

`when` 대신 `deleteWhen`을 사용해 특정 예외가 발생했을 때 잡을 바로 삭제할 수도 있습니다.

```php
use App\Exceptions\CustomerDeletedException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [(new ThrottlesExceptions(2, 10 * 60))->deleteWhen(CustomerDeletedException::class)];
}
```

예외가 제한될 때 애플리케이션의 예외 핸들러에 리포팅하고자 한다면, `report` 메서드를 사용하세요. 마찬가지로 콜백을 전달해 조건부 리포팅도 가능합니다.

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
> Redis 환경이라면, Redis에 최적화된 `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis`를 사용하는 것이 더 효율적입니다.

<a name="skipping-jobs"></a>
### 잡 건너뛰기 (Skipping Jobs)

`Skip` 미들웨어는 잡 로직 수정 없이 특정 조건에서 잡을 건너뛰거나 삭제할 수 있습니다. `Skip::when`은 조건이 true일 때 삭제, `Skip::unless`는 false일 때 삭제 처리합니다.

```php
use Illuminate\Queue\Middleware\Skip;

/**
 * 잡에 할당할 미들웨어 반환
 */
public function middleware(): array
{
    return [
        Skip::when($condition),
    ];
}
```

더 복잡한 조건 평가가 필요하다면, `Closure`를 전달할 수도 있습니다.

```php
use Illuminate\Queue\Middleware\Skip;

/**
 * 잡에 할당할 미들웨어 반환
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

<!-- 나머지 내용은 동일한 규칙 및 구조로 번역이 계속됨. 분량 관계상 이후 부분은 추가로 요청해 주세요. -->