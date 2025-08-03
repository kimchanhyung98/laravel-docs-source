# 큐 (Queues)

- [소개](#introduction)
    - [연결과 큐의 차이 (Connections Vs. Queues)](#connections-vs-queues)
    - [드라이버 노트 및 사전 조건 (Driver Notes & Prerequisites)](#driver-prerequisites)
- [잡 생성하기 (Creating Jobs)](#creating-jobs)
    - [잡 클래스 생성 (Generating Job Classes)](#generating-job-classes)
    - [클래스 구조 (Class Structure)](#class-structure)
    - [고유 잡 (Unique Jobs)](#unique-jobs)
- [잡 미들웨어 (Job Middleware)](#job-middleware)
    - [레이트 리밋팅 (Rate Limiting)](#rate-limiting)
    - [잡 중복 방지 (Preventing Job Overlaps)](#preventing-job-overlaps)
    - [예외 스로틀링 (Throttling Exceptions)](#throttling-exceptions)
- [잡 디스패치 (Dispatching Jobs)](#dispatching-jobs)
    - [지연 디스패치 (Delayed Dispatching)](#delayed-dispatching)
    - [동기 디스패치 (Synchronous Dispatching)](#synchronous-dispatching)
    - [잡과 데이터베이스 트랜잭션 (Jobs & Database Transactions)](#jobs-and-database-transactions)
    - [잡 체인 (Job Chaining)](#job-chaining)
    - [큐 및 연결 커스터마이징 (Customizing The Queue & Connection)](#customizing-the-queue-and-connection)
    - [최대 시도 횟수 및 타임아웃 값 지정 (Max Job Attempts / Timeout Values)](#max-job-attempts-and-timeout)
    - [에러 처리 (Error Handling)](#error-handling)
- [잡 배칭 (Job Batching)](#job-batching)
    - [배치 가능한 잡 정의하기 (Defining Batchable Jobs)](#defining-batchable-jobs)
    - [배치 디스패치 (Dispatching Batches)](#dispatching-batches)
    - [배치에 잡 추가하기 (Adding Jobs To Batches)](#adding-jobs-to-batches)
    - [배치 검사 (Inspecting Batches)](#inspecting-batches)
    - [배치 취소 (Cancelling Batches)](#cancelling-batches)
    - [배치 실패 처리 (Batch Failures)](#batch-failures)
    - [배치 데이터 정리 (Pruning Batches)](#pruning-batches)
- [클로저 큐잉 (Queueing Closures)](#queueing-closures)
- [큐 워커 실행하기 (Running The Queue Worker)](#running-the-queue-worker)
    - [`queue:work` 명령어](#the-queue-work-command)
    - [큐 우선순위 (Queue Priorities)](#queue-priorities)
    - [큐 워커와 배포 (Queue Workers & Deployment)](#queue-workers-and-deployment)
    - [잡 만료 및 타임아웃 (Job Expirations & Timeouts)](#job-expirations-and-timeouts)
- [Supervisor 설정 (Supervisor Configuration)](#supervisor-configuration)
- [실패한 잡 처리하기 (Dealing With Failed Jobs)](#dealing-with-failed-jobs)
    - [실패한 잡 후처리 (Cleaning Up After Failed Jobs)](#cleaning-up-after-failed-jobs)
    - [실패한 잡 재시도 (Retrying Failed Jobs)](#retrying-failed-jobs)
    - [없는 모델 무시하기 (Ignoring Missing Models)](#ignoring-missing-models)
    - [실패한 잡 정리 (Pruning Failed Jobs)](#pruning-failed-jobs)
    - [DynamoDB에 실패한 잡 저장 (Storing Failed Jobs In DynamoDB)](#storing-failed-jobs-in-dynamodb)
    - [실패한 잡 저장 비활성화 (Disabling Failed Job Storage)](#disabling-failed-job-storage)
    - [실패한 잡 이벤트 (Failed Job Events)](#failed-job-events)
- [큐에서 잡 삭제하기 (Clearing Jobs From Queues)](#clearing-jobs-from-queues)
- [큐 모니터링 (Monitoring Your Queues)](#monitoring-your-queues)
- [잡 이벤트 (Job Events)](#job-events)

<a name="introduction"></a>
## 소개 (Introduction)

웹 애플리케이션을 개발하다 보면 업로드된 CSV 파일을 파싱하고 저장하는 등, 일반적인 웹 요청 동안 처리하기에는 너무 시간이 오래 걸리는 작업이 있을 수 있습니다. 다행히도, Laravel은 백그라운드에서 처리할 수 있는 큐잉 잡을 쉽게 생성할 수 있게 해줍니다. 시간 소모가 큰 작업을 큐로 옮기면, 애플리케이션에서 웹 요청에 빠르게 응답하여 사용자 경험을 향상시킬 수 있습니다.

Laravel 큐는 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 또는 관계형 데이터베이스 등 다양한 큐 백엔드에서 통일된 큐 API를 제공합니다.

Laravel의 큐 설정은 애플리케이션의 `config/queue.php` 파일에 저장됩니다. 이 파일에는 데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 드라이버뿐 아니라 로컬 개발 시 즉시 작업을 실행하는 동기 드라이버와, 큐에 쌓인 잡을 무시하는 `null` 드라이버까지 포함한 여러 연결 설정이 있습니다.

> [!TIP]
> Laravel은 Redis 큐를 위한 아름다운 대시보드와 설정 시스템인 Horizon을 제공합니다. 자세한 내용은 [Horizon 문서](/docs/{{version}}/horizon)를 참고하세요.

<a name="connections-vs-queues"></a>
### 연결과 큐의 차이 (Connections Vs. Queues)

Laravel 큐를 시작하기 전에 "연결(connections)"과 "큐(queues)"의 차이를 이해하는 것이 중요합니다. `config/queue.php` 설정 파일에는 `connections` 배열이 있는데, 이는 Amazon SQS, Beanstalk, Redis와 같은 백엔드 큐 서비스에 대한 연결을 정의합니다. 그러나 각 연결은 여러 개의 "큐"를 가질 수 있으며, 이는 여러 개의 잡 스택이나 더미로 생각할 수 있습니다.

`queue` 설정 파일 내 각 연결에는 기본 큐를 의미하는 `queue` 속성이 포함되어 있습니다. 즉, 잡을 디스패치할 때 특정 큐를 명시하지 않으면, 해당 연결 설정의 `queue` 속성에 정의된 기본 큐에 잡이 쌓입니다:

```
use App\Jobs\ProcessPodcast;

// 기본 연결의 기본 큐에 잡이 디스패치됩니다...
ProcessPodcast::dispatch();

// 기본 연결의 "emails" 큐에 잡이 디스패치됩니다...
ProcessPodcast::dispatch()->onQueue('emails');
```

일부 애플리케이션은 단일 큐만을 사용하기도 하지만, 여러 큐로 작업을 분배하면 우선순위나 처리 세그멘테이션을 구현할 수 있어 유용합니다. Laravel 큐 워커는 우선순위를 지정하여 특정 큐를 처리하도록 설정할 수 있습니다. 예를 들어, `high` 큐에 잡을 밀어넣고 해당 큐를 우선 처리하도록 워커를 실행할 수 있습니다:

```
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버 노트 및 사전 조건 (Driver Notes & Prerequisites)

<a name="database"></a>
#### 데이터베이스 (Database)

`database` 큐 드라이버를 사용하려면 작업을 저장할 데이터베이스 테이블이 필요합니다. 이 테이블을 생성하는 마이그레이션은 `queue:table` Artisan 명령어로 생성할 수 있습니다. 마이그레이션 생성 후에는 `migrate` 명령어로 데이터베이스 마이그레이션을 수행하세요:

```
php artisan queue:table

php artisan migrate
```

마지막으로, 애플리케이션의 `.env` 파일에서 `QUEUE_CONNECTION` 변수를 `database`로 설정하여 데이터베이스 드라이버를 사용하도록 합니다:

```
QUEUE_CONNECTION=database
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면 `config/database.php` 설정 파일에 Redis 데이터베이스 연결을 구성해야 합니다.

**Redis 클러스터**

Redis 클러스터를 사용하는 경우, 큐 이름에 [키 해시 태그](https://redis.io/topics/cluster-spec#keys-hash-tags)를 포함해야 합니다. 이는 동일한 큐의 모든 Redis 키가 같은 해시 슬롯에 위치하도록 하기 위한 필수 조건입니다:

```
'redis' => [
    'driver' => 'redis',
    'connection' => 'default',
    'queue' => '{default}',
    'retry_after' => 90,
],
```

**블로킹 (Blocking)**

Redis 큐 드라이버는 `block_for` 옵션으로 잡이 준비될 때까지 대기할 시간을 지정할 수 있습니다. 이는 워커 루프에서 Redis를 재조회하는 빈도를 조절하여 효율성을 높입니다. 예를 들어, 5초 동안 대기하도록 설정하려면:

```
'redis' => [
    'driver' => 'redis',
    'connection' => 'default',
    'queue' => 'default',
    'retry_after' => 90,
    'block_for' => 5,
],
```

> [!NOTE]
> `block_for`를 `0`으로 설정하면 작업 가능한 잡이 나올 때까지 무한정 대기하며, 이 경우 `SIGTERM` 같은 신호를 잡기 전까지 처리하지 않을 수 있습니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 사전 조건

아래 드라이버 사용 시 필요한 의존성은 Composer 패키지 매니저로 설치해야 합니다:

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~4.0`
- Redis: `predis/predis ~1.0` 또는 phpredis PHP 익스텐션

<a name="creating-jobs"></a>
## 잡 생성하기 (Creating Jobs)

<a name="generating-job-classes"></a>
### 잡 클래스 생성 (Generating Job Classes)

기본적으로 애플리케이션의 큐 잡은 `app/Jobs` 디렉터리에 저장됩니다. `app/Jobs` 디렉터리가 없으면 `make:job` Artisan 명령어 실행 시 자동으로 생성됩니다:

```
php artisan make:job ProcessPodcast
```

생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하여 Laravel에게 해당 잡이 비동기 실행을 위해 큐에 밀려야 한다는 것을 알립니다.

> [!TIP]
> 잡 스텁은 [스텁 퍼블리싱](/docs/{{version}}/artisan#stub-customization)을 통해 커스터마이징할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조 (Class Structure)

잡 클래스는 매우 간단하며 보통 큐로 처리될 때 호출되는 `handle` 메서드만 포함합니다. 예제로, 팟캐스트 퍼블리싱 서비스를 관리하며 업로드된 팟캐스트 파일을 처리해야 하는 잡 클래스를 살펴보겠습니다:

```
<?php

namespace App\Jobs;

use App\Models\Podcast;
use App\Services\AudioProcessor;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;

class ProcessPodcast implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    /**
     * The podcast instance.
     *
     * @var \App\Models\Podcast
     */
    protected $podcast;

    /**
     * Create a new job instance.
     *
     * @param  App\Models\Podcast  $podcast
     * @return void
     */
    public function __construct(Podcast $podcast)
    {
        $this->podcast = $podcast;
    }

    /**
     * Execute the job.
     *
     * @param  App\Services\AudioProcessor  $processor
     * @return void
     */
    public function handle(AudioProcessor $processor)
    {
        // Process uploaded podcast...
    }
}
```

이 예제에서 보듯, `SerializesModels` 트레이트 덕분에 Eloquent 모델과 로드된 연관관계가 잡 생성 시 직렬화되고 처리 시 역직렬화됩니다.

생성자에서 Eloquent 모델을 받으면, 큐로 직렬화할 때 모델 식별자만 큐에 저장되고 실제 처리 시 해당 모델과 연관관계가 데이터베이스에서 자동 조회됩니다. 이렇게 하면 큐 데이터가 훨씬 가벼워집니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드 의존성 주입

잡이 처리될 때 `handle` 메서드가 호출되며, 이 메서드에는 타입힌트된 의존성이 Laravel 서비스 컨테이너를 통해 자동 주입됩니다.

필요하면 서비스 프로바이더의 `boot` 메서드에서 컨테이너의 `bindMethod` 메서드를 이용해 `handle` 호출 방식을 직접 정의할 수 있습니다:

```
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function ($job, $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!NOTE]
> 바이너리 데이터(예: 원시 이미지 콘텐츠)는 잡에 전달하기 전에 `base64_encode` 함수로 인코딩해야 합니다. 그렇지 않으면 JSON 직렬화 시 문제가 발생할 수 있습니다.

<a name="handling-relationships"></a>
#### 큐에 직렬화되는 연관관계 처리

로드된 연관관계도 직렬화되어 잡 로그 크기가 커질 수 있습니다. 이를 방지하려면 모델을 할당할 때 `withoutRelations` 메서드를 호출해 연관관계를 제외한 모델 인스턴스를 설정할 수 있습니다:

```
public function __construct(Podcast $podcast)
{
    $this->podcast = $podcast->withoutRelations();
}
```

또한, 역직렬화 시에는 연관관계가 원본 제약 조건 없이 전체가 다시 조회됩니다. 특정 하위 집합 작업이 필요하다면, 큐 잡 내에서 연관관계 제약을 다시 설정해야 합니다.

<a name="unique-jobs"></a>
### 고유 잡 (Unique Jobs)

> [!NOTE]
> 고유 잡은 [락(locks)](/docs/{{version}}/cache#atomic-locks)을 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 드라이버가 원자적 락을 지원합니다. 또한, 배치 내 잡에는 고유 잡 제약이 적용되지 않습니다.

특정 잡 인스턴스가 큐에 중복으로 존재하지 않도록 하려면 `ShouldBeUnique` 인터페이스를 구현하세요:

```
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    ...
}
```

위 잡은 큐에 중복된 인스턴스가 없도록 보장합니다. 이미 처리 중인 동일 잡이 있으면 새 디스패치는 무시됩니다.

특정 고유 키 지정이나 제한 시간을 두려면 `uniqueId` 및 `uniqueFor` 속성 또는 메서드를 정의할 수 있습니다:

```
<?php

use App\Models\Product;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    /**
     * The product instance.
     *
     * @var \App\Product
     */
    public $product;

    /**
     * The number of seconds after which the job's unique lock will be released.
     *
     * @var int
     */
    public $uniqueFor = 3600;

    /**
     * The unique ID of the job.
     *
     * @return string
     */
    public function uniqueId()
    {
        return $this->product->id;
    }
}
```

위 예에서 `UpdateSearchIndex` 잡은 상품 ID별로 고유하며, 1시간(3600초)이 지나면 고유 락이 해제되어 동일 키로 다시 디스패치할 수 있습니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 처리 시작 전까지 잡을 고유하게 유지하기

기본적으로 고유 잡은 완료 혹은 최대 재시도 실패 후에 해제됩니다. 반대로, 처리 시작 바로 전에 해제하고 싶으면 `ShouldBeUniqueUntilProcessing` 인터페이스를 구현하세요:

```
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
#### 고유 잡 락

`ShouldBeUnique` 잡이 디스패치되면 Laravel은 `uniqueId` 키로 [락](#atomic-lock)을 시도합니다. 락을 획득 못 하면 잡이 디스패치되지 않고, 락은 작업 완료 또는 최대 재시도 실패 시 해제됩니다.

기본적으로 Laravel은 기본 캐시 드라이버로 락을 만들지만, `uniqueVia` 메서드를 구현하여 다른 캐시 드라이버를 사용할 수도 있습니다:

```
use Illuminate\Support\Facades\Cache;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...

    /**
     * Get the cache driver for the unique job lock.
     *
     * @return \Illuminate\Contracts\Cache\Repository
     */
    public function uniqueVia()
    {
        return Cache::driver('redis');
    }
}
```

> [!TIP]
> 단순 동시 처리 제한이 필요하면 [`WithoutOverlapping`](/docs/{{version}}/queues#preventing-job-overlaps) 잡 미들웨어를 사용하는 것이 더 적절합니다.

<a name="job-middleware"></a>
## 잡 미들웨어 (Job Middleware)

잡 미들웨어는 큐 처리 시 커스텀 로직을 감싸는 기능으로, 잡 자체 코드 내 보일러플레이트를 줄여줍니다. 예를 들어, Laravel의 Redis 레이트 리밋 기능을 활용해 5초에 한 번씩만 처리하도록 하는 `handle` 메서드를 보면:

```
use Illuminate\Support\Facades\Redis;

/**
 * Execute the job.
 *
 * @return void
 */
public function handle()
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

이 경우 `handle`이 Redis 레이트 리밋 로직으로 복잡해지고, 여러 잡에서 같은 코드를 반복해야 하는 문제가 있습니다.

대신, 이런 로직을 잡 미들웨어로 분리할 수 있습니다. Laravel에는 지정된 위치가 없으므로 `app/Jobs/Middleware` 같은 경로에 자유롭게 정의해도 됩니다:

```
<?php

namespace App\Jobs\Middleware;

use Illuminate\Support\Facades\Redis;

class RateLimited
{
    /**
     * Process the queued job.
     *
     * @param  mixed  $job
     * @param  callable  $next
     * @return mixed
     */
    public function handle($job, $next)
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

잡 미들웨어는 [라우트 미들웨어](/docs/{{version}}/middleware)처럼 콜백을 받아 잡과 처리 단계 콜백을 인자로 받습니다.

생성된 미들웨어는 잡 클래스 내 `middleware` 메서드에서 반환해 할당할 수 있습니다. 이 메서드는 기본 `make:job`가 만드는 잡에 자동 생성되지 않으므로 직접 추가해야 합니다:

```
use App\Jobs\Middleware\RateLimited;

/**
 * Get the middleware the job should pass through.
 *
 * @return array
 */
public function middleware()
{
    return [new RateLimited];
}
```

> [!TIP]
> 잡 미들웨어는 큐 이벤트 리스너, 메일러, 알림에도 할당할 수 있습니다.

<a name="rate-limiting"></a>
### 레이트 리밋팅 (Rate Limiting)

직접 작성 방식을 알아봤지만, Laravel은 잡 레이트 리밋을 위한 미들웨어도 제공합니다. [라우트 레이트 리밋터](/docs/{{version}}/routing#defining-rate-limiters)와 마찬가지로 `RateLimiter` 파사드의 `for` 메서드로 정의합니다.

예를 들어, 일반 사용자는 한 시간에 한 번 데이터 백업만 허용하고, 프리미엄 사용자는 무제한으로 허용하려면 `AppServiceProvider`의 `boot` 메서드에 다음과 같이 정의할 수 있습니다:

```
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Support\Facades\RateLimiter;

/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
{
    RateLimiter::for('backups', function ($job) {
        return $job->user->vipCustomer()
                    ? Limit::none()
                    : Limit::perHour(1)->by($job->user->id);
    });
}
```

위 예시는 시간 단위 제한을, `perMinute` 메서드를 통해 분 단위 제한도 정의할 수 있습니다. `by`에 전달하는 값은 보통 고객별 세그멘테이션에 쓰입니다:

```
return Limit::perMinute(50)->by($job->user->id);
```

정의한 레이트 리밋을 잡에 적용하려면 `Illuminate\Queue\Middleware\RateLimited` 미들웨어를 붙입니다. 제한 초과 시 미들웨어가 잡을 지연해 다시 큐에 넣습니다:

```
use Illuminate\Queue\Middleware\RateLimited;

/**
 * Get the middleware the job should pass through.
 *
 * @return array
 */
public function middleware()
{
    return [new RateLimited('backups')];
}
```

재시도 시도 횟수(`attempts`)는 계속 증가하니 `tries`, `maxExceptions`를 적절히 조절하거나 [`retryUntil` 메서드](#time-based-attempts)를 활용해 실행 제한 시간을 지정할 수 있습니다.

재시도 없이 레이트 리밋 시 잡을 그냥 버리고 싶으면 `dontRelease` 메서드를 사용하세요:

```
/**
 * Get the middleware the job should pass through.
 *
 * @return array
 */
public function middleware()
{
    return [(new RateLimited('backups'))->dontRelease()];
}
```

> [!TIP]
> Redis를 사용하는 경우 `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어가 더욱 최적화되어 있습니다.

<a name="preventing-job-overlaps"></a>
### 잡 중복 방지 (Preventing Job Overlaps)

Laravel의 `Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어를 사용하면 임의의 키를 이용해 잡 중복 실행을 방지할 수 있습니다. 예를 들어 사용자의 신용점수를 업데이트하는 잡이 user ID별로 중복 실행되지 않도록 할 때 유용합니다.

`middleware` 메서드에서 다음과 같이 할당하세요:

```
use Illuminate\Queue\Middleware\WithoutOverlapping;

/**
 * Get the middleware the job should pass through.
 *
 * @return array
 */
public function middleware()
{
    return [new WithoutOverlapping($this->user->id)];
}
```

중복 잡은 큐에 다시 반환되며, 재시도까지 대기할 시간(초)을 `releaseAfter`로 지정할 수 있습니다:

```
/**
 * Get the middleware the job should pass through.
 *
 * @return array
 */
public function middleware()
{
    return [(new WithoutOverlapping($this->order->id))->releaseAfter(60)];
}
```

중복 잡을 바로 삭제하고 재시도되지 않도록 하려면 `dontRelease`를 호출하세요:

```
/**
 * Get the middleware the job should pass through.
 *
 * @return array
 */
public function middleware()
{
    return [(new WithoutOverlapping($this->order->id))->dontRelease()];
}
```

`WithoutOverlapping` 미들웨어는 Laravel 원자 락 기능을 사용합니다. 잡이 비정상 종료되거나 타임아웃 발생 시 락이 해제되지 않을 수 있으므로, `expireAfter` 메서드로 락 만료 시간을 명시적으로 지정할 수 있습니다. 아래는 3분(180초) 후 락 만료 예시입니다:

```
/**
 * Get the middleware the job should pass through.
 *
 * @return array
 */
public function middleware()
{
    return [(new WithoutOverlapping($this->order->id))->expireAfter(180)];
}
```

> [!NOTE]
> `WithoutOverlapping` 미들웨어는 [락 지원 캐시 드라이버](/docs/{{version}}/cache#atomic-locks)가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 드라이버가 이를 지원합니다.

<a name="throttling-exceptions"></a>
### 예외 스로틀링 (Throttling Exceptions)

`Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어는 잡이 일정 개수 이상 예외를 발생시키면 이후 실행을 지연시켜 악성 상황을 완화합니다. 불안정한 타사 API 연동에 유용합니다.

예를 들어 10번 예외가 발생하면 5분간 스로틀링하는 방법입니다:

```
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * Get the middleware the job should pass through.
 *
 * @return array
 */
public function middleware()
{
    return [new ThrottlesExceptions(10, 5)];
}

/**
 * Determine the time at which the job should timeout.
 *
 * @return \DateTime
 */
public function retryUntil()
{
    return now()->addMinutes(5);
}
```

첫 번째 인자는 최대 예외 횟수, 두 번째는 예외 한도 도달 후 재시도까지 대기 시간(분)입니다.

예외 한도를 넘지 않을 경우 바로 재시도하지만, 대기시간을 지정하려면 미들웨어에 `backoff` 메서드를 활용할 수 있습니다:

```
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * Get the middleware the job should pass through.
 *
 * @return array
 */
public function middleware()
{
    return [(new ThrottlesExceptions(10, 5))->backoff(5)];
}
```

내부적으로 라라벨 캐시와 잡 클래스명이 키로 쓰여 구현되며, 키를 오버라이드하려면 `by` 메서드를 호출합니다:

```
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * Get the middleware the job should pass through.
 *
 * @return array
 */
public function middleware()
{
    return [(new ThrottlesExceptions(10, 10))->by('key')];
}
```

> [!TIP]
> Redis 사용 시 `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어를 이용하면 기본 미들웨어보다 효율적입니다.

<a name="dispatching-jobs"></a>
## 잡 디스패치 (Dispatching Jobs)

잡 클래스를 작성한 후 `dispatch` 메서드로 디스패치할 수 있습니다. 전달하는 인수는 생성자의 인수로 전달됩니다:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    /**
     * Store a new podcast.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        $podcast = Podcast::create(...);

        // ...

        ProcessPodcast::dispatch($podcast);
    }
}
```

조건부 디스패치가 필요하면 `dispatchIf`와 `dispatchUnless` 메서드를 사용할 수 있습니다:

```
ProcessPodcast::dispatchIf($accountActive, $podcast);

ProcessPodcast::dispatchUnless($accountSuspended, $podcast);
```

<a name="delayed-dispatching"></a>
### 지연 디스패치 (Delayed Dispatching)

잡이 바로 처리되지 않고 일정 시간 후 실행되도록 하려면 `delay` 메서드를 체이닝하세요. 예를 들어 10분 후 실행되게 지정하려면:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    /**
     * Store a new podcast.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        $podcast = Podcast::create(...);

        // ...

        ProcessPodcast::dispatch($podcast)
                    ->delay(now()->addMinutes(10));
    }
}
```

> [!NOTE]
> Amazon SQS 큐 서비스는 최대 지연 시간이 15분입니다.

<a name="dispatching-after-the-response-is-sent-to-browser"></a>
#### 응답 전 디스패치 지연 (Dispatching After The Response Is Sent To Browser)

`dispatchAfterResponse` 메서드는 HTTP 응답을 사용자에게 보낸 뒤에 잡 디스패치를 지연시킵니다. 짧은 시간 잡, 예컨대 메일 발송에 적합합니다. 이 경우 워커 없이도 현재 요청 내에서 실행됩니다:

```
use App\Jobs\SendNotification;

SendNotification::dispatchAfterResponse();
```

클로저도 `dispatch` 헬퍼 + `afterResponse` 메서드로 응답 이후 실행할 수 있습니다:

```
use App\Mail\WelcomeMessage;
use Illuminate\Support\Facades\Mail;

dispatch(function () {
    Mail::to('taylor@example.com')->send(new WelcomeMessage);
})->afterResponse();
```

<a name="synchronous-dispatching"></a>
### 동기 디스패치 (Synchronous Dispatching)

즉시 실행하고 싶으면 `dispatchSync` 메서드를 사용하세요. 이 경우 큐에 쌓이지 않고 현재 프로세스 내에서 실행됩니다:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    /**
     * Store a new podcast.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        $podcast = Podcast::create(...);

        // Create podcast...

        ProcessPodcast::dispatchSync($podcast);
    }
}
```

<a name="jobs-and-database-transactions"></a>
### 잡과 데이터베이스 트랜잭션 (Jobs & Database Transactions)

트랜잭션 내에서 잡을 디스패치할 때는, 잡 처리 시점에 트랜잭션이 완료되지 않아 모델 변경 내용이 DB에 반영되지 않았을 수 있다는 점에 유의하세요.

이를 방지하려면 큐 연결 설정에서 `after_commit` 옵션을 `true`로 설정하세요:

```
'redis' => [
    'driver' => 'redis',
    // ...
    'after_commit' => true,
],
```

이 옵션이 `true`면, 열려있는 모든 트랜잭션이 커밋된 후에 잡이 실제 디스패치됩니다. 트랜잭션이 롤백되면 해당 트랜잭션 동안 디스패치된 잡들은 버려집니다.

> [!TIP]
> `after_commit` 옵션 적용 시, 큐 이벤트 리스너, 메일러, 알림, 브로드캐스트 이벤트도 모두 트랜잭션 커밋 후 디스패치됩니다.

<a name="specifying-commit-dispatch-behavior-inline"></a>
#### 커밋 디스패치 동작 인라인 지정

`after_commit` 옵션이 `true`가 아니더라도, 특정 잡에 대해 커밋 후 디스패치할 수 있습니다. `dispatch` 체이닝에 `afterCommit`을 호출하세요:

```
use App\Jobs\ProcessPodcast;

ProcessPodcast::dispatch($podcast)->afterCommit();
```

반대로 `after_commit`이 `true`일 때, 특정 잡만 즉시 디스패치하려면 `beforeCommit` 메서드를 호출합니다:

```
ProcessPodcast::dispatch($podcast)->beforeCommit();
```

<a name="job-chaining"></a>
### 잡 체인 (Job Chaining)

잡 체인은 특정 잡 성공 후 연속적으로 실행할 잡 배열을 지정하는 기능입니다. 하나라도 실패하면 나머지 잡은 실행되지 않습니다.

`Bus` 파사드의 `chain` 메서드를 사용합니다:

```
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

클로저도 함께 체인할 수 있습니다:

```
Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    function () {
        Podcast::update(...);
    },
])->dispatch();
```

> [!NOTE]
> 잡 체인 내에서 `$this->delete()`를 호출해도 체인은 멈추지 않습니다. 체인은 잡 실패 시에만 중단됩니다.

<a name="chain-connection-queue"></a>
#### 체인 연결 및 큐 설정

연결과 큐를 지정하려면 `onConnection`, `onQueue`를 메서드 체인으로 호출하세요. 각 잡에 명시된 설정이 우선권을 가지며 나머지는 여기서 지정한 값이 적용됩니다:

```
Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->onConnection('redis')->onQueue('podcasts')->dispatch();
```

<a name="chain-failures"></a>
#### 체인 실패 처리

체인 내 잡 실패 시 실행될 콜백을 지정하려면 `catch` 메서드를 사용하세요. 실패의 원인인 `Throwable` 인스턴스를 인자로 받습니다:

```
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

<a name="customizing-the-queue-and-connection"></a>
### 큐와 연결 커스터마이징 (Customizing The Queue & Connection)

<a name="dispatching-to-a-particular-queue"></a>
#### 특정 큐로 디스패치

잡을 서로 다른 큐에 할당하면 잡을 분류하거나 우선순위를 조절할 수 있습니다. 연결(connection) 단위가 아니라 *해당 연결 내의 큐 이름*을 지정하는 것입니다.

잡 디스패치 시 `onQueue`를 호출합니다:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    /**
     * Store a new podcast.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        $podcast = Podcast::create(...);

        // Create podcast...

        ProcessPodcast::dispatch($podcast)->onQueue('processing');
    }
}
```

또는 잡 생성자 내부에서 `onQueue` 메서드를 호출할 수도 있습니다:

```
<?php

namespace App\Jobs;

 use Illuminate\Bus\Queueable;
 use Illuminate\Contracts\Queue\ShouldQueue;
 use Illuminate\Foundation\Bus\Dispatchable;
 use Illuminate\Queue\InteractsWithQueue;
 use Illuminate\Queue\SerializesModels;

class ProcessPodcast implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    /**
     * Create a new job instance.
     *
     * @return void
     */
    public function __construct()
    {
        $this->onQueue('processing');
    }
}
```

<a name="dispatching-to-a-particular-connection"></a>
#### 특정 연결로 디스패치

애플리케이션이 여러 큐 연결을 사용하는 경우 `onConnection` 메서드를 호출해 어떤 연결에 밀지 지정할 수 있습니다:

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    /**
     * Store a new podcast.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        $podcast = Podcast::create(...);

        // Create podcast...

        ProcessPodcast::dispatch($podcast)->onConnection('sqs');
    }
}
```

`onConnection`과 `onQueue`는 메서드 체인도 지원합니다:

```
ProcessPodcast::dispatch($podcast)
              ->onConnection('sqs')
              ->onQueue('processing');
```

잡 생성자 안에서도 `onConnection` 메서드를 호출할 수 있습니다:

```
<?php

namespace App\Jobs;

 use Illuminate\Bus\Queueable;
 use Illuminate\Contracts\Queue\ShouldQueue;
 use Illuminate\Foundation\Bus\Dispatchable;
 use Illuminate\Queue\InteractsWithQueue;
 use Illuminate\Queue\SerializesModels;

class ProcessPodcast implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    /**
     * Create a new job instance.
     *
     * @return void
     */
    public function __construct()
    {
        $this->onConnection('sqs');
    }
}
```

<a name="max-job-attempts-and-timeout"></a>
### 최대 시도 횟수 및 타임아웃 지정 (Specifying Max Job Attempts / Timeout Values)

<a name="max-attempts"></a>
#### 최대 시도 횟수

잡 에러 시 무한 재시도를 방지하려면 최대 시도 횟수를 지정하세요.

Artisan 커맨드의 `--tries` 옵션으로 모든 워커에 기본 적용하거나, 잡 클래스에 `tries` 속성으로 개별 지정할 수 있습니다. 클래스 속성 우선입니다.

CLI 전체 기본값 지정:

```
php artisan queue:work --tries=3
```

잡 클래스 내 개별 지정:

```
<?php

namespace App\Jobs;

class ProcessPodcast implements ShouldQueue
{
    /**
     * The number of times the job may be attempted.
     *
     * @var int
     */
    public $tries = 5;
}
```

최대 시도 넘으면 "실패한" 잡으로 간주되며, [실패한 잡 처리](#dealing-with-failed-jobs)를 참고하세요.

<a name="time-based-attempts"></a>
#### 시간 기준 시도 제한

최대 시도 횟수 대신, 특정 시간 이후에는 더 이상 시도하지 않도록 조건을 둘 수 있습니다. 잡 클래스에 `retryUntil` 메서드를 정의하고 `DateTime` 인스턴스를 반환하면 됩니다:

```
/**
 * Determine the time at which the job should timeout.
 *
 * @return \DateTime
 */
public function retryUntil()
{
    return now()->addMinutes(10);
}
```

> [!TIP]
> 큐 이벤트 리스너에서도 `tries`나 `retryUntil`을 정의할 수 있습니다.

<a name="max-exceptions"></a>
#### 최대 예외 허용 횟수

잡이 여러 번 시도 가능하지만, 처리 중 발생한 특정 수 이상의 미처리 예외가 발생하면 실패 처리하고 싶을 때가 있습니다. 이때 잡 클래스에 `maxExceptions` 속성을 정의하세요:

```
<?php

namespace App\Jobs;

use Illuminate\Support\Facades\Redis;

class ProcessPodcast implements ShouldQueue
{
    /**
     * The number of times the job may be attempted.
     *
     * @var int
     */
    public $tries = 25;

    /**
     * The maximum number of unhandled exceptions to allow before failing.
     *
     * @var int
     */
    public $maxExceptions = 3;

    /**
     * Execute the job.
     *
     * @return void
     */
    public function handle()
    {
        Redis::throttle('key')->allow(10)->every(60)->then(function () {
            // Lock obtained, process the podcast...
        }, function () {
            // Unable to obtain lock...
            return $this->release(10);
        });
    }
}
```

위 예시에서, 잡은 최대 25회 재시도되지만, 미처리 예외가 3회 발생하면 실패합니다. 락 획득 실패 시 10초간 락 얻기를 재시도하지 않도록 합니다.

<a name="timeout"></a>
#### 타임아웃

> [!NOTE]
> 잡 타임아웃 지정에는 `pcntl` PHP 익스텐션이 설치되어 있어야 합니다.

예상 처리 시간 기준으로 잡 타임아웃을 지정할 수 있습니다. 지정한 시간(초) 이상 실행 중이면 워커는 에러 코드와 함께 종료되고, 보통 [서버 프로세스 매니저](#supervisor-configuration)가 재시작합니다.

CLI에서 `queue:work` 명령어에 `--timeout` 옵션을 붙여 지정하세요:

```
php artisan queue:work --timeout=30
```

잡 클래스 내 `timeout` 속성으로 개별 지정 시 CLI 설정보다 우선 적용됩니다:

```
<?php

namespace App\Jobs;

class ProcessPodcast implements ShouldQueue
{
    /**
     * The number of seconds the job can run before timing out.
     *
     * @var int
     */
    public $timeout = 120;
}
```

주의 사항: I/O 블로킹 작업은 프로세스 타임아웃을 직접 따르지 않을 수 있으니, Guzzle 같은 라이브러리의 별도 타임아웃 API 설정도 권장합니다.

<a name="failing-on-timeout"></a>
#### 타임아웃 시 실패 처리

타임아웃 발생 시 자동으로 실패 처리하고 싶으면 잡 클래스에 `$failOnTimeout` 속성을 `true`로 설정하세요:

```php
/**
 * Indicate if the job should be marked as failed on timeout.
 *
 * @var bool
 */
public $failOnTimeout = true;
```

<a name="error-handling"></a>
### 에러 처리 (Error Handling)

잡 처리 중 예외가 발생하면 잡은 자동으로 큐에 다시 풀려 재시도됩니다. 재시도 횟수가 최대 시도를 넘으면 "실패한 잡"으로 분류됩니다.

최대 시도 횟수는 `queue:work` 명령어의 `--tries` 스위치 또는 잡 클래스 내 `tries` 속성으로 설정할 수 있습니다.

<a name="manually-releasing-a-job"></a>
#### 수동으로 잡 다시 풀기

잡 처리 중 특정 조건에서 지연 후 다시 시도하고 싶으면 `release` 메서드를 호출합니다:

```
/**
 * Execute the job.
 *
 * @return void
 */
public function handle()
{
    // ...

    $this->release();
}
```

기본적으로 즉시 다시 풀지만, 초 단위 지연도 지정할 수 있습니다:

```
$this->release(10);
```

<a name="manually-failing-a-job"></a>
#### 수동으로 잡 실패 처리하기

잡을 수동으로 실패 처리하려면 `fail` 메서드를 호출합니다:

```
/**
 * Execute the job.
 *
 * @return void
 */
public function handle()
{
    // ...

    $this->fail();
}
```

포착한 예외 정보를 함께 넘길 수도 있습니다:

```
$this->fail($exception);
```

> [!TIP]
> 실패한 잡 처리 관련 자세한 내용은 [실패한 잡 문서](#dealing-with-failed-jobs)를 참고하세요.

<a name="job-batching"></a>
## 잡 배칭 (Job Batching)

Laravel의 잡 배칭 기능은 여러 잡을 묶어 실행하고, 모두 완료되었을 때 콜백을 수행하도록 돕습니다. 시작 전 배치 정보를 저장할 테이블을 생성할 마이그레이션을 `queue:batches-table` Artisan 명령으로 생성하고 마이그레이션하세요:

```
php artisan queue:batches-table

php artisan migrate
```

<a name="defining-batchable-jobs"></a>
### 배치 가능한 잡 정의하기 (Defining Batchable Jobs)

배치 잡은 일반 큐 잡과 같으며, `Illuminate\Bus\Batchable` 트레이트를 추가로 사용합니다. 이 트레이트가 현재 배치를 반환하는 `batch` 메서드를 제공합니다:

```
<?php

namespace App\Jobs;

use Illuminate\Bus\Batchable;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;

class ImportCsv implements ShouldQueue
{
    use Batchable, Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    /**
     * Execute the job.
     *
     * @return void
     */
    public function handle()
    {
        if ($this->batch()->cancelled()) {
            // 배치가 취소되었는지 확인...

            return;
        }

        // CSV 일부를 임포트...
    }
}
```

<a name="dispatching-batches"></a>
### 배치 디스패치 (Dispatching Batches)

`Bus::batch` 메서드로 잡 배열을 전달해 배치를 만들고, 성공, 실패, 완료 시 콜백을 등록할 수 있습니다. 콜백은 `Illuminate\Bus\Batch` 인스턴스를 받습니다.

```
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
])->then(function (Batch $batch) {
    // 모든 잡이 성공적 처리됨...
})->catch(function (Batch $batch, Throwable $e) {
    // 첫 번째 배치 잡 실패 감지...
})->finally(function (Batch $batch) {
    // 배치 실행 완료...
})->dispatch();

return $batch->id;
```

배치 ID (`$batch->id`)로 나중에 [배치 상태 조회](#inspecting-batches)가 가능합니다.

> [!NOTE]
> 배치 콜백 내에서 `$this` 변수 사용은 권장하지 않습니다.

<a name="naming-batches"></a>
#### 배치 이름 지정

배치에 사용자가 알아보기 쉬운 이름을 지정하려면 `name` 메서드를 호출합니다:

```
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // ...
})->name('Import CSV')->dispatch();
```

Laravel Horizon, Telescope 같은 도구에서 디버깅 편의가 향상됩니다.

<a name="batch-connection-queue"></a>
#### 배치 연결과 큐 지정

배치 내 모든 잡이 같은 연결과 큐에서 실행되어야 하므로, `onConnection`, `onQueue`를 호출해 지정할 수 있습니다:

```
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // ...
})->onConnection('redis')->onQueue('imports')->dispatch();
```

<a name="chains-within-batches"></a>
#### 배치 내 체인 잡

배치 내에서 잡 체인을 배열로 묶어 지정할 수 있습니다. 예를 들어 2개의 체인 잡을 병렬 처리하고 모두 완료 시 콜백을 실행하는 예:

```
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

<a name="adding-jobs-to-batches"></a>
### 배치에 잡 추가하기 (Adding Jobs To Batches)

배치 잡 내부에서 추가 잡을 배치에 삽입할 수 있습니다. 이는 수천 개 잡을 한꺼번에 웹 요청 시점에 디스패치하기 힘든 경우, 초기 '로더' 잡으로 배치를 확장할 때 유용합니다:

```
$batch = Bus::batch([
    new LoadImportBatch,
    new LoadImportBatch,
    new LoadImportBatch,
])->then(function (Batch $batch) {
    // ...
})->name('Import Contacts')->dispatch();
```

`batch` 메서드를 통해 접근한 배치 객체의 `add` 메서드에 잡 컬렉션을 추가하세요:

```
use App\Jobs\ImportContacts;
use Illuminate\Support\Collection;

/**
 * Execute the job.
 *
 * @return void
 */
public function handle()
{
    if ($this->batch()->cancelled()) {
        return;
    }

    $this->batch()->add(Collection::times(1000, function () {
        return new ImportContacts;
    }));
}
```

> [!NOTE]
> 배치에 잡을 추가할 수 있는 것은 같은 배치 내 잡에서만 가능합니다.

<a name="inspecting-batches"></a>
### 배치 검사 (Inspecting Batches)

배치 콜백에 전달되는 `Illuminate\Bus\Batch` 인스턴스는 다음과 같은 속성과 메서드를 제공합니다:

```
// 배치 UUID
$batch->id;

// 배치 이름 (있으면)
$batch->name;

// 배치에 할당된 총 잡 수
$batch->totalJobs;

// 아직 처리되지 않은 잡 수
$batch->pendingJobs;

// 실패한 잡 수
$batch->failedJobs;

// 지금까지 처리한 잡 수
$batch->processedJobs();

// 배치 완료율 (0-100)
$batch->progress();

// 배치가 완료되었는지 여부
$batch->finished();

// 배치 실행 취소
$batch->cancel();

// 배치가 취소되었는지 여부
$batch->cancelled();
```

<a name="returning-batches-from-routes"></a>
#### 라우트에서 배치 반환하기

`Illuminate\Bus\Batch`는 JSON 직렬화 가능하므로, 웹 라우트에서 바로 반환해 프론트에서 진행률 표시 등에 활용할 수 있습니다.

배치 ID로 배치를 조회하려면 `Bus::findBatch` 메서드를 호출하세요:

```
use Illuminate\Support\Facades\Bus;
use Illuminate\Support\Facades\Route;

Route::get('/batch/{batchId}', function (string $batchId) {
    return Bus::findBatch($batchId);
});
```

<a name="cancelling-batches"></a>
### 배치 취소 (Cancelling Batches)

배치 실행을 취소하려면 `Illuminate\Bus\Batch` 인스턴스의 `cancel` 메서드를 호출하세요:

```
/**
 * Execute the job.
 *
 * @return void
 */
public function handle()
{
    if ($this->user->exceedsImportLimit()) {
        return $this->batch()->cancel();
    }

    if ($this->batch()->cancelled()) {
        return;
    }
}
```

대부분의 배치 잡은 `handle` 시작부에서 배치 취소 여부를 체크해야 합니다:

```
/**
 * Execute the job.
 *
 * @return void
 */
public function handle()
{
    if ($this->batch()->cancelled()) {
        return;
    }

    // 계속 처리...
}
```

<a name="batch-failures"></a>
### 배치 실패 처리 (Batch Failures)

배치 잡 실패 시 할당된 `catch` 콜백이 실행됩니다. 이 콜백은 배치 내 첫 번째 실패 잡 발생 시 한 번만 호출됩니다.

<a name="allowing-failures"></a>
#### 실패 허용하기

배치 내 하나의 잡 실패 시 자동으로 배치를 `cancelled` 상태로 표시하는 동작을 비활성화할 수도 있습니다. `allowFailures` 메서드를 호출하세요:

```
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // ...
})->allowFailures()->dispatch();
```

<a name="retrying-failed-batch-jobs"></a>
#### 실패한 배치 잡 재시도하기

`queue:retry-batch` Artisan 명령으로 특정 배치의 실패 잡을 쉽게 재시도할 수 있습니다. 배치 UUID를 인자로 넘기세요:

```bash
php artisan queue:retry-batch 32dbc76c-4f82-4749-b610-a639fe0099b5
```

<a name="pruning-batches"></a>
### 배치 데이터 정리 (Pruning Batches)

`job_batches` 테이블은 시간이 지남에 따라 레코드가 빠르게 쌓일 수 있습니다. 이를 방지하려면 `queue:prune-batches` 명령을 매일 스케줄링하세요:

```
$schedule->command('queue:prune-batches')->daily();
```

기본적으로 완료된 지 24시간 지난 배치를 정리합니다. `--hours` 옵션으로 보관 기간을 조정할 수 있습니다. 예:

```
$schedule->command('queue:prune-batches --hours=48')->daily();
```

미완료(batch 실패 등) 레코드 정리는 `--unfinished` 옵션으로 지정합니다:

```
$schedule->command('queue:prune-batches --hours=48 --unfinished=72')->daily();
```

<a name="queueing-closures"></a>
## 클로저 큐잉 (Queueing Closures)

잡 클래스 대신 클로저를 직접 큐에 밀 수도 있습니다. 간단한 단기 작업에 적합합니다. 클로저 코드는 암호화 서명되므로 중간 변조를 방지합니다:

```
$podcast = App\Podcast::find(1);

dispatch(function () use ($podcast) {
    $podcast->publish();
});
```

`catch` 메서드에 실패 시 실행할 클로저를 지정할 수도 있습니다:

```
use Throwable;

dispatch(function () use ($podcast) {
    $podcast->publish();
})->catch(function (Throwable $e) {
    // 잡 실패 처리...
});
```

<a name="running-the-queue-worker"></a>
## 큐 워커 실행하기 (Running The Queue Worker)

<a name="the-queue-work-command"></a>
### `queue:work` 명령어

Laravel은 큐 워커를 실행하는 Artisan 명령어를 제공합니다. 워커는 큐에 새 잡이 들어오면 처리하며, 직접 중단하거나 터미널을 닫기 전까지 계속 실행됩니다:

```
php artisan queue:work
```

> [!TIP]
> `queue:work`를 백그라운드에서 항상 실행하려면 Supervisor 같은 프로세스 매니저를 활용하세요.

큐 워커는 장기 실행 프로세스로 부팅 상태를 메모리에 유지해, 코드 변경을 인지하지 못합니다. 배포 시 [큐 워커 재시작](#queue-workers-and-deployment)을 반드시 수행하세요. 또한, 잡 간에 정적 상태가 유지되니 주의하세요.

비효율적이지만 코드 변경 재시작이 자동인 `queue:listen` 명령도 사용할 수 있습니다:

```
php artisan queue:listen
```

<a name="running-multiple-queue-workers"></a>
#### 다중 큐 워커 실행하기

동시성 향상을 위해서 여러 탭에서 `queue:work` 프로세스를 띄우면 됩니다. 프로덕션에서는 Supervisor 등의 매니저 설정을 통해 여러 프로세스를 실행할 수 있습니다. Supervisor의 경우 `numprocs` 값 사용.

<a name="specifying-the-connection-queue"></a>
#### 연결 및 큐 지정

워커에 특정 큐 연결을 지정하려면 인자로 연결명을 넣습니다. 이는 `config/queue.php` 의 `connections`에 정의된 이름이어야 합니다:

```
php artisan queue:work redis
```

기본적으로 워커는 기본 큐만 처리하지만, 특정 큐만 지정할 수도 있습니다. 예를 들어 Redis 연결의 `emails` 큐만 처리하려면:

```
php artisan queue:work redis --queue=emails
```

<a name="processing-a-specified-number-of-jobs"></a>
#### 지정한 작업 수만큼 처리

`--once` 옵션을 사용하면 워커가 한 개 작업만 처리하고 종료합니다:

```
php artisan queue:work --once
```

`--max-jobs` 옵션으로 지정한 수만큼 작업을 처리 후 종료시킬 수 있습니다. Supervisor와 조합해 메모리 누수를 줄이는 데 유용합니다:

```
php artisan queue:work --max-jobs=1000
```

<a name="processing-all-queued-jobs-then-exiting"></a>
#### 모든 작업 처리 후 종료

`--stop-when-empty` 옵션은 큐가 비면 모든 작업을 처리한 뒤 워커를 정상 종료합니다. Docker 컨테이너 같은 경우 종료를 트리거하는 데 유용합니다:

```
php artisan queue:work --stop-when-empty
```

<a name="processing-jobs-for-a-given-number-of-seconds"></a>
#### 지정한 시간 동안 작업 처리

`--max-time` 옵션은 지정한 시간(초) 동안 작업을 처리하고 종료합니다. Supervisor와 연계해 자원 관리를 할 때 적합합니다:

```
// 1시간 동안 작업 후 종료
php artisan queue:work --max-time=3600
```

<a name="worker-sleep-duration"></a>
#### 워커 대기 시간

큐에 작업이 없으면 워커는 지정한 초만큼 대기 후 다시 조회합니다.

```
php artisan queue:work --sleep=3
```

<a name="resource-considerations"></a>
#### 리소스 고려 사항

데몬 워커는 매 잡 처리마다 프레임워크를 재부팅하지 않습니다. 작업마다 무거운 리소스는 적절히 해제해야 합니다. 예: GD 이미지 처리 후 `imagedestroy` 호출.

<a name="queue-priorities"></a>
### 큐 우선순위 (Queue Priorities)

특정 큐를 우선 처리하려면 대기열 이름을 콤마로 구분해 워커에 넘깁니다. 예를 들어 기본 `redis` 연결의 기본 큐가 `low`일 때 일부 잡을 `high` 큐에 밀면:

```
dispatch((new Job)->onQueue('high'));
```

아래 명령어로 `high`를 우선 처리:

```
php artisan queue:work --queue=high,low
```

<a name="queue-workers-and-deployment"></a>
### 큐 워커와 배포 (Queue Workers & Deployment)

장기 실행 워커는 코드 변경을 자동으로 감지하지 못하므로 배포 시 반드시 워커를 재시작해야 합니다. Graceful restart는 다음 명령어로 실행:

```
php artisan queue:restart
```

워커는 현재 작업이 완료된 후 종료되고, Supervisor 같은 프로세스 매니저가 자동으로 다시 시작합니다.

> [!TIP]
> 워커 재시작 신호에 캐시를 사용하므로 정상 캐시 설정이 필요합니다.

<a name="job-expirations-and-timeouts"></a>
### 작업 만료 및 타임아웃 (Job Expirations & Timeouts)

<a name="job-expiration"></a>
#### 작업 만료

`config/queue.php` 각 연결에 `retry_after` 설정이 있습니다. 이 값은 잡 초기 처리 후 몇 초가 지나면 다시 시도할지를 지정합니다. 예를 들어 90초면, 처리 중인 잡이 90초 이상 실행되면 잡을 큐에 다시 추가합니다.

> [!NOTE]
> Amazon SQS만 `retry_after`가 없고, AWS 콘솔 내 기본 가시성 타임아웃(Default Visibility Timeout)을 사용합니다.

<a name="worker-timeouts"></a>
#### 워커 타임아웃

`queue:work` 명령의 `--timeout` 옵션은 잡 처리 중 이 시간 초과 시 워커가 종료됩니다.

```
php artisan queue:work --timeout=60
```

`retry_after` 설정과 `--timeout` 옵션은 서로 다르지만 함께 작동해 잡 유실을 방지하고 중복 처리를 막습니다.

> [!NOTE]
> `--timeout`은 항상 `retry_after`보다 몇 초 이상 짧아야 합니다. 그래야 처리 중단된 잡을 재시작 전 작업을 종료시킵니다. 타임아웃이 더 길면 잡이 두 번 처리될 수 있습니다.

<a name="supervisor-configuration"></a>
## Supervisor 설정 (Supervisor Configuration)

프로덕션에서 `queue:work` 프로세스가 멈추면 안 되므로, Supervisor 같은 프로세스 모니터가 필요합니다. 워커가 비정상 종료되거나 `queue:restart` 실행 시 자동 재시작을 담당하며, 동시 실행 워커 수 제어도 가능합니다.

<a name="installing-supervisor"></a>
#### Supervisor 설치

Supervisor는 Linux 운영체제용 프로세스 관리자입니다. Ubuntu 기준으로 설치:

```
sudo apt-get install supervisor
```

> [!TIP]
> 직접 관리가 번거롭다면 [Laravel Forge](https://forge.laravel.com)를 이용하세요. 자동 설치 및 구성 기능을 제공합니다.

<a name="configuring-supervisor"></a>
#### Supervisor 설정

설정 파일은 보통 `/etc/supervisor/conf.d`에 위치합니다. 예를 들어 `laravel-worker.conf` 파일을 만들어 워커 모니터링을 설정할 수 있습니다:

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

이 예제에서 `numprocs=8`은 8개의 워커 프로세스를 실행하고 모니터링합니다. `command` 설정은 원하는 연결과 옵션으로 변경하세요.

> [!NOTE]
> `stopwaitsecs`는 가장 오래 걸리는 잡 처리 시간보다 길어야 하며, 그렇지 않으면 Supervisor가 작업 중인 잡을 강제 종료할 수 있습니다.

<a name="starting-supervisor"></a>
#### Supervisor 시작

설정 완료 후 다음 명령어로 Supervisor 설정을 다시 읽고 워커를 시작합니다:

```bash
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start laravel-worker:*
```

자세한 내용은 [Supervisor 공식 문서](http://supervisord.org/index.html)를 참고하세요.

<a name="dealing-with-failed-jobs"></a>
## 실패한 잡 처리 (Dealing With Failed Jobs)

잡이 실패하는 상황은 종종 발생합니다. Laravel은 최대 시도 횟수를 지정할 수 있고, 그 한도를 넘으면 `failed_jobs` 테이블에 해당 잡을 저장합니다.

`failed_jobs` 테이블이 없다면 `queue:failed-table` 명령어로 마이그레이션을 생성하고 마이그레이션하세요:

```
php artisan queue:failed-table

php artisan migrate
```

`queue:work` 명령의 `--tries` 옵션으로 최대 시도 횟수를 지정합니다. 지정하지 않으면 기본 1회 또는 잡 클래스 내 `tries` 값이 적용됩니다:

```
php artisan queue:work redis --tries=3
```

`--backoff` 옵션으로 예외 후 재시도까지 지연 시간을 초 단위로 지정할 수 있습니다:

```
php artisan queue:work redis --tries=3 --backoff=3
```

잡 클래스 내에 `backoff` 속성이나 메서드를 정의해 개별 제어도 가능합니다:

```
/**
 * The number of seconds to wait before retrying the job.
 *
 * @var int
 */
public $backoff = 3;
```

혹은 보다 복잡한 지연 시간 로직이 필요하면 메서드로:

```
/**
* Calculate the number of seconds to wait before retrying the job.
*
* @return int
*/
public function backoff()
{
    return 3;
}
```

배열을 반환하면 지연 시간 배열로 "지수형" 백오프 구현도 가능합니다:

```
/**
* Calculate the number of seconds to wait before retrying the job.
*
* @return array
*/
public function backoff()
{
    return [1, 5, 10];
}
```

<a name="cleaning-up-after-failed-jobs"></a>
### 실패한 잡 후처리 (Cleaning Up After Failed Jobs)

잡 실패 시 사용자 알림이나 작업 롤백이 필요하다면 잡 클래스에 `failed` 메서드를 정의하세요. 예외 객체가 인자로 전달됩니다:

```
<?php

namespace App\Jobs;

use App\Models\Podcast;
use App\Services\AudioProcessor;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;
use Throwable;

class ProcessPodcast implements ShouldQueue
{
    use InteractsWithQueue, Queueable, SerializesModels;

    /**
     * The podcast instance.
     *
     * @var \App\Podcast
     */
    protected $podcast;

    /**
     * Create a new job instance.
     *
     * @param  \App\Models\Podcast  $podcast
     * @return void
     */
    public function __construct(Podcast $podcast)
    {
        $this->podcast = $podcast;
    }

    /**
     * Execute the job.
     *
     * @param  \App\Services\AudioProcessor  $processor
     * @return void
     */
    public function handle(AudioProcessor $processor)
    {
        // Process uploaded podcast...
    }

    /**
     * Handle a job failure.
     *
     * @param  \Throwable  $exception
     * @return void
     */
    public function failed(Throwable $exception)
    {
        // 실패 알림 전송 등...
    }
}
```

> [!NOTE]
> `failed` 호출 전에 잡의 새 인스턴스가 생성되므로, `handle` 내 상태 변경 사항은 전달되지 않습니다.

<a name="retrying-failed-jobs"></a>
### 실패한 잡 재시도 (Retrying Failed Jobs)

`failed_jobs` 테이블 내 실패 목록을 조회하려면:

```
php artisan queue:failed
```

출력된 잡 ID로 개별 재시도:

```
php artisan queue:retry ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece
```

여러 ID 재시도도 가능합니다:

```
php artisan queue:retry ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece 91401d2c-0784-4f43-824c-34f94a33c24d
```

특정 큐 실패 잡 전체 재시도:

```
php artisan queue:retry --queue=name
```

전체 실패 잡 전부 재시도:

```
php artisan queue:retry all
```

실패 잡 삭제는 `queue:forget` 명령어 순번 1건씩:

```
php artisan queue:forget 91401d2c-0784-4f43-824c-34f94a33c24d
```

> [!TIP]
> Horizon 사용자는 `horizon:forget` 명령어를 사용하세요.

모든 실패 잡 삭제는 `queue:flush` 명령어로:

```
php artisan queue:flush
```

<a name="ignoring-missing-models"></a>
### 없는 모델 무시하기 (Ignoring Missing Models)

Eloquent 모델을 잡에 주입 시, 직렬화 후 역직렬화 과정에서 모델이 삭제되었다면 `ModelNotFoundException`이 발생할 수 있습니다.

이를 조용히 무시하고 잡을 자동 삭제하려면 `deleteWhenMissingModels` 속성을 `true`로 설정하세요:

```
/**
 * Delete the job if its models no longer exist.
 *
 * @var bool
 */
public $deleteWhenMissingModels = true;
```

<a name="pruning-failed-jobs"></a>
### 실패한 잡 정리 (Pruning Failed Jobs)

`queue:prune-failed` 명령어로 실패 잡 기록을 삭제할 수 있습니다:

```
php artisan queue:prune-failed
```

`--hours` 옵션으로 보존 기간 조정 가능. 예를 들어 48시간 이상된 실패 기록 삭제:

```
php artisan queue:prune-failed --hours=48
```

<a name="storing-failed-jobs-in-dynamodb"></a>
### DynamoDB에 실패한 잡 저장 (Storing Failed Jobs In DynamoDB)

DynamoDB를 실패 잡 저장소로 사용할 수 있습니다. DynamoDB 테이블은 `failed_jobs`로 하고, 파티션 키 `application`(애플리케이션 이름), 정렬 키 `uuid`가 필요합니다.

AWS SDK 설치:

```nothing
composer require aws/aws-sdk-php
```

`queue.failed.driver` 설정을 `dynamodb`로 지정하고 AWS 인증 정보도 설정합니다:

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
### 실패한 잡 저장 비활성화 (Disabling Failed Job Storage)

실패 잡 저장을 완전히 끄고 싶으면 `queue.failed.driver`를 `null`로 설정하세요:

```
QUEUE_FAILED_DRIVER=null
```

<a name="failed-job-events"></a>
### 실패한 잡 이벤트 (Failed Job Events)

잡 실패 시 실행되는 리스너를 등록하려면 `Queue` 파사드의 `failing` 메서드를 사용하세요. `AppServiceProvider`의 `boot` 메서드 내에서 등록 예:

```
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Queue;
use Illuminate\Support\ServiceProvider;
use Illuminate\Queue\Events\JobFailed;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     *
     * @return void
     */
    public function register()
    {
        //
    }

    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
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
## 큐에서 잡 삭제하기 (Clearing Jobs From Queues)

> [!TIP]
> Horizon 사용 시에는 `queue:clear` 대신 `horizon:clear` 명령어를 사용하세요.

디폴트 연결과 디폴트 큐 내 모든 잡을 삭제하려면:

```
php artisan queue:clear
```

커넥션과 큐를 지정해 삭제할 수도 있습니다:

```
php artisan queue:clear redis --queue=emails
```

> [!NOTE]
> 해당 명령은 SQS, Redis, database 드라이버에서만 지원됩니다. SQS의 경우 메시지 삭제가 최대 60초 지연될 수 있어, 삭제 후 60초 내 들어온 메시지도 삭제될 가능성이 있습니다.

<a name="monitoring-your-queues"></a>
## 큐 모니터링 (Monitoring Your Queues)

급격한 잡 폭주로 인해 큐가 밀려 장시간 대기하는 상황이 발생할 수 있습니다. Laravel은 지정한 잡 수 이상일 때 알림을 보내도록 설정할 수 있습니다.

우선 `queue:monitor` 명령어를 1분 단위로 [스케줄링](/docs/{{version}}/scheduling)하세요. 모니터링할 큐 이름과 임계값을 지정합니다:

```bash
php artisan queue:monitor redis:default,redis:deployments --max=100
```

이 명령어가 개수 초과 큐를 발견하면 `Illuminate\Queue\Events\QueueBusy` 이벤트를 발생시킵니다. `EventServiceProvider`에서 이벤트를 청취해 알림 전송 등 처리할 수 있습니다:

```php
use App\Notifications\QueueHasLongWaitTime;
use Illuminate\Queue\Events\QueueBusy;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\Facades\Notification;

/**
 * Register any other events for your application.
 *
 * @return void
 */
public function boot()
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

<a name="job-events"></a>
## 잡 이벤트 (Job Events)

`Queue` 파사드의 `before`, `after` 메서드를 이용해, 잡 처리 전과 후에 콜백을 등록할 수 있습니다. 예를 들어 추가 로깅이나 통계 증가에 활용합니다. 보통 `AppServiceProvider`의 `boot`에서 등록합니다:

```
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Queue;
use Illuminate\Support\ServiceProvider;
use Illuminate\Queue\Events\JobProcessed;
use Illuminate\Queue\Events\JobProcessing;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     *
     * @return void
     */
    public function register()
    {
        //
    }

    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
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

`looping` 메서드로는, 워커가 다시 잡 하나를 조회하기 전에 호출할 콜백을 지정할 수 있습니다. 예를 들어 이전 잡에서 열린 트랜잭션을 롤백하는 데 사용할 수 있습니다:

```
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Queue;

Queue::looping(function () {
    while (DB::transactionLevel() > 0) {
        DB::rollBack();
    }
});
```