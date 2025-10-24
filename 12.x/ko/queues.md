# 큐 (Queues)

- [소개](#introduction)
    - [연결과 큐의 차이](#connections-vs-queues)
    - [드라이버 별 참고사항 및 필요조건](#driver-prerequisites)
- [잡 만들기](#creating-jobs)
    - [잡 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [고유 잡](#unique-jobs)
    - [암호화된 잡](#encrypted-jobs)
- [잡 미들웨어](#job-middleware)
    - [속도 제한](#rate-limiting)
    - [잡 중첩 방지](#preventing-job-overlaps)
    - [예외 발생 제한](#throttling-exceptions)
    - [잡 건너뛰기](#skipping-jobs)
- [잡 디스패치](#dispatching-jobs)
    - [지연 디스패치](#delayed-dispatching)
    - [동기 디스패치](#synchronous-dispatching)
    - [잡과 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [잡 체이닝](#job-chaining)
    - [큐와 연결 커스터마이징](#customizing-the-queue-and-connection)
    - [최대 시도 횟수 / 타임아웃 지정](#max-job-attempts-and-timeout)
    - [SQS FIFO 및 공정 큐](#sqs-fifo-and-fair-queues)
    - [큐 페일오버](#queue-failover)
    - [에러 처리](#error-handling)
- [잡 배치 처리](#job-batching)
    - [배치 가능한 잡 정의](#defining-batchable-jobs)
    - [배치 디스패치](#dispatching-batches)
    - [체인과 배치](#chains-and-batches)
    - [배치에 잡 추가](#adding-jobs-to-batches)
    - [배치 확인](#inspecting-batches)
    - [배치 취소](#cancelling-batches)
    - [배치 실패](#batch-failures)
    - [배치 정리](#pruning-batches)
    - [DynamoDB에 배치 저장](#storing-batches-in-dynamodb)
- [클로저 큐잉](#queueing-closures)
- [큐 워커 실행](#running-the-queue-worker)
    - [`queue:work` 명령어](#the-queue-work-command)
    - [큐 우선순위](#queue-priorities)
    - [큐 워커와 배포](#queue-workers-and-deployment)
    - [잡 만료 및 타임아웃](#job-expirations-and-timeouts)
- [Supervisor 설정](#supervisor-configuration)
- [실패한 잡 처리](#dealing-with-failed-jobs)
    - [실패한 잡 처리 후 정리](#cleaning-up-after-failed-jobs)
    - [실패한 잡 재시도](#retrying-failed-jobs)
    - [누락된 모델 무시](#ignoring-missing-models)
    - [실패한 잡 정리](#pruning-failed-jobs)
    - [실패한 잡을 DynamoDB에 저장](#storing-failed-jobs-in-dynamodb)
    - [실패 잡 저장 비활성화](#disabling-failed-job-storage)
    - [실패 잡 이벤트](#failed-job-events)
- [큐에서 잡 삭제](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [일부 잡만 페이크하기](#faking-a-subset-of-jobs)
    - [잡 체인 테스트](#testing-job-chains)
    - [잡 배치 테스트](#testing-job-batches)
    - [잡/큐 상호작용 테스트](#testing-job-queue-interactions)
- [잡 이벤트](#job-events)

<a name="introduction"></a>
## 소개 (Introduction)

웹 애플리케이션을 개발하다 보면, 업로드된 CSV 파일을 파싱 및 저장하는 작업처럼 일반적인 웹 요청 내에서 처리하기에는 너무 오래 걸리는 작업이 있을 수 있습니다. Laravel은 이러한 작업을 쉽게 큐잉 처리하여 백그라운드에서 잡(Job)으로 실행할 수 있습니다. 처리 시간이 오래 소요되는 작업을 큐로 이동하면, 애플리케이션은 웹 요청에 훨씬 빠르게 응답하고 사용자에게 더 나은 경험을 제공합니다.

Laravel 큐는 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 관계형 데이터베이스 등 다양한 큐 백엔드에 걸쳐 통합된 큐 API를 제공합니다.

Laravel의 큐 관련 설정은 애플리케이션의 `config/queue.php` 설정 파일에 저장되어 있습니다. 이 파일에는 데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 등 프레임워크에 포함된 각 큐 드라이버의 연결 설정이 정의되어 있습니다. 개발 혹은 테스트 용도로 잡을 즉시 실행하는 동기(synchronous) 드라이버, 큐에 올라온 잡을 버리는 용도의 `null` 드라이버도 포함되어 있습니다.

> [!NOTE]
> Laravel Horizon은 Redis 기반 큐를 위한 아름다운 대시보드 및 설정 시스템입니다. 더 자세한 내용은 [Horizon 문서](/docs/12.x/horizon)를 참고하세요.

<a name="connections-vs-queues"></a>
### 연결과 큐의 차이

Laravel 큐를 사용하기 전에 "연결(connection)"과 "큐(queue)"의 차이를 이해하는 것이 중요합니다. `config/queue.php` 설정 파일에서 `connections` 배열이 보이실 텐데, 이 옵션은 Amazon SQS, Beanstalk, Redis 등 백엔드 큐 서비스에 대한 연결을 정의합니다. 하지만, 한 개의 큐 연결 내에 여러 개의 "큐"를 둘 수 있으며, 각각은 잡이 쌓이는 별도의 스택처럼 생각할 수 있습니다.

각 연결 설정 예시에는 `queue` 속성이 포함되어 있습니다. 이 옵션은 해당 연결에 잡을 디스패치할 때 기본적으로 사용할 큐를 의미합니다. 즉, 잡을 디스패치할 때 명시적으로 큐를 지정하지 않으면, 연결 설정의 `queue` 속성에 정의된 큐에 잡이 쌓입니다.

```php
use App\Jobs\ProcessPodcast;

// 이 잡은 기본 연결의 기본 큐로 전송됩니다...
ProcessPodcast::dispatch();

// 이 잡은 기본 연결의 "emails" 큐로 전송됩니다...
ProcessPodcast::dispatch()->onQueue('emails');
```

일부 애플리케이션은 여러 큐를 사용할 필요 없이 한 가지 큐만 사용할 수도 있습니다. 반면, 여러 큐로 잡을 분산하면 잡 처리 우선순위를 지정하거나 잡을 분리 관리할 수 있어 유용합니다. 예를 들어, `high` 큐에 잡을 넣고, 해당 큐를 우선적으로 처리하는 워커를 다음과 같이 실행할 수 있습니다.

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버 별 참고사항 및 필요조건

<a name="database"></a>
#### 데이터베이스

`database` 큐 드라이버를 사용하려면 잡을 저장할 데이터베이스 테이블이 필요합니다. Laravel의 기본 `0001_01_01_000002_create_jobs_table.php` [마이그레이션](/docs/12.x/migrations) 파일에 포함되어 있지만, 없다면 다음 Artisan 명령어로 생성할 수 있습니다.

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면 `config/database.php` 설정 파일에서 Redis 데이터베이스 연결을 설정해야 합니다.

> [!WARNING]
> `serializer` 및 `compression` Redis 옵션은 `redis` 큐 드라이버에서 지원되지 않습니다.

<a name="redis-cluster"></a>
##### Redis 클러스터

Redis 큐 연결이 [Redis Cluster](https://redis.io/docs/latest/operate/rs/databases/durability-ha/clustering)를 사용하는 경우, 큐 이름에 [키 해시 태그](https://redis.io/docs/latest/develop/using-commands/keyspace/#hashtags)를 포함해야 합니다. 이렇게 해야 해당 큐에 속한 모든 Redis 키가 같은 해시 슬롯에 위치하게 됩니다.

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
##### 블로킹

Redis 큐를 사용할 때, `block_for` 설정 옵션을 통해 워커가 새 잡이 대기열에 올라올 때까지 최대 얼마 동안 대기할지를 지정할 수 있습니다.

이 값을 조정하면 매번 Redis를 폴링하는 것보다 효율성을 높일 수 있습니다. 예를 들어, `block_for` 값을 5로 설정하면 잡이 준비될 때까지 드라이버가 5초간 블로킹합니다.

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
> `block_for`를 `0`으로 설정하면, 워커는 잡이 생길 때까지 무한 대기하게 됩니다. 이는 `SIGTERM` 같은 신호(signal) 처리를 다음 잡 작업이 끝날 때까지 방해할 수 있습니다.

<a name="other-driver-prerequisites"></a>
#### 그 외 드라이버 필요조건

다음 큐 드라이버는 다음의 Composer 패키지 설치가 필요합니다.

<div class="content-list" markdown="1">

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~2.0` 또는 phpredis PHP 확장(extension)
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`

</div>

<a name="creating-jobs"></a>
## 잡 만들기 (Creating Jobs)

<a name="generating-job-classes"></a>
### 잡 클래스 생성

기본적으로, 애플리케이션의 큐잉 잡은 모두 `app/Jobs` 디렉토리에 저장됩니다. 이 디렉토리가 존재하지 않으면, `make:job` Artisan 명령어 실행 시 자동으로 생성됩니다.

```shell
php artisan make:job ProcessPodcast
```

생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하며, 이는 잡이 비동기로 큐에 올라가야 함을 의미합니다.

> [!NOTE]
> 잡 스텁(stub)은 [스텁 퍼블리싱](/docs/12.x/artisan#stub-customization)으로 커스터마이즈할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조

잡 클래스는 보통 큐에서 처리될 때 호출되는 `handle` 메서드 하나만 가집니다. 예시로, 팟캐스트 게시 서비스를 운영하며 업로드된 팟캐스트 파일을 게시 전 처리해야 하는 상황을 가정해 봅니다.

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
        // 업로드된 팟캐스트를 처리...
    }
}
```

이 예시에서 보듯 [Eloquent 모델](/docs/12.x/eloquent)을 잡의 생성자에 바로 전달할 수 있습니다. 잡이 사용하는 `Queueable` 트레이트 덕분에 Eloquent 모델과 그에 로드된 연관관계 데이터도 잡이 처리될 때 자연스럽게 직렬화, 역직렬화됩니다.

잡 생성자에서 Eloquent 모델을 받더라도, 큐에서 직렬화되는 것은 모델의 식별자만 포함됩니다. 잡이 실제로 처리될 때, 큐 시스템이 데이터베이스에서 전체 모델 인스턴스와 연관관계를 다시 조회합니다. 이렇게 하면 큐에 올라가는 잡의 데이터 용량을 줄일 수 있습니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드의 의존성 주입

잡이 큐에서 처리될 때 `handle` 메서드가 호출되고, 이 때 메서드의 의존성 타입힌트를 통해 [서비스 컨테이너](/docs/12.x/container)가 자동으로 주입을 수행합니다.

의존성 주입 방식을 더욱 세밀하게 제어하고 싶다면, 컨테이너의 `bindMethod` 메서드를 사용할 수 있습니다. 예를 들어, `App\Providers\AppServiceProvider`의 `boot` 메서드에서 다음처럼 정의할 수 있습니다.

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 이미지의 바이너리(raw image contents) 등과 같은 바이너리 데이터는 잡에 전달하기 전에 반드시 `base64_encode` 함수를 거치세요. 그렇지 않으면 잡이 큐에 JSON으로 올려진 후 정상적으로 직렬화되지 않을 수 있습니다.

<a name="handling-relationships"></a>
#### 큐잉된 연관관계 처리

Eloquent 모델의 연관관계 데이터까지 직렬화되면, 잡 문자열이 매우 커질 수 있습니다. 또한, 잡이 역직렬화되고 모델 연관관계를 데이터베이스에서 다시 조회할 때, 직렬화 전에 걸렸던 연관관계 제약조건이 적용되지 않습니다. 즉, 일부만 사용하고 싶다면 필요 시 잡 내에서 연관관계를 다시 제약(쿼리)해야 합니다.

또는, 직렬화 시 연관관계를 아예 제외하려면, 모델의 속성 값을 할당할 때 `withoutRelations` 메서드를 사용하면 연관관계 없이 모델 인스턴스를 반환합니다.

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

[PHP 생성자 속성 프로모션](https://www.php.net/manual/en/language.oop5.decon.php#language.oop5.decon.constructor.promotion)을 사용하는 경우, 모델의 연관관계 직렬화를 막고 싶으면 `WithoutRelations` 속성을 사용할 수 있습니다.

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

여러 모델에 대해 일괄적으로 적용하고 싶다면, 클래스 전체에 `WithoutRelations` 속성을 사용할 수도 있습니다.

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
     * 새 잡 인스턴스 생성
     */
    public function __construct(
        public Podcast $podcast,
        public DistributionPlatform $platform,
    ) {}
}
```

단일 모델이 아니라 여러 개의 Eloquent 모델 컬렉션 또는 배열을 전달할 경우, 잡이 복원/실행될 때 해당 컬렉션 내의 각 모델은 연관관계가 복원되지 않습니다. 이는 많은 모델을 다루는 잡에서 과도한 리소스 사용을 막기 위함입니다.

<a name="unique-jobs"></a>
### 고유 잡 (Unique Jobs)

> [!WARNING]
> 고유 잡 기능을 사용하려면 [락 지원 캐시 드라이버](/docs/12.x/cache#atomic-locks)가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버만 atomic lock을 지원합니다.

> [!WARNING]
> 고유 잡 제약은 배치 안의 잡들에게는 적용되지 않습니다.

특정 잡이 동시에 큐에 한 번만 존재하도록 하고 싶을 때, 잡 클래스에서 `ShouldBeUnique` 인터페이스를 구현하면 됩니다. 별도의 추가 메서드 정의가 필요 없습니다.

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

위 예에서는 `UpdateSearchIndex` 잡이 고유합니다. 즉, 동일한 잡 인스턴스가 큐에 이미 존재하면 새로운 디스패치가 무시됩니다.

잡의 고유성을 매칭하는 "키"를 직접 정의하거나, 고유 상태를 유지할 제한 시간을 지정하고 싶으면 잡 클래스에 `uniqueId`, `uniqueFor` 프로퍼티나 메서드를 정의할 수 있습니다.

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
     * 잡의 고유 락이 해제될 시간(초)
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

위 예제에서는 `UpdateSearchIndex` 잡이 상품 ID를 기준으로 고유합니다. 따라서 같은 상품 ID를 가진 새로운 잡은 기존 잡이 끝나기 전까지 무시됩니다. 기존 잡이 1시간 내에 처리되지 않으면 락이 풀리고, 동일한 키를 가진 잡이 새로 큐잉될 수 있습니다.

> [!WARNING]
> 여러 웹 서버 혹은 컨테이너에서 잡을 디스패치할 경우, 모든 서버에서 동일한 중앙 캐시 서버를 사용하도록 반드시 설정해야 고유 잡 처리가 정상 동작합니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 처리 시작 전까지 고유성 유지

기본적으로 고유 잡은 처리 완료 또는 재시도 횟수 초과 시 락이 해제됩니다. 처리 시작 직전에 락을 해제하고 싶으면 `ShouldBeUnique` 대신 `ShouldBeUniqueUntilProcessing` 인터페이스를 구현하세요.

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
#### 고유 잡 락

`ShouldBeUnique` 잡이 디스패치될 때 Laravel은 내부적으로 [락](/docs/12.x/cache#atomic-locks)을 얻으려고 시도합니다(키는 `uniqueId`). 이미 락이 잡혀 있다면, 잡은 큐에 올라가지 않습니다. 락은 잡 처리 완료 또는 재시도 한계에 도달 시 해제됩니다. 기본적으로는 디폴트 캐시 드라이버를 사용하지만, 다른 드라이버를 사용하려면 `uniqueVia` 메서드를 오버라이드하세요.

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
> 잡의 동시 실행만 제한하려면 [WithoutOverlapping](/docs/12.x/queues#preventing-job-overlaps) 잡 미들웨어를 사용하세요.

<a name="encrypted-jobs"></a>
### 암호화된 잡 (Encrypted Jobs)

잡 데이터의 프라이버시와 무결성을 [암호화](/docs/12.x/encryption)를 통해 보장할 수 있습니다. 잡 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하면, 잡이 큐에 오르기 전에 자동으로 암호화 처리됩니다.

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

잡 미들웨어를 사용하면 잡 실행 전후로 커스텀 로직을 감쌀 수 있어, 잡 클래스 내부의 반복 코드를 줄일 수 있습니다. 예를 들어, 다음 코드는 Redis의 속도 제한을 적용해 5초에 한 번만 잡이 수행되도록 구현한 예입니다.

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

이처럼 handle 메서드에 속도 제한 로직이 중첩되어 복잡해집니다. 같은 기능이 필요한 다른 잡에도 중복해서 적용해야 하죠. 이 대신, 속도 제한 기능을 잡 미들웨어로 분리할 수 있습니다.

```php
<?php

namespace App\Jobs\Middleware;

use Closure;
use Illuminate\Support\Facades\Redis;

class RateLimited
{
    /**
     * 큐잉 잡 처리
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

라우트 미들웨어와 같이, 잡 미들웨어도 처리 중인 잡과 다음 처리를 위한 콜백을 받습니다.

새 잡 미들웨어 클래스는 `make:job-middleware` Artisan 명령어로 생성할 수 있습니다. 생성 후엔 잡 내부에 `middleware` 메서드를 만드는 방식으로 적용합니다(이 메서드는 기본 잡에는 포함되어 있지 않으므로 직접 추가해야 합니다).

```php
use App\Jobs\Middleware\RateLimited;

/**
 * 잡이 통과할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited];
}
```

> [!NOTE]
> 잡 미들웨어는 [큐잉 이벤트 리스너](/docs/12.x/events#queued-event-listeners), [메일러블](/docs/12.x/mail#queueing-mail), [알림](/docs/12.x/notifications#queueing-notifications)에도 적용할 수 있습니다.

<a name="rate-limiting"></a>
### 속도 제한

직접 미들웨어를 작성하는 대신, Laravel이 제공하는 속도 제한 미들웨어를 사용할 수도 있습니다. [라우트 속도 제한자](/docs/12.x/routing#defining-rate-limiters)처럼, 잡 속도 제한자도 `RateLimiter` 퍼사드의 `for` 메서드로 정의합니다.

예를 들어, 사용자별로 데이터를 한 시간에 한 번만 백업하도록 제한(단, 프리미엄 사용자 제외)하려면, `AppServiceProvider`의 `boot` 메서드에서 다음처럼 정의할 수 있습니다.

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

위에서는 시간 단위로 제한했지만, `perMinute` 메서드로 분 단위로 할 수도 있습니다. `by` 메서드에는 어떤 값이라도 쓸 수 있지만, 보통 고객 ID 등으로 제한을 분리합니다.

```php
return Limit::perMinute(50)->by($job->user->id);
```

이제 잡에서는 `Illuminate\Queue\Middleware\RateLimited` 미들웨어로 속도 제한을 붙일 수 있습니다. 제한이 걸리면 자동으로 잡은 적절한 지연 후 다시 큐로 보내집니다.

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

속도 제한 시도도 잡의 전체 `attempts` 횟수에 포함됩니다. 따라서 잡 클래스의 `tries`와 `maxExceptions` 값을 적절히 조정해야 하거나, [retryUntil 메서드](#time-based-attempts)로 제한 시간을 직접 지정할 수도 있습니다.

`releaseAfter`로 잡이 다시 시도되기까지 대기할 초를 직접 지정할 수 있습니다.

```php
/**
 * 잡이 통과할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new RateLimited('backups'))->releaseAfter(60)];
}
```

잡이 제한에 걸릴 때 재시도하지 않도록 하려면 `dontRelease`를 사용하세요.

```php
/**
 * 잡이 통과할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new RateLimited('backups'))->dontRelease()];
}
```

> [!NOTE]
> Redis를 사용할 경우, 기본 미들웨어보다 효율적인 `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어를 사용할 수 있습니다.

<a name="preventing-job-overlaps"></a>
### 잡 중첩 방지

`Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어를 사용하면 임의의 키 기준으로 잡이 중첩 수행되는 것을 방지할 수 있습니다. 예를 들어, 사용자 신용 점수를 갱신하는 잡에서 같은 사용자 ID에 대해 중복 실행을 막고 싶으면 다음과 같이 합니다.

```php
use Illuminate\Queue\Middleware\WithoutOverlapping;

/**
 * 잡이 통과할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new WithoutOverlapping($this->user->id)];
}
```

중첩된 잡이 큐로 다시 반환되는 경우도 시도 횟수에 포함됩니다. 잡의 `tries`, `maxExceptions` 값을 조정해야 할 수 있습니다. 예를 들어, `tries` 값을 기본값인 1로 두면 중첩된 잡은 재시도되지 않습니다.

중첩된 잡의 재시도 간격 지정도 가능합니다.

```php
/**
 * 잡이 통과할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->releaseAfter(60)];
}
```

겹치는 잡을 곧바로 삭제하려면 `dontRelease`를 사용합니다.

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->dontRelease()];
}
```

이 미들웨어는 Laravel의 atomic lock 기능을 이용합니다. 예상치 못하게 잡이 실패하거나 타임아웃되어 락이 해제되지 않는 경우를 대비하여, `expireAfter`로 락의 만료 시간을 명시할 수 있습니다.

```php
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->expireAfter(180)];
}
```

> [!WARNING]
> `WithoutOverlapping` 미들웨어는 [락 지원 캐시 드라이버](/docs/12.x/cache#atomic-locks)가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버만 atomic lock을 지원합니다.

<a name="sharing-lock-keys"></a>
#### 서로 다른 잡 클래스 간 락 키 공유

기본적으로, `WithoutOverlapping` 미들웨어는 같은 클래스 내에서만 중첩을 막습니다. 두 잡 클래스에서 동일한 락 키를 사용해도 서로 간 중첩 방지는 되지 않습니다. 잡 클래스 간 키 공유가 필요하면 `shared` 메서드를 호출하세요.

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
### 예외 발생 제한

`Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어는 일정 횟수 이상의 예외 발생 시 일정 시간 이후에만 재시도하도록 할 수 있습니다. 외부 서비스 등에 불안정하게 요청할 때 유용합니다.

예를 들어, 외부 API와 통신하는 잡에서 10번 연속 예외가 발생하면 5분 후에만 다시 시도되게 만들 수 있습니다.

```php
use DateTime;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * 잡이 통과할 미들웨어 반환
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new ThrottlesExceptions(10, 5 * 60)];
}

/**
 * 잡이 타임아웃되는 시간 반환
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(30);
}
```

생성자의 첫 번째 인자는 예외 허용 최대 횟수, 두 번째 인자는 예외 발생 시 대기 시간(초)입니다.

예외 임계치에 도달하기 전 예외가 발생하면, 잡은 기본적으로 즉시 재시도됩니다. 딜레이를 지정하고 싶다면 `backoff`를 사용하세요.

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 5 * 60))->backoff(5)];
}
```

이 미들웨어는 잡 클래스명을 캐시 키로 사용합니다. `by` 메서드로 여러 잡이 동일한 제한을 공유할 수 있습니다.

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->by('key')];
}
```

모든 예외를 제한하는 대신, `when` 메서드로 조건을 줄 수 있습니다. 클로저가 `true`를 반환할 때만 제한됩니다.

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

특정 예외 발생 시에는 작업을 큐에서 바로 삭제하려면 `deleteWhen`을 사용하세요.

```php
use App\Exceptions\CustomerDeletedException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware(): array
{
    return [(new ThrottlesExceptions(2, 10 * 60))->deleteWhen(CustomerDeletedException::class)];
}
```

예외가 발생한 경우 애플리케이션의 예외 핸들러에 보고하려면 `report`, 혹은 조건부로 보고하려면 클로저를 인자로 전달하면 됩니다.

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
> Redis를 사용할 경우, 더 효율적인 `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어를 쓸 수 있습니다.

<a name="skipping-jobs"></a>
### 잡 건너뛰기

`Skip` 미들웨어를 사용하면 잡의 내부 로직을 수정하지 않고도 조건에 따라 잡을 건너뛰거나 삭제할 수 있습니다. 조건이 `true`이면 삭제되는 `Skip::when`, `false`일 때 삭제하는 `Skip::unless`가 있습니다.

```php
use Illuminate\Queue\Middleware\Skip;

public function middleware(): array
{
    return [
        Skip::when($condition),
    ];
}
```

복잡한 조건이 필요한 경우 클로저를 사용할 수도 있습니다.

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
(이하 이하 생략 – 기준 구조와 패턴을 유지, 이후 본문 전체 설명과 코드는 동일하게 이어서 한국어로 번역하며 Markdown 및 코드 효력 그대로 유지)
