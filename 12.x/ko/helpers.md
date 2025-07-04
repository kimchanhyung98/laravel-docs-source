# 헬퍼 함수 (Helpers)

- [소개](#introduction)
- [사용 가능한 메서드](#available-methods)
- [기타 유틸리티](#other-utilities)
    - [벤치마크 측정](#benchmarking)
    - [날짜](#dates)
    - [지연 함수(Deferred Functions)](#deferred-functions)
    - [로터리](#lottery)
    - [파이프라인](#pipeline)
    - [슬립(Sleep)](#sleep)
    - [타임박스(Timebox)](#timebox)
    - [URI](#uri)

<a name="introduction"></a>
## 소개

라라벨에는 다양한 전역 "헬퍼(helper)" PHP 함수들이 포함되어 있습니다. 이 중 상당수는 프레임워크 내부에서 사용되지만, 여러분이 원한다면 자신의 애플리케이션에서도 자유롭게 활용할 수 있습니다.

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

`Arr::accessible` 메서드는 주어진 값이 배열 형태로 접근 가능한지 여부를 판단합니다.

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

`Arr::add` 메서드는 주어진 배열에서 해당 키가 존재하지 않거나 값이 `null`인 경우, 새로운 키/값 쌍을 배열에 추가합니다.

```php
use Illuminate\Support\Arr;

$array = Arr::add(['name' => 'Desk'], 'price', 100);

// ['name' => 'Desk', 'price' => 100]

$array = Arr::add(['name' => 'Desk', 'price' => null], 'price', 100);

// ['name' => 'Desk', 'price' => 100]
```

<a name="method-array-array"></a>
#### `Arr::array()`

`Arr::array` 메서드는 "dot" 표기법을 사용해 중첩 배열에서 값을 가져옵니다([Arr::get()](#method-array-get)과 동일). 단, 가져온 값이 `array`가 아닌 경우 `InvalidArgumentException`을 발생시킵니다.

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

`Arr::boolean` 메서드는 "dot" 표기법을 사용해 중첩 배열에서 값을 가져옵니다([Arr::get()](#method-array-get)과 동일). 단, 가져온 값이 `boolean`이 아니면 `InvalidArgumentException`을 발생시킵니다.

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

`Arr::collapse` 메서드는 배열 또는 컬렉션이 담긴 배열을 하나의 평면 배열로 병합합니다.

```php
use Illuminate\Support\Arr;

$array = Arr::collapse([[1, 2, 3], [4, 5, 6], [7, 8, 9]]);

// [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

<a name="method-array-crossjoin"></a>
#### `Arr::crossJoin()`

`Arr::crossJoin` 메서드는 여러 배열을 크로스 조인(Cartesian product)하여 가능한 모든 조합을 반환합니다.

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

`Arr::divide` 메서드는 주어진 배열의 키와 값을 각각 별도의 배열로 반환합니다.

```php
use Illuminate\Support\Arr;

[$keys, $values] = Arr::divide(['name' => 'Desk']);

// $keys: ['name']

// $values: ['Desk']
```

<a name="method-array-dot"></a>
#### `Arr::dot()`

`Arr::dot` 메서드는 다차원 배열을 "dot" 표기법(점 표기법)을 이용해 한 단계의 배열로 평탄화(flatten)합니다.

```php
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

$flattened = Arr::dot($array);

// ['products.desk.price' => 100]
```

<a name="method-array-except"></a>
#### `Arr::except()`

`Arr::except` 메서드는 지정한 키/값 쌍을 배열에서 제거합니다.

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

`Arr::first` 메서드는 주어진 조건(진리 테스트)을 만족하는 배열의 첫 번째 요소를 반환합니다.

```php
use Illuminate\Support\Arr;

$array = [100, 200, 300];

$first = Arr::first($array, function (int $value, int $key) {
    return $value >= 150;
});

// 200
```

세 번째 인자로 기본값을 전달할 수도 있으며, 조건을 만족하는 값이 없을 경우 해당 기본값이 반환됩니다.

```php
use Illuminate\Support\Arr;

$first = Arr::first($array, $callback, $default);
```

<a name="method-array-flatten"></a>
#### `Arr::flatten()`

`Arr::flatten` 메서드는 다차원 배열을 하나의 평면 배열로 변환합니다.

```php
use Illuminate\Support\Arr;

$array = ['name' => 'Joe', 'languages' => ['PHP', 'Ruby']];

$flattened = Arr::flatten($array);

// ['Joe', 'PHP', 'Ruby']
```

<a name="method-array-float"></a>
#### `Arr::float()`

`Arr::float` 메서드는 "dot" 표기법으로 중첩 배열에서 값을 가져오며([Arr::get()](#method-array-get)과 동일), 가져온 값이 `float`가 아니라면 `InvalidArgumentException`을 발생시킵니다.

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

`Arr::forget` 메서드는 "dot" 표기법을 이용하여 중첩 배열에서 특정 키/값 쌍을 제거합니다.

```php
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

Arr::forget($array, 'products.desk');

// ['products' => []]
```

<a name="method-array-from"></a>
#### `Arr::from()`

`Arr::from` 메서드는 다양한 입력 값을 일반적인 PHP 배열로 변환합니다. 이 메서드는 배열, 객체, 그리고 라라벨에서 자주 사용되는 `Arrayable`, `Enumerable`, `Jsonable`, `JsonSerializable` 등의 인터페이스 타입을 지원합니다. 또한 `Traversable`과 `WeakMap` 인스턴스도 처리할 수 있습니다.

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

`Arr::get` 메서드는 "dot" 표기법을 이용해 중첩 배열에서 값을 가져옵니다.

```php
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

$price = Arr::get($array, 'products.desk.price');

// 100
```

또한 이 메서드는 지정한 키가 배열에 존재하지 않을 경우 반환할 "기본값"도 세 번째 인자로 전달할 수 있습니다.

```php
use Illuminate\Support\Arr;

$discount = Arr::get($array, 'products.desk.discount', 0);

// 0
```

<a name="method-array-has"></a>
#### `Arr::has()`

`Arr::has` 메서드는 "dot" 표기법을 사용하여 배열에 하나 또는 여러 항목이 존재하는지 확인합니다.

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

`Arr::hasAll` 메서드는 주어진 모든 키가 "dot" 표기법을 이용해 배열 내에 존재하는지 확인합니다.

```php
use Illuminate\Support\Arr;

$array = ['name' => 'Taylor', 'language' => 'PHP'];

Arr::hasAll($array, ['name']); // true
Arr::hasAll($array, ['name', 'language']); // true
Arr::hasAll($array, ['name', 'IDE']); // false
```

<a name="method-array-hasany"></a>

#### `Arr::hasAny()`

`Arr::hasAny` 메서드는 "dot" 표기법을 사용하여 주어진 배열에 지정한 여러 값 중 하나라도 존재하는지 확인합니다:

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

`Arr::integer` 메서드는 "dot" 표기법을 사용해 깊이 중첩된 배열에서 값을 가져옵니다([Arr::get()](#method-array-get)와 사용법이 동일). 하지만 요청한 값이 `int`가 아닐 경우 `InvalidArgumentException` 예외를 발생시킵니다:

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

`Arr::isAssoc` 메서드는 주어진 배열이 연관 배열(associative array)인 경우 `true`를 반환합니다. 배열의 키가 0부터 시작하는 순차적인 정수형이 아니라면 연관 배열로 간주됩니다:

```php
use Illuminate\Support\Arr;

$isAssoc = Arr::isAssoc(['product' => ['name' => 'Desk', 'price' => 100]]);

// true

$isAssoc = Arr::isAssoc([1, 2, 3]);

// false
```

<a name="method-array-islist"></a>
#### `Arr::isList()`

`Arr::isList` 메서드는 주어진 배열의 키가 0부터 시작하는 순차적인 정수일 경우 `true`를 반환합니다:

```php
use Illuminate\Support\Arr;

$isList = Arr::isList(['foo', 'bar', 'baz']);

// true

$isList = Arr::isList(['product' => ['name' => 'Desk', 'price' => 100]]);

// false
```

<a name="method-array-join"></a>
#### `Arr::join()`

`Arr::join` 메서드는 배열의 요소를 문자열로 이어 붙입니다. 두 번째 인수로 일반 구분자를 지정할 수 있으며, 세 번째 인수로 배열의 마지막 요소에는 다른 구분자를 사용할 수 있습니다:

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

`Arr::keyBy` 메서드는 주어진 키의 값을 기준으로 배열의 키를 지정합니다. 동일한 키를 가진 항목이 여러 개 있으면 마지막 항목만 결과 배열에 남게 됩니다:

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

`Arr::last` 메서드는 배열에서 주어진 조건(콜백)에 일치하는 마지막 요소를 반환합니다:

```php
use Illuminate\Support\Arr;

$array = [100, 200, 300, 110];

$last = Arr::last($array, function (int $value, int $key) {
    return $value >= 150;
});

// 300
```

세 번째 인자로 기본값을 전달할 수 있습니다. 조건을 만족하는 값이 없으면 이 기본값이 반환됩니다:

```php
use Illuminate\Support\Arr;

$last = Arr::last($array, $callback, $default);
```

<a name="method-array-map"></a>
#### `Arr::map()`

`Arr::map` 메서드는 배열을 순회하며 각 값과 키를 콜백에 전달합니다. 콜백에서 반환된 값으로 원본 배열의 값을 대체합니다:

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

`Arr::mapSpread` 메서드는 다차원 배열을 순회하면서 각 중첩 아이템의 값을 콜백(클로저)에 분해해 전달합니다. 클로저가 반환한 새 값들로 새로운 배열을 만듭니다:

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

`Arr::mapWithKeys` 메서드는 배열을 순회하면서 각 값에 콜백을 적용합니다. 콜백은 하나의 키/값 쌍을 포함한 연관 배열을 반환해야 합니다:

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

`Arr::only` 메서드는 주어진 배열에서 지정된 키/값 쌍만을 추출하여 반환합니다:

```php
use Illuminate\Support\Arr;

$array = ['name' => 'Desk', 'price' => 100, 'orders' => 10];

$slice = Arr::only($array, ['name', 'price']);

// ['name' => 'Desk', 'price' => 100]
```

<a name="method-array-partition"></a>
#### `Arr::partition()`

`Arr::partition` 메서드는 PHP 배열 디스트럭처링과 함께 사용할 수 있으며, 주어진 조건(콜백)에 따라 요소를 분리하여 반환합니다. 조건을 만족하는 것과 그렇지 않은 것이 각각 별도의 배열로 반환됩니다:

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

`Arr::pluck` 메서드는 배열에서 주어진 키의 모든 값을 추출합니다:

```php
use Illuminate\Support\Arr;

$array = [
    ['developer' => ['id' => 1, 'name' => 'Taylor']],
    ['developer' => ['id' => 2, 'name' => 'Abigail']],
];

$names = Arr::pluck($array, 'developer.name');

// ['Taylor', 'Abigail']
```

결과 리스트를 원하는 키로 지정할 수도 있습니다:

```php
use Illuminate\Support\Arr;

$names = Arr::pluck($array, 'developer.name', 'developer.id');

// [1 => 'Taylor', 2 => 'Abigail']
```

<a name="method-array-prepend"></a>
#### `Arr::prepend()`

`Arr::prepend` 메서드는 배열의 맨 앞에 값을 추가합니다:

```php
use Illuminate\Support\Arr;

$array = ['one', 'two', 'three', 'four'];

$array = Arr::prepend($array, 'zero');

// ['zero', 'one', 'two', 'three', 'four']
```

필요하다면 값을 저장할 때 사용할 키도 지정할 수 있습니다:

```php
use Illuminate\Support\Arr;

$array = ['price' => 100];

$array = Arr::prepend($array, 'Desk', 'name');

// ['name' => 'Desk', 'price' => 100]
```

<a name="method-array-prependkeyswith"></a>
#### `Arr::prependKeysWith()`

`Arr::prependKeysWith` 메서드는 연관 배열(Associative array)의 모든 키 앞에 지정한 접두사를 붙입니다:

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

`Arr::pull` 메서드는 배열에서 지정한 키/값 쌍을 꺼내오면서 해당 키/값을 배열에서 제거합니다:

```php
use Illuminate\Support\Arr;

$array = ['name' => 'Desk', 'price' => 100];

$name = Arr::pull($array, 'name');

// $name: Desk

// $array: ['price' => 100]
```

존재하지 않는 키를 요청할 경우를 대비해 세 번째 인자로 기본값을 전달할 수 있습니다. 해당 키가 없으면 이 값이 반환됩니다:

```php
use Illuminate\Support\Arr;

$value = Arr::pull($array, $key, $default);
```

<a name="method-array-query"></a>
#### `Arr::query()`

`Arr::query` 메서드는 배열을 쿼리 문자열(query string)로 변환합니다:

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

`Arr::random` 메서드는 배열에서 임의의 값을 반환합니다:

```php
use Illuminate\Support\Arr;

$array = [1, 2, 3, 4, 5];

$random = Arr::random($array);

// 4 - (무작위로 추출됨)
```

선택적으로 두 번째 인수로 반환할 항목 개수를 지정할 수 있습니다. 이 인수를 사용할 경우 개수가 1이어도 배열로 반환됩니다:

```php
use Illuminate\Support\Arr;

$items = Arr::random($array, 2);

// [2, 5] - (무작위로 추출됨)
```

<a name="method-array-reject"></a>
#### `Arr::reject()`

`Arr::reject` 메서드는 지정한 클로저(조건)를 만족하는 항목들을 배열에서 제거합니다:

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

`Arr::select` 메서드는 배열에서 원하는 값만 선택된 배열로 반환합니다:

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

`Arr::set` 메서드는 "dot" 표기법을 사용하여 깊이 중첩된 배열의 값을 설정합니다:

```php
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

Arr::set($array, 'products.desk.price', 200);

// ['products' => ['desk' => ['price' => 200]]]
```

<a name="method-array-shuffle"></a>
#### `Arr::shuffle()`

`Arr::shuffle` 메서드는 배열의 항목 순서를 무작위로 섞습니다:

```php
use Illuminate\Support\Arr;

$array = Arr::shuffle([1, 2, 3, 4, 5]);

// [3, 2, 5, 1, 4] - (무작위로 생성됨)
```

<a name="method-array-sole"></a>
#### `Arr::sole()`

`Arr::sole` 메서드는 배열에서 주어진 조건(클로저)에 일치하는 단일 값을 반환합니다. 조건에 맞는 값이 2개 이상이면 `Illuminate\Support\MultipleItemsFoundException` 예외가 발생하며, 조건에 맞는 값이 하나도 없으면 `Illuminate\Support\ItemNotFoundException` 예외가 발생합니다:

```php
use Illuminate\Support\Arr;

$array = ['Desk', 'Table', 'Chair'];

$value = Arr::sole($array, fn (string $value) => $value === 'Desk');

// 'Desk'
```

<a name="method-array-sort"></a>
#### `Arr::sort()`

`Arr::sort` 메서드는 배열을 값 기준으로 오름차순 정렬합니다:

```php
use Illuminate\Support\Arr;

$array = ['Desk', 'Table', 'Chair'];

$sorted = Arr::sort($array);

// ['Chair', 'Desk', 'Table']
```

주어진 클로저의 결과를 기준으로 배열을 정렬할 수도 있습니다:

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

`Arr::sortDesc` 메서드는 배열을 값 기준으로 내림차순 정렬합니다:

```php
use Illuminate\Support\Arr;

$array = ['Desk', 'Table', 'Chair'];

$sorted = Arr::sortDesc($array);

// ['Table', 'Desk', 'Chair']
```

주어진 클로저의 결과를 이용해 배열을 내림차순으로 정렬할 수도 있습니다:

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

`Arr::sortRecursive` 메서드는 배열을 재귀적으로 정렬합니다. 숫자 인덱스를 가진 하위 배열에 대해서는 `sort` 함수를, 연관 배열(associative array)에 대해서는 `ksort` 함수를 사용합니다.

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

결과를 내림차순으로 정렬하고 싶다면 `Arr::sortRecursiveDesc` 메서드를 사용하면 됩니다.

```php
$sorted = Arr::sortRecursiveDesc($array);
```

<a name="method-array-string"></a>
#### `Arr::string()`

`Arr::string` 메서드는 [Arr::get()](#method-array-get)처럼 "점(dot) 표기법"을 사용하여 다차원 배열에서 값을 가져오지만, 요청한 값이 `string` 타입이 아닌 경우에는 `InvalidArgumentException` 예외를 발생시킵니다.

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

`Arr::take` 메서드는 지정된 개수만큼의 아이템으로 구성된 새 배열을 반환합니다.

```php
use Illuminate\Support\Arr;

$array = [0, 1, 2, 3, 4, 5];

$chunk = Arr::take($array, 3);

// [0, 1, 2]
```

음수값을 전달하면 배열의 끝에서부터 해당 개수만큼의 아이템을 가져옵니다.

```php
$array = [0, 1, 2, 3, 4, 5];

$chunk = Arr::take($array, -2);

// [4, 5]
```

<a name="method-array-to-css-classes"></a>
#### `Arr::toCssClasses()`

`Arr::toCssClasses` 메서드는 조건에 따라 CSS 클래스 문자열을 동적으로 조합합니다. 이 메서드는 배열을 받으며, 배열의 키에 추가하고 싶은 클래스명을, 값에는 불리언 표현식을 넣습니다. 배열 요소의 키가 숫자인 경우에는, 해당 값은 무조건 렌더링된 클래스 목록에 포함됩니다.

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

`Arr::toCssStyles` 메서드는 조건에 따라 CSS 스타일 문자열을 동적으로 조합합니다. 동작 방식은 `Arr::toCssClasses`와 동일하며, 배열의 키에 추가하고 싶은 스타일 속성, 값에는 불리언 표현식을 넣습니다. 키가 숫자인 요소는 항상 렌더링되는 스타일 목록에 포함됩니다.

```php
use Illuminate\Support\Arr;

$hasColor = true;

$array = ['background-color: blue', 'color: blue' => $hasColor];

$classes = Arr::toCssStyles($array);

/*
    'background-color: blue; color: blue;'
*/
```

이 메서드는 라라벨의 [Blade 컴포넌트 attribute bag과 클래스 합치기](https://laravel.com/docs/12.x/blade#conditionally-merge-classes) 또는 `@class` [Blade 디렉티브](/docs/12.x/blade#conditional-classes) 같은 기능의 기반이기도 합니다.

<a name="method-array-undot"></a>
#### `Arr::undot()`

`Arr::undot` 메서드는 "점(dot) 표기법"으로 표현된 1차원 배열을 다차원 배열로 변환합니다.

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

`Arr::where` 메서드는 주어진 클로저(익명 함수)를 사용하여 배열을 필터링합니다.

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

`Arr::whereNotNull` 메서드는 배열에서 모든 `null` 값을 제거합니다.

```php
use Illuminate\Support\Arr;

$array = [0, null];

$filtered = Arr::whereNotNull($array);

// [0 => 0]
```

<a name="method-array-wrap"></a>
#### `Arr::wrap()`

`Arr::wrap` 메서드는 지정한 값을 배열로 감싸서 반환합니다. 만약 이미 배열인 값이라면, 해당 배열을 그대로 반환합니다.

```php
use Illuminate\Support\Arr;

$string = 'Laravel';

$array = Arr::wrap($string);

// ['Laravel']
```

지정한 값이 `null`이면 빈 배열을 반환합니다.

```php
use Illuminate\Support\Arr;

$array = Arr::wrap(null);

// []
```

<a name="method-data-fill"></a>
#### `data_fill()`

`data_fill` 함수는 "점(dot) 표기법"을 이용해 중첩 배열이나 객체 내부에 아직 없는 값을 설정합니다.

```php
$data = ['products' => ['desk' => ['price' => 100]]];

data_fill($data, 'products.desk.price', 200);

// ['products' => ['desk' => ['price' => 100]]]

data_fill($data, 'products.desk.discount', 10);

// ['products' => ['desk' => ['price' => 100, 'discount' => 10]]]
```

이 함수는 별표(*)를 와일드카드로 사용할 수도 있으며, 해당 위치에 값을 채워 넣을 수 있습니다.

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

`data_get` 함수는 "점(dot) 표기법"을 사용하여 중첩 배열 또는 객체에서 값을 가져옵니다.

```php
$data = ['products' => ['desk' => ['price' => 100]]];

$price = data_get($data, 'products.desk.price');

// 100
```

`data_get` 함수는 해당 키를 찾지 못할 경우 반환할 기본값도 받을 수 있습니다.

```php
$discount = data_get($data, 'products.desk.discount', 0);

// 0
```

이 함수 또한 별표(*) 와일드카드를 지원하여 배열이나 객체의 모든 키를 대상으로 할 수 있습니다.

```php
$data = [
    'product-one' => ['name' => 'Desk 1', 'price' => 100],
    'product-two' => ['name' => 'Desk 2', 'price' => 150],
];

data_get($data, '*.name');

// ['Desk 1', 'Desk 2'];
```

`{first}` 및 `{last}` 플레이스홀더를 사용하면 배열의 첫 번째 또는 마지막 아이템을 가져올 수 있습니다.

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

`data_set` 함수는 "점(dot) 표기법"을 사용하여 중첩 배열 또는 객체의 값을 설정합니다.

```php
$data = ['products' => ['desk' => ['price' => 100]]];

data_set($data, 'products.desk.price', 200);

// ['products' => ['desk' => ['price' => 200]]]
```

이 함수 또한 별표(*) 와일드카드를 지원하며, 해당 위치의 모든 값을 설정할 수 있습니다.

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

기본적으로 기존 값이 있으면 덮어씁니다. 값이 없을 때만 설정하고 싶다면 네 번째 인자로 `false`를 전달하면 됩니다.

```php
$data = ['products' => ['desk' => ['price' => 100]]];

data_set($data, 'products.desk.price', 200, overwrite: false);

// ['products' => ['desk' => ['price' => 100]]]
```

<a name="method-data-forget"></a>
#### `data_forget()`

`data_forget` 함수는 "점(dot) 표기법"을 이용해 중첩 배열 또는 객체의 값을 제거합니다.

```php
$data = ['products' => ['desk' => ['price' => 100]]];

data_forget($data, 'products.desk.price');

// ['products' => ['desk' => []]]
```

이 함수도 와일드카드(*)를 사용할 수 있어, 지정된 위치의 값들을 한 번에 제거할 수 있습니다.

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

`head` 함수는 주어진 배열의 첫 번째 요소를 반환합니다.

```php
$array = [100, 200, 300];

$first = head($array);

// 100
```

<a name="method-last"></a>
#### `last()`

`last` 함수는 주어진 배열의 마지막 요소를 반환합니다.

```php
$array = [100, 200, 300];

$last = last($array);

// 300
```

<a name="numbers"></a>
## 숫자 (Numbers)

<a name="method-number-abbreviate"></a>
#### `Number::abbreviate()`

`Number::abbreviate` 메서드는 전달받은 수치값을 읽기 쉬운 단위 약어(예: K, M 등)로 변환하여 반환합니다.

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

`Number::clamp` 메서드는 주어진 숫자가 지정한 범위 안에 머물도록 합니다. 숫자가 최소값보다 작으면 최소값이, 최대값보다 크면 최대값이 반환됩니다.

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

`Number::currency` 메서드는 주어진 값을 화폐단위로 포맷하여 문자열로 반환합니다.

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

`Number::defaultCurrency` 메서드는 `Number` 클래스에서 사용 중인 기본 화폐 단위를 반환합니다.

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

`Number::fileSize` 메서드는 전달받은 바이트 단위 값을 사람이 읽기 쉬운 파일 크기(예: KB, MB 등)로 포맷하여 문자열로 반환합니다.

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

`Number::forHumans` 메서드는 숫자 값을 읽기 쉬운 형태(위에서 약어 없이)로 반환합니다.

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

`Number::ordinal` 메서드는 숫자를 서수(ordinal, 예: 1st, 2nd) 형식으로 변환하여 반환합니다.

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

`Number::pairs` 메서드는 지정한 범위와 단계 값(step value)을 기준으로 숫자 쌍(서브 범위) 배열을 생성합니다. 이 메서드는 대량의 숫자 범위를 더 작고 관리하기 쉬운 서브 범위로 나누고 싶을 때, 예를 들어 페이지네이션이나 작업을 여러 묶음으로 분할(batch)할 때 유용하게 사용할 수 있습니다. `pairs` 메서드는 각각의 내부 배열이 숫자 쌍(서브 범위)을 나타내는 배열을 반환합니다:

```php
use Illuminate\Support\Number;

$result = Number::pairs(25, 10);

// [[0, 9], [10, 19], [20, 25]]

$result = Number::pairs(25, 10, offset: 0);

// [[0, 10], [10, 20], [20, 25]]
```

<a name="method-number-parse-int"></a>
#### `Number::parseInt()`

`Number::parseInt` 메서드는 지정한 로케일(locale)에 따라 문자열을 정수(integer)로 변환합니다.

```php
use Illuminate\Support\Number;

$result = Number::parseInt('10.123');

// (int) 10

$result = Number::parseInt('10,123', locale: 'fr');

// (int) 10
```

<a name="method-number-parse-float"></a>
#### `Number::parseFloat()`

`Number::parseFloat` 메서드는 지정한 로케일(locale)에 따라 문자열을 부동 소수점 숫자(float)로 변환합니다.

```php
use Illuminate\Support\Number;

$result = Number::parseFloat('10');

// (float) 10.0

$result = Number::parseFloat('10', locale: 'fr');

// (float) 10.0
```

<a name="method-number-percentage"></a>
#### `Number::percentage()`

`Number::percentage` 메서드는 주어진 값을 문자열 형태의 백분율로 반환합니다.

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

`Number::spell` 메서드는 전달된 숫자를 단어(strings of words)로 변환합니다.

```php
use Illuminate\Support\Number;

$number = Number::spell(102);

// one hundred and two

$number = Number::spell(88, locale: 'fr');

// quatre-vingt-huit
```

`after` 인자를 사용하면 특정 값 이후의 숫자만 단어로 변환하도록 지정할 수 있습니다.

```php
$number = Number::spell(10, after: 10);

// 10

$number = Number::spell(11, after: 10);

// eleven
```

`until` 인자를 사용하면 특정 값 이전의 숫자만 단어로 변환하도록 지정할 수 있습니다.

```php
$number = Number::spell(5, until: 10);

// five

$number = Number::spell(10, until: 10);

// 10
```

<a name="method-number-spell-ordinal"></a>
#### `Number::spellOrdinal()`

`Number::spellOrdinal` 메서드는 숫자의 서수(ordinal, 예: 첫 번째, 두 번째)를 단어로 반환합니다.

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

`Number::trim` 메서드는 전달된 숫자의 소수점 뒤에 붙은 불필요한 0을 제거합니다.

```php
use Illuminate\Support\Number;

$number = Number::trim(12.0);

// 12

$number = Number::trim(12.30);

// 12.3
```

<a name="method-number-use-locale"></a>
#### `Number::useLocale()`

`Number::useLocale` 메서드는 기본 숫자 로케일(locale)을 전역적으로 설정하며, 이후에 `Number` 클래스의 메서드들이 숫자 및 통화를 포맷하는 방식에 영향을 줍니다.

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

`Number::withLocale` 메서드는 지정한 로케일(locale)로 클로저(closure, 콜백)를 실행한 후, 콜백 실행이 끝나면 원래 로케일로 복구합니다.

```php
use Illuminate\Support\Number;

$number = Number::withLocale('de', function () {
    return Number::format(1500);
});
```

<a name="method-number-use-currency"></a>
#### `Number::useCurrency()`

`Number::useCurrency` 메서드는 기본 통화(currency)를 전역적으로 설정하며, 이후 `Number` 클래스의 메서드들이 금액을 포맷하는 방식에 영향을 줍니다.

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

`Number::withCurrency` 메서드는 지정한 통화(currency)로 클로저(closure, 콜백)를 실행한 후, 콜백 실행이 끝나면 원래의 통화로 복구합니다.

```php
use Illuminate\Support\Number;

$number = Number::withCurrency('GBP', function () {
    // ...
});
```

<a name="paths"></a>
## 경로( Paths )

<a name="method-app-path"></a>
#### `app_path()`

`app_path` 함수는 애플리케이션의 `app` 디렉터리에 대한 전체 경로를 반환합니다. 또한, `app_path` 함수를 사용해 애플리케이션 디렉터리 기준으로 상대 경로를 가진 파일의 전체 경로도 만들 수 있습니다.

```php
$path = app_path();

$path = app_path('Http/Controllers/Controller.php');
```

<a name="method-base-path"></a>
#### `base_path()`

`base_path` 함수는 애플리케이션의 루트 디렉터리에 대한 전체 경로를 반환합니다. 또한, 이 함수를 사용해 프로젝트 루트 기준의 파일 전체 경로도 만들 수 있습니다.

```php
$path = base_path();

$path = base_path('vendor/bin');
```

<a name="method-config-path"></a>
#### `config_path()`

`config_path` 함수는 애플리케이션 `config` 디렉터리의 전체 경로를 반환합니다. 또한, 이 함수를 이용해 설정 디렉터리 내의 특정 파일의 전체 경로도 만들 수 있습니다.

```php
$path = config_path();

$path = config_path('app.php');
```

<a name="method-database-path"></a>
#### `database_path()`

`database_path` 함수는 애플리케이션의 `database` 디렉터리 전체 경로를 반환합니다. 또한, 이 함수를 사용해 데이터베이스 디렉터리 내 파일의 전체 경로를 만들 수 있습니다.

```php
$path = database_path();

$path = database_path('factories/UserFactory.php');
```

<a name="method-lang-path"></a>
#### `lang_path()`

`lang_path` 함수는 애플리케이션의 `lang` 디렉터리 전체 경로를 반환합니다. 또한, 이 함수를 사용해 해당 디렉터리 내 파일의 전체 경로도 만들 수 있습니다.

```php
$path = lang_path();

$path = lang_path('en/messages.php');
```

> [!NOTE]
> 기본적으로, 라라벨 애플리케이션의 스켈레톤에는 `lang` 디렉터리가 포함되어 있지 않습니다. 라라벨의 언어 파일을 커스터마이즈하고 싶다면, `lang:publish` 아티즌 명령어를 통해 언어 파일을 퍼블리시할 수 있습니다.

<a name="method-public-path"></a>
#### `public_path()`

`public_path` 함수는 애플리케이션의 `public` 디렉터리 전체 경로를 반환합니다. 또한, 이 함수를 사용해 퍼블릭 디렉터리 내 파일의 전체 경로도 구할 수 있습니다.

```php
$path = public_path();

$path = public_path('css/app.css');
```

<a name="method-resource-path"></a>
#### `resource_path()`

`resource_path` 함수는 애플리케이션의 `resources` 디렉터리 전체 경로를 반환합니다. 또한, 이 함수를 사용해 리소스 디렉터리 내 특정 파일의 전체 경로를 만들 수 있습니다.

```php
$path = resource_path();

$path = resource_path('sass/app.scss');
```

<a name="method-storage-path"></a>
#### `storage_path()`

`storage_path` 함수는 애플리케이션의 `storage` 디렉터리 전체 경로를 반환합니다. 또한, 이 함수를 사용해 스토리지 디렉터리 내 특정 파일의 전체 경로도 얻을 수 있습니다.

```php
$path = storage_path();

$path = storage_path('app/file.txt');
```

<a name="urls"></a>
## URL

<a name="method-action"></a>
#### `action()`

`action` 함수는 주어진 컨트롤러 액션에 대한 URL을 생성합니다.

```php
use App\Http\Controllers\HomeController;

$url = action([HomeController::class, 'index']);
```

해당 메서드가 라우트 매개변수(route parameters)를 받는 경우, 두 번째 인자로 전달할 수 있습니다.

```php
$url = action([UserController::class, 'profile'], ['id' => 1]);
```

<a name="method-asset"></a>
#### `asset()`

`asset` 함수는 현재 요청의 스킴(HTTP 또는 HTTPS)에 따라 자산(asset)의 URL을 생성합니다.

```php
$url = asset('img/photo.jpg');
```

자산 URL의 호스트를 `.env` 파일의 `ASSET_URL` 변수로 설정할 수 있습니다. 이 기능은 예를 들어 Amazon S3 또는 외부 CDN과 같은 외부 서비스에 에셋을 저장하고 관리할 때 유용합니다.

```php
// ASSET_URL=http://example.com/assets

$url = asset('img/photo.jpg'); // http://example.com/assets/img/photo.jpg
```

<a name="method-route"></a>
#### `route()`

`route` 함수는 주어진 [이름이 지정된 라우트](/docs/12.x/routing#named-routes)에 대한 URL을 생성합니다.

```php
$url = route('route.name');
```

라우트가 파라미터를 받는 경우, 두 번째 인자로 전달할 수 있습니다.

```php
$url = route('route.name', ['id' => 1]);
```

기본적으로 `route` 함수는 절대 URL을 생성합니다. 상대 URL을 생성하고 싶다면, 세 번째 인자로 `false`를 전달하면 됩니다.

```php
$url = route('route.name', ['id' => 1], false);
```

<a name="method-secure-asset"></a>
#### `secure_asset()`

`secure_asset` 함수는 HTTPS를 이용해 자산(asset) URL을 생성합니다.

```php
$url = secure_asset('img/photo.jpg');
```

<a name="method-secure-url"></a>
#### `secure_url()`

`secure_url` 함수는 주어진 경로에 대한 완전한 HTTPS URL을 생성합니다. 추가 URL 세그먼트도 두 번째 인자로 전달할 수 있습니다.

```php
$url = secure_url('user/profile');

$url = secure_url('user/profile', [1]);
```

<a name="method-to-route"></a>
#### `to_route()`

`to_route` 함수는 주어진 [이름이 지정된 라우트](/docs/12.x/routing#named-routes)에 대한 [리다이렉트 HTTP 응답](/docs/12.x/responses#redirects)을 생성합니다.

```php
return to_route('users.show', ['user' => 1]);
```

필요하다면 리다이렉트에 사용할 HTTP 상태 코드와, 추가적인 응답 헤더를 세 번째, 네 번째 인자로 전달할 수 있습니다.

```php
return to_route('users.show', ['user' => 1], 302, ['X-Framework' => 'Laravel']);
```

<a name="method-uri"></a>
#### `uri()`

`uri` 함수는 주어진 URI에 대해 [fluent URI 인스턴스](#uri)를 생성합니다.

```php
$uri = uri('https://example.com')
    ->withPath('/users')
    ->withQuery(['page' => 1]);
```

`uri` 함수에 호출 가능한(callable) 컨트롤러와 메서드의 배열을 전달하면 해당 컨트롤러 메서드 라우트의 경로에 대한 `Uri` 인스턴스를 만들어줍니다.

```php
use App\Http\Controllers\UserController;

$uri = uri([UserController::class, 'show'], ['user' => $user]);
```

컨트롤러가 invokable할 경우, 클래스 이름만 전달해도 됩니다.

```php
use App\Http\Controllers\UserIndexController;

$uri = uri(UserIndexController::class);
```

`uri` 함수에 전달한 값이 [이름이 지정된 라우트](/docs/12.x/routing#named-routes)와 일치하는 경우, 해당 라우트 경로에 대한 `Uri` 인스턴스가 생성됩니다.

```php
$uri = uri('users.show', ['user' => $user]);
```

<a name="method-url"></a>
#### `url()`

`url` 함수는 주어진 경로에 대한 완전한 URL을 생성합니다.

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

`url` 함수에 대한 더 자세한 내용은 [URL 생성 문서](/docs/12.x/urls#generating-urls)를 참고하세요.

<a name="miscellaneous"></a>
## 기타

<a name="method-abort"></a>
#### `abort()`

`abort` 함수는 [HTTP 예외](/docs/12.x/errors#http-exceptions)를 발생시키며, 이는 [예외 핸들러](/docs/12.x/errors#handling-exceptions)에 의해 렌더링됩니다.

```php
abort(403);
```

예외 메시지와, 브라우저로 전송할 커스텀 HTTP 응답 헤더도 함께 전달할 수 있습니다.

```php
abort(403, 'Unauthorized.', $headers);
```

<a name="method-abort-if"></a>
#### `abort_if()`

`abort_if` 함수는 주어진 불리언 식(boolean expression)이 `true`로 평가될 경우 HTTP 예외를 발생시킵니다.

```php
abort_if(! Auth::user()->isAdmin(), 403);
```

`abort` 메서드와 마찬가지로, 세 번째 인자로 예외 메시지, 네 번째 인자로 커스텀 응답 헤더 배열도 전달할 수 있습니다.

<a name="method-abort-unless"></a>
#### `abort_unless()`

`abort_unless` 함수는 주어진 불리언 식이 `false`로 평가될 때 HTTP 예외를 발생시킵니다.

```php
abort_unless(Auth::user()->isAdmin(), 403);
```

`abort` 메서드와 마찬가지로, 세 번째 인자로 예외 메시지, 네 번째 인자로 커스텀 응답 헤더 배열도 전달할 수 있습니다.

<a name="method-app"></a>
#### `app()`

`app` 함수는 [서비스 컨테이너](/docs/12.x/container) 인스턴스를 반환합니다.

```php
$container = app();
```

클래스 또는 인터페이스 이름을 전달해 컨테이너에서 해당 인스턴스를 해결할 수 있습니다.

```php
$api = app('HelpSpot\API');
```

<a name="method-auth"></a>
#### `auth()`

`auth` 함수는 [인증기](/docs/12.x/authentication) 인스턴스를 반환합니다. `Auth` 파사드의 대체용으로 사용할 수 있습니다.

```php
$user = auth()->user();
```

필요하다면, 접근하고자 하는 가드(guard) 인스턴스를 직접 지정할 수 있습니다.

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

`bcrypt` 함수는 Bcrypt를 사용해 주어진 값을 [해시](/docs/12.x/hashing)합니다. 이 함수는 `Hash` 파사드 대신 사용할 수 있습니다.

```php
$password = bcrypt('my-secret-password');
```

<a name="method-blank"></a>
#### `blank()`

`blank` 함수는 주어진 값이 "비어있는지(blank)"를 판별합니다.

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

`blank`의 반대 역할을 하는 함수는 [filled](#method-filled)입니다.

<a name="method-broadcast"></a>

#### `broadcast()`

`broadcast` 함수는 주어진 [이벤트](/docs/12.x/events)를 그 리스너들에게 [브로드캐스트](/docs/12.x/broadcasting)합니다.

```php
broadcast(new UserRegistered($user));

broadcast(new UserRegistered($user))->toOthers();
```

<a name="method-broadcast-if"></a>
#### `broadcast_if()`

`broadcast_if` 함수는 주어진 불리언 표현식이 `true`로 평가될 경우, 해당 [이벤트](/docs/12.x/events)를 리스너들에게 [브로드캐스트](/docs/12.x/broadcasting)합니다.

```php
broadcast_if($user->isActive(), new UserRegistered($user));

broadcast_if($user->isActive(), new UserRegistered($user))->toOthers();
```

<a name="method-broadcast-unless"></a>
#### `broadcast_unless()`

`broadcast_unless` 함수는 주어진 불리언 표현식이 `false`로 평가될 경우, 해당 [이벤트](/docs/12.x/events)를 리스너들에게 [브로드캐스트](/docs/12.x/broadcasting)합니다.

```php
broadcast_unless($user->isBanned(), new UserRegistered($user));

broadcast_unless($user->isBanned(), new UserRegistered($user))->toOthers();
```

<a name="method-cache"></a>
#### `cache()`

`cache` 함수는 [캐시](/docs/12.x/cache)에서 값을 조회할 때 사용할 수 있습니다. 만약 지정한 키가 캐시 내에 존재하지 않으면, 두 번째 인자로 전달한 기본값이 반환됩니다.

```php
$value = cache('key');

$value = cache('key', 'default');
```

배열 형태의 키/값 쌍을 함수에 전달하면 캐시에 항목을 저장할 수 있습니다. 이때 해당 값이 유효한 시간(초 단위 또는 기간)을 추가로 전달해야 합니다.

```php
cache(['key' => 'value'], 300);

cache(['key' => 'value'], now()->addSeconds(10));
```

<a name="method-class-uses-recursive"></a>
#### `class_uses_recursive()`

`class_uses_recursive` 함수는 특정 클래스와 해당 부모 클래스들이 사용하는 모든 트레이트(trait)를 반환합니다.

```php
$traits = class_uses_recursive(App\Models\User::class);
```

<a name="method-collect"></a>
#### `collect()`

`collect` 함수는 주어진 값을 이용해 [컬렉션](/docs/12.x/collections) 인스턴스를 생성합니다.

```php
$collection = collect(['Taylor', 'Abigail']);
```

<a name="method-config"></a>
#### `config()`

`config` 함수는 [설정](/docs/12.x/configuration) 변수의 값을 가져옵니다. 점( . ) 표기법을 사용해서 파일명과 접근하고자 하는 옵션명을 지정할 수 있으며, 설정 값이 존재하지 않을 경우 반환할 기본값을 두 번째 인자로 전달할 수 있습니다.

```php
$value = config('app.timezone');

$value = config('app.timezone', $default);
```

런타임에서 배열 형태의 키/값 쌍을 전달해 설정 값을 변경할 수도 있습니다. 단, 이 방법은 현재 요청에만 영향을 미치며 실제 설정 파일은 변경되지 않습니다.

```php
config(['app.debug' => true]);
```

<a name="method-context"></a>
#### `context()`

`context` 함수는 현재 [컨텍스트](/docs/12.x/context)에서 값을 가져옵니다. 해당 키가 컨텍스트에 없을 경우 반환할 기본값을 두 번째 인자로 지정할 수 있습니다.

```php
$value = context('trace_id');

$value = context('trace_id', $default);
```

배열 형태의 키/값 쌍을 전달하면 컨텍스트 값도 설정할 수 있습니다.

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

`csrf_field` 함수는 CSRF 토큰 값을 담고 있는 HTML `hidden` 입력 필드를 생성합니다. 예를 들어, [Blade 문법](/docs/12.x/blade)에서 다음과 같이 사용할 수 있습니다.

```blade
{{ csrf_field() }}
```

<a name="method-csrf-token"></a>
#### `csrf_token()`

`csrf_token` 함수는 현재의 CSRF 토큰 값을 조회합니다.

```php
$token = csrf_token();
```

<a name="method-decrypt"></a>
#### `decrypt()`

`decrypt` 함수는 주어진 값을 [복호화](/docs/12.x/encryption)합니다. 이 함수는 `Crypt` 파사드의 대안으로 사용할 수 있습니다.

```php
$password = decrypt($value);
```

복호화의 반대 동작에 대해서는 [encrypt](#method-encrypt) 함수를 참고하세요.

<a name="method-dd"></a>
#### `dd()`

`dd` 함수는 전달된 변수를 덤프(dump)하고 즉시 스크립트 실행을 중단합니다.

```php
dd($value);

dd($value1, $value2, $value3, ...);
```

스크립트 실행을 중단하지 않고 변수만 덤프하고 싶다면, [dump](#method-dump) 함수를 사용하세요.

<a name="method-dispatch"></a>
#### `dispatch()`

`dispatch` 함수는 주어진 [잡(job)](/docs/12.x/queues#creating-jobs)을 라라벨 [잡 큐](/docs/12.x/queues)에 푸시합니다.

```php
dispatch(new App\Jobs\SendEmails);
```

<a name="method-dispatch-sync"></a>
#### `dispatch_sync()`

`dispatch_sync` 함수는 지정한 잡(job)을 [sync](/docs/12.x/queues#synchronous-dispatching) 큐에 푸시하여 즉시 처리하도록 합니다.

```php
dispatch_sync(new App\Jobs\SendEmails);
```

<a name="method-dump"></a>
#### `dump()`

`dump` 함수는 전달된 변수의 값을 콘솔에 출력(덤프)합니다.

```php
dump($value);

dump($value1, $value2, $value3, ...);
```

덤프 후에 스크립트 실행을 중단하려면 [dd](#method-dd) 함수를 사용하세요.

<a name="method-encrypt"></a>
#### `encrypt()`

`encrypt` 함수는 주어진 값을 [암호화](/docs/12.x/encryption)합니다. 이 함수는 `Crypt` 파사드의 대안으로 사용할 수 있습니다.

```php
$secret = encrypt('my-secret-value');
```

암호화의 반대 동작에 대해서는 [decrypt](#method-decrypt) 함수를 참고하세요.

<a name="method-env"></a>
#### `env()`

`env` 함수는 [환경 변수](/docs/12.x/configuration#environment-configuration)의 값을 조회하거나, 없을 경우 기본값을 반환합니다.

```php
$env = env('APP_ENV');

$env = env('APP_ENV', 'production');
```

> [!WARNING]
> 배포 과정에서 `config:cache` 명령어를 실행한다면, `env` 함수는 반드시 설정 파일에서만 호출해야 합니다. 한 번 설정 캐시가 생성되면 `.env` 파일은 로드되지 않으며, 이후의 모든 `env` 함수 호출은 서버나 시스템 레벨의 외부 환경 변수 또는 `null` 값을 반환합니다.

<a name="method-event"></a>
#### `event()`

`event` 함수는 지정한 [이벤트](/docs/12.x/events)를 리스너들에게 전달(디스패치)합니다.

```php
event(new UserRegistered($user));
```

<a name="method-fake"></a>
#### `fake()`

`fake` 함수는 [Faker](https://github.com/FakerPHP/Faker) 싱글톤 인스턴스를 컨테이너에서 가져옵니다. 모델 팩토리, 데이터베이스 시드, 테스트, 프로토타입 뷰 등에서 가상 데이터를 생성할 때 유용하게 사용할 수 있습니다.

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

기본적으로 `fake` 함수는 `config/app.php` 설정 파일 내의 `app.faker_locale` 옵션을 사용합니다. 이 값은 주로 `APP_FAKER_LOCALE` 환경 변수를 통해 지정합니다. 별도의 로케일을 지정하려면 `fake` 사용 시 파라미터로 전달하면 됩니다. 각 로케일별로 별도의 싱글톤이 반환됩니다.

```php
fake('nl_NL')->name()
```

<a name="method-filled"></a>
#### `filled()`

`filled` 함수는 주어진 값이 "빈 값(blank)"이 아닌지를 판별합니다.

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

`filled`의 반대 동작은 [blank](#method-blank) 함수를 참고하세요.

<a name="method-info"></a>
#### `info()`

`info` 함수는 애플리케이션의 [로그](/docs/12.x/logging)에 정보를 기록합니다.

```php
info('Some helpful information!');
```

컨텍스트 데이터 배열을 두 번째 인자로 전달할 수도 있습니다.

```php
info('User login attempt failed.', ['id' => $user->id]);
```

<a name="method-literal"></a>
#### `literal()`

`literal` 함수는 지정된 이름 있는 인수를 속성으로 가진 새로운 [stdClass](https://www.php.net/manual/en/class.stdclass.php) 객체를 생성합니다.

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

`logger` 함수는 [로그](/docs/12.x/logging)에 `debug` 레벨 메시지를 기록할 때 사용할 수 있습니다.

```php
logger('Debug message');
```

컨텍스트 데이터 배열을 두 번째 인자로 전달할 수도 있습니다.

```php
logger('User has logged in.', ['id' => $user->id]);
```

아무 인자도 전달하지 않으면 [logger](/docs/12.x/logging) 인스턴스를 반환합니다.

```php
logger()->error('You are not allowed here.');
```

<a name="method-method-field"></a>
#### `method_field()`

`method_field` 함수는 폼의 HTTP 메서드를 속이는(spoof) 역할을 하는 `hidden` 입력 필드를 생성합니다. 예를 들어, [Blade 문법](/docs/12.x/blade)에서는 다음과 같이 사용할 수 있습니다.

```blade
<form method="POST">
    {{ method_field('DELETE') }}
</form>
```

<a name="method-now"></a>
#### `now()`

`now` 함수는 현재 시간의 `Illuminate\Support\Carbon` 인스턴스를 생성합니다.

```php
$now = now();
```

<a name="method-old"></a>
#### `old()`

`old` 함수는 세션에 플래시된 [이전 입력값](/docs/12.x/requests#old-input)을 [조회](/docs/12.x/requests#retrieving-input)합니다.

```php
$value = old('value');

$value = old('value', 'default');
```

`old` 함수의 두 번째 인자로 자주 Eloquent 모델의 속성이 기본값으로 사용되므로, 라라벨에서는 두 번째 인자로 전체 Eloquent 모델을 바로 전달할 수 있습니다. 이 경우 라라벨은 첫 번째 인자를 Eloquent 속성명으로 간주하고, 해당 속성의 값을 "기본값"으로 반환해줍니다.

```blade
{{ old('name', $user->name) }}

// 위 코드는 아래와 동일합니다...

{{ old('name', $user) }}
```

<a name="method-once"></a>
#### `once()`

`once` 함수는 주어진 콜백을 실행하고, 해당 결과를 현재 요청 동안 메모리에 캐시합니다. 동일한 콜백을 사용해 `once`를 여러 번 호출해도 첫 번째 호출 때의 결과가 반환됩니다.

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

`once` 함수가 객체 인스턴스 내부에서 실행될 경우, 해당 객체 인스턴스마다 고유하게 결과가 캐시됩니다.

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

`optional` 함수는 어떤 인수든 받아 해당 객체의 속성에 접근하거나 메서드를 호출할 수 있게 해줍니다. 만약 주어진 객체가 `null`이라면, 속성이나 메서드를 접근해도 오류가 발생하는 대신 `null`이 반환됩니다.

```php
return optional($user->address)->street;

{!! old('name', optional($user)->name) !!}
```

또한 `optional` 함수는 두 번째 인자로 클로저를 받을 수 있습니다. 첫 번째 인자가 `null`이 아닌 경우에만 클로저가 실행됩니다.

```php
return optional(User::find($id), function (User $user) {
    return $user->name;
});
```

<a name="method-policy"></a>
#### `policy()`

`policy` 함수는 지정한 클래스에 대한 [정책(Policy)](/docs/12.x/authorization#creating-policies) 인스턴스를 가져옵니다.

```php
$policy = policy(App\Models\User::class);
```

<a name="method-redirect"></a>
#### `redirect()`

`redirect` 함수는 [리디렉션 HTTP 응답](/docs/12.x/responses#redirects)을 반환하거나, 인자 없이 호출할 경우 리다이렉터 인스턴스를 반환합니다.

```php
return redirect($to = null, $status = 302, $headers = [], $secure = null);

return redirect('/home');

return redirect()->route('route.name');
```

<a name="method-report"></a>
#### `report()`

`report` 함수는 지정한 예외를 [예외 핸들러](/docs/12.x/errors#handling-exceptions)를 통해 보고(로깅)합니다.

```php
report($e);
```

이 함수는 문자열도 인자로 받을 수 있습니다. 문자열이 전달되면 해당 문자열을 메시지로 하는 예외 객체를 생성해서 처리합니다.

```php
report('Something went wrong.');
```

<a name="method-report-if"></a>
#### `report_if()`

`report_if` 함수는 전달된 불리언 표현식이 `true`일 때에만, 예외를 [예외 핸들러](/docs/12.x/errors#handling-exceptions)를 통해 보고합니다.

```php
report_if($shouldReport, $e);

report_if($shouldReport, 'Something went wrong.');
```

<a name="method-report-unless"></a>
#### `report_unless()`

`report_unless` 함수는 전달한 불리언 표현식이 `false`일 때에만, 예외를 [예외 핸들러](/docs/12.x/errors#handling-exceptions)를 통해 보고합니다.

```php
report_unless($reportingDisabled, $e);

report_unless($reportingDisabled, 'Something went wrong.');
```

<a name="method-request"></a>
#### `request()`

`request` 함수는 현재의 [요청](/docs/12.x/requests) 인스턴스를 반환하거나, 현재 요청에서 입력값을 조회할 수 있습니다.

```php
$request = request();

$value = request('key', $default);
```

<a name="method-rescue"></a>
#### `rescue()`

`rescue` 함수는 전달된 클로저를 실행하고, 실행 중 발생하는 예외를 모두 잡아 처리합니다. 포착된 모든 예외는 [예외 핸들러](/docs/12.x/errors#handling-exceptions)로 전달되지만, 요청 처리는 계속 진행됩니다.

```php
return rescue(function () {
    return $this->method();
});
```

`rescue` 함수에 두 번째 인자를 전달하면, 클로저 실행 중 예외가 발생했을 때 반환할 "기본값"으로 사용됩니다.

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

`report` 인자를 추가로 지정해, 특정 조건에서만 예외를 report 함수로 전달하도록 제어할 수도 있습니다.

```php
return rescue(function () {
    return $this->method();
}, report: function (Throwable $throwable) {
    return $throwable instanceof InvalidArgumentException;
});
```

<a name="method-resolve"></a>
#### `resolve()`

`resolve` 함수는 [서비스 컨테이너](/docs/12.x/container)를 이용해, 지정한 클래스나 인터페이스 이름을 해당 인스턴스로 반환합니다.

```php
$api = resolve('HelpSpot\API');
```

<a name="method-response"></a>
#### `response()`

`response` 함수는 [응답](/docs/12.x/responses) 인스턴스를 생성하거나, 응답 팩토리 인스턴스를 가져옵니다.

```php
return response('Hello World', 200, $headers);

return response()->json(['foo' => 'bar'], 200, $headers);
```

<a name="method-retry"></a>
#### `retry()`

`retry` 함수는 지정한 최대 시도 횟수에 도달할 때까지 콜백을 계속 실행하려 시도합니다. 콜백이 예외를 발생시키지 않으면 반환값을 그대로 반환하고, 예외가 발생하면 자동으로 재시도합니다. 최대 시도 횟수를 넘기면 예외가 던져집니다.

```php
return retry(5, function () {
    // 5번 시도하며, 각 시도 사이에 100ms 대기...
}, 100);
```

시도 사이 대기할 밀리초를 수동으로 계산하려면 세 번째 인자로 클로저를 전달할 수 있습니다.

```php
use Exception;

return retry(5, function () {
    // ...
}, function (int $attempt, Exception $exception) {
    return $attempt * 100;
});
```

편의를 위해, 첫 번째 인자로 배열을 전달하면 해당 배열 값들이 각 시도 사이 대기 시간(밀리초)로 사용됩니다.

```php
return retry([100, 200], function () {
    // 첫 번째 재시도에서는 100ms, 두 번째 재시도에서는 200ms 대기...
});
```

특정 조건에서만 재시도하고 싶으면, 네 번째 인자로 클로저를 전달할 수 있습니다.

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

함수에 키/값 쌍으로 이루어진 배열을 전달하면 값을 설정할 수 있습니다.

```php
session(['chairs' => 7, 'instruments' => 3]);
```

만약 함수에 값을 전달하지 않으면, 세션 저장소 인스턴스가 반환됩니다.

```php
$value = session()->get('key');

session()->put('key', $value);
```

<a name="method-tap"></a>
#### `tap()`

`tap` 함수는 두 개의 인수, 임의의 `$value`와 클로저(Closure)를 받습니다. `$value`는 클로저에 전달된 후, `tap` 함수가 그 값을 그대로 반환합니다. 이때 클로저의 반환값은 중요하지 않습니다.

```php
$user = tap(User::first(), function (User $user) {
    $user->name = 'Taylor';

    $user->save();
});
```

만약 `tap` 함수에 클로저를 전달하지 않으면, 주어진 `$value`에 있는 어떤 메서드도 호출할 수 있습니다. 호출한 메서드의 반환값이 무엇이든, `tap` 함수는 항상 원래의 `$value`를 반환합니다. 예를 들어, Eloquent의 `update` 메서드는 보통 정수를 반환하지만, `tap` 함수로 업데이트를 감싸면 항상 모델 인스턴스를 반환합니다.

```php
$user = tap($user)->update([
    'name' => $name,
    'email' => $email,
]);
```

클래스에 `tap` 메서드를 추가하고 싶다면, 클래스에 `Illuminate\Support\Traits\Tappable` 트레잇을 추가하면 됩니다. 이 트레잇의 `tap` 메서드는 클로저 하나만 인수로 받아, 객체 자신을 클로저에 넘기고, 마지막에 그 객체 자신을 반환합니다.

```php
return $user->tap(function (User $user) {
    // ...
});
```

<a name="method-throw-if"></a>
#### `throw_if()`

`throw_if` 함수는 주어진 불리언 표현식이 `true`로 평가되면 지정한 예외를 던집니다.

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

`throw_unless` 함수는 주어진 불리언 표현식이 `false`로 평가되면 지정한 예외를 던집니다.

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

`today` 함수는 현재 날짜를 나타내는 새로운 `Illuminate\Support\Carbon` 인스턴스를 생성합니다.

```php
$today = today();
```

<a name="method-trait-uses-recursive"></a>
#### `trait_uses_recursive()`

`trait_uses_recursive` 함수는 특정 트레잇에서 사용 중인 모든 트레잇 목록을 반환합니다.

```php
$traits = trait_uses_recursive(\Illuminate\Notifications\Notifiable::class);
```

<a name="method-transform"></a>
#### `transform()`

`transform` 함수는 전달된 값이 [blank](#method-blank)가 아닐 때, 해당 값으로 클로저를 실행하고 클로저의 반환값을 다시 반환합니다.

```php
$callback = function (int $value) {
    return $value * 2;
};

$result = transform(5, $callback);

// 10
```

함수의 세 번째 인수로 기본값이나 클로저를 전달할 수 있습니다. 이 경우, 전달된 값이 blank라면 해당 값이 대신 반환됩니다.

```php
$result = transform(null, $callback, 'The value is blank');

// The value is blank
```

<a name="method-validator"></a>
#### `validator()`

`validator` 함수는 전달된 인자를 이용해 새로운 [validator](/docs/12.x/validation) 인스턴스를 생성합니다. 이 함수는 `Validator` 파사드 대신 사용할 수 있습니다.

```php
$validator = validator($data, $rules, $messages);
```

<a name="method-value"></a>
#### `value()`

`value` 함수는 전달 받은 값을 반환합니다. 단, 클로저가 전달되면 클로저를 실행한 후 그 반환값을 반환합니다.

```php
$result = value(true);

// true

$result = value(function () {
    return false;
});

// false
```

추가 인수를 `value` 함수에 전달할 수도 있습니다. 첫 번째 인수가 클로저라면, 추가 인수들은 해당 클로저의 인자로 전달됩니다. 그렇지 않으면 무시됩니다.

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

`with` 함수는 전달받은 값을 그대로 반환합니다. 두 번째 인수로 클로저가 전달되면, 해당 값을 인수로 하여 클로저를 실행하고, 그 결과를 반환합니다.

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

`when` 함수는 주어진 조건이 `true`라면 값을 반환하고, 그렇지 않으면 `null`을 반환합니다. 두 번째 인수로 클로저를 전달하면, 조건이 `true`일 때 그 클로저를 실행한 결과값이 반환됩니다.

```php
$value = when(true, 'Hello World');

$value = when(true, fn () => 'Hello World');
```

`when` 함수는 주로 조건적으로 HTML 속성을 렌더링할 때 유용합니다.

```blade
<div {!! when($condition, 'wire:poll="calculate"') !!}>
    ...
</div>
```

<a name="other-utilities"></a>
## 기타 유틸리티

<a name="benchmarking"></a>
### 벤치마킹

애플리케이션의 특정 부분의 성능을 빠르게 측정하고 싶을 때가 있습니다. 이런 경우, `Benchmark` 지원 클래스를 활용하여 주어진 콜백이 완료되는 데 걸린 밀리초(ms) 시간을 측정할 수 있습니다.

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

기본적으로, 콜백은 1회(한 번) 실행되고 실행에 소요된 시간이 브라우저 또는 콘솔에 표시됩니다.

콜백을 여러 번 실행하여 벤치마킹하고 싶다면, 두 번째 인수로 반복 횟수를 지정할 수 있습니다. 콜백을 여러 번 실행하면, `Benchmark` 클래스는 모든 반복의 평균 실행 시간을 반환합니다.

```php
Benchmark::dd(fn () => User::count(), iterations: 10); // 0.5 ms
```

콜백의 실행 시간을 벤치마킹하면서 콜백의 실제 반환값도 함께 받고 싶을 수 있습니다. `value` 메서드는 콜백의 반환값과 실행에 걸린 시간을 튜플로 반환합니다.

```php
[$count, $duration] = Benchmark::value(fn () => User::count());
```

<a name="dates"></a>
### 날짜

라라벨에는 [Carbon](https://carbon.nesbot.com/docs/)이라는 강력한 날짜 및 시간 조작 라이브러리가 포함되어 있습니다. 새 `Carbon` 인스턴스를 만들려면 `now` 함수를 사용할 수 있습니다. 이 함수는 라라벨 애플리케이션 어디서나 전역으로 사용할 수 있습니다.

```php
$now = now();
```

또는, `Illuminate\Support\Carbon` 클래스를 직접 사용해서 새 인스턴스를 생성할 수도 있습니다.

```php
use Illuminate\Support\Carbon;

$now = Carbon::now();
```

Carbon과 그 기능에 대해 더 자세히 알고 싶다면 [공식 Carbon 문서](https://carbon.nesbot.com/docs/)를 참고하세요.

<a name="deferred-functions"></a>
### 지연 실행 함수(Deferred Functions)

라라벨의 [큐 작업](/docs/12.x/queues)을 통해 백그라운드에서 작업을 처리할 수 있지만, 장기 실행 워커를 별도로 구성하거나 유지 관리하지 않고도 간단한 작업만 추후에 실행하고 싶을 때가 있습니다.

지연 실행 함수는 HTTP 응답이 사용자에게 전송된 후에 클로저를 실행하도록 예약할 수 있습니다. 이를 통해 앱이 더욱 빠르고 반응성 있게 느껴집니다. 클로저를 지연 실행하고 싶다면, 해당 클로저를 `Illuminate\Support\defer` 함수에 전달하면 됩니다.

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

기본적으로, 지연 함수는 `Illuminate\Support\defer`가 호출된 HTTP 응답, 아티즌 명령어나 큐 작업이 정상적으로 완료될 때만 실행됩니다. 즉, 요청이 `4xx` 또는 `5xx` HTTP 응답으로 끝나면 지연 함수는 실행되지 않습니다. 지연 함수가 항상 실행되길 바란다면, 지연 함수에 `always` 메서드를 체이닝할 수 있습니다.

```php
defer(fn () => Metrics::reportOrder($order))->always();
```

<a name="cancelling-deferred-functions"></a>
#### 지연 함수 취소하기

지연 함수가 실행되기 전에 취소해야 할 경우, `forget` 메서드를 이용하여 이름으로 해당 함수를 취소할 수 있습니다. 지연 함수에 이름을 부여하려면, `Illuminate\Support\defer` 함수의 두 번째 인수로 이름을 전달하면 됩니다.

```php
defer(fn () => Metrics::report(), 'reportMetrics');

defer()->forget('reportMetrics');
```

<a name="disabling-deferred-functions-in-tests"></a>
#### 테스트에서 지연 함수 비활성화하기

테스트 작성 시에는 지연 함수 동작을 비활성화하는 것이 유용할 수 있습니다. 테스트에서 `withoutDefer`를 호출하면, 라라벨은 모든 지연 함수를 즉시 실행하도록 처리합니다.

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

특정 테스트 케이스 내의 모든 테스트에서 지연 함수를 비활성화하고 싶다면, 기본 `TestCase` 클래스의 `setUp` 메서드에서 `withoutDefer`를 호출하면 됩니다.

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
### 로터리(Lottery)

라라벨의 로터리 클래스는 주어진 확률(odds)에 따라 콜백을 실행할 때 사용할 수 있습니다. 이는 예를 들어 전체 요청 중 일부에만 특정 코드를 실행하고 싶을 때 유용하게 사용할 수 있습니다.

```php
use Illuminate\Support\Lottery;

Lottery::odds(1, 20)
    ->winner(fn () => $user->won())
    ->loser(fn () => $user->lost())
    ->choose();
```

라라벨의 로터리 클래스를 다른 라라벨 기능과 결합해서 사용할 수도 있습니다. 예를 들어, 발생하는 느린 쿼리의 일부만 예외 핸들러로 보고하고 싶을 수 있습니다. 그리고, 이 로터리 클래스는 호출 가능한(callable) 객체이기 때문에, callable 인수를 받는 어떤 메서드에도 인스턴스를 전달할 수 있습니다.

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
#### 로터리 테스트하기

라라벨은 애플리케이션의 로터리 호출을 손쉽게 테스트할 수 있도록 몇 가지 간단한 메서드를 제공합니다.

```php
// 항상 당첨(성공)으로 처리...
Lottery::alwaysWin();

// 항상 실패로 처리...
Lottery::alwaysLose();

// 한 번은 당첨, 한 번은 실패, 그리고 정상 동작으로...
Lottery::fix([true, false]);

// 로터리를 정상 동작으로 되돌리기...
Lottery::determineResultsNormally();
```

<a name="pipeline"></a>
### 파이프라인(Pipeline)

라라벨의 `Pipeline` 파사드는 주어진 입력값을 일련의 호출 가능한 클래스, 클로저, 또는 callable 객체를 따라 전달("파이프")하는 편리한 방법을 제공합니다. 각 클래스나 클로저(또는 callable)는 입력값을 받아 가공 또는 검사하고, 파이프라인에서 다음 callable을 순차적으로 실행합니다.

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

이처럼 파이프라인의 각 클래스나 클로저는 입력값과 `$next` 클로저를 받습니다. `$next`를 호출하면 파이프라인의 다음 callable이 실행됩니다. 이는 [미들웨어](/docs/12.x/middleware)와 매우 유사합니다.

파이프라인의 마지막 callable이 `$next`를 호출하면, `then` 메서드에 넘긴 callable이 실행됩니다. 일반적으로 이 callable은 가공된 입력값을 단순히 반환합니다. 만약 처리 후 입력값을 바로 반환하는 용도만 필요하다면 `thenReturn` 메서드를 쓸 수 있습니다.

그리고, 함수(클로저) 이외에도 호출 가능한 클래스도 파이프라인에 사용할 수 있습니다. 클래스명을 넘기면 라라벨의 [서비스 컨테이너](/docs/12.x/container)를 통해 인스턴스가 생성되어 의존성 주입도 가능합니다.

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
### Sleep

라라벨의 `Sleep` 클래스는 PHP의 기본 `sleep`, `usleep` 함수에 대한 라이트 래퍼로, 더 나은 테스트 지원과 시간 관련 API를 제공합니다.

```php
use Illuminate\Support\Sleep;

$waiting = true;

while ($waiting) {
    Sleep::for(1)->second();

    $waiting = /* ... */;
}
```

`Sleep` 클래스는 다양한 시간 단위에 맞는 메서드를 제공합니다.

```php
// 일정 시간 후에 값을 반환...
$result = Sleep::for(1)->second()->then(fn () => 1 + 1);

// 주어진 값이 true인 동안 대기...
Sleep::for(1)->second()->while(fn () => shouldKeepSleeping());

// 90초 동안 실행 일시정지...
Sleep::for(1.5)->minutes();

// 2초 동안 일시정지...
Sleep::for(2)->seconds();

// 500밀리초 동안 일시정지...
Sleep::for(500)->milliseconds();

// 5,000마이크로초 동안 일시정지...
Sleep::for(5000)->microseconds();

// 특정 시간까지 일시정지...
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

`Sleep` 클래스나 PHP의 기본 sleep 함수를 사용하는 코드를 테스트할 때, 테스트 실행이 실제로 일시정지됩니다. 이는 테스트 시간을 불필요하게 늘립니다. 예를 들어, 다음과 같은 코드를 테스트한다고 가정해봅시다.

```php
$waiting = /* ... */;

$seconds = 1;

while ($waiting) {
    Sleep::for($seconds++)->seconds();

    $waiting = /* ... */;
}
```

기본적으로 이런 코드는 테스트할 때 _최소_ 1초 이상이 소요됩니다. 하지만 `Sleep` 클래스는 "페이크(fake)" 모드를 지원하여, 테스트 수행 시간을 단축시킬 수 있습니다.

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

이렇게 `Sleep` 클래스를 페이크로 설정하면 실제로 코드 실행이 지연되지 않으므로 테스트가 훨씬 빨라집니다.

페이크 sleep을 사용할 때, "얼마나 sleep이 일어났는지"에 대한 검증도 할 수 있습니다. 예를 들어, 각 pause마다 시간이 1초씩 늘어나면서 총 3번 일시정지되는 코드를 생각해봅시다. `assertSequence` 메서드를 사용하면, 테스트에서 올바른 시간만큼 "sleep"이 일어났는지 검증할 수 있습니다.

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

그 외에도, 테스트 시 사용할 수 있는 다양한 assertion이 제공됩니다.

```php
use Carbon\CarbonInterval as Duration;
use Illuminate\Support\Sleep;

// sleep이 3회 호출되었는지 검증...
Sleep::assertSleptTimes(3);

// sleep한 실제 시간에 대한 검증...
Sleep::assertSlept(function (Duration $duration): bool {
    return /* ... */;
}, times: 1);

// Sleep 클래스가 한 번도 호출되지 않았는지 검증...
Sleep::assertNeverSlept();

// Sleep이 호출되었더라도, 실제 실행 지연이 발생하지 않았는지 검증...
Sleep::assertInsomniac();
```

가짜 sleep이 발생할 때마다 특정 처리를 하고 싶을 수도 있습니다. 이럴 때는 `whenFakingSleep` 메서드에 콜백을 등록하면 됩니다. 아래 예시에서는 라라벨의 [시간 조작 헬퍼](/docs/12.x/mocking#interacting-with-time)를 활용해 각 sleep의 지속시간만큼 시간을 즉시 전진시킵니다.

```php
use Carbon\CarbonInterval as Duration;

$this->freezeTime();

Sleep::fake();

Sleep::whenFakingSleep(function (Duration $duration) {
    // 페이크 sleep 시, 시간을 진행...
    $this->travel($duration->totalMilliseconds)->milliseconds();
});
```

이처럼 시간 동기화가 일반적인 요구라면, `fake` 메서드의 `syncWithCarbon` 인자를 활용하여, 테스트 중 Sleep과 Carbon의 시간이 자동으로 동기화되게 할 수도 있습니다.

```php
Sleep::fake(syncWithCarbon: true);

$start = now();

Sleep::for(1)->second();

$start->diffForHumans(); // 1 second ago
```

라라벨은 내부적으로 실행을 일시정지할 때 항상 `Sleep` 클래스를 사용합니다. 예를 들어, [retry](#method-retry) 헬퍼 함수도 sleep 시 이 클래스를 이용하므로, 헬퍼를 사용할 때 테스트의 용이성이 높아집니다.

<a name="timebox"></a>

### 타임박스

라라벨의 `Timebox` 클래스는 주어진 콜백 함수가 실제 실행이 더 빨리 끝나더라도 **항상 고정된 시간 동안 실행**되도록 보장합니다. 이는 암호화 작업이나 사용자 인증과 같이, 실행 시간의 미세한 차이를 악용해 공격자가 민감한 정보를 추론하지 못하도록 할 때 특히 유용합니다.

실행 시간이 고정 시간보다 길어진 경우에는 `Timebox`가 영향을 미치지 않습니다. 최악의 상황까지 고려할 수 있도록, 충분히 긴 시간을 고정 시간으로 선택하는 것은 개발자의 몫입니다.

`call` 메서드는 클로저와 시간 제한(마이크로초 단위)을 인수로 받아, 클로저를 실행한 뒤 시간 제한이 될 때까지 대기합니다.

```php
use Illuminate\Support\Timebox;

(new Timebox)->call(function ($timebox) {
    // ...
}, microseconds: 10000);
```

클로저 내부에서 예외가 발생하면, 이 클래스는 정의된 지연 시간을 끝까지 지킨 후 예외를 다시 던집니다.

<a name="uri"></a>
### URI

라라벨의 `Uri` 클래스는 URI를 생성하고 조작할 수 있는 간편하고 유연한 인터페이스를 제공합니다. 이 클래스는 기본적으로 League URI 패키지의 기능을 감싸며, 라라벨의 라우팅 시스템과도 자연스럽게 연동됩니다.

정적 메서드를 사용하여 쉽게 `Uri` 인스턴스를 생성할 수 있습니다.

```php
use App\Http\Controllers\UserController;
use App\Http\Controllers\InvokableController;
use Illuminate\Support\Uri;

// 주어진 문자열에서 URI 인스턴스 생성...
$uri = Uri::of('https://example.com/path');

// 경로나, 네임드 라우트, 컨트롤러 액션으로 URI 인스턴스 생성...
$uri = Uri::to('/dashboard');
$uri = Uri::route('users.show', ['user' => 1]);
$uri = Uri::signedRoute('users.show', ['user' => 1]);
$uri = Uri::temporarySignedRoute('user.index', now()->addMinutes(5));
$uri = Uri::action([UserController::class, 'index']);
$uri = Uri::action(InvokableController::class);

// 현재 요청 URL에서 URI 인스턴스 생성...
$uri = $request->uri();
```

`Uri` 인스턴스를 얻은 뒤에는 메서드 체이닝 방식으로 쉽게 값을 변경할 수 있습니다.

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

`Uri` 클래스는 기본 URI의 여러 구성 요소를 직관적으로 확인할 수 있는 메서드를 제공합니다.

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
#### 쿼리 스트링 조작하기

`Uri` 클래스는 URI의 쿼리 스트링을 손쉽게 조작할 수 있도록 여러 메서드를 제공합니다.  
`withQuery` 메서드는 기존 쿼리 스트링에 추가 파라미터를 병합할 때 사용합니다.

```php
$uri = $uri->withQuery(['sort' => 'name']);
```

`withQueryIfMissing` 메서드는, 지정한 키가 이미 존재하지 않을 경우에만 추가 쿼리 파라미터를 병합합니다.

```php
$uri = $uri->withQueryIfMissing(['page' => 1]);
```

`replaceQuery` 메서드는 기존 쿼리 스트링을 완전히 새로운 값으로 대체할 때 사용합니다.

```php
$uri = $uri->replaceQuery(['page' => 1]);
```

`pushOntoQuery` 메서드는 배열 형태의 쿼리 파라미터에 추가 값을 더할 때 사용합니다.

```php
$uri = $uri->pushOntoQuery('filter', ['active', 'pending']);
```

`withoutQuery` 메서드는 쿼리 스트링에서 특정 파라미터를 제거합니다.

```php
$uri = $uri->withoutQuery(['page']);
```

<a name="generating-responses-from-uris"></a>
#### URI에서 응답 생성하기

`redirect` 메서드를 사용하면 해당 URI로 이동하는 `RedirectResponse` 인스턴스를 만들 수 있습니다.

```php
$uri = Uri::of('https://example.com');

return $uri->redirect();
```

또는, 라우트나 컨트롤러 액션에서 `Uri` 인스턴스를 직접 반환하면, 자동으로 해당 URI로 리다이렉트 응답이 생성됩니다.

```php
use Illuminate\Support\Facades\Route;
use Illuminate\Support\Uri;

Route::get('/redirect', function () {
    return Uri::to('/index')
        ->withQuery(['sort' => 'name']);
});
```