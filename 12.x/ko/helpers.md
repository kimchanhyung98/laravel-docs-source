# 헬퍼 (Helpers)

- [소개](#introduction)
- [사용 가능한 메서드](#available-methods)
- [기타 유틸리티](#other-utilities)
    - [벤치마킹](#benchmarking)
    - [날짜](#dates)
    - [지연 함수](#deferred-functions)
    - [로터리](#lottery)
    - [파이프라인](#pipeline)
    - [슬립](#sleep)
    - [타임박스](#timebox)
    - [URI](#uri)

<a name="introduction"></a>
## 소개

라라벨에는 다양한 전역 "헬퍼" PHP 함수들이 포함되어 있습니다. 이 함수들 중 상당수는 프레임워크 자체에서 사용되지만, 여러분이 필요에 따라 애플리케이션 내에서 자유롭게 활용할 수도 있습니다.

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
[Number::parseInt](#method-number-parse-int)
[Number::parseFloat](#method-number-parse-float)
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
### 기타

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
[broadcast_if](#method-broadcast-if)
[broadcast_unless](#method-broadcast-unless)
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

`Arr::accessible` 메서드는 주어진 값이 배열처럼 접근 가능한지 여부를 판단합니다.

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

`Arr::add` 메서드는 지정된 키가 배열에 존재하지 않거나 해당 값이 `null`인 경우, 주어진 키/값 쌍을 배열에 추가합니다.

```php
use Illuminate\Support\Arr;

$array = Arr::add(['name' => 'Desk'], 'price', 100);

// ['name' => 'Desk', 'price' => 100]

$array = Arr::add(['name' => 'Desk', 'price' => null], 'price', 100);

// ['name' => 'Desk', 'price' => 100]
```

<a name="method-array-array"></a>
#### `Arr::array()`

`Arr::array` 메서드는 "dot" 표기법을 사용해 다차원 배열에서 값을 가져옵니다([Arr::get()](#method-array-get)과 동일하게 동작). 단, 요청한 값이 배열이 아닐 경우 `InvalidArgumentException` 예외를 발생시킵니다.

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

`Arr::boolean` 메서드는 "dot" 표기법을 사용해 다차원 배열에서 값을 가져오는데([Arr::get()](#method-array-get)과 동일), 요청한 값이 `boolean`이 아닐 경우 `InvalidArgumentException` 예외가 발생합니다.

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

`Arr::collapse` 메서드는 배열의 배열이나 컬렉션을 하나의 배열로 평탄화해줍니다.

```php
use Illuminate\Support\Arr;

$array = Arr::collapse([[1, 2, 3], [4, 5, 6], [7, 8, 9]]);

// [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

<a name="method-array-crossjoin"></a>
#### `Arr::crossJoin()`

`Arr::crossJoin` 메서드는 여러 배열을 크로스 조인하여 가능한 모든 조합(데카르트 곱)을 반환합니다.

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

`Arr::divide` 메서드는 주어진 배열의 키만 모은 배열 하나와, 값만 모은 배열 하나, 이렇게 두 개의 배열을 반환합니다.

```php
use Illuminate\Support\Arr;

[$keys, $values] = Arr::divide(['name' => 'Desk']);

// $keys: ['name']

// $values: ['Desk']
```

<a name="method-array-dot"></a>
#### `Arr::dot()`

`Arr::dot` 메서드는 다차원 배열을 "dot" 표기법을 사용한 단일 단계 배열로 평탄화합니다.

```php
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

$flattened = Arr::dot($array);

// ['products.desk.price' => 100]
```

<a name="method-array-except"></a>
#### `Arr::except()`

`Arr::except` 메서드는 주어진 배열에서 특정 키/값 쌍을 제거합니다.

```php
use Illuminate\Support\Arr;

$array = ['name' => 'Desk', 'price' => 100];

$filtered = Arr::except($array, ['price']);

// ['name' => 'Desk']
```

<a name="method-array-exists"></a>
#### `Arr::exists()`

`Arr::exists` 메서드는 주어진 배열에 특정 키가 존재하는지 확인합니다.

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

`Arr::first` 메서드는 전달한 배열에서 지정된 조건에 첫 번째로 만족하는 원소를 반환합니다.

```php
use Illuminate\Support\Arr;

$array = [100, 200, 300];

$first = Arr::first($array, function (int $value, int $key) {
    return $value >= 150;
});

// 200
```

세 번째 인자로 기본값을 전달할 수도 있습니다. 조건을 만족하는 값이 없을 경우 이 기본값이 반환됩니다.

```php
use Illuminate\Support\Arr;

$first = Arr::first($array, $callback, $default);
```

<a name="method-array-flatten"></a>
#### `Arr::flatten()`

`Arr::flatten` 메서드는 다차원 배열을 단일 단계의 배열로 평탄화합니다.

```php
use Illuminate\Support\Arr;

$array = ['name' => 'Joe', 'languages' => ['PHP', 'Ruby']];

$flattened = Arr::flatten($array);

// ['Joe', 'PHP', 'Ruby']
```

<a name="method-array-float"></a>
#### `Arr::float()`

`Arr::float` 메서드는 "dot" 표기법으로 다차원 배열에서 값을 추출하지만([Arr::get()](#method-array-get)과 동일), 반환된 값이 `float`가 아닐 경우 `InvalidArgumentException`을 던집니다.

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

`Arr::forget` 메서드는 "dot" 표기법을 사용해, 다차원 배열에서 특정 키/값 쌍을 제거합니다.

```php
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

Arr::forget($array, 'products.desk');

// ['products' => []]
```

<a name="method-array-from"></a>
#### `Arr::from()`

`Arr::from` 메서드는 다양한 타입의 입력을 일반 PHP 배열로 변환해줍니다. 이 메서드는 배열, 객체는 물론, 라라벨의 일부 인터페이스(`Arrayable`, `Enumerable`, `Jsonable`, `JsonSerializable`)까지 지원합니다. 또한 `Traversable`과 `WeakMap` 인스턴스도 처리할 수 있습니다.

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

이 메서드는 기본값도 전달받을 수 있습니다. 지정한 키가 배열에 없으면 이 값이 반환됩니다.

```php
use Illuminate\Support\Arr;

$discount = Arr::get($array, 'products.desk.discount', 0);

// 0
```

<a name="method-array-has"></a>
#### `Arr::has()`

`Arr::has` 메서드는 "dot" 표기법을 사용해 주어진 배열에 지정한 항목(들)이 존재하는지 검사합니다.

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

`Arr::hasAll` 메서드는 "dot" 표기법을 사용해, 지정된 모든 키가 주어진 배열에 존재하는지 확인합니다.

```php
use Illuminate\Support\Arr;

$array = ['name' => 'Taylor', 'language' => 'PHP'];

Arr::hasAll($array, ['name']); // true
Arr::hasAll($array, ['name', 'language']); // true
Arr::hasAll($array, ['name', 'IDE']); // false
```

<a name="method-array-hasany"></a>

#### `Arr::hasAny()`

`Arr::hasAny` 메서드는 "dot" 표기법을 사용하여, 지정한 여러 항목 중 하나라도 배열에 존재하는지 확인합니다.

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

`Arr::integer` 메서드는 [Arr::get()](#method-array-get)과 마찬가지로 "dot" 표기법을 사용해 다차원 배열에서 값을 가져옵니다. 그러나 요청한 값이 `int` 타입이 아닐 경우 `InvalidArgumentException` 예외를 발생시킵니다.

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

`Arr::isAssoc` 메서드는 주어진 배열이 연관 배열(associative array)인지 확인하여 `true`를 반환합니다. 배열의 키가 0부터 시작하는 연속적인 숫자가 아니면 "연관 배열"로 간주합니다.

```php
use Illuminate\Support\Arr;

$isAssoc = Arr::isAssoc(['product' => ['name' => 'Desk', 'price' => 100]]);

// true

$isAssoc = Arr::isAssoc([1, 2, 3]);

// false
```

<a name="method-array-islist"></a>
#### `Arr::isList()`

`Arr::isList` 메서드는 주어진 배열의 키가 0부터 시작하는 연속적인 숫자인 경우 `true`를 반환합니다.

```php
use Illuminate\Support\Arr;

$isList = Arr::isList(['foo', 'bar', 'baz']);

// true

$isList = Arr::isList(['product' => ['name' => 'Desk', 'price' => 100]]);

// false
```

<a name="method-array-join"></a>
#### `Arr::join()`

`Arr::join` 메서드는 배열 요소를 문자열로 이어붙입니다. 두 번째 인수로 일반적인 구분자 문자열을 지정할 수 있으며, 세 번째 인수로 마지막 요소 사이에 사용할 구분 문자를 지정할 수도 있습니다.

```php
use Illuminate\Support\Arr;

$array = ['Tailwind', 'Alpine', 'Laravel', 'Livewire'];

$joined = Arr::join($array, ', ');

// Tailwind, Alpine, Laravel, Livewire

$joined = Arr::join($array, ', ', ', and ');

// Tailwind, Alpine, Laravel, and Livewire
```

<a name="method-array-keyby"></a>
#### `Arr::keyBy()`

`Arr::keyBy` 메서드는 지정한 키의 값을 각 항목의 키로 사용하는 새로운 배열을 만듭니다. 같은 키를 가진 항목이 여러 개 있을 경우 마지막 항목만 새로운 배열에 포함됩니다.

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

`Arr::last` 메서드는 주어진 조건(콜백 함수가 `true`를 반환)과 일치하는 배열의 마지막 요소를 반환합니다.

```php
use Illuminate\Support\Arr;

$array = [100, 200, 300, 110];

$last = Arr::last($array, function (int $value, int $key) {
    return $value >= 150;
});

// 300
```

만약 어떠한 값도 조건을 통과하지 못하는 경우, 세 번째 인자로 기본값을 지정하여 반환하게 할 수 있습니다.

```php
use Illuminate\Support\Arr;

$last = Arr::last($array, $callback, $default);
```

<a name="method-array-map"></a>
#### `Arr::map()`

`Arr::map` 메서드는 배열을 순회하면서 각 값과 키를 지정한 콜백 함수에 전달합니다. 콜백에서 반환된 값으로 해당 배열의 값을 대체합니다.

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

`Arr::mapSpread` 메서드는 배열을 순회하면서 각 중첩 요소의 값을 콜백 함수에 펼쳐서 전달합니다. 콜백에서 반환된 값으로 새로운 배열이 만들어집니다.

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

`Arr::mapWithKeys` 메서드는 배열을 순회하면서 각 값을 콜백 함수에 전달합니다. 콜백 함수에서는 단일 키/값 쌍(연관 배열)을 반환해야 하며, 반환된 결과로 새로운 배열을 만듭니다.

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

`Arr::only` 메서드는 주어진 배열에서 지정한 키에 해당하는 값만을 추출하여 반환합니다.

```php
use Illuminate\Support\Arr;

$array = ['name' => 'Desk', 'price' => 100, 'orders' => 10];

$slice = Arr::only($array, ['name', 'price']);

// ['name' => 'Desk', 'price' => 100]
```

<a name="method-array-partition"></a>
#### `Arr::partition()`

`Arr::partition` 메서드는 PHP의 배열 구조 분해(Array destructuring)와 함께 사용하여, 주어진 조건에 부합하는 요소들과 그렇지 않은 요소들을 분리된 배열로 반환할 수 있습니다.

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

`Arr::pluck` 메서드는 배열에서 지정된 키에 해당하는 모든 값을 추출합니다.

```php
use Illuminate\Support\Arr;

$array = [
    ['developer' => ['id' => 1, 'name' => 'Taylor']],
    ['developer' => ['id' => 2, 'name' => 'Abigail']],
];

$names = Arr::pluck($array, 'developer.name');

// ['Taylor', 'Abigail']
```

결과 배열에 사용할 키를 직접 지정할 수도 있습니다.

```php
use Illuminate\Support\Arr;

$names = Arr::pluck($array, 'developer.name', 'developer.id');

// [1 => 'Taylor', 2 => 'Abigail']
```

<a name="method-array-prepend"></a>
#### `Arr::prepend()`

`Arr::prepend` 메서드는 하나의 항목을 배열의 맨 앞에 추가합니다.

```php
use Illuminate\Support\Arr;

$array = ['one', 'two', 'three', 'four'];

$array = Arr::prepend($array, 'zero');

// ['zero', 'one', 'two', 'three', 'four']
```

필요하다면 해당 값에 사용할 키를 따로 지정할 수도 있습니다.

```php
use Illuminate\Support\Arr;

$array = ['price' => 100];

$array = Arr::prepend($array, 'Desk', 'name');

// ['name' => 'Desk', 'price' => 100]
```

<a name="method-array-prependkeyswith"></a>
#### `Arr::prependKeysWith()`

`Arr::prependKeysWith` 메서드는 연관 배열의 모든 키 앞에 지정한 접두사를 붙여서 반환합니다.

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

`Arr::pull` 메서드는 배열에서 지정한 키/값 한 쌍을 반환하고, 그 항목을 원본 배열에서 제거합니다.

```php
use Illuminate\Support\Arr;

$array = ['name' => 'Desk', 'price' => 100];

$name = Arr::pull($array, 'name');

// $name: Desk

// $array: ['price' => 100]
```

키가 존재하지 않을 경우, 세 번째 인자로 기본값을 지정해서 반환할 수도 있습니다.

```php
use Illuminate\Support\Arr;

$value = Arr::pull($array, $key, $default);
```

<a name="method-array-query"></a>
#### `Arr::query()`

`Arr::query` 메서드는 배열을 쿼리 스트링 형태로 변환합니다.

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

`Arr::random` 메서드는 배열에서 임의의 값을 하나 반환합니다.

```php
use Illuminate\Support\Arr;

$array = [1, 2, 3, 4, 5];

$random = Arr::random($array);

// 4 - (무작위로 선택됨)
```

두 번째 인자로 반환할 항목 개수를 지정할 수도 있습니다. 이 인자를 사용하면, 반환값은 항목이 1개여도 배열로 반환됩니다.

```php
use Illuminate\Support\Arr;

$items = Arr::random($array, 2);

// [2, 5] - (무작위로 선택됨)
```

<a name="method-array-reject"></a>
#### `Arr::reject()`

`Arr::reject` 메서드는 주어진 클로저(콜백 함수)를 이용해 조건에 맞는 항목을 배열에서 제거합니다.

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

`Arr::select` 메서드는 배열에서 지정한 키만을 포함하는 항목 배열을 반환합니다.

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

`Arr::set` 메서드는 "dot" 표기법을 사용하여 다차원 배열의 특정 위치에 값을 할당합니다.

```php
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

Arr::set($array, 'products.desk.price', 200);

// ['products' => ['desk' => ['price' => 200]]]
```

<a name="method-array-shuffle"></a>
#### `Arr::shuffle()`

`Arr::shuffle` 메서드는 배열의 항목 순서를 무작위로 섞어서 반환합니다.

```php
use Illuminate\Support\Arr;

$array = Arr::shuffle([1, 2, 3, 4, 5]);

// [3, 2, 5, 1, 4] - (무작위로 생성됨)
```

<a name="method-array-sole"></a>
#### `Arr::sole()`

`Arr::sole` 메서드는 주어진 클로저 조건을 만족하는 단 하나의 값을 배열에서 찾아 반환합니다. 만약 두 개 이상이 조건을 만족하면 `Illuminate\Support\MultipleItemsFoundException` 예외가 발생하고, 조건을 만족하는 값이 하나도 없다면 `Illuminate\Support\ItemNotFoundException` 예외가 발생합니다.

```php
use Illuminate\Support\Arr;

$array = ['Desk', 'Table', 'Chair'];

$value = Arr::sole($array, fn (string $value) => $value === 'Desk');

// 'Desk'
```

<a name="method-array-sort"></a>
#### `Arr::sort()`

`Arr::sort` 메서드는 배열의 값 기준으로 정렬합니다.

```php
use Illuminate\Support\Arr;

$array = ['Desk', 'Table', 'Chair'];

$sorted = Arr::sort($array);

// ['Chair', 'Desk', 'Table']
```

또는 주어진 클로저의 결과에 따라 배열을 정렬할 수도 있습니다.

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

`Arr::sortDesc` 메서드는 배열의 값을 기준으로 내림차순 정렬합니다.

```php
use Illuminate\Support\Arr;

$array = ['Desk', 'Table', 'Chair'];

$sorted = Arr::sortDesc($array);

// ['Table', 'Desk', 'Chair']
```

주어진 클로저의 결과에 따라 내림차순 정렬할 수도 있습니다.

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

`Arr::sortRecursive` 메서드는 배열 내의 값을 재귀적으로 정렬합니다. 이때 숫자 인덱스(순차적 인덱스)를 가진 하위 배열에는 `sort` 함수를, 연관 배열에는 `ksort` 함수를 각각 사용합니다.

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

만약 내림차순으로 정렬된 결과를 원한다면 `Arr::sortRecursiveDesc` 메서드를 사용할 수 있습니다.

```php
$sorted = Arr::sortRecursiveDesc($array);
```

<a name="method-array-string"></a>
#### `Arr::string()`

`Arr::string` 메서드는 "dot" 표기법을 사용해 깊게 중첩된 배열에서 값을 가져옵니다. ([Arr::get()](#method-array-get)와 동일하게 동작) 단, 요청한 값이 `string`이 아닐 경우 `InvalidArgumentException`을 발생시킵니다.

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

`Arr::take` 메서드는 지정된 개수만큼의 원소로 구성된 새로운 배열을 반환합니다.

```php
use Illuminate\Support\Arr;

$array = [0, 1, 2, 3, 4, 5];

$chunk = Arr::take($array, 3);

// [0, 1, 2]
```

음수 값을 전달하면 배열의 마지막에서부터 해당 개수만큼의 원소를 가져옵니다.

```php
$array = [0, 1, 2, 3, 4, 5];

$chunk = Arr::take($array, -2);

// [4, 5]
```

<a name="method-array-to-css-classes"></a>
#### `Arr::toCssClasses()`

`Arr::toCssClasses` 메서드는 조건에 따라 CSS 클래스 문자열을 조합해 반환합니다. 이 메서드는 사용하고자 하는 클래스명을 배열의 key에, 그 값을 불리언 조건식으로 전달합니다. 만약 배열 원소의 key가 숫자일 경우, 렌더링되는 클래스 목록에 항상 포함됩니다.

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

`Arr::toCssStyles` 메서드는 조건에 따라 CSS 스타일 문자열을 조합해 반환합니다. 이 메서드는 사용하고자 하는 스타일을 배열의 key에, 그 값을 불리언 조건식으로 전달합니다. 배열 원소의 key가 숫자일 경우, 렌더링되는 스타일에 항상 포함됩니다.

```php
use Illuminate\Support\Arr;

$hasColor = true;

$array = ['background-color: blue', 'color: blue' => $hasColor];

$classes = Arr::toCssStyles($array);

/*
    'background-color: blue; color: blue;'
*/
```

이 메서드는 라라벨의 [Blade 컴포넌트의 attribute bag에 클래스를 병합하는 기능](/docs/12.x/blade#conditionally-merge-classes)과 `@class` [Blade 디렉티브](/docs/12.x/blade#conditional-classes)를 지원합니다.

<a name="method-array-undot"></a>
#### `Arr::undot()`

`Arr::undot` 메서드는 "dot" 표기법을 사용한 1차원 배열을 다차원 배열로 변환합니다.

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

`Arr::where` 메서드는 주어진 클로저(익명 함수)를 사용해 배열을 필터링합니다.

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

`Arr::whereNotNull` 메서드는 주어진 배열에서 모든 `null` 값을 제거합니다.

```php
use Illuminate\Support\Arr;

$array = [0, null];

$filtered = Arr::whereNotNull($array);

// [0 => 0]
```

<a name="method-array-wrap"></a>
#### `Arr::wrap()`

`Arr::wrap` 메서드는 전달된 값을 배열로 감싸 반환합니다. 만약 전달된 값이 이미 배열인 경우, 해당 배열을 그대로 반환합니다.

```php
use Illuminate\Support\Arr;

$string = 'Laravel';

$array = Arr::wrap($string);

// ['Laravel']
```

전달된 값이 `null`일 경우, 빈 배열이 반환됩니다.

```php
use Illuminate\Support\Arr;

$array = Arr::wrap(null);

// []
```

<a name="method-data-fill"></a>
#### `data_fill()`

`data_fill` 함수는 중첩된 배열이나 객체에서 "dot" 표기법을 사용해 값이 비어있는(존재하지 않는) 위치에 새로운 값을 설정합니다.

```php
$data = ['products' => ['desk' => ['price' => 100]]];

data_fill($data, 'products.desk.price', 200);

// ['products' => ['desk' => ['price' => 100]]]

data_fill($data, 'products.desk.discount', 10);

// ['products' => ['desk' => ['price' => 100, 'discount' => 10]]]
```

이 함수는 아스테리스크(*) 와일드카드를 지원하며, 대상에 맞게 값을 채워줍니다.

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

`data_get` 함수는 중첩된 배열이나 객체에서 "dot" 표기법을 사용해 값을 가져옵니다.

```php
$data = ['products' => ['desk' => ['price' => 100]]];

$price = data_get($data, 'products.desk.price');

// 100
```

`data_get` 함수는 키가 존재하지 않을 경우 반환할 기본값도 받을 수 있습니다.

```php
$discount = data_get($data, 'products.desk.discount', 0);

// 0
```

아스테리스크(*) 와일드카드를 사용해 배열이나 객체의 모든 키에 접근할 수도 있습니다.

```php
$data = [
    'product-one' => ['name' => 'Desk 1', 'price' => 100],
    'product-two' => ['name' => 'Desk 2', 'price' => 150],
];

data_get($data, '*.name');

// ['Desk 1', 'Desk 2'];
```

`{first}` 및 `{last}` 플레이스홀더를 사용하면 배열의 첫 번째 또는 마지막 항목을 가져올 수 있습니다.

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

`data_set` 함수는 중첩된 배열이나 객체에서 "dot" 표기법을 사용해 값을 설정합니다.

```php
$data = ['products' => ['desk' => ['price' => 100]]];

data_set($data, 'products.desk.price', 200);

// ['products' => ['desk' => ['price' => 200]]]
```

이 함수 역시 아스테리스크(*) 와일드카드를 지원하며, 대상에 대해 값을 일괄적으로 설정할 수 있습니다.

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

기본적으로 기존 값을 항상 덮어씁니다. 값이 존재하지 않을 때만 설정하길 원한다면, 네 번째 인자로 `false`를 전달하면 됩니다.

```php
$data = ['products' => ['desk' => ['price' => 100]]];

data_set($data, 'products.desk.price', 200, overwrite: false);

// ['products' => ['desk' => ['price' => 100]]]
```

<a name="method-data-forget"></a>
#### `data_forget()`

`data_forget` 함수는 중첩된 배열이나 객체에서 "dot" 표기법을 사용해 값을 제거합니다.

```php
$data = ['products' => ['desk' => ['price' => 100]]];

data_forget($data, 'products.desk.price');

// ['products' => ['desk' => []]]
```

이 함수도 아스테리스크(*) 와일드카드를 지원하여, 여러 대상의 값을 한 번에 지울 수 있습니다.

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

`head` 함수는 전달된 배열에서 첫 번째 요소를 반환합니다.

```php
$array = [100, 200, 300];

$first = head($array);

// 100
```

<a name="method-last"></a>
#### `last()`

`last` 함수는 전달된 배열에서 마지막 요소를 반환합니다.

```php
$array = [100, 200, 300];

$last = last($array);

// 300
```

<a name="numbers"></a>
## 숫자(수치 데이터)

<a name="method-number-abbreviate"></a>
#### `Number::abbreviate()`

`Number::abbreviate` 메서드는 전달된 숫자 값을 읽기 쉬운 단위(약어)로 변환해 반환합니다.

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

`Number::clamp` 메서드는 지정한 숫자가 특정 범위 내에 있도록 보장합니다. 숫자가 최소값보다 작으면 최소값을, 최대값보다 크면 최대값을 반환합니다.

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

`Number::currency` 메서드는 전달된 값에 대해 통화 표기를 문자열로 반환합니다.

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

`Number::defaultCurrency` 메서드는 `Number` 클래스에서 사용 중인 기본 통화 값을 반환합니다.

```php
use Illuminate\Support\Number;

$currency = Number::defaultCurrency();

// USD
```

<a name="method-default-locale"></a>
#### `Number::defaultLocale()`

`Number::defaultLocale` 메서드는 `Number` 클래스에서 사용 중인 기본 로케일을 반환합니다.

```php
use Illuminate\Support\Number;

$locale = Number::defaultLocale();

// en
```

<a name="method-number-file-size"></a>
#### `Number::fileSize()`

`Number::fileSize` 메서드는 주어진 바이트 값을 파일 크기 문자열로 변환해 반환합니다.

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

`Number::forHumans` 메서드는 제공된 숫자 값을 읽기 쉬운 형태(사람이 읽기 쉬운 수치)로 반환합니다.

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

`Number::format` 메서드는 주어진 숫자를 로케일 설정에 따라 문자열로 포맷팅해 반환합니다.

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

`Number::ordinal` 메서드는 숫자를 서수(순서를 나타내는 형태)로 반환합니다.

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

`Number::pairs` 메서드는 지정된 범위와 스텝(step) 값에 따라 숫자 쌍(서브 범위)의 배열을 생성합니다. 이 메서드는 예를 들어 페이지네이션이나 작업을 일괄 처리(batch)할 때 전체 범위를 더 작은 하위 범위로 나누는 데 유용하게 사용할 수 있습니다. `pairs` 메서드는 배열의 배열을 반환하며, 각 내부 배열이 하나의 숫자 쌍(서브 범위)을 나타냅니다.

```php
use Illuminate\Support\Number;

$result = Number::pairs(25, 10);

// [[0, 9], [10, 19], [20, 25]]

$result = Number::pairs(25, 10, offset: 0);

// [[0, 10], [10, 20], [20, 25]]
```

<a name="method-number-parse-int"></a>
#### `Number::parseInt()`

`Number::parseInt` 메서드는 지정한 로케일(locale)에 따라 문자열을 정수로 변환합니다.

```php
use Illuminate\Support\Number;

$result = Number::parseInt('10.123');

// (int) 10

$result = Number::parseInt('10,123', locale: 'fr');

// (int) 10
```

<a name="method-number-parse-float"></a>
#### `Number::parseFloat()`

`Number::parseFloat` 메서드는 지정한 로케일(locale)에 따라 문자열을 실수(float)로 변환합니다.

```php
use Illuminate\Support\Number;

$result = Number::parseFloat('10');

// (float) 10.0

$result = Number::parseFloat('10', locale: 'fr');

// (float) 10.0
```

<a name="method-number-percentage"></a>
#### `Number::percentage()`

`Number::percentage` 메서드는 전달된 값을 퍼센트(%) 표기 문자열로 반환합니다.

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

`Number::spell` 메서드는 주어진 숫자를 해당하는 단어 문자열로 변환합니다.

```php
use Illuminate\Support\Number;

$number = Number::spell(102);

// one hundred and two

$number = Number::spell(88, locale: 'fr');

// quatre-vingt-huit
```

`after` 인자를 사용하면, 지정한 값 이후부터는 모든 숫자를 영문 단어 대신 숫자로 표기할 수 있습니다.

```php
$number = Number::spell(10, after: 10);

// 10

$number = Number::spell(11, after: 10);

// eleven
```

`until` 인자를 사용하면, 지정한 값 이전까지는 모든 숫자를 영문 단어로 표기할 수 있습니다.

```php
$number = Number::spell(5, until: 10);

// five

$number = Number::spell(10, until: 10);

// 10
```

<a name="method-number-spell-ordinal"></a>
#### `Number::spellOrdinal()`

`Number::spellOrdinal` 메서드는 주어진 숫자를 서수(ordinal) 표기 형태의 영어 단어로 반환합니다.

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

`Number::trim` 메서드는 소수점 뒤에 붙는 필요 없는 0을 제거한 숫자를 반환합니다.

```php
use Illuminate\Support\Number;

$number = Number::trim(12.0);

// 12

$number = Number::trim(12.30);

// 12.3
```

<a name="method-number-use-locale"></a>
#### `Number::useLocale()`

`Number::useLocale` 메서드는 전역적으로 기본 숫자 로케일(locale)을 설정합니다. 이 설정 이후에는 `Number` 클래스의 메서드들이 모두 해당 로케일을 적용해서 숫자나 통화를 포맷합니다.

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

`Number::withLocale` 메서드는 주어진 클로저(익명 함수)를 지정한 로케일로 실행한 뒤, 완료되면 원래의 로케일로 복구합니다.

```php
use Illuminate\Support\Number;

$number = Number::withLocale('de', function () {
    return Number::format(1500);
});
```

<a name="method-number-use-currency"></a>
#### `Number::useCurrency()`

`Number::useCurrency` 메서드는 전역적으로 기본 통화(화폐 단위)를 설정합니다. 이 설정 이후에는 `Number` 클래스의 관련 메서드가 모두 해당 통화로 결과를 포맷합니다.

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

`Number::withCurrency` 메서드는 주어진 클로저를 지정한 통화로 실행하고, 이후 원래 통화로 복구합니다.

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

`app_path` 함수는 애플리케이션의 `app` 디렉토리에 대한 전체 경로(절대 경로)를 반환합니다. 또한, `app_path` 함수에 파일 경로를 전달하면 앱 디렉토리를 기준으로 상대 경로의 전체 경로를 얻을 수도 있습니다.

```php
$path = app_path();

$path = app_path('Http/Controllers/Controller.php');
```

<a name="method-base-path"></a>
#### `base_path()`

`base_path` 함수는 애플리케이션의 루트 디렉토리에 대한 전체 경로를 반환합니다. 또한, `base_path` 함수에 파일 경로를 전달하면 프로젝트 루트를 기준으로 해당 파일의 전체 경로를 얻을 수 있습니다.

```php
$path = base_path();

$path = base_path('vendor/bin');
```

<a name="method-config-path"></a>
#### `config_path()`

`config_path` 함수는 애플리케이션의 `config` 디렉토리에 대한 전체 경로를 반환합니다. 또한, 설정 디렉토리 내 특정 파일의 전체 경로를 얻기 위해 사용할 수 있습니다.

```php
$path = config_path();

$path = config_path('app.php');
```

<a name="method-database-path"></a>
#### `database_path()`

`database_path` 함수는 애플리케이션의 `database` 디렉토리에 대한 전체 경로를 반환합니다. 이 함수 역시 데이터베이스 디렉토리 내의 파일에 대한 전체 경로를 얻는 데 활용할 수 있습니다.

```php
$path = database_path();

$path = database_path('factories/UserFactory.php');
```

<a name="method-lang-path"></a>
#### `lang_path()`

`lang_path` 함수는 애플리케이션의 `lang` 디렉토리에 대한 전체 경로를 반환합니다. 또한, 디렉토리 내의 특정 파일 경로도 얻을 수 있습니다.

```php
$path = lang_path();

$path = lang_path('en/messages.php');
```

> [!NOTE]
> 기본적으로 라라벨 애플리케이션 스캐폴딩에는 `lang` 디렉토리가 포함되지 않습니다. 라라벨의 언어 파일을 직접 수정하고 싶다면, `lang:publish` 아티즌 명령어를 통해 해당 파일을 퍼블리시할 수 있습니다.

<a name="method-public-path"></a>
#### `public_path()`

`public_path` 함수는 애플리케이션의 `public` 디렉토리에 대한 전체 경로를 반환합니다. 또한, 퍼블릭 디렉토리 내의 특정 파일 경로도 생성할 수 있습니다.

```php
$path = public_path();

$path = public_path('css/app.css');
```

<a name="method-resource-path"></a>
#### `resource_path()`

`resource_path` 함수는 애플리케이션의 `resources` 디렉토리에 대한 전체 경로를 반환합니다. 이 함수를 이용해 리소스 디렉토리 내 파일의 전체 경로도 얻을 수 있습니다.

```php
$path = resource_path();

$path = resource_path('sass/app.scss');
```

<a name="method-storage-path"></a>
#### `storage_path()`

`storage_path` 함수는 애플리케이션의 `storage` 디렉토리에 대한 전체 경로를 반환합니다. 또한, 스토리지 디렉토리 내 특정 파일 경로를 생성할 수도 있습니다.

```php
$path = storage_path();

$path = storage_path('app/file.txt');
```

<a name="urls"></a>
## URL

<a name="method-action"></a>
#### `action()`

`action` 함수는 지정한 컨트롤러 액션에 대한 URL을 생성합니다.

```php
use App\Http\Controllers\HomeController;

$url = action([HomeController::class, 'index']);
```

메서드에서 라우트 파라미터를 필요로 하면, 두 번째 인수로 값을 전달할 수 있습니다.

```php
$url = action([UserController::class, 'profile'], ['id' => 1]);
```

<a name="method-asset"></a>
#### `asset()`

`asset` 함수는 현재 요청의 스킴(HTTP 또는 HTTPS)을 기준으로 애셋(정적 파일)의 URL을 생성합니다.

```php
$url = asset('img/photo.jpg');
```

`.env` 파일의 `ASSET_URL` 변수를 설정하여 애셋의 기본 URL 호스트를 지정할 수 있습니다. 이는 Amazon S3나 다른 CDN 같은 외부 서비스에서 정적 파일을 호스팅하는 경우에 유용합니다.

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

해당 라우트가 파라미터를 받는 경우, 두 번째 인수로 값을 전달할 수 있습니다.

```php
$url = route('route.name', ['id' => 1]);
```

기본적으로 `route` 함수는 절대 URL을 생성합니다. 상대 URL을 원한다면, 세 번째 인수로 `false`를 전달하면 됩니다.

```php
$url = route('route.name', ['id' => 1], false);
```

<a name="method-secure-asset"></a>
#### `secure_asset()`

`secure_asset` 함수는 HTTPS를 사용하여 애셋의 URL을 생성합니다.

```php
$url = secure_asset('img/photo.jpg');
```

<a name="method-secure-url"></a>
#### `secure_url()`

`secure_url` 함수는 지정한 경로에 대해 완전한 HTTPS URL을 생성합니다. 두 번째 인수에 추가 경로 세그먼트를 전달할 수 있습니다.

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

필요하다면, 세 번째와 네 번째 인수로 리다이렉트에 사용할 HTTP 상태 코드와 추가 응답 헤더를 전달할 수 있습니다.

```php
return to_route('users.show', ['user' => 1], 302, ['X-Framework' => 'Laravel']);
```

<a name="method-uri"></a>
#### `uri()`

`uri` 함수는 주어진 URI를 이용하여 [플루언트 URI 인스턴스](#uri)를 생성합니다.

```php
$uri = uri('https://example.com')
    ->withPath('/users')
    ->withQuery(['page' => 1]);
```

`uri` 함수에 콜러블 컨트롤러와 메서드 쌍의 배열을 전달하면, 해당 컨트롤러 메서드의 라우트 경로에 대한 `Uri` 인스턴스를 생성합니다.

```php
use App\Http\Controllers\UserController;

$uri = uri([UserController::class, 'show'], ['user' => $user]);
```

컨트롤러가 invokable(단일 호출 메서드)일 경우, 컨트롤러 클래스명만 전달해도 됩니다.

```php
use App\Http\Controllers\UserIndexController;

$uri = uri(UserIndexController::class);
```

만약 `uri` 함수에 주어진 값이 [이름 있는 라우트](/docs/12.x/routing#named-routes)와 일치한다면, 해당 라우트의 경로에 대한 `Uri` 인스턴스가 생성됩니다.

```php
$uri = uri('users.show', ['user' => $user]);
```

<a name="method-url"></a>
#### `url()`

`url` 함수는 지정한 경로에 대해 완전한 URL을 생성합니다.

```php
$url = url('user/profile');

$url = url('user/profile', [1]);
```

경로를 전달하지 않으면, `Illuminate\Routing\UrlGenerator` 인스턴스를 반환합니다.

```php
$current = url()->current();

$full = url()->full();

$previous = url()->previous();
```

`url` 함수 사용에 대한 더 많은 정보는 [URL 생성 문서](/docs/12.x/urls#generating-urls)를 참고하세요.

<a name="miscellaneous"></a>
## 기타(Miscellaneous)

<a name="method-abort"></a>
#### `abort()`

`abort` 함수는 [HTTP 예외](/docs/12.x/errors#http-exceptions)를 발생시키고, 이는 [예외 핸들러](/docs/12.x/errors#handling-exceptions)에 의해 렌더링됩니다.

```php
abort(403);
```

예외 메시지와 브라우저로 전송할 커스텀 HTTP 응답 헤더도 함께 지정할 수 있습니다.

```php
abort(403, 'Unauthorized.', $headers);
```

<a name="method-abort-if"></a>
#### `abort_if()`

`abort_if` 함수는 주어진 불리언 식의 결과가 `true`일 때 HTTP 예외를 발생시킵니다.

```php
abort_if(! Auth::user()->isAdmin(), 403);
```

`abort` 메서드와 마찬가지로, 세 번째 인수에 예외 메시지, 네 번째 인수에 응답 헤더 배열을 전달할 수 있습니다.

<a name="method-abort-unless"></a>
#### `abort_unless()`

`abort_unless` 함수는 주어진 불리언 식의 결과가 `false`일 때 HTTP 예외를 발생시킵니다.

```php
abort_unless(Auth::user()->isAdmin(), 403);
```

이 함수 역시 `abort` 메서드와 동일하게 세 번째 인수로 예외 메시지, 네 번째 인수로 응답 헤더 배열을 전달할 수 있습니다.

<a name="method-app"></a>
#### `app()`

`app` 함수는 [서비스 컨테이너](/docs/12.x/container) 인스턴스를 반환합니다.

```php
$container = app();
```

클래스명 또는 인터페이스명을 전달하면, 컨테이너에서 해당 클래스를 해결(resolve)하여 반환받을 수 있습니다.

```php
$api = app('HelpSpot\API');
```

<a name="method-auth"></a>
#### `auth()`

`auth` 함수는 [인증자](/docs/12.x/authentication) 인스턴스를 반환합니다. 이 함수는 `Auth` 파사드 대신 사용할 수 있습니다.

```php
$user = auth()->user();
```

필요하다면, 접근하고자 하는 가드(guard) 인스턴스를 명시할 수도 있습니다.

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

`bcrypt` 함수는 주어진 값을 Bcrypt를 사용해 [해싱](/docs/12.x/hashing)합니다. 이 함수는 `Hash` 파사드의 대체로 사용할 수 있습니다.

```php
$password = bcrypt('my-secret-password');
```

<a name="method-blank"></a>
#### `blank()`

`blank` 함수는 전달한 값이 "비어 있는(blank)" 값인지 판별합니다.

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

반대로 "채워져 있는(filled)" 값을 확인하려면 [filled](#method-filled) 함수를 참고하세요.

<a name="method-broadcast"></a>

#### `broadcast()`

`broadcast` 함수는 주어진 [이벤트](/docs/12.x/events)를 해당 리스너들에게 [브로드캐스트](/docs/12.x/broadcasting)합니다.

```php
broadcast(new UserRegistered($user));

broadcast(new UserRegistered($user))->toOthers();
```

<a name="method-broadcast-if"></a>
#### `broadcast_if()`

`broadcast_if` 함수는 주어진 불리언(참/거짓) 표현식이 `true`일 때, 주어진 [이벤트](/docs/12.x/events)를 해당 리스너들에게 [브로드캐스트](/docs/12.x/broadcasting)합니다.

```php
broadcast_if($user->isActive(), new UserRegistered($user));

broadcast_if($user->isActive(), new UserRegistered($user))->toOthers();
```

<a name="method-broadcast-unless"></a>
#### `broadcast_unless()`

`broadcast_unless` 함수는 주어진 불리언 표현식이 `false`일 때, 주어진 [이벤트](/docs/12.x/events)를 해당 리스너들에게 [브로드캐스트](/docs/12.x/broadcasting)합니다.

```php
broadcast_unless($user->isBanned(), new UserRegistered($user));

broadcast_unless($user->isBanned(), new UserRegistered($user))->toOthers();
```

<a name="method-cache"></a>
#### `cache()`

`cache` 함수는 [캐시](/docs/12.x/cache)에서 값을 가져올 때 사용할 수 있습니다. 만약 주어진 키가 캐시에 존재하지 않으면, 옵션으로 기본값을 반환할 수 있습니다.

```php
$value = cache('key');

$value = cache('key', 'default');
```

키와 값 쌍의 배열을 이 함수에 전달하여 캐시에 아이템을 추가할 수 있습니다. 이때, 캐시가 유효하다고 간주할 기간(초 또는 기간 객체)도 함께 전달해야 합니다.

```php
cache(['key' => 'value'], 300);

cache(['key' => 'value'], now()->addSeconds(10));
```

<a name="method-class-uses-recursive"></a>
#### `class_uses_recursive()`

`class_uses_recursive` 함수는 특정 클래스와 그 모든 부모 클래스에서 사용된 모든 트레이트(trait) 목록을 반환합니다.

```php
$traits = class_uses_recursive(App\Models\User::class);
```

<a name="method-collect"></a>
#### `collect()`

`collect` 함수는 주어진 값을 기반으로 [컬렉션](/docs/12.x/collections) 인스턴스를 생성합니다.

```php
$collection = collect(['Taylor', 'Abigail']);
```

<a name="method-config"></a>
#### `config()`

`config` 함수는 [설정](/docs/12.x/configuration) 변수의 값을 가져옵니다. 설정값은 점(dot) 표기법을 사용하여 접근할 수 있으며, 여기에는 파일명과 옵션명이 포함됩니다. 만약 설정값이 존재하지 않으면 기본값을 두 번째 인수로 제공할 수 있습니다.

```php
$value = config('app.timezone');

$value = config('app.timezone', $default);
```

런타임 중에 키와 값 쌍의 배열을 전달해 설정 변수를 지정할 수도 있습니다. 단, 이 함수로 변경한 설정값은 현재 요청에만 적용되며 실제 설정 파일이 변경되는 것은 아닙니다.

```php
config(['app.debug' => true]);
```

<a name="method-context"></a>
#### `context()`

`context` 함수는 현재 [컨텍스트](/docs/12.x/context)에서 값을 가져옵니다. 컨텍스트 키가 존재하지 않을 경우 반환할 기본값을 지정할 수도 있습니다.

```php
$value = context('trace_id');

$value = context('trace_id', $default);
```

키와 값 쌍의 배열을 전달해 컨텍스트 값을 설정할 수도 있습니다.

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

`csrf_field` 함수는 CSRF 토큰 값을 담고 있는 HTML `hidden` input 필드를 생성합니다. 예를 들어, [Blade 문법](/docs/12.x/blade)에서 사용할 수 있습니다.

```blade
{{ csrf_field() }}
```

<a name="method-csrf-token"></a>
#### `csrf_token()`

`csrf_token` 함수는 현재 CSRF 토큰 값을 가져옵니다.

```php
$token = csrf_token();
```

<a name="method-decrypt"></a>
#### `decrypt()`

`decrypt` 함수는 주어진 값을 [복호화](/docs/12.x/encryption)합니다. 이 함수는 `Crypt` 파사드의 대안으로 사용할 수 있습니다.

```php
$password = decrypt($value);
```

복호화의 반대 동작인 암호화는 [encrypt](#method-encrypt) 함수를 참고하세요.

<a name="method-dd"></a>
#### `dd()`

`dd` 함수는 전달한 변수들을 출력한 뒤, 스크립트 실행을 즉시 종료합니다.

```php
dd($value);

dd($value1, $value2, $value3, ...);
```

스크립트 실행을 중단하지 않고 변수만 출력하려면 [dump](#method-dump) 함수를 사용하세요.

<a name="method-dispatch"></a>
#### `dispatch()`

`dispatch` 함수는 주어진 [작업(잡, job)](/docs/12.x/queues#creating-jobs)을 라라벨 [잡 큐](/docs/12.x/queues)에 등록합니다.

```php
dispatch(new App\Jobs\SendEmails);
```

<a name="method-dispatch-sync"></a>
#### `dispatch_sync()`

`dispatch_sync` 함수는 주어진 작업을 [동기(sync)](/docs/12.x/queues#synchronous-dispatching) 큐에 넣어 즉시 실행되도록 합니다.

```php
dispatch_sync(new App\Jobs\SendEmails);
```

<a name="method-dump"></a>
#### `dump()`

`dump` 함수는 전달한 변수들을 출력합니다.

```php
dump($value);

dump($value1, $value2, $value3, ...);
```

변수 출력 후 스크립트 실행을 중단하고 싶다면 [dd](#method-dd) 함수를 사용하세요.

<a name="method-encrypt"></a>
#### `encrypt()`

`encrypt` 함수는 주어진 값을 [암호화](/docs/12.x/encryption)합니다. 이 함수는 `Crypt` 파사드의 대안으로 사용할 수 있습니다.

```php
$secret = encrypt('my-secret-value');
```

암호화의 반대 동작인 복호화는 [decrypt](#method-decrypt) 함수를 참고하세요.

<a name="method-env"></a>
#### `env()`

`env` 함수는 [환경 변수](/docs/12.x/configuration#environment-configuration)의 값을 가져오거나, 존재하지 않을 경우 기본값을 반환합니다.

```php
$env = env('APP_ENV');

$env = env('APP_ENV', 'production');
```

> [!WARNING]
> 배포 과정에서 `config:cache` 명령어를 실행했다면, 반드시 `env` 함수를 설정 파일 내에서만 호출해야 합니다. 설정이 캐시된 경우 `.env` 파일은 로드되지 않으므로, `env` 함수로 값을 조회하면 서버나 시스템 레벨의 환경 변수 혹은 `null`만 반환됩니다.

<a name="method-event"></a>
#### `event()`

`event` 함수는 주어진 [이벤트](/docs/12.x/events)를 리스너들에게 디스패치(발송)합니다.

```php
event(new UserRegistered($user));
```

<a name="method-fake"></a>
#### `fake()`

`fake` 함수는 [Faker](https://github.com/FakerPHP/Faker) 싱글톤 인스턴스를 컨테이너에서 반환합니다. 이 함수는 모델 팩토리, 데이터베이스 시딩, 테스트, 프로토타입 뷰 등에서 더미 데이터를 생성할 때 유용합니다.

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

기본적으로 `fake` 함수는 `config/app.php` 설정 파일의 `app.faker_locale` 옵션을 사용합니다. 보통은 환경 변수 `APP_FAKER_LOCALE`로 지정되어 있습니다. 별도의 로케일을 지정해 함수에 전달하면, 각 로케일마다 별도의 싱글톤이 생성됩니다.

```php
fake('nl_NL')->name()
```

<a name="method-filled"></a>
#### `filled()`

`filled` 함수는 주어진 값이 "비어 있지 않은지"를 판별합니다.

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

비어 있는지 판별하는 반대 동작은 [blank](#method-blank) 함수를 참고하세요.

<a name="method-info"></a>
#### `info()`

`info` 함수는 애플리케이션의 [로그](/docs/12.x/logging)에 정보를 기록합니다.

```php
info('Some helpful information!');
```

컨텍스트 데이터(배열)도 함께 전달할 수 있습니다.

```php
info('User login attempt failed.', ['id' => $user->id]);
```

<a name="method-literal"></a>
#### `literal()`

`literal` 함수는 전달된 이름 있는 인수들을 속성(property)으로 가진 새로운 [stdClass](https://www.php.net/manual/en/class.stdclass.php) 인스턴스를 생성합니다.

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

`logger` 함수는 [로그](/docs/12.x/logging)에 `debug` 레벨 메시지를 기록할 수 있습니다.

```php
logger('Debug message');
```

컨텍스트 데이터(배열)를 함께 전달할 수도 있습니다.

```php
logger('User has logged in.', ['id' => $user->id]);
```

만약 함수에 값을 전달하지 않으면, [logger](/docs/12.x/logging) 인스턴스를 반환합니다.

```php
logger()->error('You are not allowed here.');
```

<a name="method-method-field"></a>
#### `method_field()`

`method_field` 함수는 폼의 HTTP 메서드 값을 속인(spoofed) HTML `hidden` input 필드를 생성합니다. 예를 들어, [Blade 문법](/docs/12.x/blade)에서 사용할 수 있습니다.

```blade
<form method="POST">
    {{ method_field('DELETE') }}
</form>
```

<a name="method-now"></a>
#### `now()`

`now` 함수는 현재 시간을 기준으로 새로운 `Illuminate\Support\Carbon` 인스턴스를 생성합니다.

```php
$now = now();
```

<a name="method-old"></a>
#### `old()`

`old` 함수는 세션에 플래시된 [이전 입력값](/docs/12.x/requests#old-input)을 [가져옵니다](/docs/12.x/requests#retrieving-input).

```php
$value = old('value');

$value = old('value', 'default');
```

`old` 함수의 두 번째 인수로 지정한 "기본값"은 대개 Eloquent 모델의 속성인 경우가 많기 때문에, 라라벨에서는 두 번째 인수에 전체 Eloquent 모델을 바로 전달할 수 있도록 허용합니다. 이럴 경우 첫 번째 인수는 "기본값"으로 사용할 Eloquent 속성명을 의미합니다.

```blade
{{ old('name', $user->name) }}

// 아래와 동일합니다.

{{ old('name', $user) }}
```

<a name="method-once"></a>
#### `once()`

`once` 함수는 전달된 콜백을 한 번 실행하고, 결과를 요청(Request)이 끝날 때까지 메모리에 캐시합니다. 동일한 콜백을 사용한 이후의 호출은 이전에 캐시된 결과를 반환합니다.

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

`once` 함수가 어떤 객체의 인스턴스 내부에서 실행될 경우, 캐시된 결과는 객체 인스턴스 단위로 고유하게 관리됩니다.

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

`optional` 함수는 어떤 인수든 받아서, 그 객체의 속성에 접근하거나 메서드를 호출할 수 있게 해줍니다. 만약 해당 객체가 `null`이라면, 속성이나 메서드는 오류를 발생시키는 대신 `null`을 반환합니다.

```php
return optional($user->address)->street;

{!! old('name', optional($user)->name) !!}
```

`optional` 함수에는 두 번째 인수로 클로저(익명 함수)를 넘길 수도 있습니다. 첫 번째 인수로 전달한 값이 null이 아닐 때 클로저가 호출됩니다.

```php
return optional(User::find($id), function (User $user) {
    return $user->name;
});
```

<a name="method-policy"></a>
#### `policy()`

`policy` 함수는 주어진 클래스의 [정책(Policy)](/docs/12.x/authorization#creating-policies) 인스턴스를 반환합니다.

```php
$policy = policy(App\Models\User::class);
```

<a name="method-redirect"></a>
#### `redirect()`

`redirect` 함수는 [리다이렉트 HTTP 응답](/docs/12.x/responses#redirects)을 반환하거나, 아무 인수도 없이 호출하면 리다이렉터 인스턴스를 반환합니다.

```php
return redirect($to = null, $status = 302, $headers = [], $secure = null);

return redirect('/home');

return redirect()->route('route.name');
```

<a name="method-report"></a>
#### `report()`

`report` 함수는 애플리케이션의 [예외 핸들러](/docs/12.x/errors#handling-exceptions)를 통해 예외를 보고합니다.

```php
report($e);
```

`report` 함수에는 문자열을 인수로 넘길 수도 있습니다. 함수에 문자열이 전달되면, 해당 문자열을 메시지로 갖는 예외를 생성하여 보고합니다.

```php
report('Something went wrong.');
```

<a name="method-report-if"></a>
#### `report_if()`

`report_if` 함수는 주어진 불리언 표현식이 `true`일 경우, 애플리케이션의 [예외 핸들러](/docs/12.x/errors#handling-exceptions)를 통해 예외를 보고합니다.

```php
report_if($shouldReport, $e);

report_if($shouldReport, 'Something went wrong.');
```

<a name="method-report-unless"></a>
#### `report_unless()`

`report_unless` 함수는 주어진 불리언 표현식이 `false`일 경우, 애플리케이션의 [예외 핸들러](/docs/12.x/errors#handling-exceptions)를 통해 예외를 보고합니다.

```php
report_unless($reportingDisabled, $e);

report_unless($reportingDisabled, 'Something went wrong.');
```

<a name="method-request"></a>
#### `request()`

`request` 함수는 현재 [요청 인스턴스](/docs/12.x/requests)를 반환하거나, 현재 요청에서 입력 필드의 값을 얻을 수 있습니다.

```php
$request = request();

$value = request('key', $default);
```

<a name="method-rescue"></a>
#### `rescue()`

`rescue` 함수는 전달한 클로저를 실행하면서 예외가 발생하면 해당 예외를 잡아 처리합니다. 잡힌 모든 예외는 [예외 핸들러](/docs/12.x/errors#handling-exceptions)로 전달되지만, 요청 처리는 계속 진행됩니다.

```php
return rescue(function () {
    return $this->method();
});
```

`rescue` 함수에는 두 번째 인수를 전달할 수 있습니다. 이 인수는 클로저 실행 중 예외가 발생할 때 반환될 "기본값"입니다.

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

`rescue` 함수에는 `report` 인수를 전달하여, 해당 예외가 `report` 함수를 통해 보고되어야 하는지 여부를 결정할 수도 있습니다.

```php
return rescue(function () {
    return $this->method();
}, report: function (Throwable $throwable) {
    return $throwable instanceof InvalidArgumentException;
});
```

<a name="method-resolve"></a>
#### `resolve()`

`resolve` 함수는 [서비스 컨테이너](/docs/12.x/container)를 사용하여 주어진 클래스 또는 인터페이스명을 인스턴스로 해결합니다.

```php
$api = resolve('HelpSpot\API');
```

<a name="method-response"></a>
#### `response()`

`response` 함수는 [응답](/docs/12.x/responses) 인스턴스를 생성하거나, 응답 팩토리 인스턴스를 반환합니다.

```php
return response('Hello World', 200, $headers);

return response()->json(['foo' => 'bar'], 200, $headers);
```

<a name="method-retry"></a>
#### `retry()`

`retry` 함수는 지정한 최대 횟수까지 주어진 콜백을 실행하려 시도합니다. 콜백이 예외를 던지지 않으면 그 반환값을 돌려주고, 예외를 던지면 자동으로 재시도합니다. 최대 시도 횟수를 초과하면 예외가 던져집니다.

```php
return retry(5, function () {
    // 5회까지 시도하며, 각 시도 사이 100ms 대기...
}, 100);
```

각 시도 사이의 대기 시간(밀리초)을 직접 계산하고 싶다면, `retry` 함수의 세 번째 인수로 클로저를 전달할 수 있습니다.

```php
use Exception;

return retry(5, function () {
    // ...
}, function (int $attempt, Exception $exception) {
    return $attempt * 100;
});
```

편의를 위해 첫 번째 인수로 배열을 전달할 수도 있습니다. 이 배열은 각 재시도 사이에 대기할 밀리초 단위의 시간으로 사용됩니다.

```php
return retry([100, 200], function () {
    // 첫 번째 재시도는 100ms, 두 번째 재시도는 200ms 대기...
});
```

특정 조건에서만 재시도를 원한다면, `retry` 함수의 네 번째 인수로 클로저를 전달할 수 있습니다.

```php
use App\Exceptions\TemporaryException;
use Exception;

return retry(5, function () {
    // ...
}, 100, function (Exception $exception) {
    return $exception instanceof TemporaryException;
});
```

<a name="method-session"></a>

#### `session()`

`session` 함수는 [세션](/docs/12.x/session) 값을 가져오거나 설정할 때 사용할 수 있습니다.

```php
$value = session('key');
```

키-값 쌍의 배열을 함수에 전달하면 값을 설정할 수 있습니다.

```php
session(['chairs' => 7, 'instruments' => 3]);
```

함수에 값을 전달하지 않으면 세션 스토어가 반환됩니다.

```php
$value = session()->get('key');

session()->put('key', $value);
```

<a name="method-tap"></a>
#### `tap()`

`tap` 함수는 두 개의 인수, 임의의 `$value`와 클로저(Closure)를 받습니다. `$value`가 클로저에 전달된 뒤, 이 함수의 반환값과 상관없이 그대로 `tap` 함수가 반환합니다.

```php
$user = tap(User::first(), function (User $user) {
    $user->name = 'Taylor';

    $user->save();
});
```

만약 `tap` 함수에 클로저를 전달하지 않으면, 전달된 `$value`에 대해 아무 메서드나 호출할 수 있습니다. 해당 메서드가 실제 정의상으로 무엇을 반환하든, 항상 `$value`가 반환됩니다. 예를 들어, Eloquent의 `update` 메서드는 보통 정수를 반환하지만, `tap` 함수를 사용해 메서드를 체이닝하면 강제로 모델 인스턴스 자체를 반환할 수 있습니다.

```php
$user = tap($user)->update([
    'name' => $name,
    'email' => $email,
]);
```

클래스에 `tap` 메서드를 추가하고 싶다면, `Illuminate\Support\Traits\Tappable` 트레이트를 클래스에 추가하면 됩니다. 이 트레이트의 `tap` 메서드는 클로저 하나만 인수로 받으며, 객체 자신이 클로저에 인자로 전달된 뒤 그대로 반환됩니다.

```php
return $user->tap(function (User $user) {
    // ...
});
```

<a name="method-throw-if"></a>
#### `throw_if()`

`throw_if` 함수는 주어진 불리언 표현식의 결과가 `true`일 경우, 지정한 예외를 던집니다.

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

`throw_unless` 함수는 주어진 불리언 표현식의 결과가 `false`일 경우, 지정한 예외를 던집니다.

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

`today` 함수는 현재 날짜의 새로운 `Illuminate\Support\Carbon` 인스턴스를 생성합니다.

```php
$today = today();
```

<a name="method-trait-uses-recursive"></a>
#### `trait_uses_recursive()`

`trait_uses_recursive` 함수는 어떤 트레이트(trait)에서 사용 중인 모든 트레이트들을 반환합니다.

```php
$traits = trait_uses_recursive(\Illuminate\Notifications\Notifiable::class);
```

<a name="method-transform"></a>
#### `transform()`

`transform` 함수는 [blank](#method-blank)가 아닌 주어진 값에 대해 클로저를 실행하고, 그 반환값을 그대로 반환합니다.

```php
$callback = function (int $value) {
    return $value * 2;
};

$result = transform(5, $callback);

// 10
```

세 번째 인수로 기본값 또는 클로저를 함께 전달할 수도 있는데, 이 값은 전달된 값이 blank일 때 반환됩니다.

```php
$result = transform(null, $callback, 'The value is blank');

// The value is blank
```

<a name="method-validator"></a>
#### `validator()`

`validator` 함수는 입력된 인수로 새로운 [유효성 검증기](/docs/12.x/validation) 인스턴스를 만듭니다. 이 함수는 `Validator` 파사드의 대안으로 사용할 수 있습니다.

```php
$validator = validator($data, $rules, $messages);
```

<a name="method-value"></a>
#### `value()`

`value` 함수는 전달받은 값을 그대로 반환합니다. 하지만 만약 클로저를 인수로 전달하면, 해당 클로저가 실행되고, 그 반환값을 반환합니다.

```php
$result = value(true);

// true

$result = value(function () {
    return false;
});

// false
```

추가 인수를 `value` 함수에 전달할 수도 있습니다. 만약 첫 번째 인자가 클로저라면, 나머지 인수들이 클로저의 인수로 전달됩니다. 그렇지 않으면 추가 인수들은 무시됩니다.

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

`with` 함수는 전달된 값을 그대로 반환합니다. 만일 두 번째 인수로 클로저를 넣으면, 해당 클로저가 실행되고 그 반환값이 반환됩니다.

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

`when` 함수는 조건이 `true`로 평가될 때, 전달된 값을 반환합니다. 그렇지 않은 경우 `null`을 반환합니다. 두 번째 인수로 클로저를 전달하면, 해당 클로저가 실행되고 그 결과가 반환됩니다.

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

애플리케이션의 특정 부분의 성능을 빠르게 테스트하고 싶은 경우가 있습니다. 이럴 때는 `Benchmark` 지원 클래스를 이용해서 지정한 콜백이 완료될 때까지 걸린 밀리초(ms) 단위를 측정할 수 있습니다.

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

기본적으로 콜백은 한 번(1회 반복) 실행되며, 실행 소요 시간이 브라우저 또는 콘솔에 표시됩니다.

콜백을 여러 번 반복해서 호출하고 싶다면, 두 번째 인수로 반복 횟수를 지정할 수 있습니다. 콜백을 여러 번 실행하면, `Benchmark` 클래스는 모든 반복 실행에 걸린 평균 소요 시간을 밀리초 단위로 반환합니다.

```php
Benchmark::dd(fn () => User::count(), iterations: 10); // 0.5 ms
```

때로는 콜백 실행 성능을 벤치마킹하면서도, 콜백의 반환값 역시 얻고 싶을 수도 있습니다. 이럴 때는 `value` 메서드를 사용하면 콜백의 반환값과 실행에 소요된 밀리초를 튜플로 반환받을 수 있습니다.

```php
[$count, $duration] = Benchmark::value(fn () => User::count());
```

<a name="dates"></a>
### 날짜와 시간

라라벨은 [Carbon](https://carbon.nesbot.com/docs/)이라는 강력한 날짜와 시간 처리 라이브러리를 내장하고 있습니다. 새로운 `Carbon` 인스턴스를 만들려면 `now` 함수를 호출하면 됩니다. 이 함수는 라라벨 애플리케이션에서 어디서든 사용할 수 있습니다.

```php
$now = now();
```

또는, `Illuminate\Support\Carbon` 클래스를 사용해서 직접 인스턴스를 생성할 수도 있습니다.

```php
use Illuminate\Support\Carbon;

$now = Carbon::now();
```

Carbon의 자세한 기능과 사용 방법은 [공식 Carbon 문서](https://carbon.nesbot.com/docs/)를 참고하시기 바랍니다.

<a name="deferred-functions"></a>
### 지연 함수(Deferred Functions)

라라벨의 [큐 작업](/docs/12.x/queues)을 사용하면 작업을 백그라운드에서 처리할 수 있지만, 드물게는 큐 워커를 따로 구성/관리하지 않고 간단한 작업만 응답 이후로 미루고 싶을 때가 있습니다.

지연 함수는 클로저 실행을 브라우저에 HTTP 응답이 전송된 뒤로 미뤄, 애플리케이션의 반응 속도를 빠르게 유지하도록 도와줍니다. 실행을 미루고 싶은 클로저를 `Illuminate\Support\defer` 함수에 단순히 전달하면 됩니다.

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

기본적으로, 지연 함수는 HTTP 응답, 아티즌 명령어나 큐 작업이 성공적으로 처리된 경우에만 실행됩니다. 즉, 4xx 또는 5xx HTTP 응답으로 끝난 요청에서는 지연 함수가 실행되지 않습니다. 항상 실행되도록 하고 싶다면, 지연 함수에 `always` 메서드를 체이닝하세요.

```php
defer(fn () => Metrics::reportOrder($order))->always();
```

<a name="cancelling-deferred-functions"></a>
#### 지연 함수 취소하기

지연 함수가 실행되기 전에 취소해야 한다면, `forget` 메서드를 사용해 이름으로 해당 함수를 취소할 수 있습니다. 지연 함수에 이름을 지정하려면, `Illuminate\Support\defer` 함수의 두 번째 인수로 이름을 전달하면 됩니다.

```php
defer(fn () => Metrics::report(), 'reportMetrics');

defer()->forget('reportMetrics');
```

<a name="disabling-deferred-functions-in-tests"></a>
#### 테스트에서 지연 함수 비활성화

테스트 코드 작성 시에는 지연 함수를 즉시 실행하도록 비활성화하는 것이 유용할 수 있습니다. 테스트에서 `withoutDefer`를 호출하면, 라라벨이 모든 지연 함수를 바로 실행하게 할 수 있습니다.

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

테스트 케이스의 모든 테스트에서 지연 함수를 비활성화하려면, 기본 `TestCase` 클래스의 `setUp` 메서드에서 `withoutDefer`를 호출하면 됩니다.

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
### Lottery(복권)

라라벨의 Lottery 클래스는 정해진 확률에 따라 콜백을 실행하는 데 사용할 수 있습니다. 이를 통해 전체 요청의 일부에서만 특정 코드를 실행하고 싶을 때 유용합니다.

```php
use Illuminate\Support\Lottery;

Lottery::odds(1, 20)
    ->winner(fn () => $user->won())
    ->loser(fn () => $user->lost())
    ->choose();
```

라라벨의 Lottery 클래스는 다른 기능과도 쉽게 결합할 수 있습니다. 예를 들어, 느린 쿼리를 일부만 예외 핸들러로 보고하려고 할 때 사용할 수 있습니다. Lottery 클래스는 호출 가능한 객체(callable)이기 때문에, calllable을 받을 수 있는 메서드에 인스턴스를 바로 넘길 수도 있습니다.

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

Lottery를 테스트하기 위해, 라라벨은 간단한 메서드들을 제공합니다.

```php
// 항상 Lottery가 당첨되도록 설정...
Lottery::alwaysWin();

// 항상 Lottery가 꽝이 되도록 설정...
Lottery::alwaysLose();

// Lottery가 한 번 당첨되고, 한 번 꽝이 된 후, 다시 기본 동작으로 복귀...
Lottery::fix([true, false]);

// Lottery를 기본 동작으로 복귀...
Lottery::determineResultsNormally();
```

<a name="pipeline"></a>
### 파이프라인(Pipeline)

라라벨의 `Pipeline` 파사드는 지정한 입력값을 일련의 호출 가능(invokable) 클래스, 클로저, 콜러블을 거쳐 전달(파이프)할 수 있는 편리한 방법을 제공합니다. 각 클래스는 입력값을 검토하거나 수정한 뒤, 다음 콜러블을 호출할 수 있습니다.

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

위에서처럼, 파이프라인에 포함된 각 클래스나 클로저는 입력값과 `$next` 클로저를 인수로 받습니다. `$next` 클로저를 호출하면 다음 콜러블이 실행됩니다. 이런 방식은 [미들웨어](/docs/12.x/middleware)와 매우 유사합니다.

마지막 콜러블에서 `$next`를 호출하면, `then` 메서드에 전달된 클로저가 실행됩니다. 대부분의 경우 이 클로저는 처리된 입력값을 그대로 반환하면 됩니다. 만약 별다른 작업 없이 입력값만 반환하고 싶다면 `thenReturn` 메서드를 사용할 수 있습니다.

물론, 클로저 뿐만 아니라 호출 가능한 클래스도 전달할 수 있습니다. 클래스명을 전달하면, 라라벨의 [서비스 컨테이너](/docs/12.x/container)를 통해 인스턴스화되어, 의존성 주입이 가능합니다.

```php
$user = Pipeline::send($user)
    ->through([
        GenerateProfilePhoto::class,
        ActivateSubscription::class,
        SendWelcomeEmail::class,
    ])
    ->thenReturn();
```

<a name="sleep"></a>
### Sleep(일시정지)

라라벨의 `Sleep` 클래스는 PHP의 기본 `sleep`, `usleep` 함수에 가벼운 래퍼 역할을 하여, 테스트가 쉬우면서 개발자 친화적인 API로 시간 지연 처리를 할 수 있도록 해줍니다.

```php
use Illuminate\Support\Sleep;

$waiting = true;

while ($waiting) {
    Sleep::for(1)->second();

    $waiting = /* ... */;
}
```

`Sleep` 클래스는 다양한 시간 단위를 다루는 여러 메서드를 제공합니다.

```php
// 정지 후 값을 반환...
$result = Sleep::for(1)->second()->then(fn () => 1 + 1);

// 지정한 값이 true인 동안 일시정지...
Sleep::for(1)->second()->while(fn () => shouldKeepSleeping());

// 90초간 실행 일시정지...
Sleep::for(1.5)->minutes();

// 2초간 일시정지...
Sleep::for(2)->seconds();

// 500밀리초간 일시정지...
Sleep::for(500)->milliseconds();

// 5,000마이크로초간 일시정지...
Sleep::for(5000)->microseconds();

// 지정한 시간까지 일시정지...
Sleep::until(now()->addMinute());

// PHP의 기본 "sleep" 함수 별칭...
Sleep::sleep(2);

// PHP의 기본 "usleep" 함수 별칭...
Sleep::usleep(5000);
```

시간 단위를 쉽게 조합하려면 `and` 메서드를 사용할 수 있습니다.

```php
Sleep::for(1)->second()->and(10)->milliseconds();
```

<a name="testing-sleep"></a>
#### Sleep 테스트하기

`Sleep` 클래스나 PHP의 기본 sleep 함수를 사용하는 코드를 테스트하면 실제 코드 실행이 일시정지되어 테스트 속도가 심각하게 느려질 수 있습니다. 예를 들면, 아래 코드를 테스트한다고 가정합니다.

```php
$waiting = /* ... */;

$seconds = 1;

while ($waiting) {
    Sleep::for($seconds++)->seconds();

    $waiting = /* ... */;
}
```

통상적으로 이 코드를 테스트하면 _최소_ 1초가 소요됩니다. 하지만 `Sleep` 클래스의 "sleep 가짜 처리(faking)" 기능을 사용하면 테스트 실행 속도를 유지할 수 있습니다.

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

Sleep 클래스가 가짜 처리되면, 실제 실행 일시정지는 건너뛰고 테스트가 훨씬 빨라집니다.

한번 Sleep 클래스를 가짜 처리하면, 코드가 "잠들었어야" 하는 정확한 시퀀스까지 검증할 수 있습니다. 예를 들어, 실행을 세 번 일시정지하며 각 일시정지 시간이 1초씩 증가하는 코드를 테스트한다고 할 때, `assertSequence` 메서드를 사용해 의도한 시간만큼 일시정지되었는지 확인할 수 있습니다.

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

이 외에도 Sleep 클래스를 이용해 다양한 검증을 할 수 있습니다.

```php
use Carbon\CarbonInterval as Duration;
use Illuminate\Support\Sleep;

// sleep이 3번 호출되었는지 검증...
Sleep::assertSleptTimes(3);

// sleep의 지속 시간 검증...
Sleep::assertSlept(function (Duration $duration): bool {
    return /* ... */;
}, times: 1);

// Sleep 클래스가 아예 호출되지 않았는지 검증...
Sleep::assertNeverSlept();

// Sleep이 호출됐더라도 실제 일시정지는 수행되지 않았음을 검증...
Sleep::assertInsomniac();
```

가짜 sleep이 발생했을 때마다 어떤 동작을 하도록 하고 싶을 수도 있습니다. 이때는 `whenFakingSleep` 메서드에 콜백을 제공하면 됩니다. 아래 예시에서는 라라벨의 [시간 조작 헬퍼](/docs/12.x/mocking#interacting-with-time)를 이용해 일시정지 시간만큼 즉시 시간을 이동합니다.

```php
use Carbon\CarbonInterval as Duration;

$this->freezeTime();

Sleep::fake();

Sleep::whenFakingSleep(function (Duration $duration) {
    // Sleep 시 시간 동기화...
    $this->travel($duration->totalMilliseconds)->milliseconds();
});
```

시간 동기화는 자주 필요한 기능이므로, `fake` 메서드의 `syncWithCarbon` 인수를 활용하여 에플리케이션의 시간(Carbon)도 일치시킬 수 있습니다.

```php
Sleep::fake(syncWithCarbon: true);

$start = now();

Sleep::for(1)->second();

$start->diffForHumans(); // 1초 전
```

라라벨에서는 코드의 실행을 일시정지할 때 내부적으로 항상 이 `Sleep` 클래스를 사용합니다. 예를 들어, [retry](#method-retry) 헬퍼도 Sleep 클래스를 활용하여, 더 나은 테스트가 가능하도록 구현되어 있습니다.

<a name="timebox"></a>

### 타임박스 (Timebox)

라라벨의 `Timebox` 클래스는 주어진 콜백이 실제로는 더 빨리 끝나더라도 항상 고정된 시간만큼 실행되도록 보장합니다. 이는 암호화 작업이나 사용자 인증 검사와 같이, 실행 시간의 차이를 악용해 민감한 정보를 추측하려는 공격자를 방지하는 데 특히 유용합니다.

만약 실행 시간이 지정한 고정 시간보다 오래 걸린 경우에는 `Timebox`가 영향을 주지 않습니다. 즉, 최악의 상황을 감안해 충분히 긴 시간을 고정 시간으로 지정하는 것은 개발자의 책임입니다.

`call` 메서드는 클로저(익명 함수)와 마이크로초 단위의 시간 제한을 받아, 해당 클로저를 실행한 뒤 제한 시간이 될 때까지 대기합니다.

```php
use Illuminate\Support\Timebox;

(new Timebox)->call(function ($timebox) {
    // ...
}, microseconds: 10000);
```

클로저 내부에서 예외가 발생하더라도, 이 클래스는 정해진 지연 시간을 반드시 지킨 뒤 예외를 다시 던집니다.

<a name="uri"></a>
### URI

라라벨의 `Uri` 클래스는 URI를 생성하고 다루는 데 편리하고 직관적인 인터페이스를 제공합니다. 이 클래스는 기본적으로 League URI 패키지의 기능을 감싸며, 라라벨의 라우팅 시스템과도 자연스럽게 통합됩니다.

정적 메서드를 통해 쉽게 `Uri` 인스턴스를 만들 수 있습니다.

```php
use App\Http\Controllers\UserController;
use App\Http\Controllers\InvokableController;
use Illuminate\Support\Uri;

// 문자열에서 URI 인스턴스를 생성합니다...
$uri = Uri::of('https://example.com/path');

// 경로, 네임드 라우트, 컨트롤러 액션 등으로부터 URI 인스턴스 생성...
$uri = Uri::to('/dashboard');
$uri = Uri::route('users.show', ['user' => 1]);
$uri = Uri::signedRoute('users.show', ['user' => 1]);
$uri = Uri::temporarySignedRoute('user.index', now()->addMinutes(5));
$uri = Uri::action([UserController::class, 'index']);
$uri = Uri::action(InvokableController::class);

// 현재 요청의 URL에서 URI 인스턴스 생성...
$uri = $request->uri();
```

한 번 URI 인스턴스를 생성했다면, 유창한(fluent) 방식으로 다양한 값을 손쉽게 수정할 수 있습니다.

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
#### URI 구성 요소 확인하기

`Uri` 클래스는 내부 URI의 다양한 구성 요소를 간편하게 확인할 수 있는 메서드들도 제공합니다.

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
#### 쿼리 문자열 조작하기

`Uri` 클래스는 URI의 쿼리 문자열을 조작할 수 있도록 여러 메서드를 제공합니다. `withQuery` 메서드는 기존 쿼리 문자열에 추가로 파라미터들을 병합합니다.

```php
$uri = $uri->withQuery(['sort' => 'name']);
```

`withQueryIfMissing` 메서드는 기존 쿼리 문자열에 주어진 키가 없을 때만 해당 파라미터를 추가합니다.

```php
$uri = $uri->withQueryIfMissing(['page' => 1]);
```

`replaceQuery` 메서드는 기존 쿼리 문자열을 완전히 새로운 값으로 대체합니다.

```php
$uri = $uri->replaceQuery(['page' => 1]);
```

`pushOntoQuery` 메서드는 배열 값을 가진 쿼리 문자열 파라미터에 추가 값을 붙일 때 사용합니다.

```php
$uri = $uri->pushOntoQuery('filter', ['active', 'pending']);
```

`withoutQuery` 메서드는 지정한 파라미터를 쿼리 문자열에서 제거합니다.

```php
$uri = $uri->withoutQuery(['page']);
```

<a name="generating-responses-from-uris"></a>
#### URI에서 응답 생성하기

`redirect` 메서드를 사용하면 해당 URI로 이동하는 `RedirectResponse` 인스턴스를 생성할 수 있습니다.

```php
$uri = Uri::of('https://example.com');

return $uri->redirect();
```

또는, 단순히 라우트나 컨트롤러 액션에서 `Uri` 인스턴스를 반환하면, 해당 URI로 자동으로 리다이렉트하는 응답이 만들어집니다.

```php
use Illuminate\Support\Facades\Route;
use Illuminate\Support\Uri;

Route::get('/redirect', function () {
    return Uri::to('/index')
        ->withQuery(['sort' => 'name']);
});
```