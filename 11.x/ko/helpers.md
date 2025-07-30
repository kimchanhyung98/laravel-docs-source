# Helpers

- [소개](#introduction)
- [사용 가능한 메서드](#available-methods)
- [기타 유틸리티](#other-utilities)
    - [벤치마킹](#benchmarking)
    - [날짜](#dates)
    - [지연 함수](#deferred-functions)
    - [복권(Lottery)](#lottery)
    - [파이프라인](#pipeline)
    - [Sleep](#sleep)
    - [타임박스(Timebox)](#timebox)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 다양한 전역 "헬퍼" PHP 함수를 포함하고 있습니다. 이들 함수 중 상당수는 프레임워크 자체에서 사용하지만, 필요에 따라 여러분의 애플리케이션에서도 편리하게 사용할 수 있습니다.

<a name="available-methods"></a>
## 사용 가능한 메서드 (Available Methods)

<a name="arrays-and-objects-method-list"></a>
### 배열과 객체 (Arrays & Objects)

<div class="collection-method-list" markdown="1">

[Arr::accessible](#method-array-accessible)
[Arr::add](#method-array-add)
[Arr::collapse](#method-array-collapse)
[Arr::crossJoin](#method-array-crossjoin)
[Arr::divide](#method-array-divide)
[Arr::dot](#method-array-dot)
[Arr::except](#method-array-except)
[Arr::exists](#method-array-exists)
[Arr::first](#method-array-first)
[Arr::flatten](#method-array-flatten)
[Arr::forget](#method-array-forget)
[Arr::get](#method-array-get)
[Arr::has](#method-array-has)
[Arr::hasAny](#method-array-hasany)
[Arr::isAssoc](#method-array-isassoc)
[Arr::isList](#method-array-islist)
[Arr::join](#method-array-join)
[Arr::keyBy](#method-array-keyby)
[Arr::last](#method-array-last)
[Arr::map](#method-array-map)
[Arr::mapSpread](#method-array-map-spread)
[Arr::mapWithKeys](#method-array-map-with-keys)
[Arr::only](#method-array-only)
[Arr::pluck](#method-array-pluck)
[Arr::prepend](#method-array-prepend)
[Arr::prependKeysWith](#method-array-prependkeyswith)
[Arr::pull](#method-array-pull)
[Arr::query](#method-array-query)
[Arr::random](#method-array-random)
[Arr::reject](#method-array-reject)
[Arr::set](#method-array-set)
[Arr::shuffle](#method-array-shuffle)
[Arr::sort](#method-array-sort)
[Arr::sortDesc](#method-array-sort-desc)
[Arr::sortRecursive](#method-array-sort-recursive)
[Arr::take](#method-array-take)
[Arr::toCssClasses](#method-array-to-css-classes)
[Arr::toCssStyles](#method-array-to-css-styles)
[Arr::undot](#method-array-undot)
[Arr::where](#method-array-where)
[Arr::whereNotNull](#method-array-where-not-null)
[Arr::wrap](#method-array-wrap)
[data_fill](#method-data-fill)
[data_get](#method-data-get)
[data_set](#method-data-set)
[data_forget](#method-data-forget)
[head](#method-head)
[last](#method-last)
</div>

<a name="numbers-method-list"></a>
### 숫자 (Numbers)

<div class="collection-method-list" markdown="1">

[Number::abbreviate](#method-number-abbreviate)
[Number::clamp](#method-number-clamp)
[Number::currency](#method-number-currency)
[Number::defaultCurrency](#method-default-currency)
[Number::defaultLocale](#method-default-locale)
[Number::fileSize](#method-number-file-size)
[Number::forHumans](#method-number-for-humans)
[Number::format](#method-number-format)
[Number::ordinal](#method-number-ordinal)
[Number::pairs](#method-number-pairs)
[Number::percentage](#method-number-percentage)
[Number::spell](#method-number-spell)
[Number::trim](#method-number-trim)
[Number::useLocale](#method-number-use-locale)
[Number::withLocale](#method-number-with-locale)
[Number::useCurrency](#method-number-use-currency)
[Number::withCurrency](#method-number-with-currency)

</div>

<a name="paths-method-list"></a>
### 경로 (Paths)

<div class="collection-method-list" markdown="1">

[app_path](#method-app-path)
[base_path](#method-base-path)
[config_path](#method-config-path)
[database_path](#method-database-path)
[lang_path](#method-lang-path)
[mix](#method-mix)
[public_path](#method-public-path)
[resource_path](#method-resource-path)
[storage_path](#method-storage-path)

</div>

<a name="urls-method-list"></a>
### URL (URLs)

<div class="collection-method-list" markdown="1">

[action](#method-action)
[asset](#method-asset)
[route](#method-route)
[secure_asset](#method-secure-asset)
[secure_url](#method-secure-url)
[to_route](#method-to-route)
[url](#method-url)

</div>

<a name="miscellaneous-method-list"></a>
### 기타 (Miscellaneous)

<div class="collection-method-list" markdown="1">

[abort](#method-abort)
[abort_if](#method-abort-if)
[abort_unless](#method-abort-unless)
[app](#method-app)
[auth](#method-auth)
[back](#method-back)
[bcrypt](#method-bcrypt)
[blank](#method-blank)
[broadcast](#method-broadcast)
[cache](#method-cache)
[class_uses_recursive](#method-class-uses-recursive)
[collect](#method-collect)
[config](#method-config)
[context](#method-context)
[cookie](#method-cookie)
[csrf_field](#method-csrf-field)
[csrf_token](#method-csrf-token)
[decrypt](#method-decrypt)
[dd](#method-dd)
[dispatch](#method-dispatch)
[dispatch_sync](#method-dispatch-sync)
[dump](#method-dump)
[encrypt](#method-encrypt)
[env](#method-env)
[event](#method-event)
[fake](#method-fake)
[filled](#method-filled)
[info](#method-info)
[literal](#method-literal)
[logger](#method-logger)
[method_field](#method-method-field)
[now](#method-now)
[old](#method-old)
[once](#method-once)
[optional](#method-optional)
[policy](#method-policy)
[redirect](#method-redirect)
[report](#method-report)
[report_if](#method-report-if)
[report_unless](#method-report-unless)
[request](#method-request)
[rescue](#method-rescue)
[resolve](#method-resolve)
[response](#method-response)
[retry](#method-retry)
[session](#method-session)
[tap](#method-tap)
[throw_if](#method-throw-if)
[throw_unless](#method-throw-unless)
[today](#method-today)
[trait_uses_recursive](#method-trait-uses-recursive)
[transform](#method-transform)
[validator](#method-validator)
[value](#method-value)
[view](#method-view)
[with](#method-with)
[when](#method-when)

</div>

<a name="arrays"></a>
## 배열과 객체 (Arrays & Objects)

<a name="method-array-accessible"></a>
#### `Arr::accessible()`

`Arr::accessible` 메서드는 주어진 값이 배열 접근 가능한지 판단합니다:

```
use Illuminate\Support\Arr;
use Illuminate\Support\Collection;

$isAccessible = Arr::accessible(['a' => 1, 'b' => 2]);

// true

$isAccessible = Arr::accessible(new Collection);

// true

$isAccessible = Arr::accessible('abc');

// false

$isAccessible = Arr::accessible(new stdClass);

// false
```

<a name="method-array-add"></a>
#### `Arr::add()`

`Arr::add` 메서드는 배열에 주어진 키가 존재하지 않거나 `null`로 설정되어 있을 경우 키/값 쌍을 추가합니다:

```
use Illuminate\Support\Arr;

$array = Arr::add(['name' => 'Desk'], 'price', 100);

// ['name' => 'Desk', 'price' => 100]

$array = Arr::add(['name' => 'Desk', 'price' => null], 'price', 100);

// ['name' => 'Desk', 'price' => 100]
```

<a name="method-array-collapse"></a>
#### `Arr::collapse()`

`Arr::collapse` 메서드는 배열들로 이루어진 배열을 하나의 배열로 합칩니다:

```
use Illuminate\Support\Arr;

$array = Arr::collapse([[1, 2, 3], [4, 5, 6], [7, 8, 9]]);

// [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

<a name="method-array-crossjoin"></a>
#### `Arr::crossJoin()`

`Arr::crossJoin` 메서드는 주어진 배열들의 카르테시안 곱(Cartesian product)을 계산하여 가능한 모든 순열을 포함하는 행렬을 반환합니다:

```
use Illuminate\Support\Arr;

$matrix = Arr::crossJoin([1, 2], ['a', 'b']);

/*
    [
        [1, 'a'],
        [1, 'b'],
        [2, 'a'],
        [2, 'b'],
    ]
*/

$matrix = Arr::crossJoin([1, 2], ['a', 'b'], ['I', 'II']);

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

<a name="method-array-divide"></a>
#### `Arr::divide()`

`Arr::divide` 메서드는 주어진 배열의 키들과 값들 각각을 별도의 배열로 반환합니다:

```
use Illuminate\Support\Arr;

[$keys, $values] = Arr::divide(['name' => 'Desk']);

// $keys: ['name']

// $values: ['Desk']
```

<a name="method-array-dot"></a>
#### `Arr::dot()`

`Arr::dot` 메서드는 다차원 배열을 단일 깊이의 배열로 펼치면서 키 이름에 점(dot) 구문을 사용하여 깊이를 표시합니다:

```
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

$flattened = Arr::dot($array);

// ['products.desk.price' => 100]
```

<a name="method-array-except"></a>
#### `Arr::except()`

`Arr::except` 메서드는 주어진 배열에서 특정 키/값 쌍을 제거합니다:

```
use Illuminate\Support\Arr;

$array = ['name' => 'Desk', 'price' => 100];

$filtered = Arr::except($array, ['price']);

// ['name' => 'Desk']
```

<a name="method-array-exists"></a>
#### `Arr::exists()`

`Arr::exists` 메서드는 주어진 키가 배열에 존재하는지 확인합니다:

```
use Illuminate\Support\Arr;

$array = ['name' => 'John Doe', 'age' => 17];

$exists = Arr::exists($array, 'name');

// true

$exists = Arr::exists($array, 'salary');

// false
```

<a name="method-array-first"></a>
#### `Arr::first()`

`Arr::first` 메서드는 주어진 배열에서 특정 조건을 만족하는 첫 번째 요소를 반환합니다:

```
use Illuminate\Support\Arr;

$array = [100, 200, 300];

$first = Arr::first($array, function (int $value, int $key) {
    return $value >= 150;
});

// 200
```

세 번째 인수로 기본값을 전달할 수 있으며, 조건에 맞는 값이 없을 때 반환됩니다:

```
use Illuminate\Support\Arr;

$first = Arr::first($array, $callback, $default);
```

<a name="method-array-flatten"></a>
#### `Arr::flatten()`

`Arr::flatten` 메서드는 다차원 배열을 하나의 단일 깊이의 배열로 평탄화합니다:

```
use Illuminate\Support\Arr;

$array = ['name' => 'Joe', 'languages' => ['PHP', 'Ruby']];

$flattened = Arr::flatten($array);

// ['Joe', 'PHP', 'Ruby']
```

<a name="method-array-forget"></a>
#### `Arr::forget()`

`Arr::forget` 메서드는 "dot" 표기법을 사용해 깊이 중첩된 배열에서 특정 키/값 쌍을 제거합니다:

```
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

Arr::forget($array, 'products.desk');

// ['products' => []]
```

<a name="method-array-get"></a>
#### `Arr::get()`

`Arr::get` 메서드는 "dot" 표기법을 사용해 깊이 중첩된 배열에서 값을 가져옵니다:

```
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

$price = Arr::get($array, 'products.desk.price');

// 100
```

존재하지 않는 키에 대해 기본값을 지정할 수 있습니다:

```
use Illuminate\Support\Arr;

$discount = Arr::get($array, 'products.desk.discount', 0);

// 0
```

<a name="method-array-has"></a>
#### `Arr::has()`

`Arr::has` 메서드는 "dot" 표기법으로 지정된 아이템이 배열에 존재하는지 확인합니다:

```
use Illuminate\Support\Arr;

$array = ['product' => ['name' => 'Desk', 'price' => 100]];

$contains = Arr::has($array, 'product.name');

// true

$contains = Arr::has($array, ['product.price', 'product.discount']);

// false
```

<a name="method-array-hasany"></a>
#### `Arr::hasAny()`

`Arr::hasAny` 메서드는 "dot" 표기법으로 지정된 여러 아이템 중 하나라도 배열에 존재하는지 확인합니다:

```
use Illuminate\Support\Arr;

$array = ['product' => ['name' => 'Desk', 'price' => 100]];

$contains = Arr::hasAny($array, 'product.name');

// true

$contains = Arr::hasAny($array, ['product.name', 'product.discount']);

// true

$contains = Arr::hasAny($array, ['category', 'product.discount']);

// false
```

<a name="method-array-isassoc"></a>
#### `Arr::isAssoc()`

`Arr::isAssoc` 메서드는 주어진 배열이 연관 배열(키가 0부터 시작하는 연속된 정수형이 아닐 때)인지 검사하고, 연관 배열이라면 `true`를 반환합니다:

```
use Illuminate\Support\Arr;

$isAssoc = Arr::isAssoc(['product' => ['name' => 'Desk', 'price' => 100]]);

// true

$isAssoc = Arr::isAssoc([1, 2, 3]);

// false
```

<a name="method-array-islist"></a>
#### `Arr::isList()`

`Arr::isList` 메서드는 주어진 배열의 키가 0부터 시작하는 연속된 정수형 키인지 확인합니다:

```
use Illuminate\Support\Arr;

$isList = Arr::isList(['foo', 'bar', 'baz']);

// true

$isList = Arr::isList(['product' => ['name' => 'Desk', 'price' => 100]]);

// false
```

<a name="method-array-join"></a>
#### `Arr::join()`

`Arr::join` 메서드는 배열 요소를 문자열로 연결합니다. 두 번째 인자로 마지막 요소에 사용할 연결 문자열을 지정할 수도 있습니다:

```
use Illuminate\Support\Arr;

$array = ['Tailwind', 'Alpine', 'Laravel', 'Livewire'];

$joined = Arr::join($array, ', ');

// Tailwind, Alpine, Laravel, Livewire

$joined = Arr::join($array, ', ', ' and ');

// Tailwind, Alpine, Laravel and Livewire
```

<a name="method-array-keyby"></a>
#### `Arr::keyBy()`

`Arr::keyBy` 메서드는 주어진 키를 기준으로 배열의 키를 재설정합니다. 동일 키가 여러 개 있으면 마지막 요소가 배열에 남습니다:

```
use Illuminate\Support\Arr;

$array = [
    ['product_id' => 'prod-100', 'name' => 'Desk'],
    ['product_id' => 'prod-200', 'name' => 'Chair'],
];

$keyed = Arr::keyBy($array, 'product_id');

/*
    [
        'prod-100' => ['product_id' => 'prod-100', 'name' => 'Desk'],
        'prod-200' => ['product_id' => 'prod-200', 'name' => 'Chair'],
    ]
*/
```

<a name="method-array-last"></a>
#### `Arr::last()`

`Arr::last` 메서드는 배열에서 특정 조건을 만족하는 마지막 요소를 반환합니다:

```
use Illuminate\Support\Arr;

$array = [100, 200, 300, 110];

$last = Arr::last($array, function (int $value, int $key) {
    return $value >= 150;
});

// 300
```

세 번째 인수로 기본값을 전달할 수 있으며, 조건에 맞는 값이 없을 때 반환됩니다:

```
use Illuminate\Support\Arr;

$last = Arr::last($array, $callback, $default);
```

<a name="method-array-map"></a>
#### `Arr::map()`

`Arr::map` 메서드는 배열을 순회하면서 각 값과 키를 콜백에 전달하고, 콜백이 반환한 값으로 배열 요소를 교체합니다:

```
use Illuminate\Support\Arr;

$array = ['first' => 'james', 'last' => 'kirk'];

$mapped = Arr::map($array, function (string $value, string $key) {
    return ucfirst($value);
});

// ['first' => 'James', 'last' => 'Kirk']
```

<a name="method-array-map-spread"></a>
#### `Arr::mapSpread()`

`Arr::mapSpread` 메서드는 중첩 배열을 순회하며 콜백에 각각의 내부 값을 개별 인수로 전달합니다. 콜백에서 수정한 값을 반환하면 결과 배열에 반영됩니다:

```
use Illuminate\Support\Arr;

$array = [
    [0, 1],
    [2, 3],
    [4, 5],
    [6, 7],
    [8, 9],
];

$mapped = Arr::mapSpread($array, function (int $even, int $odd) {
    return $even + $odd;
});

/*
    [1, 5, 9, 13, 17]
*/
```

<a name="method-array-map-with-keys"></a>
#### `Arr::mapWithKeys()`

`Arr::mapWithKeys` 메서드는 배열을 순회하면서 각 요소를 콜백에 전달하고, 콜백에서 키-값 쌍이 포함된 연관 배열을 반환해야 합니다:

```
use Illuminate\Support\Arr;

$array = [
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
];

$mapped = Arr::mapWithKeys($array, function (array $item, int $key) {
    return [$item['email'] => $item['name']];
});

/*
    [
        'john@example.com' => 'John',
        'jane@example.com' => 'Jane',
    ]
*/
```

<a name="method-array-only"></a>
#### `Arr::only()`

`Arr::only` 메서드는 지정한 키/값 쌍만을 포함하는 배열을 반환합니다:

```
use Illuminate\Support\Arr;

$array = ['name' => 'Desk', 'price' => 100, 'orders' => 10];

$slice = Arr::only($array, ['name', 'price']);

// ['name' => 'Desk', 'price' => 100]
```

<a name="method-array-pluck"></a>
#### `Arr::pluck()`

`Arr::pluck` 메서드는 배열에서 특정 키에 대한 모든 값을 추출합니다:

```
use Illuminate\Support\Arr;

$array = [
    ['developer' => ['id' => 1, 'name' => 'Taylor']],
    ['developer' => ['id' => 2, 'name' => 'Abigail']],
];

$names = Arr::pluck($array, 'developer.name');

// ['Taylor', 'Abigail']
```

두 번째 인자로 키가 될 값을 지정할 수도 있습니다:

```
use Illuminate\Support\Arr;

$names = Arr::pluck($array, 'developer.name', 'developer.id');

// [1 => 'Taylor', 2 => 'Abigail']
```

<a name="method-array-prepend"></a>
#### `Arr::prepend()`

`Arr::prepend` 메서드는 배열의 앞부분에 항목을 추가합니다:

```
use Illuminate\Support\Arr;

$array = ['one', 'two', 'three', 'four'];

$array = Arr::prepend($array, 'zero');

// ['zero', 'one', 'two', 'three', 'four']
```

키를 지정할 수도 있습니다:

```
use Illuminate\Support\Arr;

$array = ['price' => 100];

$array = Arr::prepend($array, 'Desk', 'name');

// ['name' => 'Desk', 'price' => 100]
```

<a name="method-array-prependkeyswith"></a>
#### `Arr::prependKeysWith()`

`Arr::prependKeysWith` 메서드는 연관 배열의 모든 키 이름에 지정한 접두사를 붙입니다:

```
use Illuminate\Support\Arr;

$array = [
    'name' => 'Desk',
    'price' => 100,
];

$keyed = Arr::prependKeysWith($array, 'product.');

/*
    [
        'product.name' => 'Desk',
        'product.price' => 100,
    ]
*/
```

<a name="method-array-pull"></a>
#### `Arr::pull()`

`Arr::pull` 메서드는 키/값 쌍을 배열에서 제거하고 그 값을 반환합니다:

```
use Illuminate\Support\Arr;

$array = ['name' => 'Desk', 'price' => 100];

$name = Arr::pull($array, 'name');

// $name: Desk

// $array: ['price' => 100]
```

존재하지 않는 키에 대해 기본값을 지정할 수 있습니다:

```
use Illuminate\Support\Arr;

$value = Arr::pull($array, $key, $default);
```

<a name="method-array-query"></a>
#### `Arr::query()`

`Arr::query` 메서드는 배열을 쿼리 문자열로 변환합니다:

```
use Illuminate\Support\Arr;

$array = [
    'name' => 'Taylor',
    'order' => [
        'column' => 'created_at',
        'direction' => 'desc'
    ]
];

Arr::query($array);

// name=Taylor&order[column]=created_at&order[direction]=desc
```

<a name="method-array-random"></a>
#### `Arr::random()`

`Arr::random` 메서드는 배열에서 랜덤한 값을 반환합니다:

```
use Illuminate\Support\Arr;

$array = [1, 2, 3, 4, 5];

$random = Arr::random($array);

// 4 - (랜덤으로 선택됨)
```

두 번째 인자로 반환 항목 개수를 지정할 수 있으며, 이 경우 결과는 배열로 반환됩니다:

```
use Illuminate\Support\Arr;

$items = Arr::random($array, 2);

// [2, 5] - (랜덤으로 선택됨)
```

<a name="method-array-reject"></a>
#### `Arr::reject()`

`Arr::reject` 메서드는 주어진 클로저 조건을 만족하는 배열 요소를 제거합니다:

```
use Illuminate\Support\Arr;

$array = [100, '200', 300, '400', 500];

$filtered = Arr::reject($array, function (string|int $value, int $key) {
    return is_string($value);
});

// [0 => 100, 2 => 300, 4 => 500]
```

<a name="method-array-set"></a>
#### `Arr::set()`

`Arr::set` 메서드는 "dot" 표기법으로 깊이 중첩된 배열에 값을 설정합니다:

```
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

Arr::set($array, 'products.desk.price', 200);

// ['products' => ['desk' => ['price' => 200]]]
```

<a name="method-array-shuffle"></a>
#### `Arr::shuffle()`

`Arr::shuffle` 메서드는 배열 항목을 무작위로 섞습니다:

```
use Illuminate\Support\Arr;

$array = Arr::shuffle([1, 2, 3, 4, 5]);

// [3, 2, 5, 1, 4] - (무작위 생성됨)
```

<a name="method-array-sort"></a>
#### `Arr::sort()`

`Arr::sort` 메서드는 배열을 값 기준으로 정렬합니다:

```
use Illuminate\Support\Arr;

$array = ['Desk', 'Table', 'Chair'];

$sorted = Arr::sort($array);

// ['Chair', 'Desk', 'Table']
```

클로저 결과에 따라 정렬할 수도 있습니다:

```
use Illuminate\Support\Arr;

$array = [
    ['name' => 'Desk'],
    ['name' => 'Table'],
    ['name' => 'Chair'],
];

$sorted = array_values(Arr::sort($array, function (array $value) {
    return $value['name'];
}));

/*
    [
        ['name' => 'Chair'],
        ['name' => 'Desk'],
        ['name' => 'Table'],
    ]
*/
```

<a name="method-array-sort-desc"></a>
#### `Arr::sortDesc()`

`Arr::sortDesc` 메서드는 배열을 값 기준으로 내림차순 정렬합니다:

```
use Illuminate\Support\Arr;

$array = ['Desk', 'Table', 'Chair'];

$sorted = Arr::sortDesc($array);

// ['Table', 'Desk', 'Chair']
```

클로저 결과에 따라 내림차순 정렬할 수도 있습니다:

```
use Illuminate\Support\Arr;

$array = [
    ['name' => 'Desk'],
    ['name' => 'Table'],
    ['name' => 'Chair'],
];

$sorted = array_values(Arr::sortDesc($array, function (array $value) {
    return $value['name'];
}));

/*
    [
        ['name' => 'Table'],
        ['name' => 'Desk'],
        ['name' => 'Chair'],
    ]
*/
```

<a name="method-array-sort-recursive"></a>
#### `Arr::sortRecursive()`

`Arr::sortRecursive` 메서드는 하위 배열이 숫자 인덱스인지, 연관 배열인지 판단해 각각 `sort` 또는 `ksort`를 재귀적으로 실행하여 배열 전체를 정렬합니다:

```
use Illuminate\Support\Arr;

$array = [
    ['Roman', 'Taylor', 'Li'],
    ['PHP', 'Ruby', 'JavaScript'],
    ['one' => 1, 'two' => 2, 'three' => 3],
];

$sorted = Arr::sortRecursive($array);

/*
    [
        ['JavaScript', 'PHP', 'Ruby'],
        ['one' => 1, 'three' => 3, 'two' => 2],
        ['Li', 'Roman', 'Taylor'],
    ]
*/
```

내림차순 정렬 결과가 필요하다면 `Arr::sortRecursiveDesc` 메서드를 사용하세요:

```
$sorted = Arr::sortRecursiveDesc($array);
```

<a name="method-array-take"></a>
#### `Arr::take()`

`Arr::take` 메서드는 지정한 개수만큼 요소를 포함하는 새 배열을 반환합니다:

```
use Illuminate\Support\Arr;

$array = [0, 1, 2, 3, 4, 5];

$chunk = Arr::take($array, 3);

// [0, 1, 2]
```

음수를 전달하면 배열 끝에서부터 해당 개수를 가져옵니다:

```
$array = [0, 1, 2, 3, 4, 5];

$chunk = Arr::take($array, -2);

// [4, 5]
```

<a name="method-array-to-css-classes"></a>
#### `Arr::toCssClasses()`

`Arr::toCssClasses` 메서드는 CSS 클래스 문자열을 조건부로 컴파일합니다. 배열의 키는 CSS 클래스 이름, 값은 논리 값이며, 만약 키가 숫자이면 무조건 포함됩니다:

```
use Illuminate\Support\Arr;

$isActive = false;
$hasError = true;

$array = ['p-4', 'font-bold' => $isActive, 'bg-red' => $hasError];

$classes = Arr::toCssClasses($array);

/*
    'p-4 bg-red'
*/
```

<a name="method-array-to-css-styles"></a>
#### `Arr::toCssStyles()`

`Arr::toCssStyles` 메서드는 CSS 스타일 문자열을 조건부로 컴파일합니다. 배열 키가 스타일 문자열, 값이 논리 표현식입니다. 숫자 키는 무조건 포함됩니다:

```php
use Illuminate\Support\Arr;

$hasColor = true;

$array = ['background-color: blue', 'color: blue' => $hasColor];

$classes = Arr::toCssStyles($array);

/*
    'background-color: blue; color: blue;'
*/
```

이 메서드는 Laravel의 [Blade 속성 백](https://laravel.com/docs/11.x/blade#conditionally-merge-classes)과 `@class` [Blade 지시자](https://laravel.com/docs/11.x/blade#conditional-classes)에 사용됩니다.

<a name="method-array-undot"></a>
#### `Arr::undot()`

`Arr::undot` 메서드는 "dot" 표기법을 사용한 단일 차원 배열을 다차원 배열로 확장합니다:

```
use Illuminate\Support\Arr;

$array = [
    'user.name' => 'Kevin Malone',
    'user.occupation' => 'Accountant',
];

$array = Arr::undot($array);

// ['user' => ['name' => 'Kevin Malone', 'occupation' => 'Accountant']]
```

<a name="method-array-where"></a>
#### `Arr::where()`

`Arr::where` 메서드는 주어진 클로저 조건에 따라 배열을 필터링합니다:

```
use Illuminate\Support\Arr;

$array = [100, '200', 300, '400', 500];

$filtered = Arr::where($array, function (string|int $value, int $key) {
    return is_string($value);
});

// [1 => '200', 3 => '400']
```

<a name="method-array-where-not-null"></a>
#### `Arr::whereNotNull()`

`Arr::whereNotNull` 메서드는 배열에서 모든 `null` 값을 제거합니다:

```
use Illuminate\Support\Arr;

$array = [0, null];

$filtered = Arr::whereNotNull($array);

// [0 => 0]
```

<a name="method-array-wrap"></a>
#### `Arr::wrap()`

`Arr::wrap` 메서드는 주어진 값을 배열로 감쌉니다. 값이 이미 배열이면 수정 없이 반환됩니다:

```
use Illuminate\Support\Arr;

$string = 'Laravel';

$array = Arr::wrap($string);

// ['Laravel']
```

값이 `null`이면 빈 배열이 반환됩니다:

```
use Illuminate\Support\Arr;

$array = Arr::wrap(null);

// []
```

<a name="method-data-fill"></a>
#### `data_fill()`

`data_fill` 함수는 "dot" 표기법을 사용해 중첩 배열 또는 객체에서 값이 없을 경우에만 값을 설정합니다:

```
$data = ['products' => ['desk' => ['price' => 100]]];

data_fill($data, 'products.desk.price', 200);

// ['products' => ['desk' => ['price' => 100]]]

data_fill($data, 'products.desk.discount', 10);

// ['products' => ['desk' => ['price' => 100, 'discount' => 10]]]
```

별표(*) 와일드카드를 지원하며 해당 경로에 값을 설정합니다:

```
$data = [
    'products' => [
        ['name' => 'Desk 1', 'price' => 100],
        ['name' => 'Desk 2'],
    ],
];

data_fill($data, 'products.*.price', 200);

/*
    [
        'products' => [
            ['name' => 'Desk 1', 'price' => 100],
            ['name' => 'Desk 2', 'price' => 200],
        ],
    ]
*/
```

<a name="method-data-get"></a>
#### `data_get()`

`data_get` 함수는 "dot" 표기법으로 복잡한 배열이나 객체에서 값을 가져옵니다:

```
$data = ['products' => ['desk' => ['price' => 100]]];

$price = data_get($data, 'products.desk.price');

// 100
```

존재하지 않을 때 기본값을 제공할 수 있습니다:

```
$discount = data_get($data, 'products.desk.discount', 0);

// 0
```

별표(*) 와일드카드로 여러 경로를 대상 지정할 수 있습니다:

```
$data = [
    'product-one' => ['name' => 'Desk 1', 'price' => 100],
    'product-two' => ['name' => 'Desk 2', 'price' => 150],
];

data_get($data, '*.name');

// ['Desk 1', 'Desk 2'];
```

`{first}` 및 `{last}` 플레이스홀더로 배열의 첫 번째 또는 마지막 항목을 지정할 수도 있습니다:

```
$flight = [
    'segments' => [
        ['from' => 'LHR', 'departure' => '9:00', 'to' => 'IST', 'arrival' => '15:00'],
        ['from' => 'IST', 'departure' => '16:00', 'to' => 'PKX', 'arrival' => '20:00'],
    ],
];

data_get($flight, 'segments.{first}.arrival');

// 15:00
```

<a name="method-data-set"></a>
#### `data_set()`

`data_set` 함수는 "dot" 표기법을 사용해 중첩 배열이나 객체에 값을 설정합니다:

```
$data = ['products' => ['desk' => ['price' => 100]]];

data_set($data, 'products.desk.price', 200);

// ['products' => ['desk' => ['price' => 200]]]
```

별표(*) 와일드카드로 지정된 여러 대상에 값 설정도 지원합니다:

```
$data = [
    'products' => [
        ['name' => 'Desk 1', 'price' => 100],
        ['name' => 'Desk 2', 'price' => 150],
    ],
];

data_set($data, 'products.*.price', 200);

/*
    [
        'products' => [
            ['name' => 'Desk 1', 'price' => 200],
            ['name' => 'Desk 2', 'price' => 200],
        ],
    ]
*/
```

기존 값을 덮어쓰지 않으려면 네 번째 인수로 `false`를 전달하세요:

```
$data = ['products' => ['desk' => ['price' => 100]]];

data_set($data, 'products.desk.price', 200, overwrite: false);

// ['products' => ['desk' => ['price' => 100]]]
```

<a name="method-data-forget"></a>
#### `data_forget()`

`data_forget` 함수는 "dot" 표기법으로 중첩 배열이나 객체에서 값을 제거합니다:

```
$data = ['products' => ['desk' => ['price' => 100]]];

data_forget($data, 'products.desk.price');

// ['products' => ['desk' => []]]
```

별표(*) 와일드카드도 지원합니다:

```
$data = [
    'products' => [
        ['name' => 'Desk 1', 'price' => 100],
        ['name' => 'Desk 2', 'price' => 150],
    ],
];

data_forget($data, 'products.*.price');

/*
    [
        'products' => [
            ['name' => 'Desk 1'],
            ['name' => 'Desk 2'],
        ],
    ]
*/
```

<a name="method-head"></a>
#### `head()`

`head` 함수는 주어진 배열의 첫 번째 요소를 반환합니다:

```
$array = [100, 200, 300];

$first = head($array);

// 100
```

<a name="method-last"></a>
#### `last()`

`last` 함수는 주어진 배열의 마지막 요소를 반환합니다:

```
$array = [100, 200, 300];

$last = last($array);

// 300
```

<a name="numbers"></a>
## 숫자 (Numbers)

<a name="method-number-abbreviate"></a>
#### `Number::abbreviate()`

`Number::abbreviate` 메서드는 숫자 값을 축약 단위와 함께 사람이 읽기 쉬운 형식으로 반환합니다:

```
use Illuminate\Support\Number;

$number = Number::abbreviate(1000);

// 1K

$number = Number::abbreviate(489939);

// 490K

$number = Number::abbreviate(1230000, precision: 2);

// 1.23M
```

<a name="method-number-clamp"></a>
#### `Number::clamp()`

`Number::clamp` 메서드는 숫자를 지정한 범위 내로 제한합니다. 최소값보다 작으면 최소값, 최대값보다 크면 최대값을 반환합니다:

```
use Illuminate\Support\Number;

$number = Number::clamp(105, min: 10, max: 100);

// 100

$number = Number::clamp(5, min: 10, max: 100);

// 10

$number = Number::clamp(10, min: 10, max: 100);

// 10

$number = Number::clamp(20, min: 10, max: 100);

// 20
```

<a name="method-number-currency"></a>
#### `Number::currency()`

`Number::currency` 메서드는 주어진 값의 통화 표현을 문자열로 반환합니다:

```
use Illuminate\Support\Number;

$currency = Number::currency(1000);

// $1,000.00

$currency = Number::currency(1000, in: 'EUR');

// €1,000.00

$currency = Number::currency(1000, in: 'EUR', locale: 'de');

// 1.000,00 €
```

<a name="method-default-currency"></a>
#### `Number::defaultCurrency()`

`Number::defaultCurrency` 메서드는 `Number` 클래스가 기본으로 사용하는 통화를 반환합니다:

```
use Illuminate\Support\Number;

$currency = Number::defaultCurrency();

// USD
```

<a name="method-default-locale"></a>
#### `Number::defaultLocale()`

`Number::defaultLocale` 메서드는 `Number` 클래스가 기본으로 사용하는 로케일을 반환합니다:

```
use Illuminate\Support\Number;

$locale = Number::defaultLocale();

// en
```

<a name="method-number-file-size"></a>
#### `Number::fileSize()`

`Number::fileSize` 메서드는 바이트 값을 사람이 읽기 쉬운 파일 크기 문자열로 반환합니다:

```
use Illuminate\Support\Number;

$size = Number::fileSize(1024);

// 1 KB

$size = Number::fileSize(1024 * 1024);

// 1 MB

$size = Number::fileSize(1024, precision: 2);

// 1.00 KB
```

<a name="method-number-for-humans"></a>
#### `Number::forHumans()`

`Number::forHumans` 메서드는 숫자를 사람이 읽기 쉬운 형식으로 변환합니다:

```
use Illuminate\Support\Number;

$number = Number::forHumans(1000);

// 1 thousand

$number = Number::forHumans(489939);

// 490 thousand

$number = Number::forHumans(1230000, precision: 2);

// 1.23 million
```

<a name="method-number-format"></a>
#### `Number::format()`

`Number::format` 메서드는 숫자를 로케일 별 문자열로 포맷합니다:

```
use Illuminate\Support\Number;

$number = Number::format(100000);

// 100,000

$number = Number::format(100000, precision: 2);

// 100,000.00

$number = Number::format(100000.123, maxPrecision: 2);

// 100,000.12

$number = Number::format(100000, locale: 'de');

// 100.000
```

<a name="method-number-ordinal"></a>
#### `Number::ordinal()`

`Number::ordinal` 메서드는 숫자의 서수 표현을 반환합니다:

```
use Illuminate\Support\Number;

$number = Number::ordinal(1);

// 1st

$number = Number::ordinal(2);

// 2nd

$number = Number::ordinal(21);

// 21st
```

<a name="method-number-pairs"></a>
#### `Number::pairs()`

`Number::pairs` 메서드는 주어진 범위와 단계 값을 기반으로 번호 쌍(하위 범위) 배열을 생성합니다. 예를 들어 페이징이나 작업 배치 등에 유용합니다:

```php
use Illuminate\Support\Number;

$result = Number::pairs(25, 10);

// [[1, 10], [11, 20], [21, 25]]

$result = Number::pairs(25, 10, offset: 0);

// [[0, 10], [10, 20], [20, 25]]
```

<a name="method-number-percentage"></a>
#### `Number::percentage()`

`Number::percentage` 메서드는 숫자를 퍼센트 표현 문자열로 반환합니다:

```
use Illuminate\Support\Number;

$percentage = Number::percentage(10);

// 10%

$percentage = Number::percentage(10, precision: 2);

// 10.00%

$percentage = Number::percentage(10.123, maxPrecision: 2);

// 10.12%

$percentage = Number::percentage(10, precision: 2, locale: 'de');

// 10,00%
```

<a name="method-number-spell"></a>
#### `Number::spell()`

`Number::spell` 메서드는 숫자를 단어 형태로 변환합니다:

```
use Illuminate\Support\Number;

$number = Number::spell(102);

// one hundred and two

$number = Number::spell(88, locale: 'fr');

// quatre-vingt-huit
```

`after` 인수로 지정된 값 이후의 숫자만 단어로 변환하는 것도 가능합니다:

```
$number = Number::spell(10, after: 10);

// 10

$number = Number::spell(11, after: 10);

// eleven
```

`until` 인수로 지정된 값 이전의 숫자만 단어로 변환할 수도 있습니다:

```
$number = Number::spell(5, until: 10);

// five

$number = Number::spell(10, until: 10);

// 10
```

<a name="method-number-trim"></a>
#### `Number::trim()`

`Number::trim` 메서드는 소수점 뒤 불필요한 0을 제거합니다:

```
use Illuminate\Support\Number;

$number = Number::trim(12.0);

// 12

$number = Number::trim(12.30);

// 12.3
```

<a name="method-number-use-locale"></a>
#### `Number::useLocale()`

`Number::useLocale` 메서드는 `Number` 클래스의 기본 로케일을 전역 설정합니다. 이후 호출되는 메서드에 이 설정이 반영됩니다:

```
use Illuminate\Support\Number;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Number::useLocale('de');
}
```

<a name="method-number-with-locale"></a>
#### `Number::withLocale()`

`Number::withLocale` 메서드는 지정한 로케일을 적용해 주어진 콜백을 실행하고, 실행 후 원래 로케일로 복원합니다:

```
use Illuminate\Support\Number;

$number = Number::withLocale('de', function () {
    return Number::format(1500);
});
```

<a name="method-number-use-currency"></a>
#### `Number::useCurrency()`

`Number::useCurrency` 메서드는 `Number` 클래스의 기본 통화를 전역 설정합니다:

```
use Illuminate\Support\Number;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Number::useCurrency('GBP');
}
```

<a name="method-number-with-currency"></a>
#### `Number::withCurrency()`

`Number::withCurrency` 메서드는 지정한 통화를 적용해 콜백을 실행하고, 실행 후 기본 통화를 복원합니다:

```
use Illuminate\Support\Number;

$number = Number::withCurrency('GBP', function () {
    // ...
});
```

<a name="paths"></a>
## 경로 (Paths)

<a name="method-app-path"></a>
#### `app_path()`

`app_path` 함수는 애플리케이션의 `app` 디렉토리에 대한 절대 경로를 반환합니다. 경로 뒤에 파일명이나 디렉토리를 붙여 상대 경로를 생성할 수 있습니다:

```
$path = app_path();

$path = app_path('Http/Controllers/Controller.php');
```

<a name="method-base-path"></a>
#### `base_path()`

`base_path` 함수는 애플리케이션 루트 디렉토리의 절대 경로를 반환합니다. 상대 경로나 파일명도 지정할 수 있습니다:

```
$path = base_path();

$path = base_path('vendor/bin');
```

<a name="method-config-path"></a>
#### `config_path()`

`config_path` 함수는 애플리케이션의 `config` 디렉토리에 대한 절대 경로를 반환합니다:

```
$path = config_path();

$path = config_path('app.php');
```

<a name="method-database-path"></a>
#### `database_path()`

`database_path` 함수는 애플리케이션의 `database` 디렉토리 절대 경로를 반환합니다:

```
$path = database_path();

$path = database_path('factories/UserFactory.php');
```

<a name="method-lang-path"></a>
#### `lang_path()`

`lang_path` 함수는 애플리케이션의 `lang` 디렉토리 절대 경로를 반환합니다:

```
$path = lang_path();

$path = lang_path('en/messages.php');
```

> [!NOTE]  
> 기본적으로 Laravel 애플리케이션 스켈레톤에는 `lang` 디렉토리가 포함되어 있지 않습니다. 언어 파일을 커스터마이징하려면 `lang:publish` Artisan 명령어로 게시할 수 있습니다.

<a name="method-mix"></a>
#### `mix()`

`mix` 함수는 [버전 관리된 Mix 파일](/docs/11.x/mix)의 경로를 반환합니다:

```
$path = mix('css/app.css');
```

<a name="method-public-path"></a>
#### `public_path()`

`public_path` 함수는 애플리케이션의 `public` 디렉토리 절대 경로를 반환합니다:

```
$path = public_path();

$path = public_path('css/app.css');
```

<a name="method-resource-path"></a>
#### `resource_path()`

`resource_path` 함수는 애플리케이션의 `resources` 디렉토리 절대 경로를 반환합니다:

```
$path = resource_path();

$path = resource_path('sass/app.scss');
```

<a name="method-storage-path"></a>
#### `storage_path()`

`storage_path` 함수는 애플리케이션의 `storage` 디렉토리 절대 경로를 반환합니다:

```
$path = storage_path();

$path = storage_path('app/file.txt');
```

<a name="urls"></a>
## URL (URLs)

<a name="method-action"></a>
#### `action()`

`action` 함수는 주어진 컨트롤러 액션에 대한 URL을 생성합니다:

```
use App\Http\Controllers\HomeController;

$url = action([HomeController::class, 'index']);
```

액션에 라우트 파라미터가 있다면 두 번째 인자로 전달할 수 있습니다:

```
$url = action([UserController::class, 'profile'], ['id' => 1]);
```

<a name="method-asset"></a>
#### `asset()`

`asset` 함수는 현재 요청의 스킴(HTTP/HTTPS)을 사용해 애셋 URL을 생성합니다:

```
$url = asset('img/photo.jpg');
```

`.env` 파일에서 `ASSET_URL` 변수를 설정하면 외부 호스트에서 애셋을 제공할 때 유용합니다:

```
// ASSET_URL=http://example.com/assets

$url = asset('img/photo.jpg'); // http://example.com/assets/img/photo.jpg
```

<a name="method-route"></a>
#### `route()`

`route` 함수는 이름 있는 라우트(named route)에 대한 URL을 생성합니다:

```
$url = route('route.name');
```

라벨 파라미터가 있다면 두 번째 인자로 전달합니다:

```
$url = route('route.name', ['id' => 1]);
```

기본적으로 절대 URL을 생성하며, 상대 URL이 필요하면 세 번째 인자에 `false`를 전달하세요:

```
$url = route('route.name', ['id' => 1], false);
```

<a name="method-secure-asset"></a>
#### `secure_asset()`

`secure_asset` 함수는 HTTPS 프로토콜로 애셋 URL을 생성합니다:

```
$url = secure_asset('img/photo.jpg');
```

<a name="method-secure-url"></a>
#### `secure_url()`

`secure_url` 함수는 지정한 경로에 대해 완전한 HTTPS URL을 생성합니다. 추가 세그먼트는 두 번째 인자로 전달할 수 있습니다:

```
$url = secure_url('user/profile');

$url = secure_url('user/profile', [1]);
```

<a name="method-to-route"></a>
#### `to_route()`

`to_route` 함수는 주어진 이름 있는 라우트로 리다이렉트 HTTP 응답을 생성합니다:

```
return to_route('users.show', ['user' => 1]);
```

HTTP 상태 코드 및 추가 헤더도 세 번째, 네 번째 인자로 전달할 수 있습니다:

```
return to_route('users.show', ['user' => 1], 302, ['X-Framework' => 'Laravel']);
```

<a name="method-url"></a>
#### `url()`

`url` 함수는 주어진 경로에 대해 완전한 URL을 생성합니다:

```
$url = url('user/profile');

$url = url('user/profile', [1]);
```

경로를 생략하면 `Illuminate\Routing\UrlGenerator` 인스턴스가 반환됩니다:

```
$current = url()->current();

$full = url()->full();

$previous = url()->previous();
```

<a name="miscellaneous"></a>
## 기타 (Miscellaneous)

<a name="method-abort"></a>
#### `abort()`

`abort` 함수는 [HTTP 예외](/docs/11.x/errors#http-exceptions)를 발생시키며, [예외 핸들러](/docs/11.x/errors#handling-exceptions)에 의해 처리됩니다:

```
abort(403);
```

예외 메시지와 커스텀 HTTP 응답 헤더를 지정할 수도 있습니다:

```
abort(403, 'Unauthorized.', $headers);
```

<a name="method-abort-if"></a>
#### `abort_if()`

`abort_if` 함수는 주어진 조건이 참일 때 HTTP 예외를 발생시킵니다:

```
abort_if(! Auth::user()->isAdmin(), 403);
```

`abort` 함수와 동일하게 메시지 및 헤더도 지정할 수 있습니다.

<a name="method-abort-unless"></a>
#### `abort_unless()`

`abort_unless` 함수는 주어진 조건이 거짓일 때 HTTP 예외를 발생시킵니다:

```
abort_unless(Auth::user()->isAdmin(), 403);
```

`abort` 함수와 동일하게 메시지 및 헤더도 지정할 수 있습니다.

<a name="method-app"></a>
#### `app()`

`app` 함수는 [서비스 컨테이너](/docs/11.x/container) 인스턴스를 반환합니다:

```
$container = app();
```

클래스명 또는 인터페이스를 인자로 전달하면 해당 인스턴스로 해석합니다:

```
$api = app('HelpSpot\API');
```

<a name="method-auth"></a>
#### `auth()`

`auth` 함수는 [인증 인스턴스](/docs/11.x/authentication)를 반환합니다. `Auth` 파사드 대용으로 사용할 수 있습니다:

```
$user = auth()->user();
```

특정 가드를 지정할 수도 있습니다:

```
$user = auth('admin')->user();
```

<a name="method-back"></a>
#### `back()`

`back` 함수는 이전 사용자 위치로 리다이렉트 HTTP 응답을 생성합니다:

```
return back($status = 302, $headers = [], $fallback = '/');

return back();
```

<a name="method-bcrypt"></a>
#### `bcrypt()`

`bcrypt` 함수는 Bcrypt 해싱 알고리즘을 사용해 값을 해싱합니다. `Hash` 파사드 대안입니다:

```
$password = bcrypt('my-secret-password');
```

<a name="method-blank"></a>
#### `blank()`

`blank` 함수는 주어진 값이 "비어 있음"인지 판단합니다:

```
blank('');
blank('   ');
blank(null);
blank(collect());

// true

blank(0);
blank(true);
blank(false);

// false
```

반대 개념은 [`filled`](#method-filled) 메서드를 참고하세요.

<a name="method-broadcast"></a>
#### `broadcast()`

`broadcast` 함수는 주어진 [이벤트](/docs/11.x/events)를 방송합니다:

```
broadcast(new UserRegistered($user));

broadcast(new UserRegistered($user))->toOthers();
```

<a name="method-cache"></a>
#### `cache()`

`cache` 함수는 [캐시](/docs/11.x/cache)에서 값을 조회하거나 저장할 수 있습니다:

캐시에서 값 조회:

```
$value = cache('key');

$value = cache('key', 'default');
```

캐시에 값 저장:

```
cache(['key' => 'value'], 300);

cache(['key' => 'value'], now()->addSeconds(10));
```

<a name="method-class-uses-recursive"></a>
#### `class_uses_recursive()`

`class_uses_recursive` 함수는 클래스와 부모 클래스가 사용하는 모든 트레이트를 반환합니다:

```
$traits = class_uses_recursive(App\Models\User::class);
```

<a name="method-collect"></a>
#### `collect()`

`collect` 함수는 주어진 값을 [컬렉션](/docs/11.x/collections)으로 생성합니다:

```
$collection = collect(['taylor', 'abigail']);
```

<a name="method-config"></a>
#### `config()`

`config` 함수는 [설정 변수](/docs/11.x/configuration)를 조회하거나 변경합니다. "dot" 구문으로 접근 가능하며, 기본값도 지정할 수 있습니다:

값 조회:

```
$value = config('app.timezone');

$value = config('app.timezone', $default);
```

값 설정:

```
config(['app.debug' => true]);
```

설정은 요청 범위 내에서만 유효하며 실제 설정 파일을 변경하지는 않습니다.

<a name="method-context"></a>
#### `context()`

`context` 함수는 [현재 컨텍스트](/docs/11.x/context) 값을 가져오거나, 없으면 기본값을 반환합니다:

```
$value = context('trace_id');

$value = context('trace_id', $default);
```

컨텍스트 값 설정:

```
use Illuminate\Support\Str;

context(['trace_id' => Str::uuid()->toString()]);
```

<a name="method-cookie"></a>
#### `cookie()`

`cookie` 함수는 새로운 [쿠키](/docs/11.x/requests#cookies) 인스턴스를 생성합니다:

```
$cookie = cookie('name', 'value', $minutes);
```

<a name="method-csrf-field"></a>
#### `csrf_field()`

`csrf_field` 함수는 CSRF 토큰을 가진 HTML `hidden` 필드를 생성합니다. Blade 예시는 다음과 같습니다:

```
{{ csrf_field() }}
```

<a name="method-csrf-token"></a>
#### `csrf_token()`

`csrf_token` 함수는 현재 CSRF 토큰 값을 가져옵니다:

```
$token = csrf_token();
```

<a name="method-decrypt"></a>
#### `decrypt()`

`decrypt` 함수는 암호화된 값을 복호화합니다. `Crypt` 파사드 대안입니다:

```
$password = decrypt($value);
```

<a name="method-dd"></a>
#### `dd()`

`dd` 함수는 변수를 덤프하고 스크립트 실행을 종료합니다:

```
dd($value);

dd($value1, $value2, $value3, ...);
```

실행 중지는 원하지 않을 경우 [`dump`](#method-dump) 함수를 사용하세요.

<a name="method-dispatch"></a>
#### `dispatch()`

`dispatch` 함수는 주어진 [잡](/docs/11.x/queues#creating-jobs)을 Laravel [잡 큐](/docs/11.x/queues)에 넣습니다:

```
dispatch(new App\Jobs\SendEmails);
```

<a name="method-dispatch-sync"></a>
#### `dispatch_sync()`

`dispatch_sync` 함수는 잡을 즉시 처리되는 동기 큐로 보냅니다:

```
dispatch_sync(new App\Jobs\SendEmails);
```

<a name="method-dump"></a>
#### `dump()`

`dump` 함수는 변수를 덤프합니다:

```
dump($value);

dump($value1, $value2, $value3, ...);
```

`dd`처럼 실행을 중단하지 않습니다.

<a name="method-encrypt"></a>
#### `encrypt()`

`encrypt` 함수는 값을 암호화합니다. `Crypt` 파사드의 대안입니다:

```
$secret = encrypt('my-secret-value');
```

<a name="method-env"></a>
#### `env()`

`env` 함수는 [환경 변수](/docs/11.x/configuration#environment-configuration)을 조회하거나 기본값을 반환합니다:

```
$env = env('APP_ENV');

$env = env('APP_ENV', 'production');
```

> [!WARNING]  
> `config:cache` 명령 실행 후에는 `.env` 파일이 로드되지 않으니, `env` 호출은 설정 파일 내에서만 하세요. 그렇지 않으면 모든 `env` 호출이 `null`을 반환합니다.

<a name="method-event"></a>
#### `event()`

`event` 함수는 주어진 [이벤트](/docs/11.x/events)를 디스패치합니다:

```
event(new UserRegistered($user));
```

<a name="method-fake"></a>
#### `fake()`

`fake` 함수는 Faker 싱글톤을 컨테이너에서 해석합니다. 모델 팩토리, 데이터 시딩, 테스트, 뷰 프로토타이핑에 유용합니다:

```blade
@for($i = 0; $i < 10; $i++)
    <dl>
        <dt>Name</dt>
        <dd>{{ fake()->name() }}</dd>

        <dt>Email</dt>
        <dd>{{ fake()->unique()->safeEmail() }}</dd>
    </dl>
@endfor
```

기본 로케일은 `config/app.php`의 `app.faker_locale` 옵션이나 `APP_FAKER_LOCALE` 환경 변수로 설정됩니다. 로케일을 직접 지정할 수도 있으며, 로케일별로 싱글톤이 개별해석됩니다:

```
fake('nl_NL')->name()
```

<a name="method-filled"></a>
#### `filled()`

`filled` 함수는 주어진 값이 "비어 있지 않음"인지 판단합니다:

```
filled(0);
filled(true);
filled(false);

// true

filled('');
filled('   ');
filled(null);
filled(collect());

// false
```

`blank` 함수는 반대 개념입니다.

<a name="method-info"></a>
#### `info()`

`info` 함수는 애플리케이션 로그에 정보를 기록합니다:

```
info('Some helpful information!');
```

문맥 데이터도 함께 전달 가능:

```
info('User login attempt failed.', ['id' => $user->id]);
```

<a name="method-literal"></a>
#### `literal()`

`literal` 함수는 주어진 명명 인자를 속성으로 가진 새 `stdClass` 인스턴스를 생성합니다:

```
$obj = literal(
    name: 'Joe',
    languages: ['PHP', 'Ruby'],
);

$obj->name; // 'Joe'
$obj->languages; // ['PHP', 'Ruby']
```

<a name="method-logger"></a>
#### `logger()`

`logger` 함수는 디버그 레벨 로그를 기록합니다:

```
logger('Debug message');
```

문맥 정보를 전달할 수도 있습니다:

```
logger('User has logged in.', ['id' => $user->id]);
```

인자가 없으면 로거 인스턴스를 반환합니다:

```
logger()->error('You are not allowed here.');
```

<a name="method-method-field"></a>
#### `method_field()`

`method_field` 함수는 HTML `hidden` 필드를 생성하여 폼의 HTTP 메서드를 위조할 때 사용합니다. Blade 예시:

```
<form method="POST">
    {{ method_field('DELETE') }}
</form>
```

<a name="method-now"></a>
#### `now()`

`now` 함수는 현재 시간을 나타내는 새 `Illuminate\Support\Carbon` 인스턴스를 생성합니다:

```
$now = now();
```

<a name="method-old"></a>
#### `old()`

`old` 함수는 세션에 플래시된 [이전 입력값](/docs/11.x/requests#old-input)을 가져옵니다:

```
$value = old('value');

$value = old('value', 'default');
```

Eloquent 모델의 속성도 기본값으로 간단히 전달할 수 있습니다:

```
{{ old('name', $user->name) }}

// 기본적으로 아래와 동등합니다...

{{ old('name', $user) }}
```

<a name="method-once"></a>
#### `once()`

`once` 함수는 요청 기간 동안 콜백의 실행 결과를 메모리에 캐싱하여, 같은 콜백이 반복 호출될 때 이전 결과를 반환합니다:

```
function random(): int
{
    return once(function () {
        return random_int(1, 1000);
    });
}

random(); // 123
random(); // 123 (캐싱 결과)
random(); // 123 (캐싱 결과)
```

객체 인스턴스 내에서 호출하면, 인스턴스별로 고유 캐시가 적용됩니다:

```php
<?php

class NumberService
{
    public function all(): array
    {
        return once(fn () => [1, 2, 3]);
    }
}

$service = new NumberService;

$service->all();
$service->all(); // (캐싱 결과)

$secondService = new NumberService;

$secondService->all();
$secondService->all(); // (캐싱 결과)
```

<a name="method-optional"></a>
#### `optional()`

`optional` 함수는 어떤 값이든 받아 프로퍼티 접근이나 메서드 호출을 허용하며, 인자가 `null`이라면 `null`을 반환해 오류를 막습니다:

```
return optional($user->address)->street;

{!! old('name', optional($user)->name) !!}
```

두 번째 인자로 클로저를 받아, 값이 `null`이 아니면 클로저를 실행할 수도 있습니다:

```
return optional(User::find($id), function (User $user) {
    return $user->name;
});
```

<a name="method-policy"></a>
#### `policy()`

`policy` 함수는 주어진 클래스에 대한 [정책](/docs/11.x/authorization#creating-policies) 인스턴스를 반환합니다:

```
$policy = policy(App\Models\User::class);
```

<a name="method-redirect"></a>
#### `redirect()`

`redirect` 함수는 리다이렉트 HTTP 응답을 반환하거나, 인자가 없을 경우 리다이렉터 인스턴스를 반환합니다:

```
return redirect($to = null, $status = 302, $headers = [], $https = null);

return redirect('/home');

return redirect()->route('route.name');
```

<a name="method-report"></a>
#### `report()`

`report` 함수는 예외를 [예외 처리기](/docs/11.x/errors#handling-exceptions)에 보고합니다:

```
report($e);
```

문자열 인자를 받으면 메시지로 하는 예외를 생성해 보고합니다:

```
report('Something went wrong.');
```

<a name="method-report-if"></a>
#### `report_if()`

`report_if` 함수는 조건이 참일 때 예외를 보고합니다:

```
report_if($shouldReport, $e);

report_if($shouldReport, 'Something went wrong.');
```

<a name="method-report-unless"></a>
#### `report_unless()`

`report_unless` 함수는 조건이 거짓일 때 예외를 보고합니다:

```
report_unless($reportingDisabled, $e);

report_unless($reportingDisabled, 'Something went wrong.');
```

<a name="method-request"></a>
#### `request()`

`request` 함수는 현재 [요청](/docs/11.x/requests) 인스턴스를 반환하거나, 입력 값을 가져옵니다:

```
$request = request();

$value = request('key', $default);
```

<a name="method-rescue"></a>
#### `rescue()`

`rescue` 함수는 주어진 클로저 실행 중 발생하는 예외를 잡아내고, 예외 처리기에도 보고하면서 요청 처리를 계속합니다:

```
return rescue(function () {
    return $this->method();
});
```

두 번째 인자로 예외 발생 시 반환할 기본값이나 클로저를 지정할 수 있습니다:

```
return rescue(function () {
    return $this->method();
}, false);

return rescue(function () {
    return $this->method();
}, function () {
    return $this->failure();
});
```

`report` 인자를 지정하면, 예외를 보고할지 여부를 결정할 수 있습니다:

```
return rescue(function () {
    return $this->method();
}, report: function (Throwable $throwable) {
    return $throwable instanceof InvalidArgumentException;
});
```

<a name="method-resolve"></a>
#### `resolve()`

`resolve` 함수는 [서비스 컨테이너](/docs/11.x/container)를 사용해 클래스나 인터페이스를 인스턴스로 해석합니다:

```
$api = resolve('HelpSpot\API');
```

<a name="method-response"></a>
#### `response()`

`response` 함수는 [응답](/docs/11.x/responses) 인스턴스를 생성하거나, 응답 팩토리 인스턴스를 반환합니다:

```
return response('Hello World', 200, $headers);

return response()->json(['foo' => 'bar'], 200, $headers);
```

<a name="method-retry"></a>
#### `retry()`

`retry` 함수는 최대 시도 횟수까지 콜백 실행을 반복하며, 예외가 발생하면 재시도합니다. 예외 없이 성공하면 결과를 반환하며, 최대 시도를 초과하면 예외를 던집니다:

```
return retry(5, function () {
    // 5회까지 시도하며, 시도 간 100ms 휴식...
}, 100);
```

시도 간 대기 시간을 밀리초로 수동 계산하려면 세 번째 인자에 클로저를 전달합니다:

```
use Exception;

return retry(5, function () {
    // ...
}, function (int $attempt, Exception $exception) {
    return $attempt * 100;
});
```

첫 번째 인자로 대기 시간을 배열로 전달해 각 시도 간 대기 시간을 지정할 수 있습니다:

```
return retry([100, 200], function () {
    // 첫 번째 재시도 시 100ms, 두 번째 200ms 휴식...
});
```

특정 조건에서만 재시도하려면 네 번째 인자로 조건 클로저를 전달하세요:

```
use Exception;

return retry(5, function () {
    // ...
}, 100, function (Exception $exception) {
    return $exception instanceof RetryException;
});
```

<a name="method-session"></a>
#### `session()`

`session` 함수로 [세션](/docs/11.x/session) 값을 조회하거나 설정할 수 있습니다:

조회:

```
$value = session('key');
```

설정:

```
session(['chairs' => 7, 'instruments' => 3]);
```

세션 스토어를 반환할 수도 있습니다:

```
$value = session()->get('key');

session()->put('key', $value);
```

<a name="method-tap"></a>
#### `tap()`

`tap` 함수는 `$value`와 클로저를 받아, `$value`를 클로저에 전달 후 `$value`를 반환합니다. 클로저 반환값은 무시합니다:

```
$user = tap(User::first(), function (User $user) {
    $user->name = 'taylor';

    $user->save();
});
```

클로저를 생략하면 `$value` 메서드를 호출해도 반환값이 항상 `$value`가 됩니다. 예를 들어, `update` 메서드가 원래 정수 반환해도 이렇게:

```
$user = tap($user)->update([
    'name' => $name,
    'email' => $email,
]);
```

클래스에 `Illuminate\Support\Traits\Tappable` 트레이트를 추가하면, 그 객체 인스턴스에서도 `tap` 메서드를 사용할 수 있습니다:

```
return $user->tap(function (User $user) {
    // ...
});
```

<a name="method-throw-if"></a>
#### `throw_if()`

`throw_if` 함수는 조건이 참이면 지정한 예외를 던집니다:

```
throw_if(! Auth::user()->isAdmin(), AuthorizationException::class);

throw_if(
    ! Auth::user()->isAdmin(),
    AuthorizationException::class,
    'You are not allowed to access this page.'
);
```

<a name="method-throw-unless"></a>
#### `throw_unless()`

`throw_unless` 함수는 조건이 거짓이면 지정한 예외를 던집니다:

```
throw_unless(Auth::user()->isAdmin(), AuthorizationException::class);

throw_unless(
    Auth::user()->isAdmin(),
    AuthorizationException::class,
    'You are not allowed to access this page.'
);
```

<a name="method-today"></a>
#### `today()`

`today` 함수는 현재 날짜를 나타내는 새 `Illuminate\Support\Carbon` 인스턴스를 생성합니다:

```
$today = today();
```

<a name="method-trait-uses-recursive"></a>
#### `trait_uses_recursive()`

`trait_uses_recursive` 함수는 주어진 트레이트와 하위 트레이트들에서 사용하는 모든 트레이트를 반환합니다:

```
$traits = trait_uses_recursive(\Illuminate\Notifications\Notifiable::class);
```

<a name="method-transform"></a>
#### `transform()`

`transform` 함수는 값이 [blank](#method-blank)하지 않으면 클로저를 실행하고, 클로저 반환 값을 반환합니다:

```
$callback = function (int $value) {
    return $value * 2;
};

$result = transform(5, $callback);

// 10
```

값이 blank할 때 반환할 기본값이나 클로저도 지정할 수 있습니다:

```
$result = transform(null, $callback, 'The value is blank');

// The value is blank
```

<a name="method-validator"></a>
#### `validator()`

`validator` 함수는 주어진 인수로 [검증기](/docs/11.x/validation)를 생성합니다. `Validator` 파사드 대안입니다:

```
$validator = validator($data, $rules, $messages);
```

<a name="method-value"></a>
#### `value()`

`value` 함수는 인자를 그대로 반환합니다. 만약 인자가 클로저라면, 실행 결과를 반환합니다:

```
$result = value(true);

// true

$result = value(function () {
    return false;
});

// false
```

추가 인수가 있으면, 클로저에 인수로 전달합니다:

```
$result = value(function (string $name) {
    return $name;
}, 'Taylor');

// 'Taylor'
```

<a name="method-view"></a>
#### `view()`

`view` 함수는 [뷰](/docs/11.x/views) 인스턴스를 반환합니다:

```
return view('auth.login');
```

<a name="method-with"></a>
#### `with()`

`with` 함수는 값을 반환하며, 두 번째 인자로 클로저가 있으면 실행 결과를 반환합니다:

```
$callback = function (mixed $value) {
    return is_numeric($value) ? $value * 2 : 0;
};

$result = with(5, $callback);

// 10

$result = with(null, $callback);

// 0

$result = with(5, null);

// 5
```

<a name="method-when"></a>
#### `when()`

`when` 함수는 조건이 참이면 값을 반환하고, 거짓이면 `null`을 반환합니다. 두 번째 인자가 클로저면 실행 결과를 반환합니다:

```
$value = when(true, 'Hello World');

$value = when(true, fn () => 'Hello World');
```

주로 조건부 HTML 속성 표현에 유용합니다:

```blade
<div {!! when($condition, 'wire:poll="calculate"') !!}>
    ...
</div>
```

<a name="other-utilities"></a>
## 기타 유틸리티 (Other Utilities)

<a name="benchmarking"></a>
### 벤치마킹 (Benchmarking)

애플리케이션의 특정 부분 성능을 빠르게 테스트하고 싶을 때, `Benchmark` 클래스를 사용해 콜백 실행 시간을 측정할 수 있습니다:

```
<?php

use App\Models\User;
use Illuminate\Support\Benchmark;

Benchmark::dd(fn () => User::find(1)); // 0.1 ms

Benchmark::dd([
    'Scenario 1' => fn () => User::count(), // 0.5 ms
    'Scenario 2' => fn () => User::all()->count(), // 20.0 ms
]);
```

기본적으로 콜백은 한 번 실행되며, 실행 시간은 브라우저 또는 콘솔에 표시됩니다.

여러 번 실행하여 평균 실행 시간을 구하려면 두 번째 인자로 반복 횟수를 지정하세요:

```
Benchmark::dd(fn () => User::count(), iterations: 10); // 0.5 ms
```

실행 시간과 함께 콜백 결과도 얻고 싶으면 `value` 메서드를 사용하세요:

```
[$count, $duration] = Benchmark::value(fn () => User::count());
```

<a name="dates"></a>
### 날짜 (Dates)

Laravel은 강력한 날짜/시간 라이브러리 [Carbon](https://carbon.nesbot.com/docs/)을 포함합니다. 새 Carbon 인스턴스는 `now` 헬퍼 함수로 만들 수 있습니다:

```php
$now = now();
```

또는 `Illuminate\Support\Carbon` 클래스를 직접 사용할 수 있습니다:

```php
use Illuminate\Support\Carbon;

$now = Carbon::now();
```

자세한 내용은 공식 [Carbon 문서](https://carbon.nesbot.com/docs/)를 참조하세요.

<a name="deferred-functions"></a>
### 지연 함수 (Deferred Functions)

> [!WARNING]
> 지연 함수는 현재 베타 단계로 커뮤니티 피드백을 수집 중입니다.

Laravel의 [대기열 작업](/docs/11.x/queues)은 백그라운드에서 작업을 처리하지만, 간단한 작업을 대기열 없이 HTTP 응답 후 지연 실행하고 싶을 때도 있습니다.

지연 함수는 HTTP 응답 전송 후 클로저 실행을 지연시켜 애플리케이션 응답 속도를 유지합니다. 클로저는 `Illuminate\Support\defer` 함수로 전달하세요:

```php
use App\Services\Metrics;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use function Illuminate\Support\defer;

Route::post('/orders', function (Request $request) {
    // 주문 생성...

    defer(fn () => Metrics::reportOrder($order));

    return $order;
});
```

기본적으로 응답, Artisan 명령, 대기열 작업이 성공적으로 완료될 때만 지연 함수가 실행됩니다. `4xx` 또는 `5xx` 응답 시 실행되지 않습니다. 항상 실행하려면 `always` 메서드를 체인하세요:

```php
defer(fn () => Metrics::reportOrder($order))->always();
```

<a name="cancelling-deferred-functions"></a>
#### 지연 함수 취소

이름을 지정해 지연 함수를 취소할 수 있습니다:

```php
defer(fn () => Metrics::report(), 'reportMetrics');

defer()->forget('reportMetrics');
```

<a name="deferred-function-compatibility"></a>
#### 지연 함수 호환성

Laravel 10.x에서 11.x로 업그레이드한 후 `app/Http/Kernel.php` 파일이 아직 있다면, 커널 `$middleware` 배열 맨 앞에 `InvokeDeferredCallbacks` 미들웨어를 추가하세요:

```php
protected $middleware = [
    \Illuminate\Foundation\Http\Middleware\InvokeDeferredCallbacks::class, // [tl! add]
    \App\Http\Middleware\TrustProxies::class,
    // ...
];
```

<a name="disabling-deferred-functions-in-tests"></a>
#### 테스트에서 지연 함수 비활성화

테스트 중에 지연 함수를 비활성화하려면 다음 메서드를 호출하세요:

```php tab=Pest
test('without defer', function () {
    $this->withoutDefer();

    // ...
});
```

```php tab=PHPUnit
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_without_defer(): void
    {
        $this->withoutDefer();

        // ...
    }
}
```

테스트 클래스 전체에서 비활성화하려면 `setUp` 메서드에 호출을 추가하세요:

```php
<?php

namespace Tests;

use Illuminate\Foundation\Testing\TestCase as BaseTestCase;

abstract class TestCase extends BaseTestCase
{
    protected function setUp(): void// [tl! add:start]
    {
        parent::setUp();

        $this->withoutDefer();
    }// [tl! add:end]
}
```

<a name="lottery"></a>
### 복권(Lottery)

Laravel의 `Lottery` 클래스는 주어진 확률에 따라 콜백을 실행할 수 있어, 예를 들어 일정 비율의 요청에만 코드 실행을 제한할 때 유용합니다:

```
use Illuminate\Support\Lottery;

Lottery::odds(1, 20)
    ->winner(fn () => $user->won())
    ->loser(fn () => $user->lost())
    ->choose();
```

다른 Laravel 기능과 함께 사용도 가능합니다. 예를 들어 느린 쿼리 중 일부만 보고하려면:

```
use Carbon\CarbonInterval;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Lottery;

DB::whenQueryingForLongerThan(
    CarbonInterval::seconds(2),
    Lottery::odds(1, 100)->winner(fn () => report('Querying > 2 seconds.')),
);
```

<a name="testing-lotteries"></a>
#### 복권 테스트

복권 결과를 쉽게 테스트할 수 있는 메서드도 제공됩니다:

```
// 항상 당첨 처리...
Lottery::alwaysWin();

// 항상 당첨 실패...
Lottery::alwaysLose();

// 특정 시퀀스 당첨과 실패를 지정...
Lottery::fix([true, false]);

// 복권을 정상 동작 모드로 되돌림...
Lottery::determineResultsNormally();
```

<a name="pipeline"></a>
### 파이프라인 (Pipeline)

`Pipeline` 파사드는 연속적으로 입력을 여러 인보커블(클로저, 호출 가능 객체, 클래스)로 보내 각 단계에서 가공하도록 도와줍니다. 미들웨어와 비슷하게 동작합니다:

```php
use Closure;
use App\Models\User;
use Illuminate\Support\Facades\Pipeline;

$user = Pipeline::send($user)
    ->through([
        function (User $user, Closure $next) {
            // ...
    
            return $next($user);
        },
        function (User $user, Closure $next) {
            // ...
    
            return $next($user);
        },
    ])
    ->then(fn (User $user) => $user);
```

각 단계는 `$next` 콜러블로 다음 단계를 호출하며, 마지막 단계가 호출한 콜백(여기선 `then`)이 실행됩니다.

물론 클래스 이름을 지정하면 서비스 컨테이너로 인스턴스를 생성하고 의존성 주입도 받을 수 있습니다:

```php
$user = Pipeline::send($user)
    ->through([
        GenerateProfilePhoto::class,
        ActivateSubscription::class,
        SendWelcomeEmail::class,
    ])
    ->then(fn (User $user) => $user);
```

<a name="sleep"></a>
### Sleep

`Sleep` 클래스는 PHP 기본 `sleep`과 `usleep` 함수에 대한 가벼운 래퍼로, 테스트가 쉬우면서 시간 단위를 직관적으로 다룰 수 있습니다:

```
use Illuminate\Support\Sleep;

$waiting = true;

while ($waiting) {
    Sleep::for(1)->second();

    $waiting = /* ... */;
}
```

다양한 시간 단위 메서드를 제공합니다:

```
// 값 반환 후 대기...
$result = Sleep::for(1)->second()->then(fn () => 1 + 1);

// 조건이 참인 동안 대기...
Sleep::for(1)->second()->while(fn () => shouldKeepSleeping());

// 90초 대기...
Sleep::for(1.5)->minutes();

// 2초 대기...
Sleep::for(2)->seconds();

// 500밀리초 대기...
Sleep::for(500)->milliseconds();

// 5,000마이크로초 대기...
Sleep::for(5000)->microseconds();

// 특정 시간까지 대기...
Sleep::until(now()->addMinute());

// PHP 기본 sleep 별칭...
Sleep::sleep(2);

// PHP 기본 usleep 별칭...
Sleep::usleep(5000);
```

여러 단위를 결합할 때 `and` 메서드를 사용하세요:

```
Sleep::for(1)->second()->and(10)->milliseconds();
```

<a name="testing-sleep"></a>
#### Sleep 테스트

`Sleep` 또는 PHP 네이티브 sleep 함수를 활용한 코드는 테스트 시 실행이 멈추어 테스트 속도가 매우 느려집니다.

`Sleep::fake()`를 사용해 실제 대기를 무시할 수 있습니다:

```php tab=Pest
it('waits until ready', function () {
    Sleep::fake();

    // ...
});
```

```php tab=PHPUnit
public function test_it_waits_until_ready()
{
    Sleep::fake();

    // ...
}
```

가짜 대기 중에 예상 대기 시간에 대한 검증도 가능합니다:

```php tab=Pest
it('checks if ready three times', function () {
    Sleep::fake();

    // ...

    Sleep::assertSequence([
        Sleep::for(1)->second(),
        Sleep::for(2)->seconds(),
        Sleep::for(3)->seconds(),
    ]);
}
```

```php tab=PHPUnit
public function test_it_checks_if_ready_three_times()
{
    Sleep::fake();

    // ...

    Sleep::assertSequence([
        Sleep::for(1)->second(),
        Sleep::for(2)->seconds(),
        Sleep::for(3)->seconds(),
    ]);
}
```

기타 검증 메서드:

```
use Carbon\CarbonInterval as Duration;
use Illuminate\Support\Sleep;

// 대기 횟수 검증...
Sleep::assertSleptTimes(3);

// 대기 기간 검증...
Sleep::assertSlept(function (Duration $duration): bool {
    return /* ... */;
}, times: 1);

// 대기 불발 검증...
Sleep::assertNeverSlept();

// Sleep 호출했으나 실제 대기 없음 검증...
Sleep::assertInsomniac();
```

대기 시 특정 동작을 하게 하려면 `whenFakingSleep`에 콜백 전달:

```php
use Carbon\CarbonInterval as Duration;

$this->freezeTime();

Sleep::fake();

Sleep::whenFakingSleep(function (Duration $duration) {
    // 가짜 대기 시 Carbon 시간 이동으로 시간 동기화...
    $this->travel($duration->totalMilliseconds)->milliseconds();
});
```

`fake` 메서드는 `syncWithCarbon` 옵션으로 Carbon과 동기화할 수 있습니다:

```php
Sleep::fake(syncWithCarbon: true);

$start = now();

Sleep::for(1)->second();

$start->diffForHumans(); // 1 second ago
```

Laravel 내부적으로도 `Sleep` 클래스를 사용합니다. 예를 들어 [`retry`](#method-retry) 헬퍼가 그렇습니다.

<a name="timebox"></a>
### 타임박스(Timebox)

`Timebox` 클래스는 주어진 콜백이 항상 일정 시간(최소 마이크로초 단위) 동안 실행되도록 보장합니다. 실제 콜백이 빨리 끝나면 남은 시간동안 대기합니다. 주로 암호 연산이나 인증 확인같은 시간 변조 공격 방지에 유용합니다.

실행 시간이 지정한 한도를 넘으면 별도 조치 없이 콜백 실행 결과가 즉시 반환됩니다. 개발자가 충분히 긴 시간을 설정하는 것이 핵심입니다.

`call` 메서드는 콜백과 시간 제한(마이크로초)을 받아 콜백 실행과 지연을 처리합니다:

```php
use Illuminate\Support\Timebox;

(new Timebox)->call(function ($timebox) {
    // ...
}, microseconds: 10000);
```

콜백 내에서 예외가 발생하면, Timebox는 지연 시간을 존중하고 이후 예외를 다시 던집니다.