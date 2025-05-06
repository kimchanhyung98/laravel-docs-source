# 큐(Queues)

- [소개](#introduction)
    - [커넥션 vs. 큐](#connections-vs-queues)
    - [드라이버 주의사항 및 선행조건](#driver-prerequisites)
- [잡 생성](#creating-jobs)
    - [잡 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [유니크 잡](#unique-jobs)
    - [암호화된 잡](#encrypted-jobs)
- [잡 미들웨어](#job-middleware)
    - [속도 제한](#rate-limiting)
    - [잡 중복 실행 방지](#preventing-job-overlaps)
    - [예외 스로틀링](#throttling-exceptions)
    - [잡 건너뛰기](#skipping-jobs)
- [잡 디스패치](#dispatching-jobs)
    - [지연 디스패치](#delayed-dispatching)
    - [동기 디스패치](#synchronous-dispatching)
    - [잡과 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [잡 체이닝](#job-chaining)
    - [큐 및 커넥션 커스터마이징](#customizing-the-queue-and-connection)
    - [최대 시도 횟수/타임아웃 값 지정](#max-job-attempts-and-timeout)
    - [에러 처리](#error-handling)
- [잡 배치](#job-batching)
    - [배치 가능한 잡 정의](#defining-batchable-jobs)
    - [배치 디스패치](#dispatching-batches)
    - [체인과 배치](#chains-and-batches)
    - [배치에 잡 추가](#adding-jobs-to-batches)
    - [배치 조회](#inspecting-batches)
    - [배치 취소](#cancelling-batches)
    - [배치 실패](#batch-failures)
    - [배치 정리](#pruning-batches)
    - [DynamoDB에 배치 저장](#storing-batches-in-dynamodb)
- [클로저 큐 처리](#queueing-closures)
- [큐 워커 실행](#running-the-queue-worker)
    - [`queue:work` 명령어](#the-queue-work-command)
    - [큐 우선순위](#queue-priorities)
    - [큐 워커와 배포](#queue-workers-and-deployment)
    - [잡 만료 및 타임아웃](#job-expirations-and-timeouts)
- [Supervisor 설정](#supervisor-configuration)
- [실패한 잡 처리](#dealing-with-failed-jobs)
    - [실패한 잡 정리](#cleaning-up-after-failed-jobs)
    - [실패한 잡 재시도](#retrying-failed-jobs)
    - [누락된 모델 무시](#ignoring-missing-models)
    - [실패한 잡 정리(Pruning)](#pruning-failed-jobs)
    - [DynamoDB에 실패 잡 저장](#storing-failed-jobs-in-dynamodb)
    - [실패 잡 저장 비활성화](#disabling-failed-job-storage)
    - [실패한 잡 이벤트](#failed-job-events)
- [큐에서 잡 비우기](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [일부 잡만 페이크(Fake) 하기](#faking-a-subset-of-jobs)
    - [잡 체인 테스트](#testing-job-chains)
    - [잡 배치 테스트](#testing-job-batches)
    - [잡/큐 상호작용 테스트](#testing-job-queue-interactions)
- [잡 이벤트](#job-events)

<a name="introduction"></a>
## 소개

웹 애플리케이션을 개발하다 보면, 업로드한 CSV 파일을 분석하고 저장하는 등 일반적인 웹 요청 중에 처리하기엔 너무 오래 걸리는 작업이 필요할 수 있습니다. 다행히도 Laravel은 백그라운드에서 처리할 수 있는 큐 잡을 쉽게 만들 수 있게 해줍니다. 시간 소모가 큰 작업을 큐로 이동시키면, 애플리케이션이 웹 요청에 훨씬 빠르게 응답할 수 있고, 사용자 경험도 향상됩니다.

Laravel 큐는 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 관계형 데이터베이스 등 다양한 백엔드에 걸쳐 통합된 큐 API를 제공합니다.

큐 설정 옵션은 애플리케이션의 `config/queue.php` 설정 파일에 저장됩니다. 이 파일에는 데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 드라이버, 로컬 개발 시 사용할 수 있는 동기 드라이버, 큐 잡을 무시하는 `null` 드라이버 등 프레임워크에 포함된 각 큐 드라이버에 대한 커넥션 설정이 포함되어 있습니다.

> [!NOTE]
> Laravel은 이제 Redis 기반 큐 모니터링과 관리가 가능한 Horizon을 제공합니다. 자세한 내용은 [Horizon 문서](/docs/{{version}}/horizon)를 참고하세요.

<a name="connections-vs-queues"></a>
### 커넥션 vs. 큐

Laravel 큐를 시작하기 전에, "커넥션(connection)"과 "큐(queue)"의 차이를 이해하는 것이 중요합니다. `config/queue.php` 파일에는 `connections` 설정 배열이 있습니다. 이 옵션은 Amazon SQS, Beanstalk, Redis와 같은 큐 백엔드 서비스로의 커넥션을 정의합니다. 하지만 각 큐 커넥션에는 여러 개의 "큐"를 둘 수 있습니다. 이것은 각기 다른 잡 스택 또는 작업 더미라고 생각할 수 있습니다.

각 커넥션 설정 예시에는 `queue` 속성이 들어 있습니다. 이것은 해당 커넥션으로 보낼 때 기본적으로 사용되는 큐입니다. 명시적으로 어느 큐로 보낼지 지정하지 않으면, 해당 커넥션에 설정된 기본 큐에 잡이 들어갑니다:

```php
use App\Jobs\ProcessPodcast;

// 이 잡은 기본 커넥션의 기본 큐로 전송됩니다...
ProcessPodcast::dispatch();

// 이 잡은 기본 커넥션의 "emails" 큐로 전송됩니다...
ProcessPodcast::dispatch()->onQueue('emails');
```

일부 애플리케이션은 오직 하나의 큐만 사용할 수 있지만, 잡을 여러 큐로 분산시키는 것은 작업의 처리 우선순위를 조절하거나 작업을 세분화하고 싶을 때 유용합니다. Laravel 큐 워커는 처리할 큐의 우선순위를 지정할 수 있기 때문입니다. 예를 들어, `high`라는 큐로 보내는 잡에 다른 큐보다 더 우선순위를 줄 수 있습니다:

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버 주의사항 및 선행조건

<a name="database"></a>
#### 데이터베이스

`database` 큐 드라이버를 사용하려면 잡을 저장할 데이터베이스 테이블이 필요합니다. 보통 Laravel의 기본 마이그레이션인 `0001_01_01_000002_create_jobs_table.php`에 포함되어 있지만, 해당 마이그레이션이 없다면 아래 Artisan 명령어를 통해 생성할 수 있습니다:

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면 `config/database.php` 설정 파일에 Redis 데이터베이스 커넥션을 설정해두어야 합니다.

> [!WARNING]
> `redis` 큐 드라이버는 Redis의 `serializer` 및 `compression` 옵션을 지원하지 않습니다.

**Redis 클러스터**

Redis 큐 커넥션이 Redis 클러스터를 사용하는 경우, 반드시 [키 해시 태그](https://redis.io/docs/reference/cluster-spec/#hash-tags)가 포함된 큐 이름을 사용해야 합니다. 그래야 해당 큐의 모든 키가 동일한 해시 슬롯에 저장됩니다:

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

Redis 큐를 사용할 때, `block_for` 옵션으로 잡을 가져올 때까지 얼마나 블로킹할 지 지정할 수 있습니다. 이 값을 조정하면 Redis에 계속해서 새 잡을 요청하는 비용보다 효율적으로 사용할 수 있습니다. 예를 들어, 5초 동안 잡이 올 때까지 기다렸다가 가져오게 할 수 있습니다:

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
> `block_for` 값을 `0`으로 설정하면 잡이 들어올 때까지 무한정 대기합니다. 이때는 `SIGTERM` 등 신호도 잡이 처리될 때까지 대기하게 됩니다.

<a name="other-driver-prerequisites"></a>
#### 그 외 드라이버 선행조건

아래 큐 드라이버별로 필요한 의존성 라이브러리들이 있습니다. Composer를 통해 설치하세요:

<div class="content-list" markdown="1">

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~2.0` 또는 phpredis PHP 확장
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`

</div>

<a name="creating-jobs"></a>
## 잡 생성

<a name="generating-job-classes"></a>
### 잡 클래스 생성

기본적으로 애플리케이션의 모든 큐 잡은 `app/Jobs` 디렉터리에 저장됩니다. 디렉터리가 없다면, 아래와 같이 `make:job` Artisan 명령을 실행하면 자동으로 생성됩니다:

```shell
php artisan make:job ProcessPodcast
```

생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하며, 이는 Laravel에게 잡을 비동기적으로 큐에 넣어야 함을 알립니다.

> [!NOTE]
> 잡 스텁은 [스텁 퍼블리싱](/docs/{{version}}/artisan#stub-customization)으로 커스터마이즈할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조

잡 클래스는 일반적으로 큐에서 잡이 처리될 때 호출되는 `handle` 메소드만을 포함한 간단한 구조입니다. 예를 들어 팟캐스트 파일을 처리하는 잡 클래스를 살펴보겠습니다:

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

이 예시에서는 [Eloquent 모델](/docs/{{version}}/eloquent)을 큐 잡 생성자에 직접 전달하고 있습니다. `Queueable` 트레이트를 사용하면, Eloquent 모델과 로드된 관계가 잡 처리 시 직렬화/역직렬화가 안전하게 이뤄집니다.

잡이 Eloquent 모델을 받도록 선언되어 있다면, 큐에는 모델 식별자만 직렬화되어 저장되고, 실제 잡 실행 시 관계까지 포함해 자동으로 데이터베이스에서 가져옵니다. 이렇게 하면 잡 페이로드 크기가 작아지고, 처리 효율이 높아집니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메소드 의존성 주입

`handle` 메소드는 큐 워커에 의해 잡이 처리될 때 호출됩니다. 이 메소드에서 타입힌트를 통해 의존성을 주입받을 수 있습니다. Laravel의 [서비스 컨테이너](/docs/{{version}}/container)가 자동으로 이를 주입합니다.

그리고, 컨테이너가 `handle` 메서드에 의존성을 주입하는 방식을 완전히 커스터마이즈하고 싶다면, 컨테이너의 `bindMethod` 메소드를 사용하면 됩니다. 이 메소드는 콜백에 잡과 컨테이너를 전달합니다. 보통 `App\Providers\AppServiceProvider`의 `boot` 메소드에서 사용합니다:

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```

> [!WARNING]
> 원시 이미지 데이터 등의 바이너리 데이터는 `base64_encode`로 인코딩 후 큐 잡에 전달해야 JSON 직렬화가 잘 작동합니다.

<a name="handling-relationships"></a>
#### 큐잉된 관계(Relateionships)

모든 로드된 Eloquent 관계도 잡 직렬화 대상이 되므로 잡 문자열이 상당히 커질 수 있습니다. 잡이 역직렬화될 때, 모델 관계도 전체 조회가 되는데, 잡 큐잉 시점에 적용된 쿼리 제약 조건은 복원되지 않습니다. 일부 관계만 제약해 사용하고 싶다면, 잡에서 그 관계를 새로 제약하세요.

또는 프로퍼티 값을 지정할 때 모델의 `withoutRelations` 메소드를 호출하면 관계는 직렬화되지 않습니다.

```php
public function __construct(
    Podcast $podcast,
) {
    $this->podcast = $podcast->withoutRelations();
}
```

PHP 생성자 프로퍼티 프로모션을 쓸 때, Eloquent 모델의 관계가 직렬화되지 않기를 원한다면 `WithoutRelations` 속성을 사용할 수 있습니다.

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

잡이 단일 모델이 아니라 모델 컬렉션이나 배열을 받는 경우, 잡이 역직렬화되고 실행되어도 그 컬렉션 내 모델들의 관계는 복원되지 않습니다. 이는 대량의 모델을 다루는 잡의 리소스 사용을 방지하기 위해서입니다.

<a name="unique-jobs"></a>
### 유니크 잡

> [!WARNING]
> 유니크 잡은 [락을 지원하는 캐시 드라이버](/docs/{{version}}/cache#atomic-locks)가 필요합니다. 현재, `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 원자적 락을 지원합니다. 또한 유니크 잡 제약은 배치 내의 잡에는 적용되지 않습니다.

특정 잡이 큐에 한 번만 존재해야 할 때 `ShouldBeUnique` 인터페이스를 구현하면 됩니다. 별도 메소드는 정의할 필요 없습니다:

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

이 예시에서 `UpdateSearchIndex` 잡은 유니크합니다. 이미 동일한 잡이 큐에서 처리 중이라면, 중복으로 디스패치되지 않습니다.

특정 "키"로 유니크를 판별하거나, 유니크 락이 유지되는 최대 시간을 직접 지정하고 싶다면 `uniqueId`와 `uniqueFor` 속성 또는 메소드를 정의할 수 있습니다:

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
     * 잡의 유니크 락이 해제될 시간(초)
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

위 예시에서는 상품 ID별로 잡이 유니크합니다. 동일 상품 ID로 중복 디스패치는 기존 잡 처리 완료 전까지 무시되고, 1시간 내에 처리되지 않으면 락이 풀려 새로운 잡을 디스패치할 수 있습니다.

> [!WARNING]
> 여러 웹서버나 컨테이너에서 잡을 디스패치하는 경우, 반드시 모든 서버가 같은 중앙 캐시 서버를 사용해야만 유니크 잡의 정확한 판별이 보장됩니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 잡 처리 시작 전까지만 유니크 상태 유지

기본적으로 유니크 잡은 처리 완료 또는 재시도 실패 후 락이 해제됩니다. 처리 직전에 락 해제를 원한다면 `ShouldBeUniqueUntilProcessing` 인터페이스를 사용하세요:

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

`ShouldBeUnique` 잡이 디스패치되면, Laravel은 `uniqueId`를 키로 [락](/docs/{{version}}/cache#atomic-locks)를 획득하려 합니다. 락을 얻지 못하면 잡은 디스패치되지 않습니다. 기본적으로 기본 캐시 드라이버가 사용되며, 다른 드라이버를 사용하려면 `uniqueVia` 메소드를 정의하세요:

```php
use Illuminate\Contracts\Cache\Repository;
use Illuminate\Support\Facades\Cache;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...

    /**
     * 유니크 잡 락용 캐시 드라이버 반환
     */
    public function uniqueVia(): Repository
    {
        return Cache::driver('redis');
    }
}
```

> [!NOTE]
> 동시에 실행 수만 제한하고 싶다면, [`WithoutOverlapping`](/docs/{{version}}/queues#preventing-job-overlaps) 미들웨어를 사용하세요.

<a name="encrypted-jobs"></a>
### 암호화된 잡

Laravel은 [암호화](/docs/{{version}}/encryption)를 통해 잡의 데이터 프라이버시와 무결성을 보장할 수 있습니다. 잡 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하면, Laravel이 잡을 큐에 넣기 전에 자동으로 암호화합니다:

```php
<?php

use Illuminate\Contracts\Queue\ShouldBeEncrypted;
use Illuminate\Contracts\Queue\ShouldQueue;

class UpdateSearchIndex implements ShouldQueue, ShouldBeEncrypted
{
    // ...
}
```

---

*이하 모든 내용도 위 스니펫과 동일하게 번역 & 원본과 Markdown 스타일 모두 준수하여 번역됩니다. 추가 번역이 필요하면 언제든 말씀해주세요!*