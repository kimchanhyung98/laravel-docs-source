# Mocking

- [소개](#introduction)
- [객체 모킹](#mocking-objects)
- [파사드 모킹](#mocking-facades)
    - [파사드 스파이](#facade-spies)
- [시간 다루기](#interacting-with-time)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel 애플리케이션을 테스트할 때, 특정 부분이 실제로 실행되지 않도록 "모킹(mock)"하고 싶을 수 있습니다. 예를 들어, 이벤트를 디스패치하는 컨트롤러를 테스트할 때 이벤트 리스너가 실제로 실행되지 않도록 모킹하여, 이벤트 리스너의 실행에 신경 쓰지 않고 컨트롤러의 HTTP 응답만 테스트할 수 있습니다. 이벤트 리스너는 별도의 테스트 케이스에서 따로 테스트할 수 있기 때문입니다.

Laravel은 이벤트, 잡, 그리고 다양한 파사드를 모킹할 수 있는 유용한 메서드를 기본적으로 제공합니다. 이 헬퍼들은 주로 복잡한 Mockery 메서드 호출을 수동으로 작성하지 않도록 편리한 래퍼 역할을 합니다.

<a name="mocking-objects"></a>
## 객체 모킹 (Mocking Objects)

Laravel의 [서비스 컨테이너](/docs/master/container)를 통해 주입되는 객체를 모킹하려면, 모킹된 인스턴스를 컨테이너에 `instance` 바인딩으로 등록해야 합니다. 이렇게 하면 Laravel은 원래 객체를 새로 생성하는 대신, 모킹된 인스턴스를 사용합니다:

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

이를 더 편리하게 하려면 Laravel 기본 테스트 케이스 클래스에서 제공하는 `mock` 메서드를 사용할 수 있습니다. 예를 들어, 아래 예시는 위와 동일한 기능을 수행합니다:

```php
use App\Service;
use Mockery\MockInterface;

$mock = $this->mock(Service::class, function (MockInterface $mock) {
    $mock->shouldReceive('process')->once();
});
```

객체의 일부 메서드만 모킹하고 싶을 때는 `partialMock` 메서드를 사용하세요. 모킹하지 않은 메서드는 호출 시 평소처럼 실제 메서드가 실행됩니다:

```php
use App\Service;
use Mockery\MockInterface;

$mock = $this->partialMock(Service::class, function (MockInterface $mock) {
    $mock->shouldReceive('process')->once();
});
```

유사하게, [스파이(spy)](http://docs.mockery.io/en/latest/reference/spies.html)를 사용하려면 Laravel 기본 테스트 케이스의 `spy` 메서드를 사용할 수 있습니다. 스파이는 모킹과 비슷하지만, 테스트 대상 코드와 스파이 객체 간의 모든 상호작용을 기록하여, 실행 후에 해당 상호작용을 검증할 수 있다는 차이가 있습니다:

```php
use App\Service;

$spy = $this->spy(Service::class);

// ...

$spy->shouldHaveReceived('process');
```

<a name="mocking-facades"></a>
## 파사드 모킹 (Mocking Facades)

전통적인 정적 메서드 호출과 달리, [파사드](/docs/master/facades) (실시간 파사드 포함)도 모킹할 수 있습니다. 이 덕분에 전통적인 정적 메서드보다 훨씬 테스트하기 쉽고, 전통적인 의존성 주입을 사용하는 것과 동일한 수준의 테스트 가능성을 가질 수 있습니다. 테스트할 때 컨트롤러 내에서 호출되는 Laravel 파사드를 모킹하고 싶을 때가 많습니다. 예를 들어 아래와 같은 컨트롤러 액션을 생각해봅시다:

```php
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

`Cache` 파사드의 호출을 `shouldReceive` 메서드로 모킹할 수 있으며, 이 메서드는 [Mockery](https://github.com/padraic/mockery) 모킹 인스턴스를 반환합니다. 파사드는 실제로 Laravel [서비스 컨테이너](/docs/master/container)에서 해결 및 관리되므로 일반적인 정적 클래스보다 훨씬 테스트하기 쉽습니다. 예를 들어, `Cache` 파사드의 `get` 메서드 호출을 모킹해봅시다:

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
> `Request` 파사드는 모킹하지 마세요. 대신 테스트 실행 시 `get`, `post` 등의 [HTTP 테스트 메서드](/docs/master/http-tests)에 필요한 입력을 전달하세요. 마찬가지로 `Config` 파사드를 모킹하지 마시고 테스트에서 `Config::set` 메서드를 호출하세요.

<a name="facade-spies"></a>
### 파사드 스파이 (Facade Spies)

파사드에 대해 [스파이](http://docs.mockery.io/en/latest/reference/spies.html)를 사용하고 싶다면, 해당 파사드에서 `spy` 메서드를 호출하면 됩니다. 스파이는 모킹과 비슷하지만, 테스트 대상 코드와 스파이 사이의 모든 상호작용을 기록하여 코드 실행 후 검증할 수 있습니다:

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
## 시간 다루기 (Interacting With Time)

테스트 중에 `now` 헬퍼나 `Illuminate\Support\Carbon::now()` 같은 시간이 반환하는 값을 가끔 조작할 필요가 있습니다. 다행히도 Laravel 기본 기능 테스트 클래스는 현재 시간을 조작할 수 있는 헬퍼 메서드를 제공합니다:

```php tab=Pest
test('time can be manipulated', function () {
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

    // 특정 시점으로 이동...
    $this->travelTo(now()->subHours(6));

    // 현재 시간으로 복귀...
    $this->travelBack();
});
```

```php tab=PHPUnit
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

    // 특정 시점으로 이동...
    $this->travelTo(now()->subHours(6));

    // 현재 시간으로 복귀...
    $this->travelBack();
}
```

다양한 시간 이동 메서드에는 클로저를 전달할 수도 있습니다. 이 클로저는 지정된 시점으로 시간이 멈춘 상태에서 실행되며, 클로저 실행이 끝나면 시간은 평소대로 흐릅니다:

```php
$this->travel(5)->days(function () {
    // 앞으로 5일 후 상황을 테스트...
});

$this->travelTo(now()->subDays(10), function () {
    // 특정 순간의 상황을 테스트...
});
```

`freezeTime` 메서드를 사용하면 현재 시간을 멈출 수 있으며, `freezeSecond` 메서드는 현재 초의 시작 시점에서 시간을 멈춥니다. 두 메서드 모두 클로저 내에서 시간이 고정되고 실행 후 정상으로 돌아갑니다:

```php
use Illuminate\Support\Carbon;

// 시간을 멈추고 클로저 실행 후 정상 복귀...
$this->freezeTime(function (Carbon $time) {
    // ...
});

// 현재 초의 시작 시점에서 시간을 멈추고 클로저 실행 후 정상 복귀...
$this->freezeSecond(function (Carbon $time) {
    // ...
});
```

이러한 메서드들은 주로 토론 포럼에서 일정 기간 활동이 없는 게시글을 잠그는 등, 시간에 민감한 애플리케이션 동작을 테스트할 때 유용합니다:

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