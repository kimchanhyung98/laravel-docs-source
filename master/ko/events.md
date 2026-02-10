# 이벤트 (Events)

- [소개](#introduction)
- [이벤트 및 리스너 생성](#generating-events-and-listeners)
- [이벤트 및 리스너 등록](#registering-events-and-listeners)
    - [이벤트 자동 감지](#event-discovery)
    - [이벤트 수동 등록](#manually-registering-events)
    - [클로저 리스너](#closure-listeners)
- [이벤트 정의하기](#defining-events)
- [리스너 정의하기](#defining-listeners)
- [큐잉된 이벤트 리스너](#queued-event-listeners)
    - [큐 직접 다루기](#manually-interacting-with-the-queue)
    - [큐잉 리스너와 데이터베이스 트랜잭션](#queued-event-listeners-and-database-transactions)
    - [큐잉 리스너 미들웨어](#queued-listener-middleware)
    - [암호화된 큐잉 리스너](#encrypted-queued-listeners)
    - [고유 이벤트 리스너](#unique-event-listeners)
    - [실패한 작업 처리](#handling-failed-jobs)
- [이벤트 디스패치](#dispatching-events)
    - [데이터베이스 트랜잭션 이후 이벤트 디스패치](#dispatching-events-after-database-transactions)
    - [이벤트 지연 디스패치](#deferring-events)
- [이벤트 구독자](#event-subscribers)
    - [이벤트 구독자 작성](#writing-event-subscribers)
    - [이벤트 구독자 등록](#registering-event-subscribers)
- [테스트](#testing)
    - [일부 이벤트만 페이크 사용](#faking-a-subset-of-events)
    - [스코프가 지정된 이벤트 페이크](#scoped-event-fakes)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel의 이벤트는 간단한 옵저버 패턴을 구현하여, 애플리케이션 내에서 발생하는 다양한 이벤트에 구독(Subscribe)하고 리스닝(Listen)할 수 있도록 합니다. 이벤트 클래스는 보통 `app/Events` 디렉토리에, 해당 이벤트의 리스너는 `app/Listeners` 디렉토리에 위치합니다. 만약 애플리케이션에서 이 디렉토리가 보이지 않는다면 걱정하지 않아도 됩니다. Artisan 콘솔 명령어로 이벤트와 리스너를 생성할 때 자동으로 생성됩니다.

이벤트는 애플리케이션의 다양한 부분을 느슨하게 결합할 수 있는 훌륭한 방법입니다. 하나의 이벤트에 여러 리스너가 연결될 수 있고, 이들은 서로 독립적으로 동작합니다. 예를 들어, 주문이 배송될 때마다 사용자의 Slack에 알림을 보내고 싶다면, 주문 처리 코드와 Slack 알림 코드를 직접 연결하는 대신, `App\Events\OrderShipped` 이벤트를 발생시키고, 해당 이벤트를 받아 Slack 알림을 보내는 리스너를 만들 수 있습니다.

<a name="generating-events-and-listeners"></a>
## 이벤트 및 리스너 생성 (Generating Events and Listeners)

이벤트와 리스너를 빠르게 생성하려면 `make:event`와 `make:listener` Artisan 명령어를 사용할 수 있습니다:

```shell
php artisan make:event PodcastProcessed

php artisan make:listener SendPodcastNotification --event=PodcastProcessed
```

더 편리하게, 추가 인자 없이 `make:event`나 `make:listener` Artisan 명령어를 실행할 수도 있습니다. 이 경우, Laravel이 클래스 이름을 입력받고, 리스너 생성시 어떤 이벤트를 감지할 것인지도 물어봅니다:

```shell
php artisan make:event

php artisan make:listener
```

<a name="registering-events-and-listeners"></a>
## 이벤트 및 리스너 등록 (Registering Events and Listeners)

<a name="event-discovery"></a>
### 이벤트 자동 감지 (Event Discovery)

Laravel은 기본적으로 애플리케이션의 `Listeners` 디렉토리를 스캔하여 이벤트 리스너를 자동으로 감지하고 등록합니다. Laravel은 `handle` 또는 `__invoke`로 시작하는 메서드가 있으며, 해당 메서드의 시그니처에 타입힌트된 이벤트를 찾아 자동으로 이벤트 리스너로 등록합니다:

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

PHP의 유니언 타입을 사용해서 여러 이벤트를 리스닝할 수도 있습니다:

```php
/**
 * Handle the event.
 */
public function handle(PodcastProcessed|PodcastPublished $event): void
{
    // ...
}
```

리스너를 별도의 디렉토리나 여러 디렉토리에 보관하고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에서 `withEvents` 메서드로 해당 디렉토리를 지정할 수 있습니다:

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/Orders/Listeners',
])
```

비슷한 이름의 여러 디렉토리를 와일드카드 `*`로 한 번에 지정할 수도 있습니다:

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/*/Listeners',
])
```

`event:list` 명령어는 애플리케이션에 등록된 모든 리스너를 목록화합니다:

```shell
php artisan event:list
```

<a name="event-discovery-in-production"></a>
#### 프로덕션에서의 이벤트 자동 감지

애플리케이션의 성능 향상을 위해, `optimize` 또는 `event:cache` Artisan 명령어로 모든 리스너의 목록(매니페스트)을 캐시해두는 것이 좋습니다. 이 명령어는 애플리케이션의 [배포 프로세스](/docs/master/deployment#optimization)에서 실행하는 것이 일반적입니다. 매니페스트는 프레임워크가 이벤트 등록 프로세스를 빠르게 처리하도록 돕습니다. `event:clear` 명령어로 이벤트 캐시를 삭제할 수도 있습니다.

<a name="manually-registering-events"></a>
### 이벤트 수동 등록 (Manually Registering Events)

`Event` 파사드를 사용하여 `AppServiceProvider`의 `boot` 메서드 안에서 이벤트와 리스너를 직접 등록할 수도 있습니다:

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

`event:list` 명령어로 등록된 리스너들을 확인할 수 있습니다:

```shell
php artisan event:list
```

<a name="closure-listeners"></a>
### 클로저 리스너 (Closure Listeners)

일반적으로 리스너는 클래스로 정의하지만, `AppServiceProvider`의 `boot` 메서드에서 클로저(익명 함수)를 사용해 이벤트 리스너를 수동으로 등록할 수도 있습니다:

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

클로저 기반 이벤트 리스너 등록 시, 클로저를 `Illuminate\Events\queueable` 함수로 감싸면 Laravel이 [큐](/docs/master/queues)를 사용해 리스너를 실행하게 할 수 있습니다:

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

큐잉된 작업처럼, `onConnection`, `onQueue`, `delay` 메서드로 큐 실행 환경을 커스터마이즈할 수 있습니다:

```php
Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->onConnection('redis')->onQueue('podcasts')->delay(now()->plus(seconds: 10)));
```

익명 큐잉 리스너가 실패했을 때 처리 로직을 추가하고 싶다면, `queueable` 리스너 정의 시 `catch` 메서드로 실패 처리용 클로저를 지정할 수 있습니다. 이 클로저는 이벤트 인스턴스와 예외 객체를 전달받습니다:

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

`*` 문자를 사용해 와일드카드 리스너를 등록할 수도 있습니다. 하나의 리스너로 여러 이벤트를 동시에 처리할 수 있으며, 첫 번째 인자는 이벤트 이름, 두 번째 인자는 전체 이벤트 데이터 배열을 받습니다:

```php
Event::listen('event.*', function (string $eventName, array $data) {
    // ...
});
```

<a name="defining-events"></a>
## 이벤트 정의하기 (Defining Events)

이벤트 클래스는 관련 데이터를 담는 "데이터 컨테이너" 역할을 합니다. 예를 들어, `App\Events\OrderShipped` 이벤트가 [Eloquent ORM](/docs/master/eloquent) 객체를 전달받는다고 가정해봅시다:

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

위 예시에서 이벤트 클래스는 별다른 로직 없이 `App\Models\Order` 인스턴스만을 담고 있습니다. 이벤트에서 사용하는 `SerializesModels` 트레이트는, 이벤트 객체를 PHP의 `serialize` 함수로 직렬화할 때(예: [큐잉 리스너](#queued-event-listeners) 사용시) Eloquent 모델을 안전하게 직렬화해줍니다.

<a name="defining-listeners"></a>
## 리스너 정의하기 (Defining Listeners)

이제 위 예시의 이벤트에 대한 리스너를 살펴보겠습니다. 이벤트 리스너는 이벤트 인스턴스를 `handle` 메서드에서 전달받습니다. `make:listener` Artisan 명령에 `--event` 옵션을 주면, 적절한 이벤트 클래스를 자동으로 import하고, `handle` 메서드에 타입힌트를 추가해줍니다. `handle` 메서드 안에서 이벤트에 대응하는 필요한 작업을 수행하면 됩니다:

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
> 이벤트 리스너의 생성자에서 필요한 의존성도 타입힌트로 지정할 수 있습니다. 모든 이벤트 리스너는 Laravel [서비스 컨테이너](/docs/master/container)로 해석되므로, 의존성이 자동으로 주입됩니다.

<a name="stopping-the-propagation-of-an-event"></a>
#### 이벤트 전파 중단하기

때로는, 특정 리스너에서 이벤트의 전파를 중단하고 싶을 수 있습니다. 이럴 때는 리스너의 `handle` 메서드에서 `false`를 반환하면, 이벤트가 다른 리스너로 전달되지 않습니다.

<a name="queued-event-listeners"></a>
## 큐잉된 이벤트 리스너 (Queued Event Listeners)

리스너에서 이메일 전송이나 HTTP 요청 등 느린 작업을 수행해야 한다면, 해당 리스너를 큐잉하는 것이 좋습니다. 큐잉된 리스너를 사용하기 전, 반드시 [큐를 설정](/docs/master/queues)하고 서버나 개발환경에서 큐 워커를 실행해야 합니다.

리스너를 큐잉하려면, 클래스에 `ShouldQueue` 인터페이스를 추가하면 됩니다. Artisan 명령어로 생성된 리스너 클래스에는 이미 해당 인터페이스가 import되어 있으므로 바로 사용할 수 있습니다:

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

이제 이 리스너가 처리하는 이벤트가 디스패치되면, Laravel의 [큐 시스템](/docs/master/queues)을 통해 자동으로 큐잉됩니다. 리스너 실행 중 예외가 발생하지 않으면, 큐 작업은 실행 후 자동으로 삭제됩니다.

<a name="customizing-the-queue-connection-queue-name"></a>
#### 큐 연결, 이름, 지연 시간 커스터마이징

이벤트 리스너의 큐 연결명, 큐명, 큐 지연 시간을 커스터마이징하려면 클래스에 `$connection`, `$queue`, `$delay` 속성을 정의하면 됩니다:

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

런타임에 연결명, 큐명, 지연 시간을 동적으로 정의하고 싶다면, `viaConnection`, `viaQueue`, `withDelay` 메서드를 추가하여 처리할 수 있습니다:

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

런타임 데이터에 따라 리스너의 큐잉 여부를 결정하고 싶을 때는, `shouldQueue` 메서드를 추가해 원하는 조건에서만 큐잉되도록 할 수 있습니다. `shouldQueue`가 `false`를 반환하면 큐잉되지 않습니다:

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
### 큐 직접 다루기 (Manually Interacting With the Queue)

리스너의 큐 작업에서 `delete`나 `release` 메서드를 직접 사용하려면, `Illuminate\Queue\InteractsWithQueue` 트레이트를 추가해 활용할 수 있습니다. 이 트레이트는 Artisan 명령으로 생성한 리스너에 기본적으로 포함되어 있습니다:

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
### 큐잉 리스너와 데이터베이스 트랜잭션 (Queued Event Listeners and Database Transactions)

큐잉 리스너가 데이터베이스 트랜잭션 내에서 디스패치될 때, 트랜잭션이 커밋되기 전에 큐로 처리되는 일이 있을 수 있습니다. 이 경우, 트랜잭션 중에 변경된 모델이나 데이터베이스 레코드가 아직 반영되지 않았거나, 새로 생성된 레코드가 존재하지 않을 수도 있습니다. 따라서, 리스너가 이러한 모델에 의존한다면 예기치 않은 오류가 발생할 수 있습니다.

큐 연결의 `after_commit` 옵션이 `false`로 설정된 경우라도, 리스너 클래스에 `ShouldQueueAfterCommit` 인터페이스를 구현하면 모든 데이터베이스 트랜잭션 커밋 이후에 해당 큐잉 리스너가 디스패치됩니다:

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
> 이러한 문제를 회피하려면 [큐 작업과 데이터베이스 트랜잭션](/docs/master/queues#jobs-and-database-transactions) 관련 문서를 참고하시기 바랍니다.

<a name="queued-listener-middleware"></a>
### 큐잉 리스너 미들웨어 (Queued Listener Middleware)

큐잉 리스너에서도 [작업 미들웨어](/docs/master/queues#job-middleware)를 사용할 수 있습니다. 작업 미들웨어는 큐잉 리스너 실행에 커스텀 로직을 추가하여, 중복 코드를 줄일 수 있습니다. 작업 미들웨어를 만든 뒤, 리스너의 `middleware` 메서드에서 반환하면 적용됩니다:

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
#### 암호화된 큐잉 리스너 (Encrypted Queued Listeners)

Laravel은 [암호화](/docs/master/encryption)를 활용해, 큐잉 리스너의 데이터의 프라이버시와 무결성을 보장할 수 있습니다. 사용하려면 리스너 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하면 됩니다. 이 인터페이스를 추가하면, Laravel이 해당 리스너를 큐에 넣기 전에 자동으로 암호화합니다:

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

<a name="unique-event-listeners"></a>
### 고유 이벤트 리스너 (Unique Event Listeners)

> [!WARNING]
> 고유 리스너는 [락](/docs/master/cache#atomic-locks)을 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 원자적 락을 지원합니다.

특정 리스너의 인스턴스가 한 번에 큐에 단 1개만 존재하게 보장하고 싶을 수 있습니다. 이럴 때는 리스너 클래스에 `ShouldBeUnique` 인터페이스를 구현합니다:

```php
<?php

namespace App\Listeners;

use App\Events\LicenseSaved;
use Illuminate\Contracts\Queue\ShouldBeUnique;
use Illuminate\Contracts\Queue\ShouldQueue;

class AcquireProductKey implements ShouldQueue, ShouldBeUnique
{
    public function __invoke(LicenseSaved $event): void
    {
        // ...
    }
}
```

위 예시의 `AcquireProductKey` 리스너는 고유하므로, 아직 처리 중인 동일한 리스너가 큐에 이미 있다면 새로 큐잉되지 않습니다. 즉, 하나의 라이선스에 대해 하나의 상품 키만 발급되도록 보장할 수 있습니다.

특정 "키"를 기준으로 고유성을 정의하거나, 고유 상태가 유지될 최대 시간(타임아웃)을 지정하고 싶을 경우, `uniqueId`와 `uniqueFor` 속성 또는 메서드를 정의할 수 있습니다. 메서드는 이벤트 인스턴스를 받아, 반환값을 자유롭게 만들 수 있습니다:

```php
<?php

namespace App\Listeners;

use App\Events\LicenseSaved;
use Illuminate\Contracts\Queue\ShouldBeUnique;
use Illuminate\Contracts\Queue\ShouldQueue;

class AcquireProductKey implements ShouldQueue, ShouldBeUnique
{
    /**
     * The number of seconds after which the listener's unique lock will be released.
     *
     * @var int
     */
    public $uniqueFor = 3600;

    public function __invoke(LicenseSaved $event): void
    {
        // ...
    }

    /**
     * Get the unique ID for the listener.
     */
    public function uniqueId(LicenseSaved $event): string
    {
        return 'listener:'.$event->license->id;
    }
}
```

위 예시에서는 라이선스 ID별로 고유성이 부여되어, 동일 라이선스에 대한 추가 큐잉은 기존 리스너가 완료될 때까지 무시됩니다. 1시간 이내에 기존 리스너가 처리되지 않으면 락이 풀려 새로운 리스너가 큐잉될 수 있습니다.

> [!WARNING]
> 애플리케이션이 여러 웹 서버나 컨테이너에서 이벤트를 디스패치한다면, 모든 서버가 동일한 중앙 캐시 서버와 통신하도록 구성해야 Laravel이 정확하게 유일성을 판단할 수 있습니다.

Laravel은 기본적으로 기본 캐시 드라이버를 사용해 고유 락을 확보합니다. 별도의 드라이버를 사용하고 싶다면, `uniqueVia` 메서드를 정의해 사용할 캐시 드라이버를 반환하면 됩니다:

```php
<?php

namespace App\Listeners;

use App\Events\LicenseSaved;
use Illuminate\Contracts\Cache\Repository;
use Illuminate\Support\Facades\Cache;

class AcquireProductKey implements ShouldQueue, ShouldBeUnique
{
    // ...

    /**
     * Get the cache driver for the unique listener lock.
     */
    public function uniqueVia(LicenseSaved $event): Repository
    {
        return Cache::driver('redis');
    }
}
```

<a name="handling-failed-jobs"></a>
### 실패한 작업 처리 (Handling Failed Jobs)

큐잉된 이벤트 리스너가 실패할 수 있습니다. 큐잉 리스너가 큐 워커의 최대 시도 횟수를 초과하면, 리스너의 `failed` 메서드가 호출됩니다. 이 메서드는 이벤트 인스턴스와 예외(`Throwable`) 인스턴스를 전달받습니다:

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
#### 큐잉 리스너 최대 시도 횟수 지정

큐잉 리스너에 오류가 발생한다면, 무한 재시도를 원하지 않을 수 있습니다. Laravel에서는 시도 횟수 또는 시도 허용 시간을 설정할 수 있는 다양한 방법을 제공합니다.

리스너 클래스의 `tries` 속성이나 메서드에 시도 횟수를 지정할 수 있습니다:

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

실패 시 언제까지 리스너를 시도할지 "마감 시간"을 정의하려면, `retryUntil` 메서드를 리스너에 정의하면 됩니다. 이 메서드는 `DateTime` 인스턴스를 반환해야 합니다:

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

`retryUntil`과 `tries`가 모두 정의되어 있다면, Laravel은 `retryUntil`을 우선시합니다.

<a name="specifying-queued-listener-backoff"></a>
#### 큐잉 리스너 백오프 지정

리스너의 예외 발생 시, 얼마 동안 대기 후 다시 시도할지 `backoff` 속성으로 지정할 수 있습니다:

```php
/**
 * The number of seconds to wait before retrying the queued listener.
 *
 * @var int
 */
public $backoff = 3;
```

더 복잡한 대기 시간 로직이 필요하다면, `backoff` 메서드로 구현할 수 있습니다:

```php
/**
 * Calculate the number of seconds to wait before retrying the queued listener.
 */
public function backoff(OrderShipped $event): int
{
    return 3;
}
```

배열을 반환하면 "지수 증가" 방식의 백오프도 쉽게 설정할 수 있습니다. 아래 예시에서는 첫 재시도는 1초, 두 번째는 5초, 세 번째 이후는 10초씩 반복됩니다:

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
#### 큐잉 리스너 최대 예외 횟수 지정

리스너를 여러 번 재시도하게 하고 싶지만, 미처리 예외가 특정 횟수 이상 발생하면 즉시 실패로 간주하고 싶을 때 `maxExceptions` 속성으로 지정할 수 있습니다:

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

위 예시에서 리스너는 총 25번까지 재시도할 수 있지만, 처리되지 않은 예외가 3번 발생하면 실패로 간주됩니다.

<a name="specifying-queued-listener-timeout"></a>
#### 큐잉 리스너 타임아웃 지정

일반적으로, 큐잉 리스너의 예상 실행 시간을 알 수 있습니다. 만약 리스너가 지정한 초(second)보다 오래 실행된다면, 해당 작업을 처리하던 워커는 에러와 함께 종료됩니다. 리스너 클래스의 `timeout` 속성으로 타임아웃(초)을 지정할 수 있습니다:

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

타임아웃 발생 시 리스너를 실패로 간주하려면, `failOnTimeout` 속성을 `true`로 설정합니다:

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
## 이벤트 디스패치 (Dispatching Events)

이벤트를 디스패치하려면, 이벤트 클래스의 정적 `dispatch` 메서드를 호출합니다. 이 메서드는 이벤트에 `Illuminate\Foundation\Events\Dispatchable` 트레이트가 포함되어 있어 사용할 수 있습니다. `dispatch`로 넘겨준 인수는 이벤트 생성자(construct)에 그대로 전달됩니다:

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

조건에 따라 이벤트를 디스패치하려면 `dispatchIf` 또는 `dispatchUnless`를 사용할 수 있습니다:

```php
OrderShipped::dispatchIf($condition, $order);

OrderShipped::dispatchUnless($condition, $order);
```

> [!NOTE]
> 테스트 시 실제로 리스너가 실행되지 않고 이벤트가 디스패치되었는지 확인할 수 있게, Laravel의 [테스트 헬퍼](#testing)가 제공됩니다.

<a name="dispatching-events-after-database-transactions"></a>
### 데이터베이스 트랜잭션 이후 이벤트 디스패치

가끔은 데이터베이스 트랜잭션 커밋 이후에만 이벤트를 디스패치하고 싶을 때가 있습니다. 이럴 때 이벤트 클래스에 `ShouldDispatchAfterCommit` 인터페이스를 구현하면 됩니다.

이 인터페이스는 현재 트랜잭션이 커밋될 때까지 이벤트를 디스패치하지 않도록 Laravel에 지시합니다. 트랜잭션이 실패하면 이벤트도 무시되고, 만약 트랜잭션이 없는 상황에서 이벤트를 디스패치하면 즉시 실행됩니다:

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
### 이벤트 지연 디스패치 (Deferring Events)

이벤트 지연(Deferred) 기능을 활용하면, 지정된 코드 블록이 모두 실행 완료된 후에만 모델 이벤트나 리스너가 실행됩니다. 이는 이벤트 리스너가 관련 레코드 생성이 모두 끝난 이후 실행되어야 할 때 유용합니다.

지연 디스패치를 하려면, `Event::defer()`에 클로저를 전달하면 됩니다:

```php
use App\Models\User;
use Illuminate\Support\Facades\Event;

Event::defer(function () {
    $user = User::create(['name' => 'Victoria Otwell']);

    $user->posts()->create(['title' => 'My first post!']);
});
```

클로저 내에서 발생한 모든 이벤트는 클로저 실행 완료 후 한 번에 디스패치됩니다. 만약 클로저 내에서 예외가 발생하면, 지연된 이벤트도 디스패치되지 않습니다.

특정 이벤트만 지연하고 싶을 경우, `defer` 메서드의 두 번째 인자로 이벤트 배열을 전달하면 됩니다:

```php
use App\Models\User;
use Illuminate\Support\Facades/Event;

Event::defer(function () {
    $user = User::create(['name' => 'Victoria Otwell']);

    $user->posts()->create(['title' => 'My first post!']);
}, ['eloquent.created: '.User::class]);
```

<a name="event-subscribers"></a>
## 이벤트 구독자 (Event Subscribers)

<a name="writing-event-subscribers"></a>
### 이벤트 구독자 작성 (Writing Event Subscribers)

이벤트 구독자(Subscriber)는 하나의 클래스에서 여러 이벤트에 동시에 구독하여 여러 이벤트 핸들러를 한 곳에 정의할 수 있습니다. 구독자 클래스는 반드시 `subscribe` 메서드를 정의해야 하며, 이 메서드는 이벤트 디스패처(Dispatcher) 인스턴스를 받습니다. 전달받은 디스패처의 `listen` 메서드를 사용해 리스너를 등록할 수 있습니다:

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

구독자 자체에 리스너 메서드가 정의되어 있다면, `subscribe` 메서드에서 이벤트와 메서드를 매핑한 배열을 반환하는 방식으로도 등록할 수 있습니다. Laravel이 자동으로 구독자 클래스명을 추론합니다:

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
### 이벤트 구독자 등록 (Registering Event Subscribers)

구독자를 작성한 후, 구독자의 메서드가 [이벤트 자동 감지 규칙](#event-discovery)을 따르면 Laravel이 자동으로 등록합니다. 그렇지 않은 경우, `Event` 파사드의 `subscribe` 메서드로 수동 등록할 수 있습니다. 보통 `AppServiceProvider`의 `boot` 메서드에서 수행합니다:

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
## 테스트 (Testing)

이벤트를 디스패치하는 코드를 테스트할 때, 해당 이벤트의 리스너가 실제로 실행되지 않게 제한하고 싶을 수 있습니다. 리스너의 코드는 별도로 테스트할 수 있으니, 디스패치 코드에서는 이벤트 디스패치만 검증하면 충분합니다. 리스너 테스트의 경우, 인스턴스를 직접 생성해 `handle` 메서드를 호출해 테스트할 수 있습니다.

`Event` 파사드의 `fake` 메서드로 리스너 실행 없이, 테스트 코드 실행 후 `assertDispatched`, `assertNotDispatched`, `assertNothingDispatched` 등의 메서드로 이벤트가 디스패치되었는지 검증할 수 있습니다:

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

`assertDispatched`나 `assertNotDispatched` 메서드에 클로저를 전달하면, 해당 조건을 만족하는 이벤트가 디스패치되었는지/되지 않았는지 검증할 수 있습니다. 조건을 만족하는 이벤트가 하나라도 있으면 성공합니다:

```php
Event::assertDispatched(function (OrderShipped $event) use ($order) {
    return $event->order->id === $order->id;
});
```

특정 이벤트에 리스너가 등록되어 있는지도 `assertListening` 메서드로 검증할 수 있습니다:

```php
Event::assertListening(
    OrderShipped::class,
    SendShipmentNotification::class
);
```

> [!WARNING]
> `Event::fake()`를 호출하면 모든 이벤트 리스너가 실행되지 않습니다. 모델 팩토리에서 이벤트에 의존(예: 모델의 `creating` 이벤트에서 UUID 생성)하는 경우, 팩토리 사용 이후에 `Event::fake()`를 호출해야 합니다.

<a name="faking-a-subset-of-events"></a>
### 일부 이벤트만 페이크 사용 (Faking a Subset of Events)

특정 이벤트만 리스너 실행을 막고 싶을 때는, `fake`나 `fakeFor` 메서드에 이벤트 배열을 인자로 전달합니다:

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

반대로, 지정한 이벤트만 실제 리스너를 실행하고 나머지를 페이크로 처리하고 싶으면 `except` 메서드를 사용합니다:

```php
Event::fake()->except([
    OrderCreated::class,
]);
```

<a name="scoped-event-fakes"></a>
### 스코프가 지정된 이벤트 페이크 (Scoped Event Fakes)

테스트의 일부 구간에서만 이벤트 리스너 실행을 막고 싶다면, `fakeFor` 메서드를 사용할 수 있습니다:

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
