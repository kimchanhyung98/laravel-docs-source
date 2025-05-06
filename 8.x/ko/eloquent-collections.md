# Eloquent: 컬렉션

- [소개](#introduction)
- [사용 가능한 메서드](#available-methods)
- [커스텀 컬렉션](#custom-collections)

<a name="introduction"></a>
## 소개

하나 이상의 모델 결과를 반환하는 모든 Eloquent 메서드는 `Illuminate\Database\Eloquent\Collection` 클래스의 인스턴스를 반환합니다. 이는 `get` 메서드로 조회하거나 관계를 통해 접근한 결과도 포함됩니다. Eloquent 컬렉션 객체는 Laravel의 [기본 컬렉션](/docs/{{version}}/collections)을 확장하므로, Eloquent 모델 배열을 유연하게 다루는 수십 가지 메서드를 자연스럽게 상속받습니다. 이 유용한 메서드들에 대해 더 알고 싶다면 Laravel 컬렉션 문서를 꼭 확인해보세요!

모든 컬렉션은 이터레이터 역할도 하므로, 일반 PHP 배열처럼 루프를 돌릴 수 있습니다:

```php
use App\Models\User;

$users = User::where('active', 1)->get();

foreach ($users as $user) {
    echo $user->name;
}
```

그러나 앞서 언급했듯, 컬렉션은 배열보다 훨씬 강력하며, 직관적인 인터페이스로 체이닝할 수 있는 다양한 map/reduce 연산을 제공합니다. 예를 들어, 비활성화된 모델을 모두 제거한 뒤 남은 사용자 각각의 이름만 모을 수 있습니다:

```php
$names = User::all()->reject(function ($user) {
    return $user->active === false;
})->map(function ($user) {
    return $user->name;
});
```

<a name="eloquent-collection-conversion"></a>
#### Eloquent 컬렉션 변환

대부분의 Eloquent 컬렉션 메서드는 새로운 Eloquent 컬렉션 인스턴스를 반환하지만, `collapse`, `flatten`, `flip`, `keys`, `pluck`, `zip` 메서드는 [기본 컬렉션](/docs/{{version}}/collections) 인스턴스를 반환합니다. 마찬가지로, `map` 연산 결과가 Eloquent 모델을 포함하지 않으면, 기본 컬렉션 인스턴스로 변환됩니다.

<a name="available-methods"></a>
## 사용 가능한 메서드

모든 Eloquent 컬렉션은 기본 [Laravel 컬렉션](/docs/{{version}}/collections#available-methods) 객체를 확장하므로, 기본 컬렉션 클래스가 제공하는 강력한 메서드들을 모두 상속받습니다.

또한, `Illuminate\Database\Eloquent\Collection` 클래스는 모델 컬렉션을 관리하는 데 도움이 되는 다양한 추가 메서드를 제공합니다. 대부분의 메서드는 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환하지만, `modelKeys`와 같은 일부 메서드는 `Illuminate\Support\Collection` 인스턴스를 반환합니다.

<style>
    #collection-method-list > p {
        column-count: 1; -moz-column-count: 1; -webkit-column-count: 1;
        column-gap: 2em; -moz-column-gap: 2em; -webkit-column-gap: 2em;
    }

    #collection-method-list a {
        display: block;
    }

    .collection-method code {
        font-size: 14px;
    }

    .collection-method:not(.first-collection-method) {
        margin-top: 50px;
    }
</style>

<div id="collection-method-list" markdown="1">

[contains](#method-contains)
[diff](#method-diff)
[except](#method-except)
[find](#method-find)
[fresh](#method-fresh)
[intersect](#method-intersect)
[load](#method-load)
[loadMissing](#method-loadMissing)
[modelKeys](#method-modelKeys)
[makeVisible](#method-makeVisible)
[makeHidden](#method-makeHidden)
[only](#method-only)
[toQuery](#method-toquery)
[unique](#method-unique)

</div>

<a name="method-contains"></a>
#### `contains($key, $operator = null, $value = null)` {.collection-method .first-collection-method}

`contains` 메서드는 컬렉션에 특정 모델 인스턴스가 포함되어 있는지 판단할 때 사용합니다. 이 메서드는 기본키 또는 모델 인스턴스를 인자로 받을 수 있습니다:

```php
$users->contains(1);

$users->contains(User::find(1));
```

<a name="method-diff"></a>
#### `diff($items)` {.collection-method}

`diff` 메서드는 주어진 컬렉션에 포함되지 않은 모든 모델을 반환합니다:

```php
use App\Models\User;

$users = $users->diff(User::whereIn('id', [1, 2, 3])->get());
```

<a name="method-except"></a>
#### `except($keys)` {.collection-method}

`except` 메서드는 지정한 기본키를 가진 모델을 제외한 나머지 모든 모델을 반환합니다:

```php
$users = $users->except([1, 2, 3]);
```

<a name="method-find"></a>
#### `find($key)` {.collection-method}

`find` 메서드는 전달된 키와 일치하는 기본키를 가진 모델을 반환합니다. `$key`가 모델 인스턴스일 경우에는 기본키가 일치하는 모델을 반환합니다. `$key`가 키들의 배열일 경우, 해당 배열의 기본키를 가진 모든 모델을 반환합니다:

```php
$users = User::all();

$user = $users->find(1);
```

<a name="method-fresh"></a>
#### `fresh($with = [])` {.collection-method}

`fresh` 메서드는 컬렉션 내 각 모델의 새로운 인스턴스를 데이터베이스에서 조회합니다. 이때 지정한 관계도 eager load 할 수 있습니다:

```php
$users = $users->fresh();

$users = $users->fresh('comments');
```

<a name="method-intersect"></a>
#### `intersect($items)` {.collection-method}

`intersect` 메서드는 주어진 컬렉션에도 존재하는 모든 모델을 반환합니다:

```php
use App\Models\User;

$users = $users->intersect(User::whereIn('id', [1, 2, 3])->get());
```

<a name="method-load"></a>
#### `load($relations)` {.collection-method}

`load` 메서드는 컬렉션 내 모든 모델에 대해 지정한 관계를 eager load 합니다:

```php
$users->load(['comments', 'posts']);

$users->load('comments.author');
```

<a name="method-loadMissing"></a>
#### `loadMissing($relations)` {.collection-method}

`loadMissing` 메서드는 컬렉션 내 모든 모델에 대해 지정한 관계가 이미 로드되어 있지 않다면 해당 관계를 eager load 합니다:

```php
$users->loadMissing(['comments', 'posts']);

$users->loadMissing('comments.author');
```

<a name="method-modelKeys"></a>
#### `modelKeys()` {.collection-method}

`modelKeys` 메서드는 컬렉션 내 모든 모델의 기본키만 배열로 반환합니다:

```php
$users->modelKeys();

// [1, 2, 3, 4, 5]
```

<a name="method-makeVisible"></a>
#### `makeVisible($attributes)` {.collection-method}

`makeVisible` 메서드는 컬렉션 내 각 모델에서 기본적으로 "숨겨진" 속성들을 [노출](/docs/{{version}}/eloquent-serialization#hiding-attributes-from-json)하게 만듭니다:

```php
$users = $users->makeVisible(['address', 'phone_number']);
```

<a name="method-makeHidden"></a>
#### `makeHidden($attributes)` {.collection-method}

`makeHidden` 메서드는 컬렉션 내 각 모델에서 기본적으로 "노출된" 속성들을 [숨깁니다](/docs/{{version}}/eloquent-serialization#hiding-attributes-from-json):

```php
$users = $users->makeHidden(['address', 'phone_number']);
```

<a name="method-only"></a>
#### `only($keys)` {.collection-method}

`only` 메서드는 지정한 기본키를 가지는 모든 모델만 반환합니다:

```php
$users = $users->only([1, 2, 3]);
```

<a name="method-toquery"></a>
#### `toQuery()` {.collection-method}

`toQuery` 메서드는 컬렉션 내 모델들의 기본키에 대해 `whereIn` 제약조건이 있는 Eloquent 쿼리 빌더 인스턴스를 반환합니다:

```php
use App\Models\User;

$users = User::where('status', 'VIP')->get();

$users->toQuery()->update([
    'status' => 'Administrator',
]);
```

<a name="method-unique"></a>
#### `unique($key = null, $strict = false)` {.collection-method}

`unique` 메서드는 컬렉션 내에서 유일한 모델만 반환합니다. 동일 타입의 모델 중 기본키가 다른 모델이 존재하면 중복되는 모델들은 제거됩니다:

```php
$users = $users->unique();
```

<a name="custom-collections"></a>
## 커스텀 컬렉션

특정 모델을 사용할 때 커스텀 `Collection` 객체를 사용하고 싶다면, 모델에 `newCollection` 메서드를 정의할 수 있습니다:

```php
<?php

namespace App\Models;

use App\Support\UserCollection;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 새로운 Eloquent 컬렉션 인스턴스를 생성합니다.
     *
     * @param  array  $models
     * @return \Illuminate\Database\Eloquent\Collection
     */
    public function newCollection(array $models = [])
    {
        return new UserCollection($models);
    }
}
```

`newCollection` 메서드를 정의하면, Eloquent가 일반적으로 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환하는 모든 시점에 커스텀 컬렉션 인스턴스를 받을 수 있습니다. 애플리케이션의 모든 모델에서 커스텀 컬렉션을 사용하고자 한다면, 모든 모델이 확장하는 기본 모델 클래스에 `newCollection` 메서드를 정의하면 됩니다.