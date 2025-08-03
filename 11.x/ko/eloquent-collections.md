# Eloquent: 컬렉션 (Eloquent: Collections)

- [소개](#introduction)
- [사용 가능한 메서드](#available-methods)
- [커스텀 컬렉션](#custom-collections)

<a name="introduction"></a>
## 소개

`get` 메서드로 가져오거나 관계를 통해 접근한 결과를 포함하여, 여러 개 이상의 모델 결과를 반환하는 모든 Eloquent 메서드는 `Illuminate\Database\Eloquent\Collection` 클래스의 인스턴스를 반환합니다. Eloquent 컬렉션 객체는 Laravel의 [기본 컬렉션](/docs/11.x/collections)을 상속하므로, 내부의 Eloquent 모델 배열을 편리하게 다룰 수 있는 수십 가지 메서드를 자연스럽게 제공합니다. 이들 유용한 메서드를 자세히 알아보려면 Laravel 컬렉션 문서를 꼭 참고하세요!

모든 컬렉션은 반복자(iterator) 역할도 하기 때문에, 일반적인 PHP 배열처럼 루프를 돌며 사용할 수 있습니다:

```
use App\Models\User;

$users = User::where('active', 1)->get();

foreach ($users as $user) {
    echo $user->name;
}
```

하지만 앞서 언급했듯, 컬렉션은 단순 배열보다 훨씬 더 강력하며, 직관적인 인터페이스를 통해 체인 연결이 가능한 다양한 map/reduce 연산을 지원합니다. 예를 들어, 비활성 모델을 모두 제거하고 남은 사용자 각각의 이름을 수집할 수 있습니다:

```
$names = User::all()->reject(function (User $user) {
    return $user->active === false;
})->map(function (User $user) {
    return $user->name;
});
```

<a name="eloquent-collection-conversion"></a>
#### Eloquent 컬렉션 변환

대부분의 Eloquent 컬렉션 메서드는 새로운 Eloquent 컬렉션 인스턴스를 반환하지만, `collapse`, `flatten`, `flip`, `keys`, `pluck`, `zip` 메서드는 [기본 컬렉션](/docs/11.x/collections) 인스턴스를 반환합니다. 마찬가지로 `map` 작업이 Eloquent 모델을 포함하지 않는 컬렉션을 반환할 경우, 기본 컬렉션 인스턴스로 변환됩니다.

<a name="available-methods"></a>
## 사용 가능한 메서드

모든 Eloquent 컬렉션은 기본 [Laravel 컬렉션](/docs/11.x/collections#available-methods) 객체를 확장하므로, 기본 컬렉션 클래스가 제공하는 강력한 모든 메서드를 상속합니다.

또한 `Illuminate\Database\Eloquent\Collection` 클래스는 모델 컬렉션 관리를 돕기 위해 확장된 메서드 집합도 제공합니다. 대부분의 메서드는 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환하지만, `modelKeys` 같은 일부 메서드는 `Illuminate\Support\Collection` 인스턴스를 반환합니다.

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

`append` 메서드는 컬렉션 내 모든 모델에 대해 특정 속성을 [추가로 포함](/docs/11.x/eloquent-serialization#appending-values-to-json)하도록 지정할 때 사용합니다. 배열 또는 단일 속성을 인수로 받을 수 있습니다:

```
$users->append('team');

$users->append(['team', 'is_admin']);
```

<a name="method-contains"></a>
#### `contains($key, $operator = null, $value = null)`

`contains` 메서드는 주어진 모델 인스턴스가 컬렉션에 포함되어 있는지 확인할 때 사용합니다. 기본 키 값이나 모델 인스턴스를 인수로 받을 수 있습니다:

```
$users->contains(1);

$users->contains(User::find(1));
```

<a name="method-diff"></a>
#### `diff($items)`

`diff` 메서드는 주어진 컬렉션에 포함되지 않은 모든 모델을 반환합니다:

```
use App\Models\User;

$users = $users->diff(User::whereIn('id', [1, 2, 3])->get());
```

<a name="method-except"></a>
#### `except($keys)`

`except` 메서드는 주어진 기본 키를 가지지 않은 모든 모델을 반환합니다:

```
$users = $users->except([1, 2, 3]);
```

<a name="method-find"></a>
#### `find($key)`

`find` 메서드는 주어진 키와 일치하는 기본 키를 가진 모델을 반환합니다. `$key`가 모델 인스턴스일 경우, 해당 인스턴스의 기본 키를 기준으로 모델을 찾습니다. `$key`가 키 배열이면, 배열에 포함된 모든 키를 가진 모델을 반환합니다:

```
$users = User::all();

$user = $users->find(1);
```

<a name="method-find-or-fail"></a>
#### `findOrFail($key)`

`findOrFail` 메서드는 주어진 키와 일치하는 모델을 반환하거나, 컬렉션에서 해당 모델을 찾지 못할 경우 `Illuminate\Database\Eloquent\ModelNotFoundException` 예외를 던집니다:

```
$users = User::all();

$user = $users->findOrFail(1);
```

<a name="method-fresh"></a>
#### `fresh($with = [])`

`fresh` 메서드는 컬렉션에 포함된 각각의 모델을 데이터베이스에서 새로고침합니다. 또한 지정된 관계들도 즉시 로드(eager load)합니다:

```
$users = $users->fresh();

$users = $users->fresh('comments');
```

<a name="method-intersect"></a>
#### `intersect($items)`

`intersect` 메서드는 주어진 컬렉션에도 존재하는 모든 모델을 반환합니다:

```
use App\Models\User;

$users = $users->intersect(User::whereIn('id', [1, 2, 3])->get());
```

<a name="method-load"></a>
#### `load($relations)`

`load` 메서드는 컬렉션 내 모든 모델에 대해 주어진 관계들을 즉시 로드(eager load)합니다:

```
$users->load(['comments', 'posts']);

$users->load('comments.author');

$users->load(['comments', 'posts' => fn ($query) => $query->where('active', 1)]);
```

<a name="method-loadMissing"></a>
#### `loadMissing($relations)`

`loadMissing` 메서드는 컬렉션 내 모든 모델에 대해, 아직 로드되지 않은 경우에만 주어진 관계들을 즉시 로드합니다:

```
$users->loadMissing(['comments', 'posts']);

$users->loadMissing('comments.author');

$users->loadMissing(['comments', 'posts' => fn ($query) => $query->where('active', 1)]);
```

<a name="method-modelKeys"></a>
#### `modelKeys()`

`modelKeys` 메서드는 컬렉션 내 모든 모델의 기본 키 값을 배열로 반환합니다:

```
$users->modelKeys();

// [1, 2, 3, 4, 5]
```

<a name="method-makeVisible"></a>
#### `makeVisible($attributes)`

`makeVisible` 메서드는 일반적으로 각 모델에서 "숨겨진" 상태인 속성을 [보이도록 설정](/docs/11.x/eloquent-serialization#hiding-attributes-from-json)합니다:

```
$users = $users->makeVisible(['address', 'phone_number']);
```

<a name="method-makeHidden"></a>
#### `makeHidden($attributes)`

`makeHidden` 메서드는 일반적으로 각 모델에서 "보이는" 상태인 속성을 [숨김 처리](/docs/11.x/eloquent-serialization#hiding-attributes-from-json)합니다:

```
$users = $users->makeHidden(['address', 'phone_number']);
```

<a name="method-only"></a>
#### `only($keys)`

`only` 메서드는 주어진 기본 키를 가진 모든 모델을 반환합니다:

```
$users = $users->only([1, 2, 3]);
```

<a name="method-setVisible"></a>
#### `setVisible($attributes)`

`setVisible` 메서드는 컬렉션 내 모든 모델에서 보이는 속성을 [일시적으로 재정의](/docs/11.x/eloquent-serialization#temporarily-modifying-attribute-visibility)합니다:

```
$users = $users->setVisible(['id', 'name']);
```

<a name="method-setHidden"></a>
#### `setHidden($attributes)`

`setHidden` 메서드는 컬렉션 내 모든 모델에서 숨김 속성을 [일시적으로 재정의](/docs/11.x/eloquent-serialization#temporarily-modifying-attribute-visibility)합니다:

```
$users = $users->setHidden(['email', 'password', 'remember_token']);
```

<a name="method-toquery"></a>
#### `toQuery()`

`toQuery` 메서드는 컬렉션 모델의 기본 키에 대해 `whereIn` 제약 조건을 포함하는 Eloquent 쿼리 빌더 인스턴스를 반환합니다:

```
use App\Models\User;

$users = User::where('status', 'VIP')->get();

$users->toQuery()->update([
    'status' => 'Administrator',
]);
```

<a name="method-unique"></a>
#### `unique($key = null, $strict = false)`

`unique` 메서드는 컬렉션 내 유일한 모델만 반환합니다. 기본 키가 동일한 모델은 중복 제거됩니다:

```
$users = $users->unique();
```

<a name="custom-collections"></a>
## 커스텀 컬렉션

특정 모델을 다룰 때 커스텀 `Collection` 객체를 사용하고 싶다면, 모델에 `CollectedBy` 속성을 추가할 수 있습니다:

```
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

또는 모델에 `newCollection` 메서드를 정의할 수도 있습니다:

```
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

`newCollection` 메서드 정의나 `CollectedBy` 속성 추가를 마치면, Eloquent가 컬렉션을 반환할 때 자동으로 커스텀 컬렉션 인스턴스를 반환합니다.

애플리케이션 내 모든 모델에 대해 커스텀 컬렉션을 사용하려면, 모든 모델이 상속하는 기본 모델 클래스에 `newCollection` 메서드를 정의하면 됩니다.