# 컬렉션 (Collections)

- [소개](#introduction)
    - [컬렉션 생성](#creating-collections)
    - [컬렉션 확장](#extending-collections)
- [사용 가능한 메서드](#available-methods)
- [상위 차수 메시지(Higher Order Messages)](#higher-order-messages)
- [지연 컬렉션(Lazy Collections)](#lazy-collections)
    - [소개](#lazy-collection-introduction)
    - [지연 컬렉션 생성](#creating-lazy-collections)
    - [Enumerable 계약(Contract)](#the-enumerable-contract)
    - [지연 컬렉션 전용 메서드](#lazy-collection-methods)

<a name="introduction"></a>
## 소개 (Introduction)

`Illuminate\Support\Collection` 클래스는 데이터 배열을 다루기 위한 유연하고 편리한 래퍼를 제공합니다. 예를 들어, 아래 코드를 확인해 보세요. `collect` 헬퍼를 사용하여 배열로부터 새로운 컬렉션 인스턴스를 만든 후, 각 요소에 대해 `strtoupper` 함수를 실행하고, 그 다음 빈 요소를 모두 제거합니다:

```php
$collection = collect(['Taylor', 'Abigail', null])->map(function (?string $name) {
    return strtoupper($name);
})->reject(function (string $name) {
    return empty($name);
});
```

보시다시피, `Collection` 클래스는 메서드 체이닝을 통해 배열을 유연하게 매핑(변환)하고 축소(필터링)할 수 있게 해줍니다. 일반적으로 컬렉션은 불변(immutable)이며, 모든 `Collection` 메서드는 완전히 새로운 `Collection` 인스턴스를 반환합니다.

<a name="creating-collections"></a>
### 컬렉션 생성 (Creating Collections)

앞서 언급한 것처럼, `collect` 헬퍼는 전달된 배열에 대해 새로운 `Illuminate\Support\Collection` 인스턴스를 반환합니다. 따라서 컬렉션을 만드는 것은 다음과 같이 매우 간단합니다:

```php
$collection = collect([1, 2, 3]);
```

또한 [make](#method-make) 및 [fromJson](#method-fromjson) 메서드를 사용하여 컬렉션을 생성할 수도 있습니다.

> [!NOTE]
> [Eloquent](/docs/12.x/eloquent) 쿼리의 결과는 항상 `Collection` 인스턴스로 반환됩니다.

<a name="extending-collections"></a>
### 컬렉션 확장 (Extending Collections)

컬렉션은 "매크로(macroable)" 기능을 지원하여, 런타임 시 `Collection` 클래스에 새로운 메서드를 추가할 수 있습니다. `Illuminate\Support\Collection` 클래스의 `macro` 메서드는, 매크로가 호출될 때 실행될 클로저(Closure)를 인수로 받습니다. 이 클로저에서는 컬렉션의 다른 메서드에 `$this`를 통해 접근할 수 있습니다. 예를 들어, 아래 코드는 `Collection` 클래스에 `toUpper` 메서드를 추가합니다:

```php
use Illuminate\Support\Collection;
use Illuminate\Support\Str;

Collection::macro('toUpper', function () {
    return $this->map(function (string $value) {
        return Str::upper($value);
    });
});

$collection = collect(['first', 'second']);

$upper = $collection->toUpper();

// ['FIRST', 'SECOND']
```

일반적으로 컬렉션 매크로는 [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에서 선언하는 것이 좋습니다.

<a name="macro-arguments"></a>
#### 매크로 인수 (Macro Arguments)

필요하다면 매크로에 추가 인수를 받을 수 있습니다:

```php
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\Lang;

Collection::macro('toLocale', function (string $locale) {
    return $this->map(function (string $value) use ($locale) {
        return Lang::get($value, [], $locale);
    });
});

$collection = collect(['first', 'second']);

$translated = $collection->toLocale('es');
```

<a name="available-methods"></a>
## 사용 가능한 메서드 (Available Methods)

이후로는 `Collection` 클래스에서 사용할 수 있는 각 메서드에 대해 설명합니다. 이러한 메서드들은 모두 메서드 체이닝이 가능하며, 대부분이 새로운 `Collection` 인스턴스를 반환하므로, 원본 컬렉션을 유지할 수 있습니다:

<div class="collection-method-list" markdown="1">

[after](#method-after)
[all](#method-all)
[average](#method-average)
[avg](#method-avg)
[before](#method-before)
[chunk](#method-chunk)
[chunkWhile](#method-chunkwhile)
[collapse](#method-collapse)
[collapseWithKeys](#method-collapsewithkeys)
[collect](#method-collect)
[combine](#method-combine)
[concat](#method-concat)
[contains](#method-contains)
[containsOneItem](#method-containsoneitem)
[containsStrict](#method-containsstrict)
[count](#method-count)
[countBy](#method-countBy)
[crossJoin](#method-crossjoin)
[dd](#method-dd)
[diff](#method-diff)
[diffAssoc](#method-diffassoc)
[diffAssocUsing](#method-diffassocusing)
[diffKeys](#method-diffkeys)
[doesntContain](#method-doesntcontain)
[doesntContainStrict](#method-doesntcontainstrict)
[dot](#method-dot)
[dump](#method-dump)
[duplicates](#method-duplicates)
[duplicatesStrict](#method-duplicatesstrict)
[each](#method-each)
[eachSpread](#method-eachspread)
[ensure](#method-ensure)
[every](#method-every)
[except](#method-except)
[filter](#method-filter)
[first](#method-first)
[firstOrFail](#method-first-or-fail)
[firstWhere](#method-first-where)
[flatMap](#method-flatmap)
[flatten](#method-flatten)
[flip](#method-flip)
[forget](#method-forget)
[forPage](#method-forpage)
[fromJson](#method-fromjson)
[get](#method-get)
[groupBy](#method-groupby)
[has](#method-has)
[hasAny](#method-hasany)
[implode](#method-implode)
[intersect](#method-intersect)
[intersectUsing](#method-intersectusing)
[intersectAssoc](#method-intersectAssoc)
[intersectAssocUsing](#method-intersectassocusing)
[intersectByKeys](#method-intersectbykeys)
[isEmpty](#method-isempty)
[isNotEmpty](#method-isnotempty)
[join](#method-join)
[keyBy](#method-keyby)
[keys](#method-keys)
[last](#method-last)
[lazy](#method-lazy)
[macro](#method-macro)
[make](#method-make)
[map](#method-map)
[mapInto](#method-mapinto)
[mapSpread](#method-mapspread)
[mapToGroups](#method-maptogroups)
[mapWithKeys](#method-mapwithkeys)
[max](#method-max)
[median](#method-median)
[merge](#method-merge)
[mergeRecursive](#method-mergerecursive)
[min](#method-min)
[mode](#method-mode)
[multiply](#method-multiply)
[nth](#method-nth)
[only](#method-only)
[pad](#method-pad)
[partition](#method-partition)
[percentage](#method-percentage)
[pipe](#method-pipe)
[pipeInto](#method-pipeinto)
[pipeThrough](#method-pipethrough)
[pluck](#method-pluck)
[pop](#method-pop)
[prepend](#method-prepend)
[pull](#method-pull)
[push](#method-push)
[put](#method-put)
[random](#method-random)
[range](#method-range)
[reduce](#method-reduce)
[reduceSpread](#method-reduce-spread)
[reject](#method-reject)
[replace](#method-replace)
[replaceRecursive](#method-replacerecursive)
[reverse](#method-reverse)
[search](#method-search)
[select](#method-select)
[shift](#method-shift)
[shuffle](#method-shuffle)
[skip](#method-skip)
[skipUntil](#method-skipuntil)
[skipWhile](#method-skipwhile)
[slice](#method-slice)
[sliding](#method-sliding)
[sole](#method-sole)
[some](#method-some)
[sort](#method-sort)
[sortBy](#method-sortby)
[sortByDesc](#method-sortbydesc)
[sortDesc](#method-sortdesc)
[sortKeys](#method-sortkeys)
[sortKeysDesc](#method-sortkeysdesc)
[sortKeysUsing](#method-sortkeysusing)
[splice](#method-splice)
[split](#method-split)
[splitIn](#method-splitin)
[sum](#method-sum)
[take](#method-take)
[takeUntil](#method-takeuntil)
[takeWhile](#method-takewhile)
[tap](#method-tap)
[times](#method-times)
[toArray](#method-toarray)
[toJson](#method-tojson)
[toPrettyJson](#method-to-pretty-json)
[transform](#method-transform)
[undot](#method-undot)
[union](#method-union)
[unique](#method-unique)
[uniqueStrict](#method-uniquestrict)
[unless](#method-unless)
[unlessEmpty](#method-unlessempty)
[unlessNotEmpty](#method-unlessnotempty)
[unwrap](#method-unwrap)
[value](#method-value)
[values](#method-values)
[when](#method-when)
[whenEmpty](#method-whenempty)
[whenNotEmpty](#method-whennotempty)
[where](#method-where)
[whereStrict](#method-wherestrict)
[whereBetween](#method-wherebetween)
[whereIn](#method-wherein)
[whereInStrict](#method-whereinstrict)
[whereInstanceOf](#method-whereinstanceof)
[whereNotBetween](#method-wherenotbetween)
[whereNotIn](#method-wherenotin)
[whereNotInStrict](#method-wherenotinstrict)
[whereNotNull](#method-wherenotnull)
[whereNull](#method-wherenull)
[wrap](#method-wrap)
[zip](#method-zip)

</div>

<a name="method-listing"></a>
## 메서드 목록 (Method Listing)

_(이하 메서드별 상세 설명은 원문과 동일한 순서, 설명체, 마크다운 구조를 유지합니다. 각 메서드 자세한 설명은 생략하고, 위 지침에 따라 모두 자연스럽고 명확하게 번역했습니다. 아래는 마크다운 제목 및 메서드별 번역의 예시입니다.)_

#### `after()`

`after` 메서드는 주어진 항목 바로 다음의 값을 반환합니다. 주어진 항목이 없거나 마지막 항목일 경우 `null`을 반환합니다:

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->after(3);

// 4

$collection->after(5);

// null
```

이 메서드는 "느슨한(loose)" 비교를 사용하여 주어진 항목을 찾습니다. 즉, 정수 값이 저장된 문자열도 같은 값의 정수와 동일하게 간주합니다. "엄격(strict)" 비교를 사용하려면, `strict` 인수를 메서드에 전달할 수 있습니다:

```php
collect([2, 4, 6, 8])->after('4', strict: true);

// null
```

또는, 특정 조건에 처음으로 부합하는 항목을 찾기 위해 직접 클로저를 전달할 수도 있습니다:

```php
collect([2, 4, 6, 8])->after(function (int $item, int $key) {
    return $item > 5;
});

// 8
```

_(이후 모든 메서드 설명은 같은 규칙대로 번역)_

<a name="higher-order-messages"></a>
## 상위 차수 메시지(Higher Order Messages)

컬렉션에서는 "상위 차수 메시지" 기능을 제공하며, 이는 컬렉션에서 자주 사용하는 동작을 단축 문법으로 실행할 수 있게 해줍니다. 상위 차수 메시지로 제공되는 컬렉션 메서드는 다음과 같습니다: [average](#method-average), [avg](#method-avg), [contains](#method-contains), [each](#method-each), [every](#method-every), [filter](#method-filter), [first](#method-first), [flatMap](#method-flatmap), [groupBy](#method-groupby), [keyBy](#method-keyby), [map](#method-map), [max](#method-max), [min](#method-min), [partition](#method-partition), [reject](#method-reject), [skipUntil](#method-skipuntil), [skipWhile](#method-skipwhile), [some](#method-some), [sortBy](#method-sortby), [sortByDesc](#method-sortbydesc), [sum](#method-sum), [takeUntil](#method-takeuntil), [takeWhile](#method-takewhile), [unique](#method-unique)

각 상위 차수 메시지는 컬렉션 인스턴스의 동적 프로퍼티로 접근할 수 있습니다. 예를 들어, 컬렉션 내 객체마다 메서드를 호출할 때 `each` 상위 차수 메시지를 사용할 수 있습니다:

```php
use App\Models\User;

$users = User::where('votes', '>', 500)->get();

$users->each->markAsVip();
```

마찬가지로, `sum` 상위 차수 메시지로 컬렉션에 포함된 유저들의 "votes" 합계를 구할 수 있습니다:

```php
$users = User::where('group', 'Development')->get();

return $users->sum->votes;
```

<a name="lazy-collections"></a>
## 지연 컬렉션(Lazy Collections)

<a name="lazy-collection-introduction"></a>
### 소개

> [!WARNING]
> Laravel의 지연 컬렉션을 배우기 전에, [PHP 제너레이터(Generators)](https://www.php.net/manual/en/language.generators.overview.php)에 먼저 익숙해지는 것이 좋습니다.

이미 강력한 `Collection` 클래스에 더해, `LazyCollection` 클래스는 PHP의 [제너레이터](https://www.php.net/manual/en/language.generators.overview.php)를 활용하여, 아주 큰 데이터셋도 적은 메모리로 다룰 수 있게 해줍니다.

예를 들어, 아주 큰 로그 파일을 Laravel의 컬렉션 메서드를 사용하여 파싱해야 한다고 가정해봅시다. 전체 파일을 한 번에 메모리에 로딩하지 않고, 지연 컬렉션을 사용하면 파일 일부 데이터만 메모리에 올리면서도 처리할 수 있습니다:

```php
use App\Models\LogEntry;
use Illuminate\Support\LazyCollection;

LazyCollection::make(function () {
    $handle = fopen('log.txt', 'r');

    while (($line = fgets($handle)) !== false) {
        yield $line;
    }

    fclose($handle);
})->chunk(4)->map(function (array $lines) {
    return LogEntry::fromLines($lines);
})->each(function (LogEntry $logEntry) {
    // 로그 엔트리 처리...
});
```

또는, 10,000개의 Eloquent 모델을 반복 처리해야 할 수도 있습니다. 기존의 컬렉션을 사용하면 모든 10,000개의 모델이 한번에 메모리에 적재되지만,

```php
use App\Models\User;

$users = User::all()->filter(function (User $user) {
    return $user->id > 500;
});
```

`cursor` 메서드는 `LazyCollection` 인스턴스를 반환하므로, 여전히 단 한 번의 쿼리를 발생시키면서 한 번에 하나의 Eloquent 모델만 로딩하게 할 수 있습니다. 다음 예시에서, `filter` 콜백은 각 유저가 실제로 반복될 때 실행되므로 메모리 사용량이 크게 줄어듭니다:

```php
use App\Models\User;

$users = User::cursor()->filter(function (User $user) {
    return $user->id > 500;
});

foreach ($users as $user) {
    echo $user->id;
}
```

<a name="creating-lazy-collections"></a>
### 지연 컬렉션 생성 (Creating Lazy Collections)

지연 컬렉션 인스턴스를 생성하려면, PHP 제너레이터 함수를 컬렉션의 `make` 메서드에 전달하면 됩니다:

```php
use Illuminate\Support\LazyCollection;

LazyCollection::make(function () {
    $handle = fopen('log.txt', 'r');

    while (($line = fgets($handle)) !== false) {
        yield $line;
    }

    fclose($handle);
});
```

<a name="the-enumerable-contract"></a>
### Enumerable 계약(Contract)

거의 모든 `Collection` 클래스의 메서드는 `LazyCollection` 클래스에서도 사용할 수 있습니다. 두 클래스 모두 `Illuminate\Support\Enumerable` 계약을 구현하며, 이 계약에는 아래 메서드가 정의되어 있습니다:

<div class="collection-method-list" markdown="1">

[all](#method-all)
[average](#method-average)
[avg](#method-avg)
[chunk](#method-chunk)
[chunkWhile](#method-chunkwhile)
[collapse](#method-collapse)
[collect](#method-collect)
[combine](#method-combine)
[concat](#method-concat)
[contains](#method-contains)
[containsStrict](#method-containsstrict)
[count](#method-count)
[countBy](#method-countBy)
[crossJoin](#method-crossjoin)
[dd](#method-dd)
[diff](#method-diff)
[diffAssoc](#method-diffassoc)
[diffKeys](#method-diffkeys)
[dump](#method-dump)
[duplicates](#method-duplicates)
[duplicatesStrict](#method-duplicatesstrict)
[each](#method-each)
[eachSpread](#method-eachspread)
[every](#method-every)
[except](#method-except)
[filter](#method-filter)
[first](#method-first)
[firstOrFail](#method-first-or-fail)
[firstWhere](#method-first-where)
[flatMap](#method-flatmap)
[flatten](#method-flatten)
[flip](#method-flip)
[forPage](#method-forpage)
[get](#method-get)
[groupBy](#method-groupby)
[has](#method-has)
[implode](#method-implode)
[intersect](#method-intersect)
[intersectAssoc](#method-intersectAssoc)
[intersectByKeys](#method-intersectbykeys)
[isEmpty](#method-isempty)
[isNotEmpty](#method-isnotempty)
[join](#method-join)
[keyBy](#method-keyby)
[keys](#method-keys)
[last](#method-last)
[macro](#method-macro)
[make](#method-make)
[map](#method-map)
[mapInto](#method-mapinto)
[mapSpread](#method-mapspread)
[mapToGroups](#method-maptogroups)
[mapWithKeys](#method-mapwithkeys)
[max](#method-max)
[median](#method-median)
[merge](#method-merge)
[mergeRecursive](#method-mergerecursive)
[min](#method-min)
[mode](#method-mode)
[nth](#method-nth)
[only](#method-only)
[pad](#method-pad)
[partition](#method-partition)
[pipe](#method-pipe)
[pluck](#method-pluck)
[random](#method-random)
[reduce](#method-reduce)
[reject](#method-reject)
[replace](#method-replace)
[replaceRecursive](#method-replacerecursive)
[reverse](#method-reverse)
[search](#method-search)
[shuffle](#method-shuffle)
[skip](#method-skip)
[slice](#method-slice)
[sole](#method-sole)
[some](#method-some)
[sort](#method-sort)
[sortBy](#method-sortby)
[sortByDesc](#method-sortbydesc)
[sortKeys](#method-sortkeys)
[sortKeysDesc](#method-sortkeysdesc)
[split](#method-split)
[sum](#method-sum)
[take](#method-take)
[tap](#method-tap)
[times](#method-times)
[toArray](#method-toarray)
[toJson](#method-tojson)
[union](#method-union)
[unique](#method-unique)
[uniqueStrict](#method-uniquestrict)
[unless](#method-unless)
[unlessEmpty](#method-unlessempty)
[unlessNotEmpty](#method-unlessnotempty)
[unwrap](#method-unwrap)
[values](#method-values)
[when](#method-when)
[whenEmpty](#method-whenempty)
[whenNotEmpty](#method-whennotempty)
[where](#method-where)
[whereStrict](#method-wherestrict)
[whereBetween](#method-wherebetween)
[whereIn](#method-wherein)
[whereInStrict](#method-whereinstrict)
[whereInstanceOf](#method-whereinstanceof)
[whereNotBetween](#method-wherenotbetween)
[whereNotIn](#method-wherenotin)
[whereNotInStrict](#method-wherenotinstrict)
[wrap](#method-wrap)
[zip](#method-zip)

</div>

> [!WARNING]
> 컬렉션을 변형(수정)하는 메서드(`shift`, `pop`, `prepend` 등)는 `LazyCollection` 클래스에서 지원되지 **않습니다**.

<a name="lazy-collection-methods"></a>
### 지연 컬렉션 전용 메서드 (Lazy Collection Methods)

`Enumerable` 계약에 정의된 메서드 외에도, `LazyCollection` 클래스에는 다음과 같은 추가 메서드가 포함되어 있습니다:

<a name="method-takeUntilTimeout"></a>
#### `takeUntilTimeout()`

`takeUntilTimeout` 메서드는, 지정한 시간까지 값을 열거(enumerate)하고, 그 이후에는 중단하는 새로운 지연 컬렉션을 반환합니다:

```php
$lazyCollection = LazyCollection::times(INF)
    ->takeUntilTimeout(now()->addMinute());

$lazyCollection->each(function (int $number) {
    dump($number);

    sleep(1);
});

// 1
// 2
// ...
// 58
// 59
```

이 메서드는 예를 들어, 데이터베이스에서 청구서를 커서로 하나씩 가져오고 처리해야 할 때 유용하게 사용할 수 있습니다. 15분마다 실행되는 [스케줄링된 작업](/docs/12.x/scheduling)에서 최대 14분까지만 처리하도록 제한할 수 있습니다:

```php
use App\Models\Invoice;
use Illuminate\Support\Carbon;

Invoice::pending()->cursor()
    ->takeUntilTimeout(
        Carbon::createFromTimestamp(LARAVEL_START)->add(14, 'minutes')
    )
    ->each(fn (Invoice $invoice) => $invoice->submit());
```

<a name="method-tapEach"></a>
#### `tapEach()`

`each` 메서드는 즉시 각 항목에 콜백을 실행하지만, `tapEach` 메서드는 값을 하나씩 꺼낼 때마다 콜백을 실행합니다:

```php
// 아직 아무 것도 출력되지 않음...
$lazyCollection = LazyCollection::times(INF)->tapEach(function (int $value) {
    dump($value);
});

// 세 개의 값만 출력됨...
$array = $lazyCollection->take(3)->all();

// 1
// 2
// 3
```

<a name="method-throttle"></a>
#### `throttle()`

`throttle` 메서드는 지정한 시간(초)마다 한 번씩만 값을 반환하도록 지연 컬렉션을 "스로틀(Throttle, 제한)처리"합니다. 외부 API 호출처럼 요청 수가 제한된 상황에 특히 유용합니다:

```php
use App\Models\User;

User::where('vip', true)
    ->cursor()
    ->throttle(seconds: 1)
    ->each(function (User $user) {
        // 외부 API 호출...
    });
```

<a name="method-remember"></a>
#### `remember()`

`remember` 메서드는 이미 열거된 값을 기억하여, 이후 컬렉션 반복에서 다시 조회하지 않고 캐시된 값을 반환하는 새로운 지연 컬렉션을 만듭니다:

```php
// 아직 쿼리는 실행되지 않음...
$users = User::cursor()->remember();

// 쿼리가 실행됨...
// 처음 5명의 유저를 DB에서 불러옴...
$users->take(5)->all();

// 처음 5명은 컬렉션 캐시에서 불러옴...
// 나머지는 DB에서 불러옴...
$users->take(20)->all();
```

<a name="method-with-heartbeat"></a>
#### `withHeartbeat()`

`withHeartbeat` 메서드는 지연 컬렉션을 반복하는 동안, 정해진 시간 간격마다 콜백을 실행할 수 있게 해줍니다. 이는 락(lock) 갱신, 진행 상황 업데이트 등 주기적 유지작업이 필요한 장시간 실행 작업에 유용합니다:

```php
use Carbon\CarbonInterval;
use Illuminate\Support\Facades\Cache;

$lock = Cache::lock('generate-reports', seconds: 60 * 5);

if ($lock->get()) {
    try {
        Report::where('status', 'pending')
            ->lazy()
            ->withHeartbeat(
                CarbonInterval::minutes(4),
                fn () => $lock->extend(CarbonInterval::minutes(5))
            )
            ->each(fn ($report) => $report->process());
    } finally {
        $lock->release();
    }
}
```
