# 이벤트

- [소개](#introduction)
- [이벤트 및 리스너 등록](#registering-events-and-listeners)
    - [이벤트 및 리스너 생성](#generating-events-and-listeners)
    - [이벤트 수동 등록](#manually-registering-events)
    - [이벤트 디스커버리](#event-discovery)
- [이벤트 정의](#defining-events)
- [리스너 정의](#defining-listeners)
- [큐잉된 이벤트 리스너](#queued-event-listeners)
    - [큐와 수동으로 상호작용하기](#manually-interacting-with-the-queue)
    - [큐 리스너와 데이터베이스 트랜잭션](#queued-event-listeners-and-database-transactions)
    - [실패한 작업 처리](#handling-failed-jobs)
- [이벤트 디스패치](#dispatching-events)
- [이벤트 구독자](#event-subscribers)
    - [이벤트 구독자 작성](#writing-event-subscribers)
    - [이벤트 구독자 등록](#registering-event-subscribers)

<a name="introduction"></a>
## 소개

Laravel의 이벤트는 간단한 옵서버 패턴 구현을 제공하여 애플리케이션 내에서 발생하는 다양한 이벤트를 구독 및 청취할 수 있게 합니다. 이벤트 클래스는 일반적으로 `app/Events` 디렉터리에 저장되며, 해당 리스너들은 `app/Listeners`에 저장됩니다. 만약 애플리케이션에 이 디렉터리가 없다면, Artisan 콘솔 명령어를 사용하여 이벤트와 리스너를 생성할 때 자동으로 생성됩니다.

이벤트는 애플리케이션의 다양한 부분을 분리하는 훌륭한 방법입니다. 하나의 이벤트에 여러 리스너를 연결할 수 있는데, 이들은 서로에게 의존하지 않습니다. 예를 들어, 주문이 배송될 때마다 사용자가 Slack 알림을 받도록 하고 싶다면, 주문 처리 코드와 Slack 알림 코드를 직접 연결하지 않고, `App\Events\OrderShipped` 이벤트를 발생시키고, 리스너에서 Slack 알림을 전송하도록 할 수 있습니다.

<a name="registering-events-and-listeners"></a>
## 이벤트 및 리스너 등록

Laravel 애플리케이션에 포함된 `App\Providers\EventServiceProvider`는 모든 이벤트 리스너를 등록할 수 있는 편리한 위치를 제공합니다. `listen` 속성에는 모든 이벤트(키)와 해당 리스너(값)의 배열이 들어갑니다. 애플리케이션에서 필요한 만큼 이벤트를 추가할 수 있습니다. 예를 들어 `OrderShipped` 이벤트를 추가해보겠습니다:

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

> **참고**
> `event:list` 명령어를 사용하여 애플리케이션에 등록된 모든 이벤트와 리스너 목록을 확인할 수 있습니다.

<a name="generating-events-and-listeners"></a>
### 이벤트 및 리스너 생성

각 이벤트와 리스너 파일을 직접 만드는 것은 번거롭기 때문에, `EventServiceProvider`에 리스너 및 이벤트를 추가한 뒤 `event:generate` Artisan 명령어를 사용할 수 있습니다. 이 명령어는 `EventServiceProvider`에 정의된, 아직 존재하지 않는 이벤트 또는 리스너의 파일을 생성해줍니다:

```shell
php artisan event:generate
```

또는 `make:event` 및 `make:listener` Artisan 명령어를 사용하여 각각 개별적으로 이벤트나 리스너를 생성할 수 있습니다:

```shell
php artisan make:event PodcastProcessed

php artisan make:listener SendPodcastNotification --event=PodcastProcessed
```

<a name="manually-registering-events"></a>
### 이벤트 수동 등록

일반적으로 이벤트는 `EventServiceProvider`의 `$listen` 배열을 통해 등록해야 하지만, 클래스 또는 클로저 기반의 이벤트 리스너를 `EventServiceProvider`의 `boot` 메서드에서 수동으로 등록할 수도 있습니다:

    use App\Events\PodcastProcessed;
    use App\Listeners\SendPodcastNotification;
    use Illuminate\Support\Facades\Event;

    /**
     * 애플리케이션의 기타 이벤트를 등록합니다.
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

<a name="queuable-anonymous-event-listeners"></a>
#### 큐잉 가능한 익명 이벤트 리스너

클로저 기반 이벤트 리스너를 수동 등록할 때, 해당 리스너 클로저를 `Illuminate\Events\queueable` 함수로 감싸면 Laravel이 [큐](/docs/{{version}}/queues)를 사용해 리스너를 실행하도록 지정할 수 있습니다:

    use App\Events\PodcastProcessed;
    use function Illuminate\Events\queueable;
    use Illuminate\Support\Facades\Event;

    /**
     * 애플리케이션의 기타 이벤트를 등록합니다.
     *
     * @return void
     */
    public function boot()
    {
        Event::listen(queueable(function (PodcastProcessed $event) {
            //
        }));
    }

큐에 등록되는 작업처럼 `onConnection`, `onQueue`, `delay` 메서드를 사용하여 큐 리스너의 실행 방법을 커스터마이즈할 수 있습니다:

    Event::listen(queueable(function (PodcastProcessed $event) {
        //
    })->onConnection('redis')->onQueue('podcasts')->delay(now()->addSeconds(10)));

익명 큐 리스너가 실패했을 때 처리를 원한다면, `queueable` 리스너 정의 시 `catch` 메서드에 클로저를 제공할 수 있습니다. 이 클로저는 이벤트 인스턴스와 실패의 원인이 된 `Throwable` 인스턴스를 전달받습니다:

    use App\Events\PodcastProcessed;
    use function Illuminate\Events\queueable;
    use Illuminate\Support\Facades\Event;
    use Throwable;

    Event::listen(queueable(function (PodcastProcessed $event) {
        //
    })->catch(function (PodcastProcessed $event, Throwable $e) {
        // 큐 리스너가 실패했을 때...
    }));

<a name="wildcard-event-listeners"></a>
#### 와일드카드 이벤트 리스너

리스너를 `*` 와일드카드 파라미터로 등록하여 동일한 리스너에서 여러 이벤트를 수신할 수 있습니다. 와일드카드 리스너는 첫 번째 인자에 이벤트 이름, 두 번째 인자에 전체 이벤트 데이터 배열을 전달받습니다:

    Event::listen('event.*', function ($eventName, array $data) {
        //
    });

<a name="event-discovery"></a>
### 이벤트 디스커버리

`EventServiceProvider`의 `$listen` 배열에 이벤트와 리스너를 수동으로 등록하는 대신, 자동 이벤트 디스커버리를 사용할 수 있습니다. 이벤트 디스커버리가 활성화되면, Laravel이 애플리케이션의 `Listeners` 디렉터리를 스캔하여 자동으로 이벤트와 리스너를 찾아서 등록합니다. 또한, `EventServiceProvider`에 명시적으로 정의된 이벤트들은 계속 등록됩니다.

Laravel은 PHP의 리플렉션을 사용해 리스너 클래스를 스캔합니다. 클래스 메서드가 `handle` 또는 `__invoke`로 시작되면, 해당 메서드에 명시된 타입힌트 이벤트에 대해 리스너로 자동 등록합니다:

    use App\Events\PodcastProcessed;

    class SendPodcastNotification
    {
        /**
         * 해당 이벤트를 처리합니다.
         *
         * @param  \App\Events\PodcastProcessed  $event
         * @return void
         */
        public function handle(PodcastProcessed $event)
        {
            //
        }
    }

이벤트 디스커버리는 기본적으로 비활성화되어 있지만, 애플리케이션의 `EventServiceProvider`에서 `shouldDiscoverEvents` 메서드를 오버라이딩하여 활성화할 수 있습니다:

    /**
     * 이벤트와 리스너 자동 디스커버리 여부 반환.
     *
     * @return bool
     */
    public function shouldDiscoverEvents()
    {
        return true;
    }

기본적으로 애플리케이션의 `app/Listeners` 디렉터리가 스캔 대상입니다. 추가로 스캔할 디렉터리를 지정하고자 한다면, `EventServiceProvider`의 `discoverEventsWithin` 메서드를 오버라이딩하면 됩니다:

    /**
     * 이벤트를 찾을 리스너 디렉터리 반환.
     *
     * @return array
     */
    protected function discoverEventsWithin()
    {
        return [
            $this->app->path('Listeners'),
        ];
    }

<a name="event-discovery-in-production"></a>
#### 운영 환경에서 이벤트 디스커버리

운영 환경에서는 모든 요청마다 리스너 전체를 스캔하는 것은 비효율적입니다. 따라서 배포 시점에 `event:cache` Artisan 명령어로 애플리케이션의 모든 이벤트 및 리스너의 매니페스트를 캐시해두기 바랍니다. 이 매니페스트는 프레임워크가 이벤트 등록을 빠르게 할 수 있도록 사용됩니다. `event:clear` 명령어를 사용해 캐시를 삭제할 수도 있습니다.

<a name="defining-events"></a>
## 이벤트 정의

이벤트 클래스는 이벤트와 관련된 정보를 담는 단순한 데이터 컨테이너입니다. 예를 들어 `App\Events\OrderShipped` 이벤트가 [Eloquent ORM](/docs/{{version}}/eloquent) 객체를 받는다고 가정해봅시다:

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

이벤트 클래스에는 로직이 없습니다. 주문이 이루어진 `App\Models\Order` 인스턴스를 감싸는 컨테이너일 뿐입니다. 이벤트에서 사용하는 `SerializesModels` 트레이트는 이벤트 객체를 PHP의 `serialize` 기능으로 직렬화할 때(Eloquent 모델 포함) 자동으로 직렬화 과정을 처리해줍니다. 이는 [큐잉된 리스너](#queued-event-listeners) 사용 시 유용합니다.

<a name="defining-listeners"></a>
## 리스너 정의

이제 예제 이벤트에 대한 리스너를 살펴보겠습니다. 이벤트 리스너는 `handle` 메서드에서 이벤트 인스턴스를 전달받습니다. `event:generate` 및 `make:listener` Artisan 명령어를 사용하면 관련 이벤트 클래스를 자동으로 import하고, 타입힌트를 지정해줍니다. `handle` 메서드 내부에서 이벤트에 대한 처리를 자유롭게 할 수 있습니다:

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
         * 이벤트 처리.
         *
         * @param  \App\Events\OrderShipped  $event
         * @return void
         */
        public function handle(OrderShipped $event)
        {
            // $event->order를 사용해 주문 정보에 접근할 수 있습니다...
        }
    }

> **참고**  
> 이벤트 리스너의 생성자에서 필요한 의존성을 타입힌트 할 수도 있습니다. 모든 이벤트 리스너는 Laravel [서비스 컨테이너](/docs/{{version}}/container)를 통해 해석되므로, 의존성은 자동으로 주입됩니다.

<a name="stopping-the-propagation-of-an-event"></a>
#### 이벤트 전파 중단

때때로 이벤트가 다른 리스너로 전파되는 것을 중지하고 싶을 때가 있습니다. 리스너의 `handle` 메서드에서 `false`를 반환하면 이벤트 전파를 중단할 수 있습니다.

<a name="queued-event-listeners"></a>
## 큐잉된 이벤트 리스너

이메일 전송이나 HTTP 요청처럼 느린 작업을 수행해야 하는 경우, 리스너를 큐잉하는 것이 좋습니다. 큐잉된 리스너를 사용하기 전에 [큐 설정](/docs/{{version}}/queues)을 완료하고, 서버 또는 개발 환경에서 큐 워커를 실행해야 합니다.

리스너가 큐에 저장되도록 지정하려면 리스너 클래스에 `ShouldQueue` 인터페이스를 추가하세요. `event:generate` 및 `make:listener` 명령어로 생성한 리스너에는 이미 이 인터페이스가 import되어 있습니다:

    <?php

    namespace App\Listeners;

    use App\Events\OrderShipped;
    use Illuminate\Contracts\Queue\ShouldQueue;

    class SendShipmentNotification implements ShouldQueue
    {
        //
    }

이제 해당 이벤트가 디스패치될 때, 라라벨의 [큐 시스템](/docs/{{version}}/queues)을 사용하여 이 리스너가 자동으로 큐에 등록됩니다. 큐에서 리스너가 실행되고 예외가 발생하지 않으면, 큐 작업은 자동으로 삭제됩니다.

<a name="customizing-the-queue-connection-queue-name"></a>
#### 큐 연결 및 큐 이름 커스터마이징

큐 연결, 큐 이름, 지연(딜레이) 시간을 커스터마이징하려면 리스너 클래스에 `$connection`, `$queue`, `$delay` 속성을 정의하세요:

    <?php

    namespace App\Listeners;

    use App\Events\OrderShipped;
    use Illuminate\Contracts\Queue\ShouldQueue;

    class SendShipmentNotification implements ShouldQueue
    {
        /**
         * 이 작업이 전송될 연결 이름.
         *
         * @var string|null
         */
        public $connection = 'sqs';

        /**
         * 이 작업이 전송될 큐 이름.
         *
         * @var string|null
         */
        public $queue = 'listeners';

        /**
         * 작업 실행까지 대기 시간(초).
         *
         * @var int
         */
        public $delay = 60;
    }

실행 시점에 큐 연결이나 큐 이름을 지정하고자 한다면, `viaConnection` 또는 `viaQueue` 메서드를 리스너에 추가하세요:

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

<a name="conditionally-queueing-listeners"></a>
#### 조건부로 큐잉되는 리스너

실행 중에만 알 수 있는 데이터나 조건에 따라 리스너를 큐잉할지 판단해야 한다면, 리스너에 `shouldQueue` 메서드를 추가하면 됩니다. 이 메서드가 `false`를 반환하면 리스너는 실행되지 않습니다:

    <?php

    namespace App\Listeners;

    use App\Events\OrderCreated;
    use Illuminate\Contracts\Queue\ShouldQueue;

    class RewardGiftCard implements ShouldQueue
    {
        /**
         * 고객에게 기프트카드를 제공합니다.
         *
         * @param  \App\Events\OrderCreated  $event
         * @return void
         */
        public function handle(OrderCreated $event)
        {
            //
        }

        /**
         * 리스너가 큐잉되어야 하는지 판단.
         *
         * @param  \App\Events\OrderCreated  $event
         * @return bool
         */
        public function shouldQueue(OrderCreated $event)
        {
            return $event->order->subtotal >= 5000;
        }
    }

<a name="manually-interacting-with-the-queue"></a>
### 큐와 수동으로 상호작용하기

리스너의 큐 작업에서 `delete`, `release` 등의 메서드에 직접 접근이 필요하면, `Illuminate\Queue\InteractsWithQueue` 트레이트를 사용하면 됩니다. 이 트레이트는 생성된 리스너에 기본적으로 포함되어 있습니다:

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

<a name="queued-event-listeners-and-database-transactions"></a>
### 큐 리스너와 데이터베이스 트랜잭션

큐잉된 리스너가 데이터베이스 트랜잭션 내에서 디스패치되면, 트랜잭션 커밋 전에 큐에서 처리될 수 있습니다. 이 경우, 트랜잭션 내에서 변경된 모델이나 데이터베이스 레코드가 아직 데이터베이스에 반영되지 않았을 수 있으므로, 큐잉된 리스너가 이러한 모델에 의존한다면 오류가 발생할 수 있습니다.

큐 연결 설정의 `after_commit` 옵션이 `false`인 경우에도, 리스너 클래스에 `$afterCommit` 속성을 정의하여 모든 데이터베이스 트랜잭션이 커밋된 후에만 큐잉된 리스너가 실행되도록 지정할 수 있습니다:

    <?php

    namespace App\Listeners;

    use Illuminate\Contracts\Queue\ShouldQueue;
    use Illuminate\Queue\InteractsWithQueue;

    class SendShipmentNotification implements ShouldQueue
    {
        use InteractsWithQueue;

        public $afterCommit = true;
    }

> **참고**  
> 이러한 문제의 자세한 해결 방법은 [큐 작업과 데이터베이스 트랜잭션](/docs/{{version}}/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="handling-failed-jobs"></a>
### 실패한 작업 처리

가끔 큐잉된 이벤트 리스너가 실패할 수 있습니다. 큐잉된 리스너가 큐 워커에 정의된 최대 시도 횟수를 초과하면, 리스너의 `failed` 메서드가 호출됩니다. 이 메서드는 이벤트 인스턴스와 실패를 일으킨 `Throwable` 예외 객체를 전달받습니다:

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

<a name="specifying-queued-listener-maximum-attempts"></a>
#### 큐 리스너의 최대 시도 횟수 지정

큐잉된 리스너가 오류를 계속 발생시키면 무한정 재시도되는 걸 막는 것이 좋습니다. 이를 위해 리스너를 몇 번이나(혹은 얼마나 오랫동안) 시도할지 지정할 수 있는 방법들이 있습니다.

리스너 클래스에 `$tries` 속성을 정의하면, 정해진 횟수만큼 시도한 뒤 실패로 간주할 수 있습니다:

    <?php

    namespace App\Listeners;

    use App\Events\OrderShipped;
    use Illuminate\Contracts\Queue\ShouldQueue;
    use Illuminate\Queue\InteractsWithQueue;

    class SendShipmentNotification implements ShouldQueue
    {
        use InteractsWithQueue;

        /**
         * 큐 리스너의 최대 시도 횟수.
         *
         * @var int
         */
        public $tries = 5;
    }

반면, 지정된 시각까지 시도하다가 넘으면 더 이상 시도하지 않게 하고 싶다면, 리스너 클래스에 `retryUntil` 메서드를 추가하세요. 이 메서드는 `DateTime` 인스턴스를 반환해야 합니다:

    /**
     * 이 리스너가 타임아웃되어야 하는 시점 반환.
     *
     * @return \DateTime
     */
    public function retryUntil()
    {
        return now()->addMinutes(5);
    }

<a name="dispatching-events"></a>
## 이벤트 디스패치

이벤트를 발생시키려면, 해당 이벤트에서 static `dispatch` 메서드를 호출하세요. 이 메서드는 `Illuminate\Foundation\Events\Dispatchable` 트레이트가 제공하며, 인자로 전달하는 값은 이벤트 생성자에 전달됩니다:

    <?php

    namespace App\Http\Controllers;

    use App\Events\OrderShipped;
    use App\Http\Controllers\Controller;
    use App\Models\Order;
    use Illuminate\Http\Request;

    class OrderShipmentController extends Controller
    {
        /**
         * 지정된 주문을 배송 처리합니다.
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

조건에 따라 이벤트를 디스패치하고 싶다면, `dispatchIf`, `dispatchUnless` 메서드를 사용하세요:

    OrderShipped::dispatchIf($condition, $order);

    OrderShipped::dispatchUnless($condition, $order);

> **참고**
> 테스트 시, 실제 리스너를 작동시키지 않고 특정 이벤트가 발생했는지만 검증할 수 있습니다. Laravel의 [내장 테스트 헬퍼](/docs/{{version}}/mocking#event-fake)를 참고하세요.

<a name="event-subscribers"></a>
## 이벤트 구독자

<a name="writing-event-subscribers"></a>
### 이벤트 구독자 작성

이벤트 구독자는 하나의 클래스에서 여러 이벤트를 구독할 수 있는 클래스입니다. 이는 여러 이벤트 핸들러를 하나의 클래스에 정의할 수 있게 해줍니다. 구독자 클래스는 `subscribe` 메서드를 정의해야 하며, 이 메서드에는 이벤트 디스패처 인스턴스가 전달됩니다. 이 디스패처의 `listen` 메서드를 사용하여 이벤트 리스너를 등록할 수 있습니다:

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
         * 구독자의 리스너 등록.
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

구독자 자체에 이벤트 리스너 메서드가 정의되어 있다면, 구독자의 `subscribe` 메서드에서 이벤트와 메서드명을 배열로 반환하는 방식도 유용합니다. 이 경우 Laravel이 구독자 클래스명을 자동으로 인식하여 이벤트 리스너를 등록합니다:

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
         * 구독자의 리스너 등록.
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

<a name="registering-event-subscribers"></a>
### 이벤트 구독자 등록

구독자 클래스를 작성했다면, 이벤트 디스패처에 등록해야 합니다. 등록은 `EventServiceProvider`의 `$subscribe` 속성을 사용합니다. 예를 들어 `UserEventSubscriber`를 추가해보겠습니다:

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