# 이벤트 (Events)

- [소개](#introduction)
- [이벤트와 리스너 생성하기](#generating-events-and-listeners)
- [이벤트와 리스너 등록하기](#registering-events-and-listeners)
    - [이벤트 자동 감지(Event Discovery)](#event-discovery)
    - [이벤트 수동 등록](#manually-registering-events)
    - [클로저 리스너](#closure-listeners)
- [이벤트 정의하기](#defining-events)
- [리스너 정의하기](#defining-listeners)
- [큐잉된(Queued) 이벤트 리스너](#queued-event-listeners)
    - [큐 직접 다루기](#manually-interacting-with-the-queue)
    - [큐잉된 이벤트 리스너와 데이터베이스 트랜잭션](#queued-event-listeners-and-database-transactions)
    - [실패한 작업 처리하기](#handling-failed-jobs)
- [이벤트 디스패치(실행)하기](#dispatching-events)
    - [데이터베이스 트랜잭션 이후 이벤트 디스패치](#dispatching-events-after-database-transactions)
- [이벤트 구독자](#event-subscribers)
    - [이벤트 구독자 작성하기](#writing-event-subscribers)
    - [이벤트 구독자 등록하기](#registering-event-subscribers)
- [테스트](#testing)
    - [일부 이벤트 가짜(Fake) 처리](#faking-a-subset-of-events)
    - [스코프 기반 이벤트 가짜 처리](#scoped-event-fakes)

<a name="introduction"></a>
## 소개

라라벨의 이벤트는 간단한 옵저버 패턴을 구현하여, 애플리케이션 내에서 발생하는 다양한 이벤트를 구독하고, 청취(리스닝)할 수 있도록 지원합니다. 이벤트 클래스는 일반적으로 `app/Events` 디렉토리에, 해당 이벤트를 처리하는 리스너는 `app/Listeners` 디렉토리에 저장됩니다. 만약 여러분의 애플리케이션에 이 디렉토리가 없다면, Artisan 콘솔 명령어로 이벤트와 리스너를 생성할 때 자동으로 디렉토리가 만들어지니 걱정하지 않으셔도 됩니다.

이벤트는 애플리케이션의 여러 부분을 느슨하게 결합(decouple)하는 데에 아주 유용합니다. 하나의 이벤트에 여러 리스너가 존재할 수 있고, 이 리스너들은 서로 독립적으로 동작합니다. 예를 들어, 주문이 배송될 때마다 사용자의 슬랙(Slack)으로 알림을 보내고 싶다고 가정해봅시다. 이럴 때 주문 처리 코드와 슬랙 알림 코드를 직접 연결하는 대신, `App\Events\OrderShipped` 이벤트를 발생시키고, 리스너에서 해당 이벤트를 받아 슬랙 알림을 보낼 수 있습니다.

<a name="generating-events-and-listeners"></a>
## 이벤트와 리스너 생성하기

이벤트와 리스너를 빠르게 생성하려면, `make:event` 와 `make:listener` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan make:event PodcastProcessed

php artisan make:listener SendPodcastNotification --event=PodcastProcessed
```

더 편리하게, 추가적인 인수 없이 `make:event` 와 `make:listener` 명령어를 실행할 수도 있습니다. 이 경우, 라라벨이 클래스명을 직접 입력받아 생성하며, 리스너 생성 시 어떤 이벤트를 청취할지 물어봅니다.

```shell
php artisan make:event

php artisan make:listener
```

<a name="registering-events-and-listeners"></a>
## 이벤트와 리스너 등록하기

<a name="event-discovery"></a>
### 이벤트 자동 감지(Event Discovery)

라라벨은 기본적으로 애플리케이션의 `Listeners` 디렉토리를 스캔하여 이벤트 리스너를 자동으로 찾아 등록합니다. 라라벨이 리스너 클래스에서 `handle` 또는 `__invoke`로 시작하는 메서드를 찾으면, 그 메서드 시그니처에 타입힌트되어 있는 이벤트를 대상으로 해당 메서드를 이벤트 리스너로 등록합니다.

```php
use App\Events\PodcastProcessed;

class SendPodcastNotification
{
    /**
     * Handle the event.
     */
    public function handle(PodcastProcessed $event): void
    {
        // ...
    }
}
```

PHP의 유니언 타입(union types)을 이용해 여러 이벤트를 한 번에 청취할 수도 있습니다.

```php
/**
 * Handle the event.
 */
public function handle(PodcastProcessed|PodcastPublished $event): void
{
    // ...
}
```

리스너를 다른 디렉토리 또는 여러 디렉토리에 저장하려는 경우, 애플리케이션의 `bootstrap/app.php` 파일에서 `withEvents` 메서드를 이용해 라라벨이 추가로 디렉토리를 스캔하도록 할 수 있습니다.

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/Orders/Listeners',
])
```

`*` 와일드카드를 사용해 여러 유사한 경로를 한 번에 스캔할 수도 있습니다.

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/*/Listeners',
])
```

`event:list` 명령어를 사용하면 현재 애플리케이션에 등록된 모든 리스너 목록을 확인할 수 있습니다.

```shell
php artisan event:list
```

<a name="event-discovery-in-production"></a>
#### 운영 환경(Production)에서의 이벤트 자동 감지

애플리케이션의 성능 향상을 위해, `optimize` 또는 `event:cache` Artisan 명령어로 모든 리스너 목록을 캐싱하길 권장합니다. 이 명령어는 주로 애플리케이션 [배포 과정](/docs/12.x/deployment#optimization)에서 실행해야 합니다. 프레임워크는 이 캐시된 매니페스트 파일을 사용하여 이벤트 등록 과정을 좀 더 빠르게 처리합니다. 이벤트 캐시를 삭제하려면 `event:clear` 명령어를 사용합니다.

<a name="manually-registering-events"></a>
### 이벤트 수동 등록

`Event` 파사드를 사용해, `AppServiceProvider`의 `boot` 메서드 안에서 직접 이벤트 및 대응하는 리스너를 수동으로 등록할 수 있습니다.

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

`event:list` 명령어를 사용하여 현재 등록된 리스너를 확인할 수 있는 점은 위와 동일합니다.

```shell
php artisan event:list
```

<a name="closure-listeners"></a>
### 클로저 리스너

일반적으로 리스너는 클래스 형태로 정의되지만, `AppServiceProvider`의 `boot` 메서드 안에서 클로저 형태의 이벤트 리스너도 직접 등록할 수 있습니다.

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
#### 큐잉 가능한 익명(Anonymous) 이벤트 리스너

클로저 기반 이벤트 리스너를 등록할 때, 클로저를 `Illuminate\Events\queueable` 함수로 감싸주면 해당 리스너가 [큐](/docs/12.x/queues)를 통해 실행되도록 라라벨에 지시할 수 있습니다.

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

큐에 들어간 작업과 마찬가지로 `onConnection`, `onQueue`, `delay` 메서드를 사용해 큐잉된 리스너의 실행 환경을 커스터마이즈할 수 있습니다.

```php
Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->onConnection('redis')->onQueue('podcasts')->delay(now()->addSeconds(10)));
```

익명 큐 리스너가 실패했을 때를 처리하려면, `queueable` 리스너를 정의할 때 `catch` 메서드에 클로저를 전달하면 됩니다. 이 클로저는 이벤트 인스턴스와 리스너가 실패한 원인인 `Throwable` 인스턴스를 받습니다.

```php
use App\Events\PodcastProcessed;
use function Illuminate\Events\queueable;
use Illuminate\Support\Facades\Event;
use Throwable;

Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->catch(function (PodcastProcessed $event, Throwable $e) {
    // 큐잉된 리스너가 실패했습니다...
}));
```

<a name="wildcard-event-listeners"></a>
#### 와일드카드 이벤트 리스너

이벤트 이름에서 `*` 와일드카드 문자를 이용해 여러 이벤트를 같은 리스너에서 받아 처리할 수도 있습니다. 와일드카드 리스너는 첫 번째 인자로 이벤트 이름, 두 번째 인자로 전체 이벤트 데이터 배열을 전달받습니다.

```php
Event::listen('event.*', function (string $eventName, array $data) {
    // ...
});
```

<a name="defining-events"></a>
## 이벤트 정의하기

이벤트 클래스는 해당 이벤트와 관련된 정보를 담는 데이터 컨테이너의 역할을 합니다. 예를 들어, `App\Events\OrderShipped` 이벤트가 [Eloquent ORM](/docs/12.x/eloquent) 객체를 전달받는 경우를 생각해봅니다.

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

보시다시피, 이 이벤트 클래스에는 별도의 로직이 없습니다. 단지 구매된 `App\Models\Order` 인스턴스를 담는 컨테이너입니다. 이벤트에 사용하는 `SerializesModels` 트레이트는, 이벤트 객체가 PHP의 `serialize` 함수로 직렬화될 때(예: [큐잉된 리스너](#queued-event-listeners) 활용 시) Eloquent 모델을 안전하게 직렬화/역직렬화할 수 있게 해줍니다.

<a name="defining-listeners"></a>
## 리스너 정의하기

이제 샘플 이벤트의 리스너를 살펴보겠습니다. 이벤트 리스너는 `handle` 메서드에서 이벤트 인스턴스를 전달받습니다. `make:listener` Artisan 명령어를 `--event` 옵션과 함께 실행하면, 해당 이벤트 클래스를 자동으로 임포트하고 `handle` 메서드의 타입힌트도 만들어 줍니다. `handle` 메서드 안에서 이벤트에 반응해 필요한 작업을 수행할 수 있습니다.

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
        // $event->order로 주문 정보에 접근...
    }
}
```

> [!NOTE]
> 이벤트 리스너의 생성자에서 필요한 의존성을 타입힌트로 지정할 수도 있습니다. 모든 이벤트 리스너는 라라벨 [서비스 컨테이너](/docs/12.x/container)를 통해 해결(주입)되므로, 의존성이 자동으로 주입됩니다.

<a name="stopping-the-propagation-of-an-event"></a>
#### 이벤트 전파 중단하기

경우에 따라, 이벤트가 이후 리스너들에게 더 전달되지 않도록 하고 싶을 수 있습니다. 이럴 때는 리스너의 `handle` 메서드에서 `false`를 반환하면 됩니다.

<a name="queued-event-listeners"></a>
## 큐잉된(Queued) 이벤트 리스너

이메일 전송이나 외부 HTTP 요청처럼 오래 걸릴 수 있는 작업을 리스너에서 처리해야 하는 경우, 리스너를 큐에 넣어 비동기로 실행하도록 할 수 있습니다. 큐잉된 리스너를 사용하려면 먼저 [큐를 설정](/docs/12.x/queues)하고, 서버나 개발 환경에서 큐 워커도 실행해야 합니다.

리스너를 큐에 넣으려면, 리스너 클래스에 `ShouldQueue` 인터페이스를 추가하면 됩니다. `make:listener` Artisan 명령어로 생성한 리스너는 기본적으로 해당 인터페이스가 네임스페이스에 임포트되어 있으니 바로 사용할 수 있습니다.

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

이렇게 하면, 이 리스너가 담당하는 이벤트가 디스패치될 때 라라벨 이벤트 디스패처가 자동으로 이 리스너를 [큐 시스템](/docs/12.x/queues)을 통해 큐잉해 실행합니다. 리스너가 문제없이 실행되어 예외가 발생하지 않으면, 해당 큐잉된 작업은 처리 완료 후 자동 삭제됩니다.

<a name="customizing-the-queue-connection-queue-name"></a>
#### 큐 커넥션, 큐 이름, 딜레이(지연시간) 커스터마이즈

리스너 클래스에 `$connection`, `$queue`, `$delay` 속성을 정의하면, 큐 커넥션, 큐 이름, 큐에 올라간 후 지연시간(초)을 설정할 수 있습니다.

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    /**
     * The name of the connection the job should be sent to.
     *
     * @var string|null
     */
    public $connection = 'sqs';

    /**
     * The name of the queue the job should be sent to.
     *
     * @var string|null
     */
    public $queue = 'listeners';

    /**
     * The time (seconds) before the job should be processed.
     *
     * @var int
     */
    public $delay = 60;
}
```

실행 시점에 리스너의 큐 커넥션, 큐 이름, 딜레이를 동적으로 지정하고 싶다면, `viaConnection`, `viaQueue`, `withDelay` 메서드를 리스너에 정의하면 됩니다.

```php
/**
 * Get the name of the listener's queue connection.
 */
public function viaConnection(): string
{
    return 'sqs';
}

/**
 * Get the name of the listener's queue.
 */
public function viaQueue(): string
{
    return 'listeners';
}

/**
 * Get the number of seconds before the job should be processed.
 */
public function withDelay(OrderShipped $event): int
{
    return $event->highPriority ? 0 : 60;
}
```

<a name="conditionally-queueing-listeners"></a>
#### 리스너의 큐잉 조건 지정하기

경우에 따라, 실제로 큐잉할지는 런타임 데이터에 따라 판별해야 할 때가 있습니다. 이런 경우, 리스너에 `shouldQueue` 메서드를 추가해 조건을 명시할 수 있습니다. 이 메서드가 `false`를 반환하면 해당 리스너는 큐잉되지 않습니다.

```php
<?php

namespace App\Listeners;

use App\Events\OrderCreated;
use Illuminate\Contracts\Queue\ShouldQueue;

class RewardGiftCard implements ShouldQueue
{
    /**
     * Reward a gift card to the customer.
     */
    public function handle(OrderCreated $event): void
    {
        // ...
    }

    /**
     * Determine whether the listener should be queued.
     */
    public function shouldQueue(OrderCreated $event): bool
    {
        return $event->order->subtotal >= 5000;
    }
}
```

<a name="manually-interacting-with-the-queue"></a>
### 큐 직접 다루기

리스너 내부에서 큐 작업 객체의 `delete`, `release` 메서드에 직접 접근할 필요가 있다면, `Illuminate\Queue\InteractsWithQueue` 트레이트를 사용하면 됩니다. 기본적으로 Artisan으로 생성된 리스너에는 이 트레이트가 이미 추가되어 있으므로, 아래처럼 바로 활용할 수 있습니다.

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
     * Handle the event.
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

큐잉된 리스너가 데이터베이스 트랜잭션 안에서 실행될 때, 큐가 트랜잭션 커밋 전에 리스너를 처리할 수도 있습니다. 이런 경우, 트랜잭션 내에서 변경된 모델 정보나 데이터베이스 기록이 아직 DB에 완전히 반영되지 않아, 리스너가 의존하는 데이터가 존재하지 않거나 예기치 않은 오류가 발생할 수 있습니다.

만약 큐 커넥션의 `after_commit` 설정값이 `false`라면, 특정 큐잉된 리스너에 대해 모든 열린 트랜잭션이 커밋된 후 디스패치되게 하고 싶다면, 리스너 클래스에 `ShouldQueueAfterCommit` 인터페이스를 구현하면 됩니다.

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
> 이런 문제들에 대한 자세한 해결 방법은 [큐잉된 작업과 데이터베이스 트랜잭션](/docs/12.x/queues#jobs-and-database-transactions) 문서를 참고해 주세요.

<a name="handling-failed-jobs"></a>
### 실패한 작업 처리하기

큐잉된 이벤트 리스너가 실패할 수도 있습니다. 큐 리스너가 큐 워커에 지정한 최대 재시도 횟수를 초과하면, 리스너의 `failed` 메서드가 호출됩니다. 이 메서드는 이벤트 인스턴스와 실패 원인인 `Throwable` 객체를 인자로 받습니다.

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
     * Handle the event.
     */
    public function handle(OrderShipped $event): void
    {
        // ...
    }

    /**
     * Handle a job failure.
     */
    public function failed(OrderShipped $event, Throwable $exception): void
    {
        // ...
    }
}
```

<a name="specifying-queued-listener-maximum-attempts"></a>
#### 큐 리스너 최대 재시도 횟수 지정

큐잉된 리스너에서 오류가 발생했을 때 무한 반복으로 재시도하는 것을 방지하고 싶을 때, 재시도할 횟수 또는 시간을 지정할 수 있습니다.

리스너 클래스에 `$tries` 프로퍼티를 추가하면, 지정한 횟수만큼만 재시도하고 실패로 간주합니다.

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
     * The number of times the queued listener may be attempted.
     *
     * @var int
     */
    public $tries = 5;
}
```

실패 전 재시도 횟수 대신, 어느 시점까지만 재시도할지 시간 기반으로 설정할 수도 있습니다. 이를 위해 리스너 클래스에 `retryUntil` 메서드를 정의하고, 반환값으로 `DateTime` 인스턴스를 반환하면 됩니다.

```php
use DateTime;

/**
 * Determine the time at which the listener should timeout.
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(5);
}
```

`retryUntil`과 `tries`를 모두 정의한 경우에는 `retryUntil`이 우선 적용됩니다.

<a name="specifying-queued-listener-backoff"></a>
#### 큐 리스너 백오프(Backoff) 지정

리스너가 예외를 만나 재시도할 때, 기다릴 초(second)를 지정하고 싶으면 `backoff` 프로퍼티를 리스너 클래스에 선언할 수 있습니다.

```php
/**
 * The number of seconds to wait before retrying the queued listener.
 *
 * @var int
 */
public $backoff = 3;
```

재시도 대기 시간을 더 복잡하게 처리하고 싶으면, `backoff` 메서드를 추가해 값을 반환할 수도 있습니다.

```php
/**
 * Calculate the number of seconds to wait before retrying the queued listener.
 */
public function backoff(): int
{
    return 3;
}
```

"지수 백오프(exponential backoff)"처럼 각 재시도마다 기다리는 시간을 다르게 지정하고 싶다면, `backoff` 메서드에서 값의 배열을 반환하면 됩니다. 아래 예시에서는 1회째 재시도 후 1초, 2회째 후 5초, 3회째 후 10초, 그 이후에는 10초 간격으로 대기합니다.

```php
/**
 * Calculate the number of seconds to wait before retrying the queued listener.
 *
 * @return list<int>
 */
public function backoff(): array
{
    return [1, 5, 10];
}
```

<a name="dispatching-events"></a>

## 이벤트 디스패치(Dispatching Events)

이벤트를 디스패치하려면 해당 이벤트 클래스의 정적 `dispatch` 메서드를 호출하면 됩니다. 이 메서드는 `Illuminate\Foundation\Events\Dispatchable` 트레이트가 이벤트에 제공하는 기능입니다. `dispatch` 메서드에 전달된 모든 인수는 이벤트의 생성자에 그대로 전달됩니다.

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
     * Ship the given order.
     */
    public function store(Request $request): RedirectResponse
    {
        $order = Order::findOrFail($request->order_id);

        // Order shipment logic...

        OrderShipped::dispatch($order);

        return redirect('/orders');
    }
}
```

이벤트를 조건에 따라 디스패치하고 싶다면, `dispatchIf` 및 `dispatchUnless` 메서드를 사용할 수 있습니다.

```php
OrderShipped::dispatchIf($condition, $order);

OrderShipped::dispatchUnless($condition, $order);
```

> [!NOTE]
> 테스트 시에는 실제로 리스너를 실행하지 않고 특정 이벤트가 디스패치되었는지 확인하는 것이 도움이 될 수 있습니다. 라라벨의 [내장 테스트 헬퍼](#testing)를 사용하면 이를 매우 쉽게 할 수 있습니다.

<a name="dispatching-events-after-database-transactions"></a>
### 데이터베이스 트랜잭션 이후 이벤트 디스패치

특정 상황에서는 현재 활성화된 데이터베이스 트랜잭션이 커밋된 후에만 이벤트를 디스패치하도록 라라벨에 지시하고 싶을 때가 있습니다. 이를 위해 이벤트 클래스에서 `ShouldDispatchAfterCommit` 인터페이스를 구현할 수 있습니다.

이 인터페이스를 사용하면 현재의 데이터베이스 트랜잭션이 커밋될 때까지 이벤트를 디스패치하지 않도록 라라벨에 지시할 수 있습니다. 만약 트랜잭션이 실패한다면 이벤트는 폐기됩니다. 반대로 이벤트가 디스패치될 때 트랜잭션이 진행 중이 아니라면 이벤트는 즉시 디스패치됩니다.

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
     * Create a new event instance.
     */
    public function __construct(
        public Order $order,
    ) {}
}
```

<a name="event-subscribers"></a>
## 이벤트 구독자(Event Subscribers)

<a name="writing-event-subscribers"></a>
### 이벤트 구독자 클래스 작성하기

이벤트 구독자는 한 클래스 안에서 여러 이벤트를 구독할 수 있도록 해주는 클래스입니다. 즉, 하나의 클래스에 여러 이벤트 핸들러를 정의할 수 있습니다. 구독자 클래스는 반드시 `subscribe` 메서드를 정의해야 하며, 이 메서드는 이벤트 디스패처 인스턴스를 인수로 받습니다. 전달받은 디스패처의 `listen` 메서드를 호출하여 이벤트 리스너를 등록할 수 있습니다.

```php
<?php

namespace App\Listeners;

use Illuminate\Auth\Events\Login;
use Illuminate\Auth\Events\Logout;
use Illuminate\Events\Dispatcher;

class UserEventSubscriber
{
    /**
     * Handle user login events.
     */
    public function handleUserLogin(Login $event): void {}

    /**
     * Handle user logout events.
     */
    public function handleUserLogout(Logout $event): void {}

    /**
     * Register the listeners for the subscriber.
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

이벤트 리스너 메서드가 구독자 클래스 내에 정의되어 있는 경우, `subscribe` 메서드에서 반환할 배열로 이벤트와 메서드명을 매핑하는 방식이 더 편리할 수 있습니다. 라라벨은 이벤트 리스너를 등록할 때 구독자 클래스명을 자동으로 인식합니다.

```php
<?php

namespace App\Listeners;

use Illuminate\Auth\Events\Login;
use Illuminate\Auth\Events\Logout;
use Illuminate\Events\Dispatcher;

class UserEventSubscriber
{
    /**
     * Handle user login events.
     */
    public function handleUserLogin(Login $event): void {}

    /**
     * Handle user logout events.
     */
    public function handleUserLogout(Logout $event): void {}

    /**
     * Register the listeners for the subscriber.
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

구독자 클래스를 작성한 후, 해당 클래스가 라라벨의 [이벤트 자동 탐색 규칙](#event-discovery)을 따른다면 메서드가 자동으로 등록됩니다. 그렇지 않은 경우에는 `Event` 파사드의 `subscribe` 메서드를 이용해 구독자를 수동으로 등록할 수 있습니다. 일반적으로는 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 수행하는 것이 일반적입니다.

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
## 테스트(Testing)

이벤트를 디스패치하는 코드를 테스트할 때, 실제로 이벤트의 리스너가 실행되지 않도록 하고 싶을 수 있습니다. 리스너의 코드는 별도로 직접 테스트할 수 있기 때문입니다. 실제로 리스너를 테스트하려면 테스트에서 리스너 인스턴스를 직접 생성하여 `handle` 메서드를 호출하면 됩니다.

`Event` 파사드의 `fake` 메서드를 사용하면 리스너 실행을 막고, 테스트할 코드를 실행한 뒤, 애플리케이션에서 어떤 이벤트가 디스패치되었는지 `assertDispatched`, `assertNotDispatched`, `assertNothingDispatched` 등의 메서드를 통해 쉽게 검증할 수 있습니다.

```php tab=Pest
<?php

use App\Events\OrderFailedToShip;
use App\Events\OrderShipped;
use Illuminate\Support\Facades\Event;

test('orders can be shipped', function () {
    Event::fake();

    // Perform order shipping...

    // Assert that an event was dispatched...
    Event::assertDispatched(OrderShipped::class);

    // Assert an event was dispatched twice...
    Event::assertDispatched(OrderShipped::class, 2);

    // Assert an event was not dispatched...
    Event::assertNotDispatched(OrderFailedToShip::class);

    // Assert that no events were dispatched...
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
     * Test order shipping.
     */
    public function test_orders_can_be_shipped(): void
    {
        Event::fake();

        // Perform order shipping...

        // Assert that an event was dispatched...
        Event::assertDispatched(OrderShipped::class);

        // Assert an event was dispatched twice...
        Event::assertDispatched(OrderShipped::class, 2);

        // Assert an event was not dispatched...
        Event::assertNotDispatched(OrderFailedToShip::class);

        // Assert that no events were dispatched...
        Event::assertNothingDispatched();
    }
}
```

`assertDispatched` 또는 `assertNotDispatched` 메서드에 클로저를 전달하면, "진위 테스트"에 통과하는(즉, 조건을 만족하는) 이벤트가 디스패치되었는지 검증할 수 있습니다. 해당 조건을 만족하는 이벤트가 하나라도 디스패치되었다면 검증이 통과합니다.

```php
Event::assertDispatched(function (OrderShipped $event) use ($order) {
    return $event->order->id === $order->id;
});
```

특정 이벤트에 대해 지정한 이벤트 리스너가 실제로 등록되어 있는지 확인하고 싶다면, `assertListening` 메서드를 사용할 수 있습니다.

```php
Event::assertListening(
    OrderShipped::class,
    SendShipmentNotification::class
);
```

> [!WARNING]
> `Event::fake()`를 호출하면 이 후에 어떤 이벤트 리스너도 실행되지 않습니다. 따라서 모델의 `creating` 이벤트에서 UUID를 생성하는 것과 같이 이벤트에 의존하는 팩토리 코드를 테스트할 때는 팩토리를 먼저 사용한 후 `Event::fake()`를 호출해야 합니다.

<a name="faking-a-subset-of-events"></a>
### 특정 이벤트만 가짜(fake)로 처리하기

테스트에서 특정 이벤트 리스너만 가짜로 처리하고 싶다면, `fake` 또는 `fakeFor` 메서드에 해당 이벤트 목록을 전달할 수 있습니다.

```php tab=Pest
test('orders can be processed', function () {
    Event::fake([
        OrderCreated::class,
    ]);

    $order = Order::factory()->create();

    Event::assertDispatched(OrderCreated::class);

    // Other events are dispatched as normal...
    $order->update([
        // ...
    ]);
});
```

```php tab=PHPUnit
/**
 * Test order process.
 */
public function test_orders_can_be_processed(): void
{
    Event::fake([
        OrderCreated::class,
    ]);

    $order = Order::factory()->create();

    Event::assertDispatched(OrderCreated::class);

    // Other events are dispatched as normal...
    $order->update([
        // ...
    ]);
}
```

반대로, 특정 이벤트를 제외한 모든 이벤트 리스너를 가짜로 처리하고 싶다면 `except` 메서드를 사용할 수 있습니다.

```php
Event::fake()->except([
    OrderCreated::class,
]);
```

<a name="scoped-event-fakes"></a>
### 범위 지정 스코프 내에서만 이벤트 가짜 처리

테스트 코드의 특정 부분에서만 이벤트 리스너를 가짜로 처리하고 싶다면, `fakeFor` 메서드를 사용할 수 있습니다.

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

    // Events are dispatched as normal and observers will run...
    $order->update([
        // ...
    ]);
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
     * Test order process.
     */
    public function test_orders_can_be_processed(): void
    {
        $order = Event::fakeFor(function () {
            $order = Order::factory()->create();

            Event::assertDispatched(OrderCreated::class);

            return $order;
        });

        // Events are dispatched as normal and observers will run...
        $order->update([
            // ...
        ]);
    }
}
```