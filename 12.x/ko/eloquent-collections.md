# Eloquent: 컬렉션 (Eloquent: Collections)

- [소개](#introduction)
- [사용 가능한 메서드](#available-methods)
- [커스텀 컬렉션](#custom-collections)

<a name="introduction"></a>
## 소개

여러 개의 모델 결과를 반환하는 모든 Eloquent 메서드는 `Illuminate\Database\Eloquent\Collection` 클래스의 인스턴스를 반환합니다. 이는 `get` 메서드를 통해 조회한 결과나 연관관계를 통해 접근한 결과도 포함됩니다. Eloquent 컬렉션 객체는 Laravel의 [기본 컬렉션](/docs/12.x/collections)을 확장하므로, 내부적으로 Eloquent 모델 배열을 유연하게 다루기 위한 수십 개의 메서드를 자연스럽게 상속받습니다. 이러한 유용한 메서드들에 대해 더 자세히 알아보고 싶다면, 반드시 Laravel 컬렉션 문서를 참고하시기 바랍니다!

모든 컬렉션은 반복자(iterator) 역할도 하므로, 마치 PHP의 배열처럼 반복문을 통해 순회할 수 있습니다:

```php
use App\Models\User;

$users = User::where('active', 1)->get();

foreach ($users as $user) {
    echo $user->name;
}
```

하지만 앞서 언급했듯이, 컬렉션은 배열보다 훨씬 더 강력하며, 직관적인 인터페이스를 사용해 다양한 map/reduce 연산을 체이닝(메서드 연쇄 호출) 형태로 지원합니다. 예를 들어, 비활성화된 모델을 모두 제외하고 남은 사용자들의 이름만을 수집할 수 있습니다:

```php
$names = User::all()->reject(function (User $user) {
    return $user->active === false;
})->map(function (User $user) {
    return $user->name;
});
```

<a name="eloquent-collection-conversion"></a>
#### Eloquent 컬렉션 변환

대부분의 Eloquent 컬렉션 메서드는 새로운 Eloquent 컬렉션 인스턴스를 반환하지만, `collapse`, `flatten`, `flip`, `keys`, `pluck`, `zip` 메서드는 [기본 컬렉션](/docs/12.x/collections) 인스턴스를 반환합니다. 또한, `map` 연산이 Eloquent 모델이 아닌 컬렉션을 반환하는 경우에도, 해당 결과는 기본 컬렉션 인스턴스로 변환됩니다.

<a name="available-methods"></a>
## 사용 가능한 메서드

모든 Eloquent 컬렉션은 기본 [Laravel 컬렉션](/docs/12.x/collections#available-methods) 객체를 확장하므로, 기본 컬렉션 클래스가 제공하는 강력한 메서드를 모두 사용할 수 있습니다.

추가로, `Illuminate\Database\Eloquent\Collection` 클래스는 모델 컬렉션을 효과적으로 관리할 수 있도록 다양한 메서드를 확장 제공하고 있습니다. 대부분의 메서드는 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환하지만, `modelKeys`와 같은 일부 메서드는 `Illuminate\Support\Collection` 인스턴스를 반환합니다.

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
[mergeVisible](#method-mergeVisible)
[mergeHidden](#method-mergeHidden)
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

`append` 메서드는 컬렉션 내의 모든 모델에 대해 [속성 추가](/docs/12.x/eloquent-serialization#appending-values-to-json) 처리를 할 수 있도록 해줍니다. 이 메서드는 하나의 속성 혹은 속성 배열을 인수로 받을 수 있습니다:

```php
$users->append('team');

$users->append(['team', 'is_admin']);
```

<a name="method-contains"></a>
#### `contains($key, $operator = null, $value = null)`

`contains` 메서드는 컬렉션에 특정 모델 인스턴스가 포함되어 있는지 확인할 때 사용합니다. 이 메서드는 기본 키(primary key) 값이나 모델 인스턴스를 인수로 받을 수 있습니다:

```php
$users->contains(1);

$users->contains(User::find(1));
```

<a name="method-diff"></a>
#### `diff($items)`

`diff` 메서드는 주어진 컬렉션에 존재하지 않는 모델들만 반환합니다:

```php
use App\Models\User;

$users = $users->diff(User::whereIn('id', [1, 2, 3])->get());
```

<a name="method-except"></a>
#### `except($keys)`

`except` 메서드는 지정된 기본 키(primary key)를 가진 모델을 제외한 모든 모델을 반환합니다:

```php
$users = $users->except([1, 2, 3]);
```

<a name="method-find"></a>
#### `find($key)`

`find` 메서드는 주어진 기본 키와 일치하는 모델을 반환합니다. `$key`에 모델 인스턴스를 전달하면 해당 인스턴스의 기본 키에 일치하는 모델을 반환하며, 배열을 전달하면 배열 내의 기본 키에 해당하는 모든 모델을 반환합니다:

```php
$users = User::all();

$user = $users->find(1);
```

<a name="method-find-or-fail"></a>
#### `findOrFail($key)`

`findOrFail` 메서드는 주어진 기본 키와 일치하는 모델을 반환하거나, 컬렉션 내에 해당 모델이 존재하지 않을 경우 `Illuminate\Database\Eloquent\ModelNotFoundException` 예외를 발생시킵니다:

```php
$users = User::all();

$user = $users->findOrFail(1);
```

<a name="method-fresh"></a>
#### `fresh($with = [])`

`fresh` 메서드는 컬렉션 내의 각 모델에 대해 데이터베이스로부터 새 인스턴스를 조회합니다. 또한, 지정한 연관관계도 함께 eager load됩니다:

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

`load` 메서드는 컬렉션 내의 모든 모델에 대해 지정된 연관관계를 eager load합니다:

```php
$users->load(['comments', 'posts']);

$users->load('comments.author');

$users->load(['comments', 'posts' => fn ($query) => $query->where('active', 1)]);
```

<a name="method-loadMissing"></a>
#### `loadMissing($relations)`

`loadMissing` 메서드는 컬렉션 내의 모든 모델에 대해, 아직 로드되지 않은 지정된 연관관계만 eager load합니다:

```php
$users->loadMissing(['comments', 'posts']);

$users->loadMissing('comments.author');

$users->loadMissing(['comments', 'posts' => fn ($query) => $query->where('active', 1)]);
```

<a name="method-modelKeys"></a>
#### `modelKeys()`

`modelKeys` 메서드는 컬렉션 내 모든 모델의 기본 키 배열을 반환합니다:

```php
$users->modelKeys();

// [1, 2, 3, 4, 5]
```

<a name="method-makeVisible"></a>
#### `makeVisible($attributes)`

`makeVisible` 메서드는 컬렉션 내의 각 모델에서 일반적으로 "숨김" 처리된 [속성들을 노출](/docs/12.x/eloquent-serialization#hiding-attributes-from-json)시킵니다:

```php
$users = $users->makeVisible(['address', 'phone_number']);
```

<a name="method-makeHidden"></a>
#### `makeHidden($attributes)`

`makeHidden` 메서드는 컬렉션 내의 각 모델에서 일반적으로 "노출"되는 [속성들을 숨김](/docs/12.x/eloquent-serialization#hiding-attributes-from-json) 처리합니다:

```php
$users = $users->makeHidden(['address', 'phone_number']);
```

<a name="method-mergeVisible"></a>
#### `mergeVisible($attributes)`

`mergeVisible` 메서드는 기존에 노출된 속성들을 유지하면서 [추가로 속성을 노출](/docs/12.x/eloquent-serialization#hiding-attributes-from-json)시킵니다:

```php
$users = $users->mergeVisible(['middle_name']);
```

<a name="method-mergeHidden"></a>
#### `mergeHidden($attributes)`

`mergeHidden` 메서드는 기존에 숨김 처리된 속성들을 유지하면서, [추가로 속성을 숨김](/docs/12.x/eloquent-serialization#hiding-attributes-from-json) 처리합니다:

```php
$users = $users->mergeHidden(['last_login_at']);
```

<a name="method-only"></a>
#### `only($keys)`

`only` 메서드는 지정한 기본 키들에 해당하는 모델들만 반환합니다:

```php
$users = $users->only([1, 2, 3]);
```

<a name="method-partition"></a>
#### `partition`

`partition` 메서드는 `Illuminate\Support\Collection` 인스턴스를 반환하며, 여기에는 조건에 따라 나뉜 두 개의 `Illuminate\Database\Eloquent\Collection` 인스턴스가 담깁니다:

```php
$partition = $users->partition(fn ($user) => $user->age > 18);

dump($partition::class);    // Illuminate\Support\Collection
dump($partition[0]::class); // Illuminate\Database\Eloquent\Collection
dump($partition[1]::class); // Illuminate\Database\Eloquent\Collection
```

<a name="method-setAppends"></a>
#### `setAppends($attributes)`

`setAppends` 메서드는 컬렉션 내의 각 모델에 대해 [추가되는 속성](/docs/12.x/eloquent-serialization#appending-values-to-json)들을 임시로 재정의합니다:

```php
$users = $users->setAppends(['is_admin']);
```

<a name="method-setVisible"></a>
#### `setVisible($attributes)`

`setVisible` 메서드는 컬렉션 내의 각 모델에 대해 노출되는 모든 속성을 [임시로 재정의](/docs/12.x/eloquent-serialization#temporarily-modifying-attribute-visibility)합니다:

```php
$users = $users->setVisible(['id', 'name']);
```

<a name="method-setHidden"></a>
#### `setHidden($attributes)`

`setHidden` 메서드는 컬렉션 내의 각 모델에 대해 숨겨지는 모든 속성을 [임시로 재정의](/docs/12.x/eloquent-serialization#temporarily-modifying-attribute-visibility)합니다:

```php
$users = $users->setHidden(['email', 'password', 'remember_token']);
```

<a name="method-toquery"></a>
#### `toQuery()`

`toQuery` 메서드는 컬렉션 내 모델의 기본 키에 기반하여 `whereIn` 조건이 적용된 Eloquent 쿼리 빌더 인스턴스를 반환합니다:

```php
use App\Models\User;

$users = User::where('status', 'VIP')->get();

$users->toQuery()->update([
    'status' => 'Administrator',
]);
```

<a name="method-unique"></a>
#### `unique($key = null, $strict = false)`

`unique` 메서드는 컬렉션 내에서 중복된 기본 키를 가진 모델을 제거하고, 고유한 모델만 모두 반환합니다:

```php
$users = $users->unique();
```

<a name="method-withoutAppends"></a>
#### `withoutAppends($attributes)`

`withoutAppends` 메서드는 컬렉션 내의 각 모델에 대해 [추가된 속성](/docs/12.x/eloquent-serialization#appending-values-to-json)을 임시로 모두 제거합니다:

```php
$users = $users->withoutAppends();
```

<a name="custom-collections"></a>
## 커스텀 컬렉션

특정 모델과 연동할 때 사용자 정의(`custom`) `Collection` 객체를 사용하고 싶다면, 모델에 `CollectedBy` 속성(Attribute)을 추가할 수 있습니다:

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

또는, 모델에서 `newCollection` 메서드를 정의할 수도 있습니다:

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
        $collection = new UserCollection($models);

        if (Model::isAutomaticallyEagerLoadingRelationships()) {
            $collection->withRelationshipAutoloading();
        }

        return $collection;
    }
}
```

이렇게 `newCollection` 메서드를 정의하거나 `CollectedBy` 속성을 추가하면, Eloquent가 일반적으로 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환하는 모든 상황에서, 항상 커스텀 컬렉션 인스턴스를 반환하게 됩니다.

애플리케이션 내 모든 모델에 대해 커스텀 컬렉션을 적용하고 싶다면, 공통으로 상속받는 베이스 모델에 `newCollection` 메서드를 정의하면 됩니다.
