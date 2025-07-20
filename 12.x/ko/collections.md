# 컬렉션(Collections)

- [소개](#introduction)
    - [컬렉션 생성하기](#creating-collections)
    - [컬렉션 확장하기](#extending-collections)
- [사용 가능한 메서드](#available-methods)
- [하이오더 메시지(Higher Order Messages)](#higher-order-messages)
- [지연 컬렉션(Lazy Collections)](#lazy-collections)
    - [소개](#lazy-collection-introduction)
    - [지연 컬렉션 생성하기](#creating-lazy-collections)
    - [Enumerable 계약](#the-enumerable-contract)
    - [지연 컬렉션 메서드](#lazy-collection-methods)

<a name="introduction"></a>
## 소개

`Illuminate\Support\Collection` 클래스는 데이터 배열을 다룰 때 유창하고 편리한 래퍼를 제공합니다. 예를 들어, 아래 코드를 확인해 보세요. `collect` 헬퍼로 배열에서 새로운 컬렉션 인스턴스를 만들고, 각 요소에 `strtoupper` 함수를 적용한 뒤, 비어 있는 값을 모두 제거합니다.

```php
$collection = collect(['Taylor', 'Abigail', null])->map(function (?string $name) {
    return strtoupper($name);
})->reject(function (string $name) {
    return empty($name);
});
```

보시는 것처럼, `Collection` 클래스는 메서드 체이닝을 통해 배열을 유연하게 매핑하거나 축소(map, reduce)하는 작업을 할 수 있도록 해줍니다. 일반적으로 컬렉션은 불변(immutable) 객체이기 때문에, 대부분의 `Collection` 메서드는 완전히 새로운 `Collection` 인스턴스를 반환합니다.

<a name="creating-collections"></a>
### 컬렉션 생성하기

위에서 언급했듯이, `collect` 헬퍼는 주어진 배열을 기반으로 새로운 `Illuminate\Support\Collection` 인스턴스를 반환합니다. 따라서 컬렉션을 생성하는 방법은 매우 간단합니다.

```php
$collection = collect([1, 2, 3]);
```

또한 [make](#method-make) 및 [fromJson](#method-fromjson) 메서드를 사용해 컬렉션을 만들 수도 있습니다.

> [!NOTE]
> [Eloquent](/docs/12.x/eloquent) 쿼리의 결과는 항상 `Collection` 인스턴스로 반환됩니다.

<a name="extending-collections"></a>
### 컬렉션 확장하기

컬렉션은 "매크로 가능(macroable)"합니다. 즉, 런타임 시점에 추가적인 메서드를 `Collection` 클래스에 동적으로 등록해서 사용할 수 있습니다. `Illuminate\Support\Collection` 클래스의 `macro` 메서드는 매크로 호출 시 실행될 클로저(익명 함수)를 인자로 받습니다. 이 클로저 내부에서는 `$this`를 통해 컬렉션의 다른 메서드에 접근할 수 있으므로, 실제 컬렉션 메서드처럼 동작합니다. 예를 들어, 아래 코드는 `Collection` 클래스에 `toUpper`라는 메서드를 추가합니다.

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

일반적으로 컬렉션 매크로는 [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드 안에서 선언하는 것이 좋습니다.

<a name="macro-arguments"></a>
#### 매크로 인수

필요하다면, 추가 인수를 받을 수 있는 매크로도 정의할 수 있습니다.

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
## 사용 가능한 메서드

이후 문서에서 다루는 대부분의 내용은 `Collection` 클래스에서 사용할 수 있는 메서드들입니다. 이 모든 메서드는 메서드 체이닝 방식으로 배열을 유연하게 조작할 수 있도록 제공됩니다. 또한 거의 모든 메서드는 새로운 `Collection` 인스턴스를 반환하므로, 원본 컬렉션을 그대로 보존할 수 있습니다.



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
## 메서드 목록



<a name="method-after"></a>
#### `after()`

`after` 메서드는 지정한 값 바로 다음에 위치한 아이템을 반환합니다. 만약 지정한 값이 컬렉션 내에 없거나 마지막 아이템이면 `null`을 반환합니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->after(3);

// 4

$collection->after(5);

// null
```

이 메서드는 "느슨한(loose)" 비교를 사용해서 지정된 항목을 찾습니다. 즉, 정수 값을 가진 문자열은 같은 값을 가진 정수와 동일하게 간주됩니다. "엄격한(strict)" 비교를 사용하려면, `strict` 인수를 메서드에 전달할 수 있습니다.

```php
collect([2, 4, 6, 8])->after('4', strict: true);

// null
```

또는, 콜렉션 내에서 원하는 조건을 만족하는 첫 번째 아이템을 찾기 위해 직접 클로저를 전달할 수도 있습니다.

```php
collect([2, 4, 6, 8])->after(function (int $item, int $key) {
    return $item > 5;
});

// 8
```

<a name="method-all"></a>
#### `all()`

`all` 메서드는 컬렉션이 가지고 있는 원본 배열을 반환합니다.

```php
collect([1, 2, 3])->all();

// [1, 2, 3]
```

<a name="method-average"></a>
#### `average()`

[avg](#method-avg) 메서드의 별칭(alias)입니다.

<a name="method-avg"></a>
#### `avg()`

`avg` 메서드는 지정한 키의 [평균값](https://en.wikipedia.org/wiki/Average)을 반환합니다.

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

<a name="method-before"></a>
#### `before()`

`before` 메서드는 [after](#method-after) 메서드와 반대로 동작합니다. 지정한 값 바로 *이전*에 위치하는 아이템을 반환합니다. 만약 지정한 값이 컬렉션 내에 없거나 첫 번째 아이템이면 `null`을 반환합니다.

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

<a name="method-chunk"></a>
#### `chunk()`

`chunk` 메서드는 컬렉션을 지정한 크기로 여러 개의 작은 컬렉션으로 분할합니다.

```php
$collection = collect([1, 2, 3, 4, 5, 6, 7]);

$chunks = $collection->chunk(4);

$chunks->all();

// [[1, 2, 3, 4], [5, 6, 7]]
```

이 메서드는 [뷰](/docs/12.x/views)에서 [Bootstrap](https://getbootstrap.com/docs/5.3/layout/grid/) 같은 그리드 시스템을 사용할 때 특히 유용합니다. 예를 들어, [Eloquent](/docs/12.x/eloquent) 모델 컬렉션을 그리드 형태로 보여주려 할 때 사용할 수 있습니다.

```blade
@foreach ($products->chunk(3) as $chunk)
    <div class="row">
        @foreach ($chunk as $product)
            <div class="col-xs-4">{{ $product->name }}</div>
        @endforeach
    </div>
@endforeach
```

<a name="method-chunkwhile"></a>
#### `chunkWhile()`

`chunkWhile` 메서드는 전달한 콜백의 평가 결과에 따라 컬렉션을 여러 개의 작은 컬렉션으로 분할합니다. 클로저에 전달되는 `$chunk` 변수는 이전 요소를 확인할 때 사용할 수 있습니다.

```php
$collection = collect(str_split('AABBCCCD'));

$chunks = $collection->chunkWhile(function (string $value, int $key, Collection $chunk) {
    return $value === $chunk->last();
});

$chunks->all();

// [['A', 'A'], ['B', 'B'], ['C', 'C', 'C'], ['D']]
```

<a name="method-collapse"></a>
#### `collapse()`

`collapse` 메서드는 배열이나 컬렉션의 컬렉션을 하나의 평평한(flat) 컬렉션으로 합쳐줍니다.

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

<a name="method-collapsewithkeys"></a>
#### `collapseWithKeys()`

`collapseWithKeys` 메서드는 배열 또는 컬렉션의 컬렉션을 하나의 컬렉션으로 합치면서, 원본 키를 그대로 유지합니다. 이미 평평한 컬렉션일 경우, 빈 컬렉션을 반환합니다.

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

<a name="method-collect"></a>
#### `collect()`

`collect` 메서드는 컬렉션에 있는 아이템으로 새로운 `Collection` 인스턴스를 반환합니다.

```php
$collectionA = collect([1, 2, 3]);

$collectionB = $collectionA->collect();

$collectionB->all();

// [1, 2, 3]
```

`collect` 메서드는 [지연 컬렉션](#lazy-collections)을 일반적인 `Collection` 인스턴스로 변환할 때 주로 사용됩니다.

```php
$lazyCollection = LazyCollection::make(function () {
    yield 1;
    yield 2;
    yield 3;
});

$collection = $lazyCollection->collect();

$collection::class;

// 'Illuminate\Support\Collection'

$collection->all();

// [1, 2, 3]
```

> [!NOTE]
> `collect` 메서드는 `Enumerable` 인스턴스를 비-지연 컬렉션 인스턴스로 변환해야 할 때 유용하게 사용할 수 있습니다. `collect()`는 `Enumerable` 계약의 일부이므로, 안전하게 `Collection` 인스턴스를 얻는 데 사용할 수 있습니다.

<a name="method-combine"></a>
#### `combine()`

`combine` 메서드는 컬렉션의 값을 키로 사용하고, 다른 배열 또는 컬렉션의 값을 값으로 사용하여 조합합니다.

```php
$collection = collect(['name', 'age']);

$combined = $collection->combine(['George', 29]);

$combined->all();

// ['name' => 'George', 'age' => 29]
```

<a name="method-concat"></a>
#### `concat()`

`concat` 메서드는 주어진 배열 또는 컬렉션의 값을 현재 컬렉션의 끝부분에 이어서 추가합니다.

```php
$collection = collect(['John Doe']);

$concatenated = $collection->concat(['Jane Doe'])->concat(['name' => 'Johnny Doe']);

$concatenated->all();

// ['John Doe', 'Jane Doe', 'Johnny Doe']
```

`concat` 메서드는 기존 컬렉션에 이어 붙인 항목들의 키를 숫자로 재인덱싱합니다. 연관 배열(associative collection)의 키를 유지하려면 [merge](#method-merge) 메서드를 사용하세요.

<a name="method-contains"></a>
#### `contains()`

`contains` 메서드는 컬렉션에 주어진 값이 포함되어 있는지 확인합니다. 콜백을 전달하여, 특정 조건을 만족하는 값이 존재하는지 판단할 수도 있습니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->contains(function (int $value, int $key) {
    return $value > 5;
});

// false
```

또는, 문자열을 전달해서 해당 값이 존재하는지 확인할 수 있습니다.

```php
$collection = collect(['name' => 'Desk', 'price' => 100]);

$collection->contains('Desk');

// true

$collection->contains('New York');

// false
```

키/값 형태로 전달해서, 주어진 쌍이 존재하는지도 확인할 수 있습니다.

```php
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
]);

$collection->contains('product', 'Bookcase');

// false
```

`contains` 메서드는 값 비교 시 "느슨한(loose)" 비교를 사용합니다. 즉, 정수 값을 가진 문자열은 같은 값을 가진 정수와 동일하게 취급됩니다. "엄격한(strict)" 비교를 하고 싶다면 [containsStrict](#method-containsstrict) 메서드를 사용하세요.

`contains`의 반대 동작을 하려면 [doesntContain](#method-doesntcontain) 메서드를 참조하세요.

<a name="method-containsoneitem"></a>
#### `containsOneItem()`

`containsOneItem` 메서드는 컬렉션에 하나의 아이템만 포함되어 있는지 확인합니다.

```php
collect([])->containsOneItem();

// false

collect(['1'])->containsOneItem();

// true

collect(['1', '2'])->containsOneItem();

// false

collect([1, 2, 3])->containsOneItem(fn (int $item) => $item === 2);

// true
```

<a name="method-containsstrict"></a>
#### `containsStrict()`

이 메서드는 [contains](#method-contains)와 동일한 시그니처를 가지지만, 값 비교 시 항상 "엄격한(strict)" 비교를 사용합니다.

> [!NOTE]
> [Eloquent 컬렉션](/docs/12.x/eloquent-collections#method-contains)에서 이 메서드의 동작이 달라집니다.

<a name="method-count"></a>
#### `count()`

`count` 메서드는 컬렉션 속 아이템의 총 개수를 반환합니다.

```php
$collection = collect([1, 2, 3, 4]);

$collection->count();

// 4
```

<a name="method-countBy"></a>
#### `countBy()`

`countBy` 메서드는 컬렉션 내 값의 등장 횟수를 세어줍니다. 기본적으로는 모든 아이템의 등장 횟수를 세어서, 컬렉션 내 특정 "유형"의 개수를 셀 때 사용할 수 있습니다.

```php
$collection = collect([1, 2, 2, 2, 3]);

$counted = $collection->countBy();

$counted->all();

// [1 => 1, 2 => 3, 3 => 1]
```

콜백을 전달해서, 임의의 값으로 집계하는 것도 가능합니다.

```php
$collection = collect(['alice@gmail.com', 'bob@yahoo.com', 'carlos@gmail.com']);

$counted = $collection->countBy(function (string $email) {
    return substr(strrchr($email, '@'), 1);
});

$counted->all();

// ['gmail.com' => 2, 'yahoo.com' => 1]
```

<a name="method-crossjoin"></a>
#### `crossJoin()`

`crossJoin` 메서드는 컬렉션의 값들과 지정한 배열 또는 컬렉션들의 값을 교차 결합하여, 모든 가능한 조합의 데카르트 곱(Cartesian product)을 반환합니다.

```php
$collection = collect([1, 2]);

$matrix = $collection->crossJoin(['a', 'b']);

$matrix->all();

/*
    [
        [1, 'a'],
        [1, 'b'],
        [2, 'a'],
        [2, 'b'],
    ]
*/

$collection = collect([1, 2]);

$matrix = $collection->crossJoin(['a', 'b'], ['I', 'II']);

$matrix->all();

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
```

<a name="method-dd"></a>
#### `dd()`

`dd` 메서드는 컬렉션의 아이템을 덤프(dump)한 뒤, 스크립트 실행을 중단시킵니다.

```php
$collection = collect(['John Doe', 'Jane Doe']);

$collection->dd();

/*
    array:2 [
        0 => "John Doe"
        1 => "Jane Doe"
    ]
*/
```

스크립트 실행을 멈추고 싶지 않다면, [dump](#method-dump) 메서드를 대신 사용하세요.

<a name="method-diff"></a>
#### `diff()`

`diff` 메서드는 다른 컬렉션이나 일반 PHP `array`와 값을 기준으로 비교합니다. 기존 컬렉션에만 있고 주어진 비교 대상에는 없는 값들만 반환합니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$diff = $collection->diff([2, 4, 6, 8]);

$diff->all();

// [1, 3, 5]
```

> [!NOTE]
> [Eloquent 컬렉션](/docs/12.x/eloquent-collections#method-diff)에서 이 메서드의 동작이 달라집니다.

<a name="method-diffassoc"></a>

#### `diffAssoc()`

`diffAssoc` 메서드는 컬렉션과 다른 컬렉션 또는 일반 PHP `array`를 키와 값 기준으로 비교합니다. 이 메서드는 주어진 컬렉션에 없는 원본 컬렉션의 키/값 쌍을 반환합니다.

```php
$collection = collect([
    'color' => 'orange',
    'type' => 'fruit',
    'remain' => 6,
]);

$diff = $collection->diffAssoc([
    'color' => 'yellow',
    'type' => 'fruit',
    'remain' => 3,
    'used' => 6,
]);

$diff->all();

// ['color' => 'orange', 'remain' => 6]
```

<a name="method-diffassocusing"></a>
#### `diffAssocUsing()`

`diffAssoc`와 달리, `diffAssocUsing`은 인덱스 비교에 사용자가 정의한 콜백 함수를 인자로 받을 수 있습니다.

```php
$collection = collect([
    'color' => 'orange',
    'type' => 'fruit',
    'remain' => 6,
]);

$diff = $collection->diffAssocUsing([
    'Color' => 'yellow',
    'Type' => 'fruit',
    'Remain' => 3,
], 'strnatcasecmp');

$diff->all();

// ['color' => 'orange', 'remain' => 6]
```

콜백 함수는 반드시 정수형(음수, 0, 양수)을 반환하는 비교 함수여야 합니다. 자세한 내용은 PHP 문서의 [array_diff_uassoc](https://www.php.net/array_diff_uassoc#refsect1-function.array-diff-uassoc-parameters) 항목을 참고하세요. 이 메서드는 내부적으로 해당 PHP 함수를 사용합니다.

<a name="method-diffkeys"></a>
#### `diffKeys()`

`diffKeys` 메서드는 컬렉션과 다른 컬렉션 또는 일반 PHP `array`를 키 기준으로 비교합니다. 이 메서드는 주어진 컬렉션에 없는 원본 컬렉션의 키/값 쌍을 반환합니다.

```php
$collection = collect([
    'one' => 10,
    'two' => 20,
    'three' => 30,
    'four' => 40,
    'five' => 50,
]);

$diff = $collection->diffKeys([
    'two' => 2,
    'four' => 4,
    'six' => 6,
    'eight' => 8,
]);

$diff->all();

// ['one' => 10, 'three' => 30, 'five' => 50]
```

<a name="method-doesntcontain"></a>
#### `doesntContain()`

`doesntContain` 메서드는 컬렉션에 지정한 값이 포함되어 있지 않은지를 확인합니다. 클로저를 전달하면, 특정 조건에 맞는 요소가 컬렉션에 존재하지 않는지를 판별합니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->doesntContain(function (int $value, int $key) {
    return $value < 5;
});

// false
```

또는, 문자열을 전달하여 컬렉션에 해당 값이 포함되어 있지 않은지를 확인할 수 있습니다.

```php
$collection = collect(['name' => 'Desk', 'price' => 100]);

$collection->doesntContain('Table');

// true

$collection->doesntContain('Desk');

// false
```

키/값 쌍을 전달하면, 해당 키/값 쌍이 컬렉션에 존재하지 않는지도 확인할 수 있습니다.

```php
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
]);

$collection->doesntContain('product', 'Bookcase');

// true
```

`doesntContain` 메서드는 값 비교 시 "느슨한(loose)" 비교를 사용합니다. 즉, 문자열로 된 숫자와 정수 값이 같다면 동일하다고 간주합니다.

<a name="method-dot"></a>
#### `dot()`

`dot` 메서드는 다차원 컬렉션을 "dot" 표기법을 사용하여 1차원 컬렉션으로 평탄화(flatten)합니다.

```php
$collection = collect(['products' => ['desk' => ['price' => 100]]]);

$flattened = $collection->dot();

$flattened->all();

// ['products.desk.price' => 100]
```

<a name="method-dump"></a>
#### `dump()`

`dump` 메서드는 컬렉션의 항목들을 덤프(dump)하여 출력합니다.

```php
$collection = collect(['John Doe', 'Jane Doe']);

$collection->dump();

/*
    array:2 [
        0 => "John Doe"
        1 => "Jane Doe"
    ]
*/
```

컬렉션을 출력한 후 스크립트 실행을 중단하고 싶다면, [dd](#method-dd) 메서드를 사용하세요.

<a name="method-duplicates"></a>
#### `duplicates()`

`duplicates` 메서드는 컬렉션 내 중복된 값을 찾아 반환합니다.

```php
$collection = collect(['a', 'b', 'a', 'c', 'b']);

$collection->duplicates();

// [2 => 'a', 4 => 'b']
```

컬렉션에 배열이나 객체가 포함되어 있을 경우, 중복 체크를 원하는 속성의 키를 전달할 수 있습니다.

```php
$employees = collect([
    ['email' => 'abigail@example.com', 'position' => 'Developer'],
    ['email' => 'james@example.com', 'position' => 'Designer'],
    ['email' => 'victoria@example.com', 'position' => 'Developer'],
]);

$employees->duplicates('position');

// [2 => 'Developer']
```

<a name="method-duplicatesstrict"></a>
#### `duplicatesStrict()`

이 메서드는 [duplicates](#method-duplicates) 메서드와 시그니처는 동일하지만, 모든 값을 "엄격한(strict)" 비교로 판단합니다.

<a name="method-each"></a>
#### `each()`

`each` 메서드는 컬렉션의 각 항목을 순회하며, 각 항목을 클로저에 전달합니다.

```php
$collection = collect([1, 2, 3, 4]);

$collection->each(function (int $item, int $key) {
    // ...
});
```

순회 중에 반복을 중단하려면, 클로저에서 `false`를 반환하면 됩니다.

```php
$collection->each(function (int $item, int $key) {
    if (/* 조건 */) {
        return false;
    }
});
```

<a name="method-eachspread"></a>
#### `eachSpread()`

`eachSpread` 메서드는 컬렉션의 각 항목(중첩 배열일 경우 배열의 각 항목)을 분해하여, 각 값을 콜백의 인자로 전달하며 순회합니다.

```php
$collection = collect([['John Doe', 35], ['Jane Doe', 33]]);

$collection->eachSpread(function (string $name, int $age) {
    // ...
});
```

반복을 중단하려면 콜백에서 `false`를 반환하면 됩니다.

```php
$collection->eachSpread(function (string $name, int $age) {
    return false;
});
```

<a name="method-ensure"></a>
#### `ensure()`

`ensure` 메서드는 컬렉션의 모든 요소가 지정된 타입(또는 타입 리스트)에 속하는지 검증합니다. 조건에 맞지 않으면 `UnexpectedValueException`이 발생합니다.

```php
return $collection->ensure(User::class);

return $collection->ensure([User::class, Customer::class]);
```

`string`, `int`, `float`, `bool`, `array` 등의 기본 타입도 지정할 수 있습니다.

```php
return $collection->ensure('int');
```

> [!WARNING]
> `ensure` 메서드를 사용해도, 추후에 타입이 다른 요소가 컬렉션에 추가되는 것을 막지는 않습니다.

<a name="method-every"></a>
#### `every()`

`every` 메서드는 컬렉션의 모든 요소가 주어진 조건(클로저)을 만족하는지 검사합니다.

```php
collect([1, 2, 3, 4])->every(function (int $value, int $key) {
    return $value > 2;
});

// false
```

컬렉션이 비어 있는 경우, `every` 메서드는 true를 반환합니다.

```php
$collection = collect([]);

$collection->every(function (int $value, int $key) {
    return $value > 2;
});

// true
```

<a name="method-except"></a>
#### `except()`

`except` 메서드는 지정한 키를 제외한 컬렉션의 모든 항목을 반환합니다.

```php
$collection = collect(['product_id' => 1, 'price' => 100, 'discount' => false]);

$filtered = $collection->except(['price', 'discount']);

$filtered->all();

// ['product_id' => 1]
```

`except`의 반대 동작을 원한다면 [only](#method-only) 메서드를 참고하세요.

> [!NOTE]
> 이 메서드는 [Eloquent 컬렉션](/docs/12.x/eloquent-collections#method-except) 사용 시 동작이 다를 수 있습니다.

<a name="method-filter"></a>
#### `filter()`

`filter` 메서드는 주어진 콜백을 이용해 컬렉션에서 조건을 만족하는 항목만 남깁니다.

```php
$collection = collect([1, 2, 3, 4]);

$filtered = $collection->filter(function (int $value, int $key) {
    return $value > 2;
});

$filtered->all();

// [3, 4]
```

콜백을 지정하지 않을 경우, 컬렉션에서 `false`로 평가되는 모든 항목을 제거합니다.

```php
$collection = collect([1, 2, 3, null, false, '', 0, []]);

$collection->filter()->all();

// [1, 2, 3]
```

`filter`의 반대 동작을 원한다면 [reject](#method-reject) 메서드를 참고하세요.

<a name="method-first"></a>
#### `first()`

`first` 메서드는 주어진 조건을 만족하는 컬렉션의 첫 번째 요소를 반환합니다.

```php
collect([1, 2, 3, 4])->first(function (int $value, int $key) {
    return $value > 2;
});

// 3
```

인자를 전달하지 않으면 컬렉션의 첫 번째 요소를 반환하며, 컬렉션이 비어 있으면 `null`을 반환합니다.

```php
collect([1, 2, 3, 4])->first();

// 1
```

<a name="method-first-or-fail"></a>
#### `firstOrFail()`

`firstOrFail` 메서드는 `first`와 동일하나, 결과가 없을 경우 `Illuminate\Support\ItemNotFoundException` 예외를 발생시킵니다.

```php
collect([1, 2, 3, 4])->firstOrFail(function (int $value, int $key) {
    return $value > 5;
});

// ItemNotFoundException 예외 발생...
```

인자를 전달하지 않고 호출할 경우, 컬렉션의 첫 번째 항목을 반환합니다. 컬렉션이 비어 있으면 `Illuminate\Support\ItemNotFoundException` 예외가 발생합니다.

```php
collect([])->firstOrFail();

// ItemNotFoundException 예외 발생...
```

<a name="method-first-where"></a>
#### `firstWhere()`

`firstWhere` 메서드는 주어진 키/값 쌍과 일치하는 컬렉션의 첫 번째 요소를 반환합니다.

```php
$collection = collect([
    ['name' => 'Regena', 'age' => null],
    ['name' => 'Linda', 'age' => 14],
    ['name' => 'Diego', 'age' => 23],
    ['name' => 'Linda', 'age' => 84],
]);

$collection->firstWhere('name', 'Linda');

// ['name' => 'Linda', 'age' => 14]
```

비교 연산자를 추가로 넘겨 호출할 수도 있습니다.

```php
$collection->firstWhere('age', '>=', 18);

// ['name' => 'Diego', 'age' => 23]
```

[where](#method-where) 메서드와 마찬가지로, 인자를 하나만 전달할 수도 있습니다. 이 경우 해당 키 값이 "참(truthy)"인 첫 번째 항목이 반환됩니다.

```php
$collection->firstWhere('age');

// ['name' => 'Linda', 'age' => 14]
```

<a name="method-flatmap"></a>
#### `flatMap()`

`flatMap` 메서드는 컬렉션의 각 값을 클로저에 넘기며 순회합니다. 클로저에서 항목을 자유롭게 수정하여 반환할 수 있고, 수정된 각각의 항목이 한 단계만 평탄화(flatten)된 새로운 컬렉션이 반환됩니다.

```php
$collection = collect([
    ['name' => 'Sally'],
    ['school' => 'Arkansas'],
    ['age' => 28]
]);

$flattened = $collection->flatMap(function (array $values) {
    return array_map('strtoupper', $values);
});

$flattened->all();

// ['name' => 'SALLY', 'school' => 'ARKANSAS', 'age' => '28'];
```

<a name="method-flatten"></a>
#### `flatten()`

`flatten` 메서드는 다차원 컬렉션을 1차원 컬렉션으로 평탄화합니다.

```php
$collection = collect([
    'name' => 'Taylor',
    'languages' => [
        'PHP', 'JavaScript'
    ]
]);

$flattened = $collection->flatten();

$flattened->all();

// ['Taylor', 'PHP', 'JavaScript'];
```

필요하다면 `flatten` 메서드에 "depth"(깊이) 인자를 지정할 수 있습니다.

```php
$collection = collect([
    'Apple' => [
        [
            'name' => 'iPhone 6S',
            'brand' => 'Apple'
        ],
    ],
    'Samsung' => [
        [
            'name' => 'Galaxy S7',
            'brand' => 'Samsung'
        ],
    ],
]);

$products = $collection->flatten(1);

$products->values()->all();

/*
    [
        ['name' => 'iPhone 6S', 'brand' => 'Apple'],
        ['name' => 'Galaxy S7', 'brand' => 'Samsung'],
    ]
*/
```

이 예시에서 `flatten`을 깊이 인자 없이 호출하면, 중첩 배열까지 모두 평탄화되어 `['iPhone 6S', 'Apple', 'Galaxy S7', 'Samsung']`이 결과가 됩니다. depth(깊이)를 지정하면 몇 단계까지 평탄화할지 제어할 수 있습니다.

<a name="method-flip"></a>
#### `flip()`

`flip` 메서드는 컬렉션의 키와 값을 서로 맞바꿉니다.

```php
$collection = collect(['name' => 'Taylor', 'framework' => 'Laravel']);

$flipped = $collection->flip();

$flipped->all();

// ['Taylor' => 'name', 'Laravel' => 'framework']
```

<a name="method-forget"></a>
#### `forget()`

`forget` 메서드는 지정한 키에 해당하는 항목을 컬렉션에서 제거합니다.

```php
$collection = collect(['name' => 'Taylor', 'framework' => 'Laravel']);

// 단일 키 제거...
$collection->forget('name');

// ['framework' => 'Laravel']

// 여러 키 제거...
$collection->forget(['name', 'framework']);

// []
```

> [!WARNING]
> 대부분의 컬렉션 메서드와 달리, `forget`은 새로 수정된 컬렉션을 반환하지 않고, 호출된 컬렉션 자체를 변경합니다.

<a name="method-forpage"></a>
#### `forPage()`

`forPage` 메서드는 지정한 페이지 번호에 해당하는 항목만 포함하는 새로운 컬렉션을 반환합니다. 첫 번째 인자는 페이지 번호이며, 두 번째 인자는 페이지당 보여줄 항목 수입니다.

```php
$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9]);

$chunk = $collection->forPage(2, 3);

$chunk->all();

// [4, 5, 6]
```

<a name="method-fromjson"></a>
#### `fromJson()`

정적 메서드인 `fromJson`은 주어진 JSON 문자열을 PHP의 `json_decode` 함수로 디코딩하여, 새로운 컬렉션 인스턴스를 생성합니다.

```php
use Illuminate\Support\Collection;

$json = json_encode([
    'name' => 'Taylor Otwell',
    'role' => 'Developer',
    'status' => 'Active',
]);

$collection = Collection::fromJson($json);
```

<a name="method-get"></a>
#### `get()`

`get` 메서드는 주어진 키에 해당하는 항목을 반환합니다. 만약 해당 키가 존재하지 않으면, `null`을 반환합니다.

```php
$collection = collect(['name' => 'Taylor', 'framework' => 'Laravel']);

$value = $collection->get('name');

// Taylor
```

두 번째 인자로 기본값을 전달할 수도 있습니다.

```php
$collection = collect(['name' => 'Taylor', 'framework' => 'Laravel']);

$value = $collection->get('age', 34);

// 34
```

기본값으로 콜백을 전달하면, 해당 키가 없을 때 콜백의 반환값이 사용됩니다.

```php
$collection->get('email', function () {
    return 'taylor@example.com';
});

// taylor@example.com
```

<a name="method-groupby"></a>
#### `groupBy()`

`groupBy` 메서드는 컬렉션 항목을 주어진 키로 그룹화합니다.

```php
$collection = collect([
    ['account_id' => 'account-x10', 'product' => 'Chair'],
    ['account_id' => 'account-x10', 'product' => 'Bookcase'],
    ['account_id' => 'account-x11', 'product' => 'Desk'],
]);

$grouped = $collection->groupBy('account_id');

$grouped->all();

/*
    [
        'account-x10' => [
            ['account_id' => 'account-x10', 'product' => 'Chair'],
            ['account_id' => 'account-x10', 'product' => 'Bookcase'],
        ],
        'account-x11' => [
            ['account_id' => 'account-x11', 'product' => 'Desk'],
        ],
    ]
*/
```

문자열 키 대신 콜백을 전달하면, 그룹화에 사용할 값을 반환해야 합니다.

```php
$grouped = $collection->groupBy(function (array $item, int $key) {
    return substr($item['account_id'], -3);
});

$grouped->all();

/*
    [
        'x10' => [
            ['account_id' => 'account-x10', 'product' => 'Chair'],
            ['account_id' => 'account-x10', 'product' => 'Bookcase'],
        ],
        'x11' => [
            ['account_id' => 'account-x11', 'product' => 'Desk'],
        ],
    ]
*/
```

여러 단계로 그룹화하려면, 배열로 여러 기준을 넘길 수 있습니다. 배열의 각 요소는 다차원 배열 내에서 해당 단계별로 그룹화에 적용됩니다.

```php
$data = new Collection([
    10 => ['user' => 1, 'skill' => 1, 'roles' => ['Role_1', 'Role_3']],
    20 => ['user' => 2, 'skill' => 1, 'roles' => ['Role_1', 'Role_2']],
    30 => ['user' => 3, 'skill' => 2, 'roles' => ['Role_1']],
    40 => ['user' => 4, 'skill' => 2, 'roles' => ['Role_2']],
]);

$result = $data->groupBy(['skill', function (array $item) {
    return $item['roles'];
}], preserveKeys: true);

/*
[
    1 => [
        'Role_1' => [
            10 => ['user' => 1, 'skill' => 1, 'roles' => ['Role_1', 'Role_3']],
            20 => ['user' => 2, 'skill' => 1, 'roles' => ['Role_1', 'Role_2']],
        ],
        'Role_2' => [
            20 => ['user' => 2, 'skill' => 1, 'roles' => ['Role_1', 'Role_2']],
        ],
        'Role_3' => [
            10 => ['user' => 1, 'skill' => 1, 'roles' => ['Role_1', 'Role_3']],
        ],
    ],
    2 => [
        'Role_1' => [
            30 => ['user' => 3, 'skill' => 2, 'roles' => ['Role_1']],
        ],
        'Role_2' => [
            40 => ['user' => 4, 'skill' => 2, 'roles' => ['Role_2']],
        ],
    ],
];
*/
```

<a name="method-has"></a>
#### `has()`

`has` 메서드는 컬렉션에 주어진 키가 존재하는지 확인합니다.

```php
$collection = collect(['account_id' => 1, 'product' => 'Desk', 'amount' => 5]);

$collection->has('product');

// true

$collection->has(['product', 'amount']);

// true

$collection->has(['amount', 'price']);

// false
```

<a name="method-hasany"></a>
#### `hasAny()`

`hasAny` 메서드는 주어진 키들 중 하나라도 컬렉션에 존재하는지 확인합니다.

```php
$collection = collect(['account_id' => 1, 'product' => 'Desk', 'amount' => 5]);

$collection->hasAny(['product', 'price']);

// true

$collection->hasAny(['name', 'price']);

// false
```

<a name="method-implode"></a>

#### `implode()`

`implode` 메서드는 컬렉션의 항목들을 하나의 문자열로 합쳐줍니다. 인수는 컬렉션의 항목 타입에 따라 달라집니다. 컬렉션에 배열이나 객체가 들어 있다면, 합치고자 하는 속성의 키와 각 값 사이에 넣을 구분자 문자열("glue")을 넘겨야 합니다.

```php
$collection = collect([
    ['account_id' => 1, 'product' => 'Desk'],
    ['account_id' => 2, 'product' => 'Chair'],
]);

$collection->implode('product', ', ');

// 'Desk, Chair'
```

컬렉션에 문자열이나 숫자 값만 들어 있다면, 구분자 문자열 하나만 인자로 넘기면 됩니다.

```php
collect([1, 2, 3, 4, 5])->implode('-');

// '1-2-3-4-5'
```

값을 합칠 때 포맷을 변경하고 싶다면, `implode`에 클로저를 전달할 수 있습니다.

```php
$collection->implode(function (array $item, int $key) {
    return strtoupper($item['product']);
}, ', ');

// 'DESK, CHAIR'
```

<a name="method-intersect"></a>
#### `intersect()`

`intersect` 메서드는 원본 컬렉션에만 존재하고 주어진 배열 혹은 컬렉션에는 없는 값을 제거합니다. 결과 컬렉션은 원본 컬렉션의 키를 그대로 유지합니다.

```php
$collection = collect(['Desk', 'Sofa', 'Chair']);

$intersect = $collection->intersect(['Desk', 'Chair', 'Bookcase']);

$intersect->all();

// [0 => 'Desk', 2 => 'Chair']
```

> [!NOTE]
> 이 메서드는 [Eloquent 컬렉션](/docs/12.x/eloquent-collections#method-intersect)에서는 동작 방식이 다릅니다.

<a name="method-intersectusing"></a>
#### `intersectUsing()`

`intersectUsing` 메서드는 원본 컬렉션에만 존재하고 주어진 배열이나 컬렉션에는 없는 값을 제거하지만, 값 비교에 커스텀 콜백을 사용할 수 있습니다. 결과 컬렉션 역시 원본 컬렉션의 키를 그대로 유지합니다.

```php
$collection = collect(['Desk', 'Sofa', 'Chair']);

$intersect = $collection->intersectUsing(['desk', 'chair', 'bookcase'], function (string $a, string $b) {
    return strcasecmp($a, $b);
});

$intersect->all();

// [0 => 'Desk', 2 => 'Chair']
```

<a name="method-intersectAssoc"></a>
#### `intersectAssoc()`

`intersectAssoc` 메서드는 원본 컬렉션을 다른 컬렉션이나 배열과 비교하여, 모든 컬렉션에 존재하는 키/값 쌍만 반환합니다.

```php
$collection = collect([
    'color' => 'red',
    'size' => 'M',
    'material' => 'cotton'
]);

$intersect = $collection->intersectAssoc([
    'color' => 'blue',
    'size' => 'M',
    'material' => 'polyester'
]);

$intersect->all();

// ['size' => 'M']
```

<a name="method-intersectassocusing"></a>
#### `intersectAssocUsing()`

`intersectAssocUsing` 메서드는 원본 컬렉션을 다른 컬렉션이나 배열과 비교해, 두 컬렉션에 모두 존재하는 키/값 쌍만 반환하되, 키와 값의 동등성을 판단할 때 직접 정의한 비교 콜백을 사용합니다.

```php
$collection = collect([
    'color' => 'red',
    'Size' => 'M',
    'material' => 'cotton',
]);

$intersect = $collection->intersectAssocUsing([
    'color' => 'blue',
    'size' => 'M',
    'material' => 'polyester',
], function (string $a, string $b) {
    return strcasecmp($a, $b);
});

$intersect->all();

// ['Size' => 'M']
```

<a name="method-intersectbykeys"></a>
#### `intersectByKeys()`

`intersectByKeys` 메서드는 원본 컬렉션에 존재하지만 주어진 배열이나 컬렉션에 키가 없는 항목은 제거합니다.

```php
$collection = collect([
    'serial' => 'UX301', 'type' => 'screen', 'year' => 2009,
]);

$intersect = $collection->intersectByKeys([
    'reference' => 'UX404', 'type' => 'tab', 'year' => 2011,
]);

$intersect->all();

// ['type' => 'screen', 'year' => 2009]
```

<a name="method-isempty"></a>
#### `isEmpty()`

`isEmpty` 메서드는 컬렉션이 비어 있으면 `true`를 반환하고, 비어 있지 않으면 `false`를 반환합니다.

```php
collect([])->isEmpty();

// true
```

<a name="method-isnotempty"></a>
#### `isNotEmpty()`

`isNotEmpty` 메서드는 컬렉션에 데이터가 있으면 `true`, 그렇지 않으면 `false`를 반환합니다.

```php
collect([])->isNotEmpty();

// false
```

<a name="method-join"></a>
#### `join()`

`join` 메서드는 컬렉션의 값을 문자열로 합칠 수 있도록 해줍니다. 두 번째 인수를 사용하면 마지막 요소를 어떻게 연결할지 지정할 수 있습니다.

```php
collect(['a', 'b', 'c'])->join(', '); // 'a, b, c'
collect(['a', 'b', 'c'])->join(', ', ', and '); // 'a, b, and c'
collect(['a', 'b'])->join(', ', ' and '); // 'a and b'
collect(['a'])->join(', ', ' and '); // 'a'
collect([])->join(', ', ' and '); // ''
```

<a name="method-keyby"></a>
#### `keyBy()`

`keyBy` 메서드는 지정된 키를 컬렉션의 키로 사용합니다. 동일한 키가 여러 번 등장하면, 마지막 값만 새로운 컬렉션에 남게 됩니다.

```php
$collection = collect([
    ['product_id' => 'prod-100', 'name' => 'Desk'],
    ['product_id' => 'prod-200', 'name' => 'Chair'],
]);

$keyed = $collection->keyBy('product_id');

$keyed->all();

/*
    [
        'prod-100' => ['product_id' => 'prod-100', 'name' => 'Desk'],
        'prod-200' => ['product_id' => 'prod-200', 'name' => 'Chair'],
    ]
*/
```

이 메서드에 콜백을 전달할 수도 있습니다. 콜백은 컬렉션의 키로 사용할 값을 반환해야 합니다.

```php
$keyed = $collection->keyBy(function (array $item, int $key) {
    return strtoupper($item['product_id']);
});

$keyed->all();

/*
    [
        'PROD-100' => ['product_id' => 'prod-100', 'name' => 'Desk'],
        'PROD-200' => ['product_id' => 'prod-200', 'name' => 'Chair'],
    ]
*/
```

<a name="method-keys"></a>
#### `keys()`

`keys` 메서드는 컬렉션의 모든 키를 반환합니다.

```php
$collection = collect([
    'prod-100' => ['product_id' => 'prod-100', 'name' => 'Desk'],
    'prod-200' => ['product_id' => 'prod-200', 'name' => 'Chair'],
]);

$keys = $collection->keys();

$keys->all();

// ['prod-100', 'prod-200']
```

<a name="method-last"></a>
#### `last()`

`last` 메서드는 지정된 조건을 통과하는 컬렉션의 마지막 요소를 반환합니다.

```php
collect([1, 2, 3, 4])->last(function (int $value, int $key) {
    return $value < 3;
});

// 2
```

아무 인자 없이 호출하면 컬렉션의 마지막 요소를 반환합니다. 컬렉션이 비어 있으면 `null`이 반환됩니다.

```php
collect([1, 2, 3, 4])->last();

// 4
```

<a name="method-lazy"></a>
#### `lazy()`

`lazy` 메서드는 해당 컬렉션의 아이템 배열로부터 새로운 [LazyCollection](#lazy-collections) 인스턴스를 반환합니다.

```php
$lazyCollection = collect([1, 2, 3, 4])->lazy();

$lazyCollection::class;

// Illuminate\Support\LazyCollection

$lazyCollection->all();

// [1, 2, 3, 4]
```

이 메서드는 수많은 아이템이 담긴 방대한 `Collection`을 변환해야 할 때 특히 유용합니다.

```php
$count = $hugeCollection
    ->lazy()
    ->where('country', 'FR')
    ->where('balance', '>', '100')
    ->count();
```

컬렉션을 `LazyCollection`으로 변환하면 추가 메모리 할당을 최소화할 수 있습니다. 원본 컬렉션은 여전히 데이터 전체를 메모리에 유지하지만, 이어지는 필터 연산에서는 별도의 메모리를 거의 필요로 하지 않으므로, 결과를 필터링할 때 실질적으로 추가 메모리가 소모되지 않습니다.

<a name="method-macro"></a>
#### `macro()`

정적 메서드인 `macro`를 사용하면 런타임에 `Collection` 클래스에 메서드를 추가할 수 있습니다. 자세한 내용은 [컬렉션 확장하기](#extending-collections) 문서를 참고하세요.

<a name="method-make"></a>
#### `make()`

정적 메서드인 `make`는 새로운 컬렉션 인스턴스를 생성합니다. 자세한 내용은 [컬렉션 생성하기](#creating-collections) 섹션에서 확인할 수 있습니다.

```php
use Illuminate\Support\Collection;

$collection = Collection::make([1, 2, 3]);
```

<a name="method-map"></a>
#### `map()`

`map` 메서드는 컬렉션을 순회하면서 각 값을 주어진 콜백에 전달합니다. 콜백 내에서 아이템을 수정해 반환할 수 있으며, 이렇게 수정된 값들로 새로운 컬렉션이 만들어집니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$multiplied = $collection->map(function (int $item, int $key) {
    return $item * 2;
});

$multiplied->all();

// [2, 4, 6, 8, 10]
```

> [!WARNING]
> 대부분의 다른 컬렉션 메서드와 마찬가지로, `map`은 기존 컬렉션을 변경하지 않고 새로운 컬렉션 인스턴스를 반환합니다. 원본 컬렉션 자체를 변환하려면 [transform](#method-transform) 메서드를 이용하세요.

<a name="method-mapinto"></a>
#### `mapInto()`

`mapInto()` 메서드는 컬렉션을 순회하며, 각 값을 생성자에 전달하여 지정한 클래스의 새 인스턴스를 만듭니다.

```php
class Currency
{
    /**
     * 새 Currency 인스턴스를 생성합니다.
     */
    function __construct(
        public string $code,
    ) {}
}

$collection = collect(['USD', 'EUR', 'GBP']);

$currencies = $collection->mapInto(Currency::class);

$currencies->all();

// [Currency('USD'), Currency('EUR'), Currency('GBP')]
```

<a name="method-mapspread"></a>
#### `mapSpread()`

`mapSpread` 메서드는 컬렉션의 각 중첩된 항목(예: 배열) 값을 주어진 클로저에 인수로 넘깁니다. 클로저 내에서 아이템을 수정해 반환하면, 이 값들로 새로운 컬렉션이 만들어집니다.

```php
$collection = collect([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]);

$chunks = $collection->chunk(2);

$sequence = $chunks->mapSpread(function (int $even, int $odd) {
    return $even + $odd;
});

$sequence->all();

// [1, 5, 9, 13, 17]
```

<a name="method-maptogroups"></a>
#### `mapToGroups()`

`mapToGroups` 메서드는 컬렉션의 아이템을 주어진 클로저로 그룹화합니다. 클로저는 단일 키/값 쌍(연관 배열)을 반환해야 하며, 이 키값들을 기준으로 새로 그룹핑된 컬렉션이 만들어집니다.

```php
$collection = collect([
    [
        'name' => 'John Doe',
        'department' => 'Sales',
    ],
    [
        'name' => 'Jane Doe',
        'department' => 'Sales',
    ],
    [
        'name' => 'Johnny Doe',
        'department' => 'Marketing',
    ]
]);

$grouped = $collection->mapToGroups(function (array $item, int $key) {
    return [$item['department'] => $item['name']];
});

$grouped->all();

/*
    [
        'Sales' => ['John Doe', 'Jane Doe'],
        'Marketing' => ['Johnny Doe'],
    ]
*/

$grouped->get('Sales')->all();

// ['John Doe', 'Jane Doe']
```

<a name="method-mapwithkeys"></a>
#### `mapWithKeys()`

`mapWithKeys` 메서드는 컬렉션을 순회하면서 각 값을 주어진 콜백에 전달합니다. 콜백은 단일 키/값 쌍(연관 배열)를 반환해야 합니다.

```php
$collection = collect([
    [
        'name' => 'John',
        'department' => 'Sales',
        'email' => 'john@example.com',
    ],
    [
        'name' => 'Jane',
        'department' => 'Marketing',
        'email' => 'jane@example.com',
    ]
]);

$keyed = $collection->mapWithKeys(function (array $item, int $key) {
    return [$item['email'] => $item['name']];
});

$keyed->all();

/*
    [
        'john@example.com' => 'John',
        'jane@example.com' => 'Jane',
    ]
*/
```

<a name="method-max"></a>
#### `max()`

`max` 메서드는 주어진 키의 최대값을 반환합니다.

```php
$max = collect([
    ['foo' => 10],
    ['foo' => 20]
])->max('foo');

// 20

$max = collect([1, 2, 3, 4, 5])->max();

// 5
```

<a name="method-median"></a>
#### `median()`

`median` 메서드는 주어진 키의 [중앙값(중간값)](https://en.wikipedia.org/wiki/Median)을 반환합니다.

```php
$median = collect([
    ['foo' => 10],
    ['foo' => 10],
    ['foo' => 20],
    ['foo' => 40]
])->median('foo');

// 15

$median = collect([1, 1, 2, 4])->median();

// 1.5
```

<a name="method-merge"></a>
#### `merge()`

`merge` 메서드는 주어진 배열이나 컬렉션을 원본 컬렉션과 병합합니다. 주어진 항목에 문자열 키가 있고, 이것이 원본 컬렉션에도 있다면, 주어진 항목의 값이 원본 컬렉션 값을 덮어씁니다.

```php
$collection = collect(['product_id' => 1, 'price' => 100]);

$merged = $collection->merge(['price' => 200, 'discount' => false]);

$merged->all();

// ['product_id' => 1, 'price' => 200, 'discount' => false]
```

주어진 항목의 키가 숫자일 경우, 해당 값들은 컬렉션의 마지막에 추가됩니다.

```php
$collection = collect(['Desk', 'Chair']);

$merged = $collection->merge(['Bookcase', 'Door']);

$merged->all();

// ['Desk', 'Chair', 'Bookcase', 'Door']
```

<a name="method-mergerecursive"></a>
#### `mergeRecursive()`

`mergeRecursive` 메서드는 주어진 배열이나 컬렉션을 원본 컬렉션과 재귀적으로 병합합니다. 주어진 항목의 문자열 키가 원본 컬렉션에도 있다면, 해당 키의 값이 배열로 합쳐지며, 이 과정이 반복적으로 수행됩니다.

```php
$collection = collect(['product_id' => 1, 'price' => 100]);

$merged = $collection->mergeRecursive([
    'product_id' => 2,
    'price' => 200,
    'discount' => false
]);

$merged->all();

// ['product_id' => [1, 2], 'price' => [100, 200], 'discount' => false]
```

<a name="method-min"></a>
#### `min()`

`min` 메서드는 주어진 키의 최소값을 반환합니다.

```php
$min = collect([['foo' => 10], ['foo' => 20]])->min('foo');

// 10

$min = collect([1, 2, 3, 4, 5])->min();

// 1
```

<a name="method-mode"></a>
#### `mode()`

`mode` 메서드는 주어진 키의 [최빈값(가장 많이 등장하는 값)](https://en.wikipedia.org/wiki/Mode_(statistics))을 반환합니다.

```php
$mode = collect([
    ['foo' => 10],
    ['foo' => 10],
    ['foo' => 20],
    ['foo' => 40]
])->mode('foo');

// [10]

$mode = collect([1, 1, 2, 4])->mode();

// [1]

$mode = collect([1, 1, 2, 2])->mode();

// [1, 2]
```

<a name="method-multiply"></a>
#### `multiply()`

`multiply` 메서드는 컬렉션의 모든 항목을 지정한 횟수만큼 복제하여 새로운 컬렉션을 만듭니다.

```php
$users = collect([
    ['name' => 'User #1', 'email' => 'user1@example.com'],
    ['name' => 'User #2', 'email' => 'user2@example.com'],
])->multiply(3);

/*
    [
        ['name' => 'User #1', 'email' => 'user1@example.com'],
        ['name' => 'User #2', 'email' => 'user2@example.com'],
        ['name' => 'User #1', 'email' => 'user1@example.com'],
        ['name' => 'User #2', 'email' => 'user2@example.com'],
        ['name' => 'User #1', 'email' => 'user1@example.com'],
        ['name' => 'User #2', 'email' => 'user2@example.com'],
    ]
*/
```

<a name="method-nth"></a>
#### `nth()`

`nth` 메서드는 컬렉션에서 n번째마다 하나씩 골라 새로운 컬렉션을 만듭니다.

```php
$collection = collect(['a', 'b', 'c', 'd', 'e', 'f']);

$collection->nth(4);

// ['a', 'e']
```

두 번째 인수로 시작 오프셋을 지정할 수도 있습니다.

```php
$collection->nth(4, 1);

// ['b', 'f']
```

<a name="method-only"></a>
#### `only()`

`only` 메서드는 지정한 키에 해당하는 컬렉션의 항목들만 반환합니다.

```php
$collection = collect([
    'product_id' => 1,
    'name' => 'Desk',
    'price' => 100,
    'discount' => false
]);

$filtered = $collection->only(['product_id', 'name']);

$filtered->all();

// ['product_id' => 1, 'name' => 'Desk']
```

반대로 지정한 키를 제외하고 반환하려면 [except](#method-except) 메서드를 참고하세요.

> [!NOTE]
> [Eloquent 컬렉션](/docs/12.x/eloquent-collections#method-only)에서 이 메서드는 동작 방식이 다릅니다.

<a name="method-pad"></a>
#### `pad()`

`pad` 메서드는 배열이 지정한 크기에 도달할 때까지 지정한 값으로 채웁니다. 이 메서드는 [array_pad](https://secure.php.net/manual/en/function.array-pad.php) PHP 함수와 동작이 동일합니다.

왼쪽(앞쪽)에서 채우려면 음수 크기를 지정하세요. 지정한 크기의 절댓값이 배열 길이와 같거나 작으면 패딩이 이루어지지 않습니다.

```php
$collection = collect(['A', 'B', 'C']);

$filtered = $collection->pad(5, 0);

$filtered->all();

// ['A', 'B', 'C', 0, 0]

$filtered = $collection->pad(-5, 0);

$filtered->all();

// [0, 0, 'A', 'B', 'C']
```

<a name="method-partition"></a>
#### `partition()`

`partition` 메서드는 PHP 배열 구조 분해 할당과 함께 사용하여, 지정한 조건을 만족하는 요소와 그렇지 않은 요소로 컬렉션을 분리할 수 있습니다.

```php
$collection = collect([1, 2, 3, 4, 5, 6]);

[$underThree, $equalOrAboveThree] = $collection->partition(function (int $i) {
    return $i < 3;
});

$underThree->all();

// [1, 2]

$equalOrAboveThree->all();

// [3, 4, 5, 6]
```

> [!NOTE]
> [Eloquent 컬렉션](/docs/12.x/eloquent-collections#method-partition)에서 이 메서드는 동작 방식이 다릅니다.

<a name="method-percentage"></a>
#### `percentage()`

`percentage` 메서드는 컬렉션에서 지정한 조건을 통과하는 항목의 비율(%)을 빠르게 구할 수 있습니다.

```php
$collection = collect([1, 1, 2, 2, 2, 3]);

$percentage = $collection->percentage(fn (int $value) => $value === 1);

// 33.33
```

기본적으로 소수점 두 자리까지 반올림한 값을 반환합니다. 두 번째 인수로 소수점 자릿수를 지정하면 이 동작을 변경할 수 있습니다.

```php
$percentage = $collection->percentage(fn (int $value) => $value === 1, precision: 3);

// 33.333
```

<a name="method-pipe"></a>
#### `pipe()`

`pipe` 메서드는 컬렉션을 주어진 클로저로 넘기고, 해당 클로저의 실행 결과를 반환합니다.

```php
$collection = collect([1, 2, 3]);

$piped = $collection->pipe(function (Collection $collection) {
    return $collection->sum();
});

// 6
```

<a name="method-pipeinto"></a>

#### `pipeInto()`

`pipeInto` 메서드는 지정한 클래스의 새 인스턴스를 생성하고, 컬렉션을 그 생성자에 전달합니다.

```php
class ResourceCollection
{
    /**
     * Create a new ResourceCollection instance.
     */
    public function __construct(
        public Collection $collection,
    ) {}
}

$collection = collect([1, 2, 3]);

$resource = $collection->pipeInto(ResourceCollection::class);

$resource->collection->all();

// [1, 2, 3]
```

<a name="method-pipethrough"></a>
#### `pipeThrough()`

`pipeThrough` 메서드는 컬렉션을 주어진 클로저 배열에 차례로 전달하고, 최종적으로 실행된 클로저의 결과를 반환합니다.

```php
use Illuminate\Support\Collection;

$collection = collect([1, 2, 3]);

$result = $collection->pipeThrough([
    function (Collection $collection) {
        return $collection->merge([4, 5]);
    },
    function (Collection $collection) {
        return $collection->sum();
    },
]);

// 15
```

<a name="method-pluck"></a>
#### `pluck()`

`pluck` 메서드는 지정한 키의 모든 값을 가져옵니다.

```php
$collection = collect([
    ['product_id' => 'prod-100', 'name' => 'Desk'],
    ['product_id' => 'prod-200', 'name' => 'Chair'],
]);

$plucked = $collection->pluck('name');

$plucked->all();

// ['Desk', 'Chair']
```

결과로 반환될 컬렉션의 키를 지정하고 싶을 때는 두 번째 인수로 키를 전달할 수 있습니다.

```php
$plucked = $collection->pluck('name', 'product_id');

$plucked->all();

// ['prod-100' => 'Desk', 'prod-200' => 'Chair']
```

`pluck` 메서드는 "dot" 표기법을 사용하여 중첩된 값을 가져오는 것도 지원합니다.

```php
$collection = collect([
    [
        'name' => 'Laracon',
        'speakers' => [
            'first_day' => ['Rosa', 'Judith'],
        ],
    ],
    [
        'name' => 'VueConf',
        'speakers' => [
            'first_day' => ['Abigail', 'Joey'],
        ],
    ],
]);

$plucked = $collection->pluck('speakers.first_day');

$plucked->all();

// [['Rosa', 'Judith'], ['Abigail', 'Joey']]
```

중복되는 키가 있는 경우, 마지막에 일치하는 요소만이 plucked 컬렉션에 저장됩니다.

```php
$collection = collect([
    ['brand' => 'Tesla',  'color' => 'red'],
    ['brand' => 'Pagani', 'color' => 'white'],
    ['brand' => 'Tesla',  'color' => 'black'],
    ['brand' => 'Pagani', 'color' => 'orange'],
]);

$plucked = $collection->pluck('color', 'brand');

$plucked->all();

// ['Tesla' => 'black', 'Pagani' => 'orange']
```

<a name="method-pop"></a>
#### `pop()`

`pop` 메서드는 컬렉션의 마지막 아이템을 제거해서 반환합니다. 컬렉션이 비어 있다면 `null`이 반환됩니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->pop();

// 5

$collection->all();

// [1, 2, 3, 4]
```

`pop` 메서드에 정수를 전달하면, 컬렉션의 끝에서 여러 개의 아이템을 제거해 반환할 수 있습니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->pop(3);

// collect([5, 4, 3])

$collection->all();

// [1, 2]
```

<a name="method-prepend"></a>
#### `prepend()`

`prepend` 메서드는 컬렉션의 맨 앞에 아이템을 추가합니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->prepend(0);

$collection->all();

// [0, 1, 2, 3, 4, 5]
```

추가될 아이템의 키를 지정하려면 두 번째 인수로 키를 전달할 수 있습니다.

```php
$collection = collect(['one' => 1, 'two' => 2]);

$collection->prepend(0, 'zero');

$collection->all();

// ['zero' => 0, 'one' => 1, 'two' => 2]
```

<a name="method-pull"></a>
#### `pull()`

`pull` 메서드는 지정한 키로 컬렉션에서 아이템을 제거하여 반환합니다.

```php
$collection = collect(['product_id' => 'prod-100', 'name' => 'Desk']);

$collection->pull('name');

// 'Desk'

$collection->all();

// ['product_id' => 'prod-100']
```

<a name="method-push"></a>
#### `push()`

`push` 메서드는 컬렉션의 끝에 아이템을 추가합니다.

```php
$collection = collect([1, 2, 3, 4]);

$collection->push(5);

$collection->all();

// [1, 2, 3, 4, 5]
```

컬렉션의 끝에 여러 개의 아이템을 추가하고 싶다면, 여러 인수를 전달할 수 있습니다.

```php
$collection = collect([1, 2, 3, 4]);

$collection->push(5, 6, 7);
 
$collection->all();
 
// [1, 2, 3, 4, 5, 6, 7]
```

<a name="method-put"></a>
#### `put()`

`put` 메서드는 지정한 키와 값을 컬렉션에 저장합니다.

```php
$collection = collect(['product_id' => 1, 'name' => 'Desk']);

$collection->put('price', 100);

$collection->all();

// ['product_id' => 1, 'name' => 'Desk', 'price' => 100]
```

<a name="method-random"></a>
#### `random()`

`random` 메서드는 컬렉션에서 임의의 아이템을 반환합니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->random();

// 4 - (임의로 가져옴)
```

몇 개의 아이템을 임의로 뽑고 싶다면, `random` 메서드에 정수를 전달할 수 있습니다. 이때는 항상 컬렉션 인스턴스가 반환됩니다.

```php
$random = $collection->random(3);

$random->all();

// [2, 4, 5] - (임의로 가져옴)
```

컬렉션이 요청한 갯수보다 적은 아이템을 가지고 있으면 `random` 메서드는 `InvalidArgumentException`을 발생시킵니다.

또한, `random` 메서드는 클로저를 인수로 받을 수도 있으며, 이때는 현재 컬렉션 인스턴스가 클로저로 전달됩니다.

```php
use Illuminate\Support\Collection;

$random = $collection->random(fn (Collection $items) => min(10, count($items)));

$random->all();

// [1, 2, 3, 4, 5] - (임의로 가져옴)
```

<a name="method-range"></a>
#### `range()`

`range` 메서드는 지정한 범위의 정수들이 들어있는 컬렉션을 반환합니다.

```php
$collection = collect()->range(3, 6);

$collection->all();

// [3, 4, 5, 6]
```

<a name="method-reduce"></a>
#### `reduce()`

`reduce` 메서드는 컬렉션을 단일 값으로 축약(reduce)하며, 각 반복의 결과를 다음 반복에 전달합니다.

```php
$collection = collect([1, 2, 3]);

$total = $collection->reduce(function (?int $carry, int $item) {
    return $carry + $item;
});

// 6
```

첫 번째 반복에서 `$carry` 값은 `null`입니다. 하지만 두 번째 인수로 초기값을 전달하여 시작 값을 지정할 수 있습니다.

```php
$collection->reduce(function (int $carry, int $item) {
    return $carry + $item;
}, 4);

// 10
```

`reduce` 메서드는 배열의 키도 콜백 함수에 전달합니다.

```php
$collection = collect([
    'usd' => 1400,
    'gbp' => 1200,
    'eur' => 1000,
]);

$ratio = [
    'usd' => 1,
    'gbp' => 1.37,
    'eur' => 1.22,
];

$collection->reduce(function (int $carry, int $value, string $key) use ($ratio) {
    return $carry + ($value * $ratio[$key]);
}, 0);

// 4264
```

<a name="method-reduce-spread"></a>
#### `reduceSpread()`

`reduceSpread` 메서드는 컬렉션을 여러 값의 배열로 축약(reduce)하며, 각 반복의 결과 배열을 다음 반복에 전달합니다. 이 메서드는 `reduce`와 비슷하지만, 여러 개의 초기 값을 사용할 수 있습니다.

```php
[$creditsRemaining, $batch] = Image::where('status', 'unprocessed')
    ->get()
    ->reduceSpread(function (int $creditsRemaining, Collection $batch, Image $image) {
        if ($creditsRemaining >= $image->creditsRequired()) {
            $batch->push($image);

            $creditsRemaining -= $image->creditsRequired();
        }

        return [$creditsRemaining, $batch];
    }, $creditsAvailable, collect());
```

<a name="method-reject"></a>
#### `reject()`

`reject` 메서드는 지정한 클로저를 사용하여 컬렉션을 필터링합니다. 클로저가 `true`를 반환하는 아이템은 결과 컬렉션에서 제외됩니다.

```php
$collection = collect([1, 2, 3, 4]);

$filtered = $collection->reject(function (int $value, int $key) {
    return $value > 2;
});

$filtered->all();

// [1, 2]
```

`reject` 메서드와 반대 기능을 원한다면 [filter](#method-filter) 메서드를 참고하세요.

<a name="method-replace"></a>
#### `replace()`

`replace` 메서드는 `merge`와 비슷하게 동작하지만, 문자열 키뿐만 아니라 숫자 키가 일치하는 아이템도 덮어쓴다는 차이점이 있습니다.

```php
$collection = collect(['Taylor', 'Abigail', 'James']);

$replaced = $collection->replace([1 => 'Victoria', 3 => 'Finn']);

$replaced->all();

// ['Taylor', 'Victoria', 'James', 'Finn']
```

<a name="method-replacerecursive"></a>
#### `replaceRecursive()`

`replaceRecursive` 메서드는 `replace`와 비슷하지만, 내부 배열까지 재귀적으로 순회하면서 같은 방식으로 값을 교체합니다.

```php
$collection = collect([
    'Taylor',
    'Abigail',
    [
        'James',
        'Victoria',
        'Finn'
    ]
]);

$replaced = $collection->replaceRecursive([
    'Charlie',
    2 => [1 => 'King']
]);

$replaced->all();

// ['Charlie', 'Abigail', ['James', 'King', 'Finn']]
```

<a name="method-reverse"></a>
#### `reverse()`

`reverse` 메서드는 컬렉션의 모든 아이템 순서를 반대로 뒤집으며, 원래의 키는 그대로 유지합니다.

```php
$collection = collect(['a', 'b', 'c', 'd', 'e']);

$reversed = $collection->reverse();

$reversed->all();

/*
    [
        4 => 'e',
        3 => 'd',
        2 => 'c',
        1 => 'b',
        0 => 'a',
    ]
*/
```

<a name="method-search"></a>
#### `search()`

`search` 메서드는 지정한 값을 컬렉션에서 찾아, 발견 시 그 키를 반환합니다. 찾지 못하면 `false`를 반환합니다.

```php
$collection = collect([2, 4, 6, 8]);

$collection->search(4);

// 1
```

기본적으로 "느슨한(loose)" 비교가 사용되어, 정수 값의 문자열도 같은 값의 정수와 동일하게 취급됩니다. "엄격한(strict)" 비교를 원한다면 메서드의 두 번째 인수로 `true`를 전달하세요.

```php
collect([2, 4, 6, 8])->search('4', strict: true);

// false
```

또는, 원하는 조건을 만족하는 첫 번째 아이템을 직접 찾기 위해 클로저를 사용할 수도 있습니다.

```php
collect([2, 4, 6, 8])->search(function (int $item, int $key) {
    return $item > 5;
});

// 2
```

<a name="method-select"></a>
#### `select()`

`select` 메서드는 지정한 키들만 골라내어 반환합니다. SQL의 `SELECT` 구문과 비슷하게 작동합니다.

```php
$users = collect([
    ['name' => 'Taylor Otwell', 'role' => 'Developer', 'status' => 'active'],
    ['name' => 'Victoria Faith', 'role' => 'Researcher', 'status' => 'active'],
]);

$users->select(['name', 'role']);

/*
    [
        ['name' => 'Taylor Otwell', 'role' => 'Developer'],
        ['name' => 'Victoria Faith', 'role' => 'Researcher'],
    ],
*/
```

<a name="method-shift"></a>
#### `shift()`

`shift` 메서드는 컬렉션의 첫 번째 아이템을 제거하여 반환합니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->shift();

// 1

$collection->all();

// [2, 3, 4, 5]
```

`shift` 메서드에 정수를 전달하면, 컬렉션의 앞에서 여러 개의 아이템을 제거해 반환할 수 있습니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->shift(3);

// collect([1, 2, 3])

$collection->all();

// [4, 5]
```

<a name="method-shuffle"></a>
#### `shuffle()`

`shuffle` 메서드는 컬렉션의 아이템 순서를 무작위로 섞어서 반환합니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$shuffled = $collection->shuffle();

$shuffled->all();

// [3, 2, 5, 1, 4] - (임의로 섞임)
```

<a name="method-skip"></a>
#### `skip()`

`skip` 메서드는 컬렉션의 앞에서 지정한 개수만큼의 아이템을 건너뛴 나머지로 새로운 컬렉션을 반환합니다.

```php
$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);

$collection = $collection->skip(4);

$collection->all();

// [5, 6, 7, 8, 9, 10]
```

<a name="method-skipuntil"></a>
#### `skipUntil()`

`skipUntil` 메서드는 지정한 콜백이 `false`를 반환하는 동안 컬렉션의 아이템들을 건너뜁니다. 콜백이 `true`를 반환하면, 그 시점부터 남은 모든 아이템을 새로운 컬렉션으로 반환합니다.

```php
$collection = collect([1, 2, 3, 4]);

$subset = $collection->skipUntil(function (int $item) {
    return $item >= 3;
});

$subset->all();

// [3, 4]
```

또는, skipUntil 메서드에 단일 값을 전달하여 해당 값이 나올 때까지 아이템을 건너뛸 수도 있습니다.

```php
$collection = collect([1, 2, 3, 4]);

$subset = $collection->skipUntil(3);

$subset->all();

// [3, 4]
```

> [!WARNING]
> 지정한 값이 없거나, 콜백이 한 번도 `true`를 반환하지 않는 경우, `skipUntil` 메서드는 빈 컬렉션을 반환합니다.

<a name="method-skipwhile"></a>
#### `skipWhile()`

`skipWhile` 메서드는 지정한 콜백이 `true`를 반환하는 동안 컬렉션의 아이템들을 건너뜁니다. 콜백이 `false`를 반환하는 순간부터 남은 모든 아이템을 새로운 컬렉션으로 반환합니다.

```php
$collection = collect([1, 2, 3, 4]);

$subset = $collection->skipWhile(function (int $item) {
    return $item <= 3;
});

$subset->all();

// [4]
```

> [!WARNING]
> 콜백이 한 번도 `false`를 반환하지 않으면, `skipWhile` 메서드는 빈 컬렉션을 반환하게 됩니다.

<a name="method-slice"></a>
#### `slice()`

`slice` 메서드는 지정한 인덱스부터 컬렉션의 일부(슬라이스)를 잘라냅니다.

```php
$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);

$slice = $collection->slice(4);

$slice->all();

// [5, 6, 7, 8, 9, 10]
```

반환되는 슬라이스의 크기를 제한하고 싶다면 두 번째 인수로 원하는 값을 지정할 수 있습니다.

```php
$slice = $collection->slice(4, 2);

$slice->all();

// [5, 6]
```

슬라이스는 기본적으로 원래의 키를 유지합니다. 키를 새로 부여하고 싶으면 [values](#method-values) 메서드를 사용할 수 있습니다.

<a name="method-sliding"></a>
#### `sliding()`

`sliding` 메서드는 컬렉션의 아이템을 "슬라이딩 윈도우" 단위로 잘라 여러 개의 청크(조각)가 담긴 새 컬렉션을 반환합니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$chunks = $collection->sliding(2);

$chunks->toArray();

// [[1, 2], [2, 3], [3, 4], [4, 5]]
```

이 방법은 [eachSpread](#method-eachspread) 메서드와 함께 사용할 때 특히 유용합니다.

```php
$transactions->sliding(2)->eachSpread(function (Collection $previous, Collection $current) {
    $current->total = $previous->total + $current->amount;
});
```

옵션으로 두 번째 인수인 "step" 값을 설정해, 각 청크의 첫 번째 아이템 사이의 간격을 조정할 수 있습니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$chunks = $collection->sliding(3, step: 2);

$chunks->toArray();

// [[1, 2, 3], [3, 4, 5]]
```

<a name="method-sole"></a>
#### `sole()`

`sole` 메서드는 지정한 조건을 통과하는 컬렉션의 첫 번째 요소를 반환합니다. 단, 조건을 만족하는 요소가 정확히 하나여야만 합니다.

```php
collect([1, 2, 3, 4])->sole(function (int $value, int $key) {
    return $value === 2;
});

// 2
```

또는 `sole` 메서드에 키/값 쌍을 전달해, 해당 조건에 일치하는 요소가 오직 하나일 때만 그 값을 반환할 수 있습니다.

```php
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
]);

$collection->sole('product', 'Chair');

// ['product' => 'Chair', 'price' => 100]
```

아무 인수도 전달하지 않고 `sole`을 호출할 경우, 컬렉션에 요소가 하나만 있을 때 그 값을 반환합니다.

```php
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
]);

$collection->sole();

// ['product' => 'Desk', 'price' => 200]
```

`sole` 메서드로 반환할 요소가 없는 경우에는 `\Illuminate\Collections\ItemNotFoundException` 예외가 발생합니다. 반환할 요소가 둘 이상일 경우에는 `\Illuminate\Collections\MultipleItemsFoundException` 예외가 발생합니다.

<a name="method-some"></a>

#### `some()`

[contains](#method-contains) 메서드의 별칭입니다.

<a name="method-sort"></a>
#### `sort()`

`sort` 메서드는 컬렉션을 정렬합니다. 정렬된 컬렉션은 원본 배열의 키를 그대로 유지하기 때문에, 아래 예시처럼 [values](#method-values) 메서드를 사용해 키를 연속된 숫자 인덱스로 재설정할 수 있습니다.

```php
$collection = collect([5, 3, 1, 2, 4]);

$sorted = $collection->sort();

$sorted->values()->all();

// [1, 2, 3, 4, 5]
```

더 복잡한 정렬이 필요하다면, `sort` 메서드에 직접 콜백을 전달하여 고유한 정렬 알고리즘을 구현할 수도 있습니다. 내부적으로 컬렉션의 `sort` 메서드는 PHP의 [uasort](https://secure.php.net/manual/en/function.uasort.php#refsect1-function.uasort-parameters) 함수를 사용합니다. 자세한 내용은 해당 PHP 문서를 참고하십시오.

> [!NOTE]
> 중첩 배열이나 객체의 컬렉션을 정렬하고 싶다면 [sortBy](#method-sortby) 또는 [sortByDesc](#method-sortbydesc) 메서드를 참고하세요.

<a name="method-sortby"></a>
#### `sortBy()`

`sortBy` 메서드는 지정한 키를 기준으로 컬렉션을 정렬합니다. 정렬된 컬렉션은 원본 배열의 키를 그대로 유지하므로, 아래 예시처럼 [values](#method-values) 메서드를 사용해 키를 연속된 숫자 인덱스로 재설정할 수 있습니다.

```php
$collection = collect([
    ['name' => 'Desk', 'price' => 200],
    ['name' => 'Chair', 'price' => 100],
    ['name' => 'Bookcase', 'price' => 150],
]);

$sorted = $collection->sortBy('price');

$sorted->values()->all();

/*
    [
        ['name' => 'Chair', 'price' => 100],
        ['name' => 'Bookcase', 'price' => 150],
        ['name' => 'Desk', 'price' => 200],
    ]
*/
```

`sortBy` 메서드는 두 번째 인수로 [정렬 플래그](https://www.php.net/manual/en/function.sort.php)를 받을 수 있습니다.

```php
$collection = collect([
    ['title' => 'Item 1'],
    ['title' => 'Item 12'],
    ['title' => 'Item 3'],
]);

$sorted = $collection->sortBy('title', SORT_NATURAL);

$sorted->values()->all();

/*
    [
        ['title' => 'Item 1'],
        ['title' => 'Item 3'],
        ['title' => 'Item 12'],
    ]
*/
```

또한, 컬렉션 값의 정렬 방법을 결정하기 위한 클로저(익명 함수)를 직접 전달할 수도 있습니다.

```php
$collection = collect([
    ['name' => 'Desk', 'colors' => ['Black', 'Mahogany']],
    ['name' => 'Chair', 'colors' => ['Black']],
    ['name' => 'Bookcase', 'colors' => ['Red', 'Beige', 'Brown']],
]);

$sorted = $collection->sortBy(function (array $product, int $key) {
    return count($product['colors']);
});

$sorted->values()->all();

/*
    [
        ['name' => 'Chair', 'colors' => ['Black']],
        ['name' => 'Desk', 'colors' => ['Black', 'Mahogany']],
        ['name' => 'Bookcase', 'colors' => ['Red', 'Beige', 'Brown']],
    ]
*/
```

여러 속성을 기준으로 컬렉션을 정렬하고 싶다면, `sortBy` 메서드에 정렬 조건의 배열을 전달할 수 있습니다. 각 정렬 조건은 정렬 기준이 될 속성과 정렬 방향으로 이루어진 배열입니다.

```php
$collection = collect([
    ['name' => 'Taylor Otwell', 'age' => 34],
    ['name' => 'Abigail Otwell', 'age' => 30],
    ['name' => 'Taylor Otwell', 'age' => 36],
    ['name' => 'Abigail Otwell', 'age' => 32],
]);

$sorted = $collection->sortBy([
    ['name', 'asc'],
    ['age', 'desc'],
]);

$sorted->values()->all();

/*
    [
        ['name' => 'Abigail Otwell', 'age' => 32],
        ['name' => 'Abigail Otwell', 'age' => 30],
        ['name' => 'Taylor Otwell', 'age' => 36],
        ['name' => 'Taylor Otwell', 'age' => 34],
    ]
*/
```

여러 속성을 기준으로 정렬할 때, 각 정렬 작업을 정의하는 클로저를 배열에 전달할 수도 있습니다.

```php
$collection = collect([
    ['name' => 'Taylor Otwell', 'age' => 34],
    ['name' => 'Abigail Otwell', 'age' => 30],
    ['name' => 'Taylor Otwell', 'age' => 36],
    ['name' => 'Abigail Otwell', 'age' => 32],
]);

$sorted = $collection->sortBy([
    fn (array $a, array $b) => $a['name'] <=> $b['name'],
    fn (array $a, array $b) => $b['age'] <=> $a['age'],
]);

$sorted->values()->all();

/*
    [
        ['name' => 'Abigail Otwell', 'age' => 32],
        ['name' => 'Abigail Otwell', 'age' => 30],
        ['name' => 'Taylor Otwell', 'age' => 36],
        ['name' => 'Taylor Otwell', 'age' => 34],
    ]
*/
```

<a name="method-sortbydesc"></a>
#### `sortByDesc()`

이 메서드는 [sortBy](#method-sortby) 메서드와 시그니처가 동일하지만, 컬렉션을 반대 순서(내림차순)로 정렬합니다.

<a name="method-sortdesc"></a>
#### `sortDesc()`

이 메서드는 [sort](#method-sort) 메서드와 반대 순서(내림차순)로 컬렉션을 정렬합니다.

```php
$collection = collect([5, 3, 1, 2, 4]);

$sorted = $collection->sortDesc();

$sorted->values()->all();

// [5, 4, 3, 2, 1]
```

`sort`와 달리 `sortDesc`에는 클로저를 전달할 수 없습니다. 직접 비교 로직을 구현하려면 [sort](#method-sort) 메서드를 사용하고, 비교 결과를 반전시키는 방식으로 구현해야 합니다.

<a name="method-sortkeys"></a>
#### `sortKeys()`

`sortKeys` 메서드는 컬렉션을 내부 연관 배열의 키로 정렬합니다.

```php
$collection = collect([
    'id' => 22345,
    'first' => 'John',
    'last' => 'Doe',
]);

$sorted = $collection->sortKeys();

$sorted->all();

/*
    [
        'first' => 'John',
        'id' => 22345,
        'last' => 'Doe',
    ]
*/
```

<a name="method-sortkeysdesc"></a>
#### `sortKeysDesc()`

이 메서드는 [sortKeys](#method-sortkeys) 메서드와 시그니처가 동일하지만, 반대 순서(내림차순)로 정렬됩니다.

<a name="method-sortkeysusing"></a>
#### `sortKeysUsing()`

`sortKeysUsing` 메서드는 콜백을 이용해 내부 연관 배열의 키로 컬렉션을 정렬합니다.

```php
$collection = collect([
    'ID' => 22345,
    'first' => 'John',
    'last' => 'Doe',
]);

$sorted = $collection->sortKeysUsing('strnatcasecmp');

$sorted->all();

/*
    [
        'first' => 'John',
        'ID' => 22345,
        'last' => 'Doe',
    ]
*/
```

콜백 함수는 비교 함수여야 하며, PHP에서 비교 결과에 따라 0보다 작거나 같거나 큰 정수를 반환해야 합니다. 내부적으로 [uksort](https://www.php.net/manual/en/function.uksort.php#refsect1-function.uksort-parameters) 함수를 사용하므로, 자세한 내용은 PHP 공식 문서를 확인하세요.

<a name="method-splice"></a>
#### `splice()`

`splice` 메서드는 지정한 인덱스에서 시작하여 아이템의 일부를 제거하고, 제거한 부분을 새 컬렉션으로 반환합니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$chunk = $collection->splice(2);

$chunk->all();

// [3, 4, 5]

$collection->all();

// [1, 2]
```

두 번째 인수를 전달하면 결과 컬렉션의 반환 크기를 제한할 수 있습니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$chunk = $collection->splice(2, 1);

$chunk->all();

// [3]

$collection->all();

// [1, 2, 4, 5]
```

또한, 세 번째 인수로 제거된 아이템을 대체할 새로운 값을 배열로 전달할 수도 있습니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$chunk = $collection->splice(2, 1, [10, 11]);

$chunk->all();

// [3]

$collection->all();

// [1, 2, 10, 11, 4, 5]
```

<a name="method-split"></a>
#### `split()`

`split` 메서드는 컬렉션을 지정한 수 만큼의 그룹으로 나눕니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$groups = $collection->split(3);

$groups->all();

// [[1, 2], [3, 4], [5]]
```

<a name="method-splitin"></a>
#### `splitIn()`

`splitIn` 메서드는 컬렉션을 지정한 그룹 수로 나누되, 마지막 그룹을 제외한 나머지 그룹을 가득 채운 뒤, 남은 항목을 마지막 그룹에 할당합니다.

```php
$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);

$groups = $collection->splitIn(3);

$groups->all();

// [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10]]
```

<a name="method-sum"></a>
#### `sum()`

`sum` 메서드는 컬렉션의 모든 항목의 합계를 반환합니다.

```php
collect([1, 2, 3, 4, 5])->sum();

// 15
```

컬렉션의 값이 중첩 배열이나 객체라면, 합계를 구할 키를 지정해주어야 합니다.

```php
$collection = collect([
    ['name' => 'JavaScript: The Good Parts', 'pages' => 176],
    ['name' => 'JavaScript: The Definitive Guide', 'pages' => 1096],
]);

$collection->sum('pages');

// 1272
```

또는, 컬렉션에서 어떤 값을 더할지 직접 정의하는 클로저를 전달할 수도 있습니다.

```php
$collection = collect([
    ['name' => 'Chair', 'colors' => ['Black']],
    ['name' => 'Desk', 'colors' => ['Black', 'Mahogany']],
    ['name' => 'Bookcase', 'colors' => ['Red', 'Beige', 'Brown']],
]);

$collection->sum(function (array $product) {
    return count($product['colors']);
});

// 6
```

<a name="method-take"></a>
#### `take()`

`take` 메서드는 지정한 개수만큼의 아이템을 포함하는 새로운 컬렉션을 반환합니다.

```php
$collection = collect([0, 1, 2, 3, 4, 5]);

$chunk = $collection->take(3);

$chunk->all();

// [0, 1, 2]
```

음수 값을 지정하면 컬렉션 끝에서부터 해당 개수만큼의 아이템을 가져옵니다.

```php
$collection = collect([0, 1, 2, 3, 4, 5]);

$chunk = $collection->take(-2);

$chunk->all();

// [4, 5]
```

<a name="method-takeuntil"></a>
#### `takeUntil()`

`takeUntil` 메서드는 주어진 콜백이 `true`를 반환할 때까지 컬렉션의 아이템을 반환합니다.

```php
$collection = collect([1, 2, 3, 4]);

$subset = $collection->takeUntil(function (int $item) {
    return $item >= 3;
});

$subset->all();

// [1, 2]
```

단순한 값을 전달해서, 해당 값이 등장할 때까지의 아이템을 가져올 수도 있습니다.

```php
$collection = collect([1, 2, 3, 4]);

$subset = $collection->takeUntil(3);

$subset->all();

// [1, 2]
```

> [!WARNING]
> 주어진 값이 컬렉션에 없거나 콜백이 한 번도 `true`를 반환하지 않으면, `takeUntil` 메서드는 컬렉션의 모든 아이템을 반환합니다.

<a name="method-takewhile"></a>
#### `takeWhile()`

`takeWhile` 메서드는 주어진 콜백이 `false`를 반환할 때까지 컬렉션의 아이템을 반환합니다.

```php
$collection = collect([1, 2, 3, 4]);

$subset = $collection->takeWhile(function (int $item) {
    return $item < 3;
});

$subset->all();

// [1, 2]
```

> [!WARNING]
> 만약 콜백이 한 번도 `false`를 반환하지 않으면, `takeWhile` 메서드는 컬렉션의 모든 아이템을 반환합니다.

<a name="method-tap"></a>
#### `tap()`

`tap` 메서드는 현재 컬렉션을 지정한 콜백에 전달하여, 원하는 시점에 컬렉션의 값을 확인하거나 다른 작업을 할 수 있도록 해줍니다. 이 메서드는 컬렉션 자체에는 영향을 주지 않으며, 호출 후에는 원래의 컬렉션을 반환합니다.

```php
collect([2, 4, 3, 1, 5])
    ->sort()
    ->tap(function (Collection $collection) {
        Log::debug('Values after sorting', $collection->values()->all());
    })
    ->shift();

// 1
```

<a name="method-times"></a>
#### `times()`

정적 메서드인 `times`는 지정한 횟수만큼 클로저를 실행하여 반환된 값으로 새로운 컬렉션을 만듭니다.

```php
$collection = Collection::times(10, function (int $number) {
    return $number * 9;
});

$collection->all();

// [9, 18, 27, 36, 45, 54, 63, 72, 81, 90]
```

<a name="method-toarray"></a>
#### `toArray()`

`toArray` 메서드는 컬렉션을 일반 PHP `array`로 변환합니다. 컬렉션의 항목이 [Eloquent](/docs/12.x/eloquent) 모델인 경우, 모델도 배열로 변환됩니다.

```php
$collection = collect(['name' => 'Desk', 'price' => 200]);

$collection->toArray();

/*
    [
        ['name' => 'Desk', 'price' => 200],
    ]
*/
```

> [!WARNING]
> `toArray`는 컬렉션의 모든 중첩 객체 중 `Arrayable` 인스턴스도 배열로 변환합니다. 만약 컬렉션의 실제 배열 데이터만 얻고 싶다면, [all](#method-all) 메서드를 사용하세요.

<a name="method-tojson"></a>
#### `toJson()`

`toJson` 메서드는 컬렉션을 JSON 직렬화된 문자열로 변환합니다.

```php
$collection = collect(['name' => 'Desk', 'price' => 200]);

$collection->toJson();

// '{"name":"Desk", "price":200}'
```

<a name="method-transform"></a>
#### `transform()`

`transform` 메서드는 컬렉션의 각 아이템에 대해 주어진 콜백을 호출하며, 콜백에서 반환된 값으로 컬렉션의 아이템을 모두 대체합니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->transform(function (int $item, int $key) {
    return $item * 2;
});

$collection->all();

// [2, 4, 6, 8, 10]
```

> [!WARNING]
> 대부분의 컬렉션 메서드와 달리, `transform`은 컬렉션 자체를 변경합니다. 새로운 컬렉션을 생성하고 싶다면 [map](#method-map) 메서드를 사용하세요.

<a name="method-undot"></a>
#### `undot()`

`undot` 메서드는 일차원 컬렉션(평면 배열)이 "닷(dot)" 표기법을 사용하는 경우, 이를 다차원 컬렉션으로 확장합니다.

```php
$person = collect([
    'name.first_name' => 'Marie',
    'name.last_name' => 'Valentine',
    'address.line_1' => '2992 Eagle Drive',
    'address.line_2' => '',
    'address.suburb' => 'Detroit',
    'address.state' => 'MI',
    'address.postcode' => '48219'
]);

$person = $person->undot();

$person->toArray();

/*
    [
        "name" => [
            "first_name" => "Marie",
            "last_name" => "Valentine",
        ],
        "address" => [
            "line_1" => "2992 Eagle Drive",
            "line_2" => "",
            "suburb" => "Detroit",
            "state" => "MI",
            "postcode" => "48219",
        ],
    ]
*/
```

<a name="method-union"></a>
#### `union()`

`union` 메서드는 전달된 배열을 컬렉션에 추가합니다. 추가되는 배열에 원래 컬렉션에 있는 키가 존재할 경우, 컬렉션의 값이 우선적으로 유지됩니다.

```php
$collection = collect([1 => ['a'], 2 => ['b']]);

$union = $collection->union([3 => ['c'], 1 => ['d']]);

$union->all();

// [1 => ['a'], 2 => ['b'], 3 => ['c']]
```

<a name="method-unique"></a>
#### `unique()`

`unique` 메서드는 컬렉션에서 중복되지 않는(고유한) 모든 항목을 반환합니다. 반환된 컬렉션은 원본 배열의 키를 그대로 유지하므로, 연속된 숫자 인덱스가 필요하다면 [values](#method-values) 메서드를 사용하세요.

```php
$collection = collect([1, 1, 2, 2, 3, 4, 2]);

$unique = $collection->unique();

$unique->values()->all();

// [1, 2, 3, 4]
```

중첩 배열이나 객체의 컬렉션에서 고유값을 판단할 특정 키를 지정할 수도 있습니다.

```php
$collection = collect([
    ['name' => 'iPhone 6', 'brand' => 'Apple', 'type' => 'phone'],
    ['name' => 'iPhone 5', 'brand' => 'Apple', 'type' => 'phone'],
    ['name' => 'Apple Watch', 'brand' => 'Apple', 'type' => 'watch'],
    ['name' => 'Galaxy S6', 'brand' => 'Samsung', 'type' => 'phone'],
    ['name' => 'Galaxy Gear', 'brand' => 'Samsung', 'type' => 'watch'],
]);

$unique = $collection->unique('brand');

$unique->values()->all();

/*
    [
        ['name' => 'iPhone 6', 'brand' => 'Apple', 'type' => 'phone'],
        ['name' => 'Galaxy S6', 'brand' => 'Samsung', 'type' => 'phone'],
    ]
*/
```

마지막으로, 어떤 값으로 고유성을 판단할지 결정하기 위해 직접 클로저를 전달할 수도 있습니다.

```php
$unique = $collection->unique(function (array $item) {
    return $item['brand'].$item['type'];
});

$unique->values()->all();

/*
    [
        ['name' => 'iPhone 6', 'brand' => 'Apple', 'type' => 'phone'],
        ['name' => 'Apple Watch', 'brand' => 'Apple', 'type' => 'watch'],
        ['name' => 'Galaxy S6', 'brand' => 'Samsung', 'type' => 'phone'],
        ['name' => 'Galaxy Gear', 'brand' => 'Samsung', 'type' => 'watch'],
    ]
*/
```

`unique` 메서드는 비교 시 "느슨한(loose)" 비교를 사용합니다. 즉, '123'(문자열)과 123(정수)는 동일한 값으로 간주합니다. "엄격한(strict)" 비교를 통해 중복을 제거하고 싶다면 [uniqueStrict](#method-uniquestrict) 메서드를 사용하세요.

> [!NOTE]
> 이 메서드는 [Eloquent 컬렉션](/docs/12.x/eloquent-collections#method-unique)에서 동작 방식이 다를 수 있습니다.

<a name="method-uniquestrict"></a>
#### `uniqueStrict()`

이 메서드는 [unique](#method-unique) 메서드와 시그니처가 동일하지만, 모든 값을 "엄격(strict)"하게 비교하여 필터링합니다.

<a name="method-unless"></a>
#### `unless()`

`unless` 메서드는 첫 번째 인수가 `true`로 평가되지 않을 때, 주어진 콜백을 실행합니다. 이때 컬렉션 인스턴스와 첫 번째 인수가 콜백에 전달됩니다.

```php
$collection = collect([1, 2, 3]);

$collection->unless(true, function (Collection $collection, bool $value) {
    return $collection->push(4);
});

$collection->unless(false, function (Collection $collection, bool $value) {
    return $collection->push(5);
});

$collection->all();

// [1, 2, 3, 5]
```

`unless` 메서드에 두 번째 콜백을 전달할 수도 있습니다. 이 경우, 첫 번째 인수가 `true`일 때 두 번째 콜백이 실행됩니다.

```php
$collection = collect([1, 2, 3]);

$collection->unless(true, function (Collection $collection, bool $value) {
    return $collection->push(4);
}, function (Collection $collection, bool $value) {
    return $collection->push(5);
});

$collection->all();

// [1, 2, 3, 5]
```

`unless`의 반대 동작을 원한다면 [when](#method-when) 메서드를 참고하세요.

<a name="method-unlessempty"></a>
#### `unlessEmpty()`

[whenNotEmpty](#method-whennotempty) 메서드의 별칭입니다.

<a name="method-unlessnotempty"></a>
#### `unlessNotEmpty()`

[whenEmpty](#method-whenempty) 메서드의 별칭입니다.

<a name="method-unwrap"></a>
#### `unwrap()`

정적 메서드인 `unwrap`은 적용 가능한 경우 전달된 값에서 컬렉션의 실제 아이템만 반환합니다.

```php
Collection::unwrap(collect('John Doe'));

// ['John Doe']

Collection::unwrap(['John Doe']);

// ['John Doe']

Collection::unwrap('John Doe');

// 'John Doe'
```

<a name="method-value"></a>

#### `value()`

`value` 메서드는 컬렉션의 첫 번째 요소에서 지정한 값을 가져옵니다.

```php
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Speaker', 'price' => 400],
]);

$value = $collection->value('price');

// 200
```

<a name="method-values"></a>
#### `values()`

`values` 메서드는 키를 0부터 시작하는 연속된 정수로 재설정한 새로운 컬렉션을 반환합니다.

```php
$collection = collect([
    10 => ['product' => 'Desk', 'price' => 200],
    11 => ['product' => 'Desk', 'price' => 200],
]);

$values = $collection->values();

$values->all();

/*
    [
        0 => ['product' => 'Desk', 'price' => 200],
        1 => ['product' => 'Desk', 'price' => 200],
    ]
*/
```

<a name="method-when"></a>
#### `when()`

`when` 메서드는 첫 번째 인자로 전달된 값이 `true`로 평가될 때, 주어진 콜백을 실행합니다. 이 콜백에는 컬렉션 인스턴스와 `when` 메서드에 전달된 첫 번째 인자가 함께 전달됩니다.

```php
$collection = collect([1, 2, 3]);

$collection->when(true, function (Collection $collection, bool $value) {
    return $collection->push(4);
});

$collection->when(false, function (Collection $collection, bool $value) {
    return $collection->push(5);
});

$collection->all();

// [1, 2, 3, 4]
```

`when` 메서드에는 두 번째 콜백을 전달할 수도 있습니다. 첫 번째 인자가 `false`로 평가될 때는 이 두 번째 콜백이 실행됩니다.

```php
$collection = collect([1, 2, 3]);

$collection->when(false, function (Collection $collection, bool $value) {
    return $collection->push(4);
}, function (Collection $collection, bool $value) {
    return $collection->push(5);
});

$collection->all();

// [1, 2, 3, 5]
```

`when`의 반대 동작에 대해서는 [unless](#method-unless) 메서드를 참고하시기 바랍니다.

<a name="method-whenempty"></a>
#### `whenEmpty()`

`whenEmpty` 메서드는 컬렉션이 비어 있을 때 주어진 콜백을 실행합니다.

```php
$collection = collect(['Michael', 'Tom']);

$collection->whenEmpty(function (Collection $collection) {
    return $collection->push('Adam');
});

$collection->all();

// ['Michael', 'Tom']

$collection = collect();

$collection->whenEmpty(function (Collection $collection) {
    return $collection->push('Adam');
});

$collection->all();

// ['Adam']
```

`whenEmpty` 메서드에도 두 번째 클로저를 전달할 수 있는데, 이 클로저는 컬렉션이 비어 있지 않을 때 실행됩니다.

```php
$collection = collect(['Michael', 'Tom']);

$collection->whenEmpty(function (Collection $collection) {
    return $collection->push('Adam');
}, function (Collection $collection) {
    return $collection->push('Taylor');
});

$collection->all();

// ['Michael', 'Tom', 'Taylor']
```

`whenEmpty`의 반대 동작은 [whenNotEmpty](#method-whennotempty) 메서드를 참고하세요.

<a name="method-whennotempty"></a>
#### `whenNotEmpty()`

`whenNotEmpty` 메서드는 컬렉션이 비어 있지 않을 때 주어진 콜백을 실행합니다.

```php
$collection = collect(['Michael', 'Tom']);

$collection->whenNotEmpty(function (Collection $collection) {
    return $collection->push('Adam');
});

$collection->all();

// ['Michael', 'Tom', 'Adam']

$collection = collect();

$collection->whenNotEmpty(function (Collection $collection) {
    return $collection->push('Adam');
});

$collection->all();

// []
```

`whenNotEmpty` 메서드에도 두 번째 클로저를 전달할 수 있으며, 컬렉션이 비어 있을 때 이 클로저가 실행됩니다.

```php
$collection = collect();

$collection->whenNotEmpty(function (Collection $collection) {
    return $collection->push('Adam');
}, function (Collection $collection) {
    return $collection->push('Taylor');
});

$collection->all();

// ['Taylor']
```

`whenNotEmpty`의 반대 동작은 [whenEmpty](#method-whenempty) 메서드를 참고하세요.

<a name="method-where"></a>
#### `where()`

`where` 메서드는 주어진 키/값 쌍을 기준으로 컬렉션을 필터링합니다.

```php
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
    ['product' => 'Bookcase', 'price' => 150],
    ['product' => 'Door', 'price' => 100],
]);

$filtered = $collection->where('price', 100);

$filtered->all();

/*
    [
        ['product' => 'Chair', 'price' => 100],
        ['product' => 'Door', 'price' => 100],
    ]
*/
```

`where` 메서드는 값 비교 시 "느슨한(loose) 비교"를 사용합니다. 즉, 값이 정수인 문자열과 해당 정수는 같다고 간주됩니다. "엄격한(strict) 비교"가 필요한 경우 [whereStrict](#method-wherestrict) 메서드를 사용하세요.

또한, 두 번째 인자로 비교 연산자를 지정할 수 있습니다. 지원되는 연산자는 다음과 같습니다: '===', '!==', '!=', '==', '=', '<>', '>', '<', '>=', '<='

```php
$collection = collect([
    ['name' => 'Jim', 'deleted_at' => '2019-01-01 00:00:00'],
    ['name' => 'Sally', 'deleted_at' => '2019-01-02 00:00:00'],
    ['name' => 'Sue', 'deleted_at' => null],
]);

$filtered = $collection->where('deleted_at', '!=', null);

$filtered->all();

/*
    [
        ['name' => 'Jim', 'deleted_at' => '2019-01-01 00:00:00'],
        ['name' => 'Sally', 'deleted_at' => '2019-01-02 00:00:00'],
    ]
*/
```

<a name="method-wherestrict"></a>
#### `whereStrict()`

이 메서드는 [where](#method-where) 메서드와 동일한 시그니처를 가지며, 값을 "엄격하게(strict)" 비교하여 필터링합니다.

<a name="method-wherebetween"></a>
#### `whereBetween()`

`whereBetween` 메서드는 지정한 아이템의 값이 주어진 범위 내에 있는지를 기준으로 컬렉션을 필터링합니다.

```php
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 80],
    ['product' => 'Bookcase', 'price' => 150],
    ['product' => 'Pencil', 'price' => 30],
    ['product' => 'Door', 'price' => 100],
]);

$filtered = $collection->whereBetween('price', [100, 200]);

$filtered->all();

/*
    [
        ['product' => 'Desk', 'price' => 200],
        ['product' => 'Bookcase', 'price' => 150],
        ['product' => 'Door', 'price' => 100],
    ]
*/
```

<a name="method-wherein"></a>
#### `whereIn()`

`whereIn` 메서드는 지정한 값 배열에 포함되지 않은 요소를 컬렉션에서 제거합니다.

```php
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
    ['product' => 'Bookcase', 'price' => 150],
    ['product' => 'Door', 'price' => 100],
]);

$filtered = $collection->whereIn('price', [150, 200]);

$filtered->all();

/*
    [
        ['product' => 'Desk', 'price' => 200],
        ['product' => 'Bookcase', 'price' => 150],
    ]
*/
```

`whereIn` 메서드 또한 값 비교 시 "느슨한(loose) 비교"를 사용합니다. "엄격한(strict) 비교"가 필요하다면 [whereInStrict](#method-whereinstrict) 메서드를 사용하세요.

<a name="method-whereinstrict"></a>
#### `whereInStrict()`

이 메서드는 [whereIn](#method-wherein) 메서드와 동일한 시그니처를 가지며, 값을 "엄격하게(strict)" 비교하여 필터링합니다.

<a name="method-whereinstanceof"></a>
#### `whereInstanceOf()`

`whereInstanceOf` 메서드는 주어진 클래스 타입을 기준으로 컬렉션을 필터링합니다.

```php
use App\Models\User;
use App\Models\Post;

$collection = collect([
    new User,
    new User,
    new Post,
]);

$filtered = $collection->whereInstanceOf(User::class);

$filtered->all();

// [App\Models\User, App\Models\User]
```

<a name="method-wherenotbetween"></a>
#### `whereNotBetween()`

`whereNotBetween` 메서드는 지정한 아이템의 값이 주어진 범위 밖에 있는지를 기준으로 컬렉션을 필터링합니다.

```php
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 80],
    ['product' => 'Bookcase', 'price' => 150],
    ['product' => 'Pencil', 'price' => 30],
    ['product' => 'Door', 'price' => 100],
]);

$filtered = $collection->whereNotBetween('price', [100, 200]);

$filtered->all();

/*
    [
        ['product' => 'Chair', 'price' => 80],
        ['product' => 'Pencil', 'price' => 30],
    ]
*/
```

<a name="method-wherenotin"></a>
#### `whereNotIn()`

`whereNotIn` 메서드는 지정한 값 배열에 포함된 값을 가진 요소를 컬렉션에서 제거합니다.

```php
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
    ['product' => 'Bookcase', 'price' => 150],
    ['product' => 'Door', 'price' => 100],
]);

$filtered = $collection->whereNotIn('price', [150, 200]);

$filtered->all();

/*
    [
        ['product' => 'Chair', 'price' => 100],
        ['product' => 'Door', 'price' => 100],
    ]
*/
```

`whereNotIn` 메서드도 값 비교 시 "느슨한(loose) 비교"를 사용합니다. "엄격한(strict) 비교"를 하려면 [whereNotInStrict](#method-wherenotinstrict) 메서드를 이용하세요.

<a name="method-wherenotinstrict"></a>
#### `whereNotInStrict()`

이 메서드는 [whereNotIn](#method-wherenotin) 메서드와 동일한 시그니처를 가지며, 값을 "엄격하게(strict)" 비교하여 필터링합니다.

<a name="method-wherenotnull"></a>
#### `whereNotNull()`

`whereNotNull` 메서드는 주어진 키의 값이 `null`이 아닌 컬렉션 내의 요소만 반환합니다.

```php
$collection = collect([
    ['name' => 'Desk'],
    ['name' => null],
    ['name' => 'Bookcase'],
]);

$filtered = $collection->whereNotNull('name');

$filtered->all();

/*
    [
        ['name' => 'Desk'],
        ['name' => 'Bookcase'],
    ]
*/
```

<a name="method-wherenull"></a>
#### `whereNull()`

`whereNull` 메서드는 주어진 키의 값이 `null`인 컬렉션 내의 요소만 반환합니다.

```php
$collection = collect([
    ['name' => 'Desk'],
    ['name' => null],
    ['name' => 'Bookcase'],
]);

$filtered = $collection->whereNull('name');

$filtered->all();

/*
    [
        ['name' => null],
    ]
*/
```

<a name="method-wrap"></a>
#### `wrap()`

정적 메서드인 `wrap`은 전달된 값을 적합하면 컬렉션으로 감쌉니다.

```php
use Illuminate\Support\Collection;

$collection = Collection::wrap('John Doe');

$collection->all();

// ['John Doe']

$collection = Collection::wrap(['John Doe']);

$collection->all();

// ['John Doe']

$collection = Collection::wrap(collect('John Doe'));

$collection->all();

// ['John Doe']
```

<a name="method-zip"></a>
#### `zip()`

`zip` 메서드는 원본 컬렉션의 값과 주어진 배열의 값을 같은 인덱스끼리 합쳐 반환합니다.

```php
$collection = collect(['Chair', 'Desk']);

$zipped = $collection->zip([100, 200]);

$zipped->all();

// [['Chair', 100], ['Desk', 200]]
```

<a name="higher-order-messages"></a>
## 하이어 오더 메시지(Higher Order Messages)

컬렉션은 "하이어 오더 메시지(Higher Order Message)"도 지원합니다. 이는 컬렉션에서 자주 사용하는 메서드 호출을 더 간편하게 작성할 수 있는 문법입니다. 하이어 오더 메시지를 제공하는 컬렉션 메서드는 다음과 같습니다: [average](#method-average), [avg](#method-avg), [contains](#method-contains), [each](#method-each), [every](#method-every), [filter](#method-filter), [first](#method-first), [flatMap](#method-flatmap), [groupBy](#method-groupby), [keyBy](#method-keyby), [map](#method-map), [max](#method-max), [min](#method-min), [partition](#method-partition), [reject](#method-reject), [skipUntil](#method-skipuntil), [skipWhile](#method-skipwhile), [some](#method-some), [sortBy](#method-sortby), [sortByDesc](#method-sortbydesc), [sum](#method-sum), [takeUntil](#method-takeuntil), [takeWhile](#method-takewhile), [unique](#method-unique).

각 하이어 오더 메시지는 컬렉션 인스턴스의 동적 프로퍼티로 접근할 수 있습니다. 예를 들어, `each` 하이어 오더 메시지를 사용해 컬렉션의 각 객체마다 메서드를 호출해볼 수 있습니다.

```php
use App\Models\User;

$users = User::where('votes', '>', 500)->get();

$users->each->markAsVip();
```

이와 같이 `sum` 하이어 오더 메시지를 사용해 사용자 컬렉션의 "votes" 총합을 구할 수 있습니다.

```php
$users = User::where('group', 'Development')->get();

return $users->sum->votes;
```

<a name="lazy-collections"></a>
## 레이지 컬렉션(Lazy Collections)

<a name="lazy-collection-introduction"></a>
### 소개

> [!WARNING]
> 라라벨의 레이지 컬렉션을 학습하기 전에, 먼저 [PHP 제너레이터](https://www.php.net/manual/en/language.generators.overview.php)에 대해 익혀두시는 것이 좋습니다.

이미 강력한 `Collection` 클래스 외에, `LazyCollection` 클래스는 PHP의 [제너레이터(generator)](https://www.php.net/manual/en/language.generators.overview.php) 기능을 활용해 아주 큰 데이터셋을 메모리 사용량을 최소화하며 처리할 수 있게 해줍니다.

예를 들어, 애플리케이션에서 수 기가바이트(GB) 크기의 로그 파일을 읽으며 라라벨의 컬렉션 메서드로 파싱하고 싶다고 가정해봅시다. 전체 로그 파일을 한 번에 메모리로 모두 읽지 않고, 레이지 컬렉션을 사용해 한 번에 일부 데이터만 메모리에 올리면서 작업할 수 있습니다.

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

또는, 10,000개의 Eloquent 모델을 반복(iterate)해야 하는 경우를 생각해봅시다. 일반적인 라라벨 컬렉션을 사용하면 10,000개 모델을 한 번에 메모리에 모두 로드해야 합니다.

```php
use App\Models\User;

$users = User::all()->filter(function (User $user) {
    return $user->id > 500;
});
```

하지만 쿼리 빌더의 `cursor` 메서드는 `LazyCollection` 인스턴스를 반환합니다. 이를 사용하면 실제로 데이터베이스 쿼리는 한 번만 실행되고, 동시에 메모리엔 한 번에 하나의 Eloquent 모델만 유지할 수 있습니다. 아래 예제에서처럼, 실제로 각 유저를 반복해서 순회할 때 필터 콜백이 실행되므로 메모리 사용량을 크게 줄일 수 있습니다.

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
### 레이지 컬렉션 생성하기

레이지 컬렉션 인스턴스를 생성하려면, 컬렉션의 `make` 메서드에 PHP 제너레이터 함수를 전달해야 합니다.

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

`Collection` 클래스에서 사용할 수 있는 거의 모든 메서드는 `LazyCollection` 클래스에서도 사용할 수 있습니다. 두 클래스 모두 `Illuminate\Support\Enumerable` 계약(Contract)을 구현하며, 이 인터페이스에는 다음과 같은 메서드가 정의되어 있습니다.



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
> 컬렉션의 내용을 변경하는(`shift`, `pop`, `prepend` 등) 메서드는 `LazyCollection` 클래스에서는 **사용할 수 없습니다**.

<a name="lazy-collection-methods"></a>
### 레이지 컬렉션 전용 메서드

`Enumerable` 계약에 정의된 메서드 외에도, `LazyCollection` 클래스에는 다음과 같은 추가 메서드가 있습니다.

<a name="method-takeUntilTimeout"></a>
#### `takeUntilTimeout()`

`takeUntilTimeout` 메서드는 지정된 시점까지 값을 열거(enumerate)하는 새로운 레이지 컬렉션을 반환합니다. 해당 시간이 지난 후에는 열거를 멈춥니다.

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

이 메서드의 사용 예시로, 데이터베이스에서 커서를 사용해 송장(invoices)을 제출하는 애플리케이션을 상상해보세요. 예를 들어, [스케줄링된 작업](/docs/12.x/scheduling)을 15분마다 실행하되, 송장은 최대 14분 동안만 처리하도록 할 수 있습니다.

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

`each` 메서드는 컬렉션의 각 항목에 대해 즉시 주어진 콜백을 호출하는 반면, `tapEach` 메서드는 리스트에서 항목을 하나씩 꺼낼 때마다 콜백을 호출합니다.

```php
// 현재까지 아무 값도 dump되지 않았습니다...
$lazyCollection = LazyCollection::times(INF)->tapEach(function (int $value) {
    dump($value);
});

// 세 개의 값이 dump됩니다...
$array = $lazyCollection->take(3)->all();

// 1
// 2
// 3
```

<a name="method-throttle"></a>
#### `throttle()`

`throttle` 메서드는 레이지 컬렉션(lazy collection)이 지정된 초(seconds)만큼 간격을 두고 각 값을 반환하도록 합니다. 이 메서드는 주로 외부 API와 상호 작용할 때, 요청 빈도 제한(rate limit)이 걸려 있는 상황에서 유용하게 사용할 수 있습니다.

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

`remember` 메서드는 컬렉션을 열거(순회)할 때, 이미 조회한 값은 기억(캐시)해서 이후 동일 데이터를 다시 꺼내지 않도록 하는 새로운 레이지 컬렉션(lazy collection)을 반환합니다.

```php
// 아직 쿼리가 실행되지 않았습니다...
$users = User::cursor()->remember();

// 쿼리가 실행됩니다...
// 첫 5명의 사용자가 데이터베이스에서 조회(hydrate)됩니다...
$users->take(5)->all();

// 첫 5명의 사용자는 컬렉션의 캐시에서 가져오고...
// 나머지는 데이터베이스에서 새로 조회됩니다...
$users->take(20)->all();
```