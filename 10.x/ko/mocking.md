# Mocking (모킹)

- [소개](#introduction)
- [객체 모킹](#mocking-objects)
- [페이사드 모킹](#mocking-facades)
    - [페이사드 스파이](#facade-spies)
- [시간 조작하기](#interacting-with-time)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel 애플리케이션을 테스트할 때, 특정 부분이 실제로 실행되지 않게 "모킹(mock)"하고 싶을 수 있습니다. 예를 들어, 이벤트를 디스패치하는 컨트롤러를 테스트할 때 이벤트 리스너가 실제로 실행되지는 않도록 모킹하여, 테스트가 컨트롤러의 HTTP 응답에만 집중되도록 할 수 있습니다. 이벤트 리스너 자체는 별도의 테스트 케이스에서 검증하면 됩니다.

Laravel은 이벤트, 작업(job), 그리고 기타 페이사드(facade)를 쉽게 모킹할 수 있도록 여러 메서드를 기본 제공하며, 이들은 주로 Mockery를 수동으로 복잡하게 호출하지 않아도 되도록 편리한 래퍼(wrapper)를 제공합니다.

<a name="mocking-objects"></a>
## 객체 모킹 (Mocking Objects)

객체를 Laravel의 [서비스 컨테이너](/docs/10.x/container)를 통해 주입할 때, 모킹된 인스턴스를 컨테이너에 `instance` 바인딩으로 등록해야 합니다. 이렇게 하면 Laravel 컨테이너가 직접 객체를 생성하는 대신 모킹된 인스턴스를 사용하게 됩니다:

```
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

더 편리하게는 Laravel 기본 테스트 케이스 클래스가 제공하는 `mock` 메서드를 사용할 수 있습니다. 아래 예제는 위의 코드와 결과가 동일합니다:

```
use App\Service;
use Mockery\MockInterface;

$mock = $this->mock(Service::class, function (MockInterface $mock) {
    $mock->shouldReceive('process')->once();
});
```

객체의 일부 메서드만 모킹하고 싶을 때는 `partialMock` 메서드를 사용하세요. 모킹되지 않은 메서드는 호출 시 정상적으로 실행됩니다:

```
use App\Service;
use Mockery\MockInterface;

$mock = $this->partialMock(Service::class, function (MockInterface $mock) {
    $mock->shouldReceive('process')->once();
});
```

또한, [스파이(spy)](http://docs.mockery.io/en/latest/reference/spies.html)를 사용하고 싶다면 Laravel 기본 테스트 케이스 클래스가 제공하는 `spy` 메서드를 사용할 수 있습니다. 스파이는 모킹과 비슷하지만, 코드 실행 중 발생하는 모든 상호작용을 기록하여 실행 후 검증(assertion)을 할 수 있습니다:

```
use App\Service;

$spy = $this->spy(Service::class);

// ...

$spy->shouldHaveReceived('process');
```

<a name="mocking-facades"></a>
## 페이사드 모킹 (Mocking Facades)

전통적인 정적 메서드 호출과 달리, [페이사드](/docs/10.x/facades) (실시간 페이사드 포함)도 모킹할 수 있습니다. 이는 전통적인 정적 클래스 호출보다 훨씬 테스트하기 쉬우며, 의존성 주입을 사용하는 것과 동등한 테스트 가능성을 제공합니다. 테스트 시 컨트롤러 내에서 호출되는 Laravel 페이사드를 모킹하는 경우가 많습니다. 예를 들어, 다음 컨트롤러 액션을 보세요:

```
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Cache;

class UserController extends Controller
{
    /**
     * 애플리케이션의 모든 사용자 목록을 가져옵니다.
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

`Cache` 페이사드에 대한 호출을 `shouldReceive` 메서드를 사용해 모킹할 수 있으며, 이는 [Mockery](https://github.com/padraic/mockery) 모킹 인스턴스를 반환합니다. 페이사드는 실제로 Laravel [서비스 컨테이너](/docs/10.x/container)에 의해 해결되고 관리되기 때문에 전형적인 정적 클래스보다 훨씬 테스트하기 좋습니다. 다음은 `Cache` 페이사드의 `get` 메서드를 모킹하는 예시입니다:

```
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
> `Request` 페이사드는 모킹하지 말고, 대신 테스트 실행 시 `get`이나 `post` 같은 [HTTP 테스트 메서드](/docs/10.x/http-tests)에 원하는 입력을 전달하세요. 마찬가지로, `Config` 페이사드를 모킹하는 대신 테스트 내에서 `Config::set` 메서드를 호출하는 것을 권장합니다.

<a name="facade-spies"></a>
### 페이사드 스파이 (Facade Spies)

페이사드에 대해 [스파이](http://docs.mockery.io/en/latest/reference/spies.html)를 사용하려면 해당 페이사드의 `spy` 메서드를 호출하면 됩니다. 스파이는 모킹과 유사하지만, 코드 실행 중 페이사드와의 모든 상호작용을 기록하여 실행 후 검증할 수 있습니다:

```
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
## 시간 조작하기 (Interacting With Time)

테스트 중에 `now` 또는 `Illuminate\Support\Carbon::now()`와 같은 시간 관련 헬퍼가 반환하는 시간을 수정해야 할 때가 있습니다. 다행히도 Laravel 기본 기능 테스트 클래스에는 현재 시간을 조작할 수 있는 헬퍼가 포함되어 있습니다:

```
use Illuminate\Support\Carbon;

public function test_time_can_be_manipulated(): void
{
    // 미래로 여행하기...
    $this->travel(5)->milliseconds();
    $this->travel(5)->seconds();
    $this->travel(5)->minutes();
    $this->travel(5)->hours();
    $this->travel(5)->days();
    $this->travel(5)->weeks();
    $this->travel(5)->years();

    // 과거로 여행하기...
    $this->travel(-5)->hours();

    // 특정 시점으로 이동하기...
    $this->travelTo(now()->subHours(6));

    // 현재 시점으로 되돌아가기...
    $this->travelBack();
}
```

다양한 시간 여행 메서드는 클로저를 인수로 받을 수도 있습니다. 클로저는 특정 시간에 시간이 멈춘 상태로 실행되고, 클로저 실행이 끝나면 시간 흐름이 정상적으로 돌아옵니다:

```
$this->travel(5)->days(function () {
    // 5일 후에 무언가를 테스트...
});

$this->travelTo(now()->subDays(10), function () {
    // 특정 시점에서 무언가를 테스트...
});
```

`freezeTime` 메서드는 현재 시간을 고정(freeze)할 때 사용합니다. 비슷하게 `freezeSecond` 메서드는 현재 초 단위의 시작 시점에서 시간을 고정합니다:

```
use Illuminate\Support\Carbon;

// 시간을 고정한 뒤 클로저 실행이 끝나면 정상 시간 흐름으로 복귀...
$this->freezeTime(function (Carbon $time) {
    // ...
});

// 현재 초로 시간을 고정하고 클로저 실행 후 정상 시간 흐름 복귀...
$this->freezeSecond(function (Carbon $time) {
    // ...
})
```

위에서 설명한 모든 메서드는 주로 토론 게시판의 비활성 게시물을 잠그는 등 시간에 민감한 애플리케이션 동작을 테스트할 때 유용합니다:

```
use App\Models\Thread;

public function test_forum_threads_lock_after_one_week_of_inactivity()
{
    $thread = Thread::factory()->create();
    
    $this->travel(1)->week();
    
    $this->assertTrue($thread->isLockedByInactivity());
}
```