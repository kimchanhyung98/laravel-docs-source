# 큐 (Queues)

- [소개](#introduction)
    - [커넥션과 큐의 차이](#connections-vs-queues)
    - [드라이버별 유의사항 및 사전 준비](#driver-prerequisites)
- [잡(Job) 생성](#creating-jobs)
    - [잡 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [유니크 잡](#unique-jobs)
    - [암호화된 잡](#encrypted-jobs)
- [잡 미들웨어](#job-middleware)
    - [요청 제한(Rate Limiting)](#rate-limiting)
    - [잡 중복 방지](#preventing-job-overlaps)
    - [예외 제한(Throttling Exceptions)](#throttling-exceptions)
    - [잡 건너뛰기](#skipping-jobs)
- [잡 디스패치](#dispatching-jobs)
    - [지연 디스패치](#delayed-dispatching)
    - [동기식 디스패치](#synchronous-dispatching)
    - [잡 & 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [잡 체이닝](#job-chaining)
    - [큐와 커넥션 커스터마이징](#customizing-the-queue-and-connection)
    - [최대 시도 횟수/타임아웃 값 지정](#max-job-attempts-and-timeout)
    - [에러 처리](#error-handling)
- [잡 배치 처리](#job-batching)
    - [배치 처리 가능한 잡 정의](#defining-batchable-jobs)
    - [배치 디스패치](#dispatching-batches)
    - [체인과 배치](#chains-and-batches)
    - [배치에 잡 추가하기](#adding-jobs-to-batches)
    - [배치 조회](#inspecting-batches)
    - [배치 취소](#cancelling-batches)
    - [배치 실패 처리](#batch-failures)
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
    - [실패한 잡 정리](#cleaning-up-after-failed-jobs)
    - [실패한 잡 재실행](#retrying-failed-jobs)
    - [없는 모델 무시](#ignoring-missing-models)
    - [실패한 잡 가지치기(Pruning)](#pruning-failed-jobs)
    - [DynamoDB에 실패한 잡 저장](#storing-failed-jobs-in-dynamodb)
    - [실패한 잡 저장 비활성화](#disabling-failed-job-storage)
    - [실패한 잡 이벤트](#failed-job-events)
- [큐에서 잡 삭제](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [일부 잡 페이크 처리](#faking-a-subset-of-jobs)
    - [잡 체인 테스트](#testing-job-chains)
    - [잡 배치 테스트](#testing-job-batches)
    - [잡/큐 상호작용 테스트](#testing-job-queue-interactions)
- [잡 이벤트](#job-events)

<a name="introduction"></a>
## 소개

웹 애플리케이션을 만들다 보면, 예를 들어 업로드한 CSV 파일을 파싱하고 저장하는 작업과 같이 일반적인 웹 요청 중에 처리하기에는 시간이 많이 소요되는 작업이 있을 수 있습니다. 다행히도 라라벨은 백그라운드에서 처리할 수 있는 큐 잡을 쉽게 생성할 수 있도록 도와줍니다. 시간이 많이 걸리는 작업을 큐로 분리하면, 애플리케이션은 웹 요청에 훨씬 빠르게 응답할 수 있고, 사용자에게 더 좋은 경험을 제공합니다.

라라벨 큐는 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 또는 관계형 데이터베이스처럼 다양한 큐 백엔드에 대해 통합된 큐 API를 제공합니다.

큐와 관련된 라라벨의 설정 옵션들은 애플리케이션의 `config/queue.php` 설정 파일에 저장되어 있습니다. 이 파일에는 프레임워크에 기본 포함된 각 큐 드라이버(데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 등) 사용을 위한 커넥션 설정이 담겨 있습니다. 또한 잡을 즉시 실행하는(로컬 개발 시 사용) 동기식(synchronous) 드라이버와, 큐 잡을 바로 폐기하는 `null` 큐 드라이버도 포함되어 있습니다.

> [!NOTE]
> 라라벨은 이제 Redis 기반 큐의 대시보드와 설정을 한 눈에 볼 수 있는 Horizon을 제공합니다. 자세한 내용은 [Horizon 문서](/docs/12.x/horizon)를 참고하시기 바랍니다.

<a name="connections-vs-queues"></a>
### 커넥션과 큐의 차이

라라벨 큐를 처음 사용할 때, "커넥션(connection)"과 "큐(queue)"의 차이를 이해하는 것이 중요합니다. `config/queue.php` 파일에는 `connections`라는 설정 배열이 있습니다. 이 설정은 Amazon SQS, Beanstalk, Redis 같은 백엔드 큐 서비스와의 연결 정보를 정의합니다. 하지만, 각각의 큐 커넥션에는 여러 개의 "큐"를 둘 수 있으며, 각각은 별도의 잡 묶음 또는 스택이라고 생각할 수 있습니다.

각 커넥션 설정 예시에는 반드시 `queue` 속성이 포함되어 있다는 점에 주목하세요. 이 속성은 해당 커넥션으로 보낼 때 기본적으로 사용하는 큐를 지정합니다. 즉, 어떤 잡을 디스패치할 때 어느 큐에 넣을지 명시하지 않았다면, 잡은 커넥션 설정의 `queue` 속성에 지정된 큐에 들어가게 됩니다.

```php
use App\Jobs\ProcessPodcast;

// 이 잡은 기본 커넥션의 기본 큐로 전송됩니다...
ProcessPodcast::dispatch();

// 이 잡은 기본 커넥션의 "emails" 큐로 전송됩니다...
ProcessPodcast::dispatch()->onQueue('emails');
```

어떤 애플리케이션에서는 굳이 여러 큐를 사용하지 않고, 하나의 큐만 운용하는 것이 더 간단할 수 있습니다. 반면, 여러 큐를 사용하는 것은 작업의 우선순위나 분할 처리가 필요한 경우에 특히 유용합니다. 라라벨의 큐 워커는 어떤 큐를 어떤 우선순위로 처리할지 지정할 수 있기 때문입니다. 예를 들어, `high` 큐가 있다면 해당 큐를 우선 처리하도록 워커를 실행할 수 있습니다.

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버별 유의사항 및 사전 준비

<a name="database"></a>
#### 데이터베이스

`database` 큐 드라이버를 사용하려면, 잡 정보를 저장할 데이터베이스 테이블이 필요합니다. 일반적으로 라라벨 기본에 포함된 `0001_01_01_000002_create_jobs_table.php` [마이그레이션 파일](/docs/12.x/migrations)로 제공되지만, 애플리케이션에 해당 마이그레이션이 없다면 Artisan의 `make:queue-table` 명령어를 통해 추가할 수 있습니다.

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면, `config/database.php` 설정 파일에서 Redis 데이터베이스 커넥션을 먼저 설정해야 합니다.

> [!WARNING]
> `redis` 큐 드라이버에서는 `serializer`와 `compression` 옵션이 지원되지 않습니다.

**Redis 클러스터**

Redis 큐 커넥션이 Redis 클러스터를 사용할 경우, 큐 이름에 [키 해시 태그](https://redis.io/docs/reference/cluster-spec/#hash-tags)를 반드시 포함해야 합니다. 이렇게 해야 같은 큐에 대한 Redis 키가 동일한 해시 슬롯에 저장되어 정상적으로 동작합니다.

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

Redis 큐를 사용할 때, `block_for` 설정값을 지정하여 워커가 잡을 기다리는 대기 시간을 설정할 수 있습니다. 이 값에 따라 큐 워커가 Redis 데이터베이스를 새 잡이 있을 때마다 계속 폴링하지 않고, 잡이 들어올 때까지 대기하게 만들 수 있습니다. 예를 들어 `block_for` 값을 `5`로 설정하면, 새 잡이 들어올 때까지 최대 5초 동안 대기했다가, 그 이후에 워커 루프를 다시 반복하며 Redis를 폴링합니다.

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
> `block_for` 값을 `0`으로 설정하면, 워커가 잡이 올 때까지 무한히 블록됩니다. 이 경우 다음 잡이 처리될 때까지 `SIGTERM` 같은 신호가 처리되지 않습니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 사전 준비

아래 큐 드라이버를 사용하려면 추가로 필요한 의존성이 있습니다. 이 의존성들은 Composer 패키지 매니저를 통해 설치할 수 있습니다.

<div class="content-list" markdown="1">

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~2.0` 또는 phpredis PHP 확장
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`

</div>

<a name="creating-jobs"></a>
## 잡(Job) 생성

<a name="generating-job-classes"></a>
### 잡 클래스 생성

애플리케이션에서 작성하는 큐 잡 클래스는 기본적으로 `app/Jobs` 디렉터리에 저장됩니다. 만약 `app/Jobs` 디렉터리가 없다면, `make:job` Artisan 명령어를 실행할 때 자동으로 생성됩니다.

```shell
php artisan make:job ProcessPodcast
```

생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하며, 이로써 해당 잡이 큐에 추가되어 비동기적으로 실행됨을 라라벨에 알리게 됩니다.

> [!NOTE]
> 잡 스텁(stub)은 [스텁 퍼블리싱](/docs/12.x/artisan#stub-customization)을 통해 커스터마이즈할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조

잡 클래스는 매우 단순하며, 대개 큐에서 잡이 처리될 때 실행되는 `handle` 메서드만을 포함합니다. 먼저 예제 잡 클래스를 살펴봅니다. 여기에서는 팟캐스트 퍼블리싱 서비스를 운영하면서, 업로드된 팟캐스트 파일을 퍼블리싱 전에 처리해야 하는 상황을 가정합니다.

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

이 예제에서 볼 수 있듯이, [Eloquent 모델](/docs/12.x/eloquent)을 잡 생성자에 직접 주입할 수 있습니다. 잡에서 사용하는 `Queueable` 트레이트 덕분에, Eloquent 모델과 그에 로드된 연관관계도 잡이 처리될 때 자동으로 직렬화/역직렬화됩니다.

잡 생성자에 Eloquent 모델을 주입하면, 큐에는 오직 모델의 식별자만이 직렬화되어 저장됩니다. 그리고 잡이 실제로 처리될 때, 큐 시스템이 데이터베이스로부터 전체 모델 인스턴스와 관련 연관관계를 자동으로 다시 조회합니다. 이런 모델 직렬화 방식 덕분에 큐 드라이버로 보내는 잡 페이로드의 크기가 훨씬 작아집니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드의 의존성 주입

잡이 큐에서 처리될 때 `handle` 메서드가 호출됩니다. 이때, 잡의 `handle` 메서드에서 의존성 타입힌트가 가능하며, 라라벨 [서비스 컨테이너](/docs/12.x/container)가 의존성을 자동으로 주입해줍니다.

만약 컨테이너가 어떻게 `handle` 메서드의 의존성을 주입할지 직접 제어하고 싶다면, 컨테이너의 `bindMethod` 메서드를 사용할 수 있습니다. 이 메서드는 콜백을 인자로 받으며, 콜백은 잡과 컨테이너 객체를 전달받습니다. 그 안에서 원하는 방식으로 `handle` 메서드를 호출하면 됩니다. 일반적으로 이 코드는 `App\Providers\AppServiceProvider` [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에서 호출합니다.

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 원시 이미지 데이터 등 이진 데이터는 잡에 전달하기 전에 반드시 `base64_encode` 함수를 사용해 인코딩해야 합니다. 그렇지 않으면 잡을 큐에 넣을 때 JSON 직렬화가 제대로 이루어지지 않을 수 있습니다.

<a name="handling-relationships"></a>
#### 큐잉된 연관관계

잡이 큐에 들어갈 때, Eloquent 모델의 연관관계까지 함께 직렬화되기 때문에 때로는 직렬화된 잡 문자열이 매우 커질 수 있습니다. 또한, 잡이 역직렬화되고 나서 연관관계를 데이터베이스에서 재조회할 때, 기존에 잡을 큐잉하기 전에 적용했던 연관관계 제약 조건은 적용되지 않고 전체가 조회됩니다. 따라서 연관관계의 일부만을 대상으로 처리하고 싶다면, 큐잉된 잡 안에서 직접 다시 제약 조건을 설정해야 합니다.

또는, 연관관계 직렬화를 아예 방지하고 싶다면, 모델 속성값을 지정할 때 `withoutRelations` 메서드를 호출하세요. 이 메서드를 사용하면 연관관계가 로드되지 않은 모델 인스턴스만 담을 수 있습니다.

```php
/**
 * Create a new job instance.
 */
public function __construct(
    Podcast $podcast,
) {
    $this->podcast = $podcast->withoutRelations();
}
```

PHP 생성자 프로퍼티 프로모션을 사용하면서, Eloquent 모델의 연관관계까지 직렬화하지 않으려면 `WithoutRelations` attribute를 사용할 수 있습니다.

```php
use Illuminate\Queue\Attributes\WithoutRelations;

/**
 * Create a new job instance.
 */
public function __construct(
    #[WithoutRelations]
    public Podcast $podcast,
) {}
```

잡이 단일 모델이 아닌 컬렉션이나 배열로 여러 Eloquent 모델을 전달받는다면, 잡이 역직렬화되어 실행될 때 그 컬렉션/배열 내의 모델들은 연관관계가 복원되지 않습니다. 이는 대량의 모델을 다루는 잡에서 불필요한 리소스 사용을 방지하기 위한 조치입니다.

<a name="unique-jobs"></a>
### 유니크 잡

> [!WARNING]
> 유니크 잡은 [락](/docs/12.x/cache#atomic-locks)을 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 원자적 락을 지원합니다. 또한, 유니크 잡 제약은 배치 안의 잡에는 적용되지 않습니다.

특정 종류의 잡이 한 번에 한 인스턴스만 큐에 존재하도록 보장하고 싶을 때, 잡 클래스에 `ShouldBeUnique` 인터페이스를 구현하면 됩니다. 이 인터페이스를 구현할 때 추가 메서드를 구현할 필요는 없습니다.

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

위 예제에서 `UpdateSearchIndex` 잡은 유니크하게 동작합니다. 즉, 동일한 잡이 이미 큐에 들어가 있고 처리가 완료되지 않았다면, 잡이 추가적으로 디스패치되지 않습니다.

경우에 따라 잡의 유니크 여부를 결정하는 고유 "키"를 지정하거나, 잡이 얼마 동안 유니크 상태를 유지할지 타임아웃을 지정하고 싶을 수도 있습니다. 이를 위해 잡 클래스에 `uniqueId`와 `uniqueFor` 프로퍼티나 메서드를 정의할 수 있습니다.

```php
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
     * 잡의 유니크 락이 풀릴 때까지의 시간(초).
     *
     * @var int
     */
    public $uniqueFor = 3600;

    /**
     * 잡의 유니크 ID를 반환합니다.
     */
    public function uniqueId(): string
    {
        return $this->product->id;
    }
}
```

예를 들어 위와 같이 `UpdateSearchIndex` 잡을 상품의 ID로 유니크하게 지정하면, 같은 상품 ID로 새로운 잡을 디스패치해도 기존 잡이 처리될 때까지 무시됩니다. 또, 기존 잡이 1시간 내에 처리되지 않으면 유니크 락이 해제되어 같은 키로 새로운 잡이 큐에 들어갑니다.

> [!WARNING]
> 여러 웹 서버나 컨테이너에서 잡을 디스패치하는 경우, 모든 서버가 같은 중앙 캐시 서버를 사용하도록 구성해야 라라벨이 잡의 유니크 여부를 정확하게 판단할 수 있습니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 잡이 처리 시작 시점까지 유니크 상태 유지

기본적으로 유니크 잡은 잡이 처리 완료되거나 모든 재시도가 실패한 뒤에 "락"이 풀립니다. 하지만 잡이 "실제로 처리되기 직전"에 즉시 락을 해제하고 싶은 경우에는, `ShouldBeUnique` 대신 `ShouldBeUniqueUntilProcessing` 인터페이스를 구현하세요.

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

실제 동작에서는, `ShouldBeUnique` 잡이 디스패치될 때 라라벨은 내부적으로 `uniqueId` 키를 이용해 [락](/docs/12.x/cache#atomic-locks) 획득을 시도합니다. 락 획득에 실패하면 잡은 디스패치되지 않습니다. 이 락은 잡이 처리 완료되거나 모든 재시도가 끝나면 해제됩니다.

라라벨은 기본적으로 기본 캐시 드라이버를 사용해 락을 관리하지만, 락 사용 시에 다른 드라이버를 이용하고 싶다면 `uniqueVia` 메서드를 정의해서 사용하는 캐시 드라이버를 반환할 수 있습니다.

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
> 만약 잡의 동시 실행 수만 제한하고 싶다면, [WithoutOverlapping](/docs/12.x/queues#preventing-job-overlaps) 잡 미들웨어를 사용하세요.

<a name="encrypted-jobs"></a>
### 암호화된 잡

라라벨은 [암호화](/docs/12.x/encryption) 기능을 통해 잡 데이터의 프라이버시와 무결성을 보장할 수 있습니다. 이를 위해 잡 클래스에 `ShouldBeEncrypted` 인터페이스만 추가해주면, 해당 잡이 큐에 들어갈 때 라라벨이 자동으로 암호화를 적용합니다.

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
## 잡 미들웨어

잡 미들웨어를 사용하면 큐잉된 잡의 실행 주위에 커스텀 로직을 감쌀 수 있으므로, 각 잡 내부의 중복 코드(보일러플레이트 코드)를 줄일 수 있습니다. 예를 들어, 아래 `handle` 메서드는 라라벨의 Redis 요청 제한 기능을 사용해 5초마다 한 개의 잡만 처리하도록 제한하는 코드입니다.

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

이 코드 역시 정상적이지만, Redis 요청 제한 로직이 `handle` 메서드를 복잡하게 만들고, 동일한 요청 제한이 필요한 다른 잡에도 코드를 중복해서 작성해야 합니다.

대신, 요청 제한 로직을 잡의 `handle` 메서드가 아니라 별도의 잡 미들웨어로 분리할 수 있습니다. 라라벨은 잡 미들웨어의 기본 위치를 정해두지 않았으므로, 애플리케이션에서 원하는 디렉터리에 미들웨어를 둘 수 있습니다. 이 예제에서는 `app/Jobs/Middleware` 디렉터리에 추가합니다.

```php
<?php

namespace App\Jobs\Middleware;

use Closure;
use Illuminate\Support\Facades\Redis;

class RateLimited
{
    /**
     * Process the queued job.
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

위에서 볼 수 있듯이, [라우트 미들웨어](/docs/12.x/middleware)와 비슷하게 잡 미들웨어는 처리 중인 잡과, 다음 처리를 실행해야 하는 콜백을 받습니다.

이렇게 잡 미들웨어를 만든 뒤, 잡 클래스의 `middleware` 메서드에서 해당 미들웨어를 반환하면 됩니다. 이 메서드는 `make:job` Artisan 명령어로 생성된 잡에는 기본적으로 포함되어 있지 않으니 여러분이 직접 추가해야 합니다.

```php
use App\Jobs\Middleware\RateLimited;

/**
 * 이 잡이 통과해야 하는 미들웨어를 반환합니다.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited];
}
```

> [!NOTE]
> 잡 미들웨어는 큐잉 가능한 이벤트 리스너, 메일러블, 알림에도 사용할 수 있습니다.

<a name="rate-limiting"></a>
### 요청 제한(Rate Limiting)

앞서 직접 요청 제한 잡 미들웨어를 구현하는 법을 살펴봤지만, 라라벨에는 이미 잡을 위한 요청 제한 미들웨어가 내장되어 있습니다. [라우트 요청 제한자](/docs/12.x/routing#defining-rate-limiters)와 마찬가지로, 잡 요청 제한자도 `RateLimiter` 파사드의 `for` 메서드를 사용해서 정의할 수 있습니다.

예를 들어, 일반 사용자는 시간당 한 번만 데이터를 백업할 수 있도록 하고, 프리미엄 고객에는 제한을 두지 않으려면, 아래와 같이 `AppServiceProvider`의 `boot` 메서드에서 요청 제한자를 정의할 수 있습니다.

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Support\Facades\RateLimiter;

/**
 * Bootstrap any application services.
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

이 예시에서는 시간 단위(all hour)의 요청 제한을 정의했습니다. 분 단위 제한이 필요하다면 `perMinute` 메서드를 사용할 수 있습니다. 또한, `by` 메서드에 원하는 값을 전달해 제한 기준을 세분화할 수 있습니다. 대개 고객별로 제한을 걸 때 사용합니다.

```php
return Limit::perMinute(50)->by($job->user->id);
```

요청 제한을 정의했다면, `Illuminate\Queue\Middleware\RateLimited` 미들웨어를 잡에 붙여 사용할 수 있습니다. 잡이 요청 제한에 걸릴 때마다, 미들웨어가 잡을 적절한 지연(delay)으로 다시 큐에 넣어줍니다.

```php
use Illuminate\Queue\Middleware\RateLimited;

/**
 * 이 잡이 통과해야 하는 미들웨어를 반환합니다.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited('backups')];
}
```

요청 제한에 걸려 큐에 다시 들어가는 경우에도 잡의 `attempts`(시도 횟수)는 증가합니다. 따라서 잡 클래스의 `tries`나 `maxExceptions` 속성을 상황에 맞게 조정하거나, [retryUntil 메서드](#time-based-attempts)로 잡의 만료 기준을 별도로 정할 수도 있습니다.

`releaseAfter` 메서드를 사용하면, 잡이 다시 시도되기 전까지 몇 초의 지연이 있어야 하는지 직접 지정할 수 있습니다.

```php
/**
 * 이 잡이 통과해야 하는 미들웨어를 반환합니다.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new RateLimited('backups'))->releaseAfter(60)];
}
```

잡이 요청 제한으로 인해 재시도되기를 원하지 않는다면, `dontRelease` 메서드를 사용할 수 있습니다.

```php
/**
 * 이 잡이 통과해야 하는 미들웨어를 반환합니다.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new RateLimited('backups'))->dontRelease()];
}
```

> [!NOTE]
> Redis를 사용할 경우, 기본 미들웨어보다 Redis에 최적화된 `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어를 사용할 수 있습니다.

<a name="preventing-job-overlaps"></a>
### 잡 중복 방지

라라벨에는 임의의 키를 기준으로 잡의 중복 실행을 방지하는 `Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어가 내장되어 있습니다. 이는 하나의 리소스를 동시에 여러 잡에서 수정하면 안 되는 상황에서 유용합니다.

예를 들어, 사용자의 신용점수를 업데이트하는 큐 잡이 있고, 같은 사용자 ID에 대해 중복 업데이트가 실행되지 않도록 하려면 잡의 `middleware` 메서드에서 `WithoutOverlapping` 미들웨어를 반환하면 됩니다.

```php
use Illuminate\Queue\Middleware\WithoutOverlapping;

/**
 * 이 잡이 통과해야 하는 미들웨어를 반환합니다.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new WithoutOverlapping($this->user->id)];
}
```

동일한 키로 중복된 잡이 있으면, 그 잡은 다시 큐에 리스케줄됩니다. 그리고 얼마 뒤에 다시 시도할지 `releaseAfter`로 지정할 수 있습니다.

```php
/**
 * 이 잡이 통과해야 하는 미들웨어를 반환합니다.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->releaseAfter(60)];
}
```

즉시 중복 잡을 삭제해서(재시도 없이) 더 이상 실행되지 않도록 하려면, `dontRelease` 메서드를 사용할 수 있습니다.

```php
/**
 * 이 잡이 통과해야 하는 미들웨어를 반환합니다.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->dontRelease()];
}
```

`WithoutOverlapping` 미들웨어는 라라벨의 원자적 락 기능을 기반으로 동작합니다. 때때로 잡이 예상치 못하게 실패하거나 타임아웃되어 락이 해제되지 않은 채로 남을 수 있습니다. 이때는 `expireAfter` 메서드로 락이 자동으로 풀리는 만료 시간을 명시할 수 있습니다. 아래 예시는 잡이 처리된 후 3분(180초) 후 락을 해제하도록 설정합니다.

```php
/**
 * 이 잡이 통과해야 하는 미들웨어를 반환합니다.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->expireAfter(180)];
}
```

> [!WARNING]
> `WithoutOverlapping` 미들웨어는 [락](/docs/12.x/cache#atomic-locks)을 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 원자적 락을 지원합니다.

<a name="sharing-lock-keys"></a>

#### 여러 잡 클래스에서 Lock 키 공유하기

기본적으로 `WithoutOverlapping` 미들웨어는 동일한 클래스의 잡이 겹쳐서 실행되는 것만 방지합니다. 따라서 두 개의 서로 다른 잡 클래스가 동일한 lock 키를 사용하더라도, 이 키로 인해 겹침(동시 실행)이 방지되지는 않습니다. 하지만, `shared` 메서드를 사용하여 라라벨이 이 키를 여러 잡 클래스 간에 적용하도록 지시할 수 있습니다.

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
### 예외 발생 제한(Throttling Exceptions)

라라벨에는 예외 발생을 제한할 수 있는 `Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어가 포함되어 있습니다. 이 미들웨어를 사용하면, 잡이 지정한 횟수만큼 예외를 던진 뒤에는, 정해진 시간 간격이 지나기 전까지 추가 시도를 지연시킬 수 있습니다. 이 미들웨어는 특히 불안정한 외부 서비스와 상호작용하는 잡에서 유용합니다.

예를 들어, 외부 API와 통신하는 잡이 예외를 발생시키기 시작했다고 가정해보겠습니다. 예외 발생 제한을 적용하려면, 잡의 `middleware` 메서드에서 `ThrottlesExceptions` 미들웨어를 반환하면 됩니다. 일반적으로 이 미들웨어는 [시간 기반 재시도](#time-based-attempts)와 함께 사용하는 것이 좋습니다.

```php
use DateTime;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡이 거쳐야 할 미들웨어를 반환합니다.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new ThrottlesExceptions(10, 5 * 60)];
}

/**
 * 잡이 타임아웃되어야 할 시점을 결정합니다.
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(30);
}
```

미들웨어 생성자의 첫 번째 인수는 예외가 몇 번 발생하면 제한(throttled)할지 지정합니다. 두 번째 인수는 제한된 후 몇 초가 지나야 다시 잡 실행을 시도할지 지정합니다. 위 예시 코드에서는 잡이 10번 연속으로 예외를 던질 경우, 5분 동안 실행을 지연시키며, 이 동작은 30분 이내에만 반복됩니다.

잡이 예외를 던졌지만 임계값에 아직 도달하지 않았을 때는, 기본적으로 즉시 재시도됩니다. 하지만, 이 잡을 일정 시간만큼 지연시켜 재시도하려면, 미들웨어를 붙일 때 `backoff` 메서드를 호출할 수 있습니다.

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡이 거쳐야 할 미들웨어를 반환합니다.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 5 * 60))->backoff(5)];
}
```

이 미들웨어는 내부적으로 라라벨의 캐시 시스템을 사용해 속도 제한(rate limiting)을 구현합니다. 잡 클래스명이 캐시 "키"로 사용됩니다. 잡을 여러 개 두고 동일한 외부 서비스를 다루며, 공통 제한 "버킷"을 공유하고 싶다면, 미들웨어를 붙일 때 `by` 메서드로 키를 오버라이드할 수 있습니다.

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡이 거쳐야 할 미들웨어를 반환합니다.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->by('key')];
}
```

기본적으로 이 미들웨어는 모든 예외를 제한합니다(throttle). 이 동작을 변경하고 싶다면, 미들웨어를 붙일 때 `when` 메서드를 사용하세요. 이 메서드에 전달된 클로저가 `true`를 반환할 때에만 해당 예외를 제한합니다.

```php
use Illuminate\Http\Client\HttpClientException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡이 거쳐야 할 미들웨어를 반환합니다.
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

`when` 메서드와는 달리, 예외 상황에 잡을 큐에 다시 올리거나 예외를 던지는 대신, `deleteWhen` 메서드는 특정 예외가 발생했을 때 잡을 즉시 삭제합니다.

```php
use App\Exceptions\CustomerDeletedException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡이 거쳐야 할 미들웨어를 반환합니다.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(2, 10 * 60))->deleteWhen(CustomerDeletedException::class)];
}
```

제한된 예외(throttled exception)를 애플리케이션의 예외 핸들러에 보고하고 싶다면, 미들웨어를 붙일 때 `report` 메서드를 사용하면 됩니다. 클로저를 추가로 전달하면, 해당 클로저가 `true`를 반환할 때에만 예외가 보고됩니다.

```php
use Illuminate\Http\Client\HttpClientException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡이 거쳐야 할 미들웨어를 반환합니다.
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
> Redis를 사용하는 경우, `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어를 사용할 수 있으며, 이는 Redis 환경에 최적화되어 기본 예외 제한 미들웨어보다 훨씬 효율적입니다.

<a name="skipping-jobs"></a>
### 잡 건너뛰기

`Skip` 미들웨어를 사용하면, 잡의 로직을 따로 수정하지 않아도 잡을 건너뛰거나 삭제하도록 지정할 수 있습니다. `Skip::when` 메서드는 조건이 `true`로 평가될 경우 잡을 삭제하고, `Skip::unless` 메서드는 조건이 `false`일 때 잡을 삭제합니다.

```php
use Illuminate\Queue\Middleware\Skip;

/**
 * 잡이 거쳐야 할 미들웨어를 반환합니다.
 */
public function middleware(): array
{
    return [
        Skip::when($someCondition),
    ];
}
```

복잡한 조건 평가가 필요하다면, `when`과 `unless` 메서드에 `Closure`를 전달할 수도 있습니다.

```php
use Illuminate\Queue\Middleware\Skip;

/**
 * 잡이 거쳐야 할 미들웨어를 반환합니다.
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
## 잡 디스패치(Dispatching Jobs)

잡 클래스를 작성했다면, 잡 자체의 `dispatch` 메서드를 사용해서 큐에 등록할 수 있습니다. `dispatch` 메서드에 전달된 인수는 잡의 생성자(constructor)에 그대로 전달됩니다.

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
     * 새 팟캐스트를 저장합니다.
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

잡을 조건부로 디스패치하고 싶다면, `dispatchIf` 와 `dispatchUnless` 메서드를 사용할 수 있습니다.

```php
ProcessPodcast::dispatchIf($accountActive, $podcast);

ProcessPodcast::dispatchUnless($accountSuspended, $podcast);
```

새로운 라라벨 애플리케이션에서 기본 큐 드라이버는 `sync`입니다. 이 드라이버는 잡을 현재 요청의 포그라운드에서 동기적으로 실행하며, 로컬 개발 도중에는 매우 편리합니다. 백그라운드에서 큐 작업을 처리하고 싶다면, 애플리케이션의 `config/queue.php` 설정 파일에서 다른 큐 드라이버를 지정하면 됩니다.

<a name="delayed-dispatching"></a>
### 디스패치 지연(Delayed Dispatching)

잡이 바로 큐 워커에 의해 처리되지 않고 일정 시간 이후에만 대기열에 들어가게 하고 싶다면, 잡을 디스패치할 때 `delay` 메서드를 사용할 수 있습니다. 예를 들어, 잡이 디스패치된 후 10분이 지나야 처리 가능하게 하려면 아래와 같이 할 수 있습니다.

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
     * 새 팟캐스트를 저장합니다.
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

잡에 기본 지연(delay)이 설정돼 있는 경우가 있는데, 이 지연을 무시하고 즉시 처리하고 싶다면 `withoutDelay` 메서드를 사용할 수 있습니다.

```php
ProcessPodcast::dispatch($podcast)->withoutDelay();
```

> [!WARNING]
> Amazon SQS 큐 서비스에서 지정 가능한 최대 딜레이(지연) 시간은 15분입니다.

<a name="dispatching-after-the-response-is-sent-to-browser"></a>
#### 브라우저에 응답이 전달된 후 디스패치하기

또 한 가지 방법은, 웹 서버가 FastCGI를 사용할 때 `dispatchAfterResponse` 메서드를 활용하여 HTTP 응답이 사용자 브라우저에 전달된 이후에 잡을 디스패치할 수 있습니다. 이렇게 하면 잡이 큐에서 실행 중이어도 사용자는 즉시 애플리케이션을 사용할 수 있습니다. 이 방식은 보통 이메일 발송처럼 1초 정도가 소요되는 작업에 사용해야 하며, 단일 HTTP 요청 내에서 처리되기에, 별도의 큐 워커가 실행되고 있을 필요는 없습니다.

```php
use App\Jobs\SendNotification;

SendNotification::dispatchAfterResponse();
```

또한, 클로저도 `dispatch` 헬퍼로 등록한 뒤 `afterResponse` 메서드를 체이닝하여, 브라우저로 HTTP 응답을 보낸 이후에 실행할 수 있습니다.

```php
use App\Mail\WelcomeMessage;
use Illuminate\Support\Facades\Mail;

dispatch(function () {
    Mail::to('taylor@example.com')->send(new WelcomeMessage);
})->afterResponse();
```

<a name="synchronous-dispatching"></a>
### 동기적 디스패치(Synchronous Dispatching)

잡을 즉시(동기적으로) 실행하고 싶을 때는, `dispatchSync` 메서드를 사용합니다. 이 메서드를 사용할 경우, 잡은 큐에 등록되지 않고 현재 프로세스에서 바로 실행됩니다.

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
     * 새 팟캐스트를 저장합니다.
     */
    public function store(Request $request): RedirectResponse
    {
        $podcast = Podcast::create(/* ... */);

        // Create podcast...

        ProcessPodcast::dispatchSync($podcast);

        return redirect('/podcasts');
    }
}
```

<a name="jobs-and-database-transactions"></a>
### 잡과 데이터베이스 트랜잭션(Jobs & Database Transactions)

데이터베이스 트랜잭션 안에서 잡을 디스패치하는 것은 아무 문제가 없지만, 잡이 정말로 성공적으로 실행될 수 있도록 주의해야 합니다. 트랜잭션 내부에서 잡을 디스패치하는 경우, 잡이 워커에 의해 처리될 때 상위(parent) 트랜잭션이 아직 커밋되지 않았을 수 있습니다. 이때, 트랜잭션에서 반영한 모델 혹은 데이터베이스 레코드의 변경 내용이 실제 데이터베이스에 반영되지 않을 수 있습니다. 또한, 트랜잭션 중 생성한 모델이나 데이터베이스 레코드가 데이터베이스에 존재하지 않을 수도 있습니다.

다행히 라라벨은 이 문제를 해결할 수 있는 여러 방법을 제공합니다. 먼저, 큐 연결 설정 배열에 `after_commit` 옵션을 추가하면 됩니다.

```php
'redis' => [
    'driver' => 'redis',
    // ...
    'after_commit' => true,
],
```

`after_commit` 옵션을 `true`로 설정하면, 데이터베이스 트랜잭션 내에서도 잡을 디스패치할 수 있지만, 라라벨은 열린 상위 데이터베이스 트랜잭션이 모두 커밋된 후에 비로소 잡을 디스패치합니다. 물론, 열린 트랜잭션이 없다면, 잡은 즉시 디스패치됩니다.

만약 트랜잭션 과정에서 예외로 인해 트랜잭션이 롤백되면, 그 트랜잭션 중에 디스패치된 잡은 모두 폐기됩니다.

> [!NOTE]
> `after_commit` 설정 옵션을 `true`로 설정하면, 큐에 대기 중인 이벤트 리스너, 메일러블, 알림, 브로드캐스트 이벤트 등도 모든 열린 데이터베이스 트랜잭션이 커밋된 다음에 디스패치됩니다.

<a name="specifying-commit-dispatch-behavior-inline"></a>
#### 커밋 후 디스패치 동작을 인라인으로 지정

큐 연결 설정에서 `after_commit` 옵션을 `true`로 지정하지 않은 경우에도, 특정 잡만 커밋 이후 디스패치 되도록 직접 지정할 수 있습니다. 이때는 디스패치 연산에 `afterCommit` 메서드를 체이닝하면 됩니다.

```php
use App\Jobs\ProcessPodcast;

ProcessPodcast::dispatch($podcast)->afterCommit();
```

반대로, 큐 연결의 `after_commit` 옵션이 `true`로 되어 있다면, 특정 잡만 트랜잭션 커밋을 기다리지 않고 즉시 디스패치하도록 `beforeCommit` 메서드를 사용할 수 있습니다.

```php
ProcessPodcast::dispatch($podcast)->beforeCommit();
```

<a name="job-chaining"></a>
### 잡 체이닝(Job Chaining)

잡 체이닝을 사용하면, 첫 번째 잡이 성공적으로 실행된 뒤 이어서 실행되어야 할 잡 목록을 순차적으로 지정할 수 있습니다. 체인 중간에 하나라도 실패하면, 그 이후의 잡은 실행되지 않습니다. 잡 체인을 실행하려면, `Bus` 파사드의 `chain` 메서드를 사용하면 됩니다. 라라벨의 커맨드 버스는 큐 잡 디스패칭이 그 위에 구현된 저수준 컴포넌트입니다.

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

잡 클래스 인스턴스뿐만 아니라 클로저도 체인에 추가할 수 있습니다.

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
> 잡 내부에서 `$this->delete()` 메서드를 사용해 잡을 삭제하더라도, 체이닝된 후속 잡의 실행을 막을 수 없습니다. 체인은 오직 중간의 잡이 실패한 경우에만 멈춥니다.

<a name="chain-connection-queue"></a>
#### 체인 연결 및 큐 지정

체이닝된 잡들에 사용할 연결(connection)과 큐(queue)를 지정하고 싶다면, `onConnection` 및 `onQueue` 메서드를 사용할 수 있습니다. 이 메서드들은, 개별 잡에서 별도로 큐 연결/큐를 지정하지 않은 경우 전체 체인에,
각각 큐 연결명과 큐명을 지정하게 됩니다.

```php
Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->onConnection('redis')->onQueue('podcasts')->dispatch();
```

<a name="adding-jobs-to-the-chain"></a>
#### 체인에 잡 추가하기

가끔은, 현재 체인 내 다른 잡에서 이미 존재하는 체인에 잡을 앞이나 뒤에 추가할 필요가 있을 수 있습니다. 이럴 때는 `prependToChain` 과 `appendToChain` 메서드를 사용할 수 있습니다.

```php
/**
 * 잡 실행 메서드
 */
public function handle(): void
{
    // ...

    // 현재 체인 맨 앞에 추가. 현재 잡 다음에 바로 실행...
    $this->prependToChain(new TranscribePodcast);

    // 현재 체인 맨 뒤에 추가. 체인 맨 마지막에 실행...
    $this->appendToChain(new TranscribePodcast);
}
```

<a name="chain-failures"></a>
#### 체인 실패 처리

잡을 체이닝할 때, 체인 내 잡이 실패하는 경우 실행할 클로저를 `catch` 메서드로 지정할 수 있습니다. 지정한 콜백은 잡 실패의 원인이 된 `Throwable` 인스턴스를 인자로 받습니다.

```php
use Illuminate\Support\Facades\Bus;
use Throwable;

Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->catch(function (Throwable $e) {
    // 체인 내 잡 중 하나가 실패했습니다...
})->dispatch();
```

> [!WARNING]
> 체인 콜백은 직렬화되어 큐에서 나중에 실행되므로, 체인 콜백 내에서 `$this` 변수를 사용해서는 안 됩니다.

<a name="customizing-the-queue-and-connection"></a>
### 큐 및 커넥션 커스터마이즈

<a name="dispatching-to-a-particular-queue"></a>
#### 특정 큐로 디스패치

여러 큐로 잡을 분류하여 배치할 수 있습니다. 이를 통해 잡을 “카테고리”로 분리할 수 있으며, 다양한 큐별로 워커를 다르게 할당해 우선순위를 조절할 수도 있습니다. 이때, 큐 연결(connection)이 나뉘는 것은 아니고, 단일 connection 내 큐만 구분하는 것임을 유념하세요. 잡을 특정 큐로 보낼 때는 `onQueue` 메서드를 사용하면 됩니다.

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
     * 새 팟캐스트를 저장합니다.
     */
    public function store(Request $request): RedirectResponse
    {
        $podcast = Podcast::create(/* ... */);

        // Create podcast...

        ProcessPodcast::dispatch($podcast)->onQueue('processing');

        return redirect('/podcasts');
    }
}
```

혹은, 잡 클래스의 생성자 내부에서 `onQueue` 메서드를 호출하여 잡 자체가 항상 특정 큐로 가도록 지정할 수도 있습니다.

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    /**
     * 새 잡 인스턴스를 생성합니다.
     */
    public function __construct()
    {
        $this->onQueue('processing');
    }
}
```

<a name="dispatching-to-a-particular-connection"></a>
#### 특정 커넥션으로 디스패치

애플리케이션이 여러 큐 연결을 사용하는 경우, `onConnection` 메서드를 이용해 잡이 푸시될 커넥션을 직접 지정할 수 있습니다.

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
     * 새 팟캐스트를 저장합니다.
     */
    public function store(Request $request): RedirectResponse
    {
        $podcast = Podcast::create(/* ... */);

        // Create podcast...

        ProcessPodcast::dispatch($podcast)->onConnection('sqs');

        return redirect('/podcasts');
    }
}
```

`onConnection`과 `onQueue` 메서드를 체인으로 연결하여, 잡의 커넥션과 큐를 동시에 지정할 수도 있습니다.

```php
ProcessPodcast::dispatch($podcast)
    ->onConnection('sqs')
    ->onQueue('processing');
```

혹은, 잡 클래스의 생성자 내부에서 `onConnection` 메서드를 사용하여 잡 인스턴스가 생성될 때 해당 커넥션으로 항상 지정하도록 할 수 있습니다.

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    /**
     * 새 잡 인스턴스를 생성합니다.
     */
    public function __construct()
    {
        $this->onConnection('sqs');
    }
}
```

<a name="max-job-attempts-and-timeout"></a>

### 최대 작업 시도 횟수 / 타임아웃 값 지정하기

<a name="max-attempts"></a>
#### 최대 시도 횟수

큐에 등록된 작업이 오류를 계속 발생시킬 경우, 무한히 재시도하는 것은 원하지 않을 것입니다. 그래서 라라벨은 작업이 시도될 최대 횟수나 기간을 지정할 수 있는 여러 방법을 제공합니다.

가장 간단한 방법 중 하나는 Artisan 명령어에서 `--tries` 옵션을 사용하여 작업이 시도될 최대 횟수를 지정하는 것입니다. 이 옵션은 워커가 처리하는 모든 작업에 적용되며, 개별 작업에서 시도 횟수를 별도로 지정하지 않은 경우에만 적용됩니다.

```shell
php artisan queue:work --tries=3
```

작업이 최대 시도 횟수를 초과하면, 해당 작업은 "실패"한 작업으로 간주됩니다. 실패한 작업 처리에 대한 자세한 내용은 [실패한 작업 문서](#dealing-with-failed-jobs)를 참고하세요. 만약 `queue:work` 명령어에 `--tries=0`을 지정하면, 작업은 무한히 재시도됩니다.

더 세밀하게 제어하고 싶다면, 작업 클래스 자체에 최대 시도 횟수를 지정할 수 있습니다. 이 경우, 작업에 지정한 시도 횟수가 Artisan 명령어의 `--tries` 값보다 우선적으로 적용됩니다.

```php
<?php

namespace App\Jobs;

class ProcessPodcast implements ShouldQueue
{
    /**
     * 작업이 시도될 최대 횟수
     *
     * @var int
     */
    public $tries = 5;
}
```

특정 작업의 최대 시도 횟수를 동적으로 제어하려면, 작업 클래스에 `tries` 메서드를 정의할 수 있습니다.

```php
/**
 * 작업이 시도될 최대 횟수 반환
 */
public function tries(): int
{
    return 5;
}
```

<a name="time-based-attempts"></a>
#### 시간 기반 시도 제한

작업이 실패하기 전까지 시도할 최대 횟수 대신, 특정 시간까지 작업을 계속 시도하도록 지정할 수도 있습니다. 이렇게 하면 정해진 시간 안에서 작업이 여러 번 재시도될 수 있습니다. 이 기능을 사용하려면 작업 클래스에 `retryUntil` 메서드를 추가하고, 이 메서드가 `DateTime` 인스턴스를 반환하도록 작성합니다.

```php
use DateTime;

/**
 * 작업이 더 이상 시도되지 않아야 하는 시간을 반환
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(10);
}
```

`retryUntil`과 `tries`가 모두 지정되어 있다면, 라라벨은 `retryUntil` 메서드를 우선적으로 적용합니다.

> [!NOTE]
> [큐에 등록된 이벤트 리스너](/docs/12.x/events#queued-event-listeners)와 [큐에 등록된 알림](/docs/12.x/notifications#queueing-notifications)에서도 `tries` 속성이나 `retryUntil` 메서드를 정의할 수 있습니다.

<a name="max-exceptions"></a>
#### 최대 예외 개수

작업이 여러 번 시도될 수 있도록 허용하되, 처리 중에 지정한 횟수만큼 예외가 발생하면 실패로 처리하고 싶을 때가 있을 수 있습니다(즉, `release` 메서드를 직접 호출한 경우가 아니라, 예외로 인해 재시도되는 경우를 한정). 이때는 작업 클래스에 `maxExceptions` 속성을 정의하면 됩니다.

```php
<?php

namespace App\Jobs;

use Illuminate\Support\Facades\Redis;

class ProcessPodcast implements ShouldQueue
{
    /**
     * 작업이 시도될 최대 횟수
     *
     * @var int
     */
    public $tries = 25;

    /**
     * 실패하기 전에 허용할 최대 미처리 예외 개수
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
            // 락 획득 성공, podcast 처리...
        }, function () {
            // 락 획득 실패...
            return $this->release(10);
        });
    }
}
```

위 예시에서, 애플리케이션이 Redis 락을 획득하지 못하면 작업은 10초 동안 릴리즈(대기)되고, 최대 25번까지 시도됩니다. 그러나 예외가 3번 발생하면 작업은 실패로 처리됩니다.

<a name="timeout"></a>
#### 타임아웃

일반적으로, 각 작업이 얼마 정도 걸릴지 대략적으로 예상할 수 있습니다. 그래서 라라벨에서는 "타임아웃" 값을 설정할 수 있습니다. 기본적으로 타임아웃 값은 60초입니다. 만약 작업이 타임아웃 값 이상으로 실행된다면, 해당 작업을 처리하던 워커는 에러와 함께 종료됩니다. 보통 이러한 워커는 [서버에 설정된 프로세스 매니저](#supervisor-configuration)가 자동으로 재시작합니다.

작업이 실행될 수 있는 최대 시간(초 단위)은 Artisan 명령어의 `--timeout` 옵션을 사용하여 지정할 수 있습니다.

```shell
php artisan queue:work --timeout=30
```

작업이 타임아웃에 걸려 계속 최대 시도 횟수를 초과하는 경우, 해당 작업은 실패로 기록됩니다.

또한, 작업 클래스에서 직접 최대 실행 시간을 설정할 수도 있습니다. 이렇게 설정하면, 클래스에 정의된 타임아웃이 Artisan 명령의 타임아웃보다 우선 적용됩니다.

```php
<?php

namespace App\Jobs;

class ProcessPodcast implements ShouldQueue
{
    /**
     * 타임아웃(초 단위)
     *
     * @var int
     */
    public $timeout = 120;
}
```

때로는 소켓이나 외부 HTTP 연결처럼 I/O 블로킹이 발생하는 프로세스에서는 라라벨의 타임아웃이 제대로 동작하지 않을 수 있습니다. 따라서 이런 기능을 사용할 때는 관련 라이브러리(API)에서도 타임아웃을 따로 설정하는 것이 좋습니다. 예를 들어, Guzzle을 사용할 때는 반드시 연결 및 요청 타임아웃 값을 명시해야 합니다.

> [!WARNING]
> 작업 타임아웃을 지정하려면 `pcntl` PHP 확장 모듈이 설치되어 있어야 합니다. 또한, 작업의 "timeout" 값은 ["retry after"](#job-expiration) 값보다 항상 작아야 합니다. 그렇지 않으면, 작업이 실제로 실행 중이거나 타임아웃되기도 전에 다시 시도될 수 있습니다.

<a name="failing-on-timeout"></a>
#### 타임아웃 시 작업을 실패로 처리하기

작업이 타임아웃될 때 해당 작업을 [실패한 작업](#dealing-with-failed-jobs)으로 표시하고 싶다면 작업 클래스에 `$failOnTimeout` 속성을 정의하면 됩니다.

```php
/**
 * 작업이 타임아웃될 때 실패로 표시할지 여부
 *
 * @var bool
 */
public $failOnTimeout = true;
```

<a name="error-handling"></a>
### 에러 처리

작업을 처리하는 도중 예외가 발생하면, 해당 작업은 자동으로 큐에 다시 등록되어 재시도됩니다. 이 작업은 애플리케이션에서 지정한 최대 시도 횟수에 도달할 때까지 반복됩니다. 최대 시도 횟수는 `queue:work` Artisan 명령어의 `--tries` 옵션을 사용하거나, 작업 클래스에서 직접 지정할 수 있습니다. 큐 워커 실행에 대한 더 자세한 정보는 [아래에서 확인할 수 있습니다](#running-the-queue-worker).

<a name="manually-releasing-a-job"></a>
#### 작업을 수동으로 릴리즈(재시도 예약)하기

특정 상황에서 작업을 수동으로 큐에 다시 등록해 나중에 재시도할 수 있도록 만들고 싶을 수 있습니다. 이럴 때는 `release` 메서드를 호출하면 됩니다.

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

기본적으로 `release` 메서드는 작업을 큐에 즉시 다시 등록합니다. 하지만, 정해진 시간(초) 이후에 작업이 다시 처리되도록 하려면 정수 값이나 날짜 인스턴스를 인자로 넘겨줄 수 있습니다.

```php
$this->release(10);

$this->release(now()->addSeconds(10));
```

<a name="manually-failing-a-job"></a>
#### 작업을 수동으로 실패 처리하기

특정 경우, 작업을 직접 "실패"로 처리하고 싶을 때가 있을 수 있습니다. 이럴 때는 `fail` 메서드를 호출하면 됩니다.

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

만약 예외를 포착(try-catch)하여 그로 인해 작업을 실패로 처리하고 싶다면, `fail` 메서드에 해당 예외 객체를 넘기면 됩니다. 또는, 간편하게 문자열 형태의 에러 메시지를 넘기면 라라벨이 이를 예외로 변환해 처리합니다.

```php
$this->fail($exception);

$this->fail('Something went wrong.');
```

> [!NOTE]
> 실패한 작업에 대한 자세한 내용은 [실패한 작업 처리 문서](#dealing-with-failed-jobs)를 참고하세요.

<a name="job-batching"></a>
## 작업 배치 실행

라라벨의 작업 배치(batch) 기능을 사용하면 여러 작업을 한 번에 실행하고, 모든 작업이 완료된 후 특정 동작을 수행할 수 있습니다. 시작하기 전에 각 작업 배치의 meta 정보(예: 완료 비율 등)를 저장할 테이블에 대한 데이터베이스 마이그레이션을 생성해야 합니다. 이 마이그레이션은 `make:queue-batches-table` Artisan 명령어로 생성할 수 있습니다.

```shell
php artisan make:queue-batches-table

php artisan migrate
```

<a name="defining-batchable-jobs"></a>
### 배치 처리 가능한 작업 정의하기

배치 실행이 가능한 작업을 정의하려면, [일반적인 큐 작업 생성 방법](#creating-jobs)과 동일하게 작업 클래스를 만들되, 해당 클래스에 `Illuminate\Bus\Batchable` 트레이트를 추가해야 합니다. 이 트레이트는 작업이 현재 어떤 배치에서 실행 중인지 조회할 수 있는 `batch` 메서드를 제공합니다.

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
            // 배치가 취소되었는지 확인...

            return;
        }

        // CSV 파일의 일부 데이터를 import...
    }
}
```

<a name="dispatching-batches"></a>
### 배치 작업 디스패치하기

여러 작업을 배치로 디스패치(실행 요청)하려면 `Bus` 파사드의 `batch` 메서드를 사용하면 됩니다. 배치 기능의 주요 장점은 완료 후 콜백을 쉽고 유연하게 등록할 수 있다는 점입니다. `then`, `catch`, `finally` 등의 메서드를 활용하여 배치가 완료되거나, 실패했을 때 또는 끝났을 때 동작할 콜백을 등록할 수 있습니다. 각 콜백에는 `Illuminate\Bus\Batch` 인스턴스가 전달됩니다. 다음 예제에서는 각 작업이 CSV 파일의 일부 행을 처리하는 작업들을 배치로 큐잉한다고 가정합니다.

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
    // 배치가 생성됐으나 아직 작업이 추가되지 않은 상태...
})->progress(function (Batch $batch) {
    // 개별 작업이 하나 완료됨...
})->then(function (Batch $batch) {
    // 모든 작업이 성공적으로 완료됨...
})->catch(function (Batch $batch, Throwable $e) {
    // 첫 번째 실패 작업 발견 시...
})->finally(function (Batch $batch) {
    // 배치의 실행이 종료됨...
})->dispatch();

return $batch->id;
```

배치의 ID는 `$batch->id` 프로퍼티를 통해 접근할 수 있으며, 이후 [라라벨 커맨드 버스](#inspecting-batches)를 통해 해당 배치 정보를 조회할 때 활용할 수 있습니다.

> [!WARNING]
> 배치 콜백은 직렬화되어 나중에 라라벨 큐에서 실행됩니다. 따라서 콜백 내부에서 `$this` 변수를 사용하지 마세요. 그리고, 배치로 묶인 모든 작업은 데이터베이스 트랜잭션 내에서 실행되므로, 암묵적으로 커밋이 발생하는 데이터베이스 쿼리를 작업 내부에서 실행해서는 안 됩니다.

<a name="naming-batches"></a>
#### 배치 이름 지정하기

Laravel Horizon, Laravel Telescope 같은 도구들은 배치에 이름이 지정되어 있으면 더 직관적인 디버그 정보를 제공해줍니다. 임의의 이름을 배치에 지정하려면, 배치 정의 시 `name` 메서드를 호출하면 됩니다.

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // 모든 작업이 성공적으로 완료됨...
})->name('Import CSV')->dispatch();
```

<a name="batch-connection-queue"></a>
#### 배치 연결 및 큐 지정

배치로 실행되는 작업들이 사용할 연결 및 큐를 지정하려면, `onConnection` 및 `onQueue` 메서드를 사용할 수 있습니다. 모든 배치 작업은 동일한 연결과 큐에서 실행되어야 합니다.

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // 모든 작업이 성공적으로 완료됨...
})->onConnection('redis')->onQueue('imports')->dispatch();
```

<a name="chains-and-batches"></a>
### 체이닝(Chaining)과 배치

여러 [체이닝된 작업](#job-chaining)을 한 배치 안에 배열로 넣어 정의할 수 있습니다. 예를 들어, 두 개의 작업 체인을 동시에 병렬로 실행하고, 두 체인 모두 끝났을 때 콜백을 실행할 수 있습니다.

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

반대로, [체이닝](#job-chaining) 안에 배치들을 넣는 것도 가능합니다. 예를 들어 여러 podcast를 발행하는 작업 배치를 실행한 후, 알림을 보내는 작업 배치를 순차적으로 실행할 수 있습니다.

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
### 배치에 작업 추가하기

때로는 배치 작업 내부에서, 해당 배치에 추가 작업을 더 동적으로 추가해야 할 때가 있습니다. 예를 들어, 너무 많은 작업을 한 번에 디스패치하기에는 웹 요청 시간이 오래 걸릴 수 있기에, 일종의 "로더" 역할의 작업을 배치로 등록해 로딩 중에 추가 작업을 계속 추가하도록 설계할 수 있습니다.

```php
$batch = Bus::batch([
    new LoadImportBatch,
    new LoadImportBatch,
    new LoadImportBatch,
])->then(function (Batch $batch) {
    // 모든 작업이 성공적으로 완료됨...
})->name('Import Contacts')->dispatch();
```

위 예제에서는 `LoadImportBatch` 작업이 동적으로 더 많은 작업을 추가하는 역할을 합니다. 이를 위해 작업의 `batch` 메서드를 이용해 `add` 메서드로 추가 작업을 등록하면 됩니다.

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
> 배치에 작업을 추가하는 작업 역시 동일한 배치에 소속된 작업에서만 해야 합니다.

<a name="inspecting-batches"></a>
### 배치 정보 조회하기

배치 완료 콜백에서 제공받는 `Illuminate\Bus\Batch` 인스턴스를 사용하면, 해당 배치와 관련된 다양한 정보를 확인하거나 조작할 수 있습니다.

```php
// 배치 UUID
$batch->id;

// 배치 이름(있는 경우)
$batch->name;

// 배치에 할당된 작업 수
$batch->totalJobs;

// 아직 처리되지 않은 작업 수
$batch->pendingJobs;

// 실패한 작업 수
$batch->failedJobs;

// 현재까지 처리된 작업 수
$batch->processedJobs();

// 전체 배치의 완료 비율(0~100)
$batch->progress();

// 배치 실행 완료 여부
$batch->finished();

// 배치 실행 취소
$batch->cancel();

// 배치가 취소되었는지 여부
$batch->cancelled();
```

<a name="returning-batches-from-routes"></a>
#### 라우트에서 배치 결과 반환하기

모든 `Illuminate\Bus\Batch` 인스턴스는 JSON 직렬화가 가능하므로, 애플리케이션의 라우트에서 직접 반환하여 배치 진행 상황 등을 JSON 응답으로 바로 제공할 수 있습니다. 이를 활용하면 UI에서 배치의 진행 상황을 편리하게 표시할 수 있습니다.

배치 ID로 배치를 조회하려면, `Bus` 파사드의 `findBatch` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Support\Facades\Bus;
use Illuminate\Support\Facades\Route;

Route::get('/batch/{batchId}', function (string $batchId) {
    return Bus::findBatch($batchId);
});
```

<a name="cancelling-batches"></a>
### 배치 취소

특정 배치의 실행을 중간에 취소하고 싶다면, `Illuminate\Bus\Batch` 인스턴스의 `cancel` 메서드를 호출하면 됩니다.

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

위 예제들에서 볼 수 있듯이, 배치 작업 내부에서는 실행을 시작하기 전에 해당 배치가 취소됐는지를 확인하는 것이 보통입니다. 하지만 더 편리하게 하려면 [미들웨어](#job-middleware)인 `SkipIfBatchCancelled`를 작업에 할당할 수 있습니다. 이 미들웨어는 배치가 취소된 경우 해당 작업을 실행하지 않도록 합니다.

```php
use Illuminate\Queue\Middleware\SkipIfBatchCancelled;

/**
 * 작업이 거칠 미들웨어 반환
 */
public function middleware(): array
{
    return [new SkipIfBatchCancelled];
}
```

<a name="batch-failures"></a>
### 배치 실패 처리

배치에 포함된 작업이 실패하면, `catch` 콜백이 등록되어 있다면 해당 콜백이 호출됩니다. 이 콜백은 배치에서 발생한 첫 번째 실패 작업에 대해서만 실행됩니다.

<a name="allowing-failures"></a>
#### 실패 허용하기

배치 내 작업 중 하나라도 실패하면, 라라벨은 기본적으로 해당 배치를 "취소됨" 상태로 표시합니다. 만약, 작업이 실패해도 배치가 자동으로 취소되지 않도록 하고 싶다면, 배치 디스패치 시 `allowFailures` 메서드를 사용하세요.

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // 모든 작업이 성공적으로 완료됨...
})->allowFailures()->dispatch();
```

<a name="retrying-failed-batch-jobs"></a>
#### 배치 내 실패한 작업 재시도

라라벨은 배치 내에서 실패한 모든 작업을 간편하게 재시도할 수 있도록 `queue:retry-batch` Artisan 명령어를 제공합니다. 이 명령어에 실패한 작업이 있는 배치의 UUID를 전달하면 됩니다.

```shell
php artisan queue:retry-batch 32dbc76c-4f82-4749-b610-a639fe0099b5
```

<a name="pruning-batches"></a>
### 배치 데이터 정리(Prune)

`job_batches` 테이블은 별도로 관리하지 않는 한, 빠르게 데이터가 쌓일 수 있습니다. 이를 방지하기 위해, [스케줄링 기능](/docs/12.x/scheduling)을 사용해 `queue:prune-batches` Artisan 명령어를 매일 실행하도록 설정하는 것이 좋습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches')->daily();
```

기본적으로 완료된 후 24시간이 지난 모든 배치가 정리(삭제)됩니다. 보존 기간을 더 길게 지정하고 싶다면, 명령어 호출 시 `hours` 옵션을 사용할 수 있습니다. 아래 명령어는 48시간 전에 끝난 모든 배치를 삭제합니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48')->daily();
```

때로는 `job_batches` 테이블에 성공적으로 끝나지 못한 배치(예: 일부 작업이 실패한 후 성공적으로 재시도되지 않은 경우) 데이터가 쌓일 수도 있습니다. 이 경우에는 `unfinished` 옵션을 사용하여 완료되지 않은 배치 데이터도 함께 정리할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48 --unfinished=72')->daily();
```

또한, 취소된 배치에 대한 데이터가 누적될 수도 있습니다. 이 경우에는 `cancelled` 옵션을 추가하여 취소된 배치 데이터도 정리할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48 --cancelled=72')->daily();
```

<a name="storing-batches-in-dynamodb"></a>

### DynamoDB에 배치 정보 저장

라라벨은 관계형 데이터베이스 대신 [DynamoDB](https://aws.amazon.com/dynamodb)에 배치 메타 정보를 저장하는 것도 지원합니다. 다만, 모든 배치 레코드를 저장할 DynamoDB 테이블을 직접 생성해야 합니다.

일반적으로 이 테이블의 이름은 `job_batches`로 지정하지만, 애플리케이션의 `queue` 설정 파일 내 `queue.batching.table` 설정값을 따라 테이블 이름을 지정해야 합니다.

<a name="dynamodb-batch-table-configuration"></a>
#### DynamoDB 배치 테이블 설정

`job_batches` 테이블은 `application`이라는 문자열 형식의 기본 파티션 키와, `id`라는 문자열 형식의 기본 정렬 키를 가져야 합니다. `application` 키에는 애플리케이션의 `app` 설정 파일 내 `name` 설정값이 저장됩니다. DynamoDB 테이블 키에 애플리케이션 이름이 포함되어 있기 때문에, 여러 라라벨 애플리케이션의 잡 배치를 동일한 테이블에 저장할 수 있습니다.

또한, [자동 배치 정리](#pruning-batches-in-dynamodb) 기능을 활용하고 싶다면 테이블에 `ttl` 속성을 정의해야 합니다.

<a name="dynamodb-configuration"></a>
#### DynamoDB 설정

다음으로, 라라벨 애플리케이션이 Amazon DynamoDB와 통신할 수 있도록 AWS SDK를 설치합니다.

```shell
composer require aws/aws-sdk-php
```

이후, `queue.batching.driver` 설정 옵션의 값을 `dynamodb`로 지정합니다. 그리고 `batching` 설정 배열 안에 `key`, `secret`, `region` 설정 옵션을 정의해야 합니다. 이 옵션들은 AWS 인증에 사용됩니다. `dynamodb` 드라이버를 사용하는 경우, `queue.batching.database` 옵션은 필요하지 않습니다.

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
#### DynamoDB에서 배치 정리

[Amazon DynamoDB](https://aws.amazon.com/dynamodb)에 잡 배치 정보를 저장하는 경우, 관계형 데이터베이스에 저장된 배치를 정리할 때 사용하는 명령어들은 사용할 수 없습니다. 대신, [DynamoDB의 기본 TTL 기능](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html)을 활용해 오래된 배치 레코드를 자동으로 삭제할 수 있습니다.

만약 테이블에 `ttl` 속성을 정의했다면, 라라벨에 배치 레코드를 어떻게 정리할지 안내하는 설정값을 지정할 수 있습니다. `queue.batching.ttl_attribute` 설정값은 TTL 값이 저장되는 속성의 이름을, `queue.batching.ttl` 설정값은 레코드가 마지막으로 업데이트된 후 얼마 뒤에 DynamoDB 테이블에서 배치 레코드를 제거할지(초 단위)를 지정합니다.

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
## 클로저를 큐잉하기

잡 클래스를 큐에 디스패치하는 대신, 클로저(익명 함수)를 큐에 디스패치할 수도 있습니다. 간단하게 요청 사이클 외부에서 실행해야 하는 빠른 작업에 적합한 방법입니다. 클로저를 큐에 디스패치하면, 클로저의 코드 내용은 암호화 서명되어 전송 중 변조될 수 없습니다.

```php
$podcast = App\Podcast::find(1);

dispatch(function () use ($podcast) {
    $podcast->publish();
});
```

큐잉된 클로저에 이름을 부여하고 싶다면, `name` 메서드를 사용할 수 있습니다. 이 이름은 큐 대시보드에서 사용되거나 `queue:work` 명령어에서 표시됩니다.

```php
dispatch(function () {
    // ...
})->name('Publish Podcast');
```

`catch` 메서드를 사용하면, 큐잉된 클로저가 [설정된 재시도 횟수](#max-job-attempts-and-timeout)를 모두 소진한 뒤에도 정상적으로 완료되지 않으면 실행될 클로저를 지정할 수 있습니다.

```php
use Throwable;

dispatch(function () use ($podcast) {
    $podcast->publish();
})->catch(function (Throwable $e) {
    // 이 잡은 실패했습니다...
});
```

> [!WARNING]
> `catch` 콜백은 시리얼라이즈되어 나중에 라라벨 큐에 의해 실행되므로, `catch` 콜백 내부에서 `$this` 변수를 사용해서는 안 됩니다.

<a name="running-the-queue-worker"></a>
## 큐 워커 실행

<a name="the-queue-work-command"></a>
### `queue:work` 명령어

라라벨에는 큐 워커를 시작하고 새 잡이 큐에 추가될 때마다 이를 처리하는 Artisan 명령어가 내장되어 있습니다. `queue:work` Artisan 명령어로 워커를 실행할 수 있습니다. 주의할 점은, `queue:work` 명령어를 실행하면 수동으로 중지하거나 터미널을 닫을 때까지 계속 실행된다는 것입니다.

```shell
php artisan queue:work
```

> [!NOTE]
> `queue:work` 프로세스를 백그라운드에서 항상 실행 상태로 유지하려면, [Supervisor](#supervisor-configuration) 같은 프로세스 모니터를 사용해 큐 워커가 멈추지 않도록 관리하는 것이 좋습니다.

명령어 실행 시 `-v` 플래그를 추가하면, 처리된 잡의 ID가 출력 결과에 포함됩니다.

```shell
php artisan queue:work -v
```

큐 워커는 장시간 실행되는 프로세스이며, 애플리케이션이 부팅된 상태가 메모리에 저장됩니다. 따라서 워커가 시작된 이후 코드 베이스의 변경을 감지하지 못합니다. 배포(deployment) 과정에서는 반드시 [큐 워커를 재시작](#queue-workers-and-deployment)해야 하며, 애플리케이션에서 생성되거나 수정된 모든 정적 상태(static state)는 각 잡 사이에 자동으로 초기화되지 않는다는 점을 기억해야 합니다.

또는 `queue:listen` 명령어를 실행할 수도 있습니다. `queue:listen` 명령어를 사용하면, 코드가 변경되었거나 애플리케이션 상태를 재설정해야 할 때 워커를 직접 재시작할 필요가 없습니다. 그러나 이 명령어는 `queue:work` 명령어보다 효율이 훨씬 떨어집니다.

```shell
php artisan queue:listen
```

<a name="running-multiple-queue-workers"></a>
#### 다수의 큐 워커 실행

하나의 큐에 여러 워커를 할당해 동시에 여러 잡을 처리하려면, `queue:work` 프로세스를 여러 개 실행하면 됩니다. 이 작업은 로컬에서는 터미널의 여러 탭으로 가능하며, 프로덕션 환경에서는 프로세스 매니저(예: [Supervisor](#supervisor-configuration))의 설정을 활용할 수 있습니다. Supervisor의 경우, `numprocs` 설정값을 사용할 수 있습니다.

<a name="specifying-the-connection-queue"></a>
#### 커넥션과 큐 지정

워커가 사용할 큐 커넥션을 직접 지정할 수도 있습니다. `work` 명령어에 넘기는 커넥션 이름은 `config/queue.php` 설정 파일에 정의된 커넥션 이름 중 하나여야 합니다.

```shell
php artisan queue:work redis
```

기본적으로 `queue:work` 명령어는 해당 커넥션의 기본 큐만 처리합니다. 그러나 특정 커넥션에서 특정 큐만 처리하도록 워커를 좀 더 세밀하게 조정할 수 있습니다. 예를 들어, 모든 이메일 관련 잡이 `redis` 커넥션의 `emails` 큐에 있고, 해당 큐만 처리하는 워커를 실행하려면 아래와 같이 명령어를 입력합니다.

```shell
php artisan queue:work redis --queue=emails
```

<a name="processing-a-specified-number-of-jobs"></a>
#### 지정된 개수의 잡만 처리

`--once` 옵션을 사용하면 워커가 큐에서 단 하나의 잡만 처리하도록 할 수 있습니다.

```shell
php artisan queue:work --once
```

`--max-jobs` 옵션을 사용하면 워커가 지정한 개수만큼 잡을 처리한 후 종료됩니다. 이 옵션은 [Supervisor](#supervisor-configuration)와 함께 사용하면, 워커가 일정량의 잡을 처리한 뒤 자동으로 재시작되어 누적된 메모리가 해제되는 효과가 있습니다.

```shell
php artisan queue:work --max-jobs=1000
```

<a name="processing-all-queued-jobs-then-exiting"></a>
#### 전체 잡 처리 후 종료하기

`--stop-when-empty` 옵션을 사용하면 큐에 남아있는 모든 잡을 처리한 뒤 워커가 정상적으로 종료됩니다. 이 옵션은 라라벨 큐를 Docker 컨테이너에서 처리하는 경우, 큐가 비워졌을 때 컨테이너를 안전하게 종료하려는 상황에 유용합니다.

```shell
php artisan queue:work --stop-when-empty
```

<a name="processing-jobs-for-a-given-number-of-seconds"></a>
#### 지정된 시간 동안 잡 처리

`--max-time` 옵션을 사용하면 워커가 정해진 시간(초) 동안 잡을 처리한 뒤 종료합니다. 이 옵션 역시 [Supervisor](#supervisor-configuration)와 같이 활용하면, 일정 시간마다 워커를 자동으로 재시작하여 누적된 메모리를 해제하는 데 도움이 됩니다.

```shell
# 1시간 동안 잡을 처리한 뒤 종료...
php artisan queue:work --max-time=3600
```

<a name="worker-sleep-duration"></a>
#### 워커 대기 시간(sleep duration)

큐에 잡이 있을 때는 워커가 쉬지 않고 계속해서 잡을 처리합니다. 하지만, 큐에 잡이 없을 때 워커가 몇 초 동안 대기(슬립)할지를 `sleep` 옵션으로 설정할 수 있습니다. 워커가 대기 중일 때는 새 잡을 처리하지 않습니다.

```shell
php artisan queue:work --sleep=3
```

<a name="maintenance-mode-queues"></a>
#### 유지보수 모드와 큐

애플리케이션이 [유지보수 모드](/docs/12.x/configuration#maintenance-mode)일 때는 큐잉된 잡이 처리되지 않습니다. 애플리케이션이 유지보수 모드에서 해제되면, 잡 처리는 정상적으로 재개됩니다.

유지보수 모드 상태에서도 큐 워커가 잡을 처리하도록 강제하려면, `--force` 옵션을 사용할 수 있습니다.

```shell
php artisan queue:work --force
```

<a name="resource-considerations"></a>
#### 리소스 관리 유의사항

데몬 큐 워커는 잡을 처리할 때마다 프레임워크를 "재부팅"하지 않습니다. 따라서 각 잡이 끝날 때마다 무거운 리소스(예: 이미지 작업 시 GD 라이브러리)가 있다면 반드시 해제해야 합니다. 예를 들어, 이미지를 처리할 때는 작업이 끝난 후 `imagedestroy`로 메모리를 해제해야 합니다.

<a name="queue-priorities"></a>
### 큐 우선순위

큐가 처리되는 순서를 조정하고 싶은 경우도 있습니다. 예를 들어, `config/queue.php` 설정 파일에서 `redis` 커넥션의 기본 `queue`를 `low`로 설정한다고 하더라도, 때로는 잡을 `high` 우선순위 큐에 할당하고 싶을 수 있습니다.

```php
dispatch((new Job)->onQueue('high'));
```

`work` 명령어에 콤마로 구분된 큐 이름 목록을 전달하면, 지정한 순서대로 큐를 처리하는 워커를 실행할 수 있습니다. 즉, `high` 큐의 모든 잡이 먼저 처리되고 그다음에 `low` 큐의 잡이 처리됩니다.

```shell
php artisan queue:work --queue=high,low
```

<a name="queue-workers-and-deployment"></a>
### 큐 워커와 배포

큐 워커는 장기간 실행되는 프로세스이기 때문에, 코드가 변경되어도 워커를 재시작하지 않으면 변경 사항을 감지할 수 없습니다. 따라서 큐 워커를 사용하는 애플리케이션을 배포할 때 가장 간단한 방법은 배포 과정에서 워커를 재시작하는 것입니다. `queue:restart` 명령어를 실행하면 모든 워커가 현재 처리 중인 잡을 끝낸 뒤 정상적으로 종료되도록 안내할 수 있습니다.

```shell
php artisan queue:restart
```

이 명령어는 모든 큐 워커에게 현재 처리 중인 잡을 마친 뒤 정상 종료하라는 신호를 보냅니다. 이때 작업 중이던 잡 데이터가 유실되지 않습니다. 워커가 종료된 후 다시 자동으로 큐 워커가 실행되게 하려면 [Supervisor](#supervisor-configuration) 같은 프로세스 매니저를 사용해야 합니다.

> [!NOTE]
> 큐 워커 재시작 신호는 [캐시](/docs/12.x/cache)에 저장되므로, 이 기능을 사용하기 전에 애플리케이션에 적절하게 캐시 드라이버가 설정되어 있는지 확인해야 합니다.

<a name="job-expirations-and-timeouts"></a>
### 잡 만료 및 타임아웃

<a name="job-expiration"></a>
#### 잡 만료(Expiration)

`config/queue.php` 설정 파일에서 각 큐 커넥션은 `retry_after` 옵션을 가지고 있습니다. 이 옵션은 잡이 처리되는 중 지정한 초만큼 시간이 경과하면 다시 잡을 큐에 반환할지 여부를 결정합니다. 예를 들어, `retry_after` 값을 90으로 지정하면, 잡이 90초 동안 처리되지 않고 반환(release)되거나 삭제(delete)되지 않을 경우 큐에 다시 올라가게 됩니다. 일반적으로 이 값은 잡이 합리적으로 완료되는 데 걸리는 최대 시간을 기준으로 설정해야 합니다.

> [!WARNING]
> Amazon SQS 커넥션만 예외적으로 `retry_after` 값을 사용하지 않습니다. SQS는 [기본 Visibility Timeout](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/AboutVT.html) 값을 사용하며, 이는 AWS 콘솔에서 관리합니다.

<a name="worker-timeouts"></a>
#### 워커 타임아웃

`queue:work` Artisan 명령어에는 `--timeout` 옵션이 있습니다. 기본값은 60초입니다. 만약 잡이 지정한 초보다 오래 실행되면, 잡을 처리하던 워커는 에러와 함께 종료됩니다. 일반적으로 [서버에 구성된 프로세스 매니저](#supervisor-configuration)에 의해 워커는 자동으로 재시작됩니다.

```shell
php artisan queue:work --timeout=60
```

`retry_after` 설정 옵션과 `--timeout` CLI 옵션은 서로 다르지만, 잡이 유실되지 않고 한 번만 성공적으로 처리되도록 협력합니다.

> [!WARNING]
> 항상 `--timeout` 값을 `retry_after` 설정값보다 몇 초 더 짧게 지정해야 합니다. 그래야 멈춰버린 워커가 재시도 전에 우선 종료되어, 동일 잡이 두 번 처리되는 상황을 막을 수 있습니다. 만약 `--timeout` 옵션이 `retry_after` 값보다 길다면, 잡이 반복해서 처리될 수 있습니다.

<a name="supervisor-configuration"></a>
## Supervisor 구성

운영 환경에서는 `queue:work` 프로세스를 항상 실행 상태로 유지해야 합니다. 워커 프로세스는 여러 가지 원인(워커 타임아웃 초과, `queue:restart` 명령어 등)으로 인해 중단될 수 있습니다.

이런 이유로, `queue:work` 프로세스가 종료되면 자동으로 감지하여 다시 시작할 프로세스 모니터가 필요합니다. 또한, 프로세스 모니터를 사용하면 동시에 몇 개의 `queue:work` 프로세스를 실행할지도 지정할 수 있습니다. 리눅스 환경에서 가장 보편적으로 사용하는 프로세스 모니터가 Supervisor이며, 아래에서 자세히 다룹니다.

<a name="installing-supervisor"></a>
#### Supervisor 설치

Supervisor는 리눅스 운영체제에서 워커를 자동으로 재시작해주는 프로세스 감시 도구입니다. 우분투 환경에서는 다음 명령어로 Supervisor를 설치할 수 있습니다.

```shell
sudo apt-get install supervisor
```

> [!NOTE]
> Supervisor를 직접 설치·관리하는 것이 부담스럽게 느껴진다면, [Laravel Cloud](https://cloud.laravel.com)의 완전관리형 큐 워커 플랫폼을 고려해볼 수 있습니다.

<a name="configuring-supervisor"></a>
#### Supervisor 설정

Supervisor 설정 파일은 보통 `/etc/supervisor/conf.d` 디렉터리에 저장됩니다. 이 디렉터리 안에 여러 개의 설정 파일을 작성해서 Supervisor가 각각의 프로세스를 어떻게 감시할지 지정할 수 있습니다. 예를 들어, `laravel-worker.conf` 파일을 만들어 `queue:work` 프로세스를 실행·감시하도록 설정할 수 있습니다.

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

이 예제에서 `numprocs` 지시자는 Supervisor가 8개의 `queue:work` 프로세스를 동시에 실행·감시함을 의미합니다. 각 항목을 실제 환경에 맞게 변경하여 사용해야 합니다(예: `command` 부분의 큐 커넥션이나 옵션).

> [!WARNING]
> `stopwaitsecs` 값이 가장 오래 걸리는 잡의 실행 시간보다 커야 합니다. 이 값이 부족하면 Supervisor가 잡이 끝나기도 전에 작업을 중단시킬 수 있습니다.

<a name="starting-supervisor"></a>
#### Supervisor 시작

설정 파일을 만들고 나면, 다음 명령어로 Supervisor 설정을 반영하고 작업을 시작할 수 있습니다.

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start "laravel-worker:*"
```

Supervisor에 관한 더 자세한 정보는 [Supervisor 공식 문서](http://supervisord.org/index.html)를 참고하십시오.

<a name="dealing-with-failed-jobs"></a>
## 실패한 잡 처리하기

큐잉된 잡이 실패하는 경우도 발생할 수 있습니다. 걱정하지 마세요! 라라벨에서는 [잡의 최대 시도 횟수 지정](#max-job-attempts-and-timeout)을 지원해, 비동기 잡이 지정한 횟수만큼 재시도한 후에도 실패하면 `failed_jobs` 데이터베이스 테이블에 저장됩니다. [동기식으로 디스패치된 잡](/docs/12.x/queues#synchronous-dispatching)이 실패하는 경우에는 이 테이블에 저장되지 않고, 예외는 즉시 애플리케이션에서 처리됩니다.

일반적으로 새 라라벨 애플리케이션에는 이미 `failed_jobs` 테이블 생성을 위한 마이그레이션 파일이 포함되어 있습니다. 만약 없다면, `make:queue-failed-table` 명령어로 마이그레이션을 생성할 수 있습니다.

```shell
php artisan make:queue-failed-table

php artisan migrate
```

[큐 워커](#running-the-queue-worker) 프로세스를 실행할 때, `queue:work` 명령어의 `--tries` 옵션으로 잡의 최대 시도 횟수를 지정할 수 있습니다. 값을 지정하지 않으면 각 잡 클래스의 `$tries` 속성값 또는 1회만 재시도합니다.

```shell
php artisan queue:work redis --tries=3
```

`--backoff` 옵션을 사용하면, 라라벨이 예외가 발생한 잡을 다시 시도하기 전에 대기할 초를 지정할 수 있습니다. 기본적으로는 예외가 발생한 잡이 곧바로 큐에 다시 올라갑니다.

```shell
php artisan queue:work redis --tries=3 --backoff=3
```

잡 클래스 자체에서 잡별로 예외 발생 후 재시도까지 대기할 시간을 지정하고 싶다면, 클래스에 `backoff` 속성 또는 메서드를 정의하면 됩니다.

```php
/**
 * 잡을 재시도하기 전 대기할 초.
 *
 * @var int
 */
public $backoff = 3;
```

좀 더 복잡한 로직이 필요하다면, `backoff` 메서드를 정의할 수 있습니다.

```php
/**
 * 잡을 재시도하기 전 대기할 초를 계산합니다.
 */
public function backoff(): int
{
    return 3;
}
```

"지수형" 재시도(backoff)가 필요하다면, `backoff` 메서드에서 배열로 값을 반환하면 됩니다. 아래 예시에서는 첫 번째 재시도는 1초, 두 번째는 5초, 세 번째는 10초, 이후 추가 재시도가 있다면 계속 10초씩 대기하게 됩니다.

```php
/**
 * 잡을 재시도하기 전 대기할 초를 계산합니다.
 *
 * @return array<int, int>
 */
public function backoff(): array
{
    return [1, 5, 10];
}
```

<a name="cleaning-up-after-failed-jobs"></a>
### 실패한 잡 정리(Clean-up)

특정 잡이 실패했을 때, 사용자에게 알림을 보내거나 이미 일부 완료된 작업을 되돌려야 할 수도 있습니다. 이를 위해 잡 클래스에 `failed` 메서드를 정의할 수 있습니다. 잡이 실패한 원인이 되는 `Throwable` 인스턴스가 해당 메서드에 전달됩니다.

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
     * 새 잡 인스턴스 생성자.
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

    /**
     * 잡 실패 처리.
     */
    public function failed(?Throwable $exception): void
    {
        // 사용자에게 실패 알림 전송 등...
    }
}
```

> [!WARNING]
> `failed` 메서드는 새롭게 인스턴스화된 잡에서 실행되므로, `handle` 메서드 내에서 변경된 속성(property)은 이 단계에서 반영되지 않습니다.

<a name="retrying-failed-jobs"></a>
### 실패한 잡 재시도

`failed_jobs` 데이터베이스에 저장된 모든 실패한 잡 목록은 `queue:failed` Artisan 명령어로 확인할 수 있습니다.

```shell
php artisan queue:failed
```

`queue:failed` 명령어로 출력된 잡 ID는, 이후 해당 잡을 재시도할 때 사용할 수 있습니다. 예를 들어, ID가 `ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece`인 잡을 재시도하려면 다음과 같이 명령어를 입력합니다.

```shell
php artisan queue:retry ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece
```

필요하다면 여러 ID를 동시에 넘길 수도 있습니다.

```shell
php artisan queue:retry ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece 91401d2c-0784-4f43-824c-34f94a33c24d
```

특정 큐에 속한 모든 실패한 잡만 개별적으로 재시도할 수도 있습니다.

```shell
php artisan queue:retry --queue=name
```

모든 실패 잡을 한 번에 재시도하려면, ID 대신 `all`을 인자로 전달합니다.

```shell
php artisan queue:retry all
```

실패한 잡 정보를 삭제하고 싶다면, `queue:forget` 명령어를 사용할 수 있습니다.

```shell
php artisan queue:forget 91401d2c-0784-4f43-824c-34f94a33c24d
```

> [!NOTE]
> [Horizon](/docs/12.x/horizon)을 사용할 경우에는, `queue:forget` 명령어 대신 `horizon:forget` 명령어로 실패한 잡을 삭제해야 합니다.

`failed_jobs` 테이블에서 모든 실패한 잡을 한 번에 삭제하려면, `queue:flush` 명령어를 사용하면 됩니다.

```shell
php artisan queue:flush
```

<a name="ignoring-missing-models"></a>
### 없는 모델 무시하기

잡에 Eloquent 모델 인스턴스를 주입하면, 잡이 큐에 들어갈 때 모델이 자동으로 시리얼라이즈되고, 잡을 처리할 때 데이터베이스에서 다시 조회됩니다. 그러나 잡이 대기 중인 동안 모델이 삭제되어 버렸다면, `ModelNotFoundException` 예외로 잡이 실패할 수 있습니다.

이런 경우, 잡 클래스의 `deleteWhenMissingModels` 속성을 `true`로 설정하면, 해당 모델이 없을 때 예외를 던지지 않고 조용히 잡을 삭제할 수 있습니다.

```php
/**
 * 잡에 연결된 모델이 더 이상 없으면 잡을 삭제할지 여부.
 *
 * @var bool
 */
public $deleteWhenMissingModels = true;
```

<a name="pruning-failed-jobs"></a>
### 실패한 잡 정리(Pruning)

애플리케이션의 `failed_jobs` 테이블에 쌓인 레코드는 `queue:prune-failed` Artisan 명령어로 정리(prune)할 수 있습니다.

```shell
php artisan queue:prune-failed
```

기본적으로는 생성된 지 24시간이 지난 모든 레코드가 삭제(prune)됩니다. `--hours` 옵션을 전달하면, 최근 N시간 이내에 생성된 실패 잡만 남겨둡니다. 예를 들어 아래 명령어는 48시간 이상 지난 잡만 삭제합니다.

```shell
php artisan queue:prune-failed --hours=48
```

<a name="storing-failed-jobs-in-dynamodb"></a>
### 실패한 잡을 DynamoDB에 저장

라라벨은 [DynamoDB](https://aws.amazon.com/dynamodb)를 활용해 실패한 잡을 관계형 데이터베이스가 아닌 DynamoDB 테이블에 저장하는 것도 지원합니다. 이 경우 역시 모든 실패 잡 레코드를 저장할 DynamoDB 테이블을 직접 만들어야 합니다. 일반적으로 테이블 이름은 `failed_jobs`로 지정하나, 애플리케이션의 `queue.failed.table` 설정값에 따라 다를 수 있습니다.

`failed_jobs` 테이블은 문자열 형식의 기본 파티션 키 `application`과, 문자열 형식의 기본 정렬 키 `uuid`를 가져야 합니다. `application` 키에는 애플리케이션의 `app` 설정 파일의 `name` 값이 들어갑니다. 때문에 여러 라라벨 애플리케이션의 실패한 잡 정보를 동일한 테이블에 저장할 수 있습니다.

그리고 라라벨 애플리케이션이 Amazon DynamoDB와 통신할 수 있도록 반드시 AWS SDK를 설치해야 합니다.

```shell
composer require aws/aws-sdk-php
```

다음으로, `queue.failed.driver` 설정값을 `dynamodb`로 지정합니다. 또, 실패한 잡 설정 배열 안에 `key`, `secret`, `region` 설정 옵션을 정의해야 합니다. 이 옵션들은 AWS 인증에 사용됩니다. `dynamodb` 드라이버 사용 시에는 `queue.failed.database` 옵션을 지정할 필요가 없습니다.

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
### 실패 잡 저장 비활성화

`queue.failed.driver` 설정값을 `null`로 지정하면, 라라벨이 실패한 잡을 저장하지 않도록 할 수 있습니다. 일반적으로는 `QUEUE_FAILED_DRIVER` 환경 변수로 쉽게 지정합니다.

```ini
QUEUE_FAILED_DRIVER=null
```

<a name="failed-job-events"></a>
### 실패 잡 이벤트

잡이 실패할 때 실행되는 이벤트 리스너를 등록하려면, `Queue` 파사드의 `failing` 메서드를 사용할 수 있습니다. 예를 들어, 라라벨의 `AppServiceProvider`의 `boot` 메서드에서 아래와 같이 이벤트 핸들러(클로저)를 등록할 수 있습니다.

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Queue;
use Illuminate\Support\ServiceProvider;
use Illuminate\Queue\Events\JobFailed;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 등록.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * 애플리케이션 서비스 부트스트랩.
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

## 큐에서 작업 삭제하기

> [!NOTE]
> [Horizon](/docs/12.x/horizon)을 사용하고 있다면, 작업을 큐에서 삭제할 때는 `queue:clear` 명령어 대신 `horizon:clear` 명령어를 사용해야 합니다.

기본 연결의 기본 큐에 있는 모든 작업을 삭제하고 싶다면, 아래와 같이 `queue:clear` 아티즌 명령어를 실행하면 됩니다.

```shell
php artisan queue:clear
```

특정 연결과 큐의 작업만 삭제하고 싶을 때는 `connection` 인수와 `queue` 옵션을 함께 지정할 수 있습니다.

```shell
php artisan queue:clear redis --queue=emails
```

> [!WARNING]
> 큐에서 작업을 삭제하는 기능은 SQS, Redis, 데이터베이스 큐 드라이버에서만 사용할 수 있습니다. 또한 SQS 메시지 삭제 과정은 최대 60초가 걸릴 수 있으므로, 큐를 삭제한 후 60초 이내에 SQS 큐로 전송된 작업도 함께 삭제될 수 있습니다.

<a name="monitoring-your-queues"></a>
## 큐 모니터링하기

큐에 갑자기 많은 작업이 몰리면, 처리 지연이 길어질 수 있습니다. 이럴 때 라라벨이 큐에 쌓인 작업 수가 특정 임계값을 초과하면 알림을 보내도록 설정할 수 있습니다.

먼저, `queue:monitor` 명령어를 [매 분마다 실행](/docs/12.x/scheduling)되도록 스케줄링해야 합니다. 이 명령어에는 모니터링할 큐의 이름과 감시하고 싶은 작업 수 임계값을 지정할 수 있습니다.

```shell
php artisan queue:monitor redis:default,redis:deployments --max=100
```

이 명령어를 스케줄링하는 것만으로는 큐가 과부하 상태일 때 알림이 발생하지 않습니다. 명령어가 임계값을 초과한 큐를 발견하면 `Illuminate\Queue\Events\QueueBusy` 이벤트를 발생시킵니다. 애플리케이션의 `AppServiceProvider`에서 이 이벤트를 감지하여, 본인이나 팀원에게 알림을 보낼 수 있습니다.

```php
use App\Notifications\QueueHasLongWaitTime;
use Illuminate\Queue\Events\QueueBusy;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\Facades\Notification;

/**
 * 애플리케이션 서비스를 부트스트랩합니다.
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
## 테스트

작업을 디스패치하는 코드를 테스트할 때는, 실제로 작업이 실행되지 않도록 라라벨에 지시할 수 있습니다. 작업 자체의 코드는 디스패치 코드와는 별개로 직접 테스트할 수 있습니다. 즉, 작업 자체를 테스트하고 싶다면 인스턴스화 후 테스트에서 직접 `handle` 메서드를 호출할 수 있습니다.

실제로 작업이 큐에 들어가지 않도록 하려면 `Queue` 파사드의 `fake` 메서드를 사용하세요. `Queue::fake()`를 호출한 후, 작업이 큐에 들어갔는지를 다양한 방법으로 검증할 수 있습니다.

```php tab=Pest
<?php

use App\Jobs\AnotherJob;
use App\Jobs\FinalJob;
use App\Jobs\ShipOrder;
use Illuminate\Support\Facades\Queue;

test('orders can be shipped', function () {
    Queue::fake();

    // 주문 배송 작업 실행...

    // 작업이 아무것도 큐에 등록되지 않았는지 확인...
    Queue::assertNothingPushed();

    // 특정 큐에 작업이 등록되었는지 확인...
    Queue::assertPushedOn('queue-name', ShipOrder::class);

    // 작업이 두 번 등록되었는지 확인...
    Queue::assertPushed(ShipOrder::class, 2);

    // 특정 작업이 등록되지 않았는지 확인...
    Queue::assertNotPushed(AnotherJob::class);

    // 클로저 작업이 큐에 등록되었는지 확인...
    Queue::assertClosurePushed();

    // 총 등록된 작업 개수 확인...
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

        // 주문 배송 작업 실행...

        // 작업이 아무것도 큐에 등록되지 않았는지 확인...
        Queue::assertNothingPushed();

        // 특정 큐에 작업이 등록되었는지 확인...
        Queue::assertPushedOn('queue-name', ShipOrder::class);

        // 작업이 두 번 등록되었는지 확인...
        Queue::assertPushed(ShipOrder::class, 2);

        // 특정 작업이 등록되지 않았는지 확인...
        Queue::assertNotPushed(AnotherJob::class);

        // 클로저 작업이 큐에 등록되었는지 확인...
        Queue::assertClosurePushed();

        // 총 등록된 작업 개수 확인...
        Queue::assertCount(3);
    }
}
```

`assertPushed` 또는 `assertNotPushed` 메서드에 클로저를 전달하면, 전달한 "진리성 검사"를 통과하는 작업이 큐에 등록되었는지 추가로 검증할 수 있습니다. 조건을 충족하는 작업이 한 건이라도 등록되어 있으면 검증이 통과합니다.

```php
Queue::assertPushed(function (ShipOrder $job) use ($order) {
    return $job->order->id === $order->id;
});
```

<a name="faking-a-subset-of-jobs"></a>
### 일부 작업만 페이크로 처리하기

특정 작업만 페이크로 처리하고 나머지는 실제로 실행하려면, `fake` 메서드에 페이크로 처리할 작업 클래스명을 배열로 전달하면 됩니다.

```php tab=Pest
test('orders can be shipped', function () {
    Queue::fake([
        ShipOrder::class,
    ]);

    // 주문 배송 작업 실행...

    // 작업이 두 번 등록되었는지 확인...
    Queue::assertPushed(ShipOrder::class, 2);
});
```

```php tab=PHPUnit
public function test_orders_can_be_shipped(): void
{
    Queue::fake([
        ShipOrder::class,
    ]);

    // 주문 배송 작업 실행...

    // 작업이 두 번 등록되었는지 확인...
    Queue::assertPushed(ShipOrder::class, 2);
}
```

특정 작업만 제외하고 나머지 모든 작업을 페이크로 처리하려면, `except` 메서드를 사용하세요.

```php
Queue::fake()->except([
    ShipOrder::class,
]);
```

<a name="testing-job-chains"></a>
### 작업 체인 테스트하기

작업 체인에 대한 테스트는 `Bus` 파사드의 페이크 기능을 활용하면 됩니다. `Bus::assertChained` 메서드는 [작업 체인](/docs/12.x/queues#job-chaining)이 디스패치되었는지 검증합니다. 첫 번째 인수로 연결된 작업의 배열을 넘길 수 있습니다.

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

위 예시처럼, 연결된 작업들을 클래스명으로 배열에 넣어 전달할 수 있습니다. 또는, 실제 작업 인스턴스의 배열을 전달해도 됩니다. 이 경우 라라벨은 작업 인스턴스의 클래스와 속성 값이 디스패치된 작업과 동일한지 확인합니다.

```php
Bus::assertChained([
    new ShipOrder,
    new RecordShipment,
    new UpdateInventory,
]);
```

`assertDispatchedWithoutChain` 메서드를 사용하면, 체인 없이 단독으로 디스패치된 작업이 있는지 검증할 수 있습니다.

```php
Bus::assertDispatchedWithoutChain(ShipOrder::class);
```

<a name="testing-chain-modifications"></a>
#### 체인 추가/수정 테스트하기

체인에 [작업을 앞이나 뒤에 추가](#adding-jobs-to-the-chain)하는 경우, 작업 인스턴스의 `assertHasChain` 메서드를 통해 남아있는 작업 체인이 기대한 값과 일치하는지 검증할 수 있습니다.

```php
$job = new ProcessPodcast;

$job->handle();

$job->assertHasChain([
    new TranscribePodcast,
    new OptimizePodcast,
    new ReleasePodcast,
]);
```

`assertDoesntHaveChain` 메서드를 사용하면, 작업의 남은 체인이 비어있는지 검증할 수 있습니다.

```php
$job->assertDoesntHaveChain();
```

<a name="testing-chained-batches"></a>
#### 체인 내부의 배치 작업 테스트하기

작업 체인에 [배치 작업이 포함된 경우](#chains-and-batches), 체인 검증 시 `Bus::chainedBatch` 정의를 포함하여 기대하는 배치 작업이 맞게 등록되었는지 확인할 수 있습니다.

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
### 작업 배치 테스트하기

`Bus` 파사드의 `assertBatched` 메서드를 사용하면, [작업 배치](/docs/12.x/queues#job-batching)가 디스패치 되었는지 검증할 수 있습니다. `assertBatched`에 넘기는 클로저는 `Illuminate\Bus\PendingBatch` 인스턴스를 받아, 배치 내의 작업들을 검사할 수 있습니다.

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

`assertBatchCount` 메서드를 사용하면, 디스패치된 배치의 개수를 검증할 수 있습니다.

```php
Bus::assertBatchCount(3);
```

`assertNothingBatched`로 어떤 배치도 디스패치되지 않았는지 확인할 수도 있습니다.

```php
Bus::assertNothingBatched();
```

<a name="testing-job-batch-interaction"></a>
#### 개별 작업의 배치 상호작용 테스트

특정 작업이 속한 배치와 상호작용하는 시나리오(예: 작업이 배치의 나머지 작업 처리를 취소하는 경우 등)를 테스트할 필요가 있을 수 있습니다. 이럴 때는 `withFakeBatch` 메서드로 작업에 페이크 배치를 할당할 수 있습니다. 이 메서드는 작업 인스턴스와 페이크 배치의 튜플을 반환합니다.

```php
[$job, $batch] = (new ShipOrder)->withFakeBatch();

$job->handle();

$this->assertTrue($batch->cancelled());
$this->assertEmpty($batch->added);
```

<a name="testing-job-queue-interactions"></a>
### 작업과 큐 상호작용 테스트

작업이 [자신을 다시 큐에 등록](#manually-releasing-a-job)하거나, 스스로를 삭제하는 등의 큐 상호작용을 테스트해야 하는 경우가 있습니다. 이때 작업을 인스턴스화하고 `withFakeQueueInteractions` 메서드를 호출하면, 큐 상호작용을 페이크로 처리할 수 있습니다.

작업의 큐 상호작용을 페이크로 만든 후, `handle` 메서드를 호출하면 됩니다. 이후 `assertReleased`, `assertDeleted`, `assertNotDeleted`, `assertFailed`, `assertFailedWith`, `assertNotFailed` 등의 메서드로 작업의 큐 상호작용 결과를 검증할 수 있습니다.

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
## 작업 이벤트

`Queue` [파사드](/docs/12.x/facades)의 `before` 및 `after` 메서드를 사용하면, 큐에 등록된 작업이 처리되기 전이나 후에 실행할 콜백을 지정할 수 있습니다. 이런 콜백은 로그 기록이나 대시보드의 통계 집계 등에 활용할 수 있습니다. 보통은 [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에서 이 작업을 진행합니다. 다음은 라라벨 기본 제공 `AppServiceProvider`에서 사용할 수 있는 예시입니다.

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
     * 애플리케이션 서비스 등록.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * 애플리케이션 서비스 부트스트랩.
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

또한 `Queue` [파사드](/docs/12.x/facades)의 `looping` 메서드를 사용하면, 워커가 큐에서 작업을 가져오기 직전에 실행할 콜백을 등록할 수 있습니다. 예를 들어, 이전에 실패한 작업으로 인해 열린 상태로 남아 있는 트랜잭션이 있으면 이를 롤백하도록 클로저를 등록할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Queue;

Queue::looping(function () {
    while (DB::transactionLevel() > 0) {
        DB::rollBack();
    }
});
```