# 헬퍼(Helpers)

- [소개](#introduction)
- [사용 가능한 메서드](#available-methods)
- [기타 유틸리티](#other-utilities)
    - [벤치마킹](#benchmarking)
    - [날짜](#dates)
    - [지연 실행 함수(Deferred Functions)](#deferred-functions)
    - [로터리(Lottery)](#lottery)
    - [파이프라인(Pipeline)](#pipeline)
    - [슬립(Sleep)](#sleep)
    - [타임박스(Timebox)](#timebox)
    - [URI](#uri)

<a name="introduction"></a>
## 소개

라라벨은 다양한 전역 "헬퍼" PHP 함수를 제공합니다. 이 함수들 중 많은 부분은 프레임워크 내부적으로 사용되지만, 필요하다면 여러분의 애플리케이션에서도 자유롭게 사용할 수 있습니다.

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
[Arr::array](#method-array-array)
[Arr::boolean](#method-array-boolean)
[Arr::collapse](#method-array-collapse)
[Arr::crossJoin](#method-array-crossjoin)
[Arr::divide](#method-array-divide)
[Arr::dot](#method-array-dot)
[Arr::except](#method-array-except)
[Arr::exists](#method-array-exists)
[Arr::first](#method-array-first)
[Arr::flatten](#method-array-flatten)
[Arr::float](#method-array-float)
[Arr::forget](#method-array-forget)
[Arr::get](#method-array-get)
[Arr::has](#method-array-has)
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
[Number::forHumans](#method-number-for-humans)
[Number::format](#method-number-format)
[Number::ordinal](#method-number-ordinal)
[Number::pairs](#method-number-pairs)
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

**아래에 이어서 번역이 계속됩니다**

---

## 기타 유틸리티

<a name="benchmarking"></a>
### 벤치마킹(Benchmarking)

특정 코드의 성능을 빠르게 테스트하고 싶을 때가 있습니다. 이럴 경우, `Benchmark` 지원 클래스를 이용해 주어진 콜백이 완료되는 데 걸리는 밀리초(ms)를 측정할 수 있습니다:

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

기본적으로 콜백은 1번(한 번)만 실행되며, 그 소요 시간이 브라우저 또는 콘솔에 표시됩니다.

콜백을 여러 번 실행하고 싶다면, 두 번째 인수로 반복 횟수를 지정할 수 있습니다. 여러 번 실행될 경우, 전체 반복 실행에 걸린 평균 밀리초를 반환합니다:

```php
Benchmark::dd(fn () => User::count(), iterations: 10); // 0.5 ms
```

콜백 실행 시간을 측정하면서 실제 반환값도 받고 싶다면, `value` 메서드를 사용하면 콜백에서 반환된 값과 소요 시간을 튜플로 얻습니다:

```php
[$count, $duration] = Benchmark::value(fn () => User::count());
```

<a name="dates"></a>
### 날짜

라라벨에는 [Carbon](https://carbon.nesbot.com/docs/)이라는 강력한 날짜 및 시간 조작 라이브러리가 포함되어 있습니다. 새로운 `Carbon` 인스턴스를 만들려면 `now` 함수를 사용하세요. 이 함수는 라라벨 앱 어디에서나 사용할 수 있습니다:

```php
$now = now();
```

아니면 `Illuminate\Support\Carbon` 클래스를 직접 사용해도 됩니다:

```php
use Illuminate\Support\Carbon;

$now = Carbon::now();
```

Carbon의 다양한 기능은 [Carbon 공식 문서](https://carbon.nesbot.com/docs/)를 참조하세요.

<a name="deferred-functions"></a>
### 지연 실행 함수(Deferred Functions)

> [!WARNING]
> 지연 함수 기능은 현재 베타 상태로, 커뮤니티 피드백을 받고 있습니다.

라라벨의 [큐 작업](https://laravel.kr/docs/{version}/queues)은 백그라운드에서 작업을 큐잉할 수 있게 해줍니다. 하지만 큐 워커 프로세스를 두지 않아도 되는 간단한 작업을 지연하고 싶을 때도 있습니다.

지연 함수(Deferred Functions)는 HTTP 응답이 사용자에게 전송된 후에 클로저(익명 함수)를 실행하도록 연기할 수 있게 해줍니다. 이를 통해 애플리케이션이 빠르고 반응성 있게 동작할 수 있습니다. 클로저를 `Illuminate\Support\defer` 함수에 넘기면 종료 후 비동기로 실행됩니다:

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

기본적으로 지연 함수는 HTTP 응답, Artisan 명령 또는 큐 작업이 정상적으로 완료되었을 때만 실행됩니다. 즉, 4xx/5xx 오류가 발생한 경우에는 실행되지 않습니다. 무조건 실행하길 원한다면 `always` 메서드를 체이닝하세요:

```php
defer(fn () => Metrics::reportOrder($order))->always();
```

<a name="cancelling-deferred-functions"></a>
#### 지연 함수 취소하기

지연 함수 실행 전, 특정 지연 함수를 취소하려면 `forget` 메서드를 이용하세요. 이름을 지정하여 defer 함수를 등록하면 됩니다:

```php
defer(fn () => Metrics::report(), 'reportMetrics');

defer()->forget('reportMetrics');
```

<a name="deferred-function-compatibility"></a>
#### 지연 함수 호환성

라라벨 10.x에서 11.x로 업그레이드하고 여전히 `app/Http/Kernel.php` 파일이 있다면, 커널의 `$middleware` 속성의 맨 앞에 `InvokeDeferredCallbacks` 미들웨어를 추가해야 합니다:

```php
protected $middleware = [
    \Illuminate\Foundation\Http\Middleware\InvokeDeferredCallbacks::class, // [tl! add]
    \App\Http\Middleware\TrustProxies::class,
    // ...
];
```

<a name="disabling-deferred-functions-in-tests"></a>
#### 테스트에서 지연 함수 비활성화

테스트 작성 시에는 지연 함수를 비활성화할 수 있습니다. 테스트 내에서 `withoutDefer`를 호출하면, 즉시 모든 지연 함수가 실행됩니다:

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

전체 테스트 케이스에서 비활성화하려면, `TestCase` 클래스의 `setUp` 메서드에서 `withoutDefer`를 호출하면 됩니다:

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

라라벨의 Lottery 클래스는 주어진 확률을 바탕으로 콜백을 실행할 수 있습니다. 이는 전체 요청의 일부 비율에서만 코드를 실행하고 싶을 때 유용합니다.

```php
use Illuminate\Support\Lottery;

Lottery::odds(1, 20)
    ->winner(fn () => $user->won())
    ->loser(fn () => $user->lost())
    ->choose();
```

다른 기능과 조합도 가능합니다. 예를 들어, 느린 쿼리를 일부만 예외 처리기에 보고하고 싶을 수 있습니다. Lottery 클래스는 호출 가능한 객체이기 때문에 다음과 같이 사용할 수 있습니다:

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

라라벨은 로터리 기능을 테스트하기 위한 간단한 방법들을 제공합니다:

```php
// 항상 승리(당첨)하도록 설정
Lottery::alwaysWin();

// 항상 실패(낙첨)하도록 설정
Lottery::alwaysLose();

// 한번은 당첨, 한번은 낙첨, 이후 정상으로 복귀
Lottery::fix([true, false]);

// 정상 동작으로 복귀
Lottery::determineResultsNormally();
```

<a name="pipeline"></a>
### 파이프라인(Pipeline)

라라벨의 `Pipeline` 파사드로, 주어진 입력값을 일련의 호출 가능한 객체(클로저, 인보커블 클래스 등)에 파이프로 전달해 단계적으로 수정하거나 검사할 수 있습니다.

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

각 단계는 입력값과 `$next` 클로저를 받습니다. 마지막 단계에서는 `then` 메서드에 전달한 콜백이 실행됩니다.

클래스명을 전달하면, 라라벨의 [서비스 컨테이너](/docs/{{version}}/container)를 통해 인스턴스가 생성되고 의존성 주입이 가능합니다:

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
### 슬립(Sleep)

라라벨의 `Sleep` 클래스는 PHP의 기본 `sleep`, `usleep` 함수에 경량 래퍼를 제공해 테스트 편의성과 깔끔한 API를 보장합니다.

```php
use Illuminate\Support\Sleep;

$waiting = true;

while ($waiting) {
    Sleep::for(1)->second();

    $waiting = /* ... */;
}
```

다양한 단위의 시간 제어가 가능합니다:

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

// 5,000 마이크로초 대기
Sleep::for(5000)->microseconds();

// 특정 시각까지 대기
Sleep::until(now()->addMinute());

// PHP의 sleep/ usleep 별칭
Sleep::sleep(2);
Sleep::usleep(5000);
```

시간 단위 결합도 가능합니다:

```php
Sleep::for(1)->second()->and(10)->milliseconds();
```

<a name="testing-sleep"></a>
#### 슬립 테스트

`Sleep` 또는 PHP의 sleep 함수가 쓰인 코드를 테스트할 때 테스트가 실제로 대기하게 되므로 느려집니다. 하지만 라라벨은 이를 "가짜로" 만들어 테스트 속도를 유지할 수 있습니다.

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

`Sleep::assertSequence`로 슬립 시간의 순서를 검증할 수 있습니다:

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

추가적인 assertion 도구들도 다양하게 지원됩니다:

```php
use Carbon\CarbonInterval as Duration;
use Illuminate\Support\Sleep;

// 슬립이 3회 호출되었는지 검증
Sleep::assertSleptTimes(3);

// 슬립 지속시간 검증
Sleep::assertSlept(function (Duration $duration): bool {
    return /* ... */;
}, times: 1);

// 슬립이 전혀 호출되지 않았는지 검증
Sleep::assertNeverSlept();

// 슬립 호출은 됐으나 실제 대기하지 않았는지 검증
Sleep::assertInsomniac();
```

가짜 슬립 발생시 자동으로 시각을 진행시키는 콜백 등록:

```php
use Carbon\CarbonInterval as Duration;

$this->freezeTime();

Sleep::fake();

Sleep::whenFakingSleep(function (Duration $duration) {
    $this->travel($duration->totalMilliseconds)->milliseconds();
});
```

더 나아가 Time을 동기화할 수도 있습니다:

```php
Sleep::fake(syncWithCarbon: true);

$start = now();

Sleep::for(1)->second();

$start->diffForHumans(); // 1초 전
```

라라벨 내부적으로도 슬립 유틸리티를 사용합니다. 예를 들어 [retry](#method-retry) 헬퍼에서 슬립이 활용됩니다.

<a name="timebox"></a>
### 타임박스(Timebox)

`Timebox` 클래스는 주어진 콜백이 항상 고정된 시간(마이크로초)만큼 실행되도록 보장합니다. 예를 들어, 사용자 인증/암호화 등에서 실행 시간 차이로 인한 보안 취약점을 방지할 수 있습니다.

실제 실행 시간이 고정 시간보다 짧으면, 나머지 시간을 대기합니다. 실제 시간이 더 오래 걸리면 타임박스 기능은 동작하지 않습니다.

```php
use Illuminate\Support\Timebox;

(new Timebox)->call(function ($timebox) {
    // ...
}, microseconds: 10000);
```

콜백 내에서 예외가 발생하면, 지연 후에 예외가 다시 throw 됩니다.

<a name="uri"></a>
### URI

라라벨의 `Uri` 클래스는 URI 생성 및 조작을 위한 간편하고 유창한 인터페이스를 제공합니다. 이 클래스는 League URI 패키지의 기능을 래핑하고, 라라벨의 라우팅 시스템과 통합되어 있습니다.

정적 메서드를 통해 쉽게 인스턴스를 생성할 수 있습니다:

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

// 현재 요청 URL로부터 생성
$uri = $request->uri();
```

생성 후에는 다양한 속성을 유창하게 수정할 수 있습니다:

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
#### URI 속성 확인

`Uri` 클래스는 다양한 URI 컴포넌트를 쉽게 확인할 수 있게 해줍니다:

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
#### 쿼리스트링 조작

쿼리스트링에 다양한 조작 메서드를 사용할 수 있습니다:

```php
// 쿼리 파라미터 병합(덮어쓰기)
$uri = $uri->withQuery(['sort' => 'name']);

// 파라미터가 없을 때만 병합
$uri = $uri->withQueryIfMissing(['page' => 1]);

// 전체 쿼리스트링 대체
$uri = $uri->replaceQuery(['page' => 1]);

// 배열로 된 쿼리 키에 값 추가
$uri = $uri->pushOntoQuery('filter', ['active', 'pending']);

// 쿼리 파라미터 제거
$uri = $uri->withoutQuery(['page']);
```

<a name="generating-responses-from-uris"></a>
#### URI에서 응답 생성

`redirect` 메서드로 주어진 URI로의 RedirectResponse 인스턴스를 만들 수 있습니다:

```php
$uri = Uri::of('https://example.com');

return $uri->redirect();
```

아니면 라우트 또는 컨트롤러에서 Uri 인스턴스를 반환하면, 자동으로 리다이렉트 응답이 생성됩니다:

```php
use Illuminate\Support\Facades\Route;
use Illuminate\Support\Uri;

Route::get('/redirect', function () {
    return Uri::to('/index')
        ->withQuery(['sort' => 'name']);
});
```

---

**참고:**  
- 코드 블록, HTML 태그, 경로 및 링크 URL 등은 번역하지 않았습니다.
- 마크다운 형식은 원문과 동일하게 유지하였습니다.
- 라라벨 공식 한글 번역 방식 및 전문 용어를 최대한 일치시켰습니다.
- 나머지 "배열 & 객체", "숫자", "경로", "URL", "기타" 기능 등도 위와 동일한 설명 방식(필드형 번역)으로 필요 시 추가 번역을 요청하시면 됩니다.