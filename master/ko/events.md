# 이벤트 (Events)

- [소개](#introduction)
- [이벤트 및 리스너 생성](#generating-events-and-listeners)
- [이벤트 및 리스너 등록](#registering-events-and-listeners)
    - [이벤트 자동 감지](#event-discovery)
    - [이벤트 수동 등록](#manually-registering-events)
    - [클로저 리스너](#closure-listeners)
- [이벤트 정의](#defining-events)
- [리스너 정의](#defining-listeners)
- [큐잉된 이벤트 리스너](#queued-event-listeners)
    - [큐 수동 제어](#manually-interacting-with-the-queue)
    - [큐잉된 리스너와 데이터베이스 트랜잭션](#queued-event-listeners-and-database-transactions)
    - [큐 리스너 미들웨어](#queued-listener-middleware)
    - [암호화된 큐 리스너](#encrypted-queued-listeners)
    - [실패한 작업 처리](#handling-failed-jobs)
- [이벤트 디스패치](#dispatching-events)
    - [데이터베이스 트랜잭션 이후 이벤트 디스패치](#dispatching-events-after-database-transactions)
    - [이벤트 지연 디스패치](#deferring-events)
- [이벤트 구독자](#event-subscribers)
    - [이벤트 구독자 작성](#writing-event-subscribers)
    - [이벤트 구독자 등록](#registering-event-subscribers)
- [테스트](#testing)
    - [일부 이벤트 페이크 처리](#faking-a-subset-of-events)
    - [범위 지정 이벤트 페이크](#scoped-event-fakes)

<a name="introduction"></a>
## 소개

Laravel의 이벤트 시스템은 간단한 옵저버 패턴(observer pattern) 구현을 제공하여, 애플리케이션 내부에서 발생하는 다양한 이벤트에 구독(subscribe)하고 리스닝(listen)할 수 있도록 해줍니다. 이벤트 클래스는 보통 `app/Events` 디렉터리에, 해당 리스너(listener)는 `app/Listeners` 디렉터리에 저장됩니다. 만약 애플리케이션에 이 디렉터리가 없다면, Artisan 콘솔 명령어로 이벤트 및 리스너를 생성할 때 자동으로 만들어집니다.

이벤트는 애플리케이션의 여러 부분을 느슨하게 결합(loose coupling)하는 훌륭한 방법입니다. 하나의 이벤트는 서로 의존하지 않는 여러 리스너를 가질 수 있습니다. 예를 들어, 주문이 배송될 때마다 사용자의 Slack(슬랙)으로 알림을 전송하고 싶다고 가정해 봅시다. 주문 처리 코드에 직접 Slack 알림 코드를 결합하지 않고, `App\Events\OrderShipped` 이벤트를 발생시킨 뒤, 리스너가 이 이벤트를 받아서 Slack 알림을 전송하도록 만들 수 있습니다.

<a name="generating-events-and-listeners"></a>
## 이벤트 및 리스너 생성

이벤트와 리스너를 빠르게 생성하려면 `make:event` 및 `make:listener` Artisan 명령어를 사용할 수 있습니다:

```shell
php artisan make:event PodcastProcessed

php artisan make:listener SendPodcastNotification --event=PodcastProcessed
```

편의상 추가 인수 없이 `make:event`와 `make:listener` 명령어를 실행할 수도 있습니다. 이 경우, Laravel이 클래스명(및 리스너 생성 시 리스닝할 이벤트)을 직접 입력받도록 안내해줍니다:

```shell
php artisan make:event

php artisan make:listener
```

<a name="registering-events-and-listeners"></a>
## 이벤트 및 리스너 등록

<a name="event-discovery"></a>
### 이벤트 자동 감지

기본적으로 Laravel은 애플리케이션의 `Listeners` 디렉터리를 스캔하여 이벤트 리스너를 자동으로 찾고 등록합니다. 리스너 클래스 내에서 `handle` 또는 `__invoke`로 시작하는 메서드가 있다면, 해당 메서드의 시그니처에서 타입힌트된 이벤트에 관한 리스너로 자동 등록됩니다:

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

PHP의 유니언 타입을 사용하여 여러 이벤트를 리스닝할 수도 있습니다:

```php
/**
 * Handle the event.
 */
public function handle(PodcastProcessed|PodcastPublished $event): void
{
    // ...
}
```

리스너를 다른 디렉터리나 여러 디렉터리에 저장하려면, `bootstrap/app.php` 파일의 `withEvents` 메서드를 사용하여 Laravel이 해당 디렉터리도 스캔하도록 지정할 수 있습니다:

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/Orders/Listeners',
])
```

유사한 여러 디렉터리를 스캔하려면 `*` 와일드카드를 사용할 수 있습니다:

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/*/Listeners',
])
```

`event:list` 명령어를 통해 현재 애플리케이션에 등록된 모든 리스너를 조회할 수 있습니다:

```shell
php artisan event:list
```

<a name="event-discovery-in-production"></a>
#### 운영 환경에서의 이벤트 감지

애플리케이션 성능을 높이기 위해, `optimize` 또는 `event:cache` Artisan 명령어를 사용하여 모든 리스너 목록을 캐시해두는 것이 좋습니다. 보통 이 명령어는 애플리케이션의 [배포 프로세스](/docs/master/deployment#optimization)에서 실행합니다. 이 매니페스트 파일은 이벤트 등록 속도를 높이기 위해 프레임워크에서 사용됩니다. `event:clear` 명령어는 이벤트 캐시를 삭제하는 데 사용합니다.

<a name="manually-registering-events"></a>
### 이벤트 수동 등록

`Event` 파사드를 사용해, 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 이벤트와 해당 리스너를 수동으로 등록할 수 있습니다:

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

`event:list` 명령어로 현재 애플리케이션에 등록된 모든 리스너를 볼 수 있습니다:

```shell
php artisan event:list
```

<a name="closure-listeners"></a>
### 클로저 리스너

일반적으로 리스너는 클래스 형태로 정의하지만, 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 클로저(익명 함수) 기반의 이벤트 리스너도 수동으로 등록할 수 있습니다:

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
#### 큐잉 가능한 익명 이벤트 리스너

클로저 기반 리스너 등록 시, `Illuminate\Events\queueable` 함수를 사용해 해당 리스너를 [큐](/docs/master/queues)를 통해 실행하도록 지정할 수 있습니다:

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

큐잉되는 작업처럼, `onConnection`, `onQueue`, `delay` 메서드로 큐 연결, 큐 이름, 지연 시간 등을 지정할 수 있습니다:

```php
Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->onConnection('redis')->onQueue('podcasts')->delay(now()->plus(seconds: 10)));
```

익명 큐 리스너 실행 시 실패 처리를 위해, `queueable` 리스너 정의 시 `catch` 메서드에 클로저를 전달할 수 있습니다. 이 클로저는 이벤트 인스턴스와 실패 원인이 된 `Throwable` 인스턴스를 받게 됩니다:

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

`*` 와일드카드 파라미터를 사용해서 리스너를 등록할 수도 있습니다. 와일드카드 리스너는 동일한 리스너에서 여러 이벤트를 한 번에 수신할 수 있습니다. 이때, 첫 번째 인자는 이벤트명, 두 번째 인자는 이벤트 데이터 배열이 전달됩니다:

```php
Event::listen('event.*', function (string $eventName, array $data) {
    // ...
});
```

<a name="defining-events"></a>
## 이벤트 정의

이벤트 클래스는 기본적으로 해당 이벤트와 관련된 정보를 담는 데이터 컨테이너입니다. 예를 들어, `App\Events\OrderShipped` 이벤트가 [Eloquent ORM](/docs/master/eloquent) 객체를 받는 경우는 다음과 같습니다:

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

이벤트 클래스에는 별도의 로직이 없습니다. 단지 구매된 `App\Models\Order` 인스턴스를 담는 컨테이너 역할일 뿐입니다. 이벤트에서 사용하는 `SerializesModels` 트레이트(trait)는 이벤트가 PHP의 `serialize` 함수로 직렬화될 때(예: [큐잉된 리스너](#queued-event-listeners) 활용 시) Eloquent 모델을 안전하게 직렬화해줍니다.

<a name="defining-listeners"></a>
## 리스너 정의

이제 예제 이벤트에 대한 리스너를 살펴봅시다. 리스너는 `handle` 메서드에서 이벤트 인스턴스를 전달받습니다. `make:listener` Artisan 명령어를 `--event` 옵션과 함께 사용하면, 적절한 이벤트 클래스를 자동으로 import 하고, `handle` 메서드에 타입힌트를 추가합니다. `handle` 메서드 내에서, 이벤트에 대응하는 로직을 자유롭게 구현할 수 있습니다:

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
> 이벤트 리스너는 생성자에서 필요한 의존성을 타입힌트로 지정할 수 있습니다. 모든 이벤트 리스너는 Laravel [서비스 컨테이너](/docs/master/container)를 통해 해석되므로, 의존성은 자동으로 주입됩니다.

<a name="stopping-the-propagation-of-an-event"></a>
#### 이벤트 전파 중단

경우에 따라, 해당 이벤트의 전파를 다른 리스너에게 전달하지 않고 중단하고 싶을 수 있습니다. 이를 위해 리스너의 `handle` 메서드에서 `false`를 반환하면 전파가 멈춥니다.

<a name="queued-event-listeners"></a>
## 큐잉된 이벤트 리스너

리스너가 이메일 발송, HTTP 요청 등 느린 작업을 수행해야 할 때는 큐잉하는 것이 효과적입니다. 큐잉된 리스너를 사용하기 전에 [큐 설정](/docs/master/queues)을 완료하고, 서버 또는 로컬 개발 환경에서 큐 워커(queue worker)가 실행 중이어야 합니다.

리스너가 큐잉되어야 함을 명시하려면, 해당 클래스에 `ShouldQueue` 인터페이스를 구현합니다. `make:listener` Artisan 명령어로 생성한 리스너라면 이미 이 인터페이스가 import되어 있으므로 바로 사용할 수 있습니다:

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

이제 이 리스너가 처리하는 이벤트가 디스패치될 때, Laravel [큐 시스템](/docs/master/queues)에 의해 자동으로 큐잉됩니다. 큐에서 리스너가 예외 없이 실행되면, 해당 큐 작업은 자동으로 삭제됩니다.

<a name="customizing-the-queue-connection-queue-name"></a>
#### 큐 연결, 이름, 지연 시간 커스터마이징

이벤트 리스너의 큐 연결(connection), 큐 이름(queue), 큐 지연 시간(delay) 등을 지정하려면 클래스의 `$connection`, `$queue`, `$delay` 프로퍼티를 정의하세요:

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

런타임에 큐 연결, 이름, 지연 시간을 동적으로 정의하고 싶다면, `viaConnection`, `viaQueue`, `withDelay` 메서드를 리스너에 추가할 수 있습니다:

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
#### 조건부 리스너 큐잉

런타임에서 특정 데이터에 따라 리스너를 큐잉할지 결정해야 할 경우가 있습니다. 이를 지원하기 위해, 리스너에 `shouldQueue` 메서드를 추가하면 됩니다. 만약 이 메서드가 `false`를 반환하면 해당 리스너는 큐잉되지 않습니다:

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
### 큐 수동 제어

리스너의 내부 큐 작업의 `delete` 및 `release` 메서드를 직접 사용해야 할 경우, `Illuminate\Queue\InteractsWithQueue` 트레이트를 통해 접근할 수 있습니다. 이 트레이트는 생성된 리스너에 기본적으로 import되어 있으며, 관련 메서드 사용을 제공합니다:

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
        if ($condition) {
            $this->release(30);
        }
    }
}
```

<a name="queued-event-listeners-and-database-transactions"></a>
### 큐잉된 리스너와 데이터베이스 트랜잭션

큐잉된 리스너가 데이터베이스 트랜잭션 내에서 디스패치될 경우, 트랜잭션이 커밋되기 전에 큐에서 처리될 수 있습니다. 이 경우, 트랜잭션 내에서 수행된 모델 또는 레코드의 변경 사항이 아직 데이터베이스에 반영되지 않은 상태일 수 있으며, 트랜잭션 내에서 새로 생성된 모델/레코드는 아직 존재하지 않을 수 있습니다. 만약 리스너가 이러한 모델에 의존한다면, 예기치 않은 오류가 발생할 수 있습니다.

큐 연결의 `after_commit` 설정이 `false`인 경우에도, 리스너 클래스에 `ShouldQueueAfterCommit` 인터페이스를 구현하면, 해당 리스너가 열린 모든 데이터베이스 트랜잭션 커밋 이후에 디스패치되도록 할 수 있습니다:

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
> 이와 관련된 자세한 내용은 [큐 작업 및 데이터베이스 트랜잭션](/docs/master/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="queued-listener-middleware"></a>
### 큐 리스너 미들웨어

큐로 실행되는 리스너는 [작업 미들웨어](/docs/master/queues#job-middleware)를 사용할 수 있습니다. 작업 미들웨어는 리스너의 실행을 커스텀 로직으로 감싸 불필요한 반복 코드(보일러플레이트)를 줄여줍니다. 작업 미들웨어를 만든 후, 리스너의 `middleware` 메서드에서 이를 반환하면 연결됩니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use App\Jobs\Middleware\RateLimited;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    /**
     * Handle the event.
     */
    public function handle(OrderShipped $event): void
    {
        // Process the event...
    }

    /**
     * Get the middleware the listener should pass through.
     *
     * @return array<int, object>
     */
    public function middleware(OrderShipped $event): array
    {
        return [new RateLimited];
    }
}
```

<a name="encrypted-queued-listeners"></a>
#### 암호화된 큐 리스너

큐에 저장되는 리스너의 데이터의 프라이버시와 무결성을 보장하기 위해 [암호화](/docs/master/encryption)를 사용할 수 있습니다. `ShouldBeEncrypted` 인터페이스를 리스너 클래스에 추가하면, 해당 리스너는 큐에 저장될 때 자동으로 암호화됩니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldBeEncrypted;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue, ShouldBeEncrypted
{
    // ...
}
```

<a name="handling-failed-jobs"></a>
### 실패한 작업 처리

큐잉된 이벤트 리스너가 실패할 때가 있습니다. 만약 큐 리스너가 큐 워커에 정의된 최대 시도 횟수를 넘어서면, 리스너의 `failed` 메서드가 호출됩니다. 이 메서드는 이벤트 인스턴스와, 실패를 일으킨 `Throwable` 객체를 전달받습니다:

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

큐잉된 리스너에서 오류가 발생한다면, 무한정 재시도하는 것을 원치 않을 것입니다. Laravel은 리스너가 실패 전 몇 번이나 혹은 얼마동안 시도될 수 있는지 여러 방법을 제공합니다.

리스너 클래스에서 `tries` 프로퍼티 또는 메서드를 정의해, 실패 전 허용되는 최대 시도 횟수를 지정할 수 있습니다:

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

실패까지의 횟수 대신, 리스너가 더이상 재시도되지 않아야 하는 시점을 지정할 수도 있습니다. 이를 위해 `retryUntil` 메서드를 추가하여, 시도될 수 있는 마지막 시각을 `DateTime` 객체로 반환하면 됩니다:

```php
use DateTime;

/**
 * Determine the time at which the listener should timeout.
 */
public function retryUntil(): DateTime
{
    return now()->plus(minutes: 5);
}
```

`retryUntil`과 `tries`가 모두 정의되어 있다면, Laravel은 `retryUntil` 메서드를 우선합니다.

<a name="specifying-queued-listener-backoff"></a>
#### 큐 리스너 재시도 대기(backoff) 지정

리스너가 예외를 만난 후 재시도 전 몇 초를 대기할지 지정하려면 `backoff` 프로퍼티를 클래스에 추가하세요:

```php
/**
 * The number of seconds to wait before retrying the queued listener.
 *
 * @var int
 */
public $backoff = 3;
```

더 복잡한 backoff 로직이 필요하다면, `backoff` 메서드를 클래스에 정의할 수 있습니다:

```php
/**
 * Calculate the number of seconds to wait before retrying the queued listener.
 */
public function backoff(OrderShipped $event): int
{
    return 3;
}
```

"지수(backoff)" 증가 방식으로 재시도 지연을 설정하고 싶으면, `backoff` 메서드에서 배열을 반환하면 됩니다. 아래 예시에서는 첫 번째 재시도 시 1초 대기, 두 번째 재시도 시 5초, 세 번째 및 그 이후는 10초씩 대기합니다:

```php
/**
 * Calculate the number of seconds to wait before retrying the queued listener.
 *
 * @return list<int>
 */
public function backoff(OrderShipped $event): array
{
    return [1, 5, 10];
}
```

<a name="specifying-queued-listener-max-exceptions"></a>
#### 큐 리스너 최대 예외 횟수 지정

경우에 따라, 큐 리스너가 많은 횟수(try)로 시도하도록 하되, 직접 `release` 메서드로 해제한 경우가 아닌, 정의된 비처리 예외가 일정 횟수 이상 발생하면 실패 처리하고 싶을 수 있습니다. 이를 위해 `maxExceptions` 프로퍼티를 정의하면 됩니다:

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
    public $tries = 25;

    /**
     * The maximum number of unhandled exceptions to allow before failing.
     *
     * @var int
     */
    public $maxExceptions = 3;

    /**
     * Handle the event.
     */
    public function handle(OrderShipped $event): void
    {
        // Process the event...
    }
}
```

이 예시에서, 리스너는 최대 25번까지 재시도되지만, 3번의 비처리 예외가 발생하면 즉시 실패 처리됩니다.

<a name="specifying-queued-listener-timeout"></a>
#### 큐 리스너 실행 제한 시간(timeout) 지정

보통 큐 리스너가 예상보다 오래 걸릴 경우를 대비해 실행 제한 시간을 지정할 수 있습니다. 지정한 제한 시간(초)보다 길게 실행되면, 해당 리스너를 처리 중인 워커가 오류와 함께 종료됩니다. 제한 시간은 클래스 내 `timeout` 프로퍼티로 지정합니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    /**
     * The number of seconds the listener can run before timing out.
     *
     * @var int
     */
    public $timeout = 120;
}
```

timeout 발생 시 리스너를 실패로 표시하려면, `failOnTimeout` 프로퍼티를 클래스에 정의하세요:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    /**
     * Indicate if the listener should be marked as failed on timeout.
     *
     * @var bool
     */
    public $failOnTimeout = true;
}
```

<a name="dispatching-events"></a>
## 이벤트 디스패치

이벤트를 디스패치하려면, 이벤트 클래스의 static `dispatch` 메서드를 호출하면 됩니다. 이 메서드는 이벤트의 `Illuminate\Foundation\Events\Dispatchable` 트레이트에서 제공됩니다. `dispatch` 메서드에 전달된 인수는 이벤트의 생성자에 그대로 넘어갑니다:

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

조건부로 이벤트를 디스패치하려면 `dispatchIf`, `dispatchUnless` 메서드를 사용하세요:

```php
OrderShipped::dispatchIf($condition, $order);

OrderShipped::dispatchUnless($condition, $order);
```

> [!NOTE]
> 테스트 시, 리스너를 실제로 실행하지 않고도 어떤 이벤트가 디스패치되었는지 검증할 수 있습니다. Laravel의 [내장 테스트 헬퍼](#testing)를 활용하세요.

<a name="dispatching-events-after-database-transactions"></a>
### 데이터베이스 트랜잭션 이후 이벤트 디스패치

경우에 따라, 현재 데이터베이스 트랜잭션이 커밋된 이후에만 이벤트가 디스패치되길 원할 수 있습니다. 이럴 때 이벤트 클래스에 `ShouldDispatchAfterCommit` 인터페이스를 구현하세요.

이 인터페이스는 이벤트가 현재 트랜잭션이 커밋되기 전까지 디스패치되지 않게 만듭니다. 트랜잭션이 실패하면 이벤트도 폐기됩니다. 만약 트랜잭션이 없는 경우에는 이벤트가 즉시 디스패치됩니다:

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

<a name="deferring-events"></a>
### 이벤트 지연 디스패치

지연(deferred) 이벤트를 사용하면 특정 코드 블록이 모두 완료된 이후 모델 이벤트 디스패치 및 리스너 실행을 늦출 수 있습니다. 이 방식은 관련된 모든 레코드가 생성된 뒤에 리스너가 실행되도록 보장해야 할 때 매우 유용합니다.

이벤트를 지연시키려면, `Event::defer()` 메서드에 클로저를 전달하면 됩니다:

```php
use App\Models\User;
use Illuminate\Support\Facades\Event;

Event::defer(function () {
    $user = User::create(['name' => 'Victoria Otwell']);

    $user->posts()->create(['title' => 'My first post!']);
});
```

클로저 내에서 발생한 모든 이벤트는 클로저 실행 후에 디스패치됩니다. 이를 통해, 지연된 실행 동안 생성된 모든 관련 레코드를 이벤트 리스너에서 안전하게 처리할 수 있습니다. 만약 클로저 실행 중 예외가 발생하면, 지연된 이벤트는 디스패치되지 않습니다.

특정 이벤트만 지연 처리하고 싶다면, 두 번째 인수로 이벤트 배열을 `defer` 메서드에 전달하세요:

```php
use App\Models\User;
use Illuminate\Support\Facades/Event;

Event::defer(function () {
    $user = User::create(['name' => 'Victoria Otwell']);

    $user->posts()->create(['title' => 'My first post!']);
}, ['eloquent.created: '.User::class]);
```

<a name="event-subscribers"></a>
## 이벤트 구독자

<a name="writing-event-subscribers"></a>
### 이벤트 구독자 작성

이벤트 구독자(subscriber)는 여러 이벤트를 한 클래스 안에서 구독(subscribe)할 수 있게 해줍니다. 이로써 하나의 클래스 내에 여러 이벤트 핸들러를 정의할 수 있습니다. 구독자는 `subscribe` 메서드를 정의해야 하며, 이 메서드는 이벤트 디스패처 인스턴스를 받습니다. 주어진 디스패처의 `listen` 메서드로 이벤트 리스너를 등록할 수 있습니다:

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

리스너 메서드가 구독자 클래스 내부에 정의되어 있을 경우, `subscribe` 메서드에서 이벤트와 메서드 이름의 배열을 반환하는 방식이 더욱 편리할 수 있습니다. Laravel은 리스너 등록시 자동으로 구독자의 클래스명을 인식합니다:

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
### 이벤트 구독자 등록

구독자를 작성한 후, 구독자 메서드가 Laravel의 [이벤트 감지 규칙](#event-discovery)을 따르고 있다면 자동으로 핸들러가 등록됩니다. 그렇지 않은 경우 `Event` 파사드의 `subscribe` 메서드를 사용하여 수동으로 등록할 수 있습니다. 보통 이 작업은 애플리케이션의 `AppServiceProvider`의 `boot` 메서드 내에서 수행합니다:

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

이벤트를 디스패치하는 코드를 테스트할 때, 실제로 이벤트 리스너를 실행하지 않도록 하면서도 한편으로 어떤 이벤트가 디스패치되었는지 검증하고 싶을 수 있습니다. 리스너의 코드는 개별적으로 테스트할 수 있으므로, 해당 이벤트의 `handle` 메서드를 테스트에서 직접 호출해도 무방합니다.

`Event` 파사드의 `fake` 메서드를 사용하면, 리스너의 실행을 막고 테스트하려는 코드를 실행한 뒤, `assertDispatched`, `assertNotDispatched`, `assertNothingDispatched` 메서드로 어떤 이벤트가 디스패치되었는지 검증할 수 있습니다:

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

    // Assert an event was dispatched once...
    Event::assertDispatchedOnce(OrderShipped::class);

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

        // Assert an event was dispatched once...
        Event::assertDispatchedOnce(OrderShipped::class);

        // Assert an event was not dispatched...
        Event::assertNotDispatched(OrderFailedToShip::class);

        // Assert that no events were dispatched...
        Event::assertNothingDispatched();
    }
}
```

`assertDispatched` 또는 `assertNotDispatched` 메서드에 클로저를 전달하여, 특정 조건을 만족하는 이벤트가 디스패치되었는지 "진위 테스트(true test)"를 할 수 있습니다. 조건을 만족하는 이벤트가 하나라도 존재하면 검증에 성공합니다:

```php
Event::assertDispatched(function (OrderShipped $event) use ($order) {
    return $event->order->id === $order->id;
});
```

특정 이벤트에 대해 지정한 리스너가 실제로 리스닝 중인지 검증하려면, `assertListening` 메서드를 사용할 수 있습니다:

```php
Event::assertListening(
    OrderShipped::class,
    SendShipmentNotification::class
);
```

> [!WARNING]
> `Event::fake()`를 호출하면 리스너가 실행되지 않습니다. 따라서, 이벤트에 의존하는 UUID 생성 등 모델 팩토리를 사용하는 테스트에서는 팩토리 사용 후에 `Event::fake()`를 호출해야 합니다.

<a name="faking-a-subset-of-events"></a>
### 일부 이벤트 페이크 처리

특정 이벤트에 대해서만 리스너 실행을 페이크로 처리하고 싶다면, 해당 이벤트들을 `fake` 또는 `fakeFor` 메서드에 전달하세요:

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

특정 이벤트만 빼고 나머지 모든 이벤트를 페이크 처리하고 싶다면, `except` 메서드를 사용할 수 있습니다:

```php
Event::fake()->except([
    OrderCreated::class,
]);
```

<a name="scoped-event-fakes"></a>
### 범위 지정 이벤트 페이크

테스트의 일부 코드 블록에 대해서만 이벤트 리스너 실행을 페이크 처리하려면, `fakeFor` 메서드를 사용하세요:

```php tab=Pest
<?php

use App\Events\OrderCreated;
use App\Models\Order;
use Illuminate\Support\Facades/Event;

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
