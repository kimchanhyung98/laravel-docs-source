# Helpers

- [소개](#introduction)
- [사용 가능한 메서드](#available-methods)
- [기타 유틸리티](#other-utilities)
    - [성능 측정 (Benchmarking)](#benchmarking)
    - [로또 기능 (Lottery)](#lottery)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 다양한 전역 "헬퍼" PHP 함수를 포함하고 있습니다. 이 함수들 중 다수는 프레임워크 자체에서 사용되지만, 필요에 따라 여러분의 애플리케이션에서도 편리하게 사용할 수 있습니다.

<a name="available-methods"></a>
## 사용 가능한 메서드 (Available Methods)



<a name="arrays-and-objects-method-list"></a>
### 배열 및 객체 (Arrays & Objects)

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
[Arr::toCssClasses](#method-array-to-css-classes)  
[Arr::undot](#method-array-undot)  
[Arr::where](#method-array-where)  
[Arr::whereNotNull](#method-array-where-not-null)  
[Arr::wrap](#method-array-wrap)  
[data_fill](#method-data-fill)  
[data_get](#method-data-get)  
[data_set](#method-data-set)  
[head](#method-head)  
[last](#method-last)  
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

<a name="strings-method-list"></a>
### 문자열 (Strings)

<div class="collection-method-list" markdown="1">

[\__](#method-__)  
[class_basename](#method-class-basename)  
[e](#method-e)  
[preg_replace_array](#method-preg-replace-array)  
[Str::after](#method-str-after)  
[Str::afterLast](#method-str-after-last)  
[Str::ascii](#method-str-ascii)  
[Str::before](#method-str-before)  
[Str::beforeLast](#method-str-before-last)  
[Str::between](#method-str-between)  
[Str::betweenFirst](#method-str-between-first)  
[Str::camel](#method-camel-case)  
[Str::contains](#method-str-contains)  
[Str::containsAll](#method-str-contains-all)  
[Str::endsWith](#method-ends-with)  
[Str::excerpt](#method-excerpt)  
[Str::finish](#method-str-finish)  
[Str::headline](#method-str-headline)  
[Str::inlineMarkdown](#method-str-inline-markdown)  
[Str::is](#method-str-is)  
[Str::isAscii](#method-str-is-ascii)  
[Str::isJson](#method-str-is-json)  
[Str::isUlid](#method-str-is-ulid)  
[Str::isUuid](#method-str-is-uuid)  
[Str::kebab](#method-kebab-case)  
[Str::lcfirst](#method-str-lcfirst)  
[Str::length](#method-str-length)  
[Str::limit](#method-str-limit)  
[Str::lower](#method-str-lower)  
[Str::markdown](#method-str-markdown)  
[Str::mask](#method-str-mask)  
[Str::orderedUuid](#method-str-ordered-uuid)  
[Str::padBoth](#method-str-padboth)  
[Str::padLeft](#method-str-padleft)  
[Str::padRight](#method-str-padright)  
[Str::plural](#method-str-plural)  
[Str::pluralStudly](#method-str-plural-studly)  
[Str::random](#method-str-random)  
[Str::remove](#method-str-remove)  
[Str::replace](#method-str-replace)  
[Str::replaceArray](#method-str-replace-array)  
[Str::replaceFirst](#method-str-replace-first)  
[Str::replaceLast](#method-str-replace-last)  
[Str::reverse](#method-str-reverse)  
[Str::singular](#method-str-singular)  
[Str::slug](#method-str-slug)  
[Str::snake](#method-str-snake-case)  
[Str::squish](#method-str-squish)  
[Str::start](#method-str-start)  
[Str::startsWith](#method-starts-with)  
[Str::studly](#method-studly-case)  
[Str::substr](#method-str-substr)  
[Str::substrCount](#method-str-substrcount)  
[Str::substrReplace](#method-str-substrreplace)  
[Str::swap](#method-str-swap)  
[Str::title](#method-title-case)  
[Str::toHtmlString](#method-str-to-html-string)  
[Str::ucfirst](#method-str-ucfirst)  
[Str::ucsplit](#method-str-ucsplit)  
[Str::upper](#method-str-upper)  
[Str::ulid](#method-str-ulid)  
[Str::uuid](#method-str-uuid)  
[Str::wordCount](#method-str-word-count)  
[Str::words](#method-str-words)  
[str](#method-str)  
[trans](#method-trans)  
[trans_choice](#method-trans-choice)  

</div>

<a name="fluent-strings-method-list"></a>
### 플루언트 문자열 (Fluent Strings)

<div class="collection-method-list" markdown="1">

[after](#method-fluent-str-after)  
[afterLast](#method-fluent-str-after-last)  
[append](#method-fluent-str-append)  
[ascii](#method-fluent-str-ascii)  
[basename](#method-fluent-str-basename)  
[before](#method-fluent-str-before)  
[beforeLast](#method-fluent-str-before-last)  
[between](#method-fluent-str-between)  
[betweenFirst](#method-fluent-str-between-first)  
[camel](#method-fluent-str-camel)  
[classBasename](#method-fluent-str-class-basename)  
[contains](#method-fluent-str-contains)  
[containsAll](#method-fluent-str-contains-all)  
[dirname](#method-fluent-str-dirname)  
[endsWith](#method-fluent-str-ends-with)  
[excerpt](#method-fluent-str-excerpt)  
[exactly](#method-fluent-str-exactly)  
[explode](#method-fluent-str-explode)  
[finish](#method-fluent-str-finish)  
[headline](#method-fluent-str-headline)  
[inlineMarkdown](#method-fluent-str-inline-markdown)  
[is](#method-fluent-str-is)  
[isAscii](#method-fluent-str-is-ascii)  
[isEmpty](#method-fluent-str-is-empty)  
[isNotEmpty](#method-fluent-str-is-not-empty)  
[isJson](#method-fluent-str-is-json)  
[isUlid](#method-fluent-str-is-ulid)  
[isUuid](#method-fluent-str-is-uuid)  
[kebab](#method-fluent-str-kebab)  
[lcfirst](#method-fluent-str-lcfirst)  
[length](#method-fluent-str-length)  
[limit](#method-fluent-str-limit)  
[lower](#method-fluent-str-lower)  
[ltrim](#method-fluent-str-ltrim)  
[markdown](#method-fluent-str-markdown)  
[mask](#method-fluent-str-mask)  
[match](#method-fluent-str-match)  
[matchAll](#method-fluent-str-match-all)  
[newLine](#method-fluent-str-new-line)  
[padBoth](#method-fluent-str-padboth)  
[padLeft](#method-fluent-str-padleft)  
[padRight](#method-fluent-str-padright)  
[pipe](#method-fluent-str-pipe)  
[plural](#method-fluent-str-plural)  
[prepend](#method-fluent-str-prepend)  
[remove](#method-fluent-str-remove)  
[replace](#method-fluent-str-replace)  
[replaceArray](#method-fluent-str-replace-array)  
[replaceFirst](#method-fluent-str-replace-first)  
[replaceLast](#method-fluent-str-replace-last)  
[replaceMatches](#method-fluent-str-replace-matches)  
[rtrim](#method-fluent-str-rtrim)  
[scan](#method-fluent-str-scan)  
[singular](#method-fluent-str-singular)  
[slug](#method-fluent-str-slug)  
[snake](#method-fluent-str-snake)  
[split](#method-fluent-str-split)  
[squish](#method-fluent-str-squish)  
[start](#method-fluent-str-start)  
[startsWith](#method-fluent-str-starts-with)  
[studly](#method-fluent-str-studly)  
[substr](#method-fluent-str-substr)  
[substrReplace](#method-fluent-str-substrreplace)  
[swap](#method-fluent-str-swap)  
[tap](#method-fluent-str-tap)  
[test](#method-fluent-str-test)  
[title](#method-fluent-str-title)  
[trim](#method-fluent-str-trim)  
[ucfirst](#method-fluent-str-ucfirst)  
[ucsplit](#method-fluent-str-ucsplit)  
[upper](#method-fluent-str-upper)  
[when](#method-fluent-str-when)  
[whenContains](#method-fluent-str-when-contains)  
[whenContainsAll](#method-fluent-str-when-contains-all)  
[whenEmpty](#method-fluent-str-when-empty)  
[whenNotEmpty](#method-fluent-str-when-not-empty)  
[whenStartsWith](#method-fluent-str-when-starts-with)  
[whenEndsWith](#method-fluent-str-when-ends-with)  
[whenExactly](#method-fluent-str-when-exactly)  
[whenNotExactly](#method-fluent-str-when-not-exactly)  
[whenIs](#method-fluent-str-when-is)  
[whenIsAscii](#method-fluent-str-when-is-ascii)  
[whenIsUlid](#method-fluent-str-when-is-ulid)  
[whenIsUuid](#method-fluent-str-when-is-uuid)  
[whenTest](#method-fluent-str-when-test)  
[wordCount](#method-fluent-str-word-count)  
[words](#method-fluent-str-words)  

</div>

<a name="urls-method-list"></a>
### URL 관련 (URLs)

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

<a name="method-listing"></a>
## 메서드 목록 (Method Listing)



<a name="arrays"></a>
## 배열 및 객체 (Arrays & Objects)

<a name="method-array-accessible"></a>
#### `Arr::accessible()`

`Arr::accessible` 메서드는 주어진 값이 배열 접근이 가능한지 판단합니다:

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

`Arr::add` 메서드는 배열에 주어진 키/값 쌍을 추가합니다. 단, 배열에 해당 키가 존재하지 않거나 값이 `null`일 때만 추가됩니다:

```
use Illuminate\Support\Arr;

$array = Arr::add(['name' => 'Desk'], 'price', 100);

// ['name' => 'Desk', 'price' => 100]

$array = Arr::add(['name' => 'Desk', 'price' => null], 'price', 100);

// ['name' => 'Desk', 'price' => 100]
```


<a name="method-array-collapse"></a>
#### `Arr::collapse()`

`Arr::collapse` 메서드는 배열들의 배열을 단일 배열로 합칩니다:

```
use Illuminate\Support\Arr;

$array = Arr::collapse([[1, 2, 3], [4, 5, 6], [7, 8, 9]]);

// [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

<a name="method-array-crossjoin"></a>
#### `Arr::crossJoin()`

`Arr::crossJoin` 메서드는 주어진 배열들을 카르테시안 곱으로 조합하여 가능한 모든 순열로 된 행렬을 반환합니다:

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

`Arr::divide` 메서드는 주어진 배열의 키와 값으로 두 개의 배열을 반환합니다:

```
use Illuminate\Support\Arr;

[$keys, $values] = Arr::divide(['name' => 'Desk']);

// $keys: ['name']

// $values: ['Desk']
```

<a name="method-array-dot"></a>
#### `Arr::dot()`

`Arr::dot` 메서드는 다차원 배열을 "닷(.)" 표기법을 사용해 단일 차원 배열로 펼칩니다:

```
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

$flattened = Arr::dot($array);

// ['products.desk.price' => 100]
```

<a name="method-array-except"></a>
#### `Arr::except()`

`Arr::except` 메서드는 배열에서 주어진 키/값 쌍들을 제거합니다:

```
use Illuminate\Support\Arr;

$array = ['name' => 'Desk', 'price' => 100];

$filtered = Arr::except($array, ['price']);

// ['name' => 'Desk']
```

<a name="method-array-exists"></a>
#### `Arr::exists()`

`Arr::exists` 메서드는 배열에 해당 키가 존재하는지 확인합니다:

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

`Arr::first` 메서드는 지정된 조건을 만족하는 배열의 첫 번째 요소를 반환합니다:

```
use Illuminate\Support\Arr;

$array = [100, 200, 300];

$first = Arr::first($array, function ($value, $key) {
    return $value >= 150;
});

// 200
```

조건에 맞는 값이 없을 경우 반환할 기본값을 세 번째 인수로도 전달할 수 있습니다:

```
use Illuminate\Support\Arr;

$first = Arr::first($array, $callback, $default);
```

<a name="method-array-flatten"></a>
#### `Arr::flatten()`

`Arr::flatten` 메서드는 다차원 배열을 단일 차원 배열로 평탄화합니다:

```
use Illuminate\Support\Arr;

$array = ['name' => 'Joe', 'languages' => ['PHP', 'Ruby']];

$flattened = Arr::flatten($array);

// ['Joe', 'PHP', 'Ruby']
```

<a name="method-array-forget"></a>
#### `Arr::forget()`

`Arr::forget` 메서드는 "닷" 표기법을 사용해 중첩된 배열에서 특정 키/값 쌍을 제거합니다:

```
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

Arr::forget($array, 'products.desk');

// ['products' => []]
```

<a name="method-array-get"></a>
#### `Arr::get()`

`Arr::get` 메서드는 "닷" 표기법을 사용해 중첩 배열에서 값을 추출합니다:

```
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

$price = Arr::get($array, 'products.desk.price');

// 100
```

키가 존재하지 않을 경우 반환할 기본값도 전달할 수 있습니다:

```
use Illuminate\Support\Arr;

$discount = Arr::get($array, 'products.desk.discount', 0);

// 0
```

<a name="method-array-has"></a>
#### `Arr::has()`

`Arr::has` 메서드는 "닷" 표기법을 사용해 배열에 주어진 항목 또는 항목들이 존재하는지 검사합니다:

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

`Arr::hasAny` 메서드는 "닷" 표기법을 사용해 배열에 주어진 항목들 중 하나라도 존재하는지 검사합니다:

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

`Arr::isAssoc` 메서드는 주어진 배열이 연관 배열인지(`true`) 아닌지(`false`) 판단합니다. 연관 배열은 0부터 시작하는 연속 숫자 키를 갖지 않는 배열을 의미합니다:

```
use Illuminate\Support\Arr;

$isAssoc = Arr::isAssoc(['product' => ['name' => 'Desk', 'price' => 100]]);

// true

$isAssoc = Arr::isAssoc([1, 2, 3]);

// false
```

<a name="method-array-islist"></a>
#### `Arr::isList()`

`Arr::isList` 메서드는 주어진 배열의 키가 0부터 시작하여 연속적인 정수인지 검사합니다:

```
use Illuminate\Support\Arr;

$isList = Arr::isList(['foo', 'bar', 'baz']);

// true

$isList = Arr::isList(['product' => ['name' => 'Desk', 'price' => 100]]);

// false
```

<a name="method-array-join"></a>
#### `Arr::join()`

`Arr::join` 메서드는 배열의 요소들을 문자열로 이어 붙입니다. 두 번째 인수로 최종 요소 사이에 사용할 구분 문자열을 지정할 수 있습니다:

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

`Arr::keyBy` 메서드는 배열 요소들의 특정 키를 기준으로 새로운 배열의 키를 생성합니다. 같은 키가 여러 개 있을 경우 마지막 값으로 덮어씌워집니다:

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

`Arr::last` 메서드는 주어진 조건을 만족하는 배열의 마지막 요소를 반환합니다:

```
use Illuminate\Support\Arr;

$array = [100, 200, 300, 110];

$last = Arr::last($array, function ($value, $key) {
    return $value >= 150;
});

// 300
```

조건에 맞는 값이 없을 경우 반환할 기본값을 세 번째 인수로도 전달할 수 있습니다:

```
use Illuminate\Support\Arr;

$last = Arr::last($array, $callback, $default);
```

<a name="method-array-map"></a>
#### `Arr::map()`

`Arr::map` 메서드는 배열의 각 값과 키를 콜백에 전달하면서 콜백의 반환값으로 값을 변환합니다:

```
use Illuminate\Support\Arr;

$array = ['first' => 'james', 'last' => 'kirk'];

$mapped = Arr::map($array, function ($value, $key) {
    return ucfirst($value);
});

// ['first' => 'James', 'last' => 'Kirk']
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

`Arr::pluck` 메서드는 배열에서 특정 키에 해당하는 모든 값을 추출합니다:

```
use Illuminate\Support\Arr;

$array = [
    ['developer' => ['id' => 1, 'name' => 'Taylor']],
    ['developer' => ['id' => 2, 'name' => 'Abigail']],
];

$names = Arr::pluck($array, 'developer.name');

// ['Taylor', 'Abigail']
```

추출된 리스트의 키를 별도로 지정할 수도 있습니다:

```
use Illuminate\Support\Arr;

$names = Arr::pluck($array, 'developer.name', 'developer.id');

// [1 => 'Taylor', 2 => 'Abigail']
```

<a name="method-array-prepend"></a>
#### `Arr::prepend()`

`Arr::prepend` 메서드는 배열의 맨 앞에 요소를 삽입합니다:

```
use Illuminate\Support\Arr;

$array = ['one', 'two', 'three', 'four'];

$array = Arr::prepend($array, 'zero');

// ['zero', 'one', 'two', 'three', 'four']
```

필요하다면 키도 지정할 수 있습니다:

```
use Illuminate\Support\Arr;

$array = ['price' => 100];

$array = Arr::prepend($array, 'Desk', 'name');

// ['name' => 'Desk', 'price' => 100]
```

<a name="method-array-prependkeyswith"></a>
#### `Arr::prependKeysWith()`

`Arr::prependKeysWith` 메서드는 연관 배열의 모든 키 이름 앞에 주어진 접두사를 추가합니다:

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

`Arr::pull` 메서드는 배열에서 특정 키의 값을 얻어와 반환하며, 해당 키/값 쌍을 배열에서 제거합니다:

```
use Illuminate\Support\Arr;

$array = ['name' => 'Desk', 'price' => 100];

$name = Arr::pull($array, 'name');

// $name: Desk

// $array: ['price' => 100]
```

키가 존재하지 않을 때 반환할 기본값도 세 번째 인수로 전달할 수 있습니다:

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

`Arr::random` 메서드는 배열에서 무작위로 값을 하나 반환합니다:

```
use Illuminate\Support\Arr;

$array = [1, 2, 3, 4, 5];

$random = Arr::random($array);

// 4 - (랜덤 반환)
```

두 번째 인수로 반환할 아이템 수를 지정할 수 있습니다. 이 경우 반환값은 배열입니다:

```
use Illuminate\Support\Arr;

$items = Arr::random($array, 2);

// [2, 5] - (랜덤 반환)
```

<a name="method-array-set"></a>
#### `Arr::set()`

`Arr::set` 메서드는 "닷" 표기법을 이용해 깊게 중첩된 배열에 값을 설정합니다:

```
use Illuminate\Support\Arr;

$array = ['products' => ['desk' => ['price' => 100]]];

Arr::set($array, 'products.desk.price', 200);

// ['products' => ['desk' => ['price' => 200]]]
```

<a name="method-array-shuffle"></a>
#### `Arr::shuffle()`

`Arr::shuffle` 메서드는 배열의 요소들을 무작위로 섞습니다:

```
use Illuminate\Support\Arr;

$array = Arr::shuffle([1, 2, 3, 4, 5]);

// [3, 2, 5, 1, 4] - (랜덤 생성)
```

<a name="method-array-sort"></a>
#### `Arr::sort()`

`Arr::sort` 메서드는 배열을 값 기준 오름차순으로 정렬합니다:

```
use Illuminate\Support\Arr;

$array = ['Desk', 'Table', 'Chair'];

$sorted = Arr::sort($array);

// ['Chair', 'Desk', 'Table']
```

콜백을 사용해 결과값을 기준으로 정렬할 수도 있습니다:

```
use Illuminate\Support\Arr;

$array = [
    ['name' => 'Desk'],
    ['name' => 'Table'],
    ['name' => 'Chair'],
];

$sorted = array_values(Arr::sort($array, function ($value) {
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

`Arr::sortDesc` 메서드는 배열을 값 기준 내림차순으로 정렬합니다:

```
use Illuminate\Support\Arr;

$array = ['Desk', 'Table', 'Chair'];

$sorted = Arr::sortDesc($array);

// ['Table', 'Desk', 'Chair']
```

콜백을 사용해 결과값을 기준으로 정렬할 수도 있습니다:

```
use Illuminate\Support\Arr;

$array = [
    ['name' => 'Desk'],
    ['name' => 'Table'],
    ['name' => 'Chair'],
];

$sorted = array_values(Arr::sortDesc($array, function ($value) {
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

`Arr::sortRecursive` 메서드는 숫자 키 배열은 `sort` 함수로, 연관 배열은 `ksort` 함수로 재귀적으로 정렬합니다:

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

<a name="method-array-to-css-classes"></a>
#### `Arr::toCssClasses()`

`Arr::toCssClasses` 메서드는 조건부로 CSS 클래스를 문자열 형태로 컴파일합니다. 배열의 키는 클래스 이름이며, 값은 해당 클래스를 추가할지 결정하는 불리언 표현식입니다. 키가 숫자일 경우 항상 클래스로 포함됩니다:

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

이 메서드는 Blade 컴포넌트의 속성 가방에서 클래스를 조건부로 병합하거나 Blade의 `@class` 디렉티브 기능에 활용됩니다.

<a name="method-array-undot"></a>
#### `Arr::undot()`

`Arr::undot` 메서드는 "닷" 표기법을 사용한 단일 차원 배열을 다차원 배열로 확장합니다:

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

`Arr::where` 메서드는 주어진 클로저를 사용해 배열에서 조건에 맞는 요소만 필터링합니다:

```
use Illuminate\Support\Arr;

$array = [100, '200', 300, '400', 500];

$filtered = Arr::where($array, function ($value, $key) {
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

`Arr::wrap` 메서드는 주어진 값을 배열로 감쌉니다. 이미 배열이라면 변경 없이 반환되고, `null`이면 빈 배열을 반환합니다:

```
use Illuminate\Support\Arr;

$string = 'Laravel';

$array = Arr::wrap($string);

// ['Laravel']
```

```
use Illuminate\Support\Arr;

$array = Arr::wrap(null);

// []
```

<a name="method-data-fill"></a>
#### `data_fill()`

`data_fill` 함수는 중첩된 배열이나 객체에서 값이 비어있는 경우에만 "닷" 표기법을 써서 값을 채웁니다:

```
$data = ['products' => ['desk' => ['price' => 100]]];

data_fill($data, 'products.desk.price', 200);

// ['products' => ['desk' => ['price' => 100]]]

data_fill($data, 'products.desk.discount', 10);

// ['products' => ['desk' => ['price' => 100, 'discount' => 10]]]
```

와일드카드(`*`)도 사용할 수 있어 대상에 맞게 일괄 적용합니다:

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

`data_get` 함수는 중첩된 배열이나 객체에서 "닷" 표기법을 통해 값을 가져옵니다:

```
$data = ['products' => ['desk' => ['price' => 100]]];

$price = data_get($data, 'products.desk.price');

// 100
```

키가 없다면 기본값을 반환합니다:

```
$discount = data_get($data, 'products.desk.discount', 0);

// 0
```

와일드카드(`*`)로 배열이나 객체의 모든 키를 타겟팅할 수도 있습니다:

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

`data_set` 함수는 중첩 배열이나 객체에 "닷" 표기법으로 값을 설정합니다:

```
$data = ['products' => ['desk' => ['price' => 100]]];

data_set($data, 'products.desk.price', 200);

// ['products' => ['desk' => ['price' => 200]]]
```

와일드카드(`*`)도 지원하며 대상에 맞게 동시에 값들을 설정합니다:

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

기본적으로 기존 값들은 덮어쓰기가 됩니다. 만약 값이 존재하지 않을 때만 설정하려면 네 번째 인수를 `false`로 줍니다:

```
$data = ['products' => ['desk' => ['price' => 100]]];

data_set($data, 'products.desk.price', 200, overwrite: false);

// ['products' => ['desk' => ['price' => 100]]]
```

<a name="method-head"></a>
#### `head()`

`head` 함수는 배열의 첫 번째 요소를 반환합니다:

```
$array = [100, 200, 300];

$first = head($array);

// 100
```

<a name="method-last"></a>
#### `last()`

`last` 함수는 배열의 마지막 요소를 반환합니다:

```
$array = [100, 200, 300];

$last = last($array);

// 300
```

<a name="paths"></a>
## 경로 (Paths)

<a name="method-app-path"></a>
#### `app_path()`

`app_path` 함수는 애플리케이션의 `app` 디렉토리 전체 경로를 반환합니다. 인자로 상대경로를 전달해 내부 파일 경로를 얻을 수도 있습니다:

```
$path = app_path();

$path = app_path('Http/Controllers/Controller.php');
```

<a name="method-base-path"></a>
#### `base_path()`

`base_path` 함수는 애플리케이션 루트 디렉토리 전체 경로를 반환합니다. 인자를 파일 경로로 전달할 수도 있습니다:

```
$path = base_path();

$path = base_path('vendor/bin');
```

<a name="method-config-path"></a>
#### `config_path()`

`config_path` 함수는 애플리케이션의 `config` 디렉토리 전체 경로를 반환합니다. 인자 전달 시 해당 설정 파일 경로를 생성할 수도 있습니다:

```
$path = config_path();

$path = config_path('app.php');
```

<a name="method-database-path"></a>
#### `database_path()`

`database_path` 함수는 애플리케이션의 `database` 디렉토리 전체 경로를 반환합니다. 인자를 전달해 데이터베이스 관련 파일 경로도 생성 가능합니다:

```
$path = database_path();

$path = database_path('factories/UserFactory.php');
```

<a name="method-lang-path"></a>
#### `lang_path()`

`lang_path` 함수는 애플리케이션의 `lang` 디렉토리 전체 경로를 반환합니다. 인자를 전달해 내부 파일 경로를 생성할 수 있습니다:

```
$path = lang_path();

$path = lang_path('en/messages.php');
```

<a name="method-mix"></a>
#### `mix()`

`mix` 함수는 [버전 관리된 Mix 파일] 경로를 반환합니다:

```
$path = mix('css/app.css');
```

<a name="method-public-path"></a>
#### `public_path()`

`public_path` 함수는 애플리케이션의 `public` 디렉토리 전체 경로를 반환합니다. 인자를 전달해 파일 경로도 생성할 수 있습니다:

```
$path = public_path();

$path = public_path('css/app.css');
```

<a name="method-resource-path"></a>
#### `resource_path()`

`resource_path` 함수는 애플리케이션의 `resources` 디렉토리 전체 경로를 반환합니다. 인자를 전달해 내부 파일 경로를 생성할 수 있습니다:

```
$path = resource_path();

$path = resource_path('sass/app.scss');
```

<a name="method-storage-path"></a>
#### `storage_path()`

`storage_path` 함수는 애플리케이션의 `storage` 디렉토리 전체 경로를 반환합니다. 인자를 전달해 내부 파일 경로를 생성할 수 있습니다:

```
$path = storage_path();

$path = storage_path('app/file.txt');
```

<a name="strings"></a>
## 문자열 (Strings)

<a name="method-__"></a>
#### `__()`

`__` 함수는 [로컬라이제이션 파일]을 사용해 지정된 문자열이나 키를 번역합니다:

```
echo __('Welcome to our application');

echo __('messages.welcome');
```

만약 지정된 번역 문자열이나 키가 없으면 입력한 값 그대로 반환합니다. 예를 들어 `messages.welcome` 키가 없으면 그대로 `messages.welcome`이 반환됩니다.

<a name="method-class-basename"></a>
#### `class_basename()`

`class_basename` 함수는 주어진 클래스 이름에서 네임스페이스를 제외한 클래스명만 반환합니다:

```
$class = class_basename('Foo\Bar\Baz');

// Baz
```

<a name="method-e"></a>
#### `e()`

`e` 함수는 PHP의 `htmlspecialchars` 함수를 기본적으로 `double_encode` 옵션을 켜둔 채 실행합니다:

```
echo e('<html>foo</html>');

// &lt;html&gt;foo&lt;/html&gt;
```

<a name="method-preg-replace-array"></a>
#### `preg_replace_array()`

`preg_replace_array` 함수는 문자열 내 특정 패턴들을 순서대로 배열 값으로 치환합니다:

```
$string = 'The event will take place between :start and :end';

$replaced = preg_replace_array('/:[a-z_]+/', ['8:30', '9:00'], $string);

// The event will take place between 8:30 and 9:00
```

<a name="method-str-after"></a>
#### `Str::after()`

`Str::after` 메서드는 문자열 내 특정 값 뒤에 나오는 모든 내용을 반환합니다. 값이 없으면 전체 문자열을 반환합니다:

```
use Illuminate\Support\Str;

$slice = Str::after('This is my name', 'This is');

// ' my name'
```

<a name="method-str-after-last"></a>
#### `Str::afterLast()`

`Str::afterLast` 메서드는 문자열 내 특정 값의 마지막 출현 위치 이후 모든 내용을 반환합니다. 값이 없으면 전체 문자열을 반환합니다:

```
use Illuminate\Support\Str;

$slice = Str::afterLast('App\Http\Controllers\Controller', '\\');

// 'Controller'
```

<a name="method-str-ascii"></a>
#### `Str::ascii()`

`Str::ascii` 메서드는 문자열을 ASCII 값으로 변환(음역)합니다:

```
use Illuminate\Support\Str;

$slice = Str::ascii('û');

// 'u'
```

<a name="method-str-before"></a>
#### `Str::before()`

`Str::before` 메서드는 문자열 내 특정 값 이전 모든 내용을 반환합니다:

```
use Illuminate\Support\Str;

$slice = Str::before('This is my name', 'my name');

// 'This is '
```

<a name="method-str-before-last"></a>
#### `Str::beforeLast()`

`Str::beforeLast` 메서드는 문자열 내 특정 값 마지막 출현 이전 모든 내용을 반환합니다:

```
use Illuminate\Support\Str;

$slice = Str::beforeLast('This is my name', 'is');

// 'This '
```

<a name="method-str-between"></a>
#### `Str::between()`

`Str::between` 메서드는 두 값 사이에 있는 문자열의 일부를 반환합니다:

```
use Illuminate\Support\Str;

$slice = Str::between('This is my name', 'This', 'name');

// ' is my '
```

<a name="method-str-between-first"></a>
#### `Str::betweenFirst()`

`Str::betweenFirst` 메서드는 두 값 사이에서 가능한 가장 작은 범위의 문자열 일부를 반환합니다:

```
use Illuminate\Support\Str;

$slice = Str::betweenFirst('[a] bc [d]', '[', ']');

// 'a'
```

<a name="method-camel-case"></a>
#### `Str::camel()`

`Str::camel` 메서드는 주어진 문자열을 `camelCase` 형식으로 변환합니다:

```
use Illuminate\Support\Str;

$converted = Str::camel('foo_bar');

// fooBar
```

<a name="method-str-contains"></a>
#### `Str::contains()`

`Str::contains` 메서드는 문자열에 특정 값이 포함되어 있는지 확인합니다. 대소문자를 구분합니다:

```
use Illuminate\Support\Str;

$contains = Str::contains('This is my name', 'my');

// true
```

배열을 전달하면 값 중 하나라도 포함되어 있는지 검사할 수 있습니다:

```
use Illuminate\Support\Str;

$contains = Str::contains('This is my name', ['my', 'foo']);

// true
```

<a name="method-str-contains-all"></a>
#### `Str::containsAll()`

`Str::containsAll` 메서드는 문자열이 배열의 모든 값을 포함하는지 확인합니다:

```
use Illuminate\Support\Str;

$containsAll = Str::containsAll('This is my name', ['my', 'name']);

// true
```

<a name="method-ends-with"></a>
#### `Str::endsWith()`

`Str::endsWith` 메서드는 문자열이 특정 값으로 끝나는지 확인합니다:

```
use Illuminate\Support\Str;

$result = Str::endsWith('This is my name', 'name');

// true
```

배열을 전달하면 값들 중 하나라도 끝나는지 검사할 수 있습니다:

```
use Illuminate\Support\Str;

$result = Str::endsWith('This is my name', ['name', 'foo']);

// true

$result = Str::endsWith('This is my name', ['this', 'foo']);

// false
```

<a name="method-excerpt"></a>
#### `Str::excerpt()`

`Str::excerpt` 메서드는 문자열에서 특정 구절이 처음 등장하는 부분을 중심으로 발췌합니다:

```
use Illuminate\Support\Str;

$excerpt = Str::excerpt('This is my name', 'my', [
    'radius' => 3
]);

// '...is my na...'
```

`radius` 옵션은 기본 100자로, 발췌할 문자열 좌우에 표시할 문자 수를 정합니다.

또한 `omission` 옵션으로 발췌 양쪽에 붙일 문자열을 지정할 수 있습니다:

```
use Illuminate\Support\Str;

$excerpt = Str::excerpt('This is my name', 'name', [
    'radius' => 3,
    'omission' => '(...) '
]);

// '(...) my name'
```

<a name="method-str-finish"></a>
#### `Str::finish()`

`Str::finish` 메서드는 문자열이 특정 값으로 끝나지 않으면, 그 값을 한 번만 추가합니다:

```
use Illuminate\Support\Str;

$adjusted = Str::finish('this/string', '/');

// this/string/

$adjusted = Str::finish('this/string/', '/');

// this/string/
```

<a name="method-str-headline"></a>
#### `Str::headline()`

`Str::headline` 메서드는 케이스, 하이픈, 언더스코어로 구분된 문자열을 각 단어 첫 글자가 대문자인 공백 구분 문자열로 변환합니다:

```
use Illuminate\Support\Str;

$headline = Str::headline('steve_jobs');

// Steve Jobs

$headline = Str::headline('EmailNotificationSent');

// Email Notification Sent
```

<a name="method-str-inline-markdown"></a>
#### `Str::inlineMarkdown()`

`Str::inlineMarkdown` 메서드는 GitHub 스타일 Markdown을 [CommonMark](https://commonmark.thephpleague.com/) 사용해 인라인 HTML로 변환합니다. `markdown`과 달리 블록 레벨 태그로 감싸지 않습니다:

```
use Illuminate\Support\Str;

$html = Str::inlineMarkdown('**Laravel**');

// <strong>Laravel</strong>
```

<a name="method-str-is"></a>
#### `Str::is()`

`Str::is` 메서드는 와일드카드(*)를 사용하여 문자열이 패턴과 일치하는지 검사합니다:

```
use Illuminate\Support\Str;

$matches = Str::is('foo*', 'foobar');

// true

$matches = Str::is('baz*', 'foobar');

// false
```

<a name="method-str-is-ascii"></a>
#### `Str::isAscii()`

`Str::isAscii` 메서드는 문자열이 7비트 ASCII인지 검사합니다:

```
use Illuminate\Support\Str;

$isAscii = Str::isAscii('Taylor');

// true

$isAscii = Str::isAscii('ü');

// false
```

<a name="method-str-is-json"></a>
#### `Str::isJson()`

`Str::isJson` 메서드는 문자열이 유효 JSON인지 검사합니다:

```
use Illuminate\Support\Str;

$result = Str::isJson('[1,2,3]');

// true

$result = Str::isJson('{"first": "John", "last": "Doe"}');

// true

$result = Str::isJson('{first: "John", last: "Doe"}');

// false
```

<a name="method-str-is-ulid"></a>
#### `Str::isUlid()`

`Str::isUlid` 메서드는 문자열이 유효한 ULID인지 검사합니다:

```
use Illuminate\Support\Str;

$isUlid = Str::isUlid('01gd6r360bp37zj17nxb55yv40');

// true

$isUlid = Str::isUlid('laravel');

// false
```

<a name="method-str-is-uuid"></a>
#### `Str::isUuid()`

`Str::isUuid` 메서드는 문자열이 유효한 UUID인지 검사합니다:

```
use Illuminate\Support\Str;

$isUuid = Str::isUuid('a0a2a2d2-0b87-4a18-83f2-2529882be2de');

// true

$isUuid = Str::isUuid('laravel');

// false
```

<a name="method-kebab-case"></a>
#### `Str::kebab()`

`Str::kebab` 메서드는 문자열을 `kebab-case` 형식으로 변환합니다:

```
use Illuminate\Support\Str;

$converted = Str::kebab('fooBar');

// foo-bar
```

<a name="method-str-lcfirst"></a>
#### `Str::lcfirst()`

`Str::lcfirst` 메서드는 문자열의 첫 글자를 소문자로 변경합니다:

```
use Illuminate\Support\Str;

$string = Str::lcfirst('Foo Bar');

// foo Bar
```

<a name="method-str-length"></a>
#### `Str::length()`

`Str::length` 메서드는 문자열 길이를 반환합니다:

```
use Illuminate\Support\Str;

$length = Str::length('Laravel');

// 7
```

<a name="method-str-limit"></a>
#### `Str::limit()`

`Str::limit` 메서드는 지정한 길이로 문자열을 잘라냅니다:

```
use Illuminate\Support\Str;

$truncated = Str::limit('The quick brown fox jumps over the lazy dog', 20);

// The quick brown fox...
```

잘린 부분 뒤에 붙일 문자열도 세 번째 인수로 지정 가능합니다:

```
use Illuminate\Support\Str;

$truncated = Str::limit('The quick brown fox jumps over the lazy dog', 20, ' (...)');

// The quick brown fox (...)
```

<a name="method-str-lower"></a>
#### `Str::lower()`

`Str::lower` 메서드는 문자열을 소문자로 변환합니다:

```
use Illuminate\Support\Str;

$converted = Str::lower('LARAVEL');

// laravel
```

<a name="method-str-markdown"></a>
#### `Str::markdown()`

`Str::markdown` 메서드는 GitHub 스타일 Markdown을 [CommonMark](https://commonmark.thephpleague.com/)로 HTML로 변환합니다:

```
use Illuminate\Support\Str;

$html = Str::markdown('# Laravel');

// <h1>Laravel</h1>

$html = Str::markdown('# Taylor <b>Otwell</b>', [
    'html_input' => 'strip',
]);

// <h1>Taylor Otwell</h1>
```

<a name="method-str-mask"></a>
#### `Str::mask()`

`Str::mask` 메서드는 문자열 일부를 반복 문자로 가려 이메일, 전화번호 등 일부를 숨길 때 사용합니다:

```
use Illuminate\Support\Str;

$string = Str::mask('taylor@example.com', '*', 3);

// tay***************
```

음수 인자를 주면 문자열 끝을 기준으로 가리기 시작합니다:

```
$string = Str::mask('taylor@example.com', '*', -15, 3);

// tay***@example.com
```

<a name="method-str-ordered-uuid"></a>
#### `Str::orderedUuid()`

`Str::orderedUuid` 메서드는 "타임스탬프 우선" UUID를 생성하며, 인덱스된 DB 컬럼에 효율적으로 저장 가능합니다. 생성된 UUID는 이전 것 이후로 정렬됩니다:

```
use Illuminate\Support\Str;

return (string) Str::orderedUuid();
```

<a name="method-str-padboth"></a>
#### `Str::padBoth()`

`Str::padBoth` 메서드는 PHP `str_pad` 함수를 감싸 양쪽에 문자열을 채워 지정 길이까지 패딩합니다:

```
use Illuminate\Support\Str;

$padded = Str::padBoth('James', 10, '_');

// '__James___'

$padded = Str::padBoth('James', 10);

// '  James   '
```

<a name="method-str-padleft"></a>
#### `Str::padLeft()`

`Str::padLeft` 메서드는 문자열 왼쪽에 패딩을 추가합니다:

```
use Illuminate\Support\Str;

$padded = Str::padLeft('James', 10, '-=');

// '-=-=-James'

$padded = Str::padLeft('James', 10);

// '     James'
```

<a name="method-str-padright"></a>
#### `Str::padRight()`

`Str::padRight` 메서드는 문자열 오른쪽에 패딩을 추가합니다:

```
use Illuminate\Support\Str;

$padded = Str::padRight('James', 10, '-');

// 'James-----'

$padded = Str::padRight('James', 10);

// 'James     '
```

<a name="method-str-plural"></a>
#### `Str::plural()`

`Str::plural` 메서드는 단수형 문자열을 복수형으로 변환합니다. Laravel 복수화 지원 언어를 모두 지원합니다:

```
use Illuminate\Support\Str;

$plural = Str::plural('car');

// cars

$plural = Str::plural('child');

// children
```

두 번째 인수에 숫자를 주어 단수/복수 결정도 가능합니다:

```
use Illuminate\Support\Str;

$plural = Str::plural('child', 2);

// children

$singular = Str::plural('child', 1);

// child
```

<a name="method-str-plural-studly"></a>
#### `Str::pluralStudly()`

`Str::pluralStudly` 메서드는 StudlyCase 단수형 문자열을 복수형으로 변환합니다. Laravel 복수화 지원 언어를 모두 지원합니다:

```
use Illuminate\Support\Str;

$plural = Str::pluralStudly('VerifiedHuman');

// VerifiedHumans

$plural = Str::pluralStudly('UserFeedback');

// UserFeedback
```

두 번째 인수에 숫자를 주어 단수/복수 결정도 가능합니다:

```
use Illuminate\Support\Str;

$plural = Str::pluralStudly('VerifiedHuman', 2);

// VerifiedHumans

$singular = Str::pluralStudly('VerifiedHuman', 1);

// VerifiedHuman
```

<a name="method-str-random"></a>
#### `Str::random()`

`Str::random` 메서드는 지정한 길이만큼 임의 문자열을 생성합니다. PHP의 `random_bytes` 함수 기반입니다:

```
use Illuminate\Support\Str;

$random = Str::random(40);
```

<a name="method-str-remove"></a>
#### `Str::remove()`

`Str::remove` 메서드는 문자열에서 지정 값 또는 배열 값을 제거합니다:

```
use Illuminate\Support\Str;

$string = 'Peter Piper picked a peck of pickled peppers.';

$removed = Str::remove('e', $string);

// Ptr Pipr pickd a pck of pickld ppprs.
```

세 번째 인수에 `false`를 주면 대소문자 구분 없이 제거합니다.

<a name="method-str-replace"></a>
#### `Str::replace()`

`Str::replace` 메서드는 문자열 내에서 특정 문자열을 치환합니다:

```
use Illuminate\Support\Str;

$string = 'Laravel 8.x';

$replaced = Str::replace('8.x', '9.x', $string);

// Laravel 9.x
```

<a name="method-str-replace-array"></a>
#### `Str::replaceArray()`

`Str::replaceArray` 메서드는 문자열 내 특정 값을 배열에 순서대로 치환합니다:

```
use Illuminate\Support\Str;

$string = 'The event will take place between ? and ?';

$replaced = Str::replaceArray('?', ['8:30', '9:00'], $string);

// The event will take place between 8:30 and 9:00
```

<a name="method-str-replace-first"></a>
#### `Str::replaceFirst()`

`Str::replaceFirst` 메서드는 문자열 내 첫 번째로 나타나는 특정 값을 치환합니다:

```
use Illuminate\Support\Str;

$replaced = Str::replaceFirst('the', 'a', 'the quick brown fox jumps over the lazy dog');

// a quick brown fox jumps over the lazy dog
```

<a name="method-str-replace-last"></a>
#### `Str::replaceLast()`

`Str::replaceLast` 메서드는 문자열 내 마지막으로 나타나는 특정 값을 치환합니다:

```
use Illuminate\Support\Str;

$replaced = Str::replaceLast('the', 'a', 'the quick brown fox jumps over the lazy dog');

// the quick brown fox jumps over a lazy dog
```


<a name="method-str-reverse"></a>
#### `Str::reverse()`

`Str::reverse` 메서드는 문자열을 뒤집습니다:

```
use Illuminate\Support\Str;

$reversed = Str::reverse('Hello World');

// dlroW olleH
```

<a name="method-str-singular"></a>
#### `Str::singular()`

`Str::singular` 메서드는 문자열을 단수형으로 변환합니다. Laravel 복수화 지원 언어 모두를 지원합니다:

```
use Illuminate\Support\Str;

$singular = Str::singular('cars');

// car

$singular = Str::singular('children');

// child
```

<a name="method-str-slug"></a>
#### `Str::slug()`

`Str::slug` 메서드는 URL 친화적인 "슬러그" 문자열을 생성합니다:

```
use Illuminate\Support\Str;

$slug = Str::slug('Laravel 5 Framework', '-');

// laravel-5-framework
```

<a name="method-snake-case"></a>
#### `Str::snake()`

`Str::snake` 메서드는 문자열을 `snake_case` 형식으로 변환합니다:

```
use Illuminate\Support\Str;

$converted = Str::snake('fooBar');

// foo_bar

$converted = Str::snake('fooBar', '-');

// foo-bar
```

<a name="method-str-squish"></a>
#### `Str::squish()`

`Str::squish` 메서드는 문자열 좌우 및 단어 사이 불필요한 공백을 모두 제거합니다:

```
use Illuminate\Support\Str;

$string = Str::squish('    laravel    framework    ');

// laravel framework
```

<a name="method-str-start"></a>
#### `Str::start()`

`Str::start` 메서드는 문자열이 특정 값으로 시작하지 않으면, 그 값을 한 번만 추가합니다:

```
use Illuminate\Support\Str;

$adjusted = Str::start('this/string', '/');

// /this/string

$adjusted = Str::start('/this/string', '/');

// /this/string
```

<a name="method-starts-with"></a>
#### `Str::startsWith()`

`Str::startsWith` 메서드는 문자열이 특정 값으로 시작하는지 검사합니다:

```
use Illuminate\Support\Str;

$result = Str::startsWith('This is my name', 'This');

// true
```

배열을 전달하면, 값들 중 하나라도 시작 하면 `true`를 반환합니다:

```
$result = Str::startsWith('This is my name', ['This', 'That', 'There']);

// true
```

<a name="method-studly-case"></a>
#### `Str::studly()`

`Str::studly` 메서드는 문자열을 `StudlyCase` 형식으로 변환합니다:

```
use Illuminate\Support\Str;

$converted = Str::studly('foo_bar');

// FooBar
```

<a name="method-str-substr"></a>
#### `Str::substr()`

`Str::substr` 메서드는 지정한 시작 위치와 길이만큼 문자열 일부를 반환합니다:

```
use Illuminate\Support\Str;

$converted = Str::substr('The Laravel Framework', 4, 7);

// Laravel
```

<a name="method-str-substrcount"></a>
#### `Str::substrCount()`

`Str::substrCount` 메서드는 문자열 내 특정 값의 출현 횟수를 반환합니다:

```
use Illuminate\Support\Str;

$count = Str::substrCount('If you like ice cream, you will like snow cones.', 'like');

// 2
```

<a name="method-str-substrreplace"></a>
#### `Str::substrReplace()`

`Str::substrReplace` 메서드는 문자열 내 특정 위치부터 지정한 길이만큼 문자를 다른 문자열로 대체합니다. 네 번째 인수에 `0`을 전달하면 삽입만 하고 기존 문자는 덮어쓰지 않습니다:

```
use Illuminate\Support\Str;

$result = Str::substrReplace('1300', ':', 2);
// 13:

$result = Str::substrReplace('1300', ':', 2, 0);
// 13:00
```

<a name="method-str-swap"></a>
#### `Str::swap()`

`Str::swap` 메서드는 PHP `strtr` 함수를 이용해 다중 문자열 대체를 실행합니다:

```
use Illuminate\Support\Str;

$string = Str::swap([
    'Tacos' => 'Burritos',
    'great' => 'fantastic',
], 'Tacos are great!');

// Burritos are fantastic!
```

<a name="method-title-case"></a>
#### `Str::title()`

`Str::title` 메서드는 문자열을 각 단어 첫 글자 대문자인 `Title Case`로 변환합니다:

```
use Illuminate\Support\Str;

$converted = Str::title('a nice title uses the correct case');

// A Nice Title Uses The Correct Case
```

<a name="method-str-to-html-string"></a>
#### `Str::toHtmlString()`

`Str::toHtmlString` 메서드는 문자열 인스턴스를 Blade 템플릿에서 출력 가능한 `Illuminate\Support\HtmlString` 인스턴스로 변환합니다:

```
use Illuminate\Support\Str;

$htmlString = Str::of('Nuno Maduro')->toHtmlString();
```

<a name="method-str-ucfirst"></a>
#### `Str::ucfirst()`

`Str::ucfirst` 메서드는 문자열 첫 글자를 대문자로 변경합니다:

```
use Illuminate\Support\Str;

$string = Str::ucfirst('foo bar');

// Foo bar
```

<a name="method-str-ucsplit"></a>
#### `Str::ucsplit()`

`Str::ucsplit` 메서드는 대문자 기준으로 문자열을 배열로 분리합니다:

```
use Illuminate\Support\Str;

$segments = Str::ucsplit('FooBar');

// [0 => 'Foo', 1 => 'Bar']
```

<a name="method-str-upper"></a>
#### `Str::upper()`

`Str::upper` 메서드는 문자열을 모두 대문자로 변환합니다:

```
use Illuminate\Support\Str;

$string = Str::upper('laravel');

// LARAVEL
```

<a name="method-str-ulid"></a>
#### `Str::ulid()`

`Str::ulid` 메서드는 ULID를 생성합니다:

```
use Illuminate\Support\Str;

return (string) Str::ulid();

// 01gd6r360bp37zj17nxb55yv40
```

<a name="method-str-uuid"></a>
#### `Str::uuid()`

`Str::uuid` 메서드는 UUID(version 4)를 생성합니다:

```
use Illuminate\Support\Str;

return (string) Str::uuid();
```

<a name="method-str-word-count"></a>
#### `Str::wordCount()`

`Str::wordCount` 메서드는 문자열의 단어 개수를 반환합니다:

```php
use Illuminate\Support\Str;

Str::wordCount('Hello, world!'); // 2
```

<a name="method-str-words"></a>
#### `Str::words()`

`Str::words` 메서드는 문자열을 지정한 단어 수만큼 제한합니다. 잘림 표시 문자열도 세 번째 인수로 지정 가능합니다:

```
use Illuminate\Support\Str;

return Str::words('Perfectly balanced, as all things should be.', 3, ' >>>');

// Perfectly balanced, as >>>
```

<a name="method-str"></a>
#### `str()`

`str` 함수는 주어진 문자열을 `Illuminate\Support\Stringable` 인스턴스로 반환합니다. `Str::of` 메서드와 같습니다:

```
$string = str('Taylor')->append(' Otwell');

// 'Taylor Otwell'
```

인수가 없으면 `Illuminate\Support\Str` 인스턴스를 반환합니다:

```
$snake = str()->snake('FooBar');

// 'foo_bar'
```

<a name="method-trans"></a>
#### `trans()`

`trans` 함수는 [로컬라이제이션 파일]을 이용해 지정된 번역 키를 변환합니다:

```
echo trans('messages.welcome');
```

키가 없으면 입력한 키를 반환합니다.

<a name="method-trans-choice"></a>
#### `trans_choice()`

`trans_choice` 함수는 번역 키를 기반으로 수량에 따른 복수형 변환 등을 처리합니다:

```
echo trans_choice('messages.notifications', $unreadCount);
```

키가 없으면 입력한 키를 반환합니다.

<a name="fluent-strings"></a>
## 플루언트 문자열 (Fluent Strings)

플루언트 문자열은 문자열 조작을 객체지향적으로 직관적 구문으로 연결(chain)할 수 있게 해줍니다. 기존 문자열함수보다 가독성이 높고 편리합니다.

<a name="method-fluent-str-after"></a>
#### `after`

문자열 내 지정된 값 다음의 모든 내용을 반환합니다. 값이 없으면 문자열 전체를 반환합니다:

```
use Illuminate\Support\Str;

$slice = Str::of('This is my name')->after('This is');

// ' my name'
```

<a name="method-fluent-str-after-last"></a>
#### `afterLast`

마지막 출현하는 지정 값 다음 모든 내용을 반환합니다. 없으면 전체 반환:

```
use Illuminate\Support\Str;

$slice = Str::of('App\Http\Controllers\Controller')->afterLast('\\');

// 'Controller'
```

<a name="method-fluent-str-append"></a>
#### `append`

주어진 값을 문자열 뒤에 덧붙입니다:

```
use Illuminate\Support\Str;

$string = Str::of('Taylor')->append(' Otwell');

// 'Taylor Otwell'
```

<a name="method-fluent-str-ascii"></a>
#### `ascii`

문자열을 ASCII 값으로 치환 시도합니다:

```
use Illuminate\Support\Str;

$string = Str::of('ü')->ascii();

// 'u'
```

<a name="method-fluent-str-basename"></a>
#### `basename`

문자열의 마지막 경로 요소를 반환합니다:

```
use Illuminate\Support\Str;

$string = Str::of('/foo/bar/baz')->basename();

// 'baz'
```

필요하다면 제거할 확장자도 지정 가능:

```
use Illuminate\Support\Str;

$string = Str::of('/foo/bar/baz.jpg')->basename('.jpg');

// 'baz'
```

<a name="method-fluent-str-before"></a>
#### `before`

주어진 값 이전 문자열 전체를 반환합니다:

```
use Illuminate\Support\Str;

$slice = Str::of('This is my name')->before('my name');

// 'This is '
```

<a name="method-fluent-str-before-last"></a>
#### `beforeLast`

마지막 출현 값 이전 문자열 전체 반환:

```
use Illuminate\Support\Str;

$slice = Str::of('This is my name')->beforeLast('is');

// 'This '
```

<a name="method-fluent-str-between"></a>
#### `between`

두 값 사이 문자열 일부 반환:

```
use Illuminate\Support\Str;

$converted = Str::of('This is my name')->between('This', 'name');

// ' is my '
```

<a name="method-fluent-str-between-first"></a>
#### `betweenFirst`

가능한 가장 작은 부분 문자열 반환:

```
use Illuminate\Support\Str;

$converted = Str::of('[a] bc [d]')->betweenFirst('[', ']');

// 'a'
```

<a name="method-fluent-str-camel"></a>
#### `camel`

문자열을 `camelCase` 변환:

```
use Illuminate\Support\Str;

$converted = Str::of('foo_bar')->camel();

// fooBar
```

<a name="method-fluent-str-class-basename"></a>
#### `classBasename`

네임스페이스 제외 클래스명 반환:

```
use Illuminate\Support\Str;

$class = Str::of('Foo\Bar\Baz')->classBasename();

// Baz
```

<a name="method-fluent-str-contains"></a>
#### `contains`

대소문자 구분하며 특정 값을 포함하는지:

```
use Illuminate\Support\Str;

$contains = Str::of('This is my name')->contains('my');

// true
```

배열로도 검사 가능:

```
use Illuminate\Support\Str;

$contains = Str::of('This is my name')->contains(['my', 'foo']);

// true
```

<a name="method-fluent-str-contains-all"></a>
#### `containsAll`

모든 값 포함 여부 검사:

```
use Illuminate\Support\Str;

$containsAll = Str::of('This is my name')->containsAll(['my', 'name']);

// true
```

<a name="method-fluent-str-dirname"></a>
#### `dirname`

부모 디렉토리 경로 반환:

```
use Illuminate\Support\Str;

$string = Str::of('/foo/bar/baz')->dirname();

// '/foo/bar'
```

원한다면 몇 단계 부모까지 지정 가능:

```
use Illuminate\Support\Str;

$string = Str::of('/foo/bar/baz')->dirname(2);

// '/foo'
```

<a name="method-fluent-str-excerpt"></a>
#### `excerpt`

특정 구절 중심 발췌:

```
use Illuminate\Support\Str;

$excerpt = Str::of('This is my name')->excerpt('my', [
    'radius' => 3
]);

// '...is my na...'
```

옵션은 위와 같습니다.

<a name="method-fluent-str-ends-with"></a>
#### `endsWith`

특정 값으로 끝나는지 판단:

```
use Illuminate\Support\Str;

$result = Str::of('This is my name')->endsWith('name');

// true
```

배열도 가능:

```
use Illuminate\Support\Str;

$result = Str::of('This is my name')->endsWith(['name', 'foo']);

// true

$result = Str::of('This is my name')->endsWith(['this', 'foo']);

// false
```

<a name="method-fluent-str-exactly"></a>
#### `exactly`

두 문자열이 완전히 같은지 검사:

```
use Illuminate\Support\Str;

$result = Str::of('Laravel')->exactly('Laravel');

// true
```

<a name="method-fluent-str-explode"></a>
#### `explode`

문자열을 구분자 기준으로 나누고 컬렉션 형태로 반환:

```
use Illuminate\Support\Str;

$collection = Str::of('foo bar baz')->explode(' ');

// collect(['foo', 'bar', 'baz'])
```

<a name="method-fluent-str-finish"></a>
#### `finish`

문자열 끝에 지정값이 없으면 한 번만 추가:

```
use Illuminate\Support\Str;

$adjusted = Str::of('this/string')->finish('/');

// this/string/

$adjusted = Str::of('this/string/')->finish('/');

// this/string/
```

<a name="method-fluent-str-headline"></a>
#### `headline`

케이스, 하이픈, 언더스코어 구분 문자열을 각 단어 첫 글자 대문자 공백 문자열로 변환:

```
use Illuminate\Support\Str;

$headline = Str::of('taylor_otwell')->headline();

// Taylor Otwell

$headline = Str::of('EmailNotificationSent')->headline();

// Email Notification Sent
```

<a name="method-fluent-str-inline-markdown"></a>
#### `inlineMarkdown`

GitHub 스타일 마크다운을 인라인 HTML로 변환. 블록 태그로 자동 감싸지 않음:

```
use Illuminate\Support\Str;

$html = Str::of('**Laravel**')->inlineMarkdown();

// <strong>Laravel</strong>
```

<a name="method-fluent-str-is"></a>
#### `is`

와일드카드(*) 포함 패턴과 문자열 일치 검사:

```
use Illuminate\Support\Str;

$matches = Str::of('foobar')->is('foo*');

// true

$matches = Str::of('foobar')->is('baz*');

// false
```

<a name="method-fluent-str-is-ascii"></a>
#### `isAscii`

문자열이 ASCII 인지 판단:

```
use Illuminate\Support\Str;

$result = Str::of('Taylor')->isAscii();

// true

$result = Str::of('ü')->isAscii();

// false
```

<a name="method-fluent-str-is-empty"></a>
#### `isEmpty`

문자열이 비어있는지 검사:

```
use Illuminate\Support\Str;

$result = Str::of('  ')->trim()->isEmpty();

// true

$result = Str::of('Laravel')->trim()->isEmpty();

// false
```

<a name="method-fluent-str-is-not-empty"></a>
#### `isNotEmpty`

문자열이 비어있지 않은지 검사:

```
use Illuminate\Support\Str;

$result = Str::of('  ')->trim()->isNotEmpty();

// false

$result = Str::of('Laravel')->trim()->isNotEmpty();

// true
```

<a name="method-fluent-str-is-json"></a>
#### `isJson`

문자열이 유효 JSON인지 검사:

```
use Illuminate\Support\Str;

$result = Str::of('[1,2,3]')->isJson();

// true

$result = Str::of('{"first": "John", "last": "Doe"}')->isJson();

// true

$result = Str::of('{first: "John", last: "Doe"}')->isJson();

// false
```

<a name="method-fluent-str-is-ulid"></a>
#### `isUlid`

문자열이 ULID인지 검사:

```
use Illuminate\Support\Str;

$result = Str::of('01gd6r360bp37zj17nxb55yv40')->isUlid();

// true

$result = Str::of('Taylor')->isUlid();

// false
```

<a name="method-fluent-str-is-uuid"></a>
#### `isUuid`

문자열이 UUID인지 검사:

```
use Illuminate\Support\Str;

$result = Str::of('5ace9ab9-e9cf-4ec6-a19d-5881212a452c')->isUuid();

// true

$result = Str::of('Taylor')->isUuid();

// false
```

<a name="method-fluent-str-kebab"></a>
#### `kebab`

`kebab-case` 변환:

```
use Illuminate\Support\Str;

$converted = Str::of('fooBar')->kebab();

// foo-bar
```

<a name="method-fluent-str-lcfirst"></a>
#### `lcfirst`

첫 글자 소문자 변환:

```
use Illuminate\Support\Str;

$string = Str::of('Foo Bar')->lcfirst();

// foo Bar
```


<a name="method-fluent-str-length"></a>
#### `length`

문자열 길이 반환:

```
use Illuminate\Support\Str;

$length = Str::of('Laravel')->length();

// 7
```

<a name="method-fluent-str-limit"></a>
#### `limit`

문자열 잘라내기:

```
use Illuminate\Support\Str;

$truncated = Str::of('The quick brown fox jumps over the lazy dog')->limit(20);

// The quick brown fox...
```

잘림 표시 문자열도 전달 가능:

```
use Illuminate\Support\Str;

$truncated = Str::of('The quick brown fox jumps over the lazy dog')->limit(20, ' (...)');

// The quick brown fox (...)
```

<a name="method-fluent-str-lower"></a>
#### `lower`

소문자 변환:

```
use Illuminate\Support\Str;

$result = Str::of('LARAVEL')->lower();

// 'laravel'
```

<a name="method-fluent-str-ltrim"></a>
#### `ltrim`

문자열 왼쪽 공백 등 제거:

```
use Illuminate\Support\Str;

$string = Str::of('  Laravel  ')->ltrim();

// 'Laravel  '

$string = Str::of('/Laravel/')->ltrim('/');

// 'Laravel/'
```

<a name="method-fluent-str-markdown"></a>
#### `markdown`

GitHub 마크다운을 HTML로 변환:

```
use Illuminate\Support\Str;

$html = Str::of('# Laravel')->markdown();

// <h1>Laravel</h1>

$html = Str::of('# Taylor <b>Otwell</b>')->markdown([
    'html_input' => 'strip',
]);

// <h1>Taylor Otwell</h1>
```

<a name="method-fluent-str-mask"></a>
#### `mask`

문자열 일부 마스킹:

```
use Illuminate\Support\Str;

$string = Str::of('taylor@example.com')->mask('*', 3);

// tay***************
```

음수 인수로 가리기 시작 위치 조절 가능:

```
$string = Str::of('taylor@example.com')->mask('*', -15, 3);

// tay***@example.com

$string = Str::of('taylor@example.com')->mask('*', 4, -4);

// tayl**********.com
```

<a name="method-fluent-str-match"></a>
#### `match`

정규식 패턴과 일치하는 문자열 일부 반환:

```
use Illuminate\Support\Str;

$result = Str::of('foo bar')->match('/bar/');

// 'bar'

$result = Str::of('foo bar')->match('/foo (.*)/');

// 'bar'
```

<a name="method-fluent-str-match-all"></a>
#### `matchAll`

패턴과 일치하는 모든 문자열을 컬렉션으로 반환:

```
use Illuminate\Support\Str;

$result = Str::of('bar foo bar')->matchAll('/bar/');

// collect(['bar', 'bar'])
```

만약 그룹을 지정하면 해당 그룹 매칭 결과만 모읍니다:

```
use Illuminate\Support\Str;

$result = Str::of('bar fun bar fly')->matchAll('/f(\w*)/');

// collect(['un', 'ly']);
```

일치하는 문자열이 없으면 빈 컬렉션 반환.

<a name="method-fluent-str-new-line"></a>
#### `newLine`

문자열 뒤에 줄바꿈 문자를 추가:

```
use Illuminate\Support\Str;

$padded = Str::of('Laravel')->newLine()->append('Framework');

// 'Laravel
//  Framework'
```

<a name="method-fluent-str-padboth"></a>
#### `padBoth`

좌우 양쪽에 지정 문자열로 패딩:

```
use Illuminate\Support\Str;

$padded = Str::of('James')->padBoth(10, '_');

// '__James___'

$padded = Str::of('James')->padBoth(10);

// '  James   '
```

<a name="method-fluent-str-padleft"></a>
#### `padLeft`

왼쪽에 패딩:

```
use Illuminate\Support\Str;

$padded = Str::of('James')->padLeft(10, '-=');

// '-=-=-James'

$padded = Str::of('James')->padLeft(10);

// '     James'
```

<a name="method-fluent-str-padright"></a>
#### `padRight`

오른쪽에 패딩:

```
use Illuminate\Support\Str;

$padded = Str::of('James')->padRight(10, '-');

// 'James-----'

$padded = Str::of('James')->padRight(10);

// 'James     '
```

<a name="method-fluent-str-pipe"></a>
#### `pipe`

현재 문자열을 콜러블에 전달해 변환 후 결과 반환:

```
use Illuminate\Support\Str;

$hash = Str::of('Laravel')->pipe('md5')->prepend('Checksum: ');

// 'Checksum: a5c95b86291ea299fcbe64458ed12702'

$closure = Str::of('foo')->pipe(function ($str) {
    return 'bar';
});

// 'bar'
```

<a name="method-fluent-str-plural"></a>
#### `plural`

단수 문자열을 복수형으로 변환:

```
use Illuminate\Support\Str;

$plural = Str::of('car')->plural();

// cars

$plural = Str::of('child')->plural();

// children
```

두 번째 인수로 단수/복수 선택:

```
use Illuminate\Support\Str;

$plural = Str::of('child')->plural(2);

// children

$plural = Str::of('child')->plural(1);

// child
```

<a name="method-fluent-str-prepend"></a>
#### `prepend`

문자열 앞에 지정값을 추가:

```
use Illuminate\Support\Str;

$string = Str::of('Framework')->prepend('Laravel ');

// Laravel Framework
```

<a name="method-fluent-str-remove"></a>
#### `remove`

문자열에서 지정 값 또는 배열 값을 제거:

```
use Illuminate\Support\Str;

$string = Str::of('Arkansas is quite beautiful!')->remove('quite');

// Arkansas is beautiful!
```

대소문자 구분 없애려면 두 번째 인수에 `false` 전달.

<a name="method-fluent-str-replace"></a>
#### `replace`

문자열 내 특정 문자열 교체:

```
use Illuminate\Support\Str;

$replaced = Str::of('Laravel 6.x')->replace('6.x', '7.x');

// Laravel 7.x
```

<a name="method-fluent-str-replace-array"></a>
#### `replaceArray`

문자열 내 특정 값을 배열로 순차 교체:

```
use Illuminate\Support\Str;

$string = 'The event will take place between ? and ?';

$replaced = Str::of($string)->replaceArray('?', ['8:30', '9:00']);

// The event will take place between 8:30 and 9:00
```

<a name="method-fluent-str-replace-first"></a>
#### `replaceFirst`

첫 번째 나타나는 특정 값을 교체:

```
use Illuminate\Support\Str;

$replaced = Str::of('the quick brown fox jumps over the lazy dog')->replaceFirst('the', 'a');

// a quick brown fox jumps over the lazy dog
```

<a name="method-fluent-str-replace-last"></a>
#### `replaceLast`

마지막 나타나는 특정 값을 교체:

```
use Illuminate\Support\Str;

$replaced = Str::of('the quick brown fox jumps over the lazy dog')->replaceLast('the', 'a');

// the quick brown fox jumps over a lazy dog
```

<a name="method-fluent-str-replace-matches"></a>
#### `replaceMatches`

문자열에서 정규식과 매칭되는 모든 부분을 지정 문자열로 교체합니다:

```
use Illuminate\Support\Str;

$replaced = Str::of('(+1) 501-555-1000')->replaceMatches('/[^A-Za-z0-9]++/', '')

// '15015551000'
```

콜백을 사용해 교체 로직을 직접 구현할 수도 있습니다:

```
use Illuminate\Support\Str;

$replaced = Str::of('123')->replaceMatches('/\d/', function ($match) {
    return '['.$match[0].']';
});

// '[1][2][3]'
```

<a name="method-fluent-str-rtrim"></a>
#### `rtrim`

문자열 오른쪽 공백 등 제거:

```
use Illuminate\Support\Str;

$string = Str::of('  Laravel  ')->rtrim();

// '  Laravel'

$string = Str::of('/Laravel/')->rtrim('/');

// '/Laravel'
```

<a name="method-fluent-str-scan"></a>
#### `scan`

[`sscanf` PHP 함수](https://www.php.net/manual/en/function.sscanf.php)와 동일한 형식 문자열에 따라 문자열을 파싱하여 컬렉션으로 반환합니다:

```
use Illuminate\Support\Str;

$collection = Str::of('filename.jpg')->scan('%[^.].%s');

// collect(['filename', 'jpg'])
```

<a name="method-fluent-str-singular"></a>
#### `singular`

단수형으로 변환:

```
use Illuminate\Support\Str;

$singular = Str::of('cars')->singular();

// car

$singular = Str::of('children')->singular();

// child
```

<a name="method-fluent-str-slug"></a>
#### `slug`

URL 친화적 슬러그 생성:

```
use Illuminate\Support\Str;

$slug = Str::of('Laravel Framework')->slug('-');

// laravel-framework
```

<a name="method-fluent-str-snake"></a>
#### `snake`

`snake_case` 변환:

```
use Illuminate\Support\Str;

$converted = Str::of('fooBar')->snake();

// foo_bar
```

<a name="method-fluent-str-split"></a>
#### `split`

정규식으로 문자열 분리 후 컬렉션 반환:

```
use Illuminate\Support\Str;

$segments = Str::of('one, two, three')->split('/[\s,]+/');

// collect(["one", "two", "three"])
```

<a name="method-fluent-str-squish"></a>
#### `squish`

불필요한 모든 공백 제거:

```
use Illuminate\Support\Str;

$string = Str::of('    laravel    framework    ')->squish();

// laravel framework
```

<a name="method-fluent-str-start"></a>
#### `start`

문자열이 지정 값으로 시작하지 않으면 한 번만 추가:

```
use Illuminate\Support\Str;

$adjusted = Str::of('this/string')->start('/');

// /this/string

$adjusted = Str::of('/this/string')->start('/');

// /this/string
```

<a name="method-fluent-str-starts-with"></a>
#### `startsWith`

문자열 시작 검사:

```
use Illuminate\Support\Str;

$result = Str::of('This is my name')->startsWith('This');

// true
```

<a name="method-fluent-str-studly"></a>
#### `studly`

`StudlyCase` 변환:

```
use Illuminate\Support\Str;

$converted = Str::of('foo_bar')->studly();

// FooBar
```

<a name="method-fluent-str-substr"></a>
#### `substr`

지정 시작과 길이만큼 문자열 일부 추출:

```
use Illuminate\Support\Str;

$string = Str::of('Laravel Framework')->substr(8);

// Framework

$string = Str::of('Laravel Framework')->substr(8, 5);

// Frame
```

<a name="method-fluent-str-substrreplace"></a>
#### `substrReplace`

지정 위치부터 지정 길이만큼 문자열 대체. 길이 0이면 기존 문자 덮어쓰기 없이 삽입:

```
use Illuminate\Support\Str;

$string = Str::of('1300')->substrReplace(':', 2);

// 13:

$string = Str::of('The Framework')->substrReplace(' Laravel', 3, 0);

// The Laravel Framework
```

<a name="method-fluent-str-swap"></a>
#### `swap`

`strtr`로 여러 문자열 동시 교체:

```
use Illuminate\Support\Str;

$string = Str::of('Tacos are great!')
    ->swap([
        'Tacos' => 'Burritos',
        'great' => 'fantastic',
    ]);

// Burritos are fantastic!
```

<a name="method-fluent-str-tap"></a>
#### `tap`

문자열을 클로저에 전달해 조작하지만, 원래 문자열을 변경하지 않고 반환합니다:

```
use Illuminate\Support\Str;

$string = Str::of('Laravel')
    ->append(' Framework')
    ->tap(function ($string) {
        dump('String after append: '.$string);
    })
    ->upper();

// LARAVEL FRAMEWORK
```

<a name="method-fluent-str-test"></a>
#### `test`

정규식에 문자열이 일치하는지 확인:

```
use Illuminate\Support\Str;

$result = Str::of('Laravel Framework')->test('/Laravel/');

// true
```

<a name="method-fluent-str-title"></a>
#### `title`

각 단어 첫 글자 대문자인 Title Case 변환:

```
use Illuminate\Support\Str;

$converted = Str::of('a nice title uses the correct case')->title();

// A Nice Title Uses The Correct Case
```

<a name="method-fluent-str-trim"></a>
#### `trim`

문자열 양쪽 공백 또는 지정 문자 제거:

```
use Illuminate\Support\Str;

$string = Str::of('  Laravel  ')->trim();

// 'Laravel'

$string = Str::of('/Laravel/')->trim('/');

// 'Laravel'
```

<a name="method-fluent-str-ucfirst"></a>
#### `ucfirst`

첫 글자 대문자 변환:

```
use Illuminate\Support\Str;

$string = Str::of('foo bar')->ucfirst();

// Foo bar
```

<a name="method-fluent-str-ucsplit"></a>
#### `ucsplit`

대문자 기준 분할하여 컬렉션 반환:

```
use Illuminate\Support\Str;

$string = Str::of('Foo Bar')->ucsplit();

// collect(['Foo', 'Bar'])
```

<a name="method-fluent-str-upper"></a>
#### `upper`

대문자 변환:

```
use Illuminate\Support\Str;

$adjusted = Str::of('laravel')->upper();

// LARAVEL
```

<a name="method-fluent-str-when"></a>
#### `when`

조건이 `true`일 때 클로저를 호출하여 문자열을 변환할 수 있습니다:

```
use Illuminate\Support\Str;

$string = Str::of('Taylor')
                ->when(true, function ($string) {
                    return $string->append(' Otwell');
                });

// 'Taylor Otwell'
```

조건이 `false`일 때 실행할 클로저를 세 번째 인수로 전달 가능.

<a name="method-fluent-str-when-contains"></a>
#### `whenContains`

문자열이 특정 값을 포함할 때 클로저 호출:

```
use Illuminate\Support\Str;

$string = Str::of('tony stark')
            ->whenContains('tony', function ($string) {
                return $string->title();
            });

// 'Tony Stark'
```

조건이 부합하지 않을 때 실행할 클로저도 전달 가능. 배열로 여러 값을 검사 가능.

<a name="method-fluent-str-when-contains-all"></a>
#### `whenContainsAll`

문자열이 모든 서브 문자열을 포함할 때 클로저 호출:

```
use Illuminate\Support\Str;

$string = Str::of('tony stark')
                ->whenContainsAll(['tony', 'stark'], function ($string) {
                    return $string->title();
                });

// 'Tony Stark'
```

부합하지 않은 경우 대체 클로저 전달 가능.

<a name="method-fluent-str-when-empty"></a>
#### `whenEmpty`

문자열이 비었을 때 클로저 호출. 클로저 반환값을 반환하거나 없으면 원래 문자열 반환:

```
use Illuminate\Support\Str;

$string = Str::of('  ')->whenEmpty(function ($string) {
    return $string->trim()->prepend('Laravel');
});

// 'Laravel'
```

<a name="method-fluent-str-when-not-empty"></a>
#### `whenNotEmpty`

문자열이 비어있지 않을 때 클로저 호출:

```
use Illuminate\Support\Str;

$string = Str::of('Framework')->whenNotEmpty(function ($string) {
    return $string->prepend('Laravel ');
});

// 'Laravel Framework'
```

<a name="method-fluent-str-when-starts-with"></a>
#### `whenStartsWith`

문자열이 특정 서브 문자열로 시작하면 클로저 호출:

```
use Illuminate\Support\Str;

$string = Str::of('disney world')->whenStartsWith('disney', function ($string) {
    return $string->title();
});

// 'Disney World'
```

<a name="method-fluent-str-when-ends-with"></a>
#### `whenEndsWith`

문자열이 특정 서브 문자열로 끝나면 클로저 호출:

```
use Illuminate\Support\Str;

$string = Str::of('disney world')->whenEndsWith('world', function ($string) {
    return $string->title();
});

// 'Disney World'
```

<a name="method-fluent-str-when-exactly"></a>
#### `whenExactly`

문자열이 정확히 특정 문자열과 일치할 때 클로저 호출:

```
use Illuminate\Support\Str;

$string = Str::of('laravel')->whenExactly('laravel', function ($string) {
    return $string->title();
});

// 'Laravel'
```

<a name="method-fluent-str-when-not-exactly"></a>
#### `whenNotExactly`

문자열이 정확히 특정 문자열과 일치하지 않을 때 클로저 호출:

```
use Illuminate\Support\Str;

$string = Str::of('framework')->whenNotExactly('laravel', function ($string) {
    return $string->title();
});

// 'Framework'
```

<a name="method-fluent-str-when-is"></a>
#### `whenIs`

문자열이 와일드카드 포함 패턴과 일치할 때 클로저 호출:

```
use Illuminate\Support\Str;

$string = Str::of('foo/bar')->whenIs('foo/*', function ($string) {
    return $string->append('/baz');
});

// 'foo/bar/baz'
```

<a name="method-fluent-str-when-is-ascii"></a>
#### `whenIsAscii`

문자열이 7비트 ASCII일 때 클로저 호출:

```
use Illuminate\Support\Str;

$string = Str::of('laravel')->whenIsAscii(function ($string) {
    return $string->title();
});

// 'Laravel'
```

<a name="method-fluent-str-when-is-ulid"></a>
#### `whenIsUlid`

문자열이 ULID라면 클로저 호출:

```
use Illuminate\Support\Str;

$string = Str::of('01gd6r360bp37zj17nxb55yv40')->whenIsUlid(function ($string) {
    return $string->substr(0, 8);
});

// '01gd6r36'
```

<a name="method-fluent-str-when-is-uuid"></a>
#### `whenIsUuid`

문자열이 UUID라면 클로저 호출:

```
use Illuminate\Support\Str;

$string = Str::of('a0a2a2d2-0b87-4a18-83f2-2529882be2de')->whenIsUuid(function ($string) {
    return $string->substr(0, 8);
});

// 'a0a2a2d2'
```

<a name="method-fluent-str-when-test"></a>
#### `whenTest`

정규식과 매칭되면 클로저 호출:

```
use Illuminate\Support\Str;

$string = Str::of('laravel framework')->whenTest('/laravel/', function ($string) {
    return $string->title();
});

// 'Laravel Framework'
```

<a name="method-fluent-str-word-count"></a>
#### `wordCount`

문자열 단어 수 반환:

```php
use Illuminate\Support\Str;

Str::of('Hello, world!')->wordCount(); // 2
```

<a name="method-fluent-str-words"></a>
#### `words`

지정 단어 수까지 문자열 제한. 잘림 표시 문자열 전달 가능:

```
use Illuminate\Support\Str;

$string = Str::of('Perfectly balanced, as all things should be.')->words(3, ' >>>');

// Perfectly balanced, as >>>
```

<a name="urls"></a>
## URL 관련 (URLs)

<a name="method-action"></a>
#### `action()`

컨트롤러 액션을 위한 URL을 생성합니다:

```
use App\Http\Controllers\HomeController;

$url = action([HomeController::class, 'index']);
```

파라미터가 있다면 두 번째 인수로 전달 가능:

```
$url = action([UserController::class, 'profile'], ['id' => 1]);
```

<a name="method-asset"></a>
#### `asset()`

요청 스킴을 사용하여 애셋의 URL을 생성합니다(HTTP/HTTPS):

```
$url = asset('img/photo.jpg');
```

`.env` 파일 내 `ASSET_URL` 변수로 호스트를 설정할 수 있습니다:

```
// ASSET_URL=http://example.com/assets

$url = asset('img/photo.jpg'); // http://example.com/assets/img/photo.jpg
```

<a name="method-route"></a>
#### `route()`

이름 있는 라우트를 위한 URL을 생성합니다:

```
$url = route('route.name');
```

파라미터가 있다면 두 번째 인수로 전달 가능:

```
$url = route('route.name', ['id' => 1]);
```

기본은 절대 URL 생성이며, 상대 URL을 원하면 세 번째 인수에 `false` 전달:

```
$url = route('route.name', ['id' => 1], false);
```

<a name="method-secure-asset"></a>
#### `secure_asset()`

HTTPS를 사용해 애셋 URL 생성:

```
$url = secure_asset('img/photo.jpg');
```

<a name="method-secure-url"></a>
#### `secure_url()`

지정 경로에 대한 완전한 HTTPS URL 생성. 추가 URL 세그먼트는 두 번째 인수로 전달:

```
$url = secure_url('user/profile');

$url = secure_url('user/profile', [1]);
```

<a name="method-to-route"></a>
#### `to_route()`

이름 있는 라우트로 리다이렉트 응답을 생성합니다:

```
return to_route('users.show', ['user' => 1]);
```

세 번째/네 번째 인수로 HTTP 상태코드 및 응답 헤더 지정 가능:

```
return to_route('users.show', ['user' => 1], 302, ['X-Framework' => 'Laravel']);
```

<a name="method-url"></a>
#### `url()`

지정 경로에 완전한 URL을 생성합니다:

```
$url = url('user/profile');

$url = url('user/profile', [1]);
```

경로가 없으면 `Illuminate\Routing\UrlGenerator` 인스턴스 반환:

```
$current = url()->current();

$full = url()->full();

$previous = url()->previous();
```

<a name="miscellaneous"></a>
## 기타 (Miscellaneous)

<a name="method-abort"></a>
#### `abort()`

HTTP 예외를 발생시켜 [예외 핸들러]에 의해 렌더링됩니다:

```
abort(403);
```

메시지 및 커스텀 HTTP 헤더도 전달할 수 있습니다:

```
abort(403, 'Unauthorized.', $headers);
```

<a name="method-abort-if"></a>
#### `abort_if()`

조건이 `true`일 때 HTTP 예외 발생:

```
abort_if(! Auth::user()->isAdmin(), 403);
```

<a name="method-abort-unless"></a>
#### `abort_unless()`

조건이 `false`일 때 HTTP 예외 발생:

```
abort_unless(Auth::user()->isAdmin(), 403);
```

<a name="method-app"></a>
#### `app()`

서비스 컨테이너 인스턴스를 반환합니다:

```
$container = app();
```

클래스나 인터페이스 이름을 전달해 인스턴스 주입 가능:

```
$api = app('HelpSpot\API');
```

<a name="method-auth"></a>
#### `auth()`

인증기 인스턴스를 반환합니다. `Auth` 파사드 대신 사용 가능:

```
$user = auth()->user();
```

가드 이름을 인자로 전달 가능:

```
$user = auth('admin')->user();
```

<a name="method-back"></a>
#### `back()`

사용자 이전 위치로 리다이렉트하는 응답을 생성합니다:

```
return back($status = 302, $headers = [], $fallback = '/');

return back();
```

<a name="method-bcrypt"></a>
#### `bcrypt()`

Bcrypt 해시로 비밀번호 등을 해싱합니다:

```
$password = bcrypt('my-secret-password');
```

<a name="method-blank"></a>
#### `blank()`

값이 "비어있는지" 판단합니다:

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

반대는 [`filled`](#method-filled) 함수 참조.

<a name="method-broadcast"></a>
#### `broadcast()`

이벤트를 방송합니다:

```
broadcast(new UserRegistered($user));

broadcast(new UserRegistered($user))->toOthers();
```

<a name="method-cache"></a>
#### `cache()`

캐시에서 값을 가져오거나 설정합니다. 키 없으면 기본값 반환:

```
$value = cache('key');

$value = cache('key', 'default');
```

배열로 키/값을 저장할 수도 있고 만료 시간 지정 가능:

```
cache(['key' => 'value'], 300);

cache(['key' => 'value'], now()->addSeconds(10));
```

<a name="method-class-uses-recursive"></a>
#### `class_uses_recursive()`

클래스 및 부모 클래스가 사용하는 모든 트레이트를 반환합니다:

```
$traits = class_uses_recursive(App\Models\User::class);
```

<a name="method-collect"></a>
#### `collect()`

컬렉션 인스턴스 생성:

```
$collection = collect(['taylor', 'abigail']);
```

<a name="method-config"></a>
#### `config()`

설정 값을 가져오거나 설정합니다. "닷" 표기법으로 접근 가능:

```
$value = config('app.timezone');

$value = config('app.timezone', $default);
```

실시간 설정 갱신도 가능, 다만 현재 요청에만 반영됨:

```
config(['app.debug' => true]);
```

<a name="method-cookie"></a>
#### `cookie()`

새 쿠키 인스턴스 생성:

```
$cookie = cookie('name', 'value', $minutes);
```

<a name="method-csrf-field"></a>
#### `csrf_field()`

CSRF 토큰을 가진 HTML `hidden` 필드 생성. Blade 예:

```
{{ csrf_field() }}
```

<a name="method-csrf-token"></a>
#### `csrf_token()`

현재 CSRF 토큰 값 반환:

```
$token = csrf_token();
```

<a name="method-decrypt"></a>
#### `decrypt()`

암호화된 값을 복호화:

```
$password = decrypt($value);
```

<a name="method-dd"></a>
#### `dd()`

변수 덤프 후 실행 중단:

```
dd($value);

dd($value1, $value2, $value3, ...);
```

실행 중단 없이 보고 싶으면 [`dump`](#method-dump) 사용.

<a name="method-dispatch"></a>
#### `dispatch()`

잡을 큐에 푸시:

```
dispatch(new App\Jobs\SendEmails);
```

<a name="method-dump"></a>
#### `dump()`

변수 덤프:

```
dump($value);

dump($value1, $value2, $value3, ...);
```

실행 중단하려면 [`dd`](#method-dd) 사용.

<a name="method-encrypt"></a>
#### `encrypt()`

값 암호화:

```
$secret = encrypt('my-secret-value');
```

<a name="method-env"></a>
#### `env()`

환경 변수 값 가져오기 또는 기본값 반환:

```
$env = env('APP_ENV');

$env = env('APP_ENV', 'production');
```

> [!WARNING]  
> 배포 시 `config:cache`를 실행하면 `.env`가 로드되지 않아 `env` 함수는 설정 파일 내에서만 호출해야 합니다. 캐시가 있으면 모든 다른 호출은 `null` 반환.

<a name="method-event"></a>
#### `event()`

이벤트를 디스패치:

```
event(new UserRegistered($user));
```

<a name="method-fake"></a>
#### `fake()`

Faker 싱글톤 자동해결 함수. 팩토리, 시딩, 테스트, 뷰 프로토타이핑 등에 사용:

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

기본적으로 `config/app.php` 내 `app.faker_locale` 옵션을 사용하며, 인자로 지역 설정 전달 가능:

```
fake('nl_NL')->name()
```

<a name="method-filled"></a>
#### `filled()`

값이 비어있지 않은지 판단:

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

반대는 [`blank`](#method-blank) 함수 참조.

<a name="method-info"></a>
#### `info()`

로그에 정보 메시지 기록:

```
info('Some helpful information!');
```

컨텍스트 배열도 전달 가능:

```
info('User login attempt failed.', ['id' => $user->id]);
```

<a name="method-logger"></a>
#### `logger()`

디버그 레벨 로그 기록:

```
logger('Debug message');
```

컨텍스트 배열 가능:

```
logger('User has logged in.', ['id' => $user->id]);
```

값 없으면 로거 인스턴스 반환:

```
logger()->error('You are not allowed here.');
```

<a name="method-method-field"></a>
#### `method_field()`

HTML `hidden` 입력 필드 생성, 폼 HTTP 메서드 스푸핑에 사용:

```
<form method="POST">
    {{ method_field('DELETE') }}
</form>
```

<a name="method-now"></a>
#### `now()`

현재 시간을 갖는 `Illuminate\Support\Carbon` 인스턴스 생성:

```
$now = now();
```

<a name="method-old"></a>
#### `old()`

세션에 플래시된 이전 입력값을 가져옵니다:

```
$value = old('value');

$value = old('value', 'default');
```

Eloquent 모델 속성도 기본값으로 손쉽게 지정 가능:

```
{{ old('name', $user->name) }}

// 또는...

{{ old('name', $user) }}
```

<a name="method-optional"></a>
#### `optional()`

인자로 받은 객체나 배열의 속성/메서드에 접근할 때, 값이 null이면 `null` 반환:

```
return optional($user->address)->street;

{!! old('name', optional($user)->name) !!}
```

두 번째 인수로 클로저 전달 가능, 값이 null이 아니면 실행:

```
return optional(User::find($id), function ($user) {
    return $user->name;
});
```

<a name="method-policy"></a>
#### `policy()`

주어진 클래스에 대한 권한 정책 인스턴스를 반환:

```
$policy = policy(App\Models\User::class);
```

<a name="method-redirect"></a>
#### `redirect()`

리다이렉트 응답 반환. 인수 없으면 리다이렉터 반환:

```
return redirect($to = null, $status = 302, $headers = [], $https = null);

return redirect('/home');

return redirect()->route('route.name');
```

<a name="method-report"></a>
#### `report()`

예외를 예외 처리기에게 리포트:

```
report($e);
```

문자열 입력 시 예외 메시지로 사용:

```
report('Something went wrong.');
```

<a name="method-report-if"></a>
#### `report_if()`

조건이 `true`일 때 예외 리포트:

```
report_if($shouldReport, $e);

report_if($shouldReport, 'Something went wrong.');
```

<a name="method-report-unless"></a>
#### `report_unless()`

조건이 `false`일 때 예외 리포트:

```
report_unless($reportingDisabled, $e);

report_unless($reportingDisabled, 'Something went wrong.');
```

<a name="method-request"></a>
#### `request()`

현재 요청 인스턴스 반환 또는 입력값 조회:

```
$request = request();

$value = request('key', $default);
```

<a name="method-rescue"></a>
#### `rescue()`

클로저 실행 중 예외를 포착하고 예외 처리기에 전달한 뒤 요청을 계속 진행:

```
return rescue(function () {
    return $this->method();
});
```

두 번째 인수로 예외 시 반환할 기본값 또는 클로저 지정 가능:

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

<a name="method-resolve"></a>
#### `resolve()`

서비스 컨테이너에서 클래스나 인터페이스를 인스턴스화:

```
$api = resolve('HelpSpot\API');
```

<a name="method-response"></a>
#### `response()`

응답 인스턴스 생성 또는 팩토리 획득:

```
return response('Hello World', 200, $headers);

return response()->json(['foo' => 'bar'], 200, $headers);
```

<a name="method-retry"></a>
#### `retry()`

최대 시도 횟수까지 콜백을 재시도합니다. 예외가 발생하면 자동 재시도, 시도 초과 시 예외 throw:

```
return retry(5, function () {
    // 5회 시도, 시도 간 100ms 휴식
}, 100);
```

콜백 인수로 수면시간을 계산하는 클로저 사용 가능:

```
return retry(5, function () {
    // ...
}, function ($attempt, $exception) {
    return $attempt * 100;
});
```

진짜 대기시간 목록 배열도 가능:

```
return retry([100, 200], function () {
    // 1회차 100ms, 2회차 200ms 대기
});
```

특정 예외에만 재시도 하려면 네 번째 인수로 클로저 전달:

```
return retry(5, function () {
    // ...
}, 100, function ($exception) {
    return $exception instanceof RetryException;
});
```

<a name="method-session"></a>
#### `session()`

세션 값을 얻거나 설정:

```
$value = session('key');
```

배열로 여러값 설정 가능:

```
session(['chairs' => 7, 'instruments' => 3]);
```

세션 저장소 반환도 가능:

```
$value = session()->get('key');

session()->put('key', $value);
```

<a name="method-tap"></a>
#### `tap()`

값과 클로저를 받아, 클로저에 전달 후 본래 값을 반환합니다. 클로저 반환값은 무시합니다:

```
$user = tap(User::first(), function ($user) {
    $user->name = 'taylor';

    $user->save();
});
```

클로저 없이 호출하면 메서드 호출 후에도 원래 값을 반환하여 메서드 반환값 무시 가능:

```
$user = tap($user)->update([
    'name' => $name,
    'email' => $email,
]);
```

클래스에 `Illuminate\Support\Traits\Tappable` 트레잇 추가 시 메서드 구현:

```
return $user->tap(function ($user) {
    //
});
```

<a name="method-throw-if"></a>
#### `throw_if()`

조건이 `true`이면 예외를 던집니다:

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

조건이 `false`이면 예외를 던집니다:

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

현재 날짜 기준 `Illuminate\Support\Carbon` 인스턴스 생성:

```
$today = today();
```

<a name="method-trait-uses-recursive"></a>
#### `trait_uses_recursive()`

트레잇이 사용하는 모든 트레잇 반환:

```
$traits = trait_uses_recursive(\Illuminate\Notifications\Notifiable::class);
```

<a name="method-transform"></a>
#### `transform()`

값이 비어있지 않으면 클로저 실행 후 반환값을 반환합니다:

```
$callback = function ($value) {
    return $value * 2;
};

$result = transform(5, $callback);

// 10
```

값이 비었으면 기본값이나 클로저 반환값을 반환:

```
$result = transform(null, $callback, 'The value is blank');

// The value is blank
```

<a name="method-validator"></a>
#### `validator()`

검증기 인스턴스 생성, `Validator` 파사드 대체용:

```
$validator = validator($data, $rules, $messages);
```

<a name="method-value"></a>
#### `value()`

값 반환, 인자가 클로저면 클로저 실행 후 반환값 반환:

```
$result = value(true);

// true

$result = value(function () {
    return false;
});

// false
```

추가 인수를 클로저 인수로 전달 가능:

```
$result = value(function ($name) {
    return $name;
}, 'Taylor');

// 'Taylor'
```

<a name="method-view"></a>
#### `view()`

뷰 인스턴스 반환:

```
return view('auth.login');
```

<a name="method-with"></a>
#### `with()`

값을 반환합니다. 두 번째 인자로 클로저가 있으면 실행 후 결과 반환:

```
$callback = function ($value) {
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
### 성능 측정 (Benchmarking)

애플리케이션 특정 부분의 성능을 빠르게 테스트할 때 `Benchmark` 클래스를 사용해 콜백 실행에 걸린 밀리초를 측정할 수 있습니다:

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

기본은 콜백을 1회 실행하며, 결과는 브라우저나 콘솔에 표시됩니다.

실행 횟수를 두 번째 인수로 지정하면 해당 횟수만큼 실행 후 평균 실행 시간을 보여줍니다:

```
Benchmark::dd(fn () => User::count(), iterations: 10); // 0.5 ms
```

<a name="lottery"></a>
### 로또 기능 (Lottery)

Laravel 로또 클래스는 확률에 따라 콜백을 실행할 수 있게 하는 기능입니다. 예를 들어 일부 요청에만 특정 코드를 실행할 때 유용합니다:

```
use Illuminate\Support\Lottery;

Lottery::odds(1, 20)
    ->winner(fn () => $user->won())
    ->loser(fn () => $user->lost())
    ->choose();
```

로또 클래스를 다른 Laravel 기능과 결합해서, 예를 들어 느린 쿼리 일부만 예외 처리기에 보고할 수도 있습니다:

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
#### 로또 테스트

로또 결과를 쉽게 테스트할 수 있습니다:

```
// 로또가 항상 당첨
Lottery::alwaysWin();

// 로또가 항상 꽝
Lottery::alwaysLose();

// 로또가 한 번 당첨 후 한 번 꽝, 이후 정상 동작
Lottery::fix([true, false]);

// 로또를 정상 동작으로 되돌림
Lottery::determineResultsNormally();
```

# 끝.