# Eloquent: 컬렉션 (Eloquent: Collections)

- [소개](#introduction)
- [사용 가능한 메서드](#available-methods)
- [커스텀 컬렉션](#custom-collections)

<a name="introduction"></a>
## 소개

여러 개의 모델 결과를 반환하는 모든 Eloquent 메서드는 `get` 메서드로 조회하거나 관계를 통해 접근한 결과를 포함하여 `Illuminate\Database\Eloquent\Collection` 클래스의 인스턴스를 반환합니다. Eloquent 컬렉션 객체는 Laravel의 [기본 컬렉션](/docs/9.x/collections)을 확장하므로 Eloquent 모델 배열을 유연하게 다루기 위한 수십 가지 메서드를 자연스럽게 상속받습니다. 이러한 유용한 메서드들에 대해 완벽히 이해하려면 Laravel 컬렉션 문서를 꼭 확인하세요!

모든 컬렉션은 또한 반복자(iterator) 역할을 하여, 마치 단순한 PHP 배열처럼 `foreach` 문으로 순회할 수 있습니다:

```
use App\Models\User;

$users = User::where('active', 1)->get();

foreach ($users as $user) {
    echo $user->name;
}
```

하지만 앞서 언급한 것처럼, 컬렉션은 단순한 배열보다 훨씬 강력하며 직관적인 인터페이스로 연결할 수 있는 다양한 map/reduce 연산을 제공합니다. 예를 들어, 비활성 사용자 모델들을 모두 제거한 뒤 남은 사용자들의 이름만 모을 수도 있습니다:

```
$names = User::all()->reject(function ($user) {
    return $user->active === false;
})->map(function ($user) {
    return $user->name;
});
```

<a name="eloquent-collection-conversion"></a>
#### Eloquent 컬렉션 변환

대부분의 Eloquent 컬렉션 메서드는 Eloquent 컬렉션의 새 인스턴스를 반환하지만, `collapse`, `flatten`, `flip`, `keys`, `pluck`, `zip` 메서드는 [기본 컬렉션](/docs/9.x/collections) 인스턴스를 반환합니다. 마찬가지로 `map` 연산 결과가 Eloquent 모델을 포함하지 않는 컬렉션일 경우 해당 결과는 기본 컬렉션 인스턴스로 변환됩니다.

<a name="available-methods"></a>
## 사용 가능한 메서드

모든 Eloquent 컬렉션은 Laravel의 기본 [컬렉션](/docs/9.x/collections#available-methods) 객체를 확장하므로, 기본 컬렉션 클래스가 제공하는 강력한 모든 메서드를 상속받습니다.

추가로, `Illuminate\Database\Eloquent\Collection` 클래스는 모델 컬렉션 관리를 돕기 위한 확장된 메서드 집합을 제공합니다. 대부분의 메서드는 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환하지만, `modelKeys` 같은 일부 메서드는 `Illuminate\Support\Collection` 인스턴스를 반환합니다.

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

`append` 메서드는 컬렉션 내 모든 모델에 특정 속성을 [추가하여 직렬화 시 포함](/docs/9.x/eloquent-serialization#appending-values-to-json)하도록 지정할 때 사용합니다. 배열이나 단일 속성을 인수로 받습니다:

```
$users->append('team');

$users->append(['team', 'is_admin']);
```

<a name="method-contains"></a>
#### `contains($key, $operator = null, $value = null)`

`contains` 메서드는 컬렉션에 특정 모델 인스턴스가 포함되어 있는지 확인할 때 사용합니다. 인수로 기본 키 또는 모델 인스턴스를 받을 수 있습니다:

```
$users->contains(1);

$users->contains(User::find(1));
```

<a name="method-diff"></a>
#### `diff($items)`

`diff` 메서드는 지정한 컬렉션에 없는 모델들만 반환합니다:

```
use App\Models\User;

$users = $users->diff(User::whereIn('id', [1, 2, 3])->get());
```

<a name="method-except"></a>
#### `except($keys)`

`except` 메서드는 주어진 기본 키를 가지지 않은 모델들만 반환합니다:

```
$users = $users->except([1, 2, 3]);
```

<a name="method-find"></a>
#### `find($key)`

`find` 메서드는 주어진 기본 키와 일치하는 모델을 반환합니다. `$key`가 모델 인스턴스면 해당 모델의 기본 키와 일치하는 모델을 반환하며, 배열인 경우 배열 내 모든 기본 키를 가진 모델들을 반환합니다:

```
$users = User::all();

$user = $users->find(1);
```

<a name="method-fresh"></a>
#### `fresh($with = [])`

`fresh` 메서드는 컬렉션 내 각 모델을 데이터베이스에서 새로 조회한 인스턴스로 갱신합니다. 선택적으로 지정한 관계도 함께 지연 로드됩니다:

```
$users = $users->fresh();

$users = $users->fresh('comments');
```

<a name="method-intersect"></a>
#### `intersect($items)`

`intersect` 메서드는 지정한 컬렉션과 겹치는 모델들만 반환합니다:

```
use App\Models\User;

$users = $users->intersect(User::whereIn('id', [1, 2, 3])->get());
```

<a name="method-load"></a>
#### `load($relations)`

`load` 메서드는 컬렉션 내 모든 모델에 대해 지정한 관계를 지연 로드(eager load)합니다:

```
$users->load(['comments', 'posts']);

$users->load('comments.author');

$users->load(['comments', 'posts' => fn ($query) => $query->where('active', 1)]);
```

<a name="method-loadMissing"></a>
#### `loadMissing($relations)`

`loadMissing` 메서드는 컬렉션 내 모델 중 아직 로드되지 않은 관계만 지연 로드합니다:

```
$users->loadMissing(['comments', 'posts']);

$users->loadMissing('comments.author');

$users->loadMissing(['comments', 'posts' => fn ($query) => $query->where('active', 1)]);
```

<a name="method-modelKeys"></a>
#### `modelKeys()`

`modelKeys` 메서드는 컬렉션 내 모든 모델의 기본 키만 모아 반환합니다:

```
$users->modelKeys();

// [1, 2, 3, 4, 5]
```

<a name="method-makeVisible"></a>
#### `makeVisible($attributes)`

`makeVisible` 메서드는 보통 각 모델에서 "숨겨진" 속성을 [보이도록 변경](/docs/9.x/eloquent-serialization#hiding-attributes-from-json)할 때 사용합니다:

```
$users = $users->makeVisible(['address', 'phone_number']);
```

<a name="method-makeHidden"></a>
#### `makeHidden($attributes)`

`makeHidden` 메서드는 기본적으로 보이는 속성을 [숨김 처리](/docs/9.x/eloquent-serialization#hiding-attributes-from-json)합니다:

```
$users = $users->makeHidden(['address', 'phone_number']);
```

<a name="method-only"></a>
#### `only($keys)`

`only` 메서드는 주어진 기본 키에 해당하는 모델들만 반환합니다:

```
$users = $users->only([1, 2, 3]);
```

<a name="method-setVisible"></a>
#### `setVisible($attributes)`

`setVisible` 메서드는 컬렉션 내 모든 모델에 대해 현재 보이는 속성을 [일시적으로 재정의](/docs/9.x/eloquent-serialization#temporarily-modifying-attribute-visibility)합니다:

```
$users = $users->setVisible(['id', 'name']);
```

<a name="method-setHidden"></a>
#### `setHidden($attributes)`

`setHidden` 메서드는 컬렉션 내 모든 모델에 대해 현재 숨긴 속성을 [일시적으로 재정의](/docs/9.x/eloquent-serialization#temporarily-modifying-attribute-visibility)합니다:

```
$users = $users->setHidden(['email', 'password', 'remember_token']);
```

<a name="method-toquery"></a>
#### `toQuery()`

`toQuery` 메서드는 컬렉션 모델의 기본 키에 `whereIn` 조건을 적용한 Eloquent 쿼리 빌더 인스턴스를 반환합니다:

```
use App\Models\User;

$users = User::where('status', 'VIP')->get();

$users->toQuery()->update([
    'status' => 'Administrator',
]);
```

<a name="method-unique"></a>
#### `unique($key = null, $strict = false)`

`unique` 메서드는 컬렉션 내 고유한 모델만 반환합니다. 컬렉션에 같은 타입에서 동일한 기본 키를 가진 모델이 있으면 중복된 모델들은 제거됩니다:

```
$users = $users->unique();
```

<a name="custom-collections"></a>
## 커스텀 컬렉션

특정 모델과 상호작용할 때 기본 Eloquent 컬렉션 대신 커스텀 `Collection` 객체를 사용하고 싶다면, 모델 클래스에 `newCollection` 메서드를 정의할 수 있습니다:

```
<?php

namespace App\Models;

use App\Support\UserCollection;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 새로운 Eloquent 컬렉션 인스턴스 생성.
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

`newCollection` 메서드를 정의하면, Eloquent가 기본적으로 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환하는 모든 경우에 사용자의 커스텀 컬렉션 인스턴스를 받게 됩니다. 애플리케이션 내 모든 모델에서 커스텀 컬렉션을 사용하고 싶다면, 모든 모델이 상속하는 베이스 모델 클래스에 `newCollection` 메서드를 정의하는 것이 좋습니다.