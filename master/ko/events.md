# 이벤트 (Events)

- [소개](#introduction)
- [이벤트와 리스너 생성하기](#generating-events-and-listeners)
- [이벤트와 리스너 등록하기](#registering-events-and-listeners)
    - [이벤트 자동 감지](#event-discovery)
    - [이벤트 수동 등록](#manually-registering-events)
    - [클로저 기반 리스너](#closure-listeners)
- [이벤트 정의하기](#defining-events)
- [리스너 정의하기](#defining-listeners)
- [큐 처리되는 이벤트 리스너](#queued-event-listeners)
    - [큐 직접 다루기](#manually-interacting-with-the-queue)
    - [큐 리스너와 데이터베이스 트랜잭션](#queued-event-listeners-and-database-transactions)
    - [큐 리스너 미들웨어](#queued-listener-middleware)
    - [암호화된 큐 리스너](#encrypted-queued-listeners)
    - [유일한 이벤트 리스너](#unique-event-listeners)
    - [실패한 작업 처리](#handling-failed-jobs)
- [이벤트 디스패치하기](#dispatching-events)
    - [데이터베이스 트랜잭션 이후 이벤트 디스패치](#dispatching-events-after-database-transactions)
    - [이벤트 지연 디스패치](#deferring-events)
- [이벤트 구독자](#event-subscribers)
    - [이벤트 구독자 작성](#writing-event-subscribers)
    - [이벤트 구독자 등록](#registering-event-subscribers)
- [테스트](#testing)
    - [특정 이벤트만 페이크 처리](#faking-a-subset-of-events)
    - [스코프 이벤트 페이크](#scoped-event-fakes)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel의 이벤트는 간단한 옵저버 패턴을 구현하여, 애플리케이션 내에서 발생하는 다양한 이벤트에 구독 및 리스닝할 수 있도록 지원합니다. 보통 이벤트 클래스는 `app/Events` 디렉터리에, 해당 이벤트를 처리하는 리스너는 `app/Listeners` 디렉터리에 저장합니다. 만약 애플리케이션에 이런 디렉터리가 없다면, Artisan 콘솔 명령어를 이용해 이벤트와 리스너를 생성할 때 자동으로 만들어집니다.

이벤트는 애플리케이션의 다양한 부분을 분리(디커플링)하는 데 탁월한 방법입니다. 하나의 이벤트에 여러 개의 리스너가 독립적으로 작동할 수 있기 때문입니다. 예를 들어, 주문이 발송될 때마다 사용자에게 Slack 알림을 보내고 싶을 수 있습니다. 주문 처리 코드와 Slack 알림 코드를 직접 연결하는 대신, `App\Events\OrderShipped` 이벤트를 발생시키고, 해당 이벤트를 수신하는 리스너에서 Slack 알림을 보낼 수 있습니다.

<a name="generating-events-and-listeners"></a>
## 이벤트와 리스너 생성하기 (Generating Events and Listeners)

이벤트와 리스너를 빠르게 생성하려면 `make:event` 및 `make:listener` Artisan 명령어를 사용할 수 있습니다:

```shell
php artisan make:event PodcastProcessed

php artisan make:listener SendPodcastNotification --event=PodcastProcessed
```

또한, 추가 인수 없이 `make:event` 및 `make:listener` 명령어를 실행하면, Laravel이 클래스명(리스너 생성 시에는 어떤 이벤트를 수신할지)을 프롬프트로 물어봅니다:

```shell
php artisan make:event

php artisan make:listener
```

<a name="registering-events-and-listeners"></a>
## 이벤트와 리스너 등록하기 (Registering Events and Listeners)

<a name="event-discovery"></a>
### 이벤트 자동 감지 (Event Discovery)

기본적으로 Laravel은 애플리케이션의 `Listeners` 디렉터리를 스캔하여 자동으로 이벤트 리스너를 찾고 등록합니다. 클래스의 메서드 중 `handle` 또는 `__invoke`로 시작하는 메서드를 발견하면, 해당 메서드 매개변수에 타입힌트로 지정된 이벤트를 자동으로 리스닝 대상으로 등록합니다:

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

PHP의 유니언 타입을 사용하면 여러 이벤트를 동시에 리스닝할 수 있습니다:

```php
/**
 * Handle the event.
 */
public function handle(PodcastProcessed|PodcastPublished $event): void
{
    // ...
}
```

리스너 클래스를 다른 디렉터리에 두거나 여러 디렉터리에 걸쳐 저장하려면, 애플리케이션의 `bootstrap/app.php` 파일에서 `withEvents` 메서드를 이용해 해당 디렉터리들을 지정할 수 있습니다:

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/Orders/Listeners',
])
```

`*` 와일드카드를 사용하여 여러 유사한 디렉터리를 한 번에 스캔할 수도 있습니다:

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/*/Listeners',
])
```

`event:list` 명령어를 사용하면, 애플리케이션에 등록된 모든 리스너 목록을 조회할 수 있습니다:

```shell
php artisan event:list
```

<a name="event-discovery-in-production"></a>
#### 운영 환경에서의 이벤트 자동 감지

애플리케이션의 성능을 높이기 위해, `optimize` 또는 `event:cache` Artisan 명령어를 사용해 모든 리스너의 목록(manifest)를 캐싱하는 것이 좋습니다. 보통 이 명령어는 애플리케이션의 [배포 과정](/docs/master/deployment#optimization)에서 실행됩니다. 이 manifest는 프레임워크가 이벤트 등록을 더 빠르게 처리할 수 있도록 도와줍니다. 이벤트 캐시를 제거하려면 `event:clear` 명령어를 사용합니다.

<a name="manually-registering-events"></a>
### 이벤트 수동 등록 (Manually Registering Events)

`Event` 파사드를 사용하면, 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 이벤트와 해당 리스너를 직접 등록할 수 있습니다:

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

모든 등록된 리스너의 목록은 `event:list` 명령어로 확인할 수 있습니다:

```shell
php artisan event:list
```

<a name="closure-listeners"></a>
### 클로저 기반 리스너 (Closure Listeners)

일반적으로 리스너는 클래스 형태이지만, 클로저(익명함수)로도 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 직접 등록할 수 있습니다:

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
#### 큐 처리되는 익명 이벤트 리스너 (Queueable Anonymous Event Listeners)

클로저 기반 리스너 등록 시, `Illuminate\Events\queueable` 함수를 통해 해당 리스너를 [큐](/docs/master/queues)로 실행하도록 지정할 수 있습니다:

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

큐 작업과 마찬가지로, `onConnection`, `onQueue`, `delay` 메서드를 이용해 큐 리스너의 실행 방식을 커스터마이즈할 수 있습니다:

```php
Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->onConnection('redis')->onQueue('podcasts')->delay(now()->plus(seconds: 10)));
```

익명 큐 리스너 실패 처리를 위해, `queueable` 리스너 정의 시 `catch` 메서드에 클로저를 전달할 수 있습니다. 이 클로저는 이벤트 인스턴스와 실패의 원인인 `Throwable` 인스턴스를 전달받습니다:

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
#### 와일드카드 이벤트 리스너 (Wildcard Event Listeners)

리스너를 등록할 때 `*` 문자를 와일드카드로 써서 여러 이벤트를 한 리스너에서 처리할 수 있습니다. 와일드카드 리스너는 첫 번째 인수로 이벤트명, 두 번째 인수로 전체 이벤트 데이터 배열을 받습니다:

```php
Event::listen('event.*', function (string $eventName, array $data) {
    // ...
});
```

<a name="defining-events"></a>
## 이벤트 정의하기 (Defining Events)

이벤트 클래스는 이벤트와 관련된 정보를 보관하는 데이터 컨테이너에 가깝습니다. 예를 들어, `App\Events\OrderShipped` 이벤트가 [Eloquent ORM](/docs/master/eloquent) 오브젝트를 받는다고 가정해봅니다:

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

이벤트 클래스는 별도의 실행 로직 없이, 구매된 `App\Models\Order` 인스턴스만 보관합니다. 이벤트에서 사용하는 `SerializesModels` 트레이트는, PHP의 `serialize` 함수를 통해 이벤트 오브젝트가 직렬화될 때(예: [큐 리스너](#queued-event-listeners) 사용 시) Eloquent 모델을 안전하게 직렬화/언직렬화할 수 있도록 도와줍니다.

<a name="defining-listeners"></a>
## 리스너 정의하기 (Defining Listeners)

다음으로, 앞서 예시로 든 이벤트를 처리하는 리스너를 살펴보겠습니다. 이벤트 리스너의 `handle` 메서드는 이벤트 인스턴스를 전달로 받습니다. `make:listener` Artisan 명령어를 `--event` 옵션과 함께 사용하면, 적절한 이벤트 클래스를 자동으로 import하고, `handle` 메서드에 타입힌트까지 지정해줍니다. `handle` 메서드 안에서, 이벤트에 대응한 원하는 작업을 수행하면 됩니다:

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
> 리스너 생성자에서 필요한 의존성은 타입힌트로 지정할 수 있습니다. 모든 리스너는 Laravel [서비스 컨테이너](/docs/master/container)를 통해 해석되므로 의존성이 자동 주입됩니다.

<a name="stopping-the-propagation-of-an-event"></a>
#### 이벤트 전파 중단하기

때때로 이벤트가 다른 리스너로 전파되지 않도록 하고 싶을 수 있습니다. 이럴 경우, 리스너의 `handle` 메서드에서 `false`를 반환하면 전파를 중단할 수 있습니다.

<a name="queued-event-listeners"></a>
## 큐 처리되는 이벤트 리스너 (Queued Event Listeners)

이메일 발송이나 HTTP 요청처럼 느린 작업을 하는 리스너는 큐로 처리하는 것이 유리합니다. 큐 리스너를 사용하기 전에는 [큐 설정](/docs/master/queues)을 마치고, 서버나 로컬 개발환경에서 큐 워커를 시작해야 합니다.

리스너를 큐에 넣으려면, 해당 리스너 클래스에 `ShouldQueue` 인터페이스를 구현하면 됩니다. `make:listener` Artisan 명령어로 생성된 리스너는 이미 이 인터페이스가 import 되어 있으므로 바로 사용할 수 있습니다:

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

이렇게 하면, 해당 리스너가 맡은 이벤트가 디스패치될 때마다 Laravel의 [큐 시스템](/docs/master/queues)을 통해 큐에 자동 등록되어 실행됩니다. 큐에서 리스너가 예외 없이 실행을 마치면, 해당 큐 작업은 자동으로 삭제됩니다.

<a name="customizing-the-queue-connection-queue-name"></a>
#### 큐 연결/이름/지연 시간 커스터마이즈

리스너 별로 큐 연결, 큐 이름, 큐 지연 시간을 커스터마이즈하려면, 리스너 클래스에 아래와 같이 `Connection`, `Queue`, `Delay` 속성을 지정할 수 있습니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\Attributes\Connection;
use Illuminate\Queue\Attributes\Delay;
use Illuminate\Queue\Attributes\Queue;

#[Connection('sqs')]
#[Queue('listeners')]
#[Delay(60)]
class SendShipmentNotification implements ShouldQueue
{
    // ...
}
```
런타임에 리스너의 큐 연결, 큐 이름, 지연 시간을 지정하려면 `viaConnection`, `viaQueue`, `withDelay` 메서드를 정의해주면 됩니다:

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
#### 조건부 큐 리스닝

런타임 데이터에 따라 리스너를 큐에 넣을지 결정해야 할 때는, 리스너 내에 `shouldQueue` 메서드를 구현하면 됩니다. 반환값이 `false`일 경우 해당 리스너는 큐에 등록되지 않습니다:

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

리스너 내부에서 큐 작업의 `delete`, `release` 메서드 등을 직접 호출해야 할 경우, `Illuminate\Queue\InteractsWithQueue` 트레이트를 사용하면 됩니다. 이 트레이트는 기본적으로 Artisan 명령어로 생성한 리스너에 이미 포함되어 있습니다:

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
### 큐 리스너와 데이터베이스 트랜잭션 (Queued Event Listeners and Database Transactions)

큐 리스너가 데이터베이스 트랜잭션 내에서 디스패치되는 경우, 트랜잭션 커밋 전 큐에서 리스너를 처리해버릴 수 있습니다. 이렇게 되면, 트랜잭션 안에서 변경된 데이터가 아직 DB에 반영되지 않은 상태이기 때문에, 그 데이터를 참조하는 리스너에서 예상치 못한 오류가 발생할 수 있습니다.

큐 연결의 `after_commit` 설정값이 `false`라면, 특정 리스너만 트랜잭션 커밋 후 디스패치되도록 하려면 리스너 클래스에 `ShouldQueueAfterCommit` 인터페이스를 구현하면 됩니다:

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
> 이 문제를 더 깊이 이해하려면, [큐 작업과 데이터베이스 트랜잭션](/docs/master/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="queued-listener-middleware"></a>
### 큐 리스너 미들웨어 (Queued Listener Middleware)

큐 리스너에서도 [작업 미들웨어](/docs/master/queues#job-middleware)를 사용할 수 있습니다. 작업 미들웨어는 큐 리스너의 실행 전후로 원하는 로직을 감쌀 수 있으므로, 리스너 본문 코드가 더 간결해집니다. 미들웨어를 만들고 나면, 리스너의 `middleware` 메서드를 통해 적용할 수 있습니다:

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
#### 암호화된 큐 리스너 (Encrypted Queued Listeners)

Laravel은 [암호화](/docs/master/encryption)를 통해, 큐 리스너의 데이터 프라이버시와 무결성을 보호할 수 있습니다. 리스너 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하면, 해당 리스너는 큐에 등록될 때 자동으로 암호화됩니다:

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
### 유일한 이벤트 리스너 (Unique Event Listeners)

> [!WARNING]
> 유일한 리스너는 [락(lock)](/docs/master/cache#atomic-locks)를 지원하는 캐시 드라이버에서만 사용할 수 있습니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버가 이를 지원합니다.

특정 리스너의 인스턴스가 한 번에 큐에 하나만 존재하도록 보장하고 싶을 때는, 리스너 클래스에 `ShouldBeUnique` 인터페이스를 구현하면 됩니다:

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

위 케이스에서 `AcquireProductKey` 리스너는 유일하게 동작하므로, 이미 큐에 동일 리스너가 실행 중이면 새로운 요청이 들어와도 큐에 추가되지 않습니다. 이렇게 하면 라이선스가 여러 번 저장되어도 하나의 제품키만 발급하게 할 수 있습니다.

특정 기준으로 유일성을 결정하거나, 유일 유지 시간을 정하고 싶을 때는 리스너 클래스에 `uniqueId`와 `uniqueFor` 속성이나 메서드를 정의하면 됩니다. 이 메서드들은 이벤트 인스턴스를 받아올 수 있으므로, 이벤트 데이터를 활용해 값을 만들 수 있습니다:

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

위 예시에서, `AcquireProductKey` 리스너의 유일성 기준은 라이선스 ID입니다. 따라서 동일 라이선스에 대해 기존 리스너가 작업을 마치기 전에는 새 리스너가 큐에 추가되지 않습니다. 또한, 만약 한 시간이 지나도 기존 리스너가 처리되지 않으면 unique 락이 풀리고, 동일한 키로 다시 큐에 등록할 수 있습니다.

> [!WARNING]
> 여러 웹 서버나 컨테이너에서 이벤트를 디스패치 하는 경우, 모든 서버가 동일한 중앙 캐시 서버를 사용해야만 Laravel이 리스너의 유일성을 제대로 판단할 수 있습니다.

기본적으로 Laravel은 기본 캐시 드라이버를 사용해 unique 락을 얻습니다. 다른 캐시 드라이버를 쓰고 싶다면, 리스너 클래스에 `uniqueVia` 메서드를 만들어 원하는 캐시 드라이버를 반환하게 할 수 있습니다:

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

큐 리스너가 실패하는 경우가 있을 수 있습니다. 리스너가 큐 워커에서 정의한 최대 재시도 횟수를 초과하면, 리스너의 `failed` 메서드가 호출됩니다. 이 메서드는 이벤트 인스턴스와 실패의 원인인 `Throwable` 인스턴스를 전달받습니다:

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

큐 리스너가 오류가 발생하면, 무한정 재시도 되는 것을 원치 않을 수 있습니다. Laravel은 리스너의 최대 재시도 횟수 또는 유효 시간을 지정하는 여러 방법을 제공합니다.

리스너 클래스에 `Tries` 속성을 사용하면, 큐 리스너가 실패로 간주되기 전까지 몇 번까지 재시도할 수 있는지 지정할 수 있습니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\Attributes\Tries;
use Illuminate\Queue\InteractsWithQueue;

#[Tries(5)]
class SendShipmentNotification implements ShouldQueue
{
    use InteractsWithQueue;

    // ...
}
```

횟수 대신 리스너가 더 이상 시도되지 않아야 할 시점을 지정하려면, 리스너 클래스에 `retryUntil` 메서드를 추가하면 됩니다. 이 메서드는 `DateTime` 인스턴스를 반환해야 하며, 해당 시점까지만 리스너를 재시도합니다:

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

`tries`와 `retryUntil`이 모두 정의되어 있으면, Laravel은 `retryUntil`의 값을 우선 적용합니다.

<a name="specifying-queued-listener-backoff"></a>
#### 큐 리스너 백오프(대기) 지정

큐 리스너가 예외로 인해 재시도 될 때, 얼마나 기다려야 할지 설정하고 싶다면, 리스너 클래스에 `Backoff` 속성을 사용할 수 있습니다:

```php
<?php

namespace App\Listeners;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\Attributes\Backoff;

#[Backoff(3)]
class SendShipmentNotification implements ShouldQueue
{
    // ...
}
```

좀 더 복잡하게 백오프 시간을 계산하고 싶다면, `backoff` 메서드를 정의할 수도 있습니다:

```php
/**
 * Calculate the number of seconds to wait before retrying the queued listener.
 */
public function backoff(OrderShipped $event): int
{
    return 3;
}
```

"지수형(exponential)" 백오프 적용이 필요하다면, 배열을 반환하면 됩니다. 예를 들어, 첫 재시도는 1초, 두번째는 5초, 세번째와 이후에는 10초씩 대기하게 할 수 있습니다:

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
#### 큐 리스너 허용 예외 최대치 지정

큐 리스너를 여러 번 재시도하더라도, 예외가 반복적으로 발생하면 실패로 간주하고 싶을 수 있습니다. 이럴 때는, 리스너 클래스에 `Tries`와 `MaxExceptions` 속성을 함께 선언하면 됩니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\Attributes\MaxExceptions;
use Illuminate\Queue\Attributes\Tries;
use Illuminate\Queue\InteractsWithQueue;

#[Tries(25)]
#[MaxExceptions(3)]
class SendShipmentNotification implements ShouldQueue
{
    use InteractsWithQueue;

    /**
     * Handle the event.
     */
    public function handle(OrderShipped $event): void
    {
        // Process the event...
    }
}
```

이렇게 하면, 해당 리스너는 최대 25회까지 재시도되지만, 3회 이상 예외가 발생하면 실패로 처리합니다.

<a name="specifying-queued-listener-timeout"></a>
#### 큐 리스너 타임아웃 지정

보통 큐 리스너가 대략 얼마나 오래 실행될지 예상할 수 있습니다. Laravel은 지정된 시간(seconds) 이상 동작하면 워커가 에러로 종료되게 하는 "타임아웃" 값을 설정할 수 있게 해줍니다. 리스너 클래스에 `Timeout` 속성을 선언해 타임아웃을 지정할 수 있습니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\Attributes\Timeout;

#[Timeout(120)]
class SendShipmentNotification implements ShouldQueue
{
    // ...
}
```

타임아웃 시 해당 리스너를 실패 처리하고 싶다면, `FailOnTimeout` 속성을 사용할 수 있습니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\Attributes\FailOnTimeout;

#[FailOnTimeout]
class SendShipmentNotification implements ShouldQueue
{
    // ...
}
```

<a name="dispatching-events"></a>
## 이벤트 디스패치하기 (Dispatching Events)

이벤트를 디스패치(발생)하려면 이벤트 클래스의 static `dispatch` 메서드를 호출하면 됩니다. 이 메서드는 `Illuminate\Foundation\Events\Dispatchable` 트레이트에서 제공되며, `dispatch`에 전달한 인수는 이벤트 생성자에 그대로 전달됩니다:

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

조건부로 이벤트를 디스패치하고 싶을 때는, `dispatchIf`와 `dispatchUnless` 메서드를 사용할 수 있습니다:

```php
OrderShipped::dispatchIf($condition, $order);

OrderShipped::dispatchUnless($condition, $order);
```

> [!NOTE]
> 테스트 시, 실제로 리스너가 실행되지 않으면서도 특정 이벤트가 디스패치 되었는지 확인하고 싶다면, Laravel의 [내장 테스트 헬퍼](#testing)를 참고하세요.

<a name="dispatching-events-after-database-transactions"></a>
### 데이터베이스 트랜잭션 이후 이벤트 디스패치 (Dispatching Events After Database Transactions)

경우에 따라, 현재 데이터베이스 트랜잭션이 커밋된 이후에만 이벤트가 디스패치되길 원할 때가 있습니다. 이를 위해, 이벤트 클래스에 `ShouldDispatchAfterCommit` 인터페이스를 구현하면 됩니다.

이 인터페이스가 구현된 이벤트는 트랜잭션이 커밋될 때까지 디스패치가 지연되고, 트랜잭션이 실패하면 이벤트는 버려집니다. 만약 트랜잭션이 없다면, 이벤트는 즉시 디스패치됩니다:

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

이벤트 지연(Deferred Event)을 통해, 특정 코드 블록이 끝난 후에만 모델 이벤트나 리스너를 실행할 수 있습니다. 이는 반드시 관련 레코드가 모두 생성된 후에 이벤트 리스너가 실행되게 하고 싶을 때 유용합니다.

이벤트 지연은 `Event::defer()` 메서드에 클로저를 넘기면 사용할 수 있습니다:

```php
use App\Models\User;
use Illuminate\Support\Facades\Event;

Event::defer(function () {
    $user = User::create(['name' => 'Victoria Otwell']);

    $user->posts()->create(['title' => 'My first post!']);
});
```

클로저 내부에서 발생하는 모든 이벤트는 클로저 실행이 끝난 후에 디스패치됩니다. 덕분에, 새로 생성된 모든 레코드에 리스너가 확실히 접근할 수 있습니다. 클로저 내부에서 예외가 발생하면, 지연된 이벤트는 디스패치되지 않습니다.

특정 이벤트만 지연하고 싶다면, 이벤트 배열을 `defer`의 두 번째 인수로 넘기면 됩니다:

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

이벤트 구독자는 여러 개의 이벤트를 한 클래스 내에서 구독, 처리할 수 있게 하는 클래스입니다. 하나의 구독자 클래스에서 여러 이벤트에 대한 핸들러를 정의하고 사용할 수 있습니다. 구독자에는 반드시 `subscribe` 메서드가 있어야 하며, 이 메서드는 이벤트 디스패처 인스턴스를 인수로 받습니다. 주어진 디스패처의 `listen` 메서드를 통해 이벤트 리스너를 등록할 수 있습니다:

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

구독자 내에 이벤트 리스너 메서드들이 정의되어 있다면, `subscribe` 메서드에서 이벤트-메서드 매핑을 배열로 반환하는 것도 가능합니다. 이 경우, 라라벨이 이벤트 리스너 등록 시 구독자의 클래스명을 자동으로 판단합니다:

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

구독자를 작성한 후에는, 구독자의 핸들러 메서드가 [이벤트 감지 규칙](#event-discovery)을 따르기만 하면 Laravel이 자동으로 등록합니다. 그렇지 않은 경우, `Event` 파사드의 `subscribe` 메서드를 통해 직접 등록할 수 있습니다. 주로 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 수행합니다:

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

이벤트를 디스패치하는 코드를 테스트할 때는, 실제 리스너까지 실행하지 않도록 하고 싶을 수 있습니다. 리스너 코드는 별도의 테스트가 가능하니까요. 리스너 자체를 테스트할 때는, 리스너 인스턴스를 직접 생성해서 `handle` 메서드를 호출하면 됩니다.

`Event` 파사드의 `fake` 메서드를 이용하면, 리스너 실행 없이 테스트 대상 코드를 수행한 뒤, `assertDispatched`, `assertNotDispatched`, `assertNothingDispatched` 메서드로 어떤 이벤트들이 디스패치됐는지 검증할 수 있습니다:

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

`assertDispatched`, `assertNotDispatched` 메서드에는 클로저를 인수로 넘겨, "특정 조건"을 만족하는 이벤트가 디스패치됐는지도 확인할 수 있습니다. 조건을 만족하는 이벤트가 하나라도 디스패치됐다면 검증에 성공합니다:

```php
Event::assertDispatched(function (OrderShipped $event) use ($order) {
    return $event->order->id === $order->id;
});
```

특정 리스너가 지정된 이벤트를 리스닝하는지 검증하려면, `assertListening` 메서드를 사용할 수 있습니다:

```php
Event::assertListening(
    OrderShipped::class,
    SendShipmentNotification::class
);
```

> [!WARNING]
> `Event::fake()`를 호출하면 모든 이벤트 리스너가 실행되지 않습니다. 따라서, 모델의 `creating` 이벤트 등에서 UUID 생성 등에 의존하는 팩토리를 사용한다면, factory 사용 **이후에** `Event::fake()`를 호출해야 합니다.

<a name="faking-a-subset-of-events"></a>
### 특정 이벤트만 페이크 처리 (Faking a Subset of Events)

특정 이벤트에 한해서만 리스너가 실행되지 않게 하려면, 해당 이벤트들을 `fake` 또는 `fakeFor` 메서드에 배열로 전달합니다:

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

반대로, 지정한 이벤트만 제외하고 나머지를 모두 페이크 처리하려면 `except` 메서드를 사용합니다:

```php
Event::fake()->except([
    OrderCreated::class,
]);
```

<a name="scoped-event-fakes"></a>
### 스코프 이벤트 페이크 (Scoped Event Fakes)

테스트의 특정 부분에서만 이벤트 리스너를 페이크 처리하고 싶다면, `fakeFor` 메서드를 사용할 수 있습니다:

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
