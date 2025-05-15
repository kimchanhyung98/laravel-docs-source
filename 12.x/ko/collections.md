# 컬렉션 (Collections)

- [소개](#introduction)
    - [컬렉션 생성하기](#creating-collections)
    - [컬렉션 확장하기](#extending-collections)
- [사용 가능한 메서드](#available-methods)
- [고차 메시지](#higher-order-messages)
- [지연 컬렉션](#lazy-collections)
    - [소개](#lazy-collection-introduction)
    - [지연 컬렉션 생성하기](#creating-lazy-collections)
    - [Enumerable 계약](#the-enumerable-contract)
    - [지연 컬렉션 메서드](#lazy-collection-methods)

<a name="introduction"></a>
## 소개

`Illuminate\Support\Collection` 클래스는 데이터 배열을 더욱 편리하게 다룰 수 있도록 유연하고 간결한 래퍼를 제공합니다. 예를 들어, 아래 코드를 참고해보세요. `collect` 헬퍼를 사용해 배열로부터 새로운 컬렉션 인스턴스를 만들고, 각 요소에 `strtoupper` 함수를 적용한 뒤, 비어 있는 요소는 모두 제거합니다.

```php
$collection = collect(['taylor', 'abigail', null])->map(function (?string $name) {
    return strtoupper($name);
})->reject(function (string $name) {
    return empty($name);
});
```

보시는 것처럼, `Collection` 클래스는 다양한 메서드를 체이닝해서 배열 기반의 데이터에 유연하게 매핑이나 필터링 작업을 수행할 수 있습니다. 일반적으로 컬렉션은 불변(immutable) 객체로, 각 `Collection` 메서드는 항상 완전히 새로운 `Collection` 인스턴스를 반환합니다.

<a name="creating-collections"></a>
### 컬렉션 생성하기

앞서 설명한 대로, `collect` 헬퍼는 주어진 배열로부터 새로운 `Illuminate\Support\Collection` 인스턴스를 반환합니다. 따라서 컬렉션을 생성하는 방법은 매우 간단합니다.

```php
$collection = collect([1, 2, 3]);
```

또한 [make](#method-make) 메서드와 [fromJson](#method-fromjson) 메서드를 사용해서도 컬렉션을 생성할 수 있습니다.

> [!NOTE]
> [Eloquent](/docs/12.x/eloquent) 쿼리의 결과는 항상 `Collection` 인스턴스로 반환됩니다.

<a name="extending-collections"></a>
### 컬렉션 확장하기

컬렉션은 "매크로(macro)화"가 가능합니다. 즉, 실행 시점에 `Collection` 클래스에 새로운 메서드를 동적으로 추가할 수 있습니다. `Illuminate\Support\Collection` 클래스의 `macro` 메서드는 매크로로 등록할 클로저(익명 함수)를 받으며, 매크로가 호출될 때 실행됩니다. 이 매크로 안에서는 `$this`를 통해 컬렉션의 기존 기능을 활용할 수 있어, 실제 컬렉션 메서드처럼 작동합니다. 예를 들어, 아래 코드는 `Collection` 클래스에 `toUpper` 메서드를 추가하는 방식입니다.

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

일반적으로 컬렉션 매크로는 [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드 내에서 선언하는 것이 좋습니다.

<a name="macro-arguments"></a>
#### 매크로 인수

필요하다면, 매크로 정의 시 추가 인수를 받을 수도 있습니다.

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

이후 컬렉션 문서에서는 `Collection` 클래스에서 사용 가능한 각 메서드를 자세히 살펴보겠습니다. 이 모든 메서드는 체이닝이 가능해서, 컬렉션의 내부 배열을 더욱 유연하고 효율적으로 다룰 수 있습니다. 그리고 대부분의 메서드는 새로운 `Collection` 인스턴스를 반환하기 때문에, 컬렉션의 원본을 필요에 따라 안전하게 그대로 보존할 수 있습니다.



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

`after` 메서드는 지정한 값 바로 다음에 위치한 아이템을 반환합니다. 주어진 값이 컬렉션에 없거나 마지막 아이템인 경우에는 `null`을 반환합니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->after(3);

// 4

$collection->after(5);

// null
```

이 메서드는 "느슨한(loose)" 비교를 사용해서 검색하기 때문에, 정수값이 들어있는 문자열과 같은 값이라도 동일한 값으로 간주합니다. "엄격한(strict)" 비교를 사용하려면, `strict` 인수를 메서드에 전달하면 됩니다.

```php
collect([2, 4, 6, 8])->after('4', strict: true);

// null
```

또는, 주어진 조건을 만족하는 첫 번째 아이템을 찾기 위해 직접 클로저를 전달할 수도 있습니다.

```php
collect([2, 4, 6, 8])->after(function (int $item, int $key) {
    return $item > 5;
});

// 8
```

<a name="method-all"></a>
#### `all()`

`all` 메서드는 컬렉션이 표현하고 있는 내부 배열을 그대로 반환합니다.

```php
collect([1, 2, 3])->all();

// [1, 2, 3]
```

<a name="method-average"></a>
#### `average()`

[avg](#method-avg) 메서드의 다른 이름(alias)입니다.

<a name="method-avg"></a>
#### `avg()`

`avg` 메서드는 주어진 키의 [평균값](https://ko.wikipedia.org/wiki/%ED%8F%89%EA%B7%A0) 을 반환합니다.

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

`before` 메서드는 [after](#method-after) 메서드와 반대 개념입니다. 지정한 값 바로 앞에 위치한 아이템을 반환하며, 값이 존재하지 않거나 첫 번째 아이템일 경우 `null`을 반환합니다.

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

`chunk` 메서드는 컬렉션을 지정한 크기만큼 작게 여러 개의 컬렉션으로 분할합니다.

```php
$collection = collect([1, 2, 3, 4, 5, 6, 7]);

$chunks = $collection->chunk(4);

$chunks->all();

// [[1, 2, 3, 4], [5, 6, 7]]
```

이 메서드는 [Bootstrap](https://getbootstrap.com/docs/5.3/layout/grid/) 등 그리드 시스템을 이용해 [뷰](/docs/12.x/views) 에서 데이터를 나누어 보여줄 때 특히 유용합니다. 예를 들어, [Eloquent](/docs/12.x/eloquent) 모델 컬렉션을 그리드 형태로 보여주고 싶다면 다음과 같이 사용할 수 있습니다.

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

`chunkWhile` 메서드는 전달한 콜백 결과에 따라 컬렉션을 다수의 작은 컬렉션으로 나눕니다. 클로저의 `$chunk` 인자를 통해 직전 요소를 참고할 수 있습니다.

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

`collapse` 메서드는 여러 개의 배열이나 컬렉션이 들어 있는 컬렉션을 하나의 평평한(flat) 컬렉션으로 합쳐줍니다.

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

`collapseWithKeys` 메서드는 여러 배열이나 컬렉션이 담긴 컬렉션을, 키를 그대로 유지한 채 하나의 평평한 컬렉션으로 만듭니다.

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

`collect` 메서드는 현재 컬렉션의 아이템들로 새로운 `Collection` 인스턴스를 반환합니다.

```php
$collectionA = collect([1, 2, 3]);

$collectionB = $collectionA->collect();

$collectionB->all();

// [1, 2, 3]
```

이 메서드는 [지연 컬렉션](#lazy-collections) 을 일반적인 `Collection` 인스턴스로 변환할 때 주로 사용됩니다.

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
> `collect` 메서드는 `Enumerable` 인스턴스가 있을 때, 일반 컬렉션으로 변환해야 하는 경우에 특히 유용합니다. `collect()`는 `Enumerable` 계약의 일부이므로 언제든 안전하게 `Collection` 인스턴스로 변환할 수 있습니다.

<a name="method-combine"></a>
#### `combine()`

`combine` 메서드는 컬렉션 내부 값들을 키로 사용하고, 인자로 전달한 배열이나 컬렉션의 값들을 그 값에 매핑해서 새로운 컬렉션을 만듭니다.

```php
$collection = collect(['name', 'age']);

$combined = $collection->combine(['George', 29]);

$combined->all();

// ['name' => 'George', 'age' => 29]
```

<a name="method-concat"></a>
#### `concat()`

`concat` 메서드는 지정한 배열 또는 컬렉션의 값을 현재 컬렉션 맨 뒤에 덧붙입니다.

```php
$collection = collect(['John Doe']);

$concatenated = $collection->concat(['Jane Doe'])->concat(['name' => 'Johnny Doe']);

$concatenated->all();

// ['John Doe', 'Jane Doe', 'Johnny Doe']
```

`concat` 메서드는 추가된 아이템에 대해 키를 숫자로 다시 할당합니다(재인덱스). 연관(associative) 컬렉션의 키를 그대로 유지하려면 [merge](#method-merge) 메서드를 참고하세요.

<a name="method-contains"></a>
#### `contains()`

`contains` 메서드는 컬렉션에 특정 아이템이 포함되어 있는지 확인합니다. 검증 조건을 가진 클로저(익명 함수)를 전달해서, 컬렉션 내에 그 조건을 만족하는 요소가 존재하는지도 확인할 수 있습니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->contains(function (int $value, int $key) {
    return $value > 5;
});

// false
```

또는 컬렉션이 특정 값을 갖고 있는지를 문자열로 직접 지정해 검사할 수 있습니다.

```php
$collection = collect(['name' => 'Desk', 'price' => 100]);

$collection->contains('Desk');

// true

$collection->contains('New York');

// false
```

키/값 쌍을 전달하면, 해당하는 쌍이 존재하는지도 확인할 수 있습니다.

```php
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
]);

$collection->contains('product', 'Bookcase');

// false
```

`contains` 메서드는 값 비교 시 "느슨한" 비교를 사용하므로, 정수값이 담긴 문자열도 같은 값으로 봅니다. "엄격한" 비교를 통해 필터링하려면 [containsStrict](#method-containsstrict) 메서드를 사용하세요.

반대로, 컬렉션에 포함되어 있지 않은지를 확인하고 싶다면 [doesntContain](#method-doesntcontain) 메서드를 참고하세요.

<a name="method-containsoneitem"></a>
#### `containsOneItem()`

`containsOneItem` 메서드는 컬렉션에 단 하나의 아이템만 들어 있는지 확인합니다.

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
> [Eloquent 컬렉션](/docs/12.x/eloquent-collections#method-contains)을 사용할 때 이 메서드의 동작이 달라집니다.

<a name="method-count"></a>
#### `count()`

`count` 메서드는 컬렉션에 포함된 아이템의 전체 개수를 반환합니다.

```php
$collection = collect([1, 2, 3, 4]);

$collection->count();

// 4
```

<a name="method-countBy"></a>
#### `countBy()`

`countBy` 메서드는 컬렉션 내 값이 각각 몇 번 등장하는지 세어줍니다. 기본적으로는 모든 요소의 출현 횟수를 계산하므로, 특정 "유형"별로 요소의 개수를 셀 수 있습니다.

```php
$collection = collect([1, 2, 2, 2, 3]);

$counted = $collection->countBy();

$counted->all();

// [1 => 1, 2 => 3, 3 => 1]
```

`countBy` 메서드에 클로저(익명 함수)를 전달하여, 원하는 방식으로 아이템의 개수를 셀 수도 있습니다.

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

`crossJoin` 메서드는 현재 컬렉션과 전달한 배열 또는 컬렉션들을 교차 조인하여, 가능한 모든 조합(데카르트 곱, Cartesian product)을 반환합니다.

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

`dd` 메서드는 컬렉션의 아이템을 출력(dump)한 뒤 프로그램 실행을 즉시 중단합니다.

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

스크립트 실행을 중단하지 않고 값만 출력하고 싶다면 [dump](#method-dump) 메서드를 사용하면 됩니다.

<a name="method-diff"></a>
#### `diff()`

`diff` 메서드는 컬렉션을 다른 컬렉션이나 일반 PHP `array`와 값 기준으로 비교합니다. 이 메서드는 원래 컬렉션에는 있지만, 전달한 컬렉션에는 없는 값들을 반환합니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$diff = $collection->diff([2, 4, 6, 8]);

$diff->all();

// [1, 3, 5]
```

> [!NOTE]
> [Eloquent 컬렉션](/docs/12.x/eloquent-collections#method-diff)을 사용할 때 이 메서드의 동작이 달라집니다.

<a name="method-diffassoc"></a>
#### `diffAssoc()`

`diffAssoc` 메서드는 컬렉션을 다른 컬렉션이나 일반 PHP `array`와 키와 값 기준으로 비교합니다. 이 메서드는 원래 컬렉션에는 있지만, 전달한 컬렉션에는 없는 키 / 값 쌍을 반환합니다.

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

`diffAssoc`와 달리, `diffAssocUsing`은 인덱스(키) 비교를 위해 직접 콜백 함수를 지정할 수 있습니다.

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

콜백 함수는 비교 결과에 따라 0보다 작거나 같거나 큰 정수를 반환해야 합니다. 보다 자세한 내용은 내부적으로 이 메서드에서 사용되는 PHP의 [array_diff_uassoc](https://www.php.net/array_diff_uassoc#refsect1-function.array-diff-uassoc-parameters) 문서를 참고하세요.

<a name="method-diffkeys"></a>
#### `diffKeys()`

`diffKeys` 메서드는 컬렉션을 다른 컬렉션이나 일반 PHP `array`와 키 기준으로 비교하며, 원래 컬렉션에는 있지만 전달한 컬렉션에는 없는 키 / 값 쌍을 반환합니다.

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

`doesntContain` 메서드는 컬렉션에 특정 값이 **포함되어 있지 않은지** 여부를 확인합니다. 클로저(익명 함수)를 전달하면, 특정 조건을 만족하는 요소가 컬렉션에 없는지 검사할 수 있습니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->doesntContain(function (int $value, int $key) {
    return $value < 5;
});

// false
```

또는, 단순히 문자열을 전달하여 컬렉션에 해당 값이 없는지 확인할 수 있습니다.

```php
$collection = collect(['name' => 'Desk', 'price' => 100]);

$collection->doesntContain('Table');

// true

$collection->doesntContain('Desk');

// false
```

키 / 값 쌍을 전달하여 해당 쌍이 존재하지 않는지도 확인할 수 있습니다.

```php
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
]);

$collection->doesntContain('product', 'Bookcase');

// true
```

`doesntContain` 메서드는 값 비교 시 "느슨한(loose)" 비교를 사용하기 때문에, 숫자값을 가진 문자열과 동일한 숫자도 같은 값으로 간주됩니다.

<a name="method-dot"></a>
#### `dot()`

`dot` 메서드는 다차원 컬렉션을 "점(dot)" 표기법을 이용해 하나의 평면 컬렉션으로 변환합니다.

```php
$collection = collect(['products' => ['desk' => ['price' => 100]]]);

$flattened = $collection->dot();

$flattened->all();

// ['products.desk.price' => 100]
```

<a name="method-dump"></a>
#### `dump()`

`dump` 메서드는 컬렉션의 아이템을 출력(dump)합니다.

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

컬렉션을 출력한 후 스크립트 실행까지 중단하려면 [dd](#method-dd) 메서드를 사용하세요.

<a name="method-duplicates"></a>
#### `duplicates()`

`duplicates` 메서드는 컬렉션 내에 중복된 값만을 추출하여 반환합니다.

```php
$collection = collect(['a', 'b', 'a', 'c', 'b']);

$collection->duplicates();

// [2 => 'a', 4 => 'b']
```

컬렉션에 배열이나 객체가 포함된 경우, 중복 여부를 확인할 속성의 키를 지정할 수 있습니다.

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

`each` 메서드는 컬렉션 내 각 요소를 반복(iterate)하며, 각 요소를 클로저에 전달합니다.

```php
$collection = collect([1, 2, 3, 4]);

$collection->each(function (int $item, int $key) {
    // ...
});
```

요소 순회를 중단(stop)하고 싶을 경우, 클로저에서 `false`를 반환하면 됩니다.

```php
$collection->each(function (int $item, int $key) {
    if (/* condition */) {
        return false;
    }
});
```

<a name="method-eachspread"></a>
#### `eachSpread()`

`eachSpread` 메서드는 컬렉션 아이템이 배열일 때, 그 내부 값을 차례로 콜백의 인자(argument)로 전달하며 순회합니다.

```php
$collection = collect([['John Doe', 35], ['Jane Doe', 33]]);

$collection->eachSpread(function (string $name, int $age) {
    // ...
});
```

순회를 중단하려면 콜백에서 `false`를 반환할 수 있습니다.

```php
$collection->eachSpread(function (string $name, int $age) {
    return false;
});
```

<a name="method-ensure"></a>
#### `ensure()`

`ensure` 메서드는 컬렉션의 모든 요소가 특정 타입(혹은 타입들)에 해당하는지 검증할 때 사용합니다. 만약 일치하지 않는 요소가 있으면 `UnexpectedValueException` 예외가 발생합니다.

```php
return $collection->ensure(User::class);

return $collection->ensure([User::class, Customer::class]);
```

`string`, `int`, `float`, `bool`, `array`와 같은 기본 데이터 타입도 지정할 수 있습니다.

```php
return $collection->ensure('int');
```

> [!WARNING]
> `ensure` 메서드는 추후에 다른 타입의 요소가 컬렉션에 추가되는 것을 막아주진 않습니다.

<a name="method-every"></a>
#### `every()`

`every` 메서드는 컬렉션의 모든 요소가 주어진 조건을 만족하는지 확인할 때 사용합니다.

```php
collect([1, 2, 3, 4])->every(function (int $value, int $key) {
    return $value > 2;
});

// false
```

컬렉션이 비어 있을 경우, `every` 메서드는 항상 true를 반환합니다.

```php
$collection = collect([]);

$collection->every(function (int $value, int $key) {
    return $value > 2;
});

// true
```

<a name="method-except"></a>
#### `except()`

`except` 메서드는 지정한 키를 가진 아이템을 제외한 나머지 모든 아이템을 반환합니다.

```php
$collection = collect(['product_id' => 1, 'price' => 100, 'discount' => false]);

$filtered = $collection->except(['price', 'discount']);

$filtered->all();

// ['product_id' => 1]
```

반대로 특정 키만 반환하려면 [only](#method-only) 메서드를 참고하세요.

> [!NOTE]
> [Eloquent 컬렉션](/docs/12.x/eloquent-collections#method-except)을 사용할 때 이 메서드의 동작이 달라집니다.

<a name="method-filter"></a>
#### `filter()`

`filter` 메서드는 클로저로 전달한 조건에 맞는 아이템만 남기고 컬렉션을 필터링합니다.

```php
$collection = collect([1, 2, 3, 4]);

$filtered = $collection->filter(function (int $value, int $key) {
    return $value > 2;
});

$filtered->all();

// [3, 4]
```

콜백을 제공하지 않으면, `false`와 동일하게 간주되는 값들을 모두 제거합니다.

```php
$collection = collect([1, 2, 3, null, false, '', 0, []]);

$collection->filter()->all();

// [1, 2, 3]
```

반대로 동작하는 메서드가 필요할 때는 [reject](#method-reject) 메서드를 참고하세요.

<a name="method-first"></a>
#### `first()`

`first` 메서드는 컬렉션에서 주어진 조건을 처음으로 만족하는 요소를 반환합니다.

```php
collect([1, 2, 3, 4])->first(function (int $value, int $key) {
    return $value > 2;
});

// 3
```

인자를 전달하지 않으면 컬렉션의 첫 번째 요소를 반환합니다. 컬렉션이 비어 있으면 `null`을 반환합니다.

```php
collect([1, 2, 3, 4])->first();

// 1
```

<a name="method-first-or-fail"></a>
#### `firstOrFail()`

`firstOrFail` 메서드는 `first` 메서드와 동일하지만, 결과를 찾지 못할 경우 `Illuminate\Support\ItemNotFoundException` 예외를 발생시킵니다.

```php
collect([1, 2, 3, 4])->firstOrFail(function (int $value, int $key) {
    return $value > 5;
});

// Throws ItemNotFoundException...
```

인자를 전달하지 않으면 컬렉션의 첫 번째 요소를 반환합니다. 컬렉션이 비어 있을 경우에도 `Illuminate\Support\ItemNotFoundException` 예외가 발생합니다.

```php
collect([])->firstOrFail();

// Throws ItemNotFoundException...
```

<a name="method-first-where"></a>
#### `firstWhere()`

`firstWhere` 메서드는 컬렉션에서 특정 키 / 값 쌍을 가진 첫 번째 요소를 반환합니다.

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

비교 연산자를 함께 사용할 수도 있습니다.

```php
$collection->firstWhere('age', '>=', 18);

// ['name' => 'Diego', 'age' => 23]
```

[where](#method-where) 메서드처럼, `firstWhere`에 인자를 하나만 전달하면 해당 키의 값이 "참(truthy)"인 첫 번째 아이템을 반환합니다.

```php
$collection->firstWhere('age');

// ['name' => 'Linda', 'age' => 14]
```

<a name="method-flatmap"></a>
#### `flatMap()`

`flatMap` 메서드는 컬렉션을 순회하며 각 값을 클로저로 전달합니다. 이 클로저에서 아이템을 가공 후 반환하면, 가공된 아이템으로 새로운 컬렉션이 생성되고, 이 컬렉션은 한 단계(depth) 평탄화(flatten)된 배열로 바뀝니다.

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

`flatten` 메서드는 다차원 컬렉션을 한 단계 평탄화된(flattened) 컬렉션으로 만듭니다.

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

필요하다면, `flatten` 메서드에 "depth(깊이)" 인자를 전달할 수 있습니다.

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

이 예제에서, 만약 depth를 지정하지 않고 `flatten`을 호출하면 내부 배열까지 전부 평탄화되어 `['iPhone 6S', 'Apple', 'Galaxy S7', 'Samsung']`처럼 반환됩니다. depth 인자를 전달하면 내부 배열 중 몇 단계만 평탄화할지 제어할 수 있습니다.

<a name="method-flip"></a>

#### `flip()`

`flip` 메서드는 컬렉션의 키와 해당 값을 서로 맞바꿉니다.

```php
$collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

$flipped = $collection->flip();

$flipped->all();

// ['taylor' => 'name', 'laravel' => 'framework']
```

<a name="method-forget"></a>
#### `forget()`

`forget` 메서드는 지정한 키에 해당하는 항목을 컬렉션에서 제거합니다.

```php
$collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

// 하나의 키만 삭제...
$collection->forget('name');

// ['framework' => 'laravel']

// 여러 키 삭제...
$collection->forget(['name', 'framework']);

// []
```

> [!WARNING]
> 대부분의 컬렉션 메서드와 달리, `forget`은 새로운 컬렉션을 반환하지 않고, 호출한 컬렉션 인스턴스 자체를 수정합니다.

<a name="method-forpage"></a>
#### `forPage()`

`forPage` 메서드는 지정한 페이지 번호에 해당하는 항목만 포함하는 새로운 컬렉션을 반환합니다. 첫 번째 인수는 페이지 번호, 두 번째 인수는 페이지당 항목 수를 지정합니다.

```php
$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9]);

$chunk = $collection->forPage(2, 3);

$chunk->all();

// [4, 5, 6]
```

<a name="method-fromjson"></a>
#### `fromJson()`

정적 메서드인 `fromJson`은 주어진 JSON 문자열을 PHP의 `json_decode` 함수로 디코딩하여 새로운 컬렉션 인스턴스를 만듭니다.

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

`get` 메서드는 주어진 키에 해당하는 항목을 반환합니다. 해당 키가 존재하지 않으면 `null`을 반환합니다.

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

또한 기본값으로 콜백을 전달할 수도 있습니다. 지정한 키가 존재하지 않을 경우, 콜백의 반환값이 반환됩니다.

```php
$collection->get('email', function () {
    return 'taylor@example.com';
});

// taylor@example.com
```

<a name="method-groupby"></a>
#### `groupBy()`

`groupBy` 메서드는 컬렉션의 항목을 지정한 키로 그룹화합니다.

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

문자열 키 대신 콜백을 전달할 수도 있습니다. 이때 그룹의 키로 사용할 값을 콜백에서 반환해야 합니다.

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

여러 그룹화 조건을 배열로 전달할 수도 있습니다. 배열의 각 요소는 다차원 배열에서 해당 레벨에 적용됩니다.

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

`has` 메서드는 주어진 키가 컬렉션에 존재하는지 확인합니다.

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

`implode` 메서드는 컬렉션의 항목들을 문자열로 합칩니다. 컬렉션의 항목 타입에 따라 인수가 달라집니다. 만약 배열이나 오브젝트가 컬렉션에 포함되어 있다면, 합치고자 하는 속성의 키와 값을 연결할 "접착제(glue)" 문자열을 차례로 전달해야 합니다.

```php
$collection = collect([
    ['account_id' => 1, 'product' => 'Desk'],
    ['account_id' => 2, 'product' => 'Chair'],
]);

$collection->implode('product', ', ');

// 'Desk, Chair'
```

컬렉션에 단순 문자열이나 숫자 값만 있는 경우, "접착제"만 단일 인수로 전달하면 됩니다.

```php
collect([1, 2, 3, 4, 5])->implode('-');

// '1-2-3-4-5'
```

만약 각각의 값을 포맷팅해서 합치고 싶다면, `implode` 메서드에 클로저를 전달할 수도 있습니다.

```php
$collection->implode(function (array $item, int $key) {
    return strtoupper($item['product']);
}, ', ');

// 'DESK, CHAIR'
```

<a name="method-intersect"></a>
#### `intersect()`

`intersect` 메서드는 원본 컬렉션에서 주어진 배열 또는 컬렉션에 없는 값을 모두 제거합니다. 반환된 컬렉션은 원본의 키를 그대로 유지합니다.

```php
$collection = collect(['Desk', 'Sofa', 'Chair']);

$intersect = $collection->intersect(['Desk', 'Chair', 'Bookcase']);

$intersect->all();

// [0 => 'Desk', 2 => 'Chair']
```

> [!NOTE]
> 이 메서드는 [Eloquent 컬렉션](/docs/12.x/eloquent-collections#method-intersect)을 사용할 때 동작 방식이 다를 수 있습니다.

<a name="method-intersectusing"></a>
#### `intersectUsing()`

`intersectUsing` 메서드는 원본 컬렉션에서 주어진 배열 또는 컬렉션에 없는 값을 커스텀 콜백으로 비교해 제거합니다. 결과 컬렉션은 원본 컬렉션의 키를 그대로 유지합니다.

```php
$collection = collect(['Desk', 'Sofa', 'Chair']);

$intersect = $collection->intersectUsing(['desk', 'chair', 'bookcase'], function ($a, $b) {
    return strcasecmp($a, $b);
});

$intersect->all();

// [0 => 'Desk', 2 => 'Chair']
```

<a name="method-intersectAssoc"></a>
#### `intersectAssoc()`

`intersectAssoc` 메서드는 키/값 쌍이 모든 컬렉션에 존재하는 경우만을 반환합니다.

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

`intersectAssocUsing` 메서드는 커스텀 콜백을 이용해, 키와 값 모두의 일치 여부를 비교하여 두 컬렉션 모두에 존재하는 키/값 쌍만 반환합니다.

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
], function ($a, $b) {
    return strcasecmp($a, $b);
});

$intersect->all();

// ['Size' => 'M']
```

<a name="method-intersectbykeys"></a>
#### `intersectByKeys()`

`intersectByKeys` 메서드는 주어진 배열이나 컬렉션에 존재하지 않는 키와 해당 값을 모두 제거합니다.

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

`isEmpty` 메서드는 컬렉션이 비어 있으면 `true`, 아니면 `false`를 반환합니다.

```php
collect([])->isEmpty();

// true
```

<a name="method-isnotempty"></a>
#### `isNotEmpty()`

`isNotEmpty` 메서드는 컬렉션에 항목이 하나라도 있으면 `true`, 없으면 `false`를 반환합니다.

```php
collect([])->isNotEmpty();

// false
```

<a name="method-join"></a>
#### `join()`

`join` 메서드는 컬렉션의 값을 문자열로 합쳐 반환합니다. 두 번째 인수로 마지막 요소를 붙일 때 사용할 문자열을 지정할 수 있습니다.

```php
collect(['a', 'b', 'c'])->join(', '); // 'a, b, c'
collect(['a', 'b', 'c'])->join(', ', ', and '); // 'a, b, and c'
collect(['a', 'b'])->join(', ', ' and '); // 'a and b'
collect(['a'])->join(', ', ' and '); // 'a'
collect([])->join(', ', ' and '); // ''
```

<a name="method-keyby"></a>
#### `keyBy()`

`keyBy` 메서드는 지정한 키를 컬렉션의 새로운 키로 사용합니다. 여러 항목이 동일한 키를 갖는 경우, 마지막 항목만 새로운 컬렉션에 남게 됩니다.

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

콜백을 전달하면, 각 항목을 어떤 값으로 키를 생성할지 자유롭게 정의할 수 있습니다.

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

`last` 메서드는 주어진 조건을 만족하는 컬렉션의 마지막 요소를 반환합니다.

```php
collect([1, 2, 3, 4])->last(function (int $value, int $key) {
    return $value < 3;
});

// 2
```

인수 없이 호출하면 컬렉션의 마지막 요소를 반환합니다. 컬렉션이 비어 있으면 `null`을 반환합니다.

```php
collect([1, 2, 3, 4])->last();

// 4
```

<a name="method-lazy"></a>
#### `lazy()`

`lazy` 메서드는 주어진 배열을 기반으로 새로운 [LazyCollection](#lazy-collections) 인스턴스를 반환합니다.

```php
$lazyCollection = collect([1, 2, 3, 4])->lazy();

$lazyCollection::class;

// Illuminate\Support\LazyCollection

$lazyCollection->all();

// [1, 2, 3, 4]
```

이 메서드는 특히 많은 수의 항목을 가진 대용량 `Collection`에서 변환 작업이 필요할 때 유용합니다.

```php
$count = $hugeCollection
    ->lazy()
    ->where('country', 'FR')
    ->where('balance', '>', '100')
    ->count();
```

컬렉션을 `LazyCollection`으로 변환하면, 추가 메모리 할당을 거의 하지 않아도 수많은 항목에 대해 필터링 같은 작업을 할 수 있습니다. 원본 컬렉션 자체의 값은 여전히 메모리에 있지만, 그 이후의 필터링은 추가적인 메모리 부담 없이 이루어집니다.

<a name="method-macro"></a>
#### `macro()`

정적 메서드인 `macro`를 사용하면 실행 시간에 `Collection` 클래스에 새로운 메서드를 추가할 수 있습니다. 자세한 내용은 [컬렉션 확장하기](#extending-collections) 문서를 참고하세요.

<a name="method-make"></a>
#### `make()`

정적 메서드인 `make`는 새로운 컬렉션 인스턴스를 생성합니다. 자세한 내용은 [컬렉션 생성하기](#creating-collections) 섹션을 참조하세요.

```php
use Illuminate\Support\Collection;

$collection = Collection::make([1, 2, 3]);
```

<a name="method-map"></a>
#### `map()`

`map` 메서드는 컬렉션을 순회하며 각 값에 대해 지정한 콜백을 실행합니다. 콜백에서는 항목을 수정해서 반환할 수 있으며, 이 반환값들로 새 컬렉션이 생성됩니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$multiplied = $collection->map(function (int $item, int $key) {
    return $item * 2;
});

$multiplied->all();

// [2, 4, 6, 8, 10]
```

> [!WARNING]
> 대부분의 컬렉션 메서드와 마찬가지로, `map`은 항상 새로운 컬렉션 인스턴스를 반환하며 호출한 컬렉션 자체를 수정하지 않습니다. 원본 컬렉션 자체를 변환하려면 [transform](#method-transform) 메서드를 사용하세요.

<a name="method-mapinto"></a>
#### `mapInto()`

`mapInto()` 메서드는 컬렉션을 순회하며 각 값을 지정한 클래스의 생성자에 전달하여, 새로운 클래스 인스턴스를 만들어 반환하는 컬렉션을 생성합니다.

```php
class Currency
{
    /**
     * 새로운 Currency 인스턴스를 생성합니다.
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

`mapSpread` 메서드는 컬렉션의 각 아이템(중첩된 값들)을 꺼내서 주어진 클로저에 전달합니다. 이 클로저에서는 각 값을 자유롭게 가공하여 반환할 수 있으며, 최종적으로 수정된 값들로 새로운 컬렉션이 만들어집니다:

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

`mapToGroups` 메서드는 컬렉션의 아이템들을 주어진 클로저의 반환값에 따라 그룹화합니다. 클로저는 하나의 키/값 쌍으로 이루어진 연관 배열을 반환해야 하며, 이 과정을 통해 그룹화된 값들의 새로운 컬렉션이 생성됩니다:

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

`mapWithKeys` 메서드는 컬렉션의 각 값을 주어진 콜백에 전달하며, 콜백은 반드시 하나의 키/값 쌍이 담긴 연관 배열을 반환해야 합니다:

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

`max` 메서드는 주어진 키의 최대값을 반환합니다:

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

`median` 메서드는 주어진 키의 [중앙값(중간값)](https://en.wikipedia.org/wiki/Median)을 반환합니다:

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

`merge` 메서드는 주어진 배열 또는 컬렉션을 기존 컬렉션과 병합합니다. 만약 주어진 아이템에 포함된 문자열 키가 기존 컬렉션에도 존재한다면, 기존 값은 새로운 값으로 덮어씌워집니다:

```php
$collection = collect(['product_id' => 1, 'price' => 100]);

$merged = $collection->merge(['price' => 200, 'discount' => false]);

$merged->all();

// ['product_id' => 1, 'price' => 200, 'discount' => false]
```

만약 주어진 아이템의 키가 숫자형이라면, 값들이 컬렉션 맨 뒤에 추가됩니다:

```php
$collection = collect(['Desk', 'Chair']);

$merged = $collection->merge(['Bookcase', 'Door']);

$merged->all();

// ['Desk', 'Chair', 'Bookcase', 'Door']
```

<a name="method-mergerecursive"></a>
#### `mergeRecursive()`

`mergeRecursive` 메서드는 주어진 배열 또는 컬렉션을 기존 컬렉션과 재귀적으로 병합합니다. 만약 두 컬렉션에 동일한 문자열 키가 있다면, 해당 키의 값이 배열로 합쳐지고, 이 과정이 재귀적으로 반복됩니다:

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

`min` 메서드는 주어진 키의 최소값을 반환합니다:

```php
$min = collect([['foo' => 10], ['foo' => 20]])->min('foo');

// 10

$min = collect([1, 2, 3, 4, 5])->min();

// 1
```

<a name="method-mode"></a>
#### `mode()`

`mode` 메서드는 주어진 키의 [최빈값(가장 자주 등장하는 값)](https://en.wikipedia.org/wiki/Mode_(statistics))을 반환합니다:

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

`multiply` 메서드는 컬렉션 내의 모든 항목의 복사본을 지정한 횟수만큼 생성합니다:

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

`nth` 메서드는 컬렉션의 N번째마다 하나씩의 요소만을 모아서 새로운 컬렉션을 만듭니다:

```php
$collection = collect(['a', 'b', 'c', 'd', 'e', 'f']);

$collection->nth(4);

// ['a', 'e']
```

두 번째 인자로 시작 오프셋(출발 위치)을 지정할 수도 있습니다:

```php
$collection->nth(4, 1);

// ['b', 'f']
```

<a name="method-only"></a>
#### `only()`

`only` 메서드는 컬렉션에서 지정한 키의 아이템만 반환합니다:

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
> 이 메서드는 [Eloquent 컬렉션](/docs/12.x/eloquent-collections#method-only)을 사용할 경우 동작이 달라질 수 있습니다.

<a name="method-pad"></a>
#### `pad()`

`pad` 메서드는 배열의 길이가 원하는 크기에 도달할 때까지 주어진 값으로 채워 넣습니다. 이 메서드는 PHP의 [array_pad](https://secure.php.net/manual/en/function.array-pad.php) 함수와 동작이 동일합니다.

왼쪽에 값을 채워넣고 싶다면, 원하는 크기를 음수로 지정해야 합니다. 만약 지정한 크기의 절대값이 배열 길이보다 작거나 같다면 아무런 동작도 하지 않습니다:

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

`partition` 메서드는 PHP의 배열 구조 분해 기능과 함께 사용하면, 조건에 따라 참을 반환하는 요소와 그렇지 않은 요소를 분리할 수 있습니다:

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
> 이 메서드는 [Eloquent 컬렉션](/docs/12.x/eloquent-collections#method-partition)과 동작이 다를 수 있습니다.

<a name="method-percentage"></a>
#### `percentage()`

`percentage` 메서드는 주어진 조건을 만족하는 아이템이 컬렉션 전체에서 차지하는 비율(%)을 빠르게 구할 수 있습니다:

```php
$collection = collect([1, 1, 2, 2, 2, 3]);

$percentage = $collection->percentage(fn ($value) => $value === 1);

// 33.33
```

기본적으로 소수점 둘째 자리까지 반올림되며, 두 번째 인자(precision)를 이용해 소숫점 자릿수를 변경할 수 있습니다:

```php
$percentage = $collection->percentage(fn ($value) => $value === 1, precision: 3);

// 33.333
```

<a name="method-pipe"></a>
#### `pipe()`

`pipe` 메서드는 컬렉션을 주어진 클로저에 전달하고, 클로저 내부에서 가공된 결과를 반환합니다:

```php
$collection = collect([1, 2, 3]);

$piped = $collection->pipe(function (Collection $collection) {
    return $collection->sum();
});

// 6
```

<a name="method-pipeinto"></a>
#### `pipeInto()`

`pipeInto` 메서드는 주어진 클래스의 새 인스턴스를 생성하고, 해당 클래스 생성자에 컬렉션을 전달합니다:

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

`pipeThrough` 메서드는 컬렉션을 주어진 클로저 배열에 차례로 전달하며, 각 클로저의 실행 결과를 반환합니다:

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

`pluck` 메서드는 주어진 키의 모든 값을 추출하여 반환합니다:

```php
$collection = collect([
    ['product_id' => 'prod-100', 'name' => 'Desk'],
    ['product_id' => 'prod-200', 'name' => 'Chair'],
]);

$plucked = $collection->pluck('name');

$plucked->all();

// ['Desk', 'Chair']
```

결과 컬렉션의 키를 지정하고 싶을 때는 두 번째 인자를 사용할 수 있습니다:

```php
$plucked = $collection->pluck('name', 'product_id');

$plucked->all();

// ['prod-100' => 'Desk', 'prod-200' => 'Chair']
```

또한, `pluck` 메서드는 "dot" 표기법을 사용하여 중첩된 값도 추출할 수 있습니다:

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

만약 중복되는 키가 존재할 경우, 마지막에 일치하는 요소가 pluck된 컬렉션에 들어갑니다:

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

`pop` 메서드는 컬렉션에서 마지막 아이템을 제거하고 그 값을 반환합니다:

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->pop();

// 5

$collection->all();

// [1, 2, 3, 4]
```

`pop` 메서드에 정수를 전달하면 컬렉션의 끝에서 여러 개의 아이템을 한 번에 제거하고 반환할 수 있습니다:

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->pop(3);

// collect([5, 4, 3])

$collection->all();

// [1, 2]
```

<a name="method-prepend"></a>
#### `prepend()`

`prepend` 메서드는 컬렉션의 맨 앞에 아이템을 추가합니다:

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->prepend(0);

$collection->all();

// [0, 1, 2, 3, 4, 5]
```

추가할 아이템의 키를 두 번째 인자로 지정할 수도 있습니다:

```php
$collection = collect(['one' => 1, 'two' => 2]);

$collection->prepend(0, 'zero');

$collection->all();

// ['zero' => 0, 'one' => 1, 'two' => 2]
```

<a name="method-pull"></a>
#### `pull()`

`pull` 메서드는 컬렉션에서 지정한 키의 아이템을 제거하고 해당 값을 반환합니다:

```php
$collection = collect(['product_id' => 'prod-100', 'name' => 'Desk']);

$collection->pull('name');

// 'Desk'

$collection->all();

// ['product_id' => 'prod-100']
```

<a name="method-push"></a>
#### `push()`

`push` 메서드는 컬렉션의 맨 뒤에 아이템을 추가합니다:

```php
$collection = collect([1, 2, 3, 4]);

$collection->push(5);

$collection->all();

// [1, 2, 3, 4, 5]
```

<a name="method-put"></a>

#### `put()`

`put` 메서드는 지정한 키와 값을 컬렉션에 추가하거나 설정합니다.

```php
$collection = collect(['product_id' => 1, 'name' => 'Desk']);

$collection->put('price', 100);

$collection->all();

// ['product_id' => 1, 'name' => 'Desk', 'price' => 100]
```

<a name="method-random"></a>
#### `random()`

`random` 메서드는 컬렉션에서 임의의 항목 하나를 반환합니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->random();

// 4 - (임의로 반환된 값)
```

`random` 메서드에 정수를 전달하면, 지정한 개수만큼의 임의의 항목들을 반환합니다. 여러 항목을 요청할 경우 항상 컬렉션 형태로 반환됩니다.

```php
$random = $collection->random(3);

$random->all();

// [2, 4, 5] - (임의로 반환된 값)
```

컬렉션 내 항목 개수가 요청한 개수보다 적을 경우, `random` 메서드는 `InvalidArgumentException` 예외를 발생시킵니다.

또한 `random` 메서드는 현재 컬렉션 인스턴스를 인자로 받는 클로저를 전달할 수도 있습니다.

```php
use Illuminate\Support\Collection;

$random = $collection->random(fn (Collection $items) => min(10, count($items)));

$random->all();

// [1, 2, 3, 4, 5] - (임의로 반환된 값)
```

<a name="method-range"></a>
#### `range()`

`range` 메서드는 지정한 범위에 해당하는 정수들을 담은 컬렉션을 반환합니다.

```php
$collection = collect()->range(3, 6);

$collection->all();

// [3, 4, 5, 6]
```

<a name="method-reduce"></a>
#### `reduce()`

`reduce` 메서드는 컬렉션을 하나의 값으로 축소합니다. 각 반복의 결과가 그다음 반복에 인자로 전달됩니다.

```php
$collection = collect([1, 2, 3]);

$total = $collection->reduce(function (?int $carry, int $item) {
    return $carry + $item;
});

// 6
```

첫 번째 반복에서 `$carry`의 값은 `null`이지만, 두 번째 인수로 초기값을 지정할 수도 있습니다.

```php
$collection->reduce(function (int $carry, int $item) {
    return $carry + $item;
}, 4);

// 10
```

`reduce` 메서드는 또한 배열의 키도 콜백 함수에 인자로 전달합니다.

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

`reduceSpread` 메서드는 컬렉션을 하나의 값이 아니라 여러 값으로 축소합니다. 각 반복의 결과가 여러 값을 담을 수 있으며, 그 결과들이 다음 반복에 전달됩니다. 이 메서드는 `reduce`와 유사하지만, 여러 개의 초기값도 전달할 수 있습니다.

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

`reject` 메서드는 전달받은 클로저를 이용해 컬렉션을 필터링합니다. 클로저가 `true`를 반환하는 항목은 결과 컬렉션에서 제외됩니다.

```php
$collection = collect([1, 2, 3, 4]);

$filtered = $collection->reject(function (int $value, int $key) {
    return $value > 2;
});

$filtered->all();

// [1, 2]
```

`reject` 메서드의 반대 기능이 필요한 경우 [filter](#method-filter) 메서드를 참고하세요.

<a name="method-replace"></a>
#### `replace()`

`replace` 메서드는 `merge`와 유사하지만, 문자열 키가 일치하는 항목뿐만 아니라, 숫자 키가 일치하는 항목도 덮어쓴다는 점이 다릅니다.

```php
$collection = collect(['Taylor', 'Abigail', 'James']);

$replaced = $collection->replace([1 => 'Victoria', 3 => 'Finn']);

$replaced->all();

// ['Taylor', 'Victoria', 'James', 'Finn']
```

<a name="method-replacerecursive"></a>
#### `replaceRecursive()`

이 메서드는 `replace`와 비슷하게 동작하지만, 배열 내부 값까지 재귀적으로 진입하여 동일한 방식으로 항목을 교체합니다.

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

`reverse` 메서드는 컬렉션 내 항목의 순서를 뒤집어 반환합니다. 이때 원래의 키는 그대로 유지됩니다.

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

`search` 메서드는 컬렉션에서 전달받은 값을 찾아, 발견되면 해당 키를 반환합니다. 찾지 못하면 `false`를 반환합니다.

```php
$collection = collect([2, 4, 6, 8]);

$collection->search(4);

// 1
```

검색은 "느슨한(loose)" 비교로 이루어집니다. 즉, 문자열 형태의 숫자도 동일한 정수와 같은 값으로 간주됩니다. "엄격한(strict)" 비교를 원한다면 메서드의 두 번째 인자로 `true`를 전달하면 됩니다.

```php
collect([2, 4, 6, 8])->search('4', strict: true);

// false
```

또는, 자신만의 클로저를 전달하여 조건에 부합하는 첫 번째 항목을 찾을 수도 있습니다.

```php
collect([2, 4, 6, 8])->search(function (int $item, int $key) {
    return $item > 5;
});

// 2
```

<a name="method-select"></a>
#### `select()`

`select` 메서드는 SQL의 `SELECT` 구문처럼 지정한 키만을 선택해 컬렉션을 만듭니다.

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

`shift` 메서드에 정수를 전달하면 컬렉션의 앞쪽에서 여러 항목을 제거하고 반환할 수 있습니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->shift(3);

// collect([1, 2, 3])

$collection->all();

// [4, 5]
```

<a name="method-shuffle"></a>
#### `shuffle()`

`shuffle` 메서드는 컬렉션 내 항목들의 순서를 무작위로 섞어줍니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$shuffled = $collection->shuffle();

$shuffled->all();

// [3, 2, 5, 1, 4] - (임의로 섞인 값)
```

<a name="method-skip"></a>
#### `skip()`

`skip` 메서드는 컬렉션의 앞에서 지정한 개수만큼의 항목을 건너뛴 새로운 컬렉션을 반환합니다.

```php
$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);

$collection = $collection->skip(4);

$collection->all();

// [5, 6, 7, 8, 9, 10]
```

<a name="method-skipuntil"></a>
#### `skipUntil()`

`skipUntil` 메서드는 주어진 콜백이 `false`를 반환하는 동안 컬렉션의 항목을 건너뜁니다. 콜백이 처음으로 `true`를 반환하는 시점부터 끝까지의 항목이 새로운 컬렉션이 되어 반환됩니다.

```php
$collection = collect([1, 2, 3, 4]);

$subset = $collection->skipUntil(function (int $item) {
    return $item >= 3;
});

$subset->all();

// [3, 4]
```

또한, 콜백 대신 특정 값 하나를 전달하여 그 값이 나올 때까지 모든 항목을 건너뛸 수도 있습니다.

```php
$collection = collect([1, 2, 3, 4]);

$subset = $collection->skipUntil(3);

$subset->all();

// [3, 4]
```

> [!WARNING]
> 만약 지정한 값이 컬렉션에 없거나 콜백이 끝까지 한 번도 `true`를 반환하지 않으면, `skipUntil` 메서드는 빈 컬렉션을 반환합니다.

<a name="method-skipwhile"></a>
#### `skipWhile()`

`skipWhile` 메서드는 주어진 콜백이 `true`를 반환하는 동안 컬렉션의 항목을 건너뜁니다. 콜백이 처음으로 `false`를 반환하는 시점부터 끝까지의 항목이 새로운 컬렉션이 되어 반환됩니다.

```php
$collection = collect([1, 2, 3, 4]);

$subset = $collection->skipWhile(function (int $item) {
    return $item <= 3;
});

$subset->all();

// [4]
```

> [!WARNING]
> 콜백이 끝까지 한 번도 `false`를 반환하지 않으면, `skipWhile` 메서드는 빈 컬렉션을 반환합니다.

<a name="method-slice"></a>
#### `slice()`

`slice` 메서드는 특정 인덱스부터 시작하는 컬렉션의 일부(슬라이스)를 반환합니다.

```php
$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);

$slice = $collection->slice(4);

$slice->all();

// [5, 6, 7, 8, 9, 10]
```

슬라이스의 크기를 제한하려면 두 번째 인수로 원하는 크기를 지정하면 됩니다.

```php
$slice = $collection->slice(4, 2);

$slice->all();

// [5, 6]
```

반환된 슬라이스는 기본적으로 키를 보존합니다. 만약 원본 키의 보존이 필요하지 않다면 [values](#method-values) 메서드로 재인덱싱할 수 있습니다.

<a name="method-sliding"></a>
#### `sliding()`

`sliding` 메서드는 컬렉션 내 항목들을 "슬라이딩 윈도우" 방식으로 분할한 새로운 컬렉션(덩어리들)을 반환합니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$chunks = $collection->sliding(2);

$chunks->toArray();

// [[1, 2], [2, 3], [3, 4], [4, 5]]
```

특히 [eachSpread](#method-eachspread) 메서드와 결합하여 사용할 때 유용합니다.

```php
$transactions->sliding(2)->eachSpread(function (Collection $previous, Collection $current) {
    $current->total = $previous->total + $current->amount;
});
```

또한, 두 번째 인수로 "step" 값을 지정하여 각 덩어리의 첫 번째 항목 간의 간격을 조절할 수 있습니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$chunks = $collection->sliding(3, step: 2);

$chunks->toArray();

// [[1, 2, 3], [3, 4, 5]]
```

<a name="method-sole"></a>
#### `sole()`

`sole` 메서드는 조건을 만족하는 단 하나의 요소만 있을 때, 그 첫 번째 요소를 반환합니다.

```php
collect([1, 2, 3, 4])->sole(function (int $value, int $key) {
    return $value === 2;
});

// 2
```

또한, `sole` 메서드에 키/값 쌍을 지정해서 해당 값이 단 하나만 일치하면 그것을 반환할 수도 있습니다.

```php
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
]);

$collection->sole('product', 'Chair');

// ['product' => 'Chair', 'price' => 100]
```

아무 인자도 없이 호출해, 컬렉션에 요소가 단 하나뿐이라면 그 요소를 바로 반환하는 것도 가능합니다.

```php
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
]);

$collection->sole();

// ['product' => 'Desk', 'price' => 200]
```

`sole` 메서드로 반환할 요소가 하나도 없다면 `\Illuminate\Collections\ItemNotFoundException` 예외가 발생합니다. 여러 개가 일치하는 경우에는 `\Illuminate\Collections\MultipleItemsFoundException` 예외가 발생합니다.

<a name="method-some"></a>
#### `some()`

[contains](#method-contains) 메서드의 별칭입니다.

<a name="method-sort"></a>
#### `sort()`

`sort` 메서드는 컬렉션의 항목을 정렬합니다. 정렬된 컬렉션은 원본 배열의 키를 그대로 유지하므로, 아래 예시처럼 [values](#method-values) 메서드를 이용해 키를 0부터의 연속된 인덱스로 초기화할 수 있습니다.

```php
$collection = collect([5, 3, 1, 2, 4]);

$sorted = $collection->sort();

$sorted->values()->all();

// [1, 2, 3, 4, 5]
```

정렬 로직이 더 복잡하다면, 콜백을 전달해 자신만의 알고리즘을 정의할 수도 있습니다. 컬렉션의 `sort` 메서드는 내부적으로 PHP의 [uasort](https://secure.php.net/manual/en/function.uasort.php#refsect1-function.uasort-parameters)를 사용합니다.

> [!NOTE]
> 중첩 배열이나 객체 등으로 구성된 컬렉션을 정렬하려면 [sortBy](#method-sortby) 또는 [sortByDesc](#method-sortbydesc) 메서드를 참고하세요.

<a name="method-sortby"></a>
#### `sortBy()`

`sortBy` 메서드는 지정한 키로 컬렉션을 정렬합니다. 정렬된 컬렉션은 원래 배열의 키를 유지하므로, 아래 예시에서는 [values](#method-values) 메서드로 인덱스를 초기화하고 있습니다.

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

`sortBy` 메서드는 두 번째 인수로 [정렬 플래그](https://www.php.net/manual/en/function.sort.php)도 사용할 수 있습니다.

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

또한, 값 정렬 기준을 정의하는 클로저를 직접 전달할 수도 있습니다.

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

여러 속성으로 정렬하고 싶다면, `sortBy` 메서드에 정렬 기준들을 배열 형태로 전달할 수 있습니다. 각각의 정렬 기준은 정렬할 속성과 정렬 방향이 들어간 배열이어야 합니다.

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

여러 속성으로 정렬할 때, 각 기준 자체를 정의하는 클로저를 전달할 수도 있습니다.

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

이 메서드는 [sortBy](#method-sortby) 메서드와 동일한 시그니처를 가지지만, 컬렉션을 반대 방향(내림차순)으로 정렬합니다.

<a name="method-sortdesc"></a>
#### `sortDesc()`

이 메서드는 [sort](#method-sort) 메서드와는 반대로, 컬렉션을 내림차순으로 정렬합니다.

```php
$collection = collect([5, 3, 1, 2, 4]);

$sorted = $collection->sortDesc();

$sorted->values()->all();

// [5, 4, 3, 2, 1]
```

`sort`와 달리, `sortDesc`에는 클로저를 전달할 수 없습니다. 대신 [sort](#method-sort) 메서드를 사용한 뒤 비교 결과를 반대로 만들어야 합니다.

<a name="method-sortkeys"></a>
#### `sortKeys()`

`sortKeys` 메서드는 컬렉션을 내부의 연관 배열 키 기준으로 정렬합니다.

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

이 메서드는 [sortKeys](#method-sortkeys) 메서드와 동일한 시그니처를 가지지만, 컬렉션을 반대 방향(내림차순)으로 정렬합니다.

<a name="method-sortkeysusing"></a>
#### `sortKeysUsing()`

`sortKeysUsing` 메서드는 콜백 함수를 이용하여 내부 연관 배열의 키 기준으로 컬렉션을 정렬합니다.

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

콜백 함수는 비교 함수여야 하며, 0보다 작은 수, 0, 0보다 큰 수 중 하나의 정수를 반환해야 합니다. 자세한 내용은 PHP 공식 문서의 [uksort](https://www.php.net/manual/en/function.uksort.php#refsect1-function.uksort-parameters) 문서를 참고하세요. 이 메서드는 내부적으로 PHP의 `uksort` 함수를 사용합니다.

<a name="method-splice"></a>
#### `splice()`

`splice` 메서드는 지정한 인덱스에서 시작하여 항목 일부를 제거하고, 제거된 항목의 슬라이스를 반환합니다.

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

또한, 세 번째 인수로 제거되는 항목 대신 새 항목을 추가할 수도 있습니다.

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

`split` 메서드는 컬렉션을 지정한 개수만큼 그룹으로 분할합니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$groups = $collection->split(3);

$groups->all();

// [[1, 2], [3, 4], [5]]
```

<a name="method-splitin"></a>
#### `splitIn()`

`splitIn` 메서드는 컬렉션을 지정한 개수만큼 그룹으로 분할합니다. 이때 마지막 그룹을 제외한 앞의 그룹들을 가능한 한 모두 꽉 채운 뒤, 남은 원소를 마지막 그룹에 할당합니다.

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

컬렉션에 중첩 배열이나 객체가 포함된 경우, 합계를 구할 값을 결정할 키를 전달해야 합니다.

```php
$collection = collect([
    ['name' => 'JavaScript: The Good Parts', 'pages' => 176],
    ['name' => 'JavaScript: The Definitive Guide', 'pages' => 1096],
]);

$collection->sum('pages');

// 1272
```

또한, 합계를 구할 값을 직접 지정하려면 클로저를 전달할 수도 있습니다.

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

`take` 메서드는 지정한 개수만큼의 항목으로 구성된 새로운 컬렉션을 반환합니다.

```php
$collection = collect([0, 1, 2, 3, 4, 5]);

$chunk = $collection->take(3);

$chunk->all();

// [0, 1, 2]
```

음수 값을 전달하면 컬렉션의 끝에서부터 지정한 개수만큼의 항목을 가져올 수 있습니다.

```php
$collection = collect([0, 1, 2, 3, 4, 5]);

$chunk = $collection->take(-2);

$chunk->all();

// [4, 5]
```

<a name="method-takeuntil"></a>
#### `takeUntil()`

`takeUntil` 메서드는 전달된 콜백이 `true`를 반환할 때까지 컬렉션의 항목을 반환합니다.

```php
$collection = collect([1, 2, 3, 4]);

$subset = $collection->takeUntil(function (int $item) {
    return $item >= 3;
});

$subset->all();

// [1, 2]
```

또한, 단순한 값을 전달하여 해당 값이 나올 때까지의 항목을 반환받을 수도 있습니다.

```php
$collection = collect([1, 2, 3, 4]);

$subset = $collection->takeUntil(3);

$subset->all();

// [1, 2]
```

> [!WARNING]
> 전달된 값이 컬렉션에서 찾아지지 않거나, 콜백이 한 번도 `true`를 반환하지 않는 경우 `takeUntil` 메서드는 컬렉션의 모든 항목을 반환합니다.

<a name="method-takewhile"></a>
#### `takeWhile()`

`takeWhile` 메서드는 전달된 콜백이 `false`를 반환할 때까지 컬렉션의 항목을 반환합니다.

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

`tap` 메서드는 컬렉션 전체를 지정한 콜백에 전달하여, 컬렉션의 특정 지점에서 값을 "가로채서(tap)", 무언가를 수행하게 해줍니다. 이 과정에서 컬렉션 자체는 변경되지 않으며, 그 후 컬렉션 인스턴스를 다시 반환합니다.

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

정적 메서드인 `times`는 지정한 횟수만큼 클로저를 실행해서, 그 결과 값들로 새로운 컬렉션을 생성합니다.

```php
$collection = Collection::times(10, function (int $number) {
    return $number * 9;
});

$collection->all();

// [9, 18, 27, 36, 45, 54, 63, 72, 81, 90]
```

<a name="method-toarray"></a>
#### `toArray()`

`toArray` 메서드는 컬렉션을 일반 PHP `array`로 변환합니다. 컬렉션의 값이 [Eloquent](/docs/12.x/eloquent) 모델이라면, 모델 또한 배열로 변환됩니다.

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
> `toArray`는 컬렉션의 모든 중첩 객체가 `Arrayable` 인스턴스인 경우 배열로 변환합니다. 컬렉션이 원래 가지고 있던 배열을 그대로 반환받으려면 [all](#method-all) 메서드를 사용하세요.

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

`transform` 메서드는 컬렉션의 각 항목에 대해 지정된 콜백을 실행하며, 해당 콜백이 반환하는 값으로 컬렉션 내 항목이 교체됩니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->transform(function (int $item, int $key) {
    return $item * 2;
});

$collection->all();

// [2, 4, 6, 8, 10]
```

> [!WARNING]
> 대부분의 다른 컬렉션 메서드와 달리, `transform`은 컬렉션 인스턴스 자체를 변경합니다. 새로운 컬렉션을 생성하고 싶다면 [map](#method-map) 메서드를 사용하세요.

<a name="method-undot"></a>
#### `undot()`

`undot` 메서드는 "dot" 표기법을 사용하는 1차원 컬렉션을 다차원 컬렉션으로 확장합니다.

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

`union` 메서드는 전달된 배열을 컬렉션에 추가합니다. 만약 전달된 배열에 기존 컬렉션과 동일한 키가 있다면, 컬렉션의 값이 우선하여 유지됩니다.

```php
$collection = collect([1 => ['a'], 2 => ['b']]);

$union = $collection->union([3 => ['c'], 1 => ['d']]);

$union->all();

// [1 => ['a'], 2 => ['b'], 3 => ['c']]
```

<a name="method-unique"></a>
#### `unique()`

`unique` 메서드는 컬렉션 내 고유한 항목만 반환합니다. 반환된 컬렉션은 원래 배열의 키를 그대로 사용하므로, 예제에서는 [values](#method-values) 메서드를 사용하여 키를 연속된 인덱스로 재설정했습니다.

```php
$collection = collect([1, 1, 2, 2, 3, 4, 2]);

$unique = $collection->unique();

$unique->values()->all();

// [1, 2, 3, 4]
```

중첩 배열이나 객체가 포함된 컬렉션의 경우, 고유성을 판단하는 기준이 되는 키를 지정할 수 있습니다.

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

마지막으로, 고유성 판단에 사용할 값을 직접 지정하려면, 클로저를 `unique` 메서드에 전달할 수 있습니다.

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

`unique` 메서드는 값 비교 시 "느슨한(loose)" 비교를 사용하므로, 동일한 값을 가진 문자열과 정수는 같은 값으로 간주됩니다. 보다 엄격한 비교를 원한다면 [uniqueStrict](#method-uniquestrict) 메서드를 사용하세요.

> [!NOTE]
> [Eloquent 컬렉션](/docs/12.x/eloquent-collections#method-unique)을 사용할 때 이 메서드의 동작이 달라질 수 있습니다.

<a name="method-uniquestrict"></a>
#### `uniqueStrict()`

이 메서드는 [unique](#method-unique) 메서드와 동일한 시그니처를 갖지만, 모든 값을 "엄격한(strict)" 비교로 판별합니다.

<a name="method-unless"></a>
#### `unless()`

`unless` 메서드는 첫 번째 인수의 평가 결과가 `true`가 아닐 때에만, 지정한 콜백을 실행합니다. 컬렉션 인스턴스와 `unless` 메서드에 전달된 첫 번째 인수가 클로저에 함께 전달됩니다.

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

두 번째 콜백을 `unless` 메서드에 전달할 수 있습니다. 이 두 번째 콜백은 첫 번째 인수가 `true`로 평가될 때 실행됩니다.

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

`unless`와 반대 동작을 하고 싶다면 [when](#method-when) 메서드를 참고하세요.

<a name="method-unlessempty"></a>
#### `unlessEmpty()`

[whenNotEmpty](#method-whennotempty) 메서드의 별칭입니다.

<a name="method-unlessnotempty"></a>
#### `unlessNotEmpty()`

[whenEmpty](#method-whenempty) 메서드의 별칭입니다.

<a name="method-unwrap"></a>
#### `unwrap()`

정적 메서드인 `unwrap`은 컬렉션 적용이 가능한 값이라면 그 내부의 아이템을, 아니라면 원본 값을 그대로 반환합니다.

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

`values` 메서드는 키를 0부터 시작하는 연속된 정수로 초기화한 새로운 컬렉션을 반환합니다.

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

`when` 메서드는 첫 번째 인자로 전달한 값이 `true`로 평가될 때, 지정한 콜백을 실행합니다. `when` 메서드에는 컬렉션 인스턴스와 첫 번째 인자가 클로저로 전달됩니다.

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

`when` 메서드에는 두 번째 콜백을 추가로 전달할 수 있습니다. 이 두 번째 콜백은 첫 번째 인자가 `false`로 평가될 때 실행됩니다.

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

`when` 메서드의 반대 기능은 [unless](#method-unless) 메서드를 참고하시기 바랍니다.

<a name="method-whenempty"></a>
#### `whenEmpty()`

`whenEmpty` 메서드는 컬렉션이 비어 있을 때, 지정한 콜백을 실행합니다.

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

또한, 컬렉션이 비어 있지 않을 때 실행되는 두 번째 클로저를 `whenEmpty` 메서드에 전달할 수도 있습니다.

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

`whenEmpty` 메서드의 반대 기능은 [whenNotEmpty](#method-whennotempty) 메서드를 참고하세요.

<a name="method-whennotempty"></a>
#### `whenNotEmpty()`

`whenNotEmpty` 메서드는 컬렉션이 비어 있지 않을 때, 지정한 콜백을 실행합니다.

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

또한, 컬렉션이 비어 있을 때 실행되는 두 번째 클로저를 `whenNotEmpty` 메서드에 전달할 수도 있습니다.

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

`whenNotEmpty` 메서드의 반대 기능은 [whenEmpty](#method-whenempty) 메서드를 참고하세요.

<a name="method-where"></a>
#### `where()`

`where` 메서드는 지정한 키/값 쌍으로 컬렉션을 필터링합니다.

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

`where` 메서드는 아이템 값을 비교할 때 "느스한(loose)" 비교를 사용합니다. 즉, 문자열로 된 값이 정수와 같은 값일 경우에도 같다고 간주합니다. 엄격한 비교를 통해 필터링하려면 [whereStrict](#method-wherestrict) 메서드를 사용하세요.

옵션으로, 두 번째 인자에 비교 연산자를 전달할 수도 있습니다. 지원되는 연산자는 다음과 같습니다: '===', '!==', '!=', '==', '=', '<>', '>', '<', '>=', '<='

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

이 메서드는 [where](#method-where) 메서드와 동일한 시그니처를 갖지만, 모든 값을 "엄격하게(strict)" 비교하여 필터링합니다.

<a name="method-wherebetween"></a>
#### `whereBetween()`

`whereBetween` 메서드는 지정한 아이템 값이 주어진 범위 내에 속하는지를 판단해 컬렉션을 필터링합니다.

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

`whereIn` 메서드는 지정한 값 배열에 포함되지 않는 아이템을 컬렉션에서 제거합니다.

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

`whereIn` 메서드는 값 비교 시 "느스한(loose)" 비교를 사용합니다. 즉, 문자열로 된 값이 정수와 같은 값일 경우에도 일치한다고 간주합니다. 엄격한 비교를 원하면 [whereInStrict](#method-whereinstrict) 메서드를 사용하세요.

<a name="method-whereinstrict"></a>
#### `whereInStrict()`

이 메서드는 [whereIn](#method-wherein) 메서드와 동일한 시그니처를 갖지만, 모든 값을 "엄격하게(strict)" 비교하여 필터링합니다.

<a name="method-whereinstanceof"></a>
#### `whereInstanceOf()`

`whereInstanceOf` 메서드는 아이템이 특정 클래스의 인스턴스인지에 따라 컬렉션을 필터링합니다.

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

`whereNotBetween` 메서드는 지정한 값 범위 밖에 있는 아이템만 남도록 컬렉션을 필터링합니다.

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

`whereNotIn` 메서드는 지정한 값 배열에 속한 아이템을 컬렉션에서 제거합니다.

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

`whereNotIn` 메서드는 값 비교 시 "느스한(loose)" 비교를 사용합니다. 즉, 문자열로 된 값이 정수와 같은 값일 경우에도 일치한다고 간주합니다. 엄격한 비교를 원하면 [whereNotInStrict](#method-wherenotinstrict) 메서드를 사용하세요.

<a name="method-wherenotinstrict"></a>
#### `whereNotInStrict()`

이 메서드는 [whereNotIn](#method-wherenotin) 메서드와 동일한 시그니처를 갖지만, 모든 값을 "엄격하게(strict)" 비교하여 필터링합니다.

<a name="method-wherenotnull"></a>
#### `whereNotNull()`

`whereNotNull` 메서드는 지정한 키의 값이 `null`이 아닌 아이템만 반환합니다.

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

`whereNull` 메서드는 지정한 키의 값이 `null`인 아이템만 반환합니다.

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

정적 메서드인 `wrap`은 전달된 값을 컬렉션으로 감쌉니다.

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

`zip` 메서드는 원본 컬렉션과 주어진 배열의 같은 인덱스에 있는 값들을 병합합니다.

```php
$collection = collect(['Chair', 'Desk']);

$zipped = $collection->zip([100, 200]);

$zipped->all();

// [['Chair', 100], ['Desk', 200]]
```

<a name="higher-order-messages"></a>
## 하이어 오더 메시지(Higher Order Messages)

컬렉션은 "하이어 오더 메시지(higher order messages)"도 지원합니다. 이 기능을 사용하면 컬렉션에서 자주 사용하는 동작을 간편한 축약형으로 수행할 수 있습니다. 하이어 오더 메시지를 제공하는 메서드는 다음과 같습니다: [average](#method-average), [avg](#method-avg), [contains](#method-contains), [each](#method-each), [every](#method-every), [filter](#method-filter), [first](#method-first), [flatMap](#method-flatmap), [groupBy](#method-groupby), [keyBy](#method-keyby), [map](#method-map), [max](#method-max), [min](#method-min), [partition](#method-partition), [reject](#method-reject), [skipUntil](#method-skipuntil), [skipWhile](#method-skipwhile), [some](#method-some), [sortBy](#method-sortby), [sortByDesc](#method-sortbydesc), [sum](#method-sum), [takeUntil](#method-takeuntil), [takeWhile](#method-takewhile), [unique](#method-unique).

각 하이어 오더 메시지는 컬렉션 인스턴스의 동적 프로퍼티로 접근할 수 있습니다. 예를 들어, 컬렉션 내 모든 객체에서 메서드를 호출하려면 다음과 같이 `each` 하이어 오더 메시지를 사용할 수 있습니다.

```php
use App\Models\User;

$users = User::where('votes', '>', 500)->get();

$users->each->markAsVip();
```

마찬가지로, `sum` 하이어 오더 메시지를 활용해 사용자 컬렉션의 "votes" 합계를 가져올 수도 있습니다.

```php
$users = User::where('group', 'Development')->get();

return $users->sum->votes;
```

<a name="lazy-collections"></a>
## 레이지 컬렉션(Lazy Collections)

<a name="lazy-collection-introduction"></a>
### 소개

> [!WARNING]
> 라라벨의 레이지 컬렉션을 더 자세히 배우기 전에, 먼저 [PHP 제너레이터](https://www.php.net/manual/en/language.generators.overview.php)에 대해 익혀두는 것이 좋습니다.

이미 강력한 `Collection` 클래스에 더해, `LazyCollection` 클래스는 PHP의 [제너레이터(generators)](https://www.php.net/manual/en/language.generators.overview.php)를 활용하여 매우 큰 데이터셋도 메모리 사용량을 최소화하면서 다룰 수 있도록 해줍니다.

예를 들어, 애플리케이션에서 수 기가바이트에 이르는 로그 파일을 파싱해야 할 때, 라라벨의 컬렉션 메서드를 활용하고 싶다고 가정해보겠습니다. 파일 전체를 한 번에 메모리에 올리는 대신, 레이지 컬렉션을 사용하면 한 번에 파일의 일부분만 메모리에 남겨둘 수 있습니다.

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

또는, 10,000개의 Eloquent 모델을 순회해야 한다고 가정해봅시다. 기존의 라라벨 컬렉션을 사용하는 경우, 모든 10,000개 모델을 한 번에 메모리에 적재해야 합니다.

```php
use App\Models\User;

$users = User::all()->filter(function (User $user) {
    return $user->id > 500;
});
```

하지만 쿼리 빌더의 `cursor` 메서드는 `LazyCollection` 인스턴스를 반환합니다. 이를 사용하면 데이터베이스에는 한 번만 쿼리를 실행하면서, 동시에 한 번에 하나의 Eloquent 모델만 메모리에 올라가도록 할 수 있습니다. 이 예제에서 `filter` 콜백은 실제로 사용자를 하나씩 순회할 때에만 실행되어, 메모리 사용량을 크게 줄일 수 있습니다.

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

레이지 컬렉션 인스턴스를 생성하려면, PHP 제너레이터 함수를 컬렉션의 `make` 메서드에 전달하면 됩니다.

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
### Enumerable 컨트랙트

`Collection` 클래스에서 사용할 수 있는 거의 모든 메서드는 `LazyCollection` 클래스에서도 사용할 수 있습니다. 두 클래스 모두 `Illuminate\Support\Enumerable` 컨트랙트를 구현하며, 이 컨트랙트는 다음과 같은 메서드들을 정의합니다.

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
> 컬렉션을 직접 변경하는 메서드(예: `shift`, `pop`, `prepend` 등)는 `LazyCollection` 클래스에서 **지원되지 않습니다**.

<a name="lazy-collection-methods"></a>

### 지연 컬렉션 메서드

`Enumerable` 계약에서 정의된 메서드 외에도, `LazyCollection` 클래스는 다음과 같은 메서드를 제공합니다.

<a name="method-takeUntilTimeout"></a>
#### `takeUntilTimeout()`

`takeUntilTimeout` 메서드는 지정한 시간까지 값들을 나열(열거)하는 새로운 지연 컬렉션을 반환합니다. 해당 시간이 지나면 컬렉션의 나열이 중단됩니다.

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

이 메서드의 사용 예를 들어보면, 데이터베이스에서 커서로 송장(invoice)을 제출하는 애플리케이션이 있다고 가정해 보겠습니다. 15분마다 실행되는 [스케줄링된 작업](/docs/12.x/scheduling)을 정의하고, 최대 14분까지만 송장을 처리하도록 할 수 있습니다.

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

`each` 메서드는 컬렉션의 각 항목마다 즉시 주어진 콜백을 실행하지만, `tapEach` 메서드는 항목이 하나씩 리스트에서 꺼내질 때에만 콜백을 실행합니다.

```php
// 아직 아무것도 dump 되지 않았습니다...
$lazyCollection = LazyCollection::times(INF)->tapEach(function (int $value) {
    dump($value);
});

// 세 개의 항목이 dump 됩니다...
$array = $lazyCollection->take(3)->all();

// 1
// 2
// 3
```

<a name="method-throttle"></a>
#### `throttle()`

`throttle` 메서드는 지연 컬렉션의 각 값이 지정한 초(seconds)의 간격을 두고 반환되도록 조절해 줍니다. 이 방법은 요청 제한이 있는 외부 API와 상호작용해야 하는 경우 특히 유용합니다.

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

`remember` 메서드는 이미 나열된(열거된) 값들을 기억해서, 이후 컬렉션을 다시 통해 반복할 때 더 이상 그 값들을 다시 가져오지 않는 새로운 지연 컬렉션을 반환합니다.

```php
// 아직 쿼리가 실행되지 않았습니다...
$users = User::cursor()->remember();

// 쿼리가 실행됩니다...
// 처음 5명의 사용자가 데이터베이스에서 조회됩니다...
$users->take(5)->all();

// 처음 5명은 컬렉션의 캐시에서 가져오고,
// 그 이후 항목은 데이터베이스에서 조회됩니다...
$users->take(20)->all();
```