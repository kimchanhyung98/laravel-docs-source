# 이벤트 (Events)

- [소개](#introduction)
- [이벤트 및 리스너 생성하기](#generating-events-and-listeners)
- [이벤트 및 리스너 등록하기](#registering-events-and-listeners)
    - [이벤트 탐색](#event-discovery)
    - [이벤트 수동 등록](#manually-registering-events)
    - [클로저 리스너](#closure-listeners)
- [이벤트 정의하기](#defining-events)
- [리스너 정의하기](#defining-listeners)
- [큐잉된 이벤트 리스너](#queued-event-listeners)
    - [큐와 수동으로 상호작용하기](#manually-interacting-with-the-queue)
    - [큐잉된 리스너와 데이터베이스 트랜잭션](#queued-event-listeners-and-database-transactions)
    - [실패한 작업 처리하기](#handling-failed-jobs)
- [이벤트 디스패치하기](#dispatching-events)
    - [데이터베이스 트랜잭션 후 이벤트 디스패치하기](#dispatching-events-after-database-transactions)
- [이벤트 구독자](#event-subscribers)
    - [이벤트 구독자 작성하기](#writing-event-subscribers)
    - [이벤트 구독자 등록하기](#registering-event-subscribers)
- [테스트](#testing)
    - [일부 이벤트 페이크하기](#faking-a-subset-of-events)
    - [범위 지정된 이벤트 페이크](#scoped-event-fakes)

<a name="introduction"></a>
## 소개

Laravel의 이벤트는 간단한 옵저버 패턴(observer pattern)을 구현한 것으로, 애플리케이션 내에서 발생하는 다양한 이벤트를 구독하고 청취할 수 있게 해줍니다. 이벤트 클래스는 보통 `app/Events` 디렉터리에 저장되며, 해당 이벤트를 수신하는 리스너는 `app/Listeners`에 위치합니다. 애플리케이션에 이 디렉터리들이 없더라도 Artisan 콘솔 명령어를 통해 이벤트와 리스너를 생성할 때 자동으로 만들어지므로 걱정하지 않으셔도 됩니다.

이벤트는 애플리케이션의 다양한 부분을 느슨하게 결합하는 훌륭한 수단입니다. 하나의 이벤트에 여러 리스너가 연결될 수 있고, 리스너들이 서로 의존하지 않아도 됩니다. 예를 들어, 주문이 출고될 때마다 Slack 알림을 보내고 싶다고 할 때, 주문 처리 코드에 Slack 알림 코드를 직접 연결하는 대신 `App\Events\OrderShipped` 이벤트를 발생시키고, 이 이벤트를 청취하는 리스너가 Slack 알림을 보내도록 작성할 수 있습니다.

<a name="generating-events-and-listeners"></a>
## 이벤트 및 리스너 생성하기

이벤트와 리스너를 빠르게 생성하려면 `make:event` 및 `make:listener` Artisan 명령어를 사용할 수 있습니다:

```shell
php artisan make:event PodcastProcessed

php artisan make:listener SendPodcastNotification --event=PodcastProcessed
```

편의를 위해, 추가 인자 없이 `make:event`와 `make:listener` 명령어를 호출하면 Laravel이 자동으로 클래스 이름과, 리스너 생성 시에는 어떤 이벤트를 청취할지 차례로 물어봅니다:

```shell
php artisan make:event

php artisan make:listener
```

<a name="registering-events-and-listeners"></a>
## 이벤트 및 리스너 등록하기

<a name="event-discovery"></a>
### 이벤트 탐색

기본적으로 Laravel은 애플리케이션 내 `Listeners` 디렉터리를 스캔하여 이벤트 리스너를 자동으로 찾아 등록합니다. Laravel이 `handle`이나 `__invoke`로 시작하는 메서드가 있는 리스너 클래스를 발견하면, 해당 메서드의 타입 힌트된 인자(이벤트 클래스)를 보고 관련 이벤트의 리스너로 등록합니다:

```
use App\Events\PodcastProcessed;

class SendPodcastNotification
{
    /**
     * 주어진 이벤트 처리하기.
     */
    public function handle(PodcastProcessed $event): void
    {
        // ...
    }
}
```

PHP의 합집합 타입(union types)을 사용해 여러 이벤트를 수신하는 것도 가능합니다:

```
/**
 * 주어진 이벤트 처리하기.
 */
public function handle(PodcastProcessed|PodcastPublished $event): void
{
    // ...
}
```

리스너를 다른 디렉터리나 여러 디렉터리에 저장할 계획이라면, 애플리케이션의 `bootstrap/app.php` 파일에서 `withEvents` 메서드를 이용해 Laravel에 스캔할 경로를 명시할 수 있습니다:

```
->withEvents(discover: [
    __DIR__.'/../app/Domain/Orders/Listeners',
])
```

`*` 와일드카드를 사용해 비슷한 구조의 여러 디렉터리를 한 번에 스캔할 수도 있습니다:

```
->withEvents(discover: [
    __DIR__.'/../app/Domain/*/Listeners',
])
```

등록된 모든 리스너 목록은 `event:list` 명령어로 확인할 수 있습니다:

```shell
php artisan event:list
```

<a name="event-discovery-in-production"></a>
#### 프로덕션 환경에서 이벤트 탐색

애플리케이션 성능 향상을 위해 `optimize` 혹은 `event:cache` Artisan 명령어를 사용해 모든 리스너의 매니페스트 캐시를 생성할 수 있습니다. 보통 이 명령은 [배포 과정](/docs/11.x/deployment#optimization)에 포함시킵니다. 캐시된 매니페스트를 프레임워크가 이용해 이벤트 등록 속도를 높입니다. 이벤트 캐시를 제거하려면 `event:clear` 명령어를 사용하세요.

<a name="manually-registering-events"></a>
### 이벤트 수동 등록

`Event` 파사드를 사용하면 애플리케이션의 `AppServiceProvider`의 `boot` 메서드 내에서 이벤트와 그에 대응하는 리스너를 수동으로 등록할 수 있습니다:

```
use App\Domain\Orders\Events\PodcastProcessed;
use App\Domain\Orders\Listeners\SendPodcastNotification;
use Illuminate\Support\Facades\Event;

/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Event::listen(
        PodcastProcessed::class,
        SendPodcastNotification::class,
    );
}
```

등록된 모든 리스너는 동일하게 `event:list` 명령어로 확인할 수 있습니다:

```shell
php artisan event:list
```

<a name="closure-listeners"></a>
### 클로저 리스너

보통 리스너는 클래스로 정의하지만, 애플리케이션의 `AppServiceProvider`의 `boot` 메서드 내에서 클로저 기반 이벤트 리스너를 직접 등록할 수도 있습니다:

```
use App\Events\PodcastProcessed;
use Illuminate\Support\Facades\Event;

/**
 * 애플리케이션 서비스 부트스트랩.
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

클로저 기반 이벤트 리스너를 등록할 때, `Illuminate\Events\queueable` 함수를 사용해 해당 클로저 리스너를 큐에서 실행하도록 Laravel에 지시할 수 있습니다:

```
use App\Events\PodcastProcessed;
use function Illuminate\Events\queueable;
use Illuminate\Support\Facades\Event;

/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Event::listen(queueable(function (PodcastProcessed $event) {
        // ...
    }));
}
```

큐잉된 작업처럼 `onConnection`, `onQueue`, `delay` 메서드를 사용해 큐에 들어가는 리스너의 실행 환경을 커스터마이징할 수 있습니다:

```
Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->onConnection('redis')->onQueue('podcasts')->delay(now()->addSeconds(10)));
```

익명 큐잉 리스너 실패 시 처리하고 싶다면 `queueable` 리스너 정의 시 `catch` 메서드에 클로저를 제공할 수 있습니다. 해당 클로저는 이벤트 객체와 실패 원인인 `Throwable` 객체를 받습니다:

```
use App\Events\PodcastProcessed;
use function Illuminate\Events\queueable;
use Illuminate\Support\Facades\Event;
use Throwable;

Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->catch(function (PodcastProcessed $event, Throwable $e) {
    // 큐잉된 리스너가 실패했을 때 처리...
}));
```

<a name="wildcard-event-listeners"></a>
#### 와일드카드 이벤트 리스너

`*` 문자를 와일드카드로 사용해 다수의 이벤트를 한 리스너에서 처리할 수도 있습니다. 와일드카드 리스너는 첫 번째 인자로 이벤트 이름을, 두 번째 인자로 전체 이벤트 데이터 배열을 받습니다:

```
Event::listen('event.*', function (string $eventName, array $data) {
    // ...
});
```

<a name="defining-events"></a>
## 이벤트 정의하기

이벤트 클래스는 이벤트와 관련된 정보를 담는 데이터 컨테이너입니다. 예를 들어 `App\Events\OrderShipped` 이벤트가 Eloquent ORM 객체를 받는 경우를 살펴봅시다:

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
     * 새로운 이벤트 인스턴스 생성.
     */
    public function __construct(
        public Order $order,
    ) {}
}
```

보시다시피 이 이벤트 클래스에는 로직이 없습니다. 구매된 `App\Models\Order` 인스턴스를 담는 컨테이너 역할만 합니다. 이벤트가 PHP의 `serialize` 함수로 직렬화될 때, 예를 들어 [큐잉된 리스너](#queued-event-listeners)를 사용할 때 `SerializesModels` 트레이트가 Eloquent 모델을 적절히 직렬화해 줍니다.

<a name="defining-listeners"></a>
## 리스너 정의하기

다음은 예제 이벤트를 수신하는 리스너입니다. 이벤트 리스너는 `handle` 메서드로 이벤트 인스턴스를 받습니다. `make:listener` Artisan 명령어는 `--event` 옵션과 함께 실행 시 적절한 이벤트 클래스를 import하며, `handle` 메서드에 타입힌트를 자동으로 추가해 줍니다. `handle` 메서드 내에서 이벤트에 대응해 필요한 작업을 수행할 수 있습니다:

```
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
     * 이벤트 처리 메서드.
     */
    public function handle(OrderShipped $event): void
    {
        // $event->order를 통해 주문에 접근...
    }
}
```

> [!NOTE]  
> 이벤트 리스너는 생성자에 필요한 의존성을 타입힌트할 수 있습니다. 모든 이벤트 리스너는 Laravel [서비스 컨테이너](/docs/11.x/container)를 통해 해결되므로 의존성이 자동으로 주입됩니다.

<a name="stopping-the-propagation-of-an-event"></a>
#### 이벤트 전파 중단하기

때때로 이벤트가 다른 리스너에게 전파되는 것을 중단하고 싶을 수 있습니다. 이 경우 리스너의 `handle` 메서드에서 `false`를 반환하면 이벤트 전파가 중단됩니다.

<a name="queued-event-listeners"></a>
## 큐잉된 이벤트 리스너

리스너가 이메일 전송이나 HTTP 요청 같이 시간이 오래 걸리는 작업을 수행한다면 큐잉하는 것이 유리합니다. 큐잉된 리스너를 사용하기 전에 [큐 설정](/docs/11.x/queues)을 마치고, 서버나 개발 환경에서 큐 작업자를 실행해야 합니다.

리스너를 큐잉 대상으로 지정하려면 리스너 클래스에 `ShouldQueue` 인터페이스를 추가하세요. `make:listener` 명령어로 생성된 리스너는 이미 이 인터페이스를 import하고 있으므로 바로 사용하면 됩니다:

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

이제 이 리스너가 처리하는 이벤트가 디스패치되면, Laravel의 [큐 시스템](/docs/11.x/queues)을 통해 자동으로 큐잉됩니다. 큐 작업자가 실행 중 오류 없이 처리하면, 작업이 끝난 후 자동으로 삭제됩니다.

<a name="customizing-the-queue-connection-queue-name"></a>
#### 큐 연결, 큐 이름, 지연 시간 커스터마이징

리스너 클래스에 `$connection`, `$queue`, `$delay` 속성을 정의해 큐 연결명, 큐 이름, 작업 지연 시간을 지정할 수 있습니다:

```
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    /**
     * 작업이 전송될 큐 연결명.
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
     * 작업이 처리되기 전까지 지연되는 시간(초).
     *
     * @var int
     */
    public $delay = 60;
}
```

런타임에서 연결명, 큐 이름, 지연 시간을 지정하고 싶으면 `viaConnection`, `viaQueue`, `withDelay` 메서드를 구현하세요:

```
/**
 * 리스너의 큐 연결명 반환.
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
 * 작업이 처리되기 전까지 대기할 초 단위 시간 반환.
 */
public function withDelay(OrderShipped $event): int
{
    return $event->highPriority ? 0 : 60;
}
```

<a name="conditionally-queueing-listeners"></a>
#### 조건부 큐잉 리스너

런타임에 따라 리스너를 큐에 넣을지 판단하려면, 리스너에 `shouldQueue` 메서드를 추가해 `true` 혹은 `false`를 반환하게 하세요. `false`를 반환하면 큐에 들어가지 않습니다:

```
<?php

namespace App\Listeners;

use App\Events\OrderCreated;
use Illuminate\Contracts\Queue\ShouldQueue;

class RewardGiftCard implements ShouldQueue
{
    /**
     * 기프트카드 보상 처리.
     */
    public function handle(OrderCreated $event): void
    {
        // ...
    }

    /**
     * 리스너가 큐에 들어갈지 여부 결정.
     */
    public function shouldQueue(OrderCreated $event): bool
    {
        return $event->order->subtotal >= 5000;
    }
}
```

<a name="manually-interacting-with-the-queue"></a>
### 큐와 수동으로 상호작용하기

리스너의 내부 큐 작업의 `delete` 또는 `release` 메서드에 직접 접근해야 할 경우 `Illuminate\Queue\InteractsWithQueue` 트레이트를 사용할 수 있습니다. 생성된 리스너에는 기본적으로 이 트레이트가 import되어 있으며, 이 메서드들을 사용할 수 있게 합니다:

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
     * 이벤트 처리 메서드.
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
### 큐잉된 리스너와 데이터베이스 트랜잭션

데이터베이스 트랜잭션 중에 큐잉된 리스너를 디스패치하면, 큐 작업자가 트랜잭션 커밋 전에 작업을 처리할 수 있습니다. 이 경우 트랜잭션에서 갱신한 모델이나 레코드가 데이터베이스에 반영되지 않았거나, 새롭게 생성한 모델이나 레코드가 존재하지 않을 수 있습니다. 이런 상황에서 리스너가 해당 모델에 의존하면 예상치 못한 오류가 날 수 있습니다.

큐 연결의 `after_commit` 설정이 `false`일 경우, 특정 큐잉 리스너가 모든 열린 데이터베이스 트랜잭션이 커밋된 후에 실행되도록 하려면, 리스너 클래스에 `ShouldQueueAfterCommit` 인터페이스를 구현하세요:

```
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
> 이 이슈 관련 자세한 내용은 [큐 작업과 데이터베이스 트랜잭션](/docs/11.x/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="handling-failed-jobs"></a>
### 실패한 작업 처리하기

큐잉된 이벤트 리스너가 실패할 수 있습니다. 큐 작업자가 최대 시도 횟수를 초과하면 리스너 내 `failed` 메서드가 호출됩니다. `failed` 메서드는 이벤트 인스턴스와 실패 원인이 된 `Throwable` 객체를 인자로 받습니다:

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
     * 이벤트 처리 메서드.
     */
    public function handle(OrderShipped $event): void
    {
        // ...
    }

    /**
     * 작업 실패 처리 메서드.
     */
    public function failed(OrderShipped $event, Throwable $exception): void
    {
        // ...
    }
}
```

<a name="specifying-queued-listener-maximum-attempts"></a>
#### 큐잉된 리스너 최대 시도 횟수 지정하기

에러가 발생하는 큐 리스너가 무한히 재시도하는 것을 방지하기 위해, 리스너 클래스에 `$tries` 속성을 정의해 최대 시도 횟수를 지정할 수 있습니다:

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
     * 최대 재시도 횟수.
     *
     * @var int
     */
    public $tries = 5;
}
```

또는, 특정 시간 이후에는 시도를 중단하도록 `retryUntil` 메서드를 구현할 수도 있습니다. 이 메서드는 `DateTime` 인스턴스를 반환해야 합니다:

```
use DateTime;

/**
 * 리스너 타임아웃 시간 결정.
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(5);
}
```

<a name="specifying-queued-listener-backoff"></a>
#### 큐잉된 리스너 재시도 대기 시간 지정하기

리스너가 예외로 실패했을 때, 다음 재시도를 몇 초 뒤에 할지 정하려면 리스너 클래스에 `backoff` 속성을 정의하거나, 더 복잡한 로직이 필요하면 `backoff()` 메서드를 구현하세요:

```
/**
 * 재시도 전 대기 시간(초).
 *
 * @var int
 */
public $backoff = 3;
```

```
/**
 * 재시도 전 대기 시간(초) 계산.
 */
public function backoff(): int
{
    return 3;
}
```

`backoff()` 메서드에서 배열을 반환하면 "지수 증가" 방식도 쉽게 구현할 수 있습니다. 예를 들어 다음과 같이 반환하면 첫 재시도는 1초, 두 번째는 5초, 세 번째는 10초, 그 이후는 계속 10초 대기합니다:

```
/**
 * 재시도 전 대기 시간 배열 반환.
 *
 * @return array<int, int>
 */
public function backoff(): array
{
    return [1, 5, 10];
}
```

<a name="dispatching-events"></a>
## 이벤트 디스패치하기

이벤트를 디스패치하려면 이벤트 클래스에서 정적 `dispatch` 메서드를 호출하면 됩니다. 이 메서드는 이벤트 클래스 내 `Illuminate\Foundation\Events\Dispatchable` 트레이트를 통해 제공됩니다. `dispatch` 메서드에 전달한 인수들은 이벤트 생성자에 그대로 전달됩니다:

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
     * 주어진 주문을 출고 처리합니다.
     */
    public function store(Request $request): RedirectResponse
    {
        $order = Order::findOrFail($request->order_id);

        // 주문 출고 처리 로직...

        OrderShipped::dispatch($order);

        return redirect('/orders');
    }
}
```

조건에 따라 이벤트 디스패치 여부를 결정하려면 `dispatchIf`와 `dispatchUnless` 메서드를 사용할 수 있습니다:

```
OrderShipped::dispatchIf($condition, $order);

OrderShipped::dispatchUnless($condition, $order);
```

> [!NOTE]  
> 테스트 시 이벤트 리스너를 실제로 실행하지 않고 이벤트가 디스패치되었는지 검증하고 싶을 때 Laravel 내장 테스트 도구([테스트](#testing) 참고)를 활용하면 편리합니다.

<a name="dispatching-events-after-database-transactions"></a>
### 데이터베이스 트랜잭션 후 이벤트 디스패치하기

활성화된 데이터베이스 트랜잭션이 커밋된 후에만 이벤트를 디스패치하려면, 이벤트 클래스에 `ShouldDispatchAfterCommit` 인터페이스를 구현하세요.

이 인터페이스를 구현하면 현재 트랜잭션이 커밋될 때까지 이벤트가 디스패치되지 않습니다. 만약 트랜잭션이 실패하면 이벤트는 무시됩니다. 트랜잭션이 실행 중이지 않을 때는 이벤트가 즉시 디스패치됩니다:

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
     * 새로운 이벤트 인스턴스 생성.
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

이벤트 구독자는 하나의 클래스 안에서 여러 이벤트를 구독하고 처리할 수 있는 클래스로, 여러 이벤트 핸들러를 하나의 클래스에서 정의할 때 유용합니다. 구독자는 `subscribe` 메서드를 정의하며, 이 메서드는 이벤트 디스패처 인스턴스를 인자로 받습니다. 디스패처 객체의 `listen` 메서드를 호출해 이벤트 리스너를 등록할 수 있습니다:

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
     * 구독자 리스너 등록.
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

리스너가 구독자 클래스 내부에 모두 정의되어 있다면, `subscribe` 메서드에서 이벤트와 메서드명 배열을 반환하는 편이 더 편리합니다. Laravel은 구독자 클래스를 자동으로 인식해 이벤트 리스너를 등록합니다:

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
     * 구독자의 리스너 등록.
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

구독자 작성 후, Laravel은 [이벤트 탐색 규칙](#event-discovery)에 따라 자동으로 관련 핸들러 메서드를 등록합니다. 그렇지 않은 경우, `Event` 파사드의 `subscribe` 메서드를 사용해 수동으로 구독자를 등록할 수 있습니다. 보통 애플리케이션의 `AppServiceProvider` `boot` 메서드 내에서 이 작업을 합니다:

```
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
```

<a name="testing"></a>
## 테스트

이벤트를 디스패치하는 코드를 테스트할 때는, 이벤트 리스너들이 실제 실행되지 않도록 할 수 있습니다. 리스너의 동작은 리스너 자체를 직접 테스트할 수 있기 때문입니다. 리스너 직접 테스트를 위해선 테스트 내에서 리스너 인스턴스를 생성하고 `handle` 메서드를 호출하면 됩니다.

`Event` 파사드의 `fake` 메서드를 사용하면 리스너 실행을 막고, 테스트하려는 코드를 실행한 후 애플리케이션에서 어떤 이벤트가 디스패치됐는지 `assertDispatched`, `assertNotDispatched`, `assertNothingDispatched` 메서드를 통해 검증할 수 있습니다:

```php tab=Pest
<?php

use App\Events\OrderFailedToShip;
use App\Events\OrderShipped;
use Illuminate\Support\Facades\Event;

test('orders can be shipped', function () {
    Event::fake();

    // 주문 출고 처리...

    // 이벤트가 디스패치됐는지 검증...
    Event::assertDispatched(OrderShipped::class);

    // 이벤트가 두 번 디스패치됐는지 검증...
    Event::assertDispatched(OrderShipped::class, 2);

    // 이벤트가 디스패치되지 않았는지 검증...
    Event::assertNotDispatched(OrderFailedToShip::class);

    // 어떤 이벤트도 디스패치되지 않았는지 검증...
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
     * 주문 출고 테스트.
     */
    public function test_orders_can_be_shipped(): void
    {
        Event::fake();

        // 주문 출고 처리...

        // 이벤트가 디스패치됐는지 검증...
        Event::assertDispatched(OrderShipped::class);

        // 이벤트가 두 번 디스패치됐는지 검증...
        Event::assertDispatched(OrderShipped::class, 2);

        // 이벤트가 디스패치되지 않았는지 검증...
        Event::assertNotDispatched(OrderFailedToShip::class);

        // 어떤 이벤트도 디스패치되지 않았는지 검증...
        Event::assertNothingDispatched();
    }
}
```

`assertDispatched` 또는 `assertNotDispatched` 메서드에 클로저를 전달해 특정 조건을 만족하는 이벤트가 디스패치됐는지 체크할 수도 있습니다. 해당 조건을 만족하는 이벤트가 하나라도 있으면 검증이 성공합니다:

```
Event::assertDispatched(function (OrderShipped $event) use ($order) {
    return $event->order->id === $order->id;
});
```

특정 이벤트에 대해 리스너가 제대로 배정되어 있는지도 `assertListening` 메서드로 확인할 수 있습니다:

```
Event::assertListening(
    OrderShipped::class,
    SendShipmentNotification::class
);
```

> [!WARNING]  
> `Event::fake()`를 호출하면 모든 이벤트 리스너가 실행되지 않습니다. 따라서 모델 팩토리가 이벤트에 의존해 UUID를 생성하는 등 동작한다면, 팩토리를 사용한 뒤 `Event::fake()`를 호출하도록 하세요.

<a name="faking-a-subset-of-events"></a>
### 일부 이벤트만 페이크하기

특정 이벤트에 대해서만 리스너 실행을 막고 싶으면 `fake` 또는 `fakeFor` 메서드에 이벤트 배열을 전달하세요:

```php tab=Pest
test('orders can be processed', function () {
    Event::fake([
        OrderCreated::class,
    ]);

    $order = Order::factory()->create();

    Event::assertDispatched(OrderCreated::class);

    // 나머지 이벤트들은 정상적으로 디스패치됨...
    $order->update([...]);
});
```

```php tab=PHPUnit
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

    // 나머지 이벤트들은 정상적으로 디스패치됨...
    $order->update([...]);
}
```

특정 이벤트를 제외하고 모두 페이크하고 싶다면 `except` 메서드를 사용하세요:

```
Event::fake()->except([
    OrderCreated::class,
]);
```

<a name="scoped-event-fakes"></a>
### 범위 지정된 이벤트 페이크

테스트의 일부 구간에 한해 이벤트 리스너 실행을 막고 싶을 때 `fakeFor` 메서드를 사용할 수 있습니다:

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

    // 이후부터는 이벤트가 정상적으로 디스패치되고 옵저버도 실행됨...
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
     * 주문 처리 테스트.
     */
    public function test_orders_can_be_processed(): void
    {
        $order = Event::fakeFor(function () {
            $order = Order::factory()->create();

            Event::assertDispatched(OrderCreated::class);

            return $order;
        });

        // 이후부터는 이벤트가 정상적으로 디스패치되고 옵저버도 실행됨...
        $order->update([...]);
    }
}
```