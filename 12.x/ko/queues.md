# 큐 (Queues)

- [소개](#introduction)
    - [커넥션과 큐의 차이](#connections-vs-queues)
    - [드라이버별 안내 및 사전 준비](#driver-prerequisites)
- [잡 생성하기](#creating-jobs)
    - [잡 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [유니크 잡](#unique-jobs)
    - [암호화된 잡](#encrypted-jobs)
- [잡 미들웨어](#job-middleware)
    - [속도 제한](#rate-limiting)
    - [잡 중복 처리 방지](#preventing-job-overlaps)
    - [예외 쓰로틀링](#throttling-exceptions)
    - [잡 건너뛰기](#skipping-jobs)
- [잡 디스패치하기](#dispatching-jobs)
    - [디스패치 지연하기](#delayed-dispatching)
    - [동기식 디스패치](#synchronous-dispatching)
    - [잡과 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [잡 체인](#job-chaining)
    - [큐와 커넥션 커스터마이징](#customizing-the-queue-and-connection)
    - [최대 시도 횟수/타임아웃 값 명시](#max-job-attempts-and-timeout)
    - [에러 처리](#error-handling)
- [잡 배치](#job-batching)
    - [배치 가능한 잡 정의하기](#defining-batchable-jobs)
    - [배치 디스패치하기](#dispatching-batches)
    - [체인과 배치](#chains-and-batches)
    - [배치에 잡 추가](#adding-jobs-to-batches)
    - [배치 조회](#inspecting-batches)
    - [배치 취소](#cancelling-batches)
    - [배치 실패](#batch-failures)
    - [배치 정리(pruning)](#pruning-batches)
    - [DynamoDB에 배치 저장](#storing-batches-in-dynamodb)
- [클로저 큐잉](#queueing-closures)
- [큐 워커 실행](#running-the-queue-worker)
    - [`queue:work` 명령어](#the-queue-work-command)
    - [큐 우선 순위](#queue-priorities)
    - [큐 워커와 배포](#queue-workers-and-deployment)
    - [잡 만료 및 타임아웃](#job-expirations-and-timeouts)
- [Supervisor 설정](#supervisor-configuration)
- [실패한 잡 처리](#dealing-with-failed-jobs)
    - [실패한 잡 정리](#cleaning-up-after-failed-jobs)
    - [실패한 잡 재시도](#retrying-failed-jobs)
    - [누락된 모델 무시](#ignoring-missing-models)
    - [실패한 잡 정리(pruning)](#pruning-failed-jobs)
    - [DynamoDB에 실패 잡 저장](#storing-failed-jobs-in-dynamodb)
    - [실패 잡 저장 비활성화](#disabling-failed-job-storage)
    - [실패 잡 이벤트](#failed-job-events)
- [큐에서 잡 삭제](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [일부 잡만 페이크로 처리](#faking-a-subset-of-jobs)
    - [잡 체인 테스트](#testing-job-chains)
    - [잡 배치 테스트](#testing-job-batches)
    - [잡 / 큐 상호작용 테스트](#testing-job-queue-interactions)
- [잡 이벤트](#job-events)

<a name="introduction"></a>
## 소개 (Introduction)

웹 애플리케이션을 개발하다 보면, 업로드된 CSV 파일을 파싱하고 저장하는 등 일반적인 웹 요청 동안 실행하기에는 오래 걸리는 작업들이 생길 수 있습니다. 다행히도 Laravel은 이러한 작업을 간단히 백그라운드에서 처리할 수 있도록 큐 잡(queued jobs)을 쉽게 만들 수 있도록 지원합니다. 시간 소모가 큰 작업을 큐로 보내면, 애플리케이션은 웹 요청에 훨씬 빠르게 응답할 수 있으며 사용자에게 더 좋은 경험을 제공합니다.

Laravel 큐는 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 또는 관계형 데이터베이스 등 다양한 큐 백엔드를 통합적으로 사용할 수 있는 API를 제공합니다.

큐 관련 설정은 애플리케이션의 `config/queue.php` 파일에 저장되어 있습니다. 이 파일에서는 프레임워크에 포함된 각 큐 드라이버(데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 등) 별로 커넥션 설정을 확인할 수 있습니다. 또한, 잡을 즉시 실행하는 동기식 드라이버(로컬 개발용)와, 큐 잡을 버리는 `null` 큐 드라이버도 제공됩니다.

> [!NOTE]
> Laravel은 Redis 기반 큐를 위한 아름다운 대시보드 및 설정 시스템인 Horizon을 제공합니다. 자세한 정보는 [Horizon 문서](/docs/12.x/horizon)를 참고하세요.

<a name="connections-vs-queues"></a>
### 커넥션과 큐의 차이

Laravel 큐를 사용하기 전에, "커넥션(connection)"과 "큐(queue)"의 차이를 이해하는 것이 중요합니다. `config/queue.php` 설정 파일에는 `connections` 배열이 있습니다. 이 옵션은 Amazon SQS, Beanstalk, Redis 등의 백엔드 큐 서비스에 대한 커넥션을 정의합니다. 단, 하나의 큐 커넥션 안에 여러 개의 "큐"가 있을 수 있습니다. 각 큐는 서로 다른 대기열, 즉 잡이 쌓이는 공간으로 생각하면 됩니다.

각 커넥션 설정 예시에는 `queue` 속성이 포함되어 있는데, 이것이 해당 커넥션의 기본 큐입니다. 즉, 특정 큐를 명시하지 않고 잡을 디스패치하면 이 속성에 정의된 큐로 전송됩니다:

```php
use App\Jobs\ProcessPodcast;

// 이 잡은 기본 커넥션의 기본 큐로 전송됩니다...
ProcessPodcast::dispatch();

// 이 잡은 기본 커넥션의 "emails" 큐로 전송됩니다...
ProcessPodcast::dispatch()->onQueue('emails');
```

어떤 애플리케이션은 한 개의 큐만으로 충분할 수 있지만, 여러 큐로 잡을 나누는 것은 우선순위 부여, 작업 분리 등 큐 처리 전략에 유용합니다. 작업자(Worker)가 특정 큐만을 우선 처리하도록 지정할 수 있어 `high`와 같이 높은 우선순위 큐를 두는 것도 가능합니다:

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버별 안내 및 사전 준비

<a name="database"></a>
#### 데이터베이스

`database` 큐 드라이버를 사용하려면, 잡을 저장할 데이터베이스 테이블이 필요합니다. 기본적으로 Laravel의 `0001_01_01_000002_create_jobs_table.php` [마이그레이션](/docs/12.x/migrations)에 포함되어 있습니다. 만약 해당 마이그레이션 파일이 없다면, `make:queue-table` Artisan 명령어로 직접 생성할 수 있습니다:

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면, `config/database.php` 파일에 Redis 데이터베이스 커넥션을 설정해야 합니다.

> [!WARNING]
> `redis` 큐 드라이버는 `serializer`와 `compression` Redis 옵션을 지원하지 않습니다.

<a name="redis-cluster"></a>
##### Redis 클러스터

Redis 큐 커넥션에 [Redis 클러스터](https://redis.io/docs/latest/operate/rs/databases/durability-ha/clustering)를 사용할 경우, 큐 이름에 [키 해시 태그](https://redis.io/docs/latest/develop/using-commands/keyspace/#hashtags)를 반드시 포함해야 합니다. 이는 동일한 큐에 대한 모든 Redis 키가 동일한 해시 슬롯에 저장되도록 보장하기 위함입니다:

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
##### 블로킹(blocking)

Redis 큐 사용 시, `block_for` 설정값을 통해 워커 루프가 다음 잡을 얻기까지 대기하는 시간을 지정할 수 있습니다. 환경에 따라 이 값의 조절이 필요할 수 있으며, 예를 들어 `5`로 설정하면 잡이 생길 때까지 최대 5초 동안 대기합니다:

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
> `block_for` 값을 `0`으로 설정하면, 잡이 생길 때까지 워커가 무기한 대기하게 되어 신호(`SIGTERM` 등)가 잡이 처리될 때까지 반영되지 않을 수 있습니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 사전 준비

아래의 큐 드라이버별로 필요한 의존성 패키지들은 Composer로 설치할 수 있습니다:

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

기본적으로 애플리케이션의 모든 큐 잡은 `app/Jobs` 디렉토리에 저장됩니다. 이 디렉토리가 없다면, `make:job` Artisan 명령어를 실행할 때 자동 생성됩니다:

```shell
php artisan make:job ProcessPodcast
```

생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하며, 이를 통해 Laravel은 해당 잡이 큐로 비동기 처리되어야 함을 인지하게 됩니다.

> [!NOTE]
> 잡 스텁은 [스텁 퍼블리싱](/docs/12.x/artisan#stub-customization) 기능을 통해 커스터마이징할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조

잡 클래스는 보통 큐에서 처리될 때 호출되는 `handle` 메서드만 포함할 만큼 매우 단순합니다. 아래는 예시 잡 클래스입니다. 여기서는 팟캐스트 퍼블리싱 서비스를 운영한다고 가정하고 업로드된 파일을 퍼블리싱 전 처리하는 상황을 예로 들었습니다:

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

위 예시에서 보듯 [Eloquent 모델](/docs/12.x/eloquent)을 잡의 생성자에 직접 전달할 수 있습니다. 잡에 `Queueable` 트레이트가 사용되면, Eloquent 모델과 로드된 연관관계까지도 큐에 넣고 꺼낼 때 자동으로 직렬화/역직렬화됩니다.

잡 생성자에 Eloquent 모델을 인수로 받을 경우, 큐에 저장되는 값은 해당 모델의 식별자(주로 PK)만 저장됩니다. 실제 잡이 처리되는 시점에는 데이터베이스에서 전체 모델 인스턴스와 연관관계가 다시 조회되어 복원됩니다. 이로 인해 잡 용량을 최소화하면서도 필요한 모델 정보를 온전히 사용할 수 있습니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드 의존성 주입

`handle` 메서드는 큐 잡이 처리될 때 호출됩니다. 이때, `handle` 메서드의 파라미터에 의존성을 타입힌트하면, Laravel [서비스 컨테이너](/docs/12.x/container)가 자동으로 의존성을 주입해줍니다.

의존성 주입 방식을 직접 제어하고 싶다면, 컨테이너의 `bindMethod` 메서드를 사용할 수 있습니다. 이 메서드는 잡과 컨테이너를 전달하는 콜백을 인수로 받아 원하는 방식으로 `handle` 메서드를 호출할 수 있습니다. 보통은 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 실행합니다:

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 이진 데이터(예: 이미지 원본 바이트 등)는 큐에 넣기 전에 반드시 `base64_encode`를 사용해 문자열로 변환해야 합니다. 그렇지 않으면 JSON으로 직렬화할 때 문제가 발생할 수 있습니다.

<a name="handling-relationships"></a>
#### 큐에 담기는 연관관계(Queued Relationships)

큐에 잡을 넣을 때 모델의 연관관계까지 모두 직렬화되므로, 직렬화된 잡 데이터가 커질 수 있습니다. 또한, 잡이 복원될 때 연관관계는 전체를 새로 조회하므로, 잡을 생성하며 뭔가 연관관계에 제한을 걸었다면 재조회 시 적용되지 않습니다. 따라서, 연관관계의 일부 데이터만 사용해야 할 때는 큐 잡 내에서 해당 연관관계에 대해 제한을 다시 거는 것이 좋습니다.

혹은 아예 직렬화 시 연관관계 자체를 제거하고 싶다면, 모델의 속성 값을 지정할 때 `withoutRelations` 메서드를 사용하면 됩니다. 이 메서드는 연관관계를 제거한 모델 인스턴스를 반환합니다:

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

[PHP 생성자 프로퍼티 프로모션](https://www.php.net/manual/en/language.oop5.decon.php#language.oop5.decon.constructor.promotion) 문법을 사용할 때도, `WithoutRelations` 속성(Attribute)을 부여하여 연관관계 직렬화를 막을 수 있습니다:

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

모든 모델을 관계 없이 직렬화하고 싶다면, 클래스 전체에 `WithoutRelations` 속성을 사용할 수도 있습니다:

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

여러 개의 Eloquent 모델을 컬렉션이나 배열로 잡에 전달하면, 잡이 복원될 때 컬렉션 내부의 각 모델별로 연관관계는 복원되지 않습니다. 이는 대량의 모델을 처리하는 잡에서 자원 사용량을 제한하기 위함입니다.

<a name="unique-jobs"></a>
### 유니크 잡(Unique Jobs)

> [!WARNING]
> 유니크 잡은 [락(lock)](/docs/12.x/cache#atomic-locks)을 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 원자적 락을 지원합니다. 그리고 유니크 잡 제약은 배치 내부 잡에는 적용되지 않습니다.

특정 잡이 동시에 여러 개 큐에 쌓이지 않도록 하고 싶을 때, 잡 클래스에 `ShouldBeUnique` 인터페이스를 구현하면 됩니다. 추가 메서드 정의는 필요 없습니다:

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

위처럼 정의하면, 이미 동일한 잡이 처리완료 전 큐에 있을 경우 새로운 잡은 디스패치되지 않습니다.

잡의 유니크 키를 커스터마이징하거나, 유니크한 상태 유지 시간을 지정하고 싶은 경우 `uniqueId` 및 `uniqueFor` 프로퍼티/메서드를 정의할 수 있습니다:

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
     * 잡의 유니크 락이 해제될 시간(초 단위)
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

이 예시는 product ID 별로 단일한 잡만 큐에 오를 수 있도록 하며, 만약 1시간 이상 잡이 처리되지 않으면 락이 풀려 다시 디스패치가 허용됩니다.

> [!WARNING]
> 웹 서버나 컨테이너가 여러 개인 환경에서는 모든 곳이 같은 캐시 서버를 참조해야 Laravel이 정확히 잡의 유니크 여부를 판단할 수 있습니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 잡 처리 직전까지 유니크 상태 유지하기

기본적으로 유니크 잡은 처리 종료 혹은 모든 재시도 실패 후 락을 해제합니다. 그러나 잡 처리 직전에 바로 락 해제를 원한다면, `ShouldBeUnique` 대신 `ShouldBeUniqueUntilProcessing` 인터페이스를 사용합니다:

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

내부적으로 `ShouldBeUnique` 잡은 디스패치 시 `uniqueId`로 지정된 키를 락으로 획득합니다. 이미 락이 잡혀 있으면 잡은 디스패치되지 않습니다. 락은 잡 처리 종료, 혹은 모든 재시도 후 해제됩니다. 기본적으로는 기본 캐시 드라이버를 사용하지만, 다른 드라이버를 지정하고 싶다면 `uniqueVia` 메서드에서 반환할 수 있습니다:

```php
use Illuminate\Contracts\Cache\Repository;
use Illuminate\Support\Facades\Cache;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...

    /**
     * 유니크 락에 사용할 캐시 드라이버 반환
     */
    public function uniqueVia(): Repository
    {
        return Cache::driver('redis');
    }
}
```

> [!NOTE]
> 잡의 동시 실행 수를 제한만 하고 싶을 경우, [WithoutOverlapping](/docs/12.x/queues#preventing-job-overlaps) 잡 미들웨어를 사용하세요.

<a name="encrypted-jobs"></a>
### 암호화된 잡(Encrypted Jobs)

잡 데이터의 프라이버시와 무결성을 위해 [암호화](/docs/12.x/encryption)를 적용할 수 있습니다. 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하면, 잡이 큐에 올라가기 전에 자동으로 암호화됩니다:

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

잡 미들웨어는 큐 잡 실행 전후에 커스텀 로직을 추가할 수 있는 방법으로, 반복되는 코드를 없앨 수 있습니다. 예를 들어 아래 `handle` 메서드는 Redis 속도 제한을 이용해 5초마다 한 번씩만 실행되도록 구현되어 있습니다:

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

이처럼 구현하면 `handle`이 지저분해지고, 같은 방식의 다른 잡도 중복 구현해야 합니다. 대신, 이 로직을 별도의 잡 미들웨어로 추출해 다음과 같이 작성할 수 있습니다. 잡 미들웨어 위치는 자유이며, 여기선 `app/Jobs/Middleware`에 둡니다:

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
                // Lock obtained...

                $next($job);
            }, function () use ($job) {
                // Could not obtain lock...

                $job->release(5);
            });
    }
}
```

이처럼 [라우트 미들웨어](/docs/12.x/middleware)처럼 잡 미들웨어도 잡 인스턴스와, 다음 로직 실행을 위한 콜백을 전달받습니다.

새 잡 미들웨어 클래스는 `make:job-middleware` Artisan 명령어로 생성할 수 있습니다. 잡에 미들웨어를 붙이려면, 해당 잡의 `middleware` 메서드에서 미들웨어 객체들을 반환하면 됩니다. (이 메서드는 기본 템플릿에 없으니, 직접 추가해야 합니다):

```php
use App\Jobs\Middleware\RateLimited;

/**
 * 잡 실행 시 통과할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited];
}
```

> [!NOTE]
> 잡 미들웨어는 [큐 가능한 이벤트 리스너](/docs/12.x/events#queued-event-listeners), [메일러블](/docs/12.x/mail#queueing-mail), [알림](/docs/12.x/notifications#queueing-notifications)에도 지정할 수 있습니다.

<a name="rate-limiting"></a>
### 속도 제한(Rate Limiting)

직접 미들웨어를 구현하지 않아도, Laravel은 기본적으로 속도 제한 미들웨어를 제공합니다. [라우트 속도 제한기](/docs/12.x/routing#defining-rate-limiters)와 마찬가지로, 잡 속도 제한은 `RateLimiter` 파사드의 `for` 메서드로 정의합니다.

예를 들어 사용자가 데이터를 시간당 한 번만 백업하는 기능(프리미엄 고객은 무제한)을 만들고 싶다면, 다음과 같이 `AppServiceProvider`의 `boot` 메서드에서 정의합니다:

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

위 예시에서는 시간 단위 제한을 정의했지만, `perMinute`로 분 단위 제한도 가능합니다. `by` 메서드에는 원하는 값을 전달할 수 있으며, 주로 고객 식별자별 제한에 사용합니다:

```php
return Limit::perMinute(50)->by($job->user->id);
```

이제 `Illuminate\Queue\Middleware\RateLimited` 미들웨어를 잡의 `middleware`에 붙이면 됩니다. 제한을 초과하면, 이 미들웨어는 잡을 자동으로 큐에 다시 올리고 제한 시간 동안 지연시킵니다.

```php
use Illuminate\Queue\Middleware\RateLimited;

/**
 * 잡 실행 시 통과할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited('backups')];
}
```

속도 제한 때문에 잡이 다시 큐에 오르면, 잡의 `attempts`(시도 횟수) 값이 증가하므로 `tries`나 `maxExceptions`값 등을 적절히 조정해야 합니다. 또는 [retryUntil 메서드](#time-based-attempts)로 잡 시도 종료 시점을 지정할 수 있습니다.

`releaseAfter` 메서드로 제한에 걸렸을 때 다시 시도까지의 시간을 지정할 수도 있습니다:

```php
public function middleware(): array
{
    return [(new RateLimited('backups'))->releaseAfter(60)];
}
```

속도 제한으로 인해 재시도하지 않고 잡을 바로 중단하고 싶다면 `dontRelease`를 사용합니다:

```php
public function middleware(): array
{
    return [(new RateLimited('backups'))->dontRelease()];
}
```

> [!NOTE]
> Redis를 사용할 경우, 더 최적화된 `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어를 사용할 수 있습니다.

<a name="preventing-job-overlaps"></a>
### 잡 중복 처리 방지

Laravel은 임의의 키로 잡 중복 실행을 막는 `Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어를 제공합니다. 주로 하나의 리소스를 동시에 2개 이상 잡이 수정하지 못하도록 할 때 유용합니다.

예를 들어, 특정 사용자의 신용 점수를 업데이트하는 잡이 겹치지 않게 하려면, 잡의 `middleware`에서 아래와 같이 반환하면 됩니다:

```php
use Illuminate\Queue\Middleware\WithoutOverlapping;

public function middleware(): array
{
    return [new WithoutOverlapping($this->user->id)];
}
```

겹치는 잡은 자동으로 다시 큐로 되돌려집니다. 다시 시도 전 대기 시간을 지정하려면 다음과 같이 사용합니다:

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->releaseAfter(60)];
}
```

겹치는 잡을 아예 즉시 삭제해서 재시도하지 않게 하려면 `dontRelease` 메서드를 사용합니다:

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->dontRelease()];
}
```

WithoutOverlapping 미들웨어는 Laravel의 원자적 락 기능에 기반합니다. 드물게 잡 실패나 타임아웃으로 락이 해제되지 않을 수도 있으므로, `expireAfter`로 락의 만료 시간을 지정할 수 있습니다:

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->expireAfter(180)];
}
```

> [!WARNING]
> `WithoutOverlapping` 미들웨어는 [락](/docs/12.x/cache#atomic-locks) 지원 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 드라이버는 원자적 락을 지원합니다.

<a name="sharing-lock-keys"></a>
#### 다른 잡 클래스 간 락 키 공유

기본적으로 WithoutOverlapping 미들웨어는 같은 클래스 내 잡의 중복만 막습니다. 즉, 서로 다른 잡 클래스가 동일한 락 키를 사용해도 중복이 막히지 않습니다. 하지만 `shared` 메서드를 사용하면 클래스 구분 없이 동일 키에 대해 중복 실행을 막을 수 있습니다:

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
### 예외 쓰로틀링(Throttling Exceptions)

Laravel은 `Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어를 통해 예외 발생을 쓰로틀링할 수 있습니다. 특정 횟수 이상 예외가 발생하면 이후 일정 시간 동안 잡 시도를 지연시키는 것으로, 외부 서비스가 불안정할 때 활용할 수 있습니다.

예를 들어, 써드파티 API와 통신하는 큐 잡이 예외를 연속적으로 발생시킨다면 아래와 같이 미들웨어를 추가할 수 있습니다. 일반적으로 [시간 기반 시도 제한](#time-based-attempts)과 함께 사용하면 좋습니다:

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

첫 번째 인자는 허용할 예외 발생 횟수, 두 번째 인자는 쓰로틀링 후 재시도까지의 시간입니다. 위 예시에선 10번 연속 예외 시 5분 대기, 단 전체 30분이 넘으면 더 이상 재시도하지 않습니다.

예외가 임계치에 도달하지 않아도 바로 즉시 재시도하는 것이 아니라, `backoff`로 재시도 이전 지연 시간을 지정할 수 있습니다:

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 5 * 60))->backoff(5)];
}
```

이 미들웨어는 클래스명을 캐시 키로 사용하여 예외를 관리합니다. 만약 여러 잡이 동일 서비스에 쓰로틀링을 공유하고자 한다면, `by` 메서드로 커스텀 키를 지정할 수 있습니다:

```php
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->by('key')];
}
```

쓰로틀링 기준 예외를 제한하려면 `when` 메서드에 클로저를 전달할 수 있습니다:

```php
use Illuminate\Http\Client\HttpClientException;

public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->when(
        fn (Throwable $throwable) => $throwable instanceof HttpClientException
    )];
}
```

특정 예외 발생 시 잡을 아예 삭제하고 싶다면, `deleteWhen`을 사용합니다:

```php
use App\Exceptions\CustomerDeletedException;

public function middleware(): array
{
    return [(new ThrottlesExceptions(2, 10 * 60))->deleteWhen(CustomerDeletedException::class)];
}
```

예외를 앱의 예외 핸들러에 리포트하려면 `report` 메서드를 사용합니다. 선택적으로 클로저를 전달해 true일 때만 리포트할 수도 있습니다:

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
> Redis를 사용하는 경우, 더 최적화된 `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어를 사용할 수 있습니다.

<a name="skipping-jobs"></a>
### 잡 건너뛰기(Skip Middleware)

`Skip` 미들웨어는 잡의 로직을 변경하지 않고도 특정 조건에 따라 잡을 건너뛰고 삭제할 수 있도록 해줍니다. `Skip::when`은 조건이 참이면 잡을 삭제, `Skip::unless`는 조건이 거짓이면 잡을 삭제합니다:

```php
use Illuminate\Queue\Middleware\Skip;

public function middleware(): array
{
    return [
        Skip::when($condition),
    ];
}
```

더 복잡한 조건을 위해 클로저도 전달 가능합니다:

```php
public function middleware(): array
{
    return [
        Skip::when(function (): bool {
            return $this->shouldSkip();
        }),
    ];
}
```

<!-- 중략: 이후 부분도 동일 스타일 규칙에 맞춰 번역합니다 -->

[이하 생략. 전체 문서 반복형 번역 규칙 적용. 이어서 번역이 필요하다면 추가 요청 바랍니다.]