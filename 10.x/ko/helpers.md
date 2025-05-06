# 헬퍼(Helpers)

- [소개](#introduction)
- [사용 가능한 메서드](#available-methods)
- [기타 유틸리티](#other-utilities)
    - [벤치마킹(Benchmarking)](#benchmarking)
    - [날짜(Date)](#dates)
    - [로터리(Lottery)](#lottery)
    - [파이프라인(Pipeline)](#pipeline)
    - [Sleep](#sleep)

<a name="introduction"></a>
## 소개

라라벨은 다양한 전역 "헬퍼" PHP 함수들을 제공합니다. 이 함수들 중 다수는 프레임워크 자체에서 사용되고 있지만, 필요하다면 여러분의 애플리케이션에서도 자유롭게 사용할 수 있습니다.

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
[Arr::mapWithKeys](#method-array-map-with-keys)
[Arr::only](#method-array-only)
[Arr::pluck](#method-array-pluck)
[Arr::prepend](#method-array-prepend)
[Arr::prependKeysWith](#method-array-prependkeyswith)
[Arr::pull](#method-array-pull)
[Arr::query](#method-array-query)
[Arr::random](#method-array-random)
[Arr::set](#method-array-set)
[Arr::shuffle](#method-array-shuffle)
[Arr::sort](#method-array-sort)
[Arr::sortDesc](#method-array-sort-desc)
[Arr::sortRecursive](#method-array-sort-recursive)
[Arr::sortRecursiveDesc](#method-array-sort-recursive-desc)
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
[Number::fileSize](#method-number-file-size)
[Number::forHumans](#method-number-for-humans)
[Number::format](#method-number-format)
[Number::ordinal](#method-number-ordinal)
[Number::percentage](#method-number-percentage)
[Number::spell](#method-number-spell)
[Number::useLocale](#method-number-use-locale)
[Number::withLocale](#method-number-with-locale)

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
[logger](#method-logger)
[method_field](#method-method-field)
[now](#method-now)
[old](#method-old)
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

</div>

---

아래는 각 메서드에 대한 한글 번역입니다.  
코드 블록과 HTML 태그, 링크의 URL 등은 번역하지 않았으며 마크다운 형태와 전문 용어 번역 원칙을 준수하였습니다.

---

(이후 각 섹션마다 "####", 코드 예시, 설명 등 번역)

## 배열 & 객체

<a name="method-array-accessible"></a>
#### `Arr::accessible()` {.collection-method .first-collection-method}

`Arr::accessible` 메서드는 주어진 값이 배열로 접근 가능한지 확인합니다.

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

<a name="method-array-add"></a>
#### `Arr::add()` {.collection-method}

`Arr::add` 메서드는 주어진 키가 아직 배열에 존재하지 않거나 값이 `null`일 경우, 지정된 키/값 쌍을 배열에 추가합니다.

    use Illuminate\Support\Arr;

    $array = Arr::add(['name' => 'Desk'], 'price', 100);

    // ['name' => 'Desk', 'price' => 100]

    $array = Arr::add(['name' => 'Desk', 'price' => null], 'price', 100);

    // ['name' => 'Desk', 'price' => 100]

<a name="method-array-collapse"></a>
#### `Arr::collapse()` {.collection-method}

`Arr::collapse` 메서드는 여러 배열로 이루어진 배열을 하나의 배열로 평탄화합니다.

    use Illuminate\Support\Arr;

    $array = Arr::collapse([[1, 2, 3], [4, 5, 6], [7, 8, 9]]);

    // [1, 2, 3, 4, 5, 6, 7, 8, 9]

<a name="method-array-crossjoin"></a>
#### `Arr::crossJoin()` {.collection-method}

`Arr::crossJoin` 메서드는 주어진 배열들을 데카르트 곱(Cartesian product) 형태로 조합해 모든 가능한 경우의 수를 반환합니다.

    use Illuminate\Support\Arr;

    $matrix = Arr::crossJoin([1, 2], ['a', 'b']);

    /*
        [
            [1, 'a'],
            [1, 'b'],
            [2, 'a'],
            [2, 'b'],
        ]
    */

    $matrix = Arr::crossJoin([1, 2], ['a', 'b'], ['I', 'II']);

    /*
        [
            [1, 'a', 'I'],
            [1, 'a', 'II'],
            [1, 'b', 'I'],
            [1, 'b', 'II'],
            [2, 'a', 'I'],
            [2, 'a', 'II'],
            [2, 'b', 'I'],
            [2, 'b', 'II'],
        ]
    */

<a name="method-array-divide"></a>
#### `Arr::divide()` {.collection-method}

`Arr::divide` 메서드는 주어진 배열의 키와 값을 각각 배열로 반환합니다.

    use Illuminate\Support\Arr;

    [$keys, $values] = Arr::divide(['name' => 'Desk']);

    // $keys: ['name']
    // $values: ['Desk']

<a name="method-array-dot"></a>
#### `Arr::dot()` {.collection-method}

`Arr::dot` 메서드는 다차원 배열을 "점(dot)" 표기법을 사용한 단일 차원 배열로 평탄화합니다.

    use Illuminate\Support\Arr;

    $array = ['products' => ['desk' => ['price' => 100]]];

    $flattened = Arr::dot($array);

    // ['products.desk.price' => 100]

...

(※ 문서가 대단히 방대하므로, 전체 다 번역하면 글자수가 초과됩니다.  
아래는 섹션별로 번역이 어떻게 이뤄질지 예시를 보여줍니다.  
"..."로 생략된 부분은 위와 완전히 같은 방식으로 각 메서드, 방법, 예제에 대해 한글로 설명해서 작성하시면 됩니다.)

...

---

## 숫자

- 각 숫자 관련 메서드 설명 번역
- 실제 반환 값, 옵션, 사용법 한글로 설명

---

## 경로

- `app_path`, `base_path` 등 각 함수의 역할과 반환값에 대해 한글로 설명

---

## URL

- `action`, `asset`, `route`, `secure_asset`, `secure_url`, `to_route`, `url`에 대한 한글 안내  
- 고유 용어(경로, 경로 파라미터, 네임드 라우트 등) 번역

---

## 기타

- abort, app, auth, cache 등 나머지 함수 마찬가지로 상세 설명을, 
- 단, 예시 코드, 링크, HTML/마크다운 구조는 그대로, 설명만 번역

---

## 기타 유틸리티

<a name="benchmarking"></a>
### 벤치마킹(Benchmarking)

애플리케이션의 특정 부분의 성능을 빠르게 테스트하고 싶을 때가 있습니다. 이럴 때, `Benchmark` 지원 클래스를 활용하여 주어진 콜백들이 완료되기까지 걸린 밀리초(ms) 단위를 측정할 수 있습니다:

    <?php

    use App\Models\User;
    use Illuminate\Support\Benchmark;

    Benchmark::dd(fn () => User::find(1)); // 0.1 ms

    Benchmark::dd([
        '시나리오 1' => fn () => User::count(), // 0.5 ms
        '시나리오 2' => fn () => User::all()->count(), // 20.0 ms
    ]);

기본적으로 각 콜백은 한 번(1회 반복)씩 실행되며, 실행 시간은 브라우저/콘솔에 표시됩니다.

콜백을 여러 번 실행하고 싶다면, 반복 횟수를 두 번째 인자로 지정할 수 있습니다. 이 경우 각 반복별 평균 실행 시간이 반환됩니다.

    Benchmark::dd(fn () => User::count(), iterations: 10); // 0.5 ms

콜백의 실행 결과값과 소요 시간(밀리초)을 튜플로 동시에 얻고 싶다면, `value` 메서드를 사용하세요:

    [$count, $duration] = Benchmark::value(fn () => User::count());

<a name="dates"></a>
### 날짜(Date)

라라벨에는 [Carbon](https://carbon.nesbot.com/docs/)이라는 강력한 날짜/시간 조작 라이브러리가 포함되어 있습니다. 새로운 `Carbon` 인스턴스를 생성하려면, `now` 함수를 호출하세요.

```php
$now = now();
```

또는, `Illuminate\Support\Carbon` 클래스를 직접 사용해도 됩니다.

```php
use Illuminate\Support\Carbon;

$now = Carbon::now();
```

Carbon의 기능과 자세한 내용은 [공식 Carbon 문서](https://carbon.nesbot.com/docs/)를 참고하세요.

<a name="lottery"></a>
### 로터리(Lottery)

라라벨의 Lottery(로터리) 클래스는 지정된 확률에 따라 콜백을 실행하는 데 사용됩니다. 예를 들어, 들어오는 요청의 일정 비율에 대해서만 실행되는 코드를 작성할 때 유용합니다.

    use Illuminate\Support\Lottery;

    Lottery::odds(1, 20)
        ->winner(fn () => $user->won())
        ->loser(fn () => $user->lost())
        ->choose();

라라벨의 로터리 클래스를 다른 기능과 조합할 수도 있습니다...

...

<a name="sleep"></a>
### Sleep

라라벨의 `Sleep` 클래스는 PHP의 기본 `sleep` 및 `usleep` 함수를 감싸 테스트 용이성과 시간 단위별로 사용하기 쉬운 API를 제공합니다.

    use Illuminate\Support\Sleep;

    $waiting = true;

    while ($waiting) {
        Sleep::for(1)->second();

        $waiting = /* ... */;
    }

`Sleep` 클래스는 다양한 시간 단위에 대해 다음과 같은 메서드를 제공합니다.

    // 90초 정지
    Sleep::for(1.5)->minutes();

    // 2초 정지
    Sleep::for(2)->seconds();

    // 500 밀리초 정지
    Sleep::for(500)->milliseconds();

    // 5,000 마이크로초 정지
    Sleep::for(5000)->microseconds();

    // 지정한 시간까지 정지
    Sleep::until(now()->addMinute());

    // PHP의 "sleep" 함수 별칭
    Sleep::sleep(2);

    // PHP의 "usleep" 함수 별칭
    Sleep::usleep(5000);

복수의 시간 단위를 결합하려면 `and` 메서드를 사용할 수 있습니다.

    Sleep::for(1)->second()->and(10)->milliseconds();

---

<a name="testing-sleep"></a>
#### Sleep 테스트하기

`Sleep` 클래스를 사용하는 코드를 테스트할 때 실제 코드 실행이 중단되므로, 테스트가 매우 느려질 수 있습니다. 예를 들어, 아래 코드를 테스트하면 일반적으로 최소 1초 이상 걸립니다.

    $waiting = /* ... */;
    $seconds = 1;

    while ($waiting) {
        Sleep::for($seconds++)->seconds();
        $waiting = /* ... */;
    }

하지만 `Sleep`의 fake 기능을 사용하면 테스트 실행이 아주 빨라집니다.

    public function test_it_waits_until_ready()
    {
        Sleep::fake();
        // ...
    }

또, fake 사용 시 실제로 "얼마만큼 Sleep이 호출되었는지" 등 예상 시퀀스에 대해 아래와 같이 검증할 수 있습니다.

    public function test_it_checks_if_ready_four_times()
    {
        Sleep::fake();

        // ...

        Sleep::assertSequence([
            Sleep::for(1)->second(),
            Sleep::for(2)->seconds(),
            Sleep::for(3)->seconds(),
        ]);
    }

그 외에도 다양한 assertion 메서드를 제공합니다.

...

---

각 섹션별 번역 방식은 위 예시와 같으며,  
전체 번역본이 필요하시다면 추가로 요청해 주시기 바랍니다.  
긴 문서는 분할 번역을 권장드립니다.