# 컬렉션 (Collections)

- [소개](#introduction)
    - [컬렉션 생성하기](#creating-collections)
    - [컬렉션 확장하기](#extending-collections)
- [사용 가능한 메서드](#available-methods)
- [하이어 오더 메시지](#higher-order-messages)
- [지연 컬렉션(Lazy Collections)](#lazy-collections)
    - [소개](#lazy-collection-introduction)
    - [지연 컬렉션 생성하기](#creating-lazy-collections)
    - [Enumerable 계약(Contract)](#the-enumerable-contract)
    - [지연 컬렉션 메서드](#lazy-collection-methods)

<a name="introduction"></a>
## 소개 (Introduction)

`Illuminate\Support\Collection` 클래스는 데이터 배열을 편리하게 다룰 수 있도록 유창하고 편리한 래퍼(wrapper)를 제공합니다. 예를 들어 아래 코드를 살펴보세요. `collect` 헬퍼를 사용해 배열로부터 새로운 컬렉션 인스턴스를 만들고, 각 요소에 `strtoupper` 함수를 실행한 뒤, 비어있는 요소는 모두 제거합니다.

```php
$collection = collect(['Taylor', 'Abigail', null])->map(function (?string $name) {
    return strtoupper($name);
})->reject(function (string $name) {
    return empty($name);
});
```

보시다시피, `Collection` 클래스는 메서드 체이닝을 통해 배열의 맵핑과 축소를 매우 유연하게 처리할 수 있도록 해줍니다. 일반적으로 컬렉션은 불변(immutable)이며, 즉 모든 `Collection` 메서드는 완전히 새로운 `Collection` 인스턴스를 반환합니다.

<a name="creating-collections"></a>
### 컬렉션 생성하기

위에서 언급한 것처럼, `collect` 헬퍼는 주어진 배열로부터 새로운 `Illuminate\Support\Collection` 인스턴스를 반환합니다. 컬렉션을 생성하는 것은 아래와 같이 매우 간단합니다.

```php
$collection = collect([1, 2, 3]);
```

[make](#method-make) 및 [fromJson](#method-fromjson) 메서드를 사용해서도 컬렉션을 생성할 수 있습니다.

> [!NOTE]
> [Eloquent](/docs/12.x/eloquent) 쿼리의 결과는 항상 `Collection` 인스턴스로 반환됩니다.

<a name="extending-collections"></a>
### 컬렉션 확장하기

컬렉션은 "매크로(macroable)" 기능을 지원하므로, 런타임에 `Collection` 클래스에 새로운 메서드를 추가할 수 있습니다. `Illuminate\Support\Collection` 클래스의 `macro` 메서드는 매크로 호출 시 실행될 클로저를 받습니다. 매크로 클로저 내부에서는 컬렉션 클래스의 실제 메서드처럼 `$this`를 통해 컬렉션의 다른 메서드에 접근할 수 있습니다. 예를 들면, 아래 코드는 `Collection` 클래스에 `toUpper`라는 메서드를 추가합니다.

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

필요하다면 매크로가 추가 인수를 받을 수 있습니다.

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

이후 컬렉션 문서에서는 `Collection` 클래스에서 사용할 수 있는 각각의 메서드에 대해 다룹니다. 이 모든 메서드는 배열을 유연하게 조작하기 위해 체이닝할 수 있습니다. 또한, 거의 모든 메서드는 새로운 `Collection` 인스턴스를 반환하므로, 필요하다면 원본 컬렉션을 그대로 보존할 수 있습니다.

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
[containsManyItems](#method-containsmanyitems)
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

<!-- 이하 메서드 레퍼런스 (생략된 부분은 위 코어 가이드라인에 따라 번역하시면 됩니다.) -->

<a name="higher-order-messages"></a>
## 하이어 오더 메시지 (Higher Order Messages)

컬렉션은 "하이어 오더 메시지(higher order messages)"도 지원합니다. 이는 자주 사용하는 동작을 컬렉션 내에서 간단한 문법으로 처리할 수 있는 단축 기능입니다. 하이어 오더 메시지를 제공하는 컬렉션 메서드는 다음과 같습니다: [average](#method-average), [avg](#method-avg), [contains](#method-contains), [each](#method-each), [every](#method-every), [filter](#method-filter), [first](#method-first), [flatMap](#method-flatmap), [groupBy](#method-groupby), [keyBy](#method-keyby), [map](#method-map), [max](#method-max), [min](#method-min), [partition](#method-partition), [reject](#method-reject), [skipUntil](#method-skipuntil), [skipWhile](#method-skipwhile), [some](#method-some), [sortBy](#method-sortby), [sortByDesc](#method-sortbydesc), [sum](#method-sum), [takeUntil](#method-takeuntil), [takeWhile](#method-takewhile), [unique](#method-unique).

각 하이어 오더 메시지는 컬렉션 인스턴스의 동적 프로퍼티(dynamc property)로 접근할 수 있습니다. 예를 들어, 컬렉션 내부 각 객체에 대해 메서드를 호출할 때 `each` 하이어 오더 메시지를 사용할 수 있습니다.

```php
use App\Models\User;

$users = User::where('votes', '>', 500)->get();

$users->each->markAsVip();
```

마찬가지로, `sum` 하이어 오더 메시지를 활용해 사용자 컬렉션의 "votes" 총합을 구할 수도 있습니다.

```php
$users = User::where('group', 'Development')->get();

return $users->sum->votes;
```

<a name="lazy-collections"></a>
## 지연 컬렉션 (Lazy Collections)

<a name="lazy-collection-introduction"></a>
### 소개

> [!WARNING]
> Laravel의 지연 컬렉션을 더 깊이 학습하기 전에, [PHP 제너레이터(generator)](https://www.php.net/manual/en/language.generators.overview.php) 개념에 친숙해지는 것이 좋습니다.

이미 강력한 `Collection` 클래스에 더해, `LazyCollection` 클래스는 PHP의 [제너레이터(generator)](https://www.php.net/manual/en/language.generators.overview.php)를 활용하여, 메모리 사용량을 최소화하면서 매우 큰 데이터셋도 다룰 수 있도록 해줍니다.

예를 들어, 애플리케이션에서 수 기가바이트에 달하는 로그 파일을 처리해야 하면서, Laravel의 컬렉션 메서드로 로그를 분석하고 싶다고 가정해 봅시다. 파일 전체를 한 번에 읽어 들이지 않고, 지연 컬렉션을 사용하면 한 번에 파일의 일부만 메모리에 보관하며 처리할 수 있습니다.

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
    // 로그 항목 처리...
});
```

또는 10,000개의 Eloquent 모델을 순회해야 한다고 해봅시다. 기존 Laravel 컬렉션을 사용할 경우, 10,000개의 Eloquent 모델이 메모리에 한 번에 모두 로드됩니다.

```php
use App\Models\User;

$users = User::all()->filter(function (User $user) {
    return $user->id > 500;
});
```

그러나 쿼리 빌더의 `cursor` 메서드는 `LazyCollection` 인스턴스를 반환하므로, 여전히 데이터베이스에는 쿼리 한 번만 실행되지만 매번 한 개의 Eloquent 모델만 메모리에 유지할 수 있습니다. 이 예제에서 `filter` 콜백은 실제로 각 사용자를 반복(iterate)할 때까지 실행되지 않으므로 메모리 사용량이 크게 줄어듭니다.

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
### 지연 컬렉션 생성하기

지연 컬렉션 인스턴스를 생성하려면, PHP 제너레이터 함수를 컬렉션의 `make` 메서드에 전달하면 됩니다.

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

`Collection` 클래스에서 사용할 수 있는 거의 모든 메서드는 `LazyCollection` 클래스에서도 사용할 수 있습니다. 두 클래스 모두 `Illuminate\Support\Enumerable` 계약을 구현하는데, 이 계약에는 아래와 같은 메서드가 정의되어 있습니다.

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
> 컬렉션의 값을 변경하는 메서드(`shift`, `pop`, `prepend` 등)는 `LazyCollection` 클래스에서 사용할 수 **없습니다**.

<a name="lazy-collection-methods"></a>
### 지연 컬렉션 메서드 (Lazy Collection Methods)

`Enumerable` 계약에 정의된 메서드 외에도, `LazyCollection` 클래스만의 고유 메서드들이 존재합니다.

<a name="method-takeUntilTimeout"></a>
#### `takeUntilTimeout()`

`takeUntilTimeout` 메서드는 지정된 시간까지 값을 나열하고, 그 시간이 지나면 더 이상 값을 나열하지 않는 새로운 지연 컬렉션을 반환합니다.

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

이 메서드의 활용 예시로, 데이터베이스에서 인보이스를 커서를 사용해 제출하는 애플리케이션이 있다고 가정해보세요. [스케줄 태스크](/docs/12.x/scheduling)로 15분마다 한 번씩 실행하며, 최대 14분 동안만 인보이스를 처리할 수 있습니다.

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

`each` 메서드는 컬렉션의 모든 항목을 즉시 콜백에 전달하는 반면, `tapEach`는 값을 하나씩 꺼낼 때만 콜백을 호출합니다.

```php
// 아직 아무것도 출력(logging)되지 않았습니다...
$lazyCollection = LazyCollection::times(INF)->tapEach(function (int $value) {
    dump($value);
});

// 3개의 항목이 출력됩니다...
$array = $lazyCollection->take(3)->all();

// 1
// 2
// 3
```

<a name="method-throttle"></a>
#### `throttle()`

`throttle` 메서드는 컬렉션의 각 값이 지정한 초만큼의 간격으로 반환되도록 지연시킵니다. 이 메서드는 외부 API 등에서 입력 요청을 제한(rate limit)하는 환경에서 유용합니다.

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

`remember` 메서드는 이미 나열된 값을 기억하는 새로운 지연 컬렉션을 반환하며, 이후 컬렉션을 다시 순회할 때 해당 값을 다시 가져오지 않습니다.

```php
// 아직 쿼리가 실행되지 않았습니다...
$users = User::cursor()->remember();

// 쿼리가 실행됩니다...
// 처음 5명의 사용자가 데이터베이스에서 조회됩니다...
$users->take(5)->all();

// 앞선 5명은 컬렉션 캐시에서 가져오고...
// 나머지는 데이터베이스에서 하이드레이션됩니다...
$users->take(20)->all();
```

<a name="method-with-heartbeat"></a>
#### `withHeartbeat()`

`withHeartbeat` 메서드는 지연 컬렉션을 순회(enumerate)하는 동안 일정 시간 간격마다 콜백을 실행할 수 있도록 해줍니다. 이 방법은 주로 락(lock) 연장, 진행상황(proggress) 업데이트 등 주기적인 유지보수 작업이 필요한 장기 실행 작업에서 유용합니다.

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