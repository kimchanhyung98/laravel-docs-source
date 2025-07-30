# 큐 (Queues)

- [소개](#introduction)
    - [연결과 큐의 차이 (Connections Vs. Queues)](#connections-vs-queues)
    - [드라이버 주의사항 및 사전 준비 (Driver Notes & Prerequisites)](#driver-prerequisites)
- [잡 생성하기 (Creating Jobs)](#creating-jobs)
    - [잡 클래스 생성하기 (Generating Job Classes)](#generating-job-classes)
    - [클래스 구조 (Class Structure)](#class-structure)
    - [고유 잡 (Unique Jobs)](#unique-jobs)
- [잡 미들웨어 (Job Middleware)](#job-middleware)
    - [비율 제한 (Rate Limiting)](#rate-limiting)
    - [잡 중복 방지 (Preventing Job Overlaps)](#preventing-job-overlaps)
    - [예외 조절 (Throttling Exceptions)](#throttling-exceptions)
- [잡 디스패치 (Dispatching Jobs)](#dispatching-jobs)
    - [지연 디스패치 (Delayed Dispatching)](#delayed-dispatching)
    - [동기 디스패치 (Synchronous Dispatching)](#synchronous-dispatching)
    - [잡과 데이터베이스 트랜잭션 (Jobs & Database Transactions)](#jobs-and-database-transactions)
    - [잡 체이닝 (Job Chaining)](#job-chaining)
    - [큐 및 연결 커스터마이징 (Customizing The Queue & Connection)](#customizing-the-queue-and-connection)
    - [최대 재시도 및 타임아웃 지정 (Max Job Attempts / Timeout Values)](#max-job-attempts-and-timeout)
    - [에러 처리 (Error Handling)](#error-handling)
- [잡 배칭 (Job Batching)](#job-batching)
    - [배치 가능 잡 정의 (Defining Batchable Jobs)](#defining-batchable-jobs)
    - [배치 디스패치 (Dispatching Batches)](#dispatching-batches)
    - [배치에 잡 추가 (Adding Jobs To Batches)](#adding-jobs-to-batches)
    - [배치 정보 확인 (Inspecting Batches)](#inspecting-batches)
    - [배치 취소 (Cancelling Batches)](#cancelling-batches)
    - [배치 실패 처리 (Batch Failures)](#batch-failures)
    - [배치 데이터 정리 (Pruning Batches)](#pruning-batches)
- [클로저 큐잉 (Queueing Closures)](#queueing-closures)
- [큐 작업자 실행 (Running The Queue Worker)](#running-the-queue-worker)
    - [`queue:work` 명령어](#the-queue-work-command)
    - [큐 우선순위 설정 (Queue Priorities)](#queue-priorities)
    - [큐 작업자와 배포 (Queue Workers & Deployment)](#queue-workers-and-deployment)
    - [잡 만료 및 타임아웃 (Job Expirations & Timeouts)](#job-expirations-and-timeouts)
- [Supervisor 설정 (Supervisor Configuration)](#supervisor-configuration)
- [실패한 잡 다루기 (Dealing With Failed Jobs)](#dealing-with-failed-jobs)
    - [실패한 잡 정리 (Cleaning Up After Failed Jobs)](#cleaning-up-after-failed-jobs)
    - [실패한 잡 재시도 (Retrying Failed Jobs)](#retrying-failed-jobs)
    - [모델이 없을 때 무시하기 (Ignoring Missing Models)](#ignoring-missing-models)
    - [실패한 잡 정리 (Pruning Failed Jobs)](#pruning-failed-jobs)
    - [DynamoDB에 실패한 잡 저장하기 (Storing Failed Jobs In DynamoDB)](#storing-failed-jobs-in-dynamodb)
    - [실패 잡 저장 비활성화 (Disabling Failed Job Storage)](#disabling-failed-job-storage)
    - [실패 잡 이벤트 (Failed Job Events)](#failed-job-events)
- [큐에서 잡 삭제하기 (Clearing Jobs From Queues)](#clearing-jobs-from-queues)
- [큐 모니터링 (Monitoring Your Queues)](#monitoring-your-queues)
- [잡 이벤트 (Job Events)](#job-events)

<a name="introduction"></a>
## 소개 (Introduction)

웹 애플리케이션을 개발할 때, 업로드된 CSV 파일을 파싱하고 저장하는 등의 작업이 일반적인 웹 요청 처리 시간 안에 끝나기에는 너무 오래 걸릴 수 있습니다. 다행히 Laravel은 쉽게 백그라운드에서 처리할 수 있는 큐 잡(queue jobs)을 만들 수 있게 해줍니다. 시간이 오래 걸리는 작업을 큐로 이동하면, 애플리케이션은 웹 요청에 매우 빠르게 응답할 수 있으며 사용자에게 더 좋은 경험을 제공합니다.

Laravel 큐는 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 혹은 관계형 데이터베이스 등 여러 큐 백엔드를 아우르는 통일된 큐 API를 제공합니다.

Laravel 큐 설정 옵션은 애플리케이션의 `config/queue.php` 파일에 있습니다. 이 파일에서 데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 드라이버를 포함한 프레임워크 내장 큐 드라이버 각각의 연결 설정을 볼 수 있습니다. 또한 즉시 작업을 실행하는 동기 드라이버(synchronous driver)도 있어, 로컬 개발 중에 즉시 실행할 때 유용합니다. `null` 드라이버도 제공되는데, 이는 큐 잡을 버립니다.

> [!NOTE]
> Laravel은 Redis 기반 큐를 위한 멋진 대시보드 및 설정 시스템인 Horizon을 제공합니다. 자세한 내용은 [Horizon 문서](/docs/9.x/horizon)를 참고하세요.

<a name="connections-vs-queues"></a>
### 연결과 큐의 차이 (Connections Vs. Queues)

Laravel 큐를 시작하기 전에 `connections`와 `queues`의 차이를 이해하는 것이 중요합니다. `config/queue.php` 파일에는 `connections` 배열이 있는데, 이는 Amazon SQS, Beanstalk, Redis 등 백엔드 큐 서비스와의 연결을 정의합니다. 그러나 각 연결(connection)은 여러 "queues"를 가질 수 있는데, 이는 각각 다른 작업 더미(stack)라고 생각하면 됩니다.

`queue.php` 설정 파일 내 각 연결 구성은 `queue` 속성을 포함하는데, 이는 해당 연결에 작업이 디스패치될 때 기본적으로 사용되는 큐입니다. 즉, 잡을 디스패치할 때 명시적으로 큐를 지정하지 않으면 연결 구성의 `queue` 속성으로 정의된 큐에 잡이 들어갑니다:

```php
use App\Jobs\ProcessPodcast;

// 디폴트 연결의 디폴트 큐에 잡이 전송됩니다...
ProcessPodcast::dispatch();

// 디폴트 연결의 "emails" 큐에 잡이 전송됩니다...
ProcessPodcast::dispatch()->onQueue('emails');
```

어떤 애플리케이션은 여러 큐에 잡을 푸시할 필요 없이 하나의 간단한 큐만으로 충분할 수 있습니다. 하지만 여러 큐를 사용하는 것은 작업 처리 우선순위 또는 처리를 분리하고자 할 때 특히 유용합니다. Laravel 큐 작업자는 처리할 큐를 우선순위별로 지정할 수 있기 때문입니다. 예를 들어, `high` 큐에 작업을 푸시한 뒤, `high` 큐를 우선 처리하는 작업자를 실행할 수 있습니다:

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버 주의사항 및 사전 준비 (Driver Notes & Prerequisites)

<a name="database"></a>
#### 데이터베이스 (Database)

`database` 큐 드라이버를 사용하려면 잡을 저장할 데이터베이스 테이블이 필요합니다. 테이블 생성 마이그레이션을 만들려면 `queue:table` Artisan 명령어를 실행하세요. 마이그레이션 파일 생성 후에는 `migrate` 명령어를 사용해 마이그레이션을 수행합니다:

```shell
php artisan queue:table

php artisan migrate
```

마지막으로, 애플리케이션 `.env` 파일에서 `QUEUE_CONNECTION` 변수를 `database`로 설정하여 애플리케이션이 이 드라이버를 사용하도록 지정하는 것을 잊지 마세요:

```
QUEUE_CONNECTION=database
```

<a name="redis"></a>
#### Redis

Redis 큐 드라이버를 사용하려면 `config/database.php` 파일에 Redis 데이터베이스 연결을 구성해야 합니다.

**Redis 클러스터**

Redis 클러스터를 사용하는 경우, 큐 이름에 [키 해시 태그(key hash tag)](https://redis.io/docs/reference/cluster-spec/#hash-tags)를 포함해야 합니다. 이는 주어진 큐의 모든 Redis 키가 같은 해시 슬롯에 들어가도록 보장하기 위한 것입니다:

```php
'redis' => [
    'driver' => 'redis',
    'connection' => 'default',
    'queue' => '{default}',
    'retry_after' => 90,
],
```

**블로킹 (Blocking)**

Redis 큐에서 `block_for` 구성 옵션으로 드라이버가 잡이 사용 가능해질 때까지 얼마나 오래 기다릴지 지정할 수 있습니다. 큐 로드에 맞춰 이 값을 조절하면 계속해서 Redis를 폴링하는 것보다 효율적일 수 있습니다. 예를 들어, 잡이 생길 때까지 5초간 블로킹하도록 설정할 수 있습니다:

```php
'redis' => [
    'driver' => 'redis',
    'connection' => 'default',
    'queue' => 'default',
    'retry_after' => 90,
    'block_for' => 5,
],
```

> [!WARNING]
> `block_for` 값을 `0`으로 설정하면 큐 작업자는 잡이 들어올 때까지 무기한 블로킹되며, 이 동안 `SIGTERM` 같은 시그널을 처리하지 못합니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 사전 준비

아래 드라이버들은 설치를 위해 Composer 패키지 관리자를 통해 의존성을 별도로 설치해야 합니다:

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~4.0`
- Redis: `predis/predis ~1.0` 또는 phpredis PHP 확장

<a name="creating-jobs"></a>
## 잡 생성하기 (Creating Jobs)

<a name="generating-job-classes"></a>
### 잡 클래스 생성하기 (Generating Job Classes)

기본적으로 큐 작업 클래스는 `app/Jobs` 디렉터리에 저장됩니다. `app/Jobs` 디렉터리가 없으면 `make:job` Artisan 명령어를 실행할 때 자동으로 생성됩니다:

```shell
php artisan make:job ProcessPodcast
```

생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하며, Laravel에게 이 잡이 비동기로 큐에 푸시되어 실행되어야 한다는 것을 알립니다.

> [!NOTE]
> 잡 스텁은 [스텁 퍼블리싱](/docs/9.x/artisan#stub-customization) 기능을 통해 사용자 정의할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조 (Class Structure)

잡 클래스는 매우 단순하며 보통 큐 실행 시 호출되는 `handle` 메서드만 포함합니다. 시작을 위해 팟캐스트 퍼블리싱 서비스를 관리한다고 가정하고, 업로드된 팟캐스트 파일 처리가 필요한 예시 잡 클래스를 살펴봅니다:

```php
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
     * 팟캐스트 인스턴스
     *
     * @var \App\Models\Podcast
     */
    public $podcast;

    /**
     * 새로운 잡 인스턴스 생성
     *
     * @param  App\Models\Podcast  $podcast
     * @return void
     */
    public function __construct(Podcast $podcast)
    {
        $this->podcast = $podcast;
    }

    /**
     * 잡 실행
     *
     * @param  App\Services\AudioProcessor  $processor
     * @return void
     */
    public function handle(AudioProcessor $processor)
    {
        // 업로드된 팟캐스트 처리...
    }
}
```

위 예시에서 Eloquent 모델을 잡 생성자에 직접 전달할 수 있는데, 이는 잡 클래스에서 `SerializesModels` 트레이트를 사용하기 때문입니다. 이 덕분에 Eloquent 모델과 로드된 연관관계가 큐에 직렬화되어 작업 처리 시 원활하게 역직렬화됩니다.

큐에 넣은 잡이 Eloquent 모델을 받을 때, 모델 전체가 아니라 모델 식별자만 직렬화됩니다. 작업 처리 시, 큐 시스템이 DB에서 모델과 연관 관계를 자동으로 다시 조회합니다. 이렇게 하면 큐 드라이버에 전송되는 작업 페이로드가 훨씬 작아져 효율적입니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드 의존성 주입

`handle` 메서드는 잡 작업 큐 실행 시 호출되며, 여기에 파라미터 타입힌트를 지정하면 Laravel 서비스 컨테이너가 자동으로 의존성을 주입합니다.

컨테이너가 `handle` 메서드에 대한 의존성 주입 방식을 완전히 제어하려면, `bindMethod` 메서드를 사용할 수 있습니다. 이 메서드는 잡과 컨테이너를 인수로 받는 콜백을 등록하며, 콜백에서 `handle` 메서드를 원하는 방식으로 호출할 수 있습니다. 보통 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 호출합니다:

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function ($job, $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 바이너리 데이터(예: 원본 이미지)는 큐에 전달하기 전 `base64_encode` 함수를 거쳐야 합니다. 그렇지 않으면 잡이 큐에 JSON으로 제대로 직렬화되지 않을 수 있습니다.

<a name="handling-relationships"></a>
#### 큐에직렬화된 연관관계

로드된 연관관계도 직렬화되기 때문에 직렬화된 잡 데이터가 매우 커질 수 있습니다. 연관관계 직렬화를 방지하려면, 모델을 속성으로 할당할 때 `withoutRelations` 메서드를 호출하세요. 이 메서드는 연관관계가 제외된 모델 인스턴스를 반환합니다:

```php
/**
 * 새로운 잡 인스턴스 생성
 *
 * @param  \App\Models\Podcast  $podcast
 * @return void
 */
public function __construct(Podcast $podcast)
{
    $this->podcast = $podcast->withoutRelations();
}
```

또한, 직렬화된 잡이 역직렬화되어 모델 연관관계가 다시 DB에서 조회될 때, 직렬화 당시 적용한 관계 제한 조건은 적용되지 않습니다. 따라서 특정 연관관계 부분집합을 다루려면 잡 처리 시 다시 제한을 걸어야 합니다.

<a name="unique-jobs"></a>
### 고유 잡 (Unique Jobs)

> [!WARNING]
> 고유 잡은 [락(lock)](/docs/9.x/cache#atomic-locks)을 지원하는 캐시 드라이버가 필요합니다. 현재는 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버에서 지원됩니다. 또한 고유 잡 제약은 배치 내 잡에는 적용되지 않습니다.

특정 잡이 큐에 단 하나만 존재하도록 보장하고 싶을 때, 잡 클래스가 `ShouldBeUnique` 인터페이스를 구현하도록 하면 됩니다. 이 인터페이스는 메서드 구현을 요구하지 않습니다:

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    ...
}
```

위 예시는 `UpdateSearchIndex` 잡이 고유하므로, 같은 잡 인스턴스가 큐에 이미 있으면 새 디스패치를 무시합니다.

특정 키를 고유성 판별 기준으로 지정하거나, 고유성이 유지되는 시간 제한을 두고 싶을 때는 `uniqueId`와 `uniqueFor` 속성 또는 메서드를 구현합니다:

```php
<?php

use App\Models\Product;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    /**
     * 제품 인스턴스
     *
     * @var \App\Product
     */
    public $product;

    /**
     * 고유 락 해제까지의 초
     *
     * @var int
     */
    public $uniqueFor = 3600;

    /**
     * 잡의 고유 ID 반환
     *
     * @return string
     */
    public function uniqueId()
    {
        return $this->product->id;
    }
}
```

위 예시는 제품 ID별로 잡이 고유하므로, 같은 제품 ID로 신규 디스패치 요청을 무시하며 기존 작업이 완료되면 다시 받아들입니다. 처리 완료까지 1시간이 넘으면 락이 해제되어 같은 키로 새로운 잡을 디스패치할 수 있습니다.

> [!WARNING]
> 여러 웹 서버나 컨테이너에서 잡을 디스패치한다면 모든 서버가 동일한 중앙 캐시 서버를 사용해야 정확한 고유성 판단이 가능합니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 처리 시작 전까지 잡 고유 유지

기본적으로 고유 잡 락은 잡이 처리 완료되거나 모든 재시도 실패 시 해제됩니다. 하지만 처리 시작 직전에 락 해제를 원하면, `ShouldBeUnique` 대신 `ShouldBeUniqueUntilProcessing` 인터페이스를 구현하세요:

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
#### 고유 잡 락 (Unique Job Locks)

`ShouldBeUnique` 잡이 디스패치되면, Laravel은 `uniqueId` 기반의 [락](/docs/9.x/cache#atomic-locks)을 획득하려합니다. 락을 얻지 못하면 잡은 디스패치되지 않습니다. 락은 잡 처리 완료 혹은 모든 재시도 실패 시 해제됩니다. 기본적으로는 기본 캐시 드라이버를 사용합니다. 다른 드라이버를 쓰고 싶다면 `uniqueVia` 메서드를 구현해 락에 사용할 캐시 드라이버를 반환하세요:

```php
use Illuminate\Support\Facades\Cache;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    ...

    /**
     * 고유 잡 락에 사용할 캐시 드라이버 반환
     *
     * @return \Illuminate\Contracts\Cache\Repository
     */
    public function uniqueVia()
    {
        return Cache::driver('redis');
    }
}
```

> [!NOTE]
> 잡 동시 처리 제한만 필요하다면 [`WithoutOverlapping`](/docs/9.x/queues#preventing-job-overlaps) 잡 미들웨어를 사용하는 것이 적절합니다.

<a name="job-middleware"></a>
## 잡 미들웨어 (Job Middleware)

잡 미들웨어는 큐 작업 실행 전후에 맞춤 로직을 감싸기 위해 사용하며, 잡 내 중복 코드를 줄여줍니다. 예를 들어, Laravel의 Redis 비율 제한 기능을 이용해 5초에 한 번만 잡이 실행되도록 한 `handle` 메서드는 다음과 같습니다:

```php
use Illuminate\Support\Facades\Redis;

/**
 * 잡 실행
 *
 * @return void
 */
public function handle()
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

이 코드는 유효하지만, `handle` 메서드에 비율 제한 로직이 낀 채로 복잡해집니다. 또한 비율 제한을 적용할 다른 잡마다 중복 구현해야 합니다.

이 대신, 비율 제한 잡 미들웨어를 만들어 적용할 수 있습니다. Laravel은 잡 미들웨어 위치를 정하지 않으므로 원하는 곳에 미들웨어를 둘 수 있습니다. 이 예시에선 `app/Jobs/Middleware` 폴더에 둡니다:

```php
<?php

namespace App\Jobs\Middleware;

use Illuminate\Support\Facades\Redis;

class RateLimited
{
    /**
     * 큐 잡 처리
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
                    // 락 획득됨...

                    $next($job);
                }, function () use ($job) {
                    // 락 획득 실패...

                    $job->release(5);
                });
    }
}
```

작동 방식은 [라우트 미들웨어](/docs/9.x/middleware)와 유사하게 잡 미들웨어도 처리 중인 잡과 다음 콜백을 인수로 받습니다.

만든 미들웨어는 잡 클래스의 `middleware` 메서드에서 반환하여 붙일 수 있습니다. `make:job`으로 생성한 잡 클래스에는 기본에 없으므로 직접 추가해야 합니다:

```php
use App\Jobs\Middleware\RateLimited;

/**
 * 통과시킬 미들웨어 반환
 *
 * @return array
 */
public function middleware()
{
    return [new RateLimited];
}
```

> [!NOTE]
> 잡 미들웨어는 큐에 들어가는 이벤트 리스너, 메일러, 알림 등에도 할당할 수 있습니다.

<a name="rate-limiting"></a>
### 비율 제한 (Rate Limiting)

직접 만든 미들웨어 대신, Laravel은 잡 비율 제한 미들웨어를 기본 제공하며 사용할 수 있습니다. 라우트 비율 제한기처럼 `RateLimiter` 파사드의 `for` 메서드로 정의합니다.

예를 들어, 일반 고객은 한 시간에 한 번만 백업하도록 제한하고, 프리미엄 고객은 제한 없이 허용하고 싶다면, `AppServiceProvider`의 `boot` 메서드에 다음을 정의합니다:

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Support\Facades\RateLimiter;

/**
 * 애플리케이션 서비스 부트스트랩
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

위는 시간 단위 제한 예시이며, `perMinute` 메서드로 분 단위 제한도 정의할 수 있습니다. `by` 메서드에는 어떤 값이든 넣을 수 있으나, 보통 고객 기준으로 세그먼트합니다:

```php
return Limit::perMinute(50)->by($job->user->id);
```

비율 제한을 정의한 뒤 잡 클래스의 `Illuminate\Queue\Middleware\RateLimited` 미들웨어에 이름을 지정해 붙입니다. 제한 초과 시 미들웨어는 적절한 지연을 두고 작업을 다시 큐에 재전송합니다.

```php
use Illuminate\Queue\Middleware\RateLimited;

/**
 * 잡 미들웨어 반환
 *
 * @return array
 */
public function middleware()
{
    return [new RateLimited('backups')];
}
```

비율 제한으로 다시 큐에 들어간 잡은 시도 횟수(`attempts`)가 계속 증가합니다. 따라서 잡 클래스의 `tries`나 `maxExceptions` 속성을 조정하거나 [`retryUntil` 메서드](#time-based-attempts)로 재시도 종료 시간을 조절할 수 있습니다.

재시도 시 비율 제한 잡을 재발송하지 않으려면 `dontRelease` 메서드를 사용하세요:

```php
/**
 * 잡 미들웨어 반환
 *
 * @return array
 */
public function middleware()
{
    return [(new RateLimited('backups'))->dontRelease()];
}
```

> [!NOTE]
> Redis를 사용할 경우, `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어가 기본 RateLimited 미들웨어보다 Redis에 최적화되어 있고 효율적입니다.

<a name="preventing-job-overlaps"></a>
### 잡 중복 방지 (Preventing Job Overlaps)

Laravel은 임의 키를 기준으로 잡 중복을 방지하는 `Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어를 제공합니다. 이는 큐 잡이 리소스를 수정하는데 한 번에 하나의 잡만 수정하도록 보장할 때 유용합니다.

예를 들어, 사용자 신용점수를 업데이트하는 잡이 있고 같은 사용자 ID에 대해 중복 실행을 방지하려면 잡 클래스의 `middleware` 메서드에서 `WithoutOverlapping` 미들웨어를 반환합니다:

```php
use Illuminate\Queue\Middleware\WithoutOverlapping;

/**
 * 잡 미들웨어 반환
 *
 * @return array
 */
public function middleware()
{
    return [new WithoutOverlapping($this->user->id)];
}
```

같은 인스턴스가 중복 실행되면 다시 큐에 재발송됩니다. 재발송 전에 대기해야 하는 시간(초)을 지정하려면 `releaseAfter` 메서드를 사용합니다:

```php
/**
 * 잡 미들웨어 반환
 *
 * @return array
 */
public function middleware()
{
    return [(new WithoutOverlapping($this->order->id))->releaseAfter(60)];
}
```

중복된 잡이 즉시 삭제되어 재시도하지 않게 하려면 `dontRelease`를 호출하세요:

```php
/**
 * 잡 미들웨어 반환
 *
 * @return array
 */
public function middleware()
{
    return [(new WithoutOverlapping($this->order->id))->dontRelease()];
}
```

`WithoutOverlapping` 미들웨어는 Laravel 원자 락 기능을 사용합니다. 잡이 실패하거나 타임아웃 되어 락이 해제되지 않을 수도 있으므로 `expireAfter` 메서드로 락 만료 시간을 설정할 수 있습니다. 예를 들어 처리 시작 후 3분 뒤 락을 해제하도록 설정하는 코드입니다:

```php
/**
 * 잡 미들웨어 반환
 *
 * @return array
 */
public function middleware()
{
    return [(new WithoutOverlapping($this->order->id))->expireAfter(180)];
}
```

> [!WARNING]
> `WithoutOverlapping` 미들웨어는 [락을 지원하는 캐시 드라이버](/docs/9.x/cache#atomic-locks)가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array`를 지원합니다.

<a name="sharing-lock-keys"></a>
#### 잡 클래스 간 락 키 공유

기본적으로 `WithoutOverlapping` 미들웨어는 동일 클래스의 중복 잡만 방지합니다. 다른 클래스의 잡이라도 같은 락 키를 쓰면 중복 방지가 작동하지 않습니다. 하지만 `shared` 메서드를 호출하면 서로 다른 잡 클래스 간에도 락 키를 공유하도록 할 수 있습니다:

```php
use Illuminate\Queue\Middleware\WithoutOverlapping;

class ProviderIsDown
{
    // ...

    public function middleware()
    {
        return [
            (new WithoutOverlapping("status:{$this->provider}"))->shared(),
        ];
    }
}

class ProviderIsUp
{
    // ...

    public function middleware()
    {
        return [
            (new WithoutOverlapping("status:{$this->provider}"))->shared(),
        ];
    }
}
```

<a name="throttling-exceptions"></a>
### 예외 조절 (Throttling Exceptions)

Laravel은 예외 발생을 조절하는 `Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어를 제공합니다. 잡이 지정 횟수 이상의 예외를 던지면, 이후 실행 시도를 지정 시간 동안 지연시킵니다. 제3자 서비스와 상호작용하는 잡의 불안정성을 완화할 때 유용합니다.

예시: 불안정한 API와 상호작용하는 잡이 예외를 연속적으로 던질 때 예외 조절 미들웨어를 쓰면 아래처럼 설정합니다. 이 미들웨어는 [시간 기반 재시도](#time-based-attempts)와 함께 쓰는 것이 권장됩니다.

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡 미들웨어 반환
 *
 * @return array
 */
public function middleware()
{
    return [new ThrottlesExceptions(10, 5)];
}

/**
 * 잡 재시도 종료 시간
 *
 * @return \DateTime
 */
public function retryUntil()
{
    return now()->addMinutes(5);
}
```

생성자 첫번째 인자는 예외 발생 횟수 임계값, 두번째 인자는 조절 해제까지 대기할 분(minutes)입니다. 위 예시에서는 5분 동안 10회 예외가 발생하면 이후 5분 동안 잡 실행을 중지합니다.

예외가 발생했지만 임계치에 도달하지 않은 경우 즉시 재시도하나, `backoff` 메서드로 지연 시간을 지정할 수 있습니다:

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡 미들웨어 반환
 *
 * @return array
 */
public function middleware()
{
    return [(new ThrottlesExceptions(10, 5))->backoff(5)];
}
```

내부에는 Laravel 캐시 시스템을 이용해 제한하며, 잡 클래스 명이 캐시 키로 쓰입니다. 여러 잡이 같은 서비스와 상호작용하는 경우, `by` 메서드로 키를 지정해 예외 조절 공유가 가능합니다:

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡 미들웨어 반환
 *
 * @return array
 */
public function middleware()
{
    return [(new ThrottlesExceptions(10, 10))->by('key')];
}
```

> [!NOTE]
> Redis 사용 시 `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어가 기본 미들웨어보다 Redis에 최적화되어 효율적입니다.

<a name="dispatching-jobs"></a>
## 잡 디스패치 (Dispatching Jobs)

잡 클래스를 작성한 뒤, 해당 클래스의 `dispatch` 메서드를 통해 디스패치할 수 있습니다. `dispatch`에 전달된 인수는 잡 생성자에 전달됩니다:

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    /**
     * 새 팟캐스트 저장
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        $podcast = Podcast::create(/* ... */);

        // ...

        ProcessPodcast::dispatch($podcast);
    }
}
```

조건부로 디스패치하려면 `dispatchIf`와 `dispatchUnless` 메서드를 쓸 수 있습니다:

```php
ProcessPodcast::dispatchIf($accountActive, $podcast);

ProcessPodcast::dispatchUnless($accountSuspended, $podcast);
```

새 Laravel 애플리케이션에서는 기본 큐 드라이버로 `sync`가 설정되어 있습니다. 이는 잡을 동기적으로 현재 요청 내에서 실행하므로 로컬 개발에 편리합니다. 실제 백그라운드 처리를 위해선 `config/queue.php`에서 다른 큐 드라이버를 지정하세요.

<a name="delayed-dispatching"></a>
### 지연 디스패치 (Delayed Dispatching)

잡이 즉시 대기열에 나타나지 않고 일정 시간이 지난 후에 처리되도록 하려면, 디스패치 시 `delay` 메서드를 체인으로 연결할 수 있습니다. 예를 들어, 디스패치한 지 10분 후부터 잡이 처리되도록 지정하는 코드입니다:

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    /**
     * 새 팟캐스트 저장
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        $podcast = Podcast::create(/* ... */);

        // ...

        ProcessPodcast::dispatch($podcast)
                    ->delay(now()->addMinutes(10));
    }
}
```

> [!WARNING]
> Amazon SQS 큐 서비스의 최대 지연 시간은 15분입니다.

<a name="dispatching-after-the-response-is-sent-to-browser"></a>
#### 응답 후 잡 디스패치

`dispatchAfterResponse` 메서드는 HTTP 응답이 사용자에게 전송된 후에 잡을 디스패치합니다(FastCGI 서버에서 동작). 실행 중인 잡이 있더라도 사용자 경험에 영향을 주지 않도록 합니다. 보통 이메일 전송 등 1초 정도 걸리는 작업에 적합합니다. 이 경우 큐 작업자가 필요 없습니다:

```php
use App\Jobs\SendNotification;

SendNotification::dispatchAfterResponse();
```

또한 클로저를 디스패치하고 `afterResponse` 메서드를 체인하여 응답 후 실행 설정할 수도 있습니다:

```php
use App\Mail\WelcomeMessage;
use Illuminate\Support\Facades\Mail;

dispatch(function () {
    Mail::to('taylor@example.com')->send(new WelcomeMessage);
})->afterResponse();
```

<a name="synchronous-dispatching"></a>
### 동기 디스패치 (Synchronous Dispatching)

즉시 잡을 실행하려면 `dispatchSync` 메서드를 사용합니다. 이 경우 잡은 큐에 들어가지 않고 현재 프로세스에서 즉시 실행됩니다:

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    /**
     * 새 팟캐스트 저장
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        $podcast = Podcast::create(/* ... */);

        // 팟캐스트 생성...

        ProcessPodcast::dispatchSync($podcast);
    }
}
```

<a name="jobs-and-database-transactions"></a>
### 잡과 데이터베이스 트랜잭션 (Jobs & Database Transactions)

잡을 데이터베이스 트랜잭션 내에서 디스패치해도 문제없지만, 잡이 정상 실행될 수 있도록 주의해야 합니다. 트랜잭션이 커밋되기 전에 작업자가 잡을 처리하면, 트랜잭션 내에서 변경한 모델이나 DB 레코드가 반영되지 않을 수 있고, 트랜잭션 내에서 새로 생성된 모델이나 레코드는 존재하지 않을 수 있습니다.

Laravel은 이를 해결하기 위해 여러 방법을 제공합니다. 첫 번째로, 큐 연결 구성 배열에 `after_commit` 옵션을 설정할 수 있습니다:

```php
'redis' => [
    'driver' => 'redis',
    // ...
    'after_commit' => true,
],
```

`after_commit` 옵션이 `true`면, 트랜잭션 내에서 잡을 디스패치해도 Laravel은 열린 모든 트랜잭션이 커밋된 후에 잡을 실제로 디스패치합니다. 트랜잭션이 없으면 즉시 디스패치합니다.

트랜잭션 중에 예외가 발생해 롤백되면, 해당 트랜잭션 내에 디스패치된 잡들은 폐기됩니다.

> [!NOTE]
> `after_commit` 옵션을 `true`로 설정하면, 큐 이벤트 리스너, 메일러, 알림, 브로드캐스트 이벤트도 열린 트랜잭션이 모두 커밋된 후 디스패치 됩니다.

<a name="specifying-commit-dispatch-behavior-inline"></a>
#### 커밋 후 디스패치 동작을 인라인으로 지정

`after_commit` 옵션을 설정하지 않더라도, 특정 잡만 열린 트랜잭션 커밋 후에 디스패치할 수 있습니다. 이때 `afterCommit` 메서드를 체인으로 연결하세요:

```php
use App\Jobs\ProcessPodcast;

ProcessPodcast::dispatch($podcast)->afterCommit();
```

반대로 `after_commit` 옵션이 `true`일 때, 특정 잡을 즉시 디스패치하려면 `beforeCommit` 메서드를 체인으로 연결할 수 있습니다:

```php
ProcessPodcast::dispatch($podcast)->beforeCommit();
```

<a name="job-chaining"></a>
### 잡 체이닝 (Job Chaining)

잡 체이닝은 주 잡 실행 성공 후 순차적으로 실행되는 잡 리스트를 지정하는 기능입니다. 한 잡이라도 실패하면 이후 잡은 실행되지 않습니다. 잡 체인을 실행하려면 `Bus` 파사드의 `chain` 메서드를 사용하세요:

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

클래스 인스턴스뿐 아니라 클로저도 체이닝할 수 있습니다:

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
> 잡 내부에서 `$this->delete()`를 호출해도 체인이 중단되지 않습니다. 오직 체인 내 잡이 실패할 때만 중단됩니다.

<a name="chain-connection-queue"></a>
#### 체인 연결 및 큐 지정

체인 잡의 연결과 큐를 지정하려면 `onConnection`과 `onQueue` 메서드를 사용합니다. 잡 클래스가 다른 연결과 큐를 명시하지 않으면 여기서 지정한 값이 적용됩니다:

```php
Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->onConnection('redis')->onQueue('podcasts')->dispatch();
```

<a name="chain-failures"></a>
#### 체인 실패 처리

체인 잡 중 하나가 실패하면 `catch` 메서드로 등록한 콜백이 호출됩니다. 콜백 인자로 실패를 일으킨 `Throwable` 객체가 전달됩니다:

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
> 체인 콜백은 나중에 큐로 실행되므로 `$this` 변수 사용을 피하세요.

<a name="customizing-the-queue-and-connection"></a>
### 큐 및 연결 커스터마이징 (Customizing The Queue & Connection)

<a name="dispatching-to-a-particular-queue"></a>
#### 특정 큐에 디스패치하기

여러 큐로 잡을 분류해 우선순위와 작업자 할당을 조절할 수 있습니다. 이는 `config/queue.php`에서 정의한 연결 내, 특정 큐 이름으로만 지정되는 것입니다. 잡 디스패치 시 `onQueue` 메서드로 큐를 정합니다:

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    /**
     * 새 팟캐스트 저장
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        $podcast = Podcast::create(/* ... */);

        // 팟캐스트 생성...

        ProcessPodcast::dispatch($podcast)->onQueue('processing');
    }
}
```

또는 잡 생성자 안에서 `onQueue`를 호출해 디폴트 큐를 정할 수도 있습니다:

```php
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
     * 새 잡 인스턴스 생성
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
#### 특정 연결에 디스패치하기

애플리케이션이 여러 큐 연결을 사용할 경우, 잡을 어느 연결에 푸시할지 `onConnection` 메서드로 지정합니다:

```php
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    /**
     * 새 팟캐스트 저장
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        $podcast = Podcast::create(/* ... */);

        // 팟캐스트 생성...

        ProcessPodcast::dispatch($podcast)->onConnection('sqs');
    }
}
```

`onConnection`과 `onQueue`를 체인할 수 있습니다:

```php
ProcessPodcast::dispatch($podcast)
              ->onConnection('sqs')
              ->onQueue('processing');
```

잡 생성자에서 연결을 정할 수도 있습니다:

```php
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
     * 새 잡 인스턴스 생성
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
#### 최대 시도 횟수 (Max Attempts)

큐 잡이 오류를 겪으면 무한 재시도는 원치 않을 겁니다. Laravel은 여러 방식으로 최대 시도 횟수를 지정할 수 있습니다.

Artisan 명령어 `queue:work` 실행 시 `--tries` 옵션을 지정하면, 해당 값만큼 작업자(worker)가 잡 재시도를 시도합니다. 잡 클래스에 별도로 시도 횟수를 정의하면, CLI 옵션보다 잡 클래스 설정이 우선합니다:

```shell
php artisan queue:work --tries=3
```

최대 시도를 넘으면 잡은 "실패한 잡"으로 간주돼 처리됩니다. 실패한 잡 처리 방법은 [실패 잡 문서](#dealing-with-failed-jobs)를 참고하세요. `--tries=0`일 경우 무한 재시도합니다.

잡 클래스 필드로도 재시도 횟수를 지정할 수 있습니다:

```php
<?php

namespace App\Jobs;

class ProcessPodcast implements ShouldQueue
{
    /**
     * 최대 시도 횟수
     *
     * @var int
     */
    public $tries = 5;
}
```

<a name="time-based-attempts"></a>
#### 시간 기반 시도 제한 (Time Based Attempts)

재시도 횟수 제한 대신, 특정 시간이 지나면 더 이상 잡을 시도하지 않도록 할 수 있습니다. 잡 클래스에 `retryUntil` 메서드를 추가하고 `DateTime` 객체를 리턴하면 됩니다:

```php
/**
 * 잡 타임아웃 시점 결정
 *
 * @return \DateTime
 */
public function retryUntil()
{
    return now()->addMinutes(10);
}
```

> [!NOTE]
> [큐에 들어가는 이벤트 리스너](/docs/9.x/events#queued-event-listeners)에도 `tries` 속성과 `retryUntil` 메서드를 지정할 수 있습니다.

<a name="max-exceptions"></a>
#### 최대 예외 횟수 (Max Exceptions)

잡이 재시도는 많이 하지만, 예외 발생 횟수로 실패 조건을 걸고 싶을 때 `maxExceptions` 속성을 지정합니다:

```php
<?php

namespace App\Jobs;

use Illuminate\Support\Facades\Redis;

class ProcessPodcast implements ShouldQueue
{
    /**
     * 최대 재시도 횟수
     *
     * @var int
     */
    public $tries = 25;

    /**
     * 잡 실패 전 허용 최대 미처리 예외 횟수
     *
     * @var int
     */
    public $maxExceptions = 3;

    /**
     * 잡 실행
     *
     * @return void
     */
    public function handle()
    {
        Redis::throttle('key')->allow(10)->every(60)->then(function () {
            // 락 획득, 팟캐스트 처리...
        }, function () {
            // 락 획득 실패...
            return $this->release(10);
        });
    }
}
```

위 예시에서 Redis 락 획득 실패 시 10초 후에 잡 재발송하며 최대 25번 시도하지만, 예외가 3회 이상 발생하면 잡 실패 처리합니다.

<a name="timeout"></a>
#### 타임아웃 (Timeout)

> [!WARNING]
> 잡 타임아웃 지정에는 `pcntl` PHP 확장 모듈 설치가 필요합니다.

예상 잡 처리 시간을 알면 타임아웃 시간을 지정해 작업자가 작업 중 무한정 멈추는 것을 방지할 수 있습니다. 기본값은 60초입니다. 실행 중 잡이 타임아웃을 넘으면 작업자가 오류와 함께 종료되며, 이는 보통 서버의 [프로세스 관리자](/docs/9.x/queues#supervisor-configuration)가 자동으로 다시 시작합니다.

Artisan 명령어 `queue:work` 실행 시 `--timeout` 옵션으로 지정할 수 있습니다:

```shell
php artisan queue:work --timeout=30
```

재시도 횟수 제한과 타임아웃은 목적이 다르지만 함께 사용됩니다.

> [!WARNING]
> `--timeout` 값은 `retry_after`보다 몇 초 이상 짧게 설정해야 합니다. 그래야 응답이 정지한 작업자가 종료되고 잡이 재시도되기 때문입니다. 반대의 경우 잡이 중복 처리될 수 있습니다.

잡 클래스 내부에도 설정 가능하며 CLI 옵션보다 우선합니다:

```php
<?php

namespace App\Jobs;

class ProcessPodcast implements ShouldQueue
{
    /**
     * 타임아웃 초 단위 시간
     *
     * @var int
     */
    public $timeout = 120;
}
```

소켓, 외부 HTTP 요청 등 블로킹 작업은 이 타임아웃을 따르지 못할 수 있으므로, 이런 처리용 라이브러리(API) 내에서 별도 타임아웃 설정을 항상 하는 것이 좋습니다.

<a name="failing-on-timeout"></a>
#### 타임아웃 시 실패 처리

타임아웃 발생 시 잡을 실패 상태로 표시하려면 잡 클래스의 `$failOnTimeout` 속성을 `true`로 설정합니다:

```php
/**
 * 타임아웃 시 잡을 실패로 표시 여부
 *
 * @var bool
 */
public $failOnTimeout = true;
```

<a name="error-handling"></a>
### 에러 처리 (Error Handling)

잡 처리 중 예외가 발생하면 잡은 자동으로 큐에 다시 넣어져 다시 실행됩니다. 재시도 횟수를 넘게 되면 잡은 실패 처리됩니다. 재시도 횟수는 `queue:work` 명령어의 `--tries` 옵션이나 잡 클래스 설정을 따릅니다. 작업자 실행에 관한 더 자세한 내용은 [아래](#running-the-queue-worker)를 참고하세요.

<a name="manually-releasing-a-job"></a>
#### 잡 직접 재발송 (Manually Releasing A Job)

잡을 특정 시간 후에 다시 시도하려면 `release` 메서드를 호출할 수 있습니다:

```php
/**
 * 잡 실행
 *
 * @return void
 */
public function handle()
{
    // ...

    $this->release();
}
```

기본적으로는 즉시 큐에 재입력하지만, 밀리초 단위 숫자를 넘기면 해당 시간 이후에 재처리됩니다:

```php
$this->release(10);
```

<a name="manually-failing-a-job"></a>
#### 잡 직접 실패 처리 (Manually Failing A Job)

가끔 잡을 수동으로 실패 처리하고 싶으면 `fail` 메서드를 호출합니다:

```php
/**
 * 잡 실행
 *
 * @return void
 */
public function handle()
{
    // ...

    $this->fail();
}
```

잡 실패 원인 예외인 `Throwable` 객체나, 문자열 오류 메시지를 인수로 줄 수도 있습니다:

```php
$this->fail($exception);

$this->fail('오류가 발생했습니다.');
```

> [!NOTE]
> 실패한 잡에 관한 자세한 내용은 [실패 잡 문서](#dealing-with-failed-jobs)를 참고하세요.

<a name="job-batching"></a>
## 잡 배칭 (Job Batching)

Laravel 잡 배칭 기능은 잡 집합을 한 번에 실행하고, 완료 후 특정 작업을 수행하게 해줍니다. 시작 전, 배치 정보를 저장할 테이블을 만드는 마이그레이션을 생성해야 합니다. 다음 Artisan 명령어로 생성하세요:

```shell
php artisan queue:batches-table

php artisan migrate
```

<a name="defining-batchable-jobs"></a>
### 배치 가능 잡 정의 (Defining Batchable Jobs)

배치 생성 기능을 쓰려면, 일반 큐 잡을 만든 후 `Illuminate\Bus\Batchable` 트레이트를 잡 클래스에 추가합니다. 이 트레이트는 실행 중인 배치를 불러오는 `batch` 메서드를 제공합니다:

```php
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
     * 잡 실행
     *
     * @return void
     */
    public function handle()
    {
        if ($this->batch()->cancelled()) {
            // 배치가 취소되었는지 확인

            return;
        }

        // CSV 일부를 임포트...
    }
}
```

<a name="dispatching-batches"></a>
### 배치 디스패치 (Dispatching Batches)

배치 잡을 실행하려면 `Bus` 파사드의 `batch` 메서드를 사용합니다. 완료 콜백을 함께 지정할 수도 있으며 `then`, `catch`, `finally` 메서드로 배치 객체(`Illuminate\Bus\Batch`)를 인자로 받는 콜백을 각각 등록합니다.

예를 들어 CSV 파일 행을 여러 구간으로 나누어 각각 처리하는 잡 배치를 디스패치하는 예시는 다음과 같습니다:

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
])->then(function (Batch $batch) {
    // 모든 잡이 성공적으로 완료됨
})->catch(function (Batch $batch, Throwable $e) {
    // 배치 내 첫 잡 실패 발생
})->finally(function (Batch $batch) {
    // 배치 실행 종료
})->dispatch();

return $batch->id;
```

배치 ID는 `$batch->id`로 접근 가능하며, [명령 버스에서 배치 정보 조회](#inspecting-batches) 시 사용합니다.

> [!WARNING]
> 배치 콜백은 큐 실행 시점에 직렬화되어 실행되므로 `$this` 변수를 쓰지 마십시오.

<a name="naming-batches"></a>
#### 배치 이름 지정

Laravel Horizon, Telescope와 같은 도구가 사용자 친화적인 디버깅 정보를 제공하려면 배치에 이름을 붙이는 것이 좋습니다. `name` 메서드를 체인으로 호출해 이름을 지정하세요:

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // ...
})->name('Import CSV')->dispatch();
```

<a name="batch-connection-queue"></a>
#### 배치 연결 및 큐 지정

배치 잡 전체의 연결과 큐는 `onConnection`과 `onQueue` 메서드로 지정합니다. 모든 배치 잡은 동일 연결과 큐에서 실행되어야 합니다:

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // ...
})->onConnection('redis')->onQueue('imports')->dispatch();
```

<a name="chains-within-batches"></a>
#### 배치 내 체인 처리

배치 내에서 [체인 작업](#job-chaining)을 정의하려면 체인 잡들을 배열로 묶으면 됩니다. 예를 들어, 두 잡 체인을 병렬로 실행하고 모두 완료되면 콜백 실행 코드입니다:

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

<a name="adding-jobs-to-batches"></a>
### 배치에 잡 추가 (Adding Jobs To Batches)

배치 내 배치 잡에서 추가 작업을 동적으로 배치에 추가할 수 있습니다. 수천 개 작업을 한꺼번에 웹 요청으로 디스패치하는 데 오래 걸릴 상황에서 초기 로더 잡을 먼저 디스패치 한 뒤, 그 내부에서 추가 잡을 배치에 넣는 패턴입니다:

```php
$batch = Bus::batch([
    new LoadImportBatch,
    new LoadImportBatch,
    new LoadImportBatch,
])->then(function (Batch $batch) {
    // 모든 잡 완료...
})->name('Import Contacts')->dispatch();
```

`LoadImportBatch` 잡 핸들러 내에서 다음과 같이 배치 인스턴스의 `add` 메서드로 추가 잡을 넣을 수 있습니다:

```php
use App\Jobs\ImportContacts;
use Illuminate\Support\Collection;

/**
 * 잡 실행
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

> [!WARNING]
> 배치에 잡을 추가할 수 있는 것은 반드시 동일 배치 내 잡이어야 합니다.

<a name="inspecting-batches"></a>
### 배치 확인하기 (Inspecting Batches)

`Illuminate\Bus\Batch` 인스턴스가 배치 콜백에 전달되며, 다양한 속성과 메서드를 통해 배치를 조작, 상태 확인할 수 있습니다:

```php
// 배치 UUID
$batch->id;

// 배치 이름(있을 경우)
$batch->name;

// 배치에 할당된 잡 총 수
$batch->totalJobs;

// 아직 처리되지 않은 잡 개수
$batch->pendingJobs;

// 실패한 잡 개수
$batch->failedJobs;

// 지금까지 처리한 잡 개수
$batch->processedJobs();

// 배치 진행율(0~100)
$batch->progress();

// 배치가 완료되었는지 여부
$batch->finished();

// 배치 실행 취소
$batch->cancel();

// 배치가 취소되었는지 확인
$batch->cancelled();
```

<a name="returning-batches-from-routes"></a>
#### 라우트에서 배치 반환하기

`Illuminate\Bus\Batch` 인스턴스는 JSON 직렬화가 가능하므로, 라우트 반환 시 배치 진행 여부 및 상태를 쉽게 프론트엔드에 전달할 수 있습니다.

배치를 ID로 조회하려면 `Bus::findBatch` 메서드를 사용하세요:

```php
use Illuminate\Support\Facades\Bus;
use Illuminate\Support\Facades\Route;

Route::get('/batch/{batchId}', function (string $batchId) {
    return Bus::findBatch($batchId);
});
```

<a name="cancelling-batches"></a>
### 배치 취소 (Cancelling Batches)

배치 실행을 취소하려면 `Illuminate\Bus\Batch` 인스턴스의 `cancel` 메서드를 호출합니다:

```php
/**
 * 잡 실행
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

보통 배치 잡은 실행 전에 배치가 취소되었는지 확인합니다. 편의상, `SkipIfBatchCancelled` [미들웨어](#job-middleware)를 할당하면 배치 취소 시 해당 잡 처리 자체를 건너뜁니다:

```php
use Illuminate\Queue\Middleware\SkipIfBatchCancelled;

/**
 * 잡 미들웨어 반환
 *
 * @return array
 */
public function middleware()
{
    return [new SkipIfBatchCancelled];
}
```

<a name="batch-failures"></a>
### 배치 실패 처리 (Batch Failures)

배치 내 잡이 실패하면, 첫 실패 잡에 대해 설정한 `catch` 콜백이 호출됩니다.

<a name="allowing-failures"></a>
#### 실패 허용하기

배치 내 잡 실패 시 기본으로 배치를 "취소" 처리합니다. 이를 비활성화하고 싶으면, 배치 디스패치 시 `allowFailures` 메서드를 호출합니다:

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // ...
})->allowFailures()->dispatch();
```

<a name="retrying-failed-batch-jobs"></a>
#### 실패한 배치 잡 재시도

Laravel은 실패한 배치 잡을 재시도하는 `queue:retry-batch` Artisan 명령어를 제공합니다. 옵션에 배치 UUID를 지정합니다:

```shell
php artisan queue:retry-batch 32dbc76c-4f82-4749-b610-a639fe0099b5
```

<a name="pruning-batches"></a>
### 배치 데이터 정리 (Pruning Batches)

`job_batches` 테이블 레코드가 빠르게 누적됩니다. 이를 방지하려면 [스케줄러](/docs/9.x/scheduling)를 이용해 `queue:prune-batches` Artisan 명령어를 매일 실행하세요:

```php
$schedule->command('queue:prune-batches')->daily();
```

디폴트는 완료된 배치 중 24시간 넘어간 레코드를 삭제합니다. 유지 기간은 `--hours` 옵션으로 제어 가능합니다. 예를 들어 48시간 이전 것만 삭제하려면:

```php
$schedule->command('queue:prune-batches --hours=48')->daily();
```

완료되지 않은 배치(예: 실패하고 재시도 성공하지 않은 큰 배치)도 삭제하려면 `--unfinished` 옵션을 씁니다:

```php
$schedule->command('queue:prune-batches --hours=48 --unfinished=72')->daily();
```

취소된 배치도 삭제하려면 `--cancelled` 옵션을 씁니다:

```php
$schedule->command('queue:prune-batches --hours=48 --cancelled=72')->daily();
```

<a name="queueing-closures"></a>
## 클로저 큐잉 (Queueing Closures)

잡 클래스 대신 간단한 작업을 클로저로 큐에 넣을 수도 있습니다. 이 경우 클로저 코드 내용은 암호화되어 변조를 방지합니다:

```php
$podcast = App\Podcast::find(1);

dispatch(function () use ($podcast) {
    $podcast->publish();
});
```

`catch` 메서드로 클로저 실패 시 실행할 콜백도 지정 가능하며 예외 객체가 전달됩니다:

```php
use Throwable;

dispatch(function () use ($podcast) {
    $podcast->publish();
})->catch(function (Throwable $e) {
    // 잡 실패 처리...
});
```

> [!WARNING]
> 클로저 `catch` 콜백도 큐에서 나중에 실행하므로 `$this`를 쓰지 마세요.

<a name="running-the-queue-worker"></a>
## 큐 작업자 실행 (Running The Queue Worker)

<a name="the-queue-work-command"></a>
### `queue:work` 명령어

Laravel은 큐 작업자(worker)를 시작해 큐에 쌓인 새 잡을 처리하는 Artisan 명령어 `queue:work`를 제공합니다. 이 명령을 실행하면 수동 중지하거나 터미널을 닫을 때까지 계속 실행됩니다:

```shell
php artisan queue:work
```

> [!NOTE]
> `queue:work` 프로세스를 백그라운드에서 항상 유지하려면, [Supervisor](#supervisor-configuration) 같은 프로세스 모니터를 사용하는 것이 좋습니다.

`-v` 옵션을 붙이면 처리한 잡의 ID를 출력합니다:

```shell
php artisan queue:work -v
```

큐 작업자는 지속 실행 프로세스라 코드 변경을 바로 반영하지 않습니다. 따라서 배포 과정에선 작업자를 반드시 재시작해야 합니다([아래 참고](#queue-workers-and-deployment)). 또한 정적 상태는 잡 간 유지되므로 클린업 처리도 필요합니다.

대안으로 `queue:listen` 명령이 있는데, 코드 변경 후 작업자를 재시작할 필요는 없으나, 비효율적입니다:

```shell
php artisan queue:listen
```

<a name="running-multiple-queue-workers"></a>
#### 다중 큐 작업자 실행

여러 작업자를 두어 잡을 병렬 처리하려면, 여러 개 `queue:work` 프로세스를 실행하세요. 로컬에서는 여러 터미널 탭에서 실행하면 되고, 프로덕션에서는 프로세스 관리자 설정을 이용해 실행합니다. Supervisor에서는 `numprocs` 설정으로 이 수를 지정합니다.

<a name="specifying-the-connection-queue"></a>
#### 연결 및 큐 지정

작업자가 사용할 큐 연결을 지정할 수 있습니다. 연결 이름은 `config/queue.php` 내 연결 이름과 일치해야 합니다:

```shell
php artisan queue:work redis
```

기본적으로 `queue:work`는 연결 내 기본 큐의 잡만 처리합니다. 특정 큐만 처리하도록 제한할 수도 있습니다:

```shell
php artisan queue:work redis --queue=emails
```

<a name="processing-a-specified-number-of-jobs"></a>
#### 지정 횟수만큼 잡 처리

`--once` 옵션을 사용하면 작업자가 한 개 잡만 처리하고 종료합니다:

```shell
php artisan queue:work --once
```

`--max-jobs` 옵션은 작업자가 지정한 횟수만큼 잡을 처리하고 종료합니다. 프로세스 관리자와 조합하면 메모리 누수 문제를 완화할 수 있습니다:

```shell
php artisan queue:work --max-jobs=1000
```

<a name="processing-all-queued-jobs-then-exiting"></a>
#### 큐가 빌 때까지 잡 처리 후 종료

`--stop-when-empty` 옵션은 큐가 빌 때까지 잡을 처리한 후 작업자가 종료되도록 합니다. Docker 컨테이너에서 작업 큐 후 컨테이너를 종료할 때 유용합니다:

```shell
php artisan queue:work --stop-when-empty
```

<a name="processing-jobs-for-a-given-number-of-seconds"></a>
#### 지정 시간 동안 잡 처리 후 종료

`--max-time` 옵션은 지정 초 동안 잡을 처리한 후 종료합니다. 프로세스 관리자와 조합하면 메모리 누수를 줄이는 데 도움됩니다:

```shell
# 1시간 동안 처리 후 종료
php artisan queue:work --max-time=3600
```

<a name="worker-sleep-duration"></a>
#### 작업자 대기 시간

잡이 없으면 작업자는 대기 상태로 들어갑니다. `--sleep` 옵션으로 대기 시간을 지정합니다(초 단위). 대기 중은 새 잡을 처리하지 않습니다:

```shell
php artisan queue:work --sleep=3
```

<a name="resource-considerations"></a>
#### 리소스 관리

데몬 큐 작업자는 잡마다 프레임워크를 재부팅하지 않으므로, 각 잡 완료 후 무거운 리소스는 해제하는 것이 좋습니다. 예: GD 이미지 처리 후 `imagedestroy` 호출.

<a name="queue-priorities"></a>
### 큐 우선순위 (Queue Priorities)

큐 처리 우선순위를 지정할 수 있습니다. 예를 들어 `config/queue.php`의 Redis 연결 기본 큐가 `low`일 때, 가끔 `high` 우선순위 큐에 잡을 푸시할 수 있습니다:

```php
dispatch((new Job)->onQueue('high'));
```

`queue:work` 실행 명령어에 다음처럼 큐를 우선순위 순서대로 지정하세요:

```shell
php artisan queue:work --queue=high,low
```

<a name="queue-workers-and-deployment"></a>
### 큐 작업자와 배포 (Queue Workers & Deployment)

큐 작업자가 장기간 실행 프로세스라 코드 변경을 감지하지 못하므로, 배포 때 작업자를 재시작해야 합니다. 작업자를 부드럽게 재시작하려면 `queue:restart` 명령어를 실행하세요:

```shell
php artisan queue:restart
```

이 명령은 작업자에게 현재 잡 완료 후 종료할 것을 알립니다. 작업자는 종료 후 프로세스 관리자가 자동으로 재시작하도록 구성해야 합니다([Supervisor 참고](#supervisor-configuration)).

> [!NOTE]
> 재시작 신호는 [캐시 시스템](/docs/9.x/cache)을 사용하므로, 캐시 드라이버 설정이 정상인지 확인하세요.

<a name="job-expirations-and-timeouts"></a>
### 잡 만료 및 타임아웃 (Job Expirations & Timeouts)

<a name="job-expiration"></a>
#### 잡 만료 시간 (Job Expiration)

`config/queue.php`에서 각 연결 설정에 `retry_after` 값이 있는데, 이는 잡을 처리 중인데 얼마나 오래 기다린 후 재시도하는지 초 단위 시간입니다.

예: `retry_after`가 90초면, 잡이 90초 이상 실행되고 완료나 삭제되지 않으면 다시 큐에 들어갑니다. 대개 작업이 처리되는 최대 예상 시간을 설정합니다.

> [!WARNING]
> Amazon SQS는 `retry_after` 값을 사용하지 않습니다. AWS 콘솔에서 관리하는 [기본 가시성 타임아웃](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/AboutVT.html)을 기반으로 동작합니다.

<a name="worker-timeouts"></a>
#### 작업자 타임아웃

`queue:work` 명령어는 `--timeout` 옵션을 노출하며 기본값은 60초입니다. 타임아웃을 넘으면 작업자가 에러 상태로 종료되고, 프로세스 관리자가 재시작합니다:

```shell
php artisan queue:work --timeout=60
```

`retry_after` 설정과 `--timeout` 옵션은 다르지만 함께 작동되어 잡이 중복 처리되지 않도록 합니다.

> [!WARNING]
> `--timeout` 값을 `retry_after`보다 몇 초 이상 짧게 설정해야 작업 중 정지한 잡을 확실히 종료 후 재시도합니다. 그렇지 않으면 잡이 중복 처리될 수 있습니다.

<a name="supervisor-configuration"></a>
## Supervisor 설정 (Supervisor Configuration)

프로덕션에서는 `queue:work` 프로세스가 죽었을 때 자동으로 다시 시작하도록 프로세스 모니터가 필요합니다. 작업자는 타임아웃 초과, `queue:restart` 호출 등 다양한 이유로 종료될 수 있습니다.

Linux 환경에서 Supervisor는 널리 쓰이며, `/etc/supervisor/conf.d`에 설정 파일을 생성해 실행할 명령과 옵션, 동시 작업자 수 등을 지정합니다.

<a name="installing-supervisor"></a>
#### Supervisor 설치

Supervisor는 Linux용 프로세스 관리자이며 `queue:work` 프로세스를 관리해 자동 재시작합니다. Ubuntu 기준 설치:

```shell
sudo apt-get install supervisor
```

> [!NOTE]
> Supervisor 설정이 부담스럽다면, [Laravel Forge](https://forge.laravel.com)를 이용하면 자동 설치 및 구성도 가능합니다.

<a name="configuring-supervisor"></a>
#### Supervisor 설정

설정 파일 예시 (`laravel-worker.conf`):

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

- `numprocs`는 작업자를 몇 개 실행할지 지정합니다(여기선 8개).
- `command`는 작업자 실행 명령으로 연결 및 옵션을 변경하세요.
- `stopwaitsecs` 값은 가장 긴 작업 시간이 되도록 지정해야 작업이 강제 종료되지 않습니다.

> [!WARNING]
> `stopwaitsecs`가 가장 긴 잡 처리 시간보다 짧으면 작업이 완료 전에 강제 종료될 수 있습니다.

<a name="starting-supervisor"></a>
#### Supervisor 시작

설정 파일 생성 후, Supervisor 설정을 재적용하고 프로세스를 시작합니다:

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start laravel-worker:*
```

Supervisor에 관한 자세한 내용은 [Supervisor 공식 문서](http://supervisord.org/index.html)를 참고하세요.

<a name="dealing-with-failed-jobs"></a>
## 실패한 잡 다루기 (Dealing With Failed Jobs)

가끔 큐 잡이 실패하는 경우가 있습니다. Laravel은 [최대 재시도 횟수](#max-job-attempts-and-timeout) 초과 시 비동기 잡은 `failed_jobs` 테이블에 저장합니다. 동기 처리 잡은 실패 시 바로 예외 처리됩니다.

`failed_jobs` 테이블 생성 마이그레이션은 신규 Laravel에 기본 포함되어 있지만, 그게 없으면 다음 명령어로 생성 및 마이그레이트할 수 있습니다:

```shell
php artisan queue:failed-table

php artisan migrate
```

[큐 작업자](#running-the-queue-worker)를 실행할 때, `--tries` 옵션으로 최대 재시도 횟수를 정할 수 있습니다. 지정하지 않으면 기본적으로 1회 혹은 잡 클래스 내 설정을 따릅니다:

```shell
php artisan queue:work redis --tries=3
```

`--backoff` 옵션으로 예외 발생 시 재시도 전 대기 시간을 초 단위로 지정할 수 있습니다. 기본은 즉시 재시도입니다:

```shell
php artisan queue:work redis --tries=3 --backoff=3
```

잡 내부에서 개별 재시도 대기 시간을 지정하는 방법도 있습니다:

```php
/**
 * 재시도 전 대기할 초
 *
 * @var int
 */
public $backoff = 3;
```

복잡한 로직이나 지연 간격 배열도 `backoff` 메서드로 정의 가능합니다:

```php
/**
 * 재시도 전 대기할 초 계산
 *
 * @return int|array
 */
public function backoff()
{
    return [1, 5, 10];
}
```

<a name="cleaning-up-after-failed-jobs"></a>
### 실패한 잡 정리 (Cleaning Up After Failed Jobs)

잡 실패 시 알림을 보내거나 부분 진행된 작업을 롤백하려면, `failed` 메서드를 잡 클래스에 정의하세요. `Throwable` 인스턴스가 전달됩니다:

```php
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
     * 팟캐스트 인스턴스
     *
     * @var \App\Podcast
     */
    public $podcast;

    /**
     * 새 잡 인스턴스 생성
     *
     * @param  \App\Models\Podcast  $podcast
     * @return void
     */
    public function __construct(Podcast $podcast)
    {
        $this->podcast = $podcast;
    }

    /**
     * 잡 실행
     *
     * @param  \App\Services\AudioProcessor  $processor
     * @return void
     */
    public function handle(AudioProcessor $processor)
    {
        // 업로드된 팟캐스트 처리...
    }

    /**
     * 잡 실패 처리
     *
     * @param  \Throwable  $exception
     * @return void
     */
    public function failed(Throwable $exception)
    {
        // 사용자에게 실패 알림 전송 등...
    }
}
```

> [!WARNING]
> `failed` 호출 시점에는 새로운 잡 인스턴스가 생성되므로 `handle`에서 수정한 속성값은 초기화됩니다.

<a name="retrying-failed-jobs"></a>
### 실패한 잡 재시도 (Retrying Failed Jobs)

`failed_jobs` 테이블에 저장된 실패 잡을 확인하려면 `queue:failed` 명령어를 사용하세요:

```shell
php artisan queue:failed
```

잡 ID로 특정 실패 잡을 재시도:

```shell
php artisan queue:retry ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece
```

여러 ID도 함께 지정 가능:

```shell
php artisan queue:retry ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece 91401d2c-0784-4f43-824c-34f94a33c24d
```

특정 큐 이름으로 실패 잡 전체 재시도:

```shell
php artisan queue:retry --queue=name
```

모든 실패 잡 한 번에 재시도:

```shell
php artisan queue:retry all
```

실패 잡을 삭제하려면 `queue:forget` 명령어를 사용합니다:

```shell
php artisan queue:forget 91401d2c-0784-4f43-824c-34f94a33c24d
```

> [!NOTE]
> Horizon을 사용 중인 경우 `queue:forget` 대신 `horizon:forget`을 사용하세요.

모든 실패 잡 일괄 삭제는 `queue:flush` 명령어를 사용합니다:

```shell
php artisan queue:flush
```

<a name="ignoring-missing-models"></a>
### 모델이 없을 때 무시하기 (Ignoring Missing Models)

잡에 Eloquent 모델을 주입하면 모델은 직렬화 후 재조회됩니다. 모델이 삭제된 상태에서 잡이 처리되면 `ModelNotFoundException`이 발생할 수 있습니다.

이때 잡 클래스 내 `deleteWhenMissingModels` 속성을 `true`로 지정하면, Laravel이 조용히 잡을 버리고 예외 발생을 막아줍니다:

```php
/**
 * 모델이 존재하지 않으면 잡 삭제
 *
 * @var bool
 */
public $deleteWhenMissingModels = true;
```

<a name="pruning-failed-jobs"></a>
### 실패 잡 정리 (Pruning Failed Jobs)

`failed_jobs` 테이블 레코드 정리는 `queue:prune-failed` 명령어로 할 수 있으며 기본은 24시간 이상 된 기록 삭제입니다:

```shell
php artisan queue:prune-failed
```

`--hours` 옵션으로 유지 기간을 조정할 수 있습니다. 예를 들어 48시간 이전 실패 잡 삭제:

```shell
php artisan queue:prune-failed --hours=48
```

<a name="storing-failed-jobs-in-dynamodb"></a>
### DynamoDB에 실패한 잡 저장하기 (Storing Failed Jobs In DynamoDB)

실패한 잡 기록을 관계형 DB 대신 AWS DynamoDB에 저장할 수도 있습니다. 이를 위해 DynamoDB에 테이블 생성이 필요합니다. 테이블은 보통 `failed_jobs` 이름이나 `queue.failed.table` 설정값에 맞게 지정하세요.

테이블 키 구성은 `application` (애플리케이션 이름)과 `uuid` (고유 ID)로, 다중 Laravel 앱이 한 테이블을 공유 가능합니다.

AWS SDK 설치가 필요합니다:

```shell
composer require aws/aws-sdk-php
```

`queue.failed.driver` 설정을 `dynamodb`로, 인증 정보(`key`, `secret`, `region`)는 `.env` 변수 등에서 설정합니다. `database` 설정은 필요 없습니다:

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

실패 잡 저장을 아예 하지 않고 무시하려면 `queue.failed.driver` 설정을 `null`로 하세요. `.env` 변수로 설정 가능합니다:

```ini
QUEUE_FAILED_DRIVER=null
```

<a name="failed-job-events"></a>
### 실패 잡 이벤트 (Failed Job Events)

잡 실패 시 이벤트 리스너를 등록하려면 `Queue` 파사드의 `failing` 메서드를 이용하세요. 예시는 `AppServiceProvider`의 `boot` 메서드 내입니다:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Queue;
use Illuminate\Support\ServiceProvider;
use Illuminate\Queue\Events\JobFailed;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 부트스트랩
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

> [!NOTE]
> Horizon 사용 시 `queue:clear` 대신 `horizon:clear` 명령어를 사용하세요.

기본 연결의 기본 큐에서 모든 잡을 삭제하려면 `queue:clear` Artisan 명령어를 실행합니다:

```shell
php artisan queue:clear
```

특정 연결 및 큐에서 삭제할 수도 있습니다:

```shell
php artisan queue:clear redis --queue=emails
```

> [!WARNING]
> 큐 삭제는 SQS, Redis, 데이터베이스 드라이버만 지원하며, SQS 메시지 삭제는 최대 60초가 걸려 삭제 후 60초 이내 도착 잡도 같이 삭제될 수 있습니다.

<a name="monitoring-your-queues"></a>
## 큐 모니터링 (Monitoring Your Queues)

갑작스런 큐 작업 증가로 대기 시간이 길어질 수 있습니다. Laravel은 큐 잡 개수가 지정 임계치 이상일 때 알림을 받을 수 있도록 지원합니다.

먼저 `queue:monitor` 명령어를 [분 단위 스케줄](/docs/9.x/scheduling)에 추가하고, 모니터링할 큐 이름과 임계값을 지정하십시오:

```shell
php artisan queue:monitor redis:default,redis:deployments --max=100
```

이 명령어만 예약해도 알림이 발생하지 않습니다. 임계치 초과 시 `Illuminate\Queue\Events\QueueBusy` 이벤트가 디스패치되므로, `EventServiceProvider`에서 이벤트 리스너를 등록해 알림을 보내세요:

```php
use App\Notifications\QueueHasLongWaitTime;
use Illuminate\Queue\Events\QueueBusy;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\Facades\Notification;

/**
 * 이벤트 등록
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

`Queue` 파사드에서 `before`, `after` 메서드를 활용해 잡 처리 전후에 콜백을 등록할 수 있습니다. 주로 로그 기록이나 대시보드용 통계 집계에 사용하며, 보통 서비스를 등록하는 프로바이더의 `boot` 메서드 내에 작성합니다:

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
     * 애플리케이션 서비스 부트스트랩
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

`looping` 메서드를 이용하면 작업자가 큐에서 잡을 가져오기 전 콜백을 등록할 수 있습니다. 예를 들어 이전 잡 실패로 열린 DB 트랜잭션을 롤백하는 코드:

```php
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Queue;

Queue::looping(function () {
    while (DB::transactionLevel() > 0) {
        DB::rollBack();
    }
});
```