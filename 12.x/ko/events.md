# 이벤트 (Events)

- [소개](#introduction)
- [이벤트 및 리스너 생성](#generating-events-and-listeners)
- [이벤트와 리스너 등록](#registering-events-and-listeners)
    - [이벤트 디스커버리](#event-discovery)
    - [이벤트 수동 등록](#manually-registering-events)
    - [클로저 리스너](#closure-listeners)
- [이벤트 정의](#defining-events)
- [리스너 정의](#defining-listeners)
- [큐 처리 이벤트 리스너](#queued-event-listeners)
    - [큐와 수동으로 상호작용하기](#manually-interacting-with-the-queue)
    - [큐 처리 리스너와 데이터베이스 트랜잭션](#queued-event-listeners-and-database-transactions)
    - [큐 리스너 미들웨어](#queued-listener-middleware)
    - [암호화된 큐 리스너](#encrypted-queued-listeners)
    - [유니크 이벤트 리스너](#unique-event-listeners)
    - [실패한 작업 처리](#handling-failed-jobs)
- [이벤트 디스패치](#dispatching-events)
    - [데이터베이스 트랜잭션 이후 이벤트 디스패치](#dispatching-events-after-database-transactions)
    - [이벤트 디퍼 (지연)](#deferring-events)
- [이벤트 구독자](#event-subscribers)
    - [이벤트 구독자 작성](#writing-event-subscribers)
    - [이벤트 구독자 등록](#registering-event-subscribers)
- [테스트](#testing)
    - [일부 이벤트만 페이크로 처리하기](#faking-a-subset-of-events)
    - [스코프별 이벤트 페이크](#scoped-event-fakes)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel의 이벤트 시스템은 간단한 옵서버 패턴을 구현하여 애플리케이션 내에서 발생하는 다양한 이벤트를 구독(subscribe)하고 청취(listen)할 수 있도록 해줍니다. 이벤트 클래스는 보통 `app/Events` 디렉토리에, 이들의 리스너는 `app/Listeners` 디렉토리에 위치합니다. 이러한 디렉토리가 애플리케이션에 보이지 않더라도 걱정하지 마십시오. Artisan 콘솔 명령어로 이벤트와 리스너를 생성할 때 자동으로 만들어집니다.

이벤트는 애플리케이션의 다양한 부분을 느슨하게 결합하는 좋은 방법입니다. 하나의 이벤트에 여러 리스너를 연결할 수 있으며, 이 리스너들은 서로에게 의존하지 않습니다. 예를 들어, 주문이 배송될 때마다 사용자에게 Slack 알림을 보내고 싶을 수 있습니다. 이때 주문 처리 코드에 Slack 알림 코드를 직접 결합하는 대신, `App\Events\OrderShipped` 이벤트를 발생시키고, 해당 이벤트를 수신하는 리스너에서 Slack 알림을 보내도록 할 수 있습니다.

<a name="generating-events-and-listeners"></a>
## 이벤트 및 리스너 생성 (Generating Events and Listeners)

이벤트와 리스너를 빠르게 생성하려면 `make:event`와 `make:listener` Artisan 명령어를 사용하면 됩니다:

```shell
php artisan make:event PodcastProcessed

php artisan make:listener SendPodcastNotification --event=PodcastProcessed
```

또한, 추가 인수 없이 `make:event`와 `make:listener` Artisan 명령어를 실행할 수도 있습니다. 이 경우 Laravel이 자동으로 클래스명과(리스너 생성 시) 이벤트명을 입력하도록 프롬프트를 제공합니다:

```shell
php artisan make:event

php artisan make:listener
```

<a name="registering-events-and-listeners"></a>
## 이벤트와 리스너 등록 (Registering Events and Listeners)

<a name="event-discovery"></a>
### 이벤트 디스커버리

기본적으로 Laravel은 애플리케이션의 `Listeners` 디렉토리를 스캔하여 이벤트 리스너를 자동으로 찾고 등록합니다. Laravel은 클래스 메서드 중 `handle`이나 `__invoke`로 시작하는 메서드를 찾으면, 해당 메서드에 타입힌트(type-hint)된 이벤트를 자동으로 리스너로 등록합니다:

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

PHP의 유니온 타입을 사용하여 여러 이벤트를 청취할 수도 있습니다:

```php
/**
 * Handle the event.
 */
public function handle(PodcastProcessed|PodcastPublished $event): void
{
    // ...
}
```

리스너를 다른 디렉토리나 여러 디렉토리 내에 저장하려면, 애플리케이션의 `bootstrap/app.php` 파일에서 `withEvents` 메서드를 사용해 Laravel이 추가 경로를 스캔하도록 지정할 수 있습니다:

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/Orders/Listeners',
])
```

`*` 문자를 와일드카드로 사용해 여러 유사한 경로를 스캔할 수도 있습니다:

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/*/Listeners',
])
```

`event:list` 명령어는 애플리케이션에 등록된 모든 리스너를 목록으로 보여줍니다:

```shell
php artisan event:list
```

<a name="event-discovery-in-production"></a>
#### 프로덕션 환경에서의 이벤트 디스커버리

애플리케이션의 성능 향상을 위해, `optimize` 또는 `event:cache` Artisan 명령어로 모든 리스너의 매니페스트를 캐싱하는 것이 좋습니다. 이 명령어는 일반적으로 [배포 프로세스](/docs/12.x/deployment#optimization)에서 실행됩니다. 캐시된 매니페스트를 사용하면 이벤트 등록 과정이 더 빨라집니다. 캐시를 제거하려면 `event:clear` 명령어를 사용하세요.

<a name="manually-registering-events"></a>
### 이벤트 수동 등록

`Event` 파사드를 사용하면, 애플리케이션의 `AppServiceProvider`의 `boot` 메서드 안에서 이벤트와 해당 리스너를 수동으로 등록할 수 있습니다:

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

`event:list` 명령어로 애플리케이션에 등록된 모든 리스너를 확인할 수 있습니다:

```shell
php artisan event:list
```

<a name="closure-listeners"></a>
### 클로저 리스너 (Closure Listeners)

일반적으로 리스너는 클래스로 정의하지만, 익명 함수(클로저) 기반의 이벤트 리스너를 `AppServiceProvider`의 `boot` 메서드에서 수동으로 등록할 수도 있습니다:

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
#### Queueable 익명 이벤트 리스너

클로저 기반 이벤트 리스너를 등록할 때, `Illuminate\Events\queueable` 함수를 사용해 리스너 클로저를 래핑하면, Laravel이 해당 리스너를 [큐](/docs/12.x/queues)를 통해 처리하도록 할 수 있습니다:

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

큐에 들어가는 작업과 동일하게, `onConnection`, `onQueue`, `delay` 메서드로 큐 리스너의 실행 환경을 커스터마이즈할 수 있습니다:

```php
Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->onConnection('redis')->onQueue('podcasts')->delay(now()->plus(seconds: 10)));
```

익명 큐 리스너에서 실패 발생 시, `queueable` 리스너를 정의할 때 `catch` 메서드에 클로저를 전달해 실패 처리를 할 수 있습니다. 이 클로저는 이벤트 인스턴스와 리스너 실패 원인인 `Throwable` 인스턴스를 받게 됩니다:

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

리스너를 등록할 때 `*` 문자를 와일드카드로 사용하면, 여러 이벤트를 하나의 리스너 함수에서 처리할 수 있습니다. 와일드카드 리스너는 첫 번째 인수로 이벤트 이름, 두 번째 인수로 전체 이벤트 데이터 배열을 받습니다:

```php
Event::listen('event.*', function (string $eventName, array $data) {
    // ...
});
```

<a name="defining-events"></a>
## 이벤트 정의 (Defining Events)

이벤트 클래스는 해당 이벤트와 관련된 정보를 담는 데이터 컨테이너와 같습니다. 예를 들어, `App\Events\OrderShipped` 이벤트가 [Eloquent ORM](/docs/12.x/eloquent) 객체를 받는다고 가정해 보겠습니다:

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

보시는 것처럼, 이 이벤트 클래스는 별도의 논리가 없습니다. 구매된 `App\Models\Order` 인스턴스를 담는 역할만 합니다. 이벤트에 포함된 `SerializesModels` 트레잇은 이벤트 객체가 PHP의 `serialize` 함수로 직렬화될 경우(Eloquent 모델 포함 시) 이를 안전하게 처리해 줍니다. 이는 주로 [큐 리스너](#queued-event-listeners)를 사용할 때 유용합니다.

<a name="defining-listeners"></a>
## 리스너 정의 (Defining Listeners)

이제 앞서 예시로 든 이벤트의 리스너에 대해 살펴보겠습니다. 이벤트 리스너는 `handle` 메서드에서 이벤트 인스턴스를 인수로 받아 처리합니다. `make:listener` Artisan 명령어에 `--event` 옵션을 이용하면 자동으로 이벤트 클래스를 import하고, `handle` 메서드의 타입힌트까지 맞춰줍니다. `handle` 메서드 내에서는 이벤트에 대응하는 필요한 작업을 자유롭게 수행할 수 있습니다:

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
> 이벤트 리스너의 생성자에서 필요한 의존성을 타입힌트하면 자동으로 [서비스 컨테이너](/docs/12.x/container)를 통해 주입받을 수 있습니다.

<a name="stopping-the-propagation-of-an-event"></a>
#### 이벤트 전파(stop) 중단

경우에 따라, 특정 리스너에서 이벤트의 전파를 중단(이벤트의 나머지 리스너가 실행되지 않도록)하고 싶을 수 있습니다. 리스너의 `handle` 메서드에서 `false`를 반환하면 이벤트 전파가 멈춥니다.

<a name="queued-event-listeners"></a>
## 큐 처리 이벤트 리스너 (Queued Event Listeners)

리스너가 이메일 전송이나 HTTP 요청 같은 느린 작업을 수행할 경우, 리스너를 큐에 넣는 것이 유리합니다. 큐 리스너를 사용하기 전, [큐를 설정](/docs/12.x/queues)하고, 서버나 로컬 개발 환경에서 큐 워커를 시작해야 합니다.

리스너를 큐에 넣으려면 리스너 클래스에 `ShouldQueue` 인터페이스를 추가하면 됩니다. `make:listener` Artisan 명령어로 생성된 리스너에는 이미 이 인터페이스가 import되어 있습니다:

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

이렇게 하면, 해당 리스너가 처리하는 이벤트가 발생할 때마다, Laravel의 [큐 시스템](/docs/12.x/queues)을 통해 리스너가 자동으로 큐에 등록되고 실행됩니다. 큐에서 리스너가 예외 없이 성공적으로 실행되면, 리스너의 큐 작업은 자동으로 삭제됩니다.

<a name="customizing-the-queue-connection-queue-name"></a>
#### 큐 연결, 큐 이름, 지연시간 커스터마이즈

리스너에서 사용될 큐 연결명, 큐 이름, 지연 시간(Delay) 등을 커스터마이즈하려면 리스너 클래스에 `$connection`, `$queue`, `$delay` 속성을 정의하면 됩니다:

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

실행 시점에 동적으로 큐 연결명, 큐 이름, 지연시간을 지정하려면 `viaConnection`, `viaQueue`, `withDelay` 메서드를 정의하면 됩니다:

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
#### 조건부 큐 처리

경우에 따라 리스너를 큐에 넣을지 여부를 런타임 데이터로 결정해야 할 수도 있습니다. 리스너에 `shouldQueue` 메서드를 정의하면, 그 결과에 따라 리스너의 큐 작업 등록 여부가 결정됩니다. `shouldQueue`가 `false`를 반환하면, 해당 리스너는 큐에 등록되지 않습니다:

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
### 큐와 수동으로 상호작용하기

큐 리스너의 기본 큐 작업에서 `delete` 및 `release` 메서드에 직접 접근하려면 `Illuminate\Queue\InteractsWithQueue` 트레잇을 리스너에 추가하면 됩니다. 이 트레잇은 Artisan으로 생성된 리스너에 기본적으로 포함됩니다:

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
### 큐 처리 리스너와 데이터베이스 트랜잭션

큐 리스너가 데이터베이스 트랜잭션 내에서 디스패치될 경우, 트랜잭션이 커밋되기 전에 큐에서 해당 리스너가 처리될 수 있습니다. 이때 트랜잭션 내에서 수정된 모델이나 레코드는 아직 실제 데이터베이스에 반영되지 않아, 리스너에서 의도치 않은 에러가 발생할 수 있습니다.

큐 커넥션의 `after_commit` 옵션이 `false`로 되어 있을 때도, 해당 리스너 클래스에서 `ShouldQueueAfterCommit` 인터페이스를 구현하면 모든 열린 트랜잭션이 커밋된 후에만 큐 리스너가 디스패치됩니다:

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
> 이 이슈를 우회하는 방법은 [큐 작업과 데이터베이스 트랜잭션](/docs/12.x/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="queued-listener-middleware"></a>
### 큐 리스너 미들웨어

큐 리스너도 [작업 미들웨어](/docs/12.x/queues#job-middleware)를 사용할 수 있습니다. 작업 미들웨어는 큐 리스너 실행에 커스텀 로직을 삽입하여, 리스너 내에서 반복되는 보일러플레이트 코드를 줄여줍니다. 미들웨어를 생성한 뒤, 리스너의 `middleware` 메서드에서 반환하면 해당 미들웨어가 적용됩니다:

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

Laravel은 큐 리스너의 데이터 보안과 무결성을 [암호화](/docs/12.x/encryption)로 보장할 수 있습니다. 리스너 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하면 됩니다. 이 인터페이스를 클래스에 추가하면, 해당 리스너는 자동으로 암호화되어 큐에 등록됩니다:

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
### 유니크 이벤트 리스너 (Unique Event Listeners)

> [!WARNING]
> 유니크 리스너는 [락(lock) 지원](/docs/12.x/cache#atomic-locks)이 가능한 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 이를 지원합니다.

특정 리스너가 동시에 하나의 인스턴스만 큐에 등록되도록 보장하려면, 리스너 클래스에 `ShouldBeUnique` 인터페이스를 구현하세요:

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

위 예시에서는 `AcquireProductKey` 리스너가 유니크하게 동작합니다. 즉, 같은 리스너의 인스턴스가 큐에서 처리가 끝나지 않은 상태라면 새로운 인스턴스는 큐에 등록되지 않습니다. 이를 통해 라이선스 한 건에 대해 하나의 제품 키만 발급하도록 강제할 수 있습니다.

경우에 따라, 리스너의 유니크함을 결정짓는 "키"를 직접 정의하거나, 유니크한 상태가 유지되는 타임아웃을 지정할 수도 있습니다. 이때는 리스너 클래스에 `uniqueId`, `uniqueFor` 속성이나 메서드를 정의할 수 있습니다. 이 메서드들은 이벤트 인스턴스를 받아, 고유한 값을 반환할 수 있게 합니다:

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

위의 예제에서는, 라이선스 ID를 기준으로 리스너의 유니크함이 결정됩니다. 즉, 동일한 라이선스 ID에 대해 기존 리스너의 처리가 끝날 때까지 새로운 리스너는 무시됩니다. 또한, 유니크 락이 1시간(3600초) 이내에 해제되지 않으면 자동으로 풀리고, 이후 동일한 키의 리스너가 다시 큐에 들어갈 수 있습니다.

> [!WARNING]
> 여러 웹 서버나 컨테이너에서 이벤트를 디스패치하는 애플리케이션이라면, 모든 서버가 동일한 중앙 캐시 서버와 통신하도록 설정해야만, 리스너의 유니크함이 올바르게 보장됩니다.

Laravel은 기본적으로 기본 캐시 드라이버를 사용해 유니크 락을 관리합니다. 별도의 드라이버를 지정하려면, `uniqueVia` 메서드에서 원하는 캐시 드라이버를 반환하세요:

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

큐에 등록된 이벤트 리스너가 실패할 수도 있습니다. 큐 리스너가 큐 워커에 설정된 최대 시도 횟수를 초과하면, 리스너의 `failed` 메서드가 호출됩니다. 이 메서드는 이벤트 인스턴스와 실패 원인인 `Throwable` 객체를 받습니다:

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
#### 큐 리스너의 최대 시도 횟수 지정

큐 리스너에서 오류가 발생할 경우, 무한정 재시도되는 것을 원하지 않을 수 있습니다. Laravel에서는 리스너가 얼마나 많은 횟수 또는 얼마 동안 재시도될 수 있는지 다양하게 설정할 수 있습니다.

리스너 클래스에 `tries` 속성이나 메서드를 정의하여, 시도 가능 최대 횟수를 지정할 수 있습니다:

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

재시도 횟수 대신, 리스너의 재시도 제한 시점을 설정할 수도 있습니다. 이 경우 `retryUntil` 메서드를 정의하고, 이 메서드가 `DateTime` 인스턴스를 반환하도록 하면, 해당 시간까지는 무제한 시도할 수 있고, 이후에는 더 이상 재시도하지 않습니다:

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

`retryUntil`과 `tries`가 모두 정의되어 있으면, Laravel은 `retryUntil` 메서드를 우선적으로 적용합니다.

<a name="specifying-queued-listener-backoff"></a>
#### 큐 리스너 백오프(재시도 대기) 설정

리스너가 예외를 만났을 때, 재시도 전에 Laravel이 얼마나 기다려야 할지 `backoff` 속성으로 지정할 수 있습니다:

```php
/**
 * The number of seconds to wait before retrying the queued listener.
 *
 * @var int
 */
public $backoff = 3;
```

더 복잡한 백오프 로직이 필요하다면, `backoff` 메서드로 값을 동적으로 지정할 수도 있습니다:

```php
/**
 * Calculate the number of seconds to wait before retrying the queued listener.
 */
public function backoff(OrderShipped $event): int
{
    return 3;
}
```

"지수적(Exponential)" 백오프를 적용하고 싶다면, `backoff` 메서드에서 배열을 반환하면 됩니다. 예시에서는 첫 번째 재시도 1초, 두 번째 5초, 세 번째 10초 이후 매번 10초 간격으로 재시도합니다:

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

리스너가 여러 번 재시도될 수 있지만, 특정 개수의 미처리 예외가 발생할 경우에는 더 이상 리스너를 재시도하지 않고 실패로 간주하고 싶을 수 있습니다. 이때는 리스너 클래스에 `maxExceptions` 속성을 지정하면 됩니다:

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

위 예제에서 리스너는 총 25번까지 재시도될 수 있지만, 처리되지 않은 예외가 3번 발생하면 즉시 실패로 간주됩니다.

<a name="specifying-queued-listener-timeout"></a>
#### 큐 리스너 타임아웃 지정

큐 리스너가 얼마나 오랫동안 실행될지 대략적으로 예상할 수 있다면, "타임아웃" 값을 지정할 수 있습니다. 리스너가 지정된 초 수 이상 실행되면, 워커는 에러와 함께 종료됩니다. 리스너 클래스에 `timeout` 속성을 지정하면 최대 실행 시간을 설정할 수 있습니다:

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

타임아웃 시 리스너를 실패 상태로 처리하려면, 리스너 클래스에 `failOnTimeout` 속성을 설정하면 됩니다:

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

이벤트를 디스패치하려면, 해당 이벤트의 정적 `dispatch` 메서드를 호출하면 됩니다. 이 메서드는 `Illuminate\Foundation\Events\Dispatchable` 트레잇을 통해 사용 가능합니다. `dispatch` 메서드에 전달한 모든 인수는 이벤트의 생성자로 전달됩니다:

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

조건에 따라 이벤트를 디스패치하려면, `dispatchIf` 및 `dispatchUnless` 메서드를 사용할 수 있습니다:

```php
OrderShipped::dispatchIf($condition, $order);

OrderShipped::dispatchUnless($condition, $order);
```

> [!NOTE]
> 테스트 시, 특정 이벤트가 실제로 리스너를 트리거하지 않고 디스패치만 되었는지 쉽게 검증할 수 있습니다. Laravel의 [내장 테스트 헬퍼](#testing)를 참고하세요.

<a name="dispatching-events-after-database-transactions"></a>
### 데이터베이스 트랜잭션 이후 이벤트 디스패치

때로는, 현재 진행 중인 데이터베이스 트랜잭션이 커밋된 이후에만 이벤트를 디스패치하도록 하고 싶을 수 있습니다. 이때는 이벤트 클래스에 `ShouldDispatchAfterCommit` 인터페이스를 구현하면 됩니다.

이 인터페이스를 사용할 경우, 트랜잭션이 커밋될 때까지 이벤트가 디스패치되지 않습니다. 트랜잭션에서 문제가 생기면 이벤트는 버려집니다. 트랜잭션이 없을 경우에는 즉시 이벤트가 디스패치됩니다:

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
### 이벤트 디퍼 (지연)

이벤트 디퍼는 특정 코드 블록이 실행된 후에만 모델 이벤트를 디스패치하고, 이벤트 리스너의 실행도 지연시키도록 해줍니다. 이는 연관된 레코드가 모두 생성된 이후에만 리스너가 동작해야 할 때 유용합니다.

이벤트를 지연시키려면, `Event::defer()` 메서드에 클로저를 인자로 전달하면 됩니다:

```php
use App\Models\User;
use Illuminate\Support\Facades\Event;

Event::defer(function () {
    $user = User::create(['name' => 'Victoria Otwell']);

    $user->posts()->create(['title' => 'My first post!']);
});
```

클로저 내에서 발생한 모든 이벤트는 클로저가 실행된 이후에 디스패치됩니다. 이렇게 하면 이벤트 리스너가 클로저 내에서 생성된 모든 레코드에 접근할 수 있습니다. 만약 클로저 내에서 예외가 발생하면, 해당 이벤트는 디스패치되지 않습니다.

특정 이벤트만 지연시키고 싶을 경우, `defer` 메서드의 두 번째 인자로 이벤트 배열을 전달하면 됩니다:

```php
use App\Models\User;
use Illuminate\Support\Facades\Event;

Event::defer(function () {
    $user = User::create(['name' => 'Victoria Otwell']);

    $user->posts()->create(['title' => 'My first post!']);
}, ['eloquent.created: '.User::class]);
```

<a name="event-subscribers"></a>
## 이벤트 구독자 (Event Subscribers)

<a name="writing-event-subscribers"></a>
### 이벤트 구독자 작성

이벤트 구독자는 하나의 클래스 안에서 여러 이벤트를 구독하도록 설계된 클래스입니다. 이 구독자 클래스 내에서는 여러 이벤트 핸들러를 정의할 수 있습니다. 구독자는 반드시 `subscribe` 메서드를 정의해야 하며, 이 메서드는 이벤트 디스패처 인스턴스를 인자로 받습니다. 제공된 디스패처의 `listen` 메서드를 호출해 이벤트 리스너를 등록할 수 있습니다:

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

구독자 자체에 이벤트 리스너 메서드가 정의되어 있다면, `subscribe` 메서드에서 이벤트와 메서드명의 배열을 반환하는 방식이 더 편리할 수 있습니다. 이 경우, Laravel이 자동으로 구독자 클래스명을 가져옵니다:

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

구독자를 작성한 후, 해당 구독자가 [이벤트 디스커버리 규칙](#event-discovery)을 따르는 핸들러 메서드를 포함하고 있다면 Laravel이 자동으로 등록합니다. 그렇지 않을 경우, `Event` 파사드의 `subscribe` 메서드를 이용해 수동으로 구독자를 등록할 수 있습니다. 일반적으로 이 작업은 애플리케이션의 `AppServiceProvider`의 `boot` 메서드 안에서 이루어집니다:

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

이벤트를 디스패치하는 코드를 테스트할 때, 이벤트 리스너가 실제로 실행되지 않도록 하고 싶을 수 있습니다. 리스너의 코드는 별도로 테스트할 수 있고, 이벤트를 디스패치하는 코드와는 별도로 테스트하는 것이 좋기 때문입니다. 당연히 리스너 자체의 테스트를 위해서는 인스턴스를 직접 생성해 `handle` 메서드를 호출하면 됩니다.

`Event` 파사드의 `fake` 메서드를 이용하면, 리스너의 실행을 차단하고, 테스트 코드 내에서 실제 디스패치된 이벤트에 대해 `assertDispatched`, `assertNotDispatched`, `assertNothingDispatched` 메서드를 활용해 검증할 수 있습니다:

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

`assertDispatched` 또는 `assertNotDispatched` 메서드에 클로저를 전달하여, 특정 조건을 만족하는 이벤트가 디스패치되었는지 검증할 수 있습니다. 하나라도 해당 조건을 만족하는 이벤트가 디스패치되었다면, 검증에 성공합니다:

```php
Event::assertDispatched(function (OrderShipped $event) use ($order) {
    return $event->order->id === $order->id;
});
```

특정 이벤트에 대해 특정 리스너가 등록되어 있는지 테스트하려면, `assertListening` 메서드를 사용할 수 있습니다:

```php
Event::assertListening(
    OrderShipped::class,
    SendShipmentNotification::class
);
```

> [!WARNING]
> `Event::fake()`를 호출한 이후에는, 실제로 모든 이벤트 리스너가 실행되지 않습니다. 만일 테스트에서 모델 팩토리가 이벤트에 의존한다면(예를 들어, `creating` 이벤트에서 UUID를 생성하는 경우), 팩토리 사용 후에 `Event::fake()`를 호출해야 합니다.

<a name="faking-a-subset-of-events"></a>
### 일부 이벤트만 페이크로 처리하기

특정 이벤트에 대해서만 리스너를 페이크로 처리하고 싶을 경우, 해당 이벤트를 배열에 담아 `fake` 또는 `fakeFor` 메서드에 전달할 수 있습니다:

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

모든 이벤트를 페이크 처리하면서, 특정 이벤트만 예외로 둘 수도 있습니다. 이 경우 `except` 메서드를 사용할 수 있습니다:

```php
Event::fake()->except([
    OrderCreated::class,
]);
```

<a name="scoped-event-fakes"></a>
### 스코프별 이벤트 페이크

테스트 코드의 일부 구간에 대해서만 이벤트 리스너를 페이크 처리하고 싶을 경우에는, `fakeFor` 메서드를 사용할 수 있습니다:

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
