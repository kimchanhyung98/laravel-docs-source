# 컬렉션 (Collections)

- [소개](#introduction)
    - [컬렉션 생성하기](#creating-collections)
    - [컬렉션 확장하기](#extending-collections)
- [사용 가능한 메서드](#available-methods)
- [고차 메시지](#higher-order-messages)
- [지연 컬렉션 (Lazy Collections)](#lazy-collections)
    - [소개](#lazy-collection-introduction)
    - [지연 컬렉션 생성하기](#creating-lazy-collections)
    - [Enumerable 계약](#the-enumerable-contract)
    - [지연 컬렉션 메서드](#lazy-collection-methods)

<a name="introduction"></a>
## 소개 (Introduction)

`Illuminate\Support\Collection` 클래스는 배열 데이터를 다룰 때 유창하고 편리한 래퍼(wrapper)를 제공합니다. 예를 들어, 다음 코드를 확인하세요. `collect` 도우미 함수를 사용하여 배열을 컬렉션 인스턴스로 만들고, 각 요소에 `strtoupper` 함수를 적용한 후, 빈 값을 제거합니다:

```php
$collection = collect(['Taylor', 'Abigail', null])->map(function (?string $name) {
    return strtoupper($name);
})->reject(function (string $name) {
    return empty($name);
});
```

보시다시피 `Collection` 클래스는 메서드를 연쇄(chaining)하여 기반 배열에 대해 매핑과 축소 작업을 편리하게 수행할 수 있도록 합니다. 일반적으로 컬렉션은 불변(immutable)이며, 모든 `Collection` 메서드는 완전히 새로운 `Collection` 인스턴스를 반환합니다.

<a name="creating-collections"></a>
### 컬렉션 생성하기 (Creating Collections)

앞서 설명한 것처럼 `collect` 도우미 함수는 주어진 배열을 기반으로 새로운 `Illuminate\Support\Collection` 인스턴스를 반환합니다. 따라서 컬렉션 생성은 매우 간단합니다:

```php
$collection = collect([1, 2, 3]);
```

또한 [make](#method-make) 및 [fromJson](#method-fromjson) 메서드를 통해서도 컬렉션을 만들 수 있습니다.

> [!NOTE]
> [Eloquent](/docs/12.x/eloquent)의 쿼리 결과는 항상 `Collection` 인스턴스로 반환됩니다.

<a name="extending-collections"></a>
### 컬렉션 확장하기 (Extending Collections)

컬렉션은 "매크로(macroable)"를 지원하여 런타임 시 `Collection` 클래스에 추가 메서드를 붙일 수 있습니다. `Illuminate\Support\Collection` 클래스의 `macro` 메서드는 매크로가 호출될 때 실행될 클로저를 받습니다. 매크로 클로저는 컬렉션 클래스의 실제 메서드처럼 `$this`를 통해 컬렉션의 다른 메서드에 접근할 수 있습니다. 예를 들어, 다음은 `Collection` 클래스에 `toUpper` 메서드를 추가하는 코드입니다:

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

일반적으로 컬렉션 매크로는 [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드 안에 선언하는 것이 좋습니다.

<a name="macro-arguments"></a>
#### 매크로 인수 (Macro Arguments)

필요하면 추가 인수를 받는 매크로도 정의할 수 있습니다:

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

남은 컬렉션 문서에서는 `Collection` 클래스에서 사용할 수 있는 각각의 메서드를 설명합니다. 모든 메서드는 메서드 체이닝이 가능하여 기반 배열을 유창하게 다룰 수 있습니다. 또한 거의 모든 메서드는 새로운 `Collection` 인스턴스를 반환하므로 필요할 경우 원본 컬렉션을 보존할 수 있습니다.

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
## 메서드 목록 (Method Listing)

<a name="method-after"></a>
#### `after()`

`after` 메서드는 주어진 항목 뒤에 오는 항목을 반환합니다. 주어진 항목이 없거나 마지막 항목일 경우 `null`을 반환합니다:

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->after(3);

// 4

$collection->after(5);

// null
```

이 함수는 "느슨한(loose)" 비교를 사용해 값을 검색합니다. 즉, 정수 값을 가진 문자열도 동일한 정수 값과 같다고 간주합니다. "엄격한(strict)" 비교를 사용하려면 `strict` 인수를 지정하면 됩니다:

```php
collect([2, 4, 6, 8])->after('4', strict: true);

// null
```

또는 자신의 클로저를 제공하여 해당 조건을 만족하는 첫 번째 항목을 찾을 수도 있습니다:

```php
collect([2, 4, 6, 8])->after(function (int $item, int $key) {
    return $item > 5;
});

// 8
```

<a name="method-all"></a>
#### `all()`

`all` 메서드는 컬렉션이 표현하는 내부 배열을 반환합니다:

```php
collect([1, 2, 3])->all();

// [1, 2, 3]
```

<a name="method-average"></a>
#### `average()`

`avg` 메서드의 별칭입니다.

<a name="method-avg"></a>
#### `avg()`

주어진 키에 대한 [평균값](https://en.wikipedia.org/wiki/Average)을 반환합니다:

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

`before` 메서드는 `after` 메서드와 반대로, 주어진 항목 바로 전의 항목을 반환합니다. 주어진 항목이 없거나 처음 항목이면 `null`을 반환합니다:

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

`chunk` 메서드는 컬렉션을 지정한 크기의 작은 컬렉션들로 나눕니다:

```php
$collection = collect([1, 2, 3, 4, 5, 6, 7]);

$chunks = $collection->chunk(4);

$chunks->all();

// [[1, 2, 3, 4], [5, 6, 7]]
```

이 메서드는 [뷰](/docs/12.x/views)에서 [Bootstrap](https://getbootstrap.com/docs/5.3/layout/grid/) 같은 그리드 시스템을 사용할 때 편리합니다. 예를 들어, 그리드에 표시할 [Eloquent](/docs/12.x/eloquent) 모델 컬렉션이 있다면:

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

`chunkWhile` 메서드는 주어진 콜백 조건으로 평가할 때 참인 동안 컬렉션을 더 작은 여러 컬렉션으로 나눕니다. 클로저의 `$chunk` 변수로 이전 요소를 검사할 수 있습니다:

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

`collapse` 메서드는 배열 또는 컬렉션들의 컬렉션을 단일 평면 컬렉션으로 합칩니다:

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

`collapseWithKeys` 메서드는 배열 또는 컬렉션의 컬렉션을 평평하게 합치며 원본 키를 그대로 유지합니다. 컬렉션이 이미 평면이라면 빈 컬렉션을 반환합니다:

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

현재 컬렉션 항목들을 갖는 새 `Collection` 인스턴스를 반환합니다:

```php
$collectionA = collect([1, 2, 3]);

$collectionB = $collectionA->collect();

$collectionB->all();

// [1, 2, 3]
```

`collect` 메서드는 주로 [지연 컬렉션](#lazy-collections)을 표준 `Collection` 인스턴스로 변환할 때 유용합니다:

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
> `collect` 메서드는 `Enumerable` 계약의 일부로, `Enumerable` 인스턴스가 있을 때 표준 `Collection` 인스턴스를 안전하게 얻을 수 있습니다.

<a name="method-combine"></a>
#### `combine()`

컬렉션의 값을 키로, 다른 배열 또는 컬렉션의 값을 값으로 하여 결합합니다:

```php
$collection = collect(['name', 'age']);

$combined = $collection->combine(['George', 29]);

$combined->all();

// ['name' => 'George', 'age' => 29]
```

<a name="method-concat"></a>
#### `concat()`

주어진 배열 또는 컬렉션 값을 다른 컬렉션 뒤에 추가합니다:

```php
$collection = collect(['John Doe']);

$concatenated = $collection->concat(['Jane Doe'])->concat(['name' => 'Johnny Doe']);

$concatenated->all();

// ['John Doe', 'Jane Doe', 'Johnny Doe']
```

`concat`는 숫자 키만 재인덱싱합니다. 키를 유지하려면 [merge](#method-merge) 메서드를 이용하세요.

<a name="method-contains"></a>
#### `contains()`

컬렉션에 주어진 값이 포함되어 있는지 확인합니다. 클로저를 전달하여 조건에 맞는 요소가 있는지 검사할 수 있습니다:

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->contains(function (int $value, int $key) {
    return $value > 5;
});

// false
```

문자열로 값을 확인할 수도 있습니다:

```php
$collection = collect(['name' => 'Desk', 'price' => 100]);

$collection->contains('Desk');

// true

$collection->contains('New York');

// false
```

키/값 쌍을 전달해 해당 쌍이 존재하는지 확인할 수도 있습니다:

```php
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
]);

$collection->contains('product', 'Bookcase');

// false
```

`contains`는 느슨한 비교(loose comparison)를 사용합니다. 엄격하게 비교하려면 [containsStrict](#method-containsstrict) 메서드를 사용하세요.

반대되는 메서드는 [doesntContain](#method-doesntcontain)입니다.

<a name="method-containsoneitem"></a>
#### `containsOneItem()`

컬렉션에 단일 항목이 포함되어 있는지 확인합니다:

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

`contains`와 동일한 함수지만 모든 값을 "엄격한(strict)" 비교로 검사합니다.

> [!NOTE]
> 이 메서드는 [Eloquent Collections](/docs/12.x/eloquent-collections#method-contains) 사용 시 동작이 다릅니다.

<a name="method-count"></a>
#### `count()`

컬렉션에 포함된 항목 개수를 반환합니다:

```php
$collection = collect([1, 2, 3, 4]);

$collection->count();

// 4
```

<a name="method-countBy"></a>
#### `countBy()`

컬렉션 내 값의 출현 횟수를 센 후 각각 카운트를 반환합니다. 클로저로 커스터마이징도 가능합니다:

```php
$collection = collect([1, 2, 2, 2, 3]);

$counted = $collection->countBy();

$counted->all();

// [1 => 1, 2 => 3, 3 => 1]
```

클로저 사용 예:

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

여러 배열 또는 컬렉션과 카르테시안 곱을 계산하여 가능한 모든 조합을 반환합니다:

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
```

복수 배열 인자 예:

```php
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

컬렉션 항목을 덤프(dump)하고 스크립트 실행을 종료합니다:

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

스크립트를 계속 실행하려면 [dump](#method-dump)를 사용하세요.

<a name="method-diff"></a>
#### `diff()`

주어진 배열 또는 컬렉션과 비교해서 원본 컬렉션에만 있는 값을 반환합니다:

```php
$collection = collect([1, 2, 3, 4, 5]);

$diff = $collection->diff([2, 4, 6, 8]);

$diff->all();

// [1, 3, 5]
```

> [!NOTE]
> [Eloquent Collections](/docs/12.x/eloquent-collections#method-diff) 사용 시 동작이 다릅니다.

<a name="method-diffassoc"></a>
#### `diffAssoc()`

키와 값 모두를 비교하여 원본 컬렉션에만 있는 키/값 쌍을 반환합니다:

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

`diffAssoc`와 유사하지만, 사용자 제공 콜백 함수로 키 비교를 수행합니다:

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

콜백 함수는 비교 함수여야 하며, PHP 내장 함수 [array_diff_uassoc](https://www.php.net/array_diff_uassoc#refsect1-function.array-diff-uassoc-parameters)와 연동됩니다.

<a name="method-diffkeys"></a>
#### `diffKeys()`

키만을 기준으로 비교하여 원본 컬렉션에만 있는 키/값 쌍을 반환합니다:

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

컬렉션에 주어진 값이 포함되어 있지 않은지 확인합니다. `contains` 메서드와 같이 클로저, 값, 키/값 쌍을 인수로 받습니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->doesntContain(function (int $value, int $key) {
    return $value < 5;
});

// false
```

값 인수 예:

```php
$collection = collect(['name' => 'Desk', 'price' => 100]);

$collection->doesntContain('Table');

// true
```

키/값 쌍 예:

```php
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
]);

$collection->doesntContain('product', 'Bookcase');

// true
```

느슨한 비교(loose comparison)를 사용합니다.

<a name="method-dot"></a>
#### `dot()`

다차원 컬렉션을 “dot” 표기법을 키로 하는 단일 차원 컬렉션으로 평탄화합니다:

```php
$collection = collect(['products' => ['desk' => ['price' => 100]]]);

$flattened = $collection->dot();

$flattened->all();

// ['products.desk.price' => 100]
```

<a name="method-dump"></a>
#### `dump()`

컬렉션 항목을 덤프합니다:

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

덤프 후 스크립트를 멈추고 싶다면 [dd](#method-dd) 메서드를 사용하세요.

<a name="method-duplicates"></a>
#### `duplicates()`

중복된 값을 찾아 반환합니다:

```php
$collection = collect(['a', 'b', 'a', 'c', 'b']);

$collection->duplicates();

// [2 => 'a', 4 => 'b']
```

배열이나 객체가 포함된 경우, 중복 검사에 사용할 키를 전달할 수 있습니다:

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

`duplicates`와 동일한 시그니처를 가지나, 모든 값은 엄격한 비교로 검사합니다.

<a name="method-each"></a>
#### `each()`

컬렉션의 각 항목을 순회하며 클로저에 전달합니다:

```php
$collection = collect([1, 2, 3, 4]);

$collection->each(function (int $item, int $key) {
    // ...
});
```

클로저에서 `false`를 반환하면 반복을 중지할 수 있습니다:

```php
$collection->each(function (int $item, int $key) {
    if (/* condition */) {
        return false;
    }
});
```

<a name="method-eachspread"></a>
#### `eachSpread()`

중첩된 배열 값들을 분해하여 클로저에 전달합니다:

```php
$collection = collect([['John Doe', 35], ['Jane Doe', 33]]);

$collection->eachSpread(function (string $name, int $age) {
    // ...
});
```

반복 중단도 가능합니다:

```php
$collection->eachSpread(function (string $name, int $age) {
    return false;
});
```

<a name="method-ensure"></a>
#### `ensure()`

컬렉션 요소가 지정한 타입 또는 타입 리스트에 모두 해당하는지 검증합니다. 아니라면 `UnexpectedValueException` 예외가 발생합니다:

```php
return $collection->ensure(User::class);

return $collection->ensure([User::class, Customer::class]);
```

PHP 기본 자료형도 지정할 수 있습니다:

```php
return $collection->ensure('int');
```

> [!WARNING]
> `ensure` 메서드는 컬렉션에 나중에 다른 타입 요소가 추가되는 것을 막지 않습니다.

<a name="method-every"></a>
#### `every()`

모든 컬렉션 요소가 주어진 조건을 만족하는지 확인합니다:

```php
collect([1, 2, 3, 4])->every(function (int $value, int $key) {
    return $value > 2;
});

// false
```

빈 컬렉션에 대해서는 `true`를 반환합니다:

```php
$collection = collect([]);

$collection->every(function (int $value, int $key) {
    return $value > 2;
});

// true
```

<a name="method-except"></a>
#### `except()`

지정된 키를 제외한 모든 항목을 포함하는 새 컬렉션을 반환합니다:

```php
$collection = collect(['product_id' => 1, 'price' => 100, 'discount' => false]);

$filtered = $collection->except(['price', 'discount']);

$filtered->all();

// ['product_id' => 1]
```

반대되는 메서드는 [only](#method-only)입니다.

> [!NOTE]
> [Eloquent Collections](/docs/12.x/eloquent-collections#method-except)에서는 동작이 다릅니다.

<a name="method-filter"></a>
#### `filter()`

주어진 콜백을 통과하는 항목만 남깁니다:

```php
$collection = collect([1, 2, 3, 4]);

$filtered = $collection->filter(function (int $value, int $key) {
    return $value > 2;
});

$filtered->all();

// [3, 4]
```

콜백을 주지 않으면 `false`로 평가되는 값들을 제거합니다:

```php
$collection = collect([1, 2, 3, null, false, '', 0, []]);

$collection->filter()->all();

// [1, 2, 3]
```

반대되는 메서드는 [reject](#method-reject)입니다.

<a name="method-first"></a>
#### `first()`

주어진 조건에 부합하는 첫 번째 항목을 반환합니다:

```php
collect([1, 2, 3, 4])->first(function (int $value, int $key) {
    return $value > 2;
});

// 3
```

인수가 없으면 단순히 첫 번째 항목을 반환합니다. 컬렉션이 비어 있으면 `null`을 반환합니다:

```php
collect([1, 2, 3, 4])->first();

// 1
```

<a name="method-first-or-fail"></a>
#### `firstOrFail()`

`first`와 같으나 결과가 없으면 `Illuminate\Support\ItemNotFoundException` 예외를 던집니다:

```php
collect([1, 2, 3, 4])->firstOrFail(function (int $value, int $key) {
    return $value > 5;
});

// ItemNotFoundException 발생
```

인수 없이 호출하면 빈 컬렉션일 때도 예외가 발생합니다:

```php
collect([])->firstOrFail();

// ItemNotFoundException 발생
```

<a name="method-first-where"></a>
#### `firstWhere()`

지정한 키 / 값 쌍에 부합하는 첫 번째 요소를 반환합니다:

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

비교 연산자를 함께 전달할 수도 있습니다:

```php
$collection->firstWhere('age', '>=', 18);

// ['name' => 'Diego', 'age' => 23]
```

키만 전달할 경우 해당 키 값이 "참"이면 반환합니다:

```php
$collection->firstWhere('age');

// ['name' => 'Linda', 'age' => 14]
```

---  

이후 메서드 설명은 원 문서의 형식과 내용대로 계속됩니다. 필요 시 추가 요청하시면 해당 부분도 이어서 번역해 드리겠습니다.