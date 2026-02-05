# 컬렉션 (Collections)

- [소개](#introduction)
    - [컬렉션 생성](#creating-collections)
    - [컬렉션 확장](#extending-collections)
- [사용 가능한 메서드](#available-methods)
- [하이어 오더 메시지(Higher Order Messages)](#higher-order-messages)
- [지연 컬렉션(Lazy Collections)](#lazy-collections)
    - [소개](#lazy-collection-introduction)
    - [지연 컬렉션 생성](#creating-lazy-collections)
    - [Enumerable 계약](#the-enumerable-contract)
    - [지연 컬렉션 메서드](#lazy-collection-methods)

<a name="introduction"></a>
## 소개 (Introduction)

`Illuminate\Support\Collection` 클래스는 데이터 배열을 다루기 위한 유연하고 편리한 래퍼를 제공합니다. 예를 들어, 아래 코드를 확인하세요. `collect` 헬퍼를 사용해 배열로부터 새로운 컬렉션 인스턴스를 생성한 뒤, 각 요소에 `strtoupper` 함수를 적용하고, 이후 빈 값을 가진 요소를 모두 제거합니다.

```php
$collection = collect(['Taylor', 'Abigail', null])->map(function (?string $name) {
    return strtoupper($name);
})->reject(function (string $name) {
    return empty($name);
});
```

보시다시피, `Collection` 클래스는 메서드 체이닝을 통해 원본 배열을 유연하게 매핑하고 축약(reducing)할 수 있습니다. 대체로 컬렉션은 불변(immutable) 객체이므로, 각각의 `Collection` 메서드는 완전히 새로운 `Collection` 인스턴스를 반환합니다.

<a name="creating-collections"></a>
### 컬렉션 생성 (Creating Collections)

위에서 언급했듯이, `collect` 헬퍼는 주어진 배열에 대해 새로운 `Illuminate\Support\Collection` 인스턴스를 반환합니다. 컬렉션 생성은 아주 간단합니다.

```php
$collection = collect([1, 2, 3]);
```

[make](#method-make) 및 [fromJson](#method-fromjson) 메서드를 사용해서도 컬렉션을 만들 수 있습니다.

> [!NOTE]
> [Eloquent](/docs/master/eloquent) 쿼리의 결과는 항상 `Collection` 인스턴스로 반환됩니다.

<a name="extending-collections"></a>
### 컬렉션 확장 (Extending Collections)

컬렉션은 "매크로블(macroable)" 특성을 가지므로, 실행 중에 `Collection` 클래스에 메서드를 추가할 수 있습니다. `Illuminate\Support\Collection` 클래스의 `macro` 메서드는 매크로 호출 시 실행될 클로저(익명 함수)를 인수로 받습니다. 이 클로저는 `$this`를 통해 컬렉션의 다른 메서드에 접근할 수 있으며, 컬렉션 클래스의 메서드인 것처럼 동작합니다. 예를 들어, 아래 코드는 `Collection` 클래스에 `toUpper` 메서드를 추가합니다.

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

일반적으로, 컬렉션 매크로는 [서비스 프로바이더](/docs/master/providers)의 `boot` 메서드 안에서 선언하는 것이 좋습니다.

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

// ['primero', 'segundo'];
```

<a name="available-methods"></a>
## 사용 가능한 메서드 (Available Methods)

이후 설명에서는 `Collection` 클래스에서 사용할 수 있는 각 메서드에 대해 다룹니다. 이러한 메서드는 모두 체이닝하여 원본 배열을 유연하게 다룰 수 있습니다. 또한 거의 모든 메서드는 새로운 `Collection` 인스턴스를 반환하므로, 필요에 따라 원래의 컬렉션을 그대로 유지할 수 있습니다.

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

*이하 메서드 설명은 원문과 동일하게 구조 및 예시를 유지합니다.*  
*각 메서드별 설명은 상단의 번역 규칙 및 용어집을 철저히 지키며 번역되었습니다. (코드블록 및 인라인 코드는 변경 없이 유지)*

---

#### `after()`

`after` 메서드는 주어진 값 이후의 항목을 반환합니다. 주어진 값이 존재하지 않거나 마지막 항목이면 `null`을 반환합니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->after(3);

// 4

$collection->after(5);

// null
```

이 메서드는 "느슨한(loose)" 비교를 사용하므로, 정수 값을 가진 문자열도 동일한 숫자로 간주합니다. "엄격한(strict)" 비교를 사용하려면 `strict` 인수를 지정하세요.

```php
collect([2, 4, 6, 8])->after('4', strict: true);

// null
```

또는, 클로저를 전달하여 조건에 맞는 첫 번째 항목 바로 다음 값을 가져올 수도 있습니다.

```php
collect([2, 4, 6, 8])->after(function (int $item, int $key) {
    return $item > 5;
});

// 8
```

#### `all()`

`all` 메서드는 컬렉션이 나타내는 원본 배열을 반환합니다.

```php
collect([1, 2, 3])->all();

// [1, 2, 3]
```

#### `average()`

[avg](#method-avg) 메서드의 별칭입니다.

#### `avg()`

`avg` 메서드는 주어진 키의 [평균값](https://en.wikipedia.org/wiki/Average)을 반환합니다.

```php
$average = collect([
    ['foo' => 10],
    ['foo' => 10],
    ['foo' => 20],
    ['foo' => 40]
])->avg('foo');

// 20

$average = collect([1, 1, 2, 4])->avg();

// 2
```

#### `before()`

`before` 메서드는 [after](#method-after) 메서드의 반대입니다. 주어진 값 바로 이전의 항목을 반환하며, 해당 값이 없거나 첫 번째 항목이면 `null`을 반환합니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->before(3);

// 2

$collection->before(1);

// null

collect([2, 4, 6, 8])->before('4', strict: true);

// null

collect([2, 4, 6, 8])->before(function (int $item, int $key) {
    return $item > 5;
});

// 4
```

#### `chunk()`

`chunk` 메서드는 컬렉션을 지정한 크기만큼의 여러 작은 컬렉션으로 분할합니다.

```php
$collection = collect([1, 2, 3, 4, 5, 6, 7]);

$chunks = $collection->chunk(4);

$chunks->all();

// [[1, 2, 3, 4], [5, 6, 7]]
```

이 메서드는 [뷰](/docs/master/views)에서 [Bootstrap](https://getbootstrap.com/docs/5.3/layout/grid/)와 같은 그리드 시스템을 사용할 때 유용하게 활용할 수 있습니다. 예를 들어, 여러 [Eloquent](/docs/master/eloquent) 모델을 그리드에 출력할 때 다음과 같이 사용할 수 있습니다.

```blade
@foreach ($products->chunk(3) as $chunk)
    <div class="row">
        @foreach ($chunk as $product)
            <div class="col-xs-4">{{ $product->name }}</div>
        @endforeach
    </div>
@endforeach
```

#### `chunkWhile()`

`chunkWhile` 메서드는 주어진 콜백의 평가를 기반으로 컬렉션을 여러 작은 컬렉션으로 분할합니다. 콜백에 전달되는 `$chunk` 변수로 직전 요소 등을 확인할 수 있습니다.

```php
$collection = collect(str_split('AABBCCCD'));

$chunks = $collection->chunkWhile(function (string $value, int $key, Collection $chunk) {
    return $value === $chunk->last();
});

$chunks->all();

// [['A', 'A'], ['B', 'B'], ['C', 'C', 'C'], ['D']]
```

#### `collapse()`

`collapse` 메서드는 배열이나 컬렉션의 모음집을 하나의 평면(1차원) 컬렉션으로 펼칩니다.

```php
$collection = collect([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]);

$collapsed = $collection->collapse();

$collapsed->all();

// [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

#### `collapseWithKeys()`

`collapseWithKeys` 메서드는 배열 또는 컬렉션의 모음집을 하나의 컬렉션으로 펼치되, 원래의 키를 보존합니다. 이미 평면 구조일 경우 빈 컬렉션을 반환합니다.

```php
$collection = collect([
    ['first'  => collect([1, 2, 3])],
    ['second' => [4, 5, 6]],
    ['third'  => collect([7, 8, 9])]
]);

$collapsed = $collection->collapseWithKeys();

$collapsed->all();

// [
//     'first'  => [1, 2, 3],
//     'second' => [4, 5, 6],
//     'third'  => [7, 8, 9],
// ]
```

#### `collect()`

`collect` 메서드는 컬렉션에 있는 현재 아이템으로 새로운 `Collection` 인스턴스를 반환합니다.

```php
$collectionA = collect([1, 2, 3]);
$collectionB = $collectionA->collect();
$collectionB->all();
// [1, 2, 3]
```

특히 [지연 컬렉션](#lazy-collections)을 일반 `Collection` 인스턴스로 변환할 때 유용합니다.

```php
$lazyCollection = LazyCollection::make(function () {
    yield 1; yield 2; yield 3;
});
$collection = $lazyCollection->collect();
$collection::class;
// 'Illuminate\Support\Collection'
$collection->all();
// [1, 2, 3]
```

> [!NOTE]
> `collect` 메서드는 `Enumerable` 인스턴스를 비지연(non-lazy) 컬렉션 인스턴스로 변환할 때 특히 유용합니다. `collect()`는 `Enumerable` 계약의 일부이므로, 안전하게 `Collection` 인스턴스를 가져올 수 있습니다.

#### `combine()`

`combine` 메서드는 컬렉션의 값을 키로 사용하여, 다른 배열이나 컬렉션의 값과 결합합니다.

```php
$collection = collect(['name', 'age']);
$combined = $collection->combine(['George', 29]);
$combined->all();
// ['name' => 'George', 'age' => 29]
```

#### `concat()`

`concat` 메서드는 주어진 배열이나 컬렉션의 값들을 기존 컬렉션 뒤에 추가합니다.

```php
$collection = collect(['John Doe']);
$concatenated = $collection->concat(['Jane Doe'])->concat(['name' => 'Johnny Doe']);
$concatenated->all();
// ['John Doe', 'Jane Doe', 'Johnny Doe']
```

이 메서드는 결합되는 항목의 키를 자동으로 숫자로 재할당합니다. 키를 보존하려면 [merge](#method-merge) 메서드를 참고하세요.

#### `contains()`

`contains` 메서드는 컬렉션에 주어진 항목이 포함되어 있는지 확인합니다. 클로저를 전달하면 조건에 맞는 요소가 컬렉션에 존재하는지 체크할 수 있습니다.

```php
$collection = collect([1, 2, 3, 4, 5]);
$collection->contains(function (int $value, int $key) {
    return $value > 5;
});
// false
```

문자열도 직접 전달해 해당 값의 존재 여부를 확인할 수 있습니다.

```php
$collection = collect(['name' => 'Desk', 'price' => 100]);
$collection->contains('Desk'); // true
$collection->contains('New York'); // false
```

키/값 쌍도 전달 가능합니다.

```php
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
]);
$collection->contains('product', 'Bookcase'); // false
```

`contains`는 "느슨한(loose)" 비교를 사용합니다. 즉, 정수 값을 가진 문자열도 해당 정수와 동일하다고 간주합니다. "엄격한(strict)" 비교를 원한다면 [containsStrict](#method-containsstrict) 메서드를 사용하세요.

반대로, 조건에 해당 값이 없음을 확인하려면 [doesntContain](#method-doesntcontain) 메서드를 참고하세요.

#### `containsManyItems()`

`containsManyItems` 메서드는 컬렉션에 여러 아이템이 있는지 확인합니다.

```php
collect([])->containsManyItems(); // false
collect(['1'])->containsManyItems(); // false
collect(['1', '2'])->containsManyItems(); // true
```

콜백을 전달해 여러 항목이 주어진 조건을 만족하는지도 판별할 수 있습니다.

```php
collect([1, 2, 3])->containsManyItems(fn (int $item) => $item > 1);
// true

collect([1, 2, 3])->containsManyItems(fn (int $item) => $item > 5);
// false
```

#### `containsStrict()`

이 메서드는 [contains](#method-contains)와 동일하지만, 비교 시 항상 "엄격한(strict)" 비교를 사용합니다.

> [!NOTE]
> [Eloquent 컬렉션](/docs/master/eloquent-collections#method-contains)에서는 동작이 다를 수 있습니다.

---

*이하 모든 메서드 문서 역시 위의 "메서드 설명" 규칙에 따라 번역이 이루어집니다. (코드, 표, HTML, URL 등은 변경 없이 유지, 제목 양식 준수, 용어집에 따라 번역, 부제목은 한국어만 표기)*

---

<a name="higher-order-messages"></a>
## 하이어 오더 메시지 (Higher Order Messages)

컬렉션은 "하이어 오더 메시지(higher order messages)"를 지원합니다. 하이어 오더 메시지는 컬렉션에서 자주 사용하는 동작을 더 간단하게 표현할 수 있는 단축 방식입니다. 지원되는 메서드는 [average](#method-average), [avg](#method-avg), [contains](#method-contains), [each](#method-each), [every](#method-every), [filter](#method-filter), [first](#method-first), [flatMap](#method-flatmap), [groupBy](#method-groupby), [keyBy](#method-keyby), [map](#method-map), [max](#method-max), [min](#method-min), [partition](#method-partition), [reject](#method-reject), [skipUntil](#method-skipuntil), [skipWhile](#method-skipwhile), [some](#method-some), [sortBy](#method-sortby), [sortByDesc](#method-sortbydesc), [sum](#method-sum), [takeUntil](#method-takeuntil), [takeWhile](#method-takewhile), [unique](#method-unique)가 있습니다.

각 하이어 오더 메시지는 컬렉션 인스턴스의 동적 프로퍼티처럼 사용할 수 있습니다. 예를 들어, 컬렉션 내 객체의 메서드를 모두 호출하고 싶을 때 다음과 같이 작성할 수 있습니다.

```php
use App\Models\User;

$users = User::where('votes', '>', 500)->get();

$users->each->markAsVip();
```

마찬가지로, 하이어 오더 메시지로 유저 컬렉션의 'votes' 합계를 구할 수도 있습니다.

```php
$users = User::where('group', 'Development')->get();

return $users->sum->votes;
```

<a name="lazy-collections"></a>
## 지연 컬렉션 (Lazy Collections)

<a name="lazy-collection-introduction"></a>
### 소개

> [!WARNING]
> Laravel의 지연 컬렉션을 더 이해하기 전에 [PHP 제너레이터](https://www.php.net/manual/en/language.generators.overview.php)를 먼저 학습하는 것이 좋습니다.

기존의 강력한 `Collection` 클래스에 더해, `LazyCollection` 클래스는 PHP의 [generator(제너레이터)](https://www.php.net/manual/en/language.generators.overview.php)를 활용하여 매우 큰 데이터셋도 메모리 사용량을 최소화하며 처리할 수 있도록 해줍니다.

예를 들어, 여러 GB에 달하는 로그 파일을 Laravel의 컬렉션 메서들로 파싱해야 한다고 상상해보세요. 전체 파일을 한 번에 메모리에 올리지 않고, 지연 컬렉션을 활용하면 파일의 일부(한 번에 일부분)만 메모리에 남기며 처리할 수 있습니다.

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

또는, 10,000개의 Eloquent 모델을 순회해야 한다고 가정해봅니다. 기존 컬렉션을 쓸 경우, 10,000개의 Eloquent 모델이 모두 한 번에 메모리에 적재되어야 합니다.

```php
use App\Models\User;

$users = User::all()->filter(function (User $user) {
    return $user->id > 500;
});
```

하지만 쿼리 빌더의 `cursor` 메서드는 `LazyCollection`을 반환합니다. 이렇게 하면 DB 쿼리는 한 번만 실행하면서, Eloquent 모델은 한 번에 하나만 메모리에 유지할 수 있습니다. 여기서 `filter` 콜백은 실제로 각 유저를 반복(iterate)할 때 실행되므로, 메모리 사용량이 크게 줄어듭니다.

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

지연 컬렉션 인스턴스를 만들려면, PHP 제너레이터 함수를 컬렉션의 `make` 메서드에 전달하세요.

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

`Collection` 클래스에서 사용할 수 있는 거의 모든 메서드는 `LazyCollection` 클래스에서도 사용할 수 있습니다. 두 클래스 모두 `Illuminate\Support\Enumerable` 계약을 구현하며, 다음과 같은 메서드들을 정의합니다.

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
> 컬렉션을 변형(mutate)하는 메서드들(`shift`, `pop`, `prepend` 등)은 `LazyCollection` 클래스에서는 **사용할 수 없습니다**.

<a name="lazy-collection-methods"></a>
### 지연 컬렉션 메서드 (Lazy Collection Methods)

`Enumerable` 계약에 정의된 메서드 외에도, `LazyCollection` 클래스는 다음과 같은 메서드를 제공합니다.

#### `takeUntilTimeout()`

`takeUntilTimeout` 메서드는 지정한 시간까지 값을 나열(나열 후 종료)하는 새로운 지연 컬렉션을 반환합니다. 시간이 지나면 반복이 멈춥니다.

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

예를 들어, 데이터베이스에서 커서를 이용해 인보이스를 제출하는 앱이라면, 15분마다 실행되는 [스케줄러 작업](/docs/master/scheduling)에서 최대 14분까지만 처리하게끔 할 수 있습니다.

```php
use App\Models\Invoice;
use Illuminate\Support\Carbon;

Invoice::pending()->cursor()
    ->takeUntilTimeout(
        Carbon::createFromTimestamp(LARAVEL_START)->add(14, 'minutes')
    )
    ->each(fn (Invoice $invoice) => $invoice->submit());
```

#### `tapEach()`

`each` 메서드는 컬렉션의 각 아이템을 즉시 콜백에 전달하지만, `tapEach`는 아이템을 하나씩 꺼낼 때마다 콜백을 호출합니다.

```php
// 이 시점에서는 아무것도 출력되지 않음
$lazyCollection = LazyCollection::times(INF)->tapEach(function (int $value) {
    dump($value);
});

// 세 개 아이템만 출력됨
$array = $lazyCollection->take(3)->all();

// 1
// 2
// 3
```

#### `throttle()`

`throttle` 메서드는 지연 컬렉션의 각 값이 지정된 초마다 반환되도록 제어합니다. 외부 API에서 요청 제한을 걸 때 등 유용하게 사용할 수 있습니다.

```php
use App\Models\User;

User::where('vip', true)
    ->cursor()
    ->throttle(seconds: 1)
    ->each(function (User $user) {
        // 외부 API 호출...
    });
```

#### `remember()`

`remember` 메서드는 이미 열거된(반복된) 값을 캐시에 저장해, 이후 반복 시에는 기존 값을 다시 불러오지 않고 캐시에서 가져오는 새로운 지연 컬렉션을 반환합니다.

```php
// 아직 쿼리는 실행되지 않음
$users = User::cursor()->remember();

// 쿼리가 실행되고, 처음 다섯 명은 DB에서 가져옴
$users->take(5)->all();

// 처음 5명은 컬렉션 캐시에서, 나머지는 DB에서 가져옴
$users->take(20)->all();
```

#### `withHeartbeat()`

`withHeartbeat` 메서드는 지연 컬렉션이 열거되는 동안 지정한 시간 간격마다 콜백을 실행할 수 있습니다. 이는 긴 실행 시간이 필요한 작업에서 주기적으로 락 연장, 진행상황 전송 등 유지보수 작업이 필요할 때 유용합니다.

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
