# 이벤트 (Events)

- [소개](#introduction)
- [이벤트 및 리스너 생성](#generating-events-and-listeners)
- [이벤트 및 리스너 등록](#registering-events-and-listeners)
    - [이벤트 탐지](#event-discovery)
    - [이벤트 수동 등록](#manually-registering-events)
    - [클로저 리스너](#closure-listeners)
- [이벤트 정의](#defining-events)
- [리스너 정의](#defining-listeners)
- [큐 처리 이벤트 리스너](#queued-event-listeners)
    - [큐와 수동 상호작용](#manually-interacting-with-the-queue)
    - [큐 처리 이벤트 리스너와 데이터베이스 트랜잭션](#queued-event-listeners-and-database-transactions)
    - [실패한 작업 처리](#handling-failed-jobs)
- [이벤트 디스패치](#dispatching-events)
    - [데이터베이스 트랜잭션 이후 이벤트 디스패치](#dispatching-events-after-database-transactions)
- [이벤트 구독자](#event-subscribers)
    - [이벤트 구독자 작성](#writing-event-subscribers)
    - [이벤트 구독자 등록](#registering-event-subscribers)
- [테스트](#testing)
    - [일부 이벤트 가짜 처리](#faking-a-subset-of-events)
    - [범위 지정 이벤트 가짜 처리](#scoped-event-fakes)

<a name="introduction"></a>
## 소개

Laravel의 이벤트는 간단한 옵저버 패턴(observer pattern) 구현을 제공하여, 애플리케이션 내에서 발생하는 다양한 이벤트를 구독하고 청취할 수 있게 해줍니다. 이벤트 클래스는 일반적으로 `app/Events` 디렉토리에 저장되며, 해당 이벤트의 리스너는 `app/Listeners`에 저장됩니다. Artisan 콘솔 명령어로 이벤트와 리스너를 생성할 때 이 디렉토리들이 자동으로 생성되기 때문에 해당 디렉토리가 없다고 걱정하지 않으셔도 됩니다.

이벤트는 애플리케이션의 여러 부분을 효과적으로 분리할 수 있는 좋은 방법입니다. 단일 이벤트에 여러 개의 리스너가 연결될 수 있고, 이들은 서로 의존하지 않습니다. 예를 들어, 주문이 배송될 때마다 사용자에게 Slack 알림을 보내고 싶다고 가정해보겠습니다. 주문 처리 코드와 Slack 알림 코드를 강하게 결합하는 대신, `App\Events\OrderShipped` 이벤트를 발생시키고, 리스너가 이 이벤트를 받아 Slack 알림을 실행하도록 할 수 있습니다.

<a name="generating-events-and-listeners"></a>
## 이벤트 및 리스너 생성

빠르게 이벤트와 리스너를 생성하고 싶으면 `make:event` 및 `make:listener` Artisan 명령어를 사용하세요:

```shell
php artisan make:event PodcastProcessed

php artisan make:listener SendPodcastNotification --event=PodcastProcessed
```

명령어에 인수를 주지 않고 `make:event` 또는 `make:listener`를 실행하면, Laravel이 자동으로 클래스명과 (리스너 생성 시) 어떤 이벤트를 청취할지 질문합니다:

```shell
php artisan make:event

php artisan make:listener
```

<a name="registering-events-and-listeners"></a>
## 이벤트 및 리스너 등록

<a name="event-discovery"></a>
### 이벤트 탐지

기본적으로 Laravel은 애플리케이션의 `Listeners` 디렉토리를 스캔해서 이벤트 리스너를 자동으로 찾아 등록합니다. Laravel은 `handle` 또는 `__invoke`로 시작하는 메서드를 가진 리스너 클래스를 찾으면, 해당 메서드 시그니처에 타입힌트된 이벤트에 연결하여 리스너로 등록합니다:

```php
use App\Events\PodcastProcessed;

class SendPodcastNotification
{
    /**
     * 주어진 이벤트를 처리합니다.
     */
    public function handle(PodcastProcessed $event): void
    {
        // ...
    }
}
```

PHP의 유니온 타입을 이용해 하나의 리스너 메서드에서 여러 이벤트를 청취할 수도 있습니다:

```php
/**
 * 주어진 이벤트를 처리합니다.
 */
public function handle(PodcastProcessed|PodcastPublished $event): void
{
    // ...
}
```

리스너를 여러 디렉토리나 다른 디렉토리에 저장할 계획이라면, 애플리케이션의 `bootstrap/app.php` 파일에서 `withEvents` 메서드에 스캔할 경로를 지정할 수 있습니다:

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/Orders/Listeners',
])
```

`*` 와일드카드를 사용하여 유사한 여러 디렉토리를 지정할 수도 있습니다:

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/*/Listeners',
])
```

애플리케이션에 등록된 모든 리스너 목록은 `event:list` Artisan 명령어로 확인할 수 있습니다:

```shell
php artisan event:list
```

<a name="event-discovery-in-production"></a>
#### 프로덕션 환경에서 이벤트 탐지

애플리케이션의 리스너 목록을 캐시해 이벤트 등록 속도를 향상시키려면 `optimize` 또는 `event:cache` Artisan 명령어를 사용하세요. 보통 이 작업은 배포 과정 중에 이루어집니다([배포 문서](/docs/master/deployment#optimization) 참고). 캐시를 삭제하려면 `event:clear` 명령어를 사용하면 됩니다.

<a name="manually-registering-events"></a>
### 이벤트 수동 등록

`Event` 파사드를 사용해 애플리케이션의 `AppServiceProvider`의 `boot` 메서드 내에서 이벤트와 리스너를 수동으로 등록할 수도 있습니다:

```php
use App\Domain\Orders\Events\PodcastProcessed;
use App\Domain\Orders\Listeners\SendPodcastNotification;
use Illuminate\Support\Facades\Event;

/**
 * 애플리케이션 서비스 부트스트랩
 */
public function boot(): void
{
    Event::listen(
        PodcastProcessed::class,
        SendPodcastNotification::class,
    );
}
```

등록된 리스너 목록은 `event:list` 명령어로 확인할 수 있습니다:

```shell
php artisan event:list
```

<a name="closure-listeners"></a>
### 클로저 리스너

일반적으로 리스너는 클래스 형태로 정의하지만, `AppServiceProvider`의 `boot` 메서드에서 클로저 기반 리스너를 등록할 수도 있습니다:

```php
use App\Events\PodcastProcessed;
use Illuminate\Support\Facades\Event;

/**
 * 애플리케이션 서비스 부트스트랩
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

클로저 기반 리스너 등록 시, `Illuminate\Events\queueable` 함수를 사용해 Laravel에게 해당 리스너를 큐로 실행하도록 지시할 수 있습니다:

```php
use App\Events\PodcastProcessed;
use function Illuminate\Events\queueable;
use Illuminate\Support\Facades\Event;

/**
 * 애플리케이션 서비스 부트스트랩
 */
public function boot(): void
{
    Event::listen(queueable(function (PodcastProcessed $event) {
        // ...
    }));
}
```

큐 작업처럼 `onConnection`, `onQueue`, `delay` 메서드로 큐 연결, 큐 이름, 지연 시간을 지정할 수 있습니다:

```php
Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->onConnection('redis')->onQueue('podcasts')->delay(now()->addSeconds(10)));
```

익명 큐 리스너 실패를 처리하려면, `catch` 메서드에 클로저를 전달할 수 있습니다. 이 클로저는 이벤트 인스턴스와 오류를 발생시킨 `Throwable` 인스턴스를 받습니다:

```php
use App\Events\PodcastProcessed;
use function Illuminate\Events\queueable;
use Illuminate\Support\Facades\Event;
use Throwable;

Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->catch(function (PodcastProcessed $event, Throwable $e) {
    // 큐 리스너 실패 처리...
}));
```

<a name="wildcard-event-listeners"></a>
#### 와일드카드 이벤트 리스너

`*` 와일드카드를 사용해 여러 이벤트를 하나의 리스너에서 처리할 수 있습니다. 이때 와일드카드 리스너는 첫 인수로 이벤트 이름, 두 번째 인수로 전체 이벤트 데이터를 배열 형태로 받습니다:

```php
Event::listen('event.*', function (string $eventName, array $data) {
    // ...
});
```

<a name="defining-events"></a>
## 이벤트 정의

이벤트 클래스는 이벤트와 관련된 데이터를 담는 컨테이너 역할을 합니다. 예를 들어, `App\Events\OrderShipped` 이벤트가 Eloquent ORM 객체를 받는 상황을 봅시다:

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
     * 새 이벤트 인스턴스 생성
     */
    public function __construct(
        public Order $order,
    ) {}
}
```

보시다시피 해당 이벤트 클래스에는 로직이 없습니다. 단순히 구매한 `App\Models\Order` 인스턴스를 담는 컨테이너입니다. `SerializesModels` 트레이트는 이벤트 객체가 PHP `serialize` 함수로 직렬화될 때(예: 큐 처리 리스너에서) Eloquent 모델을 우아하게 직렬화해줍니다.

<a name="defining-listeners"></a>
## 리스너 정의

다음으로, 위 이벤트의 리스너 예시를 살펴봅시다. 이벤트 리스너는 `handle` 메서드에서 이벤트 인스턴스를 받습니다. `make:listener` Artisan 명령어에 `--event` 옵션을 주면, 자동으로 올바른 이벤트 클래스 임포트와 `handle` 메서드 타입힌트를 추가해줍니다. `handle` 메서드 내에서 이벤트에 반응하기 위한 작업을 수행하면 됩니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;

class SendShipmentNotification
{
    /**
     * 이벤트 리스너 생성자
     */
    public function __construct() {}

    /**
     * 이벤트 처리 메서드
     */
    public function handle(OrderShipped $event): void
    {
        // $event->order 를 사용하여 주문 정보 접근...
    }
}
```

> [!NOTE]  
> 이벤트 리스너는 생성자에서 필요한 의존성을 타입힌트하여 주입받을 수도 있습니다. 모든 이벤트 리스너는 Laravel [서비스 컨테이너](/docs/master/container)를 통해 해결되기 때문에 의존성은 자동으로 주입됩니다.

<a name="stopping-the-propagation-of-an-event"></a>
#### 이벤트 전파 중단

경우에 따라 이벤트가 다른 리스너로 전달되지 않도록 중단할 수 있습니다. 이때 리스너의 `handle` 메서드에서 `false`를 반환하면 이벤트 전파가 멈춥니다.

<a name="queued-event-listeners"></a>
## 큐 처리 이벤트 리스너

리스너가 이메일 전송이나 HTTP 요청처럼 느린 작업을 수행한다면, 큐로 처리하는 것이 좋습니다. 큐 처리 리스너 사용 전에는 큐 설정을 마치고, 서버나 로컬 개발환경에서 큐 워커를 반드시 실행해야 합니다.

리스너 클래스로 큐 처리하도록 하려면 `ShouldQueue` 인터페이스를 적용하세요. `make:listener` Artisan 명령어로 생성한 리스너는 이미 이 인터페이스를 임포트해둡니다:

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

이제 이 리스너가 처리하는 이벤트가 발생하면, Laravel은 큐 시스템을 통해 자동으로 이 리스너를 큐에 넣습니다. 큐 워커가 해당 작업을 실행하며, 작업에 예외가 발생하지 않으면 완료 후 자동으로 큐에서 삭제됩니다.

<a name="customizing-the-queue-connection-queue-name"></a>
#### 큐 연결, 큐 이름 및 지연 시간 설정

큐 연결명, 큐 이름, 지연 시간을 리스너 클래스에서 `$connection`, `$queue`, `$delay` 속성을 정의해 조정할 수 있습니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    /**
     * 이 작업이 속할 큐 연결명
     *
     * @var string|null
     */
    public $connection = 'sqs';

    /**
     * 이 작업이 사용할 큐 이름
     *
     * @var string|null
     */
    public $queue = 'listeners';

    /**
     * 작업을 처리하기 전에 대기할 초 단위 시간
     *
     * @var int
     */
    public $delay = 60;
}
```

실행 시 동적으로 설정하고 싶다면 `viaConnection`, `viaQueue`, `withDelay` 메서드를 정의할 수도 있습니다:

```php
/**
 * 큐 연결명을 반환
 */
public function viaConnection(): string
{
    return 'sqs';
}

/**
 * 큐 이름을 반환
 */
public function viaQueue(): string
{
    return 'listeners';
}

/**
 * 대기할 초 단위 시간을 계산해 반환
 */
public function withDelay(OrderShipped $event): int
{
    return $event->highPriority ? 0 : 60;
}
```

<a name="conditionally-queueing-listeners"></a>
#### 조건부 큐 처리

실행 중에 전달되는 데이터에 따라 큐 처리할지 결정하고 싶다면, 리스너 클래스에 `shouldQueue` 메서드를 추가하여 반환값으로 결정하게 할 수 있습니다. `false`를 반환하면 큐에 넣지 않고 즉시 실행합니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderCreated;
use Illuminate\Contracts\Queue\ShouldQueue;

class RewardGiftCard implements ShouldQueue
{
    /**
     * 선물 카드를 리워드로 지급합니다.
     */
    public function handle(OrderCreated $event): void
    {
        // ...
    }

    /**
     * 리스너를 큐에 보낼지 결정합니다.
     */
    public function shouldQueue(OrderCreated $event): bool
    {
        return $event->order->subtotal >= 5000;
    }
}
```

<a name="manually-interacting-with-the-queue"></a>
### 큐와 수동 상호작용

리스너의 큐 작업에 내장된 `delete`나 `release` 메서드를 직접 호출할 일이 있을 때는 `Illuminate\Queue\InteractsWithQueue` 트레이트를 사용하세요. 이 트레이트는 기본 생성 리스너에 포함되어 아래와 같은 메서드를 제공합니다:

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
     * 이벤트 처리
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
### 큐 처리 이벤트 리스너와 데이터베이스 트랜잭션

큐 처리 리스너가 데이터베이스 트랜잭션 내에서 디스패치되면, 트랜잭션이 커밋되기 전에 큐 작업이 실행되어 모델이나 데이터가 DB에 반영되지 않은 상태일 수 있습니다. 이 경우 모델 상태를 기준으로 한 리스너 실행에 오류가 발생할 수 있습니다.

큐 연결의 `after_commit` 설정이 `false`일 경우, 특정 큐 리스너가 모든 DB 트랜잭션 커밋 후에 실행되도록 하려면 리스너에 `ShouldQueueAfterCommit` 인터페이스를 구현하세요:

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
> 더 자세한 내용은 [큐 작업과 데이터베이스 트랜잭션](/docs/master/queues#jobs-and-database-transactions) 문서를 참고하세요.

<a name="handling-failed-jobs"></a>
### 실패한 작업 처리

큐 처리 이벤트 리스너가 실패하면, 큐 작업이 최대 시도 횟수를 초과했을 때 `failed` 메서드가 호출됩니다. 이 메서드는 이벤트 인스턴스와 실패 원인이 된 `Throwable` 인스턴스를 인자로 받습니다:

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
     * 이벤트 처리
     */
    public function handle(OrderShipped $event): void
    {
        // ...
    }

    /**
     * 실패한 작업 처리
     */
    public function failed(OrderShipped $event, Throwable $exception): void
    {
        // ...
    }
}
```

<a name="specifying-queued-listener-maximum-attempts"></a>
#### 큐 리스너 최대 시도 횟수 지정

큐 리스너가 오류를 낼 경우 무한 재시도하지 않도록, 시도 횟수를 제한하는 여러 방법이 있습니다.

리스너 클래스에 `$tries` 속성을 정의하여 시도 횟수를 지정할 수 있습니다:

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
    public $tries = 5;
}
```

시도 횟수 대신 일정 시간 동안만 시도하게 하려면 `retryUntil` 메서드를 정의하고 `DateTime` 인스턴스를 반환하면 됩니다:

```php
use DateTime;

/**
 * 리스너 타임아웃 시간을 결정
 */
public function retryUntil(): DateTime
{
    return now()->addMinutes(5);
}
```

<a name="specifying-queued-listener-backoff"></a>
#### 큐 리스너 재시도 지연 시간 설정

예외 발생 후 재시도까지의 대기 시간을 설정하려면 리스너 클래스에 `$backoff` 속성을 정의하세요:

```php
/**
 * 큐 리스너 재시도 전 대기할 초 단위 시간
 *
 * @var int
 */
public $backoff = 3;
```

더 복잡한 로직이 필요하면 `backoff` 메서드로 초 단위 대기 시간을 반환할 수도 있습니다:

```php
/**
 * 재시도 전 대기 시간을 계산
 */
public function backoff(): int
{
    return 3;
}
```

재시도 지연을 '지수적'으로 구성하려면 `backoff` 메서드에서 지연 시간 배열을 반환하세요. 아래 예시는 재시도 1회차는 1초, 2회차 5초, 3회차 및 이후 10초 지연을 의미합니다:

```php
/**
 * 재시도 전 대기 시간 배열 반환
 *
 * @return array<int, int>
 */
public function backoff(): array
{
    return [1, 5, 10];
}
```

<a name="dispatching-events"></a>
## 이벤트 디스패치

이벤트를 발생시키려면, 이벤트 클래스의 정적 `dispatch` 메서드를 호출하세요. 이 메서드는 `Illuminate\Foundation\Events\Dispatchable` 트레이트에서 제공합니다. `dispatch`에 넘긴 인수는 이벤트 생성자에 전달됩니다:

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
     * 주문을 배송 처리합니다.
     */
    public function store(Request $request): RedirectResponse
    {
        $order = Order::findOrFail($request->order_id);

        // 주문 배송 처리 로직...

        OrderShipped::dispatch($order);

        return redirect('/orders');
    }
}
```

조건에 따라 이벤트를 디스패치하려면 `dispatchIf`, `dispatchUnless` 메서드를 사용할 수 있습니다:

```php
OrderShipped::dispatchIf($condition, $order);

OrderShipped::dispatchUnless($condition, $order);
```

> [!NOTE]  
> 테스트 시에는 이벤트를 실제로 발생시키지 않고도 이벤트가 디스패치됐는지 검증할 수 있는 Laravel 내장 테스트 도우미를 활용하면 편리합니다.

<a name="dispatching-events-after-database-transactions"></a>
### 데이터베이스 트랜잭션 이후 이벤트 디스패치

활성화된 데이터베이스 트랜잭션이 커밋된 이후에만 이벤트를 발생시키고 싶다면 이벤트 클래스에 `ShouldDispatchAfterCommit` 인터페이스를 구현하세요.

이 인터페이스를 적용하면, 현재 트랜잭션이 커밋될 때까지 이벤트가 디스패치되지 않고, 트랜잭션 실패 시 이벤트는 무시됩니다. 트랜잭션이 없다면 즉시 이벤트가 디스패치됩니다:

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
     * 새 이벤트 인스턴스 생성
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

이벤트 구독자 클래스는 여러 이벤트를 한 곳에서 구독하도록 해 여러 이벤트 핸들러를 한 클래스로 정의할 수 있습니다. 구독자는 `subscribe` 메서드를 정의하며, 이 메서드는 이벤트 디스패처 인스턴스를 인자로 받습니다. 전달 받은 디스패처의 `listen` 메서드를 호출해 이벤트 리스너를 등록할 수 있습니다:

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
     * 구독자 리스너 등록
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

이벤트 리스너 메서드가 구독자 안에 직접 정의되어 있다면, `subscribe` 메서드에서 이벤트와 메서드명을 배열로 반환하는 방식이 더 편리합니다. Laravel은 이 경우 자동으로 클래스 이름을 판단해 리스너를 등록합니다:

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
     * 구독자 리스너 등록
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

구독자를 작성한 이후에는, 구독자 내부 핸들러 메서드가 Laravel의 [이벤트 탐지 규칙](#event-discovery)에 부합하면 자동 등록됩니다. 그렇지 않다면, `Event` 파사드의 `subscribe` 메서드로 수동 등록해야 합니다. 보통 `AppServiceProvider`의 `boot` 메서드에서 수행합니다:

```php
<?php

namespace App\Providers;

use App\Listeners\UserEventSubscriber;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 부트스트랩
     */
    public function boot(): void
    {
        Event::subscribe(UserEventSubscriber::class);
    }
}
```

<a name="testing"></a>
## 테스트

이벤트를 디스패치하는 코드를 테스트할 때, 리스너가 실제로 실행되지 않도록 지시할 수 있습니다. 리스너 코드는 별도로 직접 인스턴스를 생성해 `handle` 메서드를 호출하며 테스트할 수 있습니다.

`Event` 파사드의 `fake` 메서드를 사용해 리스너 실행을 막고, 테스트 대상 코드를 수행한 후 어떤 이벤트가 디스패치됐는지 `assertDispatched`, `assertNotDispatched`, `assertNothingDispatched` 메서드로 검증할 수 있습니다:

```php tab=Pest
<?php

use App\Events\OrderFailedToShip;
use App\Events\OrderShipped;
use Illuminate\Support\Facades\Event;

test('orders can be shipped', function () {
    Event::fake();

    // 주문 배송 처리...

    // 이벤트가 디스패치됐는지 검증
    Event::assertDispatched(OrderShipped::class);

    // 이벤트가 두 번 디스패치됐는지 검증
    Event::assertDispatched(OrderShipped::class, 2);

    // 특정 이벤트가 디스패치되지 않았는지 검증
    Event::assertNotDispatched(OrderFailedToShip::class);

    // 이벤트가 전혀 디스패치되지 않았는지 검증
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
     * 주문 배송 테스트
     */
    public function test_orders_can_be_shipped(): void
    {
        Event::fake();

        // 주문 배송 처리...

        // 이벤트 디스패치 검증
        Event::assertDispatched(OrderShipped::class);

        // 두 번 디스패치 검증
        Event::assertDispatched(OrderShipped::class, 2);

        // 특정 이벤트 비디스패치 검증
        Event::assertNotDispatched(OrderFailedToShip::class);

        // 이벤트 미디스패치 검증
        Event::assertNothingDispatched();
    }
}
```

`assertDispatched` 또는 `assertNotDispatched` 메서드에 클로저를 전달해 조건을 만족하는 이벤트가 디스패치됐는지 검증할 수 있습니다. 조건에 맞는 이벤트가 한 번이라도 디스패치되면 검증이 성공합니다:

```php
Event::assertDispatched(function (OrderShipped $event) use ($order) {
    return $event->order->id === $order->id;
});
```

특정 이벤트를 리스너가 청취하는지 확인하려면 `assertListening`을 사용할 수 있습니다:

```php
Event::assertListening(
    OrderShipped::class,
    SendShipmentNotification::class
);
```

> [!WARNING]  
> `Event::fake()` 호출 이후에는 이벤트 리스너들이 실행되지 않습니다. 만약 모델의 `creating` 이벤트 등 이벤트 의존성이 있는 팩토리를 사용한다면, `Event::fake()`를 팩토리 호출 **후에** 호출해야 합니다.

<a name="faking-a-subset-of-events"></a>
### 일부 이벤트만 가짜 처리하기

특정 이벤트만 가짜 처리하려면 `fake` 또는 `fakeFor` 메서드에 대상 이벤트 배열을 전달하세요:

```php tab=Pest
test('orders can be processed', function () {
    Event::fake([
        OrderCreated::class,
    ]);

    $order = Order::factory()->create();

    Event::assertDispatched(OrderCreated::class);

    // 나머지 이벤트는 정상적으로 디스패치됩니다...
    $order->update([...]);
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

    // 나머지 이벤트는 정상적으로 디스패치됩니다...
    $order->update([...]);
}
```

`except` 메서드로 특정 이벤트만 제외하고 나머지는 모두 가짜 처리할 수도 있습니다:

```php
Event::fake()->except([
    OrderCreated::class,
]);
```

<a name="scoped-event-fakes"></a>
### 범위 지정 이벤트 가짜 처리

테스트 일부분에 대해서만 이벤트 리스너를 가짜 처리하고 싶다면 `fakeFor` 메서드를 사용하세요:

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

    // 이후부터는 이벤트가 정상적으로 디스패치되고 옵저버도 실행됩니다...
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
     * 주문 처리 테스트
     */
    public function test_orders_can_be_processed(): void
    {
        $order = Event::fakeFor(function () {
            $order = Order::factory()->create();

            Event::assertDispatched(OrderCreated::class);

            return $order;
        });

        // 이후부터는 이벤트가 정상적으로 디스패치되고 옵저버도 실행됩니다...
        $order->update([...]);
    }
}
```