# 큐 (Queues)

- [소개](#introduction)
    - [커넥션과 큐의 차이](#connections-vs-queues)
    - [드라이버별 참고사항 및 전제 조건](#driver-prerequisites)
- [잡 생성하기](#creating-jobs)
    - [잡 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [유일 잡(Unique Jobs)](#unique-jobs)
    - [암호화된 잡](#encrypted-jobs)
- [잡 미들웨어](#job-middleware)
    - [속도 제한(Rate Limiting)](#rate-limiting)
    - [잡 중복 방지](#preventing-job-overlaps)
    - [예외 허들링(Throttling Exceptions)](#throttling-exceptions)
    - [잡 건너뛰기](#skipping-jobs)
- [잡 디스패치](#dispatching-jobs)
    - [지연 디스패치](#delayed-dispatching)
    - [동기 디스패치](#synchronous-dispatching)
    - [잡 & 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [잡 체이닝](#job-chaining)
    - [큐와 커넥션 커스터마이징](#customizing-the-queue-and-connection)
    - [최대 시도 횟수 / 타임아웃 값 지정](#max-job-attempts-and-timeout)
    - [에러 처리](#error-handling)
- [잡 배치 처리(Job Batching)](#job-batching)
    - [배치 처리 가능한 잡 정의](#defining-batchable-jobs)
    - [배치 디스패치하기](#dispatching-batches)
    - [체인과 배치의 조합](#chains-and-batches)
    - [잡을 배치에 추가하기](#adding-jobs-to-batches)
    - [배치 상태 확인하기](#inspecting-batches)
    - [배치 취소](#cancelling-batches)
    - [배치 실패 처리](#batch-failures)
    - [배치 기록 정리(Pruning Batches)](#pruning-batches)
    - [DynamoDB에 배치 저장](#storing-batches-in-dynamodb)
- [클로저 큐잉](#queueing-closures)
- [큐 워커 실행](#running-the-queue-worker)
    - [`queue:work` 명령어](#the-queue-work-command)
    - [큐 우선순위](#queue-priorities)
    - [큐 워커와 배포](#queue-workers-and-deployment)
    - [잡 만료 및 타임아웃](#job-expirations-and-timeouts)
- [Supervisor 설정](#supervisor-configuration)
- [실패한 잡 처리하기](#dealing-with-failed-jobs)
    - [실패한 잡 정리](#cleaning-up-after-failed-jobs)
    - [실패한 잡 재시도](#retrying-failed-jobs)
    - [누락된 모델 무시](#ignoring-missing-models)
    - [실패한 잡 가지치기(Pruning)](#pruning-failed-jobs)
    - [실패한 잡을 DynamoDB에 저장](#storing-failed-jobs-in-dynamodb)
    - [실패한 잡 저장 비활성화](#disabling-failed-job-storage)
    - [실패한 잡 이벤트](#failed-job-events)
- [큐에서 잡 제거](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [잡 일부만 페이크 처리하기](#faking-a-subset-of-jobs)
    - [잡 체인 테스트](#testing-job-chains)
    - [잡 배치 테스트](#testing-job-batches)
    - [잡/큐 상호작용 테스트](#testing-job-queue-interactions)
- [잡 이벤트](#job-events)

<a name="introduction"></a>
## 소개

웹 애플리케이션을 개발하다 보면, 업로드된 CSV 파일을 파싱하고 저장하는 작업처럼 한 번의 일반적인 웹 요청으로는 처리 시간이 너무 오래 걸리는 작업들이 있을 수 있습니다. 다행히 라라벨에서는 이러한 작업을 쉽게 큐에 넣어 백그라운드에서 처리할 수 있는 잡(job)을 만들 수 있습니다. 시간 소모가 큰 작업을 큐로 분리하면, 애플리케이션은 웹 요청에 매우 빠르게 응답하며 사용자에게 더 나은 경험을 제공하게 됩니다.

라라벨의 큐 시스템은 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 또는 관계형 데이터베이스 등 다양한 큐 백엔드를 하나의 통합된 API로 사용할 수 있도록 지원합니다.

큐 설정은 애플리케이션의 `config/queue.php` 설정 파일에 저장되어 있습니다. 이 파일에는 프레임워크에 포함된 각 큐 드라이버(데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 드라이버 등)와 관련된 커넥션 설정이 담겨 있습니다. 또한, 잡을 즉시 실행하는 동기 드라이버(주로 로컬 개발 용도)와, 큐에 쌓인 잡을 무시하고 모두 폐기하는 `null` 드라이버도 포함되어 있습니다.

> [!NOTE]
> 라라벨은 이제 Redis 기반 큐를 위한 아름다운 대시보드 및 설정 시스템인 Horizon을 제공합니다. 더 자세한 내용은 [Horizon 공식 문서](/docs/12.x/horizon)를 확인하세요.

<a name="connections-vs-queues"></a>
### 커넥션과 큐의 차이

라라벨 큐 시스템을 사용하기 전에 "커넥션(Connection)"과 "큐(Queue)"가 어떻게 구분되는지 이해하는 것이 중요합니다. `config/queue.php` 설정 파일에는 `connections`라는 설정 배열이 있습니다. 이 옵션은 Amazon SQS, Beanstalk, Redis와 같은 백엔드 큐 서비스에 대한 연결 정보를 정의합니다. 한편, 큐 커넥션 하나는 여러 개의 "큐"를 가질 수 있는데, 각각을 별도의 잡 스택 또는 잡 모음으로 생각할 수 있습니다.

각 커넥션 예시에는 `queue`라는 속성이 포함되어 있습니다. 이 속성은 해당 커넥션으로 잡을 디스패치할 때 기본적으로 사용되는 큐 이름을 의미합니다. 즉, 잡을 디스패치할 때 어떤 큐로 보낼지 명시하지 않으면, 커넥션 설정의 `queue` 속성에 지정된 큐로 잡이 쌓이게 됩니다.

```php
use App\Jobs\ProcessPodcast;

// 이 잡은 기본 커넥션의 기본 큐로 전송됩니다...
ProcessPodcast::dispatch();

// 이 잡은 기본 커넥션의 "emails" 큐로 전송됩니다...
ProcessPodcast::dispatch()->onQueue('emails');
```

어떤 애플리케이션은 여러 개의 큐를 사용할 필요 없이 단순하게 하나의 큐만 쓸 수도 있습니다. 그러나 잡의 처리 우선순위나 분리를 위해 여러 큐를 사용하는 것이 유용한 경우도 많습니다. 라라벨 큐 워커는 어떤 큐를 먼저 처리할지 우선순위를 지정할 수 있으므로, 예를 들어 `high`라는 큐로 잡을 모아두고 워커를 우선 처리하도록 다음과 같이 실행할 수 있습니다.

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버별 참고사항 및 전제 조건

<a name="database"></a>
#### 데이터베이스

`database` 큐 드라이버를 사용하려면 잡을 저장할 데이터베이스 테이블이 필요합니다. 일반적으로, 라라벨 기본 제공 `0001_01_01_000002_create_jobs_table.php` [마이그레이션](/docs/12.x/migrations)에 이 테이블 생성이 포함되어 있습니다. 만약 애플리케이션에 해당 마이그레이션 파일이 없다면, `make:queue-table` 아티즌 명령어로 직접 생성할 수 있습니다.

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면, `config/database.php` 파일에서 Redis 데이터베이스 커넥션을 먼저 설정해야 합니다.

> [!WARNING]
> `redis` 큐 드라이버는 Redis의 `serializer` 및 `compression` 옵션을 지원하지 않습니다.

**Redis 클러스터**

Redis 큐 커넥션이 Redis 클러스터를 사용하는 경우, 큐 이름에 [키 해시 태그(key hash tag)](https://redis.io/docs/reference/cluster-spec/#hash-tags)가 반드시 포함되어야 합니다. 이렇게 하면 하나의 큐가 사용하는 모든 Redis 키가 동일한 해시 슬롯에 저장되도록 보장할 수 있습니다.

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

**Blocking (대기 설정)**

Redis 큐를 사용할 때는 `block_for` 설정 옵션을 통해, 워커 루프가 잡을 기다리는 시간(초)을 지정할 수 있습니다. 이 값에 따라 Redis 데이터베이스를 잡이 있는지 계속 폴링하는 대신, 정해진 시간만큼 대기하는 방식으로 효율적으로 작동할 수 있습니다. 예를 들어, 아래처럼 5초로 설정하면 잡이 생길 때까지 최대 5초간 대기합니다.

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
> `block_for` 값을 `0`으로 설정하면, 큐 워커는 잡이 생길 때까지 무한정 대기하게 되며, 이로 인해 `SIGTERM` 등 종료 신호가 잡 처리 직전까지 반영되지 않을 수 있습니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 전제 조건

아래 큐 드라이버를 사용하려면 추가 의존성을 설치해야 합니다. 이들은 Composer 패키지 관리자를 통해 설치할 수 있습니다.

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

기본적으로 애플리케이션의 큐잉 가능한 모든 잡 클래스는 `app/Jobs` 디렉터리에 저장됩니다. 만약 `app/Jobs` 디렉터리가 없다면, `make:job` 아티즌 명령어를 실행할 때 자동으로 생성됩니다.

```shell
php artisan make:job ProcessPodcast
```

생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현합니다. 이 인터페이스는 해당 잡이 큐에 넣어져 비동기로 실행되어야 함을 라라벨에 알리는 역할을 합니다.

> [!NOTE]
> 잡 스텁(stub)은 [스텁 퍼블리싱](/docs/12.x/artisan#stub-customization) 기능으로 커스터마이즈할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조

잡 클래스는 일반적으로 매우 단순하며, 큐에서 잡이 처리될 때 호출되는 `handle` 메서드만 포함되는 경우가 많습니다. 먼저 예시 잡 클래스를 살펴보겠습니다. 이 예시에서는 팟캐스트 게시 서비스에서 업로드된 팟캐스트 파일을 게시 전에 가공 처리하는 잡을 다룹니다.

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

이 예제에서처럼, [Eloquent 모델](/docs/12.x/eloquent)을 큐잉된 잡의 생성자에 직접 전달할 수 있습니다. 잡에 `Queueable` 트레이트를 사용할 경우, Eloquent 모델과 그에 로드된 연관관계까지도 잡이 큐에 들어갈 때 자동으로 시리얼라이즈(직렬화)되고, 잡 처리 시에는 자동으로 언시리얼라이즈되어 복원됩니다.

큐잉된 잡이 Eloquent 모델을 생성자 인수로 받아 처리할 경우, 큐에는 해당 모델의 식별자만 저장됩니다. 실제로 잡이 실행될 때, 큐 시스템이 데이터베이스로부터 해당 모델 인스턴스와 필요한 연관관계를 자동으로 다시 조회합니다. 이렇게 하면 큐로 보내는 잡의 크기가 매우 작아지는 이점이 있습니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드의 의존성 주입

잡의 `handle` 메서드는 큐에서 잡이 처리될 때 호출됩니다. 이때, 메서드에 의존성을 타이핑힌트(타입힌트)로 선언할 수 있습니다. 라라벨 [서비스 컨테이너](/docs/12.x/container)가 여기에 필요한 의존 객체를 자동으로 주입해줍니다.

만약 의존성 주입을 컨테이너가 어떻게 처리하는지 완전히 제어하고 싶다면, 컨테이너의 `bindMethod` 메서드를 사용할 수 있습니다. `bindMethod`는 콜백을 받아 잡과 컨테이너 인스턴스를 전달합니다. 콜백 내부에서 원하는 방식으로 `handle` 메서드를 호출할 수 있습니다. 보통 이 코드는 `App\Providers\AppServiceProvider`의 [서비스 프로바이더](/docs/12.x/providers) `boot` 메서드에서 작성합니다.

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 이미지 이진 데이터(raw image 등)와 같은 이진 데이터는 잡에 전달하기 전에 반드시 `base64_encode` 함수를 이용해 인코딩해야 합니다. 그렇지 않으면 큐에 저장 과정에서 잡이 제대로 JSON으로 시리얼라이즈되지 않을 수 있습니다.

<a name="handling-relationships"></a>
#### 큐잉된 연관관계

잡을 큐에 넣을 때 Eloquent 모델의 모든 연관관계가 함께 시리얼라이즈되기 때문에, 큐에 저장되는 잡 데이터가 매우 커질 수도 있습니다. 그리고 잡이 복원되면서 모델의 연관관계가 데이터베이스에서 다시 조회될 때, 큐에 넣기 전 미리 걸어둔 쿼리 제약 조건이 무시될 수 있습니다. 따라서 특정 연관관계의 일부만 다루고 싶다면, 잡 내부에서 원하는 쿼리 제약을 다시 적용해야 합니다.

또는, 연관관계 정보가 큐에 저장되지 않게 하려면, 모델에 값을 할당할 때 `withoutRelations` 메서드를 호출하면 됩니다. 이 메서드는 연관관계를 제거한 모델 인스턴스를 반환합니다.

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

또한, PHP 생성자 프로퍼티 승격(생성자 매개변수를 곧바로 프로퍼티로 할당하는 문법)을 사용할 때 Eloquent 모델의 연관관계가 시리얼라이즈되지 않게 하려면, `WithoutRelations` 속성(attribute)을 사용할 수 있습니다.

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

잡이 단일 모델이 아니라 Eloquent 모델의 컬렉션이나 배열을 받는 경우에는, 큐에서 복원될 때 컬렉션 내의 각 모델들의 연관관계는 자동으로 다시 로드되지 않습니다. 이는 대규모 모델을 다루는 잡에서 리소스 사용량이 과도해지는 것을 막기 위함입니다.

<a name="unique-jobs"></a>
### 유일 잡(Unique Jobs)

> [!WARNING]
> 유일 잡 기능은 [락(Lock)](/docs/12.x/cache#atomic-locks)을 지원하는 캐시 드라이버가 필수입니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 원자적 락을 지원합니다. 또한, 잡 배치 내의 잡에는 유일 잡 제한이 적용되지 않습니다.

특정 잡이 동시에 큐에 중복해서 존재하지 않도록 하고 싶을 때가 있습니다. 이때 잡 클래스에 `ShouldBeUnique` 인터페이스를 구현하면 됩니다. 이 인터페이스는 추가 메서드를 정의할 필요 없이 적용할 수 있습니다.

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

위 예제에서 `UpdateSearchIndex`라는 잡은 유일하게 동작합니다. 즉, 큐에 동일한 잡 인스턴스가 아직 처리 완료되지 않은 상태라면, 새로운 잡 디스패치는 무시됩니다.

잡의 유일성을 판별하는 특정 "키"를 지정하거나, 유일 상태의 지속시간 타임아웃을 지정하고 싶다면, 잡 클래스에 `uniqueId` 또는 `uniqueFor` 프로퍼티/메서드를 추가할 수 있습니다.

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
     * 잡의 유일 락이 해제되는(만료되는) 시간(초)
     *
     * @var int
     */
    public $uniqueFor = 3600;

    /**
     * 해당 잡의 유일 ID를 반환
     */
    public function uniqueId(): string
    {
        return $this->product->id;
    }
}
```

위 예제에서는 product ID로 잡의 유일성을 판별합니다. 즉, 동일한 product ID로 잡을 여러 번 디스패치해도 기존 잡이 처리되기 전까지는 새로 추가되지 않습니다. 그리고 만약 기존 잡이 1시간 이내에 처리되지 않으면 유일 락이 풀리고, 같은 키를 가진 새로운 잡이 큐에 들어갈 수 있습니다.

> [!WARNING]
> 여러 웹 서버나 컨테이너에서 잡을 디스패치하는 경우, 모든 서버가 동일한 중앙 캐시 서버와 통신하도록 설정해야 라라벨이 정확하게 잡의 유일 여부를 판단할 수 있습니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### "처리 시작 전까지" 유일 잡 유지

기본적으로, 유일 잡은 큐에서 처리 완료되거나 모든 재시도 횟수가 소진되었을 때 락이 해제됩니다. 하지만 잡이 실제로 처리되기 직전에 락을 해제하고 싶은 상황이 있을 수 있습니다. 이 경우 잡 클래스가 `ShouldBeUnique` 대신 `ShouldBeUniqueUntilProcessing` 인터페이스를 구현하면 됩니다.

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
#### 유일 잡 락(Unique Job Locks)

내부적으로, `ShouldBeUnique` 잡이 디스패치될 때 라라벨은 해당 잡의 `uniqueId` 키로 [락(Lock)](/docs/12.x/cache#atomic-locks)을 얻으려고 시도합니다. 락 취득에 실패하면 잡은 디스패치되지 않습니다. 이 락은 잡이 실행을 마치거나 모든 재시도가 실패할 때 해제됩니다. 라라벨은 기본 캐시 드라이버를 사용해 락을 관리하지만, 다른 드라이버로 락을 획득하도록 하고 싶으면 `uniqueVia` 메서드를 추가로 정의할 수 있습니다.

```php
use Illuminate\Contracts\Cache\Repository;
use Illuminate\Support\Facades\Cache;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...

    /**
     * 유일 잡 락을 위한 캐시 드라이버 반환
     */
    public function uniqueVia(): Repository
    {
        return Cache::driver('redis');
    }
}
```

> [!NOTE]
> 단순히 잡이 동시에 처리되는 개수만을 제한하고 싶다면, [WithoutOverlapping](/docs/12.x/queues#preventing-job-overlaps) 잡 미들웨어를 사용하는 것이 더 적합합니다.

<a name="encrypted-jobs"></a>
### 암호화된 잡

라라벨은 [암호화](/docs/12.x/encryption)를 통해 잡 데이터의 개인정보 보호와 무결성을 보장할 수 있습니다. 사용 방법은 매우 간단합니다. 잡 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하면, 라라벨이 해당 잡을 큐에 넣기 전에 자동으로 암호화합니다.

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

잡 미들웨어를 통해, 큐잉된 잡의 실행을 감싸며 추가 로직을 적용할 수 있습니다. 이렇게 하면 잡 클래스 자체가 복잡해지지 않고, 반복되는 보일러플레이트 코드를 줄일 수 있습니다. 예를 들어, 아래 `handle` 메서드는 라라벨의 Redis 속도 제한(Rate Limiting) 기능을 활용해 5초에 한 번만 잡이 처리되도록 합니다.

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

이 코드도 정상적으로 동작하지만, `handle` 메서드 내부에 Redis 속도 제한 로직이 너무 많아져 잡 자체의 가독성이 떨어집니다. 또한, 여러 잡에서 동일한 속도 제한이 필요하면 코드를 중복 작성해야 하는 문제도 있습니다.

이러한 경우 handle 메서드가 아닌 별도의 잡 미들웨어를 만들어 속도 제한을 처리할 수 있습니다. 라라벨은 기본적으로 잡 미들웨어의 저장 위치를 정해두고 있지 않으므로, 원하는 곳에 자유롭게 구현하면 됩니다. 아래 예제에서는 `app/Jobs/Middleware` 디렉터리에 미들웨어를 둡니다.

```php
<?php

namespace App\Jobs\Middleware;

use Closure;
use Illuminate\Support\Facades\Redis;

class RateLimited
{
    /**
     * 큐잉된 잡을 처리합니다.
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

위에서 볼 수 있듯이, [라우트 미들웨어](/docs/12.x/middleware)와 마찬가지로 잡 미들웨어에도 현재 처리 중인 잡과, 다음 단계를 이어주는 콜백이 주입됩니다.

잡 미들웨어 클래스는 `make:job-middleware` 아티즌 명령어로 생성할 수 있습니다. 미들웨어를 만든 후에는 잡 클래스의 `middleware` 메서드에서 반환해 잡에 할당할 수 있습니다. 이 메서드는 `make:job` 명령어로 scaffold된 잡에 기본적으로 포함되어 있지 않으니, 직접 추가해주어야 합니다.

```php
use App\Jobs\Middleware\RateLimited;

/**
 * 잡이 통과할 미들웨어들을 반환합니다.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited];
}
```

> [!NOTE]
> 잡 미들웨어는 [큐잉 가능한 이벤트 리스너](/docs/12.x/events#queued-event-listeners), [메일러블](/docs/12.x/mail#queueing-mail), [알림(Notification)](/docs/12.x/notifications#queueing-notifications)에도 할당할 수 있습니다.

<a name="rate-limiting"></a>
### 속도 제한(Rate Limiting)

앞서 보면 직접 Rate Limiting 잡 미들웨어를 작성하는 방법을 소개했으나, 라라벨에는 이미 사용할 수 있는 속도 제한 미들웨어가 내장되어 있습니다. [라우트 속도 제한](/docs/12.x/routing#defining-rate-limiters)와 마찬가지로, 잡 전용 rate limiter 역시 `RateLimiter` 파사드의 `for` 메서드로 정의할 수 있습니다.

예를 들어, 사용자가 데이터를 백업할 때 일반 사용자에게는 한 시간에 한 번만 허용하고, 프리미엄 고객은 별도의 제한 없이 처리하고 싶을 수 있습니다. 이를 위해서는 `AppServiceProvider`의 `boot` 메서드에서 아래처럼 RateLimiter를 정의하면 됩니다.

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

위 예제에서는 시간 단위 제한을 설정했지만, `perMinute` 메서드를 사용해 분 단위 제한도 할 수 있습니다. 그리고 `by` 메서드에는 원하는 값을 지정할 수 있는데, 주로 고객별로 분리해서 제한할 때 사용합니다.

```php
return Limit::perMinute(50)->by($job->user->id);
```

RateLimiter를 정의한 후, 해당 잡에 `Illuminate\Queue\Middleware\RateLimited` 미들웨어를 할당할 수 있습니다. 잡이 속도 제한을 초과하면 이 미들웨어가 잡을 자동으로 다시 큐에 반환하며, 반환 딜레이는 제한 시간에 따라 결정됩니다.

```php
use Illuminate\Queue\Middleware\RateLimited;

/**
 * 잡이 통과할 미들웨어들을 반환합니다.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited('backups')];
}
```

속도 제한 때문에 잡이 다시 큐로 이동될 때에도 `attempts`(시도 횟수)는 계속 누적됩니다. 따라서, 잡 클래스의 `tries`, `maxExceptions` 값을 상황에 맞게 조정하거나, [retryUntil 메서드](#time-based-attempts)로 잡 시도 가능 기간을 직접 지정하는 것도 좋습니다.

`releaseAfter` 메서드를 사용하면, 잡이 재시도 되기 전까지 대기할 시간을 초 단위로 직접 지정할 수도 있습니다.

```php
/**
 * 잡이 통과할 미들웨어들을 반환합니다.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new RateLimited('backups'))->releaseAfter(60)];
}
```

만약 잡이 속도 제한으로 인한 대기 시에 재시도하지 않도록 하고 싶다면 `dontRelease` 메서드를 활용합니다.

```php
/**
 * 잡이 통과할 미들웨어들을 반환합니다.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new RateLimited('backups'))->dontRelease()];
}
```

> [!NOTE]
> Redis를 사용할 경우, `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어를 사용할 수 있습니다. 이 미들웨어는 Redis에 최적화되어 기본 RateLimited 미들웨어보다 더 효율적으로 동작합니다.

<a name="preventing-job-overlaps"></a>
### 잡 중복 방지

라라벨은 `Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어를 통해 임의의 키 기준으로 잡의 중복 실행을 방지할 수 있습니다. 이는 한 번에 하나의 잡만 특정 리소스를 수정해야 할 때 유용합니다.

예를 들어, 사용자의 신용점수를 갱신하는 잡이 있다고 가정해 봅시다. 같은 사용자 ID로 동시에 여러 잡이 실행되지 않도록 하고 싶다면 잡의 `middleware` 메서드에서 `WithoutOverlapping` 미들웨어를 반환하면 됩니다.

```php
use Illuminate\Queue\Middleware\WithoutOverlapping;

/**
 * 잡이 통과할 미들웨어들을 반환합니다.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new WithoutOverlapping($this->user->id)];
}
```

동일 유형의 잡이 겹칠 경우, 중복 잡은 큐에 다시 반환됩니다. 또한, `releaseAfter`로 큐에 다시 넣기 전까지 대기할 시간을 지정할 수도 있습니다.

```php
/**
 * 잡이 통과할 미들웨어들을 반환합니다.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->releaseAfter(60)];
}
```

만약 중복 잡을 즉시 삭제하길 원한다면, 즉 재시도되지 않게 하려면 `dontRelease`를 사용할 수 있습니다.

```php
/**
 * 잡이 통과할 미들웨어들을 반환합니다.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->dontRelease()];
}
```

`WithoutOverlapping` 미들웨어는 라라벨의 원자적 락(atomic lock) 기능을 사용합니다. 때때로 잡이 예기치 않게 실패하거나 타임아웃되어 락이 해제되지 않을 수 있습니다. 이때는 `expireAfter` 메서드로 락 만료 시간을 명시적으로 지정할 수 있습니다. 아래 예시는 잡이 시작된 후 3분(180초) 뒤에 락을 자동 해제합니다.

```php
/**
 * 잡이 통과할 미들웨어들을 반환합니다.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->expireAfter(180)];
}
```

> [!WARNING]
> `WithoutOverlapping` 미들웨어는 [락](/docs/12.x/cache#atomic-locks)을 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 지원됩니다.

<a name="sharing-lock-keys"></a>

#### 작업 클래스 간의 락 키 공유

기본적으로 `WithoutOverlapping` 미들웨어는 동일한 클래스의 중복된 작업(잡) 실행만 방지합니다. 따라서 서로 다른 두 작업 클래스가 동일한 락 키를 사용하더라도, 중복 실행을 막을 수 없습니다. 하지만, 라라벨의 `shared` 메서드를 활용하면 락 키를 작업 클래스 간에 공유하도록 지정할 수 있습니다.

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
### 예외 제한(Throttle) 처리

라라벨은 `Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어를 제공하여 작업에서 발생하는 예외의 빈도를 제한(throttle)할 수 있습니다. 작업이 정해진 횟수만큼 예외를 던지면, 이후 이 작업의 다음 실행 시도는 지정된 시간만큼 지연됩니다. 이 미들웨어는 외부 서비스와 상호작용하는 작업에서 해당 서비스가 불안정할 때 특히 유용합니다.

예를 들어, 외부 API와 연동하는 큐잉된 작업이 있다고 가정했을 때, 예외 발생을 제한하려면 작업의 `middleware` 메서드에서 `ThrottlesExceptions` 미들웨어를 반환하면 됩니다. 보통 이 미들웨어는 [시간 기반 시도](#time-based-attempts)를 구현한 작업과 함께 사용됩니다.

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
 * 작업의 타임아웃 시각을 결정합니다.
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(30);
}
```

이 미들웨어의 첫 번째 생성자 인자는 작업이 제한되기 전까지 발생할 수 있는 예외의 개수이며, 두 번째 인자는 제한이 시작된 후 작업을 다시 시도하기까지 대기할 초 단위의 시간입니다. 위 예시에서, 만약 작업이 연속해서 10번 예외를 발생시키면, 이후 이 작업은 5분 동안 대기한 후 30분 제한 내에서 다시 처리됩니다.

작업이 예외를 발생시켰지만 제한 기준에 도달하지 않은 경우에는 일반적으로 즉시 재시도됩니다. 그러나 미들웨어를 작업에 적용할 때 `backoff` 메서드를 호출하면, 지연시킬 분(minute) 수를 지정할 수 있습니다.

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

이 미들웨어는 내부적으로 라라벨의 캐시 시스템을 사용하여 제한을 구현하며, 작업의 클래스명이 캐시 "키"로 활용됩니다. 여러 작업이 동일한 외부 서비스와 상호작용하면서 동일한 제한 "버킷"을 공유하려는 경우, 미들웨어를 적용할 때 `by` 메서드를 호출하여 키를 오버라이드(재정의)할 수 있습니다.

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

기본적으로 이 미들웨어는 모든 예외에 대해 제한을 적용합니다. `when` 메서드를 사용하여 예외가 특정 조건을 만족할 때만 제한되도록 동작을 변경할 수 있습니다. 즉, `when` 메서드에 전달한 클로저가 `true`를 반환할 경우에만 예외가 제한(Throttle)됩니다.

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

`when` 메서드는 작업을 큐에 다시 올리거나 예외를 던지는 반면, `deleteWhen` 메서드는 특정 예외가 발생할 경우 해당 작업 자체를 완전히 삭제할 수 있도록 해줍니다.

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

제한된 예외를 애플리케이션의 예외 핸들러로 리포트하고 싶다면, 미들웨어를 적용할 때 `report` 메서드를 호출하면 됩니다. 옵션으로, 클로저를 `report`에 전달할 수도 있는데, 이 경우 해당 클로저가 `true`를 반환할 때만 예외가 리포트됩니다.

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
> Redis를 사용하는 경우, Redis에 최적화되고 일반 예외 제한 미들웨어보다 효율적인 `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어를 사용할 수 있습니다.

<a name="skipping-jobs"></a>
### 작업 건너뛰기(Skip)

`Skip` 미들웨어를 사용하면 작업의 로직을 변경하지 않고도 작업 자체를 건너뛰거나 삭제할 수 있습니다. `Skip::when` 메서드에 지정한 조건이 `true`로 평가되면 작업은 삭제되며, `Skip::unless`는 조건이 `false`일 때 작업을 삭제합니다.

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

보다 복잡한 조건 판단이 필요하다면 `when` 및 `unless` 메서드에 `Closure`를 전달할 수도 있습니다.

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
## 작업(잡) 디스패치(Dispatch)하기

작업 클래스를 작성한 후에는 작업 클래스에서 직접 `dispatch` 메서드를 이용해 해당 작업을 큐에 등록(디스패치)할 수 있습니다. `dispatch` 메서드에 전달하는 인자는 작업의 생성자(constructor)로 넘겨집니다.

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

작업을 조건적으로 디스패치하고 싶다면 `dispatchIf` 및 `dispatchUnless` 메서드를 사용할 수 있습니다.

```php
ProcessPodcast::dispatchIf($accountActive, $podcast);

ProcessPodcast::dispatchUnless($accountSuspended, $podcast);
```

새로운 라라벨 애플리케이션에서는 `sync` 드라이버가 기본 큐 드라이버로 설정되어 있습니다. 이 드라이버는 작업을 현재 요청의 처리 중, 즉시 동기적으로 실행합니다. 이는 보통 로컬 개발 환경에서 편리하게 사용할 수 있습니다. 작업을 실제로 큐에 추가하여 백그라운드에서 처리하고 싶다면, 애플리케이션의 `config/queue.php` 설정 파일에서 다른 큐 드라이버를 지정하면 됩니다.

<a name="delayed-dispatching"></a>
### 지연 디스패치(Delayed Dispatch)

작업이 즉시 큐 워커(worker)에게 처리되지 않고, 일정 시간이 지난 후에 처리되도록 하고 싶다면 작업을 디스패치할 때 `delay` 메서드를 사용할 수 있습니다. 예를 들어, 작업을 디스패치한 후 10분이 지나야만 처리 가능하도록 지정하려면 다음과 같이 작성합니다.

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

경우에 따라 작업에 기본 지연 시간이 설정되어 있을 수도 있습니다. 이 지연을 무시하고 즉시 작업을 디스패치하려면 `withoutDelay` 메서드를 사용할 수 있습니다.

```php
ProcessPodcast::dispatch($podcast)->withoutDelay();
```

> [!WARNING]
> Amazon SQS 큐 서비스는 최대 지연 시간이 15분으로 제한되어 있습니다.

<a name="dispatching-after-the-response-is-sent-to-browser"></a>
#### 브라우저로 응답이 전송된 후에 작업 디스패치하기

또한, `dispatchAfterResponse` 메서드를 사용하면 작업 디스패치를 HTTP 응답이 사용자 브라우저로 전송된 후(웹 서버가 FastCGI를 사용하는 경우)에 지연시킬 수 있습니다. 이를 통해 유저는 작업이 수행되는 동안에도 애플리케이션을 바로 이용할 수 있습니다. 이 방식은 보통 이메일 전송 등 1초 내외로 처리되는 작업에 권장됩니다. 현재 HTTP 요청 내에서 작업이 처리되므로 이런 방식으로 디스패치된 작업은 별도의 큐 워커가 실행 중이 아니더라도 처리됩니다.

```php
use App\Jobs\SendNotification;

SendNotification::dispatchAfterResponse();
```

또한 클로저를 `dispatch` 헬퍼로 디스패치한 후 `afterResponse` 메서드를 연결(chain)하여, 브라우저에 응답이 전송된 후 클로저가 실행되도록 할 수 있습니다.

```php
use App\Mail\WelcomeMessage;
use Illuminate\Support\Facades\Mail;

dispatch(function () {
    Mail::to('taylor@example.com')->send(new WelcomeMessage);
})->afterResponse();
```

<a name="synchronous-dispatching"></a>
### 동기적 디스패치(Synchronous Dispatch)

작업을 즉시(동기적으로) 실행하고 싶다면 `dispatchSync` 메서드를 사용할 수 있습니다. 이 메서드를 이용하면 작업이 큐에 등록되지 않고, 현재 프로세스에서 곧바로 실행됩니다.

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
### 작업과 데이터베이스 트랜잭션

데이터베이스 트랜잭션 내에서 작업을 디스패치해도 괜찮지만, 작업이 실제로 성공적으로 실행될 수 있도록 각별한 주의가 필요합니다. 트랜잭션 내부에서 작업을 디스패치할 때, 부모 트랜잭션이 커밋되기 전에 큐 워커가 작업을 처리할 가능성이 있습니다. 이 경우, 트랜잭션 중에 모델이나 데이터베이스 레코드에 가한 수정사항이 데이터베이스에 반영되기 전이기 때문에, 작업에서 이를 참조하면 반영되지 않은 데이터가 사용될 수 있습니다. 또한 트랜잭션 내에서 생성된 데이터베이스 레코드가 아직 존재하지 않을 수도 있습니다.

이 문제를 해결하기 위해 라라벨은 몇 가지 방법을 제공합니다. 첫 번째로, 큐 연결 설정 배열에서 `after_commit` 옵션을 지정할 수 있습니다.

```php
'redis' => [
    'driver' => 'redis',
    // ...
    'after_commit' => true,
],
```

`after_commit` 옵션이 `true`라면, 데이터베이스 트랜잭션 내에서도 작업을 디스패치할 수 있지만 라라벨은 열린 트랜잭션이 모두 커밋된 후에 실제로 작업을 디스패치합니다. 물론, 현재 열린 데이터베이스 트랜잭션이 없다면 작업은 즉시 디스패치됩니다.

만약 트랜잭션 도중 예외가 발생하여 롤백되는 경우, 해당 트랜잭션 중에 디스패치되었던 작업들도 모두 삭제됩니다.

> [!NOTE]
> `after_commit` 설정을 `true`로 할 경우, 큐로 처리되는 이벤트 리스너, 메일러블, 알림, 브로드캐스트 이벤트도 데이터베이스 트랜잭션이 모두 커밋된 후에 디스패치됩니다.

<a name="specifying-commit-dispatch-behavior-inline"></a>
#### 커밋 후 디스패치 동작을 인라인으로 지정하기

큐 연결의 `after_commit` 설정을 `true`로 하지 않은 경우에도, 특정 작업이 열린 데이터베이스 트랜잭션이 모두 커밋된 후에 디스패치되도록 설정할 수 있습니다. 이를 위해 디스패치 작업에 `afterCommit` 메서드를 체이닝하면 됩니다.

```php
use App\Jobs\ProcessPodcast;

ProcessPodcast::dispatch($podcast)->afterCommit();
```

반대로, `after_commit` 설정이 `true`인 경우에는 작업이 트랜잭션 커밋을 기다리지 않고 즉시 디스패치되도록 `beforeCommit` 메서드를 사용할 수 있습니다.

```php
ProcessPodcast::dispatch($podcast)->beforeCommit();
```

<a name="job-chaining"></a>
### 작업 체이닝(Job Chaining)

작업 체이닝을 사용하면, 기본 작업이 성공적으로 실행된 후 순차적으로 실행되어야 할 작업 목록을 지정할 수 있습니다. 체인 중 하나의 작업이 실패하면 남은 작업은 실행되지 않습니다. 큐잉된 작업 체인을 실행하려면 `Bus` 파사드의 `chain` 메서드를 사용하면 됩니다. 라라벨의 커맨드 버스는 큐 작업 디스패치의 기반이 되는 하위 레벨 컴포넌트입니다.

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

작업 클래스 인스턴스 뿐만 아니라 클로저도 체인에 연결할 수 있습니다.

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
> 작업 내에서 `$this->delete()` 메서드로 작업을 삭제해도 체이닝된 나머지 작업이 계속 실행됩니다. 체인 내의 작업이 실패해야만 체이닝이 중단됩니다.

<a name="chain-connection-queue"></a>
#### 체인 작업의 연결(Connection) 및 큐(Queue) 지정

체이닝된 작업이 사용할 연결 및 큐를 지정하고 싶다면, `onConnection` 및 `onQueue` 메서드를 사용할 수 있습니다. 이 메서드는 명시적으로 다른 연결/큐가 할당되지 않은 한, 체인 내 작업이 사용할 연결과 큐 이름을 지정합니다.

```php
Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->onConnection('redis')->onQueue('podcasts')->dispatch();
```

<a name="adding-jobs-to-the-chain"></a>
#### 체인에 작업 추가하기

가끔은 체인 내 다른 작업의 내부에서 기존 작업 체인 앞에(prepend) 또는 뒤에(append) 작업을 추가해야 할 수도 있습니다. 이럴 때는 `prependToChain` 및 `appendToChain` 메서드를 사용할 수 있습니다.

```php
/**
 * 작업 실행 메서드입니다.
 */
public function handle(): void
{
    // ...

    // 현재 체인 앞에 추가, 현재 작업 직후에 실행...
    $this->prependToChain(new TranscribePodcast);

    // 현재 체인 끝에 추가, 체인 맨 마지막에 실행...
    $this->appendToChain(new TranscribePodcast);
}
```

<a name="chain-failures"></a>
#### 체인 내 작업 실패 처리

체이닝된 작업이 실패한 경우, `catch` 메서드로 실패 시 실행할 클로저를 지정할 수 있습니다. 전달된 콜백은 작업 실패를 유발한 `Throwable` 인스턴스를 인자로 받습니다.

```php
use Illuminate\Support\Facades\Bus;
use Throwable;

Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->catch(function (Throwable $e) {
    // 체인 내의 작업 중 하나가 실패...
})->dispatch();
```

> [!WARNING]
> 체인 콜백은 직렬화되어 라라벨 큐가 나중에 실행하기 때문에, 체인 콜백 내에서 `$this` 변수를 사용해서는 안 됩니다.

<a name="customizing-the-queue-and-connection"></a>
### 큐와 연결 커스터마이징

<a name="dispatching-to-a-particular-queue"></a>
#### 특정 큐로 디스패치하기

작업들을 서로 다른 큐에 분류(push)하면 작업의 카테고리를 나누고, 각 큐에 할당할 워커의 우선순위를 조정할 수 있습니다. 이는 큐 설정 파일에 정의된 서로 다른 큐 "연결(connection)"에 작업을 추가한다는 의미가 아니라, 하나의 연결 내에서 큐를 다르게 지정하는 것입니다. 작업을 특정 큐로 디스패치하려면 작업 디스패치 시 `onQueue` 메서드를 사용하면 됩니다.

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

또는, 작업 클래스의 생성자 내부에서 `onQueue` 메서드를 호출하여 작업의 큐를 지정할 수도 있습니다.

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
#### 특정 연결로 디스패치하기

애플리케이션이 여러 큐 연결을 사용할 경우, `onConnection` 메서드를 사용하여 작업을 어느 연결로 보낼지 지정할 수 있습니다.

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

`onConnection`과 `onQueue` 메서드를 연결하여, 작업이 사용할 연결과 큐를 동시에 지정할 수 있습니다.

```php
ProcessPodcast::dispatch($podcast)
    ->onConnection('sqs')
    ->onQueue('processing');
```

또는, 작업 클래스의 생성자에서 `onConnection` 메서드를 호출해 연결을 지정할 수도 있습니다.

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

### 최대 작업 시도 횟수 / 타임아웃 값 지정

<a name="max-attempts"></a>
#### 최대 시도 횟수(Max Attempts)

큐에 등록된 작업이 오류를 발생시키는 경우, 해당 작업이 무한정 재시도되는 것을 원하지 않을 것입니다. 따라서 라라벨에서는 작업이 몇 번, 또는 얼마 동안 시도될 수 있는지 다양한 방법으로 지정할 수 있습니다.

가장 기본적인 방법은 Artisan 명령행에서 `--tries` 옵션을 사용하는 것입니다. 이 옵션을 지정하면 워커가 처리하는 모든 작업에 해당 횟수가 적용됩니다. 단, 작업 클래스 내에서 별도로 최대 시도 횟수를 지정한 경우, 그 값이 우선 적용됩니다.

```shell
php artisan queue:work --tries=3
```

작업이 최대 시도 횟수를 초과하면 "실패한 작업"으로 간주됩니다. 실패한 작업 처리 방법에 대해서는 [실패한 작업 문서](#dealing-with-failed-jobs)를 참고하십시오. 만약 `queue:work` 명령에 `--tries=0`을 지정하면, 해당 작업은 무한정 재시도됩니다.

더 세밀하게 컨트롤하고 싶으면, 작업 클래스에서 최대 시도 횟수를 직접 지정할 수 있습니다. 만약 작업 클래스에서 최대 시도 횟수를 지정하면, 명령행의 `--tries` 값보다 우선 적용됩니다.

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

특정 작업의 최대 시도 횟수를 동적으로 제어해야 하는 경우, 작업 클래스에 `tries` 메서드를 정의할 수 있습니다.

```php
/**
 * 작업이 시도될 최대 횟수 결정
 */
public function tries(): int
{
    return 5;
}
```

<a name="time-based-attempts"></a>
#### 시간 기반 시도(Time Based Attempts)

실패하기 전, 작업이 몇 번 시도될지 대신, 작업이 더 이상 실행되지 않아야 하는 시점을 지정할 수도 있습니다. 이 방식을 사용하면 정해진 시간 내에 제한 없이 작업이 여러 번 시도될 수 있습니다. 작업이 시도될 최대 시간을 지정하려면, 작업 클래스에 `retryUntil` 메서드를 추가하면 됩니다. 이 메서드는 `DateTime` 인스턴스를 반환해야 합니다.

```php
use DateTime;

/**
 * 작업이 중단될 시간을 결정
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(10);
}
```

`retryUntil`과 `tries`가 모두 정의된 경우, 라라벨은 `retryUntil` 메서드를 우선 적용합니다.

> [!NOTE]
> [큐잉된 이벤트 리스너](/docs/12.x/events#queued-event-listeners)나 [큐잉된 알림](/docs/12.x/notifications#queueing-notifications)에도 `tries` 속성이나 `retryUntil` 메서드를 정의할 수 있습니다.

<a name="max-exceptions"></a>
#### 최대 예외 횟수(Max Exceptions)

작업이 여러 번 시도되더라도, 미처리된 예외가 일정 횟수 이상 발생하면 작업을 실패로 처리하고 싶을 때가 있습니다. (예: `release` 메서드에 의한 반복이 아니라, 실제로 예외가 반복적으로 발생하는 경우) 이를 위해 작업 클래스에 `maxExceptions` 속성을 지정할 수 있습니다.

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
     * 실패 처리 전 허용할 최대 미처리 예외 수
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
            // Lock을 획득했을 때, 팟캐스트 처리...
        }, function () {
            // Lock 획득 실패...
            return $this->release(10);
        });
    }
}
```

위 예시에서는, 레디스 Lock 획득에 실패하면 작업이 10초 동안 release되고, 최대 25번까지 재시도됩니다. 그러나, 작업이 3번 이상 미처리 예외를 던지면 실패한 작업으로 처리됩니다.

<a name="timeout"></a>
#### 타임아웃(Timeout)

대부분의 경우, 큐에 등록한 작업이 어느 정도 시간 내에 완료되길 기대할 것입니다. 이를 위해 라라벨에서는 "타임아웃" 값을 지정할 수 있습니다. 기본 타임아웃은 60초입니다. 작업이 지정된 초 수 이상 실행되면, 해당 작업을 처리하던 워커는 에러와 함께 종료됩니다. 보통 서버에 구성된 [프로세스 매니저](#supervisor-configuration)가 워커를 자동으로 재시작합니다.

작업 실행의 최대 시간을 지정하려면 Artisan 명령행에서 `--timeout` 옵션을 사용할 수 있습니다.

```shell
php artisan queue:work --timeout=30
```

작업이 계속 타임아웃되어 최대 시도 횟수를 넘기면, 해당 작업은 실패로 기록됩니다.

작업 클래스 내에서도 최대 실행 시간을 설정할 수 있으며, 이때는 클래스의 설정이 명령행 옵션보다 우선합니다.

```php
<?php

namespace App\Jobs;

class ProcessPodcast implements ShouldQueue
{
    /**
     * 작업이 타임아웃되기 전까지 허용되는 최대 초
     *
     * @var int
     */
    public $timeout = 120;
}
```

가끔 소켓, 외부 HTTP 연결 등 IO 블로킹이 있는 프로세스의 경우 지정한 타임아웃이 제대로 적용되지 않을 수 있습니다. 이런 기능을 사용할 때는 각 라이브러리나 API에서 별도로 타임아웃을 설정하는 것이 좋습니다. 예를 들어, Guzzle을 사용하는 경우 연결/요청 타임아웃을 반드시 설정하십시오.

> [!WARNING]
> 작업 타임아웃을 지정하려면 `pcntl` PHP 확장 모듈이 반드시 설치되어 있어야 합니다. 또한, 작업의 "timeout" 값은 항상 ["retry after"](#job-expiration) 값보다 작아야 하며, 그렇지 않으면 작업이 실제로 종료(또는 타임아웃)되기 전에 재시도가 발생할 수 있습니다.

<a name="failing-on-timeout"></a>
#### 타임아웃시 작업을 실패로 처리하기

타임아웃이 발생시 해당 작업을 [실패한 작업](#dealing-with-failed-jobs)으로 표시하고 싶다면, 작업 클래스에 `$failOnTimeout` 속성을 지정하면 됩니다.

```php
/**
 * 타임아웃 시 해당 작업을 실패로 표시할지 여부
 *
 * @var bool
 */
public $failOnTimeout = true;
```

<a name="error-handling"></a>
### 에러 처리(Error Handling)

작업 실행 중에 예외가 발생하면, 해당 작업은 자동으로 큐에 다시 릴리즈(release)되어 재시도하게 됩니다. 작업은 애플리케이션이 허용하는 최대 시도 횟수까지 반복 릴리즈/실행됩니다. 최대 시도 횟수는 `queue:work` Artisan 명령에서 사용하는 `--tries` 옵션이나, 작업 클래스 내에서 개별적으로 정의할 수 있습니다. 큐 워커 실행에 대한 자세한 내용은 [아래에서 확인할 수 있습니다](#running-the-queue-worker).

<a name="manually-releasing-a-job"></a>
#### 작업을 수동으로 릴리즈하기

작업을 수동으로 큐에 다시 릴리즈하여 나중에 다시 시도하게 하고 싶을 경우, `release` 메서드를 호출하면 됩니다.

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

기본적으로 `release` 메서드는 해당 작업을 즉시 큐로 되돌립니다. 하지만, 정수나 날짜 인스턴스를 인자로 전달함으로써 지정한 시간(초)만큼 대기 후 다시 처리되게 할 수 있습니다.

```php
$this->release(10);

$this->release(now()->addSeconds(10));
```

<a name="manually-failing-a-job"></a>
#### 작업을 수동으로 실패 처리하기

경우에 따라 작업을 수동으로 "실패" 상태로 표시하고 싶을 수 있습니다. 이 경우 `fail` 메서드를 호출하면 됩니다.

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

직접 캐치한 예외 때문에 작업을 실패로 처리하고 싶으면, 예외를 `fail` 메서드에 인자로 전달할 수 있습니다. 또는, 문자열 형태의 에러 메시지를 전달하면 라라벨이 해당 메시지를 포함한 예외로 변환해줍니다.

```php
$this->fail($exception);

$this->fail('문제가 발생했습니다.');
```

> [!NOTE]
> 실패한 작업에 대한 자세한 내용은 [실패한 작업 처리 문서](#dealing-with-failed-jobs)를 참고하세요.

<a name="fail-jobs-on-exceptions"></a>
#### 특정 예외 발생 시 작업 실패 처리

`FailOnException` [작업 미들웨어](#job-middleware)를 사용하면 특정 예외가 발생했을 때 재시도 없이 즉시 작업을 실패 처리할 수 있습니다. 예를 들어, 외부 API 에러와 같은 일시적 예외에서는 재시도를 허용하지만, 사용자의 권한이 박탈된 경우와 같은 영구적 예외에서는 작업을 바로 실패로 처리하는 것이 가능합니다.

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
     * 새 작업 인스턴스 생성
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
     * 적용할 미들웨어 반환
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
## 작업 배치(Job Batching)

라라벨의 작업 배치 기능을 이용하면 여러 작업을 손쉽게 한 번에 실행하고, 전체 작업이 완료된 후 추가적인 동작을 수행할 수 있습니다. 사용 전에, 각 작업 배치의 진행 상황(예: 완료 퍼센트 등)과 관련된 메타 정보를 저장할 테이블을 위한 데이터베이스 마이그레이션을 먼저 생성해야 합니다. 이 마이그레이션은 `make:queue-batches-table` Artisan 명령어로 만들 수 있습니다.

```shell
php artisan make:queue-batches-table

php artisan migrate
```

<a name="defining-batchable-jobs"></a>
### 배치 작업 정의하기

배치 가능한 작업을 정의하려면, [일반적으로 큐 작업을 생성](#creating-jobs)하듯 생성하되, 작업 클래스에 `Illuminate\Bus\Batchable` 트레이트를 추가합니다. 이 트레이트를 사용하면 현재 작업이 어떤 배치 안에서 실행되고 있는지 확인할 수 있는 `batch` 메서드에 접근할 수 있습니다.

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

        // CSV 파일의 일부를 가져오기...
    }
}
```

<a name="dispatching-batches"></a>
### 배치 작업 디스패치하기

여러 작업을 하나의 배치로 디스패치하려면 `Bus` 파사드의 `batch` 메서드를 사용합니다. 보통, 배치 기능은 완료 콜백과 함께 사용될 때 유용합니다. 따라서, `then`, `catch`, `finally` 등의 메서드로 배치 완료 시 실행할 콜백을 정의할 수 있습니다. 각 콜백은 호출될 때 `Illuminate\Bus\Batch` 인스턴스를 전달받습니다. 아래 예제에서는 CSV 파일의 여러 행을 각각 처리하는 일련의 작업들을 배치로 큐에 등록하는 상황을 가정하였습니다.

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
    // 배치가 생성됐지만 아직 작업이 추가되지 않은 상태...
})->progress(function (Batch $batch) {
    // 개별 작업이 하나 성공적으로 완료됨...
})->then(function (Batch $batch) {
    // 모든 작업이 성공적으로 완료됨...
})->catch(function (Batch $batch, Throwable $e) {
    // 배치 내 첫 번째 작업 실패 감지...
})->finally(function (Batch $batch) {
    // 배치 실행이 모두 끝남...
})->dispatch();

return $batch->id;
```

배치 ID는 `$batch->id`로 접근할 수 있으며, [라라벨 커맨드 버스](#inspecting-batches)에서 해당 배치에 관한 정보를 조회하는 데 사용할 수 있습니다.

> [!WARNING]
> 배치 콜백은 큐에 의해 직렬화되어 나중에 실행되므로, 콜백 내부에서는 `$this` 변수를 사용해서는 안 됩니다. 또한, 배치 작업은 데이터베이스 트랜잭션 내에서 실행되기 때문에, 암묵적 커밋을 유발하는 DB 구문은 배치 작업 내에서 사용하지 않도록 주의하세요.

<a name="naming-batches"></a>
#### 배치 이름 지정하기

라라벨 Horizon, 라라벨 Telescope 등 일부 도구는 배치에 이름이 지정되어 있을 때 좀 더 친절한 디버그 정보를 제공할 수 있습니다. 배치의 이름을 지정하려면, 배치를 정의할 때 `name` 메서드를 호출하면 됩니다.

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // 모든 작업이 성공적으로 완료됨...
})->name('Import CSV')->dispatch();
```

<a name="batch-connection-queue"></a>
#### 배치의 커넥션 및 큐 지정

배치 작업에 사용할 연결(Connection)과 큐(Queue)를 지정하고 싶다면, `onConnection`, `onQueue` 메서드를 사용할 수 있습니다. 모든 배치 작업은 동일한 커넥션과 큐에서 실행되어야 합니다.

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // 모든 작업이 성공적으로 완료됨...
})->onConnection('redis')->onQueue('imports')->dispatch();
```

<a name="chains-and-batches"></a>
### 체인과 배치(Chains and Batches)

배치 내에서 [체인 작업](#job-chaining) 집합을 정의하려면, 각각의 체인 작업들을 배열로 감싸주면 됩니다. 예를 들어, 두 개의 작업 체인을 병렬로 실행하고, 두 체인 모두 처리가 끝나면 콜백을 실행하도록 할 수 있습니다.

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

반대로, [체인](#job-chaining) 내부에서 여러 개의 배치 작업을 실행할 수도 있습니다. 예를 들어, 먼저 여러 팟캐스트를 배포하는 작업을 배치로 실행한 후, 배포 알림 전송 작업을 또 다른 배치로 실행할 수 있습니다.

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

경우에 따라, 배치에 속한 특정 작업이 실행되는 중에, 새로운 작업을 배치에 추가하고 싶을 수 있습니다. 이 패턴은 수천 개의 작업을 한 번에 웹 요청으로 디스패치하기에는 너무 시간이 오래 걸릴 때 유용합니다. 대신, 일단 "로더" 작업들을 먼저 배치로 등록하고, 그 작업이 추가 작업들을 동적으로 배치에 넣을 수 있습니다.

```php
$batch = Bus::batch([
    new LoadImportBatch,
    new LoadImportBatch,
    new LoadImportBatch,
])->then(function (Batch $batch) {
    // 모든 작업이 성공적으로 완료됨...
})->name('Import Contacts')->dispatch();
```

이 예제에서, `LoadImportBatch` 작업에서 추가 작업들을 동적으로 배치에 주입하게 됩니다. 이를 위해 작업의 `batch` 메서드를 통해 얻은 배치 인스턴스에서 `add` 메서드를 사용할 수 있습니다.

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
> 똑같은 배치에 속한 작업 내에서만 배치에 새로운 작업을 추가할 수 있습니다.

<a name="inspecting-batches"></a>
### 배치 정보 조회하기

배치 완료 콜백 등에서 전달되는 `Illuminate\Bus\Batch` 인스턴스는, 현재 배치에 대한 다양한 속성과 메서드를 제공하여, 배치 내 작업들의 상태를 확인하거나 상호작용할 수 있습니다.

```php
// 배치의 UUID...
$batch->id;

// 배치 이름(지정된 경우)...
$batch->name;

// 배치에 할당된 총 작업 수...
$batch->totalJobs;

// 큐에서 아직 처리되지 않은 작업 수...
$batch->pendingJobs;

// 실패한 작업 수...
$batch->failedJobs;

// 지금까지 처리된 작업 수...
$batch->processedJobs();

// 배치의 완료 퍼센트(0~100)...
$batch->progress();

// 배치 실행이 완료됐는지 여부...
$batch->finished();

// 배치 실행 취소...
$batch->cancel();

// 배치가 취소됐는지 여부...
$batch->cancelled();
```

<a name="returning-batches-from-routes"></a>
#### 라우트에서 배치 반환하기

모든 `Illuminate\Bus\Batch` 인스턴스는 JSON으로 변환이 가능하기 때문에, 애플리케이션의 라우트에서 직접 반환하여, 해당 배치의 완료율 등 정보를 JSON 형태로 받아볼 수 있습니다. 이를 통해, UI에서 각 배치 진행 상황을 손쉽게 보여줄 수 있습니다.

배치 ID로 배치를 조회하려면, `Bus` 파사드의 `findBatch` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Support\Facades\Bus;
use Illuminate\Support\Facades\Route;

Route::get('/batch/{batchId}', function (string $batchId) {
    return Bus::findBatch($batchId);
});
```

<a name="cancelling-batches"></a>
### 배치 실행 취소하기

특정 배치 실행을 취소해야 할 때, `Illuminate\Bus\Batch` 인스턴스의 `cancel` 메서드를 호출하면 됩니다.

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

앞선 예제들에서 볼 수 있듯, 배치에 속한 작업들은 실행 전 배치가 취소되었는지 확인하는 것이 일반적입니다. 그러나 더 편리하게 처리하고 싶다면, 작업에 `SkipIfBatchCancelled` [미들웨어](#job-middleware)를 지정할 수 있습니다. 이 미들웨어를 사용하면, 배치가 취소된 경우 해당 작업은 아예 실행되지 않습니다.

```php
use Illuminate\Queue\Middleware\SkipIfBatchCancelled;

/**
 * 적용할 미들웨어 반환
 */
public function middleware(): array
{
    return [new SkipIfBatchCancelled];
}
```

<a name="batch-failures"></a>
### 배치 실패 처리

배치 내 작업이 실패하면, `catch` 콜백(정의된 경우)이 호출됩니다. 이 콜백은 배치 내 첫 번째 작업이 실패했을 때만 실행됩니다.

<a name="allowing-failures"></a>

#### 실패 허용

배치 내의 작업이 실패할 경우 라라벨은 자동으로 해당 배치를 "취소됨" 상태로 표시합니다. 만약 작업이 실패하더라도 배치가 자동으로 취소 상태가 되지 않도록 하려면, 이러한 동작을 비활성화할 수 있습니다. 이를 위해 배치를 디스패치할 때 `allowFailures` 메서드를 호출하면 됩니다.

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // 모든 작업이 정상적으로 완료됨...
})->allowFailures()->dispatch();
```

<a name="retrying-failed-batch-jobs"></a>
#### 실패한 배치 작업 재시도

라라벨은 편리하게도, 특정 배치의 실패한 모든 작업을 쉽게 재시도할 수 있도록 `queue:retry-batch` 아티즌 명령어를 제공합니다. `queue:retry-batch` 명령어는 실패한 작업을 재시도할 배치의 UUID를 인자로 받습니다.

```shell
php artisan queue:retry-batch 32dbc76c-4f82-4749-b610-a639fe0099b5
```

<a name="pruning-batches"></a>
### 배치 레코드 정리(Pruning)

정리 작업을 하지 않으면, `job_batches` 테이블에 레코드가 매우 빠르게 누적될 수 있습니다. 이를 방지하기 위해, [스케줄러](/docs/12.x/scheduling)를 활용하여 `queue:prune-batches` 아티즌 명령어를 매일 실행하도록 예약하는 것이 좋습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches')->daily();
```

기본적으로, 완료된 지 24시간이 지난 모든 배치는 정리(prune)됩니다. 명령어 실행 시 `hours` 옵션을 사용하여 배치 데이터를 얼마 동안 유지할지 지정할 수 있습니다. 예를 들어, 아래 명령어는 48시간 이전에 완료된 모든 배치를 삭제합니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48')->daily();
```

때때로 `jobs_batches` 테이블에는 성공적으로 완료되지 않은 배치(예: 작업이 실패해서 재시도가 이루어지지 않은 배치)에 대한 기록이 남을 수 있습니다. 이런 완료되지 않은 배치 레코드도 `unfinished` 옵션을 사용하여 정리하도록 명령할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48 --unfinished=72')->daily();
```

마찬가지로, `jobs_batches` 테이블에는 취소된 배치의 기록도 누적될 수 있습니다. `cancelled` 옵션을 사용하여 이러한 취소된 배치 레코드를 정리하도록 지정할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48 --cancelled=72')->daily();
```

<a name="storing-batches-in-dynamodb"></a>
### DynamoDB에 배치 저장

라라벨은 배치 메타 정보를 관계형 데이터베이스 대신 [DynamoDB](https://aws.amazon.com/dynamodb)에 저장하는 기능도 지원합니다. 단, 모든 배치 레코드를 저장할 DynamoDB 테이블을 직접 생성해야 합니다.

일반적으로 이 테이블의 이름은 `job_batches`이어야 하지만, 애플리케이션의 `queue` 설정 파일 내의 `queue.batching.table` 구성 값에 따라 이름을 정해야 합니다.

<a name="dynamodb-batch-table-configuration"></a>
#### DynamoDB 배치 테이블 구성

`job_batches` 테이블에는 문자열 타입의 파티션 키인 `application`과 문자열 타입의 정렬 키인 `id`가 있어야 합니다. `application` 부분에는 애플리케이션의 `app` 설정 파일에서 지정한 `name` 구성 값이 저장됩니다. 애플리케이션 이름이 이 테이블의 키 일부로 사용되므로, 여러분은 여러 라라벨 애플리케이션의 작업 배치를 한 테이블에 저장할 수 있습니다.

또한, 자동 배치 정리 기능을 사용하려면 테이블에 `ttl` 속성(attribute)을 정의할 수 있습니다. ([DynamoDB에서 자동 배치 정리](#pruning-batches-in-dynamodb) 참고)

<a name="dynamodb-configuration"></a>
#### DynamoDB 설정

이제 라라벨 애플리케이션이 Amazon DynamoDB와 통신할 수 있도록 AWS SDK를 설치하세요.

```shell
composer require aws/aws-sdk-php
```

그런 다음, `queue.batching.driver` 설정 값을 `dynamodb`로 지정합니다. 추가로, `batching` 설정 배열 안에 `key`, `secret`, `region` 옵션들을 정의해야 합니다. 이 옵션들은 AWS 인증에 사용됩니다. `dynamodb` 드라이버를 사용할 때는 `queue.batching.database` 옵션이 필요하지 않습니다.

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

[DynamoDB](https://aws.amazon.com/dynamodb)에 작업 배치 정보를 저장하는 경우, 관계형 데이터베이스에서 배치 데이터를 정리하는 일반 명령어는 동작하지 않습니다. 대신 [DynamoDB 자체의 TTL 기능](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html)을 활용하여 오래된 배치 레코드를 자동으로 삭제할 수 있습니다.

DynamoDB 테이블에 `ttl` 속성을 정의했다면, 라라벨에서 어떻게 배치 레코드를 정리할지 알려주는 설정값을 지정할 수 있습니다. `queue.batching.ttl_attribute` 설정 값은 TTL을 저장하는 속성명을 지정하며, `queue.batching.ttl`은 마지막 업데이트 시점을 기준으로 해당 초(second)가 지나면 배치 레코드를 DynamoDB 테이블에서 삭제할 수 있도록 합니다.

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
## 클로저(Closure)를 큐에 등록하기

작업(Job) 클래스 대신 클로저를 큐에 디스패치할 수도 있습니다. 이는 간단한 작업을 현재 요청과 별개로 빠르게 실행하고자 할 때 유용합니다. 클로저를 큐에 디스패치할 때, 클로저 코드의 내용은 암호학적으로 서명되어 전송 중에 수정될 수 없도록 보호됩니다.

```php
$podcast = App\Podcast::find(1);

dispatch(function () use ($podcast) {
    $podcast->publish();
});
```

큐에 등록된 클로저에 이름을 지정하고 싶다면, `name` 메서드를 사용할 수 있습니다. 이 이름은 큐 대시보드 보고에 활용되거나 `queue:work` 명령어에서 표시됩니다.

```php
dispatch(function () {
    // ...
})->name('Publish Podcast');
```

또한, `catch` 메서드를 사용하여, 큐에 등록된 클로저가 모든 [재시도 횟수](#max-job-attempts-and-timeout)를 소진한 후에도 정상적으로 완료되지 않을 경우 실행할 클로저를 지정할 수 있습니다.

```php
use Throwable;

dispatch(function () use ($podcast) {
    $podcast->publish();
})->catch(function (Throwable $e) {
    // 이 작업이 실패함...
});
```

> [!WARNING]
> `catch` 콜백은 라라벨 큐에 의해 직렬화된 후 나중에 실행되기 때문에, `catch` 콜백 내부에서 `$this` 변수를 사용해서는 안 됩니다.

<a name="running-the-queue-worker"></a>
## 큐 워커 실행하기

<a name="the-queue-work-command"></a>
### `queue:work` 명령어

라라벨은 큐 워커를 시작하고 큐로 들어오는 새 작업을 처리하는 아티즌 명령어를 제공합니다. `queue:work` 아티즌 명령어를 사용하여 워커를 실행할 수 있습니다. 명령어가 시작되면 수동으로 중지하거나 터미널을 닫을 때까지 계속 실행됩니다.

```shell
php artisan queue:work
```

> [!NOTE]
> `queue:work` 프로세스를 백그라운드에서 계속 실행하려면, [Supervisor](#supervisor-configuration) 같은 프로세스 관리자를 사용하여 워커가 중단 없이 동작하도록 설정하는 것을 권장합니다.

워크에 의해 처리된 작업 ID 정보를 명령어 출력에 포함시키고 싶다면 `-v` 플래그를 함께 사용할 수 있습니다.

```shell
php artisan queue:work -v
```

큐 워커는 장기간 실행되는 프로세스이며, 애플리케이션의 기동 상태를 메모리에 유지합니다. 따라서 워커가 시작된 후 코드가 변경되어도 이를 감지하지 못합니다. 배포 과정 중에는 반드시 [큐 워커를 재시작](#queue-workers-and-deployment)해야 합니다. 또한, 애플리케이션에서 생성되거나 수정된 모든 static 상태는 작업 간에 자동으로 초기화되지 않음을 기억하세요.

대안으로는 `queue:listen` 명령어를 사용할 수도 있습니다. 이 명령어는 코드 수정이나 애플리케이션 상태 리셋이 필요할 때 워커를 수동으로 재시작하지 않아도 됩니다. 그러나 `queue:work` 명령어보다 성능이 낮으니 가급적이면 `queue:work` 사용을 권장합니다.

```shell
php artisan queue:listen
```

<a name="running-multiple-queue-workers"></a>
#### 여러 큐 워커 실행하기

여러 워커를 큐에 할당하고 동시에 작업을 처리하려면, 단순히 여러 개의 `queue:work` 프로세스를 실행하면 됩니다. 이는 로컬에서 터미널을 여러 개 띄워 실행하거나 운영 환경에서는 프로세스 관리자 설정을 통해 가능합니다. [Supervisor 사용 시](#supervisor-configuration) `numprocs` 옵션을 활용할 수 있습니다.

<a name="specifying-the-connection-queue"></a>
#### 연결(Connection) 및 큐(Queue) 지정하기

워커가 어떤 큐 연결을 사용할지 지정할 수도 있습니다. `work` 명령어에 전달하는 연결 이름은 `config/queue.php` 구성 파일에 정의된 커넥션 중 하나여야 합니다.

```shell
php artisan queue:work redis
```

기본적으로, `queue:work` 명령어는 지정한 커넥션의 기본 큐에 저장된 작업만 처리합니다. 특정 큐만 고집해서 처리하고 싶다면, 예를 들어 이메일 발송 작업이 `redis` 커넥션의 `emails` 큐로만 들어온다면 아래처럼 해당 큐만 처리하도록 워커를 시작하면 됩니다.

```shell
php artisan queue:work redis --queue=emails
```

<a name="processing-a-specified-number-of-jobs"></a>
#### 지정된 개수의 작업 처리

`--once` 옵션을 사용하면 워커가 큐에서 단 한 건의 작업만 처리하도록 할 수 있습니다.

```shell
php artisan queue:work --once
```

`--max-jobs` 옵션을 사용하면 워커가 주어진 수만큼의 작업만 처리한 후 종료하도록 할 수 있습니다. 이 기능은 [Supervisor](#supervisor-configuration)와 같이 사용하면, 워커가 지정된 작업 수만큼 처리한 뒤 자동으로 재시작돼 누적된 메모리가 해제되는 데 유용합니다.

```shell
php artisan queue:work --max-jobs=1000
```

<a name="processing-all-queued-jobs-then-exiting"></a>
#### 대기 중인 모든 작업을 처리 후 종료

`--stop-when-empty` 옵션을 사용하면 워커가 큐에 쌓인 모든 작업을 처리한 후 정상적으로 종료합니다. 이 옵션은 Docker 컨테이너에서 라라벨 큐를 실행할 때, 큐가 모두 비워진 후 컨테이너를 안전하게 종료하고픈 경우에 유용합니다.

```shell
php artisan queue:work --stop-when-empty
```

<a name="processing-jobs-for-a-given-number-of-seconds"></a>
#### 일정 시간 동안만 작업 처리

`--max-time` 옵션을 사용하면 워커가 지정된 초(Second)만큼만 작업을 처리한 뒤 종료하도록 만들 수 있습니다. 이 옵션 역시 [Supervisor](#supervisor-configuration)와 조합해 사용할 때 유용합니다. 지정된 시간이 경과하면 워커가 자동으로 재시작되어 누적된 메모리가 해제됩니다.

```shell
# 한 시간(3600초) 동안 작업을 처리한 뒤 종료...
php artisan queue:work --max-time=3600
```

<a name="worker-sleep-duration"></a>
#### 워커 대기(Sleep) 시간 설정

큐에 작업이 있을 때 워커는 중단 없이 계속해서 작업을 처리합니다. 다만, 작업이 없을 때 워커가 "잠자기"할 시간(초 단위)은 `sleep` 옵션으로 지정합니다. 워커가 대기 중인 동안엔 새로운 작업을 처리하지 않습니다.

```shell
php artisan queue:work --sleep=3
```

<a name="maintenance-mode-queues"></a>
#### 유지보수 모드와 큐

애플리케이션이 [유지보수 모드](/docs/12.x/configuration#maintenance-mode)에 들어간 경우, 큐에 들어온 작업은 처리되지 않습니다. 유지보수 모드가 종료되면 다시 정상적으로 작업이 처리됩니다.

유지보수 모드에서도 강제로 큐 워커가 작업을 처리하게 하려면, `--force` 옵션을 사용할 수 있습니다.

```shell
php artisan queue:work --force
```

<a name="resource-considerations"></a>
#### 리소스 관리 유의사항

데몬 큐 워커는 각각의 작업을 처리할 때마다 프레임워크를 "재시작"하지 않기 때문에, 무거운 리소스는 각 작업이 끝날 때 직접 해제해야 합니다. 예를 들어, GD 라이브러리를 활용한 이미지 처리를 한다면, 작업 완료 후 `imagedestroy`로 메모리를 해제해야 합니다.

<a name="queue-priorities"></a>
### 큐 우선순위

가끔은 큐의 처리 우선순위를 조정하고 싶을 때가 있습니다. 예를 들어, `config/queue.php`에 `redis` 커넥션의 기본 큐를 `low`로 설정해두었다고 해봅시다. 그런데 특정 작업을 더 높은 우선순위의 큐(예: `high`)에 넣고 싶다면 다음과 같이 할 수 있습니다.

```php
dispatch((new Job)->onQueue('high'));
```

`high` 큐의 작업을 모두 우선 처리한 뒤에 `low` 큐 작업으로 넘어가길 원한다면, 큐 이름을 쉼표(,)로 여러 개 나열해 `work` 명령어에 전달하면 됩니다.

```shell
php artisan queue:work --queue=high,low
```

<a name="queue-workers-and-deployment"></a>
### 큐 워커와 배포

큐 워커는 장기간 실행되는 프로세스이기 때문에, 코드가 변경돼도 자동으로 감지할 수 없습니다. 따라서 애플리케이션을 배포할 때는 큐 워커를 반드시 재시작해야 합니다. 모든 워커를 정상적으로 종료시킨 후 재시작하려면 `queue:restart` 명령어를 실행하세요.

```shell
php artisan queue:restart
```

이 명령어는 현재 처리 중인 작업이 완료되는 즉시 워커에게 종료를 지시하므로, 기존 작업이 유실되지 않습니다. 워커가 종료되면 [Supervisor](#supervisor-configuration) 같은 프로세스 관리자를 이용해 자동 재시작되도록 해야 합니다.

> [!NOTE]
> 큐 워커 재시작 신호는 [캐시](/docs/12.x/cache)를 활용하여 저장됩니다. 따라서 이 기능을 사용하기 전 애플리케이션에 적절한 캐시 드라이버가 설정돼 있는지 반드시 확인해야 합니다.

<a name="job-expirations-and-timeouts"></a>
### 작업(Job) 만료 및 타임아웃

<a name="job-expiration"></a>
#### 작업 만료

`config/queue.php` 설정 파일에서 각 큐 연결별로 `retry_after` 옵션을 설정할 수 있습니다. 이 값은 지정된 초만큼 작업 처리가 지연되면, 해당 작업을 다시 큐에 반환하여 재시도 시점을 지정합니다. 예를 들어, `retry_after` 값이 90이면, 해당 작업이 90초 동안 처리되지 않거나 삭제되지 않은 경우 작업은 다시 큐에 반환됩니다. 일반적으로, 이 값은 여러분의 작업이 합리적으로 끝나야 하는 최대 초 수로 설정해야 합니다.

> [!WARNING]
> `retry_after` 옵션이 없는 유일한 큐 연결은 Amazon SQS입니다. SQS는 [기본 가시성 타임아웃(Default Visibility Timeout)](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/AboutVT.html)에 따라 재시도합니다. 이 값은 AWS 콘솔에서 관리됩니다.

<a name="worker-timeouts"></a>
#### 워커 타임아웃

`queue:work` 아티즌 명령어는 `--timeout` 옵션을 사용합니다. 기본값은 60초입니다. 작업이 지정한 타임아웃을 초과해 처리될 경우, 해당 작업을 실행 중이던 워커는 에러와 함께 종료됩니다. 일반적으로, [서버에 프로세스 관리자를 설정](#supervisor-configuration)해두면 워커는 자동으로 재시작됩니다.

```shell
php artisan queue:work --timeout=60
```

`retry_after` 옵션과 `--timeout` 옵션은 서로 다르지만, 작업이 유실되지 않고 한 번만 정상적으로 처리되도록 함께 작동합니다.

> [!WARNING]
> `--timeout` 값은 반드시 `retry_after` 값보다 몇 초라도 더 짧게 설정해야 합니다. 그래야 멈춘 작업을 처리하던 워커가 항상 재시도 전에 종료됩니다. 반대로 `--timeout` 값이 더 크면 작업이 중복 처리될 수 있습니다.

<a name="supervisor-configuration"></a>
## Supervisor(슈퍼바이저) 설정

운영 환경에서는 `queue:work` 프로세스가 항상 동작하도록 해야 합니다. 워커 프로세스는 워커 타임아웃 초과나 `queue:restart` 명령 실행 등 여러 이유로 종료될 수 있습니다.

따라서, 프로세스가 종료되면 자동으로 재시작하고, 동시에 몇 개의 워커를 병렬로 실행할지 지정할 수 있는 프로세스 관리자를 설정해야 합니다. Supervisor는 리눅스 환경에서 널리 사용되는 프로세스 관리자이며, 아래에서 사용하는 방법을 안내합니다.

<a name="installing-supervisor"></a>
#### Supervisor 설치

Supervisor는 리눅스 운영체제용 프로세스 관리자로, `queue:work` 프로세스가 실패하더라도 자동 재시작해줍니다. Ubuntu에서 Supervisor를 설치하려면 다음 명령어를 실행하세요.

```shell
sudo apt-get install supervisor
```

> [!NOTE]
> 직접 Supervisor 설치·관리가 부담스럽다면, 라라벨 큐 워커를 위임해서 운영할 수 있는 완전관리형 플랫폼 [Laravel Cloud](https://cloud.laravel.com) 이용을 고려해보세요.

<a name="configuring-supervisor"></a>
#### Supervisor 설정

Supervisor 설정 파일은 일반적으로 `/etc/supervisor/conf.d` 디렉터리에 저장됩니다. 이 디렉터리 안에 여러 설정 파일을 만들어 여러분의 프로세스를 어떻게 모니터링할지 지정할 수 있습니다. 예를 들어, `queue:work` 프로세스를 시작하고 모니터링하는 `laravel-worker.conf` 파일을 아래와 같이 만들 수 있습니다.

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

이 예시에서 `numprocs` 지시어는 Supervisor에게 8개의 `queue:work` 프로세스를 실행하고 모니터링하도록 지시합니다. 설정 파일의 `command` 부분은 원하는 큐 연결과 워커 옵션에 맞게 반드시 수정해야 합니다.

> [!WARNING]
> `stopwaitsecs`의 값이 가장 오래 걸리는 작업의 시간보다 항상 커야 합니다. 그렇지 않으면 Supervisor가 작업이 끝나기 전에 프로세스를 강제로 종료시킬 수 있습니다.

<a name="starting-supervisor"></a>
#### Supervisor 시작하기

설정 파일을 만든 후, 아래 명령어로 Supervisor 설정을 갱신하고 프로세스를 시작합니다.

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start "laravel-worker:*"
```

Supervisor에 대한 더 자세한 정보는 [Supervisor 공식 문서](http://supervisord.org/index.html)를 참고하세요.

<a name="dealing-with-failed-jobs"></a>
## 실패한 작업 처리하기

가끔은 큐에 등록된 작업이 실패할 수 있습니다. 당황할 필요 없습니다! 라라벨에는 [최대 시도 횟수 지정](#max-job-attempts-and-timeout)과, 비동기 작업이 이 횟수를 초과하면 해당 작업을 `failed_jobs` 데이터베이스 테이블에 저장하는 기능이 내장되어 있습니다. [동기식으로 디스패치한 작업](/docs/12.x/queues#synchronous-dispatching)이 실패할 경우에는 이 테이블에 저장되지 않고 예외가 바로 애플리케이션에서 처리됩니다.

`failed_jobs` 테이블을 만드는 마이그레이션은 새 라라벨 애플리케이션에 기본 포함되어 있습니다. 애플리케이션에 이 테이블의 마이그레이션이 없다면, 다음과 같이 `make:queue-failed-table` 명령어로 생성할 수 있습니다.

```shell
php artisan make:queue-failed-table

php artisan migrate
```

[큐 워커](#running-the-queue-worker) 프로세스를 실행할 때, `queue:work` 명령어의 `--tries` 옵션으로 각 작업의 최대 시도 횟수를 지정할 수 있습니다. 값을 지정하지 않으면 작업은 한 번만 실행되거나, 작업 클래스의 `$tries` 속성에 지정한 횟수만큼만 시도합니다.

```shell
php artisan queue:work redis --tries=3
```

`--backoff` 옵션을 사용하면, 작업이 예외에 부딪혀 재시도할 때 대기할 초 단위를 지정할 수 있습니다. 기본적으로는 작업이 즉시 다시 큐에 반환됩니다.

```shell
php artisan queue:work redis --tries=3 --backoff=3
```

작업별로 예외 발생 시 몇 초 후 재시도할지 개별 설정하려면, 작업 클래스에 `backoff` 속성을 정의하면 됩니다.

```php
/**
 * 작업 재시도 전 대기할 초 수
 *
 * @var int
 */
public $backoff = 3;
```

재시도 대기 시간에 더 복잡한 로직이 필요하다면, `backoff` 메서드를 정의해도 됩니다.

```php
/**
 * 재시도 전 대기할 초 수 계산
 */
public function backoff(): int
{
    return 3;
}
```

배열을 반환하면 "지수적 백오프(exponential backoff)"도 쉽게 구성할 수 있습니다. 아래 예시에서 1회 재시도는 1초, 2회째는 5초, 3회째와 이후엔 10초가 각각 대기 시간으로 사용됩니다.

```php
/**
 * 재시도 전 대기할 초 수 계산
 *
 * @return array<int, int>
 */
public function backoff(): array
{
    return [1, 5, 10];
}
```

<a name="cleaning-up-after-failed-jobs"></a>
### 실패한 작업 후 처리

특정 작업이 실패할 때, 사용자에게 알림을 보내거나 작업이 일부만 완료되었다면 이전 상태로 되돌려야 할 수 있습니다. 이를 위해 작업 클래스에 `failed` 메서드를 정의하면 됩니다. 작업 실패를 유발한 `Throwable` 인스턴스가 `failed` 메서드로 전달됩니다.

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
     * 새로운 작업 인스턴스 생성자.
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
     * 작업 실패 처리 메서드.
     */
    public function failed(?Throwable $exception): void
    {
        // 사용자에게 실패 알림 전송 등...
    }
}
```

> [!WARNING]
> `failed` 메서드가 호출되기 전 새 작업 인스턴스가 생성되므로, `handle` 메서드 내에서 변경한 클래스 속성들은 모두 초기화됩니다.

<a name="retrying-failed-jobs"></a>
### 실패한 작업 재시도

`failed_jobs` 데이터베이스 테이블에 저장된 모든 실패한 작업을 확인하려면 `queue:failed` 아티즌 명령어를 이용하면 됩니다.

```shell
php artisan queue:failed
```

`queue:failed` 명령어는 작업 ID, 연결, 큐 이름, 실패 시간 등 다양한 정보를 보여줍니다. 작업 ID를 이용해 특정 실패 작업을 재시도할 수 있습니다. 예를 들어, ID가 `ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece`인 작업을 재시도하려면 다음과 같이 실행합니다.

```shell
php artisan queue:retry ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece
```

필요에 따라 여러 ID를 한꺼번에 전달할 수도 있습니다.

```shell
php artisan queue:retry ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece 91401d2c-0784-4f43-824c-34f94a33c24d
```

특정 큐의 모든 실패 작업을 재시도하려면 아래처럼 실행합니다.

```shell
php artisan queue:retry --queue=name
```

모든 실패 작업을 재시도하려면, ID 대신 `all`을 전달하면 됩니다.

```shell
php artisan queue:retry all
```

특정 실패 작업을 삭제하려면 `queue:forget` 명령어를 사용할 수 있습니다.

```shell
php artisan queue:forget 91401d2c-0784-4f43-824c-34f94a33c24d
```

> [!NOTE]
> [Horizon](/docs/12.x/horizon)을 사용할 경우 실패한 작업 삭제에는 `queue:forget`이 아니라 `horizon:forget` 명령어를 사용해야 합니다.

`failed_jobs` 테이블에 저장된 모든 실패 작업을 삭제하려면 `queue:flush` 명령어를 실행하세요.

```shell
php artisan queue:flush
```

<a name="ignoring-missing-models"></a>
### 존재하지 않는 모델 무시하기

Eloquent 모델을 작업에 주입할 경우, 해당 모델은 큐에 넣을 때 자동으로 직렬화되고, 작업 처리가 시작될 때 데이터베이스에서 다시 불러옵니다. 하지만 작업이 대기하는 동안 모델이 삭제되면, 작업이 `ModelNotFoundException` 예외와 함께 실패할 수 있습니다.

이럴 때, 작업 클래스의 `deleteWhenMissingModels` 속성을 `true`로 지정하면, 모델이 없을 경우 라라벨이 예외를 발생시키지 않고 조용히 작업을 삭제하게 할 수 있습니다.

```php
/**
 * 모델이 더 이상 존재하지 않으면 작업도 즉시 삭제합니다.
 *
 * @var bool
 */
public $deleteWhenMissingModels = true;
```

<a name="pruning-failed-jobs"></a>
### 실패한 작업 레코드 정리

애플리케이션의 `failed_jobs` 테이블을 정리하고 싶다면, `queue:prune-failed` 아티즌 명령어를 사용하세요.

```shell
php artisan queue:prune-failed
```

기본적으로, 24시간이 지난 모든 실패 작업 레코드가 정리됩니다. `--hours` 옵션을 추가하면 최근 N시간 이내 레코드만 남아 있게 할 수 있습니다. 예를 들어, 48시간이 지난 실패 작업만 삭제하려면 다음과 같이 합니다.

```shell
php artisan queue:prune-failed --hours=48
```

<a name="storing-failed-jobs-in-dynamodb"></a>
### 실패한 작업을 DynamoDB에 저장하기

라라벨은 실패한 작업도 [DynamoDB](https://aws.amazon.com/dynamodb)에 저장하는 기능을 지원합니다. 단, 모든 레코드를 저장할 DynamoDB 테이블을 직접 생성해야 합니다. 보통 테이블 이름은 `failed_jobs`로 하고, 이는 애플리케이션의 `queue` 설정 파일 내 `queue.failed.table` 값에 따라 달라질 수 있습니다.

`failed_jobs` 테이블에는 문자열 파티션 키 `application`과 문자열 정렬 키 `uuid`가 있어야 합니다. `application`에는 애플리케이션의 `app` 설정 파일의 `name` 값이 들어갑니다. 애플리케이션 이름이 키 일부이므로, 여러 라라벨 애플리케이션의 작업을 같은 테이블에 저장할 수 있습니다.

또한, 라라벨 애플리케이션이 Amazon DynamoDB와 통신할 수 있도록 AWS SDK 역시 설치해 주어야 합니다.

```shell
composer require aws/aws-sdk-php
```

이제 `queue.failed.driver` 설정 값을 `dynamodb`로 지정하세요. 추가로, 실패 작업 설정 배열에 `key`, `secret`, `region` 옵션을 정의해야 하며, 이는 AWS 인증에 사용됩니다. `dynamodb` 드라이버를 사용할 때는 `queue.failed.database`는 필요하지 않습니다.

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

### 실패한 잡 저장 비활성화

`queue.failed.driver` 설정 값을 `null`로 지정하면, 라라벨이 실패한 잡을 저장하지 않고 바로 폐기하도록 할 수 있습니다. 일반적으로, 이는 `QUEUE_FAILED_DRIVER` 환경 변수를 통해 설정할 수 있습니다.

```ini
QUEUE_FAILED_DRIVER=null
```

<a name="failed-job-events"></a>
### 실패한 잡 이벤트

잡이 실패할 때 실행되는 이벤트 리스너를 등록하고 싶다면, `Queue` 파사드의 `failing` 메서드를 사용할 수 있습니다. 예를 들어, 라라벨에 포함된 `AppServiceProvider`의 `boot` 메서드에서 클로저를 이 이벤트에 연결할 수 있습니다.

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Queue;
use Illuminate\Support\ServiceProvider;
use Illuminate\Queue\Events\JobFailed;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스를 등록합니다.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * 애플리케이션 서비스를 부트스트랩합니다.
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
## 큐에서 잡 비우기

> [!NOTE]
> [Horizon](/docs/12.x/horizon)을 사용하는 경우, `queue:clear` 명령어 대신 `horizon:clear` 명령어를 사용하여 큐를 비워야 합니다.

기본 연결의 기본 큐에서 모든 잡을 삭제하려면, `queue:clear` 아티즌 명령어를 사용할 수 있습니다.

```shell
php artisan queue:clear
```

특정 연결 및 큐에서 잡을 삭제하려면, `connection` 인수와 `queue` 옵션을 지정할 수 있습니다.

```shell
php artisan queue:clear redis --queue=emails
```

> [!WARNING]
> 큐에서 잡을 비우는 기능은 SQS, Redis, 데이터베이스 큐 드라이버에서만 지원됩니다. 또한, SQS의 메시지 삭제는 최대 60초가 소요되므로, 큐를 정리한 후 최대 60초 이내에 SQS 큐로 전송된 잡도 함께 삭제될 수 있습니다.

<a name="monitoring-your-queues"></a>
## 큐 모니터링

큐에 갑작스럽게 많은 잡이 몰리면, 큐가 과부하되어 각 잡의 처리가 지연될 수 있습니다. 필요하다면, 잡 대기 수가 특정 임계치를 초과했을 때 라라벨이 알림을 보낼 수 있습니다.

먼저, `queue:monitor` 명령어를 [매 분 실행](https://laravel.com/docs/12.x/scheduling)하도록 스케줄링해야 합니다. 이 명령어는 모니터링할 큐 이름들과 잡 개수 임계값을 인수로 받을 수 있습니다.

```shell
php artisan queue:monitor redis:default,redis:deployments --max=100
```

이 명령어를 스케줄하는 것만으로는 큐 과부하를 알리는 알림이 즉시 작동하지 않습니다. 설정한 임계값을 초과하는 큐를 이 명령어가 발견할 때, `Illuminate\Queue\Events\QueueBusy` 이벤트가 발생합니다. 애플리케이션의 `AppServiceProvider` 내에서 이 이벤트를 감지하여, 알림을 개발팀이나 본인에게 보낼 수 있습니다.

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

잡을 dispatch하는 코드를 테스트할 때, 실제로 잡 자체가 실행되지 않도록 하는 것이 좋을 수 있습니다. 잡의 코드는 별도로 직접 테스트할 수 있기 때문입니다. 따라서 잡 그 자체를 테스트하려면 잡 인스턴스를 직접 생성하여, 테스트 내에서 `handle` 메서드를 호출하면 됩니다.

잡이 실제로 큐에 푸시되지 않도록 하려면, `Queue` 파사드의 `fake` 메서드를 사용할 수 있습니다. 이 메서드를 호출한 뒤, 애플리케이션이 잡을 큐에 푸시했는지에 대해 assert 할 수 있습니다.

```php tab=Pest
<?php

use App\Jobs\AnotherJob;
use App\Jobs\FinalJob;
use App\Jobs\ShipOrder;
use Illuminate\Support\Facades\Queue;

test('orders can be shipped', function () {
    Queue::fake();

    // 주문 발송 처리...

    // 잡이 푸시되지 않았는지 확인...
    Queue::assertNothingPushed();

    // 특정 큐에 잡이 푸시됐는지 확인...
    Queue::assertPushedOn('queue-name', ShipOrder::class);

    // 잡이 두 번 푸시됐는지 확인...
    Queue::assertPushed(ShipOrder::class, 2);

    // 특정 잡이 푸시되지 않았는지 확인...
    Queue::assertNotPushed(AnotherJob::class);

    // Closure가 큐에 푸시됐는지 확인...
    Queue::assertClosurePushed();

    // 전체 푸시된 잡 수 확인...
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

        // 주문 발송 처리...

        // 잡이 푸시되지 않았는지 확인...
        Queue::assertNothingPushed();

        // 특정 큐에 잡이 푸시됐는지 확인...
        Queue::assertPushedOn('queue-name', ShipOrder::class);

        // 잡이 두 번 푸시됐는지 확인...
        Queue::assertPushed(ShipOrder::class, 2);

        // 특정 잡이 푸시되지 않았는지 확인...
        Queue::assertNotPushed(AnotherJob::class);

        // Closure가 큐에 푸시됐는지 확인...
        Queue::assertClosurePushed();

        // 전체 푸시된 잡 수 확인...
        Queue::assertCount(3);
    }
}
```

`assertPushed` 또는 `assertNotPushed` 메서드에 클로저를 전달하여, 특정 "진위 테스트"를 통과한 잡이 푸시됐는지 단언할 수 있습니다. 최소 한 개의 잡이라도 진위 테스트를 통과해 푸시되었다면 assert는 성공합니다.

```php
Queue::assertPushed(function (ShipOrder $job) use ($order) {
    return $job->order->id === $order->id;
});
```

<a name="faking-a-subset-of-jobs"></a>
### 일부 잡만 페이크하기

특정 잡만 페이크 처리하고, 그 외 잡은 실제로 실행되게 하려면, 페이크할 잡의 클래스명을 `fake` 메서드에 배열로 전달하면 됩니다.

```php tab=Pest
test('orders can be shipped', function () {
    Queue::fake([
        ShipOrder::class,
    ]);

    // 주문 발송 처리...

    // 잡이 두 번 푸시됐는지 확인...
    Queue::assertPushed(ShipOrder::class, 2);
});
```

```php tab=PHPUnit
public function test_orders_can_be_shipped(): void
{
    Queue::fake([
        ShipOrder::class,
    ]);

    // 주문 발송 처리...

    // 잡이 두 번 푸시됐는지 확인...
    Queue::assertPushed(ShipOrder::class, 2);
}
```

반대로, 지정한 잡을 제외한 모든 잡을 페이크 처리하고 싶다면, `except` 메서드를 사용할 수 있습니다.

```php
Queue::fake()->except([
    ShipOrder::class,
]);
```

<a name="testing-job-chains"></a>
### 잡 체인 테스트

잡 체인을 테스트하려면, `Bus` 파사드의 페이크 기능을 활용해야 합니다. `Bus` 파사드의 `assertChained` 메서드는 [잡 체인](/docs/12.x/queues#job-chaining)이 dispatch됐는지 단언할 때 사용합니다. 첫 번째 인수로는 체인 잡의 배열을 받습니다.

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

위 예시처럼, 체인 잡의 배열은 잡 클래스명 배열로 전달할 수 있습니다. 또는 실제 잡 인스턴스 배열도 지원합니다. 이 경우, 라라벨은 잡 인스턴스가 같은 클래스이며, 체인으로 dispatch된 잡과 속성 값이 동일한지도 확인합니다.

```php
Bus::assertChained([
    new ShipOrder,
    new RecordShipment,
    new UpdateInventory,
]);
```

`assertDispatchedWithoutChain` 메서드를 사용하면, 체인 없이 단독으로 푸시된 잡인지 단언할 수 있습니다.

```php
Bus::assertDispatchedWithoutChain(ShipOrder::class);
```

<a name="testing-chain-modifications"></a>
#### 체인 수정 테스트

체인에 연결된 잡이 [앞 또는 뒤에 잡을 추가하는 경우](#adding-jobs-to-the-chain), 잡의 `assertHasChain` 메서드로 남아 있는 체인이 예상과 일치하는지 단언할 수 있습니다.

```php
$job = new ProcessPodcast;

$job->handle();

$job->assertHasChain([
    new TranscribePodcast,
    new OptimizePodcast,
    new ReleasePodcast,
]);
```

`assertDoesntHaveChain` 메서드를 사용하면, 잡의 남아 있는 체인이 비어 있는지도 단언할 수 있습니다.

```php
$job->assertDoesntHaveChain();
```

<a name="testing-chained-batches"></a>
#### 체인 내 배치 테스트

잡 체인에 [잡 배치가 포함된 경우](#chains-and-batches), 체인 내 배치가 예상과 일치하는지 단언하려면, 체인 단언 배열에 `Bus::chainedBatch` 구문을 넣으면 됩니다.

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

`Bus` 파사드의 `assertBatched` 메서드를 활용하면, [잡 배치](/docs/12.x/queues#job-batching)가 dispatch 되었는지 단언할 수 있습니다. 이 메서드에 전달하는 클로저는 `Illuminate\Bus\PendingBatch` 인스턴스를 받아, 배치 내의 잡들을 검사할 수 있습니다.

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

`assertBatchCount` 메서드를 사용해, dispatch된 배치 수가 원하는 값과 일치하는지 확인할 수 있습니다.

```php
Bus::assertBatchCount(3);
```

`assertNothingBatched`를 사용하면, 어떤 배치도 dispatch되지 않았는지 확인할 수 있습니다.

```php
Bus::assertNothingBatched();
```

<a name="testing-job-batch-interaction"></a>
#### 잡/배치 상호작용 테스트

특정 잡이 자신의 배치와 상호작용하는지 테스트할 필요가 있을 때가 있습니다. 예를 들어, 잡이 배치의 추가 처리(cancel)를 중지시키는 경우를 들 수 있습니다. 이를 테스트하려면, `withFakeBatch` 메서드로 잡에 페이크 배치를 할당해야 합니다. `withFakeBatch`는 잡 인스턴스와 페이크 배치를 담은 튜플을 반환합니다.

```php
[$job, $batch] = (new ShipOrder)->withFakeBatch();

$job->handle();

$this->assertTrue($batch->cancelled());
$this->assertEmpty($batch->added);
```

<a name="testing-job-queue-interactions"></a>
### 잡/큐 상호작용 테스트

가끔씩 큐잉된 잡이 [스스로 큐에 다시 올리는(release)](#manually-releasing-a-job) 동작이나, 자기 자신을 삭제하는 동작을 테스트해야 할 수도 있습니다. 이런 큐 동작을 테스트하려면, 잡을 인스턴스화한 뒤 `withFakeQueueInteractions` 메서드를 호출하면 됩니다.

잡의 큐 인터랙션이 페이크 처리된 상태에서 잡의 `handle` 메서드를 호출할 수 있고, 그 후 `assertReleased`, `assertDeleted`, `assertNotDeleted`, `assertFailed`, `assertFailedWith`, `assertNotFailed` 등을 사용해 잡의 큐 인터랙션을 단언할 수 있습니다.

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

`Queue` [파사드](/docs/12.x/facades)의 `before` 및 `after` 메서드를 사용하면, 큐잉된 잡이 처리되기 전 또는 후에 실행할 콜백을 지정할 수 있습니다. 이 콜백은 추가로 로그를 기록하거나, 대시보드용 통계값을 누적하는데 유용합니다. 보통 이러한 메서드는 [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에서 호출하는 것이 좋습니다. 예를 들어, 라라벨이 기본으로 제공하는 `AppServiceProvider`에서 아래처럼 사용할 수 있습니다.

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
     * 애플리케이션 서비스를 등록합니다.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * 애플리케이션 서비스를 부트스트랩합니다.
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

`Queue` [파사드](/docs/12.x/facades)의 `looping` 메서드를 사용하면, 워커가 큐에서 잡을 가져오기 직전에 실행할 콜백을 지정할 수 있습니다. 예를 들면, 이전에 실패한 잡 때문에 열린 채 남아있는 트랜잭션을 롤백하도록 클로저를 등록할 수 있습니다.

```php
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Queue;

Queue::looping(function () {
    while (DB::transactionLevel() > 0) {
        DB::rollBack();
    }
});
```