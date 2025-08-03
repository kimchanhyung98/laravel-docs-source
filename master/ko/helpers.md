# 헬퍼 (Helpers)

- [소개](#introduction)
- [사용 가능한 메서드](#available-methods)
- [기타 유틸리티](#other-utilities)
    - [벤치마킹](#benchmarking)
    - [날짜](#dates)
    - [지연 함수](#deferred-functions)
    - [복권](#lottery)
    - [파이프라인](#pipeline)
    - [슬립](#sleep)
    - [타임박스](#timebox)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel에는 다양한 전역 "헬퍼" PHP 함수들이 포함되어 있습니다. 이 중 많은 함수는 프레임워크 자체에서 사용되지만, 편리하다고 생각되면 직접 작성하는 애플리케이션에서도 자유롭게 사용할 수 있습니다.

<a name="available-methods"></a>
## 사용 가능한 메서드 (Available Methods)

<a name="arrays-and-objects-method-list"></a>
### 배열 & 객체 (Arrays & Objects)

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
[Arr::partition](#method-array-partition)
[Arr::pluck](#method-array-pluck)
[Arr::prepend](#method-array-prepend)
[Arr::prependKeysWith](#method-array-prependkeyswith)
[Arr::pull](#method-array-pull)
[Arr::query](#method-array-query)
[Arr::random](#method-array-random)
[Arr::reject](#method-array-reject)
[Arr::select](#method-array-select)
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
## 배열 & 객체 (Arrays & Objects)

<a name="method-array-accessible"></a>
#### `Arr::accessible()`

`Arr::accessible` 메서드는 주어진 값이 배열 접근 가능한지 확인합니다:

```php
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

`Arr::add` 메서드는 주어진 키가 배열 안에 없거나 `null`인 경우에만 해당 키/값 쌍을 배열에 추가합니다:

```php
use Illuminate\Support\Arr;

$array = Arr::add(['name' => 'Desk'], 'price', 100);

// ['name' => 'Desk', 'price' => 100]

$array = Arr::add(['name' => 'Desk', 'price' => null], 'price', 100);

// ['name' => 'Desk', 'price' => 100]
```

<a name="method-array-collapse"></a>
#### `Arr::collapse()`

`Arr::collapse` 메서드는 여러 배열을 하나의 배열로 병합합니다:

```php
use Illuminate\Support\Arr;

$array = Arr::collapse([[1, 2, 3], [4, 5, 6], [7, 8, 9]]);

// [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

<a name="method-array-crossjoin"></a>
#### `Arr::crossJoin()`

`Arr::crossJoin` 메서드는 주어진 배열들의 카르테시안 곱(Cartesian product)을 만들어 모든 가능한 조합의 배열을 반환합니다:

```php
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

`Arr::divide` 메서드는 주어진 배열의 키 배열과 값 배열 두 개를 반환합니다:

```php
use Illuminate\Support\Arr;

[$keys, $values] = Arr::divide(['name' => 'Desk']);

// $keys: ['name']

// $values: ['Desk']
```

<a name="method-array-dot"></a>
#### `Arr::dot()`

`Arr::dot` 메서드는 다차원 배열을 "dot" 표기법이 적용된 단일 수준 배열로 평탄화(flatten)합니다:

```php
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

$flattened = Arr::dot($array);

// ['products.desk.price' => 100]
```

<a name="method-array-except"></a>
#### `Arr::except()`

`Arr::except` 메서드는 주어진 키/값 쌍을 배열에서 제거합니다:

```php
use Illuminate\Support\Arr;

$array = ['name' => 'Desk', 'price' => 100];

$filtered = Arr::except($array, ['price']);

// ['name' => 'Desk']
```

<a name="method-array-exists"></a>
#### `Arr::exists()`

`Arr::exists` 메서드는 주어진 키가 배열에 존재하는지 확인합니다:

```php
use Illuminate\Support\Arr;

$array = ['name' => 'John Doe', 'age' => 17];

$exists = Arr::exists($array, 'name');

// true

$exists = Arr::exists($array, 'salary');

// false
```

<a name="method-array-first"></a>
#### `Arr::first()`

`Arr::first` 메서드는 주어진 조건을 만족하는 배열의 첫 번째 요소를 반환합니다:

```php
use Illuminate\Support\Arr;

$array = [100, 200, 300];

$first = Arr::first($array, function (int $value, int $key) {
    return $value >= 150;
});

// 200
```

또한 세 번째 인자에 기본값을 전달할 수 있으며, 조건에 맞는 값이 없으면 이 기본값이 리턴됩니다:

```php
use Illuminate\Support\Arr;

$first = Arr::first($array, $callback, $default);
```

<a name="method-array-flatten"></a>
#### `Arr::flatten()`

`Arr::flatten` 메서드는 다차원 배열을 단일 수준 배열로 평탄화합니다:

```php
use Illuminate\Support\Arr;

$array = ['name' => 'Joe', 'languages' => ['PHP', 'Ruby']];

$flattened = Arr::flatten($array);

// ['Joe', 'PHP', 'Ruby']
```

<a name="method-array-forget"></a>
#### `Arr::forget()`

`Arr::forget` 메서드는 "dot" 표기법을 사용해 깊게 중첩된 배열에서 특정 키/값 쌍을 제거합니다:

```php
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

Arr::forget($array, 'products.desk');

// ['products' => []]
```

<a name="method-array-get"></a>
#### `Arr::get()`

`Arr::get` 메서드는 "dot" 표기법을 사용해 깊게 중첩된 배열에서 값을 가져옵니다:

```php
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

$price = Arr::get($array, 'products.desk.price');

// 100
```

이 메서드는 기본값도 지원하며, 지정한 키가 없을 때 기본값이 리턴됩니다:

```php
use Illuminate\Support\Arr;

$discount = Arr::get($array, 'products.desk.discount', 0);

// 0
```

<a name="method-array-has"></a>
#### `Arr::has()`

`Arr::has` 메서드는 "dot" 표기법을 사용해 배열 안에 특정 항목이 존재하는지 확인합니다:

```php
use Illuminate\Support\Arr;

$array = ['product' => ['name' => 'Desk', 'price' => 100]];

$contains = Arr::has($array, 'product.name');

// true

$contains = Arr::has($array, ['product.price', 'product.discount']);

// false
```

<a name="method-array-hasany"></a>
#### `Arr::hasAny()`

`Arr::hasAny` 메서드는 "dot" 표기법을 사용해 배열에 주어진 항목 중 적어도 하나가 존재하는지 확인합니다:

```php
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

`Arr::isAssoc` 메서드는 배열이 연관 배열(Associative array)인지 아닌지 확인합니다. 연관 배열은 0부터 시작하는 연속적인 숫자 키가 없는 배열입니다:

```php
use Illuminate\Support\Arr;

$isAssoc = Arr::isAssoc(['product' => ['name' => 'Desk', 'price' => 100]]);

// true

$isAssoc = Arr::isAssoc([1, 2, 3]);

// false
```

<a name="method-array-islist"></a>
#### `Arr::isList()`

`Arr::isList` 메서드는 배열 키가 0부터 시작하는 연속적인 정수인지 확인합니다:

```php
use Illuminate\Support\Arr;

$isList = Arr::isList(['foo', 'bar', 'baz']);

// true

$isList = Arr::isList(['product' => ['name' => 'Desk', 'price' => 100]]);

// false
```

<a name="method-array-join"></a>
#### `Arr::join()`

`Arr::join` 메서드는 배열 요소들을 문자열로 결합합니다. 두 번째 인자로 마지막 요소에 사용할 구분자 문자열을 지정할 수도 있습니다:

```php
use Illuminate\Support\Arr;

$array = ['Tailwind', 'Alpine', 'Laravel', 'Livewire'];

$joined = Arr::join($array, ', ');

// Tailwind, Alpine, Laravel, Livewire

$joined = Arr::join($array, ', ', ' and ');

// Tailwind, Alpine, Laravel and Livewire
```

<a name="method-array-keyby"></a>
#### `Arr::keyBy()`

`Arr::keyBy` 메서드는 배열을 주어진 키로 인덱싱합니다. 만약 키가 중복되면 마지막 항목이 유지됩니다:

```php
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

`Arr::last` 메서드는 주어진 조건을 만족하는 배열의 마지막 요소를 반환합니다:

```php
use Illuminate\Support\Arr;

$array = [100, 200, 300, 110];

$last = Arr::last($array, function (int $value, int $key) {
    return $value >= 150;
});

// 300
```

조건에 만족하는 값이 없으면 기본값을 세 번째 인자로 전달할 수 있습니다:

```php
use Illuminate\Support\Arr;

$last = Arr::last($array, $callback, $default);
```

<a name="method-array-map"></a>
#### `Arr::map()`

`Arr::map` 메서드는 배열을 순회하며 각 값과 키를 콜백에 전달하고, 콜백의 반환값으로 배열의 값을 대체합니다:

```php
use Illuminate\Support\Arr;

$array = ['first' => 'james', 'last' => 'kirk'];

$mapped = Arr::map($array, function (string $value, string $key) {
    return ucfirst($value);
});

// ['first' => 'James', 'last' => 'Kirk']
```

<a name="method-array-map-spread"></a>
#### `Arr::mapSpread()`

`Arr::mapSpread` 메서드는 배열을 순회하며 중첩된 각 값들을 콜백에 인수로 넘겨줍니다. 콜백은 아이템을 수정해 반환할 수 있습니다:

```php
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

`Arr::mapWithKeys` 메서드는 배열을 순회하며 각 값을 콜백에 전달하고, 콜백은 하나의 키/값 쌍을 포함한 연관 배열을 반환해야 합니다:

```php
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

`Arr::only` 메서드는 주어진 배열에서 특정 키들만 포함한 부분 배열을 반환합니다:

```php
use Illuminate\Support\Arr;

$array = ['name' => 'Desk', 'price' => 100, 'orders' => 10];

$slice = Arr::only($array, ['name', 'price']);

// ['name' => 'Desk', 'price' => 100]
```

<a name="method-array-partition"></a>
#### `Arr::partition()`

`Arr::partition` 메서드는 PHP 배열 구조 분해와 결합해, 조건에 만족하는 항목과 그렇지 않은 항목들을 분리합니다:

```php
<?php

use Illuminate\Support\Arr;

$numbers = [1, 2, 3, 4, 5, 6];

[$underThree, $equalOrAboveThree] = Arr::partition($numbers, function (int $i) {
    return $i < 3;
});

dump($underThree);

// [1, 2]

dump($equalOrAboveThree);

// [3, 4, 5, 6]
```

<a name="method-array-pluck"></a>
#### `Arr::pluck()`

`Arr::pluck` 메서드는 배열에서 주어진 키에 해당하는 모든 값을 추출합니다:

```php
use Illuminate\Support\Arr;

$array = [
    ['developer' => ['id' => 1, 'name' => 'Taylor']],
    ['developer' => ['id' => 2, 'name' => 'Abigail']],
];

$names = Arr::pluck($array, 'developer.name');

// ['Taylor', 'Abigail']
```

결과 배열의 키를 어떻게 할지도 세 번째 인자로 지정할 수 있습니다:

```php
use Illuminate\Support\Arr;

$names = Arr::pluck($array, 'developer.name', 'developer.id');

// [1 => 'Taylor', 2 => 'Abigail']
```

<a name="method-array-prepend"></a>
#### `Arr::prepend()`

`Arr::prepend` 메서드는 배열 앞쪽에 아이템을 추가합니다:

```php
use Illuminate\Support\Arr;

$array = ['one', 'two', 'three', 'four'];

$array = Arr::prepend($array, 'zero');

// ['zero', 'one', 'two', 'three', 'four']
```

필요하면 값을 위한 키도 지정할 수 있습니다:

```php
use Illuminate\Support\Arr;

$array = ['price' => 100];

$array = Arr::prepend($array, 'Desk', 'name');

// ['name' => 'Desk', 'price' => 100]
```

<a name="method-array-prependkeyswith"></a>
#### `Arr::prependKeysWith()`

`Arr::prependKeysWith` 메서드는 연관 배열의 모든 키에 대해 지정한 접두사를 붙입니다:

```php
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

`Arr::pull` 메서드는 배열에서 키/값 쌍을 제거하면서 해당 값을 반환합니다:

```php
use Illuminate\Support\Arr;

$array = ['name' => 'Desk', 'price' => 100];

$name = Arr::pull($array, 'name');

// $name: Desk

// $array: ['price' => 100]
```

키가 없으면 반환할 기본값을 세 번째 인자로 전달할 수 있습니다:

```php
use Illuminate\Support\Arr;

$value = Arr::pull($array, $key, $default);
```

<a name="method-array-query"></a>
#### `Arr::query()`

`Arr::query` 메서드는 배열을 쿼리 문자열로 변환합니다:

```php
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

`Arr::random` 메서드는 배열에서 무작위로 한 개 또는 여러 개 값을 반환합니다:

```php
use Illuminate\Support\Arr;

$array = [1, 2, 3, 4, 5];

$random = Arr::random($array);

// 4 - (랜덤으로 추출됨)
```

두 번째 인자로 반환할 개수를 지정할 수 있으며, 이 경우 항상 배열이 반환됩니다:

```php
use Illuminate\Support\Arr;

$items = Arr::random($array, 2);

// [2, 5] - (랜덤으로 추출됨)
```

<a name="method-array-reject"></a>
#### `Arr::reject()`

`Arr::reject` 메서드는 주어진 콜백을 기준으로 배열에서 아이템을 제거합니다:

```php
use Illuminate\Support\Arr;

$array = [100, '200', 300, '400', 500];

$filtered = Arr::reject($array, function (string|int $value, int $key) {
    return is_string($value);
});

// [0 => 100, 2 => 300, 4 => 500]
```

<a name="method-array-select"></a>
#### `Arr::select()`

`Arr::select` 메서드는 배열에서 지정한 키들만 선택해 배열의 배열을 반환합니다:

```php
use Illuminate\Support\Arr;

$array = [
    ['id' => 1, 'name' => 'Desk', 'price' => 200],
    ['id' => 2, 'name' => 'Table', 'price' => 150],
    ['id' => 3, 'name' => 'Chair', 'price' => 300],
];

Arr::select($array, ['name', 'price']);

// [['name' => 'Desk', 'price' => 200], ['name' => 'Table', 'price' => 150], ['name' => 'Chair', 'price' => 300]]
```

<a name="method-array-set"></a>
#### `Arr::set()`

`Arr::set` 메서드는 "dot" 표기법을 사용해 깊게 중첩된 배열에 값을 설정합니다:

```php
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

Arr::set($array, 'products.desk.price', 200);

// ['products' => ['desk' => ['price' => 200]]]
```

<a name="method-array-shuffle"></a>
#### `Arr::shuffle()`

`Arr::shuffle` 메서드는 배열 요소를 무작위로 섞습니다:

```php
use Illuminate\Support\Arr;

$array = Arr::shuffle([1, 2, 3, 4, 5]);

// [3, 2, 5, 1, 4] - (랜덤 생성됨)
```

<a name="method-array-sort"></a>
#### `Arr::sort()`

`Arr::sort` 메서드는 배열 값을 기준으로 오름차순 정렬합니다:

```php
use Illuminate\Support\Arr;

$array = ['Desk', 'Table', 'Chair'];

$sorted = Arr::sort($array);

// ['Chair', 'Desk', 'Table']
```

콜백의 반환값을 기준으로 정렬할 수도 있습니다:

```php
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

`Arr::sortDesc` 메서드는 배열 값을 기준으로 내림차순 정렬합니다:

```php
use Illuminate\Support\Arr;

$array = ['Desk', 'Table', 'Chair'];

$sorted = Arr::sortDesc($array);

// ['Table', 'Desk', 'Chair']
```

콜백 결과를 기준으로 내림차순 정렬할 수도 있습니다:

```php
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

`Arr::sortRecursive` 메서드는 재귀적으로 배열을 정렬합니다. 숫자 인덱스 배열은 `sort`를, 연관 배열은 `ksort`를 적용합니다:

```php
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

내림차순 결과가 필요하면 `Arr::sortRecursiveDesc` 메서드를 사용하세요:

```php
$sorted = Arr::sortRecursiveDesc($array);
```

<a name="method-array-take"></a>
#### `Arr::take()`

`Arr::take` 메서드는 지정한 개수 만큼의 아이템을 가진 새 배열을 반환합니다:

```php
use Illuminate\Support\Arr;

$array = [0, 1, 2, 3, 4, 5];

$chunk = Arr::take($array, 3);

// [0, 1, 2]
```

음수를 전달하면 배열 끝에서부터 개수를 가져옵니다:

```php
$array = [0, 1, 2, 3, 4, 5];

$chunk = Arr::take($array, -2);

// [4, 5]
```

<a name="method-array-to-css-classes"></a>
#### `Arr::toCssClasses()`

`Arr::toCssClasses` 메서드는 조건부로 CSS 클래스 문자열을 조합합니다. 배열 키는 클래스 이름 혹은 클래스 목록이며, 값은 불리언 조건입니다. 숫자 키가 있으면 항상 포함됩니다:

```php
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

`Arr::toCssStyles` 메서드는 조건부로 CSS 스타일 문자열을 조합합니다. 동작 방식은 `toCssClasses`와 유사합니다:

```php
use Illuminate\Support\Arr;

$hasColor = true;

$array = ['background-color: blue', 'color: blue' => $hasColor];

$classes = Arr::toCssStyles($array);

/*
    'background-color: blue; color: blue;'
*/
```

이 메서드는 Laravel의 [Blade 컴포넌트 속성 가방 클래스 병합 기능](/docs/master/blade#conditionally-merge-classes)과 `@class` [Blade 지시어](/docs/master/blade#conditional-classes)에서 사용됩니다.

<a name="method-array-undot"></a>
#### `Arr::undot()`

`Arr::undot` 메서드는 "dot" 표기법을 사용한 단일 수준 배열을 다차원 배열로 확장합니다:

```php
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

`Arr::where` 메서드는 주어진 콜백을 사용해 배열을 필터링합니다:

```php
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

```php
use Illuminate\Support\Arr;

$array = [0, null];

$filtered = Arr::whereNotNull($array);

// [0 => 0]
```

<a name="method-array-wrap"></a>
#### `Arr::wrap()`

`Arr::wrap` 메서드는 주어진 값을 배열로 래핑합니다. 이미 배열이면 변경하지 않고 그대로 반환합니다:

```php
use Illuminate\Support\Arr;

$string = 'Laravel';

$array = Arr::wrap($string);

// ['Laravel']
```

값이 `null`이면 빈 배열을 반환합니다:

```php
use Illuminate\Support\Arr;

$array = Arr::wrap(null);

// []
```

<a name="method-data-fill"></a>
#### `data_fill()`

`data_fill` 함수는 "dot" 표기법으로 중첩 배열 또는 객체 내에서 누락된 값을 설정합니다:

```php
$data = ['products' => ['desk' => ['price' => 100]]];

data_fill($data, 'products.desk.price', 200);

// ['products' => ['desk' => ['price' => 100]]]

data_fill($data, 'products.desk.discount', 10);

// ['products' => ['desk' => ['price' => 100, 'discount' => 10]]]
```

와일드카드(*)도 지원하여 대상에 따라 값을 채웁니다:

```php
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

`data_get` 함수는 "dot" 표기법으로 중첩 배열이나 객체에서 값을 가져옵니다:

```php
$data = ['products' => ['desk' => ['price' => 100]]];

$price = data_get($data, 'products.desk.price');

// 100
```

기본값도 지정할 수 있으며, 값이 없으면 기본값을 반환합니다:

```php
$discount = data_get($data, 'products.desk.discount', 0);

// 0
```

와일드카드(*)를 사용해 배열 또는 객체 내 모든 키에 접근할 수 있습니다:

```php
$data = [
    'product-one' => ['name' => 'Desk 1', 'price' => 100],
    'product-two' => ['name' => 'Desk 2', 'price' => 150],
];

data_get($data, '*.name');

// ['Desk 1', 'Desk 2'];
```

`{first}`, `{last}` 자리 표시자를 사용해 배열의 첫 항목이나 마지막 항목을 가져올 수도 있습니다:

```php
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

`data_set` 함수는 "dot" 표기법을 사용해 중첩 배열 또는 객체 내에 값을 설정합니다:

```php
$data = ['products' => ['desk' => ['price' => 100]]];

data_set($data, 'products.desk.price', 200);

// ['products' => ['desk' => ['price' => 200]]]
```

와일드카드(*)로 대상 모두에 값을 설정할 수 있습니다:

```php
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

기존 값이 덮어쓰이지 않게 하려면 네 번째 인자를 `false`로 전달합니다:

```php
$data = ['products' => ['desk' => ['price' => 100]]];

data_set($data, 'products.desk.price', 200, overwrite: false);

// ['products' => ['desk' => ['price' => 100]]]
```

<a name="method-data-forget"></a>
#### `data_forget()`

`data_forget` 함수는 "dot" 표기법을 사용해 중첩 배열 또는 객체 내에서 값을 제거합니다:

```php
$data = ['products' => ['desk' => ['price' => 100]]];

data_forget($data, 'products.desk.price');

// ['products' => ['desk' => []]]
```

와일드카드(*)도 지원하여 대상에 따라 값을 제거합니다:

```php
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

```php
$array = [100, 200, 300];

$first = head($array);

// 100
```

<a name="method-last"></a>
#### `last()`

`last` 함수는 주어진 배열의 마지막 요소를 반환합니다:

```php
$array = [100, 200, 300];

$last = last($array);

// 300
```

<a name="numbers"></a>
## 숫자 (Numbers)

<a name="method-number-abbreviate"></a>
#### `Number::abbreviate()`

`Number::abbreviate` 메서드는 숫자를 사람이 읽기 좋은 축약형 단위와 함께 반환합니다:

```php
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

`Number::clamp` 메서드는 숫자가 지정된 범위 내에 있도록 보장합니다. 범위보다 작으면 최소값, 크면 최대값을 반환합니다:

```php
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

`Number::currency` 메서드는 숫자 값을 통화 형식 문자열로 반환합니다:

```php
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

`Number::defaultCurrency` 메서드는 `Number` 클래스에서 사용하는 기본 통화를 반환합니다:

```php
use Illuminate\Support\Number;

$currency = Number::defaultCurrency();

// USD
```

<a name="method-default-locale"></a>
#### `Number::defaultLocale()`

`Number::defaultLocale` 메서드는 `Number` 클래스에서 사용하는 기본 로케일을 반환합니다:

```php
use Illuminate\Support\Number;

$locale = Number::defaultLocale();

// en
```

<a name="method-number-file-size"></a>
#### `Number::fileSize()`

`Number::fileSize` 메서드는 바이트 단위의 파일 크기를 사람이 읽기 좋은 문자열로 반환합니다:

```php
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

`Number::forHumans` 메서드는 숫자를 사람이 읽기 쉬운 형식으로 반환합니다:

```php
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

`Number::format` 메서드는 숫자를 로케일별 문자열로 서식화합니다:

```php
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

`Number::ordinal` 메서드는 숫자의 서수(순서) 표현을 반환합니다:

```php
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

`Number::pairs` 메서드는 지정한 범위와 스텝 값을 기반으로 숫자 쌍(하위 범위) 배열을 생성합니다. 페이지네이션이나 작업 배치 등에서 범위를 작은 단위로 분할할 때 유용합니다. 반환값은 숫자 쌍 배열입니다:

```php
use Illuminate\Support\Number;

$result = Number::pairs(25, 10);

// [[1, 10], [11, 20], [21, 25]]

$result = Number::pairs(25, 10, offset: 0);

// [[0, 10], [10, 20], [20, 25]]
```

<a name="method-number-percentage"></a>
#### `Number::percentage()`

`Number::percentage` 메서드는 숫자 값을 백분율 문자열로 반환합니다:

```php
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

```php
use Illuminate\Support\Number;

$number = Number::spell(102);

// one hundred and two

$number = Number::spell(88, locale: 'fr');

// quatre-vingt-huit
```

`after` 인자는 해당 값 이후 모든 숫자에 대해 철자 출력하도록 지정합니다:

```php
$number = Number::spell(10, after: 10);

// 10

$number = Number::spell(11, after: 10);

// eleven
```

`until` 인자는 해당 값 이전의 숫자들에 대해 철자 출력하도록 지정합니다:

```php
$number = Number::spell(5, until: 10);

// five

$number = Number::spell(10, until: 10);

// 10
```

<a name="method-number-trim"></a>
#### `Number::trim()`

`Number::trim` 메서드는 소수점 아래 불필요한 0들을 제거합니다:

```php
use Illuminate\Support\Number;

$number = Number::trim(12.0);

// 12

$number = Number::trim(12.30);

// 12.3
```

<a name="method-number-use-locale"></a>
#### `Number::useLocale()`

`Number::useLocale` 메서드는 기본 숫자 로케일을 전역으로 설정하여, 이후 `Number` 클래스의 메서드 동작에 영향을 미칩니다:

```php
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

`Number::withLocale` 메서드는 지정한 로케일을 사용해 콜백을 실행하며, 콜백 실행 후 원래 로케일을 복원합니다:

```php
use Illuminate\Support\Number;

$number = Number::withLocale('de', function () {
    return Number::format(1500);
});
```

<a name="method-number-use-currency"></a>
#### `Number::useCurrency()`

`Number::useCurrency` 메서드는 기본 통화를 전역으로 설정하여, 이후 `Number` 클래스 메서드에서 통화 포맷에 영향을 미칩니다:

```php
use Illuminate\Support\Number;

/**
 * 애플리케이션 서비스 부트스트랩
 */
public function boot(): void
{
    Number::useCurrency('GBP');
}
```

<a name="method-number-with-currency"></a>
#### `Number::withCurrency()`

`Number::withCurrency` 메서드는 지정한 통화를 사용해 콜백을 실행하며, 콜백 실행 후 원래 통화를 복원합니다:

```php
use Illuminate\Support\Number;

$number = Number::withCurrency('GBP', function () {
    // ...
});
```

<a name="paths"></a>
## 경로 (Paths)

<a name="method-app-path"></a>
#### `app_path()`

`app_path` 함수는 애플리케이션의 `app` 디렉터리 절대 경로를 반환합니다. 인자로 경로를 전달하면, 애플리케이션 디렉터리를 기준으로 한 경로를 반환합니다:

```php
$path = app_path();

$path = app_path('Http/Controllers/Controller.php');
```

<a name="method-base-path"></a>
#### `base_path()`

`base_path` 함수는 애플리케이션 루트 디렉터리 절대 경로를 반환합니다. 인자 전달 시 루트 디렉터리 기준 경로를 반환합니다:

```php
$path = base_path();

$path = base_path('vendor/bin');
```

<a name="method-config-path"></a>
#### `config_path()`

`config_path` 함수는 애플리케이션의 `config` 디렉터리 절대 경로를 반환합니다. 인자 전달 시 설정 디렉터리 기준 경로를 반환합니다:

```php
$path = config_path();

$path = config_path('app.php');
```

<a name="method-database-path"></a>
#### `database_path()`

`database_path` 함수는 애플리케이션의 `database` 디렉터리 절대 경로를 반환합니다. 인자 전달 시 데이터베이스 디렉터리 기준 경로를 반환합니다:

```php
$path = database_path();

$path = database_path('factories/UserFactory.php');
```

<a name="method-lang-path"></a>
#### `lang_path()`

`lang_path` 함수는 애플리케이션의 `lang` 디렉터리 절대 경로를 반환합니다. 인자 전달 시 해당 디렉터리 기준 경로를 반환합니다:

```php
$path = lang_path();

$path = lang_path('en/messages.php');
```

> [!NOTE]
> 기본적으로 Laravel 애플리케이션 골격에는 `lang` 디렉터리가 포함되어 있지 않습니다. 언어 파일을 커스터마이즈하려면 `lang:publish` Artisan 명령어로 퍼블리싱하세요.

<a name="method-mix"></a>
#### `mix()`

`mix` 함수는 [버전 관리된 Mix 파일](/docs/master/mix) 경로를 반환합니다:

```php
$path = mix('css/app.css');
```

<a name="method-public-path"></a>
#### `public_path()`

`public_path` 함수는 애플리케이션의 `public` 디렉터리 절대 경로를 반환합니다. 인자 전달 시 해당 디렉터리 기준 경로를 반환합니다:

```php
$path = public_path();

$path = public_path('css/app.css');
```

<a name="method-resource-path"></a>
#### `resource_path()`

`resource_path` 함수는 애플리케이션의 `resources` 디렉터리 절대 경로를 반환합니다. 인자 전달 시 해당 디렉터리 기준 경로를 반환합니다:

```php
$path = resource_path();

$path = resource_path('sass/app.scss');
```

<a name="method-storage-path"></a>
#### `storage_path()`

`storage_path` 함수는 애플리케이션의 `storage` 디렉터리 절대 경로를 반환합니다. 인자 전달 시 해당 디렉터리 기준 경로를 반환합니다:

```php
$path = storage_path();

$path = storage_path('app/file.txt');
```

<a name="urls"></a>
## URL (URLs)

<a name="method-action"></a>
#### `action()`

`action` 함수는 지정한 컨트롤러 액션의 URL을 생성합니다:

```php
use App\Http\Controllers\HomeController;

$url = action([HomeController::class, 'index']);
```

라우트 매개변수를 메서드 두 번째 인자로 전달할 수 있습니다:

```php
$url = action([UserController::class, 'profile'], ['id' => 1]);
```

<a name="method-asset"></a>
#### `asset()`

`asset` 함수는 현재 요청의 스킴(HTTP/HTTPS)을 사용해 자산 URL을 생성합니다:

```php
$url = asset('img/photo.jpg');
```

`.env` 파일 `ASSET_URL` 변수로 자산 URL 호스트를 설정할 수 있습니다. S3, CDN 등 외부 호스트에 자산을 둘 때 유용합니다:

```php
// ASSET_URL=http://example.com/assets

$url = asset('img/photo.jpg'); // http://example.com/assets/img/photo.jpg
```

<a name="method-route"></a>
#### `route()`

`route` 함수는 지정한 [이름이 붙은 라우트](/docs/master/routing#named-routes)의 URL을 생성합니다:

```php
$url = route('route.name');
```

라운트에 매개변수가 있으면 두 번째 인자로 전달하세요:

```php
$url = route('route.name', ['id' => 1]);
```

기본적으로 절대 URL이 생성됩니다. 상대 URL이 필요하면, 세 번째 인자로 `false`를 전달하세요:

```php
$url = route('route.name', ['id' => 1], false);
```

<a name="method-secure-asset"></a>
#### `secure_asset()`

`secure_asset` 함수는 HTTPS를 사용해 자산 URL을 생성합니다:

```php
$url = secure_asset('img/photo.jpg');
```

<a name="method-secure-url"></a>
#### `secure_url()`

`secure_url` 함수는 지정한 경로에 대해 완전한 HTTPS URL을 생성합니다. 추가 경로 세그먼트를 두 번째 인자로 전달할 수 있습니다:

```php
$url = secure_url('user/profile');

$url = secure_url('user/profile', [1]);
```

<a name="method-to-route"></a>
#### `to_route()`

`to_route` 함수는 지정한 [이름이 붙은 라우트](/docs/master/routing#named-routes)로 리다이렉트 HTTP 응답을 생성합니다:

```php
return to_route('users.show', ['user' => 1]);
```

필요하면 HTTP 상태 코드와 추가 헤더도 세 번째, 네 번째 인자로 전달할 수 있습니다:

```php
return to_route('users.show', ['user' => 1], 302, ['X-Framework' => 'Laravel']);
```

<a name="method-url"></a>
#### `url()`

`url` 함수는 지정한 경로에 대해 완전한 URL을 생성합니다:

```php
$url = url('user/profile');

$url = url('user/profile', [1]);
```

경로를 지정하지 않으면 `Illuminate\Routing\UrlGenerator` 인스턴스를 반환합니다:

```php
$current = url()->current();

$full = url()->full();

$previous = url()->previous();
```

<a name="miscellaneous"></a>
## 기타 (Miscellaneous)

<a name="method-abort"></a>
#### `abort()`

`abort` 함수는 [HTTP 예외](/docs/master/errors#http-exceptions)를 발생시켜, [예외 처리기](/docs/master/errors#handling-exceptions)에 의해 렌더링됩니다:

```php
abort(403);
```

예외 메시지와 사용자 정의 HTTP 헤더도 전달할 수 있습니다:

```php
abort(403, 'Unauthorized.', $headers);
```

<a name="method-abort-if"></a>
#### `abort_if()`

`abort_if` 함수는 주어진 조건이 참일 경우 HTTP 예외를 발생시킵니다:

```php
abort_if(! Auth::user()->isAdmin(), 403);
```

`abort` 함수와 마찬가지로 메시지 및 헤더 인자를 추가로 전달할 수 있습니다.

<a name="method-abort-unless"></a>
#### `abort_unless()`

`abort_unless` 함수는 주어진 조건이 거짓일 경우 HTTP 예외를 발생시킵니다:

```php
abort_unless(Auth::user()->isAdmin(), 403);
```

`abort` 함수와 마찬가지로 메시지 및 헤더 인자를 추가로 전달할 수 있습니다.

<a name="method-app"></a>
#### `app()`

`app` 함수는 [서비스 컨테이너](/docs/master/container) 인스턴스를 반환합니다:

```php
$container = app();
```

클래스나 인터페이스 이름을 인자로 넘기면 컨테이너에서 실행 결과를 반환합니다:

```php
$api = app('HelpSpot\API');
```

<a name="method-auth"></a>
#### `auth()`

`auth` 함수는 [인증기](/docs/master/authentication) 인스턴스를 반환합니다. `Auth` 파사드 대신 사용 가능합니다:

```php
$user = auth()->user();
```

원하는 가드를 지정할 수도 있습니다:

```php
$user = auth('admin')->user();
```

<a name="method-back"></a>
#### `back()`

`back` 함수는 사용자의 이전 위치로 [리다이렉트 HTTP 응답](/docs/master/responses#redirects)을 생성합니다:

```php
return back($status = 302, $headers = [], $fallback = '/');

return back();
```

<a name="method-bcrypt"></a>
#### `bcrypt()`

`bcrypt` 함수는 주어진 값을 Bcrypt 방식으로 해시 합니다. `Hash` 파사드 대안으로 사용됩니다:

```php
$password = bcrypt('my-secret-password');
```

<a name="method-blank"></a>
#### `blank()`

`blank` 함수는 주어진 값이 "비어있다"라고 판단되는지 확인합니다:

```php
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

`blank`의 반대는 [`filled`](#method-filled) 메서드를 참고하세요.

<a name="method-broadcast"></a>
#### `broadcast()`

`broadcast` 함수는 주어진 [이벤트](/docs/master/events)를 청취자들에게 방송합니다:

```php
broadcast(new UserRegistered($user));

broadcast(new UserRegistered($user))->toOthers();
```

<a name="method-cache"></a>
#### `cache()`

`cache` 함수는 [캐시](/docs/master/cache)에서 값을 가져오거나 저장하는 데 사용됩니다. 주어진 캐시 키가 없으면 기본값을 반환합니다:

```php
$value = cache('key');

$value = cache('key', 'default');
```

배열로 여러 키/값을 저장할 수 있고, 캐시 유지 기간(초 또는 지속 시간)도 함께 전달해야 합니다:

```php
cache(['key' => 'value'], 300);

cache(['key' => 'value'], now()->addSeconds(10));
```

<a name="method-class-uses-recursive"></a>
#### `class_uses_recursive()`

`class_uses_recursive` 함수는 주어진 클래스와 부모 클래스가 사용하는 모든 트레이트를 반환합니다:

```php
$traits = class_uses_recursive(App\Models\User::class);
```

<a name="method-collect"></a>
#### `collect()`

`collect` 함수는 주어진 값으로부터 [컬렉션](/docs/master/collections) 인스턴스를 생성합니다:

```php
$collection = collect(['taylor', 'abigail']);
```

<a name="method-config"></a>
#### `config()`

`config` 함수는 [설정](/docs/master/configuration) 값을 가져오거나 설정합니다. "dot" 표기법을 사용해 파일과 옵션명을 지정하며, 기본값도 지정할 수 있습니다:

```php
$value = config('app.timezone');

$value = config('app.timezone', $default);
```

실행 중에 설정 값을 변경하려면 배열로 키/값을 전달하세요. 다만, 이는 현재 요청 시에만 적용되며 실제 구성 파일에 영향을 주지 않습니다:

```php
config(['app.debug' => true]);
```

<a name="method-context"></a>
#### `context()`

`context` 함수는 [현재 컨텍스트](/docs/master/context) 값을 가져옵니다. 기본값도 지정 가능합니다:

```php
$value = context('trace_id');

$value = context('trace_id', $default);
```

배열로 컨텍스트 값을 설정할 수 있습니다:

```php
use Illuminate\Support\Str;

context(['trace_id' => Str::uuid()->toString()]);
```

<a name="method-cookie"></a>
#### `cookie()`

`cookie` 함수는 새로운 [쿠키](/docs/master/requests#cookies) 인스턴스를 생성합니다:

```php
$cookie = cookie('name', 'value', $minutes);
```

<a name="method-csrf-field"></a>
#### `csrf_field()`

`csrf_field` 함수는 CSRF 토큰 값을 포함한 HTML `hidden` 입력 필드를 생성합니다:

```blade
{{ csrf_field() }}
```

<a name="method-csrf-token"></a>
#### `csrf_token()`

`csrf_token` 함수는 현재 CSRF 토큰 값을 가져옵니다:

```php
$token = csrf_token();
```

<a name="method-decrypt"></a>
#### `decrypt()`

`decrypt` 함수는 주어진 값을 [복호화](/docs/master/encryption)합니다. `Crypt` 파사드 대안으로 사용할 수 있습니다:

```php
$password = decrypt($value);
```

<a name="method-dd"></a>
#### `dd()`

`dd` 함수는 변수를 덤프하고 스크립트 실행을 종료합니다:

```php
dd($value);

dd($value1, $value2, $value3, ...);
```

중단 없이 덤프만 하고 싶다면 [`dump`](#method-dump) 함수를 사용하세요.

<a name="method-dispatch"></a>
#### `dispatch()`

`dispatch` 함수는 주어진 [잡](/docs/master/queues#creating-jobs)을 Laravel [잡 큐](/docs/master/queues)에 푸시합니다:

```php
dispatch(new App\Jobs\SendEmails);
```

<a name="method-dispatch-sync"></a>
#### `dispatch_sync()`

`dispatch_sync` 함수는 주어진 잡을 [동기(sync)](/docs/master/queues#synchronous-dispatching) 큐에 넣어 즉시 처리합니다:

```php
dispatch_sync(new App\Jobs\SendEmails);
```

<a name="method-dump"></a>
#### `dump()`

`dump` 함수는 변수를 덤프합니다:

```php
dump($value);

dump($value1, $value2, $value3, ...);
```

덤프 후 실행 중단이 필요하면 [`dd`](#method-dd) 함수를 사용하세요.

<a name="method-encrypt"></a>
#### `encrypt()`

`encrypt` 함수는 주어진 값을 [암호화](/docs/master/encryption)합니다. `Crypt` 파사드 대안으로 사용할 수 있습니다:

```php
$secret = encrypt('my-secret-value');
```

<a name="method-env"></a>
#### `env()`

`env` 함수는 [환경 변수](/docs/master/configuration#environment-configuration) 값을 가져오거나 기본값을 반환합니다:

```php
$env = env('APP_ENV');

$env = env('APP_ENV', 'production');
```

> [!WARNING]
> 배포 과정에서 `config:cache` 명령어를 실행하면, `env` 함수는 반드시 구성 파일 내에서만 호출해야 합니다. 캐시가 생성되면 `.env` 파일이 더 이상 로드되지 않아 `env` 함수가 `null`을 반환할 수 있습니다.

<a name="method-event"></a>
#### `event()`

`event` 함수는 주어진 [이벤트](/docs/master/events)를 청취자에게 디스패치합니다:

```php
event(new UserRegistered($user));
```

<a name="method-fake"></a>
#### `fake()`

`fake` 함수는 Faker 싱글톤을 컨테이너에서 해석해 제공합니다. 모델 팩토리, DB 시드, 테스트, 프로토타입 등에서 가짜 데이터를 생성하기 편리합니다:

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

기본적으로 `fake` 함수는 `config/app.php` 내 `app.faker_locale` 설정을 따릅니다. 이는 보통 `APP_FAKER_LOCALE` 환경 변수로 지정합니다. 로케일을 직접 지정할 수도 있으며, 로케일별로 개별 싱글톤이 생성됩니다:

```php
fake('nl_NL')->name()
```

<a name="method-filled"></a>
#### `filled()`

`filled` 함수는 주어진 값이 "비어있지 않다"를 판단합니다:

```php
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

`filled`의 반대는 [`blank`](#method-blank) 메서드를 참고하세요.

<a name="method-info"></a>
#### `info()`

`info` 함수는 애플리케이션 [로그](/docs/master/logging)에 정보 레벨 메시지를 기록합니다:

```php
info('Some helpful information!');
```

컨텍스트 배열도 함께 전달할 수 있습니다:

```php
info('User login attempt failed.', ['id' => $user->id]);
```

<a name="method-literal"></a>
#### `literal()`

`literal` 함수는 주어진 명명 인자를 속성으로 하는 새 [stdClass](https://www.php.net/manual/en/class.stdclass.php) 인스턴스를 생성합니다:

```php
$obj = literal(
    name: 'Joe',
    languages: ['PHP', 'Ruby'],
);

$obj->name; // 'Joe'
$obj->languages; // ['PHP', 'Ruby']
```

<a name="method-logger"></a>
#### `logger()`

`logger` 함수는 디버그 레벨 메시지를 로그에 기록합니다:

```php
logger('Debug message');
```

컨텍스트 배열도 전달할 수 있습니다:

```php
logger('User has logged in.', ['id' => $user->id]);
```

인자를 전달하지 않으면 [로거](/docs/master/logging) 인스턴스를 반환합니다:

```php
logger()->error('You are not allowed here.');
```

<a name="method-method-field"></a>
#### `method_field()`

`method_field` 함수는 폼의 HTTP 메서드 스푸핑 값을 담은 HTML `hidden` 입력 필드를 생성합니다:

```blade
<form method="POST">
    {{ method_field('DELETE') }}
</form>
```

<a name="method-now"></a>
#### `now()`

`now` 함수는 현재 시각에 대한 새로운 `Illuminate\Support\Carbon` 인스턴스를 생성합니다:

```php
$now = now();
```

<a name="method-old"></a>
#### `old()`

`old` 함수는 세션에 플래시 된 이전 입력 값을 가져옵니다:

```php
$value = old('value');

$value = old('value', 'default');
```

모델 속성으로서 기본값을 주로 쓰기에, Eloquent 모델을 두 번째 인자로 넘길 수도 있습니다:

```blade
{{ old('name', $user->name) }}

// 아래와 동일
{{ old('name', $user) }}
```

<a name="method-once"></a>
#### `once()`

`once` 함수는 주어진 콜백을 실행하고, 요청 내에서 결과를 캐싱합니다. 같은 콜백을 반복 호출해도 최초 결과를 반환합니다:

```php
function random(): int
{
    return once(function () {
        return random_int(1, 1000);
    });
}

random(); // 123
random(); // 123 (캐싱된 결과)
random(); // 123 (캐싱된 결과)
```

객체 내에서 실행될 경우 캐싱된 결과도 객체 인스턴스에 고유합니다:

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
$service->all(); // (캐싱된 결과)

$secondService = new NumberService;

$secondService->all();
$secondService->all(); // (캐싱된 결과)
```
<a name="method-optional"></a>
#### `optional()`

`optional` 함수는 어떤 객체나 값을 받아, 값이 `null`일 경우 프로퍼티 혹은 메서드 호출 시 `null`을 반환해 오류를 방지합니다:

```php
return optional($user->address)->street;

{!! old('name', optional($user)->name) !!}
```

또한 두 번째 인자에 콜백을 전달할 수 있으며, 값이 `null`이 아니면 콜백을 실행합니다:

```php
return optional(User::find($id), function (User $user) {
    return $user->name;
});
```

<a name="method-policy"></a>
#### `policy()`

`policy` 메서드는 주어진 클래스에 대한 [정책](/docs/master/authorization#creating-policies) 인스턴스를 반환합니다:

```php
$policy = policy(App\Models\User::class);
```

<a name="method-redirect"></a>
#### `redirect()`

`redirect` 함수는 [리다이렉트 HTTP 응답](/docs/master/responses#redirects)을 반환하며, 인자 없이 호출 시 리다이렉트 인스턴스를 반환합니다:

```php
return redirect($to = null, $status = 302, $headers = [], $https = null);

return redirect('/home');

return redirect()->route('route.name');
```

<a name="method-report"></a>
#### `report()`

`report` 함수는 [예외 처리기](/docs/master/errors#handling-exceptions)에 예외를 보고합니다:

```php
report($e);
```

문자열이 전달되면, 해당 메시지를 가진 예외 객체를 만들어 보고합니다:

```php
report('Something went wrong.');
```

<a name="method-report-if"></a>
#### `report_if()`

`report_if` 함수는 주어진 조건이 참일 때 예외를 보고합니다:

```php
report_if($shouldReport, $e);

report_if($shouldReport, 'Something went wrong.');
```

<a name="method-report-unless"></a>
#### `report_unless()`

`report_unless` 함수는 주어진 조건이 거짓일 때 예외를 보고합니다:

```php
report_unless($reportingDisabled, $e);

report_unless($reportingDisabled, 'Something went wrong.');
```

<a name="method-request"></a>
#### `request()`

`request` 함수는 현재 [요청](/docs/master/requests) 인스턴스를 반환하거나, 특정 입력 값을 가져옵니다:

```php
$request = request();

$value = request('key', $default);
```

<a name="method-rescue"></a>
#### `rescue()`

`rescue` 함수는 콜백을 실행하며 예외 발생 시 예외 처리기로 보고하고, 예외를 던지지 않고 계속 실행을 이어갑니다:

```php
return rescue(function () {
    return $this->method();
});
```

두 번째 인자로 예외 발생시 반환할 기본값을 줄 수 있습니다:

```php
return rescue(function () {
    return $this->method();
}, false);

return rescue(function () {
    return $this->method();
}, function () {
    return $this->failure();
});
```

`report` 인자는 예외를 보고할지 여부를 콜백으로 결정하도록 합니다:

```php
return rescue(function () {
    return $this->method();
}, report: function (Throwable $throwable) {
    return $throwable instanceof InvalidArgumentException;
});
```

<a name="method-resolve"></a>
#### `resolve()`

`resolve` 함수는 주어진 클래스 또는 인터페이스 이름을 서비스 컨테이너에서 해석해 인스턴스를 반환합니다:

```php
$api = resolve('HelpSpot\API');
```

<a name="method-response"></a>
#### `response()`

`response` 함수는 [응답](/docs/master/responses) 인스턴스를 생성하거나 응답 팩토리 인스턴스를 반환합니다:

```php
return response('Hello World', 200, $headers);

return response()->json(['foo' => 'bar'], 200, $headers);
```

<a name="method-retry"></a>
#### `retry()`

`retry` 함수는 지정한 최대 시도 횟수까지 콜백을 시도하며, 예외 발생 시 재시도합니다. 최대 시도 초과 시 예외를 던집니다:

```php
return retry(5, function () {
    // 최대 5회 시도하면서 100ms 휴식...
}, 100);
```

시도마다 휴식 시간을 직접 계산하고 싶으면 세 번째 인자에 콜백을 전달하세요:

```php
use Exception;

return retry(5, function () {
    // ...
}, function (int $attempt, Exception $exception) {
    return $attempt * 100;
});
```

첫 번째 인자에 밀리초 휴식 배열을 전달할 수도 있습니다:

```php
return retry([100, 200], function () {
    // 첫 재시도 후 100ms, 두 번째 재시도 후 200ms 휴식...
});
```

특정 조건에서만 재시도하려면 네 번째 인자로 콜백을 전달하세요:

```php
use Exception;

return retry(5, function () {
    // ...
}, 100, function (Exception $exception) {
    return $exception instanceof RetryException;
});
```

<a name="method-session"></a>
#### `session()`

`session` 함수는 [세션](/docs/master/session) 값을 조회하거나 설정합니다:

```php
$value = session('key');
```

배열로 키/값을 전달해 설정할 수도 있습니다:

```php
session(['chairs' => 7, 'instruments' => 3]);
```

인자 없이 호출하면 세션 스토어 인스턴스를 반환합니다:

```php
$value = session()->get('key');

session()->put('key', $value);
```

<a name="method-tap"></a>
#### `tap()`

`tap` 함수는 값과 클로저를 받아, 클로저에 값을 전달하고 값을 반환합니다. 클로저 반환값은 무시됩니다:

```php
$user = tap(User::first(), function (User $user) {
    $user->name = 'taylor';

    $user->save();
});
```

클로저를 전달하지 않으면 값에 메서드를 호출할 수 있는데, 호출 결과와 상관없이 항상 `$value`가 리턴됩니다. 예를 들어 Eloquent `update`는 정수 반환이 기본이지만, `tap`을 통해 모델 자체를 반환하게 할 수 있습니다:

```php
$user = tap($user)->update([
    'name' => $name,
    'email' => $email,
]);
```

클래스에 `tap` 메서드를 추가하려면 `Illuminate\Support\Traits\Tappable` 트레이트를 사용하세요. `tap` 메서드는 클로저 하나만 받고, 자기 자신을 클로저에 전달 후 반환합니다:

```php
return $user->tap(function (User $user) {
    // ...
});
```

<a name="method-throw-if"></a>
#### `throw_if()`

`throw_if` 함수는 조건이 참일 경우 주어진 예외를 던집니다:

```php
throw_if(! Auth::user()->isAdmin(), AuthorizationException::class);

throw_if(
    ! Auth::user()->isAdmin(),
    AuthorizationException::class,
    'You are not allowed to access this page.'
);
```

<a name="method-throw-unless"></a>
#### `throw_unless()`

`throw_unless` 함수는 조건이 거짓일 경우 주어진 예외를 던집니다:

```php
throw_unless(Auth::user()->isAdmin(), AuthorizationException::class);

throw_unless(
    Auth::user()->isAdmin(),
    AuthorizationException::class,
    'You are not allowed to access this page.'
);
```

<a name="method-today"></a>
#### `today()`

`today` 함수는 현재 날짜에 대한 새로운 `Illuminate\Support\Carbon` 인스턴스를 생성합니다:

```php
$today = today();
```

<a name="method-trait-uses-recursive"></a>
#### `trait_uses_recursive()`

`trait_uses_recursive` 함수는 주어진 트레이트가 사용하는 모든 트레이트를 반환합니다:

```php
$traits = trait_uses_recursive(\Illuminate\Notifications\Notifiable::class);
```

<a name="method-transform"></a>
#### `transform()`

`transform` 함수는 값이 [blank](#method-blank)가 아니라면 클로저를 실행해 반환값을 리턴합니다:

```php
$callback = function (int $value) {
    return $value * 2;
};

$result = transform(5, $callback);

// 10
```

값이 blank이면 기본값 혹은 기본 클로저(세 번째 인자)를 반환합니다:

```php
$result = transform(null, $callback, 'The value is blank');

// The value is blank
```

<a name="method-validator"></a>
#### `validator()`

`validator` 함수는 주어진 인자를 사용해 새로운 [검증기](/docs/master/validation) 인스턴스를 생성합니다. `Validator` 파사드 대안입니다:

```php
$validator = validator($data, $rules, $messages);
```

<a name="method-value"></a>
#### `value()`

`value` 함수는 인자를 그대로 반환합니다. 만약 인자가 클로저라면 실행 후 반환값을 리턴합니다:

```php
$result = value(true);

// true

$result = value(function () {
    return false;
});

// false
```

추가 인자를 전달할 수 있으며, 첫 인자가 클로저라면 이를 클로저 인자로 넘깁니다:

```php
$result = value(function (string $name) {
    return $name;
}, 'Taylor');

// 'Taylor'
```

<a name="method-view"></a>
#### `view()`

`view` 함수는 [뷰](/docs/master/views) 인스턴스를 반환합니다:

```php
return view('auth.login');
```

<a name="method-with"></a>
#### `with()`

`with` 함수는 인자를 그대로 반환합니다. 두 번째 인자로 클로저가 주어지면 실행 후 결과를 반환합니다:

```php
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

`when` 함수는 조건이 참이면 주어진 값을 반환합니다. 거짓이면 `null`입니다. 두 번째 인자가 클로저면 실행 결과를 반환합니다:

```php
$value = when(true, 'Hello World');

$value = when(true, fn () => 'Hello World');
```

주로 HTML 속성 조건부 렌더링에 유용합니다:

```blade
<div {!! when($condition, 'wire:poll="calculate"') !!}>
    ...
</div>
```

<a name="other-utilities"></a>
## 기타 유틸리티 (Other Utilities)

<a name="benchmarking"></a>
### 벤치마킹 (Benchmarking)

애플리케이션의 일부 성능 테스트가 필요할 때, `Benchmark` 클래스는 지정한 콜백들이 실행되는 데 걸리는 밀리초를 측정할 수 있습니다:

```php
<?php

use App\Models\User;
use Illuminate\Support\Benchmark;

Benchmark::dd(fn () => User::find(1)); // 0.1 ms

Benchmark::dd([
    'Scenario 1' => fn () => User::count(), // 0.5 ms
    'Scenario 2' => fn () => User::all()->count(), // 20.0 ms
]);
```

기본적으로 콜백을 한 번 호출하며 소요 시간을 출력합니다.

반복 호출 수(Iterations)를 두 번째 인자로 지정해 평균 실행 시간을 확인할 수 있습니다:

```php
Benchmark::dd(fn () => User::count(), iterations: 10); // 0.5 ms
```

콜백이 반환하는 값을 얻으면서 실행 시간도 알고 싶으면 `value` 메서드를 사용하세요. 반환값과 밀리초를 가진 튜플을 반환합니다:

```php
[$count, $duration] = Benchmark::value(fn () => User::count());
```

<a name="dates"></a>
### 날짜 (Dates)

Laravel은 강력한 날짜 및 시간 조작 라이브러리 [Carbon](https://carbon.nesbot.com/docs/)을 포함합니다. 새 `Carbon` 인스턴스는 애플리케이션 어디에서나 `now` 함수를 통해 생성할 수 있습니다:

```php
$now = now();
```

또는 `Illuminate\Support\Carbon` 클래스로 생성할 수도 있습니다:

```php
use Illuminate\Support\Carbon;

$now = Carbon::now();
```

Carbon과 기능에 대한 자세한 사항은 [공식 Carbon 문서](https://carbon.nesbot.com/docs/)를 참고하세요.

<a name="deferred-functions"></a>
### 지연 함수 (Deferred Functions)

> [!WARNING]
> 지연 함수 기능은 현재 베타 상태로, 커뮤니티 피드백을 수집 중입니다.

Laravel의 [큐 잡](/docs/master/queues)이 백그라운드 작업 큐를 제공하지만, 간단한 작업을 즉시 처리하지 않고 나중에 처리하도록 넘기고 싶을 때 지연 함수를 사용할 수 있습니다.

`Illuminate\Support\defer` 함수에 클로저를 전달하면 HTTP 응답이 사용자의 브라우저에 전달된 후에 클로저가 실행되어 애플리케이션의 반응 속도를 향상시킵니다:

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

기본적으로, `Illuminate\Support\defer`를 호출한 HTTP 응답, Artisan 명령, 또는 큐 잡이 성공적으로 완료되었을 때만 실행됩니다. `4xx` 혹은 `5xx` 응답이 발생하면 실행되지 않습니다. 항상 실행하려면 `always` 메서드를 체이닝하세요:

```php
defer(fn () => Metrics::reportOrder($order))->always();
```

<a name="cancelling-deferred-functions"></a>
#### 지연 함수 취소하기

실행 전 지연 함수를 취소하려면 이름을 지정하고 `forget` 메서드를 사용하세요:

```php
defer(fn () => Metrics::report(), 'reportMetrics');

defer()->forget('reportMetrics');
```

<a name="deferred-function-compatibility"></a>
#### 지연 함수 호환성

Laravel 10.x에서 11.x로 업그레이드했는데 아직 `app/Http/Kernel.php` 파일을 쓰는 경우, 커널의 `$middleware` 속성 맨 앞에 `InvokeDeferredCallbacks` 미들웨어를 추가해야 합니다:

```php
protected $middleware = [
    \Illuminate\Foundation\Http\Middleware\InvokeDeferredCallbacks::class, // [tl! add]
    \App\Http\Middleware\TrustProxies::class,
    // ...
];
```

<a name="disabling-deferred-functions-in-tests"></a>
#### 테스트에서 지연 함수 비활성화하기

테스트 작성 시 지연 함수 실행을 바로 하도록 비활성화하고 싶으면 `withoutDefer`를 호출하세요:

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

기본 테스트 클래스의 `setUp` 메서드에서 호출해 전체 테스트에 적용할 수도 있습니다:

```php
<?php

namespace Tests;

use Illuminate\Foundation\Testing\TestCase as BaseTestCase;

abstract class TestCase extends BaseTestCase
{
    protected function setUp(): void // [tl! add:start]
    {
        parent::setUp();

        $this->withoutDefer();
    } // [tl! add:end]
}
```

<a name="lottery"></a>
### 복권 (Lottery)

Laravel의 복권 클래스는 주어진 확률에 따라 콜백을 실행할 수 있습니다. 예를 들어, 5% 확률로만 코드를 실행하고 싶을 때 유용합니다:

```php
use Illuminate\Support\Lottery;

Lottery::odds(1, 20)
    ->winner(fn () => $user->won())
    ->loser(fn () => $user->lost())
    ->choose();
```

다른 Laravel 기능과 결합하여, 예를 들어 느린 쿼리 보고를 일정 확률로 제한할 수도 있습니다. `Lottery` 클래스가 호출 가능한(callable)이므로, 호출 가능한 곳에 넘길 수 있습니다:

```php
use Carbon\CarbonInterval;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Lottery;

DB::whenQueryingForLongerThan(
    CarbonInterval::seconds(2),
    Lottery::odds(1, 100)->winner(fn () => report('Querying > 2 seconds.')),
);
```

<a name="testing-lotteries"></a>
#### 복권 테스트하기

Laravel은 복권 호출을 테스트하기 편리하게 돕는 메서드를 제공합니다:

```php
// 복권 항상 당첨...
Lottery::alwaysWin();

// 복권 항상 미당첨...
Lottery::alwaysLose();

// 복권 당첨 → 미당첨 → 정상 동작 순서 반복...
Lottery::fix([true, false]);

// 복권 정상 동작으로 복원...
Lottery::determineResultsNormally();
```

<a name="pipeline"></a>
### 파이프라인 (Pipeline)

Laravel의 `Pipeline` 패사드는 입력값을 일련의 호출 가능한 클래스, 클로저, 콜러블을 통해 전달하며, 각 단계에서 입력값을 검사하거나 변형할 수 있게 합니다:

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

각 단계에서는 입력값과 `$next` 클로저를 받으며, `$next`를 호출해 다음 단계로 넘깁니다. 마지막 단계 호출 시 `then` 메서드에 전달한 콜러블이 호출됩니다.

물론, 클로저 외에 인보커블 클래스도 쓸 수 있습니다. 클래스명은 서비스 컨테이너에서 인스턴스화하여 의존성 주입이 가능합니다:

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
### 슬립 (Sleep)

Laravel의 `Sleep` 클래스는 PHP 네이티브 `sleep`와 `usleep` 함수들을 감싸 테스트하기 편리한 API를 제공합니다:

```php
use Illuminate\Support\Sleep;

$waiting = true;

while ($waiting) {
    Sleep::for(1)->second();

    $waiting = /* ... */;
}
```

다양한 시간 단위 메서드를 사용할 수 있습니다:

```php
// 슬립 후 값을 반환...
$result = Sleep::for(1)->second()->then(fn () => 1 + 1);

// 조건을 만족하는 동안 슬립...
Sleep::for(1)->second()->while(fn () => shouldKeepSleeping());

// 90초 동안 일시 중지...
Sleep::for(1.5)->minutes();

// 2초 동안 일시 중지...
Sleep::for(2)->seconds();

// 500 밀리초 동안 일시 중지...
Sleep::for(500)->milliseconds();

// 5000 마이크로초 동안 일시 중지...
Sleep::for(5000)->microseconds();

// 지정 시각까지 일시 중지...
Sleep::until(now()->addMinute());

// PHP 네이티브 sleep 별칭...
Sleep::sleep(2);

// PHP 네이티브 usleep 별칭...
Sleep::usleep(5000);
```

시간 단위를 조합하려면 `and` 메서드를 이용하세요:

```php
Sleep::for(1)->second()->and(10)->milliseconds();
```

<a name="testing-sleep"></a>
#### 슬립 테스트하기

`Sleep` 혹은 PHP 네이티브 sleep 함수를 테스트하면 실행이 지연되어 테스트 속도가 느려집니다. 다음 예제 코드는 최소 1초 이상 소요될 것입니다:

```php
$waiting = /* ... */;

$seconds = 1;

while ($waiting) {
    Sleep::for($seconds++)->seconds();

    $waiting = /* ... */;
}
```

다행히 `Sleep::fake()` 로 슬립을 가짜 처리해 테스트 속도를 빠르게 유지할 수 있습니다:

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

가짜 슬립 상태에서 발생한 슬립에 대해 여러 검사 메서드를 제공합니다. 예를 들어 정해진 순서대로 슬립했는지 테스트:

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

기타 유용한 어서션 메서드들:

```php
use Carbon\CarbonInterval as Duration;
use Illuminate\Support\Sleep;

// 슬립 횟수 검증
Sleep::assertSleptTimes(3);

// 슬립 지속시간 검증
Sleep::assertSlept(function (Duration $duration): bool {
    return /* ... */;
}, times: 1);

// 슬립이 한 번도 호출되지 않음 검증
Sleep::assertNeverSlept();

// 슬립 호출되었지만 실제 실행 정지는 없었음 검증
Sleep::assertInsomniac();
```

가짜 슬립 발생 시 특정 동작을 수행하려면 `whenFakingSleep` 콜백을 설정하세요. 아래 예시에서는 Carbon 시간 조작 기능으로 가짜 슬립 시간만큼 즉시 시간 경과시킵니다:

```php
use Carbon\CarbonInterval as Duration;

$this->freezeTime();

Sleep::fake();

Sleep::whenFakingSleep(function (Duration $duration) {
    // 가짜 슬립 시 시간 진전...
    $this->travel($duration->totalMilliseconds)->milliseconds();
});
```

위가 자주 쓰이므로 `fake` 메서드의 `syncWithCarbon` 인자로 Carbon 동기화를 활성화할 수 있습니다:

```php
Sleep::fake(syncWithCarbon: true);

$start = now();

Sleep::for(1)->second();

$start->diffForHumans(); // 1 second ago
```

Laravel 내부는 슬립 클래스를 사용해 중지 상태를 구현합니다. 예를 들어 [`retry`](#method-retry) 헬퍼가 이를 사용해 테스트 하기 쉽게 개선됩니다.

<a name="timebox"></a>
### 타임박스 (Timebox)

`Timebox` 클래스는 지정한 시간 동안 콜백이 최소한 그 시간만큼 실행되도록 보장합니다. 암호학, 인증 검사 등에서 실행 시간 차이로 인한 공격을 방지할 때 유용합니다.

실행 시간이 타임박스보다 길면 별도 동작하지 않습니다. 최대 시간을 충분히 여유 있게 지정하는 책임은 개발자에게 있습니다.

클로저와 마이크로초 단위 제한 시간을 받아 호출 후 지정 시간까지 대기합니다:

```php
use Illuminate\Support\Timebox;

(new Timebox)->call(function ($timebox) {
    // ...
}, microseconds: 10000);
```

클로저 내 예외가 발생해도 지정 시간만큼 기다린 후 예외를 다시 던집니다.