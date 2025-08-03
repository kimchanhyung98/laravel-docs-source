# Mocking (모킹)

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
- [메일 페이크](#mail-fake)
- [Notification Fake](#notification-fake)
- [Queue Fake](#queue-fake)
    - [작업 체인](#job-chains)
- [Storage Fake](#storage-fake)
- [시간 조작](#interacting-with-time)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel 애플리케이션을 테스트할 때, 특정 부분을 "모킹(mock)"하여 테스트 중 실제로 실행되지 않도록 할 수 있습니다. 예를 들어, 이벤트를 디스패치하는 컨트롤러를 테스트할 때 이벤트 리스너가 실제로 실행되지 않도록 모킹하여 컨트롤러의 HTTP 응답만 테스트할 수 있습니다. 이벤트 리스너는 별도의 테스트에서 개별적으로 검증할 수 있기 때문입니다.

Laravel은 이벤트, 작업(job), 기타 파사드들을 손쉽게 모킹할 수 있는 메서드를 기본으로 제공합니다. 이 헬퍼들은 복잡한 Mockery 호출 없이 간편하게 사용할 수 있도록 Mockery 위에 편리한 추상화를 추가한 것입니다.

<a name="mocking-objects"></a>
## 객체 모킹 (Mocking Objects)

Laravel [서비스 컨테이너](/docs/9.x/container)를 통해 애플리케이션에 주입될 객체를 모킹할 경우, 모킹된 인스턴스를 `instance` 바인딩으로 컨테이너에 바인딩해야 합니다. 이렇게 하면 컨테이너가 객체를 직접 생성하는 대신 모킹된 인스턴스를 사용하게 됩니다:

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

더 편리하게 하려면 Laravel 기본 테스트 케이스 클래스에서 제공하는 `mock` 메서드를 사용할 수 있습니다. 다음 예제는 위의 코드와 동일한 기능을 합니다:

```
use App\Service;
use Mockery\MockInterface;

$mock = $this->mock(Service::class, function (MockInterface $mock) {
    $mock->shouldReceive('process')->once();
});
```

객체의 일부 메서드만 모킹하고 싶을 때는 `partialMock` 메서드를 사용하세요. 모킹하지 않은 메서드는 호출 시 정상적으로 실행됩니다:

```
use App\Service;
use Mockery\MockInterface;

$mock = $this->partialMock(Service::class, function (MockInterface $mock) {
    $mock->shouldReceive('process')->once();
});
```

동일하게, 객체에 대해 [스파이(spy)](http://docs.mockery.io/en/latest/reference/spies.html)를 만들고 싶다면 기본 테스트 케이스의 `spy` 메서드를 사용할 수 있습니다. 스파이는 모킹과 비슷하지만, 테스트 대상 코드와의 모든 상호작용을 기록하여 코드 실행 후 검증이 가능합니다:

```
use App\Service;

$spy = $this->spy(Service::class);

// ...

$spy->shouldHaveReceived('process');
```

<a name="mocking-facades"></a>
## 파사드 모킹 (Mocking Facades)

기존의 정적 메서드 호출과 달리, [파사드](/docs/9.x/facades) (실시간 파사드 포함)도 모킹할 수 있습니다. 이는 전통적인 의존성 주입 방식과 동등한 수준의 테스트 가능성을 제공합니다. 예를 들어, 컨트롤러 내에서 Laravel 파사드 호출을 모킹하려 할 때가 많습니다. 다음은 그런 컨트롤러 액션 예제입니다:

```
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Cache;

class UserController extends Controller
{
    /**
     * 애플리케이션의 모든 사용자 목록을 가져옵니다.
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

`Cache` 파사드 호출을 `shouldReceive` 메서드로 모킹할 수 있으며, 이는 [Mockery](https://github.com/padraic/mockery) 모킹 인스턴스를 반환합니다. 파사드는 Laravel [서비스 컨테이너](/docs/9.x/container)에서 해결되고 관리되므로, 일반적인 정적 클래스보다 테스트가 훨씬 용이합니다. 예를 들어 `Cache`의 `get` 메서드를 다음과 같이 모킹할 수 있습니다:

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

> [!WARNING]
> `Request` 파사드는 모킹하지 마십시오. 테스트 시 입력값은 `get`, `post` 등 [HTTP 테스트 메서드](/docs/9.x/http-tests)에 직접 전달하세요. 마찬가지로 `Config` 파사드를 모킹하지 말고 테스트 내에서 `Config::set` 메서드를 호출하는 방식으로 설정하세요.

<a name="facade-spies"></a>
### 파사드 스파이 (Facade Spies)

파사드에 대해 [스파이(spy)](http://docs.mockery.io/en/latest/reference/spies.html)를 만들고 싶다면 해당 파사드에서 `spy` 메서드를 호출하세요. 스파이는 모킹처럼 동작하지만 코드 실행 후 호출 기록을 기반으로 검증할 수 있습니다:

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

작업(job)을 디스패치하는 코드를 테스트할 때, 보통 해당 작업이 큐에 추가되었는지만 검증하고 실제 큐잉이나 실행은 하지 않게 합니다. 작업 실행 자체는 별도의 테스트 클래스에서 검증할 수 있기 때문입니다.

`Bus` 파사드의 `fake` 메서드를 사용하면 작업의 큐 디스패치를 방지할 수 있습니다. 테스트 대상 코드를 실행한 후 `assertDispatched`, `assertNotDispatched` 등의 메서드로 어떤 작업이 디스패치되었는지 확인할 수 있습니다:

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

        // 주문 배송 수행...

        // 작업이 디스패치되었는지 검증...
        Bus::assertDispatched(ShipOrder::class);

        // 작업이 디스패치되지 않았는지 검증...
        Bus::assertNotDispatched(AnotherJob::class);

        // 작업이 동기 호출되었는지 검증...
        Bus::assertDispatchedSync(AnotherJob::class);

        // 작업이 동기 호출되지 않았는지 검증...
        Bus::assertNotDispatchedSync(AnotherJob::class);

        // 응답 이후 작업이 디스패치되었는지 검증...
        Bus::assertDispatchedAfterResponse(AnotherJob::class);

        // 응답 이후 작업이 디스패치되지 않았는지 검증...
        Bus::assertNotDispatchedAfterResponse(AnotherJob::class);

        // 작업이 전혀 디스패치되지 않았는지 검증...
        Bus::assertNothingDispatched();
    }
}
```

검증 메서드들에 클로저를 전달하면, 특정 조건을 만족하는 작업이 디스패치되었는지를 테스트할 수 있습니다. 예를 들어, 특정 주문에 대한 작업이 디스패치되었는지 검증하려면:

```
Bus::assertDispatched(function (ShipOrder $job) use ($order) {
    return $job->order->id === $order->id;
});
```

<a name="faking-a-subset-of-jobs"></a>
#### 일부 작업만 페이크하기

특정 작업만 페이크하고 싶으면 `fake` 메서드에 모킹할 작업 클래스를 배열로 전달하세요:

```
/**
 * 주문 처리 테스트.
 */
public function test_orders_can_be_shipped()
{
    Bus::fake([
        ShipOrder::class,
    ]);

    // ...
}
```

반대로, 특정 작업만 제외하고 나머지를 모두 모킹하려면 `except` 메서드를 사용합니다:

```
Bus::fake()->except([
    ShipOrder::class,
]);
```

<a name="bus-job-chains"></a>
### 작업 체인 (Job Chains)

`Bus` 파사드의 `assertChained` 메서드를 사용하면 [작업 체인](/docs/9.x/queues#job-chaining)이 디스패치되었는지 검증할 수 있습니다. 첫 번째 인수로 체인 작업 배열을 받습니다:

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

체인 작업 배열은 클래스명 배열일 수도 있고, 실제 작업 인스턴스 배열일 수도 있습니다. 인스턴스를 넘기면 Laravel은 클래스와 프로퍼티 값이 동일한지 검사합니다:

```
Bus::assertChained([
    new ShipOrder,
    new RecordShipment,
    new UpdateInventory,
]);
```

<a name="job-batches"></a>
### 작업 배치 (Job Batches)

`Bus` 파사드의 `assertBatched` 메서드를 사용하면 [작업 배치](/docs/9.x/queues#job-batching)가 디스패치되었는지 검증할 수 있습니다. 이 메서드는 `Illuminate\Bus\PendingBatch` 인스턴스를 인수로 받으며, 이를 통해 배치 내 작업들을 확인할 수 있습니다:

```
use Illuminate\Bus\PendingBatch;
use Illuminate\Support\Facades\Bus;

Bus::assertBatched(function (PendingBatch $batch) {
    return $batch->name == 'import-csv' &&
           $batch->jobs->count() === 10;
});
```

<a name="testing-job-batch-interaction"></a>
#### 작업과 배치 상호작용 테스트

가끔 개별 작업이 배치와 어떻게 상호작용하는지 테스트해야 할 때가 있습니다. 예를 들어 작업이 배치 처리를 중단하는 경우입니다. 이때는 `withFakeBatch` 메서드로 작업에 페이크 배치를 할당할 수 있으며, 이 메서드는 작업 인스턴스와 페이크 배치의 튜플을 반환합니다:

```
[$job, $batch] = (new ShipOrder)->withFakeBatch();

$job->handle();

$this->assertTrue($batch->cancelled());
$this->assertEmpty($batch->added);
```

<a name="event-fake"></a>
## Event Fake

이벤트를 디스패치하는 코드를 테스트할 때, 이벤트 리스너가 실제로 실행되지 않도록 할 수 있습니다. `Event` 파사드의 `fake` 메서드를 사용하면 리스너 실행을 차단하고, 테스트 대상 코드를 실행한 후 `assertDispatched`, `assertNotDispatched`, `assertNothingDispatched` 메서드로 어떤 이벤트가 디스패치되었는지 확인할 수 있습니다:

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

        // 주문 배송 수행...

        // 이벤트가 디스패치되었는지 검증...
        Event::assertDispatched(OrderShipped::class);

        // 이벤트가 두 번 디스패치되었는지 검증...
        Event::assertDispatched(OrderShipped::class, 2);

        // 이벤트가 디스패치되지 않았는지 검증...
        Event::assertNotDispatched(OrderFailedToShip::class);

        // 이벤트가 전혀 디스패치되지 않았는지 검증...
        Event::assertNothingDispatched();
    }
}
```

`assertDispatched` 또는 `assertNotDispatched` 메서드에 클로저를 전달하면, 특정 조건을 만족하는 이벤트가 디스패치되었는지 검증할 수 있습니다:

```
Event::assertDispatched(function (OrderShipped $event) use ($order) {
    return $event->order->id === $order->id;
});
```

특정 이벤트에 리스너가 등록되어 있는지만 확인하려면 `assertListening` 메서드를 사용하세요:

```
Event::assertListening(
    OrderShipped::class,
    SendShipmentNotification::class
);
```

> [!WARNING]
> `Event::fake()`를 호출하면 이벤트 리스너가 전혀 실행되지 않습니다. 따라서 모델의 `creating` 이벤트에서 UUID 생성을 등 이벤트가 필요한 팩토리를 사용할 때는 `Event::fake()`를 팩토리 사용 **이후**에 호출해야 합니다.

<a name="faking-a-subset-of-events"></a>
#### 일부 이벤트만 페이크하기

특정 이벤트만 페이크하고 싶으면 `fake` 또는 `fakeFor` 메서드에 이벤트 클래스를 배열로 전달하세요:

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

    // 다른 이벤트는 정상적으로 디스패치됩니다...
    $order->update([...]);
}
```

특정 이벤트를 제외하고 나머지 모두 페이크하려면 `except` 메서드를 사용하세요:

```
Event::fake()->except([
    OrderCreated::class,
]);
```

<a name="scoped-event-fakes"></a>
### 범위 지정 이벤트 페이크 (Scoped Event Fakes)

테스트 일부 구간에만 이벤트 리스너를 페이크하고 싶다면 `fakeFor` 메서드를 사용하세요:

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

        // 이벤트가 정상적으로 디스패치되고 옵저버도 실행됩니다 ...
        $order->update([...]);
    }
}
```

<a name="http-fake"></a>
## HTTP Fake

`Http` 파사드의 `fake` 메서드는 외부 HTTP 클라이언트가 요청할 때 가짜/스텁 응답을 반환하도록 지시할 수 있습니다. 상세 내용은 [HTTP 클라이언트 테스트 문서](/docs/9.x/http-client#testing)에서 확인하세요.

<a name="mail-fake"></a>
## 메일 페이크 (Mail Fake)

`Mail` 파사드의 `fake` 메서드를 사용하면 메일 발송이 실제로 이루어지지 않게 할 수 있습니다. 보통 테스트 대상 코드와 메일 발송은 직접 관련이 없기 때문에, 메일이 발송되었는지만 확인하면 충분한 경우가 많습니다.

`Mail::fake()`를 호출하면, 메일 발송 대신 어떤 메일러블(mailables)이 발송 명령을 받았는지 검증할 수 있습니다:

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

        // 주문 배송 수행...

        // 메일이 전혀 발송되지 않았는지 검증...
        Mail::assertNothingSent();

        // 특정 메일러블이 발송되었는지 검증...
        Mail::assertSent(OrderShipped::class);

        // 특정 메일러블이 두 번 발송되었는지 검증...
        Mail::assertSent(OrderShipped::class, 2);

        // 특정 메일러블이 발송되지 않았는지 검증...
        Mail::assertNotSent(AnotherMailable::class);
    }
}
```

메일러블이 백그라운드 큐에 적재되는 경우에는 `assertQueued` 메서드를, 그렇지 않은 전송 확인은 `assertSent`를 사용하세요:

```
Mail::assertQueued(OrderShipped::class);

Mail::assertNotQueued(OrderShipped::class);

Mail::assertNothingQueued();
```

검증 메서드에 클로저를 전달하면, 특정 조건을 만족하는 메일러블이 발송되었는지 검사할 수 있습니다:

```
Mail::assertSent(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

`Mail` 파사드의 검증 메서드에서 인수로 받는 메일러블 인스턴스는 수신자 및 헤더를 확인할 수 있는 유용한 메서드를 제공합니다:

```
Mail::assertSent(OrderShipped::class, function ($mail) use ($user) {
    return $mail->hasTo($user->email) &&
           $mail->hasCc('...') &&
           $mail->hasBcc('...') &&
           $mail->hasReplyTo('...') &&
           $mail->hasFrom('...') &&
           $mail->hasSubject('...');
});
```

메일러블 첨부파일 확인을 위한 여러 메서드도 포함되어 있습니다:

```
use Illuminate\Mail\Mailables\Attachment;

Mail::assertSent(OrderShipped::class, function ($mail) {
    return $mail->hasAttachment(
        Attachment::fromPath('/path/to/file')
                ->as('name.pdf')
                ->withMime('application/pdf')
    );
});

Mail::assertSent(OrderShipped::class, function ($mail) {
    return $mail->hasAttachment(
        Attachment::fromStorageDisk('s3', '/path/to/file')
    );
});

Mail::assertSent(OrderShipped::class, function ($mail) use ($pdfData) {
    return $mail->hasAttachment(
        Attachment::fromData(fn () => $pdfData, 'name.pdf')
    );
});
```

메일이 발송되지 않았음을 검증하는 메서드가 두 가지(`assertNotSent`와 `assertNotQueued`) 있는데, 때로는 발송 또는 큐 적재가 모두 없었음을 검증하고 싶을 때도 있습니다. 이 경우 `assertNothingOutgoing` 와 `assertNotOutgoing` 메서드를 사용하세요:

```
Mail::assertNothingOutgoing();

Mail::assertNotOutgoing(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

<a name="testing-mailable-content"></a>
#### 메일러블 콘텐츠 테스트

메일러블을 특정 사용자에게 발송했다고 검증하는 테스트와는 별도로, 메일러블의 내용을 별도 테스트하는 것을 권장합니다. 메일러블 테스트 방법은 [메일러블 테스트 문서](/docs/9.x/mail#testing-mailables)를 참고하세요.

<a name="notification-fake"></a>
## 알림 페이크 (Notification Fake)

`Notification` 파사드의 `fake` 메서드를 사용하면 알림 발송을 실제로 수행하지 않게 할 수 있습니다. 알림 발송은 테스트 대상 코드와 직접 관련 없는 경우가 많아, 발송 시도 여부만 검증하는 정도면 충분한 경우가 많습니다.

`Notification::fake()` 호출 후에는 [알림(notification)](/docs/9.x/notifications) 발송 여부를 검증할 수 있습니다. 또한 전달된 데이터도 확인할 수 있습니다:

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

        // 주문 배송 수행...

        // 알림이 전혀 발송되지 않았는지 검증...
        Notification::assertNothingSent();

        // 특정 사용자에게 알림이 발송되었는지 검증...
        Notification::assertSentTo(
            [$user], OrderShipped::class
        );

        // 특정 사용자에게 알림이 발송되지 않았는지 검증...
        Notification::assertNotSentTo(
            [$user], AnotherNotification::class
        );

        // 알림 발송 횟수를 검증...
        Notification::assertCount(3);
    }
}
```

`assertSentTo`와 `assertNotSentTo` 메서드에 클로저를 전달하면, 조건에 맞는 알림이 발송되었는지 여부를 검증할 수 있습니다:

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

테스트 대상 코드가 [온디맨드 알림](/docs/9.x/notifications#on-demand-notifications)을 발송한다면, `assertSentOnDemand` 메서드로 발송 여부를 확인할 수 있습니다:

```
Notification::assertSentOnDemand(OrderShipped::class);
```

두 번째 인수로 클로저를 넘기면 올바른 "route" 주소로 알림이 발송되었는지도 검증할 수 있습니다:

```
Notification::assertSentOnDemand(
    OrderShipped::class,
    function ($notification, $channels, $notifiable) use ($user) {
        return $notifiable->routes['mail'] === $user->email;
    }
);
```

<a name="queue-fake"></a>
## 큐 페이크 (Queue Fake)

`Queue` 파사드의 `fake` 메서드는 큐에 작업이 푸시되는 것을 막습니다. 대부분 작업 자체는 별도 테스트 클래스에서 검증하므로, 작업이 큐에 푸시되었는지만 검증해도 충분한 경우가 많습니다.

`Queue::fake()` 호출 후, 작업 큐 푸시 시도 여부를 다음과 같이 검증할 수 있습니다:

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

        // 주문 배송 수행...

        // 작업이 전혀 푸시되지 않았는지 검증...
        Queue::assertNothingPushed();

        // 특정 큐에 작업이 푸시되었는지 검증...
        Queue::assertPushedOn('queue-name', ShipOrder::class);

        // 작업이 두 번 푸시되었는지 검증...
        Queue::assertPushed(ShipOrder::class, 2);

        // 작업이 푸시되지 않았는지 검증...
        Queue::assertNotPushed(AnotherJob::class);
    }
}
```

클로저를 사용해 특정 조건을 만족하는 작업이 푸시되었는지 확인할 수도 있습니다:

```
Queue::assertPushed(function (ShipOrder $job) use ($order) {
    return $job->order->id === $order->id;
});
```

특정 작업만 페이크하고 나머지는 정상 실행하려면 `fake` 메서드에 작업 클래스명을 배열로 넘기세요:

```
public function test_orders_can_be_shipped()
{
    Queue::fake([
        ShipOrder::class,
    ]);
    
    // 주문 배송 수행...

    // 작업이 두 번 푸시되었는지 검증...
    Queue::assertPushed(ShipOrder::class, 2);
}
```

<a name="job-chains"></a>
### 작업 체인 (Job Chains)

`Queue` 파사드의 `assertPushedWithChain` 및 `assertPushedWithoutChain` 메서드로, 푸시된 작업의 체인 여부를 검증할 수 있습니다. `assertPushedWithChain`은 첫 번째 인자로 기본 작업, 두 번째 인자로 체인 작업 배열을 받습니다:

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

체인 작업 배열은 클래스명 배열 또는 실제 작업 인스턴스 배열이 될 수 있습니다. 인스턴스 배열의 경우 Laravel이 클래스와 프로퍼티 동일성을 검사합니다:

```
Queue::assertPushedWithChain(ShipOrder::class, [
    new RecordShipment,
    new UpdateInventory,
]);
```

작업이 체인 없이 푸시되었는지도 다음과 같이 검증할 수 있습니다:

```
Queue::assertPushedWithoutChain(ShipOrder::class);
```

<a name="storage-fake"></a>
## Storage Fake

`Storage` 파사드의 `fake` 메서드를 사용하면 가짜 디스크를 손쉽게 생성할 수 있습니다. 이것과 `Illuminate\Http\UploadedFile` 클래스의 파일 생성 유틸리티를 함께 사용하면 파일 업로드 기능 테스트가 매우 편리해집니다. 예를 들어:

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

        // 하나 이상의 파일이 저장되었는지 검증...
        Storage::disk('photos')->assertExists('photo1.jpg');
        Storage::disk('photos')->assertExists(['photo1.jpg', 'photo2.jpg']);

        // 특정 파일이 저장되지 않았는지 검증...
        Storage::disk('photos')->assertMissing('missing.jpg');
        Storage::disk('photos')->assertMissing(['missing.jpg', 'non-existing.jpg']);

        // 특정 디렉터리가 비어 있는지 검증...
        Storage::disk('photos')->assertDirectoryEmpty('/wallpapers');
    }
}
```

기본적으로 `fake` 메서드는 임시 디렉터리의 모든 파일을 삭제합니다. 해당 파일을 유지하고 싶다면 대신 `persistentFake` 메서드를 사용하세요. 파일 업로드 테스트에 관해서는 [HTTP 테스트 문서의 파일 업로드 섹션](/docs/9.x/http-tests#testing-file-uploads)을 참조하세요.

> [!WARNING]
> `image` 메서드를 사용하려면 [GD 확장](https://www.php.net/manual/en/book.image.php)이 필요합니다.

<a name="interacting-with-time"></a>
## 시간 조작 (Interacting With Time)

테스트 중 `now()` 또는 `Illuminate\Support\Carbon::now()`와 같은 헬퍼에서 반환하는 시간을 변경해야 할 때가 있습니다. Laravel 기본 피처 테스트 클래스는 현재 시간을 조작할 수 있는 헬퍼를 제공합니다:

```
use Illuminate\Support\Carbon;

public function testTimeCanBeManipulated()
{
    // 미래로 시간 이동...
    $this->travel(5)->milliseconds();
    $this->travel(5)->seconds();
    $this->travel(5)->minutes();
    $this->travel(5)->hours();
    $this->travel(5)->days();
    $this->travel(5)->weeks();
    $this->travel(5)->years();

    // 시간을 멈추고 클로저 실행 후 정상 시간 복귀...
    $this->freezeTime(function (Carbon $time) {
        // ...
    });

    // 과거로 시간 이동...
    $this->travel(-5)->hours();

    // 특정 시간으로 이동...
    $this->travelTo(now()->subHours(6));

    // 현재 시간으로 돌아오기...
    $this->travelBack();
}
```