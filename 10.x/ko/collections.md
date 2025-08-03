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
## 소개

`Illuminate\Support\Collection` 클래스는 데이터 배열을 편리하고 유연하게 다룰 수 있는 래퍼를 제공합니다. 예를 들어, 아래 코드를 확인하세요. `collect` 헬퍼를 사용해 배열로부터 새로운 컬렉션 인스턴스를 생성하고, 각 요소에 `strtoupper` 함수를 적용한 뒤 빈 요소를 모두 제거합니다:

```
$collection = collect(['taylor', 'abigail', null])->map(function (?string $name) {
    return strtoupper($name);
})->reject(function (string $name) {
    return empty($name);
});
```

보시다시피 `Collection` 클래스는 메서드 체이닝을 지원하여 기본 배열에 대해 유창한 매핑과 축소를 수행할 수 있습니다. 일반적으로 컬렉션은 불변(immutable)이며, 모든 `Collection` 메서드는 완전히 새로운 `Collection` 인스턴스를 반환합니다.

<a name="creating-collections"></a>
### 컬렉션 생성하기

앞서 언급했듯이, `collect` 헬퍼는 주어진 배열로부터 새로운 `Illuminate\Support\Collection` 인스턴스를 반환합니다. 따라서 컬렉션 생성은 매우 간단합니다:

```
$collection = collect([1, 2, 3]);
```

> [!NOTE]  
> [Eloquent](/docs/10.x/eloquent) 쿼리 결과는 항상 `Collection` 인스턴스로 반환됩니다.

<a name="extending-collections"></a>
### 컬렉션 확장하기

컬렉션은 "macroable"하며, 런타임에 `Collection` 클래스에 추가 메서드를 더할 수 있습니다. `Illuminate\Support\Collection` 클래스의 `macro` 메서드는 매크로 호출 시 실행될 클로저를 인수로 받습니다. 이 매크로 클로저는 마치 컬렉션 클래스의 실제 메서드처럼 `$this`를 통해 컬렉션의 다른 메서드에 접근할 수 있습니다. 예를 들어, 아래 코드는 `Collection` 클래스에 `toUpper` 메서드를 추가합니다:

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

일반적으로 컬렉션 매크로는 [서비스 프로바이더](/docs/10.x/providers)의 `boot` 메서드 내에서 선언하는 것이 좋습니다.

<a name="macro-arguments"></a>
#### 매크로 인수

필요에 따라, 매크로가 추가 인수를 받을 수 있도록 정의할 수 있습니다:

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
## 사용 가능한 메서드

컬렉션 문서 대부분은 `Collection` 클래스에 존재하는 각 메서드에 대해 설명합니다. 모든 메서드는 체인할 수 있어 기본 배열을 유창하게 조작할 수 있습니다. 또한 거의 모든 메서드는 새로운 `Collection` 인스턴스를 반환해 원본 컬렉션 복사본을 유지할 수 있도록 합니다:



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
[intersectAssoc](#method-intersectAssoc)
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



<a name="method-all"></a>
#### `all()`

`all` 메서드는 컬렉션이 감싸고 있는 기본 배열을 반환합니다:

```
collect([1, 2, 3])->all();

// [1, 2, 3]
```

<a name="method-average"></a>
#### `average()`

[`avg`](#method-avg) 메서드의 별칭입니다.

<a name="method-avg"></a>
#### `avg()`

`avg` 메서드는 주어진 키에 대한 [평균값](https://en.wikipedia.org/wiki/Average)을 반환합니다:

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

<a name="method-chunk"></a>
#### `chunk()`

`chunk` 메서드는 컬렉션을 지정한 크기의 여러 작은 컬렉션으로 나눕니다:

```
$collection = collect([1, 2, 3, 4, 5, 6, 7]);

$chunks = $collection->chunk(4);

$chunks->all();

// [[1, 2, 3, 4], [5, 6, 7]]
```

이 메서드는 [Bootstrap](https://getbootstrap.com/docs/4.1/layout/grid/)과 같은 그리드 시스템과 함께 [뷰](/docs/10.x/views)에서 특히 유용합니다. 예를 들어, [Eloquent](/docs/10.x/eloquent) 모델의 컬렉션을 그리드 형태로 보여주고 싶다면:

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

`chunkWhile` 메서드는 주어진 콜백 평가에 따라 컬렉션을 여러 작은 컬렉션으로 나눕니다. 클로저에 전달된 `$chunk` 변수로 이전 요소를 확인할 수 있습니다:

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

`collapse` 메서드는 배열 컬렉션을 하나의 평탄한(flat) 컬렉션으로 합칩니다:

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

<a name="method-collect"></a>
#### `collect()`

`collect` 메서드는 현재 컬렉션에 있는 아이템으로 새로운 `Collection` 인스턴스를 반환합니다:

```
$collectionA = collect([1, 2, 3]);

$collectionB = $collectionA->collect();

$collectionB->all();

// [1, 2, 3]
```

이 메서드는 주로 [지연 컬렉션](#lazy-collections)을 표준 `Collection`으로 변환할 때 유용합니다:

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
> 이 메서드는 `Enumerable` 계약의 일부로, `Enumerable` 인스턴스가 있을 때 비지연(non-lazy) 컬렉션 인스턴스를 얻는 데 유용합니다.

<a name="method-combine"></a>
#### `combine()`

`combine` 메서드는 컬렉션의 값을 키로, 다른 배열 또는 컬렉션의 값을 값으로 하여 결합합니다:

```
$collection = collect(['name', 'age']);

$combined = $collection->combine(['George', 29]);

$combined->all();

// ['name' => 'George', 'age' => 29]
```

<a name="method-concat"></a>
#### `concat()`

`concat` 메서드는 주어진 배열이나 컬렉션의 값을 또 다른 컬렉션의 끝에 덧붙입니다:

```
$collection = collect(['John Doe']);

$concatenated = $collection->concat(['Jane Doe'])->concat(['name' => 'Johnny Doe']);

$concatenated->all();

// ['John Doe', 'Jane Doe', 'Johnny Doe']
```

`concat` 메서드는 덧붙이는 아이템들의 키를 숫자로 다시 인덱싱합니다. 연관 컬렉션에서 키를 유지하려면 [merge](#method-merge) 메서드를 사용하세요.

<a name="method-contains"></a>
#### `contains()`

`contains` 메서드는 컬렉션이 주어진 아이템을 포함하는지 확인합니다. 콜백을 전달하면 조건 검사에 따라 존재 여부를 판단할 수 있습니다:

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->contains(function (int $value, int $key) {
    return $value > 5;
});

// false
```

문자열을 전달하면 해당 값이 컬렉션에 있는지 검사합니다:

```
$collection = collect(['name' => 'Desk', 'price' => 100]);

$collection->contains('Desk');

// true

$collection->contains('New York');

// false
```

키/값 쌍을 전달할 수도 있습니다:

```
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
]);

$collection->contains('product', 'Bookcase');

// false
```

값 비교는 "느슨한(loose)" 비교를 사용하며, 정수와 같은 값의 문자열도 동일하게 간주합니다. 엄격한(strict) 검사가 필요할 때는 [`containsStrict`](#method-containsstrict)를 사용하세요.

반대 동작은 [doesntContain](#method-doesntcontain) 메서드를 참고하세요.

<a name="method-containsoneitem"></a>
#### `containsOneItem()`

`containsOneItem` 메서드는 컬렉션에 단 하나의 아이템이 포함되어 있는지 판단합니다:

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

`contains` 메서드와 동일한 서명을 가지며, 모든 값 비교가 엄격하게 수행됩니다.

> [!NOTE]  
> 이 메서드는 [Eloquent 컬렉션](/docs/10.x/eloquent-collections#method-contains)에서 동작 방식이 다릅니다.

<a name="method-count"></a>
#### `count()`

`count` 메서드는 컬렉션 내 아이템 개수를 반환합니다:

```
$collection = collect([1, 2, 3, 4]);

$collection->count();

// 4
```

<a name="method-countBy"></a>
#### `countBy()`

`countBy` 메서드는 컬렉션 내 값들의 등장 횟수를 셉니다. 기본적으로 모든 값의 출현 빈도를 세어 특정 "타입"이 얼마나 있는지 셀 수 있습니다:

```
$collection = collect([1, 2, 2, 2, 3]);

$counted = $collection->countBy();

$counted->all();

// [1 => 1, 2 => 3, 3 => 1]
```

클로저를 전달해 커스텀 값을 기준으로 셀 수도 있습니다:

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

`crossJoin` 메서드는 컬렉션의 값과 주어진 배열 또는 컬렉션들의 값을 곱집합(Cartesian product) 형태로 조합하여 모든 가능한 순열을 반환합니다:

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

`dd` 메서드는 컬렉션의 아이템을 덤프(dump)하고 스크립트 실행을 종료합니다:

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

스크립트 실행을 멈추지 않으려면 [`dump`](#method-dump) 메서드를 사용하세요.

<a name="method-diff"></a>
#### `diff()`

`diff` 메서드는 값 기준으로 비교하여, 주어진 컬렉션 또는 배열에 없는 원본 컬렉션의 값을 반환합니다:

```
$collection = collect([1, 2, 3, 4, 5]);

$diff = $collection->diff([2, 4, 6, 8]);

$diff->all();

// [1, 3, 5]
```

> [!NOTE]  
> 이 메서드는 [Eloquent 컬렉션](/docs/10.x/eloquent-collections#method-diff)에서 동작 방식이 다릅니다.

<a name="method-diffassoc"></a>
#### `diffAssoc()`

`diffAssoc` 메서드는 키와 값을 기준으로 비교하여, 주어진 컬렉션이나 배열에 없는 원본 컬렉션의 키/값 쌍을 반환합니다:

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

`diffAssocUsing` 메서드는 키 비교를 위해 사용자 정의 콜백 함수를 받습니다:

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

콜백은 비교 함수로, 0보다 작거나, 같거나, 크기를 정수로 반환해야 합니다. 자세한 내용은 PHP의 [`array_diff_uassoc`](https://www.php.net/array_diff_uassoc#refsect1-function.array-diff-uassoc-parameters) 문서를 참고하세요.

<a name="method-diffkeys"></a>
#### `diffKeys()`

`diffKeys` 메서드는 키 기준으로 비교하여, 주어진 컬렉션이나 배열에 없는 원본 컬렉션의 키/값 쌍을 반환합니다:

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

`doesntContain` 메서드는 컬렉션이 주어진 아이템을 포함하지 않는지 판단합니다. 콜백을 전달하여 조건 검사를 할 수 있습니다:

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->doesntContain(function (int $value, int $key) {
    return $value < 5;
});

// false
```

문자열을 전달해 값 존재 여부를 확인할 수도 있습니다:

```
$collection = collect(['name' => 'Desk', 'price' => 100]);

$collection->doesntContain('Table');

// true

$collection->doesntContain('Desk');

// false
```

키/값 쌍을 전달할 수도 있습니다:

```
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
]);

$collection->doesntContain('product', 'Bookcase');

// true
```

값 비교는 "느슨한(loose)" 비교로 수행합니다.

<a name="method-dot"></a>
#### `dot()`

`dot` 메서드는 다차원 컬렉션을 "dot" 표기법을 사용해 단일 키로 평탄화(flatten)합니다:

```
$collection = collect(['products' => ['desk' => ['price' => 100]]]);

$flattened = $collection->dot();

$flattened->all();

// ['products.desk.price' => 100]
```

<a name="method-dump"></a>
#### `dump()`

`dump` 메서드는 컬렉션 아이템을 덤프합니다:

```
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

스크립트 중단을 원하면 [`dd`](#method-dd) 메서드를 사용하세요.

<a name="method-duplicates"></a>
#### `duplicates()`

`duplicates` 메서드는 컬렉션에서 중복된 값을 찾아 반환합니다:

```
$collection = collect(['a', 'b', 'a', 'c', 'b']);

$collection->duplicates();

// [2 => 'a', 4 => 'b']
```

배열이나 객체가 포함된 컬렉션에 대해서는, 중복 확인할 속성 키를 지정할 수 있습니다:

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

`duplicates` 메서드와 동일한 서명을 갖지만, 모든 값 비교가 엄격하게 수행됩니다.

<a name="method-each"></a>
#### `each()`

`each` 메서드는 컬렉션의 각 아이템을 반복하며, 각 아이템을 클로저에 전달합니다:

```
$collection = collect([1, 2, 3, 4]);

$collection->each(function (int $item, int $key) {
    // ...
});
```

반복을 중단하고 싶으면 클로저에서 `false`를 반환하세요:

```
$collection->each(function (int $item, int $key) {
    if (/* condition */) {
        return false;
    }
});
```

<a name="method-eachspread"></a>
#### `eachSpread()`

`eachSpread` 메서드는 각 중첩된 아이템 값을 클로저에 펼쳐 인수로 전달합니다:

```
$collection = collect([['John Doe', 35], ['Jane Doe', 33]]);

$collection->eachSpread(function (string $name, int $age) {
    // ...
});
```

`false` 반환으로 반복 중단 가능:

```
$collection->eachSpread(function (string $name, int $age) {
    return false;
});
```

<a name="method-ensure"></a>
#### `ensure()`

`ensure` 메서드는 컬렉션 내 모든 요소가 주어진 타입 또는 타입 목록에 속하는지를 검증합니다. 그렇지 않으면 `UnexpectedValueException` 예외가 발생합니다:

```
return $collection->ensure(User::class);

return $collection->ensure([User::class, Customer::class]);
```

`string`, `int`, `float`, `bool`, `array` 같은 원시 타입도 지정 가능합니다:

```
return $collection->ensure('int');
```

> [!WARNING]  
> `ensure` 메서드는 추후에 다른 타입의 요소가 컬렉션에 추가되지 않음을 보장하지 않습니다.

<a name="method-every"></a>
#### `every()`

`every` 메서드는 컬렉션 내 모든 요소가 주어진 조건을 만족하는지를 검사합니다:

```
collect([1, 2, 3, 4])->every(function (int $value, int $key) {
    return $value > 2;
});

// false
```

빈 컬렉션일 경우 `true`를 반환합니다:

```
$collection = collect([]);

$collection->every(function (int $value, int $key) {
    return $value > 2;
});

// true
```

<a name="method-except"></a>
#### `except()`

`except` 메서드는 지정된 키를 제외한 모든 아이템을 반환합니다:

```
$collection = collect(['product_id' => 1, 'price' => 100, 'discount' => false]);

$filtered = $collection->except(['price', 'discount']);

$filtered->all();

// ['product_id' => 1]
```

반대 동작은 [only](#method-only) 메서드를 참고하세요.

> [!NOTE]  
> 이 메서드는 [Eloquent 컬렉션](/docs/10.x/eloquent-collections#method-except)에서 다르게 동작할 수 있습니다.

<a name="method-filter"></a>
#### `filter()`

`filter` 메서드는 주어진 조건에 맞는 아이템만 남겨 나머지를 제거합니다:

```
$collection = collect([1, 2, 3, 4]);

$filtered = $collection->filter(function (int $value, int $key) {
    return $value > 2;
});

$filtered->all();

// [3, 4]
```

콜백이 없으면, `false`에 해당하는 값들을 모두 제거합니다:

```
$collection = collect([1, 2, 3, null, false, '', 0, []]);

$collection->filter()->all();

// [1, 2, 3]
```

반대 동작은 [reject](#method-reject) 메서드를 참고하세요.

<a name="method-first"></a>
#### `first()`

`first` 메서드는 주어진 조건을 만족하는 첫 번째 요소를 반환합니다:

```
collect([1, 2, 3, 4])->first(function (int $value, int $key) {
    return $value > 2;
});

// 3
```

인수를 주지 않으면 첫 번째 요소를 반환하며, 컬렉션이 비어있으면 `null`을 반환합니다:

```
collect([1, 2, 3, 4])->first();

// 1
```

<a name="method-first-or-fail"></a>
#### `firstOrFail()`

`first` 메서드와 동일하나, 결과가 없으면 `Illuminate\Support\ItemNotFoundException` 예외를 던집니다:

```
collect([1, 2, 3, 4])->firstOrFail(function (int $value, int $key) {
    return $value > 5;
});

// ItemNotFoundException 발생
```

인수가 없을 때도 마찬가지입니다:

```
collect([])->firstOrFail();

// ItemNotFoundException 발생
```

<a name="method-first-where"></a>
#### `firstWhere()`

`firstWhere` 메서드는 주어진 키/값 쌍과 일치하는 첫 번째 요소를 반환합니다:

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

비교 연산자도 지정할 수 있습니다:

```
$collection->firstWhere('age', '>=', 18);

// ['name' => 'Diego', 'age' => 23]
```

인수를 하나만 전달하면, 그 키가 "참(truthy)"인 첫 번째 요소를 반환합니다:

```
$collection->firstWhere('age');

// ['name' => 'Linda', 'age' => 14]
```

<a name="method-flatmap"></a>
#### `flatMap()`

`flatMap` 메서드는 각 요소를 전달받은 클로저에 처리시키고, 반환된 배열을 1단계 평탄화하여 새로운 컬렉션을 생성합니다:

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

// ['name' => 'SALLY', 'school' => 'ARKANSAS', 'age' => '28'];
```

<a name="method-flatten"></a>
#### `flatten()`

`flatten` 메서드는 다차원 컬렉션을 단일 차원으로 평탄화합니다:

```
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

깊이(depth)를 인수로 지정할 수도 있습니다:

```
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

깊이를 지정하지 않으면 완전히 평탄화됩니다.

<a name="method-flip"></a>
#### `flip()`

`flip` 메서드는 컬렉션의 키와 값을 서로 뒤바꿉니다:

```
$collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

$flipped = $collection->flip();

$flipped->all();

// ['taylor' => 'name', 'laravel' => 'framework']
```

<a name="method-forget"></a>
#### `forget()`

`forget` 메서드는 지정한 키에 해당하는 아이템을 컬렉션에서 제거합니다:

```
$collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

$collection->forget('name');

$collection->all();

// ['framework' => 'laravel']
```

> [!WARNING]  
> `forget` 메서드는 대부분 컬렉션 메서드와 달리 새로운 컬렉션을 반환하지 않고 원본 컬렉션을 직접 수정합니다.

<a name="method-forpage"></a>
#### `forPage()`

`forPage` 메서드는 특정 페이지 번호에 해당하는 아이템만 포함하는 새 컬렉션을 반환합니다. 첫 번째 인수는 페이지 번호, 두 번째 인수는 페이지당 아이템 수입니다:

```
$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9]);

$chunk = $collection->forPage(2, 3);

$chunk->all();

// [4, 5, 6]
```

<a name="method-get"></a>
#### `get()`

`get` 메서드는 주어진 키의 아이템 값을 반환하며, 키가 없으면 기본적으로 `null`을 반환합니다:

```
$collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

$value = $collection->get('name');

// taylor
```

기본값을 두 번째 인수로 지정할 수 있습니다:

```
$value = $collection->get('age', 34);

// 34
```

콜백을 기본값으로 지정하면, 키가 없을 때 콜백 결과를 반환합니다:

```
$collection->get('email', function () {
    return 'taylor@example.com';
});

// taylor@example.com
```

<a name="method-groupby"></a>
#### `groupBy()`

`groupBy` 메서드는 주어진 키를 기준으로 컬렉션의 아이템을 그룹화합니다:

```
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

키 대신 콜백을 사용할 수도 있습니다:

```
$grouped = $collection->groupBy(function (array $item, int $key) {
    return substr($item['account_id'], -3);
});

$grouped->all();

/*
    [
        'x10' => [...],
        'x11' => [...],
    ]
*/
```

여러 레벨로 그룹화하려면 배열을 넘길 수 있습니다:

```
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
        'Role_1' => [...],
        'Role_2' => [...],
        'Role_3' => [...],
    ],
    2 => [
        'Role_1' => [...],
        'Role_2' => [...],
    ],
];
*/
```

<a name="method-has"></a>
#### `has()`

`has` 메서드는 주어진 키가 컬렉션에 존재하는지 확인합니다:

```
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

`hasAny` 메서드는 주어진 키 중 하나라도 컬렉션에 존재하는지 확인합니다:

```
$collection = collect(['account_id' => 1, 'product' => 'Desk', 'amount' => 5]);

$collection->hasAny(['product', 'price']);

// true

$collection->hasAny(['name', 'price']);

// false
```

<a name="method-implode"></a>
#### `implode()`

`implode` 메서드는 컬렉션 아이템을 문자열로 연결합니다. 컬렉션이 배열이나 객체를 포함하면, 연결할 속성 키와 구분 문자열을 제공합니다:

```
$collection = collect([
    ['account_id' => 1, 'product' => 'Desk'],
    ['account_id' => 2, 'product' => 'Chair'],
]);

$collection->implode('product', ', ');

// Desk, Chair
```

단순 문자열 또는 숫자 배열일 경우 구분자만 넘기면 됩니다:

```
collect([1, 2, 3, 4, 5])->implode('-');

// '1-2-3-4-5'
```

값 포맷팅을 위해 클로저를 넘길 수도 있습니다:

```
$collection->implode(function (array $item, int $key) {
    return strtoupper($item['product']);
}, ', ');

// DESK, CHAIR
```

<a name="method-intersect"></a>
#### `intersect()`

`intersect` 메서드는 원래 컬렉션에 존재하되, 주어진 배열이나 컬렉션에 존재하는 값만 남깁니다. 원본 키는 유지됩니다:

```
$collection = collect(['Desk', 'Sofa', 'Chair']);

$intersect = $collection->intersect(['Desk', 'Chair', 'Bookcase']);

$intersect->all();

// [0 => 'Desk', 2 => 'Chair']
```

> [!NOTE]  
> 이 메서드는 [Eloquent 컬렉션](/docs/10.x/eloquent-collections#method-intersect)에서 다르게 동작할 수 있습니다.

<a name="method-intersectAssoc"></a>
#### `intersectAssoc()`

`intersectAssoc` 메서드는 키와 값 모두를 비교하여 주어진 컬렉션/배열에 모두 존재하는 키/값 쌍을 반환합니다:

```
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

<a name="method-intersectbykeys"></a>
#### `intersectByKeys()`

`intersectByKeys` 메서드는 주어진 배열/컬렉션에 키가 존재하는 원본 아이템만 남깁니다:

```
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

컬렉션이 비어있으면 `true`를, 그렇지 않으면 `false`를 반환합니다:

```
collect([])->isEmpty();

// true
```

<a name="method-isnotempty"></a>
#### `isNotEmpty()`

컬렉션이 비어있지 않으면 `true`를, 그렇지 않으면 `false`를 반환합니다:

```
collect([])->isNotEmpty();

// false
```

<a name="method-join"></a>
#### `join()`

`join` 메서드는 컬렉션 값을 문자열로 결합합니다. 두 번째 인수로 마지막 요소를 어떻게 붙일지도 지정할 수 있습니다:

```
collect(['a', 'b', 'c'])->join(', '); // 'a, b, c'
collect(['a', 'b', 'c'])->join(', ', ', and '); // 'a, b, and c'
collect(['a', 'b'])->join(', ', ' and '); // 'a and b'
collect(['a'])->join(', ', ' and '); // 'a'
collect([])->join(', ', ' and '); // ''
```

<a name="method-keyby"></a>
#### `keyBy()`

`keyBy` 메서드는 주어진 키를 기준으로 컬렉션의 키를 설정합니다. 동일한 키가 여러 개 있을 경우 마지막 항목만 남깁니다:

```
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

```
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

컬렉션의 모든 키를 반환합니다:

```
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

`last` 메서드는 주어진 조건을 만족하는 마지막 요소를 반환합니다:

```
collect([1, 2, 3, 4])->last(function (int $value, int $key) {
    return $value < 3;
});

// 2
```

인수 없이 호출하면 마지막 요소를 반환합니다(빈 컬렉션은 `null`):

```
collect([1, 2, 3, 4])->last();

// 4
```

<a name="method-lazy"></a>
#### `lazy()`

`lazy` 메서드는 기본 아이템 배열에서 새로운 [`LazyCollection`](#lazy-collections) 인스턴스를 반환합니다:

```
$lazyCollection = collect([1, 2, 3, 4])->lazy();

$lazyCollection::class;

// Illuminate\Support\LazyCollection

$lazyCollection->all();

// [1, 2, 3, 4]
```

대용량 `Collection`에 대해 변환 작업을 수행할 때 유용합니다:

```
$count = $hugeCollection
    ->lazy()
    ->where('country', 'FR')
    ->where('balance', '>', '100')
    ->count();
```

`LazyCollection`으로 변환하면 추가 메모리 할당을 줄일 수 있습니다.

<a name="method-macro"></a>
#### `macro()`

정적 메서드 `macro`는 런타임에 `Collection` 클래스에 메서드를 추가합니다. 확장 관련 문서는 [컬렉션 확장하기](#extending-collections)를 참고하세요.

<a name="method-make"></a>
#### `make()`

정적 `make` 메서드는 새로운 컬렉션 인스턴스를 만듭니다. 자세한 내용은 [컬렉션 생성하기](#creating-collections) 섹션을 참고하세요.

<a name="method-map"></a>
#### `map()`

`map` 메서드는 각 아이템을 클로저에 전달하여 결과값으로 새로운 컬렉션을 만듭니다:

```
$collection = collect([1, 2, 3, 4, 5]);

$multiplied = $collection->map(function (int $item, int $key) {
    return $item * 2;
});

$multiplied->all();

// [2, 4, 6, 8, 10]
```

> [!WARNING]  
> `map`은 새로운 컬렉션을 반환하고 원본 컬렉션은 변경하지 않습니다. 원본 컬렉션 자체를 변경하려면 [`transform`](#method-transform) 메서드를 사용하세요.

<a name="method-mapinto"></a>
#### `mapInto()`

`mapInto()` 메서드는 컬렉션을 순회하며 값으로 새로운 클래스 인스턴스를 생성합니다:

```
class Currency
{
    /**
     * Create a new currency instance.
     */
    function __construct(
        public string $code
    ) {}
}

$collection = collect(['USD', 'EUR', 'GBP']);

$currencies = $collection->mapInto(Currency::class);

$currencies->all();

// [Currency('USD'), Currency('EUR'), Currency('GBP')]
```

<a name="method-mapspread"></a>
#### `mapSpread()`

`mapSpread` 메서드는 각 중첩 아이템 값을 클로저에 펼쳐 인수로 전달하며, 변환된 새 컬렉션을 반환합니다:

```
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

`mapToGroups` 메서드는 클로저의 반환값(단일 키/값 쌍)을 이용해 컬렉션을 그룹으로 나눕니다:

```
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

`mapWithKeys` 메서드는 클로저가 반환하는 단일 키/값 쌍으로 컬렉션을 새 키 값으로 매핑합니다:

```
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

`max` 메서드는 주어진 키의 최대 값을 반환합니다:

```
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

`median` 메서드는 주어진 키의 [중앙값](https://en.wikipedia.org/wiki/Median)을 반환합니다:

```
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

`merge` 메서드는 주어진 배열이나 컬렉션을 원본 컬렉션에 병합합니다. 문자열 키가 겹치면 주어진 값이 덮어씌웁니다:

```
$collection = collect(['product_id' => 1, 'price' => 100]);

$merged = $collection->merge(['price' => 200, 'discount' => false]);

$merged->all();

// ['product_id' => 1, 'price' => 200, 'discount' => false]
```

숫자 키는 뒤에 값이 추가됩니다:

```
$collection = collect(['Desk', 'Chair']);

$merged = $collection->merge(['Bookcase', 'Door']);

$merged->all();

// ['Desk', 'Chair', 'Bookcase', 'Door']
```

<a name="method-mergerecursive"></a>
#### `mergeRecursive()`

`mergeRecursive`는 내부 배열까지 재귀적으로 병합합니다:

```
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

`min` 메서드는 주어진 키의 최소 값을 반환합니다:

```
$min = collect([['foo' => 10], ['foo' => 20]])->min('foo');

// 10

$min = collect([1, 2, 3, 4, 5])->min();

// 1
```

<a name="method-mode"></a>
#### `mode()`

`mode` 메서드는 주어진 키의 최빈값([모드](https://en.wikipedia.org/wiki/Mode_(statistics)))을 배열로 반환합니다:

```
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

<a name="method-nth"></a>
#### `nth()`

`nth` 메서드는 n번째 요소만 포함하는 새 컬렉션을 생성합니다:

```
$collection = collect(['a', 'b', 'c', 'd', 'e', 'f']);

$collection->nth(4);

// ['a', 'e']
```

시작 오프셋도 지정할 수 있습니다:

```
$collection->nth(4, 1);

// ['b', 'f']
```

<a name="method-only"></a>
#### `only()`

`only` 메서드는 지정된 키에 해당하는 아이템만 반환합니다:

```
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

반대는 [except](#method-except) 메서드를 참고하세요.

> [!NOTE]  
> [Eloquent 컬렉션](/docs/10.x/eloquent-collections#method-only)에서 다르게 동작할 수 있습니다.

<a name="method-pad"></a>
#### `pad()`

`pad` 메서드는 배열이 지정한 크기에 도달할 때까지 주어진 값으로 채웁니다. `array_pad` 함수와 비슷하게 음수 크기는 왼쪽에 채웁니다:

```
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

`partition`은 조건에 맞는 아이템과 맞지 않는 아이템을 분리해 PHP 배열 비구조화로 받을 수 있습니다:

```
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

`percentage` 메서드는 조건에 맞는 아이템의 비율(퍼센트)을 빠르게 구합니다:

```php
$collection = collect([1, 1, 2, 2, 2, 3]);

$percentage = $collection->percentage(fn ($value) => $value === 1);

// 33.33
```

소수점 자릿수는 두 번째 인수로 조정할 수 있습니다:

```php
$percentage = $collection->percentage(fn ($value) => $value === 1, precision: 3);

// 33.333
```

<a name="method-pipe"></a>
#### `pipe()`

`pipe` 메서드는 컬렉션을 클로저에 전달하고, 실행 결과를 반환합니다:

```
$collection = collect([1, 2, 3]);

$piped = $collection->pipe(function (Collection $collection) {
    return $collection->sum();
});

// 6
```

<a name="method-pipeinto"></a>
#### `pipeInto()`

`pipeInto` 메서드는 주어진 클래스의 새 인스턴스를 생성하고 컬렉션을 생성자 인수로 전달합니다:

```
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

`pipeThrough` 메서드는 컬렉션을 여러 클로저 연산에 순차적으로 전달하며, 최종 결과를 반환합니다:

```
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

`pluck` 메서드는 주어진 키에 해당하는 모든 값을 반환합니다:

```
$collection = collect([
    ['product_id' => 'prod-100', 'name' => 'Desk'],
    ['product_id' => 'prod-200', 'name' => 'Chair'],
]);

$plucked = $collection->pluck('name');

$plucked->all();

// ['Desk', 'Chair']
```

키를 지정해 결과 컬렉션의 키로 사용할 수도 있습니다:

```
$plucked = $collection->pluck('name', 'product_id');

$plucked->all();

// ['prod-100' => 'Desk', 'prod-200' => 'Chair']
```

"dot" 표기법으로 중첩 값도 조회 가능합니다:

```
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

중복 키는 마지막 일치 항목이 덮어씁니다:

```
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

`pop` 메서드는 컬렉션에서 마지막 아이템을 제거하고 반환합니다:

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->pop();

// 5

$collection->all();

// [1, 2, 3, 4]
```

정수를 인수로 주면 여러 아이템을 뒤에서부터 제거하고 반환합니다:

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->pop(3);

// collect([5, 4, 3])

$collection->all();

// [1, 2]
```

<a name="method-prepend"></a>
#### `prepend()`

`prepend` 메서드는 컬렉션 앞에 아이템을 추가합니다:

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->prepend(0);

$collection->all();

// [0, 1, 2, 3, 4, 5]
```

두 번째 인수로 키를 지정할 수도 있습니다:

```
$collection = collect(['one' => 1, 'two' => 2]);

$collection->prepend(0, 'zero');

$collection->all();

// ['zero' => 0, 'one' => 1, 'two' => 2]
```

<a name="method-pull"></a>
#### `pull()`

`pull` 메서드는 키를 통해 아이템을 제거하고 반환합니다:

```
$collection = collect(['product_id' => 'prod-100', 'name' => 'Desk']);

$collection->pull('name');

// 'Desk'

$collection->all();

// ['product_id' => 'prod-100']
```

<a name="method-push"></a>
#### `push()`

`push` 메서드는 컬렉션 끝에 아이템을 추가합니다:

```
$collection = collect([1, 2, 3, 4]);

$collection->push(5);

$collection->all();

// [1, 2, 3, 4, 5]
```

<a name="method-put"></a>
#### `put()`

`put` 메서드는 주어진 키와 값을 컬렉션에 설정합니다:

```
$collection = collect(['product_id' => 1, 'name' => 'Desk']);

$collection->put('price', 100);

$collection->all();

// ['product_id' => 1, 'name' => 'Desk', 'price' => 100]
```

<a name="method-random"></a>
#### `random()`

`random` 메서드는 컬렉션에서 랜덤한 아이템을 반환합니다:

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->random();

// 4 - (임의 반환)
```

인수로 개수를 줄 수도 있으며, 이 경우 컬렉션을 반환합니다:

```
$random = $collection->random(3);

$random->all();

// [2, 4, 5] (임의 추출)
```

요청한 개수보다 아이템이 적으면 `InvalidArgumentException` 예외가 발생합니다.

콜백을 인수로 전달해 현재 컬렉션 인스턴스를 이용할 수도 있습니다:

```
use Illuminate\Support\Collection;

$random = $collection->random(fn (Collection $items) => min(10, count($items)));

$random->all();

// [1, 2, 3, 4, 5] (임의 추출)
```

<a name="method-range"></a>
#### `range()`

`range` 메서드는 지정한 범위 내 정수들을 포함하는 컬렉션을 반환합니다:

```
$collection = collect()->range(3, 6);

$collection->all();

// [3, 4, 5, 6]
```

<a name="method-reduce"></a>
#### `reduce()`

`reduce` 메서드는 컬렉션을 단일 값으로 축소하며, 각 반복 결과는 다음 반복으로 넘깁니다:

```
$collection = collect([1, 2, 3]);

$total = $collection->reduce(function (?int $carry, int $item) {
    return $carry + $item;
});

// 6
```

초기값을 두 번째 인수로 지정할 수 있습니다:

```
$collection->reduce(function (int $carry, int $item) {
    return $carry + $item;
}, 4);

// 10
```

키를 포함한 콜백 파라미터도 전달할 수 있습니다:

```
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

`reduceSpread` 메서드는 배열을 축소하며, 여러 초기값을 지원합니다:

```
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

`reject` 메서드는 주어진 조건을 만족하는 요소를 제거합니다:

```
$collection = collect([1, 2, 3, 4]);

$filtered = $collection->reject(function (int $value, int $key) {
    return $value > 2;
});

$filtered->all();

// [1, 2]
```

반대는 [`filter`](#method-filter) 메서드를 참고하세요.

<a name="method-replace"></a>
#### `replace()`

`replace` 메서드는 `merge`와 유사하지만 문자열 키뿐만 아니라 숫자 키도 덮어씁니다:

```
$collection = collect(['Taylor', 'Abigail', 'James']);

$replaced = $collection->replace([1 => 'Victoria', 3 => 'Finn']);

$replaced->all();

// ['Taylor', 'Victoria', 'James', 'Finn']
```

<a name="method-replacerecursive"></a>
#### `replaceRecursive()`

내부 배열까지 재귀적으로 덮어씁니다:

```
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

`reverse` 메서드는 원본 키를 유지하며 컬렉션을 역순으로 뒤집습니다:

```
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

`search` 메서드는 주어진 값을 찾아 해당 키를 반환합니다. 찾지 못하면 `false`를 반환합니다:

```
$collection = collect([2, 4, 6, 8]);

$collection->search(4);

// 1
```

비교는 "느슨한(loose)" 비교를 사용합니다. 엄격한 비교는 두 번째 인수에 `true`를 전달하세요:

```
collect([2, 4, 6, 8])->search('4', $strict = true);

// false
```

콜백으로 조건을 지정할 수도 있습니다:

```
collect([2, 4, 6, 8])->search(function (int $item, int $key) {
    return $item > 5;
});

// 2
```

<a name="method-select"></a>
#### `select()`

`select` 메서드는 SQL의 `SELECT`처럼 주어진 키만 선택합니다:

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

`shift` 메서드는 처음 아이템을 제거하고 반환합니다:

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->shift();

// 1

$collection->all();

// [2, 3, 4, 5]
```

여러 개를 제거하려면 정수를 인수로 전달합니다:

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->shift(3);

// collect([1, 2, 3])

$collection->all();

// [4, 5]
```

<a name="method-shuffle"></a>
#### `shuffle()`

`shuffle` 메서드는 컬렉션 아이템을 무작위로 섞습니다:

```
$collection = collect([1, 2, 3, 4, 5]);

$shuffled = $collection->shuffle();

$shuffled->all();

// [3, 2, 5, 1, 4] (임의 생성)
```

<a name="method-skip"></a>
#### `skip()`

`skip` 메서드는 처음 n개 아이템을 제거한 새 컬렉션을 반환합니다:

```
$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);

$collection = $collection->skip(4);

$collection->all();

// [5, 6, 7, 8, 9, 10]
```

<a name="method-skipuntil"></a>
#### `skipUntil()`

`skipUntil` 메서드는 콜백이 `true`를 반환할 때까지 아이템을 건너뛰고 나머지를 반환합니다:

```
$collection = collect([1, 2, 3, 4]);

$subset = $collection->skipUntil(function (int $item) {
    return $item >= 3;
});

$subset->all();

// [3, 4]
```

값을 전달하면 해당 값이 나올 때까지 건너뜁니다:

```
$subset = $collection->skipUntil(3);

$subset->all();

// [3, 4]
```

> [!WARNING]  
> 값이 없거나 콜백이 항상 `false`이면 빈 컬렉션을 반환합니다.

<a name="method-skipwhile"></a>
#### `skipWhile()`

`skipWhile` 메서드는 콜백이 `true`일 때 계속 건너뛰고, `false`가 나오면 나머지를 반환합니다:

```
$collection = collect([1, 2, 3, 4]);

$subset = $collection->skipWhile(function (int $item) {
    return $item <= 3;
});

$subset->all();

// [4]
```

> [!WARNING]  
> 콜백이 항상 `true`면 빈 컬렉션을 반환합니다.

<a name="method-slice"></a>
#### `slice()`

`slice` 메서드는 지정한 시작 인덱스부터 잘라낸 새로운 컬렉션을 반환합니다:

```
$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);

$slice = $collection->slice(4);

$slice->all();

// [5, 6, 7, 8, 9, 10]
```

크기 제한도 지정 가능합니다:

```
$slice = $collection->slice(4, 2);

$slice->all();

// [5, 6]
```

키는 기본적으로 유지되며, 재인덱싱 하려면 [`values`](#method-values) 메서드를 호출하세요.

<a name="method-sliding"></a>
#### `sliding()`

`sliding` 메서드는 "슬라이딩 윈도우" 형태로 컬렉션의 아이템을 크기별로 나누어 반환합니다:

```
$collection = collect([1, 2, 3, 4, 5]);

$chunks = $collection->sliding(2);

$chunks->toArray();

// [[1, 2], [2, 3], [3, 4], [4, 5]]
```

`eachSpread` 메서드와 함께 유용하게 사용됩니다:

```
$transactions->sliding(2)->eachSpread(function (Collection $previous, Collection $current) {
    $current->total = $previous->total + $current->amount;
});
```

두 번째 인수로 스텝(간격)을 지정할 수 있습니다:

```
$chunks = $collection->sliding(3, step: 2);

$chunks->toArray();

// [[1, 2, 3], [3, 4, 5]]
```

<a name="method-sole"></a>
#### `sole()`

`sole` 메서드는 조건에 맞는 정확히 하나의 아이템만 반환합니다:

```
collect([1, 2, 3, 4])->sole(function (int $value, int $key) {
    return $value === 2;
});

// 2
```

키/값 쌍 전달 가능:

```
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
]);

$collection->sole('product', 'Chair');

// ['product' => 'Chair', 'price' => 100]
```

인수가 없으면 하나뿐인 항목을 반환합니다:

```
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
]);

$collection->sole();

// ['product' => 'Desk', 'price' => 200]
```

해당 조건을 만족하는 항목이 없으면 `ItemNotFoundException`이, 둘 이상이면 `MultipleItemsFoundException` 예외가 발생합니다.

<a name="method-some"></a>
#### `some()`

[`contains`](#method-contains) 메서드의 별칭입니다.

<a name="method-sort"></a>
#### `sort()`

`sort` 메서드는 컬렉션을 정렬합니다. 원본 키를 유지하기 때문에, 일반적으로 [`values`](#method-values)로 키를 리셋합니다:

```
$collection = collect([5, 3, 1, 2, 4]);

$sorted = $collection->sort();

$sorted->values()->all();

// [1, 2, 3, 4, 5]
```

콜백을 전달해 정렬 방식을 직접 지정할 수도 있습니다.

> [!NOTE]  
> 다차원 배열 또는 객체 정렬은 [`sortBy`](#method-sortby), [`sortByDesc`](#method-sortbydesc) 메서드를 참고하세요.

<a name="method-sortby"></a>
#### `sortBy()`

주어진 키를 기준으로 컬렉션을 정렬합니다:

```
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

정렬 옵션([sort flags](https://www.php.net/manual/en/function.sort.php))을 두 번째 인수로 지정할 수 있습니다:

```
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

또는 클로저로 직접 정렬 방식을 지정 가능합니다:

```
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

여러 키로 정렬하려면 배열로 키들을 지정하세요:

```
$sorted = $collection->sortBy(['name', 'age']);

$sorted->values()->all();
```

다중 키와 방향(asc/desc) 지정 시 배열에 배열로 전달합니다:

```
$sorted = $collection->sortBy([
    ['name', 'asc'],
    ['age', 'desc'],
]);

$sorted->values()->all();
```

클로저 배열로 직접 비교함수를 지정할 수도 있습니다:

```
$sorted = $collection->sortBy([
    fn (array $a, array $b) => $a['name'] <=> $b['name'],
    fn (array $a, array $b) => $b['age'] <=> $a['age'],
]);

$sorted->values()->all();
```

<a name="method-sortbydesc"></a>
#### `sortByDesc()`

`sortBy`와 같은 서명을 갖지만 내림차순으로 정렬합니다.

<a name="method-sortdesc"></a>
#### `sortDesc()`

`sort`의 내림차순 버전입니다:

```
$collection = collect([5, 3, 1, 2, 4]);

$sorted = $collection->sortDesc();

$sorted->values()->all();

// [5, 4, 3, 2, 1]
```

콜백 인수를 받을 수 없으니, `sort`에서 비교를 반대로 구현하세요.

<a name="method-sortkeys"></a>
#### `sortKeys()`

키 기준으로 컬렉션을 정렬합니다:

```
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

`sortKeys`와 같으나 내림차순 정렬입니다.

<a name="method-sortkeysusing"></a>
#### `sortKeysUsing()`

키 기준으로 사용자 정의 콜백으로 정렬합니다:

```
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

콜백은 비교 함수로, PHP `uksort` 함수와 동일 원리입니다.

<a name="method-splice"></a>
#### `splice()`

`splice` 메서드는 지정 인덱스부터 일정 범위의 아이템을 제거하고 반환합니다:

```
$collection = collect([1, 2, 3, 4, 5]);

$chunk = $collection->splice(2);

$chunk->all();

// [3, 4, 5]

$collection->all();

// [1, 2]
```

두 번째 인수로 크기 제한 가능:

```
$chunk = $collection->splice(2, 1);

$chunk->all();

// [3]

$collection->all();

// [1, 2, 4, 5]
```

세 번째 인수로 대체 아이템 지정도 가능합니다:

```
$chunk = $collection->splice(2, 1, [10, 11]);

$chunk->all();

// [3]

$collection->all();

// [1, 2, 10, 11, 4, 5]
```

<a name="method-split"></a>
#### `split()`

`split` 메서드는 컬렉션을 지정한 수의 그룹으로 나눕니다:

```
$collection = collect([1, 2, 3, 4, 5]);

$groups = $collection->split(3);

$groups->all();

// [[1, 2], [3, 4], [5]]
```

<a name="method-splitin"></a>
#### `splitIn()`

`splitIn` 메서드는 지정한 그룹 수로 나누며, 끝 그룹 빼고 전부 균등하게 채웁니다:

```
$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);

$groups = $collection->splitIn(3);

$groups->all();

// [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10]]
```

<a name="method-sum"></a>
#### `sum()`

`sum` 메서드는 컬렉션 아이템의 합계를 반환합니다:

```
collect([1, 2, 3, 4, 5])->sum();

// 15
```

중첩 배열이나 객체라면 키를 지정하세요:

```
$collection = collect([
    ['name' => 'JavaScript: The Good Parts', 'pages' => 176],
    ['name' => 'JavaScript: The Definitive Guide', 'pages' => 1096],
]);

$collection->sum('pages');

// 1272
```

클로저도 가능합니다:

```
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

`take` 메서드는 지정 개수만큼 아이템을 포함하는 새 컬렉션을 반환합니다:

```
$collection = collect([0, 1, 2, 3, 4, 5]);

$chunk = $collection->take(3);

$chunk->all();

// [0, 1, 2]
```

음수를 주면 뒤에서부터 가져옵니다:

```
$collection = collect([0, 1, 2, 3, 4, 5]);

$chunk = $collection->take(-2);

$chunk->all();

// [4, 5]
```

<a name="method-takeuntil"></a>
#### `takeUntil()`

`takeUntil` 메서드는 콜백이 `true`가 될 때까지 아이템을 반환합니다:

```
$collection = collect([1, 2, 3, 4]);

$subset = $collection->takeUntil(function (int $item) {
    return $item >= 3;
});

$subset->all();

// [1, 2]
```

값으로 지정할 수 있습니다:

```
$subset = $collection->takeUntil(3);

$subset->all();

// [1, 2]
```

> [!WARNING]  
> 값이 없거나 콜백이 항상 `false`면 모든 아이템을 반환합니다.

<a name="method-takewhile"></a>
#### `takeWhile()`

`takeWhile` 메서드는 콜백이 `false`가 될 때까지 아이템을 반환합니다:

```
$collection = collect([1, 2, 3, 4]);

$subset = $collection->takeWhile(function (int $item) {
    return $item < 3;
});

$subset->all();

// [1, 2]
```

> [!WARNING]  
> 콜백이 항상 `true`면 모든 아이템을 반환합니다.

<a name="method-tap"></a>
#### `tap()`

`tap` 메서드는 컬렉션을 클로저에 전달하여 중간 작업을 수행한 뒤, 본 컬렉션을 다시 반환합니다:

```
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

정적 `times` 메서드는 지정 횟수만큼 클로저를 호출해 새 컬렉션을 생성합니다:

```
$collection = Collection::times(10, function (int $number) {
    return $number * 9;
});

$collection->all();

// [9, 18, 27, 36, 45, 54, 63, 72, 81, 90]
```

<a name="method-toarray"></a>
#### `toArray()`

`toArray` 메서드는 컬렉션을 순수 PHP 배열로 변환합니다. [Eloquent](/docs/10.x/eloquent) 모델이 포함된 경우 모델들도 배열로 변환됩니다:

```
$collection = collect(['name' => 'Desk', 'price' => 200]);

$collection->toArray();

/*
    [
        ['name' => 'Desk', 'price' => 200],
    ]
*/
```

> [!WARNING]  
> `toArray`는 `Arrayable` 인스턴스인 모든 중첩 객체도 배열로 변환합니다. 원시 배열을 얻으려면 [`all`](#method-all) 메서드를 사용하세요.

<a name="method-tojson"></a>
#### `toJson()`

`toJson` 메서드는 컬렉션을 JSON 문자열로 직렬화합니다:

```
$collection = collect(['name' => 'Desk', 'price' => 200]);

$collection->toJson();

// '{"name":"Desk", "price":200}'
```

<a name="method-transform"></a>
#### `transform()`

`transform` 메서드는 컬렉션을 직접 수정하며, 아이템을 순회하며 클로저 반환값으로 교체합니다:

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->transform(function (int $item, int $key) {
    return $item * 2;
});

$collection->all();

// [2, 4, 6, 8, 10]
```

> [!WARNING]  
> `transform`은 원본 컬렉션을 수정합니다. 새 컬렉션을 만들려면 [`map`](#method-map)을 사용하세요.

<a name="method-undot"></a>
#### `undot()`

`undot` 메서드는 "dot" 표기법으로 된 단일 차원 컬렉션을 다차원 컬렉션으로 확장합니다:

```
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

`union` 메서드는 주어진 배열을 컬렉션에 추가합니다. 키가 중복되면 원본 값이 우선합니다:

```
$collection = collect([1 => ['a'], 2 => ['b']]);

$union = $collection->union([3 => ['c'], 1 => ['d']]);

$union->all();

// [1 => ['a'], 2 => ['b'], 3 => ['c']]
```

<a name="method-unique"></a>
#### `unique()`

`unique` 메서드는 유일한(item 중복을 제거한) 아이템만 반환합니다:

```
$collection = collect([1, 1, 2, 2, 3, 4, 2]);

$unique = $collection->unique();

$unique->values()->all();

// [1, 2, 3, 4]
```

중첩 배열이나 객체라면 비교할 키를 지정할 수 있습니다:

```
$unique = $collection->unique('brand');

$unique->values()->all();

/*
    [
        ['name' => 'iPhone 6', 'brand' => 'Apple', 'type' => 'phone'],
        ['name' => 'Galaxy S6', 'brand' => 'Samsung', 'type' => 'phone'],
    ]
*/
```

클로저를 사용해 유일성 기준을 직접 정할 수도 있습니다:

```
$unique = $collection->unique(function (array $item) {
    return $item['brand'].$item['type'];
});

$unique->values()->all();
```

비교는 기본적으로 느슨한(loose) 비교입니다. 엄격 비교가 필요하면 [`uniqueStrict`](#method-uniquestrict)를 사용하세요.

> [!NOTE]  
> [Eloquent 컬렉션](/docs/10.x/eloquent-collections#method-unique)에서는 동작이 다를 수 있습니다.

<a name="method-uniquestrict"></a>
#### `uniqueStrict()`

`unique`와 동일하지만, 모든 비교가 엄격합니다.

<a name="method-unless"></a>
#### `unless()`

`unless` 메서드는 첫 인수가 `true`가 아니면 클로저를 실행합니다:

```
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

두 번째 클로저를 전달해 첫 인수가 `true`일 때 실행할 수도 있습니다:

```
$collection->unless(true, function (Collection $collection) {
    return $collection->push(4);
}, function (Collection $collection) {
    return $collection->push(5);
});

$collection->all();

// [1, 2, 3, 5]
```

반대는 [`when`](#method-when) 메서드를 참고하세요.

<a name="method-unlessempty"></a>
#### `unlessEmpty()`

[`whenNotEmpty`](#method-whennotempty) 메서드 별칭입니다.

<a name="method-unlessnotempty"></a>
#### `unlessNotEmpty()`

[`whenEmpty`](#method-whenempty) 메서드 별칭입니다.

<a name="method-unwrap"></a>
#### `unwrap()`

정적 메서드 `unwrap`은 컬렉션 인스턴스면 내부 아이템을, 배열이면 그대로, 그 외는 인수를 반환합니다:

```
Collection::unwrap(collect('John Doe'));

// ['John Doe']

Collection::unwrap(['John Doe']);

// ['John Doe']

Collection::unwrap('John Doe');

// 'John Doe'
```

<a name="method-value"></a>
#### `value()`

`value` 메서드는 컬렉션 첫 요소에서 지정한 키 값을 반환합니다:

```
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Speaker', 'price' => 400],
]);

$value = $collection->value('price');

// 200
```

<a name="method-values"></a>
#### `values()`

`values` 메서드는 키를 연속된 정수로 리셋한 새 컬렉션을 반환합니다:

```
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

`when` 메서드는 첫 인수가 `true`일 때 클로저를 실행합니다:

```
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

두 번째 클로저를 넘겨 첫 인수가 `false`일 때 실행할 수도 있습니다:

```
$collection->when(false, function (Collection $collection, int $value) {
    return $collection->push(4);
}, function (Collection $collection) {
    return $collection->push(5);
});

$collection->all();

// [1, 2, 3, 5]
```

반대는 [`unless`](#method-unless) 메서드를 참고하세요.

<a name="method-whenempty"></a>
#### `whenEmpty()`

컬렉션이 비어있으면 클로저를 실행합니다:

```
$collection = collect(['Michael', 'Tom']);

$collection->whenEmpty(function (Collection $collection) {
    return $collection->push('Adam');
});

$collection->all();

// ['Michael', 'Tom']
```

```
$collection = collect();

$collection->whenEmpty(function (Collection $collection) {
    return $collection->push('Adam');
});

$collection->all();

// ['Adam']
```

두 번째 클로저를 넘겨 비어있지 않을 때 다른 작업도 가능합니다:

```
$collection = collect(['Michael', 'Tom']);

$collection->whenEmpty(function (Collection $collection) {
    return $collection->push('Adam');
}, function (Collection $collection) {
    return $collection->push('Taylor');
});

$collection->all();

// ['Michael', 'Tom', 'Taylor']
```

반대는 [`whenNotEmpty`](#method-whennotempty)입니다.

<a name="method-whennotempty"></a>
#### `whenNotEmpty()`

컬렉션이 비어있지 않으면 클로저를 실행합니다:

```
$collection = collect(['michael', 'tom']);

$collection->whenNotEmpty(function (Collection $collection) {
    return $collection->push('adam');
});

$collection->all();

// ['michael', 'tom', 'adam']
```

```
$collection = collect();

$collection->whenNotEmpty(function (Collection $collection) {
    return $collection->push('adam');
});

$collection->all();

// []
```

두 번째 클로저를 넘겨 비어있으면 실행할 수 있습니다:

```
$collection = collect();

$collection->whenNotEmpty(function (Collection $collection) {
    return $collection->push('adam');
}, function (Collection $collection) {
    return $collection->push('taylor');
});

$collection->all();

// ['taylor']
```

반대는 [`whenEmpty`](#method-whenempty)입니다.

<a name="method-where"></a>
#### `where()`

`where` 메서드는 주어진 키/값 쌍 조건으로 필터링합니다:

```
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

비교는 기본적으로 느슨한(loose) 비교입니다. 엄격한 비교를 원하면 [`whereStrict`](#method-wherestrict)를 사용하세요.

비교 연산자를 두 번째 인수로 지정할 수도 있습니다:

```
$filtered = $collection->where('deleted_at', '!=', null);

// ['name' => 'Jim' ...], ['name' => 'Sally' ...]
```

<a name="method-wherestrict"></a>
#### `whereStrict()`

`where`와 동일하나 모든 비교를 엄격하게 진행합니다.

<a name="method-wherebetween"></a>
#### `whereBetween()`

`whereBetween` 메서드는 값이 지정 범위 내에 있는 아이템만 반환합니다:

```
$filtered = $collection->whereBetween('price', [100, 200]);
```

<a name="method-wherein"></a>
#### `whereIn()`

`whereIn` 메서드는 주어진 배열에 포함된 값만 남깁니다:

```
$filtered = $collection->whereIn('price', [150, 200]);
```

느슨한 비교를 하며, 엄격한 비교는 [`whereInStrict`](#method-whereinstrict)를 사용하세요.

<a name="method-whereinstrict"></a>
#### `whereInStrict()`

`whereIn`과 동일하지만 엄격한 비교를 수행합니다.

<a name="method-whereinstanceof"></a>
#### `whereInstanceOf()`

`whereInstanceOf`는 주어진 클래스 타입에 해당하는 아이템만 남깁니다:

```
$filtered = $collection->whereInstanceOf(User::class);
```

<a name="method-wherenotbetween"></a>
#### `whereNotBetween()`

`whereNotBetween`은 지정 범위 밖 값만 남깁니다.

<a name="method-wherenotin"></a>
#### `whereNotIn()`

`whereNotIn`은 주어진 배열에 포함된 값은 제외시킵니다.

비교는 기본 느슨한 비교이며, 엄격 비교는 [`whereNotInStrict`](#method-wherenotinstrict)를 사용하세요.

<a name="method-wherenotinstrict"></a>
#### `whereNotInStrict()`

`whereNotIn`과 동일하나 엄격하게 비교합니다.

<a name="method-wherenotnull"></a>
#### `whereNotNull()`

지정 키의 값이 `null`이 아닌 아이템만 반환합니다.

<a name="method-wherenull"></a>
#### `whereNull()`

지정 키의 값이 `null`인 아이템만 반환합니다.


<a name="method-wrap"></a>
#### `wrap()`

정적 `wrap` 메서드는 값이 컬렉션이 아니면 컬렉션으로 감싸 반환합니다:

```
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

`zip` 메서드는 컬렉션과 주어진 배열을 인덱스별로 병합합니다:

```
$collection = collect(['Chair', 'Desk']);

$zipped = $collection->zip([100, 200]);

$zipped->all();

// [['Chair', 100], ['Desk', 200]]
```

<a name="higher-order-messages"></a>
## 고차 메시지

컬렉션은 흔히 쓰이는 작업을 간단히 처리할 수 있게 "고차 메시지"를 지원합니다. 예를 들면 [`average`](#method-average), [`contains`](#method-contains), [`each`](#method-each), [`filter`](#method-filter), [`map`](#method-map), [`sum`](#method-sum), [`unique`](#method-unique) 등이 있습니다.

고차 메시지는 컬렉션 인스턴스의 동적 프로퍼티로 접근할 수 있습니다. 예를 들어, `each` 고차 메시지로 각 객체의 메서드를 호출할 수 있습니다:

```
use App\Models\User;

$users = User::where('votes', '>', 500)->get();

$users->each->markAsVip();
```

`sum` 고차 메시지로는 컬렉션 내 특정 속성의 총합을 구할 수 있습니다:

```
$users = User::where('group', 'Development')->get();

return $users->sum->votes;
```

<a name="lazy-collections"></a>
## 지연 컬렉션 (Lazy Collections)

<a name="lazy-collection-introduction"></a>
### 소개

> [!WARNING]  
> Laravel 지연 컬렉션에 대해 배우기 전에 [PHP 제네레이터](https://www.php.net/manual/en/language.generators.overview.php)에 익숙해지세요.

`LazyCollection` 클래스는 PHP 제네레이터를 활용해 대용량 데이터셋을 메모리 효율적으로 다룰 수 있게 합니다.

예를 들어, 수 GB 크기의 로그 파일을 처리하면서 Laravel 컬렉션 메서드를 사용한다고 해도, 한 번에 전체를 메모리에 올리지 않고 일부분만 유지할 수 있습니다:

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
    // 로그 처리...
});
```

또는 10,000개의 Eloquent 모델을 반복해야 할 때, 기존 컬렉션은 모두 메모리에 적재하지만, 쿼리 빌더의 `cursor` 메서드는 `LazyCollection`을 반환하여 하나씩 처리할 수 있습니다:

```
use App\Models\User;

$users = User::cursor()->filter(function (User $user) {
    return $user->id > 500;
});

foreach ($users as $user) {
    echo $user->id;
}
```

필터 콜백은 나중에 각 사용자 개별 순회 시 실행되므로, 메모리 사용량을 크게 줄일 수 있습니다.

<a name="creating-lazy-collections"></a>
### 지연 컬렉션 생성하기

지연 컬렉션은 PHP 제네레이터 함수와 함께 `make` 메서드에 전달하여 만듭니다:

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
### Enumerable 계약

`Collection`과 `LazyCollection` 클래스는 모두 `Illuminate\Support\Enumerable` 계약을 구현하여 아래 메서드를 제공합니다:



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
> `shift`, `pop`, `prepend` 등 컬렉션 내용을 직접 변경하는 메서드는 `LazyCollection`에서는 사용할 수 없습니다.

<a name="lazy-collection-methods"></a>
### 지연 컬렉션 메서드

`Enumerable` 계약에 정의된 메서드 외에도 `LazyCollection`은 아래 추가 메서드를 제공합니다:

<a name="method-takeUntilTimeout"></a>
#### `takeUntilTimeout()`

`takeUntilTimeout` 메서드는 지정한 시각까지 아이템을 나열하다가, 이후 중단하는 지연 컬렉션을 만듭니다:

```
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

예를 들어, 데이터베이스에서 인보이스를 커서로 가져와 15분마다 실행되는 [스케줄러 작업](/docs/10.x/scheduling)에서 최대 14분간만 처리할 수 있습니다:

```
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

`each` 메서드는 컬렉션의 모든 아이템에 즉시 클로저를 호출하지만, `tapEach`는 아이템이 하나씩 처리될 때 클로저를 호출합니다:

```
// 아직 아무것도 출력되지 않음...
$lazyCollection = LazyCollection::times(INF)->tapEach(function (int $value) {
    dump($value);
});

// 세 개 아이템이 출력됨...
$array = $lazyCollection->take(3)->all();

// 1
// 2
// 3
```

<a name="method-remember"></a>
#### `remember()`

`remember` 메서드는 이미 나열된 값을 기억하여 반복 시 다시 조회하지 않는 지연 컬렉션을 반환합니다:

```
// 아직 쿼리 실행 안 됨...
$users = User::cursor()->remember();

// 쿼리 실행됨...
// 처음 5명은 DB에서 로드됨...
$users->take(5)->all();

// 처음 5명은 컬렉션 캐시에서 사용되고,
// 나머지는 DB에서 로드됨...
$users->take(20)->all();
```