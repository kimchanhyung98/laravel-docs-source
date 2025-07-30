# 모킹 (Mocking)

- [소개](#introduction)
- [객체 모킹](#mocking-objects)
- [파사드 모킹](#mocking-facades)
    - [파사드 스파이](#facade-spies)
- [시간 다루기](#interacting-with-time)

<a name="introduction"></a>
## 소개

Laravel 애플리케이션을 테스트할 때, 특정 기능이 실제로 실행되지 않도록 "모킹"하고 싶을 수 있습니다. 예를 들어, 컨트롤러가 이벤트를 발송할 때, 이벤트 리스너가 실제 실행되지 않도록 모킹하여 테스트할 수 있습니다. 이렇게 하면 이벤트 리스너는 별도의 테스트 케이스로 시험할 수 있으므로, 컨트롤러의 HTTP 응답만 집중해서 테스트할 수 있습니다.

Laravel은 이벤트, 작업(job), 기타 파사드(facade)를 모킹할 수 있도록 기본적으로 유용한 메서드를 제공합니다. 이 헬퍼들은 복잡한 Mockery 메서드 호출을 직접 하지 않아도 되도록 편리한 추상화 계층을 제공합니다.

<a name="mocking-objects"></a>
## 객체 모킹

Laravel의 [서비스 컨테이너](/docs/11.x/container)를 통해 애플리케이션에 주입할 객체를 모킹하려면, 모킹한 인스턴스를 `instance` 바인딩으로 컨테이너에 등록해야 합니다. 그러면 컨테이너가 객체를 직접 생성하는 대신 당신이 등록한 모킹한 인스턴스를 사용합니다:

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

좀 더 편리하게 하려면, Laravel 기본 테스트 클래스에서 제공하는 `mock` 메서드를 사용할 수 있습니다. 다음 예제가 위 예제와 동일합니다:

```
use App\Service;
use Mockery\MockInterface;

$mock = $this->mock(Service::class, function (MockInterface $mock) {
    $mock->shouldReceive('process')->once();
});
```

객체의 일부 메서드만 모킹하려면, 모킹하지 않은 메서드는 그대로 실행되도록 하는 `partialMock` 메서드를 사용할 수 있습니다:

```
use App\Service;
use Mockery\MockInterface;

$mock = $this->partialMock(Service::class, function (MockInterface $mock) {
    $mock->shouldReceive('process')->once();
});
```

비슷하게, 객체를 [스파이(spy)](http://docs.mockery.io/en/latest/reference/spies.html)하고자 한다면, Laravel 기본 테스트 클래스의 `spy` 메서드를 이용할 수 있습니다. 스파이는 모킹과 유사하지만, 모킹 대상과 코드 간의 모든 상호작용을 기록하여 코드 실행 후에 검증할 수 있습니다:

```
use App\Service;

$spy = $this->spy(Service::class);

// ...

$spy->shouldHaveReceived('process');
```

<a name="mocking-facades"></a>
## 파사드 모킹

기존의 정적 메서드 호출과 달리, [파사드](/docs/11.x/facades) (실시간 파사드([real-time facades](/docs/11.x/facades#real-time-facades)) 포함)은 모킹할 수 있습니다. 이는 기존 정적 메서드에 비해 큰 장점이며, 의존성 주입을 사용할 때와 같은 테스트 가능성을 제공합니다. 테스트 시 컨트롤러 안에서 호출되는 Laravel 파사드 메서드를 모킹하고 싶을 때가 많습니다. 예를 들어, 다음 컨트롤러 액션을 살펴보십시오:

```
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Cache;

class UserController extends Controller
{
    /**
     * 애플리케이션의 모든 사용자 목록을 반환합니다.
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

`Cache` 파사드의 호출을 `shouldReceive` 메서드로 모킹할 수 있는데, 이 메서드는 [Mockery](https://github.com/padraic/mockery) 모킹 인스턴스를 반환합니다. 파사드는 실제로 Laravel [서비스 컨테이너](/docs/11.x/container)를 통해 해결되고 관리되므로 일반적인 정적 클래스보다 훨씬 테스트하기 쉽습니다. 예를 들어, `Cache` 파사드의 `get` 메서드를 모킹하는 코드입니다:

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
> `Request` 파사드는 모킹하지 마십시오. 대신 테스트 실행 시 `get`, `post` 같은 [HTTP 테스트 메서드](/docs/11.x/http-tests)에 원하는 입력을 전달하세요. 마찬가지로 `Config` 파사드 대신 테스트 내에서 `Config::set` 메서드를 호출하여 설정을 변경해야 합니다.

<a name="facade-spies"></a>
### 파사드 스파이

파사드를 [스파이](http://docs.mockery.io/en/latest/reference/spies.html)하고 싶다면, 해당 파사드의 `spy` 메서드를 호출할 수 있습니다. 스파이는 모킹과 유사하나, 코드 실행 후 상호작용을 기록하여 검증할 수 있습니다:

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
## 시간 다루기

테스트 중에 `now` 또는 `Illuminate\Support\Carbon::now()` 같은 헬퍼가 반환하는 시간을 수정해야 할 때가 있습니다. 다행히, Laravel 기본 기능 테스트 클래스에 현재 시간을 조작할 수 있는 헬퍼가 포함되어 있습니다:

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

    // 특정 시간으로 이동...
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

    // 특정 시간으로 이동...
    $this->travelTo(now()->subHours(6));

    // 현재 시간으로 복귀...
    $this->travelBack();
}
```

다양한 시간 이동 메서드들에 클로저를 전달할 수도 있습니다. 이렇게 하면 클로저 내에서 시간이 지정한 시점으로 고정(freeze)되어 실행되고, 클로저 실행 후에는 시간이 정상적으로 흐릅니다:

```
$this->travel(5)->days(function () {
    // 5일 후 시점에서 무언가를 테스트...
});

$this->travelTo(now()->subDays(10), function () {
    // 특정 순간의 시간을 기준으로 테스트...
});
```

현재 시간을 고정하려면 `freezeTime` 메서드를 사용할 수 있습니다. 마찬가지로 `freezeSecond` 메서드는 현재 초의 시작 시점으로 시간을 고정합니다:

```
use Illuminate\Support\Carbon;

// 클로저 실행 중 시간을 고정하고, 끝나면 정상 흐름 복원...
$this->freezeTime(function (Carbon $time) {
    // ...
});

// 현재 초의 시작 시점으로 고정하고, 종료 후 정상 시간 흐름 복원...
$this->freezeSecond(function (Carbon $time) {
    // ...
});
```

위 메서드들은 주로, 예를 들어 토론 포럼에서 일정 기간 활동 없는 게시물을 잠그는 등 시간에 민감한 애플리케이션 동작을 테스트할 때 유용합니다:

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