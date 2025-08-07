# 이벤트 (Events)

- [소개](#introduction)
- [이벤트 및 리스너 생성](#generating-events-and-listeners)
- [이벤트 및 리스너 등록](#registering-events-and-listeners)
    - [이벤트 자동 검색](#event-discovery)
    - [이벤트 수동 등록](#manually-registering-events)
    - [클로저 리스너](#closure-listeners)
- [이벤트 정의](#defining-events)
- [리스너 정의](#defining-listeners)
- [큐잉된 이벤트 리스너](#queued-event-listeners)
    - [큐와의 수동 상호작용](#manually-interacting-with-the-queue)
    - [큐잉된 이벤트 리스너와 데이터베이스 트랜잭션](#queued-event-listeners-and-database-transactions)
    - [큐 리스너 미들웨어](#queued-listener-middleware)
    - [암호화된 큐 리스너](#encrypted-queued-listeners)
    - [실패한 작업 처리](#handling-failed-jobs)
- [이벤트 디스패치](#dispatching-events)
    - [데이터베이스 트랜잭션 후 이벤트 디스패치](#dispatching-events-after-database-transactions)
    - [이벤트 지연(Defer)](#deferring-events)
- [이벤트 구독자](#event-subscribers)
    - [이벤트 구독자 작성](#writing-event-subscribers)
    - [이벤트 구독자 등록](#registering-event-subscribers)
- [테스트](#testing)
    - [특정 이벤트만 페이크 처리](#faking-a-subset-of-events)
    - [스코프 이벤트 페이크](#scoped-event-fakes)

<a name="introduction"></a>
## 소개

Laravel의 이벤트는 간단한 옵저버 패턴(observer pattern) 구현을 제공하여, 애플리케이션 내에서 발생하는 다양한 이벤트를 구독하고 들을(listen) 수 있게 해줍니다. 일반적으로 이벤트 클래스는 `app/Events` 디렉터리에, 해당 이벤트의 리스너(listener)는 `app/Listeners` 디렉터리에 저장됩니다. 만약 애플리케이션에 이 디렉터리가 없다면, Artisan 콘솔 명령어로 이벤트와 리스너를 생성할 때 자동으로 만들어집니다.

이벤트는 애플리케이션의 여러 부분을 느슨하게 결합하는(decouple) 훌륭한 방법입니다. 하나의 이벤트에 여러 리스너를 등록할 수 있지만, 각각의 리스너는 서로에게 직접적으로 의존하지 않습니다. 예를 들어, 주문이 발송될 때마다 사용자에게 Slack 알림을 보내고 싶을 수 있습니다. 이때 주문 처리 코드와 Slack 알림 코드를 서로 결합하지 않고, `App\Events\OrderShipped` 이벤트를 발생시키면, 리스너가 이 이벤트를 받아서 Slack 알림을 전송할 수 있습니다.

<a name="generating-events-and-listeners"></a>
## 이벤트 및 리스너 생성

이벤트 및 리스너를 빠르게 생성하려면 `make:event` 및 `make:listener` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan make:event PodcastProcessed

php artisan make:listener SendPodcastNotification --event=PodcastProcessed
```

더 간편하게 명령어에 추가 인수를 전달하지 않고도 이벤트 및 리스너를 생성할 수 있습니다. 이 경우 Laravel이 클래스를 생성할 때 클래스명(리스너의 경우, 어떤 이벤트를 들을 것인지)도 자동으로 입력받게 됩니다.

```shell
php artisan make:event

php artisan make:listener
```

<a name="registering-events-and-listeners"></a>
## 이벤트 및 리스너 등록

<a name="event-discovery"></a>
### 이벤트 자동 검색

Laravel은 기본적으로 애플리케이션의 `Listeners` 디렉터리를 스캔하여 이벤트 리스너를 자동으로 찾아 등록합니다. Laravel이 `handle` 또는 `__invoke`로 시작하는 리스너 클래스의 메서드를 찾으면, 해당 메서드에 타입힌트로 명시된 이벤트를 자동으로 리스너로 등록합니다.

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

PHP의 유니언 타입을 이용해 여러 이벤트를 한 번에 들을 수도 있습니다.

```php
/**
 * Handle the event.
 */
public function handle(PodcastProcessed|PodcastPublished $event): void
{
    // ...
}
```

리스너를 다른 디렉터리 또는 여러 디렉터리에 저장하려는 경우, 애플리케이션의 `bootstrap/app.php` 파일에서 `withEvents` 메서드를 사용해 Laravel이 해당 디렉터리도 스캔하도록 지시할 수 있습니다.

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/Orders/Listeners',
])
```

`*`를 사용하면 여러 비슷한 경로를 한 번에 스캔할 수도 있습니다.

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/*/Listeners',
])
```

현재 애플리케이션에 등록된 모든 리스너 목록을 보려면 `event:list` 명령어를 사용할 수 있습니다.

```shell
php artisan event:list
```

<a name="event-discovery-in-production"></a>
#### 운영 환경에서의 이벤트 자동 검색

애플리케이션의 성능을 높이려면, `optimize` 또는 `event:cache` Artisan 명령어를 사용해 모든 리스너의 매니페스트(manifest)를 캐시해야 합니다. 일반적으로 이 명령은 애플리케이션의 [배포 과정](/docs/12.x/deployment#optimization) 중에 실행합니다. 이 매니페스트 파일은 프레임워크에서 이벤트 등록 속도를 높이기 위해 사용합니다. `event:clear` 명령어로 이벤트 캐시를 삭제할 수 있습니다.

<a name="manually-registering-events"></a>
### 이벤트 수동 등록

`Event` 파사드를 사용하여, 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드에서 직접 이벤트와 리스너를 등록할 수 있습니다.

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

현재 등록된 모든 리스너 목록 역시 아래 명령어로 확인 가능합니다.

```shell
php artisan event:list
```

<a name="closure-listeners"></a>
### 클로저 리스너

대부분의 경우 리스너는 클래스로 정의하지만, `AppServiceProvider`의 `boot` 메서드에서 클로저(익명 함수) 기반 이벤트 리스너를 직접 등록할 수도 있습니다.

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
#### 큐잉 가능한(Queueable) 익명 이벤트 리스너

클로저 기반 이벤트 리스너를 등록할 때, 해당 리스너 클로저를 `Illuminate\Events\queueable` 함수로 감싸면 Laravel이 이 리스너를 [큐](/docs/12.x/queues)에서 실행하도록 할 수 있습니다.

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

일반 큐 작업(잡, job)과 마찬가지로, `onConnection`, `onQueue`, `delay` 메서드를 사용해 리스너가 실행될 큐의 커넥션, 큐 이름, 지연 시간을 설정할 수 있습니다.

```php
Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->onConnection('redis')->onQueue('podcasts')->delay(now()->addSeconds(10)));
```

익명 큐 리스너의 실패를 처리하고 싶다면, `queueable` 리스너 정의 시 `catch` 메서드에 클로저를 전달할 수 있습니다. 이 클로저는 이벤트 인스턴스와 리스너 실패를 일으킨 `Throwable` 인스턴스를 받습니다.

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

`*` 문자를 와일드카드 매개변수로 사용하여 여러 이벤트를 한 리스너에서 받을 수도 있습니다. 와일드카드 리스너는 첫 번째 인수로 이벤트 이름, 두 번째 인수로 전체 이벤트 데이터 배열을 받습니다.

```php
Event::listen('event.*', function (string $eventName, array $data) {
    // ...
});
```

<a name="defining-events"></a>
## 이벤트 정의

이벤트 클래스는 기본적으로 이벤트와 관련된 정보를 담고 있는 데이터 컨테이너입니다. 예를 들어 `App\Events\OrderShipped` 이벤트가 [Eloquent ORM](/docs/12.x/eloquent) 객체를 받는다고 가정해보겠습니다.

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

위와 같이, 이 이벤트 클래스에는 별도의 로직이 없습니다. 단지 구매된 `App\Models\Order` 인스턴스를 담고 있습니다. 이벤트에서 사용하는 `SerializesModels` 트레이트는 PHP의 `serialize` 함수를 통해 객체가 직렬화될 때(예: [큐잉된 리스너](#queued-event-listeners)에서) Eloquent 모델을 적절하게 직렬화해줍니다.

<a name="defining-listeners"></a>
## 리스너 정의

다음은 예제 이벤트의 리스너를 살펴봅니다. 이벤트 리스너는 `handle` 메서드에서 이벤트 인스턴스를 받습니다. `--event` 옵션과 함께 `make:listener` Artisan 명령어를 실행하면, 적절한 이벤트 클래스를 자동으로 임포트하고 `handle` 메서드의 타입힌트도 지정해줍니다. 이 `handle` 메서드 안에서 이벤트에 대한 처리 작업을 수행할 수 있습니다.

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
> 이벤트 리스너의 생성자에서 필요한 의존성을 타입힌트로 지정할 수도 있습니다. 모든 이벤트 리스너는 Laravel [서비스 컨테이너](/docs/12.x/container)를 통해 해석되므로, 의존성 주입이 자동으로 이루어집니다.

<a name="stopping-the-propagation-of-an-event"></a>
#### 이벤트 전파(Propagation) 중지하기

경우에 따라 이벤트가 다른 리스너로 더 이상 전달되는 것을 중지하고 싶을 수 있습니다. 리스너의 `handle` 메서드에서 `false`를 반환하면, 그 이후의 리스너에게는 이벤트가 전달되지 않습니다.

<a name="queued-event-listeners"></a>
## 큐잉된 이벤트 리스너

리스너에서 이메일 전송, HTTP 요청 등 느린 작업을 수행한다면, 해당 리스너를 큐에 넣는 것이 좋습니다. 큐 리스너를 사용하기 전에 [큐 설정](/docs/12.x/queues)을 마치고, 서버나 로컬 개발 환경에서 큐 워커(queue worker)를 실행해야 합니다.

리스너가 큐잉되도록 하려면, 리스너 클래스에 `ShouldQueue` 인터페이스를 추가하세요. `make:listener` Artisan 명령어로 생성된 리스너는 이미 해당 인터페이스가 네임스페이스에 임포트되어 있습니다.

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

이제 이 리스너가 처리하는 이벤트가 디스패치되면, 이벤트 디스패처가 자동으로 Laravel [큐 시스템](/docs/12.x/queues)을 이용해 리스너를 큐에 넣습니다. 리스너가 예외 없이 실행되면, 해당 큐 작업은 자동으로 삭제됩니다.

<a name="customizing-the-queue-connection-queue-name"></a>
#### 큐 연결, 큐 이름, 지연 시간 커스터마이즈

큐에 사용할 연결(connection), 큐 이름, 지연 시간(seconds)을 지정하려면, 리스너 클래스에 `$connection`, `$queue`, `$delay` 속성을 정의할 수 있습니다.

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

런타임에 큐 정보 또는 지연 시간을 동적으로 지정하려면, `viaConnection`, `viaQueue`, `withDelay` 메서드를 정의해 사용할 수 있습니다.

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
#### 리스너의 큐잉 여부를 조건부로 판별

경우에 따라 런타임 데이터에 따라 리스너를 큐잉할지 여부를 판별해야 할 수 있습니다. 이를 위해 리스너에 `shouldQueue` 메서드를 추가할 수 있으며, 이 메서드가 `false`를 반환하면 해당 리스너는 큐에 적용되지 않습니다.

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
### 큐와의 수동 상호작용

리스너의 내부 큐 작업에서 큐의 `delete`, `release` 메서드를 직접 사용하려면, `Illuminate\Queue\InteractsWithQueue` 트레이트를 사용할 수 있습니다. 이 트레이트는 기본으로 생성된 리스너에 이미 포함되어 있으므로, 아래와 같이 사용할 수 있습니다.

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
### 큐잉된 이벤트 리스너와 데이터베이스 트랜잭션

큐잉된 리스너가 데이터베이스 트랜잭션 내에서 디스패치되면, 큐가 데이터베이스 트랜잭션이 커밋되기 전에 이벤트를 처리할 수 있습니다. 이 경우 트랜잭션 동안 모델이나 데이터베이스 레코드를 업데이트했더라도 커밋이 되기 전이라면 DB에 반영되지 않은 상태일 수 있습니다. 또한, 트랜잭션 내에서 생성된 모델이나 레코드는 DB에 존재하지 않을 수 있습니다. 만약 리스너에서 이러한 모델을 의존한다면, 예기치 않은 오류가 발생할 수 있습니다.

큐 연결의 `after_commit` 설정 옵션이 `false`로 되어 있더라도, 특정 큐 리스너만 트랜잭션 커밋 이후에 디스패치되도록 지정하려면 해당 리스너 클래스에 `ShouldQueueAfterCommit` 인터페이스를 구현하세요.

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
> 이러한 이슈 및 해결 방법에 대해 더 알고 싶으면 [큐 작업과 데이터베이스 트랜잭션](/docs/12.x/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="queued-listener-middleware"></a>
### 큐 리스너 미들웨어

큐잉된 리스너는 [잡 미들웨어](/docs/12.x/queues#job-middleware)도 활용할 수 있습니다. 잡 미들웨어를 통해 큐 리스너 실행 전후에 커스텀 로직을 감쌀 수 있어, 리스너 내부의 중복 코드를 줄일 수 있습니다. 잡 미들웨어는 리스너의 `middleware` 메서드에서 반환하면 연결됩니다.

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

Laravel에서는 [암호화](/docs/12.x/encryption)를 통해 큐잉된 리스너 데이터의 기밀성과 무결성을 보장할 수 있습니다. `ShouldBeEncrypted` 인터페이스를 리스너 클래스에 추가하면, Laravel은 해당 리스너를 큐에 넣기 전에 자동으로 암호화합니다.

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

큐잉된 이벤트 리스너가 실패하는 경우가 있을 수 있습니다. 리스너가 큐 워커에 정의된 최대 시도 횟수를 초과하면, 리스너의 `failed` 메서드가 호출됩니다. 이때 이벤트 인스턴스와 실패 원인이 된 `Throwable` 객체를 인수로 받습니다.

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

에러가 발생해도 리스너가 무한 반복 재시도되지 않도록, 최대 몇 번까지(또는 얼마 동안) 시도할지 지정할 수 있습니다.

리스너 클래스에서 `tries` 속성을 지정하면, 정해진 횟수만큼만 재시도합니다.

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

또는 리스너가 더 이상 시도되지 않아야 할 시간을 지정하려면, `retryUntil` 메서드를 리스너에 추가하면 됩니다. 이 메서드는 `DateTime` 인스턴스를 반환해야 합니다.

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

`retryUntil`과 `tries`가 동시에 정의되어 있으면, Laravel은 `retryUntil`을 우선 적용합니다.

<a name="specifying-queued-listener-backoff"></a>
#### 큐 리스너 백오프(Backoff) 설정

예외가 발생한 뒤 리스너를 재시도하기 전까지 대기할 시간을 지정하려면, 리스너 클래스에 `backoff` 속성을 설정합니다.

```php
/**
 * The number of seconds to wait before retrying the queued listener.
 *
 * @var int
 */
public $backoff = 3;
```

더 복잡한 백오프 로직이 필요하다면, `backoff` 메서드를 정의하세요.

```php
/**
 * Calculate the number of seconds to wait before retrying the queued listener.
 */
public function backoff(OrderShipped $event): int
{
    return 3;
}
```

배열을 반환하면 "지수 백오프" 방식으로 동작하며, 아래 예시에서는 첫 번째 재시도는 1초, 두 번째는 5초, 세 번째는 10초, 그 이후는 모두 10초씩 대기합니다.

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
#### 큐 리스너 최대 예외 허용 개수 지정

특정 리스너가 여러 번 시도되는 동안, 핸들링되지 않은 예외가 일정 횟수 발생하면 바로 실패 처리되도록 하고 싶을 수 있습니다. 이런 경우 리스너에 `maxExceptions` 속성을 지정합니다.

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

이 예시에서는 리스너가 최대 25번까지 시도되지만, 3회의 핸들링되지 않은 예외가 발생하면 즉시 실패 처리됩니다.

<a name="specifying-queued-listener-timeout"></a>
#### 큐 리스너 타임아웃 지정

큐잉된 리스너가 어느 정도의 실행 시간을 가질지 예상할 수 있다면, "타임아웃" 값을 지정할 수 있습니다. 리스너가 해당 시간(초) 이상 실행되면, 워커가 오류와 함께 종료합니다. 이를 위해, 리스너 클래스에 `timeout` 속성을 정의하세요.

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

타임아웃 발생 시 리스너를 실패 처리하고 싶으면, `failOnTimeout` 속성에 `true`를 지정합니다.

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

이벤트를 발생시키려면, 이벤트 클래스에서 static `dispatch` 메서드를 호출하면 됩니다. 이 메서드는 `Illuminate\Foundation\Events\Dispatchable` 트레이트를 통해 제공됩니다. `dispatch`에 전달된 모든 인수는 이벤트 생성자의 인수로 전달됩니다.

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

        // 주문 발송 처리 로직...

        OrderShipped::dispatch($order);

        return redirect('/orders');
    }
}
```

조건부로 이벤트를 디스패치하고 싶을 때는 `dispatchIf` 또는 `dispatchUnless` 메서드를 사용할 수 있습니다.

```php
OrderShipped::dispatchIf($condition, $order);

OrderShipped::dispatchUnless($condition, $order);
```

> [!NOTE]
> 테스트 시, 특정 이벤트가 디스패치되었는지만 확인하고 실제 리스너가 실행되진 않도록 하는 것이 유용할 수 있습니다. Laravel의 [내장 테스트 헬퍼](#testing)를 사용하면 쉽게 처리할 수 있습니다.

<a name="dispatching-events-after-database-transactions"></a>
### 데이터베이스 트랜잭션 후 이벤트 디스패치

경우에 따라, 활성화된 데이터베이스 트랜잭션이 커밋된 후에만 이벤트를 디스패치하도록 Laravel에 지시하고 싶을 때가 있습니다. 이를 위해 이벤트 클래스에 `ShouldDispatchAfterCommit` 인터페이스를 구현하세요.

이 인터페이스는 현재 데이터베이스 트랜잭션이 커밋될 때까지 이벤트가 디스패치되지 않도록 합니다. 만약 트랜잭션이 실패하면, 이벤트는 무시됩니다. 트랜잭션 없이 이벤트가 디스패치된다면 즉시 디스패치됩니다.

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
### 이벤트 지연(Defer)

이벤트 지연(Defer)은 모델 이벤트 발생과 리스너 실행을 지정한 코드 블록(클로저) 실행이 완료될 때까지 미룹니다. 이는 관련 레코드가 모두 생성된 뒤에 리스너가 실행되어야 할 때 특히 유용합니다.

이벤트를 지연시키려면 `Event::defer()` 메서드에 클로저를 전달하세요.

```php
use App\Models\User;
use Illuminate\Support\Facades\Event;

Event::defer(function () {
    $user = User::create(['name' => 'Victoria Otwell']);

    $user->posts()->create(['title' => 'My first post!']);
});
```

이렇게 하면, 해당 클로저 내부에서 발생한 모든 이벤트가 클로저 실행 이후에 한꺼번에 디스패치됩니다. 만약 클로저 내에서 예외가 발생하면, 이벤트는 디스패치되지 않습니다.

<a name="event-subscribers"></a>
## 이벤트 구독자

<a name="writing-event-subscribers"></a>
### 이벤트 구독자 작성

이벤트 구독자(Subscriber)는 여러 이벤트를 하나의 클래스에서 구독할 수 있도록 해줍니다. 즉, 하나의 클래스에 여러 이벤트 핸들러를 정의할 수 있습니다. 구독자 클래스는 `subscribe` 메서드를 정의해야 하며, 이 메서드는 이벤트 디스패처 인스턴스를 인수로 받습니다. `listen` 메서드를 호출해 이벤트와 해당 리스너를 등록할 수 있습니다.

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

구독자 클래스 자체 내에 이벤트 리스너 메서드가 정의되어 있다면, 배열 형태로 `subscribe` 메서드에서 반환할 수도 있습니다. Laravel은 자동으로 구독자 클래스명을 인식해 이벤트 리스너를 등록합니다.

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

구독자를 작성한 뒤, Laravel의 [이벤트 자동 검색 규칙](#event-discovery)을 따르는 경우에는 핸들러 메서드가 자동으로 등록됩니다. 그렇지 않은 경우, `Event` 파사드의 `subscribe` 메서드를 직접 호출하여 구독자를 수동 등록할 수 있습니다. 일반적으로, `AppServiceProvider`의 `boot` 메서드에서 등록합니다.

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

이벤트를 디스패치하는 코드를 테스트할 때, 실제로 이벤트 리스너가 실행되진 않도록 하고 싶을 수 있습니다. 리스너의 코드는 별도로 테스트할 수 있으므로, 테스트에서는 이벤트가 디스패치되는지만 검증하면 됩니다. 리스너 자체를 테스트하려면, 리스너 인스턴스를 직접 생성해 `handle` 메서드를 테스트하면 됩니다.

`Event` 파사드의 `fake` 메서드를 사용하면 리스너의 실행을 막고, 테스트 중에 어떤 이벤트가 디스패치되었는지만 `assertDispatched`, `assertNotDispatched`, `assertNothingDispatched` 등의 메서드로 검증할 수 있습니다.

```php tab=Pest
<?php

use App\Events\OrderFailedToShip;
use App\Events\OrderShipped;
use Illuminate\Support\Facades/Event;

test('orders can be shipped', function () {
    Event::fake();

    // Perform order shipping...

    // 이벤트가 디스패치되었는지 검증...
    Event::assertDispatched(OrderShipped::class);

    // 이벤트가 두 번 디스패치되었는지 검증...
    Event::assertDispatched(OrderShipped::class, 2);

    // 이벤트가 한 번 디스패치되었는지 검증...
    Event::assertDispatchedOnce(OrderShipped::class);

    // 특정 이벤트가 디스패치되지 않았는지 검증...
    Event::assertNotDispatched(OrderFailedToShip::class);

    // 아무 이벤트도 디스패치되지 않았는지 검증...
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

        // 이벤트가 디스패치되었는지 검증...
        Event::assertDispatched(OrderShipped::class);

        // 이벤트가 두 번 디스패치되었는지 검증...
        Event::assertDispatched(OrderShipped::class, 2);

        // 이벤트가 한 번 디스패치되었는지 검증...
        Event::assertDispatchedOnce(OrderShipped::class);

        // 특정 이벤트가 디스패치되지 않았는지 검증...
        Event::assertNotDispatched(OrderFailedToShip::class);

        // 아무 이벤트도 디스패치되지 않았는지 검증...
        Event::assertNothingDispatched();
    }
}
```

`assertDispatched` 또는 `assertNotDispatched` 메서드에 클로저를 전달하면, 전달받은 "조건"을 통과하는 이벤트가 실제로 디스패치되었는지 검증할 수 있습니다. 하나 이상의 이벤트가 조건을 통과하면, 검증이 성공합니다.

```php
Event::assertDispatched(function (OrderShipped $event) use ($order) {
    return $event->order->id === $order->id;
});
```

특정 이벤트를 특정 리스너가 듣고 있는지 검증하려면 `assertListening` 메서드를 사용할 수 있습니다.

```php
Event::assertListening(
    OrderShipped::class,
    SendShipmentNotification::class
);
```

> [!WARNING]
> `Event::fake()`를 호출하면, 이벤트 리스너가 모두 실행되지 않습니다. 따라서, 모델의 `creating` 이벤트를 통해 UUID를 생성하는 등 이벤트에 의존하는 모델 팩토리를 사용하는 경우, 팩토리 호출 **이후에** `Event::fake()`를 호출해야 합니다.

<a name="faking-a-subset-of-events"></a>
### 특정 이벤트만 페이크 처리

특정 이벤트의 리스너만 페이크로 처리(Pretend)하고 싶다면, 해당 이벤트를 `fake` 또는 `fakeFor` 메서드에 전달하면 됩니다.

```php tab=Pest
test('orders can be processed', function () {
    Event::fake([
        OrderCreated::class,
    ]);

    $order = Order::factory()->create();

    Event::assertDispatched(OrderCreated::class);

    // 다른 이벤트는 평소처럼 디스패치됨...
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

    // 다른 이벤트는 평소처럼 디스패치됨...
    $order->update([
        // ...
    ]);
}
```

특정 이벤트만 빼고 나머지를 모두 페이크 처리하려면 `except` 메서드를 사용하세요.

```php
Event::fake()->except([
    OrderCreated::class,
]);
```

<a name="scoped-event-fakes"></a>
### 스코프 이벤트 페이크

테스트의 일부 코드에서만 이벤트 리스너를 페이크 처리하고 싶을 때는 `fakeFor` 메서드를 활용하세요.

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

    // 이후에는 이벤트가 평소처럼 디스패치되고, 옵저버도 정상 실행됨...
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

        // 이후에는 이벤트가 평소처럼 디스패치되고, 옵저버도 정상 실행됨...
        $order->update([
            // ...
        ]);
    }
}
```
