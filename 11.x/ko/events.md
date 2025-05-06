# 이벤트

- [소개](#introduction)
- [이벤트 및 리스너 생성](#generating-events-and-listeners)
- [이벤트 및 리스너 등록](#registering-events-and-listeners)
    - [이벤트 검색](#event-discovery)
    - [이벤트 수동 등록](#manually-registering-events)
    - [클로저 리스너](#closure-listeners)
- [이벤트 정의](#defining-events)
- [리스너 정의](#defining-listeners)
- [큐잉된 이벤트 리스너](#queued-event-listeners)
    - [큐 수동 조작](#manually-interacting-with-the-queue)
    - [큐잉된 이벤트 리스너와 데이터베이스 트랜잭션](#queued-event-listeners-and-database-transactions)
    - [실패한 작업 처리하기](#handling-failed-jobs)
- [이벤트 디스패치(발생시키기)](#dispatching-events)
    - [데이터베이스 트랜잭션 이후의 이벤트 디스패치](#dispatching-events-after-database-transactions)
- [이벤트 구독자](#event-subscribers)
    - [이벤트 구독자 작성하기](#writing-event-subscribers)
    - [이벤트 구독자 등록하기](#registering-event-subscribers)
- [테스트](#testing)
    - [이벤트 일부만 페이크 처리하기](#faking-a-subset-of-events)
    - [스코프를 제한한 이벤트 페이크](#scoped-event-fakes)

<a name="introduction"></a>
## 소개

Laravel의 이벤트는 간단한 옵저버 패턴 구현체를 제공하여, 애플리케이션 내에서 발생하는 다양한 이벤트를 구독하고 리스닝할 수 있게 해줍니다. 이벤트 클래스는 일반적으로 `app/Events` 디렉터리에 저장되며, 리스너는 `app/Listeners` 디렉터리에 저장됩니다. 만약 애플리케이션에 이 디렉터리가 없다면, Artisan 콘솔 명령어로 이벤트와 리스너를 생성할 때 자동으로 생성되므로 걱정하지 않으셔도 됩니다.

이벤트는 애플리케이션의 다양한 측면을 결합하지 않고 처리하는 좋은 방법이 됩니다. 하나의 이벤트는 서로 의존하지 않는 여러 리스너를 가질 수 있기 때문입니다. 예를 들어, 주문이 출고될 때마다 사용자에게 Slack 알림을 보내고 싶을 때, 주문 프로세싱 코드를 Slack 알림 코드와 결합하는 대신, `App\Events\OrderShipped` 이벤트를 발생시키고 해당 이벤트를 리스너에서 수신하여 Slack 알림을 보내는 방식으로 구현할 수 있습니다.

<a name="generating-events-and-listeners"></a>
## 이벤트 및 리스너 생성

이벤트와 리스너를 빠르게 생성하려면, `make:event`와 `make:listener` Artisan 명령어를 사용할 수 있습니다:

```shell
php artisan make:event PodcastProcessed

php artisan make:listener SendPodcastNotification --event=PodcastProcessed
```

편의를 위해, 추가 인수 없이 `make:event` 및 `make:listener` Artisan 명령어를 실행할 수도 있습니다. 이렇게 하면 Laravel이 클래스 이름과(리스너 생성 시에는) 리스너가 수신할 이벤트를 자동으로 물어봅니다.

```shell
php artisan make:event

php artisan make:listener
```

<a name="registering-events-and-listeners"></a>
## 이벤트 및 리스너 등록

<a name="event-discovery"></a>
### 이벤트 검색

기본적으로, Laravel은 애플리케이션의 `Listeners` 디렉터리를 검색하여 이벤트 리스너를 자동으로 찾고 등록합니다. `handle` 또는 `__invoke`로 시작하는 리스너 클래스 메서드를 발견하면, 해당 메서드의 시그니처에 타입힌트된 이벤트에 대한 리스너로 등록합니다.

    use App\Events\PodcastProcessed;

    class SendPodcastNotification
    {
        /**
         * 주어진 이벤트를 처리합니다.
         */
        public function handle(PodcastProcessed $event): void
        {
            // ...
        }
    }

PHP의 유니언 타입을 활용하여 여러 이벤트를 수신할 수도 있습니다.

    /**
     * 주어진 이벤트를 처리합니다.
     */
    public function handle(PodcastProcessed|PodcastPublished $event): void
    {
        // ...
    }

리스너를 별도의 디렉터리나 여러 디렉터리에 보관하려는 경우, `bootstrap/app.php` 파일에서 `withEvents` 메서드를 사용하여 해당 디렉터리를 검색하도록 Laravel에 지시할 수 있습니다:

    ->withEvents(discover: [
        __DIR__.'/../app/Domain/Orders/Listeners',
    ])

`*` 문자를 와일드카드로 사용하여 여러 유사한 디렉터리를 한 번에 검색할 수도 있습니다:

    ->withEvents(discover: [
        __DIR__.'/../app/Domain/*/Listeners',
    ])

`event:list` 명령어를 사용하면 애플리케이션에 등록된 모든 리스너를 확인할 수 있습니다:

```shell
php artisan event:list
```

<a name="event-discovery-in-production"></a>
#### 운영 환경에서 이벤트 검색

애플리케이션의 속도를 높이기 위해, `optimize` 또는 `event:cache` Artisan 명령어를 사용하여 애플리케이션의 모든 리스너에 대한 매니페스트를 캐싱해야 합니다. 이 명령어는 일반적으로 애플리케이션 [배포 과정](/docs/{{version}}/deployment#optimization) 중에 실행되어야 합니다. 이 매니페스트는 이벤트 등록 절차를 빠르게 하기 위해 프레임워크에서 사용됩니다. `event:clear` 명령어는 이벤트 캐시를 제거할 때 사용합니다.

<a name="manually-registering-events"></a>
### 이벤트 수동 등록

`Event` 파사드를 사용하여, 앱의 `AppServiceProvider`에서 이벤트와 해당 리스너를 수동으로 등록할 수 있습니다:

    use App\Domain\Orders\Events\PodcastProcessed;
    use App\Domain\Orders\Listeners\SendPodcastNotification;
    use Illuminate\Support\Facades\Event;

    /**
     * 애플리케이션 서비스를 부트스트랩합니다.
     */
    public function boot(): void
    {
        Event::listen(
            PodcastProcessed::class,
            SendPodcastNotification::class,
        );
    }

등록된 모든 리스너 목록을 확인하려면 `event:list` 명령어를 사용할 수 있습니다:

```shell
php artisan event:list
```

<a name="closure-listeners"></a>
### 클로저 리스너

일반적으로 리스너는 클래스로 정의되지만, 앱의 `AppServiceProvider`에서 클로저 기반 이벤트 리스너도 수동으로 등록할 수 있습니다:

    use App\Events\PodcastProcessed;
    use Illuminate\Support\Facades\Event;

    /**
     * 애플리케이션 서비스를 부트스트랩합니다.
     */
    public function boot(): void
    {
        Event::listen(function (PodcastProcessed $event) {
            // ...
        });
    }

<a name="queuable-anonymous-event-listeners"></a>
#### 큐잉 가능한 익명 이벤트 리스너

클로저 기반 이벤트 리스너를 등록할 때, 리스너 클로저를 `Illuminate\Events\queueable` 함수로 감싸서 [큐](/docs/{{version}}/queues)를 통해 리스너를 실행하도록 할 수 있습니다.

    use App\Events\PodcastProcessed;
    use function Illuminate\Events\queueable;
    use Illuminate\Support\Facades/Event;

    /**
     * 애플리케이션 서비스 부트스트랩
     */
    public function boot(): void
    {
        Event::listen(queueable(function (PodcastProcessed $event) {
            // ...
        }));
    }

큐잉된 작업과 동일하게, `onConnection`, `onQueue`, `delay` 메서드를 사용하여 큐 리스너의 실행을 사용자화할 수 있습니다:

    Event::listen(queueable(function (PodcastProcessed $event) {
        // ...
    })->onConnection('redis')->onQueue('podcasts')->delay(now()->addSeconds(10)));

익명 큐 리스너가 실패할 경우를 처리하고 싶다면, `queueable` 리스너를 정의할 때 `catch` 메서드에 클로저를 전달할 수 있습니다. 이 클로저는 이벤트 인스턴스와 리스너 실패의 원인이 된 `Throwable` 인스턴스를 전달받습니다:

    use App\Events\PodcastProcessed;
    use function Illuminate\Events\queueable;
    use Illuminate\Support\Facades\Event;
    use Throwable;

    Event::listen(queueable(function (PodcastProcessed $event) {
        // ...
    })->catch(function (PodcastProcessed $event, Throwable $e) {
        // 큐 리스너가 실패했을 때...
    }));

<a name="wildcard-event-listeners"></a>
#### 와일드카드 이벤트 리스너

`*` 문자를 와일드카드로 사용하여 하나의 리스너에서 여러 이벤트를 포착하도록 리스너를 등록할 수도 있습니다. 와일드카드 리스너는 이벤트 이름을 첫 번째 인자로, 전체 이벤트 데이터 배열을 두 번째 인자로 받습니다.

    Event::listen('event.*', function (string $eventName, array $data) {
        // ...
    });

<a name="defining-events"></a>
## 이벤트 정의

이벤트 클래스는 본질적으로 이벤트와 관련된 정보를 담는 데이터 컨테이너입니다. 예를 들어, `App\Events\OrderShipped` 이벤트가 [Eloquent ORM](/docs/{{version}}/eloquent) 객체를 받는다고 가정해보겠습니다:

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
         * 새로운 이벤트 인스턴스 생성자.
         */
        public function __construct(
            public Order $order,
        ) {}
    }

보시다시피, 이 이벤트 클래스엔 로직이 없습니다. 이는 구매된 `App\Models\Order` 인스턴스를 담는 컨테이너 역할만을 합니다. 이벤트에서 사용하는 `SerializesModels` trait은 이벤트 객체를 PHP의 `serialize` 함수로 직렬화할 때(예: [큐잉 리스너](#queued-event-listeners) 사용 시) Eloquent 모델을 안전하게 직렬화해줍니다.

<a name="defining-listeners"></a>
## 리스너 정의

다음으로, 예시 이벤트의 리스너를 살펴보겠습니다. 이벤트 리스너는 이벤트 인스턴스를 `handle` 메서드에서 받습니다. `make:listener` Artisan 명령어를 실행할 때 `--event` 옵션을 함께 사용하면, 해당 이벤트 클래스를 자동 import 및 타입힌트 해줍니다. `handle` 메서드 내에서 이벤트에 대한 응답 작업을 수행할 수 있습니다.

    <?php

    namespace App\Listeners;

    use App\Events\OrderShipped;

    class SendShipmentNotification
    {
        /**
         * 이벤트 리스너 생성자.
         */
        public function __construct() {}

        /**
         * 이벤트 처리.
         */
        public function handle(OrderShipped $event): void
        {
            // $event->order를 통해 주문 정보 접근
        }
    }

> [!NOTE]  
> 이벤트 리스너는 생성자에서 필요한 의존성을 타입힌트로 명시할 수도 있습니다. 모든 이벤트 리스너는 Laravel [서비스 컨테이너](/docs/{{version}}/container)를 통해 해석되므로, 의존성 주입이 자동으로 이루어집니다.

<a name="stopping-the-propagation-of-an-event"></a>
#### 이벤트 전파 중단

경우에 따라 이벤트의 전파를 다른 리스너로 전달하지 않고 중단하고 싶을 수 있습니다. 이를 위해 리스너의 `handle` 메서드에서 `false`를 반환하면 전파가 중지됩니다.

<a name="queued-event-listeners"></a>
## 큐잉된 이벤트 리스너

리스너에서 메일 전송, HTTP 요청과 같은 느린 작업을 할 경우, 리스너를 큐잉시키면 성능상 이점이 있습니다. 큐잉된 리스너를 사용하려면, [큐를 설정](/docs/{{version}}/queues) 하고, 서버나 개발 환경에서 큐 워커를 실행해야 합니다.

리스너가 큐잉되어야 함을 지정하려면, 리스너 클래스에 `ShouldQueue` 인터페이스를 추가하세요. `make:listener` Artisan 명령어로 생성된 리스너는 이미 이 인터페이스가 import되어 있으므로 바로 사용할 수 있습니다.

    <?php

    namespace App\Listeners;

    use App\Events\OrderShipped;
    use Illuminate\Contracts\Queue\ShouldQueue;

    class SendShipmentNotification implements ShouldQueue
    {
        // ...
    }

이제, 이 리스너가 처리하는 이벤트가 디스패치될 때, 리스너는 Laravel의 [큐 시스템](/docs/{{version}}/queues)을 통해 자동으로 큐잉됩니다. 큐에서 작업이 실행될 때 예외가 발생하지 않으면, 큐 작업은 처리 후 자동으로 삭제됩니다.

<a name="customizing-the-queue-connection-queue-name"></a>
#### 큐 연결, 이름, 지연 시간 커스터마이즈

리스너의 큐 연결(Connection), 큐 이름(Queue Name), 지연 시간(Delay)을 커스터마이즈하려면, 리스너 클래스에 `$connection`, `$queue`, `$delay` 속성을 정의할 수 있습니다.

    <?php

    namespace App\Listeners;

    use App\Events\OrderShipped;
    use Illuminate\Contracts\Queue\ShouldQueue;

    class SendShipmentNotification implements ShouldQueue
    {
        /**
         * 작업이 보낼 연결 이름
         *
         * @var string|null
         */
        public $connection = 'sqs';

        /**
         * 작업이 보낼 큐 이름
         *
         * @var string|null
         */
        public $queue = 'listeners';

        /**
         * 작업이 처리되기 전 대기 시간(초)
         *
         * @var int
         */
        public $delay = 60;
    }

런타임에 연결, 큐, 지연을 동적으로 지정하려면, 리스너에 `viaConnection`, `viaQueue`, `withDelay` 메서드를 정의할 수 있습니다.

    /**
     * 리스너 큐 연결 이름 반환.
     */
    public function viaConnection(): string
    {
        return 'sqs';
    }

    /**
     * 리스너의 큐 이름 반환.
     */
    public function viaQueue(): string
    {
        return 'listeners';
    }

    /**
     * 작업이 처리될 때까지의 지연 시간(초) 반환.
     */
    public function withDelay(OrderShipped $event): int
    {
        return $event->highPriority ? 0 : 60;
    }

<a name="conditionally-queueing-listeners"></a>
#### 조건부 큐잉 리스너

런타임에만 가능한 데이터에 따라 리스너가 큐잉되어야 하는지 결정해야 할 때가 있습니다. 이럴 땐 `shouldQueue` 메서드를 추가해서 리스너의 큐잉 여부를 결정할 수 있습니다. 이 메서드가 `false`를 반환하면 리스너는 큐잉되지 않습니다.

    <?php

    namespace App\Listeners;

    use App\Events\OrderCreated;
    use Illuminate\Contracts\Queue\ShouldQueue;

    class RewardGiftCard implements ShouldQueue
    {
        /**
         * 고객에게 기프트카드를 지급.
         */
        public function handle(OrderCreated $event): void
        {
            // ...
        }

        /**
         * 리스너가 큐잉되어야 하는지 여부 반환.
         */
        public function shouldQueue(OrderCreated $event): bool
        {
            return $event->order->subtotal >= 5000;
        }
    }

<a name="manually-interacting-with-the-queue"></a>
### 큐 수동 조작

리스너의 기본 큐 작업인 `delete`, `release` 메서드에 직접 접근해야 할 경우, `Illuminate\Queue\InteractsWithQueue` 트레잇을 사용하면 됩니다. 이 트레잇은 기본적으로 생성된 리스너에서 import되어 있습니다.

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

<a name="queued-event-listeners-and-database-transactions"></a>
### 큐잉된 이벤트 리스너와 데이터베이스 트랜잭션

큐잉된 리스너가 데이터베이스 트랜잭션 내에서 디스패치될 때, 큐에서 리스너가 트랜잭션 커밋 이전에 실행될 수 있습니다. 이런 일이 발생하면, 트랜잭션 중에 수정한 모델이나 DB 레코드가 아직 반영되지 않은 상태일 수 있고, 트랜잭션 내에서 생성된 데이터 역시 DB에 존재하지 않을 수 있습니다. 리스너가 이런 모델이나 레코드에 의존한다면 예기치 못한 오류가 발생할 수 있습니다.

큐 연결의 `after_commit` 옵션이 `false`로 설정된 경우에도, 특정 큐잉 리스너를 모든 열린 데이터베이스 트랜잭션 커밋 후에 디스패치하려면, 리스너 클래스에 `ShouldQueueAfterCommit` 인터페이스를 구현하면 됩니다.

    <?php

    namespace App\Listeners;

    use Illuminate\Contracts\Queue\ShouldQueueAfterCommit;
    use Illuminate\Queue\InteractsWithQueue;

    class SendShipmentNotification implements ShouldQueueAfterCommit
    {
        use InteractsWithQueue;
    }

> [!NOTE]
> 이 이슈를 우회하는 방법을 더 알고 싶다면 [큐잉 작업과 데이터베이스 트랜잭션](/docs/{{version}}/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="handling-failed-jobs"></a>
### 실패한 작업 처리하기

때때로 큐잉된 이벤트 리스너가 실패할 수 있습니다. 큐 워커에서 정의한 최대 시도 횟수를 초과하면, 리스너의 `failed` 메서드가 호출됩니다. 이 메서드는 이벤트 인스턴스와 원인이 된 `Throwable`을 전달받습니다.

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
         * 작업 실패 처리.
         */
        public function failed(OrderShipped $event, Throwable $exception): void
        {
            // ...
        }
    }

<a name="specifying-queued-listener-maximum-attempts"></a>
#### 큐 리스너 최대 시도 횟수 지정

큐잉된 리스너에서 오류가 발생했다면, 무한 반복해서 재시도하는 것을 원치 않을 것입니다. Laravel은 리스너가 시도할 수 있는 횟수나 시간을 명시할 다양한 방법을 제공합니다.

리스너 클래스에 `$tries` 속성을 정의하면, 리스너를 최대 몇 번까지 시도할지 지정할 수 있습니다:

    <?php

    namespace App\Listeners;

    use App\Events\OrderShipped;
    use Illuminate\Contracts\Queue\ShouldQueue;
    use Illuminate\Queue\InteractsWithQueue;

    class SendShipmentNotification implements ShouldQueue
    {
        use InteractsWithQueue;

        /**
         * 큐잉된 리스너가 시도될 최대 횟수
         *
         * @var int
         */
        public $tries = 5;
    }

시도 횟수가 아니라, 얼마만큼의 시간 동안만 시도해야 하는지 지정할 수도 있습니다. 이를 위해 리스너 클래스에 `retryUntil` 메서드를 추가하세요. 이 메서드는 `DateTime` 인스턴스를 반환해야 합니다:

    use DateTime;

    /**
     * 리스너의 타임아웃 시간 반환.
     */
    public function retryUntil(): DateTime
    {
        return now()->addMinutes(5);
    }

<a name="specifying-queued-listener-backoff"></a>
#### 큐 리스너 백오프(대기 시간) 지정

예외가 발생한 큐잉 리스너를 Laravel이 재시도하기 전 대기할 초를 지정하려면, 리스너 클래스에 `backoff` 속성을 정의하세요:

    /**
     * 큐잉된 리스너 재시도까지 대기할 초
     *
     * @var int
     */
    public $backoff = 3;

좀 더 복잡한 백오프 로직이 필요하다면, 클래스에 `backoff` 메서드를 정의할 수 있습니다:

    /**
     * 리스너 재시도 전 대기할 초 계산.
     */
    public function backoff(): int
    {
        return 3;
    }

배열을 반환하여 "지수적(exponential)" 백오프를 쉽게 구현할 수 있습니다. 아래 예시에서는, 첫 번째 재시도는 1초, 두 번째는 5초, 세 번째는 10초, 이후는 10초로 대기 시간이 늘어납니다:

    /**
     * 리스너 재시도 전 대기할 초 계산.
     *
     * @return array<int, int>
     */
    public function backoff(): array
    {
        return [1, 5, 10];
    }

<a name="dispatching-events"></a>
## 이벤트 디스패치(발생시키기)

이벤트를 발생시키려면, 해당 이벤트의 정적 `dispatch` 메서드를 호출하면 됩니다. 이 메서드는 이벤트가 사용하는 `Illuminate\Foundation\Events\Dispatchable` 트레잇을 통해 제공됩니다. `dispatch`에 전달하는 모든 인자는 이벤트의 생성자로 전달됩니다.

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
         * 주어진 주문을 출고 처리.
         */
        public function store(Request $request): RedirectResponse
        {
            $order = Order::findOrFail($request->order_id);

            // 주문 출고 로직...

            OrderShipped::dispatch($order);

            return redirect('/orders');
        }
    }

조건부로 이벤트를 디스패치하고 싶으면, `dispatchIf`, `dispatchUnless` 메서드를 사용할 수 있습니다:

    OrderShipped::dispatchIf($condition, $order);

    OrderShipped::dispatchUnless($condition, $order);

> [!NOTE]
> 테스트할 때, 실제로 리스너를 실행하지 않고 특정 이벤트가 디스패치되었는지 검증할 수 있습니다. Laravel의 [내장 테스트 헬퍼](#testing)가 이를 쉽게 만들어줍니다.

<a name="dispatching-events-after-database-transactions"></a>
### 데이터베이스 트랜잭션 이후의 이벤트 디스패치

종종, 이벤트를 적극 트랜잭션 커밋이 완료된 후에만 실행하고 싶을 수 있습니다. 이럴 경우, 이벤트 클래스에 `ShouldDispatchAfterCommit` 인터페이스를 구현하면 됩니다.

이 인터페이스를 구현하면, 현재 데이터베이스 트랜잭션이 커밋될 때까지 이벤트를 디스패치하지 않습니다. 트랜잭션이 실패하면 이벤트도 폐기됩니다. 만약 트랜잭션 없이 이벤트를 디스패치하면, 바로 디스패치됩니다.

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
         * 새로운 이벤트 인스턴스 생성자.
         */
        public function __construct(
            public Order $order,
        ) {}
    }

<a name="event-subscribers"></a>
## 이벤트 구독자

<a name="writing-event-subscribers"></a>
### 이벤트 구독자 작성하기

이벤트 구독자는 한 클래스 내부에서 여러 이벤트에 구독(등록)할 수 있도록 해주며, 여러 이벤트 핸들러를 한 클래스에 정의할 수 있습니다. 구독자는 반드시 `subscribe` 메서드를 정의하여야 하며, 이 메서드에는 이벤트 디스패처 인스턴스가 전달됩니다. 전달받은 디스패처의 `listen` 메서드를 호출하여 이벤트 리스너를 등록할 수 있습니다.

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
         * 구독자의 리스너 등록.
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

구독자 안에 리스너 메서드가 정의된 경우, `subscribe` 메서드에서 이벤트와 메서드명을 배열로 반환하면 더 편리합니다. Laravel이 이벤트 리스너 등록 시 구독자 클래스명을 자동으로 파악합니다.

    <?php

    namespace App\Listeners;

    use Illuminate\Auth\Events\Login;
    use Illuminate\Auth\Events\Logout;
    use Illuminate\Events\Dispatcher;

    class UserEventSubscriber
    {
        /**
         * 로그인 이벤트 처리.
         */
        public function handleUserLogin(Login $event): void {}

        /**
         * 로그아웃 이벤트 처리.
         */
        public function handleUserLogout(Logout $event): void {}

        /**
         * 구독자 리스너 등록.
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

<a name="registering-event-subscribers"></a>
### 이벤트 구독자 등록하기

구독자를 작성한 후, 구독자 메서드명이 [이벤트 검색 규칙](#event-discovery)을 따른다면 Laravel이 자동으로 등록합니다. 그렇지 않은 경우, `Event` 파사드의 `subscribe` 메서드로 수동 등록하면 됩니다. 이는 보통 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 설정합니다.

    <?php

    namespace App\Providers;

    use App\Listeners\UserEventSubscriber;
    use Illuminate\Support\Facades\Event;
    use Illuminate\Support\ServiceProvider;

    class AppServiceProvider extends ServiceProvider
    {
        /**
         * 애플리케이션 서비스 부트스트랩.
         */
        public function boot(): void
        {
            Event::subscribe(UserEventSubscriber::class);
        }
    }

<a name="testing"></a>
## 테스트

이벤트를 발생시키는 코드를 테스트할 때, 실제로 이벤트의 리스너가 동작하지 않게 하고 싶을 때가 있습니다. 왜냐하면 리스너의 코드는 따로 직접 테스트할 수 있기 때문이죠. 물론, 리스너 자체를 테스트할 때는 리스너 인스턴스를 생성하고 `handle` 메서드를 직접 호출하면 됩니다.

`Event` 파사드의 `fake` 메서드를 통해 리스너 실행을 막고, 테스트 대상 코드를 실행한 후, 애플리케이션에서 어떤 이벤트가 디스패치되었는지 `assertDispatched`, `assertNotDispatched`, `assertNothingDispatched` 메서드로 검증할 수 있습니다.

```php tab=Pest
<?php

use App\Events\OrderFailedToShip;
use App\Events\OrderShipped;
use Illuminate\Support\Facades\Event;

test('orders can be shipped', function () {
    Event::fake();

    // 주문 출고 처리...

    // 이벤트가 디스패치되었는지 확인...
    Event::assertDispatched(OrderShipped::class);

    // 이벤트가 2번 디스패치되었는지 확인...
    Event::assertDispatched(OrderShipped::class, 2);

    // 이벤트가 디스패치되지 않았는지 확인...
    Event::assertNotDispatched(OrderFailedToShip::class);

    // 아무 이벤트도 디스패치되지 않았는지 확인...
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
     * 주문 출고 테스트
     */
    public function test_orders_can_be_shipped(): void
    {
        Event::fake();

        // 주문 출고 처리...

        // 이벤트가 디스패치되었는지 확인...
        Event::assertDispatched(OrderShipped::class);

        // 이벤트가 2번 디스패치되었는지 확인...
        Event::assertDispatched(OrderShipped::class, 2);

        // 이벤트가 디스패치되지 않았는지 확인...
        Event::assertNotDispatched(OrderFailedToShip::class);

        // 아무 이벤트도 디스패치되지 않았는지 확인...
        Event::assertNothingDispatched();
    }
}
```

`assertDispatched`, `assertNotDispatched` 메서드에 클로저를 전달하면, 해당 "조건"을 만족하는 이벤트가 디스패치되었는지 검증할 수 있습니다. 조건에 맞는 이벤트가 하나라도 발견되면 테스트가 성공합니다.

    Event::assertDispatched(function (OrderShipped $event) use ($order) {
        return $event->order->id === $order->id;
    });

특정 이벤트에 대해 특정 리스너가 할당되어 있는지만 검증하고 싶다면 `assertListening` 메서드를 사용할 수 있습니다.

    Event::assertListening(
        OrderShipped::class,
        SendShipmentNotification::class
    );

> [!WARNING]
> `Event::fake()` 호출 이후에는 어떤 이벤트 리스너도 실행되지 않습니다. 따라서, 모델의 `creating` 이벤트를 통해 UUID를 생성하는 등 이벤트에 의존하는 팩토리를 사용하는 테스트에서는, 팩토리 사용 **이후**에 `Event::fake()`를 호출해야 합니다.

<a name="faking-a-subset-of-events"></a>
### 이벤트 일부만 페이크 처리하기

특정 이벤트에 대해서만 리스너 실행을 페이크 처리하고 싶다면, 해당 이벤트들을 `fake` 또는 `fakeFor` 메서드에 배열로 전달하세요:

```php tab=Pest
test('orders can be processed', function () {
    Event::fake([
        OrderCreated::class,
    ]);

    $order = Order::factory()->create();

    Event::assertDispatched(OrderCreated::class);

    // 다른 이벤트는 그대로 정상 디스패치됩니다...
    $order->update([...]);
});
```

```php tab=PHPUnit
/**
 * 주문 처리 테스트
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

특정 이벤트를 제외한 모든 이벤트를 페이크 처리하려면 `except` 메서드를 사용하세요:

    Event::fake()->except([
        OrderCreated::class,
    ]);

<a name="scoped-event-fakes"></a>
### 스코프를 제한한 이벤트 페이크

테스트의 특정 부분에서만 이벤트 리스너를 페이크 처리하고 싶으면, `fakeFor` 메서드를 사용할 수 있습니다.

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

    // 이후에는 이벤트 및 옵저버가 정상 실행됨...
    $order->update([...]);
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
     * 주문 처리 테스트
     */
    public function test_orders_can_be_processed(): void
    {
        $order = Event::fakeFor(function () {
            $order = Order::factory()->create();

            Event::assertDispatched(OrderCreated::class);

            return $order;
        });

        // 이후에는 이벤트 및 옵저버가 정상 실행됨...
        $order->update([...]);
    }
}
```