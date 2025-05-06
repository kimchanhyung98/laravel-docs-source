# Eloquent: 컬렉션

- [소개](#introduction)
- [사용 가능한 메서드](#available-methods)
- [커스텀 컬렉션](#custom-collections)

<a name="introduction"></a>
## 소개

하나 이상의 모델 결과를 반환하는 모든 Eloquent 메서드는 `Illuminate\Database\Eloquent\Collection` 클래스의 인스턴스를 반환합니다. 여기에는 `get` 메서드를 통해 조회된 결과나 관계를 통해 접근한 결과가 포함됩니다. Eloquent 컬렉션 객체는 Laravel의 [기본 컬렉션](/docs/{{version}}/collections)을 확장하므로, Eloquent 모델의 배열을 유연하게 다룰 수 있는 다양한 메서드를 자연스럽게 상속받습니다. 유용한 컬렉션 메서드에 대해 더 알아보려면 Laravel 컬렉션 관련 문서를 확인하세요!

모든 컬렉션은 이터레이터(iterators)의 역할도 하므로, 간단한 PHP 배열처럼 반복문으로 순회할 수 있습니다:

```php
use App\Models\User;

$users = User::where('active', 1)->get();

foreach ($users as $user) {
    echo $user->name;
}
```

하지만 앞서 언급했듯이, 컬렉션은 배열보다 훨씬 강력하며, 직관적인 인터페이스로 체이닝할 수 있는 다양한 map/reduce 연산을 제공합니다. 예를 들어, 모든 비활성화된 모델을 제거한 다음 남은 사용자 각각의 이름만 모을 수 있습니다:

```php
$names = User::all()->reject(function (User $user) {
    return $user->active === false;
})->map(function (User $user) {
    return $user->name;
});
```

<a name="eloquent-collection-conversion"></a>
#### Eloquent 컬렉션 변환

대부분의 Eloquent 컬렉션 메서드는 새로운 Eloquent 컬렉션 인스턴스를 반환하지만, `collapse`, `flatten`, `flip`, `keys`, `pluck`, `zip` 메서드는 [기본 컬렉션](/docs/{{version}}/collections) 인스턴스를 반환합니다. 마찬가지로, `map` 연산의 결과가 더 이상 Eloquent 모델을 포함하지 않을 경우 기본 컬렉션 인스턴스로 변환됩니다.

<a name="available-methods"></a>
## 사용 가능한 메서드

모든 Eloquent 컬렉션은 [Laravel 기본 컬렉션](/docs/{{version}}/collections#available-methods) 객체를 확장하므로, 기본 컬렉션 클래스가 제공하는 강력한 메서드를 모두 상속받습니다.

또한 `Illuminate\Database\Eloquent\Collection` 클래스는 모델 컬렉션을 관리하는 데 도움이 되는 추가 메서드를 제공합니다. 대부분의 메서드는 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환하지만, `modelKeys`와 같은 일부 메서드는 `Illuminate\Support\Collection` 인스턴스를 반환합니다.

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
[partition](#method-partition)
[setVisible](#method-setVisible)
[setHidden](#method-setHidden)
[toQuery](#method-toquery)
[unique](#method-unique)

</div>

<a name="method-append"></a>
#### `append($attributes)` {.collection-method .first-collection-method}

`append` 메서드는 컬렉션 내 모든 모델에 대해 속성이 [추가](/docs/{{version}}/eloquent-serialization#appending-values-to-json)되어야 함을 명시할 때 사용합니다. 이 메서드는 속성의 배열이나 단일 속성을 인수로 받을 수 있습니다:

```php
$users->append('team');

$users->append(['team', 'is_admin']);
```

<a name="method-contains"></a>
#### `contains($key, $operator = null, $value = null)` {.collection-method}

`contains` 메서드는 특정 모델 인스턴스가 컬렉션에 포함되어 있는지를 확인할 때 사용합니다. 이 메서드는 기본 키 또는 모델 인스턴스를 인수로 받을 수 있습니다:

```php
$users->contains(1);

$users->contains(User::find(1));
```

<a name="method-diff"></a>
#### `diff($items)` {.collection-method}

`diff` 메서드는 주어진 컬렉션에 없는 모든 모델을 반환합니다:

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

`find` 메서드는 주어진 기본 키와 일치하는 모델을 반환합니다. `$key`가 모델 인스턴스인 경우, 해당 모델의 기본 키와 일치하는 모델을 반환합니다. `$key`가 기본 키의 배열이면, 해당 배열 속 모든 기본 키와 일치하는 모델들을 반환합니다:

```php
$users = User::all();

$user = $users->find(1);
```

<a name="method-find-or-fail"></a>
#### `findOrFail($key)` {.collection-method}

`findOrFail` 메서드는 주어진 기본 키와 일치하는 모델을 반환하거나, 컬렉션 내에서 일치하는 모델을 찾을 수 없을 경우 `Illuminate\Database\Eloquent\ModelNotFoundException` 예외를 던집니다:

```php
$users = User::all();

$user = $users->findOrFail(1);
```

<a name="method-fresh"></a>
#### `fresh($with = [])` {.collection-method}

`fresh` 메서드는 컬렉션 내 모든 모델을 데이터베이스에서 최신 상태로 다시 조회합니다. 또한 지정된 관계를 eager load 할 수도 있습니다:

```php
$users = $users->fresh();

$users = $users->fresh('comments');
```

<a name="method-intersect"></a>
#### `intersect($items)` {.collection-method}

`intersect` 메서드는 주어진 컬렉션에도 동시에 존재하는 모든 모델을 반환합니다:

```php
use App\Models\User;

$users = $users->intersect(User::whereIn('id', [1, 2, 3])->get());
```

<a name="method-load"></a>
#### `load($relations)` {.collection-method}

`load` 메서드는 컬렉션 내 모든 모델에 대해 주어진 관계를 eager load합니다:

```php
$users->load(['comments', 'posts']);

$users->load('comments.author');

$users->load(['comments', 'posts' => fn ($query) => $query->where('active', 1)]);
```

<a name="method-loadMissing"></a>
#### `loadMissing($relations)` {.collection-method}

`loadMissing` 메서드는 컬렉션 내 모든 모델에서 해당 관계가 이미 로드되어 있지 않다면 해당 관계를 eager load합니다:

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

`makeVisible` 메서드는 컬렉션 내 각 모델에서 일반적으로 "숨겨진" [속성을 표시](/docs/{{version}}/eloquent-serialization#hiding-attributes-from-json)하도록 합니다:

```php
$users = $users->makeVisible(['address', 'phone_number']);
```

<a name="method-makeHidden"></a>
#### `makeHidden($attributes)` {.collection-method}

`makeHidden` 메서드는 컬렉션 내 각 모델에서 일반적으로 "표시되는" [속성을 숨깁니다](/docs/{{version}}/eloquent-serialization#hiding-attributes-from-json):

```php
$users = $users->makeHidden(['address', 'phone_number']);
```

<a name="method-only"></a>
#### `only($keys)` {.collection-method}

`only` 메서드는 주어진 기본 키를 가진 모든 모델을 반환합니다:

```php
$users = $users->only([1, 2, 3]);
```

<a name="method-partition"></a>
#### `partition` {.collection-method}

`partition` 메서드는 `Illuminate\Support\Collection` 인스턴스를 반환하며, 각각이 `Illuminate\Database\Eloquent\Collection` 컬렉션 인스턴스를 포함합니다:

```php
$partition = $users->partition(fn ($user) => $user->age > 18);

dump($partition::class);    // Illuminate\Support\Collection
dump($partition[0]::class); // Illuminate\Database\Eloquent\Collection
dump($partition[1]::class); // Illuminate\Database\Eloquent\Collection
```

<a name="method-setVisible"></a>
#### `setVisible($attributes)` {.collection-method}

`setVisible` 메서드는 컬렉션 내 모든 모델의 표시 속성을 [임시로 재정의](/docs/{{version}}/eloquent-serialization#temporarily-modifying-attribute-visibility)합니다:

```php
$users = $users->setVisible(['id', 'name']);
```

<a name="method-setHidden"></a>
#### `setHidden($attributes)` {.collection-method}

`setHidden` 메서드는 컬렉션 내 모든 모델의 숨김 속성을 [임시로 재정의](/docs/{{version}}/eloquent-serialization#temporarily-modifying-attribute-visibility)합니다:

```php
$users = $users->setHidden(['email', 'password', 'remember_token']);
```

<a name="method-toquery"></a>
#### `toQuery()` {.collection-method}

`toQuery` 메서드는 컬렉션에 포함된 모델의 기본 키에 대해 `whereIn` 조건이 추가된 Eloquent 쿼리 빌더 인스턴스를 반환합니다:

```php
use App\Models\User;

$users = User::where('status', 'VIP')->get();

$users->toQuery()->update([
    'status' => 'Administrator',
]);
```

<a name="method-unique"></a>
#### `unique($key = null, $strict = false)` {.collection-method}

`unique` 메서드는 컬렉션 내에서 고유한 모델만 반환합니다. 동일한 기본 키를 가진 모델이 여러 개 있는 경우 하나만 남기고 제거됩니다:

```php
$users = $users->unique();
```

<a name="custom-collections"></a>
## 커스텀 컬렉션

특정 모델과 상호작용할 때 커스텀 `Collection` 객체를 사용하고 싶다면, 모델에 `CollectedBy` 어트리뷰트를 추가하면 됩니다:

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

또한, 모델에서 `newCollection` 메서드를 정의하여 사용할 수도 있습니다:

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

`newCollection` 메서드를 정의하거나 `CollectedBy` 어트리뷰트를 모델에 추가한 경우, Eloquent가 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환하는 대신 항상 여러분의 커스텀 컬렉션을 반환합니다.

애플리케이션 내 모든 모델에 대해 커스텀 컬렉션을 사용하고 싶다면, 애플리케이션의 모든 모델이 상속받는 기본 모델 클래스에서 `newCollection` 메서드를 정의하면 됩니다.