# 이벤트 (Events)

- [소개](#introduction)
- [이벤트 및 리스너 등록](#registering-events-and-listeners)
    - [이벤트 및 리스너 생성](#generating-events-and-listeners)
    - [수동으로 이벤트 등록하기](#manually-registering-events)
    - [이벤트 자동 발견 (Event Discovery)](#event-discovery)
- [이벤트 정의하기](#defining-events)
- [리스너 정의하기](#defining-listeners)
- [큐잉된 이벤트 리스너 (Queued Event Listeners)](#queued-event-listeners)
    - [큐와 수동으로 상호작용하기](#manually-interacting-with-the-queue)
    - [큐잉된 이벤트 리스너와 데이터베이스 트랜잭션](#queued-event-listeners-and-database-transactions)
    - [실패한 작업 처리하기](#handling-failed-jobs)
- [이벤트 디스패치하기 (Dispatching Events)](#dispatching-events)
    - [데이터베이스 트랜잭션 후 이벤트 디스패치](#dispatching-events-after-database-transactions)
- [이벤트 구독자 (Event Subscribers)](#event-subscribers)
    - [이벤트 구독자 작성하기](#writing-event-subscribers)
    - [이벤트 구독자 등록하기](#registering-event-subscribers)
- [테스트](#testing)
    - [일부 이벤트 페이크하기](#faking-a-subset-of-events)
    - [범위를 제한한 이벤트 페이크](#scoped-event-fakes)

<a name="introduction"></a>
## 소개

Laravel의 이벤트는 간단한 옵저버 패턴(observer pattern)을 구현하여 애플리케이션 내에서 발생하는 다양한 이벤트를 구독하고 청취할 수 있게 해줍니다. 이벤트 클래스는 일반적으로 `app/Events` 디렉토리에 저장되며, 이들의 리스너는 `app/Listeners`에 저장됩니다. 애플리케이션에 이러한 디렉토리가 보이지 않아도 걱정하지 마세요. Artisan 콘솔 명령어를 이용해 이벤트와 리스너를 생성할 때 자동으로 생성됩니다.

이벤트는 애플리케이션의 여러 부분을 느슨하게 결합하는 데 탁월한 방법입니다. 하나의 이벤트에 여러 리스너가 연결되어 서로 의존하지 않고 독립적으로 동작할 수 있기 때문입니다. 예를 들어, 주문이 배송될 때마다 사용자에게 슬랙 알림을 보내고 싶을 수 있습니다. 주문 처리 코드와 슬랙 알림 코드를 분리하고, 대신 `App\Events\OrderShipped` 이벤트를 발생시키고, 해당 이벤트를 수신하는 리스너가 슬랙 알림을 전송하도록 할 수 있습니다.

<a name="registering-events-and-listeners"></a>
## 이벤트 및 리스너 등록

Laravel 애플리케이션과 함께 제공되는 `App\Providers\EventServiceProvider`는 애플리케이션의 모든 이벤트 리스너를 등록하기에 편리한 장소를 제공합니다. `$listen` 속성은 모든 이벤트(키)와 해당 이벤트에 바인딩된 리스너 배열(값)로 구성된 배열입니다. 애플리케이션 요구에 따라 이 배열에 원하는 만큼 이벤트를 추가할 수 있습니다. 예를 들어 `OrderShipped` 이벤트를 추가해봅시다:

```
use App\Events\OrderShipped;
use App\Listeners\SendShipmentNotification;

/**
 * The event listener mappings for the application.
 *
 * @var array<class-string, array<int, class-string>>
 */
protected $listen = [
    OrderShipped::class => [
        SendShipmentNotification::class,
    ],
];
```

> [!NOTE]  
> `event:list` 명령어를 사용해 애플리케이션에 등록된 모든 이벤트와 리스너 목록을 출력할 수 있습니다.

<a name="generating-events-and-listeners"></a>
### 이벤트 및 리스너 생성

각 이벤트와 리스너 파일을 수동으로 만드는 것은 번거롭습니다. 대신 `EventServiceProvider`에 이벤트와 리스너를 추가한 후 `event:generate` Artisan 명령어를 실행하세요. 이 명령어는 `EventServiceProvider`에 등록되어 있지만 아직 존재하지 않는 이벤트와 리스너를 자동으로 생성합니다:

```shell
php artisan event:generate
```

또한 개별적으로 이벤트와 리스너를 생성할 때는 `make:event` 및 `make:listener` 명령어를 사용할 수 있습니다:

```shell
php artisan make:event PodcastProcessed

php artisan make:listener SendPodcastNotification --event=PodcastProcessed
```

<a name="manually-registering-events"></a>
### 수동으로 이벤트 등록하기

일반적으로 이벤트는 `EventServiceProvider`의 `$listen` 배열을 통해 등록하는 것이 권장되지만, `EventServiceProvider` 클래스의 `boot` 메서드에서 클래스 기반 혹은 클로저 기반 이벤트 리스너를 수동으로 등록할 수도 있습니다:

```
use App\Events\PodcastProcessed;
use App\Listeners\SendPodcastNotification;
use Illuminate\Support\Facades\Event;

/**
 * Register any other events for your application.
 */
public function boot(): void
{
    Event::listen(
        PodcastProcessed::class,
        SendPodcastNotification::class,
    );

    Event::listen(function (PodcastProcessed $event) {
        // ...
    });
}
```

<a name="queuable-anonymous-event-listeners"></a>
#### 큐잉 가능한 익명 이벤트 리스너

클로저 기반 이벤트 리스너를 수동으로 등록할 때 `Illuminate\Events\queueable` 함수를 이용해 클로저를 감싸면 해당 리스너를 Laravel 큐 시스템으로 실행하도록 지시할 수 있습니다:

```
use App\Events\PodcastProcessed;
use function Illuminate\Events\queueable;
use Illuminate\Support\Facades\Event;

/**
 * Register any other events for your application.
 */
public function boot(): void
{
    Event::listen(queueable(function (PodcastProcessed $event) {
        // ...
    }));
}
```

큐에 들어가는 작업처럼, `onConnection`, `onQueue`, `delay` 메서드를 이용해 큐 연결, 큐 이름, 지연 시간을 커스터마이즈 할 수 있습니다:

```
Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->onConnection('redis')->onQueue('podcasts')->delay(now()->addSeconds(10)));
```

익명 큐잉 리스너 실패 처리를 위해, `queueable` 리스너 정의 시 `catch` 메서드에 클로저를 제공할 수 있습니다. 이 클로저는 이벤트 인스턴스와 실패 원인이 된 `Throwable` 인스턴스를 받습니다:

```
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

`*` 와일드카드를 사용해 여러 이벤트를 하나의 리스너에서 포착할 수도 있습니다. 와일드카드 리스너는 첫 번째 인수로 이벤트 이름, 두 번째 인수로 전체 이벤트 데이터 배열을 받습니다:

```
Event::listen('event.*', function (string $eventName, array $data) {
    // ...
});
```

<a name="event-discovery"></a>
### 이벤트 자동 발견 (Event Discovery)

`EventServiceProvider`의 `$listen` 배열에 수동으로 이벤트와 리스너를 등록하지 않고, 자동 이벤트 발견 기능을 활성화할 수 있습니다. 자동 발견이 활성화되면 Laravel은 애플리케이션의 `Listeners` 디렉토리를 스캔하여 이벤트와 리스너를 자동 등록합니다. 다만, `EventServiceProvider`에 명시적으로 등록된 이벤트들은 여전히 해당대로 등록됩니다.

Laravel은 PHP 리플렉션을 통해 `handle` 또는 `__invoke` 로 시작하는 리스너 클래스 메서드를 찾고, 해당 메서드의 매개변수 타입힌트를 따라 이벤트에 대한 리스너로 등록합니다:

```
use App\Events\PodcastProcessed;

class SendPodcastNotification
{
    /**
     * Handle the given event.
     */
    public function handle(PodcastProcessed $event): void
    {
        // ...
    }
}
```

이벤트 자동 발견은 기본적으로 비활성화되어 있으며, 이를 활성화하려면 애플리케이션 `EventServiceProvider`의 `shouldDiscoverEvents` 메서드를 오버라이드하세요:

```
/**
 * Determine if events and listeners should be automatically discovered.
 */
public function shouldDiscoverEvents(): bool
{
    return true;
}
```

기본적으로 `app/Listeners` 디렉토리가 스캔 대상입니다. 추가로 스캔할 디렉토리를 지정하려면 `discoverEventsWithin` 메서드를 오버라이드하세요:

```
/**
 * Get the listener directories that should be used to discover events.
 *
 * @return array<int, string>
 */
protected function discoverEventsWithin(): array
{
    return [
        $this->app->path('Listeners'),
    ];
}
```

<a name="event-discovery-in-production"></a>
#### 운영 환경에서의 이벤트 자동 발견

운영 환경에서는 매 요청마다 모든 리스너를 스캔하는 것이 비효율적입니다. 따라서 배포 시 `event:cache` Artisan 명령어를 실행해서 애플리케이션 내 모든 이벤트와 리스너의 매니페스트를 캐시하는 것을 권장합니다. 이는 이벤트 등록 작업을 가속화합니다. 캐시를 제거하려면 `event:clear` 명령어를 사용하세요.

<a name="defining-events"></a>
## 이벤트 정의하기

이벤트 클래스는 이벤트와 관련된 정보를 담는 데이터 컨테이너 역할을 합니다. 예를 들어, `App\Events\OrderShipped` 이벤트가 [Eloquent ORM](/docs/10.x/eloquent) 모델 객체를 받는 경우를 살펴봅시다:

```
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

보다시피 이 이벤트 클래스는 별도의 비즈니스 로직을 포함하지 않습니다. 구매된 `App\Models\Order` 인스턴스를 담는 컨테이너일 뿐입니다. 사용된 `SerializesModels` 트레이트는 해당 이벤트 객체가 PHP `serialize` 함수로 직렬화될 때 Eloquent 모델을 우아하게 직렬화해줍니다. 이는 [큐잉된 리스너](#queued-event-listeners)를 사용할 때 유용합니다.

<a name="defining-listeners"></a>
## 리스너 정의하기

다음으로, 위 예시 이벤트에 대한 리스너를 살펴봅시다. 이벤트 리스너는 `handle` 메서드에서 이벤트 인스턴스를 받습니다. `event:generate` 및 `make:listener` Artisan 명령어는 적절한 이벤트 클래스를 자동으로 임포트하고 `handle` 메서드에 타입힌트를 삽입합니다. `handle` 메서드 내에서 이벤트에 대응하는 모든 작업을 수행하면 됩니다:

```
<?php

namespace App\Listeners;

use App\Events\OrderShipped;

class SendShipmentNotification
{
    /**
     * Create the event listener.
     */
    public function __construct()
    {
        // ...
    }

    /**
     * Handle the event.
     */
    public function handle(OrderShipped $event): void
    {
        // $event->order를 통해 주문에 접근...
    }
}
```

> [!NOTE]  
> 이벤트 리스너는 생성자에 필요로 하는 의존성을 타입힌트로 선언할 수 있습니다. 모든 이벤트 리스너는 Laravel [서비스 컨테이너](/docs/10.x/container)로부터 해석(Resolve)되므로 자동으로 의존성 주입이 이루어집니다.

<a name="stopping-the-propagation-of-an-event"></a>
#### 이벤트 전파 중지하기

때로는 이벤트가 다른 리스너들에게 전달되는 것을 중지시키고 싶을 수 있습니다. 이 경우, 리스너의 `handle` 메서드에서 `false`를 반환하면 이벤트 전파가 중지됩니다.

<a name="queued-event-listeners"></a>
## 큐잉된 이벤트 리스너

리스너가 이메일 전송이나 HTTP 요청 같은 느린 작업을 수행해야 할 때는 큐잉이 유용합니다. 큐잉 리스너를 사용하기 전에 반드시 [큐를 설정](/docs/10.x/queues)하고, 서버나 로컬 개발 환경에서 큐 워커를 실행하세요.

리스너 클래스를 큐에 넣으려면 `ShouldQueue` 인터페이스를 구현하면 됩니다. `event:generate` 및 `make:listener` 명령어로 생성되는 리스너는 이미 이 인터페이스를 임포트하므로 바로 사용할 수 있습니다:

```
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    // ...
}
```

이제 이 리스너가 처리하는 이벤트가 디스패치되면, 이벤트 디스패처가 자동으로 Laravel의 [큐 시스템](/docs/10.x/queues)을 통해 리스너를 큐에 넣습니다. 큐에서 리스너가 정상 동작하면, 큐 작업은 처리 완료 후 자동으로 삭제됩니다.

<a name="customizing-the-queue-connection-queue-name"></a>
#### 큐 연결, 큐 이름, 지연 시간 커스터마이즈하기

이벤트 리스너의 큐 연결, 큐 이름, 지연 시간을 사용자 정의하려면, 리스너 클래스 내에 `$connection`, `$queue`, `$delay` 속성을 정의하세요:

```
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
     * 작업이 처리되기 전 대기 시간(초).
     *
     * @var int
     */
    public $delay = 60;
}
```

런타임에 동적으로 큐 설정을 조정하려면, 각각 `viaConnection`, `viaQueue`, `withDelay` 메서드를 정의하면 됩니다:

```
/**
 * 리스너가 사용할 큐 연결 이름 가져오기.
 */
public function viaConnection(): string
{
    return 'sqs';
}

/**
 * 리스너가 사용할 큐 이름 가져오기.
 */
public function viaQueue(): string
{
    return 'listeners';
}

/**
 * 작업이 처리되기 전 대기 시간(초) 가져오기.
 */
public function withDelay(OrderShipped $event): int
{
    return $event->highPriority ? 0 : 60;
}
```

<a name="conditionally-queueing-listeners"></a>
#### 조건부로 리스너 큐잉하기

일부 상황에서는 런타임에 큐잉할지 말지를 결정해야 할 수 있습니다. 이때 리스너에 `shouldQueue` 메서드를 정의하여, 이 메서드가 `false`를 반환하면 큐에 쌓이지 않고 즉시 실행됩니다:

```
<?php

namespace App\Listeners;

use App\Events\OrderCreated;
use Illuminate\Contracts\Queue\ShouldQueue;

class RewardGiftCard implements ShouldQueue
{
    /**
     * 고객에게 상품권 보상.
     */
    public function handle(OrderCreated $event): void
    {
        // ...
    }

    /**
     * 리스너가 큐에 쌓일지 판단.
     */
    public function shouldQueue(OrderCreated $event): bool
    {
        return $event->order->subtotal >= 5000;
    }
}
```

<a name="manually-interacting-with-the-queue"></a>
### 큐와 수동으로 상호작용하기

리스너 내부에서 큐 작업의 `delete` 및 `release` 메서드에 수동으로 접근해야 할 경우, 기본 생성된 리스너에 임포트된 `Illuminate\Queue\InteractsWithQueue` 트레이트를 사용할 수 있습니다. 해당 트레이트는 이런 메서드들을 제공합니다:

```
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\InteractsWithQueue;

class SendShipmentNotification implements ShouldQueue
{
    use InteractsWithQueue;

    /**
     * 이벤트 처리.
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

큐잉된 리스너가 데이터베이스 트랜잭션 내에서 디스패치되면, 큐에서 작업이 데이터베이스 트랜잭션 커밋 전에 처리될 수 있습니다. 이 경우 트랜잭션 중 변경된 모델이나 데이터베이스 레코드가 아직 커밋되지 않아 없는 것처럼 보일 수 있고, 의존하는 모델이 존재하지 않는 경우 예기치 않은 오류가 발생할 수 있습니다.

만약 큐 연결의 `after_commit` 설정이 `false`로 되어 있다면, 리스너 클래스에 `ShouldHandleEventsAfterCommit` 인터페이스를 구현해 해당 리스너만 현재 열려 있는 데이터베이스 트랜잭션 모두가 커밋된 후에 처리하도록 할 수 있습니다:

```
<?php

namespace App\Listeners;

use Illuminate\Contracts\Events\ShouldHandleEventsAfterCommit;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\InteractsWithQueue;

class SendShipmentNotification implements ShouldQueue, ShouldHandleEventsAfterCommit
{
    use InteractsWithQueue;
}
```

> [!NOTE]  
> 이 문제 해결법에 대해 자세히 알고 싶으면, [큐 작업과 데이터베이스 트랜잭션](/docs/10.x/queues#jobs-and-database-transactions) 관련 문서를 참고하세요.

<a name="handling-failed-jobs"></a>
### 실패한 작업 처리하기

가끔 큐잉된 이벤트 리스너가 실패할 수도 있습니다. 큐 작업이 워커에 정의된 최대 재시도 횟수를 초과하면, 리스너의 `failed` 메서드가 호출됩니다. 이 메서드는 이벤트 인스턴스와 실패 원인이 된 `Throwable` 인스턴스를 받습니다:

```
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
     * 이벤트 처리.
     */
    public function handle(OrderShipped $event): void
    {
        // ...
    }

    /**
     * 실패한 작업 처리.
     */
    public function failed(OrderShipped $event, Throwable $exception): void
    {
        // ...
    }
}
```

<a name="specifying-queued-listener-maximum-attempts"></a>
#### 큐잉된 리스너 최대 시도 횟수 지정하기

실패하는 큐 리스너가 무한 재시도되지 않도록, 리스너가 최대 몇 번 시도될지 지정할 수 있습니다. `$tries` 속성을 리스너 클래스에 선언하세요:

```
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\InteractsWithQueue;

class SendShipmentNotification implements ShouldQueue
{
    use InteractsWithQueue;

    /**
     * 큐잉 리스너가 최대 시도할 횟수.
     *
     * @var int
     */
    public $tries = 5;
}
```

또는 시도 횟수 대신 특정 시간까지 시도하도록 하려면, `retryUntil` 메서드를 추가하세요. 이 메서드는 `DateTime` 인스턴스를 반환해야 합니다:

```
use DateTime;

/**
 * 작업이 제한 시간에 도달하는 시점 지정.
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(5);
}
```

<a name="dispatching-events"></a>
## 이벤트 디스패치하기

이벤트를 디스패치하려면, 이벤트 클래스의 정적 `dispatch` 메서드를 호출하면 됩니다. 이 메서드는 `Illuminate\Foundation\Events\Dispatchable` 트레이트로 제공됩니다. `dispatch` 메서드에 전달한 모든 인수는 이벤트 클래스의 생성자에 그대로 전달됩니다:

```
<?php

namespace App\Http\Controllers;

use App\Events\OrderShipped;
use App\Http\Controllers\Controller;
use App\Models\Order;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class OrderShipmentController extends Controller
{
    /**
     * 주어진 주문을 배송 처리.
     */
    public function store(Request $request): RedirectResponse
    {
        $order = Order::findOrFail($request->order_id);

        // 주문 배송 처리 로직...

        OrderShipped::dispatch($order);

        return redirect('/orders');
    }
}
```

조건부로 이벤트를 디스패치하고 싶다면 `dispatchIf` 와 `dispatchUnless` 메서드를 사용할 수 있습니다:

```
OrderShipped::dispatchIf($condition, $order);

OrderShipped::dispatchUnless($condition, $order);
```

> [!NOTE]  
> 테스트 시에는 이벤트 리스너가 실행되지 않도록 하고, 특정 이벤트가 디스패치 되었는지만 검증하는 것이 유용합니다. Laravel의 [내장된 테스트 헬퍼](#testing)를 참고하세요.

<a name="dispatching-events-after-database-transactions"></a>
### 데이터베이스 트랜잭션 후 이벤트 디스패치

가끔 활성 데이터베이스 트랜잭션이 커밋된 후에만 이벤트가 디스패치되게 하고 싶을 때가 있습니다. 이 경우 이벤트 클래스에 `ShouldDispatchAfterCommit` 인터페이스를 구현하세요.

이 인터페이스는 Laravel에 현재 데이터베이스 트랜잭션이 커밋될 때까지 이벤트 디스패치를 미루게 합니다. 트랜잭션이 실패하면 이벤트는 무시됩니다. 만약 실행 시점에 활성 데이터베이스 트랜잭션이 없다면 이벤트는 즉시 디스패치됩니다:

```
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
     * 새 이벤트 인스턴스 생성.
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

이벤트 구독자는 단일 클래스 내에서 여러 이벤트를 구독할 수 있도록 하는 클래스입니다. 구독자는 이벤트 디스패처 인스턴스를 인수로 받는 `subscribe` 메서드를 정의하며, 이 메서드에서 `listen` 호출로 이벤트 리스너를 등록합니다:

```
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

리스너 메서드가 구독자 클래스 내에 모두 정의되어 있다면, `subscribe` 메서드에서 이벤트와 메서드 이름을 배열로 리턴하는 형태가 더 간편할 수 있습니다. Laravel이 구독자 클래스명을 자동으로 알아서 등록해줍니다:

```
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

구독자 클래스를 작성했다면 이벤트 디스패처에 등록할 준비가 된 것입니다. `EventServiceProvider`의 `$subscribe` 속성에 구독자 클래스를 추가하여 등록할 수 있습니다. 예를 들어 `UserEventSubscriber`를 추가해봅시다:

```
<?php

namespace App\Providers;

use App\Listeners\UserEventSubscriber;
use Illuminate\Foundation\Support\Providers\EventServiceProvider as ServiceProvider;

class EventServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션의 이벤트 리스너 매핑.
     *
     * @var array
     */
    protected $listen = [
        // ...
    ];

    /**
     * 등록할 구독자 클래스.
     *
     * @var array
     */
    protected $subscribe = [
        UserEventSubscriber::class,
    ];
}
```

<a name="testing"></a>
## 테스트

이벤트를 디스패치하는 코드를 테스트할 때 실제 이벤트 리스너가 실행되지 않도록 설정하고 싶을 수 있습니다. 리스너 코드는 별개로 직접 테스트할 수 있기 때문입니다. 물론 리스너 자체를 테스트할 때는 인스턴스를 생성하고 `handle` 메서드를 직접 호출하면 됩니다.

`Event` 페사드의 `fake` 메서드를 사용하면 리스너 실행을 중지하고, 테스트하고자 하는 코드를 실행한 후, `assertDispatched`, `assertNotDispatched`, `assertNothingDispatched` 메서드를 통해 어떤 이벤트가 디스패치 되었는지 검증할 수 있습니다:

```
<?php

namespace Tests\Feature;

use App\Events\OrderFailedToShip;
use App\Events\OrderShipped;
use Illuminate\Support\Facades\Event;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * 주문 배송 테스트.
     */
    public function test_orders_can_be_shipped(): void
    {
        Event::fake();

        // 주문 배송 동작 수행...

        // 특정 이벤트가 디스패치 되었는지 확인...
        Event::assertDispatched(OrderShipped::class);

        // 특정 이벤트가 두 번 디스패치 되었는지 확인...
        Event::assertDispatched(OrderShipped::class, 2);

        // 특정 이벤트가 디스패치 되지 않았음을 확인...
        Event::assertNotDispatched(OrderFailedToShip::class);

        // 어떤 이벤트도 디스패치되지 않았음을 확인...
        Event::assertNothingDispatched();
    }
}
```

`assertDispatched` 또는 `assertNotDispatched` 메서드에 클로저를 전달하여, 특정 조건을 만족하는 이벤트가 디스패치 되었는지 검증할 수도 있습니다. 이 경우 조건을 만족하는 이벤트가 하나라도 존재하면 검증이 성공합니다:

```
Event::assertDispatched(function (OrderShipped $event) use ($order) {
    return $event->order->id === $order->id;
});
```

단순히 이벤트 리스너가 특정 이벤트를 듣고 있는지만 확인하고 싶다면 `assertListening` 메서드를 쓸 수 있습니다:

```
Event::assertListening(
    OrderShipped::class,
    SendShipmentNotification::class
);
```

> [!WARNING]  
> `Event::fake()` 호출 이후에는 이벤트 리스너가 모두 실행되지 않습니다. 따라서 모델에 UUID를 생성하는 등 이벤트 의존적인 팩토리를 사용한다면, 팩토리 사용 후 **반드시 `Event::fake()`를 호출하세요.**

<a name="faking-a-subset-of-events"></a>
### 일부 이벤트 페이크하기

일부 특정 이벤트만 페이크하고 싶다면 `fake` 또는 `fakeFor` 메서드에 이벤트 클래스를 배열로 전달하세요:

```
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

    // 다른 이벤트는 정상적으로 디스패치됨...
    $order->update([...]);
}
```

특정 이벤트만 제외하고 모두 페이크하고 싶다면, `except` 메서드를 사용하세요:

```
Event::fake()->except([
    OrderCreated::class,
]);
```

<a name="scoped-event-fakes"></a>
### 범위를 제한한 이벤트 페이크

테스트 중 일부 코드에 한해 이벤트 페이크를 적용하고 싶다면, `fakeFor` 메서드를 사용하세요:

```
<?php

namespace Tests\Feature;

use App\Events\OrderCreated;
use App\Models\Order;
use Illuminate\Support\Facades\Event;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * 주문 처리 테스트.
     */
    public function test_orders_can_be_processed(): void
    {
        $order = Event::fakeFor(function () {
            $order = Order::factory()->create();

            Event::assertDispatched(OrderCreated::class);

            return $order;
        });

        // 이 시점부터 이벤트가 정상적으로 디스패치되고 옵저버도 실행됨...
        $order->update([...]);
    }
}
```