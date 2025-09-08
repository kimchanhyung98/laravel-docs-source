# 헬퍼(Helpers)

- [소개](#introduction)
- [사용 가능한 메서드](#available-methods)
- [기타 유틸리티](#other-utilities)
    - [벤치마킹](#benchmarking)
    - [날짜](#dates)
    - [지연 함수](#deferred-functions)
    - [로터리](#lottery)
    - [파이프라인](#pipeline)
    - [Sleep](#sleep)
    - [Timebox](#timebox)
    - [URI](#uri)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 다양한 글로벌 "헬퍼" PHP 함수를 포함합니다. 이 함수들 중 많은 것들은 Laravel 프레임워크 자체에서 사용되지만, 여러분이 필요하다면 애플리케이션에서 자유롭게 사용할 수 있습니다.

<a name="available-methods"></a>
## 사용 가능한 메서드 (Available Methods)

<a name="arrays-and-objects-method-list"></a>
### 배열 & 객체

<div class="collection-method-list" markdown="1">

[Arr::accessible](#method-array-accessible)
[Arr::add](#method-array-add)
[Arr::array](#method-array-array)
[Arr::boolean](#method-array-boolean)
[Arr::collapse](#method-array-collapse)
[Arr::crossJoin](#method-array-crossjoin)
[Arr::divide](#method-array-divide)
[Arr::dot](#method-array-dot)
[Arr::every](#method-array-every)
[Arr::except](#method-array-except)
[Arr::exists](#method-array-exists)
[Arr::first](#method-array-first)
[Arr::flatten](#method-array-flatten)
[Arr::float](#method-array-float)
[Arr::forget](#method-array-forget)
[Arr::from](#method-array-from)
[Arr::get](#method-array-get)
[Arr::has](#method-array-has)
[Arr::hasAll](#method-array-hasall)
[Arr::hasAny](#method-array-hasany)
[Arr::integer](#method-array-integer)
[Arr::isAssoc](#method-array-isassoc)
[Arr::isList](#method-array-islist)
[Arr::join](#method-array-join)
[Arr::keyBy](#method-array-keyby)
[Arr::last](#method-array-last)
[Arr::map](#method-array-map)
[Arr::mapSpread](#method-array-map-spread)
[Arr::mapWithKeys](#method-array-map-with-keys)
[Arr::only](#method-array-only)
[Arr::partition](#method-array-partition)
[Arr::pluck](#method-array-pluck)
[Arr::prepend](#method-array-prepend)
[Arr::prependKeysWith](#method-array-prependkeyswith)
[Arr::pull](#method-array-pull)
[Arr::push](#method-array-push)
[Arr::query](#method-array-query)
[Arr::random](#method-array-random)
[Arr::reject](#method-array-reject)
[Arr::select](#method-array-select)
[Arr::set](#method-array-set)
[Arr::shuffle](#method-array-shuffle)
[Arr::sole](#method-array-sole)
[Arr::some](#method-array-some)
[Arr::sort](#method-array-sort)
[Arr::sortDesc](#method-array-sort-desc)
[Arr::sortRecursive](#method-array-sort-recursive)
[Arr::string](#method-array-string)
[Arr::take](#method-array-take)
[Arr::toCssClasses](#method-array-to-css-classes)
[Arr::toCssStyles](#method-array-to-css-styles)
[Arr::undot](#method-array-undot)
[Arr::where](#method-array-where)
[Arr::whereNotNull](#method-array-where-not-null)
[Arr::wrap](#method-array-wrap)
[data_fill](#method-data-fill)
[data_get](#method-data-get)
[data_set](#method-data-set)
[data_forget](#method-data-forget)
[head](#method-head)
[last](#method-last)
</div>

<a name="numbers-method-list"></a>
### 숫자

<div class="collection-method-list" markdown="1">

[Number::abbreviate](#method-number-abbreviate)
[Number::clamp](#method-number-clamp)
[Number::currency](#method-number-currency)
[Number::defaultCurrency](#method-default-currency)
[Number::defaultLocale](#method-default-locale)
[Number::fileSize](#method-number-file-size)
[Number::forHumans](#method-for-humans)
[Number::format](#method-number-format)
[Number::ordinal](#method-number-ordinal)
[Number::pairs](#method-number-pairs)
[Number::parseInt](#method-number-parse-int)
[Number::parseFloat](#method-number-parse-float)
[Number::percentage](#method-number-percentage)
[Number::spell](#method-number-spell)
[Number::spellOrdinal](#method-number-spell-ordinal)
[Number::trim](#method-number-trim)
[Number::useLocale](#method-number-use-locale)
[Number::withLocale](#method-number-with-locale)
[Number::useCurrency](#method-number-use-currency)
[Number::withCurrency](#method-number-with-currency)

</div>

<a name="paths-method-list"></a>
### 경로

<div class="collection-method-list" markdown="1">

[app_path](#method-app-path)
[base_path](#method-base-path)
[config_path](#method-config-path)
[database_path](#method-database-path)
[lang_path](#method-lang-path)
[public_path](#method-public-path)
[resource_path](#method-resource-path)
[storage_path](#method-storage-path)

</div>

<a name="urls-method-list"></a>
### URL

<div class="collection-method-list" markdown="1">

[action](#method-action)
[asset](#method-asset)
[route](#method-route)
[secure_asset](#method-secure-asset)
[secure_url](#method-secure-url)
[to_action](#method-to-action)
[to_route](#method-to-route)
[uri](#method-uri)
[url](#method-url)

</div>

<a name="miscellaneous-method-list"></a>
### 기타

<div class="collection-method-list" markdown="1">

[abort](#method-abort)
[abort_if](#method-abort-if)
[abort_unless](#method-abort-unless)
[app](#method-app)
[auth](#method-auth)
[back](#method-back)
[bcrypt](#method-bcrypt)
[blank](#method-blank)
[broadcast](#method-broadcast)
[broadcast_if](#method-broadcast-if)
[broadcast_unless](#method-broadcast-unless)
[cache](#method-cache)
[class_uses_recursive](#method-class-uses-recursive)
[collect](#method-collect)
[config](#method-config)
[context](#method-context)
[cookie](#method-cookie)
[csrf_field](#method-csrf-field)
[csrf_token](#method-csrf-token)
[decrypt](#method-decrypt)
[dd](#method-dd)
[dispatch](#method-dispatch)
[dispatch_sync](#method-dispatch-sync)
[dump](#method-dump)
[encrypt](#method-encrypt)
[env](#method-env)
[event](#method-event)
[fake](#method-fake)
[filled](#method-filled)
[info](#method-info)
[literal](#method-literal)
[logger](#method-logger)
[method_field](#method-method-field)
[now](#method-now)
[old](#method-old)
[once](#method-once)
[optional](#method-optional)
[policy](#method-policy)
[redirect](#method-redirect)
[report](#method-report)
[report_if](#method-report-if)
[report_unless](#method-report-unless)
[request](#method-request)
[rescue](#method-rescue)
[resolve](#method-resolve)
[response](#method-response)
[retry](#method-retry)
[session](#method-session)
[tap](#method-tap)
[throw_if](#method-throw-if)
[throw_unless](#method-throw-unless)
[today](#method-today)
[trait_uses_recursive](#method-trait-uses-recursive)
[transform](#method-transform)
[validator](#method-validator)
[value](#method-value)
[view](#method-view)
[with](#method-with)
[when](#method-when)

</div>

모든 개별 함수에 대한 설명은 본문에서 [배열 & 객체](#arrays)부터 순서대로 확인하세요.

<a name="other-utilities"></a>
## 기타 유틸리티 (Other Utilities)

<a name="benchmarking"></a>
### 벤치마킹 (Benchmarking)

애플리케이션의 특정 부분 성능을 빠르게 테스트하고 싶을 때, `Benchmark` 지원 클래스를 사용하여 주어진 콜백이 완료되는 데 걸린 밀리초(ms) 시간을 측정할 수 있습니다:

```php
<?php

use App\Models\User;
use Illuminate\Support\Benchmark;

Benchmark::dd(fn () => User::find(1)); // 0.1 ms

Benchmark::dd([
    '시나리오 1' => fn () => User::count(), // 0.5 ms
    '시나리오 2' => fn () => User::all()->count(), // 20.0 ms
]);
```

기본적으로 하나의 콜백만 1회 실행됩니다(1회 반복) 그리고 소요 시간이 브라우저 또는 콘솔에 표시됩니다.

콜백을 여러 번 실행하고 싶다면, 두 번째 인자로 반복 실행 횟수를 지정할 수 있습니다. 여러 번 실행할 경우, `Benchmark` 클래스는 모든 반복의 평균 실행 시간을 반환합니다:

```php
Benchmark::dd(fn () => User::count(), iterations: 10); // 0.5 ms
```

콜백의 값도 얻으면서 벤치마킹하고 싶다면, `value` 메서드를 사용하면 콜백의 반환값과 실행에 걸린 밀리초 수가 튜플 형태로 반환됩니다:

```php
[$count, $duration] = Benchmark::value(fn () => User::count());
```

<a name="dates"></a>
### 날짜 (Dates)

Laravel에는 [Carbon](https://carbon.nesbot.com/docs/)이라는 강력한 날짜/시간 처리 라이브러리가 내장되어 있습니다. 새로운 `Carbon` 인스턴스를 생성하려면 `now` 함수를 사용하세요. 이 함수는 Laravel 애플리케이션의 전역에서 사용할 수 있습니다:

```php
$now = now();
```

혹은, `Illuminate\Support\Carbon` 클래스를 직접 사용할 수도 있습니다:

```php
use Illuminate\Support\Carbon;

$now = Carbon::now();
```

Carbon과 그 기능에 대한 자세한 내용은 [공식 Carbon 문서](https://carbon.nesbot.com/docs/)를 참고하세요.

<a name="deferred-functions"></a>
### 지연 함수 (Deferred Functions)

Laravel의 [큐잉 작업(queued jobs)](/docs/12.x/queues)을 통해 백그라운드에서 작업을 처리할 수 있지만, 장기 실행 큐 워커를 구성하거나 유지 관리하지 않고 단순한 작업을 잠시 미루어 실행하고 싶을 수 있습니다.

지연 함수(deferred functions)는 클로저 실행을 HTTP 응답이 사용자에게 전송된 이후로 미뤄서, 애플리케이션을 빠르고 반응성 있게 만듭니다. 클로저 실행을 지연하려면 단순히 클로저를 `Illuminate\Support\defer` 함수에 전달하면 됩니다:

```php
use App\Services\Metrics;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use function Illuminate\Support\defer;

Route::post('/orders', function (Request $request) {
    // 주문 생성 ...

    defer(fn () => Metrics::reportOrder($order));

    return $order;
});
```

기본적으로, 지연 함수는 `Illuminate\Support\defer`가 호출된 HTTP 응답, Artisan 명령어, 큐된 작업이 성공적으로 완료된 경우에만 실행됩니다. 즉, 요청이 `4xx` 또는 `5xx` HTTP 응답을 내보내는 경우에는 실행되지 않습니다. 무조건 실행되기를 원한다면, `always` 메서드를 체이닝하면 됩니다:

```php
defer(fn () => Metrics::reportOrder($order))->always();
```

> [!WARNING]
> [Swoole PHP 확장](https://www.php.net/manual/en/book.swoole.php)을 설치한 경우, Laravel의 `defer` 함수는 Swoole의 글로벌 `defer` 함수와 충돌할 수 있어 웹서버 오류를 유발할 수 있습니다. 반드시 Laravel의 `defer` 헬퍼를 네임스페이스 포함(`use function Illuminate\Support\defer;`)으로 호출하세요.

<a name="cancelling-deferred-functions"></a>
#### 지연 함수 취소하기

지연 함수 실행 이전에 취소할 필요가 있으면, `forget` 메서드로 함수명을 이용해 취소할 수 있습니다. 지연 함수에 이름을 지정하려면 `Illuminate\Support\defer` 함수의 두 번째 인자로 전달하세요:

```php
defer(fn () => Metrics::report(), 'reportMetrics');

defer()->forget('reportMetrics');
```

<a name="disabling-deferred-functions-in-tests"></a>
#### 테스트 환경에서 지연 함수 비활성화

테스트를 할 때 지연 함수를 비활성화하는 것이 유용할 수 있습니다. 테스트 내에서 `withoutDefer`를 호출하면 모든 지연 함수가 즉시 실행됩니다:

```php tab=Pest
test('without defer', function () {
    $this->withoutDefer();

    // ...
});
```

```php tab=PHPUnit
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_without_defer(): void
    {
        $this->withoutDefer();

        // ...
    }
}
```

테스트 케이스 전체에서 지연 함수 비활성화를 적용하려면, 기본 `TestCase` 클래스의 `setUp` 메서드에서 `withoutDefer`를 호출하세요:

```php
<?php

namespace Tests;

use Illuminate\Foundation\Testing\TestCase as BaseTestCase;

abstract class TestCase extends BaseTestCase
{
    protected function setUp(): void// [tl! add:start]
    {
        parent::setUp();

        $this->withoutDefer();
    }// [tl! add:end]
}
```

<a name="lottery"></a>
### 로터리 (Lottery)

Laravel의 로터리(lottery) 클래스는 주어진 확률에 따라 콜백을 실행할 수 있도록 해줍니다. 예를 들어, 전체 요청 중 일부에만 코드를 실행하고 싶을 때 유용합니다:

```php
use Illuminate\Support\Lottery;

Lottery::odds(1, 20)
    ->winner(fn () => $user->won())
    ->loser(fn () => $user->lost())
    ->choose();
```

Laravel의 로터리 클래스를 다른 기능과 조합하는 것도 가능합니다. 예를 들어, 느린 쿼리를 예외 핸들러에 일부만 보고하고 싶을 때 다음처럼 사용할 수 있습니다. 로터리 클래스는 호출 가능(callable)하기 때문에, 콜러블 매개변수를 받는 모든 메서드에 전달할 수 있습니다:

```php
use Carbon\CarbonInterval;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Lottery;

DB::whenQueryingForLongerThan(
    CarbonInterval::seconds(2),
    Lottery::odds(1, 100)->winner(fn () => report('Querying > 2 seconds.')),
);
```

<a name="testing-lotteries"></a>
#### 로터리 테스트하기

Laravel은 로터리 호출을 테스트할 수 있도록 간단한 메서드들을 제공합니다:

```php
// 무조건 당첨...
Lottery::alwaysWin();

// 무조건 꽝...
Lottery::alwaysLose();

// 당첨, 꽝, 그 이후 원래 확률로 동작...
Lottery::fix([true, false]);

// 다시 원래 확률로 동작...
Lottery::determineResultsNormally();
```

<a name="pipeline"></a>
### 파이프라인 (Pipeline)

Laravel의 `Pipeline` 파사드는 입력값을 일련의 invokable 클래스, 클로저, 콜러블에 "파이프" 형식으로 전달할 수 있게 해 주며, 각 단계에서 입력값을 수정하거나 관찰 한 뒤 다음 단계로 진행할 수 있도록 해줍니다:

```php
use Closure;
use App\Models\User;
use Illuminate\Support\Facades\Pipeline;

$user = Pipeline::send($user)
    ->through([
        function (User $user, Closure $next) {
            // ...

            return $next($user);
        },
        function (User $user, Closure $next) {
            // ...

            return $next($user);
        },
    ])
    ->then(fn (User $user) => $user);
```

각 invokable 클래스 또는 클로저는 입력값과 `$next` 클로저를 전달받아 `$next`를 호출함으로써 다음 단계를 실행합니다. 이 방식은 [미들웨어](/docs/12.x/middleware)와 유사합니다.

파이프라인에서 마지막 콜러블이 `$next`를 호출하면, `then` 메서드에 전달한 콜러블이 실행됩니다. 보통은 단순히 처리된 입력값을 반환합니다. 그냥 입력값만 반환하고 싶으면 `thenReturn` 메서드를 사용할 수 있습니다.

클로저 뿐 아니라 invokable 클래스명도 전달할 수 있습니다. 클래스명을 넘기면 Laravel의 [서비스 컨테이너](/docs/12.x/container)를 통해 인스턴스화되어, 의존성 주입도 가능합니다:

```php
$user = Pipeline::send($user)
    ->through([
        GenerateProfilePhoto::class,
        ActivateSubscription::class,
        SendWelcomeEmail::class,
    ])
    ->thenReturn();
```

파이프라인의 모든 단계를 하나의 데이터베이스 트랜잭션에서 실행하고 싶다면 `withinTransaction` 메서드를 사용할 수 있습니다:

```php
$user = Pipeline::send($user)
    ->withinTransaction()
    ->through([
        ProcessOrder::class,
        TransferFunds::class,
        UpdateInventory::class,
    ])
    ->thenReturn();
```

<a name="sleep"></a>
### Sleep

Laravel의 `Sleep` 클래스는 PHP의 기본 `sleep`, `usleep` 함수를 감싼 가벼운 래퍼로, 테스트가 편리하고 여러 시간 단위를 다루기 쉬운 API를 제공합니다:

```php
use Illuminate\Support\Sleep;

$waiting = true;

while ($waiting) {
    Sleep::for(1)->second();

    $waiting = /* ... */;
}
```

`Sleep` 클래스는 다양한 시간 단위를 지원하는 여러 메서드를 제공합니다:

```php
// 일정 시간 후 값을 반환합니다...
$result = Sleep::for(1)->second()->then(fn () => 1 + 1);

// 주어진 값이 true일 때까지 대기합니다...
Sleep::for(1)->second()->while(fn () => shouldKeepSleeping());

// 90초 동안 대기...
Sleep::for(1.5)->minutes();

// 2초 대기...
Sleep::for(2)->seconds();

// 500 밀리초 대기...
Sleep::for(500)->milliseconds();

// 5,000 마이크로초 대기...
Sleep::for(5000)->microseconds();

// 특정 시각이 될 때까지 대기...
Sleep::until(now()->addMinute());

// PHP의 기본 "sleep" 함수 별칭...
Sleep::sleep(2);

// PHP의 기본 "usleep" 함수 별칭...
Sleep::usleep(5000);
```

다양한 시간 단위를 조합하려면 `and` 메서드를 사용할 수 있습니다:

```php
Sleep::for(1)->second()->and(10)->milliseconds();
```

<a name="testing-sleep"></a>
#### Sleep 테스트

`Sleep` 클래스나 PHP의 sleep 함수를 사용하는 코드를 테스트할 때 실제로 테스트가 지연되어 전체 테스트 속도가 느려질 수 있습니다. 예를 들어, 다음과 같은 코드를 테스트한다고 가정해보겠습니다:

```php
$waiting = /* ... */;

$seconds = 1;

while ($waiting) {
    Sleep::for($seconds++)->seconds();

    $waiting = /* ... */;
}
```

보통 이런 코드를 테스트하면 _최소_ 1초 이상 소요됩니다. 다행히도 `Sleep` 클래스의 파이크(faking) 기능을 사용하면 실제 대기를 건너뛰어 빠른 테스트가 가능합니다:

```php tab=Pest
it('waits until ready', function () {
    Sleep::fake();

    // ...
});
```

```php tab=PHPUnit
public function test_it_waits_until_ready()
{
    Sleep::fake();

    // ...
}
```

Sleep 클래스를 파이크하면 실제로는 대기가 발생하지 않아 테스트가 훨씬 빨라집니다.

Sleep 클래스를 파이크한 이후에는, 기대한 "sleep"이 제대로 수행됐는지 다양한 assertion 메서드를 사용할 수 있습니다. 예를 들어, 1초, 2초, 3초씩 3회 대기하는 코드를 테스트할 때는 다음과 같이 assert할 수 있습니다:

```php tab=Pest
it('checks if ready three times', function () {
    Sleep::fake();

    // ...

    Sleep::assertSequence([
        Sleep::for(1)->second(),
        Sleep::for(2)->seconds(),
        Sleep::for(3)->seconds(),
    ]);
}
```

```php tab=PHPUnit
public function test_it_checks_if_ready_three_times()
{
    Sleep::fake();

    // ...

    Sleep::assertSequence([
        Sleep::for(1)->second(),
        Sleep::for(2)->seconds(),
        Sleep::for(3)->seconds(),
    ]);
}
```

또 `Sleep` 클래스에는 더욱 다양한 assertion 메서드가 있습니다:

```php
use Carbon\CarbonInterval as Duration;
use Illuminate\Support\Sleep;

// 총 3회 sleep이 실행됐는지 확인...
Sleep::assertSleptTimes(3);

// sleep된 기간이 예상과 일치하는지 확인...
Sleep::assertSlept(function (Duration $duration): bool {
    return /* ... */;
}, times: 1);

// Sleep 클래스가 한 번도 호출되지 않았는지 확인...
Sleep::assertNeverSlept();

// Sleep이 호출돼도 실제로 대기가 없었는지 확인...
Sleep::assertInsomniac();
```

파이크된 sleep 호출시 특정 동작을 실행하고 싶을 땐, `whenFakingSleep` 메서드에 콜백을 넘기면 됩니다. 다음 예제에서는 Sleep 호출마다 Laravel의 [시간 헬퍼](/docs/12.x/mocking#interacting-with-time)를 이용해 즉시 시간을 진행시킵니다:

```php
use Carbon\CarbonInterval as Duration;

$this->freezeTime();

Sleep::fake();

Sleep::whenFakingSleep(function (Duration $duration) {
    // 대기 시간만큼 시간 진행...
    $this->travel($duration->totalMilliseconds)->milliseconds();
});
```

시간을 맞춰 진행하는 경우가 많으므로, `fake` 메서드에 `syncWithCarbon` 인자를 사용하면 테스트 내에서 Carbon 시간과 동기화됩니다:

```php
Sleep::fake(syncWithCarbon: true);

$start = now();

Sleep::for(1)->second();

$start->diffForHumans(); // 1초 전
```

Laravel 내에서는 대기 구현이 필요한 경우 내부적으로 항상 Sleep 클래스를 사용하므로, 예를 들면 [retry](#method-retry) 헬퍼 등에서도 보다 테스트가 쉬워집니다.

<a name="timebox"></a>
### Timebox

Laravel의 `Timebox` 클래스는 주어진 콜백 실행 시간이 항상 일정하게 유지되도록 보장합니다. 만약 실제 실행이 더 빨리 끝나도 지정한 시간만큼 대기 후 반환합니다. 이 기능은 주로 암호화 연산, 사용자 인증에서 공격자가 실행 시간 차이로 민감 정보를 유추하는 것을 방지하는 용도로 사용합니다.

반대로, 실제 실행 시간이 고정 시간보다 더 오래 걸리는 경우에는 Timebox가 관여하지 않습니다. 따라서 개발자가 충분히 넉넉한 시간을 지정해야 합니다.

`call` 메서드는 클로저와 마이크로초 단위 제한시간을 받아, 클로저 실행 및 종료까지 지연을 보장합니다:

```php
use Illuminate\Support\Timebox;

(new Timebox)->call(function ($timebox) {
    // ...
}, microseconds: 10000);
```

만약 클로저 내부에서 예외가 발생해도, 지정된 시간이 지난 후에 예외를 다시 throw합니다.

<a name="uri"></a>
### URI

Laravel의 `Uri` 클래스는 URI를 쉽고 유연하게 생성, 조작할 수 있도록 도와주는 플루언트 인터페이스를 제공합니다. 이 클래스는 League URI 패키지의 기능을 감싸며, Laravel의 라우팅 시스템과 자연스럽게 통합됩니다.

정적 메서드로 `Uri` 인스턴스를 쉽게 생성할 수 있습니다:

```php
use App\Http\Controllers\UserController;
use App\Http\Controllers\InvokableController;
use Illuminate\Support\Uri;

// 주어진 문자열에서 URI 인스턴스 생성...
$uri = Uri::of('https://example.com/path');

// 경로, 네임드 라우트, 컨트롤러 액션 등에서 URI 인스턴스 생성...
$uri = Uri::to('/dashboard');
$uri = Uri::route('users.show', ['user' => 1]);
$uri = Uri::signedRoute('users.show', ['user' => 1]);
$uri = Uri::temporarySignedRoute('user.index', now()->addMinutes(5));
$uri = Uri::action([UserController::class, 'index']);
$uri = Uri::action(InvokableController::class);

// 현재 요청 URL에서 URI 인스턴스 생성...
$uri = $request->uri();
```

URI 인스턴스를 얻었다면 다양한 방식으로 체이닝하여 조작할 수 있습니다:

```php
$uri = Uri::of('https://example.com')
    ->withScheme('http')
    ->withHost('test.com')
    ->withPort(8000)
    ->withPath('/users')
    ->withQuery(['page' => 2])
    ->withFragment('section-1');
```

<a name="inspecting-uris"></a>
#### URI 검사

`Uri` 클래스는 내부 URI의 다양한 요소를 쉽게 확인할 수 있도록 메서드를 제공합니다:

```php
$scheme = $uri->scheme();
$host = $uri->host();
$port = $uri->port();
$path = $uri->path();
$segments = $uri->pathSegments();
$query = $uri->query();
$fragment = $uri->fragment();
```

<a name="manipulating-query-strings"></a>
#### 쿼리 스트링 조작

`Uri` 클래스는 URI의 쿼리 스트링을 조작하는 다양한 메서드를 제공합니다. 예를 들어 `withQuery`는 쿼리 파라미터를 병합하고, 기존에 없는 경우만 병합하려면 `withQueryIfMissing`을, 쿼리 전체를 완전히 교체하려면 `replaceQuery`, 배열 형태 쿼리 파라미터에 값을 추가하려면 `pushOntoQuery`, 쿼리 파라미터 제거는 `withoutQuery`를 사용할 수 있습니다:

```php
$uri = $uri->withQuery(['sort' => 'name']);
$uri = $uri->withQueryIfMissing(['page' => 1]);
$uri = $uri->replaceQuery(['page' => 1]);
$uri = $uri->pushOntoQuery('filter', ['active', 'pending']);
$uri = $uri->withoutQuery(['page']);
```

<a name="generating-responses-from-uris"></a>
#### URI로부터 응답 생성

`redirect` 메서드를 사용하면 해당 URI로의 `RedirectResponse` 인스턴스를 생성할 수 있습니다:

```php
$uri = Uri::of('https://example.com');

return $uri->redirect();
```

또는, 라우트나 컨트롤러에서 직접 `Uri` 인스턴스를 반환하면 자동으로 해당 URI로 리다이렉트하는 응답이 생성됩니다:

```php
use Illuminate\Support\Facades\Route;
use Illuminate\Support\Uri;

Route::get('/redirect', function () {
    return Uri::to('/index')
        ->withQuery(['sort' => 'name']);
});
```
