# 이벤트 (Events)

- [소개](#introduction)
- [이벤트 및 리스너 생성](#generating-events-and-listeners)
- [이벤트 및 리스너 등록](#registering-events-and-listeners)
    - [이벤트 자동 탐색](#event-discovery)
    - [이벤트 수동 등록](#manually-registering-events)
    - [클로저 리스너](#closure-listeners)
- [이벤트 정의](#defining-events)
- [리스너 정의](#defining-listeners)
- [큐잉되는 이벤트 리스너](#queued-event-listeners)
    - [큐 직접 제어하기](#manually-interacting-with-the-queue)
    - [큐잉 리스너와 데이터베이스 트랜잭션](#queued-event-listeners-and-database-transactions)
    - [큐잉 리스너 미들웨어](#queued-listener-middleware)
    - [암호화된 큐잉 리스너](#encrypted-queued-listeners)
    - [실패한 작업 처리](#handling-failed-jobs)
- [이벤트 디스패치](#dispatching-events)
    - [데이터베이스 트랜잭션 이후 이벤트 디스패치](#dispatching-events-after-database-transactions)
- [이벤트 구독자](#event-subscribers)
    - [이벤트 구독자 작성](#writing-event-subscribers)
    - [이벤트 구독자 등록](#registering-event-subscribers)
- [테스트](#testing)
    - [특정 이벤트만 가짜로 만들기](#faking-a-subset-of-events)
    - [스코프별 이벤트 가짜 처리](#scoped-event-fakes)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel의 이벤트는 간단한 옵저버 패턴을 구현하여, 애플리케이션 내에서 발생하는 다양한 이벤트에 구독하고 리스닝할 수 있도록 해줍니다. 이벤트 클래스는 일반적으로 `app/Events` 디렉토리에, 리스너는 `app/Listeners` 디렉토리에 저장합니다. 만약 애플리케이션에 해당 디렉토리가 없다면, Artisan 콘솔 명령어를 통해 이벤트와 리스너를 생성할 때 자동으로 만들어집니다.

이벤트는 여러 부분의 코드를 분리하는 데 매우 유용합니다. 하나의 이벤트에 여러 리스너를 부착할 수 있고, 각각은 서로 독립적으로 동작합니다. 예를 들어, 주문이 발송될 때마다 사용자의 Slack에 알림을 보내고 싶을 수 있습니다. 이 경우 주문 처리 코드와 Slack 알림 코드를 직접 연결하지 않고, `App\Events\OrderShipped` 이벤트를 발생시키면 해당 이벤트를 리스닝하는 리스너에서 Slack 알림을 전송할 수 있습니다.

<a name="generating-events-and-listeners"></a>
## 이벤트 및 리스너 생성 (Generating Events and Listeners)

이벤트와 리스너를 빠르게 생성하려면, `make:event`와 `make:listener` Artisan 명령어를 사용할 수 있습니다:

```shell
php artisan make:event PodcastProcessed

php artisan make:listener SendPodcastNotification --event=PodcastProcessed
```

편의상, 추가 인자 없이 `make:event` 또는 `make:listener` Artisan 명령어를 실행할 수도 있습니다. 이 경우 Laravel이 자동으로 클래스 이름을 입력받으며, 리스너를 만들 때는 어떤 이벤트를 리스닝할지도 물어봅니다:

```shell
php artisan make:event

php artisan make:listener
```

<a name="registering-events-and-listeners"></a>
## 이벤트 및 리스너 등록 (Registering Events and Listeners)

<a name="event-discovery"></a>
### 이벤트 자동 탐색 (Event Discovery)

기본적으로 Laravel은 애플리케이션의 `Listeners` 디렉토리를 스캔하여 이벤트 리스너를 자동으로 찾고 등록합니다. Laravel이 `handle` 또는 `__invoke`로 시작하는 메서드를 리스너 클래스에서 발견하면, 메서드 시그니처에 타입힌트된 이벤트에 해당 메서드를 자동으로 리스너로 등록합니다:

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

리스너를 다른 디렉토리, 또는 여러 디렉토리에 저장하려는 경우, 애플리케이션의 `bootstrap/app.php` 파일에서 `withEvents` 메서드를 사용해 해당 디렉토리도 스캔하도록 지정할 수 있습니다:

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/Orders/Listeners',
])
```

`*` 문자를 와일드카드로 사용하여 여러 유사한 디렉토리를 동시에 스캔할 수도 있습니다:

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/*/Listeners',
])
```

`event:list` 명령어를 사용하면 애플리케이션 내에 등록된 모든 리스너를 나열할 수 있습니다:

```shell
php artisan event:list
```

<a name="event-discovery-in-production"></a>
#### 운영 환경에서의 이벤트 자동 탐색

애플리케이션의 성능 향상을 위해 `optimize` 또는 `event:cache` Artisan 명령어를 사용해 모든 리스너의 매니페스트를 캐싱해야 합니다. 일반적으로 이 명령어는 [배포 프로세스](/docs/12.x/deployment#optimization)에 포함되어야 합니다. 이 매니페스트를 통해 프레임워크가 이벤트 등록 과정을 더욱 빠르게 처리할 수 있습니다. 캐시를 지우려면 `event:clear` 명령어를 사용하십시오.

<a name="manually-registering-events"></a>
### 이벤트 수동 등록 (Manually Registering Events)

`Event` 파사드를 이용하면, 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 이벤트와 해당 리스너를 직접 수동으로 등록할 수도 있습니다:

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

`event:list` 명령어로 등록된 모든 리스너를 확인할 수 있습니다:

```shell
php artisan event:list
```

<a name="closure-listeners"></a>
### 클로저 리스너 (Closure Listeners)

일반적으로 리스너는 클래스로 정의하지만, `AppServiceProvider`의 `boot` 메서드에서 클로저 기반 이벤트 리스너를 직접 등록할 수도 있습니다:

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
#### 큐잉되는 익명 이벤트 리스너 (Queueable Anonymous Event Listeners)

클로저 기반 이벤트 리스너를 등록할 때, `Illuminate\Events\queueable` 함수를 사용해 리스너 클로저를 감싸면 해당 리스너가 [큐](/docs/12.x/queues)를 통해 실행되도록 지정할 수 있습니다:

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

큐에 등록된 작업과 마찬가지로, `onConnection`, `onQueue`, `delay` 메서드로 큐잉 리스너의 실행 방식을 커스터마이즈할 수 있습니다:

```php
Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->onConnection('redis')->onQueue('podcasts')->delay(now()->addSeconds(10)));
```

익명 큐잉 리스너에서 실패 처리를 하고 싶다면, `queueable` 리스너를 정의할 때 `catch` 메서드에 클로저를 전달할 수 있습니다. 이 클로저는 이벤트 인스턴스와 리스너가 실패하게 만든 `Throwable` 인스턴스를 전달받습니다:

```php
use App\Events\PodcastProcessed;
use function Illuminate\Events\queueable;
use Illuminate\Support\Facades\Event;
use Throwable;

Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->catch(function (PodcastProcessed $event, Throwable $e) {
    // 큐잉 리스너가 실패한 경우의 처리...
}));
```

<a name="wildcard-event-listeners"></a>
#### 와일드카드 이벤트 리스너 (Wildcard Event Listeners)

`*` 문자를 와일드카드로 사용하여 여러 이벤트를 한 리스너에서 받을 수 있습니다. 와일드카드 리스너에서는 첫 번째 인수로 이벤트 이름, 두 번째 인수로 전체 이벤트 데이터 배열이 전달됩니다:

```php
Event::listen('event.*', function (string $eventName, array $data) {
    // ...
});
```

<a name="defining-events"></a>
## 이벤트 정의 (Defining Events)

이벤트 클래스는 본질적으로 이벤트와 관련된 정보를 담는 데이터 컨테이너입니다. 예를 들어, `App\Events\OrderShipped` 이벤트가 [Eloquent ORM](/docs/12.x/eloquent) 객체를 전달받는다고 가정해보겠습니다:

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

이벤트 클래스에는 별도의 로직이 들어 있지 않습니다. 단지 구매된 `App\Models\Order` 인스턴스를 담는 컨테이너 역할만 합니다. 이벤트에서 사용하는 `SerializesModels` 트레이트는, [큐잉 리스너](#queued-event-listeners)와 같이 PHP의 `serialize` 함수로 이벤트 객체가 직렬화될 때 Eloquent 모델을 안전하게 직렬화해 줍니다.

<a name="defining-listeners"></a>
## 리스너 정의 (Defining Listeners)

다음으로, 연결된 이벤트의 리스너를 살펴보겠습니다. 이벤트 리스너는 이벤트 인스턴스를 `handle` 메서드에서 전달받습니다. `make:listener` Artisan 명령어를 `--event` 옵션과 함께 실행하면, 이벤트 클래스를 자동으로 임포트하고 `handle` 메서드에 타입힌트로 추가합니다. `handle` 메서드 내부에서는 이벤트에 대한 필요한 처리를 자유롭게 할 수 있습니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;

class SendShipmentNotification
{
    /**
     * 이벤트 리스너 생성자.
     */
    public function __construct() {}

    /**
     * 이벤트 처리.
     */
    public function handle(OrderShipped $event): void
    {
        // $event->order로 주문 정보에 접근...
    }
}
```

> [!NOTE]
> 이벤트 리스너의 생성자에서 필요한 의존성을 타입힌트로 지정할 수 있습니다. 모든 이벤트 리스너는 Laravel [서비스 컨테이너](/docs/12.x/container)를 통해 해석되므로, 의존성은 자동으로 주입됩니다.

<a name="stopping-the-propagation-of-an-event"></a>
#### 이벤트 전파 중단하기

경우에 따라, 이벤트가 다른 리스너로 전파되는 것을 막고 싶을 수 있습니다. 이럴 때 리스너의 `handle` 메서드에서 `false`를 반환하면 이벤트 전파가 중단됩니다.

<a name="queued-event-listeners"></a>
## 큐잉되는 이벤트 리스너 (Queued Event Listeners)

이메일 발송이나 HTTP 요청처럼 시간이 오래 걸리는 작업을 리스너에서 처리한다면, 큐잉 리스너를 사용하는 것이 좋습니다. 큐잉 리스너를 사용하기 전에는 반드시 [큐 설정](/docs/12.x/queues)을 마치고, 서버 또는 개발 환경에서 큐 워커를 실행하세요.

리스너가 큐에 들어가도록 하려면, 해당 클래스에 `ShouldQueue` 인터페이스를 추가하면 됩니다. `make:listener` Artisan 명령어로 생성된 리스너에는 이 인터페이스가 이미 네임스페이스에 임포트되어 있습니다:

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

이제 이 리스너가 처리하는 이벤트가 발생하면, 이벤트 디스패처가 Laravel의 [큐 시스템](/docs/12.x/queues)으로 자동으로 리스너를 큐에 올립니다. 리스너 실행 중 예외가 발생하지 않으면, 해당 큐 작업은 처리 후 자동으로 삭제됩니다.

<a name="customizing-the-queue-connection-queue-name"></a>
#### 큐 커넥션, 큐 이름, 지연 시간 커스터마이즈

이벤트 리스너의 큐 커넥션, 큐 이름, 큐 작업 지연 시간을 커스터마이즈하려면 리스너 클래스에 `$connection`, `$queue`, `$delay` 속성을 정의하면 됩니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    /**
     * 큐 작업이 보내질 커넥션 이름.
     *
     * @var string|null
     */
    public $connection = 'sqs';

    /**
     * 큐 작업이 보내질 큐 이름.
     *
     * @var string|null
     */
    public $queue = 'listeners';

    /**
     * 작업이 처리되기 전 대기 시간(초).
     *
     * @var int
     */
    public $delay = 60;
}
```

런타임에 큐 커넥션, 큐 이름, 지연 시간을 동적으로 정의하려면, 다음과 같이 `viaConnection`, `viaQueue`, `withDelay` 메서드를 구현하면 됩니다:

```php
/**
 * 리스너의 큐 커넥션 이름을 반환.
 */
public function viaConnection(): string
{
    return 'sqs';
}

/**
 * 리스너의 큐 이름을 반환.
 */
public function viaQueue(): string
{
    return 'listeners';
}

/**
 * 작업이 처리되기 전 대기 시간(초)을 반환.
 */
public function withDelay(OrderShipped $event): int
{
    return $event->highPriority ? 0 : 60;
}
```

<a name="conditionally-queueing-listeners"></a>
#### 조건부 큐잉 리스너

데이터에 따라 리스너를 큐잉할지 결정해야 할 경우, 리스너에 `shouldQueue` 메서드를 정의하여 해당 메서드가 `false`를 반환하면 큐잉되지 않습니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderCreated;
use Illuminate\Contracts\Queue\ShouldQueue;

class RewardGiftCard implements ShouldQueue
{
    /**
     * 고객에게 기프트카드 지급.
     */
    public function handle(OrderCreated $event): void
    {
        // ...
    }

    /**
     * 리스너를 큐잉할지 결정.
     */
    public function shouldQueue(OrderCreated $event): bool
    {
        return $event->order->subtotal >= 5000;
    }
}
```

<a name="manually-interacting-with-the-queue"></a>
### 큐 직접 제어하기 (Manually Interacting With the Queue)

리스너 내부에서 큐 작업의 `delete`, `release` 메서드 등에 직접 접근해야 할 때는, `Illuminate\Queue\InteractsWithQueue` 트레이트를 리스너에 사용하면 됩니다. 이 트레이트는 Artisan 명령어로 생성된 리스너에 기본적으로 포함되어 있습니다:

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
     * 이벤트 처리.
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
### 큐잉 리스너와 데이터베이스 트랜잭션 (Queued Event Listeners and Database Transactions)

큐잉 리스너가 데이터베이스 트랜잭션 내에서 디스패치될 때, 큐에서 실제로 처리되는 시점이 트랜잭션 커밋 이전일 수 있습니다. 이 경우, 트랜잭션 과정에서 변경된 모델의 정보가 아직 DB에 반영되지 않았거나, 트랜잭션 내에서 생성된 모델이 DB에 없을 수 있습니다. 리스너가 이런 모델에 의존하고 있다면, 예기치 않은 오류가 발생할 수 있습니다.

큐 커넥션의 `after_commit` 옵션이 `false`여도, 리스너 클래스에 `ShouldQueueAfterCommit` 인터페이스를 구현하면 모든 오픈된 트랜잭션이 커밋된 후 해당 큐잉 리스너가 디스패치됩니다:

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
> 이런 문제에 대한 자세한 해결 방법은 [큐 작업과 데이터베이스 트랜잭션](/docs/12.x/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="queued-listener-middleware"></a>
### 큐잉 리스너 미들웨어 (Queued Listener Middleware)

큐잉 리스너에서도 [작업 미들웨어](/docs/12.x/queues#job-middleware)를 사용할 수 있습니다. 작업 미들웨어를 사용하면, 큐잉 리스너 실행 전후에 커스텀 로직을 쉽게 적용할 수 있어, 리스너 코드의 반복적인 부분을 줄일 수 있습니다. 미들웨어를 정의한 후, 리스너의 `middleware` 메서드에서 리턴해 연결할 수 있습니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use App\Jobs\Middleware\RateLimited;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    /**
     * 이벤트 처리.
     */
    public function handle(OrderShipped $event): void
    {
        // 이벤트 처리...
    }

    /**
     * 리스너가 통과할 미들웨어 반환.
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

Laravel은 [암호화](/docs/12.x/encryption)를 이용해 큐잉 리스너의 데이터도 안전하게 보호할 수 있습니다. 이를 위해 리스너 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하면, 해당 리스너는 큐에 올라가기 전에 자동으로 암호화됩니다:

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
### 실패한 작업 처리 (Handling Failed Jobs)

큐잉 이벤트 리스너가 실패하는 경우, 큐 워커의 최대 시도 횟수를 초과하면 리스너의 `failed` 메서드가 호출됩니다. 이 메서드는 실패 원인을 담은 이벤트 인스턴스와 `Throwable` 객체를 전달받습니다:

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
     * 이벤트 처리.
     */
    public function handle(OrderShipped $event): void
    {
        // ...
    }

    /**
     * 작업 실패 처리.
     */
    public function failed(OrderShipped $event, Throwable $exception): void
    {
        // ...
    }
}
```

<a name="specifying-queued-listener-maximum-attempts"></a>
#### 큐잉 리스너 최대 시도 횟수 지정

큐잉 리스너에 오류가 발생할 경우, 무한 반복으로 계속 재시도하지 않도록 다양한 방식으로 최대 시도 횟수 또는 기간을 지정할 수 있습니다.

리스너 클래스에 `tries` 속성을 정의하면, 해당 리스너가 실패로 처리되기 전까지 최대 몇 번까지 시도할지 지정할 수 있습니다:

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
     * 큐잉 리스너의 최대 시도 횟수.
     *
     * @var int
     */
    public $tries = 5;
}
```

리스너를 실패로 간주할 특정 시도 횟수 대신, 더 이상 재시도하지 않을 시간을 정의하려면, 리스너 클래스에 `retryUntil` 메서드를 추가하세요. 이 메서드는 `DateTime` 인스턴스를 반환해야 합니다:

```php
use DateTime;

/**
 * 리스너가 타임아웃으로 간주될 시간 지정.
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(5);
}
```

`retryUntil`과 `tries`가 동시에 정의되어 있으면, Laravel은 `retryUntil` 메서드의 설정을 우선합니다.

<a name="specifying-queued-listener-backoff"></a>
#### 큐잉 리스너 재시도 대기(backoff) 시간 지정

리스너가 예외를 만난 뒤 재시도 전 Laravel이 대기해야 할 시간을 바꾸고 싶다면, 리스너 클래스에 `backoff` 속성을 설정할 수 있습니다:

```php
/**
 * 큐잉 리스너가 재시도하기 전 대기할 초(second).
 *
 * @var int
 */
public $backoff = 3;
```

더 복잡한 재시도 대기 로직이 필요하다면, 리스너 클래스에 `backoff` 메서드를 구현해서 사용하세요:

```php
/**
 * 큐잉 리스너가 재시도하기 전 대기할 초 계산.
 */
public function backoff(OrderShipped $event): int
{
    return 3;
}
```

"지수(backoff)" 대기를 손쉽게 설정하려면 `backoff` 메서드에서 배열로 값을 리턴합니다. 아래 예시는 첫 번째 재시도에는 1초, 두 번째는 5초, 세 번째 이후에는 10초씩 대기합니다:

```php
/**
 * 큐잉 리스너가 재시도하기 전 대기할 초 배열.
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

많은 횟수로 리스너를 재시도하도록 하고 싶지만, 특정 개수의 미처리 예외가 발생하면 실패로 간주하고 싶을 때는, 리스너 클래스에 `maxExceptions` 속성을 추가하면 됩니다:

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
     * 큐잉 리스너 최대 시도 횟수.
     *
     * @var int
     */
    public $tries = 25;

    /**
     * 실패 처리 전 허용되는 최대 미처리 예외 개수.
     *
     * @var int
     */
    public $maxExceptions = 3;

    /**
     * 이벤트 처리.
     */
    public function handle(OrderShipped $event): void
    {
        // 이벤트 처리...
    }
}
```

위 예시에서는 최대 25회 재시도가 가능하지만, 미처리 예외가 3번 발생하면 리스너가 실패 처리됩니다.

<a name="specifying-queued-listener-timeout"></a>
#### 큐잉 리스너 타임아웃 지정

일반적으로 큐잉 리스너가 얼마나 걸릴지 대략 알 수 있는 경우 timeout(최대 실행 시간)을 지정할 수 있습니다. 타임아웃 시간(초)을 초과하면 해당 리스너를 실행하던 워커는 에러와 함께 종료됩니다. 리스너 클래스에 `timeout` 속성을 지정해 제한할 수 있습니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    /**
     * 리스너가 실행될 수 있는 최대 시간(초).
     *
     * @var int
     */
    public $timeout = 120;
}
```

타임아웃이 발생했을 때 작업을 실패로 처리하려면, 리스너 클래스에 `failOnTimeout` 속성을 추가하세요:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    /**
     * 타임아웃 발생 시 작업 실패 처리 여부.
     *
     * @var bool
     */
    public $failOnTimeout = true;
}
```

<a name="dispatching-events"></a>
## 이벤트 디스패치 (Dispatching Events)

이벤트를 디스패치하려면, 이벤트의 static `dispatch` 메서드를 호출하면 됩니다. 이 메서드는 `Illuminate\Foundation\Events\Dispatchable` 트레이트에 의해 이벤트 클래스에 추가됩니다. `dispatch`에 전달한 인자는 이벤트 생성자에 그대로 전달됩니다:

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
     * 주어진 주문 발송.
     */
    public function store(Request $request): RedirectResponse
    {
        $order = Order::findOrFail($request->order_id);

        // 주문 발송 처리...

        OrderShipped::dispatch($order);

        return redirect('/orders');
    }
}
```

조건부로 이벤트를 디스패치하려면, `dispatchIf`, `dispatchUnless` 메서드를 사용할 수 있습니다:

```php
OrderShipped::dispatchIf($condition, $order);

OrderShipped::dispatchUnless($condition, $order);
```

> [!NOTE]
> 테스트 시, 실제 리스너가 실행되지 않아도 특정 이벤트가 디스패치되었는지 검증하고 싶을 때가 많습니다. Laravel의 [테스트 헬퍼](#testing)를 사용하면 쉽게 검증할 수 있습니다.

<a name="dispatching-events-after-database-transactions"></a>
### 데이터베이스 트랜잭션 이후 이벤트 디스패치

경우에 따라, 활성화된 데이터베이스 트랜잭션이 커밋된 후에만 이벤트를 디스패치하고 싶을 수 있습니다. 이럴 때 이벤트 클래스에 `ShouldDispatchAfterCommit` 인터페이스를 구현하면 됩니다.

이 인터페이스를 추가하면, 트랜잭션이 커밋될 때까지 이벤트가 실제로 디스패치되지 않습니다. 트랜잭션이 실패하면 이벤트는 폐기됩니다. 만약 디스패치 시점에 활성 트랜잭션이 없다면, 바로 디스패치됩니다:

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
     * 새 이벤트 인스턴스 생성자.
     */
    public function __construct(
        public Order $order,
    ) {}
}
```

<a name="event-subscribers"></a>
## 이벤트 구독자 (Event Subscribers)

<a name="writing-event-subscribers"></a>
### 이벤트 구독자 작성 (Writing Event Subscribers)

이벤트 구독자는 클래스 내부에서 여러 이벤트를 구독할 수 있도록 해주며, 하나의 클래스 내에서 여러 이벤트 핸들러를 정의할 수 있습니다. 구독자 클래스에는 `subscribe` 메서드를 정의하고, 이벤트 디스패처 인스턴스를 전달받아 `listen` 메서드로 리스너를 등록합니다:

```php
<?php

namespace App\Listeners;

use Illuminate\Auth\Events\Login;
use Illuminate\Auth\Events\Logout;
use Illuminate\Events\Dispatcher;

class UserEventSubscriber
{
    /**
     * 로그인 이벤트 핸들러.
     */
    public function handleUserLogin(Login $event): void {}

    /**
     * 로그아웃 이벤트 핸들러.
     */
    public function handleUserLogout(Logout $event): void {}

    /**
     * 구독자의 리스너 등록.
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

구독자 내부에 이벤트 리스너 메서드가 있다면, `subscribe` 메서드에서 이벤트와 메서드명을 배열로 반환하여 자동 등록되도록 할 수도 있습니다. 이 경우 Laravel이 내부적으로 클래스명을 자동으로 결정합니다:

```php
<?php

namespace App\Listeners;

use Illuminate\Auth\Events\Login;
use Illuminate\Auth\Events\Logout;
use Illuminate\Events\Dispatcher;

class UserEventSubscriber
{
    /**
     * 로그인 이벤트 핸들러.
     */
    public function handleUserLogin(Login $event): void {}

    /**
     * 로그아웃 이벤트 핸들러.
     */
    public function handleUserLogout(Logout $event): void {}

    /**
     * 구독자의 리스너 등록.
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

구독자를 작성한 뒤, 구독자의 핸들러 메서드가 Laravel의 [이벤트 자동 탐색 규칙](#event-discovery)에 맞게 작성되어 있으면 자동으로 등록됩니다. 그렇지 않은 경우에는, `Event` 파사드의 `subscribe` 메서드를 사용해 직접 등록해야 합니다. 일반적으로 `AppServiceProvider`의 `boot` 메서드 내에서 등록합니다:

```php
<?php

namespace App\Providers;

use App\Listeners\UserEventSubscriber;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 부트스트랩.
     */
    public function boot(): void
    {
        Event::subscribe(UserEventSubscriber::class);
    }
}
```

<a name="testing"></a>
## 테스트 (Testing)

이벤트를 디스패치하는 코드를 테스트할 때, 실제로 이벤트의 리스너가 실행되지 않게 하고 싶을 수 있습니다. 리스너의 코드는 직접 개별적으로 테스트할 수 있으므로, 이벤트 디스패치 코드와 리스너 코드를 분리해서 테스트하는 것이 이상적입니다. 리스너 자체를 테스트하려면, 리스너 인스턴스를 만들어 `handle` 메서드를 직접 호출하면 됩니다.

`Event` 파사드의 `fake` 메서드를 사용하면, 리스너 실행을 막고 테스트 대상 코드를 수행한 뒤, 해당 애플리케이션에서 어떤 이벤트가 디스패치되었는지 `assertDispatched`, `assertNotDispatched`, `assertNothingDispatched` 등의 메서드로 검증할 수 있습니다:

```php tab=Pest
<?php

use App\Events\OrderFailedToShip;
use App\Events\OrderShipped;
use Illuminate\Support\Facades/Event;

test('orders can be shipped', function () {
    Event::fake();

    // 주문 발송...

    // 이벤트가 디스패치되었는지 확인...
    Event::assertDispatched(OrderShipped::class);

    // 이벤트가 두 번 디스패치되었는지 확인...
    Event::assertDispatched(OrderShipped::class, 2);

    // 이벤트가 한 번 디스패치되었는지 확인...
    Event::assertDispatchedOnce(OrderShipped::class);

    // 이벤트가 디스패치되지 않았는지 확인...
    Event::assertNotDispatched(OrderFailedToShip::class);

    // 아무 이벤트도 디스패치되지 않았는지 확인...
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
     * 주문 발송 테스트.
     */
    public function test_orders_can_be_shipped(): void
    {
        Event::fake();

        // 주문 발송...

        // 이벤트가 디스패치되었는지 확인...
        Event::assertDispatched(OrderShipped::class);

        // 이벤트가 두 번 디스패치되었는지 확인...
        Event::assertDispatched(OrderShipped::class, 2);

        // 이벤트가 한 번 디스패치되었는지 확인...
        Event::assertDispatchedOnce(OrderShipped::class);

        // 이벤트가 디스패치되지 않았는지 확인...
        Event::assertNotDispatched(OrderFailedToShip::class);

        // 아무 이벤트도 디스패치되지 않았는지 확인...
        Event::assertNothingDispatched();
    }
}
```

특정 조건을 만족하는 이벤트가 디스패치되었는지 검증하려면, `assertDispatched` 또는 `assertNotDispatched`에 클로저를 전달할 수 있습니다. 전달된 클로저가 `true`를 반환하면 검증이 성공합니다:

```php
Event::assertDispatched(function (OrderShipped $event) use ($order) {
    return $event->order->id === $order->id;
});
```

특정 리스너가 지정한 이벤트를 리스닝하고 있는지 확인하려면, `assertListening` 메서드를 사용할 수 있습니다:

```php
Event::assertListening(
    OrderShipped::class,
    SendShipmentNotification::class
);
```

> [!WARNING]
> `Event::fake()`를 호출하면, 어떤 이벤트 리스너도 실행되지 않습니다. 따라서 팩토리를 통해 UUID를 생성하는 등, 생성 이벤트에 의존하는 경우라면 팩토리 실행 이후에 `Event::fake()`를 호출해야 합니다.

<a name="faking-a-subset-of-events"></a>
### 특정 이벤트만 가짜로 만들기 (Faking a Subset of Events)

특정 이벤트에 대해서만 리스너를 가짜로 만들고 싶을 때는, 해당 이벤트들을 `fake` 또는 `fakeFor` 메서드에 배열로 전달할 수 있습니다:

```php tab=Pest
test('orders can be processed', function () {
    Event::fake([
        OrderCreated::class,
    ]);

    $order = Order::factory()->create();

    Event::assertDispatched(OrderCreated::class);

    // 다른 이벤트들은 평소처럼 디스패치됨...
    $order->update([
        // ...
    ]);
});
```

```php tab=PHPUnit
/**
 * 주문 처리 테스트.
 */
public function test_orders_can_be_processed(): void
{
    Event::fake([
        OrderCreated::class,
    ]);

    $order = Order::factory()->create();

    Event::assertDispatched(OrderCreated::class);

    // 다른 이벤트들은 평소처럼 디스패치됨...
    $order->update([
        // ...
    ]);
}
```

일부를 제외한 모든 이벤트를 fake 처리하려면, `except` 메서드를 사용하면 됩니다:

```php
Event::fake()->except([
    OrderCreated::class,
]);
```

<a name="scoped-event-fakes"></a>
### 스코프별 이벤트 가짜 처리 (Scoped Event Fakes)

테스트의 일부 부분에서만 이벤트를 fake 처리하고 싶다면, `fakeFor` 메서드를 사용할 수 있습니다:

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

    // 여기서는 이벤트가 평소처럼 디스패치되고, 옵저버도 실행됨...
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
     * 주문 처리 테스트.
     */
    public function test_orders_can_be_processed(): void
    {
        $order = Event::fakeFor(function () {
            $order = Order::factory()->create();

            Event::assertDispatched(OrderCreated::class);

            return $order;
        });

        // 여기서는 이벤트가 평소처럼 디스패치되고, 옵저버도 실행됨...
        $order->update([
            // ...
        ]);
    }
}
```
