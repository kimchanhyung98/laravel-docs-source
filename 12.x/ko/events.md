# 이벤트 (Events)

- [소개](#introduction)
- [이벤트와 리스너 생성](#generating-events-and-listeners)
- [이벤트와 리스너 등록](#registering-events-and-listeners)
    - [이벤트 자동 탐지(Event Discovery)](#event-discovery)
    - [수동으로 이벤트 등록](#manually-registering-events)
    - [클로저 리스너](#closure-listeners)
- [이벤트 정의](#defining-events)
- [리스너 정의](#defining-listeners)
- [큐 처리되는(Queued) 이벤트 리스너](#queued-event-listeners)
    - [큐 직접 다루기](#manually-interacting-with-the-queue)
    - [큐 리스너와 데이터베이스 트랜잭션](#queued-event-listeners-and-database-transactions)
    - [큐 리스너 미들웨어](#queued-listener-middleware)
    - [암호화된 큐 리스너](#encrypted-queued-listeners)
    - [실패한 작업 처리](#handling-failed-jobs)
- [이벤트 디스패치하기](#dispatching-events)
    - [데이터베이스 트랜잭션 이후 이벤트 디스패치](#dispatching-events-after-database-transactions)
    - [이벤트 지연(Deferred Events)](#deferring-events)
- [이벤트 구독자](#event-subscribers)
    - [이벤트 구독자 작성](#writing-event-subscribers)
    - [이벤트 구독자 등록](#registering-event-subscribers)
- [테스트](#testing)
    - [일부분 이벤트만 페이크 처리](#faking-a-subset-of-events)
    - [스코프별 이벤트 페이크](#scoped-event-fakes)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel의 이벤트는 간단한 옵저버 패턴(Observer Pattern) 구현을 제공하여, 애플리케이션 내에서 발생하는 다양한 이벤트를 구독하고 리스닝할 수 있도록 합니다. 이벤트 클래스는 일반적으로 `app/Events` 디렉터리에 저장되며, 해당 리스너는 `app/Listeners`에 저장됩니다. 만약 애플리케이션에 이러한 디렉터리가 없다면, Artisan 콘솔 명령어로 이벤트와 리스너를 생성할 때 자동으로 생성됩니다.

이벤트는 애플리케이션의 여러 부분을 느슨하게 결합(Decoupling)하는 훌륭한 방법입니다. 하나의 이벤트에 여러 리스너가 존재할 수 있으며, 이들은 서로 의존하지 않아도 됩니다. 예를 들어, 주문이 배송될 때마다 사용자에게 Slack 알림을 보내고 싶다면, 주문 처리 코드와 Slack 알림 코드를 직접 연결하지 않고 `App\Events\OrderShipped` 이벤트를 발생시켜 별도의 리스너에서 Slack 알림을 전송하도록 할 수 있습니다.

<a name="generating-events-and-listeners"></a>
## 이벤트와 리스너 생성 (Generating Events and Listeners)

이벤트와 리스너를 빠르게 생성하려면 `make:event` 및 `make:listener` Artisan 명령어를 사용할 수 있습니다:

```shell
php artisan make:event PodcastProcessed

php artisan make:listener SendPodcastNotification --event=PodcastProcessed
```

편리하게도, `make:event` 또는 `make:listener` 명령어를 별도 인수 없이 실행할 수도 있습니다. 이 경우 Laravel이 클래스 이름(그리고 리스너일 경우 리스닝할 이벤트)을 물어보는 프롬프트를 보여줍니다:

```shell
php artisan make:event

php artisan make:listener
```

<a name="registering-events-and-listeners"></a>
## 이벤트와 리스너 등록 (Registering Events and Listeners)

<a name="event-discovery"></a>
### 이벤트 자동 탐지(Event Discovery)

기본적으로 Laravel은 애플리케이션의 `Listeners` 디렉터리를 스캔하여 이벤트 리스너를 자동으로 찾아 등록합니다. `handle` 또는 `__invoke`로 시작하는 메서드가 있다면, 해당 메서드의 시그니처에 타입힌트 된 이벤트에 대한 리스너로 자동 등록됩니다:

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

PHP의 유니언 타입을 사용하여 여러 이벤트를 한 번에 리슨할 수도 있습니다:

```php
/**
 * Handle the event.
 */
public function handle(PodcastProcessed|PodcastPublished $event): void
{
    // ...
}
```

리스너를 다른 디렉터리 또는 여러 디렉터리에 저장하고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에서 `withEvents` 메서드를 사용해 Laravel이 해당 디렉터리를 스캔하도록 지정할 수 있습니다:

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/Orders/Listeners',
])
```

와일드카드 `*` 문자를 이용하여 유사한 여러 디렉터리를 한 번에 스캔할 수도 있습니다:

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/*/Listeners',
])
```

`event:list` 명령어를 사용하면 현재 애플리케이션에 등록된 모든 리스너를 확인할 수 있습니다:

```shell
php artisan event:list
```

<a name="event-discovery-in-production"></a>
#### 운영환경에서의 이벤트 자동 탐지

애플리케이션의 성능 향상을 위해 `optimize` 또는 `event:cache` Artisan 명령어를 실행하여 모든 리스너의 매니페스트를 캐시해둘 것을 권장합니다. 일반적으로 이 명령어는 [배포 프로세스](/docs/12.x/deployment#optimization)의 일부로 수행됩니다. 이 매니페스트는 이벤트 등록 속도를 높이기 위해 프레임워크에서 사용됩니다. 이벤트 캐시를 제거하려면 `event:clear` 명령어를 사용하십시오.

<a name="manually-registering-events"></a>
### 수동으로 이벤트 등록

`Event` 파사드를 사용하여 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 이벤트와 그에 대응하는 리스너를 수동으로 등록할 수 있습니다:

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

현재 애플리케이션에 등록된 모든 리스너 목록은 다음 명령어로 확인할 수 있습니다:

```shell
php artisan event:list
```

<a name="closure-listeners"></a>
### 클로저 리스너

일반적으로 리스너는 클래스 단위로 정의되지만, 클로저(익명 함수) 기반 이벤트 리스너를 `AppServiceProvider`의 `boot` 메서드에서 수동으로 등록할 수도 있습니다:

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
#### 큐 처리되는 익명(Anonymous) 이벤트 리스너

클로저 기반 이벤트 리스너를 등록할 때, `Illuminate\Events\queueable` 함수를 사용해서 해당 리스너를 [큐](/docs/12.x/queues)에서 실행할 수 있도록 지정할 수 있습니다:

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

큐 처리 작업과 마찬가지로, `onConnection`, `onQueue`, `delay` 메서드를 사용해 큐 리스너의 실행 환경을 커스터마이즈할 수 있습니다:

```php
Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->onConnection('redis')->onQueue('podcasts')->delay(now()->plus(seconds: 10)));
```

익명 큐 리스너에서 실패를 처리하고 싶다면, `queueable` 리스너를 정의할 때 `catch` 메서드에 클로저를 전달할 수 있습니다. 이 클로저에는 이벤트 인스턴스와 실패 원인인 `Throwable` 인스턴스가 전달됩니다:

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
#### 와일드카드(Wildcard) 이벤트 리스너

`*` 와일드카드 문자를 사용해 여러 이벤트를 한 번에 캡처하는 리스너를 등록할 수 있습니다. 와일드카드 리스너는 첫 번째 인수로 이벤트 이름을, 두 번째 인수로 이벤트 데이터 배열을 전달받습니다:

```php
Event::listen('event.*', function (string $eventName, array $data) {
    // ...
});
```

<a name="defining-events"></a>
## 이벤트 정의 (Defining Events)

이벤트 클래스는 본질적으로 이벤트와 관련된 정보를 담는 데이터 컨테이너입니다. 예를 들어, `App\Events\OrderShipped` 이벤트가 [Eloquent ORM](/docs/12.x/eloquent) 객체를 받는다고 가정해보겠습니다:

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

이 이벤트 클래스는 별도의 로직 없이 `App\Models\Order` 인스턴스를 저장하는 역할만 수행합니다. 이벤트에서 `SerializesModels` 트레이트가 사용되기 때문에, PHP의 `serialize` 함수를 사용할 때(예: [큐 리스너](#queued-event-listeners) 사용 시) Eloquent 모델을 안전하게 직렬화할 수 있게 됩니다.

<a name="defining-listeners"></a>
## 리스너 정의 (Defining Listeners)

다음으로, 예시 이벤트에 대한 리스너를 살펴보겠습니다. 이벤트 리스너는 이벤트 인스턴스를 `handle` 메서드로 전달받습니다. `make:listener` Artisan 명령어를 사용할 때 `--event` 옵션을 추가하면, 해당 이벤트 클래스를 자동으로 import하고 `handle` 메서드의 타입힌트도 자동으로 추가됩니다. `handle` 메서드 내부에서 이벤트에 대응하는 작업을 수행할 수 있습니다:

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
> 이벤트 리스너의 생성자에서 필요한 의존성을 타입힌트로 지정할 수도 있습니다. 모든 이벤트 리스너는 Laravel의 [서비스 컨테이너](/docs/12.x/container)를 통해 해결되므로, 필요한 의존성이 자동으로 주입됩니다.

<a name="stopping-the-propagation-of-an-event"></a>
#### 이벤트 전파 중단(Stopping The Propagation Of An Event)

때때로 이벤트가 다른 리스너로 전파되지 않게 하고 싶을 때가 있습니다. 이 경우, 리스너의 `handle` 메서드에서 `false`를 반환하면 이벤트 전파가 중단됩니다.

<a name="queued-event-listeners"></a>
## 큐 처리되는(Queued) 이벤트 리스너 (Queued Event Listeners)

리스너가 이메일 전송, HTTP 요청 등 느린 작업을 할 예정이라면, 리스너를 큐에 등록해 비동기로 처리하는 것이 좋습니다. 큐 리스너를 사용하기 전에 [큐 설정](/docs/12.x/queues)을 반드시 마치고, 서버나 로컬 개발 환경에서 큐 워커를 실행해야 합니다.

리스너를 큐로 지정하려면, 리스너 클래스에 `ShouldQueue` 인터페이스를 추가하면 됩니다. `make:listener` Artisan 명령어로 생성한 리스너에는 이미 이 인터페이스가 import되어 있습니다:

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

이제 이 리스너가 처리해야하는 이벤트가 디스패치될 때마다, Laravel의 [큐 시스템](/docs/12.x/queues)을 통해 리스너가 자동으로 큐에 등록됩니다. 만약 큐에서 리스너 실행 시 예외가 발생하지 않는다면, 작업이 끝난 뒤 자동으로 삭제됩니다.

<a name="customizing-the-queue-connection-queue-name"></a>
#### 큐 연결, 이름, 지연 시간 커스터마이즈

리스너의 큐 연결 이름, 큐명, 지연 시간 등을 커스터마이즈하려면 리스너 클래스에 `$connection`, `$queue`, `$delay` 속성을 설정하면 됩니다:

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

이 속성들을 런타임에 동적으로 정하고 싶을 때는 `viaConnection`, `viaQueue`, `withDelay` 메서드를 정의하면 됩니다:

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
#### 리스너를 조건부로 큐잉하기

실행 시점의 데이터에 따라 리스너를 큐에 넣을지 결정해야 할 때도 있습니다. 이 경우, 리스너에 `shouldQueue` 메서드를 만들어 `false`를 반환하면 큐에 넣지 않습니다:

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
### 큐 직접 다루기

리스너의 내부에서 큐 작업의 `delete`, `release` 메서드를 직접 호출하려면 `Illuminate\Queue\InteractsWithQueue` 트레이트를 사용하면 됩니다. 이 트레이트는 기본적으로 생성된 리스너에 포함되어 있습니다:

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
        if ($condition) {
            $this->release(30);
        }
    }
}
```

<a name="queued-event-listeners-and-database-transactions"></a>
### 큐 리스너와 데이터베이스 트랜잭션

큐 리스너가 데이터베이스 트랜잭션 내에서 디스패치될 때, 큐에 의해 트랜잭션 커밋 전에 리스너가 처리될 수 있습니다. 이럴 경우 트랜잭션 내에서 변경한 모델이나 레코드가 아직 데이터베이스에 반영되지 않았을 수 있습니다. 이런 상황에서 리스너가 해당 데이터에 의존하면, 예기치 않은 에러가 발생할 수 있습니다.

큐 연결의 `after_commit` 설정이 `false`일 경우, 특정 큐 리스너는 `ShouldQueueAfterCommit` 인터페이스를 구현하여 모든 열린 데이터베이스 트랜잭션이 커밋된 이후에만 디스패치될 수 있습니다:

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
> 이러한 문제를 우회하는 방법에 대해서는 [큐 작업과 데이터베이스 트랜잭션](/docs/12.x/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="queued-listener-middleware"></a>
### 큐 리스너 미들웨어

큐 리스너는 [잡 미들웨어](/docs/12.x/queues#job-middleware)를 활용할 수 있습니다. 잡 미들웨어는 큐 리스너 실행 전후에 커스텀 로직을 감쌀 수 있게 하여, 리스너 자체의 반복 코드를 줄여줍니다. 미들웨어를 생성한 후에는 리스너의 `middleware` 메서드에서 반환하여 사용할 수 있습니다:

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

Laravel에서는 [암호화](/docs/12.x/encryption)를 통해 큐 리스너의 데이터 프라이버시와 무결성을 보장할 수 있습니다. `ShouldBeEncrypted` 인터페이스를 리스너 클래스에 추가하기만 하면, Laravel이 리스너를 큐에 넣기 전에 자동으로 암호화해줍니다:

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
### 실패한 작업 처리(Handling Failed Jobs)

큐에 등록된 이벤트 리스너가 실패할 수도 있습니다. 큐 리스너가 큐 워커에서 정의한 최대 재시도 횟수를 초과하면, 리스너의 `failed` 메서드가 호출됩니다. 이 메서드에는 이벤트 인스턴스와 실패 원인인 `Throwable`이 전달됩니다:

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

큐 리스너가 에러를 계속 만나고 있다면, 무한히 다시 실행하도록 두고 싶지 않을 것입니다. Laravel은 시도 횟수나 최대 지속 시간 등 다양한 방식으로 리스너의 재시도 제한을 지정할 수 있습니다.

리스너 클래스를 정의할 때 `tries` 속성이나 메서드로 최대 시도 횟수를 설정할 수 있습니다:

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

시도 횟수 대신 리스너의 재시도 종료 시점을 정하고 싶다면, 클래스에 `retryUntil` 메서드를 추가하세요. 이 메서드는 `DateTime` 인스턴스를 반환해야 합니다:

```php
use DateTime;

/**
 * Determine the time at which the listener should timeout.
 */
public function retryUntil(): DateTime
{
    return now()->plus(minutes: 5);
}
```

`retryUntil`과 `tries`가 모두 정의되어 있으면, Laravel은 `retryUntil` 메서드 값을 우선으로 사용합니다.

<a name="specifying-queued-listener-backoff"></a>
#### 큐 리스너 백오프(Backoff) 설정

실패한 리스너를 재시도하기 전 Laravel이 몇 초를 기다려야 할지 설정하려면, 클래스에 `backoff` 속성을 추가합니다:

```php
/**
 * The number of seconds to wait before retrying the queued listener.
 *
 * @var int
 */
public $backoff = 3;
```

더 복잡한 백오프 로직이 필요하다면, 클래스에 `backoff` 메서드를 정의하면 됩니다:

```php
/**
 * Calculate the number of seconds to wait before retrying the queued listener.
 */
public function backoff(OrderShipped $event): int
{
    return 3;
}
```

배열을 반환해 "지수 백오프"를 쉽게 설정할 수도 있습니다. 예를 들어 아래와 같이 하면, 첫 번째 재시도는 1초, 두 번째는 5초, 세 번째는 10초, 그 이후는 계속 10초의 딜레이가 적용됩니다:

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
#### 큐 리스너 최대 예외 횟수 지정

많은 재시도가 가능하도록 하면서, 처리되지 않은 예외가 일정 횟수 이상 발생할 때는 실패로 간주하고 싶을 때도 있습니다. 이럴 때는 `maxExceptions` 속성을 정의하세요:

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

이 예시에서는 최대 25번까지 재시도되지만, 처리되지 않은 예외가 세 번 발생하면 리스너가 실패로 간주됩니다.

<a name="specifying-queued-listener-timeout"></a>
#### 큐 리스너 타임아웃 지정

일반적으로 큐 리스너가 어느 정도 시간 동안 실행될지 예상할 수 있습니다. Laravel에서는 "타임아웃" 값을 설정해, 지정한 초보다 오래 처리되면 워커가 에러와 함께 종료되도록 할 수 있습니다. 리스너 클래스에 `timeout` 속성을 추가하세요:

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

타임아웃 발생 시 리스너를 실패로 표시하려면, 클래스에 `failOnTimeout` 속성을 추가합니다:

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
## 이벤트 디스패치하기 (Dispatching Events)

이벤트를 디스패치하려면, 해당 이벤트의 정적 `dispatch` 메서드를 호출하면 됩니다. 이 메서드는 `Illuminate\Foundation\Events\Dispatchable` 트레이트를 통해 제공됩니다. `dispatch`에 전달한 모든 인수는 이벤트의 생성자에 전달됩니다:

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

이벤트를 조건부로 디스패치하고 싶을 때는 `dispatchIf`, `dispatchUnless` 메서드를 사용할 수 있습니다:

```php
OrderShipped::dispatchIf($condition, $order);

OrderShipped::dispatchUnless($condition, $order);
```

> [!NOTE]
> 테스트 시 특정 이벤트가 실제로 리스너를 실행하지 않고 디스패치만 되었는지 손쉽게 검증하고자 한다면, Laravel의 [내장 테스트 헬퍼](#testing)를 활용하면 간단합니다.

<a name="dispatching-events-after-database-transactions"></a>
### 데이터베이스 트랜잭션 이후 이벤트 디스패치

특정 이벤트가 활성화된 데이터베이스 트랜잭션이 커밋된 후에만 디스패치되도록 하고 싶을 때도 있습니다. 이럴 때는 이벤트 클래스에 `ShouldDispatchAfterCommit` 인터페이스를 구현하세요.

이 인터페이스를 구현한 이벤트는, 트랜잭션이 커밋될 때까지 디스패치되지 않습니다. 트랜잭션이 실패할 경우 이벤트 자체도 무시되며, 트랜잭션이 없을 때는 곧바로 디스패치됩니다:

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
### 이벤트 지연(Deferred Events)

지연 이벤트(Deferred Events)는 모델 이벤트의 디스패치와 리스너의 실행을 특정 코드 블록 이후로 미루는 기능입니다. 이 기능은 모든 관련 레코드가 생성된 이후에만 이벤트 리스너가 트리거되어야 할 때 유용합니다.

이벤트를 지연하려면 `Event::defer()` 메서드에 클로저를 전달하세요:

```php
use App\Models\User;
use Illuminate\Support\Facades\Event;

Event::defer(function () {
    $user = User::create(['name' => 'Victoria Otwell']);

    $user->posts()->create(['title' => 'My first post!']);
});
```

위 클로저 내에서 발생한 모든 이벤트는 클로저 실행이 끝난 뒤에 디스패치됩니다. 따라서 리스너는 클로저 중 생성된 모든 관련 레코드에 접근할 수 있습니다. 클로저 내에서 예외가 발생한다면 이벤트는 디스패치되지 않습니다.

특정 이벤트만 지연하고 싶다면, `defer` 메서드의 두 번째 인수에 이벤트 배열을 전달할 수 있습니다:

```php
use App\Models\User;
use Illuminate\Support\Facades/Event;

Event::defer(function () {
    $user = User::create(['name' => 'Victoria Otwell']);

    $user->posts()->create(['title' => 'My first post!']);
}, ['eloquent.created: '.User::class]);
```

<a name="event-subscribers"></a>
## 이벤트 구독자 (Event Subscribers)

<a name="writing-event-subscribers"></a>
### 이벤트 구독자 작성 (Writing Event Subscribers)

이벤트 구독자는 하나의 클래스 안에서 여러 이벤트를 구독할 수 있는 구조로, 여러 이벤트 핸들러를 하나의 클래스에 정의할 수 있습니다. 구독자 클래스에서는 `subscribe` 메서드를 정의해야 하며, 이 메서드는 이벤트 디스패처 인스턴스를 인자로 받습니다. `listen` 메서드를 통해 이벤트 리스너를 등록할 수 있습니다:

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

구독자 내의 메서드에서 직접 리스너를 정의했다면, `subscribe` 메서드에서 이벤트와 메서드 이름의 배열을 반환하는 방식을 더 편리하게 사용할 수 있습니다. Laravel이 자동으로 구독자 클래스명을 판단합니다:

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
### 이벤트 구독자 등록 (Registering Event Subscribers)

구독자를 작성한 뒤, 해당 메서드가 Laravel의 [이벤트 자동 탐지 규칙](#event-discovery)을 만족한다면 자동으로 등록됩니다. 그렇지 않은 경우 `Event` 파사드의 `subscribe` 메서드를 사용해 수동으로 등록할 수 있습니다. 일반적으로 `AppServiceProvider`의 `boot` 메서드에서 수행합니다:

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
## 테스트 (Testing)

이벤트를 디스패치하는 코드를 테스트할 때, 실제로 이벤트 리스너를 실행하지 않도록 처리하고 싶을 수 있습니다. 리스너의 코드는 별도로 독립해서 테스트할 수 있기 때문입니다. 리스너 자체를 테스트하고 싶을 때에는 리스너 인스턴스를 만들어 테스트에서 직접 `handle` 메서드를 호출하면 됩니다.

`Event` 파사드의 `fake` 메서드를 사용하면, 리스너 실행을 막고, 테스트하고자 하는 동작을 수행한 후, `assertDispatched`, `assertNotDispatched`, `assertNothingDispatched` 등 다양한 메서드로 어떤 이벤트가 디스패치되었는지 검증할 수 있습니다:

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

특정 이벤트가 조건에 부합하는지 확인하려면, `assertDispatched` 또는 `assertNotDispatched` 메서드에 클로저를 전달할 수 있습니다. 전달한 "트루스 테스트"를 통과한 이벤트가 하나라도 있다면 검증이 성공합니다:

```php
Event::assertDispatched(function (OrderShipped $event) use ($order) {
    return $event->order->id === $order->id;
});
```

특정 이벤트에 대해 리스너가 실제로 등록되어 있는지 검증하고 싶다면 `assertListening` 메서드를 사용할 수 있습니다:

```php
Event::assertListening(
    OrderShipped::class,
    SendShipmentNotification::class
);
```

> [!WARNING]
> `Event::fake()`를 호출하면 어떤 이벤트 리스너도 실행되지 않습니다. 따라서, 만약 테스트에서 이벤트에 의존하는 모델 팩토리를 사용한다면(예: 모델 생성 시 UUID를 부여하는 `creating` 이벤트 등), 팩토리 사용 **이후에** `Event::fake()`를 호출해야 합니다.

<a name="faking-a-subset-of-events"></a>
### 일부분 이벤트만 페이크 처리

특정 이벤트에 대해서만 페이크 리스너를 적용하고 싶다면, 해당 이벤트들을 `fake` 또는 `fakeFor` 메서드의 인수로 전달할 수 있습니다:

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

특정 이벤트만 제외하고 나머지 모든 이벤트에 대해 페이크 처리를 하려면 `except` 메서드를 사용할 수 있습니다:

```php
Event::fake()->except([
    OrderCreated::class,
]);
```

<a name="scoped-event-fakes"></a>
### 스코프별 이벤트 페이크 (Scoped Event Fakes)

테스트의 일부분 구간에만 이벤트 리스너 페이크를 적용하고 싶다면, `fakeFor` 메서드를 사용할 수 있습니다:

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
