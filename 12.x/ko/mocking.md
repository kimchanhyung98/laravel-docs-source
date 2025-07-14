# 목(mock) 객체 활용 (Mocking)

- [소개](#introduction)
- [오브젝트 목(mock) 만들기](#mocking-objects)
- [파사드 목(mock) 만들기](#mocking-facades)
    - [파사드 스파이](#facade-spies)
- [시간 다루기](#interacting-with-time)

<a name="introduction"></a>
## 소개

라라벨 애플리케이션을 테스트할 때 실제로 실행되지 않았으면 하는 애플리케이션의 특정 부분을 "목(mock)" 처리하고 싶을 때가 있습니다. 예를 들어, 이벤트를 디스패치하는 컨트롤러를 테스트할 때는 이벤트 리스너가 테스트 중에 실제로 실행되지 않도록 목(mock) 처리하고 싶을 수 있습니다. 이렇게 하면 이벤트 리스너의 동작은 별도의 테스트 케이스에서 검증할 수 있으니, 컨트롤러의 HTTP 응답만 집중해서 테스트할 수 있습니다.

라라벨은 이벤트, 잡(job), 기타 다양한 파사드(facade)를 위한 목(mock) 메서드를 기본적으로 제공합니다. 이 메서드들은 Mockery를 직접 복잡하게 호출하지 않아도 되도록 편리한 래퍼 역할을 하는 것이 특징입니다.

<a name="mocking-objects"></a>
## 오브젝트 목(mock) 만들기

라라벨의 [서비스 컨테이너](/docs/12.x/container)를 통해 애플리케이션에 주입되는 객체를 목(mock) 처리하고 싶다면, 해당 객체의 목(mock) 인스턴스를 `instance` 바인딩으로 컨테이너에 등록해야 합니다. 이렇게 하면 컨테이너가 직접 객체를 만들어내는 대신, 여러분이 만든 목(mock) 인스턴스를 사용하게 됩니다:

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

이를 좀 더 편리하게 사용하려면, 라라벨의 기본 테스트 케이스 클래스에서 제공하는 `mock` 메서드를 사용할 수 있습니다. 아래 예제는 위와 동일한 동작을 합니다:

```php
use App\Service;
use Mockery\MockInterface;

$mock = $this->mock(Service::class, function (MockInterface $mock) {
    $mock->expects('process');
});
```

특정 메서드만 목(mock) 처리하고 나머지 메서드는 실제로 동작하게 하고 싶다면 `partialMock` 메서드를 사용할 수 있습니다. 이렇게 하면 목(mock) 처리하지 않은 메서드는 평소처럼 실행됩니다:

```php
use App\Service;
use Mockery\MockInterface;

$mock = $this->partialMock(Service::class, function (MockInterface $mock) {
    $mock->expects('process');
});
```

비슷하게, [spy](http://docs.mockery.io/en/latest/reference/spies.html)를 사용해 객체가 어떤 방식으로 호출되는지 확인하고 싶다면, 라라벨의 기본 테스트 케이스 클래스에서 `spy` 메서드를 쓸 수 있습니다. 스파이는 목(mock)과 유사하지만, 코드 실행 후 스파이 객체와의 상호작용 내역을 기록해두기 때문에 실행 뒤에 검증(어설션)을 할 수 있게 도와줍니다:

```php
use App\Service;

$spy = $this->spy(Service::class);

// ...

$spy->shouldHaveReceived('process');
```

<a name="mocking-facades"></a>
## 파사드 목(mock) 만들기

전통적인 정적(static) 메서드와 달리, [파사드](/docs/12.x/facades)([실시간 파사드](/docs/12.x/facades#real-time-facades) 포함)는 목(mock) 처리할 수 있습니다. 이 점은 정적 메서드보다 훨씬 테스트하기 쉽다는 큰 장점이 있습니다. 즉, 의존성 주입 방식과 같은 수준의 테스트 유연성을 누릴 수 있습니다. 컨트롤러 내에서 발생하는 라라벨 파사드의 호출을 테스트할 때, 파사드의 메서드를 목(mock) 처리하는 경우가 많습니다. 예를 들어, 다음과 같은 컨트롤러 액션을 살펴보겠습니다:

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

`Cache` 파사드의 호출을 목(mock) 처리하려면, `expects` 메서드를 사용하면 됩니다. 이 메서드는 [Mockery](https://github.com/padraic/mockery) 목(mock)의 인스턴스를 반환합니다. 파사드는 라라벨 [서비스 컨테이너](/docs/12.x/container)를 통해 해결(resolved)되고 관리되기 때문에, 일반적인 정적 클래스보다 테스트하기가 훨씬 쉽습니다. 예를 들어, 아래처럼 `Cache` 파사드의 `get` 메서드 호출을 목(mock) 처리할 수 있습니다:

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
> `Request` 파사드는 목(mock) 처리해서는 안 됩니다. 원하는 입력값이 있다면, 테스트 시 [HTTP 테스트 메서드](/docs/12.x/http-tests)에서 `get`, `post`와 같은 메서드에 값을 전달해야 합니다. 마찬가지로, `Config` 파사드를 목(mock) 처리하기보다는, 테스트 내에서 `Config::set` 메서드를 직접 호출하는 방식이 권장됩니다.

<a name="facade-spies"></a>
### 파사드 스파이

파사드에 [spy](http://docs.mockery.io/en/latest/reference/spies.html)를 적용하려면, 해당 파사드에서 `spy` 메서드를 호출하면 됩니다. 스파이는 목(mock)과 거의 같지만, 호출 내역을 기록해 두었다가 코드 수행 이후에 어설션을 할 수 있다는 점이 특징입니다:

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

테스트를 할 때, `now` 헬퍼나 `Illuminate\Support\Carbon::now()` 등에서 반환되는 시간을 임의로 변경해야 할 때가 있습니다. 다행히도, 라라벨의 기본 기능 테스트 클래스에는 현재 시간을 쉽게 조작할 수 있는 헬퍼 메서드들이 포함되어 있습니다:

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

각종 시간 이동 메서드에는 클로저(익명 함수)를 전달할 수도 있습니다. 이 경우, 지정된 시간으로 고정된 채 클로저가 실행되고, 클로저 실행이 끝난 뒤 시간은 원래대로 돌아옵니다:

```php
$this->travel(5)->days(function () {
    // 5일 후의 시점을 기준으로 테스트...
});

$this->travelTo(now()->subDays(10), function () {
    // 특정 시점에서 테스트 수행...
});
```

`freezeTime` 메서드를 사용하면 현재 시각을 그대로 멈출 수 있습니다. 이와 비슷하게, `freezeSecond` 메서드는 현재 초의 첫 시점으로 시간을 고정합니다:

```php
use Illuminate\Support\Carbon;

// 현재 시각을 멈췄다가, 클로저 실행 후 다시 원래처럼 시간 흐름을 복원...
$this->freezeTime(function (Carbon $time) {
    // ...
});

// 현재 초의 시작 시점으로 시간을 멈췄다가, 클로저 실행 후 복구...
$this->freezeSecond(function (Carbon $time) {
    // ...
})
```

앞서 살펴본 메서드들은 모두 시간에 민감한 애플리케이션 동작, 예를 들어 토론 게시판의 비활성 글을 일정 시간이 지난 뒤 잠그는 기능을 테스트할 때 유용하게 사용할 수 있습니다:

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