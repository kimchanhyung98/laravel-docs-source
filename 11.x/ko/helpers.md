# 헬퍼(Helpers)

- [소개](#introduction)
- [사용 가능한 메서드](#available-methods)
- [기타 유틸리티](#other-utilities)
    - [벤치마킹(Benchmarking)](#benchmarking)
    - [날짜](#dates)
    - [지연 함수(Deferred Functions)](#deferred-functions)
    - [로터리(Lottery)](#lottery)
    - [파이프라인(Pipeline)](#pipeline)
    - [슬립(Sleep)](#sleep)
    - [타임박스(Timebox)](#timebox)

<a name="introduction"></a>
## 소개

Laravel에는 다양한 전역 "헬퍼" PHP 함수들이 포함되어 있습니다. 이 함수들 중 다수는 프레임워크 자체에서 사용되지만, 여러분은 필요에 따라 애플리케이션에서 자유롭게 사용할 수 있습니다.

<a name="available-methods"></a>
## 사용 가능한 메서드

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
[Arr::pluck](#method-array-pluck)
[Arr::prepend](#method-array-prepend)
[Arr::prependKeysWith](#method-array-prependkeyswith)
[Arr::pull](#method-array-pull)
[Arr::query](#method-array-query)
[Arr::random](#method-array-random)
[Arr::reject](#method-array-reject)
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

---

**아래 메서드별 설명, 예시 포함 부분은 요청하시면 추가 제공합니다.**  
문서가 매우 길기 때문에, 위 인덱스/목차 및 소개, 기타 안내 등 전형적인 마크다운 구조와 용어 번역을 우선 제공합니다.

아래는 "기타 유틸리티" 주요 항목에 대해 전문 용어와 마크다운 양식 준수하여 예시를 들어 번역한 예시 섹션입니다.

---

<a name="other-utilities"></a>
## 기타 유틸리티

<a name="benchmarking"></a>
### 벤치마킹(Benchmarking)

애플리케이션의 특정 부분의 성능을 빠르게 테스트할 때, `Benchmark` 지원 클래스를 사용하여 지정한 콜백이 완료되는 데 걸리는 밀리초(ms) 시간을 측정할 수 있습니다.

```php
use App\Models\User;
use Illuminate\Support\Benchmark;

Benchmark::dd(fn () => User::find(1)); // 0.1 ms

Benchmark::dd([
    '시나리오 1' => fn () => User::count(),         // 0.5 ms
    '시나리오 2' => fn () => User::all()->count(), // 20.0 ms
]);
```

기본적으로 지정한 콜백은 한 번(1회) 실행되며, 소요 시간이 브라우저/콘솔에 표시됩니다.

콜백을 여러 번 호출하고 싶다면 두 번째 인자로 반복 횟수를 지정할 수 있습니다. 이 경우 `Benchmark` 클래스는 모든 반복에 걸친 평균 실행 시간을 반환합니다.

```php
Benchmark::dd(fn () => User::count(), iterations: 10); // 0.5 ms
```

콜백 실행 값을 반환받으면서 벤치마킹하고 싶다면 `value` 메서드를 사용해 반환값과 소요 시간 튜플을 받을 수 있습니다.

```php
[$count, $duration] = Benchmark::value(fn () => User::count());
```

---

<a name="dates"></a>
### 날짜

Laravel은 강력한 날짜 및 시간 조작 라이브러리인 [Carbon](https://carbon.nesbot.com/docs/)을 포함하고 있습니다. 새로운 `Carbon` 인스턴스를 생성하려면 `now` 함수를 사용할 수 있으며, Laravel 내에서 전역적으로 사용 가능합니다.

```php
$now = now();
```

혹은 다음과 같이 `Illuminate\Support\Carbon` 클래스를 사용할 수도 있습니다.

```php
use Illuminate\Support\Carbon;

$now = Carbon::now();
```

Carbon의 다양한 기능에 대한 자세한 설명은 [공식 Carbon 문서](https://carbon.nesbot.com/docs/)를 참조하세요.

---

<a name="deferred-functions"></a>
### 지연 함수(Deferred Functions)

> [!WARNING]
> 지연 함수 기능은 현재 베타로, 커뮤니티 피드백을 받고 있습니다.

Laravel의 [큐 작업](/docs/{{version}}/queues)은 백그라운드에서 작업을 처리할 수 있게 해주지만, 단순한 작업을 큐 워커를 구성하지 않고도 지연시키고 싶을 때가 있습니다.

지연 함수는 HTTP 응답이 사용자에게 전달된 후 클로저 실행을 연기할 수 있게 해, 애플리케이션의 속도와 반응성을 높여줍니다. 다음과 같이 사용합니다.

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

기본적으로, 지연 함수는 해당 HTTP 응답, Artisan 명령어, 큐 작업이 정상적으로 완료된 경우에만 실행됩니다. 4xx나 5xx 응답일 경우 실행되지 않습니다. 항상 실행되기를 원한다면 `always` 체이닝을 사용하세요.

```php
defer(fn () => Metrics::reportOrder($order))->always();
```

#### 지연 함수 취소

지연 함수 실행 전에 취소가 필요하다면, 함수의 이름을 지정한 후 `forget` 메서드를 이용해 취소할 수 있습니다.

```php
defer(fn () => Metrics::report(), 'reportMetrics');

defer()->forget('reportMetrics');
```

#### 지연 함수 호환성

Laravel 10.x에서 11.x로 업그레이드 하였고, `app/Http/Kernel.php` 파일이 남아 있다면, `$middleware` 속성의 맨 앞에 `InvokeDeferredCallbacks` 미들웨어를 추가해야 합니다.

```php
protected $middleware = [
    \Illuminate\Foundation\Http\Middleware\InvokeDeferredCallbacks::class, // [tl! add]
    \App\Http\Middleware\TrustProxies::class,
    // ...
];
```

#### 테스트에서 지연 함수 비활성화

테스트 작성 시에는 지연 함수를 즉시 실행하도록 비활성화해야 할 수 있습니다. 테스트 내에서 `withoutDefer`를 호출하세요.

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

전체 테스트 케이스에서 비활성화하려면 base `TestCase`의 `setUp` 메서드에서 호출하세요.

```php
abstract class TestCase extends BaseTestCase
{
    protected function setUp(): void
    {
        parent::setUp();

        $this->withoutDefer();
    }
}
```

---

<a name="lottery"></a>
### 로터리(Lottery)

Laravel의 로터리 클래스는 지정한 확률에 따라 콜백을 실행할 수 있습니다. 예를 들어 전체 요청의 일정 퍼센트에만 코드를 실행하고 싶을 때 유용합니다.

```php
use Illuminate\Support\Lottery;

Lottery::odds(1, 20)
    ->winner(fn () => $user->won())
    ->loser(fn () => $user->lost())
    ->choose();
```

다른 Laravel 기능과도 조합이 가능합니다. 예를 들어, 느린 쿼리 일부만 보고하게 하고 싶다면 다음과 같이 사용할 수 있습니다.

```php
use Carbon\CarbonInterval;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Lottery;

DB::whenQueryingForLongerThan(
    CarbonInterval::seconds(2),
    Lottery::odds(1, 100)->winner(fn () => report('Querying > 2 seconds.')),
);
```

#### 로터리 테스트

Laravel은 로터리 테스트를 쉽게 할 수 있는 메서드도 제공합니다.

```php
Lottery::alwaysWin();    // 항상 당첨
Lottery::alwaysLose();   // 항상 낙첨
Lottery::fix([true, false]); // 순서대로 당첨, 낙첨, 이후 정상 작동
Lottery::determineResultsNormally(); // 원래대로
```

---

<a name="pipeline"></a>
### 파이프라인(Pipeline)

Laravel의 `Pipeline` 파사드는 주어진 입력값을 일련의 인보커블 클래스, 클로저, 혹은 콜러블을 거치게 하여 각 단계에서 입력값을 검사, 수정할 수 있게 합니다. 각 단계는 `$next` 클로저를 호출하여 다음 단계를 실행합니다.

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

클로저 대신 인보커블 클래스도 사용 가능하며, 클래스명으로 지정하면 서비스 컨테이너를 통해 인스턴스화되어 의존성 주입이 가능합니다.

```php
$user = Pipeline::send($user)
    ->through([
        GenerateProfilePhoto::class,
        ActivateSubscription::class,
        SendWelcomeEmail::class,
    ])
    ->then(fn (User $user) => $user);
```

---

<a name="sleep"></a>
### 슬립(Sleep)

Laravel의 `Sleep` 클래스는 PHP의 기본 `sleep` 및 `usleep` 함수에 경량 래퍼를 제공하여, 테스트가 용이하고 개발자 친화적 API를 제공합니다.

```php
use Illuminate\Support\Sleep;

$waiting = true;

while ($waiting) {
    Sleep::for(1)->second();
    $waiting = /* ... */;
}
```

다양한 단위로 사용할 수 있으며, 여러 단위를 `and`로 결합할 수도 있습니다.

```php
Sleep::for(1)->second()->and(10)->milliseconds();
```

#### 슬립 테스트하기

`sleep` 함수가 포함된 코드를 테스트할 때, 실제로 테스트가 느려지는 문제를 해결하기 위해 `Sleep::fake()`로 페이크 처리할 수 있습니다.

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

실행 중 페이크 슬립이 발생할 때마다 콜백을 실행하려면 `whenFakingSleep`을 사용하세요.

```php
use Carbon\CarbonInterval as Duration;

$this->freezeTime();

Sleep::fake();

Sleep::whenFakingSleep(function (Duration $duration) {
    $this->travel($duration->totalMilliseconds)->milliseconds();
});
```

시간 동기화가 필요하다면 `syncWithCarbon` 옵션을 활용하세요.

```php
Sleep::fake(syncWithCarbon: true);

$start = now();

Sleep::for(1)->second();

$start->diffForHumans(); // 1초 전
```

---

<a name="timebox"></a>
### 타임박스(Timebox)

Laravel의 `Timebox` 클래스는 주어진 콜백이 항상 고정된 시간 동안 실행되게 보장합니다. 실제 실행이 더 짧게 끝나도, 최소 지정 시간만큼 대기합니다. 이는 암호화 연산이나 사용자 인증 검사 등 실행 시간의 차이로 정보가 유출되지 않게 할 때 유용합니다.

실행이 기준 시간을 초과하면 제한이 적용되지 않습니다. 즉, 최장 시간에 알맞은 기준값을 개발자가 선정해야 합니다.

```php
use Illuminate\Support\Timebox;

(new Timebox)->call(function ($timebox) {
    // ...
}, microseconds: 10000);
```

콜백 내에서 예외가 발생하더라도 지연을 지킨 후 예외를 다시 던집니다.

---

번역본이 너무 길어 하나의 답변에 모두 담을 수 없으므로, 원하시는 영역(예: "배열과 객체 편 전체" 등)을 말씀해주시면 지속적으로 구체적인 예제 및 설명을 번역해드릴 수 있습니다.  
코드 블록, 마크다운, URL, HTML 등은 원문 그대로 유지하며, 전문 용어와 형식에 주의해 번역합니다.