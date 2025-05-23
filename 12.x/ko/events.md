# 이벤트 (Events)

- [소개](#introduction)
- [이벤트 및 리스너 생성](#generating-events-and-listeners)
- [이벤트 및 리스너 등록](#registering-events-and-listeners)
    - [이벤트 자동 탐색](#event-discovery)
    - [이벤트 수동 등록](#manually-registering-events)
    - [클로저 리스너](#closure-listeners)
- [이벤트 정의](#defining-events)
- [리스너 정의](#defining-listeners)
- [큐잉된 이벤트 리스너](#queued-event-listeners)
    - [큐 직접 다루기](#manually-interacting-with-the-queue)
    - [큐잉 리스너와 데이터베이스 트랜잭션](#queued-event-listeners-and-database-transactions)
    - [실패한 작업 처리](#handling-failed-jobs)
- [이벤트 디스패치](#dispatching-events)
    - [데이터베이스 트랜잭션 이후 이벤트 디스패치](#dispatching-events-after-database-transactions)
- [이벤트 구독자](#event-subscribers)
    - [이벤트 구독자 작성](#writing-event-subscribers)
    - [이벤트 구독자 등록](#registering-event-subscribers)
- [테스트](#testing)
    - [일부 이벤트만 가짜 처리하기](#faking-a-subset-of-events)
    - [스코프 단위 이벤트 페이크](#scoped-event-fakes)

<a name="introduction"></a>
## 소개

라라벨의 이벤트 기능은 간단한 옵저버 패턴을 제공합니다. 이를 통해 여러분의 애플리케이션에서 발생하는 다양한 이벤트를 구독하고, 해당 이벤트를 수신하여 처리할 수 있습니다. 이벤트 클래스는 일반적으로 `app/Events` 디렉터리에, 리스너는 `app/Listeners` 디렉터리에 저장됩니다. 만약 이 디렉터리가 현재 애플리케이션에 없다면, Artisan 콘솔 명령어로 이벤트와 리스너를 생성할 때 자동으로 만들어지니 걱정하지 않으셔도 됩니다.

이벤트는 애플리케이션의 여러 부분을 느슨하게 결합하는 데 탁월한 방법입니다. 하나의 이벤트에 여러 리스너를 등록할 수 있으며, 이 리스너들은 서로에게 의존하지 않습니다. 예를 들어, 주문이 발송될 때마다 사용자에게 Slack 알림을 보내고 싶다고 가정해봅시다. 주문 처리 코드를 Slack 알림 코드와 직접 연결하지 않고, `App\Events\OrderShipped` 이벤트를 발생시키면, 이를 수신하는 리스너에서 Slack 알림을 전송하도록 처리할 수 있습니다.

<a name="generating-events-and-listeners"></a>
## 이벤트 및 리스너 생성

이벤트와 리스너를 빠르게 생성하려면 `make:event`와 `make:listener` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan make:event PodcastProcessed

php artisan make:listener SendPodcastNotification --event=PodcastProcessed
```

편의를 위해, 추가 인수 없이 `make:event`나 `make:listener` Artisan 명령어를 실행할 수도 있습니다. 이 경우 라라벨에서 클래스명을 입력하도록 안내하고, 리스너를 생성할 때는 어떤 이벤트를 수신할지 물어봅니다.

```shell
php artisan make:event

php artisan make:listener
```

<a name="registering-events-and-listeners"></a>
## 이벤트 및 리스너 등록

<a name="event-discovery"></a>
### 이벤트 자동 탐색

기본적으로 라라벨은 애플리케이션의 `Listeners` 디렉터리를 스캔하여 이벤트 리스너를 자동으로 찾아 등록합니다. 라라벨은 리스너 클래스의 메서드 중 `handle` 또는 `__invoke`로 시작하는 메서드를 발견하면, 해당 메서드 시그니처에 타입힌트된 이벤트 클래스에 대한 리스너로 자동 등록합니다.

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

PHP의 유니언 타입을 활용하여 여러 이벤트를 동시에 수신할 수도 있습니다.

```php
/**
 * Handle the event.
 */
public function handle(PodcastProcessed|PodcastPublished $event): void
{
    // ...
}
```

만약 리스너를 다른 디렉터리나 여러 디렉터리에 저장하고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에서 `withEvents` 메서드를 사용해 해당 디렉터리를 스캔하도록 지정할 수 있습니다.

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/Orders/Listeners',
])
```

비슷한 여러 디렉터리를 한 번에 탐색하려면, `*` 와일드카드 문자를 사용할 수 있습니다.

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/*/Listeners',
])
```

`event:list` 명령어를 실행하면 애플리케이션에 등록된 모든 리스너를 확인할 수 있습니다.

```shell
php artisan event:list
```

<a name="event-discovery-in-production"></a>
#### 운영 환경에서 이벤트 자동 탐색

애플리케이션의 성능을 향상시키기 위해, `optimize` 또는 `event:cache` Artisan 명령어를 사용하여 모든 리스너의 매니페스트를 캐시해두는 것이 좋습니다. 보통 이 명령어는 애플리케이션 [배포 과정](/docs/12.x/deployment#optimization)에서 실행해야 합니다. 이 매니페스트는 프레임워크가 이벤트 등록 과정을 더 빠르게 처리하는 데 사용됩니다. 이벤트 캐시를 삭제하려면 `event:clear` 명령어를 사용하면 됩니다.

<a name="manually-registering-events"></a>
### 이벤트 수동 등록

`Event` 파사드를 이용해, 애플리케이션의 `AppServiceProvider`의 `boot` 메서드 안에서 이벤트와 해당 리스너를 직접 등록할 수 있습니다.

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

`event:list` 명령어를 사용하면, 애플리케이션에 등록된 모든 리스너를 볼 수 있습니다.

```shell
php artisan event:list
```

<a name="closure-listeners"></a>
### 클로저 리스너

일반적으로 리스너는 클래스로 정의하지만, 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 클로저 기반 이벤트 리스너를 수동으로 등록할 수도 있습니다.

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
#### 큐잉이 가능한 익명 이벤트 리스너

클로저 기반 이벤트 리스너를 등록할 때, 해당 클로저를 `Illuminate\Events\queueable` 함수로 감싸주면 라라벨이 이 리스너를 [큐](/docs/12.x/queues)로 비동기 실행하도록 지정할 수 있습니다.

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

큐잉된 작업과 마찬가지로, `onConnection`, `onQueue`, `delay` 메서드를 사용해 큐의 연결, 큐 이름, 지연 시간 등을 조정할 수 있습니다.

```php
Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->onConnection('redis')->onQueue('podcasts')->delay(now()->addSeconds(10)));
```

익명 큐 리스너가 실패했을 때 처리하고 싶다면, `queueable` 리스너 정의 시 `catch` 메서드에 클로저를 전달할 수 있습니다. 이 클로저는 이벤트 인스턴스와 실패 원인인 `Throwable` 인스턴스를 전달받습니다.

```php
use App\Events\PodcastProcessed;
use function Illuminate\Events\queueable;
use Illuminate\Support\Facades\Event;
use Throwable;

Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->catch(function (PodcastProcessed $event, Throwable $e) {
    // 큐 리스너 실패 처리...
}));
```

<a name="wildcard-event-listeners"></a>
#### 와일드카드 이벤트 리스너

`*` 문자를 와일드카드 파라미터로 사용해 여러 이벤트를 하나의 리스너로 받을 수도 있습니다. 와일드카드 리스너는 첫 번째 인수로 이벤트 이름을, 두 번째 인수로 이벤트 데이터 배열을 전달받습니다.

```php
Event::listen('event.*', function (string $eventName, array $data) {
    // ...
});
```

<a name="defining-events"></a>
## 이벤트 정의

이벤트 클래스는 이벤트와 관련된 데이터를 담는 데이터 컨테이너 역할을 합니다. 예를 들어 `App\Events\OrderShipped` 이벤트가 [Eloquent ORM](/docs/12.x/eloquent) 객체를 전달받는다고 가정해봅시다.

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

위에서 볼 수 있듯, 이 이벤트 클래스는 별도의 로직을 포함하지 않고, 실제로 주문된 `App\Models\Order` 인스턴스를 담는 컨테이너 역할을 합니다. 이벤트에서 사용하는 `SerializesModels` 트레이트는, 이벤트 객체가 PHP의 `serialize` 함수를 이용해 직렬화될 때(Eloquent 모델을 포함하는 경우, 예: [큐잉 리스너](#queued-event-listeners) 사용 시), 해당 모델을 안전하게 직렬화합니다.

<a name="defining-listeners"></a>
## 리스너 정의

이제 예시 이벤트를 처리할 리스너를 살펴보겠습니다. 이벤트 리스너는 `handle` 메서드에서 이벤트 인스턴스를 전달받습니다. `make:listener` Artisan 명령어를 `--event` 옵션과 함께 사용하면, 해당 이벤트 클래스를 자동으로 임포트하고, `handle` 메서드에 타입힌트까지 추가해줍니다. `handle` 메서드 안에서는 이벤트에 응답하는 데 필요한 모든 처리를 자유롭게 할 수 있습니다.

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
        // $event->order로 주문 접근...
    }
}
```

> [!NOTE]
> 이벤트 리스너의 생성자에서 필요한 의존성을 타입힌트로 선언할 수도 있습니다. 모든 이벤트 리스너는 라라벨 [서비스 컨테이너](/docs/12.x/container)를 통해 해결되므로, 의존성은 자동으로 주입됩니다.

<a name="stopping-the-propagation-of-an-event"></a>
#### 이벤트 전파 중단하기

때때로, 여러분은 이벤트가 다른 리스너로 전파되는 것을 중단하고 싶을 수 있습니다. 이럴 때는 리스너의 `handle` 메서드에서 `false`를 반환하면 됩니다.

<a name="queued-event-listeners"></a>
## 큐잉된 이벤트 리스너

리스너에서 이메일 전송이나 HTTP 요청과 같은 시간이 오래 걸리는 작업을 한다면, 리스너를 큐로 비동기 처리하면 좋습니다. 큐잉된 리스너를 사용하기 전에 [큐 설정](/docs/12.x/queues)을 하고, 서버 또는 로컬 개발 환경에서 큐 워커를 실행하고 있어야 합니다.

리스너를 큐잉 대상으로 지정하려면, 해당 리스너 클래스에 `ShouldQueue` 인터페이스를 구현하면 됩니다. `make:listener` Artisan 명령어로 생성된 리스너는 이 인터페이스를 기본으로 네임스페이스에 임포트하므로 바로 사용할 수 있습니다.

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

이제 이 리스너가 처리하는 이벤트가 발생하면, 이벤트 디스패처가 자동으로 라라벨의 [큐 시스템](/docs/12.x/queues)을 사용해 리스너를 큐에 등록합니다. 큐에서 리스너가 실행될 때 예외가 발생하지 않으면, 처리 후 해당 큐 작업은 자동으로 삭제됩니다.

<a name="customizing-the-queue-connection-queue-name"></a>
#### 큐 연결, 이름, 지연 시간 커스터마이징

리스너 클래스에 `$connection`, `$queue`, `$delay` 속성을 정의하여, 큐 연결 이름, 큐 이름, 큐 지연 시간을 커스터마이징할 수 있습니다.

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

런타임에 큐 연결명이나 큐 이름, 지연 시간을 지정하려면, `viaConnection`, `viaQueue`, `withDelay` 메서드를 정의할 수 있습니다.

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

경우에 따라, 리스너가 큐에 등록되어야 할지 여부를 실행 시점에 결정해야 할 수도 있습니다. 이를 위해 리스너에 `shouldQueue` 메서드를 추가할 수 있으며, 이 메서드가 `false`를 반환하면 해당 리스너는 큐에 등록되지 않습니다.

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

리스너가 내부적으로 사용하는 큐 작업의 `delete`, `release` 메서드에 직접 접근해야 한다면, `Illuminate\Queue\InteractsWithQueue` 트레이트를 사용할 수 있습니다. 이 트레이트는 기본적으로 생성된 리스너에 포함되어 있으며, 해당 메서드 사용을 지원합니다.

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
### 큐잉 리스너와 데이터베이스 트랜잭션

큐잉된 리스너가 데이터베이스 트랜잭션 내에서 디스패치될 때, 큐가 데이터베이스 트랜잭션이 커밋되기 전에 리스너를 처리할 수도 있습니다. 이렇게 되면, 트랜잭션에서 모델이나 레코드에 적용한 변경 사항이 실제 데이터베이스에 반영되기 전에 큐가 처리될 수 있습니다. 또한 트랜잭션 내에서 생성한 모델이나 레코드가 실제로 데이터베이스에 존재하지 않을 수도 있습니다. 리스너가 이런 모델에 의존한다면, 큐 작업이 실행될 때 예기치 않은 오류가 발생할 수 있습니다.

만약 큐 연결 설정의 `after_commit` 옵션이 `false`로 되어 있다면, 특정 큐잉 리스너가 모든 열린 데이터베이스 트랜잭션이 커밋된 후에 디스패치되도록 하려면 리스너 클래스에 `ShouldQueueAfterCommit` 인터페이스를 구현하면 됩니다.

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
> 이러한 문제를 회피하는 방법에 대해 더 알고 싶다면, [큐 작업과 데이터베이스 트랜잭션](/docs/12.x/queues#jobs-and-database-transactions) 문서를 참조하세요.

<a name="handling-failed-jobs"></a>
### 실패한 작업 처리

큐잉된 이벤트 리스너가 실패할 수 있는 경우가 있습니다. 큐잉 리스너가 큐 워커에서 설정한 최대 재시도 횟수를 초과하면, `failed` 메서드가 해당 리스너에서 호출됩니다. 이 `failed` 메서드는 이벤트 인스턴스와 실패를 일으킨 `Throwable` 인스턴스를 전달받습니다.

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

큐잉된 리스너에서 에러가 발생했을 때, 무한정 재시도되길 원하지는 않을 것입니다. 라라벨에서는 리스너가 몇 번 혹은 얼마 동안 시도될지 다양한 방법으로 설정할 수 있습니다.

리스너 클래스에 `$tries` 속성을 정의해, 해당 리스너가 실패로 간주되기 전까지 몇 번 재시도할지 지정할 수 있습니다.

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

실패 전 몇 번 재시도할지를 지정하는 대신, 언제까지 재시도할지 기준을 정할 수도 있습니다. 이 경우 정해진 시간까지만 무한히 재시도됩니다. 재시도 제한 시간을 정하려면 리스너 클래스에 `retryUntil` 메서드를 추가하면 됩니다. 이 메서드는 `DateTime` 인스턴스를 반환해야 합니다.

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

`retryUntil`과 `tries`가 모두 정의되어 있다면, 라라벨은 우선적으로 `retryUntil` 메서드를 적용합니다.

<a name="specifying-queued-listener-backoff"></a>
#### 큐 리스너 백오프(재시도 대기 시간) 지정

예외가 발생한 리스너를 몇 초 후 다시 재시도할지 설정하려면, 리스너 클래스에 `backoff` 속성을 추가하면 됩니다.

```php
/**
 * The number of seconds to wait before retrying the queued listener.
 *
 * @var int
 */
public $backoff = 3;
```

리스너의 백오프 시간을 더 복잡하게 지정하고 싶다면, 리스너 클래스에 `backoff` 메서드를 정의할 수 있습니다.

```php
/**
 * Calculate the number of seconds to wait before retrying the queued listener.
 */
public function backoff(): int
{
    return 3;
}
```

아래와 같이 백오프 값 배열을 반환하면, "지수형" 백오프 방식도 쉽게 구현할 수 있습니다. 예를 들어 최초 재시도는 1초 대기, 두 번째는 5초, 세 번째와 이후부터는 10초 동안 대기하게 됩니다.

```php
/**
 * Calculate the number of seconds to wait before retrying the queued listener.
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

이벤트를 디스패치하려면, 해당 이벤트의 정적 `dispatch` 메서드를 호출하면 됩니다. 이 메서드는 이벤트 클래스가 `Illuminate\Foundation\Events\Dispatchable` 트레이트를 사용할 때 자동으로 제공됩니다. `dispatch` 메서드에 전달한 모든 인자는 이벤트의 생성자로 전달됩니다.

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

이벤트를 조건부로 디스패치하고 싶다면, `dispatchIf`와 `dispatchUnless` 메서드를 사용할 수 있습니다.

```php
OrderShipped::dispatchIf($condition, $order);

OrderShipped::dispatchUnless($condition, $order);
```

> [!NOTE]
> 테스트를 진행할 때, 실제로 이벤트 리스너가 동작하지 않고 특정 이벤트가 디스패치되었는지 검증하려면 라라벨의 [내장 테스트 도우미](#testing)를 이용하면 아주 간편하게 처리할 수 있습니다.

<a name="dispatching-events-after-database-transactions"></a>
### 데이터베이스 트랜잭션 이후에 이벤트 디스패치하기

때로는, 현재 진행 중인 데이터베이스 트랜잭션이 커밋된 이후에만 이벤트를 디스패치하도록 라라벨에 지시하고 싶을 수 있습니다. 이를 위해서는 이벤트 클래스에서 `ShouldDispatchAfterCommit` 인터페이스를 구현하면 됩니다.

이 인터페이스는 라라벨이 현재 데이터베이스 트랜잭션이 커밋될 때까지 해당 이벤트를 디스패치하지 않도록 동작을 변경합니다. 만약 트랜잭션이 실패한다면, 이벤트는 무시(폐기)됩니다. 이벤트가 디스패치될 때 활성 트랜잭션이 없다면 즉시 이벤트가 디스패치됩니다.

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
## 이벤트 구독자(Event Subscriber)

<a name="writing-event-subscribers"></a>
### 이벤트 구독자 작성하기

이벤트 구독자는 여러 개의 이벤트를 한 클래스에서 구독(subscribe)할 수 있도록 하는 클래스입니다. 즉, 하나의 클래스 안에 여러 이벤트에 대한 핸들러를 정의할 수 있습니다. 구독자는 반드시 `subscribe` 메서드를 정의해야 하며, 이 메서드에는 이벤트 디스패처 인스턴스가 전달됩니다. 전달된 이벤트 디스패처의 `listen` 메서드를 사용해서 이벤트 리스너를 등록할 수 있습니다.

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

구독자 내부에서 이벤트 리스너 메서드를 정의할 경우, 구독자 클래스의 `subscribe` 메서드에서 이벤트와 핸들러 메서드명을 매핑한 배열을 반환하는 방식이 더 편리할 수 있습니다. 이 방법을 사용하면, 이벤트 리스너 등록 시 라라벨이 구독자 클래스명을 자동으로 처리해 줍니다.

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

구독자 클래스를 작성한 후, 해당 클래스의 핸들러 메서드 이름이 라라벨의 [이벤트 자동 탐색 규칙](#event-discovery)을 따르고 있다면 라라벨이 자동으로 등록해 줍니다. 만약 그렇지 않다면, `Event` 파사드의 `subscribe` 메서드를 통해 수동으로 구독자를 등록할 수 있습니다. 보통 이는 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드 안에서 처리합니다.

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

이벤트를 디스패치하는 코드를 테스트할 때, 실제로 이벤트의 리스너가 동작하지 않도록 라라벨에 지시하고 싶을 수 있습니다. 왜냐하면 리스너의 코드는 별도로 단위 테스트가 가능하고, 이벤트 디스패치 코드와 분리해서 테스트하는 것이 좋기 때문입니다. 물론, 직접 리스너 인스턴스를 생성해서 `handle` 메서드를 호출하는 방식으로 리스너 자체를 테스트할 수도 있습니다.

`Event` 파사드의 `fake` 메서드를 사용하면 리스너를 실행하지 않고 테스트 코드를 수행한 뒤, `assertDispatched`, `assertNotDispatched`, `assertNothingDispatched` 메서드를 사용해서 실제 앱에서 어떤 이벤트가 디스패치되었는지 확실하게 검증할 수 있습니다.

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

`assertDispatched` 또는 `assertNotDispatched` 메서드에 클로저를 전달하여, 클로저에서 정의한 "진실성 조건(truth test)"을 만족하는 이벤트가 실제로 디스패치되었는지 검증할 수 있습니다. 조건에 맞는 이벤트가 하나라도 디스패치되었다면 검증에 성공하게 됩니다.

```php
Event::assertDispatched(function (OrderShipped $event) use ($order) {
    return $event->order->id === $order->id;
});
```

특정 이벤트에 대해 어떤 이벤트 리스너가 실제로 리스닝하고 있는지 검증하고 싶다면, `assertListening` 메서드를 사용할 수 있습니다.

```php
Event::assertListening(
    OrderShipped::class,
    SendShipmentNotification::class
);
```

> [!WARNING]
> `Event::fake()`를 호출하면 **모든** 이벤트 리스너가 실행되지 않습니다. 따라서, 예를 들어 모델의 `creating` 이벤트에서 UUID를 생성하는 등 이벤트 기반 동작에 의존하는 모델 팩토리를 사용할 경우에는, 팩토리를 먼저 사용하고 난 뒤에 `Event::fake()`를 호출해야 합니다.

<a name="faking-a-subset-of-events"></a>
### 일부 이벤트만 페이크로 처리하기

특정 이벤트 리스너만 페이크 처리하고 싶다면, 해당 이벤트들을 배열로 `fake` 또는 `fakeFor` 메서드에 전달할 수 있습니다.

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

`except` 메서드를 활용하면 지정한 일부 이벤트를 제외한 **모든** 이벤트를 페이크 처리할 수도 있습니다.

```php
Event::fake()->except([
    OrderCreated::class,
]);
```

<a name="scoped-event-fakes"></a>
### 범위 한정 이벤트 페이크(Scoped Event Fakes)

테스트 코드의 일부분에서만 이벤트 리스너를 페이크 처리를 하고 싶다면, `fakeFor` 메서드를 사용하면 됩니다.

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