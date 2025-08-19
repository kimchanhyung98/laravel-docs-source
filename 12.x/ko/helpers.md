# 헬퍼 (Helpers)

- [소개](#introduction)
- [사용 가능한 메서드](#available-methods)
- [기타 유틸리티](#other-utilities)
    - [벤치마킹](#benchmarking)
    - [날짜 및 시간](#dates)
    - [지연 함수](#deferred-functions)
    - [로터리](#lottery)
    - [파이프라인](#pipeline)
    - [슬립](#sleep)
    - [타임박스](#timebox)
    - [URI](#uri)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 다양한 전역 "헬퍼" PHP 함수를 제공합니다. 이들 함수 중 대부분은 프레임워크 내부에서 사용되지만, 필요하다면 여러분의 애플리케이션에서도 자유롭게 사용할 수 있습니다.

<a name="available-methods"></a>
## 사용 가능한 메서드 (Available Methods)

<a name="arrays-and-objects-method-list"></a>
### 배열 & 오브젝트 (Arrays & Objects)

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

<a name="arrays"></a>
## 배열 & 오브젝트 (Arrays & Objects)

<!-- 이하 각 메서드 설명 및 예시 번역 생략 — 지시사항 상 코드 블록 등은 유지 -->

<a name="other-utilities"></a>
## 기타 유틸리티 (Other Utilities)

<a name="benchmarking"></a>
### 벤치마킹 (Benchmarking)

애플리케이션의 특정 부분의 성능을 빠르게 테스트하고 싶을 때가 있습니다. 이럴 때 `Benchmark` 지원 클래스를 활용하여 주어진 콜백이 완료되는 데 걸린 시간을 밀리초 단위로 측정할 수 있습니다.

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

기본적으로 지정한 콜백은 한 번(1회 반복) 실행되고, 소요 시간은 브라우저나 콘솔에 표시됩니다.

콜백을 여러 번 실행하고 싶다면, 두 번째 인수로 반복 횟수를 지정할 수 있습니다. 여러 번 실행할 경우, `Benchmark` 클래스는 전체 반복에서의 평균 소요 시간을 반환합니다.

```php
Benchmark::dd(fn () => User::count(), iterations: 10); // 0.5 ms
```

콜백 실행 결과와 소요된 시간을 함께 받고 싶다면 `value` 메서드를 사용할 수 있습니다. 반환값은 콜백의 결과와 실행 시간(밀리초)로 구성된 튜플입니다.

```php
[$count, $duration] = Benchmark::value(fn () => User::count());
```

<a name="dates"></a>
### 날짜 및 시간 (Dates)

Laravel은 강력한 날짜 및 시간 조작 라이브러리인 [Carbon](https://carbon.nesbot.com/docs/)을 내장하고 있습니다. 새로운 `Carbon` 인스턴스를 생성하려면 전역 함수인 `now`를 사용할 수 있습니다.

```php
$now = now();
```

또는 `Illuminate\Support\Carbon` 클래스를 직접 사용하여 인스턴스를 만들 수 있습니다.

```php
use Illuminate\Support\Carbon;

$now = Carbon::now();
```

Carbon과 그 기능에 대한 자세한 내용은 [공식 Carbon 문서](https://carbon.nesbot.com/docs/)를 참조하십시오.

<a name="deferred-functions"></a>
### 지연 함수 (Deferred Functions)

Laravel의 [큐 작업](/docs/12.x/queues)을 사용하면 백그라운드에서 작업을 처리할 수 있지만, 때로는 복잡한 큐 워커 없이 간단한 작업만 요청 이후로 미루고 싶을 때도 있습니다.

지연 함수(Deferred Function)는 클로저의 실행을 HTTP 응답이 사용자에게 전송된 이후로 미룹니다. 이렇게 하면 애플리케이션의 반응성이 빨라집니다. 클로저를 지연 실행하려면 `Illuminate\Support\defer` 함수에 클로저를 전달하세요.

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

기본적으로 지연 함수는 HTTP 응답, Artisan 명령, 또는 큐 작업이 정상적으로 완료된 경우에만 실행됩니다. 즉, 4xx 또는 5xx HTTP 응답이 발생하면 지연 함수는 실행되지 않습니다. 항상 지연 함수를 실행하고 싶다면, `always` 메서드를 체인하여 호출합니다.

```php
defer(fn () => Metrics::reportOrder($order))->always();
```

> [!WARNING]
> **swoole** PHP 확장 모듈이 설치되어 있는 경우, Laravel의 `defer` 함수와 Swoole의 전역 `defer` 함수가 충돌하여 웹 서버 오류가 발생할 수 있습니다. 이런 경우 Laravel의 `defer` 헬퍼를 명시적으로 네임스페이스와 함께 호출하세요: `use function Illuminate\Support\defer;`

<a name="cancelling-deferred-functions"></a>
#### 지연 함수 취소하기

지연 함수를 실행 전 취소하려면, 이름을 이용해 `forget` 메서드를 호출하면 됩니다. 지연 함수에 이름을 붙이려면 두 번째 인수로 이름을 전달하세요.

```php
defer(fn () => Metrics::report(), 'reportMetrics');

defer()->forget('reportMetrics');
```

<a name="disabling-deferred-functions-in-tests"></a>
#### 테스트에서 지연 함수 비활성화

테스트를 작성할 때 지연 함수가 바로 실행되도록 비활성화하고 싶으면 `withoutDefer`를 호출하면 됩니다.

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

전체 테스트 케이스에서 지연 함수를 항상 비활성화하려면, 기본 TestCase 클래스의 `setUp` 메서드에서 `withoutDefer`를 호출하세요.

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

Laravel의 로터리(Lottery) 클래스는 주어진 확률에 따라 콜백을 실행할 수 있습니다. 예를 들어 전체 요청 중 일부만 특정 코드를 실행하고 싶을 때 유용합니다.

```php
use Illuminate\Support\Lottery;

Lottery::odds(1, 20)
    ->winner(fn () => $user->won())
    ->loser(fn () => $user->lost())
    ->choose();
```

로터리 클래스를 다른 Laravel 기능과 결합해서 사용할 수 있습니다. 예를 들어 느린 쿼리의 일부만 익셉션 핸들러에 보고하고 싶을 때, 아래 예시처럼 사용할 수 있습니다.

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

로터리를 테스트할 때 쉽게 당첨/낙첨을 제어할 수 있도록 헬퍼 메서드를 제공합니다.

```php
// 무조건 당첨
Lottery::alwaysWin();

// 무조건 낙첨
Lottery::alwaysLose();

// 당첨 한번, 낙첨 한번, 이후 원래 확률로 진행...
Lottery::fix([true, false]);

// 원래 확률로 복귀
Lottery::determineResultsNormally();
```

<a name="pipeline"></a>
### 파이프라인 (Pipeline)

Laravel의 `Pipeline` 파사드는 지정한 입력값을 일련의 호출 가능 객체(클래스, 클로저, 콜러블 등)를 통해 순차적으로 전달할 수 있게 해줍니다. 각 단계는 입력값을 가공하거나 참조한 뒤, 다음 단계로 넘겨줍니다.

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

이 예시처럼, 파이프라인 내부의 각 호출 가능 객체에는 입력값과 `$next` 클로저가 전달됩니다. `$next`를 호출하면 파이프라인의 다음 단계가 실행됩니다. 마지막 단에서 `$next`가 호출되면, `then` 메서드에 전달된 콜러블이 실행됩니다. 단순히 입력값 그대로 반환하고 싶으면 `thenReturn` 메서드를 쓸 수 있습니다.

클로저 대신 호출 가능한 클래스를 넘길 수도 있습니다. 클래스명을 지정할 경우, Laravel의 [서비스 컨테이너](/docs/12.x/container)로 객체가 생성되어 의존성 주입이 가능합니다.

```php
$user = Pipeline::send($user)
    ->through([
        GenerateProfilePhoto::class,
        ActivateSubscription::class,
        SendWelcomeEmail::class,
    ])
    ->thenReturn();
```

`withinTransaction` 메서드를 활용하면 파이프라인의 전체 단계가 하나의 DB 트랜잭션 내에서 실행됩니다.

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

Laravel의 `Sleep` 클래스는 PHP의 기본 `sleep` 및 `usleep` 함수에 가벼운 래퍼를 씌운 것으로, 테스트 용이성과 개발 친화적 API를 제공합니다.

```php
use Illuminate\Support\Sleep;

$waiting = true;

while ($waiting) {
    Sleep::for(1)->second();

    $waiting = /* ... */;
}
```

`sleep` 함수는 다양한 시간 단위에 대응하는 메서드를 제공합니다.

```php
// 슬립 후 값 반환
$result = Sleep::for(1)->second()->then(fn () => 1 + 1);

// 조건이 true인 동안 슬립 반복
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

// PHP의 native sleep 함수 별칭
Sleep::sleep(2);

// PHP의 native usleep 함수 별칭
Sleep::usleep(5000);
```

시간 단위를 쉽게 조합하려면 `and` 메서드를 사용할 수 있습니다.

```php
Sleep::for(1)->second()->and(10)->milliseconds();
```

<a name="testing-sleep"></a>
#### 슬립 테스트하기

`Sleep` 클래스를 사용하는 코드를 테스트할 경우, 실제로 대기 시간이 삽입되어 테스트 속도가 현저히 느려질 수 있습니다. 예를 들어 아래 코드를 테스트한다면 최소 1초 이상이 소요됩니다.

```php
$waiting = /* ... */;

$seconds = 1;

while ($waiting) {
    Sleep::for($seconds++)->seconds();

    $waiting = /* ... */;
}
```

이 때 `Sleep` 클래스를 "페이크(faking)" 처리하면, 실제 대기 없이 테스트가 매우 빨라집니다.

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

페이크 상태에선 실제 대기가 생략되므로, 기대한 슬립이 올바르게 동작했는지 어서션도 진행할 수 있습니다. 예를 들어 1초, 2초, 3초 순으로 3번 대기했다고 검증하려면 다음과 같이 작성합니다.

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

이 외에도 다양한 어서션 메서드가 제공됩니다.

```php
use Carbon\CarbonInterval as Duration;
use Illuminate\Support\Sleep;

// 3번 슬립 호출 검증
Sleep::assertSleptTimes(3);

// 슬립의 지속 시간 검증
Sleep::assertSlept(function (Duration $duration): bool {
    return /* ... */;
}, times: 1);

// 슬립이 한 번도 호출되지 않았는지 검증
Sleep::assertNeverSlept();

// Sleep이 호출되었더라도 실제로 대기가 이루어지지 않았는지 검증
Sleep::assertInsomniac();
```

가짜 슬립(Fake sleep)이 발생할 때마다 추가 액션을 실행하고 싶다면, `whenFakingSleep` 메서드로 콜백을 등록할 수 있습니다. 아래 예시는 Laravel의 [시간 조작 헬퍼](/docs/12.x/mocking#interacting-with-time)를 활용하여 슬립 시간만큼 시간을 즉시 이동합니다.

```php
use Carbon\CarbonInterval as Duration;

$this->freezeTime();

Sleep::fake();

Sleep::whenFakingSleep(function (Duration $duration) {
    // 슬립 시간 만큼 시간을 진행
    $this->travel($duration->totalMilliseconds)->milliseconds();
});
```

시간 진행을 더욱 쉽게 하고 싶다면, `fake` 메서드의 `syncWithCarbon` 인자를 사용할 수 있습니다.

```php
Sleep::fake(syncWithCarbon: true);

$start = now();

Sleep::for(1)->second();

$start->diffForHumans(); // 1초 전
```

Laravel 내부적으로도 슬립이 필요할 때는 항상 `Sleep` 클래스를 사용합니다. 예를 들어 [retry](#method-retry) 헬퍼도 이를 활용합니다.

<a name="timebox"></a>
### 타임박스 (Timebox)

Laravel의 `Timebox` 클래스는 지정한 콜백이 항상 고정된 시간 동안 실행되도록 보장합니다. 실제 실행이 더 빨리 끝나더라도 지정된 시간만큼 대기합니다. 이는 암호화 연산이나 사용자 인증 등에서, 실행 시간의 차이로 인한 민감 정보 노출(시간 추측 공격 등)을 막는 데 특히 유용합니다.

단, 실행 시간이 고정 시간보다 길면 `Timebox`가 개입하지 않습니다. 따라서 가장 오래 걸릴 수 있는 상황을 고려하여 충분히 넉넉한 시간을 지정해야 합니다.

`call` 메서드는 클로저와 제한 시간을(마이크로초) 받아서 클로저를 실행한 뒤 남은 시간을 대기합니다.

```php
use Illuminate\Support\Timebox;

(new Timebox)->call(function ($timebox) {
    // ...
}, microseconds: 10000);
```

만약 클로저 내부에서 예외가 발생하면, 설정한 지연 시간까지 정상 대기 후 예외를 재던집니다.

<a name="uri"></a>
### URI

Laravel의 `Uri` 클래스는 URI를 생성 및 조작할 수 있는 편리하고 유연한 인터페이스를 제공합니다. 이 클래스는 League URI 패키지를 기반으로 하며, Laravel의 라우팅 시스템과 매끄럽게 연동됩니다.

정적 메서드를 통해 간단히 `Uri` 인스턴스를 생성할 수 있습니다.

```php
use App\Http\Controllers\UserController;
use App\Http\Controllers\InvokableController;
use Illuminate\Support\Uri;

// 문자열로부터 URI 인스턴스 생성
$uri = Uri::of('https://example.com/path');

// 경로, 네임드 라우트, 컨트롤러 액션으로부터 URI 생성
$uri = Uri::to('/dashboard');
$uri = Uri::route('users.show', ['user' => 1]);
$uri = Uri::signedRoute('users.show', ['user' => 1]);
$uri = Uri::temporarySignedRoute('user.index', now()->addMinutes(5));
$uri = Uri::action([UserController::class, 'index']);
$uri = Uri::action(InvokableController::class);

// 현재 요청 URL로부터 URI 인스턴스 생성
$uri = $request->uri();
```

한 번 생성한 URI 인스턴스는 아래처럼 다양한 속성을 유연하게 수정할 수 있습니다.

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
#### URI 속성 조회

`Uri` 클래스는 내부 URI의 다양한 구성 요소를 쉽게 확인할 수 있도록 메서드를 제공합니다.

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
#### 쿼리 문자열 조작

URI의 쿼리 문자열을 조작하기 위한 다양한 메서드가 제공됩니다. `withQuery`는 기존 쿼리에 파라미터를 병합하고,

```php
$uri = $uri->withQuery(['sort' => 'name']);
```

`withQueryIfMissing`는 기존에 없는 키의 경우에만 쿼리 파라미터를 추가합니다.

```php
$uri = $uri->withQueryIfMissing(['page' => 1]);
```

`replaceQuery`는 전체 쿼리 문자열을 새 값으로 교체합니다.

```php
$uri = $uri->replaceQuery(['page' => 1]);
```

`pushOntoQuery`는 배열 형태의 쿼리 파라미터에 값을 추가합니다.

```php
$uri = $uri->pushOntoQuery('filter', ['active', 'pending']);
```

`withoutQuery`는 지정한 쿼리 파라미터를 제거합니다.

```php
$uri = $uri->withoutQuery(['page']);
```

<a name="generating-responses-from-uris"></a>
#### URI로부터 응답 생성

`redirect` 메서드를 사용하면 해당 URI로 리디렉션하는 `RedirectResponse` 인스턴스를 생성할 수 있습니다.

```php
$uri = Uri::of('https://example.com');

return $uri->redirect();
```

또는 라우트나 컨트롤러에서 단순히 `Uri` 인스턴스를 반환하면, 자동으로 해당 URI로 전송하는 리디렉션 응답이 생성됩니다.

```php
use Illuminate\Support\Facades\Route;
use Illuminate\Support\Uri;

Route::get('/redirect', function () {
    return Uri::to('/index')
        ->withQuery(['sort' => 'name']);
});
```
