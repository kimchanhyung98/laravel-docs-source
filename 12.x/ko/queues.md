# 큐 (Queues)

- [소개](#introduction)
    - [커넥션과 큐의 차이](#connections-vs-queues)
    - [드라이버별 참고사항 및 선행조건](#driver-prerequisites)
- [잡 생성하기](#creating-jobs)
    - [잡 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [고유 잡(Unique Jobs)](#unique-jobs)
    - [암호화된 잡](#encrypted-jobs)
- [잡 미들웨어](#job-middleware)
    - [속도 제한](#rate-limiting)
    - [잡 중첩 방지](#preventing-job-overlaps)
    - [예외 상황 제어(Throttling Exceptions)](#throttling-exceptions)
    - [잡 스킵(건너뛰기)](#skipping-jobs)
- [잡 디스패치하기](#dispatching-jobs)
    - [지연 디스패치하기](#delayed-dispatching)
    - [동기식 디스패치](#synchronous-dispatching)
    - [잡과 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [잡 체이닝](#job-chaining)
    - [큐와 커넥션 커스터마이즈](#customizing-the-queue-and-connection)
    - [최대 시도 횟수/타임아웃 값 지정하기](#max-job-attempts-and-timeout)
    - [에러 핸들링](#error-handling)
- [잡 배치 처리(Job Batching)](#job-batching)
    - [배치 가능한 잡 정의](#defining-batchable-jobs)
    - [배치 디스패치하기](#dispatching-batches)
    - [체인과 배치](#chains-and-batches)
    - [배치에 잡 추가하기](#adding-jobs-to-batches)
    - [배치 상태 확인](#inspecting-batches)
    - [배치 취소하기](#cancelling-batches)
    - [배치 실패 처리](#batch-failures)
    - [배치 정리(Pruning)](#pruning-batches)
    - [DynamoDB에 배치 저장하기](#storing-batches-in-dynamodb)
- [클로저 큐잉](#queueing-closures)
- [큐 워커 실행](#running-the-queue-worker)
    - [`queue:work` 명령어](#the-queue-work-command)
    - [큐 우선순위](#queue-priorities)
    - [큐 워커와 배포](#queue-workers-and-deployment)
    - [잡 만료 및 타임아웃](#job-expirations-and-timeouts)
- [Supervisor 설정](#supervisor-configuration)
- [실패한 잡 처리하기](#dealing-with-failed-jobs)
    - [실패 잡 후처리](#cleaning-up-after-failed-jobs)
    - [실패 잡 재시도](#retrying-failed-jobs)
    - [존재하지 않는 모델 무시](#ignoring-missing-models)
    - [실패한 잡 정리(Pruning)](#pruning-failed-jobs)
    - [DynamoDB에 실패 잡 저장하기](#storing-failed-jobs-in-dynamodb)
    - [실패 잡 저장 비활성화](#disabling-failed-job-storage)
    - [실패 잡 이벤트](#failed-job-events)
- [큐에서 잡 삭제하기](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [일부 잡만 페이크 처리하기](#faking-a-subset-of-jobs)
    - [잡 체인 테스트](#testing-job-chains)
    - [잡 배치 테스트](#testing-job-batches)
    - [잡/큐 상호작용 테스트](#testing-job-queue-interactions)
- [잡 이벤트](#job-events)

<a name="introduction"></a>
## 소개

웹 애플리케이션을 개발하다 보면 업로드된 CSV 파일을 파싱하고 저장하는 등, 일반적인 웹 요청 처리 중에는 너무 오래 걸리는 작업이 있을 수 있습니다. 다행히도 라라벨은 이러한 작업을 백그라운드에서 처리할 수 있도록, 쉽고 간편하게 큐에 등록하여 실행될 수 있는 잡(job)을 만들 수 있는 기능을 제공합니다. 시간 소모가 큰 작업을 큐로 분리하면, 애플리케이션이 웹 요청에 더욱 빠르게 응답할 수 있어 사용자에게 더 좋은 경험을 제공할 수 있습니다.

라라벨 큐 시스템은 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 또는 관계형 데이터베이스 등 다양한 백엔드 큐 시스템을 아우르는 통합된 큐 API를 제공합니다.

라라벨의 큐 설정 옵션들은 애플리케이션의 `config/queue.php` 설정 파일에 저장되어 있습니다. 이 파일에는 프레임워크에 포함된 각 큐 드라이버(데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 등)와, 개발 환경에서 바로 잡을 실행하는 동기식 드라이버(즉시 실행), 그리고 큐에 등록된 잡을 모두 폐기처리하는 `null` 드라이버에 대한 커넥션 설정 정보를 확인할 수 있습니다.

> [!NOTE]
> 라라벨은 Redis 기반 큐를 위한 아름답고 편리한 대시보드 및 설정 시스템인 Horizon을 제공합니다. 자세한 내용은 [Horizon 공식 문서](/docs/12.x/horizon)를 참고하세요.

<a name="connections-vs-queues"></a>
### 커넥션과 큐의 차이

라라벨 큐를 본격적으로 사용하기에 앞서, 반드시 "커넥션(connection)"과 "큐(queue)"의 차이점을 이해해야 합니다. `config/queue.php` 설정 파일에는 `connections` 배열이 있습니다. 이 옵션은 Amazon SQS, Beanstalk, Redis 등 다양한 백엔드 큐 서비스와 통신하기 위한 커넥션을 정의합니다. 그러나 하나의 큐 커넥션 안에는 여러 "큐"가 존재할 수 있습니다. 각각의 큐는 작업이 쌓이는 별도의 공간, 즉 다른 작업을 구분하는 스택 또는 더미로 볼 수 있습니다.

각 큐 커넥션 설정 예제에서는 `queue`라는 속성이 포함되어 있습니다. 이 속성이 디스패치되는 잡이 기본으로 쌓일 큐를 지정합니다. 즉, 잡을 보낼 때 어떤 큐로 보낼지 명시하지 않으면, 커넥션 설정의 `queue` 속성에 지정된 큐로 잡이 전송됩니다:

```php
use App\Jobs\ProcessPodcast;

// 이 잡은 기본 커넥션의 기본 큐로 전송됩니다...
ProcessPodcast::dispatch();

// 이 잡은 기본 커넥션의 "emails" 큐로 전송됩니다...
ProcessPodcast::dispatch()->onQueue('emails');
```

어떤 애플리케이션은 여러 큐로 작업을 분산하지 않고, 하나의 간단한 큐만 사용하는 것이 더 적합할 수 있습니다. 하지만 여러 큐를 사용하면, 잡을 어떻게 처리할지 우선순위나 작업의 종류별로 분류하는 데 특히 유용합니다. 라라벨 큐 워커는 어떤 큐를 어떤 우선순위로 처리할지 지정할 수 있기 때문입니다. 예를 들어, `high`라는 큐에 잡을 보낸 경우, 해당 큐에 더 높은 처리 우선순위를 부여해 워커를 실행할 수도 있습니다:

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버별 참고사항 및 선행조건

<a name="database"></a>
#### 데이터베이스

`database` 큐 드라이버를 사용하려면 잡 정보를 저장할 데이터베이스 테이블이 필요합니다. 보통 라라벨의 기본 제공 마이그레이션인 `0001_01_01_000002_create_jobs_table.php` 파일에 이 테이블 생성 정보가 들어 있습니다. 만약 애플리케이션에 이 마이그레이션 파일이 없다면, `make:queue-table` Artisan 명령어로 직접 생성할 수 있습니다:

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면, `config/database.php` 설정 파일에서 Redis 데이터베이스 커넥션을 먼저 설정해야 합니다.

> [!WARNING]
> `redis` 큐 드라이버는 Redis의 `serializer` 및 `compression` 옵션을 지원하지 않습니다.

**Redis 클러스터(Cluster)**

Redis 큐 커넥션에서 Redis 클러스터를 사용하는 경우, 큐 이름에 반드시 [키 해시 태그(key hash tag)](https://redis.io/docs/reference/cluster-spec/#hash-tags)를 포함해야 합니다. 이렇게 해야 동일한 큐에 대한 모든 Redis 키가 같은 해시 슬롯에 저장될 수 있습니다:

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

Redis 큐를 사용할 때 `block_for` 설정 옵션으로, 새 잡이 나타나기 전까지 드라이버가 얼마 동안 대기할지 제어할 수 있습니다. 이 값을 적절히 조정하면, 항상 Redis 데이터베이스에 새 잡이 있는지 반복적으로 확인하는 것보다 효율적으로 리소스를 사용할 수 있습니다. 예를 들어, `block_for`를 `5`로 설정하면, 잡이 도착할 때까지 5초 동안 대기합니다:

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
> `block_for` 값을 `0`으로 설정하면, 잡이 들어올 때까지 워커가 무한 대기 상태에 빠집니다. 이렇게 되면 `SIGTERM`과 같은 시그널도 다음 잡이 처리될 때까지 무시되어 정상적으로 워커를 중지할 수 없게 됩니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 선행조건

아래 큐 드라이버를 사용하려면 각 드라이버별로 다음과 같은 의존성 패키지가 필요합니다. 이 패키지들은 Composer를 통해 설치할 수 있습니다.

<div class="content-list" markdown="1">

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~2.0` 또는 phpredis PHP 확장 모듈
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`

</div>

<a name="creating-jobs"></a>
## 잡 생성하기

<a name="generating-job-classes"></a>
### 잡 클래스 생성

기본적으로, 애플리케이션에서 큐에 넣을 모든 잡 클래스는 `app/Jobs` 디렉토리에 저장됩니다. 만약 `app/Jobs` 디렉토리가 없다면, `make:job` Artisan 명령어를 실행할 때 자동으로 생성됩니다:

```shell
php artisan make:job ProcessPodcast
```

생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하며, 라라벨이 이 잡을 비동기적으로 큐에 넣어 실행해야 함을 인식하게 됩니다.

> [!NOTE]
> 잡 스텁(stub)은 [스텁 공개(publishing)](/docs/12.x/artisan#stub-customization) 기능을 통해 커스터마이즈할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조

잡 클래스는 일반적으로 매우 단순합니다. 보통 큐에서 작업을 처리할 때 호출되는 `handle` 메서드만 포함합니다. 아래 예제에서는 팟캐스트 게시 서비스에서 업로드된 팟캐스트 파일을 공개 전 먼저 처리하는 잡을 만든다고 가정해보겠습니다:

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

이 예제에서 볼 수 있듯, [Eloquent 모델](/docs/12.x/eloquent)을 잡의 생성자에 직접 전달할 수 있습니다. 잡 클래스에서 `Queueable` 트레이트를 사용하면, Eloquent 모델과 그에 연결된 연관된 데이터(연관관계)도 잡이 처리되는 과정에서 자동으로 직렬화/역직렬화됩니다.

큐에 넣는 잡 생성자에서 Eloquent 모델을 받는 경우, 실제로는 모델의 식별자만 큐에 직렬화되어 저장됩니다. 잡이 실제로 처리될 때, 큐 시스템이 데이터베이스에서 전체 모델 인스턴스 및 연관된 데이터를 다시 조회합니다. 이런 방식 덕분에 큐에 전송되는 잡 페이로드가 훨씬 작아지며, 효율적으로 동작할 수 있습니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드의 의존성 주입

큐에서 잡이 실행되면 `handle` 메서드가 호출됩니다. 이때, `handle` 메서드의 인자로 필요한 의존성을 타입힌트로 명시할 수 있습니다. 라라벨의 [서비스 컨테이너](/docs/12.x/container)가 해당 의존성을 자동으로 주입해줍니다.

컨테이너가 `handle` 메서드에 의존성을 어떻게 주입할지 완전히 직접 제어하고 싶다면, 컨테이너의 `bindMethod` 메서드를 사용할 수 있습니다. 이 메서드는 잡과 컨테이너를 전달받는 콜백을 받아 사용자가 원하는 방식으로 `handle` 메서드를 직접 호출할 수 있습니다. 보통, 이 코드는 `App\Providers\AppServiceProvider` [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에서 호출합니다:

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 바이너리 데이터(원시 이미지 데이터 등)는 큐에 전달하기 전에 반드시 `base64_encode` 함수를 사용해 인코딩해야 합니다. 그렇지 않으면, 잡을 큐에 올릴 때 JSON으로 직렬화하는 과정에서 오류가 발생할 수 있습니다.

<a name="handling-relationships"></a>
#### 큐 직렬화와 연관관계 처리

잡을 큐에 넣을 때 Eloquent 모델의 모든 연관관계도 함께 직렬화되기 때문에, 직렬화된 잡 문자열이 매우 커질 수 있습니다. 또한, 잡이 역직렬화되어 모델의 연관관계를 데이터베이스에서 다시 조회할 때, 해당 연관관계 전체가 조회됩니다. 잡을 큐에 넣기 이전에 연관관계에 별도로 제약조건(조건 쿼리 등)을 걸었더라도, 잡이 재처리될 때는 적용되지 않습니다. 따라서, 특정 연관관계의 일부만 필요하다면, 잡 클래스 내부에서 다시 해당 연관관계에 제약조건을 걸어주는 것이 좋습니다.

또는, 모델을 프로퍼티로 설정할 때 `withoutRelations` 메서드를 호출해 연관관계가 직렬화되지 않도록 할 수 있습니다. 이 메서드는 연관관계가 로드되지 않은 새 모델 인스턴스를 반환합니다:

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

PHP의 생성자 프로퍼티 프로모션 기능을 사용할 때, 해당 Eloquent 모델의 연관관계를 직렬화하지 않으려면 `WithoutRelations` 어트리뷰트를 사용할 수 있습니다:

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

잡에서 Eloquent 모델의 컬렉션이나 배열을 받는 경우, 큐에서 역직렬화 및 실행될 때 컬렉션 내의 각 모델에 대해 연관관계가 복원되지 않습니다. 이는 한 번에 많은 모델을 처리하는 잡의 리소스 사용량을 최소화하기 위함입니다.

<a name="unique-jobs"></a>
### 고유 잡(Unique Jobs)

> [!WARNING]
> 고유 잡 기능을 사용하려면 [락(lock)](/docs/12.x/cache#atomic-locks) 기능을 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 atomic lock을 지원합니다. 또한, 고유 잡 제약 조건은 배치(batch) 내의 잡에는 적용되지 않습니다.

때로는 특정 잡의 인스턴스가 한 번에 큐 상에 반드시 하나만 존재하도록 보장하고 싶을 수 있습니다. 이를 위해, 잡 클래스에 `ShouldBeUnique` 인터페이스를 구현하면 됩니다. 이 인터페이스는 별도의 추가 메서드 구현이 필요하지 않습니다:

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

위 예시에서 `UpdateSearchIndex` 잡은 고유 잡입니다. 즉, 이미 동일한 잡 인스턴스가 큐에 존재하여 처리 중이라면, 추가 잡은 디스패치되지 않습니다.

특정한 "고유 키(key)"를 기준으로 잡을 고유하게 만들거나, 잡의 고유 락이 얼마 동안 유지될지 타임아웃을 지정하고 싶을 때는, 잡 클래스에 `uniqueId` 및 `uniqueFor` 프로퍼티나 메서드를 정의하면 됩니다:

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
     * 잡의 고유 락이 해제될 때까지의 초(second) 단위 시간.
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

위 예제에서는 상품 ID로 잡이 고유하게 구분됩니다. 즉, 같은 상품 ID로 또 다른 잡을 디스패치해도, 기존 잡이 완료되기 전까지는 새로운 잡이 큐에 올라가지 않습니다. 또한, 기존 잡이 한 시간(3600초) 안에 처리되지 않으면 고유 락이 해제되어 같은 키의 새 잡이 다시 큐에 올라갈 수 있습니다.

> [!WARNING]
> 여러 웹 서버나 컨테이너에서 잡을 디스패치하는 경우, 반드시 모든 서버가 같은 중앙 캐시 서버를 사용하도록 설정해야 라라벨이 잡의 고유성을 정상적으로 판단할 수 있습니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 잡 실행 전까지 고유성 유지하기

기본적으로, 고유 잡은 처리 완료되거나 모든 재시도 시도를 모두 실패해야 "언락(unlock, 고유 락 해제)"됩니다. 그런데 잡이 처리되기 '직전'에 락을 해제하길 원할 수도 있습니다. 이런 경우에는 `ShouldBeUnique` 대신 `ShouldBeUniqueUntilProcessing` 인터페이스를 구현하세요:

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
#### 고유 잡 락(Unique Job Locks)

내부적으로, `ShouldBeUnique` 잡이 디스패치될 때 라라벨은 해당 잡의 `uniqueId` 키로 [락(lock)](/docs/12.x/cache#atomic-locks)을 획득하려 시도합니다. 락을 획득하지 못하면 잡은 디스패치되지 않습니다. 이 락은 잡이 처리 완료되거나 모든 재시도가 실패하면 해제됩니다. 기본적으로 라라벨은 기본 캐시 드라이버로 락을 관리하지만, 따로 락을 획득할 드라이버를 지정하고 싶다면 `uniqueVia` 메서드를 정의해 사용할 캐시 드라이버를 반환하면 됩니다:

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
> 단순히 잡의 동시 실행 제한이 필요하다면, [WithoutOverlapping](/docs/12.x/queues#preventing-job-overlaps) 잡 미들웨어를 사용하세요.

<a name="encrypted-jobs"></a>
### 암호화된 잡

라라벨은 [암호화](/docs/12.x/encryption)를 통해 잡 데이터의 보안성과 무결성을 보장할 수 있습니다. 사용 방법은 간단하며, 잡 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하기만 하면 됩니다. 이 인터페이스가 추가된 잡 클래스는 큐에 등록되기 전에 자동으로 암호화 처리됩니다:

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

잡 미들웨어(job middleware)를 활용하면, 큐 잡 실행 과정에 커스텀 로직을 쉽고 간편하게 추가할 수 있어 잡 클래스 내부에서 반복적으로 작성해야 하는 코드(보일러플레이트)를 줄여줍니다. 예를 들어, 아래는 라라벨의 Redis 속도 제한(rate limiting) 기능을 활용해 5초마다 한 번만 잡이 실행되도록 제한하는 `handle` 메서드 예시입니다:

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

이 코드는 정상적으로 동작하지만, `handle` 메서드 내부에 Redis 속도 제한 기능이 혼합되어 복잡해지고, 동일한 기능이 필요한 다른 잡에도 똑같은 코드를 반복해 작성해야 한다는 단점이 있습니다.

이런 경우, `handle` 메서드에서 직접 속도 제한 처리를 하지 않고, 속도 제한 처리를 전담하는 잡 미들웨어를 따로 만들어서 활용할 수 있습니다. 라라벨에는 잡 미들웨어의 기본 위치가 정해져 있지 않으므로, 원하는 곳에 자유롭게 위치시킬 수 있습니다. 아래에서는 `app/Jobs/Middleware` 디렉토리에 미들웨어를 생성하는 예를 보여줍니다:

```php
<?php

namespace App\Jobs\Middleware;

use Closure;
use Illuminate\Support\Facades\Redis;

class RateLimited
{
    /**
     * 큐 잡 처리 메서드
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

위 예제처럼, [라우트 미들웨어](/docs/12.x/middleware)와 마찬가지로 잡 미들웨어 역시 처리 대상인 잡과, 처리를 계속 이어갈 콜백을 전달받습니다.

잡 미들웨어를 만들고 나면, 잡 클래스에서 `middleware` 메서드를 만들어 미들웨어를 반환하면 해당 잡에 적용됩니다. 이 메서드는 기본적으로 `make:job` Artisan 명령어로 scaffold된 잡에는 포함되어 있지 않으므로, 직접 추가해야 합니다:

```php
use App\Jobs\Middleware\RateLimited;

/**
 * 잡이 거쳐야 할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited];
}
```

> [!NOTE]
> 잡 미들웨어는 큐로 실행되는 이벤트 리스너, 메일러블, 알림 등에도 적용할 수 있습니다.

<a name="rate-limiting"></a>
### 속도 제한

직접 잡 미들웨어를 만들어 속도 제한을 처리하는 방법을 위에서 다뤘지만, 라라벨은 잡에 적용할 수 있는 속도 제한 미들웨어도 기본 제공합니다. [라우트 속도 제한자](/docs/12.x/routing#defining-rate-limiters)와 마찬가지로, 잡 속도 제한자는 `RateLimiter` 파사드의 `for` 메서드를 사용해 정의할 수 있습니다.

예를 들어, 일반 사용자는 데이터를 한 시간에 한 번만 백업할 수 있고, 프리미엄 고객은 제한을 두지 않으려면, `AppServiceProvider`의 `boot` 메서드에서 `RateLimiter`를 다음과 같이 정의하면 됩니다:

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

위 예제에서는 한 시간 단위로 제한하지만, 필요에 따라 `perMinute` 메서드를 사용해 분 단위로도 제한할 수 있습니다. 그리고 `by` 메서드에는 어떤 값도 지정할 수 있지만, 보통 고객별로 제한을 분리하기 위해 사용합니다:

```php
return Limit::perMinute(50)->by($job->user->id);
```

이제 속도 제한을 정의했다면, `Illuminate\Queue\Middleware\RateLimited` 미들웨어를 잡에 붙여서 사용할 수 있습니다. 해당 잡이 속도 제한을 초과할 경우, 이 미들웨어가 잡을 큐에 다시 반환(release)시키며, 적절한 지연 시간도 함께 적용됩니다.

```php
use Illuminate\Queue\Middleware\RateLimited;

/**
 * 잡이 거쳐야 할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited('backups')];
}
```

속도 제한에 걸려 큐에 재등록(release)되는 경우에도 잡의 `attempts`(시도 횟수)는 늘어납니다. 이에 따라 `tries`나 `maxExceptions` 프로퍼티 값을 조정하거나, 또는 [retryUntil 메서드](#time-based-attempts)로 잡 재시도의 종료 시점을 다르게 지정할 수 있습니다.

`releaseAfter` 메서드를 사용해, 재실행까지 대기할 시간을 직접 초 단위로 지정할 수도 있습니다:

```php
/**
 * 잡이 거쳐야 할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new RateLimited('backups'))->releaseAfter(60)];
}
```

속도 제한에 걸렸을 때 잡이 재시도되지 않기를 원한다면, `dontRelease` 메서드를 사용하세요:

```php
/**
 * 잡이 거쳐야 할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new RateLimited('backups'))->dontRelease()];
}
```

> [!NOTE]
> Redis를 사용한다면, Redis에 특화되어 더 효율적으로 동작하는 `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어도 사용할 수 있습니다.

<a name="preventing-job-overlaps"></a>
### 잡 중첩 방지

라라벨에는 `Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어가 내장되어 있습니다. 이 미들웨어를 사용하면 임의의 키 값을 기준으로 같은 종류의 잡이 한 번에 하나만 동시에 실행되도록 중첩(Overlap)을 방지할 수 있습니다. 예를 들어, 사용자 신용점수를 업데이트하는 잡이 있을 때, 같은 사용자 ID에 대한 점수 업데이트 잡이 동시에 여러 개 실행되는 것을 막고 싶다면, 해당 사용자 ID를 기준으로 `WithoutOverlapping` 미들웨어를 잡의 `middleware` 메서드에서 반환하면 됩니다:

```php
use Illuminate\Queue\Middleware\WithoutOverlapping;

/**
 * 잡이 거쳐야 할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new WithoutOverlapping($this->user->id)];
}
```

동일 타입의 중첩 잡은 큐로 다시 release(재등록)되며, 재시도까지 대기할 시간을 직접 초 단위로 지정할 수도 있습니다:

```php
/**
 * 잡이 거쳐야 할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->releaseAfter(60)];
}
```

겹치는 잡이 재시도되지 않고 즉시 삭제되길 원한다면, `dontRelease` 메서드를 사용하세요:

```php
/**
 * 잡이 거쳐야 할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->dontRelease()];
}
```

`WithoutOverlapping` 미들웨어는 라라벨의 atomic lock 기능을 사용합니다. 때로는 잡이 예기치 않게 실패하거나 타임아웃되어 락이 정상적으로 해제되지 않을 수 있습니다. 이런 경우를 대비해, `expireAfter` 메서드로 락의 만료 시간을 직접 설정할 수 있습니다. 예를 들어, 아래 예제는 잡이 실행된 후 3분(180초) 후에 락이 해제됩니다:

```php
/**
 * 잡이 거쳐야 할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->expireAfter(180)];
}
```

> [!WARNING]
> `WithoutOverlapping` 미들웨어는 [락(lock)](/docs/12.x/cache#atomic-locks) 기능을 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 atomic lock을 지원합니다.

<a name="sharing-lock-keys"></a>

#### 작업 클래스 간의 Lock Key 공유

기본적으로 `WithoutOverlapping` 미들웨어는 같은 클래스 내에서만 중복 실행을 방지합니다. 즉, 서로 다른 두 작업 클래스가 동일한 lock key를 사용하더라도, 기본값으로는 중복 실행이 차단되지 않습니다. 하지만, `shared` 메서드를 이용해서 라라벨이 작업 클래스 간에도 동일한 key가 적용되도록 설정할 수 있습니다.

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
### 예외 제한(Throttling Exceptions)

라라벨에는 예외 발생을 제한할 수 있는 `Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어가 포함되어 있습니다. 작업이 지정한 횟수만큼 예외를 던진 후에는, 일정한 대기 시간이 지나기 전까지 추가 실행 시도가 모두 지연됩니다. 이 미들웨어는 안정적이지 않은 외부 서비스와 상호작용하는 작업에 특히 유용합니다.

예를 들어, 외부 API와 상호작용하는 큐 작업이 계속해서 예외를 발생시킨다고 가정해 봅시다. 예외 수 제한을 적용하려면, 작업의 `middleware` 메서드에서 `ThrottlesExceptions` 미들웨어를 반환하면 됩니다. 일반적으로 이 미들웨어는 [시간 기반 시도](#time-based-attempts)를 구현한 작업과 함께 사용해야 합니다.

```php
use DateTime;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 작업이 통과해야 할 미들웨어를 반환합니다.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new ThrottlesExceptions(10, 5 * 60)];
}

/**
 * 작업이 시간 초과로 중단되어야 하는 시점을 반환합니다.
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(30);
}
```

미들웨어의 첫 번째 생성자 인자는 예외를 몇 번까지 허용할지의 숫자이고, 두 번째 인자는 제한 도달 시 몇 초 뒤에 재실행할지(초 단위) 설정하는 값입니다. 위 예시에서 작업이 10번 연속 예외를 발생하면 5분 후에 다시 실행을 시도하며, 이 모든 과정은 30분 이내에서만 시도됩니다.

작업이 예외를 던졌으나 아직 임계치에 도달하지 않았다면, 기본적으로 곧바로 재시도됩니다. 하지만, 미들웨어에 `backoff` 메서드를 연결하면 이런 작업이 일정 시간(분 단위) 지연된 후 재시도되도록 지정할 수 있습니다.

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 작업이 통과해야 할 미들웨어를 반환합니다.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 5 * 60))->backoff(5)];
}
```

이 미들웨어는 내부적으로 라라벨의 캐시 시스템을 활용하여 속도 제한을 구현하며, 작업 클래스명이 캐시 "키"로 사용됩니다. 여러 작업이 동일한 외부 서비스와 연관되어 공통의 제한 "버킷"을 공유하길 원한다면, 미들웨어를 연결할 때 `by` 메서드를 호출하여 키를 직접 지정할 수 있습니다.

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 작업이 통과해야 할 미들웨어를 반환합니다.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->by('key')];
}
```

기본적으로 이 미들웨어는 모든 예외를 제한 대상으로 삼습니다. 이 동작을 변경하려면, 미들웨어를 연결할 때 `when` 메서드를 호출해 특정 조건이 맞을 때만 예외 제한이 동작하도록 할 수 있습니다. 즉, `when` 메서드에 전달한 클로저가 `true`를 반환할 때만 예외가 제한됩니다.

```php
use Illuminate\Http\Client\HttpClientException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 작업이 통과해야 할 미들웨어를 반환합니다.
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

`when` 메서드는 작업을 다시 큐에 넣거나 예외를 발생시키는 반면, `deleteWhen` 메서드는 특정 예외가 발생했을 때 그 즉시 해당 작업을 큐에서 제거할 수 있게 해줍니다.

```php
use App\Exceptions\CustomerDeletedException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 작업이 통과해야 할 미들웨어를 반환합니다.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(2, 10 * 60))->deleteWhen(CustomerDeletedException::class)];
}
```

예외 제한 상황도 애플리케이션의 예외 핸들러로 보고되길 원한다면, 미들웨어를 연결할 때 `report` 메서드를 사용할 수 있습니다. 선택적으로 `report` 메서드에 클로저를 전달하면, 클로저가 `true`를 반환하는 경우에만 보고됩니다.

```php
use Illuminate\Http\Client\HttpClientException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 작업이 통과해야 할 미들웨어를 반환합니다.
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
> Redis를 사용하는 경우, Redis에 최적화되어 있고 일반 예외 제한 미들웨어보다 더 효율적인 `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어를 사용할 수 있습니다.

<a name="skipping-jobs"></a>
### 작업 건너뛰기(Skipping Jobs)

`Skip` 미들웨어를 사용하면 작업 내부 로직을 변경하지 않고도, 특정 조건에 따라 작업이 자동으로 건너뛰어지거나(즉시 삭제됨) 하도록 할 수 있습니다. `Skip::when` 메서드는 주어진 조건이 `true`가 되면 작업을 삭제하고, `Skip::unless`는 조건이 `false`일 때 작업을 삭제합니다.

```php
use Illuminate\Queue\Middleware\Skip;

/**
 * 작업이 통과해야 할 미들웨어를 반환합니다.
 */
public function middleware(): array
{
    return [
        Skip::when($someCondition),
    ];
}
```

조건 평가가 더 복잡한 경우, `when`과 `unless` 메서드에 `Closure`(익명 함수)를 전달할 수도 있습니다.

```php
use Illuminate\Queue\Middleware\Skip;

/**
 * 작업이 통과해야 할 미들웨어를 반환합니다.
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
## 작업 디스패치(Dispatching Jobs)

작업 클래스를 작성한 후, 해당 작업 클래스의 `dispatch` 메서드를 사용해서 작업을 디스패치할 수 있습니다. `dispatch` 메서드에 전달한 인수들은 작업의 생성자에 그대로 전달됩니다.

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

작업을 조건부로 디스패치하고 싶다면 `dispatchIf` 및 `dispatchUnless` 메서드를 사용할 수 있습니다.

```php
ProcessPodcast::dispatchIf($accountActive, $podcast);

ProcessPodcast::dispatchUnless($accountSuspended, $podcast);
```

새로운 라라벨 애플리케이션에서는 기본 큐 드라이버로 `sync` 드라이버가 사용됩니다. 이 드라이버는 작업을 요청 처리 중(동기적으로) 바로 실행하며, 로컬 개발 환경에서 편리하게 활용할 수 있습니다. 실제로 작업을 백그라운드에서 큐잉하려면, 애플리케이션의 `config/queue.php` 설정 파일에서 다른 큐 드라이버를 지정해야 합니다.

<a name="delayed-dispatching"></a>
### 지연 디스패치(Delayed Dispatching)

작업이 바로 큐 워커에 의해 처리되지 않고, 일정 시간 이후에 처리하도록 하려면 작업 디스패치 시 `delay` 메서드를 사용할 수 있습니다. 예를 들어, 작업이 디스패치된 후 10분 뒤에 처리되길 원한다면 아래와 같이 할 수 있습니다.

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

특정 작업이 이미 디폴트로 지연 처리가 적용되어 있다면, 이 지연을 무시하고 곧바로 처리하도록 디스패치하려면 `withoutDelay` 메서드를 사용할 수 있습니다.

```php
ProcessPodcast::dispatch($podcast)->withoutDelay();
```

> [!WARNING]
> Amazon SQS 큐 서비스는 최대 15분의 지연만 지원합니다.

<a name="dispatching-after-the-response-is-sent-to-browser"></a>
#### 브라우저로 응답이 전송된 후 디스패치하기

또 다른 방법으로, `dispatchAfterResponse` 메서드는 웹 서버가 FastCGI를 사용할 때, HTTP 응답이 사용자 브라우저에 전송된 다음에 작업이 디스패치되도록 지연합니다. 즉, 사용자가 이미 애플리케이션을 이용하기 시작하더라도, 큐 작업이 백그라운드에서 처리되고 있는 상태가 됩니다. 일반적으로 이메일 전송 등 1초 내외로 처리되는 작업에 사용하는 것이 적합합니다. 이 방식으로 디스패치된 작업은 실행에 별도의 큐 워커가 필요 없으며, 현재 HTTP 요청(프로세스)에서 처리됩니다.

```php
use App\Jobs\SendNotification;

SendNotification::dispatchAfterResponse();
```

또한 `dispatch` 헬퍼에 클로저(익명 함수)를 전달하고, `afterResponse` 메서드를 연결하면 HTTP 응답이 브라우저로 전송된 후 해당 클로저가 실행됩니다.

```php
use App\Mail\WelcomeMessage;
use Illuminate\Support\Facades\Mail;

dispatch(function () {
    Mail::to('taylor@example.com')->send(new WelcomeMessage);
})->afterResponse();
```

<a name="synchronous-dispatching"></a>
### 동기 디스패치(Synchronous Dispatching)

작업을 즉시(동기적으로) 실행하고 싶다면 `dispatchSync` 메서드를 사용할 수 있습니다. 이 방식을 사용하면 작업이 큐잉되지 않고 현재 프로세스 내에서 바로 실행됩니다.

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

        // 팟캐스트 생성...

        ProcessPodcast::dispatchSync($podcast);

        return redirect('/podcasts');
    }
}
```

<a name="jobs-and-database-transactions"></a>
### 작업과 데이터베이스 트랜잭션(Jobs & Database Transactions)

데이터베이스 트랜잭션 내에서 작업을 디스패치하는 것은 기본적으로 문제가 없지만, 작업이 실제로 성공적으로 실행될 수 있는지 특별히 신경 써야 합니다. 트랜잭션 내에서 작업을 디스패치하는 경우, 해당 작업이 트랜잭션이 커밋되기 전에 워커에 의해 처리될 수도 있습니다. 이 상황에서는 트랜잭션 도중에 변경된 모델이나 레코드가 아직 데이터베이스에 확정적으로 기록되지 않았기 때문에, 워커가 실제 데이터 변경 사항을 확인할 수 없는 문제가 발생할 수 있습니다. 또한 트랜잭션 내에서 새로 생성한 모델, 레코드도 데이터베이스에 아예 존재하지 않을 수 있습니다.

다행히 라라벨은 이 문제를 해결할 수 있도록 몇 가지 방법을 제공합니다. 먼저, 큐 연결 설정 배열에서 `after_commit` 옵션을 설정하면 됩니다.

```php
'redis' => [
    'driver' => 'redis',
    // ...
    'after_commit' => true,
],
```

`after_commit` 옵션이 `true`로 설정되어 있다면, 데이터베이스 트랜잭션 내에서도 작업을 디스패치할 수 있습니다. 단, 라라벨은 상위 트랜잭션이 모두 커밋될 때까지 실제로 작업을 디스패치하지 않고 대기합니다. 물론, 현재 열린 트랜잭션이 없다면 작업은 곧바로 디스패치됩니다.

만약 트랜잭션 도중 예외가 발생해 트랜잭션이 롤백된다면, 해당 트랜잭션 중에 디스패치된 작업도 같이 무시(삭제)됩니다.

> [!NOTE]
> 큐 연결의 `after_commit` 설정값을 `true`로 하면, 큐에 보내지는 이벤트 리스너, 메일, 알림, 브로드캐스트 이벤트 역시 모든 트랜잭션 커밋 이후에만 디스패치됩니다.

<a name="specifying-commit-dispatch-behavior-inline"></a>
#### 인라인으로 커밋 후 디스패치 지정하기

큐 연결 설정에서 `after_commit`을 `true`로 설정하지 않은 경우라도, 특정 작업에 대해선 직접 디스패치 시 `afterCommit` 메서드를 체이닝하면 트랜잭션 커밋 이후에만 디스패치되도록 할 수 있습니다.

```php
use App\Jobs\ProcessPodcast;

ProcessPodcast::dispatch($podcast)->afterCommit();
```

반대로, `after_commit` 설정이 이미 `true`일 때, 해당 작업에 대해선 트랜잭션 커밋을 기다리지 않고 바로 디스패치하고 싶다면 `beforeCommit` 메서드를 사용합니다.

```php
ProcessPodcast::dispatch($podcast)->beforeCommit();
```

<a name="job-chaining"></a>
### 작업 체이닝(Job Chaining)

작업 체이닝을 사용하면, 하나의 주요 작업이 성공적으로 실행된 이후에 순차적으로 이어서 실행할 작업 리스트를 지정할 수 있습니다. 체인 내 작업 중 하나라도 실패하면 나머지 작업들은 실행되지 않습니다. 체인 작업을 실행하려면, `Bus` 파사드에서 제공하는 `chain` 메서드를 사용합니다. 라라벨의 커맨드 버스는 작업 큐 처리의 하위 레벨 컴포넌트입니다.

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

작업 클래스 인스턴스뿐만 아니라, 클로저(익명 함수)도 체인에 추가할 수 있습니다.

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
> 작업 내에서 `$this->delete()` 메서드로 작업을 삭제해도, 체이닝된 다음 작업은 계속 실행됩니다. 체인 내의 작업 중 하나가 실패할 때만 나머지 작업들이 실행되지 않습니다.

<a name="chain-connection-queue"></a>
#### 체인 연결 및 큐 지정하기

체이닝된 작업들에서 사용할 큐 연결 및 큐 이름을 지정하려면 `onConnection`과 `onQueue` 메서드를 사용할 수 있습니다. 이렇게 하면 각 작업이 별도로 연결/큐를 지정하지 않는 한 해당 값이 사용됩니다.

```php
Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->onConnection('redis')->onQueue('podcasts')->dispatch();
```

<a name="adding-jobs-to-the-chain"></a>
#### 체인에 작업 추가하기

경우에 따라 체인 내의 다른 작업에서, 현재 체인 앞이나 뒤에 작업을 추가해야 할 때가 있습니다. 이 경우, `prependToChain`과 `appendToChain` 메서드를 사용할 수 있습니다.

```php
/**
 * 작업을 실행합니다.
 */
public function handle(): void
{
    // ...

    // 현재 체인 앞에 추가. 즉, 이 작업 바로 다음에 실행됩니다.
    $this->prependToChain(new TranscribePodcast);

    // 현재 체인 뒤에 추가. 체인의 마지막에 실행됩니다.
    $this->appendToChain(new TranscribePodcast);
}
```

<a name="chain-failures"></a>
#### 체인 작업 실패 처리

체이닝된 작업 중 하나가 실패했을 때 실행할 콜백은 `catch` 메서드에서 지정할 수 있습니다. 이 콜백은 실패 원인이 된 `Throwable` 인스턴스를 인수로 받습니다.

```php
use Illuminate\Support\Facades\Bus;
use Throwable;

Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->catch(function (Throwable $e) {
    // 체인 내에 있는 작업이 실패했습니다...
})->dispatch();
```

> [!WARNING]
> 체인 콜백은 직렬화되어 나중에 라라벨 큐 워커에 의해 실행됩니다. 따라서 콜백 내부에서는 `$this` 변수를 사용하지 않아야 합니다.

<a name="customizing-the-queue-and-connection"></a>
### 큐와 연결 커스터마이징

<a name="dispatching-to-a-particular-queue"></a>
#### 특정 큐로 디스패치하기

작업을 다양한 큐로 분류(push)함으로써, 큐별로 작업을 "카테고리화"하고 각 큐에 할당할 워커 수를 통해 우선순위를 조정할 수 있습니다. 이 방식은 큐 설정 파일에서 정의한 서로 다른 큐 "연결(connection)"이 아닌, 단일 연결 내의 특정 큐로 작업을 보내는 것임을 유의하세요. 작업을 디스패치할 때 `onQueue` 메서드를 사용해서 큐를 지정할 수 있습니다.

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

        // 팟캐스트 생성...

        ProcessPodcast::dispatch($podcast)->onQueue('processing');

        return redirect('/podcasts');
    }
}
```

또는, 작업 클래스의 생성자에서 `onQueue` 메서드를 호출해 작업이 사용할 큐를 지정할 수 있습니다.

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    /**
     * 새 작업 인스턴스를 생성합니다.
     */
    public function __construct()
    {
        $this->onQueue('processing');
    }
}
```

<a name="dispatching-to-a-particular-connection"></a>
#### 특정 연결로 디스패치하기

여러 큐 연결(connection)을 사용하는 애플리케이션의 경우, `onConnection` 메서드를 사용해서 작업을 원하는 연결로 보낼 수 있습니다.

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

        // 팟캐스트 생성...

        ProcessPodcast::dispatch($podcast)->onConnection('sqs');

        return redirect('/podcasts');
    }
}
```

물론, `onConnection`과 `onQueue` 메서드를 함께 체이닝하여 연결과 큐를 동시에 지정할 수도 있습니다.

```php
ProcessPodcast::dispatch($podcast)
    ->onConnection('sqs')
    ->onQueue('processing');
```

또는, 작업 클래스 생성자에서 `onConnection` 메서드를 호출해 작업의 연결을 설정할 수 있습니다.

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    /**
     * 새 작업 인스턴스를 생성합니다.
     */
    public function __construct()
    {
        $this->onConnection('sqs');
    }
}
```

<a name="max-job-attempts-and-timeout"></a>

### 최대 작업 시도 횟수/타임아웃 값 지정

<a name="max-attempts"></a>
#### 최대 시도 횟수

큐에 등록된 작업 중 하나에서 오류가 발생한다면, 무한정 계속해서 재시도하도록 두고 싶지는 않을 것입니다. 그래서 라라벨은 작업이 시도될 수 있는 횟수나 기간을 지정할 수 있는 다양한 방법을 제공합니다.

하나의 방법은 아티즌 명령어의 `--tries` 옵션을 사용하여 작업이 시도될 최대 횟수를 지정하는 것입니다. 이 옵션을 사용하면, 작업별로 따로 지정하지 않은 한 모든 작업자(worker)가 처리하는 작업에 해당 횟수가 적용됩니다.

```shell
php artisan queue:work --tries=3
```

작업이 최대 시도 횟수를 초과하면 "실패(failed)"한 작업으로 간주됩니다. 실패한 작업 처리에 대한 자세한 내용은 [실패한 작업 문서](#dealing-with-failed-jobs)를 참고하세요. 또, `queue:work` 명령어에 `--tries=0`을 지정하면 작업은 무한정 재시도됩니다.

좀 더 세밀하게 작업별 최대 시도 횟수를 지정하고 싶다면, 작업 클래스 내에서 최대 시도 횟수를 지정할 수 있습니다. 작업 클래스에 최대 시도 횟수를 명시하면, 커맨드 라인에 지정한 `--tries` 값보다 우선 적용됩니다.

```php
<?php

namespace App\Jobs;

class ProcessPodcast implements ShouldQueue
{
    /**
     * 작업이 시도될 수 있는 최대 횟수
     *
     * @var int
     */
    public $tries = 5;
}
```

특정 작업의 최대 시도 횟수를 동적으로 제어해야 하는 경우, 작업 클래스에 `tries` 메서드를 정의할 수 있습니다.

```php
/**
 * 작업이 시도될 수 있는 최대 횟수를 반환합니다.
 */
public function tries(): int
{
    return 5;
}
```

<a name="time-based-attempts"></a>
#### 시간 기반 시도 관리

작업이 실패하기 전 시도 횟수 대신, 일정 시간이 지난 뒤에는 더 이상 시도하지 않도록 구성할 수도 있습니다. 이 방법을 사용하면, 주어진 시간 내에는 횟수 제한 없이 재시도가 가능합니다. 작업이 더 이상 재시도되지 않아야 하는 시점을 지정하려면 작업 클래스에 `retryUntil` 메서드를 추가하면 됩니다. 이 메서드는 `DateTime` 인스턴스를 반환해야 합니다.

```php
use DateTime;

/**
 * 작업의 타임아웃 시점을 반환합니다.
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(10);
}
```

`retryUntil`과 `tries`가 모두 정의되어 있으면, 라라벨은 `retryUntil` 메서드를 우선 적용합니다.

> [!NOTE]
> [큐로 처리되는 이벤트 리스너](/docs/12.x/events#queued-event-listeners)에서도 `tries` 속성이나 `retryUntil` 메서드를 정의할 수 있습니다.

<a name="max-exceptions"></a>
#### 최대 예외 횟수

작업이 많게는 여러 번 시도되어야 하지만, 특정 횟수만큼 처리되지 않은 예외(unhandled exception)가 발생할 경우에는 작업을 실패로 처리하고 싶을 때가 있습니다. 이런 경우, 작업 클래스에 `maxExceptions` 속성을 정의할 수 있습니다.

```php
<?php

namespace App\Jobs;

use Illuminate\Support\Facades\Redis;

class ProcessPodcast implements ShouldQueue
{
    /**
     * 작업이 시도될 수 있는 최대 횟수
     *
     * @var int
     */
    public $tries = 25;

    /**
     * 실패 처리되기 전 허용할 최대 미처리 예외 횟수
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
            // 락을 획득했을 때, 팟캐스트 처리...
        }, function () {
            // 락을 획득하지 못했을 때...
            return $this->release(10);
        });
    }
}
```

위 예시에서, 애플리케이션이 Redis 락을 획득하지 못하면 10초 후에 작업을 다시 재시도할 것이며 최대 25번까지 시도하게 됩니다. 그러나 만약 3번의 미처리 예외가 연속해서 발생하면 해당 작업은 실패로 처리됩니다.

<a name="timeout"></a>
#### 타임아웃

일반적으로 여러분은 큐에 등록된 작업들이 대략 얼마 정도 소요될지를 알고 있을 때가 많습니다. 라라벨에서는 이러한 이유로 "타임아웃" 값을 지정할 수 있습니다. 기본 타임아웃은 60초이며, 지정한 시간(초)보다 작업 실행이 더 오래 걸리면 작업자는 오류와 함께 종료됩니다. 일반적으로 작업자는 [서버에 구성된 프로세스 매니저](#supervisor-configuration)가 자동으로 재시작해줍니다.

작업이 실행될 수 있는 최대 초 단위 시간은 아티즌 명령어의 `--timeout` 옵션으로 지정할 수 있습니다.

```shell
php artisan queue:work --timeout=30
```

작업이 타임아웃에 의한 오류로 계속해서 최대 시도 횟수를 초과하면 해당 작업은 실패로 처리됩니다.

작업 클래스 내에서도 개별적으로 작업의 허용 실행 시간을 지정할 수 있습니다. 이 경우, 클래스 내부의 타임아웃 설정이 커맨드라인에서 지정한 값보다 우선 적용됩니다.

```php
<?php

namespace App\Jobs;

class ProcessPodcast implements ShouldQueue
{
    /**
     * 작업이 타임아웃 되기 전 실행 가능한 최대 시간(초)
     *
     * @var int
     */
    public $timeout = 120;
}
```

가끔 소켓이나 외부 HTTP 연결과 같이 IO 블로킹 처리가 필요한 프로세스들은 지정한 타임아웃 값을 지키지 않을 수 있습니다. 이런 기능을 사용할 경우, 해당 기능의 API를 통해 타임아웃 값을 별도로 설정하는 것이 좋습니다. 예를 들어, Guzzle을 사용할 때는 연결 타임아웃과 요청 타임아웃 값을 반드시 지정해야 합니다.

> [!WARNING]
> 작업 타임아웃을 지정하려면 `pcntl` PHP 확장이 필수로 설치되어 있어야 합니다. 또한, 작업의 "timeout" 값은 항상 ["retry after"](#job-expiration) 값보다 작아야 합니다. 그렇지 않을 경우 작업이 실제로 끝나거나 타임아웃 처리가 되지 않았는데도 재시도가 발생할 수 있습니다.

<a name="failing-on-timeout"></a>
#### 타임아웃 시 실패 처리

작업이 [실패한 작업](#dealing-with-failed-jobs)으로 타임아웃되었는지 표시하고 싶다면, 작업 클래스에 `$failOnTimeout` 속성을 정의할 수 있습니다.

```php
/**
 * 작업이 타임아웃 시 실패로 처리되어야 하는지 여부를 지정합니다.
 *
 * @var bool
 */
public $failOnTimeout = true;
```

<a name="error-handling"></a>
### 오류 처리

작업이 처리 중 예외를 발생시키면 작업은 자동으로 큐에 다시 반환되어 재시도가 가능합니다. 작업은 애플리케이션에서 지정한 최대 시도 횟수에 도달할 때까지 계속해서 출시(재시도)됩니다. 최대 시도 횟수는 `queue:work` 아티즌 명령어에서 사용하는 `--tries` 옵션으로 지정하거나, 작업 클래스 내에서 직접 지정할 수 있습니다. 큐 작업자 실행에 관한 자세한 정보는 [아래에서 확인할 수 있습니다](#running-the-queue-worker).

<a name="manually-releasing-a-job"></a>
#### 작업 직접 출시(재시도)하기

작업을 큐에서 직접 다시 출시하여 일정 시간 후에 재시도하도록 수동으로 제어해야 할 때가 있습니다. 이런 경우, `release` 메서드를 호출하여 작업을 다시 큐로 보낼 수 있습니다.

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

기본적으로 `release` 메서드는 작업을 즉시 다시 처리하도록 큐에 반환합니다. 그러나 정수 또는 날짜 인스턴스를 인자로 넘겨주면 해당 시간 동안 작업이 재처리되지 않도록 지연시킬 수 있습니다.

```php
$this->release(10);

$this->release(now()->addSeconds(10));
```

<a name="manually-failing-a-job"></a>
#### 작업을 수동으로 실패 처리

특별한 경우, 작업을 직접 "실패"로 표시해야 할 때가 있습니다. 이때는 `fail` 메서드를 호출하면 됩니다.

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

예외를 직접 캐치해서 해당 예외로 작업을 실패 처리하고 싶다면, `fail` 메서드에 예외 인스턴스를 전달하세요. 또는 간단하게, 오류 메시지 문자열을 전달하면 라라벨이 이를 예외로 변환합니다.

```php
$this->fail($exception);

$this->fail('Something went wrong.');
```

> [!NOTE]
> 실패한 작업에 대한 추가 정보는 [실패한 작업 처리 문서](#dealing-with-failed-jobs)를 참고하세요.

<a name="job-batching"></a>
## 작업 배치 처리

라라벨의 작업 배치(batch) 기능은 여러 개의 작업을 한 번에 실행하고, 이 작업 집합이 모두 완료되면 후속 동작을 처리하는 방법을 쉽게 제공합니다. 시작하기 전에, 각 작업 배치의 완료율 등 메타정보를 저장할 테이블을 만들기 위해 데이터베이스 마이그레이션을 먼저 생성해야 합니다. 이 마이그레이션은 아래의 `make:queue-batches-table` 아티즌 명령어로 생성할 수 있습니다.

```shell
php artisan make:queue-batches-table

php artisan migrate
```

<a name="defining-batchable-jobs"></a>
### 배치 처리 가능한 작업 정의

배치 가능한 작업을 정의하려면, [일반적인 큐 작업](#creating-jobs)처럼 작업을 생성하되, 작업 클래스에 `Illuminate\Bus\Batchable` 트레이트(trait)를 추가해야 합니다. 이 트레이트는 작업이 현재 어떤 배치 내에서 실행되고 있는지 확인할 수 있는 `batch` 메서드를 제공합니다.

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

        // CSV 파일의 일부를 import 처리...
    }
}
```

<a name="dispatching-batches"></a>
### 배치 작업 디스패치

작업 집합을 배치로 디스패치하려면, `Bus` 파사드의 `batch` 메서드를 사용하면 됩니다. 보통 배치를 쓸 때는 완료 콜백과 결합하여 사용하는 것이 유용합니다. 따라서 `then`, `catch`, `finally` 등 메서드를 통해 배치 완료 시 동작할 콜백을 정의할 수 있습니다. 각 콜백은 실행 시점에 `Illuminate\Bus\Batch` 인스턴스를 인자로 받습니다. 아래 예시에서는 CSV 파일의 여러 행을 각각 처리하는 작업들을 배치로 등록한다고 가정합니다.

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
    // 배치가 생성되었지만 아직 작업이 추가되지 않은 상태
})->progress(function (Batch $batch) {
    // 단일 작업이 성공적으로 완료됨
})->then(function (Batch $batch) {
    // 모든 작업이 성공적으로 완료됨
})->catch(function (Batch $batch, Throwable $e) {
    // 최초의 작업 실패 발생 시
})->finally(function (Batch $batch) {
    // 배치 실행이 모두 끝남
})->dispatch();

return $batch->id;
```

배치의 ID는 `$batch->id` 속성으로 접근할 수 있으며, [라라벨 커맨드 버스의 배치 조회 기능](#inspecting-batches)을 통해 배치 실행 이후 관련 정보를 확인할 때 사용할 수 있습니다.

> [!WARNING]
> 배치 콜백은 직렬화되어 라라벨 큐에서 나중에 실행되기 때문에 콜백 내부에서 `$this` 변수는 사용할 수 없습니다. 또한, 배치 안에 포함된 작업들은 데이터베이스 트랜잭션 내에서 실행되므로, 암묵적 커밋을 발생시키는 데이터베이스 구문은 피해야 합니다.

<a name="naming-batches"></a>
#### 배치 이름 지정

Laravel Horizon, Laravel Telescope 등의 일부 도구에서는 배치에 이름을 지정하면 디버그 정보가 더 보기 좋게 표시될 수 있습니다. 배치에 이름을 할당하려면 배치 정의 시 `name` 메서드를 호출하세요.

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // 모든 작업이 성공적으로 완료됨
})->name('Import CSV')->dispatch();
```

<a name="batch-connection-queue"></a>
#### 배치의 연결 및 큐 설정

배치로 처리되는 작업들의 연결(connection)과 큐(queue)를 지정하고 싶다면, `onConnection`과 `onQueue` 메서드를 사용할 수 있습니다. 모든 배치 작업은 동일한 연결과 큐에서 실행되어야 합니다.

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // 모든 작업이 성공적으로 완료됨
})->onConnection('redis')->onQueue('imports')->dispatch();
```

<a name="chains-and-batches"></a>
### 체인과 배치 결합

배치 안에 [체인 작업 집합](#job-chaining)을 정의할 수 있습니다. 예를 들어, 두 개의 작업 체인을 동시에 실행하고 두 체인이 모두 끝나면 콜백을 실행할 수 있습니다.

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

반대로, [작업 체인](#job-chaining) 내에서 여러 개의 배치로 작업 집합을 실행할 수도 있습니다. 예를 들어, 먼저 여러 개의 팟캐스트를 공개하는 배치 작업을 실행한 후, 다시 공개 알림을 보내는 작업을 배치로 실행할 수 있습니다.

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

경우에 따라, 배치에 속한 작업 실행 중에 배치에 추가 작업을 넣고 싶을 때가 있습니다. 수천 개의 작업을 한 번에 큐에 디스패치하기에는 웹 요청 동안 너무 오래 걸릴 수 있기 때문에, 이 경우 초기에 "로더(loader)" 역할의 작업 몇 개로 배치를 시작하고, 이후 추가 작업을 배치에 동적으로 추가하는 패턴이 유용할 수 있습니다.

```php
$batch = Bus::batch([
    new LoadImportBatch,
    new LoadImportBatch,
    new LoadImportBatch,
])->then(function (Batch $batch) {
    // 모든 작업이 성공적으로 완료됨
})->name('Import Contacts')->dispatch();
```

위 예시에서는 `LoadImportBatch` 작업을 사용하여 추가 작업을 계속 배치에 추가합니다. 이를 위해 작업에서 제공하는 `batch` 메서드로 배치 인스턴스를 얻고, 그 위에서 `add` 메서드를 이용하여 작업을 추가할 수 있습니다.

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
> 배치 내부에서 같은 배치에 속한 작업만 추가할 수 있습니다.

<a name="inspecting-batches"></a>
### 배치 정보 조회

배치 완료 콜백에서 제공되는 `Illuminate\Bus\Batch` 인스턴스에는 해당 작업 집합을 조회하고 상호작용할 수 있는 다양한 속성과 메서드가 포함되어 있습니다.

```php
// 배치의 UUID
$batch->id;

// 배치 이름 (있다면)
$batch->name;

// 배치에 할당된 작업 수
$batch->totalJobs;

// 아직 큐에서 처리되지 않은 작업 수
$batch->pendingJobs;

// 실패한 작업 수
$batch->failedJobs;

// 지금까지 처리된 작업 수
$batch->processedJobs();

// 현재 배치의 완료율(0-100)
$batch->progress();

// 배치 실행 종료 여부
$batch->finished();

// 배치 실행 취소
$batch->cancel();

// 배치가 취소되었는지 여부
$batch->cancelled();
```

<a name="returning-batches-from-routes"></a>
#### 라우트에서 배치 반환

모든 `Illuminate\Bus\Batch` 인스턴스는 JSON으로 직렬화될 수 있으므로, 애플리케이션의 라우트에서 바로 반환하여 배치의 완료율 등 정보를 JSON 페이로드로 쉽게 조회할 수 있습니다. 이를 활용하면, 애플리케이션 UI에서 배치 진행 상황을 손쉽게 표시할 수 있습니다.

배치 ID로 특정 배치를 조회하려면, `Bus` 파사드의 `findBatch` 메서드를 사용하세요.

```php
use Illuminate\Support\Facades\Bus;
use Illuminate\Support\Facades\Route;

Route::get('/batch/{batchId}', function (string $batchId) {
    return Bus::findBatch($batchId);
});
```

<a name="cancelling-batches"></a>
### 배치 취소

특정 배치의 실행을 취소해야 할 때는, 해당 `Illuminate\Bus\Batch` 인스턴스의 `cancel` 메서드를 호출하면 됩니다.

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

이전 예시들처럼, 배치로 처리되는 작업에서는 실행 전에 해당 배치가 이미 취소됐는지 확인하는 것이 좋습니다. 보다 편리하게 구현하려면, 해당 작업에 `SkipIfBatchCancelled` [미들웨어](#job-middleware)를 지정할 수도 있습니다. 이 미들웨어는 배치가 취소된 경우 해당 작업을 실행하지 않도록 라라벨에 지시합니다.

```php
use Illuminate\Queue\Middleware\SkipIfBatchCancelled;

/**
 * 작업 실행 시 통과해야 할 미들웨어 반환
 */
public function middleware(): array
{
    return [new SkipIfBatchCancelled];
}
```

<a name="batch-failures"></a>
### 배치 실패

배치 내 작업이 실패하면, `catch` 콜백(지정된 경우)이 실행됩니다. 이 콜백은 배치에서 처음으로 실패한 작업에 대해서만 호출됩니다.

<a name="allowing-failures"></a>
#### 실패 허용

배치 내 작업이 실패하면 라라벨은 자동으로 해당 배치를 "취소됨(cancelled)" 상태로 표시합니다. 만약 작업 실패에도 배치가 자동으로 취소되지 않도록 하려면, 배치 디스패치 시 `allowFailures` 메서드를 호출하면 됩니다.

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // 모든 작업이 성공적으로 완료됨
})->allowFailures()->dispatch();
```

<a name="retrying-failed-batch-jobs"></a>
#### 실패한 배치 작업 재시도

실패한 배치 내 작업을 모두 쉽게 재시도할 수 있도록 라라벨은 `queue:retry-batch` 아티즌 명령어를 제공합니다. 이 명령어는 실패한 작업을 재시도할 배치의 UUID를 인자로 받습니다.

```shell
php artisan queue:retry-batch 32dbc76c-4f82-4749-b610-a639fe0099b5
```

<a name="pruning-batches"></a>
### 배치 자동 정리(Pruning)

배치 정보를 저장하는 `job_batches` 테이블은 관리하지 않으면 매우 빠르게 레코드가 누적될 수 있습니다. 이를 방지하기 위해, [스케줄러](/docs/12.x/scheduling)를 통해 `queue:prune-batches` 아티즌 명령어를 매일 자동 실행되도록 예약하는 것이 좋습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches')->daily();
```

기본적으로 완료된 지 24시간이 지난 모든 배치 레코드는 자동으로 정리(prune)됩니다. 보관 기간을 조정하려면 명령어 실행 시 `hours` 옵션을 사용할 수 있습니다. 아래 예시의 경우 48시간 이상 지난 배치를 삭제합니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48')->daily();
```

가끔 `jobs_batches` 테이블에는 실패한 작업이 끝내 재시도되지 않아 완료되지 않은 배치 정보가 누적될 수 있습니다. 이런 완료되지 않은 배치 기록도 `unfinished` 옵션을 통해 선택적으로 정리할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48 --unfinished=72')->daily();
```

마찬가지로, `jobs_batches` 테이블에는 취소된 배치 정보도 누적될 수 있습니다. 이 경우에는 `cancelled` 옵션을 이용해 해당 배치 기록을 정리할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48 --cancelled=72')->daily();
```

<a name="storing-batches-in-dynamodb"></a>

### DynamoDB에 배치 정보 저장

라라벨은 배치의 메타 정보를 [DynamoDB](https://aws.amazon.com/dynamodb)에 저장할 수 있도록 지원합니다. 단, 모든 배치 레코드를 저장할 DynamoDB 테이블은 직접 생성해야 합니다.

일반적으로 이 테이블의 이름은 `job_batches`이어야 하지만, 애플리케이션의 `queue` 설정 파일 내에서 `queue.batching.table` 설정값에 따라 테이블 이름을 지정해야 합니다.

<a name="dynamodb-batch-table-configuration"></a>
#### DynamoDB 배치 테이블 구성

`job_batches` 테이블에는 문자열 기본 파티션 키 `application`과 문자열 기본 정렬 키 `id`가 필요합니다. 키의 `application` 부분에는 애플리케이션의 `app` 설정 파일에서 지정한 `name` 값이 포함됩니다. 이처럼 애플리케이션 이름이 DynamoDB 테이블의 키에 포함되므로, 하나의 테이블을 여러 라라벨 애플리케이션의 작업 배치 저장소로 사용할 수 있습니다.

또한, [배치 자동 정리](#pruning-batches-in-dynamodb) 기능을 활용하려면 테이블에 `ttl` 속성(attribute)을 추가로 정의할 수 있습니다.

<a name="dynamodb-configuration"></a>
#### DynamoDB 설정

다음으로, 라라벨 애플리케이션이 Amazon DynamoDB와 통신할 수 있도록 AWS SDK를 설치해야 합니다.

```shell
composer require aws/aws-sdk-php
```

그런 다음 `queue.batching.driver` 설정 옵션의 값을 `dynamodb`로 지정합니다. 또한, `batching` 설정 배열에 `key`, `secret`, `region` 옵션을 추가해야 합니다. 이 옵션들은 AWS 인증에 사용됩니다. `dynamodb` 드라이버를 사용할 때는 `queue.batching.database` 설정 옵션이 필요하지 않습니다.

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
#### DynamoDB에서 배치 자동 정리

작업 배치 정보를 [DynamoDB](https://aws.amazon.com/dynamodb)에 저장하는 경우, 관계형 데이터베이스에 저장된 배치를 정리할 때 사용하던 일반적인 정리(Prune) 명령어들은 사용하실 수 없습니다. 대신, [DynamoDB의 기본 TTL(Time to Live) 기능](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html)을 활용하여 오래된 배치 레코드를 자동으로 삭제할 수 있습니다.

DynamoDB 테이블에 `ttl` 속성을 추가했다면, 라라벨이 배치 레코드를 어떻게 정리할지 설정값으로 지정할 수 있습니다. `queue.batching.ttl_attribute` 설정은 TTL 값을 저장하는 속성명을 명시하며, `queue.batching.ttl` 설정은 마지막으로 레코드가 업데이트된 시점 이후, 해당 배치 레코드를 DynamoDB 테이블에서 제거할 때까지의 기간(초 단위)을 지정합니다.

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

작업 클래스(job class)를 큐에 디스패치(dispatch)하는 대신, 클로저(closure)를 큐에 전달할 수도 있습니다. 이는 현재 요청 사이클과 분리되어 별도로 실행되어야 하는 간단한 작업을 빠르게 처리할 때 유용합니다. 클로저를 큐에 디스패치할 때, 클로저의 코드 내용은 암호학적으로 서명되어 전송 중(transport) 변조될 수 없습니다.

```php
$podcast = App\Podcast::find(1);

dispatch(function () use ($podcast) {
    $podcast->publish();
});
```

큐잉된 클로저에 이름을 부여하려면 `name` 메서드를 사용할 수 있습니다. 이 이름은 큐 대시보드에서 조회될 수 있으며, `queue:work` 명령어에서도 표시됩니다.

```php
dispatch(function () {
    // ...
})->name('Publish Podcast');
```

`catch` 메서드를 사용하여, 지정한 모든 [재시도 횟수](#max-job-attempts-and-timeout)가 소진된 후에도 큐잉된 클로저가 정상적으로 실행되지 못했을 때 동작할 클로저를 추가로 정의할 수 있습니다.

```php
use Throwable;

dispatch(function () use ($podcast) {
    $podcast->publish();
})->catch(function (Throwable $e) {
    // 이 작업은 실패했습니다...
});
```

> [!WARNING]
> `catch` 콜백은 라라벨 큐에 의해 직렬화되어 이후에 실행됩니다. 따라서 `catch` 콜백 내에서는 `$this` 변수를 사용하지 않아야 합니다.

<a name="running-the-queue-worker"></a>
## 큐 워커 실행하기

<a name="the-queue-work-command"></a>
### `queue:work` 명령어

라라벨에는 새로운 작업이 큐에 추가될 때 처리하는 큐 워커(worker)를 시작하는 Artisan 명령어가 포함되어 있습니다. `queue:work` Artisan 명령어로 워커를 실행할 수 있습니다. 이 명령어는 한 번 시작하면 수동으로 중지하거나 터미널을 닫을 때까지 계속 실행됩니다.

```shell
php artisan queue:work
```

> [!NOTE]
> `queue:work` 프로세스를 영구적으로 백그라운드에서 실행하려면, [Supervisor](#supervisor-configuration)와 같은 프로세스 모니터를 사용해 큐 워커가 중단되지 않도록 유지해야 합니다.

처리된 작업의 ID도 함께 출력하고 싶다면, `queue:work` 명령어에 `-v` 플래그를 추가로 사용할 수 있습니다.

```shell
php artisan queue:work -v
```

큐 워커는 오랜 시간 실행되는 프로세스이기 때문에, 애플리케이션이 부팅된 상태가 메모리에 저장됩니다. 즉, 워커가 시작된 후에 코드에 변경이 있더라도 이를 감지하지 못합니다. 따라서 배포(Deploy) 과정에서 반드시 [큐 워커를 재시작](#queue-workers-and-deployment)해야 합니다. 또한, 애플리케이션에서 생성되었거나 변경된 정적(static) 상태는 각 작업(job) 간 자동으로 초기화되지 않습니다.

만약 코드를 수정하거나 애플리케이션 상태를 재설정하고 싶을 때 워커를 수동으로 재시작하고 싶지 않다면, `queue:listen` 명령어를 사용할 수도 있습니다. 그러나 이 명령어는 `queue:work` 명령어에 비해 효율성이 상당히 떨어집니다.

```shell
php artisan queue:listen
```

<a name="running-multiple-queue-workers"></a>
#### 여러 큐 워커 실행

큐에 여러 워커를 할당하여 작업을 동시에(병렬로) 처리하려면, `queue:work` 프로세스를 여러 개 실행하면 됩니다. 이는 로컬 환경에서는 터미널에서 여러 탭을 사용해 실행하거나, 운영 환경에서는 프로세스 관리자의 설정을 통해 가능합니다. [Supervisor를 사용할 때](#supervisor-configuration)는 `numprocs` 설정값을 지정할 수 있습니다.

<a name="specifying-the-connection-queue"></a>
#### 연결 및 큐 선택 지정

워커가 사용할 큐 연결(connection)을 직접 지정할 수도 있습니다. `work` 명령어에 전달하는 연결 이름은 `config/queue.php` 설정 파일에 정의된 연결명과 일치해야 합니다.

```shell
php artisan queue:work redis
```

기본적으로 `queue:work` 명령어는 지정한 연결에서 기본 큐만 처리합니다. 하지만, 특정 큐만 처리하도록 워커 동작을 더 세밀하게 설정할 수도 있습니다. 예를 들어, 모든 이메일 발송 작업이 `redis` 큐 연결의 `emails` 큐에서 처리된다면, 다음과 같이 해당 큐만 처리하는 워커를 시작할 수 있습니다.

```shell
php artisan queue:work redis --queue=emails
```

<a name="processing-a-specified-number-of-jobs"></a>
#### 지정된 개수의 작업만 처리하기

`--once` 옵션을 사용하면 워커가 큐에서 단일 작업만 처리하도록 할 수 있습니다.

```shell
php artisan queue:work --once
```

`--max-jobs` 옵션은 워커가 지정된 개수의 작업을 처리한 후 종료하도록 설정합니다. 이 옵션을 [Supervisor](#supervisor-configuration)와 함께 사용하면, 워커가 메모리를 과다하게 점유했을 때 지정한 작업 수만큼 처리 후 자동으로 재시작되게 할 수 있습니다.

```shell
php artisan queue:work --max-jobs=1000
```

<a name="processing-all-queued-jobs-then-exiting"></a>
#### 모든 큐 작업 처리 후 종료하기

`--stop-when-empty` 옵션을 사용하면 워커가 큐에 쌓인 모든 작업을 처리한 후 정상적으로 종료할 수 있습니다. 도커 컨테이너 내에서 라라벨 큐를 처리할 때, 큐가 비워지면 컨테이너를 종료시키고 싶을 때 유용합니다.

```shell
php artisan queue:work --stop-when-empty
```

<a name="processing-jobs-for-a-given-number-of-seconds"></a>
#### 지정된 시간 동안 작업 처리하기

`--max-time` 옵션을 사용하면 워커가 지정한(초 단위로) 시간 동안만 작업을 처리하고 종료하도록 할 수 있습니다. 이 옵션 역시 [Supervisor](#supervisor-configuration)와 결합해 일정 시간 마다 워커를 재시작할 수 있게 활용됩니다.

```shell
# 한 시간 동안 작업을 처리하고 종료...
php artisan queue:work --max-time=3600
```

<a name="worker-sleep-duration"></a>
#### 워커의 대기(sleep) 시간

큐에 작업이 있다면 워커는 지연 없이 계속 작업을 처리합니다. 그러나 `sleep` 옵션은 큐에 작업이 없을 때 워커가 얼마나 오래 대기할지를 결정합니다. 워커가 대기 중일 때는 새로운 작업을 처리하지 않습니다.

```shell
php artisan queue:work --sleep=3
```

<a name="maintenance-mode-queues"></a>
#### 유지보수 모드와 큐

애플리케이션이 [유지보수 모드](/docs/12.x/configuration#maintenance-mode)일 때는 큐에 쌓인 작업이 처리되지 않습니다. 유지보수 모드가 해제되면, 쌓인 작업들은 정상적으로 처리됩니다.

유지보수 모드에서도 큐 워커가 작업을 강제로 처리하게 하려면 `--force` 옵션을 사용합니다.

```shell
php artisan queue:work --force
```

<a name="resource-considerations"></a>
#### 자원(Resource) 관리 주의사항

데몬 기반의 큐 워커는 각 작업을 처리할 때마다 프레임워크를 재부팅하지 않습니다. 따라서 각 작업이 완료된 후에는 메모리나 리소스를 직접 해제해야 합니다. 예를 들어 GD 라이브러리로 이미지 작업을 했다면, 처리가 끝난 후에는 반드시 `imagedestroy` 함수를 호출해 메모리를 해제해야 합니다.

<a name="queue-priorities"></a>
### 큐 우선순위

경우에 따라 큐별로 작업 처리의 우선순위를 지정하고 싶을 때가 있습니다. 예를 들어 `config/queue.php` 설정 파일에서 `redis` 연결의 기본 `queue` 값을 `low`로 설정했다고 합시다. 하지만, 가끔은 높은 우선순위가 필요한 작업을 `high` 큐로 보내고 싶을 수도 있습니다.

```php
dispatch((new Job)->onQueue('high'));
```

`work` 명령에 큐 이름을 콤마(,)로 구분해 여러 개 전달하면, 먼저 `high` 큐의 작업이 모두 처리된 후에 `low` 큐의 작업으로 넘어가도록 할 수 있습니다.

```shell
php artisan queue:work --queue=high,low
```

<a name="queue-workers-and-deployment"></a>
### 큐 워커와 배포(Deployment)

큐 워커는 오랜 시간 실행되는 프로세스이기 때문에, 코드를 수정해도 워커를 재시작하지 않는 한 변경 사항이 반영되지 않습니다. 따라서 큐 워커를 사용하는 애플리케이션을 배포할 때는, 배포 과정에서 워커를 재시작하는 것이 가장 간단한 방법입니다. `queue:restart` 명령어로 모든 워커를 정상적으로(gracefully) 재시작할 수 있습니다.

```shell
php artisan queue:restart
```

이 명령어는 각 큐 워커에게 현재 진행 중인 작업이 끝나면 정상적으로 종료하도록 지시합니다. 덕분에 진행 중이었던 작업이 유실되지 않습니다. 워커가 명령 실행 시점에 종료되므로, [Supervisor](#supervisor-configuration)와 같은 프로세스 관리자를 사용해 자동으로 워커를 다시 실행시켜 주어야 합니다.

> [!NOTE]
> 큐에서는 [캐시](/docs/12.x/cache)에 재시작 신호를 저장합니다. 이 기능 사용 전, 애플리케이션에 적절한 캐시 드라이버가 설정되어 있는지 확인해야 합니다.

<a name="job-expirations-and-timeouts"></a>
### 작업 만료 및 타임아웃

<a name="job-expiration"></a>
#### 작업 만료

`config/queue.php` 설정 파일의 각 큐 연결에는 `retry_after` 옵션이 있습니다. 이 옵션은 어떤 작업이 처리 중일 때, 지정한 초(seconds)만큼 기다린 후 해당 작업을 큐로 다시 되돌릴지를 설정합니다. 예를 들어 `retry_after` 값을 90으로 지정하면, 한 작업이 90초 동안 처리 중(삭제 또는 릴리즈되지 않은 상태)이라면 다시 큐로 반환됩니다. 보통 이 값은 작업이 완료될 때까지 예상되는 최대 소요 시간으로 설정합니다.

> [!WARNING]
> Amazon SQS만은 `retry_after` 옵션이 없습니다. SQS는 [기본 가시성 타임아웃(Default Visibility Timeout)](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/AboutVT.html)에 따라 재시도 결정이 이루어지며, 이 값은 AWS 콘솔에서 직접 관리합니다.

<a name="worker-timeouts"></a>
#### 워커 타임아웃

`queue:work` Artisan 명령어에는 `--timeout` 옵션이 있습니다. 기본값은 60초입니다. 만약 작업이 지정한 타임아웃 시간(초 단위)보다 오래 걸리면, 작업을 처리하던 워커가 에러와 함께 종료됩니다. 대부분의 경우, 서버에 [프로세스 관리자가 설정되어 있다면](#supervisor-configuration) 워커가 자동으로 재시작됩니다.

```shell
php artisan queue:work --timeout=60
```

`retry_after` 설정값과 CLI의 `--timeout` 옵션은 서로 다르지만, 두 옵션이 함께 동작해 작업이 중복 처리되지 않고, 유실되지 않도록 보장합니다.

> [!WARNING]
> `--timeout` 값은 항상 `retry_after` 설정값보다 반드시 몇 초 짧아야 합니다. 이렇게 해야, 문제가 생긴(frozen) 작업을 처리하는 워커가 작업을 재시도하기 전에 강제로 종료되어야 합니다. 반대로 `--timeout` 값이 `retry_after` 값보다 길면 작업이 중복 처리될 수 있습니다.

<a name="supervisor-configuration"></a>
## Supervisor 설정

운영 환경에서는 `queue:work` 프로세스가 항상 실행되도록 관리해야 합니다. `queue:work` 프로세스는 워커 타임아웃 초과, `queue:restart` 명령 실행 등 다양한 이유로 중단될 수 있습니다.

따라서 프로세스 모니터를 설정해 `queue:work` 프로세스가 종료되었는지 감지하고, 자동으로 재시작해야 합니다. 또한 프로세스 모니터를 활용하면 원하는 만큼 여러 개의 `queue:work` 프로세스를 동시에 실행할 수 있습니다. Supervisor는 일반적으로 리눅스 환경에서 사용하는 대표적 프로세스 모니터로, 아래에서 설정 방법을 살펴보겠습니다.

<a name="installing-supervisor"></a>
#### Supervisor 설치

Supervisor는 리눅스 운영체제용 프로세스 모니터로, 워커 프로세스가 실패할 경우 자동으로 재시작해 줍니다. Ubuntu에서는 다음 명령으로 Supervisor를 설치할 수 있습니다.

```shell
sudo apt-get install supervisor
```

> [!NOTE]
> Supervisor 직접 설정 및 관리가 복잡하게 느껴진다면, 라라벨 큐 워커를 완전히 관리형 플랫폼에서 실행할 수 있는 [Laravel Cloud](https://cloud.laravel.com)을 고려해 보세요.

<a name="configuring-supervisor"></a>
#### Supervisor 설정

Supervisor 설정 파일은 일반적으로 `/etc/supervisor/conf.d` 디렉토리에 저장됩니다. 이 디렉토리 안에 원하는 만큼 설정 파일을 만들어, Supervisor가 어떤 프로세스를 어떻게 모니터할지 정의할 수 있습니다. 예를 들어, `laravel-worker.conf` 파일을 만들어 `queue:work` 프로세스를 시작 및 모니터링해 봅니다.

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

위 예시에서 `numprocs` 지시어는 Supervisor가 8개의 `queue:work` 프로세스를 실행 및 모니터링하도록 지정합니다. 각자의 환경에 맞게 `command` 지시어(큐 연결명, 워커 옵션)를 변경해서 사용하시면 됩니다.

> [!WARNING]
> `stopwaitsecs` 값은 가장 오래 걸리는 작업의 소요 시간보다 길어야 합니다. 그렇지 않으면 Supervisor가 작업이 끝나기 전에 강제로 프로세스를 종료할 수 있습니다.

<a name="starting-supervisor"></a>
#### Supervisor 시작

설정 파일을 생성(또는 수정)한 뒤, 다음 명령어로 Supervisor 설정을 갱신하고 프로세스를 시작할 수 있습니다.

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start "laravel-worker:*"
```

Supervisor에 대한 더 자세한 내용은 [Supervisor 공식 문서](http://supervisord.org/index.html)를 참고하세요.

<a name="dealing-with-failed-jobs"></a>
## 실패한 작업 처리하기

큐에 넣은 작업이 실패할 때가 있습니다. 당황하지 마세요, 생각한 대로 항상 일이 잘 풀리지는 않습니다! 라라벨에는 [작업의 최대 시도 횟수 지정](#max-job-attempts-and-timeout)이 가능한 편리한 기능이 포함되어 있습니다. 비동기 작업이 지정한 횟수를 초과해도 처리에 성공하지 못하면, 해당 작업은 `failed_jobs` 데이터베이스 테이블에 저장됩니다. [동기 방식(synchronous)으로 디스패치한 작업](/docs/12.x/queues#synchronous-dispatching)의 실패는 이 테이블에 저장되지 않으며, 애플리케이션 예외로 즉시 처리됩니다.

신규 라라벨 애플리케이션에는 `failed_jobs` 테이블 생성을 위한 마이그레이션이 이미 포함되어 있습니다. 만약 해당 마이그레이션이 없다면, 아래 명령어로 추가할 수 있습니다.

```shell
php artisan make:queue-failed-table

php artisan migrate
```

[큐 워커](#running-the-queue-worker) 프로세스를 실행할 때, `queue:work` 명령어의 `--tries` 옵션으로 한 작업에 대해 최대 몇 번까지 재시도할지 지정할 수 있습니다. 별도 값을 지정하지 않으면, 각 작업 클래스의 `$tries` 속성값 또는 기본 1회만 시도합니다.

```shell
php artisan queue:work redis --tries=3
```

또한 `--backoff` 옵션으로, 작업 처리 중 예외가 발생한 경우 작업을 재시도하기 전 대기할 시간을(초 단위로) 설정할 수 있습니다. 기본적으로는 즉시 큐로 작업이 복귀(release)되어 다시 시도됩니다.

```shell
php artisan queue:work redis --tries=3 --backoff=3
```

작업마다 재시도 대기 시간을 개별적으로 지정하고 싶다면, 작업 클래스에 `backoff` 속성을 정의하면 됩니다.

```php
/**
 * 작업 재시도 전 대기할 시간(초).
 *
 * @var int
 */
public $backoff = 3;
```

더 복잡한 규칙의 대기 시간이 필요하다면, 작업 클래스에 `backoff` 메서드를 정의할 수 있습니다.

```php
/**
 * 재시도 전 대기할 시간을 계산합니다.
 */
public function backoff(): int
{
    return 3;
}
```

"지수적" 대기 시간을 지정하려면, `backoff` 메서드에서 대기 시간 배열을 반환해주세요. 아래 예시는 첫 번째 재시도는 1초, 두 번째는 5초, 세 번째와 이후 재시도는 10초 대기하게 됩니다.

```php
/**
 * 작업 재시도 전 대기할 시간(초) 계산.
 *
 * @return array<int, int>
 */
public function backoff(): array
{
    return [1, 5, 10];
}
```

<a name="cleaning-up-after-failed-jobs"></a>
### 실패한 작업 후 정리하기

특정 작업이 실패했을 때 사용자에게 알림을 보내거나, 작업 중 일부만 완료되었던 작업을 원복(롤백)하고 싶을 수도 있습니다. 이를 위해, 작업 클래스에 `failed` 메서드를 정의하면 됩니다. 이 메서드에는 작업이 실패하도록 만든 `Throwable` 인스턴스가 전달됩니다.

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
     * 새로운 작업 인스턴스 생성.
     */
    public function __construct(
        public Podcast $podcast,
    ) {}

    /**
     * 작업 실행.
     */
    public function handle(AudioProcessor $processor): void
    {
        // 업로드된 팟캐스트 처리...
    }

    /**
     * 작업 실패 시 처리.
     */
    public function failed(?Throwable $exception): void
    {
        // 실패 알림 전송 등...
    }
}
```

> [!WARNING]
> `failed` 메서드가 호출되기 전, 해당 작업의 새 인스턴스가 새로 생성됩니다. 따라서 `handle` 메서드 내에서 변경한 클래스 속성 값은 모두 소실됩니다.

<a name="retrying-failed-jobs"></a>
### 실패한 작업 재시도하기

`failed_jobs` 데이터베이스 테이블에 저장된 모든 실패 작업 목록은 `queue:failed` Artisan 명령어로 확인할 수 있습니다.

```shell
php artisan queue:failed
```

`queue:failed` 명령은 작업 ID, 연결명, 큐 이름, 실패 시간 등 작업 정보를 출력합니다. 이 중 작업 ID를 사용해 해당 실패 작업을 재시도할 수 있습니다. 예를 들어, ID가 `ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece`인 작업을 재시도하려면 다음 명령어를 실행하세요.

```shell
php artisan queue:retry ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece
```

필요하다면 여러 작업 ID를 한 번에 전달할 수도 있습니다.

```shell
php artisan queue:retry ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece 91401d2c-0784-4f43-824c-34f94a33c24d
```

특정 큐의 모든 실패 작업만 재시도하려면 아래와 같이 명령어를 사용할 수 있습니다.

```shell
php artisan queue:retry --queue=name
```

모든 실패 작업을 한 번에 재시도하려면, `queue:retry` 명령에 `all`을 ID 대신 전달하십시오.

```shell
php artisan queue:retry all
```

실패한 작업을 삭제하려면 `queue:forget` 명령어를 사용할 수 있습니다.

```shell
php artisan queue:forget 91401d2c-0784-4f43-824c-34f94a33c24d
```

> [!NOTE]
> [Horizon](/docs/12.x/horizon) 사용 시, `queue:forget` 대신 `horizon:forget` 명령어로 실패한 작업을 삭제하세요.

`failed_jobs` 테이블에 기록된 모든 실패 작업을 한 번에 삭제하려면 `queue:flush` 명령어를 사용하세요.

```shell
php artisan queue:flush
```

<a name="ignoring-missing-models"></a>
### 누락된 모델 무시하기

작업에 Eloquent 모델을 인젝션하면, 해당 모델은 큐에 넣기 전에 직렬화되고, 작업 처리 시점에 데이터베이스에서 다시 조회됩니다. 그러나 작업이 큐에서 대기하는 동안 모델이 삭제되었을 경우, 작업이 `ModelNotFoundException`으로 실패할 수 있습니다.

이럴 때, 작업 클래스의 `deleteWhenMissingModels` 속성을 `true`로 설정하면 해당 모델이 존재하지 않을 경우 예외를 발생시키지 않고, 조용히 해당 작업을 삭제할 수 있습니다.

```php
/**
 * 모델이 더 이상 존재하지 않으면 작업 삭제.
 *
 * @var bool
 */
public $deleteWhenMissingModels = true;
```

<a name="pruning-failed-jobs"></a>
### 실패 작업 기록 자동 정리

`queue:prune-failed` Artisan 명령어로 애플리케이션의 `failed_jobs` 테이블에서 오래된 작업 기록을 정리할 수 있습니다.

```shell
php artisan queue:prune-failed
```

기본적으로 24시간 이상 지난 모든 실패 작업이 정리됩니다. `--hours` 옵션을 지정하면, 최근 N시간 이내에 기록된 실패 작업만 남기고, 그보다 오래된 작업 기록은 삭제됩니다. 아래 예시는 48시간 이상 지난 실패 기록을 모두 삭제합니다.

```shell
php artisan queue:prune-failed --hours=48
```

<a name="storing-failed-jobs-in-dynamodb"></a>
### DynamoDB에 실패한 작업 저장

라라벨은 관계형 데이터베이스 대신 [DynamoDB](https://aws.amazon.com/dynamodb)에 실패한 작업 기록을 저장하는 기능도 지원합니다. 이때도 모든 실패 작업 레코드를 저장할 DynamoDB 테이블은 직접 생성해야 합니다. 기본적으로 이 테이블 이름은 `failed_jobs`이어야 하지만, 애플리케이션의 `queue` 설정 파일 내 `queue.failed.table` 설정값을 바탕으로 테이블 이름을 지정해야 합니다.

`failed_jobs` 테이블에는 문자열 기본 파티션 키 `application`과 문자열 기본 정렬 키 `uuid`가 필요합니다. 키의 `application` 부분에는 애플리케이션의 `app` 설정 파일에서 정의한 `name` 값이 들어갑니다. 애플리케이션 이름이 DynamoDB 테이블 키에 포함되어 있으므로, 여러 라라벨 애플리케이션의 실패 작업 기록을 하나의 테이블에 저장할 수도 있습니다.

또한, 반드시 AWS SDK를 설치해서 라라벨 애플리케이션이 Amazon DynamoDB와 통신할 수 있도록 해야 합니다.

```shell
composer require aws/aws-sdk-php
```

이제 `queue.failed.driver` 설정값을 `dynamodb`로 지정합니다. 그리고 실패작업 저장 설정 배열에 `key`, `secret`, `region` 값을 명시해야 합니다. 모두 AWS 인증에 사용됩니다. `dynamodb` 드라이버 사용 시에는 `queue.failed.database` 설정 옵션이 필요하지 않습니다.

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
### 실패 작업 저장 비활성화

실패한 작업을 저장하지 않고 즉시 폐기하려면, `queue.failed.driver` 설정 옵션 값을 `null`로 지정하면 됩니다. 보통 환경 변수로 다음과 같이 처리할 수 있습니다.

```ini
QUEUE_FAILED_DRIVER=null
```

<a name="failed-job-events"></a>
### 실패 작업 이벤트

작업 실패 시 실행되는 이벤트 리스너를 등록하려면, `Queue` 파사드의 `failing` 메서드를 사용할 수 있습니다. 예를 들어, 라라벨에 포함된 `AppServiceProvider`의 `boot` 메서드에서 익명 함수(클로저)로 해당 이벤트를 등록할 수 있습니다.

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
> [Horizon](/docs/12.x/horizon)을 사용하는 경우, `queue:clear` 명령어 대신 `horizon:clear` 명령어로 큐의 작업을 삭제해야 합니다.

기본 연결의 기본 큐에서 모든 작업을 삭제하고 싶다면, 아래와 같이 `queue:clear` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan queue:clear
```

특정 연결과 큐에서 작업을 삭제하고자 할 때는 `connection` 인수와 `queue` 옵션을 함께 지정할 수 있습니다.

```shell
php artisan queue:clear redis --queue=emails
```

> [!WARNING]
> 큐에서 작업을 삭제하는 기능은 SQS, Redis, 그리고 데이터베이스 큐 드라이버에서만 지원됩니다. 또한 SQS의 메시지 삭제 과정은 최대 60초가 소요될 수 있으므로, 큐를 비운 이후 60초 이내에 SQS 큐로 전송된 작업도 함께 삭제될 수 있습니다.

<a name="monitoring-your-queues"></a>
## 큐 모니터링하기

큐에 갑자기 많은 작업이 몰리면, 큐가 과부하 상태에 빠져 작업 처리 대기 시간이 길어질 수 있습니다. 이런 상황을 방지하고 싶다면, 지정한 임계값을 초과할 경우 라라벨에서 큐 작업 개수에 대한 알림을 받을 수 있습니다.

먼저, `queue:monitor` 명령어를 [매 분마다 실행](/docs/12.x/scheduling) 하도록 예약해야 합니다. 이 명령어는 모니터링할 큐 이름과, 임계값으로 사용할 최대 작업 수를 인자로 받습니다.

```shell
php artisan queue:monitor redis:default,redis:deployments --max=100
```

이 명령어만 예약한다고 해서 과부하 상태 알림이 바로 전송되지는 않습니다. 큐 작업 개수가 임계값을 초과하면, `Illuminate\Queue\Events\QueueBusy` 이벤트가 발생합니다. 이 이벤트를 앱의 `AppServiceProvider` 내에서 감지하여 본인이나 개발팀에 알림을 보낼 수 있습니다.

```php
use App\Notifications\QueueHasLongWaitTime;
use Illuminate\Queue\Events\QueueBusy;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\Facades\Notification;

/**
 * Bootstrap any application services.
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
## 테스트하기

작업을 디스패치하는 코드를 테스트할 때는, 실제 작업이 바로 실행되지 않도록 라라벨에 지시하는 것이 도움이 될 수 있습니다. 작업 코드 자체는 개별적으로 테스트할 수 있으므로, 작업을 실행하는 코드와 분리하여 각각 검증할 수 있습니다. 작업 자체를 테스트하려면 테스트 내에서 작업 인스턴스를 생성하고 `handle` 메서드를 직접 호출하면 됩니다.

큐 작업이 실제로 큐에 푸시되지 않도록 하려면 `Queue` 파사드의 `fake` 메서드를 호출하면 됩니다. 이후, 해당 메서드 호출 후에 특정 작업이 큐에 푸시되었는지 또는 안 되었는지 검증할 수 있습니다.

```php tab=Pest
<?php

use App\Jobs\AnotherJob;
use App\Jobs\FinalJob;
use App\Jobs\ShipOrder;
use Illuminate\Support\Facades\Queue;

test('orders can be shipped', function () {
    Queue::fake();

    // Perform order shipping...

    // Assert that no jobs were pushed...
    Queue::assertNothingPushed();

    // Assert a job was pushed to a given queue...
    Queue::assertPushedOn('queue-name', ShipOrder::class);

    // Assert a job was pushed twice...
    Queue::assertPushed(ShipOrder::class, 2);

    // Assert a job was not pushed...
    Queue::assertNotPushed(AnotherJob::class);

    // Assert that a Closure was pushed to the queue...
    Queue::assertClosurePushed();

    // Assert the total number of jobs that were pushed...
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

        // Perform order shipping...

        // Assert that no jobs were pushed...
        Queue::assertNothingPushed();

        // Assert a job was pushed to a given queue...
        Queue::assertPushedOn('queue-name', ShipOrder::class);

        // Assert a job was pushed twice...
        Queue::assertPushed(ShipOrder::class, 2);

        // Assert a job was not pushed...
        Queue::assertNotPushed(AnotherJob::class);

        // Assert that a Closure was pushed to the queue...
        Queue::assertClosurePushed();

        // Assert the total number of jobs that were pushed...
        Queue::assertCount(3);
    }
}
```

`assertPushed` 또는 `assertNotPushed` 메서드에는 클로저를 전달해, 주어진 "진실성 테스트(조건)"을 통과한 작업이 푸시되었는지 검증할 수 있습니다. 조건을 만족하는 작업이 하나라도 푸시됐다면 검증이 성공합니다.

```php
Queue::assertPushed(function (ShipOrder $job) use ($order) {
    return $job->order->id === $order->id;
});
```

<a name="faking-a-subset-of-jobs"></a>
### 일부 작업만 페이크 처리하기

특정 작업만 페이크 처리하고, 다른 작업들은 정상적으로 실행되게 하고 싶을 때는 `fake` 메서드에 페이크로 만들 작업의 클래스명을 배열로 전달하면 됩니다.

```php tab=Pest
test('orders can be shipped', function () {
    Queue::fake([
        ShipOrder::class,
    ]);

    // Perform order shipping...

    // Assert a job was pushed twice...
    Queue::assertPushed(ShipOrder::class, 2);
});
```

```php tab=PHPUnit
public function test_orders_can_be_shipped(): void
{
    Queue::fake([
        ShipOrder::class,
    ]);

    // Perform order shipping...

    // Assert a job was pushed twice...
    Queue::assertPushed(ShipOrder::class, 2);
}
```

`except` 메서드를 사용하면, 특정 작업만 제외하고 나머지 모든 작업을 페이크 해줄 수 있습니다.

```php
Queue::fake()->except([
    ShipOrder::class,
]);
```

<a name="testing-job-chains"></a>
### 작업 체인 테스트하기

작업 체인(job chain)을 테스트하려면 `Bus` 파사드의 페이킹 기능을 활용해야 합니다. `Bus` 파사드의 `assertChained` 메서드는 [연결된 작업 체인](/docs/12.x/queues#job-chaining)이 디스패치되었는지 검증할 수 있습니다. `assertChained` 메서드에는 체인에 포함될 작업들을 배열 형태로 인자로 전달합니다.

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

위 예제와 같이 작업 클래스명을 배열로 전달할 수도 있고, 실제 작업 인스턴스를 배열로 전달할 수도 있습니다. 이 경우 라라벨은 작업 인스턴스의 클래스와 속성 값이 실제로 애플리케이션에서 체인으로 디스패치된 것과 동일한지 검사합니다.

```php
Bus::assertChained([
    new ShipOrder,
    new RecordShipment,
    new UpdateInventory,
]);
```

`assertDispatchedWithoutChain` 메서드를 이용하면, 특정 작업이 체인 없이 단독으로 디스패치되었는지 검증할 수 있습니다.

```php
Bus::assertDispatchedWithoutChain(ShipOrder::class);
```

<a name="testing-chain-modifications"></a>
#### 체인 수정 테스트하기

체인에 걸린 작업이 [기존 체인 앞뒤로 작업을 추가](#adding-jobs-to-the-chain)한다면, 해당 작업 인스턴스의 `assertHasChain` 메서드로 체인이 기대한 대로 남아있는지 검증할 수 있습니다.

```php
$job = new ProcessPodcast;

$job->handle();

$job->assertHasChain([
    new TranscribePodcast,
    new OptimizePodcast,
    new ReleasePodcast,
]);
```

`assertDoesntHaveChain` 메서드를 사용하면 작업의 남은 체인이 비어 있는지 확인할 수 있습니다.

```php
$job->assertDoesntHaveChain();
```

<a name="testing-chained-batches"></a>
#### 체인에 포함된 배치 테스트하기

만약 작업 체인에 [배치 작업](#chains-and-batches)이 포함되어 있다면, 체인 검증 시 `Bus::chainedBatch`를 체인 배열에 포함시켜 배치의 기대 조건을 명시적으로 검증할 수 있습니다.

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
### 배치 작업 테스트하기

`Bus` 파사드의 `assertBatched` 메서드를 사용하면, [배치 작업](/docs/12.x/queues#job-batching)이 디스패치되었는지 검증할 수 있습니다. 이 메서드에 전달하는 클로저는 `Illuminate\Bus\PendingBatch` 인스턴스를 인자로 받아 배치 안의 작업들을 살펴볼 수 있습니다.

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

디스패치된 배치의 개수가 특정 숫자임을 검증하려면 `assertBatchCount` 메서드를 사용할 수 있습니다.

```php
Bus::assertBatchCount(3);
```

아무 배치도 디스패치되지 않았는지 확인하려면 `assertNothingBatched`를 사용합니다.

```php
Bus::assertNothingBatched();
```

<a name="testing-job-batch-interaction"></a>
#### 개별 작업과 배치의 상호작용 테스트

개별 작업이 소속된 배치와 어떻게 상호작용하는지 테스트해야 할 때도 있습니다. 예를 들어, 작업이 배치의 후속 처리를 취소하는 로직이 정상 동작하는지 검증해야 할 수 있습니다. 이 경우 `withFakeBatch` 메서드로 작업에 페이크 배치를 할당해주면 됩니다. 이 메서드는 작업 인스턴스와 페이크 배치가 쌍으로 담긴 배열을 반환합니다.

```php
[$job, $batch] = (new ShipOrder)->withFakeBatch();

$job->handle();

$this->assertTrue($batch->cancelled());
$this->assertEmpty($batch->added);
```

<a name="testing-job-queue-interactions"></a>
### 작업과 큐 간의 상호작용 테스트

때론 큐에 있는 작업이 [스스로 다시 큐에 올라가도록 리리스](#manually-releasing-a-job)하거나, 직접 자신의 삭제를 수행하는지 등을 테스트해야 할 수도 있습니다. 이럴 때는 작업 인스턴스를 만들고 `withFakeQueueInteractions` 메서드를 호출하면 됩니다.

큐와의 상호작용이 페이크 처리된 이후에는 그 작업 인스턴스의 `handle` 메서드를 호출하면 됩니다. 작업이 실행된 후에는, `assertReleased`, `assertDeleted`, `assertNotDeleted`, `assertFailed`, `assertFailedWith`, `assertNotFailed` 등의 메서드로 작업의 큐 동작을 검증할 수 있습니다.

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

`Queue` [파사드](/docs/12.x/facades)의 `before`, `after` 메서드를 사용하여, 큐 작업이 처리되기 전이나 후에 콜백 함수를 실행할 수 있습니다. 이 콜백에서는 별도의 로그를 남기거나 대시보드 통계를 집계하는 등의 추가 작업을 할 수 있습니다. 보통은 이런 메서드를 [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에서 호출해 둡니다. 예를 들어, 라라벨에 기본 탑재된 `AppServiceProvider`를 아래와 같이 활용할 수 있습니다.

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
     * Register any application services.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * Bootstrap any application services.
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

`Queue` [파사드](/docs/12.x/facades)의 `looping` 메서드를 활용하면, 워커가 큐에서 작업을 가져오기 전에 실행할 콜백을 지정할 수 있습니다. 예를 들어, 이전에 실패한 작업이 남겨놓은 데이터베이스 트랜잭션이 있다면 아래와 같이 롤백 처리를 등록할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Queue;

Queue::looping(function () {
    while (DB::transactionLevel() > 0) {
        DB::rollBack();
    }
});
```