# Eloquent: 컬렉션 (Collections)

- [소개](#introduction)
- [사용 가능한 메서드](#available-methods)
- [커스텀 컬렉션](#custom-collections)

<a name="introduction"></a>
## 소개

하나 이상의 모델 결과를 반환하는 모든 Eloquent 메서드는 `get` 메서드를 통해서든, 연관관계를 통해 접근하든, `Illuminate\Database\Eloquent\Collection` 클래스의 인스턴스를 반환합니다. Eloquent 컬렉션 객체는 Laravel의 [기본 컬렉션](/docs/{{version}}/collections) 클래스를 확장하므로, Eloquent 모델 배열을 다룰 때 유용한 수십 가지 메서드를 상속받아 사용할 수 있습니다. 이 유용한 메서드들을 모두 익히기 위해 Laravel 컬렉션 문서를 꼭 참고하세요!

모든 컬렉션 객체는 반복자(iterator) 역할도 하므로, 일반 PHP 배열처럼 반복문을 통해 순회할 수 있습니다:

```
use App\Models\User;

$users = User::where('active', 1)->get();

foreach ($users as $user) {
    echo $user->name;
}
```

하지만 앞서 언급했듯, 컬렉션은 배열보다 훨씬 강력하며, 직관적인 인터페이스로 연결(chain)할 수 있는 다양한 map/reduce 연산을 제공합니다. 예를 들어, 비활성 사용자 모델을 모두 제거하고 나머지 사용자 각각의 이름만 추출할 수 있습니다:

```
$names = User::all()->reject(function ($user) {
    return $user->active === false;
})->map(function ($user) {
    return $user->name;
});
```

<a name="eloquent-collection-conversion"></a>
#### Eloquent 컬렉션 변환

대부분의 Eloquent 컬렉션 메서드는 Eloquent 컬렉션의 새 인스턴스를 반환하지만, `collapse`, `flatten`, `flip`, `keys`, `pluck`, `zip` 메서드는 [기본 컬렉션](/docs/{{version}}/collections) 인스턴스를 반환합니다. 마찬가지로, `map` 연산이 Eloquent 모델을 포함하지 않는 컬렉션을 반환하는 경우, 기본 컬렉션 인스턴스로 변환됩니다.

<a name="available-methods"></a>
## 사용 가능한 메서드

모든 Eloquent 컬렉션은 기본 [Laravel 컬렉션](/docs/{{version}}/collections#available-methods) 객체를 확장하므로, 기본 컬렉션 클래스가 제공하는 모든 강력한 메서드를 상속받습니다.

추가로, `Illuminate\Database\Eloquent\Collection` 클래스에는 모델 컬렉션 관리를 돕는 다양한 메서드 세트가 포함되어 있습니다. 대부분의 메서드는 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환하지만, `modelKeys` 같은 일부 메서드는 `Illuminate\Support\Collection` 인스턴스를 반환합니다.

<div id="collection-method-list" markdown="1">

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
[toQuery](#method-toquery)  
[unique](#method-unique)

</div>

<a name="method-contains"></a>
#### `contains($key, $operator = null, $value = null)`

`contains` 메서드는 컬렉션이 특정 모델 인스턴스를 포함하고 있는지 확인할 때 사용합니다. 이 메서드는 기본 키(primary key)나 모델 인스턴스를 인수로 받을 수 있습니다:

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

`except` 메서드는 주어진 기본 키들을 포함하지 않는 모든 모델을 반환합니다:

```
$users = $users->except([1, 2, 3]);
```

<a name="method-find"></a>
#### `find($key)`

`find` 메서드는 주어진 기본 키와 일치하는 모델을 반환합니다. `$key`가 모델 인스턴스라면, 해당 인스턴스의 기본 키에 맞는 모델을 반환합니다. 만약 `$key`가 기본 키 배열이라면, 배열 내 기본 키를 가진 모든 모델을 반환합니다:

```
$users = User::all();

$user = $users->find(1);
```

<a name="method-fresh"></a>
#### `fresh($with = [])`

`fresh` 메서드는 컬렉션에 있는 각 모델의 최신 인스턴스를 데이터베이스에서 새로 조회합니다. 추가로, 전달된 연관관계는 eager loading 됩니다:

```
$users = $users->fresh();

$users = $users->fresh('comments');
```

<a name="method-intersect"></a>
#### `intersect($items)`

`intersect` 메서드는 주어진 컬렉션에도 포함된 모든 모델을 반환합니다:

```
use App\Models\User;

$users = $users->intersect(User::whereIn('id', [1, 2, 3])->get());
```

<a name="method-load"></a>
#### `load($relations)`

`load` 메서드는 컬렉션에 포함된 모든 모델에 대해 지정된 연관관계를 eager loading 합니다:

```
$users->load(['comments', 'posts']);

$users->load('comments.author');
```

<a name="method-loadMissing"></a>
#### `loadMissing($relations)`

`loadMissing` 메서드는 이미 로드되어 있지 않은 연관관계에 한해 컬렉션 내 모든 모델에 대해 지정된 연관관계를 eager loading 합니다:

```
$users->loadMissing(['comments', 'posts']);

$users->loadMissing('comments.author');
```

<a name="method-modelKeys"></a>
#### `modelKeys()`

`modelKeys` 메서드는 컬렉션 내 모든 모델의 기본 키를 반환합니다:

```
$users->modelKeys();

// [1, 2, 3, 4, 5]
```

<a name="method-makeVisible"></a>
#### `makeVisible($attributes)`

`makeVisible` 메서드는 컬렉션 내 각 모델에서 기본적으로 숨겨져 있는 속성들을 [보이도록 설정](/docs/{{version}}/eloquent-serialization#hiding-attributes-from-json) 합니다:

```
$users = $users->makeVisible(['address', 'phone_number']);
```

<a name="method-makeHidden"></a>
#### `makeHidden($attributes)`

`makeHidden` 메서드는 컬렉션 내 각 모델에서 기본적으로 보이는 속성들을 [숨김 처리](/docs/{{version}}/eloquent-serialization#hiding-attributes-from-json) 합니다:

```
$users = $users->makeHidden(['address', 'phone_number']);
```

<a name="method-only"></a>
#### `only($keys)`

`only` 메서드는 주어진 기본 키를 가진 모든 모델을 반환합니다:

```
$users = $users->only([1, 2, 3]);
```

<a name="method-toquery"></a>
#### `toQuery()`

`toQuery` 메서드는 컬렉션 모델의 기본 키들을 기준으로 `whereIn` 조건이 적용된 Eloquent 쿼리 빌더 인스턴스를 반환합니다:

```
use App\Models\User;

$users = User::where('status', 'VIP')->get();

$users->toQuery()->update([
    'status' => 'Administrator',
]);
```

<a name="method-unique"></a>
#### `unique($key = null, $strict = false)`

`unique` 메서드는 컬렉션에서 중복되지 않는 고유한 모델만 반환합니다. 같은 타입이며 기본 키가 같은 모델이 여러 개 있다면 하나만 남기고 제거됩니다:

```
$users = $users->unique();
```

<a name="custom-collections"></a>
## 커스텀 컬렉션

특정 모델을 다룰 때 커스텀 `Collection` 객체를 사용하려면, 모델에 `newCollection` 메서드를 정의할 수 있습니다:

```
<?php

namespace App\Models;

use App\Support\UserCollection;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 새로운 Eloquent 컬렉션 인스턴스를 생성합니다.
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

`newCollection` 메서드를 정의하면, Eloquent가 일반적으로 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환하는 대신 커스텀 컬렉션 인스턴스를 반환합니다. 애플리케이션 내 모든 모델에서 커스텀 컬렉션을 사용하려면, 애플리케이션의 모든 모델이 상속받는 기본 모델 클래스에 `newCollection` 메서드를 정의하는 것이 좋습니다.