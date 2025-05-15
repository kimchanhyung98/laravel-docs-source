# 컬렉션 (Collections)

- [소개](#introduction)
    - [컬렉션 생성](#creating-collections)
    - [컬렉션 확장](#extending-collections)
- [사용 가능한 메서드](#available-methods)
- [고차 메시지(Higher Order Messages)](#higher-order-messages)
- [레이지 컬렉션(Lazy Collections)](#lazy-collections)
    - [소개](#lazy-collection-introduction)
    - [레이지 컬렉션 생성](#creating-lazy-collections)
    - [Enumerable 계약](#the-enumerable-contract)
    - [레이지 컬렉션 메서드](#lazy-collection-methods)

<a name="introduction"></a>
## 소개

`Illuminate\Support\Collection` 클래스는 데이터 배열을 다루기 위한 유연하고 편리한 래퍼(wrapper)를 제공합니다. 예를 들어, 아래 코드를 보시면 `collect` 헬퍼를 이용해 배열로부터 새로운 컬렉션 인스턴스를 만들고, 각 요소에 대해 `strtoupper` 함수를 실행한 뒤에, 비어 있는 모든 요소를 제거합니다.

```php
$collection = collect(['taylor', 'abigail', null])->map(function (?string $name) {
    return strtoupper($name);
})->reject(function (string $name) {
    return empty($name);
});
```

보시는 것처럼, `Collection` 클래스는 메서드 체이닝을 통해 배열에 대한 연속적인 맵(mapping) 및 축소(reducing) 작업을 손쉽게 수행할 수 있습니다. 일반적으로 컬렉션은 불변(immutable) 객체이며, 모든 `Collection` 메서드는 항상 완전히 새로운 `Collection` 인스턴스를 반환합니다.

<a name="creating-collections"></a>
### 컬렉션 생성

앞서 설명한 것처럼, `collect` 헬퍼는 전달된 배열을 기반으로 새로운 `Illuminate\Support\Collection` 인스턴스를 반환합니다. 즉, 컬렉션을 생성하는 것은 다음과 같이 매우 간단합니다.

```php
$collection = collect([1, 2, 3]);
```

[make](#method-make) 메서드와 [fromJson](#method-fromjson) 메서드를 사용해 컬렉션을 생성하는 것도 가능합니다.

> [!NOTE]
> [Eloquent](/docs/12.x/eloquent) 쿼리의 결과는 항상 `Collection` 인스턴스로 반환됩니다.

<a name="extending-collections"></a>
### 컬렉션 확장

컬렉션은 "매크로 등록이 가능(macroable)"하므로 실행 중에 `Collection` 클래스에 사용자 정의 메서드를 추가할 수 있습니다. `Illuminate\Support\Collection` 클래스의 `macro` 메서드는 매크로가 호출될 때 실행될 클로저를 받습니다. 이 클로저 내에서는 `$this`를 이용해 컬렉션의 다른 메서드에 접근할 수 있으므로, 실제 컬렉션 클래스의 메서드를 작성하는 것처럼 사용할 수 있습니다. 예를 들어, 아래 코드는 `Collection` 클래스에 `toUpper`라는 메서드를 추가합니다.

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

필요하다면, 매크로에서 추가 인수를 받을 수도 있습니다.

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

이후 컬렉션 문서의 대부분에서는 `Collection` 클래스에서 제공하는 각 메서드에 대해 설명합니다. 모든 메서드는 체이닝이 가능해, 기본 배열에 대해 유연하게 조작을 이어갈 수 있습니다. 또한 대부분의 메서드는 새로운 `Collection` 인스턴스를 반환하므로, 필요하다면 원본 컬렉션을 그대로 남겨둘 수 있습니다.



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

`after` 메서드는 주어진 항목 바로 다음에 위치한 값을 반환합니다. 만약 해당 항목이 없거나 마지막 항목이라면 `null`이 반환됩니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->after(3);

// 4

$collection->after(5);

// null
```

이 메서드는 "느슨한(loose)" 비교를 사용해 주어진 항목을 찾습니다. 즉, 정수 값을 포함하는 문자열이라도 같은 값의 정수와 같다고 간주합니다. "엄격한(strict)" 비교를 사용하려면, `strict` 인수를 추가로 전달할 수 있습니다.

```php
collect([2, 4, 6, 8])->after('4', strict: true);

// null
```

또는, 콜백을 전달해 조건을 충족하는 첫 번째 항목 다음 값을 가져올 수도 있습니다.

```php
collect([2, 4, 6, 8])->after(function (int $item, int $key) {
    return $item > 5;
});

// 8
```

<a name="method-all"></a>
#### `all()`

`all` 메서드는 컬렉션이 감싸고 있는 실제 배열을 그대로 반환합니다.

```php
collect([1, 2, 3])->all();

// [1, 2, 3]
```

<a name="method-average"></a>
#### `average()`

[avg](#method-avg) 메서드의 별칭입니다.

<a name="method-avg"></a>
#### `avg()`

`avg` 메서드는 지정된 키의 [평균값](https://en.wikipedia.org/wiki/Average)을 반환합니다.

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

`before` 메서드는 [after](#method-after) 메서드와 반대 동작을 합니다. 주어진 항목 바로 앞에 있는 값을 반환합니다. 만약 해당 항목이 없거나 첫 번째 항목이라면 `null`이 반환됩니다.

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

`chunk` 메서드는 컬렉션을 지정한 크기만큼 여러 개의 작은 컬렉션으로 나누어줍니다.

```php
$collection = collect([1, 2, 3, 4, 5, 6, 7]);

$chunks = $collection->chunk(4);

$chunks->all();

// [[1, 2, 3, 4], [5, 6, 7]]
```

이 메서드는 [Bootstrap](https://getbootstrap.com/docs/5.3/layout/grid/)과 같은 그리드 시스템이 적용된 [뷰](/docs/12.x/views)에서 컬렉션을 사용할 때 특히 유용합니다. 예를 들어, 여러 개의 [Eloquent](/docs/12.x/eloquent) 모델을 격자 형태로 출력한다면 아래처럼 활용할 수 있습니다.

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

`chunkWhile` 메서드는 전달한 콜백의 판단 결과에 따라 컬렉션을 여러 개의 작은 컬렉션으로 분할합니다. 클로저에 전달되는 `$chunk` 변수로 직전 요소를 참고할 수 있습니다.

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

`collapse` 메서드는 배열 또는 컬렉션의 컬렉션을 하나의 평평한(flat) 컬렉션으로 합쳐줍니다.

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

`collapseWithKeys` 메서드는 배열 또는 컬렉션의 컬렉션을 하나의 컬렉션으로 평탄화하되, 원래의 키를 그대로 유지합니다.

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

`collect` 메서드는 현재 컬렉션이 담고 있는 값들로 새로운 `Collection` 인스턴스를 반환합니다.

```php
$collectionA = collect([1, 2, 3]);

$collectionB = $collectionA->collect();

$collectionB->all();

// [1, 2, 3]
```

이 메서드는 [레이지 컬렉션](#lazy-collections)을 일반적인 `Collection` 인스턴스로 변환할 때 주로 사용됩니다.

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
> `collect` 메서드는 `Enumerable` 인스턴스를 가지고 있고, 레이지 컬렉션이 아닌 일반 컬렉션 인스턴스가 필요한 경우에 특히 유용합니다. `collect()`는 `Enumerable` 계약의 일부이므로, 안전하게 `Collection` 인스턴스를 얻는 용도로 사용할 수 있습니다.

<a name="method-combine"></a>
#### `combine()`

`combine` 메서드는 현재 컬렉션의 값들을 키로 사용하고, 전달된 배열이나 컬렉션의 값들을 값으로 사용해 새로운 컬렉션을 만듭니다.

```php
$collection = collect(['name', 'age']);

$combined = $collection->combine(['George', 29]);

$combined->all();

// ['name' => 'George', 'age' => 29]
```

<a name="method-concat"></a>
#### `concat()`

`concat` 메서드는 전달된 배열이나 컬렉션의 값을 현재 컬렉션의 마지막에 이어붙입니다.

```php
$collection = collect(['John Doe']);

$concatenated = $collection->concat(['Jane Doe'])->concat(['name' => 'Johnny Doe']);

$concatenated->all();

// ['John Doe', 'Jane Doe', 'Johnny Doe']
```

`concat` 메서드는 이어 붙여진 항목의 키를 숫자 형태로 재정렬합니다. 연관 배열(associative collection)에서 키를 유지하려면 [merge](#method-merge) 메서드를 사용하세요.

<a name="method-contains"></a>
#### `contains()`

`contains` 메서드는 컬렉션에 특정 항목이 포함되어 있는지 확인합니다. 콜백을 전달하면, 해당 조건을 만족하는 요소가 컬렉션에 존재하는지 여부를 검사합니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->contains(function (int $value, int $key) {
    return $value > 5;
});

// false
```

또는, 문자열 값을 직접 전달해 컬렉션에 해당 값이 존재하는지 검사할 수 있습니다.

```php
$collection = collect(['name' => 'Desk', 'price' => 100]);

$collection->contains('Desk');

// true

$collection->contains('New York');

// false
```

키와 값의 쌍을 전달하여 컬렉션에 해당 쌍이 존재하는지 검사하는 것도 가능합니다.

```php
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
]);

$collection->contains('product', 'Bookcase');

// false
```

`contains` 메서드는 아이템 값을 검사할 때 "느슨한(loose)" 비교를 사용합니다. 즉, 정수 값을 포함한 문자열도 해당 정수 값과 같은 것으로 간주합니다. "엄격한(strict)" 비교를 하려면 [containsStrict](#method-containsstrict) 메서드를 이용하세요.

`contains`의 반대 동작을 하려면 [doesntContain](#method-doesntcontain) 메서드를 참고하세요.

<a name="method-containsoneitem"></a>
#### `containsOneItem()`

`containsOneItem` 메서드는 컬렉션에 단 하나의 항목만 존재하는지를 확인합니다.

```php
collect([])->containsOneItem();

// false

collect(['1'])->containsOneItem();

// true

collect(['1', '2'])->containsOneItem();

// false

collect([1, 2, 3])->containsOneItem(fn ($item) => $item === 2);

// true
```

<a name="method-containsstrict"></a>

#### `containsStrict()`

이 메서드는 [contains](#method-contains) 메서드와 동일한 시그니처를 가지지만, 모든 값의 비교를 "엄격(strict)"하게 수행합니다.

> [!NOTE]
> 이 메서드는 [Eloquent 컬렉션](/docs/12.x/eloquent-collections#method-contains)을 사용할 때 동작 방식이 달라집니다.

<a name="method-count"></a>
#### `count()`

`count` 메서드는 컬렉션에 있는 전체 아이템의 개수를 반환합니다.

```php
$collection = collect([1, 2, 3, 4]);

$collection->count();

// 4
```

<a name="method-countBy"></a>
#### `countBy()`

`countBy` 메서드는 컬렉션에서 값의 등장 횟수를 세어줍니다. 기본적으로, 컬렉션의 각 요소가 몇 번씩 등장하는지 계산해서, 특정 "타입"의 요소가 몇 개 있는지 구할 때 사용할 수 있습니다.

```php
$collection = collect([1, 2, 2, 2, 3]);

$counted = $collection->countBy();

$counted->all();

// [1 => 1, 2 => 3, 3 => 1]
```

또한, `countBy` 메서드에 클로저를 전달하여 특정 기준에 따라 사용자 정의 값을 기준으로 횟수를 셀 수도 있습니다.

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

`crossJoin` 메서드는 컬렉션의 값과 전달된 배열 또는 컬렉션들을 곱집합 형태로 결합해, 가능한 모든 조합(카티션 곱)을 반환합니다.

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

`dd` 메서드는 컬렉션의 아이템을 출력하고 스크립트 실행을 즉시 종료합니다.

```php
$collection = collect(['John Doe', 'Jane Doe']);

$collection->dd();

/*
    Collection {
        #items: array:2 [
            0 => "John Doe"
            1 => "Jane Doe"
        ]
    }
*/
```

코드를 종료하지 않고 컬렉션을 출력만 하고 싶다면 [dump](#method-dump) 메서드를 사용하세요.

<a name="method-diff"></a>
#### `diff()`

`diff` 메서드는 컬렉션을 전달받은 다른 컬렉션이나 일반 PHP 배열과 값 기준으로 비교합니다. 원본 컬렉션에는 있지만, 전달한 컬렉션에는 없는 값만 반환합니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$diff = $collection->diff([2, 4, 6, 8]);

$diff->all();

// [1, 3, 5]
```

> [!NOTE]
> 이 메서드는 [Eloquent 컬렉션](/docs/12.x/eloquent-collections#method-diff)을 사용할 때 동작 방식이 달라집니다.

<a name="method-diffassoc"></a>
#### `diffAssoc()`

`diffAssoc` 메서드는 컬렉션을 전달받은 다른 컬렉션이나 일반 PHP 배열과, 키와 값 모두를 기준으로 비교합니다. 원본 컬렉션에는 있지만 전달된 컬렉션에는 없는 키/값 쌍만 반환합니다.

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

`diffAssoc`와 달리, `diffAssocUsing`은 인덱스 비교를 위해 사용자 정의 콜백 함수를 받아들입니다.

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

콜백 함수는 0 보다 작거나 같거나 큰 정수를 반환하는 비교 함수여야 합니다. 더 자세한 내용은 PHP 공식 문서의 [array_diff_uassoc](https://www.php.net/array_diff_uassoc#refsect1-function.array-diff-uassoc-parameters) 설명을 참고하세요. `diffAssocUsing` 메서드는 내부적으로 이 함수와 동일하게 동작합니다.

<a name="method-diffkeys"></a>
#### `diffKeys()`

`diffKeys` 메서드는 컬렉션을 전달받은 다른 컬렉션이나 일반 PHP 배열과 키를 기준으로 비교합니다. 원본 컬렉션에는 있지만 전달된 컬렉션에는 없는 키/값 쌍만 반환합니다.

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

`doesntContain` 메서드는 컬렉션에 특정 아이템이 포함되어 있지 않은지 확인합니다. 클로저를 전달하여, 특정 조건을 만족하지 않는 요소가 컬렉션에 없는지 검사할 수도 있습니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->doesntContain(function (int $value, int $key) {
    return $value < 5;
});

// false
```

또한, 문자열을 직접 전달하여 컬렉션에 특정 값이 없는지 확인할 수도 있습니다.

```php
$collection = collect(['name' => 'Desk', 'price' => 100]);

$collection->doesntContain('Table');

// true

$collection->doesntContain('Desk');

// false
```

키/값 쌍을 전달해 해당 데이터가 컬렉션에 없는지 검사할 수도 있습니다.

```php
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
]);

$collection->doesntContain('product', 'Bookcase');

// true
```

`doesntContain` 메서드는 값의 비교에 "느슨한(loose)" 비교를 사용합니다. 즉, 문자열로 된 숫자 값과 숫자가 같은 값으로 간주됩니다.

<a name="method-dot"></a>
#### `dot()`

`dot` 메서드는 다차원 컬렉션을 "점(dot) 표기법"을 이용해 하나의 평면 컬렉션으로 변환해줍니다.

```php
$collection = collect(['products' => ['desk' => ['price' => 100]]]);

$flattened = $collection->dot();

$flattened->all();

// ['products.desk.price' => 100]
```

<a name="method-dump"></a>
#### `dump()`

`dump` 메서드는 컬렉션의 아이템을 출력합니다.

```php
$collection = collect(['John Doe', 'Jane Doe']);

$collection->dump();

/*
    Collection {
        #items: array:2 [
            0 => "John Doe"
            1 => "Jane Doe"
        ]
    }
*/
```

출력 후 스크립트 실행을 중지하려면 [dd](#method-dd) 메서드를 사용하세요.

<a name="method-duplicates"></a>
#### `duplicates()`

`duplicates` 메서드는 컬렉션에서 중복된 값을 찾아 반환합니다.

```php
$collection = collect(['a', 'b', 'a', 'c', 'b']);

$collection->duplicates();

// [2 => 'a', 4 => 'b']
```

컬렉션에 배열이나 객체가 들어있다면, 중복 여부를 검사할 속성의 키를 지정할 수도 있습니다.

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

이 메서드는 [duplicates](#method-duplicates) 메서드와 동일한 시그니처를 가지지만, 모든 값을 "엄격(strict)"하게 비교합니다.

<a name="method-each"></a>
#### `each()`

`each` 메서드는 컬렉션의 각 요소를 순회하면서, 각각의 요소를 콜백(클로저)에 전달합니다.

```php
$collection = collect([1, 2, 3, 4]);

$collection->each(function (int $item, int $key) {
    // ...
});
```

순회를 중단하고 싶을 때는 클로저에서 `false`를 반환하면 됩니다.

```php
$collection->each(function (int $item, int $key) {
    if (/* condition */) {
        return false;
    }
});
```

<a name="method-eachspread"></a>
#### `eachSpread()`

`eachSpread` 메서드는 컬렉션의 아이템을 순회하고, 중첩된 배열의 값들을 콜백의 별도 인수로 전달해줍니다.

```php
$collection = collect([['John Doe', 35], ['Jane Doe', 33]]);

$collection->eachSpread(function (string $name, int $age) {
    // ...
});
```

이때도 콜백에서 `false`를 반환하여 순회를 중단할 수 있습니다.

```php
$collection->eachSpread(function (string $name, int $age) {
    return false;
});
```

<a name="method-ensure"></a>
#### `ensure()`

`ensure` 메서드는 컬렉션의 모든 요소가 특정 타입 또는 타입 목록에 속하는지 확인할 때 사용합니다. 만약 그렇지 않은 요소가 있으면 `UnexpectedValueException` 예외가 발생합니다.

```php
return $collection->ensure(User::class);

return $collection->ensure([User::class, Customer::class]);
```

`string`, `int`, `float`, `bool`, `array`와 같은 원시 타입도 지정할 수 있습니다.

```php
return $collection->ensure('int');
```

> [!WARNING]
> `ensure` 메서드는 나중에 타입이 다른 요소가 추가되는 경우까지 보장하지는 않습니다.

<a name="method-every"></a>
#### `every()`

`every` 메서드는 컬렉션의 모든 요소가 주어진 조건을 만족하는지 확인할 때 사용합니다.

```php
collect([1, 2, 3, 4])->every(function (int $value, int $key) {
    return $value > 2;
});

// false
```

컬렉션이 비어 있다면, `every` 메서드는 항상 true를 반환합니다.

```php
$collection = collect([]);

$collection->every(function (int $value, int $key) {
    return $value > 2;
});

// true
```

<a name="method-except"></a>
#### `except()`

`except` 메서드는 지정한 키에 해당하는 아이템을 제외한 나머지 아이템만 반환합니다.

```php
$collection = collect(['product_id' => 1, 'price' => 100, 'discount' => false]);

$filtered = $collection->except(['price', 'discount']);

$filtered->all();

// ['product_id' => 1]
```

반대 동작을 원한다면 [only](#method-only) 메서드를 참고하세요.

> [!NOTE]
> 이 메서드는 [Eloquent 컬렉션](/docs/12.x/eloquent-collections#method-except)을 사용할 때 동작 방식이 달라집니다.

<a name="method-filter"></a>
#### `filter()`

`filter` 메서드는 전달한 콜백의 진위 검사 결과가 true인 요소만 남겨 컬렉션을 걸러냅니다.

```php
$collection = collect([1, 2, 3, 4]);

$filtered = $collection->filter(function (int $value, int $key) {
    return $value > 2;
});

$filtered->all();

// [3, 4]
```

콜백을 전달하지 않으면, "false"로 간주되는 모든 요소(null, false, 빈 문자열, 0, 빈 배열 등)가 삭제됩니다.

```php
$collection = collect([1, 2, 3, null, false, '', 0, []]);

$collection->filter()->all();

// [1, 2, 3]
```

반대 동작을 원하신다면 [reject](#method-reject) 메서드를 참고하세요.

<a name="method-first"></a>
#### `first()`

`first` 메서드는 전달된 진위 검사를 통과하는 컬렉션의 첫 번째 요소를 반환합니다.

```php
collect([1, 2, 3, 4])->first(function (int $value, int $key) {
    return $value > 2;
});

// 3
```

인자를 전달하지 않으면 컬렉션의 첫 번째 요소를 반환합니다. 컬렉션이 비어 있으면 `null`이 반환됩니다.

```php
collect([1, 2, 3, 4])->first();

// 1
```

<a name="method-first-or-fail"></a>
#### `firstOrFail()`

`firstOrFail` 메서드는 `first`와 동일하게 동작하지만, 결과가 없으면 `Illuminate\Support\ItemNotFoundException` 예외가 발생합니다.

```php
collect([1, 2, 3, 4])->firstOrFail(function (int $value, int $key) {
    return $value > 5;
});

// ItemNotFoundException 예외 발생...
```

인자를 전달하지 않고 호출하면 컬렉션의 첫 번째 요소를 반환합니다. 컬렉션이 비어 있으면 `Illuminate\Support\ItemNotFoundException` 예외가 발생합니다.

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

비교 연산자를 지정해 사용할 수도 있습니다.

```php
$collection->firstWhere('age', '>=', 18);

// ['name' => 'Diego', 'age' => 23]
```

[where](#method-where) 메서드처럼, 인자를 한 개만 전달하면 지정한 키의 값이 "truthy"인 첫 번째 요소를 반환합니다.

```php
$collection->firstWhere('age');

// ['name' => 'Linda', 'age' => 14]
```

<a name="method-flatmap"></a>
#### `flatMap()`

`flatMap` 메서드는 컬렉션을 순회하며 각 값을 콜백에 전달합니다. 콜백은 요소를 수정해서 반환할 수 있고, 이렇게 반환된 요소들이 한 단계만 평탄화(flatten)되어 새로운 컬렉션을 만듭니다.

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

`flatten` 메서드는 다차원 컬렉션을 한 차원으로 평탄하게 만듭니다.

```php
$collection = collect([
    'name' => 'taylor',
    'languages' => [
        'php', 'javascript'
    ]
]);

$flattened = $collection->flatten();

$flattened->all();

// ['taylor', 'php', 'javascript'];
```

필요하다면, 평탄화할 "깊이(depth)"를 인수로 지정할 수 있습니다.

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

이 예시에서, 깊이 인수를 생략하고 `flatten`을 호출하면 내부의 배열까지 모두 평탄화되어 `['iPhone 6S', 'Apple', 'Galaxy S7', 'Samsung']`이 됩니다. 깊이를 지정하면, 중첩된 배열이 몇 단계까지 평탄화될지 정할 수 있습니다.

<a name="method-flip"></a>

#### `flip()`

`flip` 메서드는 컬렉션의 키와 값을 서로 맞바꿉니다.

```php
$collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

$flipped = $collection->flip();

$flipped->all();

// ['taylor' => 'name', 'laravel' => 'framework']
```

<a name="method-forget"></a>
#### `forget()`

`forget` 메서드는 지정한 키에 해당하는 컬렉션의 항목을 제거합니다.

```php
$collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

// 키 하나 제거...
$collection->forget('name');

// ['framework' => 'laravel']

// 여러 키를 한 번에 제거...
$collection->forget(['name', 'framework']);

// []
```

> [!WARNING]
> 대부분의 다른 컬렉션 메서드와 달리, `forget` 메서드는 새로운 컬렉션을 반환하지 않습니다. 대신 호출된 컬렉션 자체를 직접 수정하고 반환합니다.

<a name="method-forpage"></a>
#### `forPage()`

`forPage` 메서드는 지정한 페이지에 나타날 항목들만을 담는 새로운 컬렉션을 반환합니다. 첫 번째 인수로 페이지 번호를, 두 번째 인수로 페이지당 보여줄 항목 수를 전달합니다.

```php
$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9]);

$chunk = $collection->forPage(2, 3);

$chunk->all();

// [4, 5, 6]
```

<a name="method-fromjson"></a>
#### `fromJson()`

정적 메서드인 `fromJson`은 주어진 JSON 문자열을 PHP의 `json_decode` 함수로 해석하여, 새로운 컬렉션 인스턴스를 생성합니다.

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

`get` 메서드는 지정한 키에 해당하는 값을 반환합니다. 해당 키가 존재하지 않으면 `null`이 반환됩니다.

```php
$collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

$value = $collection->get('name');

// taylor
```

두 번째 인수로 기본값을 전달할 수도 있습니다.

```php
$collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

$value = $collection->get('age', 34);

// 34
```

기본값 자리에 콜백을 전달하면, 지정한 키가 없을 때 콜백의 반환 값이 기본값으로 사용됩니다.

```php
$collection->get('email', function () {
    return 'taylor@example.com';
});

// taylor@example.com
```

<a name="method-groupby"></a>
#### `groupBy()`

`groupBy` 메서드는 컬렉션의 항목들을 지정한 키로 그룹화합니다.

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

문자열 키 대신 콜백을 전달할 수도 있습니다. 콜백은 각 항목을 그룹화할 기준값을 반환해야 합니다.

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

배열로 다수의 그룹화 기준을 전달할 수도 있습니다. 각 배열 항목은 다차원 배열에서 서로 다른 그룹화 레벨에 적용됩니다.

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

`has` 메서드는 지정한 키가 컬렉션 내에 존재하는지 여부를 확인합니다.

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

`hasAny` 메서드는 전달한 여러 키 중 하나라도 컬렉션에 존재하는지 확인합니다.

```php
$collection = collect(['account_id' => 1, 'product' => 'Desk', 'amount' => 5]);

$collection->hasAny(['product', 'price']);

// true

$collection->hasAny(['name', 'price']);

// false
```

<a name="method-implode"></a>
#### `implode()`

`implode` 메서드는 컬렉션의 항목들을 하나의 문자열로 결합합니다. 컬렉션이 배열이나 객체로 구성되어 있을 경우, 결합할 속성(attribute)의 키와 값을 구분할 "글루(glue)" 문자열을 전달해야 합니다.

```php
$collection = collect([
    ['account_id' => 1, 'product' => 'Desk'],
    ['account_id' => 2, 'product' => 'Chair'],
]);

$collection->implode('product', ', ');

// 'Desk, Chair'
```

컬렉션이 단순 문자열이나 숫자 값으로만 구성되어 있다면, 메서드에 "글루" 문자열만 전달하면 됩니다.

```php
collect([1, 2, 3, 4, 5])->implode('-');

// '1-2-3-4-5'
```

값들을 원하는 형식으로 가공해 결합하고 싶다면, `implode` 메서드에 클로저를 전달할 수 있습니다.

```php
$collection->implode(function (array $item, int $key) {
    return strtoupper($item['product']);
}, ', ');

// 'DESK, CHAIR'
```

<a name="method-intersect"></a>
#### `intersect()`

`intersect` 메서드는 원본 컬렉션에서 주어진 배열 또는 컬렉션에 존재하지 않는 값을 모두 제거합니다. 반환되는 컬렉션은 원본의 키를 그대로 유지합니다.

```php
$collection = collect(['Desk', 'Sofa', 'Chair']);

$intersect = $collection->intersect(['Desk', 'Chair', 'Bookcase']);

$intersect->all();

// [0 => 'Desk', 2 => 'Chair']
```

> [!NOTE]
> 이 메서드는 [Eloquent 컬렉션](/docs/12.x/eloquent-collections#method-intersect)을 사용할 때 동작이 다를 수 있습니다.

<a name="method-intersectusing"></a>
#### `intersectUsing()`

`intersectUsing` 메서드는 주어진 배열 또는 컬렉션과 비교해서 존재하지 않는 값을 제거할 때, 값 비교에 사용자 정의 콜백을 사용할 수 있습니다. 반환되는 컬렉션은 원본의 키를 그대로 유지합니다.

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

`intersectAssoc` 메서드는 원본 컬렉션과 다른 컬렉션 또는 배열을 비교하여, 두 컬렉션 모두에 존재하는 키/값 쌍만 반환합니다.

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

`intersectAssocUsing` 메서드는 원본 컬렉션과 다른 컬렉션 또는 배열을 비교하여, 사용자 정의 콜백을 이용해 키와 값의 동일 여부를 판단하고, 둘 다 만족하는 키/값 쌍만 반환합니다.

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

`intersectByKeys` 메서드는 주어진 배열이나 컬렉션에 없는 키와 그에 해당하는 값을 모두 제거합니다.

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

`isEmpty` 메서드는 컬렉션이 비어 있으면 `true`를, 비어 있지 않으면 `false`를 반환합니다.

```php
collect([])->isEmpty();

// true
```

<a name="method-isnotempty"></a>
#### `isNotEmpty()`

`isNotEmpty` 메서드는 컬렉션이 비어 있지 않으면 `true`를, 그렇지 않으면 `false`를 반환합니다.

```php
collect([])->isNotEmpty();

// false
```

<a name="method-join"></a>
#### `join()`

`join` 메서드는 컬렉션의 값을 문자열로 결합합니다. 두 번째 인자를 사용하면, 마지막 원소가 문자열에 추가되는 방식을 지정할 수 있습니다.

```php
collect(['a', 'b', 'c'])->join(', '); // 'a, b, c'
collect(['a', 'b', 'c'])->join(', ', ', and '); // 'a, b, and c'
collect(['a', 'b'])->join(', ', ' and '); // 'a and b'
collect(['a'])->join(', ', ' and '); // 'a'
collect([])->join(', ', ' and '); // ''
```

<a name="method-keyby"></a>
#### `keyBy()`

`keyBy` 메서드는 컬렉션의 인덱스를 지정한 키로 재구성합니다. 중복된 키가 있으면 마지막 항목만 새 컬렉션에 남게 됩니다.

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

이 메서드에는 콜백을 전달할 수도 있습니다. 콜백의 반환 값이 컬렉션의 인덱스로 사용됩니다.

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

`last` 메서드는 주어진 조건(트루시 테스트)을 만족하는 컬렉션의 마지막 요소를 반환합니다.

```php
collect([1, 2, 3, 4])->last(function (int $value, int $key) {
    return $value < 3;
});

// 2
```

인자를 전달하지 않으면 컬렉션의 마지막 요소를 반환하며, 컬렉션이 비어 있다면 `null`을 반환합니다.

```php
collect([1, 2, 3, 4])->last();

// 4
```

<a name="method-lazy"></a>
#### `lazy()`

`lazy` 메서드는 컬렉션의 항목을 기반으로 새로운 [LazyCollection](#lazy-collections) 인스턴스를 반환합니다.

```php
$lazyCollection = collect([1, 2, 3, 4])->lazy();

$lazyCollection::class;

// Illuminate\Support\LazyCollection

$lazyCollection->all();

// [1, 2, 3, 4]
```

이 기능은 특히 많은 항목을 가진 거대한 `Collection`에서 변환 작업이 필요할 때 유용합니다.

```php
$count = $hugeCollection
    ->lazy()
    ->where('country', 'FR')
    ->where('balance', '>', '100')
    ->count();
```

컬렉션을 `LazyCollection`으로 변환하면, 추가적인 메모리 할당 없이 필터 작업을 할 수 있습니다. 원본 컬렉션은 여전히 값들을 메모리에 가지고 있지만, 이후의 필터링 단계에서는 별도의 추가 메모리가 사실상 소모되지 않습니다.

<a name="method-macro"></a>
#### `macro()`

정적 메서드인 `macro`를 사용하면 런타임에 `Collection` 클래스에 메서드를 동적으로 추가할 수 있습니다. 자세한 내용은 [컬렉션 확장하기](#extending-collections) 문서를 참고하세요.

<a name="method-make"></a>
#### `make()`

정적 메서드인 `make`는 새로운 컬렉션 인스턴스를 생성합니다. 자세한 내용은 [컬렉션 생성하기](#creating-collections) 섹션을 참고하세요.

```php
use Illuminate\Support\Collection;

$collection = Collection::make([1, 2, 3]);
```

<a name="method-map"></a>
#### `map()`

`map` 메서드는 컬렉션을 순회하며 각 값을 주어진 콜백에 전달합니다. 콜백에서 항목을 수정해서 반환하면, 이 수정된 항목들로 새로운 컬렉션이 만들어집니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$multiplied = $collection->map(function (int $item, int $key) {
    return $item * 2;
});

$multiplied->all();

// [2, 4, 6, 8, 10]
```

> [!WARNING]
> 대부분의 컬렉션 메서드처럼, `map`은 원본 컬렉션을 수정하지 않고 새로운 컬렉션 인스턴스를 반환합니다. 원본 컬렉션 자체를 변환하고 싶다면, [transform](#method-transform) 메서드를 사용하세요.

<a name="method-mapinto"></a>
#### `mapInto()`

`mapInto()` 메서드는 컬렉션을 순회하면서, 각 항목을 지정한 클래스의 인스턴스로 만들어줍니다. 값은 해당 클래스의 생성자로 전달됩니다.

```php
class Currency
{
    /**
     * 새로운 Currency 인스턴스 생성
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

`mapSpread` 메서드는 컬렉션의 각 아이템(특히 중첩된 아이템들)을 반복하면서, 각 중첩 아이템의 값을 지정한 클로저로 전달합니다. 클로저 안에서 아이템을 자유롭게 수정하여 반환할 수 있으며, 이로 인해 수정된 아이템들로 이루어진 새로운 컬렉션을 만들 수 있습니다.

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

`mapToGroups` 메서드는 컬렉션의 아이템들을 지정한 클로저에 따라 그룹으로 묶어줍니다. 이 클로저는 반드시 하나의 키/값 쌍을 가진 연관 배열을 반환해야 하며, 이로써 그룹화된 값들로 새로운 컬렉션이 생성됩니다.

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

`mapWithKeys` 메서드는 컬렉션의 각 아이템을 반복하며 지정한 콜백에 전달합니다. 이 콜백은 반드시 하나의 키/값 쌍을 포함한 연관 배열을 반환해야 합니다.

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

`max` 메서드는 지정한 키에 대한 최대값을 반환합니다.

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

`median` 메서드는 지정한 키의 [중앙값(중위값)](https://en.wikipedia.org/wiki/Median)을 반환합니다.

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

`merge` 메서드는 주어진 배열이나 컬렉션을 기존 컬렉션과 합칩니다. 만약 주어진 아이템에 문자열 키가 있고, 기존 컬렉션에도 동일한 키가 있다면, 새로운 값이 기존 값을 덮어씁니다.

```php
$collection = collect(['product_id' => 1, 'price' => 100]);

$merged = $collection->merge(['price' => 200, 'discount' => false]);

$merged->all();

// ['product_id' => 1, 'price' => 200, 'discount' => false]
```

주어진 아이템에서 키가 숫자일 경우, 해당 값들은 컬렉션의 끝에 추가됩니다.

```php
$collection = collect(['Desk', 'Chair']);

$merged = $collection->merge(['Bookcase', 'Door']);

$merged->all();

// ['Desk', 'Chair', 'Bookcase', 'Door']
```

<a name="method-mergerecursive"></a>
#### `mergeRecursive()`

`mergeRecursive` 메서드는 주어진 배열이나 컬렉션을 기존 컬렉션과 재귀적으로 합칩니다. 만약 주어진 아이템에 문자열 키가 있고, 기존 컬렉션에도 동일한 키가 있다면, 해당 키에 대한 값들이 배열로 합쳐진 뒤, 이 동작이 재귀적으로 반복됩니다.

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

`min` 메서드는 지정한 키에 대한 최소값을 반환합니다.

```php
$min = collect([['foo' => 10], ['foo' => 20]])->min('foo');

// 10

$min = collect([1, 2, 3, 4, 5])->min();

// 1
```

<a name="method-mode"></a>
#### `mode()`

`mode` 메서드는 지정한 키의 [최빈값(모드)](https://en.wikipedia.org/wiki/Mode_(statistics))을 반환합니다.

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

`multiply` 메서드는 컬렉션에 속한 모든 아이템을 지정한 숫자만큼 복제하여 새로운 컬렉션을 만듭니다.

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

`nth` 메서드는 주어진 간격마다 한 번씩 요소를 뽑아 새로운 컬렉션을 만듭니다.

```php
$collection = collect(['a', 'b', 'c', 'd', 'e', 'f']);

$collection->nth(4);

// ['a', 'e']
```

두 번째 인수로 시작 위치(오프셋)를 전달할 수도 있습니다.

```php
$collection->nth(4, 1);

// ['b', 'f']
```

<a name="method-only"></a>
#### `only()`

`only` 메서드는 지정한 키에 해당하는 아이템만을 반환합니다.

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

반대 동작을 원한다면 [except](#method-except) 메서드를 참고하세요.

> [!NOTE]
> 이 메서드는 [Eloquent 컬렉션](/docs/12.x/eloquent-collections#method-only)을 사용할 때 동작 방식이 다릅니다.

<a name="method-pad"></a>
#### `pad()`

`pad` 메서드는 주어진 값으로 컬렉션을 채워, 컬렉션이 지정한 크기만큼 될 때까지 확장합니다. 이 메서드는 PHP의 [array_pad](https://secure.php.net/manual/en/function.array-pad.php) 함수와 유사하게 동작합니다.

컬렉션의 왼쪽(앞쪽)에 값을 채우려면, 크기를 음수로 지정해야 합니다. 만약 지정한 크기의 절대값이 현재 컬렉션의 길이보다 작거나 같다면 아무런 패딩이 적용되지 않습니다.

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

`partition` 메서드는 PHP의 배열 구조 분해 할당과 조합하여, 지정한 조건에 부합하는 요소와 부합하지 않는 요소를 각각 분리할 수 있도록 해줍니다.

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
> 이 메서드는 [Eloquent 컬렉션](/docs/12.x/eloquent-collections#method-partition)과 함께 사용할 때 동작 방식이 다릅니다.

<a name="method-percentage"></a>
#### `percentage()`

`percentage` 메서드는 컬렉션에서 지정한 조건을 만족하는 아이템의 백분율을 손쉽게 구할 수 있습니다.

```php
$collection = collect([1, 1, 2, 2, 2, 3]);

$percentage = $collection->percentage(fn (int $value) => $value === 1);

// 33.33
```

기본적으로 이 메서드는 소수점 둘째 자리까지 반올림하여 결과를 반환합니다. 하지만 두 번째 인수로 소수점 자릿수를 지정해 정밀도를 조절할 수 있습니다.

```php
$percentage = $collection->percentage(fn (int $value) => $value === 1, precision: 3);

// 33.333
```

<a name="method-pipe"></a>
#### `pipe()`

`pipe` 메서드는 컬렉션 자체를 지정된 클로저에 전달하고, 이 클로저의 실행 결과를 반환합니다.

```php
$collection = collect([1, 2, 3]);

$piped = $collection->pipe(function (Collection $collection) {
    return $collection->sum();
});

// 6
```

<a name="method-pipeinto"></a>
#### `pipeInto()`

`pipeInto` 메서드는 지정한 클래스의 새 인스턴스를 만들고, 컬렉션을 이 클래스의 생성자에 전달합니다.

```php
class ResourceCollection
{
    /**
     * 새로운 ResourceCollection 인스턴스를 생성합니다.
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

`pipeThrough` 메서드는 컬렉션을 다수의 클로저 배열에 순차적으로 전달하며, 그 실행 결과를 반환합니다.

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

`pluck` 메서드는 지정한 키에 해당하는 모든 값을 추출하여 반환합니다.

```php
$collection = collect([
    ['product_id' => 'prod-100', 'name' => 'Desk'],
    ['product_id' => 'prod-200', 'name' => 'Chair'],
]);

$plucked = $collection->pluck('name');

$plucked->all();

// ['Desk', 'Chair']
```

추출된 값의 결과 컬렉션의 키를 지정하고 싶을 때는 두 번째 인수로 지정할 수 있습니다.

```php
$plucked = $collection->pluck('name', 'product_id');

$plucked->all();

// ['prod-100' => 'Desk', 'prod-200' => 'Chair']
```

`pluck` 메서드는 "점 표기법(dot notation)"을 이용하여 중첩된 값도 추출할 수 있습니다.

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

중복된 키가 있는 경우, pluck 결과 컬렉션에는 마지막에 매칭된 요소가 저장됩니다.

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

`pop` 메서드는 컬렉션의 마지막 아이템을 제거하고 그 값을 반환합니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->pop();

// 5

$collection->all();

// [1, 2, 3, 4]
```

`pop` 메서드에 정수를 전달하면, 컬렉션의 마지막 n개의 아이템을 제거하여 반환할 수 있습니다.

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

또한 두 번째 인수로 추가할 아이템의 키를 지정할 수도 있습니다.

```php
$collection = collect(['one' => 1, 'two' => 2]);

$collection->prepend(0, 'zero');

$collection->all();

// ['zero' => 0, 'one' => 1, 'two' => 2]
```

<a name="method-pull"></a>
#### `pull()`

`pull` 메서드는 지정한 키에 해당하는 아이템을 컬렉션에서 제거하고, 그 값을 반환합니다.

```php
$collection = collect(['product_id' => 'prod-100', 'name' => 'Desk']);

$collection->pull('name');

// 'Desk'

$collection->all();

// ['product_id' => 'prod-100']
```

<a name="method-push"></a>
#### `push()`

`push` 메서드는 컬렉션의 마지막에 아이템을 추가합니다.

```php
$collection = collect([1, 2, 3, 4]);

$collection->push(5);

$collection->all();

// [1, 2, 3, 4, 5]
```

<a name="method-put"></a>

#### `put()`

`put` 메서드는 지정된 키와 값을 컬렉션에 설정합니다.

```php
$collection = collect(['product_id' => 1, 'name' => 'Desk']);

$collection->put('price', 100);

$collection->all();

// ['product_id' => 1, 'name' => 'Desk', 'price' => 100]
```

<a name="method-random"></a>
#### `random()`

`random` 메서드는 컬렉션에서 무작위로 하나의 항목을 반환합니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->random();

// 4 - (무작위로 선택됨)
```

`random` 메서드에 정수를 전달하면, 지정한 개수만큼의 항목을 무작위로 추출할 수 있습니다. 요청한 개수를 명시적으로 전달하면, 항상 컬렉션 형태로 반환합니다.

```php
$random = $collection->random(3);

$random->all();

// [2, 4, 5] - (무작위로 선택됨)
```

컬렉션 안에 요청한 개수보다 항목이 적다면, `random` 메서드는 `InvalidArgumentException`을 발생시킵니다.

또한, `random` 메서드는 현재 컬렉션 인스턴스를 전달받는 클로저도 인자로 받을 수 있습니다.

```php
use Illuminate\Support\Collection;

$random = $collection->random(fn (Collection $items) => min(10, count($items)));

$random->all();

// [1, 2, 3, 4, 5] - (무작위로 선택됨)
```

<a name="method-range"></a>
#### `range()`

`range` 메서드는 지정한 범위의 정수로 구성된 컬렉션을 반환합니다.

```php
$collection = collect()->range(3, 6);

$collection->all();

// [3, 4, 5, 6]
```

<a name="method-reduce"></a>
#### `reduce()`

`reduce` 메서드는 컬렉션을 단일 값으로 축소합니다. 각 반복에서 반환된 결과가 다음 반복으로 전달됩니다.

```php
$collection = collect([1, 2, 3]);

$total = $collection->reduce(function (?int $carry, int $item) {
    return $carry + $item;
});

// 6
```

첫 번째 반복에서 `$carry` 값은 `null`입니다. 그러나 `reduce`의 두 번째 인자로 초기값을 지정할 수 있습니다.

```php
$collection->reduce(function (int $carry, int $item) {
    return $carry + $item;
}, 4);

// 10
```

`reduce` 메서드는 제공된 콜백으로 배열의 키도 전달합니다.

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

`reduceSpread` 메서드는 컬렉션을 여러 값의 배열로 축소합니다. 각 반복의 결과들이 다음 반복에 전달됩니다. 이 메서드는 `reduce`와 비슷하지만, 여러 개의 초기값을 받을 수 있습니다.

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

`reject` 메서드는 제공된 클로저를 통해 컬렉션을 필터링합니다. 클로저가 `true`를 반환하면 그 항목은 결과 컬렉션에서 제거됩니다.

```php
$collection = collect([1, 2, 3, 4]);

$filtered = $collection->reject(function (int $value, int $key) {
    return $value > 2;
});

$filtered->all();

// [1, 2]
```

`reject`와 반대 역할을 하는 메서드는 [filter](#method-filter) 메서드입니다.

<a name="method-replace"></a>
#### `replace()`

`replace` 메서드는 `merge`와 비슷하게 동작합니다. 하지만 문자열 키가 일치하는 항목뿐 아니라, 숫자 키가 일치하는 항목도 덮어씁니다.

```php
$collection = collect(['Taylor', 'Abigail', 'James']);

$replaced = $collection->replace([1 => 'Victoria', 3 => 'Finn']);

$replaced->all();

// ['Taylor', 'Victoria', 'James', 'Finn']
```

<a name="method-replacerecursive"></a>
#### `replaceRecursive()`

이 메서드는 `replace`와 유사하나, 배열의 내부까지 재귀적으로 탐색해 동일한 방식으로 값을 대체합니다.

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

`reverse` 메서드는 컬렉션 내 항목의 순서를 뒤집으며, 기존 키를 유지합니다.

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

`search` 메서드는 컬렉션에서 주어진 값을 찾아 해당 키를 반환합니다. 해당 항목을 찾지 못하면 `false`가 반환됩니다.

```php
$collection = collect([2, 4, 6, 8]);

$collection->search(4);

// 1
```

검색은 "느슨한(loose)" 비교로 이루어지므로, 문자열로 된 숫자도 같은 숫자 값으로 간주됩니다. "엄격한(strict)" 비교를 원한다면 두 번째 인수로 `true`를 전달하세요.

```php
collect([2, 4, 6, 8])->search('4', strict: true);

// false
```

또한, 특정 조건을 만족하는 첫 번째 항목을 탐색하고 싶다면 직접 클로저를 전달할 수도 있습니다.

```php
collect([2, 4, 6, 8])->search(function (int $item, int $key) {
    return $item > 5;
});

// 2
```

<a name="method-select"></a>
#### `select()`

`select` 메서드는 지정한 키만을 선택하여 새로운 컬렉션을 만듭니다. 마치 SQL의 `SELECT` 문의 역할과 비슷합니다.

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

`shift` 메서드는 컬렉션의 첫 번째 항목을 제거하고 반환합니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->shift();

// 1

$collection->all();

// [2, 3, 4, 5]
```

정수를 `shift` 메서드에 전달하면, 컬렉션 앞부분에서 여러 개의 항목을 제거하여 반환할 수도 있습니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->shift(3);

// collect([1, 2, 3])

$collection->all();

// [4, 5]
```

<a name="method-shuffle"></a>
#### `shuffle()`

`shuffle` 메서드는 컬렉션의 항목들을 무작위로 섞어줍니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$shuffled = $collection->shuffle();

$shuffled->all();

// [3, 2, 5, 1, 4] - (무작위로 생성됨)
```

<a name="method-skip"></a>
#### `skip()`

`skip` 메서드는 지정한 개수만큼 앞에서 항목을 제거한 새로운 컬렉션을 반환합니다.

```php
$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);

$collection = $collection->skip(4);

$collection->all();

// [5, 6, 7, 8, 9, 10]
```

<a name="method-skipuntil"></a>
#### `skipUntil()`

`skipUntil` 메서드는 주어진 콜백이 `false`를 반환하는 동안 컬렉션의 항목을 건너뜁니다. 콜백이 `true`를 반환하면, 이후 남은 모든 항목이 새 컬렉션에 포함되어 반환됩니다.

```php
$collection = collect([1, 2, 3, 4]);

$subset = $collection->skipUntil(function (int $item) {
    return $item >= 3;
});

$subset->all();

// [3, 4]
```

`skipUntil` 메서드에 단순 값을 전달하면 해당 값이 나올 때까지 모든 항목을 건너뜁니다.

```php
$collection = collect([1, 2, 3, 4]);

$subset = $collection->skipUntil(3);

$subset->all();

// [3, 4]
```

> [!WARNING]
> 전달한 값이 컬렉션 내에 없거나, 콜백이 한 번도 `true`를 반환하지 않으면 `skipUntil` 메서드는 빈 컬렉션을 반환합니다.

<a name="method-skipwhile"></a>
#### `skipWhile()`

`skipWhile` 메서드는 주어진 콜백이 `true`를 반환하는 동안 컬렉션 항목을 건너뜁니다. 콜백이 `false`를 반환하면, 그 이후의 모든 항목이 새로운 컬렉션으로 반환됩니다.

```php
$collection = collect([1, 2, 3, 4]);

$subset = $collection->skipWhile(function (int $item) {
    return $item <= 3;
});

$subset->all();

// [4]
```

> [!WARNING]
> 콜백이 한 번도 `false`를 반환하지 않으면 `skipWhile` 메서드는 빈 컬렉션을 반환합니다.

<a name="method-slice"></a>
#### `slice()`

`slice` 메서드는 지정한 인덱스부터 컬렉션의 일부 구간을 잘라서 반환합니다.

```php
$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);

$slice = $collection->slice(4);

$slice->all();

// [5, 6, 7, 8, 9, 10]
```

반환되는 조각의 크기를 제한하고 싶다면 두 번째 인자로 원하는 크기를 전달하세요.

```php
$slice = $collection->slice(4, 2);

$slice->all();

// [5, 6]
```

반환된 슬라이스는 기본적으로 키를 보존합니다. 만약 원래의 키를 유지하고 싶지 않다면, [values](#method-values) 메서드를 사용해서 인덱스를 재정렬할 수 있습니다.

<a name="method-sliding"></a>
#### `sliding()`

`sliding` 메서드는 컬렉션 항목들의 "슬라이딩 윈도우" 형태의 청크(조각) 컬렉션을 반환합니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$chunks = $collection->sliding(2);

$chunks->toArray();

// [[1, 2], [2, 3], [3, 4], [4, 5]]
```

이 기능은 [eachSpread](#method-eachspread) 메서드와 함께 사용하면 특히 유용합니다.

```php
$transactions->sliding(2)->eachSpread(function (Collection $previous, Collection $current) {
    $current->total = $previous->total + $current->amount;
});
```

옵션으로 두 번째 인자로 "step" 값을 전달하면, 각 청크의 첫 번째 항목 간 간격을 조정할 수 있습니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$chunks = $collection->sliding(3, step: 2);

$chunks->toArray();

// [[1, 2, 3], [3, 4, 5]]
```

<a name="method-sole"></a>
#### `sole()`

`sole` 메서드는 주어진 조건을 통과하는 항목이 정확히 하나일 때, 그 첫 번째 항목을 반환합니다.

```php
collect([1, 2, 3, 4])->sole(function (int $value, int $key) {
    return $value === 2;
});

// 2
```

또는, `sole` 메서드에 키/값 쌍을 전달해서 조건에 일치하는 항목이 정확히 하나일 때 반환할 수도 있습니다.

```php
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
]);

$collection->sole('product', 'Chair');

// ['product' => 'Chair', 'price' => 100]
```

아무런 인자를 전달하지 않으면, 컬렉션에 오직 하나의 요소만 있는 경우 해당 요소를 반환합니다.

```php
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
]);

$collection->sole();

// ['product' => 'Desk', 'price' => 200]
```

`sole` 메서드가 반환할 항목이 없으면 `\Illuminate\Collections\ItemNotFoundException` 예외가 발생합니다. 일치하는 항목이 둘 이상이면 `\Illuminate\Collections\MultipleItemsFoundException` 예외가 발생합니다.

<a name="method-some"></a>
#### `some()`

[contain](#method-contains) 메서드의 별칭입니다.

<a name="method-sort"></a>
#### `sort()`

`sort` 메서드는 컬렉션을 정렬합니다. 정렬된 컬렉션은 원래의 배열 키를 유지하므로, 아래 예제와 같이 [values](#method-values) 메서드를 사용하여 키를 재정렬할 수 있습니다.

```php
$collection = collect([5, 3, 1, 2, 4]);

$sorted = $collection->sort();

$sorted->values()->all();

// [1, 2, 3, 4, 5]
```

정렬이 더 복잡하게 필요할 경우, `sort`에 직접 콜백을 전달할 수 있습니다. 이 메서드는 내부적으로 PHP의 [uasort](https://secure.php.net/manual/en/function.uasort.php#refsect1-function.uasort-parameters) 함수를 활용합니다.

> [!NOTE]
> 중첩 배열 혹은 객체 컬렉션을 정렬하려면 [sortBy](#method-sortby) 또는 [sortByDesc](#method-sortbydesc) 메서드를 사용하세요.

<a name="method-sortby"></a>
#### `sortBy()`

`sortBy` 메서드는 지정된 키를 기준으로 컬렉션을 정렬합니다. 정렬된 컬렉션은 원래의 배열 키를 그대로 유지하므로, 예제와 같이 [values](#method-values) 메서드로 키를 정수형 인덱스로 재정렬할 수 있습니다.

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

`sortBy` 메서드는 두 번째 인수로 [정렬 플래그(sort flags)](https://www.php.net/manual/en/function.sort.php)를 전달받을 수 있습니다.

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

혹은 직접 원하는 방법으로 정렬을 수행하려면 클로저를 전달해도 됩니다.

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

컬렉션을 여러 속성으로 정렬하고 싶을 땐, `sortBy`에 여러 정렬 조건의 배열을 전달할 수 있습니다. 각 정렬 조건은 정렬할 속성과 방향이 들어있는 배열입니다.

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

여러 개의 속성으로 정렬할 때, 각 정렬 조건을 정의하는 클로저를 전달할 수도 있습니다.

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

이 메서드는 [sortBy](#method-sortby) 메서드와 동일한 시그니처를 가지지만, 컬렉션을 반대 순서로 정렬합니다.

<a name="method-sortdesc"></a>
#### `sortDesc()`

이 메서드는 [sort](#method-sort) 메서드와 반대 순서로 컬렉션을 정렬합니다.

```php
$collection = collect([5, 3, 1, 2, 4]);

$sorted = $collection->sortDesc();

$sorted->values()->all();

// [5, 4, 3, 2, 1]
```

`sort`와는 달리 `sortDesc`에는 클로저를 전달할 수 없습니다. 대신 [sort](#method-sort) 메서드를 사용한 후 비교 로직을 반대로 구현해야 합니다.

<a name="method-sortkeys"></a>
#### `sortKeys()`

`sortKeys` 메서드는 컬렉션의 내부 연관 배열의 키를 기준으로 정렬합니다.

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

이 메서드는 [sortKeys](#method-sortkeys) 메서드와 동일한 시그니처를 가지지만, 키를 반대 순서로 정렬합니다.

<a name="method-sortkeysusing"></a>
#### `sortKeysUsing()`

`sortKeysUsing` 메서드는 콜백을 사용해 컬렉션의 내부 연관 배열의 키를 기준으로 정렬합니다.

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

콜백은 0보다 작거나, 0과 같거나, 0보다 큰 정수를 반환하는 비교 함수여야 합니다. 자세한 내용은 PHP가 내부적으로 `sortKeysUsing`에서 사용하는 [uksort](https://www.php.net/manual/en/function.uksort.php#refsect1-function.uksort-parameters)의 PHP 공식 문서를 참고하세요.

<a name="method-splice"></a>
#### `splice()`

`splice` 메서드는 지정한 인덱스부터 시작하는 컬렉션의 항목들을 잘라내어 반환합니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$chunk = $collection->splice(2);

$chunk->all();

// [3, 4, 5]

$collection->all();

// [1, 2]
```

두 번째 인수를 전달하면 반환되는 컬렉션의 크기를 제한할 수 있습니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$chunk = $collection->splice(2, 1);

$chunk->all();

// [3]

$collection->all();

// [1, 2, 4, 5]
```

또한 세 번째 인수로 삭제된 항목 대신 새 항목을 전달할 수 있습니다.

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

`split` 메서드는 컬렉션을 지정한 그룹 개수만큼 나눕니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$groups = $collection->split(3);

$groups->all();

// [[1, 2], [3, 4], [5]]
```

<a name="method-splitin"></a>
#### `splitIn()`

`splitIn` 메서드는 컬렉션을 지정한 그룹 개수만큼 나누되, 마지막 그룹을 할당하기 전에 나머지 그룹을 최대한 가득 채웁니다.

```php
$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);

$groups = $collection->splitIn(3);

$groups->all();

// [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10]]
```

<a name="method-sum"></a>
#### `sum()`

`sum` 메서드는 컬렉션 내 모든 항목의 합계를 반환합니다.

```php
collect([1, 2, 3, 4, 5])->sum();

// 15
```

컬렉션에 중첩 배열이나 객체가 포함된 경우, 어떤 값을 합산할지 결정할 수 있도록 키를 전달할 수 있습니다.

```php
$collection = collect([
    ['name' => 'JavaScript: The Good Parts', 'pages' => 176],
    ['name' => 'JavaScript: The Definitive Guide', 'pages' => 1096],
]);

$collection->sum('pages');

// 1272
```

또한, 어떤 값을 합산할지 직접 정의하고 싶다면 클로저를 전달할 수 있습니다.

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

`take` 메서드는 지정한 개수만큼의 항목을 가진 새로운 컬렉션을 반환합니다.

```php
$collection = collect([0, 1, 2, 3, 4, 5]);

$chunk = $collection->take(3);

$chunk->all();

// [0, 1, 2]
```

음수 값을 전달하면 컬렉션의 끝에서부터 지정한 개수만큼의 항목을 가져옵니다.

```php
$collection = collect([0, 1, 2, 3, 4, 5]);

$chunk = $collection->take(-2);

$chunk->all();

// [4, 5]
```

<a name="method-takeuntil"></a>
#### `takeUntil()`

`takeUntil` 메서드는 지정한 콜백이 `true`를 반환할 때까지 컬렉션의 항목을 반환합니다.

```php
$collection = collect([1, 2, 3, 4]);

$subset = $collection->takeUntil(function (int $item) {
    return $item >= 3;
});

$subset->all();

// [1, 2]
```

또한 특정 값을 전달해서 해당 값이 나올 때까지의 항목을 가져올 수도 있습니다.

```php
$collection = collect([1, 2, 3, 4]);

$subset = $collection->takeUntil(3);

$subset->all();

// [1, 2]
```

> [!WARNING]
> 전달한 값이 컬렉션에서 발견되지 않거나, 콜백이 한 번도 `true`를 반환하지 않으면, `takeUntil` 메서드는 컬렉션의 모든 항목을 반환합니다.

<a name="method-takewhile"></a>
#### `takeWhile()`

`takeWhile` 메서드는 지정한 콜백이 `false`를 반환할 때까지 컬렉션의 항목을 반환합니다.

```php
$collection = collect([1, 2, 3, 4]);

$subset = $collection->takeWhile(function (int $item) {
    return $item < 3;
});

$subset->all();

// [1, 2]
```

> [!WARNING]
> 콜백이 한 번도 `false`를 반환하지 않으면, `takeWhile` 메서드는 컬렉션의 모든 항목을 반환합니다.

<a name="method-tap"></a>
#### `tap()`

`tap` 메서드는 전달한 콜백에 컬렉션 자체를 전달하여, 컬렉션의 특정 시점에서 항목을 참조하거나 무언가 작업을 할 수 있게 해줍니다. 단, 컬렉션 자체에는 영향을 주지 않으며, `tap` 메서드는 컬렉션 객체를 그대로 반환합니다.

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

정적 메서드인 `times`는 지정한 횟수만큼 클로저를 실행하여, 그 결과를 새로운 컬렉션으로 만듭니다.

```php
$collection = Collection::times(10, function (int $number) {
    return $number * 9;
});

$collection->all();

// [9, 18, 27, 36, 45, 54, 63, 72, 81, 90]
```

<a name="method-toarray"></a>
#### `toArray()`

`toArray` 메서드는 컬렉션을 일반 PHP `array`로 변환합니다. 만약 컬렉션의 값이 [Eloquent](/docs/12.x/eloquent) 모델이라면, 모델들도 배열로 변환됩니다.

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
> `toArray`는 컬렉션 내에 `Arrayable` 인스턴스인 중첩 객체도 모두 배열로 변환합니다. 컬렉션의 원본 배열만 가져오고 싶다면 [all](#method-all) 메서드를 사용하세요.

<a name="method-tojson"></a>
#### `toJson()`

`toJson` 메서드는 컬렉션을 JSON으로 직렬화된 문자열로 변환합니다.

```php
$collection = collect(['name' => 'Desk', 'price' => 200]);

$collection->toJson();

// '{"name":"Desk", "price":200}'
```

<a name="method-transform"></a>
#### `transform()`

`transform` 메서드는 컬렉션의 각 항목에 대해 전달된 콜백을 실행하고, 그 반환값으로 컬렉션의 항목을 교체합니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->transform(function (int $item, int $key) {
    return $item * 2;
});

$collection->all();

// [2, 4, 6, 8, 10]
```

> [!WARNING]
> 대부분의 컬렉션 메서드와 달리, `transform`은 컬렉션 자체를 직접 수정합니다. 새로운 컬렉션을 생성하고 싶다면 [map](#method-map) 메서드를 사용하세요.

<a name="method-undot"></a>
#### `undot()`

`undot` 메서드는 "dot" 표기법을 사용하는 단일 차원의 컬렉션을 다차원 컬렉션으로 확장합니다.

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

`union` 메서드는 전달받은 배열을 컬렉션에 합칩니다. 만약 전달된 배열에 이미 존재하는 키가 있을 경우, 기존 컬렉션의 값이 우선시됩니다.

```php
$collection = collect([1 => ['a'], 2 => ['b']]);

$union = $collection->union([3 => ['c'], 1 => ['d']]);

$union->all();

// [1 => ['a'], 2 => ['b'], 3 => ['c']]
```

<a name="method-unique"></a>
#### `unique()`

`unique` 메서드는 컬렉션에서 중복되지 않는 항목만 반환합니다. 반환된 컬렉션은 원래 배열의 키를 유지하기 때문에, 아래 예시에서는 [values](#method-values) 메서드로 키를 연속된 숫자 인덱스로 재설정해 사용합니다.

```php
$collection = collect([1, 1, 2, 2, 3, 4, 2]);

$unique = $collection->unique();

$unique->values()->all();

// [1, 2, 3, 4]
```

중첩 배열이나 객체가 포함되어 있는 경우, 어떤 키를 기준으로 중복을 판단할지 지정할 수 있습니다.

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

마지막으로, 어느 값을 기준으로 중복 여부를 판단할지 클로저로 직접 지정할 수도 있습니다.

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

`unique` 메서드는 항목의 값을 비교할 때 "느슨한(loose) 비교"를 사용하므로, 문자열 형태의 숫자 값과 정수 값은 동일한 값으로 간주합니다. "엄격한 비교"를 통한 필터링이 필요하다면 [uniqueStrict](#method-uniquestrict) 메서드를 사용하세요.

> [!NOTE]
> 이 메서드는 [Eloquent 컬렉션](/docs/12.x/eloquent-collections#method-unique)을 사용할 때 동작이 달라집니다.

<a name="method-uniquestrict"></a>
#### `uniqueStrict()`

이 메서드는 [unique](#method-unique) 메서드와 동일한 시그니처를 가지지만, 모든 값이 "엄격한 비교" 방식으로 비교됩니다.

<a name="method-unless"></a>
#### `unless()`

`unless` 메서드는 첫 번째 인자로 전달한 값이 `true`로 판별되지 않는 경우에만, 두 번째 인자(콜백)를 실행합니다. 이때 컬렉션 인스턴스와 첫 번째 인자가 콜백에 전달됩니다.

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

`unless` 메서드에는 두 번째 콜백을 추가로 전달할 수 있으며, 이 콜백은 첫 번째 인자가 `true`일 때 실행됩니다.

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

`unless`와 반대되는 동작을 원한다면 [when](#method-when) 메서드를 참고하세요.

<a name="method-unlessempty"></a>
#### `unlessEmpty()`

[whenNotEmpty](#method-whennotempty) 메서드의 별칭입니다.

<a name="method-unlessnotempty"></a>
#### `unlessNotEmpty()`

[whenEmpty](#method-whenempty) 메서드의 별칭입니다.

<a name="method-unwrap"></a>
#### `unwrap()`

정적 메서드 `unwrap`은 사용할 수 있는 경우 지정된 값에서 컬렉션의 원본 항목을 반환합니다.

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

`values` 메서드는 컬렉션의 키를 0부터 시작하는 연속된 정수로 리셋한 새로운 컬렉션을 반환합니다.

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

`when` 메서드는 첫 번째 인자로 전달된 값이 `true`로 평가될 때, 지정된 콜백을 실행합니다. 이때 컬렉션 인스턴스와 `when` 메서드에 전달된 첫 번째 인자가 클로저에 함께 전달됩니다.

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

`when` 메서드에는 두 번째 콜백을 넘길 수도 있습니다. 이 두 번째 콜백은 첫 번째 인자가 `false`로 평가될 때 실행됩니다.

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

`when`의 반대 동작을 원한다면 [unless](#method-unless) 메서드를 참고하세요.

<a name="method-whenempty"></a>
#### `whenEmpty()`

`whenEmpty` 메서드는 컬렉션이 비어 있을 때 지정된 콜백을 실행합니다.

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

`whenEmpty` 메서드에는 두 번째 클로저를 넘길 수도 있습니다. 이 클로저는 컬렉션이 비어 있지 않을 때 실행됩니다.

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

`whenEmpty`의 반대 동작을 원한다면 [whenNotEmpty](#method-whennotempty) 메서드를 참고하세요.

<a name="method-whennotempty"></a>
#### `whenNotEmpty()`

`whenNotEmpty` 메서드는 컬렉션이 비어 있지 않을 때 지정된 콜백을 실행합니다.

```php
$collection = collect(['michael', 'tom']);

$collection->whenNotEmpty(function (Collection $collection) {
    return $collection->push('adam');
});

$collection->all();

// ['michael', 'tom', 'adam']

$collection = collect();

$collection->whenNotEmpty(function (Collection $collection) {
    return $collection->push('adam');
});

$collection->all();

// []
```

`whenNotEmpty` 메서드에는 두 번째 클로저를 넘길 수도 있습니다. 이 클로저는 컬렉션이 비어 있을 때 실행됩니다.

```php
$collection = collect();

$collection->whenNotEmpty(function (Collection $collection) {
    return $collection->push('adam');
}, function (Collection $collection) {
    return $collection->push('taylor');
});

$collection->all();

// ['taylor']
```

`whenNotEmpty`의 반대 동작을 원한다면 [whenEmpty](#method-whenempty) 메서드를 참고하세요.

<a name="method-where"></a>
#### `where()`

`where` 메서드는 주어진 키/값 쌍에 따라 컬렉션을 필터링합니다.

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

`where` 메서드는 값 비교시 "느슨한(loose)" 비교를 사용합니다. 즉, 문자열로 된 정수 값도 같은 정수와 동등하게 간주합니다. "엄격한(strict)" 비교를 사용하려면 [whereStrict](#method-wherestrict) 메서드를 사용하세요.

옵션으로, 두 번째 파라미터에 비교 연산자를 지정할 수도 있습니다. 지원하는 연산자: '===', '!==', '!=', '==', '=', '<>', '>', '<', '>=', '<=' 입니다.

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

이 메서드는 [where](#method-where) 메서드와 같은 시그니처를 가지고 있지만, 모든 값 비교에서 "엄격한(strict)" 비교를 사용합니다.

<a name="method-wherebetween"></a>
#### `whereBetween()`

`whereBetween` 메서드는 지정된 값이 주어진 범위 내에 있는지 확인하여 컬렉션을 필터링합니다.

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

`whereIn` 메서드는 컬렉션에서 지정한 배열에 값이 포함되어 있지 않은 요소들을 제거합니다.

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

`whereIn` 메서드는 값 비교시 "느슨한(loose)" 비교를 사용합니다. 즉, 문자열로 된 정수 값도 같은 정수와 동등하게 간주합니다. "엄격한(strict)" 비교를 사용하려면 [whereInStrict](#method-whereinstrict) 메서드를 사용하세요.

<a name="method-whereinstrict"></a>
#### `whereInStrict()`

이 메서드는 [whereIn](#method-wherein) 메서드와 같은 시그니처를 가지고 있지만, 모든 값 비교에서 "엄격한(strict)" 비교를 사용합니다.

<a name="method-whereinstanceof"></a>
#### `whereInstanceOf()`

`whereInstanceOf` 메서드는 지정한 클래스 타입으로 컬렉션을 필터링합니다.

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

`whereNotBetween` 메서드는 지정한 값이 주어진 범위 밖에 있는지 확인하여 컬렉션을 필터링합니다.

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

`whereNotIn` 메서드는 컬렉션에서 지정한 배열에 값이 포함된 요소들을 제거합니다.

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

`whereNotIn` 메서드는 값 비교시 "느슨한(loose)" 비교를 사용합니다. 즉, 문자열로 된 정수 값도 같은 정수와 동등하게 간주합니다. "엄격한(strict)" 비교를 사용하려면 [whereNotInStrict](#method-wherenotinstrict) 메서드를 사용하세요.

<a name="method-wherenotinstrict"></a>
#### `whereNotInStrict()`

이 메서드는 [whereNotIn](#method-wherenotin) 메서드와 같은 시그니처를 가지고 있지만, 모든 값 비교에서 "엄격한(strict)" 비교를 사용합니다.

<a name="method-wherenotnull"></a>
#### `whereNotNull()`

`whereNotNull` 메서드는 지정한 키의 값이 `null`이 아닌 요소만 반환합니다.

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

`whereNull` 메서드는 지정한 키의 값이 `null`인 요소만 반환합니다.

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

정적 메서드인 `wrap`은 전달받은 값을 필요에 따라 컬렉션으로 감쌉니다.

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

`zip` 메서드는 지정한 배열의 값들과 원본 컬렉션의 값들을 동일 인덱스끼리 합쳐서 새로운 컬렉션을 만듭니다.

```php
$collection = collect(['Chair', 'Desk']);

$zipped = $collection->zip([100, 200]);

$zipped->all();

// [['Chair', 100], ['Desk', 200]]
```

<a name="higher-order-messages"></a>
## 하이어 오더 메시지 (Higher Order Messages)

컬렉션은 "하이어 오더 메시지(Higher Order Messages)"라는 편리한 단축 문법도 제공합니다. 이 기능을 이용하면 일반적으로 많이 사용하는 컬렉션 메서드를 더 간단하게 사용할 수 있습니다. 하이어 오더 메시지를 제공하는 컬렉션 메서드로는 다음과 같은 것들이 있습니다: [average](#method-average), [avg](#method-avg), [contains](#method-contains), [each](#method-each), [every](#method-every), [filter](#method-filter), [first](#method-first), [flatMap](#method-flatmap), [groupBy](#method-groupby), [keyBy](#method-keyby), [map](#method-map), [max](#method-max), [min](#method-min), [partition](#method-partition), [reject](#method-reject), [skipUntil](#method-skipuntil), [skipWhile](#method-skipwhile), [some](#method-some), [sortBy](#method-sortby), [sortByDesc](#method-sortbydesc), [sum](#method-sum), [takeUntil](#method-takeuntil), [takeWhile](#method-takewhile), [unique](#method-unique).

이 하이어 오더 메시지는 컬렉션 인스턴스의 동적 프로퍼티로 접근할 수 있습니다. 예를 들어, 컬렉션에 포함된 모든 객체에서 특정 메서드를 호출하려면 다음과 같이 사용할 수 있습니다.

```php
use App\Models\User;

$users = User::where('votes', '>', 500)->get();

$users->each->markAsVip();
```

마찬가지로, 컬렉션에 포함된 사용자들의 'votes' 합계를 구할 때 `sum` 하이어 오더 메시지를 쓸 수도 있습니다.

```php
$users = User::where('group', 'Development')->get();

return $users->sum->votes;
```

<a name="lazy-collections"></a>
## 레이지 컬렉션 (Lazy Collections)

<a name="lazy-collection-introduction"></a>
### 소개

> [!WARNING]
> 라라벨의 레이지 컬렉션(Lazy Collection)을 본격적으로 학습하기 전, [PHP 제너레이터](https://www.php.net/manual/en/language.generators.overview.php) 개념에 먼저 익숙해지시기를 권장합니다.

이미 강력한 기능을 제공하는 `Collection` 클래스와 더불어, `LazyCollection` 클래스는 PHP의 [제너레이터(generator)](https://www.php.net/manual/en/language.generators.overview.php) 기능을 활용하여, 매우 큰 데이터를 효과적으로 다루면서도 메모리 사용량을 적게 유지할 수 있도록 도와줍니다.

예를 들어, 여러분의 애플리케이션이 여러 GB(기가바이트)에 달하는 로그 파일을 처리해야 한다고 가정해보겠습니다. 이때 라라벨의 컬렉션 메서드를 활용해 로그를 파싱하고 싶을 수 있습니다. 전체 파일을 한 번에 메모리로 불러오는 대신, 레이지 컬렉션을 사용하면 파일의 일부만 메모리에 올려서 처리할 수 있습니다.

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

또 다른 예로, 만약 여러분이 10,000개의 Eloquent 모델을 반복 처리해야 한다고 합시다. 기존 라라벨 컬렉션을 사용한다면, 10,000개의 모든 Eloquent 모델을 한꺼번에 메모리에 적재해야 합니다.

```php
use App\Models\User;

$users = User::all()->filter(function (User $user) {
    return $user->id > 500;
});
```

하지만 쿼리 빌더의 `cursor` 메서드는 `LazyCollection` 인스턴스를 반환합니다. 이를 이용하면, 데이터베이스 쿼리는 한 번만 실행하지만, 매 순간 오직 하나의 Eloquent 모델만 메모리에 로드하여 처리할 수 있습니다. 이 예에서 `filter` 콜백은 actually 각 유저를 순회(iterate)할 때까지 실행되지 않으므로, 메모리 사용량이 크게 줄어듭니다.

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
### 레이지 컬렉션 인스턴스 생성

레이지 컬렉션 인스턴스를 생성하려면, 컬렉션의 `make` 메서드에 PHP 제너레이터 함수를 전달하면 됩니다.

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
### Enumerable 인터페이스(Contract)

`Collection` 클래스에서 사용할 수 있는 대부분의 메서드는 `LazyCollection` 클래스에서도 사용할 수 있습니다. 두 클래스 모두 `Illuminate\Support\Enumerable` 인터페이스(Contract)를 구현하며, 이 인터페이스는 다음과 같은 메서드들을 정의하고 있습니다.



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
> 컬렉션을 변형하는 메서드(예: `shift`, `pop`, `prepend` 등)는 `LazyCollection` 클래스에서 사용할 수 없습니다.

<a name="lazy-collection-methods"></a>

### 레이지(Lazy) 컬렉션 메서드

`Enumerable` 계약에 정의된 메서드 외에도, `LazyCollection` 클래스는 다음과 같은 메서드를 추가로 제공합니다.

<a name="method-takeUntilTimeout"></a>
#### `takeUntilTimeout()`

`takeUntilTimeout` 메서드는 지정한 시간까지 값을 순차적으로 나열(enumerate)하다가, 시간이 지나면 컬렉션의 나열을 종료하는 새로운 레이지 컬렉션을 반환합니다.

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

이 메서드의 사용 예시로, 데이터베이스에서 커서를 사용해 인보이스를 제출하는 애플리케이션을 생각해볼 수 있습니다. 예를 들어, 15분마다 실행되는 [스케줄링된 작업](/docs/12.x/scheduling)을 정의하고, 최대 14분까지만 인보이스를 처리하도록 할 수 있습니다.

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

`each` 메서드는 컬렉션의 각 항목에 대해 즉시 지정된 콜백을 실행합니다. 반면, `tapEach` 메서드는 리스트에서 항목이 하나씩 실제로 꺼내질 때마다 콜백을 실행합니다.

```php
// 아직 아무것도 dump되지 않습니다...
$lazyCollection = LazyCollection::times(INF)->tapEach(function (int $value) {
    dump($value);
});

// 3개의 항목이 dump됩니다...
$array = $lazyCollection->take(3)->all();

// 1
// 2
// 3
```

<a name="method-throttle"></a>
#### `throttle()`

`throttle` 메서드는 레이지 컬렉션이 각 값을 지정한 초 간격마다 반환하도록 동작을 제어(throttle)합니다. 외부 API에서 요청 빈도 제한(rate limit)이 있을 때 주로 유용하게 사용할 수 있습니다.

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

`remember` 메서드는 이미 나열된(enumerated) 값을 메모리에 저장하고, 이후 컬렉션을 다시 순회할 때는 새로 조회하지 않고 저장된 값을 재활용하는 새로운 레이지 컬렉션을 반환합니다.

```php
// 아직 쿼리가 실행되지 않았습니다...
$users = User::cursor()->remember();

// 쿼리가 실행됩니다...
// 첫 5명의 사용자가 데이터베이스에서 불러들여집니다...
$users->take(5)->all();

// 처음 5명의 사용자는 컬렉션의 캐시에서 가져오고...
// 나머지는 데이터베이스에서 새로 불러옵니다...
$users->take(20)->all();
```