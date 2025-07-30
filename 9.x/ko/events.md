# 이벤트 (Events)

- [소개](#introduction)
- [이벤트 및 리스너 등록](#registering-events-and-listeners)
    - [이벤트 및 리스너 생성](#generating-events-and-listeners)
    - [이벤트를 수동으로 등록하기](#manually-registering-events)
    - [이벤트 자동 발견(Event Discovery)](#event-discovery)
- [이벤트 정의하기](#defining-events)
- [리스너 정의하기](#defining-listeners)
- [대기열(큐) 처리 이벤트 리스너](#queued-event-listeners)
    - [대기열과 수동으로 상호작용하기](#manually-interacting-with-the-queue)
    - [대기열 처리 이벤트 리스너와 데이터베이스 트랜잭션](#queued-event-listeners-and-database-transactions)
    - [실패한 작업 처리하기](#handling-failed-jobs)
- [이벤트 발생시키기](#dispatching-events)
- [이벤트 구독자(Event Subscribers)](#event-subscribers)
    - [이벤트 구독자 작성하기](#writing-event-subscribers)
    - [이벤트 구독자 등록하기](#registering-event-subscribers)

<a name="introduction"></a>
## 소개

Laravel의 이벤트는 간단한 옵저버 패턴(observer pattern) 구현체를 제공하여, 애플리케이션 내에서 발생하는 다양한 이벤트를 구독하고 청취할 수 있게 합니다. 이벤트 클래스는 일반적으로 `app/Events` 디렉토리에 저장되고, 해당 이벤트를 처리하는 리스너는 `app/Listeners`에 저장됩니다. 만약 애플리케이션에서 이 디렉토리가 보이지 않아도 걱정할 필요가 없습니다. Artisan 콘솔 명령어로 이벤트와 리스너를 생성하면 자동으로 생성됩니다.

이벤트는 애플리케이션의 여러 부분을 느슨하게 결합하는 데 아주 효과적입니다. 하나의 이벤트가 여러 리스너를 가질 수 있으며, 이 리스너들은 서로 독립적입니다. 예를 들어, 주문이 발송될 때마다 사용자에게 Slack 알림을 보내고 싶다고 가정해 보겠습니다. 주문 처리 코드와 Slack 알림 코드를 직접 연결하는 대신, `App\Events\OrderShipped` 이벤트를 발생시키고, 이 이벤트를 수신하는 리스너에서 Slack 알림을 처리할 수 있습니다.

<a name="registering-events-and-listeners"></a>
## 이벤트 및 리스너 등록

Laravel 애플리케이션에 기본 포함된 `App\Providers\EventServiceProvider`는 모든 애플리케이션 이벤트 리스너를 등록할 수 있는 편리한 장소를 제공합니다. 이 클래스의 `listen` 속성은 모든 이벤트(키)와 그에 대응하는 리스너(값)를 배열로 포함합니다. 필요에 따라 이 배열에 원하는 만큼 이벤트를 추가할 수 있습니다. 예를 들어, `OrderShipped` 이벤트를 다음과 같이 등록할 수 있습니다:

```php
use App\Events\OrderShipped;
use App\Listeners\SendShipmentNotification;

/**
 * 애플리케이션의 이벤트 리스너 매핑.
 *
 * @var array
 */
protected $listen = [
    OrderShipped::class => [
        SendShipmentNotification::class,
    ],
];
```

> [!NOTE]
> `event:list` 명령어를 사용하면 애플리케이션에 등록된 모든 이벤트와 리스너 목록을 출력할 수 있습니다.

<a name="generating-events-and-listeners"></a>
### 이벤트 및 리스너 생성

물론, 각각의 이벤트와 리스너 파일을 수동으로 만드는 것은 번거롭습니다. 대신, `EventServiceProvider`에 이벤트와 리스너를 추가한 후 `event:generate` Artisan 명령어를 사용하세요. 이 명령어는 `EventServiceProvider`에 정의되어 있지만 아직 존재하지 않는 이벤트 또는 리스너를 자동 생성합니다:

```shell
php artisan event:generate
```

또는 개별 이벤트와 리스너를 만들기 위해 `make:event`와 `make:listener` Artisan 명령어를 사용할 수도 있습니다:

```shell
php artisan make:event PodcastProcessed

php artisan make:listener SendPodcastNotification --event=PodcastProcessed
```

<a name="manually-registering-events"></a>
### 이벤트를 수동으로 등록하기

보통 이벤트는 `EventServiceProvider`의 `$listen` 배열을 통해 등록하지만, 이벤트 리스너 클래스 또는 클로저(익명 함수)를 수동으로 `EventServiceProvider`의 `boot` 메서드에서 등록할 수도 있습니다:

```php
use App\Events\PodcastProcessed;
use App\Listeners\SendPodcastNotification;
use Illuminate\Support\Facades\Event;

/**
 * 애플리케이션의 다른 이벤트들을 등록합니다.
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
#### 큐 처리 가능한 익명 이벤트 리스너

클로저 기반 리스너를 수동 등록할 때, `Illuminate\Events\queueable` 함수를 사용하여 해당 리스너를 [큐](/docs/9.x/queues)를 통해 실행하도록 Laravel에 지시할 수 있습니다:

```php
use App\Events\PodcastProcessed;
use function Illuminate\Events\queueable;
use Illuminate\Support\Facades\Event;

/**
 * 애플리케이션의 다른 이벤트들을 등록합니다.
 *
 * @return void
 */
public function boot()
{
    Event::listen(queueable(function (PodcastProcessed $event) {
        //
    }));
}
```

큐 작업처럼, `onConnection`, `onQueue`, `delay` 메서드를 사용해 큐 처리 방식과 지연 시간을 설정할 수 있습니다:

```php
Event::listen(queueable(function (PodcastProcessed $event) {
    //
})->onConnection('redis')->onQueue('podcasts')->delay(now()->addSeconds(10)));
```

익명 큐 리스너 실패를 처리하려면 `queueable` 리스너 정의 시 `catch` 메서드에 클로저를 전달할 수 있습니다. 이 클로저는 이벤트 인스턴스와 실패 원인인 `Throwable` 인스턴스를 받습니다:

```php
use App\Events\PodcastProcessed;
use function Illuminate\Events\queueable;
use Illuminate\Support\Facades\Event;
use Throwable;

Event::listen(queueable(function (PodcastProcessed $event) {
    //
})->catch(function (PodcastProcessed $event, Throwable $e) {
    // 큐 리스너가 실패했을 때 처리할 로직...
}));
```

<a name="wildcard-event-listeners"></a>
#### 와일드카드 이벤트 리스너

`*` 와일드카드를 사용해 여러 이벤트를 한 리스너에서 처리하도록 등록할 수도 있습니다. 와일드카드 리스너는 첫 번째 인수로 이벤트 이름을, 두 번째 인수로 전체 이벤트 데이터 배열을 받습니다:

```php
Event::listen('event.*', function ($eventName, array $data) {
    //
});
```

<a name="event-discovery"></a>
### 이벤트 자동 발견(Event Discovery)

`EventServiceProvider`의 `$listen` 배열에 이벤트와 리스너를 직접 등록하는 대신, 이벤트 자동 발견 기능을 활성화할 수 있습니다. 자동 발견이 활성화되면, Laravel은 애플리케이션 `Listeners` 디렉토리를 스캔하여 이벤트와 리스너를 자동 등록합니다. 물론, 명시적으로 `$listen` 배열에 등록된 이벤트도 함께 등록됩니다.

Laravel은 PHP 리플렉션 기능을 사용해 리스너 클래스를 스캔하며, `handle` 또는 `__invoke` 메서드로 시작하는 메서드를 찾아 해당 메서드의 타입힌트 된 이벤트 클래스에 맞는 이벤트 리스너로 등록합니다:

```php
use App\Events\PodcastProcessed;

class SendPodcastNotification
{
    /**
     * 이벤트 처리 메서드.
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

자동 발견 기능은 기본적으로 비활성화되어 있지만, 애플리케이션 `EventServiceProvider`에서 `shouldDiscoverEvents` 메서드를 재정의하여 활성화할 수 있습니다:

```php
/**
 * 이벤트와 리스너를 자동으로 발견할지 여부를 결정합니다.
 *
 * @return bool
 */
public function shouldDiscoverEvents()
{
    return true;
}
```

기본적으로 `app/Listeners` 디렉토리 내 모든 리스너가 스캔됩니다. 추가로 탐색할 디렉토리를 정의하려면 `discoverEventsWithin` 메서드를 재정의하세요:

```php
/**
 * 이벤트 탐색 시 스캔할 리스너 디렉토리를 반환합니다.
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
#### 프로덕션 환경에서의 이벤트 자동 발견

프로덕션 환경에서는 매 요청마다 모든 리스너를 스캔하는 것이 비효율적입니다. 따라서 배포 과정 중에 `event:cache` Artisan 명령어를 실행하여 애플리케이션 이벤트 및 리스너 목록을 캐시하는 매니페스트를 생성하는 것이 좋습니다. 이 매니페스트를 통해 프레임워크는 이벤트 등록 속도를 높입니다. 캐시를 삭제하려면 `event:clear` 명령어를 사용하세요.

<a name="defining-events"></a>
## 이벤트 정의하기

이벤트 클래스는 기본적으로 이벤트와 관련된 정보를 담는 데이터 컨테이너 역할을 합니다. 예를 들어, `App\Events\OrderShipped` 이벤트가 [Eloquent ORM](/docs/9.x/eloquent) 모델 인스턴스를 받는 경우를 살펴봅시다:

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
     * 주문 인스턴스.
     *
     * @var \App\Models\Order
     */
    public $order;

    /**
     * 새 이벤트 인스턴스를 생성합니다.
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

보시다시피, 이 이벤트 클래스에는 별다른 로직이 없으며, 구매된 `App\Models\Order` 인스턴스를 담는 컨테이너 역할만 합니다. 이벤트에서 사용하는 `SerializesModels` 트레이트는 PHP의 `serialize` 함수로 이벤트 객체가 직렬화 될 때 Eloquent 모델을 유연하게 직렬화할 수 있게 해줍니다. 이는 [대기열 처리 이벤트 리스너](#queued-event-listeners)를 사용할 때 유용합니다.

<a name="defining-listeners"></a>
## 리스너 정의하기

다음은 위 예제 이벤트의 리스너 예시입니다. 이벤트 리스너는 `handle` 메서드에서 이벤트 인스턴스를 받습니다. `event:generate`나 `make:listener` Artisan 명령어로 생성하면 이벤트 클래스가 자동으로 임포트되고, `handle` 메서드에 이벤트가 타입힌트 됩니다. `handle` 메서드 내에서 이벤트에 대응하는 작업을 수행하세요:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;

class SendShipmentNotification
{
    /**
     * 이벤트 리스너를 생성합니다.
     *
     * @return void
     */
    public function __construct()
    {
        //
    }

    /**
     * 이벤트를 처리합니다.
     *
     * @param  \App\Events\OrderShipped  $event
     * @return void
     */
    public function handle(OrderShipped $event)
    {
        // $event->order를 통해 주문에 접근할 수 있습니다...
    }
}
```

> [!NOTE]
> 이벤트 리스너는 생성자에서 필요한 의존성을 타입힌트 할 수도 있습니다. Laravel의 [서비스 컨테이너](/docs/9.x/container)를 통해 모든 이벤트 리스너가 자동으로 의존성 주입되므로 편리합니다.

<a name="stopping-the-propagation-of-an-event"></a>
#### 이벤트 전파 중단하기

때로는 이벤트 전파를 다른 리스너로 중단하고 싶을 수 있습니다. 이때는 리스너의 `handle` 메서드에서 `false`를 반환하면 됩니다.

<a name="queued-event-listeners"></a>
## 대기열(큐) 처리 이벤트 리스너

리스너가 이메일 전송이나 HTTP 요청 등 느린 작업을 수행한다면, 큐를 사용해 비동기 처리하는 것이 좋습니다. 큐 처리 전에 [큐 설정](/docs/9.x/queues)을 완료하고, 서버 또는 개발 환경에서 큐 워커를 실행 중인지 확인하세요.

리스너를 큐 처리하도록 하려면, 리스너 클래스에 `ShouldQueue` 인터페이스를 추가하세요. `event:generate`와 `make:listener` 명령어로 생성된 리스너는 이미 이 인터페이스를 임포트하므로 바로 사용할 수 있습니다:

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

이제 이 리스너가 처리하는 이벤트가 발생하면, 이벤트 디스패처가 자동으로 Laravel [큐 시스템](/docs/9.x/queues)을 통해 리스너를 큐에 넣고 처리합니다. 큐 작업이 정상 처리되면 작업은 자동으로 삭제됩니다.

<a name="customizing-the-queue-connection-queue-name"></a>
#### 큐 연결 및 큐 이름 지정

리스너의 큐 연결, 큐 이름, 지연 시간(delay)을 변경하려면 리스너 클래스에 `$connection`, `$queue`, `$delay` 속성을 정의하세요:

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
     * 작업 처리를 시작하기 전 지연 시간(초).
     *
     * @var int
     */
    public $delay = 60;
}
```

실행 시점에 큐 연결이나 큐 이름을 유동적으로 지정하려면, 리스너에 `viaConnection` 및 `viaQueue` 메서드를 정의할 수 있습니다:

```php
/**
 * 리스너의 큐 연결 이름을 반환합니다.
 *
 * @return string
 */
public function viaConnection()
{
    return 'sqs';
}

/**
 * 리스너의 큐 이름을 반환합니다.
 *
 * @return string
 */
public function viaQueue()
{
    return 'listeners';
}
```

<a name="conditionally-queueing-listeners"></a>
#### 조건부로 큐 처리하기

리스너를 큐에 넣을지 여부를 런타임에 결정해야 하는 경우, `shouldQueue` 메서드를 리스너에 추가하세요. 이 메서드가 `false`를 반환하면 큐 처리가 되지 않습니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderCreated;
use Illuminate\Contracts\Queue\ShouldQueue;

class RewardGiftCard implements ShouldQueue
{
    /**
     * 선물 카드를 고객에게 보상합니다.
     *
     * @param  \App\Events\OrderCreated  $event
     * @return void
     */
    public function handle(OrderCreated $event)
    {
        //
    }

    /**
     * 이 리스너가 큐에 들어가야 하는지 결정합니다.
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
### 대기열과 수동으로 상호작용하기

리스너의 내부 큐 작업에 대해 `delete`와 `release` 메서드를 직접 호출해야 할 경우, `Illuminate\Queue\InteractsWithQueue` 트레이트를 사용할 수 있습니다. 이 트레이트는 기본적으로 생성된 리스너에 포함되며, 해당 메서드들을 제공합니다:

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
### 대기열 처리 이벤트 리스너와 데이터베이스 트랜잭션

데이터베이스 트랜잭션 안에서 큐 처리 리스너를 디스패치하는 경우, 큐 작업이 트랜잭션 커밋 전에 실행될 수 있어 문제가 발생할 수 있습니다. 트랜잭션 내에서 모델이나 데이터베이스 기록이 아직 커밋되지 않아 실제 데이터베이스에 반영되지 않은 시점에 큐 작업이 실행되는 상황입니다. 이로 인해 의존하는 모델이 없거나 예상치 못한 오류가 발생할 수 있습니다.

큐 연결의 `after_commit` 설정이 `false`인 경우에도, 특정 큐 리스너가 모든 열린 트랜잭션이 커밋된 후에야 실행되도록 하려면 리스너 클래스에 `$afterCommit` 속성을 `true`로 정의하세요:

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

> [!NOTE]
> 이 문제를 다루는 방법에 대해 더 알고 싶다면, [대기열 작업과 데이터베이스 트랜잭션 관련 문서](/docs/9.x/queues#jobs-and-database-transactions)를 참고하세요.

<a name="handling-failed-jobs"></a>
### 실패한 작업 처리하기

때때로, 큐에 있는 이벤트 리스너가 실패할 수 있습니다. 큐 작업이 워커에 정의된 최대 재시도 횟수를 넘겼을 때, 리스너의 `failed` 메서드가 호출됩니다. 이 메서드는 이벤트 인스턴스와 실패 원인인 `Throwable` 인스턴스를 받습니다:

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
     *
     * @param  \App\Events\OrderShipped  $event
     * @return void
     */
    public function handle(OrderShipped $event)
    {
        //
    }

    /**
     * 큐 작업이 실패했을 때 처리합니다.
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
#### 큐 리스너 최대 재시도 횟수 지정하기

큐 리스너가 오류를 자주 만난다면 무한 반복 재시도를 막는 것이 좋습니다. Laravel은 리스너가 재시도할 최대 횟수나 최대 재시도 기간을 지정하는 여러 방법을 제공합니다.

리스너 클래스에 `$tries` 속성을 정의하면, 이 값만큼 재시도 후 실패 처리됩니다:

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
     * 큐 리스너가 시도할 최대 횟수입니다.
     *
     * @var int
     */
    public $tries = 5;
}
```

횟수 대신 특정 시간까지 재시도하게 만들고 싶으면, `retryUntil` 메서드를 추가해 `DateTime` 인스턴스를 반환하도록 하세요. 이 시간 전까지는 횟수 제한 없이 재시도합니다:

```php
/**
 * 리스너가 타임아웃되는 시간을 결정합니다.
 *
 * @return \DateTime
 */
public function retryUntil()
{
    return now()->addMinutes(5);
}
```

<a name="dispatching-events"></a>
## 이벤트 발생시키기

이벤트를 발생시키려면, 이벤트 클래스의 정적 `dispatch` 메서드를 호출하면 됩니다. 이 메서드는 `Illuminate\Foundation\Events\Dispatchable` 트레이트에서 제공되며, `dispatch`에 넘기는 모든 인수는 이벤트 생성자의 인자로 전달됩니다:

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
     * 주어진 주문을 배송 처리합니다.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        $order = Order::findOrFail($request->order_id);

        // 주문 배송 관련 로직...

        OrderShipped::dispatch($order);
    }
}
```

조건에 따라 이벤트를 발송하려면, `dispatchIf`와 `dispatchUnless` 메서드를 사용할 수 있습니다:

```php
OrderShipped::dispatchIf($condition, $order);

OrderShipped::dispatchUnless($condition, $order);
```

> [!NOTE]
> 테스트 시 실제 리스너를 실행하지 않고 특정 이벤트가 발생했는지만 확인하고 싶다면, Laravel 내장 테스트 도구 [이벤트 가짜(Event Fake)](/docs/9.x/mocking#event-fake)를 활용하세요.

<a name="event-subscribers"></a>
## 이벤트 구독자(Event Subscribers)

<a name="writing-event-subscribers"></a>
### 이벤트 구독자 작성하기

이벤트 구독자는 한 클래스 내에서 여러 이벤트에 구독할 수 있도록 해 주어, 한 클래스에 복수 이벤트 핸들러를 정의할 수 있게 합니다. 구독자는 `subscribe` 메서드를 정의하며, 이 메서드는 이벤트 디스패처 인스턴스를 인수로 받습니다. 디스패처의 `listen` 메서드를 호출해 이벤트 리스너를 등록하세요:

```php
<?php

namespace App\Listeners;

use Illuminate\Auth\Events\Login;
use Illuminate\Auth\Events\Logout;

class UserEventSubscriber
{
    /**
     * 사용자 로그인 이벤트 처리.
     */
    public function handleUserLogin($event) {}

    /**
     * 사용자 로그아웃 이벤트 처리.
     */
    public function handleUserLogout($event) {}

    /**
     * 구독자의 리스너를 등록합니다.
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

리스너 메서드가 구독자 내부에 정의되어 있다면, `subscribe` 메서드에서 이벤트 클래스와 메서드명을 배열로 반환할 수도 있습니다. Laravel은 자동으로 클래스 이름을 감지해 등록합니다:

```php
<?php

namespace App\Listeners;

use Illuminate\Auth\Events\Login;
use Illuminate\Auth\Events\Logout;

class UserEventSubscriber
{
    /**
     * 사용자 로그인 이벤트 처리.
     */
    public function handleUserLogin($event) {}

    /**
     * 사용자 로그아웃 이벤트 처리.
     */
    public function handleUserLogout($event) {}

    /**
     * 구독자의 리스너를 등록합니다.
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
### 이벤트 구독자 등록하기

구독자 클래스를 작성한 후에는 이벤트 디스패처에 등록해야 합니다. 이를 위해 `EventServiceProvider`에서 `$subscribe` 속성에 구독자 클래스를 추가하세요. 예를 들어 `UserEventSubscriber`를 등록하는 방법은 다음과 같습니다:

```php
<?php

namespace App\Providers;

use App\Listeners\UserEventSubscriber;
use Illuminate\Foundation\Support\Providers\EventServiceProvider as ServiceProvider;

class EventServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 이벤트 리스너 매핑.
     *
     * @var array
     */
    protected $listen = [
        //
    ];

    /**
     * 등록할 구독자 클래스 목록.
     *
     * @var array
     */
    protected $subscribe = [
        UserEventSubscriber::class,
    ];
}
```