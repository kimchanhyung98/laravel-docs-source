아래는 요청하신 마크다운 문서의 한글 번역본입니다.

---

# 큐(Queues)

- [소개](#introduction)
    - [커넥션 vs. 큐](#connections-vs-queues)
    - [드라이버 참고 사항 및 사전 준비 사항](#driver-prerequisites)
- [잡 생성하기](#creating-jobs)
    - [잡 클래스 생성](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [고유 잡(Unique Jobs)](#unique-jobs)
    - [암호화된 잡(Encrypted Jobs)](#encrypted-jobs)
- [잡 미들웨어](#job-middleware)
    - [속도 제한(Rate Limiting)](#rate-limiting)
    - [잡 중복 방지](#preventing-job-overlaps)
    - [예외 한도 제한](#throttling-exceptions)
    - [잡 건너뛰기](#skipping-jobs)
- [잡 디스패치](#dispatching-jobs)
    - [지연 디스패치](#delayed-dispatching)
    - [동기 디스패치](#synchronous-dispatching)
    - [잡 & 데이터베이스 트랜잭션](#jobs-and-database-transactions)
    - [잡 체이닝(Chaining)](#job-chaining)
    - [큐 및 커넥션 커스터마이징](#customizing-the-queue-and-connection)
    - [최대 시도 횟수/타임아웃 값 지정](#max-job-attempts-and-timeout)
    - [오류 처리](#error-handling)
- [잡 배치 처리(Job Batching)](#job-batching)
    - [배치 처리 가능한 잡 정의](#defining-batchable-jobs)
    - [배치 디스패치](#dispatching-batches)
    - [체인 & 배치](#chains-and-batches)
    - [배치에 잡 추가하기](#adding-jobs-to-batches)
    - [배치 상태 확인](#inspecting-batches)
    - [배치 취소](#cancelling-batches)
    - [배치 실패 처리](#batch-failures)
    - [배치 레코드 정리(Pruning)](#pruning-batches)
    - [DynamoDB에 배치 저장](#storing-batches-in-dynamodb)
- [클로저를 큐로 보내기](#queueing-closures)
- [큐 워커 실행](#running-the-queue-worker)
    - [`queue:work` 명령어](#the-queue-work-command)
    - [큐 우선순위](#queue-priorities)
    - [큐 워커 & 배포](#queue-workers-and-deployment)
    - [잡 만료 및 타임아웃](#job-expirations-and-timeouts)
- [Supervisor 설정](#supervisor-configuration)
- [실패한 잡 처리하기](#dealing-with-failed-jobs)
    - [실패한 잡 후처리](#cleaning-up-after-failed-jobs)
    - [실패한 잡 재시도](#retrying-failed-jobs)
    - [누락된 모델 무시](#ignoring-missing-models)
    - [실패한 잡 정리](#pruning-failed-jobs)
    - [DynamoDB에 실패한 잡 저장](#storing-failed-jobs-in-dynamodb)
    - [실패한 잡 저장 비활성화](#disabling-failed-job-storage)
    - [실패한 잡 이벤트](#failed-job-events)
- [큐에서 잡 지우기](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [테스트](#testing)
    - [일부 잡만 페이크 처리](#faking-a-subset-of-jobs)
    - [잡 체인 테스트](#testing-job-chains)
    - [잡 배치 테스트](#testing-job-batches)
    - [잡/큐 상호작용 테스트](#testing-job-queue-interactions)
- [잡 이벤트](#job-events)

<a name="introduction"></a>
## 소개

웹 애플리케이션을 개발하다 보면, 업로드된 CSV 파일을 파싱하고 저장하는 등 일반적인 웹 요청에서 처리하기엔 너무 오래 걸리는 작업이 있을 수 있습니다. 다행히도, Laravel은 이러한 작업들을 큐에 등록하여 백그라운드에서 처리할 수 있는 큐 시스템을 쉽게 제공합니다. 시간이 많이 소요되는 작업을 큐로 분리함으로써, 애플리케이션은 더욱 빠르게 웹 요청에 응답할 수 있으며, 고객에게 더 나은 사용자 경험을 제공할 수 있습니다.

Laravel 큐는 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 관계형 데이터베이스 등 다양한 큐 백엔드에 대해 통합된 큐 API를 제공합니다.

큐의 설정 값은 애플리케이션의 `config/queue.php` 파일에 저장되어 있습니다. 이 파일에는 데이터베이스, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/) 등 다양한 드라이버별 커넥션 설정이 포함되어 있으며, (로컬 개발용으로) 즉시 잡을 실행하는 동기 드라이버도 포함되어 있습니다. 큐에 쌓인 잡을 그냥 버리는 `null` 드라이버도 포함되어 있습니다.

> [!NOTE]
> Laravel은 현재 Redis 기반 큐를 위한 아름다운 대시보드 및 설정 시스템인 Horizon을 제공합니다. 자세한 내용은 [Horizon 공식 문서](/docs/{{version}}/horizon)를 참고하세요.

<a name="connections-vs-queues"></a>
### 커넥션 vs. 큐

Laravel 큐를 사용하기 전에 "커넥션(connection)"과 "큐(queue)"의 차이를 이해하는 것이 중요합니다. `config/queue.php` 설정 파일에는 `connections`라는 배열이 있습니다. 이 옵션은 Amazon SQS, Beanstalk, Redis 등 백엔드 큐 서비스와의 연결을 정의합니다. 하지만 하나의 큐 커넥션은 여러 개의 "큐"를 가질 수 있으며, 각각은 서로 다른 큐 잡의 스택 또는 집합으로 생각할 수 있습니다.

`queue` 설정 파일의 각 커넥션 설정 예시에는 `queue` 속성이 포함되어 있습니다. 이 속성은 해당 커넥션에 잡이 디스패치될 때 기본적으로 사용할 큐 이름을 지정합니다. 즉, 잡을 특정 큐에 배치하지 않고 디스패치하면 커넥션 설정의 `queue` 속성에 지정된 큐로 이동하게 됩니다:

```php
use App\Jobs\ProcessPodcast;

// 이 잡은 기본 커넥션의 기본 큐로 전송됩니다...
ProcessPodcast::dispatch();

// 이 잡은 기본 커넥션의 "emails" 큐로 전송됩니다...
ProcessPodcast::dispatch()->onQueue('emails');
```

일부 애플리케이션은 처리 우선순위 같은 것이 필요 없어서 한 개의 간단한 큐만 사용해도 충분할 수 있습니다. 하지만 잡을 여러 큐로 분리하면 우선순위대로 작업을 처리할 수 있으므로, (아래 예시처럼) `high` 큐의 작업을 우선 처리하는 워커를 별도로 실행하는 등의 전략을 세울 수 있습니다:

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버 참고 사항 및 사전 준비 사항

<a name="database"></a>
#### 데이터베이스

`database` 큐 드라이버를 사용하려면 잡을 저장할 데이터베이스 테이블이 필요합니다. 일반적으로 Laravel의 기본 마이그레이션 가운데 `0001_01_01_000002_create_jobs_table.php` 파일에 이 테이블 생성이 포함되어 있지만, 만약 애플리케이션에 해당 마이그레이션이 없다면 `make:queue-table` Artisan 명령어로 생성할 수 있습니다:

```shell
php artisan make:queue-table

php artisan migrate
```

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면 `config/database.php` 설정 파일에서 Redis 데이터베이스 연결을 구성해야 합니다.

> [!WARNING]
> `redis` 큐 드라이버는 `serializer` 및 `compression` 옵션을 지원하지 않습니다.

**Redis 클러스터**

Redis 클러스터를 사용하는 경우, 큐 이름에 [key hash tag](https://redis.io/docs/reference/cluster-spec/#hash-tags)를 포함해야 합니다. 그래야 동일한 큐에 대한 모든 Redis 키가 같은 해시 슬롯에 배치됩니다:

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

Redis 큐를 사용할 때 `block_for` 옵션으로 워커가 잡을 찾기까지 얼마나 대기할지 지정할 수 있습니다. 큐에 잡이 많지 않을 때 계속해서 Redis를 폴링하는 대신, 이 옵션을 적절히 조절하면 효과적입니다. 예를 들어 5초로 설정하면, 잡이 나타날 때까지 5초씩 대기 후 다시 폴링을 반복합니다:

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
> `block_for` 값을 `0`으로 하면 워커는 잡이 생길 때까지 무한 대기합니다. 이 상태에서는 `SIGTERM`과 같은 신호를 처리하지 못하고, 잡 처리가 끝난 후에야 신호를 반영합니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 사전 준비 사항

아래 큐 드라이버들을 사용하려면 다음 패키지들이 필요합니다. Composer로 설치하세요:

<div class="content-list" markdown="1">

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~2.0` 또는 phpredis PHP 확장
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`

</div>

---

**[아래의 추가 내용 번역 요청이 있으시면 이어서 번역해 드릴 수 있습니다!]**

> 현재 게시글은 분량 관계상 "소개", "커넥션 vs. 큐", "드라이버 참고 사항 및 사전 준비 사항"까지만 번역되었습니다.
> 만약 이외의 섹션(잡 생성, 잡 미들웨어 등)도 한글 번역이 계속해서 필요하시다면, 원하시는 섹션을 알려주세요! 이어서 빠르게 전체 분량 번역을 계속해드릴 수 있습니다.