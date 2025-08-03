# Helpers

- [소개](#introduction)
- [사용 가능한 메서드](#available-methods)
- [기타 유틸리티](#other-utilities)
    - [벤치마킹](#benchmarking)
    - [날짜](#dates)
    - [지연 실행 함수](#deferred-functions)
    - [복권(Lottery)](#lottery)
    - [파이프라인](#pipeline)
    - [Sleep](#sleep)
    - [Timebox](#timebox)
    - [URI](#uri)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 다양한 전역 "헬퍼" PHP 함수를 포함하고 있습니다. 이 함수들은 프레임워크 자체에서 자주 사용되지만, 여러분께서 편리하다면 애플리케이션에서 자유롭게 사용하실 수 있습니다.

<a name="available-methods"></a>
## 사용 가능한 메서드 (Available Methods)



<a name="arrays-and-objects-method-list"></a>
### 배열 및 객체 (Arrays & Objects)

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
### 경로 (Paths)

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
### URL (URLs)

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
## 배열 및 객체 (Arrays & Objects)

<a name="method-array-accessible"></a>
#### `Arr::accessible()`

`Arr::accessible` 메서드는 주어진 값이 배열 접근 가능한지 여부를 판정합니다:

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

`Arr::add` 메서드는 배열에 주어진 키가 아직 없거나 `null`로 설정되어 있을 때만, 해당 키/값 쌍을 추가합니다:

```php
use Illuminate\Support\Arr;

$array = Arr::add(['name' => 'Desk'], 'price', 100);

// ['name' => 'Desk', 'price' => 100]

$array = Arr::add(['name' => 'Desk', 'price' => null], 'price', 100);

// ['name' => 'Desk', 'price' => 100]
```

<a name="method-array-array"></a>
#### `Arr::array()`

`Arr::array` 메서드는 "dot" 표기법을 사용해 깊게 중첩된 배열에서 값을 가져옵니다([Arr::get()](#method-array-get)와 동일). 다만, 요청한 값이 배열이 아닐 경우 `InvalidArgumentException` 예외를 던집니다:

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

`Arr::boolean` 메서드는 "dot" 표기법으로 깊게 중첩된 배열에서 값을 가져옵니다([Arr::get()](#method-array-get)와 동일). 다만, 요청한 값이 부울형이 아닐 경우 `InvalidArgumentException` 예외를 던집니다:

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

`Arr::collapse` 메서드는 배열들의 배열 또는 컬렉션들을 하나의 배열로 병합합니다:

```php
use Illuminate\Support\Arr;

$array = Arr::collapse([[1, 2, 3], [4, 5, 6], [7, 8, 9]]);

// [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

<a name="method-array-crossjoin"></a>
#### `Arr::crossJoin()`

`Arr::crossJoin` 메서드는 주어진 배열들의 데카르트 곱(Cartesian product)를 생성하여 모든 가능한 조합을 반환합니다:

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

`Arr::divide` 메서드는 주어진 배열에서 키 배열과 값 배열 두 개를 리턴합니다:

```php
use Illuminate\Support\Arr;

[$keys, $values] = Arr::divide(['name' => 'Desk']);

// $keys: ['name']

// $values: ['Desk']
```

<a name="method-array-dot"></a>
#### `Arr::dot()`

`Arr::dot` 메서드는 다차원 배열을 "dot" 표기법 키를 가진 단일 차원 배열로 평탄화합니다:

```php
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

$flattened = Arr::dot($array);

// ['products.desk.price' => 100]
```

<a name="method-array-except"></a>
#### `Arr::except()`

`Arr::except` 메서드는 주어진 배열에서 특정 키/값 쌍들을 제거합니다:

```php
use Illuminate\Support\Arr;

$array = ['name' => 'Desk', 'price' => 100];

$filtered = Arr::except($array, ['price']);

// ['name' => 'Desk']
```

<a name="method-array-exists"></a>
#### `Arr::exists()`

`Arr::exists` 메서드는 주어진 키가 배열에 존재하는지 여부를 검사합니다:

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

`Arr::first` 메서드는 주어진 배열에서 지정한 조건을 만족하는 첫 번째 요소를 반환합니다:

```php
use Illuminate\Support\Arr;

$array = [100, 200, 300];

$first = Arr::first($array, function (int $value, int $key) {
    return $value >= 150;
});

// 200
```

세 번째 인수로 기본값을 전달할 수도 있습니다. 조건에 맞는 요소가 없으면 이 값을 반환합니다:

```php
use Illuminate\Support\Arr;

$first = Arr::first($array, $callback, $default);
```

<a name="method-array-flatten"></a>
#### `Arr::flatten()`

`Arr::flatten` 메서드는 다차원 배열을 단일 차원 배열로 평평하게 만듭니다:

```php
use Illuminate\Support\Arr;

$array = ['name' => 'Joe', 'languages' => ['PHP', 'Ruby']];

$flattened = Arr::flatten($array);

// ['Joe', 'PHP', 'Ruby']
```

<a name="method-array-float"></a>
#### `Arr::float()`

`Arr::float` 메서드는 "dot" 표기법으로 깊게 중첩된 배열에서 값을 가져옵니다([Arr::get()](#method-array-get)와 동일). 다만, 요청한 값이 `float` 타입이 아니면 `InvalidArgumentException` 예외를 던집니다:

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

`Arr::forget` 메서드는 "dot" 표기법으로 깊게 중첩된 배열에서 지정한 키/값 쌍을 제거합니다:

```php
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

Arr::forget($array, 'products.desk');

// ['products' => []]
```

<a name="method-array-from"></a>
#### `Arr::from()`

`Arr::from` 메서드는 여러 입력 타입을 일반 PHP 배열로 변환합니다. 배열, 객체, Laravel의 `Arrayable`, `Enumerable`, `Jsonable`, `JsonSerializable` 인터페이스 구현체, `Traversable`, `WeakMap` 등을 지원합니다:

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

`Arr::get` 메서드는 "dot" 표기법으로 깊게 중첩된 배열에서 값을 가져옵니다:

```php
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

$price = Arr::get($array, 'products.desk.price');

// 100
```

기본값을 지정할 수 있으며, 키가 없으면 기본값이 반환됩니다:

```php
use Illuminate\Support\Arr;

$discount = Arr::get($array, 'products.desk.discount', 0);

// 0
```

<a name="method-array-has"></a>
#### `Arr::has()`

`Arr::has` 메서드는 "dot" 표기법으로 배열 내에 특정 항목이 존재하는지 확인합니다:

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

`Arr::hasAll` 메서드는 지정한 모든 키가 배열에 존재하는지 확인합니다:

```php
use Illuminate\Support\Arr;

$array = ['name' => 'Taylor', 'language' => 'PHP'];

Arr::hasAll($array, ['name']); // true
Arr::hasAll($array, ['name', 'language']); // true
Arr::hasAll($array, ['name', 'IDE']); // false
```

<a name="method-array-hasany"></a>
#### `Arr::hasAny()`

`Arr::hasAny` 메서드는 지정한 키들 중 하나라도 배열에 존재하는지 확인합니다:

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

`Arr::integer` 메서드는 "dot" 표기법으로 깊게 중첩된 배열에서 값을 가져옵니다([Arr::get()](#method-array-get)와 동일). 다만, 요청한 값이 `int` 타입이 아니면 `InvalidArgumentException` 예외를 던집니다:

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

`Arr::isAssoc` 메서드는 배열이 연관 배열인지 여부를 반환합니다. 키가 0부터 시작하는 연속적인 숫자가 아니면 연관 배열로 간주합니다:

```php
use Illuminate\Support\Arr;

$isAssoc = Arr::isAssoc(['product' => ['name' => 'Desk', 'price' => 100]]);

// true

$isAssoc = Arr::isAssoc([1, 2, 3]);

// false
```

<a name="method-array-islist"></a>
#### `Arr::isList()`

`Arr::isList` 메서드는 배열이 키가 0부터 시작하는 연속된 정수인지 여부를 반환합니다:

```php
use Illuminate\Support\Arr;

$isList = Arr::isList(['foo', 'bar', 'baz']);

// true

$isList = Arr::isList(['product' => ['name' => 'Desk', 'price' => 100]]);

// false
```

<a name="method-array-join"></a>
#### `Arr::join()`

`Arr::join` 메서드는 배열 요소들을 문자열로 합칩니다. 세 번째 인수로 마지막 요소 사이에 사용할 구분자를 지정할 수 있습니다:

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

`Arr::keyBy` 메서드는 배열을 주어진 키로 인덱싱하며, 동일 키를 가진 항목이 여러 개 있을 경우 마지막 항목만 남깁니다:

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

`Arr::last` 메서드는 배열에서 조건에 맞는 마지막 요소를 반환합니다:

```php
use Illuminate\Support\Arr;

$array = [100, 200, 300, 110];

$last = Arr::last($array, function (int $value, int $key) {
    return $value >= 150;
});

// 300
```

세 번째 인수로 기본값을 지정할 수 있으며 조건에 맞는 값이 없으면 기본값이 반환됩니다:

```php
use Illuminate\Support\Arr;

$last = Arr::last($array, $callback, $default);
```

<a name="method-array-map"></a>
#### `Arr::map()`

`Arr::map` 메서드는 배열을 반복하며 각 키와 값을 콜백에 전달 후, 콜백 반환값으로 배열 값을 대체합니다:

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

`Arr::mapSpread` 메서드는 중첩 배열의 각 항목을 대상 클로저에 펼쳐 전달해, 변형된 새 배열을 만듭니다:

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

`Arr::mapWithKeys` 메서드는 배열을 반복하며 각 값을 콜백에 전달, 콜백은 키/값 쌍이 담긴 연관 배열 하나를 반환해야 합니다:

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

`Arr::only` 메서드는 지정된 키/값 쌍만 반환합니다:

```php
use Illuminate\Support\Arr;

$array = ['name' => 'Desk', 'price' => 100, 'orders' => 10];

$slice = Arr::only($array, ['name', 'price']);

// ['name' => 'Desk', 'price' => 100]
```

<a name="method-array-partition"></a>
#### `Arr::partition()`

`Arr::partition` 메서드는 PHP 배열 구조 분해와 함께 사용해, 주어진 조건을 통과하는 요소와 그렇지 않은 요소를 분리합니다:

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

`Arr::pluck` 메서드는 배열에서 특정 키의 모든 값을 추출합니다:

```php
use Illuminate\Support\Arr;

$array = [
    ['developer' => ['id' => 1, 'name' => 'Taylor']],
    ['developer' => ['id' => 2, 'name' => 'Abigail']],
];

$names = Arr::pluck($array, 'developer.name');

// ['Taylor', 'Abigail']
```

결과 배열의 키를 지정할 수도 있습니다:

```php
use Illuminate\Support\Arr;

$names = Arr::pluck($array, 'developer.name', 'developer.id');

// [1 => 'Taylor', 2 => 'Abigail']
```

<a name="method-array-prepend"></a>
#### `Arr::prepend()`

`Arr::prepend` 메서드는 배열의 앞부분에 새로운 값을 추가합니다:

```php
use Illuminate\Support\Arr;

$array = ['one', 'two', 'three', 'four'];

$array = Arr::prepend($array, 'zero');

// ['zero', 'one', 'two', 'three', 'four']
```

키를 지정할 수도 있습니다:

```php
use Illuminate\Support\Arr;

$array = ['price' => 100];

$array = Arr::prepend($array, 'Desk', 'name');

// ['name' => 'Desk', 'price' => 100]
```

<a name="method-array-prependkeyswith"></a>
#### `Arr::prependKeysWith()`

`Arr::prependKeysWith` 메서드는 연관 배열의 모든 키 앞에 지정한 접두사를 붙입니다:

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

`Arr::pull` 메서드는 배열에서 키/값 쌍을 반환하면서 제거합니다:

```php
use Illuminate\Support\Arr;

$array = ['name' => 'Desk', 'price' => 100];

$name = Arr::pull($array, 'name');

// $name: Desk

// $array: ['price' => 100]
```

존재하지 않는 키에 대해 기본값을 지정할 수도 있습니다:

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

`Arr::random` 메서드는 배열에서 무작위 값을 반환합니다:

```php
use Illuminate\Support\Arr;

$array = [1, 2, 3, 4, 5];

$random = Arr::random($array);

// 4 - (무작위로 선택된 값)
```

두 번째 인수로 반환할 개수를 지정할 수도 있습니다. 이 경우 결과는 한 개라도 배열로 반환됩니다:

```php
use Illuminate\Support\Arr;

$items = Arr::random($array, 2);

// [2, 5] - (무작위로 선택된 값)
```

<a name="method-array-reject"></a>
#### `Arr::reject()`

`Arr::reject` 메서드는 콜백을 사용해 특정 요소를 걸러냅니다:

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

`Arr::select` 메서드는 배열에서 특정 키들의 값을 선택합니다:

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

`Arr::set` 메서드는 "dot" 표기법을 사용해 깊게 중첩된 배열 내의 값을 설정합니다:

```php
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

Arr::set($array, 'products.desk.price', 200);

// ['products' => ['desk' => ['price' => 200]]]
```

<a name="method-array-shuffle"></a>
#### `Arr::shuffle()`

`Arr::shuffle` 메서드는 배열의 항목을 무작위로 섞습니다:

```php
use Illuminate\Support\Arr;

$array = Arr::shuffle([1, 2, 3, 4, 5]);

// [3, 2, 5, 1, 4] - (무작위로 섞인 배열)
```

<a name="method-array-sole"></a>
#### `Arr::sole()`

`Arr::sole` 메서드는 콜백 조건을 만족하는 단일 값을 반환합니다. 조건에 맞는 값이 여러 개면 `MultipleItemsFoundException`, 없으면 `ItemNotFoundException` 예외를 던집니다:

```php
use Illuminate\Support\Arr;

$array = ['Desk', 'Table', 'Chair'];

$value = Arr::sole($array, fn (string $value) => $value === 'Desk');

// 'Desk'
```

<a name="method-array-sort"></a>
#### `Arr::sort()`

`Arr::sort` 메서드는 배열을 값 기준으로 정렬합니다:

```php
use Illuminate\Support\Arr;

$array = ['Desk', 'Table', 'Chair'];

$sorted = Arr::sort($array);

// ['Chair', 'Desk', 'Table']
```

콜백 결과 값으로 정렬할 수도 있습니다:

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

`Arr::sortDesc` 메서드는 배열을 내림차순으로 정렬합니다:

```php
use Illuminate\Support\Arr;

$array = ['Desk', 'Table', 'Chair'];

$sorted = Arr::sortDesc($array);

// ['Table', 'Desk', 'Chair']
```

콜백 결과 값으로 내림차순 정렬할 수도 있습니다:

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

`Arr::sortRecursive` 메서드는 배열 내부 숫자 인덱스 배열은 `sort`로, 연관 배열은 `ksort`로 재귀 정렬합니다:

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

내림차순으로 정렬하려면 `Arr::sortRecursiveDesc` 메서드를 사용하세요:

```php
$sorted = Arr::sortRecursiveDesc($array);
```

<a name="method-array-string"></a>
#### `Arr::string()`

`Arr::string` 메서드는 "dot" 표기법으로 깊게 중첩된 배열에서 문자열 값을 가져옵니다([Arr::get()](#method-array-get)와 동일). 요청한 값이 문자열이 아니면 `InvalidArgumentException` 예외를 던집니다:

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

`Arr::take` 메서드는 지정 개수만큼 아이템을 포함하는 새 배열을 반환합니다:

```php
use Illuminate\Support\Arr;

$array = [0, 1, 2, 3, 4, 5];

$chunk = Arr::take($array, 3);

// [0, 1, 2]
```

음수도 전달할 수 있으며, 그러면 끝에서부터 지정 개수를 가져옵니다:

```php
$array = [0, 1, 2, 3, 4, 5];

$chunk = Arr::take($array, -2);

// [4, 5]
```

<a name="method-array-to-css-classes"></a>
#### `Arr::toCssClasses()`

`Arr::toCssClasses` 메서드는 조건적 CSS 클래스 문자열을 만듭니다. 배열 키가 클래스명이며 값이 `true`일 때만 클래스가 포함됩니다. 숫자 키는 무조건 포함됩니다:

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

`Arr::toCssStyles` 메서드는 조건적 CSS 스타일 문자열을 만듭니다. 배열 키가 스타일이며 값이 `true`일 때만 포함됩니다. 숫자 키는 무조건 포함됩니다:

```php
use Illuminate\Support\Arr;

$hasColor = true;

$array = ['background-color: blue', 'color: blue' => $hasColor];

$classes = Arr::toCssStyles($array);

/*
    'background-color: blue; color: blue;'
*/
```

이 메서드는 [Blade 컴포넌트 속성 백합 클래스 병합](/docs/12.x/blade#conditionally-merge-classes) 및 `@class` [Blade 디렉티브](/docs/12.x/blade#conditional-classes) 기능에 사용됩니다.

<a name="method-array-undot"></a>
#### `Arr::undot()`

`Arr::undot` 메서드는 "dot" 표기법을 사용하는 단일 차원 배열을 다차원 배열로 확장합니다:

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

`Arr::where` 메서드는 주어진 클로저를 사용해 배열을 필터링합니다:

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

`Arr::whereNotNull` 메서드는 배열 내 모든 `null` 값을 제거합니다:

```php
use Illuminate\Support\Arr;

$array = [0, null];

$filtered = Arr::whereNotNull($array);

// [0 => 0]
```

<a name="method-array-wrap"></a>
#### `Arr::wrap()`

`Arr::wrap` 메서드는 주어진 값을 배열로 감쌉니다. 이미 배열이면 그대로 반환됩니다:

```php
use Illuminate\Support\Arr;

$string = 'Laravel';

$array = Arr::wrap($string);

// ['Laravel']
```

값이 `null`이면 빈 배열이 반환됩니다:

```php
use Illuminate\Support\Arr;

$array = Arr::wrap(null);

// []
```

<a name="method-data-fill"></a>
#### `data_fill()`

`data_fill` 함수는 "dot" 표기법으로 중첩된 배열이나 객체에 값이 비어있으면 지정한 값으로 채웁니다:

```php
$data = ['products' => ['desk' => ['price' => 100]]];

data_fill($data, 'products.desk.price', 200);

// ['products' => ['desk' => ['price' => 100]]]

data_fill($data, 'products.desk.discount', 10);

// ['products' => ['desk' => ['price' => 100, 'discount' => 10]]]
```

별표(*)를 와일드카드로 사용해 일괄 채우기도 가능합니다:

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

`data_get` 함수는 "dot" 표기법으로 중첩된 배열이나 객체에서 값을 가져옵니다:

```php
$data = ['products' => ['desk' => ['price' => 100]]];

$price = data_get($data, 'products.desk.price');

// 100
```

기본값을 지정할 수도 있습니다:

```php
$discount = data_get($data, 'products.desk.discount', 0);

// 0
```

별표(*) 와일드카드를 사용해 배열이나 객체 내의 모든 키를 조회할 수 있습니다:

```php
$data = [
    'product-one' => ['name' => 'Desk 1', 'price' => 100],
    'product-two' => ['name' => 'Desk 2', 'price' => 150],
];

data_get($data, '*.name');

// ['Desk 1', 'Desk 2'];
```

`{first}`와 `{last}` 플레이스홀더로 배열의 첫 번째 또는 마지막 아이템을 조회할 수 있습니다:

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

`data_set` 함수는 "dot" 표기법으로 중첩된 배열이나 객체 내에 값을 설정합니다:

```php
$data = ['products' => ['desk' => ['price' => 100]]];

data_set($data, 'products.desk.price', 200);

// ['products' => ['desk' => ['price' => 200]]]
```

별표(*) 와일드카드를 사용해 일괄적으로 값을 설정할 수도 있습니다:

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

기존 값을 덮어쓰지 않고, 값이 없을 때만 설정하려면 네 번째 인수에 `false`를 전달하세요:

```php
$data = ['products' => ['desk' => ['price' => 100]]];

data_set($data, 'products.desk.price', 200, overwrite: false);

// ['products' => ['desk' => ['price' => 100]]]
```

<a name="method-data-forget"></a>
#### `data_forget()`

`data_forget` 함수는 "dot" 표기법으로 중첩된 배열이나 객체에서 값을 제거합니다:

```php
$data = ['products' => ['desk' => ['price' => 100]]];

data_forget($data, 'products.desk.price');

// ['products' => ['desk' => []]]
```

별표(*) 와일드카드를 사용해 일괄 제거할 수도 있습니다:

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

`head` 함수는 배열의 첫 번째 요소를 반환합니다. 빈 배열일 경우 `false`를 반환합니다:

```php
$array = [100, 200, 300];

$first = head($array);

// 100
```

<a name="method-last"></a>
#### `last()`

`last` 함수는 배열의 마지막 요소를 반환합니다. 빈 배열일 경우 `false`를 반환합니다:

```php
$array = [100, 200, 300];

$last = last($array);

// 300
```

<a name="numbers"></a>
## 숫자 (Numbers)

<a name="method-number-abbreviate"></a>
#### `Number::abbreviate()`

`Number::abbreviate` 메서드는 숫자 값을 단위 약어와 함께 사람에게 읽기 좋은 형태로 반환합니다:

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

`Number::clamp` 메서드는 숫자를 지정된 범위 내에 유지합니다. 최소값 미만이면 최소값, 최대값 초과면 최대값을 반환합니다:

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

`Number::currency` 메서드는 주어진 값을 화폐 형식 문자열로 반환합니다:

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

`Number::defaultCurrency` 메서드는 `Number` 클래스가 기본으로 사용하는 화폐를 반환합니다:

```php
use Illuminate\Support\Number;

$currency = Number::defaultCurrency();

// USD
```

<a name="method-default-locale"></a>
#### `Number::defaultLocale()`

`Number::defaultLocale` 메서드는 `Number` 클래스가 기본으로 사용하는 로케일을 반환합니다:

```php
use Illuminate\Support\Number;

$locale = Number::defaultLocale();

// en
```

<a name="method-number-file-size"></a>
#### `Number::fileSize()`

`Number::fileSize` 메서드는 바이트 크기를 파일 크기 문자열로 반환합니다:

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

`Number::forHumans` 메서드는 숫자 값을 사람이 읽기 좋은 형태로 반환합니다:

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

`Number::format` 메서드는 로케일별 형식으로 숫자를 포맷팅합니다:

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

`Number::ordinal` 메서드는 숫자의 서수 표현을 반환합니다:

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

`Number::pairs` 메서드는 지정된 범위와 간격으로 숫자 쌍 배열(부분 범위)을 생성합니다. 주로 페이징이나 작업 배치에 유용합니다:

```php
use Illuminate\Support\Number;

$result = Number::pairs(25, 10);

// [[0, 9], [10, 19], [20, 25]]

$result = Number::pairs(25, 10, offset: 0);

// [[0, 10], [10, 20], [20, 25]]
```

<a name="method-number-parse-int"></a>
#### `Number::parseInt()`

`Number::parseInt` 메서드는 주어진 문자열을 지정된 로케일에 맞춰 정수로 파싱합니다:

```php
use Illuminate\Support\Number;

$result = Number::parseInt('10.123');

// (int) 10

$result = Number::parseInt('10,123', locale: 'fr');

// (int) 10
```

<a name="method-number-parse-float"></a>
#### `Number::parseFloat()`

`Number::parseFloat` 메서드는 주어진 문자열을 지정된 로케일에 맞춰 부동 소수점 숫자로 파싱합니다:

```php
use Illuminate\Support\Number;

$result = Number::parseFloat('10');

// (float) 10.0

$result = Number::parseFloat('10', locale: 'fr');

// (float) 10.0
```

<a name="method-number-percentage"></a>
#### `Number::percentage()`

`Number::percentage` 메서드는 값을 백분율 문자열로 반환합니다:

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

`Number::spell` 메서드는 숫자를 단어로 변환합니다:

```php
use Illuminate\Support\Number;

$number = Number::spell(102);

// one hundred and two

$number = Number::spell(88, locale: 'fr');

// quatre-vingt-huit
```

`after` 인수로 특정 숫자 이상부터 단어로 변환하게 할 수 있습니다:

```php
$number = Number::spell(10, after: 10);

// 10

$number = Number::spell(11, after: 10);

// eleven
```

`until` 인수로 특정 숫자 이하까지만 단어로 변환하게 할 수 있습니다:

```php
$number = Number::spell(5, until: 10);

// five

$number = Number::spell(10, until: 10);

// 10
```

<a name="method-number-spell-ordinal"></a>
#### `Number::spellOrdinal()`

`Number::spellOrdinal` 메서드는 숫자를 서수 단어로 변환합니다:

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

`Number::trim` 메서드는 소수점 뒤 불필요한 0을 제거합니다:

```php
use Illuminate\Support\Number;

$number = Number::trim(12.0);

// 12

$number = Number::trim(12.30);

// 12.3
```

<a name="method-number-use-locale"></a>
#### `Number::useLocale()`

`Number::useLocale` 메서드는 기본 숫자 로케일을 전역 설정해 이후 `Number` 클래스 메서드에 영향을 줍니다:

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

`Number::withLocale` 메서드는 지정한 로케일로 클로저를 실행하고, 완료 후 원래 로케일로 복원합니다:

```php
use Illuminate\Support\Number;

$number = Number::withLocale('de', function () {
    return Number::format(1500);
});
```

<a name="method-number-use-currency"></a>
#### `Number::useCurrency()`

`Number::useCurrency` 메서드는 기본 화폐 설정을 전역에 적용해 이후 `Number` 클래스 메서드에 영향을 줍니다:

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

`Number::withCurrency` 메서드는 지정한 화폐로 클로저를 실행하고, 완료 후 원래 화폐로 복원합니다:

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

`app_path` 함수는 애플리케이션의 `app` 디렉터리 절대 경로를 반환합니다. 파일 경로를 지정하면 그 상대 경로도 생성됩니다:

```php
$path = app_path();

$path = app_path('Http/Controllers/Controller.php');
```

<a name="method-base-path"></a>
#### `base_path()`

`base_path` 함수는 애플리케이션 루트 디렉터리 절대 경로를 반환합니다. 파일 경로를 지정하면 그 상대 경로도 생성됩니다:

```php
$path = base_path();

$path = base_path('vendor/bin');
```

<a name="method-config-path"></a>
#### `config_path()`

`config_path` 함수는 애플리케이션의 `config` 디렉터리 절대 경로를 반환합니다. 파일 경로를 지정하면 그 상대 경로도 생성됩니다:

```php
$path = config_path();

$path = config_path('app.php');
```

<a name="method-database-path"></a>
#### `database_path()`

`database_path` 함수는 애플리케이션의 `database` 디렉터리 절대 경로를 반환합니다. 파일 경로를 지정하면 그 상대 경로도 생성됩니다:

```php
$path = database_path();

$path = database_path('factories/UserFactory.php');
```

<a name="method-lang-path"></a>
#### `lang_path()`

`lang_path` 함수는 애플리케이션의 `lang` 디렉터리 절대 경로를 반환합니다. 파일 경로를 지정하면 그 상대 경로도 생성됩니다:

```php
$path = lang_path();

$path = lang_path('en/messages.php');
```

> [!NOTE]
> 기본적으로 Laravel 애플리케이션 스켈레톤에는 `lang` 디렉터리가 포함되어 있지 않습니다. 언어 파일을 커스텀하려면 `lang:publish` Artisan 명령어로 발행할 수 있습니다.

<a name="method-public-path"></a>
#### `public_path()`

`public_path` 함수는 애플리케이션의 `public` 디렉터리 절대 경로를 반환합니다. 파일 경로를 지정하면 그 상대 경로도 생성됩니다:

```php
$path = public_path();

$path = public_path('css/app.css');
```

<a name="method-resource-path"></a>
#### `resource_path()`

`resource_path` 함수는 애플리케이션의 `resources` 디렉터리 절대 경로를 반환합니다. 파일 경로를 지정하면 그 상대 경로도 생성됩니다:

```php
$path = resource_path();

$path = resource_path('sass/app.scss');
```

<a name="method-storage-path"></a>
#### `storage_path()`

`storage_path` 함수는 애플리케이션의 `storage` 디렉터리 절대 경로를 반환합니다. 파일 경로를 지정하면 그 상대 경로도 생성됩니다:

```php
$path = storage_path();

$path = storage_path('app/file.txt');
```

<a name="urls"></a>
## URL (URLs)

<a name="method-action"></a>
#### `action()`

`action` 함수는 주어진 컨트롤러 액션에 대한 URL을 생성합니다:

```php
use App\Http\Controllers\HomeController;

$url = action([HomeController::class, 'index']);
```

라우트 매개변수가 필요하면 두 번째 인수로 전달할 수 있습니다:

```php
$url = action([UserController::class, 'profile'], ['id' => 1]);
```

<a name="method-asset"></a>
#### `asset()`

`asset` 함수는 현재 요청의 스킴(HTTP 또는 HTTPS)을 기반으로 자산 URL을 생성합니다:

```php
$url = asset('img/photo.jpg');
```

`.env` 파일에서 `ASSET_URL` 값을 설정하면 외부 CDN 등에서 호스팅하는 자산의 베이스 URL을 지정할 수 있습니다:

```php
// ASSET_URL=http://example.com/assets

$url = asset('img/photo.jpg'); // http://example.com/assets/img/photo.jpg
```

<a name="method-route"></a>
#### `route()`

`route` 함수는 이름 붙은 라우트에 대한 URL을 생성합니다:

```php
$url = route('route.name');
```

라우트 매개변수가 필요하면 두 번째 인수로 전달할 수 있습니다:

```php
$url = route('route.name', ['id' => 1]);
```

기본으로 절대 URL을 반환하며, 상대 URL을 원하면 세 번째 인수에 `false`를 전달하세요:

```php
$url = route('route.name', ['id' => 1], false);
```

<a name="method-secure-asset"></a>
#### `secure_asset()`

`secure_asset` 함수는 HTTPS 스킴 자산 URL을 생성합니다:

```php
$url = secure_asset('img/photo.jpg');
```

<a name="method-secure-url"></a>
#### `secure_url()`

`secure_url` 함수는 주어진 경로에 완전한 HTTPS URL을 생성합니다. 추가 세그먼트는 두 번째 인수로 전달할 수 있습니다:

```php
$url = secure_url('user/profile');

$url = secure_url('user/profile', [1]);
```

<a name="method-to-route"></a>
#### `to_route()`

`to_route` 함수는 이름 붙은 라우트에 대한 [리다이렉트 HTTP 응답](/docs/12.x/responses#redirects)을 생성합니다:

```php
return to_route('users.show', ['user' => 1]);
```

세 번째 인수로 HTTP 상태 코드, 네 번째 인수로 응답 헤더를 전달할 수 있습니다:

```php
return to_route('users.show', ['user' => 1], 302, ['X-Framework' => 'Laravel']);
```

<a name="method-uri"></a>
#### `uri()`

`uri` 함수는 주어진 URI에 대해 [유연한 URI 인스턴스](#uri)를 생성합니다:

```php
$uri = uri('https://example.com')
    ->withPath('/users')
    ->withQuery(['page' => 1]);
```

배열로 컨트롤러와 메서드 콜러블이 전달되면 해당 컨트롤러 액션 라우트 경로의 `Uri` 인스턴스를 만들기도 합니다:

```php
use App\Http\Controllers\UserController;

$uri = uri([UserController::class, 'show'], ['user' => $user]);
```

컨트롤러가 단일 호출 액션이라면 클래스명만 전달할 수 있습니다:

```php
use App\Http\Controllers\UserIndexController;

$uri = uri(UserIndexController::class);
```

라운드 이름과 일치할 경우에는 해당 라우트 경로의 `Uri` 인스턴스를 생성합니다:

```php
$uri = uri('users.show', ['user' => $user]);
```

<a name="method-url"></a>
#### `url()`

`url` 함수는 주어진 경로에 대해 절대 URL을 생성합니다:

```php
$url = url('user/profile');

$url = url('user/profile', [1]);
```

경로가 없으면 `Illuminate\Routing\UrlGenerator` 인스턴스를 반환합니다:

```php
$current = url()->current();

$full = url()->full();

$previous = url()->previous();
```

자세한 내용은 [URL 생성 문서](/docs/12.x/urls#generating-urls)를 참고하세요.

<a name="miscellaneous"></a>
## 기타 (Miscellaneous)

<a name="method-abort"></a>
#### `abort()`

`abort` 함수는 [HTTP 예외](/docs/12.x/errors#http-exceptions)를 던지며, 예외 핸들러가 렌더링합니다:

```php
abort(403);
```

메시지 및 커스텀 HTTP 응답 헤더도 지정할 수 있습니다:

```php
abort(403, 'Unauthorized.', $headers);
```

<a name="method-abort-if"></a>
#### `abort_if()`

`abort_if` 함수는 특정 불리언 표현식이 참이면 HTTP 예외를 던집니다:

```php
abort_if(! Auth::user()->isAdmin(), 403);
```

`abort`와 마찬가지로 메시지와 헤더를 지정할 수 있습니다.

<a name="method-abort-unless"></a>
#### `abort_unless()`

`abort_unless` 함수는 특정 불리언 표현식이 거짓이면 HTTP 예외를 던집니다:

```php
abort_unless(Auth::user()->isAdmin(), 403);
```

`abort`처럼 메시지와 헤더를 지정할 수 있습니다.

<a name="method-app"></a>
#### `app()`

`app` 함수는 [서비스 컨테이너](/docs/12.x/container) 인스턴스를 반환합니다:

```php
$container = app();
```

클래스명이나 인터페이스명을 전달해 인스턴스를 해결할 수도 있습니다:

```php
$api = app('HelpSpot\API');
```

<a name="method-auth"></a>
#### `auth()`

`auth` 함수는 [인증자](/docs/12.x/authentication) 인스턴스를 반환합니다. `Auth` 파사드 대용입니다:

```php
$user = auth()->user();
```

접근할 특정 guard를 지정할 수도 있습니다:

```php
$user = auth('admin')->user();
```

<a name="method-back"></a>
#### `back()`

`back` 함수는 사용자의 이전 위치로 [리다이렉트](/docs/12.x/responses#redirects)를 생성합니다:

```php
return back($status = 302, $headers = [], $fallback = '/');

return back();
```

<a name="method-bcrypt"></a>
#### `bcrypt()`

`bcrypt` 함수는 주어진 값을 Bcrypt 해시합니다. `Hash` 파사드 대신 사용할 수 있습니다:

```php
$password = bcrypt('my-secret-password');
```

<a name="method-blank"></a>
#### `blank()`

`blank` 함수는 주어진 값이 "빈 값"인지 판정합니다:

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

`blank`의 반대는 [filled](#method-filled) 함수입니다.

<a name="method-broadcast"></a>
#### `broadcast()`

`broadcast` 함수는 주어진 [이벤트](/docs/12.x/events)를 수신자에게 방송합니다:

```php
broadcast(new UserRegistered($user));

broadcast(new UserRegistered($user))->toOthers();
```

<a name="method-broadcast-if"></a>
#### `broadcast_if()`

`broadcast_if` 함수는 지정된 불리언이 참일 경우 이벤트를 방송합니다:

```php
broadcast_if($user->isActive(), new UserRegistered($user));

broadcast_if($user->isActive(), new UserRegistered($user))->toOthers();
```

<a name="method-broadcast-unless"></a>
#### `broadcast_unless()`

`broadcast_unless` 함수는 지정된 불리언이 거짓일 경우 이벤트를 방송합니다:

```php
broadcast_unless($user->isBanned(), new UserRegistered($user));

broadcast_unless($user->isBanned(), new UserRegistered($user))->toOthers();
```

<a name="method-cache"></a>
#### `cache()`

`cache` 함수는 캐시에서 값을 가져오거나 기본값을 반환합니다:

```php
$value = cache('key');

$value = cache('key', 'default');
```

키/값 쌍을 배열로 전달해 캐시에 값을 저장할 수 있고, 지속 시간을 초 또는 `DateTime` 객체로 지정할 수 있습니다:

```php
cache(['key' => 'value'], 300);

cache(['key' => 'value'], now()->addSeconds(10));
```

<a name="method-class-uses-recursive"></a>
#### `class_uses_recursive()`

`class_uses_recursive` 함수는 클래스 및 모든 부모 클래스에서 사용한 모든 trait를 반환합니다:

```php
$traits = class_uses_recursive(App\Models\User::class);
```

<a name="method-collect"></a>
#### `collect()`

`collect` 함수는 주어진 값으로 [컬렉션](/docs/12.x/collections) 인스턴스를 생성합니다:

```php
$collection = collect(['Taylor', 'Abigail']);
```

<a name="method-config"></a>
#### `config()`

`config` 함수는 [설정값](/docs/12.x/configuration)을 "dot" 표기법으로 가져오거나 기본값을 반환합니다:

```php
$value = config('app.timezone');

$value = config('app.timezone', $default);
```

배열로 전달해 런타임에 설정값을 변경할 수도 있지만, 이는 현재 요청 내에서만 유효합니다:

```php
config(['app.debug' => true]);
```

<a name="method-context"></a>
#### `context()`

`context` 함수는 현재 [컨텍스트](/docs/12.x/context) 값을 가져오거나 기본값을 반환합니다:

```php
$value = context('trace_id');

$value = context('trace_id', $default);
```

배열로 전달해 컨텍스트 값을 설정할 수 있습니다:

```php
use Illuminate\Support\Str;

context(['trace_id' => Str::uuid()->toString()]);
```

<a name="method-cookie"></a>
#### `cookie()`

`cookie` 함수는 새 [쿠키](/docs/12.x/requests#cookies) 인스턴스를 생성합니다:

```php
$cookie = cookie('name', 'value', $minutes);
```

<a name="method-csrf-field"></a>
#### `csrf_field()`

`csrf_field` 함수는 CSRF 토큰 값을 포함하는 HTML `hidden` 입력 필드를 생성합니다. Blade 사용 예:

```blade
{{ csrf_field() }}
```

<a name="method-csrf-token"></a>
#### `csrf_token()`

`csrf_token` 함수는 현재 CSRF 토큰 값을 반환합니다:

```php
$token = csrf_token();
```

<a name="method-decrypt"></a>
#### `decrypt()`

`decrypt` 함수는 암호화된 값을 복호화합니다. `Crypt` 파사드의 대체 함수입니다:

```php
$password = decrypt($value);
```

반대 개념은 [encrypt](#method-encrypt) 함수입니다.

<a name="method-dd"></a>
#### `dd()`

`dd` 함수는 주어진 변수를 출력 한 후 스크립트 실행을 중지합니다:

```php
dd($value);

dd($value1, $value2, $value3, ...);
```

실행 중지를 원치 않으면 [dump](#method-dump) 함수를 사용하세요.

<a name="method-dispatch"></a>
#### `dispatch()`

`dispatch` 함수는 주어진 [잡](/docs/12.x/queues#creating-jobs)을 Laravel [잡 큐](/docs/12.x/queues)에 푸시합니다:

```php
dispatch(new App\Jobs\SendEmails);
```

<a name="method-dispatch-sync"></a>
#### `dispatch_sync()`

`dispatch_sync` 함수는 잡을 즉시 처리하기 위해 동기화 큐에 푸시합니다:

```php
dispatch_sync(new App\Jobs\SendEmails);
```

<a name="method-dump"></a>
#### `dump()`

`dump` 함수는 변수들을 출력합니다:

```php
dump($value);

dump($value1, $value2, $value3, ...);
```

출력 후 스크립트 실행 중지를 원하면 [dd](#method-dd)를 사용하세요.

<a name="method-encrypt"></a>
#### `encrypt()`

`encrypt` 함수는 값을 암호화합니다. `Crypt` 파사드 대체 함수입니다:

```php
$secret = encrypt('my-secret-value');
```

반대 개념은 [decrypt](#method-decrypt) 함수입니다.

<a name="method-env"></a>
#### `env()`

`env` 함수는 [환경 변수](/docs/12.x/configuration#environment-configuration)를 가져오거나 기본값을 반환합니다:

```php
$env = env('APP_ENV');

$env = env('APP_ENV', 'production');
```

> [!WARNING]
> 배포 시 `config:cache` 명령어 실행 시 `.env` 파일이 로드되지 않으므로, `env` 함수는 설정 파일 내에서만 호출해야 합니다. 그 외는 시스템/서버 환경 변수 또는 `null`을 반환할 수 있습니다.

<a name="method-event"></a>
#### `event()`

`event` 함수는 주어진 [이벤트](/docs/12.x/events)를 리스너에게 전달합니다:

```php
event(new UserRegistered($user));
```

<a name="method-fake"></a>
#### `fake()`

`fake` 함수는 Faker 인스턴스를 반환하며 모델 팩토리나 테스트, 시딩 등에서 가짜 데이터를 생성할 때 유용합니다:

```blade
@for ($i = 0; $i < 10; $i++)
    <dl>
        <dt>Name</dt>
        <dd>{{ fake()->name() }}</dd>

        <dt>Email</dt>
        <dd>{{ fake()->unique()->safeEmail() }}</dd>
    </dl>
@endfor
```

기본적으로 `config/app.php`의 `app.faker_locale` 설정을 사용하며, 환경 변수 `APP_FAKER_LOCALE`로 설정 가능합니다. 로케일을 직접 지정할 수도 있습니다:

```php
fake('nl_NL')->name()
```

<a name="method-filled"></a>
#### `filled()`

`filled` 함수는 주어진 값이 "비어있지 않음"인지 판정합니다:

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

반의어는 [blank](#method-blank) 함수입니다.

<a name="method-info"></a>
#### `info()`

`info` 함수는 애플리케이션 로그에 정보를 기록합니다:

```php
info('Some helpful information!');
```

추가 컨텍스트 배열도 전달할 수 있습니다:

```php
info('User login attempt failed.', ['id' => $user->id]);
```

<a name="method-literal"></a>
#### `literal()`

`literal` 함수는 전달된 이름 인수를 프로퍼티로 가지는 새로운 `stdClass` 인스턴스를 생성합니다:

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

`logger` 함수는 `debug` 레벨 메시지를 로그에 기록할 수 있습니다:

```php
logger('Debug message');
```

컨텍스트 배열도 전달할 수 있습니다:

```php
logger('User has logged in.', ['id' => $user->id]);
```

값을 전달하지 않으면 로거 인스턴스를 반환합니다:

```php
logger()->error('You are not allowed here.');
```

<a name="method-method-field"></a>
#### `method_field()`

`method_field` 함수는 폼 HTTP 메서드 스푸핑을 위한 HTML `hidden` 입력 필드를 생성합니다. Blade 사용 예:

```blade
<form method="POST">
    {{ method_field('DELETE') }}
</form>
```

<a name="method-now"></a>
#### `now()`

`now` 함수는 현재 시간의 새 `Illuminate\Support\Carbon` 인스턴스를 생성합니다:

```php
$now = now();
```

<a name="method-old"></a>
#### `old()`

`old` 함수는 세션에 플래시된 이전 입력값을 가져옵니다:

```php
$value = old('value');

$value = old('value', 'default');
```

보통 두 번째 인수는 Eloquent 모델의 속성이므로, 모델 전체를 넘겨도 인식합니다:

```blade
{{ old('name', $user->name) }}

// 다음과 동일

{{ old('name', $user) }}
```

<a name="method-once"></a>
#### `once()`

`once` 함수는 클로저를 실행하고 결과를 현재 요청 동안 메모리에 캐시해 동일 클로저 재호출 시 캐시된 결과를 반환합니다:

```php
function random(): int
{
    return once(function () {
        return random_int(1, 1000);
    });
}

random(); // 123
random(); // 123 (캐시됨)
random(); // 123 (캐시됨)
```

객체 인스턴스 내에서 호출하면 해당 객체에 한정되어 캐시됩니다:

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
$service->all(); // (캐시됨)

$secondService = new NumberService;

$secondService->all();
$secondService->all(); // (캐시됨)
```

<a name="method-optional"></a>
#### `optional()`

`optional` 함수는 임의의 객체를 받아 속성 접근이나 메서드 호출을 지원하며, 대상이 `null`이면 `null`을 반환해 오류를 방지합니다:

```php
return optional($user->address)->street;

{!! old('name', optional($user)->name) !!}
```

두 번째 인수로 클로저를 전달하면 값이 `null`이 아닐 때 실행됩니다:

```php
return optional(User::find($id), function (User $user) {
    return $user->name;
});
```

<a name="method-policy"></a>
#### `policy()`

`policy` 메서드는 주어진 클래스용 [정책](/docs/12.x/authorization#creating-policies) 인스턴스를 반환합니다:

```php
$policy = policy(App\Models\User::class);
```

<a name="method-redirect"></a>
#### `redirect()`

`redirect` 함수는 [리다이렉트 HTTP 응답](/docs/12.x/responses#redirects)을 반환하거나 인수가 없으면 리다이렉터 인스턴스를 반환합니다:

```php
return redirect($to = null, $status = 302, $headers = [], $secure = null);

return redirect('/home');

return redirect()->route('route.name');
```

<a name="method-report"></a>
#### `report()`

`report` 함수는 [예외 핸들러](/docs/12.x/errors#handling-exceptions)를 사용해 예외를 보고합니다:

```php
report($e);
```

문자열을 인수로 주면 메시지로 하는 예외 객체를 생성해 보고합니다:

```php
report('Something went wrong.');
```

<a name="method-report-if"></a>
#### `report_if()`

`report_if` 함수는 특정 불리언이 참일 때 예외를 보고합니다:

```php
report_if($shouldReport, $e);

report_if($shouldReport, 'Something went wrong.');
```

<a name="method-report-unless"></a>
#### `report_unless()`

`report_unless` 함수는 특정 불리언이 거짓일 때 예외를 보고합니다:

```php
report_unless($reportingDisabled, $e);

report_unless($reportingDisabled, 'Something went wrong.');
```

<a name="method-request"></a>
#### `request()`

`request` 함수는 현재 [요청](/docs/12.x/requests) 인스턴스를 반환하거나 현재 요청 입력값을 가져옵니다:

```php
$request = request();

$value = request('key', $default);
```

<a name="method-rescue"></a>
#### `rescue()`

`rescue` 함수는 주어진 클로저를 실행하며 예외를 잡아 예외 핸들러에 보고하지만, 요청 처리는 계속합니다:

```php
return rescue(function () {
    return $this->method();
});
```

두 번째 인수로 예외 발생 시 반환할 기본값이나 클로저를 지정할 수 있습니다:

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

`report` 인수로 예외를 보고할지 여부를 결정할 수 있습니다:

```php
return rescue(function () {
    return $this->method();
}, report: function (Throwable $throwable) {
    return $throwable instanceof InvalidArgumentException;
});
```

<a name="method-resolve"></a>
#### `resolve()`

`resolve` 함수는 [서비스 컨테이너](/docs/12.x/container)를 통해 클래스나 인터페이스를 인스턴스화합니다:

```php
$api = resolve('HelpSpot\API');
```

<a name="method-response"></a>
#### `response()`

`response` 함수는 [응답](/docs/12.x/responses) 인스턴스 생성이나 응답 팩토리 인스턴스를 반환합니다:

```php
return response('Hello World', 200, $headers);

return response()->json(['foo' => 'bar'], 200, $headers);
```

<a name="method-retry"></a>
#### `retry()`

`retry` 함수는 주어진 클로저를 최대 지정 횟수까지 재시도하며, 예외가 발생하지 않을 시 리턴값을 반환합니다. 최대 시도 초과시 예외가 다시 던져집니다:

```php
return retry(5, function () {
    // 최대 5회 시도, 각 시도 후 100밀리초 대기
}, 100);
```

대기시간을 계산하는 클로저도 인수로 전달할 수 있습니다:

```php
use Exception;

return retry(5, function () {
    // ...
}, function (int $attempt, Exception $exception) {
    return $attempt * 100;
});
```

대기시간 배열을 전달해 각 시도마다 다른 시간 대기할 수도 있습니다:

```php
return retry([100, 200], function () {
    // 첫 재시도는 100ms, 두 번째는 200ms 대기
});
```

특정 조건에서만 재시도하도록 네 번째 인수로 클로저를 지정할 수 있습니다:

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

`session` 함수는 [세션](/docs/12.x/session) 값을 가져오거나 설정합니다:

```php
$value = session('key');
```

배열로 여러 값을 설정할 수 있습니다:

```php
session(['chairs' => 7, 'instruments' => 3]);
```

값이 없으면 세션 저장소 인스턴스를 반환합니다:

```php
$value = session()->get('key');

session()->put('key', $value);
```

<a name="method-tap"></a>
#### `tap()`

`tap` 함수는 첫 번째 인수 값을 받아 두 번째 클로저에 전달하고, 클로저 반환값과 상관 없이 첫 번째 인수를 반환합니다:

```php
$user = tap(User::first(), function (User $user) {
    $user->name = 'Taylor';

    $user->save();
});
```

클로저가 없으면 전달 값에 대해 메서드를 호출할 수 있고, 호출 결과와 무관하게 원값을 반환합니다:

```php
$user = tap($user)->update([
    'name' => $name,
    'email' => $email,
]);
```

`Illuminate\Support\Traits\Tappable` 트레이트를 클래스에 추가하면 클래스 내에서 `tap` 메서드를 사용할 수 있습니다:

```php
return $user->tap(function (User $user) {
    // ...
});
```

<a name="method-throw-if"></a>
#### `throw_if()`

`throw_if` 함수는 특정 불리언 표현식이 참이라면 지정한 예외를 던집니다:

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

`throw_unless` 함수는 특정 불리언 표현식이 거짓이라면 예외를 던집니다:

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

`today` 함수는 현재 날짜의 새 `Illuminate\Support\Carbon` 인스턴스를 생성합니다:

```php
$today = today();
```

<a name="method-trait-uses-recursive"></a>
#### `trait_uses_recursive()`

`trait_uses_recursive` 함수는 주어진 trait이 사용하는 모든 trait를 반환합니다:

```php
$traits = trait_uses_recursive(\Illuminate\Notifications\Notifiable::class);
```

<a name="method-transform"></a>
#### `transform()`

`transform` 함수는 주어진 값이 빈 값이 아니면 클로저를 실행해 결과를 반환하고, 빈 값이면 기본값 또는 클로저를 반환합니다:

```php
$callback = function (int $value) {
    return $value * 2;
};

$result = transform(5, $callback);

// 10
```

기본값이나 클로저를 세 번째 인수로 전달할 수 있습니다:

```php
$result = transform(null, $callback, 'The value is blank');

// The value is blank
```

<a name="method-validator"></a>
#### `validator()`

`validator` 함수는 주어진 인수로 새로운 [검증기](/docs/12.x/validation) 인스턴스를 생성합니다. `Validator` 파사드 대용입니다:

```php
$validator = validator($data, $rules, $messages);
```

<a name="method-value"></a>
#### `value()`

`value` 함수는 값을 그대로 반환합니다. 만약 클로저라면 클로저 실행 결과를 반환합니다:

```php
$result = value(true);

// true

$result = value(function () {
    return false;
});

// false
```

추가 인수를 클로저 인자로 전달할 수 있습니다. 클로저가 아닌 경우 추가 인수는 무시됩니다:

```php
$result = value(function (string $name) {
    return $name;
}, 'Taylor');

// 'Taylor'
```

<a name="method-view"></a>
#### `view()`

`view` 함수는 [뷰](/docs/12.x/views) 인스턴스를 반환합니다:

```php
return view('auth.login');
```

<a name="method-with"></a>
#### `with()`

`with` 함수는 주어진 값을 반환합니다. 두 번째 인수로 클로저를 전달하면 실행 결과를 반환합니다:

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

`when` 함수는 조건이 참일 때 값을 반환하고, 그렇지 않으면 `null`을 반환합니다. 두 번째 인수로 클로저가 주어지면 실행 결과를 반환합니다:

```php
$value = when(true, 'Hello World');

$value = when(true, fn () => 'Hello World');
```

주로 HTML 속성을 조건부로 렌더링할 때 사용됩니다:

```blade
<div {!! when($condition, 'wire:poll="calculate"') !!}>
    ...
</div>
```

<a name="other-utilities"></a>
## 기타 유틸리티 (Other Utilities)

<a name="benchmarking"></a>
### 벤치마킹 (Benchmarking)

애플리케이션 특정 부분 성능을 빠르게 측정할 때 `Benchmark` 클래스를 사용할 수 있습니다. 콜백 함수 실행 시간을 밀리초 단위로 측정합니다:

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

기본으로 콜백은 한 번 실행하며, 반복 실행 시 두 번째 인수에 횟수를 지정합니다. 이 경우 평균 밀리초를 반환합니다:

```php
Benchmark::dd(fn () => User::count(), iterations: 10); // 0.5 ms
```

`value` 메서드는 콜백 반환값과 실행 시간을 튜플로 반환합니다:

```php
[$count, $duration] = Benchmark::value(fn () => User::count());
```

<a name="dates"></a>
### 날짜 (Dates)

Laravel은 강력한 날짜/시간 조작 라이브러리 [Carbon](https://carbon.nesbot.com/docs/)을 포함합니다. 새 `Carbon` 인스턴스는 전역 함수 `now` 또는 `Illuminate\Support\Carbon` 클래스로 만들 수 있습니다:

```php
$now = now();
```

또는

```php
use Illuminate\Support\Carbon;

$now = Carbon::now();
```

Carbon 공식 문서를 참고하면 더 많은 기능을 확인할 수 있습니다.

<a name="deferred-functions"></a>
### 지연 실행 함수 (Deferred Functions)

Laravel 큐드 잡과 달리, 간단히 HTTP 응답 후 비동기 작업을 지연 실행할 수 있습니다. `Illuminate\Support\defer` 함수에 클로저를 전달해 사용합니다:

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

기본적으로 HTTP 응답, Artisan 명령, 큐드 잡이 성공해야만 실행됩니다. 항상 실행하려면 `always` 메서드를 체이닝하세요:

```php
defer(fn () => Metrics::reportOrder($order))->always();
```

<a name="cancelling-deferred-functions"></a>
#### 지연 함수 취소

이름을 지정해 지연 함수를 예약하고, `forget` 메서드로 실행 전에 취소할 수 있습니다:

```php
defer(fn () => Metrics::report(), 'reportMetrics');

defer()->forget('reportMetrics');
```

<a name="disabling-deferred-functions-in-tests"></a>
#### 테스트 시 지연 함수 비활성화

테스트 중 지연 실행을 비활성화해 즉시 실행하도록 할 수 있습니다. `withoutDefer` 메서드를 호출합니다:

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

모든 테스트에서 비활성화하려면 `TestCase`의 `setUp` 메서드에 추가하세요:

```php
<?php

namespace Tests;

use Illuminate\Foundation\Testing\TestCase as BaseTestCase;

abstract class TestCase extends BaseTestCase
{
    protected function setUp(): void
    {
        parent::setUp();

        $this->withoutDefer();
    }
}
```

<a name="lottery"></a>
### 복권 (Lottery)

Laravel의 `Lottery` 클래스는 확률 기반으로 콜백 실행 여부를 결정할 때 유용합니다:

```php
use Illuminate\Support\Lottery;

Lottery::odds(1, 20)
    ->winner(fn () => $user->won())
    ->loser(fn () => $user->lost())
    ->choose();
```

Laravel의 다른 기능과 조합해 일부 느린 쿼리를 확률적으로 예외 보고하는 데 활용할 수 있습니다:

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
#### 복권 테스트

`Lottery`와 관련한 테스트 편의를 위해 아래 메서드들을 제공합니다:

```php
// 항상 이기는 복권...
Lottery::alwaysWin();

// 항상 지는 복권...
Lottery::alwaysLose();

// 이기고 지고, 다시 정상 확률로...
Lottery::fix([true, false]);

// 정상 확률로 복권 확률 복원...
Lottery::determineResultsNormally();
```

<a name="pipeline"></a>
### 파이프라인 (Pipeline)

Laravel `Pipeline` 퍼사드를 사용하면 입력을 일련의 호출 가능한 클래스, 클로저를 통해 "파이프로" 연결해 순차적으로 처리할 수 있습니다:

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

각 파이프는 `$next` 클로저를 호출해 다음 파이프를 실행합니다. 마지막 파이프 호출 후 `then` 메서드 콜백이 실행됩니다. 단순히 입력값을 반환하려면 `thenReturn`을 사용하면 편리합니다.

클로저 대신 서비스 컨테이너에서 의존성 주입을 받는 호출 가능한 클래스도 지정할 수 있습니다:

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

Laravel `Sleep` 클래스는 PHP 기본 `sleep` 및 `usleep` 함수를 감싸서 테스트 친화적이며 시간 단위로 API를 제공합니다:

```php
use Illuminate\Support\Sleep;

$waiting = true;

while ($waiting) {
    Sleep::for(1)->second();

    $waiting = /* ... */;
}
```

다양한 단위로 사용할 수 있습니다:

```php
// 값을 반환하며 잠시 대기...
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

// PHP 네이티브 sleep 함수 별칭...
Sleep::sleep(2);

// PHP 네이티브 usleep 함수 별칭...
Sleep::usleep(5000);
```

`and` 메서드로 시간 단위 결합 가능:

```php
Sleep::for(1)->second()->and(10)->milliseconds();
```

<a name="testing-sleep"></a>
#### Sleep 테스트

`Sleep` 클래스 사용 코드는 테스트할 때 실행이 멈춰 느려집니다. `Sleep::fake()`로 페이크하면 테스트가 빨라집니다:

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

`Sleep::fake` 상태에서 실행한 대기 시간에 대해 어설션 가능:

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

다른 어설션 메서드도 있습니다:

```php
use Carbon\CarbonInterval as Duration;
use Illuminate\Support\Sleep;

// 3번 대기했는지 확인...
Sleep::assertSleptTimes(3);

// 대기 시간 기준 어설션...
Sleep::assertSlept(function (Duration $duration): bool {
    return /* ... */;
}, times: 1);

// 대기가 한 번도 없었는지...
Sleep::assertNeverSlept();

// 호출 됐지만 실제 대기는 없었는지...
Sleep::assertInsomniac();
```

페이크된 대기 시 특정 동작을 수행할 콜백 등록도 가능합니다. 예: Carbon 시간 조작과 동기화:

```php
use Carbon\CarbonInterval as Duration;

$this->freezeTime();

Sleep::fake();

Sleep::whenFakingSleep(function (Duration $duration) {
    // 대기 시간만큼 시간 진행...
    $this->travel($duration->totalMilliseconds)->milliseconds();
});
```

동기화를 편하게 하려면 `fake` 메서드 인수로 지정하세요:

```php
Sleep::fake(syncWithCarbon: true);

$start = now();

Sleep::for(1)->second();

$start->diffForHumans(); // 1 second ago
```

Laravel 내부에서 대기 시 `Sleep` 클래스를 사용하므로 [retry](#method-retry) 헬퍼도 테스트 용이성이 높아집니다.

<a name="timebox"></a>
### Timebox

Laravel `Timebox` 클래스는 클로저 실행 시간을 고정된 시간 이상으로 앞당겨 일정 시간 이상 실행된 것처럼 만듭니다. 주로 암호화 및 인증 시 공격자가 시간 변화를 이용해 정보를 추측하는 것을 막는데 유용합니다.

실행 시간이 지정 시간보다 길면 아무 효과 없습니다. 고정 시간은 최악의 경우 시간을 고려해 충분히 길게 설정해야 합니다.

콜(call) 메서드는 클로저와 마이크로초 단위 제한 시간을 받아 실행 후 제한 시간까지 대기합니다:

```php
use Illuminate\Support\Timebox;

(new Timebox)->call(function ($timebox) {
    // ...
}, microseconds: 10000);
```

클로저 내에서 예외가 발생해도 지연 시간 동안 기다린 후 예외가 다시 던져집니다.

<a name="uri"></a>
### URI

Laravel `Uri` 클래스는 URI 생성 및 조작을 편리하고 유창한 인터페이스로 제공합니다. League URI 패키지를 감싸고 Laravel 라우팅과 통합됩니다.

정적 메서드로 쉽게 인스턴스를 생성할 수 있습니다:

```php
use App\Http\Controllers\UserController;
use App\Http\Controllers\InvokableController;
use Illuminate\Support\Uri;

// 문자열에서 URI 인스턴스 생성...
$uri = Uri::of('https://example.com/path');

// 경로나 이름 붙은 라우트, 컨트롤러 액션 경로로부터 URI 생성...
$uri = Uri::to('/dashboard');
$uri = Uri::route('users.show', ['user' => 1]);
$uri = Uri::signedRoute('users.show', ['user' => 1]);
$uri = Uri::temporarySignedRoute('user.index', now()->addMinutes(5));
$uri = Uri::action([UserController::class, 'index']);
$uri = Uri::action(InvokableController::class);

// 현재 요청 URL에서 URI 인스턴스 생성...
$uri = $request->uri();
```

생성 후 메서드 체이닝으로 유연하게 조작할 수 있습니다:

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
#### URI 검사

`Uri` 클래스는 여러 URI 구성 요소도 쉽게 조회할 수 있습니다:

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

`withQuery`는 기존 쿼리 문자열에 추가 파라미터를 머지합니다:

```php
$uri = $uri->withQuery(['sort' => 'name']);
```

`withQueryIfMissing`는 주어진 키가 없을 때만 파라미터를 머지합니다:

```php
$uri = $uri->withQueryIfMissing(['page' => 1]);
```

`replaceQuery`는 기존 쿼리 문자열을 완전히 대체합니다:

```php
$uri = $uri->replaceQuery(['page' => 1]);
```

`pushOntoQuery`는 배열 값 쿼리 파라미터에 값을 추가합니다:

```php
$uri = $uri->pushOntoQuery('filter', ['active', 'pending']);
```

`withoutQuery`는 특정 파라미터를 제거합니다:

```php
$uri = $uri->withoutQuery(['page']);
```

<a name="generating-responses-from-uris"></a>
#### URI로부터 응답 생성

`redirect` 메서드는 지정 URI로 리다이렉트 응답 인스턴스를 생성합니다:

```php
$uri = Uri::of('https://example.com');

return $uri->redirect();
```

라우트나 컨트롤러에서 `Uri` 인스턴스를 반환해도 자동으로 리다이렉트 응답이 생성됩니다:

```php
use Illuminate\Support\Facades\Route;
use Illuminate\Support\Uri;

Route::get('/redirect', function () {
    return Uri::to('/index')
        ->withQuery(['sort' => 'name']);
});
```