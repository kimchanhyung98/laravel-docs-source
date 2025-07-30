# 큐 (Queues)

- [소개](#introduction)
    - [커넥션과 큐의 차이](#connections-vs-queues)
    - [드라이버 참고사항과 사전 조건](#driver-prerequisites)
- [잡 생성하기](#creating-jobs)
    - [잡 클래스 생성하기](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [고유 잡 (Unique Jobs)](#unique-jobs)
    - [암호화된 잡 (Encrypted Jobs)](#encrypted-jobs)
- [잡 미들웨어](#job-middleware)
    - [속도 제한 (Rate Limiting)](#rate-limiting)
    - [잡 중복 방지](#preventing-job-overlaps)
    - [예외 속도 제한](#throttling-exceptions)
    - [잡 건너뛰기](#skipping-jobs)
- [잡 디스패치하기](#dispatching-jobs)
    - [지연 디스패치](#delayed-dispatching)
    - [동기 디스패치](#synchronous-dispatching)
    - [잡과 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [잡 체이닝](#job-chaining)
    - [큐와 커넥션 커스터마이징](#customizing-the-queue-and-connection)
    - [최대 재시도 및 타임아웃 설정](#max-job-attempts-and-timeout)
    - [오류 처리](#error-handling)
- [잡 배칭 (Job Batching)](#job-batching)
    - [배치 가능한 잡 정의하기](#defining-batchable-jobs)
    - [배치 디스패치](#dispatching-batches)
    - [체인과 배치](#chains-and-batches)
    - [배치에 잡 추가하기](#adding-jobs-to-batches)
    - [배치 검사하기](#inspecting-batches)
    - [배치 취소하기](#cancelling-batches)
    - [배치 실패 처리](#batch-failures)
    - [배치 기록 정리하기](#pruning-batches)
    - [DynamoDB에 배치 저장하기](#storing-batches-in-dynamodb)
- [클로저 큐잉 (Queueing Closures)](#queueing-closures)
- [큐 워커 실행하기](#running-the-queue-worker)
    - [`queue:work` 명령어](#the-queue-work-command)
    - [큐 우선 순위 설정](#queue-priorities)
    - [큐 워커와 배포](#queue-workers-and-deployment)
    - [잡 만료 및 타임아웃](#job-expirations-and-timeouts)
- [Supervisor 설정](#supervisor-configuration)
- [실패한 잡 처리](#dealing-with-failed-jobs)
    - [실패 잡 정리](#cleaning-up-after-failed-jobs)
    - [실패한 잡 재시도](#retrying-failed-jobs)
    - [삭제된 모델 무시하기](#ignoring-missing-models)
    - [실패 잡 정리하기](#pruning-failed-jobs)
    - [DynamoDB에 실패 잡 저장하기](#storing-failed-jobs-in-dynamodb)
    - [실패 잡 저장 비활성화](#disabling-failed-job-storage)
    - [실패 잡 이벤트](#failed-job-events)
- [큐에서 잡 삭제하기](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [일부 잡만 가짜 처리하기](#faking-a-subset-of-jobs)
    - [잡 체인 테스트하기](#testing-job-chains)
    - [잡 배치 테스트하기](#testing-job-batches)
    - [잡 / 큐 상호작용 테스트](#testing-job-queue-interactions)
- [잡 이벤트](#job-events)

<a name="introduction"></a>
## 소개 (Introduction)

웹 애플리케이션을 개발하는 동안, 업로드된 CSV 파일을 파싱하고 저장하는 등 일반적인 웹 요청 처리 중에 시간이 너무 오래 걸리는 작업이 있을 수 있습니다. 다행히 Laravel은 이러한 작업들을 백그라운드에서 처리할 수 있도록 큐에 작업을 쉽게 생성할 수 있도록 지원합니다. 시간이 많이 걸리는 작업을 큐로 옮기면, 애플리케이션이 매우 빠르게 웹 요청에 응답할 수 있어 사용자 경험이 향상됩니다.

Laravel 큐는 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 심지어 관계형 데이터베이스 등 다양한 큐 백엔드에서 통합된 큐 API를 제공합니다.

Laravel의 큐 설정은 `config/queue.php` 설정 파일에 저장되어 있습니다. 이 파일에서는 프레임워크에 내장된 데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 드라이버 각각에 대한 커넥션 구성을 확인할 수 있습니다. 또한 로컬 개발 시에 즉시 잡을 실행하는 동기 드라이버와, 큐에 저장된 잡을 삭제하는 `null` 큐 드라이버도 포함되어 있습니다.

> [!NOTE]
> Laravel은 Redis 기반 큐를 위한 아름다운 대시보드 및 설정 시스템인 Horizon도 제공합니다. 자세한 내용은 [Horizon 문서](/docs/master/horizon)를 참고하세요.

<a name="connections-vs-queues"></a>
### 커넥션과 큐의 차이 (Connections vs. Queues)

Laravel 큐를 사용하기 전에, `config/queue.php` 설정 파일 내 `connections` 배열과 "큐"의 차이를 이해하는 것이 중요합니다. `connections` 배열은 Amazon SQS, Beanstalk, Redis 등의 백엔드 큐 서비스와 연결되는 커넥션을 정의합니다. 그러나 각 큐 커넥션에는 여러 개의 "큐"가 있을 수 있으며, 이는 서로 다른 작업 대기열 스택/더미로 생각할 수 있습니다.

설정 파일의 각 커넥션 구성에는 `queue` 속성이 있습니다. 이 속성은 해당 커넥션에 디스패치될 때 잡이 기본으로 배치되는 큐 이름입니다. 즉, 잡을 명시적으로 어느 큐에 보낼지 지정하지 않으면, 그 커넥션의 `queue` 속성에 정의된 큐에 잡이 쌓입니다:

```php
use App\Jobs\ProcessPodcast;

// 기본 커넥션의 기본 큐로 잡을 보냄...
ProcessPodcast::dispatch();

// 기본 커넥션의 "emails" 큐로 잡을 보냄...
ProcessPodcast::dispatch()->onQueue('emails');
```

어떤 애플리케이션은 단 하나의 간단한 큐만 필요할 수 있지만, 여러 큐로 작업을 분산시키는 것은 처리 우선순위나 작업 구분에 매우 유용합니다. Laravel 큐 워커는 처리할 큐를 우선순위로 지정할 수 있기 때문입니다. 예를 들어, ‘high’ 큐에 잡을 넣으면, 해당 큐를 우선 처리하는 워커를 실행할 수 있습니다:

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버 참고사항과 사전 조건 (Driver Notes and Prerequisites)

<a name="database"></a>
#### 데이터베이스

`database` 큐 드라이버를 사용하려면 작업을 저장할 데이터베이스 테이블이 필요합니다. 일반적으로 Laravel 기본 마이그레이션 `0001_01_01_000002_create_jobs_table.php`에 포함되어 있지만, 만약 애플리케이션에 없다면 `make:queue-table` Artisan 명령어로 생성할 수 있습니다:

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면 `config/database.php`에서 Redis 데이터베이스 커넥션을 설정해야 합니다.

> [!WARNING]
> `redis` 큐 드라이버는 `serializer` 및 `compression` Redis 옵션을 지원하지 않습니다.

**Redis 클러스터**

Redis 클러스터 사용 시, 큐 이름에 [키 해시 태그](https://redis.io/docs/reference/cluster-spec/#hash-tags)를 포함해야 합니다. 이는 해당 큐의 모든 Redis 키를 같은 해시 슬롯에 배치하기 위한 필수 조건입니다:

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

Redis 큐 사용 시 `block_for` 옵션으로 잡이 준비될 때까지 기다리는 시간을 초 단위로 지정할 수 있습니다. 이를 통해 지속적으로 Redis를 폴링하는 것보다 효율적으로 대기할 수 있습니다. 예를 들어 5초 동안 기다리려면:

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
> `block_for` 값을 `0`으로 설정하면 큐 워커는 잡이 준비될 때까지 무한 대기하며, 이로 인해 `SIGTERM` 같은 시그널 처리가 다음 잡이 완료될 때까지 지연될 수 있습니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 사전 조건

아래 큐 드라이버들은 Composer를 통해 다음과 같은 패키지 의존성을 설치해야 작동합니다:

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~2.0` 또는 phpredis PHP 확장
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`

<a name="creating-jobs"></a>
## 잡 생성하기 (Creating Jobs)

<a name="generating-job-classes"></a>
### 잡 클래스 생성하기 (Generating Job Classes)

기본적으로 애플리케이션의 큐 가능한 잡 클래스들은 `app/Jobs` 디렉터리에 저장됩니다. `app/Jobs` 디렉터리가 없으면 `make:job` Artisan 명령어를 실행할 때 자동 생성됩니다:

```shell
php artisan make:job ProcessPodcast
```

생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하는데, 이는 Laravel에게 해당 잡이 비동기적으로 큐에 푸시되어야 함을 알립니다.

> [!NOTE]
> 잡 스텁은 [스텁 게시 (stub publishing)](/docs/master/artisan#stub-customization)을 통해 커스터마이징할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조 (Class Structure)

잡 클래스는 매우 간단하며, 일반적으로 큐에서 처리할 때 호출되는 `handle` 메서드만 포함합니다. 다음은 팟캐스트 업로드 파일을 처리하는 예시 잡 클래스입니다:

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
     * 작업 수행
     */
    public function handle(AudioProcessor $processor): void
    {
        // 업로드된 팟캐스트 처리...
    }
}
```

이 예시에서 Eloquent 모델을 잡 생성자에 직접 전달했습니다. `Queueable` 트레이트 덕분에, Eloquent 모델 및 로드된 관계들은 잡이 직렬화 및 역직렬화될 때 우아하게 처리됩니다.

큐에 잡을 넣을 때 Eloquent 모델을 전달하면, 모델의 식별자만 직렬화되어 큐에 저장됩니다. 실제로 잡이 처리될 때는 시스템이 해당 식별자를 사용해 데이터베이스에서 완전한 모델과 관계를 다시 조회합니다. 이렇게 하면 큐 드라이버로 전송되는 잡 데이터 크기를 많이 줄일 수 있습니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드 의존성 주입

잡이 큐에 의해 처리될 때 `handle` 메서드가 호출됩니다. `handle` 메서드에 타입 힌트된 의존성을 Laravel 서비스 컨테이너가 자동으로 주입합니다.

의존성 주입을 완전히 제어하고 싶은 경우에는 컨테이너의 `bindMethod` 메서드를 활용할 수 있습니다. `bindMethod`는 잡과 컨테이너를 인자로 받는 콜백을 실행하며, 이 콜백 내에서 임의로 `handle` 메서드를 호출할 수 있습니다. 일반적으로 이 코드는 `AppServiceProvider`의 `boot` 메서드에서 실행합니다:

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 이미지 원본 데이터 같은 바이너리 데이터는 잡에 전달하기 전에 `base64_encode` 함수로 인코딩해야 합니다. 그렇지 않으면 잡이 큐에 저장될 때 JSON 직렬화가 제대로 동작하지 않을 수 있습니다.

<a name="handling-relationships"></a>
#### 큐잉된 관계 (Queued Relationships)

Eloquent 모델의 모든 로드된 관계도 직렬화되기 때문에, 직렬화된 잡 문자열이 매우 커질 수 있습니다. 또한 잡이 역직렬화되어 모델 관계가 데이터베이스에서 다시 조회될 때, 직렬화 시점에 적용된 관계 제약 조건은 재적용되지 않습니다. 따라서 관계의 일부만 다뤄야 할 경우, 잡 내부에서 다시 제한조건을 걸어야 합니다.

또는 모델에서 관계를 직렬화하지 않으려면, `withoutRelations` 메서드를 호출해 관계를 제외한 모델 인스턴스를 프로퍼티에 할당할 수 있습니다:

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

PHP 생성자 프로퍼티 승격(constructor property promotion)을 사용할 경우, `WithoutRelations` 어트리뷰트를 붙여 모델의 관계 직렬화를 방지할 수도 있습니다:

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

컬렉션 또는 배열 형태로 Eloquent 모델 집합이 잡에 전달될 경우, 큐 처리 시 관계가 복원되지 않습니다. 이는 많은 수의 모델을 처리하는 잡에서 과도한 자원 사용을 방지하기 위한 조치입니다.

<a name="unique-jobs"></a>
### 고유 잡 (Unique Jobs)

> [!WARNING]
> 고유 잡은 [락을 지원하는 캐시 드라이버](/docs/master/cache#atomic-locks)가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 드라이버가 원자적 락을 지원합니다. 또한, 고유 잡 제약 조건은 배치 잡에는 적용되지 않습니다.

특정 잡이 큐에 단 하나만 존재하도록 보장하고 싶다면, 잡 클래스에 `ShouldBeUnique` 인터페이스를 구현하면 됩니다. 별도의 메서드 정의는 필요 없습니다:

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

위 예제의 `UpdateSearchIndex` 잡은 고유하게 구성되어 동일 잡이 큐에 중복해서 들어가지 않도록 합니다.

경우에 따라 고유성의 기준 키를 직접 지정하거나, 특정 시간이 지나면 고유성이 해제되도록 타임아웃을 정의할 수 있습니다. 이때 `uniqueId` 및 `uniqueFor` 속성이나 메서드를 잡 클래스에 정의하세요:

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
     * 고유 락이 해제될 때까지 초 단위
     *
     * @var int
     */
    public $uniqueFor = 3600;

    /**
     * 잡의 고유 ID 반환
     */
    public function uniqueId(): string
    {
        return $this->product->id;
    }
}
```

위 예제에서 `UpdateSearchIndex` 잡은 상품 ID마다 고유하므로, 동일 상품 ID로 새 잡을 디스패치해도 기존 작업이 처리되는 동안 무시됩니다. 또한 한 시간이 지나면 고유 락이 해제되어 동일 키 잡을 다시 디스패치할 수 있습니다.

> [!WARNING]
> 애플리케이션이 여러 웹 서버 또는 컨테이너에서 잡을 디스패치한다면, 모든 서버가 같은 중앙 캐시 서버와 연결돼 고유 여부를 정확히 파악할 수 있도록 해야 합니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 처리 시작 전까지 고유성 유지

기본적으로 고유 잡은 실행 완료 또는 최대 재시도 실패 후 락이 해제됩니다. 그러나 처리 시작 직전에 락을 해제하고 싶으면 `ShouldBeUnique` 대신 `ShouldBeUniqueUntilProcessing` 인터페이스를 구현하면 됩니다:

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
#### 고유 잡 락

`ShouldBeUnique` 잡이 디스패치되면 내부적으로 Laravel은 `uniqueId` 키를 사용해 [락](/docs/master/cache#atomic-locks)을 획득하려 시도합니다. 락이 획득되지 않으면 잡이 큐에 푸시되지 않습니다. 락은 작업 완료 또는 모든 재시도 실패 시 해제됩니다. 기본적으로 Laravel은 기본 캐시 드라이버로 락을 획득하지만, 다른 드라이버를 지정하려면 `uniqueVia` 메서드를 정의해 캐시 드라이버를 반환할 수 있습니다:

```php
use Illuminate\Contracts\Cache\Repository;
use Illuminate\Support\Facades\Cache;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...

    /**
     * 고유 잡 락용 캐시 드라이버 반환
     */
    public function uniqueVia(): Repository
    {
        return Cache::driver('redis');
    }
}
```

> [!NOTE]
> 병렬 처리 제한만 필요하다면 [`WithoutOverlapping`](/docs/master/queues#preventing-job-overlaps) 잡 미들웨어를 사용하는 것이 적절합니다.

<a name="encrypted-jobs"></a>
### 암호화된 잡 (Encrypted Jobs)

Laravel은 잡 데이터의 비밀성과 무결성을 보장하기 위해 [암호화](/docs/master/encryption)를 지원합니다. 잡 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하면, Laravel이 자동으로 잡 데이터를 암호화한 후 큐에 저장합니다:

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

잡 미들웨어는 큐에 저장된 잡의 실행 전후 로직을 감싸 반복 코드를 줄일 수 있습니다. 예를 들어, Redis 기반 속도 제한 기능을 활용하여 5초에 한 번만 잡을 실행하도록 하는 `handle` 메서드는 다음과 같습니다:

```php
use Illuminate\Support\Facades\Redis;

/**
 * 작업 실행
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

이 코드는 유효하지만, 로직이 `handle` 메서드에 섞여 가독성이 떨어집니다. 중복도 불가피합니다.

대신, 잡 미들웨어로 위 로직을 분리할 수 있습니다. Laravel 디폴트 위치는 없으므로 원하는 위치에 둬도 되며, 여기서는 `app/Jobs/Middleware`에 예시를 들겠습니다:

```php
<?php

namespace App\Jobs\Middleware;

use Closure;
use Illuminate\Support\Facades\Redis;

class RateLimited
{
    /**
     * 큐 작업 처리
     *
     * @param  \Closure(object): void  $next
     */
    public function handle(object $job, Closure $next): void
    {
        Redis::throttle('key')
            ->block(0)->allow(1)->every(5)
            ->then(function () use ($job, $next) {
                // 락 획득 성공...

                $next($job);
            }, function () use ($job) {
                // 락 획득 실패...

                $job->release(5);
            });
    }
}
```

Route 미들웨어와 마찬가지로, 잡 미들웨어는 처리 중인 잡과 다음 단계를 호출하는 콜백을 받습니다.

잡 미들웨어 생성 후, 잡 클래스의 `middleware` 메서드에서 반환하여 미들웨어를 등록합니다. `make:job` 커맨드로 육성된 잡에는 자동 포함되어 있지 않으니 직접 추가해야 합니다:

```php
use App\Jobs\Middleware\RateLimited;

/**
 * 통과할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited];
}
```

> [!NOTE]
> 잡 미들웨어는 큐 가능 이벤트 리스너, 메일러, 알림에도 할당할 수 있습니다.

<a name="rate-limiting"></a>
### 속도 제한 (Rate Limiting)

직접 속도 제한 미들웨어를 작성할 수도 있지만, Laravel에는 속도 제한 미들웨어가 기본 제공됩니다. 라우트 속도 제한과 마찬가지로 `RateLimiter` 파사드의 `for` 메서드로 정의합니다.

예를 들어, 일반 고객은 1시간에 한 번만 백업을 수행하게 하고, 프리미엄 고객은 제한 없이 처리하도록 설정할 수 있습니다. `AppServiceProvider`의 `boot` 메서드에 정의하세요:

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

위 코드는 시간 단위 제한을 정의한 예이지만, `perMinute` 메서드로 분 단위 제한도 가능합니다. `by` 메서드에 임의 값을 전달할 수 있으며, 보통 고객 별 제한 분할에 이용됩니다:

```php
return Limit::perMinute(50)->by($job->user->id);
```

정의한 속도 제한은 `Illuminate\Queue\Middleware\RateLimited` 미들웨어로 잡에 할당할 수 있습니다. 속도 제한을 넘으면 미들웨어가 적절한 지연 시간과 함께 잡을 큐에 재배치합니다.

```php
use Illuminate\Queue\Middleware\RateLimited;

/**
 * 통과할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited('backups')];
}
```

지연하여 다시 큐에 넣더라도 `attempts` 값은 증가합니다. `tries` 및 `maxExceptions` 속성 조정이 필요하거나, [`retryUntil` 메서드](#time-based-attempts)를 활용해 재시도 기간을 제한하세요.

재시도하지 않고 바로 실패 처리하려면 `dontRelease` 메서드를 사용합니다:

```php
public function middleware(): array
{
    return [(new RateLimited('backups'))->dontRelease()];
}
```

> [!NOTE]
> Redis를 사용한다면, Redis에 최적화된 `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어를 사용하는 것이 성능상 유리합니다.

<a name="preventing-job-overlaps"></a>
### 잡 중복 방지 (Preventing Job Overlaps)

Laravel의 `Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어를 사용하면 임의 키를 기준으로 잡 중복 실행을 방지할 수 있습니다. 예를 들어, 동일 사용자 ID의 크레딧 점수 업데이트 작업이 중복 실행되지 않도록 할 때 유용합니다.

잡 클래스의 `middleware` 메서드에서 `WithoutOverlapping` 미들웨어를 반환하세요:

```php
use Illuminate\Queue\Middleware\WithoutOverlapping;

/**
 * 통과할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new WithoutOverlapping($this->user->id)];
}
```

중복 탐지된 잡은 큐로 재배치됩니다. 재배치 대기 시간을 초 단위로 지정할 수도 있습니다:

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->releaseAfter(60)];
}
```

즉시 중복 잡을 삭제하고 재시도하지 않으려면 `dontRelease`를 사용하세요:

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->dontRelease()];
}
```

`WithoutOverlapping` 미들웨어는 원자적 락 기능을 씁니다. 잡이 비정상 종료되어 락이 해제되지 않은 경우를 대비해 락 만료 시간(`expireAfter`)을 명시할 수 있습니다. 아래 예제는 잡 처리 시작 후 3분 뒤 락을 해제하도록 지정합니다:

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->expireAfter(180)];
}
```

> [!WARNING]
> `WithoutOverlapping` 미들웨어는 [락 지원 캐시 드라이버](/docs/master/cache#atomic-locks)가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 드라이버에서 락이 지원됩니다.

<a name="sharing-lock-keys"></a>
#### 잡 클래스 간 락 키 공유하기

기본적으로 `WithoutOverlapping` 미들웨어는 같은 클래스 간에만 중복을 방지합니다. 즉, 서로 다른 잡 클래스가 같은 락 키를 써도 중복 실행은 막지 않습니다. 하지만 `shared` 메서드를 호출하면 여러 잡 클래스에 키를 공유할 수 있습니다:

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
### 예외 속도 제한 (Throttling Exceptions)

Laravel의 `Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어는 잡에서 예외가 특정 횟수 이상 발생하면, 재시도를 지연시켜 안정적이지 않은 외부 서비스 호출을 보호할 수 있습니다.

예를 들어, 서드파티 API와 연동하는 잡이 예외를 던질 경우, 다음과 같이 `middleware` 메서드에 등록합니다. 보통 이 미들웨어는 시간 기반 시도 제한을 구현하는 잡과 함께 사용합니다:

```php
use DateTime;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 통과할 미들웨어 반환
 */
public function middleware(): array
{
    return [new ThrottlesExceptions(10, 5 * 60)];
}

/**
 * 잡의 타임아웃 시점 정의
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(30);
}
```

첫 인자는 예외 발생 횟수 제한, 두 번째 인자는 제한 초과 시 재시도하기 전까지 대기 시간(초)입니다. 위 예시에서는 10회 연속 예외 발생 시 5분 대기, 최대 30분 후 시도 중지입니다.

예외가 제한 횟수에 도달하지 않은 경우, 기본적으로 즉시 재시도하지만 `backoff` 메서드를 이용해 재시도 지연 시간을 지정할 수 있습니다:

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 5 * 60))->backoff(5)];
}
```

내부적으로 Laravel 캐시를 이용하며, 기본 키는 잡 클래스명입니다. `by` 메서드로 키를 지정할 수 있어 동일 서드파티 API를 여러 잡이 공유하는 경우에 유용합니다:

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->by('key')];
}
```

기본적으로 모든 예외를 제한하지만, `when` 메서드로 조건을 지정하면 해당 조건을 만족하는 예외만 제한 대상이 됩니다:

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

예외가 발생할 때 앱의 예외 핸들러에 보고하도록 하려면 `report` 메서드를 호출하세요. 이를 조건부로 동작시키려면 클로저 인자를 넘길 수 있습니다:

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
> Redis를 사용한다면 Redis에 최적화된 `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어를 활용하세요.

<a name="skipping-jobs"></a>
### 잡 건너뛰기 (Skipping Jobs)

`Skip` 미들웨어를 사용하면 잡 로직을 수정하지 않고도 특정 조건에서 잡을 삭제할 수 있습니다. `Skip::when`은 조건이 `true`일 때 잡을 삭제하며, `Skip::unless`는 조건이 `false`일 때 잡을 삭제합니다:

```php
use Illuminate\Queue\Middleware\Skip;

public function middleware(): array
{
    return [
        Skip::when($someCondition),
    ];
}
```

복잡한 조건을 위해서 본문에 `Closure`를 전달할 수 있습니다:

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
## 잡 디스패치하기 (Dispatching Jobs)

잡 클래스를 작성한 뒤, 잡 클래스의 `dispatch` 메서드로 잡을 디스패치할 수 있습니다. `dispatch`에 넘긴 인수는 잡 생성자로 전달됩니다:

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

조건부 디스패치는 `dispatchIf`, `dispatchUnless` 메서드를 쓸 수 있습니다:

```php
ProcessPodcast::dispatchIf($accountActive, $podcast);

ProcessPodcast::dispatchUnless($accountSuspended, $podcast);
```

새 Laravel 애플리케이션의 기본 큐 드라이버는 `sync`입니다. 이 드라이버는 잡을 동기적으로 즉시 실행하며, 로컬 개발 시 편리합니다. 백그라운드 큐 처리를 원한다면 `config/queue.php`에서 다른 큐 드라이버를 설정하세요.

<a name="delayed-dispatching"></a>
### 지연 디스패치 (Delayed Dispatching)

잡을 즉시 실행하지 않고 일정 시간 지연 후 처리하고 싶으면, `delay` 메서드를 체인하여 사용하세요. 아래 예시는 10분 후에만 큐에 잡이 노출됩니다:

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

기본 지연 시간이 설정된 잡도 있는데, 이 기본 지연을 무시하고 즉시 디스패치하려면 `withoutDelay` 메서드를 호출하세요:

```php
ProcessPodcast::dispatch($podcast)->withoutDelay();
```

> [!WARNING]
> Amazon SQS 큐 서비스는 최대 지연 시간이 15분입니다.

<a name="dispatching-after-the-response-is-sent-to-browser"></a>
#### HTTP 응답 후 디스패치하기

FastCGI 웹 서버를 사용할 경우, `dispatchAfterResponse` 메서드는 HTTP 응답이 사용자에게 전송된 이후에 잡 디스패치를 수행합니다. 이로써 사용자는 앱을 곧바로 사용할 수 있고, 잡은 백그라운드로 처리됩니다. 보통 1초 가량 작업하는 이메일 전송 등에서 사용되며, 이 경우 별도 큐 워커 없이도 디스패치된 잡이 처리됩니다:

```php
use App\Jobs\SendNotification;

SendNotification::dispatchAfterResponse();
```

또는 클로저를 디스패치하고 `afterResponse` 메서드로 체이닝할 수도 있습니다:

```php
use App\Mail\WelcomeMessage;
use Illuminate\Support\Facades\Mail;

dispatch(function () {
    Mail::to('taylor@example.com')->send(new WelcomeMessage);
})->afterResponse();
```

<a name="synchronous-dispatching"></a>
### 동기 디스패치 (Synchronous Dispatching)

즉각 동기적으로 잡을 실행하려면 `dispatchSync` 메서드를 씁니다. 이 경우 잡은 큐에 쌓이지 않고 현재 프로세스에서 바로 실행됩니다:

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

데이터베이스 트랜잭션 내에서 잡을 디스패치하는 건 가능하지만, 잡이 제대로 실행할 수 있게 주의를 기울여야 합니다. 트랜잭션 커밋 전에 워커가 잡을 처리하면, 트랜잭션 내에서 만든 변경 내용이나 새 모델이 데이터베이스에 반영되지 않았을 수 있습니다.

이를 해결하기 위한 방법이 여러 가지 있습니다. 첫째, 큐 커넥션 설정 배열에 `after_commit` 옵션을 `true`로 설정할 수 있습니다:

```php
'redis' => [
    'driver' => 'redis',
    // ...
    'after_commit' => true,
],
```

`after_commit`이 `true`면, 트랜잭션이 열린 상태에서는 잡 디스패치가 지연되고, 트랜잭션 커밋이 완료되어야 실제 디스패치됩니다. 예외로 트랜잭션이 롤백되면 디스패치한 잡도 취소됩니다.

> [!NOTE]
> `after_commit`이 `true`면, 큐에 저장된 이벤트 리스너, 메일러, 알림, 브로드캐스트 이벤트도 트랜잭션 커밋 이후에만 발생됩니다.

<a name="specifying-commit-dispatch-behavior-inline"></a>
#### 커밋 디스패치 행동을 인라인으로 지정하기

`after_commit`을 `true`로 설정하지 않은 경우에도 특정 잡을 트랜잭션 커밋 이후에 디스패치하도록 지정할 수 있습니다:

```php
use App\Jobs\ProcessPodcast;

ProcessPodcast::dispatch($podcast)->afterCommit();
```

반대로 `after_commit` 설정이 `true`여도, 특정 잡을 즉시 디스패치하려면 `beforeCommit` 메서드를 호출하세요:

```php
ProcessPodcast::dispatch($podcast)->beforeCommit();
```

<a name="job-chaining"></a>
### 잡 체이닝 (Job Chaining)

잡 체이닝을 사용하면, 주 작업이 성공적으로 실행된 뒤에 실행할 잡들을 순차적으로 지정할 수 있습니다. 체인 중 하나라도 실패하면 나머지는 실행되지 않습니다. `Bus` 파사드의 `chain` 메서드를 사용해 체인을 실행할 수 있습니다:

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

클래스 인스턴스 뿐만 아니라 클로저 체인도 가능합니다:

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
> 체인 내 잡에서 `$this->delete()`를 호출해 잡을 삭제해도 체인 실행은 멈추지 않습니다. 체인이 중단되려면 잡이 실패해야 합니다.

<a name="chain-connection-queue"></a>
#### 체인 잡의 커넥션과 큐

체인 잡들에 사용할 기본 큐 커넥션과 큐를 지정하려면 `onConnection`과 `onQueue` 메서드를 사용하세요. 특정 잡이 별도로 지정하지 않으면 이 값들이 적용됩니다:

```php
Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->onConnection('redis')->onQueue('podcasts')->dispatch();
```

<a name="adding-jobs-to-the-chain"></a>
#### 체인에 잡 추가하기

가끔 체인 내부 잡에서 체인 맨 앞이나 끝에 잡을 추가해야 할 때가 있습니다. `prependToChain`과 `appendToChain` 메서드를 사용합니다:

```php
/**
 * 작업 실행
 */
public function handle(): void
{
    // ...

    // 현재 체인 앞에 잡 추가 - 현재 작업 직후 실행
    $this->prependToChain(new TranscribePodcast);

    // 현재 체인 뒤에 잡 추가 - 체인 마지막에 실행
    $this->appendToChain(new TranscribePodcast);
}
```

<a name="chain-failures"></a>
#### 체인 실패 처리

체인 잡 중 하나가 실패 시 호출할 콜백을 `catch` 메서드로 지정할 수 있습니다. 콜백은 실패 사유가 된 `Throwable` 인스턴스를 받습니다:

```php
use Illuminate\Support\Facades\Bus;
use Throwable;

Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->catch(function (Throwable $e) {
    // 체인 내 잡 중 실패 발생...
})->dispatch();
```

> [!WARNING]
> 체인은 큐에서 직렬화되어 나중에 실행되므로, 콜백 내에서 `$this` 변수를 사용하면 안 됩니다.

<a name="customizing-the-queue-and-connection"></a>
### 큐와 커넥션 커스터마이징 (Customizing the Queue and Connection)

<a name="dispatching-to-a-particular-queue"></a>
#### 특정 큐에 디스패치하기

서로 다른 큐에 잡을 푸시함으로써 작업을 구분하고, 작업 우선순위별 워커 배정도 가능해집니다. 커넥션 설정은 그대로 두고, 잡 디스패치 시 `onQueue` 메서드로 큐 이름을 지정하세요:

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

        ProcessPodcast::dispatch($podcast)->onQueue('processing');

        return redirect('/podcasts');
    }
}
```

또는 잡 생성자에서 `onQueue`를 호출해 기본 큐를 지정할 수도 있습니다:

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    /**
     * 새 잡 인스턴스 생성자
     */
    public function __construct()
    {
        $this->onQueue('processing');
    }
}
```

<a name="dispatching-to-a-particular-connection"></a>
#### 특정 커넥션에 디스패치하기

여러 큐 커넥션을 사용하는 경우, `onConnection` 메서드로 대상 커넥션을 지정할 수 있습니다:

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

        ProcessPodcast::dispatch($podcast)->onConnection('sqs');

        return redirect('/podcasts');
    }
}
```

`onConnection`과 `onQueue`를 함께 체이닝해 지정할 수도 있습니다:

```php
ProcessPodcast::dispatch($podcast)
    ->onConnection('sqs')
    ->onQueue('processing');
```

또는 잡 생성자에서 기본 커넥션을 지정할 수 있습니다:

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    /**
     * 새 잡 인스턴스 생성자
     */
    public function __construct()
    {
        $this->onConnection('sqs');
    }
}
```

<a name="max-job-attempts-and-timeout"></a>
### 최대 재시도 횟수 및 타임아웃 설정 (Specifying Max Job Attempts / Timeout Values)

<a name="max-attempts"></a>
#### 최대 재시도 횟수

잡이 오류를 계속 발생하면 무한 재시도되는 것을 막기 위해 최대 시도 횟수를 설정할 수 있습니다.

커맨드라인 Artisan 명령어 `queue:work`에 `--tries` 옵션을 주면 해당 워커가 처리하는 모든 잡에 기본 적용됩니다. 다만, 잡 클래스에 별도로 최대 재시도 횟수가 지정되어 있으면 그 값이 우선합니다:

```shell
php artisan queue:work --tries=3
```

최대 재시도를 초과하면 잡은 "실패" 처리되고, 실패 잡 관리 문서([#dealing-with-failed-jobs](#dealing-with-failed-jobs))를 참고하세요. `--tries=0`이면 재시도 무한대로 설정됩니다.

잡 클래스에 최대 시도 횟수를 지정하는 방법:

```php
<?php

namespace App\Jobs;

class ProcessPodcast implements ShouldQueue
{
    /**
     * 최대 재시도 횟수
     *
     * @var int
     */
    public $tries = 5;
}
```

다이나믹하게 결정하려면 `tries` 메서드를 정의할 수도 있습니다:

```php
/**
 * 최대 재시도 횟수 반환
 */
public function tries(): int
{
    return 5;
}
```

<a name="time-based-attempts"></a>
#### 시간 기반 재시도 제한

시도 횟수가 아니라 시간 기반으로 재시도 종료 시점을 지정할 수 있습니다. 이렇게 하면 제한 시간 동안은 원하는 만큼 재시도하고, 지정한 시간이 지나면 더 이상 시도하지 않습니다. `retryUntil` 메서드에 `DateTime` 인스턴스를 반환하세요:

```php
use DateTime;

/**
 * 잡 재시도 종료 시점 반환
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(10);
}
```

> [!NOTE]
> 큐에 저장된 이벤트 리스너에도 `tries` 속성이나 `retryUntil` 메서드를 정의할 수 있습니다.

<a name="max-exceptions"></a>
#### 최대 예외 발생 허용 횟수

재시도 횟수는 많지만, 처리 중 발생하는 미처리 예외가 일정 횟수를 넘으면 실패 처리하고 싶으면 잡 클래스에 `maxExceptions` 속성을 선언하세요:

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
     * 최대 허용 예외 횟수
     *
     * @var int
     */
    public $maxExceptions = 3;

    /**
     * 작업 실행
     */
    public function handle(): void
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

이 예시에서 10초 대기 후 재시도하며 최대 25번 시도하지만, 3회 미처리 예외가 발생하면 즉시 실패 처리됩니다.

<a name="timeout"></a>
#### 타임아웃

잡 실행 예상 시간을 기준으로 타임아웃을 설정할 수 있습니다. 기본값은 60초이며, 이 시간을 초과해 실행 중인 잡의 워커 프로세스는 에러와 함께 종료됩니다. 종료된 워커는 일반적으로 프로세스 관리자에 의해 자동 재시작됩니다.

`queue:work` 커맨드에서 `--timeout` 옵션으로 타임아웃 값을 설정할 수 있습니다:

```shell
php artisan queue:work --timeout=30
```

잡 클래스에 `$timeout` 속성을 선언해 잡별 제한 시간을 지정할 수도 있습니다. 클래스 속성 설정이 커맨드라인 옵션보다 우선합니다:

```php
<?php

namespace App\Jobs;

class ProcessPodcast implements ShouldQueue
{
    /**
     * 잡의 최대 실행 시간 (초)
     *
     * @var int
     */
    public $timeout = 120;
}
```

네트워크 소켓, 외부 HTTP 연결 등 IO 차단 작업은 PHP 타임아웃을 무시할 수 있으니, 해당 라이브러리의 API 기반 타임아웃 설정도 함께 사용하세요.

> [!WARNING]
> 작업 타임아웃 기능은 `pcntl` PHP 확장 설치가 필요합니다. 또한 잡의 타임아웃 시간은 큐 설정 중 `retry_after` 값보다 짧아야 합니다. 그렇지 않으면 작업 완료 전에 잡이 재시도될 수 있습니다.

<a name="failing-on-timeout"></a>
#### 타임아웃 시 실패 처리

잡이 타임아웃 시 실패로 처리되도록 하려면 `$failOnTimeout` 속성을 `true`로 지정하세요:

```php
/**
 * 타임아웃 시 잡을 실패 처리할지 여부
 *
 * @var bool
 */
public $failOnTimeout = true;
```

<a name="error-handling"></a>
### 오류 처리 (Error Handling)

잡 실행 중 예외가 발생하면, 잡은 자동으로 다시 큐에 재배치되어 재시도됩니다. 재시도 횟수는 `queue:work` 커맨드의 `--tries` 옵션이나 잡 클래스의 재시도 설정에 의해 제한됩니다. 워커 실행과 관련한 자세한 내용은 [큐 워커 실행하기](#running-the-queue-worker) 섹션을 참고하세요.

<a name="manually-releasing-a-job"></a>
#### 수동으로 잡 재배치하기

직접 잡을 다시 큐로 재배치해 나중에 재시도하도록 만들고 싶으면 잡 내에서 `release` 메서드를 호출하세요:

```php
/**
 * 작업 실행
 */
public function handle(): void
{
    // ...

    $this->release();
}
```

기본적으로 `release`는 즉시 큐에 재배치하지만, 정수나 날짜를 넘기면 해당 시간 동안 대기 후 재배치합니다:

```php
$this->release(10);

$this->release(now()->addSeconds(10));
```

<a name="manually-failing-a-job"></a>
#### 수동으로 잡 실패 처리하기

잡을 수동으로 실패 처리하려면 `fail` 메서드를 호출하세요:

```php
/**
 * 작업 실행
 */
public function handle(): void
{
    // ...

    $this->fail();
}
```

잡 실패 이유가 된 예외를 인자로 넘기거나, 에러 메시지 문자열을 넘길 수도 있습니다 (내부에서 예외로 변환):

```php
$this->fail($exception);

$this->fail('Something went wrong.');
```

> [!NOTE]
> 실패 잡 관련 추가 정보는 [실패 잡 처리](#dealing-with-failed-jobs) 섹션을 참고하세요.

<a name="job-batching"></a>
## 잡 배칭 (Job Batching)

Laravel의 잡 배칭 기능은 여러 잡을 그룹으로 실행하고, 전체 배치 완료 시 후속 동작을 수행하도록 도와줍니다. 시작 전, 잡 배치 메타 정보를 저장할 데이터베이스 테이블을 생성하는 마이그레이션을 만들어야 합니다. `make:queue-batches-table` Artisan 명령어로 생성 후 마이그레이션 실행:

```shell
php artisan make:queue-batches-table

php artisan migrate
```

<a name="defining-batchable-jobs"></a>
### 배치 가능한 잡 정의하기

배치 잡을 정의하려면 일반 잡을 생성하되 `Illuminate\Bus\Batchable` 트레이트를 추가하세요. 이 트레이트는 현재 잡이 포함된 배치 정보를 반환하는 `batch` 메서드를 제공합니다:

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
     * 작업 실행
     */
    public function handle(): void
    {
        if ($this->batch()->cancelled()) {
            // 배치가 취소된 상태면 중지...

            return;
        }

        // CSV 파일 일부를 임포트...
    }
}
```

<a name="dispatching-batches"></a>
### 배치 디스패치 (Dispatching Batches)

잡 배치는 `Bus` 파사드의 `batch` 메서드로 작성합니다. 주로 완료 콜백(`then`, `catch`, `finally`)과 함께 사용됩니다. 각 콜백은 실행 시점에 `Illuminate\Bus\Batch` 인스턴스를 인자로 받습니다.

아래 예시에서는 CSV 파일 일부 블록을 처리하는 여러 잡을 배치에 넣고, 다양한 콜백으로 배치 상태를 관리합니다:

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
    // 배치 생성됐지만 잡이 아직 없음
})->progress(function (Batch $batch) {
    // 개별 잡이 완료됨
})->then(function (Batch $batch) {
    // 모든 잡이 성공적으로 종료됨
})->catch(function (Batch $batch, Throwable $e) {
    // 배치 내 첫 잡 실패 감지됨
})->finally(function (Batch $batch) {
    // 배치 실행 완료됨
})->dispatch();

return $batch->id;
```

배치 ID는 `$batch->id` 프로퍼티로 접근 가능하며, 나중에 [Laravel 명령 버스 쿼리](#inspecting-batches)에 사용합니다.

> [!WARNING]
> 콜백은 큐 직렬화되어 나중에 실행되므로 콜백 내에서 `$this` 변수 사용을 피하고, 트랜잭션 내에서 암묵적 커밋을 발생시키는 DB 문은 피하세요.

<a name="naming-batches"></a>
#### 배치 이름 붙이기

Laravel Horizon, Telescope 같은 도구들이 배치에 이름이 있으면 더 친숙한 디버깅 정보를 제공합니다. 배치 정의 시 `name` 메서드로 임의 이름을 지정하세요:

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // 모든 잡 완료
})->name('Import CSV')->dispatch();
```

<a name="batch-connection-queue"></a>
#### 배치용 커넥션과 큐

배치 잡 전체에 사용할 커넥션과 큐를 지정하려면 `onConnection`과 `onQueue` 메서드를 사용하세요. 모든 배치 잡은 같은 커넥션과 큐를 써야 합니다:

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // 모든 잡 완료
})->onConnection('redis')->onQueue('imports')->dispatch();
```

<a name="chains-and-batches"></a>
### 체인과 배치 (Chains and Batches)

배치 내에 잡 체인을 포함시킬 수 있습니다. 예를 들어, 두 개 이상의 잡 체인을 병렬로 실행하고 양쪽이 완료되면 콜백을 실행:

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

반대로, 잡 체인 내에 배치를 포함시키는 것도 가능합니다. 예를 들어, 여러 팟캐스트 릴리즈 배치와 알림 배치를 순차 실행:

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

많은 잡을 웹 요청처럼 짧은 시간에 디스패치가 어려울 때, "로더" 잡을 이용해 배치에 잡을 동적으로 추가할 수 있습니다:

```php
$batch = Bus::batch([
    new LoadImportBatch,
    new LoadImportBatch,
    new LoadImportBatch,
])->then(function (Batch $batch) {
    // 모든 잡 정상 종료
})->name('Import Contacts')->dispatch();
```

`LoadImportBatch` 잡 내에서 현재 배치에 새 잡을 추가하려면, `batch` 메서드로 배치 인스턴스를 얻고 `add` 메서드로 잡을 추가합니다:

```php
use App\Jobs\ImportContacts;
use Illuminate\Support\Collection;

/**
 * 작업 실행
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
> 같은 배치에 속한 잡 내부에서만 배치에 잡을 추가할 수 있습니다.

<a name="inspecting-batches"></a>
### 배치 검사하기 (Inspecting Batches)

콜백에 전달되는 `Illuminate\Bus\Batch` 인스턴스는 다양한 프로퍼티와 메서드를 제공해 배치 상태를 조회하거나 작업할 수 있습니다:

```php
// 배치 UUID
$batch->id;

// 배치 이름 (있다면)
$batch->name;

// 배치에 배정된 총 잡 수
$batch->totalJobs;

// 아직 처리되지 않은 잡 수
$batch->pendingJobs;

// 실패한 잡 수
$batch->failedJobs;

// 지금까지 처리한 잡 수
$batch->processedJobs();

// 배치 완료 비율 (0~100)
$batch->progress();

// 배치 실행이 완료되었는지 여부
$batch->finished();

// 배치 실행 취소
$batch->cancel();

// 배치가 취소되었는지 여부
$batch->cancelled();
```

<a name="returning-batches-from-routes"></a>
#### 라우트에서 배치 반환하기

`Illuminate\Bus\Batch` 인스턴스는 JSON 직렬화를 지원해, 라우트에서 직접 반환하면 배치 진행 상태 등 JSON 데이터로 바로 노출할 수 있습니다.

ID로 배치를 조회하려면 `Bus` 파사드의 `findBatch` 메서드를 사용하세요:

```php
use Illuminate\Support\Facades\Bus;
use Illuminate\Support\Facades\Route;

Route::get('/batch/{batchId}', function (string $batchId) {
    return Bus::findBatch($batchId);
});
```

<a name="cancelling-batches"></a>
### 배치 취소하기 (Cancelling Batches)

배치 실행을 취소하려면 `Illuminate\Bus\Batch` 인스턴스의 `cancel` 메서드를 호출하면 됩니다:

```php
/**
 * 작업 실행
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

또는 `SkipIfBatchCancelled` 미들웨어를 잡 미들웨어로 지정해, 배치가 취소된 잡은 자동으로 처리하지 않게 할 수 있습니다:

```php
use Illuminate\Queue\Middleware\SkipIfBatchCancelled;

/**
 * 통과할 미들웨어 반환
 */
public function middleware(): array
{
    return [new SkipIfBatchCancelled];
}
```

<a name="batch-failures"></a>
### 배치 실패 (Batch Failures)

배치 잡이 실패하면, `catch` 콜백이 호출됩니다. 이 콜백은 배치 내 첫 번째 실패 잡에서만 실행됩니다.

<a name="allowing-failures"></a>
#### 실패 허용 설정

기본적으로 배치 내 잡이 하나라도 실패하면, Laravel이 자동으로 배치를 "취소" 상태로 표시합니다. 실패해도 배치 취소하지 않으려면 배치 디스패치 시 `allowFailures` 메서드를 호출하세요:

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // 모든 잡 정상 완료
})->allowFailures()->dispatch();
```

<a name="retrying-failed-batch-jobs"></a>
#### 실패 배치 잡 재시도

특정 배치의 모든 실패 잡을 재시도하려면 `queue:retry-batch` Artisan 명령어를 사용하세요. 배치 UUID를 인자로 받습니다:

```shell
php artisan queue:retry-batch 32dbc76c-4f82-4749-b610-a639fe0099b5
```

여러 UUID를 한꺼번에 넘기거나 특정 큐의 실패 잡을 재시도할 수도 있습니다.

<a name="pruning-batches"></a>
### 배치 기록 정리하기 (Pruning Batches)

`job_batches` 테이블이 점차 쌓이므로, Artisan `queue:prune-batches` 명령을 매일 실행 예약하는 것을 권장합니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches')->daily();
```

기본적으로 24시간 지난 완료된 배치가 삭제됩니다. `--hours` 옵션으로 유지 기간을 조절할 수 있습니다:

```php
Schedule::command('queue:prune-batches --hours=48')->daily();
```

실패하여 완료하지 못한 미완료 배치나 취소된 배치도 제거하려면 `--unfinished` 및 `--cancelled` 옵션을 지정하세요:

```php
Schedule::command('queue:prune-batches --hours=48 --unfinished=72')->daily();

Schedule::command('queue:prune-batches --hours=48 --cancelled=72')->daily();
```

<a name="storing-batches-in-dynamodb"></a>
### DynamoDB에 배치 저장하기 (Storing Batches in DynamoDB)

Laravel은 배치 메타 정보 저장에 관계형 DB 대신 [DynamoDB](https://aws.amazon.com/dynamodb)를 사용할 수 있습니다. 다만 해당 테이블은 직접 생성해야 합니다.

보통 테이블 이름은 `job_batches`이며, 설정 파일 `queue.batching.table` 값에 맞춰 바꿀 수 있습니다.

<a name="dynamodb-batch-table-configuration"></a>
#### DynamoDB 배치 테이블 구성

`job_batches` 테이블은 문자열 파티션 키로 `application`, 정렬 키로 `id`를 가져야 합니다. `application`은 `app.php` 설정의 `name` 값입니다. 다수 Laravel 애플리케이션이 같은 테이블을 공유해서 사용할 수 있습니다.

자동 배치 정리를 위해 `ttl` 속성을 정의할 수도 있습니다.

<a name="dynamodb-configuration"></a>
#### DynamoDB 구성

AWS SDK를 설치해 DynamoDB와 통신 가능하도록 합니다:

```shell
composer require aws/aws-sdk-php
```

`queue.batching.driver` 설정을 `dynamodb`로 지정하고, `key`, `secret`, `region` 설정을 지정하세요. `queue.batching.database` 옵션은 필요 없습니다:

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

관례적으로 관계형 DB 전용 `queue:prune-batches` 명령은 DynamoDB 저장 배치에 적용되지 않습니다. 대신 DynamoDB의 TTL 기능을 사용해 오래된 레코드를 자동 삭제하세요.

`queue.batching.ttl_attribute` 설정에 TTL 속성 이름, `queue.batching.ttl`에 보관 기간(초)을 지정합니다:

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

잡 클래스를 사용하는 대신, 클로저를 큐에 디스패치할 수도 있습니다. 짧고 단순한 작업에 적합합니다. 디스패치하는 클로저는 변조 방지를 위해 암호화된 서명이 붙습니다:

```php
$podcast = App\Podcast::find(1);

dispatch(function () use ($podcast) {
    $podcast->publish();
});
```

`catch` 메서드로 실패 시 실행할 클로저를 지정할 수 있습니다:

```php
use Throwable;

dispatch(function () use ($podcast) {
    $podcast->publish();
})->catch(function (Throwable $e) {
    // 이 잡은 실패함...
});
```

> [!WARNING]
> `catch` 콜백도 큐 직렬화되어 나중에 실행되므로, `$this` 변수 사용을 피하세요.

<a name="running-the-queue-worker"></a>
## 큐 워커 실행하기 (Running the Queue Worker)

<a name="the-queue-work-command"></a>
### `queue:work` 명령어

Laravel은 큐 워커를 시작해 새 잡이 쌓일 때 자동으로 처리하는 Artisan 커맨드를 제공합니다. 워커는 수동 중지 전까지 계속 실행됩니다:

```shell
php artisan queue:work
```

> [!NOTE]
> 워커 프로세스를 항상 백그라운드에서 유지하려면, [Supervisor](#supervisor-configuration)와 같은 프로세스 모니터를 사용하세요.

`-v` 옵션을 사용하면 처리되는 잡 ID가 출력됩니다:

```shell
php artisan queue:work -v
```

큐 워커는 주기적으로 애플리케이션을 재부팅하지 않아 변화된 코드를 자동 감지하지 못합니다. 따라서 배포 시 [워크 재시작](#queue-workers-and-deployment)이 필요합니다. 애플리케이션의 정적 상태도 작업 간 초기화되지 않습니다.

비효율적이지만 코드 변경 시 워커 자동 재시작 기능이 필요한 경우 `queue:listen` 명령어를 사용할 수 있습니다:

```shell
php artisan queue:listen
```

<a name="running-multiple-queue-workers"></a>
#### 여러 워커 실행하기

동시에 여러 워커를 실행하려면 단순히 여러 개의 `queue:work` 프로세스를 시작하세요. 로컬에서는 여러 터미널 탭을 열고, 생산 환경에서는 프로세스 관리자의 설정을 사용합니다. [Supervisor 설정](#supervisor-configuration) 시 `numprocs` 옵션 활용 가능.

<a name="specifying-the-connection-queue"></a>
#### 커넥션과 큐 지정

워커가 사용할 큐 커넥션 이름을 지정할 수 있습니다. 이름은 `config/queue.php`의 설정과 일치해야 합니다:

```shell
php artisan queue:work redis
```

기본적으로 지정된 커넥션의 기본 큐만 처리하지만, 큐 이름을 콤마로 구분해 여러 큐를 지정할 수도 있습니다:

```shell
php artisan queue:work redis --queue=emails
```

<a name="processing-a-specified-number-of-jobs"></a>
#### 지정한 잡만 처리하기

`--once` 옵션으로 워커가 큐에서 한 개 잡만 처리하고 종료하도록 할 수 있습니다:

```shell
php artisan queue:work --once
```

`--max-jobs` 옵션으로 워커가 지정한 횟수만큼 잡을 처리한 후 종료하게 할 수 있습니다. 메모리 누수 방지를 위해 프로세스 모니터와 함께 쓰입니다:

```shell
php artisan queue:work --max-jobs=1000
```

<a name="processing-all-queued-jobs-then-exiting"></a>
#### 큐에 남은 잡 모두 처리 후 종료

`--stop-when-empty` 옵션으로 큐에 남은 모든 잡을 처리하고 워커를 종료할 수 있습니다. Docker 기반 배포 시 유용합니다:

```shell
php artisan queue:work --stop-when-empty
```

<a name="processing-jobs-for-a-given-number-of-seconds"></a>
#### 지정 시간을 기준으로 잡 처리 후 종료

`--max-time` 옵션으로 지정 초 수 동안만 잡을 처리하다 종료할 수 있습니다. 프로세스 모니터와의 조합으로 메모리 누수를 완화할 때 유용합니다:

```shell
# 1시간간 잡 처리
php artisan queue:work --max-time=3600
```

<a name="worker-sleep-duration"></a>
#### 워커의 대기 시간

잡이 없을 때 워커가 잠자는 시간을 `sleep` 옵션으로 초 단위 지정할 수 있습니다:

```shell
php artisan queue:work --sleep=3
```

잠자는 동안에는 잡을 처리하지 않습니다.

<a name="maintenance-mode-queues"></a>
#### 유지보수 모드와 큐

애플리케이션이 [유지보수 모드](/docs/master/configuration#maintenance-mode)일 땐 큐 잡을 처리하지 않습니다. 모드 해제 시 다시 정상 처리됩니다.

강제로 유지보수 모드여도 잡을 처리하려면 `--force` 옵션을 사용하세요:

```shell
php artisan queue:work --force
```

<a name="resource-considerations"></a>
#### 리소스 고려사항

큐 워커는 데몬 프로세스로, 잡 실행 후 프레임워크를 매번 재부팅하지 않습니다. 따라서 이미지 처럼 무거운 리소스는 잡 실행 후 반드시 해제해야 합니다 (`imagedestroy` 같은 함수 이용).

<a name="queue-priorities"></a>
### 큐 우선순위 설정 (Queue Priorities)

여러 큐 우선순위를 다루려면, 예를 들어 `config/queue.php`에서 Redis 커넥션 기본 큐를 ‘low’로 설정하고, 중요한 잡은 ‘high’ 큐로 푸시할 수 있습니다:

```php
dispatch((new Job)->onQueue('high'));
```

`queue:work`를 다음처럼 실행하면 모든 ‘high’ 큐 잡을 먼저 처리합니다:

```shell
php artisan queue:work --queue=high,low
```

<a name="queue-workers-and-deployment"></a>
### 큐 워커와 배포 (Queue Workers and Deployment)

큐 워커는 장시간 실행하는 프로세스라, 코드 변경을 직접 감지하지 못합니다. 따라서 배포 시 워커를 재시작해야 합니다. 사용자 요청 처리 중 작업이 날아가지 않도록, `queue:restart` 명령으로 워커들에게 현재 잡 완료 후 종료하라는 신호를 보낼 수 있습니다:

```shell
php artisan queue:restart
```

워커가 종료되면 Supervisor 같은 프로세스 관리자가 자동 재시작합니다.

> [!NOTE]
> 워커 재시작 신호는 [캐시 시스템](/docs/master/cache)을 통해 전달되므로, 적절한 캐시 드라이버 설정이 꼭 필요합니다.

<a name="job-expirations-and-timeouts"></a>
### 잡 만료와 타임아웃 (Job Expirations and Timeouts)

<a name="job-expiration"></a>
#### 잡 만료

`config/queue.php` 각 큐 커넥션에 `retry_after` 옵션이 있습니다. 이 값은 잡 처리 중  지정한 초만큼 신호가 없으면 해당 잡을 재시도하도록 큐가 판단하는 시간입니다.  예를 들어 기본값 90초면, 워커가 90초 넘게 잡을 완료하고 다음 작업으로 옮기지 못하면 잡이 다시 큐에 쌓입니다.

> [!WARNING]
> Amazon SQS는 `retry_after` 설정이 없으며, AWS 콘솔 내 [기본 가시성 타임아웃](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/AboutVT.html)에 의해 재시도가 관리됩니다.

<a name="worker-timeouts"></a>
#### 워커 타임아웃

`queue:work` 명령어의 `--timeout` 옵션 값은 기본 60초입니다. 이 시간을 초과해 잡을 처리 중인 워커는 에러를 내고 종료하며, 보통 프로세스 관리자에 의해 자동 재실행됩니다:

```shell
php artisan queue:work --timeout=60
```

`retry_after`와 `--timeout` 옵션은 서로 다르지만, 함께 잡 유실 방지 및 중복 처리를 조절합니다.

> [!WARNING]
> `--timeout` 값은 `retry_after` 값보다 항상 짧아야 합니다. 그래야 실행 중인 워커가 타임아웃으로 종료된 후 잡이 재시도됩니다. `--timeout`이 더 길면 잡이 중복 실행될 수 있습니다.

<a name="supervisor-configuration"></a>
## Supervisor 설정

운영 환경에서 워커를 계속 실행하려면, 워커가 중단될 경우 자동 재시작할 프로세스 모니터가 필요합니다. 워커가 중단되는 이유는 워커 타임아웃 초과, `queue:restart` 명령 실행 등 다양합니다.

Supervisor는 Linux 환경에서 많이 쓰이며, 워커 프로세스를 감시하고 관리하는 역할을 합니다.

<a name="installing-supervisor"></a>
#### Supervisor 설치

Ubuntu에서 Supervisor를 설치하려면:

```shell
sudo apt-get install supervisor
```

> [!NOTE]
> 직접 Supervisor 설정이 어렵다면, Laravel에서 제공하는 [Laravel Cloud](https://cloud.laravel.com)를 이용하면 완전 관리형 플랫폼으로 워커를 운영할 수 있습니다.

<a name="configuring-supervisor"></a>
#### Supervisor 설정

설정 파일은 `/etc/supervisor/conf.d`에 위치합니다. 워커 프로세스를 실행하는 `laravel-worker.conf` 예시는 다음과 같습니다:

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

`numprocs`는 워커 프로세스를 8개 띄워 관리하라는 의미입니다. 워커 옵션에 맞게 `command`는 적절히 변경해 주세요.

> [!WARNING]
> `stopwaitsecs` 값은 가장 오래 걸리는 잡 처리 시간보다 크게 설정하세요. 그렇지 않으면 작업 중인 잡이 강제로 종료될 수 있습니다.

<a name="starting-supervisor"></a>
#### Supervisor 시작

설정 파일 변경 후 Supervisor를 재로드하고 워커를 시작하려면:

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start "laravel-worker:*"
```

자세한 내용은 [Supervisor 공식 문서](http://supervisord.org/index.html)를 참고하세요.

<a name="dealing-with-failed-jobs"></a>
## 실패 잡 처리 (Dealing With Failed Jobs)

잡이 반복 실패할 때가 있습니다. Laravel은 최대 재시도 횟수를 지정해 이를 제한하고, 실패 잡은 `failed_jobs` 테이블에 기록합니다. 동기 실행 잡은 실패 시 즉시 예외를 처리하며 테이블에 기록하지 않습니다.

기본 새 Laravel 앱에 실패 잡 테이블 마이그레이션이 포함되지만, 없으면 `make:queue-failed-table` 명령어로 생성할 수 있습니다:

```shell
php artisan make:queue-failed-table

php artisan migrate
```

워커 실행 시 최대 재시도 횟수를 `--tries` 옵션으로 지정할 수 있으며, 지정 없으면 잡 클래스 속성이 기본입니다:

```shell
php artisan queue:work redis --tries=3
```

`--backoff` 옵션을 주어 실패 시 재시도 전 대기 시간을 지정할 수 있습니다 (기본 즉시 재시도):

```shell
php artisan queue:work redis --tries=3 --backoff=3
```

잡 단위로도 `backoff` 속성이나 메서드를 정의하여 대기 시간 동작을 제어할 수 있습니다:

```php
/**
 * 재시도 전 대기 시간(초)
 *
 * @var int
 */
public $backoff = 3;
```

복잡한 대기시간 로직은 `backoff` 메서드로 구현할 수 있습니다:

```php
/**
 * 재시도 전 대기 시간을 배열로 반환 (초 단위)
 *
 * @return array<int, int>
 */
public function backoff(): array
{
    return [1, 5, 10];
}
```

이 예시는 첫 재시도는 1초, 두 번째는 5초, 그 후는 10초씩 대기함을 의미합니다.

<a name="cleaning-up-after-failed-jobs"></a>
### 실패 잡 정리 (Cleaning Up After Failed Jobs)

잡 실패 시 사용자 알림, 롤백 같은 후처리를 위해 잡 클래스에 `failed` 메서드를 정의할 수 있습니다. 실패 사유인 `Throwable` 인자를 받습니다:

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
     * 새 잡 인스턴스 생성자
     */
    public function __construct(
        public Podcast $podcast,
    ) {}

    /**
     * 작업 실행
     */
    public function handle(AudioProcessor $processor): void
    {
        // 팟캐스트 처리...
    }

    /**
     * 잡 실패 시 처리
     */
    public function failed(?Throwable $exception): void
    {
        // 실패 알림 전송 등...
    }
}
```

> [!WARNING]
> `failed`가 호출되기 전 잡 인스턴스가 새로 생성되어, `handle` 중 변경된 프로퍼티는 반영되지 않습니다.

<a name="retrying-failed-jobs"></a>
### 실패 잡 재시도 (Retrying Failed Jobs)

`failed_jobs` 테이블에 저장된 실패 잡 목록을 보려면 `queue:failed` 명령어를 쓰세요:

```shell
php artisan queue:failed
```

나열된 잡 ID를 사용해 재시도할 수 있습니다:

```shell
php artisan queue:retry ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece
```

여러 ID와 특정 큐 지정 재시도도 가능합니다:

```shell
php artisan queue:retry ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece 91401d2c-0784-4f43-824c-34f94a33c24d

php artisan queue:retry --queue=name
```

모든 실패 잡을 재시도하려면 ID로 `all`을 넘기세요:

```shell
php artisan queue:retry all
```

실패 잡을 삭제하려면 `queue:forget` 명령어를 사용합니다:

```shell
php artisan queue:forget 91401d2c-0784-4f43-824c-34f94a33c24d
```

> [!NOTE]
> Horizon 사용 시 실패 잡 삭제는 `horizon:forget` 명령어를 쓰세요.

모든 실패 잡을 삭제하려면 `queue:flush` 명령어를 사용합니다:

```shell
php artisan queue:flush
```

<a name="ignoring-missing-models"></a>
### 삭제된 모델 무시하기 (Ignoring Missing Models)

잡에서 Eloquent 모델을 주입하면, 큐에 넣을 때 모델이 직렬화되고 작업 처리 시 DB에서 다시 조회합니다. 잡 처리 중 모델이 삭제되었다면 `ModelNotFoundException` 예외가 던져질 수 있습니다.

이때 잡 클래스에 `deleteWhenMissingModels` 속성을 `true`로 지정하면, 모델이 없으면 예외 없이 잡을 조용히 폐기합니다:

```php
/**
 * 모델이 없으면 잡을 삭제함
 *
 * @var bool
 */
public $deleteWhenMissingModels = true;
```

<a name="pruning-failed-jobs"></a>
### 실패 잡 기록 정리 (Pruning Failed Jobs)

`queue:prune-failed` 명령어로 오래된 실패 잡 기록을 정리할 수 있습니다:

```shell
php artisan queue:prune-failed
```

기본으론 24시간 지난 실패 잡이 삭제됩니다. `--hours` 옵션으로 유지 기간을 조절할 수 있습니다:

```php
php artisan queue:prune-failed --hours=48
```

<a name="storing-failed-jobs-in-dynamodb"></a>
### DynamoDB에 실패 잡 저장하기 (Storing Failed Jobs in DynamoDB)

실패 잡도 관계형 DB 대신 [DynamoDB](https://aws.amazon.com/dynamodb)에 저장할 수 있습니다. 실패 잡 레코드 저장용 DynamoDB 테이블은 수동 생성해야 하며, 보통 `failed_jobs` 이름입니다.

테이블은 문자열 파티션 키 `application`, 정렬 키 `uuid`가 필요합니다. `application`은 앱 이름(`app` 설정 내 `name`)입니다. 여러 Laravel 애플리케이션에서 같은 테이블 공유 가능.

AWS SDK 설치:

```shell
composer require aws/aws-sdk-php
```

`queue.failed.driver` 설정을 `dynamodb`로 변경하고, `key`, `secret`, `region`을 설정합니다:

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

실패 잡 저장을 원하지 않으면 `queue.failed.driver` 설정을 `null`로 지정하세요. `.env` 환경변수 `QUEUE_FAILED_DRIVER=null`로 설정할 수 있습니다:

```ini
QUEUE_FAILED_DRIVER=null
```

<a name="failed-job-events"></a>
### 실패 잡 이벤트 (Failed Job Events)

잡 실패 시점에 이벤트를 수신하려면 `Queue` 파사드의 `failing` 메서드를 사용합니다. 예를 들어 `AppServiceProvider` `boot` 메서드에서 등록할 수 있습니다:

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
## 큐에서 잡 삭제하기 (Clearing Jobs From Queues)

> [!NOTE]
> Horizon 사용 시 큐 내 잡 삭제는 `horizon:clear` 명령어를 사용하세요.

기본 커넥션 기본 큐의 잡 전체를 삭제하려면 `queue:clear` 명령어를 실행합니다:

```shell
php artisan queue:clear
```

특정 커넥션과 큐를 지정해 삭제할 수도 있습니다:

```shell
php artisan queue:clear redis --queue=emails
```

> [!WARNING]
> 이 기능은 SQS, Redis, 데이터베이스 드라이버만 지원하며, SQS 메시지 삭제는 최대 60초 걸립니다. 그러므로 큐를 비운 후 60초 이내 잡이 삭제될 수 있습니다.

<a name="monitoring-your-queues"></a>
## 큐 모니터링 (Monitoring Your Queues)

단기간 잡이 급증하면 작업 지연이 길어질 수 있습니다. Laravel은 특정 잡 수 임계치를 넘어가면 알림을 보낼 수 있게 지원합니다.

`queue:monitor` 명령어를 1분마다 스케줄에 등록하세요. 큐 이름과 임계 임을 파라미터로 받습니다:

```shell
php artisan queue:monitor redis:default,redis:deployments --max=100
```

이 명령어가 임계치 초과 큐를 탐지하면 `Illuminate\Queue\Events\QueueBusy` 이벤트가 발생합니다. 이를 앱에서 수신해 알림을 보낼 수 있습니다:

```php
use App\Notifications\QueueHasLongWaitTime;
use Illuminate\Queue\Events\QueueBusy;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\Facades\Notification;

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

잡 디스패치 코드를 테스트할 때 잡 실행은 하지 않고, 잡이 큐에 올려진 사실만 검증하고 싶을 수 있습니다. 잡 자체 테스트는 잡 인스턴스 생성 및 `handle` 메서드를 직접 호출해 독립적으로 할 수 있습니다.

`Queue` 파사드의 `fake` 메서드로 큐 실제 동작을 중단하고, 이후에 큐에 푸시한 잡을 검증할 수 있습니다:

```php tab=Pest
<?php

use App\Jobs\AnotherJob;
use App\Jobs\FinalJob;
use App\Jobs\ShipOrder;
use Illuminate\Support\Facades\Queue;

test('orders can be shipped', function () {
    Queue::fake();

    // 주문 배송 작업 수행...

    // 큐에 푸시된 잡이 없었음을 검증
    Queue::assertNothingPushed();

    // 특정 큐에 특정 잡이 푸시되었는지 검증
    Queue::assertPushedOn('queue-name', ShipOrder::class);

    // 특정 잡이 두 번 푸시되었는지 검증
    Queue::assertPushed(ShipOrder::class, 2);

    // 특정 잡이 푸시되지 않았음을 검증
    Queue::assertNotPushed(AnotherJob::class);

    // 클로저 잡이 푸시되었는지 검증
    Queue::assertClosurePushed();

    // 전체 푸시된 잡 수 검증
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

        // 주문 배송 작업 수행...

        Queue::assertNothingPushed();

        Queue::assertPushedOn('queue-name', ShipOrder::class);

        Queue::assertPushed(ShipOrder::class, 2);

        Queue::assertNotPushed(AnotherJob::class);

        Queue::assertClosurePushed();

        Queue::assertCount(3);
    }
}
```

`assertPushed`나 `assertNotPushed`에 클로저를 넘기면, 클로저 내 조건을 만족하는 잡이 푸시되었는지 검사할 수 있습니다:

```php
Queue::assertPushed(function (ShipOrder $job) use ($order) {
    return $job->order->id === $order->id;
});
```

<a name="faking-a-subset-of-jobs"></a>
### 일부 잡만 가짜 처리하기

특정 잡만 가짜 처리하고 나머지는 정상 동작하도록 하려면, `fake` 메서드에 잡 클래스 배열을 넘기세요:

```php tab=Pest
test('orders can be shipped', function () {
    Queue::fake([
        ShipOrder::class,
    ]);

    // ...

    Queue::assertPushed(ShipOrder::class, 2);
});
```

그 반대로, 특정 잡만 제외하고 모두 가짜 처리하려면 `except` 메서드를 사용하세요:

```php
Queue::fake()->except([
    ShipOrder::class,
]);
```

<a name="testing-job-chains"></a>
### 잡 체인 테스트하기

잡 체인은 `Bus` 파사드의 가짜 처리 기능을 써야 합니다. `assertChained` 메서드는 디스패치된 잡 체인 배열을 인자로 받아 체인 실행을 검증합니다:

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

직접 잡 인스턴스 배열을 전달할 수도 있으며, 이 경우 클래스 뿐 아니라 프로퍼티 값도 검사합니다:

```php
Bus::assertChained([
    new ShipOrder,
    new RecordShipment,
    new UpdateInventory,
]);
```

체인 없는 디스패치를 검증하려면 `assertDispatchedWithoutChain` 메서드를 사용합니다:

```php
Bus::assertDispatchedWithoutChain(ShipOrder::class);
```

<a name="testing-chain-modifications"></a>
#### 체인 수정 테스트하기

체인 중 잡에서 체인 앞뒤로 잡을 추가하는 경우, 잡 인스턴스의 `assertHasChain` 메서드로 예상 체인을 검증할 수 있습니다:

```php
$job = new ProcessPodcast;

$job->handle();

$job->assertHasChain([
    new TranscribePodcast,
    new OptimizePodcast,
    new ReleasePodcast,
]);
```

남은 체인이 비어있는지도 `assertDoesntHaveChain`으로 검증 가능:

```php
$job->assertDoesntHaveChain();
```

<a name="testing-chained-batches"></a>
#### 체인 내 배치 테스트하기

잡 체인 내에 배치가 있다면, 체인 배열에 `Bus::chainedBatch` 정의를 넣어 검증할 수 있습니다:

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
### 잡 배치 테스트하기

`Bus` 파사드의 `assertBatched` 메서드는 잡 배치가 정상 디스패치되었는지 확인합니다. 클로저 인자는 `Illuminate\Bus\PendingBatch` 인스턴스를 받으며, 잡 상태와 수를 검사할 수 있습니다:

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

특정 배치 수를 검증하려면 `assertBatchCount`를 씁니다:

```php
Bus::assertBatchCount(3);
```

배치가 하나도 없음을 검증하려면 `assertNothingBatched`를 사용합니다:

```php
Bus::assertNothingBatched();
```

<a name="testing-job-batch-interaction"></a>
#### 잡과 배치 상호작용 테스트하기

잡 내부에서 배치 상태를 조작하는 케이스가 있다면, `withFakeBatch` 메서드로 가짜 배치 인스턴스를 할당해 테스트할 수 있습니다:

```php
[$job, $batch] = (new ShipOrder)->withFakeBatch();

$job->handle();

$this->assertTrue($batch->cancelled());
$this->assertEmpty($batch->added);
```

<a name="testing-job-queue-interactions"></a>
### 잡과 큐 상호작용 테스트

잡이 스스로 재배치하거나 삭제하는 상호작용을 테스트하려면, 잡 인스턴스에 `withFakeQueueInteractions`를 호출하여 큐 대상을 가짜로 교체 후, `handle` 메서드를 호출합니다. 이후 다음과 같은 메서드로 상태를 검증할 수 있습니다:

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

`Queue` 파사드의 `before` 및 `after` 메서드로 잡 처리 전후 실행할 콜백을 등록할 수 있습니다. 로깅, 통계 집계 등 다양한 용도로 활용합니다. 보통 `AppServiceProvider` 같은 서비스 프로바이더 `boot` 메서드에서 호출하세요:

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

`Queue` 파사드의 `looping` 메서드로 워커가 큐에서 잡을 가져오기 직전 실행할 콜백을 등록할 수도 있습니다. 예를 들어, 이전 작업에서 트랜잭션이 열려 있다면 롤백할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Queue;

Queue::looping(function () {
    while (DB::transactionLevel() > 0) {
        DB::rollBack();
    }
});
```