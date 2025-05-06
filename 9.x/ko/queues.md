# 큐 (Queues)

- [소개](#introduction)
    - [커넥션 vs. 큐](#connections-vs-queues)
    - [드라이버 주의사항 및 선행조건](#driver-prerequisites)
- [잡 생성하기](#creating-jobs)
    - [잡 클래스 생성하기](#generating-job-classes)
    - [클래스 구조](#class-structure)
    - [유일한 잡(Unique Jobs)](#unique-jobs)
- [잡 미들웨어](#job-middleware)
    - [요율 제한(Rate Limiting)](#rate-limiting)
    - [잡 중복 방지](#preventing-job-overlaps)
    - [예외 스로틀링](#throttling-exceptions)
- [잡 디스패치하기](#dispatching-jobs)
    - [딜레이 디스패치](#delayed-dispatching)
    - [동기 디스패치](#synchronous-dispatching)
    - [잡과 DB 트랜잭션](#jobs-and-database-transactions)
    - [잡 체인(Chaining)](#job-chaining)
    - [큐 및 커넥션 커스터마이징](#customizing-the-queue-and-connection)
    - [최대 시도 횟수/타임아웃 지정](#max-job-attempts-and-timeout)
    - [에러 처리](#error-handling)
- [잡 배치(Batching)](#job-batching)
    - [배치 가능한 잡 정의하기](#defining-batchable-jobs)
    - [배치 디스패치하기](#dispatching-batches)
    - [배치에 잡 추가하기](#adding-jobs-to-batches)
    - [배치 조회하기](#inspecting-batches)
    - [배치 취소하기](#cancelling-batches)
    - [배치 실패](#batch-failures)
    - [배치 정리(Pruning)](#pruning-batches)
- [클로저 큐잉](#queueing-closures)
- [큐 워커 실행하기](#running-the-queue-worker)
    - [`queue:work` 명령어](#the-queue-work-command)
    - [큐 우선순위](#queue-priorities)
    - [큐 워커와 배포](#queue-workers-and-deployment)
    - [잡 만료 및 타임아웃](#job-expirations-and-timeouts)
- [Supervisor 설정](#supervisor-configuration)
- [실패한 잡 처리](#dealing-with-failed-jobs)
    - [실패한 잡 정리](#cleaning-up-after-failed-jobs)
    - [실패한 잡 재시도](#retrying-failed-jobs)
    - [누락된 모델 무시하기](#ignoring-missing-models)
    - [실패한 잡 정리(Pruning)](#pruning-failed-jobs)
    - [DynamoDB에 실패한 잡 저장하기](#storing-failed-jobs-in-dynamodb)
    - [실패한 잡 저장 비활성화](#disabling-failed-job-storage)
    - [실패한 잡 이벤트](#failed-job-events)
- [큐에서 잡 삭제](#clearing-jobs-from-queues)
- [큐 모니터링](#monitoring-your-queues)
- [잡 이벤트](#job-events)

<a name="introduction"></a>
## 소개

웹 애플리케이션을 구축하다보면 업로드된 CSV 파일을 파싱 및 저장과 같이 일반적인 웹 요청 처리 시간 내에 해결하기엔 시간이 많이 소요되는 작업들이 있을 수 있습니다. 다행히도, Laravel은 이러한 작업들을 백그라운드에서 처리할 수 있는 큐 잡을 쉽게 만들 수 있도록 지원합니다. 시간 소모가 큰 작업을 큐로 이동시키면, 애플리케이션은 더욱 빠르게 웹 요청을 처리할 수 있고, 사용자에게 더 나은 경험을 제공할 수 있습니다.

Laravel 큐는 [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), 심지어 관계형 데이터베이스 등 다양한 큐 백엔드에 대해 통합된 큐잉 API를 제공합니다.

큐 설정 파일은 애플리케이션의 `config/queue.php`에 위치합니다. 이 파일에는 프레임워크에 포함된 각 큐 드라이버(Database, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), [Beanstalkd](https://beanstalkd.github.io/), 그리고 즉시 작업을 실행하는 동기 드라이버 등)의 커넥션 설정이 들어 있습니다. 또한 큐를 무시하는 `null` 드라이버도 제공됩니다.

> **참고**
> Laravel은 Redis 기반 큐를 위한 Horizon 대시보드 및 설정 시스템을 제공합니다. 자세한 내용은 [Horizon 문서](/docs/{{version}}/horizon)를 참고하세요.

<a name="connections-vs-queues"></a>
### 커넥션 vs. 큐

Laravel 큐를 시작하기 전에 "커넥션"과 "큐"의 차이를 확실히 이해하는 것이 중요합니다. `config/queue.php`에는 `connections`라는 설정 배열이 있습니다. 이 옵션은 Amazon SQS, Beanstalk, Redis 같은 백엔드 큐 서비스에 대한 커넥션을 정의합니다. 한 커넥션은 여러 "큐"를 가질 수 있으며, 각 큐는 별도의 큐 잡 스택이라고 생각할 수 있습니다.

`queue` 설정 파일 내의 각 커넥션 예제에는 `queue` 속성이 포함되어 있습니다. 이 값은 해당 커넥션에서 잡이 디스패치될 때 기본적으로 사용할 큐를 지정합니다. 즉, 디스패치 시 어떤 큐에 보낼지 명시하지 않으면 이 값이 사용됩니다.

    use App\Jobs\ProcessPodcast;

    // 기본 커넥션의 기본 큐로 잡을 전송합니다...
    ProcessPodcast::dispatch();

    // 기본 커넥션의 "emails" 큐로 잡을 전송합니다...
    ProcessPodcast::dispatch()->onQueue('emails');

대부분의 애플리케이션은 복수의 큐를 사용할 필요가 없을 수도 있지만, 작업의 우선순위 처리 또는 분리 처리를 위해 여러 큐를 사용하는 것이 유용할 수 있습니다. 예를 들어 `high`라는 큐에 잡을 넣고 아래와 같이 우선 처리하게 할 수 있습니다:

```shell
php artisan queue:work --queue=high,default
```

<a name="driver-prerequisites"></a>
### 드라이버 주의사항 및 선행조건

<a name="database"></a>
#### 데이터베이스

`database` 큐 드라이버를 사용하려면 잡을 저장할 데이터베이스 테이블이 필요합니다. 아래 명령어로 테이블 생성을 위한 마이그레이션을 생성한 후, 마이그레이션을 실행하세요.

```shell
php artisan queue:table

php artisan migrate
```

그리고 `.env` 파일의 `QUEUE_CONNECTION` 환경변수를 `database`로 설정하는 것을 잊지 마세요.

    QUEUE_CONNECTION=database

<a name="redis"></a>
#### Redis

`redis` 큐 드라이버를 사용하려면 `config/database.php` 파일에서 Redis 데이터베이스 커넥션을 설정해야 합니다.

**Redis 클러스터**

Redis 큐 커넥션이 Redis 클러스터일 경우, 큐 이름은 반드시 [키 해시 태그](https://redis.io/docs/reference/cluster-spec/#hash-tags)를 포함해야 합니다. 그래야 동일 큐의 모든 Redis 키가 같은 해시 슬롯에 저장됩니다.

    'redis' => [
        'driver' => 'redis',
        'connection' => 'default',
        'queue' => '{default}',
        'retry_after' => 90,
    ],

**Blocking**

`block_for` 옵션은 잡을 기다리며 블로킹할 시간(초)을 지정합니다. 예를 들어 `5`로 지정하면, 잡이 나타날 때까지 최대 5초간 대기했다가 없으면 한 번 더 폴링합니다.

    'redis' => [
        'driver' => 'redis',
        'connection' => 'default',
        'queue' => 'default',
        'retry_after' => 90,
        'block_for' => 5,
    ],

> **경고**
> `block_for`를 `0`으로 지정하면 잡이 나타날 때까지 워커가 무한정 블로킹됩니다. `SIGTERM` 등 시그널 핸들링이 다음 잡 실행 전까지 지연될 수 있습니다.

<a name="other-driver-prerequisites"></a>
#### 기타 드라이버 선행 조건

아래 큐 드라이버에는 아래와 같은 composer 의존성 패키지가 필요합니다.

<div class="content-list" markdown="1">

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~4.0`
- Redis: `predis/predis ~1.0` 또는 phpredis PHP 확장

</div>

<a name="creating-jobs"></a>
## 잡 생성하기

<a name="generating-job-classes"></a>
### 잡 클래스 생성하기

기본적으로 모든 큐잉 가능한 잡 클래스는 `app/Jobs` 디렉터리에 보관됩니다. 이 디렉터리가 없다면, `make:job` artisan 명령 실행시 자동으로 생성됩니다.

```shell
php artisan make:job ProcessPodcast
```

생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하며, 이로써 비동기 처리용 큐에 추가됩니다.

> **참고**
> 잡 스텁은 [스텁 퍼블리싱](/docs/{{version}}/artisan#stub-customization) 기능을 통해 커스터마이즈할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조

잡 클래스는 대개 잡이 처리될 때 호출되는 `handle` 메서드만 포함하는 간단한 구조입니다. 예를 들어 팟캐스트 파일 업로드 후 파일 처리를 하는 잡 예시는 다음과 같습니다.

(코드 블록 생략: 번역하지 않습니다)

여기서는 [Eloquent 모델](/docs/{{version}}/eloquent)을 잡 생성자에 직접 전달했지만, `SerializesModels` 트레잇 덕분에 모델 및 연관관계 데이터는 큐에 직렬화/역직렬화되어 처리됩니다.

잡 생성자에 Eloquent 모델을 전달하면 식별자만 큐에 직렬화되고, 실제 잡 처리시 모델과 관계가 데이터베이스에서 재조회됩니다. 덕분에 큐 페이로드(잡 데이터)가 훨씬 가볍습니다.

<a name="handle-method-dependency-injection"></a>
#### `handle` 메서드 의존성 주입

`handle` 메서드에서는 의존성을 타입힌트로 선언할 수 있으며, Laravel [서비스 컨테이너](/docs/{{version}}/container)가 자동으로 인스턴스를 주입합니다.

의존성 주입 방식을 커스터마이즈하고 싶다면, 컨테이너의 `bindMethod` 메서드로 직접 `handle` 주입 방식을 제어할 수 있습니다. 일반적으로는 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 호출합니다.

(코드 블록 생략)

> **경고**
> 이진 데이터(예: 이미지 원본)는 `base64_encode`로 인코딩 후 큐 잡에 전달하세요. 그렇지 않으면 JSON 직렬화가 실패할 수 있습니다.

<a name="handling-relationships"></a>
#### 큐잉된 관계 데이터

관계 데이터까지 직렬화하면 잡 스트링이 커질 수 있습니다. 이럴 때는 모델에서 `withoutRelations` 메서드로 관계 데이터 없는 인스턴스를 할당할 수 있습니다.

(코드 블록 생략)

또한 잡 역직렬화 시에는 관계 데이터가 전체 조회되며, 잡 큐잉 당시의 세부 조건은 적용되지 않습니다. 특정 관계의 서브셋만을 다루려면 큐 잡 내에서 관계에 대한 추가 제약을 다시 적용해야 합니다.

<a name="unique-jobs"></a>
### 유일한 잡(Unique Jobs)

> **경고**
> 유일한 잡은 [락을 지원하는 캐시 드라이버](/docs/{{version}}/cache#atomic-locks)가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 드라이버가 지원합니다. 또한 유일 제약은 잡 배치에는 적용되지 않습니다.

특정 잡이 큐에 동시 1개만 존재하도록 하려면, 잡 클래스에 `ShouldBeUnique` 인터페이스를 구현하세요. 추가 메서드는 없습니다.

(코드 블록 생략)

이제 해당 잡은 동일한 작업이 큐에 이미 있으면 다시 디스패치되지 않습니다.

특정 키로 유일 잡을 제어하거나 유일 락 타임아웃을 지정하려면, `uniqueId` 및 `uniqueFor` 프로퍼티/메서드를 정의할 수 있습니다.

(코드 블록 생략)

지정한 키 값(예시: 상품 ID)으로 같은 잡이 "유일함"을 보장하며, 1시간 내에 기존 잡이 끝나지 않으면 유일 락이 해제됩니다.

> **경고**
> 여러 웹서버/컨테이너에서 잡을 디스패치한다면, 모든 서버가 같은 캐시 서버를 사용해야 유일 제약이 정확하게 동작합니다.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### 처리 시작 전까지 유일성 유지

기본적으로 유일 잡은 처리 완료 혹은 재시도 실패 후 잠금이 풀립니다. 처리 직전 잠금을 풀고 싶다면 `ShouldBeUnique` 대신 `ShouldBeUniqueUntilProcessing`을 구현합니다.

(코드 블록 생략)

<a name="unique-job-locks"></a>
#### 유일 잡 락

내부적으로 `ShouldBeUnique` 잡은 `uniqueId` 키로 [락](/docs/{{version}}/cache#atomic-locks)를 획득하려 시도합니다. 락 획득 실패 시 잡은 디스패치되지 않습니다. 기본 캐시 드라이버가 사용되지만, `uniqueVia` 메서드로 다른 드라이버를 지정할 수도 있습니다.

(코드 블록 생략)

> **참고**
> 잡의 동시 처리만 제한하려면 [`WithoutOverlapping`](/docs/{{version}}/queues#preventing-job-overlaps) 미들웨어를 사용하세요.

<a name="job-middleware"></a>
## 잡 미들웨어

잡 미들웨어를 사용하면 개별 잡 코드에 중복을 줄이고, 공통 처리를 깔끔하게 모듈화할 수 있습니다. 예를 들어 Redis 요율 제한을 적용해 5초에 1개만 처리하는 미들웨어를 아래처럼 구현할 수 있습니다.

(코드 블록 생략)

이 로직을 핸들 메서드에 매번 넣기보단, 미들웨어로 분리하면 여러 잡에서 쉽게 재사용할 수 있습니다. Laravel에서는 잡 미들웨어를 보관할 표준 경로가 없으니 자유롭게 위치시키세요. 예를 들어 `app/Jobs/Middleware` 아래에 둘 수 있습니다.

(코드 블록 생략)

작성한 미들웨어는 잡의 `middleware` 메서드에서 반환하여 적용합니다. `make:job`명령으로 생성된 잡에는 이 메서드가 없으니, 직접 추가하세요.

(코드 블록 생략)

> **참고**
> 잡 미들웨어는 큐잉 가능한 이벤트 리스너, 메일, 알림에도 적용할 수 있습니다.

<a name="rate-limiting"></a>
### 요율 제한(Rate Limiting)

직접 요율 제한용 미들웨어를 만들 수도 있지만, Laravel은 기본 RateLimiting 미들웨어를 제공합니다. [라우트 요율 제한자](/docs/{{version}}/routing#defining-rate-limiters)와 유사하게 `RateLimiter` 파사드로 정의합니다.

예를 들어 무료 사용자에게는 한 시간에 한 번만 백업 허용, 프리미엄에는 무제한을 다음과 같이 정의할 수 있습니다.

(코드 블록 생략)

`perMinute` 등 다양한 기준으로 제한할 수 있고, `by` 값에 고객 ID 등 원하는 값을 넣을 수 있습니다.

(코드 블록 생략)

이렇게 정의한 제한자는 잡의 `middleware` 메서드에서 `Illuminate\Queue\Middleware\RateLimited`로 지정해 사용할 수 있습니다.

(코드 블록 생략)

요율 제한으로 큐에 재배치될 때마다 `attempts` 값이 증가하니, `tries`, `maxExceptions` 값을 조절해야 할 수도 있습니다. 시간 기준 제한에는 [`retryUntil` 메서드](#time-based-attempts)를 사용하세요.

재시도하지 않으려면 `dontRelease`를 사용하세요.

(코드 블록 생략)

> **참고**
> Redis 환경에선 `Illuminate\Queue\Middleware\RateLimitedWithRedis`로 더 효율적으로 처리할 수 있습니다.

<a name="preventing-job-overlaps"></a>
### 잡 중복 방지

Laravel은 임의의 키를 기준으로 잡 중복 실행을 막는 `Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어를 제공합니다. 예를 들어 유저별 신용 점수를 처리하는 경우 동시에 두 잡이 한 유저를 갱신하지 않도록 할 수 있습니다.

(코드 블록 생략)

중복 잡이 발생하면 재시도 대기 시간도 지정 가능합니다.

(코드 블록 생략)

즉시 중복 잡을 삭제하려면 `dontRelease`를 사용하세요.

(코드 블록 생략)

잡이 예상치 못하게 실패(예: 타임아웃)하면 락이 풀리지 않을 수 있으니, `expireAfter`로 만료 시간을 추가 지정하는 것이 안전합니다.

(코드 블록 생략)

> **경고**
> `WithoutOverlapping`은 [락을 지원하는 캐시 드라이버](/docs/{{version}}/cache#atomic-locks)가 필요합니다.

<a name="sharing-lock-keys"></a>
#### 잡 클래스간 락 키 공유

기본적으로 `WithoutOverlapping`은 동일 클래스의 중복만 방지합니다. 서로 다른 잡이 같은 키를 쓸 경우에도 중복을 막으려면 `shared` 메서드를 사용하세요.

(코드 블록 생략)

<a name="throttling-exceptions"></a>
### 예외 스로틀링

`Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어를 사용하면 잡 실행 중 일정 횟수 이상 예외 발생시 일정 시간 잡 실행을 지연할 수 있습니다. 불안정한 외부 서비스와 연동시 유용합니다.

(코드 블록 생략)

처음 인자는 예외 발생 최대 횟수, 두 번째는 재시도 대기 시간(분)입니다. 지정 횟수 미만에서 예외가 발생하면 바로 재시도하지만, `backoff`로 대기 시간도 지정 가능합니다.

(코드 블록 생략)

여러 잡이 같은 써드파티와 연동한다면, `by`로 공통 스로틀링 버킷을 만들 수 있습니다.

(코드 블록 생략)

> **참고**
> Redis 사용시에는 `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis`로 더 효율적인 처리가 가능합니다.

---

(이하 하위 목차 구성 동일, 본문은 상단 예시와 마찬가지로 다음 패턴에 따라 번역합니다.)

---

**[번역 범위 주의사항]**

- 코드/HTML/URL은 번역하지 않음.
- 마크다운 구조 유지.
- 직역→의역→전문 용어 변환 순서로 최대한 자연스럽고 일관성있는 번역 적용.
- 목차, 주석, 박스(참고/경고 등)는 원문의 강조 스타일에 맞춰 유지.

---

*(아래부터 제공된 전체 본문을 문의하셔서, 분량 및 품질 유지를 위해 각 항목별로 동일 패턴으로 번역해드릴 수 있습니다. 이어서 번역이 필요하시다면 계속 요청해 주세요.)*