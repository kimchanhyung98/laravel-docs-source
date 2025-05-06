# 목(mock) 처리

- [소개](#introduction)
- [객체 목(mock) 처리](#mocking-objects)
- [파사드 목(mock) 처리](#mocking-facades)
    - [파사드 스파이](#facade-spies)
- [Bus 페이크](#bus-fake)
    - [잡 체인](#bus-job-chains)
    - [잡 배치](#job-batches)
- [이벤트 페이크](#event-fake)
    - [범위 지정 이벤트 페이크](#scoped-event-fakes)
- [HTTP 페이크](#http-fake)
- [메일 페이크](#mail-fake)
- [알림 페이크](#notification-fake)
- [큐 페이크](#queue-fake)
    - [잡 체인](#job-chains)
- [스토리지 페이크](#storage-fake)
- [시간 조작](#interacting-with-time)

<a name="introduction"></a>
## 소개

Laravel 애플리케이션을 테스트할 때, 특정 부분을 "목(mock)" 처리하여 테스트 중 실제로 실행되지 않도록 할 수 있습니다. 예를 들어, 이벤트를 디스패치하는 컨트롤러를 테스트할 때 이벤트 리스너들이 실제로 실행되지 않길 바랄 수 있습니다. 이렇게 하면 이벤트 리스너의 동작을 걱정할 필요 없이 컨트롤러의 HTTP 응답만을 테스트할 수 있습니다. 이벤트 리스너 자체는 별도의 테스트 케이스에서 테스트하면 됩니다.

Laravel은 이벤트, 잡, 그리고 기타 파사드를 목 처리할 수 있는 유용한 메서드를 기본적으로 제공합니다. 이러한 헬퍼들은 Mockery 위에 편의 레이어를 제공하므로 직접 복잡한 Mockery 메서드 호출을 작성하지 않아도 됩니다.

<a name="mocking-objects"></a>
## 객체 목(mock) 처리

Laravel의 [서비스 컨테이너](/docs/{{version}}/container)를 통해 애플리케이션에 주입되는 객체를 목 처리할 때, 목 인스턴스를 `instance` 바인딩으로 컨테이너에 바인딩해야 합니다. 이렇게 하면 컨테이너가 직접 객체를 생성하는 대신, 바인딩된 목 인스턴스를 사용하게 됩니다.

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

이 과정을 더 간단하게 하려면, Laravel의 기본 테스트 케이스 클래스에서 제공하는 `mock` 메서드를 사용할 수 있습니다. 아래 예시도 위와 동일합니다.

```php
use App\Service;
use Mockery\MockInterface;

$mock = $this->mock(Service::class, function (MockInterface $mock) {
    $mock->shouldReceive('process')->once();
});
```

객체의 일부 메서드만 목 처리하고 싶다면 `partialMock`을 사용할 수 있습니다. 목 처리하지 않은 메서드는 정상적으로 실행됩니다.

```php
use App\Service;
use Mockery\MockInterface;

$mock = $this->partialMock(Service::class, function (MockInterface $mock) {
    $mock->shouldReceive('process')->once();
});
```

마찬가지로, 객체를 [스파이](http://docs.mockery.io/en/latest/reference/spies.html)하고 싶은 경우, `spy` 메서드를 사용할 수 있습니다. 스파이는 테스트 중 코드와의 상호작용을 기록해, 코드 실행 후 주장(assertion)에 사용할 수 있습니다.

```php
use App\Service;

$spy = $this->spy(Service::class);

// ...

$spy->shouldHaveReceived('process');
```

<a name="mocking-facades"></a>
## 파사드 목(mock) 처리

전통적인 정적 메서드 호출과는 달리, [파사드](/docs/{{version}}/facades) (및 [실시간 파사드](/docs/{{version}}/facades#real-time-facades))는 목 처리할 수 있습니다. 이는 전통적인 정적 메서드보다 더 뛰어난 테스트 가능성을 제공합니다. 테스트 중, 컨트롤러에서 호출되는 Laravel 파사드도 종종 목 처리하게 됩니다. 예를 들어, 다음과 같은 컨트롤러 액션을 보겠습니다.

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

`Cache` 파사드에 대한 호출은 `shouldReceive` 메서드를 통해 목 처리할 수 있습니다. 이는 [Mockery](https://github.com/padraic/mockery) 목 인스턴스를 반환합니다. 파사드는 Laravel [서비스 컨테이너](/docs/{{version}}/container)로 관리되므로, 일반적인 정적 클래스보다 더 뛰어난 테스트 가능성을 제공합니다. 예를 들어, `Cache` 파사드의 `get` 메서드에 대한 호출을 목 처리해 보겠습니다.

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

> {note} `Request` 파사드는 목 처리하지 마세요. 대신, 테스트를 실행할 때 `get`이나 `post`와 같은 [HTTP 테스트 메서드](/docs/{{version}}/http-tests)에 원하는 입력값을 전달하세요. 마찬가지로, `Config` 파사드를 목 처리하는 대신, 테스트에서 `Config::set` 메서드를 사용하세요.

<a name="facade-spies"></a>
### 파사드 스파이

파사드를 [스파이](http://docs.mockery.io/en/latest/reference/spies.html)하고 싶다면, 해당 파사드의 `spy` 메서드를 호출할 수 있습니다. 스파이는 테스트 중 코드와의 상호작용을 기록해, 코드 실행 후 주장(assertion)에 사용할 수 있습니다.

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
## Bus 페이크

잡을 디스패치하는 코드를 테스트할 때, 실제로 잡을 큐에 넣거나 실행하지 않고, 특정 잡이 디스패치되었는지 주장(assert)하고자 할 수 있습니다. 잡 실행 자체는 별도의 테스트 클래스에서 테스트할 수 있기 때문입니다.

`Bus` 파사드의 `fake` 메서드를 사용하면 잡이 큐에 디스패치되는 것을 방지할 수 있습니다. 테스트 코드 실행 이후, `assertDispatched` 및 `assertNotDispatched` 메서드를 통해 애플리케이션이 디스패치 시도한 잡을 검사할 수 있습니다.

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

        // 주문 배송 수행...

        // 잡이 디스패치되었는지 주장
        Bus::assertDispatched(ShipOrder::class);

        // 잡이 디스패치되지 않았는지 주장
        Bus::assertNotDispatched(AnotherJob::class);

        // 동기적으로 잡이 디스패치되었는지 주장
        Bus::assertDispatchedSync(AnotherJob::class);

        // 동기적으로 잡이 디스패치되지 않았는지 주장
        Bus::assertNotDispatchedSync(AnotherJob::class);

        // 응답 이후 잡 디스패치 주장
        Bus::assertDispatchedAfterResponse(AnotherJob::class);

        // 응답 이후 잡 미디스패치 주장
        Bus::assertNotDispatchedAfterResponse(AnotherJob::class);

        // 아무 잡도 디스패치 안됨 주장
        Bus::assertNothingDispatched();
    }
}
```

클로저를 전달하여 특정 "진실 테스트(truth test)"를 통과하는 잡이 디스패치되었는지 주장할 수도 있습니다. 하나라도 통과하면 성공입니다. 예를 들어, 특정 주문에 대한 잡이 디스패치되었는지 주장할 수 있습니다.

```php
Bus::assertDispatched(function (ShipOrder $job) use ($order) {
    return $job->order->id === $order->id;
});
```

<a name="bus-job-chains"></a>
### 잡 체인

`Bus` 파사드의 `assertChained` 메서드를 사용하면 [잡 체인](/docs/{{version}}/queues#job-chaining)이 디스패치되었는지 주장할 수 있습니다. 첫 번째 인자로 잡 클래스명이 담긴 배열 또는 실제 인스턴스 배열을 받을 수 있습니다.

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

실제 잡 인스턴스 배열도 사용할 수 있습니다. 이때 Laravel은 디스패치된 잡 체인과 클래스 및 프로퍼티 값이 동일한지 검사합니다.

```php
Bus::assertChained([
    new ShipOrder,
    new RecordShipment,
    new UpdateInventory,
]);
```

<a name="job-batches"></a>
### 잡 배치

`Bus` 파사드의 `assertBatched` 메서드는 [잡배치](/docs/{{version}}/queues#job-batching)가 디스패치되었는지 주장할 때 사용합니다. 클로저는 `Illuminate\Bus\PendingBatch` 인스턴스를 받아 배치 내 잡을 검사할 수 있습니다.

```php
use Illuminate\Bus\PendingBatch;
use Illuminate\Support\Facades\Bus;

Bus::assertBatched(function (PendingBatch $batch) {
    return $batch->name == 'import-csv' &&
           $batch->jobs->count() === 10;
});
```

<a name="event-fake"></a>
## 이벤트 페이크

이벤트를 디스패치하는 코드를 테스트할 때, Laravel이 이벤트 리스너를 실제로 실행하지 않도록 할 수 있습니다. `Event` 파사드의 `fake` 메서드를 사용하면 리스너 실행을 막고, 코드 실행 후 `assertDispatched`, `assertNotDispatched`, `assertNothingDispatched`를 통해 어떤 이벤트가 디스패치되었는지 주장할 수 있습니다.

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
     * 주문 배송 테스트
     */
    public function test_orders_can_be_shipped()
    {
        Event::fake();

        // 주문 배송 수행...

        // 이벤트가 디스패치 되었는지 주장
        Event::assertDispatched(OrderShipped::class);

        // 이벤트가 2번 디스패치 되었는지 주장
        Event::assertDispatched(OrderShipped::class, 2);

        // 이벤트가 디스패치되지 않았는지 주장
        Event::assertNotDispatched(OrderFailedToShip::class);

        // 아무 이벤트도 디스패치 안됨 주장
        Event::assertNothingDispatched();
    }
}
```

`assertDispatched` 또는 `assertNotDispatched` 메서드에 클로저를 전달하여 특정 "진실 테스트"를 통과하는 이벤트만 주장할 수 있습니다.

```php
Event::assertDispatched(function (OrderShipped $event) use ($order) {
    return $event->order->id === $order->id;
});
```

단순히 이벤트 리스너가 특정 이벤트를 리스닝하는지만 주장하고 싶으면 `assertListening`을 사용할 수 있습니다.

```php
Event::assertListening(
    OrderShipped::class,
    SendShipmentNotification::class
);
```

> {note} `Event::fake()`를 호출하면 이벤트 리스너가 실행되지 않습니다. 따라서 UUID 생성 등 이벤트에 의존하는 모델 팩토리를 사용하는 경우, 팩토리 실행 **이후**에 `Event::fake()`를 호출해야 합니다.

<a name="faking-a-subset-of-events"></a>
#### 특정 이벤트만 페이크 처리하기

특정 이벤트만 리스너를 페이크 처리하고 싶다면, 배열로 넘겨 `fake` 또는 `fakeFor` 메서드를 사용하세요.

```php
/**
 * 주문 처리 테스트
 */
public function test_orders_can_be_processed()
{
    Event::fake([
        OrderCreated::class,
    ]);

    $order = Order::factory()->create();

    Event::assertDispatched(OrderCreated::class);

    // 다른 이벤트들은 정상적으로 디스패치됨
    $order->update([...]);
}
```

<a name="scoped-event-fakes"></a>
### 범위 지정 이벤트 페이크

테스트의 일부 구간에서만 이벤트 리스너를 페이크 처리하고 싶다면 `fakeFor` 메서드를 사용하세요.

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
     * 주문 처리 테스트
     */
    public function test_orders_can_be_processed()
    {
        $order = Event::fakeFor(function () {
            $order = Order::factory()->create();

            Event::assertDispatched(OrderCreated::class);

            return $order;
        });

        // 이후 이벤트는 정상적으로 디스패치되고, 옵저버도 실행됨...
        $order->update([...]);
    }
}
```

<a name="http-fake"></a>
## HTTP 페이크

`Http` 파사드의 `fake` 메서드를 이용하면, HTTP 클라이언트가 요청 시 미리 지정된 더미 응답을 반환하도록 할 수 있습니다. 자세한 내용은 [HTTP 클라이언트 테스트 문서](/docs/{{version}}/http-client#testing)를 참고하세요.

<a name="mail-fake"></a>
## 메일 페이크

`Mail` 파사드의 `fake` 메서드를 통해 실제로 메일을 발송하지 않도록 할 수 있습니다. 대부분, 메일 발송은 실제로 테스트하려는 코드와 직접적인 관련이 없습니다. Laravel이 특정 mailable을 전송하도록 지시했는지를 주장하는 것으로 충분합니다.

`Mail` 파사드의 `fake` 이후, [mailable](/docs/{{version}}/mail)이 전송 지시되었는지, 수신자 등 데이터도 검증할 수 있습니다.

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

        // 주문 배송 수행...

        // 아무 mailable도 전송되지 않았는지
        Mail::assertNothingSent();

        // 특정 mailable 전송 주장
        Mail::assertSent(OrderShipped::class);

        // mailable이 2번 전송되었는지
        Mail::assertSent(OrderShipped::class, 2);

        // mailable이 전송되지 않았는지
        Mail::assertNotSent(AnotherMailable::class);
    }
}
```

백그라운드에서 mailable을 큐에 넣는 경우, `assertSent` 대신 `assertQueued`를 사용해야 합니다.

```php
Mail::assertQueued(OrderShipped::class);

Mail::assertNotQueued(OrderShipped::class);

Mail::assertNothingQueued();
```

`assertSent`, `assertNotSent`, `assertQueued`, `assertNotQueued`에도 클로저를 전달해 특정 조건을 충족하는 mailable 전송을 주장할 수 있습니다.

```php
Mail::assertSent(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

또한 클로저 내 mailable 인스턴스를 통해 수신자 등 정보를 편리하게 검사할 수 있습니다.

```php
Mail::assertSent(OrderShipped::class, function ($mail) use ($user) {
    return $mail->hasTo($user->email) &&
           $mail->hasCc('...') &&
           $mail->hasBcc('...');
});
```

메일 전송이 없음을 주장하는 방법은 `assertNotSent`와 `assertNotQueued` 두 가지가 있으며, 둘 다 만족하는 경우를 위해 `assertNothingOutgoing`과 `assertNotOutgoing`를 사용할 수 있습니다.

```php
Mail::assertNothingOutgoing();

Mail::assertNotOutgoing(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```

<a name="notification-fake"></a>
## 알림 페이크

`Notification` 파사드의 `fake` 메서드를 통해 실제로 알림이 전송되지 않도록 할 수 있습니다. 대부분의 경우, Laravel이 특정 알림을 전송하도록 지시했는지만 주장하면 충분합니다.

`Notification` 파사드의 `fake` 이후, [알림](/docs/{{version}}/notifications)이 전송 지시되었는지와 받은 데이터도 검증할 수 있습니다.

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

        // 주문 배송 수행...

        // 아무 알림도 전송되지 않았는지
        Notification::assertNothingSent();

        // 특정 유저에게 알림이 전송됐는지 주장
        Notification::assertSentTo(
            [$user], OrderShipped::class
        );

        // 알림이 전송되지 않았는지 주장
        Notification::assertNotSentTo(
            [$user], AnotherNotification::class
        );
    }
}
```

`assertSentTo`, `assertNotSentTo`에도 클로저를 전달해 특정 조건을 만족하는 알림 전송을 주장할 수 있습니다.

```php
Notification::assertSentTo(
    $user,
    function (OrderShipped $notification, $channels) use ($order) {
        return $notification->order->id === $order->id;
    }
);
```

<a name="on-demand-notifications"></a>
#### 온디맨드 알림

테스트 중 코드가 [온디맨드 알림](/docs/{{version}}/notifications#on-demand-notifications)을 전송한다면, 반드시 `Illuminate\Notifications\AnonymousNotifiable` 인스턴스로 전송 여부를 주장해야 합니다.

```php
use Illuminate\Notifications\AnonymousNotifiable;

Notification::assertSentTo(
    new AnonymousNotifiable, OrderShipped::class
);
```

알림 주장 메서드의 세 번째 인자로 클로저를 전달하면, 온디맨드 알림이 올바른 "라우트" 주소로 전송되었는지 검사할 수 있습니다.

```php
Notification::assertSentTo(
    new AnonymousNotifiable,
    OrderShipped::class,
    function ($notification, $channels, $notifiable) use ($user) {
        return $notifiable->routes['mail'] === $user->email;
    }
);
```

<a name="queue-fake"></a>
## 큐 페이크

`Queue` 파사드의 `fake` 메서드를 사용해 실제 큐 작업이 발생하지 않도록 할 수 있습니다. 일반적으로, 특정 잡이 큐에 전송되었는지만 주장하면 됩니다. 큐 잡 자체는 별도 테스트 클래스로 검증하세요.

`Queue` 파사드의 `fake` 이후, 애플리케이션이 잡을 큐에 넣으려 했는지 주장할 수 있습니다.

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

        // 주문 배송 ...

        // 아무 잡도 큐에 안 넣었는지
        Queue::assertNothingPushed();

        // 특정 큐에 잡이 들어갔는지
        Queue::assertPushedOn('queue-name', ShipOrder::class);

        // 잡이 2번 들어갔는지
        Queue::assertPushed(ShipOrder::class, 2);

        // 잡이 안 들어갔는지
        Queue::assertNotPushed(AnotherJob::class);
    }
}
```

`assertPushed`, `assertNotPushed`에도 클로저를 전달해 특정 조건에 부합하는 잡 전송을 주장할 수 있습니다.

```php
Queue::assertPushed(function (ShipOrder $job) use ($order) {
    return $job->order->id === $order->id;
});
```

<a name="job-chains"></a>
### 잡 체인

`Queue` 파사드의 `assertPushedWithChain`과 `assertPushedWithoutChain`으로 잡이 체인과 함께 혹은 별개로 큐에 들어갔는지 주장할 수 있습니다.

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

실제 잡 인스턴스 배열로도 주장할 수 있습니다.

```php
Queue::assertPushedWithChain(ShipOrder::class, [
    new RecordShipment,
    new UpdateInventory,
]);
```

잡이 체인 없이 큐에 들어갔는지 확인하려면 `assertPushedWithoutChain`을 사용하세요.

```php
Queue::assertPushedWithoutChain(ShipOrder::class);
```

<a name="storage-fake"></a>
## 스토리지 페이크

`Storage` 파사드의 `fake` 메서드를 이용하면, `Illuminate\Http\UploadedFile`의 파일 생성 유틸리티와 결합해 파일 업로드 테스트를 간편하게 할 수 있습니다. 예시:

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

        // 파일 저장 여부 주장
        Storage::disk('photos')->assertExists('photo1.jpg');
        Storage::disk('photos')->assertExists(['photo1.jpg', 'photo2.jpg']);

        // 파일 미저장 주장
        Storage::disk('photos')->assertMissing('missing.jpg');
        Storage::disk('photos')->assertMissing(['missing.jpg', 'non-existing.jpg']);
    }
}
```

파일 업로드 테스트에 대한 더 자세한 내용은 [HTTP 테스트 문서의 파일 업로드](/docs/{{version}}/http-tests#testing-file-uploads) 부분을 참고하세요.

> {tip} 기본적으로, `fake` 메서드는 임시 디렉터리의 모든 파일을 삭제합니다. 파일을 유지하고 싶다면 `persistentFake` 메서드를 사용하세요.

<a name="interacting-with-time"></a>
## 시간 조작

테스트 중, `now` 또는 `Illuminate\Support\Carbon::now()`와 같은 헬퍼가 반환하는 시간을 수정해야 할 때가 있습니다. Laravel의 기본 기능 테스트 클래스에는 현재 시간을 조작할 수 있는 헬퍼가 내장되어 있습니다.

```php
public function testTimeCanBeManipulated()
{
    // 미래로 이동
    $this->travel(5)->milliseconds();
    $this->travel(5)->seconds();
    $this->travel(5)->minutes();
    $this->travel(5)->hours();
    $this->travel(5)->days();
    $this->travel(5)->weeks();
    $this->travel(5)->years();

    // 과거로 이동
    $this->travel(-5)->hours();

    // 특정 시간으로 이동
    $this->travelTo(now()->subHours(6));

    // 현재로 복귀
    $this->travelBack();
}
```
