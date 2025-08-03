# 큐 (Queues)

- [소개](#introduction)
    - [연결(Connections)과 큐(Queues)의 차이](#connections-vs-queues)
    - [드라이버 참고사항 및 전제조건](#driver-prerequisites)
- [잡 생성하기](#creating-jobs)
    - [잡 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [유니크 잡(Unique Jobs)](#unique-jobs)
    - [암호화된 잡(Encrypted Jobs)](#encrypted-jobs)
- [잡 미들웨어](#job-middleware)
    - [속도 제한(Rate Limiting)](#rate-limiting)
    - [잡 중복 방지](#preventing-job-overlaps)
    - [예외 발생 속도 제한(Throttling Exceptions)](#throttling-exceptions)
    - [잡 건너뛰기(Skipping Jobs)](#skipping-jobs)
- [잡 디스패치](#dispatching-jobs)
    - [지연 디스패치](#delayed-dispatching)
    - [동기 디스패치](#synchronous-dispatching)
    - [잡과 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [잡 체이닝(Job Chaining)](#job-chaining)
    - [큐 및 연결 맞춤 설정](#customizing-the-queue-and-connection)
    - [최대 시도 횟수 및 타임아웃 값 지정](#max-job-attempts-and-timeout)
    - [에러 처리](#error-handling)
- [잡 배칭(Job Batching)](#job-batching)
    - [배치 가능한 잡 정의](#defining-batchable-jobs)
    - [배치 디스패치](#dispatching-batches)
    - [체인과 배치](#chains-and-batches)
    - [배치에 잡 추가](#adding-jobs-to-batches)
    - [배치 상태 조회](#inspecting-batches)
    - [배치 취소](#cancelling-batches)
    - [배치 실패 처리](#batch-failures)
    - [배치 정리(Pruning)](#pruning-batches)
    - [DynamoDB에 배치 저장](#storing-batches-in-dynamodb)
- [클로저 큐잉(Queueing Closures)](#queueing-closures)
- [큐 워커 실행](#running-the-queue-worker)
    - [`queue:work` 명령어](#the-queue-work-command)
    - [큐 우선순위(Queue Priorities)](#queue-priorities)
    - [큐 워커 및 배포](#queue-workers-and-deployment)
    - [잡 만료와 타임아웃](#job-expirations-and-timeouts)
- [Supervisor 설정](#supervisor-configuration)
- [실패한 잡 처리](#dealing-with-failed-jobs)
    - [실패한 잡 후처리](#cleaning-up-after-failed-jobs)
    - [실패한 잡 재시도](#retrying-failed-jobs)
    - [누락된 모델 무시](#ignoring-missing-models)
    - [실패 잡 정리](#pruning-failed-jobs)
    - [DynamoDB에 실패 잡 저장](#storing-failed-jobs-in-dynamodb)
    - [실패 잡 저장 비활성화](#disabling-failed-job-storage)
    - [실패 잡 이벤트](#failed-job-events)
- [큐에서 잡 삭제](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [일부 잡만 페이크](#faking-a-subset-of-jobs)
    - [잡 체인 테스트](#testing-job-chains)
    - [잡 배치 테스트](#testing-job-batches)
    - [잡과 큐 상호작용 테스트](#testing-job-queue-interactions)
- [잡 이벤트](#job-events)

<a name="introduction"></a>
## 소개 (Introduction)

웹 애플리케이션을 개발할 때, 업로드된 CSV 파일 파싱 및 저장 같은 작업은 일반적인 웹 요청 처리 중에 너무 오래 걸릴 수 있습니다. 다행히 Laravel은 백그라운드에서 처리될 수 있는 큐잉 작업(queued jobs)을 손쉽게 만들도록 도와줍니다. 시간이 많이 걸리는 작업을 큐로 옮기면 애플리케이션은 빠르게 웹 요청에 응답하여 사용자 경험을 개선할 수 있습니다.

Laravel 큐는 Amazon SQS, Redis, 또는 관계형 데이터베이스 같은 다양한 큐 백엔드에 대해 통합된 큐 API를 제공합니다.

큐 설정은 `config/queue.php` 파일에 저장되며, 이 파일에 기본 제공되는 데이터베이스, Amazon SQS, Redis, Beanstalkd 드라이버뿐만 아니라 즉시 작업을 수행하는 동기 드라이버(로컬 개발용), 그리고 작업을 버리는 null 드라이버의 연결 설정이 포함되어 있습니다.

> [!NOTE]
> Laravel은 이제 Redis 기반 큐를 위한 멋진 대시보드 및 설정 시스템인 Horizon을 제공합니다. 자세한 내용은 [Horizon 문서](/docs/12.x/horizon)를 참고하세요.

<a name="connections-vs-queues"></a>
### 연결(Connections)과 큐(Queues)의 차이 (Connections vs. Queues)

Laravel 큐를 시작하기 전에 "연결"과 "큐"의 차이를 명확히 이해하는 것이 중요합니다. `config/queue.php` 설정 파일 내 `connections` 배열은 Amazon SQS, Beanstalk, Redis 같은 백엔드 큐 서비스에 대한 연결 정보를 담습니다. 이 연결 하나가 여러 개의 "큐"(여러 작업 스택 또는 모음) 가질 수 있습니다.

각 연결 설정에는 기본 큐를 의미하는 `queue` 속성이 있습니다. 만약 작업을 디스패치할 때 명시적으로 큐를 지정하지 않으면, 이 기본 큐로 작업이 들어갑니다:

```php
use App\Jobs\ProcessPodcast;

// 기본 연결의 기본 큐에 작업 디스패치
ProcessPodcast::dispatch();

// 기본 연결의 'emails' 큐에 작업 디스패치
ProcessPodcast::dispatch()->onQueue('emails');
```

보통 하나의 단일 큐만 사용하는 애플리케이션도 많지만, 여러 큐를 이용해 작업 처리 우선순위를 조정하거나 분리하는 것은 매우 유용할 수 있습니다. Laravel의 큐 워커는 처리할 큐를 우선순위에 따라 지정할 수 있기 때문입니다. 예를 들어, `high` 큐에 작업을 넣고 다음과 같이 우선 처리할 수 있습니다:

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버 참고사항 및 전제조건 (Driver Notes and Prerequisites)

<a name="database"></a>
#### 데이터베이스

`database` 큐 드라이버를 사용하려면 작업을 저장할 데이터베이스 테이블이 필요합니다. Laravel 기본 마이그레이션 `0001_01_01_000002_create_jobs_table.php`에 포함되어 있지만, 없는 경우 `make:queue-table` Artisan 명령어로 생성할 수 있습니다:

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면 `config/database.php`에서 Redis 연결을 설정해야 합니다.

> [!WARNING]
> `serializer`와 `compression` Redis 옵션은 `redis` 큐 드라이버에서 지원되지 않습니다.

**Redis 클러스터**

Redis 클러스터를 사용하는 경우, 큐 이름에 반드시 [key hash tag](https://redis.io/docs/reference/cluster-spec/#hash-tags)를 포함해야 합니다. 이는 같은 해시 슬롯에 큐 관련 모든 키를 몰아넣기 위해 필요합니다:

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

**블로킹(Blocking)**

Redis 큐에서 `block_for` 옵션은 작업 대기 시 드라이버가 Redis에서 새 작업이 나올 때까지 몇 초간 대기할지 정합니다. 적절히 조정하면 계속 재시도하는 것보다 효율적입니다. 예를 들어, 5초간 대기하도록 할 수 있습니다:

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
> `block_for`를 `0`으로 설정하면 작업 가능 시까지 무한정 대기하며 `SIGTERM` 같은 신호가 수신되어도 즉시 처리되지 않습니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 전제조건

아래 드라이버들은 다음과 같은 의존성을 Composer를 통해 설치해야 합니다:

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~2.0` 또는 phpredis PHP 확장
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`

<a name="creating-jobs"></a>
## 잡 생성하기 (Creating Jobs)

<a name="generating-job-classes"></a>
### 잡 클래스 생성 (Generating Job Classes)

기본적으로, 큐에 넣을 모든 잡 클래스는 `app/Jobs` 디렉터리에 있습니다. 이 폴더가 없으면 `make:job` Artisan 명령어를 실행할 때 자동 생성됩니다:

```shell
php artisan make:job ProcessPodcast
```

자동생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하여, Laravel에 해당 잡이 비동기로 큐에 들어갈 잡임을 알립니다.

> [!NOTE]
> 잡 스텁은 [stub 퍼블리싱](/docs/12.x/artisan#stub-customization)을 통해 커스터마이징할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조 (Class Structure)

잡 클래스는 일반적으로 매우 단순하며, 큐에서 작업을 처리할 때 호출되는 `handle` 메서드만을 가집니다. 예를 들어, 팟캐스트 발행 서비스를 관리하며 업로드된 팟캐스트 파일을 처리한다고 가정해 보겠습니다:

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

여기서 Eloquent 모델을 직접 생성자에 전달할 수 있습니다. `Queueable` 트레이트 덕분에, Eloquent 모델과 그 관계(relationships)가 자동으로 직렬화 및 역직렬화됩니다.

큐에 넣을 때 모델은 식별자만 직렬화되고, 실제 처리를 할 때 큐 시스템은 데이터베이스에서 해당 모델과 관계들을 다시 조회합니다. 이는 큐 드라이버에 전송되는 페이로드를 크게 줄여줍니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드 의존성 주입

`handle` 메서드는 잡이 큐에서 처리될 때 호출됩니다. 메서드 인수에 타입힌트를 달아 의존성을 주입할 수 있습니다. Laravel 서비스 컨테이너가 자동으로 의존성을 해결해 줍니다.

의존성 주입 방식을 완전히 제어하려면 서비스 컨테이너의 `bindMethod` 메서드를 활용할 수 있습니다. 보통 `App\Providers\AppServiceProvider`의 `boot` 메서드에 작성합니다:

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 이미지와 같은 바이너리 데이터는 큐에 넣기 전에 반드시 `base64_encode` 함수로 인코딩해야 하며, 그렇지 않으면 JSON 직렬화가 제대로 되지 않을 수 있습니다.

<a name="handling-relationships"></a>
#### 큐 내에서의 관계 처리

Eloquent 모델 관계도 함께 직렬화되므로, 큰 관계 데이터가 묶여 큐 직렬화 데이터가 커질 수 있습니다. 또한, 역직렬화 후 관계를 다시 불러올 때 처음 직렬화 당시의 제약 조건이 적용되지 않아 관계 전체가 조회됩니다. 만약 특정 관계의 일부만을 처리하려면, 잡 내에서 관계에 제약을 다시 걸어야 합니다.

또는, 모델을 속성에 할당할 때 `withoutRelations` 메서드를 호출하면 관계를 제외한 모델 인스턴스를 반환합니다:

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

PHP 8 생성자 프로퍼티 프로모션을 사용한다면, `WithoutRelations` 어트리뷰트를 붙여 관계 직렬화를 방지할 수 있습니다:

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

컬렉션이나 배열로 여러 모델을 받는 경우, 관계는 복원되지 않습니다. 이는 대용량 모델 작업 시 리소스 사용을 줄이기 위함입니다.

<a name="unique-jobs"></a>
### 유니크 잡(Unique Jobs)

> [!WARNING]
> 유니크 잡은 [락을 지원하는 캐시 드라이버](/docs/12.x/cache#atomic-locks)가 필요합니다. 현재 memcached, redis, dynamodb, database, file, array 드라이버가 지원합니다. 또한, 유니크 제약 조건은 배치 내 잡에는 적용되지 않습니다.

특정 잡이 큐에 한 번에 하나만 존재하도록 보장하려면 `ShouldBeUnique` 인터페이스를 구현하세요. 추가 메서드를 정의할 필요는 없습니다:

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

위 예시에서 `UpdateSearchIndex` 잡은 유니크이므로, 이미 큐 안에 처리 중인 인스턴스가 있으면 새 잡은 디스패치하지 않습니다.

특정 키로 유니크를 지정하거나, 유니크 유지 시간을 제한하고 싶다면 `uniqueId` 메서드와 `uniqueFor` 속성을 정의할 수 있습니다:

```php
<?php

use App\Models\Product;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    /**
     * 상품 인스턴스
     *
     * @var \App\Product
     */
    public $product;

    /**
     * 고유 락 유지 시간(초)
     *
     * @var int
     */
    public $uniqueFor = 3600;

    /**
     * 고유 ID 반환
     */
    public function uniqueId(): string
    {
        return $this->product->id;
    }
}
```

이렇게 하면 프로덕트 ID별로 유니크하게 처리되어, 동일 상품 ID의 잡 디스패치는 기존 잡이 완료되기 전까지 무시됩니다. 또한 1시간이 지나면 락이 해제되어 다시 디스패치합니다.

> [!WARNING]
> 여러 웹서버나 컨테이너에서 잡을 디스패치하는 경우, 모든 서버가 동일한 중앙 캐시 서버를 사용하도록 해야 Laravel이 유니크 여부를 정확히 판단할 수 있습니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 처리 시작 전까지 유니크 유지하기

기본적으로 유니크 잡은 처리 완료 또는 모든 재시도 시도 실패 후 락이 해제됩니다. 만약 처리 바로 직전에 락을 해제하고 싶다면 `ShouldBeUnique` 대신 `ShouldBeUniqueUntilProcessing` 계약을 구현하세요:

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
#### 유니크 잡 락 (Unique Job Locks)

내부적으로 `ShouldBeUnique` 잡을 디스패치할 때 Laravel은 `uniqueId`를 키로 하는 [락](/docs/12.x/cache#atomic-locks)을 획득하려 합니다. 락 획득 실패 시 잡은 디스패치되지 않습니다. 락은 잡 완료 또는 최대 재시도 실패 시 해제됩니다.

기본적으로 Laravel은 캐시 드라이버로 락을 생성하지만, 락 드라이버를 바꾸고 싶으면 `uniqueVia` 메서드를 정의할 수 있습니다:

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
> 병렬 처리 제한만 필요하면 [WithoutOverlapping](/docs/12.x/queues#preventing-job-overlaps) 미들웨어를 사용하는 것이 적합합니다.

<a name="encrypted-jobs"></a>
### 암호화된 잡 (Encrypted Jobs)

Laravel은 잡 데이터 보안과 무결성을 위해 [암호화](/docs/12.x/encryption)를 지원합니다. `ShouldBeEncrypted` 인터페이스를 클래스에 추가하면, Laravel이 자동으로 잡 데이터를 암호화해 큐에 보냅니다:

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

잡 미들웨어는 큐 작업 실행 전후로 사용자 정의 로직을 감싸 작업 자체 코드의 중복을 줄여줍니다. 예를 들어, Redis 기반 속도 제한 로직을 `handle` 메서드에 직접 넣는 대신 미들웨어로 분리할 수 있습니다.

```php
use Illuminate\Support\Facades\Redis;

/**
 * 잡 처리
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

`handle` 메서드가 이런 로직으로 지저분해지고, 여러 잡에 중복 작성해야 할 경우 미들웨어를 정의하는 편이 낫습니다.

Laravel은 기본 잡 미들웨어 디렉터리를 정해두지 않았으므로 원하는 위치에 둘 수 있습니다. 예를 들어 `app/Jobs/Middleware`에 다음과 같이 작성할 수 있습니다:

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

라우트 미들웨어처럼, 작업과 다음 콜백을 인수로 받으며 콜백을 호출해 처리 흐름을 연결합니다.

미들웨어 클래스는 `make:job-middleware` Artisan 명령어로 생성할 수 있습니다. 생성한 후에는 잡 클래스의 `middleware` 메서드에서 반환해 할당할 수 있습니다. `make:job` 명령으로 생성된 잡에는 `middleware` 메서드가 없으므로 직접 추가해야 합니다:

```php
use App\Jobs\Middleware\RateLimited;

/**
 * 잡에 통과시킬 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited];
}
```

> [!NOTE]
> 잡 미들웨어는 [큐잉된 이벤트 리스너](/docs/12.x/events#queued-event-listeners), [메일](/docs/12.x/mail#queueing-mail), [알림](/docs/12.x/notifications#queueing-notifications)에도 할당할 수 있습니다.

<a name="rate-limiting"></a>
### 속도 제한 (Rate Limiting)

직접 속도 제한 로직을 구현하는 대신, Laravel은 `RateLimited` 미들웨어를 기본 제공합니다. 이는 라우트 속도 제한기와 비슷하게 `RateLimiter` 파사드의 `for` 메서드로 정의합니다.

예를 들어, 일반 유저는 1시간에 한 번 백업 가능하지만, VIP는 제한하지 않는 예를 보겠습니다. 보통 `AppServiceProvider`의 `boot` 메서드에 작성합니다:

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

`perMinute`도 쉽게 쓸 수 있고, `by` 메서드는 주로 고객 단위로 제한을 나누는 데 쓰입니다:

```php
return Limit::perMinute(50)->by($job->user->id);
```

정의한 제한을 잡에 붙이려면 `Illuminate\Queue\Middleware\RateLimited` 미들웨어를 사용합니다. 제한 초과 시 미들웨어가 잡을 큐에 딜레이를 걸어 다시 넣습니다:

```php
use Illuminate\Queue\Middleware\RateLimited;

/**
 * 잡에 붙일 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited('backups')];
}
```

딜레이 재입력해도 재시도 횟수는 증가하니 `tries`와 `maxExceptions`를 적절히 조절하세요. 또는 [retryUntil 메서드](#time-based-attempts)를 이용해 시도기한을 제한할 수도 있습니다.

딜레이 시간을 직접 지정하려면 `releaseAfter` 메서드를 호출합니다:

```php
/**
 * 잡에 붙일 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new RateLimited('backups'))->releaseAfter(60)];
}
```

재시도가 필요 없으면 `dontRelease` 메서드를 사용합니다:

```php
/**
 * 잡에 붙일 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new RateLimited('backups'))->dontRelease()];
}
```

> [!NOTE]
> Redis를 사용하는 경우, Redis 최적화된 `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어를 사용하세요.

<a name="preventing-job-overlaps"></a>
### 잡 중복 방지 (Preventing Job Overlaps)

Laravel은 `Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어를 제공하며, 특정 키를 기준으로 잡이 중복 실행되는 것을 방지합니다. 예를 들어, 사용자 신용 점수 업데이트를 중복하지 않도록 할 수 있습니다:

```php
use Illuminate\Queue\Middleware\WithoutOverlapping;

/**
 * 잡에 붙일 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new WithoutOverlapping($this->user->id)];
}
```

중복 잡은 다시 큐에 넣어 재시도합니다. 재시도 전에 딜레이를 지정하려면 `releaseAfter`를 사용하세요:

```php
/**
 * 잡에 붙일 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->releaseAfter(60)];
}
```

즉시 중복 잡을 삭제하고 재시도를 막으려면 `dontRelease`를 붙입니다:

```php
/**
 * 잡에 붙일 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->dontRelease()];
}
```

`WithoutOverlapping`는 아토믹 락 기능으로 작동합니다. 잡이 예상치 못하게 실패해 락을 해제하지 못할 수 있으니 `expireAfter`로 락 만료도 지정할 수 있습니다:

```php
/**
 * 잡에 붙일 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->expireAfter(180)];
}
```

> [!WARNING]
> `WithoutOverlapping` 미들웨어도 락 지원 캐시 드라이버가 필요합니다.

<a name="sharing-lock-keys"></a>
#### 여러 잡 클래스 간 락 키 공유

기본적으로 `WithoutOverlapping`는 동일 클래스 내 중복만 막습니다. 다른 클래스가 같은 락 키를 써도 서로 중복 방지하지 않으나, `shared` 메서드로 락 키를 공유할 수 있습니다:

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
### 예외 속도 제한 (Throttling Exceptions)

`Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어는 죽어가는 제3자 API 같은 외부 서비스 호출 중 예외 발생 시 재시도 간격을 조절하는 데 유용합니다. 지정한 예외 수 이상 발생하면 설정 시간만큼 재시도를 지연시킵니다.

예를 들어, 외부 API 호출 시 예외가 계속난다고 가정하면 `middleware` 메서드에 다음 미들웨어를 붙이고, `retryUntil`도 정의합니다:

```php
use DateTime;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡에 붙일 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new ThrottlesExceptions(10, 5 * 60)];
}

/**
 * 잡을 더 이상 실행하지 않을 시간 지정
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(30);
}
```

첫 매개변수는 예외 발생 횟수, 두 번째는 지연 시간(초) 입니다. 위 예시는 연속 10회 예외 발생 시 5분 대기 후 재시도하며, 최대 30분 동안만 시도합니다.

예외 한도가 미만이라면 기본적으로 바로 재시도합니다. 지연하려면 `backoff` 메서드를 미들웨어에 붙입니다:

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡에 붙일 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 5 * 60))->backoff(5)];
}
```

내부적으로 Laravel 캐시를 이용하며 잡 클래스 이름을 캐시 키로 씁니다. 키를 바꾸려면 `by` 메서드로 재정의 가능합니다:

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡에 붙일 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->by('key')];
}
```

예외를 속도 제한할 조건을 커스터마이징하려면 `when` 메서드를 사용하고, 조건이 참일 때만 제한됩니다:

```php
use Illuminate\Http\Client\HttpClientException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡에 붙일 미들웨어 반환
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

`when`과 달리 `deleteWhen`은 조건 예외 발생 시 작업을 아예 삭제합니다:

```php
use App\Exceptions\CustomerDeletedException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡에 붙일 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(2, 10 * 60))->deleteWhen(CustomerDeletedException::class)];
}
```

예외 상황을 애플리케이션 예외 핸들러에 보고하려면 `report` 메서드를 사용합니다. 선택적으로 조건부 보고도 가능합니다:

```php
use Illuminate\Http\Client\HttpClientException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡에 붙일 미들웨어 반환
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
> Redis를 쓰면 Redis용 최적화 미들웨어 `ThrottlesExceptionsWithRedis`를 쓸 수 있습니다.

<a name="skipping-jobs"></a>
### 잡 건너뛰기 (Skipping Jobs)

`Skip` 미들웨어는 잡 논리를 변경하지 않고 조건에 따라 잡을 건너뛰거나 삭제할 수 있게 합니다. `Skip::when`은 조건이 참일 때 잡을 삭제하고, `Skip::unless`는 조건이 거짓일 때 잡을 삭제합니다:

```php
use Illuminate\Queue\Middleware\Skip;

/**
 * 잡에 붙일 미들웨어 반환
 */
public function middleware(): array
{
    return [
        Skip::when($someCondition),
    ];
}
```

복잡한 조건은 `Closure`로도 넘길 수 있습니다:

```php
use Illuminate\Queue\Middleware\Skip;

/**
 * 잡에 붙일 미들웨어 반환
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

잡 클래스를 작성한 후, 잡 자체의 `dispatch` 메서드를 호출해 디스패치할 수 있습니다. 인수는 생성자로 전달됩니다:

```php
<?php

namespace App\Http\Controllers;

use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    /**
     * 새 팟캐스트 저장
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

조건부 디스패치는 `dispatchIf`, `dispatchUnless`를 사용합니다:

```php
ProcessPodcast::dispatchIf($accountActive, $podcast);

ProcessPodcast::dispatchUnless($accountSuspended, $podcast);
```

새 Laravel 애플리케이션은 기본 큐 드라이버로 `sync`를 사용하며, 동기적으로 즉시 잡을 실행합니다. 실 배포에서는 `config/queue.php`에서 다른 드라이버를 지정해 백그라운드 큐 처리를 활성화합니다.

<a name="delayed-dispatching"></a>
### 지연 디스패치 (Delayed Dispatching)

작업이 즉시 처리되지 않고 지연되도록 하려면 `delay` 메서드를 체이닝하세요. 예를 들어, 10분 후부터 처리 가능하도록 지연을 줍니다:

```php
<?php

namespace App\Http\Controllers;

use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    /**
     * 새 팟캐스트 저장
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

기본 지연을 우회하여 즉시 디스패치하려면 `withoutDelay` 사용:

```php
ProcessPodcast::dispatch($podcast)->withoutDelay();
```

> [!WARNING]
> Amazon SQS 큐 서비스는 최대 지연 시간이 15분입니다.

<a name="dispatching-after-the-response-is-sent-to-browser"></a>
#### 응답 후 디스패치하기

`dispatchAfterResponse`는 FastCGI 사용 시, HTTP 응답을 사용자에게 보내고 나서 잡을 디스패치합니다. 약 1초 정도 잡에 적합하며, 워커를 따로 실행하지 않아도 됩니다:

```php
use App\Jobs\SendNotification;

SendNotification::dispatchAfterResponse();
```

익명 함수도 `dispatch`에서 `afterResponse`를 체인해 응답 후 실행할 수 있습니다:

```php
use App\Mail\WelcomeMessage;
use Illuminate\Support\Facades\Mail;

dispatch(function () {
    Mail::to('taylor@example.com')->send(new WelcomeMessage);
})->afterResponse();
```

<a name="synchronous-dispatching"></a>
### 동기 디스패치 (Synchronous Dispatching)

즉시 잡을 실행하려면 `dispatchSync` 메서드를 사용합니다. 이 경우 잡은 큐에 들어가지 않고 현재 프로세스에서 바로 실행됩니다:

```php
<?php

namespace App\Http\Controllers;

use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    /**
     * 새 팟캐스트 저장
     */
    public function store(Request $request): RedirectResponse
    {
        $podcast = Podcast::create(/* ... */);

        // 팟캐스트 생성...

        ProcessPodcast::dispatchSync($podcast);

        return redirect('/podcasts');
    }
}
```

<a name="jobs-and-database-transactions"></a>
### 잡과 데이터베이스 트랜잭션 (Jobs & Database Transactions)

트랜잭션 내에서 잡을 디스패치할 때, 워커가 트랜잭션 커밋 전에 잡을 처리할 수 있습니다. 이때 갱신이나 신규 생성한 데이터가 DB에 반영되지 않았을 수 있으니 주의가 필요합니다.

이를 위해 큐 연결 설정에 `after_commit` 옵션을 활성화하세요:

```php
'redis' => [
    'driver' => 'redis',
    // ...
    'after_commit' => true,
],
```

`after_commit`이 `true`면, 열린 트랜잭션이 커밋될 때까지 디스패치를 지연하고, 트랜잭션이 롤백되면 디스패치된 잡을 버립니다. 열린 트랜잭션이 없으면 즉시 실행합니다.

> [!NOTE]
> `after_commit` 옵션 활성화 시, 큐잉된 이벤트 리스너, 메일, 알림, 브로드캐스트 이벤트도 트랜잭션 커밋 후 실행됩니다.

<a name="specifying-commit-dispatch-behavior-inline"></a>
#### 커밋 디스패치 동작을 직접 지정하기

`after_commit` 옵션을 켜지 않아도 특정 잡만 커밋 후 디스패치할 수 있습니다:

```php
use App\Jobs\ProcessPodcast;

ProcessPodcast::dispatch($podcast)->afterCommit();
```

반대로 `after_commit`이 켜져 있으면, 특정 잡을 트랜잭션 커밋 전 바로 디스패치할 수도 있습니다:

```php
ProcessPodcast::dispatch($podcast)->beforeCommit();
```

<a name="job-chaining"></a>
### 잡 체이닝 (Job Chaining)

잡 체이닝은 기본 잡이 성공적으로 실행된 뒤 순차적으로 실행할 작업 시퀀스를 정의할 수 있게 합니다. 중간에 실패하면 나머지 잡은 실행되지 않습니다.

`Bus` 파사드의 `chain` 메서드로 실행합니다:

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

객체 대신 익명 함수도 체인에 포함 가능합니다:

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
> 잡 내 `delete()` 호출로 잡을 삭제해도 체인은 중단되지 않으며, 실패 시에만 이어지는 체인을 멈춥니다.

<a name="chain-connection-queue"></a>
#### 체인 연결과 큐 지정

체인에 사용될 큐 연결 및 큐 이름은 `onConnection`과 `onQueue`로 지정 가능합니다. 잡별로 달리 지정된 경우 그 값을 우선합니다:

```php
Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->onConnection('redis')->onQueue('podcasts')->dispatch();
```

<a name="adding-jobs-to-the-chain"></a>
#### 체인에 잡 추가하기

체인 중 잡 내에서 체인 앞 또는 뒤에 잡을 추가하려면 `prependToChain`과 `appendToChain`을 사용합니다:

```php
/**
 * 잡 처리
 */
public function handle(): void
{
    // ...

    // 현재 체인 앞에 추가: 지금 잡 바로 다음에 처리
    $this->prependToChain(new TranscribePodcast);

    // 현재 체인 끝에 추가: 체인 마지막에 처리
    $this->appendToChain(new TranscribePodcast);
}
```

<a name="chain-failures"></a>
#### 체인 실패 처리

체인 내 잡이 실패 시 호출할 콜백은 `catch` 메서드로 지정하며, 예외 인스턴스를 인자로 받습니다:

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
> 체인 콜백은 나중에 직렬화되어 실행되므로 `$this` 변수는 사용하지 마세요.

<a name="customizing-the-queue-and-connection"></a>
### 큐 및 연결 맞춤 설정 (Customizing the Queue and Connection)

<a name="dispatching-to-a-particular-queue"></a>
#### 특정 큐로 디스패치하기

큐를 나눠 작업 종류별 분류 또는 우선순위를 줄 수 있습니다. 연결 단위가 아닌 단일 연결 내 큐 이름만 지정할 뿐임을 기억하세요. 디스패치 시 `onQueue`를 사용합니다:

```php
ProcessPodcast::dispatch($podcast)->onQueue('processing');
```

또는 잡 생성자에서 `onQueue`를 호출할 수 있습니다:

```php
public function __construct()
{
    $this->onQueue('processing');
}
```

<a name="dispatching-to-a-particular-connection"></a>
#### 특정 연결로 디스패치하기

여러 큐 연결을 사용하는 경우, `onConnection`으로 어느 연결에 넣을지 지정하세요:

```php
ProcessPodcast::dispatch($podcast)->onConnection('sqs');
```

`onConnection`과 `onQueue`를 함께 체인 가능:

```php
ProcessPodcast::dispatch($podcast)
    ->onConnection('sqs')
    ->onQueue('processing');
```

생성자에서 지정할 수도 있습니다:

```php
public function __construct()
{
    $this->onConnection('sqs');
}
```

<a name="max-job-attempts-and-timeout"></a>
### 최대 시도 횟수 / 타임아웃 값 지정 (Specifying Max Job Attempts / Timeout Values)

<a name="max-attempts"></a>
#### 최대 시도 횟수 (Max Attempts)

잡이 오류 발생 시 무한 재시도를 막으려면 최대 시도 횟수를 지정하세요. Artisan `queue:work` 명령에 `--tries` 옵션을 주는 대표적 방법이 있습니다:

```shell
php artisan queue:work --tries=3
```

옵션 없이 실행하면 기본 1회 재시도하거나 잡 클래스의 `$tries` 값을 참조합니다.

잡 클래스 내부에 `$tries`를 정의하면 명령어 옵션보다 우선합니다:

```php
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

동적으로 최대 시도를 정의하려면 `tries` 메서드 구현:

```php
/**
 * 최대 시도 횟수 반환
 */
public function tries(): int
{
    return 5;
}
```

<a name="time-based-attempts"></a>
#### 시간 기반 시도 (Time Based Attempts)

시도 횟수 대신 특정 시각 이후로는 새 시도를 하지 않도록 `retryUntil` 메서드로 지정할 수 있습니다:

```php
use DateTime;

/**
 * 재시도 금지 시각 정의
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(10);
}
```

`retryUntil`과 `tries`가 모두 있으면 `retryUntil`이 우선합니다.

> [!NOTE]
> [큐잉된 이벤트 리스너](/docs/12.x/events#queued-event-listeners)와 [알림](/docs/12.x/notifications#queueing-notifications)에도 `tries`나 `retryUntil`을 지정할 수 있습니다.

<a name="max-exceptions"></a>
#### 최대 예외 횟수 (Max Exceptions)

잡은 여러 번 시도할 수 있으나, 특정 예외 횟수 초과 시 실패하도록 하려면 `$maxExceptions` 속성을 정의하세요:

```php
class ProcessPodcast implements ShouldQueue
{
    public $tries = 25;

    /**
     * 최대 허용 예외 횟수
     *
     * @var int
     */
    public $maxExceptions = 3;

    /**
     * 잡 처리
     */
    public function handle(): void
    {
        Redis::throttle('key')->allow(10)->every(60)->then(function () {
            // 락 획득, 작업 수행...
        }, function () {
            // 락 획득 실패
            return $this->release(10);
        });
    }
}
```

위 예에서는 25회 시도, 예외 3회 초과 시 실패 처리입니다.

<a name="timeout"></a>
#### 타임아웃 (Timeout)

잡이 얼마나 오래 실행할지 예상 가능하면, 타임아웃을 지정할 수 있습니다. 기본값은 60초이며, 초과 시 작업 중인 워커가 종료됩니다. 서버 내 프로세스 관리자에 의해 자동 재시작됩니다.

명령어 옵션으로 `--timeout`을 지정:

```shell
php artisan queue:work --timeout=30
```

잡 클래스 내 `$timeout` 속성으로 설정하면 명령어 옵션보다 우선합니다:

```php
class ProcessPodcast implements ShouldQueue
{
    /**
     * 타임아웃 시간(초)
     *
     * @var int
     */
    public $timeout = 120;
}
```

소켓이나 HTTP 연결 같은 IO 차단 작업은 외부 API에서 시간초과도 적절히 지정해야 합니다.

> [!WARNING]
> 타임아웃 지정은 PCNTL 확장이 필요하고, `timeout` 값은 항상 `retry_after` 설정값보다 작아야 합니다(아래 참고).

<a name="failing-on-timeout"></a>
#### 타임아웃 시 실패 처리 (Failing on Timeout)

타임아웃 발생 시 잡을 실패로 표시하려면 `$failOnTimeout` 속성을 `true`로 설정:

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

잡 처리 중 예외 발생 시 잡은 자동으로 큐에 재입력되어 재시도합니다. 최대 시도 횟수 초과 시 실패로 간주됩니다. 시도 횟수는 `--tries` 옵션 또는 잡 클래스 설정 기준입니다.

<a name="manually-releasing-a-job"></a>
#### 수동으로 잡 재입력하기 (Manually Releasing a Job)

잡을 직접 다시 큐에 넣고 싶다면 `release` 메서드를 호출하세요:

```php
/**
 * 잡 처리
 */
public function handle(): void
{
    // ...

    $this->release();
}
```

인수로 초 또는 시간 객체를 전달해 지연시간을 지정할 수 있습니다:

```php
$this->release(10);

$this->release(now()->addSeconds(10));
```

<a name="manually-failing-a-job"></a>
#### 수동으로 잡 실패 처리 (Manually Failing a Job)

잡을 수동으로 실패 처리하려면 `fail` 메서드 호출:

```php
/**
 * 잡 처리
 */
public function handle(): void
{
    // ...

    $this->fail();
}
```

예외 객체나 문자열 에러 메시지를 인수로 넘길 수도 있습니다:

```php
$this->fail($exception);

$this->fail('Something went wrong.');
```

> [!NOTE]
> 실패 잡 처리에 대해서는 [실패 잡 처리 문서](#dealing-with-failed-jobs)를 참고하세요.

<a name="fail-jobs-on-exceptions"></a>
#### 특정 예외에 대해 잡 실패 처리 (Failing Jobs on Specific Exceptions)

`FailOnException` 잡 미들웨어는 특정 예외 시 즉시 잡을 실패 처리해 재시도를 중단할 수 있습니다. 예외가 전이성면 재시도하며, 지속성 문제면 영구 실패 처리할 때 유용합니다:

```php
<?php

namespace App\Jobs;

use App\Models\User;
use Illuminate\Auth\Access\AuthorizationException;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\Middleware\FailOnException;
use Illuminate\Support\Facades\Http;

class SyncChatHistory implements ShouldQueue
{
    use InteractsWithQueue;

    public $tries = 3;

    /**
     * 새 잡 인스턴스 생성
     */
    public function __construct(
        public User $user,
    ) {}

    /**
     * 잡 처리
     */
    public function handle(): void
    {
        $user->authorize('sync-chat-history');

        $response = Http::throw()->get(
            "https://chat.laravel.test/?user={$user->uuid}"
        );

        // ...
    }

    /**
     * 잡에 할 미들웨어 반환
     */
    public function middleware(): array
    {
        return [
            new FailOnException([AuthorizationException::class])
        ];
    }
}
```

<a name="job-batching"></a>
## 잡 배칭 (Job Batching)

잡 배치는 여러 잡을 한 번에 실행하고, 완료 후 특정 작업을 수행할 수 있는 기능입니다. 시작 전 배치 정보 저장용 테이블 마이그레이션을 생성하세요:

```shell
php artisan make:queue-batches-table

php artisan migrate
```

<a name="defining-batchable-jobs"></a>
### 배치 가능한 잡 정의 (Defining Batchable Jobs)

기존 큐잉 잡과 동일하게 작성하고, `Illuminate\Bus\Batchable` 트레이트를 추가하세요. 이 트레이트의 `batch` 메서드로 현재 배치를 접근할 수 있습니다:

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
     * 잡 처리
     */
    public function handle(): void
    {
        if ($this->batch()->cancelled()) {
            // 배치 취소 여부 체크...

            return;
        }

        // CSV 파일 일부 임포트...
    }
}
```

<a name="dispatching-batches"></a>
### 배치 디스패치 (Dispatching Batches)

`Bus` 파사드의 `batch` 메서드로 배치를 디스패치하며, 완료 콜백을 `then`, `catch`, `finally`로 정의할 수 있습니다. 콜백들은 `Illuminate\Bus\Batch` 인스턴스를 받습니다:

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
    // 배치 생성됨, 잡 미포함 상태
})->progress(function (Batch $batch) {
    // 단일 잡 성공 처리됨
})->then(function (Batch $batch) {
    // 모든 잡 성공
})->catch(function (Batch $batch, Throwable $e) {
    // 첫 실패 잡 감지됨
})->finally(function (Batch $batch) {
    // 배치 완료
})->dispatch();

return $batch->id;
```

배치 ID로 나중에 [배치 상태 조회](#inspecting-batches)가 가능합니다.

> [!WARNING]
> 배치 콜백은 큐에 직렬화되어 실행되므로 `$this` 사용을 피하세요. 배치 잡은 DB 트랜잭션 내 처리되므로 트랜잭션이 암묵적으로 커밋되는 쿼리는 주의하세요.

<a name="naming-batches"></a>
#### 배치 이름 지정 (Naming Batches)

Laravel Horizon, Telescope 같은 도구에서 배치를 더 친숙하게 표시하려면 `name` 메서드로 임의 이름 부여 가능:

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // ...
})->name('Import CSV')->dispatch();
```

<a name="batch-connection-queue"></a>
#### 배치 연결과 큐 지정

배치 잡은 단일 연결과 큐 내에서 실행되어야 하며, `onConnection`과 `onQueue` 메서드로 지정할 수 있습니다:

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // ...
})->onConnection('redis')->onQueue('imports')->dispatch();
```

<a name="chains-and-batches"></a>
### 체인과 배치 (Chains and Batches)

배치 내 체인을 배열로 정의해, 예를 들어 병렬로 두 개 체인을 실행하고 완료 시 콜백을 정의할 수 있습니다:

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

반대로, 체인 내 배치를 넣을 수도 있습니다:

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
### 배치에 잡 추가하기 (Adding Jobs to Batches)

처음부터 수천 개 잡을 디스패치하기 어려우면, 초기 "로더" 잡 배치를 디스패치하고 이 잡 안에서 추가 잡을 배치에 넣을 수 있습니다:

```php
$batch = Bus::batch([
    new LoadImportBatch,
    new LoadImportBatch,
    new LoadImportBatch,
])->then(function (Batch $batch) {
    // ...
})->name('Import Contacts')->dispatch();
```

`LoadImportBatch` 잡 처리 시 `batch` 메서드로 배치에 잡을 추가:

```php
use App\Jobs\ImportContacts;
use Illuminate\Support\Collection;

/**
 * 잡 처리
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
> 배치에 잡 추가는 해당 배치 내부 잡에서만 가능합니다.

<a name="inspecting-batches"></a>
### 배치 상태 조회 (Inspecting Batches)

`Illuminate\Bus\Batch` 객체의 주요 속성과 메서드:

```php
// 배치 UUID
$batch->id;

// 배치 이름(있으면)
$batch->name;

// 할당된 총 잡 수
$batch->totalJobs;

// 아직 처리 안 된 잡 수
$batch->pendingJobs;

// 실패한 잡 수
$batch->failedJobs;

// 처리된 잡 수
$batch->processedJobs();

// 배치 진행률(0~100)
$batch->progress();

// 배치 실행 완료 여부
$batch->finished();

// 배치 실행 취소
$batch->cancel();

// 배치 취소 여부
$batch->cancelled();
```

<a name="returning-batches-from-routes"></a>
#### 라우트에서 배치 반환

`Batch` 인스턴스는 JSON 직렬화 가능하므로 API 엔드포인트에서 직접 반환해 UI에서 진행률 등을 표시할 수 있습니다:

```php
use Illuminate\Support\Facades\Bus;
use Illuminate\Support\Facades\Route;

Route::get('/batch/{batchId}', function (string $batchId) {
    return Bus::findBatch($batchId);
});
```

<a name="cancelling-batches"></a>
### 배치 취소 (Cancelling Batches)

배치를 취소하려면 `cancel` 메서드를 호출합니다:

```php
/**
 * 잡 처리
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

편의상 `SkipIfBatchCancelled` 미들웨어를 잡에 붙여 배치가 취소되면 잡 처리를 스킵할 수도 있습니다:

```php
use Illuminate\Queue\Middleware\SkipIfBatchCancelled;

/**
 * 잡에 붙일 미들웨어 반환
 */
public function middleware(): array
{
    return [new SkipIfBatchCancelled];
}
```

<a name="batch-failures"></a>
### 배치 실패 처리 (Batch Failures)

배치 내 잡이 실패하면, 할당한 `catch` 콜백이 호출됩니다. 최초 실패 잡에만 호출됩니다.

<a name="allowing-failures"></a>
#### 실패 허용 설정

기본 상태에서는 배치 내 잡 실패 시 배치를 자동으로 취소합니다. 원하면 `allowFailures` 호출로 실패 시 배치가 취소되지 않도록 할 수 있습니다:

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // ...
})->allowFailures()->dispatch();
```

<a name="retrying-failed-batch-jobs"></a>
#### 실패한 배치 잡 재시도

`queue:retry-batch` Artisan 명령으로 배치의 실패한 잡을 재시도할 수 있습니다. 배치 UUID를 인수로 전달합니다:

```shell
php artisan queue:retry-batch 32dbc76c-4f82-4749-b610-a639fe0099b5
```

<a name="pruning-batches"></a>
### 배치 정리 (Pruning Batches)

`job_batches` 테이블은 기록이 빠르게 쌓입니다. `queue:prune-batches` 명령을 스케줄해 매일 정리하세요:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches')->daily();
```

기본은 완료된 배치 중 24시간 이상 지난 기록을 삭제합니다. `--hours` 옵션으로 기간 조절:

```php
Schedule::command('queue:prune-batches --hours=48')->daily();
```

성공하지 않은 배치 기록도 삭제 가능:

```php
Schedule::command('queue:prune-batches --hours=48 --unfinished=72')->daily();
```

취소된 배치도 삭제 가능:

```php
Schedule::command('queue:prune-batches --hours=48 --cancelled=72')->daily();
```

<a name="storing-batches-in-dynamodb"></a>
### DynamoDB에 배치 저장 (Storing Batches in DynamoDB)

RDB 대신 Amazon DynamoDB에 배치 메타정보를 저장할 수 있으나, 직접 테이블을 만들어야 합니다.

일반적으로 테이블명은 `job_batches`이며, `queue.batching.table` 설정값에 맞춤 지정 가능합니다.

<a name="dynamodb-batch-table-configuration"></a>
#### DynamoDB 배치 테이블 구성

기본 파티션 키는 문자열 `application`, 정렬 키는 문자열 `id`입니다. 이때 `application` 값은 `app.name` 설정에 맞추어 여러 Laravel 애플리케이션이 한 테이블을 공유해 기록할 수 있습니다.

자동 배치 정리를 위해 `ttl` 속성을 지정할 수도 있습니다.

<a name="dynamodb-configuration"></a>
#### DynamoDB 구성

AWS SDK를 설치해 Laravel이 DynamoDB와 통신하도록 합니다:

```shell
composer require aws/aws-sdk-php
```

`queue.batching.driver`를 `dynamodb`로 설정하고, `batching` 배열에 AWS 인증 정보(`key`, `secret`, `region`)를 정의합니다:

```php
'batching' => [
    'driver' => env('QUEUE_BATCHING_DRIVER', 'dynamodb'),
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'table' => 'job_batches',
],
```

`queue.batching.database` 설정은 필요 없습니다.

<a name="pruning-batches-in-dynamodb"></a>
#### DynamoDB 배치 정리

RDB용 정리 명령은 DynamoDB에 적용되지 않으므로, [DynamoDB TTL 기능](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html)을 사용해 자동으로 만료된 레코드를 삭제합니다.

`ttl_attribute`에 TTL 필드 이름, `ttl`에 만료가 완료된 레코드를 삭제할 경과 시간을 초 단위로 지정하세요:

```php
'batching' => [
    'driver' => env('QUEUE_FAILED_DRIVER', 'dynamodb'),
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'table' => 'job_batches',
    'ttl_attribute' => 'ttl',
    'ttl' => 60 * 60 * 24 * 7, // 7일
],
```

<a name="queueing-closures"></a>
## 클로저 큐잉 (Queueing Closures)

잡 클래스를 큐에 넣는 대신 클로저(익명 함수)도 디스패치할 수 있습니다. 간단히 요청 주기 외 작업이 필요할 때 유용합니다. 이때 클로저 코드는 암호화되어 전송됩니다:

```php
$podcast = App\Podcast::find(1);

dispatch(function () use ($podcast) {
    $podcast->publish();
});
```

대시보드용 이름을 붙이려면 `name` 메서드를 사용합니다:

```php
dispatch(function () {
    // ...
})->name('Publish Podcast');
```

모두 재시도 후 실패 시 실행할 `catch` 클로저도 붙일 수 있습니다:

```php
use Throwable;

dispatch(function () use ($podcast) {
    $podcast->publish();
})->catch(function (Throwable $e) {
    // 잡 실패 처리...
});
```

> [!WARNING]
> `catch` 콜백은 큐에 직렬화되어 실행되므로 `$this` 사용을 피하세요.

<a name="running-the-queue-worker"></a>
## 큐 워커 실행 (Running the Queue Worker)

<a name="the-queue-work-command"></a>
### `queue:work` 명령어

Laravel은 새 작업을 큐에서 처리할 워커 프로세스를 실행하는 `queue:work` Artisan 명령을 제공합니다. 실행 후에는 수동 중지 또는 터미널 종료 전까지 계속 실행됩니다:

```shell
php artisan queue:work
```

> [!NOTE]
> 워커를 백그라운드에서 항상 실행하려면 [Supervisor](#supervisor-configuration) 같은 프로세스 관리자를 사용하세요.

`-v` 옵션을 붙이면 처리한 잡 ID, 연결명, 큐명을 출력합니다:

```shell
php artisan queue:work -v
```

워커는 장기 실행 프로세스로, 시작 시 애플리케이션 상태를 메모리에 보관합니다. 따라서 코드 변경 후 워커가 변경을 인지하지 못하므로, 배포 때는 반드시 [워커 재시작](#queue-workers-and-deployment)을 수행해야 하며, 정적 상태가 초기화되지 않는 점도 유념하세요.

비효율적이지만, 코드를 자동 리로드하려면 `queue:listen` 명령도 있습니다:

```shell
php artisan queue:listen
```

<a name="running-multiple-queue-workers"></a>
#### 여러 워커 실행

동시에 여러 워커를 실행해 병렬 작업 처리하려면 동일 명령을 여러 개 실행하세요. 터미널 여러 탭 또는 프로세스 관리자 설정 시 `numprocs`를 지정합니다.

<a name="specifying-the-connection-queue"></a>
#### 연결 및 큐 지정

처리할 연결 명칭을 `queue:work` 명령에 지정할 수 있습니다:

```shell
php artisan queue:work redis
```

기본적으로는 해당 연결의 기본 큐만 처리하지만, 특정 큐만 다음과 같이 작업 가능:

```shell
php artisan queue:work redis --queue=emails
```

<a name="processing-a-specified-number-of-jobs"></a>
#### 지정된 갯수만 처리

`--once` 옵션은 한 작업만 처리 후 종료:

```shell
php artisan queue:work --once
```

`--max-jobs`는 지정 개수만 처리하고 종료합니다:

```shell
php artisan queue:work --max-jobs=1000
```

주로 Supervisor와 함께 쓰여 메모리 누수 방지에 도움됩니다.

<a name="processing-all-queued-jobs-then-exiting"></a>
#### 큐 비워질 때까지 처리 후 종료

`--stop-when-empty` 옵션은 큐가 빌 때까지 처리 후 우아하게 종료합니다. 도커 컨테이너 내에서 큐 처리를 마친 뒤 종료에 유용합니다:

```shell
php artisan queue:work --stop-when-empty
```

<a name="processing-jobs-for-a-given-number-of-seconds"></a>
#### 지정된 시간 동안만 처리

`--max-time`은 지정 초 동안만 잡을 처리 후 종료합니다:

```shell
# 1시간 동안 처리 후 종료
php artisan queue:work --max-time=3600
```

Supervisor와 함께 자주 사용합니다.

<a name="worker-sleep-duration"></a>
#### 워커 대기 시간

작업이 없으면 워커는 `sleep` 옵션만큼 잠들어 대기합니다. 대기 중에는 작업을 처리하지 않습니다:

```shell
php artisan queue:work --sleep=3
```

<a name="maintenance-mode-queues"></a>
#### 유지보수 모드 중 큐 처리

애플리케이션 유지보수 모드에서는 큐 작업을 처리하지 않습니다.

유지보수 모드 중에도 강제로 처리하려면 `--force` 옵션을 사용하세요:

```shell
php artisan queue:work --force
```

<a name="resource-considerations"></a>
#### 리소스 고려사항

워커는 각 작업 실행 후 프레임워크를 재부팅하지 않습니다. 따라서 잡 완료 후 소모한 자원을 해제해야 합니다. 예를 들어 GD 이미지 메모리는 `imagedestroy`로 해제하세요.

<a name="queue-priorities"></a>
### 큐 우선순위 (Queue Priorities)

우선순위가 다른 큐를 운영하는 경우 있습니다. 예: 기본 `redis` 연결 큐는 `low`지만, `high` 큐에 넣은 잡은 빨리 처리:

```php
dispatch((new Job)->onQueue('high'));
```

워커는 다음과 같이 우선순위 큐명을 쉼표로 구분해 지정 가능:

```shell
php artisan queue:work --queue=high,low
```

`high` 큐를 먼저 처리합니다.

<a name="queue-workers-and-deployment"></a>
### 큐 워커와 배포

워커는 장기 실행 프로세스로 코드 변경을 인지하지 못하므로, 배포 시 워커를 재시작해야 합니다. 다음 명령으로 모든 워커에게 종료 신호를 보냅니다:

```shell
php artisan queue:restart
```

워커가 현재 잡 처리 완료 후 종료해 작업 손실을 막고, Supervisor 같은 프로세스 관리자가 워커를 자동 재시작합니다.

> [!NOTE]
> 재시작 신호는 [캐시](/docs/12.x/cache)에 저장되므로 캐시 드라이버가 적절히 설정되어야 합니다.

<a name="job-expirations-and-timeouts"></a>
### 잡 만료와 타임아웃 (Job Expirations and Timeouts)

<a name="job-expiration"></a>
#### 잡 만료

`config/queue.php` 각 연결에는 `retry_after` 옵션이 있으며, 처리 중인 잡이 해당 초만큼 완료 또는 삭제되지 않으면 재시도됩니다.

예: `retry_after`가 90초면, 90초 안에 처리가 끝나지 않으면 처리 대기 잡으로 돌아갑니다.

> [!WARNING]
> Amazon SQS만 `retry_after`가 없으며, AWS 콘솔의 [기본 가시성 타임아웃]을 따릅니다.

<a name="worker-timeouts"></a>
#### 워커 타임아웃

`queue:work` 명령은 기본 타임아웃 60초의 `--timeout` 옵션을 제공합니다. 이를 초과하면 워커는 오류와 함께 종료되고, 프로세스 관리자가 워커를 재시작합니다:

```shell
php artisan queue:work --timeout=60
```

`retry_after`와 `--timeout`은 다르지만 협력하여 잡 손실 방지와 중복 처리 방지를 돕습니다.

> [!WARNING]
> `--timeout`은 항상 `retry_after`보다 짧아야 하며, 그렇지 않으면 잡이 두 번 처리될 수 있습니다.

<a name="supervisor-configuration"></a>
## Supervisor 설정 (Supervisor Configuration)

배포 환경에서 `queue:work` 프로세스가 멈출 수 있으므로, 프로세스 모니터로 자동 재시작 설정이 필요합니다. Supervisor는 리눅스에서 많이 쓰이며 다음과 같이 구성할 수 있습니다.

<a name="installing-supervisor"></a>
### Supervisor 설치

우분투에 Supervisor 설치:

```shell
sudo apt-get install supervisor
```

> [!NOTE]
> 직접 관리가 어려우면 [Laravel Cloud](https://cloud.laravel.com) 같은 매니지드 플랫폼 활용을 고려하세요.

<a name="configuring-supervisor"></a>
### Supervisor 설정

보통 설정 파일은 `/etc/supervisor/conf.d`에 위치합니다. 예를 들어 `laravel-worker.conf` 파일을 만들고 다음과 같이 작성:

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

`numprocs=8`로 8개 워커를 실행합니다. 실제 환경에 맞게 명령어를 수정하세요.

> [!WARNING]
> `stopwaitsecs`가 가장 긴 잡 실행 시간보다 길어야 정상 종료됩니다.

<a name="starting-supervisor"></a>
### Supervisor 시작

설정 후 다음 명령으로 Supervisor를 재설정하고 워커를 시작:

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start "laravel-worker:*"
```

Supvervisor 사용하는 방법은 [공식 문서](http://supervisord.org/index.html) 참조.

<a name="dealing-with-failed-jobs"></a>
## 실패한 잡 처리 (Dealing With Failed Jobs)

잡이 실패할 수 있습니다. Laravel은 최대 시도 횟수 초과 시 실패 잡으로 기록하는 기능을 제공합니다. 즉시 실행하는 잡은 실패 시 곧바로 예외 처리됩니다.

`failed_jobs` 테이블 생성 마이그레이션이 기본 포함되어 있으나, 없으면 다음 명령으로 만드세요:

```shell
php artisan make:queue-failed-table

php artisan migrate
```

`queue:work` 실행 시 `--tries` 옵션으로 최대 시도 횟수를 지정할 수 있습니다. 미설정 시 기본값 또는 잡 클래스 `$tries`를 따릅니다:

```shell
php artisan queue:work redis --tries=3
```

`--backoff` 옵션으로 예외 재시도 전 지연 시간을 초 단위로 설정할 수 있습니다:

```shell
php artisan queue:work redis --tries=3 --backoff=3
```

잡 클래스 내 `$backoff` 속성으로 작업별 지연을 정의해도 됩니다:

```php
/**
 * 재시도 전 대기 시간(초)
 *
 * @var int
 */
public $backoff = 3;
```

복잡하면 `backoff` 메서드로 동적 계산 가능:

```php
/**
 * 재시도 전 대기 시간 계산
 */
public function backoff(): int
{
    return 3;
}
```

`backoff` 메서드가 배열을 반환하면 지수 백오프 등을 구현 가능:

```php
/**
 * 재시도 전 대기 시간 배열 반환
 *
 * @return array<int, int>
 */
public function backoff(): array
{
    return [1, 5, 10];
}
```

<a name="cleaning-up-after-failed-jobs"></a>
### 실패 잡 후처리 (Cleaning Up After Failed Jobs)

잡 실패 시 사용자 알림 또는 부분 완료된 작업 복원이 필요하면 `failed` 메서드를 잡 클래스에 정의하세요. 실패 원인 예외가 인수로 전달됩니다:

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

    // ...

    /**
     * 잡 처리
     */
    public function handle(AudioProcessor $processor): void
    {
        // 팟캐스트 처리...
    }

    /**
     * 실패 처리
     */
    public function failed(?Throwable $exception): void
    {
        // 실패 알림 전송 등...
    }
}
```

> [!WARNING]
> `failed` 호출 시 잡 인스턴스는 새로 생성되므로 `handle`에서 변경된 프로퍼티 값은 초기화됩니다.

<a name="retrying-failed-jobs"></a>
### 실패 잡 재시도 (Retrying Failed Jobs)

실패 잡 조회:

```shell
php artisan queue:failed
```

잡 ID를 사용해 재시도:

```shell
php artisan queue:retry ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece
```

복수 ID 가능:

```shell
php artisan queue:retry ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece 91401d2c-0784-4f43-824c-34f94a33c24d
```

큐별 재시도:

```shell
php artisan queue:retry --queue=name
```

전체 재시도:

```shell
php artisan queue:retry all
```

실패 잡 삭제:

```shell
php artisan queue:forget 91401d2c-0784-4f43-824c-34f94a33c24d
```

> [!NOTE]
> Horizon 사용 시 `horizon:forget`을 이용하세요.

모든 실패 잡 삭제:

```shell
php artisan queue:flush
```

<a name="ignoring-missing-models"></a>
### 누락된 모델 무시 (Ignoring Missing Models)

잡에 인젝션된 Eloquent 모델이 처리 전에 삭제될 수 있습니다. 이때 `ModelNotFoundException`이 발생할 수 있는데, `deleteWhenMissingModels` 속성을 `true`로 설정하면 예외 대신 잡을 조용히 삭제합니다:

```php
/**
 * 모델 누락 시 잡 삭제 여부
 *
 * @var bool
 */
public $deleteWhenMissingModels = true;
```

<a name="pruning-failed-jobs"></a>
### 실패 잡 정리 (Pruning Failed Jobs)

`queue:prune-failed` 명령으로 `failed_jobs` 테이블 오래된 레코드를 삭제하세요:

```shell
php artisan queue:prune-failed
```

기본은 24시간 이상 된 레코드 삭제이며, `--hours` 변경 가능:

```shell
php artisan queue:prune-failed --hours=48
```

<a name="storing-failed-jobs-in-dynamodb"></a>
### DynamoDB에 실패 잡 저장 (Storing Failed Jobs in DynamoDB)

Amazon DynamoDB에 실패 잡 기록을 저장할 수도 있습니다. 직접 `failed_jobs` 테이블을 만들고, 다음 구조를 갖춰야 합니다:

- 파티션 키: 문자열 `application`
- 정렬 키: 문자열 `uuid`

`application` 값은 `app.name` 설정입니다.

AWS SDK 설치 필요:

```shell
composer require aws/aws-sdk-php
```

`queue.failed.driver`를 `dynamodb`로 설정하고 AWS 인증 정보 추가:

```php
'failed' => [
    'driver' => env('QUEUE_FAILED_DRIVER', 'dynamodb'),
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'table' => 'failed_jobs',
],
```

`queue.failed.database` 설정은 필요 없습니다.

<a name="disabling-failed-job-storage"></a>
### 실패 잡 저장 비활성화 (Disabling Failed Job Storage)

실패 잡 기록을 아예 저장하지 않으려면 `queue.failed.driver`를 `null`로 설정하세요. 보통 환경변수로 지정합니다:

```ini
QUEUE_FAILED_DRIVER=null
```

<a name="failed-job-events"></a>
### 실패 잡 이벤트 (Failed Job Events)

잡 실패 시 실행할 이벤트 리스너를 등록하려면 `Queue` 파사드의 `failing` 메서드를 사용합니다. 예를 들어 `AppServiceProvider` `boot` 메서드 내:

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
## 큐에서 잡 삭제 (Clearing Jobs From Queues)

> [!NOTE]
> Horizon 사용 시 `horizon:clear`를 사용하세요.

기본 연결 기본 큐에서 모든 잡을 삭제하려면 `queue:clear` 명령:

```shell
php artisan queue:clear
```

특정 연결 및 큐 지정도 가능합니다:

```shell
php artisan queue:clear redis --queue=emails
```

> [!WARNING]
> 삭제 명령은 SQS, Redis, 데이터베이스 드라이버만 지원하며, SQS는 메시지 삭제가 최대 60초 걸립니다. 따라서 삭제 후 60초 내 보낸 메시지는 같이 삭제될 수 있습니다.

<a name="monitoring-your-queues"></a>
## 큐 모니터링 (Monitoring Your Queues)

큐 작업 급증 시 작업 대기 시간이 길어질 수 있습니다. Laravel은 지정한 작업 개수 초과 시 알림을 보냅니다.

`queue:monitor` 명령을 분 단위 스케줄러로 실행하고 모니터링할 큐를 지정하세요:

```shell
php artisan queue:monitor redis:default,redis:deployments --max=100
```

실제 알림은 `Illuminate\Queue\Events\QueueBusy` 이벤트가 발생할 때 감지해 처리합니다. `AppServiceProvider`에 이벤트 리스너와 알림 로직을 등록하세요:

```php
use App\Notifications\QueueHasLongWaitTime;
use Illuminate\Queue\Events\QueueBusy;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\Facades\Notification;

/**
 * 애플리케이션 서비스 부트스트랩
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

잡 디스패치 코드 테스트 시 실질적으로 잡을 실행하지 않고, 잡 자체는 별도로 테스트하는 경우가 많습니다.

`Queue` 파사드의 `fake`를 호출하면 큐에 잡 푸시를 차단하며, 이후 푸시 시도를 검증할 수 있습니다:

```php tab=Pest
<?php

use App\Jobs\AnotherJob;
use App\Jobs\FinalJob;
use App\Jobs\ShipOrder;
use Illuminate\Support\Facades\Queue;

test('orders can be shipped', function () {
    Queue::fake();

    // 주문 배송 처리...

    Queue::assertNothingPushed();

    Queue::assertPushedOn('queue-name', ShipOrder::class);

    Queue::assertPushed(ShipOrder::class, 2);

    Queue::assertNotPushed(AnotherJob::class);

    Queue::assertClosurePushed();

    Queue::assertClosureNotPushed();

    Queue::assertCount(3);
});
```

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

        Queue::assertClosureNotPushed();

        Queue::assertCount(3);
    }
}
```

`assertPushed`, `assertNotPushed`, `assertClosurePushed`, `assertClosureNotPushed`는 조건 클로저를 인수로 받아 해당 조건을 만족하는 잡이 푸시됐는지 검증할 수 있습니다:

```php
use Illuminate\Queue\CallQueuedClosure;

Queue::assertPushed(function (ShipOrder $job) use ($order) {
    return $job->order->id === $order->id;
});

Queue::assertClosurePushed(function (CallQueuedClosure $job) {
    return $job->name === 'validate-order';
});
```

<a name="faking-a-subset-of-jobs"></a>
### 일부 잡만 페이크 (Faking a Subset of Jobs)

특정 잡만 페이크하고 다른 잡은 정상 실행하려면, 클래스 이름을 배열로 넘깁니다:

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

`except` 메서드는 지정 잡만 제외하고 모두 페이크합니다:

```php
Queue::fake()->except([
    ShipOrder::class,
]);
```

<a name="testing-job-chains"></a>
### 잡 체인 테스트 (Testing Job Chains)

체인 테스트는 `Bus` 파사드 페이크를 사용하세요. `assertChained`로 체인 배열을 검증:

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

클래스명 배열 대신 인스턴스 배열도 가능합니다. 이 경우 각 잡 인스턴스의 클래스와 프로퍼티를 검사합니다:

```php
Bus::assertChained([
    new ShipOrder,
    new RecordShipment,
    new UpdateInventory,
]);
```

체인 없는 디스패치는 `assertDispatchedWithoutChain`으로 검증:

```php
Bus::assertDispatchedWithoutChain(ShipOrder::class);
```

<a name="testing-chain-modifications"></a>
#### 체인 수정 테스트

체인 중 잡이 `prependToChain`이나 `appendToChain`으로 잡을 추가할 때, 잡 인스턴스의 `assertHasChain`으로 남은 체인을 검증합니다:

```php
$job = new ProcessPodcast;

$job->handle();

$job->assertHasChain([
    new TranscribePodcast,
    new OptimizePodcast,
    new ReleasePodcast,
]);
```

체인이 비어야 한다면 `assertDoesntHaveChain`:

```php
$job->assertDoesntHaveChain();
```

<a name="testing-chained-batches"></a>
#### 체인 내 배치 테스트

체인에 배치가 포함되어 있다면 `Bus::chainedBatch` 정의로 검증:

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

`Bus` 파사드의 `assertBatched`로 배치 디스패치 여부를 검증합니다. 클로저 인수로 `PendingBatch` 인스턴스가 넘어옵니다:

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

배치 개수 검증은 `assertBatchCount`:

```php
Bus::assertBatchCount(3);
```

배치가 없어야 할 때는 `assertNothingBatched`:

```php
Bus::assertNothingBatched();
```

<a name="testing-job-batch-interaction"></a>
#### 잡과 배치 상호작용 테스트

개별 잡에서 배치 작업을 테스트할 때, `withFakeBatch`로 가짜 배치를 설정하고 잡과 배치 인스턴스를 받습니다:

```php
[$job, $batch] = (new ShipOrder)->withFakeBatch();

$job->handle();

$this->assertTrue($batch->cancelled());
$this->assertEmpty($batch->added);
```

<a name="testing-job-queue-interactions"></a>
### 잡과 큐 상호작용 테스트 (Testing Job / Queue Interactions)

잡이 스스로 큐에 재입력, 삭제, 실패 등의 행위를 테스트하려면 `withFakeQueueInteractions`로 인터랙션을 페이크합니다. 그 후 `assertReleased`, `assertDeleted` 등 메서드로 검증:

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

`Queue` 파사드에서 `before`와 `after` 메서드로 잡 처리 전후 콜백을 지정 가능하며, 부트스트랩이나 로깅에 유용합니다. 보통 `AppServiceProvider` `boot` 메서드에 작성합니다:

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

`looping` 메서드로 워커가 작업 수집 전 호출할 콜백을 지정할 수 있습니다. 예를 들어 열린 DB 트랜잭션을 모두 롤백할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Queue;

Queue::looping(function () {
    while (DB::transactionLevel() > 0) {
        DB::rollBack();
    }
});
```