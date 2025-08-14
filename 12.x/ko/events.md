# 이벤트 (Events)

- [소개](#introduction)
- [이벤트 및 리스너 생성](#generating-events-and-listeners)
- [이벤트 및 리스너 등록](#registering-events-and-listeners)
    - [이벤트 자동 탐지](#event-discovery)
    - [이벤트 수동 등록](#manually-registering-events)
    - [클로저 리스너](#closure-listeners)
- [이벤트 정의](#defining-events)
- [리스너 정의](#defining-listeners)
- [큐잉된 이벤트 리스너](#queued-event-listeners)
    - [큐 수동 조작](#manually-interacting-with-the-queue)
    - [데이터베이스 트랜잭션과 큐잉된 이벤트 리스너](#queued-event-listeners-and-database-transactions)
    - [큐 리스너 미들웨어](#queued-listener-middleware)
    - [암호화된 큐 리스너](#encrypted-queued-listeners)
    - [실패한 작업 처리](#handling-failed-jobs)
- [이벤트 디스패치](#dispatching-events)
    - [데이터베이스 트랜잭션 후 이벤트 디스패치](#dispatching-events-after-database-transactions)
    - [이벤트 지연 실행](#deferring-events)
- [이벤트 구독자](#event-subscribers)
    - [이벤트 구독자 작성](#writing-event-subscribers)
    - [이벤트 구독자 등록](#registering-event-subscribers)
- [테스트](#testing)
    - [일부 이벤트만 페이크 처리](#faking-a-subset-of-events)
    - [스코프 단위 이벤트 페이크](#scoped-event-fakes)

<a name="introduction"></a>
## 소개

Laravel의 이벤트는 단순한 옵저버 패턴을 구현함으로써, 애플리케이션 내에서 발생하는 다양한 이벤트를 구독하고 감지할 수 있도록 도와줍니다. 이벤트 클래스는 보통 `app/Events` 디렉토리에, 해당 이벤트를 감지하는 리스너들은 `app/Listeners` 디렉토리에 위치합니다. 만약 이 디렉토리가 아직 없다면 걱정하지 마십시오. Artisan 콘솔 명령어를 사용하여 이벤트와 리스너를 생성하는 과정에서 자동으로 만들어집니다.

이벤트는 애플리케이션의 다양한 부분을 서로 분리(decouple)하는 데 탁월한 방법입니다. 하나의 이벤트가 여러 리스너에 의해 감지될 수 있으며, 이 리스너들끼리는 서로의 존재를 알 필요가 없습니다. 예를 들어, 주문이 발송될 때마다 사용자에게 Slack 알림을 보내고 싶다고 가정해봅시다. 주문 처리 코드를 Slack 알림 코드와 직접 연결하지 않고, `App\Events\OrderShipped` 이벤트를 발생시키면, 해당 이벤트를 감지하는 리스너에서 Slack 알림을 전송할 수 있습니다.

<a name="generating-events-and-listeners"></a>
## 이벤트 및 리스너 생성

이벤트와 리스너를 빠르게 생성하려면 `make:event` 및 `make:listener` Artisan 명령어를 사용하면 됩니다:

```shell
php artisan make:event PodcastProcessed

php artisan make:listener SendPodcastNotification --event=PodcastProcessed
```

또한 `make:event` 및 `make:listener` 명령어를 추가 인수 없이 실행할 수도 있습니다. 이 경우 Laravel이 클래스 이름(그리고 리스너 생성 시 리스너가 감지할 이벤트)을 입력하라고 자동으로 안내합니다:

```shell
php artisan make:event

php artisan make:listener
```

<a name="registering-events-and-listeners"></a>
## 이벤트 및 리스너 등록

<a name="event-discovery"></a>
### 이벤트 자동 탐지

기본적으로 Laravel은 애플리케이션의 `Listeners` 디렉토리를 스캔하여 이벤트 리스너를 자동으로 찾고 등록합니다. Laravel은 `handle` 또는 `__invoke`로 시작하는 리스너 클래스의 메서드를 찾아, 해당 메서드의 시그니처에 타입힌트된 이벤트에 대한 이벤트 리스너로 등록합니다:

```php
use App\Events\PodcastProcessed;

class SendPodcastNotification
{
    /**
     * Handle the event.
     */
    public function handle(PodcastProcessed $event): void
    {
        // ...
    }
}
```

PHP의 유니언 타입을 사용하여 여러 이벤트를 감지할 수도 있습니다:

```php
/**
 * Handle the event.
 */
public function handle(PodcastProcessed|PodcastPublished $event): void
{
    // ...
}
```

리스너를 다른 디렉토리 또는 여러 디렉토리에 저장하고자 한다면, 애플리케이션의 `bootstrap/app.php` 파일에서 `withEvents` 메서드를 사용하여 탐지할 디렉토리를 지정할 수 있습니다:

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/Orders/Listeners',
])
```

`*` 문자를 와일드카드로 사용하여 비슷한 여러 디렉토리를 동시에 탐지할 수도 있습니다:

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/*/Listeners',
])
```

애플리케이션에 등록된 모든 리스너 목록을 확인하려면 `event:list` 명령어를 사용할 수 있습니다:

```shell
php artisan event:list
```

<a name="event-discovery-in-production"></a>
#### 프로덕션 환경에서의 이벤트 자동 탐지

애플리케이션의 성능을 높이기 위해, `optimize` 또는 `event:cache` Artisan 명령어를 사용하여 모든 이벤트 리스너의 매니페스트를 캐시해야 합니다. 이 명령은 보통 애플리케이션의 [배포 프로세스](/docs/12.x/deployment#optimization) 일부로 실행되어야 합니다. 생성된 매니페스트는 프레임워크가 이벤트 등록을 더 빠르게 수행하도록 도와줍니다. 이벤트 캐시를 삭제하려면 `event:clear` 명령어를 사용할 수 있습니다.

<a name="manually-registering-events"></a>
### 이벤트 수동 등록

`Event` 파사드를 사용하면 애플리케이션의 `AppServiceProvider`의 `boot` 메서드 내에서 이벤트와 해당 리스너를 수동으로 등록할 수 있습니다:

```php
use App\Domain\Orders\Events\PodcastProcessed;
use App\Domain\Orders\Listeners\SendPodcastNotification;
use Illuminate\Support\Facades\Event;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Event::listen(
        PodcastProcessed::class,
        SendPodcastNotification::class,
    );
}
```

애플리케이션에 등록된 모든 리스너의 목록은 다음 명령어로 확인할 수 있습니다:

```shell
php artisan event:list
```

<a name="closure-listeners"></a>
### 클로저 리스너

일반적으로 리스너는 클래스 형태로 정의하지만, 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 클로저 기반 이벤트 리스너를 직접 등록할 수도 있습니다:

```php
use App\Events\PodcastProcessed;
use Illuminate\Support\Facades\Event;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Event::listen(function (PodcastProcessed $event) {
        // ...
    });
}
```

<a name="queuable-anonymous-event-listeners"></a>
#### 큐에 넣을 수 있는 익명 이벤트 리스너

클로저 기반 이벤트 리스너를 등록할 때 `Illuminate\Events\queueable` 함수를 사용하여 리스너 클로저를 감싸면, Laravel이 해당 리스너를 [큐](/docs/12.x/queues)에서 실행하도록 지정할 수 있습니다:

```php
use App\Events\PodcastProcessed;
use function Illuminate\Events\queueable;
use Illuminate\Support\Facades\Event;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Event::listen(queueable(function (PodcastProcessed $event) {
        // ...
    }));
}
```

큐에 넣는 작업처럼, `onConnection`, `onQueue`, `delay` 메서드를 사용하여 큐 리스너의 동작을 세부적으로 조정할 수 있습니다:

```php
Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->onConnection('redis')->onQueue('podcasts')->delay(now()->addSeconds(10)));
```

익명 큐 리스너의 실패를 처리하고 싶다면, `queueable` 리스너 정의 시 `catch` 메서드에 클로저를 전달할 수 있습니다. 이 클로저는 이벤트 인스턴스와 리스너 실패를 일으킨 `Throwable` 인스턴스를 인수로 받습니다:

```php
use App\Events\PodcastProcessed;
use function Illuminate\Events\queueable;
use Illuminate\Support\Facades\Event;
use Throwable;

Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->catch(function (PodcastProcessed $event, Throwable $e) {
    // The queued listener failed...
}));
```

<a name="wildcard-event-listeners"></a>
#### 와일드카드 이벤트 리스너

`*`를 와일드카드 매개변수로 사용하여 여러 이벤트를 한 리스너에서 감지하도록 등록할 수도 있습니다. 와일드카드 리스너는 첫 번째 인수로 이벤트 이름을, 두 번째 인수로 전체 이벤트 데이터 배열을 받습니다:

```php
Event::listen('event.*', function (string $eventName, array $data) {
    // ...
});
```

<a name="defining-events"></a>
## 이벤트 정의

이벤트 클래스는 해당 이벤트와 관련된 정보를 보관하는 데이터 컨테이너 역할을 합니다. 예를 들어, `App\Events\OrderShipped` 이벤트가 [Eloquent ORM](/docs/12.x/eloquent) 객체를 전달받는다고 가정해보겠습니다:

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
     * Create a new event instance.
     */
    public function __construct(
        public Order $order,
    ) {}
}
```

보시다시피, 이 이벤트 클래스는 별다른 로직 없이 단지 구매된 `App\Models\Order` 인스턴스를 담고 있습니다. 이벤트에서 사용하는 `SerializesModels` 트레이트는 이벤트 객체가 PHP의 `serialize` 함수로 직렬화될 때([큐 리스너](#queued-event-listeners) 등에서) Eloquent 모델을 적절하게 직렬화해줍니다.

<a name="defining-listeners"></a>
## 리스너 정의

이제 예시 이벤트의 리스너를 살펴보겠습니다. 이벤트 리스너는 `handle` 메서드로 이벤트 인스턴스를 전달받습니다. `make:listener` Artisan 명령어를 `--event` 옵션과 함께 실행하면, 알맞은 이벤트 클래스를 자동으로 임포트하고, `handle` 메서드에 타입힌트까지 추가해줍니다. `handle` 메서드에서는 이벤트에 반응하여 필요한 작업을 수행하면 됩니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;

class SendShipmentNotification
{
    /**
     * Create the event listener.
     */
    public function __construct() {}

    /**
     * Handle the event.
     */
    public function handle(OrderShipped $event): void
    {
        // Access the order using $event->order...
    }
}
```

> [!NOTE]
> 이벤트 리스너의 생성자에서 필요한 의존성을 타입힌트로 지정할 수도 있습니다. 모든 이벤트 리스너는 Laravel [서비스 컨테이너](/docs/12.x/container)에서 해석되므로, 자동으로 의존성 주입이 이루어집니다.

<a name="stopping-the-propagation-of-an-event"></a>
#### 이벤트 전파 중지

특정 상황에서 이벤트가 다른 리스너로 전파되는 것을 중단하고 싶을 수도 있습니다. 이럴 때는 리스너의 `handle` 메서드에서 `false`를 반환하면 됩니다.

<a name="queued-event-listeners"></a>
## 큐잉된 이벤트 리스너

이메일 발송이나 HTTP 요청처럼 시간이 오래 걸리는 작업을 리스너에서 처리해야 한다면, 해당 리스너를 큐에 넣어 비동기로 실행하는 것이 좋습니다. 큐잉된 리스너를 사용하기 전에 반드시 [큐를 설정](/docs/12.x/queues)하고, 서버나 개발 환경에서 큐 워커를 실행하세요.

리스너를 큐에 넣으려면, 리스너 클래스에 `ShouldQueue` 인터페이스를 추가하면 됩니다. `make:listener` Artisan 명령어로 생성된 리스너에는 이미 이 인터페이스가 임포트되어 있으므로 바로 사용할 수 있습니다:

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

이제 해당 리스너가 감지하는 이벤트가 디스패치될 때마다, Laravel의 [큐 시스템](/docs/12.x/queues)을 통해 리스너가 자동으로 큐에 포함됩니다. 리스너 실행 중 예외가 발생하지 않으면, 큐 작업은 처리 후 자동으로 삭제됩니다.

<a name="customizing-the-queue-connection-queue-name"></a>
#### 큐 커넥션, 큐 이름, 지연 시간 설정

리스너 클래스에서 `$connection`, `$queue`, `$delay` 프로퍼티를 정의하여 큐 커넥션, 큐 이름, 지연 시간(초 단위)을 커스터마이징할 수 있습니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    /**
     * The name of the connection the job should be sent to.
     *
     * @var string|null
     */
    public $connection = 'sqs';

    /**
     * The name of the queue the job should be sent to.
     *
     * @var string|null
     */
    public $queue = 'listeners';

    /**
     * The time (seconds) before the job should be processed.
     *
     * @var int
     */
    public $delay = 60;
}
```

런타임에 큐 연결, 큐 이름, 지연 시간을 동적으로 설정하고 싶다면, `viaConnection`, `viaQueue`, `withDelay` 메서드를 정의하면 됩니다:

```php
/**
 * Get the name of the listener's queue connection.
 */
public function viaConnection(): string
{
    return 'sqs';
}

/**
 * Get the name of the listener's queue.
 */
public function viaQueue(): string
{
    return 'listeners';
}

/**
 * Get the number of seconds before the job should be processed.
 */
public function withDelay(OrderShipped $event): int
{
    return $event->highPriority ? 0 : 60;
}
```

<a name="conditionally-queueing-listeners"></a>
#### 조건부 큐 리스너

실행 시점에만 알 수 있는 특정 데이터에 따라 리스너를 큐에 넣을지 결정해야 할 때가 있습니다. 이럴 때는 리스너에 `shouldQueue` 메서드를 정의하면 됩니다. 이 메서드가 `false`를 반환하면 리스너는 큐에 들어가지 않습니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderCreated;
use Illuminate\Contracts\Queue\ShouldQueue;

class RewardGiftCard implements ShouldQueue
{
    /**
     * Reward a gift card to the customer.
     */
    public function handle(OrderCreated $event): void
    {
        // ...
    }

    /**
     * Determine whether the listener should be queued.
     */
    public function shouldQueue(OrderCreated $event): bool
    {
        return $event->order->subtotal >= 5000;
    }
}
```

<a name="manually-interacting-with-the-queue"></a>
### 큐 수동 조작

리스너의 내부 큐 작업 객체의 `delete` 또는 `release` 메서드를 직접 다뤄야 하는 경우, `Illuminate\Queue\InteractsWithQueue` 트레이트를 사용하면 됩니다. 이 트레이트는 기본적으로 자동 생성되는 리스너에서 임포트되어 있으며, 다음과 같이 사용할 수 있습니다:

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
     * Handle the event.
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
### 데이터베이스 트랜잭션과 큐잉된 이벤트 리스너

큐잉된 리스너가 데이터베이스 트랜잭션 내에서 디스패치될 경우, 트랜잭션이 커밋되기 전에 큐에서 작업이 처리될 수도 있습니다. 이 경우, 트랜잭션 과정에서 모델이나 데이터베이스 레코드에 대한 변경이 아직 커밋되지 않은 상태일 수 있으며, 새로 생성된 레코드가 실제로 DB에 존재하지 않을 수도 있습니다. 리스너에서 이를 참조하면 예기치 않은 오류가 발생할 수 있습니다.

만약 큐 커넥션의 `after_commit` 설정이 `false`일 경우에도, 특정 리스너만이라도 DB 트랜잭션이 커밋된 후 실행되도록 하고 싶다면, 리스너 클래스에 `ShouldQueueAfterCommit` 인터페이스를 구현할 수 있습니다:

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
> 이런 종류의 이슈에 대해 더 자세히 알고 싶다면, [큐 작업과 데이터베이스 트랜잭션](/docs/12.x/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="queued-listener-middleware"></a>
### 큐 리스너 미들웨어

큐잉된 리스너에서도 [작업 미들웨어](/docs/12.x/queues#job-middleware)를 사용할 수 있습니다. 작업 미들웨어를 통해 리스너 실행 전후에 커스텀 로직을 래핑할 수 있으며, 리스너 내부의 보일러플레이트를 줄여줍니다. 생성한 작업 미들웨어는 리스너의 `middleware` 메서드에서 반환하여 적용할 수 있습니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use App\Jobs\Middleware\RateLimited;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    /**
     * Handle the event.
     */
    public function handle(OrderShipped $event): void
    {
        // Process the event...
    }

    /**
     * Get the middleware the listener should pass through.
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
#### 암호화된 큐 리스너

Laravel은 [암호화](/docs/12.x/encryption)를 통해 큐잉된 리스너의 데이터의 기밀성과 무결성을 보장할 수 있습니다. 사용 방법은 리스너 클래스에 `ShouldBeEncrypted` 인터페이스만 추가하면 됩니다. 이 인터페이스를 추가하면, 해당 리스너가 큐에 들어가기 전에 Laravel이 자동으로 암호화합니다:

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

큐잉된 이벤트 리스너가 실패하는 경우도 있습니다. 리스너가 큐 워커에서 지정한 최대 시도 횟수를 초과하면, `failed` 메서드가 호출됩니다. 이 메서드는 이벤트 인스턴스와 실패를 발생시킨 `Throwable`을 인수로 전달받습니다:

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
     * Handle the event.
     */
    public function handle(OrderShipped $event): void
    {
        // ...
    }

    /**
     * Handle a job failure.
     */
    public function failed(OrderShipped $event, Throwable $exception): void
    {
        // ...
    }
}
```

<a name="specifying-queued-listener-maximum-attempts"></a>
#### 큐 리스너 최대 시도 횟수 지정

큐잉된 리스너가 에러를 만났을 때 무한히 재시도되는 것을 원치 않는 경우가 많습니다. 따라서 Laravel은 시도 횟수나 시도 시간을 제한하는 다양한 방법을 제공합니다.

리스너 클래스에 `tries` 프로퍼티를 정의하여, 특정 횟수만큼만 시도하도록 할 수 있습니다:

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
     * The number of times the queued listener may be attempted.
     *
     * @var int
     */
    public $tries = 5;
}
```

이와 달리, 리스너가 시도될 수 있는 최대 시간을 지정할 수도 있습니다. 이 방법을 사용하면, 주어진 시간 안에서는 재시도 횟수에 상관없이 계속 시도됩니다. 만료 시간을 지정하려면 `retryUntil` 메서드를 리스너에 추가하면 되며, 이 메서드는 `DateTime` 인스턴스를 반환해야 합니다:

```php
use DateTime;

/**
 * Determine the time at which the listener should timeout.
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(5);
}
```

`retryUntil`과 `tries`를 모두 지정하면, Laravel은 `retryUntil` 우선으로 판단합니다.

<a name="specifying-queued-listener-backoff"></a>
#### 큐 리스너 백오프(재시도 지연) 지정

큐잉된 리스너가 예외로 인해 재시도될 때, Laravel이 다음 시도까지 얼마나 대기해야 하는지 지정하려면, `backoff` 프로퍼티를 사용할 수 있습니다:

```php
/**
 * The number of seconds to wait before retrying the queued listener.
 *
 * @var int
 */
public $backoff = 3;
```

더 복잡한 재시도 지연 로직이 필요하다면, `backoff` 메서드를 리스너에 정의할 수 있습니다:

```php
/**
 * Calculate the number of seconds to wait before retrying the queued listener.
 */
public function backoff(OrderShipped $event): int
{
    return 3;
}
```

배열을 반환해서 "지수형(Exponential)" 백오프도 쉽게 구성할 수 있습니다. 아래 예시에서, 첫 번째 재시도엔 1초, 두 번째엔 5초, 세 번째 및 이후에는 각각 10초씩 대기하게 됩니다:

```php
/**
 * Calculate the number of seconds to wait before retrying the queued listener.
 *
 * @return list<int>
 */
public function backoff(OrderShipped $event): array
{
    return [1, 5, 10];
}
```

<a name="specifying-queued-listener-max-exceptions"></a>
#### 큐 리스너 최대 예외 발생 횟수 지정

경우에 따라선 큐잉된 리스너가 여러 번 시도는 가능하지만, 일정 횟수 이상 미처리된 예외가 발생하면 실패로 처리하고 싶은 경우가 있습니다. 이럴 때는 `maxExceptions` 프로퍼티를 리스너 클래스에 정의합니다:

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
     * The number of times the queued listener may be attempted.
     *
     * @var int
     */
    public $tries = 25;

    /**
     * The maximum number of unhandled exceptions to allow before failing.
     *
     * @var int
     */
    public $maxExceptions = 3;

    /**
     * Handle the event.
     */
    public function handle(OrderShipped $event): void
    {
        // Process the event...
    }
}
```

위 예시에서 리스너는 최대 25회까지 재시도될 수 있지만, 미처리 예외가 3번 이상 발생하면 바로 실패 처리됩니다.

<a name="specifying-queued-listener-timeout"></a>
#### 큐 리스너 처리 시간 제한 지정

큐잉된 리스너가 대략 어느 정도의 시간이 소요될지 예상될 때, 타임아웃을 설정해야 할 수 있습니다. 리스너의 처리 시간이 타임아웃 값을 초과하면, 해당 리스너를 실행 중인 워커가 에러와 함께 종료됩니다. 리스너 클래스에 `timeout` 프로퍼티를 지정하여 최대 실행 시간을 지정할 수 있습니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    /**
     * The number of seconds the listener can run before timing out.
     *
     * @var int
     */
    public $timeout = 120;
}
```

타임아웃이 발생했을 때 해당 리스너를 실패로 처리하고 싶다면, `failOnTimeout` 프로퍼티를 정의하면 됩니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    /**
     * Indicate if the listener should be marked as failed on timeout.
     *
     * @var bool
     */
    public $failOnTimeout = true;
}
```

<a name="dispatching-events"></a>
## 이벤트 디스패치

이벤트를 발생시키려면, 해당 이벤트의 `dispatch` 정적 메서드를 호출하면 됩니다. 이 메서드는 `Illuminate\Foundation\Events\Dispatchable` 트레이트에 의해 이벤트에 추가되어 있습니다. `dispatch` 메서드에 전달한 모든 인수는 이벤트의 생성자로 전달됩니다:

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
     * Ship the given order.
     */
    public function store(Request $request): RedirectResponse
    {
        $order = Order::findOrFail($request->order_id);

        // Order shipment logic...

        OrderShipped::dispatch($order);

        return redirect('/orders');
    }
}
```

특정 조건에 따라 이벤트를 발생시키고 싶다면 `dispatchIf`나 `dispatchUnless` 메서드를 사용할 수 있습니다:

```php
OrderShipped::dispatchIf($condition, $order);

OrderShipped::dispatchUnless($condition, $order);
```

> [!NOTE]
> 테스트할 때는 실제 리스너가 실행되지 않고 이벤트 발생만 검증할 수 있습니다. Laravel의 [테스트 헬퍼](#testing)를 활용해 간편하게 검증할 수 있습니다.

<a name="dispatching-events-after-database-transactions"></a>
### 데이터베이스 트랜잭션 후 이벤트 디스패치

특정 상황에서는 이벤트를 현재 진행 중인 데이터베이스 트랜잭션이 커밋된 뒤에만 발생시키고 싶은 경우가 있습니다. 이럴 때는 이벤트 클래스에 `ShouldDispatchAfterCommit` 인터페이스를 구현하면 됩니다.

이 인터페이스는, 현재 트랜잭션이 커밋되기 전까지 이벤트가 디스패치되지 않도록 지시합니다. 트랜잭션이 실패하면, 해당 이벤트는 버려집니다. 만약 이벤트 발생 시 트랜잭션이 없었다면 즉시 이벤트가 디스패치됩니다:

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
     * Create a new event instance.
     */
    public function __construct(
        public Order $order,
    ) {}
}
```

<a name="deferring-events"></a>
### 이벤트 지연 실행

이벤트 지연(Deferred Events)을 사용하면 특정 코드 블록이 모두 실행된 후, 모델 이벤트 발생 및 리스너 실행을 나중으로 미룰 수 있습니다. 이 기능은 서로 관련된 레코드가 모두 생성된 다음에 이벤트 리스너가 실행되게 하려는 경우에 특히 유용합니다.

이벤트를 지연시키려면, `Event::defer()` 메서드에 클로저를 전달하면 됩니다:

```php
use App\Models\User;
use Illuminate\Support\Facades/Event;

Event::defer(function () {
    $user = User::create(['name' => 'Victoria Otwell']);

    $user->posts()->create(['title' => 'My first post!']);
});
```

클로저 내부에서 발생한 모든 이벤트는 클로저 실행이 끝난 뒤에 디스패치됩니다. 이를 통해 이벤트 리스너에서 클로저 내에서 생성된 모든 관계 레코드에 접근할 수 있습니다. 만약 클로저 내부에서 예외가 발생하면, 지연된 이벤트는 발생되지 않습니다.

특정 이벤트만 지연시키고 싶다면, `defer` 메서드의 두 번째 인수로 이벤트 배열을 전달할 수 있습니다:

```php
use App\Models\User;
use Illuminate\Support\Facades/Event;

Event::defer(function () {
    $user = User::create(['name' => 'Victoria Otwell']);

    $user->posts()->create(['title' => 'My first post!']);
}, ['eloquent.created: '.User::class]);
```

<a name="event-subscribers"></a>
## 이벤트 구독자

<a name="writing-event-subscribers"></a>
### 이벤트 구독자 작성

이벤트 구독자(Subscriber)는 하나의 클래스 내에서 여러 이벤트를 구독할 수 있으며, 다양한 이벤트에 대한 핸들러를 한 곳에 정의할 수 있습니다. 구독자 클래스는 반드시 `subscribe` 메서드를 정의해야 하며, 이 메서드는 이벤트 디스패처 인스턴스를 인수로 받습니다. 전달받은 디스패처의 `listen` 메서드를 호출하여 이벤트 리스너를 등록할 수 있습니다:

```php
<?php

namespace App\Listeners;

use Illuminate\Auth\Events\Login;
use Illuminate\Auth\Events\Logout;
use Illuminate\Events\Dispatcher;

class UserEventSubscriber
{
    /**
     * Handle user login events.
     */
    public function handleUserLogin(Login $event): void {}

    /**
     * Handle user logout events.
     */
    public function handleUserLogout(Logout $event): void {}

    /**
     * Register the listeners for the subscriber.
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

구독자 자신 내부에 이벤트 리스너 메서드가 정의되어 있다면, `subscribe` 메서드에서 이벤트와 메서드명을 배열로 반환하여 더욱 간결하게 등록할 수 있습니다. Laravel은 리스너 등록 시 구독자의 클래스명을 자동으로 판단합니다:

```php
<?php

namespace App\Listeners;

use Illuminate\Auth\Events\Login;
use Illuminate\Auth\Events\Logout;
use Illuminate\Events\Dispatcher;

class UserEventSubscriber
{
    /**
     * Handle user login events.
     */
    public function handleUserLogin(Login $event): void {}

    /**
     * Handle user logout events.
     */
    public function handleUserLogout(Logout $event): void {}

    /**
     * Register the listeners for the subscriber.
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
### 이벤트 구독자 등록

구독자를 작성한 후, 구독자 내부의 핸들러 메서드가 Laravel의 [이벤트 자동 탐지 규칙](#event-discovery)을 따른다면, Laravel이 이를 자동으로 등록합니다. 그렇지 않을 경우에는 `Event` 파사드의 `subscribe` 메서드를 사용하여 구독자를 수동으로 등록할 수 있습니다. 보통 이 작업은 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 수행합니다:

```php
<?php

namespace App\Providers;

use App\Listeners\UserEventSubscriber;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Event::subscribe(UserEventSubscriber::class);
    }
}
```

<a name="testing"></a>
## 테스트

이벤트를 디스패치하는 코드를 테스트할 때, 실제로 이벤트 리스너가 실행되는 것을 원하지 않을 수도 있습니다. 리스너의 로직은 별도로 테스트할 수 있기 때문입니다. 물론 리스너 자체를 테스트하고 싶다면, 리스너 인스턴스를 직접 생성해서 `handle` 메서드를 호출하면 됩니다.

`Event` 파사드의 `fake` 메서드를 활용하면, 리스너의 실제 실행을 막은 뒤 테스트 대상 코드를 실행하고, `assertDispatched`, `assertNotDispatched`, `assertNothingDispatched` 메서드로 어떤 이벤트가 발생했는지 검증할 수 있습니다:

```php tab=Pest
<?php

use App\Events\OrderFailedToShip;
use App\Events\OrderShipped;
use Illuminate\Support\Facades/Event;

test('orders can be shipped', function () {
    Event::fake();

    // Perform order shipping...

    // Assert that an event was dispatched...
    Event::assertDispatched(OrderShipped::class);

    // Assert an event was dispatched twice...
    Event::assertDispatched(OrderShipped::class, 2);

    // Assert an event was dispatched once...
    Event::assertDispatchedOnce(OrderShipped::class);

    // Assert an event was not dispatched...
    Event::assertNotDispatched(OrderFailedToShip::class);

    // Assert that no events were dispatched...
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
     * Test order shipping.
     */
    public function test_orders_can_be_shipped(): void
    {
        Event::fake();

        // Perform order shipping...

        // Assert that an event was dispatched...
        Event::assertDispatched(OrderShipped::class);

        // Assert an event was dispatched twice...
        Event::assertDispatched(OrderShipped::class, 2);

        // Assert an event was dispatched once...
        Event::assertDispatchedOnce(OrderShipped::class);

        // Assert an event was not dispatched...
        Event::assertNotDispatched(OrderFailedToShip::class);

        // Assert that no events were dispatched...
        Event::assertNothingDispatched();
    }
}
```

특정 조건을 만족하는 이벤트가 발생했는지 검증하고 싶다면, `assertDispatched` 또는 `assertNotDispatched` 메서드에 클로저를 전달할 수 있습니다. 한 번이라도 조건을 충족하는 이벤트가 발생했으면 이 검증은 통과합니다:

```php
Event::assertDispatched(function (OrderShipped $event) use ($order) {
    return $event->order->id === $order->id;
});
```

특정 리스너가 특정 이벤트를 감지하고 있는지만 검증하고 싶다면, `assertListening` 메서드를 사용할 수 있습니다:

```php
Event::assertListening(
    OrderShipped::class,
    SendShipmentNotification::class
);
```

> [!WARNING]
> `Event::fake()` 호출 이후에는 이벤트 리스너가 실행되지 않습니다. 따라서, UUID 같은 이벤트 기반 데이터 생성을 사용하는 모델 팩토리를 테스트할 때는, 팩토리 사용 이후에 `Event::fake()`를 호출해야 합니다.

<a name="faking-a-subset-of-events"></a>
### 일부 이벤트만 페이크 처리

특정 이벤트만 리스너가 실행되지 않도록 페이크하고 싶다면, 해당 이벤트를 `fake` 또는 `fakeFor` 메서드에 배열로 전달할 수 있습니다:

```php tab=Pest
test('orders can be processed', function () {
    Event::fake([
        OrderCreated::class,
    ]);

    $order = Order::factory()->create();

    Event::assertDispatched(OrderCreated::class);

    // Other events are dispatched as normal...
    $order->update([
        // ...
    ]);
});
```

```php tab=PHPUnit
/**
 * Test order process.
 */
public function test_orders_can_be_processed(): void
{
    Event::fake([
        OrderCreated::class,
    ]);

    $order = Order::factory()->create();

    Event::assertDispatched(OrderCreated::class);

    // Other events are dispatched as normal...
    $order->update([
        // ...
    ]);
}
```

특정 이벤트만 제외하고 나머지 모든 이벤트를 페이크하고 싶다면, `except` 메서드를 사용할 수 있습니다:

```php
Event::fake()->except([
    OrderCreated::class,
]);
```

<a name="scoped-event-fakes"></a>
### 스코프 단위 이벤트 페이크

테스트의 특정 부분에서만 이벤트 리스너를 페이크하고 싶다면, `fakeFor` 메서드를 사용할 수 있습니다:

```php tab=Pest
<?php

use App\Events\OrderCreated;
use App\Models\Order;
use Illuminate\Support\Facades/Event;

test('orders can be processed', function () {
    $order = Event::fakeFor(function () {
        $order = Order::factory()->create();

        Event::assertDispatched(OrderCreated::class);

        return $order;
    });

    // Events are dispatched as normal and observers will run...
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
     * Test order process.
     */
    public function test_orders_can_be_processed(): void
    {
        $order = Event::fakeFor(function () {
            $order = Order::factory()->create();

            Event::assertDispatched(OrderCreated::class);

            return $order;
        });

        // Events are dispatched as normal and observers will run...
        $order->update([
            // ...
        ]);
    }
}
```
