# 이벤트

- [소개](#introduction)
- [이벤트 및 리스너 생성하기](#generating-events-and-listeners)
- [이벤트 및 리스너 등록하기](#registering-events-and-listeners)
    - [이벤트 자동 탐지(Event Discovery)](#event-discovery)
    - [이벤트 수동 등록하기](#manually-registering-events)
    - [클로저(Closure) 리스너](#closure-listeners)
- [이벤트 정의하기](#defining-events)
- [리스너 정의하기](#defining-listeners)
- [큐잉되는 이벤트 리스너](#queued-event-listeners)
    - [큐 직접 다루기](#manually-interacting-with-the-queue)
    - [큐잉된 이벤트 리스너와 DB 트랜잭션](#queued-event-listeners-and-database-transactions)
    - [실패한 작업 처리하기](#handling-failed-jobs)
- [이벤트 디스패치(발생)하기](#dispatching-events)
    - [DB 트랜잭션 후 이벤트 디스패치](#dispatching-events-after-database-transactions)
- [이벤트 구독자](#event-subscribers)
    - [이벤트 구독자 작성하기](#writing-event-subscribers)
    - [이벤트 구독자 등록하기](#registering-event-subscribers)
- [테스트](#testing)
    - [일부 이벤트 Fake 처리](#faking-a-subset-of-events)
    - [범위 지정 이벤트 Fake](#scoped-event-fakes)

<a name="introduction"></a>
## 소개

Laravel의 이벤트는 간단한 옵저버 패턴(Observer Pattern) 구현을 제공하여, 애플리케이션 내에서 발생하는 다양한 이벤트를 구독하고 들을 수 있도록 해줍니다. 이벤트 클래스는 일반적으로 `app/Events` 디렉터리에, 리스너는 `app/Listeners` 디렉터리에 저장됩니다. 만약 애플리케이션에 이 디렉터리가 없더라도 Artisan 콘솔 명령어를 통해 이벤트와 리스너를 생성하면 자동으로 만들어집니다.

이벤트는 애플리케이션의 다양한 측면을 느슨하게 결합(Decouple)하는데 아주 유용합니다. 하나의 이벤트는 서로 의존하지 않는 여러 개의 리스너를 가질 수 있기 때문입니다. 예를 들어, 주문이 발송될 때마다 사용자의 슬랙에 알림을 보내고 싶다면 주문 처리 코드와 슬랙 알림 코드를 직접 연결하는 대신, `App\Events\OrderShipped` 이벤트를 발생시키고, 리스너가 이 이벤트를 받아 슬랙 알림을 전송하게 할 수 있습니다.

<a name="generating-events-and-listeners"></a>
## 이벤트 및 리스너 생성하기

이벤트와 리스너를 빠르게 생성하려면, `make:event`와 `make:listener` Artisan 명령어를 사용할 수 있습니다:

```shell
php artisan make:event PodcastProcessed

php artisan make:listener SendPodcastNotification --event=PodcastProcessed
```

편의를 위해 추가 인수 없이 `make:event`와 `make:listener` 명령어를 사용할 수도 있습니다. 이런 경우 Laravel이 클래스명 입력을 요청하고, 리스너 생성 시 어떤 이벤트를 들을지 물어봅니다:

```shell
php artisan make:event

php artisan make:listener
```

<a name="registering-events-and-listeners"></a>
## 이벤트 및 리스너 등록하기

<a name="event-discovery"></a>
### 이벤트 자동 탐지(Event Discovery)

Laravel은 기본적으로 애플리케이션의 `Listeners` 디렉터리를 스캔하여 이벤트 리스너를 자동으로 찾고 등록합니다. `handle` 또는 `__invoke`로 시작하는 리스너 클래스의 메서드는, 해당 메서드에서 타입힌트된 이벤트의 리스너로 자동 등록됩니다:

```php
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
```

PHP의 유니언 타입을 활용해 여러 이벤트를 들을 수도 있습니다:

```php
/**
 * 주어진 이벤트를 처리합니다.
 */
public function handle(PodcastProcessed|PodcastPublished $event): void
{
    // ...
}
```

리스너를 다른 디렉터리 또는 여러 디렉터리에 저장하려면, 애플리케이션의 `bootstrap/app.php` 파일에서 `withEvents` 메서드를 사용해 해당 경로를 지정할 수 있습니다:

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/Orders/Listeners',
])
```

`*`를 사용해 여러 유사한 디렉터리를 와일드카드로 지정할 수 있습니다:

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/*/Listeners',
])
```

현재 애플리케이션에 등록된 모든 리스너를 확인하려면 `event:list` 명령어를 사용할 수 있습니다:

```shell
php artisan event:list
```

<a name="event-discovery-in-production"></a>
#### 프로덕션 환경에서의 이벤트 자동 탐지

애플리케이션의 성능을 위해, `optimize` 또는 `event:cache` Artisan 명령어로 모든 리스너의 매니페스트를 캐싱해야 합니다. 일반적으로 이 명령어는 [배포 과정](/docs/{{version}}/deployment#optimization)에서 실행합니다. 이 매니페스트는 이벤트 등록 속도를 높이기 위해 프레임워크가 사용합니다. 이벤트 캐시를 삭제하려면 `event:clear` 명령어를 사용하면 됩니다.

<a name="manually-registering-events"></a>
### 이벤트 수동 등록하기

`Event` 파사드를 활용하면, 애플리케이션의 `AppServiceProvider`의 `boot` 메서드 안에서 이벤트와 해당 리스너를 수동으로 등록할 수 있습니다:

```php
use App\Domain\Orders\Events\PodcastProcessed;
use App\Domain\Orders\Listeners\SendPodcastNotification;
use Illuminate\Support\Facades\Event;

/**
 * 모든 애플리케이션 서비스를 부트스트랩합니다.
 */
public function boot(): void
{
    Event::listen(
        PodcastProcessed::class,
        SendPodcastNotification::class,
    );
}
```

`event:list` 명령어로 등록된 모든 리스너를 확인할 수 있습니다:

```shell
php artisan event:list
```

<a name="closure-listeners"></a>
### 클로저(Closure) 리스너

보통 리스너는 클래스 형태로 정의하지만, `AppServiceProvider`의 `boot` 메서드에 클로저로 이벤트 리스너를 등록할 수도 있습니다:

```php
use App\Events\PodcastProcessed;
use Illuminate\Support\Facades\Event;

/**
 * 모든 애플리케이션 서비스를 부트스트랩합니다.
 */
public function boot(): void
{
    Event::listen(function (PodcastProcessed $event) {
        // ...
    });
}
```

<a name="queuable-anonymous-event-listeners"></a>
#### 큐잉되는 익명(클로저) 이벤트 리스너

클로저로 이벤트 리스너를 등록할 때, `Illuminate\Events\queueable` 함수를 사용하여 Laravel이 이 리스너를 [큐](/docs/{{version}}/queues)로 실행하도록 지정할 수 있습니다:

```php
use App\Events\PodcastProcessed;
use function Illuminate\Events\queueable;
use Illuminate\Support\Facades/Event;

/**
 * 모든 애플리케이션 서비스를 부트스트랩합니다.
 */
public function boot(): void
{
    Event::listen(queueable(function (PodcastProcessed $event) {
        // ...
    }));
}
```

큐잉된 작업처럼 `onConnection`, `onQueue`, `delay` 메서드를 사용해 큐 리스너의 실행 방식을 커스터마이즈할 수 있습니다:

```php
Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->onConnection('redis')->onQueue('podcasts')->delay(now()->addSeconds(10)));
```

익명 큐 리스너에서 실패 처리를 하고 싶다면 `queueable` 정의 시 `catch` 메서드에 클로저를 전달할 수 있습니다. 이때 이벤트 인스턴스와 실패 원인인 `Throwable` 인스턴스를 인자로 받습니다:

```php
use App\Events\PodcastProcessed;
use function Illuminate\Events\queueable;
use Illuminate\Support\Facades\Event;
use Throwable;

Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->catch(function (PodcastProcessed $event, Throwable $e) {
    // 큐 리스너 실패...
}));
```

<a name="wildcard-event-listeners"></a>
#### 와일드카드 이벤트 리스너

`*` 와일드카드 문자로 여러 이벤트를 한 리스너에 등록할 수도 있습니다. 와일드카드 리스너는 첫 번째 인자로 이벤트 이름, 두 번째 인자로 전체 이벤트 데이터 배열을 받습니다:

```php
Event::listen('event.*', function (string $eventName, array $data) {
    // ...
});
```

<a name="defining-events"></a>
## 이벤트 정의하기

이벤트 클래스는 이벤트와 관련된 정보를 저장하는 데이터 컨테이너 역할을 합니다. 예를 들어, `App\Events\OrderShipped` 이벤트가 [Eloquent ORM](/docs/{{version}}/eloquent) 오브젝트를 받을 수 있습니다:

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
     * 새로운 이벤트 인스턴스를 생성합니다.
     */
    public function __construct(
        public Order $order,
    ) {}
}
```

이벤트 클래스는 별도의 로직 없이, 구매된 `App\Models\Order` 인스턴스만 담는 컨테이너입니다. `SerializesModels` 트레이트로 인해, 해당 이벤트 오브젝트가 PHP의 `serialize`로 직렬화될 때 Eloquent 모델도 적절히 직렬화됩니다(예: [큐 리스너](#queued-event-listeners)에서 사용될 때).

<a name="defining-listeners"></a>
## 리스너 정의하기

다음으로, 예제 이벤트의 리스너를 살펴보겠습니다. 이벤트 리스너 클래스는 `handle` 메서드에서 이벤트 인스턴스를 받습니다. `make:listener` 명령어를 `--event` 옵션과 함께 사용하면, 올바른 이벤트 클래스를 자동으로 import 하고 `handle`에서 타입힌트됩니다. `handle`에서 이벤트에 대응하는 어떤 동작도 수행할 수 있습니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;

class SendShipmentNotification
{
    /**
     * 이벤트 리스너를 생성합니다.
     */
    public function __construct() {}

    /**
     * 이벤트를 처리합니다.
     */
    public function handle(OrderShipped $event): void
    {
        // $event->order를 통해 주문 접근...
    }
}
```

> [!NOTE]
> 이벤트 리스너의 생성자에서도 의존성 타입힌트가 가능합니다. 모든 이벤트 리스너는 Laravel [서비스 컨테이너](/docs/{{version}}/container)를 통해 해석되므로, 의존성이 자동으로 주입됩니다.

<a name="stopping-the-propagation-of-an-event"></a>
#### 이벤트 전파 중단하기

가끔은 이벤트가 다른 리스너로 전파되지 않도록 하고 싶을 수 있습니다. 리스너의 `handle` 메서드에서 `false`를 반환하면 이벤트 전파가 중단됩니다.

<a name="queued-event-listeners"></a>
## 큐잉되는 이벤트 리스너

리스너가 이메일 전송, HTTP 요청 등 느린 작업을 수행한다면 큐잉하는 것이 좋습니다. 큐 리스너를 사용하기 전에는 [큐 설정](/docs/{{version}}/queues)을 완료하고 서버나 로컬에서 큐 워커를 실행해야 합니다.

리스너를 큐잉 대상으로 지정하려면 `ShouldQueue` 인터페이스를 리스너 클래스에 추가하세요. `make:listener` 명령어로 생성한 리스너에는 이미 이 인터페이스를 사용할 수 있도록 import 되어 있습니다:

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

이제 이 리스너가 처리하는 이벤트가 디스패치될 때, Laravel의 [큐 시스템](/docs/{{version}}/queues)으로 자동 큐잉됩니다. 실행 중 예외가 발생하지 않으면, 큐에서 작업이 끝난 후 자동으로 삭제됩니다.

<a name="customizing-the-queue-connection-queue-name"></a>
#### 큐 커넥션, 이름, 딜레이 커스터마이징

리스너가 사용할 큐 커넥션, 큐 이름, 지연(delay) 시간을 `$connection`, `$queue`, `$delay` 속성으로 지정할 수 있습니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    /**
     * job이 전송될 커넥션명
     *
     * @var string|null
     */
    public $connection = 'sqs';

    /**
     * job이 전송될 큐 이름
     *
     * @var string|null
     */
    public $queue = 'listeners';

    /**
     * job이 실행되기까지의 지연 시간(초)
     *
     * @var int
     */
    public $delay = 60;
}
```

런타임에 커넥션, 큐명, 지연 시간을 동적으로 지정하려면 `viaConnection`, `viaQueue`, `withDelay` 메서드를 정의할 수 있습니다:

```php
/**
 * 리스너의 큐 커넥션 명을 반환합니다.
 */
public function viaConnection(): string
{
    return 'sqs';
}

/**
 * 리스너가 사용할 큐 이름을 반환합니다.
 */
public function viaQueue(): string
{
    return 'listeners';
}

/**
 * 작업 실행까지 대기할 시간(초)
 */
public function withDelay(OrderShipped $event): int
{
    return $event->highPriority ? 0 : 60;
}
```

<a name="conditionally-queueing-listeners"></a>
#### 리스너 큐잉 여부 조건 지정

런타임 정보에 따라 리스너를 큐잉할지 결정해야 할 때, `shouldQueue` 메서드를 정의하면 됩니다. 이 메서드가 false를 반환하면 큐잉되지 않습니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderCreated;
use Illuminate\Contracts\Queue\ShouldQueue;

class RewardGiftCard implements ShouldQueue
{
    /**
     * 고객에게 기프트카드 제공
     */
    public function handle(OrderCreated $event): void
    {
        // ...
    }

    /**
     * 리스너 큐잉 여부 결정
     */
    public function shouldQueue(OrderCreated $event): bool
    {
        return $event->order->subtotal >= 5000;
    }
}
```

<a name="manually-interacting-with-the-queue"></a>
### 큐 직접 다루기

리스너에서 underlying 큐 잡의 `delete`와 `release` 메서드를 수동으로 사용하려면 `Illuminate\Queue\InteractsWithQueue` 트레이트를 사용할 수 있습니다. 이 트레이트는 기본적으로 생성된 리스너에 포함되어 있습니다:

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
     * 이벤트를 처리합니다.
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

큐잉된 리스너가 데이터베이스 트랜잭션 내에서 디스패치되면, 트랜잭션이 커밋되기 전에 큐에서 작업이 처리될 수 있습니다. 이 경우 트랜잭션 중 변경/생성한 모델이나 레코드는 아직 데이터베이스에 반영되지 않았을 수 있습니다. 리스너가 이 모델에 의존하면 예상치 못한 에러가 발생할 수 있습니다.

만약 큐 커넥션의 `after_commit` 설정이 false인 경우라도, 리스너 클래스에 `ShouldQueueAfterCommit` 인터페이스를 구현하면 트랜잭션이 모두 커밋된 후에만 큐잉됩니다:

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
> 이 문제의 우회 해결 방법은 [큐 작업과 DB 트랜잭션](/docs/{{version}}/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="handling-failed-jobs"></a>
### 실패한 작업 처리하기

큐잉된 이벤트 리스너가 실패하는 경우, 큐 워커가 지정한 최대 시도 횟수를 초과하면 리스너의 `failed` 메서드가 호출됩니다. 이 메서드는 이벤트 인스턴스와 `Throwable`을 인자로 받습니다:

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
#### 큐잉된 리스너의 최대 시도 횟수 지정

큐 리스너에서 오류가 발생할 경우, 무한 반복 재시도는 원치 않을 수 있습니다. Laravel에서는 시도 횟수나 시간 제한을 다양한 방법으로 지정할 수 있습니다.

리스너 클래스에 `$tries` 속성을 정의해, 지정 횟수 만큼만 시도되도록 할 수 있습니다:

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
     * 큐 리스너의 최대 시도 횟수
     *
     * @var int
     */
    public $tries = 5;
}
```

시도 횟수 대신, 리스너가 더 이상 시도되지 않아야 할 시점을 시간으로 지정할 수도 있습니다. 이 경우 `retryUntil` 메서드를 추가하고, 반환값으로 `DateTime` 인스턴스를 반환하세요:

```php
use DateTime;

/**
 * 리스너의 타임아웃 시각 지정
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(5);
}
```

<a name="specifying-queued-listener-backoff"></a>
#### 큐잉된 리스너의 백오프 지정

예외 발생 후 재시도까지 대기할 시간을 지정하려면, 리스너 클래스에 `backoff` 속성을 정의하세요:

```php
/**
 * 재시도 전 대기할 초(seconds)
 *
 * @var int
 */
public $backoff = 3;
```

더 복잡한 백오프 로직이 필요하다면 `backoff` 메서드를 정의할 수 있습니다:

```php
/**
 * 재시도 전 대기할 시간을 계산
 */
public function backoff(): int
{
    return 3;
}
```

"지수 백오프"처럼 여러 재시도에 따라 다른 대기 시간을 배열로 반환할 수도 있습니다. 아래 예에서 1번째 재시도는 1초, 2번째는 5초, 3번째부터는 10초입니다:

```php
/**
 * 큐잉된 리스너의 재시도 대기 시간 계산
 *
 * @return array<int, int>
 */
public function backoff(): array
{
    return [1, 5, 10];
}
```

<a name="dispatching-events"></a>
## 이벤트 디스패치(발생)하기

이벤트를 발생시키려면 해당 이벤트에서 static `dispatch` 메서드를 호출하면 됩니다. 이 메서드는 `Illuminate\Foundation\Events\Dispatchable` 트레이트가 제공하며, 전달된 인수들은 이벤트 생성자인자로 넘겨집니다:

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
     * 주어진 주문 발송 처리
     */
    public function store(Request $request): RedirectResponse
    {
        $order = Order::findOrFail($request->order_id);

        // 주문 발송 로직...

        OrderShipped::dispatch($order);

        return redirect('/orders');
    }
}
```

조건에 따라 이벤트를 발생시키고 싶다면 `dispatchIf`, `dispatchUnless`를 사용할 수 있습니다:

```php
OrderShipped::dispatchIf($condition, $order);

OrderShipped::dispatchUnless($condition, $order);
```

> [!NOTE]
> 테스트 시, 실제 리스너를 실행하지 않고 이벤트 발생만을 검증하고 싶다면 Laravel의 [테스트 헬퍼](#testing)를 활용하면 매우 쉽습니다.

<a name="dispatching-events-after-database-transactions"></a>
### 데이터베이스 트랜잭션 커밋 후 이벤트 디스패치하기

가끔은 활성화된 데이터베이스 트랜잭션이 커밋된 후에만 이벤트가 발생하도록 하고 싶을 수 있습니다. 이럴 때 이벤트 클래스에 `ShouldDispatchAfterCommit` 인터페이스를 구현하세요. 해당 트랜잭션이 롤백되면 이벤트도 버려집니다. 만약 트랜잭션이 진행 중이 아니면, 즉시 이벤트가 발생됩니다:

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
     * 새로운 이벤트 생성자
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

이벤트 구독자는 여러 이벤트를 클래스 내부에서 직접 구독할 수 있으며, 하나의 클래스에 여러 이벤트 핸들러를 정의할 수 있습니다. 구독자 클래스는 반드시 `subscribe` 메서드를 정의해야 하며, 해당 메서드는 이벤트 디스패처 인스턴스를 받습니다. 디스패처의 `listen` 메서드로 이벤트 리스너를 등록할 수 있습니다:

```php
<?php

namespace App\Listeners;

use Illuminate\Auth\Events\Login;
use Illuminate\Auth\Events\Logout;
use Illuminate\Events\Dispatcher;

class UserEventSubscriber
{
    /**
     * 로그인 이벤트 처리
     */
    public function handleUserLogin(Login $event): void {}

    /**
     * 로그아웃 이벤트 처리
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

구독자 클래스 내부에 이벤트 리스너 메서드가 있다면, `subscribe` 메서드에서 이벤트와 메서드명을 배열로 반환하는 것이 간편합니다. Laravel은 이벤트 등록 시 구독자 클래스명을 자동으로 처리합니다:

```php
<?php

namespace App\Listeners;

use Illuminate\Auth\Events\Login;
use Illuminate\Auth\Events\Logout;
use Illuminate\Events\Dispatcher;

class UserEventSubscriber
{
    /**
     * 로그인 이벤트 처리
     */
    public function handleUserLogin(Login $event): void {}

    /**
     * 로그아웃 이벤트 처리
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
### 이벤트 구독자 등록하기

구독자를 작성한 후, 구독자의 핸들러 메서드가 Laravel의 [이벤트 자동 탐지 규칙](#event-discovery)을 따른다면 자동으로 등록됩니다. 아니라면, `Event` 파사드의 `subscribe` 메서드를 사용해 수동 등록해야 합니다. 일반적으로 이 코드는 `AppServiceProvider`의 `boot` 메서드에 위치합니다:

```php
<?php

namespace App\Providers;

use App\Listeners\UserEventSubscriber;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 모든 애플리케이션 서비스를 부트스트랩합니다.
     */
    public function boot(): void
    {
        Event::subscribe(UserEventSubscriber::class);
    }
}
```

<a name="testing"></a>
## 테스트

이벤트를 디스패치하는 코드를 테스트할 때, 리스너가 실제로 실행되지 않도록 하려면 Laravel의 테스트 헬퍼를 사용할 수 있습니다. 이렇게 하면 리스너 로직은 별도로, 이벤트 자체의 디스패치만 검증할 수 있습니다. 리스너 자체를 테스트하고 싶다면 인스턴스화 후 handle 메서드를 직접 호출하면 됩니다.

`Event` 파사드의 `fake` 메서드를 사용해 리스너 실행을 중단시키고, 테스트 코드를 실행한 뒤 `assertDispatched`, `assertNotDispatched`, `assertNothingDispatched`로 어떤 이벤트가 발생했는지 검증할 수 있습니다:

```php tab=Pest
<?php

use App\Events\OrderFailedToShip;
use App\Events\OrderShipped;
use Illuminate\Support\Facades\Event;

test('orders can be shipped', function () {
    Event::fake();

    // 주문 발송 처리...

    // 이벤트가 발생했는지 검증…
    Event::assertDispatched(OrderShipped::class);

    // 2번 발생했는지…
    Event::assertDispatched(OrderShipped::class, 2);

    // 발생하지 않았는지…
    Event::assertNotDispatched(OrderFailedToShip::class);

    // 아무 이벤트도 발생하지 않았는지…
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
     * 주문 발송 테스트
     */
    public function test_orders_can_be_shipped(): void
    {
        Event::fake();

        // 주문 발송 처리...

        // 이벤트 발생 검증
        Event::assertDispatched(OrderShipped::class);

        // 2회 발생 검증
        Event::assertDispatched(OrderShipped::class, 2);

        // 미발생 검증
        Event::assertNotDispatched(OrderFailedToShip::class);

        // 아무 이벤트도 발생하지 않았는지
        Event::assertNothingDispatched();
    }
}
```

`assertDispatched`나 `assertNotDispatched`에는 클로저를 전달해 원하는 "진실성 테스트"를 통과하는 이벤트가 발생/미발생했는지 확인할 수도 있습니다. 최소 하나의 이벤트라도 이 조건을 통과하면 assertion이 성공합니다:

```php
Event::assertDispatched(function (OrderShipped $event) use ($order) {
    return $event->order->id === $order->id;
});
```

특정 이벤트에 리스너가 등록되어있는지만 검증하고 싶으면, `assertListening`을 사용할 수 있습니다:

```php
Event::assertListening(
    OrderShipped::class,
    SendShipmentNotification::class
);
```

> [!WARNING]
> `Event::fake()`를 호출하면 모든 이벤트 리스너가 실행되지 않습니다. 만약 모델 팩토리에서, 예를 들어 `creating`이벤트에서 UUID를 만드는 등 이벤트에 의존하면 팩토리 사용 **후**에 `Event::fake()`를 호출해야 합니다.

<a name="faking-a-subset-of-events"></a>
### 일부 이벤트만 Fake 처리

특정 이벤트들에 대해서만 리스너를 fake 하고 싶으면, `fake` 혹은 `fakeFor`에 해당 이벤트 클래스 목록을 전달하면 됩니다:

```php tab=Pest
test('orders can be processed', function () {
    Event::fake([
        OrderCreated::class,
    ]);

    $order = Order::factory()->create();

    Event::assertDispatched(OrderCreated::class);

    // 다른 이벤트는 정상적으로 디스패치됨
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

    // 다른 이벤트는 정상적으로 디스패치됨
    $order->update([...]);
}
```

특정 이벤트를 제외한 나머지 전체 이벤트를 fake 하려면 `except`를 사용하세요:

```php
Event::fake()->except([
    OrderCreated::class,
]);
```

<a name="scoped-event-fakes"></a>
### 범위 지정 이벤트 Fake

테스트 실행 중 일부 구간에서만 리스너 fake 처리를 하고 싶다면, `fakeFor`를 사용할 수 있습니다:

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

    // 이후엔 이벤트가 정상적으로 디스패치되고 옵저버도 실행됨
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

        // 이후엔 이벤트가 정상적으로 디스패치되고 옵저버도 실행됨
        $order->update([...]);
    }
}
```
