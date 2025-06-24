# 큐 (Queues)

- [소개](#introduction)
    - [커넥션과 큐의 차이](#connections-vs-queues)
    - [드라이버별 안내 및 필요 사항](#driver-prerequisites)
- [잡(Job) 생성](#creating-jobs)
    - [잡 클래스 생성하기](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [유일한 잡(Unique Jobs)](#unique-jobs)
    - [암호화된 잡(Encrypted Jobs)](#encrypted-jobs)
- [잡 미들웨어](#job-middleware)
    - [속도 제한(Rate Limiting)](#rate-limiting)
    - [잡 중첩 방지](#preventing-job-overlaps)
    - [예외 처리 지연(Throttling Exceptions)](#throttling-exceptions)
    - [잡 스킵(건너뛰기)](#skipping-jobs)
- [잡 디스패치](#dispatching-jobs)
    - [디스패치 지연시키기](#delayed-dispatching)
    - [동기식 디스패치](#synchronous-dispatching)
    - [잡과 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [잡 체이닝](#job-chaining)
    - [커넥션 및 큐 커스터마이징](#customizing-the-queue-and-connection)
    - [최대 시도 횟수 및 타임아웃 지정](#max-job-attempts-and-timeout)
    - [에러 처리](#error-handling)
- [잡 배치](#job-batching)
    - [배치 가능한 잡 정의](#defining-batchable-jobs)
    - [배치 디스패치](#dispatching-batches)
    - [체인과 배치](#chains-and-batches)
    - [배치에 잡 추가하기](#adding-jobs-to-batches)
    - [배치 확인하기](#inspecting-batches)
    - [배치 취소하기](#cancelling-batches)
    - [배치 실패 처리](#batch-failures)
    - [배치 가지치기(Pruning)](#pruning-batches)
    - [DynamoDB에 배치 저장하기](#storing-batches-in-dynamodb)
- [클로저 큐잉](#queueing-closures)
- [큐 워커 실행](#running-the-queue-worker)
    - [`queue:work` 명령어](#the-queue-work-command)
    - [큐 우선순위 설정](#queue-priorities)
    - [큐 워커와 배포](#queue-workers-and-deployment)
    - [잡 만료 및 타임아웃](#job-expirations-and-timeouts)
- [Supervisor 설정](#supervisor-configuration)
- [실패한 잡 처리](#dealing-with-failed-jobs)
    - [실패한 잡 정리](#cleaning-up-after-failed-jobs)
    - [실패 잡 재시도](#retrying-failed-jobs)
    - [누락된 모델 무시](#ignoring-missing-models)
    - [실패한 잡 가지치기](#pruning-failed-jobs)
    - [DynamoDB에 실패 잡 저장하기](#storing-failed-jobs-in-dynamodb)
    - [실패한 잡 저장 비활성화](#disabling-failed-job-storage)
    - [실패한 잡 이벤트](#failed-job-events)
- [큐에서 잡 삭제](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [일부 잡 가짜로 만들기](#faking-a-subset-of-jobs)
    - [잡 체인 테스트](#testing-job-chains)
    - [잡 배치 테스트](#testing-job-batches)
    - [잡/큐 상호작용 테스트](#testing-job-queue-interactions)
- [잡 이벤트](#job-events)

<a name="introduction"></a>
## 소개

웹 애플리케이션을 개발하다 보면, 업로드된 CSV 파일을 파싱하고 저장하는 작업과 같이 일반적인 웹 요청 처리 중에는 시간이 오래 걸리는 작업이 있을 수 있습니다. 다행히도 라라벨은 백그라운드에서 처리할 수 있는 대기열(큐)에 잡을 쉽게 생성할 수 있도록 지원합니다. 이렇게 시간이 많이 소요되는 작업을 큐에 넘겨 처리하면, 애플리케이션이 웹 요청에 훨씬 빠르게 응답할 수 있어 사용자 경험이 한층 더 향상됩니다.

라라벨 큐는 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 또는 관계형 데이터베이스와 같은 다양한 큐 백엔드에서, 일관된 큐 API를 제공합니다.

라라벨의 큐 설정 옵션은 애플리케이션의 `config/queue.php` 설정 파일에 저장되어 있습니다. 이 파일에서는 프레임워크에 포함된 각 큐 드라이버에 대한 커넥션 설정(데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 드라이버 등)뿐만 아니라, 잡을 즉시 실행하는 동기식 드라이버(로컬 개발용), 그리고 잡을 모두 무시하는 `null` 큐 드라이버도 확인할 수 있습니다.

> [!NOTE]
> 라라벨은 이제 Redis 기반 큐를 위한 아름다운 대시보드 및 구성 시스템인 Horizon을 제공합니다. 자세한 내용은 [Horizon 공식 문서](/docs/12.x/horizon)를 참고하세요.

<a name="connections-vs-queues"></a>
### 커넥션과 큐의 차이

라라벨 큐를 본격적으로 사용하기 전에, "커넥션(connection)"과 "큐(queue)"의 차이를 이해하는 것이 중요합니다. `config/queue.php` 설정 파일에는 `connections`라는 설정 배열이 있습니다. 이 옵션은 Amazon SQS, Beanstalk, Redis 등 백엔드 큐 서비스들과의 커넥션을 정의합니다. 하지만, 하나의 큐 커넥션 안에 여러 개의 "큐"를 둘 수 있으며, 각각은 단순히 잡을 쌓아두는 여러 개의 스택(Stack)처럼 생각할 수 있습니다.

각 커넥션 설정 예시에는 `queue`라는 속성이 있는데, 이는 잡이 특정 커넥션으로 디스패치(전송)될 때 기본적으로 사용할 큐를 의미합니다. 즉, 특정 큐를 지정하지 않고 잡을 디스패치하면, 해당 커넥션의 `queue` 속성에 지정된 큐로 잡이 쌓입니다:

```php
use App\Jobs\ProcessPodcast;

// 이 잡은 기본 커넥션의 기본 큐로 전송됩니다...
ProcessPodcast::dispatch();

// 이 잡은 기본 커넥션의 "emails" 큐로 전송됩니다...
ProcessPodcast::dispatch()->onQueue('emails');
```

모든 애플리케이션이 여러 큐를 사용할 필요는 없습니다. 단순한 큐 하나만으로 충분한 경우도 많습니다. 하지만 여러 큐에 잡을 분산해서 쌓는 기능은, 잡 처리 우선순위나 분리 처리가 필요한 경우 특히 유용합니다. 라라벨 큐 워커에서는 어떤 큐를 어떤 순서대로 처리할지 직접 지정할 수 있기 때문입니다. 예를 들어, `high`라는 우선순위 큐에 잡을 전송하면, 해당 큐를 먼저 처리하는 워커를 별도로 띄워 높은 우선순위로 처리할 수 있습니다.

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버별 안내 및 필요 사항

<a name="database"></a>
#### 데이터베이스

`database` 큐 드라이버를 사용하려면, 잡을 저장할 수 있는 데이터베이스 테이블이 필요합니다. 일반적으로 라라벨의 기본 `0001_01_01_000002_create_jobs_table.php` [데이터베이스 마이그레이션](/docs/12.x/migrations)에 포함되어 있지만, 애플리케이션에 해당 마이그레이션이 없는 경우 다음의 `make:queue-table` Artisan 명령어로 생성할 수 있습니다:

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면, 먼저 `config/database.php` 설정 파일에 Redis 데이터베이스 커넥션을 설정해야 합니다.

> [!WARNING]
> `serializer` 및 `compression` Redis 옵션은 `redis` 큐 드라이버에서 지원되지 않습니다.

**Redis 클러스터(Cluster) 사용 시**

Redis 큐 커넥션에서 Redis 클러스터를 사용하는 경우, 큐 이름에 반드시 [키 해시 태그(key hash tag)](https://redis.io/docs/reference/cluster-spec/#hash-tags)를 포함해야 합니다. 그래야 하나의 큐에 해당하는 Redis 키들이 모두 동일한 해시 슬롯에 담깁니다.

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

**Blocking(대기) 설정**

Redis 큐를 사용할 때, `block_for` 설정 옵션을 통해 워커가 잡이 활성화될 때까지 얼마나 대기할지 지정할 수 있습니다. 이후 워커 루프를 반복하며 Redis에서 새 잡을 다시 확인하게 됩니다.

큐 부하에 맞게 이 값을 조절하면, 새로운 잡을 위해 Redis를 계속해서 조회(polling)하는 것보다 더 효율적으로 운영할 수 있습니다. 예를 들어, 5초 동안 대기하도록 설정하면, 워커는 잡이 도착할 때까지 최대 5초간 대기하게 됩니다.

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
> `block_for` 값을 `0`으로 설정하면, 잡이 활성화될 때까지 워커가 무한정 대기합니다. 이 경우, 다음 잡이 처리되기 전까지는 `SIGTERM`과 같은 신호가 전달되지 않습니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 필요 사항

아래 큐 드라이버를 사용하려면 다음의 의존 패키지가 필요합니다. 의존성 패키지는 Composer 패키지 매니저로 설치할 수 있습니다.

<div class="content-list" markdown="1">

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~2.0` 또는 phpredis PHP 확장
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`

</div>

<a name="creating-jobs"></a>
## 잡(Job) 생성

<a name="generating-job-classes"></a>
### 잡 클래스 생성하기

기본적으로, 애플리케이션의 큐에 사용할 잡 클래스는 모두 `app/Jobs` 디렉터리에 위치합니다. 만약 `app/Jobs` 디렉터리가 없다면, `make:job` Artisan 명령어를 실행할 때 자동으로 생성됩니다.

```shell
php artisan make:job ProcessPodcast
```

생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하고 있어서, 이 잡이 큐에 비동기적으로 쌓여야 함을 라라벨에 알려줍니다.

> [!NOTE]
> 잡 스텁(stub)은 [스텁 퍼블리싱](/docs/12.x/artisan#stub-customization) 기능을 통해 커스터마이즈할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조

잡 클래스는 일반적으로 매우 간단하며, 큐에서 잡이 처리될 때 호출되는 `handle` 메서드만을 포함합니다. 예시로, 팟캐스트 발행 서비스에서 업로드된 팟캐스트 파일을 처리하는 잡 클래스를 살펴봅니다.

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
     * 잡 실행
     */
    public function handle(AudioProcessor $processor): void
    {
        // 업로드된 팟캐스트 파일 처리...
    }
}
```

이 예시에서 볼 수 있듯이, [Eloquent 모델](/docs/12.x/eloquent) 객체를 잡 생성자에 직접 전달할 수 있습니다. 잡 클래스에 `Queueable` 트레이트를 추가하면, Eloquent 모델과 이미 로드된 연관관계가 큐에 직렬화 및 역직렬화되는 과정이 매끄럽게 처리됩니다.

큐에 쌓이는 잡이 Eloquent 모델을 생성자로 받을 경우, 모델의 식별자(Primary Key)만이 큐에 직렬화되어 저장됩니다. 잡이 실제로 처리될 때, 큐 시스템이 해당 모델 인스턴스와 로딩되어 있던 연관관계를 데이터베이스에서 다시 조회합니다. 이 방식 덕분에 큐 드라이버로 전송되는 잡의 페이로드(payload) 크기가 훨씬 작아집니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드 의존성 주입

큐에서 잡을 실제로 처리할 때 `handle` 메서드가 호출됩니다. `handle` 메서드의 인자에 타입힌트를 지정하면, 라라벨 [서비스 컨테이너](/docs/12.x/container)가 자동으로 해당 의존성을 주입해 줍니다.

컨테이너가 `handle` 메서드의 의존성을 주입하는 방식을 완전히 직접 제어하고 싶다면, 컨테이너의 `bindMethod` 메서드를 사용할 수 있습니다. 이 메서드는 잡과 컨테이너를 인자로 받는 콜백을 등록하며, 콜백 안에서 자유롭게 `handle` 메서드를 호출할 수 있습니다. 보통은 이 코드를 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 사용할 수 있습니다.

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 이미지와 같은 바이너리 데이터는 큐에 잡으로 전달하기 전에 반드시 `base64_encode` 함수를 통해 인코딩해야 합니다. 그렇지 않으면, 잡이 큐에 쌓일 때 JSON 직렬화가 제대로 이루어지지 않을 수 있습니다.

<a name="handling-relationships"></a>
#### 큐에 올라가는 연관관계(Queued Relationships)

큐에 올라가는 잡이 Eloquent 모델의 연관관계를 이미 로딩했다면, 이 관계 정보 역시 함께 직렬화됩니다. 이로 인해 경우에 따라 직렬화된 잡 문자열이 꽤 커질 수 있습니다. 또한, 잡이 언직렬화되어 데이터베이스에서 관계를 다시 조회할 때 관계의 모든 데이터가 한 번에 조회되며, 잡을 큐에 쌓기 전에 모델에 걸었던 쿼리 제한 조건은 적용되지 않습니다. 따라서 일부 연관 데이터만 필요하다면, 큐에 올라간 잡 안에서 그 관계에 다시 쿼리 제한을 걸어야 합니다.

아니면, 관계 정보 자체를 직렬화에 포함하지 않고 싶다면, 모델 객체에 값을 지정할 때 `withoutRelations` 메서드를 사용하세요. 이 메서드는 이미 로딩된 연관관계가 없는 모델 인스턴스를 반환합니다.

```php
/**
 * 새 잡 인스턴스를 생성합니다.
 */
public function __construct(
    Podcast $podcast,
) {
    $this->podcast = $podcast->withoutRelations();
}
```

PHP의 생성자 프로퍼티 프로모션(Constructor Property Promotion)을 사용할 때, Eloquent 모델이 직렬화될 때 연관관계 정보가 포함되지 않게 하고 싶다면, `WithoutRelations` 속성(attribute)을 사용할 수 있습니다.

```php
use Illuminate\Queue\Attributes\WithoutRelations;

/**
 * 새 잡 인스턴스를 생성합니다.
 */
public function __construct(
    #[WithoutRelations]
    public Podcast $podcast,
) {}
```

만약 잡이 단일 모델이 아닌, 컬렉션이나 배열 형태로 여러 모델을 받는다면, 큐에서 잡이 언직렬화되고 실행될 때 이 컬렉션 내 모델들의 관계 정보는 자동 복구되지 않습니다. 이는 수많은 모델을 다루는 잡에서 비효율적인 리소스 사용을 방지하기 위한 동작입니다.

<a name="unique-jobs"></a>
### 유일한 잡(Unique Jobs)

> [!WARNING]
> 유일한 잡 기능을 사용하려면 [락(locks)](/docs/12.x/cache#atomic-locks)을 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 원자적 락을 지원합니다. 또한, 유일 잡 제약은 배치(batch) 내부의 잡에는 적용되지 않습니다.

특정 잡이 한 번에 큐에 오직 하나만 존재하도록 제한하고 싶을 때는, 잡 클래스에 `ShouldBeUnique` 인터페이스를 구현하면 됩니다. 이 인터페이스는 별도의 추가 메서드 구현 없이 바로 사용 가능합니다.

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

위 예시에서, `UpdateSearchIndex` 잡은 유일하게 동작합니다. 즉, 동일한 잡이 이미 큐에 쌓여 있고 아직 처리 중이라면, 새로운 잡은 디스패치되지 않습니다.

경우에 따라, 잡을 유일하게 만드는 "키(key)"를 직접 지정하거나, 얼마 동안만 유일성을 유지할지 타임아웃을 설정하고 싶을 수 있습니다. 이를 위해 잡 클래스에 `uniqueId` 및 `uniqueFor` 프로퍼티 또는 메서드를 정의할 수 있습니다.

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
     * 유일 락이 해제될 때까지의 초(second)
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

이 예시에서는 `UpdateSearchIndex` 잡이 상품 ID 기준으로 유일하게 지정됩니다. 따라서 동일한 상품 ID로 잡을 디스패치하면, 기존에 처리 중인 잡이 끝나기 전까지 새로운 잡은 무시됩니다. 또, 기존 잡이 1시간 내에 처리되지 않을 경우 락이 자동 해제되어, 동일한 유일 키로 다른 잡을 다시 큐에 올릴 수 있습니다.

> [!WARNING]
> 여러 웹 서버나 컨테이너 환경에서 잡을 디스패치한다면, 모든 서버가 동일한 중앙 캐시 서버를 사용하도록 해야 라라벨이 유일 잡 여부를 정확하게 판단할 수 있습니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 잡이 처리 시작 전까지 유일성 유지하기

기본적으로 유일한 잡의 락은 잡이 정상 처리되거나 재시도 횟수를 초과해 실패하면 해제됩니다. 하지만 실질적으로 처리 직전에 락을 해제하고 싶을 때는, 잡이 `ShouldBeUnique` 대신 `ShouldBeUniqueUntilProcessing` 인터페이스를 구현하면 됩니다.

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
#### 유일 잡 락의 동작 방식

내부적으로 `ShouldBeUnique` 잡이 디스패치되면, 라라벨은 `uniqueId` 키로 [락(atomic lock)](/docs/12.x/cache#atomic-locks) 획득을 시도합니다. 락을 획득하지 못하면 잡이 디스패치되지 않습니다. 락은 해당 잡이 정상 처리되거나, 모든 재시도에서 실패하면 해제됩니다. 라라벨은 기본적으로 기본 캐시 드라이버를 사용하여 락을 관리합니다. 만약 락 관리를 다른 캐시 드라이버로 별도로 하고 싶다면, 캐시 드라이버를 반환하는 `uniqueVia` 메서드를 정의할 수 있습니다.

```php
use Illuminate\Contracts\Cache\Repository;
use Illuminate\Support\Facades\Cache;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...

    /**
     * 유일 잡 락에 사용할 캐시 드라이버 반환
     */
    public function uniqueVia(): Repository
    {
        return Cache::driver('redis');
    }
}
```

> [!NOTE]
> 잡의 동시 실행 수 만을 제한하고 싶다면, [WithoutOverlapping](/docs/12.x/queues#preventing-job-overlaps) 잡 미들웨어를 사용하는 것이 더 적합합니다.

<a name="encrypted-jobs"></a>
### 암호화된 잡

라라벨은 잡 데이터의 프라이버시와 무결성을 보장하기 위해 [암호화](/docs/12.x/encryption) 기능을 제공합니다. 사용 방법은, 잡 클래스에 `ShouldBeEncrypted` 인터페이스만 추가하면 됩니다. 이 인터페이스를 추가하면, 라라벨이 잡을 큐에 쌓기 전에 자동으로 데이터를 암호화합니다.

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

잡 미들웨어를 사용하면, 잡 실행 전후에 커스텀 로직을 손쉽게 감쌀 수 있어, 반복적인 코드를 줄이고 잡 내 코드를 깔끔하게 유지할 수 있습니다. 예를 들어, 아래 `handle` 메서드는 라라벨의 Redis 속도 제한 기능을 활용해 5초마다 한 번씩만 잡이 실행되도록 한다고 가정해봅니다.

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

이 코드는 문제가 없다 해도, `handle` 메서드에 Redis 속도 제한 로직이 섞여 코드가 지저분해지고, 같은 로직을 여러 잡에 복사해야 하는 불편이 있습니다.

이럴 때는 `handle` 메서드에서 직접 속도 제한을 하지 말고, 전용 잡 미들웨어를 만들어 처리할 수 있습니다. 라라벨에는 잡 미들웨어를 위한 기본 경로가 없으므로, 애플리케이션 내 원하는 위치에 생성해도 무방합니다. 아래 예시에서는 `app/Jobs/Middleware` 디렉터리에 생성했습니다.

```php
<?php

namespace App\Jobs\Middleware;

use Closure;
use Illuminate\Support\Facades\Redis;

class RateLimited
{
    /**
     * 큐에 올라가는 잡 처리
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

[라우트 미들웨어](/docs/12.x/middleware)와 마찬가지로, 잡 미들웨어도 처리 중인 잡과 계속 처리할 때 호출되는 콜백을 전달받습니다.

추가로, `make:job-middleware` Artisan 명령어를 사용해 잡 미들웨어 클래스를 생성할 수도 있습니다. 이렇게 생성한 미들웨어는 잡 클래스의 `middleware` 메서드에서 배열로 반환하면 해당 잡에 적용할 수 있습니다. 참고로 `make:job` Artisan 명령어로 생성한 잡에는 `middleware` 메서드가 기본적으로 포함되어 있지 않으므로, 직접 추가해야 합니다.

```php
use App\Jobs\Middleware\RateLimited;

/**
 * 잡에 적용할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited];
}
```

> [!NOTE]
> 잡 미들웨어는 [큐잉 이벤트 리스너](/docs/12.x/events#queued-event-listeners), [메일러블](/docs/12.x/mail#queueing-mail), [알림](/docs/12.x/notifications#queueing-notifications) 등에도 사용할 수 있습니다.

<a name="rate-limiting"></a>
### 속도 제한(Rate Limiting)

직접 속도 제한 미들웨어를 작성하는 방법을 살펴보았지만, 라라벨은 이미 사용 가능한 속도 제한 미들웨어도 제공합니다. [라우트 레이트 리미터](/docs/12.x/routing#defining-rate-limiters)와 유사하게, 잡 별 레이트 리미터도 `RateLimiter` 파사드의 `for` 메서드로 정의합니다.

예를 들어, 일반 사용자는 데이터를 1시간에 한 번만 백업할 수 있게 제한하고, 프리미엄 고객은 제한 없이 처리하고 싶다면, `AppServiceProvider`의 `boot` 메서드 안에서 `RateLimiter`를 다음과 같이 정의할 수 있습니다.

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

위 예시에서는 시간 단위 레이트 리미터를 정의했지만, `perMinute` 메서드를 사용해 분 단위로도 손쉽게 제한할 수 있습니다. 또한 `by` 메서드에는 원하는 값을 전달할 수 있으며, 주로 고객별로 제한을 분리할 때 사용합니다.

```php
return Limit::perMinute(50)->by($job->user->id);
```

레이트 리미터를 정의한 뒤에는, `Illuminate\Queue\Middleware\RateLimited` 미들웨어를 사용해 잡에 적용할 수 있습니다. 잡이 레이트 리밋에 걸릴 때마다 해당 미들웨어는 제한시간만큼 잡을 큐에 다시 릴리스(재등록)합니다.

```php
use Illuminate\Queue\Middleware\RateLimited;

/**
 * 잡에 적용할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited('backups')];
}
```

레이트 리미트로 잡이 다시 큐로 릴리스되면, 잡의 `attempts`(시도 횟수)도 증가하니, 잡 클래스의 `tries` 및 `maxExceptions` 값을 상황에 맞게 조절해야 할 수 있습니다. 아니면 [retryUntil 메서드](#time-based-attempts)로 얼마나 오랫동안 재시도할 수 있을지 정의하는 방법도 있습니다.

추가로, `releaseAfter` 메서드를 사용해 잡이 다시 시도되기 전까지 기다릴 초(second)도 지정할 수 있습니다.

```php
/**
 * 잡에 적용할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new RateLimited('backups'))->releaseAfter(60)];
}
```

레이트 리미트에 걸렸을 때 잡을 아예 다시 시도하지 않으려면, `dontRelease` 메서드를 사용할 수 있습니다.

```php
/**
 * 잡에 적용할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new RateLimited('backups'))->dontRelease()];
}
```

> [!NOTE]
> Redis를 사용한다면, Redis에 특화되어 더 효율적으로 동작하는 `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어를 사용할 수 있습니다.

<a name="preventing-job-overlaps"></a>
### 잡 중첩 방지

라라벨은 임의의 키를 기준으로 잡 중첩을 방지할 수 있는 `Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어를 제공합니다. 이 미들웨어는, 예를 들어 하나의 자원을 동시에 여러 잡이 수정하지 못하도록 하고 싶을 때 유용하게 사용할 수 있습니다.

예를 들어 사용자의 신용 점수 업데이트 잡이 동시에 중복 처리되지 않게 하려면, 잡의 `middleware` 메서드에서 `WithoutOverlapping` 미들웨어를 반환하도록 하면 됩니다.

```php
use Illuminate\Queue\Middleware\WithoutOverlapping;

/**
 * 잡에 적용할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new WithoutOverlapping($this->user->id)];
}
```

동일 유형의 중첩 잡은 다시 큐로 릴리스됩니다. 몇 초 후에 릴리스된 잡을 재시도할지 지정하려면 `releaseAfter` 메서드를 사용합니다.

```php
/**
 * 잡에 적용할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->releaseAfter(60)];
}
```

중첩 상태의 잡을 아예 재시도하지 않고 즉시 삭제하려면, `dontRelease` 메서드를 사용합니다.

```php
/**
 * 잡에 적용할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->dontRelease()];
}
```

`WithoutOverlapping` 미들웨어는 라라벨의 원자적 락 기능으로 구현되어 있습니다. 구동 중 잡이 실패하거나 타임아웃 등이 발생해 락이 해제되지 않고 남아 있을 수 있으므로, `expireAfter` 메서드로 명시적인 락 만료 시간을 지정하는 것이 좋습니다. 아래 예시는 잡 실행 시작 후 3분 뒤 락이 풀리도록 설정합니다.

```php
/**
 * 잡에 적용할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->expireAfter(180)];
}
```

> [!WARNING]
> `WithoutOverlapping` 미들웨어는 [락](/docs/12.x/cache#atomic-locks) 기능을 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 원자적 락을 지원합니다.

<a name="sharing-lock-keys"></a>

#### 작업 클래스 간 Lock 키 공유하기

기본적으로 `WithoutOverlapping` 미들웨어는 동일한 클래스의 중복 실행만을 방지합니다. 따라서 서로 다른 두 작업 클래스가 같은 lock 키를 사용하더라도, 이들은 중복 실행을 막지 못합니다. 그러나 `shared` 메서드를 사용하면 라라벨이 이 키를 작업 클래스 간에 적용하도록 지시할 수 있습니다.

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

라라벨은 예외를 제한(Throttling)할 수 있는 `Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어를 제공합니다. 작업이 특정 횟수만큼 예외를 발생시키면, 그 이후의 실행 시도는 지정된 시간만큼 지연됩니다. 이 미들웨어는 특히 불안정한 외부 서비스와 상호작용하는 작업에 유용합니다.

예를 들어, 외부 API와 통신하는 큐 작업이 예외를 연속해서 발생시키는 상황을 가정해 보겠습니다. 예외 제한 기능을 사용하려면, 작업의 `middleware` 메서드에서 `ThrottlesExceptions` 미들웨어를 반환하면 됩니다. 이 미들웨어는 일반적으로 [시간 기반 시도](#time-based-attempts)와 함께 사용해야 합니다.

```php
use DateTime;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 작업이 거쳐야 할 미들웨어를 반환합니다.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new ThrottlesExceptions(10, 5 * 60)];
}

/**
 * 작업의 타임아웃 시점을 결정합니다.
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(30);
}
```

위 코드에서 미들웨어의 첫 번째 인수는 예외가 몇 번 발생하면 제한할지(이 예시에서는 10회), 두 번째 인수는 제한 이후 다시 작업을 시도할 때까지 대기해야 하는 시간(초 단위, 이 예시는 5분)입니다. 즉, 작업이 10번 연속 예외를 던지면 5분 동안 실행이 중지되며, 최대 30분 안에 시도합니다.

작업이 예외를 던졌지만 아직 제한 임계값에 도달하지 않았다면, 작업은 즉시 재시도됩니다. 하지만 미들웨어를 작업에 연결할 때 `backoff` 메서드를 호출하여 재시도까지 지연할 분을 지정할 수도 있습니다.

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 작업이 거쳐야 할 미들웨어를 반환합니다.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 5 * 60))->backoff(5)];
}
```

이 미들웨어는 내부적으로 라라벨의 캐시 시스템을 활용해 속도 제한을 구현하며, 작업의 클래스명이 캐시 "키"로 사용됩니다. 여러 작업이 같은 외부 서비스와 상호작용하고, 이들이 동일한 제한 "버킷"을 공유하도록 하려면, 미들웨어에 `by` 메서드를 사용해 키를 지정할 수 있습니다.

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 작업이 거쳐야 할 미들웨어를 반환합니다.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->by('key')];
}
```

기본적으로 이 미들웨어는 모든 예외에 대해 제한을 적용합니다. 그러나 미들웨어를 작업에 연결할 때 `when` 메서드를 사용해 특정 상황에서만 제한을 적용하도록 변경할 수 있습니다. 이때 제공하는 클로저가 `true`를 반환하면 해당 예외에만 제한이 걸립니다.

```php
use Illuminate\Http\Client\HttpClientException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 작업이 거쳐야 할 미들웨어를 반환합니다.
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

`when` 메서드와 달리, `deleteWhen` 메서드는 특정 예외가 발생할 때 해당 작업을 큐에서 완전히 삭제하도록 사용할 수 있습니다.

```php
use App\Exceptions\CustomerDeletedException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 작업이 거쳐야 할 미들웨어를 반환합니다.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(2, 10 * 60))->deleteWhen(CustomerDeletedException::class)];
}
```

제한된 예외를 애플리케이션의 예외 핸들러로 리포트하고 싶다면, 미들웨어를 연결할 때 `report` 메서드를 사용할 수 있습니다. 선택적으로 클로저를 전달하면, 해당 클로저가 `true`를 반환하는 경우에만 리포트됩니다.

```php
use Illuminate\Http\Client\HttpClientException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 작업이 거쳐야 할 미들웨어를 반환합니다.
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
> Redis를 사용 중이라면, Redis에 최적화되어 있고 더 효율적인 `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어를 사용할 수 있습니다.

<a name="skipping-jobs"></a>
### 작업 건너뛰기(Skipping Jobs)

`Skip` 미들웨어를 사용하면 작업 로직 자체를 수정하지 않고도 작업을 건너뛰거나 삭제할 수 있습니다. `Skip::when` 메서드는 조건이 `true`일 때 작업을 삭제하고, `Skip::unless` 메서드는 조건이 `false`일 때 작업을 삭제합니다.

```php
use Illuminate\Queue\Middleware\Skip;

/**
 * 작업이 거쳐야 할 미들웨어를 반환합니다.
 */
public function middleware(): array
{
    return [
        Skip::when($someCondition),
    ];
}
```

더 복잡한 조건 판단이 필요한 경우, `when`과 `unless` 메서드에 `Closure`(익명 함수)를 전달할 수도 있습니다.

```php
use Illuminate\Queue\Middleware\Skip;

/**
 * 작업이 거쳐야 할 미들웨어를 반환합니다.
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

작업 클래스를 작성했다면, 해당 작업 클래스의 `dispatch` 메서드를 호출해 작업을 디스패치할 수 있습니다. `dispatch` 메서드에 전달한 인수들은 작업 클래스의 생성자로 전달됩니다.

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
     * 새 팟캐스트 저장하기.
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

새 라라벨 애플리케이션에서는 `sync` 드라이버가 기본 큐 드라이버입니다. 이 드라이버는 작업을 현재 요청의 포그라운드에서 동기적으로 실행하므로, 로컬 개발 시 유용합니다. 백그라운드 작업 큐 처리를 실제로 사용하려면 애플리케이션의 `config/queue.php` 설정 파일에서 다른 큐 드라이버를 지정하면 됩니다.

<a name="delayed-dispatching"></a>
### 지연 디스패치(Delayed Dispatching)

작업이 즉시 큐 워커에 의해 처리되지 않고 일정 시간 이후에 처리되길 원한다면, 작업 디스패치 시 `delay` 메서드를 사용할 수 있습니다. 예를 들어, 작업이 디스패치되고 10분 후에만 처리 가능하도록 하려면 다음과 같이 작성할 수 있습니다.

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
     * 새 팟캐스트 저장하기.
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

경우에 따라 작업에 기본 지연(delay)이 설정되어 있을 수 있습니다. 이 지연을 무시하고 즉시 작업을 처리하고 싶다면 `withoutDelay` 메서드를 사용할 수 있습니다.

```php
ProcessPodcast::dispatch($podcast)->withoutDelay();
```

> [!WARNING]
> Amazon SQS 큐 서비스는 최대 지연 시간을 15분으로 제한합니다.

<a name="dispatching-after-the-response-is-sent-to-browser"></a>
#### 응답 전송 후 작업 디스패치

또한, `dispatchAfterResponse` 메서드를 사용하면 웹 서버가 FastCGI를 사용 중일 때 HTTP 응답을 사용자 브라우저에 전송한 후 작업이 디스패치되도록 할 수 있습니다. 이를 통해 큐 작업이 실행되는 도중이라도 사용자는 바로 애플리케이션을 사용할 수 있습니다. 일반적으로 이메일 전송처럼 1초 내외로 짧게 걸리는 작업에만 이 기능을 사용하는 것이 좋습니다. 이 방식으로 실행된 작업은 현재 HTTP 요청 내에서 처리되므로 별도의 큐 워커가 실행 중일 필요가 없습니다.

```php
use App\Jobs\SendNotification;

SendNotification::dispatchAfterResponse();
```

또한 클로저를 `dispatch`할 때 `afterResponse` 메서드를 체이닝하면, 브라우저에 HTTP 응답이 보내진 후 클로저가 실행됩니다.

```php
use App\Mail\WelcomeMessage;
use Illuminate\Support\Facades\Mail;

dispatch(function () {
    Mail::to('taylor@example.com')->send(new WelcomeMessage);
})->afterResponse();
```

<a name="synchronous-dispatching"></a>
### 동기 디스패치(Synchronous Dispatching)

작업을 즉시(동기적으로) 실행하고 싶다면 `dispatchSync` 메서드를 사용하면 됩니다. 이 메서드를 사용하면 작업이 큐에 등록되지 않고 현재 프로세스에서 바로 실행됩니다.

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
     * 새 팟캐스트 저장하기.
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
### 작업과 데이터베이스 트랜잭션

데이터베이스 트랜잭션 내부에서 작업을 디스패치해도 문제는 없지만, 작업이 제대로 실행될 수 있도록 몇 가지를 유의해야 합니다. 트랜잭션 내에서 작업을 디스패치하는 경우, 트랜잭션이 커밋되기 전에 워커가 먼저 작업을 처리할 수 있습니다. 이러한 상황이 발생하면, 트랜잭션 중 업데이트된 모델이나 데이터베이스 레코드가 아직 데이터베이스에 반영되지 않았을 수 있고, 트랜잭션 내에서 생성된 레코드 역시 존재하지 않을 수 있습니다.

다행히 라라벨에서는 이 문제를 해결할 수 있는 여러 방법을 제공합니다. 먼저, 큐 커넥션의 설정 배열에서 `after_commit` 옵션을 설정할 수 있습니다.

```php
'redis' => [
    'driver' => 'redis',
    // ...
    'after_commit' => true,
],
```

`after_commit` 옵션이 `true`로 설정되어 있으면, 트랜잭션 내에서 작업이 디스패치되어도 라라벨은 부모 데이터베이스 트랜잭션이 모두 커밋될 때까지 실제 작업 디스패치를 지연합니다. 물론 트랜잭션이 없으면 즉시 디스패치됩니다.

트랜잭션 중 예외로 인해 롤백이 발생하면, 해당 트랜잭션에서 디스패치된 작업들은 모두 폐기(discard)됩니다.

> [!NOTE]
> `after_commit` 설정을 `true`로 하면, 큐잉된 이벤트 리스너, 메일, 알림, 브로드캐스트 이벤트 또한 모든 데이터베이스 트랜잭션 커밋 이후에 디스패치됩니다.

<a name="specifying-commit-dispatch-behavior-inline"></a>
#### 커밋 후 디스패치 여부를 코드로 지정하기

`after_commit` 큐 커넥션 설정을 `true`로 하지 않은 경우에도, 특정 작업만 트랜잭션 커밋 후 디스패치되도록 직접 지정할 수 있습니다. 이를 위해 작업 디스패치 시 `afterCommit` 메서드를 체이닝하면 됩니다.

```php
use App\Jobs\ProcessPodcast;

ProcessPodcast::dispatch($podcast)->afterCommit();
```

반대로 `after_commit` 설정이 이미 `true`로 되어 있다면, 특정 작업만 현재 열린 트랜잭션 커밋을 기다리지 않고 바로 디스패치하도록 `beforeCommit` 메서드를 사용할 수 있습니다.

```php
ProcessPodcast::dispatch($podcast)->beforeCommit();
```

<a name="job-chaining"></a>
### 작업 체이닝(Job Chaining)

작업 체이닝은, 주 작업이 성공적으로 실행된 후 순차적으로 실행되어야 하는 작업 목록을 지정할 수 있는 기능입니다. 시퀀스 중 하나라도 실패하면 그 이후 작업은 실행되지 않습니다. 큐에 대기 중인 작업 체인을 실행하려면 `Bus` 파사드에서 제공하는 `chain` 메서드를 사용할 수 있습니다. 라라벨의 커맨드 버스(command bus)는 큐 작업 디스패치의 낮은 레벨 컴포넌트입니다.

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

체이닝에는 작업 클래스 인스턴스뿐만 아니라 클로저도 사용할 수 있습니다.

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
> 작업 내에서 `$this->delete()` 메서드로 삭제해도, 체인에 연결된 다음 작업의 실행은 막을 수 없습니다. 체인의 작업이 실패할 때만 잔여 작업이 중단됩니다.

<a name="chain-connection-queue"></a>
#### 체인 연결 및 큐 지정

체인에 사용할 큐 연결 및 큐 이름을 지정하려면 `onConnection`과 `onQueue` 메서드를 사용할 수 있습니다. 이 메서드들은 명시적으로 연결/큐가 지정되지 않았을 때 체인 전체에 동일한 값을 적용합니다.

```php
Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->onConnection('redis')->onQueue('podcasts')->dispatch();
```

<a name="adding-jobs-to-the-chain"></a>
#### 체인에 작업 추가하기

때때로, 체인 내의 다른 작업에서 기존 작업 체인 앞이나 뒤에 작업을 추가해야 할 수도 있습니다. 이럴 때는 `prependToChain` 또는 `appendToChain` 메서드를 사용하면 됩니다.

```php
/**
 * 작업 실행.
 */
public function handle(): void
{
    // ...

    // 현재 체인 앞에 추가, 현재 작업 이후 즉시 실행...
    $this->prependToChain(new TranscribePodcast);

    // 현재 체인 뒤에 추가, 체인 마지막에 실행...
    $this->appendToChain(new TranscribePodcast);
}
```

<a name="chain-failures"></a>
#### 체인 작업 실패 처리

체이닝 작업 중 하나가 실패했을 때 실행할 콜백을 지정하려면 `catch` 메서드를 사용할 수 있습니다. 전달된 콜백에는 작업 실패의 원인이 된 `Throwable` 인스턴스가 주어집니다.

```php
use Illuminate\Support\Facades\Bus;
use Throwable;

Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->catch(function (Throwable $e) {
    // 체인 내 일부 작업이 실패했습니다...
})->dispatch();
```

> [!WARNING]
> 체인 콜백은 직렬화되어 라라벨 큐에서 나중에 실행되므로, 콜백 내부에서 `$this` 변수를 사용하면 안 됩니다.

<a name="customizing-the-queue-and-connection"></a>
### 큐 및 연결 커스터마이징

<a name="dispatching-to-a-particular-queue"></a>
#### 특정 큐로 디스패치하기

작업을 여러 큐에 분산하여 배치하면, 큐 대기열을 "분류"하고 다양한 큐별로 워커 수를 달리 설정하여 우선순위를 줄 수 있습니다. 단, 이는 큐 설정 파일에 정의된 "커넥션"별로 작업을 분리하는 것이 아니라, 하나의 커넥션 내 여러 큐에 분배하는 것입니다. 작업을 특정 큐에 할당하려면 디스패치 시 `onQueue` 메서드를 사용하세요.

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
     * 새 팟캐스트 저장하기.
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

또는, 작업 클래스의 생성자 내부에서 `onQueue` 메서드를 호출하여 큐를 지정할 수도 있습니다.

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    /**
     * 새 작업 인스턴스 생성.
     */
    public function __construct()
    {
        $this->onQueue('processing');
    }
}
```

<a name="dispatching-to-a-particular-connection"></a>
#### 특정 커넥션으로 디스패치하기

애플리케이션이 여러 큐 커넥션을 사용할 경우, `onConnection` 메서드를 사용해 작업을 보낼 커넥션을 지정할 수 있습니다.

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
     * 새 팟캐스트 저장하기.
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

`onConnection`과 `onQueue` 메서드를 체이닝하여 작업의 커넥션과 큐를 모두 지정할 수도 있습니다.

```php
ProcessPodcast::dispatch($podcast)
    ->onConnection('sqs')
    ->onQueue('processing');
```

또는, 작업 클래스 생성자에서 `onConnection` 메서드를 사용해 미리 커넥션을 지정할 수도 있습니다.

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    /**
     * 새 작업 인스턴스 생성.
     */
    public function __construct()
    {
        $this->onConnection('sqs');
    }
}
```

<a name="max-job-attempts-and-timeout"></a>

### 최대 작업 시도 횟수 / 타임아웃 값 지정

<a name="max-attempts"></a>
#### 최대 시도 횟수

큐에 등록된 작업이 오류를 발생시키는 경우, 이를 무한히 재시도하게 두고 싶지는 않을 것입니다. 이를 위해, 라라벨에서는 작업이 최대 몇 번 또는 얼마 동안 시도될 수 있는지 지정하는 다양한 방법을 제공합니다.

작업이 시도될 최대 횟수를 지정하는 한 가지 방법은 아티즌 커맨드 라인에서 `--tries` 스위치를 사용하는 것입니다. 이 값은 워커가 처리하는 모든 작업에 적용되며, 만약 개별 작업에서 시도 횟수를 별도로 지정했다면, 해당 값이 우선 적용됩니다.

```shell
php artisan queue:work --tries=3
```

작업이 최대 시도 횟수를 초과하면, 해당 작업은 "실패"한 것으로 간주됩니다. 실패한 작업 처리 방법에 대한 자세한 내용은 [실패한 작업 문서](#dealing-with-failed-jobs)를 참고하십시오. 만일 `queue:work` 명령어에 `--tries=0`을 지정하면, 작업은 무한정 재시도됩니다.

좀 더 세분화된 방식으로, 작업 클래스 자체에 최대 시도 횟수를 정의할 수도 있습니다. 작업 클래스에서 최대 시도 횟수를 지정하면, 커맨드라인에서 지정한 `--tries` 값보다 우선 적용됩니다.

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

특정 작업의 최대 시도 횟수를 동적으로 제어해야 한다면, 작업 클래스에 `tries` 메서드를 정의할 수 있습니다.

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

작업이 실패하기 전까지 최대 몇 번 시도할지 지정하는 대신, 더 이상 재시도하지 않을 시점을 시간으로 지정할 수도 있습니다. 이 방식은 특정 시간 내에 작업을 여러 번 재시도할 수 있도록 해줍니다. 이를 위해 작업 클래스에 `retryUntil` 메서드를 추가하면 됩니다. 이 메서드는 `DateTime` 인스턴스를 반환해야 합니다.

```php
use DateTime;

/**
 * 작업이 언제까지 타임아웃 되어야 하는지 반환
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(10);
}
```

`retryUntil`과 `tries`가 모두 정의된 경우, 라라벨은 `retryUntil` 메서드를 우선시합니다.

> [!NOTE]
> [큐 처리 이벤트 리스너](/docs/12.x/events#queued-event-listeners)나 [큐 처리 알림](/docs/12.x/notifications#queueing-notifications)에도 `tries` 속성 또는 `retryUntil` 메서드를 정의할 수 있습니다.

<a name="max-exceptions"></a>
#### 최대 예외 수

작업을 여러 번 재시도하고 싶지만, 직접 `release` 메서드를 호출하는 것이 아니라 처리되지 않은 예외가 지정한 횟수만큼 발생하면 실패로 간주하고 싶을 때도 있습니다. 이런 경우, 작업 클래스에 `maxExceptions` 속성을 정의해서 처리할 수 있습니다.

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
     * 작업 실패로 간주되기 전 허용할 최대 처리되지 않은 예외 개수
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
            // Lock을 획득하면 팟캐스트 처리...
        }, function () {
            // Lock을 획득할 수 없음...
            return $this->release(10);
        });
    }
}
```

위 예시에서, 만약 애플리케이션이 Redis 락을 얻지 못하면 작업을 10초 동안 릴리즈하며, 최대 25번 재시도합니다. 그러나 작업 처리 중 세 번 처리가 안 된 예외가 발생하면 작업은 실패로 간주됩니다.

<a name="timeout"></a>
#### 타임아웃

대부분의 경우, 큐 작업이 어느 정도 시간 안에는 완료될 것이라 예상할 수 있습니다. 이런 이유로 라라벨에서는 "타임아웃" 값을 지정할 수 있습니다. 기본적으로 타임아웃 값은 60초이며, 작업이 지정한 초(second)보다 오래 처리되면 해당 작업을 처리하던 워커는 에러와 함께 종료됩니다. 일반적으로 워커는 [서버에 구성된 프로세스 관리자](#supervisor-configuration)가 자동으로 재시작합니다.

작업이 실행될 수 있는 최대 시간을 지정하려면 아티즌 커맨드 라인에서 `--timeout` 스위치를 사용할 수 있습니다.

```shell
php artisan queue:work --timeout=30
```

만약 시간이 초과되어 작업이 최대 시도 횟수까지 계속해서 타임아웃이 발생하면, 해당 작업은 실패로 처리됩니다.

작업 클래스 자체에도 작업이 허용될 최대 실행 시간을 정의할 수 있습니다. 작업 클래스에 정의된 타임아웃 값이 있으면 커맨드라인에서 지정한 값보다 우선 적용됩니다.

```php
<?php

namespace App\Jobs;

class ProcessPodcast implements ShouldQueue
{
    /**
     * 타임아웃 전까지 작업이 실행될 수 있는 최대 초 단위 시간
     *
     * @var int
     */
    public $timeout = 120;
}
```

가끔씩, 소켓이나 외부 HTTP 연결과 같은 IO 블로킹 프로세스는 명시적으로 지정한 타임아웃을 지키지 않을 수 있습니다. 이런 기능을 사용할 때는, 해당 기능의 API를 이용해 타임아웃을 따로 지정하는 것이 좋습니다. 예를 들어 Guzzle을 사용할 때는 연결과 요청 타임아웃 값을 반드시 직접 지정해야 합니다.

> [!WARNING]
> 작업 타임아웃을 사용하려면 PHP의 `pcntl` 확장 모듈이 반드시 설치되어 있어야 합니다. 또한 작업의 "타임아웃" 값은 반드시 ["retry after"](#job-expiration) 값보다 작아야 합니다. 그렇지 않으면, 실제로 작업이 끝나거나 타임아웃되기 전에 재시도가 시작될 수 있습니다.

<a name="failing-on-timeout"></a>
#### 타임아웃 시 실패 처리

작업이 타임아웃될 때 [실패](#dealing-with-failed-jobs)로 간주되도록 하고 싶다면, 작업 클래스에 `$failOnTimeout` 속성을 정의하면 됩니다.

```php
/**
 * 작업이 타임아웃되었을 때 실패로 간주할지 여부
 *
 * @var bool
 */
public $failOnTimeout = true;
```

<a name="error-handling"></a>
### 오류 처리

작업을 처리하는 중에 예외가 발생하면, 해당 작업은 자동으로 큐에 다시 등록되어 재시도됩니다. 이 과정은 작업이 애플리케이션에서 허용하는 최대 시도 횟수에 도달할 때까지 반복됩니다. 최대 시도 횟수는 `queue:work` 아티즌 명령어의 `--tries` 스위치 또는 작업 클래스의 설정으로 정의할 수 있습니다. 큐 워커 실행 방법에 대한 자세한 내용은 [아래에서 확인](#running-the-queue-worker)할 수 있습니다.

<a name="manually-releasing-a-job"></a>
#### 작업을 수동으로 릴리즈하기

경우에 따라 작업을 수동으로 큐에 다시 등록하여 나중에 다시 시도하고 싶을 때가 있습니다. 이럴 때는 `release` 메서드를 호출하면 됩니다.

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

기본적으로 `release` 메서드는 작업을 즉시 다시 큐에 등록합니다. 하지만, 정수나 날짜 인스턴스를 인자로 전달하여, 지정한 시간(초)만큼 대기 후에 작업이 처리될 수 있도록 할 수도 있습니다.

```php
$this->release(10);

$this->release(now()->addSeconds(10));
```

<a name="manually-failing-a-job"></a>
#### 작업을 수동으로 실패 처리하기

가끔은 작업을 "실패"한 것으로 수동으로 처리해야 하는 경우도 있습니다. 이때는 `fail` 메서드를 호출하면 됩니다.

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

예외를 직접 캐치하여 작업을 실패로 처리하고 싶다면, 해당 예외를 `fail` 메서드에 전달할 수 있습니다. 또는, 편의상 오류 메시지 문자열을 전달하면, 라라벨이 예외로 변환하여 처리해줍니다.

```php
$this->fail($exception);

$this->fail('Something went wrong.');
```

> [!NOTE]
> 실패한 작업에 대한 자세한 정보는 [작업 실패 처리 문서](#dealing-with-failed-jobs)를 참고하세요.

<a name="fail-jobs-on-exceptions"></a>
#### 특정 예외 발생 시 작업 실패 처리

`FailOnException` [작업 미들웨어](#job-middleware)는 특정 예외가 발생할 경우 즉시 재시도를 중단하고, 작업을 실패로 처리할 수 있게 해줍니다. 이 기능은 외부 API 에러와 같이 일시적인 예외에 대해서는 재시도를 하고, 사용자의 권한이 회수되는 등 영구적인 예외가 발생하면 작업을 영구적으로 실패 처리하고 싶을 때 유용합니다.

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
     * 새로운 작업 인스턴스 생성
     */
    public function __construct(
        public User $user,
    ) {}

    /**
     * 작업 실행
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
     * 이 작업에 적용할 미들웨어 반환
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
## 작업 배치 (Job Batching)

라라벨의 작업 배치 기능을 사용하면, 복수의 작업을 한 번에 실행하고 모든 작업이 종료된 후 특정 작업을 수행할 수 있습니다. 시작하기 전에, 각 배치의 진행률 등 메타 정보를 저장할 데이터베이스 테이블 생성을 위해 마이그레이션을 생성해야 합니다. 해당 마이그레이션은 `make:queue-batches-table` 아티즌 명령어로 손쉽게 생성할 수 있습니다.

```shell
php artisan make:queue-batches-table

php artisan migrate
```

<a name="defining-batchable-jobs"></a>
### 배치 가능한 작업 정의

배치 가능한 작업을 정의하려면 [일반적인 방식으로 큐 작업을 생성](#creating-jobs)하지만, 작업 클래스에 `Illuminate\Bus\Batchable` 트레이트를 추가해야 합니다. 이 트레이트는 현재 작업이 속해 있는 배치 정보를 반환하는 `batch` 메서드를 사용할 수 있게 해줍니다.

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

        // CSV 파일 일부를 가져오기...
    }
}
```

<a name="dispatching-batches"></a>
### 배치 디스패치하기

작업을 배치로 디스패치하려면 `Bus` 파사드의 `batch` 메서드를 사용하면 됩니다. 일반적으로 배치는 완료 콜백과 함께 사용될 때 가장 효과적입니다. 따라서 `then`, `catch`, `finally` 메서드로 배치가 완료될 때 호출할 콜백을 정의할 수 있습니다. 이 콜백들은 실행 시점에 `Illuminate\Bus\Batch` 인스턴스를 인자로 받습니다. 아래 예시는 여러 CSV 행을 처리하는 작업을 배치로 큐에 등록하는 모습입니다.

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
    // 배치가 생성되었지만 작업은 아직 추가되지 않음...
})->progress(function (Batch $batch) {
    // 하나의 작업이 정상적으로 완료됨...
})->then(function (Batch $batch) {
    // 모든 작업이 정상적으로 완료됨...
})->catch(function (Batch $batch, Throwable $e) {
    // 첫 번째 작업 실패 발생...
})->finally(function (Batch $batch) {
    // 배치가 실행을 마침...
})->dispatch();

return $batch->id;
```

배치의 ID는 `$batch->id` 속성으로 접근할 수 있으며, 추후 [Laravel 커맨드 버스](#inspecting-batches)를 통해 배치에 대한 정보를 조회할 때 사용합니다.

> [!WARNING]
> 배치 콜백은 직렬화된 후 나중에 라라벨 큐에서 실행되므로, 콜백 내부에서 `$this` 변수를 사용해서는 안 됩니다. 또한 배치된 작업은 데이터베이스 트랜잭션으로 감싸져 있으므로, 암묵적으로 커밋을 발생시키는 데이터베이스 쿼리는 작업 내에서 실행하면 안 됩니다.

<a name="naming-batches"></a>
#### 배치에 이름 부여하기

라라벨 Horizon, Telescope 등의 일부 툴에서는 배치에 이름이 부여되어 있을 경우 더 편리한 디버그 정보를 제공할 수 있습니다. 배치에 임의의 이름을 지정하려면 배치 정의 시 `name` 메서드를 호출하면 됩니다.

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // 모든 작업이 정상적으로 완료됨...
})->name('Import CSV')->dispatch();
```

<a name="batch-connection-queue"></a>
#### 배치 연결 및 큐 지정

배치를 처리할 때 사용될 커넥션(Connection)과 큐(Queue)를 지정하고 싶다면 `onConnection` 및 `onQueue` 메서드를 사용할 수 있습니다. 배치 내의 모든 작업은 동일한 커넥션과 큐에서 실행되어야 합니다.

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // 모든 작업이 정상적으로 완료됨...
})->onConnection('redis')->onQueue('imports')->dispatch();
```

<a name="chains-and-batches"></a>
### 체인과 배치

배치 내에 [체이닝된 작업](#job-chaining)을 배열 형태로 정의하여, 여러 체인 작업을 병렬로 실행하고, 모든 작업 체인이 처리 완료된 후 콜백을 실행할 수 있습니다.

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

반대로, [체인](#job-chaining) 내에 배치들을 배치하여 작동시킬 수도 있습니다. 예를 들어, 먼저 여러 팟캐스트를 공개(release)하는 배치를 실행하고, 그 후 공개 알림을 보내는 배치를 실행할 수 있습니다.

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

경우에 따라, 이미 실행 중인 배치 내부에서 추가적인 작업을 배치에 더해야 할 때가 있습니다. 이 방식은 수천 개의 작업을 한 번에 디스패치해야 하지만, 웹 요청 시점에 모두 디스패치하기에는 소요 시간이 너무 길어지는 경우에 유용합니다. 이런 상황에서는, 최초로 일부 "로더(Loader)" 작업만 배치에 등록해두고, 나머지 작업들을 실시간으로 배치에 추가하도록 구성할 수 있습니다.

```php
$batch = Bus::batch([
    new LoadImportBatch,
    new LoadImportBatch,
    new LoadImportBatch,
])->then(function (Batch $batch) {
    // 모든 작업이 정상적으로 완료됨...
})->name('Import Contacts')->dispatch();
```

위 예시에서 `LoadImportBatch` 작업을 이용해 배치에 추가 작업을 더합니다. 이를 위해 작업 클래스에서 `batch` 메서드로 배치 인스턴스를 가져와, `add` 메서드를 사용할 수 있습니다.

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
> 배치에 작업을 추가할 때는 반드시 같은 배치에 속한 작업 안에서만 가능합니다.

<a name="inspecting-batches"></a>
### 배치 조회

배치 완료 콜백에 전달되는 `Illuminate\Bus\Batch` 인스턴스에는, 해당 배치 작업들과 상호작용하고 정보를 조회하는 데 도움이 되는 다양한 속성과 메서드가 있습니다.

```php
// 배치의 UUID...
$batch->id;

// 배치의 이름(지정된 경우)...
$batch->name;

// 배치에 할당된 작업 수
$batch->totalJobs;

// 아직 큐에서 처리되지 않은 작업 수
$batch->pendingJobs;

// 실패한 작업 수
$batch->failedJobs;

// 지금까지 처리된 작업 수
$batch->processedJobs();

// 배치의 완료율(0~100)
$batch->progress();

// 배치 실행이 끝났는지 여부
$batch->finished();

// 배치 실행 취소
$batch->cancel();

// 배치가 취소되었는지 여부
$batch->cancelled();
```

<a name="returning-batches-from-routes"></a>
#### 라우트에서 배치 정보 반환하기

모든 `Illuminate\Bus\Batch` 인스턴스는 JSON 직렬화가 가능하므로, 애플리케이션의 라우트에서 해당 인스턴스를 직접 반환해 배치에 관한 정보를 JSON 형태로 얻을 수 있습니다. 이를 이용하면, 애플리케이션의 UI에서 배치의 완료 진행률 등을 쉽게 표시할 수 있습니다.

배치를 ID로 조회하려면, `Bus` 파사드의 `findBatch` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Support\Facades\Bus;
use Illuminate\Support\Facades\Route;

Route::get('/batch/{batchId}', function (string $batchId) {
    return Bus::findBatch($batchId);
});
```

<a name="cancelling-batches"></a>
### 배치 취소

특정 배치의 실행을 중단하고 싶을 때는, 해당 `Illuminate\Bus\Batch` 인스턴스에서 `cancel` 메서드를 호출하면 됩니다.

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

앞선 예시들에서도 볼 수 있듯이, 배치 작업은 계속 실행을 진행하기 전에 자신이 속한 배치가 취소되었는지 확인하는 것이 일반적입니다. 하지만 편의상, 이 역할을 대신해주는 `SkipIfBatchCancelled` [미들웨어](#job-middleware)를 작업에 지정할 수도 있습니다. 이 미들웨어는 배치가 이미 취소된 상태라면 해당 작업이 처리되지 않도록 라라벨에 지시합니다.

```php
use Illuminate\Queue\Middleware\SkipIfBatchCancelled;

/**
 * 이 작업에 적용할 미들웨어 반환
 */
public function middleware(): array
{
    return [new SkipIfBatchCancelled];
}
```

<a name="batch-failures"></a>
### 배치 실패

배치에 포함된 작업이 실패할 경우, `catch` 콜백(지정된 경우)이 호출됩니다. 이 콜백은 배치 내에서 처음으로 실패한 작업에만 한 번 호출됩니다.

<a name="allowing-failures"></a>

#### 실패 허용

배치 내의 하나의 작업이 실패하면, 라라벨은 해당 배치를 자동으로 "취소됨" 상태로 표시합니다. 만약 여러분이 이 동작을 원하지 않는 경우, 작업이 실패해도 배치가 자동으로 취소되지 않도록 설정할 수 있습니다. 이는 배치를 디스패치할 때 `allowFailures` 메서드를 호출하여 설정할 수 있습니다.

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // 모든 작업이 성공적으로 완료됨...
})->allowFailures()->dispatch();
```

<a name="retrying-failed-batch-jobs"></a>
#### 실패한 배치 작업 재시도

라라벨은 특정 배치에서 실패한 모든 작업을 쉽고 편리하게 재시도할 수 있도록 `queue:retry-batch` Artisan 명령어를 제공합니다. `queue:retry-batch` 명령어는 재시도하려는 배치의 UUID를 인자로 받습니다.

```shell
php artisan queue:retry-batch 32dbc76c-4f82-4749-b610-a639fe0099b5
```

<a name="pruning-batches"></a>
### 배치 레코드 정리(Pruning)

정리 작업 없이 두면, `job_batches` 테이블에는 레코드가 빠르게 쌓일 수 있습니다. 이를 방지하기 위해, [스케줄링](/docs/12.x/scheduling)을 통해 `queue:prune-batches` Artisan 명령어가 매일 실행되도록 예약하는 것이 좋습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches')->daily();
```

기본적으로, 24시간이 지난 모든 완료된 배치가 정리됩니다. 명령어 실행 시 `hours` 옵션을 지정하여 배치 데이터를 얼마나 오래 보관할지 결정할 수 있습니다. 다음 예시는 48시간 이상 경과한 모든 배치를 삭제합니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48')->daily();
```

때때로 `jobs_batches` 테이블에, 작업이 중간에 실패하거나 성공적으로 재시도되지 않은 배치 등, 완료되지 않은 배치 레코드가 쌓일 수 있습니다. `queue:prune-batches` 명령어에 `unfinished` 옵션을 지정하여 이런 미완료된 배치 레코드를 정리할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48 --unfinished=72')->daily();
```

마찬가지로, 취소된 배치 레코드가 `jobs_batches` 테이블에 쌓일 수도 있습니다. `queue:prune-batches` 명령어에 `cancelled` 옵션을 지정하면 이러한 취소된 배치 레코드도 정리할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48 --cancelled=72')->daily();
```

<a name="storing-batches-in-dynamodb"></a>
### 배치 메타데이터를 DynamoDB에 저장

라라벨은 배치의 메타 정보를 [DynamoDB](https://aws.amazon.com/dynamodb)에 저장하는 것도 지원합니다. 다만, 모든 배치 레코드를 저장할 DynamoDB 테이블을 직접 만들어야 합니다.

일반적으로 이 테이블의 이름은 `job_batches`로 하는 것이 좋지만, 애플리케이션의 `queue` 설정 파일에 있는 `queue.batching.table` 설정 값을 기준으로 테이블 이름을 정해야 합니다.

<a name="dynamodb-batch-table-configuration"></a>
#### DynamoDB 배치 테이블 설정

`job_batches` 테이블에는 문자열 타입의 파티션(primary partition) 키로 `application`, 정렬(primary sort) 키로 `id`가 있어야 합니다. `application` 키에는 애플리케이션의 `app` 설정 파일 내 `name` 설정 값이 들어갑니다. 애플리케이션 이름이 DynamoDB 테이블 키의 일부이므로, 여러 라라벨 애플리케이션의 작업 배치를 같은 테이블에 저장할 수 있습니다.

또한 [자동 배치 정리 기능](#pruning-batches-in-dynamodb)을 활용하려면, 테이블에 `ttl` 속성(attribute)을 추가할 수도 있습니다.

<a name="dynamodb-configuration"></a>
#### DynamoDB 설정

다음으로, 라라벨 애플리케이션이 Amazon DynamoDB와 통신할 수 있도록 AWS SDK를 설치합니다.

```shell
composer require aws/aws-sdk-php
```

이후 `queue.batching.driver` 설정 값을 `dynamodb`로 지정해야 합니다. 그리고 `batching` 설정 배열 내에 `key`, `secret`, `region` 옵션도 정의해야 하며, 이 값들은 AWS 인증에 사용됩니다. `dynamodb` 드라이버 사용 시에는 `queue.batching.database` 설정 옵션이 불필요합니다.

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

[Amazon DynamoDB](https://aws.amazon.com/dynamodb)에 작업 배치 정보를 저장할 경우, 관계형 데이터베이스용 일반 정리 명령어로는 배치를 정리할 수 없습니다. 대신, [DynamoDB의 기본 TTL(Time To Live) 기능](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html)을 이용해 오래된 배치 레코드를 자동 삭제할 수 있습니다.

테이블에 `ttl` 속성을 정의한 경우, 라라벨이 배치 레코드 정리 기준을 알 수 있도록 설정 항목을 추가로 지정할 수 있습니다. `queue.batching.ttl_attribute` 값은 TTL을 저장하는 속성 이름을 지정하며, `queue.batching.ttl` 값은 레코드가 최종 업데이트된 시점을 기준으로 삭제까지 대기할 초(second) 단위의 시간을 지정합니다.

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
## 클로저(Closure)를 큐에 올리기

작업 클래스 대신 클로저(Closure)를 큐에 올릴 수도 있습니다. 간단하고 빠른 작업을 현재 요청 처리 흐름과 분리하여 비동기로 실행하고자 할 때 유용합니다. 클로저를 큐에 올릴 때 클로저의 코드 내용은 암호화 서명되어 전송 도중 변조될 수 없도록 보호됩니다.

```php
$podcast = App\Podcast::find(1);

dispatch(function () use ($podcast) {
    $podcast->publish();
});
```

큐에 올린 클로저에 이름을 지정하여, 큐 리포트 대시보드나 `queue:work` 명령어에서 클로저 이름이 표시되도록 하려면 `name` 메서드를 사용할 수 있습니다.

```php
dispatch(function () {
    // ...
})->name('Publish Podcast');
```

또한, `catch` 메서드를 사용하면 큐에 올린 클로저가 모든 [설정된 재시도 횟수](#max-job-attempts-and-timeout)를 소진하고도 정상적으로 실행되지 못했을 때 실행할 처리를 클로저로 지정할 수 있습니다.

```php
use Throwable;

dispatch(function () use ($podcast) {
    $podcast->publish();
})->catch(function (Throwable $e) {
    // 이 작업은 실패하였습니다...
});
```

> [!WARNING]
> `catch` 콜백은 라라벨 큐에서 직렬화되었다가 나중에 실행됩니다. 따라서 `catch` 콜백 내부에서는 `$this` 변수를 사용하면 안 됩니다.

<a name="running-the-queue-worker"></a>
## 큐 워커 실행하기

<a name="the-queue-work-command"></a>
### `queue:work` 명령어

라라벨은 큐에 작업이 추가될 때마다 작업을 가져와 실행할 큐 워커를 시작할 수 있도록 Artisan 명령어를 제공합니다. `queue:work` 명령어로 워커를 실행할 수 있습니다. 한 번 실행하면 수동으로 중단하거나 터미널을 종료하기 전까지 계속 동작합니다.

```shell
php artisan queue:work
```

> [!NOTE]
> `queue:work` 프로세스를 항상 백그라운드에서 실행하려면, [Supervisor](#supervisor-configuration)와 같은 프로세스 모니터를 사용하여 큐 워커가 멈추지 않고 계속 동작하도록 설정해야 합니다.

만약 작업의 ID, 연결명, 큐 이름 등의 세부 정보를 출력에서 함께 보고 싶다면, `-v` 플래그를 명령어에 추가할 수 있습니다.

```shell
php artisan queue:work -v
```

큐 워커는 한 번 실행하면 메모리에 부팅된 애플리케이션 상태를 계속 유지하며 장시간 동작합니다. 따라서 워커가 시작된 이후 코드의 변경사항은 감지하지 못합니다. 그러므로 애플리케이션 배포 시 꼭 [큐 워커 리스타트](#queue-workers-and-deployment) 작업을 해주셔야 합니다. 또, 애플리케이션에서 생성되거나 변경된 정적(static) 상태는 작업별로 자동 초기화되지 않는다는 점을 주의하세요.

또한, `queue:listen` 명령어를 사용할 수도 있습니다. 이 명령어는 코드 변경 사항이 있다면 워커를 직접 재시작하지 않아도 수정된 코드를 자동으로 반영하고, 애플리케이션 상태도 자동 리셋됩니다. 다만, `queue:work` 명령어보다 비효율적이므로 주의해야 합니다.

```shell
php artisan queue:listen
```

<a name="running-multiple-queue-workers"></a>
#### 여러 큐 워커 실행하기

하나의 큐에 여러 워커를 할당하여 작업을 동시에 실행하고 싶다면, 단순히 여러 개의 `queue:work` 프로세스를 실행하면 됩니다. 이는 개발 환경에서는 터미널의 다른 탭에서, 운영환경에서는 프로세스 매니저(예: Supervisor) 설정으로 관리할 수 있습니다. [Supervisor 사용 시](#supervisor-configuration), `numprocs` 설정 값을 활용합니다.

<a name="specifying-the-connection-queue"></a>
#### 워커의 연결 및 큐 지정

워커가 사용할 큐 연결명을 명시적으로 지정할 수도 있습니다. 이때 이름은 `config/queue.php` 설정 파일에서 정의된 연결명 중 하나여야 합니다.

```shell
php artisan queue:work redis
```

기본적으로 `queue:work` 명령어는 지정한 연결의 기본 큐 작업만 처리합니다. 하지만, 특정 지정 큐만 처리하도록 하여 워커를 더욱 세밀하게 설정할 수 있습니다. 예를 들어, 이메일 작업을 `redis` 연결의 `emails` 큐에만 넣어두었다면 아래와 같이 실행할 수 있습니다.

```shell
php artisan queue:work redis --queue=emails
```

<a name="processing-a-specified-number-of-jobs"></a>
#### 정해진 개수의 작업만 처리하기

`--once` 옵션을 지정하면 워커가 큐에서 작업 하나만 처리한 뒤 종료됩니다.

```shell
php artisan queue:work --once
```

`--max-jobs` 옵션으로 워커가 일정 개수의 작업을 처리한 뒤 종료하도록 지정할 수도 있습니다. 이는 [Supervisor](#supervisor-configuration)와 함께 사용하여 워커가 많은 작업을 처리하면서 쌓인 메모리를 주기적으로 해제하도록 할 때 유용합니다.

```shell
php artisan queue:work --max-jobs=1000
```

<a name="processing-all-queued-jobs-then-exiting"></a>
#### 큐에 쌓인 모든 작업을 처리한 후 종료하기

`--stop-when-empty` 옵션은 큐에 대기 중인 모든 작업을 처리한 후 워커를 정상적으로 종료시킵니다. 이 옵션은 도커 컨테이너에서 라라벨 큐를 처리할 때, 큐가 모두 비워지면 컨테이너를 종료하고 싶을 때 활용할 수 있습니다.

```shell
php artisan queue:work --stop-when-empty
```

<a name="processing-jobs-for-a-given-number-of-seconds"></a>
#### 지정된 시간 동안만 작업 처리하기

`--max-time` 옵션은 워커가 주어진 초(second) 동안 작업을 처리하다가 종료하게 합니다. 이 옵션 역시 [Supervisor](#supervisor-configuration)와 결합하여 워커가 일정 시간마다 재시작되도록 할 때 활용할 수 있습니다.

```shell
# 한 시간 동안 작업을 처리한 뒤 종료
php artisan queue:work --max-time=3600
```

<a name="worker-sleep-duration"></a>
#### 워커의 대기(sleep) 시간 설정

큐에 작업이 있을 때는 작업을 쉼 없이 곧바로 처리합니다. 반면, 작업이 없으면 `sleep` 옵션에 지정된 시간(초)만큼 워커가 '잠시 대기'하게 됩니다. 대기 중엔 새로운 작업을 즉시 처리하지 않습니다.

```shell
php artisan queue:work --sleep=3
```

<a name="maintenance-mode-queues"></a>
#### 점검 모드와 큐

애플리케이션이 [점검 모드](/docs/12.x/configuration#maintenance-mode)인 경우, 큐에 올라온 작업은 처리되지 않습니다. 점검 모드 해제 이후에는 정상적으로 작업이 처리됩니다.

점검 모드 상태에서라도 워커가 작업을 처리하게 하려면 `--force` 옵션을 사용할 수 있습니다.

```shell
php artisan queue:work --force
```

<a name="resource-considerations"></a>
#### 리소스 사용 주의점

데몬 큐 워커는 각 작업마다 프레임워크가 '재부팅'되지 않으므로, 메모리 등 무거운 리소스는 각 작업 종료 후 반드시 해제해주어야 합니다. 예를 들어 GD 라이브러리를 사용해 이미지 조작을 했다면, 작업 후에는 `imagedestroy`로 메모리를 반환해야 합니다.

<a name="queue-priorities"></a>
### 큐 우선순위 지정

큐의 처리 우선순위를 부여하고 싶을 때가 있습니다. 예를 들어, `config/queue.php` 파일에서 `redis` 연결의 기본 큐를 `low`로 설정해 두었더라도, 가끔은 특정 작업을 우선 순위가 높은 `high` 큐로 보내고 싶을 수 있습니다.

```php
dispatch((new Job)->onQueue('high'));
```

`high` 큐의 작업을 모두 처리한 후에만 `low` 큐 작업을 처리하도록 하려면, `work` 명령어에 쉼표로 구분한 큐 이름 목록을 전달하면 됩니다.

```shell
php artisan queue:work --queue=high,low
```

<a name="queue-workers-and-deployment"></a>
### 큐 워커와 배포

큐 워커는 장시간 실행되는 프로세스이기 때문에 코드 변경을 인지하지 못합니다. 따라서 큐 워커를 사용하는 애플리케이션을 배포할 때는 워커를 재시작해야 합니다. 모든 워커를 정상적으로 재시작하려면 `queue:restart` 명령어를 실행하세요.

```shell
php artisan queue:restart
```

이 명령어는 현재 실행 중인 모든 작업을 정상적으로 마친 후 워커가 종료되도록 안내합니다. 그러므로 작업이 유실되지 않습니다. `queue:restart` 명령어 실행 시, 워커가 종료되면 [Supervisor](#supervisor-configuration)와 같은 프로세스 매니저로 워커가 자동 재기동되도록 해야 합니다.

> [!NOTE]
> 큐는 [캐시](/docs/12.x/cache)를 사용해 재시작 신호를 저장하므로, 이 기능을 사용하기 전에 애플리케이션의 캐시 드라이버가 정상적으로 설정되어 있는지 확인해야 합니다.

<a name="job-expirations-and-timeouts"></a>
### 작업 만료 및 타임아웃

<a name="job-expiration"></a>
#### 작업 만료

`config/queue.php` 파일에서 각 큐 연결은 `retry_after` 옵션을 정의합니다. 이 옵션은 큐 연결이 작업을 처리할 때, 작업이 얼마나 오래 처리 중이었는지 확인하여, 작업이 지정된 초 만큼 처리 중이라면 다시 큐로 반환해야 하는지를 결정합니다. 예를 들어 `retry_after`가 90으로 지정되어 있다면, 90초 동안 처리되었음에도 작업이 완료(반환 또는 삭제)되지 않으면 작업이 큐로 되돌아갑니다. 일반적으로 이 값은 작업 하나가 최대 얼마만큼 오래 걸릴 수 있는지 고려하여 지정해야 합니다.

> [!WARNING]
> `retry_after` 값을 지정하지 않는 유일한 큐 연결은 Amazon SQS입니다. SQS는 [기본 Visibility Timeout](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/AboutVT.html) 설정값에 따라 동작하며, AWS 콘솔에서 관리합니다.

<a name="worker-timeouts"></a>
#### 워커 타임아웃

`queue:work` Artisan 명령어는 `--timeout` 옵션을 제공합니다. 기본 `--timeout` 값은 60초입니다. 작업이 지정된 초 수만큼(이 값 이상) 계속 처리 중이면, 워커는 에러와 함께 종료됩니다. 대개 워커는 [서버에 구성된 프로세스 매니저](#supervisor-configuration)에 의해 자동으로 재시작됩니다.

```shell
php artisan queue:work --timeout=60
```

`retry_after` 설정 옵션과 `--timeout` CLI 옵션은 서로 다르지만, 함께 동작해 작업이 중복 처리되거나 유실되지 않도록 보장해줍니다.

> [!WARNING]
> `--timeout` 값은 반드시 `retry_after` 값보다 몇 초 짧게 설정해야 합니다. 그래야 워커가 멈춘(응답하지 않는) 작업을 먼저 종료한 뒤, 해당 작업을 재시도하도록 보장할 수 있습니다. 만약 `--timeout` 값이 `retry_after` 값보다 길다면, 한 작업이 두 번 처리될 수 있습니다.

<a name="supervisor-configuration"></a>
## Supervisor(슈퍼바이저) 설정

운영 환경에서는 `queue:work` 프로세스가 항상 실행 중이어야 합니다. 그러나 워커 프로세스는 워커 타임아웃 초과나, `queue:restart` 명령 실행 등 다양한 이유로 언제든 종료될 수 있습니다.

따라서, `queue:work` 프로세스가 종료될 때 이를 탐지해 자동으로 재시작할 수 있는 프로세스 모니터를 반드시 설정해야 합니다. 또한, 프로세스 모니터를 통해 동시에 몇 개의 워커 프로세스를 실행할지도 지정할 수 있습니다. Linux 환경에서는 Supervisor가 많이 쓰이며, 아래에서 Supervisor 설정 방법을 안내합니다.

<a name="installing-supervisor"></a>
#### Supervisor 설치

Supervisor는 리눅스용 프로세스 모니터로, `queue:work` 프로세스가 실패 시 자동으로 재시작해줍니다. Ubuntu에서 Supervisor를 설치하려면 다음 명령어를 입력하세요.

```shell
sudo apt-get install supervisor
```

> [!NOTE]
> Supervisor 직접 설정과 관리를 부담스럽게 느낀다면, 라라벨 큐 워커를 완전히 관리해주는 [Laravel Cloud](https://cloud.laravel.com)를 고려할 수 있습니다.

<a name="configuring-supervisor"></a>
#### Supervisor 설정

Supervisor 설정 파일은 일반적으로 `/etc/supervisor/conf.d` 디렉터리에 저장됩니다. 이 디렉터리 안에 여러 개의 설정 파일을 만들어 프로세스 관리 정책을 지정할 수 있습니다. 예를 들어 `laravel-worker.conf` 파일을 만들어 `queue:work` 프로세스를 시작하고 감시할 수 있습니다.

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

위 예시에서 `numprocs` 설정 값은 Supervisor가 8개의 `queue:work` 프로세스를 실행하도록 합니다. 각 워커는 자동으로 감시 및 재시작됩니다. `command` 값은 실제 운영 환경과 워커 옵션에 맞게 수정해 사용해야 합니다.

> [!WARNING]
> `stopwaitsecs` 값은 가장 오래 걸리는 작업의 실행 시간보다 크게 잡아야 합니다. 그렇지 않으면 Supervisor가 작업이 끝나기 전에 프로세스를 강제로 종료할 수 있습니다.

<a name="starting-supervisor"></a>
#### Supervisor 시작

설정 파일을 만든 후에는 Supervisor 구성을 갱신하고 프로세스를 아래 명령어로 시작할 수 있습니다.

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start "laravel-worker:*"
```

Supervisor에 대한 더 자세한 정보는 [Supervisor 공식 문서](http://supervisord.org/index.html)를 참고하세요.

<a name="dealing-with-failed-jobs"></a>
## 실패한 작업 처리하기

큐에 올린 작업이 실패할 수도 있습니다. 걱정하지 마세요! 라라벨은 [작업이 재시도될 최대 횟수](#max-job-attempts-and-timeout)를 지정하는 편리한 방법을 제공합니다. 비동기 작업이 최대 재시도 횟수를 초과하면 `failed_jobs` 데이터베이스 테이블에 저장됩니다. [동기 방식으로 디스패치한 작업](/docs/12.x/queues#synchronous-dispatching)이 실패한 경우에는 이 테이블에 저장되지 않고, 즉시 예외가 애플리케이션에서 처리됩니다.

새로운 라라벨 프로젝트에는 대부분 `failed_jobs` 테이블 마이그레이션이 기본 제공됩니다. 만약 여러분의 애플리케이션에 해당 마이그레이션이 없다면, 다음 `make:queue-failed-table` 명령어로 만들 수 있습니다.

```shell
php artisan make:queue-failed-table

php artisan migrate
```

[큐 워커](#running-the-queue-worker) 실행 시 `queue:work` 명령어에 `--tries` 옵션을 사용해 한 작업에 대해 최대 몇 번 재시도할지 직접 지정할 수 있습니다. 옵션을 지정하지 않으면 기본적으로 한 번만 시도하거나, 작업 클래스의 `$tries` 속성 값만큼 시도합니다.

```shell
php artisan queue:work redis --tries=3
```

`--backoff` 옵션으로 라라벨이 작업이 예외를 만난 후 다시 시도하기 전 몇 초 대기할지 지정할 수 있습니다. 기본적으로는 즉시 큐에 다시 올려 재시도합니다.

```shell
php artisan queue:work redis --tries=3 --backoff=3
```

특정 작업별로 재시도 대기 시간을 설정하려면, 작업 클래스에 `backoff` 속성을 정의하면 됩니다.

```php
/**
 * 작업 재시도 전 대기할 초(second)
 *
 * @var int
 */
public $backoff = 3;
```

더 복잡한 대기 시간이 필요하다면, 작업 클래스에 `backoff` 메서드를 정의할 수도 있습니다.

```php
/**
 * 작업 재시도 전 대기할 초(second) 반환
 */
public function backoff(): int
{
    return 3;
}
```

`backoff` 메서드에서 배열을 반환하면, "지수(backoff)" 알고리즘 방식의 복잡한 재시도 딜레이를 쉽게 설정할 수 있습니다. 아래 예시는 첫 번째 재시도엔 1초, 두 번째엔 5초, 세 번째엔 10초, 이후 남은 재시도(있다면)는 계속 10초 대기로 반복됩니다.

```php
/**
 * 작업 재시도 전 대기할 초(second) 배열 반환
 *
 * @return array<int, int>
 */
public function backoff(): array
{
    return [1, 5, 10];
}
```

<a name="cleaning-up-after-failed-jobs"></a>
### 실패한 작업 정리 및 후처리

작업이 실패했을 때, 사용자에게 알림을 보내거나 일부 완료된 작업을 원상 복구하는 추가 처리가 필요할 수 있습니다. 이를 위해 작업 클래스에 `failed` 메서드를 정의할 수 있습니다. `failed` 메서드에는 해당 작업을 실패하게 만든 `Throwable` 예외 인스턴스가 전달됩니다.

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
     * 새 작업 인스턴스 생성
     */
    public function __construct(
        public Podcast $podcast,
    ) {}

    /**
     * 작업 실행
     */
    public function handle(AudioProcessor $processor): void
    {
        // 업로드된 팟캐스트 처리...
    }

    /**
     * 작업 실패 시 후처리
     */
    public function failed(?Throwable $exception): void
    {
        // 실패 알림 전송 등 추가 처리...
    }
}
```

> [!WARNING]
> `failed` 메서드가 호출되기 직전에 작업 인스턴스가 새로 생성되므로, `handle` 메서드 내부에서 변경된 속성 값들은 반영되지 않는 점에 유의해야 합니다.

<a name="retrying-failed-jobs"></a>
### 실패한 작업 재시도

`failed_jobs` 테이블에 저장된 모든 실패한 작업 목록을 확인하려면 `queue:failed` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan queue:failed
```

`queue:failed` 명령어는 작업 ID, 연결명, 큐 이름, 실패 시간 등 각 작업의 상세 정보를 보여줍니다. 작업 ID를 이용해 해당 작업을 재시도할 수 있습니다. 예를 들어, ID가 `ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece`인 실패한 작업을 재시도하려면 아래와 같이 실행하세요.

```shell
php artisan queue:retry ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece
```

필요하다면 여러 작업 ID를 한 번에 전달할 수도 있습니다.

```shell
php artisan queue:retry ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece 91401d2c-0784-4f43-824c-34f94a33c24d
```

특정 큐에서 발생한 실패 작업만 모두 재시도하려면 아래처럼 실행하세요.

```shell
php artisan queue:retry --queue=name
```

실패한 모든 작업을 한 번에 재시도하려면 `queue:retry` 명령에 `all`을 인자로 전달하면 됩니다.

```shell
php artisan queue:retry all
```

실패한 작업을 삭제하려면 `queue:forget` 명령을 사용할 수 있습니다.

```shell
php artisan queue:forget 91401d2c-0784-4f43-824c-34f94a33c24d
```

> [!NOTE]
> [Horizon](/docs/12.x/horizon)을 사용할 때는, `queue:forget` 명령 대신 반드시 `horizon:forget` 명령을 사용하여 실패한 작업을 삭제해야 합니다.

`failed_jobs` 테이블에 저장된 모든 실패 작업 기록을 완전히 삭제하려면 `queue:flush` 명령을 사용할 수 있습니다.

```shell
php artisan queue:flush
```

<a name="ignoring-missing-models"></a>
### 누락된 모델 무시하기

Eloquent 모델을 작업에 의존성 주입하면, 큐에 올릴 때 해당 모델이 직렬화되어 저장되고, 작업 처리 시 데이터베이스에서 다시 조회됩니다. 하지만 작업이 대기 중인 동안 모델이 삭제될 수도 있는데, 이럴 경우 `ModelNotFoundException` 예외로 인해 작업이 실패하게 됩니다.

이런 상황에서, 특정 작업의 `deleteWhenMissingModels` 속성을 `true`로 설정해 두면 관련 모델이 없어도 예외를 발생시키지 않고 해당 작업을 조용히 삭제할 수 있습니다.

```php
/**
 * 참조 모델이 존재하지 않으면 작업을 바로 삭제
 *
 * @var bool
 */
public $deleteWhenMissingModels = true;
```

<a name="pruning-failed-jobs"></a>
### 실패한 작업 기록 정리(Pruning)

애플리케이션의 `failed_jobs` 테이블을 정리하려면 `queue:prune-failed` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan queue:prune-failed
```

기본적으로 24시간 이상 경과한 모든 실패 작업 기록이 정리됩니다. `--hours` 옵션을 사용하면 최근 N시간 이내에 기록된 실패 작업만 남기고 나머지를 삭제할 수 있습니다. 예를 들어, 아래 명령어는 48시간이 지난 실패 작업만 삭제합니다.

```shell
php artisan queue:prune-failed --hours=48
```

<a name="storing-failed-jobs-in-dynamodb"></a>
### 실패한 작업 기록 DynamoDB에 저장하기

라라벨은 [DynamoDB](https://aws.amazon.com/dynamodb)에 실패한 작업 기록을 저장할 수도 있습니다. 이 경우에도 별도의 DynamoDB 테이블을 직접 만들어야 합니다. 보통 테이블 이름은 `failed_jobs`로 하지만, 애플리케이션의 `queue` 설정 파일 내 `queue.failed.table` 값이 있다면 그에 맞추어야 합니다.

`failed_jobs` 테이블에는 문자열 타입 파티션 키로 `application`, 정렬 키로 `uuid`가 있어야 합니다. `application`에는 `app` 설정 파일 내 `name` 값이 들어가므로 여러 라라벨 애플리케이션이 같은 테이블에 실패 작업을 저장할 수 있습니다.

또한, 라라벨 애플리케이션이 Amazon DynamoDB와 통신할 수 있도록 AWS SDK를 설치해야 합니다.

```shell
composer require aws/aws-sdk-php
```

이후 `queue.failed.driver` 설정 값을 `dynamodb`로 지정해야 합니다. 그리고 실패 작업 설정 배열에도 `key`, `secret`, `region` 값을 지정해야 하며, AWS 인증에 사용됩니다. `dynamodb` 드라이버 사용 시에는 `queue.failed.database` 옵션이 필요하지 않습니다.

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

### 실패한 작업 저장 비활성화

`queue.failed.driver` 설정 옵션의 값을 `null`로 지정하면, 라라벨이 실패한 작업을 저장하지 않고 즉시 폐기하도록 할 수 있습니다. 일반적으로는 `QUEUE_FAILED_DRIVER` 환경 변수를 통해 쉽게 설정할 수 있습니다.

```ini
QUEUE_FAILED_DRIVER=null
```

<a name="failed-job-events"></a>
### 실패한 작업 이벤트

작업이 실패했을 때 호출되는 이벤트 리스너를 등록하고 싶다면, `Queue` 파사드의 `failing` 메서드를 사용할 수 있습니다. 예를 들어, 라라벨에서 기본 제공하는 `AppServiceProvider`의 `boot` 메서드에서 이 이벤트에 클로저를 등록할 수 있습니다.

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Queue;
use Illuminate\Support\ServiceProvider;
use Illuminate\Queue\Events\JobFailed;

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
        Queue::failing(function (JobFailed $event) {
            // $event->connectionName
            // $event->job
            // $event->exception
        });
    }
}
```

<a name="clearing-jobs-from-queues"></a>
## 큐에서 작업 비우기

> [!NOTE]
> [Horizon](/docs/12.x/horizon)을 사용하는 경우에는 큐의 작업을 비울 때 `queue:clear` 명령어 대신 `horizon:clear` 명령어를 사용해야 합니다.

기본 연결의 기본 큐에 있는 모든 작업을 삭제하려면 다음 아티즌 명령어를 사용할 수 있습니다.

```shell
php artisan queue:clear
```

특정 연결 및 큐의 작업을 삭제하려면, `connection` 인수와 `queue` 옵션을 함께 지정할 수 있습니다.

```shell
php artisan queue:clear redis --queue=emails
```

> [!WARNING]
> 큐에서 작업을 비우는 기능은 SQS, Redis, 그리고 데이터베이스 큐 드라이버에서만 사용할 수 있습니다. 또한, SQS의 메시지 삭제는 최대 60초까지 소요될 수 있으므로, 큐를 비운 후 60초 이내에 SQS 큐로 전송된 작업도 삭제될 수 있습니다.

<a name="monitoring-your-queues"></a>
## 큐 모니터링

큐에 갑자기 많은 작업이 밀려들면, 작업이 완료될 때까지 대기 시간이 길어질 수 있습니다. 필요하다면, 라라벨이 큐의 작업 개수가 설정한 임계값을 초과할 때 알림을 보내도록 설정할 수 있습니다.

시작하려면, [매 분마다](/docs/12.x/scheduling) `queue:monitor` 명령어를 스케줄링해야 합니다. 이 명령어는 모니터링하려는 큐의 이름과 원하는 작업 개수 임계값이 인수로 필요합니다.

```shell
php artisan queue:monitor redis:default,redis:deployments --max=100
```

이 명령어를 스케줄하는 것만으로는 큐 작업 과부하 상태에 대한 알림이 자동으로 전송되지 않습니다. 명령어 실행 중 모니터링 대상 큐가 임계값을 초과하면, `Illuminate\Queue\Events\QueueBusy` 이벤트가 발생합니다. 이 이벤트를 애플리케이션의 `AppServiceProvider`에서 감지하여, 개발자나 팀에 알림을 보낼 수 있습니다.

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
## 테스트

작업을 디스패치하는 코드를 테스트할 때는, 실제로 큐 작업을 실행하지 않도록 라라벨에 지시하고 싶을 수 있습니다. (큐에 등록되는 작업의 코드는 별도 테스트를 통해 직접 실행 및 검증할 수 있습니다.) 작업 자체를 테스트하려면, 작업 인스턴스를 만들어서 테스트 코드에서 직접 `handle` 메서드를 호출하면 됩니다.

큐에 실제로 작업이 추가되는 것을 방지하려면, `Queue` 파사드의 `fake` 메서드를 사용할 수 있습니다. `Queue::fake()`를 호출한 후에는 작업 디스패치 시도 자체를 검증(어설션)할 수 있습니다.

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

`assertPushed` 또는 `assertNotPushed` 메서드에 클로저를 전달하여, 지정한 "조건"을 만족하는 작업이 큐에 추가(또는 미추가)되었는지 검증할 수 있습니다. 전달한 조건을 만족하는 작업이 하나라도 큐에 추가된 경우에 어설션이 통과합니다.

```php
Queue::assertPushed(function (ShipOrder $job) use ($order) {
    return $job->order->id === $order->id;
});
```

<a name="faking-a-subset-of-jobs"></a>
### 일부 작업만 페이크 처리하기

특정 작업만 페이크(faking) 처리하고, 나머지 작업은 평소처럼 실제로 실행되도록 하려면, 페이크 처리할 작업의 클래스명을 배열로 전달하여 `fake` 메서드를 사용할 수 있습니다.

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

특정 작업들을 제외한 나머지 모든 작업을 페이크 처리하고 싶을 때는 `except` 메서드를 사용할 수 있습니다.

```php
Queue::fake()->except([
    ShipOrder::class,
]);
```

<a name="testing-job-chains"></a>
### 작업 체인 테스트

작업 체인을 테스트하려면, `Bus` 파사드의 페이크 기능을 사용해야 합니다. `Bus` 파사드의 `assertChained` 메서드를 이용하면 [연속된 작업 체인](/docs/12.x/queues#job-chaining)이 정상적으로 디스패치되었는지 확인할 수 있습니다. `assertChained` 메서드의 첫 번째 인수로 체인을 이루는 작업 목록을 배열로 전달합니다.

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

위 예시처럼, 체인 배열에 작업의 클래스명만 나열할 수도 있습니다. 하지만, 실제 작업 인스턴스의 배열을 전달할 수도 있습니다. 이렇게 하면, 라라벨이 체인으로 디스패치된 작업의 클래스와 속성 값이 정확히 일치하는지까지 검사합니다.

```php
Bus::assertChained([
    new ShipOrder,
    new RecordShipment,
    new UpdateInventory,
]);
```

특정 작업이 별도 체인 없이 개별적으로 디스패치되었는지 확인하고 싶다면, `assertDispatchedWithoutChain` 메서드를 사용합니다.

```php
Bus::assertDispatchedWithoutChain(ShipOrder::class);
```

<a name="testing-chain-modifications"></a>
#### 체인 수정 테스트하기

체인에 속한 작업이 기존 체인에 작업을 [앞에 추가(prepend)하거나 뒤에 추가(append)](#adding-jobs-to-the-chain)할 경우, 해당 작업의 `assertHasChain` 메서드를 사용해 기대하는 작업들의 체인이 남아있는지 검증할 수 있습니다.

```php
$job = new ProcessPodcast;

$job->handle();

$job->assertHasChain([
    new TranscribePodcast,
    new OptimizePodcast,
    new ReleasePodcast,
]);
```

남아 있는 체인이 비어 있는지 확인할 때는 `assertDoesntHaveChain` 메서드를 사용할 수 있습니다.

```php
$job->assertDoesntHaveChain();
```

<a name="testing-chained-batches"></a>
#### 체인에 포함된 배치 테스트

작업 체인에 [배치(batch) 작업](#chains-and-batches)이 포함된 경우에는, 체인 어설션 내에 `Bus::chainedBatch`를 사용해 체인에 포함된 배치가 기대에 부합하는지 확인할 수 있습니다.

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
### 작업 배치 테스트

`Bus` 파사드의 `assertBatched` 메서드를 사용하면, [작업 배치](/docs/12.x/queues#job-batching)가 디스패치되었는지 확인할 수 있습니다. `assertBatched`로 전달하는 클로저에는 `Illuminate\Bus\PendingBatch` 인스턴스가 넘어오며, 이를 통해 해당 배치에 포함된 작업들을 검사할 수 있습니다.

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

`assertBatchCount` 메서드를 사용하면 디스패치된 배치의 개수가 원하는 값인지 검증할 수 있습니다.

```php
Bus::assertBatchCount(3);
```

또한, `assertNothingBatched`를 사용하면 배치가 디스패치되지 않았는지 확인할 수 있습니다.

```php
Bus::assertNothingBatched();
```

<a name="testing-job-batch-interaction"></a>
#### 작업과 배치 상호작용 테스트

가끔 개별 작업과 해당 배치 간의 상호작용을 테스트해야 할 때가 있습니다. 예를 들어, 작업이 배치의 진행을 취소하는지 등을 확인할 필요가 있을 수 있습니다. 이를 위해서, 테스트 시 `withFakeBatch` 메서드를 사용해 작업에 페이크 배치를 할당할 수 있습니다. `withFakeBatch`는 작업 인스턴스와 페이크 배치를 튜플로 반환합니다.

```php
[$job, $batch] = (new ShipOrder)->withFakeBatch();

$job->handle();

$this->assertTrue($batch->cancelled());
$this->assertEmpty($batch->added);
```

<a name="testing-job-queue-interactions"></a>
### 작업과 큐 상호작용 테스트

가끔 큐에 등록된 작업이 [스스로 다시 큐로 되돌리는(release)](#manually-releasing-a-job) 동작, 또는 스스로 삭제하는 동작 등이 잘 작동하는지 테스트해야 할 수 있습니다. 이런 큐-작업 상호작용을 검증하기 위해서는, 작업 인스턴스를 생성한 뒤 `withFakeQueueInteractions` 메서드를 호출합니다.

이렇게 큐 상호작용을 페이크 처리한 후에, 작업의 `handle` 메서드를 호출하면 됩니다. 이후 `assertReleased`, `assertDeleted`, `assertNotDeleted`, `assertFailed`, `assertFailedWith`, `assertNotFailed` 등 다양한 검증 메서드를 이용해 큐 상호작용 결과를 어설션할 수 있습니다.

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

`Queue` [파사드](/docs/12.x/facades)의 `before`와 `after` 메서드를 사용하면, 큐 작업이 처리되기 전 또는 후에 실행할 콜백을 정의할 수 있습니다. 이 콜백을 활용해서 추가 로깅을 하거나, 대시보드 통계 값을 증가시키는 등의 작업을 할 수 있습니다. 보통 이런 코드는 [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에서 구현합니다. 예를 들어, 라라벨에서 기본 제공하는 `AppServiceProvider`를 사용할 수 있습니다.

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

`Queue` [파사드](/docs/12.x/facades)의 `looping` 메서드를 사용하면, 워커가 큐에서 작업을 가져오기 전에 실행되는 콜백을 등록할 수 있습니다. 예를 들어, 이전에 실패한 작업이 남긴 트랜잭션이 있다면, 이를 롤백하도록 클로저를 등록할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Queue;

Queue::looping(function () {
    while (DB::transactionLevel() > 0) {
        DB::rollBack();
    }
});
```