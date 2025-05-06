# 큐 (Queues)

- [소개](#introduction)
    - [커넥션과 큐의 차이](#connections-vs-queues)
    - [드라이버별 참고사항 및 사전 준비](#driver-prerequisites)
- [잡 생성하기](#creating-jobs)
    - [잡 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [유니크 잡](#unique-jobs)
- [잡 미들웨어](#job-middleware)
    - [속도 제한](#rate-limiting)
    - [잡 중복 실행 방지](#preventing-job-overlaps)
    - [예외 트래핑/지연](#throttling-exceptions)
- [잡 디스패치(실행)하기](#dispatching-jobs)
    - [지연 디스패치](#delayed-dispatching)
    - [동기식 디스패치](#synchronous-dispatching)
    - [잡, DB 트랜잭션과 함께 사용](#jobs-and-database-transactions)
    - [잡 체이닝](#job-chaining)
    - [큐/커넥션 커스터마이징](#customizing-the-queue-and-connection)
    - [최대 시도 횟수/타임아웃 설정](#max-job-attempts-and-timeout)
    - [에러 처리](#error-handling)
- [배치 잡 실행](#job-batching)
    - [배치 작업 정의](#defining-batchable-jobs)
    - [배치 디스패치](#dispatching-batches)
    - [배치에 잡 추가하기](#adding-jobs-to-batches)
    - [배치 조회](#inspecting-batches)
    - [배치 취소](#cancelling-batches)
    - [배치 실패 처리](#batch-failures)
    - [배치 데이터 정리(Pruning)](#pruning-batches)
- [클로저 큐잉](#queueing-closures)
- [큐 워커 실행](#running-the-queue-worker)
    - [`queue:work` 명령어](#the-queue-work-command)
    - [큐 우선순위](#queue-priorities)
    - [큐 워커와 배포](#queue-workers-and-deployment)
    - [잡 만료 및 타임아웃](#job-expirations-and-timeouts)
- [Supervisor 설정](#supervisor-configuration)
- [실패한 잡 처리](#dealing-with-failed-jobs)
    - [실패한 잡 정리](#cleaning-up-after-failed-jobs)
    - [실패한 잡 재시도](#retrying-failed-jobs)
    - [존재하지 않는 모델 무시하기](#ignoring-missing-models)
    - [실패 잡 데이터 정리](#pruning-failed-jobs)
    - [DynamoDB에 실패 잡 저장](#storing-failed-jobs-in-dynamodb)
    - [실패 잡 저장 비활성화](#disabling-failed-job-storage)
    - [실패 잡 이벤트](#failed-job-events)
- [큐에서 잡 제거하기](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [잡 이벤트](#job-events)

<a name="introduction"></a>
## 소개

웹 애플리케이션을 개발하다 보면 업로드된 CSV 파일을 파싱하고 저장하는 등 일반적인 웹 요청 동안 수행하기에는 시간이 오래 걸리는 작업이 있을 수 있습니다. Laravel은 이러한 작업을 쉽게 백그라운드에서 처리할 수 있도록 큐 잡(Queued Jobs)을 생성할 수 있도록 지원합니다. 시간이 오래 걸리는 작업을 큐로 옮김으로써, 애플리케이션은 웹 요청에 매우 빠르게 응답하고, 더 나은 사용자 경험을 제공할 수 있습니다.

Laravel의 큐는 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io) 또는 관계형 데이터베이스 등 여러 백엔드를 아우르는 통합 큐 API를 제공합니다.

큐 설정은 애플리케이션의 `config/queue.php` 파일에 저장됩니다. 여기에는 데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 드라이버와 필요한 경우 로컬 개발을 위한 동기 드라이버(즉시 실행), 큐 작업을 버리는 `null` 드라이버가 포함되어 있습니다.

> {tip} Laravel은 Redis 기반 큐를 위한 아름다운 대시보드 및 설정 시스템인 Horizon도 제공합니다. 자세한 내용은 [Horizon 문서](/docs/{{version}}/horizon)를 참고하세요.

<a name="connections-vs-queues"></a>
### 커넥션과 큐의 차이

Laravel 큐를 사용하기 전에 "커넥션(connection)"과 "큐(queue)"의 차이를 이해하는 것이 중요합니다. `config/queue.php`에는 `connections` 배열이 있습니다. 여기에는 Amazon SQS, Beanstalk, Redis 등과 연결하기 위한 설정이 담깁니다. 각 커넥션은 여러 개의 "큐"를 가질 수 있습니다. 큐는 쉽게 말해 잡이 쌓이는 데이터 스택/범주입니다.

각 커넥션에는 `queue`라는 속성이 있는데 잡을 어디에 기본적으로 디스패치할 것인지 지정합니다. 즉, 디스패치 시 별도로 큐를 명시하지 않으면 해당 커넥션의 기본 큐에 잡이 들어갑니다.

예시:
```php
use App\Jobs\ProcessPodcast;

// 기본 커넥션의 기본 큐로 잡 디스패치
ProcessPodcast::dispatch();

// 기본 커넥션의 "emails" 큐로 잡 디스패치
ProcessPodcast::dispatch()->onQueue('emails');
```

일부 애플리케이션은 하나의 큐만 사용하지만, 잡을 여러 큐로 나누어 우선순위별로 처리할 수도 있습니다. 예를 들어, `high` 큐에 넣은 잡을 우선 처리하고 싶다면 다음처럼 워커를 대상으로 실행할 수 있습니다.

```
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버별 참고사항 및 사전 준비

<a name="database"></a>
#### 데이터베이스

`database` 큐 드라이버를 사용하려면 잡을 저장할 테이블이 필요합니다. 마이그레이션 생성을 위해 `queue:table` Artisan 명령어를 실행한 뒤, `migrate` 명령어로 테이블을 만드세요.

```
php artisan queue:table

php artisan migrate
```

그리고 `.env` 파일에서 `QUEUE_CONNECTION=database`로 드라이버를 지정해야 합니다.

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면 `config/database.php`에 Redis 연결 설정이 필요합니다.

**Redis 클러스터**

Redis 클러스터 사용 시, 큐 이름에 [키 해시 태그](https://redis.io/topics/cluster-spec#keys-hash-tags)가 포함되어야 합니다. 예:

```php
'redis' => [
    'driver' => 'redis',
    'connection' => 'default',
    'queue' => '{default}',
    'retry_after' => 90,
],
```

**Blocking**

`block_for` 옵션은 대기할 시간(초)을 지정하여, 워커가 새 잡을 기다리는 동안 효율적으로 Redis DB를 폴링합니다.

```php
'redis' => [
    'driver' => 'redis',
    'connection' => 'default',
    'queue' => 'default',
    'retry_after' => 90,
    'block_for' => 5,
],
```

> {note} `block_for`를 `0`으로 설정하면 워커가 잡이 생길 때까지 무한정 대기합니다. 이 경우 `SIGTERM` 같은 시그널을 잡은 뒤에야 처리할 수 있습니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 준비사항

아래 큐 드라이버를 위해서는 각각 다음 의존 패키지가 필요합니다(Composer로 설치).

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~4.0`
- Redis: `predis/predis ~1.0` 또는 phpredis 확장

<a name="creating-jobs"></a>
## 잡 생성하기

<a name="generating-job-classes"></a>
### 잡 클래스 생성

기본적으로 모든 큐 잡 클래스는 `app/Jobs` 디렉터리에 저장됩니다. 이 폴더가 없으면 `make:job` 명령 실행 시 자동 생성됩니다.

```
php artisan make:job ProcessPodcast
```

생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하여, Laravel이 이 잡을 비동기 큐에 넣을 수 있음을 나타냅니다.

> {tip} 잡 스텁은 [스텁 퍼블리싱](/docs/{{version}}/artisan#stub-customization) 기능으로 사용자 정의할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조

잡 클래스는 보통 큐에서 실행될 때 호출되는 `handle` 메서드만 포함하면 충분합니다. 예:

```php
<?php

namespace App\Jobs;

use App\Models\Podcast;
use App\Services\AudioProcessor;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;

class ProcessPodcast implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    protected $podcast;

    public function __construct(Podcast $podcast)
    {
        $this->podcast = $podcast;
    }

    public function handle(AudioProcessor $processor)
    {
        // 팟캐스트 파일 처리...
    }
}
```

이 예에서 알 수 있듯이, [Eloquent 모델](/docs/{{version}}/eloquent)을 잡 생성자에 직접 넘길 수 있으며, `SerializesModels` 트레이트 덕분에 연관된 관계까지 적절히 직렬화/비직렬화됩니다. 실제 큐 처리 시 데이터베이스에서 모델 전체가 재조회됩니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드 의존성 주입

`handle` 메서드는 큐 처리 시점에 호출됩니다. 이때 의존성을 타입힌트로 명시하면, Laravel의 [서비스 컨테이너](/docs/{{version}}/container)가 의존 객체를 자동 주입합니다.

컨테이너의 의존성 주입을 커스터마이즈하려면 `bindMethod`를 [서비스 프로바이더](/docs/{{version}}/providers)에서 사용할 수 있습니다.

> {note} 이진 데이터(예: 원시 이미지 등)는 반드시 `base64_encode`를 거쳐 처리해야 합니다. 그렇지 않으면 JSON 직렬화에 실패할 수 있습니다.

<a name="handling-relationships"></a>
#### 큐 모델 관계 다루기

모델의 관계까지 모두 직렬화할 경우 잡 페이로드가 너무 커질 수 있습니다. 이때는 모델로부터 `withoutRelations`를 호출해 관계 정보를 제거하고 잡 속성에 할당하세요.

```php
public function __construct(Podcast $podcast)
{
    $this->podcast = $podcast->withoutRelations();
}
```

또한 잡 처리 시 데이터베이스에서 관계 전체를 새로 조회한다는 점을 기억해야 하며, 직렬화 전에 지정한 필터는 재적용되지 않습니다.

<a name="unique-jobs"></a>
### 유니크 잡

> {note} 유니크 잡 기능은 [락 지원 캐시 드라이버](/docs/{{version}}/cache#atomic-locks)가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 드라이버만 지원합니다. 배치 내부 잡에는 적용되지 않습니다.

특정 잡이 큐에 오직 하나만 존재하도록 하려면 `ShouldBeUnique` 인터페이스를 잡 클래스에 구현합니다.

```php
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```

기본적으로 잡 클래스에 추가 메서드가 필요 없지만, 유니크 기준 키나 유효 시간 등을 지정할 수 있습니다.

```php
class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    public $product;
    public $uniqueFor = 3600;

    public function uniqueId()
    {
        return $this->product->id;
    }
}
```

동일 product ID에 대해 잡이 이미 큐에 있으면, 새로 디스패치해도 무시됩니다. 기존 잡이 1시간 안에 처리되지 않으면 락이 해제되어 다시 등록할 수 있습니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 처리 시작 직전까지 유니크 락 유지

기본적으로 유니크 잡은 처리 완료 또는 최대 재시도 도달 시 락이 해제됩니다. 처리 시작 직전에만 락을 해제하려면 `ShouldBeUniqueUntilProcessing`을 구현하세요.

```php
class UpdateSearchIndex implements ShouldQueue, ShouldBeUniqueUntilProcessing
{
    // ...
}
```

<a name="unique-job-locks"></a>
#### 유니크 잡 락

실제로 `ShouldBeUnique` 잡이 디스패치될 때, Laravel은 [락](/docs/{{version}}/cache#atomic-locks) 취득을 시도합니다. 락 미취득 시 잡은 디스패치되지 않습니다. 락은 처리 완료 또는 모든 재시도 실패 시 해제됩니다. 기본 캐시 드라이버가 사용되며, 이를 변경하려면 `uniqueVia` 메서드를 추가하세요.

```php
use Illuminate\Support\Facades\Cache;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    public function uniqueVia()
    {
        return Cache::driver('redis');
    }
}
```

> {tip} 동시에 여러 잡의 중복 처리를 제한하고 싶다면 [`WithoutOverlapping`](/docs/{{version}}/queues#preventing-job-overlaps) 미들웨어를 사용하세요.

<a name="job-middleware"></a>
## 잡 미들웨어

잡 미들웨어는 큐 잡 실행 전후에 커스텀 로직을 래핑할 수 있도록 도와줍니다. 예를 들어, Redis 기반 속도 제한을 모든 잡마다 직접 작성하지 않고 미들웨어로 추출할 수 있습니다.

```php
use Illuminate\Support\Facades\Redis;

public function handle()
{
    Redis::throttle('key')->block(0)->allow(1)->every(5)->then(function () {
        info('Lock obtained...');
        // 잡 처리...
    }, function () {
        // 락 획득 불가 시
        return $this->release(5);
    });
}
```

위 코드처럼 핸들러가 복잡해지는 것을 방지하기 위해 미들웨어를 별도로 분리할 수 있습니다.

```php
namespace App\Jobs\Middleware;

use Illuminate\Support\Facades\Redis;

class RateLimited
{
    public function handle($job, $next)
    {
        Redis::throttle('key')
             ->block(0)->allow(1)->every(5)
             ->then(function () use ($job, $next) {
                $next($job);
             }, function () use ($job) {
                $job->release(5);
             });
    }
}
```

잡 클래스에 `middleware` 메서드를 추가하여 위 미들웨어를 지정할 수 있습니다.

```php
use App\Jobs\Middleware\RateLimited;

public function middleware()
{
    return [new RateLimited];
}
```

> {tip} 잡 미들웨어는 큐잉되는 이벤트 리스너, 메일러블, 알림에도 적용할 수 있습니다.

<a name="rate-limiting"></a>
### 속도 제한

Laravel은 자체 미들웨어로도 잡 속도 제한을 지원합니다. 예를 들어, 일반 사용자는 데이터 백업 잡을 1시간에 1번쯤만 허용하고, 프리미엄 고객은 무제한 허용한다면 다음처럼 구현할 수 있습니다.

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Support\Facades\RateLimiter;

public function boot()
{
    RateLimiter::for('backups', function ($job) {
        return $job->user->vipCustomer()
            ? Limit::none()
            : Limit::perHour(1)->by($job->user->id);
    });
}
```

정의한 레이트 리미터를 잡에 붙이려면, 다음과 같이 미들웨어를 지정합니다.

```php
use Illuminate\Queue\Middleware\RateLimited;

public function middleware()
{
    return [new RateLimited('backups')];
}
```

잡이 제한에 걸린 경우, 재시도 횟수(`attempts`)는 계속 증가합니다. 반복 시도 제한이나 기간을 조정해야 한다면 [`retryUntil` 메서드](#time-based-attempts)를 사용하세요.

더 이상 재시도하지 않고 잡을 바로 취소하려면 `dontRelease`를 사용합니다.

```php
public function middleware()
{
    return [(new RateLimited('backups'))->dontRelease()];
}
```

> {tip} Redis 사용 시 더 효율적인 `RateLimitedWithRedis` 미들웨어를 사용할 수 있습니다.

<a name="preventing-job-overlaps"></a>
### 잡 중복 실행 방지

`Illuminate\Queue\Middleware\WithoutOverlapping`는 지정한 키에 대해 잡의 동시 실행을 방지합니다. 예: 같은 유저 ID로 크레딧 점수 업데이트 잡을 동시 처리하지 않으려면 다음처럼 지정합니다.

```php
use Illuminate\Queue\Middleware\WithoutOverlapping;

public function middleware()
{
    return [new WithoutOverlapping($this->user->id)];
}
```

겹치는 잡은 큐로 되돌려(릴리즈)줍니다. 지연 시간(초) 지정은 다음과 같습니다.

```php
public function middleware()
{
    return [(new WithoutOverlapping($this->order->id))->releaseAfter(60)];
}
```

겹치는 잡을 아예 재시도하지 않고 삭제하려면 `dontRelease`를 사용하세요.

락이 예상치 못하게 해제되지 않을 경우를 대비해, `expireAfter`로 제한 시간(초)을 지정할 수 있습니다.

```php
public function middleware()
{
    return [(new WithoutOverlapping($this->order->id))->expireAfter(180)];
}
```

> {note} 이 미들웨어는 락 지원 캐시 드라이버가 필요합니다. (`memcached`, `redis`, `dynamodb`, `database`, `file`, `array`)

<a name="throttling-exceptions"></a>
### 예외 트래핑/지연

`Illuminate\Queue\Middleware\ThrottlesExceptions`는 일정 횟수 이상 예외 발생 시 잡을 지연시키는 미들웨어입니다. 외부 서비스 등 불안정한 API 연동 시 유용합니다.

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

public function middleware()
{
    return [new ThrottlesExceptions(10, 5)];
}

public function retryUntil()
{
    return now()->addMinutes(5);
}
```

위 예제에서, 잡이 5분간 10번 예외를 던지면 5분 후 재시도됩니다. 추가로 `backoff`로 재시도 간격을 지정할 수 있고, 여러 잡이 동일한 키로 동작하도록 `by`를 쓸 수 있습니다.

> {tip} Redis 사용 시 `ThrottlesExceptionsWithRedis` 미들웨어가 더 효율적입니다.

<a name="dispatching-jobs"></a>
## 잡 디스패치(실행)하기

작성한 잡 클래스는 `dispatch` 메서드로 디스패치할 수 있습니다. 생성자 인자는 그대로 전달됩니다.

```php
ProcessPodcast::dispatch($podcast);
```

조건부로 디스패치하고 싶다면:

```php
ProcessPodcast::dispatchIf($accountActive, $podcast);

ProcessPodcast::dispatchUnless($accountSuspended, $podcast);
```

<a name="delayed-dispatching"></a>
### 지연 디스패치

지연 작업이 필요하다면 `delay` 메서드를 체이닝하여, 지정 시점 이후에만 처리 가능하게 할 수 있습니다.

```php
ProcessPodcast::dispatch($podcast)->delay(now()->addMinutes(10));
```

> {note} Amazon SQS는 지연 시간이 최대 15분입니다.

<a name="dispatching-after-the-response-is-sent-to-browser"></a>
#### 브라우저 응답 이후 디스패치

`dispatchAfterResponse`를 사용하면, HTTP 응답이 브라우저로 전송된 뒤 잡이 디스패치됩니다. 이 방식은 이메일 전송 등 약 1초 내외의 짧은 작업에 적합합니다. 이때는 워커가 필요 없습니다.

```php
SendNotification::dispatchAfterResponse();
```

클로저도 마찬가지로 사용할 수 있습니다.

```php
dispatch(function () {
    Mail::to('taylor@example.com')->send(new WelcomeMessage);
})->afterResponse();
```

<a name="synchronous-dispatching"></a>
### 동기식 디스패치

잡을 바로(동기적으로) 실행하려면 `dispatchSync`를 사용하세요. 이 경우 큐에 잡이 쌓이지 않고 즉시 실행됩니다.

```php
ProcessPodcast::dispatchSync($podcast);
```

<a name="jobs-and-database-transactions"></a>
### 잡과 데이터베이스 트랜잭션

트랜잭션 내에서 잡을 디스패치할 경우, 아직 커밋이 안 된 상태에서 잡이 처리될 가능성에 주의하세요. 이로 인해 변경된 데이터가 실제 DB에 반영되지 않아 잡이 실패할 수 있습니다.

해결 방법으로는, 큐 커넥션 설정에서 `after_commit` 옵션을 true로 두는 것입니다.

```php
'redis' => [
    'driver' => 'redis',
    // ...
    'after_commit' => true,
],
```

또는 개별 잡에 대해 `afterCommit`/`beforeCommit` 메서드를 체이닝할 수도 있습니다.

```php
ProcessPodcast::dispatch($podcast)->afterCommit();
ProcessPodcast::dispatch($podcast)->beforeCommit();
```

> {tip} 이 옵션 활성화 시 모든 이벤트 리스너, 메일, 알림, 브로드캐스트도 트랜잭션 커밋 후에만 디스패치됩니다.

<a name="job-chaining"></a>
### 잡 체이닝

여러 잡을 순차적으로 실행하고 싶을 때 `Bus::chain` 메서드를 사용하면 됩니다. 앞 잡이 실패하면 다음 잡은 실행되지 않습니다.

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

클로저도 포함할 수 있습니다.

```php
Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    function () {
        Podcast::update(...);
    },
])->dispatch();
```

> {note} `$this->delete()`로 잡을 삭제해도, 잡 체인이 중단되지 않습니다. 체인 내 잡이 실패해야 실행이 멈춥니다.

#### 체인 커넥션/큐 지정

체인에 사용할 커넥션 및 큐를 지정하려면 `onConnection`, `onQueue`를 사용할 수 있습니다.

```php
Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->onConnection('redis')->onQueue('podcasts')->dispatch();
```

#### 체인 실패 처리

체인 중 하나라도 실패 시 실행할 콜백을 지정하려면 `catch` 메서드를 사용하세요.

```php
Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->catch(function (Throwable $e) {
    // 체인 내 잡이 하나라도 실패하면 실행
})->dispatch();
```

<a name="customizing-the-queue-and-connection"></a>
### 큐/커넥션 커스터마이징

#### 특정 큐로 디스패치

잡을 특정 큐로 나누어 넣으면 워커의 분배, 잡 우선순위 관리가 용이합니다. 큐는 커넥션 내부의 큐 이름입니다.

```php
ProcessPodcast::dispatch($podcast)->onQueue('processing');
```

잡 클래스 내부 생성자에서 `onQueue`를 호출하여도 됩니다.

#### 특정 커넥션으로 디스패치

여러 큐 커넥션을 사용할 경우 `onConnection`으로 명시할 수 있습니다.

```php
ProcessPodcast::dispatch($podcast)->onConnection('sqs');
```

커넥션과 큐를 함께 지정하려면 체이닝하세요.

```php
ProcessPodcast::dispatch($podcast)
  ->onConnection('sqs')
  ->onQueue('processing');
```

클래스 생성자에서도 `onConnection` 호출 가능.

<a name="max-job-attempts-and-timeout"></a>
### 최대 시도 횟수 및 타임아웃 값 지정

#### 최대 시도 횟수

잡이 무한히 재시도되는 것을 막기 위해 다양한 제한 방법을 지원합니다.

- Artisan 커맨드에 `--tries` 옵션 추가 시 워커 공통 적용:

  ```
  php artisan queue:work --tries=3
  ```

- 잡 클래스에 `$tries` 속성 지정(워크 커맨드보다 우선):

  ```php
  public $tries = 5;
  ```

#### 시간 기반 시도

정해진 시간 내에만 잡을 재시도하게 하려면 `retryUntil` 메서드를 추가하세요.

```php
public function retryUntil()
{
    return now()->addMinutes(10);
}
```

> {tip} 이벤트 리스너에서도 `tries`/`retryUntil` 사용 가능.

#### 최대 예외 수

많은 시도를 허용하되, 미처리된 예외가 특정 횟수 이상 발생하면 실패 처리하고 싶을 때:

```php
public $tries = 25;
public $maxExceptions = 3;
```

#### 타임아웃

> {note} 잡 타임아웃 지정에는 `pcntl` PHP 확장 설치 필요.

`--timeout` 옵션 또는 잡 클래스의 `$timeout` 속성으로 지정.

```
php artisan queue:work --timeout=30
```

```php
public $timeout = 120;
```

외부 서비스 연동 시(예: Guzzle) 해당 API에서도 별도로 타임아웃 지정이 권장됩니다.

#### 타임아웃 시 실패 처리

잡이 타임아웃시 실패로 간주하려면 `$failOnTimeout` 속성을 true로 두세요.

```php
public $failOnTimeout = true;
```

<a name="error-handling"></a>
### 에러 처리

잡 실행 중 예외 발생 시 자동으로 큐에 재등록(release)되며, 최대 시도 횟수까지 반복됩니다.

#### 수동 릴리즈

특정 상황에서 직접 잡을 큐에 다시 넣으려면 `release()` 호출:

```php
$this->release();
$this->release(10); // 10초 후
```

#### 수동 실패처리

잡을 강제로 실패시키려고 하면 `fail()` 메서드 사용:

```php
$this->fail();
$this->fail($exception);
```

> {tip} 실패 잡 관련 자세한 내용은 [아래 문서](#dealing-with-failed-jobs) 참고.

<a name="job-batching"></a>
## 배치 잡 실행

Laravel 배치 기능은 잡 세트를 일괄 처리하고, 완료 후 후속 작업을 쉽게 처리할 수 있도록 합니다. 사용 전, 메타 정보를 담는 테이블을 만들기 위한 마이그레이션을 생성하세요.

```
php artisan queue:batches-table
php artisan migrate
```

### 배치 잡 정의

평소처럼 [큐 잡]을 생성하지만, `Illuminate\Bus\Batchable` 트레이트를 추가합니다. 이로써 자신이 포함된 배치 정보를 얻을 수 있습니다.

```php
use Illuminate\Bus\Batchable;

class ImportCsv implements ShouldQueue
{
    use Batchable, Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public function handle()
    {
        if ($this->batch()->cancelled()) {
            return;
        }
        // CSV 파일 일부 처리...
    }
}
```

### 배치 디스패치

`Bus::batch`로 여러 잡을 배치로 디스패치할 수 있습니다. 완료, 실패, 최종 콜백을 쉽게 지정할 수 있습니다.

```php
$batch = Bus::batch([
    new ImportCsv(1, 100),
    ...
])->then(function (Batch $batch) {
    // 모든 잡이 성공적으로 완료됨
})->catch(function (Batch $batch, Throwable $e) {
    // 첫 실패 감지
})->finally(function (Batch $batch) {
    // 배치 실행 완료
})->dispatch();

return $batch->id;
```

> {note} 배치 콜백 내부에서 `$this` 변수 사용을 피하세요.

#### 배치 이름 지정

배치에 이름을 지정하면 Horizon, Telescope 등에서 가독성이 향상됩니다.

```php
$batch = Bus::batch([...])->name('Import CSV')->dispatch();
```

#### 배치 커넥션/큐 지정

모든 배치 잡은 같은 커넥션/큐로 실행되어야 하며, `onConnection`, `onQueue`로 지정 가능합니다.

#### 배치 내 체인

배치 내부에서도 [잡 체이닝](#job-chaining)처럼 배열로 정의해 병렬 처리가 가능합니다.

#### 배치에 잡 추가

잡 내부에서 배치에 잡을 동적으로 추가하려면 `add` 메서드 사용.

```php
$this->batch()->add(Collection::times(1000, function () {
    return new ImportContacts;
}));
```

> {note} 반드시 같은 배치의 잡 안에서만 추가 가능합니다.

### 배치 조회

`Batch` 인스턴스에는 총 잡 수, 대기/실패/완료 수, 진행률, 취소 여부 등 다양한 속성이 있습니다.

### 라우트에서 배치 반환

`Bus::findBatch`로 배치 ID로 배치 정보를 API 등에서 JSON으로 반환할 수 있습니다.

```php
Route::get('/batch/{batchId}', function (string $batchId) {
    return Bus::findBatch($batchId);
});
```

### 배치 취소

잡 실행 도중에 배치를 취소하려면 `cancel()`을 부르세요. 대개 `handle`의 초반에 `cancelled()` 체크와 함께 사용합니다.

### 배치 실패

배치 잡 중 하나라도 실패하면, 등록된 `catch` 콜백이 호출됩니다(오직 최초 1회).

#### 실패 허용

기본적으로 잡이 실패하면 배치 전체가 취소되는데, `allowFailures`로 이 동작을 비활성화할 수 있습니다.

```php
$batch = Bus::batch([...])->allowFailures()->dispatch();
```

#### 실패 잡 재시도

`queue:retry-batch` 명령어로 전체 실패 잡을 재시도 가능합니다.

```
php artisan queue:retry-batch 32dbc76c-4f82-4749-b610-a639fe0099b5
```

### 배치 데이터 정리(Pruning)

`job_batches` 테이블에 배치 레코드가 누적될 수 있으므로, `queue:prune-batches` 명령을 [일정 등록 작업](/docs/{{version}}/scheduling)으로 매일 실행하는 것이 권장됩니다.

```php
$schedule->command('queue:prune-batches')->daily();
```

기본으로는 24시간 이상 지난 배치가 대상이며, 옵션으로 기간 조정이 가능합니다.

```php
$schedule->command('queue:prune-batches --hours=48')->daily();
$schedule->command('queue:prune-batches --hours=48 --unfinished=72')->daily();
```

<a name="queueing-closures"></a>
## 클로저 큐잉

잡 클래스 대신 클로저도 큐에 디스패치할 수 있습니다. 클로저 코드는 안전하게 서명되어 전송됩니다.

```php
$podcast = App\Podcast::find(1);

dispatch(function () use ($podcast) {
    $podcast->publish();
});
```

`catch` 메서드 체이닝으로 실패 처리도 가능합니다.

```php
dispatch(function () use ($podcast) {
    $podcast->publish();
})->catch(function (Throwable $e) {
    // 이 잡은 실패함...
});
```

<a name="running-the-queue-worker"></a>
## 큐 워커 실행

<a name="the-queue-work-command"></a>
### `queue:work` 명령어

아래 명령어로 큐 워커를 실행할 수 있습니다.

```
php artisan queue:work
```

> {tip} 워커 프로세스를 영구 실행하고 싶으면 [Supervisor](#supervisor-configuration) 같은 프로세스 모니터를 활용하세요.

해당 프로세스는 꺼지지 않으므로, 코드가 바뀌더라도 자동 인식하지 못합니다. 배포 시에는 반드시 [워커를 재시작](#queue-workers-and-deployment)해야 합니다.

`queue:listen` 명령은 실시간 코드 반영에 유리하지만, 퍼포먼스가 떨어집니다.

```
php artisan queue:listen
```

#### 다중 워커 실행

여러 잡을 병렬 처리하려면 워커를 여러 개 실행하세요. Supervisor 프로세스 매니저에서 `numprocs`로 제어할 수 있습니다.

#### 커넥션/큐 지정

특정 커넥션, 큐만 처리하려면 다음처럼 실행합니다.

```
php artisan queue:work redis --queue=emails
```

#### 정해진 개수의 잡만 처리

`--once` 또는 `--max-jobs` 옵션으로 1회/지정 횟수까지만 잡을 처리하게 할 수 있습니다.

```
php artisan queue:work --once
php artisan queue:work --max-jobs=1000
```

#### 큐가 빌 때까지 처리 후 종료

`--stop-when-empty`로 모든 잡을 처리하고 자동 종료시킬 수 있어, Docker 등의 컨테이너 환경에서 유용합니다.

```
php artisan queue:work --stop-when-empty
```

#### 지정 시간만 처리

`--max-time`으로 주어진 시간만큼만 처리한 후 자동종료되게 할 수 있습니다.

```
php artisan queue:work --max-time=3600   // 1시간 후 종료
```

#### 워커 슬립(대기) 설정

예약된 잡이 없을 때 워커가 얼마나 대기할지 `--sleep`으로 지정합니다.

```
php artisan queue:work --sleep=3
```

#### 리소스 관리

데몬 워커는 각 잡이 끝나도 프레임워크를 재시작(재부팅)하지 않으므로, 무거운 리소스는 미리 반납하세요.

<a name="queue-priorities"></a>
### 큐 우선순위

여러 큐 우선순위를 지원합니다. 예를 들어, `redis`의 기본 큐를 `low`로, 긴급 잡은 `high`로 디스패치했다면:

```
dispatch((new Job)->onQueue('high'));

// 워커는 high가 비거나 없으면 low의 잡을 처리
php artisan queue:work --queue=high,low
```

<a name="queue-workers-and-deployment"></a>
### 큐 워커와 배포

워커는 장시간 실행되므로 배포 후 반드시 재시작해야 합니다.

```
php artisan queue:restart
```

이 명령은 현재 처리 중인 잡까지 마친 후 워커를 안전하게 종료시킵니다. Supervisor를 통해 자동재시작을 권장합니다.

> {tip} 큐는 [캐시](/docs/{{version}}/cache)를 통해 재시작 신호를 관리하므로, 캐시 드라이버 설정이 필요합니다.

<a name="job-expirations-and-timeouts"></a>
### 잡 만료 및 타임아웃

#### 잡 만료

각 큐 커넥션에는 `retry_after` 옵션이 있으며, 지정한 시간(초) 동안 잡 처리가 안되면 큐에 다시 올라갑니다. 이 값을 적절하게 잡아야 동시 중복 처리/유실이 발생하지 않습니다.

> {note} Amazon SQS 커넥션엔 `retry_after`가 없고, [기본 Visibility Timeout](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/AboutVT.html)으로 관리합니다.

#### 워커 타임아웃

`queue:work` 명령줄의 `--timeout` 옵션은 특정 시간이 지나면 워커를 종료시킵니다. 이와 `retry_after` 값은 다르지만 서로 연동하여, 잡이 유실되거나 중복 처리되는 일을 막습니다.

> {note} `--timeout` 값은 `retry_after`보다 반드시 수 초 정도 더 짧아야 합니다.

<a name="supervisor-configuration"></a>
## Supervisor 설정

프로덕션 환경에서는 워커 프로세스가 중단될 경우를 대비해, 자동 재시작이 가능한 프로세스 모니터가 필요합니다. Supervisor는 Linux에서 널리 쓰이는 프로세스 모니터입니다.

#### Supervisor 설치

Ubuntu에서 Supervisor를 설치하려면:

```
sudo apt-get install supervisor
```

> {tip} Supervisor 설치/관리가 번거롭다면 [Laravel Forge](https://forge.laravel.com)에서 자동 설치/설정을 지원합니다.

#### Supervisor 설정

Supervisor 설정 파일은 `/etc/supervisor/conf.d`에 두고, 예를 들어 `laravel-worker.conf` 파일로 프로세스를 관리합니다.

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

> {note} `stopwaitsecs` 값은 가장 오래 걸리는 잡 처리 시간보다 충분히 크게 설정해야 합니다.

#### Supervisor 시작

설정 완료 후 다음 명령어로 Supervisor를 적용 및 시작합니다.

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start laravel-worker:*
```

자세한 내용은 [Supervisor 공식문서](http://supervisord.org/index.html)를 참고하세요.

<a name="dealing-with-failed-jobs"></a>
## 실패한 잡 처리

잡이 반복해서 실패하면, 재시도 횟수 초과 후 `failed_jobs` 테이블에 기록됩니다. 테이블 생성이 필요하다면:

```
php artisan queue:failed-table
php artisan migrate
```

워커 실행 시, 최대 시도 횟수는 `--tries` 옵션(또는 잡 클래스의 `$tries` 프로퍼티)로 조정할 수 있습니다.

```
php artisan queue:work redis --tries=3
```

`--backoff` 옵션을 사용하면 실패 재시도 간격(초)을 지정할 수 있습니다.

```
php artisan queue:work redis --tries=3 --backoff=3
```

잡 클래스별로 `$backoff` 프로퍼티나 `backoff()` 메서드로 세밀하게 지정할 수 있습니다.

```php
public $backoff = 3;

public function backoff() {
    return 3;
}

public function backoff() {
    return [1, 5, 10]; // 첫 재시도 1초, 두 번째 5초, 세 번째 10초
}
```

### 실패한 잡 후처리

잡이 실패했을 때 사용자 알림 발송, 롤백 등을 원한다면, 잡 클래스에 `failed` 메서드를 정의합니다.

```php
public function failed(Throwable $exception)
{
    // 예: 실패 알림 발송 등
}
```

> {note} `failed` 메서드 호출 전 새로운 잡 인스턴스가 생성되므로, `handle`에서 변경한 속성 값은 초기화됩니다.

### 실패 잡 재시도

실패 잡 목록 조회:

```
php artisan queue:failed
```

실패 잡(예: ID가 `ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece`) 재시도:

```
php artisan queue:retry ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece
```

여러 개/전체 재시도 및 삭제도 지원합니다.

> {tip} [Horizon](/docs/{{version}}/horizon) 사용 시, `horizon:forget` 명령으로 삭제하세요.

### 존재하지 않는 모델 무시

Eloquent 모델이 큐에 직렬화된 후 삭제된 경우, `deleteWhenMissingModels` 속성이 true면 자동으로 해당 잡을 삭제(예외 없이)합니다.

```php
public $deleteWhenMissingModels = true;
```

### 실패 잡 데이터 정리

모든 실패 잡 삭제:

```
php artisan queue:prune-failed
```

특정 시간(예: 48시간)이 지난 실패 잡만 삭제:

```
php artisan queue:prune-failed --hours=48
```

### DynamoDB에 실패 잡 저장

`failed_jobs` 테이블을 DynamoDB에 둘 수 있습니다. 관련 AWS SDK를 설치하고, 환경 변수로 AWS 자격정보를 세팅하면 됩니다.

```php
'failed' => [
    'driver' => env('QUEUE_FAILED_DRIVER', 'dynamodb'),
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'table' => 'failed_jobs',
],
```

### 실패 잡 저장 비활성화

실패 잡을 저장하지 않으려면, 드라이버를 `null`로 지정하세요.

```
QUEUE_FAILED_DRIVER=null
```

### 실패 잡 이벤트

잡 실패 시, 이벤트 리스너(예: 알림)를 등록하려면 `Queue::failing`으로 설정 가능합니다.

```php
Queue::failing(function (JobFailed $event) {
    // $event->connectionName
    // $event->job
    // $event->exception
});
```

<a name="clearing-jobs-from-queues"></a>
## 큐에 있는 잡 전체 삭제

> {tip} [Horizon](/docs/{{version}}/horizon) 사용 시, `horizon:clear` 명령을 쓰세요.

특정 큐/커넥션에서 잡 전체 삭제:

```
php artisan queue:clear redis --queue=emails
```

> {note} 지원 드라이버: SQS, Redis, Database. SQS는 삭제에 최대 60초 소요되고, 새로 전송된 잡이 삭제될 수 있습니다.

<a name="monitoring-your-queues"></a>
## 큐 모니터링

큐에 잡이 몰려 처리 지연이 생길 위험이 있다면, Laravel이 임계값 초과시 알림이 가능하도록 지원합니다.

먼저 `queue:monitor` 명령을 [매분 실행](/docs/{{version}}/scheduling)하도록 예약하세요.

```
php artisan queue:monitor redis:default,redis:deployments --max=100
```

잡 개수가 임계값을 넘으면 `Illuminate\Queue\Events\QueueBusy` 이벤트가 발생합니다. 이벤트 리스너에서 Slack, 메일 등 알림을 발송하면 됩니다.

```php
Event::listen(function (QueueBusy $event) {
    Notification::route('mail', 'dev@example.com')
        ->notify(new QueueHasLongWaitTime(
            $event->connection,
            $event->queue,
            $event->size
        ));
});
```

<a name="job-events"></a>
## 잡 이벤트

`Queue` [파사드](/docs/{{version}}/facades)의 `before`/`after` 메서드로, 잡 처리 전후에 콜백을 지정할 수 있습니다(로그, 통계용 등). 주로 서비스 프로바이더의 `boot`에서 호출합니다.

```php
Queue::before(function (JobProcessing $event) {
    // $event->connectionName
    // $event->job
    // $event->job->payload()
});

Queue::after(function (JobProcessed $event) {
    // ...
});
```

`looping` 메서드로는, 워커가 큐에서 잡을 꺼내기 전 매번 수행할 콜백을 등록할 수 있습니다.

```php
Queue::looping(function () {
    while (DB::transactionLevel() > 0) {
        DB::rollBack();
    }
});
```

---