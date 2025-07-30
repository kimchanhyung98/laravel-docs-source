# 모킹 (Mocking)

- [소개](#introduction)
- [객체 모킹](#mocking-objects)
- [파사드 모킹](#mocking-facades)
    - [파사드 스파이](#facade-spies)
- [시간 다루기](#interacting-with-time)

<a name="introduction"></a>
## 소개

Laravel 애플리케이션을 테스트할 때, 특정 부분이 실제로 실행되지 않도록 "모킹(Mocking)"하고 싶을 수 있습니다. 예를 들어, 이벤트를 디스패치하는 컨트롤러를 테스트할 때, 이벤트 리스너들이 실제로 실행되지 않도록 모킹하면 테스트 도중 리스너의 실행 걱정 없이 오직 컨트롤러의 HTTP 응답만 테스트할 수 있습니다. 이벤트 리스너들은 별도의 테스트 케이스에서 별도로 검증할 수 있기 때문입니다.

Laravel은 기본적으로 이벤트, 잡(job), 그리고 다른 파사드(facade)를 모킹하기 위한 편리한 메서드를 제공합니다. 이런 헬퍼들은 복잡한 Mockery 메서드 호출을 직접 하지 않아도 되도록 Mockery 위에 편의성을 제공합니다.

<a name="mocking-objects"></a>
## 객체 모킹

Laravel의 [서비스 컨테이너](/docs/12.x/container)를 통해 애플리케이션 내에 주입할 객체를 모킹할 때는, 컨테이너에 모킹된 인스턴스를 `instance` 바인딩으로 등록해야 합니다. 이렇게 하면 컨테이너는 객체를 직접 생성하는 대신 모킹된 인스턴스를 사용하게 됩니다:

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

이 과정을 더욱 편리하게 하기 위해, Laravel의 기본 테스트 케이스 클래스는 `mock` 메서드를 제공합니다. 다음 예제는 위의 예제와 동일한 기능을 합니다:

```php
use App\Service;
use Mockery\MockInterface;

$mock = $this->mock(Service::class, function (MockInterface $mock) {
    $mock->expects('process');
});
```

객체의 일부 메서드만 모킹하고 싶을 때는 `partialMock` 메서드를 사용할 수 있습니다. 모킹하지 않은 메서드는 호출 시 정상적으로 실행됩니다:

```php
use App\Service;
use Mockery\MockInterface;

$mock = $this->partialMock(Service::class, function (MockInterface $mock) {
    $mock->expects('process');
});
```

또한 객체를 [스파이(spy)](http://docs.mockery.io/en/latest/reference/spies.html)하고 싶다면, Laravel의 기본 테스트 케이스 클래스는 `spy` 메서드를 제공하며 이는 `Mockery::spy` 메서드의 편리한 래퍼입니다. 스파이는 모킹과 비슷하지만, 스파이와 테스트 중인 코드 간의 상호작용을 기록하여 코드 실행 후에 검증할 수 있습니다:

```php
use App\Service;

$spy = $this->spy(Service::class);

// ...

$spy->shouldHaveReceived('process');
```

<a name="mocking-facades"></a>
## 파사드 모킹

전통적인 정적 메서드 호출과 달리, [파사드](/docs/12.x/facades) (여기에는 [실시간 파사드](/docs/12.x/facades#real-time-facades)도 포함) 역시 모킹할 수 있습니다. 이는 일반적인 정적 클래스보다 훨씬 뛰어난 테스트 가능성을 제공합니다. 테스트 중 컨트롤러 등에서 호출되는 Laravel 파사드를 모킹할 때가 많은데, 예를 들어 다음 컨트롤러 액션을 보십시오:

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

`Cache` 파사드의 `get` 메서드 호출을 모킹하려면 `expects` 메서드를 사용할 수 있으며, 이 메서드는 [Mockery](https://github.com/padraic/mockery) 모킹 인스턴스를 반환합니다. 파사드는 실제로 Laravel의 [서비스 컨테이너](/docs/12.x/container)에 의해 해석 및 관리되므로 일반적인 정적 클래스보다 더 뛰어난 테스트 가능성을 갖습니다. 다음은 `Cache::get` 호출 모킹 예제입니다:

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
> `Request` 파사드는 모킹하지 마십시오. 대신 테스트 시 `get`, `post`와 같은 [HTTP 테스트 메서드](/docs/12.x/http-tests)에 원하는 입력을 전달하세요. 마찬가지로 `Config` 파사드를 모킹하는 대신 테스트 내에서 `Config::set` 메서드를 호출하는 것이 좋습니다.

<a name="facade-spies"></a>
### 파사드 스파이

파사드를 [스파이](http://docs.mockery.io/en/latest/reference/spies.html)하고 싶을 때는 해당 파사드에서 `spy` 메서드를 호출하면 됩니다. 스파이는 모킹과 비슷하지만, 스파이와 테스트 중인 코드 간의 상호작용을 기록하여 코드 실행 후에 검증할 수 있습니다:

```php tab=Pest
<?php

use Illuminate\Support\Facades\Cache;

test('values are stored in cache', function () {
    Cache::spy();

    $response = $this->get('/');

    $response->assertStatus(200);

    Cache::shouldHaveReceived('put')->with('name', 'Taylor', 10);
});
```

```php tab=PHPUnit
use Illuminate\Support\Facades\Cache;

public function test_values_are_stored_in_cache(): void
{
    Cache::spy();

    $response = $this->get('/');

    $response->assertStatus(200);

    Cache::shouldHaveReceived('put')->with('name', 'Taylor', 10);
}
```

<a name="interacting-with-time"></a>
## 시간 다루기

테스트 시 `now` 헬퍼나 `Illuminate\Support\Carbon::now()` 같은 시간을 반환하는 메서드의 값을 변경해야 할 경우가 있습니다. 다행히도 Laravel의 기본 기능 테스트 클래스에는 현재 시간을 조작할 수 있는 헬퍼가 포함되어 있습니다:

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

각 시간 이동 메서드에 클로저를 전달할 수도 있습니다. 이 때 지정한 시점에서 시간이 멈추고 클로저가 실행된 뒤 시간이 정상적으로 다시 흐르도록 합니다:

```php
$this->travel(5)->days(function () {
    // 5일 후를 기준으로 어떤 테스트를 실행...
});

$this->travelTo(now()->subDays(10), function () {
    // 특정 시점에 대해 어떤 테스트를 실행...
});
```

`freezeTime` 메서드는 현재 시간을 멈출 때 사용합니다. 비슷하게, `freezeSecond` 메서드는 현재 초 단위 시작 시점에서 시간을 멈춥니다:

```php
use Illuminate\Support\Carbon;

// 시간이 멈춘 상태에서 클로저 실행 후 정상 흐름 복귀...
$this->freezeTime(function (Carbon $time) {
    // ...
});

// 현재 초 단위 시작 시점에서 시간이 멈춘 상태에서 클로저 실행 후 복귀...
$this->freezeSecond(function (Carbon $time) {
    // ...
});
```

이 메서드들은 시간 민감한 애플리케이션 동작을 테스트할 때 주로 유용합니다. 예를 들어 토론 포럼에서 한 주간 활동 없는 게시글이 잠기는 기능을 테스트하는 경우입니다:

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