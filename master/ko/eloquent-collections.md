# Eloquent: 컬렉션

- [소개](#introduction)
- [사용 가능한 메서드](#available-methods)
- [커스텀 컬렉션](#custom-collections)

<a name="introduction"></a>
## 소개

여러 모델 결과를 반환하는 모든 Eloquent 메서드는 `Illuminate\Database\Eloquent\Collection` 클래스의 인스턴스를 반환합니다. 여기에는 `get` 메서드로 가져온 결과, 관계를 통해 접근한 결과가 모두 포함됩니다. Eloquent 컬렉션 객체는 Laravel의 [기본 컬렉션](/docs/{{version}}/collections)을 확장하므로, 기본 배열을 유연하게 다룰 수 있는 다양한 메서드를 자연스럽게 상속받게 됩니다. 이 유용한 메서드들에 대해 자세히 알아보려면 Laravel 컬렉션 문서도 꼭 참고하세요!

컬렉션은 반복자로도 동작하므로, 단순한 PHP 배열처럼 foreach로 순회할 수 있습니다.

```php
use App\Models\User;

$users = User::where('active', 1)->get();

foreach ($users as $user) {
    echo $user->name;
}
```

그러나 앞서 언급했듯이, 컬렉션은 배열보다 훨씬 강력하며, 직관적인 인터페이스로 체이닝할 수 있는 다양한 map/reduce 연산을 제공합니다. 예를 들어, 비활성화된 모델을 제외하고, 남은 사용자 각각의 이름만 모을 수도 있습니다.

```php
$names = User::all()->reject(function (User $user) {
    return $user->active === false;
})->map(function (User $user) {
    return $user->name;
});
```

<a name="eloquent-collection-conversion"></a>
#### Eloquent 컬렉션 변환

대부분의 Eloquent 컬렉션 메서드는 새로운 Eloquent 컬렉션 인스턴스를 반환하지만, `collapse`, `flatten`, `flip`, `keys`, `pluck`, `zip` 메서드는 [기본 컬렉션](/docs/{{version}}/collections) 인스턴스를 반환합니다. 마찬가지로, `map` 연산의 결과가 Eloquent 모델을 포함하지 않으면 기본 컬렉션 인스턴스로 변환됩니다.

<a name="available-methods"></a>
## 사용 가능한 메서드

모든 Eloquent 컬렉션은 기본 [Laravel 컬렉션](/docs/{{version}}/collections#available-methods) 객체를 확장하므로, 기본 컬렉션 클래스가 제공하는 강력한 메서드를 모두 상속받습니다.

추가로, `Illuminate\Database\Eloquent\Collection` 클래스는 모델 컬렉션 관리를 돕는 몇 가지 확장 메서드를 제공합니다. 대부분의 메서드는 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환하지만, `modelKeys`와 같은 일부 메서드는 `Illuminate\Support\Collection` 인스턴스를 반환합니다.

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
[findOrFail](#method-find-or-fail)
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

`append` 메서드는 컬렉션 내 모든 모델에 대해 [속성을 추가적으로 포함](/docs/{{version}}/eloquent-serialization#appending-values-to-json)하도록 지정할 수 있습니다. 배열 또는 단일 속성을 인자로 받을 수 있습니다.

```php
$users->append('team');

$users->append(['team', 'is_admin']);
```

<a name="method-contains"></a>
#### `contains($key, $operator = null, $value = null)` {.collection-method}

`contains` 메서드는 주어진 모델 인스턴스가 컬렉션에 포함되어 있는지 확인할 수 있습니다. 이 메서드는 기본키 혹은 모델 인스턴스를 인자로 받을 수 있습니다.

```php
$users->contains(1);

$users->contains(User::find(1));
```

<a name="method-diff"></a>
#### `diff($items)` {.collection-method}

`diff` 메서드는 주어진 컬렉션에 없는 모든 모델을 반환합니다.

```php
use App\Models\User;

$users = $users->diff(User::whereIn('id', [1, 2, 3])->get());
```

<a name="method-except"></a>
#### `except($keys)` {.collection-method}

`except` 메서드는 지정한 기본키와 일치하지 않는 모델만 반환합니다.

```php
$users = $users->except([1, 2, 3]);
```

<a name="method-find"></a>
#### `find($key)` {.collection-method}

`find` 메서드는 주어진 기본키와 일치하는 모델을 반환합니다. `$key`가 모델 인스턴스인 경우, 해당 기본키와 일치하는 모델을 시도해서 반환합니다. `$key`가 기본키 배열이라면, 해당 배열에 포함된 모든 모델을 반환합니다.

```php
$users = User::all();

$user = $users->find(1);
```

<a name="method-find-or-fail"></a>
#### `findOrFail($key)` {.collection-method}

`findOrFail` 메서드는 주어진 기본키와 일치하는 모델을 반환하거나, 일치하는 모델이 없으면 `Illuminate\Database\Eloquent\ModelNotFoundException` 예외를 던집니다.

```php
$users = User::all();

$user = $users->findOrFail(1);
```

<a name="method-fresh"></a>
#### `fresh($with = [])` {.collection-method}

`fresh` 메서드는 컬렉션 내 각 모델의 새 인스턴스를 데이터베이스에서 새로 조회해 반환합니다. 또한 지정한 관계도 eager load됩니다.

```php
$users = $users->fresh();

$users = $users->fresh('comments');
```

<a name="method-intersect"></a>
#### `intersect($items)` {.collection-method}

`intersect` 메서드는 주어진 컬렉션에 포함되어 있는 모든 모델만 반환합니다.

```php
use App\Models\User;

$users = $users->intersect(User::whereIn('id', [1, 2, 3])->get());
```

<a name="method-load"></a>
#### `load($relations)` {.collection-method}

`load` 메서드는 컬렉션 내 모든 모델에 대해 지정한 관계를 eager load합니다.

```php
$users->load(['comments', 'posts']);

$users->load('comments.author');

$users->load(['comments', 'posts' => fn ($query) => $query->where('active', 1)]);
```

<a name="method-loadMissing"></a>
#### `loadMissing($relations)` {.collection-method}

`loadMissing` 메서드는 컬렉션 내 모든 모델에 대해, 아직 로드되지 않은 관계만 eager load합니다.

```php
$users->loadMissing(['comments', 'posts']);

$users->loadMissing('comments.author');

$users->loadMissing(['comments', 'posts' => fn ($query) => $query->where('active', 1)]);
```

<a name="method-modelKeys"></a>
#### `modelKeys()` {.collection-method}

`modelKeys` 메서드는 컬렉션 내 모든 모델의 기본키를 배열로 반환합니다.

```php
$users->modelKeys();

// [1, 2, 3, 4, 5]
```

<a name="method-makeVisible"></a>
#### `makeVisible($attributes)` {.collection-method}

`makeVisible` 메서드는 컬렉션에 포함된 각 모델에서 일반적으로 "숨겨진" 속성을 [노출](/docs/{{version}}/eloquent-serialization#hiding-attributes-from-json)하도록 변경합니다.

```php
$users = $users->makeVisible(['address', 'phone_number']);
```

<a name="method-makeHidden"></a>
#### `makeHidden($attributes)` {.collection-method}

`makeHidden` 메서드는 컬렉션에 포함된 각 모델에서 일반적으로 "노출"되는 속성을 [숨기도록](/docs/{{version}}/eloquent-serialization#hiding-attributes-from-json) 변경합니다.

```php
$users = $users->makeHidden(['address', 'phone_number']);
```

<a name="method-only"></a>
#### `only($keys)` {.collection-method}

`only` 메서드는 지정한 기본키를 가진 모델만 반환합니다.

```php
$users = $users->only([1, 2, 3]);
```

<a name="method-setVisible"></a>
#### `setVisible($attributes)` {.collection-method}

`setVisible` 메서드는 컬렉션 내 각 모델의 노출 속성을 [일시적으로 덮어씁니다](/docs/{{version}}/eloquent-serialization#temporarily-modifying-attribute-visibility).

```php
$users = $users->setVisible(['id', 'name']);
```

<a name="method-setHidden"></a>
#### `setHidden($attributes)` {.collection-method}

`setHidden` 메서드는 컬렉션 내 각 모델의 숨긴 속성을 [일시적으로 덮어씁니다](/docs/{{version}}/eloquent-serialization#temporarily-modifying-attribute-visibility).

```php
$users = $users->setHidden(['email', 'password', 'remember_token']);
```

<a name="method-toquery"></a>
#### `toQuery()` {.collection-method}

`toQuery` 메서드는 컬렉션 모델의 기본키에 `whereIn` 제약조건이 걸린 Eloquent 쿼리 빌더 인스턴스를 반환합니다.

```php
use App\Models\User;

$users = User::where('status', 'VIP')->get();

$users->toQuery()->update([
    'status' => 'Administrator',
]);
```

<a name="method-unique"></a>
#### `unique($key = null, $strict = false)` {.collection-method}

`unique` 메서드는 컬렉션 내에서 고유한 모델만 반환합니다. 컬렉션 내 다른 모델과 기본키가 같은 모델은 제거됩니다.

```php
$users = $users->unique();
```

<a name="custom-collections"></a>
## 커스텀 컬렉션

특정 모델에서 사용자 정의 `Collection` 객체를 사용하고 싶다면, 모델에 `CollectedBy` 특성을 추가할 수 있습니다.

```php
<?php

namespace App\Models;

use App\Support\UserCollection;
use Illuminate\Database\Eloquent\Attributes\CollectedBy;
use Illuminate\Database\Eloquent\Model;

#[CollectedBy(UserCollection::class)]
class User extends Model
{
    // ...
}
```

또는, 모델에서 `newCollection` 메서드를 정의할 수도 있습니다.

```php
<?php

namespace App\Models;

use App\Support\UserCollection;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 새로운 Eloquent Collection 인스턴스를 생성합니다.
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

`newCollection` 메서드를 정의하거나 `CollectedBy` 특성을 모델에 추가했다면, Eloquent가 보통 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환하는 모든 곳에서 사용자 정의 컬렉션 인스턴스를 받게 됩니다.

애플리케이션의 모든 모델에서 사용자 정의 컬렉션을 사용하려면, 모든 모델이 상속하는 기본 모델 클래스에 `newCollection` 메서드를 정의해야 합니다.
