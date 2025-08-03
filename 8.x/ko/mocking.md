# 모킹 (Mocking)

- [소개](#introduction)
- [객체 모킹](#mocking-objects)
- [파사드 모킹](#mocking-facades)
    - [파사드 스파이](#facade-spies)
- [Bus Fake](#bus-fake)
    - [작업 체인](#bus-job-chains)
    - [작업 배치](#job-batches)
- [Event Fake](#event-fake)
    - [범위 지정 이벤트 페이크](#scoped-event-fakes)
- [HTTP Fake](#http-fake)
- [Mail Fake](#mail-fake)
- [Notification Fake](#notification-fake)
- [Queue Fake](#queue-fake)
    - [작업 체인](#job-chains)
- [Storage Fake](#storage-fake)
- [시간 다루기](#interacting-with-time)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel 애플리케이션을 테스트할 때, 실제로 실행되지 않도록 특정 부분을 "모킹(mock)"하고 싶을 수 있습니다. 예를 들어, 이벤트를 디스패치하는 컨트롤러를 테스트할 때 이벤트 리스너가 실제로 실행되지 않도록 모킹하면, 이벤트 리스너의 실행에 신경 쓰지 않고 컨트롤러의 HTTP 응답만 테스트할 수 있습니다. 이벤트 리스너 자체는 별도의 테스트 케이스에서 테스트하면 되기 때문입니다.

Laravel은 이벤트, 작업(job), 기타 파사드를 모킹할 수 있는 편리한 메서드를 기본 제공하며, 이 헬퍼들은 주로 Mockery의 복잡한 메서드 호출을 직접 하지 않아도 되도록 편의를 제공합니다.

<a name="mocking-objects"></a>
## 객체 모킹 (Mocking Objects)

Laravel의 [서비스 컨테이너](/docs/{{version}}/container)를 통해 주입될 객체를 모킹할 때는, 컨테이너에 모킹된 인스턴스를 `instance` 바인딩으로 직접 등록해야 합니다. 이렇게 하면 컨테이너가 객체를 직접 생성하는 대신, 모킹된 인스턴스를 사용하도록 지시할 수 있습니다:

```
use App\Service;
use Mockery;
use Mockery\MockInterface;

public function test_something_can_be_mocked()
{
    $this->instance(
        Service::class,
        Mockery::mock(Service::class, function (MockInterface $mock) {
            $mock->shouldReceive('process')->once();
        })
    );
}
```

더 편리하게 하기 위해 Laravel의 기본 테스트 클래스에 제공되는 `mock` 메서드를 사용할 수도 있습니다. 아래 예시는 위 예제와 동일합니다:

```
use App\Service;
use Mockery\MockInterface;

$mock = $this->mock(Service::class, function (MockInterface $mock) {
    $mock->shouldReceive('process')->once();
});
```

특정 객체의 몇몇 메서드만 모킹해야 할 경우에는 `partialMock` 메서드를 사용할 수 있습니다. 모킹되지 않은 메서드는 호출되면 원래대로 실행됩니다:

```
use App\Service;
use Mockery\MockInterface;

$mock = $this->partialMock(Service::class, function (MockInterface $mock) {
    $mock->shouldReceive('process')->once();
});
```

비슷하게, 객체를 [스파이(Spy)](http://docs.mockery.io/en/latest/reference/spies.html)하고자 할 경우, Laravel의 기본 테스트 클래스에서 `Mockery::spy` 메서드의 편리한 래퍼인 `spy` 메서드를 제공합니다. 스파이는 모킹과 유사하지만, 코드 실행 후 스파이와의 모든 상호작용을 기록하여 검증할 수 있게 해줍니다:

```
use App\Service;

$spy = $this->spy(Service::class);

// ...

$spy->shouldHaveReceived('process');
```

<a name="mocking-facades"></a>
## 파사드 모킹 (Mocking Facades)

전통적인 정적 메서드 호출과 달리, [파사드](/docs/{{version}}/facades) (실시간 파사드 포함 [real-time facades](/docs/{{version}}/facades#real-time-facades))는 모킹할 수 있습니다. 이는 전통적인 정적 메서드 대비 큰 테스트 용이성을 제공하며, 의존성 주입을 사용하는 것과 유사한 수준의 테스트 편의성을 부여합니다. 테스트 시, 컨트롤러 등에서 호출되는 Laravel 파사드 메서드를 모킹하고 싶을 때가 많습니다. 예를 들어 다음 컨트롤러 액션을 보겠습니다:

```
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Cache;

class UserController extends Controller
{
    /**
     * 애플리케이션의 모든 사용자 목록을 조회합니다.
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        $value = Cache::get('key');

        //
    }
}
```

`Cache` 파사드의 호출을 `shouldReceive` 메서드를 사용해 모킹하면, Mockery의 모킹 인스턴스가 반환됩니다. 파사드는 실제로 Laravel [서비스 컨테이너](/docs/{{version}}/container)에서 해석되고 관리되기 때문에 일반적인 정적 클래스보다 훨씬 테스트하기 쉽습니다. 예를 들어 `Cache` 파사드의 `get` 메서드 호출을 모킹해 봅시다:

```
<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Illuminate\Support\Facades\Cache;
use Tests\TestCase;

class UserControllerTest extends TestCase
{
    public function testGetIndex()
    {
        Cache::shouldReceive('get')
                    ->once()
                    ->with('key')
                    ->andReturn('value');

        $response = $this->get('/users');

        // ...
    }
}
```

> [!NOTE]
> `Request` 파사드는 모킹하지 마십시오. 대신 테스트 실행 시 `get`, `post` 등의 [HTTP 테스트 메서드](/docs/{{version}}/http-tests)에 원하는 입력을 전달하세요. 마찬가지로, `Config` 파사드를 모킹하지 말고, 테스트에서 `Config::set` 메서드를 호출하세요.

<a name="facade-spies"></a>
### 파사드 스파이 (Facade Spies)

파사드를 [스파이](http://docs.mockery.io/en/latest/reference/spies.html)하고자 한다면, 해당 파사드에서 `spy` 메서드를 호출할 수 있습니다. 스파이는 모킹과 유사하지만, 코드 실행 후 스파이와 코드 간의 모든 상호작용을 기록해 검증을 가능하게 합니다:

```
use Illuminate\Support\Facades\Cache;

public function test_values_are_be_stored_in_cache()
{
    Cache::spy();

    $response = $this->get('/');

    $response->assertStatus(200);

    Cache::shouldHaveReceived('put')->once()->with('name', 'Taylor', 10);
}
```

<a name="bus-fake"></a>
## Bus Fake

작업(job)을 디스패치하는 코드를 테스트할 때, 특정 작업이 디스패치 됐다는 것만 검증하고 실제로 작업을 큐에 넣거나 실행시키지 않으려는 경우가 많습니다. 작업 실행은 일반적으로 별도의 테스트 클래스에서 진행되기 때문입니다.

`Bus` 파사드의 `fake` 메서드를 사용해 작업이 큐에 디스패치 되는 것을 막을 수 있습니다. 이후 테스트 대상 코드를 실행한 뒤, `assertDispatched`, `assertNotDispatched` 메서드를 사용해 어떤 작업이 디스패치 되었는지 검증할 수 있습니다:

```
<?php

namespace Tests\Feature;

use App\Jobs\ShipOrder;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Illuminate\Support\Facades\Bus;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_orders_can_be_shipped()
    {
        Bus::fake();

        // 주문 배송 처리...

        // 작업이 디스패치 되었는지 검증...
        Bus::assertDispatched(ShipOrder::class);

        // 작업이 디스패치 되지 않았는지 검증...
        Bus::assertNotDispatched(AnotherJob::class);

        // 동기 방식으로 작업이 디스패치 되었는지 검증...
        Bus::assertDispatchedSync(AnotherJob::class);

        // 동기 방식으로 작업이 디스패치 되지 않았는지 검증...
        Bus::assertNotDispatchedSync(AnotherJob::class);

        // 응답 후 작업이 디스패치 되었는지 검증...
        Bus::assertDispatchedAfterResponse(AnotherJob::class);

        // 응답 후 작업이 디스패치 되지 않았는지 검증...
        Bus::assertNotDispatchedAfterResponse(AnotherJob::class);

        // 어떤 작업도 디스패치 되지 않았음을 검증...
        Bus::assertNothingDispatched();
    }
}
```

검증 메서드들에는 클로저를 전달할 수 있는데, 전달된 클로저를 통해 인자로 받은 작업이 조건을 만족하는지 검사할 수 있습니다. 조건을 만족하는 작업이 하나라도 있으면 검증에 성공합니다. 예를 들어 특정 주문에 대한 작업이 디스패치 되었는지 검증하는 경우입니다:

```
Bus::assertDispatched(function (ShipOrder $job) use ($order) {
    return $job->order->id === $order->id;
});
```

<a name="bus-job-chains"></a>
### 작업 체인 (Job Chains)

`Bus` 파사드의 `assertChained` 메서드로 [작업 체인](/docs/{{version}}/queues#job-chaining)이 디스패치 되었는지 확인할 수 있습니다. 첫 번째 인자로 체인 작업 배열을 받습니다:

```
use App\Jobs\RecordShipment;
use App\Jobs\ShipOrder;
use App\Jobs\UpdateInventory;
use Illuminate\Support\Facades\Bus;

Bus::assertChained([
    ShipOrder::class,
    RecordShipment::class,
    UpdateInventory::class
]);
```

위 예시처럼 체인 작업은 작업 클래스 이름의 배열이 될 수 있습니다. 실제 작업 인스턴스 배열도 전달할 수 있고, 이 경우 Laravel은 실제 디스패치된 체인 작업들이 같은 클래스이고 속성값도 일치하는지 검사합니다:

```
Bus::assertChained([
    new ShipOrder,
    new RecordShipment,
    new UpdateInventory,
]);
```

<a name="job-batches"></a>
### 작업 배치 (Job Batches)

`Bus` 파사드의 `assertBatched` 메서드로 [작업 배치](/docs/{{version}}/queues#job-batching)가 디스패치 되었는지 확인할 수 있습니다. `assertBatched`에 전달된 클로저에는 `Illuminate\Bus\PendingBatch` 인스턴스가 전달되며, 배치 내 작업들을 검사할 수 있습니다:

```
use Illuminate\Bus\PendingBatch;
use Illuminate\Support\Facades\Bus;

Bus::assertBatched(function (PendingBatch $batch) {
    return $batch->name == 'import-csv' &&
           $batch->jobs->count() === 10;
});
```

<a name="event-fake"></a>
## Event Fake

이벤트를 디스패치하는 코드를 테스트할 때, 이벤트 리스너가 실제로 실행되지 않도록 할 수 있습니다. `Event` 파사드의 `fake` 메서드를 사용해 리스너 실행을 막은 뒤, 테스트할 코드를 실행하고, `assertDispatched`, `assertNotDispatched`, `assertNothingDispatched` 메서드를 통해 어떤 이벤트가 디스패치 됐는지 검증할 수 있습니다:

```
<?php

namespace Tests\Feature;

use App\Events\OrderFailedToShip;
use App\Events\OrderShipped;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Illuminate\Support\Facades\Event;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * 주문 배송 테스트.
     */
    public function test_orders_can_be_shipped()
    {
        Event::fake();

        // 주문 배송 처리...

        // 이벤트 디스패치 여부 검증...
        Event::assertDispatched(OrderShipped::class);

        // 이벤트가 두 번 디스패치 되었는지 검증...
        Event::assertDispatched(OrderShipped::class, 2);

        // 이벤트가 디스패치 되지 않았는지 검증...
        Event::assertNotDispatched(OrderFailedToShip::class);

        // 어떤 이벤트도 디스패치 되지 않았는지 검증...
        Event::assertNothingDispatched();
    }
}
```

`assertDispatched` 및 `assertNotDispatched` 메서드에 클로저를 전달해, 전달받은 이벤트가 특정 조건을 만족하는지 검사할 수 있습니다. 조건을 만족하는 이벤트가 하나라도 디스패치 되면 검증은 성공합니다:

```
Event::assertDispatched(function (OrderShipped $event) use ($order) {
    return $event->order->id === $order->id;
});
```

간단히 특정 이벤트에 리스너가 등록되어 있는지만 검증하고 싶다면 `assertListening` 메서드를 사용할 수 있습니다:

```
Event::assertListening(
    OrderShipped::class,
    SendShipmentNotification::class
);
```

> [!NOTE]
> `Event::fake()`를 호출하면 이후에는 이벤트 리스너가 실행되지 않습니다. 따라서, 예를 들어 모델의 `creating` 이벤트에서 UUID 생성 같은 작업을 실행하는 모델 팩토리를 사용한다면, `Event::fake()` 호출은 팩토리를 사용한 후에 해야 합니다.

<a name="faking-a-subset-of-events"></a>
#### 일부 이벤트만 페이크하기

특정 이벤트들에 대해서만 리스너 실행을 막고 싶으면, `fake` 또는 `fakeFor` 메서드에 이벤트 클래스를 배열로 전달할 수 있습니다:

```
/**
 * 주문 처리 테스트.
 */
public function test_orders_can_be_processed()
{
    Event::fake([
        OrderCreated::class,
    ]);

    $order = Order::factory()->create();

    Event::assertDispatched(OrderCreated::class);

    // 나머지 이벤트는 평소처럼 디스패치됨...
    $order->update([...]);
}
```

<a name="scoped-event-fakes"></a>
### 범위 지정 이벤트 페이크 (Scoped Event Fakes)

테스트 중 특정 코드 구간에 대해서만 이벤트 리스너 실행을 막고 싶다면 `fakeFor` 메서드를 사용할 수 있습니다:

```
<?php

namespace Tests\Feature;

use App\Events\OrderCreated;
use App\Models\Order;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\Event;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * 주문 처리 테스트.
     */
    public function test_orders_can_be_processed()
    {
        $order = Event::fakeFor(function () {
            $order = Order::factory()->create();

            Event::assertDispatched(OrderCreated::class);

            return $order;
        });

        // 이후에는 이벤트가 정상적으로 디스패치되고 옵저버도 실행됨...
        $order->update([...]);
    }
}
```

<a name="http-fake"></a>
## HTTP Fake

`Http` 파사드의 `fake` 메서드를 사용하면 HTTP 클라이언트 요청 시 더미 또는 스텁된 응답을 반환하도록 할 수 있습니다. 외부 HTTP 요청을 페이크하는 자세한 내용은 [HTTP 클라이언트 테스트 문서](/docs/{{version}}/http-client#testing)를 참고하세요.

<a name="mail-fake"></a>
## Mail Fake

`Mail` 파사드의 `fake` 메서드를 통해 메일 전송을 막을 수 있습니다. 일반적으로 메일 발송 자체는 테스트 대상 코드와 무관한 경우가 많으므로, Laravel이 특정 메일러블(mailable)을 전송하도록 지시했는지만 검증하는 것이 적절합니다.

`Mail::fake()` 호출 후, 메일러블이 사용자에게 전송되었는지 확인할 수 있고, 전달된 데이터도 검사할 수 있습니다:

```
<?php

namespace Tests\Feature;

use App\Mail\OrderShipped;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Illuminate\Support\Facades\Mail;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_orders_can_be_shipped()
    {
        Mail::fake();

        // 주문 배송 처리...

        // 메일러블이 전송되지 않았음을 검증...
        Mail::assertNothingSent();

        // 특정 메일러블이 전송되었음을 검증...
        Mail::assertSent(OrderShipped::class);

        // 두 번 전송되었음 검증...
        Mail::assertSent(OrderShipped::class, 2);

        // 메일러블이 전송되지 않았음을 검증...
        Mail::assertNotSent(AnotherMailable::class);
    }
}
```

메일러블을 백그라운드 큐에 넣어 전송하는 경우, `assertSent` 대신 `assertQueued` 메서드를 사용하세요:

```
Mail::assertQueued(OrderShipped::class);

Mail::assertNotQueued(OrderShipped::class);

Mail::assertNothingQueued();
```

검증 메서드들에 클로저를 전달해, 메일러블 인스턴스가 특정 조건을 만족하는지 검사할 수 있습니다. 해당 조건을 만족하는 메일러블이 하나라도 전송되면 성공합니다:

```
Mail::assertSent(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

`Mail` 파사드의 검증 메서드에 전달하는 클로저에서, 메일러블 인스턴스는 수신자 검사를 위한 편리한 메서드도 제공합니다:

```
Mail::assertSent(OrderShipped::class, function ($mail) use ($user) {
    return $mail->hasTo($user->email) &&
           $mail->hasCc('...') &&
           $mail->hasBcc('...');
});
```

메일 전송이 안 되었음을 검증하는 메서드는 `assertNotSent`와 `assertNotQueued` 두 종류가 있습니다. 때로는 메일이 전송되거나 큐에 넣어지지 않았음을 한꺼번에 검증하고 싶을 수 있는데, 이때는 `assertNothingOutgoing` 및 `assertNotOutgoing` 메서드를 사용할 수 있습니다:

```
Mail::assertNothingOutgoing();

Mail::assertNotOutgoing(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

<a name="notification-fake"></a>
## Notification Fake

`Notification` 파사드의 `fake` 메서드를 사용해 알림 전송을 차단할 수 있습니다. 일반적으로 알림 전송 자체는 테스트 대상 로직과 관련 없는 경우가 많아, Laravel이 특정 알림을 보내도록 지시했는지만 검증하는 것으로 충분합니다.

`Notification::fake()` 호출 후, [알림](/docs/{{version}}/notifications)이 사용자에게 전송 지시되었는지, 또 알림에 전달된 데이터까지 검사할 수 있습니다:

```
<?php

namespace Tests\Feature;

use App\Notifications\OrderShipped;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Illuminate\Support\Facades\Notification;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_orders_can_be_shipped()
    {
        Notification::fake();

        // 주문 배송 처리...

        // 알림이 전송되지 않았음을 검증...
        Notification::assertNothingSent();

        // 특정 사용자에게 알림이 전송되었음을 검증...
        Notification::assertSentTo(
            [$user], OrderShipped::class
        );

        // 알림이 전송되지 않았음을 검증...
        Notification::assertNotSentTo(
            [$user], AnotherNotification::class
        );
    }
}
```

`assertSentTo`, `assertNotSentTo` 검증 메서드에 클로저를 전달해, 알림과 채널이 조건을 만족하는지 검사할 수 있습니다. 조건을 만족하는 알림이 하나라도 전송되면 검증은 성공합니다:

```
Notification::assertSentTo(
    $user,
    function (OrderShipped $notification, $channels) use ($order) {
        return $notification->order->id === $order->id;
    }
);
```

<a name="on-demand-notifications"></a>
#### 온디맨드 알림 (On-Demand Notifications)

테스트 대상 코드가 [온디맨드 알림](/docs/{{version}}/notifications#on-demand-notifications)을 보내는 경우, `Illuminate\Notifications\AnonymousNotifiable` 인스턴스에 전송됐는지를 검증해야 합니다:

```
use Illuminate\Notifications\AnonymousNotifiable;

Notification::assertSentTo(
    new AnonymousNotifiable, OrderShipped::class
);
```

알림 검증 메서드에 세 번째 인수로 클로저를 넘겨 온디맨드 알림이 올바른 "라우트" 주소로 전송됐는지 확인할 수도 있습니다:

```
Notification::assertSentTo(
    new AnonymousNotifiable,
    OrderShipped::class,
    function ($notification, $channels, $notifiable) use ($user) {
        return $notifiable->routes['mail'] === $user->email;
    }
);
```

<a name="queue-fake"></a>
## Queue Fake

`Queue` 파사드의 `fake` 메서드로 큐 작업이 실제로 큐에 들어가지 않도록 할 수 있습니다. 대부분 큐 작업은 별도의 테스트 클래스에서 점검하므로, 단순히 특정 작업이 큐에 푸시되었는지만 검증하면 충분합니다.

`Queue::fake()` 호출 후, 애플리케이션이 큐에 작업을 푸시했는지 검증할 수 있습니다:

```
<?php

namespace Tests\Feature;

use App\Jobs\AnotherJob;
use App\Jobs\FinalJob;
use App\Jobs\ShipOrder;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Illuminate\Support\Facades\Queue;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_orders_can_be_shipped()
    {
        Queue::fake();

        // 주문 배송 처리...

        // 큐에 아무 작업도 푸시되지 않았음을 검증...
        Queue::assertNothingPushed();

        // 특정 큐에 작업이 푸시되었음을 검증...
        Queue::assertPushedOn('queue-name', ShipOrder::class);

        // 두 번 작업이 푸시되었음을 검증...
        Queue::assertPushed(ShipOrder::class, 2);

        // 작업이 푸시되지 않았음을 검증...
        Queue::assertNotPushed(AnotherJob::class);
    }
}
```

`assertPushed`, `assertNotPushed` 메서드에 클로저를 넘겨 작업 인스턴스가 조건을 만족하는지 확인할 수도 있습니다:

```
Queue::assertPushed(function (ShipOrder $job) use ($order) {
    return $job->order->id === $order->id;
});
```

<a name="job-chains"></a>
### 작업 체인 (Job Chains)

`Queue` 파사드의 `assertPushedWithChain`, `assertPushedWithoutChain` 메서드로 푸시된 작업의 체인을 검사할 수 있습니다. `assertPushedWithChain`은 첫 번째 인자로 주 작업, 두 번째 인자로 체인 작업 배열을 받습니다:

```
use App\Jobs\RecordShipment;
use App\Jobs\ShipOrder;
use App\Jobs\UpdateInventory;
use Illuminate\Support\Facades\Queue;

Queue::assertPushedWithChain(ShipOrder::class, [
    RecordShipment::class,
    UpdateInventory::class
]);
```

체인 작업은 클래스 이름 배열도 되고 실제 작업 인스턴스 배열도 가능합니다. 후자일 경우 Laravel은 클래스와 속성값 일치를 검사합니다:

```
Queue::assertPushedWithChain(ShipOrder::class, [
    new RecordShipment,
    new UpdateInventory,
]);
```

`assertPushedWithoutChain` 메서드는 작업이 체인 없이 푸시되었는지 검증합니다:

```
Queue::assertPushedWithoutChain(ShipOrder::class);
```

<a name="storage-fake"></a>
## Storage Fake

`Storage` 파사드의 `fake` 메서드는 임시 가짜 디스크를 생성해 파일 업로드 테스트를 쉽게 해줍니다. `Illuminate\Http\UploadedFile` 클래스의 파일 생성 유틸리티와 함께 사용하면 매우 편리합니다. 예를 들어:

```
<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_albums_can_be_uploaded()
    {
        Storage::fake('photos');

        $response = $this->json('POST', '/photos', [
            UploadedFile::fake()->image('photo1.jpg'),
            UploadedFile::fake()->image('photo2.jpg')
        ]);

        // 하나 이상의 파일이 저장되었음을 검증...
        Storage::disk('photos')->assertExists('photo1.jpg');
        Storage::disk('photos')->assertExists(['photo1.jpg', 'photo2.jpg']);

        // 저장되지 않은 파일이 있음을 검증...
        Storage::disk('photos')->assertMissing('missing.jpg');
        Storage::disk('photos')->assertMissing(['missing.jpg', 'non-existing.jpg']);
    }
}
```

파일 업로드 테스트에 관한 자세한 내용은 [HTTP 테스트 문서의 파일 업로드 섹션](/docs/{{version}}/http-tests#testing-file-uploads)을 참고하십시오.

> [!TIP]
> 기본적으로 `fake` 메서드는 임시 디렉터리 내 모든 파일을 삭제합니다. 임시 파일을 보존하고 싶다면 `persistentFake` 메서드를 사용하세요.

<a name="interacting-with-time"></a>
## 시간 다루기 (Interacting With Time)

테스트 시, `now`나 `Illuminate\Support\Carbon::now()` 같은 헬퍼를 통해 반환되는 현재 시간을 조작해야 하는 경우가 있습니다. 다행히 Laravel의 기본 기능 테스트 클래스에는 현재 시간을 쉽게 조작할 수 있는 헬퍼 메서드들이 포함되어 있습니다:

```
public function testTimeCanBeManipulated()
{
    // 미래 시간으로 이동...
    $this->travel(5)->milliseconds();
    $this->travel(5)->seconds();
    $this->travel(5)->minutes();
    $this->travel(5)->hours();
    $this->travel(5)->days();
    $this->travel(5)->weeks();
    $this->travel(5)->years();

    // 과거 시간으로 이동...
    $this->travel(-5)->hours();

    // 특정 시점으로 이동...
    $this->travelTo(now()->subHours(6));

    // 현재 시간으로 복귀...
    $this->travelBack();
}
```