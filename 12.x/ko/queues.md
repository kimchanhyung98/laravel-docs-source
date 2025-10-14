# 큐 (Queues)

- [소개](#introduction)
    - [커넥션과 큐의 차이](#connections-vs-queues)
    - [드라이버 특이사항 및 사전 준비](#driver-prerequisites)
- [잡 생성](#creating-jobs)
    - [잡 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [유니크 잡](#unique-jobs)
    - [암호화된 잡](#encrypted-jobs)
- [잡 미들웨어](#job-middleware)
    - [속도 제한](#rate-limiting)
    - [잡 중복 실행 방지](#preventing-job-overlaps)
    - [예외 쓰로틀링](#throttling-exceptions)
    - [잡 스킵하기](#skipping-jobs)
- [잡 디스패치하기](#dispatching-jobs)
    - [지연 디스패치](#delayed-dispatching)
    - [동기 디스패치](#synchronous-dispatching)
    - [잡과 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [잡 체이닝](#job-chaining)
    - [큐 및 커넥션 커스터마이징](#customizing-the-queue-and-connection)
    - [최대 시도 횟수 및 타임아웃 값 지정](#max-job-attempts-and-timeout)
    - [SQS FIFO 및 공정 큐](#sqs-fifo-and-fair-queues)
    - [큐 페일오버](#queue-failover)
    - [에러 핸들링](#error-handling)
- [잡 배치 처리](#job-batching)
    - [배치 가능한 잡 정의](#defining-batchable-jobs)
    - [배치 디스패치](#dispatching-batches)
    - [체인과 배치의 결합](#chains-and-batches)
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
- [Supervisor 설정](#supervisor-configuration)
- [실패한 잡 처리](#dealing-with-failed-jobs)
    - [실패한 잡 후처리](#cleaning-up-after-failed-jobs)
    - [실패한 잡 재시도](#retrying-failed-jobs)
    - [누락된 모델 무시](#ignoring-missing-models)
    - [실패한 잡 정리](#pruning-failed-jobs)
    - [DynamoDB에 실패한 잡 저장](#storing-failed-jobs-in-dynamodb)
    - [실패한 잡 저장 비활성화](#disabling-failed-job-storage)
    - [실패한 잡 이벤트](#failed-job-events)
- [큐에서 잡 제거](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [일부 잡만 페이크하기](#faking-a-subset-of-jobs)
    - [잡 체인 테스트](#testing-job-chains)
    - [잡 배치 테스트](#testing-job-batches)
    - [잡/큐 상호작용 테스트](#testing-job-queue-interactions)
- [잡 이벤트](#job-events)

<a name="introduction"></a>
## 소개 (Introduction)

웹 애플리케이션을 개발하다보면 업로드된 CSV 파일을 파싱해 저장하는 작업처럼 일반적인 웹 요청 처리 시간에 수행하기에는 너무 오래 걸리는 작업이 있을 수 있습니다. 다행히 Laravel에서는 큐를 활용해 백그라운드에서 처리할 수 있는 큐 잡(queued job)을 쉽게 만들 수 있습니다. 시간 소모가 큰 작업을 큐로 분리함으로써, 애플리케이션은 웹 요청에 훨씬 빠르게 응답할 수 있고, 사용자에게 더 나은 경험을 제공합니다.

Laravel 큐는 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io) 또는 일반 관계형 데이터베이스 등 여러 큐 백엔드에서 동일한 큐 API를 제공하며 이를 통합해 다룰 수 있게 해줍니다.

큐 관련 모든 설정 옵션은 애플리케이션의 `config/queue.php` 설정 파일에 저장되어 있습니다. 이 파일에는 데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 드라이버 등 다양한 큐 드라이버의 커넥션 설정이 포함되어 있습니다. 또한, 잡을 즉시 실행하는(테스트 혹은 개발용) 동기(동시) 드라이버와 큐에 들어온 잡을 그냥 폐기하는 `null` 드라이버도 기본 제공됩니다.

> [!NOTE]
> Laravel Horizon은 Redis 기반 큐를 위한 아름다운 대시보드 및 설정 시스템입니다. 더 자세한 내용은 [Horizon 문서](/docs/12.x/horizon)를 참고하세요.

<a name="connections-vs-queues"></a>
### 커넥션과 큐의 차이 (Connections vs. Queues)

Laravel 큐를 사용하기 전, "커넥션(connection)"과 "큐(queue)"의 차이를 이해하는 것이 중요합니다. `config/queue.php` 설정 파일에는 `connections`라는 배열 설정이 있습니다. 이 옵션은 Amazon SQS, Beanstalk, Redis 같은 백엔드 큐 서비스에 접속하는 커넥션 정보를 정의합니다. 그리고 특정 큐 커넥션은 여러 개의 "큐"를 가질 수 있어, 각기 다른 잡의 스택(묶음)처럼 활용할 수 있습니다.

각 커넥션의 설정 예제를 보면 `queue`라는 속성이 있습니다. 이는 해당 커넥션에서 잡이 디스패치될 때 기본으로 사용되는 큐를 뜻합니다. 즉, 잡을 디스패치할 때 별도로 큐를 지정하지 않으면, 커넥션 설정의 `queue` 속성에 명시된 큐에 잡이 쌓이게 됩니다:

```php
use App\Jobs\ProcessPodcast;

// 이 잡은 기본 커넥션의 기본 큐로 전송됩니다...
ProcessPodcast::dispatch();

// 이 잡은 기본 커넥션의 "emails" 큐로 전송됩니다...
ProcessPodcast::dispatch()->onQueue('emails');
```

몇몇 애플리케이션은 잡을 하나의 큐에만 쌓고 단순하게 운영할 수도 있습니다. 하지만 여러 개의 큐에 잡을 분산해서 넣는 것이 잡의 우선순위 지정이나 분류 처리가 필요한 경우에 특히 유용할 수 있습니다. Laravel 큐 워커는 처리 우선순위에 따라 어떤 큐를 먼저 처리할지 지정할 수 있기 때문입니다. 예를 들어, 우선순위가 높은 `high` 큐를 두고 잡을 보낸 다음, 아래와 같이 `high` 큐를 우선적으로 처리하게 워커를 돌릴 수 있습니다:

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버 특이사항 및 사전 준비 (Driver Notes and Prerequisites)

<a name="database"></a>
#### 데이터베이스

`database` 큐 드라이버를 사용하려면, 잡이 저장될 데이터베이스 테이블이 필요합니다. 보통은 Laravel의 기본 제공 마이그레이션(`0001_01_01_000002_create_jobs_table.php`)에 이 테이블이 포함되어 있습니다. 만약 애플리케이션에 이 마이그레이션이 없다면, 아래 Artisan 명령어로 직접 생성할 수 있습니다:

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면, `config/database.php` 설정 파일에 Redis 데이터베이스 커넥션을 추가해주어야 합니다.

> [!WARNING]
> `redis` 큐 드라이버는 Redis의 `serializer`와 `compression` 옵션을 지원하지 않습니다.

<a name="redis-cluster"></a>
##### Redis 클러스터

[Redis Cluster](https://redis.io/docs/latest/operate/rs/databases/durability-ha/clustering)를 사용하는 경우, 큐 이름에 [키 해시 태그](https://redis.io/docs/latest/develop/using-commands/keyspace/#hashtags)를 반드시 포함해야 합니다. 이는 해당 큐의 모든 Redis 키가 같은 해시 슬롯에 저장되도록 보장합니다:

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
##### 블로킹(대기)

Redis 큐에서는 `block_for` 옵션을 사용해, 워커 루프를 돌 때 몇 초 동안 잡이 대기 큐에 들어올 때까지 기다릴 것인지 설정할 수 있습니다.

큐에 쌓이는 잡의 양에 맞춰 이 값을 조정하면 Redis를 계속 폴링하는 비효율을 줄일 수 있습니다. 예를 들어, 이 값을 `5`로 하면, 잡이 올라올 때까지 최대 5초 동안 대기했다가 없으면 워커 루프를 다시 탑니다:

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
> `block_for` 옵션을 `0`으로 설정하면, 워커는 잡이 올 때까지 무한정(Indefinite) 대기합니다. 이 경우, `SIGTERM` 등 신호(signal)도 현재 잡이 처리될 때까지 무시됩니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 사전 준비

아래 드라이버를 사용하려면 각 드라이버 별로 필요한 패키지를 Composer로 설치해야 합니다:

<div class="content-list" markdown="1">

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~2.0` 또는 phpredis PHP 확장
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`

</div>

<a name="creating-jobs"></a>
## 잡 생성 (Creating Jobs)

<a name="generating-job-classes"></a>
### 잡 클래스 생성 (Generating Job Classes)

기본적으로 애플리케이션의 모든 큐 잡 클래스는 `app/Jobs` 디렉토리에 저장됩니다. 이 디렉토리가 없다면, `make:job` Artisan 명령어를 실행할 때 자동으로 생성됩니다:

```shell
php artisan make:job ProcessPodcast
```

생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하며, 이 인터페이스를 통해 Laravel은 해당 잡이 큐에 비동기적으로 추가되어야 함을 인식하게 됩니다.

> [!NOTE]
> 잡의 스텁 파일은 [스텁 퍼블리싱](/docs/12.x/artisan#stub-customization)을 통해 커스터마이즈할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조 (Class Structure)

일반적으로 잡 클래스는 매우 단순하며, 큐가 잡을 처리할 때 호출되는 `handle` 메서드만 포함합니다. 예를 들어, 팟캐스트 퍼블리싱 서비스를 운영하며 업로드된 파일을 처리해야 한다고 가정해 봅니다:

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
     * 새 잡 인스턴스 생성자
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

이 예시에서는 [Eloquent 모델](/docs/12.x/eloquent)을 생성자에 바로 전달할 수 있습니다. 잡에서 사용하는 `Queueable` 트레이트 덕분에, Eloquent 모델과 연결된 연관관계(relationships) 정보도 큐에 넣을 때 경량화되어 직렬화/비직렬화 처리됩니다.

잡 생성자에 Eloquent 모델을 전달하면, 모델의 식별자만 큐에 직렬화되어 저장됩니다. 큐가 잡을 실제로 처리할 때, 큐 시스템이 자동으로 데이터베이스에서 전체 모델 인스턴스와 연관관계를 다시 조회해 복원해줍니다. 이 방식은 큐로 보내는 데이터 크기를 최소화합니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드의 의존성 주입

`handle` 메서드는 큐 워커가 잡을 처리할 때 호출됩니다. `handle` 메서드의 파라미터에 타입힌트를 지정하면, Laravel의 [서비스 컨테이너](/docs/12.x/container)가 자동으로 의존성을 주입해줍니다.

컨테이너의 의존성 주입 방식을 세밀하게 제어하려면, 컨테이너의 `bindMethod` 메서드를 사용할 수 있습니다. 이 메서드는 잡과 컨테이너를 파라미터로 받는 콜백을 등록합니다. 일반적으로 이 코드는 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 호출합니다:

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 이미지 등 바이너리 데이터를 큐에 넘길 때는 반드시 `base64_encode` 함수를 사용해 인코딩해야 합니다. 그렇지 않으면 잡을 JSON으로 직렬화할 때 문제가 발생할 수 있습니다.

<a name="handling-relationships"></a>
#### 큐의 Eloquent 연관관계 처리

잡에 Eloquent 모델과 그 연관관계까지 로딩된 상태로 큐에 올려보내면, 직렬화된 데이터의 크기가 커질 수 있습니다. 또, 큐에서 잡을 복원할 때 관계 전체가 다시 조회됩니다. 즉, 큐에 넣을 당시 적용됐던 쿼리 조건(제한)이 사라질 수 있습니다. 따라서, 연관관계의 일부만 다루려면, 잡 안에서 관계 조회에 필요한 조건을 다시 지정하는 것이 좋습니다.

아니면, 아예 모델을 큐에 추가할 때 `withoutRelations` 메서드를 호출해 연관관계 직렬화를 방지할 수 있습니다:

```php
/**
 * 새 잡 인스턴스 생성자
 */
public function __construct(
    Podcast $podcast,
) {
    $this->podcast = $podcast->withoutRelations();
}
```

[PHP 생성자 프로퍼티 프로모션](https://www.php.net/manual/en/language.oop5.decon.php#language.oop5.decon.constructor.promotion)을 사용하는 경우, Eloquent 모델에 연관관계 직렬화를 막으려면 `WithoutRelations` 어트리뷰트를 사용할 수 있습니다:

```php
use Illuminate\Queue\Attributes\WithoutRelations;

/**
 * 새 잡 인스턴스 생성자
 */
public function __construct(
    #[WithoutRelations]
    public Podcast $podcast,
) {}
```

모든 모델에서 연관관계를 직렬화하지 않으려면, 클래스 전체에 `WithoutRelations` 어트리뷰트를 지정할 수도 있습니다:

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
     * 새 잡 인스턴스 생성자
     */
    public function __construct(
        public Podcast $podcast,
        public DistributionPlatform $platform,
    ) {}
}
```

잡이 단일 모델이 아닌 컬렉션이나 배열로 여러 Eloquent 모델을 전달받는 경우, 큐에서 복원 시 연관관계는 복구되지 않습니다. 이는 많은 모델을 다루는 잡에서 과도한 리소스 사용을 방지하기 위함입니다.

<a name="unique-jobs"></a>
### 유니크 잡 (Unique Jobs)

> [!WARNING]
> 유니크 잡은 [락 기능](/docs/12.x/cache#atomic-locks)을 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 아토믹 락을 지원합니다.

> [!WARNING]
> 유니크 잡 제약은 배치 잡에는 적용되지 않습니다.

특정 잡이 동시에 큐에 한 번만 올라가도록 설정하고 싶을 때가 있습니다. 이럴 때 잡 클래스에 `ShouldBeUnique` 인터페이스를 구현하면 됩니다. 이 인터페이스는 별도의 메서드 구현이 필요 없습니다:

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

예를 들어, `UpdateSearchIndex` 잡이 유니크하다면, 이미 동일한 잡이 큐에서 처리 중이면 새로운 잡은 디스패치되지 않습니다.

특정한 "키"로 유니크 잡 판별을 하거나, 유니크 상태 유지 시간 제한을 두고 싶을 때는 `uniqueId` 및 `uniqueFor` 프로퍼티나 메서드를 정의하세요:

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
     * 유니크 락을 해제할(보유할) 시간(초)
     *
     * @var int
     */
    public $uniqueFor = 3600;

    /**
     * 잡의 유니크 ID 반환
     */
    public function uniqueId(): string
    {
        return $this->product->id;
    }
}
```

위 예시처럼 product ID로 잡을 구분하면, 동일 product ID로 중복 잡이 올라오지 않고, 기존 잡이 1시간 내에 끝나지 않으면 락이 해제되어 새로운 잡이 큐에 들어올 수 있습니다.

> [!WARNING]
> 여러 웹 서버/컨테이너에서 잡을 디스패치한다면, 모든 서버가 동일한 중앙 캐시 서버를 사용해야 유니크 잡 판단이 올바르게 동작합니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 처리 시작 전까지 유니크 상태 유지

유니크 잡은 기본적으로 처리 완료(또는 모든 재시도 실패) 시 유니크 락이 해제됩니다. 하지만 잡 처리 "시작 직전"에 락 해제를 원한다면, `ShouldBeUnique` 대신 `ShouldBeUniqueUntilProcessing` 계약을 구현하세요:

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
#### 유니크 잡 락 커스터마이징

내부적으로 `ShouldBeUnique` 잡이 디스패치되면, Laravel은 `uniqueId` 키로 [락](/docs/12.x/cache#atomic-locks)을 획득하려 시도합니다. 락이 이미 잡혀 있다면 디스패치가 건너뜁니다. 이 락은 잡이 처리 완료(또는 모든 재시도 실패) 시 해제됩니다. 기본적으로 기본 캐시 드라이버를 사용하지만, 다른 드라이버를 명시적으로 사용하고 싶다면 `uniqueVia` 메서드를 구현하세요:

```php
use Illuminate\Contracts\Cache\Repository;
use Illuminate\Support\Facades\Cache;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...

    /**
     * 유니크 잡 락에 사용할 캐시 드라이버 반환
     */
    public function uniqueVia(): Repository
    {
        return Cache::driver('redis');
    }
}
```

> [!NOTE]
> 동시 실행 제한만 필요하다면 [WithoutOverlapping](/docs/12.x/queues#preventing-job-overlaps) 잡 미들웨어를 활용하세요.

<a name="encrypted-jobs"></a>
### 암호화된 잡 (Encrypted Jobs)

Laravel은 [암호화](/docs/12.x/encryption)를 통해 잡 데이터의 기밀성과 무결성을 보장할 수 있습니다. 잡 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하기만 하면, 잡이 자동으로 암호화되어 큐에 추가됩니다:

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

잡 미들웨어를 사용하면, 각 잡 실행 전후에 커스텀 로직을 감쌀 수 있어 잡 클래스에서 중복되는 코드(보일러플레이트)를 줄일 수 있습니다. 예를 들어, 아래와 같이 Redis 속도 제한을 직접 구현할 수도 있지만:

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

이처럼 handle 메서드에 로직이 섞이면 코드가 복잡해지고, 유사한 잡마다 중복 구현이 필요합니다. 이를 해결하기 위해 rate limiting 처리를 잡 미들웨어로 분리할 수 있습니다:

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

[라우트 미들웨어](/docs/12.x/middleware)처럼, 잡 미들웨어도 현재 잡 인스턴스와 다음 콜백을 인자로 받습니다.

새 잡 미들웨어 클래스는 `make:job-middleware` Artisan 명령어로 생성할 수 있습니다. 만든 미들웨어는 잡 클래스의 `middleware` 메서드에서 반환합니다. (이 메서드는 `make:job`으로 스캐폴딩시 생성되지 않으며, 직접 추가해야 합니다):

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
> 잡 미들웨어는 [큐처리 이벤트 리스너](/docs/12.x/events#queued-event-listeners), [메일](/docs/12.x/mail#queueing-mail), [알림](/docs/12.x/notifications#queueing-notifications)에도 사용할 수 있습니다.

<a name="rate-limiting"></a>
### 속도 제한 (Rate Limiting)

직접 미들웨어를 구현하지 않아도, Laravel의 기본 rate limiting 미들웨어를 사용할 수 있습니다. [라우트 rate limiter](/docs/12.x/routing#defining-rate-limiters)와 동일하게, `RateLimiter` 파사드의 `for` 메서드로 미들웨어를 정의합니다.

예를 들어, 일반 사용자는 시간당 1회 백업만 허용하고, 프리미엄 사용자는 제한이 없다고 가정해봅니다. `AppServiceProvider`의 `boot` 메서드에서 rate limiter를 정의할 수 있습니다:

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

위 예시는 시간 단위 제한이지만, `perMinute` 메서드로 분 단위 제한도 가능합니다. `by` 메서드에는 보통 고객마다 제한을 나누기 위해 사용자의 ID 등을 넣습니다.

```php
return Limit::perMinute(50)->by($job->user->id);
```

레이트리미터가 정의되면, 잡에 `Illuminate\Queue\Middleware\RateLimited` 미들웨어를 연결하면 됩니다. 속도 제한에 걸리면 잡을 적절한 지연시간과 함께 큐에 다시 띄웁니다:

```php
use Illuminate\Queue\Middleware\RateLimited;

/**
 * 잡이 통과해야 할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited('backups')];
}
```

레이트리밋으로 인해 잡이 지연되어도, 시도 횟수(`attempts`)는 계속 늘어납니다. 이에 따라 잡의 `tries`와 `maxExceptions` 프로퍼티를 조절하거나, [retryUntil 메서드](#time-based-attempts)로 시도 기간 한계를 설정하세요.

`releaseAfter` 메서드로 잡이 재시도되기 전 대기할 시간을 초 단위로 지정할 수도 있습니다:

```php
/**
 * 잡이 통과해야 할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new RateLimited('backups'))->releaseAfter(60)];
}
```

rate 제한에 걸렸을 때 재시도 자체를 원하지 않으면 `dontRelease` 메서드를 사용할 수 있습니다:

```php
/**
 * 잡이 통과해야 할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new RateLimited('backups'))->dontRelease()];
}
```

> [!NOTE]
> Redis를 사용하는 경우, 기본 미들웨어보다 효율적인 `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어를 사용할 수 있습니다.

<a name="preventing-job-overlaps"></a>
### 잡 중복 실행 방지 (Preventing Job Overlaps)

`Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어를 사용하면 임의의 키를 기준으로 잡의 중복 실행을 방지할 수 있습니다. 이는 같은 리소스를 동시에 여러 잡이 수정하지 못하게 막을 때 유용합니다.

예를 들어, 사용자의 크레딧 점수를 업데이트하는 큐 잡이 있는데, 동일 사용자 ID에 동시에 여러 잡이 처리되지 않게 하려면 다음과 같이 미들웨어를 반환하면 됩니다:

```php
use Illuminate\Queue\Middleware\WithoutOverlapping;

/**
 * 잡이 통과해야 할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new WithoutOverlapping($this->user->id)];
}
```

중복(Overlapping) 잡을 다시 큐로 돌려도 시도 횟수는 계속 집계됩니다. 예를 들어 `tries` 값을 기본값 1로 두면 중복 잡은 재시도 기회가 없습니다.

중복 잡을 일정 시간 후에 재시도하려면 `releaseAfter` 메서드를 사용하세요:

```php
/**
 * 잡이 통과해야 할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->releaseAfter(60)];
}
```

중복 잡은 즉시 삭제(재시도 안 함)하고 싶다면 `dontRelease` 메서드를 사용하세요:

```php
/**
 * 잡이 통과해야 할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->dontRelease()];
}
```

`WithoutOverlapping` 미들웨어는 Laravel의 아토믹 락 기능을 기반으로 동작합니다. 때때로 잡 실행이 실패하거나 타임아웃될 경우 락이 해제되지 않을 수 있으니, `expireAfter` 메서드로 락 만료시간을 명시할 수 있습니다. 아래 예제는 잡 처리 시작 후 3분(180초)에 락이 자동 해제됩니다:

```php
/**
 * 잡이 통과해야 할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->expireAfter(180)];
}
```

> [!WARNING]
> `WithoutOverlapping` 미들웨어는 [락을 지원하는 캐시 드라이버](/docs/12.x/cache#atomic-locks)가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 드라이버가 지원합니다.

<a name="sharing-lock-keys"></a>
#### 여러 잡 클래스에서 락 키 공유

기본적으로 `WithoutOverlapping` 미들웨어는 같은 클래스의 잡끼리만 중복 실행을 막아줍니다. 만약 서로 다른 잡 클래스여도 같은 락 키로 묶고 싶다면, `shared` 메서드를 쓰면 됩니다:

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
### 예외 쓰로틀링 (Throttling Exceptions)

`Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어를 사용하면 잡에서 일정 횟수 이상의 예외가 발생했을 때, 남은 시도 횟수는 일정 시간 후에만 다시 시도하게 제한할 수 있습니다. 특히 불안정한 타사 API와 연동하는 잡에 효과적입니다.

예를 들어, 외부 API에서 예외가 연달아 발생하면 아래처럼 미들웨어를 설정하고, [시간 기반 시도 제한](#time-based-attempts)과 함께 활용할 수 있습니다:

```php
use DateTime;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡이 통과해야 할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new ThrottlesExceptions(10, 5 * 60)];
}

/**
 * 잡의 최대 시도 허용 기간 결정
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(30);
}
```

생성자의 첫 번째 인자는 허용 예외 횟수, 두 번째 인자는 쓰로틀링 후 다음 시도까지 대기할 시간(초)입니다. 위의 예에서는 10번 연속 예외가 발생하면 5분간 쉬었다가 다시 시도하게 됩니다. 전체 시도 기간은 30분입니다.

예외 발생 시마다 즉시 재시도하지 않고, 일정 시간 대기 후 재시도하려면 `backoff` 메서드를 호출하세요:

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡이 통과해야 할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 5 * 60))->backoff(5)];
}
```

내부적으로 이 미들웨어는 캐시 시스템을 이용해 쓰로틀링을 구현하며, 기본적으로는 잡 클래스명이 캐시 "키"로 사용됩니다. 여러 잡이 동일한 타사 서비스를 공유하며 동일하게 쓰로틀링되길 원하면, `by` 메서드로 키를 명시적으로 지정할 수 있습니다:

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡이 통과해야 할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->by('key')];
}
```

모든 예외가 아니라 특정 조건의 예외만 쓰로틀링하고 싶다면 `when` 메서드에 클로저를 넘기세요:

```php
use Illuminate\Http\Client\HttpClientException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡이 통과해야 할 미들웨어 반환
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

`when`과 달리, 예외가 발생하면 잡을 큐에서 즉시 삭제하고 싶다면 `deleteWhen` 메서드를 사용하세요:

```php
use App\Exceptions\CustomerDeletedException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡이 통과해야 할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(2, 10 * 60))->deleteWhen(CustomerDeletedException::class)];
}
```

예외를 앱의 예외 핸들러에 리포트하고 싶다면, `report` 메서드를 호출하세요. 필요하다면 클로저를 넘겨 조건을 세울 수도 있습니다:

```php
use Illuminate\Http\Client\HttpClientException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡이 통과해야 할 미들웨어 반환
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
> Redis를 사용하는 경우, 기본 미들웨어보다 효율적인 `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어를 사용할 수 있습니다.

<a name="skipping-jobs"></a>
### 잡 스킵하기 (Skipping Jobs)

`Skip` 미들웨어는 잡 내부 로직을 수정하지 않고도 잡을 조건에 따라 스킵(삭제)할 수 있게 해줍니다. `Skip::when` 메서드는 조건이 true면 잡을 삭제하고, `Skip::unless` 메서드는 false면 잡을 삭제합니다:

```php
use Illuminate\Queue\Middleware\Skip;

/**
 * 잡이 통과해야 할 미들웨어 반환
 */
public function middleware(): array
{
    return [
        Skip::when($condition),
    ];
}
```

좀 더 복잡한 조건이 필요한 경우, `when`과 `unless`에 클로저를 넘길 수 있습니다:

```php
use Illuminate\Queue\Middleware\Skip;

/**
 * 잡이 통과해야 할 미들웨어 반환
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
(이하 생략)

(※ 내용이 길어, 나머지 섹션(잡 디스패치하기 ~ 끝까지)은 추가 요청시 바로 이어서 번역해 드릴 수 있습니다.)