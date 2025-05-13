# 큐 (Queues)

- [소개](#introduction)
    - [커넥션과 큐의 차이](#connections-vs-queues)
    - [드라이버별 참고 사항 및 선행 조건](#driver-prerequisites)
- [잡 생성](#creating-jobs)
    - [잡 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [유일한 잡(Unique Jobs)](#unique-jobs)
    - [암호화된 잡](#encrypted-jobs)
- [잡 미들웨어](#job-middleware)
    - [속도 제한(Rate Limiting)](#rate-limiting)
    - [잡 중복 실행 방지](#preventing-job-overlaps)
    - [예외 상황에서의 제한(Throttling Exceptions)](#throttling-exceptions)
    - [잡 건너뛰기](#skipping-jobs)
- [잡 디스패치](#dispatching-jobs)
    - [지연 디스패치](#delayed-dispatching)
    - [동기 디스패치](#synchronous-dispatching)
    - [잡과 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [잡 체이닝](#job-chaining)
    - [큐와 커넥션 커스터마이징](#customizing-the-queue-and-connection)
    - [최대 시도 횟수/타임아웃 설정](#max-job-attempts-and-timeout)
    - [에러 처리](#error-handling)
- [잡 배치 처리(Job Batching)](#job-batching)
    - [배치 가능한 잡 정의](#defining-batchable-jobs)
    - [배치 디스패치](#dispatching-batches)
    - [체인과 배치의 관계](#chains-and-batches)
    - [배치에 잡 추가하기](#adding-jobs-to-batches)
    - [배치 조회](#inspecting-batches)
    - [배치 취소](#cancelling-batches)
    - [배치 실패 처리](#batch-failures)
    - [배치 데이터 정리](#pruning-batches)
    - [DynamoDB에 배치 저장](#storing-batches-in-dynamodb)
- [클로저 큐잉](#queueing-closures)
- [큐 워커 실행](#running-the-queue-worker)
    - [`queue:work` 명령어](#the-queue-work-command)
    - [큐 우선순위](#queue-priorities)
    - [큐 워커와 배포](#queue-workers-and-deployment)
    - [잡 만료 및 타임아웃](#job-expirations-and-timeouts)
- [Supervisor 설정](#supervisor-configuration)
- [실패한 잡 처리](#dealing-with-failed-jobs)
    - [실패한 잡 후처리](#cleaning-up-after-failed-jobs)
    - [실패한 잡 재시도](#retrying-failed-jobs)
    - [존재하지 않는 모델 무시](#ignoring-missing-models)
    - [실패한 잡 데이터 정리](#pruning-failed-jobs)
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

웹 애플리케이션을 개발하다 보면, 업로드된 CSV 파일 파싱 및 저장과 같이 일반적인 웹 요청 시간 내에 처리하기에는 너무 오래 걸리는 작업들이 있을 수 있습니다. 이런 경우, 라라벨에서는 큐를 사용해 백그라운드에서 처리할 수 있는 잡(jobs)을 쉽게 만들 수 있습니다. 시간이 많이 소요되는 작업을 큐로 옮기면, 애플리케이션은 웹 요청에 더욱 빠르게 응답할 수 있고, 사용자 경험 또한 크게 향상됩니다.

라라벨의 큐 시스템은 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io)와 같은 다양한 큐 백엔드, 또는 관계형 데이터베이스까지 다양한 환경에서 일관된 큐 API를 제공합니다.

라라벨의 큐 관련 설정은 애플리케이션의 `config/queue.php` 설정 파일에 저장되어 있습니다. 이 파일에는 프레임워크에 기본 포함된 각 큐 드라이버(데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 등) 별로 커넥션 구성이 들어 있습니다. 또한 잡을 즉시 실행하는 동기(synchronous) 드라이버(로컬 개발용)도 포함되어 있습니다. 잡을 버리는 `null` 큐 드라이버도 제공됩니다.

> [!NOTE]
> 라라벨은 이제 Redis 기반 큐를 위한 아름다운 대시보드와 구성 시스템인 Horizon을 제공합니다. 보다 자세한 내용은 [Horizon 공식 문서](/docs/12.x/horizon)를 참고하세요.

<a name="connections-vs-queues"></a>
### 커넥션과 큐의 차이

라라벨 큐를 다루기 전에 "커넥션(connection)"과 "큐(queue)"의 차이를 먼저 이해하는 것이 중요합니다. `config/queue.php` 설정 파일에는 `connections`라는 배열이 들어 있습니다. 이 설정은 Amazon SQS, Beanstalk, Redis 같은 큐 백엔드와의 커넥션을 정의합니다. 하나의 큐 커넥션 아래에는 여러 개의 "큐"를 정의할 수 있는데, 각각은 잡이 쌓이는 별도의 스택 또는 더미라고 생각할 수 있습니다.

각 커넥션 설정의 예제에는 `queue` 속성이 포함되어 있는데, 이 속성은 해당 커넥션에 잡을 디스패치할 때 사용할 기본 큐를 의미합니다. 즉, 잡을 어떤 큐에 넣을지 명시하지 않고 디스패치하면, 커넥션 설정에 정의된 `queue` 속성의 큐로 잡이 들어가게 됩니다.

```php
use App\Jobs\ProcessPodcast;

// 이 잡은 기본 커넥션의 기본 큐에 넣어집니다...
ProcessPodcast::dispatch();

// 이 잡은 기본 커넥션의 "emails" 큐에 넣어집니다...
ProcessPodcast::dispatch()->onQueue('emails');
```

모든 애플리케이션이 반드시 여러 큐를 분리해 사용할 필요는 없으므로, 단일 큐만 사용하는 단순한 구조도 충분히 가능합니다. 하지만 여러 큐에 잡을 분리해서 넣으면, 잡 워커가 어떤 큐를 우선 처리할 지 지정할 수 있어, 업무 우선순위나 분산처리에 유용합니다. 예를 들어, `high` 큐로 잡을 보내면, 해당 큐를 우선 처리하는 워커를 실행할 수 있습니다.

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버별 참고 사항 및 선행 조건

<a name="database"></a>
#### 데이터베이스

`database` 큐 드라이버를 사용하려면, 잡을 저장할 데이터베이스 테이블이 필요합니다. 일반적으로 이 테이블은 라라벨 기본 제공 마이그레이션 파일(`0001_01_01_000002_create_jobs_table.php`)에 포함되어 있습니다. 만약 해당 마이그레이션이 없다면, 아래와 같이 `make:queue-table` Artisan 명령어로 생성한 뒤 마이그레이션을 실행할 수 있습니다.

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면, `config/database.php` 설정 파일에서 Redis 데이터베이스 커넥션을 먼저 구성해야 합니다.

> [!WARNING]
> `serializer` 및 `compression` Redis 옵션은 `redis` 큐 드라이버에서는 사용할 수 없습니다.

**Redis 클러스터**

Redis 큐 커넥션에서 Redis 클러스터를 사용할 때는, 큐 이름에 [키 해시 태그](https://redis.io/docs/reference/cluster-spec/#hash-tags)를 포함해야 합니다. 이렇게 해야 특정 큐의 Redis 키들이 동일한 해시 슬롯에 배치되어 올바르게 동작합니다.

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

Redis 큐 사용 시에는 `block_for` 설정 옵션을 사용할 수 있습니다. 이 옵션은 잡이 준비될 때까지 큐 드라이버가 얼마나 기다릴지(초 단위) 지정합니다. 설정값이 0보다 크면, 워커 루프가 반복되기 전에 지정한 시간만큼 대기하여 잡이 새로 들어올 때까지 Redis 데이터베이스에 대한 불필요한 폴링을 줄일 수 있습니다.

예를 들어, 잡이 대기할 때 5초 동안만 대기하도록 설정할 수 있습니다.

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
> `block_for`를 `0`으로 설정하면, 잡이 대기열에 들어올 때까지 queue worker가 무한정 대기하게 됩니다. 이 경우, 다음 잡이 처리되기 전까지 `SIGTERM` 등 종료 신호가 제대로 전달되지 않을 수 있습니다.

<a name="other-driver-prerequisites"></a>
#### 다른 드라이버 사용을 위한 선행 패키지

아래의 큐 드라이버를 사용할 때는 다음과 같은 의존성이 필요합니다. 이들은 Composer 패키지 매니저로 설치할 수 있습니다.

<div class="content-list" markdown="1">

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~2.0` 또는 phpredis PHP 익스텐션
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`

</div>

<a name="creating-jobs"></a>
## 잡 생성

<a name="generating-job-classes"></a>
### 잡 클래스 생성

애플리케이션 내의 큐잉 가능한 모든 잡은 기본적으로 `app/Jobs` 디렉터리에 저장됩니다. 만약 `app/Jobs` 디렉터리가 없다면, 아래와 같이 `make:job` Artisan 명령어를 실행하면 디렉터리가 자동으로 생성됩니다.

```shell
php artisan make:job ProcessPodcast
```

생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하며, 이는 라라벨에게 해당 잡을 비동기로 큐에 넣어 처리할 잡임을 알립니다.

> [!NOTE]
> 잡 스텁 파일은 [스텁 퍼블리싱](/docs/12.x/artisan#stub-customization)을 통해 커스터마이징 할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조

잡 클래스는 일반적으로 매우 단순하며, 큐에서 잡이 처리될 때 호출되는 `handle` 메서드만 포함하는 경우가 많습니다. 예를 들어, 팟캐스트 게시 서비스를 운영하며 업로드된 팟캐스트 파일을 게시 전에 처리해야 한다고 가정해봅시다.

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
     * 새로운 잡 인스턴스 생성자입니다.
     */
    public function __construct(
        public Podcast $podcast,
    ) {}

    /**
     * 잡 실행 메서드입니다.
     */
    public function handle(AudioProcessor $processor): void
    {
        // 업로드된 팟캐스트 파일 처리...
    }
}
```

위 예제에서는 [Eloquent 모델](/docs/12.x/eloquent)을 잡 생성자의 인수로 직접 전달할 수 있다는 점에 주목하세요. 잡이 `Queueable` 트레잇을 사용하고 있기 때문에, Eloquent 모델과 이미 로드된 관계 정보 역시 잡이 큐에 들어갈 때 깔끔하게 직렬화 및 역직렬화됩니다.

잡의 생성자가 Eloquent 모델을 받는 경우, 해당 모델의 식별자만 큐에 직렬화되어 저장됩니다. 실제로 잡이 처리될 때는, 큐 시스템이 데이터베이스에서 모델 인스턴스와 관계 데이터를 다시 가져와 복원해 줍니다. 이 방식 덕분에 큐 드라이버로 전달되는 잡 페이로드의 용량을 훨씬 줄일 수 있습니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드 의존성 주입

`handle` 메서드는 잡이 큐에서 처리될 때 호출됩니다. 이때, `handle` 메서드의 타입힌트를 통해 필요한 의존성을 자동으로 주입받을 수 있습니다. 라라벨의 [서비스 컨테이너](/docs/12.x/container)가 이를 자동으로 처리해줍니다.

서비스 컨테이너에서 `handle` 메서드의 의존성 주입 방식을 완전히 제어하고 싶다면, 컨테이너의 `bindMethod` 메서드를 사용할 수 있습니다. `bindMethod`는 콜백 함수를 받고, 이 콜백 안에서 잡 인스턴스와 컨테이너를 직접 이용해 원하는 방식으로 `handle`을 호출할 수 있습니다. 일반적으로 해당 코드는 `App\Providers\AppServiceProvider` [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에서 호출합니다.

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 바이너리 데이터(예: 이미지 원본 데이터 등)를 큐잉 잡으로 전달할 때는 `base64_encode` 함수를 거친 뒤 전달해야 합니다. 그렇지 않으면 잡이 큐에 저장될 때 JSON 직렬화가 제대로 이루어지지 않을 수 있습니다.

<a name="handling-relationships"></a>
#### 큐잉된 관계 데이터 다루기

큐잉 잡에 Eloquent 모델의 관계가 로드된 채로 들어가는 경우, 직렬화된 잡 문자열의 용량이 매우 커질 수 있습니다. 또, 잡이 역직렬화되어 모델 관계가 다시 로드될 때는, 그 관계 전체가 데이터베이스에서 무조건 다시 조회됩니다. 따라서 잡이 큐에 들어가기 전 특정 관계의 일부만 지정해서 가져왔더라도, 잡 처리 시에는 그 제약이 무시되고 전체 관계가 로드된다는 점에 유의해야 합니다. 만약 관계의 일부만 사용하고 싶다면, 잡 내에서 해당 관계에 다시 제약을 걸어주는 것이 안전합니다.

또는, 아예 관계 데이터가 직렬화되지 않도록 하고 싶다면, 모델 프로퍼티를 할당할 때 `withoutRelations` 메서드를 호출하면 됩니다. 이 메서드는 관계가 분리된 모델 인스턴스를 반환합니다.

```php
/**
 * 새로운 잡 인스턴스 생성자입니다.
 */
public function __construct(
    Podcast $podcast,
) {
    $this->podcast = $podcast->withoutRelations();
}
```

PHP 생성자 속성 프로모션을 사용할 때, Eloquent 모델의 관계를 직렬화하지 않도록 지정하려면 `WithoutRelations` 속성(attribute)을 사용할 수 있습니다.

```php
use Illuminate\Queue\Attributes\WithoutRelations;

/**
 * 새로운 잡 인스턴스 생성자입니다.
 */
public function __construct(
    #[WithoutRelations]
    public Podcast $podcast,
) {}
```

잡이 단일 모델이 아니라 Eloquent 모델의 컬렉션이나 배열을 인수로 받을 경우, 해당 컬렉션/배열 내부의 모델에서는 관계 복원이 이루어지지 않습니다. 이는 대량의 모델을 동시에 처리할 때 불필요한 리소스 소비를 방지하기 위함입니다.

<a name="unique-jobs"></a>
### 유일한 잡(Unique Jobs)

> [!WARNING]
> 유일한 잡 기능을 사용하려면 [락을 지원하는 캐시 드라이버](/docs/12.x/cache#atomic-locks)가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버에서 원자적 락을 지원합니다. 또한, 유일한 잡 제약은 잡 배치(batch) 내의 잡에는 적용되지 않습니다.

특정 잡이 일정 시점에 큐 내에 한 개만 존재하도록 보장하고 싶을 때가 있습니다. 이 기능은 잡 클래스에 `ShouldBeUnique` 인터페이스를 구현하여 간단히 사용할 수 있습니다. 별도의 추가 메서드 정의는 필요하지 않습니다.

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

위 예제의 경우, `UpdateSearchIndex` 잡은 유일하게 동작합니다. 즉, 동일한 잡이 이미 큐에 있고 아직 처리 중이라면, 새로운 잡이 디스패치되지 않습니다.

특정 "키"로 잡을 유일하게 만들거나, 잡의 유일성 유지 시간을 제한하고 싶다면 `uniqueId` 및 `uniqueFor` 프로퍼티나 메서드를 잡 클래스에 정의할 수 있습니다.

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
     * 잡의 유일 락이 해제되기까지 지속될 시간(초)입니다.
     *
     * @var int
     */
    public $uniqueFor = 3600;

    /**
     * 잡의 유일 ID 반환.
     */
    public function uniqueId(): string
    {
        return $this->product->id;
    }
}
```

위 예시에서는 상품 번호를 이용해 잡의 유일성을 부여했습니다. 즉, 동일 상품 ID로 잡을 추가 디스패치하려 할 때, 기존 잡이 끝나야만 새로운 잡이 큐에 추가됩니다. 더불어, 만약 기존 잡이 1시간 내에 끝나지 않으면 락이 해제되어 동일한 키를 가진 다른 잡을 큐에 다시 넣을 수 있게 됩니다.

> [!WARNING]
> 여러 웹 서버나 컨테이너에서 잡을 디스패치한다면, 모든 서버가 같은 중앙 캐시 서버를 사용하도록 설정해야만 라라벨이 잡의 유일성을 제대로 판단할 수 있습니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 잡 처리 직전까지 유일성 유지

유일한 잡은 기본적으로 잡 처리가 끝나거나 허용된 재시도 횟수를 모두 소진했을 때 "락"이 해제됩니다. 하지만, 잡이 처리 시작 직전에 바로 락을 해제하고 싶을 때도 있습니다. 이 경우, 잡 클래스에 `ShouldBeUnique` 대신 `ShouldBeUniqueUntilProcessing` 인터페이스를 구현하면 됩니다.

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
#### 유일 잡 락 동작 방식

내부적으로는 `ShouldBeUnique` 잡이 디스패치되면, 라라벨이 `uniqueId` 키를 사용해 [락](/docs/12.x/cache#atomic-locks)을 획득하려 시도합니다. 락을 획득하지 못하면 잡을 디스패치하지 않습니다. 이 락은 잡이 정상 처리되거나 재시도 한도를 넘어서면 해제됩니다. 기본적으로는 라라벨이 기본 캐시 드라이버로 락을 획득하지만, 다른 드라이버를 사용하고 싶을 때는 `uniqueVia` 메서드를 정의하여 캐시 드라이버를 반환하면 됩니다.

```php
use Illuminate\Contracts\Cache\Repository;
use Illuminate\Support\Facades\Cache;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...

    /**
     * 유일 잡 락에 사용할 캐시 드라이버 반환.
     */
    public function uniqueVia(): Repository
    {
        return Cache::driver('redis');
    }
}
```

> [!NOTE]
> 단순히 동시에 여러 개의 잡이 처리되는 것을 제한하고 싶을 뿐이라면, [WithoutOverlapping](/docs/12.x/queues#preventing-job-overlaps) 잡 미들웨어를 사용하는 것이 더 적합합니다.

<a name="encrypted-jobs"></a>
### 암호화된 잡

라라벨은 [암호화](/docs/12.x/encryption)를 통해 잡 데이터의 기밀성과 무결성을 보장할 수 있습니다. 사용 방법은 매우 간단합니다. 해당 잡 클래스에 `ShouldBeEncrypted` 인터페이스를 구현하기만 하면, 라라벨이 자동으로 잡을 암호화한 뒤 큐에 넣고, 처리 시 복호화해 실행합니다.

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

잡 미들웨어는 큐잉된 잡의 실행을 감싸는 커스텀 로직을 추가할 수 있게 해주어, 잡 클래스 자체의 중복 코드를 줄이는 데 도움을 줍니다. 예를 들어, 아래의 `handle` 메서드는 라라벨의 Redis 속도 제한 기능을 활용해, 5초에 한 번만 잡이 실행되도록 제한한 예시입니다.

```php
use Illuminate\Support\Facades\Redis;

/**
 * 잡 실행 메서드입니다.
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

이 코드는 동작에는 문제가 없지만, `handle` 메서드 내부가 Redis 속도 제한 로직으로 복잡해지고, 비슷한 제한이 필요한 다른 잡에도 코드를 복제해야만 하는 단점이 있습니다.

이럴 때는 `handle` 메서드 내에 직접 속도 제한 로직을 두는 대신, 이를 전담하는 잡 미들웨어를 따로 만들면 훨씬 깔끔합니다. 라라벨에는 잡 미들웨어 전용 기본 위치가 정해져 있지 않으므로, 원하는 위치에 자유롭게 생성하면 됩니다. 예제에서는 `app/Jobs/Middleware` 디렉터리에 미들웨어를 생성합니다.

```php
<?php

namespace App\Jobs\Middleware;

use Closure;
use Illuminate\Support\Facades\Redis;

class RateLimited
{
    /**
     * 큐잉된 잡 처리.
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

이처럼 [라우트 미들웨어](/docs/12.x/middleware)와 마찬가지로, 잡 미들웨어는 처리 중인 잡 객체와 잡을 계속 진행시키는 콜백을 인수로 받습니다.

잡 미들웨어를 만들었다면, 잡 클래스의 `middleware` 메서드에서 반환값으로 미들웨어 인스턴스를 포함하면 됩니다. 이 메서드는 `make:job` Artisan 명령어로 생성된 잡에는 기본적으로 존재하지 않으므로, 직접 추가해야 합니다.

```php
use App\Jobs\Middleware\RateLimited;

/**
 * 잡이 거쳐야 할 미들웨어 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited];
}
```

> [!NOTE]
> 잡 미들웨어는 큐잉 이벤트 리스너, 메일러블, 알림(Notification) 등에도 적용할 수 있습니다.

<a name="rate-limiting"></a>
### 속도 제한(Rate Limiting)

위에서 직접 속도 제한 잡 미들웨어를 만드는 방법을 보았지만, 라라벨에는 이미 기본 제공되는 속도 제한 미들웨어도 있습니다. [라우트 속도 제한자](/docs/12.x/routing#defining-rate-limiters)와 마찬가지로, 잡 속도 제한도 `RateLimiter` 파사드의 `for` 메서드를 사용해 정의할 수 있습니다.

예를 들어, 일반 사용자는 데이터 백업을 한 시간에 한 번만 할 수 있도록 제한하되, 프리미엄 고객에게는 제한을 두지 않는다고 가정해봅시다. 이 경우, `AppServiceProvider`의 `boot` 메서드에서 `RateLimiter`를 다음과 같이 정의할 수 있습니다.

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

위 샘플은 시간 단위로 제한했지만, `perMinute` 메서드를 써서 분 단위로도 제한할 수 있습니다. 또, `by` 메서드에는 어떤 값이든 줄 수 있는데, 일반적으로 고객별로 제한을 세분화할 때 주로 사용합니다.

```php
return Limit::perMinute(50)->by($job->user->id);
```

속도 제한을 정의했다면, 잡 클래스에서 `Illuminate\Queue\Middleware\RateLimited` 미들웨어를 추가해 적용할 수 있습니다. 잡이 제한을 초과할 때마다 미들웨어가 잡을 적합한 딜레이를 적용해 큐로 다시 재진입시킵니다.

```php
use Illuminate\Queue\Middleware\RateLimited;

/**
 * 잡이 거쳐야 할 미들웨어 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited('backups')];
}
```

속도 제한에 의해 큐로 다시 반납된 잡도 시도 횟수(`attempts`)가 증가합니다. 따라서 잡 클래스의 `tries`, `maxExceptions` 속성이나, 또는 [retryUntil 메서드](#time-based-attempts) 등을 상황에 맞게 조정해야 할 수 있습니다.

`releaseAfter` 메서드를 사용하면, 잡이 다시 시도되기 전 대기할 시간을 초 단위로 직접 지정할 수 있습니다.

```php
/**
 * 잡이 거쳐야 할 미들웨어 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new RateLimited('backups'))->releaseAfter(60)];
}
```

속도 제한에 걸렸을 때 잡을 재시도하지 않도록 하려면, `dontRelease` 메서드를 사용할 수 있습니다.

```php
/**
 * 잡이 거쳐야 할 미들웨어 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new RateLimited('backups'))->dontRelease()];
}
```

> [!NOTE]
> Redis를 사용 중이라면, `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어를 사용하는 것이 더 효율적입니다. 이 미들웨어는 Redis에 최적화된 구현을 제공합니다.

<a name="preventing-job-overlaps"></a>
### 잡 중복 실행 방지

라라벨에는 `Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어가 내장되어 있습니다. 이 미들웨어를 사용하면 임의의 키를 기준으로 동일 리소스를 동시에 수정하는 잡의 중복 실행을 손쉽게 막을 수 있습니다.

예를 들어, 사용자의 신용점수 업데이트 잡에서 같은 사용자 ID가 중복 업데이트되는 것을 방지하고 싶다면, 잡의 `middleware` 메서드에서 `WithoutOverlapping` 미들웨어를 반환하면 됩니다.

```php
use Illuminate\Queue\Middleware\WithoutOverlapping;

/**
 * 잡이 거쳐야 할 미들웨어 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new WithoutOverlapping($this->user->id)];
}
```

동일한 타입의 중복 잡은 모두 큐로 다시 반납됩니다. `releaseAfter` 메서드를 이용해, 잡을 다시 시도하기 전 대기할 시간(초)을 지정할 수 있습니다.

```php
/**
 * 잡이 거쳐야 할 미들웨어 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->releaseAfter(60)];
}
```

중복 잡을 바로 삭제해 재시도가 아예 되지 않게 하려면, `dontRelease` 메서드를 사용하면 됩니다.

```php
/**
 * 잡이 거쳐야 할 미들웨어 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->dontRelease()];
}
```

`WithoutOverlapping` 미들웨어는 라라벨의 원자적 락 기능으로 구현되어 있습니다. 잡이 예상치 못하게 실패하거나 타임아웃될 경우, 락이 해제되지 않을 수 있기 때문에, `expireAfter` 메서드로 락이 자동 해제될 시간(초)을 명시적으로 지정해둘 수도 있습니다. 아래 예시에서는 잡 실행 시점 기준으로 3분(180초) 뒤에 락이 해제되게 됩니다.

```php
/**
 * 잡이 거쳐야 할 미들웨어 반환.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->expireAfter(180)];
}
```

> [!WARNING]
> `WithoutOverlapping` 미들웨어는 [락을 지원하는 캐시 드라이버](/docs/12.x/cache#atomic-locks)가 반드시 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버에서만 원자적 락을 지원합니다.

<a name="sharing-lock-keys"></a>

#### 작업 클래스 간의 Lock 키 공유

기본적으로, `WithoutOverlapping` 미들웨어는 동일한 클래스의 중복 실행만을 방지합니다. 즉, 서로 다른 두 작업 클래스가 동일한 lock 키를 사용하더라도 동시에 실행되는 것은 방지하지 않습니다. 그러나 `shared` 메서드를 이용하면 여러 작업 클래스에 걸쳐 lock 키를 공유하도록 라라벨에 지시할 수 있습니다.

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
### 예외 건수 제한(Throttling Exceptions)

라라벨에는 예외 발생 횟수를 제한할 수 있는 `Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어가 포함되어 있습니다. 해당 작업이 지정된 횟수만큼 예외를 발생시키면, 이후의 시도는 설정한 시간 간격이 지날 때까지 지연됩니다. 이 미들웨어는 불안정한 타사 서비스와 상호작용하는 작업에서 특히 유용하게 사용됩니다.

예를 들어, 타사 API와 통신하는 큐 작업에서 예외가 여러 번 발생한다고 가정해보겠습니다. 예외를 제한(Throttle)하고 싶다면, 작업의 `middleware` 메서드에서 `ThrottlesExceptions` 미들웨어를 반환하면 됩니다. 이 미들웨어는 일반적으로 [시간 기반 시도](#time-based-attempts)를 구현한 작업과 함께 사용합니다.

```php
use DateTime;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 작업을 통과해야 하는 미들웨어를 반환합니다.
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

위 예시에서 미들웨어 생성자의 첫 번째 인수는 작업이 제한되기 전에 허용되는 예외 발생 횟수이며, 두 번째 인수는 제한된 이후 작업이 다시 시도될 때까지 대기해야 하는 시간(초)입니다. 예를 들어, 작업이 10번 연속 예외를 발생시키면, 5분(300초) 후에 다시 작업을 시도하며, 최대 30분 안에만 시도합니다.

예외가 발생했지만 예외 임계치에 도달하지 않았다면, 작업은 일반적으로 즉시 다시 시도됩니다. 다만, 미들웨어를 작업에 추가할 때 `backoff` 메서드를 사용하여 지연될 분(minute) 수를 지정할 수도 있습니다.

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 작업을 통과해야 하는 미들웨어를 반환합니다.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 5 * 60))->backoff(5)];
}
```

내부적으로 이 미들웨어는 라라벨의 캐시 시스템을 활용하여 속도 제한(rate limiting)을 구현하며, 작업의 클래스 이름이 캐시 "키"로 사용됩니다. 작업을 미들웨어에 연결할 때 `by` 메서드를 사용하면 이 키를 오버라이드할 수 있습니다. 여러 작업이 동일한 타사 서비스와 상호작용하면서 동일한 제한 "버킷"을 공유하도록 하고 싶을 때 유용합니다.

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 작업을 통과해야 하는 미들웨어를 반환합니다.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->by('key')];
}
```

기본적으로 이 미들웨어는 모든 예외를 제한(throttle)합니다. 만약 특정 조건에서만 예외가 제한되도록 하려면, 미들웨어를 작업에 추가할 때 `when` 메서드를 사용하세요. 이때 제공한 클로저가 `true`를 반환할 때만 예외 제한이 적용됩니다.

```php
use Illuminate\Http\Client\HttpClientException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 작업을 통과해야 하는 미들웨어를 반환합니다.
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

미들웨어에 `report` 메서드를 연결해 제한된 예외가 애플리케이션의 예외 핸들러에 보고되도록 할 수도 있습니다. 이때, 클로저를 전달하면 해당 클로저가 `true`를 반환할 때만 예외가 보고됩니다.

```php
use Illuminate\Http\Client\HttpClientException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 작업을 통과해야 하는 미들웨어를 반환합니다.
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
> Redis를 사용하는 경우, Redis에 최적화되고 더욱 효율적인 `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어를 사용할 수 있습니다.

<a name="skipping-jobs"></a>
### 작업 건너뛰기(Skipping Jobs)

`Skip` 미들웨어를 사용하면 작업의 내부 로직을 별도로 수정하지 않고도 해당 작업을 건너뛰거나 삭제할 수 있습니다. `Skip::when` 메서드는 전달된 조건이 `true`일 때 작업을 삭제하며, `Skip::unless` 메서드는 조건이 `false`일 때 작업을 삭제합니다.

```php
use Illuminate\Queue\Middleware\Skip;

/**
 * 작업을 통과해야 하는 미들웨어를 반환합니다.
 */
public function middleware(): array
{
    return [
        Skip::when($someCondition),
    ];
}
```

보다 복잡한 조건을 평가하려면 `when` 또는 `unless` 메서드에 `Closure`를 전달할 수도 있습니다.

```php
use Illuminate\Queue\Middleware\Skip;

/**
 * 작업을 통과해야 하는 미들웨어를 반환합니다.
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

작업 클래스를 작성한 후에는 해당 작업 클래스에서 `dispatch` 메서드를 사용해 작업을 디스패치할 수 있습니다. `dispatch` 메서드에 전달하는 인수들은 작업 클래스의 생성자로 전달됩니다.

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

작업을 조건에 따라 디스패치하고 싶다면, `dispatchIf` 또는 `dispatchUnless` 메서드를 사용할 수 있습니다.

```php
ProcessPodcast::dispatchIf($accountActive, $podcast);

ProcessPodcast::dispatchUnless($accountSuspended, $podcast);
```

최신 라라벨 애플리케이션에서는 `sync` 드라이버가 기본 큐 드라이버입니다. 이 드라이버는 작업을 현재 요청의 포그라운드에서 동기적으로 실행하므로, 로컬 개발 중에 편리하게 사용할 수 있습니다. 작업을 실제로 백그라운드에서 처리하고 싶다면, 애플리케이션의 `config/queue.php` 설정 파일에서 다른 큐 드라이버를 지정하면 됩니다.

<a name="delayed-dispatching"></a>
### 지연 디스패치(Delayed Dispatching)

작업이 바로 큐 워커에 의해 처리되지 않도록 하고 싶다면, 작업을 디스패치할 때 `delay` 메서드를 사용할 수 있습니다. 예를 들어, 작업이 디스패치된 후 10분이 지나야 처리되도록 할 수도 있습니다.

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

작업에 기본 지연(delay)이 설정되어 있는 경우, 이 지연을 무시하고 즉시 작업을 디스패치하려면 `withoutDelay` 메서드를 사용할 수 있습니다.

```php
ProcessPodcast::dispatch($podcast)->withoutDelay();
```

> [!WARNING]
> Amazon SQS 큐 서비스는 최대 지연 시간이 15분입니다.

<a name="dispatching-after-the-response-is-sent-to-browser"></a>
#### 브라우저 전송 후 디스패치(Dispatching After the Response is Sent to the Browser)

또한, 웹 서버가 FastCGI를 사용할 경우, `dispatchAfterResponse` 메서드는 HTTP 응답이 유저의 브라우저로 전송된 후에 작업을 디스패치합니다. 이렇게 하면 큐의 실행과 상관없이 사용자가 즉시 애플리케이션을 사용할 수 있습니다. 대체로 이메일 발송 등 1초 이내로 끝나는 작업에만 사용하는 것이 좋습니다. 이 방식은 현재 HTTP 요청 내에서 처리되기 때문에, 별도의 큐 워커가 실행되고 있을 필요는 없습니다.

```php
use App\Jobs\SendNotification;

SendNotification::dispatchAfterResponse();
```

또한 클로저를 디스패치한 뒤 `afterResponse` 메서드를 체이닝하여 HTTP 응답 전송 이후에 실행될 클로저를 등록할 수도 있습니다.

```php
use App\Mail\WelcomeMessage;
use Illuminate\Support\Facades\Mail;

dispatch(function () {
    Mail::to('taylor@example.com')->send(new WelcomeMessage);
})->afterResponse();
```

<a name="synchronous-dispatching"></a>
### 동기 디스패치(Synchronous Dispatching)

작업을 즉시(동기적으로) 실행하고 싶다면, `dispatchSync` 메서드를 사용할 수 있습니다. 이 메서드로 디스패치된 작업은 큐에 등록되지 않고, 현재 프로세스에서 즉시 실행됩니다.

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

        // Create podcast...

        ProcessPodcast::dispatchSync($podcast);

        return redirect('/podcasts');
    }
}
```

<a name="jobs-and-database-transactions"></a>
### 작업과 데이터베이스 트랜잭션(Jobs & Database Transactions)

데이터베이스 트랜잭션 내에서 작업을 디스패치하는 것은 아무 문제가 없지만, 작업이 실제로 성공적으로 실행될 수 있도록 각별히 주의해야 합니다. 트랜잭션 내에서 작업을 디스패치하면, 부모 트랜잭션이 커밋되기 전에 워커가 작업을 처리하기 시작할 수 있습니다. 이런 경우, 트랜잭션 중에 모델이나 데이터베이스 레코드에 적용된 변경 내용이 아직 데이터베이스에 반영되지 않았거나, 트랜잭션 내에서 생성한 모델/레코드가 실제로 존재하지 않을 수도 있습니다.

다행히 라라벨은 이 문제를 해결할 수 있는 여러 방법을 제공합니다. 먼저, 큐 연결 설정 배열에 `after_commit` 옵션을 지정할 수 있습니다.

```php
'redis' => [
    'driver' => 'redis',
    // ...
    'after_commit' => true,
],
```

`after_commit` 옵션이 `true`일 때는, 트랜잭션 안에서 작업을 디스패치하더라도, 라라벨은 모든 부모 데이터베이스 트랜잭션이 커밋된 후에 실제로 작업을 디스패치합니다. 물론, 데이터베이스 트랜잭션이 열려 있지 않은 경우에는 작업이 즉시 디스패치됩니다.

만약 트랜잭션 중에 예외로 인해 트랜잭션이 롤백되면, 해당 트랜잭션에서 디스패치된 작업들은 모두 폐기됩니다.

> [!NOTE]
> `after_commit` 설정을 true로 하면, 큐 대기 중인 이벤트 리스너, 메일, 알림, 브로드캐스트 이벤트도 모두 데이터베이스 트랜잭션 커밋 이후 디스패치됩니다.

<a name="specifying-commit-dispatch-behavior-inline"></a>
#### 인라인으로 커밋 후 디스패치 지정하기

큐 연결 설정에서 `after_commit` 옵션을 true로 지정하지 않은 경우, 특정 작업에 한해 모든 데이터베이스 트랜잭션이 커밋된 후에 디스패치하도록 할 수도 있습니다. 이때는 디스패치 작업에 `afterCommit` 메서드를 체이닝하면 됩니다.

```php
use App\Jobs\ProcessPodcast;

ProcessPodcast::dispatch($podcast)->afterCommit();
```

반대로, `after_commit` 옵션이 true로 설정된 경우라면, 특정 작업을 데이터베이스 트랜잭션 커밋을 기다리지 않고 즉시 디스패치하려면 `beforeCommit` 메서드를 사용하면 됩니다.

```php
ProcessPodcast::dispatch($podcast)->beforeCommit();
```

<a name="job-chaining"></a>
### 작업 체이닝(Job Chaining)

작업 체이닝을 사용하면, 메인 작업이 성공적으로 실행된 후에 순차적으로 실행되어야 하는 큐 작업 목록을 지정할 수 있습니다. 체인 내 작업 중 하나라도 실패하면, 나머지 작업은 실행되지 않습니다. 큐 체인을 실행하려면, `Bus` 파사드에서 제공하는 `chain` 메서드를 사용하면 됩니다. 라라벨의 커맨드 버스(Command Bus)는 큐 작업 디스패치의 기반이 되는 하위 컴포넌트입니다.

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

작업 클래스 인스턴스 외에도 체이닝 대상에 클로저를 사용할 수도 있습니다.

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
> 작업 내에서 `$this->delete()` 메서드로 작업을 삭제해도 체인된 다음 작업의 실행이 중단되지 않습니다. 체인은 오직 체인 내의 작업이 실패한 경우에만 실행이 중단됩니다.

<a name="chain-connection-queue"></a>
#### 체인의 연결(Connection) 및 큐(Queue) 지정

체인으로 등록된 작업이 사용할 큐 연결 및 큐 이름을 지정하려면, `onConnection` 및 `onQueue` 메서드를 사용할 수 있습니다. 각각 체인된 작업에 기본으로 사용될 큐 연결/이름을 지정하지만, 작업에 별도로 연결이나 큐가 지정된 경우에는 해당 설정이 우선 적용됩니다.

```php
Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->onConnection('redis')->onQueue('podcasts')->dispatch();
```

<a name="adding-jobs-to-the-chain"></a>
#### 체인에 작업 추가하기

때때로, 기존 작업 체인 내에서 다른 작업을 체인 앞이나 뒤에 추가해야 할 수도 있습니다. 이때는 `prependToChain`과 `appendToChain` 메서드를 사용할 수 있습니다.

```php
/**
 * 작업 실행
 */
public function handle(): void
{
    // ...

    // 현재 체인의 앞에 작업 추가: 현재 작업 다음에 즉시 실행
    $this->prependToChain(new TranscribePodcast);

    // 현재 체인의 끝에 작업 추가: 체인 마지막에 실행
    $this->appendToChain(new TranscribePodcast);
}
```

<a name="chain-failures"></a>
#### 체인 실패(Chain Failures)

체이닝된 작업이 실패한 경우, `catch` 메서드를 사용하여 실패 시 호출될 클로저를 지정할 수 있습니다. 해당 콜백은 작업 실패를 일으킨 `Throwable` 인스턴스를 인수로 받습니다.

```php
use Illuminate\Support\Facades\Bus;
use Throwable;

Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->catch(function (Throwable $e) {
    // 체인 내 작업이 실패함...
})->dispatch();
```

> [!WARNING]
> 체인 콜백은 직렬화되어 나중에 라라벨 큐에 의해 실행되므로, 체인 콜백 내부에서는 `$this` 변수 사용을 피해야 합니다.

<a name="customizing-the-queue-and-connection"></a>
### 큐와 연결(Connection) 커스터마이징

<a name="dispatching-to-a-particular-queue"></a>
#### 특정 큐로 디스패치하기

작업을 서로 다른 큐에 할당하면 큐 작업을 "분류"할 수 있고, 각 큐에 얼마나 많은 워커를 할당할지 조정하여 우선순위를 부여할 수도 있습니다. 이 방법은 큐 설정 파일에 정의된 다른 큐 "연결(connection)"에 작업을 푸시하는 것이 아니라, 하나의 연결 내에서 서로 다른 큐에 작업을 푸시합니다. 특정 큐를 지정하려면 작업을 디스패치할 때 `onQueue` 메서드를 사용하면 됩니다.

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

        // Create podcast...

        ProcessPodcast::dispatch($podcast)->onQueue('processing');

        return redirect('/podcasts');
    }
}
```

또는, 작업 클래스의 생성자에서 `onQueue` 메서드를 호출하여 해당 작업에 큐를 직접 지정할 수도 있습니다.

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    /**
     * 새로운 작업 인스턴스를 생성합니다.
     */
    public function __construct()
    {
        $this->onQueue('processing');
    }
}
```

<a name="dispatching-to-a-particular-connection"></a>
#### 특정 연결(Connection)로 디스패치하기

여러 큐 연결(connection)과 상호작용하는 애플리케이션이라면, 작업을 디스패치할 때 `onConnection` 메서드로 사용할 연결을 지정할 수 있습니다.

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

        // Create podcast...

        ProcessPodcast::dispatch($podcast)->onConnection('sqs');

        return redirect('/podcasts');
    }
}
```

또한, `onConnection`과 `onQueue` 메서드를 체이닝하여 작업의 연결과 큐를 동시에 지정할 수도 있습니다.

```php
ProcessPodcast::dispatch($podcast)
    ->onConnection('sqs')
    ->onQueue('processing');
```

또는, 작업 클래스의 생성자에서 직접 연결을 지정할 수도 있습니다.

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    /**
     * 새로운 작업 인스턴스를 생성합니다.
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

대기열에 등록된 작업 중 하나에서 오류가 발생하는 경우, 해당 작업이 무한히 재시도되는 것을 원치 않을 수 있습니다. 이를 위해 라라벨은 작업을 몇 번 시도할지 또는 얼마 동안 시도할지 지정할 수 있는 다양한 방법을 제공합니다.

작업이 시도될 최대 횟수를 지정하는 한 가지 방법은 Artisan 명령행에서 `--tries` 옵션을 사용하는 것입니다. 이 설정은 워커가 처리하는 모든 작업에 적용되며, 개별 작업에서 시도 횟수를 지정하지 않는 한 전체에 적용됩니다.

```shell
php artisan queue:work --tries=3
```

작업이 최대 시도 횟수를 초과하면, 해당 작업은 "실패한" 작업으로 간주됩니다. 실패한 작업 처리에 관한 자세한 내용은 [실패한 작업 문서](#dealing-with-failed-jobs)를 참고하시기 바랍니다. 만약 `queue:work` 명령어에 `--tries=0`을 지정하면, 작업은 무한정 재시도됩니다.

좀 더 세밀하게, 작업 클래스에서 직접 작업의 최대 시도 횟수를 지정할 수도 있습니다. 작업에 최대 시도 횟수가 지정되어 있으면 이 값이 명령행에서 지정한 `--tries` 값보다 우선 적용됩니다.

```php
<?php

namespace App\Jobs;

class ProcessPodcast implements ShouldQueue
{
    /**
     * 작업이 시도될 수 있는 횟수입니다.
     *
     * @var int
     */
    public $tries = 5;
}
```

특정 작업의 최대 시도 횟수를 동적으로 제어하고 싶을 경우, 작업 클래스에 `tries` 메서드를 정의할 수 있습니다.

```php
/**
 * 작업이 시도될 수 있는 횟수를 반환합니다.
 */
public function tries(): int
{
    return 5;
}
```

<a name="time-based-attempts"></a>
#### 시간 기반 시도 제어

작업이 실패하기 전 시도 횟수를 지정하는 대신, 더 이상 작업을 시도하지 않을 시간을 지정할 수도 있습니다. 이 방식을 사용하면 지정한 시간 내에서 임의의 횟수만큼 시도할 수 있습니다. 작업이 더 이상 시도되지 않을 시간을 지정하려면, 작업 클래스에 `retryUntil` 메서드를 추가하세요. 이 메서드는 `DateTime` 인스턴스를 반환해야 합니다.

```php
use DateTime;

/**
 * 작업이 타임아웃되는 시점을 반환합니다.
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(10);
}
```

> [!NOTE]
> [대기열 이벤트 리스너](/docs/12.x/events#queued-event-listeners)에도 `tries` 속성이나 `retryUntil` 메서드를 정의할 수 있습니다.

<a name="max-exceptions"></a>
#### 최대 예외 횟수

작업이 여러 번 시도되는 것은 허용하지만, `release` 메서드로 직접 해제된 것이 아니라 처리되지 않은 예외가 특정 횟수 발생하면 작업을 실패시키고 싶을 수 있습니다. 이를 위해 작업 클래스에 `maxExceptions` 속성을 정의할 수 있습니다.

```php
<?php

namespace App\Jobs;

use Illuminate\Support\Facades\Redis;

class ProcessPodcast implements ShouldQueue
{
    /**
     * 작업이 시도될 수 있는 횟수입니다.
     *
     * @var int
     */
    public $tries = 25;

    /**
     * 실패로 처리되기 전 허용되는 최대 미처리 예외 횟수입니다.
     *
     * @var int
     */
    public $maxExceptions = 3;

    /**
     * 작업을 실행합니다.
     */
    public function handle(): void
    {
        Redis::throttle('key')->allow(10)->every(60)->then(function () {
            // 락을 획득하여 팟캐스트를 처리합니다...
        }, function () {
            // 락을 획득하지 못했을 때...
            return $this->release(10);
        });
    }
}
```

위의 예제에서, 애플리케이션이 Redis 락을 획득하지 못하면 작업이 10초 동안 해제(release)되고 최대 25회까지 재시도됩니다. 하지만 작업 내부에서 3번의 미처리 예외가 발생하면 해당 작업은 실패로 간주됩니다.

<a name="timeout"></a>
#### 타임아웃

보통 대기열 작업이 어느 정도 시간 내에 처리되길 기대하게 됩니다. 이를 위해 라라벨에서는 "타임아웃" 값을 지정할 수 있습니다. 기본적으로 타임아웃 값은 60초입니다. 만약 작업이 지정된 초(second)보다 오래 실행되면, 작업을 처리하는 워커는 에러와 함께 중단됩니다. 일반적으로, 서버에 설정된 [프로세스 관리 도구](#supervisor-configuration)가 워커를 자동으로 재시작합니다.

작업이 실행될 수 있는 최대 시간(초)은 Artisan 명령행의 `--timeout` 옵션으로 지정할 수 있습니다.

```shell
php artisan queue:work --timeout=30
```

작업이 타임아웃으로 인해 최대 시도 횟수를 초과하게 되면, 해당 작업은 실패로 처리됩니다.

작업 클래스 자체에서 작업이 실행될 수 있는 최대 시간을 지정할 수도 있습니다. 작업에 타임아웃이 지정된 경우, 명령행에서 지정한 어떤 타임아웃 값보다 우선 적용됩니다.

```php
<?php

namespace App\Jobs;

class ProcessPodcast implements ShouldQueue
{
    /**
     * 타임아웃되기 전 작업이 실행될 수 있는 최대 시간(초)입니다.
     *
     * @var int
     */
    public $timeout = 120;
}
```

때때로, 소켓 연결이나 외부 HTTP 요청 등의 IO 차단 프로세스는 지정한 타임아웃을 제대로 준수하지 않을 수 있습니다. 따라서 이런 기능을 사용할 때에는 해당 API에서도 반드시 타임아웃 값을 지정해야 합니다. 예를 들어 Guzzle을 사용하는 경우, 연결 및 요청 타임아웃을 반드시 지정해야 합니다.

> [!WARNING]
> 작업 타임아웃을 지정하려면 `pcntl` PHP 확장 기능이 반드시 설치되어 있어야 합니다. 또한, 작업의 "타임아웃" 값은 ["재시도 대기 시간(retry after)"](#job-expiration) 값보다 항상 작아야 합니다. 그렇지 않으면 작업이 실제로 종료되거나 타임아웃되기 전에 다시 시도될 수 있습니다.

<a name="failing-on-timeout"></a>
#### 타임아웃 시 작업 실패 처리

작업이 타임아웃 되면 해당 작업을 [실패한 작업](#dealing-with-failed-jobs)으로 처리하고 싶다면, 작업 클래스에 `$failOnTimeout` 속성을 정의하세요.

```php
/**
 * 타임아웃 발생 시 작업을 실패로 표시할지 여부입니다.
 *
 * @var bool
 */
public $failOnTimeout = true;
```

<a name="error-handling"></a>
### 에러 처리

작업이 처리되는 도중 예외가 발생하면, 해당 작업은 자동으로 대기열에 재등록되어 다시 시도됩니다. 이 과정은 설정된 최대 시도 횟수에 도달할 때까지 반복됩니다. 최대 시도 횟수는 `queue:work` Artisan 명령어에 사용된 `--tries` 옵션 또는, 작업 클래스 자체에서 지정할 수 있습니다. 대기열 워커 실행에 관한 자세한 정보는 [아래에서 확인하실 수 있습니다](#running-the-queue-worker).

<a name="manually-releasing-a-job"></a>
#### 작업을 수동으로 재등록(Release)하기

때로는 작업을 수동으로 대기열에 다시 등록하여 나중에 다시 시도하고 싶을 수 있습니다. 이 경우 `release` 메서드를 호출하면 됩니다.

```php
/**
 * 작업을 실행합니다.
 */
public function handle(): void
{
    // ...

    $this->release();
}
```

기본적으로 `release` 메서드는 작업을 대기열에 즉시 재등록합니다. 하지만, 처리 대기 시간을 지정하고 싶다면 정수(초)나 날짜 인스턴스를 `release` 메서드에 인자로 전달할 수 있습니다.

```php
$this->release(10);

$this->release(now()->addSeconds(10));
```

<a name="manually-failing-a-job"></a>
#### 작업을 수동으로 실패 처리하기

가끔은 작업을 수동으로 "실패" 상태로 표시해야 할 때가 있습니다. 이럴 때는 `fail` 메서드를 호출하면 됩니다.

```php
/**
 * 작업을 실행합니다.
 */
public function handle(): void
{
    // ...

    $this->fail();
}
```

예외를 감지하여 작업을 실패로 처리하려는 경우, 해당 예외 인스턴스를 `fail` 메서드에 인자로 전달할 수 있습니다. 또는 간편하게 문자열로 에러 메시지를 전달하면, 라라벨이 해당 메시지를 예외로 변환하여 처리합니다.

```php
$this->fail($exception);

$this->fail('Something went wrong.');
```

> [!NOTE]
> 실패한 작업에 대한 자세한 내용은 [작업 실패 처리 문서](#dealing-with-failed-jobs)를 참고하세요.

<a name="job-batching"></a>
## 작업 배치 처리

라라벨의 작업 배치(batch) 기능을 사용하면 여러 개의 작업을 한 번에 실행하고, 모든 작업이 완료된 후 특정 동작을 손쉽게 수행할 수 있습니다. 먼저, 작업 배치의 메타 정보(예: 완료율 등)를 저장할 테이블을 만드는 데이터베이스 마이그레이션을 생성해야 합니다. 이 마이그레이션은 `make:queue-batches-table` Artisan 명령어로 만들 수 있습니다.

```shell
php artisan make:queue-batches-table

php artisan migrate
```

<a name="defining-batchable-jobs"></a>
### 배치 가능한 작업 정의하기

배치로 처리할 작업을 정의하려면 [일반적인 대기열 작업 생성](#creating-jobs)과 동일하지만, 작업 클래스에 `Illuminate\Bus\Batchable` 트레이트를 추가해야 합니다. 이 트레이트는 해당 작업이 어떤 배치에서 실행되고 있는지 확인할 수 있는 `batch` 메서드를 제공합니다.

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
     * 작업을 실행합니다.
     */
    public function handle(): void
    {
        if ($this->batch()->cancelled()) {
            // 배치가 취소되었는지 확인합니다...

            return;
        }

        // CSV 파일의 일부를 가져옵니다...
    }
}
```

<a name="dispatching-batches"></a>
### 배치 작업 디스패치하기

여러 작업을 배치로 디스패치하려면 `Bus` 파사드의 `batch` 메서드를 사용합니다. 보통 배치는 완료 콜백과 함께 사용할 때 가장 유용합니다. 따라서 `then`, `catch`, `finally` 등의 메서드를 사용해 배치 완료 시 실행할 콜백을 정의할 수 있습니다. 각 콜백은 호출 시 `Illuminate\Bus\Batch` 인스턴스를 전달받습니다. 아래 예제에서는 CSV 파일의 일부 줄을 처리하는 작업들을 배치로 큐에 등록하는 상황을 가정합니다.

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
    // 배치가 생성되었으나 아직 작업이 추가되지 않은 상태...
})->progress(function (Batch $batch) {
    // 개별 작업이 하나씩 성공적으로 완료될 때마다...
})->then(function (Batch $batch) {
    // 모든 작업이 성공적으로 완료됨...
})->catch(function (Batch $batch, Throwable $e) {
    // 첫 번째 작업 실패 감지 시 호출됨...
})->finally(function (Batch $batch) {
    // 배치가 모두 실행된 후 호출됨...
})->dispatch();

return $batch->id;
```

배치의 ID는 `$batch->id` 속성을 통해 접근할 수 있으며, 이 ID를 이용해 [라라벨 커맨드 버스에서](#inspecting-batches) 해당 배치 정보를 조회할 수 있습니다.

> [!WARNING]
> 배치 콜백은 직렬화되어 나중에 라라벨 대기열에서 실행되므로 콜백 내에서는 `$this` 변수를 사용하지 마십시오. 또한, 배치 작업은 데이터베이스 트랜잭션 내에서 실행되므로 암묵적으로 커밋을 유발하는 데이터베이스 명령어는 사용하지 않는 것이 좋습니다.

<a name="naming-batches"></a>
#### 배치 이름 지정하기

Laravel Horizon이나 Laravel Telescope와 같은 도구에서는 배치에 이름을 지정하면 더 편리한 디버그 정보를 제공할 수 있습니다. 임의의 이름을 배치에 할당하려면 배치 정의 시 `name` 메서드를 사용하세요.

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // 모든 작업이 성공적으로 완료됨...
})->name('Import CSV')->dispatch();
```

<a name="batch-connection-queue"></a>
#### 배치의 커넥션 및 큐 지정

배치 작업이 사용할 연결(connection)과 큐(queue)를 지정하려면, `onConnection`과 `onQueue` 메서드를 사용할 수 있습니다. 모든 배치 작업은 동일한 연결과 큐에서 실행되어야 합니다.

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // 모든 작업이 성공적으로 완료됨...
})->onConnection('redis')->onQueue('imports')->dispatch();
```

<a name="chains-and-batches"></a>
### 체인과 배치 함께 사용하기

[체인 작업](#job-chaining)을 배열 형태로 배치에 넣어 한 번에 여러 체인을 병렬로 실행하고, 모든 체인이 끝난 뒤 콜백을 실행할 수 있습니다. 예를 들어 두 개의 작업 체인을 병렬로 실행한 뒤, 둘 다 완료되면 후속 동작을 할 수 있습니다.

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

반대로, [체인](#job-chaining) 내에 배치를 정의해 먼저 여러 팟캐스트를 발행하는 배치 작업을 실행한 뒤, 각각에 알림을 보내는 배치 작업을 이어서 실행할 수도 있습니다.

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

어떤 경우에는 배치에 포함된 작업 내부에서 더 많은 작업을 추가하고 싶을 수 있습니다. 이 패턴은 수천 개의 작업을 웹 요청 중에 모두 디스패치하면 과부하가 걸릴 수 있을 때 유용합니다. 대신, "로더(loader)" 작업을 먼저 배치로 등록해 나중에 추가 작업을 적재(hydrate)할 수 있습니다.

```php
$batch = Bus::batch([
    new LoadImportBatch,
    new LoadImportBatch,
    new LoadImportBatch,
])->then(function (Batch $batch) {
    // 모든 작업이 성공적으로 완료됨...
})->name('Import Contacts')->dispatch();
```

이 예제에서는 `LoadImportBatch` 작업을 이용해 배치에 추가 작업을 포함(hydrate)합니다. 이를 위해 작업 내의 `batch` 메서드로 가져온 배치 인스턴스의 `add` 메서드를 사용할 수 있습니다.

```php
use App\Jobs\ImportContacts;
use Illuminate\Support\Collection;

/**
 * 작업을 실행합니다.
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
> 같은 배치에 포함된 작업 내부에서만 배치에 작업을 추가할 수 있습니다.

<a name="inspecting-batches"></a>
### 배치 조회하기

배치 완료 콜백에 전달된 `Illuminate\Bus\Batch` 인스턴스는 배치 작업과 상호작용하고, 정보를 확인하는 다양한 속성과 메서드를 제공합니다.

```php
// 배치의 UUID...
$batch->id;

// 배치 이름(지정된 경우)...
$batch->name;

// 배치에 할당된 작업 수...
$batch->totalJobs;

// 아직 대기열에서 처리되지 않은 작업 수...
$batch->pendingJobs;

// 실패한 작업 수...
$batch->failedJobs;

// 현재까지 처리된 작업 수...
$batch->processedJobs();

// 배치의 완료 진행률(0-100)...
$batch->progress();

// 배치 실행이 끝났는지 여부...
$batch->finished();

// 배치 실행을 취소합니다...
$batch->cancel();

// 배치가 취소되었는지 여부...
$batch->cancelled();
```

<a name="returning-batches-from-routes"></a>
#### 라우트에서 배치 반환하기

모든 `Illuminate\Bus\Batch` 인스턴스는 JSON 직렬화가 가능하므로, 애플리케이션 라우트에서 직접 반환하여 해당 배치 정보(진행률 등)를 담은 JSON 데이터를 얻을 수 있습니다. 이를 통해 애플리케이션 UI에서 배치의 진행상황을 쉽게 시각화할 수 있습니다.

배치 ID로 배치를 조회하려면 `Bus` 파사드의 `findBatch` 메서드를 사용하세요.

```php
use Illuminate\Support\Facades\Bus;
use Illuminate\Support\Facades\Route;

Route::get('/batch/{batchId}', function (string $batchId) {
    return Bus::findBatch($batchId);
});
```

<a name="cancelling-batches"></a>
### 배치 취소하기

특정 배치의 실행을 취소해야 할 때는 `Illuminate\Bus\Batch` 인스턴스의 `cancel` 메서드를 호출하면 됩니다.

```php
/**
 * 작업을 실행합니다.
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

앞선 예제들에서 볼 수 있듯, 배치 작업을 실행할 때는 일반적으로 해당 배치가 취소되었는지 확인해야 합니다. 하지만 보다 간결하게 처리하고 싶다면, 해당 작업에 `SkipIfBatchCancelled` [미들웨어](#job-middleware)를 할당할 수 있습니다. 이 미들웨어를 사용하면, 배치가 취소된 경우 작업이 실행되지 않습니다.

```php
use Illuminate\Queue\Middleware\SkipIfBatchCancelled;

/**
 * 이 작업에 적용할 미들웨어를 반환합니다.
 */
public function middleware(): array
{
    return [new SkipIfBatchCancelled];
}
```

<a name="batch-failures"></a>
### 배치 실패 처리

배치에 포함된 작업 중 하나가 실패하면, `catch` 콜백(정의되어 있다면)이 호출됩니다. 이 콜백은 배치 내에서 처음 실패한 작업에 대해서만 실행됩니다.

<a name="allowing-failures"></a>
#### 작업 실패 시 배치 취소 방지

배치 내 작업이 실패하면, 라라벨은 자동으로 해당 배치를 "취소됨" 상태로 표시합니다. 이 동작을 원치 않는 경우, 작업 실패 시 자동으로 배치가 취소되지 않도록 할 수 있습니다. 배치를 디스패치할 때 `allowFailures` 메서드를 호출하면 됩니다.

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // 모든 작업이 성공적으로 완료됨...
})->allowFailures()->dispatch();
```

<a name="retrying-failed-batch-jobs"></a>
#### 실패한 배치 작업 재시도

편의상, 라라벨은 특정 배치에서 실패한 모든 작업을 쉽게 재시도할 수 있는 `queue:retry-batch` Artisan 명령어를 제공합니다. 이 명령어는 재시도할 실패 작업들을 포함하는 배치의 UUID를 인자로 받습니다.

```shell
php artisan queue:retry-batch 32dbc76c-4f82-4749-b610-a639fe0099b5
```

<a name="pruning-batches"></a>
### 배치 데이터 정리(Pruning)

정리를 하지 않으면 `job_batches` 테이블에 레코드가 매우 빠르게 쌓일 수 있습니다. 이를 방지하려면 [스케줄러](/docs/12.x/scheduling)로 `queue:prune-batches` Artisan 명령어를 매일 실행하도록 예약하세요.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches')->daily();
```

기본적으로, 완료된 지 24시간 이상 지난 모든 배치가 자동으로 정리(prune)됩니다. 명령어 호출 시 `hours` 옵션을 사용해 배치 데이터를 얼마 동안 보관할지 지정할 수 있습니다. 예를 들어 아래 명령은 48시간 이상 지난 배치를 모두 삭제합니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48')->daily();
```

경우에 따라 작업이 실패하고 재시도되지 않아 영원히 미완료로 남은 배치 기록이 테이블에 쌓일 수 있습니다. 이런 미완료 배치도 `unfinished` 옵션을 사용하여 정리하도록 지정할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48 --unfinished=72')->daily();
```

마찬가지로, 취소된 배치 기록도 누적될 수 있으므로 `cancelled` 옵션을 이용해 이들 역시 정리할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48 --cancelled=72')->daily();
```

<a name="storing-batches-in-dynamodb"></a>

### DynamoDB에 배치 정보 저장하기

라라벨은 배치 메타 정보를 관계형 데이터베이스 대신 [DynamoDB](https://aws.amazon.com/dynamodb)에 저장하는 것도 지원합니다. 하지만, 모든 배치 레코드를 저장할 DynamoDB 테이블을 직접 생성해야 합니다.

일반적으로 이 테이블의 이름은 `job_batches`로 설정하는 것이 좋으나, 실제로는 애플리케이션의 `queue` 설정 파일 내 `queue.batching.table` 설정값에 따라 이름을 정해야 합니다.

<a name="dynamodb-batch-table-configuration"></a>
#### DynamoDB 배치 테이블 설정

`job_batches` 테이블은 문자열 타입의 파티션 프라이머리 키 `application`과 문자열 타입의 소트 프라이머리 키 `id`를 가져야 합니다. 이 중 `application` 키에는 애플리케이션의 `app` 설정 파일 내 `name` 설정값이 들어갑니다. 애플리케이션 이름이 DynamoDB 테이블 키의 일부이기 때문에, 여러 개의 라라벨 애플리케이션의 작업 배치 기록을 하나의 테이블에 저장할 수 있습니다.

또한, [자동 배치 삭제 기능](#pruning-batches-in-dynamodb)을 활용하려면, 테이블에 `ttl` 속성을 지정할 수도 있습니다.

<a name="dynamodb-configuration"></a>
#### DynamoDB 설정

다음으로, 라라벨 애플리케이션이 Amazon DynamoDB와 통신할 수 있도록 AWS SDK를 설치해야 합니다.

```shell
composer require aws/aws-sdk-php
```

그런 다음, `queue.batching.driver` 설정 값을 `dynamodb`로 변경합니다. 그리고 `batching` 설정 배열 내에 `key`, `secret`, `region` 설정 항목을 정의해야 합니다. 이 값들은 AWS 인증에 사용됩니다. `dynamodb` 드라이버를 사용할 때는 `queue.batching.database` 설정 항목은 필요하지 않습니다.

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
#### DynamoDB에서 배치 레코드 정리(Pruning)

작업 배치 정보를 [DynamoDB](https://aws.amazon.com/dynamodb)에 저장할 때는, 관계형 데이터베이스에 저장된 배치들을 정리하는 데 사용되는 일반적인 프루닝(pruning) 명령어를 사용할 수 없습니다. 대신, [DynamoDB의 자체 TTL(Timel to Live) 기능](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html)을 활용해 오래된 배치 레코드를 자동으로 삭제할 수 있습니다.

DynamoDB 테이블에 `ttl` 속성을 정의했다면, 라라벨이 배치 레코드를 어떻게 정리할 것인지 설정값을 지정할 수 있습니다. `queue.batching.ttl_attribute` 설정값은 TTL을 저장하는 속성의 이름을, `queue.batching.ttl` 값은 마지막으로 기록이 업데이트되고 난 뒤 몇 초 후에 해당 배치 레코드를 DynamoDB 테이블에서 삭제할 수 있는지를 지정합니다.

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
## 클로저(Closure) 큐잉하기

작업(Job) 클래스를 큐에 디스패치하는 대신, 클로저(익명 함수)를 큐에 디스패치할 수도 있습니다. 이 방식은 현재 요청 사이클에서 벗어나 간단한 일을 빠르게 처리하고 싶을 때 유용합니다. 클로저를 큐에 디스패치할 때는, 해당 클로저의 코드 내용이 암호화 서명되어 전송 중에 변조될 수 없습니다.

```php
$podcast = App\Podcast::find(1);

dispatch(function () use ($podcast) {
    $podcast->publish();
});
```

큐에 등록한 클로저에 이름을 지정하고 싶다면, `name` 메서드를 사용할 수 있습니다. 이렇게 하면 큐 모니터링 대시보드나 `queue:work` 명령어 실행 시 지정한 이름이 표시됩니다.

```php
dispatch(function () {
    // ...
})->name('Publish Podcast');
```

또한 `catch` 메서드를 사용하면, 클로저가 큐에서 실행될 때 모든 [설정된 재시도 횟수](#max-job-attempts-and-timeout)가 소진된 뒤에도 성공적으로 완료되지 않았을 경우 실행될 클로저를 지정할 수 있습니다.

```php
use Throwable;

dispatch(function () use ($podcast) {
    $podcast->publish();
})->catch(function (Throwable $e) {
    // 이 작업은 실패했습니다...
});
```

> [!WARNING]
> `catch` 콜백은 직렬화되어 나중에 라라벨 큐에 의해 실행되므로, `catch` 콜백 내부에서 `$this` 변수를 사용해서는 안 됩니다.

<a name="running-the-queue-worker"></a>
## 큐 워커(Queue Worker) 실행하기

<a name="the-queue-work-command"></a>
### `queue:work` 명령어

라라벨에는 큐 워커를 실행하여 큐에 새로 추가된 작업을 처리하는 Artisan 명령어가 내장되어 있습니다. `queue:work` Artisan 명령어를 사용해 워커를 실행할 수 있습니다. 한 번 실행하면, 워커는 수동으로 중지시키거나 터미널을 닫을 때까지 계속해서 실행됩니다.

```shell
php artisan queue:work
```

> [!NOTE]
> `queue:work` 프로세스를 백그라운드에서 항상 실행되게 하려면, [Supervisor](#supervisor-configuration)와 같은 프로세스 모니터를 사용하여 큐 워커가 중지되지 않게 관리하는 것이 좋습니다.

`queue:work` 명령어를 실행할 때 `-v` 플래그를 붙이면, 처리된 작업 ID를 커맨드 출력에 포함시킬 수 있습니다.

```shell
php artisan queue:work -v
```

큐 워커는 오랜 시간 실행되는 프로세스이며, 기동(boot)된 애플리케이션 상태를 메모리에 저장합니다. 그 결과, 워커가 시작된 이후 코드가 변경되어도 이를 자동으로 인지하지 못합니다. 따라서, 배포(deployment) 과정에서는 반드시 [큐 워커를 재시작](#queue-workers-and-deployment)해야 합니다. 또, 애플리케이션에서 생성하거나 수정한 모든 정적(static) 상태는 작업 간에 자동으로 초기화되지 않는다는 점도 기억해야 합니다.

대안으로, `queue:listen` 명령어를 사용할 수도 있습니다. 이 명령어를 사용하면 코드가 변경되었거나 애플리케이션 상태를 리셋해야 할 때 워커를 수동으로 다시 시작할 필요가 없습니다. 그러나 이 명령어는 `queue:work` 명령어에 비해 성능이 낮습니다.

```shell
php artisan queue:listen
```

<a name="running-multiple-queue-workers"></a>
#### 여러 큐 워커 실행하기

한 큐에 여러 워커를 할당하여 동시 처리하고자 한다면, 단순히 여러 개의 `queue:work` 프로세스를 실행하면 됩니다. 이는 터미널에서 여러 탭을 열어 실행하거나, 프로덕션 환경에서는 프로세스 매니저의 설정을 통해 할 수 있습니다. [Supervisor를 사용할 때](#supervisor-configuration)는 `numprocs` 설정 값을 활용하면 됩니다.

<a name="specifying-the-connection-queue"></a>
#### 연결 및 큐 선택

워커가 사용할 특정 큐 연결을 지정할 수도 있습니다. `work` 명령어에 전달한 연결 이름은 `config/queue.php` 설정 파일에 정의된 연결 중 하나여야 합니다.

```shell
php artisan queue:work redis
```

기본적으로 `queue:work` 명령어는 해당 연결의 기본 큐에서만 작업을 처리합니다. 하지만, 더 세부적으로 워커가 특정 큐만 처리하게 하고 싶다면, 큐 이름을 지정할 수 있습니다. 예를 들어, 모든 이메일 작업이 `redis` 연결의 `emails` 큐에 쌓이고 있다면, 아래와 같이 해당 큐만 처리하는 워커를 실행할 수 있습니다.

```shell
php artisan queue:work redis --queue=emails
```

<a name="processing-a-specified-number-of-jobs"></a>
#### 특정 개수의 작업만 처리하기

`--once` 옵션을 사용하면 워커가 큐에서 단 하나의 작업만 처리하도록 할 수 있습니다.

```shell
php artisan queue:work --once
```

`--max-jobs` 옵션을 사용하면 워커가 지정된 개수만큼 작업을 처리한 뒤 종료되도록 할 수 있습니다. 이 옵션은 [Supervisor](#supervisor-configuration)와 결합해 사용할 때, 워커가 일정 개수의 작업을 처리하고 누적된 메모리를 해제하며 자동으로 재시작되도록 설정하는 데 유용합니다.

```shell
php artisan queue:work --max-jobs=1000
```

<a name="processing-all-queued-jobs-then-exiting"></a>
#### 큐에 쌓인 모든 작업 처리 후 종료하기

`--stop-when-empty` 옵션을 사용하면, 워커가 큐의 모든 작업을 처리한 후 정상적으로 종료되도록 할 수 있습니다. 이 옵션은 Docker 컨테이너 내에서 라라벨 큐를 처리할 때 큐가 비면 컨테이너를 종료하고 싶은 경우 유용합니다.

```shell
php artisan queue:work --stop-when-empty
```

<a name="processing-jobs-for-a-given-number-of-seconds"></a>
#### 특정 시간 동안만 작업 처리하기

`--max-time` 옵션을 사용하면 워커가 지정한 초 수 동안 작업을 처리한 뒤 종료하도록 할 수 있습니다. 이 옵션 역시 [Supervisor](#supervisor-configuration)와 함께 활용하면 워커가 일정 시간마다 자동으로 재시작되어 누적된 메모리가 해제됩니다.

```shell
# 한 시간 동안 작업을 처리한 후 종료...
php artisan queue:work --max-time=3600
```

<a name="worker-sleep-duration"></a>
#### 워커 대기(sleep) 시간

작업이 큐에 있으면, 워커는 작업들 사이에 지체 없이 계속해서 처리합니다. 반면, 작업이 없을 때는 `sleep` 옵션만큼(초 단위) 대기한 뒤 다시 큐를 확인합니다. 대기 중에는 새로운 작업이 있어도 즉시 처리하지 않습니다.

```shell
php artisan queue:work --sleep=3
```

<a name="maintenance-mode-queues"></a>
#### 유지보수 모드와 큐

애플리케이션이 [유지보수 모드](/docs/12.x/configuration#maintenance-mode)인 동안 큐에 쌓인 작업은 처리되지 않습니다. 애플리케이션이 유지보수 모드를 벗어나면 작업이 정상적으로 처리됩니다.

유지보수 모드임에도 불구하고 큐 워커가 작업을 처리하게 하려면, `--force` 옵션을 사용할 수 있습니다.

```shell
php artisan queue:work --force
```

<a name="resource-considerations"></a>
#### 리소스 사용 주의사항

데몬 큐 워커는 각 작업을 처리할 때마다 프레임워크를 "재부팅"(재시작)하지 않습니다. 따라서 각 작업이 끝날 때마다 무거운 리소스를 적절히 해제해야 합니다. 예를 들어 GD 라이브러리를 이용해 이미지 처리를 했을 경우, 작업이 끝난 뒤에는 `imagedestroy` 등을 이용해 메모리를 해제해주어야 합니다.

<a name="queue-priorities"></a>
### 큐 우선순위

때때로 큐가 처리되는 순서를 우선순위별로 지정하고 싶을 때가 있습니다. 예를 들어 `config/queue.php`의 `redis` 연결 기본 `queue`를 `low`로 설정할 수 있습니다. 하지만 특정 작업을 높은 우선순위의 큐(`high`와 같은)로 보내고 싶다면 다음과 같이 할 수 있습니다.

```php
dispatch((new Job)->onQueue('high'));
```

그리고 모든 `high` 큐 작업이 우선적으로 처리된 뒤에 `low` 큐의 작업을 처리하도록 하려면, 워커 실행 시 큐 이름을 콤마로 구분하여 지정하면 됩니다.

```shell
php artisan queue:work --queue=high,low
```

<a name="queue-workers-and-deployment"></a>
### 큐 워커와 배포(Deployment)

큐 워커는 오랜 시간 실행되는 프로세스이므로, 코드가 변경되어도 자동으로 반영되지 않습니다. 따라서, 배포 시에는 워커를 재시작하는 것이 가장 간단하고 확실한 방법입니다. `queue:restart` 명령어로 모든 워커를 안전하게 재시작할 수 있습니다.

```shell
php artisan queue:restart
```

이 명령어를 실행하면, 각 큐 워커는 현재 진행 중인 작업이 끝나면 안전하게 종료하라는 신호를 받게 되고, 처리중인 작업이 유실되지 않게 합니다. `queue:restart` 명령어 실행 후 워커가 종료되므로, [Supervisor](#supervisor-configuration)와 같은 프로세스 관리자를 사용하여 워커가 자동으로 재시작되게 해야 합니다.

> [!NOTE]
> 큐는 [캐시](/docs/12.x/cache)를 사용해 재시작 신호 상태를 저장하므로, 이 기능을 사용하기 전에 애플리케이션에 적절한 캐시 드라이버가 구성되어 있는지 확인하세요.

<a name="job-expirations-and-timeouts"></a>
### 작업 만료 및 타임아웃

<a name="job-expiration"></a>
#### 작업 만료

`config/queue.php`의 각 큐 연결 설정에는 `retry_after` 옵션이 있습니다. 이 값은 작업이 처리되는 동안 이 시간이 초과되었을 때, 작업을 다시 큐에 넣을지 결정합니다. 예를 들어, `retry_after`가 90으로 설정되어 있다면, 작업이 90초 동안 처리되고 있으나 여전히 완료되지 않은 경우 작업이 큐에 다시 방출됩니다. 보통, 이 값은 작업이 합리적으로 완료될 것이라 기대되는 최대 소요 시간으로 설정해야 합니다.

> [!WARNING]
> Amazon SQS 연결만 `retry_after` 값을 가지지 않습니다. SQS는 [기본 가시성 타임아웃(Default Visibility Timeout)](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/AboutVT.html) 방식으로 처리하며, 이는 AWS 콘솔 내에서 관리됩니다.

<a name="worker-timeouts"></a>
#### 워커 타임아웃

`queue:work` Artisan 명령어는 `--timeout` 옵션을 제공합니다. 기본값은 60초입니다. 만약 작업 처리 시간이 지정한 `--timeout` 값을 초과하면, 작업을 처리하는 워커는 오류와 함께 종료됩니다. 일반적으로 서버에 [Supervisor 등 프로세스 관리자를 구성](#supervisor-configuration)해두면 자동으로 다시 시작됩니다.

```shell
php artisan queue:work --timeout=60
```

`retry_after` 설정값과 CLI의 `--timeout` 옵션은 서로 다르지만, 함께 사용하여 작업이 유실되지 않으면서도 한 번만 성공적으로 처리되도록 보장합니다.

> [!WARNING]
> `--timeout` 값은 항상 `retry_after` 설정 값보다 몇 초는 더 짧게 설정해야 합니다. 그래야 정지된 작업을 처리 중인 워커가 작업을 재시작하기 전에 항상 종료될 수 있습니다. 만약 `--timeout`이 `retry_after`보다 길면, 작업이 두 번 처리될 수도 있습니다.

<a name="supervisor-configuration"></a>
## Supervisor 설정

프로덕션 환경에서는 `queue:work` 프로세스가 항상 실행 중이어야 합니다. `queue:work` 프로세스가 중지되는 원인은 다양하며, 워커 타임아웃 초과나, `queue:restart` 명령 실행 등 여러 가지가 있습니다.

이러한 이유로, 큐 워커 프로세스가 종료되었을 때를 감지해 자동으로 재시작할 수 있는 프로세스 모니터를 설정해야 합니다. 프로세스 모니터는 동시에 몇 개의 `queue:work` 프로세스를 실행할지 지정할 수도 있습니다. Supervisor는 리눅스 환경에서 많이 사용되는 대표적인 프로세스 모니터이며, 아래에서 Supervisor 설정 방법에 대해 설명합니다.

<a name="installing-supervisor"></a>
#### Supervisor 설치하기

Supervisor는 리눅스 운영체제용 프로세스 모니터입니다. 만약 워커 프로세스가 실패하면 자동으로 다시 실행해줍니다. Ubuntu에서는 아래와 같이 Supervisor를 설치할 수 있습니다.

```shell
sudo apt-get install supervisor
```

> [!NOTE]
> Supervisor 설치 및 관리를 직접 하는 것이 부담스럽게 느껴진다면, [Laravel Cloud](https://cloud.laravel.com)를 이용하는 것도 고려해보세요. 라라벨 클라우드는 라라벨 큐 워커 실행까지 완전히 관리해주는 플랫폼입니다.

<a name="configuring-supervisor"></a>
#### Supervisor 설정하기

Supervisor 설정 파일은 대체로 `/etc/supervisor/conf.d` 디렉토리에 저장됩니다. 이 디렉토리 안에서 원하는 대로 여러 개의 설정 파일을 만들어, Supervisor가 워커 프로세스를 어떻게 관리해야 할지 지정할 수 있습니다. 예를 들어, `laravel-worker.conf` 파일을 만들어 `queue:work` 프로세스 실행 및 모니터링을 설정해보겠습니다.

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

이 예시에서 `numprocs` 설정은 Supervisor가 8개의 `queue:work` 프로세스를 실행하고, 모두 모니터링하면서 실패 시 자동으로 다시 시작하게 합니다. 각자 실행할 연결이나 옵션은 `command` 설정 값을 자신의 환경에 맞게 바꿔야 합니다.

> [!WARNING]
> `stopwaitsecs` 값은 가장 오래 걸리는 작업의 소요 시간보다 커야 합니다. 그렇지 않으면 Supervisor가 작업이 끝나기 전에 프로세스를 강제로 종료해버릴 수 있습니다.

<a name="starting-supervisor"></a>
#### Supervisor 실행하기

설정 파일을 만들었으면, 다음 명령어로 Supervisor 설정을 갱신하고, 프로세스를 시작할 수 있습니다.

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start "laravel-worker:*"
```

Supervisor에 대한 더 많은 정보는 [Supervisor 공식 문서](http://supervisord.org/index.html)를 참고하세요.

<a name="dealing-with-failed-jobs"></a>
## 실패한 작업(잡) 처리하기

큐에 넣은 작업이 실패하는 경우도 종종 생깁니다. 걱정하지 마세요! 라라벨에서는 [작업 최대 시도 횟수 지정](#max-job-attempts-and-timeout) 등, 실패한 작업 관리를 위한 다양한 방법을 제공합니다. 비동기 작업이 정해진 시도 횟수를 모두 초과하면, 해당 작업이 `failed_jobs` 데이터베이스 테이블에 저장됩니다. [동기(Synchronous)로 디스패치한 작업](/docs/12.x/queues#synchronous-dispatching)이 실패한 경우에는 이 테이블에 저장되지 않고, 발생한 예외가 애플리케이션에 즉시 전달되어 처리됩니다.

새로운 라라벨 애플리케이션에는 대개 `failed_jobs` 테이블을 생성하는 마이그레이션 파일이 포함되어 있습니다. 만약 애플리케이션에 이 테이블 마이그레이션이 없다면, `make:queue-failed-table` 명령으로 생성할 수 있습니다.

```shell
php artisan make:queue-failed-table

php artisan migrate
```

[큐 워커](#running-the-queue-worker) 실행 시, `queue:work` 명령어의 `--tries` 옵션으로 작업별 최대 재시도 횟수를 지정할 수 있습니다. 값을 지정하지 않으면 한 번만 시도되거나, 작업 클래스 내 `$tries` 속성에 정의된 횟수만큼 시도됩니다.

```shell
php artisan queue:work redis --tries=3
```

`--backoff` 옵션을 사용하면, 예외가 발생해 작업을 다시 시도하기 전에 라라벨이 몇 초를 대기해야 할지 지정할 수 있습니다. 기본적으로는 바로 큐에 다시 방출되어 즉시 재시도됩니다.

```shell
php artisan queue:work redis --tries=3 --backoff=3
```

개별 작업 클래스에서 재시도 전 대기 시간을 세부적으로 제어하고 싶다면, Job 클래스에 `backoff` 속성을 추가할 수 있습니다.

```php
/**
 * 작업을 재시도하기 전에 대기할 시간(초)
 *
 * @var int
 */
public $backoff = 3;
```

좀 더 복잡한 로직이 필요하다면, `backoff` 메서드를 정의해 원하는 만큼 동적으로 반환할 수 있습니다.

```php
/**
 * 작업 재시도 전 대기 시간(초)을 계산합니다.
 */
public function backoff(): int
{
    return 3;
}
```

"지수적(backoff)" 대기 시간을 구현하고 싶다면, `backoff` 메서드에서 값의 배열을 반환하면 됩니다. 아래 예시에서는 처음 재시도는 1초, 두 번째는 5초, 세 번째 이후부터는 10초씩 대기합니다.

```php
/**
 * 작업 재시도 전 대기 시간(초) 계산
 *
 * @return array<int, int>
 */
public function backoff(): array
{
    return [1, 5, 10];
}
```

<a name="cleaning-up-after-failed-jobs"></a>
### 실패한 작업 후 처리(Cleanup)

특정 작업이 실패하면, 사용자에게 알림을 보내거나 작업 중 일부만 완료된 내용을 원상복구하고 싶을 수 있습니다. 이를 위해서는 작업 클래스에 `failed` 메서드를 정의할 수 있습니다. 작업이 실패한 원인이 되는 `Throwable` 인스턴스가 `failed` 메서드로 전달됩니다.

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
     * 새 작업 인스턴스 생성자
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
     * 작업 실패 처리
     */
    public function failed(?Throwable $exception): void
    {
        // 실패 알림 전송 등...
    }
}
```

> [!WARNING]
> `failed` 메서드가 호출되기 전에 새로운 작업 인스턴스가 생성되므로, 만약 `handle` 메서드에서 클래스 속성을 변경했다면 해당 변경사항은 손실됩니다.

<a name="retrying-failed-jobs"></a>
### 실패한 작업 재시도

`failed_jobs` 데이터베이스 테이블에 저장된 실패한 작업을 모두 확인하려면, `queue:failed` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan queue:failed
```

`queue:failed` 명령어를 실행하면 작업 ID, 연결, 큐, 실패 시간 등 작업에 대한 정보가 출력됩니다. 작업 ID를 사용해 해당 실패한 작업만 선택적으로 다시 시도할 수 있습니다. 예를 들어, 작업 ID가 `ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece`인 실패 작업을 재시도하려면 아래와 같이 실행합니다.

```shell
php artisan queue:retry ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece
```

필요하다면 여러 ID를 한 번에 전달할 수도 있습니다.

```shell
php artisan queue:retry ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece 91401d2c-0784-4f43-824c-34f94a33c24d
```

특정 큐의 실패한 작업만 재시도하려면 다음과 같이 실행하세요.

```shell
php artisan queue:retry --queue=name
```

실패한 모든 작업을 한 번에 재시도하려면, ID 대신 `all`을 전달하면 됩니다.

```shell
php artisan queue:retry all
```

실패한 작업을 삭제하고 싶다면, `queue:forget` 명령을 사용할 수 있습니다.

```shell
php artisan queue:forget 91401d2c-0784-4f43-824c-34f94a33c24d
```

> [!NOTE]
> [Horizon](/docs/12.x/horizon)을 사용할 경우, 실패한 작업을 삭제할 때는 `queue:forget` 대신 `horizon:forget` 명령을 사용해야 합니다.

`failed_jobs` 테이블의 모든 실패한 작업을 삭제하려면, `queue:flush` 명령어를 사용하세요.

```shell
php artisan queue:flush
```

<a name="ignoring-missing-models"></a>
### 존재하지 않는 모델 무시하기

Eloquent 모델을 작업에 주입하면, 해당 모델 정보가 큐에 들어가기 전에 직렬화되고, 작업이 처리될 때 다시 데이터베이스에서 불러옵니다. 하지만, 작업이 처리되기 전 해당 모델이 이미 삭제되었다면, `ModelNotFoundException` 예외가 발생해 작업이 실패할 수 있습니다.

이때, 작업 클래스의 `deleteWhenMissingModels` 속성을 `true`로 지정하면, 모델이 존재하지 않는 작업은 예외를 발생시키지 않고 조용히 삭제됩니다.

```php
/**
 * 모델이 더 이상 존재하지 않으면 작업을 삭제합니다.
 *
 * @var bool
 */
public $deleteWhenMissingModels = true;
```

<a name="pruning-failed-jobs"></a>
### 실패한 작업 레코드 정리(Pruning)

애플리케이션의 `failed_jobs` 테이블에서 실패한 작업 기록을 정리하려면, `queue:prune-failed` Artisan 명령어를 실행하면 됩니다.

```shell
php artisan queue:prune-failed
```

기본적으로, 24시간 이상 지난 모든 실패 작업 레코드가 삭제됩니다. 만약 커맨드에 `--hours` 옵션을 지정하면, 최근 N시간 이내에 등록된 작업만 남기고 나머지는 삭제됩니다. 예를 들어, 아래 명령어는 48시간 이상된 모든 실패 작업 레코드를 삭제합니다.

```shell
php artisan queue:prune-failed --hours=48
```

<a name="storing-failed-jobs-in-dynamodb"></a>
### 실패한 작업을 DynamoDB에 저장하기

라라벨은 실패한 작업 기록 또한 [DynamoDB](https://aws.amazon.com/dynamodb)에 저장하는 기능을 제공합니다. 다만, 모든 실패 작업 레코드를 저장할 DynamoDB 테이블을 수동으로 생성해야 합니다. 이 테이블의 이름은 일반적으로 `failed_jobs`를 사용하지만, 실제 이름은 애플리케이션의 `queue` 설정 파일 내 `queue.failed.table` 설정값에 맞춰야 합니다.

`failed_jobs` 테이블은 문자열 타입의 파티션 프라이머리 키 `application`과 문자열 타입의 소트 프라이머리 키 `uuid`를 가져야 합니다. 여기서 `application` 키에는 애플리케이션의 `app` 설정 파일 내 `name` 항목 값이 들어갑니다. 애플리케이션 이름이 키의 일부이므로, 여러 개의 라라벨 앱 실패 작업을 하나의 테이블에서 관리할 수 있습니다.

또한, 라라벨이 Amazon DynamoDB와 통신할 수 있도록 AWS SDK도 설치해야 합니다.

```shell
composer require aws/aws-sdk-php
```

그리고 `queue.failed.driver` 설정 값을 `dynamodb`로, 인증에 사용할 `key`, `secret`, `region` 등도 함께 설정합니다. 이 때, `dynamodb` 드라이버 사용 시 `queue.failed.database` 옵션은 불필요합니다.

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

실패한 작업을 보관하지 않고 바로 삭제하려면, `queue.failed.driver` 값을 `null`로 지정하면 됩니다. 대부분의 경우 환경 변수 `QUEUE_FAILED_DRIVER`를 통해 설정할 수 있습니다.

```ini
QUEUE_FAILED_DRIVER=null
```

<a name="failed-job-events"></a>
### 실패한 작업 이벤트 처리

작업이 실패할 때 실행되는 이벤트 리스너를 등록하고 싶다면, `Queue` 파사드의 `failing` 메서드를 사용하면 됩니다. 예를 들어, 라라벨의 `AppServiceProvider`에서 `boot` 메서드를 통해 아래처럼 클로저를 이벤트로 연결할 수 있습니다.

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Queue;
use Illuminate\Support\ServiceProvider;
use Illuminate\Queue\Events\JobFailed;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 필요한 서비스 등록
     */
    public function register(): void
    {
        // ...
    }

    /**
     * 서비스 부트스트랩
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
> [Horizon](/docs/12.x/horizon)을 사용하는 경우, `queue:clear` 명령어 대신 `horizon:clear` 명령어를 사용해서 큐의 작업을 삭제해야 합니다.

기본 연결의 기본 큐에 있는 모든 작업을 삭제하려면 `queue:clear` 아티즌 명령어를 사용할 수 있습니다.

```shell
php artisan queue:clear
```

특정 연결과 큐의 작업만 삭제하고 싶다면, `connection` 인수와 `queue` 옵션을 함께 지정할 수 있습니다.

```shell
php artisan queue:clear redis --queue=emails
```

> [!WARNING]
> 큐에서 작업을 삭제하는 기능은 SQS, Redis, 데이터베이스 큐 드라이버에서만 사용할 수 있습니다. 또한 SQS의 메시지 삭제 과정은 최대 60초가 소요될 수 있으므로, 큐를 비운 직후 60초 이내에 SQS 큐로 전송된 작업도 함께 삭제될 수 있습니다.

<a name="monitoring-your-queues"></a>
## 큐 모니터링

큐에 작업이 갑자기 몰려들면, 큐가 감당할 수 없을 정도로 과도한 부하가 걸려 작업 처리 대기 시간이 길어질 수 있습니다. 이럴 때 라라벨이 사전에 설정한 임계값을 초과하면 알림을 보낼 수 있습니다.

우선, [매 분마다 실행되도록](/docs/12.x/scheduling) `queue:monitor` 명령어를 스케줄링해야 합니다. 이 명령어는 모니터링할 큐의 이름과, 원하는 작업 개수 임계값을 인수로 받을 수 있습니다.

```shell
php artisan queue:monitor redis:default,redis:deployments --max=100
```

이 명령어를 예약 실행하는 것만으로는 큐가 과부하라는 알림이 자동으로 발송되지는 않습니다. 만약 명령어 실행 시 임계값을 초과한 큐 작업 개수가 발견되면, `Illuminate\Queue\Events\QueueBusy` 이벤트가 디스패치됩니다. 이 이벤트를 애플리케이션의 `AppServiceProvider` 등에서 리스닝하여, 여러분이나 개발팀에게 알림을 보낼 수 있습니다.

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

잡을 디스패치하는 코드를 테스트할 때, 실제로 작업(job)이 실행되지 않고, 디스패치 자체만 검사하고 싶을 수 있습니다. 잡의 동작 자체는 별도로 인스턴스를 만들어 `handle` 메서드를 직접 호출하는 방식으로 테스트할 수도 있습니다.

이를 위해 `Queue` 파사드의 `fake` 메서드를 사용하면, 큐에 실제로 작업이 등록되는 것을 막을 수 있습니다. 이후 `fake`를 호출한 뒤, 원하는 잡이 큐로 푸시(pushed)되었는지 assert를 통해 확인할 수 있습니다.

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

`assertPushed`나 `assertNotPushed` 메서드에 클로저를 인수로 전달하면, 해당 잡이 푸시될 때 추가적인 조건을 만족하는지 확인하는 "진위 테스트"를 할 수 있습니다. 해당 진위 테스트를 통과하는 잡이 하나라도 푸시되었다면, assert는 성공하게 됩니다.

```php
Queue::assertPushed(function (ShipOrder $job) use ($order) {
    return $job->order->id === $order->id;
});
```

<a name="faking-a-subset-of-jobs"></a>
### 일부 잡만 페이크 처리하기

전체 잡이 아닌 특정 잡만 페이크 처리하고, 나머지 잡은 그대로 실행되도록 하고 싶다면, 페이크할 잡의 클래스명을 배열로 `fake` 메서드에 전달하면 됩니다.

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

`except` 메서드를 사용하면, 지정한 잡을 제외하고(즉, 지정한 잡만 실제 큐에 푸시) 나머지 모든 잡을 페이크 처리할 수도 있습니다.

```php
Queue::fake()->except([
    ShipOrder::class,
]);
```

<a name="testing-job-chains"></a>
### 잡 체인 테스트

잡 체인(여러 잡을 연속으로 실행하는 기능)을 테스트하려면, `Bus` 파사드의 페이크 기능을 활용해야 합니다. `Bus` 파사드의 `assertChained` 메서드는 [잡 체인](/docs/12.x/queues#job-chaining)이 제대로 디스패치되었는지 검증할 수 있습니다. 이 메서드는 체인에 포함된 잡 클래스명을 배열로 받습니다.

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

위 예시처럼 체인 배열에는 잡 클래스명만 넣을 수도 있고, 실제 잡 인스턴스 배열을 넣을 수도 있습니다. 잡 인스턴스 배열을 사용하면 각 잡이 같은 클래스이며 동일한 속성(property) 값을 갖고 있는지까지 비교해서 일치하는지 확인합니다.

```php
Bus::assertChained([
    new ShipOrder,
    new RecordShipment,
    new UpdateInventory,
]);
```

잡이 체인 없이 단독으로 푸시되었는지 확인하려면 `assertDispatchedWithoutChain` 메서드를 사용할 수 있습니다.

```php
Bus::assertDispatchedWithoutChain(ShipOrder::class);
```

<a name="testing-chain-modifications"></a>
#### 체인 수정 테스트

이미 생성된 잡 체인에 [작업을 맨 앞 또는 맨 뒤에 추가](#adding-jobs-to-the-chain)하는 경우, 해당 잡 인스턴스의 `assertHasChain` 메서드를 사용해 남아 있는 체인의 순서와 작업들이 기대치에 맞는지 assert 할 수 있습니다.

```php
$job = new ProcessPodcast;

$job->handle();

$job->assertHasChain([
    new TranscribePodcast,
    new OptimizePodcast,
    new ReleasePodcast,
]);
```

`assertDoesntHaveChain` 메서드는 남은 체인에 어떠한 작업도 남아있지 않은지(즉, 체인이 비어 있는지) 확인할 때 사용합니다.

```php
$job->assertDoesntHaveChain();
```

<a name="testing-chained-batches"></a>
#### 체인 내 배치 테스트

잡 체인에 [배치 작업](#chains-and-batches)이 포함된 경우, 체인 내에 정의된 배치가 기대에 부합하는지 확인하려면 체인 assertion 내에 `Bus::chainedBatch` 정의를 포함시키면 됩니다.

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
### 잡 배치 테스트

`Bus` 파사드의 `assertBatched` 메서드는 [잡 배치](/docs/12.x/queues#job-batching)가 디스패치되었는지 assert 할 수 있습니다. 이 메서드에 전달한 클로저는 `Illuminate\Bus\PendingBatch` 인스턴스를 인수로 받으므로, 배치에 등록된 잡들에 대한 검사도 가능합니다.

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

`assertBatchCount` 메서드를 사용하면 특정 개수의 배치가 디스패치되었는지 확인할 수 있습니다.

```php
Bus::assertBatchCount(3);
```

어떠한 배치도 디스패치되지 않았는지 assert하려면 `assertNothingBatched`를 사용합니다.

```php
Bus::assertNothingBatched();
```

<a name="testing-job-batch-interaction"></a>
#### 개별 잡과 배치 간의 상호작용 테스트

가끔 개별 잡이 자신이 속한 배치와 어떻게 상호작용하는지 테스트하고 싶을 수 있습니다. 예를 들어, 잡이 배치의 이후 작업 처리를 취소했는지 검증하고 싶다면, `withFakeBatch` 메서드를 사용해 잡에 페이크 배치를 할당할 수 있습니다. 이 메서드는 잡 인스턴스와 페이크 배치가 담긴 튜플을 반환합니다.

```php
[$job, $batch] = (new ShipOrder)->withFakeBatch();

$job->handle();

$this->assertTrue($batch->cancelled());
$this->assertEmpty($batch->added);
```

<a name="testing-job-queue-interactions"></a>
### 개별 잡과 큐 상호작용 테스트

때때로 큐에 등록된 잡이 [스스로 다시 큐에 재등록](#manually-releasing-a-job)하는지, 혹은 잡이 스스로 삭제되는지 등을 테스트해야 할 때가 있습니다. 이런 경우 잡을 인스턴스화한 뒤, `withFakeQueueInteractions` 메서드를 호출해 해당 잡의 큐 인터랙션을 페이크로 만들 수 있습니다.

큐 인터랙션이 페이크로 설정된 이후에는 잡의 `handle` 메서드를 호출해 동작을 실행할 수 있습니다. 이후 `assertReleased`, `assertDeleted`, `assertNotDeleted`, `assertFailed`, `assertFailedWith`, `assertNotFailed` 등의 메서드를 사용해 큐 인터랙션 결과를 검증할 수 있습니다.

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
## 잡 이벤트

`Queue` [파사드](/docs/12.x/facades)의 `before`와 `after` 메서드를 사용하면, 큐 작업이 처리되기 전이나 후에 실행할 콜백을 지정할 수 있습니다. 이 콜백은 추가적인 로깅(log)이나, 대시보드 통계를 집계하는 데 활용할 수 있습니다. 이런 코드는 [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에서 작성하는 것이 일반적입니다. 예를 들어, 라라벨에 포함된 `AppServiceProvider`에서 다음과 같이 사용할 수 있습니다.

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

`Queue` [파사드](/docs/12.x/facades)의 `looping` 메서드를 사용하면 워커가 큐에서 작업을 가져오기 전에 실행되는 콜백을 등록할 수 있습니다. 예를 들어, 이전에 실패한 잡 때문에 열린 트랜잭션이 남아 있는 경우, 이를 모두 롤백하는 클로저를 등록할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Queue;

Queue::looping(function () {
    while (DB::transactionLevel() > 0) {
        DB::rollBack();
    }
});
```