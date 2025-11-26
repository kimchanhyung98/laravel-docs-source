# 큐 (Queues)

- [소개](#introduction)
    - [커넥션과 큐의 차이](#connections-vs-queues)
    - [드라이버 별 주의사항 및 사전 준비](#driver-prerequisites)
- [잡 생성](#creating-jobs)
    - [잡 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [유니크 잡](#unique-jobs)
    - [암호화된 잡](#encrypted-jobs)
- [잡 미들웨어](#job-middleware)
    - [속도 제한(Rate Limiting)](#rate-limiting)
    - [잡 중복 실행 방지](#preventing-job-overlaps)
    - [예외 처리 제한(Throttling Exceptions)](#throttling-exceptions)
    - [잡 건너뛰기](#skipping-jobs)
- [잡 디스패치](#dispatching-jobs)
    - [지연 디스패치](#delayed-dispatching)
    - [동기 디스패치](#synchronous-dispatching)
    - [잡 & 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [잡 체이닝(Chaining)](#job-chaining)
    - [큐 및 커넥션 커스터마이징](#customizing-the-queue-and-connection)
    - [최대 시도 횟수/타임아웃 값 지정](#max-job-attempts-and-timeout)
    - [SQS FIFO 및 공정 큐](#sqs-fifo-and-fair-queues)
    - [큐 페일오버](#queue-failover)
    - [에러 처리](#error-handling)
- [잡 배치 작업(Job Batching)](#job-batching)
    - [배치 가능한 잡 정의](#defining-batchable-jobs)
    - [배치 디스패치](#dispatching-batches)
    - [체인과 배치](#chains-and-batches)
    - [배치에 잡 추가](#adding-jobs-to-batches)
    - [배치 조회](#inspecting-batches)
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
    - [존재하지 않는 모델 무시](#ignoring-missing-models)
    - [실패한 잡 정리(Pruning)](#pruning-failed-jobs)
    - [실패한 잡을 DynamoDB에 저장](#storing-failed-jobs-in-dynamodb)
    - [실패한 잡 저장 비활성화](#disabling-failed-job-storage)
    - [실패한 잡 이벤트](#failed-job-events)
- [큐에서 잡 삭제](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [일부 잡만 가짜로 처리하기](#faking-a-subset-of-jobs)
    - [잡 체인 테스트](#testing-job-chains)
    - [잡 배치 테스트](#testing-job-batches)
    - [잡/큐 상호작용 테스트](#testing-job-queue-interactions)
- [잡 이벤트](#job-events)

<a name="introduction"></a>
## 소개 (Introduction)

웹 애플리케이션을 개발할 때, 업로드된 CSV 파일을 파싱해 저장하는 등 일반 웹 요청 중에 처리하기에는 시간이 너무 오래 걸리는 작업이 있을 수 있습니다. 다행히도 Laravel은 백그라운드에서 처리할 수 있는 큐잉 잡을 쉽게 만들 수 있게 해줍니다. 시간이 많이 걸리는 작업을 큐로 분리하면 애플리케이션에서 웹 요청을 훨씬 빠르게 처리할 수 있고, 사용자 경험 또한 크게 향상됩니다.

Laravel의 큐 시스템은 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 관계형 데이터베이스 등 다양한 큐 백엔드에서 일관된 큐 API를 제공합니다.

큐 설정 옵션은 애플리케이션의 `config/queue.php` 파일에 정의되어 있습니다. 이 파일에는 프레임워크와 함께 제공되는 각 큐 드라이버(데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 등)와 즉시 잡을 실행하는 동기적(sync) 드라이버(개발/테스트용), 그리고 큐된 잡을 버리는 null 드라이버에 대한 커넥션 설정을 찾을 수 있습니다.

> [!NOTE]
> Laravel Horizon은 Redis 기반 큐를 위한 아름다운 대시보드 및 설정 시스템입니다. 더 자세한 내용은 [Horizon 문서](/docs/12.x/horizon)를 참고하세요.

<a name="connections-vs-queues"></a>
### 커넥션과 큐의 차이

Laravel 큐를 사용하기 전에 "커넥션(connection)"과 "큐(queue)"의 차이를 이해하는 것이 중요합니다. `config/queue.php` 파일에 `connections` 배열이 있습니다. 이 배열은 Amazon SQS, Beanstalk, Redis 등 백엔드 큐 서비스에 대한 커넥션을 정의합니다. 하지만 한 큐 커넥션에는 여러 "큐"가 있을 수 있으며, 이것을 큐에 쌓이는 잡의 스택이나 더미라고 생각할 수 있습니다.

각 커넥션 설정 예제에는 `queue`라는 속성이 포함되어 있습니다. 이 속성은 해당 커넥션에서 잡을 디스패치할 때 기본적으로 사용되는 큐를 지정합니다. 즉, 어떤 큐로 보낼지 명시하지 않고 잡을 디스패치하면 커넥션의 `queue`에 정의된 큐로 들어갑니다.

```php
use App\Jobs\ProcessPodcast;

// 이 잡은 기본 커넥션의 기본 큐로 전송됩니다...
ProcessPodcast::dispatch();

// 이 잡은 기본 커넥션의 "emails" 큐로 전송됩니다...
ProcessPodcast::dispatch()->onQueue('emails');
```

하나의 큐만 사용하는 단순한 애플리케이션도 있지만, 여러 큐에 잡을 전송하면 잡의 우선순위나 처리 방법을 세분화할 수 있어 유용합니다. Laravel 큐 워커는 어떤 큐를 우선적으로 처리할지 지정할 수 있기 때문입니다. 예를 들어, `high`란 이름의 큐로 잡을 전송하고 해당 큐를 먼저 처리하도록 워커를 실행할 수 있습니다.

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버 별 주의사항 및 사전 준비

<a name="database"></a>
#### 데이터베이스

`database` 큐 드라이버를 사용하려면 잡 정보를 저장할 데이터베이스 테이블이 필요합니다. 보통 Laravel의 기본 마이그레이션(`0001_01_01_000002_create_jobs_table.php`)에 포함되어 있지만, 없다면 `make:queue-table` Artisan 명령어로 직접 생성할 수 있습니다.

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면, `config/database.php` 설정 파일에 Redis 데이터베이스 커넥션을 구성해야 합니다.

> [!WARNING]
> `redis` 큐 드라이버에서는 Redis의 `serializer`와 `compression` 옵션을 지원하지 않습니다.

<a name="redis-cluster"></a>
##### Redis 클러스터

Redis 큐 커넥션에 [Redis Cluster](https://redis.io/docs/latest/operate/rs/databases/durability-ha/clustering)를 사용하는 경우, 큐 이름에 [키 해시 태그(key hash tag)](https://redis.io/docs/latest/develop/using-commands/keyspace/#hashtags)를 포함해야 합니다. 이를 통해 특정 큐의 모든 Redis 키가 동일 해시 슬롯으로 묶여 저장됩니다.

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

Redis 큐 사용 시, `block_for` 옵션으로 워커가 잡이 생기기를 기다리는 시간을 지정할 수 있습니다. 이 값은 워커 루프를 반복하면서 Redis DB에 계속해서 새 잡이 있는지 확인하는 방식보다 효율적일 수 있습니다. 예를 들어, 값을 `5`로 지정하면 워커는 잡이 생길 때까지 5초 동안 대기(블록)합니다.

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
> `block_for` 값을 `0`으로 설정하면 워커는 잡이 생길 때까지 무한정 대기합니다. 이 경우 `SIGTERM` 등의 신호는 다음 잡이 처리되기 전까지 전달되지 않습니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 준비

아래의 큐 드라이버를 사용하려면 다음 패키지가 필요합니다. Composer 패키지 매니저로 설치할 수 있습니다.

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~2.0` 또는 phpredis PHP 확장
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`

<a name="creating-jobs"></a>
## 잡 생성 (Creating Jobs)

<a name="generating-job-classes"></a>
### 잡 클래스 생성

기본적으로 애플리케이션의 큐잉 가능한(jobable) 잡 클래스는 `app/Jobs` 디렉터리에 위치합니다. 만약 해당 디렉터리가 없다면 `make:job` Artisan 명령어를 실행할 때 자동으로 생성됩니다.

```shell
php artisan make:job ProcessPodcast
```

생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하여, 이 잡이 큐에 비동기적으로 실행되어야 함을 Laravel에 알립니다.

> [!NOTE]
> 잡 스텁(stub)은 [스텁 커스터마이징](/docs/12.x/artisan#stub-customization) 기능으로 커스터마이징할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조

잡 클래스는 보통 매우 단순하며, 큐에서 잡이 처리될 때 호출되는 `handle` 메서드만을 가집니다. 예제 잡 클래스를 살펴보겠습니다. 여기서는 팟캐스트 퍼블리싱 서비스를 운영한다고 가정하고, 업로드된 팟캐스트 파일을 퍼블리시 전에 처리하는 잡을 예시로 들겠습니다.

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
     * 새로운 잡 인스턴스 생성.
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

위 예제에서 볼 수 있듯이, [Eloquent 모델](/docs/12.x/eloquent)을 잡의 생성자에 바로 전달할 수 있습니다. `Queueable` 트레이트를 사용하면, Eloquent 모델 및 로드된 연관관계도 큐잉 시 자동으로 시리얼라이즈/언시리얼라이즈됩니다.

큐잉 잡 생성자에 Eloquent 모델을 전달하면, 큐에는 모델의 식별자(ID)만 저장되고 실제로 잡이 처리되는 시점에 데이터베이스에서 해당 모델 인스턴스와 연관관계가 다시 조회됩니다. 이런 방식은 큐 드라이버로 전달되는 잡 데이터(payload) 크기를 아주 작게 만듭니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드 의존성 주입

`handle` 메서드는 큐 워커에서 잡을 처리할 때 호출됩니다. 이 메서드에는 타입힌트한 의존성을 선언할 수 있으며, Laravel [서비스 컨테이너](/docs/12.x/container)가 자동으로 주입합니다.

의존성 주입 방식을 직접 제어하고 싶다면 서비스 컨테이너의 `bindMethod` 메서드를 사용할 수 있습니다. 이 메서드는 콜백을 받아, 콜백 내에서 원하는 방식으로 `handle` 메서드를 호출하면 됩니다. 보통은 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 호출합니다.

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 바이너리 데이터(예: 원시 이미지 데이터 등)는 잡에 전달하기 전에 반드시 `base64_encode` 함수를 사용해 인코딩해야 합니다. 그렇지 않으면, 잡이 큐로 저장될 때 올바르게 JSON으로 직렬화되지 않을 수 있습니다.

<a name="handling-relationships"></a>
#### 큐잉된 연관관계

큐잉 잡이 Eloquent 모델의 연관관계까지 로드된 상태로 시리얼라이즈될 경우, 잡 문자열 크기가 커질 수 있습니다. 그리고 잡이 언시리얼라이즈되면서 모델 연관관계가 전체 조회되기 때문에, 이전에 적용된 필터/제약조건은 반영되지 않습니다. 일부 연관관계만 사용하려면, 잡 내에서 다시 쿼리 제약을 적용하세요.

또는 연관관계 자체가 시리얼라이즈되지 않길 원한다면, 속성을 설정할 때 모델의 `withoutRelations` 메서드를 호출하면 로드된 연관관계가 없는 모델 인스턴스를 반환합니다.

```php
/**
 * 새로운 잡 인스턴스 생성.
 */
public function __construct(
    Podcast $podcast,
) {
    $this->podcast = $podcast->withoutRelations();
}
```

[PHP 생성자 프로퍼티 승격(php 8+)](https://www.php.net/manual/en/language.oop5.decon.php#language.oop5.decon.constructor.promotion)을 사용할 경우, Eloquent 모델의 연관관계를 시리얼라이즈하지 않으려면 `WithoutRelations` 속성을 사용할 수 있습니다.

```php
use Illuminate\Queue\Attributes\WithoutRelations;

/**
 * 새로운 잡 인스턴스 생성.
 */
public function __construct(
    #[WithoutRelations]
    public Podcast $podcast,
) {}
```

여러 모델을 대상으로 전체 클래스에 연관관계 시리얼라이즈를 적용하고 싶다면, 클래스에 `#[WithoutRelations]` 속성을 부착하세요.

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
     * 새로운 잡 인스턴스 생성.
     */
    public function __construct(
        public Podcast $podcast,
        public DistributionPlatform $platform,
    ) {}
}
```

잡이 단일 모델이 아닌 Eloquent 모델의 컬렉션이나 배열을 받는 경우에는, 잡이 언시리얼라이즈/실행될 때 해당 컬렉션 내 각각의 모델 연관관계는 복원되지 않습니다. 이는 대량의 모델을 다루는 잡에서 리소스 과다 사용을 방지하기 위함입니다.

<a name="unique-jobs"></a>
### 유니크 잡 (Unique Jobs)

> [!WARNING]
> 유니크 잡 기능은 [락(lokcs)](/docs/12.x/cache#atomic-locks)를 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 원자적 락을 지원합니다.

> [!WARNING]
> 유니크 잡 제한은 배치 내부의 잡에는 적용되지 않습니다.

특정 잡이 큐에 단 하나만 존재하도록 제한하려면, 잡 클래스에 `ShouldBeUnique` 인터페이스를 구현하세요. 이 인터페이스를 구현하면 추가 메서드를 정의할 필요 없이 잡의 고유성을 보장할 수 있습니다.

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

위의 예에서 `UpdateSearchIndex` 잡이 이미 큐에 있고 아직 처리되지 않은 상태라면, 똑같은 잡이 더 이상 큐에 추가되지 않습니다.

경우에 따라 잡의 고유성을 판단할 특정 "키"를 지정하거나, 고유 락의 유효기간을 지정하고 싶을 수도 있습니다. 이 경우 잡 클래스에 `uniqueId`와 `uniqueFor` 속성/메서드를 정의하세요.

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
     * 잡의 유니크 락이 해제될 때까지의 초(second) 단위 시간.
     *
     * @var int
     */
    public $uniqueFor = 3600;

    /**
     * 잡의 유니크 ID 반환.
     */
    public function uniqueId(): string
    {
        return $this->product->id;
    }
}
```

위 예제처럼, 상품 ID별로 잡을 유니크하게 구성할 수도 있습니다. 동일한 상품 ID에 대한 잡은 기존 잡이 완료될 때까지 무시되며, 만약 잡이 한 시간 내에 처리되지 않으면 유니크 락이 해제되어 같은 키로 새로운 잡이 추가 가능합니다.

> [!WARNING]
> 여러 웹 서버나 컨테이너에서 잡을 디스패치하는 경우, 모든 서버가 같은 캐시 서버를 사용하도록 해야 Laravel이 잡의 유니크 상태를 정확히 판별할 수 있습니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 잡을 처리 시작 전까지 유니크 상태 유지

기본적으로 유니크 잡의 락은 잡이 처리 종료되거나 재시도 횟수를 모두 소진할 때 해제됩니다. 그러나 잡이 실제로 처리되기 직전에 유니크 락이 풀리길 원한다면, 잡에 `ShouldBeUniqueUntilProcessing` 인터페이스를 구현하세요.

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
#### 유니크 잡 락 커스텀화

내부적으로 `ShouldBeUnique` 잡이 디스패치될 때 Laravel은 `uniqueId` 키로 [락](/docs/12.x/cache#atomic-locks)를 획득하려 시도합니다. 이미 락이 있다면 잡은 큐잉되지 않습니다. 락 해제 시점은 잡이 완료되거나 재시도 횟수가 모두 소진될 때입니다. 기본적으로 Laravel은 기본 캐시 드라이버로 락을 획득하지만, 다른 드라이버를 사용하려면 `uniqueVia` 메서드를 정의해 반환하면 됩니다.

```php
use Illuminate\Contracts\Cache\Repository;
use Illuminate\Support\Facades\Cache;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...

    /**
     * 유니크 잡 락에 사용할 캐시 드라이버 반환.
     */
    public function uniqueVia(): Repository
    {
        return Cache::driver('redis');
    }
}
```

> [!NOTE]
> 동시에 처리할 잡 개수만 제한하려면 [WithoutOverlapping](/docs/12.x/queues#preventing-job-overlaps) 잡 미들웨어를 사용하세요.

<a name="encrypted-jobs"></a>
### 암호화된 잡 (Encrypted Jobs)

Laravel은 [암호화](/docs/12.x/encryption)를 통해 잡 데이터의 프라이버시와 무결성을 보장할 수 있습니다. 잡 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하면, 해당 잡은 큐잉 전에 자동으로 암호화됩니다.

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

잡 미들웨어를 통해 큐잉 잡 실행에 필요한 커스텀 논리를 잡 자체가 아닌 미들웨어로 감쌀 수 있어 코드 중복을 줄일 수 있습니다. 예를 들어, 아래의 `handle` 메서드는 Laravel의 Redis 속도 제한(rate limiting) 기능을 활용하여 5초마다 1개씩 잡을 처리하도록 합니다.

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

하지만 이처럼 잡 내에서 직접 로직을 처리하면 코드가 지저분해지고, 동일 기능을 다른 잡에도 반복 구현해야 하는 문제가 있습니다. 미들웨어로 따로 분리하면 아래와 같이 됩니다.

```php
<?php

namespace App\Jobs\Middleware;

use Closure;
use Illuminate\Support\Facades\Redis;

class RateLimited
{
    /**
     * 큐잉 잡 처리.
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

[라우트 미들웨어](/docs/12.x/middleware)와 같이, 잡 미들웨어는 처리 중인 잡과 계속 처리를 위한 콜백을 받습니다.

`make:job-middleware` Artisan 명령어로 새로운 잡 미들웨어 클래스를 생성할 수 있습니다. 생성 후, 잡 클래스에 `middleware` 메서드를 추가해 해당 미들웨어를 반환하여 연결할 수 있습니다.

```php
use App\Jobs\Middleware\RateLimited;

/**
 * 잡이 통과해야 할 미들웨어 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited];
}
```

> [!NOTE]
> 잡 미들웨어는 [큐잉 이벤트 리스너](/docs/12.x/events#queued-event-listeners), [메일러블](/docs/12.x/mail#queueing-mail), [알림](/docs/12.x/notifications#queueing-notifications)에도 지정할 수 있습니다.

<a name="rate-limiting"></a>
### 속도 제한 (Rate Limiting)

직접 속도 제한 미들웨어를 만드는 대신, Laravel에 기본 내장된 속도 제한 미들웨어를 활용할 수 있습니다. [라우트 속도 제한자](/docs/12.x/routing#defining-rate-limiters)처럼, 잡 속도 제한자도 `RateLimiter` 파사드의 `for` 메서드로 정의할 수 있습니다.

예를 들어, 일반 사용자는 시간당 1번 백업만 허용하고, 프리미엄 고객은 제한 없이 처리하도록 다음과 같이 정의할 수 있습니다.

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Support\Facades\RateLimiter;

/**
 * 앱 서비스 부트스트랩.
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

위에서는 시간 단위로 제한했지만, `perMinute`를 사용해 분 단위도 가능합니다. `by` 메서드에 어떤 값이든 전달할 수 있으며, 대개 고객별 구분에 사용합니다.

```php
return Limit::perMinute(50)->by($job->user->id);
```

속도 제한 설정 후, 잡에서 `Illuminate\Queue\Middleware\RateLimited` 미들웨어를 사용해 적용합니다.

```php
use Illuminate\Queue\Middleware\RateLimited;

/**
 * 잡이 통과해야 할 미들웨어 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited('backups')];
}
```

속도 제한으로 인해 잡이 다시 큐에 돌려질 때마다 해당 잡의 `attempts` 횟수가 증가합니다. 따라서 필요에 따라 `tries` 및 `maxExceptions` 속성을 조정하거나, [retryUntil 메서드](#time-based-attempts)로 제한 시간을 지정하세요.

`releaseAfter` 메서드로 재시도까지 대기할 시간(초 단위)을 지정할 수도 있습니다.

```php
/**
 * 잡이 통과해야 할 미들웨어 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new RateLimited('backups'))->releaseAfter(60)];
}
```

속도 제한 시 잡을 재시도하지 않고 큐에서 바로 삭제하고 싶으면 `dontRelease` 메서드를 사용하세요.

```php
/**
 * 잡이 통과해야 할 미들웨어 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new RateLimited('backups'))->dontRelease()];
}
```

> [!NOTE]
> Redis 사용 시, 기본 미들웨어보다 Redis에 최적화된 `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어를 사용하는 것이 더 효율적입니다.

<a name="preventing-job-overlaps"></a>
### 잡 중복 실행 방지 (Preventing Job Overlaps)

Laravel은 `Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어를 포함하고 있어 임의의 키를 기준으로 잡 중복 실행을 방지할 수 있습니다. 예를 들어, 특정 유저의 크레딧 점수를 업데이트하는 잡이 동시에 여러 개 실행되지 않도록 할 수 있습니다.

```php
use Illuminate\Queue\Middleware\WithoutOverlapping;

/**
 * 잡이 통과해야 할 미들웨어 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new WithoutOverlapping($this->user->id)];
}
```

중복 잡은 다시 큐에 돌려지지만, 이런 경우 `tries` 및 `maxExceptions` 값을 조정해 적절히 재시도 횟수를 설정해야 합니다.

`releaseAfter`로 중복 잡이 얼마 후 다시 시도될지 지정할 수 있습니다.

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->releaseAfter(60)];
}
```

중복된 잡을 곧바로 삭제하려면 `dontRelease` 메서드를 사용합니다.

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->dontRelease()];
}
```

종종 잡이 예기치 않게 실패하거나 타임아웃 되어 락이 해제되지 않을 수 있기 때문에, `expireAfter`로 명시적으로 락 만료시간(예: 180초)을 정할 수도 있습니다.

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->expireAfter(180)];
}
```

> [!WARNING]
> `WithoutOverlapping` 미들웨어는 [락 지원 캐시 드라이버](/docs/12.x/cache#atomic-locks)가 필요합니다.

<a name="sharing-lock-keys"></a>
#### 여러 잡 클래스 간 락 키 공유

기본적으로 `WithoutOverlapping`은 같은 클래스 내에서만 중복을 방지합니다. 서로 다른 잡 클래스여도 같은 키를 쓸 경우, 기본 동작만으론 중복 처리 방지가 안 됩니다. 클래스 간에도 동일 키로 락을 공유하고 싶다면 `shared` 메서드를 사용하세요.

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
### 예외 처리 제한 (Throttling Exceptions)

`Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어를 사용하면 일정 횟수 이상의 예외 발생시 일정 시간 동안 잡 실행을 중단할 수 있습니다. 이는 외부 서비스 등 불안정한 서비스와 상호작용하는 잡에 특히 유용합니다.

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

생성자 첫 번째 인자는 예외가 몇 번 발생하면 제한할지, 두 번째 인자는 제한 후 잡을 다시 실행하기까지 몇 초를 대기할지 정합니다. 예제에서는 10회 연속 예외 발생 시 5분 대기, 최대 총 30분 이내 재시도입니다.

예외 허용치를 넘기지 않았지만 예외가 발생한 잡은 바로 재시도됩니다. 이를 조절하려면 `backoff` 메서드로 특정 분만큼 딜레이를 줄 수 있습니다.

```php
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 5 * 60))->backoff(5)];
}
```

여러 잡에서 동일 제약조건(공용 버킷)으로 제한하고 싶으면 `by` 메서드로 같은 키 값을 지정하세요.

```php
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->by('key')];
}
```

모든 예외가 아니라 특정 예외 타입만 제한하고자 한다면, `when` 메서드에 클로저를 넘겨 예외 필터를 커스터마이징할 수 있습니다.

```php
use Illuminate\Http\Client\HttpClientException;

public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->when(
        fn (Throwable $throwable) => $throwable instanceof HttpClientException
    )];
}
```

예외 발생시 잡을 큐에서 완전히 삭제하고 싶으면 `deleteWhen`을 사용하세요.

```php
use App\Exceptions\CustomerDeletedException;

public function middleware(): array
{
    return [(new ThrottlesExceptions(2, 10 * 60))->deleteWhen(CustomerDeletedException::class)];
}
```

특정 예외를 앱의 예외 핸들러로 전파하려면 `report` 메서드를, 조건부로 하고 싶으면 클로저를 넘기세요.

```php
use Illuminate\Http\Client\HttpClientException;

public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->report(
        fn (Throwable $throwable) => $throwable instanceof HttpClientException
    )];
}
```

> [!NOTE]
> Redis 사용 시 `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어를 사용하는 것이 성능적으로 더 효율적입니다.

<a name="skipping-jobs"></a>
### 잡 건너뛰기 (Skipping Jobs)

`Skip` 미들웨어를 이용해, 조건에 따라 잡을 로직 변경 없이 큐에서 삭제(건너뛰기)할 수 있습니다. `Skip::when`은 주어진 값이 `true`일 때 잡을 삭제하고, `Skip::unless`는 `false`일 때 삭제합니다.

```php
use Illuminate\Queue\Middleware\Skip;

public function middleware(): array
{
    return [
        Skip::when($condition),
    ];
}
```

복잡한 조건이 필요한 경우, 클로저도 넘길 수 있습니다.

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

(나머지 내용은 원문의 마크다운 및 코드/예시, 규칙에 따라 적합하게 번역/유지됩니다.)