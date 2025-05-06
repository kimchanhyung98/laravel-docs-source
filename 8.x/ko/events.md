# 이벤트

- [소개](#introduction)
- [이벤트 및 리스너 등록](#registering-events-and-listeners)
    - [이벤트 및 리스너 생성](#generating-events-and-listeners)
    - [이벤트 수동 등록](#manually-registering-events)
    - [이벤트 자동 감지](#event-discovery)
- [이벤트 정의](#defining-events)
- [리스너 정의](#defining-listeners)
- [큐잉된 이벤트 리스너](#queued-event-listeners)
    - [큐 직접 제어](#manually-interacting-with-the-queue)
    - [큐잉된 이벤트 리스너와 DB 트랜잭션](#queued-event-listeners-and-database-transactions)
    - [실패한 작업 처리](#handling-failed-jobs)
- [이벤트 디스패치](#dispatching-events)
- [이벤트 구독자](#event-subscribers)
    - [이벤트 구독자 작성](#writing-event-subscribers)
    - [이벤트 구독자 등록](#registering-event-subscribers)

<a name="introduction"></a>
## 소개

Laravel의 이벤트는 간단한 옵저버 패턴 구현을 제공하여 애플리케이션 내에서 발생하는 다양한 이벤트를 구독하고 감지할 수 있도록 해줍니다. 이벤트 클래스는 일반적으로 `app/Events` 디렉터리에, 이벤트 리스너는 `app/Listeners` 디렉터리에 저장됩니다. 만약 애플리케이션에 해당 디렉터리가 없다면 Artisan 콘솔 명령어로 이벤트와 리스너를 생성할 때 자동으로 생성됩니다.

이벤트는 애플리케이션의 다양한 부분을 분리(디커플링)하는 좋은 방식입니다. 하나의 이벤트에 여러 리스너를 지정할 수 있지만, 리스너들은 서로 의존하지 않습니다. 예를 들어, 주문이 배송될 때마다 사용자에게 Slack 알림을 보내고 싶을 수 있습니다. 주문 처리 코드와 Slack 알림 코드를 직접 연결하는 대신, `App\Events\OrderShipped` 이벤트를 발생시키고 리스너를 통해 Slack 알림을 전송할 수 있습니다.

<a name="registering-events-and-listeners"></a>
## 이벤트 및 리스너 등록

Laravel 애플리케이션에 포함된 `App\Providers\EventServiceProvider`는 애플리케이션의 모든 이벤트 리스너를 등록할 수 있는 편리한 위치를 제공합니다. `listen` 프로퍼티에는 모든 이벤트(키)와 해당 리스너(값) 배열이 포함됩니다. 애플리케이션에 필요한 만큼 이벤트를 이 배열에 추가할 수 있습니다. 예를 들어, `OrderShipped` 이벤트를 등록하면 다음과 같습니다:

```php
use App\Events\OrderShipped;
use App\Listeners\SendShipmentNotification;

/**
 * The event listener mappings for the application.
 *
 * @var array
 */
protected $listen = [
    OrderShipped::class => [
        SendShipmentNotification::class,
    ],
];
```

> {tip} `event:list` 명령어를 사용하면 애플리케이션에 등록된 모든 이벤트 및 리스너 목록을 볼 수 있습니다.

<a name="generating-events-and-listeners"></a>
### 이벤트 및 리스너 생성

각 이벤트와 리스너 파일을 수동으로 만드는 것은 번거로울 수 있습니다. 대신, 리스너와 이벤트를 `EventServiceProvider`에 추가한 후, `event:generate` Artisan 명령어를 사용하세요. 이 명령어는 `EventServiceProvider`에 등록된 이미 존재하지 않는 이벤트나 리스너 파일을 생성합니다:

```
php artisan event:generate
```

또는, 각각의 이벤트와 리스너를 생성하기 위해 `make:event`와 `make:listener` Artisan 명령어를 사용할 수도 있습니다:

```
php artisan make:event PodcastProcessed

php artisan make:listener SendPodcastNotification --event=PodcastProcessed
```

<a name="manually-registering-events"></a>
### 이벤트 수동 등록

일반적으로 이벤트는 `EventServiceProvider`의 `$listen` 배열을 통해 등록해야 하지만, 클래스 또는 클로저 방식의 이벤트 리스너를 `EventServiceProvider`의 `boot` 메소드에서 직접 등록할 수도 있습니다:

```php
use App\Events\PodcastProcessed;
use App\Listeners\SendPodcastNotification;
use Illuminate\Support\Facades\Event;

/**
 * Register any other events for your application.
 *
 * @return void
 */
public function boot()
{
    Event::listen(
        PodcastProcessed::class,
        [SendPodcastNotification::class, 'handle']
    );

    Event::listen(function (PodcastProcessed $event) {
        //
    });
}
```

<a name="queuable-anonymous-event-listeners"></a>
#### 큐잉 가능한 익명 이벤트 리스너

클로저 기반 이벤트 리스너를 수동으로 등록할 때, `Illuminate\Events\queueable` 함수를 사용해 리스너 클로저를 감싸면 Laravel이 해당 리스너를 [큐](/docs/{{version}}/queues)를 사용하여 실행하도록 할 수 있습니다.

```php
use App\Events\PodcastProcessed;
use function Illuminate\Events\queueable;
use Illuminate\Support\Facades\Event;

public function boot()
{
    Event::listen(queueable(function (PodcastProcessed $event) {
        //
    }));
}
```

큐잉된 작업과 마찬가지로, `onConnection`, `onQueue`, `delay` 메서드를 사용하여 큐잉된 리스너의 실행을 커스터마이즈할 수 있습니다:

```php
Event::listen(queueable(function (PodcastProcessed $event) {
    //
})->onConnection('redis')->onQueue('podcasts')->delay(now()->addSeconds(10)));
```

익명 큐잉 리스너의 실패를 처리하고 싶다면, `queueable` 리스너를 정의할 때 `catch` 메소드에 클로저를 제공할 수 있습니다. 이 클로저는 이벤트 인스턴스와 실패 원인이 된 `Throwable` 인스턴스를 전달받습니다:

```php
use App\Events\PodcastProcessed;
use function Illuminate\Events\queueable;
use Illuminate\Support\Facades\Event;
use Throwable;

Event::listen(queueable(function (PodcastProcessed $event) {
    //
})->catch(function (PodcastProcessed $event, Throwable $e) {
    // 큐잉된 리스너가 실패했습니다...
}));
```

<a name="wildcard-event-listeners"></a>
#### 와일드카드 이벤트 리스너

`*`를 와일드카드 매개변수로 사용하여 하나의 리스너에서 여러 이벤트를 잡을 수도 있습니다. 와일드카드 리스너는 첫 번째 인자로 이벤트 이름, 두 번째 인자로 전체 이벤트 데이터 배열을 받습니다:

```php
Event::listen('event.*', function ($eventName, array $data) {
    //
});
```

<a name="event-discovery"></a>
### 이벤트 자동 감지

`EventServiceProvider`의 `$listen` 배열에 이벤트와 리스너를 수동으로 등록하는 대신, 자동 이벤트 감지를 활성화할 수 있습니다. 자동 감지 기능을 사용하면, Laravel이 애플리케이션의 `Listeners` 디렉터리를 스캔하여 이벤트와 리스너를 자동으로 등록합니다. 또한 `EventServiceProvider`에 명시적으로 정의된 이벤트도 계속 등록됩니다.

Laravel은 PHP의 reflection 기능을 사용하여 리스너 클래스를 스캔하고, `handle`로 시작하는 모든 메서드를 해당 타입힌트된 이벤트의 리스너로 등록합니다:

```php
use App\Events\PodcastProcessed;

class SendPodcastNotification
{
    /**
     * Handle the given event.
     *
     * @param  \App\Events\PodcastProcessed  $event
     * @return void
     */
    public function handle(PodcastProcessed $event)
    {
        //
    }
}
```

이벤트 자동 감지는 기본적으로 비활성화되어 있지만, 애플리케이션의 `EventServiceProvider`에서 `shouldDiscoverEvents` 메서드를 오버라이드하여 활성화할 수 있습니다:

```php
/**
 * Determine if events and listeners should be automatically discovered.
 *
 * @return bool
 */
public function shouldDiscoverEvents()
{
    return true;
}
```

기본적으로 애플리케이션의 `app/Listeners` 디렉터리 내 리스너만 스캔합니다. 추가로 스캔할 디렉터리를 지정하고 싶다면, `discoverEventsWithin` 메서드를 오버라이드하면 됩니다:

```php
/**
 * Get the listener directories that should be used to discover events.
 *
 * @return array
 */
protected function discoverEventsWithin()
{
    return [
        $this->app->path('Listeners'),
    ];
}
```

<a name="event-discovery-in-production"></a>
#### 운영 환경에서의 이벤트 자동 감지

운영 환경에서는 모든 요청마다 모든 리스너를 스캔하는 것은 비효율적입니다. 따라서 배포 과정에서 `event:cache` Artisan 명령어를 실행하여 모든 이벤트와 리스너의 매니페스트를 캐싱해야 합니다. 이 매니페스트는 이벤트 등록 과정을 빠르게 만드는 데 사용됩니다. 캐시를 삭제하려면 `event:clear` 명령어를 사용하세요.

<a name="defining-events"></a>
## 이벤트 정의

이벤트 클래스는 이벤트와 관련된 정보를 담는 데이터 컨테이너입니다. 예를 들어, `App\Events\OrderShipped` 이벤트는 [Eloquent ORM](/docs/{{version}}/eloquent) 객체를 받을 수 있습니다:

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
     * The order instance.
     *
     * @var \App\Models\Order
     */
    public $order;

    /**
     * Create a new event instance.
     *
     * @param  \App\Models\Order  $order
     * @return void
     */
    public function __construct(Order $order)
    {
        $this->order = $order;
    }
}
```

위 예시에서 보듯이, 이벤트 클래스에는 별도의 로직이 없습니다. 단순히 구매된 `App\Models\Order` 인스턴스를 담는 용기 역할입니다. 이벤트에서 사용하는 `SerializesModels` 트레이트는 PHP의 `serialize` 함수로 이벤트 객체가 직렬화될 때 Eloquent 모델을 안전하게 직렬화해 줍니다. ([큐잉된 리스너](#queued-event-listeners) 사용 시 필요합니다.)

<a name="defining-listeners"></a>
## 리스너 정의

다음으로, 위 예시 이벤트의 리스너를 살펴봅시다. 이벤트 리스너는 `handle` 메서드에서 이벤트 인스턴스를 전달받습니다. `event:generate`와 `make:listener` Artisan 명령어 모두 올바른 이벤트 클래스 임포트와 타입힌트를 자동으로 처리합니다. `handle` 메서드 안에서 이벤트에 반응하는 모든 작업을 할 수 있습니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;

class SendShipmentNotification
{
    /**
     * Create the event listener.
     *
     * @return void
     */
    public function __construct()
    {
        //
    }

    /**
     * Handle the event.
     *
     * @param  \App\Events\OrderShipped  $event
     * @return void
     */
    public function handle(OrderShipped $event)
    {
        // $event->order로 주문에 접근...
    }
}
```

> {tip} 이벤트 리스너의 생성자에서도 의존성을 타입힌트할 수 있습니다. 모든 이벤트 리스너는 Laravel [서비스 컨테이너](/docs/{{version}}/container)로 해석되므로, 의존성 주입이 자동으로 이루어집니다.

<a name="stopping-the-propagation-of-an-event"></a>
#### 이벤트 전파 중지

때때로 특정 이벤트가 다른 리스너로 전파되는 것을 중지하고 싶을 수 있습니다. 리스너의 `handle` 메서드에서 `false`를 반환하면 이벤트의 전파가 중지됩니다.

<a name="queued-event-listeners"></a>
## 큐잉된 이벤트 리스너

이메일 전송이나 HTTP 요청 등 리스너에서 느린 작업을 수행해야 한다면, 리스너를 큐로 처리하는 것이 좋습니다. 큐잉된 리스너를 사용하기 전에 반드시 [큐 구성](/docs/{{version}}/queues) 및 서버나 개발 환경에서 큐 워커를 시작하세요.

리스너를 큐로 처리하도록 지정하려면 리스너 클래스에 `ShouldQueue` 인터페이스를 추가하면 됩니다. `event:generate`와 `make:listener` Artisan 명령어로 생성된 리스너에는 이 인터페이스가 자동으로 임포트되어 있습니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    //
}
```

이제 이 리스너가 처리하는 이벤트가 발생되면, Laravel의 [큐 시스템](/docs/{{version}}/queues)으로 자동으로 큐잉됩니다. 리스너가 큐에서 실행될 때 예외가 발생하지 않는다면, 작업 처리 후 큐에서 자동으로 삭제됩니다.

<a name="customizing-the-queue-connection-queue-name"></a>
#### 큐 연결 및 큐 이름 커스터마이즈

이벤트 리스너의 큐 연결, 큐 이름, 지연 시간 등 커스터마이즈가 필요한 경우, 리스너 클래스에 `$connection`, `$queue`, `$delay` 프로퍼티를 정의할 수 있습니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    /**
     * 작업이 전송될 연결의 이름.
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
     * 작업이 처리되기 전까지 대기할 시간(초).
     *
     * @var int
     */
    public $delay = 60;
}
```

실행 시점에 큐 연결이나 큐 이름을 동적으로 지정하려면, `viaConnection` 또는 `viaQueue` 메서드를 리스너에 추가하면 됩니다:

```php
/**
 * 리스너의 큐 연결 이름을 반환.
 *
 * @return string
 */
public function viaConnection()
{
    return 'sqs';
}

/**
 * 리스너의 큐 이름을 반환.
 *
 * @return string
 */
public function viaQueue()
{
    return 'listeners';
}
```

<a name="conditionally-queueing-listeners"></a>
#### 조건부 큐잉

실행 시점에 정보를 기반으로 큐잉 여부를 결정해야 할 때, 리스너에 `shouldQueue` 메서드를 추가할 수 있습니다. 이 메서드가 `false`를 반환하면 해당 리스너는 큐잉되지 않습니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderCreated;
use Illuminate\Contracts\Queue\ShouldQueue;

class RewardGiftCard implements ShouldQueue
{
    /**
     * 고객에게 기프트 카드를 지급합니다.
     *
     * @param  \App\Events\OrderCreated  $event
     * @return void
     */
    public function handle(OrderCreated $event)
    {
        //
    }

    /**
     * 리스너가 큐잉될지 여부를 결정합니다.
     *
     * @param  \App\Events\OrderCreated  $event
     * @return bool
     */
    public function shouldQueue(OrderCreated $event)
    {
        return $event->order->subtotal >= 5000;
    }
}
```

<a name="manually-interacting-with-the-queue"></a>
### 큐 직접 제어

리스너가 가진 큐 작업의 `delete`와 `release` 메서드에 직접 접근할 필요가 있다면, `Illuminate\Queue\InteractsWithQueue` 트레이트를 사용하면 됩니다. 이 트레이트는 기본적으로 자동 생성된 리스너에 포함되어 있습니다:

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
     * 이벤트 처리.
     *
     * @param  \App\Events\OrderShipped  $event
     * @return void
     */
    public function handle(OrderShipped $event)
    {
        if (true) {
            $this->release(30);
        }
    }
}
```

<a name="queued-event-listeners-and-database-transactions"></a>
### 큐잉된 이벤트 리스너와 DB 트랜잭션

큐잉된 리스너가 데이터베이스 트랜잭션 내에서 디스패치될 때, 큐에서 트랜잭션 커밋 전에 리스너가 처리될 수 있습니다. 이렇게 되면, 트랜잭션 중 변경된 모델이나 레코드가 아직 DB에 반영되지 않았을 수 있습니다. 만약 리스너가 이런 모델에 의존한다면 예기치 않은 에러가 발생할 수 있습니다.

만약 큐 연결의 `after_commit` 구성 옵션이 `false`라면, 리스너 클래스에 `$afterCommit` 프로퍼티를 정의해 해당 리스너가 트랜잭션 커밋 이후에 디스패치되도록 지정할 수 있습니다:

```php
<?php

namespace App\Listeners;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\InteractsWithQueue;

class SendShipmentNotification implements ShouldQueue
{
    use InteractsWithQueue;

    public $afterCommit = true;
}
```

> {tip} 이 문제를 해결하는 더 자세한 방법은 [큐 작업과 데이터베이스 트랜잭션](/docs/{{version}}/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="handling-failed-jobs"></a>
### 실패한 작업 처리

큐잉된 이벤트 리스너가 실패하는 경우, 큐 워커에서 지정된 최대 재시도 횟수를 초과하면 리스너의 `failed` 메서드가 호출됩니다. 이 메서드는 이벤트 인스턴스와 실패 원인이 된 `Throwable`을 전달받습니다:

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
     * 이벤트 처리.
     *
     * @param  \App\Events\OrderShipped  $event
     * @return void
     */
    public function handle(OrderShipped $event)
    {
        //
    }

    /**
     * 작업 실패 처리.
     *
     * @param  \App\Events\OrderShipped  $event
     * @param  \Throwable  $exception
     * @return void
     */
    public function failed(OrderShipped $event, $exception)
    {
        //
    }
}
```

<a name="specifying-queued-listener-maximum-attempts"></a>
#### 큐잉된 리스너의 최대 시도 횟수 지정

큐잉된 리스너가 에러를 만났을 때 무한 재시도를 막으려면, Laravel은 리스너의 시도 횟수나 기간을 지정할 수 있는 다양한 방법을 제공합니다.

리스너 클래스에 `$tries` 프로퍼티를 정의하여 최대 시도 횟수를 설정할 수 있습니다:

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
     * 큐잉된 리스너의 최대 시도 횟수.
     *
     * @var int
     */
    public $tries = 5;
}
```

실패 전 시도 횟수 대신, 특정 시간 이후에는 리스너가 더 이상 시도되지 않도록 설정할 수도 있습니다. 이를 위해 리스너 클래스에 `retryUntil` 메서드를 추가하면 됩니다. 이 메서드는 `DateTime` 인스턴스를 반환해야 합니다:

```php
/**
 * 리스너의 타임아웃 시간을 결정합니다.
 *
 * @return \DateTime
 */
public function retryUntil()
{
    return now()->addMinutes(5);
}
```

<a name="dispatching-events"></a>
## 이벤트 디스패치

이벤트를 디스패치하려면, 이벤트 클래스의 정적 `dispatch` 메서드를 호출합니다. 이 메서드는 `Illuminate\Foundation\Events\Dispatchable` 트레이트 덕분에 제공됩니다. `dispatch`에 전달한 인자는 이벤트 생성자에 전달됩니다:

```php
<?php

namespace App\Http\Controllers;

use App\Events\OrderShipped;
use App\Http\Controllers\Controller;
use App\Models\Order;
use Illuminate\Http\Request;

class OrderShipmentController extends Controller
{
    /**
     * 지정된 주문을 배송합니다.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        $order = Order::findOrFail($request->order_id);

        // 주문 배송 처리 로직...

        OrderShipped::dispatch($order);
    }
}
```

> {tip} 테스트 시에는 실제로 리스너가 동작하지 않고도 특정 이벤트가 디스패치되었는지 검증할 수 있습니다. Laravel의 [빌트인 테스트 헬퍼](/docs/{{version}}/mocking#event-fake)를 사용해보세요.

<a name="event-subscribers"></a>
## 이벤트 구독자

<a name="writing-event-subscribers"></a>
### 이벤트 구독자 작성

이벤트 구독자는 한 클래스 내에서 여러 이벤트를 구독할 수 있도록 해줍니다. 구독자 클래스는 `subscribe` 메서드를 정의해야 하며, 이 메서드는 이벤트 디스패처 인스턴스를 전달받습니다. 전달된 디스패처의 `listen` 메서드를 통해 이벤트 리스너를 등록할 수 있습니다:

```php
<?php

namespace App\Listeners;

use Illuminate\Auth\Events\Login;
use Illuminate\Auth\Events\Logout;

class UserEventSubscriber
{
    /**
     * 사용자 로그인 이벤트 처리
     */
    public function handleUserLogin($event) {}

    /**
     * 사용자 로그아웃 이벤트 처리
     */
    public function handleUserLogout($event) {}

    /**
     * 구독자를 위한 리스너 등록.
     *
     * @param  \Illuminate\Events\Dispatcher  $events
     * @return void
     */
    public function subscribe($events)
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

이벤트 리스너 메서드가 구독자 내부에 모두 정의되어 있다면, `subscribe`에서 이벤트와 메서드명을 배열로 반환하는 방식도 편리합니다. Laravel은 자동으로 클래스 이름을 유추합니다:

```php
<?php

namespace App\Listeners;

use Illuminate\Auth\Events\Login;
use Illuminate\Auth\Events\Logout;

class UserEventSubscriber
{
    /**
     * 사용자 로그인 이벤트 처리
     */
    public function handleUserLogin($event) {}

    /**
     * 사용자 로그아웃 이벤트 처리
     */
    public function handleUserLogout($event) {}

    /**
     * 구독자를 위한 리스너 등록.
     *
     * @param  \Illuminate\Events\Dispatcher  $events
     * @return array
     */
    public function subscribe($events)
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

구독자 클래스를 작성한 후, 실제로 이벤트 디스패처에 등록할 수 있습니다. 구독자는 `EventServiceProvider`의 `$subscribe` 프로퍼티에 등록합니다. 예를 들어, `UserEventSubscriber`를 추가하는 방법은 다음과 같습니다:

```php
<?php

namespace App\Providers;

use App\Listeners\UserEventSubscriber;
use Illuminate\Foundation\Support\Providers\EventServiceProvider as ServiceProvider;

class EventServiceProvider extends ServiceProvider
{
    /**
     * The event listener mappings for the application.
     *
     * @var array
     */
    protected $listen = [
        //
    ];

    /**
     * The subscriber classes to register.
     *
     * @var array
     */
    protected $subscribe = [
        UserEventSubscriber::class,
    ];
}
```
