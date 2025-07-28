# 이벤트 (Events)

- [소개](#introduction)
- [이벤트 및 리스너 생성](#generating-events-and-listeners)
- [이벤트 및 리스너 등록](#registering-events-and-listeners)
    - [이벤트 자동 검색](#event-discovery)
    - [이벤트 수동 등록](#manually-registering-events)
    - [클로저 리스너](#closure-listeners)
- [이벤트 정의](#defining-events)
- [리스너 정의](#defining-listeners)
- [큐 처리 이벤트 리스너](#queued-event-listeners)
    - [큐와 직접 상호작용하기](#manually-interacting-with-the-queue)
    - [큐 리스너와 데이터베이스 트랜잭션](#queued-event-listeners-and-database-transactions)
    - [큐 리스너 미들웨어](#queued-listener-middleware)
    - [암호화된 큐 리스너](#encrypted-queued-listeners)
    - [실패한 작업 처리](#handling-failed-jobs)
- [이벤트 디스패치](#dispatching-events)
    - [데이터베이스 트랜잭션 후 이벤트 디스패치](#dispatching-events-after-database-transactions)
- [이벤트 구독자](#event-subscribers)
    - [이벤트 구독자 작성](#writing-event-subscribers)
    - [이벤트 구독자 등록](#registering-event-subscribers)
- [테스트](#testing)
    - [일부 이벤트 Faking](#faking-a-subset-of-events)
    - [스코프된 이벤트 Fake](#scoped-event-fakes)

<a name="introduction"></a>
## 소개

라라벨의 이벤트 시스템은 간단한 옵저버 패턴(Observer Pattern) 구현을 제공하여, 애플리케이션 내에서 발생하는 다양한 이벤트를 구독하고 처리할 수 있도록 해줍니다. 일반적으로 이벤트 클래스는 `app/Events` 디렉터리에, 해당 리스너는 `app/Listeners` 디렉터리에 저장됩니다. 만약 이 디렉터리들이 프로젝트에 없다면 걱정하지 마십시오. Artisan 콘솔 명령어로 이벤트와 리스너를 생성할 때 자동으로 만들어집니다.

이벤트는 애플리케이션의 여러 측면을 느슨하게 결합하는 훌륭한 방법입니다. 하나의 이벤트에 여러 리스너가 각각 독립적으로 연결되어 동작할 수 있기 때문입니다. 예를 들어, 주문이 배송될 때마다 사용자의 슬랙(Slack)으로 알림을 보내고 싶다고 가정해봅시다. 주문 처리 코드에 슬랙 알림 코드를 직접 연결(결합)하는 대신, `App\Events\OrderShipped` 이벤트를 발생시키고, 이 이벤트를 리스너에서 받아서 슬랙 알림을 보낼 수 있습니다.

<a name="generating-events-and-listeners"></a>
## 이벤트 및 리스너 생성

이벤트와 리스너를 빠르게 생성하려면 `make:event` 및 `make:listener` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan make:event PodcastProcessed

php artisan make:listener SendPodcastNotification --event=PodcastProcessed
```

편의상, 추가 인수 없이 `make:event` 및 `make:listener` Artisan 명령어를 실행할 수도 있습니다. 이 경우, 라라벨이 클래스 이름(리스너는 어떤 이벤트를 들을지) 입력을 자동으로 요청합니다.

```shell
php artisan make:event

php artisan make:listener
```

<a name="registering-events-and-listeners"></a>
## 이벤트 및 리스너 등록

<a name="event-discovery"></a>
### 이벤트 자동 검색

기본적으로 라라벨은 애플리케이션의 `Listeners` 디렉터리를 스캔하여 이벤트 리스너 클래스를 자동으로 찾아 등록합니다. 라라벨은 `handle` 또는 `__invoke`로 시작하는 메서드를 가진 리스너 클래스를 발견하면, 그 메서드 시그니처에 타입힌트된 이벤트를 위한 리스너로 자동 등록합니다.

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

PHP의 유니언 타입(union types)을 이용해 여러 이벤트를 동시에 들을 수도 있습니다.

```php
/**
 * Handle the event.
 */
public function handle(PodcastProcessed|PodcastPublished $event): void
{
    // ...
}
```

다른 디렉터리나 여러 디렉터리에 리스너를 저장하려는 경우, 애플리케이션의 `bootstrap/app.php` 파일에서 `withEvents` 메서드를 사용해 라라벨에게 해당 디렉터리에서도 자동 검색을 하도록 지정할 수 있습니다.

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/Orders/Listeners',
])
```

와일드카드(`*`) 문자로 여러 비슷한 경로의 디렉터리를 한 번에 스캔하도록 지정할 수도 있습니다.

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/*/Listeners',
])
```

`event:list` 명령어를 사용하면 애플리케이션에 등록된 모든 리스너를 확인할 수 있습니다.

```shell
php artisan event:list
```

<a name="event-discovery-in-production"></a>
#### 프로덕션 환경의 이벤트 자동 검색

애플리케이션의 성능을 높이려면 `optimize` 또는 `event:cache` Artisan 명령어를 사용해 모든 리스너의 매니페스트를 캐시해두는 것이 좋습니다. 이 명령어는 보통 [배포 프로세스](/docs/12.x/deployment#optimization) 중 일부로 실행합니다. 프레임워크는 이 매니페스트를 활용해 이벤트 등록을 훨씬 빠르게 처리할 수 있습니다. 캐시를 삭제하려면 `event:clear` 명령어를 사용할 수 있습니다.

<a name="manually-registering-events"></a>
### 이벤트 수동 등록

`Event` 파사드를 사용하면, 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 이벤트와 해당 리스너를 수동으로 등록할 수 있습니다.

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

`event:list` 명령어를 사용하여 등록된 모든 리스너를 확인할 수 있습니다.

```shell
php artisan event:list
```

<a name="closure-listeners"></a>
### 클로저 리스너

일반적으로 리스너는 클래스 형태로 정의하지만, `AppServiceProvider`의 `boot` 메서드에서 클로저(익명 함수) 기반의 이벤트 리스너를 수동으로 등록할 수도 있습니다.

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
#### 큐 처리 가능한 익명 이벤트 리스너

클로저 기반의 이벤트 리스너를 등록할 때, 해당 리스너 클로저를 `Illuminate\Events\queueable` 함수로 감싸면, 이 리스너를 [큐](/docs/12.x/queues)에서 비동기적으로 실행하도록 지시할 수 있습니다.

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

큐잉된 작업처럼 `onConnection`, `onQueue`, `delay` 메서드를 사용해 큐 리스너의 동작 방식을 세밀하게 조정할 수 있습니다.

```php
Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->onConnection('redis')->onQueue('podcasts')->delay(now()->addSeconds(10)));
```

익명 큐 리스너가 실패했을 때의 처리를 원한다면, `queueable` 리스너 정의 시 `catch` 메서드에 클로저를 전달할 수 있습니다. 이 클로저는 이벤트 인스턴스와 리스너 실패의 원인인 `Throwable` 인스턴스를 인자로 받습니다.

```php
use App\Events\PodcastProcessed;
use function Illuminate\Events\queueable;
use Illuminate\Support\Facades\Event;
use Throwable;

Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->catch(function (PodcastProcessed $event, Throwable $e) {
    // 큐 리스너가 실패했습니다...
}));
```

<a name="wildcard-event-listeners"></a>
#### 와일드카드 이벤트 리스너

`*` 문자를 와일드카드로 사용하여 여러 이벤트를 하나의 리스너에서 받을 수도 있습니다. 와일드카드 리스너는 첫 번째 인자로 이벤트 이름, 두 번째 인자로 이벤트 데이터 배열을 받습니다.

```php
Event::listen('event.*', function (string $eventName, array $data) {
    // ...
});
```

<a name="defining-events"></a>
## 이벤트 정의

이벤트 클래스는 이벤트와 관련된 정보를 담는 일종의 데이터 컨테이너입니다. 예를 들어, `App\Events\OrderShipped` 이벤트가 [Eloquent ORM](/docs/12.x/eloquent) 객체를 전달받는다고 가정해보겠습니다.

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

위 예시에서 알 수 있듯이, 이 이벤트 클래스는 별도의 로직을 포함하지 않고 `App\Models\Order` 인스턴스만을 보관합니다. 이벤트에서 사용하는 `SerializesModels` 트레이트는 이벤트 객체가 PHP의 `serialize` 함수로 직렬화될 때 Eloquent 모델을 안전하게 직렬화해줍니다. 이 방식은 [큐 리스너](#queued-event-listeners)를 사용할 때 유용하게 작동합니다.

<a name="defining-listeners"></a>
## 리스너 정의

다음으로, 앞서 예시로 들었던 이벤트에 대한 리스너를 살펴보겠습니다. 이벤트 리스너는 `handle` 메서드에서 이벤트 인스턴스를 전달받습니다. `make:listener` Artisan 명령어를 `--event` 옵션과 함께 사용하면 적절한 이벤트 클래스를 자동으로 import 및 타입힌트해줍니다. `handle` 메서드 내부에서 이벤트에 대응한 필요한 모든 작업을 수행할 수 있습니다.

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
        // $event->order로 주문 정보를 사용할 수 있습니다...
    }
}
```

> [!NOTE]
> 이벤트 리스너의 생성자에서 필요한 의존성을 타입힌트로 지정할 수도 있습니다. 모든 이벤트 리스너는 라라벨 [서비스 컨테이너](/docs/12.x/container)를 통해 생성되므로, 의존성은 자동 주입됩니다.

<a name="stopping-the-propagation-of-an-event"></a>
#### 이벤트 전파 멈추기

때로는 이벤트가 다른 리스너에 전달되는 것을 중단하고 싶을 수도 있습니다. 이 경우, 리스너의 `handle` 메서드에서 `false`를 반환하면 이벤트 전파가 멈춥니다.

<a name="queued-event-listeners"></a>
## 큐 처리 이벤트 리스너

이메일 전송 또는 HTTP 요청처럼 시간이 오래 걸리는 작업을 하는 리스너라면, 큐에 등록하여 비동기적으로 처리하는 것이 좋습니다. 큐 리스너를 사용하기 전에 반드시 [큐를 설정](/docs/12.x/queues)하고, 서버나 로컬 개발 환경에서 큐 워커를 실행해야 합니다.

리스너 클래스를 큐에 등록하려면, 클래스에 `ShouldQueue` 인터페이스를 추가하면 됩니다. `make:listener` Artisan 명령어로 생성된 리스너는 이미 이 인터페이스가 네임스페이스에 import되어 있으므로 바로 사용할 수 있습니다.

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

이제 이 리스너가 처리하는 이벤트가 디스패치되면, 해당 리스너는 라라벨의 [큐 시스템](/docs/12.x/queues)에 의해 자동으로 큐에 등록되어 실행됩니다. 리스너가 큐에서 예외 없이 정상적으로 실행되면, 작업은 자동으로 삭제됩니다.

<a name="customizing-the-queue-connection-queue-name"></a>
#### 큐 연결, 큐 이름, 대기시간 커스터마이징

이벤트 리스너가 사용할 큐 연결, 큐 이름, 또는 큐 대기시간(딜레이)을 직접 지정하고 싶다면, 리스너 클래스에 `$connection`, `$queue`, `$delay` 속성을 지정하면 됩니다.

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    /**
     * 이 작업이 전송될 큐 연결명
     *
     * @var string|null
     */
    public $connection = 'sqs';

    /**
     * 이 작업이 전송될 큐 이름
     *
     * @var string|null
     */
    public $queue = 'listeners';

    /**
     * 작업이 처리되기까지 대기할 시간(초)
     *
     * @var int
     */
    public $delay = 60;
}
```

런타임에서 리스너의 큐 연결명, 큐 이름, 대기시간을 동적으로 지정하고 싶다면, `viaConnection`, `viaQueue`, `withDelay` 메서드를 추가로 정의할 수 있습니다.

```php
/**
 * 리스너의 큐 연결명을 반환합니다.
 */
public function viaConnection(): string
{
    return 'sqs';
}

/**
 * 리스너의 큐 이름을 반환합니다.
 */
public function viaQueue(): string
{
    return 'listeners';
}

/**
 * 작업 처리 전 대기할 시간을(초 단위로) 반환합니다.
 */
public function withDelay(OrderShipped $event): int
{
    return $event->highPriority ? 0 : 60;
}
```

<a name="conditionally-queueing-listeners"></a>
#### 리스너의 큐 등록 조건부 처리

가끔 런타임에서만 알 수 있는 데이터에 따라 리스너를 큐에 넣을지 결정해야 할 때가 있습니다. 이럴 경우, 리스너에 `shouldQueue` 메서드를 추가하여, 큐 등록 여부를 제어할 수 있습니다. 이 메서드가 `false`를 반환하면 리스너는 큐에 등록되지 않습니다.

```php
<?php

namespace App\Listeners;

use App\Events\OrderCreated;
use Illuminate\Contracts\Queue\ShouldQueue;

class RewardGiftCard implements ShouldQueue
{
    /**
     * 고객에게 기프트 카드를 보상합니다.
     */
    public function handle(OrderCreated $event): void
    {
        // ...
    }

    /**
     * 리스너를 큐에 추가할지 여부를 결정합니다.
     */
    public function shouldQueue(OrderCreated $event): bool
    {
        return $event->order->subtotal >= 5000;
    }
}
```

<a name="manually-interacting-with-the-queue"></a>
### 큐와 직접 상호작용하기

리스너의 내부 큐 작업에서 `delete`와 `release` 메서드에 수동으로 접근해야 하는 경우, `Illuminate\Queue\InteractsWithQueue` 트레이트를 사용할 수 있습니다. 이 트레이트는 기본적으로 생성된 리스너에 import되어 있으며, 관련 메서드를 제공합니다.

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
     * 이벤트를 처리합니다.
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

큐잉된 리스너가 데이터베이스 트랜잭션 안에서 디스패치(dispach)되면, 해당 리스너가 트랜잭션이 커밋되기 전에 큐에서 처리되는 상황이 발생할 수 있습니다. 이 경우, 트랜잭션에서 업데이트된 모델이나 레코드는 아직 데이터베이스에 반영되지 않았을 수 있습니다. 또한, 트랜잭션 내부에서 새로 생성된 모델이나 레코드 역시 아직 데이터베이스에 존재하지 않을 수 있습니다. 만약 리스너가 이러한 모델에 의존한다면, 큐 작업이 처리될 때 예기치 않은 오류가 발생할 수 있습니다.

만약 큐 연결의 `after_commit` 설정 옵션이 `false`로 되어 있어도, 특정 큐 리스너만은 모든 데이터베이스 트랜잭션이 커밋된 이후에 디스패치하도록 지정할 수 있습니다. 이를 위해 리스너에서 `ShouldQueueAfterCommit` 인터페이스를 구현하면 됩니다.

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
> 해당 내용에 대한 더 자세한 정보는 [큐 작업과 데이터베이스 트랜잭션](/docs/12.x/queues#jobs-and-database-transactions) 문서를 참고하시기 바랍니다.

<a name="queued-listener-middleware"></a>
### 큐 리스너 미들웨어

큐 리스너에서도 [작업 미들웨어(job middleware)](/docs/12.x/queues#job-middleware)를 사용할 수 있습니다. 작업 미들웨어를 이용하면, 큐 리스너 실행 과정에 커스텀 로직을 쉽게 추가할 수 있어 각 리스너 내부의 반복 코드를 줄일 수 있습니다. 미들웨어를 생성하고 나면, 리스너의 `middleware` 메서드에서 반환하여 미들웨어를 적용할 수 있습니다.

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use App\Jobs\Middleware\RateLimited;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    /**
     * 이벤트 처리
     */
    public function handle(OrderShipped $event): void
    {
        // 이벤트를 처리합니다...
    }

    /**
     * 리스너가 거쳐야 할 미들웨어 반환.
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

라라벨은 [암호화](/docs/12.x/encryption)를 통해 큐잉된 리스너의 데이터 무결성과 보안을 보장할 수 있도록 지원합니다. 사용 방법은 간단하게, 리스너 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하기만 하면 됩니다. 이 인터페이스가 추가된 리스너는 자동으로 암호화되어 큐에 올라갑니다.

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

큐 처리 이벤트 리스너가 실패하는 경우도 있습니다. 큐에 등록된 리스너가 큐 워커에 지정된 최대 시도 횟수를 초과하면, 리스너의 `failed` 메서드가 호출됩니다. 이 메서드는 실패한 원인인 `Throwable` 인스턴스와 이벤트 인스턴스를 인자로 받습니다.

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
     * 이벤트를 처리합니다.
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
#### 큐 리스너의 최대 시도 횟수 지정

만약 특정 큐 리스너에서 에러가 발생한다면, 무한정 시도(재시도)하는 것을 원치 않을 수 있습니다. 라라벨은 리스너의 최대 시도 횟수나 최대 시도 시간을 지정할 수 있는 다양한 방법을 제공합니다.

리스너 클래스에 `$tries` 속성을 지정하면, 해당 리스너가 실패로 간주되기 전까지 최대 몇 번 시도할지를 지정할 수 있습니다.

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
     * 큐 리스너의 최대 시도 횟수
     *
     * @var int
     */
    public $tries = 5;
}
```

리스너가 몇 번 실패할 때까지 시도할지 대신, 언제까지 시도할지를 정하고 싶다면, 리스너 클래스에 `retryUntil` 메서드를 추가하세요. 이 메서드는 `DateTime` 인스턴스를 반환해야 합니다.

```php
use DateTime;

/**
 * 리스너를 더 이상 시도하지 않을 시간을 반환합니다.
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(5);
}
```

`retryUntil`과 `tries`를 모두 지정한 경우에는, 라라벨이 `retryUntil`을 우선 적용합니다.

<a name="specifying-queued-listener-backoff"></a>
#### 큐 리스너의 재시도 대기(backoff) 지정

큐 리스너가 예외로 인해 실패했을 때 재시도 전 대기할 시간을 조정하려면, 리스너 클래스에 `$backoff` 속성을 지정하면 됩니다.

```php
/**
 * 큐 리스너 재시도 전 대기할 시간(초)
 *
 * @var int
 */
public $backoff = 3;
```

대기 시간 계산이 더 복잡하다면, 리스너 클래스에 `backoff` 메서드를 정의해 원하는 값을 반환할 수 있습니다.

```php
/**
 * 큐 리스너 재시도 전 대기할 시간(초 단위)을 반환합니다.
 */
public function backoff(OrderShipped $event): int
{
    return 3;
}
```

"지수(exponential)" 형태의 backoff가 필요하다면, `backoff` 메서드에서 배열로 여러 값을 반환할 수 있습니다. 아래 예시는 첫 번째 재시도는 1초, 두 번째는 5초, 세 번째 이후는 10초씩 대기합니다.

```php
/**
 * 큐 리스너 재시도 전 대기 시간(초)을 배열로 반환합니다.
 *
 * @return list<int>
 */
public function backoff(OrderShipped $event): array
{
    return [1, 5, 10];
}
```

<a name="specifying-queued-listener-max-exceptions"></a>
#### 큐 리스너의 최대 예외 횟수 지정

경우에 따라, 리스너가 여러 번(예를 들어 25회) 시도될 수 있도록 허용하면서도, 미처리된 예외가 특정 횟수(예: 3회) 발생할 경우에는 실패로 처리하고 싶을 수 있습니다. 이를 위해 리스너 클래스에서 `$maxExceptions` 속성을 지정할 수 있습니다.

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
     * 큐 리스너 최대 시도 횟수
     *
     * @var int
     */
    public $tries = 25;

    /**
     * 실패로 간주하기 전 허용할 최대 예외 발생 횟수
     *
     * @var int
     */
    public $maxExceptions = 3;

    /**
     * 이벤트를 처리합니다.
     */
    public function handle(OrderShipped $event): void
    {
        // 이벤트 처리...
    }
}
```

이 예시에서 리스너는 최대 25번까지 재시도되지만, 예외가 3번 발생하면 더 이상 시도하지 않고 실패로 처리됩니다.

<a name="specifying-queued-listener-timeout"></a>
#### 큐 리스너 타임아웃 지정

보통 큐 리스너가 얼마나 걸릴지 대략 예상할 수 있습니다. 라라벨은 리스너 실행이 지정 초(second) 이상 걸릴 경우, 워커가 에러와 함께 종료되도록 "타임아웃(timeout)" 값을 지정할 수 있습니다. 리스너 클래스에 `$timeout` 속성을 지정하면 해당 값만큼(초 단위) 실행됩니다.

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    /**
     * 큐 리스너의 최대 실행 시간(초)
     *
     * @var int
     */
    public $timeout = 120;
}
```

타임아웃이 발생했을 때 리스너를 실패로 간주하려면 `$failOnTimeout` 속성을 `true`로 지정할 수 있습니다.

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    /**
     * 타임아웃 시 리스너를 실패로 처리할지 여부
     *
     * @var bool
     */
    public $failOnTimeout = true;
}
```

<a name="dispatching-events"></a>

## 이벤트 디스패치하기

이벤트를 디스패치하려면, 해당 이벤트에서 정적 `dispatch` 메서드를 호출하면 됩니다. 이 메서드는 `Illuminate\Foundation\Events\Dispatchable` 트레이트를 이벤트 클래스에 추가함으로써 사용할 수 있게 됩니다. `dispatch` 메서드에 전달한 모든 인수는 이벤트의 생성자에 그대로 전달됩니다.

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

이벤트를 조건에 따라 디스패치하고 싶을 때는 `dispatchIf`와 `dispatchUnless` 메서드를 사용할 수 있습니다.

```php
OrderShipped::dispatchIf($condition, $order);

OrderShipped::dispatchUnless($condition, $order);
```

> [!NOTE]
> 테스트를 진행할 때는 실제로 리스너가 실행되지 않고, 특정 이벤트가 디스패치되었는지만 검증(assert)하는 것이 도움이 될 수 있습니다. 라라벨의 [내장 테스트 헬퍼](#testing)를 사용하면 이런 작업을 매우 쉽게 할 수 있습니다.

<a name="dispatching-events-after-database-transactions"></a>
### 데이터베이스 트랜잭션 후에 이벤트 디스패치하기

때로는 현재 실행 중인 데이터베이스 트랜잭션이 커밋된 이후에만 이벤트를 디스패치하도록 라라벨에 지시하고 싶을 수 있습니다. 이 경우, 이벤트 클래스에서 `ShouldDispatchAfterCommit` 인터페이스를 구현하면 됩니다.

이 인터페이스를 구현하면 라라벨은 현재의 데이터베이스 트랜잭션이 커밋될 때까지 해당 이벤트를 디스패치하지 않습니다. 만약 트랜잭션이 실패하면, 해당 이벤트는 버려집니다. 이벤트를 디스패치할 때 데이터베이스 트랜잭션이 진행 중이지 않다면, 이벤트는 즉시 디스패치됩니다.

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
### 이벤트 구독자 작성하기

이벤트 구독자(Event Subscriber)는 하나의 클래스에서 여러 개의 이벤트를 구독할 수 있도록 해주는 클래스입니다. 즉, 여러 이벤트 핸들러를 하나의 클래스에서 정의할 수 있습니다. 구독자 클래스에는 `subscribe` 메서드를 정의해야 하며, 이 메서드는 이벤트 디스패처 인스턴스를 인수로 받습니다. 주어진 디스패처의 `listen` 메서드를 호출하여 이벤트 리스너를 등록할 수 있습니다.

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

만약 구독자 내부에 이벤트 리스너 메서드를 정의했다면, `subscribe` 메서드에서 이벤트와 메서드 이름 배열을 반환하는 방법이 더 편리할 수 있습니다. 리스너를 등록할 때 라라벨이 자동으로 구독자 클래스 이름을 판단해줍니다.

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

구독자 클래스를 작성한 후, 이벤트 리스너 메서드의 시그니처가 라라벨의 [이벤트 디스커버리 규칙](#event-discovery)을 따른다면 라라벨이 자동으로 구독자를 등록해줍니다. 그렇지 않은 경우에는 `Event` 파사드의 `subscribe` 메서드를 사용해 수동으로 구독자를 등록할 수 있습니다. 일반적으로 이 코드는 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 작성합니다.

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

이벤트를 디스패치하는 코드를 테스트할 때, 이벤트 리스너가 실제로 실행되지 않도록 라라벨에 지시하고 싶을 때가 있습니다. 리스너의 코드는 해당 리스너의 단위 테스트에서 별도로 검증할 수 있기 때문입니다. 물론, 리스너 자체를 테스트하고 싶을 때는 리스너 인스턴스를 직접 생성해서 테스트에서 `handle` 메서드를 호출할 수 있습니다.

`Event` 파사드의 `fake` 메서드를 사용하면 리스너의 실행을 막을 수 있으며, 테스트 중인 코드를 실행한 후 애플리케이션에서 어떤 이벤트가 디스패치되었는지 `assertDispatched`, `assertNotDispatched`, `assertNothingDispatched` 등의 메서드로 확인할 수 있습니다.

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

`assertDispatched`나 `assertNotDispatched` 메서드에 클로저를 전달하면, 해당 클로저(“조건식”)가 참을 반환하는 한, 그에 일치하는 이벤트 디스패치가 있었는지를 검증할 수 있습니다. 이러한 조건에 맞는 이벤트가 하나라도 디스패치되었다면 검증은 통과합니다.

```php
Event::assertDispatched(function (OrderShipped $event) use ($order) {
    return $event->order->id === $order->id;
});
```

특정 이벤트에 대해 어떤 리스너가 정상적으로 리스닝하고 있는지를 단순히 검증하고 싶다면, `assertListening` 메서드를 사용할 수 있습니다.

```php
Event::assertListening(
    OrderShipped::class,
    SendShipmentNotification::class
);
```

> [!WARNING]
> `Event::fake()`를 호출한 이후에는 어떠한 이벤트 리스너도 실행되지 않습니다. 따라서, 테스트에서 이벤트에 의존하는 모델 팩토리를 사용하는 경우(예: 모델의 `creating` 이벤트에서 UUID를 생성하는 등), 팩토리 사용 **이후**에 `Event::fake()`를 호출해야 합니다.

<a name="faking-a-subset-of-events"></a>
### 특정 이벤트만 페이크 처리하기

특정 이벤트 리스너만 페이크(faking)하고 싶다면, `fake` 또는 `fakeFor` 메서드에 해당 이벤트들을 명시적으로 전달하면 됩니다.

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

또한, `except` 메서드를 사용하면 명시한 이벤트를 제외하고, 나머지 모든 이벤트를 페이크 처리할 수 있습니다.

```php
Event::fake()->except([
    OrderCreated::class,
]);
```

<a name="scoped-event-fakes"></a>
### 범위 지정 이벤트 페이크

테스트의 일부 구간에서만 이벤트 리스너를 페이크하고, 나머지 구간에서는 원래대로 동작하게 하려면 `fakeFor` 메서드를 사용할 수 있습니다.

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