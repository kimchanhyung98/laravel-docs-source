# 큐 (Queues)

- [소개](#introduction)
    - [커넥션과 큐의 차이점](#connections-vs-queues)
    - [드라이버 노트 및 전제 조건](#driver-prerequisites)
- [잡 생성](#creating-jobs)
    - [잡 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [유니크 잡](#unique-jobs)
    - [암호화된 잡](#encrypted-jobs)
- [잡 미들웨어](#job-middleware)
    - [레이트 리미팅](#rate-limiting)
    - [잡 중복 방지](#preventing-job-overlaps)
    - [예외 제한](#throttling-exceptions)
    - [잡 건너뛰기](#skipping-jobs)
- [잡 디스패치](#dispatching-jobs)
    - [지연 디스패치](#delayed-dispatching)
    - [동기 디스패치](#synchronous-dispatching)
    - [잡과 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [잡 체이닝](#job-chaining)
    - [큐와 커넥션 사용자 지정](#customizing-the-queue-and-connection)
    - [최대 시도 횟수 및 타임아웃 값 지정](#max-job-attempts-and-timeout)
    - [에러 처리](#error-handling)
- [잡 배칭](#job-batching)
    - [배치 가능 잡 정의](#defining-batchable-jobs)
    - [배치 디스패치](#dispatching-batches)
    - [체인과 배치](#chains-and-batches)
    - [배치에 잡 추가](#adding-jobs-to-batches)
    - [배치 검사](#inspecting-batches)
    - [배치 취소](#cancelling-batches)
    - [배치 실패](#batch-failures)
    - [배치 정리](#pruning-batches)
    - [DynamoDB에 배치 저장](#storing-batches-in-dynamodb)
- [클로저 큐잉](#queueing-closures)
- [큐 워커 실행](#running-the-queue-worker)
    - [`queue:work` 명령어](#the-queue-work-command)
    - [큐 우선순위](#queue-priorities)
    - [큐 워커와 배포](#queue-workers-and-deployment)
    - [잡 만료 및 타임아웃](#job-expirations-and-timeouts)
- [Supervisor 설정](#supervisor-configuration)
- [실패 잡 처리](#dealing-with-failed-jobs)
    - [실패 잡 정리](#cleaning-up-after-failed-jobs)
    - [실패 잡 재시도](#retrying-failed-jobs)
    - [누락된 모델 무시](#ignoring-missing-models)
    - [실패 잡 정리](#pruning-failed-jobs)
    - [DynamoDB에 실패 잡 저장](#storing-failed-jobs-in-dynamodb)
    - [실패 잡 저장 비활성화](#disabling-failed-job-storage)
    - [실패 잡 이벤트](#failed-job-events)
- [큐에서 잡 비우기](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [잡 일부만 가짜로 처리하기](#faking-a-subset-of-jobs)
    - [잡 체인 테스트](#testing-job-chains)
    - [잡 배치 테스트](#testing-job-batches)
    - [잡/큐 상호작용 테스트](#testing-job-queue-interactions)
- [잡 이벤트](#job-events)

<a name="introduction"></a>
## 소개 (Introduction)

웹 애플리케이션을 구축하면서, 예를 들어 업로드된 CSV 파일을 파싱하고 저장하는 작업처럼, 일반적인 웹 요청 도중 실행하기에는 너무 오래 걸리는 작업들이 있을 수 있습니다. 다행히 Laravel은 백그라운드에서 처리될 수 있는 큐잉된 잡을 쉽게 만들 수 있게 해줍니다. 시간이 오래 걸리는 작업을 큐로 옮김으로써, 애플리케이션은 웹 요청에 더욱 빠르게 응답할 수 있어 사용자 경험이 향상됩니다.

Laravel 큐는 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 또는 관계형 데이터베이스 같은 다양한 큐 백엔드에 걸쳐 통합된 큐잉 API를 제공합니다.

Laravel의 큐 설정은 `config/queue.php` 설정 파일에 저장됩니다. 이 파일에서 데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 드라이버와, 잡을 즉시 실행하는 동기식 드라이버(로컬 개발 환경에서 사용)를 위한 각각의 커넥션 구성을 찾을 수 있습니다. 또한 큐에 있는 잡을 폐기하는 `null` 드라이버도 포함됩니다.

> [!NOTE]  
> Laravel은 이제 Redis 기반 큐를 위한 멋진 대시보드 및 설정 시스템인 Horizon을 제공합니다. 자세한 내용은 전체 [Horizon 문서](/docs/11.x/horizon)를 참조하세요.

<a name="connections-vs-queues"></a>
### 커넥션과 큐의 차이점 (Connections vs. Queues)

Laravel 큐를 시작하기 전에, "커넥션"과 "큐"의 차이점을 이해하는 것이 중요합니다. `config/queue.php` 파일의 `connections` 설정 배열은 Amazon SQS, Beanstalk, Redis 같은 백엔드 큐 서비스의 커넥션을 정의합니다. 하지만 하나의 큐 커넥션은 여러 개의 "큐"를 가질 수 있으며, 이는 서로 다른 스택이나 잡의 더미로 생각할 수 있습니다.

`queue` 설정 파일에서는 각 커넥션 구성에 `queue` 속성이 포함되어 있습니다. 이 속성은 해당 커넥션에 잡이 보내질 때 기본 큐를 의미합니다. 즉, 명시적으로 어느 큐로 보낼지 지정하지 않는다면, 잡은 커넥션 설정의 `queue` 속성에 정의된 큐에 처리됩니다:

```php
use App\Jobs\ProcessPodcast;

// 이 잡은 기본 커넥션의 기본 큐로 전송됩니다...
ProcessPodcast::dispatch();

// 이 잡은 기본 커넥션의 "emails" 큐로 전송됩니다...
ProcessPodcast::dispatch()->onQueue('emails');
```

일부 애플리케이션은 단순히 하나의 큐만 사용하여 여러 큐에 잡을 넣지 않아도 됩니다. 하지만 두 개 이상의 큐에 잡을 넣으면 잡 처리 우선순위를 지정하거나 분할할 때 매우 유용합니다. Laravel 큐 워커는 우선순위에 따라 어떤 큐를 처리할지 지정할 수 있기 때문입니다. 예를 들어 `high` 큐에 잡을 넣고, 그 우선순위가 더 높은 큐를 먼저 처리하도록 워커를 실행할 수 있습니다:

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버 노트 및 전제 조건 (Driver Notes and Prerequisites)

<a name="database"></a>
#### 데이터베이스

`database` 큐 드라이버를 사용하려면 잡을 저장할 데이터베이스 테이블이 필요합니다. 보통 Laravel의 기본 마이그레이션인 `0001_01_01_000002_create_jobs_table.php`가 포함되어 있지만, 만약 없을 경우 `make:queue-table` Artisan 명령어로 테이블 생성을 위한 마이그레이션 파일을 만들 수 있습니다:

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면 `config/database.php` 파일에서 Redis 데이터베이스 커넥션을 설정해야 합니다.

> [!WARNING]  
> Redis 큐 드라이버는 `serializer` 와 `compression` Redis 옵션을 지원하지 않습니다.

**Redis 클러스터**

만약 Redis 큐 커넥션이 Redis 클러스터를 사용한다면, 큐 이름에 [key hash tag](https://redis.io/docs/reference/cluster-spec/#hash-tags)를 포함해야 합니다. 이는 해당 큐의 모든 Redis 키가 같은 해시 슬롯에 위치하도록 보장하기 위해 필수입니다:

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

**블로킹**

Redis 큐를 사용할 때, `block_for` 설정 옵션을 사용하여 워커가 작업 대기 중 새 잡을 기다리는 대기 시간을 지정할 수 있습니다. 이는 지속적으로 Redis를 폴링하는 것보다 효율적일 수 있습니다. 예를 들어, `5`로 설정하면 5초간 작업 대기를 위해 블록됩니다:

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
> `block_for`를 `0`으로 설정하면 워커가 잡이 만들어질 때까지 무한정 블로킹되며, `SIGTERM` 같은 신호를 잡을 때까지 다음 작업이 실행되기 전까지 처리하지 못합니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 전제 조건

아래 큐 드라이버를 사용하려면 필요한 의존성이 있습니다. 보통 Composer 패키지 매니저로 설치합니다:

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~2.0` 또는 phpredis PHP 확장
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`

<a name="creating-jobs"></a>
## 잡 생성 (Creating Jobs)

<a name="generating-job-classes"></a>
### 잡 클래스 생성 (Generating Job Classes)

기본적으로 애플리케이션의 큐에 넣을 잡은 `app/Jobs` 디렉터리에 저장됩니다. 만약 `app/Jobs` 디렉터리가 없다면, `make:job` Artisan 명령어를 실행할 때 자동으로 생성됩니다:

```shell
php artisan make:job ProcessPodcast
```

생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하며, 이를 통해 Laravel에게 이 잡을 비동기적으로 큐에 넣어 실행해야 함을 알립니다.

> [!NOTE]  
> 잡 스텁은 [스텁 퍼블리싱](/docs/11.x/artisan#stub-customization)을 통해 커스터마이징할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조

잡 클래스는 매우 단순해서 보통 `handle` 메서드만 포함하며, 잡이 큐에서 처리될 때 이 메서드가 호출됩니다. 예를 들어 팟캐스트 게시 서비스를 관리하며, 업로드된 팟캐스트 파일을 게시 전에 처리하는 잡 클래스를 살펴봅시다:

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
     * 새 잡 인스턴스 생성.
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

이 예제에서, 생성자에 직접 [Eloquent 모델](/docs/11.x/eloquent)을 전달했습니다. `Queueable` 트레이트 덕분에 Eloquent 모델과 그 연관관계가 잡을 큐에 넣고 처리하는 과정에서 효과적으로 직렬화/역직렬화됩니다.

만약 잡이 Eloquent 모델을 생성자로 받으면, 큐에는 모델 식별자만 직렬화됩니다. 잡이 처리될 때 큐 시스템은 데이터베이스에서 해당 모델 인스턴스와 연관된 로드된 관계들을 자동으로 다시 가져옵니다. 이러한 모델 직렬화 방식 덕분에 보다 작은 크기의 잡 페이로드를 큐 드라이버로 보낼 수 있습니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드 의존성 주입

`handle` 메서드는 잡이 큐에서 처리될 때 호출됩니다. 이 메서드는 타입힌트를 이용해 의존성을 주입받을 수 있으며, Laravel [서비스 컨테이너](/docs/11.x/container)가 자동으로 이들을 주입합니다.

컨테이너가 `handle` 메서드에 의존성을 주입하는 방식을 완전 제어하려면, 컨테이너의 `bindMethod` 메서드를 사용하세요. `bindMethod`는 잡과 컨테이너를 전달받는 콜백을 인수로 받으며, 이 콜백 내에서 직접 `handle` 메서드를 호출할 수 있습니다. 보통 `App\Providers\AppServiceProvider` 서비스 프로바이더의 `boot` 메서드에서 호출합니다:

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]  
> 원시 이미지 데이터 같은 바이너리 데이터는 직렬화 과정에서 JSON 직렬화가 되지 않을 수 있으니, 잡에 전달하기 전에 `base64_encode` 함수를 통해 인코딩하세요.

<a name="handling-relationships"></a>
#### 큐잉된 관계(Relationships)

로드된 Eloquent 모델 관계도 잡이 큐에 직렬화될 때 함께 저장됩니다. 따라서 경우에 따라 직렬화된 잡 문자열이 매우 커질 수 있습니다. 게다가 잡 역직렬화 후 모델 관계를 다시 데이터베이스에서 가져올 때는, 직렬화 이전에 모델에 적용된 관계 제약 조건들이 무시되고 관계 전체가 불러와집니다. 특정 관계의 부분집합만 다루고 싶다면, 잡 실행 시점에 해당 관계에 다시 제약 조건을 걸어주어야 합니다.

관계를 직렬화하지 않으려면 모델 객체에 `withoutRelations` 메서드를 호출해 관계가 제외된 모델 객체를 얻어 속성에 할당할 수 있습니다:

```php
/**
 * 새 잡 인스턴스 생성.
 */
public function __construct(
    Podcast $podcast,
) {
    $this->podcast = $podcast->withoutRelations();
}
```

PHP 생성자 프로퍼티 승격을 사용할 때, Eloquent 모델의 관계를 직렬화하지 않으려면 `WithoutRelations` 속성을 사용할 수 있습니다:

```php
use Illuminate\Queue\Attributes\WithoutRelations;

/**
 * 새 잡 인스턴스 생성.
 */
public function __construct(
    #[WithoutRelations]
    public Podcast $podcast,
) {}
```

만약 잡에 단일 모델 대신 컬렉션이나 배열 형태의 Eloquent 모델이 전달되면, 잡 역직렬화 후 모델 내부의 관계는 회복되지 않습니다. 이는 많은 모델을 처리하는 잡에서 과도한 자원 사용을 방지하기 위함입니다.

<a name="unique-jobs"></a>
### 유니크 잡 (Unique Jobs)

> [!WARNING]  
> 유니크 잡은 [락](/docs/11.x/cache#atomic-locks) 지원하는 캐시 드라이버가 필요합니다. `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 현재 지원합니다. 그리고 유니크 제약은 배치 내 잡에는 적용되지 않습니다.

특정 잡 유형이 큐에 단 하나만 존재하도록 보장하고 싶을 수 있습니다. 이럴 때 잡 클래스에서 `ShouldBeUnique` 인터페이스를 구현하면 됩니다. 이 인터페이스 구현 시 추가 메서드를 정의할 필요는 없습니다:

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    ...
}
```

위 예제에서 `UpdateSearchIndex` 잡은 유니크하므로, 이미 큐에 해당 잡 인스턴스가 존재하고 처리 중이라면 중복되어 디스패치되지 않습니다.

경우에 따라 유니크를 결정하는 "키"를 지정하거나 유니크 상태가 유지되는 기간(타임아웃)을 설정하려면, `uniqueId` 메서드와 `uniqueFor` 프로퍼티 또는 메서드를 잡 클래스 내에 정의하세요:

```php
<?php

use App\Models\Product;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    /**
     * 상품 인스턴스.
     *
     * @var \App\Product
     */
    public $product;

    /**
     * 유니크 락 해제까지 초 단위 시간.
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

위 예제에서 같은 상품 ID에 대해서는 잡이 하나만 큐에 존재하며, 이미 큐에 존재하는 잡이 완료되기 전에는 같은 ID의 새 잡이 무시됩니다. 그리고 기존 잡이 1시간(3600초) 안에 처리되지 않으면 락이 풀려 같은 키로 잡을 다시 디스패치할 수 있습니다.

> [!WARNING]  
> 여러 웹 서버 또는 컨테이너에서 잡을 디스패치한다면, 모든 서버가 동일한 중앙 캐시 서버와 통신하게 해야 Laravel이 정확한 유니크 여부를 판단할 수 있습니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 처리 시작 전까지 유니크 유지

기본적으로 유니크 잡은 처리 종료 또는 재시도 실패 시 락이 해제됩니다. 하지만 잡이 처리 직전 즉시 락을 해제하고 싶을 수 있습니다. 이 경우 `ShouldBeUnique` 대신 `ShouldBeUniqueUntilProcessing` 인터페이스를 구현하세요:

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

내부적으로 `ShouldBeUnique` 잡이 디스패치되면 Laravel은 `uniqueId` 키로 [락](/docs/11.x/cache#atomic-locks)을 획득하려 시도합니다. 락 획득에 실패하면 잡은 큐에 디스패치되지 않습니다. 락은 처리 완료 또는 재시도 실패 시 해제됩니다. 기본 캐시 드라이버를 통해 락을 획득하지만, 다른 드라이버를 사용하려면 `uniqueVia` 메서드를 정의하세요:

```php
use Illuminate\Contracts\Cache\Repository;
use Illuminate\Support\Facades\Cache;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    ...

    /**
     * 유니크 잡 락용 캐시 드라이버 반환.
     */
    public function uniqueVia(): Repository
    {
        return Cache::driver('redis');
    }
}
```

> [!NOTE]  
> 단순히 동시 처리 제한만 필요하다면 [`WithoutOverlapping`](/docs/11.x/queues#preventing-job-overlaps) 잡 미들웨어를 사용하는 것이 좋습니다.

<a name="encrypted-jobs"></a>
### 암호화된 잡 (Encrypted Jobs)

Laravel은 작업 데이터의 개인 정보 보호와 무결성을 위해 [암호화](/docs/11.x/encryption)를 지원합니다. 잡 클래스에 `ShouldBeEncrypted` 인터페이스만 추가하면 자동으로 큐에 넣기 전 잡을 암호화합니다:

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

잡 미들웨어는 큐 처리 시 잡 실행을 감싸는 커스텀 로직을 삽입할 수 있게 해 작업 본문에서 중복되는 코드를 줄여줍니다. 예를 들어, Laravel의 Redis 레이트 리미팅 기능을 이용해 5초마다 한 번씩만 잡이 실행되도록 제한하는 `handle` 메서드가 있다고 합시다:

```php
use Illuminate\Support\Facades\Redis;

/**
 * 잡 실행.
 */
public function handle(): void
{
    Redis::throttle('key')->block(0)->allow(1)->every(5)->then(function () {
        info('락 획득됨...');

        // 잡 처리...
    }, function () {
        // 락 획득 실패...

        return $this->release(5);
    });
}
```

이렇게 하면 코드가 레디스 레이트 리미팅 로직으로 복잡해지고 다른 잡에도 반복해서 구현해야 합니다.

대신 잡 미들웨어를 정의하여 레이트 리미팅을 처리할 수 있습니다. Laravel에 미들웨어 기본 위치는 없으므로, 원하는 곳 어디에도 둘 수 있습니다. 여기서는 `app/Jobs/Middleware` 디렉터리에 만들어봅니다:

```php
<?php

namespace App\Jobs\Middleware;

use Closure;
use Illuminate\Support\Facades\Redis;

class RateLimited
{
    /**
     * 큐 잡 처리.
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

추가로, [라우트 미들웨어](/docs/11.x/middleware)처럼, 잡 미들웨어는 처리 중인 잡과 잡 처리를 계속할 콜백을 인수로 받습니다.

미들웨어를 만든 후, 잡 클래스의 `middleware` 메서드에서 미들웨어 인스턴스를 반환하여 적용할 수 있습니다. `make:job` 명령어로 생성한 잡에는 기본적으로 `middleware` 메서드가 없으니 직접 추가해야 합니다:

```php
use App\Jobs\Middleware\RateLimited;

/**
 * 잡이 통과해야 하는 미들웨어 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited];
}
```

> [!NOTE]  
> 잡 미들웨어는 큐에 넣을 수 있는 이벤트 리스너, 발송자(mailables), 알림(notification)에도 할당할 수 있습니다.

<a name="rate-limiting"></a>
### 레이트 리미팅 (Rate Limiting)

직접 레이트 리미팅 잡 미들웨어를 작성하는 대신, Laravel은 잡 전용 레이트 리미팅 미들웨어를 제공합니다. 라우트 레이트 리미터와 비슷하게 `RateLimiter` 파사드의 `for` 메서드로 정의합니다.

예를 들어 일반 사용자는 1시간에 1회만 데이터를 백업할 수 있게 하되, 프리미엄 사용자는 제한 없이 허용한다고 합시다. 이 설정은 `AppServiceProvider`의 `boot` 메서드에서 작성합니다:

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Support\Facades\RateLimiter;

/**
 * 애플리케이션 서비스 부트스트랩.
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

위 예에선 시간 단위 제한을 설정했고, 분 단위 제한은 `perMinute` 메서드를 사용해 쉽게 설정할 수 있습니다. `by` 메서드에는 고객별 구분을 위한 어떤 값이라도 전달할 수 있습니다:

```php
return Limit::perMinute(50)->by($job->user->id);
```

이 레이트 리미터를 잡에 적용하려면 `Illuminate\Queue\Middleware\RateLimited` 미들웨어를 사용하세요. 잡이 제한되는 경우 미들웨어가 지연 시간을 두고 큐에 다시 넣습니다.

```php
use Illuminate\Queue\Middleware\RateLimited;

/**
 * 잡이 통과할 미들웨어를 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited('backups')];
}
```

레이트 제한된 잡이 큐에 다시 들어가도 시도 횟수(`attempts`)는 증가합니다. 따라서 잡 클래스의 `tries` 및 `maxExceptions` 속성을 적절히 조정하거나, [`retryUntil` 메서드](#time-based-attempts)를 사용해 시도 시간을 제한할 수 있습니다.

재시도하지 않고 싶으면 `dontRelease` 메서드를 사용하세요:

```php
/**
 * 잡이 통과할 미들웨어 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new RateLimited('backups'))->dontRelease()];
}
```

> [!NOTE]  
> Redis를 쓴다면 `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어를 사용하면 더 효율적입니다.

<a name="preventing-job-overlaps"></a>
### 잡 중복 방지 (Preventing Job Overlaps)

Laravel은 `Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어를 제공해 키를 기준으로 잡 중복 실행을 방지할 수 있습니다. 이는 한 번에 한 잡만 특정 자원을 수정하도록 할 때 유용합니다.

예를 들어, 같은 사용자 ID에 대해 신용 점수를 갱신하는 잡 중복을 막고 싶다면, 잡 클래스의 `middleware` 메서드에서 다음과 같이 미들웨어를 반환하세요:

```php
use Illuminate\Queue\Middleware\WithoutOverlapping;

/**
 * 잡이 통과할 미들웨어 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new WithoutOverlapping($this->user->id)];
}
```

중복 잡은 큐에 다시 들어가며, 재시도까지 기다리는 시간을 초 단위로 지정할 수도 있습니다:

```php
/**
 * 잡이 통과할 미들웨어 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->releaseAfter(60)];
}
```

중복 잡을 즉시 삭제하여 재시도 방지하려면 `dontRelease`를 사용하세요:

```php
/**
 * 잡이 통과할 미들웨어 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->dontRelease()];
}
```

이 미들웨어는 Laravel의 원자적 락 기능을 기반으로 합니다. 가끔 잡이 실패하거나 타임아웃되어 락이 해제되지 않는 경우, 락 만료 시간을 명시적으로 지정할 수 있습니다. 아래 예는 잡이 처리 시작 후 3분 후 락을 해제하도록 설정합니다:

```php
/**
 * 잡이 통과할 미들웨어 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->expireAfter(180)];
}
```

> [!WARNING]  
> `WithoutOverlapping` 미들웨어는 [락](/docs/11.x/cache#atomic-locks)을 지원하는 캐시 드라이버가 필요합니다. `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 등이 지원합니다.

<a name="sharing-lock-keys"></a>
#### 잡 클래스 간 락 키 공유

기본적으로 `WithoutOverlapping` 미들웨어는 동일 클래스 잡에 대해서만 중복을 방지합니다. 서로 다른 잡 클래스가 같은 락 키를 사용하더라도 이를 공유하지 않습니다. 만약 락 키를 여러 잡 클래스 간에 공유하고 싶으면 `shared` 메서드를 호출하세요:

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

Laravel은 `Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어를 제공해 잡의 예외 발생 횟수를 제한할 수 있습니다. 지정 횟수 이상의 예외가 발생하면, 이후 잡 실행은 지연되어 재시도됩니다. 이는 불안정한 외부 API 등과 연동한 잡에 유용합니다.

예를 들어, 외부 API와 상호작용하는 잡을 가정하면 `middleware` 메서드에서 `ThrottlesExceptions`를 반환해 제한할 수 있습니다. 보통 [시간 기반 시도 제한](#time-based-attempts)과 함께 사용합니다:

```php
use DateTime;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡이 통과할 미들웨어 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new ThrottlesExceptions(10, 5 * 60)];
}

/**
 * 잡의 타임아웃 시간.
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(30);
}
```

첫 번째 인자는 최대 예외 허용 횟수, 두 번째 인자는 제한 후 다음 재시도까지의 지연 시간(초)입니다. 위 예제에서는 10회 연속 예외 발생 시 5분 동안 재시도를 지연하며, 30분 간 최대 재시도합니다.

예외 발생 후 제한 횟수 미만이면 보통 즉시 재시도됩니다. 지연 시간(분)을 조절하려면 미들웨어 생성 시 `backoff` 메서드를 호출하세요:

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡이 통과할 미들웨어 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 5 * 60))->backoff(5)];
}
```

내부적으로 이 미들웨어는 캐시 시스템을 사용하며, 잡 클래스명이 캐시 키로 쓰입니다. 만약 여러 잡이 동일 API를 이용하며 통합 제한을 원한다면, `by` 메서드로 키를 오버라이드하세요:

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡이 통과할 미들웨어 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->by('key')];
}
```

또한 전체 예외를 제한하는 기본 동작을 조절하려면, `when` 메서드로 조건부 제한을 줄 수 있습니다. 클로저가 `true`를 반환할 때만 제한됩니다:

```php
use Illuminate\Http\Client\HttpClientException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡이 통과할 미들웨어 반환.
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

발생한 예외를 애플리케이션의 예외 핸들러에 보고하려면 `report` 메서드를 사용합니다. 선택적으로 조건 클로저를 전달해 특정 예외만 보고할 수도 있습니다:

```php
use Illuminate\Http\Client\HttpClientException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡이 통과할 미들웨어 반환.
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
> Redis를 쓴다면 `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어를 사용하는 편이 더 효율적입니다.

<a name="skipping-jobs"></a>
### 잡 건너뛰기 (Skipping Jobs)

`Skip` 미들웨어를 사용하면 잡 코드 수정 없이 조건에 따라 잡을 건너뛰고 삭제할 수 있습니다. `Skip::when`은 조건이 참일 때, `Skip::unless`는 조건이 거짓일 때 잡을 삭제합니다:

```php
use Illuminate\Queue\Middleware\Skip;

/**
 * 잡이 통과할 미들웨어 반환.
 */
public function middleware(): array
{
    return [
        Skip::when($someCondition),
    ];
}
```

또는 복잡한 조건에는 `Closure` 형태로 전달할 수도 있습니다:

```php
use Illuminate\Queue\Middleware\Skip;

/**
 * 잡이 통과할 미들웨어 반환.
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
## 잡 디스패치 (Dispatching Jobs)

잡 클래스를 만든 후에는 자기 자신에서 `dispatch` 메서드를 호출해 디스패치할 수 있습니다. `dispatch`에 전달된 인수는 잡 생성자에 전달됩니다:

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    /**
     * 새 팟캐스트 저장.
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

조건부로 디스패치하려면 `dispatchIf`와 `dispatchUnless` 메서드를 사용할 수 있습니다:

```php
ProcessPodcast::dispatchIf($accountActive, $podcast);

ProcessPodcast::dispatchUnless($accountSuspended, $podcast);
```

새 Laravel 애플리케이션에서는 기본 큐 드라이버가 `sync`입니다. 이 드라이버는 현재 요청에서 잡을 즉시 동기 실행하므로, 로컬 개발 중 편리합니다. 실제 백그라운드 처리용으로 큐잉하려면 `config/queue.php`에서 다른 큐 드라이버를 지정하면 됩니다.

<a name="delayed-dispatching"></a>
### 지연 디스패치 (Delayed Dispatching)

잡이 큐 워커에서 즉시 처리되지 않고 일정 시간 이후에 처리되도록 하려면, `dispatch` 후 `delay` 메서드를 체인으로 붙입니다. 예를 들어, 10분 후에 처리되도록 설정:

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    /**
     * 새 팟캐스트 저장.
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

디폴트 지연(delay)이 잡에 설정되어 있는데 즉시 처리하고 싶으면 `withoutDelay` 메서드를 사용하세요:

```php
ProcessPodcast::dispatch($podcast)->withoutDelay();
```

> [!WARNING]  
> Amazon SQS 큐는 최대 지연 시간 제한이 15분입니다.

<a name="dispatching-after-the-response-is-sent-to-browser"></a>
#### 응답 전송 후 디스패치

웹 서버가 FastCGI인 경우, `dispatchAfterResponse` 메서드를 사용하면 HTTP 응답이 브라우저로 전송된 뒤에 잡을 디스패치합니다. 이렇게 하면 사용자가 작동을 계속할 수 있으면서 백그라운드에서 잡을 실행할 수 있습니다. 보통 메일 전송 같은 1초 정도 걸리는 짧은 작업용입니다. 이 방식의 잡은 큐 워커 없이도 현재 HTTP 요청에서 처리됩니다:

```php
use App\Jobs\SendNotification;

SendNotification::dispatchAfterResponse();
```

또는 `dispatch` 헬퍼로 클로저를 디스패치하고, `afterResponse` 메서드와 체인해 응답 후 실행할 수도 있습니다:

```php
use App\Mail\WelcomeMessage;
use Illuminate\Support\Facades\Mail;

dispatch(function () {
    Mail::to('taylor@example.com')->send(new WelcomeMessage);
})->afterResponse();
```

<a name="synchronous-dispatching"></a>
### 동기 디스패치 (Synchronous Dispatching)

즉시(동기) 잡을 실행하려면 `dispatchSync` 메서드를 사용하세요. 이렇게 하면 작업이 큐에 넣어지지 않고 현재 프로세스에서 바로 실행됩니다:

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    /**
     * 새 팟캐스트 저장.
     */
    public function store(Request $request): RedirectResponse
    {
        $podcast = Podcast::create(/* ... */);

        // 팟캐스트 처리...

        ProcessPodcast::dispatchSync($podcast);

        return redirect('/podcasts');
    }
}
```

<a name="jobs-and-database-transactions"></a>
### 잡과 데이터베이스 트랜잭션 (Jobs & Database Transactions)

데이터베이스 트랜잭션 내에서 잡을 디스패치하는 것은 가능하나, 잡이 올바르게 실행될 수 있도록 주의해야 합니다. 트랜잭션 커밋 전에 잡이 워커에서 처리되면, 트랜잭션 내에서 변경한 모델이나 레코드 데이터가 아직 DB에 반영되지 않았을 수 있습니다. 심지어 트랜잭션 내에서 생성된 레코드는 DB에 존재하지 않을 수 있습니다.

이 문제를 해결하기 위해 Laravel은 몇 가지 방법을 제공합니다. 우선, 큐 연결 설정의 `after_commit` 옵션을 활성화할 수 있습니다:

```php
'redis' => [
    'driver' => 'redis',
    // ...
    'after_commit' => true,
],
```

`after_commit`이 `true`면, 잡을 트랜잭션 안에서 디스패치해도, Laravel은 현재 열려있는 모든 DB 트랜잭션이 커밋될 때까지 잡 실행을 지연합니다. 물론 현재 트랜잭션이 없다면 즉시 디스패치됩니다.

트랜잭션이 예외로 롤백되면, 그 트랜잭션 내에서 디스패치된 잡들은 폐기됩니다.

> [!NOTE]  
> `after_commit` 옵션을 `true`로 설정하면, 대기열화된 이벤트 리스너, 메일 발송자, 알림, 방송 이벤트 역시 모든 DB 트랜잭션이 커밋된 뒤에 디스패치됩니다.

<a name="specifying-commit-dispatch-behavior-inline"></a>
#### 커밋 후 디스패치 동작을 인라인으로 지정

`after_commit` 옵션을 `true`로 설정하지 않아도, 특정 잡에 대해 트랜잭션 커밋 후 디스패치를 지정할 수 있습니다. 디스패치 시 `afterCommit` 메서드를 체인하면 됩니다:

```php
use App\Jobs\ProcessPodcast;

ProcessPodcast::dispatch($podcast)->afterCommit();
```

반대로 `after_commit` 옵션이 `true`라면, 특정 잡에 대해 트랜잭션 커밋 전 즉시 디스패치를 하려면 `beforeCommit` 메서드를 체인하세요:

```php
ProcessPodcast::dispatch($podcast)->beforeCommit();
```

<a name="job-chaining"></a>
### 잡 체이닝 (Job Chaining)

잡 체이닝은 기본 잡 실행 성공 후 일련의 큐 잡을 순차적으로 실행하도록 지정하는 기능입니다. 체인 중 하나가 실패하면 나머지 체인이 실행되지 않습니다. 체인은 `Bus` 파사드의 `chain` 메서드로 실행합니다:

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

클래스 인스턴스 뿐 아니라 클로저도 체인에 포함할 수 있습니다:

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
> 잡에서 `$this->delete()`를 호출해 삭제해도 체인은 중단되지 않습니다. 체인이 멈추려면 체인 중 잡이 실패해야 합니다.

<a name="chain-connection-queue"></a>
#### 체인 커넥션 및 큐 지정

체인 잡에 사용할 커넥션과 큐를 지정하려면 `onConnection` 및 `onQueue` 메서드를 체인합니다. 잡에 명시적으로 지정된 커넥션/큐가 없다면 이 값이 사용됩니다:

```php
Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->onConnection('redis')->onQueue('podcasts')->dispatch();
```

<a name="adding-jobs-to-the-chain"></a>
#### 체인에 잡 추가

체인 내 잡에서 현재 체인 앞이나 뒤에 잡을 추가하는 경우 `prependToChain` 또는 `appendToChain` 메서드를 사용하세요:

```php
/**
 * 잡 실행.
 */
public function handle(): void
{
    // ...

    // 현재 체인 앞에 삽입. 현재 잡 직후 실행...
    $this->prependToChain(new TranscribePodcast);

    // 체인 끝에 추가. 체인 마지막에 실행...
    $this->appendToChain(new TranscribePodcast);
}
```

<a name="chain-failures"></a>
#### 체인 실패 핸들링

체인 내 잡이 실패할 때 호출할 콜백을 `catch` 메서드로 지정할 수 있습니다. 콜백은 실패 예외(`Throwable`)를 인자로 받습니다:

```php
use Illuminate\Support\Facades\Bus;
use Throwable;

Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->catch(function (Throwable $e) {
    // 체인 내 잡 실패 처리...
})->dispatch();
```

> [!WARNING]  
> 체인 콜백은 직렬화되어 큐 작업으로 나중에 실행되므로 `$this` 변수를 사용하지 마세요.

<a name="customizing-the-queue-and-connection"></a>
### 큐와 커넥션 사용자 지정 (Customizing The Queue and Connection)

<a name="dispatching-to-a-particular-queue"></a>
#### 특정 큐에 디스패치

잡을 카테고리화하거나 우선순위를 나누려면, 같은 커넥션 내에서 다른 큐를 지정할 수 있습니다. 디스패치 시 `onQueue` 메서드를 사용하세요:

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    /**
     * 새 팟캐스트 저장.
     */
    public function store(Request $request): RedirectResponse
    {
        $podcast = Podcast::create(/* ... */);

        // 팟캐스트 생성...

        ProcessPodcast::dispatch($podcast)->onQueue('processing');

        return redirect('/podcasts');
    }
}
```

생성자 내 `onQueue` 호출로도 지정 가능합니다:

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    /**
     * 새 잡 인스턴스 생성.
     */
    public function __construct()
    {
        $this->onQueue('processing');
    }
}
```

<a name="dispatching-to-a-particular-connection"></a>
#### 특정 커넥션에 디스패치

여러 큐 커넥션을 사용하는 경우, `onConnection` 메서드로 어느 커넥션을 사용할지 지정하세요:

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    /**
     * 새 팟캐스트 저장.
     */
    public function store(Request $request): RedirectResponse
    {
        $podcast = Podcast::create(/* ... */);

        // 팟캐스트 생성...

        ProcessPodcast::dispatch($podcast)->onConnection('sqs');

        return redirect('/podcasts');
    }
}
```

커넥션과 큐를 함께 지정하려면 두 메서드를 체인하세요:

```php
ProcessPodcast::dispatch($podcast)
    ->onConnection('sqs')
    ->onQueue('processing');
```

잡 생성자에서도 `onConnection` 호출로 커넥션을 지정할 수 있습니다:

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    /**
     * 새 잡 인스턴스 생성.
     */
    public function __construct()
    {
        $this->onConnection('sqs');
    }
}
```

<a name="max-job-attempts-and-timeout"></a>
### 최대 시도 횟수 및 타임아웃 값 지정 (Specifying Max Job Attempts / Timeout Values)

<a name="max-attempts"></a>
#### 최대 시도 횟수

잡 오류 시 무한 재시도하는 걸 방지하려면, 최대 시도 횟수를 제한하세요.

커맨드라인에서 `queue:work` 명령어의 `--tries` 옵션으로 모든 잡에 기본 시도 횟수를 지정할 수 있습니다. 단, 잡 클래스 자체에서 시도 횟수를 지정하면 커맨드 옵션보다 우선합니다:

```shell
php artisan queue:work --tries=3
```

최대 시도를 넘은 잡은 실패로 간주되어 `failed_jobs` 테이블에 저장됩니다. `--tries=0`이면 무제한 재시도입니다.

잡 클래스에서 속성으로 직접 최대 시도 횟수를 지정할 수도 있습니다:

```php
<?php

namespace App\Jobs;

class ProcessPodcast implements ShouldQueue
{
    /**
     * 최대 시도 횟수.
     *
     * @var int
     */
    public $tries = 5;
}
```

동적 제어가 필요하면 `tries` 메서드를 정의하세요:

```php
/**
 * 최대 시도 횟수 반환.
 */
public function tries(): int
{
    return 5;
}
```

<a name="time-based-attempts"></a>
#### 시간 기반 시도 제한

최대 시도 횟수 대신, 잡을 재시도할 최대 기간을 지정할 수도 있습니다. 이를 위해 `retryUntil` 메서드를 정의하고 `DateTime` 인스턴스를 반환하세요:

```php
use DateTime;

/**
 * 잡 타임아웃 시각 반환.
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(10);
}
```

> [!NOTE]  
> [큐잉된 이벤트 리스너](/docs/11.x/events#queued-event-listeners)에서도 `tries` 속성이나 `retryUntil` 메서드를 정의할 수 있습니다.

<a name="max-exceptions"></a>
#### 최대 예외 횟수

때로는 재시도 횟수는 많게 주지만, 지정 횟수 이상의 처리되지 않은 예외가 발생하면 실패로 처리하고 싶을 수 있습니다. 이때는 `maxExceptions` 속성을 지정하세요:

```php
<?php

namespace App\Jobs;

use Illuminate\Support\Facades\Redis;

class ProcessPodcast implements ShouldQueue
{
    /**
     * 최대 시도 횟수.
     *
     * @var int
     */
    public $tries = 25;

    /**
     * 최대 처리 실패 예외 허용 횟수.
     *
     * @var int
     */
    public $maxExceptions = 3;

    /**
     * 잡 실행.
     */
    public function handle(): void
    {
        Redis::throttle('key')->allow(10)->every(60)->then(function () {
            // 락 획득, 팟캐스트 처리...
        }, function () {
            // 락 획득 불가...
            return $this->release(10);
        });
    }
}
```

위 예제는 락 획득 실패 시 10초 후 재시도하며, 최대 25회 재시도 가능합니다. 단, 3회 이상의 처리되지 않은 예외 발생 시 잡은 실패로 처리됩니다.

<a name="timeout"></a>
#### 타임아웃

잡이 보통 어느 정도 시간이 걸리는지 예상 가능할 경우, 타임아웃을 지정할 수 있습니다. 기본값은 60초입니다. 타임아웃을 초과하면 잡을 처리하는 워커 프로세스가 오류로 종료됩니다. 보통 서버의 프로세스 매니저가 자동으로 워커를 재시작합니다.

CLI에서 `queue:work` 명령어 `--timeout` 옵션을 지정해 최대 실행 시간을 바꿀 수 있습니다:

```shell
php artisan queue:work --timeout=30
```

잡 클래스 내 `timeout` 속성을 지정하면 CLI 옵션보다 우선합니다:

```php
<?php

namespace App\Jobs;

class ProcessPodcast implements ShouldQueue
{
    /**
     * 잡 타임아웃 시간 (초).
     *
     * @var int
     */
    public $timeout = 120;
}
```

소켓이나 외부 HTTP 요청처럼 IO 블로킹 작업은 job timeout을 지키지 않을 수 있으니, Guzzle 같은 라이브러리 API에서 별도로 타임아웃을 지정하는 것이 좋습니다.

> [!WARNING]  
> PHP 확장 `pcntl`이 설치되어 있어야 잡 타임아웃을 지정할 수 있습니다. 그리고 잡의 `timeout` 값은 항상 `retry_after` 값보다 작아야 합니다. 그렇지 않으면 잡이 실제 종료 전에 재시도될 수 있습니다.

<a name="failing-on-timeout"></a>
#### 타임아웃 시 실패 처리

타임아웃 발생 시 잡을 실패 처리하려면 잡 클래스 내 `$failOnTimeout` 속성을 `true`로 설정하세요:

```php
/**
 * 타임아웃 시 잡을 실패 처리할지 여부.
 *
 * @var bool
 */
public $failOnTimeout = true;
```

<a name="error-handling"></a>
### 에러 처리 (Error Handling)

잡 실행 중 예외 발생 시, 잡은 자동으로 큐에 다시 들어가 재시도됩니다. 최대 시도 횟수를 초과할 때까지 반복됩니다. 최대 시도 횟수는 CLI `queue:work` 명령어 `--tries` 옵션이나 잡 클래스 속성으로 지정합니다. 워커 실행 방법은 [다음](#running-the-queue-worker)에서 상세히 다룹니다.

<a name="manually-releasing-a-job"></a>
#### 잡 수동 재시도 (Manually Releasing a Job)

원할 경우 잡 내 `release` 메서드를 호출해 잡을 큐에 다시 넣어 늦게 재시도할 수 있습니다:

```php
/**
 * 잡 실행.
 */
public function handle(): void
{
    // ...

    $this->release();
}
```

`release`는 기본적으로 즉시 재시도하도록 큐에 넣습니다. 지연 시간을 주려면 초 단위 정수 또는 `DateTime` 인스턴스를 전달하세요:

```php
$this->release(10);

$this->release(now()->addSeconds(10));
```

<a name="manually-failing-a-job"></a>
#### 잡 수동 실패 처리 (Manually Failing a Job)

잡을 수동으로 실패 처리하려면 `fail` 메서드를 호출하세요:

```php
/**
 * 잡 실행.
 */
public function handle(): void
{
    // ...

    $this->fail();
}
```

잡 실패 이유로 캐치한 예외나 메시지를 전달할 수도 있습니다:

```php
$this->fail($exception);

$this->fail('문제가 발생했습니다.');
```

> [!NOTE]  
> 실패 잡 관련 자세한 내용은 [실패 잡 처리](#dealing-with-failed-jobs) 문서를 참고하세요.

<a name="job-batching"></a>
## 잡 배칭 (Job Batching)

Laravel의 잡 배칭 기능은 여러 잡을 한 번에 실행하고, 배치가 완료되면 후속 동작 실행을 쉽게 만듭니다. 시작하려면, 잡 배치 메타 정보를 저장할 테이블을 만드는 마이그레이션을 생성해야 합니다. `make:queue-batches-table` 명령어로 만드세요:

```shell
php artisan make:queue-batches-table

php artisan migrate
```

<a name="defining-batchable-jobs"></a>
### 배치 가능 잡 정의 (Defining Batchable Jobs)

배치 가능 잡은 일반 큐 잡과 같지만, `Illuminate\Bus\Batchable` 트레이트를 추가해야 합니다. 이 트레이트가 잡이 실행되는 현재 배치를 `batch` 메서드를 통해 반환합니다:

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
     * 잡 실행.
     */
    public function handle(): void
    {
        if ($this->batch()->cancelled()) {
            // 배치가 취소됐는지 확인...

            return;
        }

        // CSV 파일 일부를 임포트...
    }
}
```

<a name="dispatching-batches"></a>
### 배치 디스패치 (Dispatching Batches)

`Bus` 파사드의 `batch` 메서드로 여러 잡을 배치로 묶어 디스패치합니다. 유용한 건 이후 완료 콜백을 정의할 수 있다는 점입니다. `then`, `catch`, `finally` 메서드로 지정하며 각각 `Illuminate\Bus\Batch` 인스턴스를 인자로 받습니다.

예를 들어 CSV 파일 여러 부분을 처리하는 여러 잡 배치를 다음과 같이 디스패치합니다:

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
    // 배치 생성됐으나 잡은 아직 없음...
})->progress(function (Batch $batch) {
    // 잡 하나가 성공적으로 완료됨...
})->then(function (Batch $batch) {
    // 모든 잡 성공 완료...
})->catch(function (Batch $batch, Throwable $e) {
    // 배치 내 첫 번째 잡 실패 감지...
})->finally(function (Batch $batch) {
    // 배치 실행 완료...
})->dispatch();

return $batch->id;
```

배치 아이디 `$batch->id`는 디스패치 후에도 [작업 버스 정보를 조회](#inspecting-batches)할 때 사용합니다.

> [!WARNING]  
> 배치 콜백도 직렬화되어 큐에서 나중에 실행되므로 콜백 내에서 `$this` 변수를 사용하지 마세요. 또, 배치 잡은 DB 트랜잭션 내에서 실행되므로 암묵적 커밋을 발생시키는 쿼리는 사용하지 않는 게 안전합니다.

<a name="naming-batches"></a>
#### 배치 이름 지정

Laravel Horizon, Telescope 같은 도구에서 보다 친숙한 디버깅 정보를 제공하려면 배치에 이름을 줄 수 있습니다. `name` 메서드로 설정하세요:

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // 모든 잡 성공...
})->name('Import CSV')->dispatch();
```

<a name="batch-connection-queue"></a>
#### 배치 커넥션 및 큐 지정

배치 내 모든 잡은 같은 큐 커넥션과 큐에서 실행되어야 하며, `onConnection` 및 `onQueue` 메서드로 지정할 수 있습니다:

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // 모든 잡 성공...
})->onConnection('redis')->onQueue('imports')->dispatch();
```

<a name="chains-and-batches"></a>
### 체인과 배치 (Chains and Batches)

배치 내에서 [체인](#job-chaining) 잡 세트를 정의할 수 있습니다. 예를 들어, 두 개 체인을 병렬 실행하고 둘 다 끝나면 콜백을 실행하는 코드:

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

반대로, 배치 집합을 [체인](#job-chaining) 내에 넣어, 예컨대 팟캐스트 릴리즈를 위한 배치를 먼저 실행하고 릴리즈 알림 배치를 나중에 실행하는 것도 가능합니다:

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
### 배치에 잡 추가 (Adding Jobs to Batches)

웹 요청 중에 너무 많은 잡을 배치할 경우, 초기에 소량의 "로더" 잡을 배치 디스패치해 실행 중에 더 많은 잡을 배치에 동적으로 추가할 수 있습니다. 다음과 같이 `batch` 메서드로 현재 배치 인스턴스를 가져와 `add` 메서드로 잡을 추가하세요:

```php
$batch = Bus::batch([
    new LoadImportBatch,
    new LoadImportBatch,
    new LoadImportBatch,
])->then(function (Batch $batch) {
    // 모든 잡 성공...
})->name('Import Contacts')->dispatch();
```

`LoadImportBatch` 잡 내:

```php
use App\Jobs\ImportContacts;
use Illuminate\Support\Collection;

/**
 * 잡 실행.
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
> 같은 배치에 속한 잡 내에서만 배치에 잡을 추가할 수 있습니다.

<a name="inspecting-batches"></a>
### 배치 검사 (Inspecting Batches)

`Illuminate\Bus\Batch` 인스턴스는 배치 콜백에서 받을 수 있으며, 다음과 같이 여러 속성과 메서드로 배치 상태를 조회할 수 있습니다:

```php
// 배치 UUID
$batch->id;

// 배치 이름 (있다면)
$batch->name;

// 배치에 할당된 총 잡 수
$batch->totalJobs;

// 아직 처리되지 않은 잡 수
$batch->pendingJobs;

// 실패한 잡 수
$batch->failedJobs;

// 지금까지 처리된 잡 수
$batch->processedJobs();

// 배치 진행률(0-100)
$batch->progress();

// 배치 실행 완료 여부
$batch->finished();

// 배치 실행 취소
$batch->cancel();

// 배치가 취소됐는지 여부
$batch->cancelled();
```

<a name="returning-batches-from-routes"></a>
#### 라우트에서 배치 반환

모든 `Illuminate\Bus\Batch` 인스턴스는 JSON 직렬화 가능하므로, 라우트에서 바로 반환해 UI에서 진행률 등을 표시할 수 있습니다.

배치 ID를 이용해 `Bus` 파사드의 `findBatch` 메서드로 배치 정보를 조회할 수 있습니다:

```php
use Illuminate\Support\Facades\Bus;
use Illuminate\Support\Facades\Route;

Route::get('/batch/{batchId}', function (string $batchId) {
    return Bus::findBatch($batchId);
});
```

<a name="cancelling-batches"></a>
### 배치 취소 (Cancelling Batches)

특정 배치 실행을 중단하려면, `Illuminate\Bus\Batch` 인스턴스의 `cancel` 메서드를 호출하세요:

```php
/**
 * 잡 실행.
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

대개 배치 잡은 실행 전 취소 여부를 확인하는 로직을 넣어야 하지만, 편의상 `SkipIfBatchCancelled` 미들웨어를 배치 잡에 붙여 미들웨어로 처리하게 할 수도 있습니다:

```php
use Illuminate\Queue\Middleware\SkipIfBatchCancelled;

/**
 * 잡이 통과할 미들웨어 반환.
 */
public function middleware(): array
{
    return [new SkipIfBatchCancelled];
}
```

<a name="batch-failures"></a>
### 배치 실패 (Batch Failures)

배치 잡이 실패하면, 실패한 첫 번째 잡에 대해 등록된 `catch` 콜백이 호출됩니다.

<a name="allowing-failures"></a>
#### 실패 허용

잡 실패 시 자동으로 배치가 "취소"되는 동작을 끄려면, `allowFailures` 메서드를 배치 디스패치 시 체인하세요:

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // 모든 잡 성공...
})->allowFailures()->dispatch();
```

<a name="retrying-failed-batch-jobs"></a>
#### 실패한 배치 잡 재시도

`queue:retry-batch` Artisan 명령어로 특정 배치에서 실패한 모든 잡을 재시도할 수 있습니다. 배치 UUID를 인수로 전달하세요:

```shell
php artisan queue:retry-batch 32dbc76c-4f82-4749-b610-a639fe0099b5
```

<a name="pruning-batches"></a>
### 배치 정리 (Pruning Batches)

`job_batches` 테이블이 빨리 커지는 것을 방지하려면, 스케줄러에서 `queue:prune-batches` 명령을 매일 실행하도록 설정하세요:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches')->daily();
```

기본적으로 완료된 배치 중 24시간 지난 레코드를 삭제합니다. `--hours` 옵션으로 보관 기간을 조절할 수 있습니다:

```php
Schedule::command('queue:prune-batches --hours=48')->daily();
```

미완료 배치 또한 삭제하려면 `--unfinished` 옵션을 추가합니다:

```php
Schedule::command('queue:prune-batches --hours=48 --unfinished=72')->daily();
```

취소된 배치도 삭제하려면 `--cancelled` 옵션을 추가하세요:

```php
Schedule::command('queue:prune-batches --hours=48 --cancelled=72')->daily();
```

<a name="storing-batches-in-dynamodb"></a>
### DynamoDB에 배치 저장 (Storing Batches in DynamoDB)

Laravel은 관계형 DB 대신 [DynamoDB](https://aws.amazon.com/dynamodb)에 배치 정보를 저장할 수도 있습니다. 다만 DynamoDB 테이블을 수동으로 생성해야 하며 보통 `job_batches` 라고 명명합니다. 이명은 `queue.batching.table` 설정 값에 따라 달라질 수 있습니다.

<a name="dynamodb-batch-table-configuration"></a>
#### DynamoDB 배치 테이블 구성

테이블은 문자열 타입 `application` 파티션 키와 `id` 정렬 키가 있어야 합니다. `application`에는 환경설정 `app.name`이 할당되므로, 여러 Laravel 앱이 하나의 테이블을 사용할 수 있습니다.

또한 자동 배치 정리를 위해 `ttl` 속성을 정의할 수 있습니다.

<a name="dynamodb-configuration"></a>
#### DynamoDB 설정

AWS SDK를 설치하여 Laravel이 DynamoDB와 통신 가능하게 합니다:

```shell
composer require aws/aws-sdk-php
```

그다음 `queue.batching.driver`를 `dynamodb`로 설정하고, AWS 인증용 `key`, `secret`, `region` 옵션을 `batching` 설정 배열에 정의하세요. `dynamodb` 사용 시 `queue.batching.database` 옵션은 필요 없습니다:

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
#### DynamoDB 배치 정리

DynamoDB 저장 배치는 관계형 DB처럼 명령어로 정리되지 않으므로, DynamoDB 고유 기능인 [TTL](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html)을 활용합니다.

만약 테이블에 `ttl` 속성이 있다면, `queue.batching.ttl_attribute`와 `queue.batching.ttl` 설정으로 Laravel 정리 정책을 제어할 수 있습니다. `ttl`은 레코드 최종 업데이트 시점 이후 삭제될 때까지 경과해야 하는 초 단위 시간입니다:

```php
'batching' => [
    'driver' => env('QUEUE_FAILED_DRIVER', 'dynamodb'),
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'table' => 'job_batches',
    'ttl_attribute' => 'ttl',
    'ttl' => 60 * 60 * 24 * 7, // 7일...
],
```

<a name="queueing-closures"></a>
## 클로저 큐잉 (Queueing Closures)

잡 클래스 대신 클로저를 큐에 디스패치할 수도 있습니다. 간단한 비동기 작업에 좋으며, 클로저 코드가 전송 중 변조되지 않도록 암호화 서명됩니다:

```php
$podcast = App\Podcast::find(1);

dispatch(function () use ($podcast) {
    $podcast->publish();
});
```

`catch` 메서드로 클로저 실패 시 실행할 후속 클로저를 지정할 수도 있습니다:

```php
use Throwable;

dispatch(function () use ($podcast) {
    $podcast->publish();
})->catch(function (Throwable $e) {
    // 작업 실패 처리...
});
```

> [!WARNING]  
> `catch` 콜백은 직렬화되어 나중에 큐에서 실행되므로 `$this` 변수 사용은 금지됩니다.

<a name="running-the-queue-worker"></a>
## 큐 워커 실행 (Running the Queue Worker)

<a name="the-queue-work-command"></a>
### `queue:work` 명령어

Laravel은 큐 워커를 실행해 새 잡이 큐에 들어오면 즉시 처리하는 Artisan 명령어를 제공합니다. 워커는 종료하기 전까지 계속 실행됩니다:

```shell
php artisan queue:work
```

> [!NOTE]  
> 워커를 백그라운드에서 계속 실행하려면 [Supervisor](#supervisor-configuration) 같은 프로세스 모니터를 사용하는 게 안전합니다.

`-v` 옵션을 붙이면 처리된 잡 ID가 출력됩니다:

```shell
php artisan queue:work -v
```

워커는 장시간 실행 프로세스이며 애플리케이션 상태를 메모리에 유지합니다. 따라서 실행 중 코드 변경 사항을 인식하지 못하므로 배포 시 워커를 반드시 재시작하세요. 또한 애플리케이션 내 정적 상태도 잡 간에 자동 초기화되지 않습니다.

비효율적이지만 코드 변경 인식을 위해 워커를 재시작할 필요 없는 `queue:listen` 명령어를 사용할 수도 있습니다:

```shell
php artisan queue:listen
```

<a name="running-multiple-queue-workers"></a>
#### 여러 워커 실행

동시에 여러 워커를 실행하려면 단순히 `queue:work` 프로세스를 여러 개 실행하세요. 로컬에서는 터미널 여러 탭으로, 프로덕션은 프로세스 매니저 설정에서 처리할 수 있습니다. Supervisor를 쓴다면 `numprocs` 옵션을 이용합니다.

<a name="specifying-the-connection-queue"></a>
#### 커넥션 및 큐 지정

워커가 사용할 큐 커넥션 이름을 지정하려면, `work` 명령에 커넥션 이름을 전달합니다. 커넥션은 `config/queue.php` 내 정의와 일치해야 합니다:

```shell
php artisan queue:work redis
```

기본적으로 워커는 커넥션의 기본 큐만 처리하지만, 특정 큐만 처리하도록 지정할 수 있습니다. 예를 들어 `redis` 커넥션 내 `emails` 큐만 처리하려면:

```shell
php artisan queue:work redis --queue=emails
```

<a name="processing-a-specified-number-of-jobs"></a>
#### 지정한 잡 수만큼 처리

`--once` 옵션을 사용하면 워커가 큐에서 한 개 잡만 처리하고 종료합니다:

```shell
php artisan queue:work --once
```

`--max-jobs` 옵션은 지정 횟수만큼 잡을 처리 후 종료하도록 합니다. Supervisor와 함께 사용해 워커 메모리 누수를 방지할 때 유용합니다:

```shell
php artisan queue:work --max-jobs=1000
```

<a name="processing-all-queued-jobs-then-exiting"></a>
#### 큐가 빌 때까지 처리 후 종료

`--stop-when-empty` 옵션은 큐가 빌 때까지 잡을 처리하다가 종료합니다. Docker 컨테이너 내에서 큐 처리 후 컨테이너 종료에 유용합니다:

```shell
php artisan queue:work --stop-when-empty
```

<a name="processing-jobs-for-a-given-number-of-seconds"></a>
#### 지정 시간 동안 잡 처리

`--max-time` 옵션은 지정 초 동안만 잡을 처리하다 종료합니다. Supervisor와 함께 메모리 관리용으로 쓰기 좋습니다:

```shell
# 한 시간 처리 후 종료
php artisan queue:work --max-time=3600
```

<a name="worker-sleep-duration"></a>
#### 워커 슬립 시간

잡이 없으면 워커는 계속 폴링하지 않고 지정한 초만큼 '휴식'합니다. 휴식 시간 동안은 잡을 처리하지 않습니다:

```shell
php artisan queue:work --sleep=3
```

<a name="maintenance-mode-queues"></a>
#### 유지보수 모드와 큐 처리

[유지보수 모드](/docs/11.x/configuration#maintenance-mode)에서 큐 잡 처리는 중지됩니다. 유지보수를 종료해야 정상 처리됩니다.

강제 처리하려면 `--force` 옵션을 사용하세요:

```shell
php artisan queue:work --force
```

<a name="resource-considerations"></a>
#### 자원 고려 사항

데몬 워커는 잡마다 프레임워크 재시작이 없으므로, 작업 후 무거운 리소스(예: GD 이미지)를 반드시 해제해야 합니다.

<a name="queue-priorities"></a>
### 큐 우선순위 (Queue Priorities)

큐 우선순위를 지정하고 싶으면, 예를 들어 `config/queue.php`의 redis 기본 큐를 `low`로 설정하더라도, 우선순위 높은 `high` 큐에 잡을 넣고 실행할 수 있습니다:

```php
dispatch((new Job)->onQueue('high'));
```

워커 실행 시 `--queue` 옵션에 우선순위대로 콤마로 구분해 큐를 전달하면 높은 큐를 먼저 처리합니다:

```shell
php artisan queue:work --queue=high,low
```

<a name="queue-workers-and-deployment"></a>
### 큐 워커와 배포 (Queue Workers and Deployment)

큐 워커는 장기간 실행되므로 코드 변경을 인식하지 못합니다. 따라서 배포 시 워커를 재시작하세요. `queue:restart` 명령어로 워커에게 현재 작업 완료 후 종료하도록 신호를 보낼 수 있습니다:

```shell
php artisan queue:restart
```

워커 종료 후 Supervisor 같은 프로세스 매니저가 워커를 자동 재시작해야 합니다.

> [!NOTE]  
> `queue:restart`는 Laravel의 [캐시](/docs/11.x/cache) 시스템을 신호 저장소로 사용하므로, 캐시 설정이 올바른지 확인하세요.

<a name="job-expirations-and-timeouts"></a>
### 잡 만료 및 타임아웃 (Job Expirations and Timeouts)

<a name="job-expiration"></a>
#### 잡 만료

`config/queue.php` 내 각 커넥션은 `retry_after` 옵션을 가집니다. 이 값은 잡이 처리 중 실패한 것으로 간주되고 재시도될 때까지 기다리는 시간(초)입니다. 예) 90초면, 90초 이상 처리 중인 잡은 다시 큐에 돌아갑니다. 적절하게 최대 처리 시간을 설정하세요.

> [!WARNING]  
> Amazon SQS만 `retry_after` 옵션이 없으며, AWS 콘솔의 [Default Visibility Timeout](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/AboutVT.html) 설정을 따릅니다.

<a name="worker-timeouts"></a>
#### 워커 타임아웃

`queue:work` 명령어의 `--timeout` 옵션 기본값은 60초입니다. 이 시간을 넘으면 워커 프로세스가 종료되고 프로세스 매니저가 재시작합니다:

```shell
php artisan queue:work --timeout=60
```

`retry_after`와 CLI `--timeout`은 다르지만 협력해 잡이 중복 처리되지 않고 놓치지 않게 합니다.

> [!WARNING]  
> `--timeout` 값은 `retry_after` 값보다 항상 몇 초 짧아야 합니다. 그래야 처리 중 멈춘 잡에 대해 워커가 종료된 뒤 재시도가 발생합니다. 반대면 잡이 두 번 처리될 위험이 있습니다.

<a name="supervisor-configuration"></a>
## Supervisor 설정 (Supervisor Configuration)

프로덕션에서 `queue:work` 프로세스를 계속 실행하려면 프로세스 모니터가 필요합니다. 워커가 타임아웃되거나 `queue:restart` 명령 실행 시 종료될 수 있기 때문입니다.

Linux 환경에서 일반적으로 쓰이는 Supervisor를 설치해 워커 프로세스가 종료되면 자동 재시작하도록 합니다.

<a name="installing-supervisor"></a>
#### Supervisor 설치

Ubuntu에서 Supervisor 설치:

```shell
sudo apt-get install supervisor
```

> [!NOTE]  
> 직접 설치 및 관리가 어렵다면, [Laravel Forge](https://forge.laravel.com)를 이용하세요. 자동 설정을 지원합니다.

<a name="configuring-supervisor"></a>
#### Supervisor 설정

Supervisor 설정 파일은 보통 `/etc/supervisor/conf.d`에 둡니다. 예를 들어 `laravel-worker.conf`를 생성해 `queue:work` 워커 관리 설정:

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

`numprocs`는 워커 프로세스 수를 지정합니다. `command`는 원하는 큐 커넥션과 옵션으로 수정해야 합니다.

> [!WARNING]  
> `stopwaitsecs` 값은 가장 오래 걸리는 잡 처리 시간보다 커야 합니다. 그렇지 않으면 잡 처리 중 강제 종료될 수 있습니다.

<a name="starting-supervisor"></a>
#### Supervisor 시작

설정을 만들고 아래 명령으로 Supervisor에 반영 후 워커를 시작하세요:

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start "laravel-worker:*"
```

Supervisor에 관한 더 자세한 내용은 [Supervisor 공식 문서](http://supervisord.org/index.html)를 참고하세요.

<a name="dealing-with-failed-jobs"></a>
## 실패 잡 처리 (Dealing With Failed Jobs)

큐 잡이 실패할 수도 있습니다. Laravel은 [최대 시도 횟수](#max-job-attempts-and-timeout)를 지정하여, 그 횟수를 초과하는 비동기 잡을 `failed_jobs` 테이블에 저장합니다. 동기식 잡이 실패하면 즉시 예외가 처리되어 이 테이블에 저장되지 않습니다.

새 프로젝트라면 `failed_jobs` 테이블 생성 마이그레이션이 기본 포함되어 있으나 없으면 `make:queue-failed-table` 명령어로 생성하세요:

```shell
php artisan make:queue-failed-table

php artisan migrate
```

`queue:work` 명령어 실행 시 `--tries` 옵션으로 최대 시도 횟수를 지정할 수 있습니다. 옵션을 지정하지 않으면 잡 클래스 `$tries` 속성을 사용하거나 기본 1회만 재시도합니다:

```shell
php artisan queue:work redis --tries=3
```

`--backoff` 옵션은 실패 시 재시도까지 기다릴 초를 지정합니다. 기본값은 즉시 재시도입니다:

```shell
php artisan queue:work redis --tries=3 --backoff=3
```

잡 클래스 내 `backoff` 속성으로 작업별 재시도 지연 시간을 지정할 수도 있습니다:

```php
/**
 * 잡 재시도 전 대기 시간(초).
 *
 * @var int
 */
public $backoff = 3;
```

더 복잡한 로직이 필요하면 `backoff` 메서드를 정의해 초 또는 초 배열을 반환할 수 있습니다. 배열을 반환하면 재시도 횟수별 지연 시간이 달라집니다:

```php
/**
 * 잡 재시도 전 대기 시간을 계산.
 *
 * @return array<int, int>
 */
public function backoff(): array
{
    return [1, 5, 10];
}
```

<a name="cleaning-up-after-failed-jobs"></a>
### 실패 잡 정리 (Cleaning Up After Failed Jobs)

잡이 실패하면 사용자에게 알림을 보내거나 수행한 일의 일부를 롤백할 수 있습니다. `failed` 메서드를 잡 클래스에 구현하세요. 실패 원인 예외가 전달됩니다:

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
     * 새 잡 인스턴스 생성.
     */
    public function __construct(
        public Podcast $podcast,
    ) {}

    /**
     * 잡 실행.
     */
    public function handle(AudioProcessor $processor): void
    {
        // 팟캐스트 처리...
    }

    /**
     * 잡 실패 처리.
     */
    public function failed(?Throwable $exception): void
    {
        // 실패 알림 전송 등...
    }
}
```

> [!WARNING]  
> `failed` 호출 전 새로운 잡 인스턴스가 만들어지므로, `handle` 내에서 수정한 클래스 프로퍼티는 반영되지 않습니다.

<a name="retrying-failed-jobs"></a>
### 실패 잡 재시도 (Retrying Failed Jobs)

`failed_jobs` 테이블에 있는 실패 잡 목록을 확인하려면 `queue:failed` 명령어를 사용합니다:

```shell
php artisan queue:failed
```

실패 잡 ID를 이용해 재시도하려면 `queue:retry` 명령어를 사용합니다:

```shell
php artisan queue:retry ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece
```

여러 개 ID도 지정할 수 있습니다:

```shell
php artisan queue:retry ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece 91401d2c-0784-4f43-824c-34f94a33c24d
```

특정 큐 실패 잡만 재시도할 수도 있습니다:

```shell
php artisan queue:retry --queue=name
```

전체 실패 잡을 재시도하려면:

```shell
php artisan queue:retry all
```

실패 잡을 삭제하려면 `queue:forget` 명령어를 쓰세요:

```shell
php artisan queue:forget 91401d2c-0784-4f43-824c-34f94a33c24d
```

> [!NOTE]  
> Laravel Horizon을 사용 중이면 `queue:forget` 대신 `horizon:forget` 을 사용하세요.

전체 실패 잡을 삭제하려면 `queue:flush` 명령어를 사용합니다:

```shell
php artisan queue:flush
```

<a name="ignoring-missing-models"></a>
### 누락된 모델 무시 (Ignoring Missing Models)

Eloquent 모델을 잡에 주입하면 모델이 직렬화됐다가 처리가능할 때 다시 가져옵니다. 하지만 모델이 큐에 있는 동안 삭제됐으면 `ModelNotFoundException`이 발생할 수 있습니다.

이럴 때 잡에 `deleteWhenMissingModels` 속성을 `true`로 설정하면, 누락된 모델의 잡을 조용히 폐기해 예외 없이 처리할 수 있습니다:

```php
/**
 * 모델이 없으면 잡 삭제.
 *
 * @var bool
 */
public $deleteWhenMissingModels = true;
```

<a name="pruning-failed-jobs"></a>
### 실패 잡 정리 (Pruning Failed Jobs)

`queue:prune-failed` Artisan 명령어로 `failed_jobs` 테이블의 레코드를 정리할 수 있습니다:

```shell
php artisan queue:prune-failed
```

기본적으로 24시간 넘은 레코드를 삭제합니다. `--hours` 옵션으로 보존 기간을 조절해서 예를 들어 48시간 전 기록만 남기려면:

```shell
php artisan queue:prune-failed --hours=48
```

<a name="storing-failed-jobs-in-dynamodb"></a>
### DynamoDB에 실패 잡 저장 (Storing Failed Jobs in DynamoDB)

Laravel은 실패 잡을 관계형 DB 대신 [DynamoDB](https://aws.amazon.com/dynamodb)에 저장하는 것도 지원합니다. 하지만 테이블을 직접 생성해야 하며, 이름은 보통 `failed_jobs`으로 하거나 `queue.failed.table` 설정을 따릅니다.

테이블에 `application` 문자열 파티션 키와 `uuid` 문자열 정렬 키가 있어야 하며, `application` 필드에는 앱 이름(`app.name` 설정 값)이 들어갑니다. 이 방식으로 여러 앱이 같은 테이블을 공유할 수 있습니다.

AWS SDK를 설치하세요:

```shell
composer require aws/aws-sdk-php
```

`queue.failed.driver` 설정을 `dynamodb`로 바꾸고, 인증용 `key`, `secret`, `region` 설정을 추가합니다. `dynamodb` 사용 시 `queue.failed.database` 설정은 필요 없습니다:

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
### 실패 잡 저장 비활성화 (Disabling Failed Job Storage)

실패 잡을 저장하지 않고 폐기하려면 `queue.failed.driver` 값을 `null`로 설정하세요. 보통 `.env` 환경변수로 설정합니다:

```ini
QUEUE_FAILED_DRIVER=null
```

<a name="failed-job-events"></a>
### 실패 잡 이벤트 (Failed Job Events)

잡 실패 시 호출할 이벤트 리스너를 등록하려면 `Queue` 파사드의 `failing` 메서드를 사용합니다. 예를 들어 `AppServiceProvider`의 `boot` 메서드에서 다음과 같이 작성:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Queue;
use Illuminate\Support\ServiceProvider;
use Illuminate\Queue\Events\JobFailed;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 서비스 등록.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * 서비스 부트스트랩.
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
## 큐에서 잡 비우기 (Clearing Jobs From Queues)

> [!NOTE]  
> Laravel Horizon을 쓸 때는 `queue:clear` 대신 `horizon:clear` 명령어로 큐를 비우세요.

기본 커넥션과 큐에서 모든 잡을 삭제하려면 `queue:clear` 명령을 실행합니다:

```shell
php artisan queue:clear
```

특정 커넥션과 큐에서 삭제하려면 다음처럼 명령하세요:

```shell
php artisan queue:clear redis --queue=emails
```

> [!WARNING]  
> `queue:clear`는 SQS, Redis, 데이터베이스 드라이버에서만 지원됩니다. 그리고 SQS 메시지 삭제는 최대 60초 걸릴 수 있으므로, 명령 후 60초 이내에 등록된 메시지는 삭제되지 않을 수 있습니다.

<a name="monitoring-your-queues"></a>
## 큐 모니터링 (Monitoring Your Queues)

큐에 갑작스러운 작업 대량 유입이 생기면 처리 지연이 발생할 수 있습니다. 특정 임계값 이상의 작업이 대기 중이면 알림을 받도록 할 수 있습니다.

`queue:monitor` 명령을 1분마다 실행하도록 스케줄링해 모니터링하세요. 명령에 모니터링 큐 이름 목록과 임계값을 지정합니다:

```shell
php artisan queue:monitor redis:default,redis:deployments --max=100
```

임계값 초과 시 `Illuminate\Queue\Events\QueueBusy` 이벤트가 발생합니다. 이를 `AppServiceProvider` 등에서 청취하여 알림을 전송할 수 있습니다:

```php
use App\Notifications\QueueHasLongWaitTime;
use Illuminate\Queue\Events\QueueBusy;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\Facades\Notification;

/**
 * 서비스 부트스트랩.
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
## 테스트 (Testing)

잡 디스패치 코드를 테스트할 때, 잡 자체를 실행하지 않고 디스패치만 시뮬레이션하고 싶다면 `Queue` 파사드의 `fake` 메서드를 사용하세요. 이후 푸시 시도 여부를 검증할 수 있습니다.

Pest 예제:

```php tab=Pest
<?php

use App\Jobs\AnotherJob;
use App\Jobs\FinalJob;
use App\Jobs\ShipOrder;
use Illuminate\Support\Facades\Queue;

test('orders can be shipped', function () {
    Queue::fake();

    // 주문 배송 처리...

    // 잡이 전혀 큐에 푸시되지 않았는지 확인...
    Queue::assertNothingPushed();

    // 특정 큐에 지정 잡이 푸시되었는지 확인...
    Queue::assertPushedOn('queue-name', ShipOrder::class);

    // 잡이 두 번 푸시되었는지 확인...
    Queue::assertPushed(ShipOrder::class, 2);

    // 특정 잡이 푸시되지 않았는지 확인...
    Queue::assertNotPushed(AnotherJob::class);

    // 클로저가 큐에 푸시되었는지 확인...
    Queue::assertClosurePushed();

    // 푸시된 잡 총 수량 확인...
    Queue::assertCount(3);
});
```

PHPUnit 예제:

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

        // 주문 배송 처리...

        Queue::assertNothingPushed();

        Queue::assertPushedOn('queue-name', ShipOrder::class);

        Queue::assertPushed(ShipOrder::class, 2);

        Queue::assertNotPushed(AnotherJob::class);

        Queue::assertClosurePushed();

        Queue::assertCount(3);
    }
}
```

클로저를 `assertPushed` 또는 `assertNotPushed` 메서드에 전달해 구체적인 조건 검사도 할 수 있습니다:

```php
Queue::assertPushed(function (ShipOrder $job) use ($order) {
    return $job->order->id === $order->id;
});
```

<a name="faking-a-subset-of-jobs"></a>
### 잡 일부만 가짜로 처리하기

특정 잡만 가짜로 처리하고 나머지는 실제 실행하려면, `fake` 메서드에 가짜로 처리할 잡 클래스 배열을 전달하세요:

```php tab=Pest
test('orders can be shipped', function () {
    Queue::fake([
        ShipOrder::class,
    ]);

    // 주문 배송 처리...

    Queue::assertPushed(ShipOrder::class, 2);
});
```

```php tab=PHPUnit
public function test_orders_can_be_shipped(): void
{
    Queue::fake([
        ShipOrder::class,
    ]);

    // 주문 배송 처리...

    Queue::assertPushed(ShipOrder::class, 2);
}
```

가짜 처리하지 않을 잡을 `except` 메서드로 지정할 수도 있습니다:

```php
Queue::fake()->except([
    ShipOrder::class,
]);
```

<a name="testing-job-chains"></a>
### 잡 체인 테스트 (Testing Job Chains)

잡 체인은 `Bus` 파사드의 기능입니다. `Bus::fake()` 후 `assertChained` 메서드로 체인된 잡이 디스패치됐는지 확인할 수 있습니다. 배열에는 클래스를 지정하거나 인스턴스를 전달하세요:

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

```php
Bus::assertChained([
    new ShipOrder,
    new RecordShipment,
    new UpdateInventory,
]);
```

체인을 포함하지 않고 디스패치된 잡은 `assertDispatchedWithoutChain` 메서드로 테스트합니다:

```php
Bus::assertDispatchedWithoutChain(ShipOrder::class);
```

<a name="testing-chain-modifications"></a>
#### 체인 수정 테스트

잡이 위에서 소개한 [`prependToChain` 또는 `appendToChain`](#adding-jobs-to-the-chain)로 체인을 수정하면, 잡 인스턴스의 `assertHasChain` 메서드로 남은 체인이 예상대로인지 검사할 수 있습니다:

```php
$job = new ProcessPodcast;

$job->handle();

$job->assertHasChain([
    new TranscribePodcast,
    new OptimizePodcast,
    new ReleasePodcast,
]);
```

남은 체인이 없음을 확인하려면 `assertDoesntHaveChain`을 사용하세요:

```php
$job->assertDoesntHaveChain();
```

<a name="testing-chained-batches"></a>
#### 체인 내 배치 테스트

체인 중간에 배치가 포함되어 있다면, `Bus::chainedBatch`를 사용해 예상과 맞는지 확인할 수 있습니다:

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
### 잡 배치 테스트 (Testing Job Batches)

`Bus` 파사드의 `assertBatched` 메서드로 잡 배치가 디스패치됐는지 확인할 수 있습니다. 클로저엔 `PendingBatch`가 전달됩니다:

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

배치 개수는 `assertBatchCount`로, 배치가 없음을 `assertNothingBatched`로 확인 가능합니다:

```php
Bus::assertBatchCount(3);

Bus::assertNothingBatched();
```

<a name="testing-job-batch-interaction"></a>
#### 잡과 배치 상호작용 테스트

잡이 배치 진행 중 처리를 취소하거나 추가된 잡 여부를 테스트하려면, `withFakeBatch` 메서드로 가짜 배치를 잡에 할당합니다. 이 메서드는 잡과 배치 인스턴스의 배열을 반환합니다:

```php
[$job, $batch] = (new ShipOrder)->withFakeBatch();

$job->handle();

$this->assertTrue($batch->cancelled());
$this->assertEmpty($batch->added);
```

<a name="testing-job-queue-interactions"></a>
### 잡/큐 상호작용 테스트 (Testing Job / Queue Interactions)

잡이 스스로 큐에 재진입(`release`), 삭제(`delete`), 실패(`fail`)하는지 테스트하려면, 잡 인스턴스를 만들고 `withFakeQueueInteractions` 메서드를 호출하세요. 이후 `handle` 실행 후, 여러 assert 메서드로 검증합니다:

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
## 잡 이벤트 (Job Events)

`Queue` 파사드의 `before`와 `after` 메서드로 잡 처리 전후 실행할 콜백을 지정할 수 있습니다. 로깅하거나 통계를 기록하는 데 유용합니다. 보통 서비스 프로바이더 `boot` 메서드에서 정의합니다. 예:

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
     * 서비스 등록.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * 부트스트랩.
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

`Queue` 파사드의 `looping` 메서드로 워커가 큐 잡을 가져오기 전에 실행할 콜백을 지정할 수도 있습니다. 예를 들어, 이전 잡에서 열린 트랜잭션을 롤백할 때 사용합니다:

```php
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Queue;

Queue::looping(function () {
    while (DB::transactionLevel() > 0) {
        DB::rollBack();
    }
});
```