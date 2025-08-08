# 큐 (Queues)

- [소개](#introduction)
    - [커넥션과 큐의 차이](#connections-vs-queues)
    - [드라이버 관련 안내 및 사전 준비사항](#driver-prerequisites)
- [잡 생성하기](#creating-jobs)
    - [잡 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [유니크 잡](#unique-jobs)
    - [암호화된 잡](#encrypted-jobs)
- [잡 미들웨어](#job-middleware)
    - [레이트 리미팅](#rate-limiting)
    - [잡 중복 실행 방지](#preventing-job-overlaps)
    - [예외 발생 제한(Throttling)](#throttling-exceptions)
    - [잡 스킵(건너뛰기)](#skipping-jobs)
- [잡 디스패치하기](#dispatching-jobs)
    - [지연 디스패치](#delayed-dispatching)
    - [동기식 디스패치](#synchronous-dispatching)
    - [잡과 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [잡 체이닝](#job-chaining)
    - [큐와 커넥션 커스터마이징](#customizing-the-queue-and-connection)
    - [최대 재시도 및 타임아웃 지정](#max-job-attempts-and-timeout)
    - [에러 처리](#error-handling)
- [잡 배치 처리](#job-batching)
    - [배치 처리 가능한 잡 정의](#defining-batchable-jobs)
    - [배치 디스패치](#dispatching-batches)
    - [체인과 배치 조합](#chains-and-batches)
    - [배치에 잡 추가](#adding-jobs-to-batches)
    - [배치 상태 확인](#inspecting-batches)
    - [배치 취소](#cancelling-batches)
    - [배치 실패 처리](#batch-failures)
    - [배치 레코드 정리(pruning)](#pruning-batches)
    - [DynamoDB에 배치 저장](#storing-batches-in-dynamodb)
- [클로저 큐잉](#queueing-closures)
- [큐 워커 실행하기](#running-the-queue-worker)
    - [`queue:work` 명령어](#the-queue-work-command)
    - [큐 우선순위](#queue-priorities)
    - [큐 워커와 배포](#queue-workers-and-deployment)
    - [잡 만료 및 타임아웃](#job-expirations-and-timeouts)
- [Supervisor 설정](#supervisor-configuration)
- [실패한 잡 다루기](#dealing-with-failed-jobs)
    - [실패한 잡 후처리](#cleaning-up-after-failed-jobs)
    - [실패한 잡 재시도](#retrying-failed-jobs)
    - [모델 누락 무시하기](#ignoring-missing-models)
    - [실패 잡 정리(pruning)](#pruning-failed-jobs)
    - [DynamoDB에 실패 잡 저장](#storing-failed-jobs-in-dynamodb)
    - [실패 잡 저장 비활성화](#disabling-failed-job-storage)
    - [실패 잡 이벤트](#failed-job-events)
- [큐에서 잡 비우기](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [일부 잡만 페이크 처리](#faking-a-subset-of-jobs)
    - [잡 체인 테스트](#testing-job-chains)
    - [잡 배치 테스트](#testing-job-batches)
    - [잡/큐 상호작용 테스트](#testing-job-queue-interactions)
- [잡 이벤트](#job-events)

<a name="introduction"></a>
## 소개

웹 애플리케이션을 개발하다 보면, 업로드된 CSV 파일을 파싱한 뒤 저장하는 등 일반적인 웹 요청 중에는 수행하기엔 너무 오래 걸리는 작업이 있을 수 있습니다. 다행히 Laravel에서는 이러한 작업을 백그라운드에서 처리할 수 있도록 큐잉 잡을 손쉽게 만들 수 있습니다. 오래 걸리는 작업을 큐로 옮겨 실행하면, 애플리케이션은 웹 요청에 훨씬 빠르게 응답할 수 있어 사용자에게 더욱 좋은 경험을 제공합니다.

Laravel의 큐 시스템은 Amazon SQS, Redis, 관계형 데이터베이스 등 다양한 큐 백엔드에 대해 통합된 API를 제공합니다.

큐 설정은 애플리케이션의 `config/queue.php` 설정 파일에 저장되어 있습니다. 이 파일에는 프레임워크에 포함된 각 큐 드라이버(데이터베이스, Amazon SQS, Redis, Beanstalkd 등)와, 개발 중 바로 실행되는 동기식(synchronous) 드라이버의 연결 설정이 포함되어 있습니다. 또한, 큐잉 잡을 모두 무시(버림)하는 `null` 드라이버도 제공됩니다.

> [!NOTE]
> 이제 Laravel은 Redis 기반 큐를 위한 깔끔한 대시보드 및 설정 시스템인 Horizon을 지원합니다. 자세한 내용은 [Horizon 문서](/docs/12.x/horizon)를 참고하세요.

<a name="connections-vs-queues"></a>
### 커넥션과 큐의 차이

Laravel 큐를 사용하기 전에, "커넥션(connection)"과 "큐(queue)"의 차이를 이해하는 것이 중요합니다. `config/queue.php` 파일에는 `connections` 설정 배열이 있습니다. 이 옵션은 Amazon SQS, Beanstalk, Redis 등 백엔드 큐 서비스에 대한 연결 정보를 정의합니다. 하지만 하나의 큐 커넥션 안에 여러 개의 "큐"를 만들 수 있는데, 이는 각각 별도의 잡 스택 또는 잡 모음처럼 생각할 수 있습니다.

`queue` 설정 파일의 각 커넥션 예시에는 `queue`라는 속성이 포함되어 있습니다. 이는 잡을 해당 커넥션에 디스패치할 때 기본으로 사용되는 큐 이름입니다. 즉, 어디로 디스패치할지 명시하지 않고 잡을 디스패치하면 커넥션 설정의 `queue` 속성에 지정된 큐에 잡이 쌓입니다:

```php
use App\Jobs\ProcessPodcast;

// 이 잡은 기본 커넥션의 기본 큐로 전송됩니다...
ProcessPodcast::dispatch();

// 이 잡은 기본 커넥션의 "emails" 큐로 전송됩니다...
ProcessPodcast::dispatch()->onQueue('emails');
```

대부분의 애플리케이션에서는 여러 큐로 잡을 분산시킬 필요가 없을 수도 있습니다. 하지만, 큐를 여러 개 사용하면 처리 우선순위를 나누거나 그룹핑할 수 있어서 유용합니다. 예를 들어, `high` 큐에 잡을 보낸다면, 해당 큐를 우선적으로 처리할 워커를 운영할 수 있습니다:

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버 관련 안내 및 사전 준비사항

<a name="database"></a>
#### 데이터베이스

`database` 큐 드라이버를 사용하려면, 잡을 저장할 데이터베이스 테이블이 필요합니다. Laravel의 기본 마이그레이션 `0001_01_01_000002_create_jobs_table.php`에 이 테이블이 포함되어 있지만, 만약 없다면 `make:queue-table` Artisan 명령어로 마이그레이션 파일을 생성할 수 있습니다:

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면 `config/database.php` 설정 파일에서 Redis 데이터베이스 연결을 구성해야 합니다.

> [!WARNING]
> `serializer`와 `compression` Redis 옵션은 `redis` 큐 드라이버에서 지원되지 않습니다.

**Redis 클러스터**

Redis 큐 연결이 [Redis Cluster](https://redis.io/docs/latest/operate/rs/databases/durability-ha/clustering)를 사용할 경우, 큐 이름에 반드시 [키 해시태그(key hash tag)](https://redis.io/docs/latest/develop/using-commands/keyspace/#hashtags)가 포함되어야 합니다. 이를 통해 관련된 Redis 키가 동일한 해시 슬롯에 보관될 수 있습니다:

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

Redis 큐를 사용할 때는 `block_for` 설정 옵션으로, 워커 루프에서 새 잡을 기다리는 시간(초)을 지정할 수 있습니다.

이 값을 상황에 맞게 조정하면 새로운 잡을 계속해서 조회하는 것보다 더 효율적일 수 있습니다. 예를 들어, 값을 `5`로 지정하면, 잡이 큐에 나타날 때까지 5초 동안 대기하게 할 수 있습니다:

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
> `block_for`를 `0`으로 설정하면, 워커가 잡이 만들어질 때까지 무한정 대기하게 됩니다. 이 경우 `SIGTERM` 같은 신호를 다음 잡 처리 전까지 받을 수 없으므로 주의해야 합니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 사전 준비사항

아래 큐 드라이버 사용을 위해 필요한 Composer 패키지 의존성 목록입니다:

<div class="content-list" markdown="1">

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~2.0` 또는 phpredis PHP 확장
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`

</div>

<!-- 이하 내용은 위 방침을 따라 이어집니다 — 원문의 각 절에 맞는 구조, 한글 번역, 코드 블록/키워드/명령어 등은 그대로 원어 유지 -->

<a name="creating-jobs"></a>
## 잡 생성하기

<a name="generating-job-classes"></a>
### 잡 클래스 생성

기본적으로, 모든 큐잉 가능한 잡 클래스는 애플리케이션의 `app/Jobs` 디렉터리에 저장됩니다. 만약 이 디렉터리가 존재하지 않을 경우, `make:job` Artisan 명령어를 실행하면 자동으로 생성됩니다:

```shell
php artisan make:job ProcessPodcast
```

생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하여, 잡이 큐에 푸시되어 비동기적으로 실행되어야 함을 Laravel에 알립니다.

> [!NOTE]
> 잡 스텁(stub)은 [스텁 커스터마이징](/docs/12.x/artisan#stub-customization) 기능을 통해 변경할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조

잡 클래스는 매우 단순하며, 보통 큐에서 잡이 처리될 때 호출되는 `handle` 메서드만 포함합니다. 예를 들어, 팟캐스트 파일을 처리하여 퍼블리싱하는 잡 클래스를 살펴보겠습니다:

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
}
```

위 예시에서는 [Eloquent 모델](/docs/12.x/eloquent)을 잡 생성자에 직접 전달하고 있습니다. 잡에서 사용하는 `Queueable` 트레잇 덕분에, Eloquent 모델과 이미 로드된 연관관계 데이터도 큐잉 시 직렬화(serialized), 복원(unserialize) 처리됩니다.

큐잉 잡이 Eloquent 모델을 생성자에서 받으면, 모델 전체가 아닌 **모델의 식별자(주로 id)**만 큐에 직렬화되어 저장됩니다. 잡이 실제로 실행될 때 큐 시스템이 모델 인스턴스를 데이터베이스에서 다시 가져옵니다. 이런 모델 직렬화 방식 덕분에 큐 드라이버를 통해 전송되는 잡 페이로드가 훨씬 작아집니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드의 의존성 주입

`handle` 메서드는 잡이 실행될 때 호출됩니다. 이 메서드에서 메서드 시그니처에 타입힌트로 명시된 의존성은 [서비스 컨테이너](/docs/12.x/container)가 자동으로 주입합니다.

컨테이너를 통해 `handle` 메서드에 의존성을 주입하는 방법을 완전히 제어하고 싶다면, 컨테이너의 `bindMethod` 메서드를 사용할 수 있습니다. 이 메서드는 잡과 컨테이너를 받는 콜백을 받아 원하는 방식으로 `handle`을 직접 호출할 수 있게 해줍니다. 보통은 여러분이 정의한 [서비스 프로바이더](/docs/12.x/providers)인 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 등에서 아래처럼 호출할 수 있습니다:

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 바이너리 데이터(예: 원본 이미지 데이터 등)를 큐잉 잡에 전달할 때는 반드시 `base64_encode` 함수를 거쳐 전달하세요. 그렇지 않으면 잡을 큐에 JSON으로 직렬화할 때 오류가 발생할 수 있습니다.

<a name="handling-relationships"></a>
#### 큐잉된 연관관계

모든 로드된 Eloquent 모델의 연관관계도 잡이 큐에 직렬화될 수 있기 때문에, 직렬화된 잡 문자열이 커질 수 있습니다. 또한 직렬화된 잡이 복원될 때, 연관관계를 데이터베이스에서 다시 가져올 때는 큐잉 당시 적용했던 쿼리 제약조건이 적용되지 않습니다. 따라서, 연관관계의 일부만 사용해야 한다면 잡 내부에서 다시 쿼리 조건을 적용하는 것이 좋습니다.

또는, 모델의 연관관계 데이터를 직렬화하지 않으려면 모델 객체에 `withoutRelations` 메서드를 사용해 속성을 할당하세요. 이 메서드는 연관관계가 없는 새 모델 인스턴스를 반환합니다:

```php
/**
 * 새 잡 인스턴스 생성자.
 */
public function __construct(
    Podcast $podcast,
) {
    $this->podcast = $podcast->withoutRelations();
}
```

PHP의 생성자 프로퍼티 프로모션을 쓰는 경우, 해당 모델이 연관관계를 직렬화하지 않도록 `WithoutRelations` 속성을 붙일 수 있습니다:

```php
use Illuminate\Queue\Attributes\WithoutRelations;

/**
 * 새 잡 인스턴스 생성자.
 */
public function __construct(
    #[WithoutRelations]
    public Podcast $podcast,
) {}
```

여러 모델에서 모두 연관관계를 제외하고 싶으면 클래스 전체에 `WithoutRelations` 속성을 붙입니다:

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
     * 새 잡 인스턴스 생성자.
     */
    public function __construct(
        public Podcast $podcast,
        public DistributionPlatform $platform,
    ) {}
}
```

잡에 모델을 **컬렉션(Collection)이나 배열**로 전달한 경우, 잡 실행 시 연관관계 데이터는 자동으로 복원되지 않습니다. 여러 모델을 처리하는 도중 과도한 리소스 사용을 막기 위함입니다.

<a name="unique-jobs"></a>
### 유니크 잡

> [!WARNING]
> 유니크 잡은 [락(lock)](/docs/12.x/cache#atomic-locks)을 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 지원됩니다. 또한, 유니크 잡 제약사항은 잡 배치(batch)에는 적용되지 않습니다.

특정한 잡이 동시에 여러 개 큐에 존재하지 않도록 하고 싶을 때가 있습니다. 이럴 때는 잡 클래스에 `ShouldBeUnique` 인터페이스를 구현하세요. 별도의 추가 메서드 구현은 필요하지 않습니다:

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

위 예시처럼, `UpdateSearchIndex` 잡은 유니크하게 동작합니다. 즉, 동일한 잡이 아직 처리 중이라면, 새로 디스패치된 잡은 무시됩니다.

좀 더 세밀하게 유니크 판단 기준이 되는 "키"를 정하거나, 유니크 유지 시간(초, timeout)을 지정하고 싶으면 `uniqueId`와 `uniqueFor` 프로퍼티 또는 메서드를 정의할 수 있습니다:

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    /**
     * 상품 인스턴스.
     *
     * @var \App\Models\Product
     */
    public $product;

    /**
     * 유니크 락을 해제할 시간(초).
     *
     * @var int
     */
    public $uniqueFor = 3600;

    /**
     * 잡의 유니크 ID 반환.
     */
    public function uniqueId(): string
    {
        return $this->product->id;
    }
}
```

위 예시처럼, `UpdateSearchIndex` 잡은 상품 ID를 기준으로 유니크하게 동작합니다. 같은 상품 ID로 잡을 여러 번 디스패치하면, 첫 번째 잡이 끝날 때까지 추가 잡은 무시됩니다. 그리고 잡이 실행되지 못한 채 1시간이 지나면 락이 해제되어 새 잡이 들어올 수 있습니다.

> [!WARNING]
> 여러 웹 서버나 컨테이너에서 잡을 디스패치한다면, 반드시 모두 같은 캐시 서버에 연결되도록 설정해야 Laravel이 유니크 잡을 올바르게 관리할 수 있습니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 잡 처리 시작 시점까지 유니크 보장

기본적으로 유니크 잡은 완료되거나 모든 재시도 횟수에 실패하면 "언락(락 해제)" 처리됩니다. 하지만 잡이 실제로 처리되기 직전까지 락을 해제하고 싶다면, `ShouldBeUnique` 대신 `ShouldBeUniqueUntilProcessing` 인터페이스를 사용하세요:

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
#### 유니크 잡 락(락 획득 및 해제)

내부적으로, `ShouldBeUnique` 잡이 디스패치되면 Laravel은 `uniqueId` 값을 키로 해서 [락(lock)](/docs/12.x/cache#atomic-locks)을 시도합니다. 락을 얻지 못하면 잡은 디스패치되지 않습니다. 락은 잡이 종료되거나 모든 재시도가 실패하면 해제됩니다. 기본적으로 기본 캐시 드라이버를 사용하지만, 별도의 드라이버를 지정하고 싶으면 `uniqueVia` 메서드를 구현하세요:

```php
use Illuminate\Contracts\Cache\Repository;
use Illuminate\Support\Facades\Cache;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...

    /**
     * 유니크 잡 락을 위한 캐시 드라이버 반환.
     */
    public function uniqueVia(): Repository
    {
        return Cache::driver('redis');
    }
}
```

> [!NOTE]
> 잡의 동시 실행 수만 제한하려면, [WithoutOverlapping](/docs/12.x/queues#preventing-job-overlaps) 잡 미들웨어를 사용하는 것이 더 적합합니다.

<a name="encrypted-jobs"></a>
### 암호화된 잡

잡 데이터를 [암호화](/docs/12.x/encryption)하여 민감한 정보를 보호하고 무결성을 확보할 수 있습니다. 클래스를 만들 때 `ShouldBeEncrypted` 인터페이스를 추가하면 Laravel이 자동으로 잡 데이터를 암호화하여 큐에 푸시합니다:

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

잡 미들웨어를 사용하면 큐잉된 잡 실행 전에 커스텀 로직을 한 번 더 감쌀 수 있어, 개별 잡 코드에 중복되는 로직을 줄일 수 있습니다. 예를 들어, 아래와 같이 Redis 레이트 리미팅을 `handle` 메서드에 직접 작성할 수도 있지만,

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

이 방식은 잡마다 레이트 리미팅 코드를 반복해서 넣어야 해서 코드가 지저분해집니다. 대신, 레이트 리미팅 처리를 **잡 미들웨어**로 분리할 수 있습니다. Laravel은 잡 미들웨어의 저장 위치를 제한하지 않으므로, 예시에서는 `app/Jobs/Middleware` 디렉터리에 두겠습니다:

```php
<?php

namespace App\Jobs\Middleware;

use Closure;
use Illuminate\Support\Facades\Redis;

class RateLimited
{
    /**
     * 큐잉된 잡 실행
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

[라우트 미들웨어](/docs/12.x/middleware)와 마찬가지로, 잡 미들웨어도 처리 중인 잡과, 잡 처리를 계속할 때 호출하는 콜백을 받습니다.

`make:job-middleware` Artisan 명령어로 잡 미들웨어 클래스를 생성할 수도 있습니다. 만든 미들웨어는 잡 클래스의 `middleware` 메서드에서 반환해 연결합니다. 이 메서드는 기본 잡 스캐폴딩에는 없으니 직접 추가해야 합니다:

```php
use App\Jobs\Middleware\RateLimited;

/**
 * 잡 실행 전, 미들웨어 배열 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited];
}
```

> [!NOTE]
> 잡 미들웨어는 [큐잉 이벤트 리스너](/docs/12.x/events#queued-event-listeners), [메일러블](/docs/12.x/mail#queueing-mail), [알림](/docs/12.x/notifications#queueing-notifications)에도 사용할 수 있습니다.

<a name="rate-limiting"></a>
### 레이트 리미팅

직접 레이트 리미팅 미들웨어를 작성하지 않아도, Laravel에는 기본 제공되는 레이트 리밋 미들웨어가 있습니다. [라우트 레이트 리미터](/docs/12.x/routing#defining-rate-limiters)와 비슷하게, 잡 레이트 리미터는 `RateLimiter` 파사드의 `for` 메서드로 정의합니다.

예를 들어, 무료 사용자는 데이터 백업을 1시간에 1번만, 프리미엄 고객은 제한 없이 가능하게 하고 싶다고 합시다. `AppServiceProvider`의 `boot` 메서드에서 아래처럼 레이트 리밋을 정의할 수 있습니다:

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

여기서는 시간 단위(rate-per-hour)를 적용했지만, `perMinute` 방식도 가능합니다. 그리고 레이트 리밋 `by()` 메서드에는 고객 등 원하는 기준을 넘길 수 있습니다:

```php
return Limit::perMinute(50)->by($job->user->id);
```

레이트 리밋을 정의했다면, 잡 클래스 `middleware`에서 `Illuminate\Queue\Middleware\RateLimited`를 추가해 사용할 수 있습니다. 잡이 레이트 리밋에 걸리면, 이 미들웨어는 잡을 적절한 대기로(release) 큐에 다시 넣습니다.

```php
use Illuminate\Queue\Middleware\RateLimited;

/**
 * 잡 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited('backups')];
}
```

레이트 리밋된 잡도 전체 `attempts`(재시도 횟수)가 증가하므로, `tries`, `maxExceptions` 속성을 상황에 맞게 조정하거나, [retryUntil 메서드](#time-based-attempts)로 재시도 제한 시간을 지정하는 것이 좋습니다.

`releaseAfter` 메서드로 잡을 다시 시도할 최소 대기 시간을(초 단위) 직접 지정할 수 있습니다:

```php
/**
 * 잡 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new RateLimited('backups'))->releaseAfter(60)];
}
```

레이트 리밋에 걸렸을 때 잡을 더 이상 재시도하지 않으려면 `dontRelease`를 사용하세요:

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
> Redis를 사용할 경우, 더 효율적인 `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어를 사용할 수 있습니다.

<a name="preventing-job-overlaps"></a>
### 잡 중복 실행 방지

Laravel에는 잡 중복 실행을 막을 수 있는 `Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어가 있습니다. 임의의 키로 잡 중복 실행을 방지할 수 있어서, 동시 실행 시 문제가 되는 리소스를 안전하게 다룰 수 있습니다.

예를 들어, 특정 사용자의 신용점수 갱신 잡이 동시에 여러 개 실행되지 않도록 하고 싶다면 아래처럼 사용할 수 있습니다:

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

동일 타입의 중복 잡은 큐로 다시 보내집니다. 잡을 다시 시도할 최소 대기 시간도 `releaseAfter`로 정할 수 있습니다:

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

중복 잡을 즉시 삭제(재시도 불가)하려면 `dontRelease`를 사용하세요:

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

`WithoutOverlapping` 미들웨어는 Laravel 원자적 락(atomic lock) 기능을 사용합니다. 잡이 예기치 않게 실패하거나 타임아웃날 때 락이 풀리지 않을 수 있으므로, `expireAfter`로 락 만료 시간을 명시하는 것도 가능합니다:

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
> `WithoutOverlapping` 미들웨어는 [락을 지원하는 캐시 드라이버](/docs/12.x/cache#atomic-locks)가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array`가 지원됩니다.

<a name="sharing-lock-keys"></a>
#### 여러 잡 클래스 간에 락 키 공유

기본적으로 `WithoutOverlapping` 미들웨어는 **동일 클래스** 내 중복 잡만 방지합니다. 즉, 다른 클래스라면 동일 키를 사용해도 제한받지 않습니다. 만약 여러 잡 클래스 간에도 동일 키로 락을 공유하고 싶으면 `shared` 메서드를 호출하세요:

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
### 예외 발생 제한(Throttling)

Laravel에는 `Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어가 있어 예외 발생을 제한할 수 있습니다. 잡이 지정된 횟수 만큼 예외를 발생시키면, 이후 시도는 지정 시간만큼 지연됩니다. 이는 외부 서비스 연동 시 불안정한 상황을 제어할 때 유용합니다.

예를 들어, 외부 API를 호출하는 잡에서 예외가 자주 발생한다면 다음처럼 사용할 수 있습니다. 일반적으로 [시간 기반 재시도](#time-based-attempts)를 함께 활용하길 권장합니다:

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
    return [new ThrottlesExceptions(10, 5 * 60)];
}

/**
 * 잡 타임아웃 시각 결정
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(30);
}
```

미들웨어의 첫 번째 파라미터는 예외 허용 횟수, 두 번째는 제한 이후 재시도까지 대기 시간(초)입니다.

예외 허용 횟수에 도달하지 않더라도 지연을 적용하고 싶으면, `backoff` 메서드로 분 단위 딜레이를 지정할 수 있습니다:

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 5 * 60))->backoff(5)];
}
```

내부적으로 캐시 시스템에 잡 클래스명이 키로 저장돼 제한이 적용됩니다. 여러 잡이 같은 외부 서비스로 동작한다면, `by` 메서드로 키를 직접 지정해 묶을 수 있습니다:

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->by('key')];
}
```

기본적으로 **모든 예외**에 제한이 적용됩니다. 특정 예외에만 제한을 적용하려면, `when` 메서드를 써서 클로저에서 true 일 때만 제한하도록 지정할 수 있습니다:

```php
use Illuminate\Http\Client\HttpClientException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡 미들웨어 반환
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

예외가 발생했을 때 잡을 단순히 큐로 되돌리지(재시도) 않고, 즉시 삭제하려면 `deleteWhen`을 사용합니다:

```php
use App\Exceptions\CustomerDeletedException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(2, 10 * 60))->deleteWhen(CustomerDeletedException::class)];
}
```

예외 발생 시 애플리케이션의 예외 핸들러로 예외를 리포팅(report)하려면, `report` 메서드에 클로저를 넘길 수 있으며, 클로저에서 true를 반환할 때만 리포팅됩니다:

```php
use Illuminate\Http\Client\HttpClientException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡 미들웨어 반환
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
> Redis를 사용할 경우, 더 최적화된 `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어를 사용할 수 있습니다.

<a name="skipping-jobs"></a>
### 잡 스킵(건너뛰기)

`Skip` 미들웨어를 사용하면, 잡 로직을 수정하지 않고 조건에 따라 잡을 삭제(건너뛰기)할 수 있습니다. `Skip::when`은 전달 조건이 true일 때 잡을 삭제하고, `Skip::unless`는 false일 때 잡을 삭제합니다:

```php
use Illuminate\Queue\Middleware\Skip;

/**
 * 잡 미들웨어 반환
 */
public function middleware(): array
{
    return [
        Skip::when($someCondition),
    ];
}
```

더 복잡한 조건 평가가 필요할 때는 클로저를 넘길 수도 있습니다:

```php
use Illuminate\Queue\Middleware\Skip;

/**
 * 잡 미들웨어 반환
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

<!--  
    이후 절부터도 동일하게 방침 및 규칙을 따라 문단별 번역, 코드 블록, 키워드, 파일/클래스/메서드 유지 등 적용합니다.
    전체 텍스트가 매우 길어, 이 요청 내에서 반드시 완결 편집을 해주세요. (본문이 너무 길다면 이어서 요청해주시면 됩니다.)
-->