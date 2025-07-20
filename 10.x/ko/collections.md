# 컬렉션 (Collections)

- [소개](#introduction)
    - [컬렉션 생성](#creating-collections)
    - [컬렉션 확장하기](#extending-collections)
- [사용 가능한 메서드](#available-methods)
- [고차 메시지](#higher-order-messages)
- [지연 컬렉션](#lazy-collections)
    - [소개](#lazy-collection-introduction)
    - [지연 컬렉션 생성](#creating-lazy-collections)
    - [Enumerable 계약](#the-enumerable-contract)
    - [지연 컬렉션 메서드](#lazy-collection-methods)

<a name="introduction"></a>
## 소개

`Illuminate\Support\Collection` 클래스는 데이터 배열을 다루기 위한 유연하고 편리한 래퍼를 제공합니다. 예를 들어, 아래 코드를 살펴보십시오. `collect` 헬퍼를 이용하여 배열에서 새로운 컬렉션 인스턴스를 생성한 후, 각 요소에 `strtoupper` 함수를 적용하고, 빈 값을 모두 제거합니다.

```
$collection = collect(['taylor', 'abigail', null])->map(function (?string $name) {
    return strtoupper($name);
})->reject(function (string $name) {
    return empty($name);
});
```

이 예시처럼 `Collection` 클래스는 메서드 체이닝을 통해 기본 배열을 유연하게 매핑 및 축약할 수 있도록 해줍니다. 일반적으로 컬렉션은 불변(immutable)합니다. 즉, 각 `Collection` 메서드는 완전히 새로운 `Collection` 인스턴스를 반환합니다.

<a name="creating-collections"></a>
### 컬렉션 생성

앞에서 설명했듯이, `collect` 헬퍼는 주어진 배열에 대해 새로운 `Illuminate\Support\Collection` 인스턴스를 반환합니다. 따라서 컬렉션을 만드는 것은 아래와 같이 매우 간단합니다.

```
$collection = collect([1, 2, 3]);
```

> [!NOTE]  
> [Eloquent](/docs/10.x/eloquent) 쿼리의 결과는 항상 `Collection` 인스턴스로 반환됩니다.

<a name="extending-collections"></a>
### 컬렉션 확장하기

컬렉션은 "매크로 가능(macroable)"하므로 실행 중에 `Collection` 클래스에 추가 메서드를 동적으로 추가할 수 있습니다. `Illuminate\Support\Collection` 클래스의 `macro` 메서드는 나중에 매크로가 호출될 때 실행될 클로저를 인자로 받습니다. 이 매크로 클로저 안에서는 `$this`를 통해 컬렉션의 다른 메서드에 접근할 수 있으며, 마치 컬렉션 클래스의 실제 메서드처럼 작동합니다. 예를 들어, 아래 코드는 `Collection` 클래스에 `toUpper` 메서드를 추가합니다.

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

일반적으로 컬렉션 매크로는 [서비스 프로바이더](/docs/10.x/providers)의 `boot` 메서드에서 선언해야 합니다.

<a name="macro-arguments"></a>
#### 매크로 인수

필요하다면, 추가 인수를 받는 매크로도 정의할 수 있습니다.

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

이후의 컬렉션 문서에서는 `Collection` 클래스에서 사용할 수 있는 각 메서드에 대해 다룹니다. 이 모든 메서드는 기본 배열을 유연하게 조작하기 위해 체이닝할 수 있다는 점을 기억해두십시오. 또한, 거의 모든 메서드는 새로운 `Collection` 인스턴스를 반환하므로, 필요하다면 기존 컬렉션의 원본을 보존할 수 있습니다.

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

`all` 메서드는 컬렉션이 표현하는 원본 배열을 반환합니다.

```
collect([1, 2, 3])->all();

// [1, 2, 3]
```

<a name="method-average"></a>
#### `average()`

[`avg`](#method-avg) 메서드의 별칭입니다.

<a name="method-avg"></a>
#### `avg()`

`avg` 메서드는 지정한 키의 [평균값](https://en.wikipedia.org/wiki/Average)을 반환합니다.

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

`chunk` 메서드는 컬렉션을 지정한 크기만큼 여러 개의 더 작은 컬렉션으로 나눕니다.

```
$collection = collect([1, 2, 3, 4, 5, 6, 7]);

$chunks = $collection->chunk(4);

$chunks->all();

// [[1, 2, 3, 4], [5, 6, 7]]
```

이 메서드는 [Bootstrap](https://getbootstrap.com/docs/4.1/layout/grid/)과 같은 그리드 시스템을 사용하는 [뷰](/docs/10.x/views)에서 특히 유용합니다. 예를 들어, 그리드 형태로 보여주고 싶은 [Eloquent](/docs/10.x/eloquent) 모델 컬렉션이 있다고 가정해 보겠습니다.

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

`chunkWhile` 메서드는 주어진 콜백의 평가 결과에 따라 컬렉션을 여러 개의 더 작은 컬렉션으로 나눕니다. 클로저로 전달되는 `$chunk` 변수는 이전의 요소를 확인할 때 사용할 수 있습니다.

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

`collapse` 메서드는 배열로 이루어진 컬렉션을 하나의 평평한 컬렉션으로 펼칩니다.

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

`collect` 메서드는 현재 컬렉션 내의 항목으로 새로운 `Collection` 인스턴스를 반환합니다.

```
$collectionA = collect([1, 2, 3]);

$collectionB = $collectionA->collect();

$collectionB->all();

// [1, 2, 3]
```

`collect` 메서드는 주로 [지연 컬렉션](#lazy-collections)을 일반 `Collection` 인스턴스로 변환할 때 유용합니다.

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
> `collect` 메서드는 `Enumerable` 인스턴스를 사용할 때, 일반(비-지연) 컬렉션 인스턴스를 얻고 싶을 때 특히 유용합니다. `collect()`는 `Enumerable` 계약(Contract)의 일부이므로, `Collection` 인스턴스를 안전하게 얻기 위해 사용할 수 있습니다.

<a name="method-combine"></a>
#### `combine()`

`combine` 메서드는 현재 컬렉션의 값들을 키로, 다른 배열이나 컬렉션의 값들을 값으로 결합합니다.

```
$collection = collect(['name', 'age']);

$combined = $collection->combine(['George', 29]);

$combined->all();

// ['name' => 'George', 'age' => 29]
```

<a name="method-concat"></a>
#### `concat()`

`concat` 메서드는 주어진 배열이나 컬렉션의 값을 현재 컬렉션의 마지막에 추가합니다.

```
$collection = collect(['John Doe']);

$concatenated = $collection->concat(['Jane Doe'])->concat(['name' => 'Johnny Doe']);

$concatenated->all();

// ['John Doe', 'Jane Doe', 'Johnny Doe']
```

`concat` 메서드는 원래 컬렉션에 추가된 항목의 키를 숫자 인덱스로 다시 할당합니다. 연관 배열(associative collection)의 키를 유지하려면 [merge](#method-merge) 메서드를 참고하세요.

<a name="method-contains"></a>
#### `contains()`

`contains` 메서드는 컬렉션에 특정 항목이 포함되어 있는지 확인합니다. 클로저를 전달하여 컬렉션에서 주어진 조건을 만족하는 요소가 있는지 검사할 수 있습니다.

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->contains(function (int $value, int $key) {
    return $value > 5;
});

// false
```

또는, 검사하려는 항목 값을 문자열로 직접 전달할 수도 있습니다.

```
$collection = collect(['name' => 'Desk', 'price' => 100]);

$collection->contains('Desk');

// true

$collection->contains('New York');

// false
```

또한, 키 / 값 쌍을 전달하여 해당 쌍이 컬렉션에 존재하는지 확인할 수도 있습니다.

```
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
]);

$collection->contains('product', 'Bookcase');

// false
```

`contains` 메서드는 항목 값을 비교할 때 "느슨한(loose)" 비교를 사용합니다. 즉, 정수 값이 문자열로 되어 있어도 값이 같으면 같다고 판단합니다. "엄격한(strict)" 비교를 원한다면 [`containsStrict`](#method-containsstrict) 메서드를 사용하세요.

`contains`의 반대 기능이 필요하다면 [doesntContain](#method-doesntcontain) 메서드를 참고하십시오.

<a name="method-containsoneitem"></a>
#### `containsOneItem()`

`containsOneItem` 메서드는 컬렉션이 단 하나의 항목만 포함하는지 여부를 판별합니다.

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

이 메서드는 [`contains`](#method-contains) 메서드와 동일한 시그니처를 가지지만, 모든 값은 "엄격한(strict)" 비교로 판단합니다.

> [!NOTE]  
> [Eloquent 컬렉션](/docs/10.x/eloquent-collections#method-contains)에서 이 메서드의 동작이 달라질 수 있습니다.

<a name="method-count"></a>
#### `count()`

`count` 메서드는 컬렉션 내의 항목 전체 개수를 반환합니다.

```
$collection = collect([1, 2, 3, 4]);

$collection->count();

// 4
```

<a name="method-countBy"></a>
#### `countBy()`

`countBy` 메서드는 컬렉션 내 값들의 출현 횟수를 셉니다. 기본적으로 각 요소의 발생 횟수를 모두 카운트하여, 컬렉션 내 특정 "종류"의 요소 개수를 셀 수 있습니다.

```
$collection = collect([1, 2, 2, 2, 3]);

$counted = $collection->countBy();

$counted->all();

// [1 => 1, 2 => 3, 3 => 1]
```

콜백을 전달하여 모든 항목을 특정 값 기준으로 그룹화해서 개수를 셀 수도 있습니다.

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

`crossJoin` 메서드는 컬렉션의 값들과 전달된 배열 또는 컬렉션들을 교차 조인하여 카르테시안 곱(모든 가능한 조합)을 반환합니다.

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

`dd` 메서드는 컬렉션 항목을 출력하고, 스크립트 실행을 즉시 종료합니다.

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

스크립트 실행을 멈추지 않고 항목만 출력하고 싶다면 [`dump`](#method-dump) 메서드를 사용하십시오.

<a name="method-diff"></a>
#### `diff()`

`diff` 메서드는 해당 컬렉션과 다른 컬렉션 또는 일반 PHP `array`의 값들을 비교하여, 주어진 컬렉션에 없는 원본 컬렉션의 값만 반환합니다.

```
$collection = collect([1, 2, 3, 4, 5]);

$diff = $collection->diff([2, 4, 6, 8]);

$diff->all();

// [1, 3, 5]
```

> [!NOTE]  
> [Eloquent 컬렉션](/docs/10.x/eloquent-collections#method-diff)에서 이 메서드의 동작이 달라질 수 있습니다.

<a name="method-diffassoc"></a>
#### `diffAssoc()`

`diffAssoc` 메서드는 키와 값을 기준으로, 컬렉션과 다른 컬렉션 또는 일반 PHP `array`를 비교합니다. 이 메서드는 주어진 컬렉션에 존재하지 않는 원본 컬렉션의 키/값 쌍만 반환합니다.

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

`diffAssoc`와 달리, `diffAssocUsing`은 인덱스(키) 비교를 위해 사용자가 제공한 콜백 함수를 사용할 수 있습니다.

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

콜백 함수는 0보다 작거나, 같거나, 크거나 한 정수를 반환하는 비교 함수여야 합니다. 자세한 내용은 PHP 공식 문서의 [`array_diff_uassoc`](https://www.php.net/array_diff_uassoc#refsect1-function.array-diff-uassoc-parameters)를 참고하십시오. 이 PHP 함수는 `diffAssocUsing` 메서드가 내부적으로 사용하는 함수입니다.

<a name="method-diffkeys"></a>
#### `diffKeys()`

`diffKeys` 메서드는 컬렉션과 다른 컬렉션 또는 일반 PHP `array`의 키를 기준으로 비교하여, 주어진 컬렉션에 없는 원본 컬렉션의 키/값 쌍을 반환합니다.

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

`doesntContain` 메서드는 컬렉션에 특정 항목이 *포함되어 있지 않은지* 확인합니다. 클로저를 전달하여 컬렉션에 주어진 조건을 만족하지 않는 요소가 있는지 확인할 수 있습니다.

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->doesntContain(function (int $value, int $key) {
    return $value < 5;
});

// false
```

또는, 검사하려는 값을 문자열로 직접 전달할 수도 있습니다.

```
$collection = collect(['name' => 'Desk', 'price' => 100]);

$collection->doesntContain('Table');

// true

$collection->doesntContain('Desk');

// false
```

키 / 값 쌍을 전달하여 해당 쌍이 컬렉션에 *존재하지 않는지* 검사할 수도 있습니다.

```
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
]);

$collection->doesntContain('product', 'Bookcase');

// true
```

`doesntContain` 메서드는 항목 값을 비교할 때 "느슨한(loose)" 비교를 사용하므로, 값을 문자열이나 정수로 입력해도 값이 같으면 같다고 판단합니다.

<a name="method-dot"></a>

#### `dot()`

`dot` 메서드는 다차원 컬렉션을 "점(dot)" 표기법을 사용하여, 깊이를 나타내는 단일 수준의 컬렉션으로 평탄화(flatten)합니다.

```
$collection = collect(['products' => ['desk' => ['price' => 100]]]);

$flattened = $collection->dot();

$flattened->all();

// ['products.desk.price' => 100]
```

<a name="method-dump"></a>
#### `dump()`

`dump` 메서드는 컬렉션의 아이템들을 출력(dump)합니다.

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

컬렉션을 출력한 후 스크립트 실행을 중지하고 싶다면 [`dd`](#method-dd) 메서드를 사용하십시오.

<a name="method-duplicates"></a>
#### `duplicates()`

`duplicates` 메서드는 컬렉션에서 중복된 값을 찾아 반환합니다.

```
$collection = collect(['a', 'b', 'a', 'c', 'b']);

$collection->duplicates();

// [2 => 'a', 4 => 'b']
```

컬렉션에 배열이나 객체가 포함되어 있다면, 중복 값을 검사하고 싶은 속성의 키를 인수로 전달할 수 있습니다.

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

이 메서드는 [`duplicates`](#method-duplicates) 메서드와 동일한 시그니처를 가지고 있습니다. 다만, 모든 값의 비교를 "엄격한 비교(strict)"로 수행합니다.

<a name="method-each"></a>
#### `each()`

`each` 메서드는 컬렉션의 모든 아이템을 순회하며, 각 아이템을 클로저(익명 함수)에 전달합니다.

```
$collection = collect([1, 2, 3, 4]);

$collection->each(function (int $item, int $key) {
    // ...
});
```

순회를 중단하고 싶을 경우, 클로저에서 `false`를 반환하면 됩니다.

```
$collection->each(function (int $item, int $key) {
    if (/* condition */) {
        return false;
    }
});
```

<a name="method-eachspread"></a>
#### `eachSpread()`

`eachSpread` 메서드는 컬렉션의 아이템(중첩 배열 형태)을 순회하며, 각 중첩 아이템의 값을 콜백 함수의 인수로 펼쳐서 전달합니다.

```
$collection = collect([['John Doe', 35], ['Jane Doe', 33]]);

$collection->eachSpread(function (string $name, int $age) {
    // ...
});
```

반환값으로 `false`를 반환하면 순회가 중단됩니다.

```
$collection->eachSpread(function (string $name, int $age) {
    return false;
});
```

<a name="method-ensure"></a>
#### `ensure()`

`ensure` 메서드는 컬렉션의 모든 요소가 지정한 타입 또는 타입 목록에 해당하는지 검증합니다. 해당하지 않는 값이 존재하면 `UnexpectedValueException` 예외가 발생합니다.

```
return $collection->ensure(User::class);

return $collection->ensure([User::class, Customer::class]);
```

`string`, `int`, `float`, `bool`, `array`와 같은 원시 타입도 지정할 수 있습니다.

```
return $collection->ensure('int');
```

> [!WARNING]  
> `ensure` 메서드는 이후에 컬렉션에 다른 타입의 값이 추가되지 않음을 보장하지는 않습니다.

<a name="method-every"></a>
#### `every()`

`every` 메서드는 컬렉션의 모든 요소가 지정한 조건(참/거짓 판별)을 만족하는지 확인할 때 사용합니다.

```
collect([1, 2, 3, 4])->every(function (int $value, int $key) {
    return $value > 2;
});

// false
```

컬렉션이 비어 있다면, `every` 메서드는 항상 true를 반환합니다.

```
$collection = collect([]);

$collection->every(function (int $value, int $key) {
    return $value > 2;
});

// true
```

<a name="method-except"></a>
#### `except()`

`except` 메서드는 지정한 키를 가진 아이템을 제외한 컬렉션을 반환합니다.

```
$collection = collect(['product_id' => 1, 'price' => 100, 'discount' => false]);

$filtered = $collection->except(['price', 'discount']);

$filtered->all();

// ['product_id' => 1]
```

반대 동작을 원한다면 [only](#method-only) 메서드를 참조하세요.

> [!NOTE]  
> [Eloquent 컬렉션](/docs/10.x/eloquent-collections#method-except) 사용 시 이 메서드의 동작이 다르게 동작할 수 있습니다.

<a name="method-filter"></a>
#### `filter()`

`filter` 메서드는 주어진 콜백에 따라 컬렉션을 필터링하여, 조건에 해당하는 아이템만 남깁니다.

```
$collection = collect([1, 2, 3, 4]);

$filtered = $collection->filter(function (int $value, int $key) {
    return $value > 2;
});

$filtered->all();

// [3, 4]
```

콜백을 전달하지 않으면, `false`에 해당하는 값(빈 문자열, 0, null, false 등)이 모두 제거됩니다.

```
$collection = collect([1, 2, 3, null, false, '', 0, []]);

$collection->filter()->all();

// [1, 2, 3]
```

반대 동작을 원할 경우 [reject](#method-reject) 메서드를 확인하세요.

<a name="method-first"></a>
#### `first()`

`first` 메서드는 주어진 조건에 처음으로 부합하는 컬렉션의 요소를 반환합니다.

```
collect([1, 2, 3, 4])->first(function (int $value, int $key) {
    return $value > 2;
});

// 3
```

인수를 전달하지 않으면, 컬렉션의 첫 번째 요소를 반환합니다. 컬렉션이 비어있는 경우 `null`이 반환됩니다.

```
collect([1, 2, 3, 4])->first();

// 1
```

<a name="method-first-or-fail"></a>
#### `firstOrFail()`

`firstOrFail` 메서드는 `first` 메서드와 동일하게 동작하지만, 해당하는 결과가 없을 때 `Illuminate\Support\ItemNotFoundException` 예외를 발생시킵니다.

```
collect([1, 2, 3, 4])->firstOrFail(function (int $value, int $key) {
    return $value > 5;
});

// ItemNotFoundException 예외 발생...
```

인수를 전달하지 않으면, 컬렉션의 첫 번째 요소를 가져오며, 컬렉션이 비어 있는 경우 예외가 발생합니다.

```
collect([])->firstOrFail();

// ItemNotFoundException 예외 발생...
```

<a name="method-first-where"></a>
#### `firstWhere()`

`firstWhere` 메서드는 지정한 키/값 쌍에 부합하는 컬렉션의 첫 번째 요소를 반환합니다.

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

비교 연산자를 사용할 수도 있습니다.

```
$collection->firstWhere('age', '>=', 18);

// ['name' => 'Diego', 'age' => 23]
```

또한, [where](#method-where) 메서드와 마찬가지로 인자를 하나만 전달할 수도 있습니다. 이 경우, 지정한 키의 값이 true로 간주되는 첫 번째 아이템을 반환합니다.

```
$collection->firstWhere('age');

// ['name' => 'Linda', 'age' => 14]
```

<a name="method-flatmap"></a>
#### `flatMap()`

`flatMap` 메서드는 컬렉션의 각 값을 주어진 클로저에 전달하여 새로운 값으로 변환하고, 한 단계 평탄화(flatten)된 새로운 컬렉션을 생성합니다.

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

`flatten` 메서드는 다차원 컬렉션을 단일 차원의 컬렉션으로 평탄화합니다.

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

필요하다면 "depth" 인수를 사용해 평탄화할 단계 수를 지정할 수 있습니다.

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

이 예시에서 `flatten`을 depth를 지정하지 않고 사용할 경우, 중첩 배열까지 모두 평탄화되어 `['iPhone 6S', 'Apple', 'Galaxy S7', 'Samsung']`과 같은 결과가 됩니다. depth 파라미터를 사용하면 평탄화할 중첩 단계 수를 지정할 수 있습니다.

<a name="method-flip"></a>
#### `flip()`

`flip` 메서드는 컬렉션의 키와 값을 서로 뒤바꿉니다.

```
$collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

$flipped = $collection->flip();

$flipped->all();

// ['taylor' => 'name', 'laravel' => 'framework']
```

<a name="method-forget"></a>
#### `forget()`

`forget` 메서드는 지정한 키를 가진 아이템을 컬렉션에서 즉시 삭제합니다.

```
$collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

$collection->forget('name');

$collection->all();

// ['framework' => 'laravel']
```

> [!WARNING]  
> 대부분의 다른 컬렉션 메서드와는 달리, `forget`은 새 컬렉션을 반환하지 않고, 자신이 호출된 컬렉션 자체를 직접 수정합니다.

<a name="method-forpage"></a>
#### `forPage()`

`forPage` 메서드는 지정한 페이지 번호에 해당하는 아이템만 포함하는 새로운 컬렉션을 반환합니다. 첫 번째 인자는 페이지 번호, 두 번째 인자는 페이지당 보여줄 아이템 개수입니다.

```
$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9]);

$chunk = $collection->forPage(2, 3);

$chunk->all();

// [4, 5, 6]
```

<a name="method-get"></a>
#### `get()`

`get` 메서드는 지정한 키의 값을 반환합니다. 키가 없으면 `null`이 반환됩니다.

```
$collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

$value = $collection->get('name');

// taylor
```

두 번째 인자로 기본값을 지정할 수 있습니다.

```
$collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

$value = $collection->get('age', 34);

// 34
```

또한, 기본값으로 콜백을 전달하면 키가 존재하지 않을 때 콜백의 반환값이 사용됩니다.

```
$collection->get('email', function () {
    return 'taylor@example.com';
});

// taylor@example.com
```

<a name="method-groupby"></a>
#### `groupBy()`

`groupBy` 메서드는 컬렉션의 아이템을 지정한 키로 그룹화합니다.

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

문자열 키 대신 콜백 함수를 전달할 수도 있습니다. 콜백의 반환값이 그룹의 키로 사용됩니다.

```
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

여러 기준을 배열로 전달하여 다차원 배열에서 각 단계별로 그룹화할 수도 있습니다.

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

`has` 메서드는 지정한 키가 컬렉션에 존재하는지 확인합니다.

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

`hasAny` 메서드는 지정한 키들 중 하나라도 컬렉션에 존재하는지 확인합니다.

```
$collection = collect(['account_id' => 1, 'product' => 'Desk', 'amount' => 5]);

$collection->hasAny(['product', 'price']);

// true

$collection->hasAny(['name', 'price']);

// false
```

<a name="method-implode"></a>
#### `implode()`

`implode` 메서드는 컬렉션의 값을 특정 문자열로 연결(join)해줍니다. 컬렉션이 배열이나 객체라면, 합칠 속성의 키와 값을 연결할 문자열(glue)을 인수로 전달해야 합니다.

```
$collection = collect([
    ['account_id' => 1, 'product' => 'Desk'],
    ['account_id' => 2, 'product' => 'Chair'],
]);

$collection->implode('product', ', ');

// Desk, Chair
```

컬렉션이 단순 문자열이나 숫자값을 가진 경우, glue만 인수로 전달하면 됩니다.

```
collect([1, 2, 3, 4, 5])->implode('-');

// '1-2-3-4-5'
```

값을 결합하기 전 포맷팅이 필요하다면, 콜백을 전달할 수도 있습니다.

```
$collection->implode(function (array $item, int $key) {
    return strtoupper($item['product']);
}, ', ');

// DESK, CHAIR
```

<a name="method-intersect"></a>
#### `intersect()`

`intersect` 메서드는 원본 컬렉션에 존재하면서, 지정한 배열 또는 컬렉션에도 존재하는 값만 남기고 반환합니다. 반환 결과는 원본 컬렉션의 키를 그대로 유지합니다.

```
$collection = collect(['Desk', 'Sofa', 'Chair']);

$intersect = $collection->intersect(['Desk', 'Chair', 'Bookcase']);

$intersect->all();

// [0 => 'Desk', 2 => 'Chair']
```

> [!NOTE]  
> [Eloquent 컬렉션](/docs/10.x/eloquent-collections#method-intersect) 사용 시 이 메서드의 동작이 다르게 동작할 수 있습니다.

<a name="method-intersectAssoc"></a>
#### `intersectAssoc()`

`intersectAssoc` 메서드는 원본 컬렉션과 다른 컬렉션(또는 배열)과 비교하여, 모두에 존재하는 키/값 쌍만 남겨 반환합니다.

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

`intersectByKeys` 메서드는 원본 컬렉션에서, 지정한 배열 또는 컬렉션과 키가 서로 일치하는 키/값 쌍만 남깁니다.

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

`isEmpty` 메서드는 컬렉션이 비어 있으면 `true`를, 아니면 `false`를 반환합니다.

```
collect([])->isEmpty();

// true
```

<a name="method-isnotempty"></a>
#### `isNotEmpty()`

`isNotEmpty` 메서드는 컬렉션에 하나 이상의 아이템이 존재하면 `true`를, 아니면 `false`를 반환합니다.

```
collect([])->isNotEmpty();

// false
```

<a name="method-join"></a>
#### `join()`

`join` 메서드는 컬렉션의 값을 문자열로 조합합니다. 두 번째 인수를 사용하면 마지막 요소(마지막 두 요소 사이)에 삽입할 문자열을 지정할 수 있습니다.

```
collect(['a', 'b', 'c'])->join(', '); // 'a, b, c'
collect(['a', 'b', 'c'])->join(', ', ', and '); // 'a, b, and c'
collect(['a', 'b'])->join(', ', ' and '); // 'a and b'
collect(['a'])->join(', ', ' and '); // 'a'
collect([])->join(', ', ' and '); // ''
```

<a name="method-keyby"></a>
#### `keyBy()`

`keyBy` 메서드는 컬렉션을 지정한 키로 인덱싱합니다. 동일한 키를 가진 아이템이 여럿 있다면, 마지막 아이템만 새로운 컬렉션에 남게 됩니다.

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

메서드에 콜백을 전달하여, 해당 값을 키로 사용할 수도 있습니다.

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

`keys` 메서드는 컬렉션의 모든 키를 반환합니다.

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

`last` 메서드는 전달된 조건을 만족하는 컬렉션의 마지막 요소를 반환합니다.

```
collect([1, 2, 3, 4])->last(function (int $value, int $key) {
    return $value < 3;
});

// 2
```

`last` 메서드에 인자를 전달하지 않으면 컬렉션의 마지막 요소를 반환합니다. 컬렉션이 비어 있다면 `null`이 반환됩니다.

```
collect([1, 2, 3, 4])->last();

// 4
```

<a name="method-lazy"></a>
#### `lazy()`

`lazy` 메서드는 해당 아이템 배열로부터 새로운 [`LazyCollection`](#lazy-collections) 인스턴스를 반환합니다.

```
$lazyCollection = collect([1, 2, 3, 4])->lazy();

$lazyCollection::class;

// Illuminate\Support\LazyCollection

$lazyCollection->all();

// [1, 2, 3, 4]
```

이 기능은 많은 아이템을 가진 거대한 `Collection`에서 변환 작업을 수행해야 할 때 특히 유용합니다.

```
$count = $hugeCollection
    ->lazy()
    ->where('country', 'FR')
    ->where('balance', '>', '100')
    ->count();
```

컬렉션을 `LazyCollection`으로 변환할 경우, 대량의 추가 메모리 할당을 피할 수 있습니다. 원본 컬렉션은 _자신의_ 값은 메모리에 유지하지만, 이후 필터 작업에서는 추가적인 메모리를 거의 사용하지 않습니다. 따라서 결과를 필터링할 때 사실상 별도의 메모리 할당이 일어나지 않습니다.

<a name="method-macro"></a>
#### `macro()`

정적 메서드인 `macro`는 런타임에 `Collection` 클래스에 메서드를 추가할 수 있습니다. 자세한 내용은 [컬렉션 확장하기](#extending-collections) 문서를 참고하시기 바랍니다.

<a name="method-make"></a>
#### `make()`

정적 메서드인 `make`는 새로운 컬렉션 인스턴스를 생성합니다. 자세한 내용은 [컬렉션 생성하기](#creating-collections) 섹션을 참고하세요.

<a name="method-map"></a>
#### `map()`

`map` 메서드는 컬렉션을 순회하면서 각 값을 전달된 콜백 함수에 넘깁니다. 콜백은 아이템을 자유롭게 수정하고, 그 값을 반환하여, 수정된 아이템들로 새로운 컬렉션을 만듭니다.

```
$collection = collect([1, 2, 3, 4, 5]);

$multiplied = $collection->map(function (int $item, int $key) {
    return $item * 2;
});

$multiplied->all();

// [2, 4, 6, 8, 10]
```

> [!WARNING]  
> 대부분의 다른 컬렉션 메서드와 마찬가지로, `map`은 새 컬렉션 인스턴스를 반환하며, 원래의 컬렉션은 변경하지 않습니다. 원본 컬렉션 자체를 변환하려면 [`transform`](#method-transform) 메서드를 사용하세요.

<a name="method-mapinto"></a>
#### `mapInto()`

`mapInto()` 메서드는 컬렉션을 순회하며, 각 값을 생성자의 인수로 전달해서 지정한 클래스의 새 인스턴스를 생성합니다.

```
class Currency
{
    /**
     * 새로운 Currency 인스턴스 생성.
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

`mapSpread` 메서드는 컬렉션의 각 중첩 아이템 값을 전달된 클로저에 분해해서 넘깁니다. 클로저는 아이템을 자유롭게 수정하고, 그 값을 반환하여, 수정된 아이템들로 새로운 컬렉션을 만듭니다.

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

`mapToGroups` 메서드는 전달된 클로저를 사용해서 컬렉션의 아이템을 그룹별로 묶습니다. 클로저는 하나의 키/값 쌍만을 담은 연관 배열을 반환해야 하며, 이를 통해 그룹화된 새로운 컬렉션이 만들어집니다.

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

`mapWithKeys` 메서드는 컬렉션을 순회하면서 각 값을 전달된 콜백에 넘깁니다. 이 콜백은 반드시 하나의 키/값 쌍만을 담은 연관 배열을 반환해야 합니다.

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

`max` 메서드는 지정한 키에 대해 최대값을 반환합니다.

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

`median` 메서드는 주어진 키의 [중앙값](https://en.wikipedia.org/wiki/Median)을 반환합니다.

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

`merge` 메서드는 전달받은 배열 또는 컬렉션과 원본 컬렉션을 병합합니다. 만약 전달받은 아이템의 문자열 키가 원본 컬렉션의 문자열 키와 일치하면, 전달받은 아이템의 값이 원본 컬렉션의 값을 덮어씁니다.

```
$collection = collect(['product_id' => 1, 'price' => 100]);

$merged = $collection->merge(['price' => 200, 'discount' => false]);

$merged->all();

// ['product_id' => 1, 'price' => 200, 'discount' => false]
```

전달받은 아이템의 키가 숫자라면, 값이 컬렉션의 끝에 추가됩니다.

```
$collection = collect(['Desk', 'Chair']);

$merged = $collection->merge(['Bookcase', 'Door']);

$merged->all();

// ['Desk', 'Chair', 'Bookcase', 'Door']
```

<a name="method-mergerecursive"></a>
#### `mergeRecursive()`

`mergeRecursive` 메서드는 전달받은 배열 또는 컬렉션을 원본 컬렉션과 재귀적으로 병합합니다. 전달된 아이템과 원본 컬렉션의 문자열 키가 일치하면, 해당 키의 값들이 배열로 병합되며, 이 동작이 재귀적으로 반복됩니다.

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

`min` 메서드는 지정한 키에 대한 최소값을 반환합니다.

```
$min = collect([['foo' => 10], ['foo' => 20]])->min('foo');

// 10

$min = collect([1, 2, 3, 4, 5])->min();

// 1
```

<a name="method-mode"></a>
#### `mode()`

`mode` 메서드는 주어진 키에 대한 [최빈값](https://en.wikipedia.org/wiki/Mode_(statistics))을 반환합니다.

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

`nth` 메서드는 n번째마다의 요소들로 구성된 새로운 컬렉션을 만듭니다.

```
$collection = collect(['a', 'b', 'c', 'd', 'e', 'f']);

$collection->nth(4);

// ['a', 'e']
```

두 번째 인수로 시작 오프셋을 지정할 수도 있습니다.

```
$collection->nth(4, 1);

// ['b', 'f']
```

<a name="method-only"></a>
#### `only()`

`only` 메서드는 컬렉션에서 지정한 키의 아이템만 반환합니다.

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

`only`의 반대 동작은 [except](#method-except) 메서드를 참고하세요.

> [!NOTE]  
> [Eloquent 컬렉션](/docs/10.x/eloquent-collections#method-only)에서 사용할 때는 동작이 다르게 나타날 수 있습니다.

<a name="method-pad"></a>
#### `pad()`

`pad` 메서드는 배열의 크기가 지정한 크기에 도달할 때까지, 주어진 값으로 배열을 채웁니다. 이 메서드는 PHP의 [array_pad](https://secure.php.net/manual/en/function.array-pad.php) 함수와 비슷하게 동작합니다.

음수를 지정하면 배열의 왼쪽에 값을 채울 수 있습니다. 절대값이 배열의 길이보다 작거나 같으면 패딩은 적용되지 않습니다.

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

`partition` 메서드는 PHP의 배열 구조 분해와 함께 사용하여 주어진 조건을 만족하는 요소와 그렇지 않은 요소를 분리할 수 있습니다.

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

`percentage` 메서드는 컬렉션 내에서 주어진 조건을 만족하는 아이템의 비율을 빠르게 계산할 때 사용할 수 있습니다.

```php
$collection = collect([1, 1, 2, 2, 2, 3]);

$percentage = $collection->percentage(fn ($value) => $value === 1);

// 33.33
```

기본적으로 소수점 두 자리까지 반올림됩니다. 이 동작은 두 번째 인자로 지정해서 원하는 소수점 자리수를 변경할 수 있습니다.

```php
$percentage = $collection->percentage(fn ($value) => $value === 1, precision: 3);

// 33.333
```

<a name="method-pipe"></a>
#### `pipe()`

`pipe` 메서드는 컬렉션을 전달된 클로저에 넘기고, 그 실행 결과를 반환합니다.

```
$collection = collect([1, 2, 3]);

$piped = $collection->pipe(function (Collection $collection) {
    return $collection->sum();
});

// 6
```

<a name="method-pipeinto"></a>
#### `pipeInto()`

`pipeInto` 메서드는 지정한 클래스의 새 인스턴스를 만들고, 컬렉션을 생성자의 인수로 전달합니다.

```
class ResourceCollection
{
    /**
     * 새로운 ResourceCollection 인스턴스 생성.
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

`pipeThrough` 메서드는 컬렉션을 전달된 클로저 배열에 순서대로 넘기고, 실행 결과를 반환합니다.

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

`pluck` 메서드는 지정한 키에 해당하는 값을 모두 가져옵니다.

```
$collection = collect([
    ['product_id' => 'prod-100', 'name' => 'Desk'],
    ['product_id' => 'prod-200', 'name' => 'Chair'],
]);

$plucked = $collection->pluck('name');

$plucked->all();

// ['Desk', 'Chair']
```

반환되는 컬렉션의 키를 지정할 수도 있습니다.

```
$plucked = $collection->pluck('name', 'product_id');

$plucked->all();

// ['prod-100' => 'Desk', 'prod-200' => 'Chair']
```

`pluck` 메서드는 "dot" 표기법을 사용해 중첩 값을 가져오는 것도 지원합니다.

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

중복된 키가 있는 경우, 마지막 일치 요소가 pluck된 컬렉션에 삽입됩니다.

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

`pop` 메서드는 컬렉션에서 마지막 아이템을 제거하고 반환합니다.

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->pop();

// 5

$collection->all();

// [1, 2, 3, 4]
```

`pop` 메서드에 정수를 전달하면 컬렉션의 끝에서 여러 아이템을 제거하고 반환할 수 있습니다.

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->pop(3);

// collect([5, 4, 3])

$collection->all();

// [1, 2]
```

<a name="method-prepend"></a>
#### `prepend()`

`prepend` 메서드는 컬렉션의 맨 앞에 아이템을 추가합니다.

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->prepend(0);

$collection->all();

// [0, 1, 2, 3, 4, 5]
```

추가되는 아이템의 키를 두 번째 인수로 지정할 수도 있습니다.

```
$collection = collect(['one' => 1, 'two' => 2]);

$collection->prepend(0, 'zero');

$collection->all();

// ['zero' => 0, 'one' => 1, 'two' => 2]
```

<a name="method-pull"></a>
#### `pull()`

`pull` 메서드는 지정한 키의 아이템을 컬렉션에서 제거하고 값을 반환합니다.

```
$collection = collect(['product_id' => 'prod-100', 'name' => 'Desk']);

$collection->pull('name');

// 'Desk'

$collection->all();

// ['product_id' => 'prod-100']
```

<a name="method-push"></a>
#### `push()`

`push` 메서드는 컬렉션 끝에 아이템을 추가합니다.

```
$collection = collect([1, 2, 3, 4]);

$collection->push(5);

$collection->all();

// [1, 2, 3, 4, 5]
```

<a name="method-put"></a>
#### `put()`

`put` 메서드는 지정한 키와 값을 컬렉션에 설정합니다.

```
$collection = collect(['product_id' => 1, 'name' => 'Desk']);

$collection->put('price', 100);

$collection->all();

// ['product_id' => 1, 'name' => 'Desk', 'price' => 100]
```

<a name="method-random"></a>
#### `random()`

`random` 메서드는 컬렉션에서 무작위로 하나의 아이템을 반환합니다.

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->random();

// 4 - (랜덤하게 반환됨)
```

`random` 메서드에 정수를 전달해 원하는 개수만큼의 아이템을 무작위로 가져올 수도 있습니다. 개수를 지정하면 항상 여러 아이템으로 이루어진 컬렉션이 반환됩니다.

```
$random = $collection->random(3);

$random->all();

// [2, 4, 5] - (랜덤하게 반환됨)
```

만약 컬렉션에 요청한 개수보다 적은 아이템만 있다면, `random` 메서드는 `InvalidArgumentException`을 발생시킵니다.

`random` 메서드는 클로저도 인수로 받을 수 있으며, 현재 컬렉션 인스턴스가 전달됩니다.

```
use Illuminate\Support\Collection;

$random = $collection->random(fn (Collection $items) => min(10, count($items)));

$random->all();

// [1, 2, 3, 4, 5] - (랜덤하게 반환됨)
```

<a name="method-range"></a>

#### `range()`

`range` 메서드는 지정한 범위 내의 정수들로 이루어진 컬렉션을 반환합니다.

```
$collection = collect()->range(3, 6);

$collection->all();

// [3, 4, 5, 6]
```

<a name="method-reduce"></a>
#### `reduce()`

`reduce` 메서드는 컬렉션의 각 항목을 반복 처리하며 결과값을 다음 반복에 넘겨주어, 모든 항목을 하나의 값으로 줄여줍니다.

```
$collection = collect([1, 2, 3]);

$total = $collection->reduce(function (?int $carry, int $item) {
    return $carry + $item;
});

// 6
```

첫 번째 반복에서 `$carry`의 값은 `null`입니다. 하지만 두 번째 인자로 초기값을 지정할 수 있습니다.

```
$collection->reduce(function (int $carry, int $item) {
    return $carry + $item;
}, 4);

// 10
```

`reduce` 메서드는 연관 배열(Associative collection)의 경우 배열의 키도 콜백에 전달합니다.

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

`reduceSpread` 메서드는 반복 결과를 다음 반복에 넘겨주며, 컬렉션을 여러 값이 담긴 배열로 줄여줍니다. 이 메서드는 `reduce`와 비슷하지만, 다수의 초기값을 허용한다는 차이점이 있습니다.

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

`reject` 메서드는 주어진 클로저를 통해 필터링하여, 클로저가 `true`를 반환하는 항목을 컬렉션에서 제거합니다.

```
$collection = collect([1, 2, 3, 4]);

$filtered = $collection->reject(function (int $value, int $key) {
    return $value > 2;
});

$filtered->all();

// [1, 2]
```

`reject` 메서드의 반대 동작을 원한다면 [`filter`](#method-filter) 메서드를 참고하세요.

<a name="method-replace"></a>
#### `replace()`

`replace` 메서드는 `merge`와 유사하지만, 문자열 키뿐 아니라 동일한 숫자 키도 덮어씁니다.

```
$collection = collect(['Taylor', 'Abigail', 'James']);

$replaced = $collection->replace([1 => 'Victoria', 3 => 'Finn']);

$replaced->all();

// ['Taylor', 'Victoria', 'James', 'Finn']
```

<a name="method-replacerecursive"></a>
#### `replaceRecursive()`

이 메서드는 `replace`와 동작이 비슷하지만, 배열 내부까지 재귀적으로 들어가서 같은 방식으로 값을 교체합니다.

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

`reverse` 메서드는 컬렉션의 항목 순서를 뒤집어서 반환합니다. 이때 기존의 키는 그대로 보존됩니다.

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

`search` 메서드는 컬렉션에서 주어진 값을 찾아 그 키를 반환합니다. 값이 존재하지 않으면 `false`를 반환합니다.

```
$collection = collect([2, 4, 6, 8]);

$collection->search(4);

// 1
```

검색은 "느슨한(loose)" 비교로 진행되므로, 정수 값을 가진 문자열도 같은 값을 가진 정수와 같다고 간주됩니다. "엄격한(strict)" 비교를 사용하려면 두 번째 인자로 `true`를 전달하세요.

```
collect([2, 4, 6, 8])->search('4', $strict = true);

// false
```

또는 직접 클로저를 넘겨, 조건을 만족하는 첫 번째 항목의 키를 찾을 수도 있습니다.

```
collect([2, 4, 6, 8])->search(function (int $item, int $key) {
    return $item > 5;
});

// 2
```

<a name="method-select"></a>
#### `select()`

`select` 메서드는 지정한 키들만을 골라서 새로운 컬렉션으로 반환합니다. SQL의 `SELECT` 구문과 비슷한 역할을 합니다.

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

`shift` 메서드는 컬렉션의 첫 번째 항목을 제거하고, 그 값을 반환합니다.

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->shift();

// 1

$collection->all();

// [2, 3, 4, 5]
```

정수를 인자로 지정하면 컬렉션의 앞에서부터 여러 항목을 한 번에 제거하고 반환합니다.

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->shift(3);

// collect([1, 2, 3])

$collection->all();

// [4, 5]
```

<a name="method-shuffle"></a>
#### `shuffle()`

`shuffle` 메서드는 컬렉션의 항목들을 무작위로 섞어서 반환합니다.

```
$collection = collect([1, 2, 3, 4, 5]);

$shuffled = $collection->shuffle();

$shuffled->all();

// [3, 2, 5, 1, 4] - (무작위로 생성)
```

<a name="method-skip"></a>
#### `skip()`

`skip` 메서드는 컬렉션의 앞에서 지정한 개수만큼 항목을 제거한 새로운 컬렉션을 반환합니다.

```
$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);

$collection = $collection->skip(4);

$collection->all();

// [5, 6, 7, 8, 9, 10]
```

<a name="method-skipuntil"></a>
#### `skipUntil()`

`skipUntil` 메서드는 지정한 콜백이 `true`를 반환할 때까지 항목을 건너뛰고, 그 이후부터 남은 항목들을 새로운 컬렉션으로 반환합니다.

```
$collection = collect([1, 2, 3, 4]);

$subset = $collection->skipUntil(function (int $item) {
    return $item >= 3;
});

$subset->all();

// [3, 4]
```

또한 값 자체를 바로 넘겨서, 해당 값이 나올 때까지 건너뛸 수 있습니다.

```
$collection = collect([1, 2, 3, 4]);

$subset = $collection->skipUntil(3);

$subset->all();

// [3, 4]
```

> [!WARNING]  
> 지정한 값이 컬렉션에 없거나 콜백이 한 번도 `true`를 반환하지 않으면, `skipUntil` 메서드는 빈 컬렉션을 반환합니다.

<a name="method-skipwhile"></a>
#### `skipWhile()`

`skipWhile` 메서드는 콜백이 `true`를 반환하는 동안 항목을 건너뛰고, 조건이 해제되는 순간부터 남은 항목들을 새로운 컬렉션으로 반환합니다.

```
$collection = collect([1, 2, 3, 4]);

$subset = $collection->skipWhile(function (int $item) {
    return $item <= 3;
});

$subset->all();

// [4]
```

> [!WARNING]  
> 콜백이 한 번도 `false`를 반환하지 않으면, `skipWhile` 메서드는 빈 컬렉션을 반환합니다.

<a name="method-slice"></a>
#### `slice()`

`slice` 메서드는 지정한 인덱스부터 시작하는 컬렉션의 일부 항목(슬라이스)을 반환합니다.

```
$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);

$slice = $collection->slice(4);

$slice->all();

// [5, 6, 7, 8, 9, 10]
```

슬라이스 크기를 제한하고 싶으면 두 번째 인자로 원하는 크기를 넘기면 됩니다.

```
$slice = $collection->slice(4, 2);

$slice->all();

// [5, 6]
```

기본적으로 반환된 슬라이스는 원래의 키를 유지합니다. 키를 다시 0부터 정렬하려면 [`values`](#method-values) 메서드를 사용할 수 있습니다.

<a name="method-sliding"></a>
#### `sliding()`

`sliding` 메서드는 컬렉션의 항목들을 "슬라이딩 윈도우" 방식으로 묶어서 작은 청크들의 컬렉션을 만듭니다.

```
$collection = collect([1, 2, 3, 4, 5]);

$chunks = $collection->sliding(2);

$chunks->toArray();

// [[1, 2], [2, 3], [3, 4], [4, 5]]
```

특히 [`eachSpread`](#method-eachspread) 메서드와 함께 사용하면 유용합니다.

```
$transactions->sliding(2)->eachSpread(function (Collection $previous, Collection $current) {
    $current->total = $previous->total + $current->amount;
});
```

두 번째 인자로 "스텝(step)" 값을 넘기면, 각 청크의 시작 인덱스 간격을 조정할 수 있습니다.

```
$collection = collect([1, 2, 3, 4, 5]);

$chunks = $collection->sliding(3, step: 2);

$chunks->toArray();

// [[1, 2, 3], [3, 4, 5]]
```

<a name="method-sole"></a>
#### `sole()`

`sole` 메서드는 지정한 조건을 만족하는 컬렉션의 첫 번째 항목을 반환합니다. 단, 해당 조건을 만족하는 항목이 정확히 한 개일 때만 동작합니다.

```
collect([1, 2, 3, 4])->sole(function (int $value, int $key) {
    return $value === 2;
});

// 2
```

또는 key/value 쌍을 넘겨, 조건에 맞는 항목이 정확히 하나일 때 해당 항목을 반환할 수 있습니다.

```
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
]);

$collection->sole('product', 'Chair');

// ['product' => 'Chair', 'price' => 100]
```

아무런 인자 없이 호출하면, 컬렉션에 항목이 딱 하나일 때 그 항목을 반환합니다.

```
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
]);

$collection->sole();

// ['product' => 'Desk', 'price' => 200]
```

`sole` 메서드로 반환할 항목이 없으면 `\Illuminate\Collections\ItemNotFoundException` 예외가 발생합니다. 반환할 항목이 2개 이상이면 `\Illuminate\Collections\MultipleItemsFoundException` 예외가 발생합니다.

<a name="method-some"></a>
#### `some()`

[`contains`](#method-contains) 메서드의 별칭입니다.

<a name="method-sort"></a>
#### `sort()`

`sort` 메서드는 컬렉션을 정렬합니다. 정렬된 컬렉션도 기존의 배열 키를 유지하므로, 아래 예제처럼 [`values`](#method-values) 메서드로 인덱스를 재정렬할 수 있습니다.

```
$collection = collect([5, 3, 1, 2, 4]);

$sorted = $collection->sort();

$sorted->values()->all();

// [1, 2, 3, 4, 5]
```

좀 더 복잡한 정렬이 필요하다면, 콜백을 전달해 직접 정렬 알고리즘을 지정할 수 있습니다. 내부적으로 컬렉션의 `sort` 메서드는 PHP의 [`uasort`](https://secure.php.net/manual/en/function.uasort.php#refsect1-function.uasort-parameters) 함수를 사용합니다.

> [!NOTE]  
> 중첩 배열이나 객체로 이루어진 컬렉션을 정렬하려면 [`sortBy`](#method-sortby), [`sortByDesc`](#method-sortbydesc) 메서드를 참고하세요.

<a name="method-sortby"></a>
#### `sortBy()`

`sortBy` 메서드는 지정한 키를 기준으로 컬렉션을 정렬합니다. 정렬된 컬렉션도 기존의 배열 키를 유지하므로, 인덱스를 다시 매기려면 [`values`](#method-values) 메서드를 사용할 수 있습니다.

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

두 번째 인자로 [정렬 플래그(sort flags)](https://www.php.net/manual/en/function.sort.php)도 전달할 수 있습니다.

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

또는 클로저를 넘겨서 정렬 기준을 직접 정의할 수도 있습니다.

```
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

여러 개의 속성 기준으로 정렬하고 싶을 때는, 각 정렬 기준 속성명을 배열로 넘길 수 있습니다.

```
$collection = collect([
    ['name' => 'Taylor Otwell', 'age' => 34],
    ['name' => 'Abigail Otwell', 'age' => 30],
    ['name' => 'Taylor Otwell', 'age' => 36],
    ['name' => 'Abigail Otwell', 'age' => 32],
]);

$sorted = $collection->sortBy(['name', 'age']);

$sorted->values()->all();

/*
    [
        ['name' => 'Abigail Otwell', 'age' => 30],
        ['name' => 'Abigail Otwell', 'age' => 32],
        ['name' => 'Taylor Otwell', 'age' => 34],
        ['name' => 'Taylor Otwell', 'age' => 36],
    ]
*/
```

여러 속성에 대해 정렬 방향까지 직접 지정하고 싶다면, 각 정렬 연산을 속성-방향 쌍이 담긴 배열로 넘겨줄 수 있습니다.

```
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

여러 정렬 기준을 각각 클로저로 지정하는 것도 가능합니다.

```
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

이 메서드는 [`sortBy`](#method-sortby) 메서드와 시그니처가 같지만, 반대 방향(내림차순)으로 정렬합니다.

<a name="method-sortdesc"></a>
#### `sortDesc()`

이 메서드는 [`sort`](#method-sort) 메서드와 반대로 컬렉션을 내림차순(반대 순서)으로 정렬합니다.

```
$collection = collect([5, 3, 1, 2, 4]);

$sorted = $collection->sortDesc();

$sorted->values()->all();

// [5, 4, 3, 2, 1]
```

`sort`와는 달리, `sortDesc`에는 클로저를 넘길 수 없습니다. 직접 비교 함수를 사용해야 한다면 [`sort`](#method-sort) 메서드에서 비교 순서를 반대로 하세요.

<a name="method-sortkeys"></a>
#### `sortKeys()`

`sortKeys` 메서드는 컬렉션 내부 연관 배열의 키(키 값 기준)로 정렬합니다.

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

이 메서드는 [`sortKeys`](#method-sortkeys) 메서드와 시그니처가 같지만, 키 기준 내림차순 정렬을 합니다.

<a name="method-sortkeysusing"></a>
#### `sortKeysUsing()`

`sortKeysUsing` 메서드는 연관 배열의 키로 정렬을 할 때, 정렬 기준을 정의하는 콜백을 사용할 수 있습니다.

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

이때 콜백 함수는 두 값을 비교해 0보다 작거나 같거나 큰 정수 값을 반환해야 합니다. 자세한 내용은 PHP의 [`uksort`](https://www.php.net/manual/en/function.uksort.php#refsect1-function.uksort-parameters) 문서를 참고하세요. 이 메서드는 내부적으로 해당 PHP 함수를 사용합니다.

<a name="method-splice"></a>
#### `splice()`

`splice` 메서드는 지정한 인덱스부터 시작하는 항목들을 잘라내 컬렉션에서 제거하며, 잘라낸 항목들로 새로운 컬렉션을 반환합니다.

```
$collection = collect([1, 2, 3, 4, 5]);

$chunk = $collection->splice(2);

$chunk->all();

// [3, 4, 5]

$collection->all();

// [1, 2]
```

두 번째 인자로 반환될 컬렉션의 크기를 지정할 수도 있습니다.

```
$collection = collect([1, 2, 3, 4, 5]);

$chunk = $collection->splice(2, 1);

$chunk->all();

// [3]

$collection->all();

// [1, 2, 4, 5]
```

추가로, 세 번째 인자로 컬렉션에서 잘라낸 자리에 새 항목들을 대체할 수도 있습니다.

```
$collection = collect([1, 2, 3, 4, 5]);

$chunk = $collection->splice(2, 1, [10, 11]);

$chunk->all();

// [3]

$collection->all();

// [1, 2, 10, 11, 4, 5]
```

<a name="method-split"></a>

#### `split()`

`split` 메서드는 컬렉션을 지정한 개수의 그룹으로 분할합니다.

```
$collection = collect([1, 2, 3, 4, 5]);

$groups = $collection->split(3);

$groups->all();

// [[1, 2], [3, 4], [5]]
```

<a name="method-splitin"></a>
#### `splitIn()`

`splitIn` 메서드는 컬렉션을 지정한 개수의 그룹으로 나누되, 마지막 그룹을 제외한 나머지 그룹들이 최대한 균등하게 아이템을 채우도록 나눕니다.

```
$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);

$groups = $collection->splitIn(3);

$groups->all();

// [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10]]
```

<a name="method-sum"></a>
#### `sum()`

`sum` 메서드는 컬렉션의 모든 아이템의 합계를 반환합니다.

```
collect([1, 2, 3, 4, 5])->sum();

// 15
```

컬렉션 안에 중첩 배열이나 객체가 있다면, 합계를 계산할 값을 결정할 키를 전달해야 합니다.

```
$collection = collect([
    ['name' => 'JavaScript: The Good Parts', 'pages' => 176],
    ['name' => 'JavaScript: The Definitive Guide', 'pages' => 1096],
]);

$collection->sum('pages');

// 1272
```

추가로, 합계를 계산할 값을 직접 정할 수 있도록 콜백을 전달할 수도 있습니다.

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

`take` 메서드는 지정된 개수만큼의 아이템이 담긴 새로운 컬렉션을 반환합니다.

```
$collection = collect([0, 1, 2, 3, 4, 5]);

$chunk = $collection->take(3);

$chunk->all();

// [0, 1, 2]
```

음수 값을 전달하면 컬렉션의 끝에서부터 지정한 개수만큼의 아이템을 가져올 수 있습니다.

```
$collection = collect([0, 1, 2, 3, 4, 5]);

$chunk = $collection->take(-2);

$chunk->all();

// [4, 5]
```

<a name="method-takeuntil"></a>
#### `takeUntil()`

`takeUntil` 메서드는 주어진 콜백이 `true`를 반환할 때까지 컬렉션의 아이템을 반환합니다.

```
$collection = collect([1, 2, 3, 4]);

$subset = $collection->takeUntil(function (int $item) {
    return $item >= 3;
});

$subset->all();

// [1, 2]
```

또한 값을 직접 전달하면, 해당 값을 찾을 때까지의 아이템을 반환합니다.

```
$collection = collect([1, 2, 3, 4]);

$subset = $collection->takeUntil(3);

$subset->all();

// [1, 2]
```

> [!WARNING]  
> 만약 주어진 값이 컬렉션에 없거나, 콜백이 한 번도 `true`를 반환하지 않으면, `takeUntil` 메서드는 컬렉션의 모든 아이템을 반환합니다.

<a name="method-takewhile"></a>
#### `takeWhile()`

`takeWhile` 메서드는 주어진 콜백이 `false`를 반환할 때까지 컬렉션의 아이템을 반환합니다.

```
$collection = collect([1, 2, 3, 4]);

$subset = $collection->takeWhile(function (int $item) {
    return $item < 3;
});

$subset->all();

// [1, 2]
```

> [!WARNING]  
> 콜백이 한 번도 `false`를 반환하지 않으면, `takeWhile` 메서드는 컬렉션의 모든 아이템을 반환합니다.

<a name="method-tap"></a>
#### `tap()`

`tap` 메서드는 컬렉션을 주어진 콜백에 전달하여, 컬렉션을 반환하기 전에 특정 작업을 수행할 수 있게 해줍니다. 이때 컬렉션 자체에는 영향을 주지 않습니다. `tap` 메서드는 무조건 컬렉션 본인을 반환합니다.

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

정적 메서드인 `times`는 지정된 횟수만큼 콜백을 실행하여, 그 결과로 이뤄진 새로운 컬렉션을 만듭니다.

```
$collection = Collection::times(10, function (int $number) {
    return $number * 9;
});

$collection->all();

// [9, 18, 27, 36, 45, 54, 63, 72, 81, 90]
```

<a name="method-toarray"></a>
#### `toArray()`

`toArray` 메서드는 컬렉션을 일반 PHP `array`로 변환합니다. 만약 컬렉션 값이 [Eloquent](/docs/10.x/eloquent) 모델이라면, 모델도 배열로 변환됩니다.

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
> `toArray`는 컬렉션 안에 있는 모든 중첩 객체 중 `Arrayable` 인스턴스를 배열로 변환합니다. 컬렉션 내부의 원시 배열만 가져오고 싶다면 [`all`](#method-all) 메서드를 사용하세요.

<a name="method-tojson"></a>
#### `toJson()`

`toJson` 메서드는 컬렉션을 JSON 직렬화된 문자열로 변환합니다.

```
$collection = collect(['name' => 'Desk', 'price' => 200]);

$collection->toJson();

// '{"name":"Desk", "price":200}'
```

<a name="method-transform"></a>
#### `transform()`

`transform` 메서드는 컬렉션의 각 아이템을 순회하며, 전달된 콜백을 실행해 그 반환값으로 아이템을 대체합니다.

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->transform(function (int $item, int $key) {
    return $item * 2;
});

$collection->all();

// [2, 4, 6, 8, 10]
```

> [!WARNING]  
> 대부분의 다른 컬렉션 메서드와는 달리, `transform`은 컬렉션 자체를 직접 변경합니다. 새 컬렉션을 만들고 싶다면 [`map`](#method-map) 메서드를 사용하세요.

<a name="method-undot"></a>
#### `undot()`

`undot` 메서드는 "dot(점) 표기법"을 사용하는 1차원 컬렉션을 다차원 컬렉션으로 확장합니다.

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

`union` 메서드는 지정한 배열의 요소를 컬렉션에 추가합니다. 단, 이미 컬렉션에 같은 키가 있을 경우 기존 컬렉션의 값을 우선시합니다.

```
$collection = collect([1 => ['a'], 2 => ['b']]);

$union = $collection->union([3 => ['c'], 1 => ['d']]);

$union->all();

// [1 => ['a'], 2 => ['b'], 3 => ['c']]
```

<a name="method-unique"></a>
#### `unique()`

`unique` 메서드는 컬렉션의 중복되지 않는 모든 아이템을 반환합니다. 반환되는 컬렉션은 원본 배열의 키를 그대로 유지하므로, 아래 예시에서는 [`values`](#method-values) 메서드를 활용해 키를 0부터 재정렬하고 있습니다.

```
$collection = collect([1, 1, 2, 2, 3, 4, 2]);

$unique = $collection->unique();

$unique->values()->all();

// [1, 2, 3, 4]
```

중첩 배열이나 객체를 다룰 때는, 고유성을 판단할 키를 지정할 수 있습니다.

```
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

마지막으로, 직접 콜백을 전달하여 각 아이템의 고유성을 어떻게 판별할지 지정할 수 있습니다.

```
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

`unique` 메서드는 아이템 값 비교 시 "느슨한(loose)" 비교를 사용합니다. 즉, 정수 값의 문자열과 숫자가 같은 값으로 간주됩니다. "엄격한(strict)" 비교를 적용하려면 [`uniqueStrict`](#method-uniquestrict) 메서드를 사용하세요.

> [!NOTE]  
> 이 메서드는 [Eloquent 컬렉션](/docs/10.x/eloquent-collections#method-unique)을 사용할 때 다르게 동작할 수 있습니다.

<a name="method-uniquestrict"></a>
#### `uniqueStrict()`

이 메서드는 [`unique`](#method-unique) 메서드와 동일한 시그니처를 가지지만, 값 비교 시 항상 "엄격한(strict)" 비교를 사용합니다.

<a name="method-unless"></a>
#### `unless()`

`unless` 메서드는 첫 번째 인자가 `true`로 평가되지 않는 경우, 주어진 콜백을 실행합니다.

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

`unless` 메서드에 두 번째 콜백을 전달할 수도 있는데, 이 콜백은 첫 번째 인자가 `true`로 평가될 때 실행됩니다.

```
$collection = collect([1, 2, 3]);

$collection->unless(true, function (Collection $collection) {
    return $collection->push(4);
}, function (Collection $collection) {
    return $collection->push(5);
});

$collection->all();

// [1, 2, 3, 5]
```

`unless`의 반대 동작이 궁금하다면 [`when`](#method-when) 메서드를 참고하세요.

<a name="method-unlessempty"></a>
#### `unlessEmpty()`

[`whenNotEmpty`](#method-whennotempty) 메서드의 별칭입니다.

<a name="method-unlessnotempty"></a>
#### `unlessNotEmpty()`

[`whenEmpty`](#method-whenempty) 메서드의 별칭입니다.

<a name="method-unwrap"></a>
#### `unwrap()`

정적 메서드인 `unwrap`은, 전달된 값이 컬렉션일 경우 내부 아이템을, 배열일 경우 그대로, 단일 값일 경우 그 값 자체를 반환합니다.

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

`value` 메서드는 컬렉션의 첫 번째 요소에서 지정한 값을 가져옵니다.

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

`values` 메서드는 컬렉션의 키를 0부터 연속된 숫자로 재설정한 새로운 컬렉션을 반환합니다.

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

`when` 메서드는 첫 번째 인자가 `true`로 평가될 때 주어진 콜백을 실행합니다. 이때 컬렉션 인스턴스와 첫 번째 인자가 콜백에 전달됩니다.

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

`when` 메서드에 두 번째 콜백을 전달할 수도 있으며, 이 콜백은 첫 번째 인자가 `false`로 평가될 때 실행됩니다.

```
$collection = collect([1, 2, 3]);

$collection->when(false, function (Collection $collection, int $value) {
    return $collection->push(4);
}, function (Collection $collection) {
    return $collection->push(5);
});

$collection->all();

// [1, 2, 3, 5]
```

반대 동작이 필요하다면 [`unless`](#method-unless) 메서드를 참고하세요.

<a name="method-whenempty"></a>
#### `whenEmpty()`

`whenEmpty` 메서드는 컬렉션이 비어 있으면 전달된 콜백을 실행합니다.

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

컬렉션이 비어 있지 않을 때 실행되는 두 번째 콜백을 전달할 수도 있습니다.

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

반대의 동작이 필요하다면 [`whenNotEmpty`](#method-whennotempty) 메서드를 참고하세요.

<a name="method-whennotempty"></a>
#### `whenNotEmpty()`

`whenNotEmpty` 메서드는 컬렉션이 비어 있지 않을 때 전달된 콜백을 실행합니다.

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

컬렉션이 비어 있을 때 실행되는 두 번째 콜백을 전달할 수도 있습니다.

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

반대 동작이 필요하다면 [`whenEmpty`](#method-whenempty) 메서드를 참고하세요.

<a name="method-where"></a>
#### `where()`

`where` 메서드는 지정한 키와 값이 일치하는 아이템만 컬렉션에서 필터링해 반환합니다.

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

`where` 메서드는 값 비교 시 "느슨한(loose)" 비교를 사용합니다. 즉, 정수 값의 문자열과 숫자가 같은 값으로 간주됩니다. "엄격한(strict)" 비교를 적용하려면 [`whereStrict`](#method-wherestrict) 메서드를 사용하세요.

옵션으로, 두 번째 매개변수로 비교 연산자를 전달할 수 있습니다. 지원되는 연산자는 '===', '!==', '!=', '==', '=', '<>', '>', '<', '>=', '<=' 입니다.

```
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

이 메서드는 [`where`](#method-where) 메서드와 동일한 시그니처를 가지나, 값 비교 시 항상 "엄격한(strict)" 비교를 사용합니다.

<a name="method-wherebetween"></a>
#### `whereBetween()`

`whereBetween` 메서드는 지정한 값이 특정 범위 내에 있는지 확인해 컬렉션을 필터링합니다.

```
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

`whereIn` 메서드는, 지정된 배열에 포함된 값을 가지지 않은 컬렉션의 요소들을 제거합니다.

```
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

`whereIn` 메서드는 값 비교 시 "느슨한(loose)" 비교를 사용합니다. 즉, 정수 값의 문자열과 숫자가 같은 값으로 간주됩니다. "엄격한(strict)" 비교를 적용하려면 [`whereInStrict`](#method-whereinstrict) 메서드를 사용하세요.

<a name="method-whereinstrict"></a>

#### `whereInStrict()`

이 메서드는 [`whereIn`](#method-wherein) 메서드와 동일한 시그니처를 가지지만, 모든 값을 "엄격하게(strict)" 비교하여 필터링합니다.

<a name="method-whereinstanceof"></a>
#### `whereInstanceOf()`

`whereInstanceOf` 메서드는 컬렉션에서 특정 클래스 타입의 인스턴스만 필터링할 때 사용합니다.

```
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

`whereNotBetween` 메서드는 지정한 아이템 값이 주어진 범위 바깥에 있을 때 해당 아이템만 필터링합니다.

```
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

`whereNotIn` 메서드는 주어진 배열에 포함되어 있는 특정 아이템 값을 가진 요소를 컬렉션에서 제거합니다.

```
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

`whereNotIn` 메서드는 아이템 값을 비교할 때 "느슨한(loose)" 비교를 사용합니다. 즉, 정수 값을 가진 문자열도 같은 값을 가진 정수와 동일하게 간주합니다. 엄격한 비교로 필터링하려면 [`whereNotInStrict`](#method-wherenotinstrict) 메서드를 사용하세요.

<a name="method-wherenotinstrict"></a>
#### `whereNotInStrict()`

이 메서드는 [`whereNotIn`](#method-wherenotin) 메서드와 시그니처가 동일하지만, 모든 값을 "엄격하게(strict)" 비교하여 필터링합니다.

<a name="method-wherenotnull"></a>
#### `whereNotNull()`

`whereNotNull` 메서드는 지정한 키의 값이 `null`이 아닌 아이템만 컬렉션에서 반환합니다.

```
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

`whereNull` 메서드는 지정한 키의 값이 `null`인 아이템만 컬렉션에서 반환합니다.

```
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

정적 메서드인 `wrap`은 전달된 값을 상황에 따라 컬렉션으로 감쌉니다.

```
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

`zip` 메서드는 컬렉션의 원래 값과 전달받은 배열의 값을 각 인덱스에 맞게 결합합니다.

```
$collection = collect(['Chair', 'Desk']);

$zipped = $collection->zip([100, 200]);

$zipped->all();

// [['Chair', 100], ['Desk', 200]]
```

<a name="higher-order-messages"></a>
## 하이어 오더 메시지 (Higher Order Messages)

컬렉션에서는 "하이어 오더 메시지(higher order messages)"도 지원합니다. 이는 컬렉션에서 자주 사용하는 동작을 더 간편하게 사용할 수 있는 단축 기능입니다. 하이어 오더 메시지를 제공하는 컬렉션 메서드는 다음과 같습니다: [`average`](#method-average), [`avg`](#method-avg), [`contains`](#method-contains), [`each`](#method-each), [`every`](#method-every), [`filter`](#method-filter), [`first`](#method-first), [`flatMap`](#method-flatmap), [`groupBy`](#method-groupby), [`keyBy`](#method-keyby), [`map`](#method-map), [`max`](#method-max), [`min`](#method-min), [`partition`](#method-partition), [`reject`](#method-reject), [`skipUntil`](#method-skipuntil), [`skipWhile`](#method-skipwhile), [`some`](#method-some), [`sortBy`](#method-sortby), [`sortByDesc`](#method-sortbydesc), [`sum`](#method-sum), [`takeUntil`](#method-takeuntil), [`takeWhile`](#method-takewhile), [`unique`](#method-unique).

각 하이어 오더 메시지는 컬렉션 인스턴스에서 동적 속성으로 접근할 수 있습니다. 예를 들어, `each` 하이어 오더 메시지를 사용해서 컬렉션 안의 각 객체에 대해 특정 메서드를 호출할 수 있습니다.

```
use App\Models\User;

$users = User::where('votes', '>', 500)->get();

$users->each->markAsVip();
```

마찬가지로, `sum` 하이어 오더 메시지를 사용하여 사용자 컬렉션의 "votes" 합계를 구할 수도 있습니다.

```
$users = User::where('group', 'Development')->get();

return $users->sum->votes;
```

<a name="lazy-collections"></a>
## 레이지 컬렉션 (Lazy Collections)

<a name="lazy-collection-introduction"></a>
### 소개

> [!WARNING]  
> 라라벨의 레이지 컬렉션을 본격적으로 학습하기 전에, 먼저 [PHP 제너레이터(generators)](https://www.php.net/manual/en/language.generators.overview.php)를 익혀보시는 것이 좋습니다.

기존의 강력한 `Collection` 클래스에 더해, `LazyCollection` 클래스는 PHP의 [제너레이터(generator)](https://www.php.net/manual/en/language.generators.overview.php)를 활용하여 메모리 사용량을 최소화하면서 매우 큰 데이터셋도 다룰 수 있게 합니다.

예를 들어, 애플리케이션이 수 기가바이트에 달하는 로그 파일을 처리해야 하면서 라라벨의 컬렉션 메서드로 로그를 파싱하려고 한다고 상상해 보세요. 전체 로그 파일을 한 번에 메모리로 읽어들이는 대신 레이지 컬렉션을 사용하면 특정 시점에 파일의 일부분만 메모리에 유지할 수 있습니다.

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
    // Process the log entry...
});
```

또는, 10,000개의 Eloquent 모델을 반복 처리해야 하는 상황을 생각해 볼 수 있습니다. 전통적인 라라벨 컬렉션을 사용할 경우, 모든 Eloquent 모델을 한 번에 메모리로 불러와야 합니다.

```
use App\Models\User;

$users = User::all()->filter(function (User $user) {
    return $user->id > 500;
});
```

하지만 쿼리 빌더의 `cursor` 메서드는 `LazyCollection` 인스턴스를 반환합니다. 즉, 데이터베이스 쿼리는 한 번만 수행하는 동시에, 한 번에 한 개의 Eloquent 모델만 메모리에 유지할 수 있습니다. 이 예시에서 `filter` 콜백은 실제로 각 유저를 반복 처리할 때에만 실행되므로, 메모리 사용을 크게 줄일 수 있습니다.

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
### 레이지 컬렉션 인스턴스 생성

레이지 컬렉션 인스턴스를 생성하려면, PHP 제너레이터 함수를 컬렉션의 `make` 메서드에 전달하면 됩니다.

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
### Enumerable 인터페이스

`Collection` 클래스에서 사용할 수 있는 거의 모든 메서드는 `LazyCollection` 클래스에서도 사용할 수 있습니다. 이 두 클래스는 모두 `Illuminate\Support\Enumerable` 인터페이스를 구현하고 있으며, 다음과 같은 메서드가 정의되어 있습니다.

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
> `shift`, `pop`, `prepend` 등 컬렉션(리스트)의 내용을 실제로 변경(수정)하는 메서드는 **LazyCollection 클래스에서는 사용할 수 없습니다.**

<a name="lazy-collection-methods"></a>
### 레이지 컬렉션 전용 메서드

`Enumerable` 인터페이스에서 정의된 메서드 외에도, `LazyCollection` 클래스는 다음과 같은 전용 메서드를 제공합니다.

<a name="method-takeUntilTimeout"></a>
#### `takeUntilTimeout()`

`takeUntilTimeout` 메서드는 지정한 시각까지 값들을 열거하고, 그 이후에는 반복/열거를 중단하는 새로운 레이지 컬렉션을 반환합니다.

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

이 메서드의 활용을 예로 들면, 데이터베이스에서 커서를 사용해 송장(invoices)을 제출하는 애플리케이션을 생각해 볼 수 있습니다. 15분마다 실행되는 [스케줄 작업](/docs/10.x/scheduling)을 정의하고, 한 번 실행에 최대 14분 동안만 송장을 처리하는 식으로 사용할 수 있습니다.

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

`each` 메서드는 컬렉션의 각 아이템에 대해 즉시 콜백을 실행하지만, `tapEach` 메서드는 컬렉션에서 아이템을 하나씩 꺼낼 때마다 콜백을 실행합니다.

```
// 아직 아무 것도 dump되지 않았습니다...
$lazyCollection = LazyCollection::times(INF)->tapEach(function (int $value) {
    dump($value);
});

// 세 개의 아이템이 dump됩니다...
$array = $lazyCollection->take(3)->all();

// 1
// 2
// 3
```

<a name="method-remember"></a>
#### `remember()`

`remember` 메서드는 이미 반복 처리한(열거한) 값을 "기억"하여, 컬렉션을 다시 열거할 때 그 값을 다시 가져오지 않고 캐시에서 반환하는 새로운 레이지 컬렉션을 반환합니다.

```
// 아직 쿼리가 실행되지 않았습니다...
$users = User::cursor()->remember();

// 쿼리가 실행됩니다...
// 처음 5명의 사용자가 데이터베이스에서 조회되어 적재됩니다...
$users->take(5)->all();

// 처음 5명은 컬렉션의 캐시에서 반환됩니다...
// 그 이후의 사용자들은 데이터베이스에서 적재됩니다...
$users->take(20)->all();
```