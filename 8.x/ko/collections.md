# 컬렉션 (Collections)

- [소개](#introduction)
    - [컬렉션 생성하기](#creating-collections)
    - [컬렉션 확장하기](#extending-collections)
- [사용 가능한 메서드](#available-methods)
- [고차 메시지 (Higher Order Messages)](#higher-order-messages)
- [레이지 컬렉션 (Lazy Collections)](#lazy-collections)
    - [소개](#lazy-collection-introduction)
    - [레이지 컬렉션 생성하기](#creating-lazy-collections)
    - [Enumerable 계약](#the-enumerable-contract)
    - [레이지 컬렉션 메서드](#lazy-collection-methods)

<a name="introduction"></a>
## 소개

`Illuminate\Support\Collection` 클래스는 배열 데이터 작업을 위한 직관적이고 편리한 래퍼를 제공합니다. 예를 들어, 다음 코드를 살펴보세요. `collect` 헬퍼를 사용하여 배열에서 새로운 컬렉션 인스턴스를 생성하고, 각 요소에 `strtoupper` 함수를 적용한 후, 빈 요소를 모두 제거합니다:

```
$collection = collect(['taylor', 'abigail', null])->map(function ($name) {
    return strtoupper($name);
})->reject(function ($name) {
    return empty($name);
});
```

보시다시피, `Collection` 클래스는 메서드를 체이닝하여 원본 배열에 대한 플루언트한 매핑 및 축소 작업을 수행할 수 있게 해줍니다. 일반적으로 컬렉션은 불변(immutable)이며, 모든 `Collection` 메서드는 완전히 새로운 `Collection` 인스턴스를 반환합니다.

<a name="creating-collections"></a>
### 컬렉션 생성하기

앞서 언급했듯이, `collect` 헬퍼는 주어진 배열에서 새로운 `Illuminate\Support\Collection` 인스턴스를 반환합니다. 따라서 컬렉션 생성은 단순히:

```
$collection = collect([1, 2, 3]);
```

> [!TIP]
> [Eloquent](/docs/{{version}}/eloquent) 쿼리 결과는 항상 `Collection` 인스턴스로 반환됩니다.

<a name="extending-collections"></a>
### 컬렉션 확장하기

컬렉션은 "macroable" 하여 런타임에 `Collection` 클래스에 추가 메서드를 정의할 수 있습니다. `Illuminate\Support\Collection` 클래스의 `macro` 메서드는 매크로가 호출될 때 실행될 클로저를 인수로 받습니다. 매크로 클로저는 `$this`를 사용해 컬렉션 클래스의 다른 메서드에 접근할 수 있으며, 마치 컬렉션 클래스의 실제 메서드인 것처럼 동작합니다.

예를 들어, 다음 코드는 `Collection` 클래스에 `toUpper` 메서드를 추가합니다:

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

보통 컬렉션 매크로는 [서비스 프로바이더](/docs/{{version}}/providers) 내 `boot` 메서드에서 선언하는 것이 권장됩니다.

<a name="macro-arguments"></a>
#### 매크로 인수

필요 시, 추가 인수를 받는 매크로를 정의할 수도 있습니다:

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
## 사용 가능한 메서드

남은 컬렉션 문서에서는 `Collection` 클래스에 사용 가능한 각 메서드를 살펴봅니다. 이 메서드들은 모두 체이닝하여 원본 배열을 플루언트하게 조작할 수 있습니다. 그리고 거의 모든 메서드는 새로운 `Collection` 인스턴스를 반환해, 필요 시 원본 컬렉션을 보존할 수 있도록 해줍니다.

(중간 코드 인덱싱 생략)

<a name="method-all"></a>
#### `all()`

`all` 메서드는 컬렉션이 래핑한 기본 배열을 반환합니다:

```
collect([1, 2, 3])->all();

// [1, 2, 3]
```

<a name="method-average"></a>
#### `average()`

`avg` 메서드의 별칭입니다.

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

`chunk` 메서드는 컬렉션을 주어진 크기만큼 작은 복수의 컬렉션으로 나눕니다:

```
$collection = collect([1, 2, 3, 4, 5, 6, 7]);

$chunks = $collection->chunk(4);

$chunks->all();

// [[1, 2, 3, 4], [5, 6, 7]]
```

이 메서드는 [Bootstrap](https://getbootstrap.com/docs/4.1/layout/grid/) 같은 그리드 시스템으로 렌더링할 때 유용합니다. 예를 들어 [Eloquent](/docs/{{version}}/eloquent) 모델 컬렉션을 그리드로 표시할 때:

```
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

`chunkWhile` 메서드는 주어진 콜백을 평가해 컬렉션을 여러 작은 컬렉션으로 나눕니다. 클로저에 전달되는 `$chunk` 변수로 이전 요소를 확인할 수 있습니다:

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

`collapse` 메서드는 배열 컬렉션을 단일 평탄화된 컬렉션으로 병합합니다:

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

`collect` 메서드는 현재 컬렉션 아이템으로 새 `Collection` 인스턴스를 반환합니다:

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

> [!TIP]
> `collect` 메서드는 `Enumerable` 계약의 일부이므로, `Enumerable` 인스턴스를 일반 `Collection` 인스턴스로 안전하게 변환할 때 특히 유용합니다.

<a name="method-combine"></a>
#### `combine()`

`combine` 메서드는 컬렉션의 값을 키로 사용하고, 다른 배열이나 컬렉션의 값을 값으로 결합합니다:

```
$collection = collect(['name', 'age']);

$combined = $collection->combine(['George', 29]);

$combined->all();

// ['name' => 'George', 'age' => 29]
```

<a name="method-concat"></a>
#### `concat()`

`concat` 메서드는 주어진 `array` 혹은 컬렉션의 값을 기존 컬렉션 끝에 추가합니다:

```
$collection = collect(['John Doe']);

$concatenated = $collection->concat(['Jane Doe'])->concat(['name' => 'Johnny Doe']);

$concatenated->all();

// ['John Doe', 'Jane Doe', 'Johnny Doe']
```

<a name="method-contains"></a>
#### `contains()`

`contains` 메서드는 컬렉션에 특정 항목이 있는지 판별합니다. 콜백을 전달해 조건에 맞는 요소가 컬렉션에 존재하는지 확인할 수 있습니다:

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->contains(function ($value, $key) {
    return $value > 5;
});

// false
```

혹은, 컬렉션에 특정 값을 포함하는지 검사할 수도 있습니다:

```
$collection = collect(['name' => 'Desk', 'price' => 100]);

$collection->contains('Desk');

// true

$collection->contains('New York');

// false
```

키-값 쌍으로 전달해 특정 쌍의 존재 여부를 확인하는 것도 가능합니다:

```
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
]);

$collection->contains('product', 'Bookcase');

// false
```

`contains`는 느슨한(loose) 비교를 하므로, 숫자 문자열과 같은 값들은 동일한 값으로 간주됩니다. 엄격한(strict) 비교가 필요할 경우, [`containsStrict`](#method-containsstrict) 메서드를 사용하세요.

`contains`의 반대는 [doesntContain](#method-doesntcontain) 메서드를 참고하세요.

<a name="method-containsstrict"></a>
#### `containsStrict()`

이 메서드는 [`contains`](#method-contains)와 동일한 시그니처를 가지며, 모든 값은 엄격한(strict) 비교를 사용해 비교됩니다.

> [!TIP]
> [Eloquent 컬렉션](/docs/{{version}}/eloquent-collections#method-contains) 사용 시 이 메서드 행동이 달라집니다.

<a name="method-count"></a>
#### `count()`

`count` 메서드는 컬렉션 내 아이템 수를 반환합니다:

```
$collection = collect([1, 2, 3, 4]);

$collection->count();

// 4
```

<a name="method-countBy"></a>
#### `countBy()`

`countBy` 메서드는 컬렉션 내 각 값의 출현 빈도를 계산합니다. 기본적으로 각 요소의 발생 횟수를 세며, 특정 타입별 카운팅도 가능하게 해줍니다:

```
$collection = collect([1, 2, 2, 2, 3]);

$counted = $collection->countBy();

$counted->all();

// [1 => 1, 2 => 3, 3 => 1]
```

콜백을 전달하면 커스텀 값에 따라 카운트를 셀 수도 있습니다:

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

`crossJoin` 메서드는 주어진 배열이나 컬렉션과 컬렉션의 값을 조합해 가능한 모든 조합을 포함하는 카테시안 곱을 반환합니다:

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

`dd` 메서드는 컬렉션 아이템의 내용을 덤프하고 스크립트 실행을 중단합니다:

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

스크립트 중단 없이 덤프만 할 경우 [`dump`](#method-dump) 메서드를 사용하세요.

<a name="method-diff"></a>
#### `diff()`

`diff` 메서드는 값 기준으로 다른 컬렉션이나 배열과 비교하여, 원본 컬렉션에만 존재하는 값을 반환합니다:

```
$collection = collect([1, 2, 3, 4, 5]);

$diff = $collection->diff([2, 4, 6, 8]);

$diff->all();

// [1, 3, 5]
```

> [!TIP]
> [Eloquent 컬렉션](/docs/{{version}}/eloquent-collections#method-diff)에서는 동작이 달라질 수 있습니다.

<a name="method-diffassoc"></a>
#### `diffAssoc()`

`diffAssoc` 메서드는 키와 값 모두 기준으로 다른 컬렉션이나 배열과 비교하여, 원본에만 존재하는 키-값 쌍을 반환합니다:

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

`diffKeys` 메서드는 키 기준으로 다른 컬렉션이나 배열과 비교하여, 원본에만 존재하는 키-값 쌍을 반환합니다:

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

`doesntContain` 메서드는 컬렉션에 특정 요소가 존재하지 않는지 확인합니다. 콜백 전달도 가능합니다:

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->doesntContain(function ($value, $key) {
    return $value < 5;
});

// false
```

값을 전달해 검사도 가능합니다:

```
$collection = collect(['name' => 'Desk', 'price' => 100]);

$collection->doesntContain('Table');

// true

$collection->doesntContain('Desk');

// false
```

키-값 쌍 전달도 가능합니다:

```
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
]);

$collection->doesntContain('product', 'Bookcase');

// true
```

`doesntContain`는 느슨한 비교를 사용합니다.

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

컬렉션 덤프 후 실행을 중단하려면 [`dd`](#method-dd) 메서드를 사용하세요.

<a name="method-duplicates"></a>
#### `duplicates()`

`duplicates` 메서드는 컬렉션에서 중복 값을 찾아 반환합니다:

```
$collection = collect(['a', 'b', 'a', 'c', 'b']);

$collection->duplicates();

// [2 => 'a', 4 => 'b']
```

배열이나 객체가 있는 경우, 중복 검사할 속성 키를 지정할 수 있습니다:

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

`duplicates`와 시그니처는 동일하지만 모든 값은 엄격한(strict) 비교로 검사됩니다.

<a name="method-each"></a>
#### `each()`

`each` 메서드는 컬렉션 아이템을 순회하며 각 아이템을 콜백에 전달합니다:

```
$collection->each(function ($item, $key) {
    //
});
```

중간에 순회를 중단하려면 콜백에서 `false`를 반환하세요:

```
$collection->each(function ($item, $key) {
    if (/* condition */) {
        return false;
    }
});
```

<a name="method-eachspread"></a>
#### `eachSpread()`

`eachSpread` 메서드는 중첩된 아이템 값을 펼쳐서 콜백에 전달하며 순회합니다:

```
$collection = collect([['John Doe', 35], ['Jane Doe', 33]]);

$collection->eachSpread(function ($name, $age) {
    //
});
```

`false` 반환시 순회 중단 가능:

```
$collection->eachSpread(function ($name, $age) {
    return false;
});
```

<a name="method-every"></a>
#### `every()`

`every` 메서드는 컬렉션의 모든 요소가 주어진 조건을 만족하는지 검사합니다:

```
collect([1, 2, 3, 4])->every(function ($value, $key) {
    return $value > 2;
});

// false
```

빈 컬렉션일 경우 항상 `true`를 반환합니다:

```
$collection = collect([]);

$collection->every(function ($value, $key) {
    return $value > 2;
});

// true
```

<a name="method-except"></a>
#### `except()`

`except` 메서드는 명시된 키를 제외한 나머지 아이템을 반환합니다:

```
$collection = collect(['product_id' => 1, 'price' => 100, 'discount' => false]);

$filtered = $collection->except(['price', 'discount']);

$filtered->all();

// ['product_id' => 1]
```

역으로, 반드시 포함할 키만 반환하려면 [only](#method-only) 메서드를 사용하세요.

> [!TIP]
> [Eloquent 컬렉션](/docs/{{version}}/eloquent-collections#method-except)에서는 동작이 다를 수 있습니다.

<a name="method-filter"></a>
#### `filter()`

`filter` 메서드는 콜백에 의해 참인 아이템만 필터링하여 반환합니다:

```
$collection = collect([1, 2, 3, 4]);

$filtered = $collection->filter(function ($value, $key) {
    return $value > 2;
});

$filtered->all();

// [3, 4]
```

콜백이 없으면 `false`와 동등한 값들은 제거됩니다:

```
$collection = collect([1, 2, 3, null, false, '', 0, []]);

$collection->filter()->all();

// [1, 2, 3]
```

부정 조건 필터링은 [reject](#method-reject) 메서드를 참고하세요.

<a name="method-first"></a>
#### `first()`

`first` 메서드는 조건에 맞는 첫 번째 아이템을 반환합니다:

```
collect([1, 2, 3, 4])->first(function ($value, $key) {
    return $value > 2;
});

// 3
```

인수 없이 호출하면 첫 번째 아이템을 반환하며, 빈 컬렉션인 경우 `null`을 반환합니다:

```
collect([1, 2, 3, 4])->first();

// 1
```

<a name="method-first-where"></a>
#### `firstWhere()`

`firstWhere` 메서드는 주어진 키-값 쌍과 일치하는 첫 번째 요소를 반환합니다:

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

비교 연산자도 사용 가능합니다:

```
$collection->firstWhere('age', '>=', 18);

// ['name' => 'Diego', 'age' => 23]
```

한 개 인자로 호출 시, 해당 키의 값이 참인 첫 번째 요소를 반환합니다:

```
$collection->firstWhere('age');

// ['name' => 'Linda', 'age' => 14]
```

<a name="method-flatmap"></a>
#### `flatMap()`

`flatMap`은 각 아이템을 변환 후 1단계 평탄화하여 새로운 컬렉션을 만듭니다:

```
$collection = collect([
    ['name' => 'Sally'],
    ['school' => 'Arkansas'],
    ['age' => 28]
]);

$flattened = $collection->flatMap(function ($values) {
    return array_map('strtoupper', $values);
});

$flattened->all();

// ['name' => 'SALLY', 'school' => 'ARKANSAS', 'age' => '28'];
```

<a name="method-flatten"></a>
#### `flatten()`

다차원 컬렉션을 단일 차원으로 평탄화합니다:

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

필요 시 깊이(depth)를 지정할 수도 있습니다:

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

인수를 지정하지 않으면 모든 중첩 레벨을 평탄화합니다.

<a name="method-flip"></a>
#### `flip()`

키와 값을 서로 뒤바꿉니다:

```
$collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

$flipped = $collection->flip();

$flipped->all();

// ['taylor' => 'name', 'laravel' => 'framework']
```

<a name="method-forget"></a>
#### `forget()`

키에 해당하는 아이템을 제거합니다:

```
$collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

$collection->forget('name');

$collection->all();

// ['framework' => 'laravel']
```

> [!NOTE]
> `forget` 메서드는 새로운 컬렉션을 반환하지 않고, 호출된 컬렉션을 직접 수정합니다.

<a name="method-forpage"></a>
#### `forPage()`

페이지 번호와 페이지 당 아이템 수를 받아 해당 페이지에 해당하는 아이템만 담긴 새 컬렉션을 반환합니다:

```
$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9]);

$chunk = $collection->forPage(2, 3);

$chunk->all();

// [4, 5, 6]
```

<a name="method-get"></a>
#### `get()`

키에 해당하는 아이템을 반환하며, 없으면 `null`을 반환합니다:

```
$collection = collect(['name' => 'taylor', 'framework' => 'laravel']);

$value = $collection->get('name');

// taylor
```

기본값을 두 번째 인자로 전달 가능하며, 콜백 역시 가능합니다:

```
$value = $collection->get('age', 34);

// 34

$value = $collection->get('email', function () {
    return 'taylor@example.com';
});

// taylor@example.com
```

<a name="method-groupby"></a>
#### `groupBy()`

주어진 키 또는 콜백 결과를 기준으로 컬렉션을 그룹화합니다:

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

복잡한 그룹화 기준도 전달 가능합니다:

```
$grouped = $collection->groupBy(function ($item, $key) {
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

다중 그룹화 기준을 배열로 넘길 수도 있습니다:

```
$data = new Collection([
    10 => ['user' => 1, 'skill' => 1, 'roles' => ['Role_1', 'Role_3']],
    20 => ['user' => 2, 'skill' => 1, 'roles' => ['Role_1', 'Role_2']],
    30 => ['user' => 3, 'skill' => 2, 'roles' => ['Role_1']],
    40 => ['user' => 4, 'skill' => 2, 'roles' => ['Role_2']],
]);

$result = $data->groupBy(['skill', function ($item) {
    return $item['roles'];
}], $preserveKeys = true);

/*
...
*/
```

<a name="method-has"></a>
#### `has()`

컬렉션 내에 주어진 키가 존재하는지 확인합니다:

```
$collection = collect(['account_id' => 1, 'product' => 'Desk', 'amount' => 5]);

$collection->has('product');

// true

$collection->has(['product', 'amount']);

// true

$collection->has(['amount', 'price']);

// false
```

<a name="method-implode"></a>
#### `implode()`

컬렉션 아이템을 문자열로 연결합니다. 배열/객체일 때는 키와 구분자(glue)를 전달합니다:

```
$collection = collect([
    ['account_id' => 1, 'product' => 'Desk'],
    ['account_id' => 2, 'product' => 'Chair'],
]);

$collection->implode('product', ', ');

// Desk, Chair
```

단순 값일 땐 구분자만 인수로 넘겨 호출합니다:

```
collect([1, 2, 3, 4, 5])->implode('-');

// '1-2-3-4-5'
```

<a name="method-intersect"></a>
#### `intersect()`

원본 컬렉션에서 주어진 배열 혹은 컬렉션과 일치하지 않는 값을 제거합니다. 원본 키는 유지됩니다:

```
$collection = collect(['Desk', 'Sofa', 'Chair']);

$intersect = $collection->intersect(['Desk', 'Chair', 'Bookcase']);

$intersect->all();

// [0 => 'Desk', 2 => 'Chair']
```

> [!TIP]
> [Eloquent 컬렉션](/docs/{{version}}/eloquent-collections#method-intersect)에서 동작이 달라질 수 있습니다.

<a name="method-intersectbykeys"></a>
#### `intersectByKeys()`

키 기준 일치하지 않는 키-값 쌍을 제거합니다:

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

컬렉션이 비어있으면 `true`, 아니면 `false`를 반환합니다:

```
collect([])->isEmpty();

// true
```

<a name="method-isnotempty"></a>
#### `isNotEmpty()`

컬렉션이 비어있지 않으면 `true`, 비어있으면 `false`를 반환합니다:

```
collect([])->isNotEmpty();

// false
```

<a name="method-join"></a>
#### `join()`

컬렉션 값들을 문자열로 합칩니다. 두 번째 인자로 마지막 아이템 연결 방식을 지정할 수 있습니다:

```
collect(['a', 'b', 'c'])->join(', '); // 'a, b, c'
collect(['a', 'b', 'c'])->join(', ', ', and '); // 'a, b, and c'
collect(['a', 'b'])->join(', ', ' and '); // 'a and b'
collect(['a'])->join(', ', ' and '); // 'a'
collect([])->join(', ', ' and '); // ''
```

<a name="method-keyby"></a>
#### `keyBy()`

주어진 키를 기준으로 컬렉션 키를 지정합니다. 키가 중복되면 마지막 요소가 사용됩니다:

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

콜백을 전달해 키 지정도 가능합니다:

```
$keyed = $collection->keyBy(function ($item) {
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

컬렉션 내 모든 키를 반환합니다:

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

조건에 맞는 마지막 아이템을 반환합니다:

```
collect([1, 2, 3, 4])->last(function ($value, $key) {
    return $value < 3;
});

// 2
```

인수 없이 호출 시 마지막 아이템을 반환하며, 없으면 `null`:

```
collect([1, 2, 3, 4])->last();

// 4
```

<a name="method-macro"></a>
#### `macro()`

정적 메서드로 컬렉션 클래스에 런타임 시 메서드를 추가할 수 있습니다. [컬렉션 확장하기](#extending-collections)를 참고하세요.

<a name="method-make"></a>
#### `make()`

정적 메서드로 새로운 컬렉션 인스턴스를 생성합니다. [컬렉션 생성하기](#creating-collections) 참조.

<a name="method-map"></a>
#### `map()`

각 아이템을 콜백으로 변환하여 새로운 컬렉션을 반환합니다:

```
$collection = collect([1, 2, 3, 4, 5]);

$multiplied = $collection->map(function ($item, $key) {
    return $item * 2;
});

$multiplied->all();

// [2, 4, 6, 8, 10]
```

> [!NOTE]
> `map`은 새로운 컬렉션을 반환하며 원본을 변경하지 않습니다. 원본 변경을 원한다면 [`transform`](#method-transform)을 사용하세요.

<a name="method-mapinto"></a>
#### `mapInto()`

각 아이템을 주어진 클래스 생성자에 전달하여 새 인스턴스를 생성한 컬렉션을 만듭니다:

```
class Currency
{
    function __construct(string $code)
    {
        $this->code = $code;
    }
}

$collection = collect(['USD', 'EUR', 'GBP']);

$currencies = $collection->mapInto(Currency::class);

$currencies->all();

// [Currency('USD'), Currency('EUR'), Currency('GBP')]
```

<a name="method-mapspread"></a>
#### `mapSpread()`

중첩 아이템을 펼쳐 콜백에 전달하고 변환된 아이템으로 새 컬렉션을 만듭니다:

```
$collection = collect([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]);

$chunks = $collection->chunk(2);

$sequence = $chunks->mapSpread(function ($even, $odd) {
    return $even + $odd;
});

$sequence->all();

// [1, 5, 9, 13, 17]
```

<a name="method-maptogroups"></a>
#### `mapToGroups()`

클로저가 반환하는 키-값 쌍 기준으로 그룹화된 컬렉션을 만듭니다:

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

$grouped = $collection->mapToGroups(function ($item, $key) {
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

각 아이템을 키-값 쌍으로 변환한 컬렉션을 반환합니다:

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

$keyed = $collection->mapWithKeys(function ($item, $key) {
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

주어진 키에 대한 최대값을 반환합니다:

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

주어진 키의 [중앙값](https://en.wikipedia.org/wiki/Median)을 반환합니다:

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

기존 컬렉션과 주어진 배열 또는 컬렉션을 병합합니다. 문자열 키가 중복되면 주어진 값으로 덮어씌웁니다:

```
$collection = collect(['product_id' => 1, 'price' => 100]);

$merged = $collection->merge(['price' => 200, 'discount' => false]);

$merged->all();

// ['product_id' => 1, 'price' => 200, 'discount' => false]
```

숫자 키는 끝에 추가됩니다:

```
$collection = collect(['Desk', 'Chair']);

$merged = $collection->merge(['Bookcase', 'Door']);

$merged->all();

// ['Desk', 'Chair', 'Bookcase', 'Door']
```

<a name="method-mergerecursive"></a>
#### `mergeRecursive()`

재귀적으로 배열을 병합합니다. 문자열 키가 중복 시 값들을 배열로 병합합니다:

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

주어진 키에 대한 최소값을 반환합니다:

```
$min = collect([['foo' => 10], ['foo' => 20]])->min('foo');

// 10

$min = collect([1, 2, 3, 4, 5])->min();

// 1
```

<a name="method-mode"></a>
#### `mode()`

주어진 키의 [최빈값](https://en.wikipedia.org/wiki/Mode_(statistics))을 배열로 반환합니다:

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

n 번째 요소만 담긴 컬렉션을 반환합니다:

```
$collection = collect(['a', 'b', 'c', 'd', 'e', 'f']);

$collection->nth(4);

// ['a', 'e']
```

시작 오프셋도 지정 가능합니다:

```
$collection->nth(4, 1);

// ['b', 'f']
```

<a name="method-only"></a>
#### `only()`

지정된 키에 해당하는 아이템만 반환합니다:

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

`only` 반대는 [except](#method-except) 메서드입니다.

> [!TIP]
> [Eloquent 컬렉션](/docs/{{version}}/eloquent-collections#method-only)에서 동작이 다를 수 있습니다.

<a name="method-pad"></a>
#### `pad()`

데이터가 지정한 크기에 도달할 때까지 주어진 값으로 양쪽을 채워넣습니다. 음수 크기로 왼쪽 패딩이 가능합니다:

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

조건에 맞는 요소와 맞지 않는 요소를 분리합니다:

```
$collection = collect([1, 2, 3, 4, 5, 6]);

[$underThree, $equalOrAboveThree] = $collection->partition(function ($i) {
    return $i < 3;
});

$underThree->all();

// [1, 2]

$equalOrAboveThree->all();

// [3, 4, 5, 6]
```

<a name="method-pipe"></a>
#### `pipe()`

컬렉션을 클로저에 전달하고 처리 결과를 반환합니다:

```
$collection = collect([1, 2, 3]);

$piped = $collection->pipe(function ($collection) {
    return $collection->sum();
});

// 6
```

<a name="method-pipeinto"></a>
#### `pipeInto()`

주어진 클래스를 인스턴스화 하며 생성자에 컬렉션을 전달합니다:

```
class ResourceCollection
{
    public $collection;

    public function __construct(Collection $collection)
    {
        $this->collection = $collection;
    }
}

$collection = collect([1, 2, 3]);

$resource = $collection->pipeInto(ResourceCollection::class);

$resource->collection->all();

// [1, 2, 3]
```

<a name="method-pipethrough"></a>
#### `pipeThrough()`

여러 클로저 배열에 컬렉션을 순차적으로 전달하고 최종 결과를 반환합니다:

```
$collection = collect([1, 2, 3]);

$result = $collection->pipeThrough([
    function ($collection) {
        return $collection->merge([4, 5]);
    },
    function ($collection) {
        return $collection->sum();
    },
]);

// 15
```

<a name="method-pluck"></a>
#### `pluck()`

주어진 키의 모든 값을 추출합니다:

```
$collection = collect([
    ['product_id' => 'prod-100', 'name' => 'Desk'],
    ['product_id' => 'prod-200', 'name' => 'Chair'],
]);

$plucked = $collection->pluck('name');

$plucked->all();

// ['Desk', 'Chair']
```

키를 지정해 결과 컬렉션의 키를 정할 수 있습니다:

```
$plucked = $collection->pluck('name', 'product_id');

$plucked->all();

// ['prod-100' => 'Desk', 'prod-200' => 'Chair']
```

중첩된 값도 "dot" 표기법으로 접근 가능:

```
$collection = collect([
    [
        'speakers' => [
            'first_day' => ['Rosa', 'Judith'],
            'second_day' => ['Angela', 'Kathleen'],
        ],
    ],
]);

$plucked = $collection->pluck('speakers.first_day');

$plucked->all();

// ['Rosa', 'Judith']
```

키 중복 시 마지막 값이 삽입됩니다:

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

마지막 아이템을 꺼내 반환합니다:

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->pop();

// 5

$collection->all();

// [1, 2, 3, 4]
```

숫자를 인수로 받으면 여러 개 아이템을 꺼냅니다:

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->pop(3);

// collect([5, 4, 3])

$collection->all();

// [1, 2]
```

<a name="method-prepend"></a>
#### `prepend()`

컬렉션 앞에 아이템을 추가합니다:

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->prepend(0);

$collection->all();

// [0, 1, 2, 3, 4, 5]
```

두 번째 인자로 키를 지정할 수도 있습니다:

```
$collection = collect(['one' => 1, 'two' => 2]);

$collection->prepend(0, 'zero');

$collection->all();

// ['zero' => 0, 'one' => 1, 'two' => 2]
```

<a name="method-pull"></a>
#### `pull()`

키에 해당하는 아이템을 제거하고 반환합니다:

```
$collection = collect(['product_id' => 'prod-100', 'name' => 'Desk']);

$collection->pull('name');

// 'Desk'

$collection->all();

// ['product_id' => 'prod-100']
```

<a name="method-push"></a>
#### `push()`

컬렉션 끝에 아이템을 추가합니다:

```
$collection = collect([1, 2, 3, 4]);

$collection->push(5);

$collection->all();

// [1, 2, 3, 4, 5]
```

<a name="method-put"></a>
#### `put()`

키와 값을 컬렉션에 설정합니다:

```
$collection = collect(['product_id' => 1, 'name' => 'Desk']);

$collection->put('price', 100);

$collection->all();

// ['product_id' => 1, 'name' => 'Desk', 'price' => 100]
```

<a name="method-random"></a>
#### `random()`

랜덤한 아이템을 반환합니다:

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->random();

// 4 - (무작위)
```

숫자를 전달하면 여러 아이템을 랜덤 조회합니다:

```
$random = $collection->random(3);

$random->all();

// [2, 4, 5] - (무작위)
```

요청한 수보다 적으면 `InvalidArgumentException`이 발생합니다.

<a name="method-range"></a>
#### `range()`

주어진 범위 내 정수 컬렉션을 반환합니다:

```
$collection = collect()->range(3, 6);

$collection->all();

// [3, 4, 5, 6]
```

<a name="method-reduce"></a>
#### `reduce()`

각 반복 결과를 다음 반복에 전달해 컬렉션을 단일 값으로 축소합니다:

```
$collection = collect([1, 2, 3]);

$total = $collection->reduce(function ($carry, $item) {
    return $carry + $item;
});

// 6
```

초기값을 두 번째 인자로 지정할 수도 있습니다:

```
$collection->reduce(function ($carry, $item) {
    return $carry + $item;
}, 4);

// 10
```

키도 콜백으로 전달합니다:

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

$collection->reduce(function ($carry, $value, $key) use ($ratio) {
    return $carry + ($value * $ratio[$key]);
});

// 4264
```

<a name="method-reduce-spread"></a>
#### `reduceSpread()`

`reduce`와 비슷하나 여러 초기값을 받으며 배열 결과를 반복 전달합니다:

```php
[$creditsRemaining, $batch] = Image::where('status', 'unprocessed')
        ->get()
        ->reduceSpread(function ($creditsRemaining, $batch, $image) {
            if ($creditsRemaining >= $image->creditsRequired()) {
                $batch->push($image);

                $creditsRemaining -= $image->creditsRequired();
            }

            return [$creditsRemaining, $batch];
        }, $creditsAvailable, collect());
```

<a name="method-reject"></a>
#### `reject()`

조건에 맞는 요소를 제외하고 나머지를 필터링합니다:

```
$collection = collect([1, 2, 3, 4]);

$filtered = $collection->reject(function ($value, $key) {
    return $value > 2;
});

$filtered->all();

// [1, 2]
```

`reject`의 반대는 [`filter`](#method-filter) 메서드입니다.

<a name="method-replace"></a>
#### `replace()`

`merge` 비슷하지만, 문자열뿐만 아니라 숫자 키도 덮어씁니다:

```
$collection = collect(['Taylor', 'Abigail', 'James']);

$replaced = $collection->replace([1 => 'Victoria', 3 => 'Finn']);

$replaced->all();

// ['Taylor', 'Victoria', 'James', 'Finn']
```

<a name="method-replacerecursive"></a>
#### `replaceRecursive()`

`replace`와 같으나 배열 내 중첩값도 재귀적으로 대체합니다:

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

컬렉션 아이템 순서를 뒤집으며 원래 키를 유지합니다:

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

값을 찾아 키를 반환하며, 없으면 `false`입니다:

```
$collection = collect([2, 4, 6, 8]);

$collection->search(4);

// 1
```

느슨한 비교가 기본이며, 엄격 비교하려면 두 번째 인자에 `true`를 전달하세요:

```
collect([2, 4, 6, 8])->search('4', $strict = true);

// false
```

콜백으로 조건 검색도 가능합니다:

```
collect([2, 4, 6, 8])->search(function ($item, $key) {
    return $item > 5;
});

// 2
```

<a name="method-shift"></a>
#### `shift()`

첫 번째 아이템을 꺼내 반환합니다:

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->shift();

// 1

$collection->all();

// [2, 3, 4, 5]
```

여러 개 꺼낼 수도 있습니다:

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->shift(3);

// collect([1, 2, 3])

$collection->all();

// [4, 5]
```

<a name="method-shuffle"></a>
#### `shuffle()`

아이템 순서를 무작위로 섞습니다:

```
$collection = collect([1, 2, 3, 4, 5]);

$shuffled = $collection->shuffle();

$shuffled->all();

// [3, 2, 5, 1, 4] - (무작위)
```

<a name="method-sliding"></a>
#### `sliding()`

"슬라이딩 윈도우" 방식으로 연속된 청크를 반환합니다:

```
$collection = collect([1, 2, 3, 4, 5]);

$chunks = $collection->sliding(2);

$chunks->toArray();

// [[1, 2], [2, 3], [3, 4], [4, 5]]
```

예를 들어 [`eachSpread`](#method-eachspread)와 유용하게 조합할 수 있습니다:

```
$transactions->sliding(2)->eachSpread(function ($previous, $current) {
    $current->total = $previous->total + $current->amount;
});
```

두 번째 인자로 "스텝"도 지정 가능합니다:

```
$collection = collect([1, 2, 3, 4, 5]);

$chunks = $collection->sliding(3, step: 2);

$chunks->toArray();

// [[1, 2, 3], [3, 4, 5]]
```

<a name="method-skip"></a>
#### `skip()`

처음부터 주어진 수 만큼 아이템을 제외한 새 컬렉션을 반환합니다:

```
$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);

$collection = $collection->skip(4);

$collection->all();

// [5, 6, 7, 8, 9, 10]
```

<a name="method-skipuntil"></a>
#### `skipUntil()`

콜백이 `true`를 반환할 때까지 아이템을 제외하고, 이후 나머지를 반환합니다:

```
$collection = collect([1, 2, 3, 4]);

$subset = $collection->skipUntil(function ($item) {
    return $item >= 3;
});

$subset->all();

// [3, 4]
```

값으로도 지정 가능:

```
$collection = collect([1, 2, 3, 4]);

$subset = $collection->skipUntil(3);

$subset->all();

// [3, 4]
```

> [!NOTE]
> 값이 없거나 콜백이 `true`를 반환하지 않으면 빈 컬렉션을 반환합니다.

<a name="method-skipwhile"></a>
#### `skipWhile()`

콜백이 `true`를 반환하는 동안 아이템을 제외하고 나머지 반환:

```
$collection = collect([1, 2, 3, 4]);

$subset = $collection->skipWhile(function ($item) {
    return $item <= 3;
});

$subset->all();

// [4]
```

> [!NOTE]
> 콜백이 `false`를 반환하지 않으면 빈 컬렉션 반환합니다.

<a name="method-slice"></a>
#### `slice()`

인덱스부터 시작하는 부분 집합을 반환합니다:

```
$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);

$slice = $collection->slice(4);

$slice->all();

// [5, 6, 7, 8, 9, 10]
```

길이 제한도 가능합니다:

```
$slice = $collection->slice(4, 2);

$slice->all();

// [5, 6]
```

기본적으로 키를 보존합니다. 키 리셋하려면 [`values`](#method-values) 사용하세요.

<a name="method-sole"></a>
#### `sole()`

조건에 맞는 단 하나의 아이템을 반환합니다:

```
collect([1, 2, 3, 4])->sole(function ($value, $key) {
    return $value === 2;
});

// 2
```

키-값 쌍으로도 사용할 수 있습니다:

```
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
    ['product' => 'Chair', 'price' => 100],
]);

$collection->sole('product', 'Chair');

// ['product' => 'Chair', 'price' => 100]
```

인수 없이 호출해 아이템이 하나일 때 받는 것도 가능합니다:

```
$collection = collect([
    ['product' => 'Desk', 'price' => 200],
]);

$collection->sole();

// ['product' => 'Desk', 'price' => 200]
```

요소가 없으면 `\Illuminate\Collections\ItemNotFoundException`이, 둘 이상이면 `\Illuminate\Collections\MultipleItemsFoundException`이 발생합니다.

<a name="method-some"></a>
#### `some()`

`contains` 메서드의 별칭입니다.

<a name="method-sort"></a>
#### `sort()`

컬렉션 내림차순 없이 정렬합니다. 원본 키가 유지되어, 키 초기화 위해 [`values`](#method-values)를 함께 써야 합니다:

```
$collection = collect([5, 3, 1, 2, 4]);

$sorted = $collection->sort();

$sorted->values()->all();

// [1, 2, 3, 4, 5]
```

`sort`는 PHP 내장 함수 `uasort`를 호출하며, 커스텀 비교 콜백 전달 가능.

> [!TIP]
> 배열이나 객체 내 중첩 데이터 정렬 시 [`sortBy`](#method-sortby), [`sortByDesc`](#method-sortbydesc) 사용 추천.

<a name="method-sortby"></a>
#### `sortBy()`

키 기준으로 정렬하며, 키 초기화를 위해 [`values`](#method-values) 사용:

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

정렬 플래그도 선택 가능:

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

커스텀 콜백 전달도 가능합니다:

```
$collection = collect([
    ['name' => 'Desk', 'colors' => ['Black', 'Mahogany']],
    ['name' => 'Chair', 'colors' => ['Black']],
    ['name' => 'Bookcase', 'colors' => ['Red', 'Beige', 'Brown']],
]);

$sorted = $collection->sortBy(function ($product, $key) {
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

복수 조건도 배열로 지정:

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

클로저 배열을 각각 정렬 조건으로 사용할 수도 있습니다:

```
$collection = collect([
    ['name' => 'Taylor Otwell', 'age' => 34],
    ['name' => 'Abigail Otwell', 'age' => 30],
    ['name' => 'Taylor Otwell', 'age' => 36],
    ['name' => 'Abigail Otwell', 'age' => 32],
]);

$sorted = $collection->sortBy([
    fn ($a, $b) => $a['name'] <=> $b['name'],
    fn ($a, $b) => $b['age'] <=> $a['age'],
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

`sortBy`와 같은 시그니처이나 내림차순으로 정렬합니다.

<a name="method-sortdesc"></a>
#### `sortDesc()`

`sort`의 역순으로 정렬합니다. 콜백은 전달할 수 없으며, 직접 비교함수를 뒤집어야 합니다:

```
$collection = collect([5, 3, 1, 2, 4]);

$sorted = $collection->sortDesc();

$sorted->values()->all();

// [5, 4, 3, 2, 1]
```

<a name="method-sortkeys"></a>
#### `sortKeys()`

키 기준으로 정렬합니다:

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

`sortKeys`와 같은 시그니처이나 역순입니다.

<a name="method-sortkeysusing"></a>
#### `sortKeysUsing()`

키에 사용자 지정 비교 함수를 적용하여 정렬합니다:

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

비교 함수는 `uksort` PHP 함수와 동일한 반환값을 가져야 합니다.

<a name="method-splice"></a>
#### `splice()`

지정 인덱스부터 아이템을 잘라내 반환하고, 컬렉션에서는 제거합니다:

```
$collection = collect([1, 2, 3, 4, 5]);

$chunk = $collection->splice(2);

$chunk->all();

// [3, 4, 5]

$collection->all();

// [1, 2]
```

길이 제한과 교체 아이템도 지정 가능합니다:

```
$chunk = $collection->splice(2, 1, [10, 11]);

$chunk->all();

// [3]

$collection->all();

// [1, 2, 10, 11, 4, 5]
```

<a name="method-split"></a>
#### `split()`

컬렉션을 주어진 수만큼 그룹으로 나눕니다:

```
$collection = collect([1, 2, 3, 4, 5]);

$groups = $collection->split(3);

$groups->all();

// [[1, 2], [3, 4], [5]]
```

<a name="method-splitin"></a>
#### `splitIn()`

비단말 그룹은 완전히 채우고 나머지를 마지막 그룹에 할당하며 나눕니다:

```
$collection = collect([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);

$groups = $collection->splitIn(3);

$groups->all();

// [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10]]
```

<a name="method-sum"></a>
#### `sum()`

아이템 합계를 반환합니다:

```
collect([1, 2, 3, 4, 5])->sum();

// 15
```

중첩 배열/객체일 땐 키를 지정:

```
$collection = collect([
    ['name' => 'JavaScript: The Good Parts', 'pages' => 176],
    ['name' => 'JavaScript: The Definitive Guide', 'pages' => 1096],
]);

$collection->sum('pages');

// 1272
```

커스텀 콜백도 전달 가능:

```
$collection = collect([
    ['name' => 'Chair', 'colors' => ['Black']],
    ['name' => 'Desk', 'colors' => ['Black', 'Mahogany']],
    ['name' => 'Bookcase', 'colors' => ['Red', 'Beige', 'Brown']],
]);

$collection->sum(function ($product) {
    return count($product['colors']);
});

// 6
```

<a name="method-take"></a>
#### `take()`

지정한 수만큼 아이템을 가져옵니다:

```
$collection = collect([0, 1, 2, 3, 4, 5]);

$chunk = $collection->take(3);

$chunk->all();

// [0, 1, 2]
```

음수 값으로 끝에서부터 아이템을 가져올 수도 있습니다:

```
$collection = collect([0, 1, 2, 3, 4, 5]);

$chunk = $collection->take(-2);

$chunk->all();

// [4, 5]
```

<a name="method-takeuntil"></a>
#### `takeUntil()`

콜백이 `true`를 반환할 때까지 아이템을 가져옵니다:

```
$collection = collect([1, 2, 3, 4]);

$subset = $collection->takeUntil(function ($item) {
    return $item >= 3;
});

$subset->all();

// [1, 2]
```

값 인수도 가능합니다:

```
$subset = $collection->takeUntil(3);

$subset->all();

// [1, 2]
```

> [!NOTE]
> 값이나 콜백이 `true`를 반환하지 않으면 모든 아이템을 반환합니다.

<a name="method-takewhile"></a>
#### `takeWhile()`

콜백이 `false`가 될 때까지 아이템을 가져옵니다:

```
$collection = collect([1, 2, 3, 4]);

$subset = $collection->takeWhile(function ($item) {
    return $item < 3;
});

$subset->all();

// [1, 2]
```

> [!NOTE]
> 콜백이 `false`가 되지 않으면 모든 아이템 반환합니다.

<a name="method-tap"></a>
#### `tap()`

특정 시점에 컬렉션을 만져볼 수 있도록 콜백에 전달하며, 원본은 변경하지 않고 원본을 반환합니다:

```
collect([2, 4, 3, 1, 5])
    ->sort()
    ->tap(function ($collection) {
        Log::debug('Values after sorting', $collection->values()->all());
    })
    ->shift();

// 1
```

<a name="method-times"></a>
#### `times()`

주어진 횟수만큼 클로저를 호출해 새 컬렉션을 만듭니다:

```
$collection = Collection::times(10, function ($number) {
    return $number * 9;
});

$collection->all();

// [9, 18, 27, 36, 45, 54, 63, 72, 81, 90]
```

<a name="method-toarray"></a>
#### `toArray()`

컬렉션을 일반 PHP 배열로 변환합니다. 값이 [Eloquent](/docs/{{version}}/eloquent) 모델이면 모델도 배열로 변환합니다:

```
$collection = collect(['name' => 'Desk', 'price' => 200]);

$collection->toArray();

/*
    [
        ['name' => 'Desk', 'price' => 200],
    ]
*/
```

> [!NOTE]
> `toArray`는 `Arrayable` 객체들도 재귀적으로 변환합니다. 원본 배열이 필요하면 [`all`](#method-all) 사용하세요.

<a name="method-tojson"></a>
#### `toJson()`

컬렉션을 JSON 직렬화된 문자열로 변환합니다:

```
$collection = collect(['name' => 'Desk', 'price' => 200]);

$collection->toJson();

// '{"name":"Desk", "price":200}'
```

<a name="method-transform"></a>
#### `transform()`

컬렉션을 직접 변환(변경)합니다. 콜백 반환값으로 아이템을 대체합니다:

```
$collection = collect([1, 2, 3, 4, 5]);

$collection->transform(function ($item, $key) {
    return $item * 2;
});

$collection->all();

// [2, 4, 6, 8, 10]
```

> [!NOTE]
> 대부분 메서드와 달리, `transform`은 컬렉션 내용을 직접 변경합니다. 새 컬렉션을 원한다면 [`map`](#method-map)을 사용하세요.

<a name="method-undot"></a>
#### `undot()`

"dot" 표기법을 사용하는 단일 차원 컬렉션을 다차원 컬렉션으로 확장합니다:

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

주어진 배열을 추가하며, 키가 중복되면 원본 컬렉션 값이 유지됩니다:

```
$collection = collect([1 => ['a'], 2 => ['b']]);

$union = $collection->union([3 => ['c'], 1 => ['d']]);

$union->all();

// [1 => ['a'], 2 => ['b'], 3 => ['c']]
```

<a name="method-unique"></a>
#### `unique()`

고유한 아이템을 반환합니다. 키는 유지되어 [`values`](#method-values)로 키를 초기화할 수 있습니다:

```
$collection = collect([1, 1, 2, 2, 3, 4, 2]);

$unique = $collection->unique();

$unique->values()->all();

// [1, 2, 3, 4]
```

중첩 배열/객체에선 키 지정이 가능합니다:

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

커스텀 콜백도 지원합니다:

```
$unique = $collection->unique(function ($item) {
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

느슨한 비교를 사용하며, 엄격 비교는 [`uniqueStrict`](#method-uniquestrict)를 사용하세요.

> [!TIP]
> [Eloquent 컬렉션](/docs/{{version}}/eloquent-collections#method-unique)에서 동작이 달라집니다.

<a name="method-uniquestrict"></a>
#### `uniqueStrict()`

`unique`와 같지만 모든 값을 엄격 비교합니다.

<a name="method-unless"></a>
#### `unless()`

첫 인자가 `true`가 아니면 콜백을 실행합니다:

```
$collection = collect([1, 2, 3]);

$collection->unless(true, function ($collection) {
    return $collection->push(4);
});

$collection->unless(false, function ($collection) {
    return $collection->push(5);
});

$collection->all();

// [1, 2, 3, 5]
```

두번째 콜백은 첫 인자가 `true`일 때 실행됩니다:

```
$collection = collect([1, 2, 3]);

$collection->unless(true, function ($collection) {
    return $collection->push(4);
}, function ($collection) {
    return $collection->push(5);
});

$collection->all();

// [1, 2, 3, 5]
```

반대는 [`when`](#method-when)입니다.

<a name="method-unlessempty"></a>
#### `unlessEmpty()`

[`whenNotEmpty`](#method-whennotempty) 메서드 별칭입니다.

<a name="method-unlessnotempty"></a>
#### `unlessNotEmpty()`

[`whenEmpty`](#method-whenempty) 메서드 별칭입니다.

<a name="method-unwrap"></a>
#### `unwrap()`

정적 메서드로 컬렉션이 래핑한 배열/값을 반환합니다:

```
Collection::unwrap(collect('John Doe'));

// ['John Doe']

Collection::unwrap(['John Doe']);

// ['John Doe']

Collection::unwrap('John Doe');

// 'John Doe'
```

<a name="method-values"></a>
#### `values()`

키를 연속된 정수로 재설정하여 새 컬렉션을 반환합니다:

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

첫 인자가 `true`이면 콜백을 실행합니다:

```
$collection = collect([1, 2, 3]);

$collection->when(true, function ($collection) {
    return $collection->push(4);
});

$collection->when(false, function ($collection) {
    return $collection->push(5);
});

$collection->all();

// [1, 2, 3, 4]
```

두 번째 콜백은 첫 인자가 `false`일 때 실행됩니다:

```
$collection = collect([1, 2, 3]);

$collection->when(false, function ($collection) {
    return $collection->push(4);
}, function ($collection) {
    return $collection->push(5);
});

$collection->all();

// [1, 2, 3, 5]
```

반대는 [`unless`](#method-unless)입니다.

<a name="method-whenempty"></a>
#### `whenEmpty()`

컬렉션이 비었을 때 콜백을 실행합니다:

```
$collection = collect(['Michael', 'Tom']);

$collection->whenEmpty(function ($collection) {
    return $collection->push('Adam');
});

$collection->all();

// ['Michael', 'Tom']
```

```
$collection = collect();

$collection->whenEmpty(function ($collection) {
    return $collection->push('Adam');
});

$collection->all();

// ['Adam']
```

두 번째 콜백은 컬렉션이 비어있지 않을 때 실행됩니다:

```
$collection = collect(['Michael', 'Tom']);

$collection->whenEmpty(function ($collection) {
    return $collection->push('Adam');
}, function ($collection) {
    return $collection->push('Taylor');
});

$collection->all();

// ['Michael', 'Tom', 'Taylor']
```

반대는 [`whenNotEmpty`](#method-whennotempty)입니다.

<a name="method-whennotempty"></a>
#### `whenNotEmpty()`

컬렉션이 비어있지 않을 때 콜백을 실행합니다:

```
$collection = collect(['michael', 'tom']);

$collection->whenNotEmpty(function ($collection) {
    return $collection->push('adam');
});

$collection->all();

// ['michael', 'tom', 'adam']
```

```
$collection = collect();

$collection->whenNotEmpty(function ($collection) {
    return $collection->push('adam');
});

$collection->all();

// []
```

두 번째 콜백은 비었을 때 실행됩니다:

```
$collection = collect();

$collection->whenNotEmpty(function ($collection) {
    return $collection->push('adam');
}, function ($collection) {
    return $collection->push('taylor');
});

$collection->all();

// ['taylor']
```

반대는 [`whenEmpty`](#method-whenempty)입니다.

<a name="method-where"></a>
#### `where()`

키-값 쌍으로 필터링합니다(느슨한 비교):

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

비교 연산자도 지원:

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

엄격 비교는 [`whereStrict`](#method-wherestrict) 사용.

<a name="method-wherestrict"></a>
#### `whereStrict()`

`where`와 같으나 엄격한 비교를 사용합니다.

<a name="method-wherebetween"></a>
#### `whereBetween()`

값이 지정한 범위 내에 있는 아이템 필터링:

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

값이 지정 배열에 포함된 항목만 필터링합니다(느슨한 비교):

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

엄격 비교는 [`whereInStrict`](#method-whereinstrict) 사용.

<a name="method-whereinstrict"></a>
#### `whereInStrict()`

`whereIn`과 같으나 엄격한 비교 사용.

<a name="method-whereinstanceof"></a>
#### `whereInstanceOf()`

주어진 클래스 타입인 아이템만 필터링:

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

값이 지정 범위 밖인 아이템 필터링:

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

지정 값에 포함되지 않는 아이템 필터링(느슨한 비교):

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

엄격 비교는 [`whereNotInStrict`](#method-wherenotinstrict) 사용.

<a name="method-wherenotinstrict"></a>
#### `whereNotInStrict()`

`whereNotIn`과 같으나 엄격한 비교 사용.

<a name="method-wherenotnull"></a>
#### `whereNotNull()`

키 값이 `null`이 아닌 아이템만 반환:

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

키 값이 `null`인 아이템만 반환:

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

정적 메서드로 값이 컬렉션이 아니라면 컬렉션으로 래핑합니다:

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

인덱스에 맞춰 원본 컬렉션과 주어진 배열 값을 병합합니다:

```
$collection = collect(['Chair', 'Desk']);

$zipped = $collection->zip([100, 200]);

$zipped->all();

// [['Chair', 100], ['Desk', 200]]
```

<a name="higher-order-messages"></a>
## 고차 메시지 (Higher Order Messages)

컬렉션은 간단한 공통 작업을 위한 고차 메시지를 지원합니다. 고차 메시지를 지원하는 메서드는 [`average`](#method-average)부터 [`unique`](#method-unique)까지 다양합니다.

고차 메시지는 컬렉션 인스턴스의 동적 속성처럼 접근할 수 있습니다. 예를 들어, 컬렉션 내 객체의 메서드를 일괄 호출할 수 있습니다:

```
use App\Models\User;

$users = User::where('votes', '>', 500)->get();

$users->each->markAsVip();
```

총 "votes" 합계 역시 고차 메시지로 구할 수 있습니다:

```
$users = User::where('group', 'Development')->get();

return $users->sum->votes;
```

<a name="lazy-collections"></a>
## 레이지 컬렉션 (Lazy Collections)

<a name="lazy-collection-introduction"></a>
### 소개

> [!NOTE]
> Laravel 레이지 컬렉션을 배우기 전에 [PHP 제너레이터](https://www.php.net/manual/en/language.generators.overview.php)를 숙지하세요.

`LazyCollection` 클래스는 PHP [제너레이터](https://www.php.net/manual/en/language.generators.overview.php)를 활용해 대용량 데이터도 메모리 사용량을 낮게 유지할 수 있게 합니다.

예를 들어, 수 기가바이트 크기 로그 파일을 처리할 때, 한 번에 모든 파일을 메모리에 올리지 않고 일부만 유지하며 로그를 처리할 수 있습니다:

```
use App\Models\LogEntry;
use Illuminate\Support\LazyCollection;

LazyCollection::make(function () {
    $handle = fopen('log.txt', 'r');

    while (($line = fgets($handle)) !== false) {
        yield $line;
    }
})->chunk(4)->map(function ($lines) {
    return LogEntry::fromLines($lines);
})->each(function (LogEntry $logEntry) {
    // 로그 항목 처리...
});
```

또는, 10,000개의 Eloquent 모델을 반복 조작할 때, 기존 컬렉션은 모든 모델을 메모리에 올립니다:

```
use App\Models\User;

$users = User::all()->filter(function ($user) {
    return $user->id > 500;
});
```

`cursor` 메서드는 `LazyCollection`을 반환해, 데이터베이스 쿼리는 한번만 실행하고도, 메모리에는 하나씩만 모델을 올릴 수 있습니다:

```
use App\Models\User;

$users = User::cursor()->filter(function ($user) {
    return $user->id > 500;
});

foreach ($users as $user) {
    echo $user->id;
}
```

<a name="creating-lazy-collections"></a>
### 레이지 컬렉션 생성하기

제너레이터 함수로 `make` 메서드에 전달해 레이지 컬렉션을 만듭니다:

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

거의 모든 `Collection` 클래스 메서드는 `LazyCollection` 클래스에서도 사용할 수 있습니다. 두 클래스는 `Illuminate\Support\Enumerable` 계약을 구현하며, 다음 메서드를 정의합니다:

(사용 가능한 메서드 목록 동일)

> [!NOTE]
> `shift`, `pop`, `prepend` 등 컬렉션을 변경하는 메서드는 `LazyCollection`에서는 지원하지 않습니다.

<a name="lazy-collection-methods"></a>
### 레이지 컬렉션 메서드

`Enumerable` 계약 이외에도 `LazyCollection`은 다음 메서드를 포함합니다:

<a name="method-takeUntilTimeout"></a>
#### `takeUntilTimeout()`

지정한 시간까지 요소를 열거하며, 시간이 지나면 중단합니다:

```
$lazyCollection = LazyCollection::times(INF)
    ->takeUntilTimeout(now()->addMinute());

$lazyCollection->each(function ($number) {
    dump($number);

    sleep(1);
});

// 1
// 2
// ...
// 58
// 59
```

예를 들어, 15분마다 실행하는 예약 작업에서 14분까지 처리하도록 제한할 때 활용합니다:

```
use App\Models\Invoice;
use Illuminate\Support\Carbon;

Invoice::pending()->cursor()
    ->takeUntilTimeout(
        Carbon::createFromTimestamp(LARAVEL_START)->add(14, 'minutes')
    )
    ->each(fn ($invoice) => $invoice->submit());
```

<a name="method-tapEach"></a>
#### `tapEach()`

`each`는 즉시 콜백을 실행하지만, `tapEach`는 순회하면서 하나씩 꺼낼 때만 콜백을 실행합니다:

```
// 아직 아무것도 덤프 안됨...
$lazyCollection = LazyCollection::times(INF)->tapEach(function ($value) {
    dump($value);
});

// 3개 아이템 덤프됨...
$array = $lazyCollection->take(3)->all();

// 1
// 2
// 3
```

<a name="method-remember"></a>
#### `remember()`

열거된 값들을 기억해, 재열거 시 반복 조회하지 않는 레이지 컬렉션을 반환합니다:

```
// 아직 쿼리 실행 전...
$users = User::cursor()->remember();

// 쿼리 실행, 처음 5명 사용자 조회...
$users->take(5)->all();

// 처음 5명은 캐시에서, 나머지는 데이터베이스에서 조회...
$users->take(20)->all();
```
