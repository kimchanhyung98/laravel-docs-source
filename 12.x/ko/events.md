# 이벤트 (Events)

- [소개](#introduction)
- [이벤트 및 리스너 생성](#generating-events-and-listeners)
- [이벤트 및 리스너 등록](#registering-events-and-listeners)
    - [이벤트 자동 감지](#event-discovery)
    - [이벤트 수동 등록](#manually-registering-events)
    - [클로저 리스너](#closure-listeners)
- [이벤트 정의](#defining-events)
- [리스너 정의](#defining-listeners)
- [큐잉된 이벤트 리스너](#queued-event-listeners)
    - [큐 직접 다루기](#manually-interacting-with-the-queue)
    - [큐잉된 이벤트 리스너와 데이터베이스 트랜잭션](#queued-event-listeners-and-database-transactions)
    - [큐잉 리스너 미들웨어](#queued-listener-middleware)
    - [암호화된 큐잉 리스너](#encrypted-queued-listeners)
    - [실패한 작업 처리하기](#handling-failed-jobs)
- [이벤트 디스패치](#dispatching-events)
    - [데이터베이스 트랜잭션 이후 이벤트 디스패치](#dispatching-events-after-database-transactions)
    - [이벤트 디퍼(지연) 처리](#deferring-events)
- [이벤트 구독자](#event-subscribers)
    - [이벤트 구독자 작성](#writing-event-subscribers)
    - [이벤트 구독자 등록](#registering-event-subscribers)
- [테스트](#testing)
    - [일부 이벤트만 페이크하기](#faking-a-subset-of-events)
    - [스코프별 이벤트 페이크](#scoped-event-fakes)

<a name="introduction"></a>
## 소개

Laravel의 이벤트는 간단한 옵저버 패턴(observer pattern) 구현체를 제공하여 애플리케이션 내에서 발생하는 다양한 이벤트를 구독 및 리스닝할 수 있습니다. 이벤트 클래스는 일반적으로 `app/Events` 디렉터리에 위치하며, 해당 이벤트의 리스너들은 `app/Listeners`에 저장됩니다. 만약 이 디렉터리들이 현재 프로젝트에 없다면, Artisan 콘솔 명령어로 이벤트와 리스너를 생성할 때 자동으로 만들어집니다.

이벤트는 애플리케이션의 다양한 부분을 느슨하게 결합(loose coupling)할 수 있게 해줍니다. 하나의 이벤트에 복수의 리스너가 존재할 수 있으며, 이 리스너들은 서로에게 의존하지 않습니다. 예를 들어, 주문이 발송될 때마다 사용자에게 Slack 알림을 보내고 싶다고 가정해보겠습니다. 주문 처리 코드와 Slack 알림 코드를 강하게 결합하는 대신, `App\Events\OrderShipped` 이벤트를 발생시켜서, 별도의 리스너에서 이 이벤트를 받고 Slack 알림을 보낼 수 있습니다.

<a name="generating-events-and-listeners"></a>
## 이벤트 및 리스너 생성

이벤트와 리스너를 빠르게 생성하려면 `make:event` 및 `make:listener` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan make:event PodcastProcessed

php artisan make:listener SendPodcastNotification --event=PodcastProcessed
```

또한, 편의를 위해 추가 인수 없이 `make:event`나 `make:listener` 명령어를 실행하면, Laravel이 클래스 이름(및 리스너 생성 시 리스닝할 이벤트)을 자동으로 질문합니다.

```shell
php artisan make:event

php artisan make:listener
```

<a name="registering-events-and-listeners"></a>
## 이벤트 및 리스너 등록

<a name="event-discovery"></a>
### 이벤트 자동 감지

기본적으로 Laravel은 애플리케이션의 `Listeners` 디렉터리를 스캔하여 이벤트 리스너를 자동으로 찾아 등록합니다. Laravel은 메서드 시그니처에 타입힌트된 이벤트를 기준으로, `handle` 또는 `__invoke`로 시작하는 메서드를 가진 클래스의 해당 메서드를 이벤트 리스너로 등록합니다:

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

PHP의 유니언 타입을 활용해 여러 이벤트를 동시에 수신할 수도 있습니다:

```php
/**
 * Handle the event.
 */
public function handle(PodcastProcessed|PodcastPublished $event): void
{
    // ...
}
```

리스너를 다른 디렉터리나 여러 디렉터리 내에 저장하려는 경우, 애플리케이션의 `bootstrap/app.php` 파일에서 `withEvents` 메서드를 사용해 Laravel이 해당 디렉터리를 추가로 스캔하도록 지정할 수 있습니다:

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/Orders/Listeners',
])
```

와일드카드(`*`) 문자를 활용하여 비슷한 구조의 여러 디렉터리를 한 번에 스캔할 수도 있습니다:

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/*/Listeners',
])
```

애플리케이션에 등록된 모든 리스너 목록을 확인하려면 `event:list` 명령어를 사용하세요:

```shell
php artisan event:list
```

<a name="event-discovery-in-production"></a>
#### 프로덕션 환경에서의 이벤트 자동 감지

애플리케이션 성능을 높이기 위해, `optimize` 또는 `event:cache` Artisan 명령어를 사용해 전체 리스너의 매니페스트를 캐싱해두는 것이 좋습니다. 이 명령은 보통 [배포 프로세스](/docs/12.x/deployment#optimization)에서 수행합니다. 매니페스트 캐시는 프레임워크가 이벤트 등록 절차를 더 빠르게 처리할 수 있도록 도와줍니다. `event:clear` 명령어로 이벤트 캐시를 삭제할 수 있습니다.

<a name="manually-registering-events"></a>
### 이벤트 수동 등록

`Event` 파사드를 사용하면 애플리케이션의 `AppServiceProvider`의 `boot` 메서드 내에서 이벤트 및 대응 리스너를 직접 수동으로 등록할 수 있습니다:

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

등록된 모든 리스너 목록은 다음과 같이 확인할 수 있습니다:

```shell
php artisan event:list
```

<a name="closure-listeners"></a>
### 클로저 리스너

리스너는 보통 클래스로 정의하지만, `AppServiceProvider`의 `boot` 메서드 내에서 클로저(익명 함수) 기반으로도 수동 등록이 가능합니다:

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
#### 큐잉 가능한 익명 이벤트 리스너

클로저 기반의 이벤트 리스너를 등록할 때, `Illuminate\Events\queueable` 함수를 사용하여 리스너 클로저를 감싸면, 해당 리스너를 [큐](/docs/12.x/queues)로 실행하도록 지정할 수 있습니다:

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

큐잉된 작업과 마찬가지로, `onConnection`, `onQueue`, `delay` 메서드로 큐, 커넥션 또는 지연 시간을 지정할 수 있습니다:

```php
Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->onConnection('redis')->onQueue('podcasts')->delay(now()->addSeconds(10)));
```

익명 큐잉 리스너의 실패를 처리하고 싶다면, `queueable` 리스너를 정의할 때 `catch` 메서드에 실패 처리 클로저를 넘기면 됩니다. 이 클로저는 이벤트 인스턴스 및 실패의 원인인 `Throwable` 인스턴스를 인자로 받습니다:

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

`*` 문자를 와일드카드 파라미터로 사용해 여러 이벤트를 같은 리스너에서 수신할 수도 있습니다. 와일드카드 리스너는 이벤트 이름을 첫 번째 인자로, 전체 이벤트 데이터 배열을 두 번째 인자로 받습니다:

```php
Event::listen('event.*', function (string $eventName, array $data) {
    // ...
});
```

<a name="defining-events"></a>
## 이벤트 정의

이벤트 클래스는 이벤트와 관련된 정보를 담는 데이터 컨테이너 역할을 합니다. 예를 들어, `App\Events\OrderShipped` 이벤트가 [Eloquent ORM](/docs/12.x/eloquent) 객체를 전달받도록 설계할 수 있습니다:

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

이벤트 클래스에는 별도의 로직이 없으며, 단지 `App\Models\Order` 인스턴스를 담기 위한 그릇입니다. 이벤트에서 사용된 `SerializesModels` 트레이트는 만약 이벤트 객체를 PHP의 `serialize` 함수로 직렬화해야 할 경우([큐잉된 리스너](#queued-event-listeners)에서 주로 발생), Eloquent 모델을 적절히 직렬화/복원하도록 처리해줍니다.

<a name="defining-listeners"></a>
## 리스너 정의

이제 예시 이벤트에 대한 리스너를 살펴보겠습니다. 이벤트 리스너는 `handle` 메서드 내에서 이벤트 인스턴스를 전달받습니다. `make:listener` Artisan 명령어를 `--event` 옵션과 함께 사용하면, 관련 이벤트 클래스가 자동으로 import되고 타입힌트가 적용된 상태로 리스너가 생성됩니다. `handle` 메서드 내에서 이벤트에 따른 원하는 작업을 수행할 수 있습니다:

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
> 이벤트 리스너의 생성자에서 필요로 하는 의존성이 있다면, 생성자에서 타입힌트할 수 있습니다. 모든 이벤트 리스너는 Laravel의 [서비스 컨테이너](/docs/12.x/container)로부터 자동으로 주입받으므로 별도로 인스턴스화하지 않아도 됩니다.

<a name="stopping-the-propagation-of-an-event"></a>
#### 이벤트 전파 중단

특정 상황에서 이벤트가 다른 리스너로 전파되는 것을 중지하고 싶을 수 있습니다. 이 경우, 리스너의 `handle` 메서드에서 `false`를 반환하면 전파가 중단됩니다.

<a name="queued-event-listeners"></a>
## 큐잉된 이벤트 리스너

리스너가 이메일 전송이나 HTTP 요청 등 느린 작업을 수행해야 하는 경우 큐잉하여 실행하면 유용합니다. 큐잉된 리스너를 사용하기 전에, 반드시 [큐 설정](/docs/12.x/queues)을 마치고 실제 서버 혹은 개발 환경에서 큐 워커(worker)를 실행해야 합니다.

리스너를 큐잉 대상으로 지정하려면, 해당 클래스에 `ShouldQueue` 인터페이스를 구현하세요. `make:listener` 명령어로 생성된 리스너 클래스에는 이미 이 인터페이스가 import되어 있어 바로 활용할 수 있습니다:

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

이제 해당 리스너가 이벤트에 의해 호출될 때, 이벤트 디스패처가 Laravel의 [큐 시스템](/docs/12.x/queues)을 통해 자동으로 리스너를 큐잉하게 됩니다. 리스너 실행 중 예외가 발생하지 않으면, 처리 완료 후 큐 작업은 자동으로 삭제됩니다.

<a name="customizing-the-queue-connection-queue-name"></a>
#### 큐 커넥션, 큐 이름, 지연 시간 커스터마이징

리스너가 사용할 큐 커넥션, 큐 이름, 지연 시간(delay)을 명시적으로 지정하려면 리스너 클래스에 `$connection`, `$queue`, `$delay` 속성을 선언하면 됩니다:

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

실행 시점에 동적으로 커넥션, 큐, 지연 시간 등을 결정하려면, `viaConnection`, `viaQueue`, `withDelay` 메서드를 구현하면 됩니다:

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
#### 조건부 큐잉

특정 조건에 따라 리스너를 큐잉할지 여부를 결정해야 할 경우, `shouldQueue` 메서드를 추가하면 됩니다. 이 메서드가 `false`를 반환하면 해당 리스너는 큐에 추가되지 않습니다:

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

리스너의 underlying 큐 작업 객체의 `delete` 및 `release` 메서드에 직접 접근해야 하는 경우, `Illuminate\Queue\InteractsWithQueue` 트레이트를 사용할 수 있습니다. 이 트레이트는 생성된 리스너에 기본적으로 포함되며, 관련 메서드를 제공합니다:

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
### 큐잉된 이벤트 리스너와 데이터베이스 트랜잭션

큐잉 리스너가 데이터베이스 트랜잭션 내에서 디스패치될 때, 해당 트랜잭션이 커밋되기 전에 리스너가 큐에서 실행될 수 있습니다. 이 경우 트랜잭션 중 변경한 모델이나 데이터가 아직 DB에 반영되지 않았을 수 있습니다. 또한 트랜잭션에서 생성된 레코드는 DB에 존재하지 않을 수 있습니다. 리스너가 이미 커밋된 모델에 의존한다면, 큐에서 예상치 않은 오류가 날 수 있습니다.

큐 연결의 `after_commit` 설정이 `false`여도, 특정 큐잉 리스너만 모든 트랜잭션이 커밋된 뒤 실행되도록 하려면, 리스너 클래스에 `ShouldQueueAfterCommit` 인터페이스를 구현하면 됩니다:

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
> 이 이슈에 대한 자세한 내용은 [큐잉 작업과 데이터베이스 트랜잭션](/docs/12.x/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="queued-listener-middleware"></a>
### 큐잉 리스너 미들웨어

큐잉 리스너는 [작업 미들웨어](/docs/12.x/queues#job-middleware)도 사용할 수 있습니다. 작업 미들웨어를 활용하면, 큐잉 리스너 실행에 커스텀 로직을 감쌀 수 있어, 각 리스너 내부의 보일러플레이트 코드를 줄일 수 있습니다. 미들웨어를 만들어 리스너의 `middleware` 메서드에서 반환하면 자동으로 적용됩니다:

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
#### 암호화된 큐잉 리스너

Laravel은 [암호화](/docs/12.x/encryption)를 통해 큐잉 리스너의 데이터 보호 및 무결성을 보장할 수 있도록 지원합니다. 리스너 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하기만 하면, 해당 리스너의 인스턴스는 큐에 집어넣기 전에 자동으로 암호화됩니다:

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
### 실패한 작업 처리하기

큐잉된 이벤트 리스너가 실패할 수도 있습니다. 지정된 큐 워커의 최대 시도 횟수를 초과하면, 해당 리스너의 `failed` 메서드가 호출됩니다. `failed` 메서드는 이벤트 인스턴스와 실패 원인인 `Throwable` 인스턴스를 인자로 받습니다:

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
#### 큐잉 리스너 최대 시도 횟수 지정

큐잉 리스너에서 에러가 발생하면, 무한 재시도를 방지하기 위해 시도 횟수나 시간 제한을 설정할 수 있습니다.

시도 횟수 제한은 클래스의 `tries` 속성이나 메서드로, 시간 제한은 `retryUntil` 메서드(반환값: `DateTime` 객체)로 지정할 수 있습니다:

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

시도 횟수 대신, 지정된 시간까지 무한히 재시도를 허용하려면 다음과 같이 설정할 수 있습니다:

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

`retryUntil`과 `tries`가 모두 정의된 경우, `retryUntil`이 우선 적용됩니다.

<a name="specifying-queued-listener-backoff"></a>
#### 큐잉 리스너 백오프(재시도 간격) 지정

에러 발생 시 재시도까지 대기할 시간을 조절하려면, 리스너 클래스에 `backoff` 속성 또는 메서드를 선언하세요:

```php
/**
 * The number of seconds to wait before retrying the queued listener.
 *
 * @var int
 */
public $backoff = 3;
```

더 복잡한 로직이 필요하다면, 메서드를 통해 동적으로 반환할 수 있습니다:

```php
/**
 * Calculate the number of seconds to wait before retrying the queued listener.
 */
public function backoff(OrderShipped $event): int
{
    return 3;
}
```

"지수 백오프"처럼 점진적으로 재시도 대기시간을 늘리고 싶으면 배열을 반환하세요.

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

위 예시에서는 첫 번째 재시도는 1초 후, 두 번째는 5초, 세 번째는 10초 후에 실행되며 이후에도 10초 간격을 유지합니다.

<a name="specifying-queued-listener-max-exceptions"></a>
#### 큐잉 리스너 최대 예외 횟수 지정

리스너가 여러 번 재시도를 허용하되, 무조건 리스너 해제(`release`)로 인한 재시도가 아니라, 처리되지 않은 예외로 인해 설정된 횟수만큼만 시도하고 그 이상은 실패시키고 싶을 수 있습니다. `maxExceptions` 속성을 활용하세요:

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

이 예시에서는, 최대 25회까지 재시도 가능하지만, 처리되지 않은 예외가 3회 발생하면 리스너가 실패로 처리됩니다.

<a name="specifying-queued-listener-timeout"></a>
#### 큐잉 리스너 타임아웃 지정

큐잉 리스너가 얼마만큼의 시간 동안 실행될 수 있는지 미리 알고 있다면, "타임아웃" 값을 지정할 수 있습니다. 리스너가 타임아웃 설정(초 단위) 이상 실행되면, 해당 리스너를 처리중인 워커는 에러와 함께 종료됩니다. 클래스의 `timeout` 속성으로 타임아웃 제한을 지정하세요:

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

타임아웃 발생 시, 해당 리스너를 즉시 실패 상태로 표시하려면, `failOnTimeout` 속성을 `true`로 설정하면 됩니다:

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

이벤트를 발생시키기(디스패치) 위해서는, 해당 이벤트 클래스의 static `dispatch` 메서드를 호출하세요. 이 메서드는 `Illuminate\Foundation\Events\Dispatchable` 트레이트 덕분에 사용 가능합니다. `dispatch`로 전달된 인수들은 이벤트의 생성자에 그대로 전달됩니다:

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

이벤트를 조건부로 디스패치하고 싶다면, `dispatchIf`와 `dispatchUnless` 메서드를 사용하면 됩니다:

```php
OrderShipped::dispatchIf($condition, $order);

OrderShipped::dispatchUnless($condition, $order);
```

> [!NOTE]
> 테스트에서는, 실제로 리스너를 실행시키지 않으면서 이벤트가 디스패치 되었는지만 확인하고 싶을 수 있습니다. Laravel의 [내장 테스트 헬퍼](#testing)를 이용하면 매우 간단합니다.

<a name="dispatching-events-after-database-transactions"></a>
### 데이터베이스 트랜잭션 이후 이벤트 디스패치

활성화된 데이터베이스 트랜잭션이 커밋된 후에만 이벤트를 발송하고 싶을 수도 있습니다. 이 경우 이벤트 클래스에 `ShouldDispatchAfterCommit` 인터페이스를 구현하면, 현재 트랜잭션이 커밋될 때까지 이벤트는 보류됩니다. 트랜잭션에 실패하면 이벤트는 자동으로 폐기됩니다. 트랜잭션이 없으면 즉시 이벤트가 디스패치됩니다:

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
### 이벤트 디퍼(지연) 처리

디퍼 이벤트(Deferred events)를 사용하면, 특정 코드 블록의 실행이 끝난 후에만 모델 이벤트와 리스너 실행이 이루어지도록 할 수 있습니다. 이 방식은 관련 레코드들이 모두 생성된 다음에 이벤트 리스너가 실행되도록 보장해야 하는 경우에 특히 유용합니다.

이벤트를 디퍼처리하려면, `Event::defer()` 메서드에 클로저를 전달하세요:

```php
use App\Models\User;
use Illuminate\Support\Facades/Event;

Event::defer(function () {
    $user = User::create(['name' => 'Victoria Otwell']);

    $user->posts()->create(['title' => 'My first post!']);
});
```

위 클로저 내부에서 발생한 모든 이벤트는, 클로저 실행이 끝난 뒤에 디스패치됩니다. 이 덕분에 이벤트 리스너에서 위에서 생성된 모든 관련 레코드에 접근할 수 있습니다. 만약 클로저 내부에서 예외가 발생하면, 그 안에서 트리거된 이벤트들은 디스패치되지 않습니다.

특정 이벤트만 디퍼하고 싶으면, 두 번째 인자로 이벤트 배열을 전달하세요:

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

이벤트 구독자(Subscriber)는 하나의 클래스 내에서 여러 이벤트를 구독할 수 있도록 해주는 클래스입니다. 즉, 여러 이벤트의 핸들러를 한 클래스에 정의할 수 있습니다. 구독자는 반드시 `subscribe` 메서드를 정의해야 하며, 이 메서드는 이벤트 디스패처 인스턴스를 인자로 받습니다. 넘겨받은 디스패처의 `listen` 메서드를 사용하여, 이벤트 리스너를 등록합니다:

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

구독자 내부에 정의된 메서드가 많아진다면, `subscribe` 메서드에서 이벤트와 메서드명을 배열로 반환하여 좀 더 간편하게 여러 리스너를 등록할 수도 있습니다:

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

구독자를 작성했다면, 해당 구독자의 핸들러 메서드가 Laravel의 [이벤트 감지 규약](#event-discovery)을 따른다면 Laravel이 자동으로 등록합니다. 만약 자동 감지되지 않는다면, `Event` 파사드의 `subscribe` 메서드로 수동 등록할 수 있습니다. 보통 이것은 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 수행합니다:

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

이벤트를 디스패치하는 코드를 테스트할 때, 실제로 리스너의 코드가 실행되는 것은 원하지 않을 수 있습니다. 이는 리스너의 코드는 독립적으로 별도의 테스트를 통해 검증할 수 있고, 이벤트 디스패치 코드만 따로 테스트할 수 있기 때문입니다. 리스너 자체를 테스트하려면, 테스트 코드에서 리스너 인스턴스를 만들어 `handle` 메서드를 직접 호출하면 됩니다.

`Event` 파사드의 `fake` 메서드를 사용하면, 이벤트 리스너 실행을 방지한 채로 테스트 코드를 실행하고, 어떤 이벤트들이 디스패치되었는지를 `assertDispatched`, `assertNotDispatched`, `assertNothingDispatched` 메서드로 검증할 수 있습니다:

```php tab=Pest
<?php

use App\Events\OrderFailedToShip;
use App\Events\OrderShipped;
use Illuminate\Support\Facades\Event;

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

또한 `assertDispatched`, `assertNotDispatched`에 클로저를 전달하면, 이벤트가 특정 조건(진위 테스트)을 충족하여 디스패치되었는지의 여부도 검증할 수 있습니다. 주어진 조건을 만족하는 이벤트가 단 하나라도 있으면 assertion이 통과합니다:

```php
Event::assertDispatched(function (OrderShipped $event) use ($order) {
    return $event->order->id === $order->id;
});
```

특정 이벤트에 리스너가 등록되어 있는지만 검증하고 싶으면 `assertListening` 메서드를 사용하세요:

```php
Event::assertListening(
    OrderShipped::class,
    SendShipmentNotification::class
);
```

> [!WARNING]
> `Event::fake()`를 호출하면 이후부터 모든 이벤트 리스너가 실행되지 않습니다. 따라서, 생성 이벤트(예: UUID 자동 생성 등)에 의존하는 모델 팩토리를 사용할 때는 팩토리 사용 이후에 `Event::fake()`를 호출해야 합니다.

<a name="faking-a-subset-of-events"></a>
### 일부 이벤트만 페이크하기

특정 이벤트 리스너만 페이크하고 싶으면, 해당 이벤트를 `fake` 또는 `fakeFor` 메서드에 배열로 넘기면 됩니다:

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

페이크에서 특정 이벤트만 제외하고 싶으면 `except` 메서드를 이용할 수 있습니다:

```php
Event::fake()->except([
    OrderCreated::class,
]);
```

<a name="scoped-event-fakes"></a>
### 스코프별 이벤트 페이크

테스트의 특정 구간에서만 이벤트 리스너를 페이크하고 싶으면, `fakeFor` 메서드를 사용하세요:

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
