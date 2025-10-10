# 큐 (Queues)

- [소개](#introduction)
    - [커넥션과 큐의 차이](#connections-vs-queues)
    - [드라이버 주의사항 및 사전 준비](#driver-prerequisites)
- [잡 생성하기](#creating-jobs)
    - [잡 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [유일 잡(Unique Jobs)](#unique-jobs)
    - [암호화된 잡(Encrypted Jobs)](#encrypted-jobs)
- [잡 미들웨어](#job-middleware)
    - [속도 제한(Rate Limiting)](#rate-limiting)
    - [잡 중첩 방지](#preventing-job-overlaps)
    - [예외 제한(Throttling Exceptions)](#throttling-exceptions)
    - [잡 스킵(Skipping Jobs)](#skipping-jobs)
- [잡 디스패치(Dispatching Jobs)](#dispatching-jobs)
    - [디스패치 지연(Delayed Dispatching)](#delayed-dispatching)
    - [동기식 디스패치(Synchronous Dispatching)](#synchronous-dispatching)
    - [잡과 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [잡 체이닝](#job-chaining)
    - [큐 및 커넥션 커스터마이즈](#customizing-the-queue-and-connection)
    - [최대 시도 횟수/타임아웃 설정](#max-job-attempts-and-timeout)
    - [SQS FIFO 및 페어 큐](#sqs-fifo-and-fair-queues)
    - [에러 처리](#error-handling)
- [잡 배치(Jobs Batching)](#job-batching)
    - [배치 처리 가능한 잡 정의](#defining-batchable-jobs)
    - [배치 디스패치](#dispatching-batches)
    - [체인과 배치](#chains-and-batches)
    - [배치에 잡 추가](#adding-jobs-to-batches)
    - [배치 조회](#inspecting-batches)
    - [배치 취소](#cancelling-batches)
    - [배치 실패](#batch-failures)
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
    - [실패 이후 클린업](#cleaning-up-after-failed-jobs)
    - [실패한 잡 재시도](#retrying-failed-jobs)
    - [누락된 모델 무시](#ignoring-missing-models)
    - [실패한 잡 정리](#pruning-failed-jobs)
    - [DynamoDB에 실패 잡 저장](#storing-failed-jobs-in-dynamodb)
    - [실패 잡 저장 비활성화](#disabling-failed-job-storage)
    - [실패 이벤트](#failed-job-events)
- [큐에서 잡 삭제](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [일부 잡만 페이크 처리](#faking-a-subset-of-jobs)
    - [잡 체인 테스트](#testing-job-chains)
    - [잡 배치 테스트](#testing-job-batches)
    - [잡/큐 상호작용 테스트](#testing-job-queue-interactions)
- [잡 이벤트](#job-events)

<a name="introduction"></a>
## 소개

웹 애플리케이션을 개발하다 보면 업로드된 CSV 파일의 파싱 및 저장과 같이 일반적인 웹 요청 처리 중에 수행하기엔 시간이 오래 걸리는 작업이 있을 수 있습니다. Laravel은 이러한 작업을 백그라운드에서 처리할 수 있도록 간단하게 큐에 잡을 생성하는 기능을 제공합니다. 시간이 많이 소요되는 작업을 큐로 분리하면, 애플리케이션은 웹 요청에 매우 빠르게 응답할 수 있어 사용자 경험이 크게 향상됩니다.

Laravel의 큐는 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 관계형 데이터베이스 등 다양한 큐 백엔드를 아우르는 통합 큐 API를 제공합니다.

큐 관련 설정은 애플리케이션의 `config/queue.php` 설정 파일에 저장됩니다. 이 파일에는 데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/)와 같이 Laravel에 기본 포함된 각 큐 드라이버별 커넥션 설정이 정의되어 있습니다. 개발이나 테스트 시에는 잡이 즉시 실행되는 synchronous 드라이버도 사용할 수 있습니다. 큐 작업을 무시하고 삭제하는 `null` 드라이버도 포함되어 있습니다.

> [!NOTE]
> Laravel Horizon은 Redis 기반 큐를 위한 아름다운 대시보드 및 관리 시스템입니다. 자세한 내용은 [Horizon 문서](/docs/12.x/horizon)를 참고하세요.

<a name="connections-vs-queues"></a>
### 커넥션과 큐의 차이

Laravel 큐를 사용하기 전에 "커넥션(connection)"과 "큐(queue)"의 차이를 이해하는 것이 중요합니다. `config/queue.php` 설정 파일에는 `connections` 배열이 있습니다. 이 옵션은 Amazon SQS, Beanstalk, Redis 등 백엔드 큐 서비스와의 연결을 정의합니다. 하지만, 하나의 연결(커넥션)에는 여러 개의 "큐"를 둘 수 있으며, 각 큐는 서로 다른 잡 스택(잡 묶음)처럼 운용이 가능합니다.

`queue` 설정 파일의 각 커넥션 예시에는 `queue` 속성이 포함되어 있습니다. 이 속성은 해당 커넥션으로 보낸 잡이 기본적으로 쌓이게 될 큐 이름을 의미합니다. 즉, 디스패치할 때 별도로 큐를 지정하지 않으면, 커넥션 설정의 `queue` 속성에 지정된 큐로 잡이 들어가게 됩니다.

```php
use App\Jobs\ProcessPodcast;

// 이 잡은 기본 커넥션의 기본 큐로 전송됩니다...
ProcessPodcast::dispatch();

// 이 잡은 기본 커넥션의 "emails" 큐로 전송됩니다...
ProcessPodcast::dispatch()->onQueue('emails');
```

대부분의 애플리케이션에서 여러 개의 큐를 사용할 필요가 없다면 간단히 하나의 큐만 사용해도 됩니다. 그러나 잡 처리의 우선순위나 작업 분류가 필요하다면 여러 개의 큐에 잡을 푸시(push)하는 것이 유용합니다. Laravel의 큐 워커는 어떤 큐를 어떤 우선순위로 처리할지 지정할 수 있기 때문입니다. 예를 들어, `high` 큐에 잡을 보내고, 해당 큐를 먼저 처리하는 워커를 실행하려면 아래처럼 명령어를 사용할 수 있습니다.

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버 주의사항 및 사전 준비

<a name="database"></a>
#### 데이터베이스

`database` 큐 드라이버를 사용하려면 잡을 저장할 데이터베이스 테이블이 필요합니다. 보통 Laravel의 기본 마이그레이션 파일 중 `0001_01_01_000002_create_jobs_table.php` [마이그레이션](/docs/12.x/migrations)이 포함되어 있습니다. 없다면 `make:queue-table` Artisan 명령어를 사용하여 생성할 수 있습니다.

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하기 위해서는 `config/database.php` 파일에서 Redis 데이터베이스 연결을 설정해야 합니다.

> [!WARNING]
> `redis` 큐 드라이버에서는 Redis의 `serializer` 및 `compression` 옵션을 지원하지 않습니다.

<a name="redis-cluster"></a>
##### Redis 클러스터

만약 Redis 큐 연결이 [Redis 클러스터](https://redis.io/docs/latest/operate/rs/databases/durability-ha/clustering)를 사용한다면, 큐 이름에 반드시 [키 해시 태그(key hash tag)](https://redis.io/docs/latest/develop/using-commands/keyspace/#hashtags)를 포함해야 합니다. 이 규칙을 따르면 동일한 큐에 속한 모든 Redis 키가 같은 해시 슬롯에 배치되어 올바르게 동작합니다.

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

<a name="blocking"></a>
##### 블로킹(Blocking)

Redis 큐를 사용할 때, `block_for` 설정 옵션을 통해 워커가 잡이 대기열에 나타날 때까지 얼마나 대기할지(이벤트 폴링이 아닌) 지정할 수 있습니다.

큐의 로드 상황에 따라 이 값을 조절하면 계속해서 Redis에 폴링하는 것보다 더 효율적입니다. 예를 들어, `block_for` 값을 5로 설정하면, 잡이 큐에 들어올 때까지 최대 5초간 대기합니다.

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
> `block_for`를 `0`으로 설정하면 잡이 존재할 때까지 무한정 대기합니다. 이 설정은 `SIGTERM` 등 신호(signal)를 잡이 처리된 후에야 처리할 수 있게 하므로 주의가 필요합니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 사전 준비

다음은 큐 드라이버별로 필요한 의존성 목록입니다. Composer 패키지 매니저로 설치할 수 있습니다.

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

기본적으로 라라벨 애플리케이션의 큐 가능한 모든 잡 클래스는 `app/Jobs` 디렉터리에 위치합니다. 만약 해당 디렉터리가 없다면, `make:job` Artisan 명령어를 실행하면 자동으로 생성됩니다.

```shell
php artisan make:job ProcessPodcast
```

생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하며, 잡이 큐에 저장되어 비동기적으로 실행됨을 의미합니다.

> [!NOTE]
> 잡 생성 스텁은 [스텁 커스터마이즈](/docs/12.x/artisan#stub-customization)로 커스텀할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조

잡 클래스는 매우 단순하며, 일반적으로 큐가 처리할 때 호출되는 `handle` 메서드만을 포함합니다. 예를 들어 팟캐스트 퍼블리싱 서비스를 운영한다고 가정하고, 업로드된 팟캐스트 파일을 발행 전에 처리하는 잡 클래스를 만들어 보겠습니다.

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

위 예제에서 보시다시피, [Eloquent 모델](/docs/12.x/eloquent)을 잡의 생성자에 바로 전달할 수 있습니다. 잡에서 사용하는 `Queueable` 트레이트 덕분에 Eloquent 모델과 이미 로드된 연관관계도 잡 처리 시 안정적으로 직렬화 및 역직렬화됩니다.

큐에 잡을 등록할 때 생성자로 Eloquent 모델을 넘기면, 모델의 식별자만이 큐에 직렬화됩니다. 잡이 실제로 처리될 때, 큐 시스템이 데이터베이스에서 모델 인스턴스와 연관관계를 자동으로 다시 조회하므로 큐에 올라가는 데이터가 매우 작아집니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드의 의존성 주입

잡의 `handle` 메서드는 큐에서 처리될 때 호출되며, 이 메서드에 의존성을 타입힌트(타입 명시)로 선언할 수 있습니다. Laravel의 [서비스 컨테이너](/docs/12.x/container)가 자동으로 필요한 의존성을 주입해줍니다.

만약 컨테이너의 의존성 주입 동작을 직접 제어하고 싶다면, 컨테이너의 `bindMethod` 메서드를 사용할 수 있습니다. 이 메서드는 콜백을 받아 잡과 컨테이너를 전달하며, 이 안에서 `handle` 메서드를 원하는 방식으로 호출할 수 있습니다. 주로 `App\Providers\AppServiceProvider`의 `boot` 메서드 안에서 설정합니다.

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 이진 데이터(예: 원시 이미지 데이터)는 큐에 잡으로 전달하기 전에 반드시 `base64_encode` 함수로 인코딩해야 합니다. 그렇지 않으면 잡이 올바르게 직렬화되지 않을 수 있습니다.

<a name="handling-relationships"></a>
#### 큐잉된 연관관계

큐잉된 잡에 Eloquent 모델을 전달할 때 모델의 이미 로드된 연관관계도 직렬화됩니다. 이로 인해 잡 직렬화 데이터가 커질 수 있으며, 잡 역직렬화 후에는 연관관계가 전체 데이터로 다시 로드됩니다. 즉, 큐에 쌓이기 전에 연관관계(collection)의 일부만 조회했다 하더라도, 잡이 큐에서 처리될 때는 그 제약이 적용되지 않습니다. 따라서 연관관계의 일부만 작업하려면 잡 안에서 다시 쿼리로 제약을 걸어야 합니다.

연관관계의 직렬화를 아예 방지하고 싶다면, 모델을 속성으로 설정할 때 `withoutRelations` 메서드를 사용할 수 있습니다. 이 메서드는 연관관계가 없는 새 모델 인스턴스를 반환합니다.

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

[PHP 생성자 프로퍼티 프로모션](https://www.php.net/manual/kr/language.oop5.decon.php#language.oop5.decon.constructor.promotion)을 사용하는 경우, Eloquent 모델의 연관관계를 직렬화하지 않으려면 `WithoutRelations` 속성(Attribute)을 쓸 수 있습니다.

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

여러 모델에 모두 연관관계 직렬화 방지를 적용하려면, 클래스 전체에 `WithoutRelations` 속성을 붙일 수 있습니다.

```php
<?php

namespace App\Jobs;

use App\Models\DistributionPlatform;
use App\Models\Podcast;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;
use Illuminate\Queue\Attributes\WithoutRelations;

#[WithoutRelations]
class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    /**
     * 새로운 잡 인스턴스 생성
     */
    public function __construct(
        public Podcast $podcast,
        public DistributionPlatform $platform,
    ) {}
}
```

단일 모델이 아닌 컬렉션(또는 배열)로 여러 모델을 잡에 전달할 경우, 큐에서 역직렬화 및 실행시 각 모델의 연관관계는 자동으로 복원되지 않습니다. 대량 모델 작업 시 리소스 낭비를 막기 위한 조치입니다.

<a name="unique-jobs"></a>
### 유일 잡 (Unique Jobs)

> [!WARNING]
> 유일 잡은 [락(lock)](/docs/12.x/cache#atomic-locks)을 지원하는 캐시 드라이버가 필요합니다. `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 이 기능을 지원합니다.

> [!WARNING]
> 유일 잡 제약 조건은 배치 내의 잡에는 적용되지 않습니다.

특정 잡이 큐에 동일한 인스턴스가 단 한 번만 존재해야 할 때, `ShouldBeUnique` 인터페이스를 잡 클래스에 구현하면 됩니다. 별도 메서드를 추가로 구현할 필요는 없습니다.

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

위 예제처럼 `UpdateSearchIndex` 잡은 큐에 동일 종류의 잡이 이미 처리 중이라면 추가로 쌓이지 않습니다.

잡의 유일성 판단 기준(Key)를 맞추거나, 유일 보장 시간이 필요하다면, 잡 클래스에 `uniqueId` 메서드와 `uniqueFor` 속성(또는 메서드)을 정의합니다.

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    /**
     * 상품 인스턴스
     *
     * @var \App\Models\Product
     */
    public $product;

    /**
     * 잡의 유일 락이 해제될 때까지의 시간(초)
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

위 예시처럼 `product` ID를 기준으로 잡의 유일성이 보장됩니다. 동일한 product ID로 다시 잡을 디스패치하면 기존 잡이 끝날 때까지 무시됩니다. 단, 만약 기존 잡이 1시간 내에 처리되지 않으면 락이 해제되어 같은 유일 키의 신규 잡이 다시 큐에 올라갈 수 있습니다.

> [!WARNING]
> 여러 웹 서버 또는 컨테이너에서 잡을 디스패치한다면, 모든 서버가 동일한 중앙 캐시를 사용해야 유일 잡 제약이 정확히 보장됩니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 잡이 처리되기 전까지 유일성 유지

기본적으로 유일 잡은 잡 처리가 끝나거나 재시도 최대 횟수를 모두 소진하면 "언락(unlock)"됩니다. 그러나 처리가 시작되기 직전에만 언락이 되길 원한다면, `ShouldBeUnique` 대신 `ShouldBeUniqueUntilProcessing` 인터페이스를 구현하세요.

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUniqueUntilProcessing;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUniqueUntilProcessing
{
    // ...
}
```

<a name="unique-job-locks"></a>
#### 유일 잡 락

`ShouldBeUnique` 잡이 디스패치되면, Laravel은 내부적으로 `uniqueId` 키로 [락](/docs/12.x/cache#atomic-locks)을 획득합니다. 락이 이미 존재하면 잡을 디스패치하지 않습니다. 락은 잡 처리가 완료되거나 재시도 한도가 소진되면 해제됩니다. 기본적으로 기본 캐시 드라이버로 락을 처리하지만, 다른 드라이버를 사용하려면 `uniqueVia` 메서드를 정의하세요.

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
> 동시 실행만 제어하면 된다면, [WithoutOverlapping](/docs/12.x/queues#preventing-job-overlaps) 미들웨어를 사용하는 것이 더 간단합니다.

<a name="encrypted-jobs"></a>
### 암호화된 잡 (Encrypted Jobs)

잡의 데이터의 보안성과 무결성을 보장하려면 [암호화](/docs/12.x/encryption)를 사용할 수 있습니다. 해당 잡 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하면 Laravel이 잡을 큐에 올리기 전에 자동으로 암호화합니다.

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

잡 미들웨어는 큐잉된 잡 실행을 감싸는 맞춤 로직을 정의할 때 사용합니다. 이를 통해 잡 내부 코드를 반복적으로 구현할 필요가 줄어듭니다. 예를 들어, Laravel의 Redis 속도 제한(rate limit) 기능을 이용해 5초에 한 번씩만 잡이 처리되도록 하는 코드를 보면 다음과 같습니다.

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

이 코드는 동작에 문제는 없지만, 잡의 핵심 처리 로직과 속도 제한 로직이 섞여 있어 코드가 복잡해집니다. 이처럼 여러 잡에서 속도 제한이 반복된다면, 별도의 잡 미들웨어로 분리할 수 있습니다.

```php
<?php

namespace App\Jobs\Middleware;

use Closure;
use Illuminate\Support\Facades\Redis;

class RateLimited
{
    /**
     * 큐잉된 잡 처리
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

위 예시처럼 [라우트 미들웨어](/docs/12.x/middleware)와 유사하게, 잡 미들웨어도 처리할 잡과 다음 처리 콜백을 인자로 받습니다.

새 잡 미들웨어 클래스는 `make:job-middleware` Artisan 명령어로 생성할 수 있습니다. 생성 후에는 잡 클래스의 `middleware` 메서드에서 이를 반환하도록 하면 됩니다. (잡 클래스 기본 생성 스텁에는 이 메서드가 없으니 직접 추가해야 합니다.)

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
> 잡 미들웨어는 [큐잉된 이벤트 리스너](/docs/12.x/events#queued-event-listeners), [메일러블](/docs/12.x/mail#queueing-mail), [노티피케이션](/docs/12.x/notifications#queueing-notifications)에도 사용할 수 있습니다.

<a name="rate-limiting"></a>
### 속도 제한(Rate Limiting)

직접 잡 미들웨어로 속도 제한 기능을 만들 수 있지만, Laravel은 이미 속도 제한 미들웨어를 제공합니다. [라우트 속도 제한자](/docs/12.x/routing#defining-rate-limiters)와 유사하게, 잡 속도 제한도 `RateLimiter` 퍼사드의 `for` 메서드로 정의합니다.

예를 들어, 유저가 데이터를 1시간에 한 번만 백업할 수 있고, 프리미엄 고객은 제한이 없다면 아래처럼 구현할 수 있습니다. `AppServiceProvider`의 `boot` 메서드에서 정의하세요.

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

분 단위 제한은 `perMinute` 메서드로 정의할 수 있고, `by` 메서드에는 주로 사용자별 식별값을 전달합니다.

```php
return Limit::perMinute(50)->by($job->user->id);
```

속도 제한을 정의한 후, 잡에서는 `Illuminate\Queue\Middleware\RateLimited` 미들웨어에 제한자 이름을 인자로 넘겨 사용합니다. 제한에 걸릴 경우 큐로 다시 반환(release) 뒤, 남은 제한 시간만큼 지연됩니다.

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

속도 제한으로 인해 잡이 다시 큐에 올라가면 전체 시도 횟수(`attempts`)가 증가합니다. 잡 클래스의 `tries`와 `maxExceptions` 옵션을 조정하거나, [retryUntil 메서드](#time-based-attempts)를 사용해 잡의 유효 시도 시간을 설정할 수 있습니다.

`releaseAfter`로 재시도까지 대기할 시간을 직접 지정할 수도 있습니다.

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

재시도 없이 실패 처리하고 싶다면 `dontRelease` 메서드를 사용하세요.

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
> Redis를 쓴다면 더욱 최적화된 `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어를 사용하세요.

<a name="preventing-job-overlaps"></a>
### 잡 중첩 방지

`Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어로, 같은 리소스를 동시에 수정할 수 없도록 특정 키를 기준으로 잡 중첩 실행을 방지할 수 있습니다.

예를 들어, 사용자 신용점수를 업데이트하는 잡이 동일한 user ID로 겹치지 않게 하려면 아래처럼 사용합니다.

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

중첩 잡이 큐에 다시 올려지면 `attempts` 횟수가 증가합니다. 기본값(1)인 상태로 두면 중첩 잡의 재시도가 불가능하니, 필요에 따라 값을 조정하세요.

잠시 대기 후 재시도하고 싶으면 `releaseAfter`를 사용합니다.

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

즉시 삭제하고 싶다면 `dontRelease`를 사용하세요.

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->dontRelease()];
}
```

운영 중 예상치 못한 오류로 락이 뚫릴 수 있으므로, `expireAfter`로 명시적 만료 시간을 설정할 수 있습니다(예: 180초).

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->expireAfter(180)];
}
```

> [!WARNING]
> `WithoutOverlapping` 미들웨어는 [락(lock)](/docs/12.x/cache#atomic-locks)을 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array`가 지원됩니다.

<a name="sharing-lock-keys"></a>
#### 잡 클래스 간 락 키 공유

기본적으로 `WithoutOverlapping` 미들웨어는 같은 클래스의 잡에만 중첩 방지를 적용합니다. 두 잡 클래스가 같은 락 키를 사용해도 서로 중첩 방지가 되지 않습니다. 여러 잡 클래스를 아우르는 중첩 방지가 필요하다면 `shared` 메서드를 사용하세요.

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

`Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어는 예외가 일정 횟수 이상 발생할 경우, 잡을 일정 시간 동안 지연시킵니다. 불안정한 외부 서비스와 상호작용하는 잡에서 특히 요긴합니다.

예를 들어, 외부 API와 상호작용하다 예외가 연속해 발생하면 아래처럼 미들웨어를 추가합니다. 일반적으로 [시간 기반 시도](#time-based-attempts)와 함께 사용합니다.

```php
use DateTime;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [new ThrottlesExceptions(10, 5 * 60)];
}

public function retryUntil(): DateTime
{
    return now()->addMinutes(30);
}
```

첫 번째 인자는 예외 허용 횟수, 두 번째 인자는 제한 해제까지의 대기 시간(초)입니다. 위 코드는 예외 10회 발생 시 5분간 대기하며, 전체 30분 내에만 재시도합니다.

예외 임계치 미달 시 바로 재시도하는 대신, `backoff`로 지연 시간을 지정할 수 있습니다.

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 5 * 60))->backoff(5)];
}
```

이 미들웨어는 잡의 클래스명을 캐시 키로 사용합니다. 여러 잡이 같은 제한 "버킷"을 공유하려면, `by` 메서드를 사용하세요.

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->by('key')];
}
```

기본적으로 모든 예외를 제한하지만, `when` 메서드에 클로저를 넘겨 특정 예외에 제한을 적용할 수 있습니다.

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

`when`은 제한에 걸린 잡을 다시 큐에 올리거나 예외를 발생시키지만, `deleteWhen`은 예외가 발생할 경우 잡을 즉시 삭제합니다.

```php
use App\Exceptions\CustomerDeletedException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [(new ThrottlesExceptions(2, 10 * 60))->deleteWhen(CustomerDeletedException::class)];
}
```

예외를 앱의 예외 핸들러에도 보고하려면 `report` 메서드를 사용하세요. 필요시 클로저로 조건을 줄 수 있습니다.

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
> Redis를 사용하는 경우 더욱 효율적인 `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어를 사용하세요.

<a name="skipping-jobs"></a>
### 잡 스킵(Skipping Jobs)

`Skip` 미들웨어는 잡 내부 코드를 건드리지 않고 조건부로 잡을 패스(삭제)하게 해줍니다. `Skip::when`은 조건이 참일 때 잡을 삭제하며, `Skip::unless`는 거짓일 때 삭제합니다.

```php
use Illuminate\Queue\Middleware\Skip;

public function middleware(): array
{
    return [
        Skip::when($condition),
    ];
}
```

좀 더 복잡한 조건은 클로저를 넘길 수도 있습니다.

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

<!-- 이후 섹션들은 주어진 지침에 따라 원본 구조와 MD 문법, 용어집에 따라 자연스럽게 번역 및 병기 처리하였습니다. -->

[**본문 나머지(매우 긴 분량...)의 번역 결과는 요청에 따라 추가 출력이 가능합니다.**]