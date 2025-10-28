# Eloquent: 컬렉션 (Eloquent: Collections)

- [소개](#introduction)
- [사용 가능한 메서드](#available-methods)
- [커스텀 컬렉션](#custom-collections)

<a name="introduction"></a>
## 소개

여러 개의 모델 결과값을 반환하는 모든 Eloquent 메서드는 `Illuminate\Database\Eloquent\Collection` 클래스의 인스턴스를 반환합니다. 여기에는 `get` 메서드를 통해 조회된 결과나 연관관계(relationships)를 통해 접근한 결과가 모두 포함됩니다. Eloquent 컬렉션 객체는 Laravel의 [기본 컬렉션](/docs/12.x/collections)을 확장하므로, Eloquent 모델들의 내부 배열을 다루는 다양한 메서드들을 자연스럽게 상속받아 유연하게 사용할 수 있습니다. 유용한 이 메서드들에 대해 더 자세히 알아보고 싶다면 Laravel 컬렉션 문서를 반드시 참고하시기 바랍니다.

모든 컬렉션은 또한 이터레이터 역할도 하므로, 일반 PHP 배열처럼 반복문을 사용할 수 있습니다:

```php
use App\Models\User;

$users = User::where('active', 1)->get();

foreach ($users as $user) {
    echo $user->name;
}
```

그러나 앞서 언급한 것처럼, 컬렉션은 배열보다 훨씬 강력하며 다양한 map / reduce 연산을 직관적인 인터페이스로 체이닝(연결)하여 사용할 수 있습니다. 예를 들어 비활성화된 모델을 모두 제거한 뒤, 남은 사용자 각각의 이름만 모아올 수도 있습니다:

```php
$names = User::all()->reject(function (User $user) {
    return $user->active === false;
})->map(function (User $user) {
    return $user->name;
});
```

<a name="eloquent-collection-conversion"></a>
#### Eloquent 컬렉션 변환

대부분의 Eloquent 컬렉션 메서드는 새로운 Eloquent 컬렉션 인스턴스를 반환하지만, `collapse`, `flatten`, `flip`, `keys`, `pluck`, `zip` 메서드는 [기본 컬렉션](/docs/12.x/collections) 인스턴스를 반환합니다. 마찬가지로, `map` 연산에서 반환되는 컬렉션이 Eloquent 모델을 포함하지 않는 경우, 해당 컬렉션은 기본 컬렉션 인스턴스로 변환됩니다.

<a name="available-methods"></a>
## 사용 가능한 메서드

모든 Eloquent 컬렉션은 [Laravel 기본 컬렉션](/docs/12.x/collections#available-methods) 객체를 확장하므로, 기본 컬렉션 클래스가 제공하는 다양한 강력한 메서드를 모두 사용할 수 있습니다.

뿐만 아니라 `Illuminate\Database\Eloquent\Collection` 클래스는 모델 컬렉션을 더 효과적으로 관리할 수 있도록 도와주는 추가적인 메서드들을 제공합니다. 대부분의 메서드는 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환하지만, `modelKeys`와 같은 일부 메서드는 `Illuminate\Support\Collection` 인스턴스를 반환합니다.

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
[setAppends](#method-setAppends)
[setVisible](#method-setVisible)
[setHidden](#method-setHidden)
[toQuery](#method-toquery)
[unique](#method-unique)
[withoutAppends](#method-withoutAppends)

</div>

<a name="method-append"></a>
#### `append($attributes)`

`append` 메서드는 컬렉션 내의 각 모델에 [속성을 추가](/docs/12.x/eloquent-serialization#appending-values-to-json)하도록 지정할 때 사용합니다. 이 메서드는 속성명 배열이나 단일 속성명을 인수로 받을 수 있습니다:

```php
$users->append('team');

$users->append(['team', 'is_admin']);
```

<a name="method-contains"></a>
#### `contains($key, $operator = null, $value = null)`

`contains` 메서드는 특정 모델 인스턴스가 컬렉션에 포함되어 있는지 확인합니다. 이 메서드는 기본 키(primary key) 또는 모델 인스턴스를 인수로 받을 수 있습니다:

```php
$users->contains(1);

$users->contains(User::find(1));
```

<a name="method-diff"></a>
#### `diff($items)`

`diff` 메서드는 전달받은 컬렉션에 포함되어 있지 않은 모델만을 반환합니다:

```php
use App\Models\User;

$users = $users->diff(User::whereIn('id', [1, 2, 3])->get());
```

<a name="method-except"></a>
#### `except($keys)`

`except` 메서드는 입력한 기본 키(primary key)를 가진 모델을 제외한 나머지 모델만 반환합니다:

```php
$users = $users->except([1, 2, 3]);
```

<a name="method-find"></a>
#### `find($key)`

`find` 메서드는 주어진 키와 일치하는 기본 키를 가진 모델을 반환합니다. `$key`가 모델 인스턴스일 경우에는 해당 기본 키를 찾으려고 시도합니다. 또한 `$key`가 키의 배열이라면, 해당 배열에 포함된 기본 키를 가진 모든 모델을 반환합니다:

```php
$users = User::all();

$user = $users->find(1);
```

<a name="method-find-or-fail"></a>
#### `findOrFail($key)`

`findOrFail` 메서드는 주어진 키와 일치하는 기본 키를 가진 모델을 반환합니다. 만약 컬렉션에서 해당되는 모델을 찾지 못하면 `Illuminate\Database\Eloquent\ModelNotFoundException` 예외가 발생합니다:

```php
$users = User::all();

$user = $users->findOrFail(1);
```

<a name="method-fresh"></a>
#### `fresh($with = [])`

`fresh` 메서드는 컬렉션에 담긴 각 모델을 데이터베이스에서 최신 상태로 다시 가져옵니다. 추가로, 지정된 연관관계(relationships)가 있다면 이를 즉시 로드(eager load)합니다:

```php
$users = $users->fresh();

$users = $users->fresh('comments');
```

<a name="method-intersect"></a>
#### `intersect($items)`

`intersect` 메서드는 인자로 넘겨준 컬렉션에도 존재하는 모델만 반환합니다:

```php
use App\Models\User;

$users = $users->intersect(User::whereIn('id', [1, 2, 3])->get());
```

<a name="method-load"></a>
#### `load($relations)`

`load` 메서드는 컬렉션 내 모든 모델에 대해 지정한 연관관계를 즉시 로드(eager load)합니다:

```php
$users->load(['comments', 'posts']);

$users->load('comments.author');

$users->load(['comments', 'posts' => fn ($query) => $query->where('active', 1)]);
```

<a name="method-loadMissing"></a>
#### `loadMissing($relations)`

`loadMissing` 메서드는 컬렉션 내 모든 모델에 대해, 해당 연관관계(relationship)가 아직 로드되지 않은 경우에만 즉시 로드합니다:

```php
$users->loadMissing(['comments', 'posts']);

$users->loadMissing('comments.author');

$users->loadMissing(['comments', 'posts' => fn ($query) => $query->where('active', 1)]);
```

<a name="method-modelKeys"></a>
#### `modelKeys()`

`modelKeys` 메서드는 컬렉션 내 모든 모델의 기본 키(primary key) 값을 배열로 반환합니다:

```php
$users->modelKeys();

// [1, 2, 3, 4, 5]
```

<a name="method-makeVisible"></a>
#### `makeVisible($attributes)`

`makeVisible` 메서드는 컬렉션 내 각 모델에서 평소 "숨겨진(hidden)" 상태인 속성을 [보이도록 설정](/docs/12.x/eloquent-serialization#hiding-attributes-from-json)합니다:

```php
$users = $users->makeVisible(['address', 'phone_number']);
```

<a name="method-makeHidden"></a>
#### `makeHidden($attributes)`

`makeHidden` 메서드는 컬렉션 내 각 모델에서 평소 "보이는(visible)" 상태인 속성을 [숨기도록 설정](/docs/12.x/eloquent-serialization#hiding-attributes-from-json)합니다:

```php
$users = $users->makeHidden(['address', 'phone_number']);
```

<a name="method-only"></a>
#### `only($keys)`

`only` 메서드는 입력한 기본 키(primary key)를 가진 모델만 반환합니다:

```php
$users = $users->only([1, 2, 3]);
```

<a name="method-partition"></a>
#### `partition`

`partition` 메서드는 `Illuminate\Support\Collection` 인스턴스를 반환하며, 그 내부에는 두 개의 `Illuminate\Database\Eloquent\Collection` 인스턴스가 담겨 있습니다:

```php
$partition = $users->partition(fn ($user) => $user->age > 18);

dump($partition::class);    // Illuminate\Support\Collection
dump($partition[0]::class); // Illuminate\Database\Eloquent\Collection
dump($partition[1]::class); // Illuminate\Database\Eloquent\Collection
```

<a name="method-setAppends"></a>
#### `setAppends($attributes)`

`setAppends` 메서드는 컬렉션의 모든 모델에서 기존 추가 속성([appended attributes](/docs/12.x/eloquent-serialization#appending-values-to-json))을 임시로 덮어씁니다:

```php
$users = $users->setAppends(['is_admin']);
```

<a name="method-setVisible"></a>
#### `setVisible($attributes)`

`setVisible` 메서드는 컬렉션에 포함된 각 모델의 보이는 속성을 [임시로 재정의](/docs/12.x/eloquent-serialization#temporarily-modifying-attribute-visibility)합니다:

```php
$users = $users->setVisible(['id', 'name']);
```

<a name="method-setHidden"></a>
#### `setHidden($attributes)`

`setHidden` 메서드는 컬렉션 내 각 모델의 숨겨진 속성을 [임시로 재정의](/docs/12.x/eloquent-serialization#temporarily-modifying-attribute-visibility)합니다:

```php
$users = $users->setHidden(['email', 'password', 'remember_token']);
```

<a name="method-toquery"></a>
#### `toQuery()`

`toQuery` 메서드는 해당 컬렉션의 모델 기본 키(primary key)에 `whereIn` 조건이 걸린 Eloquent 쿼리 빌더 인스턴스를 반환합니다:

```php
use App\Models\User;

$users = User::where('status', 'VIP')->get();

$users->toQuery()->update([
    'status' => 'Administrator',
]);
```

<a name="method-unique"></a>
#### `unique($key = null, $strict = false)`

`unique` 메서드는 컬렉션에서 중복되는 기본 키(primary key)를 가진 모델을 제거하고, 유일한 모델만 반환합니다:

```php
$users = $users->unique();
```

<a name="method-withoutAppends"></a>
#### `withoutAppends($attributes)`

`withoutAppends` 메서드는 컬렉션 내 각 모델에서 모든 [추가 속성(appended attributes)](/docs/12.x/eloquent-serialization#appending-values-to-json)을 임시로 제거합니다:

```php
$users = $users->withoutAppends();
```

<a name="custom-collections"></a>
## 커스텀 컬렉션

특정 모델에서 사용자 정의 `Collection` 객체를 사용하고 싶다면, 모델에 `CollectedBy` 속성을 추가하면 됩니다:

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

또는, 모델에 `newCollection` 메서드를 직접 정의할 수도 있습니다:

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
        $collection = new UserCollection($models);

        if (Model::isAutomaticallyEagerLoadingRelationships()) {
            $collection->withRelationshipAutoloading();
        }

        return $collection;
    }
}
```

`newCollection` 메서드를 정의하거나 모델에 `CollectedBy` 속성을 추가한 이후에는, Eloquent가 원래 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환하던 모든 경우에 커스텀 컬렉션 인스턴스를 받을 수 있습니다.

애플리케이션 내 모든 모델에서 공통으로 커스텀 컬렉션을 사용하고 싶다면, 모든 모델이 상속하는 기본 모델 클래스에 `newCollection` 메서드를 정의하면 됩니다.
