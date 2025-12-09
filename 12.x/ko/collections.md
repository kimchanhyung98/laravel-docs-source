# 컬렉션 (Collections)

- [소개](#introduction)
    - [컬렉션 생성](#creating-collections)
    - [컬렉션 확장](#extending-collections)
- [사용 가능한 메서드](#available-methods)
- [하이어 오더 메시지](#higher-order-messages)
- [지연 컬렉션(Lazy Collections)](#lazy-collections)
    - [소개](#lazy-collection-introduction)
    - [지연 컬렉션 생성](#creating-lazy-collections)
    - [Enumerable 계약](#the-enumerable-contract)
    - [지연 컬렉션 메서드](#lazy-collection-methods)

<a name="introduction"></a>
## 소개 (Introduction)

`Illuminate\Support\Collection` 클래스는 데이터 배열을 다루기 위한 유연하고 편리한 래퍼를 제공합니다. 예를 들어, 다음 코드를 확인해 보십시오. 배열로부터 새로운 컬렉션 인스턴스를 만들고, 각 요소에 `strtoupper` 함수를 적용한 뒤, 비어 있는 요소를 모두 제거합니다:

```php
$collection = collect(['Taylor', 'Abigail', null])->map(function (?string $name) {
    return strtoupper($name);
})->reject(function (string $name) {
    return empty($name);
});
```

보시는 것처럼, `Collection` 클래스는 메서드 체이닝을 통해 배열의 매핑과 축소 작업 등을 유연하게 수행할 수 있습니다. 일반적으로 컬렉션은 불변(immutable)이므로, 모든 `Collection` 메서드는 완전히 새로운 `Collection` 인스턴스를 반환합니다.

<a name="creating-collections"></a>
### 컬렉션 생성

앞서 언급한대로, `collect` 헬퍼는 주어진 배열에 대해 새로운 `Illuminate\Support\Collection` 인스턴스를 반환합니다. 즉, 컬렉션을 생성하는 일은 매우 간단합니다:

```php
$collection = collect([1, 2, 3]);
```

또한 [make](#method-make) 및 [fromJson](#method-fromjson) 메서드를 사용해서도 컬렉션을 만들 수 있습니다.

> [!NOTE]
> [Eloquent](/docs/12.x/eloquent) 쿼리의 결과는 항상 `Collection` 인스턴스로 반환됩니다.

<a name="extending-collections"></a>
### 컬렉션 확장

컬렉션은 "매크로 가능(macroable)" 특성을 가지고 있어 런타임에 `Collection` 클래스에 추가 메서드를 등록할 수 있습니다. `Illuminate\Support\Collection` 클래스의 `macro` 메서드는 매크로 호출 시 실행될 클로저를 인수로 받습니다. 이 클로저에서 컬렉션의 다른 메서드를 `$this`를 통해 접근할 수 있으므로 실제 컬렉션 클래스의 메서드와 비슷하게 사용할 수 있습니다. 예를 들어, 다음 코드는 `Collection` 클래스에 `toUpper` 메서드를 추가합니다:

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
#### 매크로 인수

필요하다면, 추가 인수를 받는 매크로도 정의할 수 있습니다:

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

이후에 등장하는 대부분의 컬렉션 문서에서는 `Collection` 클래스에서 사용할 수 있는 각 메서드를 설명합니다. 이 모든 메서드는 메서드 체이닝이 가능하여 배열을 유연하게 조작할 수 있으며, 대부분의 메서드는 항상 새로운 `Collection` 인스턴스를 반환하므로 필요할 경우 원본 컬렉션을 보존할 수 있습니다:



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

<!-- 이하 개별 메서드 문서... 이전 가이드라인과 동일하게 선언 -->


<a name="higher-order-messages"></a>
## 하이어 오더 메시지 (Higher Order Messages)

컬렉션은 "하이어 오더 메시지(higher order messages)"를 지원하여 컬렉션에서 자주 사용하는 작업을 간결하게 표현할 수 있습니다. 하이어 오더 메시지를 지원하는 컬렉션 메서드에는 [average](#method-average), [avg](#method-avg), [contains](#method-contains), [each](#method-each), [every](#method-every), [filter](#method-filter), [first](#method-first), [flatMap](#method-flatmap), [groupBy](#method-groupby), [keyBy](#method-keyby), [map](#method-map), [max](#method-max), [min](#method-min), [partition](#method-partition), [reject](#method-reject), [skipUntil](#method-skipuntil), [skipWhile](#method-skipwhile), [some](#method-some), [sortBy](#method-sortby), [sortByDesc](#method-sortbydesc), [sum](#method-sum), [takeUntil](#method-takeuntil), [takeWhile](#method-takewhile), [unique](#method-unique) 등이 있습니다.

각 하이어 오더 메시지는 컬렉션 인스턴스에서 동적 프로퍼티로 접근할 수 있습니다. 예를 들어, `each` 하이어 오더 메시지를 사용하여 컬렉션의 각 객체에 대해 메서드를 호출할 수 있습니다:

```php
use App\Models\User;

$users = User::where('votes', '>', 500)->get();

$users->each->markAsVip();
```

또한, `sum` 하이어 오더 메시지를 사용해 사용자 컬렉션의 "votes" 총합을 계산할 수도 있습니다:

```php
$users = User::where('group', 'Development')->get();

return $users->sum->votes;
```

<a name="lazy-collections"></a>
## 지연 컬렉션 (Lazy Collections)

<a name="lazy-collection-introduction"></a>
### 소개

> [!WARNING]
> Laravel의 지연 컬렉션에 대해 더 알아보기 전에, [PHP 제너레이터](https://www.php.net/manual/en/language.generators.overview.php)에 익숙해지는 시간을 가지시기 바랍니다.

기존의 강력한 `Collection` 클래스 외에, `LazyCollection` 클래스는 PHP의 [제너레이터(generator)](https://www.php.net/manual/en/language.generators.overview.php) 기능을 활용하여 매우 큰 데이터셋도 메모리 사용을 최소화하면서 다룰 수 있게 해줍니다.

예를 들어, 애플리케이션에서 여러 GB에 달하는 로그 파일을 처리해야 할 때 Laravel의 컬렉션 메서드를 활용해서 로그를 파싱하고 싶다면, 모든 파일을 한 번에 메모리로 읽지 않고 지연 컬렉션을 이용해 한 번에 파일의 일부만 메모리에 올릴 수 있습니다:

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
    // 로그 처리 ...
});
```

또는, 10,000개의 Eloquent 모델을 반복해야 한다고 가정해봅시다. 기존 Laravel 컬렉션을 사용하면 10,000개의 모델이 한 번에 메모리로 로드되어야 합니다:

```php
use App\Models\User;

$users = User::all()->filter(function (User $user) {
    return $user->id > 500;
});
```

하지만 쿼리 빌더의 `cursor` 메서드는 `LazyCollection` 인스턴스를 반환하므로, 데이터베이스에는 한 번만 쿼리를 실행하지만 Eloquent 모델은 한 번에 하나만 메모리에 적재할 수 있습니다. 이 예시에서 `filter` 콜백은 각 유저를 실제로 순회할 때까지 실행되지 않아 메모리 사용량이 크게 줄어듭니다:

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
### 지연 컬렉션 생성

지연 컬렉션 인스턴스를 생성하려면, 컬렉션의 `make` 메서드에 PHP 제너레이터 함수를 전달하면 됩니다:

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
### Enumerable 계약

`Collection` 클래스에서 사용할 수 있는 거의 모든 메서드는 `LazyCollection` 클래스에서도 사용할 수 있습니다. 두 클래스 모두 `Illuminate\Support\Enumerable` 계약을 구현하며, 이 계약에는 다음과 같은 메서드가 정의되어 있습니다:



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
> 컬렉션에 변이를 가하는 메서드(예: `shift`, `pop`, `prepend` 등)는 `LazyCollection` 클래스에서는 **사용할 수 없습니다**.

<a name="lazy-collection-methods"></a>
### 지연 컬렉션 메서드

`Enumerable` 계약에 정의된 메서드 외에도, `LazyCollection` 클래스에서는 다음과 같은 메서드를 추가로 제공합니다:

<a name="method-takeUntilTimeout"></a>
#### `takeUntilTimeout()`

`takeUntilTimeout` 메서드는 지정한 시간까지 값을 열거하는 새로운 지연 컬렉션을 반환합니다. 해당 시간이 지나면 컬렉션의 열거를 중단합니다:

```php
$lazyCollection = LazyCollection::times(INF)
    ->takeUntilTimeout(now()->plus(minutes: 1));

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

이 메서드의 사용 예로, 데이터베이스에서 청구서(invoice)를 커서로 가져와 제출하는 애플리케이션이 있다고 가정할 때, [스케줄된 작업](/docs/12.x/scheduling)이 15분마다 실행되지만 실제 처리 시간은 최대 14분으로 제한할 수 있습니다:

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

`each` 메서드는 컬렉션의 각 아이템마다 즉시 콜백을 호출하지만, `tapEach` 메서드는 목록에서 아이템이 하나씩 꺼내질 때에만 콜백을 호출합니다:

```php
// 아직 아무것도 dump되지 않음...
$lazyCollection = LazyCollection::times(INF)->tapEach(function (int $value) {
    dump($value);
});

// 3개의 아이템이 dump됨...
$array = $lazyCollection->take(3)->all();

// 1
// 2
// 3
```

<a name="method-throttle"></a>
#### `throttle()`

`throttle` 메서드는 각 값을 지정한 초만큼 지연하여 반환하도록 지연 컬렉션을 조절합니다. 이 메서드는 특히 외부 API와 같이 요청에 제한이 있는 상황에서 유용합니다:

```php
use App\Models\User;

User::where('vip', true)
    ->cursor()
    ->throttle(seconds: 1)
    ->each(function (User $user) {
        // 외부 API 호출 ...
    });
```

<a name="method-remember"></a>
#### `remember()`

`remember` 메서드는 이미 열거된 값을 캐시에 저장하여, 이후 컬렉션을 다시 열거할 때 해당 값을 재사용하도록 하는 새로운 지연 컬렉션을 반환합니다:

```php
// 아직 쿼리가 실행되지 않음...
$users = User::cursor()->remember();

// 이 시점에 쿼리가 실행됨...
// 처음 5명의 사용자가 DB에서 hydrate됨...
$users->take(5)->all();

// 이후 처음 5개는 캐시에서, 남은 사용자는 DB에서 가져옴...
$users->take(20)->all();
```

<a name="method-with-heartbeat"></a>
#### `withHeartbeat()`

`withHeartbeat` 메서드는 지연 컬렉션이 열거되는 동안 일정 시간마다 콜백을 실행할 수 있게 해줍니다. 이 기능은 락(lock) 연장이나 진행 상황 알림 등 주기적인 유지보수가 필요한 장기 실행 작업에 유용합니다:

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
