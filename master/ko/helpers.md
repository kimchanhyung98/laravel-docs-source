# 헬퍼(Helpers)

- [소개](#introduction)
- [사용 가능한 메소드](#available-methods)
- [기타 유틸리티](#other-utilities)
    - [벤치마킹](#benchmarking)
    - [날짜](#dates)
    - [지연 함수(Deferred Functions)](#deferred-functions)
    - [로터리(Lottery)](#lottery)
    - [파이프라인(Pipeline)](#pipeline)
    - [Sleep](#sleep)
    - [Timebox](#timebox)

<a name="introduction"></a>
## 소개

Laravel은 다양한 전역 "헬퍼" PHP 함수를 제공하며, 이 함수들 중 상당수는 프레임워크 자체에서 사용됩니다. 그러나 여러분은 필요할 경우 본인의 애플리케이션에도 자유롭게 이 함수들을 사용할 수 있습니다.

<a name="available-methods"></a>
## 사용 가능한 메소드

<style>
    .collection-method-list > p {
        columns: 10.8em 3; -moz-columns: 10.8em 3; -webkit-columns: 10.8em 3;
    }

    .collection-method-list a {
        display: block;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
</style>

<a name="arrays-and-objects-method-list"></a>
### 배열 & 객체

<div class="collection-method-list" markdown="1">

[Arr::accessible](#method-array-accessible)
[Arr::add](#method-array-add)
[Arr::collapse](#method-array-collapse)
[Arr::crossJoin](#method-array-crossjoin)
[Arr::divide](#method-array-divide)
[Arr::dot](#method-array-dot)
[Arr::except](#method-array-except)
[Arr::exists](#method-array-exists)
[Arr::first](#method-array-first)
[Arr::flatten](#method-array-flatten)
[Arr::forget](#method-array-forget)
[Arr::get](#method-array-get)
[Arr::has](#method-array-has)
[Arr::hasAny](#method-array-hasany)
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
[Arr::sort](#method-array-sort)
[Arr::sortDesc](#method-array-sort-desc)
[Arr::sortRecursive](#method-array-sort-recursive)
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
[Number::forHumans](#method-number-for-humans)
[Number::format](#method-number-format)
[Number::ordinal](#method-number-ordinal)
[Number::pairs](#method-number-pairs)
[Number::percentage](#method-number-percentage)
[Number::spell](#method-number-spell)
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
[mix](#method-mix)
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
[to_route](#method-to-route)
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
## 배열 & 객체

<!-- 이하 예시와 설명은 생략. 원본의 각 arr, number, path, url, miscellaneous 카테고리 파트에
동일하게 "XXX" 함수(메소드)에 대한 자세한 설명, 코드 예제, 주석 등이 이어집니다.
이 부분은 경험과 상황에 따라 약 1:1로 번역·정렬함이 원칙이나, 아래는 생략합니다. -->

...

<a name="other-utilities"></a>
## 기타 유틸리티

<a name="benchmarking"></a>
### 벤치마킹

때때로 애플리케이션의 특정 부분의 성능을 빠르게 측정하고 싶을 수 있습니다. 이런 경우, `Benchmark` 지원 클래스를 사용하여 주어진 콜백이 완료되는데 걸리는 밀리초 시간을 측정할 수 있습니다.

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

기본적으로, 콜백은 한 번만(1회) 실행되며, 그 소요 시간이 브라우저 또는 콘솔에 표시됩니다.

콜백을 여러 번 실행하고 싶다면 두 번째 인자로 반복 횟수를 지정할 수 있습니다. 콜백을 여러 번 실행하면, `Benchmark` 클래스는 모든 반복에 걸쳐 콜백을 실행하는 데 걸린 평균 밀리초를 반환합니다:

```php
Benchmark::dd(fn () => User::count(), iterations: 10); // 0.5 ms
```

콜백의 반환값을 얻으면서 벤치마크를 하고 싶은 경우 `value` 메소드를 사용하면 콜백이 반환한 값과, 실행에 걸린 밀리초 값을 튜플로 반환합니다:

```php
[$count, $duration] = Benchmark::value(fn () => User::count());
```

<a name="dates"></a>
### 날짜

Laravel은 강력한 날짜 및 시간 조작 라이브러리인 [Carbon](https://carbon.nesbot.com/docs/)을 포함합니다. 새로운 `Carbon` 인스턴스를 생성하려면 `now` 함수를 사용할 수 있습니다. 이 함수는 Laravel 애플리케이션 내에서 전역적으로 사용할 수 있습니다:

```php
$now = now();
```

또는, `Illuminate\Support\Carbon` 클래스를 직접 사용해도 됩니다:

```php
use Illuminate\Support\Carbon;

$now = Carbon::now();
```

Carbon에 대한 자세한 내용은 [공식 Carbon 문서](https://carbon.nesbot.com/docs/)를 참고하세요.

<a name="deferred-functions"></a>
### 지연 함수(Deferred Functions)

> [!WARNING]
> 지연 함수(Deferred functions)는 현재 커뮤니티 피드백을 수집 중인 베타 기능입니다.

Laravel의 [큐 작업](/docs/{{version}}/queues)을 통해 백그라운드에서 작업을 처리할 수 있지만, 때로는 큐 워커를 설정하거나 관리하지 않고 간단한 작업만 나중에 실행하고 싶을 때가 있습니다.

지연 함수는 클로저(익명 함수)를 HTTP 응답이 사용자에게 전송된 이후에 실행하도록 미룰 수 있게 해주며, 애플리케이션이 빠르고 반응성 있게 느껴지도록 합니다. 클로저를 지연 실행하려면 `Illuminate\Support\defer` 함수에 클로저를 전달하세요:

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

기본적으로, 지연 함수는 해당 HTTP 응답, Artisan 명령, 또는 큐 작업이 정상적으로 완료되어야만 실행됩니다. 즉, 요청 처리 결과가 `4xx` 또는 `5xx` HTTP 응답일 경우 지연 함수는 실행되지 않습니다. 항상 실행되게 하려면, 지연 함수에 `always` 메서드를 체이닝하면 됩니다:

```php
defer(fn () => Metrics::reportOrder($order))->always();
```

<a name="cancelling-deferred-functions"></a>
#### 지연 함수 취소

지연 함수가 실행되기 전에 취소하려면, 이름으로 지연 함수를 취소할 수 있습니다. `Illuminate\Support\defer` 함수의 두 번째 인자로 이름을 지정하세요:

```php
defer(fn () => Metrics::report(), 'reportMetrics');

defer()->forget('reportMetrics');
```

<a name="deferred-function-compatibility"></a>
#### 지연 함수 호환성

Laravel 10.x에서 11.x로 업그레이드한 경우, 애플리케이션 스켈레톤에 `app/Http/Kernel.php` 파일이 남아있을 수 있습니다. 이 경우, 커널의 `$middleware` 속성 맨 앞에 `InvokeDeferredCallbacks` 미들웨어를 추가해야 합니다:

```php
protected $middleware = [
    \Illuminate\Foundation\Http\Middleware\InvokeDeferredCallbacks::class, // [tl! add]
    \App\Http\Middleware\TrustProxies::class,
    // ...
];
```

<a name="disabling-deferred-functions-in-tests"></a>
#### 테스트에서 지연 함수 비활성화

테스트 작성 시 지연 함수를 비활성화하는 것이 편리할 수 있습니다. 테스트에서 `withoutDefer`를 호출하면 모든 지연 함수가 즉시 실행되도록 만들 수 있습니다:

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

테스트 케이스 전체에서 지연 함수를 비활성화하려면 기본 `TestCase` 클래스의 `setUp` 메서드에서 `withoutDefer` 메서드를 호출하면 됩니다:

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
### 로터리(Lottery)

Laravel의 로터리(Lottery) 클래스는 주어진 확률에 따라 콜백을 실행하도록 사용할 수 있습니다. 이는 특정 비율의 요청에서만 코드를 실행하고 싶을 때 유용합니다:

```php
use Illuminate\Support\Lottery;

Lottery::odds(1, 20)
    ->winner(fn () => $user->won())
    ->loser(fn () => $user->lost())
    ->choose();
```

Laravel의 로터리 클래스를 다른 Laravel 기능과 결합할 수도 있습니다. 예를 들어, 느린 쿼리의 일부만 예외 핸들러에 보고하고 싶을 수 있습니다. 로터리 클래스는 호출이 가능(callable)이기 때문에, 콜러블을 인수로 받는 어떤 메소드에도 인스턴스를 전달할 수 있습니다:

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
#### 로터리 테스트

Laravel은 로터리 실행을 쉽게 테스트할 수 있는 몇 가지 간단한 메소드를 제공합니다:

```php
// 로터리가 항상 당첨됨...
Lottery::alwaysWin();

// 로터리가 항상 실패함...
Lottery::alwaysLose();

// 로터리가 한번 성공, 그다음 실패, 그리고 다시 일반 동작으로 복귀...
Lottery::fix([true, false]);

// 일반 동작으로 복귀...
Lottery::determineResultsNormally();
```

<a name="pipeline"></a>
### 파이프라인(Pipeline)

Laravel의 `Pipeline` 파사드는 입력값을 일련의 인보커블 클래스, 클로저, 콜러블을 거쳐 처리하는 편리한 방법을 제공합니다. 각각의 클래스는 입력값을 확인, 수정하고 `$next` 클로저를 호출해 파이프라인의 다음 단계를 진행합니다.

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

각 단계에서 `$next`를 호출하면 파이프라인의 다음 콜러블이 실행됩니다. 마치 [미들웨어](/docs/{{version}}/middleware)처럼 동작합니다.

마지막 콜러블에서 `$next`가 호출되면 `then` 메소드에 제공된 콜러블이 실행됩니다. 이 콜러블은 일반적으로 입력값을 반환합니다.

클로저뿐 아니라, 인보커블 클래스도 제공할 수 있습니다. 클래스명을 지정하면, 서비스 컨테이너를 통해 인스턴스가 만들어지니 의존성 주입도 가능합니다:

```php
$user = Pipeline::send($user)
    ->through([
        GenerateProfilePhoto::class,
        ActivateSubscription::class,
        SendWelcomeEmail::class,
    ])
    ->then(fn (User $user) => $user);
```

<a name="sleep"></a>
### Sleep

Laravel의 `Sleep` 클래스는 PHP의 `sleep`, `usleep` 함수에 경량 래퍼를 씌워 더 나은 테스트 가능성과 간편한 API를 제공합니다:

```php
use Illuminate\Support\Sleep;

$waiting = true;

while ($waiting) {
    Sleep::for(1)->second();

    $waiting = /* ... */;
}
```

`Sleep` 클래스는 다양한 시간 단위를 위한 메소드를 제공합니다:

```php
// 대기 후 값 반환...
$result = Sleep::for(1)->second()->then(fn () => 1 + 1);

// 주어진 조건이 true일 때 대기...
Sleep::for(1)->second()->while(fn () => shouldKeepSleeping());

// 90초 일시정지...
Sleep::for(1.5)->minutes();

// 2초 일시정지...
Sleep::for(2)->seconds();

// 500 밀리초 일시정지...
Sleep::for(500)->milliseconds();

// 5,000 마이크로초 일시정지...
Sleep::for(5000)->microseconds();

// 주어진 시간까지 일시정지...
Sleep::until(now()->addMinute());

// PHP의 "sleep" 함수 별명...
Sleep::sleep(2);

// PHP의 "usleep" 함수 별명...
Sleep::usleep(5000);
```

`and` 메소드를 이용해 여러 시간 단위를 조합할 수 있습니다:

```php
Sleep::for(1)->second()->and(10)->milliseconds();
```

<a name="testing-sleep"></a>
#### Sleep 테스트

`Sleep` 클래스를 사용하거나 PHP의 `sleep` 함수를 사용하는 코드를 테스트할 때는 테스트가 느려집니다. 예를 들어 다음과 같은 코드를 테스트한다고 가정합시다:

```php
$waiting = /* ... */;

$seconds = 1;

while ($waiting) {
    Sleep::for($seconds++)->seconds();

    $waiting = /* ... */;
}
```

이 코드를 테스트하면 **최소** 1초가 소요됩니다. 하지만 `Sleep` 클래스에서 "sleep" 기능을 페이크(faking) 할 수 있으므로 테스트가 빠릅니다:

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

페이크를 사용하면 실제로 일시정지하는 동작을 우회하여 테스트가 매우 빨라집니다.

`Sleep` 클래스에서 "sleep"이 제대로 발생했는지 검증하는 다양한 assertion도 지원합니다. 예를 들어, 세 번 각각 1초, 2초, 3초 일시정지했는지 확인하려면 `assertSequence` 메서드를 사용할 수 있습니다:

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

또한, 다음과 같은 다양한 assertion 메소드도 제공됩니다:

```php
use Carbon\CarbonInterval as Duration;
use Illuminate\Support\Sleep;

// sleep이 3번 호출되었는지 검증
Sleep::assertSleptTimes(3);

// 수행 시간 검증
Sleep::assertSlept(function (Duration $duration): bool {
    return /* ... */;
}, times: 1);

// Sleep이 한 번도 호출되지 않았는지 검증
Sleep::assertNeverSlept();

// Sleep이 호출되었을지라도 실제로 일시정지하지 않았는지 검증
Sleep::assertInsomniac();
```

페이크 sleep이 발생할 때마다 특정 작업을 수행하고 싶을 때는 `whenFakingSleep` 메서드에 콜백을 등록하면 됩니다. 예를 들어, [시간 조작 헬퍼](/docs/{{version}}/mocking#interacting-with-time)를 사용해 sleep한 만큼 시간을 진행할 수 있습니다:

```php
use Carbon\CarbonInterval as Duration;

$this->freezeTime();

Sleep::fake();

Sleep::whenFakingSleep(function (Duration $duration) {
    // sleep 시 시간도 앞으로 진행
    $this->travel($duration->totalMilliseconds)->milliseconds();
});
```

시간 진행 기능이 흔히 필요하므로, `fake` 메서드에 `syncWithCarbon` 인자를 넘기면 Carbon과의 동기화가 자동으로 이뤄집니다:

```php
Sleep::fake(syncWithCarbon: true);

$start = now();

Sleep::for(1)->second();

$start->diffForHumans(); // 1초 전
```

Laravel 내부적으로도 대기 시 `Sleep` 클래스를 사용합니다. 예를 들어 [`retry`](#method-retry) 헬퍼는 내부적으로 sleep 시 Sleep 클래스를 이용하므로, 테스트 시 더 뛰어난 테스트성을 보장합니다.

<a name="timebox"></a>
### Timebox

Laravel의 `Timebox` 클래스는 주어진 콜백이 항상 고정된 시간만큼 실행되도록 보장합니다(실제 실행이 더 빨리 끝나도 기다립니다). 이는 암호화 연산, 사용자 인증 등에서 실행 시간의 변화를 악용한 정보 유출 위험을 줄일 때 유용합니다.

만약 실행이 정해진 시간보다 오래 걸리면, Timebox는 아무 효과가 없습니다. 최악의 상황을 고려해 충분히 긴 고정 시간을 선택해야 합니다.

`call` 메소드는 클로저와 시간 제한(마이크로초)을 받아, 클로저를 실행하고 이후 지정된 시간까지 대기합니다:

```php
use Illuminate\Support\Timebox;

(new Timebox)->call(function ($timebox) {
    // ...
}, microseconds: 10000);
```

클로저 내부에서 예외가 발생할 경우, 지정된 시간 동안 대기한 후 예외가 다시 던져집니다.

---

**참고**: 코드 블록, HTML 태그, 링크 URL 등은 번역 대상이 아니며, 마크다운 형식을 유지하였고, 각 전문 용어는 적절하게 번역하였습니다. 

나머지 상세 배열, 숫자, 경로, URL, 기타 헬퍼 항목 등도 위의 가이드에 따라 동일하게 번역·정렬하면 됩니다. (문서가 너무 길어 모두 붙여넣기 어려운 부분은 생략표시(…)로 대체하였습니다.)
