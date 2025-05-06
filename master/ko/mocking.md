# Mocking

- [소개](#introduction)
- [객체 모킹](#mocking-objects)
- [파사드 모킹](#mocking-facades)
    - [파사드 스파이](#facade-spies)
- [시간과의 상호작용](#interacting-with-time)

<a name="introduction"></a>
## 소개

Laravel 애플리케이션을 테스트할 때 특정 기능이 실제로 실행되지 않도록 "모킹(mock)"하고 싶을 때가 있습니다. 예를 들어, 이벤트를 디스패치하는 컨트롤러를 테스트할 때 이벤트 리스너가 실제로 실행되지 않도록 모킹할 수 있습니다. 이렇게 하면 이벤트 리스너의 동작은 별도의 테스트 케이스에서 검증하고, 현재 테스트에서는 컨트롤러의 HTTP 응답만 검증할 수 있습니다.

Laravel은 이벤트, 잡, 그리고 기타 파사드를 모킹하기 위한 유용한 메서드를 기본적으로 제공합니다. 이들 헬퍼는 Mockery 위에 편의 레이어를 제공하여, 복잡한 Mockery 메서드 호출을 직접 작성하지 않아도 됩니다.

<a name="mocking-objects"></a>
## 객체 모킹

Laravel의 [서비스 컨테이너](/docs/{{version}}/container)를 통해 애플리케이션에 주입될 객체를 모킹할 때는, 모킹한 인스턴스를 `instance` 바인딩으로 컨테이너에 바인딩해야 합니다. 이렇게 하면 컨테이너가 직접 객체를 생성하는 대신, 당신이 지정한 모킹 인스턴스를 사용하도록 할 수 있습니다.

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

이 과정을 더 쉽게 하기 위해, Laravel 기본 테스트 케이스 클래스에서 제공하는 `mock` 메서드를 사용할 수 있습니다. 아래 예시는 위의 예제와 동일한 동작을 수행합니다.

```php
use App\Service;
use Mockery\MockInterface;

$mock = $this->mock(Service::class, function (MockInterface $mock) {
    $mock->shouldReceive('process')->once();
});
```

객체의 일부 메서드만 모킹이 필요할 땐 `partialMock` 메서드를 사용할 수 있습니다. 모킹하지 않은 메서드는 호출 시 정상적으로 실행됩니다.

```php
use App\Service;
use Mockery\MockInterface;

$mock = $this->partialMock(Service::class, function (MockInterface $mock) {
    $mock->shouldReceive('process')->once();
});
```

비슷하게, 객체에 대해 [스파이](http://docs.mockery.io/en/latest/reference/spies.html)를 적용하고 싶을 경우, Laravel의 기본 테스트 케이스 클래스에서 제공하는 `spy` 메서드를 사용할 수 있습니다. 스파이는 모킹과 유사하지만, 테스트 중 해당 객체와의 모든 상호작용을 기록하여 코드 실행 후 이를 검증할 수 있게 해줍니다.

```php
use App\Service;

$spy = $this->spy(Service::class);

// ...

$spy->shouldHaveReceived('process');
```

<a name="mocking-facades"></a>
## 파사드 모킹

기존의 정적 메서드 호출과는 달리, [파사드](/docs/{{version}}/facades) (그리고 [실시간 파사드](/docs/{{version}}/facades#real-time-facades))는 모킹이 가능합니다. 이는 정적 메서드보다 더 나은 테스트 용이성을 제공하며, 전통적인 의존성 주입을 사용하는 것과 동일한 수준의 테스트 유연성을 제공합니다. 테스트 시 컨트롤러 등에서 발생하는 Laravel 파사드 호출을 주로 모킹하게 됩니다. 아래는 예시 컨트롤러입니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Cache;

class UserController extends Controller
{
    /**
     * 모든 사용자 목록을 조회합니다.
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

`Cache` 파사드의 호출은 [Mockery](https://github.com/padraic/mockery) 모킹 인스턴스를 반환하는 `shouldReceive` 메서드를 이용해 모킹할 수 있습니다. 파사드는 Laravel [서비스 컨테이너](/docs/{{version}}/container)에 의해 해석 및 관리되므로 일반 정적 클래스보다 훨씬 높은 테스트 용이성을 제공합니다. 예를 들어, `Cache` 파사드의 `get` 메서드 호출을 다음과 같이 모킹할 수 있습니다.

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
> `Request` 파사드는 모킹하지 말아야 합니다. 대신 테스트를 실행할 때 [HTTP 테스트 메서드](/docs/{{version}}/http-tests)인 `get`, `post` 등에 원하는 입력 값을 전달하세요. 마찬가지로 `Config` 파사드를 모킹하는 대신, 테스트에서 `Config::set` 메서드를 직접 호출하세요.

<a name="facade-spies"></a>
### 파사드 스파이

파사드에 대해 [스파이](http://docs.mockery.io/en/latest/reference/spies.html)를 적용하고 싶을 때는 해당 파사드에서 `spy` 메서드를 호출하면 됩니다. 스파이는 모킹과 비슷하지만, 테스트 중 상호작용을 기록하고 코드가 실행된 후 이를 검증할 수 있습니다.

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
## 시간과의 상호작용

테스트 시 `now` 또는 `Illuminate\Support\Carbon::now()`와 같은 헬퍼가 반환하는 시간을 조작해야 할 때가 있습니다. 다행히도, Laravel의 기본 기능 테스트 클래스는 현재 시간을 조작할 수 있는 헬퍼 메서드를 제공합니다.

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

    // 현재 시점으로 복귀...
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

    // 현재 시점으로 복귀...
    $this->travelBack();
}
```

각종 시간 이동 메서드에 클로저를 전달할 수도 있습니다. 클로저는 지정한 시간에 시간이 "멈춘" 상태로 실행되며, 실행이 끝나면 시간이 정상적으로 다시 흐르기 시작합니다.

```php
$this->travel(5)->days(function () {
    // 5일 후 미래에 대한 테스트...
});

$this->travelTo(now()->subDays(10), function () {
    // 특정 순간에 대한 테스트...
});
```

`freezeTime` 메서드를 사용하면 현재 시간을 고정(freeze)할 수 있습니다. 마찬가지로, `freezeSecond`는 현재 초가 시작되는 시점에 시간을 고정합니다.

```php
use Illuminate\Support\Carbon;

// 시간 고정 후, 클로저 실행이 끝나면 정상 시간으로 복귀...
$this->freezeTime(function (Carbon $time) {
    // ...
});

// 현재 초에 시간 고정 후, 클로저 실행이 끝나면 정상 시간으로 복귀...
$this->freezeSecond(function (Carbon $time) {
    // ...
})
```

위에서 설명한 모든 메서드는 토론 포럼에서 비활성 글을 일정 시간 이후 잠그는 등의 시간에 민감한 애플리케이션 동작을 테스트할 때 특히 유용합니다.

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
