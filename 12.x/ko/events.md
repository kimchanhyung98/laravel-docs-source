# 이벤트 (Events)

- [소개](#introduction)
- [이벤트 및 리스너 생성](#generating-events-and-listeners)
- [이벤트 및 리스너 등록](#registering-events-and-listeners)
    - [이벤트 자동 탐지](#event-discovery)
    - [이벤트 수동 등록](#manually-registering-events)
    - [클로저 리스너](#closure-listeners)
- [이벤트 정의](#defining-events)
- [리스너 정의](#defining-listeners)
- [큐를 사용하는 이벤트 리스너](#queued-event-listeners)
    - [큐 직접 다루기](#manually-interacting-with-the-queue)
    - [큐 리스너와 데이터베이스 트랜잭션](#queued-event-listeners-and-database-transactions)
    - [큐 리스너 미들웨어](#queued-listener-middleware)
    - [암호화된 큐 리스너](#encrypted-queued-listeners)
    - [실패한 작업 처리](#handling-failed-jobs)
- [이벤트 디스패치](#dispatching-events)
    - [데이터베이스 트랜잭션 이후의 이벤트 디스패치](#dispatching-events-after-database-transactions)
    - [이벤트 연기(Defer)](#deferring-events)
- [이벤트 구독자](#event-subscribers)
    - [이벤트 구독자 작성](#writing-event-subscribers)
    - [이벤트 구독자 등록](#registering-event-subscribers)
- [테스트](#testing)
    - [특정 이벤트만 가짜로 처리](#faking-a-subset-of-events)
    - [스코프 이벤트 가짜 처리](#scoped-event-fakes)

<a name="introduction"></a>
## 소개

Laravel의 이벤트는 간단한 옵저버 패턴을 제공합니다. 이를 통해 애플리케이션에서 발생하는 다양한 이벤트를 구독하고 감지할 수 있습니다. 이벤트 클래스는 보통 `app/Events` 디렉터리에 저장되며, 해당 이벤트를 처리하는 리스너는 `app/Listeners` 디렉터리에 저장됩니다. 만약 애플리케이션에 이 디렉터리가 없다면 Artisan 콘솔 명령어를 통해 이벤트와 리스너를 생성할 때 자동으로 만들어집니다.

이벤트는 애플리케이션의 여러 기능을 느슨하게 결합할 수 있는 훌륭한 방법입니다. 하나의 이벤트에 여러 리스너가 연결될 수 있으며, 각 리스너는 서로에게 의존하지 않습니다. 예를 들어, 주문이 발송될 때마다 사용자에게 Slack 알림을 보내고 싶다고 가정합시다. 이럴 때 주문 처리 코드와 Slack 알림 코드를 직접 연결하지 않고 `App\Events\OrderShipped` 이벤트를 발생시키고, 이 이벤트를 감지하여 Slack 알림을 보내는 리스너를 구현할 수 있습니다.

<a name="generating-events-and-listeners"></a>
## 이벤트 및 리스너 생성

이벤트와 리스너를 빠르게 생성하려면 `make:event` 및 `make:listener` Artisan 명령어를 사용할 수 있습니다:

```shell
php artisan make:event PodcastProcessed

php artisan make:listener SendPodcastNotification --event=PodcastProcessed
```

또한, 인수를 추가하지 않고 `make:event` 및 `make:listener` Artisan 명령어를 실행하면, Laravel이 클래스명을 입력하라는 프롬프트를 표시하며, 리스너를 생성할 때는 어떤 이벤트를 감지할지 추가로 질문합니다:

```shell
php artisan make:event

php artisan make:listener
```

<a name="registering-events-and-listeners"></a>
## 이벤트 및 리스너 등록

<a name="event-discovery"></a>
### 이벤트 자동 탐지

기본적으로 Laravel은 애플리케이션의 `Listeners` 디렉터리를 스캔하여 이벤트 리스너를 자동으로 찾고 등록합니다. 리스너 클래스 내에 `handle` 또는 `__invoke`로 시작하는 메서드를 발견하면, 해당 메서드에 타입힌트된 이벤트를 자동으로 리스너로 등록합니다:

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

PHP의 유니언 타입(union type)를 사용하면 여러 이벤트를 동시에 감지할 수도 있습니다:

```php
/**
 * Handle the event.
 */
public function handle(PodcastProcessed|PodcastPublished $event): void
{
    // ...
}
```

리스너를 여러 디렉터리나 다른 위치에 저장하고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에서 `withEvents` 메서드를 사용하여 Laravel이 해당 디렉터리를 스캔하도록 지정할 수 있습니다:

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/Orders/Listeners',
])
```

`*` 와일드카드 문자를 사용하면 여러 비슷한 디렉터리를 한 번에 스캔할 수 있습니다:

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/*/Listeners',
])
```

`event:list` 명령어를 사용하면 애플리케이션에 등록된 모든 리스너를 확인할 수 있습니다:

```shell
php artisan event:list
```

<a name="event-discovery-in-production"></a>
#### 프로덕션 환경에서의 이벤트 자동 탐지

애플리케이션의 성능을 높이기 위해 `optimize` 또는 `event:cache` Artisan 명령어로 리스너 목록을 캐싱해야 합니다. 일반적으로 이 명령은 [배포 과정](/docs/12.x/deployment#optimization)의 일부로 실행합니다. 이 매니페스트 파일을 프레임워크가 사용하여 이벤트 등록 속도를 높입니다. 이벤트 캐시를 삭제하려면 `event:clear` 명령어를 사용할 수 있습니다.

<a name="manually-registering-events"></a>
### 이벤트 수동 등록

`Event` 파사드를 사용하여 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 이벤트와 해당 리스너를 직접 등록할 수 있습니다:

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
### 클로저 리스너

일반적으로 리스너는 클래스로 정의하지만, 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 클로저(익명 함수)로 이벤트 리스너를 직접 등록할 수도 있습니다:

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
#### 큐를 지원하는 익명 이벤트 리스너

클로저 기반의 이벤트 리스너를 등록할 때, `Illuminate\Events\queueable` 함수를 사용하여 리스너를 [큐](/docs/12.x/queues)로 실행하도록 지정할 수 있습니다:

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

큐 작업과 마찬가지로 `onConnection`, `onQueue`, `delay` 메서드를 활용하여 큐 리스너의 실행 방식을 세부적으로 제어할 수 있습니다:

```php
Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->onConnection('redis')->onQueue('podcasts')->delay(now()->addSeconds(10)));
```

익명 큐 리스너에서 실패 상황을 처리하려면, `queueable` 리스너를 정의할 때 `catch` 메서드에 클로저를 전달하세요. 이 클로저는 이벤트 인스턴스와 해당 리스너의 실패를 일으킨 `Throwable` 인스턴스를 인자로 받습니다:

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

`*` 문자를 와일드카드 파라미터로 사용하여 여러 이벤트를 한 리스너에서 감지할 수도 있습니다. 와일드카드 리스너는 첫 번째 인수로 이벤트 이름을, 두 번째 인수로 전체 이벤트 데이터 배열을 받습니다:

```php
Event::listen('event.*', function (string $eventName, array $data) {
    // ...
});
```

<a name="defining-events"></a>
## 이벤트 정의

이벤트 클래스는 단순히 해당 이벤트와 관련된 데이터를 담는 데이터 컨테이너입니다. 예를 들어, `App\Events\OrderShipped` 이벤트가 [Eloquent ORM](/docs/12.x/eloquent) 객체를 받는다고 가정해 봅니다:

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

위와 같이, 이 이벤트 클래스는 별도의 로직이 없으며, 구매된 `App\Models\Order` 인스턴스를 담는 역할만 합니다. 이벤트에 사용된 `SerializesModels` 트레이트는 PHP의 `serialize` 함수로 이벤트 객체를 직렬화할 때 Eloquent 모델을 안전하게 직렬화해줍니다. 이는 [큐 리스너](#queued-event-listeners) 사용 시에 유용합니다.

<a name="defining-listeners"></a>
## 리스너 정의

예시 이벤트를 처리할 리스너를 살펴보겠습니다. 이벤트 리스너는 `handle` 메서드에서 이벤트 인스턴스를 전달받습니다. `make:listener` Artisan 명령을 사용할 때 `--event` 옵션을 지정하면, 올바른 이벤트 클래스를 자동으로 import하고, `handle` 메서드에 타입힌트를 추가해줍니다. `handle` 메서드에서는 이벤트에 응답하기 위한 필요한 작업을 수행할 수 있습니다:

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
        // $event->order를 사용하여 주문 정보를 접근할 수 있습니다...
    }
}
```

> [!NOTE]
> 리스너 클래스의 생성자에서 필요한 의존성을 타입힌트로 선언하면, Laravel [서비스 컨테이너](/docs/12.x/container)를 통해 자동으로 의존성이 주입됩니다.

<a name="stopping-the-propagation-of-an-event"></a>
#### 이벤트 전달 중단

때때로 이벤트가 추가 리스너로 전달되는 것을 막고 싶을 수도 있습니다. 이 경우, 리스너의 `handle` 메서드에서 `false`를 반환하면 이벤트가 더 이상 다른 리스너로 전달되지 않습니다.

<a name="queued-event-listeners"></a>
## 큐를 사용하는 이벤트 리스너

이메일 전송이나 HTTP 요청과 같이 느린 작업을 처리해야 하는 리스너는 큐에 넣는 것이 좋습니다. 큐 리스너를 사용하기 전에 [큐 설정](/docs/12.x/queues)과 서버 또는 로컬 개발 환경에서 큐 워커를 실행하시기 바랍니다.

리스너를 큐에 넣으려면, 리스너 클래스에 `ShouldQueue` 인터페이스를 추가하세요. `make:listener` Artisan 명령어로 생성된 리스너는 이미 이 인터페이스가 네임스페이스에 import되어 있으므로 바로 사용할 수 있습니다:

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

이제 해당 리스너가 처리하는 이벤트가 발생하면, Laravel의 [큐 시스템](/docs/12.x/queues)이 자동으로 리스너를 큐에 추가하고, 큐에서 처리됩니다. 리스너가 예외 없이 실행되면, 작업 완료 후 큐 작업은 자동으로 삭제됩니다.

<a name="customizing-the-queue-connection-queue-name"></a>
#### 큐 연결, 큐 이름, 지연 시간 설정

이벤트 리스너의 큐 연결, 큐 이름, 큐 지연 시간을 커스터마이징하고 싶다면 리스너 클래스에 `$connection`, `$queue`, `$delay` 속성을 정의하세요:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    /**
     * 작업이 전송되어야 하는 연결 이름
     *
     * @var string|null
     */
    public $connection = 'sqs';

    /**
     * 작업이 전송되어야 하는 큐 이름
     *
     * @var string|null
     */
    public $queue = 'listeners';

    /**
     * 작업이 처리되기 전까지 대기할 시간(초)
     *
     * @var int
     */
    public $delay = 60;
}
```

런타임에 큐 연결, 큐 이름, 지연 시간을 동적으로 지정하려면 `viaConnection`, `viaQueue`, `withDelay` 메서드를 정의할 수 있습니다:

```php
/**
 * 리스너의 큐 연결 이름 반환
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
 * 작업 처리 전까지 대기할 시간(초) 반환
 */
public function withDelay(OrderShipped $event): int
{
    return $event->highPriority ? 0 : 60;
}
```

<a name="conditionally-queueing-listeners"></a>
#### 리스너 큐 작업 조건부 처리

러닝타임에서의 데이터에 따라 리스너를 큐에 넣을지 판단해야 할 때가 있습니다. 이럴 때, 리스너에 `shouldQueue` 메서드를 추가하여 큐 대기 여부를 결정할 수 있습니다. `shouldQueue`가 `false`를 반환하면 리스너가 큐에 등록되지 않습니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderCreated;
use Illuminate\Contracts\Queue\ShouldQueue;

class RewardGiftCard implements ShouldQueue
{
    /**
     * 고객에게 기프트 카드를 지급
     */
    public function handle(OrderCreated $event): void
    {
        // ...
    }

    /**
     * 리스너가 큐에 등록될지 여부를 판단
     */
    public function shouldQueue(OrderCreated $event): bool
    {
        return $event->order->subtotal >= 5000;
    }
}
```

<a name="manually-interacting-with-the-queue"></a>
### 큐 직접 다루기

리스너의 기본 큐 작업에서 `delete` 및 `release` 메서드를 직접 호출하려면 `Illuminate\Queue\InteractsWithQueue` 트레이트를 사용할 수 있습니다. 이 트레이트는 리스너 생성 시 기본으로 import되어 있으며 큐 작업의 제어 기능을 제공합니다:

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

큐 리스너가 데이터베이스 트랜잭션 내에서 디스패치될 때, 경우에 따라 트랜잭션이 커밋되기 전에 큐에서 작업이 실행될 수도 있습니다. 이럴 경우, 트랜잭션 중 변경된 모델 데이터 또는 레코드가 아직 데이터베이스에 반영되지 않아 리스너 내에서 예기치 않은 에러가 발생할 수 있습니다.

큐 연결의 `after_commit` 설정이 `false`여도, 특정 큐 리스너에서 트랜잭션이 모두 커밋된 후에만 작업이 실행되게 하려면 리스너 클래스에 `ShouldQueueAfterCommit` 인터페이스를 구현하세요:

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
> 이와 관련된 추가 정보는 [큐 작업과 데이터베이스 트랜잭션](/docs/12.x/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="queued-listener-middleware"></a>
### 큐 리스너 미들웨어

큐로 처리되는 리스너 역시 [잡 미들웨어](/docs/12.x/queues#job-middleware)를 사용할 수 있습니다. 잡 미들웨어는 큐 리스너의 실행 과정을 커스텀 로직으로 감싸 반복 코드를 줄여줍니다. 잡 미들웨어 작성 후, 리스너의 `middleware` 메서드에서 반환하여 미들웨어를 리스너에 연결하세요:

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
     * 리스너가 통과해야 할 미들웨어 반환
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

Laravel은 [암호화](/docs/12.x/encryption)를 통해 큐 리스너 데이터의 기밀성과 무결성을 보장할 수 있습니다. 시작하려면 리스너 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하세요. 이 인터페이스가 추가되면, Laravel은 해당 리스너를 큐에 넣기 전에 자동으로 암호화합니다:

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

큐로 처리되는 이벤트 리스너가 실패하는 경우가 있습니다. 이 때, 큐 리스너가 설정한 최대 시도 횟수를 초과하면, 리스너의 `failed` 메서드가 호출됩니다. 이 메서드는 이벤트 인스턴스와 실패를 유발한 `Throwable`을 인자로 받습니다:

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
     * 작업 실패 처리 로직
     */
    public function failed(OrderShipped $event, Throwable $exception): void
    {
        // ...
    }
}
```

<a name="specifying-queued-listener-maximum-attempts"></a>
#### 큐 리스너 최대 시도 횟수 지정

큐 리스너에서 에러가 발생할 경우 무한 반복으로 계속 재시도를 하지 않도록, 리스너의 시도 가능 횟수(최대 시도 횟수)를 여러 방법으로 지정할 수 있습니다.

리스너 클래스에 `tries` 속성이나 메서드를 정의하여, 실패로 간주되기 전까지 시도할 최대 횟수를 지정할 수 있습니다:

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

실패 전에 몇 번 시도하는지를 지정하는 대신, 리스너가 더 이상 시도되지 않을 시각을 지정할 수도 있습니다. 이는 주어진 시간 내에 얼마나 많은 재시도가 있어도 무방하게 만듭니다. 이를 위해 리스너 클래스에 `retryUntil` 메서드를 추가하세요. 이 메서드는 `DateTime` 인스턴스를 반환해야 합니다:

```php
use DateTime;

/**
 * 리스너가 타임아웃될 시각 지정
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(5);
}
```

`retryUntil`과 `tries` 모두 정의되어 있다면, Laravel은 `retryUntil` 메서드를 우선적으로 적용합니다.

<a name="specifying-queued-listener-backoff"></a>
#### 큐 리스너 백오프(대기) 시간 지정

예외가 발생해 리스너를 다시 시도할 때 Laravel이 기다릴 시간을 지정하려면 리스너 클래스에 `backoff` 속성을 추가하세요:

```php
/**
 * 큐 리스너 재시도 전 대기할 시간(초)
 *
 * @var int
 */
public $backoff = 3;
```

더 복잡한 로직으로 백오프 시간을 계산하려면 `backoff` 메서드를 정의할 수 있습니다:

```php
/**
 * 큐 리스너 재시도 전 대기할 시간(초) 계산
 */
public function backoff(OrderShipped $event): int
{
    return 3;
}
```

"지수 백오프(exponential backoff)" 방식을 쉽게 구성하려면, `backoff` 메서드에서 배열로 값을 반환하세요. 아래 예시는 첫 번째 재시도는 1초, 두 번째는 5초, 세 번째는 10초, 이후 모든 재시도는 10초 대기합니다:

```php
/**
 * 큐 리스너 재시도 전 대기할 시간(초) 계산
 *
 * @return list<int>
 */
public function backoff(OrderShipped $event): array
{
    return [1, 5, 10];
}
```

<a name="specifying-queued-listener-max-exceptions"></a>
#### 큐 리스너 최대 예외 횟수 설정

경우에 따라, 리스너가 여러 번 재시도는 되지만 미처리 예외가 정해진 횟수만큼 연속 발생하면 곧바로 실패 처리하고 싶을 수 있습니다. 이럴 때, 리스너 클래스에 `maxExceptions` 속성을 지정하세요:

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
     * 실패 처리 전 허용되는 최대 미처리 예외 개수
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

이 예제에서는 리스너가 최대 25회까지 재시도될 수 있지만, 3회 미처리 예외가 발생하면 즉시 실패 처리됩니다.

<a name="specifying-queued-listener-timeout"></a>
#### 큐 리스너 타임아웃 지정

통상 큐 리스너가 얼마나 걸릴지 예상할 수 있다면, 타임아웃(timeout) 값을 지정할 수 있습니다. 리스너가 설정된 시간을 초과하여 실행되면, 워커가 에러와 함께 해당 작업을 종료합니다. 리스너 클래스에 `timeout` 속성을 지정하여 최대 실행 가능 시간을 정의하세요:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    /**
     * 타임아웃(초)까지 리스너 실행 허용
     *
     * @var int
     */
    public $timeout = 120;
}
```

타임아웃 이후에 리스너가 실패한 것으로 간주되게 하려면, 리스너 클래스에 `failOnTimeout` 속성을 정의하세요:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    /**
     * 타임아웃 시에 리스너 실패 처리 여부
     *
     * @var bool
     */
    public $failOnTimeout = true;
}
```

<a name="dispatching-events"></a>
## 이벤트 디스패치

이벤트를 발생시키려면, 이벤트 클래스의 정적 `dispatch` 메서드를 호출하면 됩니다. 이 메서드는 `Illuminate\Foundation\Events\Dispatchable` 트레이트에 의해 제공됩니다. `dispatch` 메서드에 전달된 인수는 이벤트 생성자에 전달됩니다:

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

        // 주문 발송 로직...

        OrderShipped::dispatch($order);

        return redirect('/orders');
    }
}
```

이벤트를 조건부로 디스패치하고 싶다면 `dispatchIf` 및 `dispatchUnless` 메서드를 사용할 수 있습니다:

```php
OrderShipped::dispatchIf($condition, $order);

OrderShipped::dispatchUnless($condition, $order);
```

> [!NOTE]
> 테스트를 할 때, 실제로 리스너가 동작하지 않아도 이벤트가 발생되었는지 쉽게 검증할 수 있습니다. Laravel의 [테스트 도구](#testing)를 활용해 보세요.

<a name="dispatching-events-after-database-transactions"></a>
### 데이터베이스 트랜잭션 이후의 이벤트 디스패치

경우에 따라 데이터베이스 트랜잭션이 커밋된 후에만 이벤트가 디스패치되도록 하고 싶을 수 있습니다. 이럴 때 이벤트 클래스에 `ShouldDispatchAfterCommit` 인터페이스를 구현하면 됩니다.

이 인터페이스가 구현된 이벤트는 트랜잭션 커밋 전까지 디스패치되지 않고, 트랜잭션이 실패하면 이벤트도 폐기됩니다. 만약 이벤트가 발생할 때 트랜잭션 중이 아니라면 즉시 디스패치됩니다:

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
### 이벤트 연기(Defer)

이벤트 연기 기능을 사용하면 특정 코드 블록 내에서 발생하는 모델 이벤트와 이벤트 리스너의 실행을 블록 종료 이후로 미룰 수 있습니다. 이는 관련 레코드가 모두 생성된 후에 이벤트 리스너가 동작해야 할 때 유용합니다.

이벤트를 연기하려면 `Event::defer()` 메서드에 클로저를 전달하세요:

```php
use App\Models\User;
use Illuminate\Support\Facades\Event;

Event::defer(function () {
    $user = User::create(['name' => 'Victoria Otwell']);

    $user->posts()->create(['title' => 'My first post!']);
});
```

클로저 내부에서 발생한 모든 이벤트는 클로저 실행 이후에 디스패치됩니다. 이는 이벤트 리스너가 연관된 모든 레코드에 접근할 수 있도록 보장합니다. 클로저에서 예외가 발생하면, 연기된 이벤트는 디스패치되지 않습니다.

특정 이벤트만 연기하고 싶다면 두 번째 인수로 이벤트 배열을 전달하세요:

```php
use App\Models\User;
use Illuminate\Support\Facades\Event;

Event::defer(function () {
    $user = User::create(['name' => 'Victoria Otwell']);

    $user->posts()->create(['title' => 'My first post!']);
}, ['eloquent.created: '.User::class]);
```

<a name="event-subscribers"></a>
## 이벤트 구독자

<a name="writing-event-subscribers"></a>
### 이벤트 구독자 작성

이벤트 구독자는 하나의 클래스에서 여러 이벤트를 구독할 수 있는 클래스입니다. 이를 통해 여러 이벤트 핸들러를 한 클래스 내부에 정의할 수 있습니다. 구독자 클래스에는 반드시 `subscribe` 메서드를 정의해야 하며, 이 메서드는 이벤트 디스패처 인스턴스를 전달받습니다. 제공된 디스패처를 활용해 리스너를 등록할 수 있습니다:

```php
<?php

namespace App\Listeners;

use Illuminate\Auth\Events\Login;
use Illuminate\Auth\Events\Logout;
use Illuminate\Events\Dispatcher;

class UserEventSubscriber
{
    /**
     * 사용자 로그인 이벤트 처리
     */
    public function handleUserLogin(Login $event): void {}

    /**
     * 사용자 로그아웃 이벤트 처리
     */
    public function handleUserLogout(Logout $event): void {}

    /**
     * 구독자에 대한 리스너 등록
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

구독자에 이벤트 리스너 메서드가 정의되어 있다면, `subscribe` 메서드에서 메서드 이름과 이벤트를 배열 형태로 반환하는 것이 편리할 수 있습니다. Laravel은 이벤트를 등록할 때 구독자의 클래스명을 자동으로 결정합니다:

```php
<?php

namespace App\Listeners;

use Illuminate\Auth\Events\Login;
use Illuminate\Auth\Events\Logout;
use Illuminate\Events\Dispatcher;

class UserEventSubscriber
{
    /**
     * 사용자 로그인 이벤트 처리
     */
    public function handleUserLogin(Login $event): void {}

    /**
     * 사용자 로그아웃 이벤트 처리
     */
    public function handleUserLogout(Logout $event): void {}

    /**
     * 구독자에 대한 리스너 등록
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

구독자를 작성한 뒤, 해당 구독자의 핸들러 메서드가 Laravel의 [이벤트 자동 탐지 규칙](#event-discovery)을 따른다면 자동으로 등록됩니다. 그렇지 않은 경우, `Event` 파사드의 `subscribe` 메서드를 사용하여 수동으로 등록할 수 있습니다. 일반적으로 이 작업은 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 수행합니다:

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

이벤트를 디스패치하는 코드를 테스트할 때, 이벤트 리스너의 실제 실행은 건너뛰고자 할 수 있습니다. 리스너 코드는 직접적으로 별도의 테스트에서 검증할 수 있기 때문입니다. 리스너 그 자체를 테스트하려면, 테스트에서 리스너 인스턴스를 생성하고 `handle` 메서드를 직접 호출하면 됩니다.

`Event` 파사드의 `fake` 메서드를 활용하면 리스너 실행 없이 테스트 코드를 실행하고, `assertDispatched`, `assertNotDispatched`, `assertNothingDispatched` 등의 메서드로 어떤 이벤트가 디스패치되었는지 검증할 수 있습니다:

```php tab=Pest
<?php

use App\Events\OrderFailedToShip;
use App\Events\OrderShipped;
use Illuminate\Support\Facades/Event;

test('orders can be shipped', function () {
    Event::fake();

    // 주문 발송 실행...

    // 이벤트가 디스패치되었는지 검증...
    Event::assertDispatched(OrderShipped::class);

    // 이벤트가 2번 디스패치되었는지 검증...
    Event::assertDispatched(OrderShipped::class, 2);

    // 이벤트가 한번만 디스패치되었는지 검증...
    Event::assertDispatchedOnce(OrderShipped::class);

    // 디스패치되지 않은 이벤트 검증...
    Event::assertNotDispatched(OrderFailedToShip::class);

    // 어떠한 이벤트도 디스패치되지 않았는지 검증...
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
     * 주문 발송 테스트
     */
    public function test_orders_can_be_shipped(): void
    {
        Event::fake();

        // 주문 발송 실행...

        // 이벤트가 디스패치되었는지 검증...
        Event::assertDispatched(OrderShipped::class);

        // 이벤트가 2번 디스패치되었는지 검증...
        Event::assertDispatched(OrderShipped::class, 2);

        // 이벤트가 한번만 디스패치되었는지 검증...
        Event::assertDispatchedOnce(OrderShipped::class);

        // 디스패치되지 않은 이벤트 검증...
        Event::assertNotDispatched(OrderFailedToShip::class);

        // 어떠한 이벤트도 디스패치되지 않았는지 검증...
        Event::assertNothingDispatched();
    }
}
```

특정 조건에 부합하는 이벤트가 디스패치되었는지 검증하고 싶으면, `assertDispatched`나 `assertNotDispatched` 메서드에 클로저를 전달하세요. 클로저의 반환값이 `true`인 이벤트가 최소 하나라도 있으면 검증에 성공합니다:

```php
Event::assertDispatched(function (OrderShipped $event) use ($order) {
    return $event->order->id === $order->id;
});
```

특정 이벤트에 대해 리스너가 등록되어 있는지만 검증하고 싶다면, `assertListening` 메서드를 사용할 수 있습니다:

```php
Event::assertListening(
    OrderShipped::class,
    SendShipmentNotification::class
);
```

> [!WARNING]
> `Event::fake()` 호출 이후에는 이벤트 리스너가 실행되지 않습니다. 따라서, 모델의 `creating` 이벤트에서 UUID를 생성하는 등 이벤트에 의존하는 팩토리를 사용하는 경우, 팩토리 사용 후에 `Event::fake()`를 호출해야 합니다.

<a name="faking-a-subset-of-events"></a>
### 특정 이벤트만 가짜로 처리

특정 이벤트에 대해서만 리스너 실행을 가짜로 처리하고 싶다면, `fake` 또는 `fakeFor` 메서드에 이벤트 목록을 전달하세요:

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
 * 주문 처리 테스트
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

일부 이벤트를 제외한 전체 이벤트를 가짜 처리하려면 `except` 메서드를 사용하세요:

```php
Event::fake()->except([
    OrderCreated::class,
]);
```

<a name="scoped-event-fakes"></a>
### 스코프 이벤트 가짜 처리

테스트의 특정 구간에서만 이벤트 리스너 실행을 가짜 처리하고 싶을 때는 `fakeFor` 메서드를 사용하세요:

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

    // 이후에는 이벤트가 정상적으로 디스패치되고, 옵저버도 동작함...
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
     * 주문 처리 테스트
     */
    public function test_orders_can_be_processed(): void
    {
        $order = Event::fakeFor(function () {
            $order = Order::factory()->create();

            Event::assertDispatched(OrderCreated::class);

            return $order;
        });

        // 이후에는 이벤트가 정상적으로 디스패치되고, 옵저버도 동작함...
        $order->update([
            // ...
        ]);
    }
}
```
