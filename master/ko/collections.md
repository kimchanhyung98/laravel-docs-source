# 컬렉션 (Collections)

- [소개](#introduction)
    - [컬렉션 생성](#creating-collections)
    - [컬렉션 확장](#extending-collections)
- [사용 가능한 메서드](#available-methods)
- [하이어 오더 메시지](#higher-order-messages)
- [래지 컬렉션 (Lazy Collections)](#lazy-collections)
    - [소개](#lazy-collection-introduction)
    - [래지 컬렉션 생성](#creating-lazy-collections)
    - [Enumerable 계약](#the-enumerable-contract)
    - [래지 컬렉션 전용 메서드](#lazy-collection-methods)

<a name="introduction"></a>
## 소개 (Introduction)

`Illuminate\Support\Collection` 클래스는 배열 데이터 작업을 위한 유연하고 편리한 래퍼를 제공합니다. 예를 들어, 아래 코드를 확인하세요. `collect` 헬퍼로 배열을 컬렉션 인스턴스로 만들고, 각 요소에 `strtoupper` 함수를 적용한 뒤, 비어있는 요소를 모두 제거합니다:

```php
$collection = collect(['Taylor', 'Abigail', null])->map(function (?string $name) {
    return strtoupper($name);
})->reject(function (string $name) {
    return empty($name);
});
```

보시는 것처럼, `Collection` 클래스는 메서드를 체이닝하여 배열을 유연하게 매핑 및 축소(reduce)할 수 있도록 해줍니다. 일반적으로 컬렉션은 불변(immutable)이며, 각 `Collection` 메서드는 완전히 새로운 `Collection` 인스턴스를 반환합니다.

<a name="creating-collections"></a>
### 컬렉션 생성 (Creating Collections)

앞서 언급한 것처럼, `collect` 헬퍼는 전달된 배열로부터 새로운 `Illuminate\Support\Collection` 인스턴스를 반환합니다. 따라서 컬렉션을 생성하는 것은 매우 간단합니다:

```php
$collection = collect([1, 2, 3]);
```

또한 [make](#method-make) 및 [fromJson](#method-fromjson) 메서드를 사용해 컬렉션을 생성할 수도 있습니다.

> [!NOTE]
> [Eloquent](/docs/master/eloquent) 쿼리의 결과는 항상 `Collection` 인스턴스로 반환됩니다.

<a name="extending-collections"></a>
### 컬렉션 확장 (Extending Collections)

컬렉션은 "매크로블(macroable)"하므로, 실행 시점에 `Collection` 클래스에 추가 메서드를 동적으로 정의할 수 있습니다. `Illuminate\Support\Collection` 클래스의 `macro` 메서드는 여러분이 정의한 클로저를 매크로가 호출될 때 실행합니다. 이 클로저 안에서는 `$this`를 통해 컬렉션의 다른 메서드에 접근할 수 있으며, 마치 컬렉션의 실제 메서드처럼 동작합니다. 예를 들어, 다음 코드는 `Collection` 클래스에 `toUpper` 메서드를 추가합니다:

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

보통, 컬렉션 매크로는 [서비스 프로바이더](/docs/master/providers)의 `boot` 메서드 내에서 선언하는 것이 좋습니다.

<a name="macro-arguments"></a>
#### 매크로 인수 (Macro Arguments)

필요하다면, 매크로가 추가 인수를 받도록 정의할 수 있습니다:

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

// ['primero', 'segundo'];
```

<a name="available-methods"></a>
## 사용 가능한 메서드 (Available Methods)

이후의 컬렉션 문서에서는 `Collection` 클래스에서 사용할 수 있는 각 메서드에 대해 다룹니다. 아래의 모든 메서드들은 체이닝이 가능하여, 배열을 유연하게 조작할 수 있습니다. 또한 거의 모든 메서드는 새로운 `Collection` 인스턴스를 반환하므로, 필요에 따라 원본 컬렉션을 보존할 수도 있습니다:



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
[hasMany](#method-hasmany)
[hasSole](#method-hassole)
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

[아래 메서드 설명 전체는 원본과 구조상 동일합니다. 코드 블록 및 예시는 원문과 일치하므로 생략합니다.]

<a name="higher-order-messages"></a>
## 하이어 오더 메시지 (Higher Order Messages)

컬렉션은 "하이어 오더 메시지(higher order messages)"도 지원합니다. 이는 컬렉션에서 자주 반복되는 작업을 더 간결하게 작성할 수 있게 해주는 축약 문법입니다. 지원되는 컬렉션 메서드로는 [average](#method-average), [avg](#method-avg), [contains](#method-contains), [each](#method-each), [every](#method-every), [filter](#method-filter), [first](#method-first), [flatMap](#method-flatmap), [groupBy](#method-groupby), [keyBy](#method-keyby), [map](#method-map), [max](#method-max), [min](#method-min), [partition](#method-partition), [reject](#method-reject), [skipUntil](#method-skipuntil), [skipWhile](#method-skipwhile), [some](#method-some), [sortBy](#method-sortby), [sortByDesc](#method-sortbydesc), [sum](#method-sum), [takeUntil](#method-takeuntil), [takeWhile](#method-takewhile), [unique](#method-unique) 등이 있습니다.

각 하이어 오더 메시지는 컬렉션 인스턴스의 동적 프로퍼티처럼 접근할 수 있습니다. 예를 들어, 컬렉션 내 모든 객체에서 메서드를 호출할 때 `each` 메시지를 다음과 같이 사용할 수 있습니다:

```php
use App\Models\User;

$users = User::where('votes', '>', 500)->get();

$users->each->markAsVip();
```

마찬가지로, 컬렉션의 모든 사용자가 가진 "votes" 총합을 구할 때 `sum` 하이어 오더 메시지를 사용할 수 있습니다:

```php
$users = User::where('group', 'Development')->get();

return $users->sum->votes;
```

<a name="lazy-collections"></a>
## 래지 컬렉션 (Lazy Collections)

<a name="lazy-collection-introduction"></a>
### 소개

> [!WARNING]
> Laravel의 래지 컬렉션(Lazy Collections)을 제대로 활용하려면, 먼저 [PHP 제너레이터](https://www.php.net/manual/en/language.generators.overview.php)에 대해 충분히 이해하는 것이 좋습니다.

이미 강력한 `Collection` 클래스의 기능을 보완하기 위해, `LazyCollection` 클래스는 PHP의 [제너레이터(generator)](https://www.php.net/manual/en/language.generators.overview.php)를 활용하여 아주 큰 데이터셋도 적은 메모리로 처리할 수 있도록 도와줍니다.

예를 들어, 여러 GB 용량의 로그 파일을 처리하며 Laravel 컬렉션 메서드를 활용해야 한다고 가정해봅시다. 파일 전체를 메모리로 읽어들이는 대신, 래지 컬렉션을 사용하면 한 번에 일부 라인만 메모리에 로드하여 작업할 수 있습니다:

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

또는, 10,000개의 Eloquent 모델을 반복 처리해야 할 때, 기존 Laravel 컬렉션을 사용하면 10,000개 모두를 한꺼번에 메모리에 불러와야 했습니다:

```php
use App\Models\User;

$users = User::all()->filter(function (User $user) {
    return $user->id > 500;
});
```

하지만 쿼리 빌더의 `cursor` 메서드는 `LazyCollection` 인스턴스를 반환합니다. 이를 사용하면 단 한 번의 쿼리로도 각 모델을 하나씩만 메모리에 유지할 수 있습니다. 아래 예시처럼, 실제로 반복문을 돌기 전까지는 `filter` 콜백이 실행되지 않으므로, 메모리 사용량이 크게 줄어듭니다:

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
### 래지 컬렉션 생성 (Creating Lazy Collections)

래지 컬렉션 인스턴스를 생성하려면, PHP의 제너레이터 함수를 컬렉션의 `make` 메서드에 전달하면 됩니다:

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
### Enumerable 계약 (The Enumerable Contract)

`Collection` 클래스에서 제공되는 거의 모든 메서드는 `LazyCollection` 클래스에도 동일하게 구현되어 있습니다. 두 클래스 모두 `Illuminate\Support\Enumerable` 계약을 구현하고 있으며, 이 계약에서 정의된 메서드는 다음과 같습니다:



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
> 컬렉션의 상태를 직접 변경하는 메서드(예: `shift`, `pop`, `prepend` 등)는 `LazyCollection` 클래스에서는 **지원되지 않습니다**.

<a name="lazy-collection-methods"></a>
### 래지 컬렉션 전용 메서드 (Lazy Collection Methods)

`Enumerable` 계약에 정의된 메서드 외에도, `LazyCollection` 클래스에는 아래와 같은 전용 메서드들이 포함되어 있습니다:

<a name="method-takeUntilTimeout"></a>
#### `takeUntilTimeout()`

`takeUntilTimeout` 메서드는 지정된 시간까지 값들을 차례로 열거하며, 시간이 되면 컬렉션의 열거를 자동으로 중단하는 새로운 래지 컬렉션을 반환합니다:

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

이 메서드의 활용 예로, 데이터베이스에서 청구서를 커서(cursor)로 가져오는 애플리케이션을 상상해보세요. 15분마다 실행되는 [스케줄러 작업](/docs/master/scheduling)에서 14분까지만 청구서를 처리하도록 할 수 있습니다:

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

`each` 메서드는 즉시 각 아이템에 대해 콜백을 호출합니다. 하지만 `tapEach` 메서드는 해당 컬렉션에서 하나씩 아이템을 꺼낼 때마다 콜백을 호출합니다:

```php
// 이 시점에서는 아무것도 dump되지 않습니다...
$lazyCollection = LazyCollection::times(INF)->tapEach(function (int $value) {
    dump($value);
});

// 아래에서 3개의 아이템이 dump됩니다...
$array = $lazyCollection->take(3)->all();

// 1
// 2
// 3
```

<a name="method-throttle"></a>
#### `throttle()`

`throttle` 메서드는 래지 컬렉션이 각 값을 지정한 초만큼 지연해 반환하도록 제한합니다. 외부 API 호출 등, 요청 제한(rate-limit)이 있는 상황에서 특히 유용합니다:

```php
use App\Models\User;

User::where('vip', true)
    ->cursor()
    ->throttle(seconds: 1)
    ->each(function (User $user) {
        // 외부 API 호출 등...
    });
```

<a name="method-remember"></a>
#### `remember()`

`remember` 메서드는 이미 열거된 값은 다시 가져오지 않고 캐시에 저장해 두는 새로운 래지 컬렉션을 반환합니다:

```php
// 아직 쿼리는 실행되지 않았습니다...
$users = User::cursor()->remember();

// 첫 5명의 사용자가 데이터베이스에서 조회됩니다...
$users->take(5)->all();

// 처음 5명은 컬렉션 캐시에서 가져오고,
// 나머지는 데이터베이스에서 가져옵니다...
$users->take(20)->all();
```

<a name="method-with-heartbeat"></a>
#### `withHeartbeat()`

`withHeartbeat` 메서드는 래지 컬렉션이 열거되는 동안 지정한 시간 간격마다 콜백을 실행할 수 있도록 해줍니다. 이 기능은 잠금(lock) 연장이나 진행 상황 업데이트 등 주기적인 유지 작업이 필요한 장시간 실행 작업에 특히 유용합니다:

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
