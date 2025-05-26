# 이벤트 (Events)

- [소개](#introduction)
- [이벤트 및 리스너 생성](#generating-events-and-listeners)
- [이벤트 및 리스너 등록](#registering-events-and-listeners)
    - [이벤트 자동 탐지](#event-discovery)
    - [이벤트 수동 등록](#manually-registering-events)
    - [클로저 리스너](#closure-listeners)
- [이벤트 정의](#defining-events)
- [리스너 정의](#defining-listeners)
- [큐잉되는 이벤트 리스너](#queued-event-listeners)
    - [큐 직접 제어하기](#manually-interacting-with-the-queue)
    - [큐잉 리스너와 데이터베이스 트랜잭션](#queued-event-listeners-and-database-transactions)
    - [실패한 작업 처리](#handling-failed-jobs)
- [이벤트 디스패치](#dispatching-events)
    - [데이터베이스 트랜잭션 이후 이벤트 디스패치](#dispatching-events-after-database-transactions)
- [이벤트 구독자](#event-subscribers)
    - [이벤트 구독자 작성](#writing-event-subscribers)
    - [이벤트 구독자 등록](#registering-event-subscribers)
- [테스트](#testing)
    - [일부 이벤트만 가짜로 처리](#faking-a-subset-of-events)
    - [범위 한정된 이벤트 가짜(fake)](#scoped-event-fakes)

<a name="introduction"></a>
## 소개

라라벨의 이벤트는 간단한 옵저버 패턴을 제공합니다. 이를 통해 애플리케이션에서 발생하는 다양한 이벤트에 구독하고, 해당 이벤트를 감지하여 처리할 수 있습니다. 이벤트 클래스는 보통 `app/Events` 디렉토리에, 해당 이벤트를 처리하는 리스너는 `app/Listeners` 디렉토리에 저장됩니다. 만약 이 디렉토리가 애플리케이션에 없다면, Artisan 콘솔 명령어로 이벤트와 리스너를 생성할 때 자동으로 만들어지므로 걱정하지 않으셔도 됩니다.

이벤트는 애플리케이션의 여러 부분을 느슨하게 결합할 수 있는 좋은 방법입니다. 하나의 이벤트에 여러 리스너를 연결할 수 있으며, 이 리스너들은 서로에게 의존하지 않습니다. 예를 들어, 주문이 발송될 때마다 사용자에게 Slack 알림을 보내고 싶다고 할 때, 주문 처리 코드와 Slack 알림 코드를 강하게 연결하지 않고, `App\Events\OrderShipped` 이벤트를 발생시키면, 리스너가 이를 받아 Slack 알림을 별도로 전송할 수 있습니다.

<a name="generating-events-and-listeners"></a>
## 이벤트 및 리스너 생성

이벤트와 리스너를 빠르게 생성하려면 `make:event` 및 `make:listener` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan make:event PodcastProcessed

php artisan make:listener SendPodcastNotification --event=PodcastProcessed
```

또한, 편의상 추가 인자 없이 `make:event`와 `make:listener` 명령어를 실행할 수도 있습니다. 이 경우 라라벨은 클래스명(리스너 생성 시에는 어떤 이벤트를 들을지)을 바로 입력받는 방식으로 안내해 줍니다.

```shell
php artisan make:event

php artisan make:listener
```

<a name="registering-events-and-listeners"></a>
## 이벤트 및 리스너 등록

<a name="event-discovery"></a>
### 이벤트 자동 탐지

기본적으로 라라벨은 애플리케이션의 `Listeners` 디렉토리를 스캔하여 리스너 클래스를 자동으로 찾아 등록합니다. 라라벨은 리스너 클래스에서 `handle` 또는 `__invoke`로 시작하는 메서드를 발견하면, 해당 메서드의 시그니처에 타입힌트 된 이벤트를 감지하여 이벤트 리스너로 등록합니다.

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

PHP의 유니언 타입을 사용하면 여러 이벤트에 동시에 리스닝할 수도 있습니다.

```php
/**
 * Handle the event.
 */
public function handle(PodcastProcessed|PodcastPublished $event): void
{
    // ...
}
```

리스너를 다른 디렉토리 또는 여러 디렉토리에 저장할 경우, 애플리케이션의 `bootstrap/app.php` 파일에서 `withEvents` 메서드를 사용해 해당 디렉토리들도 스캔하도록 지정할 수 있습니다.

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/Orders/Listeners',
])
```

유사한 여러 디렉토리를 동시에 스캔하려면 `*` 문자를 와일드카드로 사용할 수 있습니다.

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
#### 운영 환경에서의 이벤트 탐지

애플리케이션의 성능을 높이기 위해, `optimize` 또는 `event:cache` Artisan 명령어를 사용해 모든 리스너의 매니페스트를 캐싱하는 것이 좋습니다. 이 명령어는 보통 애플리케이션의 [배포 과정](/docs/12.x/deployment#optimization)에서 실행해야 합니다. 이 매니페스트는 프레임워크가 이벤트 등록 과정을 더 빠르게 처리하도록 도와줍니다. 만약 캐시를 삭제하고 싶다면 `event:clear` 명령어를 사용하면 됩니다.

<a name="manually-registering-events"></a>
### 이벤트 수동 등록

`Event` 파사드를 이용하여, 애플리케이션의 `AppServiceProvider`의 `boot` 메서드 내에서 특정 이벤트와 그에 대응하는 리스너를 수동으로 등록할 수도 있습니다.

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

`event:list` 명령어를 사용하면 애플리케이션에 등록된 모든 리스너를 확인할 수 있습니다.

```shell
php artisan event:list
```

<a name="closure-listeners"></a>
### 클로저 리스너

일반적으로 리스너는 클래스형으로 정의하지만, `AppServiceProvider`의 `boot` 메서드에서 클로저(익명 함수) 기반의 이벤트 리스너를 수동으로 등록할 수도 있습니다.

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
#### 큐잉되는 익명 이벤트 리스너

클로저 기반의 이벤트 리스너를 등록할 때, `Illuminate\Events\queueable` 함수를 사용해 해당 리스너를 [큐(queue)](/docs/12.x/queues)를 통해 실행하도록 지정할 수 있습니다.

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

일반적인 큐잉 작업처럼, `onConnection`, `onQueue`, `delay` 메서드를 사용해서 큐 리스너의 실행 방식을 자유롭게 지정할 수 있습니다.

```php
Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->onConnection('redis')->onQueue('podcasts')->delay(now()->addSeconds(10)));
```

익명 큐 리스너에서 실패 상황을 처리하고 싶다면, 리스너 정의 시 `catch` 메서드에 클로저를 전달할 수 있습니다. 이 클로저는 이벤트 인스턴스와 리스너의 실패를 유발한 `Throwable` 인스턴스를 전달받습니다.

```php
use App\Events\PodcastProcessed;
use function Illuminate\Events\queueable;
use Illuminate\Support\Facades\Event;
use Throwable;

Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->catch(function (PodcastProcessed $event, Throwable $e) {
    // The queued listener failed...
}));
```

<a name="wildcard-event-listeners"></a>
#### 와일드카드 이벤트 리스너

`*` 문자를 와일드카드 파라메터로 사용해 여러 이벤트를 하나의 리스너에서 동시에 감지할 수도 있습니다. 와일드카드 리스너는 첫 번째 인자로 이벤트 이름, 두 번째 인자로 전체 이벤트 데이터 배열을 전달받습니다.

```php
Event::listen('event.*', function (string $eventName, array $data) {
    // ...
});
```

<a name="defining-events"></a>
## 이벤트 정의

이벤트 클래스는 기본적으로 이벤트와 관련된 정보를 담는 데이터 컨테이너입니다. 예를 들어, `App\Events\OrderShipped` 이벤트가 [Eloquent ORM](/docs/12.x/eloquent) 객체를 받는다고 가정해보겠습니다.

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

보시다시피, 이 이벤트 클래스는 별도의 로직 없이 `App\Models\Order` 인스턴스만을 보관하는 그릇 역할을 합니다. 이벤트에서 사용하는 `SerializesModels` 트레이트는, PHP의 `serialize` 기능(예: [큐잉되는 리스너](#queued-event-listeners)를 사용할 때 등)으로 이벤트 객체를 직렬화할 경우, Eloquent 모델 관련 데이터를 안정적으로 직렬화해 줍니다.

<a name="defining-listeners"></a>
## 리스너 정의

다음은 예시 이벤트를 처리하는 리스너 코드입니다. 이벤트 리스너는 `handle` 메서드에서 이벤트 인스턴스를 전달받아 처리하게 됩니다. `make:listener` Artisan 명령어를 `--event` 옵션과 함께 사용하면, 자동으로 적절한 이벤트 클래스를 import하고, `handle` 메서드의 타입힌트도 적용해 줍니다. `handle` 메서드 내에서는 이벤트에 응답해야 할 모든 작업을 자유롭게 수행할 수 있습니다.

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
        // Access the order using $event->order...
    }
}
```

> [!NOTE]
> 이벤트 리스너의 생성자(constructor)에 의존성이 있다면 타입힌트로 지정할 수도 있습니다. 모든 이벤트 리스너는 라라벨 [서비스 컨테이너](/docs/12.x/container)를 통해 해석(resolve)되므로, 의존성은 자동으로 주입됩니다.

<a name="stopping-the-propagation-of-an-event"></a>
#### 이벤트 전파 중단하기

경우에 따라, 특정 리스너에서 이벤트의 추가 전파를 중단하고 싶을 수 있습니다. 이때 리스너의 `handle` 메서드에서 `false`를 반환하면 이벤트가 더 이상 다른 리스너에 전달되지 않습니다.

<a name="queued-event-listeners"></a>
## 큐잉되는 이벤트 리스너

이메일 전송이나 외부 HTTP 요청 등 시간이 오래 걸리는 작업을 리스너에서 수행해야 할 때, 해당 리스너를 큐잉하면 애플리케이션의 성능을 높일 수 있습니다. 큐잉되는 리스너를 사용하려면 먼저 [큐를 설정](/docs/12.x/queues)하고, 서버 또는 개발 환경에서 큐 워커를 실행해야 합니다.

리스너를 큐잉 대상으로 지정하려면, 리스너 클래스에 `ShouldQueue` 인터페이스를 구현하면 됩니다. `make:listener` Artisan 명령어로 리스너를 생성하면, 필요한 인터페이스 import가 이미 되어 있으므로 바로 사용할 수 있습니다.

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

이렇게 하면, 이 리스너가 처리하는 이벤트가 발생하면 라라벨의 [큐 시스템](/docs/12.x/queues)을 이용해 자동으로 리스너가 큐잉됩니다. 만약 리스너가 예외 없이 정상적으로 실행되면, 해당 큐 작업(job)은 처리 완료 후 자동으로 삭제됩니다.

<a name="customizing-the-queue-connection-queue-name"></a>
#### 큐 연결, 큐 이름, 딜레이(customizing delay) 설정

특정 리스너에 대해 큐 연결명, 큐 이름, 큐 작업의 대기 시간(딜레이)을 별도로 지정하고 싶을 때는 리스너 클래스에 `$connection`, `$queue`, `$delay` 속성을 정의하면 됩니다.

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

큐 연결명, 큐 이름, 대기 시간을 실행 시에 동적으로 지정하고 싶다면, 리스너에서 `viaConnection`, `viaQueue`, `withDelay` 메서드를 정의할 수 있습니다.

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
#### 조건부 큐잉 리스너

어떤 데이터를 기반으로 리스너를 큐잉할지 여부를 런타임에 동적으로 결정해야 하는 경우도 있습니다. 이럴 때는 리스너 클래스에 `shouldQueue` 메서드를 추가하여, 이 메서드가 `false`를 반환하면 해당 리스너가 큐잉되지 않습니다.

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
### 큐 직접 제어하기

리스너가 큐에서 실행될 때, 해당 큐 작업의 `delete`와 `release` 메서드를 직접 제어해야 할 수도 있습니다. 이를 위해 라라벨은 `Illuminate\Queue\InteractsWithQueue` 트레이트를 제공합니다. 이 트레이트는 Artisan 명령어로 생성된 리스너에 기본적으로 포함되어 있으며, 위 두 메서드에 간편하게 접근할 수 있습니다.

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

데이터베이스 트랜잭션 안에서 큐잉 리스너가 디스패치되면, 본래 트랜잭션이 완료(커밋)되기 전에 큐 워커가 리스너 처리를 시도할 수 있습니다. 이럴 경우, 트랜잭션 내부에서 모델이나 레코드를 변경했더라도 실제 반영이 되지 않은 상태에서 큐 리스너가 실행되어 문제가 발생할 수 있습니다. 특히, 트랜잭션 안에서만 생성된 모델이나 레코드는 아예 데이터베이스에 존재하지 않을 수도 있습니다. 리스너가 이러한 모델이나 데이터에 의존할 경우, 예상치 못한 에러가 발생할 수 있습니다.

만약 큐 연결의 `after_commit` 설정이 `false`일 때, 특정 큐잉 리스너만 트랜잭션 커밋 이후에 디스패치되도록 하고 싶다면, 그 리스너에 `ShouldQueueAfterCommit` 인터페이스를 구현하세요.

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
> 이러한 상황을 우회하는 방법에 대한 자세한 내용은 [큐 작업과 데이터베이스 트랜잭션](/docs/12.x/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="handling-failed-jobs"></a>
### 실패한 작업 처리

큐잉된 이벤트 리스너가 실패하는 경우가 있을 수 있습니다. 리스너가 큐 워커에서 지정한 최대 시도 횟수를 초과하면, 리스너의 `failed` 메서드가 호출됩니다. 이 메서드는 이벤트 인스턴스와 실패의 원인이 된 `Throwable` 객체를 인자로 받습니다.

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

큐잉된 리스너에서 오류가 반복적으로 발생하는 경우, 무한정 재시도하게 하고 싶지 않을 수 있습니다. 라라벨은 리스너가 최대 몇 번까지 재시도될지, 또는 얼마나 오랫동안 재시도될지를 지정할 수 있는 다양한 방법을 제공합니다.

가장 쉽게는 리스너 클래스에 `$tries` 속성을 정의해, 이 횟수를 초과하면 실패로 간주하도록 할 수 있습니다.

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

최대 시도 횟수 대신, 리스너를 더 이상 시도하지 않을 시간을 지정할 수도 있습니다. 이렇게 하면 그 시간 내에서는 무제한 시도하지만, 시간이 지나면 더 이상 시도하지 않습니다. 이를 위해 리스너 클래스에 `retryUntil` 메서드를 추가하면 됩니다. 이 메서드는 `DateTime` 인스턴스를 반환해야 합니다.

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

만약 `retryUntil`과 `tries`를 모두 지정했다면, 라라벨은 `retryUntil` 메서드를 우선적으로 사용합니다.

<a name="specifying-queued-listener-backoff"></a>
#### 큐 리스너 재시도 대기시간(backoff) 지정

리스너에서 예외가 발생했을 때, 재시도 전 대기할 초(seconds)를 설정하고 싶다면 리스너 클래스에 `backoff` 속성을 추가하면 됩니다.

```php
/**
 * The number of seconds to wait before retrying the queued listener.
 *
 * @var int
 */
public $backoff = 3;
```

더 복잡한 backoff 로직이 필요하다면, 리스너 클래스에 `backoff` 메서드를 정의할 수도 있습니다.

```php
/**
 * Calculate the number of seconds to wait before retrying the queued listener.
 */
public function backoff(): int
{
    return 3;
}
```

"지수(backoff) 방식" 대기시간을 손쉽게 설정하려면, `backoff` 메서드에서 backoff 값의 배열을 반환하면 됩니다. 예를 들어, 첫 번째 재시도는 1초, 두 번째는 5초, 세 번째는 10초, 이후는 모두 10초로 대기합니다.

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

이벤트를 디스패치(발생)하려면, 해당 이벤트에서 정적 `dispatch` 메서드를 호출하면 됩니다. 이 메서드는 `Illuminate\Foundation\Events\Dispatchable` 트레이트에 의해 제공됩니다. `dispatch` 메서드에 전달한 모든 인수는 이벤트의 생성자로 전달됩니다.

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

특정 조건이 충족될 때만 이벤트를 디스패치하고 싶다면, `dispatchIf` 또는 `dispatchUnless` 메서드를 사용할 수 있습니다.

```php
OrderShipped::dispatchIf($condition, $order);

OrderShipped::dispatchUnless($condition, $order);
```

> [!NOTE]
> 테스트 시, 실제로 리스너를 트리거하지 않고 특정 이벤트가 디스패치되었는지 검증하고 싶을 수 있습니다. 라라벨의 [내장 테스트 헬퍼](#testing)를 사용하면 이를 쉽게 할 수 있습니다.

<a name="dispatching-events-after-database-transactions"></a>
### 데이터베이스 트랜잭션 이후에 이벤트 디스패치하기

경우에 따라, 현재 활성화된 데이터베이스 트랜잭션이 커밋된 후에만 이벤트를 발생시키고 싶을 수 있습니다. 이럴 때는 해당 이벤트 클래스에 `ShouldDispatchAfterCommit` 인터페이스를 구현하면 됩니다.

이 인터페이스를 사용하면 라라벨은 현재 진행 중인 데이터베이스 트랜잭션이 커밋되기 전까지 이벤트를 디스패치하지 않습니다. 트랜잭션이 실패하면 이벤트도 폐기됩니다. 만약 이벤트가 디스패치될 때 진행 중인 트랜잭션이 없다면, 이벤트는 즉시 디스패치됩니다.

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
## 이벤트 서브스크라이버

<a name="writing-event-subscribers"></a>
### 이벤트 서브스크라이버 작성하기

이벤트 서브스크라이버는 하나의 클래스 안에서 여러 이벤트를 구독(가입)할 수 있는 클래스입니다. 즉, 단일 클래스 내에 여러 이벤트 핸들러를 정의할 수 있습니다. 서브스크라이버 클래스는 반드시 `subscribe` 메서드를 정의해야 하며, 이 메서드는 이벤트 디스패처 인스턴스를 인자로 받습니다. 전달받은 디스패처의 `listen` 메서드를 사용해 이벤트 리스너를 등록할 수 있습니다.

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

이벤트 리스너 메서드가 서브스크라이버 내부에 정의되어 있다면, `subscribe` 메서드에서 이벤트와 메서드 명의 배열을 반환하는 방식도 사용할 수 있습니다. 라라벨은 이벤트 리스너를 등록할 때 자동으로 해당 서브스크라이버의 클래스명을 사용합니다.

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
### 이벤트 서브스크라이버 등록하기

서브스크라이버를 작성한 후, 이벤트와 리스너가 라라벨의 [이벤트 자동 탐색 규칙](#event-discovery)에 맞게 작성되어 있다면 라라벨이 자동으로 핸들러 메서드를 등록합니다. 그렇지 않다면, `Event` 파사드의 `subscribe` 메서드를 호출하여 직접 서브스크라이버를 등록할 수 있습니다. 일반적으로 이 작업은 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드에서 수행합니다.

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
## 테스트하기

이벤트를 디스패치하는 코드를 테스트할 때, 실제로 리스너의 코드가 실행되지 않도록 하고 싶을 수 있습니다. 리스너의 코드는 따로(직접) 테스트할 수 있기 때문에, 이벤트만 올바로 발생하는지 분리해서 검증하고 싶을 때 유용합니다. 리스너 자체를 테스트하고 싶다면, 리스너 인스턴스를 생성하여 직접 `handle` 메서드를 테스트에서 호출하면 됩니다.

`Event` 파사드의 `fake` 메서드를 사용하면, 리스너의 실행을 방지한 상태로 테스트하고, 그 후 `assertDispatched`, `assertNotDispatched`, `assertNothingDispatched`와 같은 메서드로 애플리케이션에서 어떤 이벤트가 발생했는지 확인할 수 있습니다.

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

`assertDispatched` 또는 `assertNotDispatched` 메서드에 클로저를 전달하면 "진위 테스트(truth test)"를 통과하는 이벤트가 디스패치되었는지 검증할 수 있습니다. 조건을 만족하는 이벤트가 하나라도 디스패치되었다면 검증은 성공합니다.

```php
Event::assertDispatched(function (OrderShipped $event) use ($order) {
    return $event->order->id === $order->id;
});
```

특정 이벤트에 대해 이벤트 리스너가 등록되어 있는지 검증하고 싶다면, `assertListening` 메서드를 사용할 수 있습니다.

```php
Event::assertListening(
    OrderShipped::class,
    SendShipmentNotification::class
);
```

> [!WARNING]
> `Event::fake()`를 호출한 이후에는 이벤트 리스너가 실행되지 않습니다. 따라서, 모델의 `creating` 이벤트에서 UUID를 생성하는 것과 같이 이벤트에 의존하는 팩토리를 테스트에서 사용한다면, 팩토리를 사용한 **이후에** `Event::fake()`를 호출해야 합니다.

<a name="faking-a-subset-of-events"></a>
### 일부 이벤트에 대해서만 이벤트 페이크하기

특정 이벤트에 대해서만 리스너의 실행을 막고 싶다면, `fake` 또는 `fakeFor` 메서드에 해당 이벤트들을 전달하면 됩니다.

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

`except` 메서드를 사용하면, 지정한 이벤트를 제외하고 나머지 모든 이벤트에 대해 페이크를 적용할 수 있습니다.

```php
Event::fake()->except([
    OrderCreated::class,
]);
```

<a name="scoped-event-fakes"></a>
### 범위 지정 이벤트 페이크

테스트의 일부 구간에만 리스너 실행을 막고 싶다면, `fakeFor` 메서드를 사용할 수 있습니다.

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