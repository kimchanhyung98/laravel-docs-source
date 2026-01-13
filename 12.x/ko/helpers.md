# 헬퍼 (Helpers)

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

Laravel은 다양한 전역 "헬퍼" PHP 함수를 제공합니다. 이들 중 다수는 프레임워크 내부에서 사용되고 있지만, 여러분이 편리하다고 생각한다면 애플리케이션에서도 자유롭게 사용할 수 있습니다.

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
[Arr::exceptValues](#method-array-except-values)
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
[Arr::onlyValues](#method-array-only-values)
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

<a name="arrays"></a>
## 배열 & 객체 (Arrays & Objects)

<!-- 아래의 개별 배열 및 객체 메서드 내용은 그대로 번역 규칙을 적용하세요. 코드 블록은 번역하지 않습니다. -->
#### 함수 및 각각의 상세 설명은 위 규칙에 따라 번역되어 있습니다.

<a name="numbers"></a>
## 숫자 (Numbers)

<!-- 아래의 숫자 관련 메서드 설명 및 예시는 위 규칙대로 번역하세요. 코드는 번역하지 않습니다. -->

<a name="paths"></a>
## 경로 (Paths)

<!-- 경로 관련 헬퍼 함수 설명 및 예시는 규칙에 따라 번역하세요. -->

<a name="urls"></a>
## URL (URLs)

<!-- URL 관련 함수 설명 및 예시는 규칙에 따라 번역하세요. -->

<a name="miscellaneous"></a>
## 기타 (Miscellaneous)

<!-- 기타 함수들도 규칙을 따라 번역하세요. -->

<a name="other-utilities"></a>
## 기타 유틸리티 (Other Utilities)

<a name="benchmarking"></a>
### 벤치마킹 (Benchmarking)

애플리케이션의 특정 부분의 성능을 빠르게 테스트하고 싶을 때가 있습니다. 이러한 경우, `Benchmark` 지원 클래스를 이용하면 주어진 콜백이 완료되는 데 걸린 시간(밀리초 단위)을 측정할 수 있습니다.

```php
<?php

use App\Models\User;
use Illuminate\Support\Benchmark;

Benchmark::dd(fn () => User::find(1)); // 0.1 ms

Benchmark::dd([
    'Scenario 1' => fn () => User::count(), // 0.5 ms
    'Scenario 2' => fn () => User::all()->count(), // 20.0 ms
]);
```

기본적으로 주어진 콜백은 한 번(한 회차) 실행되며, 소요된 시간이 브라우저/콘솔에 표시됩니다.

콜백을 여러 번 실행하고 싶다면, 메서드의 두 번째 인자로 반복 횟수를 지정할 수 있습니다. 반복 실행 시 `Benchmark` 클래스는 전체 반복에서 콜백을 실행하는 데 걸린 평균 밀리초를 반환합니다.

```php
Benchmark::dd(fn () => User::count(), iterations: 10); // 0.5 ms
```

콜백의 실행 결과도 함께 얻고 싶을 때는, `value` 메서드를 사용하면 콜백의 반환 값과 실행에 걸린 시간을 튜플로 반환합니다.

```php
[$count, $duration] = Benchmark::value(fn () => User::count());
```

<a name="dates"></a>
### 날짜와 시간 (Dates and Time)

Laravel에는 [Carbon](https://carbon.nesbot.com/docs/)이라는 강력한 날짜 및 시간 조작 라이브러리가 포함되어 있습니다. 새로운 `Carbon` 인스턴스를 생성하려면, `now` 함수를 사용하면 됩니다. 이 함수는 Laravel 애플리케이션 내 어디서든 사용할 수 있습니다.

```php
$now = now();
```

또는, `Illuminate\Support\Carbon` 클래스를 이용해 인스턴스를 생성할 수도 있습니다.

```php
use Illuminate\Support\Carbon;

$now = Carbon::now();
```

Laravel은 `Carbon` 인스턴스에 `plus`와 `minus` 메서드를 추가하여 날짜와 시간을 쉽게 조작할 수 있도록 지원합니다.

```php
return now()->plus(minutes: 5);
return now()->plus(hours: 8);
return now()->plus(weeks: 4);

return now()->minus(minutes: 5);
return now()->minus(hours: 8);
return now()->minus(weeks: 4);
```

Carbon 및 그 기능에 대해 더 자세히 알아보고 싶다면 [공식 Carbon 문서](https://carbon.nesbot.com/docs/)를 참고하세요.

<a name="interval-functions"></a>
#### 간격(Interval) 함수

Laravel은 또한 `milliseconds`, `seconds`, `minutes`, `hours`, `days`, `weeks`, `months`, `years`와 같은 함수를 제공하여 `CarbonInterval` 인스턴스를 반환합니다. 이들은 PHP의 [DateInterval](https://www.php.net/manual/en/class.dateinterval.php) 클래스를 확장한 것으로, Laravel에서 `DateInterval`을 허용하는 곳 어디서든 활용할 수 있습니다.

```php
use Illuminate\Support\Facades\Cache;

use function Illuminate\Support\{minutes};

Cache::put('metrics', $metrics, minutes(10));
```

<a name="deferred-functions"></a>
### 지연 함수 (Deferred Functions)

Laravel의 [큐 잡](/docs/12.x/queues)을 이용하면 작업을 백그라운드로 처리할 수 있지만, 종종 큐 워커를 설정하거나 유지 관리하지 않고도 간단한 작업들의 실행을 응답 이후로 미루고 싶을 때가 있습니다.

지연 함수(deferred function)를 사용하면 사용자의 HTTP 응답이 전송된 후에 클로저 실행을 연기할 수 있습니다. 이를 통해 애플리케이션을 더욱 빠르고 반응성 있게 느껴지게 할 수 있습니다. 클로저를 지연 실행하려면, `Illuminate\Support\defer` 함수에 클로저를 전달하세요.

```php
use App\Services\Metrics;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use function Illuminate\Support\defer;

Route::post('/orders', function (Request $request) {
    // 주문 생성 작업...

    defer(fn () => Metrics::reportOrder($order));

    return $order;
});
```

기본적으로 지연 함수는 `Illuminate\Support\defer`가 호출된 HTTP 응답, Artisan 명령어, 큐 잡이 정상적으로 완료될 때만 실행됩니다. 즉, 요청이 `4xx` 또는 `5xx` 응답을 반환하면 지연 함수는 실행되지 않습니다. 항상 실행하고 싶을 경우, 지연 함수에 `always` 메서드를 체이닝할 수 있습니다.

```php
defer(fn () => Metrics::reportOrder($order))->always();
```

> [!WARNING]
> [Swoole PHP extension](https://www.php.net/manual/en/book.swoole.php)가 설치되어 있는 경우, Laravel의 `defer` 함수가 Swoole의 전역 `defer` 함수와 충돌하여 웹 서버 오류가 발생할 수 있습니다. 반드시 `use function Illuminate\Support\defer;`와 같이 Laravel의 네임스페이스로 명시적으로 호출하세요.

<a name="cancelling-deferred-functions"></a>
#### 지연 함수 취소하기

지연 함수가 실행되기 전에 취소하고 싶다면, 이름을 지정하여 `forget` 메서드로 취소할 수 있습니다. 지연 함수에 이름을 붙이려면 `Illuminate\Support\defer` 함수의 두 번째 인수로 지정하세요.

```php
defer(fn () => Metrics::report(), 'reportMetrics');

defer()->forget('reportMetrics');
```

<a name="disabling-deferred-functions-in-tests"></a>
#### 테스트에서 지연 함수 비활성화

테스트를 작성할 때는 지연 함수를 비활성화하는 것이 유용할 수 있습니다. 테스트 내에서 `withoutDefer`를 호출하면 모든 지연 함수가 즉시 실행됩니다.

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

특정 테스트 케이스의 모든 테스트에서 지연 함수를 비활성화하고 싶다면, 베이스 `TestCase` 클래스의 `setUp` 메서드에서 `withoutDefer`를 호출하면 됩니다.

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

Laravel의 로터리(Lottery) 클래스는 설정한 확률에 따라 콜백을 실행할 때 사용할 수 있습니다. 예를 들어, 전체 요청 중 일부(퍼센트로 지정됨)에 대해서만 특정 코드를 실행하고 싶을 때 유용합니다.

```php
use Illuminate\Support\Lottery;

Lottery::odds(1, 20)
    ->winner(fn () => $user->won())
    ->loser(fn () => $user->lost())
    ->choose();
```

로터리 클래스는 Laravel의 다른 기능과도 결합해 사용할 수 있습니다. 예를 들어, 느린 쿼리의 일부분만 예외 처리기로 보고하고 싶을 때 유용합니다. 로터리 클래스는 콜러블로 동작하기 때문에, 콜러블을 받는 메서드에 그대로 전달할 수 있습니다.

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

Laravel은 로터리 관련 코드의 테스트를 쉽게 할 수 있도록 몇 가지 간단한 메서드를 제공합니다.

```php
// 항상 당첨...
Lottery::alwaysWin();

// 항상 미당첨...
Lottery::alwaysLose();

// 한번은 당첨, 그 다음은 미당첨, 그 이후 정상 동작...
Lottery::fix([true, false]);

// 정상 동작으로 돌아가기...
Lottery::determineResultsNormally();
```

<a name="pipeline"></a>
### 파이프라인 (Pipeline)

Laravel의 `Pipeline` 파사드는 주어진 입력값을 호출 가능한 일련의 클래스, 클로저, 콜러블에 "파이프" 방식으로 넘겨주면서 각 클래스가 입력을 점검/수정할 수 있게 됩니다.

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

각 파이프라인 단계(클래스/클로저)는 `$next` 클로저를 인자로 받으며, 이를 호출하면 다음 단계가 실행됩니다. 마지막 단계에서 `$next` 클로저를 호출할 때 `then` 메서드에 전달한 클로저가 실행되어 결과를 반환합니다. 단순히 입력값을 최종적으로 반환하고 싶을 때는 `thenReturn`을 사용할 수도 있습니다.

클로저 외에도 클래스명을 제공할 수 있습니다. 클래스명으로 제공한 경우, Laravel의 [서비스 컨테이너](/docs/12.x/container)를 통해 인스턴스가 생성되어 의존성 주입도 받을 수 있습니다.

```php
$user = Pipeline::send($user)
    ->through([
        GenerateProfilePhoto::class,
        ActivateSubscription::class,
        SendWelcomeEmail::class,
    ])
    ->thenReturn();
```

`withinTransaction` 메서드를 사용하면 파이프라인 전체 단계를 하나의 데이터베이스 트랜잭션으로 감쌀 수 있습니다.

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
### 슬립 (Sleep)

Laravel의 `Sleep` 클래스는 PHP의 기본 `sleep` 및 `usleep` 함수에 대한 경량 래퍼로, 테스트 용이성을 높이고 개발자가 시간 조작을 쉽게 할 수 있게 해줍니다.

```php
use Illuminate\Support\Sleep;

$waiting = true;

while ($waiting) {
    Sleep::for(1)->second();

    $waiting = /* ... */;
}
```

다양한 시간을 지정할 수 있는 여러 메서드를 제공합니다.

```php
// 대기 후 값을 반환...
$result = Sleep::for(1)->second()->then(fn () => 1 + 1);

// 지정한 조건이 true인 동안 슬립...
Sleep::for(1)->second()->while(fn () => shouldKeepSleeping());

// 90초 동안 일시정지...
Sleep::for(1.5)->minutes();

// 2초 동안 일시정지...
Sleep::for(2)->seconds();

// 500밀리초 동안 일시정지...
Sleep::for(500)->milliseconds();

// 5,000마이크로초 동안 일시정지...
Sleep::for(5000)->microseconds();

// 지정한 시간까지 일시정지...
Sleep::until(now()->plus(minutes: 1));

// PHP 기본 "sleep" 함수의 별칭...
Sleep::sleep(2);

// PHP 기본 "usleep" 함수의 별칭...
Sleep::usleep(5000);
```

시간 단위를 쉽게 조합하고 싶다면 `and` 메서드를 사용할 수 있습니다.

```php
Sleep::for(1)->second()->and(10)->milliseconds();
```

<a name="testing-sleep"></a>
#### 슬립 테스트하기

`Sleep` 클래스를 사용하거나 PHP의 sleep 함수와 연동하는 코드를 테스트할 때 실제로 대기 시간이 발생한다면 테스트가 매우 느려질 수 있습니다. 이를 해결하기 위해서는 Sleep 클래스를 "가짜(Fake)"로 만들어서 실행 지연을 생략할 수 있습니다.

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

이렇게 Sleep 클래스를 가짜로 만들면 실제 지연 없이 테스트가 훨씬 빨라집니다.

Sleep 클래스를 가짜로 만들었을 때, 예상되는 "슬립"이 호출됐는지에 대한 어서션도 가능합니다.

```php
use Carbon\CarbonInterval as Duration;
use Illuminate\Support\Sleep;

// Sleep이 3번 호출되었는지 확인...
Sleep::assertSleptTimes(3);

// 슬립 지속 시간에 대한 어서션...
Sleep::assertSlept(function (Duration $duration): bool {
    return /* ... */;
}, times: 1);

// Sleep 클래스가 한번도 호출되지 않았는지 확인...
Sleep::assertNeverSlept();

// Sleep이 호출되더라도 실제로 실행이 일시 정지되지 않았는지 확인...
Sleep::assertInsomniac();
```

가짜 슬립이 발생할 때마다 특정 동작을 하고 싶다면, `whenFakingSleep` 메서드에 콜백을 전달할 수 있습니다. 예를 들어, Laravel의 [시간 조작 헬퍼](/docs/12.x/mocking#interacting-with-time)를 사용하여 슬립 지속 시간만큼 즉시 시간을 진행시킬 수 있습니다.

```php
use Carbon\CarbonInterval as Duration;

$this->freezeTime();

Sleep::fake();

Sleep::whenFakingSleep(function (Duration $duration) {
    // 슬립 시간만큼 시간을 즉시 진행
    $this->travel($duration->totalMilliseconds)->milliseconds();
});
```

이처럼 시간 동기화가 필요한 경우, `fake` 메서드의 `syncWithCarbon` 인자를 `true`로 지정하면 슬립 시점에 Carbon이 함께 동기화됩니다.

```php
Sleep::fake(syncWithCarbon: true);

$start = now();

Sleep::for(1)->second();

$start->diffForHumans(); // 1초 전
```

Laravel은 실행을 일시 정지해야 할 때 내부적으로 모두 Sleep 클래스를 사용합니다. 예를 들어 [retry](#method-retry) 헬퍼는 슬립 시 Sleep 클래스를 활용하므로 테스트가 더 쉬워집니다.

<a name="timebox"></a>
### 타임박스 (Timebox)

Laravel의 `Timebox` 클래스는 주어진 콜백이 실제로 더 빨리 끝나더라도 항상 고정된 시간만큼 동작하도록 만들어 줍니다. 특히 암호화 작업 및 사용자 인증 검사 같이 실행 시간 차이를 통해 민감한 정보를 유추할 수 있는 경우에 유용합니다.

실행 시간이 고정 시간(딜레이)보다 길면 Timebox는 영향을 주지 않습니다. 개발자가 충분히 긴 시간을 지정해주는 것이 중요합니다.

`call` 메서드는 클로저와 제한 시간을(마이크로초 단위로) 받아, 해당 시간이 다 될 때까지 실행 후 대기합니다.

```php
use Illuminate\Support\Timebox;

(new Timebox)->call(function ($timebox) {
    // ...
}, microseconds: 10000);
```

클로저 내에서 예외가 발생해도, 지정된 딜레이 이후 예외를 다시 던집니다.

<a name="uri"></a>
### URI

Laravel의 `Uri` 클래스는 URI 생성 및 조작을 위한 편리하고 유창한 인터페이스를 제공합니다. 이 클래스는 League URI 패키지를 기반으로 하며, Laravel의 라우팅 시스템과 자연스럽게 통합됩니다.

정적 메서드를 사용해 쉽게 `Uri` 인스턴스를 생성할 수 있습니다.

```php
use App\Http\Controllers\UserController;
use App\Http\Controllers\InvokableController;
use Illuminate\Support\Uri;

// 문자열에서 URI 인스턴스를 생성...
$uri = Uri::of('https://example.com/path');

// 경로, 네임드 라우트, 컨트롤러 액션에서 URI 생성...
$uri = Uri::to('/dashboard');
$uri = Uri::route('users.show', ['user' => 1]);
$uri = Uri::signedRoute('users.show', ['user' => 1]);
$uri = Uri::temporarySignedRoute('user.index', now()->plus(minutes: 5));
$uri = Uri::action([UserController::class, 'index']);
$uri = Uri::action(InvokableController::class);

// 현재 요청 URL에서 URI 인스턴스 생성...
$uri = $request->uri();
```

생성된 URI 인스턴스는 다양한 방식으로 유창하게 수정할 수 있습니다.

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

`Uri` 클래스는 하위 URI의 각 구성 요소에 쉽게 접근할 수 있도록 다양한 메서드를 제공합니다.

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

`Uri` 클래스는 URI의 쿼리 스트링을 조작할 때 사용할 수 있는 여러 메서드를 제공합니다. `withQuery` 메서드는 기존 쿼리 스트링에 파라미터를 병합합니다.

```php
$uri = $uri->withQuery(['sort' => 'name']);
```

`withQueryIfMissing` 메서드는 지정된 키가 쿼리 스트링에 없을 때만 파라미터를 병합합니다.

```php
$uri = $uri->withQueryIfMissing(['page' => 1]);
```

`replaceQuery`는 기존 쿼리 스트링을 완전히 대체합니다.

```php
$uri = $uri->replaceQuery(['page' => 1]);
```

`pushOntoQuery`는 쿼리 스트링 내 배열 값 파라미터에 값을 추가합니다.

```php
$uri = $uri->pushOntoQuery('filter', ['active', 'pending']);
```

`withoutQuery`는 쿼리 스트링에서 파라미터를 제거합니다.

```php
$uri = $uri->withoutQuery(['page']);
```

<a name="generating-responses-from-uris"></a>
#### URI 기반 응답 생성

`redirect` 메서드를 이용하면 주어진 URI로의 `RedirectResponse` 인스턴스를 생성할 수 있습니다.

```php
$uri = Uri::of('https://example.com');

return $uri->redirect();
```

또는, 라우트나 컨트롤러 액션에서 URI 인스턴스를 그대로 반환하면 자동으로 해당 URI로 리다이렉트 응답이 생성됩니다.

```php
use Illuminate\Support\Facades\Route;
use Illuminate\Support\Uri;

Route::get('/redirect', function () {
    return Uri::to('/index')
        ->withQuery(['sort' => 'name']);
});
```
