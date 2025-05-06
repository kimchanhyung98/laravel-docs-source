# Mocking

- [소개](#introduction)
- [객체 목(Mock)하기](#mocking-objects)
- [파사드 목(Mock)하기](#mocking-facades)
    - [파사드 스파이](#facade-spies)
- [시간과 상호작용하기](#interacting-with-time)

<a name="introduction"></a>
## 소개

Laravel 애플리케이션을 테스트할 때, 특정 부분이 실제로 실행되지 않도록 "목(mock)" 처리하고 싶을 수 있습니다. 예를 들어, 이벤트를 디스패치하는 컨트롤러를 테스트할 때 이벤트 리스너가 실제로 실행되지 않도록 목킹할 수 있습니다. 이렇게 하면 이벤트 리스너의 동작과는 별개로 컨트롤러의 HTTP 응답만 테스트할 수 있습니다. 이벤트 리스너는 별도의 테스트 케이스에서 검증할 수 있기 때문입니다.

Laravel은 이벤트, 잡, 기타 파사드를 간편하게 목킹할 수 있는 헬퍼 메서드를 기본 제공하며, 이들은 주로 Mockery를 감싸 더 복잡한 Mockery 메서드 호출을 직접 작성하지 않아도 되는 편의성을 제공합니다.

<a name="mocking-objects"></a>
## 객체 목(Mock)하기

Laravel의 [서비스 컨테이너](/docs/{{version}}/container)를 통해 주입되는 객체를 목킹할 때는, `instance` 바인딩으로 목킹된 인스턴스를 컨테이너에 바인딩해야 합니다. 이렇게 하면 컨테이너가 해당 객체의 목킹 인스턴스를 사용하도록 지정할 수 있습니다:

```php tab=Pest
use App\Service;
use Mockery;
use Mockery\MockInterface;

test('something can be mocked', function () {
    $this->instance(
        Service::class,
        Mockery::mock(Service::class, function (MockInterface $mock) {
            $mock->expects('process');
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
            $mock->expects('process');
        })
    );
}
```

이를 더 간단하게 만들기 위해, Laravel의 기본 테스트 케이스 클래스에서는 `mock` 메서드를 제공합니다. 아래 예제는 위와 동일한 동작을 합니다:

```php
use App\Service;
use Mockery\MockInterface;

$mock = $this->mock(Service::class, function (MockInterface $mock) {
    $mock->expects('process');
});
```

객체의 일부 메서드만 목킹해야 한다면, `partialMock` 메서드를 사용할 수 있습니다. 목킹하지 않은 메서드는 정상적으로 실행됩니다:

```php
use App\Service;
use Mockery\MockInterface;

$mock = $this->partialMock(Service::class, function (MockInterface $mock) {
    $mock->expects('process');
});
```

또한, 객체에 대해 [스파이](http://docs.mockery.io/en/latest/reference/spies.html)를 만들고 싶다면, Laravel의 테스트 케이스 클래스에서 `spy` 메서드를 사용할 수 있습니다. 스파이는 Mock과 비슷하지만, 테스트되는 코드와의 상호작용을 모두 기록하여, 코드 실행 이후 해당 상호작용에 대한 어설션을 할 수 있게 해줍니다:

```php
use App\Service;

$spy = $this->spy(Service::class);

// ...

$spy->shouldHaveReceived('process');
```

<a name="mocking-facades"></a>
## 파사드 목(Mock)하기

전통적인 정적(static) 메서드 호출과 달리, [파사드](/docs/{{version}}/facades)([실시간 파사드](/docs/{{version}}/facades#real-time-facades) 포함)는 목킹이 가능합니다. 이는 기존의 정적 메서드에 비해 큰 장점으로, 의존성 주입을 사용할 때와 동일한 테스트 용이성을 제공합니다. 테스트 시 컨트롤러 내부에서 발생하는 Laravel 파사드 호출을 종종 목킹하고 싶을 수 있습니다. 예를 들어, 아래와 같은 컨트롤러 동작을 생각해보세요:

```php
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
```

`Cache` 파사드 호출을 [Mockery](https://github.com/padraic/mockery) 목 인스턴스를 반환하는 `expects` 메서드로 목킹할 수 있습니다. 파사드는 실제로 Laravel의 [서비스 컨테이너](/docs/{{version}}/container)에 의해 해결되고 관리되므로, 일반적인 정적 클래스보다 더 높은 테스트 용이성을 제공합니다. 아래는 `Cache` 파사드의 `get` 메서드 호출을 목킹하는 예시입니다:

```php tab=Pest
<?php

use Illuminate\Support\Facades\Cache;

test('get index', function () {
    Cache::expects('get')
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
        Cache::expects('get')
            ->with('key')
            ->andReturn('value');

        $response = $this->get('/users');

        // ...
    }
}
```

> [!WARNING]
> `Request` 파사드는 목킹하지 않아야 합니다. 대신 원하는 값을 [HTTP 테스트 메서드](/docs/{{version}}/http-tests)인 `get` 또는 `post` 등에 전달하세요. 마찬가지로, `Config` 파사드를 목킹하는 대신 테스트 내에서 `Config::set` 메서드를 사용하세요.

<a name="facade-spies"></a>
### 파사드 스파이

[스파이](http://docs.mockery.io/en/latest/reference/spies.html) 기능을 파사드에도 적용하려면, 해당 파사드의 `spy` 메서드를 호출하면 됩니다. 스파이는 Mock과 유사하나, 테스트 중 코드와의 상호작용을 기록하여 실행 후 어설션에 사용할 수 있습니다:

```php tab=Pest
<?php

use Illuminate\Support\Facades\Cache;

test('values are be stored in cache', function () {
    Cache::spy();

    $response = $this->get('/');

    $response->assertStatus(200);

    Cache::shouldHaveReceived('put')->with('name', 'Taylor', 10);
});
```

```php tab=PHPUnit
use Illuminate\Support\Facades\Cache;

public function test_values_are_be_stored_in_cache(): void
{
    Cache::spy();

    $response = $this->get('/');

    $response->assertStatus(200);

    Cache::shouldHaveReceived('put')->with('name', 'Taylor', 10);
}
```

<a name="interacting-with-time"></a>
## 시간과 상호작용하기

테스트를 진행하다 보면 `now`나 `Illuminate\Support\Carbon::now()`와 같은 헬퍼가 반환하는 시간을 변경해야 할 때가 있습니다. 다행히 Laravel의 기본 기능 테스트 클래스에는 현재 시간을 조작할 수 있는 헬퍼가 포함되어 있습니다:

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

또한 다양한 트래블 메서드에 클로저를 전달할 수도 있습니다. 이 경우 클로저가 실행되는 동안 시간은 고정되어 있으며, 실행이 끝나면 시간이 정상적으로 재개됩니다:

```php
$this->travel(5)->days(function () {
    // 5일 뒤의 미래에서 테스트...
});

$this->travelTo(now()->subDays(10), function () {
    // 특정 시점에서 테스트...
});
```

`freezeTime` 메서드는 현재 시간을 고정할 수 있으며, `freezeSecond`는 현재 초 단위로 시간을 고정합니다:

```php
use Illuminate\Support\Carbon;

// 현재 시간 고정, 클로저 실행 후 시간 정상 재개...
$this->freezeTime(function (Carbon $time) {
    // ...
});

// 현재 초 단위로 시간 고정, 클로저 실행 후 시간 정상 재개...
$this->freezeSecond(function (Carbon $time) {
    // ...
})
```

위에 소개한 메서드들은 주로 시간에 민감한 애플리케이션 동작, 예를 들면 토론 게시판에서 비활성 스레드를 잠그는 기능 등을 테스트할 때 유용합니다:

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
