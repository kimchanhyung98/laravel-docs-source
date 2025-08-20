# 큐 (Queues)

- [소개](#introduction)
    - [커넥션과 큐의 차이](#connections-vs-queues)
    - [드라이버별 안내 및 필수 조건](#driver-prerequisites)
- [잡 생성하기](#creating-jobs)
    - [잡 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [유일한 잡(Unique Jobs)](#unique-jobs)
    - [암호화된 잡](#encrypted-jobs)
- [잡 미들웨어](#job-middleware)
    - [요율 제한(Rate Limiting)](#rate-limiting)
    - [잡 중복 실행 방지](#preventing-job-overlaps)
    - [예외 처리 요율 제한(Throttling)](#throttling-exceptions)
    - [잡 스킵하기](#skipping-jobs)
- [잡 디스패치하기](#dispatching-jobs)
    - [지연 디스패치](#delayed-dispatching)
    - [동기식 디스패치](#synchronous-dispatching)
    - [잡과 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [잡 체이닝(Job Chaining)](#job-chaining)
    - [큐 및 커넥션 커스터마이징](#customizing-the-queue-and-connection)
    - [최대 시도 횟수/타임아웃 값 지정](#max-job-attempts-and-timeout)
    - [에러 처리](#error-handling)
- [잡 배치(Job Batching)](#job-batching)
    - [배치 가능한 잡 정의](#defining-batchable-jobs)
    - [배치 디스패치](#dispatching-batches)
    - [배치와 체인 결합](#chains-and-batches)
    - [배치에 잡 추가](#adding-jobs-to-batches)
    - [배치 조회](#inspecting-batches)
    - [배치 취소](#cancelling-batches)
    - [배치 실패 처리](#batch-failures)
    - [배치 레코드 정리(Pruning)](#pruning-batches)
    - [DynamoDB에 배치 저장](#storing-batches-in-dynamodb)
- [클로저 큐잉](#queueing-closures)
- [큐 워커 실행](#running-the-queue-worker)
    - [`queue:work` 명령어](#the-queue-work-command)
    - [큐 우선순위](#queue-priorities)
    - [큐 워커와 배포](#queue-workers-and-deployment)
    - [잡 만료 및 타임아웃](#job-expirations-and-timeouts)
- [Supervisor 구성](#supervisor-configuration)
- [실패한 잡 처리](#dealing-with-failed-jobs)
    - [실패 잡 후처리](#cleaning-up-after-failed-jobs)
    - [실패한 잡 재시도](#retrying-failed-jobs)
    - [모델이 없는 경우 무시](#ignoring-missing-models)
    - [실패 잡 정리(Pruning)](#pruning-failed-jobs)
    - [DynamoDB에 실패 잡 저장](#storing-failed-jobs-in-dynamodb)
    - [실패 잡 저장 비활성화](#disabling-failed-job-storage)
    - [실패 잡 이벤트](#failed-job-events)
- [큐에서 잡 삭제](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [특정 잡만 가짜로 처리](#faking-a-subset-of-jobs)
    - [잡 체인 테스트](#testing-job-chains)
    - [잡 배치 테스트](#testing-job-batches)
    - [잡/큐 상호작용 테스트](#testing-job-queue-interactions)
- [잡 이벤트](#job-events)

<a name="introduction"></a>
## 소개 (Introduction)

웹 애플리케이션을 개발할 때, 업로드된 CSV 파일을 파싱 및 저장하는 작업과 같이 웹 요청 중에 처리하기에는 너무 오래 걸리는 작업들이 있을 수 있습니다. 다행히 Laravel은 백그라운드에서 처리할 수 있는 큐드 잡(queued jobs)을 쉽게 생성할 수 있도록 지원합니다. 이렇게 시간 소요가 큰 작업을 큐로 분리하면, 애플리케이션이 웹 요청에 훨씬 빠르게 반응할 수 있고 사용자에게 더 나은 경험을 제공합니다.

Laravel 큐는 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io) 또는 관계형 데이터베이스와 같은 다양한 큐 백엔드에 대해 통합된 큐잉 API를 제공합니다.

Laravel의 큐 관련 설정은 애플리케이션의 `config/queue.php` 설정 파일에 있습니다. 이 파일에는 프레임워크에 내장된 각 큐 드라이버(데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/)) 및 동기식 드라이버(로컬 개발용, 잡을 즉시 실행)를 위한 커넥션 설정이 포함되어 있습니다. 또한 큐에 쌓인 잡을 버리는 `null` 큐 드라이버도 제공됩니다.

> [!NOTE]
> Laravel Horizon은 Redis 기반 큐를 위한 아름다운 대시보드 및 설정 시스템입니다. 자세한 내용은 [Horizon 문서](/docs/12.x/horizon)를 참고하세요.

<a name="connections-vs-queues"></a>
### 커넥션과 큐의 차이

Laravel 큐를 사용하기 전, "커넥션(connection)"과 "큐(queue)"의 차이를 이해하는 것이 중요합니다. `config/queue.php` 파일에는 `connections` 설정 배열이 있습니다. 이 옵션은 Amazon SQS, Beanstalk, Redis와 같은 백엔드 큐 서비스에 연결하는 커넥션을 정의합니다. 하지만 하나의 큐 커넥션은 여러 개의 "큐"를 가질 수 있습니다. 각각 다른 작업 스택처럼 생각할 수 있습니다.

각 커넥션 설정 예제에는 `queue` 속성이 포함되어 있습니다. 이는 해당 커넥션으로 보낼 때 기본으로 사용되는 큐를 뜻합니다. 즉, 잡을 디스패치할 때 어떤 큐에 넣을지 명시하지 않으면, 해당 커넥션 설정의 `queue` 속성에 정의된 큐에 잡이 들어갑니다.

```php
use App\Jobs\ProcessPodcast;

// 기본 커넥션의 기본 큐로 잡을 전송...
ProcessPodcast::dispatch();

// 기본 커넥션의 "emails" 큐로 잡을 전송...
ProcessPodcast::dispatch()->onQueue('emails');
```

대부분의 애플리케이션에서는 하나의 큐만 사용해도 문제가 없지만, 여러 큐로 작업을 분산시키면 잡을 우선순위에 따라 처리하거나, 처리 방식에 따라 세분화할 수 있어 유용합니다. 예를 들어, `high`라는 큐에 잡을 추가하면, 해당 큐에 우선적으로 작업을 할당하는 워커를 실행할 수 있습니다.

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버별 안내 및 필수 조건

<a name="database"></a>
#### 데이터베이스

`database` 큐 드라이버를 사용하려면 잡을 저장할 데이터베이스 테이블이 필요합니다. 일반적으로 Laravel의 기본 마이그레이션인 `0001_01_01_000002_create_jobs_table.php` [마이그레이션](/docs/12.x/migrations)에 포함되어 있습니다. 만약 적용되어 있지 않다면, `make:queue-table` Artisan 명령어로 생성할 수 있습니다.

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면, 우선 `config/database.php`에서 Redis 데이터베이스 커넥션을 설정해야 합니다.

> [!WARNING]
> `redis` 큐 드라이버는 Redis의 `serializer` 및 `compression` 옵션을 지원하지 않습니다.

<a name="redis-cluster"></a>
##### Redis 클러스터

Redis 클러스터([Redis Cluster](https://redis.io/docs/latest/operate/rs/databases/durability-ha/clustering))를 사용하는 경우, 큐 이름에 [키 해시 태그(key hash tag)](https://redis.io/docs/latest/develop/using-commands/keyspace/#hashtags)를 포함해야 합니다. 이는 같은 큐의 모든 Redis 키가 동일한 해시 슬롯에 속하도록 보장하기 위해 필요합니다.

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
##### 블로킹 (Blocking)

Redis 큐를 사용할 때, `block_for` 설정 옵션으로 잡이 나타날 때까지 워커 루프에서 얼마나 대기할지 지정할 수 있습니다.

큐의 로드 양에 따라 이 값을 조절하면 Redis 데이터베이스를 계속 폴링하는 것보다 효율적으로 처리할 수 있습니다. 예를 들어 이 값을 `5`로 두면, 잡이 나타날 때까지 5초 동안 기다립니다.

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
> `block_for`를 `0`으로 설정하면 잡이 도착할 때까지 무한히 대기하게 됩니다. 이 경우 `SIGTERM` 등의 신호도 다음 잡이 처리되기 전까지는 전달되지 않습니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 필수 조건

아래 드라이버를 사용하려면 다음 의존성이 필요합니다. Composer 패키지 관리자를 통해 설치하세요.

<div class="content-list" markdown="1">

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~2.0` 또는 phpredis PHP 확장
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`

</div>

<a name="creating-jobs"></a>
## 잡 생성하기 (Creating Jobs)

<a name="generating-job-classes"></a>
### 잡 클래스 생성

애플리케이션의 큐 처리 가능한(job queueable) 잡 클래스는 기본적으로 `app/Jobs` 디렉터리에 보관됩니다. 만약 이 디렉터리가 없다면, `make:job` Artisan 명령어 실행 시 자동으로 생성됩니다.

```shell
php artisan make:job ProcessPodcast
```

생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하여 비동기적으로 큐에 쌓아 실행할 수 있음을 나타냅니다.

> [!NOTE]
> 잡 스텁은 [스텁 퍼블리싱](/docs/12.x/artisan#stub-customization)을 통해 커스터마이즈할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조

잡 클래스는 보통 간단하며, 큐가 잡을 처리할 때 호출되는 `handle` 메서드만 포함합니다. 예시로 팟캐스트 업로드 파일을 처리하는 잡 클래스를 살펴보겠습니다.

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

위 예시에서는 [Eloquent 모델](/docs/12.x/eloquent)을 생성자 파라미터로 바로 전달할 수 있습니다. 잡에서 사용하는 `Queueable` 트레이트 덕분에, Eloquent 모델 및 로드된 연관관계도 직렬화/역직렬화가 자연스럽게 처리됩니다.

큐로 보낼 잡의 생성자에 Eloquent 모델을 전달하면, 모델의 식별자만 큐에 직렬화되어 저장됩니다. 잡이 실제로 처리될 때는 큐 시스템이 데이터베이스에서 전체 모델 인스턴스와 로드된 연관관계를 다시 가져옵니다. 이런 모델 직렬화 방식 덕분에 잡 페이로드가 매우 작아집니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드의 의존성 주입

`handle` 메서드는 큐에서 잡을 처리할 때 호출됩니다. 이 메서드에서 타입힌트를 지정하면, [서비스 컨테이너](/docs/12.x/container)가 자동으로 해당 의존성을 주입해줍니다.

컨테이너의 의존성 주입 방식을 완전히 제어하고 싶다면, 컨테이너의 `bindMethod` 메서드를 활용할 수 있습니다. 이 메서드는 잡과 컨테이너를 콜백으로 받아 직접 `handle` 메서드 호출을 원하는 방식으로 구현할 수 있습니다. 보통 이 작업은 `App\Providers\AppServiceProvider`의 `boot` 메서드 등 [서비스 프로바이더](/docs/12.x/providers)에서 이루어집니다.

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 원시 이미지 데이터 등 바이너리 데이터는 잡으로 전달하기 전에 반드시 `base64_encode` 함수로 인코딩하십시오. 그렇지 않으면 큐에 잡을 넣을 때 JSON으로 직렬화하는 과정에서 문제가 발생할 수 있습니다.

<a name="handling-relationships"></a>
#### 큐에 포함된 연관관계

큐에 잡을 넣을 때 Eloquent 모델의 연관관계도 함께 직렬화됩니다. 이 때 직렬화된 잡 문자열이 커질 수 있습니다. 잡이 역직렬화되고 모델의 연관관계가 재조회될 때, 이전에 애플리케이션에서 적용한 연관관계 제한 조건이 그대로 적용되지 않는다는 점에 유의해야 합니다. 만약 특정 연관관계 컬렉션의 일부만 사용하고 싶다면, 잡 내에서 연관관계 제한을 다시 적용해야 합니다.

아니면 연관관계 직렬화를 아예 방지하고 싶을 땐, 프로퍼티를 지정할 때 모델의 `withoutRelations` 메서드를 호출하면 됩니다. 이 메서드는 로드된 연관관계가 제거된 모델 인스턴스를 반환합니다.

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

[PHP 생성자 프로퍼티 프로모션](https://www.php.net/manual/en/language.oop5.decon.php#language.oop5.decon.constructor.promotion)을 사용할 때, Eloquent 모델의 연관관계를 직렬화하지 않으려면 `WithoutRelations` 속성(attribute)을 활용할 수 있습니다.

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

모든 모델의 연관관계를 직렬화하지 않으려면, 각 프로퍼티가 아니라 클래스 전체에 `WithoutRelations` 속성을 부여할 수도 있습니다.

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

잡이 단일 모델이 아닌 Eloquent 모델의 컬렉션 또는 배열을 받는 경우, 역직렬화 및 실행 시 컬렉션 내부의 각 모델은 연관관계가 복원되지 않습니다. 이는 많은 모델을 다루는 잡에서 과도한 리소스 사용을 방지하기 위함입니다.

<a name="unique-jobs"></a>
### 유일한 잡 (Unique Jobs)

> [!WARNING]
> 유일한 잡 기능은 [락(locks)](/docs/12.x/cache#atomic-locks)을 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 지원됩니다. 또한 유일 잡 제약은 배치 내 잡에는 적용되지 않습니다.

특정 잡 인스턴스가 한 번에 큐에 하나만 존재하도록 하고 싶을 때, 잡 클래스에 `ShouldBeUnique` 인터페이스를 구현하면 됩니다. 이 인터페이스는 추가 메서드 구현이 필요 없습니다.

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

위 예시에서 `UpdateSearchIndex` 잡은 큐에 이미 동일한 잡이 처리 중이라면 새롭게 디스패치되지 않습니다.

특정 "키"로 잡의 유일성을 결정하거나, 일정 시간 후 유일성이 풀리도록 하고 싶을 때는 `uniqueId` 및 `uniqueFor` 프로퍼티(또는 메서드)를 정의할 수 있습니다.

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
     * 잡의 유일 락이 해제될 시간(초)
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

이 예시에서 `UpdateSearchIndex` 잡은 상품 ID로 유일성이 결정됩니다. 동일 상품에 대한 새 잡은, 기존 잡이 끝나기 전에는 무시됩니다. 만약 1시간 내에 기존 잡이 끝나지 않으면, 유일 락이 해제되어 같은 상품에 대한 새 잡을 디스패치할 수 있습니다.

> [!WARNING]
> 여러 웹 서버나 컨테이너에서 잡을 디스패치한다면, 반드시 모든 서버가 동일한 중앙 캐시 서버와 통신하는지 확인해야, Laravel이 잡의 유일성을 정확히 판단할 수 있습니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 잡 처리 직전까지 유일 락 유지

기본적으로 유일한 잡은 처리 완료 또는 모든 재시도 실패 후 "락 해제"됩니다. 하지만 때로는 잡이 실제 처리 직전에 즉시 락을 해제하고 싶을 때도 있습니다. 이 경우 `ShouldBeUnique` 대신 `ShouldBeUniqueUntilProcessing` 인터페이스를 구현하세요.

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

내부적으로 `ShouldBeUnique` 잡을 디스패치할 때 Laravel은 `uniqueId` 키로 [락](/docs/12.x/cache#atomic-locks)을 시도합니다. 이미 락이 잡혀 있다면 잡은 디스패치되지 않습니다. 이 락은 잡이 처리 완료되거나 모든 재시도에 실패할 때 해제됩니다. 기본적으로 Laravel은 기본 캐시 드라이버를 사용합니다. 특정 캐시 드라이버를 사용하고 싶다면 `uniqueVia` 메서드를 정의할 수 있습니다.

```php
use Illuminate\Contracts\Cache\Repository;
use Illuminate\Support\Facades\Cache;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...

    /**
     * 유일 잡 락용 캐시 드라이버 반환
     */
    public function uniqueVia(): Repository
    {
        return Cache::driver('redis');
    }
}
```

> [!NOTE]
> 잡의 동시 실행만 제한하고 싶다면 [WithoutOverlapping](#preventing-job-overlaps) 잡 미들웨어를 사용하는 것이 더 간단합니다.

<a name="encrypted-jobs"></a>
### 암호화된 잡 (Encrypted Jobs)

잡의 데이터 프라이버시 및 무결성을 [암호화](/docs/12.x/encryption)로 보장할 수 있습니다. 잡 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하면 됩니다. 이 인터페이스가 추가된 잡은 Laravel이 큐에 추가하기 전에 자동으로 암호화합니다.

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

잡 미들웨어를 사용하면 큐 잡 실행 시 커스텀 로직을 감쌀 수 있어, 잡 코드 자체가 간결해집니다. 예를 들어, 아래 `handle` 메서드는 Laravel의 Redis 요율 제한 기능을 이용해 5초마다 한 번씩 잡을 처리하고 있습니다.

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

이 로직은 유효하지만, 실제 잡 처리 로직과 요율 제한 코드가 섞이게 되어 복잡해집니다. 그리고 비슷한 요율 제한이 필요한 다른 잡에서도 중복해줘야 하죠. 이런 경우 직접 잡 미들웨어 클래스를 만들어서 처리할 수 있습니다.

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
                // 락 획득됨...

                $next($job);
            }, function () use ($job) {
                // 락 획득 실패...

                $job->release(5);
            });
    }
}
```

이처럼 [라우트 미들웨어](/docs/12.x/middleware)와 비슷하게, 잡 미들웨어는 처리 중인 잡과 다음 콜백을 받아 작업을 이어갈 수 있습니다.

`make:job-middleware` Artisan 명령어를 사용해 새로운 잡 미들웨어 클래스를 생성할 수 있습니다. 미들웨어를 잡에 연결하려면 잡의 `middleware` 메서드에서 반환하세요. 이 메서드는 Artisan이 생성한 기본 잡에서는 생성되지 않으니, 직접 추가해야 합니다.

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
> 잡 미들웨어는 [큐잉 이벤트 리스너](/docs/12.x/events#queued-event-listeners), [메일러블](/docs/12.x/mail#queueing-mail), [알림](/docs/12.x/notifications#queueing-notifications)에도 적용할 수 있습니다.

<a name="rate-limiting"></a>
### 요율 제한 (Rate Limiting)

직접 요율 제한 미들웨어를 작성하지 않아도 Laravel이 미리 준비한 요율 제한 미들웨어를 사용할 수 있습니다. [라우트 요율 제한자](/docs/12.x/routing#defining-rate-limiters)와 유사하게, 잡 요율 제한자도 `RateLimiter` 파사드의 `for` 메서드로 정의합니다.

예를 들어, 일반 사용자는 한 시간에 한 번만 데이터 백업을 허용하고 프리미엄 고객은 제한을 두지 않으려면 `AppServiceProvider`의 `boot`에서 RateLimiter를 정의하세요.

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

여기서는 1시간 제한을 설정했지만, `perMinute` 등으로 단위도 쉽게 바꿀 수 있습니다. `by` 메서드에는 고객 등 분할 기준이 되는 값을 전달합니다.

```php
return Limit::perMinute(50)->by($job->user->id);
```

요율 제한자를 정의했다면, `Illuminate\Queue\Middleware\RateLimited` 미들웨어를 잡에 붙이세요. 제한을 초과할 때마다 미들웨어가 잡을 적절한 지연을 두고 큐로 다시 내보냅니다.

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

요율 제한 미들웨어로 인해 잡이 재시도될 때는 `attempts` 횟수도 증가합니다. 이에 따라 `tries`, `maxExceptions` 등을 적절히 조정하세요. 또는 [retryUntil 메서드](#time-based-attempts)를 사용해 잡의 유효 기간을 지정하세요.

`releaseAfter` 메서드로 다시 시도까지 대기할 시간을 초 단위로 지정할 수 있습니다.

```php
public function middleware(): array
{
    return [(new RateLimited('backups'))->releaseAfter(60)];
}
```

잡이 요율 제한에 걸릴 때마다 재시도하고 싶지 않다면 `dontRelease` 메서드를 사용하세요.

```php
public function middleware(): array
{
    return [(new RateLimited('backups'))->dontRelease()];
}
```

> [!NOTE]
> Redis를 사용하는 경우에는 `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어를 사용하면 성능이 더 우수합니다.

<a name="preventing-job-overlaps"></a>
### 잡 중복 실행 방지

Laravel에는 임의의 키로 잡의 중첩 실행을 방지하는  `Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어가 내장되어 있습니다. 하나의 리소스를 동시에 여러 잡이 수정하는 것을 방지할 때 유용합니다.

예를 들어, 사용자의 신용 점수를 갱신하는 잡이 있는데 동일 사용자에 대한 갱신 잡이 겹치지 않도록 하려면 `middleware`에 아래처럼 반환하면 됩니다.

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

중첩 잡이 큐로 다시 전송되면 시도 횟수도 증가하므로, 필요한 만큼 `tries`와 `maxExceptions` 등을 조정하세요. 예를 들어 `tries` 기본값이 1이면 중첩 잡은 다시 실행되지 않습니다.

동일 타입의 중첩 잡은 큐로 다시 전달됩니다. 지연 시간을 지정하고 싶을 때는

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->releaseAfter(60)];
}
```

중첩 잡을 즉시 삭제해 다시 시도하지 않으려면 `dontRelease`를 사용합니다.

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->dontRelease()];
}
```

`WithoutOverlapping` 미들웨어는 Laravel의 원자적 락 기능을 이용합니다. 드물지만 잡이 실패하거나 타임아웃으로 락이 해제되지 않을 수도 있습니다. 이럴 땐 `expireAfter`로 락 만료 시간을 명시하세요.

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->expireAfter(180)];
}
```

> [!WARNING]
> `WithoutOverlapping` 미들웨어는 [락을 지원하는](/docs/12.x/cache#atomic-locks) 캐시 드라이버(`memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 등)가 필요합니다.

<a name="sharing-lock-keys"></a>
#### 잡 클래스 간 락 키 공유

기본적으로 `WithoutOverlapping` 미들웨어는 동일 클래스 잡끼리만 중첩 실행을 막습니다. 서로 다른 잡 클래스가 똑같은 락 키를 사용해도 동시 실행이 막히지 않습니다. 여러 잡 클래스에 걸쳐 락 키를 공유하려면 `shared` 메서드를 추가로 사용하세요.

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
### 예외 처리 요율 제한(Throttling Exceptions)

`Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어를 사용하면 예외 발생 빈도를 제한할 수 있습니다. 잡에서 특정 횟수 만큼 예외가 발생하면, 이후 일정 시간 동안 실행을 지연시킵니다. 서드파티 서비스 등 불안정한 시스템과 연동하는 잡에서 특히 유용합니다.

예를 들어, 외부 API와 연동하는 잡에서 예외가 반복된다면 아래처럼 미들웨어를 붙이고, [시간 기반 시도 제한](#time-based-attempts)을 함께 사용하세요.

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
 * 잡이 더 이상 시도되지 않아야 할 시간 반환
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(30);
}
```

첫 번째 인수는 허용할 예외 최대 횟수, 두 번째 인수는 제한 해제까지 대기할 초입니다. 예시처럼 10번 연속 예외시 5분 대기, 30분 내에 이 조건에 도달하지 않으면 제한이 해제됩니다.

예외 임계값 미만에서는 바로 재시도하지만, `backoff`로 일정 시간 지연도 가능합니다.

```php
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 5 * 60))->backoff(5)];
}
```

이 미들웨어는 쿠키로 잡 클래스 이름이 캐시 "키"로 사용됩니다. `by` 메서드로 키를 변경해 여러 잡이 한 버킷을 공유하도록 할 수 있습니다.

```php
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->by('key')];
}
```

기본적으로 모든 예외에 대해 요율 제한이 걸리지만, `when`에 클로저를 전달해 특정 조건의 예외만 제한할 수도 있습니다.

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

`when`과 달리, `deleteWhen`을 사용하면 특정 예외 발생 시 잡을 큐에서 완전히 삭제할 수 있습니다.

```php
use App\Exceptions\CustomerDeletedException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [(new ThrottlesExceptions(2, 10 * 60))->deleteWhen(CustomerDeletedException::class)];
}
```

예외 제한에 걸린 예외를 애플리케이션 예외 핸들러로 리포트하고 싶다면, `report` 메서드를 사용하세요. 클로저를 전달해 조건부 리포트도 가능합니다.

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
> Redis를 사용하는 경우에는, 더 최적화된 `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어를 사용하세요.

<a name="skipping-jobs"></a>
### 잡 스킵하기 (Skipping Jobs)

`Skip` 미들웨어는 잡 로직을 수정하지 않고도 잡을 건너뛰거나 삭제할 수 있게 해줍니다. `Skip::when`은 조건이 true일 때 잡을 삭제하고, `Skip::unless`는 false일 때 삭제합니다.

```php
use Illuminate\Queue\Middleware\Skip;

public function middleware(): array
{
    return [
        Skip::when($condition),
    ];
}
```

더 복잡한 조건식을 위해 클로저를 전달할 수도 있습니다.

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

<!-- 이하  문서 내용 계속... *** 답변 길이 제한으로 중단되었으니, 추가 번역이 필요하면 말씀해 주세요. *** -->