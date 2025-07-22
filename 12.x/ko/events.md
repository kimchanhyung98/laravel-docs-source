# 이벤트 (Events)

- [소개](#introduction)
- [이벤트 및 리스너 생성](#generating-events-and-listeners)
- [이벤트 및 리스너 등록](#registering-events-and-listeners)
    - [이벤트 자동 감지](#event-discovery)
    - [이벤트 수동 등록](#manually-registering-events)
    - [클로저 리스너](#closure-listeners)
- [이벤트 정의하기](#defining-events)
- [리스너 정의하기](#defining-listeners)
- [큐에 저장되는 이벤트 리스너](#queued-event-listeners)
    - [큐 직접 제어하기](#manually-interacting-with-the-queue)
    - [큐 리스너와 데이터베이스 트랜잭션](#queued-event-listeners-and-database-transactions)
    - [큐 리스너용 미들웨어](#queued-listener-middleware)
    - [암호화된 큐 리스너](#encrypted-queued-listeners)
    - [실패한 작업 처리](#handling-failed-jobs)
- [이벤트 디스패치](#dispatching-events)
    - [데이터베이스 트랜잭션 이후 이벤트 디스패치하기](#dispatching-events-after-database-transactions)
- [이벤트 구독자](#event-subscribers)
    - [이벤트 구독자 작성](#writing-event-subscribers)
    - [이벤트 구독자 등록](#registering-event-subscribers)
- [테스트](#testing)
    - [일부 이벤트만 페이크로 대체하기](#faking-a-subset-of-events)
    - [범위 지정 이벤트 페이크](#scoped-event-fakes)

<a name="introduction"></a>
## 소개

Laravel의 이벤트 기능은 단순한 옵저버 패턴을 구현하여, 애플리케이션 내에서 발생하는 다양한 이벤트를 구독하고 리스닝할 수 있도록 지원합니다. 일반적으로 이벤트 클래스는 `app/Events` 디렉터리에, 해당 리스너는 `app/Listeners` 디렉터리에 저장합니다. 만약 애플리케이션에 이 디렉터리가 보이지 않더라도 걱정하지 마십시오. Artisan 콘솔 명령어로 이벤트와 리스너를 생성할 때 자동으로 만들어집니다.

이벤트를 사용하면 애플리케이션의 여러 부분을 느슨하게 결합할 수 있습니다. 하나의 이벤트에 여러 리스너를 연결할 수 있지만, 이 리스너들은 서로에게 의존하지 않습니다. 예를 들어, 주문이 배송될 때마다 사용자에게 Slack 알림을 보내고 싶다고 가정해봅니다. 주문 처리 코드에 Slack 알림 코드를 직접 연결하는 대신, `App\Events\OrderShipped` 이벤트를 발생시키고, 리스너를 통해 Slack 알림 전송을 처리할 수 있습니다.

<a name="generating-events-and-listeners"></a>
## 이벤트 및 리스너 생성

이벤트와 리스너를 빠르게 생성하려면 `make:event` 및 `make:listener` Artisan 명령어를 사용할 수 있습니다:

```shell
php artisan make:event PodcastProcessed

php artisan make:listener SendPodcastNotification --event=PodcastProcessed
```

또한 `make:event` 및 `make:listener` Artisan 명령어를 추가 인자 없이 실행할 수도 있습니다. 이 경우 Laravel이 클래스 이름(그리고 리스너를 만드는 경우 연결해야 할 이벤트)을 자동으로 입력 받도록 안내합니다:

```shell
php artisan make:event

php artisan make:listener
```

<a name="registering-events-and-listeners"></a>
## 이벤트 및 리스너 등록

<a name="event-discovery"></a>
### 이벤트 자동 감지

기본적으로 Laravel은 애플리케이션의 `Listeners` 디렉터리를 스캔하여 이벤트 리스너를 자동으로 찾고 등록합니다. Laravel은 리스너 클래스 내의 메서드명 중 `handle` 또는 `__invoke`로 시작하는 메서드를 찾아, 해당 시그니처에 명시적으로 타입힌트된 이벤트에 대한 리스너로 등록합니다:

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

PHP의 유니언 타입을 사용하여 여러 이벤트를 동시에 리스닝할 수도 있습니다:

```php
/**
 * Handle the event.
 */
public function handle(PodcastProcessed|PodcastPublished $event): void
{
    // ...
}
```

리스너를 다른 디렉터리 또는 여러 디렉터리에 보관하고 싶을 경우, 애플리케이션의 `bootstrap/app.php` 파일에서 `withEvents` 메서드를 사용해 Laravel이 지정한 디렉터리들을 스캔하도록 설정할 수 있습니다:

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/Orders/Listeners',
])
```

`*` 문자를 와일드카드로 사용해서 여러 비슷한 디렉터리를 한 번에 스캔할 수도 있습니다:

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/*/Listeners',
])
```

애플리케이션에 등록된 모든 리스너 목록을 확인하려면 `event:list` 명령어를 사용할 수 있습니다:

```shell
php artisan event:list
```

<a name="event-discovery-in-production"></a>
#### 프로덕션 환경에서의 이벤트 자동 감지

애플리케이션의 성능을 높이려면, `optimize` 또는 `event:cache` Artisan 명령어를 이용해 리스너 목록을 캐시해야 합니다. 보통 이 명령어는 애플리케이션 [배포 과정](/docs/12.x/deployment#optimization)에 포함되어야 합니다. 캐시된 목록(manifest)은 프레임워크가 이벤트 등록 과정을 빠르게 처리하는 데 사용됩니다. `event:clear` 명령어로 이벤트 캐시를 제거할 수 있습니다.

<a name="manually-registering-events"></a>
### 이벤트 수동 등록

`Event` 파사드를 사용하여, 애플리케이션의 `AppServiceProvider`의 `boot` 메서드 내에서 이벤트와 해당 리스너를 직접 수동으로 등록할 수도 있습니다:

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

애플리케이션에 등록된 모든 리스너를 확인하려면 `event:list` 명령어를 사용할 수 있습니다:

```shell
php artisan event:list
```

<a name="closure-listeners"></a>
### 클로저 리스너

일반적으로 리스너는 클래스 형태로 정의되지만, 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 클로저(익명 함수) 기반의 이벤트 리스너를 직접 등록할 수도 있습니다:

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
#### 큐에 저장되는 익명(클로저) 이벤트 리스너

클로저 기반 이벤트 리스너를 등록할 때, 리스너 클로저를 `Illuminate\Events\queueable` 함수로 감싸면, Laravel이 해당 리스너를 [큐](/docs/12.x/queues)에서 실행하도록 명령할 수 있습니다:

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

큐 작업과 마찬가지로, `onConnection`, `onQueue`, `delay` 메서드를 이용해 큐 리스너의 실행 환경 및 지연 시간을 커스터마이징할 수 있습니다:

```php
Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->onConnection('redis')->onQueue('podcasts')->delay(now()->addSeconds(10)));
```

익명 큐 리스너에서 실패를 처리하고 싶은 경우, `queueable`로 감싼 리스너에 대해 `catch` 메서드로 클로저를 전달할 수 있습니다. 이 클로저는 이벤트 인스턴스와 실패의 원인이 된 `Throwable` 인스턴스를 인자로 받습니다:

```php
use App\Events\PodcastProcessed;
use function Illuminate\Events\queueable;
use Illuminate\Support\Facades\Event;
use Throwable;

Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->catch(function (PodcastProcessed $event, Throwable $e) {
    // 큐 리스너가 실패했을 때 처리...
}));
```

<a name="wildcard-event-listeners"></a>
#### 와일드카드 이벤트 리스너

이벤트 이름에 `*` 문자를 와일드카드로 사용하여 여러 이벤트를 하나의 리스너에서 처리할 수도 있습니다. 와일드카드 리스너는 첫 번째 인자로 이벤트명, 두 번째 인자로 전체 이벤트 데이터 배열을 전달받습니다:

```php
Event::listen('event.*', function (string $eventName, array $data) {
    // ...
});
```

<a name="defining-events"></a>
## 이벤트 정의하기

이벤트 클래스는 본질적으로 해당 이벤트와 관련된 정보를 담는 데이터 컨테이너입니다. 예를 들어, `App\Events\OrderShipped` 이벤트가 [Eloquent ORM](/docs/12.x/eloquent) 오브젝트를 전달받는다고 가정해보겠습니다:

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

보시다시피, 이 이벤트 클래스에는 별도의 로직이 없습니다. 단순히 구매된 `App\Models\Order` 인스턴스를 담는 역할만 합니다. 이벤트 내에서 사용하는 `SerializesModels` 트레이트는 이벤트 오브젝트가 PHP의 `serialize` 함수로 직렬화될 때(예: [큐 리스너](#queued-event-listeners)를 사용할 경우) Eloquent 모델을 적절히 직렬화해줍니다.

<a name="defining-listeners"></a>
## 리스너 정의하기

이제 앞서 본 예시 이벤트에 대한 리스너를 살펴보겠습니다. 이벤트 리스너는 `handle` 메서드에서 이벤트 인스턴스를 전달받습니다. `make:listener` Artisan 명령에 `--event` 옵션을 주면, 해당 이벤트 클래스를 자동으로 import 하고, `handle` 메서드에 타입힌트까지 지정해줍니다. `handle` 메서드 내부에서는 이벤트에 대한 다양한 처리 작업을 수행할 수 있습니다:

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
        // $event->order 를 사용해 주문 정보 접근...
    }
}
```

> [!NOTE]
> 이벤트 리스너의 생성자에서 필요한 의존성을 타입힌트로 지정할 수도 있습니다. 모든 이벤트 리스너는 Laravel [서비스 컨테이너](/docs/12.x/container)를 통해 해결(resolved) 되므로, 의존성은 자동으로 주입됩니다.

<a name="stopping-the-propagation-of-an-event"></a>
#### 이벤트 전달(전파) 중단하기

특정 상황에서는, 한 이벤트가 다른 리스너에게 더 이상 전달(전파)되지 않게 하고 싶을 수 있습니다. 이럴 때는 리스너의 `handle` 메서드에서 `false`를 반환하면 됩니다.

<a name="queued-event-listeners"></a>
## 큐에 저장되는 이벤트 리스너

이메일 전송이나 HTTP 요청 등 시간이 오래 걸리는 작업을 리스너가 수행한다면, 리스너를 큐에 저장하여 비동기적으로 실행하는 것이 유리합니다. 큐 리스너를 사용하기 전에는 [큐 설정](/docs/12.x/queues)을 완료하고, 서버나 로컬 개발 환경에서 큐 워커를 실행해두어야 합니다.

리스너를 큐에 저장하도록 지정하려면, 리스너 클래스에 `ShouldQueue` 인터페이스를 구현하면 됩니다. `make:listener` Artisan 명령으로 생성한 리스너에는 기본적으로 이 인터페이스가 import됩니다:

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

이렇게 하면 해당 이벤트가 발생할 때, 이벤트 디스패처는 리스너를 Laravel의 [큐 시스템](/docs/12.x/queues)을 통해 자동으로 큐에 등록합니다. 큐 워커가 리스너를 실행할 때 예외가 발생하지 않으면, 큐에 저장된 작업은 정상적으로 처리된 뒤 자동으로 삭제됩니다.

<a name="customizing-the-queue-connection-queue-name"></a>
#### 큐 연결, 큐 이름 및 지연 시간 커스터마이징

리스너가 사용할 큐 연결명, 큐 이름, 지연 시간 등을 커스터마이징하고 싶을 때는, 리스너 클래스에 `$connection`, `$queue`, `$delay` 속성을 설정할 수 있습니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    /**
     * 이 작업이 전송되어야 할 큐 연결 이름
     *
     * @var string|null
     */
    public $connection = 'sqs';

    /**
     * 이 작업이 전송되어야 할 큐 이름
     *
     * @var string|null
     */
    public $queue = 'listeners';

    /**
     * 작업 실행까지 대기할 시간(초)
     *
     * @var int
     */
    public $delay = 60;
}
```

런타임에 리스너의 큐 연결, 큐 이름, 지연 시간을 정의하고 싶다면, 리스너 클래스에 `viaConnection`, `viaQueue`, `withDelay` 메서드를 구현할 수 있습니다:

```php
/**
 * 리스너가 사용할 큐 연결 이름 반환
 */
public function viaConnection(): string
{
    return 'sqs';
}

/**
 * 리스너가 사용할 큐 이름 반환
 */
public function viaQueue(): string
{
    return 'listeners';
}

/**
 * 작업 실행까지 대기할 시간(초) 반환
 */
public function withDelay(OrderShipped $event): int
{
    return $event->highPriority ? 0 : 60;
}
```

<a name="conditionally-queueing-listeners"></a>
#### 조건부로 큐에 저장되는 리스너

때로는, 런타임에 특정 데이터에 따라 리스너를 큐에 저장할지 판단해야 할 필요가 있습니다. 이를 위해 리스너에 `shouldQueue` 메서드를 추가할 수 있으며, 이 메서드가 `false`를 반환하면 해당 리스너는 큐에 저장되지 않습니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderCreated;
use Illuminate\Contracts\Queue\ShouldQueue;

class RewardGiftCard implements ShouldQueue
{
    /**
     * 고객에게 기프트카드 제공
     */
    public function handle(OrderCreated $event): void
    {
        // ...
    }

    /**
     * 리스너를 큐에 저장할지 여부 반환
     */
    public function shouldQueue(OrderCreated $event): bool
    {
        return $event->order->subtotal >= 5000;
    }
}
```

<a name="manually-interacting-with-the-queue"></a>
### 큐 직접 제어하기

리스너가 실제로 큐 작업의 `delete` 또는 `release` 메서드를 직접 호출해야 할 경우, `Illuminate\Queue\InteractsWithQueue` 트레이트를 사용할 수 있습니다. 이 트레이트는 Artisan으로 생성한 리스너에 기본적으로 import되어 있으며, 관련 메서드에 바로 접근할 수 있게 해줍니다:

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
### 큐 리스너와 데이터베이스 트랜잭션

큐 리스너가 데이터베이스 트랜잭션 내부에서 디스패치될 경우, 해당 트랜잭션이 커밋되기 전에 큐 워커가 리스너를 처리할 수 있습니다. 이때, 트랜잭션 내에서 수정된 모델이나 레코드가 아직 데이터베이스에 반영되지 않았을 수 있으며, 트랜잭션 내에서 새로 생성된 모델이나 레코드가 아직 DB에 없을 수도 있습니다. 만약 리스너가 이런 모델에 의존한다면, 작업 처리 시 예기치 않은 오류가 발생할 수 있습니다.

만약 큐 연결의 `after_commit` 설정 값이 `false`여도, 특정 큐 리스너는 모든 오픈된 데이터베이스 트랜잭션이 커밋된 후에 보내지도록 하고 싶다면, 리스너 클래스에 `ShouldQueueAfterCommit` 인터페이스를 구현하면 됩니다:

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
> 이러한 문제를 더 자세히 다루는 방법은 [큐 작업과 데이터베이스 트랜잭션](/docs/12.x/queues#jobs-and-database-transactions) 문서를 참고하십시오.

<a name="queued-listener-middleware"></a>
### 큐 리스너용 미들웨어

큐 리스너 역시 [작업 미들웨어](/docs/12.x/queues#job-middleware)를 이용할 수 있습니다. 작업 미들웨어는 큐 리스너 실행 전후로 커스텀 로직을 감싸서, 리스너 내부의 반복 코드를 줄이는 데 효과적입니다. 미들웨어를 만든 뒤에는 리스너의 `middleware` 메서드에서 반환해 연결할 수 있습니다:

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
        // 이벤트 처리...
    }

    /**
     * 리스너가 통과할(적용할) 미들웨어 반환
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

Laravel은 큐 리스너의 데이터 보안 및 무결성을 [암호화](/docs/12.x/encryption)를 통해 보장할 수 있습니다. 이를 위해 리스너 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하면 됩니다. 이 인터페이스를 클래스로 추가하면, Laravel은 해당 리스너를 큐에 넣기 전에 자동으로 암호화합니다:

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

간혹 큐에 저장된 이벤트 리스너의 실행이 실패할 수 있습니다. 큐 리스너가 큐 워커에서 지정한 최대 재시도 횟수를 초과하면, 리스너의 `failed` 메서드가 호출됩니다. 이 `failed` 메서드는 이벤트 인스턴스와 실패 원인인 `Throwable` 객체를 전달받습니다:

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
     * 작업 실패 처리
     */
    public function failed(OrderShipped $event, Throwable $exception): void
    {
        // ...
    }
}
```

<a name="specifying-queued-listener-maximum-attempts"></a>
#### 큐 리스너의 최대 재시도 횟수 지정

큐 리스너에서 오류가 반복적으로 발생할 경우, 무한정 재시도하는 것을 방지하고 싶을 수 있습니다. Laravel은 리스너가 몇 번까지 또는 얼마나 오랫동안 시도될지 선택할 수 있도록 다양한 방법을 제공합니다.

리스너 클래스에 `$tries` 속성을 지정하여, 해당 리스너가 실패로 간주되기 전에 시도할 수 있는 최대 횟수를 설정할 수 있습니다:

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
     * 큐 리스너의 최대 실행(시도) 횟수
     *
     * @var int
     */
    public $tries = 5;
}
```

얼마나 시도할 수 있을지 횟수 대신, 리스너가 특정 시간 이후에는 더 이상 실행되지 않도록 제한할 수도 있습니다. 이럴 때는 리스너 클래스에 `retryUntil` 메서드를 추가하면 됩니다. 이 메서드는 `DateTime` 인스턴스를 반환해야 합니다:

```php
use DateTime;

/**
 * 리스너 실행이 중단되어야 할 시점 반환
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(5);
}
```

`retryUntil`과 `tries`가 모두 정의되어 있다면, Laravel은 `retryUntil` 메서드 설정을 우선 적용합니다.

<a name="specifying-queued-listener-backoff"></a>
#### 큐 리스너의 재시도 대기(backoff) 설정

큐에 저장된 리스너가 예외를 만나 재시도할 때, Laravel이 몇 초 동안 대기한 후 다시 시도할지 지정하고 싶다면, 리스너 클래스에 `backoff` 속성을 추가하면 됩니다:

```php
/**
 * 큐 리스너가 재시도 전 대기할 시간(초)
 *
 * @var int
 */
public $backoff = 3;
```

좀 더 복잡한 backoff 규칙이 필요하다면, 리스너 클래스에 `backoff` 메서드를 정의할 수 있습니다:

```php
/**
 * 큐 리스너가 재시도 전 대기할 시간(초) 반환
 */
public function backoff(OrderShipped $event): int
{
    return 3;
}
```

"지수(backoff) 증가" 형태로 지연 시간을 늘리고 싶다면, `backoff` 메서드에서 배열로 값을 반환할 수 있습니다. 예를 들어, 첫 번째 재시도는 1초, 두 번째는 5초, 세 번째 이후부터는 10초씩 대기하도록 설정할 수 있습니다:

```php
/**
 * 큐 리스너가 재시도 전 대기할 시간(초) 배열 반환
 *
 * @return list<int>
 */
public function backoff(OrderShipped $event): array
{
    return [1, 5, 10];
}
```

<a name="specifying-queued-listener-max-exceptions"></a>
#### 큐 리스너의 최대 허용 예외 횟수 지정

큐 리스너를 여러 번 시도하게 하면서도, 해제(release)가 아닌 예기치 않은 예외가 일정 횟수 이상 발생하면 즉시 실패하도록 만들고 싶을 때가 있습니다. 이때는 리스너 클래스에 `maxExceptions` 속성을 추가하면 됩니다:

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
     * 큐 리스너의 최대 실행(시도) 횟수
     *
     * @var int
     */
    public $tries = 25;

    /**
     * 실패로 간주할 최대 미처리 예외 발생 허용 횟수
     *
     * @var int
     */
    public $maxExceptions = 3;

    /**
     * Handle the event.
     */
    public function handle(OrderShipped $event): void
    {
        // 이벤트 처리...
    }
}
```

위 예시에서 이 리스너는 최대 25번까지 시도할 수 있지만, 미처리 예외가 3번 발생하면 즉시 실패로 처리됩니다.

<a name="specifying-queued-listener-timeout"></a>
#### 큐 리스너 타임아웃 설정

종종, 큐에 저장된 리스너가 대략 어느 정도 시간 안에 실행 완료될지 예측할 수 있습니다. 이런 경우, Laravel에서는 "타임아웃" 값을 지정할 수 있습니다. 리스너가 지정한 초보다 오래 실행될 경우, 해당 작업을 담당하는 워커는 오류와 함께 종료됩니다. 허용할 최대 실행 시간(초)는 리스너 클래스에 `$timeout` 속성을 지정해 줄 수 있습니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    /**
     * 리스너가 실행 가능한 최대 시간(초)
     *
     * @var int
     */
    public $timeout = 120;
}
```

리스너가 타임아웃 시 실패 처리로 간주되길 원한다면, 리스너 클래스에 `$failOnTimeout` 속성을 지정할 수 있습니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    /**
     * 타임아웃 발생 시 실패 처리 여부
     *
     * @var bool
     */
    public $failOnTimeout = true;
}
```

<a name="dispatching-events"></a>

## 이벤트 디스패치(Dispatching Events)

이벤트를 디스패치(발생시키는 것)하려면, 해당 이벤트의 정적 `dispatch` 메서드를 호출하면 됩니다. 이 메서드는 이벤트 클래스에 `Illuminate\Foundation\Events\Dispatchable` 트레이트가 적용되어 있을 때 사용할 수 있습니다. `dispatch` 메서드에 전달하는 모든 인수는 이벤트의 생성자(constructor)로 그대로 전달됩니다.

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
> 테스트할 때 실제로 리스너가 실행되지 않으면서 특정 이벤트가 디스패치됐는지 쉽게 검증하고 싶다면, 라라벨의 [내장 테스트 헬퍼](#testing)를 활용하면 매우 간편하게 처리할 수 있습니다.

<a name="dispatching-events-after-database-transactions"></a>
### 데이터베이스 트랜잭션 이후에 이벤트 디스패치하기

특정 상황에서는 현재 진행 중인 데이터베이스 트랜잭션이 **커밋된 이후에만** 이벤트를 디스패치하도록 라라벨에게 지시하고 싶을 수 있습니다. 이럴 때는 이벤트 클래스에서 `ShouldDispatchAfterCommit` 인터페이스를 구현하면 됩니다.

이 인터페이스를 구현하면, 현재의 데이터베이스 트랜잭션이 커밋될 때까지 이벤트 디스패치가 보류됩니다. 만약 트랜잭션이 실패하면 이벤트는 폐기됩니다. 이벤트가 디스패치될 때 트랜잭션이 진행 중이지 않다면, 이벤트는 즉시 디스패치됩니다.

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
## 이벤트 구독자(Event Subscribers)

<a name="writing-event-subscribers"></a>
### 이벤트 구독자 작성하기

이벤트 구독자는 여러 이벤트를 하나의 구독자 클래스 내부에서 구독할 수 있는 클래스입니다. 즉, 한 클래스 내에 여러 이벤트 핸들러를 정의할 수 있습니다. 구독자 클래스에는 반드시 `subscribe` 메서드를 정의해야 하며, 이 메서드는 이벤트 디스패처 인스턴스를 인자로 받습니다. 인자로 받은 디스패처에서 `listen` 메서드를 호출해 이벤트 리스너를 등록할 수 있습니다.

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

구독자 내부에 이벤트 리스너 메서드가 정의되어 있다면, `subscribe` 메서드에서 이벤트와 메서드명을 배열로 반환하는 방식이 더 편리할 수 있습니다. 이 경우, 라라벨이 자동으로 구독자 클래스명을 파악하여 이벤트 리스너를 등록합니다.

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

구독자를 작성한 후, 만약 구독자 내부의 핸들러 메서드가 라라벨의 [이벤트 자동 발견 규칙](#event-discovery)을 따르고 있다면, 라라벨이 자동으로 구독자 메서드를 등록해줍니다. 만약 자동 발견이 아닌 경우, 구독자는 `Event` 파사드의 `subscribe` 메서드를 이용해 직접 등록할 수 있습니다. 보통 이 과정은 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 처리합니다.

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

이벤트를 디스패치하는 코드를 테스트할 때는, 이벤트의 리스너가 실제로 실행되지 않도록 하고 싶을 수 있습니다. 이런 경우 리스너의 코드는 별도의 테스트에서 직접 검증할 수 있으니, 이벤트 디스패치 여부만을 독립적으로 확인할 수 있기 때문입니다. 리스너 자체를 테스트하려면, 테스트에서 직접 리스너 인스턴스를 생성하고 `handle` 메서드를 호출하면 됩니다.

`Event` 파사드의 `fake` 메서드를 사용하면, 리스너 실행을 차단하고 테스트 대상 코드를 실행한 뒤, `assertDispatched`, `assertNotDispatched`, `assertNothingDispatched` 메서드로 어느 이벤트가 디스패치되었는지 검증할 수 있습니다:

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

`assertDispatched` 또는 `assertNotDispatched` 메서드에는 클로저를 전달하여 주어진 "조건"을 만족하는 이벤트가 실제로 디스패치되었는지 세밀하게 검증할 수 있습니다. 클로저의 조건을 통과하는 이벤트가 하나라도 있으면 검증에 성공합니다.

```php
Event::assertDispatched(function (OrderShipped $event) use ($order) {
    return $event->order->id === $order->id;
});
```

특정 이벤트에 대해 특정 리스너가 실제로 등록되어 있는지만 검증하고자 한다면, `assertListening` 메서드를 사용할 수 있습니다.

```php
Event::assertListening(
    OrderShipped::class,
    SendShipmentNotification::class
);
```

> [!WARNING]
> `Event::fake()`을 호출하면 이후에는 **모든 이벤트 리스너가 실행되지 않습니다**. 만약 테스트 과정에서 이벤트에 의존하는 팩토리(예: 모델 `creating` 이벤트에서 UUID를 생성하는 경우)를 사용한다면, 반드시 팩토리 사용 **이후에** `Event::fake()`를 호출해야 합니다.

<a name="faking-a-subset-of-events"></a>
### 일부 이벤트만 페이크(Fake) 처리하기

특정 이벤트에 대해서만 리스너를 페이크로 처리하고자 한다면, `fake` 또는 `fakeFor` 메서드에 원하는 이벤트들만 배열 형태로 지정할 수 있습니다.

```php tab=Pest
test('orders can be processed', function () {
    Event::fake([
        OrderCreated::class,
    ]);

    $order = Order::factory()->create();

    Event::assertDispatched(OrderCreated::class);

    // 나머지 이벤트는 정상적으로 디스패치됩니다...
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

    // 나머지 이벤트는 정상적으로 디스패치됩니다...
    $order->update([
        // ...
    ]);
}
```

`except` 메서드를 사용하면 지정한 이벤트 **이외의 모든 이벤트**를 페이크 처리할 수도 있습니다.

```php
Event::fake()->except([
    OrderCreated::class,
]);
```

<a name="scoped-event-fakes"></a>
### 범위를 지정하여 이벤트 페이크 적용하기

테스트 특정 구간(일부 코드 블록)에서만 이벤트 리스너를 페이크 처리하고 싶다면, `fakeFor` 메서드를 사용할 수 있습니다.

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

    // 이제부터는 이벤트가 정상적으로 디스패치되고 옵저버도 실행됩니다...
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

        // 이제부터는 이벤트가 정상적으로 디스패치되고 옵저버도 실행됩니다...
        $order->update([
            // ...
        ]);
    }
}
```