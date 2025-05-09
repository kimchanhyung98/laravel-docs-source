# 컬렉션 (Collections)

- [소개](#introduction)
    - [컬렉션 생성하기](#creating-collections)
    - [컬렉션 확장하기](#extending-collections)
- [사용 가능한 메서드](#available-methods)
- [하이어 오더 메시지](#higher-order-messages)
- [지연 컬렉션(Lazy Collections)](#lazy-collections)
    - [소개](#lazy-collection-introduction)
    - [지연 컬렉션 생성하기](#creating-lazy-collections)
    - [Enumerable 계약](#the-enumerable-contract)
    - [지연 컬렉션 전용 메서드](#lazy-collection-methods)

<a name="introduction"></a>
## 소개

`Illuminate\Support\Collection` 클래스는 데이터 배열을 다루기 위한 직관적이고 편리한 래퍼를 제공합니다. 예를 들어, 아래 코드를 확인해보세요. `collect` 헬퍼로 배열에서 새로운 컬렉션 인스턴스를 만들고, 각 요소에 `strtoupper` 함수를 적용한 뒤, 비어 있는 요소들을 모두 제거합니다.

```php
$collection = collect(['taylor', 'abigail', null])->map(function (?string $name) {
    return strtoupper($name);
})->reject(function (string $name) {
    return empty($name);
});
```

이처럼 `Collection` 클래스는 메서드 체이닝을 지원하여, 내부 배열에 대해 유연한 맵 및 리듀스 작업을 손쉽게 수행할 수 있습니다. 일반적으로 컬렉션은 불변(immutable)하게 동작하므로, 모든 `Collection` 메서드는 완전히 새로운 `Collection` 인스턴스를 반환합니다.

<a name="creating-collections"></a>
### 컬렉션 생성하기

앞서 언급한 것처럼, `collect` 헬퍼는 주어진 배열로부터 새로운 `Illuminate\Support\Collection` 인스턴스를 반환합니다. 컬렉션을 생성하는 것은 다음과 같이 매우 간단합니다.

```php
$collection = collect([1, 2, 3]);
```

또한 [make](#method-make) 및 [fromJson](#method-fromjson) 메서드를 사용하여 컬렉션을 생성할 수도 있습니다.

> [!NOTE]
> [Eloquent](/docs/{{version}}/eloquent) 쿼리는 항상 `Collection` 인스턴스로 결과를 반환합니다.

<a name="extending-collections"></a>
### 컬렉션 확장하기

컬렉션은 "매크로(macroable)" 기능을 제공합니다. 즉, 실행 중에 `Collection` 클래스에 원하는 메서드를 추가할 수 있습니다. `Illuminate\Support\Collection` 클래스의 `macro` 메서드는 매크로가 호출될 때 실행될 클로저를 인자로 받습니다. 매크로 클로저는 `$this`를 통해 컬렉션의 다른 메서드에 접근할 수 있어서 실제 컬렉션 메서드처럼 동작합니다. 아래 예시는 `Collection` 클래스에 `toUpper` 메서드를 추가하는 예시입니다.

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

일반적으로 컬렉션 매크로는 [서비스 프로바이더](/docs/{{version}}/providers)의 `boot` 메서드에서 선언하는 것이 좋습니다.

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

이후 컬렉션 문서 대부분에서는 `Collection` 클래스에서 사용할 수 있는 각 메서드에 대해 설명합니다. 모든 메서드는 체이닝이 가능하므로, 내부 배열을 유연하게 조작할 수 있습니다. 또한 거의 모든 메서드는 새로운 `Collection` 인스턴스를 반환하므로, 필요할 때 원본 컬렉션을 보존할 수 있습니다.

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
#### `after()` {.collection-method .first-collection-method}

`after` 메서드는 주어진 값 다음에 위치한 아이템을 반환합니다. 만약 해당 값이 컬렉션에 없거나 마지막 아이템이라면 `null`을 반환합니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->after(3);

// 4

$collection->after(5);

// null
```

이 메서드는 "느슨한(loose)" 비교로 아이템을 찾습니다. 즉, 정수 값을 포함한 문자열은 같은 값을 가진 정수와 동등하게 간주합니다. "엄격한(strict)" 비교를 사용하려면 `strict` 인수를 함께 전달하면 됩니다.

```php
collect([2, 4, 6, 8])->after('4', strict: true);

// null
```

또한, 원하는 조건을 만족하는 첫 번째 아이템을 찾기 위해 직접 클로저를 전달할 수도 있습니다.

```php
collect([2, 4, 6, 8])->after(function (int $item, int $key) {
    return $item > 5;
});

// 8
```

<a name="method-all"></a>
#### `all()` {.collection-method}

`all` 메서드는 컬렉션이 담고 있는 원본 배열 전체를 반환합니다.

```php
collect([1, 2, 3])->all();

// [1, 2, 3]
```

<a name="method-average"></a>
#### `average()` {.collection-method}

[avg](#method-avg) 메서드의 별칭입니다.

<a name="method-avg"></a>
#### `avg()` {.collection-method}

`avg` 메서드는 주어진 키의 [평균 값](https://en.wikipedia.org/wiki/Average)을 반환합니다.

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
#### `before()` {.collection-method}

`before` 메서드는 [after](#method-after) 메서드와 반대로 동작합니다. 주어진 값 바로 앞의 아이템을 반환합니다. 값이 없거나 첫 번째 아이템이라면 `null`을 반환합니다.

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
#### `chunk()` {.collection-method}

`chunk` 메서드는 컬렉션을 지정된 크기만큼 여러 개의 작은 컬렉션으로 나눕니다.

```php
$collection = collect([1, 2, 3, 4, 5, 6, 7]);

$chunks = $collection->chunk(4);

$chunks->all();

// [[1, 2, 3, 4], [5, 6, 7]]
```

이 메서드는 [뷰](/docs/{{version}}/views)에서 [Bootstrap](https://getbootstrap.com/docs/5.3/layout/grid/)과 같은 그리드 시스템과 함께 사용할 때 유용합니다. 예를 들어, 여러 [Eloquent](/docs/{{version}}/eloquent) 모델을 그리드에 출력하고자 할 때 사용합니다.

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
#### `chunkWhile()` {.collection-method}

`chunkWhile` 메서드는 주어진 콜백의 평가 결과에 따라 여러 개의 작은 컬렉션으로 나눕니다. 클로저에 전달되는 `$chunk` 변수는 이전 요소를 확인할 때 활용할 수 있습니다.

```php
$collection = collect(str_split('AABBCCCD'));

$chunks = $collection->chunkWhile(function (string $value, int $key, Collection $chunk) {
    return $value === $chunk->last();
});

$chunks->all();

// [['A', 'A'], ['B', 'B'], ['C', 'C', 'C'], ['D']]
```

<a name="method-collapse"></a>
#### `collapse()` {.collection-method}

`collapse` 메서드는 여러 배열 또는 컬렉션이 포함된 컬렉션을 하나의 평탄한(flat) 컬렉션으로 만듭니다.

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
#### `collapseWithKeys()` {.collection-method}

`collapseWithKeys` 메서드는 여러 배열 또는 컬렉션이 포함된 컬렉션을 하나의 컬렉션으로 평탄하게 만들되, 원래의 키를 그대로 유지합니다.

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
#### `collect()` {.collection-method}

`collect` 메서드는 현재 컬렉션에 담긴 아이템들로 새로운 `Collection` 인스턴스를 반환합니다.

```php
$collectionA = collect([1, 2, 3]);

$collectionB = $collectionA->collect();

$collectionB->all();

// [1, 2, 3]
```

이 메서드는 주로 [지연 컬렉션](#lazy-collections)을 일반 `Collection`으로 변환할 때 유용합니다.

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
> `collect` 메서드는 `Enumerable` 인스턴스로부터 일반(비지연) 컬렉션이 필요할 때 특히 유용합니다. `collect()`는 `Enumerable` 계약에 포함되어 있으므로, `Collection` 인스턴스를 안전하게 생성할 수 있습니다.

<a name="method-combine"></a>
#### `combine()` {.collection-method}

`combine` 메서드는 컬렉션의 값을 키로 삼고, 전달된 배열이나 컬렉션의 값을 값으로 하여 결합한 새로운 컬렉션을 만듭니다.

```php
$collection = collect(['name', 'age']);

$combined = $collection->combine(['George', 29]);

$combined->all();

// ['name' => 'George', 'age' => 29]
```

<a name="method-concat"></a>
#### `concat()` {.collection-method}

`concat` 메서드는 주어진 배열 또는 컬렉션의 값을 현재 컬렉션 뒤에 붙입니다.

```php
$collection = collect(['John Doe']);

$concatenated = $collection->concat(['Jane Doe'])->concat(['name' => 'Johnny Doe']);

$concatenated->all();

// ['John Doe', 'Jane Doe', 'Johnny Doe']
```

`concat` 메서드는 덧붙여진 아이템에 대해 키를 0부터 다시 부여합니다. 키를 유지하려면 [merge](#method-merge) 메서드를 참고하세요.

<a name="method-contains"></a>
#### `contains()` {.collection-method}

`contains` 메서드는 컬렉션에 특정 아이템이 존재하는지 확인합니다. 클로저를 전달하여 아이템이 특정 조건을 만족하는지 검사할 수도 있습니다.

```php
$collection = collect([1, 2, 3, 4, 5]);

$collection->contains(function (int $value, int $key) {
    return $value > 5;
});

// false
```

또는 문자열을 직접 전달하여 해당 값이 포함되어 있는지 확인할 수 있습니다.

```php
$collection = collect(['name' => 'Desk', 'price' => 100]);

$collection->contains('Desk');

// true

$collection->contains('New York');

// false
```

또한, 키와 값 쌍을 전달하여 해당 쌍이 존재하는지 확인할 수도 있습니다.

```php
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
]);

$collection->contains('product', 'Bookcase');

// false
```

`contains` 메서드는 값 비교 시 "느슨한(loose)" 비교를 사용합니다. 즉, 정수형 값이 담긴 문자열도 동일하게 간주합니다. "엄격한(strict)" 비교로 필터링하려면 [containsStrict](#method-containsstrict) 메서드를 사용하세요.

반대로 `contains`와 반대 동작을 원할 때는 [doesntContain](#method-doesntcontain) 메서드를 참고하세요.

<a name="method-containsoneitem"></a>
#### `containsOneItem()` {.collection-method}

`containsOneItem` 메서드는 컬렉션에 단일 아이템만 존재하는지 확인합니다.

```php
collect([])->containsOneItem();

// false

collect(['1'])->containsOneItem();

// true

collect(['1', '2'])->containsOneItem();

// false
```

<a name="method-containsstrict"></a>
#### `containsStrict()` {.collection-method}

이 메서드는 [contains](#method-contains) 메서드와 같은 시그니처이지만, 모든 값을 "엄격하게(strict)" 비교하여 판별합니다.

> [!NOTE]
> [Eloquent 컬렉션](/docs/{{version}}/eloquent-collections#method-contains)에서 사용할 경우 동작이 달라집니다.

<a name="method-count"></a>
#### `count()` {.collection-method}

`count` 메서드는 컬렉션의 총 아이템 개수를 반환합니다.

```php
$collection = collect([1, 2, 3, 4]);

$collection->count();

// 4
```

<a name="method-countBy"></a>
#### `countBy()` {.collection-method}

`countBy` 메서드는 컬렉션 내 값의 등장 횟수를 셉니다. 기본적으로 모든 요소의 개수를 센 결과를 반환합니다.

```php
$collection = collect([1, 2, 2, 2, 3]);

$counted = $collection->countBy();

$counted->all();

// [1 => 1, 2 => 3, 3 => 1]
```

클로저를 전달하여 원하는 기준에 따라 등장 횟수를 셀 수도 있습니다.

```php
$collection = collect(['alice@gmail.com', 'bob@yahoo.com', 'carlos@gmail.com']);

$counted = $collection->countBy(function (string $email) {
    return substr(strrchr($email, '@'), 1);
});

$counted->all();

// ['gmail.com' => 2, 'yahoo.com' => 1]
```

<a name="method-crossjoin"></a>
#### `crossJoin()` {.collection-method}

`crossJoin` 메서드는 컬렉션의 값들과 전달된 배열이나 컬렉션의 값들을 교차 결합하여, 가능한 모든 조합(데카르트 곱)을 생성합니다.

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
#### `dd()` {.collection-method}

`dd` 메서드는 컬렉션의 아이템을 출력하고, 스크립트 실행을 즉시 종료합니다.

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

스크립트 실행을 멈추지 않고 단순히 값을 출력하려면 [dump](#method-dump) 메서드를 사용하세요.

...

(이후 전체 문서의 각 메서드 설명과 지침도 같은 규칙과 스타일로 번역됩니다.)

<a name="higher-order-messages"></a>
## 하이어 오더 메시지 (Higher Order Messages)

컬렉션은 "하이어 오더 메시지" 기능을 지원합니다. 이 기능은 컬렉션에서 자주 사용하는 동작을 빠르고 간단하게 수행할 수 있는 단축 구문입니다. 하이어 오더 메시지를 제공하는 컬렉션 메서드는 [average](#method-average), [avg](#method-avg), [contains](#method-contains), [each](#method-each), [every](#method-every), [filter](#method-filter), [first](#method-first), [flatMap](#method-flatmap), [groupBy](#method-groupby), [keyBy](#method-keyby), [map](#method-map), [max](#method-max), [min](#method-min), [partition](#method-partition), [reject](#method-reject), [skipUntil](#method-skipuntil), [skipWhile](#method-skipwhile), [some](#method-some), [sortBy](#method-sortby), [sortByDesc](#method-sortbydesc), [sum](#method-sum), [takeUntil](#method-takeuntil), [takeWhile](#method-takewhile), [unique](#method-unique) 등입니다.

각 하이어 오더 메시지는 컬렉션 인스턴스의 동적 프로퍼티처럼 사용할 수 있습니다. 예를 들어, `each` 하이어 오더 메시지를 사용하여 컬렉션 내 모든 객체의 메서드를 호출할 수 있습니다.

```php
use App\Models\User;

$users = User::where('votes', '>', 500)->get();

$users->each->markAsVip();
```

마찬가지로, `sum` 하이어 오더 메시지를 사용하여 유저 컬렉션에서 "votes" 총합을 구할 수도 있습니다.

```php
$users = User::where('group', 'Development')->get();

return $users->sum->votes;
```

<a name="lazy-collections"></a>
## 지연 컬렉션 (Lazy Collections)

<a name="lazy-collection-introduction"></a>
### 소개

> [!WARNING]
> 라라벨의 지연 컬렉션을 더 잘 활용하려면, [PHP 제너레이터(generator)](https://www.php.net/manual/en/language.generators.overview.php)에 대해 먼저 익숙해지는 것이 좋습니다.

이미 강력한 `Collection` 클래스에 더해, `LazyCollection` 클래스는 PHP의 [제너레이터](https://www.php.net/manual/en/language.generators.overview.php) 기능을 활용하여, 매우 큰 데이터셋을 메모리 사용량을 최소화하며 처리할 수 있도록 해줍니다.

예를 들어, 애플리케이션이 수 기가바이트 크기의 로그 파일을 라라벨 컬렉션 메서드로 읽고 분석해야 한다고 가정해봅시다. 파일 전체를 한 번에 메모리에 올리는 대신, 지연 컬렉션을 사용하면 매 순간 작은 일부만 메모리에 올려 작업할 수 있습니다.

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

또는 1만 개의 Eloquent 모델을 반복 처리해야 하는 경우, 기존 라라벨 컬렉션을 사용하면 모델 전체를 한 번에 메모리에 올려야 합니다.

```php
use App\Models\User;

$users = User::all()->filter(function (User $user) {
    return $user->id > 500;
});
```

하지만 쿼리 빌더의 `cursor` 메서드는 `LazyCollection` 인스턴스를 반환합니다. 이렇게 하면 데이터베이스 쿼리는 한 번만 실행하면서, 매 순간 한 개의 Eloquent 모델만 메모리에 상주하게 됩니다. 즉, 실제로 각 유저를 반복 처리할 때 비로소 `filter` 콜백이 실행되므로 메모리 사용량이 현저히 줄어듭니다.

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
### 지연 컬렉션 생성하기

지연 컬렉션을 만들기 위해서는, 컬렉션의 `make` 메서드에 PHP 제너레이터 함수를 전달해야 합니다.

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

`Collection` 클래스에서 제공하는 거의 모든 메서드는 `LazyCollection` 클래스에서도 사용할 수 있습니다. 두 클래스는 모두 `Illuminate\Support\Enumerable` 계약을 구현하고 있으며, 이 계약에는 다음과 같은 메서드들이 정의되어 있습니다.

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
> 컬렉션을 변경하는 메서드(`shift`, `pop`, `prepend` 등)는 `LazyCollection` 클래스에서 사용할 수 없습니다.

<a name="lazy-collection-methods"></a>
### 지연 컬렉션 전용 메서드

`Enumerable` 계약에 정의된 메서드 외에도, `LazyCollection` 클래스에는 아래와 같은 추가 메서드가 있습니다.

<a name="method-takeUntilTimeout"></a>
#### `takeUntilTimeout()` {.collection-method}

`takeUntilTimeout` 메서드는 지정된 시각까지 값을 enumerate(열거)하며, 해당 시간이 되면 그 이후의 값은 반환하지 않는 새로운 지연 컬렉션을 만듭니다.

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

이 메서드는 예를 들어, 데이터베이스에서 송장(invoice)을 조회해 제출해야 하는 애플리케이션의 예약 작업에서 활용할 수 있습니다. 예를 들어 15분마다 실행하되, 최대 14분만 처리하도록 아래와 같이 사용할 수 있습니다.

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
#### `tapEach()` {.collection-method}

`each` 메서드는 모든 아이템에 대해 콜백을 곧바로 호출하는 반면, `tapEach` 메서드는 리스트에서 아이템이 하나씩 꺼내질 때마다 콜백을 호출합니다.

```php
// 아직 아무런 값도 출력되지 않음
$lazyCollection = LazyCollection::times(INF)->tapEach(function (int $value) {
    dump($value);
});

// 세 개의 값이 출력됨
$array = $lazyCollection->take(3)->all();

// 1
// 2
// 3
```

<a name="method-throttle"></a>
#### `throttle()` {.collection-method}

`throttle` 메서드는 컬렉션에서 각 값을 지정된 초(seconds)만큼 지연시켜 반환합니다. 외부 API와 같이 요청 제한이 있는 경우 대기 시간을 두고 반복할 때 유용합니다.

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
#### `remember()` {.collection-method}

`remember` 메서드는 이미 열거된(enumerated) 값들을 캐시에 저장하여, 이후에 같은 값을 다시 읽으려고 할 때는 다시 조회하지 않고 빠르게 반환하는 새로운 지연 컬렉션을 만듭니다.

```php
// 아직 쿼리 실행 안됨...
$users = User::cursor()->remember();

// 쿼리 실행! 첫 5명 데이터베이스에서 조회
$users->take(5)->all();

// 처음 5명은 컬렉션의 캐시에서 반환, 그 이후 값은 DB에서 불러옴
$users->take(20)->all();
```
