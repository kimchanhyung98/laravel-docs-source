# Eloquent: 컬렉션 (Eloquent: Collections)

- [소개](#introduction)
- [사용 가능한 메서드](#available-methods)
- [커스텀 컬렉션](#custom-collections)

<a name="introduction"></a>
## 소개

여러 모델 결과를 반환하는 모든 Eloquent 메서드는 `Illuminate\Database\Eloquent\Collection` 클래스의 인스턴스를 반환합니다. 여기에는 `get` 메서드를 통해 조회된 결과나 관계를 통해 접근한 결과가 포함됩니다. Eloquent 컬렉션 객체는 Laravel의 [기본 컬렉션](/docs/12.x/collections)을 확장하므로, Eloquent 모델 배열을 유연하게 다룰 수 있는 수십 가지 메서드를 자연스럽게 상속받습니다. 이 유용한 메서드들에 대해 배우려면 반드시 Laravel 컬렉션 문서를 확인하세요!

또한 모든 컬렉션은 반복자(iterator) 역할을 하므로, 단순 PHP 배열처럼 컬렉션을 순회할 수 있습니다:

```php
use App\Models\User;

$users = User::where('active', 1)->get();

foreach ($users as $user) {
    echo $user->name;
}
```

하지만 앞서 언급했듯이, 컬렉션은 배열보다 훨씬 더 강력하며, 직관적인 인터페이스로 체이닝 가능한 다양한 map / reduce 연산을 제공합니다. 예를 들어, 비활성 사용자 모델을 모두 제거한 후 남아 있는 사용자 각각의 이름만 모을 수도 있습니다:

```php
$names = User::all()->reject(function (User $user) {
    return $user->active === false;
})->map(function (User $user) {
    return $user->name;
});
```

<a name="eloquent-collection-conversion"></a>
#### Eloquent 컬렉션 변환

대부분의 Eloquent 컬렉션 메서드는 Eloquent 컬렉션의 새 인스턴스를 반환하지만, `collapse`, `flatten`, `flip`, `keys`, `pluck`, `zip` 메서드는 [기본 컬렉션](/docs/12.x/collections) 인스턴스를 반환합니다. 또한 `map` 연산이 Eloquent 모델을 포함하지 않는 컬렉션을 반환하면, 기본 컬렉션 인스턴스로 변환됩니다.

<a name="available-methods"></a>
## 사용 가능한 메서드

모든 Eloquent 컬렉션은 기본 [Laravel 컬렉션](/docs/12.x/collections#available-methods) 객체를 확장하므로, 기본 컬렉션 클래스가 제공하는 강력한 메서드를 모두 상속받습니다.

추가로, `Illuminate\Database\Eloquent\Collection` 클래스는 모델 컬렉션 관리를 돕는 확장된 메서드들을 제공합니다. 대부분의 메서드는 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환하지만, `modelKeys` 같은 일부 메서드는 `Illuminate\Support\Collection` 인스턴스를 반환합니다.

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
#### `append($attributes)`

`append` 메서드는 컬렉션 내 모든 모델에 대해 특정 속성(attribute)을 [추가(appended)](/docs/12.x/eloquent-serialization#appending-values-to-json)하고자 할 때 사용합니다. 배열 형태 또는 단일 속성명도 받을 수 있습니다:

```php
$users->append('team');

$users->append(['team', 'is_admin']);
```

<a name="method-contains"></a>
#### `contains($key, $operator = null, $value = null)`

`contains` 메서드는 특정 모델 인스턴스가 컬렉션에 포함되어 있는지 확인할 때 사용합니다. 기본 키나 모델 인스턴스를 인수로 받을 수 있습니다:

```php
$users->contains(1);

$users->contains(User::find(1));
```

<a name="method-diff"></a>
#### `diff($items)`

`diff` 메서드는 주어진 컬렉션에 없는 모델들만 반환합니다:

```php
use App\Models\User;

$users = $users->diff(User::whereIn('id', [1, 2, 3])->get());
```

<a name="method-except"></a>
#### `except($keys)`

`except` 메서드는 지정한 기본 키(primary key)를 갖지 않은 모델들만 반환합니다:

```php
$users = $users->except([1, 2, 3]);
```

<a name="method-find"></a>
#### `find($key)`

`find` 메서드는 지정된 기본 키와 일치하는 모델을 반환합니다. 만약 `$key`가 배열인 경우, 해당 키들에 맞는 모든 모델을 반환합니다. 만약 `$key`가 모델 인스턴스라면 해당 모델의 기본 키를 기준으로 결과를 반환합니다:

```php
$users = User::all();

$user = $users->find(1);
```

<a name="method-find-or-fail"></a>
#### `findOrFail($key)`

`findOrFail` 메서드는 지정한 기본 키와 일치하는 모델을 반환하거나, 컬렉션 내에 해당 모델이 없으면 `Illuminate\Database\Eloquent\ModelNotFoundException` 예외를 던집니다:

```php
$users = User::all();

$user = $users->findOrFail(1);
```

<a name="method-fresh"></a>
#### `fresh($with = [])`

`fresh` 메서드는 컬렉션 내 각 모델의 새 인스턴스를 DB에서 다시 조회합니다. 추가로, 지정한 관계들도 지연 로딩 없이 즉시 로딩(eager loading)합니다:

```php
$users = $users->fresh();

$users = $users->fresh('comments');
```

<a name="method-intersect"></a>
#### `intersect($items)`

`intersect` 메서드는 주어진 컬렉션에도 존재하는 모델들만 반환합니다:

```php
use App\Models\User;

$users = $users->intersect(User::whereIn('id', [1, 2, 3])->get());
```

<a name="method-load"></a>
#### `load($relations)`

`load` 메서드는 컬렉션 내 모든 모델에 대해 지정한 관계들을 즉시 로딩(eager load)합니다:

```php
$users->load(['comments', 'posts']);

$users->load('comments.author');

$users->load(['comments', 'posts' => fn ($query) => $query->where('active', 1)]);
```

<a name="method-loadMissing"></a>
#### `loadMissing($relations)`

`loadMissing` 메서드는 컬렉션 내 모델에 해당 관계들이 아직 로드되지 않은 경우에만 즉시 로딩합니다:

```php
$users->loadMissing(['comments', 'posts']);

$users->loadMissing('comments.author');

$users->loadMissing(['comments', 'posts' => fn ($query) => $query->where('active', 1)]);
```

<a name="method-modelKeys"></a>
#### `modelKeys()`

`modelKeys` 메서드는 컬렉션 내 모든 모델의 기본 키 목록을 반환합니다:

```php
$users->modelKeys();

// [1, 2, 3, 4, 5]
```

<a name="method-makeVisible"></a>
#### `makeVisible($attributes)`

`makeVisible` 메서드는 컬렉션 내 각 모델에서 기본적으로 "숨겨진" 속성들을 [보이도록](/docs/12.x/eloquent-serialization#hiding-attributes-from-json) 만듭니다:

```php
$users = $users->makeVisible(['address', 'phone_number']);
```

<a name="method-makeHidden"></a>
#### `makeHidden($attributes)`

`makeHidden` 메서드는 컬렉션 내 각 모델에서 기본적으로 "보이는" 속성들을 [숨깁니다](/docs/12.x/eloquent-serialization#hiding-attributes-from-json):

```php
$users = $users->makeHidden(['address', 'phone_number']);
```

<a name="method-only"></a>
#### `only($keys)`

`only` 메서드는 주어진 기본 키를 가진 모델만 반환합니다:

```php
$users = $users->only([1, 2, 3]);
```

<a name="method-partition"></a>
#### `partition`

`partition` 메서드는 `Illuminate\Support\Collection` 인스턴스를 반환하며, 이 컬렉션은 `Illuminate\Database\Eloquent\Collection` 인스턴스들을 포함합니다:

```php
$partition = $users->partition(fn ($user) => $user->age > 18);

dump($partition::class);    // Illuminate\Support\Collection
dump($partition[0]::class); // Illuminate\Database\Eloquent\Collection
dump($partition[1]::class); // Illuminate\Database\Eloquent\Collection
```

<a name="method-setVisible"></a>
#### `setVisible($attributes)`

`setVisible` 메서드는 컬렉션 내 모든 모델에서 보이는 속성을 [일시적으로 재정의](/docs/12.x/eloquent-serialization#temporarily-modifying-attribute-visibility)합니다:

```php
$users = $users->setVisible(['id', 'name']);
```

<a name="method-setHidden"></a>
#### `setHidden($attributes)`

`setHidden` 메서드는 컬렉션 내 모든 모델에서 숨겨진 속성을 [일시적으로 재정의](/docs/12.x/eloquent-serialization#temporarily-modifying-attribute-visibility)합니다:

```php
$users = $users->setHidden(['email', 'password', 'remember_token']);
```

<a name="method-toquery"></a>
#### `toQuery()`

`toQuery` 메서드는 컬렉션 모델들의 기본 키를 기준으로 `whereIn` 조건이 포함된 Eloquent 쿼리 빌더 인스턴스를 반환합니다:

```php
use App\Models\User;

$users = User::where('status', 'VIP')->get();

$users->toQuery()->update([
    'status' => 'Administrator',
]);
```

<a name="method-unique"></a>
#### `unique($key = null, $strict = false)`

`unique` 메서드는 컬렉션 내 고유한 모델만 반환합니다. 기본 키가 같은 모델은 중복 제거됩니다:

```php
$users = $users->unique();
```

<a name="custom-collections"></a>
## 커스텀 컬렉션

특정 모델과 상호작용할 때 커스텀 `Collection` 객체를 사용하려면, 모델에 `CollectedBy` 애트리뷰트를 추가할 수 있습니다:

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

또는 모델에 `newCollection` 메서드를 정의하는 방법도 있습니다:

```php
<?php

namespace App\Models;

use App\Support\UserCollection;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 새로운 Eloquent 컬렉션 인스턴스를 생성합니다.
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

`newCollection` 메서드 또는 `CollectedBy` 애트리뷰트를 정의하면, Eloquent가 원래 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환하는 모든 경우에 커스텀 컬렉션 인스턴스를 반환합니다.

애플리케이션 내 모든 모델에 대해 커스텀 컬렉션을 사용하려면, 모든 모델이 상속하는 기본 모델 클래스에서 `newCollection` 메서드를 정의하면 됩니다.