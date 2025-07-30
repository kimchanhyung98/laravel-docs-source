# 이벤트 (Events)

- [소개](#introduction)
- [이벤트와 리스너 생성하기](#generating-events-and-listeners)
- [이벤트와 리스너 등록하기](#registering-events-and-listeners)
    - [이벤트 발견(Event Discovery)](#event-discovery)
    - [이벤트 수동 등록](#manually-registering-events)
    - [클로저(Closure) 리스너](#closure-listeners)
- [이벤트 정의하기](#defining-events)
- [리스너 정의하기](#defining-listeners)
- [큐잉된 이벤트 리스너](#queued-event-listeners)
    - [큐와 직접 상호작용하기](#manually-interacting-with-the-queue)
    - [큐잉된 이벤트 리스너와 데이터베이스 트랜잭션](#queued-event-listeners-and-database-transactions)
    - [큐잉된 리스너 미들웨어](#queued-listener-middleware)
    - [암호화된 큐잉 리스너](#encrypted-queued-listeners)
    - [실패한 작업 처리](#handling-failed-jobs)
- [이벤트 발행하기](#dispatching-events)
    - [데이터베이스 트랜잭션 이후 이벤트 발행하기](#dispatching-events-after-database-transactions)
- [이벤트 구독자](#event-subscribers)
    - [이벤트 구독자 작성하기](#writing-event-subscribers)
    - [이벤트 구독자 등록하기](#registering-event-subscribers)
- [테스트](#testing)
    - [일부 이벤트만 가짜 처리하기](#faking-a-subset-of-events)
    - [범위 지정 이벤트 가짜 처리](#scoped-event-fakes)

<a name="introduction"></a>
## 소개

Laravel의 이벤트는 간단한 옵저버 패턴 구현을 제공하여, 애플리케이션 내에서 발생하는 다양한 이벤트를 구독하고 청취할 수 있게 해줍니다. 이벤트 클래스는 보통 `app/Events` 디렉토리에 저장되며, 해당 이벤트 리스너는 `app/Listeners`에 위치합니다. 만약 이 디렉토리들이 애플리케이션 내에 없다면 걱정하지 마세요. Artisan 콘솔 명령으로 이벤트와 리스너를 생성할 때 자동으로 생성됩니다.

이벤트는 애플리케이션의 여러 부분을 결합도를 낮추는 데 매우 유용합니다. 하나의 이벤트에 여러 리스너가 독립적으로 연결될 수 있기 때문입니다. 예를 들어, 주문이 배송될 때마다 사용자에게 Slack 알림을 보내고 싶다면, 주문 처리 코드와 Slack 알림 코드를 직접 연결하는 대신 `App\Events\OrderShipped` 이벤트를 발생시키고, 이를 듣는 리스너가 Slack 알림을 전송하도록 설계할 수 있습니다.

<a name="generating-events-and-listeners"></a>
## 이벤트와 리스너 생성하기

빠르게 이벤트와 리스너를 생성하려면 `make:event`와 `make:listener` Artisan 명령어를 사용할 수 있습니다:

```shell
php artisan make:event PodcastProcessed

php artisan make:listener SendPodcastNotification --event=PodcastProcessed
```

편의를 위해 인수를 생략하고 명령어만 실행하면, Laravel이 자동으로 클래스 이름을 묻고, 리스너 생성 시에는 청취할 이벤트도 묻는 인터랙티브 모드가 활성화됩니다:

```shell
php artisan make:event

php artisan make:listener
```

<a name="registering-events-and-listeners"></a>
## 이벤트와 리스너 등록하기

<a name="event-discovery"></a>
### 이벤트 발견(Event Discovery)

기본적으로 Laravel은 애플리케이션의 `Listeners` 디렉토리를 스캔하여 이벤트 리스너를 자동으로 찾아 등록합니다. `handle` 또는 `__invoke`로 시작하는 메서드를 가진 리스너 클래스를 발견하면, 메서드 매개변수에 타입힌트 된 이벤트에 대해 해당 메서드들을 이벤트 리스너로 등록합니다:

```php
use App\Events\PodcastProcessed;

class SendPodcastNotification
{
    /**
     * 이벤트 처리 메서드
     */
    public function handle(PodcastProcessed $event): void
    {
        // ...
    }
}
```

PHP의 유니언 타입을 활용해 하나의 리스너에서 여러 이벤트를 청취할 수도 있습니다:

```php
/**
 * 이벤트 처리 메서드
 */
public function handle(PodcastProcessed|PodcastPublished $event): void
{
    // ...
}
```

리스너를 다른 디렉토리 또는 복수의 디렉토리에 저장한다면, 애플리케이션의 `bootstrap/app.php`에서 `withEvents` 메서드를 사용해 스캔할 디렉토리를 지정할 수 있습니다:

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/Orders/Listeners',
])
```

`*` 와일드카드를 사용해 비슷한 경로 여러 곳을 한 번에 스캔할 수도 있습니다:

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/*/Listeners',
])
```

`event:list` 명령어로 애플리케이션 내에 등록된 모든 리스너를 확인할 수 있습니다:

```shell
php artisan event:list
```

<a name="event-discovery-in-production"></a>
#### 프로덕션 환경에서 이벤트 발견 최적화

성능 향상을 위해 `optimize` 또는 `event:cache` Artisan 명령어를 이용해 모든 리스너를 미리 캐시된 매니페스트로 저장할 수 있습니다. 이 명령어들은 일반적으로 애플리케이션의 [배포 프로세스](/docs/12.x/deployment#optimization) 중에 실행합니다. 캐시된 매니페스트는 이벤트 등록 과정을 빠르게 만들어 줍니다. 캐시를 지우려면 `event:clear` 명령어를 사용하세요.

<a name="manually-registering-events"></a>
### 이벤트 수동 등록

`Event` 파사드를 사용해서 이벤트와 리스너를 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드 내에서 직접 등록할 수 있습니다:

```php
use App\Domain\Orders\Events\PodcastProcessed;
use App\Domain\Orders\Listeners\SendPodcastNotification;
use Illuminate\Support\Facades\Event;

/**
 * 애플리케이션 서비스 부트스트랩
 */
public function boot(): void
{
    Event::listen(
        PodcastProcessed::class,
        SendPodcastNotification::class,
    );
}
```

`event:list` 명령어로 애플리케이션 내에 등록된 모든 리스너를 확인할 수 있습니다:

```shell
php artisan event:list
```

<a name="closure-listeners"></a>
### 클로저(Closure) 리스너

일반적으로 리스너는 클래스로 정의하지만, `AppServiceProvider`의 `boot` 메서드에서 클로저 기반 리스너를 수동으로 등록할 수도 있습니다:

```php
use App\Events\PodcastProcessed;
use Illuminate\Support\Facades\Event;

/**
 * 애플리케이션 서비스 부트스트랩
 */
public function boot(): void
{
    Event::listen(function (PodcastProcessed $event) {
        // ...
    });
}
```

<a name="queuable-anonymous-event-listeners"></a>
#### 큐잉 가능한 무명 이벤트 리스너

클로저 기반 이벤트 리스너를 등록할 때, `Illuminate\Events\queueable` 함수를 사용해 리스너를 래핑하면 Laravel이 이를 큐를 사용해 실행하도록 지시할 수 있습니다:

```php
use App\Events\PodcastProcessed;
use function Illuminate\Events\queueable;
use Illuminate\Support\Facades\Event;

/**
 * 애플리케이션 서비스 부트스트랩
 */
public function boot(): void
{
    Event::listen(queueable(function (PodcastProcessed $event) {
        // ...
    }));
}
```

큐드 잡과 마찬가지로 `onConnection`, `onQueue`, `delay` 메서드를 사용해 큐 연결, 큐 이름, 지연 시간을 지정할 수 있습니다:

```php
Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->onConnection('redis')->onQueue('podcasts')->delay(now()->addSeconds(10)));
```

익명 큐잉 리스너 실패를 처리하고 싶을 때는 `queueable` 리스너에 `catch` 메서드를 체이닝해 클로저를 전달할 수 있습니다. 이 클로저는 이벤트 인스턴스와 실패 원인이 된 `Throwable` 인스턴스를 받습니다:

```php
use App\Events\PodcastProcessed;
use function Illuminate\Events\queueable;
use Illuminate\Support\Facades\Event;
use Throwable;

Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->catch(function (PodcastProcessed $event, Throwable $e) {
    // 큐잉 리스너 실패 처리...
}));
```

<a name="wildcard-event-listeners"></a>
#### 와일드카드 이벤트 리스너

`*` 문자를 와일드카드로 사용해 여러 이벤트를 동일 리스너에서 처리하도록 등록할 수도 있습니다. 와일드카드 리스너는 첫 번째 인자로 이벤트 이름을, 두 번째 인자로 이벤트 데이터 배열 전체를 받습니다:

```php
Event::listen('event.*', function (string $eventName, array $data) {
    // ...
});
```

<a name="defining-events"></a>
## 이벤트 정의하기

이벤트 클래스는 주로 해당 이벤트와 관련된 정보를 담는 데이터 컨테이너 역할을 합니다. 예를 들어, `App\Events\OrderShipped` 이벤트가 [Eloquent ORM](/docs/12.x/eloquent) 객체를 받는다고 가정해 보겠습니다:

```php
<?php

namespace App\Events;

use App\Models\Order;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;

class OrderShipped
{
    use Dispatchable, InteractsWithSockets, SerializesModels;

    /**
     * 새로운 이벤트 인스턴스 생성자.
     */
    public function __construct(
        public Order $order,
    ) {}
}
```

위 예시에서 볼 수 있듯이, 이 이벤트 클래스는 별도의 로직이 없으며, 구매된 `App\Models\Order` 인스턴스를 담는 그릇입니다. `SerializesModels` 트레이트는 이벤트 객체가 PHP의 `serialize` 함수로 직렬화될 때 해당 이벤트 내 Eloquent 모델을 유연하게 직렬화해 줍니다. 이는 [큐잉된 리스너](#queued-event-listeners)에서 특히 유용합니다.

<a name="defining-listeners"></a>
## 리스너 정의하기

이제 예시 이벤트의 리스너 코드를 살펴보겠습니다. 이벤트 리스너는 `handle` 메서드에서 이벤트 인스턴스를 받습니다. `make:listener` Artisan 명령을 `--event` 옵션과 함께 실행하면, 적절한 이벤트 클래스를 자동 임포트하고 `handle` 메서드에 타입힌트를 추가해 줍니다. `handle` 메서드 내에서는 이벤트 발생 시 실행할 동작을 작성하면 됩니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;

class SendShipmentNotification
{
    /**
     * 이벤트 리스너 생성자.
     */
    public function __construct() {}

    /**
     * 이벤트 처리 메서드.
     */
    public function handle(OrderShipped $event): void
    {
        // $event->order를 사용해 주문 정보 접근...
    }
}
```

> [!NOTE]
> 리스너는 생성자에서 필요한 의존성을 타입힌트할 수도 있습니다. 모든 이벤트 리스너는 Laravel의 [서비스 컨테이너](/docs/12.x/container)를 통해 자동으로 의존성 주입되므로, 필요한 모든 의존성은 자동으로 제공됩니다.

<a name="stopping-the-propagation-of-an-event"></a>
#### 이벤트 전파 중단하기

어떤 경우에는 이벤트가 다른 리스너로 전파되는 것을 막고 싶을 수 있습니다. 리스너의 `handle` 메서드에서 `false`를 반환하면 이벤트 전파가 중지됩니다.

<a name="queued-event-listeners"></a>
## 큐잉된 이벤트 리스너

리스너가 이메일 발송이나 HTTP 요청 등 느린 작업을 수행한다면, 큐잉이 유용합니다. 큐잉된 리스너를 사용하려면 먼저 [큐 구성하기](/docs/12.x/queues) 및 서버나 로컬 개발 환경에서 큐 워커를 실행해야 합니다.

리스너 클래스에 `ShouldQueue` 인터페이스를 추가하면 해당 리스너가 큐에 넣어집니다. `make:listener` 명령어로 생성된 리스너는 기본적으로 이 인터페이스를 네임스페이스에 임포트하므로 바로 사용할 수 있습니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    // ...
}
```

이제 이 리스너가 처리하는 이벤트가 발생하면 Laravel 큐 시스템을 통해 자동으로 큐에 쌓입니다. 큐 작업이 정상 완료되면 자동으로 작업이 삭제됩니다.

<a name="customizing-the-queue-connection-queue-name"></a>
#### 큐 연결, 큐 이름, 지연 시간 맞춤 설정하기

리스너 클래스에 `$connection`, `$queue`, `$delay` 속성을 정의하면 큐 연결, 큐 이름, 대기 시간을 지정할 수 있습니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    /**
     * 작업이 전송될 큐 연결 이름.
     *
     * @var string|null
     */
    public $connection = 'sqs';

    /**
     * 작업이 전송될 큐 이름.
     *
     * @var string|null
     */
    public $queue = 'listeners';

    /**
     * 작업 처리까지 대기할 시간(초).
     *
     * @var int
     */
    public $delay = 60;
}
```

런타임에 큐 연결, 큐 이름, 지연 시간을 지정하려면 `viaConnection`, `viaQueue`, `withDelay` 메서드를 정의할 수 있습니다:

```php
/**
 * 리스너가 사용할 큐 연결 이름 반환.
 */
public function viaConnection(): string
{
    return 'sqs';
}

/**
 * 리스너가 사용할 큐 이름 반환.
 */
public function viaQueue(): string
{
    return 'listeners';
}

/**
 * 작업 처리 전 대기할 시간(초) 반환.
 */
public function withDelay(OrderShipped $event): int
{
    return $event->highPriority ? 0 : 60;
}
```

<a name="conditionally-queueing-listeners"></a>
#### 조건에 따른 큐잉 결정하기

실행 시점에 큐잉 여부를 결정해야 하는 경우, 리스너에 `shouldQueue` 메서드를 추가해 부울 값을 반환하도록 할 수 있습니다. 이 메서드가 `false`를 반환하면 리스너가 큐에 쌓이지 않습니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderCreated;
use Illuminate\Contracts\Queue\ShouldQueue;

class RewardGiftCard implements ShouldQueue
{
    /**
     * 기프트 카드 보상 처리.
     */
    public function handle(OrderCreated $event): void
    {
        // ...
    }

    /**
     * 리스너를 큐에 쌓을지 여부 결정.
     */
    public function shouldQueue(OrderCreated $event): bool
    {
        return $event->order->subtotal >= 5000;
    }
}
```

<a name="manually-interacting-with-the-queue"></a>
### 큐와 직접 상호작용하기

리스너의 기본 큐 작업에서 `delete`나 `release` 메서드를 수동으로 호출하려면 `Illuminate\Queue\InteractsWithQueue` 트레이트를 사용할 수 있습니다. 이 트레이트는 기본 생성된 리스너에 자동 임포트되어 있으며, 관련 메서드들이 제공됩니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\InteractsWithQueue;

class SendShipmentNotification implements ShouldQueue
{
    use InteractsWithQueue;

    /**
     * 이벤트 처리 메서드.
     */
    public function handle(OrderShipped $event): void
    {
        if (true) {
            $this->release(30);
        }
    }
}
```

<a name="queued-event-listeners-and-database-transactions"></a>
### 큐잉된 이벤트 리스너와 데이터베이스 트랜잭션

데이터베이스 트랜잭션 내에서 큐잉된 리스너를 디스패치할 경우, 트랜잭션 커밋 전에 큐가 실행될 수 있습니다. 이 경우 트랜잭션 내 모델이나 데이터베이스 레코드 변경 내용이 아직 DB에 반영되지 않았거나, 새로 생성된 모델이 존재하지 않을 수 있습니다. 리스너가 해당 모델에 의존하면 처리 도중 에러가 발생할 수 있습니다.

큐 연결 설정의 `after_commit` 옵션이 `false`로 되어 있으면, 큐잉된 특정 리스너가 열린 모든 DB 트랜잭션이 커밋된 뒤에만 실행되도록 하려면 리스너 클래스에 `ShouldQueueAfterCommit` 인터페이스를 구현하면 됩니다:

```php
<?php

namespace App\Listeners;

use Illuminate\Contracts\Queue\ShouldQueueAfterCommit;
use Illuminate\Queue\InteractsWithQueue;

class SendShipmentNotification implements ShouldQueueAfterCommit
{
    use InteractsWithQueue;
}
```

> [!NOTE]
> 이 문제를 우회하는 방법에 대해 더 알고 싶다면, [큐 작업과 데이터베이스 트랜잭션](/docs/12.x/queues#jobs-and-database-transactions) 관련 문서를 참고하세요.

<a name="queued-listener-middleware"></a>
### 큐잉된 리스너 미들웨어

큐잉된 리스너는 [잡 미들웨어](/docs/12.x/queues#job-middleware)를 이용할 수 있습니다. 잡 미들웨어는 큐잉된 리스너 실행 전후에 커스텀 로직을 감싸서 중복 코드를 줄여줍니다. 잡 미들웨어 생성 후, 리스너의 `middleware` 메서드에서 반환해 연결할 수 있습니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use App\Jobs\Middleware\RateLimited;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    /**
     * 이벤트 처리 메서드.
     */
    public function handle(OrderShipped $event): void
    {
        // 이벤트 처리...
    }

    /**
     * 이 리스너가 거쳐야 하는 미들웨어 반환.
     *
     * @return array<int, object>
     */
    public function middleware(OrderShipped $event): array
    {
        return [new RateLimited];
    }
}
```

<a name="encrypted-queued-listeners"></a>
#### 암호화된 큐잉 리스너

Laravel은 큐잉된 리스너 데이터의 기밀성과 무결성을 [암호화](/docs/12.x/encryption)할 수 있도록 지원합니다. 사용하려면 리스너 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하면 됩니다. 그러면 Laravel이 자동으로 큐에 삽입하기 전에 리스너를 암호화합니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldBeEncrypted;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue, ShouldBeEncrypted
{
    // ...
}
```

<a name="handling-failed-jobs"></a>
### 실패한 작업 처리

가끔 큐잉된 이벤트 리스너가 실패할 수 있습니다. 큐 작업이 큐 워커에서 설정한 최대 시도 횟수를 넘기면, 리스너의 `failed` 메서드가 호출됩니다. 이 메서드는 이벤트 인스턴스와 실패 원인인 `Throwable` 인스턴스를 받습니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\InteractsWithQueue;
use Throwable;

class SendShipmentNotification implements ShouldQueue
{
    use InteractsWithQueue;

    /**
     * 이벤트 처리 메서드.
     */
    public function handle(OrderShipped $event): void
    {
        // ...
    }

    /**
     * 작업 실패 처리 메서드.
     */
    public function failed(OrderShipped $event, Throwable $exception): void
    {
        // ...
    }
}
```

<a name="specifying-queued-listener-maximum-attempts"></a>
#### 큐잉된 리스너 최대 시도 횟수 지정하기

큐잉된 리스너가 오류가 발생하면 무한 재시도하는 것을 원하지 않을 때가 많습니다. 이를 위해 Laravel은 리스너가 최대 몇 번까지 시도할지 지정하는 방법을 제공합니다.

리스너 클래스에 `$tries` 속성을 정의하면 시도 가능한 최대 횟수를 지정할 수 있습니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\InteractsWithQueue;

class SendShipmentNotification implements ShouldQueue
{
    use InteractsWithQueue;

    /**
     * 큐잉된 리스너 최대 시도 횟수.
     *
     * @var int
     */
    public $tries = 5;
}
```

재시도 횟수 대신 특정 시점 이후에는 더 이상 시도하지 못하도록 하려면 `retryUntil` 메서드를 정의하고 `DateTime` 인스턴스를 반환하면 됩니다:

```php
use DateTime;

/**
 * 리스너 제한 시간(타임아웃) 결정.
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(5);
}
```

`retryUntil`과 `$tries`가 모두 정의되면, Laravel은 `retryUntil`을 우선시합니다.

<a name="specifying-queued-listener-backoff"></a>
#### 큐잉된 리스너 재시도 지연 대기시간 지정하기

예외가 발생한 리스너를 재시도하기 전까지 기다릴 초 단위 시간을 지정하려면, `$backoff` 속성을 정의하세요:

```php
/**
 * 재시도 전 대기할 초 단위 시간.
 *
 * @var int
 */
public $backoff = 3;
```

더 복잡한 로직이 필요하다면 `backoff` 메서드를 정의할 수도 있습니다:

```php
/**
 * 재시도 전 대기할 초 단위 시간 계산.
 */
public function backoff(OrderShipped $event): int
{
    return 3;
}
```

"지수적" 백오프를 적용하려면 `backoff` 메서드에서 초 단위 대기 시간 배열을 반환하세요. 예를 들어, 첫 재시도는 1초, 두 번째는 5초, 세 번째부터는 10초 간 대기:

```php
/**
 * 재시도 전 대기할 초 단위 시간 배열 반환.
 *
 * @return list<int>
 */
public function backoff(OrderShipped $event): array
{
    return [1, 5, 10];
}
```

<a name="specifying-queued-listener-max-exceptions"></a>
#### 큐잉된 리스너 최대 예외 횟수 지정하기

재시도 횟수 제한과 별개로, 처리 중 발생한 미처리 예외 횟수에 따라 실패시킬 수도 있습니다. 이를 위해 `$maxExceptions` 속성을 지정하세요:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\InteractsWithQueue;

class SendShipmentNotification implements ShouldQueue
{
    use InteractsWithQueue;

    /**
     * 최대 시도 횟수.
     *
     * @var int
     */
    public $tries = 25;

    /**
     * 최대 허용 미처리 예외 횟수.
     *
     * @var int
     */
    public $maxExceptions = 3;

    /**
     * 이벤트 처리 메서드.
     */
    public function handle(OrderShipped $event): void
    {
        // 이벤트 처리...
    }
}
```

예제에서는 최대 25회까지 재시도하지만, 미처리 예외가 3회 발생하면 즉시 실패합니다.

<a name="specifying-queued-listener-timeout"></a>
#### 큐잉된 리스너 타임아웃 지정하기

예상 처리 시간을 알고 있다면, 리스너가 이를 초과 실행할 경우 큐 워커가 오류를 발생시키도록 할 수 있습니다. 리스너 클래스에 `$timeout` 속성을 정의해 최대 실행 시간을 초 단위로 지정하세요:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    /**
     * 타임아웃까지 허용할 최대 실행 시간(초).
     *
     * @var int
     */
    public $timeout = 120;
}
```

타임아웃 시점에 리스너를 실패로 표시하려면 `$failOnTimeout` 속성을 `true`로 설정합니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    /**
     * 타임아웃 시 실패 처리 여부.
     *
     * @var bool
     */
    public $failOnTimeout = true;
}
```

<a name="dispatching-events"></a>
## 이벤트 발행하기

이벤트를 실행하려면 이벤트 클래스의 정적 `dispatch` 메서드를 호출하세요. 이 메서드는 `Illuminate\Foundation\Events\Dispatchable` 트레이트를 통해 제공됩니다. `dispatch`에 넘긴 인수들은 이벤트 생성자로 전달됩니다:

```php
<?php

namespace App\Http\Controllers;

use App\Events\OrderShipped;
use App\Models\Order;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class OrderShipmentController extends Controller
{
    /**
     * 주문을 발송 처리합니다.
     */
    public function store(Request $request): RedirectResponse
    {
        $order = Order::findOrFail($request->order_id);

        // 주문 발송 로직...

        OrderShipped::dispatch($order);

        return redirect('/orders');
    }
}
```

조건에 따라 이벤트를 발행하고 싶으면 `dispatchIf`와 `dispatchUnless` 메서드를 사용할 수 있습니다:

```php
OrderShipped::dispatchIf($condition, $order);

OrderShipped::dispatchUnless($condition, $order);
```

> [!NOTE]
> 테스트 시에는 이벤트 리스너가 실제 실행되지 않도록 하면서 이벤트가 발행되었는지 검증할 때 Laravel 내장 [테스트 헬퍼](#testing)를 활용하면 편리합니다.

<a name="dispatching-events-after-database-transactions"></a>
### 데이터베이스 트랜잭션 이후 이벤트 발행하기

활성 데이터베이스 트랜잭션이 커밋된 후에만 이벤트를 발행하도록 Laravel에 지시하고 싶으면 이벤트 클래스에 `ShouldDispatchAfterCommit` 인터페이스를 구현하세요.

이 인터페이스는 트랜잭션이 커밋될 때까지 이벤트 발행을 지연시키며, 트랜잭션 실패 시 이벤트는 무시됩니다. 트랜잭션이 없을 때는 즉시 이벤트가 발행됩니다:

```php
<?php

namespace App\Events;

use App\Models\Order;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Contracts\Events\ShouldDispatchAfterCommit;
use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;

class OrderShipped implements ShouldDispatchAfterCommit
{
    use Dispatchable, InteractsWithSockets, SerializesModels;

    /**
     * 새로운 이벤트 인스턴스 생성자.
     */
    public function __construct(
        public Order $order,
    ) {}
}
```

<a name="event-subscribers"></a>
## 이벤트 구독자

<a name="writing-event-subscribers"></a>
### 이벤트 구독자 작성하기

이벤트 구독자는 여러 이벤트에 대한 여러 핸들러를 하나의 클래스에 정의할 수 있도록 해줍니다. 구독자는 `subscribe` 메서드를 정의하여 이벤트 디스패처 인스턴스를 받고, 이를 통해 여러 이벤트 리스너를 등록할 수 있습니다:

```php
<?php

namespace App\Listeners;

use Illuminate\Auth\Events\Login;
use Illuminate\Auth\Events\Logout;
use Illuminate\Events\Dispatcher;

class UserEventSubscriber
{
    /**
     * 사용자 로그인 이벤트 처리.
     */
    public function handleUserLogin(Login $event): void {}

    /**
     * 사용자 로그아웃 이벤트 처리.
     */
    public function handleUserLogout(Logout $event): void {}

    /**
     * 구독자에 대한 리스너 등록.
     */
    public function subscribe(Dispatcher $events): void
    {
        $events->listen(
            Login::class,
            [UserEventSubscriber::class, 'handleUserLogin']
        );

        $events->listen(
            Logout::class,
            [UserEventSubscriber::class, 'handleUserLogout']
        );
    }
}
```

같은 클래스 내에 이벤트 처리 메서드가 정의되어 있다면, `subscribe` 메서드에서 이벤트 클래스명과 메서드명을 배열로 반환하는 방법도 편리합니다. Laravel은 자동으로 구독자 클래스 이름을 사용해 리스너를 등록합니다:

```php
<?php

namespace App\Listeners;

use Illuminate\Auth\Events\Login;
use Illuminate\Auth\Events\Logout;
use Illuminate\Events\Dispatcher;

class UserEventSubscriber
{
    /**
     * 사용자 로그인 이벤트 처리.
     */
    public function handleUserLogin(Login $event): void {}

    /**
     * 사용자 로그아웃 이벤트 처리.
     */
    public function handleUserLogout(Logout $event): void {}

    /**
     * 구독자에 대한 리스너 등록.
     *
     * @return array<string, string>
     */
    public function subscribe(Dispatcher $events): array
    {
        return [
            Login::class => 'handleUserLogin',
            Logout::class => 'handleUserLogout',
        ];
    }
}
```

<a name="registering-event-subscribers"></a>
### 이벤트 구독자 등록하기

작성한 구독자는 Laravel의 [이벤트 발견 규칙](#event-discovery)에 따르는 핸들러 메서드가 있다면 자동 등록됩니다. 그렇지 않으면 `Event` 파사드의 `subscribe` 메서드를 통해 수동으로 등록할 수 있으며, 보통은 `AppServiceProvider` 클래스의 `boot` 메서드에 작성합니다:

```php
<?php

namespace App\Providers;

use App\Listeners\UserEventSubscriber;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 부트스트랩.
     */
    public function boot(): void
    {
        Event::subscribe(UserEventSubscriber::class);
    }
}
```

<a name="testing"></a>
## 테스트

이벤트를 발생시키는 코드를 테스트할 때, 이벤트 리스너가 실제 실행되지 않도록 하면서 이벤트가 정상적으로 발행되었는지만 검증하고 싶으면, `Event` 파사드의 `fake` 메서드를 사용할 수 있습니다.

`fake`로 이벤트를 가짜 처리하면 리스너 실행은 멈추며, 테스트 중에는 `assertDispatched`, `assertNotDispatched`, `assertNothingDispatched` 메서드로 이벤트 발행 여부를 검증할 수 있습니다:

```php tab=Pest
<?php

use App\Events\OrderFailedToShip;
use App\Events\OrderShipped;
use Illuminate\Support\Facades\Event;

test('orders can be shipped', function () {
    Event::fake();

    // 주문 발송 동작 수행...

    // 이벤트가 발행됐는지 단언.
    Event::assertDispatched(OrderShipped::class);

    // 이벤트가 두 번 발행됐는지 단언.
    Event::assertDispatched(OrderShipped::class, 2);

    // 특정 이벤트가 발행되지 않았는지 단언.
    Event::assertNotDispatched(OrderFailedToShip::class);

    // 이벤트가 전혀 발행되지 않았음을 단언.
    Event::assertNothingDispatched();
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use App\Events\OrderFailedToShip;
use App\Events\OrderShipped;
use Illuminate\Support\Facades\Event;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * 주문 발송 기능 테스트.
     */
    public function test_orders_can_be_shipped(): void
    {
        Event::fake();

        // 주문 발송 동작 수행...

        // 이벤트가 발행됐는지 단언.
        Event::assertDispatched(OrderShipped::class);

        // 이벤트가 두 번 발행됐는지 단언.
        Event::assertDispatched(OrderShipped::class, 2);

        // 특정 이벤트가 발행되지 않았는지 단언.
        Event::assertNotDispatched(OrderFailedToShip::class);

        // 이벤트가 전혀 발행되지 않았음을 단언.
        Event::assertNothingDispatched();
    }
}
```

`assertDispatched`, `assertNotDispatched`에 클로저를 넘기면, 해당 조건을 만족하는 이벤트가 적어도 하나가 발행되었는지 확인합니다:

```php
Event::assertDispatched(function (OrderShipped $event) use ($order) {
    return $event->order->id === $order->id;
});
```

특정 이벤트에 대해 리스너가 등록되어 있는지도 `assertListening`으로 확인할 수 있습니다:

```php
Event::assertListening(
    OrderShipped::class,
    SendShipmentNotification::class
);
```

> [!WARNING]
> `Event::fake()` 호출 후에는 어떤 이벤트 리스너도 실행되지 않습니다. 따라서 모델 팩토리 등이 `creating` 이벤트에서 UUID를 생성하는 등 이벤트에 의존한다면, 팩토리 호출 후에 `Event::fake()`를 실행해야 합니다.

<a name="faking-a-subset-of-events"></a>
### 일부 이벤트만 가짜 처리하기

특정 이벤트 집합만 가짜 처리하려면 `fake` 또는 `fakeFor` 메서드에 이벤트 클래스 배열을 전달하세요:

```php tab=Pest
test('orders can be processed', function () {
    Event::fake([
        OrderCreated::class,
    ]);

    $order = Order::factory()->create();

    Event::assertDispatched(OrderCreated::class);

    // 다른 이벤트는 정상적으로 발행됨...
    $order->update([
        // ...
    ]);
});
```

```php tab=PHPUnit
/**
 * 주문 처리 테스트.
 */
public function test_orders_can_be_processed(): void
{
    Event::fake([
        OrderCreated::class,
    ]);

    $order = Order::factory()->create();

    Event::assertDispatched(OrderCreated::class);

    // 다른 이벤트는 정상적으로 발행됨...
    $order->update([
        // ...
    ]);
}
```

특정 이벤트를 제외하고 모든 이벤트를 가짜 처리할 수도 있습니다. `except` 메서드를 활용하세요:

```php
Event::fake()->except([
    OrderCreated::class,
]);
```

<a name="scoped-event-fakes"></a>
### 범위 지정 이벤트 가짜 처리

테스트 일부 구간에서만 이벤트를 가짜 처리하고 싶을 때는 `fakeFor` 메서드를 사용하세요:

```php tab=Pest
<?php

use App\Events\OrderCreated;
use App\Models\Order;
use Illuminate\Support\Facades\Event;

test('orders can be processed', function () {
    $order = Event::fakeFor(function () {
        $order = Order::factory()->create();

        Event::assertDispatched(OrderCreated::class);

        return $order;
    });

    // 이후 구간에서는 이벤트가 정상적으로 발행되고 옵저버도 실행됨...
    $order->update([
        // ...
    ]);
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use App\Events\OrderCreated;
use App\Models\Order;
use Illuminate\Support\Facades\Event;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * 주문 처리 기능 테스트.
     */
    public function test_orders_can_be_processed(): void
    {
        $order = Event::fakeFor(function () {
            $order = Order::factory()->create();

            Event::assertDispatched(OrderCreated::class);

            return $order;
        });

        // 이후 구간에서는 이벤트가 정상적으로 발행되고 옵저버도 실행됨...
        $order->update([
            // ...
        ]);
    }
}
```