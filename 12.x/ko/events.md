# 이벤트 (Events)

- [소개](#introduction)
- [이벤트 및 리스너 생성](#generating-events-and-listeners)
- [이벤트 및 리스너 등록](#registering-events-and-listeners)
    - [이벤트 자동 탐색](#event-discovery)
    - [이벤트 수동 등록](#manually-registering-events)
    - [클로저 리스너](#closure-listeners)
- [이벤트 정의하기](#defining-events)
- [리스너 정의하기](#defining-listeners)
- [큐에 등록되는 이벤트 리스너](#queued-event-listeners)
    - [큐와 직접 상호작용하기](#manually-interacting-with-the-queue)
    - [이벤트 리스너와 데이터베이스 트랜잭션](#queued-event-listeners-and-database-transactions)
    - [실패한 작업 처리](#handling-failed-jobs)
- [이벤트 디스패치하기](#dispatching-events)
    - [데이터베이스 트랜잭션 후 이벤트 디스패치](#dispatching-events-after-database-transactions)
- [이벤트 구독자](#event-subscribers)
    - [이벤트 구독자 작성](#writing-event-subscribers)
    - [이벤트 구독자 등록](#registering-event-subscribers)
- [테스트](#testing)
    - [일부 이벤트만 페이크 사용하기](#faking-a-subset-of-events)
    - [범위 지정 이벤트 페이크](#scoped-event-fakes)

<a name="introduction"></a>
## 소개

라라벨의 이벤트 기능은 간단한 옵저버 패턴을 구현하여, 애플리케이션에서 발생하는 다양한 이벤트를 구독하고 리스닝할 수 있도록 해줍니다. 이벤트 클래스는 일반적으로 `app/Events` 디렉토리에, 리스너 클래스는 `app/Listeners` 디렉토리에 저장됩니다. 만약 여러분의 애플리케이션에 이 디렉토리가 없다면 걱정하지 마세요. Artisan 콘솔 명령어로 이벤트와 리스너를 생성하면 자동으로 만들어집니다.

이벤트를 사용하면 애플리케이션의 각 부분을 느슨하게 결합할 수 있습니다. 하나의 이벤트에 여러 리스너가 연결될 수 있고, 각각은 서로에게 의존하지 않으므로 코드 구조가 깔끔해집니다. 예를 들어 주문이 발송될 때마다 Slack으로 알림을 보내고 싶다고 가정해봅시다. 주문 처리 코드와 Slack 알림 코드를 직접 연결하는 대신, `App\Events\OrderShipped` 이벤트를 발생시키고, 이 이벤트를 감지하는 리스너에서 Slack 알림을 발송하도록 만들 수 있습니다.

<a name="generating-events-and-listeners"></a>
## 이벤트 및 리스너 생성

이벤트와 리스너를 빠르게 생성하려면 `make:event` 및 `make:listener` 아티즌 명령어를 사용할 수 있습니다:

```shell
php artisan make:event PodcastProcessed

php artisan make:listener SendPodcastNotification --event=PodcastProcessed
```

편의를 위해, 추가 인수 없이 `make:event`와 `make:listener` 명령을 실행하면 라라벨이 클래스명(그리고 리스너를 만들 때는 리스너가 감지할 이벤트)을 직접 입력하라고 안내합니다:

```shell
php artisan make:event

php artisan make:listener
```

<a name="registering-events-and-listeners"></a>
## 이벤트 및 리스너 등록

<a name="event-discovery"></a>
### 이벤트 자동 탐색

기본적으로 라라벨은 애플리케이션의 `Listeners` 디렉토리를 검색하여 이벤트 리스너를 자동으로 찾고 등록합니다. 라라벨은 리스너 클래스의 메서드 중 `handle` 또는 `__invoke`로 시작하는 메서드를 발견하면, 해당 메서드의 시그니처에 타입힌트 되어 있는 이벤트를 자동으로 감지하여 리스너로 등록합니다:

```php
use App\Events\PodcastProcessed;

class SendPodcastNotification
{
    /**
     * 이벤트를 처리합니다.
     */
    public function handle(PodcastProcessed $event): void
    {
        // ...
    }
}
```

여러 개의 이벤트를 PHP의 유니온 타입을 이용하여 한 번에 감지할 수도 있습니다:

```php
/**
 * 이벤트를 처리합니다.
 */
public function handle(PodcastProcessed|PodcastPublished $event): void
{
    // ...
}
```

만약 리스너를 다른 디렉토리 또는 여러 디렉토리에 보관하고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에서 `withEvents` 메서드를 사용하여 탐색할 디렉토리를 지정할 수 있습니다:

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/Orders/Listeners',
])
```

`*` 문자를 와일드카드로 사용하면 비슷한 여러 디렉토리에서 리스너를 한 번에 탐색할 수 있습니다:

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/*/Listeners',
])
```

이벤트로 등록된 모든 리스너를 확인하려면 `event:list` 명령어를 사용할 수 있습니다:

```shell
php artisan event:list
```

<a name="event-discovery-in-production"></a>
#### 운영 환경에서의 이벤트 탐색

애플리케이션의 속도를 높이기 위해, `optimize` 또는 `event:cache` 아티즌 명령어를 사용하여 모든 리스너의 매니페스트를 캐시하는 것이 좋습니다. 이 명령어는 일반적으로 애플리케이션 [배포 과정](/docs/12.x/deployment#optimization)의 일부로 실행해야 합니다. 이 매니페스트는 프레임워크가 이벤트 등록을 더 빠르게 처리하는 데 사용됩니다. 만약 이벤트 캐시를 제거하려면 `event:clear` 명령어를 사용하세요.

<a name="manually-registering-events"></a>
### 이벤트 수동 등록

`Event` 파사드를 이용하면, 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 이벤트와 그에 대응되는 리스너를 직접 등록할 수 있습니다:

```php
use App\Domain\Orders\Events\PodcastProcessed;
use App\Domain\Orders\Listeners\SendPodcastNotification;
use Illuminate\Support\Facades\Event;

/**
 * 애플리케이션 서비스를 부트스트랩합니다.
 */
public function boot(): void
{
    Event::listen(
        PodcastProcessed::class,
        SendPodcastNotification::class,
    );
}
```

이벤트로 등록된 모든 리스너를 확인하려면 다음과 같이 명령어를 사용할 수 있습니다:

```shell
php artisan event:list
```

<a name="closure-listeners"></a>
### 클로저 리스너

보통 리스너는 클래스로 정의하지만, `AppServiceProvider`의 `boot` 메서드에서 클로저(익명 함수) 형태의 이벤트 리스너도 수동으로 등록할 수 있습니다:

```php
use App\Events\PodcastProcessed;
use Illuminate\Support\Facades\Event;

/**
 * 애플리케이션 서비스를 부트스트랩합니다.
 */
public function boot(): void
{
    Event::listen(function (PodcastProcessed $event) {
        // ...
    });
}
```

<a name="queuable-anonymous-event-listeners"></a>
#### 큐에 등록되는 익명(클로저) 이벤트 리스너

클로저 기반 이벤트 리스너를 등록할 때, 리스너 클로저를 `Illuminate\Events\queueable` 함수로 감싸면 해당 리스너가 [큐](/docs/12.x/queues)를 통해 실행되도록 할 수 있습니다:

```php
use App\Events\PodcastProcessed;
use function Illuminate\Events\queueable;
use Illuminate\Support\Facades\Event;

/**
 * 애플리케이션 서비스를 부트스트랩합니다.
 */
public function boot(): void
{
    Event::listen(queueable(function (PodcastProcessed $event) {
        // ...
    }));
}
```

큐를 사용하는 작업과 마찬가지로, `onConnection`, `onQueue`, `delay` 메서드를 함께 사용해 큐 연결, 큐 이름, 지연 시간을 자유롭게 설정할 수 있습니다:

```php
Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->onConnection('redis')->onQueue('podcasts')->delay(now()->addSeconds(10)));
```

익명 큐 리스너가 실패했을 때 처리 로직을 추가하고 싶다면, `queueable` 리스너 정의 시 `catch` 메서드에 클로저를 전달하면 됩니다. 이 클로저는 이벤트 인스턴스와 오류의 원인이 된 `Throwable` 인스턴스를 전달받습니다:

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

`*` 문자를 와일드카드 파라미터로 사용해, 여러 이벤트를 하나의 리스너에서 처리할 수도 있습니다. 와일드카드 리스너는 첫 번째 인수로 이벤트 이름, 두 번째 인수로 전체 이벤트 데이터 배열을 받습니다:

```php
Event::listen('event.*', function (string $eventName, array $data) {
    // ...
});
```

<a name="defining-events"></a>
## 이벤트 정의하기

이벤트 클래스는 본질적으로 이벤트와 관련된 정보를 담는 데이터 컨테이너 역할을 합니다. 예를 들어, `App\Events\OrderShipped` 이벤트가 [Eloquent ORM](/docs/12.x/eloquent) 객체를 받는다고 가정하겠습니다:

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
     * 새로운 이벤트 인스턴스를 생성합니다.
     */
    public function __construct(
        public Order $order,
    ) {}
}
```

보시는 것처럼, 이 이벤트 클래스는 별도의 로직을 포함하지 않습니다. 단지 구매된 `App\Models\Order` 인스턴스를 담고 있는 컨테이너입니다. 이벤트에서 사용하는 `SerializesModels` 트레이트는 이벤트 객체를 PHP의 `serialize`로 직렬화할 때(예: [큐 리스너 사용 시](#queued-event-listeners)), Eloquent 모델을 적절히 직렬화해줍니다.

<a name="defining-listeners"></a>
## 리스너 정의하기

이제 예시 이벤트의 리스너를 살펴보겠습니다. 이벤트 리스너는 `handle` 메서드에서 이벤트 인스턴스를 받습니다. `make:listener` 아티즌 명령어를 `--event` 옵션과 함께 사용하면, 올바른 이벤트 클래스를 자동으로 import하고, `handle` 메서드에 타입힌트까지 추가해줍니다. `handle` 메서드 안에서 이벤트에 대한 다양한 응답 동작을 구현할 수 있습니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;

class SendShipmentNotification
{
    /**
     * 이벤트 리스너를 생성합니다.
     */
    public function __construct() {}

    /**
     * 이벤트를 처리합니다.
     */
    public function handle(OrderShipped $event): void
    {
        // $event->order로 주문 정보를 접근할 수 있습니다...
    }
}
```

> [!NOTE]
> 이벤트 리스너의 생성자에서 필요한 의존성을 타입힌트로 선언할 수도 있습니다. 모든 이벤트 리스너는 라라벨 [서비스 컨테이너](/docs/12.x/container)를 통해 해결되므로, 의존성은 자동으로 주입됩니다.

<a name="stopping-the-propagation-of-an-event"></a>
#### 이벤트 전파 멈추기

특정 상황에서, 이벤트가 다른 리스너로 전달되는 것을 멈추고 싶을 때가 있습니다. 이럴 땐 리스너의 `handle` 메서드에서 `false`를 반환하면 됩니다.

<a name="queued-event-listeners"></a>
## 큐에 등록되는 이벤트 리스너

이메일 발송이나 HTTP 요청 등 시간이 오래 걸리는 작업을 리스너가 처리한다면, 리스너를 큐에 등록하는 것이 유리합니다. 큐 리스너를 사용하기 전에 [큐 설정](/docs/12.x/queues)을 완료하고, 서버나 개발 환경에서 큐 워커를 실행해야 합니다.

리스너가 큐에 등록되어야 한다는 것을 지정하려면 리스너 클래스에 `ShouldQueue` 인터페이스를 추가하면 됩니다. `make:listener` 명령어로 생성된 리스너에는 이미 이 인터페이스가 import되어 있습니다:

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

이렇게 설정하면, 이 리스너가 처리하는 이벤트가 디스패치될 때 자동으로 큐에 등록되어 라라벨의 [큐 시스템](/docs/12.x/queues)을 통해 실행됩니다. 큐에서 리스너 실행 시 예외가 발생하지 않으면, 해당 작업은 처리 후 자동으로 삭제됩니다.

<a name="customizing-the-queue-connection-queue-name"></a>
#### 큐 연결, 큐 이름, 지연 시간 커스터마이징

이벤트 리스너의 큐 연결, 큐 이름, 큐 지연 시간(딜레이)을 커스터마이징하고 싶다면, 리스너 클래스에서 각각 `$connection`, `$queue`, `$delay` 속성을 정의하면 됩니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    /**
     * 작업이 보내질 연결 이름입니다.
     *
     * @var string|null
     */
    public $connection = 'sqs';

    /**
     * 작업이 보내질 큐 이름입니다.
     *
     * @var string|null
     */
    public $queue = 'listeners';

    /**
     * 작업이 처리되기 전까지의 시간(초)입니다.
     *
     * @var int
     */
    public $delay = 60;
}
```

실행 중에(런타임에) 큐 연결, 큐 이름, 지연 시간을 동적으로 지정하려면 `viaConnection`, `viaQueue`, `withDelay` 메서드를 리스너에 정의하면 됩니다:

```php
/**
 * 큐 연결 이름을 반환합니다.
 */
public function viaConnection(): string
{
    return 'sqs';
}

/**
 * 큐 이름을 반환합니다.
 */
public function viaQueue(): string
{
    return 'listeners';
}

/**
 * 작업이 처리되기까지 대기할 초를 반환합니다.
 */
public function withDelay(OrderShipped $event): int
{
    return $event->highPriority ? 0 : 60;
}
```

<a name="conditionally-queueing-listeners"></a>
#### 조건부 큐 등록

경우에 따라 리스너를 큐에 등록할지 말지, 런타임 데이터에 따라 결정해야 할 수 있습니다. 이럴 때 리스너에 `shouldQueue` 메서드를 추가해, 리스너를 큐에 등록해야 하면 `true`, 아니면 `false`를 반환하도록 만듭니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderCreated;
use Illuminate\Contracts\Queue\ShouldQueue;

class RewardGiftCard implements ShouldQueue
{
    /**
     * 고객에게 기프트카드를 제공합니다.
     */
    public function handle(OrderCreated $event): void
    {
        // ...
    }

    /**
     * 리스너를 큐에 등록할지 여부를 결정합니다.
     */
    public function shouldQueue(OrderCreated $event): bool
    {
        return $event->order->subtotal >= 5000;
    }
}
```

<a name="manually-interacting-with-the-queue"></a>
### 큐와 직접 상호작용하기

리스너 내부에서 큐 작업의 `delete`, `release` 등의 메서드에 직접 접근하려면, `Illuminate\Queue\InteractsWithQueue` 트레이트를 사용할 수 있습니다. 이 트레이트는 기본적으로 생성된 리스너에 포함되어 있으며, 이를 통해 해당 메서드에 접근할 수 있습니다:

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
### 이벤트 리스너와 데이터베이스 트랜잭션

큐에 등록된 리스너가 데이터베이스 트랜잭션 중에 디스패치되면, 큐가 트랜잭션이 커밋되기 전에 리스너를 먼저 실행할 수 있습니다. 이 경우, 트랜잭션 내에서 모델이나 데이터베이스 레코드를 변경했더라도 아직 DB에 반영되지 않았을 수 있습니다. 또한 트랜잭션 도중 생긴 모델/레코드는 아직 DB에 없기도 합니다. 이런 데이터에 의존하는 리스너라면, 예기치 않은 에러가 발생할 수 있습니다.

큐 연결의 `after_commit` 설정이 `false`일 때, 특정 큐 리스너는 모든 DB 트랜잭션이 커밋된 후에만 디스패치되도록 하려면 리스너 클래스에 `ShouldQueueAfterCommit` 인터페이스를 구현하면 됩니다:

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
> 이 문제를 우회하는 자세한 방법은 [큐 작업과 데이터베이스 트랜잭션](/docs/12.x/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="handling-failed-jobs"></a>
### 실패한 작업 처리

가끔 큐에 등록된 이벤트 리스너가 실패할 수 있습니다. 큐 리스너가 큐 워커에 설정한 최대 재시도 횟수를 초과하면, 리스너의 `failed` 메서드가 호출됩니다. 이 메서드는 이벤트 인스턴스와 실패의 원인이 된 `Throwable` 인스턴스를 전달받습니다:

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
     * 작업 실패를 처리합니다.
     */
    public function failed(OrderShipped $event, Throwable $exception): void
    {
        // ...
    }
}
```

<a name="specifying-queued-listener-maximum-attempts"></a>
#### 큐 리스너 최대 시도 횟수 지정

큐에 등록된 특정 리스너가 계속해서 오류를 발생시키는 상황에서는, 무한정 재시도하는 것을 막아야 할 수도 있습니다. 라라벨에서는 리스너별로 시도 횟수 또는 시도 가능한 시간을 지정할 수 있는 다양한 방법을 제공합니다.

리스너 클래스에 `$tries` 속성을 추가하면, 지정한 횟수만큼 시도 후 실패로 간주됩니다:

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
     * 큐 리스너 재시도 가능 횟수입니다.
     *
     * @var int
     */
    public $tries = 5;
}
```

특정 횟수 대신, 지정한 시점까지는 몇 번이고 시도해도 되도록 하려면, 리스너 클래스에 `retryUntil` 메서드를 추가해서 리스너의 재시도가 만료될 DateTime을 반환하면 됩니다:

```php
use DateTime;

/**
 * 리스너가 시간 초과해야 하는 시점을 반환합니다.
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(5);
}
```

<a name="specifying-queued-listener-backoff"></a>
#### 큐 리스너 백오프(대기 시간) 지정

리스너가 예외로 인해 재시도될 때, 재시도까지 몇 초를 기다릴지 지정하려면 리스너 클래스에 `backoff` 속성을 추가하면 됩니다:

```php
/**
 * 재시도까지 대기할 초(second)입니다.
 *
 * @var int
 */
public $backoff = 3;
```

더 복잡한 백오프 로직이 필요하다면, `backoff` 메서드를 정의할 수도 있습니다:

```php
/**
 * 큐 리스너 재시도까지 대기할 초(second)를 계산해서 반환합니다.
 */
public function backoff(): int
{
    return 3;
}
```

"지수 증가" 형태의 백오프를 쉽게 지정하고 싶다면, `backoff` 메서드에서 배열로 값을 반환하면 됩니다. 예를 들어, 아래와 같이 지정하면 첫 번째 재시도는 1초, 두 번째는 5초, 세 번째는 10초, 그 이후는 10초 간격으로 대기합니다:

```php
/**
 * 큐 리스너 재시도까지 대기할 초(second)들을 반환합니다.
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

이벤트를 실행(디스패치)하려면, 이벤트 클래스의 정적 `dispatch` 메서드를 호출하면 됩니다. 이 메서드는 `Illuminate\Foundation\Events\Dispatchable` 트레이트를 활용해 이벤트에 제공됩니다. `dispatch`에 전달한 인수들은 이벤트의 생성자로 그대로 넘어갑니다:

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
     * 전달받은 주문을 발송합니다.
     */
    public function store(Request $request): RedirectResponse
    {
        $order = Order::findOrFail($request->order_id);

        // 주문 발송 로직...

        OrderShipped::dispatch($order);

        return redirect('/orders');
    }
}
```

이벤트 디스패치 여부를 조건부로 걸고 싶다면 `dispatchIf`, `dispatchUnless` 메서드를 사용할 수 있습니다:

```php
OrderShipped::dispatchIf($condition, $order);

OrderShipped::dispatchUnless($condition, $order);
```

> [!NOTE]
> 테스트를 진행할 때, 실제로 리스너를 트리거하지 않고도 특정 이벤트가 디스패치됐는지 assert(검증)할 수 있으면 아주 유용합니다. 라라벨의 [내장 테스트 헬퍼](#testing)로 쉽게 처리할 수 있습니다.

<a name="dispatching-events-after-database-transactions"></a>
### 데이터베이스 트랜잭션 후 이벤트 디스패치

경우에 따라, 현재 진행 중인 데이터베이스 트랜잭션이 커밋된 후에만 이벤트를 디스패치하고 싶을 수 있습니다. 이를 위해 이벤트 클래스에 `ShouldDispatchAfterCommit` 인터페이스를 구현하면 됩니다.

이 인터페이스를 구현하면, 라라벨은 트랜잭션이 커밋된 후에만 이벤트를 디스패치합니다. 만약 트랜잭션이 실패하면 이벤트는 폐기됩니다. 트랜잭션이 없다면 이벤트가 즉시 디스패치됩니다:

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
     * 새로운 이벤트 인스턴스를 생성합니다.
     */
    public function __construct(
        public Order $order,
    ) {}
}
```

<a name="event-subscribers"></a>
## 이벤트 구독자

<a name="writing-event-subscribers"></a>
### 이벤트 구독자 작성

이벤트 구독자(subscriber)는 여러 이벤트에 대해 하나의 클래스 안에서 모두 응답할 수 있도록 해주는 클래스입니다. 즉, 한 클래스에서 여러 이벤트 핸들러를 정의할 수 있습니다. Subscriber 클래스에는 `subscribe` 메서드를 정의해야 하며, 이 메서드는 이벤트 디스패처(Dispatcher) 인스턴스를 전달받습니다. 해당 디스패처의 `listen` 메서드를 호출해 이벤트와 리스너를 등록할 수 있습니다:

```php
<?php

namespace App\Listeners;

use Illuminate\Auth\Events\Login;
use Illuminate\Auth\Events\Logout;
use Illuminate\Events\Dispatcher;

class UserEventSubscriber
{
    /**
     * 사용자 로그인 이벤트 처리.
     */
    public function handleUserLogin(Login $event): void {}

    /**
     * 사용자 로그아웃 이벤트 처리.
     */
    public function handleUserLogout(Logout $event): void {}

    /**
     * Subscriber에 대한 리스너 등록.
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

구독자 내부에 이벤트 리스너 메서드가 정의되어 있다면, `subscribe` 메서드에서 이벤트와 메서드 이름을 맵 형태의 배열로 반환하는 것이 더 편할 수도 있습니다. 라라벨은 자동으로 클래스명을 파악해 이벤트 리스너 등록을 처리합니다:

```php
<?php

namespace App\Listeners;

use Illuminate\Auth\Events\Login;
use Illuminate\Auth\Events\Logout;
use Illuminate\Events\Dispatcher;

class UserEventSubscriber
{
    /**
     * 사용자 로그인 이벤트 처리.
     */
    public function handleUserLogin(Login $event): void {}

    /**
     * 사용자 로그아웃 이벤트 처리.
     */
    public function handleUserLogout(Logout $event): void {}

    /**
     * Subscriber에 대한 리스너 등록.
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

구독자를 작성한 후, 구독자 클래스가 라라벨의 [이벤트 자동 탐색 규칙](#event-discovery)을 따르고 있다면 리스너 메서드가 자동으로 등록됩니다. 그렇지 않은 경우, `Event` 파사드의 `subscribe` 메서드로 구독자를 수동 등록할 수 있습니다. 일반적으로 이는 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 수행됩니다:

```php
<?php

namespace App\Providers;

use App\Listeners\UserEventSubscriber;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스를 부트스트랩합니다.
     */
    public function boot(): void
    {
        Event::subscribe(UserEventSubscriber::class);
    }
}
```

<a name="testing"></a>
## 테스트

이벤트를 디스패치하는 코드를 테스트할 때, 실제로 이벤트 리스너가 실행되지 않도록 하고 싶을 때가 있습니다. 리스너의 코드는 별도로 테스트할 수 있으니, 이벤트 디스패치만 검증하면 되는 경우입니다. 물론 리스너 자체를 테스트할 땐, 리스너 인스턴스를 직접 생성해서 `handle` 메서드를 호출하면 됩니다.

`Event` 파사드의 `fake` 메서드를 사용하면, 리스너 실행 없이 코드의 이벤트 디스패치 여부만 검사할 수 있습니다. 그런 다음 `assertDispatched`, `assertNotDispatched`, `assertNothingDispatched` 메서드로 어떤 이벤트가 실행되었는지 검증합니다:

```php tab=Pest
<?php

use App\Events\OrderFailedToShip;
use App\Events\OrderShipped;
use Illuminate\Support\Facades\Event;

test('orders can be shipped', function () {
    Event::fake();

    // 주문 발송 실행...

    // 이벤트가 디스패치됐는지 검증...
    Event::assertDispatched(OrderShipped::class);

    // 이벤트가 두 번 디스패치됐는지 검증...
    Event::assertDispatched(OrderShipped::class, 2);

    // 이벤트가 디스패치되지 않았는지 검증...
    Event::assertNotDispatched(OrderFailedToShip::class);

    // 아무 이벤트도 디스패치되지 않았는지 검증...
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

        // 주문 발송 실행...

        // 이벤트가 디스패치됐는지 검증...
        Event::assertDispatched(OrderShipped::class);

        // 이벤트가 두 번 디스패치됐는지 검증...
        Event::assertDispatched(OrderShipped::class, 2);

        // 이벤트가 디스패치되지 않았는지 검증...
        Event::assertNotDispatched(OrderFailedToShip::class);

        // 아무 이벤트도 디스패치되지 않았는지 검증...
        Event::assertNothingDispatched();
    }
}
```

`assertDispatched` 또는 `assertNotDispatched`에 클로저를 전달하면, 해당 클로저의 조건을 "통과"하는 이벤트가 실제로 디스패치되었는지 검증할 수도 있습니다. 해당 조건을 만족하는 이벤트가 최소 하나라도 디스패치됐다면 성공입니다:

```php
Event::assertDispatched(function (OrderShipped $event) use ($order) {
    return $event->order->id === $order->id;
});
```

특정 이벤트에 대해 어떤 리스너가 리스닝하고 있는지 검증하고 싶을 때는 `assertListening` 메서드를 사용하면 됩니다:

```php
Event::assertListening(
    OrderShipped::class,
    SendShipmentNotification::class
);
```

> [!WARNING]
> `Event::fake()`를 호출한 이후에 이벤트 리스너가 실행되지 않습니다. 따라서, 팩토리를 사용해 UUID를 생성하는 등 이벤트에 의존하는 모델 팩토리를 테스트하는 경우에는 팩토리 실행 후에 `Event::fake()`를 호출해야 합니다.

<a name="faking-a-subset-of-events"></a>
### 일부 이벤트만 페이크 사용하기

특정 이벤트에 대해서만 리스너를 fake(실행 막기)하고 싶다면, 해당 이벤트들을 `fake` 또는 `fakeFor` 메서드에 배열로 전달하면 됩니다:

```php tab=Pest
test('orders can be processed', function () {
    Event::fake([
        OrderCreated::class,
    ]);

    $order = Order::factory()->create();

    Event::assertDispatched(OrderCreated::class);

    // 그 외 이벤트들은 정상적으로 실행됨...
    $order->update([...]);
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

    // 그 외 이벤트들은 정상적으로 실행됨...
    $order->update([...]);
}
```

반대로 일부 이벤트만 실제로 리스너가 실행되고, 나머지 이벤트들만 fake로 처리하고 싶다면, `except` 메서드를 사용할 수 있습니다:

```php
Event::fake()->except([
    OrderCreated::class,
]);
```

<a name="scoped-event-fakes"></a>
### 범위 지정 이벤트 페이크

테스트 코드의 특정 구간에서만 이벤트 리스너를 fake로 처리하고 싶을 때는, `fakeFor` 메서드를 사용할 수 있습니다:

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

    // 이벤트가 정상적으로 실행되고, 옵저버도 함께 동작함...
    $order->update([...]);
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

        // 이벤트가 정상적으로 실행되고, 옵저버도 함께 동작함...
        $order->update([...]);
    }
}
```
