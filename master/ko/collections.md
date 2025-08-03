# 컬렉션 (Collections)

- [소개](#introduction)
    - [컬렉션 생성하기](#creating-collections)
    - [컬렉션 확장하기](#extending-collections)
- [사용 가능한 메서드](#available-methods)
- [고차 메시지](#higher-order-messages)
- [지연 컬렉션(Lazy Collections)](#lazy-collections)
    - [소개](#lazy-collection-introduction)
    - [지연 컬렉션 생성하기](#creating-lazy-collections)
    - [Enumerable 계약](#the-enumerable-contract)
    - [지연 컬렉션 메서드](#lazy-collection-methods)

<a name="introduction"></a>
## 소개

`Illuminate\Support\Collection` 클래스는 배열 데이터를 다룰 때 유창하고 편리한 래퍼(wrapper)를 제공합니다. 예를 들어, 다음 코드를 살펴보세요. `collect` 헬퍼를 사용해서 배열로부터 새로운 컬렉션 인스턴스를 만들고, 각 요소에 `strtoupper` 함수를 적용한 후, 빈 요소들을 제거합니다:

```php
$collection = collect(['taylor', 'abigail', null])->map(function (?string $name) {
    return strtoupper($name);
})->reject(function (string $name) {
    return empty($name);
});
```

보시다시피 `Collection` 클래스는 메서드 체인을 통해 기본 배열에 대해 유창한 매핑(mapping)과 축소(reducing)를 수행할 수 있게 합니다. 일반적으로, 컬렉션은 불변(immutable)입니다. 즉, 모든 `Collection` 메서드는 완전히 새로운 `Collection` 인스턴스를 반환합니다.

<a name="creating-collections"></a>
### 컬렉션 생성하기

위에서 언급했듯이, `collect` 헬퍼는 주어진 배열로 새로운 `Illuminate\Support\Collection` 인스턴스를 반환합니다. 따라서 컬렉션을 생성하는 것은 매우 간단합니다:

```php
$collection = collect([1, 2, 3]);
```

> [!NOTE]
> [Eloquent](/docs/master/eloquent) 쿼리 결과는 항상 `Collection` 인스턴스로 반환됩니다.

<a name="extending-collections"></a>
### 컬렉션 확장하기

컬렉션은 "macroable" 하여, 런타임에 `Collection` 클래스에 추가적인 메서드를 덧붙일 수 있습니다. `Illuminate\Support\Collection` 클래스의 `macro` 메서드는 매크로가 호출될 때 실행될 클로저를 받습니다. 이 매크로 클로저는 클래스 내 다른 메서드들을 `$this`를 통해 사용할 수 있어서 마치 컬렉션 클래스의 실제 메서드처럼 동작합니다. 예를 들어, 아래 코드는 `Collection` 클래스에 `toUpper` 메서드를 추가합니다:

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

일반적으로 컬렉션 매크로는 [서비스 프로바이더](/docs/master/providers)의 `boot` 메서드 내에서 선언하는 것이 좋습니다.

<a name="macro-arguments"></a>
#### 매크로 인수

필요하다면, 추가 인수를 받는 매크로를 정의할 수도 있습니다:

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

앞으로 남은 컬렉션 문서 대부분에서는 `Collection` 클래스에서 사용 가능한 각 메서드를 설명합니다. 이 메서드들은 모두 체이닝이 가능하여 기본 배열을 유창하게 조작할 수 있습니다. 게다가 거의 모든 메서드는 새로운 `Collection` 인스턴스를 반환하여, 필요할 때 원본 컬렉션을 보존할 수 있습니다.

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

`after` 메서드는 지정한 항목 다음에 오는 항목을 반환합니다. 주어진 항목이 없거나 마지막 항목일 경우 `null`을 반환합니다:

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->after(3);

// 4

$collection->after(5);

// null
```

이 메서드는 "느슨한(loose)" 비교를 사용하여 주어진 항목을 찾습니다. 즉, 정수 값이 문자열에 있어도 값이 같으면 동일하다고 판단합니다. "엄격한(strict)" 비교를 사용하려면 `strict` 인수를 전달하세요:

```php
collect([2, 4, 6, 8])->after('4', strict: true);

// null
```

또는 주어진 진리 검사(조건)를 통과하는 첫 번째 항목을 찾기 위해 사용자 정의 클로저를 넘길 수도 있습니다:

```php
collect([2, 4, 6, 8])->after(function (int $item, int $key) {
    return $item > 5;
});

// 8
```

<a name="method-all"></a>
#### `all()`

`all` 메서드는 컬렉션이 보유한 기본 배열을 반환합니다:

```php
collect([1, 2, 3])->all();

// [1, 2, 3]
```

<a name="method-average"></a>
#### `average()`

`avg` 메서드의 별칭(alias)입니다.

<a name="method-avg"></a>
#### `avg()`

`avg` 메서드는 특정 키에 대한 [평균값](https://en.wikipedia.org/wiki/Average)을 반환합니다:

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

`before` 메서드는 `after` 메서드의 반대입니다. 지정한 항목 이전에 오는 항목을 반환합니다. 해당 항목이 없거나 첫 번째 항목일 경우 `null`을 반환합니다:

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

`chunk` 메서드는 컬렉션을 주어진 크기의 작은 컬렉션 여러 개로 나눕니다:

```php
$collection = collect([1, 2, 3, 4, 5, 6, 7]);

$chunks = $collection->chunk(4);

$chunks->all();

// [[1, 2, 3, 4], [5, 6, 7]]
```

뷰(view)에서 [Bootstrap](https://getbootstrap.com/docs/5.3/layout/grid/) 같은 그리드 시스템을 사용할 때 매우 유용합니다. 예를 들어, 그리드에 표시할 Eloquent 모델 컬렉션이 있다고 가정하면:

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

`chunkWhile` 메서드는 주어진 콜백의 평가에 따라 컬렉션을 여러 개의 작은 컬렉션으로 나눕니다. 클로저로 전달되는 `$chunk` 변수로 이전 요소를 검사할 수 있습니다:

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

`collapse` 메서드는 배열들의 컬렉션을 단일 평탄(1차원) 컬렉션으로 만듭니다:

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

`collapseWithKeys` 메서드는 배열 또는 컬렉션의 컬렉션을 키를 유지하면서 단일 컬렉션으로 평탄화합니다:

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

`collect` 메서드는 현재 컬렉션의 아이템들로 새 `Collection` 인스턴스를 반환합니다:

```php
$collectionA = collect([1, 2, 3]);

$collectionB = $collectionA->collect();

$collectionB->all();

// [1, 2, 3]
```

`collect` 메서드는 주로 [지연 컬렉션](#lazy-collections)을 표준 `Collection` 인스턴스로 변환하는 데 유용합니다:

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
> `collect` 메서드는 `Enumerable` 인스턴스를 비지연(non-lazy) 컬렉션 인스턴스로 얻을 때 특히 유용합니다. `collect()`는 `Enumerable` 계약의 일부이므로 안전하게 사용할 수 있습니다.

<a name="method-combine"></a>
#### `combine()`

`combine` 메서드는 컬렉션의 값을 키로, 다른 배열 또는 컬렉션의 값을 값으로 조합하여 새로운 컬렉션을 반환합니다:

```php
$collection = collect(['name', 'age']);

$combined = $collection->combine(['George', 29]);

$combined->all();

// ['name' => 'George', 'age' => 29]
```

<a name="method-concat"></a>
#### `concat()`

`concat` 메서드는 주어진 배열 또는 컬렉션의 값을 기존 컬렉션 끝에 덧붙입니다:

```php
$collection = collect(['John Doe']);

$concatenated = $collection->concat(['Jane Doe'])->concat(['name' => 'Johnny Doe']);

$concatenated->all();

// ['John Doe', 'Jane Doe', 'Johnny Doe']
```

`concat` 메서드는 붙이는 항목의 키를 숫자 인덱스 기준으로 다시 매깁니다. 키를 유지해야 할 경우 [merge](#method-merge) 메서드를 사용하세요.

<a name="method-contains"></a>
#### `contains()`

`contains` 메서드는 컬렉션에 특정 항목이 포함되어 있는지 확인합니다. 주어진 인수는 다음과 같이 다양하게 활용할 수 있습니다.

- 클로저로 진리 검사하여 조건에 맞는 원소가 있는지 확인:

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->contains(function (int $value, int $key) {
    return $value > 5;
});

// false
```

- 단일 값이 컬렉션에 존재하는지 확인:

```php
$collection = collect(['name' => 'Desk', 'price' => 100]);

$collection->contains('Desk');

// true

$collection->contains('New York');

// false
```

- 키와 값 쌍으로 존재 여부 확인:

```php
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
]);

$collection->contains('product', 'Bookcase');

// false
```

`contains`는 "느슨한" 비교를 사용합니다. 즉, 정수 값을 가진 문자열이 같은 정수와 동일하다고 판단합니다. "엄격한" 비교가 필요한 경우 [`containsStrict`](#method-containsstrict) 메서드를 사용하세요.

`contains`의 반대 기능은 [doesntContain](#method-doesntcontain) 메서드를 참고하세요.

<a name="method-containsoneitem"></a>
#### `containsOneItem()`

`containsOneItem` 메서드는 컬렉션에 항목이 단 하나만 존재하는지 확인합니다:

```php
collect([])->containsOneItem();

// false

collect(['1'])->containsOneItem();

// true

collect(['1', '2'])->containsOneItem();

// false
```

<a name="method-containsstrict"></a>
#### `containsStrict()`

시그니처는 `contains` 메서드와 동일하지만 모든 값 비교를 "엄격한" 비교 방식으로 수행합니다.

> [!NOTE]
> 이 메서드 동작은 [Eloquent Collections](/docs/master/eloquent-collections#method-contains) 사용 시 다를 수 있습니다.

<a name="method-count"></a>
#### `count()`

`count` 메서드는 컬렉션 내 항목 총 개수를 반환합니다:

```php
$collection = collect([1, 2, 3, 4]);

$collection->count();

// 4
```

<a name="method-countBy"></a>
#### `countBy()`

`countBy` 메서드는 컬렉션 내 값의 발생 횟수를 셉니다. 기본적으로 모든 요소의 발생 횟수를 세며, 클로저를 전달해 특정 "분류"별 개수를 셀 수도 있습니다:

```php
$collection = collect([1, 2, 2, 2, 3]);

$counted = $collection->countBy();

$counted->all();

// [1 => 1, 2 => 3, 3 => 1]
```

클로저를 사용해 카운트할 값을 커스텀 지정할 수도 있습니다:

```php
$collection = collect(['alice@gmail.com', 'bob@yahoo.com', 'carlos@gmail.com']);

$counted = $collection->countBy(function (string $email) {
    return substr(strrchr($email, "@"), 1);
});

$counted->all();

// ['gmail.com' => 2, 'yahoo.com' => 1]
```

<a name="method-crossjoin"></a>
#### `crossJoin()`

`crossJoin` 메서드는 주어진 배열 또는 컬렉션들과 카르테시안 곱(Cartesian product)을 생성하여, 가능한 모든 조합의 배열을 반환합니다:

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

`dd` 메서드는 컬렉션의 아이템을 덤프하고 스크립트 실행을 종료합니다:

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

스크립트 실행을 멈추지 않으려면 [`dump`](#method-dump) 메서드를 사용하세요.

<a name="method-diff"></a>
#### `diff()`

`diff` 메서드는 컬렉션과 다른 컬렉션 또는 PHP 배열을 값 기준으로 비교해, 주어진 컬렉션에 없는 원래 컬렉션의 값을 반환합니다:

```php
$collection = collect([1, 2, 3, 4, 5]);

$diff = $collection->diff([2, 4, 6, 8]);

$diff->all();

// [1, 3, 5]
```

> [!NOTE]
> 이 메서드는 [Eloquent Collections](/docs/master/eloquent-collections#method-diff) 사용 시 동작이 달라질 수 있습니다.

<a name="method-diffassoc"></a>
#### `diffAssoc()`

`diffAssoc` 메서드는 키와 값 모두를 기준으로 비교해, 주어진 컬렉션에 없는 키-값 쌍을 반환합니다:

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

`diffAssocUsing` 메서드는 사용자 정의 비교 콜백 함수를 받아 키 비교에 활용합니다:

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

콜백은 0보다 작은, 같은, 큰 정수를 반환하는 비교 함수여야 합니다. 자세한 내용은 PHP 문서의 [`array_diff_uassoc`](https://www.php.net/array_diff_uassoc#refsect1-function.array-diff-uassoc-parameters) 참고.

<a name="method-diffkeys"></a>
#### `diffKeys()`

`diffKeys` 메서드는 키를 기준으로만 두 컬렉션을 비교해, 주어진 컬렉션에 없는 키-값 쌍을 반환합니다:

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

`doesntContain` 메서드는 컬렉션이 특정 항목을 포함하지 않는지 판단합니다. 사용 방식은 `contains` 메서드와 유사하지만 결과가 반대입니다:

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->doesntContain(function (int $value, int $key) {
    return $value < 5;
});

// false
```

또한 값이나 키-값 쌍으로도 확인할 수 있으며, 비교는 기본적으로 느슨한(loose) 비교입니다.

<a name="method-dot"></a>
#### `dot()`

`dot` 메서드는 다중 차원 컬렉션을 단일 차원 컬렉션으로 평탄화(flatten)하는데, 키 이름을 "점(dot)" 표기법으로 표현합니다:

```php
$collection = collect(['products' => ['desk' => ['price' => 100]]]);

$flattened = $collection->dot();

$flattened->all();

// ['products.desk.price' => 100]
```

<a name="method-dump"></a>
#### `dump()`

`dump` 메서드는 컬렉션 아이템을 덤프합니다:

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

명령 실행을 중단하려면 [`dd`](#method-dd) 메서드를 사용하세요.

<a name="method-duplicates"></a>
#### `duplicates()`

`duplicates` 메서드는 컬렉션 내 중복된 값을 찾아 반환합니다:

```php
$collection = collect(['a', 'b', 'a', 'c', 'b']);

$collection->duplicates();

// [2 => 'a', 4 => 'b']
```

배열이나 객체가 포함된 경우 중복 검사에 사용할 속성 키를 지정할 수 있습니다:

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

시그니처는 `duplicates`와 같으나 "엄격한" 비교를 수행합니다.

<a name="method-each"></a>
#### `each()`

`each` 메서드는 컬렉션의 각 아이템을 순회하며 콜백에 전달합니다:

```php
$collection = collect([1, 2, 3, 4]);

$collection->each(function (int $item, int $key) {
    // ...
});
```

`false` 를 반환하면 순회가 중단됩니다:

```php
$collection->each(function (int $item, int $key) {
    if (/* 조건 */) {
        return false;
    }
});
```

<a name="method-eachspread"></a>
#### `eachSpread()`

`eachSpread`는 중첩된 항목의 값들을 각각 콜백 인자로 넘겨 순회합니다:

```php
$collection = collect([['John Doe', 35], ['Jane Doe', 33]]);

$collection->eachSpread(function (string $name, int $age) {
    // ...
});
```

`false` 반환 시 순회 종료:

```php
$collection->eachSpread(function (string $name, int $age) {
    return false;
});
```

<a name="method-ensure"></a>
#### `ensure()`

`ensure` 메서드는 컬렉션의 모든 요소가 특정 타입(또는 타입 목록)인지 확인합니다. 그렇지 않으면 `UnexpectedValueException` 예외를 던집니다:

```php
return $collection->ensure(User::class);

return $collection->ensure([User::class, Customer::class]);
```

`string`, `int`, `float`, `bool`, `array` 같은 원시 타입도 지정할 수 있습니다:

```php
return $collection->ensure('int');
```

> [!WARNING]
> `ensure`는 이후에 다른 타입의 요소가 컬렉션에 추가되지 않음을 보장하지 않습니다.

<a name="method-every"></a>
#### `every()`

`every` 메서드는 컬렉션의 모든 요소가 주어진 검사 조건을 통과하는지 확인합니다:

```php
collect([1, 2, 3, 4])->every(function (int $value, int $key) {
    return $value > 2;
});

// false
```

빈 컬렉션의 경우 항상 `true`를 반환합니다:

```php
$collection = collect([]);

$collection->every(function (int $value, int $key) {
    return $value > 2;
});

// true
```

<a name="method-except"></a>
#### `except()`

`except` 메서드는 지정된 키들을 제외한 모든 항목을 반환합니다:

```php
$collection = collect(['product_id' => 1, 'price' => 100, 'discount' => false]);

$filtered = $collection->except(['price', 'discount']);

$filtered->all();

// ['product_id' => 1]
```

`except`의 반대는 [only](#method-only) 메서드입니다.

> [!NOTE]
> 이 메서드는 [Eloquent Collections](/docs/master/eloquent-collections#method-except) 사용 시 동작이 다릅니다.

<a name="method-filter"></a>
#### `filter()`

`filter` 메서드는 주어진 콜백을 통해 컬렉션을 필터링하며, 조건에 통과한 항목만 유지합니다:

```php
$collection = collect([1, 2, 3, 4]);

$filtered = $collection->filter(function (int $value, int $key) {
    return $value > 2;
});

$filtered->all();

// [3, 4]
```

콜백이 없으면 "거짓"으로 취급되는 항목들이 모두 제거됩니다:

```php
$collection = collect([1, 2, 3, null, false, '', 0, []]);

$collection->filter()->all();

// [1, 2, 3]
```

`filter`의 반대는 [reject](#method-reject) 메서드입니다.

<a name="method-first"></a>
#### `first()`

`first` 메서드는 주어진 검사 조건을 충족하는 컬렉션의 첫 번째 요소를 반환합니다:

```php
collect([1, 2, 3, 4])->first(function (int $value, int $key) {
    return $value > 2;
});

// 3
```

인수 없이 호출 시 첫 번째 요소를 반환하며, 컬렉션이 비어 있으면 `null`을 반환합니다:

```php
collect([1, 2, 3, 4])->first();

// 1
```

<a name="method-first-or-fail"></a>
#### `firstOrFail()`

`firstOrFail`은 `first` 메서드와 동일하지만, 조건에 맞는 요소가 없으면 `Illuminate\Support\ItemNotFoundException` 예외를 던집니다:

```php
collect([1, 2, 3, 4])->firstOrFail(function (int $value, int $key) {
    return $value > 5;
});

// ItemNotFoundException 예외 발생
```

인수 없이 호출 시 컬렉션이 비어 있으면 역시 예외가 발생합니다.

<a name="method-first-where"></a>
#### `firstWhere()`

`firstWhere` 메서드는 지정한 키-값 쌍에 맞는 첫 번째 요소를 반환합니다:

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

비교 연산자를 인수로 전달할 수도 있습니다:

```php
$collection->firstWhere('age', '>=', 18);

// ['name' => 'Diego', 'age' => 23]
```

키 하나만 전달하면, 해당 키 값이 참(truthy)인 첫 번째 요소를 반환합니다:

```php
$collection->firstWhere('age');

// ['name' => 'Linda', 'age' => 14]
```

<a name="method-flatmap"></a>
#### `flatMap()`

`flatMap` 메서드는 각 항목에 클로저를 적용하여 반환 결과를 취합 후, 한 단계 평탄화하여 새 컬렉션을 만듭니다:

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

`flatten` 메서드는 다중 차원 컬렉션을 단일 차원으로 평탄화합니다:

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

원한다면 평탄화 깊이(depth)를 지정할 수 있습니다:

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

깊이 인자를 주지 않으면 모든 하위 배열도 평탄화하여 `['iPhone 6S', 'Apple', 'Galaxy S7', 'Samsung']`처럼 됩니다.

<a name="method-flip"></a>
#### `flip()`

`flip` 메서드는 컬렉션의 키와 값을 서로 뒤바꿉니다:

```php
$collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

$flipped = $collection->flip();

$flipped->all();

// ['taylor' => 'name', 'laravel' => 'framework']
```

<a name="method-forget"></a>
#### `forget()`

`forget` 메서드는 키를 지정해 해당 항목을 컬렉션에서 제거합니다:

```php
$collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

// 단일 키 제거
$collection->forget('name');

// ['framework' => 'laravel']

// 여러 키 제거
$collection->forget(['name', 'framework']);

// []
```

> [!WARNING]
> `forget`은 다른 컬렉션 메서드와 다르게 새로운 컬렉션을 반환하지 않고, 호출된 컬렉션을 변경한 후 반환합니다.

<a name="method-forpage"></a>
#### `forPage()`

`forPage` 메서드는 특정 페이지 번호와 페이지당 아이템 수를 받아 해당 페이지에 속하는 아이템들을 새 컬렉션으로 반환합니다:

```php
$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9]);

$chunk = $collection->forPage(2, 3);

$chunk->all();

// [4, 5, 6]
```

<a name="method-get"></a>
#### `get()`

`get` 메서드는 주어진 키에 해당하는 아이템을 반환합니다. 키가 없으면 `null`을 반환합니다:

```php
$collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

$value = $collection->get('name');

// taylor
```

두 번째 인수로 기본값을 지정할 수 있습니다:

```php
$value = $collection->get('age', 34);

// 34
```

기본값으로 콜백을 줄 수도 있으며, 해당 키가 없으면 콜백 반환값이 반환됩니다:

```php
$collection->get('email', function () {
    return 'taylor@example.com';
});

// taylor@example.com
```

<a name="method-groupby"></a>
#### `groupBy()`

`groupBy` 메서드는 지정한 키 또는 콜백 함수에 따라 컬렉션 아이템을 그룹화합니다:

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

키 대신 콜백 함수를 전달할 수도 있습니다:

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

키 배열을 통해 다중 기준 그룹화를 할 수 있으며, 각 레벨에 순서대로 적용됩니다:

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

`has` 메서드는 컬렉션에 특정 키가 존재하는지 확인합니다:

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

`hasAny` 메서드는 주어진 키들 중 적어도 하나가 컬렉션에 존재하는지 확인합니다:

```php
$collection = collect(['account_id' => 1, 'product' => 'Desk', 'amount' => 5]);

$collection->hasAny(['product', 'price']);

// true

$collection->hasAny(['name', 'price']);

// false
```

<a name="method-implode"></a>
#### `implode()`

`implode` 메서드는 컬렉션 내부 항목들을 문자열로 합칩니다. 배열이나 객체의 경우, 합칠 속성명과 구분 문자열을 인수로 전달합니다:

```php
$collection = collect([
    ['account_id' => 1, 'product' => 'Desk'],
    ['account_id' => 2, 'product' => 'Chair'],
]);

$collection->implode('product', ', ');

// Desk, Chair
```

간단한 문자열/숫자 값인 경우 구분자를 하나만 전달합니다:

```php
collect([1, 2, 3, 4, 5])->implode('-');

// '1-2-3-4-5'
```

콜백을 전달하여 합치기 전에 값 포맷팅할 수도 있습니다:

```php
$collection->implode(function (array $item, int $key) {
    return strtoupper($item['product']);
}, ', ');

// DESK, CHAIR
```

<a name="method-intersect"></a>
#### `intersect()`

`intersect` 메서드는 원본 컬렉션에서 인수로 주어진 배열이나 컬렉션에 존재하지 않는 값을 제거하고, 이를 키를 유지한 채 반환합니다:

```php
$collection = collect(['Desk', 'Sofa', 'Chair']);

$intersect = $collection->intersect(['Desk', 'Chair', 'Bookcase']);

$intersect->all();

// [0 => 'Desk', 2 => 'Chair']
```

> [!NOTE]
> [Eloquent Collections](/docs/master/eloquent-collections#method-intersect) 사용 시 동작이 다를 수 있습니다.

<a name="method-intersectusing"></a>
#### `intersectUsing()`

`intersectUsing`은 사용자 정의 비교 콜백을 통해 값을 비교하며, 원본 컬렉션에서 값이 존재하지 않는 요소를 제거하고 키를 유지합니다:

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

`intersectAssoc` 메서드는 키와 값 모두를 비교하여, 모든 컬렉션에 공통으로 존재하는 키-값 쌍을 반환합니다:

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

`intersectAssocUsing`은 사용자 정의 비교 콜백을 통해 키와 값 쌍의 동등성을 판단하여 공통 요소를 반환합니다:

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

`intersectByKeys` 메서드는 키 기준으로만 값을 비교하여, 주어진 배열 또는 컬렉션에 없는 키-값 쌍을 삭제합니다:

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

`isEmpty` 메서드는 컬렉션이 비어 있으면 `true`, 아니면 `false`를 반환합니다:

```php
collect([])->isEmpty();

// true
```

<a name="method-isnotempty"></a>
#### `isNotEmpty()`

`isNotEmpty` 메서드는 컬렉션에 하나 이상의 항목이 있으면 `true`, 비어 있으면 `false`를 반환합니다:

```php
collect([])->isNotEmpty();

// false
```

<a name="method-join"></a>
#### `join()`

`join` 메서드는 컬렉션 값을 문자열로 연결합니다. 두 번째 인수로 마지막 항목의 연결 방식을 지정할 수 있습니다:

```php
collect(['a', 'b', 'c'])->join(', '); // 'a, b, c'
collect(['a', 'b', 'c'])->join(', ', ', and '); // 'a, b, and c'
collect(['a', 'b'])->join(', ', ' and '); // 'a and b'
collect(['a'])->join(', ', ' and '); // 'a'
collect([])->join(', ', ' and '); // ''
```

<a name="method-keyby"></a>
#### `keyBy()`

`keyBy` 메서드는 지정한 키를 기준으로 컬렉션을 재인덱싱합니다. 중복 키가 있으면 마지막 요소가 유지됩니다:

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

콜백을 전달할 수도 있습니다:

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

`keys` 메서드는 컬렉션의 모든 키를 반환합니다:

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

`last` 메서드는 특정 조건에 맞는 컬렉션의 마지막 요소를 반환합니다:

```php
collect([1, 2, 3, 4])->last(function (int $value, int $key) {
    return $value < 3;
});

// 2
```

인수 없이 호출 시 컬렉션의 마지막 요소를 반환하며, 비어 있으면 `null`을 반환합니다:

```php
collect([1, 2, 3, 4])->last();

// 4
```

<a name="method-lazy"></a>
#### `lazy()`

`lazy` 메서드는 내부 배열로부터 새로운 [`LazyCollection`](#lazy-collections) 인스턴스를 반환합니다:

```php
$lazyCollection = collect([1, 2, 3, 4])->lazy();

$lazyCollection::class;

// Illuminate\Support\LazyCollection

$lazyCollection->all();

// [1, 2, 3, 4]
```

대규모 컬렉션에 대해 메모리를 절약하면서 변환을 수행해야 할 때 유용합니다:

```php
$count = $hugeCollection
    ->lazy()
    ->where('country', 'FR')
    ->where('balance', '>', '100')
    ->count();
```

`LazyCollection`으로 변환하면 추가 메모리 사용 없이 필터링 가능해집니다.

<a name="method-macro"></a>
#### `macro()`

정적 `macro` 메서드는 런타임에 `Collection` 클래스에 메서드를 추가할 수 있도록 합니다. 자세한 내용은 [컬렉션 확장하기](#extending-collections)를 참고하세요.

<a name="method-make"></a>
#### `make()`

정적 `make` 메서드는 새 컬렉션 인스턴스를 생성합니다. [컬렉션 생성하기](#creating-collections) 참고.

<a name="method-map"></a>
#### `map()`

`map` 메서드는 각 항목에 클로저를 적용해 새 컬렉션을 만듭니다:

```php
$collection = collect([1, 2, 3, 4, 5]);

$multiplied = $collection->map(function (int $item, int $key) {
    return $item * 2;
});

$multiplied->all();

// [2, 4, 6, 8, 10]
```

> [!WARNING]
> 다른 대부분 컬렉션 메서드와 같이, `map`은 새 컬렉션을 반환하며 원본을 수정하지 않습니다. 원본을 변형하려면 [`transform`](#method-transform) 메서드를 사용하세요.

<a name="method-mapinto"></a>
#### `mapInto()`

`mapInto`는 각 항목을 전달하여 주어진 클래스의 새 인스턴스를 생성한 컬렉션을 반환합니다:

```php
class Currency
{
    /**
     * 새로운 통화 인스턴스 생성자.
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

`mapSpread`는 중첩된 각각의 값을 별개의 인자로 콜백에 전달하여 변환한 새 컬렉션을 만듭니다:

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

`mapToGroups`는 콜백이 반환하는 키-값 쌍으로 컬렉션을 그룹화합니다:

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

`mapWithKeys`는 콜백이 반환한 단일 키-값 배열로 새 컬렉션을 만듭니다:

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

`max` 메서드는 지정한 키의 최대 값을 반환합니다:

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

`median` 메서드는 지정한 키의 [중앙값](https://en.wikipedia.org/wiki/Median)을 반환합니다:

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

`merge` 메서드는 기존 컬렉션과 주어진 배열 또는 컬렉션을 병합합니다. 문자열 키가 겹치면 주어진 쪽 값으로 덮어씌웁니다:

```php
$collection = collect(['product_id' => 1, 'price' => 100]);

$merged = $collection->merge(['price' => 200, 'discount' => false]);

$merged->all();

// ['product_id' => 1, 'price' => 200, 'discount' => false]
```

숫자 키가 겹치는 경우 값은 뒤에 붙습니다:

```php
$collection = collect(['Desk', 'Chair']);

$merged = $collection->merge(['Bookcase', 'Door']);

$merged->all();

// ['Desk', 'Chair', 'Bookcase', 'Door']
```

<a name="method-mergerecursive"></a>
#### `mergeRecursive()`

`mergeRecursive`는 중첩된 배열까지 재귀적으로 병합하며, 같은 키에 대해 값들을 배열로 결합합니다:

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

`min` 메서드는 지정한 키의 최소 값을 반환합니다:

```php
$min = collect([['foo' => 10], ['foo' => 20]])->min('foo');

// 10

$min = collect([1, 2, 3, 4, 5])->min();

// 1
```

<a name="method-mode"></a>
#### `mode()`

`mode` 메서드는 지정한 키의 [최빈값](https://en.wikipedia.org/wiki/Mode_(statistics)) 배열을 반환합니다:

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

`multiply` 메서드는 컬렉션 내 모든 아이템을 지정된 횟수만큼 복사하여 새 컬렉션으로 만듭니다:

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

`nth` 메서드는 n번째마다 아이템을 선택한 새 컬렉션을 만듭니다:

```php
$collection = collect(['a', 'b', 'c', 'd', 'e', 'f']);

$collection->nth(4);

// ['a', 'e']
```

두 번째 인수로 시작 오프셋을 지정할 수 있습니다:

```php
$collection->nth(4, 1);

// ['b', 'f']
```

<a name="method-only"></a>
#### `only()`

`only` 메서드는 지정한 키에 해당하는 아이템만 새 컬렉션으로 반환합니다:

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

`only`의 반대는 [except](#method-except) 메서드입니다.

> [!NOTE]
> 이 메서드는 [Eloquent Collections](/docs/master/eloquent-collections#method-only) 사용 시 동작이 다릅니다.

<a name="method-pad"></a>
#### `pad()`

`pad` 메서드는 배열의 크기가 지정한 사이즈에 도달할 때까지 주어진 값으로 채워 넣습니다. 작으면 왼쪽, 양수면 오른쪽을 채웁니다:

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

`partition` 메서드는 전달된 클로저를 기준으로 컬렉션을 두 그룹으로 나누어 각각 새 컬렉션으로 반환합니다:

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

<a name="method-percentage"></a>
#### `percentage()`

`percentage` 메서드는 주어진 조건에 통과하는 아이템의 비율(%)을 쉽게 구할 수 있습니다:

```php
$collection = collect([1, 1, 2, 2, 2, 3]);

$percentage = $collection->percentage(fn ($value) => $value === 1);

// 33.33
```

두 번째 인수로 소수점 자릿수를 변경할 수 있습니다:

```php
$percentage = $collection->percentage(fn ($value) => $value === 1, precision: 3);

// 33.333
```

<a name="method-pipe"></a>
#### `pipe()`

`pipe` 메서드는 컬렉션을 주어진 클로저에 전달하고, 그 실행 결과를 반환합니다:

```php
$collection = collect([1, 2, 3]);

$piped = $collection->pipe(function (Collection $collection) {
    return $collection->sum();
});

// 6
```

<a name="method-pipeinto"></a>
#### `pipeInto()`

`pipeInto` 메서드는 지정한 클래스의 새 인스턴스를 만들고 컬렉션을 생성자에 전달합니다:

```php
class ResourceCollection
{
    /**
     * 새로운 ResourceCollection 인스턴스 생성자.
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

`pipeThrough` 메서드는 컬렉션을 여러 클로저에 순차적으로 전달하고 최종 결과를 반환합니다:

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

`pluck` 메서드는 특정 키에 해당하는 모든 값을 반환합니다:

```php
$collection = collect([
    ['product_id' => 'prod-100', 'name' => 'Desk'],
    ['product_id' => 'prod-200', 'name' => 'Chair'],
]);

$plucked = $collection->pluck('name');

$plucked->all();

// ['Desk', 'Chair']
```

두 번째 인수로 어떤 키를 기준으로 결과를 인덱싱할지 지정할 수 있습니다:

```php
$plucked = $collection->pluck('name', 'product_id');

$plucked->all();

// ['prod-100' => 'Desk', 'prod-200' => 'Chair']
```

"점(dot)" 표기법으로 중첩된 값을 가져올 수도 있습니다:

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

키가 중복되면 마지막 일치 항목이 반영됩니다:

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

`pop` 메서드는 컬렉션의 마지막 항목을 제거하고 반환합니다:

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->pop();

// 5

$collection->all();

// [1, 2, 3, 4]
```

정수를 인수로 전달해서 여러 항목을 한꺼번에 제거할 수도 있습니다:

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->pop(3);

// collect([5, 4, 3])

$collection->all();

// [1, 2]
```

<a name="method-prepend"></a>
#### `prepend()`

`prepend` 메서드는 컬렉션의 맨 앞에 항목을 추가합니다:

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->prepend(0);

$collection->all();

// [0, 1, 2, 3, 4, 5]
```

두 번째 인수로 항목의 키를 지정할 수 있습니다:

```php
$collection = collect(['one' => 1, 'two' => 2]);

$collection->prepend(0, 'zero');

$collection->all();

// ['zero' => 0, 'one' => 1, 'two' => 2]
```

<a name="method-pull"></a>
#### `pull()`

`pull` 메서드는 키를 지정해 컬렉션에서 항목을 제거하고 반환합니다:

```php
$collection = collect(['product_id' => 'prod-100', 'name' => 'Desk']);

$collection->pull('name');

// 'Desk'

$collection->all();

// ['product_id' => 'prod-100']
```

<a name="method-push"></a>
#### `push()`

`push` 메서드는 컬렉션의 끝에 항목을 추가합니다:

```php
$collection = collect([1, 2, 3, 4]);

$collection->push(5);

$collection->all();

// [1, 2, 3, 4, 5]
```

<a name="method-put"></a>
#### `put()`

`put` 메서드는 지정한 키-값 쌍을 컬렉션에 저장합니다:

```php
$collection = collect(['product_id' => 1, 'name' => 'Desk']);

$collection->put('price', 100);

$collection->all();

// ['product_id' => 1, 'name' => 'Desk', 'price' => 100]
```

<a name="method-random"></a>
#### `random()`

`random` 메서드는 컬렉션에서 임의의 항목을 반환합니다:

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->random();

// 4 (랜덤하게 선택됨)
```

숫자를 인수로 전달해 무작위로 여러 항목을 반환할 수도 있습니다:

```php
$random = $collection->random(3);

$random->all();

// [2, 4, 5] (랜덤 선택)
```

요청 개수보다 작은 항목이 있으면 예외를 던집니다.

콜백 인수도 받습니다:

```php
use Illuminate\Support\Collection;

$random = $collection->random(fn (Collection $items) => min(10, count($items)));

$random->all();

// [1, 2, 3, 4, 5] (랜덤 선택)
```

<a name="method-range"></a>
#### `range()`

`range` 메서드는 지정한 범위 내의 정수로 컬렉션을 생성합니다:

```php
$collection = collect()->range(3, 6);

$collection->all();

// [3, 4, 5, 6]
```

<a name="method-reduce"></a>
#### `reduce()`

`reduce` 메서드는 중간 결과를 누적해 하나의 값으로 축소합니다:

```php
$collection = collect([1, 2, 3]);

$total = $collection->reduce(function (?int $carry, int $item) {
    return $carry + $item;
});

// 6
```

초기 `$carry` 값은 `null`이지만, 두 번째 인수로 지정할 수 있습니다:

```php
$collection->reduce(function (int $carry, int $item) {
    return $carry + $item;
}, 4);

// 10
```

키도 콜백에 전달됩니다:

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

$collection->reduce(function (int $carry, int $value, int $key) use ($ratio) {
    return $carry + ($value * $ratio[$key]);
});

// 4264
```

<a name="method-reduce-spread"></a>
#### `reduceSpread()`

`reduceSpread` 메서드는 여러 초기 값을 인수로 받아 축소하며 배열을 반환합니다:

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

`reject` 메서드는 주어진 클로저가 `true`를 반환하는 항목을 제거합니다:

```php
$collection = collect([1, 2, 3, 4]);

$filtered = $collection->reject(function (int $value, int $key) {
    return $value > 2;
});

$filtered->all();

// [1, 2]
```

`reject`는 `filter`의 반대 메서드입니다.

<a name="method-replace"></a>
#### `replace()`

`replace` 메서드는 `merge`와 비슷하나, 문자열 키뿐 아니라 숫자 키도 덮어씁니다:

```php
$collection = collect(['Taylor', 'Abigail', 'James']);

$replaced = $collection->replace([1 => 'Victoria', 3 => 'Finn']);

$replaced->all();

// ['Taylor', 'Victoria', 'James', 'Finn']
```

<a name="method-replacerecursive"></a>
#### `replaceRecursive()`

`replace`와 유사하지만, 배열 내부에 대해서도 재귀적으로 치환을 수행합니다:

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

`reverse` 메서드는 컬렉션 아이템의 순서를 뒤집으며, 키는 그대로 유지합니다:

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

`search` 메서드는 값을 검색해 키를 반환합니다. 존재하지 않으면 `false`를 반환합니다:

```php
$collection = collect([2, 4, 6, 8]);

$collection->search(4);

// 1
```

느슨한 비교를 하며, 두 번째 인수에 `true`를 전달하면 엄격한 비교를 합니다:

```php
collect([2, 4, 6, 8])->search('4', strict: true);

// false
```

콜백으로 직접 탐색 기준을 코딩할 수도 있습니다:

```php
collect([2, 4, 6, 8])->search(function (int $item, int $key) {
    return $item > 5;
});

// 2
```

<a name="method-select"></a>
#### `select()`

`select` 메서드는 SQL의 `SELECT`처럼, 컬렉션에서 특정 키만 선택합니다:

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

`shift` 메서드는 컬렉션의 첫 번째 요소를 제거하고 반환합니다:

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->shift();

// 1

$collection->all();

// [2, 3, 4, 5]
```

정수를 인수로 전달하여 여러 항목을 한 번에 제거할 수 있습니다.

<a name="method-shuffle"></a>
#### `shuffle()`

`shuffle` 메서드는 컬렉션을 무작위로 섞습니다:

```php
$collection = collect([1, 2, 3, 4, 5]);

$shuffled = $collection->shuffle();

$shuffled->all();

// [3, 2, 5, 1, 4] - (랜덤 생성)
```

<a name="method-skip"></a>
#### `skip()`

`skip` 메서드는 시작 부분에서 지정한 수만큼 아이템을 뺀 새 컬렉션을 반환합니다:

```php
$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);

$collection = $collection->skip(4);

$collection->all();

// [5, 6, 7, 8, 9, 10]
```

<a name="method-skipuntil"></a>
#### `skipUntil()`

`skipUntil` 메서드는 주어진 콜백이 `false`를 반환하는 동안 아이템을 건너뛰고, `true`가 되면 나머지 아이템을 반환합니다:

```php
$collection = collect([1, 2, 3, 4]);

$subset = $collection->skipUntil(function (int $item) {
    return $item >= 3;
});

$subset->all();

// [3, 4]
```

간단한 값도 인수로 전달할 수 있습니다:

```php
$collection = collect([1, 2, 3, 4]);

$subset = $collection->skipUntil(3);

$subset->all();

// [3, 4]
```

> [!WARNING]
> 값이 안 나오거나 콜백이 `true`를 반환하지 않으면 빈 컬렉션 반환.

<a name="method-skipwhile"></a>
#### `skipWhile()`

`skipWhile` 메서드는 콜백이 `true`인 동안 아이템들을 건너뛰고, `false`가 되면 나머지 아이템을 반환합니다:

```php
$collection = collect([1, 2, 3, 4]);

$subset = $collection->skipWhile(function (int $item) {
    return $item <= 3;
});

$subset->all();

// [4]
```

> [!WARNING]
> 콜백이 한 번도 `false`를 반환하지 않으면 빈 컬렉션 반환.

<a name="method-slice"></a>
#### `slice()`

`slice` 메서드는 지정한 인덱스부터 시작하는 부분집합을 반환합니다:

```php
$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);

$slice = $collection->slice(4);

$slice->all();

// [5, 6, 7, 8, 9, 10]
```

두 번째 인수로 길이를 제한할 수 있습니다:

```php
$slice = $collection->slice(4, 2);

$slice->all();

// [5, 6]
```

기본적으로 키를 유지합니다. 키 재설정이 필요하면 [`values`](#method-values)를 사용하세요.

<a name="method-sliding"></a>
#### `sliding()`

`sliding` 메서드는 지정한 크기의 '슬라이딩 윈도우' 뷰를 생성합니다:

```php
$collection = collect([1, 2, 3, 4, 5]);

$chunks = $collection->sliding(2);

$chunks->toArray();

// [[1, 2], [2, 3], [3, 4], [4, 5]]
```

[`eachSpread`](#method-eachspread)와 함께 자주 사용됩니다:

```php
$transactions->sliding(2)->eachSpread(function (Collection $previous, Collection $current) {
    $current->total = $previous->total + $current->amount;
});
```

두 번째 인수 `step` 으로 조각 간 거리도 지정할 수 있습니다:

```php
$collection = collect([1, 2, 3, 4, 5]);

$chunks = $collection->sliding(3, step: 2);

$chunks->toArray();

// [[1, 2, 3], [3, 4, 5]]
```

<a name="method-sole"></a>
#### `sole()`

`sole` 메서드는 정확히 한 개의 요소만 조건에 맞으면, 그 요소를 반환합니다:

```php
collect([1, 2, 3, 4])->sole(function (int $value, int $key) {
    return $value === 2;
});

// 2
```

키-값 쌍으로도 사용 가능하며, 조건에 하나만 일치하면 반환합니다:

```php
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
]);

$collection->sole('product', 'Chair');

// ['product' => 'Chair', 'price' => 100]
```

인수 없이 호출하면 요소가 하나일 때만 반환합니다:

```php
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
]);

$collection->sole();

// ['product' => 'Desk', 'price' => 200]
```

해당 조건에 맞는 요소가 없으면 `ItemNotFoundException` 예외, 두 개 이상이면 `MultipleItemsFoundException` 예외를 던집니다.

<a name="method-some"></a>
#### `some()`

`contains` 메서드의 별칭입니다.

<a name="method-sort"></a>
#### `sort()`

`sort` 메서드는 컬렉션을 정렬합니다. 정렬된 컬렉션은 원래 키를 유지하므로, 필요하면 [`values`](#method-values)를 사용해 키를 재설정하세요:

```php
$collection = collect([5, 3, 1, 2, 4]);

$sorted = $collection->sort();

$sorted->values()->all();

// [1, 2, 3, 4, 5]
```

정렬 알고리즘 커스텀용 콜백도 전달 가능합니다.

> [!NOTE]
> 중첩 배열이나 객체 정렬은 [`sortBy`](#method-sortby), [`sortByDesc`](#method-sortbydesc)를 참고하세요.

<a name="method-sortby"></a>
#### `sortBy()`

`sortBy` 메서드는 주어진 키 또는 콜백을 기준으로 컬렉션을 정렬합니다. 정렬 후에도 원 키는 유지하며, 필요하면 [`values`](#method-values)로 키 리셋 가능:

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

두 번째 인수로 [PHP 정렬 플래그](https://www.php.net/manual/en/function.sort.php)를 줄 수 있습니다:

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

콜백을 넘겨 직접 정렬 기준을 정의할 수도 있습니다:

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

여러 속성으로 정렬하려면 배열로 정렬 작업 배열을 전달할 수 있습니다:

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

클로저 배열로도 각 정렬 기준을 정의할 수 있습니다:

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

`sortBy`와 시그니처가 같지만 역순으로 정렬합니다.

<a name="method-sortdesc"></a>
#### `sortDesc()`

`sort`와 반대 순서로 정렬합니다:

```php
$collection = collect([5, 3, 1, 2, 4]);

$sorted = $collection->sortDesc();

$sorted->values()->all();

// [5, 4, 3, 2, 1]
```

`sortDesc`는 콜백 인수를 받지 않으므로, 필요하면 [`sort`](#method-sort)에서 비교를 뒤집어 작성하세요.

<a name="method-sortkeys"></a>
#### `sortKeys()`

`sortKeys`는 연관 배열의 키를 기준으로 컬렉션을 정렬합니다:

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

`sortKeys`와 같으나 역순 정렬합니다.

<a name="method-sortkeysusing"></a>
#### `sortKeysUsing()`

`sortKeysUsing`은 사용자 지정 콜백으로 키를 정렬합니다:

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

콜백은 `uksort` 함수 형태를 따라야 합니다.

<a name="method-splice"></a>
#### `splice()`

`splice` 메서드는 지정한 인덱스부터 컬렉션 일부를 잘라내어 반환합니다:

```php
$collection = collect([1, 2, 3, 4, 5]);

$chunk = $collection->splice(2);

$chunk->all();

// [3, 4, 5]

$collection->all();

// [1, 2]
```

두 번째 인수로 자를 길이를 제한할 수 있습니다:

```php
$collection = collect([1, 2, 3, 4, 5]);

$chunk = $collection->splice(2, 1);

$chunk->all();

// [3]

$collection->all();

// [1, 2, 4, 5]
```

세 번째 인수로 대체할 새 아이템도 전달할 수 있습니다:

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

`split` 메서드는 컬렉션을 지정한 개수만큼 그룹으로 쪼갭니다:

```php
$collection = collect([1, 2, 3, 4, 5]);

$groups = $collection->split(3);

$groups->all();

// [[1, 2], [3, 4], [5]]
```

<a name="method-splitin"></a>
#### `splitIn()`

`splitIn`은 지정 개수 그룹으로 나누지만 최종 그룹만 완전히 채우지 않고 나머지를 모읍니다:

```php
$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);

$groups = $collection->splitIn(3);

$groups->all();

// [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10]]
```

<a name="method-sum"></a>
#### `sum()`

`sum` 메서드는 모든 아이템의 합을 반환합니다:

```php
collect([1, 2, 3, 4, 5])->sum();

// 15
```

배열 또는 객체라면 합할 키를 지정합니다:

```php
$collection = collect([
    ['name' => 'JavaScript: The Good Parts', 'pages' => 176],
    ['name' => 'JavaScript: The Definitive Guide', 'pages' => 1096],
]);

$collection->sum('pages');

// 1272
```

콜백으로 합할 값을 지정할 수도 있습니다:

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

`take` 메서드는 지정한 수만큼 아이템을 포함하는 새 컬렉션을 반환합니다:

```php
$collection = collect([0, 1, 2, 3, 4, 5]);

$chunk = $collection->take(3);

$chunk->all();

// [0, 1, 2]
```

음수를 전달하면 뒤에서부터 개수를 가져옵니다:

```php
$collection = collect([0, 1, 2, 3, 4, 5]);

$chunk = $collection->take(-2);

$chunk->all();

// [4, 5]
```

<a name="method-takeuntil"></a>
#### `takeUntil()`

`takeUntil` 메서드는 콜백이 `true`를 반환할 때까지 아이템을 포함합니다:

```php
$collection = collect([1, 2, 3, 4]);

$subset = $collection->takeUntil(function (int $item) {
    return $item >= 3;
});

$subset->all();

// [1, 2]
```

값 인수도 허용합니다:

```php
$collection = collect([1, 2, 3, 4]);

$subset = $collection->takeUntil(3);

$subset->all();

// [1, 2]
```

> [!WARNING]
> 조건이 충족되지 않으면 컬렉션 전체 반환.

<a name="method-takewhile"></a>
#### `takeWhile()`

`takeWhile`은 콜백이 `false`를 반환할 때까지 아이템을 포함합니다:

```php
$collection = collect([1, 2, 3, 4]);

$subset = $collection->takeWhile(function (int $item) {
    return $item < 3;
});

$subset->all();

// [1, 2]
```

> [!WARNING]
> 콜백이 `false`를 반환하지 않으면 컬렉션 전체 반환.

<a name="method-tap"></a>
#### `tap()`

`tap` 메서드는 특정 시점에 컬렉션을 콜백에 넘겨 작업하되, 컬렉션 자체에 영향을 주지 않고 원본 컬렉션을 반환합니다:

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

정적 `times` 메서드는 지정 횟수만큼 콜백을 실행하고, 결과로 새 컬렉션을 만듭니다:

```php
$collection = Collection::times(10, function (int $number) {
    return $number * 9;
});

$collection->all();

// [9, 18, 27, 36, 45, 54, 63, 72, 81, 90]
```

<a name="method-toarray"></a>
#### `toArray()`

`toArray` 메서드는 컬렉션을 일반 PHP 배열로 변환합니다. 컬렉션 내의 Eloquent 모델들도 배열로 변환됩니다:

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
> 컬렉션 내에 `Arrayable` 객체도 재귀적으로 배열로 변환합니다. 순수 배열을 원한다면 [`all`](#method-all) 메서드를 사용하세요.

<a name="method-tojson"></a>
#### `toJson()`

`toJson` 메서드는 컬렉션을 JSON 직렬화된 문자열로 변환합니다:

```php
$collection = collect(['name' => 'Desk', 'price' => 200]);

$collection->toJson();

// '{"name":"Desk", "price":200}'
```

<a name="method-transform"></a>
#### `transform()`

`transform` 메서드는 각 아이템을 콜백으로 변형하고, 원본 컬렉션을 직접 수정합니다:

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->transform(function (int $item, int $key) {
    return $item * 2;
});

$collection->all();

// [2, 4, 6, 8, 10]
```

> [!WARNING]
> `transform`은 원본 컬렉션을 수정합니다. 새 컬렉션을 만들고 싶으면 [`map`](#method-map) 메서드를 사용하세요.

<a name="method-undot"></a>
#### `undot()`

`undot` 메서드는 점(dot) 표기법 키를 가진 단일 차원 컬렉션을 다중 차원 컬렉션으로 확장합니다:

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

`union` 메서드는 지정 배열의 키-값들을 컬렉션에 추가하며, 기존 키가 있으면 컬렉션 값을 유지합니다:

```php
$collection = collect([1 => ['a'], 2 => ['b']]);

$union = $collection->union([3 => ['c'], 1 => ['d']]);

$union->all();

// [1 => ['a'], 2 => ['b'], 3 => ['c']]
```

<a name="method-unique"></a>
#### `unique()`

`unique` 메서드는 컬렉션에서 중복 값을 제거해 반환합니다. 키는 유지되므로 필요시 [`values`](#method-values)로 재인덱싱하세요:

```php
$collection = collect([1, 1, 2, 2, 3, 4, 2]);

$unique = $collection->unique();

$unique->values()->all();

// [1, 2, 3, 4]
```

중첩 배열이나 객체에 대해 유니크를 결정하는 키를 지정할 수 있습니다:

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

또는 직접 유니크 기준을 정의하는 콜백도 줄 수 있습니다:

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

`unique`는 "느슨한" 비교를 합니다. 엄격한 비교를 위해서는 [`uniqueStrict`](#method-uniquestrict)를 사용하세요.

> [!NOTE]
> 이 메서드는 [Eloquent Collections](/docs/master/eloquent-collections#method-unique)에서 다르게 동작할 수 있습니다.

<a name="method-uniquestrict"></a>
#### `uniqueStrict()`

`unique`와 시그니처는 같으나 모든 값을 "엄격히" 비교합니다.

<a name="method-unless"></a>
#### `unless()`

`unless` 메서드는 첫 번째 인수가 `true`로 평가되지 않을 때 콜백을 실행합니다:

```php
$collection = collect([1, 2, 3]);

$collection->unless(true, function (Collection $collection) {
    return $collection->push(4);
});

$collection->unless(false, function (Collection $collection) {
    return $collection->push(5);
});

$collection->all();

// [1, 2, 3, 5]
```

두 번째 콜백을 전달하면 첫 번째 인수가 `true`일 때 실행됩니다:

```php
$collection = collect([1, 2, 3]);

$collection->unless(true, function (Collection $collection) {
    return $collection->push(4);
}, function (Collection $collection) {
    return $collection->push(5);
});

$collection->all();

// [1, 2, 3, 5]
```

`unless`의 반대는 [`when`](#method-when)입니다.

<a name="method-unlessempty"></a>
#### `unlessEmpty()`

[`whenNotEmpty`](#method-whennotempty)의 별칭입니다.

<a name="method-unlessnotempty"></a>
#### `unlessNotEmpty()`

[`whenEmpty`](#method-whenempty)의 별칭입니다.

<a name="method-unwrap"></a>
#### `unwrap()`

정적 `unwrap` 메서드는 만약 가능하면 컬렉션의 내부 아이템을 반환합니다:

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

`value` 메서드는 컬렉션 첫 번째 요소에서 지정한 키의 값을 반환합니다:

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

`values` 메서드는 키를 연속된 정수로 재설정한 새 컬렉션을 반환합니다:

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

`when` 메서드는 첫 번째 인수가 `true`로 평가될 때 지정한 콜백을 실행합니다:

```php
$collection = collect([1, 2, 3]);

$collection->when(true, function (Collection $collection, int $value) {
    return $collection->push(4);
});

$collection->when(false, function (Collection $collection, int $value) {
    return $collection->push(5);
});

$collection->all();

// [1, 2, 3, 4]
```

두 번째 콜백을 전달하면 첫 번째 인수가 `false`일 때 실행됩니다:

```php
$collection = collect([1, 2, 3]);

$collection->when(false, function (Collection $collection, int $value) {
    return $collection->push(4);
}, function (Collection $collection) {
    return $collection->push(5);
});

$collection->all();

// [1, 2, 3, 5]
```

`when`의 반대는 [`unless`](#method-unless)입니다.

<a name="method-whenempty"></a>
#### `whenEmpty()`

`whenEmpty`는 컬렉션이 비어있을 때 콜백을 실행합니다:

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

두 번째 콜백을 지정해, 비어 있지 않은 경우 실행하게 할 수 있습니다:

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

`whenEmpty`의 반대는 [`whenNotEmpty`](#method-whennotempty)입니다.

<a name="method-whennotempty"></a>
#### `whenNotEmpty()`

`whenNotEmpty`는 컬렉션이 비어 있지 않을 때 콜백을 실행합니다:

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

두 번째 콜백을 지정해, 컬렉션이 비어 있을 때 실행하게 할 수 있습니다:

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

`whenNotEmpty`의 반대는 [`whenEmpty`](#method-whenempty)입니다.

<a name="method-where"></a>
#### `where()`

`where` 메서드는 주어진 키-값 조건에 따라 컬렉션을 필터링합니다:

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

느슨한 비교를 하며, [`whereStrict`](#method-wherestrict)를 이용해 엄격 비교가 가능합니다.

두 번째 인수로 비교 연산자를 지정할 수 있습니다:

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

`where`와 시그니처 같으나 값 비교에 엄격한 비교를 사용합니다.

<a name="method-wherebetween"></a>
#### `whereBetween()`

`whereBetween`은 지정한 범위 안에 값이 포함되는 아이템만 필터링합니다:

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

`whereIn`은 배열 내에 있는 값들만 필터링해 남깁니다:

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

"느슨한" 비교를 기본 사용합니다. 엄격한 비교를 위해서는 [`whereInStrict`](#method-whereinstrict)를 사용하세요.

<a name="method-whereinstrict"></a>
#### `whereInStrict()`

`whereIn`의 엄격 비교 버전입니다.

<a name="method-whereinstanceof"></a>
#### `whereInstanceOf()`

`whereInstanceOf`는 특정 클래스 인스턴스만 필터링합니다:

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

`whereNotBetween`은 지정 범위를 벗어나는 값을 필터링합니다:

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

`whereNotIn`은 배열 내 값에 포함되지 않는 항목만 유지합니다:

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

"느슨한" 비교가 기본입니다. 엄격한 비교는 [`whereNotInStrict`](#method-wherenotinstrict) 사용.

<a name="method-wherenotinstrict"></a>
#### `whereNotInStrict()`

`whereNotIn`의 엄격 비교 버전입니다.

<a name="method-wherenotnull"></a>
#### `whereNotNull()`

`whereNotNull`은 주어진 키의 값이 `null`이 아닌 아이템만 반환합니다:

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

`whereNull`은 지정 키의 값이 `null`인 아이템만 반환합니다:

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

정적 `wrap` 메서드는 값이 컬렉션이 아니면 컬렉션으로 감쌉니다:

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

`zip` 메서드는 주어진 배열 값과 인덱스별로 컬렉션 값을 병합합니다:

```php
$collection = collect(['Chair', 'Desk']);

$zipped = $collection->zip([100, 200]);

$zipped->all();

// [['Chair', 100], ['Desk', 200]]
```

<a name="higher-order-messages"></a>
## 고차 메시지(Higher Order Messages)

컬렉션은 “고차 메시지”도 지원합니다. 이는 컬렉션에서 자주 사용하는 작업을 줄여 쓸 수 있는 단축 문법입니다. 고차 메시지를 지원하는 컬렉션 메서드는 다음과 같습니다: [`average`](#method-average), [`avg`](#method-avg), [`contains`](#method-contains), [`each`](#method-each), [`every`](#method-every), [`filter`](#method-filter), [`first`](#method-first), [`flatMap`](#method-flatmap), [`groupBy`](#method-groupby), [`keyBy`](#method-keyby), [`map`](#method-map), [`max`](#method-max), [`min`](#method-min), [`partition`](#method-partition), [`reject`](#method-reject), [`skipUntil`](#method-skipuntil), [`skipWhile`](#method-skipwhile), [`some`](#method-some), [`sortBy`](#method-sortby), [`sortByDesc`](#method-sortbydesc), [`sum`](#method-sum), [`takeUntil`](#method-takeuntil), [`takeWhile`](#method-takewhile), 그리고 [`unique`](#method-unique).

각 고차 메시지는 컬렉션 인스턴스의 동적 속성으로 접근할 수 있습니다. 예를 들어, `each` 고차 메시지를 이용하면 다음과 같이 컬렉션 내 객체의 메서드를 짧게 호출할 수 있습니다:

```php
use App\Models\User;

$users = User::where('votes', '>', 500)->get();

$users->each->markAsVip();
```

마찬가지로 `sum` 고차 메시지를 써서 컬렉션 내 사용자들의 "votes" 총합을 간결하게 구할 수도 있습니다:

```php
$users = User::where('group', 'Development')->get();

return $users->sum->votes;
```

<a name="lazy-collections"></a>
## 지연 컬렉션 (Lazy Collections)

<a name="lazy-collection-introduction"></a>
### 소개

> [!WARNING]
> Laravel의 지연 컬렉션을 배우기 전, [PHP 생성자(Generators)](https://www.php.net/manual/en/language.generators.overview.php)를 숙지하는 것을 권장합니다.

`LazyCollection` 클래스는 PHP 생성자를 활용하여 메모리 사용량을 줄이면서 매우 큰 데이터셋 작업에 적합하도록 지원합니다.

예를 들어, 다중 기가바이트 로그 파일을 처리할 때 Laravel 컬렉션 메서드를 활용하고 싶다고 가정합시다. 파일 전체를 메모리에 로드하는 대신, 지연 컬렉션을 사용하면 일정 부분만 메모리에 유지하며 처리할 수 있습니다:

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

또는, 10,000개의 Eloquent 모델을 순회할 때 전통적인 컬렉션이면 모두 메모리에 올려야 하지만, 쿼리 빌더의 `cursor` 메서드는 `LazyCollection` 인스턴스를 반환해 하나씩만 메모리에 띄워 처리 가능합니다:

```php
use App\Models\User;

$users = User::cursor()->filter(function (User $user) {
    return $user->id > 500;
});

foreach ($users as $user) {
    echo $user->id;
}
```

이 경우 필터링은 실제로 개별 user를 순회할 때 실행되어 메모리 사용량이 크게 줄어듭니다.

<a name="creating-lazy-collections"></a>
### 지연 컬렉션 생성하기

지연 컬렉션 인스턴스는 PHP 생성자 함수를 `make` 메서드에 전달해 생성합니다:

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

거의 모든 `Collection` 클래스의 메서드는 `LazyCollection`에서도 사용할 수 있습니다. 두 클래스 모두 `Illuminate\Support\Enumerable` 계약을 구현하며, 이 계약은 다음 메서드를 정의합니다:

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
> `shift`, `pop`, `prepend` 같은 컬렉션을 변형하는 메서드는 `LazyCollection`에서 사용할 수 없습니다.

<a name="lazy-collection-methods"></a>
### 지연 컬렉션 메서드

`Enumerable` 계약에 정의된 메서드 외에 `LazyCollection` 클래스에는 다음과 같은 메서드가 추가됩니다:

<a name="method-takeUntilTimeout"></a>
#### `takeUntilTimeout()`

`takeUntilTimeout` 메서드는 지정 시간까지 값을 열거하는 새 지연 컬렉션을 반환하며, 해당 시간이 지나면 열거를 중지합니다:

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

이 메서드 사용 예로, 인보이스를 데이터베이스에서 커서를 통해 제출하며 스케줄러가 15분마다 실행되고 최대 14분만 처리하도록 하는 상황을 들 수 있습니다:

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

`each`는 즉시 각 항목에 콜백을 실행하지만, `tapEach`는 아이템이 하나씩 꺼낼 때마다 콜백을 호출합니다:

```php
// 아직 아무것도 덤프되지 않음
$lazyCollection = LazyCollection::times(INF)->tapEach(function (int $value) {
    dump($value);
});

// 세 가지 아이템이 덤프됨
$array = $lazyCollection->take(3)->all();

// 1
// 2
// 3
```

<a name="method-throttle"></a>
#### `throttle()`

`throttle` 메서드는 지정 초간격마다 값을 반환하도록 속도를 제한(스로틀)합니다. 주로 API 요청 제한 등의 상황에서 유용합니다:

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

`remember` 메서드는 이미 열거한 값들을 캐시해, 이후 반복 시 재호출하지 않는 새 지연 컬렉션을 반환합니다:

```php
// 쿼리 실행 전
$users = User::cursor()->remember();

// 쿼리가 실행됨...
// 첫 5명은 DB에서 Hydrate 됨
$users->take(5)->all();

// 처음 5명은 컬렉션 캐시에서 제공되고,
// 이후 항목은 다시 DB에서 Hydrate 됨
$users->take(20)->all();
```