# 이벤트 (Events)

- [소개](#introduction)
- [이벤트와 리스너 생성](#generating-events-and-listeners)
- [이벤트와 리스너 등록](#registering-events-and-listeners)
    - [이벤트 자동 감지](#event-discovery)
    - [이벤트 수동 등록](#manually-registering-events)
    - [클로저 리스너](#closure-listeners)
- [이벤트 정의](#defining-events)
- [리스너 정의](#defining-listeners)
- [큐잉된(Queued) 이벤트 리스너](#queued-event-listeners)
    - [큐 직접 다루기](#manually-interacting-with-the-queue)
    - [큐잉된 리스너와 DB 트랜잭션](#queued-event-listeners-and-database-transactions)
    - [큐잉된 리스너 미들웨어](#queued-listener-middleware)
    - [암호화된 큐잉 리스너](#encrypted-queued-listeners)
    - [실패한 작업 처리](#handling-failed-jobs)
- [이벤트 디스패치](#dispatching-events)
    - [DB 트랜잭션 이후 이벤트 디스패치](#dispatching-events-after-database-transactions)
- [이벤트 구독자](#event-subscribers)
    - [이벤트 구독자 작성](#writing-event-subscribers)
    - [이벤트 구독자 등록](#registering-event-subscribers)
- [테스트](#testing)
    - [일부 이벤트 페이크(Faking)](#faking-a-subset-of-events)
    - [스코프드 이벤트 페이크(Scoped Events Fakes)](#scoped-event-fakes)

<a name="introduction"></a>
## 소개

라라벨의 이벤트(Event) 시스템은 간단한 옵서버 패턴을 제공합니다. 이를 활용해 애플리케이션 내에서 발생하는 다양한 이벤트에 구독(subscribe)하고 리스닝(listen)할 수 있습니다. 일반적으로 이벤트 클래스는 `app/Events` 디렉터리에, 해당 이벤트를 처리하는 리스너는 `app/Listeners` 디렉터리에 저장합니다. 만약 이 디렉터리가 이미 프로젝트 내에 없다면 걱정하지 않으셔도 됩니다. Artisan 콘솔 명령어로 이벤트와 리스너를 생성하면 자동으로 만들어집니다.

이벤트를 활용하면 애플리케이션의 여러 요소를 느슨하게 결합(decoupling)할 수 있습니다. 하나의 이벤트에 여러 리스너를 등록할 수 있지만, 이 리스너들은 서로 직접적으로 의존하지 않습니다. 예를 들어, 주문이 발송될 때마다 사용자의 Slack으로 알림을 보내고 싶다고 가정해 보겠습니다. 주문 처리 코드와 Slack 알림 코드를 직접 연결하는 대신, `App\Events\OrderShipped` 이벤트를 발생시키고, 리스너에서는 이 이벤트를 받아 Slack 알림을 전송할 수 있습니다.

<a name="generating-events-and-listeners"></a>
## 이벤트와 리스너 생성

이벤트와 리스너는 `make:event`와 `make:listener` Artisan 명령어로 빠르게 생성할 수 있습니다.

```shell
php artisan make:event PodcastProcessed

php artisan make:listener SendPodcastNotification --event=PodcastProcessed
```

더 간편하게, 추가 인수 없이 `make:event`나 `make:listener` 명령어를 실행할 수 있습니다. 이 경우, 라라벨이 클래스 이름(리스너의 경우, 어떤 이벤트를 리스닝할지) 입력을 안내해 줍니다.

```shell
php artisan make:event

php artisan make:listener
```

<a name="registering-events-and-listeners"></a>
## 이벤트와 리스너 등록

<a name="event-discovery"></a>
### 이벤트 자동 감지

라라벨은 기본적으로 애플리케이션의 `Listeners` 디렉터리를 스캔하여 이벤트 리스너를 자동으로 감지하고 등록합니다. 리스너 클래스 메서드가 `handle` 또는 `__invoke`로 시작하면, 해당 메서드에 시그니처로 명시된 이벤트 타입에 따라 리스너로 자동 등록됩니다.

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

PHP의 유니언 타입(union types)을 사용하면 여러 이벤트를 하나의 리스너로 처리할 수도 있습니다.

```php
/**
 * Handle the event.
 */
public function handle(PodcastProcessed|PodcastPublished $event): void
{
    // ...
}
```

리스너를 다른 디렉터리(혹은 여러 디렉터리)에서 관리하고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에서 `withEvents` 메서드를 사용해 해당 디렉터리도 스캔하도록 라라벨에 지시할 수 있습니다.

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/Orders/Listeners',
])
```

`*` 문자를 와일드카드로 사용해 비슷한 여러 디렉터리를 한 번에 스캔할 수도 있습니다.

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/*/Listeners',
])
```

애플리케이션에 등록된 모든 리스너 목록은 `event:list` 명령어로 확인 가능합니다.

```shell
php artisan event:list
```

<a name="event-discovery-in-production"></a>
#### 운영 환경에서 이벤트 감지

애플리케이션의 성능을 높이기 위해, `optimize` 또는 `event:cache` Artisan 명령어로 모든 리스너 목록을 캐싱(최적화)해 둘 것을 권장합니다. 보통 이 명령어는 애플리케이션의 [배포 과정](/docs/12.x/deployment#optimization)에서 실행해야 합니다. 캐싱된 매니페스트는 이벤트 등록 속도를 높여줍니다. 이벤트 캐시를 초기화(삭제)할 때는 `event:clear` 명령어를 사용하세요.

<a name="manually-registering-events"></a>
### 이벤트 수동 등록

`Event` 파사드를 사용하면, `AppServiceProvider`의 `boot` 메서드 등에서 직접 이벤트와 리스너를 등록할 수도 있습니다.

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

현재 애플리케이션에 등록된 모든 리스너를 확인하려면 `event:list` 명령어를 사용할 수 있습니다.

```shell
php artisan event:list
```

<a name="closure-listeners"></a>
### 클로저 리스너

일반적으로 리스너는 클래스로 정의되지만, `AppServiceProvider`의 `boot` 메서드에서 클로저(익명 함수) 기반 이벤트 리스너를 수동으로 등록할 수도 있습니다.

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

클로저 기반 이벤트 리스너를 등록할 때, 클로저를 `Illuminate\Events\queueable` 함수로 감싸면 해당 리스너를 [큐](/docs/12.x/queues)에서 비동기로 처리하도록 만들 수 있습니다.

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

큐잉된 작업처럼, `onConnection`, `onQueue`, `delay` 메서드를 조합해 큐의 연결, 이름, 실행 지연 시간을 설정할 수 있습니다.

```php
Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->onConnection('redis')->onQueue('podcasts')->delay(now()->addSeconds(10)));
```

익명 큐 리스너가 실패할 때 처리 로직을 추가하고 싶다면, `queueable` 리스너를 정의할 때 `catch` 메서드에 클로저를 전달할 수 있습니다. 이 클로저는 이벤트 인스턴스와 에러의 원인이 된 `Throwable` 인스턴스를 인자로 받습니다.

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

`*` 문자를 와일드카드로 사용해 여러 이벤트를 하나의 리스너에서 처리할 수도 있습니다. 와일드카드 리스너는 첫 번째 인자로 이벤트 이름, 두 번째 인자로 전체 이벤트 데이터 배열을 받습니다.

```php
Event::listen('event.*', function (string $eventName, array $data) {
    // ...
});
```

<a name="defining-events"></a>
## 이벤트 정의

이벤트 클래스는 기본적으로 해당 이벤트에 관련된 정보를 담는 데이터 컨테이너 역할을 합니다. 예를 들어, `App\Events\OrderShipped` 이벤트에는 [Eloquent ORM](/docs/12.x/eloquent) 객체가 담길 수 있습니다.

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

보시다시피, 이 이벤트 클래스는 로직을 담지 않습니다. 단순히 구매된 `App\Models\Order` 인스턴스를 저장하는 역할만 합니다. 이벤트에서 사용하는 `SerializesModels` 트레잇은 이벤트 객체를 PHP의 `serialize` 함수 등으로 직렬화할 때, Eloquent 모델을 알맞게 직렬화해 줍니다. 이는 [큐잉된 리스너](#queued-event-listeners)에서 활용됩니다.

<a name="defining-listeners"></a>
## 리스너 정의

다음으로, 방금 예시의 이벤트를 처리하는 리스너를 살펴보겠습니다. 이벤트 리스너 클래스의 `handle` 메서드는 해당 이벤트 인스턴스를 인자로 받습니다. `make:listener` Artisan 명령어를 사용할 때 `--event` 옵션을 지정하면, 올바른 이벤트 클래스 임포트 및 타입 힌트가 자동으로 추가됩니다. `handle` 메서드 내부에서는 이벤트에 대응하는 모든 작업을 자유롭게 구현할 수 있습니다.

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
> 이벤트 리스너의 생성자(constructor)에서도 필요한 의존성을 타입-힌트로 명시할 수 있습니다. 모든 이벤트 리스너는 라라벨 [서비스 컨테이너](/docs/12.x/container)를 통해 자동으로 resolving(의존성 주입)됩니다.

<a name="stopping-the-propagation-of-an-event"></a>
#### 이벤트 전파 중단

때로는 한 리스너가 이벤트의 추가 전파를 중단시키고 싶을 때가 있습니다. 이럴 땐 리스너의 `handle` 메서드에서 `false`를 반환해 주면 됩니다.

<a name="queued-event-listeners"></a>
## 큐잉된(Queued) 이벤트 리스너

이메일 전송이나 HTTP 요청처럼, 리스너에서 시간이 오래 걸릴 수 있는 작업이 있을 때 큐잉을 사용하는 것이 좋습니다. 큐잉된 리스너를 사용하기 전에는 [큐 설정](/docs/12.x/queues)을 마치고, 서버(또는 로컬 개발 환경)에서 큐 워커가 실행 중이어야 합니다.

리스너에 `ShouldQueue` 인터페이스를 구현(implement)하면 자동으로 큐잉됩니다. Artisan의 `make:listener` 명령어로 생성하는 경우, 이미 `ShouldQueue`가 네임스페이스에 임포트되어 있으므로 바로 사용할 수 있습니다.

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

이제 이 리스너에서 처리해야 할 이벤트가 발생하면, 이벤트 디스패처가 자동으로 [큐 시스템](/docs/12.x/queues)을 이용해 리스너를 큐에 넣어 비동기로 실행합니다. 리스너 실행 중 예외가 발생하지 않으면, 큐에 추가된 작업은 처리 후 자동 삭제됩니다.

<a name="customizing-the-queue-connection-queue-name"></a>
#### 큐 연결, 큐 이름, 딜레이 시간 커스터마이징

이벤트 리스너가 사용할 큐 연결(connection), 큐 이름(name), 큐 지연(delay) 시간을 커스터마이징하고 싶다면 리스너 클래스에 `$connection`, `$queue`, `$delay` 속성을 선언하면 됩니다.

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

큐 연결(connection), 큐 이름(name), 실행 지연(delay) 값을 런타임에 동적으로 지정하고 싶다면, `viaConnection`, `viaQueue`, `withDelay` 등의 메서드를 리스너 클래스에 추가하면 됩니다.

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

때로는 실제 런타임 데이터에 따라 리스너를 큐잉할지 결정해야 할 수 있습니다. 이럴 때는, 리스너에 `shouldQueue` 메서드를 정의하고, 여기서 `false`를 반환하면 해당 리스너는 큐잉되지 않습니다.

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

리스너의 큐 작업에서 `delete`, `release`와 같은 메서드를 직접 사용해야 하는 경우, `Illuminate\Queue\InteractsWithQueue` 트레잇을 활용할 수 있습니다. 이 트레잇은 생성된 리스너에 기본적으로 포함되어 있어, 해당 메서드에 접근할 수 있습니다.

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
### 큐잉된 리스너와 DB 트랜잭션

DB 트랜잭션 중에 큐잉된 리스너가 디스패치되면, 큐가 트랜잭션 커밋 전에 해당 리스너를 처리할 수 있습니다. 이런 경우, 트랜잭션 안에서 변경한 모델이나 DB 레코드가 아직 DB에 반영되지 않았을 수 있습니다. 트랜잭션 내에서 새로 만든 모델이나 레코드 역시 DB에 존재하지 않을 수도 있습니다. 만약 리스너가 이 모델들에 의존한다면, 큐 작업 실행 시 예기치 않은 에러가 발생할 수 있습니다.

큐 연결의 `after_commit` 설정 값이 `false`인 경우, 리스너 클래스에서 `ShouldQueueAfterCommit` 인터페이스를 구현함으로써 해당 리스너가 모든 오픈된 트랜잭션 커밋 이후에 디스패치되도록 지정할 수 있습니다.

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
> 이 문제를 더 깊이 다루는 방법이 궁금하다면, [큐잉된 작업과 DB 트랜잭션](/docs/12.x/queues#jobs-and-database-transactions) 문서를 참고하십시오.

<a name="queued-listener-middleware"></a>
### 큐잉된 리스너 미들웨어

큐잉된 리스너에도 [작업 미들웨어](/docs/12.x/queues#job-middleware)를 적용할 수 있습니다. 작업 미들웨어는 큐잉된 리스너 실행 전후로 커스텀 로직을 감쌀 수 있어, 리스너 내부의 중복 코드를 줄일 수 있습니다. 미들웨어를 만든 뒤, 리스너의 `middleware` 메서드에서 배열로 반환하면 해당 미들웨어가 적용됩니다.

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
#### 암호화된 큐잉 리스너

라라벨은 [암호화](/docs/12.x/encryption)를 이용해 큐잉된 리스너의 데이터의 기밀성과 무결성을 보장할 수 있습니다. 시작하려면 리스너 클래스에 `ShouldBeEncrypted` 인터페이스만 추가하면 됩니다. 이렇게 하면 라라벨이 해당 리스너를 큐에 넣기 전에 자동으로 암호화합니다.

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

가끔 큐에 등록한 이벤트 리스너가 실패할 수도 있습니다. 큐잉된 리스너가 큐 워커에서 지정한 최대 재시도 횟수를 초과하면, 리스너의 `failed` 메서드가 호출됩니다. 이 메서드는 이벤트 인스턴스와 실패의 원인이 된 `Throwable` 객체를 인자로 받습니다.

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
#### 큐잉 리스너의 최대 재시도 횟수 지정

큐잉된 리스너가 오류를 만났을 때 무한정 재시도하는 것을 원하지 않을 때가 있습니다. 라라벨은 몇 번까지, 또는 얼마 동안 리스너를 재시도할지 다양하게 지정할 수 있습니다.

리스너 클래스에 `tries` 속성을 선언하면, 해당 리스너는 최대 지정한 횟수까지만 시도 후 실패로 간주됩니다.

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

실패 전 최대 시도 횟수 대신, 특정 시간까지만 재시도하도록 지정하고 싶을 수도 있습니다. 이 경우 리스너 클래스에 `retryUntil` 메서드를 추가하면 되며, 이 메서드는 `DateTime` 인스턴스를 반환해야 합니다.

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

`retryUntil`과 `tries`를 모두 정의하는 경우에는 `retryUntil`이 우선 적용됩니다.

<a name="specifying-queued-listener-backoff"></a>
#### 큐잉 리스너의 백오프(backoff) 지정

리스너가 예외로 인해 실패한 후 다시 재시도하기 전, 몇 초 동안 대기할지 설정하려면 리스너 클래스에 `backoff` 속성을 선언할 수 있습니다.

```php
/**
 * The number of seconds to wait before retrying the queued listener.
 *
 * @var int
 */
public $backoff = 3;
```

보다 복잡한 백오프 로직이 필요하다면, `backoff` 메서드를 정의해 상황에 따라 유동적으로 결정할 수 있습니다.

```php
/**
 * Calculate the number of seconds to wait before retrying the queued listener.
 */
public function backoff(OrderShipped $event): int
{
    return 3;
}
```

"지수(exponential) 백오프" 처럼 점진적 지연을 쉽게 구현하려면, `backoff` 메서드에서 백오프 값을 배열로 반환하면 됩니다. 아래 예시에서는 첫 번째 재시도 1초, 두 번째 5초, 세 번째 이후 10초의 지연이 적용됩니다.

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

여러 번 재시도는 허용하지만, 처리 과정에서 미처 처리하지 못한 예외가 일정 횟수를 넘어서면 즉시 실패 처리하고 싶을 때가 있습니다. 이럴 때는 리스너 클래스에 `maxExceptions` 속성을 정의하면 됩니다.

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

이 예시에서는, 리스너는 최대 25회까지 시도할 수 있지만 처리 중 미처 처리하지 못한 예외가 3번 발생하면 즉시 실패로 처리됩니다.

<a name="specifying-queued-listener-timeout"></a>
#### 큐잉 리스너 실행 타임아웃 지정

대부분의 경우, 큐잉된 리스너가 어느 정도 시간 내로 처리되어야 하는지 예측할 수 있습니다. 라라벨은 이러한 상황을 위해 "타임아웃(timeout)" 값을 지정하는 기능을 제공합니다. 만약 리스너가 지정한 시간(초)보다 더 오래 실행되면, 이를 처리하던 워커는 에러와 함께 종료됩니다. 리스너 클래스에 `timeout` 속성을 지정하면 됩니다.

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

타임아웃 발생 시 해당 리스너를 실패로 간주하도록 하려면, 리스너 클래스에 `failOnTimeout` 속성을 true로 지정할 수 있습니다.

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

## 이벤트 디스패치하기

이벤트를 디스패치하려면 해당 이벤트의 정적 `dispatch` 메서드를 호출하면 됩니다. 이 메서드는 이벤트 클래스에 `Illuminate\Foundation\Events\Dispatchable` 트레이트가 포함되어 있을 때 사용할 수 있습니다. `dispatch` 메서드에 전달한 인수들은 해당 이벤트의 생성자로 그대로 전달됩니다.

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

이벤트를 조건적으로 디스패치하고 싶다면, `dispatchIf`와 `dispatchUnless` 메서드를 사용할 수 있습니다.

```php
OrderShipped::dispatchIf($condition, $order);

OrderShipped::dispatchUnless($condition, $order);
```

> [!NOTE]
> 테스트 시에는 실제로 리스너를 실행하지 않고 어떤 이벤트가 디스패치되었는지 검증할 수 있으며, 라라벨의 [내장 테스트 헬퍼](#testing)를 사용하면 매우 간편하게 처리할 수 있습니다.

<a name="dispatching-events-after-database-transactions"></a>
### 데이터베이스 트랜잭션 이후에 이벤트 디스패치하기

가끔은 라라벨이 현재 진행 중인 데이터베이스 트랜잭션이 커밋된 이후에만 이벤트를 디스패치하도록 하고 싶을 수 있습니다. 이 경우, 이벤트 클래스에 `ShouldDispatchAfterCommit` 인터페이스를 구현하면 됩니다.

이 인터페이스를 구현하면, 라라벨은 현재 트랜잭션이 커밋될 때까지 해당 이벤트를 디스패치하지 않습니다. 만약 트랜잭션이 실패하면, 이벤트는 폐기됩니다. 이벤트가 디스패치될 때 진행 중인 트랜잭션이 없다면, 이벤트는 즉시 디스패치됩니다.

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
## 이벤트 구독자

<a name="writing-event-subscribers"></a>
### 이벤트 구독자 클래스 작성하기

이벤트 구독자(event subscriber)는 하나의 클래스 안에서 여러 이벤트를 한 번에 구독할 수 있도록 해 주는 클래스입니다. 즉, 한 클래스 안에 여러 이벤트 핸들러를 정의할 수 있습니다. 구독자 클래스에는 반드시 `subscribe` 메서드를 구현해야 하며, 이 메서드는 이벤트 디스패처 인스턴스를 매개변수로 받습니다. 전달받은 디스패처 인스턴스의 `listen` 메서드를 호출하여 이벤트 리스너를 등록할 수 있습니다.

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

구독자 내에 정의된 이벤트 리스너 메서드들을 배열 형태로 `subscribe` 메서드에서 반환하도록 할 수도 있습니다. 이렇게 하면 라라벨이 이벤트 리스너 등록 시 알아서 해당 구독자 클래스명을 사용합니다.

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

구독자 클래스를 작성한 후, 해당 클래스의 메서드 이름이 라라벨의 [이벤트 디스커버리 규칙](#event-discovery)을 따르고 있다면 라라벨이 자동으로 구독자 안의 핸들러 메서드를 등록해 줍니다. 하지만 그렇지 않은 경우라면, `Event` 파사드의 `subscribe` 메서드를 통해 직접 등록할 수 있습니다. 보통은 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드 안에서 등록하면 됩니다.

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

이벤트를 디스패치하는 코드를 테스트할 때는, 리스너의 실행을 막을 수 있습니다. 왜냐하면 리스너의 코드는 별도의 테스트에서 직접 검증할 수 있기 때문입니다. 리스너를 테스트할 때는 리스너 인스턴스를 직접 생성하고, `handle` 메서드를 테스트 코드에서 호출하면 됩니다.

`Event` 파사드의 `fake` 메서드를 사용하면 이벤트 리스너의 실행을 막고, 테스트할 코드만 실행한 다음, `assertDispatched`, `assertNotDispatched`, `assertNothingDispatched` 등의 메서드로 어떤 이벤트가 디스패치되었는지 검증할 수 있습니다.

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

`assertDispatched`와 `assertNotDispatched` 메서드에 클로저를 전달하여, 특정 "조건(true/false 판별)"을 만족하는 이벤트가 디스패치되었는지 검증할 수도 있습니다. 최소 하나라도 해당 조건을 만족하면 검증이 성공합니다.

```php
Event::assertDispatched(function (OrderShipped $event) use ($order) {
    return $event->order->id === $order->id;
});
```

특정 이벤트에 대해 어떤 리스너가 제대로 연결되어 있는지만 검증하고 싶다면 `assertListening` 메서드를 사용할 수 있습니다.

```php
Event::assertListening(
    OrderShipped::class,
    SendShipmentNotification::class
);
```

> [!WARNING]
> `Event::fake()`를 호출하면, 이벤트 리스너는 실행되지 않습니다. 따라서, 모델의 `creating` 이벤트 등에서 UUID 생성 등 이벤트에 의존하는 모델 팩토리를 사용할 경우, 팩토리 사용 이후에 `Event::fake()`를 호출해야 합니다.

<a name="faking-a-subset-of-events"></a>
### 일부 이벤트만 페이크하기

특정 이벤트에 대해서만 리스너 실행을 막고 싶을 때, `fake` 또는 `fakeFor` 메서드에 해당 이벤트들의 클래스를 배열로 전달할 수 있습니다.

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

특정 이벤트들을 제외한 *모든* 이벤트에 대해서만 페이크를 적용하려면, `except` 메서드를 사용할 수 있습니다.

```php
Event::fake()->except([
    OrderCreated::class,
]);
```

<a name="scoped-event-fakes"></a>
### 테스트 범위에서만 이벤트 페이크 적용하기

테스트의 일부 영역에만 이벤트 페이크를 적용하고 싶다면, `fakeFor` 메서드를 활용하면 됩니다.

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