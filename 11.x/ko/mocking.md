# Mocking

- [소개](#introduction)
- [객체 모킹](#mocking-objects)
- [퍼사드(Mock) 모킹](#mocking-facades)
    - [퍼사드 스파이](#facade-spies)
- [시간과 상호작용](#interacting-with-time)

<a name="introduction"></a>
## 소개

Laravel 애플리케이션을 테스트할 때, 테스트 중 실제로 실행되지 않도록 애플리케이션의 특정 부분을 "모킹(Mock)"하고 싶을 수 있습니다. 예를 들어, 이벤트를 디스패치하는 컨트롤러를 테스트할 때, 실제로 이벤트 리스너가 실행되지 않도록 리스너를 모킹할 수 있습니다. 이렇게 하면 이벤트 리스너의 실행을 걱정하지 않고 컨트롤러의 HTTP 응답만을 테스트할 수 있으며, 이벤트 리스너는 별도의 테스트 케이스에서 시험할 수 있습니다.

Laravel은 이벤트, 잡, 그리고 기타 퍼사드의 모킹을 위한 유용한 메서드들을 기본적으로 제공합니다. 이러한 헬퍼들은 주로 Mockery 위에 편의 계층을 제공하므로, 복잡한 Mockery 호출을 직접 작성하지 않아도 됩니다.

<a name="mocking-objects"></a>
## 객체 모킹

Laravel의 [서비스 컨테이너](/docs/{{version}}/container)를 통해 애플리케이션에 주입될 객체를 모킹하려면, `instance` 바인딩으로 모킹된 인스턴스를 컨테이너에 바인딩해야 합니다. 이렇게 하면 컨테이너가 객체를 직접 생성하는 대신, 모킹된 인스턴스를 사용하도록 지시할 수 있습니다.

```php tab=Pest
use App\Service;
use Mockery;
use Mockery\MockInterface;

test('something can be mocked', function () {
    $this->instance(
        Service::class,
        Mockery::mock(Service::class, function (MockInterface $mock) {
            $mock->shouldReceive('process')->once();
        })
    );
});
```

```php tab=PHPUnit
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

이 작업을 더 간편하게 하기 위해, Laravel의 기본 테스트 케이스 클래스에서는 `mock` 메서드를 제공합니다. 아래 예제는 위 코드와 동일한 동작을 합니다.

    use App\Service;
    use Mockery\MockInterface;

    $mock = $this->mock(Service::class, function (MockInterface $mock) {
        $mock->shouldReceive('process')->once();
    });

객체의 일부 메서드만 모킹해야 할 경우 `partialMock` 메서드를 사용할 수 있습니다. 모킹하지 않은 메서드는 평소처럼 정상적으로 실행됩니다.

    use App\Service;
    use Mockery\MockInterface;

    $mock = $this->partialMock(Service::class, function (MockInterface $mock) {
        $mock->shouldReceive('process')->once();
    });

마찬가지로, 객체에 대해 [스파이](http://docs.mockery.io/en/latest/reference/spies.html) 사용이 필요하다면, Laravel의 기본 테스트 케이스 클래스에서 제공하는 `spy` 메서드를 활용할 수 있습니다. 스파이는 모킹과 비슷하지만, 테스트되는 코드와의 모든 상호작용을 기록하므로 코드 실행 후에도 어설션을 할 수 있습니다.

    use App\Service;

    $spy = $this->spy(Service::class);

    // ...

    $spy->shouldHaveReceived('process');

<a name="mocking-facades"></a>
## 퍼사드(Mock) 모킹

전통적인 정적 메서드 호출과 달리, [퍼사드](/docs/{{version}}/facades) (그리고 [실시간 퍼사드](/docs/{{version}}/facades#real-time-facades))는 모킹이 가능합니다. 이 점은 전통적인 정적 메서드 호출 방식보다 큰 장점이며, 의존성 주입과 동일한 수준의 테스트 용이성을 제공합니다. 테스트 시 컨트롤러에서 발생하는 Laravel 퍼사드 호출을 자주 모킹할 수 있습니다. 예를 들어, 아래와 같은 컨트롤러 액션을 살펴봅시다.

    <?php

    namespace App\Http\Controllers;

    use Illuminate\Support\Facades\Cache;

    class UserController extends Controller
    {
        /**
         * 애플리케이션의 모든 사용자 목록을 조회합니다.
         */
        public function index(): array
        {
            $value = Cache::get('key');

            return [
                // ...
            ];
        }
    }

`Cache` 퍼사드 호출을 [Mockery](https://github.com/padraic/mockery) 모킹 인스턴스를 반환하는 `shouldReceive` 메서드로 모킹할 수 있습니다. 퍼사드는 Laravel [서비스 컨테이너](/docs/{{version}}/container)에 의해 실제로 해석되고 관리되기 때문에, 일반적인 정적 클래스보다 훨씬 뛰어난 테스트 용이성을 갖습니다. 아래는 `Cache` 퍼사드의 `get` 메서드 호출을 모킹하는 예시입니다.

```php tab=Pest
<?php

use Illuminate\Support\Facades\Cache;

test('get index', function () {
    Cache::shouldReceive('get')
        ->once()
        ->with('key')
        ->andReturn('value');

    $response = $this->get('/users');

    // ...
});
```

```php tab=PHPUnit
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
> `Request` 퍼사드는 모킹하지 말아야 합니다. 대신, 테스트를 실행할 때 [HTTP 테스트 메서드](/docs/{{version}}/http-tests)인 `get`, `post` 등에 원하는 입력값을 전달하세요. 마찬가지로, `Config` 퍼사드를 모킹하는 대신 테스트 내에서 `Config::set` 메서드를 호출해야 합니다.

<a name="facade-spies"></a>
### 퍼사드 스파이

특정 퍼사드에서 [스파이](http://docs.mockery.io/en/latest/reference/spies.html)를 사용하고 싶다면 해당 퍼사드의 `spy` 메서드를 호출하면 됩니다. 스파이는 모킹과 유사하지만, 테스트되는 코드와의 상호작용을 기록하여 코드 실행 후 어설션 검증이 가능합니다.

```php tab=Pest
<?php

use Illuminate\Support\Facades\Cache;

test('values are be stored in cache', function () {
    Cache::spy();

    $response = $this->get('/');

    $response->assertStatus(200);

    Cache::shouldHaveReceived('put')->once()->with('name', 'Taylor', 10);
});
```

```php tab=PHPUnit
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
## 시간과 상호작용

테스트 시, `now` 또는 `Illuminate\Support\Carbon::now()`와 같은 헬퍼가 반환하는 시간을 임의로 변경해야 할 때가 있습니다. 다행히 Laravel의 기본 기능 테스트 클래스는 현재 시간을 조작할 수 있는 헬퍼를 제공합니다.

```php tab=Pest
test('time can be manipulated', function () {
    // 미래로 시간 이동...
    $this->travel(5)->milliseconds();
    $this->travel(5)->seconds();
    $this->travel(5)->minutes();
    $this->travel(5)->hours();
    $this->travel(5)->days();
    $this->travel(5)->weeks();
    $this->travel(5)->years();

    // 과거로 시간 이동...
    $this->travel(-5)->hours();

    // 특정 시점으로 이동...
    $this->travelTo(now()->subHours(6));

    // 현재 시간으로 복귀...
    $this->travelBack();
});
```

```php tab=PHPUnit
public function test_time_can_be_manipulated(): void
{
    // 미래로 시간 이동...
    $this->travel(5)->milliseconds();
    $this->travel(5)->seconds();
    $this->travel(5)->minutes();
    $this->travel(5)->hours();
    $this->travel(5)->days();
    $this->travel(5)->weeks();
    $this->travel(5)->years();

    // 과거로 시간 이동...
    $this->travel(-5)->hours();

    // 특정 시점으로 이동...
    $this->travelTo(now()->subHours(6));

    // 현재 시간으로 복귀...
    $this->travelBack();
}
```

다양한 시간 이동 메서드에 클로저를 전달할 수도 있습니다. 클로저 내에서는 지정된 시간으로 고정되며, 클로저 실행이 끝나면 시간이 정상적으로 재개됩니다.

    $this->travel(5)->days(function () {
        // 5일 후의 미래 시간에 대한 테스트...
    });

    $this->travelTo(now()->subDays(10), function () {
        // 특정 시점에서의 동작을 테스트...
    });

현재 시간을 고정하려면 `freezeTime` 메서드를 사용할 수 있습니다. 유사하게, `freezeSecond`는 현재 초의 시작 지점에서 시간을 고정합니다.

    use Illuminate\Support\Carbon;

    // 시간을 고정하고, 클로저 실행 후 정상적으로 시간 재개...
    $this->freezeTime(function (Carbon $time) {
        // ...
    });

    // 현재 초의 시작점에서 시간을 고정한 뒤, 클로저 실행 후 정상적으로 시간 재개...
    $this->freezeSecond(function (Carbon $time) {
        // ...
    })

이 메서드들은 주로 포럼의 비활성 게시글 잠금처럼 시간에 민감한 애플리케이션 동작을 테스트할 때 유용합니다.

```php tab=Pest
use App\Models\Thread;

test('forum threads lock after one week of inactivity', function () {
    $thread = Thread::factory()->create();

    $this->travel(1)->week();

    expect($thread->isLockedByInactivity())->toBeTrue();
});
```

```php tab=PHPUnit
use App\Models\Thread;

public function test_forum_threads_lock_after_one_week_of_inactivity()
{
    $thread = Thread::factory()->create();

    $this->travel(1)->week();

    $this->assertTrue($thread->isLockedByInactivity());
}
```