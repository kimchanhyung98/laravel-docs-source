# Mocking

- [소개](#introduction)
- [객체 목킹](#mocking-objects)
- [파사드 목킹](#mocking-facades)
    - [파사드 스파이](#facade-spies)
- [시간 조작](#interacting-with-time)

<a name="introduction"></a>
## 소개

Laravel 애플리케이션을 테스트할 때, 특정 부분이 실제로 실행되지 않도록 "목(mock)" 처리하고 싶을 때가 있습니다. 예를 들어, 이벤트를 디스패치하는 컨트롤러를 테스트할 때, 이벤트 리스너를 목킹하여 테스트 중에는 실제로 실행되지 않도록 할 수 있습니다. 이렇게 하면 이벤트 리스너의 동작을 걱정하지 않고도 컨트롤러의 HTTP 응답만 테스트할 수 있습니다. 이벤트 리스너 자체는 별도의 테스트 케이스에서 테스트할 수 있기 때문입니다.

Laravel은 이벤트, 잡, 기타 파사드를 목킹하기 위한 유용한 메서드를 기본적으로 제공합니다. 이 헬퍼들은 대부분 복잡한 Mockery 메서드 호출을 직접 작성할 필요 없이 편리하게 사용할 수 있도록 Mockery 위에 편의층을 제공합니다.

<a name="mocking-objects"></a>
## 객체 목킹

Laravel의 [서비스 컨테이너](/docs/{{version}}/container)를 통해 애플리케이션에 주입될 객체를 목킹할 경우, 해당 목킹 인스턴스를 `instance` 바인딩으로 컨테이너에 바인딩해야 합니다. 이렇게 하면 컨테이너가 직접 객체를 생성하는 대신, 여러분이 만든 목킹 인스턴스를 사용하도록 지정할 수 있습니다:

```php
use App\Service;
use Mockery;
use Mockery\MockInterface;

public function test_something_can_be_mocked(): void
{
    $this->instance(
        Service::class,
        Mockery::mock(Service::class, function (MockInterface $mock) {
            $mock->shouldReceive('process')->once();
        })
    );
}
```

이를 더욱 편리하게 하기 위해, Laravel의 기본 테스트 케이스 클래스에서는 `mock` 메서드를 제공합니다. 예를 들어, 다음 예제는 위 예제와 동일하게 동작합니다:

```php
use App\Service;
use Mockery\MockInterface;

$mock = $this->mock(Service::class, function (MockInterface $mock) {
    $mock->shouldReceive('process')->once();
});
```

객체의 일부 메서드만 목킹하고 싶을 때는 `partialMock` 메서드를 사용할 수 있습니다. 목킹하지 않은 메서드는 호출 시 정상적으로 실행됩니다:

```php
use App\Service;
use Mockery\MockInterface;

$mock = $this->partialMock(Service::class, function (MockInterface $mock) {
    $mock->shouldReceive('process')->once();
});
```

마찬가지로, 객체를 [스파이](http://docs.mockery.io/en/latest/reference/spies.html)하고 싶다면, Laravel의 기본 테스트 케이스 클래스에는 `Mockery::spy` 메서드의 편리한 래퍼로서 `spy` 메서드도 존재합니다. 스파이는 목과 유사하지만, 테스트되는 코드와의 모든 상호작용을 기록하므로 코드 실행 후에 어설션을 할 수 있습니다:

```php
use App\Service;

$spy = $this->spy(Service::class);

// ...

$spy->shouldHaveReceived('process');
```

<a name="mocking-facades"></a>
## 파사드 목킹

전통적인 정적(static) 메서드 호출과 달리, [파사드](/docs/{{version}}/facades)([실시간 파사드](/docs/{{version}}/facades#real-time-facades) 포함)는 목킹할 수 있습니다. 이는 전통적인 정적 메서드에 비해 큰 장점을 제공하며, 기존의 의존성 주입을 사용하는 것과 동일한 테스트 용이성을 제공해줍니다. 테스트할 때는 컨트롤러 내에서 사용하는 Laravel 파사드 호출을 목킹하고 싶을 때가 많습니다. 예를 들어, 다음과 같은 컨트롤러 액션을 생각해볼 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Cache;

class UserController extends Controller
{
    /**
     * 애플리케이션의 모든 사용자 목록 조회
     */
    public function index(): array
    {
        $value = Cache::get('key');

        return [
            // ...
        ];
    }
}
```

`Cache` 파사드 호출은 `shouldReceive` 메서드를 사용하여 목킹할 수 있습니다. 이 메서드는 [Mockery](https://github.com/padraic/mockery) 목 인스턴스를 반환합니다. 파사드는 실제로 Laravel [서비스 컨테이너](/docs/{{version}}/container)에 의해 해석되고 관리되기 때문에, 전통적인 정적 클래스보다 훨씬 더 테스트에 적합합니다. 예를 들어, `Cache` 파사드의 `get` 메서드 호출을 목킹해보겠습니다:

```php
<?php

namespace Tests\Feature;

use Illuminate\Support\Facades\Cache;
use Tests\TestCase;

class UserControllerTest extends TestCase
{
    public function test_get_index(): void
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
> `Request` 파사드는 목킹하지 마세요. 대신 테스트 실행 시 [HTTP 테스트 메서드](/docs/{{version}}/http-tests)에서 원하는 입력값을 `get`이나 `post`로 전달하세요. 마찬가지로, `Config` 파사드를 목킹하는 대신 테스트 내에서 `Config::set` 메서드를 호출하세요.

<a name="facade-spies"></a>
### 파사드 스파이

파사드를 [스파이](http://docs.mockery.io/en/latest/reference/spies.html)하고 싶을 경우, 해당 파사드의 `spy` 메서드를 사용할 수 있습니다. 스파이는 목과 유사하지만, 테스트 코드와의 모든 상호작용을 기록하여, 코드 실행 후 어설션을 할 수 있도록 도와줍니다:

```php
use Illuminate\Support\Facades\Cache;

public function test_values_are_be_stored_in_cache(): void
{
    Cache::spy();

    $response = $this->get('/');

    $response->assertStatus(200);

    Cache::shouldHaveReceived('put')->once()->with('name', 'Taylor', 10);
}
```

<a name="interacting-with-time"></a>
## 시간 조작

테스트 과정에서 `now` 또는 `Illuminate\Support\Carbon::now()`와 같은 헬퍼가 반환하는 시간을 임의로 변경해야 할 때가 있습니다. 다행히도, Laravel의 기본 기능 테스트 케이스 클래스에는 현재 시간을 조작할 수 있는 헬퍼가 포함되어 있습니다:

```php
use Illuminate\Support\Carbon;

public function test_time_can_be_manipulated(): void
{
    // 미래로 이동...
    $this->travel(5)->milliseconds();
    $this->travel(5)->seconds();
    $this->travel(5)->minutes();
    $this->travel(5)->hours();
    $this->travel(5)->days();
    $this->travel(5)->weeks();
    $this->travel(5)->years();

    // 과거로 이동...
    $this->travel(-5)->hours();

    // 특정 시간으로 이동...
    $this->travelTo(now()->subHours(6));

    // 현재 시각으로 복귀...
    $this->travelBack();
}
```

여러 시간 이동 메서드에는 클로저를 전달할 수도 있습니다. 해당 시간에 멈춰진 상태로 클로저가 실행되며, 클로저 실행이 끝나면 시간이 정상적으로 다시 흐릅니다:

```php
$this->travel(5)->days(function () {
    // 미래 5일 후의 테스트...
});

$this->travelTo(now()->subDays(10), function () {
    // 특정 시간대에서의 테스트...
});
```

`freezeTime` 메서드를 사용하면 현재 시간을 고정할 수 있습니다. 비슷하게, `freezeSecond`는 현재 초의 시작 시점에 시간을 고정합니다:

```php
use Illuminate\Support\Carbon;

// 시간을 고정하고, 클로저 실행 후 정상 시간으로 복귀...
$this->freezeTime(function (Carbon $time) {
    // ...
});

// 현재 초의 시점에 시간을 고정하고, 클로저 실행 후 정상 시간으로 복귀...
$this->freezeSecond(function (Carbon $time) {
    // ...
});
```

위에서 설명한 모든 메서드는 주로 시간에 민감한 애플리케이션 동작을 테스트할 때 유용합니다. 예를 들어, 토론 포럼에서 비활성 스레드를 일정 기간 후 잠그는 기능을 테스트할 수 있습니다:

```php
use App\Models\Thread;

public function test_forum_threads_lock_after_one_week_of_inactivity()
{
    $thread = Thread::factory()->create();
    
    $this->travel(1)->week();
    
    $this->assertTrue($thread->isLockedByInactivity());
}
```