# 큐 (Queues)

- [소개](#introduction)
    - [커넥션과 큐의 차이](#connections-vs-queues)
    - [드라이버별 참고사항 및 사전 준비](#driver-prerequisites)
- [잡 생성](#creating-jobs)
    - [잡 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [유니크 잡](#unique-jobs)
    - [암호화된 잡](#encrypted-jobs)
- [잡 미들웨어](#job-middleware)
    - [속도 제한](#rate-limiting)
    - [잡 중복 실행 방지](#preventing-job-overlaps)
    - [예외 제한(Throttle) 처리](#throttling-exceptions)
    - [잡 건너뛰기](#skipping-jobs)
- [잡 디스패치](#dispatching-jobs)
    - [지연 디스패치](#delayed-dispatching)
    - [동기식 디스패치](#synchronous-dispatching)
    - [잡과 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [잡 체이닝](#job-chaining)
    - [큐와 커넥션 커스터마이징](#customizing-the-queue-and-connection)
    - [최대 시도 횟수/타임아웃 값 지정](#max-job-attempts-and-timeout)
    - [에러 처리](#error-handling)
- [잡 배치 처리](#job-batching)
    - [배치 가능한 잡 정의](#defining-batchable-jobs)
    - [배치 디스패치](#dispatching-batches)
    - [체인과 배치](#chains-and-batches)
    - [배치에 잡 추가](#adding-jobs-to-batches)
    - [배치 상태 조회](#inspecting-batches)
    - [배치 취소](#cancelling-batches)
    - [배치 실패 처리](#batch-failures)
    - [배치 레코드 정리(Prune)](#pruning-batches)
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
    - [실패한 잡 레코드 정리](#pruning-failed-jobs)
    - [DynamoDB에 실패한 잡 저장](#storing-failed-jobs-in-dynamodb)
    - [실패한 잡 저장 비활성화](#disabling-failed-job-storage)
    - [실패한 잡 이벤트](#failed-job-events)
- [큐에서 잡 비우기](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [일부 잡만 페이크 처리](#faking-a-subset-of-jobs)
    - [잡 체인 테스트](#testing-job-chains)
    - [잡 배치 테스트](#testing-job-batches)
    - [잡/큐 상호작용 테스트](#testing-job-queue-interactions)
- [잡 이벤트](#job-events)

<a name="introduction"></a>
## 소개 (Introduction)

웹 애플리케이션을 개발하는 과정에서, 업로드된 CSV 파일을 파싱하고 저장하는 작업과 같이 일반적인 웹 요청 중에 처리하기에는 시간이 너무 오래 걸리는 작업이 있을 수 있습니다. 다행히도 Laravel은 백그라운드에서 처리할 수 있는 큐 잡(queued job)을 손쉽게 만들 수 있도록 지원합니다. 시간 소모가 큰 작업을 큐로 분리하여 처리함으로써, 애플리케이션은 웹 요청에 훨씬 빠르게 응답할 수 있고 사용자 경험이 크게 향상됩니다.

Laravel 큐는 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 관계형 데이터베이스 등 다양한 큐 백엔드를 아우르는 통합 API를 제공합니다.

큐 관련 모든 설정 값은 애플리케이션의 `config/queue.php` 설정 파일에 저장됩니다. 이 파일에는 데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 등 프레임워크에 포함된 각 큐 드라이버에 대한 커넥션 설정이 정의되어 있습니다. 또한, 잡을 즉시 실행하는 동기식(synchronous) 드라이버(로컬 개발용)와 큐잉된 잡을 모두 폐기하는 `null` 드라이버도 포함되어 있습니다.

> [!NOTE]
> Laravel은 Redis 기반 큐를 위한 Horizon이라는 멋진 대시보드 및 관리 시스템을 제공합니다. 자세한 내용은 [Horizon 문서](/docs/12.x/horizon)를 참고하세요.

<a name="connections-vs-queues"></a>
### 커넥션과 큐의 차이

Laravel 큐를 시작하기 전에, "커넥션(connection)"과 "큐(queue)"의 차이를 이해하는 것이 중요합니다. `config/queue.php`에는 `connections`라는 설정 배열이 있는데, 이 옵션은 Amazon SQS, Beanstalk, Redis 등 백엔드 큐 서비스에 대한 커넥션을 정의합니다. 하나의 큐 커넥션은 여러 "큐"를 가질 수 있으며, 각각을 잡이 쌓이는 별도의 스택으로 생각할 수 있습니다.

각 커넥션 설정 예시에는 `queue` 속성이 있는데, 이 속성은 해당 커넥션에서 잡을 보낼 때 기본적으로 사용되는 큐 이름을 지정합니다. 즉, 잡을 보낼 때 어떤 큐로 보낼지 명시하지 않으면, 커넥션 설정에 지정된 `queue` 속성의 큐에 잡이 쌓이게 됩니다:

```php
use App\Jobs\ProcessPodcast;

// 이 잡은 기본 커넥션의 기본 큐에 전송됩니다...
ProcessPodcast::dispatch();

// 이 잡은 기본 커넥션의 "emails" 큐에 전송됩니다...
ProcessPodcast::dispatch()->onQueue('emails');
```

단일 큐만 사용해도 충분한 애플리케이션도 있지만, 여러 큐에 잡을 전송하면 작업의 우선순위 또는 분류에 따라 동작을 나눌 수 있어 특히 유용합니다. Laravel 큐 워커는 처리할 큐의 우선순위를 지정할 수 있으므로, 예를 들어 `high` 큐로 잡을 보내고, 해당 큐에 더 높은 우선순위를 부여해 워커를 실행할 수 있습니다:

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버별 참고사항 및 사전 준비

<a name="database"></a>
#### 데이터베이스

`database` 큐 드라이버를 사용하려면, 잡을 저장할 데이터베이스 테이블이 필요합니다. 일반적으로 Laravel의 기본 `0001_01_01_000002_create_jobs_table.php` [마이그레이션](/docs/12.x/migrations)에 포함되어 있습니다. 만약 이 마이그레이션이 없다면, `make:queue-table` Artisan 명령어를 사용해 생성할 수 있습니다:

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면, `config/database.php`에서 Redis 데이터베이스 커넥션을 구성해야 합니다.

> [!WARNING]
> `redis` 큐 드라이버는 Redis의 `serializer` 및 `compression` 옵션을 지원하지 않습니다.

**Redis 클러스터**

Redis 큐 커넥션에서 [Redis 클러스터](https://redis.io/docs/latest/operate/rs/databases/durability-ha/clustering)를 사용하는 경우, 반드시 큐 이름에 [키 해시 태그](https://redis.io/docs/latest/develop/using-commands/keyspace/#hashtags)를 포함해야 합니다. 이는 특정 큐의 모든 Redis 키가 같은 해시 슬롯에 할당되도록 하기 위함입니다:

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

Redis 큐를 사용할 때는 `block_for` 설정으로, 잡이 큐에 도착할 때까지 드라이버가 대기해야 하는 시간을 초 단위로 지정할 수 있습니다. 이 값을 적절히 조정하면 매번 Redis를 폴링하지 않아도 되어 효율적입니다. 예를 들어, `block_for`를 `5`로 설정하면, 잡이 도착할 때까지 최대 5초간 대기합니다:

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
> `block_for`를 `0`으로 설정하면 잡이 도착할 때까지 무한정 대기하게 됩니다. 이 경우, `SIGTERM`과 같은 신호도 다음 잡이 처리될 때까지 반영되지 않을 수 있으니 유의하세요.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 사전 준비

아래 큐 드라이버를 사용할 때는 해당 의존성을 Composer 패키지로 설치해야 합니다:

<div class="content-list" markdown="1">

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~2.0` 또는 phpredis PHP 확장(extension)
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`

</div>

(이후의 본문은 지침에 따라 코드 블록 외 내용을 계속해서 한국어로 번역합니다. 추가 답변을 원하실 경우 이어서 입력해 주세요.)