# Eloquent: 컬렉션 (Eloquent: Collections)

- [소개](#introduction)
- [사용 가능한 메서드](#available-methods)
- [커스텀 컬렉션](#custom-collections)

<a name="introduction"></a>
## 소개

하나 이상의 모델 결과를 반환하는 모든 Eloquent 메서드는 `get` 메서드를 통해 조회하거나 관계를 통해 접근한 경우를 포함하여 `Illuminate\Database\Eloquent\Collection` 클래스의 인스턴스를 반환합니다. Eloquent 컬렉션 객체는 Laravel의 [기본 컬렉션](/docs/master/collections)을 확장하므로, Eloquent 모델의 기본 배열을 유창하게 다룰 수 있는 수십여 개의 메서드를 자연스럽게 상속받습니다. 이 유용한 메서드들에 대해 모두 알아보려면 Laravel 컬렉션 문서를 꼭 참고하세요!

모든 컬렉션은 이터레이터(iterator) 역할을 하므로, 단순 PHP 배열처럼 반복문을 사용할 수 있습니다:

```php
use App\Models\User;

$users = User::where('active', 1)->get();

foreach ($users as $user) {
    echo $user->name;
}
```

그러나 앞서 언급한 것처럼 컬렉션은 배열보다 훨씬 강력하며, 직관적인 인터페이스로 체이닝할 수 있는 다양한 map / reduce 연산을 제공합니다. 예를 들어, 비활성 모델을 모두 제거하고 남아 있는 각 사용자 이름만 수집할 수 있습니다:

```php
$names = User::all()->reject(function (User $user) {
    return $user->active === false;
})->map(function (User $user) {
    return $user->name;
});
```

<a name="eloquent-collection-conversion"></a>
#### Eloquent 컬렉션 변환

대부분의 Eloquent 컬렉션 메서드는 Eloquent 컬렉션의 새 인스턴스를 반환하지만, `collapse`, `flatten`, `flip`, `keys`, `pluck`, `zip` 메서드는 [기본 컬렉션](/docs/master/collections) 인스턴스를 반환합니다. 마찬가지로, `map` 연산의 결과가 Eloquent 모델을 포함하지 않는 컬렉션일 경우, 기본 컬렉션 인스턴스로 변환됩니다.

<a name="available-methods"></a>
## 사용 가능한 메서드

모든 Eloquent 컬렉션은 기본 [Laravel 컬렉션](/docs/master/collections#available-methods) 객체를 확장하므로, 기본 컬렉션 클래스가 제공하는 강력한 모든 메서드를 상속받습니다.

또한, `Illuminate\Database\Eloquent\Collection` 클래스는 모델 컬렉션 관리를 돕는 여러 추가 메서드를 제공합니다. 대부분의 메서드는 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환하지만, 일부 메서드(예: `modelKeys`)는 `Illuminate\Support\Collection` 인스턴스를 반환합니다.

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
#### `append($attributes)`

`append` 메서드는 컬렉션 내 모든 모델에 대해 특정 속성을 [추가하여 JSON에 포함하도록](/docs/master/eloquent-serialization#appending-values-to-json) 지정할 때 사용합니다. 배열 또는 단일 속성을 인수로 받습니다:

```php
$users->append('team');

$users->append(['team', 'is_admin']);
```

<a name="method-contains"></a>
#### `contains($key, $operator = null, $value = null)`

`contains` 메서드는 주어진 모델 인스턴스가 컬렉션에 포함되어 있는지 확인할 때 사용합니다. 기본 키 또는 모델 인스턴스를 인수로 받습니다:

```php
$users->contains(1);

$users->contains(User::find(1));
```

<a name="method-diff"></a>
#### `diff($items)`

`diff` 메서드는 주어진 컬렉션에 없는 모든 모델을 반환합니다:

```php
use App\Models\User;

$users = $users->diff(User::whereIn('id', [1, 2, 3])->get());
```

<a name="method-except"></a>
#### `except($keys)`

`except` 메서드는 지정된 기본 키를 가지지 않은 모든 모델을 반환합니다:

```php
$users = $users->except([1, 2, 3]);
```

<a name="method-find"></a>
#### `find($key)`

`find` 메서드는 주어진 기본 키와 일치하는 모델을 반환합니다. `$key`가 모델 인스턴스면, 해당 기본 키에 맞는 모델을 반환하려 시도하며, `$key`가 기본 키 배열일 경우에는 배열 안의 모든 키와 일치하는 모델을 반환합니다:

```php
$users = User::all();

$user = $users->find(1);
```

<a name="method-find-or-fail"></a>
#### `findOrFail($key)`

`findOrFail` 메서드는 주어진 기본 키와 일치하는 모델을 반환하거나, 일치하는 모델이 없으면 `Illuminate\Database\Eloquent\ModelNotFoundException` 예외를 던집니다:

```php
$users = User::all();

$user = $users->findOrFail(1);
```

<a name="method-fresh"></a>
#### `fresh($with = [])`

`fresh` 메서드는 컬렉션 내 각 모델의 최신 인스턴스를 데이터베이스에서 다시 조회합니다. 또한 지정된 연관관계를 함께 즉시 로드합니다:

```php
$users = $users->fresh();

$users = $users->fresh('comments');
```

<a name="method-intersect"></a>
#### `intersect($items)`

`intersect` 메서드는 주어진 컬렉션에도 존재하는 모든 모델을 반환합니다:

```php
use App\Models\User;

$users = $users->intersect(User::whereIn('id', [1, 2, 3])->get());
```

<a name="method-load"></a>
#### `load($relations)`

`load` 메서드는 컬렉션 내 모든 모델에 대해 특정 연관관계를 즉시 로드(eager load)합니다:

```php
$users->load(['comments', 'posts']);

$users->load('comments.author');

$users->load(['comments', 'posts' => fn ($query) => $query->where('active', 1)]);
```

<a name="method-loadMissing"></a>
#### `loadMissing($relations)`

`loadMissing` 메서드는 컬렉션 내 모든 모델에서 해당 연관관계가 아직 로드되지 않은 경우에만 즉시 로드합니다:

```php
$users->loadMissing(['comments', 'posts']);

$users->loadMissing('comments.author');

$users->loadMissing(['comments', 'posts' => fn ($query) => $query->where('active', 1)]);
```

<a name="method-modelKeys"></a>
#### `modelKeys()`

`modelKeys` 메서드는 컬렉션 내 모든 모델의 기본 키 값을 반환합니다:

```php
$users->modelKeys();

// [1, 2, 3, 4, 5]
```

<a name="method-makeVisible"></a>
#### `makeVisible($attributes)`

`makeVisible` 메서드는 컬렉션 내 각 모델에서 보통 "숨겨진" 속성을 [보이도록](/docs/master/eloquent-serialization#hiding-attributes-from-json) 만듭니다:

```php
$users = $users->makeVisible(['address', 'phone_number']);
```

<a name="method-makeHidden"></a>
#### `makeHidden($attributes)`

`makeHidden` 메서드는 컬렉션 내 각 모델에서 보통 "보이는" 속성을 [숨깁니다](/docs/master/eloquent-serialization#hiding-attributes-from-json):

```php
$users = $users->makeHidden(['address', 'phone_number']);
```

<a name="method-only"></a>
#### `only($keys)`

`only` 메서드는 지정된 기본 키를 가진 모든 모델을 반환합니다:

```php
$users = $users->only([1, 2, 3]);
```

<a name="method-setVisible"></a>
#### `setVisible($attributes)`

`setVisible` 메서드는 컬렉션 내 각 모델의 모든 보이는 속성을 [임시로 재정의합니다](/docs/master/eloquent-serialization#temporarily-modifying-attribute-visibility):

```php
$users = $users->setVisible(['id', 'name']);
```

<a name="method-setHidden"></a>
#### `setHidden($attributes)`

`setHidden` 메서드는 컬렉션 내 각 모델의 모든 숨겨진 속성을 [임시로 재정의합니다](/docs/master/eloquent-serialization#temporarily-modifying-attribute-visibility):

```php
$users = $users->setHidden(['email', 'password', 'remember_token']);
```

<a name="method-toquery"></a>
#### `toQuery()`

`toQuery` 메서드는 컬렉션 모델의 기본 키에 `whereIn` 조건이 포함된 Eloquent 쿼리 빌더 인스턴스를 반환합니다:

```php
use App\Models\User;

$users = User::where('status', 'VIP')->get();

$users->toQuery()->update([
    'status' => 'Administrator',
]);
```

<a name="method-unique"></a>
#### `unique($key = null, $strict = false)`

`unique` 메서드는 컬렉션 내 고유한 모델만 반환합니다. 기본 키가 같은 모델은 제거됩니다:

```php
$users = $users->unique();
```

<a name="custom-collections"></a>
## 커스텀 컬렉션

특정 모델과 상호작용할 때 커스텀 `Collection` 객체를 사용하고 싶다면, 모델에 `CollectedBy` 속성을 추가할 수 있습니다:

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

또는, 모델에 `newCollection` 메서드를 정의할 수도 있습니다:

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

모델에 `newCollection` 메서드를 정의하거나 `CollectedBy` 속성을 추가하면, Eloquent가 기본적으로 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환할 때마다 여러분의 커스텀 컬렉션 인스턴스를 받습니다.

애플리케이션 내 모든 모델에 대해 커스텀 컬렉션을 사용하려면, 모든 모델이 상속하는 베이스 모델 클래스에 `newCollection` 메서드를 정의하는 것이 좋습니다.