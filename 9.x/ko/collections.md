# 컬렉션 (Collections)

- [소개](#introduction)
    - [컬렉션 생성하기](#creating-collections)
    - [컬렉션 확장하기](#extending-collections)
- [사용 가능한 메서드](#available-methods)
- [하이어 오더 메시지](#higher-order-messages)
- [레이지 컬렉션 (Lazy Collections)](#lazy-collections)
    - [소개](#lazy-collection-introduction)
    - [레이지 컬렉션 생성하기](#creating-lazy-collections)
    - [Enumerable 계약](#the-enumerable-contract)
    - [레이지 컬렉션 메서드](#lazy-collection-methods)

<a name="introduction"></a>
## 소개 (Introduction)

`Illuminate\Support\Collection` 클래스는 배열 데이터를 다룰 때 유창하고 편리한 래퍼를 제공합니다. 예를 들어, 다음 코드를 확인해 보세요. `collect` 헬퍼를 사용하여 배열에서 새로운 컬렉션 인스턴스를 생성하고, 각 요소에 `strtoupper` 함수를 적용한 후, 빈 값을 모두 제거합니다:

```
$collection = collect(['taylor', 'abigail', null])->map(function ($name) {
    return strtoupper($name);
})->reject(function ($name) {
    return empty($name);
});
```

보시다시피, `Collection` 클래스는 메서드를 체인하여 기본 배열을 유창하게 매핑하고 축소할 수 있게 합니다. 일반적으로 컬렉션은 불변(immutable)이며, 모든 `Collection` 메서드는 완전히 새로운 `Collection` 인스턴스를 반환합니다.

<a name="creating-collections"></a>
### 컬렉션 생성하기 (Creating Collections)

앞서 언급한 것처럼, `collect` 헬퍼는 주어진 배열에 대해 새로운 `Illuminate\Support\Collection` 인스턴스를 반환합니다. 따라서 컬렉션 생성은 다음과 같이 간단합니다:

```
$collection = collect([1, 2, 3]);
```

> [!NOTE]
> [Eloquent](/docs/9.x/eloquent) 쿼리 결과는 항상 `Collection` 인스턴스로 반환됩니다.

<a name="extending-collections"></a>
### 컬렉션 확장하기 (Extending Collections)

컬렉션은 "macroable"하여 런타임에 `Collection` 클래스에 추가 메서드를 쉽게 추가할 수 있습니다. `Illuminate\Support\Collection` 클래스의 `macro` 메서드는 매크로 호출 시 실행될 클로저를 인수로 받습니다. 이 매크로 클로저 안에서는 마치 컬렉션 클래스의 진짜 메서드인 것처럼 `$this`를 통해 다른 컬렉션 메서드에 접근할 수 있습니다. 예를 들어, 다음 코드는 `Collection` 클래스에 `toUpper` 메서드를 추가합니다:

```
use Illuminate\Support\Collection;
use Illuminate\Support\Str;

Collection::macro('toUpper', function () {
    return $this->map(function ($value) {
        return Str::upper($value);
    });
});

$collection = collect(['first', 'second']);

$upper = $collection->toUpper();

// ['FIRST', 'SECOND']
```

일반적으로 컬렉션 매크로는 [서비스 프로바이더](/docs/9.x/providers)의 `boot` 메서드 내에서 선언하는 것이 좋습니다.

<a name="macro-arguments"></a>
#### 매크로 인수 (Macro Arguments)

필요한 경우, 추가 인수를 받는 매크로를 정의할 수도 있습니다:

```
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\Lang;

Collection::macro('toLocale', function ($locale) {
    return $this->map(function ($value) use ($locale) {
        return Lang::get($value, [], $locale);
    });
});

$collection = collect(['first', 'second']);

$translated = $collection->toLocale('es');
```

<a name="available-methods"></a>
## 사용 가능한 메서드 (Available Methods)

남은 컬렉션 문서 대부분에서는 `Collection` 클래스에서 사용 가능한 각 메서드에 대해 설명합니다. 이 메서드들은 모두 체이닝이 가능하여 기본 배열을 유창하게 조작할 수 있습니다. 또한 거의 모든 메서드는 새로운 `Collection` 인스턴스를 반환하여 필요 시 원본 컬렉션을 보존할 수 있게 합니다.

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
[diffKeys](#method-diffkeys)
[doesntContain](#method-doesntcontain)
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
[forget](#method-forget)
[forPage](#method-forpage)
[get](#method-get)
[groupBy](#method-groupby)
[has](#method-has)
[hasAny](#method-hasany)
[implode](#method-implode)
[intersect](#method-intersect)
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

<a name="method-all"></a>
#### `all()`

`all` 메서드는 컬렉션이 나타내는 기본 배열을 반환합니다:

```
collect([1, 2, 3])->all();

// [1, 2, 3]
```

<a name="method-average"></a>
#### `average()`

[`avg`](#method-avg) 메서드의 별칭입니다.

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

<a name="method-chunk"></a>
#### `chunk()`

`chunk` 메서드는 컬렉션을 주어진 크기의 여러 작은 컬렉션으로 나눕니다:

```
$collection = collect([1, 2, 3, 4, 5, 6, 7]);

$chunks = $collection->chunk(4);

$chunks->all();

// [[1, 2, 3, 4], [5, 6, 7]]
```

이 메서드는 [뷰](/docs/9.x/views)에서 특히 [Bootstrap](https://getbootstrap.com/docs/4.1/layout/grid/) 같은 그리드 시스템과 작업할 때 유용합니다. 예를 들어, 그리드에 표시할 [Eloquent](/docs/9.x/eloquent) 모델 컬렉션이 있는 경우:

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

`chunkWhile` 메서드는 주어진 콜백 평가를 기반으로 컬렉션을 여러 작은 컬렉션으로 나눕니다. 클로저에 전달되는 `$chunk` 변수는 이전 요소를 검사하는 데 사용할 수 있습니다:

```
$collection = collect(str_split('AABBCCCD'));

$chunks = $collection->chunkWhile(function ($value, $key, $chunk) {
    return $value === $chunk->last();
});

$chunks->all();

// [['A', 'A'], ['B', 'B'], ['C', 'C', 'C'], ['D']]
```

<a name="method-collapse"></a>
#### `collapse()`

`collapse` 메서드는 배열의 컬렉션을 하나의 평탄한 컬렉션으로 접습니다:

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

`collect` 메서드는 컬렉션 내부의 현재 항목들로 새 `Collection` 인스턴스를 반환합니다:

```
$collectionA = collect([1, 2, 3]);

$collectionB = $collectionA->collect();

$collectionB->all();

// [1, 2, 3]
```

이 메서드는 주로 [레이지 컬렉션](#lazy-collections)을 일반 `Collection` 인스턴스로 변환할 때 유용합니다:

```
$lazyCollection = LazyCollection::make(function () {
    yield 1;
    yield 2;
    yield 3;
});

$collection = $lazyCollection->collect();

get_class($collection);

// 'Illuminate\Support\Collection'

$collection->all();

// [1, 2, 3]
```

> [!NOTE]
> `collect` 메서드는 `Enumerable` 계약의 일부이므로, `Enumerable` 인스턴스를 가지고 있을 때 일반 `Collection` 인스턴스를 안전하게 얻기 위해 사용됩니다.

<a name="method-combine"></a>
#### `combine()`

`combine` 메서드는 컬렉션의 값을 키로 하고, 다른 배열 또는 컬렉션의 값을 값으로 하여 합칩니다:

```
$collection = collect(['name', 'age']);

$combined = $collection->combine(['George', 29]);

$combined->all();

// ['name' => 'George', 'age' => 29]
```

<a name="method-concat"></a>
#### `concat()`

`concat` 메서드는 주어진 배열 또는 컬렉션의 값을 기존 컬렉션 끝에 덧붙입니다:

```
$collection = collect(['John Doe']);

$concatenated = $collection->concat(['Jane Doe'])->concat(['name' => 'Johnny Doe']);

$concatenated->all();

// ['John Doe', 'Jane Doe', 'Johnny Doe']
```

`concat` 메서드는 원래 컬렉션에 덧붙여진 항목들의 키를 숫자로 다시 인덱싱합니다. 연관 배열의 키를 유지하려면 [merge](#method-merge) 메서드를 사용하세요.

<a name="method-contains"></a>
#### `contains()`

`contains` 메서드는 컬렉션에 주어진 항목이 포함되어 있는지 판단합니다. 클로저를 전달할 수도 있어 어떤 요소가 조건을 만족하는지 검사할 수 있습니다:

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->contains(function ($value, $key) {
    return $value > 5;
});

// false
```

또는 값 자체를 전달할 수도 있습니다:

```
$collection = collect(['name' => 'Desk', 'price' => 100]);

$collection->contains('Desk');

// true

$collection->contains('New York');

// false
```

키와 값 쌍을 전달하여 해당 쌍이 존재하는지 확인할 수도 있습니다:

```
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
]);

$collection->contains('product', 'Bookcase');

// false
```

`contains` 메서드는 느슨한(loose) 비교를 사용하여 값 검사 시, 문자열 숫자와 정수 숫자를 같다고 간주합니다. 엄격 비교가 필요하다면 [`containsStrict`](#method-containsstrict) 메서드를 사용하세요.

`contains` 메서드의 반대 기능은 [doesntContain](#method-doesntcontain) 메서드를 참고하세요.

<a name="method-containsoneitem"></a>
#### `containsOneItem()`

`containsOneItem` 메서드는 컬렉션에 단 하나의 아이템만 있는지를 판단합니다:

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

이 메서드는 [`contains`](#method-contains)와 같은 시그니처를 가지지만 모든 값 검사에 대해 엄격(strict) 비교를 사용합니다.

> [!NOTE]
> [Eloquent Collections](/docs/9.x/eloquent-collections#method-contains)과 함께 사용할 경우 동작이 다를 수 있습니다.

<a name="method-count"></a>
#### `count()`

`count` 메서드는 컬렉션 내 항목 총 개수를 반환합니다:

```
$collection = collect([1, 2, 3, 4]);

$collection->count();

// 4
```

<a name="method-countBy"></a>
#### `countBy()`

`countBy` 메서드는 컬렉션 내 값들의 출현 횟수를 셉니다. 기본적으로는 모든 요소를 세지만, 클로저를 전달해 특정 기준으로 그룹별 개수를 셀 수도 있습니다:

```
$collection = collect([1, 2, 2, 2, 3]);

$counted = $collection->countBy();

$counted->all();

// [1 => 1, 2 => 3, 3 => 1]
```

클로저를 활용해 이메일 도메인별로 개수를 셀 수도 있습니다:

```
$collection = collect(['alice@gmail.com', 'bob@yahoo.com', 'carlos@gmail.com']);

$counted = $collection->countBy(function ($email) {
    return substr(strrchr($email, "@"), 1);
});

$counted->all();

// ['gmail.com' => 2, 'yahoo.com' => 1]
```

<a name="method-crossjoin"></a>
#### `crossJoin()`

`crossJoin` 메서드는 주어진 배열 또는 컬렉션과 컬렉션 값을 결합하여 모든 가능한 순열의 데카르트 곱(Cartesian product)을 반환합니다:

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

`dd` 메서드는 컬렉션 항목을 덤프하고 스크립트 실행을 종료합니다:

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

스크립트를 멈추지 않고 덤프만 원한다면 [`dump`](#method-dump) 메서드를 사용하세요.

<a name="method-diff"></a>
#### `diff()`

`diff` 메서드는 다른 컬렉션이나 배열과 값 기반으로 비교하여, 원래 컬렉션에 있지만 상대 컬렉션에는 없는 값을 반환합니다:

```
$collection = collect([1, 2, 3, 4, 5]);

$diff = $collection->diff([2, 4, 6, 8]);

$diff->all();

// [1, 3, 5]
```

> [!NOTE]
> [Eloquent Collections](/docs/9.x/eloquent-collections#method-diff)와 함께 쓰면 동작이 달라질 수 있습니다.

<a name="method-diffassoc"></a>
#### `diffAssoc()`

`diffAssoc` 메서드는 키와 값 모두를 기준으로 비교하여, 상대 컬렉션에 없는 키-값 쌍을 반환합니다:

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

<a name="method-diffkeys"></a>
#### `diffKeys()`

`diffKeys` 메서드는 키만 기준으로 비교하여 상대 컬렉션에 없는 키-값 쌍을 반환합니다:

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

`doesntContain` 메서드는 컬렉션에 주어진 항목이 없는지를 판단합니다. 클로저, 단순 값, 혹은 키/값 쌍을 인수로 받습니다:

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->doesntContain(function ($value, $key) {
    return $value < 5;
});

// false
```

값을 직접 검사할 수도 있습니다:

```
$collection = collect(['name' => 'Desk', 'price' => 100]);

$collection->doesntContain('Table');

// true

$collection->doesntContain('Desk');

// false
```

키-값 쌍으로 검사할 수도 있습니다:

```
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
]);

$collection->doesntContain('product', 'Bookcase');

// true
```

여기서도 느슨한(loose) 비교 방식을 사용합니다.

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

덤프 후 코드를 멈추려면 [`dd`](#method-dd) 메서드를 사용하세요.

<a name="method-duplicates"></a>
#### `duplicates()`

`duplicates` 메서드는 컬렉션 내 중복 값을 찾아 반환합니다:

```
$collection = collect(['a', 'b', 'a', 'c', 'b']);

$collection->duplicates();

// [2 => 'a', 4 => 'b']
```

배열이나 객체가 포함된 경우에는 중복 검사할 속성 이름을 키로 전달할 수 있습니다:

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

`duplicates` 메서드와 시그니처는 같으며, 모든 값 비교가 엄격(strict)한 방식으로 수행됩니다.

<a name="method-each"></a>
#### `each()`

`each` 메서드는 컬렉션의 항목들을 순회하며 각 항목에 대해 주어진 클로저를 호출합니다:

```
$collection->each(function ($item, $key) {
    //
});
```

순회를 멈추려면 클로저 내에서 `false`를 반환하세요:

```
$collection->each(function ($item, $key) {
    if (/* 조건 */) {
        return false;
    }
});
```

<a name="method-eachspread"></a>
#### `eachSpread()`

`eachSpread` 메서드는 중첩된 항목값을 클로저의 각 인수로 분리하여 순회합니다:

```
$collection = collect([['John Doe', 35], ['Jane Doe', 33]]);

$collection->eachSpread(function ($name, $age) {
    //
});
```

`false` 반환 시 순회 중단도 가능합니다:

```
$collection->eachSpread(function ($name, $age) {
    return false;
});
```

<a name="method-every"></a>
#### `every()`

`every` 메서드는 컬렉션 내 모든 요소가 주어진 조건을 만족하는지 검증합니다:

```
collect([1, 2, 3, 4])->every(function ($value, $key) {
    return $value > 2;
});

// false
```

빈 컬렉션일 경우 `true`를 반환합니다:

```
$collection = collect([]);

$collection->every(function ($value, $key) {
    return $value > 2;
});

// true
```

<a name="method-except"></a>
#### `except()`

`except` 메서드는 주어진 키들을 제외한 컬렉션의 모든 항목을 반환합니다:

```
$collection = collect(['product_id' => 1, 'price' => 100, 'discount' => false]);

$filtered = $collection->except(['price', 'discount']);

$filtered->all();

// ['product_id' => 1]
```

반대 메서드는 [only](#method-only)입니다.

> [!NOTE]
> [Eloquent Collections](/docs/9.x/eloquent-collections#method-except)에서는 동작이 다를 수 있습니다.

<a name="method-filter"></a>
#### `filter()`

`filter` 메서드는 주어진 조건에 통과하는 항목만 남깁니다:

```
$collection = collect([1, 2, 3, 4]);

$filtered = $collection->filter(function ($value, $key) {
    return $value > 2;
});

$filtered->all();

// [3, 4]
```

콜백을 넘기지 않으면 `false`로 간주되는 모든 항목을 제거합니다:

```
$collection = collect([1, 2, 3, null, false, '', 0, []]);

$collection->filter()->all();

// [1, 2, 3]
```

반대 메서드는 [reject](#method-reject)입니다.

<a name="method-first"></a>
#### `first()`

`first` 메서드는 주어진 조건을 만족하는 첫 번째 요소를 반환합니다:

```
collect([1, 2, 3, 4])->first(function ($value, $key) {
    return $value > 2;
});

// 3
```

인자를 안 넘기면 첫 번째 요소를 반환하며, 컬렉션이 비어있으면 `null`을 반환합니다:

```
collect([1, 2, 3, 4])->first();

// 1
```

<a name="method-first-or-fail"></a>
#### `firstOrFail()`

`first`와 동일하나 결과가 없으면 `Illuminate\Support\ItemNotFoundException` 예외를 던집니다:

```
collect([1, 2, 3, 4])->firstOrFail(function ($value, $key) {
    return $value > 5;
});

// ItemNotFoundException 발생
```

인자를 비워 호출해도 컬렉션이 비었으면 예외가 발생합니다:

```
collect([])->firstOrFail();

// ItemNotFoundException 발생
```

<a name="method-first-where"></a>
#### `firstWhere()`

주어진 키-값 쌍에 일치하는 첫 번째 요소를 반환합니다:

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

비교 연산자를 전달할 수도 있습니다:

```
$collection->firstWhere('age', '>=', 18);

// ['name' => 'Diego', 'age' => 23]
```

또는 한 인자만 넘겨서 해당 키의 값이 "truthy"인 첫 아이템을 반환할 수 있습니다:

```
$collection->firstWhere('age');

// ['name' => 'Linda', 'age' => 14]
```

---

이어서 다른 메서드 항목에 대해서도 동일한 양식과 형식으로 번역 원문과 일치하도록 자연스럽고 명확하게 이어서 번역해드립니다.