# Eloquent: 컬렉션 (Eloquent: Collections)

- [소개](#introduction)
- [사용 가능한 메서드](#available-methods)
- [커스텀 컬렉션](#custom-collections)

<a name="introduction"></a>
## 소개

Eloquent 메서드 중 다수의 모델 결과를 반환하는 모든 메서드는 `get` 메서드로 조회했거나 관계를 통해 접근한 경우를 포함하여 `Illuminate\Database\Eloquent\Collection` 클래스의 인스턴스를 반환합니다. Eloquent 컬렉션 객체는 Laravel의 [기본 컬렉션](/docs/10.x/collections)을 확장하므로, Eloquent 모델 배열을 유연하게 다루는 데 사용되는 수십 가지 메서드를 자연스럽게 상속받습니다. 이 유용한 메서드들에 대해 자세히 알아보려면 Laravel 컬렉션 문서를 꼭 참고하세요!

모든 컬렉션은 반복자(iterator)의 역할도 하므로, 마치 단순한 PHP 배열인 것처럼 루프를 돌 수 있습니다:

```
use App\Models\User;

$users = User::where('active', 1)->get();

foreach ($users as $user) {
    echo $user->name;
}
```

하지만 앞서 언급했듯 컬렉션은 단순한 배열보다 훨씬 강력하며, 직관적인 인터페이스로 체이닝이 가능한 다양한 map / reduce 연산 메서드를 제공합니다. 예를 들어, 비활성 모델을 모두 제거한 뒤 남은 사용자 각각의 이름만 추출할 수 있습니다:

```
$names = User::all()->reject(function (User $user) {
    return $user->active === false;
})->map(function (User $user) {
    return $user->name;
});
```

<a name="eloquent-collection-conversion"></a>
#### Eloquent 컬렉션 변환

대부분의 Eloquent 컬렉션 메서드는 새로운 Eloquent 컬렉션 인스턴스를 반환하지만, `collapse`, `flatten`, `flip`, `keys`, `pluck`, `zip` 메서드는 [기본 컬렉션](/docs/10.x/collections) 인스턴스를 반환합니다. 또한 `map` 연산 결과가 Eloquent 모델을 포함하지 않는 컬렉션일 경우, 기본 컬렉션 인스턴스로 변환됩니다.

<a name="available-methods"></a>
## 사용 가능한 메서드

모든 Eloquent 컬렉션은 기본 [Laravel 컬렉션](/docs/10.x/collections#available-methods) 객체를 확장하기 때문에, 기본 컬렉션 클래스가 제공하는 강력한 모든 메서드를 상속받습니다.

또한 `Illuminate\Database\Eloquent\Collection` 클래스는 모델 컬렉션 관리를 돕는 메서드 집합을 추가 제공합니다. 대부분의 메서드는 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환하지만, `modelKeys` 같은 몇몇 메서드는 `Illuminate\Support\Collection` 인스턴스를 반환합니다.

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
#### `append($attributes)`

`append` 메서드는 컬렉션 내 모든 모델에 대해 해당 속성을 [추가할(appended)](/docs/10.x/eloquent-serialization#appending-values-to-json) 것임을 지정할 때 사용합니다. 배열 또는 단일 속성을 인수로 받습니다:

```
$users->append('team');

$users->append(['team', 'is_admin']);
```

<a name="method-contains"></a>
#### `contains($key, $operator = null, $value = null)`

`contains` 메서드는 컬렉션에 특정 모델 인스턴스가 포함되어 있는지 확인할 때 쓰입니다. 기본 키 또는 모델 인스턴스를 인수로 전달할 수 있습니다:

```
$users->contains(1);

$users->contains(User::find(1));
```

<a name="method-diff"></a>
#### `diff($items)`

`diff` 메서드는 인수로 전달된 컬렉션에 없는 모델만 반환합니다:

```
use App\Models\User;

$users = $users->diff(User::whereIn('id', [1, 2, 3])->get());
```

<a name="method-except"></a>
#### `except($keys)`

`except` 메서드는 지정한 기본 키를 갖지 않는 모델만 반환합니다:

```
$users = $users->except([1, 2, 3]);
```

<a name="method-find"></a>
#### `find($key)`

`find` 메서드는 주어진 키와 일치하는 기본 키를 가진 모델을 반환합니다. 만약 `$key`가 모델 인스턴스라면, 동일 키를 가진 모델을 시도해서 반환하며, 배열일 경우 해당 배열에 있는 기본 키를 가진 모든 모델을 반환합니다:

```
$users = User::all();

$user = $users->find(1);
```

<a name="method-fresh"></a>
#### `fresh($with = [])`

`fresh` 메서드는 컬렉션 각 모델을 데이터베이스에서 새로 조회하여 인스턴스를 반환합니다. 이때 관계 로딩을 지정할 수도 있습니다:

```
$users = $users->fresh();

$users = $users->fresh('comments');
```

<a name="method-intersect"></a>
#### `intersect($items)`

`intersect` 메서드는 주어진 컬렉션에도 존재하는 모델들만 반환합니다:

```
use App\Models\User;

$users = $users->intersect(User::whereIn('id', [1, 2, 3])->get());
```

<a name="method-load"></a>
#### `load($relations)`

`load` 메서드는 컬렉션 내 모든 모델에 대해 지정된 관계를 즉시 로딩(eager load)합니다:

```
$users->load(['comments', 'posts']);

$users->load('comments.author');

$users->load(['comments', 'posts' => fn ($query) => $query->where('active', 1)]);
```

<a name="method-loadMissing"></a>
#### `loadMissing($relations)`

`loadMissing` 메서드는 관계가 로딩되어 있지 않은 경우에만 지정한 관계를 즉시 로딩합니다:

```
$users->loadMissing(['comments', 'posts']);

$users->loadMissing('comments.author');

$users->loadMissing(['comments', 'posts' => fn ($query) => $query->where('active', 1)]);
```

<a name="method-modelKeys"></a>
#### `modelKeys()`

`modelKeys` 메서드는 컬렉션에 있는 모든 모델의 기본 키를 반환합니다:

```
$users->modelKeys();

// [1, 2, 3, 4, 5]
```

<a name="method-makeVisible"></a>
#### `makeVisible($attributes)`

`makeVisible` 메서드는 컬렉션 내 각 모델에서 일반적으로 "숨겨진" 속성을 [보이도록](/docs/10.x/eloquent-serialization#hiding-attributes-from-json) 만듭니다:

```
$users = $users->makeVisible(['address', 'phone_number']);
```

<a name="method-makeHidden"></a>
#### `makeHidden($attributes)`

`makeHidden` 메서드는 컬렉션 내 각 모델에서 일반적으로 "보이는" 속성을 [숨깁니다](/docs/10.x/eloquent-serialization#hiding-attributes-from-json):

```
$users = $users->makeHidden(['address', 'phone_number']);
```

<a name="method-only"></a>
#### `only($keys)`

`only` 메서드는 지정한 기본 키를 가진 모든 모델을 반환합니다:

```
$users = $users->only([1, 2, 3]);
```

<a name="method-setVisible"></a>
#### `setVisible($attributes)`

`setVisible` 메서드는 컬렉션 내 모든 모델의 보이는 속성 목록을 [일시적으로 재정의](/docs/10.x/eloquent-serialization#temporarily-modifying-attribute-visibility)합니다:

```
$users = $users->setVisible(['id', 'name']);
```

<a name="method-setHidden"></a>
#### `setHidden($attributes)`

`setHidden` 메서드는 컬렉션 내 모든 모델의 숨김 속성 목록을 [일시적으로 재정의](/docs/10.x/eloquent-serialization#temporarily-modifying-attribute-visibility)합니다:

```
$users = $users->setHidden(['email', 'password', 'remember_token']);
```

<a name="method-toquery"></a>
#### `toQuery()`

`toQuery` 메서드는 컬렉션 모델의 기본 키에 대해 `whereIn` 조건이 걸린 Eloquent 쿼리 빌더 인스턴스를 반환합니다:

```
use App\Models\User;

$users = User::where('status', 'VIP')->get();

$users->toQuery()->update([
    'status' => 'Administrator',
]);
```

<a name="method-unique"></a>
#### `unique($key = null, $strict = false)`

`unique` 메서드는 컬렉션 내 중복되지 않는 유일한 모델만 반환합니다. 동일한 타입의 중복 기본 키를 가진 모델들은 제거됩니다:

```
$users = $users->unique();
```

<a name="custom-collections"></a>
## 커스텀 컬렉션

특정 모델과 상호작용 시 커스텀 `Collection` 객체를 사용하고 싶다면, 모델에 `newCollection` 메서드를 정의하면 됩니다:

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

`newCollection` 메서드를 정의한 후에는, Eloquent가 기존에 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환하던 모든 경우에 커스텀 컬렉션 인스턴스를 받게 됩니다. 애플리케이션 내 모든 모델에 커스텀 컬렉션을 적용하고 싶다면, 모든 모델이 확장하는 기본 베이스 모델 클래스에 `newCollection` 메서드를 정의하는 것이 좋습니다.