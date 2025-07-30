# 이벤트 (Events)

- [소개](#introduction)
- [이벤트 및 리스너 등록](#registering-events-and-listeners)
    - [이벤트 및 리스너 생성](#generating-events-and-listeners)
    - [이벤트 수동 등록](#manually-registering-events)
    - [이벤트 발견](#event-discovery)
- [이벤트 정의](#defining-events)
- [리스너 정의](#defining-listeners)
- [큐잉된 이벤트 리스너](#queued-event-listeners)
    - [큐와 수동 상호작용](#manually-interacting-with-the-queue)
    - [큐잉된 이벤트 리스너와 데이터베이스 트랜잭션](#queued-event-listeners-and-database-transactions)
    - [실패한 작업 처리](#handling-failed-jobs)
- [이벤트 발생시키기](#dispatching-events)
- [이벤트 구독자](#event-subscribers)
    - [이벤트 구독자 작성](#writing-event-subscribers)
    - [이벤트 구독자 등록](#registering-event-subscribers)

<a name="introduction"></a>
## 소개

Laravel의 이벤트는 간단한 옵저버 패턴(observer pattern)을 구현해 애플리케이션 내에서 발생하는 다양한 이벤트에 구독하고 청취할 수 있게 합니다. 이벤트 클래스는 보통 `app/Events` 디렉터리에 저장되며, 그에 대응하는 리스너는 `app/Listeners`에 위치합니다. 애플리케이션에서 이 디렉터리가 보이지 않아도 Artisan 콘솔 명령어를 통해 이벤트와 리스너를 생성하면 자동으로 만들어집니다.

이벤트는 애플리케이션의 여러 부분을 느슨하게 결합하는 좋은 방법입니다. 하나의 이벤트에 여러 리스너가 존재할 수 있으며, 이들은 서로 독립적으로 작동합니다. 예를 들어, 주문이 배송될 때마다 사용자에게 Slack 알림을 보내고 싶다면, 주문 처리 코드에 Slack 알림 코드를 직접 연결하는 대신, `App\Events\OrderShipped` 이벤트를 발생시키고 리스너에서 해당 이벤트를 받아 Slack 알림을 전송할 수 있습니다.

<a name="registering-events-and-listeners"></a>
## 이벤트 및 리스너 등록

Laravel 애플리케이션에 포함된 `App\Providers\EventServiceProvider`는 애플리케이션의 모든 이벤트 리스너를 등록하는 편리한 공간을 제공합니다. `listen` 속성은 모든 이벤트(키)와 그에 대응하는 리스너(값)의 배열을 포함합니다. 필요에 따라 이벤트를 이 배열에 얼마든지 추가할 수 있습니다. 예를 들어 `OrderShipped` 이벤트를 추가하려면 다음과 같습니다:

```
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

> [!TIP]
> `event:list` 명령어를 이용하면 애플리케이션에 등록된 모든 이벤트와 리스너 목록을 쉽게 출력할 수 있습니다.

<a name="generating-events-and-listeners"></a>
### 이벤트 및 리스너 생성

각 이벤트와 리스너 파일을 수동으로 만드는 것은 번거롭습니다. 그 대신 `EventServiceProvider`에 이벤트와 리스너를 추가한 후 `event:generate` Artisan 명령어를 사용할 수 있습니다. 이 명령어는 `EventServiceProvider`에 등록된 이벤트와 리스너 중 아직 존재하지 않는 파일을 자동 생성합니다:

```
php artisan event:generate
```

또한 개별 이벤트와 리스너를 생성하려면 `make:event`와 `make:listener` Artisan 명령어를 사용할 수 있습니다:

```
php artisan make:event PodcastProcessed

php artisan make:listener SendPodcastNotification --event=PodcastProcessed
```

<a name="manually-registering-events"></a>
### 이벤트 수동 등록

이벤트는 보통 `EventServiceProvider`의 `$listen` 배열을 통해 등록하지만, `EventServiceProvider`의 `boot` 메서드에서 클래스 기반 또는 클로저 기반 이벤트 리스너를 수동으로 등록할 수도 있습니다:

```
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

클로저 기반 이벤트 리스너를 수동 등록할 때, `Illuminate\Events\queueable` 함수를 사용해 클로저를 래핑하면 Laravel이 해당 리스너를 큐(queue)를 사용해 비동기로 실행하도록 할 수 있습니다:

```
use App\Events\PodcastProcessed;
use function Illuminate\Events\queueable;
use Illuminate\Support\Facades\Event;

/**
 * Register any other events for your application.
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

큐잉된 작업과 마찬가지로, `onConnection`, `onQueue`, `delay` 메서드를 사용해 큐 연결, 큐 이름, 지연 시간을 조정할 수 있습니다:

```
Event::listen(queueable(function (PodcastProcessed $event) {
    //
})->onConnection('redis')->onQueue('podcasts')->delay(now()->addSeconds(10)));
```

익명 큐잉 리스너 실패를 처리하려면, `queueable` 리스너 정의 시 `catch` 메서드에 클로저를 제공하면 됩니다. 이 클로저는 이벤트 인스턴스와 실패를 일으킨 `Throwable` 인스턴스를 받습니다:

```
use App\Events\PodcastProcessed;
use function Illuminate\Events\queueable;
use Illuminate\Support\Facades\Event;
use Throwable;

Event::listen(queueable(function (PodcastProcessed $event) {
    //
})->catch(function (PodcastProcessed $event, Throwable $e) {
    // 큐잉 리스너 실패 처리...
}));
```

<a name="wildcard-event-listeners"></a>
#### 와일드카드 이벤트 리스너

`*` 와일드카드 문자를 사용해 여러 이벤트에 한 리스너를 등록할 수도 있습니다. 와일드카드 리스너는 첫 번째 인자로 이벤트 이름, 두 번째 인자로 전체 이벤트 데이터 배열을 받습니다:

```
Event::listen('event.*', function ($eventName, array $data) {
    //
});
```

<a name="event-discovery"></a>
### 이벤트 발견

`EventServiceProvider`의 `$listen` 배열에 직접 이벤트와 리스너를 등록하는 대신, 이벤트 발견(discovery)을 활성화할 수 있습니다. 활성화하면 Laravel이 애플리케이션의 `Listeners` 폴더를 스캔해 자동으로 이벤트와 리스너를 찾아 등록합니다. 물론 `EventServiceProvider`에 명시적으로 등록된 이벤트도 계속 등록됩니다.

Laravel은 PHP Reflection 서비스를 사용해 리스너 클래스를 조사합니다. 리스너 클래스 메서드 중 `handle`로 시작하는 메서드가 있으면, 해당 메서드의 시그니처에 타입힌트된 이벤트 클래스를 기준으로 이벤트 리스너로 등록합니다:

```
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

이벤트 발견은 기본적으로 비활성화되어 있으며 `EventServiceProvider`에서 `shouldDiscoverEvents` 메서드를 오버라이드하여 활성화할 수 있습니다:

```
/**
 * 이벤트 및 리스너 자동 발견 활성화 여부 결정.
 *
 * @return bool
 */
public function shouldDiscoverEvents()
{
    return true;
}
```

기본적으로 애플리케이션의 `app/Listeners` 폴더 내 모든 리스너가 스캔됩니다. 추가로 스캔할 디렉터리를 지정하려면 `discoverEventsWithin` 메서드를 오버라이드하세요:

```
/**
 * 이벤트 발견에 사용할 리스너 디렉터리 반환.
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
#### 프로덕션 환경에서 이벤트 발견

프로덕션에서는 모든 요청마다 리스너 전체를 스캔하는 것이 비효율적입니다. 따라서 배포 시 `event:cache` Artisan 명령어를 실행해 모든 이벤트 및 리스너의 매니페스트를 캐싱하는 것이 좋습니다. 캐시는 이벤트 등록 과정을 가속합니다. 캐시를 삭제하려면 `event:clear` 명령어를 사용하세요.

<a name="defining-events"></a>
## 이벤트 정의

이벤트 클래스는 기본적으로 이벤트와 관련된 데이터를 담는 컨테이너입니다. 예를 들어 `App\Events\OrderShipped` 이벤트가 [Eloquent ORM](/docs/{{version}}/eloquent) 모델을 받는다고 가정할 수 있습니다:

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
     * 주문 인스턴스.
     *
     * @var \App\Models\Order
     */
    public $order;

    /**
     * 새로운 이벤트 인스턴스 생성.
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

보시다시피 이 이벤트 클래스에는 로직이 없습니다. 단지 구매된 `App\Models\Order` 인스턴스를 담는 컨테이너 역할을 합니다. 이벤트에 사용된 `SerializesModels` 트레이트는 PHP의 `serialize` 함수를 사용해 이벤트 객체를 직렬화할 때, Eloquent 모델을 우아하게 직렬화해 줍니다. (예: [큐잉된 리스너](#queued-event-listeners) 사용 시)

<a name="defining-listeners"></a>
## 리스너 정의

이제 예시 이벤트에 대한 리스너를 살펴보겠습니다. 이벤트 리스너는 `handle` 메서드에서 이벤트 인스턴스를 받습니다. `event:generate`나 `make:listener` Artisan 명령어로 생성된 리스너는 자동으로 적절한 이벤트 클래스를 임포트하고 `handle` 메서드에 타입힌트를 붙여줍니다. `handle` 내부에서는 이벤트에 대응한 작업을 수행할 수 있습니다:

```
<?php

namespace App\Listeners;

use App\Events\OrderShipped;

class SendShipmentNotification
{
    /**
     * 이벤트 리스너 생성자.
     *
     * @return void
     */
    public function __construct()
    {
        //
    }

    /**
     * 이벤트 처리 메서드.
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

> [!TIP]
> 이벤트 리스너는 생성자에 필요한 의존성을 타입힌트하여 주입받을 수 있습니다. 모든 이벤트 리스너는 Laravel [서비스 컨테이너](/docs/{{version}}/container)를 통해 해결되므로, 의존성이 자동으로 주입됩니다.

<a name="stopping-the-propagation-of-an-event"></a>
#### 이벤트 전파 멈추기

가끔 이벤트가 다른 리스너에게 전파되는 것을 중지하고 싶을 때가 있습니다. 이 경우 리스너의 `handle` 메서드에서 `false`를 반환하면 이벤트 전파가 멈춥니다.

<a name="queued-event-listeners"></a>
## 큐잉된 이벤트 리스너

리스너가 이메일 발송이나 HTTP 요청처럼 느린 작업을 수행할 경우, 큐잉하여 비동기로 처리하는 것이 유용합니다. 큐잉 리스너를 사용하기 전에, [큐 설정](/docs/{{version}}/queues)을 완료하고 큐 워커를 서버나 개발 환경에서 실행하세요.

리스너를 큐잉하려면, 리스너 클래스에 `ShouldQueue` 인터페이스를 추가하면 됩니다. `event:generate`와 `make:listener` 명령어로 생성되는 리스너는 이미 이 인터페이스를 임포트해 바로 사용할 수 있습니다:

```
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    //
}
```

이제 해당 리스너가 처리하는 이벤트가 발생하면, 이벤트 디스패처는 자동으로 Laravel의 [큐 시스템](/docs/{{version}}/queues)을 이용해 이 리스너 작업을 큐에 보냅니다. 큐에서 리스너가 실행 중 예외가 발생하지 않으면, 작업 완료 후 자동으로 큐 작업이 삭제됩니다.

<a name="customizing-the-queue-connection-queue-name"></a>
#### 큐 연결 및 큐 이름 사용자 정의

큐 연결, 큐 이름, 지연 시간을 커스텀하려면 리스너 클래스에 `$connection`, `$queue`, `$delay` 속성을 선언하세요:

```
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    /**
     * 작업이 보내질 큐 연결 이름.
     *
     * @var string|null
     */
    public $connection = 'sqs';

    /**
     * 작업이 보내질 큐 이름.
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

실행 시점에 연결이나 큐 이름을 동적으로 지정하려면 `viaConnection`과 `viaQueue` 메서드를 정의할 수도 있습니다:

```
/**
 * 리스너의 큐 연결 이름 반환.
 *
 * @return string
 */
public function viaConnection()
{
    return 'sqs';
}

/**
 * 리스너의 큐 이름 반환.
 *
 * @return string
 */
public function viaQueue()
{
    return 'listeners';
}
```

<a name="conditionally-queueing-listeners"></a>
#### 조건부 큐잉 리스너

어떤 경우에는 런타임에 수집한 데이터 기반으로 리스너가 큐잉될지 결정해야 할 수 있습니다. 이를 위해 리스너 클래스에 `shouldQueue` 메서드를 추가해 큐잉 여부를 반환하게 할 수 있습니다. `shouldQueue`가 `false`를 반환하면 리스너는 실행되지 않습니다:

```
<?php

namespace App\Listeners;

use App\Events\OrderCreated;
use Illuminate\Contracts\Queue\ShouldQueue;

class RewardGiftCard implements ShouldQueue
{
    /**
     * 고객에게 선물 카드를 지급.
     *
     * @param  \App\Events\OrderCreated  $event
     * @return void
     */
    public function handle(OrderCreated $event)
    {
        //
    }

    /**
     * 리스너를 큐잉할지 결정.
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
### 큐와 수동 상호작용

리스너 내부에서 큐 작업의 `delete`나 `release` 메서드에 직접 접근해야 한다면, `Illuminate\Queue\InteractsWithQueue` 트레이트를 사용할 수 있습니다. 이 트레이트는 자동 생성된 리스너에 기본 임포트되어 있으며, 다음과 같이 사용합니다:

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
### 큐잉된 이벤트 리스너와 데이터베이스 트랜잭션

데이터베이스 트랜잭션 안에서 큐잉된 리스너를 디스패치하면, 트랜잭션 커밋 전에 큐가 작업을 실행할 수 있습니다. 이 경우 트랜잭션 내에서 수정한 모델이나 데이터베이스 레코드가 아직 반영되지 않았거나 새로 생성된 모델이나 레코드가 존재하지 않을 수 있습니다. 이 때문에 해당 모델들에 의존하는 리스너에게는 예기치 않은 오류가 발생할 수 있습니다.

큐 연결의 `after_commit` 설정이 `false`로 되어 있어도, 특정 큐잉 리스너가 모든 열린 데이터베이스 트랜잭션이 커밋된 후에 실행되게 하려면, 리스너 클래스에 `$afterCommit` 속성을 다음과 같이 선언하세요:

```
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

> [!TIP]
> 이러한 문제 해결 방법에 대한 자세한 내용은 [큐잉 작업과 데이터베이스 트랜잭션](/docs/{{version}}/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="handling-failed-jobs"></a>
### 실패한 작업 처리

큐잉된 이벤트 리스너가 실패할 수도 있습니다. 큐 워커가 최대 시도 횟수를 초과하면, 리스너의 `failed` 메서드가 호출됩니다. 이 메서드는 이벤트 인스턴스와 실패를 발생시킨 `Throwable` 객체를 인자로 받습니다:

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
     *
     * @param  \App\Events\OrderShipped  $event
     * @return void
     */
    public function handle(OrderShipped $event)
    {
        //
    }

    /**
     * 실패한 작업 처리.
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
#### 큐잉 리스너 최대 시도 횟수 지정

큐잉 리스너가 에러가 발생해 무한 재시도하는 것을 방지하려면, 최대 시도 횟수나 시간 제한을 지정할 수 있습니다.

리스너 클래스에 `$tries` 속성을 정의해 최대 시도 횟수를 설정할 수 있습니다:

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
     * 큐잉 리스너 최대 시도 횟수.
     *
     * @var int
     */
    public $tries = 5;
}
```

횟수 대신 특정 시간까지 시도하도록 제한하려면, `retryUntil` 메서드를 정의해 `DateTime` 객체를 반환하세요. 해당 시간 이후에는 더 이상 시도하지 않습니다:

```
/**
 * 리스너 실행 제한 시간 반환.
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

이벤트를 발생시키려면, 이벤트 클래스에 포함된 `Illuminate\Foundation\Events\Dispatchable` 트레이트가 제공하는 정적 `dispatch` 메서드를 호출합니다. 메서드 인자로 넘긴 값들은 이벤트 클래스 생성자에 전달됩니다:

```
<?php

namespace App\Http\Controllers;

use App\Events\OrderShipped;
use App\Http\Controllers\Controller;
use App\Models\Order;
use Illuminate\Http\Request;

class OrderShipmentController extends Controller
{
    /**
     * 주문 배송 처리.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        $order = Order::findOrFail($request->order_id);

        // 주문 배송 로직...

        OrderShipped::dispatch($order);
    }
}
```

> [!TIP]
> 테스트할 때 실제 리스너를 호출하지 않고 이벤트가 발생했는지 검증할 수 있습니다. Laravel 내장 테스트 헬퍼 [event fake](/docs/{{version}}/mocking#event-fake)를 활용하면 편리합니다.

<a name="event-subscribers"></a>
## 이벤트 구독자

<a name="writing-event-subscribers"></a>
### 이벤트 구독자 작성

이벤트 구독자 클래스는 여러 이벤트를 구독 가능하며, 하나의 클래스 내에 여러 이벤트 핸들러를 정의할 수 있어 편리합니다. 구독자는 `subscribe` 메서드를 정의해야 하며, 이 메서드는 이벤트 디스패처 인스턴스를 인자로 받습니다. 디스패처의 `listen` 메서드를 호출해 이벤트 리스너를 등록할 수 있습니다:

```
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

리스너 메서드가 구독자 클래스 내에 정의되어 있다면, `subscribe` 메서드에서 이벤트와 메서드 이름 매핑 배열을 반환하는 방법도 있습니다. 이렇게 하면 리스너 등록 시 Laravel이 구독자 클래스 이름을 자동으로 알아냅니다:

```
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

구독자 클래스를 작성했다면, 이벤트 디스패처에 등록할 준비가 된 것입니다. `EventServiceProvider`의 `$subscribe` 속성에 구독자 클래스를 추가해 등록할 수 있습니다. 예를 들어 `UserEventSubscriber`를 등록할 때:

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
        //
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