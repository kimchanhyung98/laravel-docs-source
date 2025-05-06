# Eloquent: 컬렉션

- [소개](#introduction)
- [사용 가능한 메서드](#available-methods)
- [커스텀 컬렉션](#custom-collections)

<a name="introduction"></a>
## 소개

여러 개의 모델 결과를 반환하는 모든 Eloquent 메서드는 `Illuminate\Database\Eloquent\Collection` 클래스의 인스턴스를 반환합니다. 이는 `get` 메서드로 조회된 결과나 관계를 통해 접근할 때도 마찬가지입니다. Eloquent 컬렉션 객체는 라라벨의 [기본 컬렉션](/docs/{{version}}/collections)을 확장하므로, Eloquent 모델 배열을 유연하게 다루기 위한 수십 가지 메서드를 자연스럽게 상속합니다. 이 유용한 메서드들에 대해 알고 싶다면 라라벨 컬렉션 문서를 꼭 참고하세요!

모든 컬렉션은 반복자(iterator)로도 동작하므로, PHP 배열처럼 간단히 순회할 수 있습니다:

```php
use App\Models\User;

$users = User::where('active', 1)->get();

foreach ($users as $user) {
    echo $user->name;
}
```

하지만 앞서 언급했듯이, 컬렉션은 단순한 배열보다 훨씬 강력합니다. 직관적인 인터페이스로 체이닝 할 수 있는 다양한 map/reduce 연산을 제공합니다. 예를 들어, 모든 비활성화된 모델을 제거한 후 남은 각 사용자의 이름만 수집할 수 있습니다:

```php
$names = User::all()->reject(function (User $user) {
    return $user->active === false;
})->map(function (User $user) {
    return $user->name;
});
```

<a name="eloquent-collection-conversion"></a>
#### Eloquent 컬렉션 변환

대부분의 Eloquent 컬렉션 메서드는 새로운 Eloquent 컬렉션 인스턴스를 반환하지만, `collapse`, `flatten`, `flip`, `keys`, `pluck`, `zip` 등의 메서드는 [기본 컬렉션](/docs/{{version}}/collections) 인스턴스를 반환합니다. 또한, `map` 연산의 결과가 Eloquent 모델을 포함하지 않을 경우에도 기본 컬렉션 인스턴스로 변환됩니다.

<a name="available-methods"></a>
## 사용 가능한 메서드

모든 Eloquent 컬렉션은 기본 [라라벨 컬렉션](/docs/{{version}}/collections#available-methods) 객체를 확장하므로, 기본 컬렉션 클래스의 강력한 모든 메서드를 사용할 수 있습니다.

추가로, `Illuminate\Database\Eloquent\Collection` 클래스는 모델 컬렉션 관리를 돕는 추가 메서드들을 제공합니다. 대부분의 메서드는 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환하지만, 일부 메서드(예: `modelKeys`)는 `Illuminate\Support\Collection` 인스턴스를 반환합니다.

<style>
    .collection-method-list > p {
        columns: 14.4em 1; -moz-columns: 14.4em 1; -webkit-columns: 14.4em 1;
    }

    .collection-method-list a {
        display: block;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    .collection-method code {
        font-size: 14px;
    }

    .collection-method:not(.first-collection-method) {
        margin-top: 50px;
    }
</style>

<div class="collection-method-list" markdown="1">

[append](#method-append)
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
[setVisible](#method-setVisible)
[setHidden](#method-setHidden)
[toQuery](#method-toquery)
[unique](#method-unique)

</div>

<a name="method-append"></a>
#### `append($attributes)` {.collection-method .first-collection-method}

`append` 메서드는 컬렉션의 모든 모델에 대해 [속성이 추가되도록](/docs/{{version}}/eloquent-serialization#appending-values-to-json) 지정할 수 있습니다. 이 메서드는 속성명 배열이나 단일 속성명을 받을 수 있습니다:

```php
$users->append('team');

$users->append(['team', 'is_admin']);
```

<a name="method-contains"></a>
#### `contains($key, $operator = null, $value = null)` {.collection-method}

`contains` 메서드는 컬렉션에 주어진 모델 인스턴스가 포함되어 있는지 확인합니다. 이 메서드는 기본 키 또는 모델 인스턴스를 받을 수 있습니다:

```php
$users->contains(1);

$users->contains(User::find(1));
```

<a name="method-diff"></a>
#### `diff($items)` {.collection-method}

`diff` 메서드는 전달된 컬렉션에 존재하지 않는 모든 모델을 반환합니다:

```php
use App\Models\User;

$users = $users->diff(User::whereIn('id', [1, 2, 3])->get());
```

<a name="method-except"></a>
#### `except($keys)` {.collection-method}

`except` 메서드는 주어진 기본 키를 가지지 않은 모든 모델을 반환합니다:

```php
$users = $users->except([1, 2, 3]);
```

<a name="method-find"></a>
#### `find($key)` {.collection-method}

`find` 메서드는 주어진 기본 키와 일치하는 모델을 반환합니다. `$key`가 모델 인스턴스라면, 그 인스턴스와 기본 키가 일치하는 모델을 반환합니다. `$key`가 키 배열이라면, 해당 배열에 키가 포함된 모든 모델을 반환합니다:

```php
$users = User::all();

$user = $users->find(1);
```

<a name="method-fresh"></a>
#### `fresh($with = [])` {.collection-method}

`fresh` 메서드는 컬렉션 내 각 모델의 최신 인스턴스를 데이터베이스에서 다시 조회합니다. 또한, 지정한 관계들도 eager loading됩니다:

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

`load` 메서드는 컬렉션 내 모든 모델에 대해 지정된 관계를 eager loading 합니다:

```php
$users->load(['comments', 'posts']);

$users->load('comments.author');

$users->load(['comments', 'posts' => fn ($query) => $query->where('active', 1)]);
```

<a name="method-loadMissing"></a>
#### `loadMissing($relations)` {.collection-method}

`loadMissing` 메서드는 컬렉션 내 모든 모델에 대해 해당 관계가 이미 로드되어 있지 않은 경우에 한해 관계를 eager loading합니다:

```php
$users->loadMissing(['comments', 'posts']);

$users->loadMissing('comments.author');

$users->loadMissing(['comments', 'posts' => fn ($query) => $query->where('active', 1)]);
```

<a name="method-modelKeys"></a>
#### `modelKeys()` {.collection-method}

`modelKeys` 메서드는 컬렉션 내 모든 모델의 기본 키 배열을 반환합니다:

```php
$users->modelKeys();

// [1, 2, 3, 4, 5]
```

<a name="method-makeVisible"></a>
#### `makeVisible($attributes)` {.collection-method}

`makeVisible` 메서드는 컬렉션 내 각 모델에서 일반적으로 "숨겨져"있는 [속성을 표시](/docs/{{version}}/eloquent-serialization#hiding-attributes-from-json)할 수 있게 합니다:

```php
$users = $users->makeVisible(['address', 'phone_number']);
```

<a name="method-makeHidden"></a>
#### `makeHidden($attributes)` {.collection-method}

`makeHidden` 메서드는 컬렉션 내 각 모델에서 일반적으로 "노출되어" 있는 [속성을 숨길](/docs/{{version}}/eloquent-serialization#hiding-attributes-from-json) 수 있습니다:

```php
$users = $users->makeHidden(['address', 'phone_number']);
```

<a name="method-only"></a>
#### `only($keys)` {.collection-method}

`only` 메서드는 주어진 기본 키를 가진 모든 모델만 반환합니다:

```php
$users = $users->only([1, 2, 3]);
```

<a name="method-setVisible"></a>
#### `setVisible($attributes)` {.collection-method}

`setVisible` 메서드는 컬렉션 내 각 모델의 노출 속성을 [임시로 재정의](/docs/{{version}}/eloquent-serialization#temporarily-modifying-attribute-visibility)합니다:

```php
$users = $users->setVisible(['id', 'name']);
```

<a name="method-setHidden"></a>
#### `setHidden($attributes)` {.collection-method}

`setHidden` 메서드는 컬렉션 내 각 모델의 숨김 속성을 [임시로 재정의](/docs/{{version}}/eloquent-serialization#temporarily-modifying-attribute-visibility)합니다:

```php
$users = $users->setHidden(['email', 'password', 'remember_token']);
```

<a name="method-toquery"></a>
#### `toQuery()` {.collection-method}

`toQuery` 메서드는 컬렉션 내 모델들의 기본 키에 대해 `whereIn` 조건이 걸린 Eloquent 쿼리 빌더 인스턴스를 반환합니다:

```php
use App\Models\User;

$users = User::where('status', 'VIP')->get();

$users->toQuery()->update([
    'status' => 'Administrator',
]);
```

<a name="method-unique"></a>
#### `unique($key = null, $strict = false)` {.collection-method}

`unique` 메서드는 컬렉션 내에서 중복되지 않는 모든 모델을 반환합니다. 동일한 기본 키를 가진 동일 타입의 모델이 여러 개 있다면, 하나만 남기고 제거됩니다:

```php
$users = $users->unique();
```

<a name="custom-collections"></a>
## 커스텀 컬렉션

특정 모델과 상호작용할 때 사용자 지정 `Collection` 객체를 사용하고 싶다면, 모델에 `newCollection` 메서드를 정의하면 됩니다:

```php
<?php

namespace App\Models;

use App\Support\UserCollection;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 새로운 Eloquent 컬렉션 인스턴스 생성.
     *
     * @param  array<int, \Illuminate\Database\Eloquent\Model>  $models
     * @return \Illuminate\Database\Eloquent\Collection<int, \Illuminate\Database\Eloquent\Model>
     */
    public function newCollection(array $models = []): Collection
    {
        return new UserCollection($models);
    }
}
```

`newCollection` 메서드를 정의하면, Eloquent가 일반적으로 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환하는 모든 경우에 커스텀 컬렉션 인스턴스를 받을 수 있습니다. 만약 애플리케이션의 모든 모델에 대해 커스텀 컬렉션을 사용하고 싶다면, 모든 모델이 상속하는 베이스 모델 클래스에 `newCollection` 메서드를 정의해야 합니다.