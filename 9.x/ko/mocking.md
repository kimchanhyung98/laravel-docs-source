# Mocking

- [소개](#introduction)
- [객체 모킹](#mocking-objects)
- [파사드 모킹](#mocking-facades)
    - [파사드 스파이](#facade-spies)
- [Bus Fake](#bus-fake)
    - [잡 체인](#bus-job-chains)
    - [잡 배치](#job-batches)
- [이벤트 페이크](#event-fake)
    - [스코프드 이벤트 페이크](#scoped-event-fakes)
- [HTTP 페이크](#http-fake)
- [메일 페이크](#mail-fake)
- [노티피케이션 페이크](#notification-fake)
- [큐 페이크](#queue-fake)
    - [잡 체인](#job-chains)
- [스토리지 페이크](#storage-fake)
- [시간 조작](#interacting-with-time)

<a name="introduction"></a>
## 소개

Laravel 애플리케이션을 테스트할 때, 특정 측면을 "모킹"하여 테스트 중 실제로 실행되지 않도록 하고 싶을 때가 있을 수 있습니다. 예를 들어, 이벤트를 디스패치하는 컨트롤러를 테스트할 때, 이벤트 리스너가 실제로 실행되지 않도록 이벤트 리스너를 모킹할 수 있습니다. 이를 통해 이벤트 리스너 실행에 대해 걱정하지 않고 컨트롤러의 HTTP 응답만 테스트할 수 있습니다. 이벤트 리스너는 별도의 테스트 케이스에서 테스트할 수 있기 때문입니다.

Laravel은 이벤트, 잡, 기타 파사드를 간편하게 모킹할 수 있는 메서드를 기본적으로 제공합니다. 이러한 헬퍼는 복잡한 Mockery 메서드 호출을 직접 작성할 필요 없이 Mockery 위에 얇은 편의 레이어를 제공합니다.

<a name="mocking-objects"></a>
## 객체 모킹

Laravel의 [서비스 컨테이너](/docs/{{version}}/container)를 통해 주입될 객체를 모킹할 경우, 모킹한 인스턴스를 `instance` 바인딩으로 컨테이너에 등록해야 합니다. 이렇게 하면 컨테이너가 객체를 직접 생성하는 대신 모킹한 인스턴스를 사용하도록 지시합니다:

```php
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

이를 더 편리하게 하기 위해, Laravel의 기본 테스트 케이스 클래스에서 제공하는 `mock` 메서드를 사용할 수 있습니다. 다음 예제는 위 예제와 동일합니다:

```php
use App\Service;
use Mockery\MockInterface;

$mock = $this->mock(Service::class, function (MockInterface $mock) {
    $mock->shouldReceive('process')->once();
});
```

객체의 일부 메서드만 모킹해야 하는 경우에는 `partialMock` 메서드를 사용할 수 있습니다. 모킹되지 않은 메서드는 정상적으로 실행됩니다:

```php
use App\Service;
use Mockery\MockInterface;

$mock = $this->partialMock(Service::class, function (MockInterface $mock) {
    $mock->shouldReceive('process')->once();
});
```

마찬가지로, 객체를 [스파이](http://docs.mockery.io/en/latest/reference/spies.html)하고 싶을 때는 Laravel의 기본 테스트 케이스 클래스가 `Mockery::spy`에 대한 편의 래퍼인 `spy` 메서드를 제공합니다. 스파이는 모킹과 비슷하지만, 테스트되는 코드와의 상호작용을 기록하여, 코드 실행 후 어썰션을 할 수 있습니다:

```php
use App\Service;

$spy = $this->spy(Service::class);

// ...

$spy->shouldHaveReceived('process');
```

<a name="mocking-facades"></a>
## 파사드 모킹

기존의 정적 메서드 호출과 달리, [파사드](/docs/{{version}}/facades)([실시간 파사드](/docs/{{version}}/facades#real-time-facades) 포함)는 모킹할 수 있습니다. 이는 전통적인 정적 메서드에 비해 뛰어난 테스트 용이성을 제공하며, 의존성 주입을 사용할 때와 같은 테스트 가능성을 제공합니다. 테스트 시, 컨트롤러 등에서 발생하는 Laravel 파사드의 호출을 종종 모킹하고 싶을 수 있습니다. 예를 들어, 아래 컨트롤러 액션을 보겠습니다:

```php
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

`Cache` 파사드에 대한 호출은 `shouldReceive` 메서드를 사용하여 모킹할 수 있으며, 이는 [Mockery](https://github.com/padraic/mockery) 모크 인스턴스를 반환합니다. 파사드는 실제로 Laravel [서비스 컨테이너](/docs/{{version}}/container)에 의해 해석되고 관리되기 때문에, 일반적인 정적 클래스보다 훨씬 높은 테스트 용이성을 가집니다. 예를 들어, `Cache` 파사드의 `get` 메서드 호출을 모킹해봅시다:

```php
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

> **경고**  
> `Request` 파사드는 모킹하지 않아야 합니다. 대신 원하는 입력값을 [HTTP 테스트 메서드](/docs/{{version}}/http-tests) (`get`이나 `post` 등)에 전달하세요. 마찬가지로 `Config` 파사드를 모킹하는 대신 테스트 내에서 `Config::set` 메서드를 호출하세요.

<a name="facade-spies"></a>
### 파사드 스파이

파사드를 [스파이](http://docs.mockery.io/en/latest/reference/spies.html)해야 한다면, 해당 파사드의 `spy` 메서드를 호출할 수 있습니다. 스파이는 모킹과 비슷하지만, 테스트한 코드와의 상호작용을 기록하여 코드 실행 후 어썰션을 할 수 있습니다:

```php
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

잡을 디스패치하는 코드를 테스트할 때, 보통 특정 잡이 디스패치되었는지만 확인하고 실제로 큐에 넣거나 실행하지는 않습니다. 왜냐하면 잡의 실행은 보통 별도의 테스트 클래스에서 테스트할 수 있기 때문입니다.

`Bus` 파사드의 `fake` 메서드를 사용하면 잡이 큐에 디스패치되는 것을 방지할 수 있습니다. 이후 테스트 대상 코드를 실행한 후 `assertDispatched`, `assertNotDispatched` 등의 메서드를 사용해 어떤 잡이 디스패치되었는지 확인할 수 있습니다:

```php
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

        // 주문 발송 처리...

        // 잡이 디스패치되었는지 어썰트...
        Bus::assertDispatched(ShipOrder::class);

        // 잡이 디스패치되지 않았는지 어썰트...
        Bus::assertNotDispatched(AnotherJob::class);

        // 동기적으로 디스패치된 잡 어썰트...
        Bus::assertDispatchedSync(AnotherJob::class);

        // 동기적으로 디스패치되지 않은 잡 어썰트...
        Bus::assertNotDispatchedSync(AnotherJob::class);

        // 응답 이후 디스패치된 잡 어썰트...
        Bus::assertDispatchedAfterResponse(AnotherJob::class);

        // 응답 이후 디스패치되지 않은 잡 어썰트...
        Bus::assertNotDispatchedAfterResponse(AnotherJob::class);

        // 어떤 잡도 디스패치되지 않았는지 어썰트...
        Bus::assertNothingDispatched();
    }
}
```

"진리성 테스트"를 통과하는 잡이 디스패치되었는지 확인하기 위해, 콜백을 전달할 수 있습니다. 최소 하나의 잡이 해당 조건을 만족하면 어썰션에 통과합니다. 예를 들어, 특정 주문에 대해 잡이 디스패치되었는지 확인하려면:

```php
Bus::assertDispatched(function (ShipOrder $job) use ($order) {
    return $job->order->id === $order->id;
});
```

<a name="faking-a-subset-of-jobs"></a>
#### 특정 잡만 페이크하기

특정 잡만 디스패치되지 않도록 하려면, 페이크 할 잡을 `fake` 메서드에 전달하면 됩니다:

```php
/**
 * 주문 프로세스 테스트.
 */
public function test_orders_can_be_shipped()
{
    Bus::fake([
        ShipOrder::class,
    ]);

    // ...
}
```

특정 잡만 제외하고 모두 페이크하려면 `except` 메서드를 사용하세요:

```php
Bus::fake()->except([
    ShipOrder::class,
]);
```

<a name="bus-job-chains"></a>
### 잡 체인

`Bus` 파사드의 `assertChained` 메서드는 [잡 체인](/docs/{{version}}/queues#job-chaining)이 디스패치되었는지 확인할 때 사용할 수 있습니다. 첫 번째 인자로 체인된 잡의 배열을 받습니다:

```php
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

위 예시처럼 잡 클래스명으로 이루어진 배열을 사용할 수 있으며, 실제 잡 인스턴스 배열을 전달할 수도 있습니다. 이 경우, Laravel은 실제 체인된 잡들과 클래스 및 속성 값이 일치하는지 확인합니다:

```php
Bus::assertChained([
    new ShipOrder,
    new RecordShipment,
    new UpdateInventory,
]);
```

<a name="job-batches"></a>
### 잡 배치

`Bus` 파사드의 `assertBatched` 메서드는 [잡 배치](/docs/{{version}}/queues#job-batching)가 디스패치되었는지 확인할 때 사용합니다. 전달한 클로저에는 `Illuminate\Bus\PendingBatch` 인스턴스가 주어지며, 이를 통해 배치 내 잡을 검사할 수 있습니다:

```php
use Illuminate\Bus\PendingBatch;
use Illuminate\Support\Facades\Bus;

Bus::assertBatched(function (PendingBatch $batch) {
    return $batch->name == 'import-csv' &&
           $batch->jobs->count() === 10;
});
```

<a name="testing-job-batch-interaction"></a>
#### 잡/배치 상호작용 테스트

개별 잡이 자신의 배치와 상호작용하는지 테스트해야 할 때가 있습니다. 예를 들어, 잡이 배치의 추가 처리를 취소하는지 확인해야 할 수 있습니다. 이럴 땐 `withFakeBatch` 메서드를 사용해 잡에 페이크 배치를 할당합니다. 이 메서드는 튜플 형태로 잡 인스턴스와 페이크 배치를 반환합니다:

```php
[$job, $batch] = (new ShipOrder)->withFakeBatch();

$job->handle();

$this->assertTrue($batch->cancelled());
$this->assertEmpty($batch->added);
```

<a name="event-fake"></a>
## 이벤트 페이크

이벤트를 디스패치하는 코드를 테스트할 때, 실제로 이벤트 리스너가 실행되지 않도록 하고 싶을 수 있습니다. `Event` 파사드의 `fake` 메서드를 사용하면 리스너 실행을 방지할 수 있습니다. 테스트 대상 코드를 실행하고, `assertDispatched`, `assertNotDispatched`, `assertNothingDispatched` 메서드를 통해 어떤 이벤트가 디스패치되었는지 어썰션 할 수 있습니다:

```php
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
     * 주문 발송 테스트.
     */
    public function test_orders_can_be_shipped()
    {
        Event::fake();

        // 주문 발송 처리...

        // 이벤트 디스패치 어썰트...
        Event::assertDispatched(OrderShipped::class);

        // 이벤트 2회 디스패치 어썰트...
        Event::assertDispatched(OrderShipped::class, 2);

        // 이벤트가 디스패치되지 않았는지 어썰트...
        Event::assertNotDispatched(OrderFailedToShip::class);

        // 어떤 이벤트도 디스패치되지 않았는지 어썰트...
        Event::assertNothingDispatched();
    }
}
```

`assertDispatched` 또는 `assertNotDispatched` 메서드에 콜백을 전달하여 "진리성 테스트"를 통과하는 이벤트가 디스패치되었는지 어썰션할 수 있습니다. 한 개 이상의 이벤트가 조건을 만족하면 성공입니다:

```php
Event::assertDispatched(function (OrderShipped $event) use ($order) {
    return $event->order->id === $order->id;
});
```

특정 이벤트 리스너가 이벤트를 리스닝하고 있는지 확인하려면, `assertListening` 메서드를 사용할 수 있습니다:

```php
Event::assertListening(
    OrderShipped::class,
    SendShipmentNotification::class
);
```

> **경고**  
> `Event::fake()`를 호출한 후에는 이벤트 리스너가 실행되지 않습니다. 예를 들어, 모델 팩토리가 `creating` 이벤트 등 이벤트에 의존하여 UUID 등을 생성한다면, 팩토리 사용 **이후**에 `Event::fake()`를 호출해야 합니다.

<a name="faking-a-subset-of-events"></a>
#### 특정 이벤트만 페이크하기

특정 이벤트에 대해서만 리스너를 페이크하려면, 해당 이벤트를 `fake` 또는 `fakeFor` 메서드에 전달하세요:

```php
/**
 * 주문 프로세스 테스트.
 */
public function test_orders_can_be_processed()
{
    Event::fake([
        OrderCreated::class,
    ]);

    $order = Order::factory()->create();

    Event::assertDispatched(OrderCreated::class);

    // 다른 이벤트는 정상적으로 디스패치
    $order->update([...]);
}
```

특정 이벤트만 제외하고 모두 페이크하려면 `except` 메서드를 사용할 수 있습니다:

```php
Event::fake()->except([
    OrderCreated::class,
]);
```

<a name="scoped-event-fakes"></a>
### 스코프드 이벤트 페이크

테스트의 일부분에서만 이벤트 리스너를 페이크하려면, `fakeFor` 메서드를 사용할 수 있습니다:

```php
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
     * 주문 프로세스 테스트.
     */
    public function test_orders_can_be_processed()
    {
        $order = Event::fakeFor(function () {
            $order = Order::factory()->create();

            Event::assertDispatched(OrderCreated::class);

            return $order;
        });

        // 이벤트는 정상적으로 디스패치되고 옵저버도 실행됩니다...
        $order->update([...]);
    }
}
```

<a name="http-fake"></a>
## HTTP 페이크

`Http` 파사드의 `fake` 메서드는 HTTP 클라이언트에서 요청 시 더미 응답(스텁 응답)을 반환하도록 할 수 있습니다. 아웃고잉 HTTP 요청을 페이크하는 더 자세한 내용은 [HTTP 클라이언트 테스트 문서](/docs/{{version}}/http-client#testing)를 참조하세요.

<a name="mail-fake"></a>
## 메일 페이크

`Mail` 파사드의 `fake` 메서드를 사용하면 실제 메일 발송을 방지할 수 있습니다. 일반적으로 메일 발송은 테스트 대상 코드와 직접적인 관련이 없습니다. 대부분은 Laravel에 특정 mailable을 발송하도록 지시했다는 것을 어썰트하는 것만으로 충분합니다.

`Mail` 파사드의 `fake` 메서드 호출 이후에는 [mailable](/docs/{{version}}/mail)이 사용자에게 발송되도록 지시되었는지, 그리고 mailable에 전달된 데이터 등의 검사도 할 수 있습니다:

```php
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

        // 주문 발송 처리...

        // 어떤 mailable도 발송되지 않았는지 어썰트...
        Mail::assertNothingSent();

        // mailable이 발송되었는지 어썰트...
        Mail::assertSent(OrderShipped::class);

        // mailable이 두 번 발송되었는지 어썰트...
        Mail::assertSent(OrderShipped::class, 2);

        // mailable이 발송되지 않았는지 어썰트...
        Mail::assertNotSent(AnotherMailable::class);
    }
}
```

만약 mailable을 백그라운드에서 큐로 발송한다면 `assertSent` 대신 `assertQueued` 메서드를 사용하세요:

```php
Mail::assertQueued(OrderShipped::class);

Mail::assertNotQueued(OrderShipped::class);

Mail::assertNothingQueued();
```

"진리성 테스트"를 통과하는 mailable이 발송/큐잉되었는지 검증하려면, 클로저를 `assertSent`, `assertNotSent`, `assertQueued`, `assertNotQueued` 등에 전달하세요. 한 개 이상의 mailable이 조건에 맞으면 성공입니다:

```php
Mail::assertSent(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

mailable 인스턴스를 받는 클로저 안에서 아래와 같이 다양한 메서드를 활용해 수신자, 참조, 답장, 발신인, 제목 등을 검사할 수도 있습니다:

```php
Mail::assertSent(OrderShipped::class, function ($mail) use ($user) {
    return $mail->hasTo($user->email) &&
           $mail->hasCc('...') &&
           $mail->hasBcc('...') &&
           $mail->hasReplyTo('...') &&
           $mail->hasFrom('...') &&
           $mail->hasSubject('...');
});
```

첨부파일도 아래와 같은 방법으로 어썰트할 수 있습니다:

```php
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

메일이 발송되지 않았는지 어썰트하는 메서드는 `assertNotSent`와 `assertNotQueued`가 있습니다. 때로는 메일이 발송 **되지도** 큐잉 **되지도** 않았음을 어썰트하고 싶을 수 있습니다. 이럴 땐 `assertNothingOutgoing` 및 `assertNotOutgoing` 메서드를 사용할 수 있습니다:

```php
Mail::assertNothingOutgoing();

Mail::assertNotOutgoing(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

<a name="testing-mailable-content"></a>
#### mailable 내용 테스트

특정 사용자에게 mailable이 "발송"되었는지 어썰트하는 테스트와 별도로 mailable의 내용을 테스트하는 것을 권장합니다. mailable의 내용을 테스트하는 방법은 [메일러블 테스트](/docs/{{version}}/mail#testing-mailables) 문서를 참고하세요.

<a name="notification-fake"></a>
## 노티피케이션 페이크

`Notification` 파사드의 `fake` 메서드를 사용하면 실제 노티피케이션 발송을 방지할 수 있습니다. 대부분의 경우, Laravel이 특정 노티피케이션을 발송하도록 지시했다는 것을 어썰트하는 것만으로 충분합니다.

`Notification` 파사드의 `fake` 메서드 호출 후에는 [노티피케이션](/docs/{{version}}/notifications)이 사용자에게 보내졌는지, 그리고 노티피케이션이 받은 데이터까지 검사할 수 있습니다:

```php
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

        // 주문 발송 처리...

        // 노티피케이션이 발송되지 않았는지 어썰트...
        Notification::assertNothingSent();

        // 특정 사용자에게 노티피케이션 발송 어썰트...
        Notification::assertSentTo(
            [$user], OrderShipped::class
        );

        // 노티피케이션이 발송되지 않았는지 어썰트...
        Notification::assertNotSentTo(
            [$user], AnotherNotification::class
        );

        // 특정 개수만큼 발송되었는지 어썰트...
        Notification::assertCount(3);
    }
}
```

`assertSentTo`, `assertNotSentTo` 메서드에 클로저를 전달하여 "진리성 테스트"를 통과하는 노티피케이션이 발송되었는지 어썰션할 수 있습니다. 최소 하나가 조건에 맞으면 성공입니다:

```php
Notification::assertSentTo(
    $user,
    function (OrderShipped $notification, $channels) use ($order) {
        return $notification->order->id === $order->id;
    }
);
```

<a name="on-demand-notifications"></a>
#### 온디맨드 노티피케이션

테스트하는 코드에서 [온디맨드 노티피케이션](/docs/{{version}}/notifications#on-demand-notifications)를 발송한다면, `assertSentOnDemand` 메서드로 해당 노티피케이션의 발송을 검증할 수 있습니다:

```php
Notification::assertSentOnDemand(OrderShipped::class);
```

`assertSentOnDemand` 메서드의 두 번째 인자로 클로저를 넘겨 온디맨드 노티피케이션이 올바른 "route" 주소로 발송되었는지 확인할 수 있습니다:

```php
Notification::assertSentOnDemand(
    OrderShipped::class,
    function ($notification, $channels, $notifiable) use ($user) {
        return $notifiable->routes['mail'] === $user->email;
    }
);
```

<a name="queue-fake"></a>
## 큐 페이크

`Queue` 파사드의 `fake` 메서드를 사용하면 큐에 잡이 실제로 push되는 것을 방지할 수 있습니다. 대부분의 경우, 특정 잡이 큐에 push되었는지 어썰션만 하면 충분하며, 실제 잡의 함수 자체는 다른 테스트 클래스에서 검증하면 됩니다.

`Queue` 파사드의 `fake` 호출 후, 잡이 큐에 push되었는지 어썰트할 수 있습니다:

```php
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

        // 주문 발송 처리...

        // 잡이 push되지 않았는지 어썰트...
        Queue::assertNothingPushed();

        // 특정 큐에 잡이 push되었는지 어썰트...
        Queue::assertPushedOn('queue-name', ShipOrder::class);

        // 잡이 두 번 push되었는지 어썰트...
        Queue::assertPushed(ShipOrder::class, 2);

        // 잡이 push되지 않았는지 어썰트...
        Queue::assertNotPushed(AnotherJob::class);
    }
}
```

잡이 push될 때 "진리성 테스트"를 통과하는지 확인하려면, 클로저를 `assertPushed` 또는 `assertNotPushed`에 전달하세요:

```php
Queue::assertPushed(function (ShipOrder $job) use ($order) {
    return $job->order->id === $order->id;
});
```

특정 잡만 페이크하고, 나머지 잡은 실제로 실행되게 하려면 `fake`에 페이크 할 잡 클래스명을 배열로 전달하면 됩니다:

```php
public function test_orders_can_be_shipped()
{
    Queue::fake([
        ShipOrder::class,
    ]);
    
    // 주문 발송 처리...

    // 잡이 두 번 push되었는지 어썰트...
    Queue::assertPushed(ShipOrder::class, 2);
}
```

<a name="job-chains"></a>
### 잡 체인

`Queue` 파사드의 `assertPushedWithChain` 및 `assertPushedWithoutChain` 메서드는 push된 잡의 체인을 검사하는 데 사용됩니다. `assertPushedWithChain` 메서드는 첫 번째 인자로 메인 잡, 두 번째 인자로 체인된 잡의 배열을 받습니다:

```php
use App\Jobs\RecordShipment;
use App\Jobs\ShipOrder;
use App\Jobs\UpdateInventory;
use Illuminate\Support\Facades\Queue;

Queue::assertPushedWithChain(ShipOrder::class, [
    RecordShipment::class,
    UpdateInventory::class
]);
```

위 예시처럼 잡 클래스명 배열 외에도, 실제 잡 인스턴스 배열을 전달할 수도 있습니다. 이 경우, Laravel은 디스패치된 잡의 클래스와 프로퍼티 값이 동일한지 확인합니다:

```php
Queue::assertPushedWithChain(ShipOrder::class, [
    new RecordShipment,
    new UpdateInventory,
]);
```

잡 체인 없이 잡이 push되었는지 어썰트하려면 `assertPushedWithoutChain`을 사용하세요:

```php
Queue::assertPushedWithoutChain(ShipOrder::class);
```

<a name="storage-fake"></a>
## 스토리지 페이크

`Storage` 파사드의 `fake` 메서드를 사용하면 테스트용 가상 디스크를 쉽게 생성할 수 있으며, `Illuminate\Http\UploadedFile` 클래스의 파일 생성 유틸리티와 결합하여 파일 업로드 테스트를 크게 단순화할 수 있습니다. 예시:

```php
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

        // 한 개 이상의 파일이 저장되었는지 어썰트...
        Storage::disk('photos')->assertExists('photo1.jpg');
        Storage::disk('photos')->assertExists(['photo1.jpg', 'photo2.jpg']);

        // 한 개 이상의 파일이 저장되지 않았는지 어썰트...
        Storage::disk('photos')->assertMissing('missing.jpg');
        Storage::disk('photos')->assertMissing(['missing.jpg', 'non-existing.jpg']);

        // 특정 디렉터리가 비어 있는지 어썰트...
        Storage::disk('photos')->assertDirectoryEmpty('/wallpapers');
    }
}
```

기본적으로 `fake` 메서드는 해당 임시 디렉터리의 모든 파일을 삭제합니다. 파일을 유지하고 싶다면 `persistentFake` 메서드를 사용할 수 있습니다. 파일 업로드 테스트 관련 자세한 내용은 [HTTP 테스트 문서의 파일 업로드 섹션](/docs/{{version}}/http-tests#testing-file-uploads)를 참고하세요.

> **경고**  
> `image` 메서드 사용 시 [GD 확장 모듈](https://www.php.net/manual/en/book.image.php)이 필요합니다.

<a name="interacting-with-time"></a>
## 시간 조작

테스트에서 `now` 또는 `Illuminate\Support\Carbon::now()`와 같은 헬퍼가 반환하는 시간을 임의로 변경해야 할 일이 있을 수 있습니다. 다행히, Laravel의 기본 기능 테스트 클래스는 현재 시간을 조작할 수 있는 헬퍼를 제공합니다:

```php
use Illuminate\Support\Carbon;

public function testTimeCanBeManipulated()
{
    // 미래로 이동...
    $this->travel(5)->milliseconds();
    $this->travel(5)->seconds();
    $this->travel(5)->minutes();
    $this->travel(5)->hours();
    $this->travel(5)->days();
    $this->travel(5)->weeks();
    $this->travel(5)->years();

    // 시간 정지 후 클로저 실행, 종료 후 시간 재개...
    $this->freezeTime(function (Carbon $time) {
        // ...
    });

    // 과거로 이동...
    $this->travel(-5)->hours();

    // 특정 시간으로 이동...
    $this->travelTo(now()->subHours(6));

    // 현재 시간으로 복귀...
    $this->travelBack();
}
```
