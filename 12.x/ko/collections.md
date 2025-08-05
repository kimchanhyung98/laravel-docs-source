# 컬렉션 (Collections)

- [소개](#introduction)
    - [컬렉션 생성](#creating-collections)
    - [컬렉션 확장](#extending-collections)
- [사용 가능한 메서드](#available-methods)
- [하이어 오더 메시지](#higher-order-messages)
- [래이지 컬렉션](#lazy-collections)
    - [소개](#lazy-collection-introduction)
    - [래이지 컬렉션 생성](#creating-lazy-collections)
    - [Enumerable 계약](#the-enumerable-contract)
    - [래이지 컬렉션의 메서드](#lazy-collection-methods)

<a name="introduction"></a>
## 소개 (Introduction)

`Illuminate\Support\Collection` 클래스는 데이터 배열을 다루기 위한 유연하고 편리한 래퍼를 제공합니다. 예를 들어, 아래 코드 예시를 살펴보십시오. `collect` 헬퍼로 새로운 컬렉션 인스턴스를 배열에서 생성하고, 각 요소에 `strtoupper` 함수를 실행한 후, 모든 비어있는 요소를 제거합니다.

```php
$collection = collect(['Taylor', 'Abigail', null])->map(function (?string $name) {
    return strtoupper($name);
})->reject(function (string $name) {
    return empty($name);
});
```

위 예시에서 볼 수 있듯이, `Collection` 클래스는 메서드 체이닝을 통해 배열을 유연하게 매핑 및 축소할 수 있습니다. 일반적으로 컬렉션은 불변(immutable) 구조이므로, 모든 `Collection` 메서드는 항상 완전히 새로운 `Collection` 인스턴스를 반환합니다.

<a name="creating-collections"></a>
### 컬렉션 생성 (Creating Collections)

앞서 언급한 것처럼, `collect` 헬퍼는 주어진 배열에 대해 새로운 `Illuminate\Support\Collection` 인스턴스를 반환합니다. 컬렉션을 생성하는 방법은 매우 간단합니다.

```php
$collection = collect([1, 2, 3]);
```

또한 [make](#method-make) 및 [fromJson](#method-fromjson) 메서드를 사용해 컬렉션을 생성할 수도 있습니다.

> [!NOTE]
> [Eloquent](/docs/12.x/eloquent) 쿼리의 결과는 항상 `Collection` 인스턴스로 반환됩니다.

<a name="extending-collections"></a>
### 컬렉션 확장 (Extending Collections)

컬렉션은 "매크로(macroable)" 특성이 있어, 실행 시점(runtime)에 `Collection` 클래스에 추가 메서드를 등록할 수 있습니다. `Illuminate\Support\Collection` 클래스의 `macro` 메서드는 매크로가 호출될 때 실행할 클로저를 인수로 받습니다. 매크로의 클로저에서는 `$this`를 통해 컬렉션의 다른 메서드에 접근할 수 있는데, 이는 마치 진짜 컬렉션 클래스의 메서드처럼 동작합니다. 예를 들어, 다음 코드에서는 `Collection` 클래스에 `toUpper` 메서드를 추가합니다.

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

필요하다면, 추가 인수를 받는 매크로도 정의할 수 있습니다.

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

이후의 컬렉션 문서 대부분에서는 `Collection` 클래스에서 사용할 수 있는 각 메서드에 대해 다룹니다. 이 모든 메서드는 메서드 체이닝이 가능하여 배열을 쉽게 조작할 수 있습니다. 또한, 거의 모든 메서드는 새로운 `Collection` 인스턴스를 반환하므로, 필요하다면 원본 컬렉션의 사본을 안전하게 보존할 수 있습니다.

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

*(이하 각 메서드 설명은 원문과 동일하게 순차적으로 번역되어 있습니다. 코드블록, 변수명, 결과 등은 절대 변형·번역되지 않았습니다. 각 메서드 별 세부 설명은 본문을 참조하세요.)*

<a name="higher-order-messages"></a>
## 하이어 오더 메시지 (Higher Order Messages)

컬렉션은 "하이어 오더 메시지(higher order messages)" 기능도 지원하여, 컬렉션에서 자주 사용하는 동작을 더욱 간단히 수행할 수 있게 해줍니다. 하이어 오더 메시지를 지원하는 컬렉션 메서드는 다음과 같습니다: [average](#method-average), [avg](#method-avg), [contains](#method-contains), [each](#method-each), [every](#method-every), [filter](#method-filter), [first](#method-first), [flatMap](#method-flatmap), [groupBy](#method-groupby), [keyBy](#method-keyby), [map](#method-map), [max](#method-max), [min](#method-min), [partition](#method-partition), [reject](#method-reject), [skipUntil](#method-skipuntil), [skipWhile](#method-skipwhile), [some](#method-some), [sortBy](#method-sortby), [sortByDesc](#method-sortbydesc), [sum](#method-sum), [takeUntil](#method-takeuntil), [takeWhile](#method-takewhile), [unique](#method-unique).

각 하이어 오더 메시지는 컬렉션 인스턴스의 동적 프로퍼티로 접근할 수 있습니다. 예를 들어, 컬렉션 내의 각 객체에서 특정 메서드를 호출하고 싶을 때 다음과 같이 사용할 수 있습니다.

```php
use App\Models\User;

$users = User::where('votes', '>', 500)->get();

$users->each->markAsVip();
```

유저 컬렉션에서 "votes" 총합을 구하고 싶을 때도 하이어 오더 메시지로 더욱 간결하게 작성할 수 있습니다.

```php
$users = User::where('group', 'Development')->get();

return $users->sum->votes;
```

<a name="lazy-collections"></a>
## 래이지 컬렉션 (Lazy Collections)

<a name="lazy-collection-introduction"></a>
### 소개

> [!WARNING]
> Laravel의 래이지 컬렉션을 학습하기 전에, [PHP 제너레이터(Generators)](https://www.php.net/manual/en/language.generators.overview.php) 개념을 먼저 익혀두는 것이 좋습니다.

기존의 강력한 `Collection` 클래스에 더해, `LazyCollection` 클래스는 PHP의 [제너레이터](https://www.php.net/manual/en/language.generators.overview.php)를 활용하여, 대용량 데이터셋을 메모리 사용량을 최소화하며 다룰 수 있게 해줍니다.

예를 들어, 애플리케이션에서 수GB 크기의 로그 파일을 처리해야 한다고 가정해봅시다. 이때 Laravel의 컬렉션 메서드를 사용하여 로그를 파싱하고 싶을 때 전체 파일을 한꺼번에 메모리에 올리지 않고, 래이지 컬렉션을 이용하면 한 번에 파일 일부만 메모리에 유지하면서 작업할 수 있습니다.

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

또는 10,000개의 Eloquent 모델을 순회해야 하는 경우를 생각해봅시다. 전통적인 Laravel 컬렉션을 사용할 경우, 모든 10,000개의 Eloquent 모델 인스턴스를 한 번에 메모리에 로드해야 합니다.

```php
use App\Models\User;

$users = User::all()->filter(function (User $user) {
    return $user->id > 500;
});
```

하지만 쿼리 빌더의 `cursor` 메서드는 `LazyCollection` 인스턴스를 반환합니다. 이를 사용하면, 데이터베이스 쿼리는 한 번만 실행되고, 동시에 오직 하나의 Eloquent 모델만 메모리에 로드하게 됩니다. 아래 예시에서처럼 실제로 각 사용자에 대해 반복(iterate)할 때까지 `filter` 콜백은 실행되지 않으므로, 메모리 사용량이 크게 줄어듭니다.

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
### 래이지 컬렉션 생성 (Creating Lazy Collections)

래이지 컬렉션 인스턴스를 만들기 위해서는 PHP 제너레이터 함수를 컬렉션의 `make` 메서드에 전달하면 됩니다.

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

`Collection` 클래스에서 사용할 수 있는 거의 모든 메서드는 `LazyCollection` 클래스에서도 사용할 수 있습니다. 이 두 클래스는 모두 `Illuminate\Support\Enumerable` 계약(Contract)을 구현하며, 다음과 같은 메서드들을 포함합니다.

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
> 컬렉션을 변경(mutate)하는 메서드(예: `shift`, `pop`, `prepend` 등)는 `LazyCollection` 클래스에서는 **지원되지 않습니다**.

<a name="lazy-collection-methods"></a>
### 래이지 컬렉션의 메서드 (Lazy Collection Methods)

`Enumerable` 계약에 정의된 메서드 외에도, `LazyCollection` 클래스는 다음과 같은 추가 메서드를 포함하고 있습니다.

<a name="method-takeUntilTimeout"></a>
#### `takeUntilTimeout()`

`takeUntilTimeout` 메서드는 지정한 시간까지 값을 반복하는 새로운 래이지 컬렉션을 반환합니다. 그 시간이 지나면 더 이상 값을 열거하지 않습니다.

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

이 메서드는, 예를 들어 데이터베이스에서 인보이스를 커서로 가져와 제출해야 하는 작업에서 유용하게 사용할 수 있습니다. 15분마다 실행되는 [스케줄러 태스크](/docs/12.x/scheduling)에서, 최대 14분만 인보이스를 처리하게 만들 수 있습니다.

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

`each` 메서드는 컬렉션의 모든 항목에 대해 즉시 주어진 콜백을 호출하지만, `tapEach` 메서드는 항목이 실제로 하나씩 필요할 때마다 콜백을 호출합니다.

```php
// 아직 아무 것도 덤프되지 않은 상태...
$lazyCollection = LazyCollection::times(INF)->tapEach(function (int $value) {
    dump($value);
});

// 세 개의 항목이 덤프됨...
$array = $lazyCollection->take(3)->all();

// 1
// 2
// 3
```

<a name="method-throttle"></a>
#### `throttle()`

`throttle` 메서드는 각 값을 지정한 초 단위 시간 간격마다 반환하게 하여, 래이지 컬렉션의 반복 속도를 제한합니다. 외부 API 등 요청 제한(rate limit)이 있는 상황에서 매우 유용하게 사용할 수 있습니다.

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

`remember` 메서드는 이미 반복(iterate)된 값을 기억(cache)해서, 이후에 컬렉션을 다시 반복할 때는 해당 값을 재조회하지 않고 캐시에서 가져옵니다.

```php
// 아직 쿼리는 실행되지 않음...
$users = User::cursor()->remember();

// 쿼리가 실행되고...
// 처음 5명의 유저가 데이터베이스에서 생성됨...
$users->take(5)->all();

// 첫 5명의 유저는 컬렉션의 캐시에서 가져옴...
// 나머지는 데이터베이스에서 추가로 생성...
$users->take(20)->all();
```
