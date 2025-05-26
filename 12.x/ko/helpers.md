# 헬퍼 (Helpers)

- [소개](#introduction)
- [사용 가능한 메서드](#available-methods)
- [기타 유틸리티](#other-utilities)
    - [벤치마킹](#benchmarking)
    - [날짜](#dates)
    - [지연 실행 함수](#deferred-functions)
    - [로터리](#lottery)
    - [파이프라인](#pipeline)
    - [슬립](#sleep)
    - [타임박스](#timebox)
    - [URI](#uri)

<a name="introduction"></a>
## 소개

라라벨에는 다양한 전역 "헬퍼" PHP 함수가 내장되어 있습니다. 이들 함수 중 상당수는 프레임워크 내부에서 자체적으로 사용되지만, 필요하다면 여러분의 애플리케이션에서도 얼마든지 자유롭게 활용하실 수 있습니다.

<a name="available-methods"></a>
## 사용 가능한 메서드



<a name="arrays-and-objects-method-list"></a>
### 배열 & 객체

<div class="collection-method-list" markdown="1">

[Arr::accessible](#method-array-accessible)
[Arr::add](#method-array-add)
[Arr::array](#method-array-array)
[Arr::boolean](#method-array-boolean)
[Arr::collapse](#method-array-collapse)
[Arr::crossJoin](#method-array-crossjoin)
[Arr::divide](#method-array-divide)
[Arr::dot](#method-array-dot)
[Arr::except](#method-array-except)
[Arr::exists](#method-array-exists)
[Arr::first](#method-array-first)
[Arr::flatten](#method-array-flatten)
[Arr::float](#method-array-float)
[Arr::forget](#method-array-forget)
[Arr::from](#method-array-from)
[Arr::get](#method-array-get)
[Arr::has](#method-array-has)
[Arr::hasAll](#method-array-hasall)
[Arr::hasAny](#method-array-hasany)
[Arr::integer](#method-array-integer)
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
[Arr::sole](#method-array-sole)
[Arr::sort](#method-array-sort)
[Arr::sortDesc](#method-array-sort-desc)
[Arr::sortRecursive](#method-array-sort-recursive)
[Arr::string](#method-array-string)
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
### 숫자

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
[Number::spellOrdinal](#method-number-spell-ordinal)
[Number::trim](#method-number-trim)
[Number::useLocale](#method-number-use-locale)
[Number::withLocale](#method-number-with-locale)
[Number::useCurrency](#method-number-use-currency)
[Number::withCurrency](#method-number-with-currency)

</div>

<a name="paths-method-list"></a>
### 경로

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
[uri](#method-uri)
[url](#method-url)

</div>

<a name="miscellaneous-method-list"></a>
### 그 외

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
## 배열 & 객체

<a name="method-array-accessible"></a>
#### `Arr::accessible()`

`Arr::accessible` 메서드는 전달된 값이 배열에 접근 가능한지 여부를 판단합니다.

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

`Arr::add` 메서드는 지정한 키가 배열에 존재하지 않거나 값이 `null`일 경우, 해당 키/값 쌍을 배열에 추가합니다.

```php
use Illuminate\Support\Arr;

$array = Arr::add(['name' => 'Desk'], 'price', 100);

// ['name' => 'Desk', 'price' => 100]

$array = Arr::add(['name' => 'Desk', 'price' => null], 'price', 100);

// ['name' => 'Desk', 'price' => 100]
```

<a name="method-array-array"></a>
#### `Arr::array()`

`Arr::array` 메서드는 "dot" 표기법을 사용해 다차원 배열에서 값을 가져옵니다(동일하게 동작하는 [Arr::get()](#method-array-get) 참조). 단, 요청한 값이 `array` 타입이 아니라면 `InvalidArgumentException` 예외를 발생시킵니다.

```
use Illuminate\Support\Arr;

$array = ['name' => 'Joe', 'languages' => ['PHP', 'Ruby']];

$value = Arr::array($array, 'languages');

// ['PHP', 'Ruby']

$value = Arr::array($array, 'name');

// throws InvalidArgumentException
```

<a name="method-array-boolean"></a>
#### `Arr::boolean()`

`Arr::boolean` 메서드는 "dot" 표기법을 사용해 다차원 배열에서 값을 가져오되(동일하게 동작하는 [Arr::get()](#method-array-get) 참조), 요청한 값이 `boolean` 타입이 아니면 `InvalidArgumentException` 예외를 발생시킵니다.

```
use Illuminate\Support\Arr;

$array = ['name' => 'Joe', 'available' => true];

$value = Arr::boolean($array, 'available');

// true

$value = Arr::boolean($array, 'name');

// throws InvalidArgumentException
```


<a name="method-array-collapse"></a>
#### `Arr::collapse()`

`Arr::collapse` 메서드는 여러 배열을 하나의 배열로 합칩니다.

```php
use Illuminate\Support\Arr;

$array = Arr::collapse([[1, 2, 3], [4, 5, 6], [7, 8, 9]]);

// [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

<a name="method-array-crossjoin"></a>
#### `Arr::crossJoin()`

`Arr::crossJoin` 메서드는 주어진 배열 간의 교차 곱셈(데카르트 곱, 모든 가능한 조합)을 만들어 새로운 배열로 반환합니다.

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

`Arr::divide` 메서드는 하나의 배열을 키만 담긴 배열과 값만 담긴 배열, 두 개의 배열로 분리하여 반환합니다.

```php
use Illuminate\Support\Arr;

[$keys, $values] = Arr::divide(['name' => 'Desk']);

// $keys: ['name']

// $values: ['Desk']
```

<a name="method-array-dot"></a>
#### `Arr::dot()`

`Arr::dot` 메서드는 다차원 배열을 "dot" 표기법을 활용하여 한 단계의 평면 배열로 변환합니다. 이때 각 키에 계층 구조가 그대로 드러나도록 점(`.`)으로 표현됩니다.

```php
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

$flattened = Arr::dot($array);

// ['products.desk.price' => 100]
```

<a name="method-array-except"></a>
#### `Arr::except()`

`Arr::except` 메서드는 지정된 키/값 쌍을 배열에서 제거합니다.

```php
use Illuminate\Support\Arr;

$array = ['name' => 'Desk', 'price' => 100];

$filtered = Arr::except($array, ['price']);

// ['name' => 'Desk']
```

<a name="method-array-exists"></a>
#### `Arr::exists()`

`Arr::exists` 메서드는 주어진 키가 해당 배열에 존재하는지 검사합니다.

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

`Arr::first` 메서드는 전달된 배열에서 주어진 조건(진위 검사)에 통과하는 첫 번째 요소를 반환합니다.

```php
use Illuminate\Support\Arr;

$array = [100, 200, 300];

$first = Arr::first($array, function (int $value, int $key) {
    return $value >= 150;
});

// 200
```

또한, 세 번째 인수로 기본값을 전달할 수 있으며, 조건에 맞는 값이 없을 경우 이 값이 반환됩니다.

```php
use Illuminate\Support\Arr;

$first = Arr::first($array, $callback, $default);
```

<a name="method-array-flatten"></a>
#### `Arr::flatten()`

`Arr::flatten` 메서드는 다차원 배열을 한 단계의 평면 배열로 만들어 반환합니다.

```php
use Illuminate\Support\Arr;

$array = ['name' => 'Joe', 'languages' => ['PHP', 'Ruby']];

$flattened = Arr::flatten($array);

// ['Joe', 'PHP', 'Ruby']
```

<a name="method-array-float"></a>
#### `Arr::float()`

`Arr::float` 메서드는 "dot" 표기법을 사용해 다차원 배열에서 값을 가져오되([Arr::get()](#method-array-get)과 동일), 요청한 값이 `float` 타입이 아니면 `InvalidArgumentException` 예외를 발생시킵니다.

```
use Illuminate\Support\Arr;

$array = ['name' => 'Joe', 'balance' => 123.45];

$value = Arr::float($array, 'balance');

// 123.45

$value = Arr::float($array, 'name');

// throws InvalidArgumentException
```

<a name="method-array-forget"></a>
#### `Arr::forget()`

`Arr::forget` 메서드는 "dot" 표기법을 사용해 다차원 배열에서 지정한 키/값 쌍을 제거합니다.

```php
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

Arr::forget($array, 'products.desk');

// ['products' => []]
```

<a name="method-array-from"></a>
#### `Arr::from()`

`Arr::from` 메서드는 다양한 입력 타입을 순수 PHP 배열로 변환합니다. 이 메서드는 배열, 객체는 물론이고 라라벨의 여러 인터페이스(`Arrayable`, `Enumerable`, `Jsonable`, `JsonSerializable` 등)를 구현한 인스턴스, 그리고 `Traversable`, `WeakMap` 객체까지 지원합니다.

```php
use Illuminate\Support\Arr;

Arr::from((object) ['foo' => 'bar']); // ['foo' => 'bar']

class TestJsonableObject implements Jsonable
{
    public function toJson($options = 0)
    {
        return json_encode(['foo' => 'bar']);
    }
}

Arr::from(new TestJsonableObject); // ['foo' => 'bar']
```

<a name="method-array-get"></a>
#### `Arr::get()`

`Arr::get` 메서드는 "dot" 표기법을 사용하여 다차원 배열에서 값을 가져옵니다.

```php
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

$price = Arr::get($array, 'products.desk.price');

// 100
```

`Arr::get` 메서드는 기본값을 세 번째 인수로 받을 수 있는데, 지정한 키가 없을 경우 이 값이 반환됩니다.

```php
use Illuminate\Support\Arr;

$discount = Arr::get($array, 'products.desk.discount', 0);

// 0
```

<a name="method-array-has"></a>
#### `Arr::has()`

`Arr::has` 메서드는 "dot" 표기법을 사용해 배열에 특정 항목(또는 항목들)이 존재하는지 확인합니다.

```php
use Illuminate\Support\Arr;

$array = ['product' => ['name' => 'Desk', 'price' => 100]];

$contains = Arr::has($array, 'product.name');

// true

$contains = Arr::has($array, ['product.price', 'product.discount']);

// false
```

<a name="method-array-hasall"></a>
#### `Arr::hasAll()`

`Arr::hasAll` 메서드는 "dot" 표기법을 사용하여, 전달한 모든 키가 해당 배열에 존재하는지 확인합니다.

```php
use Illuminate\Support\Arr;

$array = ['name' => 'Taylor', 'language' => 'php'];

Arr::hasAll($array, ['name']); // true
Arr::hasAll($array, ['name', 'language']); // true
Arr::hasAll($array, ['name', 'ide']); // false
```

#### `Arr::hasAny()`

`Arr::hasAny` 메서드는 "dot" 표기법을 사용하여 배열에 주어진 항목들 중 하나라도 존재하는지 확인합니다.

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

<a name="method-array-integer"></a>
#### `Arr::integer()`

`Arr::integer` 메서드는 [Arr::get()](#method-array-get)과 마찬가지로 "dot" 표기법을 사용해 깊이 중첩된 배열에서 값을 가져오지만, 요청한 값이 `int` 타입이 아니면 `InvalidArgumentException`을 발생시킵니다.

```
use Illuminate\Support\Arr;

$array = ['name' => 'Joe', 'age' => 42];

$value = Arr::integer($array, 'age');

// 42

$value = Arr::integer($array, 'name');

// throws InvalidArgumentException
```

<a name="method-array-isassoc"></a>
#### `Arr::isAssoc()`

`Arr::isAssoc` 메서드는 주어진 배열이 연관 배열(associative array)인 경우 `true`를 반환합니다. 배열의 키가 0부터 시작하는 연속된 숫자가 아니라면 연관 배열로 간주합니다.

```php
use Illuminate\Support\Arr;

$isAssoc = Arr::isAssoc(['product' => ['name' => 'Desk', 'price' => 100]]);

// true

$isAssoc = Arr::isAssoc([1, 2, 3]);

// false
```

<a name="method-array-islist"></a>
#### `Arr::isList()`

`Arr::isList` 메서드는 주어진 배열의 키가 0부터 시작하는 연속된 정수일 경우 `true`를 반환합니다.

```php
use Illuminate\Support\Arr;

$isList = Arr::isList(['foo', 'bar', 'baz']);

// true

$isList = Arr::isList(['product' => ['name' => 'Desk', 'price' => 100]]);

// false
```

<a name="method-array-join"></a>
#### `Arr::join()`

`Arr::join` 메서드는 배열 요소들을 문자열로 결합합니다. 두 번째 인수로 일반 결합 문자열을 지정하며, 세 번째 인수로 마지막 요소 앞에만 사용될 별도의 문자열을 지정할 수 있습니다.

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

`Arr::keyBy` 메서드는 배열의 요소들을 주어진 키의 값으로 다시 키를 설정합니다. 여러 항목이 동일한 키를 가지면, 마지막 항목만 새 배열에 남게 됩니다.

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

`Arr::last` 메서드는 주어진 조건(test)을 통과한 배열의 마지막 요소를 반환합니다.

```php
use Illuminate\Support\Arr;

$array = [100, 200, 300, 110];

$last = Arr::last($array, function (int $value, int $key) {
    return $value >= 150;
});

// 300
```

조건을 통과하는 값이 없다면, 세 번째 인수로 기본값을 넘긴 경우 그 값이 반환됩니다.

```php
use Illuminate\Support\Arr;

$last = Arr::last($array, $callback, $default);
```

<a name="method-array-map"></a>
#### `Arr::map()`

`Arr::map` 메서드는 배열을 순회하며 각 값과 키를 콜백에 전달합니다. 콜백에서 반환된 값으로 배열 값이 대체됩니다.

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

`Arr::mapSpread` 메서드는 배열을 순회하면서 중첩된 항목들의 값을 콜백(클로저)에 인수로 전달합니다. 클로저에서 항목을 수정하여 반환하면, 그 결과로 새 배열이 만들어집니다.

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

`Arr::mapWithKeys` 메서드는 배열을 순회하면서 각 값을 콜백에 전달합니다. 콜백은 단일 키-값 쌍을 담은 연관 배열을 반환해야 합니다.

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

`Arr::only` 메서드는 주어진 배열에서 지정한 키-값 쌍만 반환합니다.

```php
use Illuminate\Support\Arr;

$array = ['name' => 'Desk', 'price' => 100, 'orders' => 10];

$slice = Arr::only($array, ['name', 'price']);

// ['name' => 'Desk', 'price' => 100]
```

<a name="method-array-partition"></a>
#### `Arr::partition()`

`Arr::partition` 메서드는 PHP 배열 구조 분해(destructuring)와 함께 사용해, 주어진 조건을 만족하는 요소와 만족하지 않는 요소를 분리합니다.

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

`Arr::pluck` 메서드는 배열에서 주어진 키의 모든 값을 추출합니다.

```php
use Illuminate\Support\Arr;

$array = [
    ['developer' => ['id' => 1, 'name' => 'Taylor']],
    ['developer' => ['id' => 2, 'name' => 'Abigail']],
];

$names = Arr::pluck($array, 'developer.name');

// ['Taylor', 'Abigail']
```

결과 배열에 사용할 키를 지정할 수도 있습니다.

```php
use Illuminate\Support\Arr;

$names = Arr::pluck($array, 'developer.name', 'developer.id');

// [1 => 'Taylor', 2 => 'Abigail']
```

<a name="method-array-prepend"></a>
#### `Arr::prepend()`

`Arr::prepend` 메서드는 배열의 맨 앞에 항목을 추가합니다.

```php
use Illuminate\Support\Arr;

$array = ['one', 'two', 'three', 'four'];

$array = Arr::prepend($array, 'zero');

// ['zero', 'one', 'two', 'three', 'four']
```

필요하다면 추가할 항목의 키를 지정할 수 있습니다.

```php
use Illuminate\Support\Arr;

$array = ['price' => 100];

$array = Arr::prepend($array, 'Desk', 'name');

// ['name' => 'Desk', 'price' => 100]
```

<a name="method-array-prependkeyswith"></a>
#### `Arr::prependKeysWith()`

`Arr::prependKeysWith` 메서드는 연관 배열의 모든 키에 지정한 접두어를 붙입니다.

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

`Arr::pull` 메서드는 배열에서 지정한 키-값 쌍을 반환함과 동시에 배열에서 해당 항목을 제거합니다.

```php
use Illuminate\Support\Arr;

$array = ['name' => 'Desk', 'price' => 100];

$name = Arr::pull($array, 'name');

// $name: Desk

// $array: ['price' => 100]
```

키가 존재하지 않을 경우, 세 번째 인수로 기본값을 지정하면 그 값이 반환됩니다.

```php
use Illuminate\Support\Arr;

$value = Arr::pull($array, $key, $default);
```

<a name="method-array-query"></a>
#### `Arr::query()`

`Arr::query` 메서드는 배열을 쿼리 문자열로 변환합니다.

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

`Arr::random` 메서드는 배열에서 임의의 값을 반환합니다.

```php
use Illuminate\Support\Arr;

$array = [1, 2, 3, 4, 5];

$random = Arr::random($array);

// 4 - (무작위로 반환됨)
```

두 번째 인수로 반환할 항목의 개수를 지정할 수도 있습니다. 이때 1개만 요청하더라도 결과는 배열 형태로 반환됩니다.

```php
use Illuminate\Support\Arr;

$items = Arr::random($array, 2);

// [2, 5] - (무작위로 반환됨)
```

<a name="method-array-reject"></a>
#### `Arr::reject()`

`Arr::reject` 메서드는 전달된 클로저를 사용해 조건에 맞는 항목을 배열에서 제거합니다.

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

`Arr::select` 메서드는 배열에서 지정한 키의 값만으로 이루어진 배열을 선택합니다.

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

`Arr::set` 메서드는 "dot" 표기법을 이용해 깊게 중첩된 배열 내에 값을 설정합니다.

```php
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

Arr::set($array, 'products.desk.price', 200);

// ['products' => ['desk' => ['price' => 200]]]
```

<a name="method-array-shuffle"></a>
#### `Arr::shuffle()`

`Arr::shuffle` 메서드는 배열의 항목들을 무작위로 섞어줍니다.

```php
use Illuminate\Support\Arr;

$array = Arr::shuffle([1, 2, 3, 4, 5]);

// [3, 2, 5, 1, 4] - (무작위로 생성됨)
```

<a name="method-array-sole"></a>
#### `Arr::sole()`

`Arr::sole` 메서드는 주어진 클로저(조건)에 부합하는 요소가 배열에 단 하나일 때, 해당 값을 반환합니다. 만약 두 개 이상 부합하는 값이 있으면 `Illuminate\Support\MultipleItemsFoundException` 예외가 발생하고, 아무 값도 없으면 `Illuminate\Support\ItemNotFoundException` 예외가 발생합니다.

```php
use Illuminate\Support\Arr;

$array = ['Desk', 'Table', 'Chair'];

$value = Arr::sole($array, fn (string $value) => $value === 'Desk');

// 'Desk'
```

<a name="method-array-sort"></a>
#### `Arr::sort()`

`Arr::sort` 메서드는 배열을 값 기준으로 정렬합니다.

```php
use Illuminate\Support\Arr;

$array = ['Desk', 'Table', 'Chair'];

$sorted = Arr::sort($array);

// ['Chair', 'Desk', 'Table']
```

지정한 클로저의 반환값을 기준으로 배열을 정렬할 수도 있습니다.

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

`Arr::sortDesc` 메서드는 배열을 값 기준으로 내림차순 정렬합니다.

```php
use Illuminate\Support\Arr;

$array = ['Desk', 'Table', 'Chair'];

$sorted = Arr::sortDesc($array);

// ['Table', 'Desk', 'Chair']
```

클로저의 반환값을 기준으로 내림차순 정렬할 수도 있습니다.

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

`Arr::sortRecursive` 메서드는 배열을 재귀적으로 정렬합니다. 숫자로 인덱싱된 하위 배열에는 `sort` 함수를, 연관 배열에는 `ksort` 함수를 사용하여 정렬합니다.

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

결과를 내림차순으로 정렬하고 싶다면 `Arr::sortRecursiveDesc` 메서드를 사용할 수 있습니다.

```php
$sorted = Arr::sortRecursiveDesc($array);
```

<a name="method-array-string"></a>
#### `Arr::string()`

`Arr::string` 메서드는 "닷(dot) 표기법"을 사용해 깊이 중첩된 배열에서 값을 가져옵니다([Arr::get()](#method-array-get)와 동일함). 단, 요청한 값이 `string`이 아닌 경우 `InvalidArgumentException`을 발생시킵니다.

```
use Illuminate\Support\Arr;

$array = ['name' => 'Joe', 'languages' => ['PHP', 'Ruby']];

$value = Arr::string($array, 'name');

// Joe

$value = Arr::string($array, 'languages');

// throws InvalidArgumentException
```

<a name="method-array-take"></a>
#### `Arr::take()`

`Arr::take` 메서드는 지정한 개수만큼의 아이템이 포함된 새 배열을 반환합니다.

```php
use Illuminate\Support\Arr;

$array = [0, 1, 2, 3, 4, 5];

$chunk = Arr::take($array, 3);

// [0, 1, 2]
```

음수 값을 지정하면, 배열의 끝에서부터 해당 개수만큼의 아이템을 가져옵니다.

```php
$array = [0, 1, 2, 3, 4, 5];

$chunk = Arr::take($array, -2);

// [4, 5]
```

<a name="method-array-to-css-classes"></a>
#### `Arr::toCssClasses()`

`Arr::toCssClasses` 메서드는 조건에 따라 CSS 클래스 문자열을 만듭니다. 이 메서드는 배열을 받아, 키에는 추가하고 싶은 클래스명을, 값에는 불린(boolean) 표현식을 적습니다. 배열 요소의 키가 숫자라면, 해당 클래스는 항상 결과 클래스 목록에 포함됩니다.

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

`Arr::toCssStyles` 메서드는 조건에 따라 CSS 스타일 문자열을 만듭니다. 방식은 `toCssClasses`와 동일하며, 배열의 키에 스타일 속성을, 값에 불린 표현식을 전달합니다. 숫자 키는 항상 결과에 포함됩니다.

```php
use Illuminate\Support\Arr;

$hasColor = true;

$array = ['background-color: blue', 'color: blue' => $hasColor];

$classes = Arr::toCssStyles($array);

/*
    'background-color: blue; color: blue;'
*/
```

이 메서드는 라라벨에서 [Blade 컴포넌트의 attribute bag에 클래스를 병합](/docs/12.x/blade#conditionally-merge-classes)하거나, `@class` [Blade 디렉티브](/docs/12.x/blade#conditional-classes)를 지원할 때 내부적으로 사용됩니다.

<a name="method-array-undot"></a>
#### `Arr::undot()`

`Arr::undot` 메서드는 "닷(dot) 표기법"을 사용한 1차원 배열을 다차원 배열로 확장합니다.

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

`Arr::where` 메서드는 제공된 클로저를 사용해 배열을 필터링합니다.

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

`Arr::whereNotNull` 메서드는 지정한 배열에서 모든 `null` 값을 제거합니다.

```php
use Illuminate\Support\Arr;

$array = [0, null];

$filtered = Arr::whereNotNull($array);

// [0 => 0]
```

<a name="method-array-wrap"></a>
#### `Arr::wrap()`

`Arr::wrap` 메서드는 전달된 값을 배열로 감쌉니다. 만약 값이 이미 배열이라면 그대로 반환합니다.

```php
use Illuminate\Support\Arr;

$string = 'Laravel';

$array = Arr::wrap($string);

// ['Laravel']
```

값이 `null`인 경우 빈 배열을 반환합니다.

```php
use Illuminate\Support\Arr;

$array = Arr::wrap(null);

// []
```

<a name="method-data-fill"></a>
#### `data_fill()`

`data_fill` 함수는 "닷(dot) 표기법"을 사용해 중첩된 배열 또는 객체에서 비어 있는 값을 지정합니다.

```php
$data = ['products' => ['desk' => ['price' => 100]]];

data_fill($data, 'products.desk.price', 200);

// ['products' => ['desk' => ['price' => 100]]]

data_fill($data, 'products.desk.discount', 10);

// ['products' => ['desk' => ['price' => 100, 'discount' => 10]]]
```

이 함수는 별표(*) 와일드카드도 지원하여 대상에 맞게 값을 채울 수 있습니다.

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

`data_get` 함수는 "닷(dot) 표기법"을 사용해 중첩된 배열이나 객체에서 값을 조회합니다.

```php
$data = ['products' => ['desk' => ['price' => 100]]];

$price = data_get($data, 'products.desk.price');

// 100
```

`data_get` 함수는 지정한 키를 찾지 못할 경우 반환할 기본값도 받을 수 있습니다.

```php
$discount = data_get($data, 'products.desk.discount', 0);

// 0
```

이 함수 또한 별표(*) 와일드카드를 지원하여 배열 또는 객체의 모든 키를 대상으로 값을 가져올 수 있습니다.

```php
$data = [
    'product-one' => ['name' => 'Desk 1', 'price' => 100],
    'product-two' => ['name' => 'Desk 2', 'price' => 150],
];

data_get($data, '*.name');

// ['Desk 1', 'Desk 2'];
```

`{first}`와 `{last}` 플레이스홀더를 사용하면 배열의 첫 번째 또는 마지막 아이템을 조회할 수 있습니다.

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

`data_set` 함수는 "닷(dot) 표기법"을 사용해 중첩된 배열이나 객체의 값을 지정합니다.

```php
$data = ['products' => ['desk' => ['price' => 100]]];

data_set($data, 'products.desk.price', 200);

// ['products' => ['desk' => ['price' => 200]]]
```

이 함수 역시 별표(*) 와일드카드를 지원하며, 대상 여러 곳에 값을 지정할 수 있습니다.

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

기본적으로 이미 값이 존재하면 덮어씁니다. 값이 없을 때만 지정하려면 함수의 네 번째 인자로 `false`를 전달하세요.

```php
$data = ['products' => ['desk' => ['price' => 100]]];

data_set($data, 'products.desk.price', 200, overwrite: false);

// ['products' => ['desk' => ['price' => 100]]]
```

<a name="method-data-forget"></a>
#### `data_forget()`

`data_forget` 함수는 "닷(dot) 표기법"을 사용해 중첩 배열이나 객체에서 값을 제거합니다.

```php
$data = ['products' => ['desk' => ['price' => 100]]];

data_forget($data, 'products.desk.price');

// ['products' => ['desk' => []]]
```

이 함수 역시 별표(*) 와일드카드를 지원하여 대상 여러 곳의 값을 한 번에 제거할 수 있습니다.

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

`head` 함수는 전달된 배열의 첫 번째 요소를 반환합니다.

```php
$array = [100, 200, 300];

$first = head($array);

// 100
```

<a name="method-last"></a>
#### `last()`

`last` 함수는 전달된 배열의 마지막 요소를 반환합니다.

```php
$array = [100, 200, 300];

$last = last($array);

// 300
```

<a name="numbers"></a>
## 숫자(Number)

<a name="method-number-abbreviate"></a>
#### `Number::abbreviate()`

`Number::abbreviate` 메서드는 숫자를 단위 축약형(human-readable) 형식으로 반환합니다.

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

`Number::clamp` 메서드는 지정한 범위 내에서만 숫자가 유지되도록 보장합니다. 숫자가 최솟값보다 작으면 최솟값을, 최댓값보다 크면 최댓값을 반환합니다.

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

`Number::currency` 메서드는 지정된 값을 문자열로 통화 형식으로 반환합니다.

```php
use Illuminate\Support\Number;

$currency = Number::currency(1000);

// $1,000.00

$currency = Number::currency(1000, in: 'EUR');

// €1,000.00

$currency = Number::currency(1000, in: 'EUR', locale: 'de');

// 1.000,00 €

$currency = Number::currency(1000, in: 'EUR', locale: 'de', precision: 0);

// 1.000 €
```

<a name="method-default-currency"></a>
#### `Number::defaultCurrency()`

`Number::defaultCurrency` 메서드는 `Number` 클래스에서 사용하는 기본 통화 정보를 반환합니다.

```php
use Illuminate\Support\Number;

$currency = Number::defaultCurrency();

// USD
```

<a name="method-default-locale"></a>
#### `Number::defaultLocale()`

`Number::defaultLocale` 메서드는 `Number` 클래스에서 사용하는 기본 로케일을 반환합니다.

```php
use Illuminate\Support\Number;

$locale = Number::defaultLocale();

// en
```

<a name="method-number-file-size"></a>
#### `Number::fileSize()`

`Number::fileSize` 메서드는 주어진 바이트(byte) 값을 파일 크기 문자열로 반환합니다.

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

`Number::forHumans` 메서드는 숫자를 사람이 읽기 쉬운(human-readable) 형식으로 반환합니다.

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

`Number::format` 메서드는 주어진 숫자를 로케일에 맞는 문자열로 포맷합니다.

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

`Number::ordinal` 메서드는 숫자의 서수(순위) 표기를 반환합니다.

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

`Number::pairs` 메서드는 지정한 범위와 스텝(step) 값에 따라 숫자 쌍(서브 구간)들의 배열을 생성합니다. 이 메서드는 큰 숫자 범위를 더 작고 관리하기 쉬운 서브 범위로 나누고 싶을 때(예: 페이지네이션, 작업 일괄 처리 등) 유용하게 사용할 수 있습니다. `pairs` 메서드는 각각 숫자 쌍(서브 구간)을 나타내는 배열로 구성된 배열을 반환합니다.

```php
use Illuminate\Support\Number;

$result = Number::pairs(25, 10);

// [[0, 9], [10, 19], [20, 25]]

$result = Number::pairs(25, 10, offset: 0);

// [[0, 10], [10, 20], [20, 25]]
```

<a name="method-number-percentage"></a>
#### `Number::percentage()`

`Number::percentage` 메서드는 주어진 값을 퍼센트(%) 형식의 문자열로 변환하여 반환합니다.

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

`Number::spell` 메서드는 주어진 숫자를 영어(또는 지정한 언어)의 단어 문자열로 변환해 줍니다.

```php
use Illuminate\Support\Number;

$number = Number::spell(102);

// one hundred and two

$number = Number::spell(88, locale: 'fr');

// quatre-vingt-huit
```

`after` 인자를 사용하면 지정한 값 이후의 모든 숫자는 숫자 그대로, 그 이전의 숫자만 단어로 변환하도록 할 수 있습니다.

```php
$number = Number::spell(10, after: 10);

// 10

$number = Number::spell(11, after: 10);

// eleven
```

`until` 인자를 사용하면 지정한 값 이전의 모든 숫자만 단어로 변환하고, 이후의 숫자는 숫자 그대로 반환합니다.

```php
$number = Number::spell(5, until: 10);

// five

$number = Number::spell(10, until: 10);

// 10
```

<a name="method-number-spell-ordinal"></a>
#### `Number::spellOrdinal()`

`Number::spellOrdinal` 메서드는 주어진 숫자를 영어 서수(순서를 나타내는 단어) 문자열로 반환합니다.

```php
use Illuminate\Support\Number;

$number = Number::spellOrdinal(1);

// first

$number = Number::spellOrdinal(2);

// second

$number = Number::spellOrdinal(21);

// twenty-first
```

<a name="method-number-trim"></a>
#### `Number::trim()`

`Number::trim` 메서드는 소수점 이하의 불필요한 0을 제거한 숫자 값을 반환합니다.

```php
use Illuminate\Support\Number;

$number = Number::trim(12.0);

// 12

$number = Number::trim(12.30);

// 12.3
```

<a name="method-number-use-locale"></a>
#### `Number::useLocale()`

`Number::useLocale` 메서드는 애플리케이션 전역의 기본 숫자 로케일(locale)을 지정합니다. 이후 `Number` 클래스의 메서드를 호출할 때 숫자와 통화 포맷 방식에 영향을 줍니다.

```php
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

`Number::withLocale` 메서드는 지정한 로케일(locale)로 주어진 클로저(익명 함수)를 실행한 후, 실행이 끝나면 원래의 로케일로 값을 복원합니다.

```php
use Illuminate\Support\Number;

$number = Number::withLocale('de', function () {
    return Number::format(1500);
});
```

<a name="method-number-use-currency"></a>
#### `Number::useCurrency()`

`Number::useCurrency` 메서드는 애플리케이션 전역의 기본 통화(currency)를 지정합니다. 이 설정 후 `Number` 클래스에서 통화 포맷을 사용할 때 영향을 줍니다.

```php
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

`Number::withCurrency` 메서드는 지정한 통화(currency)로 주어진 클로저를 실행한 후, 해당 클로저 실행이 끝나면 원래의 통화로 복원합니다.

```php
use Illuminate\Support\Number;

$number = Number::withCurrency('GBP', function () {
    // ...
});
```

<a name="paths"></a>
## 경로(Paths)

<a name="method-app-path"></a>
#### `app_path()`

`app_path` 함수는 애플리케이션의 `app` 디렉토리에 대한 전체 경로를 반환합니다. 또한, 이 함수에 파일 경로를 전달하여 `app` 디렉토리를 기준으로 하는 파일의 전체 경로를 생성할 수 있습니다.

```php
$path = app_path();

$path = app_path('Http/Controllers/Controller.php');
```

<a name="method-base-path"></a>
#### `base_path()`

`base_path` 함수는 애플리케이션의 루트 디렉토리(프로젝트 최상위 디렉토리) 경로를 반환합니다. 이 함수에 파일 이름이나 경로를 전달하면, 프로젝트 루트를 기준으로 해당 파일의 전체 경로를 생성합니다.

```php
$path = base_path();

$path = base_path('vendor/bin');
```

<a name="method-config-path"></a>
#### `config_path()`

`config_path` 함수는 애플리케이션의 `config` 디렉토리에 대한 전체 경로를 반환합니다. 이 함수에 파일 이름을 전달하면, 설정 디렉토리 내의 파일 전체 경로를 반환할 수 있습니다.

```php
$path = config_path();

$path = config_path('app.php');
```

<a name="method-database-path"></a>
#### `database_path()`

`database_path` 함수는 애플리케이션의 `database` 디렉토리 경로를 반환합니다. 또한 이 함수에 파일명을 전달하면, `database` 디렉토리내의 해당 파일 전체 경로를 알 수 있습니다.

```php
$path = database_path();

$path = database_path('factories/UserFactory.php');
```

<a name="method-lang-path"></a>
#### `lang_path()`

`lang_path` 함수는 애플리케이션의 `lang` 디렉토리 전체 경로를 반환합니다. 파일 경로를 함께 전달하면, 해당 lang 디렉토리 내 파일의 전체 경로를 생성할 수 있습니다.

```php
$path = lang_path();

$path = lang_path('en/messages.php');
```

> [!NOTE]
> 기본적으로 라라벨 애플리케이션 스캐폴딩에는 `lang` 디렉토리가 포함되어 있지 않습니다. 라라벨 언어 파일을 직접 커스터마이즈하려면 `lang:publish` 아티즌 명령어로 언어 파일을 공개(publish)할 수 있습니다.

<a name="method-mix"></a>
#### `mix()`

`mix` 함수는 [버전 관리된 Mix 파일](/docs/12.x/mix)의 경로를 반환합니다.

```php
$path = mix('css/app.css');
```

<a name="method-public-path"></a>
#### `public_path()`

`public_path` 함수는 애플리케이션의 `public` 디렉토리 전체 경로를 반환합니다. 이 함수에 파일명을 전달하면 public 디렉토리 내 특정 파일의 전체 경로를 알 수 있습니다.

```php
$path = public_path();

$path = public_path('css/app.css');
```

<a name="method-resource-path"></a>
#### `resource_path()`

`resource_path` 함수는 애플리케이션의 `resources` 디렉토리 전체 경로를 반환합니다. 또한, 이 함수에 파일 경로를 전달하여 리소스 디렉토리의 파일 전체 경로를 생성할 수 있습니다.

```php
$path = resource_path();

$path = resource_path('sass/app.scss');
```

<a name="method-storage-path"></a>
#### `storage_path()`

`storage_path` 함수는 애플리케이션의 `storage` 디렉토리의 전체 경로를 반환합니다. 이 함수에 파일명을 전달하여 해당 스토리지 내의 파일 전체 경로를 얻을 수 있습니다.

```php
$path = storage_path();

$path = storage_path('app/file.txt');
```

<a name="urls"></a>
## URL

<a name="method-action"></a>
#### `action()`

`action` 함수는 지정한 컨트롤러 액션의 URL을 생성합니다.

```php
use App\Http\Controllers\HomeController;

$url = action([HomeController::class, 'index']);
```

컨트롤러 메서드가 라우트 파라미터를 받는 경우, 두 번째 인수로 파라미터 배열을 전달할 수 있습니다.

```php
$url = action([UserController::class, 'profile'], ['id' => 1]);
```

<a name="method-asset"></a>
#### `asset()`

`asset` 함수는 현재 요청의 스킴(HTTP 또는 HTTPS)을 사용하여 에셋(asset)의 URL을 생성합니다.

```php
$url = asset('img/photo.jpg');
```

`.env` 파일에서 `ASSET_URL` 변수를 설정하여 에셋의 URL 호스트를 변경할 수 있습니다. Amazon S3나 다른 CDN 등 외부 서비스를 통해 에셋을 호스팅할 때 유용하게 사용할 수 있습니다.

```php
// ASSET_URL=http://example.com/assets

$url = asset('img/photo.jpg'); // http://example.com/assets/img/photo.jpg
```

<a name="method-route"></a>
#### `route()`

`route` 함수는 지정한 [이름 있는 라우트](/docs/12.x/routing#named-routes)의 URL을 생성합니다.

```php
$url = route('route.name');
```

라우트가 파라미터를 받는 경우, 두 번째 인수로 파라미터 배열을 전달할 수 있습니다.

```php
$url = route('route.name', ['id' => 1]);
```

기본적으로 `route` 함수는 절대 URL을 생성합니다. 만약 상대 URL을 생성하고 싶다면 세 번째 인수로 `false`를 전달하세요.

```php
$url = route('route.name', ['id' => 1], false);
```

<a name="method-secure-asset"></a>
#### `secure_asset()`

`secure_asset` 함수는 HTTPS를 사용하여 에셋(asset)의 URL을 생성합니다.

```php
$url = secure_asset('img/photo.jpg');
```

<a name="method-secure-url"></a>
#### `secure_url()`

`secure_url` 함수는 지정한 경로에 대해 완전한 HTTPS URL을 생성합니다. 추가적인 URL 세그먼트는 두 번째 인수로 배열 형태로 전달할 수 있습니다.

```php
$url = secure_url('user/profile');

$url = secure_url('user/profile', [1]);
```

<a name="method-to-route"></a>
#### `to_route()`

`to_route` 함수는 지정한 [이름 있는 라우트](/docs/12.x/routing#named-routes)로 [리다이렉트 HTTP 응답](/docs/12.x/responses#redirects)을 생성합니다.

```php
return to_route('users.show', ['user' => 1]);
```

필요하다면, 리다이렉트에 사용할 HTTP 상태 코드와 추가적인 응답 헤더를 세 번째, 네 번째 인수로 전달할 수도 있습니다.

```php
return to_route('users.show', ['user' => 1], 302, ['X-Framework' => 'Laravel']);
```

<a name="method-uri"></a>
#### `uri()`

`uri` 함수는 지정한 URI에 대해 [플루언트(유연한) URI 인스턴스](#uri)를 생성합니다.

```php
$uri = uri('https://example.com')
    ->withPath('/users')
    ->withQuery(['page' => 1])
```

`uri` 함수에 컨트롤러와 메서드 쌍이 담긴 배열을 전달하면, 해당 컨트롤러 메서드의 라우트 경로에 대한 `Uri` 인스턴스를 생성합니다.

```php
use App\Http\Controllers\UserController;

$uri = uri([UserController::class, 'show'], ['user' => $user])
```

컨트롤러가 invokable(호출 가능)하다면 클래스명만 전달해도 됩니다.

```php
use App\Http\Controllers\UserIndexController;

$uri = uri(UserIndexController::class);
```

`uri` 함수에 전달된 값이 [이름 있는 라우트](/docs/12.x/routing#named-routes)의 이름과 일치한다면, 해당 라우트 경로에 대한 `Uri` 인스턴스가 생성됩니다.

```php
$uri = uri('users.show', ['user' => $user]);
```

<a name="method-url"></a>
#### `url()`

`url` 함수는 지정한 경로에 대한 완전한 URL을 생성합니다.

```php
$url = url('user/profile');

$url = url('user/profile', [1]);
```

경로를 지정하지 않으면, `Illuminate\Routing\UrlGenerator` 인스턴스가 반환됩니다.

```php
$current = url()->current();

$full = url()->full();

$previous = url()->previous();
```

<a name="miscellaneous"></a>
## 기타(Miscellaneous)

<a name="method-abort"></a>
#### `abort()`

`abort` 함수는 [HTTP 예외](/docs/12.x/errors#http-exceptions)를 발생시키며, 이는 [예외 핸들러](/docs/12.x/errors#handling-exceptions)에 의해 렌더링됩니다.

```php
abort(403);
```

예외 메시지와 사용자 정의 HTTP 응답 헤더를 추가로 전달할 수도 있습니다.

```php
abort(403, 'Unauthorized.', $headers);
```

<a name="method-abort-if"></a>
#### `abort_if()`

`abort_if` 함수는 주어진 불리언 표현식이 `true`가 되면 HTTP 예외를 발생시킵니다.

```php
abort_if(! Auth::user()->isAdmin(), 403);
```

`abort` 메서드와 마찬가지로, 세 번째 인수로 응답 텍스트, 네 번째 인수로 사용자 정의 응답 헤더 배열을 전달할 수 있습니다.

<a name="method-abort-unless"></a>
#### `abort_unless()`

`abort_unless` 함수는 주어진 불리언 표현식이 `false`일 때 HTTP 예외를 발생시킵니다.

```php
abort_unless(Auth::user()->isAdmin(), 403);
```

`abort` 메서드와 마찬가지로, 세 번째 인수로 응답 텍스트, 네 번째 인수로 사용자 정의 응답 헤더 배열을 전달할 수 있습니다.

<a name="method-app"></a>
#### `app()`

`app` 함수는 [서비스 컨테이너](/docs/12.x/container) 인스턴스를 반환합니다.

```php
$container = app();
```

클래스명 혹은 인터페이스명을 전달해 해당 객체를 컨테이너에서 바로 resolve(해결)할 수도 있습니다.

```php
$api = app('HelpSpot\API');
```

<a name="method-auth"></a>
#### `auth()`

`auth` 함수는 [인증자(authenticator)](/docs/12.x/authentication) 인스턴스를 반환합니다. `Auth` 파사드 대신 사용할 수 있습니다.

```php
$user = auth()->user();
```

필요하다면 접근하고자 하는 가드 이름을 지정할 수도 있습니다.

```php
$user = auth('admin')->user();
```

<a name="method-back"></a>
#### `back()`

`back` 함수는 사용자의 이전 위치로 [리다이렉트 HTTP 응답](/docs/12.x/responses#redirects)을 생성합니다.

```php
return back($status = 302, $headers = [], $fallback = '/');

return back();
```

<a name="method-bcrypt"></a>
#### `bcrypt()`

`bcrypt` 함수는 [Bcrypt](/docs/12.x/hashing)를 사용하여 주어진 값을 해싱합니다. `Hash` 파사드의 대체 방법으로 사용할 수 있습니다.

```php
$password = bcrypt('my-secret-password');
```

<a name="method-blank"></a>
#### `blank()`

`blank` 함수는 전달된 값이 "비어있는 값(blank)"인지 판별합니다.

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

`blank`와 반대로 동작하는 함수는 [filled](#method-filled) 메서드를 참고하세요.

<a name="method-broadcast"></a>
#### `broadcast()`

`broadcast` 함수는 전달한 [이벤트](/docs/12.x/events)를 [브로드캐스트](/docs/12.x/broadcasting)합니다.

```php
broadcast(new UserRegistered($user));

broadcast(new UserRegistered($user))->toOthers();
```

<a name="method-cache"></a>
#### `cache()`

`cache` 함수는 [캐시](/docs/12.x/cache)에서 값을 가져올 때 사용할 수 있습니다. 주어진 키가 캐시에 존재하지 않으면, 선택적으로 기본 값을 반환합니다.

```php
$value = cache('key');

$value = cache('key', 'default');
```

키/값 쌍의 배열을 전달하면 캐시에 항목을 저장할 수 있으며, 캐시 유효 기간(초 단위 또는 시간 객체)을 두 번째 인자로 지정해야 합니다.

```php
cache(['key' => 'value'], 300);

cache(['key' => 'value'], now()->addSeconds(10));
```

<a name="method-class-uses-recursive"></a>

#### `class_uses_recursive()`

`class_uses_recursive` 함수는 지정한 클래스가 사용하는 모든 트레이트(trait)를 반환합니다. 여기에는 부모 클래스가 사용하는 트레이트도 모두 포함됩니다.

```php
$traits = class_uses_recursive(App\Models\User::class);
```

<a name="method-collect"></a>
#### `collect()`

`collect` 함수는 전달된 값으로부터 [컬렉션](/docs/12.x/collections) 인스턴스를 생성합니다.

```php
$collection = collect(['taylor', 'abigail']);
```

<a name="method-config"></a>
#### `config()`

`config` 함수는 [설정](/docs/12.x/configuration) 변수의 값을 가져옵니다. 설정 값은 "도트(dot) 표기법"을 사용하여 접근할 수 있으며, 여기에는 파일명과 접근하려는 옵션을 포함합니다. 만약 해당 설정 옵션이 존재하지 않을 경우 반환할 기본값을 지정할 수 있습니다.

```php
$value = config('app.timezone');

$value = config('app.timezone', $default);
```

배열 형태의 키/값 쌍을 전달하여 런타임에 설정 값을 지정할 수도 있습니다. 단, 이 함수는 현재 요청에서만 설정 값을 변경하며 실제 설정 파일이 수정되지는 않습니다.

```php
config(['app.debug' => true]);
```

<a name="method-context"></a>
#### `context()`

`context` 함수는 [현재 컨텍스트](/docs/12.x/context)에서 값을 가져옵니다. 인자로 존재하지 않는 컨텍스트 키를 전달하면, 두 번째 인자로 기본값을 지정해 반환받을 수 있습니다.

```php
$value = context('trace_id');

$value = context('trace_id', $default);
```

배열 형태의 키/값 쌍을 전달하여 컨텍스트 값을 직접 지정할 수도 있습니다.

```php
use Illuminate\Support\Str;

context(['trace_id' => Str::uuid()->toString()]);
```

<a name="method-cookie"></a>
#### `cookie()`

`cookie` 함수는 새로운 [쿠키](/docs/12.x/requests#cookies) 인스턴스를 생성합니다.

```php
$cookie = cookie('name', 'value', $minutes);
```

<a name="method-csrf-field"></a>
#### `csrf_field()`

`csrf_field` 함수는 CSRF 토큰 값을 갖는 HTML `hidden` 입력 필드를 생성합니다. 예를 들어, [Blade 구문](/docs/12.x/blade)에서는 다음과 같이 사용할 수 있습니다.

```blade
{{ csrf_field() }}
```

<a name="method-csrf-token"></a>
#### `csrf_token()`

`csrf_token` 함수는 현재 CSRF 토큰의 값을 반환합니다.

```php
$token = csrf_token();
```

<a name="method-decrypt"></a>
#### `decrypt()`

`decrypt` 함수는 지정한 값을 [복호화](/docs/12.x/encryption)합니다. 이 함수는 `Crypt` 파사드의 대체로 사용할 수 있습니다.

```php
$password = decrypt($value);
```

<a name="method-dd"></a>
#### `dd()`

`dd` 함수는 지정한 변수들의 값을 출력(dump)한 후, 즉시 스크립트 실행을 중단합니다.

```php
dd($value);

dd($value1, $value2, $value3, ...);
```

스크립트 실행을 중단하지 않고 단순히 변수만 출력하려면 [dump](#method-dump) 함수를 사용하십시오.

<a name="method-dispatch"></a>
#### `dispatch()`

`dispatch` 함수는 지정한 [잡(job)](/docs/12.x/queues#creating-jobs)을 라라벨 [잡 큐](/docs/12.x/queues)에 푸시(push)합니다.

```php
dispatch(new App\Jobs\SendEmails);
```

<a name="method-dispatch-sync"></a>
#### `dispatch_sync()`

`dispatch_sync` 함수는 지정한 잡(job)을 [동기(sync)](/docs/12.x/queues#synchronous-dispatching) 큐로 보내 즉시 처리되도록 합니다.

```php
dispatch_sync(new App\Jobs\SendEmails);
```

<a name="method-dump"></a>
#### `dump()`

`dump` 함수는 지정한 변수의 값을 출력(dump)합니다.

```php
dump($value);

dump($value1, $value2, $value3, ...);
```

변수 출력 후 스크립트 실행을 중단하려면 [dd](#method-dd) 함수를 사용하십시오.

<a name="method-encrypt"></a>
#### `encrypt()`

`encrypt` 함수는 지정한 값을 [암호화](/docs/12.x/encryption)합니다. 이 함수는 `Crypt` 파사드의 대체로 사용할 수 있습니다.

```php
$secret = encrypt('my-secret-value');
```

<a name="method-env"></a>
#### `env()`

`env` 함수는 [환경 변수](/docs/12.x/configuration#environment-configuration)의 값을 반환하거나, 존재하지 않을 경우 기본값을 반환합니다.

```php
$env = env('APP_ENV');

$env = env('APP_ENV', 'production');
```

> [!WARNING]
> 배포 과정 중에 `config:cache` 명령어를 실행하는 경우, `env` 함수를 반드시 구성 파일 내에서만 호출해야 합니다. 구성 파일이 캐시되면 `.env` 파일이 더 이상 로드되지 않으며, 모든 `env` 함수 호출은 `null`을 반환합니다.

<a name="method-event"></a>
#### `event()`

`event` 함수는 지정한 [이벤트](/docs/12.x/events)를 해당 리스너로 디스패치(dispatch)합니다.

```php
event(new UserRegistered($user));
```

<a name="method-fake"></a>
#### `fake()`

`fake` 함수는 컨테이너에서 [Faker](https://github.com/FakerPHP/Faker) 싱글톤(singleton)을 해결(resolve)합니다. 이 기능은 모델 팩토리, 데이터베이스 시딩, 테스트, 뷰 프로토타입 등에서 가짜 데이터를 생성할 때 유용합니다.

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

기본적으로 `fake` 함수는 `config/app.php`의 `app.faker_locale` 설정 옵션을 사용하며, 보통 이 값은 `APP_FAKER_LOCALE` 환경 변수로 지정됩니다. 직접 로케일(locale)을 지정하려면 `fake` 함수의 인자로 전달할 수 있습니다. 각 로케일은 별도의 싱글톤 인스턴스를 제공합니다.

```php
fake('nl_NL')->name()
```

<a name="method-filled"></a>
#### `filled()`

`filled` 함수는 전달된 값이 "비어 있지 않은지"를 확인합니다.

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

`filled`와 반대 동작이 필요한 경우, [blank](#method-blank) 메서드를 참고하세요.

<a name="method-info"></a>
#### `info()`

`info` 함수는 애플리케이션의 [로그](/docs/12.x/logging)에 정보성(informational) 메시지를 기록합니다.

```php
info('Some helpful information!');
```

함수에 맥락 정보를 담은 배열도 함께 전달할 수 있습니다.

```php
info('User login attempt failed.', ['id' => $user->id]);
```

<a name="method-literal"></a>
#### `literal()`

`literal` 함수는 지정한 이름 있는 인수(name argument)들을 속성(property)으로 갖는 새로운 [stdClass](https://www.php.net/manual/en/class.stdclass.php) 인스턴스를 생성합니다.

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

`logger` 함수는 `debug` 레벨로 [로그](/docs/12.x/logging)에 메시지를 기록할 수 있습니다.

```php
logger('Debug message');
```

맥락 정보를 담은 배열도 함께 전달할 수 있습니다.

```php
logger('User has logged in.', ['id' => $user->id]);
```

함수에 값을 전달하지 않으면 [logger](/docs/12.x/logging) 인스턴스를 반환합니다.

```php
logger()->error('You are not allowed here.');
```

<a name="method-method-field"></a>
#### `method_field()`

`method_field` 함수는 폼(form)의 HTTP 메서드(HTTP verb)를 속이는 값을 갖는 HTML `hidden` 입력 필드를 생성합니다. 예를 들어, [Blade 문법](/docs/12.x/blade)에서는 다음과 같이 사용할 수 있습니다.

```blade
<form method="POST">
    {{ method_field('DELETE') }}
</form>
```

<a name="method-now"></a>
#### `now()`

`now` 함수는 현재 시간을 기반으로 새로운 `Illuminate\Support\Carbon` 인스턴스를 생성합니다.

```php
$now = now();
```

<a name="method-old"></a>
#### `old()`

`old` 함수는 세션에 플래시된 [이전 입력값(old input)](/docs/12.x/requests#old-input)을 [조회](/docs/12.x/requests#retrieving-input)합니다.

```php
$value = old('value');

$value = old('value', 'default');
```

`old` 함수의 두 번째 인자인 "기본값"은 종종 Eloquent 모델의 속성일 수 있기 때문에, 라라벨에서는 전체 Eloquent 모델을 두 번째 인자로 바로 전달할 수도 있습니다. 이 경우, 라라벨은 첫 번째 인수를 "기본값"으로 삼을 Eloquent 속성명(attribute name)으로 간주합니다.

```blade
{{ old('name', $user->name) }}

// 위와 동일하게 동작

{{ old('name', $user) }}
```

<a name="method-once"></a>
#### `once()`

`once` 함수는 지정한 콜백을 한 번만 실행하고, 해당 요청 내에서 결과를 메모리에 캐시합니다. 같은 콜백을 전달한 이후의 호출에서는 항상 이전에 캐시된 결과가 반환됩니다.

```php
function random(): int
{
    return once(function () {
        return random_int(1, 1000);
    });
}

random(); // 123
random(); // 123 (캐시된 결과)
random(); // 123 (캐시된 결과)
```

객체 인스턴스 내에서 `once` 함수를 실행할 경우, 각 객체 인스턴스마다 별도의 캐시가 적용됩니다.

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
$service->all(); // (캐시된 결과)

$secondService = new NumberService;

$secondService->all();
$secondService->all(); // (캐시된 결과)
```
<a name="method-optional"></a>
#### `optional()`

`optional` 함수는 어떤 인수든 받아 해당 객체의 속성이나 메서드에 접근할 수 있게 해줍니다. 만약 전달된 객체가 `null`이면, 속성이나 메서드에 접근하더라도 오류 대신 `null`을 반환합니다.

```php
return optional($user->address)->street;

{!! old('name', optional($user)->name) !!}
```

`optional` 함수는 두 번째 인수로 클로저도 받을 수 있습니다. 첫 번째 인수가 null이 아니면 해당 클로저가 호출됩니다.

```php
return optional(User::find($id), function (User $user) {
    return $user->name;
});
```

<a name="method-policy"></a>
#### `policy()`

`policy` 메서드는 지정한 클래스에 대한 [정책 객체(policy)](/docs/12.x/authorization#creating-policies) 인스턴스를 반환합니다.

```php
$policy = policy(App\Models\User::class);
```

<a name="method-redirect"></a>
#### `redirect()`

`redirect` 함수는 [리디렉션 HTTP 응답](/docs/12.x/responses#redirects)을 반환하거나, 인수를 전달하지 않으면 리디렉터 인스턴스를 반환합니다.

```php
return redirect($to = null, $status = 302, $headers = [], $https = null);

return redirect('/home');

return redirect()->route('route.name');
```

<a name="method-report"></a>
#### `report()`

`report` 함수는 지정한 예외(Exception)를 [예외 핸들러](/docs/12.x/errors#handling-exceptions)에 따라 보고합니다.

```php
report($e);
```

`report` 함수는 문자열도 인수로 받을 수 있습니다. 문자열을 전달하면 해당 문자열을 메시지로 하는 예외가 생성되어 보고됩니다.

```php
report('Something went wrong.');
```

<a name="method-report-if"></a>
#### `report_if()`

`report_if` 함수는 첫 번째 인수로 조건이 `true`일 경우 [예외 핸들러](/docs/12.x/errors#handling-exceptions)에 예외를 보고합니다.

```php
report_if($shouldReport, $e);

report_if($shouldReport, 'Something went wrong.');
```

<a name="method-report-unless"></a>
#### `report_unless()`

`report_unless` 함수는 첫 번째 인수로 조건이 `false`일 경우 [예외 핸들러](/docs/12.x/errors#handling-exceptions)에 예외를 보고합니다.

```php
report_unless($reportingDisabled, $e);

report_unless($reportingDisabled, 'Something went wrong.');
```

<a name="method-request"></a>
#### `request()`

`request` 함수는 현재 [요청](/docs/12.x/requests) 인스턴스를 반환하거나, 현재 요청에서 입력값을 조회할 수 있습니다.

```php
$request = request();

$value = request('key', $default);
```

<a name="method-rescue"></a>
#### `rescue()`

`rescue` 함수는 주어진 클로저를 실행하고, 실행 중 발생하는 예외를 캐치하여 처리합니다. 캐치된 모든 예외는 [예외 핸들러](/docs/12.x/errors#handling-exceptions)로 전송되며, 요청 처리는 계속 진행됩니다.

```php
return rescue(function () {
    return $this->method();
});
```

`rescue` 함수에 두 번째 인수를 전달하여, 클로저 실행 중 예외가 발생하면 반환할 "기본값"을 지정할 수 있습니다.

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

`rescue` 함수의 `report` 인수로, 해당 예외를 `report` 함수로 보고할지 여부를 결정할 수 있습니다.

```php
return rescue(function () {
    return $this->method();
}, report: function (Throwable $throwable) {
    return $throwable instanceof InvalidArgumentException;
});
```

<a name="method-resolve"></a>
#### `resolve()`

`resolve` 함수는 [서비스 컨테이너](/docs/12.x/container)를 이용해 지정한 클래스 또는 인터페이스 명을 인스턴스로 해결(resolve)합니다.

```php
$api = resolve('HelpSpot\API');
```

<a name="method-response"></a>
#### `response()`

`response` 함수는 [응답(Response)](/docs/12.x/responses) 인스턴스를 생성하거나, 응답 팩토리 인스턴스를 반환합니다.

```php
return response('Hello World', 200, $headers);

return response()->json(['foo' => 'bar'], 200, $headers);
```

<a name="method-retry"></a>
#### `retry()`

`retry` 함수는 지정한 최대 횟수까지 콜백을 재시도하며 실행합니다. 콜백이 예외를 던지지 않으면 그 반환값이 반환됩니다. 예외가 발생하면 자동으로 재시도되며, 최대 횟수를 초과하면 예외가 던져집니다.

```php
return retry(5, function () {
    // 5번 시도, 각 시도 사이에 100ms 대기...
}, 100);
```

시도 간 대기할 밀리초(ms) 값을 직접 계산하여 동적으로 지정하고 싶다면, 세 번째 인수로 클로저를 전달할 수 있습니다.

```php
use Exception;

return retry(5, function () {
    // ...
}, function (int $attempt, Exception $exception) {
    return $attempt * 100;
});
```

간편하게 첫 번째 인수에 배열을 전달하면 각 시도별로 대기할 밀리초를 지정할 수 있습니다.

```php
return retry([100, 200], function () {
    // 첫 번째 재시도에는 100ms, 두 번째에는 200ms 대기...
});
```

특정 조건이 충족될 때만 재시도하고 싶다면 네 번째 인수로 클로저를 전달할 수 있습니다.

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

`session` 함수는 [세션](/docs/12.x/session)의 값을 조회하거나, 값을 설정할 때 사용할 수 있습니다.

```php
$value = session('key');
```

배열 형태의 키/값 쌍을 함수에 전달하여 값을 저장할 수도 있습니다.

```php
session(['chairs' => 7, 'instruments' => 3]);
```

값을 전달하지 않으면 세션 스토어 인스턴스가 반환됩니다.

```php
$value = session()->get('key');

session()->put('key', $value);
```

<a name="method-tap"></a>
#### `tap()`

`tap` 함수는 두 개의 인수, 즉 임의의 `$value`와 클로저를 받습니다. `$value`는 클로저에 전달된 후, 다시 `tap` 함수의 반환값으로 그대로 전달됩니다. 클로저의 반환값은 무시됩니다.

```php
$user = tap(User::first(), function (User $user) {
    $user->name = 'taylor';

    $user->save();
});
```

클로저를 전달하지 않으면, `$value`에 메서드 체이닝을 할 수 있습니다. 이때 호출한 메서드의 실제 반환값과 상관없이 항상 `$value`가 반환됩니다. 예를 들어, Eloquent의 `update` 메서드는 일반적으로 정수를 반환하지만, `tap` 함수와 함께 호출하면 모델 인스턴스가 그대로 반환됩니다.

```php
$user = tap($user)->update([
    'name' => $name,
    'email' => $email,
]);
```

클래스에 `tap` 메서드를 추가하려면 `Illuminate\Support\Traits\Tappable` 트레이트를 해당 클래스에 선언하면 됩니다. 이 트레이트의 `tap` 메서드는 오직 클로저만 인수로 받으며, 인스턴스 자신이 클로저에 전달된 후 반환됩니다.

```php
return $user->tap(function (User $user) {
    // ...
});
```

<a name="method-throw-if"></a>

#### `throw_if()`

`throw_if` 함수는 주어진 불리언 값이 `true`일 때 지정된 예외를 발생시킵니다.

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

`throw_unless` 함수는 주어진 불리언 값이 `false`일 때 지정된 예외를 발생시킵니다.

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

`today` 함수는 현재 날짜를 기준으로 새로운 `Illuminate\Support\Carbon` 인스턴스를 생성합니다.

```php
$today = today();
```

<a name="method-trait-uses-recursive"></a>
#### `trait_uses_recursive()`

`trait_uses_recursive` 함수는 지정된 트레이트가 사용하는 모든 트레이트 목록을 반환합니다.

```php
$traits = trait_uses_recursive(\Illuminate\Notifications\Notifiable::class);
```

<a name="method-transform"></a>
#### `transform()`

`transform` 함수는 주어진 값이 [blank](#method-blank)하지 않은 경우, 클로저를 실행한 후 그 반환값을 반환합니다.

```php
$callback = function (int $value) {
    return $value * 2;
};

$result = transform(5, $callback);

// 10
```

함수의 세 번째 인수로 기본값 또는 클로저를 전달할 수 있습니다. 만약 전달된 값이 blank라면 이 값이 반환됩니다.

```php
$result = transform(null, $callback, 'The value is blank');

// The value is blank
```

<a name="method-validator"></a>
#### `validator()`

`validator` 함수는 전달된 인수를 이용하여 새로운 [validator](/docs/12.x/validation) 인스턴스를 생성합니다. `Validator` 파사드의 대체 방법으로 사용할 수 있습니다.

```php
$validator = validator($data, $rules, $messages);
```

<a name="method-value"></a>
#### `value()`

`value` 함수는 전달된 값을 그대로 반환합니다. 하지만, 만약 함수에 클로저를 전달한다면, 그 클로저를 실행하고 그 결과값을 반환합니다.

```php
$result = value(true);

// true

$result = value(function () {
    return false;
});

// false
```

`value` 함수에는 추가로 인수를 넘길 수 있습니다. 첫 번째 인수로 클로저를 전달하면, 추가 인수들이 클로저의 인수로 전달됩니다. 만약 첫 번째 인수가 클로저가 아닐 경우, 추가 인수는 무시됩니다.

```php
$result = value(function (string $name) {
    return $name;
}, 'Taylor');

// 'Taylor'
```

<a name="method-view"></a>
#### `view()`

`view` 함수는 [뷰](/docs/12.x/views) 인스턴스를 반환합니다.

```php
return view('auth.login');
```

<a name="method-with"></a>
#### `with()`

`with` 함수는 전달된 값을 그대로 반환합니다. 만약 두 번째 인수로 클로저가 전달되면, 그 클로저를 실행하고 반환값을 반환합니다.

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

`when` 함수는 조건이 `true`일 때 전달된 값을 반환하고, 그렇지 않으면 `null`을 반환합니다. 클로저를 두 번째 인수로 전달하면, 클로저가 실행되고 그 결과값을 반환합니다.

```php
$value = when(true, 'Hello World');

$value = when(true, fn () => 'Hello World');
```

`when` 함수는 주로 HTML 속성을 조건부로 렌더링할 때 유용합니다.

```blade
<div {!! when($condition, 'wire:poll="calculate"') !!}>
    ...
</div>
```

<a name="other-utilities"></a>
## 기타 유틸리티

<a name="benchmarking"></a>
### 벤치마킹

애플리케이션의 특정 부분의 성능을 빠르게 테스트해보고자 할 때가 있습니다. 이런 경우, `Benchmark` 지원 클래스를 사용해서 특정 콜백이 완료되는 데 걸리는 밀리초(ms) 시간을 측정할 수 있습니다.

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

기본적으로, 전달된 콜백들은 한 번(1회) 실행되고, 실행에 걸린 시간이 브라우저 또는 콘솔에 표시됩니다.

콜백을 여러 번 실행하고 싶다면, 그 횟수를 두 번째 인수로 지정할 수 있습니다. 여러 번 실행할 경우, `Benchmark` 클래스는 전체 반복 동안 콜백을 실행하는 데 평균적으로 걸린 시간을 반환합니다.

```php
Benchmark::dd(fn () => User::count(), iterations: 10); // 0.5 ms
```

콜백의 반환값을 받으면서 실행 시간을 측정하고 싶을 때도 있습니다. `value` 메서드는 콜백의 반환값과 실행에 걸린 시간을 튜플로 반환합니다.

```php
[$count, $duration] = Benchmark::value(fn () => User::count());
```

<a name="dates"></a>
### 날짜와 시간

라라벨에는 [Carbon](https://carbon.nesbot.com/docs/)이라는 강력한 날짜/시간 처리 라이브러리가 내장되어 있습니다. 새로운 `Carbon` 인스턴스를 만들려면, `now` 함수를 호출하면 됩니다. 이 함수는 라라벨 애플리케이션 전체에서 전역적으로 사용할 수 있습니다.

```php
$now = now();
```

또는, `Illuminate\Support\Carbon` 클래스를 이용해 직접 인스턴스를 만들 수도 있습니다.

```php
use Illuminate\Support\Carbon;

$now = Carbon::now();
```

Carbon 및 그 기능에 대한 자세한 설명은 [공식 Carbon 문서](https://carbon.nesbot.com/docs/)를 참고하시기 바랍니다.

<a name="deferred-functions"></a>
### 지연 함수(Deferred Functions)

라라벨의 [큐 작업](/docs/12.x/queues)은 작업을 백그라운드로 처리하는 데 사용되지만, 간단한 작업을 별도의 큐 워커 설정 없이 요청 응답 이후로 미루고 싶을 때도 있습니다.

지연 함수(Deferred function)는 클로저의 실행을 HTTP 응답이 사용자에게 전송된 이후로 미뤄서 애플리케이션의 응답 속도를 빠르게 느끼도록 해줍니다. 클로저 실행을 지연하려면, 단순히 해당 클로저를 `Illuminate\Support\defer` 함수에 전달하면 됩니다.

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

기본적으로, `Illuminate\Support\defer`를 통해 등록된 지연 함수는 HTTP 응답, Artisan 명령, 큐 작업이 정상적으로 완료될 때만 실행됩니다. 즉, 요청이 `4xx` 또는 `5xx` HTTP 응답으로 끝나면 지연 함수는 실행되지 않습니다. 항상 지연 함수가 실행되도록 하려면, 지연 함수에 `always` 메서드를 체이닝하면 됩니다.

```php
defer(fn () => Metrics::reportOrder($order))->always();
```

<a name="cancelling-deferred-functions"></a>
#### 지연 함수 취소하기

실행 전에 지연 함수를 취소해야 할 때는, 해당 함수의 이름을 지정해서 `forget` 메서드를 사용할 수 있습니다. 지연 함수에 이름을 지정하려면 `Illuminate\Support\defer` 함수의 두 번째 인수로 이름을 전달하면 됩니다.

```php
defer(fn () => Metrics::report(), 'reportMetrics');

defer()->forget('reportMetrics');
```

<a name="disabling-deferred-functions-in-tests"></a>
#### 테스트에서 지연 함수 비활성화하기

테스트 코드를 작성할 때는 지연 함수를 비활성화하는 것이 유용할 수 있습니다. 테스트 내에서 `withoutDefer`를 호출하면, 라라벨은 모든 지연 함수를 즉시 실행합니다.

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

테스트 케이스 전체에서 지연 함수를 비활성화하려면, 기본 `TestCase` 클래스의 `setUp` 메서드에서 `withoutDefer`를 호출합니다.

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
### Lottery

라라벨의 Lottery 클래스는 지정된 확률에 따라 콜백을 실행할 수 있도록 해줍니다. 이를 통해 전체 요청의 일부 비율에만 특정 코드를 실행할 수 있습니다.

```php
use Illuminate\Support\Lottery;

Lottery::odds(1, 20)
    ->winner(fn () => $user->won())
    ->loser(fn () => $user->lost())
    ->choose();
```

라라벨의 Lottery 클래스는 다른 기능과도 결합할 수 있습니다. 예를 들어, 느린 쿼리에 대한 보고 작업을 일부 요청에만 실행하고 싶을 때 Lottery 클래스를 활용할 수 있습니다. 또한 Lottery 클래스 자체가 호출 가능한(callable) 객체이므로, 콜러블을 받을 수 있는 모든 메서드에 사용할 수 있습니다.

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
#### Lottery 테스트하기

라라벨에서는 Lottery 실행을 테스트하기 위해 간단하게 사용할 수 있는 여러 메서드를 제공합니다.

```php
// 항상 당첨...
Lottery::alwaysWin();

// 항상 낙첨...
Lottery::alwaysLose();

// 한 번 당첨 후 낙첨, 그리고 원래 동작으로 복귀...
Lottery::fix([true, false]);

// Lottery를 기본 동작으로 복귀...
Lottery::determineResultsNormally();
```

<a name="pipeline"></a>
### 파이프라인(Pipeline)

라라벨의 `Pipeline` 파사드는 주어진 입력값을 일련의 호출 가능한 클래스, 클로저, 콜러블 등에 "파이프" 방식으로 전달할 수 있는 편리한 방법을 제공합니다. 각 클래스는 입력값을 점검・변경하고 다음 콜러블을 호출할 수 있습니다.

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

각 콜러블(클로저 또는 클래스)은 입력값과 `$next` 클로저를 받습니다. `$next` 클로저를 호출하면 파이프라인의 다음 콜러블이 실행됩니다. 이런 구조는 [미들웨어](/docs/12.x/middleware)와 매우 유사합니다.

파이프라인의 마지막 콜러블에서 `$next`가 호출되면, `then` 메서드에 전달된 콜러블이 실행됩니다. 일반적으로 이 콜러블은 입력값을 그대로 반환합니다.

물론, 클로저뿐 아니라 호출할 수 있는 클래스도 파이프라인에 사용할 수 있습니다. 만약 클래스명을 지정하면, 해당 클래스는 라라벨의 [서비스 컨테이너](/docs/12.x/container)를 통해 자동으로 인스턴스화되며, 의존성 주입도 가능합니다.

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

라라벨의 `Sleep` 클래스는 PHP의 기본 `sleep` 및 `usleep` 함수의 경량 래퍼 역할을 하면서, 테스트에 용이하도록 친숙한 API를 제공합니다.

```php
use Illuminate\Support\Sleep;

$waiting = true;

while ($waiting) {
    Sleep::for(1)->second();

    $waiting = /* ... */;
}
```

`Sleep` 클래스는 다양한 시간 단위로 사용 가능한 여러 메서드를 제공합니다.

```php
// 일정 시간 대기 후 값 반환...
$result = Sleep::for(1)->second()->then(fn () => 1 + 1);

// 주어진 값이 true인 동안 반복해서 대기...
Sleep::for(1)->second()->while(fn () => shouldKeepSleeping());

// 90초 동안 대기...
Sleep::for(1.5)->minutes();

// 2초 동안 대기...
Sleep::for(2)->seconds();

// 500밀리초 대기...
Sleep::for(500)->milliseconds();

// 5,000마이크로초 대기...
Sleep::for(5000)->microseconds();

// 지정한 시각까지 대기...
Sleep::until(now()->addMinute());

// PHP의 기본 "sleep" 함수와 동일...
Sleep::sleep(2);

// PHP의 기본 "usleep" 함수와 동일...
Sleep::usleep(5000);
```

다양한 시간 단위를 쉽게 조합하려면 `and` 메서드를 사용할 수 있습니다.

```php
Sleep::for(1)->second()->and(10)->milliseconds();
```

<a name="testing-sleep"></a>
#### Sleep 테스트하기

`Sleep` 클래스 또는 PHP의 기본 sleep 관련 함수를 이용하는 코드를 테스트하면 실제로 테스트 실행이 일시 중지됩니다. 이로 인해 테스트 속도가 현저히 느려질 수 있습니다. 예를 들어 다음과 같은 코드가 있다고 가정해봅시다.

```php
$waiting = /* ... */;

$seconds = 1;

while ($waiting) {
    Sleep::for($seconds++)->seconds();

    $waiting = /* ... */;
}
```

이 코드를 테스트하면 _최소_ 1초가 걸리게 됩니다. 다행히 `Sleep` 클래스는 "페이크"로 동작할 수 있어서 테스트 속도를 빠르게 유지할 수 있습니다.

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

`Sleep` 클래스를 페이크로 설정하면 실제로 실행이 지연되지 않고, 테스트가 매우 빠르게 끝납니다.

또한, `Sleep` 클래스가 페이크로 설정되어 있을 때, 실제로 'sleep'이 몇 번 실행되었는지 등을 검증하는 다양한 assertion을 쓸 수 있습니다. 예를 들어, 1초, 2초, 3초씩 세 번 대기하는 코드를 테스트한다고 했을 때, `assertSequence` 메서드로 각 대기 시간을 정확하게 검증할 수 있습니다.

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

이 외에도 테스트 시 사용할 수 있는 여러 assertion 메서드가 제공됩니다.

```php
use Carbon\CarbonInterval as Duration;
use Illuminate\Support\Sleep;

// sleep이 3번 호출됐는지 검증...
Sleep::assertSleptTimes(3);

// sleep의 duration을 조건에 맞게 검증...
Sleep::assertSlept(function (Duration $duration): bool {
    return /* ... */;
}, times: 1);

// Sleep 클래스가 한 번도 호출되지 않았는지 검증...
Sleep::assertNeverSlept();

// Sleep이 호출되었더라도 실제로 대기가 일어나지 않았는지 검증...
Sleep::assertInsomniac();
```

애플리케이션 코드에서 페이크 sleep이 발생할 때 마다 어떤 행동을 하고 싶을 때도 있습니다. 이때는 `whenFakingSleep` 메서드에 콜백을 전달하면 됩니다. 아래 예시에서는 라라벨의 [시간 조작 헬퍼](/docs/12.x/mocking#interacting-with-time)를 이용해 sleep duration만큼 시간을 즉시 진전시키도록 처리했습니다.

```php
use Carbon\CarbonInterval as Duration;

$this->freezeTime();

Sleep::fake();

Sleep::whenFakingSleep(function (Duration $duration) {
    // 페이크 sleep 시 시간 진전...
    $this->travel($duration->totalMilliseconds)->milliseconds();
});
```

시간 동기화는 매우 자주 필요한 기능이기에, `fake` 메서드에 `syncWithCarbon` 인수를 true로 전달하면 sleep 시 Carbon의 시간도 함께 진전됩니다.

```php
Sleep::fake(syncWithCarbon: true);

$start = now();

Sleep::for(1)->second();

$start->diffForHumans(); // 1 second ago
```

라라벨에서는 실행 일시 중지가 필요할 때 내부적으로 모두 `Sleep` 클래스를 사용합니다. 예를 들어, [retry](#method-retry) 헬퍼도 sleep이 필요할 때 이 클래스를 사용하므로, 테스트 가능성이 높아집니다.

<a name="timebox"></a>

### 타임박스 (Timebox)

라라벨의 `Timebox` 클래스는 주어진 콜백 함수가 실제로 더 빨리 실행을 마치더라도 항상 고정된 시간만큼 실행되도록 보장합니다. 이는 암호화 작업이나 사용자 인증 검사처럼 공격자가 실행 시간의 변화를 이용해 민감한 정보를 추론하려 할 때 특히 유용합니다.

실행이 고정된 시간보다 오래 걸릴 경우에는 `Timebox`가 아무런 영향을 주지 않습니다. 따라서 최악의 경우를 고려하여 충분히 긴 시간을 고정 시간으로 설정하는 것은 개발자의 몫입니다.

`call` 메서드는 클로저와 마이크로초 단위의 시간 제한을 인수로 받아, 클로저를 실행한 후 해당 시간까지 대기합니다.

```php
use Illuminate\Support\Timebox;

(new Timebox)->call(function ($timebox) {
    // ...
}, microseconds: 10000);
```

클로저 내부에서 예외가 발생할 경우에도, 이 클래스는 정해진 지연 시간을 존중하며, 지연 후에 예외를 다시 던집니다.

<a name="uri"></a>
### URI

라라벨의 `Uri` 클래스는 URI를 생성하고 조작하는 데 편리하고 플루언트(flunet)한 인터페이스를 제공합니다. 이 클래스는 기본적으로 League URI 패키지의 기능을 감싸고 있으며, 라라벨의 라우팅 시스템과 자연스럽게 통합됩니다.

정적 메서드를 활용하여 쉽게 `Uri` 인스턴스를 생성할 수 있습니다.

```php
use App\Http\Controllers\UserController;
use App\Http\Controllers\InvokableController;
use Illuminate\Support\Uri;

// 주어진 문자열로부터 URI 인스턴스 생성...
$uri = Uri::of('https://example.com/path');

// 경로, 네임드 라우트, 컨트롤러 액션을 기반으로 URI 인스턴스 생성...
$uri = Uri::to('/dashboard');
$uri = Uri::route('users.show', ['user' => 1]);
$uri = Uri::signedRoute('users.show', ['user' => 1]);
$uri = Uri::temporarySignedRoute('user.index', now()->addMinutes(5));
$uri = Uri::action([UserController::class, 'index']);
$uri = Uri::action(InvokableController::class);

// 현재 요청 URL로부터 URI 인스턴스 생성...
$uri = $request->uri();
```

`Uri` 인스턴스를 획득한 후에는 아래와 같이 메서드 체이닝을 통해 자유롭게 수정할 수 있습니다.

```php
$uri = Uri::of('https://example.com')
    ->withScheme('http')
    ->withHost('test.com')
    ->withPort(8000)
    ->withPath('/users')
    ->withQuery(['page' => 2])
    ->withFragment('section-1');
```

<a name="inspecting-uris"></a>
#### URI 구성 요소 조회

`Uri` 클래스는 URI의 다양한 구성 요소를 손쉽게 조회할 수 있는 메서드도 제공합니다.

```php
$scheme = $uri->scheme();
$host = $uri->host();
$port = $uri->port();
$path = $uri->path();
$segments = $uri->pathSegments();
$query = $uri->query();
$fragment = $uri->fragment();
```

<a name="manipulating-query-strings"></a>
#### 쿼리 문자열 조작

`Uri` 클래스는 URI의 쿼리 문자열을 조작할 수 있는 여러 메서드를 제공합니다. `withQuery` 메서드는 기존 쿼리 문자열에 추가 파라미터를 병합할 수 있습니다.

```php
$uri = $uri->withQuery(['sort' => 'name']);
```

`withQueryIfMissing` 메서드는 지정한 키가 기존 쿼리 문자열에 없을 때만 추가 파라미터를 병합합니다.

```php
$uri = $uri->withQueryIfMissing(['page' => 1]);
```

`replaceQuery` 메서드는 기존의 쿼리 문자열 전체를 새로운 쿼리로 완전히 대체합니다.

```php
$uri = $uri->replaceQuery(['page' => 1]);
```

`pushOntoQuery` 메서드는 배열 값을 갖는 쿼리 파라미터에 요소를 추가하는 데 사용할 수 있습니다.

```php
$uri = $uri->pushOntoQuery('filter', ['active', 'pending']);
```

`withoutQuery` 메서드를 활용하면 특정 파라미터를 쿼리 문자열에서 제거할 수 있습니다.

```php
$uri = $uri->withoutQuery(['page']);
```

<a name="generating-responses-from-uris"></a>
#### URI로부터 응답 생성

`redirect` 메서드를 사용하면 해당 URI로 리디렉션하는 `RedirectResponse` 인스턴스를 생성할 수 있습니다.

```php
$uri = Uri::of('https://example.com');

return $uri->redirect();
```

또는, 라우트나 컨트롤러 액션에서 단순히 `Uri` 인스턴스를 반환하면, 자동으로 해당 URI로 리디렉션 응답이 생성됩니다.

```php
use Illuminate\Support\Facades\Route;
use Illuminate\Support\Uri;

Route::get('/redirect', function () {
    return Uri::to('/index')
        ->withQuery(['sort' => 'name']);
});
```