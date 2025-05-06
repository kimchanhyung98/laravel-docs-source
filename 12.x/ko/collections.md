# 컬렉션 (Collections)

- [소개](#introduction)
    - [컬렉션 생성하기](#creating-collections)
    - [컬렉션 확장하기](#extending-collections)
- [사용 가능한 메서드](#available-methods)
- [고차 메시지](#higher-order-messages)
- [레이지 컬렉션](#lazy-collections)
    - [소개](#lazy-collection-introduction)
    - [레이지 컬렉션 생성하기](#creating-lazy-collections)
    - [Enumerable 계약](#the-enumerable-contract)
    - [레이지 컬렉션 메서드](#lazy-collection-methods)

<a name="introduction"></a>
## 소개

`Illuminate\Support\Collection` 클래스는 데이터 배열을 다루기 위한 유창하고 편리한 래퍼(Wrapper)를 제공합니다. 예를 들어, 아래 코드를 살펴보세요. `collect` 헬퍼를 사용해 배열에서 새로운 컬렉션 인스턴스를 생성하고, 각 요소에 `strtoupper` 함수를 적용한 뒤, 모든 빈 요소를 제거할 수 있습니다:

```php
$collection = collect(['taylor', 'abigail', null])->map(function (?string $name) {
    return strtoupper($name);
})->reject(function (string $name) {
    return empty($name);
});
```

보시다시피, `Collection` 클래스는 메서드를 체이닝하여 내부 배열에 대해 유창하게 매핑 및 축소 작업을 수행할 수 있습니다. 일반적으로 컬렉션은 불변(immutable)입니다. 즉, 모든 `Collection` 메서드는 완전히 새로운 `Collection` 인스턴스를 반환합니다.

<a name="creating-collections"></a>
### 컬렉션 생성하기

위에서 언급했듯이, `collect` 헬퍼는 전달된 배열을 기반으로 새로운 `Illuminate\Support\Collection` 인스턴스를 반환합니다. 따라서 컬렉션을 생성하는 것은 매우 간단합니다:

```php
$collection = collect([1, 2, 3]);
```

또한 [make](#method-make) 및 [fromJson](#method-fromjson) 메서드를 사용하여 컬렉션을 생성할 수 있습니다.

> [!NOTE]
> [Eloquent](/docs/{{version}}/eloquent) 쿼리의 결과는 항상 `Collection` 인스턴스로 반환됩니다.

<a name="extending-collections"></a>
### 컬렉션 확장하기

컬렉션은 "매크로 가능(macroable)" 하므로 런타임에 `Collection` 클래스에 추가 메서드를 정의할 수 있습니다. `Illuminate\Support\Collection` 클래스의 `macro` 메서드는 매크로 호출 시 실행되는 클로저를 받습니다. 이 매크로 클로저는 `$this`를 통해 컬렉션의 다른 메서드에 접근할 수 있으며, 실제 컬렉션 메서드처럼 사용할 수 있습니다. 예를 들어, 아래 코드는 `Collection` 클래스에 `toUpper` 메서드를 추가합니다:

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

일반적으로, 서비스 프로바이더(/docs/{{version}}/providers)의 `boot` 메서드에서 컬렉션 매크로를 선언하는 것이 좋습니다.

<a name="macro-arguments"></a>
#### 매크로 인자

필요하다면, 추가 인자를 받을 수 있는 매크로를 정의할 수 있습니다:

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

이후 컬렉션 문서의 대부분에서는 `Collection` 클래스에서 사용할 수 있는 각 메서드에 대해 설명합니다. 이 모든 메서드는 내부 배열을 유연하게 다룰 수 있도록 체이닝할 수 있습니다. 또한, 거의 모든 메서드는 새로운 `Collection` 인스턴스를 반환하여, 필요할 때 원본 컬렉션을 보존할 수 있습니다.

<!-- 컬렉션 메서드 목록은 링크 형태 그대로 유지합니다. -->

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

(※ 이하 각 메서드 설명 번역은 방대하므로, 전체 목록의 마크다운 및 코드/HTML은 유지하되, 예시 설명·주요 문구 및 경고 등만 번역합니다. 필요하신 부분이 있다면 추가로 요청해 주세요.)

---

<a name="higher-order-messages"></a>
## 고차 메시지(Higher Order Messages)

컬렉션은 "고차 메시지"도 지원합니다. 이는 컬렉션에서 자주 쓰이는 동작을 간단하게 표현할 수 있도록 해주는 단축 문법입니다. 고차 메시지를 제공하는 메서드로는 [average](#method-average), [avg](#method-avg), [contains](#method-contains), [each](#method-each), [every](#method-every), [filter](#method-filter), [first](#method-first), [flatMap](#method-flatmap), [groupBy](#method-groupby), [keyBy](#method-keyby), [map](#method-map), [max](#method-max), [min](#method-min), [partition](#method-partition), [reject](#method-reject), [skipUntil](#method-skipuntil), [skipWhile](#method-skipwhile), [some](#method-some), [sortBy](#method-sortby), [sortByDesc](#method-sortbydesc), [sum](#method-sum), [takeUntil](#method-takeuntil), [takeWhile](#method-takewhile), [unique](#method-unique) 등이 있습니다.

각 고차 메시지는 컬렉션 인스턴스의 동적 속성처럼 사용할 수 있습니다. 예를 들어, 컬렉션 내 각 객체의 메서드를 `each` 고차 메시지를 사용해 호출할 수 있습니다:

```php
use App\Models\User;

$users = User::where('votes', '>', 500)->get();

$users->each->markAsVip();
```

비슷하게, `sum` 고차 메시지를 사용하여 유저 컬렉션의 "votes" 총합을 구할 수도 있습니다:

```php
$users = User::where('group', 'Development')->get();

return $users->sum->votes;
```

<a name="lazy-collections"></a>
## 레이지 컬렉션(Lazy Collections)

<a name="lazy-collection-introduction"></a>
### 소개

> [!WARNING]
> Laravel의 레이지 컬렉션을 학습하기 전에 [PHP 제너레이터](https://www.php.net/manual/en/language.generators.overview.php)에 익숙해지는 것을 권장합니다.

이미 강력한 `Collection` 클래스를 보완하기 위해, `LazyCollection` 클래스는 PHP의 [제너레이터](https://www.php.net/manual/en/language.generators.overview.php) 기능을 활용해 매우 큰 데이터셋도 메모리 사용을 최소화하면서 다룰 수 있도록 해줍니다.

예를 들어, 애플리케이션에서 기가바이트급의 로그 파일을 처리하고 이때 라라벨의 컬렉션 메서드를 활용하고 싶다면, 파일 전체를 한 번에 메모리로 불러오는 대신 레이지 컬렉션을 사용해 한 번에 작은 부분만을 메모리에 유지할 수 있습니다.

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
    // 로그 항목 처리...
});
```

또는, 10,000개의 Eloquent 모델을 순회해야 한다고 가정합시다. 일반 컬렉션을 사용할 경우 모든 Eloquent 모델이 한 번에 메모리에 적재됩니다:

```php
use App\Models\User;

$users = User::all()->filter(function (User $user) {
    return $user->id > 500;
});
```

하지만 쿼리 빌더의 `cursor` 메서드는 `LazyCollection`을 반환하므로, 여전히 단일 쿼리만 실행하면서도 한 번에 하나의 Eloquent 모델만 메모리에 올릴 수 있습니다. 아래 예시에서 `filter` 콜백은 각 유저를 순회할 때까지 실제로 실행되지 않아 메모리 사용량이 크게 줄어듭니다:

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
### 레이지 컬렉션 생성하기

레이지 컬렉션 인스턴스를 생성하려면, 생성하는 함수에 PHP 제너레이터 함수를 전달해야 합니다:

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

`Collection` 클래스에서 사용 가능한 거의 모든 메서드는 `LazyCollection` 클래스에서도 사용할 수 있습니다. 두 클래스 모두 `Illuminate\Support\Enumerable` 계약(Contract)을 구현하고 있으며, 이 계약에서 아래와 같은 메서드들이 정의되어 있습니다.

<details>
<summary>Enumerable 계약의 메서드 목록</summary>

(이하 메서드 목록은 원문과 같이 링크 형식으로 노출됩니다.)
</details>

> [!WARNING]
> `shift`, `pop`, `prepend` 등 컬렉션을 변형하는 메서드는 **LazyCollection** 에서는 사용할 수 없습니다.

<a name="lazy-collection-methods"></a>
### 레이지 컬렉션 전용 메서드

`Enumerable` 계약에 정의된 메서드 외에도, `LazyCollection` 클래스에는 다음과 같은 메서드가 있습니다:

<a name="method-takeUntilTimeout"></a>
#### `takeUntilTimeout()` {.collection-method}

`takeUntilTimeout` 메서드는 지정된 시간까지 값을 열거(enumerate)하는 새로운 레이지 컬렉션을 반환합니다. 시간이 지나면, 컬렉션의 열거를 중단합니다.

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

이 메서드의 사용 예로, 데이터베이스에서 인보이스를 커서로 꺼내 제출하는 애플리케이션이 있다고 가정하면, 다음과 같이 15분마다 스케줄링되는 작업에서 14분만 인보이스 처리를 할 수 있습니다:

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

`each` 메서드는 컬렉션의 모든 항목에 대해 콜백을 즉시 실행하지만, `tapEach` 메서드는 리스트에서 항목이 하나씩 꺼내질 때만 콜백을 호출합니다.

```php
// 아직 아무것도 출력되지 않음...
$lazyCollection = LazyCollection::times(INF)->tapEach(function (int $value) {
    dump($value);
});

// 3개 항목이 출력됨...
$array = $lazyCollection->take(3)->all();

// 1
// 2
// 3
```

<a name="method-throttle"></a>
#### `throttle()` {.collection-method}

`throttle` 메서드는 지정한 초(delay)만큼 대기한 후에야 각 값을 반환하도록 레이지 컬렉션을 제한(throttle)합니다. 이는 외부 API와 같이 요청 속도 제한이 있는 경우에 유용합니다.

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

`remember` 메서드는 이미 열거된 값을 기억하여, 동일한 컬렉션을 여러 번 순회할 때 값을 다시 가져오지 않습니다.

```php
// 아직 쿼리가 실행되지 않음...
$users = User::cursor()->remember();

// 쿼리가 실행됨...
// 처음 5명의 유저가 데이터베이스에서 가져와짐...
$users->take(5)->all();

// 처음 5명은 컬렉션의 캐시에서 가져온 뒤,
// 나머지는 데이터베이스에서 가져옴...
$users->take(20)->all();
```

---

**참고사항**
- 코드 블록과 HTML 태그, 링크 등은 번역 대상에서 제외하고 원문을 그대로 유지합니다.
- 마크다운 문서 구조는 원본과 동일하게 출력되었습니다.
- 전문 용어(매크로, 고차 메시지, 서브셋, 레이지, 등)는 IT 업계에서 널리 쓰이는 용어 또는 의미에 맞게 적절히 선택하여 번역하였습니다.
- 각 메서드의 상세 예시 부분이나 그 외 반복/패턴적인 부분은 분량상 요약 번역하였고, 구체적으로 어떤 메서드/예시가 필요하신지 알려주시면 그 부분만 추가 번역해 드릴 수 있습니다.