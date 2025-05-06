# 이벤트

- [소개](#introduction)
- [이벤트 및 리스너 등록](#registering-events-and-listeners)
    - [이벤트 및 리스너 생성](#generating-events-and-listeners)
    - [이벤트 수동 등록](#manually-registering-events)
    - [이벤트 자동 감지](#event-discovery)
- [이벤트 정의](#defining-events)
- [리스너 정의](#defining-listeners)
- [큐 처리 이벤트 리스너](#queued-event-listeners)
    - [큐 직접 다루기](#manually-interacting-with-the-queue)
    - [큐 이벤트 리스너와 데이터베이스 트랜잭션](#queued-event-listeners-and-database-transactions)
    - [실패한 작업 처리](#handling-failed-jobs)
- [이벤트 디스패치](#dispatching-events)
    - [트랜잭션 후 이벤트 디스패치](#dispatching-events-after-database-transactions)
- [이벤트 구독자](#event-subscribers)
    - [이벤트 구독자 작성](#writing-event-subscribers)
    - [이벤트 구독자 등록](#registering-event-subscribers)
- [테스트](#testing)
    - [일부 이벤트만 페이크하기](#faking-a-subset-of-events)
    - [스코프가 지정된 이벤트 페이크](#scoped-event-fakes)

<a name="introduction"></a>
## 소개

Laravel의 이벤트는 단순한 옵저버 패턴 구현을 제공하여 애플리케이션 내에서 발생하는 다양한 이벤트를 구독하고 들을 수 있도록 해줍니다. 일반적으로 이벤트 클래스는 `app/Events` 디렉터리에, 리스너는 `app/Listeners` 디렉터리에 저장됩니다. 애플리케이션에 해당 디렉터리가 보이지 않아도 걱정하지 마세요. Artisan 콘솔 명령어를 사용해 이벤트와 리스너를 생성하면 자동으로 디렉터리가 생성됩니다.

이벤트는 애플리케이션의 다양한 부분을 느슨하게 결합하는 데 유용합니다. 하나의 이벤트가 여러 개의 리스너를 가질 수 있고, 이들은 서로 의존하지 않기 때문입니다. 예를 들어, 주문 배송 시마다 사용자에게 Slack 알림을 보내고 싶다고 가정해봅시다. 주문 처리 코드와 Slack 알림 코드를 직접 연결하는 대신, `App\Events\OrderShipped` 이벤트를 발생시키고, 리스너에서 이를 받아 Slack 알림을 전송할 수 있습니다.

<a name="registering-events-and-listeners"></a>
## 이벤트 및 리스너 등록

Laravel 애플리케이션에 포함된 `App\Providers\EventServiceProvider`는 모든 이벤트 리스너를 등록하기에 편리한 위치를 제공합니다. `listen` 프로퍼티는 모든 이벤트(키)와 해당 리스너(값) 배열을 포함합니다. 애플리케이션의 필요에 따라 원하는 만큼 이벤트를 이 배열에 추가할 수 있습니다. 예를 들어, `OrderShipped` 이벤트를 추가해봅시다:

```php
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
> `event:list` 명령어를 사용하면 애플리케이션에 등록된 모든 이벤트와 리스너 목록을 확인할 수 있습니다.

<a name="generating-events-and-listeners"></a>
### 이벤트 및 리스너 생성

각 이벤트와 리스너의 파일을 수동으로 생성하는 것은 번거롭습니다. 대신, `EventServiceProvider`에 리스너와 이벤트를 추가한 뒤 `event:generate` Artisan 명령어를 사용하세요. 이 명령어는 `EventServiceProvider`에 나열되어 있지만 아직 존재하지 않는 이벤트나 리스너 파일을 자동으로 생성해줍니다:

```shell
php artisan event:generate
```

또는, `make:event` 및 `make:listener` Artisan 명령어를 사용하여 각각 별도의 이벤트나 리스너를 생성할 수 있습니다:

```shell
php artisan make:event PodcastProcessed

php artisan make:listener SendPodcastNotification --event=PodcastProcessed
```

<a name="manually-registering-events"></a>
### 이벤트 수동 등록

일반적으로 이벤트는 `EventServiceProvider`의 `$listen` 배열을 통해 등록해야 하지만, 클래스나 클로저 기반의 이벤트 리스너를 `EventServiceProvider`의 `boot` 메서드에서 직접 수동 등록할 수도 있습니다:

```php
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
#### 큐 처리 가능한 익명 이벤트 리스너

클로저 기반 이벤트 리스너를 수동으로 등록할 때, `Illuminate\Events\queueable` 함수를 통해 해당 리스너 클로저를 감싸면 [큐](/docs/{{version}}/queues)를 통해 리스너를 실행하도록 Laravel에 지시할 수 있습니다.

```php
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

큐 작업(job)처럼, `onConnection`, `onQueue`, `delay` 메서드를 통해 큐 리스너 실행 방식을 세밀하게 조정할 수 있습니다:

```php
Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->onConnection('redis')->onQueue('podcasts')->delay(now()->addSeconds(10)));
```

익명 큐 리스너에서 실패를 처리하고 싶다면, `queueable` 리스너 정의 시 `catch` 메서드에 클로저를 전달할 수 있습니다. 이 클로저는 이벤트 인스턴스와 실패 원인이 담긴 `Throwable` 인스턴스를 받습니다:

```php
use App\Events\PodcastProcessed;
use function Illuminate\Events\queueable;
use Illuminate\Support\Facades\Event;
use Throwable;

Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->catch(function (PodcastProcessed $event, Throwable $e) {
    // 큐 리스너가 실패했을 때 처리...
}));
```

<a name="wildcard-event-listeners"></a>
#### 와일드카드 이벤트 리스너

`*` 를 와일드카드 파라미터로 사용하여 여러 이벤트를 하나의 리스너에서 수신할 수 있습니다. 와일드카드 리스너는 첫 번째 인자에 이벤트 이름, 두 번째 인자에 전체 이벤트 데이터 배열을 전달받습니다:

```php
Event::listen('event.*', function (string $eventName, array $data) {
    // ...
});
```

<a name="event-discovery"></a>
### 이벤트 자동 감지

`EventServiceProvider`의 `$listen` 배열에서 이벤트와 리스너를 수동 등록하는 대신, 자동 감지 기능을 활성화할 수 있습니다. 자동 감지가 활성화되면, Laravel은 애플리케이션의 `Listeners` 디렉토리를 스캔하여 이벤트와 리스너를 자동으로 찾고 등록합니다. 여전히 명시적으로 정의된 이벤트는 그대로 등록됩니다.

Laravel은 PHP의 리플렉션 기능을 사용해 리스너 클래스의 메서드 중 `handle` 또는 `__invoke`로 시작하는 메서드를 감지하여, 메서드의 타입힌트된 이벤트에 대해 이벤트 리스너로 등록합니다:

```php
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

이벤트 감지는 기본적으로 비활성화되어 있습니다. 이벤트 감지를 활성화하려면, `EventServiceProvider`에서 `shouldDiscoverEvents` 메서드를 오버라이딩하여 `true`를 반환하면 됩니다:

```php
/**
 * Determine if events and listeners should be automatically discovered.
 */
public function shouldDiscoverEvents(): bool
{
    return true;
}
```

기본적으로 애플리케이션의 `app/Listeners` 디렉토리만 스캔하지만, 추가 스캔 디렉토리를 지정하려면 `discoverEventsWithin` 메서드를 오버라이딩하세요:

```php
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
#### 운영 환경에서의 이벤트 감지

운영 환경에서는 매 요청마다 모든 리스너를 스캔하는 것이 비효율적입니다. 따라서 배포 과정에서 `event:cache` Artisan 명령어를 실행하여 이벤트와 리스너의 목록을 캐시하길 권장합니다. 이 캐시는 프레임워크가 이벤트 등록을 더 빠르게 처리하는 데 사용됩니다. 캐시를 제거하려면 `event:clear` 명령어를 사용하세요.

<a name="defining-events"></a>
## 이벤트 정의

이벤트 클래스는 이벤트와 관련된 정보를 담는 데이터 컨테이너에 불과합니다. 예를 들어, `App\Events\OrderShipped` 이벤트가 [Eloquent ORM](/docs/{{version}}/eloquent) 객체를 받는다고 가정해봅시다:

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

이벤트 클래스는 어떠한 로직도 포함하지 않으며, 구매된 `App\Models\Order` 인스턴스를 담고 있습니다. 이벤트가 [큐 리스너](#queued-event-listeners)에서처럼 PHP의 `serialize` 기능을 이용해 직렬화될 때, `SerializesModels` 트레이트가 Eloquent 모델을 올바르게 직렬화해줍니다.

<a name="defining-listeners"></a>
## 리스너 정의

이제 예제 이벤트의 리스너를 살펴보겠습니다. 이벤트 리스너는 `handle` 메서드에서 이벤트 인스턴스를 전달받습니다. `event:generate`나 `make:listener` Artisan 명령어를 사용해 생성하면 이벤트 클래스가 자동으로 import되고, `handle` 메서드에서 타입힌트까지 지정됩니다. `handle` 안에서는 이벤트에 응답하기 위해 필요한 작업을 수행하면 됩니다.

```php
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
        // $event->order로 주문 정보 접근...
    }
}
```

> [!NOTE]  
> 이벤트 리스너의 생성자에 필요한 의존 객체를 타입힌트로 선언할 수 있습니다. 모든 이벤트 리스너는 Laravel의 [서비스 컨테이너](/docs/{{version}}/container)를 통해 자동으로 주입됩니다.

<a name="stopping-the-propagation-of-an-event"></a>
#### 이벤트 전파 중단

가끔 이벤트가 다른 리스너로 전파되는 것을 중단하고 싶을 수 있습니다. 리스너의 `handle` 메서드에서 `false`를 반환하면 전파를 중단할 수 있습니다.

<a name="queued-event-listeners"></a>
## 큐 처리 이벤트 리스너

이메일 전송이나 HTTP 요청과 같이 시간이 오래 걸리는 작업을 수행하는 리스너는 큐로 처리하는 것이 유리할 수 있습니다. 큐 리스너를 사용하기 전에 [큐를 설정](/docs/{{version}}/queues)하고, 서버 또는 개발 환경에서 큐 워커를 실행하세요.

리스너를 큐에 넣으려면, 리스너 클래스에 `ShouldQueue` 인터페이스를 추가하세요. `event:generate` 및 `make:listener` 명령어로 생성된 리스너에는 이미 이 인터페이스가 import되어 있으니 바로 사용할 수 있습니다.

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

이제 해당 이벤트가 발생하면, 리스너가 자동으로 [라라벨 큐 시스템](docs/{{version}}/queues)에 의해 큐에 적재됩니다. 리스너 실행 시 예외가 발생하지 않는 한, 작업이 완료되고 큐에서 자동으로 삭제됩니다.

<a name="customizing-the-queue-connection-queue-name"></a>
#### 큐 연결, 이름, 지연시간 커스터마이징

특정 이벤트 리스너의 큐 연결, 큐 이름, 큐 지연시간을 커스터마이징하려면, 리스너 클래스에 `$connection`, `$queue`, `$delay` 속성을 정의하세요.

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    /**
     * 작업을 보낼 큐 커넥션 이름
     *
     * @var string|null
     */
    public $connection = 'sqs';

    /**
     * 작업을 보낼 큐 이름
     *
     * @var string|null
     */
    public $queue = 'listeners';

    /**
     * 작업 처리 지연시간(초)
     *
     * @var int
     */
    public $delay = 60;
}
```

런타임에 동적으로 큐 연결/이름/지연시간을 지정하려면, `viaConnection`, `viaQueue`, `withDelay` 메서드를 리스너에 정의하세요.

```php
/**
 * 큐 연결명 반환
 */
public function viaConnection(): string
{
    return 'sqs';
}

/**
 * 큐 이름 반환
 */
public function viaQueue(): string
{
    return 'listeners';
}

/**
 * 지연 처리 시간 반환(초)
 */
public function withDelay(OrderShipped $event): int
{
    return $event->highPriority ? 0 : 60;
}
```

<a name="conditionally-queueing-listeners"></a>
#### 조건부 큐 리스너

런타임 데이터를 바탕으로 리스너가 큐에 들어갈지 판단해야 하는 경우가 있습니다. 이럴 땐 `shouldQueue` 메서드를 추가하세요. `shouldQueue`가 `false`를 반환하면 큐에 들어가지 않습니다.

```php
<?php

namespace App\Listeners;

use App\Events\OrderCreated;
use Illuminate\Contracts\Queue\ShouldQueue;

class RewardGiftCard implements ShouldQueue
{
    /**
     * 고객에게 기프트카드 지급
     */
    public function handle(OrderCreated $event): void
    {
        // ...
    }

    /**
     * 리스너를 큐에 넣을지 여부
     */
    public function shouldQueue(OrderCreated $event): bool
    {
        return $event->order->subtotal >= 5000;
    }
}
```

<a name="manually-interacting-with-the-queue"></a>
### 큐 직접 다루기

리스너의 큐 작업에서 `delete` 및 `release` 메서드를 직접 호출해야 할 경우, `Illuminate\Queue\InteractsWithQueue` 트레이트를 사용하세요. 이 트레이트는 생성된 리스너에 기본 포함되어 있습니다.

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
     * 이벤트 처리
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
### 큐 이벤트 리스너와 데이터베이스 트랜잭션

큐 리스너가 데이터베이스 트랜잭션 내에서 디스패치될 경우, 트랜잭션 커밋 전에 큐에서 처리될 수 있습니다. 이럴 경우, 트랜잭션 내에서 변경된 모델이나 데이터베이스 레코드가 아직 반영되지 않을 수 있으며, 추가된 레코드 역시 아직 데이터베이스에 없을 수 있습니다. 만약 리스너가 이런 모델에 의존한다면, 예기치 못한 에러가 발생할 수 있습니다.

큐 커넥션의 `after_commit` 설정이 `false`라도, 특정 큐 리스너만 모든 오픈된 트랜잭션 커밋 후에 실행하고 싶다면, 리스너 클래스에 `ShouldHandleEventsAfterCommit` 인터페이스를 구현하세요.

```php
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
> 이 문제의 자세한 내용은 [큐 작업과 데이터베이스 트랜잭션](/docs/{{version}}/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="handling-failed-jobs"></a>
### 실패한 작업 처리

큐에 등록된 이벤트 리스너가 실패하는 경우가 있습니다. 큐 리스너가 워커에 정의된 최대 시도 횟수를 초과하면, `failed` 메서드가 호출됩니다. `failed` 메서드에는 이벤트 인스턴스와 발생한 `Throwable`이 전달됩니다:

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
     * 이벤트 처리
     */
    public function handle(OrderShipped $event): void
    {
        // ...
    }

    /**
     * 작업 실패 처리
     */
    public function failed(OrderShipped $event, Throwable $exception): void
    {
        // ...
    }
}
```

<a name="specifying-queued-listener-maximum-attempts"></a>
#### 큐 리스너 최대 시도 횟수 지정

큐 리스너에서 오류가 발생할 때 무한 반복되는 것을 피하려면, 시도 횟수나 시도 기간을 설정할 수 있습니다.

리스너 클래스에 `$tries` 속성을 지정해 실패로 간주되기까지 최대 시도 횟수를 정할 수 있습니다:

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
     * 최대 시도 횟수
     *
     * @var int
     */
    public $tries = 5;
}
```

실패까지의 시도 횟수 외에, 시도 만료 시간을 지정할 수도 있습니다. 특정 시간까지만 무한번 시도하도록 하려면, `retryUntil` 메서드를 추가하세요. 이 메서드는 `DateTime` 인스턴스를 반환해야 합니다:

```php
use DateTime;

/**
 * 리스너 작업의 타임아웃 시간 지정
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(5);
}
```

<a name="dispatching-events"></a>
## 이벤트 디스패치

이벤트를 디스패치하려면, 이벤트 클래스의 정적 `dispatch` 메서드를 호출하면 됩니다. 이 메서드는 `Illuminate\Foundation\Events\Dispatchable` 트레이트에 의해 제공됩니다. `dispatch`에 전달하는 인자는 이벤트의 생성자로 전달됩니다.

```php
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
     * 선택 주문 배송 처리
     */
    public function store(Request $request): RedirectResponse
    {
        $order = Order::findOrFail($request->order_id);

        // 주문 배송 로직...

        OrderShipped::dispatch($order);

        return redirect('/orders');
    }
}
```

조건부로 이벤트를 디스패치하고 싶다면 `dispatchIf`, `dispatchUnless` 메서드를 사용할 수 있습니다:

```php
OrderShipped::dispatchIf($condition, $order);

OrderShipped::dispatchUnless($condition, $order);
```

> [!NOTE]  
> 테스트 시, 실제로 리스너를 실행하지 않고 특정 이벤트가 디스패치 됐는지만 확인하고 싶을 수 있습니다. Laravel의 [테스트 헬퍼](#testing)를 활용하면 쉽습니다.

<a name="dispatching-events-after-database-transactions"></a>
### 트랜잭션 후 이벤트 디스패치

가끔은 데이터베이스 트랜잭션이 성공적으로 커밋된 후에만 이벤트를 디스패치하고 싶을 수 있습니다. 이럴 땐 이벤트 클래스에 `ShouldDispatchAfterCommit` 인터페이스를 구현하세요.

이 인터페이스를 사용하면, 트랜잭션이 커밋되기 전에는 이벤트가 디스패치되지 않고, 트랜잭션이 실패하면 이벤트는 버려집니다. 트랜잭션 중이 아닐 때 발생하면, 즉시 이벤트가 디스패치됩니다.

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
     * 새 이벤트 인스턴스 생성
     */
    public function __construct(
        public Order $order,
    ) {}
}
```

<a name="event-subscribers"></a>
## 이벤트 구독자

<a name="writing-event-subscribers"></a>
### 이벤트 구독자 작성

이벤트 구독자는 하나의 클래스에서 여러 이벤트를 구독할 수 있도록 해줍니다. 구독자 클래스에서는 여러 이벤트 핸들러를 정의할 수 있습니다. 구독자 클래스는 `subscribe` 메서드를 정의해야 하며, 이벤트 디스패처 인스턴스를 전달받습니다. 이 인스턴스를 사용하여 `listen` 메서드로 이벤트 리스너를 등록하세요.

```php
<?php

namespace App\Listeners;

use Illuminate\Auth\Events\Login;
use Illuminate\Auth\Events\Logout;
use Illuminate\Events\Dispatcher;

class UserEventSubscriber
{
    /**
     * 사용자 로그인 이벤트 처리
     */
    public function handleUserLogin(Login $event): void {}

    /**
     * 사용자 로그아웃 이벤트 처리
     */
    public function handleUserLogout(Logout $event): void {}

    /**
     * 구독자에 대한 리스너 등록
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

이벤트 리스너 메서드가 구독자 내부에 정의되어 있다면, `subscribe`에서 이벤트와 메서드 명의 배열을 반환하는 것이 더 편리할 수 있습니다. Laravel은 구독자 클래스 이름을 자동으로 감지합니다:

```php
<?php

namespace App\Listeners;

use Illuminate\Auth\Events\Login;
use Illuminate\Auth\Events\Logout;
use Illuminate\Events\Dispatcher;

class UserEventSubscriber
{
    /**
     * 사용자 로그인 이벤트 처리
     */
    public function handleUserLogin(Login $event): void {}

    /**
     * 사용자 로그아웃 이벤트 처리
     */
    public function handleUserLogout(Logout $event): void {}

    /**
     * 구독자에 대한 리스너 등록
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

구독자를 작성했다면 이벤트 디스패처에 등록해야 합니다. `EventServiceProvider`의 `$subscribe` 프로퍼티에 구독자 클래스를 추가하면 됩니다. 아래는 `UserEventSubscriber`를 등록하는 예시입니다:

```php
<?php

namespace App\Providers;

use App\Listeners\UserEventSubscriber;
use Illuminate\Foundation\Support\Providers\EventServiceProvider as ServiceProvider;

class EventServiceProvider extends ServiceProvider
{
    /**
     * 이벤트 리스너 매핑
     *
     * @var array
     */
    protected $listen = [
        // ...
    ];

    /**
     * 등록할 구독자 클래스 배열
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

이벤트를 디스패치하는 코드를 테스트할 때, 리스너를 실제로 실행하지 않도록 하고 싶을 수 있습니다. 리스너의 코드는 별도로 테스트할 수 있기 때문입니다. 리스너를 직접 테스트할 땐, 리스너 인스턴스를 인스턴스화한 뒤 `handle` 메서드를 직접 호출하면 됩니다.

`Event` 파사드의 `fake` 메서드를 사용하면 리스너 실행 없이 테스트 코드를 실행하고, `assertDispatched`, `assertNotDispatched`, `assertNothingDispatched` 메서드를 사용해 어떤 이벤트가 디스패치헸는지 검증할 수 있습니다:

```php
<?php

namespace Tests\Feature;

use App\Events\OrderFailedToShip;
use App\Events\OrderShipped;
use Illuminate\Support\Facades\Event;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * 주문 배송 테스트
     */
    public function test_orders_can_be_shipped(): void
    {
        Event::fake();

        // 주문 배송 수행...

        // 이벤트가 디스패치됐는지 단언...
        Event::assertDispatched(OrderShipped::class);

        // 이벤트가 2번 디스패치됐는지 단언...
        Event::assertDispatched(OrderShipped::class, 2);

        // 이벤트가 디스패치되지 않았는지 단언...
        Event::assertNotDispatched(OrderFailedToShip::class);

        // 아무런 이벤트도 디스패치되지 않았는지 단언...
        Event::assertNothingDispatched();
    }
}
```

특정 이벤트가 "진실 테스트"를 통과하는 경우만 디스패치를 단언하고 싶다면, `assertDispatched`나 `assertNotDispatched`에 클로저를 전달하세요. 한 번이라도 해당 조건을 만족하면 단언이 통과합니다:

```php
Event::assertDispatched(function (OrderShipped $event) use ($order) {
    return $event->order->id === $order->id;
});
```

특정 이벤트에 리스너가 등록되어 있는지만 단언하고 싶다면 `assertListening`을 사용하세요:

```php
Event::assertListening(
    OrderShipped::class,
    SendShipmentNotification::class
);
```

> [!WARNING]  
> `Event::fake()`를 호출하면 리스너 실행이 완전히 중단됩니다. 따라서 모델의 `creating` 이벤트 등 이벤트에 의존하는 팩토리 기능을 사용할 경우, 팩토리 사용 **이후에** `Event::fake()`를 호출하세요.

<a name="faking-a-subset-of-events"></a>
### 일부 이벤트만 페이크하기

특정 이벤트만 페이크하고 싶을 경우, `fake`나 `fakeFor` 메서드에 해당 이벤트 배열을 전달하세요:

```php
/**
 * 주문 프로세스 테스트
 */
public function test_orders_can_be_processed(): void
{
    Event::fake([
        OrderCreated::class,
    ]);

    $order = Order::factory()->create();

    Event::assertDispatched(OrderCreated::class);

    // 나머지 이벤트는 평소처럼 디스패치됨
    $order->update([...]);
}
```

특정 이벤트를 제외한 모든 이벤트를 페이크하려면 `except` 메서드를 사용하세요:

```php
Event::fake()->except([
    OrderCreated::class,
]);
```

<a name="scoped-event-fakes"></a>
### 스코프가 지정된 이벤트 페이크

테스트의 특정 시점에서만 이벤트 리스너를 페이크하고 싶다면 `fakeFor` 메서드를 사용하세요:

```php
<?php

namespace Tests\Feature;

use App\Events\OrderCreated;
use App\Models\Order;
use Illuminate\Support\Facades\Event;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * 주문 프로세스 테스트
     */
    public function test_orders_can_be_processed(): void
    {
        $order = Event::fakeFor(function () {
            $order = Order::factory()->create();

            Event::assertDispatched(OrderCreated::class);

            return $order;
        });

        // 이후에는 정상적으로 이벤트가 디스패치되고, 옵저버도 실행됨
        $order->update([...]);
    }
}
```