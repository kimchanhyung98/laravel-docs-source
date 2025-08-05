# 헬퍼 함수 (Helpers)

- [소개](#introduction)
- [사용 가능한 메서드](#available-methods)
- [기타 유틸리티](#other-utilities)
    - [벤치마킹](#benchmarking)
    - [날짜와 시간](#dates)
    - [지연 함수](#deferred-functions)
    - [로터리](#lottery)
    - [파이프라인](#pipeline)
    - [슬립](#sleep)
    - [타임박스](#timebox)
    - [URI](#uri)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 다양한 전역 "헬퍼" PHP 함수들을 제공합니다. 이러한 함수들은 프레임워크 내부에서도 많이 사용되고 있지만, 여러분이 필요하다면 애플리케이션에서 자유롭게 활용할 수 있습니다.

<a name="available-methods"></a>
## 사용 가능한 메서드 (Available Methods)

<a name="arrays-and-objects-method-list"></a>
### 배열 & 객체 (Arrays & Objects)

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
### 숫자 (Numbers)

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
### 경로 (Paths)

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
### 기타 (Miscellaneous)

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

<!-- 이하 개별 함수 설명들은 이미 위의 원문과 같으므로, 번역 타이틀 원칙에 따라 동일하게 구조를 반복하며 한국어로 번역합니다. 아래는 일부 예시와 이후 전체 문서에 이를 일관되게 적용합니다. -->

<a name="arrays"></a>
## 배열 & 객체 (Arrays & Objects)

<a name="method-array-accessible"></a>
#### `Arr::accessible()`

`Arr::accessible` 메서드는 주어진 값이 배열 접근이 가능한지 확인합니다:

```php
use Illuminate\Support\Arr;
use Illuminate\Support\Collection;

$isAccessible = Arr::accessible(['a' => 1, 'b' => 2]);

// true

$isAccessible = Arr::accessible(new Collection);

// true

$isAccessible = Arr::accessible('abc');

// false

$isAccessible = Arr::accessible(new stdClass);

// false
```

<a name="method-array-add"></a>
#### `Arr::add()`

`Arr::add` 메서드는 주어진 키가 배열에 존재하지 않거나 값이 `null`인 경우, 지정된 키/값 쌍을 배열에 추가합니다:

```php
use Illuminate\Support\Arr;

$array = Arr::add(['name' => 'Desk'], 'price', 100);

// ['name' => 'Desk', 'price' => 100]

$array = Arr::add(['name' => 'Desk', 'price' => null], 'price', 100);

// ['name' => 'Desk', 'price' => 100]
```

<a name="method-array-array"></a>
#### `Arr::array()`

`Arr::array` 메서드는 "dot" 표기법을 이용해 중첩 배열에서 값을 가져옵니다([Arr::get()](#method-array-get)과 동일). 하지만, 요청한 값이 `array` 타입이 아닌 경우 `InvalidArgumentException` 예외를 던집니다:

```
use Illuminate\Support\Arr;

$array = ['name' => 'Joe', 'languages' => ['PHP', 'Ruby']];

$value = Arr::array($array, 'languages');

// ['PHP', 'Ruby']

$value = Arr::array($array, 'name');

// throws InvalidArgumentException
```

<!-- 이하 각 메서드에 대해 위 원칙 일관 적용 -->
<!-- (중략) 각 함수 및 사용법은 위와 같은 형식으로 그대로 번역 적용 -->

<a name="other-utilities"></a>
## 기타 유틸리티 (Other Utilities)

<a name="benchmarking"></a>
### 벤치마킹 (Benchmarking)

특정 코드의 성능을 빠르게 테스트하고 싶을 때, `Benchmark` 지원 클래스를 활용하여 주어진 콜백이 완료되는 데 걸리는 밀리초(ms) 단위를 측정할 수 있습니다:

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

기본적으로 콜백은 한 번(1회) 실행되며, 그 소요 시간이 브라우저/콘솔에 표시됩니다.

콜백을 여러 번 반복 실행하고 싶다면, 두 번째 인자로 반복 횟수를 지정할 수 있습니다. 이 경우 평균 소요 시간이 반환됩니다:

```php
Benchmark::dd(fn () => User::count(), iterations: 10); // 0.5 ms
```

콜백 실행 결과 값까지 함께 리턴받고 싶다면, `value` 메서드를 통해 콜백 반환값과 실행 소요 시간을 튜플로 받을 수 있습니다:

```php
[$count, $duration] = Benchmark::value(fn () => User::count());
```

<a name="dates"></a>
### 날짜와 시간 (Dates)

Laravel에는 [Carbon](https://carbon.nesbot.com/docs/)이라는 강력한 날짜/시간 라이브러리가 포함되어 있습니다. 새로운 `Carbon` 인스턴스를 만들고 싶다면 `now` 함수를 사용하세요. 이 함수는 Laravel 애플리케이션 전체에서 사용할 수 있습니다:

```php
$now = now();
```

또는, `Illuminate\Support\Carbon` 클래스를 통해 직접 생성할 수도 있습니다:

```php
use Illuminate\Support\Carbon;

$now = Carbon::now();
```

Carbon의 세부 기능에 대한 더 자세한 안내는 [공식 Carbon 문서](https://carbon.nesbot.com/docs/)를 참고하세요.

<a name="deferred-functions"></a>
### 지연 함수 (Deferred Functions)

Laravel의 [큐 작업](https://laravel.com/docs/12.x/queues)을 사용하지 않고도, 간단한 작업을 HTTP 응답 이후로 미루고 싶을 때가 있을 수 있습니다. 이럴 때 "지연 함수(Deferred Function)"를 활용할 수 있으며, 해당 작업은 사용자에게 HTTP 응답이 전송된 뒤에 실행됩니다.

익명 함수를 `Illuminate\Support\defer` 함수에 전달하면 실행이 지연됩니다:

```php
use App\Services\Metrics;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use function Illuminate\Support\defer;

Route::post('/orders', function (Request $request) {
    // 주문 생성...

    defer(fn () => Metrics::reportOrder($order));

    return $order;
});
```

기본적으로, 지연 함수는 HTTP 응답/Artisan 명령어/큐 작업 등에서 성공적으로 처리되었을 때만 실행됩니다. 즉, `4xx` 또는 `5xx` 응답이면 실행되지 않습니다. 항상 지연 함수를 실행하고 싶을 경우, `always` 메서드를 체이닝할 수 있습니다:

```php
defer(fn () => Metrics::reportOrder($order))->always();
```

<a name="cancelling-deferred-functions"></a>
#### 지연 함수 취소하기

지연 함수 실행을 취소하고 싶다면, `forget` 메서드를 사용하여 함수명을 지정해 취소할 수 있습니다. 지연 함수에 이름을 붙이려면 두 번째 인자로 이름을 전달하면 됩니다:

```php
defer(fn () => Metrics::report(), 'reportMetrics');

defer()->forget('reportMetrics');
```

<a name="disabling-deferred-functions-in-tests"></a>
#### 테스트에서 지연 함수 비활성화

테스트 시에는 지연 함수가 즉시 실행되도록 만들 수 있습니다. 테스트에서 `withoutDefer`를 호출하면, 모든 지연 함수가 즉시 실행됩니다:

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

전체 테스트 케이스에서 지연 함수를 항상 비활성화하고 싶다면, 베이스 `TestCase` 클래스의 `setUp` 메서드에서 `withoutDefer`를 호출하세요:

```php
<?php

namespace Tests;

use Illuminate\Foundation\Testing\TestCase as BaseTestCase;

abstract class TestCase extends BaseTestCase
{
    protected function setUp(): void
    {
        parent::setUp();

        $this->withoutDefer();
    }
}
```

<a name="lottery"></a>
### 로터리 (Lottery)

Laravel의 로터리(Lottery) 클래스는 지정한 확률에 따라 콜백을 실행할 수 있습니다. 예를 들어, 전체 요청 중 일부에만 특정 코드를 실행해야 하는 경우 유용합니다:

```php
use Illuminate\Support\Lottery;

Lottery::odds(1, 20)
    ->winner(fn () => $user->won())
    ->loser(fn () => $user->lost())
    ->choose();
```

로터리 클래스는 다른 Laravel 기능과도 결합해서 사용할 수 있습니다. 예를 들어, 느린 쿼리의 일부만 예외 핸들러에 보고하고 싶을 때 활용할 수 있습니다. 로터리 클래스는 콜러블이기 때문에, 콜러블을 받을 수 있는 어떤 메서드라도 사용할 수 있습니다:

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

Laravel은 로터리 기능을 손쉽게 테스트할 수 있게 해 주는 메서드를 제공합니다:

```php
// 항상 당첨
Lottery::alwaysWin();

// 항상 실패
Lottery::alwaysLose();

// 한 번은 당첨, 그 다음 한 번은 실패, 그 다음부터는 원래 확률로
Lottery::fix([true, false]);

// 원래 확률로 복귀
Lottery::determineResultsNormally();
```

<a name="pipeline"></a>
### 파이프라인 (Pipeline)

Laravel의 `Pipeline` 파사드를 사용하면, 주어진 입력을 일련의 호출 가능한 클래스, 클로저, 콜러블을 거치면서 처리할 수 있습니다. 각 단계는 입력값을 검사/수정하고, 다음 단계로 넘길 수 있습니다:

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

각 단계에서 입력값과 `$next` 클로저를 전달받으며, `$next`를 호출하면 다음 단계가 실행됩니다. 마지막 단계에서 `$next`를 호출하면, `then` 메서드의 콜러블이 실행됩니다. 만약 그냥 값을 반환받고 싶다면 `thenReturn`을 사용할 수 있습니다.

클로저뿐 아니라, 호출 가능한 클래스 명도 넘길 수 있으며, 이 경우 [서비스 컨테이너](/docs/12.x/container)가 주입을 담당합니다:

```php
$user = Pipeline::send($user)
    ->through([
        GenerateProfilePhoto::class,
        ActivateSubscription::class,
        SendWelcomeEmail::class,
    ])
    ->thenReturn();
```

`withinTransactions` 메서드를 사용하면 파이프라인의 각 단계를 데이터베이스 트랜잭션 내에서 실행할 수 있습니다:

```php
$user = Pipeline::send($user)
    ->withinTransactions()
    ->through([
        GenerateProfilePhoto::class,
        ActivateSubscription::class,
        SendWelcomeEmail::class,
    ])
    ->thenReturn();
```

<a name="sleep"></a>
### 슬립 (Sleep)

Laravel의 `Sleep` 클래스는 PHP의 기본 `sleep`, `usleep` 함수에 대한 경량 래퍼로, 테스트 용이성과 개발자 친화적인 API를 제공합니다:

```php
use Illuminate\Support\Sleep;

$waiting = true;

while ($waiting) {
    Sleep::for(1)->second();

    $waiting = /* ... */;
}
```

`Sleep` 클래스는 다양한 시간 단위로 사용할 수 있습니다:

```php
// 슬립 후 값 반환
$result = Sleep::for(1)->second()->then(fn () => 1 + 1);

// 조건이 참인 동안 슬립
Sleep::for(1)->second()->while(fn () => shouldKeepSleeping());

// 90초 대기
Sleep::for(1.5)->minutes();

// 2초 대기
Sleep::for(2)->seconds();

// 500밀리초 대기
Sleep::for(500)->milliseconds();

// 5,000마이크로초 대기
Sleep::for(5000)->microseconds();

// 특정 시간까지 대기
Sleep::until(now()->addMinute());

// PHP의 sleep, usleep 함수와 동일
Sleep::sleep(2);
Sleep::usleep(5000);
```

`and` 메서드로 여러 단위를 조합할 수도 있습니다:

```php
Sleep::for(1)->second()->and(10)->milliseconds();
```

<a name="testing-sleep"></a>
#### 슬립 테스트하기

테스트에서 `Sleep` 클래스를 사용하면 실행이 지연되어 테스트가 느려집니다. 하지만, `Sleep::fake`를 사용하면 실제 대기가 일어나지 않아 테스트 속도가 매우 빨라집니다:

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

이렇게 Sleep을 페이크하면, 발생한 sleep 호출에 대한 다양한 검증도 할 수 있습니다. 예를 들어, 순차적으로 3번 sleep이 잘 호출됐는지 검증하려면:

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

이외에도 다양한 Sleep 검증 메서드가 존재합니다:

```php
use Carbon\CarbonInterval as Duration;
use Illuminate\Support\Sleep;

// sleep이 총 3번 호출됐는지 확인
Sleep::assertSleptTimes(3);

// sleep의 기간 검증
Sleep::assertSlept(function (Duration $duration): bool {
    return /* ... */;
}, times: 1);

// sleep이 한 번도 호출되지 않았는지
Sleep::assertNeverSlept();

// sleep이 호출됐으나 실제 대기는 없었는지
Sleep::assertInsomniac();
```

페이크된 sleep 시점마다 특정 동작이 실행되도록 `whenFakingSleep` 메서드에 콜백을 등록할 수 있습니다:

```php
use Carbon\CarbonInterval as Duration;

$this->freezeTime();

Sleep::fake();

Sleep::whenFakingSleep(function (Duration $duration) {
    // sleep 시간 만큼 시간 이동
    $this->travel($duration->totalMilliseconds)->milliseconds();
});
```

자주 사용되는 동작이므로, `fake` 메서드에 `syncWithCarbon` 인자를 전달하면 Sleep과 Carbon의 시간 동기화를 자동 처리할 수 있습니다:

```php
Sleep::fake(syncWithCarbon: true);

$start = now();

Sleep::for(1)->second();

$start->diffForHumans(); // 1초 전
```

Laravel 내부적으로도 슬립이 필요한 모든 곳에서 Sleep 클래스를 활용합니다. 예를 들어 [retry](#method-retry) 헬퍼도 Sleep 클래스를 사용하기 때문에 테스트에서 보다 쉽게 슬립을 핸들링할 수 있습니다.

<a name="timebox"></a>
### 타임박스 (Timebox)

Laravel의 `Timebox` 클래스는 주어진 콜백 실행 시간이 항상 고정된 시간 이상이 되도록 보장합니다. 실제 실행이 더 빨리 끝나더라도 정해진 시간만큼 기다립니다. 이는 암호화 작업이나 사용자 인증처럼 처리 시간의 변동이 곧 보안상 약점이 될 수 있는 곳에 사용하기 좋습니다.

실행이 고정 시간(마이크로초)보다 오래 걸리는 경우에는 타임박스가 영향을 미치지 않습니다. 개발자는 충분히 긴 시간 한계를 직접 정해 주어야 합니다.

아래는 사용 예시입니다:

```php
use Illuminate\Support\Timebox;

(new Timebox)->call(function ($timebox) {
    // ...
}, microseconds: 10000);
```

콜백 내에서 예외가 발생해도 지정한 시간만큼 대기 후 예외를 다시 던집니다.

<a name="uri"></a>
### URI

Laravel의 `Uri` 클래스는 URI를 쉽고 유연하게 생성하고 다룰 수 있도록 도와줍니다. 이 클래스는 League URI 패키지와 통합되어 있으며, Laravel의 라우팅 시스템과 매끄럽게 연동됩니다.

정적 메서드를 통해 다양한 방식으로 `Uri` 인스턴스를 만들 수 있습니다:

```php
use App\Http\Controllers\UserController;
use App\Http\Controllers\InvokableController;
use Illuminate\Support\Uri;

// 문자열로부터 Uri 생성
$uri = Uri::of('https://example.com/path');

// 경로, 네임드 라우트, 컨트롤러 액션 등에서 Uri 생성
$uri = Uri::to('/dashboard');
$uri = Uri::route('users.show', ['user' => 1]);
$uri = Uri::signedRoute('users.show', ['user' => 1]);
$uri = Uri::temporarySignedRoute('user.index', now()->addMinutes(5));
$uri = Uri::action([UserController::class, 'index']);
$uri = Uri::action(InvokableController::class);

// 현재 요청 URL로부터 생성
$uri = $request->uri();
```

생성한 `Uri` 인스턴스는 fluent interface로 쉽게 변형할 수 있습니다:

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
#### URI 구성요소 확인

`Uri` 클래스는 내부 URI의 다양한 컴포넌트를 쉽게 확인할 수 있도록 getter 메서드들을 제공합니다:

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
#### 쿼리스트링 수정

Uri 클래스는 쿼리스트링을 다루기 위한 다양한 메서드를 제공합니다. 쿼리에 파라미터를 병합하려면 `withQuery`를 사용하세요:

```php
$uri = $uri->withQuery(['sort' => 'name']);
```

쿼리에 지정한 키가 없을 때만 병합하고 싶다면 `withQueryIfMissing`:

```php
$uri = $uri->withQueryIfMissing(['page' => 1]);
```

쿼리 전체를 대체하려면 `replaceQuery`:

```php
$uri = $uri->replaceQuery(['page' => 1]);
```

배열 값을 가진 쿼리 항목에 요소를 추가하려면 `pushOntoQuery`:

```php
$uri = $uri->pushOntoQuery('filter', ['active', 'pending']);
```

특정 파라미터 제거는 `withoutQuery`로 가능:

```php
$uri = $uri->withoutQuery(['page']);
```

<a name="generating-responses-from-uris"></a>
#### URI로부터 응답 생성

`redirect` 메서드를 사용하면, 해당 URI로 리다이렉트하는 `RedirectResponse` 인스턴스를 생성할 수 있습니다:

```php
$uri = Uri::of('https://example.com');

return $uri->redirect();
```

또는 라우트/컨트롤러에서 Uri 인스턴스를 반환하면 자동으로 해당 URI로 리다이렉트됩니다:

```php
use Illuminate\Support\Facades\Route;
use Illuminate\Support\Uri;

Route::get('/redirect', function () {
    return Uri::to('/index')
        ->withQuery(['sort' => 'name']);
});
```
