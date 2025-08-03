# 큐 (Queues)

- [소개](#introduction)
    - [커넥션과 큐의 차이](#connections-vs-queues)
    - [드라이버 참고사항 및 사전 조건](#driver-prerequisites)
- [잡 생성하기](#creating-jobs)
    - [잡 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [유니크 잡 (Unique Jobs)](#unique-jobs)
    - [암호화된 잡 (Encrypted Jobs)](#encrypted-jobs)
- [잡 미들웨어 (Job Middleware)](#job-middleware)
    - [레이트 리미팅](#rate-limiting)
    - [잡 중복 방지](#preventing-job-overlaps)
    - [예외 스로틀링](#throttling-exceptions)
- [잡 디스패치 (Dispatching Jobs)](#dispatching-jobs)
    - [지연 디스패치](#delayed-dispatching)
    - [동기식 디스패치](#synchronous-dispatching)
    - [잡과 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [잡 체이닝](#job-chaining)
    - [큐 및 커넥션 커스터마이징](#customizing-the-queue-and-connection)
    - [최대 재시도 횟수 및 타임아웃 지정](#max-job-attempts-and-timeout)
    - [에러 처리](#error-handling)
- [잡 배칭 (Job Batching)](#job-batching)
    - [배치 가능한 잡 정의](#defining-batchable-jobs)
    - [배치 디스패치](#dispatching-batches)
    - [체인과 배치](#chains-and-batches)
    - [배치에 잡 추가하기](#adding-jobs-to-batches)
    - [배치 검사하기](#inspecting-batches)
    - [배치 취소하기](#cancelling-batches)
    - [배치 실패](#batch-failures)
    - [배치 정리 (Pruning)](#pruning-batches)
    - [DynamoDB에 배치 저장하기](#storing-batches-in-dynamodb)
- [클로저 큐잉 (Queueing Closures)](#queueing-closures)
- [큐 워커 실행하기](#running-the-queue-worker)
    - [`queue:work` 명령어](#the-queue-work-command)
    - [큐 우선순위](#queue-priorities)
    - [큐 워커와 배포](#queue-workers-and-deployment)
    - [잡 만료 및 타임아웃](#job-expirations-and-timeouts)
- [Supervisor 설정](#supervisor-configuration)
- [실패한 잡 처리하기](#dealing-with-failed-jobs)
    - [실패한 잡 정리하기](#cleaning-up-after-failed-jobs)
    - [실패한 잡 재시도](#retrying-failed-jobs)
    - [모델이 없는 경우 무시하기](#ignoring-missing-models)
    - [실패한 잡 정리 (Pruning)](#pruning-failed-jobs)
    - [DynamoDB에 실패한 잡 저장](#storing-failed-jobs-in-dynamodb)
    - [실패한 잡 저장 비활성화](#disabling-failed-job-storage)
    - [실패한 잡 이벤트](#failed-job-events)
- [큐에서 잡 비우기](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [일부 잡만 페이크하기](#faking-a-subset-of-jobs)
    - [잡 체인 테스트](#testing-job-chains)
    - [잡 배치 테스트](#testing-job-batches)
- [잡 이벤트](#job-events)

<a name="introduction"></a>
## 소개 (Introduction)

웹 애플리케이션을 개발하다 보면, 업로드된 CSV 파일을 파싱하고 저장하는 것처럼, 일반적인 웹 요청 중에 처리하기에는 너무 오래 걸리는 작업이 있을 수 있습니다. 다행히 Laravel에서는 백그라운드에서 처리할 수 있는 큐잉 작업을 쉽게 생성할 수 있습니다. 시간이 많이 소요되는 작업을 큐로 옮기면, 애플리케이션은 웹 요청에 빠르게 응답할 수 있고, 사용자에게 더 나은 경험을 제공할 수 있습니다.

Laravel 큐는 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 또는 관계형 데이터베이스 같은 다양한 큐 백엔드에 대해 통일된 큐잉 API를 제공합니다.

Laravel의 큐 설정 옵션은 애플리케이션의 `config/queue.php` 파일에 저장되어 있습니다. 이 파일에는 데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 드라이버 등 프레임워크에 기본 포함된 각 큐 드라이버별 커넥션 설정이 있습니다. 또한, 로컬 개발용으로 즉시 잡을 실행하는 동기식 드라이버도 포함되어 있습니다. `null` 큐 드라이버 역시 포함되어 있는데, 이 드라이버는 큐에 넣은 작업을 버리는 역할을 합니다.

> [!NOTE]  
> Laravel은 Redis 기반 큐를 위한 훌륭한 대시보드 및 설정 시스템인 Horizon도 제공합니다. 자세한 내용은 [Horizon 문서](/docs/10.x/horizon)를 참고하십시오.

<a name="connections-vs-queues"></a>
### 커넥션과 큐의 차이 (Connections vs. Queues)

Laravel 큐를 시작하기 전에, `config/queue.php` 설정 파일의 `connections` 배열에 정의된 "커넥션"과 "큐" 간의 차이를 이해하는 것이 중요합니다. 이 `connections` 옵션은 Amazon SQS, Beanstalk, Redis 등 백엔드 큐 서비스에 대한 커넥션을 정의합니다. 그러나 각 큐 커넥션은 여러 개의 "큐"를 가질 수 있는데, 이는 각기 다른 작업 스택이나 묶음으로 생각하면 됩니다.

`queue` 설정 파일의 각 커넥션 예시에는 `queue` 속성이 포함되어 있으며, 이는 해당 커넥션에서 작업이 디스패치될 때 기본적으로 사용되는 큐 이름입니다. 즉, 작업을 명시적으로 어느 큐에 보낼지 지정하지 않으면, 해당 커넥션 설정의 `queue` 속성에 정의된 큐로 작업이 들어갑니다.

```php
use App\Jobs\ProcessPodcast;

// 기본 커넥션의 기본 큐에 작업 디스패치
ProcessPodcast::dispatch();

// 기본 커넥션의 "emails" 큐에 작업 디스패치
ProcessPodcast::dispatch()->onQueue('emails');
```

일부 애플리케이션은 여러 큐를 사용하지 않고 단일한 큐만 사용하는 경우가 많지만, 여러 큐에 작업을 밀어넣는 것이 작업 처리 우선순위나 구분이 필요한 애플리케이션에서는 매우 유용합니다. Laravel 큐 워커는 어떤 큐를 우선 처리할지 순서를 지정할 수 있기 때문입니다. 예를 들어, `high` 큐에 작업을 밀어넣고, 그 큐를 우선 처리하도록 워커를 실행할 수 있습니다:

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버 참고사항 및 사전 조건 (Driver Notes and Prerequisites)

<a name="database"></a>
#### 데이터베이스 (Database)

`database` 큐 드라이버를 사용하려면 작업을 저장할 데이터베이스 테이블이 필요합니다. 이 테이블을 생성하는 마이그레이션은 `queue:table` Artisan 명령어로 생성할 수 있습니다. 마이그레이션 생성 후에는 `migrate` 명령어를 사용하여 데이터베이스를 마이그레이션합니다:

```shell
php artisan queue:table

php artisan migrate
```

마지막으로 `.env` 파일에서 `QUEUE_CONNECTION` 환경변수를 `database`로 설정하여 애플리케이션이 데이터베이스 드라이버를 사용하도록 지정해야 합니다:

```
QUEUE_CONNECTION=database
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면 `config/database.php` 설정 파일에 Redis 데이터베이스 커넥션을 구성해야 합니다.

> [!WARNING]  
> `serializer` 및 `compression` Redis 옵션은 `redis` 큐 드라이버에서 지원되지 않습니다.

**Redis 클러스터**

Redis 클러스터를 사용하는 경우, 큐 이름에 [키 해시 태그](https://redis.io/docs/reference/cluster-spec/#hash-tags)를 반드시 포함해야 합니다. 이는 해당 큐에 관한 모든 Redis 키가 동일 해시 슬롯에 위치하도록 하기 위함입니다:

```php
'redis' => [
    'driver' => 'redis',
    'connection' => 'default',
    'queue' => '{default}',
    'retry_after' => 90,
],
```

**블로킹**

Redis 큐에서 `block_for` 옵션을 사용해 작업이 준비될 때까지 드라이버가 대기할 최대 시간을 초 단위로 지정할 수 있습니다. 이 값을 적절히 조절하면 계속해서 Redis를 폴링하는 것보다 효율적입니다. 예를 들어, `5`초 동안 대기하도록 설정할 수 있습니다:

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
> `block_for`를 `0`으로 설정하면 큐 워커가 작업이 들어올 때까지 무한정 블로킹되어, `SIGTERM` 같은 신호를 처리하지 못할 수 있습니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 사전 조건

다음 큐 드라이버를 사용하려면 별도의 의존성을 설치해야 하며, Composer 패키지 매니저로 설치할 수 있습니다:

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~4.0`
- Redis: `predis/predis ~1.0` 또는 phpredis PHP 확장

<a name="creating-jobs"></a>
## 잡 생성하기 (Creating Jobs)

<a name="generating-job-classes"></a>
### 잡 클래스 생성 (Generating Job Classes)

기본적으로 애플리케이션의 큐에 들어가는 모든 잡은 `app/Jobs` 디렉터리에 저장됩니다. `app/Jobs` 디렉터리가 없다면, `make:job` Artisan 명령어 실행 시 자동으로 디렉터리가 생성됩니다:

```shell
php artisan make:job ProcessPodcast
```

생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하여, Laravel에 이 잡이 비동기적으로 큐에 들어갈 잡임을 알립니다.

> [!NOTE]  
> 잡 스텁은 [stub publishing](/docs/10.x/artisan#stub-customization)을 통해 커스터마이징할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조 (Class Structure)

잡 클래스는 매우 간단하며, 보통 큐에서 처리될 때 호출되는 `handle` 메서드만 포함합니다. 예를 들어, 팟캐스트 서비스를 운영하면서 업로드된 팟캐스트 파일을 출판 전 처리해야 하는 예제를 살펴보겠습니다:

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
     * 새로운 잡 인스턴스 생성
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

이 예제에서 `SerializesModels` 트레이트 덕분에 Eloquent 모델과 로드된 연관관계가 잡이 처리될 때 적절하게 직렬화 및 역직렬화됩니다. 큐에 넣을 때는 모델의 식별자만 직렬화되고, 실제 `handle` 처리 시 데이터베이스에서 완전한 모델과 관계를 다시 불러옵니다. 덕분에 큐에 보내는 페이로드 크기를 줄일 수 있습니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드의 의존성 주입

잡이 처리될 때 `handle` 메서드를 호출합니다. 이 메서드는 메서드 인자에 타입힌트된 의존성도 Laravel 서비스 컨테이너를 통해 자동으로 주입받을 수 있습니다.

의존성 주입 방식을 직접 제어하고 싶다면, 컨테이너의 `bindMethod` 메서드를 사용할 수 있습니다. 보통은 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 다음과 같이 호출합니다:

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]  
> 이미지 데이터 같은 바이너리 데이터는 직렬화 과정에서 문제가 발생할 수 있으므로, 큐에 넣기 전에 반드시 `base64_encode` 함수를 사용해 인코딩해야 합니다.

<a name="handling-relationships"></a>
#### 큐에 저장된 관계 (Queued Relationships)

Eloquent 모델의 로드된 관계들도 직렬화되어 큐에 저장됩니다. 이로 인해 직렬화된 잡의 데이터 크기가 커질 수 있으며, 역직렬화시 관계가 데이터베이스에서 통째로 다시 로드됩니다. 트랜잭션 직전에 관계 필터를 걸었다 하더라도, 역직렬화 시에는 필터가 적용되지 않으므로, 특정 관계의 일부만 사용하고 싶으면 잡 내에서 관계에 대한 제약조건을 다시 지정해야 합니다.

또는 직렬화 과정에서 관계가 포함되지 않게 하려면, 모델을 프로퍼티에 할당할 때 `withoutRelations` 메서드를 호출할 수도 있습니다:

```php
/**
 * 새로운 잡 인스턴스 생성
 */
public function __construct(Podcast $podcast)
{
    $this->podcast = $podcast->withoutRelations();
}
```

PHP 생성자 프로퍼티 승격을 쓰면서 관계 직렬화를 제외하려면, `WithoutRelations` 속성을 이용할 수 있습니다:

```php
use Illuminate\Queue\Attributes\WithoutRelations;

/**
 * 새로운 잡 인스턴스 생성
 */
public function __construct(
    #[WithoutRelations]
    public Podcast $podcast
) {
}
```

컬렉션 또는 배열 형태로 Eloquent 모델이 넘어오는 경우, 관계는 역직렬화 후 복원되지 않습니다. 이는 많은 모델을 다루는 잡에서 과도한 리소스 사용을 방지하기 위함입니다.

<a name="unique-jobs"></a>
### 유니크 잡 (Unique Jobs)

> [!WARNING]  
> 유니크 잡 기능은 [락을 지원하는 캐시 드라이버](/docs/10.x/cache#atomic-locks)가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버는 원자적 락을 지원합니다. 단, 배치 내 잡에는 유니크 잡 제약이 적용되지 않습니다.

특정 잡의 인스턴스가 큐에 하나만 존재하도록 제한하고 싶다면, 잡 클래스에 `ShouldBeUnique` 인터페이스를 구현하세요. 추가 메서드 구현은 필요 없습니다:

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    ...
}
```

이 예에서 `UpdateSearchIndex` 잡은 유니크 하며, 동일 잡의 인스턴스가 기존 큐에 존재하면 새 잡은 큐에 추가되지 않습니다.

특정 유니크 키 또는 유니크 상태 유지 시간(타임아웃)을 정의하려면, `uniqueId` 메서드와 `uniqueFor` 속성을 선언할 수 있습니다:

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
     * 유니크 락이 유지될 초 단위 시간
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

이 예제는 상품 ID를 기준으로 유니크하므로, 동일 상품 ID의 잡은 기존 잡이 끝나기 전까지 무시됩니다. 타임아웃(예: 1시간) 이후에는 유니크 락이 해제되어 다시 잡을 보낼 수 있습니다.

> [!WARNING]  
> 애플리케이션이 여러 웹 서버 또는 컨테이너에서 잡을 디스패치하는 경우, 모든 서버가 동일한 중앙 캐시 서버와 통신해야 올바른 유니크 판단이 가능합니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 처리 시작 전까지 유니크 유지하기

기본적으로 유니크 잡 락은 잡이 완료되거나 재시도 횟수를 초과해 실패할 때 해제됩니다. 하지만, 잡이 처리되기 직전에 락을 해제하고 싶다면, `ShouldBeUnique` 대신 `ShouldBeUniqueUntilProcessing` 인터페이스를 구현해야 합니다:

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

내부적으로 `ShouldBeUnique` 잡이 디스패치될 때 Laravel은 `uniqueId` 키로 [락](/docs/10.x/cache#atomic-locks) 획득을 시도합니다. 락을 획득하지 못하면 잡이 큐에 추가되지 않습니다. 락은 잡 실행이 완료되거나 재시도 한도를 넘겨 실패 시 해제됩니다.

기본적으로 Laravel은 기본 캐시 드라이버를 통해 락을 획득하지만, 다른 드라이버를 사용하려면 `uniqueVia` 메서드를 정의할 수 있습니다:

```php
use Illuminate\Contracts\Cache\Repository;
use Illuminate\Support\Facades\Cache;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    ...

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
> 단순히 동일 잡의 동시 실행만 제한하려면 [`WithoutOverlapping`](/docs/10.x/queues#preventing-job-overlaps) 잡 미들웨어를 사용하는 것이 좋습니다.

<a name="encrypted-jobs"></a>
### 암호화된 잡 (Encrypted Jobs)

Laravel은 잡 데이터의 비밀성과 무결성을 보장하기 위해 [암호화](/docs/10.x/encryption)를 지원합니다. 이를 적용하려면 잡 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하십시오. 그럼 Laravel은 잡을 큐에 푸시하기 전에 자동으로 암호화합니다:

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

잡 미들웨어를 사용하면 큐 잡 실행을 감싸는 커스텀 로직을 적용하여 잡 클래스 내 중복 코드를 줄일 수 있습니다. 예를 들어, 아래 `handle` 메서드는 Laravel의 Redis 레이트 리미팅 기능을 이용해 5초당 하나의 잡만 처리하도록 합니다:

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

이 방식은 유효하지만, 잡 핸들러가 복잡해지고 레이트 리미팅 로직이 중복됩니다.

대신, 레이트 리미팅을 처리하는 잡 미들웨어를 정의할 수 있습니다. Laravel에는 기본 위치가 없어 애플리케이션 어디서든 넣을 수 있으며, 여기서는 `app/Jobs/Middleware` 디렉터리에 둡니다:

```php
<?php

namespace App\Jobs\Middleware;

use Closure;
use Illuminate\Support\Facades\Redis;

class RateLimited
{
    /**
     * 큐에 잡을 처리
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

잡 미들웨어는 [라우트 미들웨어](/docs/10.x/middleware)와 비슷하게, 처리 중인 잡과 다음 콜백을 받는 구조입니다.

만들어진 미들웨어는 잡 클래스 내 `middleware` 메서드에서 반환하여 할당할 수 있는데, 기본 `make:job` 명령어로 생성된 클래스에는 없으므로 직접 추가해야 합니다:

```php
use App\Jobs\Middleware\RateLimited;

/**
 * 잡이 통과해야 하는 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited];
}
```

> [!NOTE]  
> 잡 미들웨어는 큐에 들어가는 이벤트 리스너, 메일, 알림에도 할당할 수 있습니다.

<a name="rate-limiting"></a>
### 레이트 리미팅 (Rate Limiting)

앞서 직접 작성한 레이트 리미팅 미들웨어 외에도, Laravel은 레이트 리미팅 미들웨어를 기본 제공합니다. [라우트 레이트 리미터](/docs/10.x/routing#defining-rate-limiters)와 유사하게, `RateLimiter` 패싯의 `for` 메서드로 정의합니다.

예를 들어, 프리미엄 고객은 제한 없이 백업할 수 있고, 일반 고객은 한 시간당 한 번만 백업 가능하도록 하는 코드는 다음과 같습니다. `AppServiceProvider`의 `boot` 메서드에 정의합니다:

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

시간 단위 이외에도 `perMinute` 등으로 분 단위 제한도 쉽게 정의할 수 있으며, `by` 메서드에는 어떤 값도 넣을 수 있지만 보통 고객별 세그먼트를 위해 사용자 ID 등을 지정합니다:

```php
return Limit::perMinute(50)->by($job->user->id);
```

정의한 레이트 리미터는 `Illuminate\Queue\Middleware\RateLimited` 미들웨어로 잡에 붙입니다. 레이트 제한 초과 시, 이 미들웨어는 잡을 큐에 적절한 딜레이 후 다시 반환합니다:

```php
use Illuminate\Queue\Middleware\RateLimited;

/**
 * 잡이 통과할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited('backups')];
}
```

레이트 제한으로 다시 큐에 들어간 잡도 `attempts` 카운트가 증가하므로, 잡 클래스 내 `tries`나 `maxExceptions` 값을 적절히 조절하거나 [`retryUntil` 메서드](#time-based-attempts)를 이용해 작업 제한 시간을 지정할 수도 있습니다.

재시도 시 잡을 다시 큐에 보내지 않고 즉시 실패 처리하고 싶으면 `dontRelease` 메서드를 사용하세요:

```php
/**
 * 잡 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new RateLimited('backups'))->dontRelease()];
}
```

> [!NOTE]  
> Redis를 사용할 경우, Redis에 최적화된 `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어를 사용하는 것이 효율적입니다.

<a name="preventing-job-overlaps"></a>
### 잡 중복 방지 (Preventing Job Overlaps)

Laravel은 `Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어를 제공하며, 임의 키로 잡 중복 실행을 방지할 수 있습니다. 예를 들어 동일 사용자 ID에 대해 신용 점수 업데이트 잡 중복 실행을 막고 싶을 때 다음과 같이 합니다:

```php
use Illuminate\Queue\Middleware\WithoutOverlapping;

/**
 * 잡 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new WithoutOverlapping($this->user->id)];
}
```

중복된 잡은 큐에 다시 반환되며, 재시도 대기 시간을 초 단위로 지정할 수도 있습니다:

```php
/**
 * 잡 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->releaseAfter(60)];
}
```

중복 잡을 즉시 삭제하고 재시도하지 않으려면 `dontRelease` 메서드를 사용하세요:

```php
/**
 * 잡 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->dontRelease()];
}
```

`WithoutOverlapping` 미들웨어는 Laravel의 원자적 락 기능을 활용합니다. 잡이 실패하거나 타임아웃 등 예상치 못한 상황에서 락이 해제되지 않을 수 있으므로, 락 만료 시간을 명시적으로 지정하는 `expireAfter` 메서드를 제공합니다. 예:

```php
/**
 * 잡 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->expireAfter(180)];
}
```

> [!WARNING]  
> `WithoutOverlapping` 미들웨어는 [락을 지원하는 캐시 드라이버](/docs/10.x/cache#atomic-locks)가 필요합니다.

<a name="sharing-lock-keys"></a>
#### 잡 클래스 간 락 키 공유

기본적으로 `WithoutOverlapping` 미들웨어는 같은 클래스끼리만 중복 처리를 방지합니다. 다른 클래스가 같은 락 키를 사용해도 중복 방지는 되지 않습니다. 키를 여러 잡 클래스에서 공유하고 싶다면 `shared` 메서드를 사용하세요:

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
### 예외 스로틀링 (Throttling Exceptions)

`Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어는 잡이 지정된 횟수만큼 예외를 발생시키면 지정된 시간동안 모든 재시도를 지연시킵니다. 서드파티 API와 상호작용하는 불안정한 잡에 유용합니다.

예를 들어, 서드파티 API 호출 중에 예외가 자꾸 발생하는 잡을 제한하려면 다음처럼 미들웨어를 잡에 붙입니다. 보통 [시간 기반 재시도](/docs/10.x/queues#time-based-attempts)와 함께 사용합니다:

```php
use DateTime;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new ThrottlesExceptions(10, 5)];
}

/**
 * 잡 재시도 종료 시점 반환
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(5);
}
```

첫 번째 인자는 예외 횟수 제한, 두 번째 인자는 제한 후 재시도까지 대기 시간(분)입니다. 이 예에선 5분 동안 예외가 10번 발생하면 이후 5분간 잡 재시도 실행을 지연합니다.

예외 제한에 도달하지 않은 예외 발생 시 잡은 즉시 재시도되지만, 재시도 전 얼마나 딜레이할지 `backoff` 메서드로 지정할 수도 있습니다:

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 5))->backoff(5)];
}
```

내부적으로 이 미들웨어는 Laravel 캐시를 사용하며, 기본적으로 잡 클래스명이 키로 쓰입니다. 키를 오버라이드하려면 `by` 메서드를 이용하세요. 다수 잡이 같은 서드파티 API를 호출하는 경우키를 공유할 때 유용합니다:

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10))->by('key')];
}
```

> [!NOTE]  
> Redis를 사용하는 경우, Redis 최적화된 `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어를 사용할 수 있습니다.

<a name="dispatching-jobs"></a>
## 잡 디스패치 (Dispatching Jobs)

잡 클래스를 작성한 후, 해당 클래스에서 `dispatch` 메서드를 호출하여 큐에 잡을 넣을 수 있습니다. `dispatch` 메서드에 전달하는 인수는 잡 생성자의 인자로 전달됩니다:

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
     * 새로운 팟캐스트 저장
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

조건에 따라 잡을 디스패치하려면 `dispatchIf`와 `dispatchUnless` 메서드를 사용하세요:

```php
ProcessPodcast::dispatchIf($accountActive, $podcast);

ProcessPodcast::dispatchUnless($accountSuspended, $podcast);
```

새로운 Laravel 앱의 기본 큐 드라이버는 `sync`입니다. 이는 현재 요청의 포그라운드에서 즉시 잡을 실행하므로 로컬 개발 시 편리합니다. 백그라운드에서 누적처리하려면 `config/queue.php` 에서 다른 큐 드라이버를 설정하세요.

<a name="delayed-dispatching"></a>
### 지연 디스패치 (Delayed Dispatching)

잡을 큐에 넣되 즉시 처리되지 않게 10분 후부터 처리하도록 지연을 설정할 수 있습니다:

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
     * 팟캐스트 저장
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

> [!WARNING]  
> Amazon SQS 큐 서비스는 지연 최대 시간이 15분임을 주의하세요.

<a name="dispatching-after-the-response-is-sent-to-browser"></a>
#### HTTP 응답 후 디스패치

`dispatchAfterResponse` 메서드는 웹 서버가 FastCGI를 쓰는 경우, HTTP 응답을 사용자 브라우저에 전송한 뒤 잡을 디스패치합니다. 사용자는 곧바로 앱을 사용할 수 있지만 잡은 현재 HTTP 요청 중에 처리되므로 빠른 잡(예: 이메일 전송)만 추천합니다. 이 방식은 별도의 큐 워커 없이 동작합니다:

```php
use App\Jobs\SendNotification;

SendNotification::dispatchAfterResponse();
```

또한, 클로저를 `dispatch` 한 뒤 `afterResponse`를 체인하여 사용 가능합니다:

```php
use App\Mail\WelcomeMessage;
use Illuminate\Support\Facades\Mail;

dispatch(function () {
    Mail::to('taylor@example.com')->send(new WelcomeMessage);
})->afterResponse();
```

<a name="synchronous-dispatching"></a>
### 동기식 디스패치 (Synchronous Dispatching)

즉시(동기적으로) 잡을 실행하려면 `dispatchSync` 메서드를 사용하세요. 이 경우, 잡은 큐에 들어가지 않고 현재 프로세스에서 즉시 실행됩니다:

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
     * 팟캐스트 저장
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

트랜잭션 내에서 잡을 디스패치하는 것은 가능하지만, 주의가 필요합니다. 워커가 작업을 처리할 때 부모 트랜잭션이 아직 커밋되지 않았다면, 트랜잭션 내 변경사항이 DB에 반영되지 않은 상태일 수 있으며, 새로 생성된 레코드가 존재하지 않을 수도 있기 때문입니다.

이를 해결하기 위해서는 해당 큐 커넥션 설정에서 `after_commit` 옵션을 `true`로 지정하세요:

```php
'redis' => [
    'driver' => 'redis',
    // ...
    'after_commit' => true,
],
```

`after_commit`이 `true`면 트랜잭션 내에서 잡을 디스패치해도, Laravel은 열린 모든 트랜잭션이 커밋된 뒤에 잡을 실제 디스패치합니다. 만약 트랜잭션이 예외로 롤백되면, 그 시점에 디스패치된 잡은 폐기됩니다.

> [!NOTE]  
> `after_commit`을 `true`로 설정하면, 큐 이벤트 리스너, 메일, 알림, 브로드캐스트 이벤트도 모두 열린 트랜잭션 커밋 후에 디스패치됩니다.

<a name="specifying-commit-dispatch-behavior-inline"></a>
#### 커밋 후 디스패치 방식을 인라인으로 지정하기

`after_commit` 설정을 하지 않아도, 특정 잡만 트랜잭션 커밋 후에 디스패치하고 싶으면, 디스패치 시 `afterCommit` 체인을 붙이면 됩니다:

```php
use App\Jobs\ProcessPodcast;

ProcessPodcast::dispatch($podcast)->afterCommit();
```

반대로, `after_commit`이 `true`일 때, 특정 잡만 즉시 디스패치하고 싶으면 `beforeCommit`을 체인하세요:

```php
ProcessPodcast::dispatch($podcast)->beforeCommit();
```

<a name="job-chaining"></a>
### 잡 체이닝 (Job Chaining)

잡 체이닝을 통해, 주 작업이 성공적으로 실행된 뒤 순차적으로 실행할 잡 목록을 지정할 수 있습니다. 체인의 중간에 하나라도 실패하면 이후 잡은 실행되지 않습니다. 체인은 `Bus` 팩사드의 `chain` 메서드로 실행합니다:

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

클래스 인스턴스뿐 아니라 클로저도 체인에 넣을 수 있습니다:

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
> 잡 내부에서 `$this->delete()`를 호출해도 체인이 멈추지 않습니다. 체인은 잡 실패 시에만 실행을 멈춥니다.

<a name="chain-connection-queue"></a>
#### 체인 내 커넥션 및 큐 지정

체인에 사용되는 잡들의 커넥션 및 큐를 지정할 수 있습니다. 잡 개별 설정이 없는 한, `onConnection`과 `onQueue`로 지정한 값이 사용됩니다:

```php
Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->onConnection('redis')->onQueue('podcasts')->dispatch();
```

<a name="chain-failures"></a>
#### 체인 실패 처리

체인 중 한 잡이 실패하면 `catch` 메서드에 정의된 콜백이 호출됩니다. 콜백엔 실패 원인인 `Throwable` 인스턴스가 전달됩니다:

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
> 체인 콜백은 직렬화되어 큐에서 나중에 실행되므로, 콜백 내에서 `$this` 변수를 사용하지 마십시오.

<a name="customizing-the-queue-and-connection"></a>
### 큐 및 커넥션 커스터마이징 (Customizing The Queue and Connection)

<a name="dispatching-to-a-particular-queue"></a>
#### 특정 큐에 디스패치

다양한 큐에 작업을 분류하거나 우선순위 별로 워커를 배정할 때 유용합니다. 이는 큐 설정 파일에 정의된 다른 커넥션으로 보내는 것이 아니라, 동일 커넥션 내의 다른 큐를 지정하는 의미입니다. `dispatch` 시 `onQueue` 메서드를 사용하세요:

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
     * 팟캐스트 저장
     */
    public function store(Request $request): RedirectResponse
    {
        $podcast = Podcast::create(/* ... */);

        // ...

        ProcessPodcast::dispatch($podcast)->onQueue('processing');

        return redirect('/podcasts');
    }
}
```

또는 잡 생성자 내에서 `onQueue` 호출로 지정할 수도 있습니다:

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
     */
    public function __construct()
    {
        $this->onQueue('processing');
    }
}
```

<a name="dispatching-to-a-particular-connection"></a>
#### 특정 커넥션에 디스패치

여러 큐 커넥션을 사용하는 경우, `onConnection` 메서드로 잡을 보낼 커넥션을 지정할 수 있습니다:

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
     * 팟캐스트 저장
     */
    public function store(Request $request): RedirectResponse
    {
        $podcast = Podcast::create(/* ... */);

        // ...

        ProcessPodcast::dispatch($podcast)->onConnection('sqs');

        return redirect('/podcasts');
    }
}
```

`onConnection`과 `onQueue`를 연속해서 체인할 수도 있습니다:

```php
ProcessPodcast::dispatch($podcast)
              ->onConnection('sqs')
              ->onQueue('processing');
```

또는 생성자 내에서 지정할 수도 있습니다:

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
     */
    public function __construct()
    {
        $this->onConnection('sqs');
    }
}
```

<a name="max-job-attempts-and-timeout"></a>
### 최대 재시도 및 타임아웃 지정 (Specifying Max Job Attempts / Timeout Values)

<a name="max-attempts"></a>
#### 최대 재시도 횟수 (Max Attempts)

잡이 오류가 발생할 때 무한히 재시도되면 안 됩니다. Artisan 명령어 `queue:work` 실행 시 `--tries` 옵션으로 워커가 실행할 최대 재시도 횟수를 지정하세요. 잡 클래스 내 재시도 횟수가 지정되어 있으면 명령행 옵션보다 우선합니다:

```shell
php artisan queue:work --tries=3
```

재시도를 초과하면 잡은 "실패"로 간주되어 `failed_jobs` 테이블에 저장됩니다.

잡 클래스에 재시도 횟수 프로퍼티로 지정 가능합니다:

```php
<?php

namespace App\Jobs;

class ProcessPodcast implements ShouldQueue
{
    /**
     * 잡 재시도 최대 횟수
     *
     * @var int
     */
    public $tries = 5;
}
```

동적 재시도 횟수를 지정하려면 `tries` 메서드를 구현하세요:

```php
/**
 * 잡 재시도 최대 횟수 결정
 */
public function tries(): int
{
    return 5;
}
```

<a name="time-based-attempts"></a>
#### 시간 기반 재시도 (Time Based Attempts)

횟수 대신, 잡을 더 이상 시도하지 않을 시간을 지정할 수도 있습니다. `retryUntil` 메서드를 구현하여 `DateTime` 인스턴스를 반환하세요:

```php
use DateTime;

/**
 * 잡 재시도 종료 시점 결정
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(10);
}
```

> [!NOTE]  
> [큐에 들어가는 이벤트 리스너](/docs/10.x/events#queued-event-listeners)도 같은 방식으로 `tries` 또는 `retryUntil`을 지정할 수 있습니다.

<a name="max-exceptions"></a>
#### 최대 예외 횟수 (Max Exceptions)

많은 재시도를 허용하되, 지정된 횟수 이상의 처리되지 않은 예외가 발생하면 실패 처리하려면 `maxExceptions` 속성을 지정하세요:

```php
<?php

namespace App\Jobs;

use Illuminate\Support\Facades\Redis;

class ProcessPodcast implements ShouldQueue
{
    /**
     * 재시도 최대 횟수
     *
     * @var int
     */
    public $tries = 25;

    /**
     * 최대 처리되지 않은 예외 허용 횟수
     *
     * @var int
     */
    public $maxExceptions = 3;

    /**
     * 잡 실행
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

이 예에서, 락 획득 실패 시 10초 대기 후 재시도하며, 총 25회 재시도하지만 3회 이상 예외 발생 시 잡이 실패합니다.

<a name="timeout"></a>
#### 타임아웃 (Timeout)

잡 처리 시간의 대략적인 한계를 아는 경우가 많으므로, Laravel은 잡 타임아웃 시간을 지정할 수 있도록 지원합니다. 기본값은 60초이며, 타임아웃이 지나면 잡을 처리 중인 워커 프로세스는 에러와 함께 종료됩니다. 보통은 서버에 설정된 [프로세스 관리자](#supervisor-configuration)가 자동으로 워커를 재시작합니다.

명령행 옵션 `--timeout`으로 초 단위 시간을 지정할 수 있습니다:

```shell
php artisan queue:work --timeout=30
```

잡 클래스 내에서도 타임아웃 초를 지정할 수 있습니다. 이 경우, 커맨드라인 옵션보다 우선합니다:

```php
<?php

namespace App\Jobs;

class ProcessPodcast implements ShouldQueue
{
    /**
     * 잡 타임아웃 시간(초)
     *
     * @var int
     */
    public $timeout = 120;
}
```

소켓, HTTP 요청 등 IO 차단 과정은 PHP 타임아웃을 무시할 수 있으므로, 사용 중인 API에서 별도 타임아웃을 지정하는 게 좋습니다. (예: Guzzle의 연결 및 요청 타임아웃)

> [!WARNING]  
> 잡 타임아웃을 사용하려면 `pcntl` PHP 확장 모듈이 필수입니다. 또한, 잡 타임아웃 값은 같은 잡의 "retry after" 값보다 짧아야 하며, 그렇지 않으면 잡이 완전히 끝나기 전에 재시도되어 2회 처리될 수 있습니다.

<a name="failing-on-timeout"></a>
#### 타임아웃 시 실패 처리

타임아웃 시 잡을 실패 처리하려면, 잡 클래스에 `$failOnTimeout` 프로퍼티를 `true`로 설정하세요:

```php
/**
 * 타임아웃 시 잡 실패 표시 여부
 *
 * @var bool
 */
public $failOnTimeout = true;
```

<a name="error-handling"></a>
### 에러 처리 (Error Handling)

잡 처리 중 예외가 던져지면, Laravel은 자동으로 잡을 큐에 다시 넣어 재시도합니다. 이 과정은 최대 재시도 횟수까지 반복됩니다. 최대 재시도 횟수는 `queue:work` 명령어의 `--tries` 옵션이나 잡 클래스 내에 지정된 값을 따릅니다. 큐 워커 실행에 대한 자세한 내용은 [아래](#running-the-queue-worker)를 참고하세요.

<a name="manually-releasing-a-job"></a>
#### 수동으로 잡 다시 큐에 넣기 (Manually Releasing a Job)

중간에 수동으로 잡 실행을 중단하고, 나중에 재시도하려면 `release` 메서드를 호출하세요:

```php
/**
 * 잡 실행
 */
public function handle(): void
{
    // ...

    $this->release();
}
```

기본적으로 바로 다시 처리할 수 있지만, 초 단위 딜레이를 지정할 수도 있습니다:

```php
$this->release(10);

$this->release(now()->addSeconds(10));
```

<a name="manually-failing-a-job"></a>
#### 수동으로 잡 실패 처리 (Manually Failing a Job)

잡을 수동으로 실패 처리하려면 `fail` 메서드를 호출합니다:

```php
/**
 * 잡 실행
 */
public function handle(): void
{
    // ...

    $this->fail();
}
```

예외를 받아서 실패 처리할 수도 있고, 문자열 메시지를 넘겨 예외로 변환시킬 수도 있습니다:

```php
$this->fail($exception);

$this->fail('Something went wrong.');
```

> [!NOTE]  
> 실패한 잡에 관한 자세한 내용은 [실패 잡 처리](#dealing-with-failed-jobs) 항목을 참고하세요.

<a name="job-batching"></a>
## 잡 배칭 (Job Batching)

잡 배칭 기능을 사용하면, 잡 묶음을 쉽게 실행하고 배치 작업 완료 후 후속 작업을 지정할 수 있습니다. 시작하기 전에 배치 메타 정보를 저장할 데이터베이스 테이블을 만드는 마이그레이션을 만드세요. 이 마이그레이션은 `queue:batches-table` Artisan 명령어로 생성합니다:

```shell
php artisan queue:batches-table

php artisan migrate
```

<a name="defining-batchable-jobs"></a>
### 배치 가능한 잡 정의 (Defining Batchable Jobs)

배치 가능한 잡은 일반 큐 잡을 생성한 뒤, `Illuminate\Bus\Batchable` 트레이트를 추가해야 합니다. 이 트레이트는 실행 중인 배치 정보를 가져오는 `batch` 메서드를 제공합니다:

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
     */
    public function handle(): void
    {
        if ($this->batch()->cancelled()) {
            // 배치가 취소되었는지 확인...

            return;
        }

        // CSV 일부 가져오기...
    }
}
```

<a name="dispatching-batches"></a>
### 배치 디스패치 (Dispatching Batches)

`Bus` 팩사드의 `batch` 메서드로 잡 배치를 디스패치합니다. 배치가 유용한 점은 완료 후 콜백(then, catch, finally)을 지정할 수 있다는 점입니다. 각 콜백은 `Illuminate\Bus\Batch` 인스턴스를 인자로 받습니다. 예를 들어 CSV 일부를 처리하는 잡들을 큐에 넣는 예:

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
    // 배치 생성 후, 잡 추가 전...
})->progress(function (Batch $batch) {
    // 단일 잡 성공 처리...
})->then(function (Batch $batch) {
    // 모든 잡 성공 완료...
})->catch(function (Batch $batch, Throwable $e) {
    // 배치 내 첫 실패 감지...
})->finally(function (Batch $batch) {
    // 배치 실행 끝...
})->dispatch();

return $batch->id;
```

배치 ID(`$batch->id`)는 [큐 명령 버스](#inspecting-batches)에서 배치 상태 조회용으로 쓸 수 있습니다.

> [!WARNING]  
> 배치 콜백은 큐에서 직렬화해 나중에 실행하는 점을 고려해 `$this` 변수를 사용하지 말아야 합니다.

<a name="naming-batches"></a>
#### 배치 이름 지정

Laravel Horizon, Telescope 등의 툴에서 배치를 구분 짓기 위해 임의 이름을 지정할 수 있습니다:

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // 성공 처리
})->name('Import CSV')->dispatch();
```

<a name="batch-connection-queue"></a>
#### 배치의 커넥션과 큐 지정

배치 내 모든 잡은 같은 커넥션과 큐에서만 실행되어야 하며, `onConnection`과 `onQueue`로 지정할 수 있습니다:

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // 성공 처리
})->onConnection('redis')->onQueue('imports')->dispatch();
```

<a name="chains-and-batches"></a>
### 체인과 배치 (Chains and Batches)

다른 잡 체인 내에 여러 배치를 정의할 수 있습니다. 예를 들어 병렬로 두 개 배치를 실행 후 완료 콜백 실행:

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

반대로, 배치 내에 체인을 넣어 순차 실행 가능:

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

대규모 잡을 한 번에 디스패치하기 힘든 경우, 초기 "로더" 잡 배치를 디스패치해 해당 작업을 채우도록 할 수 있습니다:

```php
$batch = Bus::batch([
    new LoadImportBatch,
    new LoadImportBatch,
    new LoadImportBatch,
])->then(function (Batch $batch) {
    // 모두 성공 시...
})->name('Import Contacts')->dispatch();
```

`LoadImportBatch` 잡 내에서 다음과 같이 배치에 잡을 추가합니다:

```php
use App\Jobs\ImportContacts;
use Illuminate\Support\Collection;

/**
 * 잡 실행
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
### 배치 검사하기 (Inspecting Batches)

`Illuminate\Bus\Batch` 인스턴스는 배치 확인과 조작에 도움되는 여러 속성/메서드를 제공합니다:

```php
// 배치 UUID
$batch->id;

// 배치 이름 (존재하면)
$batch->name;

// 배치 할당된 잡 전체 수
$batch->totalJobs;

// 아직 처리 전인 잡 수
$batch->pendingJobs;

// 실패한 잡 수
$batch->failedJobs;

// 지금까지 처리 완료된 잡 수
$batch->processedJobs();

// 배치 진행률(0-100%)
$batch->progress();

// 배치 실행 완료 여부
$batch->finished();

// 배치 실행 취소
$batch->cancel();

// 배치 취소 여부
$batch->cancelled();
```

<a name="returning-batches-from-routes"></a>
#### 라우트에서 배치 반환하기

`Illuminate\Bus\Batch`는 JSON 직렬화를 지원하므로, 라우트에서 직접 반환 가능하며 배치 진행 상황 UI 표시 등에 편리합니다.

배치 ID로 조회하려면 `Bus` 팩사드의 `findBatch` 메서드 사용:

```php
use Illuminate\Support\Facades\Bus;
use Illuminate\Support\Facades\Route;

Route::get('/batch/{batchId}', function (string $batchId) {
    return Bus::findBatch($batchId);
});
```

<a name="cancelling-batches"></a>
### 배치 취소하기 (Cancelling Batches)

배치 실행을 취소하려면 `Illuminate\Bus\Batch` 인스턴스의 `cancel` 메서드를 호출하세요:

```php
/**
 * 잡 실행
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

잡 내부에서 배치가 취소됐는지 확인하는 데 번거로우면, `SkipIfBatchCancelled` 미들웨어를 잡에 추가하세요. 배치가 취소된 경우 잡 실행을 건너뜁니다:

```php
use Illuminate\Queue\Middleware\SkipIfBatchCancelled;

/**
 * 잡 미들웨어 반환
 */
public function middleware(): array
{
    return [new SkipIfBatchCancelled];
}
```

<a name="batch-failures"></a>
### 배치 실패 (Batch Failures)

배치 내 잡이 실패하면, `catch` 콜백이 호출되며, 첫 번째 실패 잡의 예외를 인자로 받습니다.

<a name="allowing-failures"></a>
#### 실패 허용하기 (Allowing Failures)

기본적으로 배치 내 잡 실패 시 Laravel은 배치를 "취소"로 표시합니다. 이 동작을 끄고 싶으면, 배치 디스패치 시 `allowFailures` 메서드를 호출하세요:

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // 성공 처리
})->allowFailures()->dispatch();
```

<a name="retrying-failed-batch-jobs"></a>
#### 실패한 배치 잡 재시도

`queue:retry-batch` Artisan 명령어로 특정 배치의 실패한 모든 잡을 재시도할 수 있습니다. 배치 UUID를 인자로 넘기세요:

```shell
php artisan queue:retry-batch 32dbc76c-4f82-4749-b610-a639fe0099b5
```

<a name="pruning-batches"></a>
### 배치 정리 (Pruning Batches)

`job_batches` 테이블은 정리하지 않으면 급격히 레코드가 늘어납니다. 이를 방지하려면 [스케줄러](/docs/10.x/scheduling)에 `queue:prune-batches` Artisan 명령어를 매일 등록하세요:

```php
$schedule->command('queue:prune-batches')->daily();
```

기본적으로 완료된 배치 중 24시간이 지난 것들을 삭제하며, `--hours` 옵션으로 보관 기간을 조절할 수 있습니다. 예를 들면 48시간 이전 배치 삭제:

```php
$schedule->command('queue:prune-batches --hours=48')->daily();
```

완료되지 않은 배치도 정리하려면 `--unfinished` 옵션 지정:

```php
$schedule->command('queue:prune-batches --hours=48 --unfinished=72')->daily();
```

취소된 배치도 정리하려면 `--cancelled` 옵션 사용:

```php
$schedule->command('queue:prune-batches --hours=48 --cancelled=72')->daily();
```

<a name="storing-batches-in-dynamodb"></a>
### DynamoDB에 배치 저장하기 (Storing Batches in DynamoDB)

배치 메타 정보를 관계형 DB 대신 [DynamoDB](https://aws.amazon.com/dynamodb)에 저장할 수도 있습니다. 단, DynamoDB 테이블(`job_batches`)을 직접 생성해야 합니다.

<a name="dynamodb-batch-table-configuration"></a>
#### DynamoDB 배치 테이블 구성

DynamoDB 테이블에는 파티션 키 `application` (문자열)과 정렬 키 `id` (문자열)를 지정해야 하며, `application` 키는 `app.name` 설정의 앱 이름을 저장합니다. 이렇게 하면 하나의 테이블로 여러 Laravel 앱의 배치 데이터를 저장할 수 있습니다.

필요하면 `ttl` 속성도 추가해 [자동 배치 정리](#pruning-batches-in-dynamodb)를 활용하세요.

<a name="dynamodb-configuration"></a>
#### DynamoDB 구성

AWS SDK를 설치해 Laravel이 DynamoDB와 통신할 수 있도록 합니다:

```shell
composer require aws/aws-sdk-php
```

`queue.batching.driver` 설정값을 `dynamodb`로 바꾸고, `batching` 설정 부분에 `key`, `secret`, `region` 값을 정의하세요:

```php
'batching' => [
    'driver' => env('QUEUE_FAILED_DRIVER', 'dynamodb'),
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'table' => 'job_batches',
],
```

`queue.batching.database` 설정은 불필요합니다.

<a name="pruning-batches-in-dynamodb"></a>
#### DynamoDB에서 배치 정리하기

DynamoDB 기반 배치는 일반 명령어로 정리되지 않으므로, DynamoDB의 TTL 기능을 활용해 오래된 레코드를 자동 삭제하세요.

DynamoDB 테이블에 `ttl` 속성을 만들고, `queue.batching.ttl_attribute`로 TTL 속성 이름을, `queue.batching.ttl`로 TTL 유지 시간(초)을 설정하세요:

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

잡 클래스를 디스패치하는 대신 클로저를 직접 큐에 넣을 수도 있습니다. 간단한 작업을 웹 요청과 분리해 실행할 때 편리합니다. 큐에 넣는 클로저는 코드 내용이 암호화된 서명과 함께 저장되므로 전송 중 변경되지 않습니다:

```php
$podcast = App\Podcast::find(1);

dispatch(function () use ($podcast) {
    $podcast->publish();
});
```

`catch` 메서드를 이용해, 모든 재시도 후에도 실패 시 실행할 콜백을 지정할 수도 있습니다:

```php
use Throwable;

dispatch(function () use ($podcast) {
    $podcast->publish();
})->catch(function (Throwable $e) {
    // 잡이 실패했을 때...
});
```

> [!WARNING]  
> 클로저의 `catch` 콜백도 지연 실행되므로 `$this` 변수 사용을 피하세요.

<a name="running-the-queue-worker"></a>
## 큐 워커 실행하기 (Running the Queue Worker)

<a name="the-queue-work-command"></a>
### `queue:work` 명령어

Laravel은 큐에서 새 작업을 감지해 처리하는 Artisan 명령어를 제공합니다. `queue:work` 명령어로 워커를 실행하면, 명령어가 종료될 때까지 계속 실행됩니다:

```shell
php artisan queue:work
```

> [!NOTE]  
> 프로덕션 환경에서 `queue:work`를 백그라운드에서 항상 실행하려면 [Supervisor](#supervisor-configuration) 같은 프로세스 모니터로 관리해야 합니다.

`-v` 옵션을 추가하면 처리된 잡 ID가 출력에 포함됩니다:

```shell
php artisan queue:work -v
```

큐 워커는 장기간 실행되는 프로세스로, 시작 후 코드 변경을 감지하지 못합니다. 따라서 배포 시 반드시 [워커 재시작](#queue-workers-and-deployment) 후 업데이트해야 하며, 앱 내 정적 상태도 초기화되지 않음을 유의하세요.

참고로, `queue:listen` 명령어도 있지만, 소스코드를 요청마다 다시 로드하므로 성능 상 비효율적입니다:

```shell
php artisan queue:listen
```

<a name="running-multiple-queue-workers"></a>
#### 다중 워커 실행하기

동시에 여러 워커를 돌리려면 여러 개의 `queue:work` 프로세스를 실행하세요. 로컬에서는 터미널 여러 탭에서 가능하며, 프로덕션에서는 프로세스 관리자 설정에서 `numprocs` 값을 쓰면 됩니다.

<a name="specifying-the-connection-queue"></a>
#### 커넥션 & 큐 지정

워커가 어떤 큐 커넥션을 사용할지 지정할 수 있습니다. 커넥션 이름은 `config/queue.php`의 `connections`와 일치해야 합니다:

```shell
php artisan queue:work redis
```

기본적으로 워커는 커넥션 내 기본 큐만 처리하지만, 특정 큐만 처리하도록 지정할 수도 있습니다. 예를 들어 Redis 연결에서 `emails` 큐만 처리하려면 다음과 같이:

```shell
php artisan queue:work redis --queue=emails
```

<a name="processing-a-specified-number-of-jobs"></a>
#### 지정 개수의 잡만 처리하기

`--once` 옵션을 지정하면 워커가 큐에서 단 1개의 잡만 처리하고 종료합니다:

```shell
php artisan queue:work --once
```

`--max-jobs` 옵션은 지정한 수만큼 잡을 처리한 뒤 종료합니다. Supervisor 등과 함께 쓰면 잦은 재시작으로 메모리 누수를 막을 수 있습니다:

```shell
php artisan queue:work --max-jobs=1000
```

<a name="processing-all-queued-jobs-then-exiting"></a>
#### 큐가 빌 때까지 처리 후 종료

`--stop-when-empty` 옵션은 대기 중인 모든 잡을 처리한 뒤 워커가 종료되도록 합니다. Docker 환경에서 큐 종료 후 컨테이너를 안전하게 종료할 때 유용합니다:

```shell
php artisan queue:work --stop-when-empty
```

<a name="processing-jobs-for-a-given-number-of-seconds"></a>
#### 지정한 시간 동안 작업 처리

`--max-time` 옵션을 이용하면 지정한 초만큼 잡을 처리한 뒤 종료합니다. Supervisor와 결합시 안정적으로 메모리를 관리할 수 있습니다:

```shell
# 1시간 동안 처리 후 종료...
php artisan queue:work --max-time=3600
```

<a name="worker-sleep-duration"></a>
#### 워커 슬립 시간

잡이 있으면 계속 처리하지만, 잡이 없을 때 얼마나 초단위로 쉴지 `--sleep` 옵션으로 지정합니다. 쉴 때는 잡 처리 불가능합니다:

```shell
php artisan queue:work --sleep=3
```

<a name="maintenance-mode-queues"></a>
#### 유지보수 모드와 큐

애플리케이션이 [유지보수 모드](/docs/10.x/configuration#maintenance-mode)일 때는 큐 잡 처리가 중단됩니다. 유지보수 모드 해제 후 정상 처리됩니다.

강제로 유지보수 모드 상태여도 잡을 처리하려면 `--force` 옵션을 추가하세요:

```shell
php artisan queue:work --force
```

<a name="resource-considerations"></a>
#### 리소스 관리 고려사항

데몬 큐 워커는 잡마다 앱을 재부팅하지 않으므로, 잡 종료 후 메모리 해제 같은 리소스 관리를 잘 해줘야 합니다. 예를 들어 GD 라이브러리로 이미지 작업 후엔 `imagedestroy`를 호출하세요.

<a name="queue-priorities"></a>
### 큐 우선순위 (Queue Priorities)

큐를 우선순위별로 처리할 수도 있습니다. 예를 들어 `config/queue.php`에서 기본 Redis 큐를 `low`로 지정했지만, 중요한 잡은 `high` 큐에 넣는다 가정:

```php
dispatch((new Job)->onQueue('high'));
```

이때, 워커를 다음과 같이 실행해 `high` 큐를 먼저 처리하도록 할 수 있습니다:

```shell
php artisan queue:work --queue=high,low
```

<a name="queue-workers-and-deployment"></a>
### 큐 워커와 배포 (Queue Workers and Deployment)

큐 워커는 장기간 실행되는 프로세스라서 코드 변경을 자동 감지하지 못합니다. 따라서 배포 시 워커를 반드시 재시작해야 합니다. 다음 명령어로 기존 워커에 종료 신호를 보내 현재 작업 완료 후 종료하도록 합니다:

```shell
php artisan queue:restart
```

워커 재시작 시, [Supervisor](#supervisor-configuration) 등 프로세스 관리자에서 자동으로 워커를 다시 시작해야 합니다.

> [!NOTE]  
> 이 기능은 [캐시](/docs/10.x/cache) 시스템에 restart 신호를 저장하므로, 캐시 드라이버가 제대로 설정되어 있어야 합니다.

<a name="job-expirations-and-timeouts"></a>
### 잡 만료 및 타임아웃 (Job Expirations and Timeouts)

<a name="job-expiration"></a>
#### 잡 만료 (Job Expiration)

`config/queue.php` 의 각 큐 커넥션에는 `retry_after` 옵션이 있습니다. 이 값(초)은 잡이 처리 중 재시도할 때까지 대기하는 최대 시간을 지정합니다.

예를 들어 `retry_after`가 `90`이면, 90초 넘게 처리 중인 잡은 다시 큐에 들어가며, 보통 잡 처리 시간이 이 시간보다 크지 않도록 설정합니다.

> [!WARNING]  
> Amazon SQS 커넥션에는 `retry_after` 값이 없고, AWS 콘솔 내에서 [기본 가시성 제한시간](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/AboutVT.html)으로 관리됩니다.

<a name="worker-timeouts"></a>
#### 워커 타임아웃

`queue:work` 명령어는 `--timeout` 옵션을 제공합니다. 기본 60초이며, 워커가 해당 시간 넘게 잡을 처리하면 에러로 종료됩니다:

```shell
php artisan queue:work --timeout=60
```

`retry_after`와 `--timeout`은 다르지만 협력하여 잡이 중복 처리되지 않도록 합니다.

> [!WARNING]  
> `--timeout` 값은 `retry_after`보다 항상 몇 초 짧아야 합니다. 그렇지 않으면 워커가 죽기 전에 잡이 다시 처리될 수 있습니다.

<a name="supervisor-configuration"></a>
## Supervisor 설정 (Supervisor Configuration)

프로덕션에서는 `queue:work` 프로세스를 항상 실행 상태로 유지해야 합니다. 워커는 타임아웃 초과, `queue:restart` 실행 등 이유로 프로세스가 종료될 수 있습니다.

프로세스 모니터를 설정해 워커 종료를 감지하고 자동 재시작하며, 동시에 여러 워커 실행 개수도 제어할 수 있습니다. Linux에서는 보통 Supervisor를 사용하며, 다음과 같이 구성합니다.

<a name="installing-supervisor"></a>
#### Supervisor 설치

Supervisor는 Linux용 프로세스 모니터로, 워커가 실패하면 자동 재시작합니다. Ubuntu에선 다음 명령어로 설치:

```shell
sudo apt-get install supervisor
```

> [!NOTE]  
> 직접 설치 및 설정이 부담된다면, [Laravel Forge](https://forge.laravel.com)가 자동으로 Supervisor를 설치 및 설정해 줍니다.

<a name="configuring-supervisor"></a>
#### Supervisor 설정

설정 파일은 보통 `/etc/supervisor/conf.d`에 저장하며, 여기서 워커 프로세스 구성을 정의합니다. 예시 `laravel-worker.conf`:

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

`numprocs=8`은 8개의 워커 프로세스를 실행하고 모니터링하며, 실패하면 재시작합니다. `command`는 원하는 커넥션과 워커 옵션으로 변경하세요.

> [!WARNING]  
> `stopwaitsecs` 값을 가장 오래 걸리는 작업 처리 시간보다 길게 해야 합니다. 그렇지 않으면 Supervisor가 잡 종료 전 워커를 강제 종료할 수 있습니다.

<a name="starting-supervisor"></a>
#### Supervisor 실행하기

설정 파일 작성 후, 다음 명령어로 Supervisor 구성을 반영하고 워커를 실행합니다:

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start "laravel-worker:*"
```

더 자세한 내용은 [Supervisor 공식 문서](http://supervisord.org/index.html)를 참고하세요.

<a name="dealing-with-failed-jobs"></a>
## 실패한 잡 처리하기 (Dealing With Failed Jobs)

가끔 큐 잡 처리에 실패할 수 있습니다. Laravel은 최대 재시도 횟수 초과 시 잡을 `failed_jobs` 테이블에 저장해 관리합니다. 동기식 잡은 실패 시 즉시 예외가 처리되며 테이블에 저장되지 않습니다.

대부분의 새 Laravel 앱에는 실패한 잡 테이블용 마이그레이션이 이미 포함되어 있지만, 없는 경우 `queue:failed-table` 명령어로 생성할 수 있습니다:

```shell
php artisan queue:failed-table

php artisan migrate
```

`queue:work` 실행 시 `--tries` 옵션으로 재시도 횟수를 설정할 수 있습니다. 지정하지 않으면 잡 클래스 내 속성 값으로 결정되거나 기본 1회입니다:

```shell
php artisan queue:work redis --tries=3
```

`--backoff` 옵션으로 예외 후 재시도 대기시간(초)도 설정할 수 있습니다(기본은 즉시 재시도):

```shell
php artisan queue:work redis --tries=3 --backoff=3
```

잡 클래스에서 `backoff` 속성으로 구성할 수도 있습니다:

```php
/**
 * 재시도 대기 시간 (초)
 *
 * @var int
 */
public $backoff = 3;
```

더 복잡한 로직이 필요하면 `backoff` 메서드를 구현하세요:

```php
/**
 * 재시도 대기 시간 계산
 */
public function backoff(): int
{
    return 3;
}
```

`backoff` 메서드는 배열을 반환해 지수적 백오프도 쉽게 구현할 수 있습니다. 예:

```php
/**
 * 재시도 대기 시간 배열 반환
 *
 * @return array<int, int>
 */
public function backoff(): array
{
    return [1, 5, 10];
}
```

위 예제는 첫 재시도 1초, 두 번째 5초, 세 번째 이후 10초 대기입니다.

<a name="cleaning-up-after-failed-jobs"></a>
### 실패 잡 후속 조치 (Cleaning Up After Failed Jobs)

잡 실패 시 사용자 알림 보내기 등 후속 조치를 하려면 잡 클래스에 `failed` 메서드를 구현하세요. 실패 원인 예외 인스턴스가 전달됩니다:

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
        // 팟캐스트 처리...
    }

    /**
     * 잡 실패 처리
     */
    public function failed(?Throwable $exception): void
    {
        // 사용자 알림, 정리 작업 등...
    }
}
```

> [!WARNING]  
> `failed` 메서드 호출 전 잡이 새 인스턴스로 복원되므로, `handle` 내 상태 변경은 사라집니다.

<a name="retrying-failed-jobs"></a>
### 실패 잡 재시도 (Retrying Failed Jobs)

`failed_jobs` 테이블에 저장된 실패 잡들을 보려면 `queue:failed` 명령어를 사용하세요:

```shell
php artisan queue:failed
```

출력된 잡 ID를 사용해 개별 실패 잡 재시도 가능:

```shell
php artisan queue:retry ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece
```

한 번에 여러 ID도 가능합니다:

```shell
php artisan queue:retry ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece 91401d2c-0784-4f43-824c-34f94a33c24d
```

특정 큐만 재시도하려면:

```shell
php artisan queue:retry --queue=name
```

모든 실패 잡 재시도는 `all` 인자 사용:

```shell
php artisan queue:retry all
```

실패 잡 삭제는 `queue:forget` 명령어를 사용:

```shell
php artisan queue:forget 91401d2c-0784-4f43-824c-34f94a33c24d
```

> [!NOTE]  
> Horizon 사용 시 `horizon:forget` 명령어를 쓰세요.

모든 실패 잡 삭제는 `queue:flush` 명령어:

```shell
php artisan queue:flush
```

<a name="ignoring-missing-models"></a>
### 모델 누락 무시 (Ignoring Missing Models)

잡에 Eloquent 모델 주입 시, 모델이 삭제되어 `ModelNotFoundException` 발생할 수 있습니다. 이를 방지하려면 잡 클래스에 다음 플래그를 설정하세요:

```php
/**
 * 모델이 없으면 잡 삭제
 *
 * @var bool
 */
public $deleteWhenMissingModels = true;
```

해당 속성이 true면 예외 대신 조용히 잡을 폐기합니다.

<a name="pruning-failed-jobs"></a>
### 실패 잡 정리 (Pruning Failed Jobs)

`failed_jobs` 테이블의 기록을 정리하려면 `queue:prune-failed` 명령어를 실행합니다:

```shell
php artisan queue:prune-failed
```

기본적으로 24시간 이전 실패 잡들이 삭제됩니다. `--hours` 옵션으로 보관 시간을 조정 가능:

```shell
php artisan queue:prune-failed --hours=48
```

<a name="storing-failed-jobs-in-dynamodb"></a>
### DynamoDB에 실패한 잡 저장 (Storing Failed Jobs in DynamoDB)

실패한 잡도 관계형 DB 대신 DynamoDB에 저장할 수 있습니다. DynamoDB 테이블(`failed_jobs`)은 파티션 키 `application`과 정렬 키 `uuid`를 갖고, `app.name`의 앱 이름을 파티션 키로 저장합니다.

AWS SDK 설치:

```shell
composer require aws/aws-sdk-php
```

`queue.failed.driver`를 `dynamodb`로 변경하고, `key`, `secret`, `region` 설정을 추가하세요:

```php
'failed' => [
    'driver' => env('QUEUE_FAILED_DRIVER', 'dynamodb'),
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'table' => 'failed_jobs',
],
```

`queue.failed.database` 설정은 불필요합니다.

<a name="disabling-failed-job-storage"></a>
### 실패 잡 저장 비활성화 (Disabling Failed Job Storage)

실패한 잡 저장을 끄려면 `QUEUE_FAILED_DRIVER` 환경변수를 `null`로 설정하세요:

```ini
QUEUE_FAILED_DRIVER=null
```

<a name="failed-job-events"></a>
### 실패 잡 이벤트 (Failed Job Events)

잡 실패 시 이벤트 리스너를 등록하려면 `Queue` 팩사드의 `failing` 메서드를 사용합니다. 예를 들어 `AppServiceProvider` 내 `boot` 메서드에서 다음과 같이 할 수 있습니다:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Queue;
use Illuminate\Support\ServiceProvider;
use Illuminate\Queue\Events\JobFailed;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 등록
     */
    public function register(): void
    {
        // ...
    }

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
## 큐에서 잡 비우기 (Clearing Jobs From Queues)

> [!NOTE]  
> Horizon을 사용하면 `queue:clear` 대신 `horizon:clear` 명령어 사용을 권장합니다.

기본 커넥션과 큐에서 모든 잡을 비우려면:

```shell
php artisan queue:clear
```

특정 커넥션과 큐를 지정하려면 `connection` 인자와 `--queue` 옵션을 사용:

```shell
php artisan queue:clear redis --queue=emails
```

> [!WARNING]  
> 삭제는 SQS, Redis, database 드라이버에만 가능합니다. SQS 메시지 삭제는 최대 60초가 걸리니, 큐를 삭제 후 60초 내 밀어넣은 메시지가 삭제될 수 있습니다.

<a name="monitoring-your-queues"></a>
## 큐 모니터링 (Monitoring Your Queues)

큐에 갑자기 잡이 몰릴 때 처리 대기 시간이 길어질 수 있습니다. Laravel은 잡 수가 지정 임계값 넘으면 알림을 보낼 수 있습니다.

먼저 `queue:monitor` 명령어를 [1분 단위로 스케줄링](/docs/10.x/scheduling)하세요. 큐 이름 목록과 임계값을 지정합니다:

```shell
php artisan queue:monitor redis:default,redis:deployments --max=100
```

이 명령어만 등록해도 알림은 자동으로 발송되지 않습니다. 임계값 초과 시 `Illuminate\Queue\Events\QueueBusy` 이벤트가 발생하며, 이를 리스닝해 알림을 발송해야 합니다. 예:

```php
use App\Notifications\QueueHasLongWaitTime;
use Illuminate\Queue\Events\QueueBusy;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\Facades\Notification;

/**
 * 이벤트 등록
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

잡을 디스패치하는 코드를 테스트할 때, 실제 잡 실행을 막고 디스패치 동작만 확인하고 싶다면 `Queue` 팩사드의 `fake` 메서드를 사용하세요. 잡 클래스의 `handle` 메서드는 별도로 테스트하면 됩니다.

`Queue::fake()`를 호출 후, 잡이 큐에 들어갔는지 확인할 수 있습니다:

```php
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

`assertPushed`, `assertNotPushed`에는 검증용 클로저를 전달해 더 세부 조건을 검사할 수도 있습니다:

```php
Queue::assertPushed(function (ShipOrder $job) use ($order) {
    return $job->order->id === $order->id;
});
```

<a name="faking-a-subset-of-jobs"></a>
### 일부 잡만 페이크하기 (Faking a Subset of Jobs)

특정 잡만 페이크하고 나머지는 실제 처리시키고 싶으면 클래스 배열을 `fake`에 전달합니다:

```php
public function test_orders_can_be_shipped(): void
{
    Queue::fake([
        ShipOrder::class,
    ]);

    // 주문 처리...

    Queue::assertPushed(ShipOrder::class, 2);
}
```

특정 잡만 제외하고 전부 페이크하려면 `except` 메서드를 사용하세요:

```php
Queue::fake()->except([
    ShipOrder::class,
]);
```

<a name="testing-job-chains"></a>
### 잡 체인 테스트 (Testing Job Chains)

잡 체인을 테스트하려면 `Bus` 팩사드를 페이크한 후 `assertChained` 메서드로 확인합니다. 인자에는 체인 잡 배열을 넣습니다:

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

클래스명 대신 잡 인스턴스 배열도 가능합니다:

```php
Bus::assertChained([
    new ShipOrder,
    new RecordShipment,
    new UpdateInventory,
]);
```

체인이 없는지 확인하려면 `assertDispatchedWithoutChain` 사용:

```php
Bus::assertDispatchedWithoutChain(ShipOrder::class);
```

<a name="testing-chained-batches"></a>
#### 체인 내 배치 테스트

체인 중에 배치가 포함된 경우, `Bus::chainedBatch` 정의로 검사할 수 있습니다:

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

`Bus` 팩사드의 `assertBatched` 메서드를 이용해 잡 배치 디스패치를 검사할 수 있습니다. 클로저 내에서 `Illuminate\Bus\PendingBatch`를 받아 검사하세요:

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

`assertBatchCount`로 디스패치된 배치 개수를 확인하고, `assertNothingBatched`로 하나도 없는지 확인 가능합니다:

```php
Bus::assertBatchCount(3);

Bus::assertNothingBatched();
```

<a name="testing-job-batch-interaction"></a>
#### 잡과 배치 상호작용 테스트

잡이 배치와 상호작용하는지 테스트할 때는 `withFakeBatch`를 사용해 잡과 페이크 배치를 함께 생성합니다:

```php
[$job, $batch] = (new ShipOrder)->withFakeBatch();

$job->handle();

$this->assertTrue($batch->cancelled());
$this->assertEmpty($batch->added);
```

<a name="job-events"></a>
## 잡 이벤트 (Job Events)

`Queue` 팩사드의 `before`와 `after` 메서드를 이용해 잡 처리 전후 호출할 콜백을 지정할 수 있습니다. 주로 추가 로그 기록이나 통계 업데이트에 활용되며, 보통 앱의 서비스 프로바이더 `boot`에서 등록합니다:

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
     * 애플리케이션 서비스 등록
     */
    public function register(): void
    {
        // ...
    }

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

`Queue` 팩사드의 `looping` 메서드는 워커가 큐에서 잡을 가져오기 전에 호출되는 콜백을 지정합니다. 예를 들어 이전 실패 잡으로 열린 DB 트랜잭션을 롤백하는 데 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Queue;

Queue::looping(function () {
    while (DB::transactionLevel() > 0) {
        DB::rollBack();
    }
});
```