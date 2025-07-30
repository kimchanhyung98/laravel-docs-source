# Helpers

- [소개](#introduction)
- [사용 가능한 메서드](#available-methods)
- [기타 유틸리티](#other-utilities)
    - [벤치마킹](#benchmarking)
    - [날짜](#dates)
    - [복권 (Lottery)](#lottery)
    - [파이프라인](#pipeline)
    - [Sleep](#sleep)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 다양한 전역 "헬퍼" PHP 함수를 포함합니다. 이 함수들 중 많은 부분은 프레임워크 자체에서 사용하지만, 필요하다면 여러분의 애플리케이션에서도 자유롭게 사용할 수 있습니다.

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
[Arr::mapWithKeys](#method-array-map-with-keys)  
[Arr::only](#method-array-only)  
[Arr::pluck](#method-array-pluck)  
[Arr::prepend](#method-array-prepend)  
[Arr::prependKeysWith](#method-array-prependkeyswith)  
[Arr::pull](#method-array-pull)  
[Arr::query](#method-array-query)  
[Arr::random](#method-array-random)  
[Arr::set](#method-array-set)  
[Arr::shuffle](#method-array-shuffle)  
[Arr::sort](#method-array-sort)  
[Arr::sortDesc](#method-array-sort-desc)  
[Arr::sortRecursive](#method-array-sort-recursive)  
[Arr::sortRecursiveDesc](#method-array-sort-recursive-desc)  
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
[Number::fileSize](#method-number-file-size)  
[Number::forHumans](#method-number-for-humans)  
[Number::format](#method-number-format)  
[Number::ordinal](#method-number-ordinal)  
[Number::percentage](#method-number-percentage)  
[Number::spell](#method-number-spell)  
[Number::useLocale](#method-number-use-locale)  
[Number::withLocale](#method-number-with-locale)

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
### URL

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
[logger](#method-logger)  
[method_field](#method-method-field)  
[now](#method-now)  
[old](#method-old)  
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

</div>

<a name="arrays"></a>
## 배열과 객체 (Arrays & Objects)

<a name="method-array-accessible"></a>
#### `Arr::accessible()`

`Arr::accessible` 메서드는 주어진 값이 배열 접근 가능한지 여부를 검사합니다:

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

`Arr::add` 메서드는 배열에 주어진 키가 없거나 `null`일 경우 키와 값을 추가합니다:

```
use Illuminate\Support\Arr;

$array = Arr::add(['name' => 'Desk'], 'price', 100);

// ['name' => 'Desk', 'price' => 100]

$array = Arr::add(['name' => 'Desk', 'price' => null], 'price', 100);

// ['name' => 'Desk', 'price' => 100]
```

<a name="method-array-collapse"></a>
#### `Arr::collapse()`

`Arr::collapse` 메서드는 배열 안에 여러 배열이 있을 때, 이를 하나의 배열로 합칩니다:

```
use Illuminate\Support\Arr;

$array = Arr::collapse([[1, 2, 3], [4, 5, 6], [7, 8, 9]]);

// [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

<a name="method-array-crossjoin"></a>
#### `Arr::crossJoin()`

`Arr::crossJoin` 메서드는 주어진 배열들의 카르테시안 곱(Cartesian product)을 반환합니다. 모든 조합의 가능한 순열을 생성합니다:

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

`Arr::divide` 메서드는 주어진 배열에서 키들만 모은 배열과 값들만 모은 배열 두 개를 반환합니다:

```
use Illuminate\Support\Arr;

[$keys, $values] = Arr::divide(['name' => 'Desk']);

// $keys: ['name']

// $values: ['Desk']
```

<a name="method-array-dot"></a>
#### `Arr::dot()`

`Arr::dot` 메서드는 다차원 배열을 점(dot) 표기법을 사용하는 1차원 배열로 평탄화합니다:

```
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

$flattened = Arr::dot($array);

// ['products.desk.price' => 100]
```

<a name="method-array-except"></a>
#### `Arr::except()`

`Arr::except` 메서드는 주어진 키/값 쌍을 배열에서 제거합니다:

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

`Arr::first` 메서드는 주어진 진리 검사를 통과하는 배열의 첫 번째 요소를 반환합니다:

```
use Illuminate\Support\Arr;

$array = [100, 200, 300];

$first = Arr::first($array, function (int $value, int $key) {
    return $value >= 150;
});

// 200
```

세 번째 인자로 기본 값을 전달할 수도 있습니다. 진리 검사를 통과하는 값이 없으면 이 값이 반환됩니다:

```
use Illuminate\Support\Arr;

$first = Arr::first($array, $callback, $default);
```

<a name="method-array-flatten"></a>
#### `Arr::flatten()`

`Arr::flatten` 메서드는 다차원 배열을 1차원 배열로 평평하게 만듭니다:

```
use Illuminate\Support\Arr;

$array = ['name' => 'Joe', 'languages' => ['PHP', 'Ruby']];

$flattened = Arr::flatten($array);

// ['Joe', 'PHP', 'Ruby']
```

<a name="method-array-forget"></a>
#### `Arr::forget()`

`Arr::forget` 메서드는 점(dot) 표기법을 사용해 깊이 중첩된 배열에서 주어진 키/값 쌍을 제거합니다:

```
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

Arr::forget($array, 'products.desk');

// ['products' => []]
```

<a name="method-array-get"></a>
#### `Arr::get()`

`Arr::get` 메서드는 점(dot) 표기법을 사용해 깊이 중첩된 배열에서 값을 가져옵니다:

```
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

$price = Arr::get($array, 'products.desk.price');

// 100
```

세 번째 인자로 기본값을 전달하면, 키가 없을 경우 기본값이 반환됩니다:

```
use Illuminate\Support\Arr;

$discount = Arr::get($array, 'products.desk.discount', 0);

// 0
```

<a name="method-array-has"></a>
#### `Arr::has()`

`Arr::has` 메서드는 점(dot) 표기법으로 배열 안에 특정 요소나 복수 요소가 존재하는지 확인합니다:

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

`Arr::hasAny` 메서드는 점(dot) 표기법을 사용하여 주어진 집합 중 어느 하나라도 배열에 존재하는지 확인합니다:

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

`Arr::isAssoc` 메서드는 주어진 배열이 연관 배열인지 확인해 `true`를 반환합니다. 배열의 키가 0부터 시작하는 연속적 숫자가 아닐 경우 "연관 배열"로 간주합니다:

```
use Illuminate\Support\Arr;

$isAssoc = Arr::isAssoc(['product' => ['name' => 'Desk', 'price' => 100]]);

// true

$isAssoc = Arr::isAssoc([1, 2, 3]);

// false
```

<a name="method-array-islist"></a>
#### `Arr::isList()`

`Arr::isList` 메서드는 키가 0부터 시작하는 연속된 정수인 배열에 대해 `true`를 반환합니다:

```
use Illuminate\Support\Arr;

$isList = Arr::isList(['foo', 'bar', 'baz']);

// true

$isList = Arr::isList(['product' => ['name' => 'Desk', 'price' => 100]]);

// false
```

<a name="method-array-join"></a>
#### `Arr::join()`

`Arr::join` 메서드는 배열 요소들을 문자열로 이어 붙입니다. 두 번째 인자로 마지막 요소를 이어 붙일 때 사용할 문자열을 지정할 수 있습니다:

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

`Arr::keyBy` 메서드는 주어진 배열을 특정 키를 기준으로 새로운 배열의 키로 사용합니다. 만약 키가 중복된다면 마지막 요소가 덮어씁니다:

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

`Arr::last` 메서드는 주어진 진리 검사 조건을 만족하는 배열의 마지막 요소를 반환합니다:

```
use Illuminate\Support\Arr;

$array = [100, 200, 300, 110];

$last = Arr::last($array, function (int $value, int $key) {
    return $value >= 150;
});

// 300
```

기본 값은 세 번째 인자로 전달할 수 있으며, 조건에 맞는 요소가 없으면 이 값이 반환됩니다:

```
use Illuminate\Support\Arr;

$last = Arr::last($array, $callback, $default);
```

<a name="method-array-map"></a>
#### `Arr::map()`

`Arr::map` 메서드는 배열 내부를 순회하며 각 값과 키를 콜백에 전달하고, 콜백이 반환한 값으로 요소를 교체합니다:

```
use Illuminate\Support\Arr;

$array = ['first' => 'james', 'last' => 'kirk'];

$mapped = Arr::map($array, function (string $value, string $key) {
    return ucfirst($value);
});

// ['first' => 'James', 'last' => 'Kirk']
```

<a name="method-array-map-with-keys"></a>
#### `Arr::mapWithKeys()`

`Arr::mapWithKeys` 메서드는 배열 내부를 순회하며 각 값을 콜백으로 전달합니다. 콜백은 반드시 한 쌍의 키와 값을 가진 연관 배열을 반환해야 합니다:

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

`Arr::only` 메서드는 주어진 배열에서 지정한 키/값 쌍만 반환합니다:

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

세 번째 인자를 지정하면 결과 배열의 키로 사용할 값을 지정할 수도 있습니다:

```
use Illuminate\Support\Arr;

$names = Arr::pluck($array, 'developer.name', 'developer.id');

// [1 => 'Taylor', 2 => 'Abigail']
```

<a name="method-array-prepend"></a>
#### `Arr::prepend()`

`Arr::prepend` 메서드는 배열의 시작 부분에 항목을 추가합니다:

```
use Illuminate\Support\Arr;

$array = ['one', 'two', 'three', 'four'];

$array = Arr::prepend($array, 'zero');

// ['zero', 'one', 'two', 'three', 'four']
```

필요시, 지정한 키를 값에 사용하도록 설정할 수도 있습니다:

```
use Illuminate\Support\Arr;

$array = ['price' => 100];

$array = Arr::prepend($array, 'Desk', 'name');

// ['name' => 'Desk', 'price' => 100]
```

<a name="method-array-prependkeyswith"></a>
#### `Arr::prependKeysWith()`

`Arr::prependKeysWith` 메서드는 연관 배열의 모든 키 이름에 접두어를 추가합니다:

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

`Arr::pull` 메서드는 배열에서 주어진 키/값 쌍을 반환하고 배열에서 제거합니다:

```
use Illuminate\Support\Arr;

$array = ['name' => 'Desk', 'price' => 100];

$name = Arr::pull($array, 'name');

// $name: Desk

// $array: ['price' => 100]
```

기본값은 세 번째 인자로 전달할 수 있으며, 키가 없을 때 반환됩니다:

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

`Arr::random` 메서드는 배열에서 무작위 값을 반환합니다:

```
use Illuminate\Support\Arr;

$array = [1, 2, 3, 4, 5];

$random = Arr::random($array);

// 4 - (무작위 선택)
```

두 번째 인수로 반환할 항목 개수를 지정할 수 있습니다. 이 경우 반환값은 항상 배열입니다:

```
use Illuminate\Support\Arr;

$items = Arr::random($array, 2);

// [2, 5] - (무작위 선택)
```

<a name="method-array-set"></a>
#### `Arr::set()`

`Arr::set` 메서드는 점(dot) 표기법을 사용해 깊이 중첩된 배열 안에 값을 설정합니다:

```
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

Arr::set($array, 'products.desk.price', 200);

// ['products' => ['desk' => ['price' => 200]]]
```

<a name="method-array-shuffle"></a>
#### `Arr::shuffle()`

`Arr::shuffle` 메서드는 배열 내 요소의 순서를 무작위로 섞습니다:

```
use Illuminate\Support\Arr;

$array = Arr::shuffle([1, 2, 3, 4, 5]);

// [3, 2, 5, 1, 4] - (랜덤 생성)
```

<a name="method-array-sort"></a>
#### `Arr::sort()`

`Arr::sort` 메서드는 값 기준으로 배열을 정렬합니다:

```
use Illuminate\Support\Arr;

$array = ['Desk', 'Table', 'Chair'];

$sorted = Arr::sort($array);

// ['Chair', 'Desk', 'Table']
```

클로저를 이용해 정렬 기준 결과로도 배열 정렬이 가능합니다:

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

`Arr::sortDesc` 메서드는 값 기준 내림차순으로 배열을 정렬합니다:

```
use Illuminate\Support\Arr;

$array = ['Desk', 'Table', 'Chair'];

$sorted = Arr::sortDesc($array);

// ['Table', 'Desk', 'Chair']
```

클로저를 써서 정렬 기준 결과에 따라 내림차순 정렬도 가능합니다:

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

`Arr::sortRecursive` 메서드는 재귀적으로 배열을 정렬합니다. 숫자 인덱스 하위 배열은 `sort` 함수로, 연관 하위 배열은 `ksort` 함수로 정렬합니다:

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

내림차순 정렬이 필요하면 `Arr::sortRecursiveDesc`를 사용하세요:

```
$sorted = Arr::sortRecursiveDesc($array);
```

<a name="method-array-take"></a>
#### `Arr::take()`

`Arr::take` 메서드는 지정한 개수만큼 요소를 반환하는 새 배열을 만듭니다:

```
use Illuminate\Support\Arr;

$array = [0, 1, 2, 3, 4, 5];

$chunk = Arr::take($array, 3);

// [0, 1, 2]
```

음수 인수를 넣으면 배열 뒤에서부터 요소를 가져옵니다:

```
$array = [0, 1, 2, 3, 4, 5];

$chunk = Arr::take($array, -2);

// [4, 5]
```

<a name="method-array-to-css-classes"></a>
#### `Arr::toCssClasses()`

`Arr::toCssClasses` 메서드는 조건부로 CSS 클래스 문자열을 만듭니다. 배열의 키는 CSS 클래스 이름이고 값은 부울이며, 키가 숫자일 경우 무조건 포함됩니다:

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

`Arr::toCssStyles` 메서드는 조건부로 CSS 스타일 문자열을 만듭니다. 배열의 키는 스타일이고 값을 부울로, 키가 숫자일 경우 무조건 포함됩니다:

```php
use Illuminate\Support\Arr;

$hasColor = true;

$array = ['background-color: blue', 'color: blue' => $hasColor];

$classes = Arr::toCssStyles($array);

/*
    'background-color: blue; color: blue;'
*/
```

이 메서드는 [Blade 컴포넌트의 속성 가방과 클래스 통합](https://laravel.com/docs/10.x/blade#conditionally-merge-classes) 및 `@class` [Blade 디렉티브](https://laravel.com/docs/10.x/blade#conditional-classes)의 기능을 지원합니다.

<a name="method-array-undot"></a>
#### `Arr::undot()`

`Arr::undot` 메서드는 점(dot) 표기법을 사용한 1차원 배열을 다차원 배열로 확장합니다:

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

`Arr::where` 메서드는 주어진 클로저로 배열을 필터링합니다:

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

`Arr::whereNotNull` 메서드는 배열 내 모든 `null` 값을 제거합니다:

```
use Illuminate\Support\Arr;

$array = [0, null];

$filtered = Arr::whereNotNull($array);

// [0 => 0]
```

<a name="method-array-wrap"></a>
#### `Arr::wrap()`

`Arr::wrap` 메서드는 주어진 값을 배열로 감쌉니다. 이미 배열인 경우 그대로 반환합니다:

```
use Illuminate\Support\Arr;

$string = 'Laravel';

$array = Arr::wrap($string);

// ['Laravel']
```

`null`이면 빈 배열을 반환합니다:

```
use Illuminate\Support\Arr;

$array = Arr::wrap(null);

// []
```

<a name="method-data-fill"></a>
#### `data_fill()`

`data_fill` 함수는 점(dot) 표기법을 사용해 중첩된 배열이나 객체 안에 값이 없을 경우 값을 설정합니다:

```
$data = ['products' => ['desk' => ['price' => 100]]];

data_fill($data, 'products.desk.price', 200);

// ['products' => ['desk' => ['price' => 100]]]

data_fill($data, 'products.desk.discount', 10);

// ['products' => ['desk' => ['price' => 100, 'discount' => 10]]]
```

이 함수는 와일드카드(*)를 허용하여 대상들을 모두 채울 수 있습니다:

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

`data_get` 함수는 점(dot) 표기법을 사용하여 중첩 배열이나 객체에서 값을 가져옵니다:

```
$data = ['products' => ['desk' => ['price' => 100]]];

$price = data_get($data, 'products.desk.price');

// 100
```

기본값도 지정할 수 있어, 키가 없으면 기본값을 반환합니다:

```
$discount = data_get($data, 'products.desk.discount', 0);

// 0
```

또한 와일드카드(*)를 이용해 배열이나 객체의 모든 키를 참조할 수도 있습니다:

```
$data = [
    'product-one' => ['name' => 'Desk 1', 'price' => 100],
    'product-two' => ['name' => 'Desk 2', 'price' => 150],
];

data_get($data, '*.name');

// ['Desk 1', 'Desk 2'];
```

<a name="method-data-set"></a>
#### `data_set()`

`data_set` 함수는 점(dot) 표기법을 사용해 중첩 배열이나 객체 안에 값을 설정합니다:

```
$data = ['products' => ['desk' => ['price' => 100]]];

data_set($data, 'products.desk.price', 200);

// ['products' => ['desk' => ['price' => 200]]]
```

와일드카드(*)로 대상 전체에 값을 설정할 수 있습니다:

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

기본적으로 기존 값은 덮어씁니다. 값이 없을 때만 설정하려면 네 번째 인자로 `false`를 넣어주세요:

```
$data = ['products' => ['desk' => ['price' => 100]]];

data_set($data, 'products.desk.price', 200, overwrite: false);

// ['products' => ['desk' => ['price' => 100]]]
```

<a name="method-data-forget"></a>
#### `data_forget()`

`data_forget` 함수는 점(dot) 표기법을 사용해 중첩된 배열이나 객체에서 값을 제거합니다:

```
$data = ['products' => ['desk' => ['price' => 100]]];

data_forget($data, 'products.desk.price');

// ['products' => ['desk' => []]]
```

와일드카드(*)를 사용해 대상 전체에서 값을 제거할 수도 있습니다:

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

`Number::abbreviate` 메서드는 숫자를 사람이 읽기 쉬운 단위 축약형으로 변환합니다:

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

`Number::clamp` 메서드는 숫자를 최소값과 최대값 사이에 제한합니다. 숫자가 최소보다 작으면 최소를, 최대보다 크면 최대를 반환합니다:

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

`Number::currency` 메서드는 주어진 값을 통화 문자열로 반환합니다:

```
use Illuminate\Support\Number;

$currency = Number::currency(1000);

// $1,000

$currency = Number::currency(1000, in: 'EUR');

// €1,000

$currency = Number::currency(1000, in: 'EUR', locale: 'de');

// 1.000 €
```

<a name="method-number-file-size"></a>
#### `Number::fileSize()`

`Number::fileSize` 메서드는 바이트 단위를 사람이 읽기 쉬운 파일 크기로 변환하여 문자열로 반환합니다:

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

`Number::format` 메서드는 숫자를 로케일에 맞는 형식으로 포맷합니다:

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

<a name="method-number-percentage"></a>
#### `Number::percentage()`

`Number::percentage` 메서드는 숫자를 퍼센트 문자열로 반환합니다:

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

`Number::spell` 메서드는 숫자를 단어 문자열로 변환합니다:

```
use Illuminate\Support\Number;

$number = Number::spell(102);

// one hundred and two

$number = Number::spell(88, locale: 'fr');

// quatre-vingt-huit
```

`after` 인자는 지정한 값 이후부터 숫자를 문자열로 변환하도록 설정합니다:

```
$number = Number::spell(10, after: 10);

// 10

$number = Number::spell(11, after: 10);

// eleven
```

`until` 인자는 지정한 값 이전까지 숫자를 문자열로 변환합니다:

```
$number = Number::spell(5, until: 10);

// five

$number = Number::spell(10, until: 10);

// 10
```

<a name="method-number-use-locale"></a>
#### `Number::useLocale()`

`Number::useLocale` 메서드는 전역 기본 숫자 로케일을 설정하여 이후 `Number` 클래스 메서드 호출 시 해당 로케일을 적용하도록 합니다:

```
use Illuminate\Support\Number;

/**
 * 애플리케이션 서비스 부트스트랩
 */
public function boot(): void
{
    Number::useLocale('de');
}
```

<a name="method-number-with-locale"></a>
#### `Number::withLocale()`

`Number::withLocale` 메서드는 지정한 로케일 내에서 클로저를 실행하며, 완료 후 기존 로케일로 복원합니다:

```
use Illuminate\Support\Number;

$number = Number::withLocale('de', function () {
    return Number::format(1500);
});
```

<a name="paths"></a>
## 경로 (Paths)

<a name="method-app-path"></a>
#### `app_path()`

`app_path` 함수는 애플리케이션의 `app` 디렉터리 절대 경로를 반환합니다. 인수로 상대 경로를 주면 해당 경로까지 절대 경로를 생성합니다:

```
$path = app_path();

$path = app_path('Http/Controllers/Controller.php');
```

<a name="method-base-path"></a>
#### `base_path()`

`base_path` 함수는 애플리케이션 루트 디렉터리 절대 경로를 반환합니다. 인수로 상대 경로를 주면 루트 기준 절대 경로를 생성합니다:

```
$path = base_path();

$path = base_path('vendor/bin');
```

<a name="method-config-path"></a>
#### `config_path()`

`config_path` 함수는 애플리케이션의 `config` 디렉터리 절대 경로를 반환합니다. 상대 경로를 인수로 주면 해당 경로까지 절대 경로를 만듭니다:

```
$path = config_path();

$path = config_path('app.php');
```

<a name="method-database-path"></a>
#### `database_path()`

`database_path` 함수는 애플리케이션의 `database` 디렉터리 절대 경로를 반환합니다. 상대 경로를 인수로 주면 해당 파일까지 절대 경로를 생성합니다:

```
$path = database_path();

$path = database_path('factories/UserFactory.php');
```

<a name="method-lang-path"></a>
#### `lang_path()`

`lang_path` 함수는 애플리케이션의 `lang` 디렉터리 절대 경로를 반환합니다. 상대 경로를 주면 해당 위치까지 절대 경로를 생성합니다:

```
$path = lang_path();

$path = lang_path('en/messages.php');
```

> [!NOTE]  
> 기본적으로 Laravel 애플리케이션 스켈레톤에는 `lang` 디렉터리가 포함되어 있지 않습니다. 언어 파일을 직접 수정하려면 `lang:publish` Artisan 명령어로 게시할 수 있습니다.

<a name="method-mix"></a>
#### `mix()`

`mix` 함수는 [버전 관리된 Mix 파일](/docs/10.x/mix)에 대한 경로를 반환합니다:

```
$path = mix('css/app.css');
```

<a name="method-public-path"></a>
#### `public_path()`

`public_path` 함수는 애플리케이션의 `public` 디렉터리 절대 경로를 반환합니다. 상대 경로를 인수로 주면 해당 파일 경로까지 절대 경로를 생성합니다:

```
$path = public_path();

$path = public_path('css/app.css');
```

<a name="method-resource-path"></a>
#### `resource_path()`

`resource_path` 함수는 애플리케이션의 `resources` 디렉터리 절대 경로를 반환합니다. 인수로 상대 경로를 주면 해당 위치까지 절대 경로를 생성합니다:

```
$path = resource_path();

$path = resource_path('sass/app.scss');
```

<a name="method-storage-path"></a>
#### `storage_path()`

`storage_path` 함수는 애플리케이션의 `storage` 디렉터리 절대 경로를 반환합니다. 인수로 상대 경로를 넣으면 해당 파일까지 절대 경로를 생성합니다:

```
$path = storage_path();

$path = storage_path('app/file.txt');
```

<a name="urls"></a>
## URL

<a name="method-action"></a>
#### `action()`

`action` 함수는 주어진 컨트롤러 액션에 대한 URL을 생성합니다:

```
use App\Http\Controllers\HomeController;

$url = action([HomeController::class, 'index']);
```

라우트 파라미터가 필요하면 두 번째 인자로 전달할 수 있습니다:

```
$url = action([UserController::class, 'profile'], ['id' => 1]);
```

<a name="method-asset"></a>
#### `asset()`

`asset` 함수는 현재 요청 스킴(HTTP 또는 HTTPS)을 사용해 자산(asset)의 URL을 생성합니다:

```
$url = asset('img/photo.jpg');
```

`.env` 파일의 `ASSET_URL` 변수로 자산 URL 호스트를 설정할 수 있습니다. 예를 들어 외부 CDN을 사용할 때 유용합니다:

```
// ASSET_URL=http://example.com/assets

$url = asset('img/photo.jpg'); // http://example.com/assets/img/photo.jpg
```

<a name="method-route"></a>
#### `route()`

`route` 함수는 [이름 있는 라우트](/docs/10.x/routing#named-routes)에 대한 URL을 생성합니다:

```
$url = route('route.name');
```

라우트 파라미터가 있으면 두 번째 인자로 전달합니다:

```
$url = route('route.name', ['id' => 1]);
```

기본적으로 절대 URL을 생성하며, 상대 URL을 원하면 세 번째 인자로 `false`를 전달하세요:

```
$url = route('route.name', ['id' => 1], false);
```

<a name="method-secure-asset"></a>
#### `secure_asset()`

`secure_asset` 함수는 HTTPS 프로토콜을 사용하는 자산 URL을 생성합니다:

```
$url = secure_asset('img/photo.jpg');
```

<a name="method-secure-url"></a>
#### `secure_url()`

`secure_url` 함수는 HTTPS 프로토콜을 사용하는 완전한 URL을 생성하며, 추가 URL 세그먼트를 두 번째 인자로 전달할 수 있습니다:

```
$url = secure_url('user/profile');

$url = secure_url('user/profile', [1]);
```

<a name="method-to-route"></a>
#### `to_route()`

`to_route` 함수는 주어진 [이름 있는 라우트](/docs/10.x/routing#named-routes)로 리다이렉트 HTTP 응답을 생성합니다:

```
return to_route('users.show', ['user' => 1]);
```

상태 코드나 헤더 등도 세 번째 및 네 번째 인자로 전달할 수 있습니다:

```
return to_route('users.show', ['user' => 1], 302, ['X-Framework' => 'Laravel']);
```

<a name="method-url"></a>
#### `url()`

`url` 함수는 주어진 경로에 대한 완전한 URL을 생성합니다:

```
$url = url('user/profile');

$url = url('user/profile', [1]);
```

경로가 없으면 `Illuminate\Routing\UrlGenerator` 인스턴스를 반환합니다:

```
$current = url()->current();

$full = url()->full();

$previous = url()->previous();
```

<a name="miscellaneous"></a>
## 기타 (Miscellaneous)

<a name="method-abort"></a>
#### `abort()`

`abort` 함수는 [HTTP 예외](/docs/10.x/errors#http-exceptions)를 발생시켜, [예외 핸들러](/docs/10.x/errors#the-exception-handler)가 이를 렌더링하도록 합니다:

```
abort(403);
```

예외 메시지와 HTTP 응답 헤더를 추가로 지정할 수도 있습니다:

```
abort(403, 'Unauthorized.', $headers);
```

<a name="method-abort-if"></a>
#### `abort_if()`

`abort_if` 함수는 표현식이 `true`로 평가되면 HTTP 예외를 발생시킵니다:

```
abort_if(! Auth::user()->isAdmin(), 403);
```

`abort` 함수와 마찬가지로 메시지와 응답 헤더도 지정할 수 있습니다.

<a name="method-abort-unless"></a>
#### `abort_unless()`

`abort_unless` 함수는 표현식이 `false`일 경우 HTTP 예외를 발생시킵니다:

```
abort_unless(Auth::user()->isAdmin(), 403);
```

메시지와 응답 헤더도 지정할 수 있습니다.

<a name="method-app"></a>
#### `app()`

`app` 함수는 [서비스 컨테이너](/docs/10.x/container) 인스턴스를 반환합니다:

```
$container = app();
```

클래스 또는 인터페이스명을 전달하면 컨테이너에서 인스턴스를 가져옵니다:

```
$api = app('HelpSpot\API');
```

<a name="method-auth"></a>
#### `auth()`

`auth` 함수는 [인증자](/docs/10.x/authentication) 인스턴스를 반환하며, `Auth` 파사드 대체로 사용할 수 있습니다:

```
$user = auth()->user();
```

가드 인스턴스를 지정할 수도 있습니다:

```
$user = auth('admin')->user();
```

<a name="method-back"></a>
#### `back()`

`back` 함수는 사용자의 이전 위치로 [리다이렉트 HTTP 응답](/docs/10.x/responses#redirects)을 생성합니다:

```
return back($status = 302, $headers = [], $fallback = '/');

return back();
```

<a name="method-bcrypt"></a>
#### `bcrypt()`

`bcrypt` 함수는 Bcrypt 알고리즘으로 값을 [해싱](/docs/10.x/hashing)합니다. `Hash` 파사드 대신 사용할 수 있습니다:

```
$password = bcrypt('my-secret-password');
```

<a name="method-blank"></a>
#### `blank()`

`blank` 함수는 값이 "빈 값"인지 판단합니다:

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

`blank`의 반대는 [`filled`](#method-filled)를 참고하세요.

<a name="method-broadcast"></a>
#### `broadcast()`

`broadcast` 함수는 주어진 [이벤트](/docs/10.x/events)를 리스너들에게 [브로드캐스트](/docs/10.x/broadcasting)합니다:

```
broadcast(new UserRegistered($user));

broadcast(new UserRegistered($user))->toOthers();
```

<a name="method-cache"></a>
#### `cache()`

`cache` 함수는 [캐시](/docs/10.x/cache)에서 값을 가져오거나, 없으면 기본 값을 반환합니다:

```
$value = cache('key');

$value = cache('key', 'default');
```

배열로 키/값 쌍을 전달하고, 유효 기간을 초 또는 `DateTime` 인스턴스로 지정해 캐시에 저장할 수 있습니다:

```
cache(['key' => 'value'], 300);

cache(['key' => 'value'], now()->addSeconds(10));
```

<a name="method-class-uses-recursive"></a>
#### `class_uses_recursive()`

`class_uses_recursive` 함수는 클래스가 사용하는 모든 트레이트를 반환합니다. 부모 클래스의 트레이트까지 포함됩니다:

```
$traits = class_uses_recursive(App\Models\User::class);
```

<a name="method-collect"></a>
#### `collect()`

`collect` 함수는 주어진 값으로 [컬렉션](/docs/10.x/collections) 인스턴스를 만듭니다:

```
$collection = collect(['taylor', 'abigail']);
```

<a name="method-config"></a>
#### `config()`

`config` 함수는 [설정](/docs/10.x/configuration) 값을 가져옵니다. 점(dot) 구문으로 파일명 및 옵션명을 조합해 접근합니다. 기본값도 지정할 수 있습니다:

```
$value = config('app.timezone');

$value = config('app.timezone', $default);
```

배열로 설정값을 전달해 요청 중 설정을 변경할 수도 있습니다. 단, 이는 현재 요청에 한정됩니다:

```
config(['app.debug' => true]);
```

<a name="method-cookie"></a>
#### `cookie()`

`cookie` 함수는 새 [쿠키](/docs/10.x/requests#cookies) 인스턴스를 만듭니다:

```
$cookie = cookie('name', 'value', $minutes);
```

<a name="method-csrf-field"></a>
#### `csrf_field()`

`csrf_field` 함수는 CSRF 토큰 값을 가진 HTML `hidden` 입력 필드를 생성합니다. 예: [Blade 문법](/docs/10.x/blade) 사용 시:

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

`decrypt` 함수는 주어진 값을 복호화합니다. `Crypt` 파사드 대체로 쓸 수 있습니다:

```
$password = decrypt($value);
```

<a name="method-dd"></a>
#### `dd()`

`dd` 함수는 주어진 변수를 덤프하고 스크립트 실행을 종료합니다:

```
dd($value);

dd($value1, $value2, $value3, ...);
```

실행을 중지하고 싶지 않으면 [`dump`](#method-dump) 함수를 사용하세요.

<a name="method-dispatch"></a>
#### `dispatch()`

`dispatch` 함수는 주어진 [잡](/docs/10.x/queues#creating-jobs)을 Laravel [잡 큐](/docs/10.x/queues)에 추가합니다:

```
dispatch(new App\Jobs\SendEmails);
```

<a name="method-dispatch-sync"></a>
#### `dispatch_sync()`

`dispatch_sync` 함수는 즉시 실행하기 위해 주어진 잡을 [동기](/docs/10.x/queues#synchronous-dispatching) 큐에 보냅니다:

```
dispatch_sync(new App\Jobs\SendEmails);
```

<a name="method-dump"></a>
#### `dump()`

`dump` 함수는 주어진 변수를 덤프합니다:

```
dump($value);

dump($value1, $value2, $value3, ...);
```

덤프 후 실행 중단을 원하면 [`dd`](#method-dd) 함수를 쓰세요.

<a name="method-encrypt"></a>
#### `encrypt()`

`encrypt` 함수는 주어진 값을 암호화합니다. `Crypt` 파사드 대신 사용할 수 있습니다:

```
$secret = encrypt('my-secret-value');
```

<a name="method-env"></a>
#### `env()`

`env` 함수는 [환경 변수](/docs/10.x/configuration#environment-configuration) 값을 가져오거나 기본값을 반환합니다:

```
$env = env('APP_ENV');

$env = env('APP_ENV', 'production');
```

> [!WARNING]  
> `config:cache` 명령어를 배포 중 실행하면, `env` 함수는 반드시 구성파일 내에서만 호출하세요. 설정이 캐시되면 `.env` 파일이 로드되지 않아 `env` 호출은 모두 `null`을 반환합니다.

<a name="method-event"></a>
#### `event()`

`event` 함수는 주어진 [이벤트](/docs/10.x/events)를 리스너들에게 디스패치합니다:

```
event(new UserRegistered($user));
```

<a name="method-fake"></a>
#### `fake()`

`fake` 함수는 컨테이너에서 [Faker](https://github.com/FakerPHP/Faker) 싱글톤을 해결합니다. 모델 팩토리, 데이터베이스 시딩, 테스트, 뷰 프로토타입에 유용합니다:

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

기본적으로 `fake` 함수는 `config/app.php`의 `app.faker_locale` 설정 옵션을 사용합니다. 로케일을 인수로 지정해 사용할 수도 있습니다. 각 로케일마다 별도의 싱글톤이 생성됩니다:

```
fake('nl_NL')->name()
```

<a name="method-filled"></a>
#### `filled()`

`filled` 함수는 값이 "빈 값"이 아닌지 확인합니다:

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

`filled`의 반대는 [`blank`](#method-blank) 함수입니다.

<a name="method-info"></a>
#### `info()`

`info` 함수는 애플리케이션의 [로그](/docs/10.x/logging)에 정보를 기록합니다:

```
info('Some helpful information!');
```

추가적으로 문맥(Contextual) 데이터를 배열로 넘길 수도 있습니다:

```
info('User login attempt failed.', ['id' => $user->id]);
```

<a name="method-logger"></a>
#### `logger()`

`logger` 함수는 [로그](/docs/10.x/logging)에 `debug` 레벨 메시지를 기록합니다:

```
logger('Debug message');
```

문맥 데이터를 배열로 넘길 수도 있습니다:

```
logger('User has logged in.', ['id' => $user->id]);
```

값이 없으면 [로거](/docs/10.x/errors#logging) 인스턴스를 반환합니다:

```
logger()->error('You are not allowed here.');
```

<a name="method-method-field"></a>
#### `method_field()`

`method_field` 함수는 폼의 HTTP 메서드를 속이는 `hidden` HTML 입력 필드를 생성합니다. 예: [Blade 문법](/docs/10.x/blade):

```
<form method="POST">
    {{ method_field('DELETE') }}
</form>
```

<a name="method-now"></a>
#### `now()`

`now` 함수는 현재 시각에 해당하는 `Illuminate\Support\Carbon` 인스턴스를 생성합니다:

```
$now = now();
```

<a name="method-old"></a>
#### `old()`

`old` 함수는 세션에 플래시된 이전 입력 값을 가져옵니다:

```
$value = old('value');

$value = old('value', 'default');
```

두 번째 인자에는 주로 Eloquent 모델의 속성을 넣을 수 있습니다. 이렇게 하면 첫 번째 인자를 자동으로 모델 속성명으로 간주합니다:

```
{{ old('name', $user->name) }}

// 다음과 동일

{{ old('name', $user) }}
```

<a name="method-optional"></a>
#### `optional()`

`optional` 함수는 아무 인수를 받으며, 값이 `null`일 때 속성 접근과 메서드 호출 결과를 `null`로 처리해 오류를 방지합니다:

```
return optional($user->address)->street;

{!! old('name', optional($user)->name) !!}
```

두 번째 인자로 클로저를 넣으면, 첫 번째 인자가 `null` 아닐 때 클로저가 호출됩니다:

```
return optional(User::find($id), function (User $user) {
    return $user->name;
});
```

<a name="method-policy"></a>
#### `policy()`

`policy` 메서드는 주어진 클래스에 대한 [정책](/docs/10.x/authorization#creating-policies) 인스턴스를 반환합니다:

```
$policy = policy(App\Models\User::class);
```

<a name="method-redirect"></a>
#### `redirect()`

`redirect` 함수는 [리다이렉트 HTTP 응답](/docs/10.x/responses#redirects)을 반환하거나, 인자가 없으면 리다이렉터 인스턴스를 반환합니다:

```
return redirect($to = null, $status = 302, $headers = [], $https = null);

return redirect('/home');

return redirect()->route('route.name');
```

<a name="method-report"></a>
#### `report()`

`report` 함수는 예외를 [예외 핸들러](/docs/10.x/errors#the-exception-handler)에 전달해 보고합니다:

```
report($e);
```

문자열을 넘기면 문자열을 메시지로 하는 예외를 생성해 보고합니다:

```
report('Something went wrong.');
```

<a name="method-report-if"></a>
#### `report_if()`

`report_if` 함수는 조건이 `true`일 때 예외를 보고합니다:

```
report_if($shouldReport, $e);

report_if($shouldReport, 'Something went wrong.');
```

<a name="method-report-unless"></a>
#### `report_unless()`

`report_unless` 함수는 조건이 `false`일 때 예외를 보고합니다:

```
report_unless($reportingDisabled, $e);

report_unless($reportingDisabled, 'Something went wrong.');
```

<a name="method-request"></a>
#### `request()`

`request` 함수는 현재 [요청](/docs/10.x/requests) 인스턴스를 반환하거나, 요청에서 입력 값을 가져옵니다:

```
$request = request();

$value = request('key', $default);
```

<a name="method-rescue"></a>
#### `rescue()`

`rescue` 함수는 클로저를 실행하며 실행 중 발생하는 예외를 잡아냅니다. 예외는 [예외 핸들러](/docs/10.x/errors#the-exception-handler)로 전달되며, 요청 처리는 계속 진행됩니다:

```
return rescue(function () {
    return $this->method();
});
```

두 번째 인자로 기본 값을 넣으면, 예외 발생 시 그 값을 반환합니다:

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

`report` 인자를 통해 예외 보고 여부를 결정하는 콜백도 지정 가능합니다:

```
return rescue(function () {
    return $this->method();
}, report: function (Throwable $throwable) {
    return $throwable instanceof InvalidArgumentException;
});
```

<a name="method-resolve"></a>
#### `resolve()`

`resolve` 함수는 클래스 또는 인터페이스명을 서비스 컨테이너에서 인스턴스로 변환합니다:

```
$api = resolve('HelpSpot\API');
```

<a name="method-response"></a>
#### `response()`

`response` 함수는 [응답](/docs/10.x/responses) 인스턴스를 생성하거나 응답 팩토리 인스턴스를 반환합니다:

```
return response('Hello World', 200, $headers);

return response()->json(['foo' => 'bar'], 200, $headers);
```

<a name="method-retry"></a>
#### `retry()`

`retry` 함수는 주어진 콜백을 최대 시도 횟수까지 재시도합니다. 예외가 발생하지 않으면 콜백의 반환값을 반환하며, 최대 횟수 초과 시 예외를 던집니다:

```
return retry(5, function () {
    // 5번 시도하며 실행 중 100ms 대기...
}, 100);
```

세 번째 인자로 복수 시도 간 대기 시간을 밀리초 단위로 계산하는 클로저를 넣을 수 있습니다:

```
use Exception;

return retry(5, function () {
    // ...
}, function (int $attempt, Exception $exception) {
    return $attempt * 100;
});
```

시도당 대기 시간을 배열로 지정할 수도 있습니다:

```
return retry([100, 200], function () {
    // 첫 번째는 100ms, 두 번째는 200ms 휴식...
});
```

재시도 조건을 제한하려면 네 번째 인자로 클로저를 넣을 수 있습니다:

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

`session` 함수는 [세션](/docs/10.x/session)에서 값을 가져오거나 설정합니다:

```
$value = session('key');
```

키/값 배열로 세션에 저장할 수도 있습니다:

```
session(['chairs' => 7, 'instruments' => 3]);
```

값 없이 호출하면 세션 스토어 인스턴스를 반환합니다:

```
$value = session()->get('key');

session()->put('key', $value);
```

<a name="method-tap"></a>
#### `tap()`

`tap` 함수는 두 인자를 받습니다. 임의의 `$value`와 클로저를 받으며, 클로저에 `$value`를 전달하고 최종적으로 `$value`를 반환합니다. 클로저 반환값은 무시됩니다:

```
$user = tap(User::first(), function (User $user) {
    $user->name = 'taylor';

    $user->save();
});
```

클로저 없이 호출하면 `$value`의 메서드를 호출할 수 있으며, 호출 결과 대신 `$value` 자체를 반환합니다:

```
$user = tap($user)->update([
    'name' => $name,
    'email' => $email,
]);
```

클래스에 `Illuminate\Support\Traits\Tappable` 트레이트를 추가하면, 해당 클래스 객체에서도 `tap` 메서드를 사용할 수 있습니다:

```
return $user->tap(function (User $user) {
    // ...
});
```

<a name="method-throw-if"></a>
#### `throw_if()`

`throw_if` 함수는 조건이 `true`일 때 지정된 예외를 던집니다:

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

`throw_unless` 함수는 조건이 `false`일 때 지정된 예외를 던집니다:

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

`today` 함수는 현재 날짜의 `Illuminate\Support\Carbon` 인스턴스를 생성합니다:

```
$today = today();
```

<a name="method-trait-uses-recursive"></a>
#### `trait_uses_recursive()`

`trait_uses_recursive` 함수는 트레이트가 사용하는 모든 트레이트를 반환합니다:

```
$traits = trait_uses_recursive(\Illuminate\Notifications\Notifiable::class);
```

<a name="method-transform"></a>
#### `transform()`

`transform` 함수는 값이 [빈 값이 아니라면](#method-blank) 인자로 받은 클로저를 실행하고, 클로저 반환값을 반환합니다:

```
$callback = function (int $value) {
    return $value * 2;
};

$result = transform(5, $callback);

// 10
```

빈 값이면 세 번째 인자로 전달된 기본값 또는 클로저 결과를 반환합니다:

```
$result = transform(null, $callback, 'The value is blank');

// The value is blank
```

<a name="method-validator"></a>
#### `validator()`

`validator` 함수는 새로운 [검증기](/docs/10.x/validation) 인스턴스를 생성합니다. `Validator` 파사드 대신 사용할 수 있습니다:

```
$validator = validator($data, $rules, $messages);
```

<a name="method-value"></a>
#### `value()`

`value` 함수는 전달받은 값을 그대로 반환합니다. 단, 클로저라면 실행 후 반환값을 반환합니다:

```
$result = value(true);

// true

$result = value(function () {
    return false;
});

// false
```

추가 인자를 넘길 수도 있습니다. 첫 인자가 클로저면 추가 인자는 클로저 인자로 전달됩니다:

```
$result = value(function (string $name) {
    return $name;
}, 'Taylor');

// 'Taylor'
```

<a name="method-view"></a>
#### `view()`

`view` 함수는 [뷰](/docs/10.x/views) 인스턴스를 반환합니다:

```
return view('auth.login');
```

<a name="method-with"></a>
#### `with()`

`with` 함수는 전달받은 값을 반환합니다. 두 번째 인자가 클로저면 실행하고 그 결과값을 반환합니다:

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

<a name="other-utilities"></a>
## 기타 유틸리티 (Other Utilities)

<a name="benchmarking"></a>
### 벤치마킹 (Benchmarking)

애플리케이션의 성능을 빠르게 측정하고 싶을 때 `Benchmark` 클래스를 사용하는 것이 편리합니다. 콜백 실행에 걸린 밀리초를 측정합니다:

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

기본적으로 콜백은 한 번 실행되고, 결과 시간이 브라우저나 콘솔에 표시됩니다.

여러 번 실행해 평균 시간을 얻으려면 두 번째 인자에 반복 횟수를 지정하세요:

```
Benchmark::dd(fn () => User::count(), iterations: 10); // 0.5 ms
```

콜백의 반환값과 소요 시간을 같이 얻고 싶으면 `value` 메서드를 사용하세요. 반환값과 밀리초를 튜플로 반환합니다:

```
[$count, $duration] = Benchmark::value(fn () => User::count());
```

<a name="dates"></a>
### 날짜 (Dates)

Laravel은 강력한 날짜 및 시간 조작 라이브러리인 [Carbon](https://carbon.nesbot.com/docs/)을 포함합니다. 새로운 `Carbon` 인스턴스를 생성하려면 전역 `now` 함수를 호출하세요:

```php
$now = now();
```

또는 `Illuminate\Support\Carbon` 클래스를 직접 사용할 수도 있습니다:

```php
use Illuminate\Support\Carbon;

$now = Carbon::now();
```

Carbon과 기능에 대해 더 자세히 알기 위해서는 [공식 Carbon 문서](https://carbon.nesbot.com/docs/)를 참고하세요.

<a name="lottery"></a>
### 복권 (Lottery)

Laravel의 Lottery 클래스는 주어진 확률로 콜백을 실행할 수 있습니다. 예를 들어 전체 요청 중 일부만 코드를 실행하고 싶을 때 유용합니다:

```
use Illuminate\Support\Lottery;

Lottery::odds(1, 20)
    ->winner(fn () => $user->won())
    ->loser(fn () => $user->lost())
    ->choose();
```

다른 Laravel 기능과 조합해, 예를 들어 느린 쿼리를 일부만 예외 처리기로 보고할 수도 있습니다. Lottery 클래스는 콜러블이기 때문에 콜러블을 받는 메서드에 인자로 넘길 수 있습니다:

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

다음 메서드로 손쉽게 로또 동작을 테스트할 수 있습니다:

```
// 무조건 당첨
Lottery::alwaysWin();

// 무조건 꽝
Lottery::alwaysLose();

// 주기적으로 당첨/꽝, 이후 일반 동작
Lottery::fix([true, false]);

// 정상적인 확률로 복귀
Lottery::determineResultsNormally();
```

<a name="pipeline"></a>
### 파이프라인 (Pipeline)

Laravel의 `Pipeline` 파사드는 입력값을 여러 인보커블(invokable) 클래스, 클로저, 콜러블에 순차적으로 전달할 수 있게 해줍니다. 각 단계에서 입력값을 검사하거나 변경할 수 있습니다:

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

각 단계에는 `$next` 클로저가 주어지며 호출하면 다음 단계로 전진합니다. 미들웨어 구조와 유사합니다.

마지막 단계가 `$next`를 호출하면 `then` 메서드에 제공된 콜러블이 실행되고 일반적으로 입력을 그대로 반환합니다.

클로저 외에 인보커블 클래스를 넣을 수도 있습니다. 클래스명은 서비스 컨테이너에서 인스턴스화되어 의존성 주입을 지원합니다:

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

Laravel의 `Sleep` 클래스는 PHP의 원래 `sleep`과 `usleep` 함수의 경량 래퍼로, 더 나은 테스트 용이성과 개발 친화적인 API를 제공합니다:

```
use Illuminate\Support\Sleep;

$waiting = true;

while ($waiting) {
    Sleep::for(1)->second();

    $waiting = /* ... */;
}
```

`Sleep` 클래스는 다양한 시간 단위 메서드를 제공합니다:

```
// 90초 일시 중지...
Sleep::for(1.5)->minutes();

// 2초 일시 중지...
Sleep::for(2)->seconds();

// 500 밀리초 일시 중지...
Sleep::for(500)->milliseconds();

// 5,000 마이크로초 일시 중지...
Sleep::for(5000)->microseconds();

// 특정 시각까지 대기...
Sleep::until(now()->addMinute());

// PHP 원본 "sleep" 함수 별칭...
Sleep::sleep(2);

// PHP 원본 "usleep" 함수 별칭...
Sleep::usleep(5000);
```

여러 시간 단위를 쉽게 조합할 수 있는 `and` 메서드도 있습니다:

```
Sleep::for(1)->second()->and(10)->milliseconds();
```

<a name="testing-sleep"></a>
#### Sleep 테스트

`Sleep` 클래스나 PHP 네이티브 sleep 함수를 사용하는 코드는 테스트 중에 실행이 정지해서 테스트 속도가 느려집니다. 예:

```
$waiting = /* ... */;

$seconds = 1;

while ($waiting) {
    Sleep::for($seconds++)->seconds();

    $waiting = /* ... */;
}
```

이 코드는 테스트 시 최소 1초 이상 걸립니다.

다행히 `Sleep` 클래스는 "가짜"로 만들어 테스트를 빠르게 할 수 있습니다:

```
public function test_it_waits_until_ready()
{
    Sleep::fake();

    // ...
}
```

가짜일 때 실제 지연이 발생하지 않아 테스트가 빨라집니다.

`Sleep`가 호출된 기록을 검증하는 다양한 관련 어서션 메서드도 제공합니다:

```
public function test_it_checks_if_ready_four_times()
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

다음과 같은 어서션도 사용할 수 있습니다:

```
use Carbon\CarbonInterval as Duration;
use Illuminate\Support\Sleep;

// sleep 호출 횟수 검사...
Sleep::assertSleptTimes(3);

// sleep 지속시간 검사 (횟수 지정 가능)...
Sleep::assertSlept(function (Duration $duration): bool {
    return /* ... */;
}, times: 1);

// sleep 호출이 없었는지 검사...
Sleep::assertNeverSlept();

// sleep 호출은 있었지만 실제 대기 시간은 없었는지 검사...
Sleep::assertInsomniac();
```

가짜 sleep 발생 시 동작을 지정하려면 `whenFakingSleep` 메서드에 콜백을 넣을 수 있습니다. 예:

```php
use Carbon\CarbonInterval as Duration;

$this->freezeTime();

Sleep::fake();

Sleep::whenFakingSleep(function (Duration $duration) {
    // 가짜 sleep 시 시간 진행 처리...
    $this->travel($duration->totalMilliseconds)->milliseconds();
});
```

Laravel은 내부적으로 실행 일시 중지 시 `Sleep` 클래스를 사용합니다. 예를 들어 [`retry`](#method-retry) 헬퍼도 `Sleep`을 사용하여 테스트 용이성이 높아집니다.