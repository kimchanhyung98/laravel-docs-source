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

`Illuminate\Support\Collection` 클래스는 배열 데이터 작업을 위한 유창한 체인 방식을 제공하는 편리한 래퍼(wrapper)입니다. 예를 들어, 다음 코드를 살펴보세요. `collect` 헬퍼를 사용해 배열로부터 새 컬렉션 인스턴스를 생성하고, 각 요소에 `strtoupper` 함수를 적용한 뒤, 빈 요소들을 제거합니다:

```
$collection = collect(['taylor', 'abigail', null])->map(function (?string $name) {
    return strtoupper($name);
})->reject(function (string $name) {
    return empty($name);
});
```

보시다시피, `Collection` 클래스는 메서드를 체인으로 연결하여 기본 배열에 대해 매핑(map)과 축소(reduce)를 유창하게 수행할 수 있도록 합니다. 일반적으로 컬렉션은 불변(immutable)입니다. 즉, 모든 `Collection` 메서드는 완전히 새로운 `Collection` 인스턴스를 반환합니다.

<a name="creating-collections"></a>
### 컬렉션 생성하기 (Creating Collections)

앞에서 언급한 대로, `collect` 헬퍼는 주어진 배열로부터 새 `Illuminate\Support\Collection` 인스턴스를 반환합니다. 따라서 컬렉션 생성은 다음처럼 간단합니다:

```
$collection = collect([1, 2, 3]);
```

> [!NOTE]  
> [Eloquent](/docs/11.x/eloquent) 쿼리 결과는 항상 `Collection` 인스턴스로 반환됩니다.

<a name="extending-collections"></a>
### 컬렉션 확장하기 (Extending Collections)

컬렉션은 "macroable"이라서 런타임에 `Collection` 클래스에 추가 메서드를 붙일 수 있습니다. `Illuminate\Support\Collection` 클래스의 `macro` 메서드는 매크로 호출 시 실행될 클로저를 받아들입니다. 이 매크로 클로저 내부에서는 `$this`를 통해 컬렉션의 다른 메서드들을 마치 자신 메서드처럼 사용할 수 있습니다. 예를 들어, 아래 코드는 `Collection` 클래스에 `toUpper` 메서드를 추가합니다:

```
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

대개 컬렉션 매크로는 [서비스 프로바이더](/docs/11.x/providers)의 `boot` 메서드 내에서 선언하는 것이 좋습니다.

<a name="macro-arguments"></a>
#### 매크로 인수 (Macro Arguments)

필요하다면 추가 인수를 받는 매크로도 정의할 수 있습니다:

```
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

이후 컬렉션 문서 대부분에서는 `Collection` 클래스에서 사용할 수 있는 메서드 하나하나를 살펴봅니다. 모든 메서드는 메서드 체인이 가능해 기본 배열을 유창하게 조작할 수 있다는 점을 기억하세요. 또한 거의 모든 메서드는 새 `Collection` 인스턴스를 반환해 필요 시 원본 컬렉션을 보존할 수 있습니다.

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
## 메서드 목록 (Method Listing)

<a name="method-after"></a>
#### `after()`

`after` 메서드는 지정한 항목 뒤의 항목을 반환합니다. 지정한 항목이 없거나 마지막 항목이면 `null`을 반환합니다:

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->after(3);

// 4

$collection->after(5);

// null
```

이 메서드는 "느슨한(loose)" 비교로 지정된 항목을 찾습니다. 즉, 정수 값을 포함하는 문자열이 동일한 정수 값과 같은 것으로 간주됩니다. "엄격한(strict)" 비교를 사용하려면 `strict` 인수를 전달하세요:

```
collect([2, 4, 6, 8])->after('4', strict: true);

// null
```

또는 사용자 정의 클로저로 특정 조건을 만족하는 첫 번째 항목을 찾을 수 있습니다:

```
collect([2, 4, 6, 8])->after(function (int $item, int $key) {
    return $item > 5;
});

// 8
```

<a name="method-all"></a>
#### `all()`

`all` 메서드는 컬렉션이 감싸고 있는 원본 배열을 반환합니다:

```
collect([1, 2, 3])->all();

// [1, 2, 3]
```

<a name="method-average"></a>
#### `average()`

`avg` 메서드의 별칭(alias)입니다.

<a name="method-avg"></a>
#### `avg()`

`avg` 메서드는 주어진 키의 [평균값](https://en.wikipedia.org/wiki/Average)을 반환합니다:

```
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

`before` 메서드는 `after` 메서드의 반대입니다. 지정된 항목 이전의 항목을 반환합니다. 지정한 항목이 없거나 첫 번째 항목인 경우 `null`을 반환합니다:

```
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

`chunk` 메서드는 컬렉션을 지정한 크기만큼 작은 여러 컬렉션으로 나눕니다:

```
$collection = collect([1, 2, 3, 4, 5, 6, 7]);

$chunks = $collection->chunk(4);

$chunks->all();

// [[1, 2, 3, 4], [5, 6, 7]]
```

이 메서드는 [Bootstrap](https://getbootstrap.com/docs/5.3/layout/grid/) 같은 그리드 시스템을 사용하는 [뷰](/docs/11.x/views)에서 특히 유용합니다. 예를 들어, [Eloquent](/docs/11.x/eloquent) 모델 컬렉션을 그리드에 표시하고 싶다면:

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

`chunkWhile` 메서드는 주어진 콜백 결과에 따라 컬렉션을 여러 작은 컬렉션으로 나눕니다. 클로저의 `$chunk` 변수로 이전 요소를 확인할 수 있습니다:

```
$collection = collect(str_split('AABBCCCD'));

$chunks = $collection->chunkWhile(function (string $value, int $key, Collection $chunk) {
    return $value === $chunk->last();
});

$chunks->all();

// [['A', 'A'], ['B', 'B'], ['C', 'C', 'C'], ['D']]
```

<a name="method-collapse"></a>
#### `collapse()`

`collapse` 메서드는 다중 배열 컬렉션을 하나의 평면 컬렉션으로 합칩니다:

```
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

`collapseWithKeys` 메서드는 배열이나 컬렉션의 컬렉션을 키를 유지한 채 하나로 평탄화합니다:

```
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

`collect` 메서드는 현재 컬렉션 내 항목들로 새 `Collection` 인스턴스를 반환합니다:

```
$collectionA = collect([1, 2, 3]);

$collectionB = $collectionA->collect();

$collectionB->all();

// [1, 2, 3]
```

이 메서드는 주로 [지연 컬렉션](#lazy-collections)을 일반 `Collection` 인스턴스로 변환할 때 유용합니다:

```
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
> `collect` 메서드는 `Enumerable` 계약의 일부이므로, `Enumerable` 인스턴스를 비지연 컬렉션 인스턴스로 안전하게 변환할 때 특히 유용합니다.

<a name="method-combine"></a>
#### `combine()`

`combine` 메서드는 컬렉션의 값을 키로 하고, 다른 배열이나 컬렉션의 값을 값으로 하여 결합합니다:

```
$collection = collect(['name', 'age']);

$combined = $collection->combine(['George', 29]);

$combined->all();

// ['name' => 'George', 'age' => 29]
```

<a name="method-concat"></a>
#### `concat()`

`concat` 메서드는 주어진 `array`나 컬렉션 값을 다른 컬렉션의 끝에 덧붙입니다:

```
$collection = collect(['John Doe']);

$concatenated = $collection->concat(['Jane Doe'])->concat(['name' => 'Johnny Doe']);

$concatenated->all();

// ['John Doe', 'Jane Doe', 'Johnny Doe']
```

`concat` 메서드는 숫자 인덱스로 키를 다시 지정합니다. 키를 유지하려면 [merge](#method-merge) 메서드를 사용하세요.

<a name="method-contains"></a>
#### `contains()`

`contains` 메서드는 컬렉션에 지정한 항목이 있는지 판단합니다. 클로저를 전달해 조건 일치 여부로 판단할 수도 있습니다:

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->contains(function (int $value, int $key) {
    return $value > 5;
});

// false
```

값을 직접 전달하여 일치하는지 확인하거나, 키/값 쌍으로 특정 조건 일치를 확인할 수 있습니다:

```
$collection = collect(['name' => 'Desk', 'price' => 100]);

$collection->contains('Desk');

// true

$collection->contains('New York');

// false

$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
]);

$collection->contains('product', 'Bookcase');

// false
```

`contains` 메서드는 "느슨한" 비교를 사용합니다. "엄격한(strict)" 비교가 필요하다면 [`containsStrict`](#method-containsstrict) 메서드를 사용하세요.

반대 개념은 [`doesntContain`](#method-doesntcontain) 메서드입니다.

<a name="method-containsoneitem"></a>
#### `containsOneItem()`

`containsOneItem` 메서드는 컬렉션에 정확히 하나의 항목만 존재하는지 판단합니다:

```
collect([])->containsOneItem();

// false

collect(['1'])->containsOneItem();

// true

collect(['1', '2'])->containsOneItem();

// false
```

<a name="method-containsstrict"></a>
#### `containsStrict()`

`contains`와 시그니처는 같으나, 모든 값을 "엄격한(strict)" 비교로 검사합니다.

> [!NOTE]  
> [Eloquent Collection](/docs/11.x/eloquent-collections#method-contains)에서 동작이 다릅니다.

<a name="method-count"></a>
#### `count()`

`count` 메서드는 컬렉션 내 항목 개수를 반환합니다:

```
$collection = collect([1, 2, 3, 4]);

$collection->count();

// 4
```

<a name="method-countBy"></a>
#### `countBy()`

`countBy` 메서드는 컬렉션 내 각 값의 등장 횟수를 셉니다. 기본적으로 모든 요소를 세고, 클로저를 전달해 특정 기준에 따라 셀 수도 있습니다:

```
$collection = collect([1, 2, 2, 2, 3]);

$counted = $collection->countBy();

$counted->all();

// [1 => 1, 2 => 3, 3 => 1]
```

```
$collection = collect(['alice@gmail.com', 'bob@yahoo.com', 'carlos@gmail.com']);

$counted = $collection->countBy(function (string $email) {
    return substr(strrchr($email, "@"), 1);
});

$counted->all();

// ['gmail.com' => 2, 'yahoo.com' => 1]
```

<a name="method-crossjoin"></a>
#### `crossJoin()`

`crossJoin` 메서드는 주어진 배열이나 컬렉션들과 컬렉션 값을 카르테시안 곱 형태로 모두 조합해 반환합니다:

```
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

더 많은 배열을 인자로 넣을 수도 있습니다.

<a name="method-dd"></a>
#### `dd()`

`dd` 메서드는 컬렉션을 덤프하고, 스크립트 실행을 중단합니다:

```
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

실행 중단 없이 단순 출력만 원하면 [`dump`](#method-dump) 메서드를 사용하세요.

<a name="method-diff"></a>
#### `diff()`

`diff` 메서드는 값 기준으로 다른 배열이나 컬렉션과 비교해 원본 컬렉션에만 있는 값을 반환합니다:

```
$collection = collect([1, 2, 3, 4, 5]);

$diff = $collection->diff([2, 4, 6, 8]);

$diff->all();

// [1, 3, 5]
```

> [!NOTE]  
> [Eloquent Collections](/docs/11.x/eloquent-collections#method-diff) 사용 시 동작이 다릅니다.

<a name="method-diffassoc"></a>
#### `diffAssoc()`

`diffAssoc`는 키와 값을 모두 비교해, 주어진 배열에 없는 키/값 쌍을 반환합니다:

```
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

`diffAssocUsing`는 키 비교 시 사용자 정의 콜백 함수를 사용합니다:

```
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

<a name="method-diffkeys"></a>
#### `diffKeys()`

`diffKeys`는 키 기준으로 비교하여, 주어진 배열에 없는 키/값 쌍을 반환합니다:

```
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

`doesntContain` 메서드는 컬렉션에 주어진 항목이 포함되지 않았는지 확인합니다. 인자로 클로저, 값, 키/값 쌍 모두 받을 수 있습니다:

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->doesntContain(function (int $value, int $key) {
    return $value < 5;
});

// false
```

<a name="method-dot"></a>
#### `dot()`

`dot` 메서드는 다차원 컬렉션을 "dot" 표기법을 사용하는 단일 레벨 컬렉션으로 평탄화합니다:

```
$collection = collect(['products' => ['desk' => ['price' => 100]]]);

$flattened = $collection->dot();

$flattened->all();

// ['products.desk.price' => 100]
```

<a name="method-dump"></a>
#### `dump()`

`dump` 메서드는 컬렉션을 덤프하지만, 실행을 멈추지 않습니다:

```
$collection = collect(['John Doe', 'Jane Doe']);

$collection->dump();
```

실행 중단이 필요한 경우 [`dd`](#method-dd) 메서드를 사용하세요.

<a name="method-duplicates"></a>
#### `duplicates()`

`duplicates` 메서드는 컬렉션 내 중복 값을 찾아 반환합니다:

```
$collection = collect(['a', 'b', 'a', 'c', 'b']);

$collection->duplicates();

// [2 => 'a', 4 => 'b']
```

속성이 있는 배열이나 객체 컬렉션에서는 중복 확인할 속성 키를 지정할 수 있습니다:

```
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

`duplicates`와 시그니처는 같으나 모든 값 비교를 "엄격한(strict)" 비교로 수행합니다.

<a name="method-each"></a>
#### `each()`

`each` 메서드는 컬렉션의 각 항목을 순회하며 클로저를 실행합니다. 클로저 내에서 `false`를 반환하면 순회를 중단할 수 있습니다:

```
$collection = collect([1, 2, 3, 4]);

$collection->each(function (int $item, int $key) {
    // ...
});
```

<a name="method-eachspread"></a>
#### `eachSpread()`

`eachSpread`는 컬렉션의 중첩 배열 각각을 별도의 인수로 클로저에 전달해 호출합니다:

```
$collection = collect([['John Doe', 35], ['Jane Doe', 33]]);

$collection->eachSpread(function (string $name, int $age) {
    // ...
});
```

<a name="method-ensure"></a>
#### `ensure()`

`ensure` 메서드는 컬렉션의 모든 요소가 특정 타입 혹은 타입 목록에 해당하는지 검사합니다. 그렇지 않으면 `UnexpectedValueException`이 발생합니다:

```
return $collection->ensure(User::class);

return $collection->ensure([User::class, Customer::class]);
```

기본 타입도 지정할 수 있습니다:

```
return $collection->ensure('int');
```

> [!WARNING]  
> 이 메서드는 나중에 다른 타입의 요소가 컬렉션에 추가되지 않는다고 보장하지 않습니다.

<a name="method-every"></a>
#### `every()`

`every` 메서드는 컬렉션의 모든 요소가 주어진 진리 검사(truth test)를 통과하는지 확인합니다. 컬렉션이 비어있으면 항상 `true`를 반환합니다:

```
collect([1, 2, 3, 4])->every(function (int $value, int $key) {
    return $value > 2;
});

// false
```

```
collect([])->every(function (int $value, int $key) {
    return $value > 2;
});

// true
```

<a name="method-except"></a>
#### `except()`

`except` 메서드는 지정한 키를 제외한 모든 항목을 반환합니다:

```
$collection = collect(['product_id' => 1, 'price' => 100, 'discount' => false]);

$filtered = $collection->except(['price', 'discount']);

$filtered->all();

// ['product_id' => 1]
```

반대 기능은 [`only`](#method-only) 메서드입니다.

> [!NOTE]  
> [Eloquent Collections](/docs/11.x/eloquent-collections#method-except)에서 동작이 다릅니다.

<a name="method-filter"></a>
#### `filter()`

`filter`는 클로저를 사용해 진리 검사를 통과한 항목만 유지합니다:

```
$collection = collect([1, 2, 3, 4]);

$filtered = $collection->filter(function (int $value, int $key) {
    return $value > 2;
});

$filtered->all();

// [3, 4]
```

콜백이 없으면 PHP에서 false로 평가되는 값을 모두 제거합니다:

```
$collection = collect([1, 2, 3, null, false, '', 0, []]);

$collection->filter()->all();

// [1, 2, 3]
```

반대 기능은 [`reject`](#method-reject)입니다.

<a name="method-first"></a>
#### `first()`

`first` 메서드는 조건에 맞는 첫 번째 요소를 반환합니다. 인자가 없으면 첫 번째 요소를 반환하며, 비었으면 `null`입니다:

```
collect([1, 2, 3, 4])->first(function (int $value, int $key) {
    return $value > 2;
});

// 3

collect([1, 2, 3, 4])->first();

// 1
```

<a name="method-first-or-fail"></a>
#### `firstOrFail()`

`firstOrFail`은 `first`와 같으나, 결과가 없으면 `ItemNotFoundException` 예외를 던집니다:

```
collect([1, 2, 3, 4])->firstOrFail(function (int $value, int $key) {
    return $value > 5;
});

// Throws ItemNotFoundException...
```

<a name="method-first-where"></a>
#### `firstWhere()`

`firstWhere`는 주어진 키/값 쌍과 일치하는 첫 번째 요소를 반환합니다:

```
$collection = collect([
    ['name' => 'Regena', 'age' => null],
    ['name' => 'Linda', 'age' => 14],
    ['name' => 'Diego', 'age' => 23],
    ['name' => 'Linda', 'age' => 84],
]);

$collection->firstWhere('name', 'Linda');

// ['name' => 'Linda', 'age' => 14]
```

비교 연산자를 지정하거나 값이 진리값인 첫 항목을 가져올 수도 있습니다.

<a name="method-flatmap"></a>
#### `flatMap()`

`flatMap` 메서드는 컬렉션 각 값을 콜백에 전달해 수정 후 반환한 컬렉션을 단일 레벨로 평탄화합니다:

```
$collection = collect([
    ['name' => 'Sally'],
    ['school' => 'Arkansas'],
    ['age' => 28]
]);

$flattened = $collection->flatMap(function (array $values) {
    return array_map('strtoupper', $values);
});

$flattened->all();

// ['name' => 'SALLY', 'school' => 'ARKANSAS', 'age' => '28']
```

<a name="method-flatten"></a>
#### `flatten()`

`flatten` 메서드는 다차원 컬렉션을 단일 레벨로 평탄화합니다:

```
$collection = collect([
    'name' => 'taylor',
    'languages' => ['php', 'javascript']
]);

$flattened = $collection->flatten();

$flattened->all();

// ['taylor', 'php', 'javascript']
```

옵션으로 평탄화할 깊이를 지정할 수 있습니다.

<a name="method-flip"></a>
#### `flip()`

`flip` 메서드는 컬렉션의 키와 값을 서로 바꿉니다:

```
$collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

$flipped = $collection->flip();

$flipped->all();

// ['taylor' => 'name', 'laravel' => 'framework']
```

<a name="method-forget"></a>
#### `forget()`

`forget` 메서드는 주어진 키에 해당하는 항목을 컬렉션에서 삭제합니다:

```
$collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

$collection->forget('name');

// ['framework' => 'laravel']
```

여러 키를 배열로 전달할 수도 있습니다.

> [!WARNING]  
> `forget`은 다른 대부분의 컬렉션 메서드와 달리 컬렉션을 직접 수정하며 새 인스턴스를 반환하지 않습니다.

<a name="method-forpage"></a>
#### `forPage()`

`forPage` 메서드는 특정 페이지 번호에 해당하는 항목들만 반환합니다:

```
$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9]);

$chunk = $collection->forPage(2, 3);

$chunk->all();

// [4, 5, 6]
```

<a name="method-get"></a>
#### `get()`

`get` 메서드는 지정한 키의 값을 반환합니다. 키가 없으면 `null`을 반환하거나 기본값을 사용할 수 있습니다:

```
$collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

$value = $collection->get('name');

// taylor
```

<a name="method-groupby"></a>
#### `groupBy()`

`groupBy`는 컬렉션을 주어진 키 혹은 콜백에 따라 그룹화합니다:

```
$collection = collect([
    ['account_id' => 'account-x10', 'product' => 'Chair'],
    ['account_id' => 'account-x10', 'product' => 'Bookcase'],
    ['account_id' => 'account-x11', 'product' => 'Desk'],
]);

$grouped = $collection->groupBy('account_id');

$grouped->all();
```

키 대신 콜백을 넘길 수도 있으며, 다중 기준 그룹화도 지원합니다.

<a name="method-has"></a>
#### `has()`

`has` 메서드는 주어진 키가 컬렉션에 존재하는지 확인합니다:

```
$collection = collect(['account_id' => 1, 'product' => 'Desk', 'amount' => 5]);

$collection->has('product'); // true
```

<a name="method-hasany"></a>
#### `hasAny()`

`hasAny`는 주어진 키 중 하나라도 컬렉션에 존재하는지 확인합니다.

<a name="method-implode"></a>
#### `implode()`

`implode` 메서드는 컬렉션 항목을 문자열로 합칩니다. 배열이나 객체 컬렉션이라면 속성 키와 구분자를 넘겨야 하며, 단순 값 컬렉션이라면 구분자만 넘겨 사용합니다.

<a name="method-intersect"></a>
#### `intersect()`

`intersect` 메서드는 주어진 배열이나 컬렉션과 공통으로 포함된 값을 반환합니다. 원본 키를 보존합니다.

> [!NOTE]  
> [Eloquent Collections]에서 동작이 다릅니다.

<a name="method-intersectusing"></a>
#### `intersectUsing()`

`intersectUsing`은 사용자 정의 콜백으로 값 비교를 수행합니다.

<a name="method-intersectAssoc"></a>
#### `intersectAssoc()`

`intersectAssoc`는 키와 값을 기준으로 공통된 키/값 쌍을 반환합니다.

<a name="method-intersectassocusing"></a>
#### `intersectAssocUsing()`

`intersectAssocUsing`은 키와 값을 사용자 콜백 함수로 정렬해 공통된 키/값 쌍을 반환합니다.

<a name="method-intersectbykeys"></a>
#### `intersectByKeys()`

키만을 기준으로 공통 키/값 쌍을 반환합니다.

<a name="method-isempty"></a>
#### `isEmpty()`

컬렉션이 비어 있으면 `true`를 반환합니다.

<a name="method-isnotempty"></a>
#### `isNotEmpty()`

비어있지 않으면 `true`를 반환합니다.

<a name="method-join"></a>
#### `join()`

아이템 값을 지정한 문자열로 연결합니다. 마지막 결합자 구분자도 지정할 수 있습니다.

<a name="method-keyby"></a>
#### `keyBy()`

`keyBy`는 컬렉션 각각 아이템의 특정 속성 값을 키로 하여 새 컬렉션을 만듭니다. 중복 키가 있으면 마지막 항목만 남습니다.

<a name="method-keys"></a>
#### `keys()`

컬렉션의 모든 키를 반환합니다.

<a name="method-last"></a>
#### `last()`

조건에 맞는 마지막 요소를 반환하거나, 인자가 없으면 마지막 요소를 반환합니다.

<a name="method-lazy"></a>
#### `lazy()`

`lazy` 메서드는 현재 컬렉션의 항목을 기반으로 `LazyCollection` 인스턴스를 생성합니다. 대량 데이터 처리 시 메모리를 절약하는 데 유용합니다.

<a name="method-macro"></a>
#### `macro()`

런타임에 `Collection` 클래스에 사용자 정의 메서드를 추가합니다.

<a name="method-make"></a>
#### `make()`

새 컬렉션 인스턴스를 생성합니다. 자세한 내용은 [컬렉션 생성하기](#creating-collections) 참고.

<a name="method-map"></a>
#### `map()`

각 항목을 콜백에 전달해 변환한 새로운 컬렉션을 반환합니다.

> [!WARNING]  
> `map`은 기존 컬렉션을 변경하지 않고 새 컬렉션을 만듭니다. 원본 변경이 필요하면 [`transform`](#method-transform) 메서드를 사용하세요.

<a name="method-mapinto"></a>
#### `mapInto()`

각 항목을 주어진 클래스 생성자에 전달해 새 인스턴스 컬렉션을 만듭니다.

<a name="method-mapspread"></a>
#### `mapSpread()`

`mapSpread`는 고차원 배열 요소마다 개별 인수를 전달해 콜백을 호출하고 변환 결과의 컬렉션을 만듭니다.

<a name="method-maptogroups"></a>
#### `mapToGroups()`

각 항목을 콜백에 전달해 키/값 쌍으로 그룹화된 새 컬렉션을 만듭니다.

<a name="method-mapwithkeys"></a>
#### `mapWithKeys()`

각 항목을 콜백에 전달해 키가 명시된 배열을 반환하고, 이를 새 컬렉션의 키/값으로 만듭니다.

<a name="method-max"></a>
#### `max()`

주어진 키의 최대값을 반환합니다.

<a name="method-median"></a>
#### `median()`

주어진 키의 [중앙값](https://en.wikipedia.org/wiki/Median)을 반환합니다.

<a name="method-merge"></a>
#### `merge()`

주어진 배열이나 컬렉션을 원본과 병합합니다. 키가 문자열이면 덮어쓰고, 숫자 키면 끝에 추가합니다.

<a name="method-mergerecursive"></a>
#### `mergeRecursive()`

병합을 재귀적으로 수행하며, 키가 같은 문자열은 배열로 병합합니다.

<a name="method-min"></a>
#### `min()`

주어진 키의 최소값을 반환합니다.

<a name="method-mode"></a>
#### `mode()`

주어진 키의 [최빈값(모드)](https://en.wikipedia.org/wiki/Mode_(statistics)) 배열을 반환합니다.

<a name="method-multiply"></a>
#### `multiply()`

컬렉션의 모든 항목을 지정한 횟수만큼 복제해 확장된 컬렉션을 만듭니다.

<a name="method-nth"></a>
#### `nth()`

컬렉션에서 n번째 항목만 포함하는 새 컬렉션을 만듭니다. 시작 오프셋 지정도 가능.

<a name="method-only"></a>
#### `only()`

지정한 키만 포함하는 새 컬렉션을 반환합니다. 반대는 [`except`](#method-except)입니다.

> [!NOTE]  
> [Eloquent Collections]에서 동작이 다릅니다.

<a name="method-pad"></a>
#### `pad()`

배열 크기가 지정한 크기가 될 때까지 지정한 값으로 빈 공간을 채웁니다. 음수 크기면 왼쪽에 채웁니다.

<a name="method-partition"></a>
#### `partition()`

주어진 진리 검사를 통과하는 요소와 통과하지 못하는 요소를 두 그룹으로 분할해 배열로 반환합니다.

<a name="method-percentage"></a>
#### `percentage()`

주어진 진리 테스트를 통과하는 항목 비율을 백분율로 반환합니다.

<a name="method-pipe"></a>
#### `pipe()`

컬렉션을 클로저에 전달하고 그 결과를 반환합니다.

<a name="method-pipeinto"></a>
#### `pipeInto()`

주어진 클래스의 새 인스턴스를 만들고 생성자에 컬렉션을 전달합니다.

<a name="method-pipethrough"></a>
#### `pipeThrough()`

여러 클로저 배열로 컬렉션을 전달하며 각 클로저 결과를 다시 다음 클로저 인자로 넘깁니다.

<a name="method-pluck"></a>
#### `pluck()`

주어진 키의 모든 값을 추출합니다. 키별로 키를 지정할 수도 있고, 점(dot) 표기법도 지원합니다.

<a name="method-pop"></a>
#### `pop()`

컬렉션의 마지막 항목을 꺼내 반환하며, 인자 지정 시 여러 개를 꺼냅니다.

<a name="method-prepend"></a>
#### `prepend()`

컬렉션 앞에 항목을 추가합니다. 두 번째 인자로 키를 지정할 수도 있습니다.

<a name="method-pull"></a>
#### `pull()`

주어진 키의 항목을 컬렉션에서 꺼내 반환합니다.

<a name="method-push"></a>
#### `push()`

항목을 컬렉션 끝에 추가합니다.

<a name="method-put"></a>
#### `put()`

지정한 키/값 쌍을 컬렉션에 넣습니다.

<a name="method-random"></a>
#### `random()`

컬렉션에서 임의 항목을 반환합니다. 인자로 숫자를 주면 여러 항목을 무작위로 반환합니다.

<a name="method-range"></a>
#### `range()`

지정한 범위의 정수 값을 포함하는 컬렉션을 만듭니다.

<a name="method-reduce"></a>
#### `reduce()`

컬렉션 각 요소를 누적하며 단일 값으로 축소합니다. 초기값 지정 가능.

<a name="method-reduce-spread"></a>
#### `reduceSpread()`

`reduce`와 비슷하나 다중 초기값을 허용하며, 각 단계 결과를 배열로 반환해야 합니다.

<a name="method-reject"></a>
#### `reject()`

`filter`의 반대입니다. 주어진 콜백이 `true`를 반환하는 항목을 제거합니다.

<a name="method-replace"></a>
#### `replace()`

`merge`와 유사하나, 숫자 키 항목도 덮어씁니다.

<a name="method-replacerecursive"></a>
#### `replaceRecursive()`

`replace`와 동일하지만 배열 내부까지 재귀적으로 덮어씁니다.

<a name="method-reverse"></a>
#### `reverse()`

컬렉션 아이템 순서를 뒤집습니다. 키는 유지합니다.

<a name="method-search"></a>
#### `search()`

주어진 값을 검색하여 해당 키를 반환합니다. 없으면 `false`를 반환합니다.

<a name="method-select"></a>
#### `select()`

SQL의 SELECT처럼, 주어진 키만 선택하여 컬렉션을 만듭니다.

<a name="method-shift"></a>
#### `shift()`

컬렉션의 첫 항목을 꺼내 반환합니다. 인자로 숫자 주면 여러 항목을 꺼냅니다.

<a name="method-shuffle"></a>
#### `shuffle()`

컬렉션 항목을 무작위로 섞어 반환합니다.

<a name="method-skip"></a>
#### `skip()`

처음부터 지정한 수만큼 항목을 건너뛰고 반환합니다.

<a name="method-skipuntil"></a>
#### `skipUntil()`

콜백이 `true`를 반환할 때까지 항목을 건너뜁니다. 값으로도 지정 가능.

> [!WARNING]  
> 값이 없거나 콜백이 `true`를 반환하지 않으면 빈 컬렉션을 반환합니다.

<a name="method-skipwhile"></a>
#### `skipWhile()`

콜백이 `true`를 반환하는 동안 항목을 건너뛰고 마지막에 남은 항목들을 반환합니다.

> [!WARNING]  
> 콜백이 `false`를 반환하지 않으면 빈 컬렉션을 반환합니다.

<a name="method-slice"></a>
#### `slice()`

지정한 인덱스부터의 슬라이스를 반환합니다. 길이 제한이 가능하며 키는 기본적으로 유지됩니다.

<a name="method-sliding"></a>
#### `sliding()`

컬렉션을 지정한 크기의 “슬라이딩 윈도우” 단위로 나눈 새 컬렉션을 반환합니다.

<a name="method-sole"></a>
#### `sole()`

조건을 만족하는 항목이 유일할 때만 반환합니다. 없거나 여러 개면 예외를 던집니다.

<a name="method-some"></a>
#### `some()`

`contains`의 별칭입니다.

<a name="method-sort"></a>
#### `sort()`

컬렉션을 정렬합니다. 정렬 후 키는 유지하므로 키 재정렬은 [`values`](#method-values) 메서드를 사용하세요.

<a name="method-sortby"></a>
#### `sortBy()`

주어진 키로 컬렉션 항목을 정렬합니다. 정렬 기준으로 콜백과 정렬 플래그도 전달 가능합니다.

<a name="method-sortbydesc"></a>
#### `sortByDesc()`

`sortBy`와 동일하지만 내림차순 정렬합니다.

<a name="method-sortdesc"></a>
#### `sortDesc()`

`sort`와 동일하지만 내림차순 정렬합니다.

<a name="method-sortkeys"></a>
#### `sortKeys()`

연관 배열의 키를 기준으로 정렬합니다.

<a name="method-sortkeysdesc"></a>
#### `sortKeysDesc()`

`sortKeys`와 같으나 내림차순입니다.

<a name="method-sortkeysusing"></a>
#### `sortKeysUsing()`

사용자 지정 비교 함수를 사용해 키 기준 정렬합니다.

<a name="method-splice"></a>
#### `splice()`

지정한 위치부터 항목 일부를 잘라내 반환합니다. 교체용 새 항목도 지정할 수 있습니다.

<a name="method-split"></a>
#### `split()`

컬렉션을 지정한 개수만큼 그룹으로 나눕니다.

<a name="method-splitin"></a>
#### `splitIn()`

그룹을 균등하게 채우면서 컬렉션을 지정한 개수 그룹으로 나눕니다.

<a name="method-sum"></a>
#### `sum()`

모든 항목 합계를 반환합니다. 키나 콜백으로 어떤 값을 더할지 지정 가능.

<a name="method-take"></a>
#### `take()`

지정한 개수만큼 컬렉션을 반환합니다. 음수면 뒤에서부터 반환합니다.

<a name="method-takeuntil"></a>
#### `takeUntil()`

콜백이 `true`를 반환할 때까지 항목을 포함해 반환합니다.

> [!WARNING]  
> 값이 없거나 콜백이 `true`를 반환하지 않으면 모든 항목을 반환합니다.

<a name="method-takewhile"></a>
#### `takeWhile()`

콜백이 `false`를 반환할 때까지 항목을 포함해 반환합니다.

> [!WARNING]  
> 콜백이 `false`를 반환하지 않으면 모든 항목을 반환합니다.

<a name="method-tap"></a>
#### `tap()`

컬렉션을 클로저에 전달해 중간에 관찰 혹은 조작하고, 원본 컬렉션을 그대로 반환합니다.

<a name="method-times"></a>
#### `times()`

통계적인 용도로, 주어진 숫자만큼 클로저를 호출해 새 컬렉션을 만듭니다.

<a name="method-toarray"></a>
#### `toArray()`

컬렉션을 배열로 변환합니다. 내부 `Arrayable` 객체까지 재귀적으로 배열로 변환합니다.

> [!WARNING]  
> 순수 PHP 배열을 원하면 [`all`](#method-all) 메서드를 사용하세요.

<a name="method-tojson"></a>
#### `toJson()`

컬렉션을 JSON 문자열로 변환합니다.

<a name="method-transform"></a>
#### `transform()`

각 항목을 클로저에 전달해 직접 컬렉션을 변환(수정)합니다.

> [!WARNING]  
> `transform`은 컬렉션 자체를 수정합니다. 새 컬렉션이 필요하면 [`map`](#method-map) 사용.

<a name="method-undot"></a>
#### `undot()`

"dot" 표기법으로 표현된 단일 차원 컬렉션을 다중 차원 컬렉션으로 확장합니다.

<a name="method-union"></a>
#### `union()`

주어진 배열을 컬렉션에 합칩니다. 키가 충돌하면 원본 컬렉션 값을 우선합니다.

<a name="method-unique"></a>
#### `unique()`

중복을 제거한 유일한 항목들의 컬렉션을 반환합니다.

<a name="method-uniquestrict"></a>
#### `uniqueStrict()`

`unique`와 같으나, "엄격한" 비교 방식으로 중복 제거합니다.

<a name="method-unless"></a>
#### `unless()`

첫 인자가 `true`일 때는 실행하지 않고, `false`일 때 주어진 콜백을 실행합니다. 두 번째 콜백은 첫 인자가 `true`일 때 실행합니다.

<a name="method-unlessempty"></a>
#### `unlessEmpty()`

[`whenNotEmpty`](#method-whennotempty) 메서드의 별칭입니다.

<a name="method-unlessnotempty"></a>
#### `unlessNotEmpty()`

[`whenEmpty`](#method-whenempty) 메서드의 별칭입니다.

<a name="method-unwrap"></a>
#### `unwrap()`

`Collection` 인스턴스일 경우 내부 항목을, 배열이나 단일 값이면 그대로 반환합니다.

<a name="method-value"></a>
#### `value()`

컬렉션의 첫 번째 요소에서 지정한 키의 값을 반환합니다.

<a name="method-values"></a>
#### `values()`

키가 연속된 정수로 리셋된 새 컬렉션을 생성합니다.

<a name="method-when"></a>
#### `when()`

첫 인자가 `true`일 때 콜백을 실행하고, `false`일 때 대체 콜백을 실행합니다.

<a name="method-whenempty"></a>
#### `whenEmpty()`

컬렉션이 비었을 때 콜백을 실행합니다. 대체 콜백도 지정 가능합니다.

<a name="method-whennotempty"></a>
#### `whenNotEmpty()`

컬렉션이 비어있지 않을 때 콜백을 실행합니다. 대체 콜백도 지정 가능합니다.

<a name="method-where"></a>
#### `where()`

주어진 키/값 쌍에 맞는 항목만 필터링합니다. 느슨한 비교를 사용하며, 비교 연산자 지정도 가능합니다.

<a name="method-wherestrict"></a>
#### `whereStrict()`

`where`와 같으나, 엄격한 비교를 사용합니다.

<a name="method-wherebetween"></a>
#### `whereBetween()`

주어진 범위 내 값에 해당하는 항목만 필터링합니다.

<a name="method-wherein"></a>
#### `whereIn()`

지정한 값 배열에 포함되는 항목만 반환합니다. 느슨한 비교를 사용합니다.

<a name="method-whereinstrict"></a>
#### `whereInStrict()`

`whereIn`과 같으나 엄격한 비교를 사용합니다.

<a name="method-whereinstanceof"></a>
#### `whereInstanceOf()`

특정 클래스 인스턴스인 항목만 필터링합니다.

<a name="method-wherenotbetween"></a>
#### `whereNotBetween()`

범위 밖에 속하는 항목만 필터링합니다.

<a name="method-wherenotin"></a>
#### `whereNotIn()`

지정한 값 배열에 포함되지 않는 항목만 반환합니다.

<a name="method-wherenotinstrict"></a>
#### `whereNotInStrict()`

`whereNotIn`과 같으나 엄격한 비교방식을 사용합니다.

<a name="method-wherenotnull"></a>
#### `whereNotNull()`

지정한 키의 값이 `null`이 아닌 항목만 반환합니다.

<a name="method-wherenull"></a>
#### `whereNull()`

지정한 키의 값이 `null`인 항목만 반환합니다.

<a name="method-wrap"></a>
#### `wrap()`

값을 감싸서 컬렉션으로 만듭니다. 컬렉션일 경우 내부 항목을 반환합니다.

<a name="method-zip"></a>
#### `zip()`

주어진 배열과 인덱스를 기준으로 원본 컬렉션과 병합해 튜플 배열 컬렉션으로 만듭니다.

<a name="higher-order-messages"></a>
## 고차 메시지 (Higher Order Messages)

컬렉션은 반복적 액션을 간략히 표현할 수 있는 "고차 메시지"도 지원합니다. 예를 들어, `each` 메서드에 고차 메시지를 사용하면 컬렉션 내 객체 각각에 메서드 호출이 가능합니다:

```
use App\Models\User;

$users = User::where('votes', '>', 500)->get();

$users->each->markAsVip();
```

총합 같은 경우도 고차 메시지로 간결히 작성할 수 있습니다:

```
$users = User::where('group', 'Development')->get();

return $users->sum->votes;
```

<a name="lazy-collections"></a>
## 지연 컬렉션 (Lazy Collections)

<a name="lazy-collection-introduction"></a>
### 소개 (Introduction)

> [!WARNING]  
> Laravel의 지연 컬렉션을 배우기 전에, [PHP 생성기(generators)](https://www.php.net/manual/en/language.generators.overview.php)를 미리 숙지하세요.

`LazyCollection` 클래스는 PHP의 생성기를 활용하여 메모리를 적게 사용하면서도 매우 큰 데이터셋을 다룰 수 있게 합니다.

예를 들어, 수 기가바이트에 달하는 로그 파일을 처리하면서 컬렉션 메서드를 사용해야 한다고 가정해봅시다. 로그 파일 전체를 메모리에 올리는 대신, 지연 컬렉션을 사용해 한 번에 파일 일부만 메모리에 보관하며 처리할 수 있습니다:

```
use App\Models\LogEntry;
use Illuminate\Support\LazyCollection;

LazyCollection::make(function () {
    $handle = fopen('log.txt', 'r');

    while (($line = fgets($handle)) !== false) {
        yield $line;
    }
})->chunk(4)->map(function (array $lines) {
    return LogEntry::fromLines($lines);
})->each(function (LogEntry $logEntry) {
    // 로그 엔트리 처리...
});
```

또는 10,000개 Eloquent 모델을 순회할 때 기존 컬렉션은 모두 메모리에 올려야 하지만,

```
use App\Models\User;

$users = User::all()->filter(function (User $user) {
    return $user->id > 500;
});
```

`cursor`로 받은 `LazyCollection`은 메모리 부담 없이 하나씩 로드합니다:

```
use App\Models\User;

$users = User::cursor()->filter(function (User $user) {
    return $user->id > 500;
});

foreach ($users as $user) {
    echo $user->id;
}
```

<a name="creating-lazy-collections"></a>
### 지연 컬렉션 생성하기 (Creating Lazy Collections)

지연 컬렉션을 생성하려면 PHP 생성기 함수를 `make` 메서드에 전달하세요:

```
use Illuminate\Support\LazyCollection;

LazyCollection::make(function () {
    $handle = fopen('log.txt', 'r');

    while (($line = fgets($handle)) !== false) {
        yield $line;
    }
});
```

<a name="the-enumerable-contract"></a>
### Enumerable 계약 (The Enumerable Contract)

`Collection` 클래스의 거의 모든 메서드는 `LazyCollection`에서도 사용 가능하며, 두 클래스 모두 `Illuminate\Support\Enumerable` 계약을 구현합니다.

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
> `shift`, `pop`, `prepend` 등 컬렉션을 직접 변경하는 메서드는 `LazyCollection`에 없습니다.

<a name="lazy-collection-methods"></a>
### 지연 컬렉션 메서드 (Lazy Collection Methods)

`Enumerable` 계약에 추가로 `LazyCollection` 클래스는 아래 메서드가 있습니다:

<a name="method-takeUntilTimeout"></a>
#### `takeUntilTimeout()`

지정한 시간까지 항목을 열거하고 이후 멈추는 지연 컬렉션을 반환합니다:

```
$lazyCollection = LazyCollection::times(INF)
    ->takeUntilTimeout(now()->addMinute());

$lazyCollection->each(function (int $number) {
    dump($number);

    sleep(1);
});
```

<a name="method-tapEach"></a>
#### `tapEach()`

`each`는 즉시 콜백을 수행하지만, `tapEach`는 항목이 실제로 소비될 때 콜백을 실행합니다:

```
$lazyCollection = LazyCollection::times(INF)->tapEach(function (int $value) {
    dump($value);
});

$array = $lazyCollection->take(3)->all();

// 1
// 2
// 3
```

<a name="method-throttle"></a>
#### `throttle()`

주어진 초 단위로 결과를 반환 속도 제한(throttle)하는 지연 컬렉션을 만듭니다. API 요청 등 외부 제한이 있는 경우 유용합니다:

```
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

열거한 값을 기억해 다음 열거 시 재요청하지 않는 지연 컬렉션을 생성합니다:

```
$users = User::cursor()->remember();

$users->take(5)->all();

$users->take(20)->all();
```
