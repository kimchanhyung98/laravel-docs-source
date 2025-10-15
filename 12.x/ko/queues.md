# 큐 (Queues)

- [소개](#introduction)
    - [커넥션과 큐의 차이](#connections-vs-queues)
    - [드라이버 특이사항 및 필수 조건](#driver-prerequisites)
- [잡(Job) 생성](#creating-jobs)
    - [잡 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [유니크 잡](#unique-jobs)
    - [암호화된 잡](#encrypted-jobs)
- [잡 미들웨어](#job-middleware)
    - [속도 제한](#rate-limiting)
    - [잡 중첩 방지](#preventing-job-overlaps)
    - [예외 제한](#throttling-exceptions)
    - [잡 스킵(건너뛰기)](#skipping-jobs)
- [잡 디스패치(실행 요청)](#dispatching-jobs)
    - [디스패치 지연](#delayed-dispatching)
    - [동기식 디스패치](#synchronous-dispatching)
    - [잡과 데이터베이스 트랜잭션 연동](#jobs-and-database-transactions)
    - [잡 체이닝](#job-chaining)
    - [큐와 커넥션 커스터마이징](#customizing-the-queue-and-connection)
    - [최대 시도 횟수 / 타임아웃 값 지정](#max-job-attempts-and-timeout)
    - [SQS FIFO 및 페어 큐](#sqs-fifo-and-fair-queues)
    - [큐 페일오버](#queue-failover)
    - [에러 처리](#error-handling)
- [잡 배치(batch)](#job-batching)
    - [배치로 묶을 수 있는 잡 정의](#defining-batchable-jobs)
    - [배치 실행](#dispatching-batches)
    - [체인과 배치](#chains-and-batches)
    - [배치에 잡 추가](#adding-jobs-to-batches)
    - [배치 조회](#inspecting-batches)
    - [배치 취소](#cancelling-batches)
    - [배치 실패 처리](#batch-failures)
    - [배치 레코드 정리](#pruning-batches)
    - [DynamoDB에 배치 저장](#storing-batches-in-dynamodb)
- [클로저 큐잉](#queueing-closures)
- [큐 워커 실행](#running-the-queue-worker)
    - [`queue:work` 명령어](#the-queue-work-command)
    - [큐 우선순위](#queue-priorities)
    - [큐 워커 & 배포](#queue-workers-and-deployment)
    - [잡 만료 및 타임아웃](#job-expirations-and-timeouts)
- [Supervisor 설정](#supervisor-configuration)
- [실패한 잡 다루기](#dealing-with-failed-jobs)
    - [실패한 잡 정리](#cleaning-up-after-failed-jobs)
    - [실패한 잡 재시도](#retrying-failed-jobs)
    - [없는 모델 무시하기](#ignoring-missing-models)
    - [실패한 잡 레코드 정리](#pruning-failed-jobs)
    - [실패한 잡 DynamoDB에 저장](#storing-failed-jobs-in-dynamodb)
    - [실패한 잡 저장 비활성화](#disabling-failed-job-storage)
    - [실패한 잡 이벤트](#failed-job-events)
- [큐에서 잡 비우기](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [일부 잡만 페이크 처리](#faking-a-subset-of-jobs)
    - [잡 체인 테스트](#testing-job-chains)
    - [잡 배치 테스트](#testing-job-batches)
    - [잡/큐 상호작용 테스트](#testing-job-queue-interactions)
- [잡 이벤트](#job-events)

<a name="introduction"></a>
## 소개 (Introduction)

웹 애플리케이션을 개발할 때 업로드된 CSV 파일을 파싱하고 저장하는 작업처럼, 일반 웹 요청 처리 중 수행하기엔 시간이 오래 걸리는 작업이 있을 수 있습니다. Laravel은 이러한 작업을 쉽게 백그라운드에서 처리할 수 있도록 큐에 잡을 생성할 수 있게 도와줍니다. 시간 소모가 많은 작업을 큐로 분리하면, 애플리케이션은 빠르게 웹 요청에 응답할 수 있으며, 사용자 경험도 크게 향상됩니다.

Laravel의 큐는 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 또는 관계형 데이터베이스 등 다양한 백엔드 큐 시스템에 대해 통합된 큐 API를 제공합니다.

큐 관련 설정은 애플리케이션의 `config/queue.php` 파일에 저장되어 있습니다. 이 파일에는 프레임워크가 제공하는 각 큐 드라이버(데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 등)와 개발/테스트용으로 잡이 즉시 실행되는 동기식 드라이버, 그리고 큐에 디스패치되는 잡을 무시하는 `null` 드라이버의 커넥션 설정이 포함되어 있습니다.

> [!NOTE]
> Laravel Horizon은 Redis 기반 큐를 위한 뛰어난 대시보드 및 설정 시스템입니다. 자세한 내용은 [Horizon 공식 문서](/docs/12.x/horizon)를 참고하세요.

<a name="connections-vs-queues"></a>
### 커넥션과 큐의 차이

Laravel 큐를 사용하기 전에, "커넥션(connection)"과 "큐(queue)"의 차이를 명확히 이해하는 것이 중요합니다. `config/queue.php` 파일에는 `connections`라는 배열 설정이 있습니다. 이 옵션은 Amazon SQS, Beanstalk, Redis와 같은 백엔드 큐 서비스와의 연결을 정의합니다. 그러나 하나의 큐 커넥션에도 여러 개의 "큐"가 존재할 수 있으며, 각각은 잡이 쌓이는 서로 다른 스택 또는 그룹으로 생각할 수 있습니다.

각 커넥션 설정 예제에는 `queue` 속성이 포함되어 있는데, 이것이 해당 커넥션에서 디스패치되는 잡이 기본적으로 쌓일 큐를 의미합니다. 즉, 특정 큐를 명시하지 않고 잡을 디스패치하면, 커넥션 설정의 `queue` 속성에 정의된 큐에 배치됩니다:

```php
use App\Jobs\ProcessPodcast;

// 이 잡은 기본 커넥션의 기본 큐로 전송됩니다...
ProcessPodcast::dispatch();

// "emails" 큐로 잡을 명시적으로 설정하는 경우...
ProcessPodcast::dispatch()->onQueue('emails');
```

애플리케이션에 하나의 큐만 두고 단순하게 운영해도 문제가 없을 수 있습니다. 하지만 여러 큐를 활용함으로써 잡 처리의 우선순위나 세분화된 관리가 가능해집니다. 예를 들어, `high` 큐에 잡을 밀어놓고 해당 큐에 작업자를 우선할당하여 더 높은 처리 우선순위를 관리할 수 있습니다:

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버 특이사항 및 필수 조건

<a name="database"></a>
#### 데이터베이스

`database` 큐 드라이버를 사용하려면 잡을 저장할 데이터베이스 테이블이 필요합니다. 일반적으로 Laravel 기본 마이그레이션에는 `0001_01_01_000002_create_jobs_table.php` [마이그레이션](/docs/12.x/migrations)이 포함되어 있지만, 없다면 `make:queue-table` Artisan 명령어를 통해 생성할 수 있습니다:

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면 `config/database.php` 설정 파일에서 Redis 데이터베이스 커넥션을 구성해야 합니다.

> [!WARNING]
> `redis` 큐 드라이버에서는 Redis의 `serializer` 및 `compression` 옵션을 지원하지 않습니다.

<a name="redis-cluster"></a>
##### Redis 클러스터

만약 Redis 큐 커넥션이 [Redis Cluster](https://redis.io/docs/latest/operate/rs/databases/durability-ha/clustering)를 사용한다면, 큐 이름에는 [키 해시태그(key hash tag)](https://redis.io/docs/latest/develop/using-commands/keyspace/#hashtags)를 반드시 포함해야 합니다. 이를 통해 동일 큐에 속한 모든 Redis 키가 동일 해시 슬롯에 저장될 수 있습니다:

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

Redis 큐를 사용할 때, `block_for` 옵션을 적용하면 잡을 기다리는 동안 워커 반복 루프를 중단하고 Redis 데이터베이스를 재폴링하기 전에 얼마나 대기할지 설정할 수 있습니다.

큐 대기 상황에 맞게 이 값을 조정하면 매번 잡을 폴링하는 것보다 효율적일 수 있습니다. 예를 들어, 값을 `5`로 설정하면 잡이 대기열에 도착할 때까지 5초간 블록(block) 됩니다:

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
> `block_for`를 `0`으로 설정하면 잡이 도착할 때까지 워커가 무한정 블록됩니다. 이로 인해 `SIGTERM`과 같은 시그널도 다음 잡이 처리될 때까지 수신하지 못할 수 있습니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 필수 패키지

아래 큐 드라이버 별로 필요한 Composer 패키지 목록입니다:

<div class="content-list" markdown="1">

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~2.0` 또는 phpredis PHP 확장 모듈
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`

</div>

<a name="creating-jobs"></a>
## 잡(Job) 생성

<a name="generating-job-classes"></a>
### 잡 클래스 생성

기본적으로 애플리케이션의 큐잉 가능한 잡 클래스는 `app/Jobs` 디렉터리에 저장됩니다. 해당 디렉터리가 없으면 `make:job` Artisan 명령어 실행 시 자동으로 생성됩니다:

```shell
php artisan make:job ProcessPodcast
```

생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하게 되며, 이를 통해 Laravel은 해당 잡을 큐에 올려 비동기적으로 처리합니다.

> [!NOTE]
> 잡 생성용 스텁은 [스텁 커스터마이징](/docs/12.x/artisan#stub-customization)을 통해 원하는 대로 변경할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조

잡 클래스는 일반적으로 매우 단순하며, 큐에서 실행될 때 호출되는 `handle` 메서드만 포함하는 경우가 많습니다. 예를 들어 팟캐스트 파일을 업로드하고 퍼블리시 전에 처리해야 하는 상황을 가정해보겠습니다:

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

여기서 [Eloquent 모델](/docs/12.x/eloquent)을 잡 생성자에 직접 전달할 수 있었습니다. `Queueable` 트레이트를 사용하면 모델과 로드된 연관관계도 큐에 안전하게 직렬화/역직렬화됩니다.

큐잉된 잡의 생성자에서 Eloquent 모델을 받을 경우, 큐에는 오직 모델 식별자만 직렬화됩니다. 실제로 잡이 실행될 때 큐 시스템은 모델 전체와 해당 로드된 연관관계를 데이터베이스에서 다시 조회합니다. 이 직렬화 방식은 큐로 전송되는 데이터의 양을 최소화할 수 있습니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드의 의존성 주입

큐에서 잡 실행 시 `handle` 메서드가 호출되며, 여기에 타입힌트를 사용해 필요한 의존성을 주입받을 수 있습니다. Laravel [서비스 컨테이너](/docs/12.x/container)는 이 의존성 주입을 자동으로 처리합니다.

만약 컨테이너가 `handle` 메서드에 의존성을 주입하는 방식을 완전히 제어하고 싶다면, 컨테이너의 `bindMethod` 메서드를 이용할 수 있습니다. `bindMethod`는 잡과 컨테이너를 인자로 받는 콜백을 지정하며, 직접 `handle` 메서드 호출 방식을 정의할 수 있습니다. 주로 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 이 설정을 추가합니다:

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 이진 데이터(예: 원시 이미지 컨텐츠 등)는 잡에 전달하기 전에 반드시 `base64_encode` 함수를 통해 인코딩해야 합니다. 그렇지 않으면 큐에 잡을 보낼 때 JSON 직렬화에 실패할 수 있습니다.

<a name="handling-relationships"></a>
#### 큐잉된 연관관계(관계) 모델

로딩된 모든 Eloquent 모델의 연관관계도 잡과 함께 직렬화되므로, 잡 직렬화 문자열이 매우 클 수 있습니다. 뿐만 아니라, 잡 직렬화 이후에 모델 연관관계에 별도의 조건이 있었다면 잡을 역직렬화할 때 해당 조건은 유지되지 않고 전체 관계가 로드됩니다. 따라서 특정 서브셋만 다루고 싶다면 잡 내에서 연관관계 재제약 작업이 필요합니다.

직렬화 시 연관관계를 포함하지 않으려면 모델의 속성에 값을 설정할 때 `withoutRelations` 메서드를 사용하세요. 이 메서드는 관계를 제거한 모델 인스턴스를 반환합니다:

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

[PHP 생성자 프로퍼티 프로모션](https://www.php.net/manual/en/language.oop5.decon.php#language.oop5.decon.constructor.promotion)을 사용하는 경우, Eloquent 모델에서 연관관계를 직렬화하지 않으려면 `WithoutRelations` 어트리뷰트를 사용할 수 있습니다:

```php
use Illuminate\Queue\Attributes\WithoutRelations;

public function __construct(
    #[WithoutRelations]
    public Podcast $podcast,
) {}
```

보다 편리하게, 만약 모든 모델에서 관계를 제거한 채 직렬화하고 싶다면, 클래스 상단에 `WithoutRelations` 어트리뷰트를 부착하세요:

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

    public function __construct(
        public Podcast $podcast,
        public DistributionPlatform $platform,
    ) {}
}
```

만약 하나의 모델이 아닌 여러 Eloquent 모델의 컬렉션이나 배열을 잡에 전달하는 경우, 각 모델의 연관관계는 잡이 역직렬화되어 실행될 때 복원되지 않습니다. 이는 많은 수의 모델을 다루는 잡에서 과도한 리소스 사용을 방지하기 위함입니다.

<a name="unique-jobs"></a>
### 유니크 잡(Unique Jobs)

> [!WARNING]
> 유니크 잡은 [락을 지원하는](/docs/12.x/cache#atomic-locks) 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 원자적(atomic) 락을 지원합니다.

> [!WARNING]
> 유니크 잡 제약은 배치 내 잡에는 적용되지 않습니다.

특정 잡의 인스턴스가 한 번에 큐에 하나만 존재하도록 보장하고 싶다면, 잡 클래스에 `ShouldBeUnique` 인터페이스를 구현하면 됩니다. 별도의 메서드 구현 없이 제약 적용이 가능합니다:

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

위 예제처럼, `UpdateSearchIndex` 잡이 큐에 이미 존재(미처리)한다면, 동일한 잡은 또다시 디스패치되지 않습니다.

특정 조건(예: 특정 키)이나 제한 시간 등으로 유니크함을 관리하고 싶다면, 잡 클래스 내에 `uniqueId` 및 `uniqueFor` 속성 또는 메서드를 정의할 수 있습니다:

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
     * 유니크 락이 해제될 제한(초 단위).
     *
     * @var int
     */
    public $uniqueFor = 3600;

    /**
     * 잡에 대한 유니크 ID 반환
     */
    public function uniqueId(): string
    {
        return $this->product->id;
    }
}
```

위 예제에서처럼, 잡은 상품 ID를 기준으로 유니크하게 동작합니다. 동일한 상품 ID로 새로운 잡을 디스패치하면, 기존 잡이 처리 완료되기 전까지 무시됩니다. 또한, 기존 잡이 1시간 내에 처리되지 않으면 락이 해제되고 동일한 키의 잡을 다시 큐에 등록할 수 있습니다.

> [!WARNING]
> 여러 웹서버 또는 컨테이너에서 잡을 디스패치할 경우, 반드시 모든 서버가 동일한 중앙 캐시 서버와 통신하도록 설정해야 유니크 잡이 올바로 동작합니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 잡의 유니크함을 처리 시작 시까지 유지하기

기본적으로 유니크 잡은 잡이 처리 완료되거나 모든 재시도 횟수를 소진한 경우 락이 해제됩니다. 하지만, 잡을 처리 시작 바로 직전에만 락을 해제하고 싶다면 `ShouldBeUnique` 대신 `ShouldBeUniqueUntilProcessing` 인터페이스를 구현합니다:

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
#### 유니크 잡 락의 동작

내부적으로 `ShouldBeUnique` 잡이 큐에 등록되면, Laravel은 `uniqueId` 값으로 [락](/docs/12.x/cache#atomic-locks)을 시도합니다. 이미 락이 잡혀 있으면 잡은 디스패치되지 않습니다. 이 락은 잡이 처리 완료되거나 모든 재시도를 마치면 해제됩니다. 기본적으로 Laravel의 기본 캐시 드라이버가 사용되지만, 별도의 드라이버를 사용하고 싶으면 `uniqueVia` 메서드를 구현하면 됩니다:

```php
use Illuminate\Contracts\Cache\Repository;
use Illuminate\Support\Facades\Cache;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...

    /**
     * 유니크 잡 락용 캐시 드라이버 반환
     */
    public function uniqueVia(): Repository
    {
        return Cache::driver('redis');
    }
}
```

> [!NOTE]
> 단순 동시 처리 개수를 제한하려면, [WithoutOverlapping](/docs/12.x/queues#preventing-job-overlaps) 잡 미들웨어를 사용하세요.

<a name="encrypted-jobs"></a>
### 암호화된 잡(Encrypted Jobs)

잡의 데이터 기밀성과 무결성을 보장해야 한다면 [암호화](/docs/12.x/encryption)를 적용할 수 있습니다. 잡 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하기만 하면, 이 잡은 큐에 올라가기 전에 자동으로 암호화됩니다:

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

잡 미들웨어를 이용하면 큐 잡 실행 전후에 맞춤 로직을 쉽게 추가해, 잡 클래스 내부의 반복 코드를 최소화할 수 있습니다. 예를 들어, Redis 속도 제한을 활용해 5초마다 한 건의 잡만 처리하도록 구현하려면 다음처럼 작성할 수 있습니다:

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

이 코드처럼 바로 사용할 수도 있지만, 잡 미들웨어를 통해 속도 제한 논리를 별도로 분리할 수 있습니다. 이렇게 하면 여러 잡에서 동일한 처리 방식을 재사용할 수 있고 잡 클래스가 더욱 깔끔해집니다:

```php
<?php

namespace App\Jobs\Middleware;

use Closure;
use Illuminate\Support\Facades\Redis;

class RateLimited
{
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

위 예제처럼 [라우트 미들웨어](/docs/12.x/middleware)와 마찬가지로 잡 미들웨어도 처리 대상 잡과 계속적 처리를 위한 콜백을 인자로 받습니다.

새 잡 미들웨어 클래스를 생성하려면 `make:job-middleware` Artisan 명령어를 사용하세요. 생성 후, 잡 클래스의 `middleware` 메서드에서 해당 미들웨어를 반환해 잡에 적용할 수 있습니다. 이 메서드는 기본적으로 생성된 잡에 없으니 직접 추가해야 합니다:

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
> 잡 미들웨어는 [큐잉된 이벤트 리스너](/docs/12.x/events#queued-event-listeners), [메일](/docs/12.x/mail#queueing-mail), [알림](/docs/12.x/notifications#queueing-notifications)에도 사용할 수 있습니다.

<a name="rate-limiting"></a>
### 속도 제한(Rate Limiting)

직접 속도 제한 미들웨어를 작성하지 않아도, Laravel에서는 이미 사용 가능한 속도 제한 미들웨어가 있습니다. [라우트 속도 제한](/docs/12.x/routing#defining-rate-limiters) 처럼, 잡 전용 속도 제한자를 `RateLimiter` 파사드의 `for` 메서드로 정의할 수 있습니다.

예를 들어, 일반 사용자는 시간당 백업을 1번만 할 수 있지만 VIP 고객은 제한이 없게 하려면 다음처럼 설정합니다. `AppServiceProvider`의 `boot` 메서드에서 아래 코드를 추가합니다:

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Support\Facades\RateLimiter;

public function boot(): void
{
    RateLimiter::for('backups', function (object $job) {
        return $job->user->vipCustomer()
            ? Limit::none()
            : Limit::perHour(1)->by($job->user->id);
    });
}
```

위 예시는 시간 단위 제한이지만, `perMinute`를 사용하면 분 단위 제한도 가능합니다. `by` 메서드에는 제한 대상을 구분할 수 있는 임의의 값을 지정할 수 있으며, 보통 고객 ID 등으로 구분합니다:

```php
return Limit::perMinute(50)->by($job->user->id);
```

이제 `Illuminate\Queue\Middleware\RateLimited` 미들웨어를 적용하면, 제한 초과 시 제한 지속 시간에 맞춰 잡이 자동으로 다시 큐에 대기됩니다:

```php
use Illuminate\Queue\Middleware\RateLimited;

public function middleware(): array
{
    return [new RateLimited('backups')];
}
```

속도 제한으로 인해 잡이 다시 큐에 대기하면, 잡의 전체 시도 횟수(`attempts`)도 상승합니다. 따라서 잡 클래스에서 `tries` 및 `maxExceptions` 프로퍼티도 상황에 맞게 조정하거나, 잡이 시도될 최대 시간(`retryUntil` 메서드 참고)을 직접 정의할 수 있습니다.

`releaseAfter` 메서드로, 재시도까지 대기할 초 단위 값을 직접 지정할 수도 있습니다:

```php
public function middleware(): array
{
    return [(new RateLimited('backups'))->releaseAfter(60)];
}
```

잡이 속도 제한으로 인해 재시도되지 않게 하려면 `dontRelease` 메서드를 사용합니다:

```php
public function middleware(): array
{
    return [(new RateLimited('backups'))->dontRelease()];
}
```

> [!NOTE]
> Redis를 사용하는 경우, `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어를 사용하는 것이 훨씬 효율적입니다.

<a name="preventing-job-overlaps"></a>
### 잡 중첩 방지(Preventing Job Overlaps)

잡이 동시에 동일 리소스를 수정하면 안 될 때, Laravel의 `Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어를 사용해 임의의 키를 기준으로 중첩 처리를 막을 수 있습니다.

예를 들어, 사용자의 신용 점수를 업데이트하는 잡이 있을 때, 같은 사용자 ID에 대해 중첩 발생을 막으려면:

```php
use Illuminate\Queue\Middleware\WithoutOverlapping;

public function middleware(): array
{
    return [new WithoutOverlapping($this->user->id)];
}
```

중첩된 잡이 다시 큐로 이동하면 전체 시도 횟수도 증가합니다. 기본값으로 `tries`가 1이라면, 중첩된 잡은 재시도되지 않을 수 있으니 필요에 따라 값을 조정하세요.

중첩된 잡이 다시 시도되기까지 대기할 시간을 초 단위로 지정하려면 `releaseAfter` 메서드를 사용합니다:

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->releaseAfter(60)];
}
```

즉시 중첩 잡을 삭제하고 재시도하지 않으려면 `dontRelease` 메서드를 사용하세요:

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->dontRelease()];
}
```

`WithoutOverlapping` 미들웨어는 Laravel의 원자적 락 기능에 의존합니다. 잡이 예기치 않게 실패하거나 타임아웃이 발생할 경우 락이 해제되지 않을 수 있으므로, 락 만료 시간을 `expireAfter` 메서드로 직접 지정할 수 있습니다. 아래 예제는 3분 후 자동으로 락이 해제되게 설정한 예입니다:

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->expireAfter(180)];
}
```

> [!WARNING]
> 이 미들웨어는 [락을 지원하는](/docs/12.x/cache#atomic-locks) 캐시 드라이버에서만 동작합니다.

<a name="sharing-lock-keys"></a>
#### 여러 잡 클래스에서 락 키 공유

기본적으로 `WithoutOverlapping` 미들웨어는 동일 클래스의 잡만 중첩 방지합니다. 다른 잡 클래스 간에도 같은 락 키를 공유하여 중첩 방지도 가능하게 하려면 `shared` 메서드를 사용하세요:

```php
use Illuminate\Queue\Middleware\WithoutOverlapping;

class ProviderIsDown
{
    public function middleware(): array
    {
        return [
            (new WithoutOverlapping("status:{$this->provider}"))->shared(),
        ];
    }
}

class ProviderIsUp
{
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

Laravel은 `Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어를 통해 예외 발생 횟수에 따라 일정 시간 잡 실행을 지연시킬 수 있습니다. 특히 불안정한 외부 서비스와 상호작용하는 잡에 유용합니다.

예를 들어, 외부 API와 통신하는 잡이 예외를 계속 발생시키는 경우, `middleware` 메서드에서 `ThrottlesExceptions` 미들웨어를 반환하면, n번 예외 후 t초 대기하도록 할 수 있습니다. 다음 예는 시간 기반 재시도 제한도 함께 적용한 예입니다:

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

첫 번째 인자는 연속 예외 발생 최대 횟수, 두 번째는 예외 제한에 걸리면 얼마나 대기할지(초 단위)입니다.
예외 제한 전까지는 잡이 즉시 재시도되지만, `backoff`로 각 재시도 사이 대기 시간도 지정할 수 있습니다:

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 5 * 60))->backoff(5)];
}
```

내부적으로 캐시 시스템을 통해 제한이 관리됩니다. 미들웨어 적용 시 `by`로 별도의 키를 직접 지정할 수 있습니다. 여러 잡이 동일 외부 서비스를 사용할 때 같은 키를 지정하면 제한 버킷을 공유할 수 있습니다:

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->by('key')];
}
```

기본적으로 모든 예외가 제한에 포함되지만, `when` 메서드로 특정 예외만 제한에 포함할 수도 있습니다:

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

`when`과 달리, 조건에 해당하는 예외가 발생하면 잡을 완전히 삭제하려면 `deleteWhen`을 사용하세요:

```php
use App\Exceptions\CustomerDeletedException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [(new ThrottlesExceptions(2, 10 * 60))->deleteWhen(CustomerDeletedException::class)];
}
```

예외가 제한에 걸릴 때 앱의 예외 핸들러에 리포트하려면 `report`를, 조건부로 하려면 클로저를 넘기세요:

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
> Redis 사용 시에는 `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어를 사용하는 것이 더욱 효율적입니다.

<a name="skipping-jobs"></a>
### 잡 스킵(건너뛰기)

`Skip` 미들웨어를 사용하면 잡 로직을 수정하지 않고도 잡을 스킵(삭제)할 수 있습니다. `Skip::when`은 조건이 true면 잡을 삭제하고, `Skip::unless`는 false면 잡을 삭제합니다:

```php
use Illuminate\Queue\Middleware\Skip;

public function middleware(): array
{
    return [
        Skip::when($condition),
    ];
}
```

더 복잡한 조건식이 필요하다면, 클로저도 사용할 수 있습니다:

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

<a name="dispatching-jobs"></a>
## 잡 디스패치(실행 요청)

작성한 잡 클래스는 해당 클래스의 `dispatch` 메서드를 통해 큐에 디스패치할 수 있습니다. 전달하는 인수는 잡 생성자에 그대로 전달됩니다:

```php
<?php

namespace App\Http\Controllers;

use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    public function store(Request $request): RedirectResponse
    {
        $podcast = Podcast::create(/* ... */);

        // ...

        ProcessPodcast::dispatch($podcast);

        return redirect('/podcasts');
    }
}
```

조건부로 잡을 디스패치하려면 `dispatchIf` 또는 `dispatchUnless` 메서드를 사용할 수 있습니다:

```php
ProcessPodcast::dispatchIf($accountActive, $podcast);

ProcessPodcast::dispatchUnless($accountSuspended, $podcast);
```

신규 Laravel 프로젝트에서는 `database` 드라이버가 기본 큐 드라이버입니다. `config/queue.php` 파일에서 다른 드라이버를 지정할 수 있습니다.

<a name="delayed-dispatching"></a>
### 디스패치 지연(Delayed Dispatching)

잡을 바로 실행하지 않고 일정 시간 후에 처리되게 하려면, 디스패치 시 `delay` 메서드를 사용하세요. 예를 들어, 10분 후 잡을 처리하려면:

```php
<?php

namespace App\Http\Controllers;

use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
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

잡에 기본 지연시간이 설정된 경우, 이를 무시하고 즉시 처리하려면 `withoutDelay` 메서드를 사용하세요:

```php
ProcessPodcast::dispatch($podcast)->withoutDelay();
```

> [!WARNING]
> Amazon SQS 큐 서비스는 최대 15분까지만 지연 가능합니다.

<a name="dispatching-after-the-response-is-sent-to-browser"></a>
#### 브라우저에 응답 전송 후 잡 디스패치

[FastCGI](https://www.php.net/manual/en/install.fpm.php) 환경에서만 동작하지만, `dispatchAfterResponse` 메서드를 사용하면 HTTP 응답이 브라우저에 전송된 후 잡을 디스패치할 수 있습니다. 사용자는 즉시 응답을 받고, 잡은 응답 전송 후 짧은 작업(예: 이메일 발송)용으로 주로 활용합니다. 이렇게 디스패치된 잡은 HTTP 요청 내에서 실행되어 별도의 워커가 필요하지 않습니다:

```php
use App\Jobs\SendNotification;

SendNotification::dispatchAfterResponse();
```

클로저도 `dispatch`로 큐에 등록하고 `afterResponse`를 체이닝할 수 있습니다:

```php
use App\Mail\WelcomeMessage;
use Illuminate\Support\Facades\Mail;

dispatch(function () {
    Mail::to('taylor@example.com')->send(new WelcomeMessage);
})->afterResponse();
```

<a name="synchronous-dispatching"></a>
### 동기식 디스패치(Synchronous Dispatching)

잡을 큐에 등록하지 않고 즉시(동기식) 실행하려면 `dispatchSync`를 사용하면 됩니다. 이 경우 잡은 현재 프로세스에서 바로 실행됩니다:

```php
<?php

namespace App\Http\Controllers;

use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    public function store(Request $request): RedirectResponse
    {
        $podcast = Podcast::create(/* ... */);

        // ...

        ProcessPodcast::dispatchSync($podcast);

        return redirect('/podcasts');
    }
}
```

<a name="jobs-and-database-transactions"></a>
### 잡과 데이터베이스 트랜잭션

트랜잭션 내부에서 잡을 디스패치하는 것은 문제가 없지만, 잡 실행 시 트랜잭션이 커밋되었는지에 특별히 신경 써야 합니다. 때때로 잡이 큐 워커에 의해 처리될 때 트랜잭션이 아직 커밋되지 않았을 수 있기 때문입니다. 이럴 경우 트랜잭션 내에서 변경된 모델 데이터는 아직 데이터베이스에 반영되지 않았거나 새로 만든 레코드도 없을 수 있습니다.

이 문제를 쉽게 해결하기 위해, 큐 커넥션 설정 배열에서 `after_commit` 옵션을 활성화할 수 있습니다:

```php
'redis' => [
    'driver' => 'redis',
    // ...
    'after_commit' => true,
],
```

`after_commit` 옵션이 `true`이면 트랜잭션 내부에서 잡을 디스패치할 때, 트랜잭션이 커밋된 뒤에 실제로 잡이 디스패치됩니다. 열린 트랜잭션이 없다면, 잡은 즉시 디스패치됩니다.

트랜잭션 내에서 예외가 발생해 롤백이 되면, 해당 트랜잭션 내에서 디스패치된 잡도 삭제(큐에 등록되지 않음)됩니다.

> [!NOTE]
> `after_commit` 옵션을 `true`로 설정하면, 큐잉된 이벤트 리스너, 메일, 알림, 브로드캐스트 이벤트도 모두 열린 트랜잭션들이 커밋된 후에 디스패치됩니다.

<a name="specifying-commit-dispatch-behavior-inline"></a>
#### 커밋 후/전 디스패치 설정

`after_commit` 옵션을 전역적으로 설정하지 않고, 특정 잡만 커밋 이후에 디스패치하고 싶으면 `afterCommit` 메서드를 체인하면 됩니다:

```php
use App\Jobs\ProcessPodcast;

ProcessPodcast::dispatch($podcast)->afterCommit();
```

반대로, 전역적으로 `after_commit`이 활성화된 경우여도, 특정 잡만 커밋을 기다리지 않고 즉시 디스패치하려면 `beforeCommit`을 사용하세요:

```php
ProcessPodcast::dispatch($podcast)->beforeCommit();
```

<a name="job-chaining"></a>
### 잡 체이닝(Job Chaining)

잡 체이닝은 여러 개의 큐 잡을 순차적으로 실행하도록 할 수 있습니다. 각 잡이 성공적으로 실행되어야 다음 잡이 실행되며, 중간에 하나라도 실패하면 체인의 나머지 잡은 실행되지 않습니다. 체이닝은 `Bus` 파사드의 `chain` 메서드를 사용합니다:

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

잡 인스턴스뿐 아니라 클로저도 체인에 포함할 수 있습니다:

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
> 잡 내에서 `$this->delete()`로 잡을 삭제해도 다른 체인 잡의 실행은 중단되지 않습니다. 반드시 불완전한 예외 처리가 발생해야만 체인이 중단됩니다.

<a name="chain-connection-queue"></a>
#### 체인용 커넥션, 큐 지정

체인 내 잡이 실행될 커넥션과 큐를 지정하고 싶으면, `onConnection`, `onQueue` 메서드를 사용하세요. (잡에서 개별 지정한 경우 우선 적용됨)

```php
Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->onConnection('redis')->onQueue('podcasts')->dispatch();
```

<a name="adding-jobs-to-the-chain"></a>
#### 체인에 잡 추가

체인 내부 잡에서 해당 체인 앞/뒤에 잡을 추가(prepend/append)할 수도 있습니다:

```php
public function handle(): void
{
    // 현재 체인 앞에 추가, 다음 작업으로 즉시 실행
    $this->prependToChain(new TranscribePodcast);

    // 현재 체인 마지막에 추가
    $this->appendToChain(new TranscribePodcast);
}
```

<a name="chain-failures"></a>
#### 체인 실패 처리

체인 잡 중 하나라도 실패하면, `catch` 메서드에 전달한 클로저가 호출됩니다. 실패 원인은 `Throwable`로 전달됩니다:

```php
use Illuminate\Support\Facades\Bus;
use Throwable;

Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->catch(function (Throwable $e) {
    // 체인 속 잡 실패...
})->dispatch();
```

> [!WARNING]
> 체인 콜백도 잡과 마찬가지로 직렬화 후 실행되며, 이때 `$this` 키워드를 사용하지 않아야 합니다.

<a name="customizing-the-queue-and-connection"></a>
### 큐와 커넥션 커스터마이징

<a name="dispatching-to-a-particular-queue"></a>
#### 특정 큐로 디스패치

잡을 여러 큐로 분리해 우선순위를 다르게 운용할 수 있습니다. 이는 큐 커넥션 자체를 여러 개 쓰는 것이 아니라, 하나의 커넥션 내에서 특정 큐 이름에 잡을 올리는 것입니다. 아래처럼 `onQueue` 메서드로 지정합니다:

```php
<?php

namespace App\Http\Controllers;

use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    public function store(Request $request): RedirectResponse
    {
        $podcast = Podcast::create(/* ... */);

        ProcessPodcast::dispatch($podcast)->onQueue('processing');

        return redirect('/podcasts');
    }
}
```

잡 클래스 생성자 내에서 `onQueue`를 호출해 기본 큐를 정하는 것도 가능합니다:

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    public function __construct()
    {
        $this->onQueue('processing');
    }
}
```

<a name="dispatching-to-a-particular-connection"></a>
#### 특정 커넥션에 잡 디스패치

애플리케이션이 여러 큐 커넥션을 동시에 사용하는 경우, `onConnection` 메서드로 잡을 보낼 커넥션을 지정할 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    public function store(Request $request): RedirectResponse
    {
        $podcast = Podcast::create(/* ... */);

        ProcessPodcast::dispatch($podcast)->onConnection('sqs');

        return redirect('/podcasts');
    }
}
```

`onConnection`과 `onQueue`를 동시에 체이닝해 커넥션과 큐 이름을 모두 지정할 수 있습니다:

```php
ProcessPodcast::dispatch($podcast)
    ->onConnection('sqs')
    ->onQueue('processing');
```

잡 클래스 생성자에서 커넥션 지정도 가능합니다:

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    public function __construct()
    {
        $this->onConnection('sqs');
    }
}
```

<a name="max-job-attempts-and-timeout"></a>
### 최대 시도 횟수/타임아웃 값 지정

<a name="max-attempts"></a>
#### 최대 시도 횟수(Max Attempts)

Laravel 큐 시스템에서 잡의 시도 횟수는 핵심 기능 중 하나로, 여러 고급 동작의 기반이 됩니다. 다소 헷갈릴 수 있지만, 동작 원리를 이해하고 나면 잡을 안전하게 관리할 수 있습니다.

잡이 디스패치되면 큐에 쌓이고, 워커가 잡을 가져와 실행을 시도합니다. 이게 곧 "잡 시도"입니다.

단, "시도"는 꼭 `handle` 메서드 실행을 의미하지는 않으며, 아래 상황에도 시도가 소진될 수 있습니다:

<div class="content-list" markdown="1">

- 실행 중 예기치 않은 예외가 발생한 경우
- `$this->release()`로 수동 재시도 처리한 경우
- `WithoutOverlapping`/`RateLimited` 등 미들웨어로 락 실패 시 재시도
- 잡 처리 중 타임아웃 발생
- 잡의 `handle` 메서드가 예외 없이 실행 완료된 경우

</div>

무한 재시도가 아닌, 잡마다 최대 시도 횟수를 명확히 제한할 필요가 있습니다.

> [!NOTE]
> Laravel은 기본적으로 잡을 1회만 시도합니다. 미들웨어가 재시도를 유발하거나 직접 잡을 재등록하는 경우에는 적절히 `tries` 옵션을 조절해야 합니다.

가장 간단하게는 Artisan 명령에서 `--tries` 스위치로 전체 워커에 적용할 수 있습니다:

```shell
php artisan queue:work --tries=3
```

잡이 최대 시도 횟수를 초과하면, 해당 잡은 "실패"로 간주되어 [실패한 잡 처리 문서](#dealing-with-failed-jobs)에 따라 관리됩니다. `--tries=0`은 무한 재시도를 의미합니다.

좀 더 세밀하게, 잡 클래스 내에서 `$tries` 프로퍼티 값을 지정할 수 있습니다. 이 경우 명령어 인자의 값보다 우선 적용됩니다:

```php
<?php

namespace App\Jobs;

class ProcessPodcast implements ShouldQueue
{
    public $tries = 5;
}
```

상황 별로 동적으로 시도 횟수를 지정하고 싶으면, `tries` 메서드를 정의하세요:

```php
public function tries(): int
{
    return 5;
}
```

<a name="time-based-attempts"></a>
#### 시간 기반 시도 제한(Time Based Attempts)

몇 번이 아니라, 일정 시간까지만 잡을 재시도하게 하려면 `retryUntil` 메서드를 잡 클래스에 추가하세요. 반환값은 `DateTime` 인스턴스여야 합니다:

```php
use DateTime;

public function retryUntil(): DateTime
{
    return now()->addMinutes(10);
}
```

`retryUntil`과 `tries`가 모두 있다면, `retryUntil`(시간 기반) 정책이 우선 적용됩니다.

> [!NOTE]
> [큐잉된 이벤트 리스너](/docs/12.x/events#queued-event-listeners), [큐잉된 알림](/docs/12.x/notifications#queueing-notifications) 관련 클래스에도 동일하게 지정할 수 있습니다.

<a name="max-exceptions"></a>
#### 최대 예외 발생 횟수(Max Exceptions)

잡이 여러 번 시도되는 경우에도, 미들웨어 자체에서 release 하는 것이 아니라 잡 실행 중 실제 예외가 일정 횟수 이상 발생할 때 실패 처리할 수도 있습니다. 이때는 잡 클래스 내에 `maxExceptions` 프로퍼티를 선언하세요:

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;
use Illuminate\Support\Facades\Redis;

class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    public $tries = 25;

    public $maxExceptions = 3;

    public function handle(): void
    {
        Redis::throttle('key')->allow(10)->every(60)->then(function () {
            // 락 획득시 팟캐스트 처리...
        }, function () {
            // 락 획득 실패...
            return $this->release(10);
        });
    }
}
```

잡이 Redis 락을 획득하지 못하면 10초 후 다시 시도하며, 최대 25번 재시도하지만 예기치 않은 예외가 3회 발생하면 곧바로 실패로 처리됩니다.

<a name="timeout"></a>
#### 타임아웃(Timeout)

잡 실행 시간이 대략적으로 예측 가능하다면, "타임아웃" 값을 지정할 수 있습니다. 기본값은 60초이며, 이 시간보다 더 오래 걸리는 잡은 워커에서 에러와 함께 종료됩니다. 워커는 [서버에 설정된 프로세스 매니저](#supervisor-configuration)에 의해 자동 재시작될 수 있습니다.

타임아웃은 Artisan 명령어의 `--timeout` 스위치로 전체 워커에 일괄 적용할 수 있습니다:

```shell
php artisan queue:work --timeout=30
```

타임아웃으로 인해 잡이 계속 실패하면, 최대 시도 횟수를 넘길 때 실패 처리됩니다.

잡 클래스 내에 `$timeout` 숫자로 개별 지정도 할 수 있으며, 이 경우 명령어 인자보다 우선합니다:

```php
<?php

namespace App\Jobs;

class ProcessPodcast implements ShouldQueue
{
    public $timeout = 120;
}
```

외부 소켓/HTTP 요청 등 IO 블로킹 작업에는 해당 라이브러리의 API를 통해 별도의 타임아웃을 지정해야 합니다. 예를 들어 [Guzzle](https://docs.guzzlephp.org) 사용 시 별도 지정 필요.

> [!WARNING]
> [PCNTL](https://www.php.net/manual/en/book.pcntl.php) PHP 확장 모듈이 설치되어야 타임아웃이 작동합니다. 또한 타임아웃 값은 ["retry_after"](#job-expiration) 값보다 반드시 작아야 하며, 그렇지 않으면 잡이 중복 실행될 위험이 있습니다.

<a name="failing-on-timeout"></a>
#### 타임아웃 시 실패 처리

타임아웃 시 잡을 [실패](#dealing-with-failed-jobs)로 바로 간주하려면, 잡 클래스에 `$failOnTimeout` 프로퍼티를 true로 지정하세요:

```php
public $failOnTimeout = true;
```

> [!NOTE]
> 기본적으로 잡이 타임아웃되면 1회 시도가 소진되고 큐에 재등록(재시도 허용 시)됩니다. 하지만 실패로 처리하면, 더 이상 재시도되지 않습니다.

<a name="sqs-fifo-and-fair-queues"></a>
### SQS FIFO 및 페어 큐

Laravel은 [Amazon SQS FIFO(First-In-First-Out)](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-fifo-queues.html) 큐를 지원합니다. FIFO 큐는 등록한 순서대로 정확한 1회만 잡을 처리할 수 있게 메시지 중복 제거 기능을 제공합니다.

FIFO 큐는 "메시지 그룹 ID"를 요구합니다. ID가 같은 메시지는 순차적으로 처리되고, 다른 ID는 동시에 병렬 처리됩니다.

잡을 디스패치할 때 `onGroup` 메서드로 메시지 그룹 ID를 지정할 수 있습니다:

```php
ProcessOrder::dispatch($order)
    ->onGroup("customer-{$order->customer_id}");
```

정확한 1회 처리 보장을 위해 메시지 중복 제거 ID 지정이 필요한 경우, 잡 클래스에 `deduplicationId` 메서드를 구현하세요:

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ProcessSubscriptionRenewal implements ShouldQueue
{
    use Queueable;

    public function deduplicationId(): string
    {
        return "renewal-{$this->subscription->id}";
    }
}
```

<a name="fifo-listeners-mail-and-notifications"></a>
#### FIFO 리스너, 메일, 알림

FIFO 큐를 사용할 때 리스너, 메일, 알림에도 메시지 그룹 설정이 필요합니다. 또는, 이러한 객체들을 큐잉할 때 비-FIFO 큐로 보낼 수도 있습니다.

[큐잉된 이벤트 리스너](/docs/12.x/events#queued-event-listeners)는 `messageGroup` 메서드로 그룹을, 필요하다면 `deduplicationId`도 별도로 정의하세요:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;

class SendShipmentNotification
{
    public function messageGroup(): string
    {
        return "shipments";
    }

    public function deduplicationId(): string
    {
        return "shipment-notification-{$this->shipment->id}";
    }
}
```

[메일](/docs/12.x/mail)을 FIFO 큐로 보내려면, `onGroup`, `withDeduplicator` 메서드를 사용하세요:

```php
use App\Mail\InvoicePaid;
use Illuminate\Support\Facades\Mail;

$invoicePaid = (new InvoicePaid($invoice))
    ->onGroup('invoices')
    ->withDeduplicator(fn () => 'invoices-'.$invoice->id);

Mail::to($request->user())->send($invoicePaid);
```

[알림](/docs/12.x/notifications)도 동일하게 할 수 있습니다:

```php
use App\Notifications\InvoicePaid;

$invoicePaid = (new InvoicePaid($invoice))
    ->onGroup('invoices')
    ->withDeduplicator(fn () => 'invoices-'.$invoice->id);

$user->notify($invoicePaid);
```

<a name="queue-failover"></a>
### 큐 페일오버

`failover` 큐 드라이버는 잡을 큐에 보낼 때 자동으로 페일오버 기능을 제공합니다. 만약 첫 번째(Primary) 큐 커넥션이 어떤 이유로든 실패하면, Laravel은 목록에 설정된 다음 커넥션으로 자동 시도합니다. 고가용성이 필요한 프로덕션 환경에서 매우 유용합니다.

페일오버 큐 커넥션을 설정하려면, `failover` 드라이버와 함께 시도할 커넥션 이름 배열을 정의합니다. Laravel은 기본 제공 큐 설정 파일(`config/queue.php`)에 예제 설정을 포함하고 있습니다:

```php
'failover' => [
    'driver' => 'failover',
    'connections' => [
        'database',
        'sync',
    ],
],
```

설정 후, `.env` 파일에서 기본 큐 커넥션을 페일오버로 지정하면 됩니다:

```ini
QUEUE_CONNECTION=failover
```

<a name="error-handling"></a>
### 에러 처리

잡 처리 중 예외가 발생하면, 잡은 자동으로 큐에 다시 등록되고 재시도가 반복됩니다. 이 과정은 [최대 시도 횟수](#max-job-attempts-and-timeout)만큼 반복됩니다. 제한은 `queue:work` Artisan 명령어의 `--tries` 인자 또는 잡 클래스 내에서 지정할 수 있습니다. 자세한 워커 실행에 대한 내용은 [이하에서 확인]((#running-the-queue-worker))하세요.

<a name="manually-releasing-a-job"></a>
#### 잡 수동 재시도(Release)

가끔 잡을 수동으로 나중에 재시도하고 싶을 때, `release` 메서드를 호출하면 즉시 큐에 다시 등록됩니다:

```php
public function handle(): void
{
    // ...
    $this->release();
}
```

기본적으로 즉시 처리 대기열에 재등록되지만, 인수로 초 단위 또는 날짜 인스턴스를 전달해 특정 시간 후까지 대기시킬 수 있습니다:

```php
$this->release(10);

$this->release(now()->addSeconds(10));
```

<a name="manually-failing-a-job"></a>
#### 잡 수동 실패 처리

가끔 잡을 강제로 "실패"로 처리해야 할 경우 `fail` 메서드를 사용하세요:

```php
public function handle(): void
{
    // ...
    $this->fail();
}
```

예외 발생으로 인해 실패 처리할 경우, 예외 객체를, 간단한 에러 메시지를 넘기면 문자 메시지가 예외로 변환되어 저장됩니다:

```php
$this->fail($exception);

$this->fail('Something went wrong.');
```

> [!NOTE]
> 실패한 잡 관리에 대한 자세한 내용은 [실패한 잡 다루기 문서](#dealing-with-failed-jobs)를 참고하세요.

<a name="fail-jobs-on-exceptions"></a>
#### 특정 예외 발생 시 잡 실패 처리

`FailOnException` [잡 미들웨어](#job-middleware)는 특정 예외가 발생하면 즉시 잡을 실패 처리해, 일시적 외부 서비스 장애에는 재시도를 허용하고 권한 변경 등 영구적 오류엔 바로 실패 처리할 수 있습니다:

```php
<?php

namespace App\Jobs;

use App\Models\User;
use Illuminate\Auth\Access\AuthorizationException;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;
use Illuminate\Queue\Middleware\FailOnException;
use Illuminate\Support\Facades\Http;

class SyncChatHistory implements ShouldQueue
{
    use Queueable;

    public $tries = 3;

    public function __construct(
        public User $user,
    ) {}

    public function handle(): void
    {
        $this->user->authorize('sync-chat-history');

        $response = Http::throw()->get(
            "https://chat.laravel.test/?user={$this->user->uuid}"
        );

        // ...
    }

    public function middleware(): array
    {
        return [
            new FailOnException([AuthorizationException::class])
        ];
    }
}
```

<!-- 이하 생략: 문서 분량 초과로 인한 중단. 필요시 이어서 번역 및 출력 요청 가능. -->