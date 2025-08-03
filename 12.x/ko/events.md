# 이벤트 (Events)

- [소개](#introduction)
- [이벤트 및 리스너 생성](#generating-events-and-listeners)
- [이벤트 및 리스너 등록](#registering-events-and-listeners)
    - [이벤트 탐색](#event-discovery)
    - [수동으로 이벤트 등록](#manually-registering-events)
    - [클로저 리스너](#closure-listeners)
- [이벤트 정의](#defining-events)
- [리스너 정의](#defining-listeners)
- [큐잉된 이벤트 리스너](#queued-event-listeners)
    - [큐와 수동으로 상호작용하기](#manually-interacting-with-the-queue)
    - [큐잉된 이벤트 리스너와 데이터베이스 트랜잭션](#queued-event-listeners-and-database-transactions)
    - [큐잉된 리스너 미들웨어](#queued-listener-middleware)
    - [암호화된 큐잉된 리스너](#encrypted-queued-listeners)
    - [실패한 작업 처리](#handling-failed-jobs)
- [이벤트 디스패치](#dispatching-events)
    - [데이터베이스 트랜잭션 후에 이벤트 디스패치](#dispatching-events-after-database-transactions)
- [이벤트 구독자](#event-subscribers)
    - [이벤트 구독자 작성](#writing-event-subscribers)
    - [이벤트 구독자 등록](#registering-event-subscribers)
- [테스트](#testing)
    - [일부 이벤트를 페이크 처리하기](#faking-a-subset-of-events)
    - [범위 제한 이벤트 페이크](#scoped-event-fakes)

<a name="introduction"></a>
## 소개

Laravel의 이벤트는 간단한 옵저버 패턴(observer pattern) 구현을 제공하여, 애플리케이션 내에서 발생하는 다양한 이벤트를 구독하고 청취할 수 있도록 합니다. 이벤트 클래스는 일반적으로 `app/Events` 디렉터리에 저장되며, 해당 리스너들은 `app/Listeners`에 저장됩니다. Artisan 콘솔 명령어로 이벤트와 리스너를 생성할 때 이 디렉터리들은 자동으로 생성되므로, 애플리케이션에 아직 없더라도 걱정하지 마십시오.

이벤트는 애플리케이션의 여러 부분을 느슨하게 결합시키는 좋은 방법입니다. 하나의 이벤트에 여러 개의 독립적인 리스너가 연결될 수 있기 때문입니다. 예를 들어, 주문이 발송될 때마다 사용자에게 Slack 알림을 보내고 싶다면, 주문 처리 코드와 Slack 알림 코드를 직접 연결하는 대신 `App\Events\OrderShipped` 이벤트를 발생시키고, 이 이벤트를 수신하여 Slack 알림을 전송하는 리스너를 두면 됩니다.

<a name="generating-events-and-listeners"></a>
## 이벤트 및 리스너 생성

빠르게 이벤트와 리스너를 생성하려면 `make:event`와 `make:listener` Artisan 명령어를 사용할 수 있습니다:

```shell
php artisan make:event PodcastProcessed

php artisan make:listener SendPodcastNotification --event=PodcastProcessed
```

추가 인수 없이 `make:event`와 `make:listener` 명령어만 실행해도 Laravel이 자동으로 클래스 이름과, 리스너 생성 시에는 어떤 이벤트를 청취할지 물어봅니다:

```shell
php artisan make:event

php artisan make:listener
```

<a name="registering-events-and-listeners"></a>
## 이벤트 및 리스너 등록

<a name="event-discovery"></a>
### 이벤트 탐색

기본적으로 Laravel은 애플리케이션의 `Listeners` 디렉터리를 스캔하며 자동으로 이벤트 리스너를 찾아 등록합니다. Laravel은 `handle` 또는 `__invoke`로 시작하는 리스너 클래스 메서드를 발견하면, 그 메서드에 타입힌트된 이벤트에 대한 리스너로 등록합니다:

```php
use App\Events\PodcastProcessed;

class SendPodcastNotification
{
    /**
     * 이벤트 처리.
     */
    public function handle(PodcastProcessed $event): void
    {
        // ...
    }
}
```

PHP의 유니언 타입으로 여러 이벤트를 동시에 청취할 수도 있습니다:

```php
/**
 * 이벤트 처리.
 */
public function handle(PodcastProcessed|PodcastPublished $event): void
{
    // ...
}
```

리스너를 다른 디렉터리나 여러 디렉터리에 저장하려면, 애플리케이션의 `bootstrap/app.php` 파일에서 `withEvents` 메서드를 사용해 Laravel에게 해당 디렉터리를 스캔하도록 지시할 수 있습니다:

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/Orders/Listeners',
])
```

`*` 와일드카드를 사용해 유사한 여러 디렉터리를 동시에 스캔할 수도 있습니다:

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/*/Listeners',
])
```

등록된 모든 리스너를 확인하려면 아래 명령어를 사용할 수 있습니다:

```shell
php artisan event:list
```

<a name="event-discovery-in-production"></a>
#### 운영 환경에서 이벤트 탐색

애플리케이션의 성능을 높이기 위해 `optimize` 또는 `event:cache` Artisan 명령어로 모든 리스너의 매니페스트를 캐싱하는 것이 좋습니다. 보통 이 명령어는 [배포 프로세스](/docs/12.x/deployment#optimization)의 일부로 실행됩니다. 이렇게 캐싱된 매니페스트는 이벤트 등록 과정을 가속화하는 데 활용됩니다. 캐시를 삭제하려면 `event:clear` 명령어를 사용하세요.

<a name="manually-registering-events"></a>
### 수동으로 이벤트 등록

`Event` 파사드를 사용하면 애플리케이션의 `AppServiceProvider`의 `boot` 메서드 내에서 이벤트와 해당 리스너를 수동으로 등록할 수 있습니다:

```php
use App\Domain\Orders\Events\PodcastProcessed;
use App\Domain\Orders\Listeners\SendPodcastNotification;
use Illuminate\Support\Facades\Event;

/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Event::listen(
        PodcastProcessed::class,
        SendPodcastNotification::class,
    );
}
```

등록된 리스너 목록 확인도 동일하게 `event:list` 명령어를 사용합니다:

```shell
php artisan event:list
```

<a name="closure-listeners"></a>
### 클로저 리스너

보통 리스너는 클래스로 정의하지만, `AppServiceProvider`의 `boot` 메서드 내에서 클로저 기반 리스너를 수동 등록할 수도 있습니다:

```php
use App\Events\PodcastProcessed;
use Illuminate\Support\Facades\Event;

/**
 * 애플리케이션 서비스 부트스트랩.
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

클로저 리스너를 등록할 때, `Illuminate\Events\queueable` 함수를 감싸면 Laravel에게 이 리스너를 큐(queue)를 통해 실행하도록 지시할 수 있습니다:

```php
use App\Events\PodcastProcessed;
use function Illuminate\Events\queueable;
use Illuminate\Support\Facades\Event;

/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Event::listen(queueable(function (PodcastProcessed $event) {
        // ...
    }));
}
```

큐에 대한 연결, 큐 이름, 지연(delay)을 `onConnection`, `onQueue`, `delay` 메서드로 조정할 수 있습니다:

```php
Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->onConnection('redis')->onQueue('podcasts')->delay(now()->addSeconds(10)));
```

익명 큐잉 리스너 실패 시 처리하려면, `queueable` 리스너 정의 시 `catch` 메서드에 클로저를 전달할 수 있습니다. 이 클로저는 이벤트 인스턴스와 실패를 일으킨 `Throwable` 인스턴스를 받습니다:

```php
use App\Events\PodcastProcessed;
use function Illuminate\Events\queueable;
use Illuminate\Support\Facades\Event;
use Throwable;

Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->catch(function (PodcastProcessed $event, Throwable $e) {
    // 큐잉 리스너 실패 처리...
}));
```

<a name="wildcard-event-listeners"></a>
#### 와일드카드 이벤트 리스너

`*` 문자를 와일드카드 매개변수로 사용해 여러 이벤트를 하나의 리스너에서 처리할 수도 있습니다. 와일드카드 리스너는 첫 번째 인수로 이벤트 이름, 두 번째 인수로 이벤트 데이터 배열 전체를 받습니다:

```php
Event::listen('event.*', function (string $eventName, array $data) {
    // ...
});
```

<a name="defining-events"></a>
## 이벤트 정의

이벤트 클래스는 이벤트와 관련된 정보를 담는 데이터 컨테이너입니다. 예를 들어 `App\Events\OrderShipped` 이벤트가 [Eloquent ORM](/docs/12.x/eloquent) 모델 객체를 받는 경우를 보겠습니다:

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
     * 새로운 이벤트 인스턴스 생성.
     */
    public function __construct(
        public Order $order,
    ) {}
}
```

보시다시피 이 이벤트 클래스에는 복잡한 로직이 없으며, 구매된 `App\Models\Order` 인스턴스를 담는 그릇 역할만 합니다. 이벤트에서 사용하는 `SerializesModels` 트레이트는 PHP의 `serialize` 함수(예: [큐잉된 리스너](#queued-event-listeners) 사용 시)에 의해 이벤트 객체가 직렬화되었을 때 Eloquent 모델을 우아하게 직렬화합니다.

<a name="defining-listeners"></a>
## 리스너 정의

다음으로 예시 이벤트에 대한 리스너를 살펴보겠습니다. 이벤트 리스너는 `handle` 메서드에서 이벤트 인스턴스를 받습니다. `make:listener` Artisan 명령어를 `--event` 옵션과 함께 실행하면, 자동으로 적절한 이벤트 클래스를 import하고 `handle` 메서드의 타입힌트를 설정해 줍니다. `handle` 메서드 내부에서 이벤트에 대응하기 위한 작업을 수행할 수 있습니다:

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
        // $event->order를 통해 주문에 접근...
    }
}
```

> [!NOTE]
> 리스너의 생성자에서 필요한 의존성을 타입힌트하여 주입받을 수도 있습니다. 모든 이벤트 리스너는 Laravel [서비스 컨테이너](/docs/12.x/container)를 통해 해석되므로 의존성은 자동으로 주입됩니다.

<a name="stopping-the-propagation-of-an-event"></a>
#### 이벤트 전파 중지

경우에 따라서 이벤트가 다른 리스너로 전파되는 것을 중지시키고 싶을 때가 있습니다. 이럴 경우 리스너의 `handle` 메서드에서 `false`를 반환하면 이벤트 전파가 중지됩니다.

<a name="queued-event-listeners"></a>
## 큐잉된 이벤트 리스너

리스너가 이메일 발송이나 HTTP 요청 같은 느린 작업을 수행할 때는 큐잉(listener를 큐에 넣어 비동기 실행) 하는 것이 좋습니다. 큐잉 리스너 사용 전에는 반드시 [큐 시스템](/docs/12.x/queues)을 설정하고, 로컬 및 서버에서 큐 워커를 실행해야 합니다.

리스너가 큐에 들어가도록 하려면 리스너 클래스에 `ShouldQueue` 인터페이스를 추가하세요. Artisan의 `make:listener` 명령어로 생성된 리스너는 기본적으로 이 인터페이스를 import 하므로 즉시 사용할 수 있습니다:

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

이제 이 리스너가 처리하는 이벤트가 발생하면 Laravel 큐 시스템에 의해 자동으로 큐잉되어 실행됩니다. 큐 워커가 리스너 실행 중 예외를 던지지 않으면 작업 완료 후 큐 작업은 자동 삭제됩니다.

<a name="customizing-the-queue-connection-queue-name"></a>
#### 큐 연결, 큐 이름 및 지연 설정

리스너의 큐 연결(connection), 큐 이름, 처리 지연(delay)을 조정하고 싶다면 리스너 클래스에 다음 속성을 정의하세요:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    /**
     * 작업이 전송될 큐 연결 이름.
     *
     * @var string|null
     */
    public $connection = 'sqs';

    /**
     * 작업이 전송될 큐 이름.
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

런타임에 설정을 동적으로 부여하려면 각각 `viaConnection`, `viaQueue`, `withDelay` 메서드를 구현하면 됩니다:

```php
/**
 * 리스너 큐 연결 이름 반환.
 */
public function viaConnection(): string
{
    return 'sqs';
}

/**
 * 리스너 큐 이름 반환.
 */
public function viaQueue(): string
{
    return 'listeners';
}

/**
 * 작업 처리 전 대기 시간(초) 반환.
 */
public function withDelay(OrderShipped $event): int
{
    return $event->highPriority ? 0 : 60;
}
```

<a name="conditionally-queueing-listeners"></a>
#### 조건부 큐잉 리스너

상황에 따라 런타임 데이터를 근거로 리스너를 큐에 넣을지 결정해야 할 때가 있습니다. 이런 경우, 리스너에 `shouldQueue` 메서드를 추가하여 큐에 넣을지 여부를 반환하도록 할 수 있습니다. 만약 `false`를 반환하면 큐에 들어가지 않습니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderCreated;
use Illuminate\Contracts\Queue\ShouldQueue;

class RewardGiftCard implements ShouldQueue
{
    /**
     * 선물 카드를 보상.
     */
    public function handle(OrderCreated $event): void
    {
        // ...
    }

    /**
     * 리스너를 큐에 넣을지 결정.
     */
    public function shouldQueue(OrderCreated $event): bool
    {
        return $event->order->subtotal >= 5000;
    }
}
```

<a name="manually-interacting-with-the-queue"></a>
### 큐와 수동으로 상호작용하기

리스너가 포함하는 큐 작업의 `delete` 및 `release` 메서드에 직접 접근해야 한다면 `Illuminate\Queue\InteractsWithQueue` 트레이트를 사용하세요. 이 트레이트는 기본 생성된 리스너에 기본 임포트 되어 있으며, 아래와 같이 활용 가능합니다:

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
### 큐잉된 이벤트 리스너와 데이터베이스 트랜잭션

큐에 명시된 리스너를 데이터베이스 트랜잭션 중에 dispatch하면, 트랜잭션 커밋 전에 큐 워커가 리스너를 처리할 수 있습니다. 이럴 경우 트랜잭션 내에서 모델이나 데이터베이스 레코드의 변경사항이 DB에 반영되지 않았거나 새로 생성된 모델이 아직 존재하지 않아, 리스너 작동 중 예기치 않은 오류가 발생할 수 있습니다.

만약 큐 연결에서 `after_commit` 설정이 `false`라면, 특정 큐잉 리스너가 열린 모든 DB 트랜잭션이 커밋된 후에 디스패치되도록 하려면, 리스너 클래스에서 `ShouldQueueAfterCommit` 인터페이스를 구현하세요:

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
> 이 문제에 대한 자세한 설명과 해결 방법은 [큐 작업과 DB 트랜잭션](/docs/12.x/queues#jobs-and-database-transactions) 문서를 참조하세요.

<a name="queued-listener-middleware"></a>
### 큐잉된 리스너 미들웨어

큐잉된 리스너도 [작업 미들웨어](/docs/12.x/queues#job-middleware)를 사용할 수 있습니다. 미들웨어를 통해 큐잉 리스너 실행 전후에 커스텀 로직을 감쌀 수 있어, 리스너 내부 코드를 간결하게 유지할 수 있습니다. 미들웨어 생성 후, 리스너의 `middleware` 메서드에서 반환하면 됩니다:

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
     * 통과할 미들웨어 반환.
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
#### 암호화된 큐잉된 리스너

Laravel은 큐잉된 리스너의 데이터 프라이버시와 무결성을 위해 [암호화](/docs/12.x/encryption)를 지원합니다. 이를 활성화하려면 리스너 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하세요. 그러면 Laravel이 큐에 넣기 전 자동으로 리스너를 암호화합니다:

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

큐잉된 이벤트 리스너가 실패하는 경우가 있을 수 있습니다. 큐 워커가 리스너 실행 시 최대 시도 횟수를 초과하면, 리스너의 `failed` 메서드가 호출됩니다. 이 메서드는 이벤트 인스턴스와 실패를 일으킨 `Throwable` 인스턴스를 인수로 받습니다:

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
#### 큐잉된 리스너 최대 시도 횟수 지정

큐잉 리스너에서 오류가 나는 경우 무한 재시도를 막기 위해 최대 시도 횟수를 설정하는 방법이 있습니다.

리스너 클래스에 `tries` 속성을 정의하며, 이 값이 리스너가 실패로 판단되기 전 시도 가능한 최대 횟수입니다:

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
     * 큐잉 리스너가 시도할 최대 횟수.
     *
     * @var int
     */
    public $tries = 5;
}
```

또한, 리스너가 실패하기 전까지 임의 횟수 시도하되 특정 시간 이후 시도 중단하려면 `retryUntil` 메서드를 정의하세요. 이 메서드는 `DateTime` 인스턴스를 반환해야 합니다:

```php
use DateTime;

/**
 * 리스너 타임아웃 시각 결정.
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(5);
}
```

`retryUntil`과 `tries`가 모두 정의되면 Laravel은 `retryUntil`을 우선시합니다.

<a name="specifying-queued-listener-backoff"></a>
#### 큐잉된 리스너 백오프 지정

예외가 발생한 후 재시도 전 대기할 시간을 초 단위로 설정하려면 `backoff` 속성을 리스너 클래스에 정의하세요:

```php
/**
 * 재시도 전 대기 시간(초).
 *
 * @var int
 */
public $backoff = 3;
```

복잡한 백오프 로직이 필요한 경우 `backoff` 메서드를 구현하면 됩니다:

```php
/**
 * 재시도 전 대기 시간(초) 계산.
 */
public function backoff(OrderShipped $event): int
{
    return 3;
}
```

또는 배열로 다중 지연 값을 반환해 "지수 백오프"를 쉽게 구현할 수 있습니다. 다음 예시는 첫 번째 재시도는 1초, 두 번째는 5초, 세 번째 이후는 10초 지연하는 패턴입니다:

```php
/**
 * 재시도 전 대기 시간 배열 반환.
 *
 * @return list<int>
 */
public function backoff(OrderShipped $event): array
{
    return [1, 5, 10];
}
```

<a name="specifying-queued-listener-max-exceptions"></a>
#### 큐잉된 리스너 최대 예외 허용 횟수 지정

종종, 재시도 횟수는 충분하지만 특정 횟수 이상의 처리되지 않은 예외(unhandled exceptions)가 발생하면 실패 처리하고 싶을 수 있습니다. 이를 위해 `maxExceptions` 속성을 리스너 클래스에 정의할 수 있습니다:

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
     * 최대 시도 횟수.
     *
     * @var int
     */
    public $tries = 25;

    /**
     * 최대 허용 처리되지 않은 예외 수.
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

이 예시에서 최대 25회 재시도하지만, 3회 미처리 예외가 발생하면 즉시 실패 처리합니다.

<a name="specifying-queued-listener-timeout"></a>
#### 큐잉된 리스너 타임아웃 지정

리스너가 실행하는 데 얼마나 오래 걸릴지 예상 가능한 경우, 타임아웃 값을 설정할 수 있습니다. 지정된 초만큼 실행 시간이 초과되면 워커가 오류와 함께 종료됩니다. 리스너 클래스에 `timeout` 속성을 정의하여 최대 실행 시간을 초 단위로 지정하세요:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    /**
     * 타임아웃 전 허용할 최대 실행 시간(초).
     *
     * @var int
     */
    public $timeout = 120;
}
```

타임아웃 시 실패 처리 여부도 플래그로 표시할 수 있습니다. `failOnTimeout` 속성을 `true`로 설정하면 타임아웃 시 리스너가 실패로 기록됩니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    /**
     * 타임아웃 시 실패 표시 여부.
     *
     * @var bool
     */
    public $failOnTimeout = true;
}
```

<a name="dispatching-events"></a>
## 이벤트 디스패치

이벤트를 발생시키려면 이벤트 클래스에서 static `dispatch` 메서드를 호출하면 됩니다. 이 메서드는 `Illuminate\Foundation\Events\Dispatchable` 트레이트에서 제공합니다. `dispatch`에 전달한 모든 인수는 이벤트 생성자에 그대로 전달됩니다:

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
     * 지정된 주문 배송 처리.
     */
    public function store(Request $request): RedirectResponse
    {
        $order = Order::findOrFail($request->order_id);

        // 주문 배송 로직...

        OrderShipped::dispatch($order);

        return redirect('/orders');
    }
}
```

조건에 따라 이벤트를 디스패치하려면 `dispatchIf`와 `dispatchUnless` 메서드를 사용할 수 있습니다:

```php
OrderShipped::dispatchIf($condition, $order);

OrderShipped::dispatchUnless($condition, $order);
```

> [!NOTE]
> 테스트 시에는 이벤트 리스너를 실제로 실행하지 않고, 특정 이벤트가 발생했는지 확인하는 것이 유용할 수 있습니다. Laravel의 [내장 테스트 도구](#testing)를 활용하면 쉽습니다.

<a name="dispatching-events-after-database-transactions"></a>
### 데이터베이스 트랜잭션 후에 이벤트 디스패치

가끔 현재 활성 데이터베이스 트랜잭션이 커밋된 후에만 이벤트를 디스패치하고 싶을 때도 있습니다. 이를 위해 이벤트 클래스에서 `ShouldDispatchAfterCommit` 인터페이스를 구현하세요.

이 인터페이스를 구현하면 Laravel은 현재 DB 트랜잭션이 커밋될 때까지 이벤트 디스패치를 미룹니다. 트랜잭션이 실패하면 이벤트가 무시되고, 트랜잭션이 없으면 즉시 디스패치합니다:

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
     * 새로운 이벤트 인스턴스 생성.
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

이벤트 구독자는 하나의 클래스 안에 여러 이벤트를 구독할 수 있게 해, 여러 이벤트 핸들러들을 한 곳에 모을 수 있습니다. 구독자 클래스는 `subscribe` 메서드를 정의하는데, 이 메서드는 이벤트 디스패처 인스턴스를 받습니다. 디스패처의 `listen` 메서드를 호출해 이벤트 리스너를 등록하세요:

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
     * 구독자 리스너 등록.
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

리스너 메서드가 구독자 클래스 내에 정의되어 있으면, `subscribe` 메서드에서 이벤트와 메서드 이름의 배열을 반환하는 것이 더 간편할 수 있습니다. Laravel이 자동으로 클래스 이름을 인식해 이벤트 리스너를 등록합니다:

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
     * 구독자 리스너 등록.
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

구독자를 작성한 후, Laravel은 구독자 클래스 내의 핸들러 메서드를 [자동 이벤트 탐색](#event-discovery) 규칙에 따를 경우 자동 등록합니다. 그렇지 않으면 `Event` 파사드의 `subscribe` 메서드를 사용해 수동 등록해야 합니다. 일반적으로 이 작업은 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 이뤄집니다:

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
## 테스트

이벤트를 디스패치하는 코드를 테스트할 때, 실제 이벤트 리스너 실행을 하지 않고 이벤트가 발생했음을 확인하는 것이 유용합니다. 물론 리스너 자체를 테스트하려면 리스너 인스턴스를 직접 생성 후 `handle` 메서드를 호출하면 됩니다.

`Event` 파사드의 `fake` 메서드 사용 시, 리스너는 실행되지 않고 테스트 대상 코드를 실행한 후, `assertDispatched`, `assertNotDispatched`, `assertNothingDispatched` 메서드로 어떤 이벤트가 디스패치되었는지 검증할 수 있습니다:

```php tab=Pest
<?php

use App\Events\OrderFailedToShip;
use App\Events\OrderShipped;
use Illuminate\Support\Facades\Event;

test('orders can be shipped', function () {
    Event::fake();

    // 주문 배송 작업 수행...

    // 이벤트 디스패치 여부 확인...
    Event::assertDispatched(OrderShipped::class);

    // 이벤트가 두 번 디스패치되었는지...
    Event::assertDispatched(OrderShipped::class, 2);

    // 이벤트가 디스패치되지 않았는지...
    Event::assertNotDispatched(OrderFailedToShip::class);

    // 이벤트가 아예 디스패치되지 않았는지...
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
     * 주문 배송 테스트.
     */
    public function test_orders_can_be_shipped(): void
    {
        Event::fake();

        // 주문 배송 작업 수행...

        // 이벤트 디스패치 여부 확인...
        Event::assertDispatched(OrderShipped::class);

        // 이벤트가 두 번 디스패치되었는지...
        Event::assertDispatched(OrderShipped::class, 2);

        // 이벤트가 디스패치되지 않았는지...
        Event::assertNotDispatched(OrderFailedToShip::class);

        // 이벤트가 아예 디스패치되지 않았는지...
        Event::assertNothingDispatched();
    }
}
```

`assertDispatched`와 `assertNotDispatched`에 클로저를 넘겨 특정 조건을 만족하는 이벤트가 디스패치되었는지 검증할 수도 있습니다. 조건에 맞는 이벤트가 적어도 하나 있으면 검증에 성공합니다:

```php
Event::assertDispatched(function (OrderShipped $event) use ($order) {
    return $event->order->id === $order->id;
});
```

특정 이벤트에 리스너가 연결되어 있는지만 확인하려면 `assertListening` 메서드를 사용하세요:

```php
Event::assertListening(
    OrderShipped::class,
    SendShipmentNotification::class
);
```

> [!WARNING]
> `Event::fake()` 호출 이후에는 어떤 이벤트 리스너도 실행되지 않습니다. 따라서 모델 팩토리에서 `creating` 이벤트 중 UUID 생성 등 이벤트에 의존하는 경우, `Event::fake()`는 팩토리 사용 이후에 호출해야 합니다.

<a name="faking-a-subset-of-events"></a>
### 일부 이벤트를 페이크 처리하기

특정 이벤트만 페이크하려면 `fake` 또는 `fakeFor` 메서드에 해당 이벤트들을 전달하세요:

```php tab=Pest
test('orders can be processed', function () {
    Event::fake([
        OrderCreated::class,
    ]);

    $order = Order::factory()->create();

    Event::assertDispatched(OrderCreated::class);

    // 그 외 이벤트들은 정상적으로 디스패치...
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

    // 그 외 이벤트들은 정상적으로 디스패치...
    $order->update([
        // ...
    ]);
}
```

페이크 처리하지 않을 이벤트만 지정해 예외 처리할 수도 있습니다:

```php
Event::fake()->except([
    OrderCreated::class,
]);
```

<a name="scoped-event-fakes"></a>
### 범위 제한 이벤트 페이크

테스트 코드 중 일부 영역에서만 이벤트 페이크를 적용하려면 `fakeFor` 메서드를 사용하세요:

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

    // 이벤트가 여전히 정상 디스패치되고 옵저버(Observers)가 작동함...
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

        // 이벤트가 여전히 정상 디스패치되고 옵저버(Observers)가 작동함...
        $order->update([
            // ...
        ]);
    }
}
```
