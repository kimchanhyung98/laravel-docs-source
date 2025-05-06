# 이벤트

- [소개](#introduction)
- [이벤트와 리스너 생성하기](#generating-events-and-listeners)
- [이벤트와 리스너 등록하기](#registering-events-and-listeners)
    - [이벤트 자동 탐지](#event-discovery)
    - [이벤트 수동 등록](#manually-registering-events)
    - [클로저 리스너](#closure-listeners)
- [이벤트 정의하기](#defining-events)
- [리스너 정의하기](#defining-listeners)
- [큐에 등록되는 이벤트 리스너](#queued-event-listeners)
    - [큐 직접 다루기](#manually-interacting-with-the-queue)
    - [큐 리스너와 데이터베이스 트랜잭션](#queued-event-listeners-and-database-transactions)
    - [실패한 작업 처리하기](#handling-failed-jobs)
- [이벤트 디스패치하기](#dispatching-events)
    - [데이터베이스 트랜잭션 이후 이벤트 디스패치](#dispatching-events-after-database-transactions)
- [이벤트 구독자](#event-subscribers)
    - [이벤트 구독자 작성하기](#writing-event-subscribers)
    - [이벤트 구독자 등록하기](#registering-event-subscribers)
- [테스트](#testing)
    - [특정 이벤트만 페이크하기](#faking-a-subset-of-events)
    - [스코프 이벤트 페이크](#scoped-event-fakes)

<a name="introduction"></a>
## 소개

Laravel의 이벤트는 간단한 옵저버 패턴(Observer Pattern) 구현을 제공하여, 애플리케이션 내에서 발생하는 다양한 이벤트를 구독하고 청취할 수 있습니다. 이벤트 클래스는 일반적으로 `app/Events` 디렉토리에, 해당 리스너는 `app/Listeners` 디렉토리에 보관됩니다. 애플리케이션에서 이 디렉토리를 아직 보지 못했다면 걱정하지 마세요. Artisan 콘솔 명령어로 이벤트와 리스너를 생성하면 자동으로 생성됩니다.

이벤트는 애플리케이션의 다양한 부분을 느슨하게 결합하는데 좋은 방법입니다. 하나의 이벤트에 여러 개의 리스너가 연결될 수 있으며, 이들은 서로에게 의존하지 않습니다. 예를 들어, 주문이 배송될 때마다 사용자의 Slack에 알림을 보내고 싶다고 가정하면, 주문 처리 코드에 Slack 알림 코드를 직접 결합하는 대신, `App\Events\OrderShipped` 이벤트를 발생시켜 해당 리스너가 Slack 알림을 처리하도록 할 수 있습니다.

<a name="generating-events-and-listeners"></a>
## 이벤트와 리스너 생성하기

이벤트와 리스너를 빠르게 생성하려면, `make:event` 및 `make:listener` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan make:event PodcastProcessed

php artisan make:listener SendPodcastNotification --event=PodcastProcessed
```

편의를 위해, 별도의 인수 없이 `make:event` 및 `make:listener` 명령어를 실행할 수도 있습니다. 이 경우, Laravel이 클래스명과 리스너를 만들 때 어떤 이벤트를 청취할 것인지를 물어봅니다.

```shell
php artisan make:event

php artisan make:listener
```

<a name="registering-events-and-listeners"></a>
## 이벤트와 리스너 등록하기

<a name="event-discovery"></a>
### 이벤트 자동 탐지

기본적으로, Laravel은 애플리케이션의 `Listeners` 디렉토리를 스캔하여 이벤트 리스너를 자동으로 찾아 등록합니다. `handle` 또는 `__invoke`로 시작하는 리스너 클래스 메서드를 발견하면, 해당 메서드의 시그니처에 타입힌트된 이벤트에 대한 리스너로 자동 등록합니다.

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

PHP의 유니언 타입을 사용해 여러 이벤트를 청취할 수도 있습니다.

```php
/**
 * Handle the given event.
 */
public function handle(PodcastProcessed|PodcastPublished $event): void
{
    // ...
}
```

리스너를 다른 디렉토리나 여러 디렉토리에 저장하고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에서 `withEvents` 메서드를 사용해 해당 디렉토리를 스캔하도록 지시할 수 있습니다.

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/Orders/Listeners',
])
```

`*` 와일드카드를 사용해 여러 비슷한 디렉토리를 스캔할 수도 있습니다.

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/*/Listeners',
])
```

애플리케이션에 등록된 모든 리스너를 나열하려면, `event:list` 명령어를 사용할 수 있습니다.

```shell
php artisan event:list
```

<a name="event-discovery-in-production"></a>
#### 운영 환경에서의 이벤트 자동 탐지

애플리케이션의 성능을 높이려면, `optimize` 또는 `event:cache` Artisan 명령어로 모든 리스너 목록을 캐싱해야 합니다. 보통 이 명령어는 [배포 과정](/docs/{{version}}/deployment#optimization)의 일부로 실행되어야 합니다. 생성된 매니페스트는 이벤트 등록 속도를 증가시키며, `event:clear` 명령어로 캐시를 삭제할 수 있습니다.

<a name="manually-registering-events"></a>
### 이벤트 수동 등록

`Event` 파사드를 사용해, 애플리케이션의 `AppServiceProvider`의 `boot` 메서드 내에서 이벤트와 해당 리스너를 수동으로 등록할 수 있습니다.

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

`event:list` 명령어를 통해 현재 애플리케이션에 등록된 모든 리스너를 나열할 수 있습니다.

```shell
php artisan event:list
```

<a name="closure-listeners"></a>
### 클로저 리스너

일반적으로 리스너는 클래스로 정의되지만, `AppServiceProvider`의 `boot` 메서드에서 클로저(익명 함수)로도 등록할 수 있습니다.

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
#### 큐가 가능한 익명 이벤트 리스너

클로저 기반의 리스너를 등록할 때, `Illuminate\Events\queueable` 함수를 사용해 해당 리스너를 [큐](/docs/{{version}}/queues)로 실행하도록 할 수 있습니다.

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

큐에 등록된 작업과 마찬가지로, `onConnection`, `onQueue`, `delay` 메서드를 사용해 큐 리스너의 실행 환경을 세부적으로 조정할 수 있습니다.

```php
Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->onConnection('redis')->onQueue('podcasts')->delay(now()->addSeconds(10)));
```

익명 큐 리스너의 실패를 처리하려면, `queueable` 리스너를 정의할 때 `catch` 메서드에 클로저를 전달할 수 있습니다. 이 클로저는 이벤트 인스턴스와 실패를 발생시킨 `Throwable` 인스턴스를 받습니다.

```php
use App\Events\PodcastProcessed;
use function Illuminate\Events\queueable;
use Illuminate\Support\Facades\Event;
use Throwable;

Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->catch(function (PodcastProcessed $event, Throwable $e) {
    // 큐 리스너가 실패했을 때...
}));
```

<a name="wildcard-event-listeners"></a>
#### 와일드카드 이벤트 리스너

`*` 와일드카드 파라미터를 사용해 여러 이벤트를 동시에 잡아낼 수 있습니다. 와일드카드 리스너는 첫 번째 인수로 이벤트 이름, 두 번째 인수로 전체 이벤트 데이터 배열을 받습니다.

```php
Event::listen('event.*', function (string $eventName, array $data) {
    // ...
});
```

<a name="defining-events"></a>
## 이벤트 정의하기

이벤트 클래스는 기본적으로 해당 이벤트와 관련된 데이터를 담는 컨테이너입니다. 예를 들어, `App\Events\OrderShipped` 이벤트가 [Eloquent ORM](/docs/{{version}}/eloquent) 객체를 받을 수 있습니다.

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

보시다시피, 이 이벤트 클래스에는 로직이 없으며 구매된 `App\Models\Order` 인스턴스를 담는 컨테이너 역할만 합니다. 이벤트에서 사용하는 `SerializesModels` 트레이트는 [큐 리스너](#queued-event-listeners)에서처럼, PHP의 `serialize` 함수로 직렬화할 때 Eloquent 모델을 안전하게 직렬화해줍니다.

<a name="defining-listeners"></a>
## 리스너 정의하기

이제 예제 이벤트에 대한 리스너를 살펴보겠습니다. 이벤트 리스너는 이벤트 인스턴스를 `handle` 메서드에서 받습니다. `make:listener` Artisan 명령어를 `--event` 옵션과 함께 호출하면, 해당 이벤트 클래스를 자동으로 임포트하고 타입힌트도 추가해줍니다. `handle` 메서드 내부에서 이벤트에 응답하는 데 필요한 모든 작업을 수행할 수 있습니다.

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
        // $event->order를 이용해 주문에 접근 ...
    }
}
```

> [!NOTE]
> 이벤트 리스너는 생성자에서 필요한 의존성을 타입힌트로 받을 수도 있습니다. 모든 이벤트 리스너는 Laravel [서비스 컨테이너](/docs/{{version}}/container)를 통해 해석되므로, 의존성이 자동으로 주입됩니다.

<a name="stopping-the-propagation-of-an-event"></a>
#### 이벤트 전파 중지하기

가끔은 이벤트가 다른 리스너로 전달되지 않도록 중간에 전파를 멈추고 싶을 수 있습니다. 이 경우, 리스너의 `handle` 메서드에서 `false`를 반환하면 됩니다.

<a name="queued-event-listeners"></a>
## 큐에 등록되는 이벤트 리스너

리스너가 메일 발송이나 HTTP 요청 등 시간이 오래 걸리는 작업을 수행하는 경우, 큐로 처리하는 것이 유용합니다. 큐 리스너를 사용하려면 먼저 [큐 설정](/docs/{{version}}/queues)을 완료하고, 서버나 로컬 개발환경에서 큐 워커를 실행해야 합니다.

리스너를 큐로 실행하려면, 리스너 클래스에 `ShouldQueue` 인터페이스를 구현해야 합니다. `make:listener` Artisan 명령어로 생성된 리스너에는 이미 이 인터페이스가 네임스페이스에 임포트되어 있습니다.

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

이제 이 리스너가 처리하는 이벤트가 발생하면, 이벤트 디스패처가 Laravel [큐 시스템](/docs/{{version}}/queues)을 통해 자동으로 큐에 등록합니다. 리스너 실행 중 예외가 발생하지 않으면, 큐 작업은 정상적으로 삭제됩니다.

<a name="customizing-the-queue-connection-queue-name"></a>
#### 큐 연결, 이름, 지연 시간 커스터마이징

이벤트 리스너가 사용할 큐 연결명, 큐 이름, 지연 시간을 지정하려면, 리스너 클래스에 `$connection`, `$queue`, `$delay` 속성을 정의할 수 있습니다.

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    /**
     * 연결명
     *
     * @var string|null
     */
    public $connection = 'sqs';

    /**
     * 큐 이름
     *
     * @var string|null
     */
    public $queue = 'listeners';

    /**
     * 작업 처리 전 대기 시간(초)
     *
     * @var int
     */
    public $delay = 60;
}
```

실행 시간에 리스너의 큐 연결명, 큐 이름, 지연 시간을 지정하려면, `viaConnection`, `viaQueue`, `withDelay` 메서드를 정의하면 됩니다.

```php
/**
 * 리스너의 큐 연결명 반환
 */
public function viaConnection(): string
{
    return 'sqs';
}

/**
 * 리스너의 큐 이름 반환
 */
public function viaQueue(): string
{
    return 'listeners';
}

/**
 * 작업 처리 전 대기 시간(초) 반환
 */
public function withDelay(OrderShipped $event): int
{
    return $event->highPriority ? 0 : 60;
}
```

<a name="conditionally-queueing-listeners"></a>
#### 리스너 큐 여부 조건부 지정

실행 시간에 따라 리스너를 큐에 등록할지 말지 결정해야 하는 경우, `shouldQueue` 메서드를 추가할 수 있습니다. `shouldQueue`가 `false`를 반환하면 리스너는 큐에 등록되지 않습니다.

```php
<?php

namespace App\Listeners;

use App\Events\OrderCreated;
use Illuminate\Contracts\Queue\ShouldQueue;

class RewardGiftCard implements ShouldQueue
{
    /**
     * 고객에게 기프트카드 보상
     */
    public function handle(OrderCreated $event): void
    {
        // ...
    }

    /**
     * 리스너를 큐에 추가할지 결정
     */
    public function shouldQueue(OrderCreated $event): bool
    {
        return $event->order->subtotal >= 5000;
    }
}
```

<a name="manually-interacting-with-the-queue"></a>
### 큐 직접 다루기

리스너가 큐 작업의 `delete` 또는 `release` 메서드에 직접 접근해야 한다면, `Illuminate\Queue\InteractsWithQueue` 트레이트를 사용할 수 있습니다. 이 트레이트는 기본적으로 생성된 리스너에 포함되며, 해당 메서드에 접근할 수 있습니다.

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
### 큐 리스너와 데이터베이스 트랜잭션

큐 리스너가 데이터베이스 트랜잭션 내에서 디스패치될 경우, 트랜잭션이 커밋되기 전에 큐가 처리될 수 있습니다. 이런 경우, 트랜잭션 중에 업데이트된 모델이나 레코드가 데이터베이스에 아직 반영되지 않았을 수 있으며, 트랜잭션 내에서 생성된 모델이나 레코드가 존재하지 않을 수 있습니다. 이러한 모델에 리스너가 의존한다면, 큐 작업이 처리될 때 예기치 않은 오류가 발생할 수 있습니다.

큐 연결의 `after_commit` 설정이 `false`라면, 해당 리스너 클래스에 `ShouldQueueAfterCommit` 인터페이스를 구현해 열린 모든 데이터베이스 트랜잭션이 커밋된 후에 큐 작업이 실행되게 할 수 있습니다.

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
> 이러한 문제에 대한 자세한 우회 방법은 [큐 작업과 데이터베이스 트랜잭션](/docs/{{version}}/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="handling-failed-jobs"></a>
### 실패한 작업 처리하기

큐 리스너가 실패할 수도 있습니다. 큐에 등록된 리스너가 queue worker에 설정된 최대 재시도 횟수를 초과하면, 리스너의 `failed` 메서드가 호출됩니다. 이 메서드는 이벤트 인스턴스와 실패 원인이 된 `Throwable`을 전달받습니다.

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
#### 큐 리스너의 재시도 횟수 설정

큐 리스너에서 오류가 반복해서 발생하는 경우, 무한정 재시도하지 않도록 제한할 수 있습니다. 이를 위해 리스너 클래스에 `$tries` 속성을 지정해 재시도 최대 횟수를 설정할 수 있습니다.

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
     * 큐 리스너의 최대 재시도 횟수
     *
     * @var int
     */
    public $tries = 5;
}
```

최대 횟수 대신 지정된 시간까지만 재시도하도록 설정하려면, `retryUntil` 메서드를 추가하고 `DateTime` 인스턴스를 반환하면 됩니다.

```php
use DateTime;

/**
 * 리스너의 재시도 시간 제한 반환
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(5);
}
```

<a name="specifying-queued-listener-backoff"></a>
#### 큐 리스너 백오프(재시도 대기) 설정

예외 발생 시 리스너가 다시 시도하기 전 대기해야 할 초를 설정하려면, 리스너 클래스에 `backoff` 속성을 정의할 수 있습니다.

```php
/**
 * 큐 리스너 재시도 전 대기 시간(초)
 *
 * @var int
 */
public $backoff = 3;
```

더 복잡한 백오프 로직이 필요하다면, `backoff` 메서드를 정의할 수도 있습니다.

```php
/**
 * 큐 리스너 재시도 전 대기 시간(초) 반환
 */
public function backoff(): int
{
    return 3;
}
```

배열로 반환하면 "지수 백오프"도 쉽게 구현할 수 있습니다. 아래 예시에서, 첫 재시도는 1초, 두 번째는 5초, 세 번째는 10초, 그 이후로는 모두 10초씩 대기합니다.

```php
/**
 * 큐 리스너 재시도 전 대기 시간(초) 배열 반환
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

이벤트를 디스패치하려면, 이벤트 클래스의 정적 `dispatch` 메서드를 호출하면 됩니다. 이 메서드는 `Illuminate\Foundation\Events\Dispatchable` 트레이트에 의해 제공됩니다. `dispatch`에 전달한 인수는 이벤트 생성자에 전달됩니다.

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
     * 주문 배송 처리
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

특정 조건일 때만 이벤트를 디스패치하고 싶다면, `dispatchIf`와 `dispatchUnless` 메서드를 사용할 수 있습니다.

```php
OrderShipped::dispatchIf($condition, $order);

OrderShipped::dispatchUnless($condition, $order);
```

> [!NOTE]
> 테스트 시에는 리스너를 실제로 실행하지 않으면서도 이벤트가 정상적으로 디스패치되었는지 검증할 수 있습니다. Laravel의 [테스트 헬퍼](#testing)를 활용하세요.

<a name="dispatching-events-after-database-transactions"></a>
### 데이터베이스 트랜잭션 이후 이벤트 디스패치

Laravel이 현재 활성화된 데이터베이스 트랜잭션 커밋 후에만 이벤트를 디스패치하도록 하려면, 이벤트 클래스에 `ShouldDispatchAfterCommit` 인터페이스를 구현하면 됩니다.

이 인터페이스를 구현하면, 트랜잭션이 커밋될 때까지 이벤트 디스패치를 연기합니다. 트랜잭션이 실패하면 이벤트가 폐기되며, 트랜잭션 중이 아니면 즉시 디스패치됩니다.

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
### 이벤트 구독자 작성하기

이벤트 구독자는 하나의 클래스 안에서 여러 이벤트를 구독할 수 있어, 여러 이벤트 핸들러를 한 클래스에 정의할 수 있습니다. 구독자 클래스는 `subscribe` 메서드를 정의해야 하며, 이 메서드는 이벤트 디스패처 인스턴스를 인수로 받습니다. 주어진 디스패처에 `listen` 메서드를 호출해 이벤트 리스너를 등록할 수 있습니다.

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
     * 구독자의 리스너 등록
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

리스너 메서드가 구독자 내부에 정의되어 있다면, `subscribe` 메서드에서 이벤트와 메서드 쌍의 배열을 반환하는 방식이 더 편할 수 있습니다. Laravel이 자동으로 구독자 클래스명을 추론합니다.

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

구독자를 작성한 뒤, 해당 구독자가 Laravel의 [이벤트 자동 탐지 규칙](#event-discovery)을 따르면, 구독자 내의 핸들러도 자동으로 등록됩니다. 그렇지 않은 경우, `Event` 파사드의 `subscribe` 메서드를 사용해 수동으로 등록할 수 있습니다. 주로 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 이 작업을 수행합니다.

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

이벤트를 디스패치하는 코드를 테스트할 때는, 실제로 리스너가 실행되지 않도록 할 수 있습니다. 리스너의 코드는 별도로 직접 테스트할 수 있기 때문입니다. 리스너를 테스트하려면, 리스너 인스턴스를 직접 생성해 `handle` 메서드를 호출하면 됩니다.

`Event` 파사드의 `fake` 메서드를 사용하면, 리스너 실행은 차단되고 코드 실행 후 어떤 이벤트가 디스패치되었는지 `assertDispatched`, `assertNotDispatched`, `assertNothingDispatched` 메서드로 검증할 수 있습니다.

```php tab=Pest
<?php

use App\Events\OrderFailedToShip;
use App\Events\OrderShipped;
use Illuminate\Support\Facades\Event;

test('orders can be shipped', function () {
    Event::fake();

    // 주문 배송 실행 ...

    // 이벤트가 디스패치되었는지 확인
    Event::assertDispatched(OrderShipped::class);

    // 이벤트가 두 번 디스패치되었는지 확인
    Event::assertDispatched(OrderShipped::class, 2);

    // 이벤트가 디스패치되지 않았는지 확인
    Event::assertNotDispatched(OrderFailedToShip::class);

    // 아무 이벤트도 디스패치되지 않았는지 확인
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
     * 주문 배송 테스트
     */
    public function test_orders_can_be_shipped(): void
    {
        Event::fake();

        // 주문 배송 실행 ...

        // 이벤트가 디스패치되었는지 확인
        Event::assertDispatched(OrderShipped::class);

        // 이벤트가 두 번 디스패치되었는지 확인
        Event::assertDispatched(OrderShipped::class, 2);

        // 이벤트가 디스패치되지 않았는지 확인
        Event::assertNotDispatched(OrderFailedToShip::class);

        // 아무 이벤트도 디스패치되지 않았는지 확인
        Event::assertNothingDispatched();
    }
}
```

`assertDispatched` 또는 `assertNotDispatched`에 클로저를 전달하면, 특정 조건을 만족하는 이벤트가 디스패치되었는지 검사할 수 있습니다. 하나라도 조건을 통과하면 성공합니다.

```php
Event::assertDispatched(function (OrderShipped $event) use ($order) {
    return $event->order->id === $order->id;
});
```

특정 이벤트에 대해 지정된 리스너가 리스닝하고 있는지 확인하려면, `assertListening` 메서드를 사용할 수 있습니다.

```php
Event::assertListening(
    OrderShipped::class,
    SendShipmentNotification::class
);
```

> [!WARNING]
> `Event::fake()`를 호출하면, 이후에 어떤 이벤트 리스너도 실행되지 않습니다. 생성 중 이벤트에 의존하는 모델 팩토리를 사용하는 테스트라면, 팩토리 이후에 `Event::fake()`를 호출해야 합니다.

<a name="faking-a-subset-of-events"></a>
### 특정 이벤트만 페이크하기

특정 이벤트에 대해서만 리스너를 페이크(실행 차단)하려면, `fake`나 `fakeFor` 메서드에 이벤트 클래스 배열을 전달하면 됩니다.

```php tab=Pest
test('orders can be processed', function () {
    Event::fake([
        OrderCreated::class,
    ]);

    $order = Order::factory()->create();

    Event::assertDispatched(OrderCreated::class);

    // 다른 이벤트는 평소처럼 동작
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

    // 다른 이벤트는 평소처럼 동작
    $order->update([...]);
}
```

특정 이벤트를 제외한 모든 이벤트에 대해서만 페이크하려면, `except` 메서드를 사용할 수 있습니다.

```php
Event::fake()->except([
    OrderCreated::class,
]);
```

<a name="scoped-event-fakes"></a>
### 스코프 이벤트 페이크

테스트의 일부분에서만 이벤트 리스너를 페이크하고 싶다면, `fakeFor` 메서드를 사용할 수 있습니다.

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

    // 이 이후에는 이벤트와 옵저버가 정상 동작 ...
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

        // 이 이후에는 이벤트와 옵저버가 정상 동작 ...
        $order->update([...]);
    }
}
```
