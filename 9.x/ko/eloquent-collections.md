# Eloquent: 컬렉션(Collections)

- [소개](#introduction)
- [사용 가능한 메서드](#available-methods)
- [커스텀 컬렉션](#custom-collections)

<a name="introduction"></a>
## 소개

하나 이상의 모델 결과를 반환하는 모든 Eloquent 메서드는 `Illuminate\Database\Eloquent\Collection` 클래스의 인스턴스를 반환합니다. 이에는 `get` 메서드로 가져온 결과나 리레이션(관계)을 통해 접근하는 결과도 포함됩니다. Eloquent 컬렉션 객체는 Laravel의 [기본 컬렉션](/docs/{{version}}/collections)을 확장하므로, 기본 Eloquent 모델 배열을 유연하게 다룰 수 있는 다양한 메서드를 자연스럽게 상속받습니다. 이러한 유용한 메서드에 대해 자세히 알고 싶다면 Laravel 컬렉션 문서를 꼭 확인하세요!

모든 컬렉션은 반복자로 동작하므로, 일반 PHP 배열처럼 반복문으로 순회할 수 있습니다:

    use App\Models\User;

    $users = User::where('active', 1)->get();

    foreach ($users as $user) {
        echo $user->name;
    }

하지만 앞서 언급했듯 컬렉션은 단순한 배열보다 훨씬 강력하며, 직관적인 인터페이스를 통해 다양한 map / reduce 작업을 체이닝할 수 있게 해줍니다. 예를 들어, 비활성화된 모델을 모두 제거한 뒤 남은 사용자 각각의 이름만 모을 수도 있습니다:

    $names = User::all()->reject(function ($user) {
        return $user->active === false;
    })->map(function ($user) {
        return $user->name;
    });

<a name="eloquent-collection-conversion"></a>
#### Eloquent 컬렉션 변환

대부분의 Eloquent 컬렉션 메서드는 새로운 Eloquent 컬렉션 인스턴스를 반환합니다. 그러나 `collapse`, `flatten`, `flip`, `keys`, `pluck`, `zip` 메서드는 [기본 컬렉션](/docs/{{version}}/collections) 인스턴스를 반환합니다. 마찬가지로, `map` 연산 결과가 Eloquent 모델을 포함하지 않는 컬렉션이라면, 이는 기본 컬렉션 인스턴스로 변환됩니다.

<a name="available-methods"></a>
## 사용 가능한 메서드

모든 Eloquent 컬렉션은 [Laravel 기본 컬렉션](/docs/{{version}}/collections#available-methods) 객체를 확장합니다. 따라서, 기본 컬렉션 클래스가 제공하는 강력한 모든 메서드를 사용할 수 있습니다.

추가로, `Illuminate\Database\Eloquent\Collection` 클래스는 모델 컬렉션 관리를 돕는 다양한 메서드를 추가로 제공합니다. 대부분의 메서드는 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환하지만, `modelKeys`와 같은 일부 메서드는 `Illuminate\Support\Collection` 인스턴스를 반환합니다.

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

`append` 메서드는 컬렉션 내의 모든 모델에 [속성을 추가](/docs/{{version}}/eloquent-serialization#appending-values-to-json)하도록 지정할 때 사용합니다. 이 메서드는 속성 단일값 또는 속성 배열을 인자로 받습니다:

    $users->append('team');
    
    $users->append(['team', 'is_admin']);

<a name="method-contains"></a>
#### `contains($key, $operator = null, $value = null)` {.collection-method}

`contains` 메서드는 특정 모델 인스턴스가 컬렉션에 포함되어 있는지 확인할 때 사용합니다. 이 메서드는 기본키 또는 모델 인스턴스를 인자로 받습니다:

    $users->contains(1);

    $users->contains(User::find(1));

<a name="method-diff"></a>
#### `diff($items)` {.collection-method}

`diff` 메서드는 주어진 컬렉션에 없는 모든 모델을 반환합니다:

    use App\Models\User;

    $users = $users->diff(User::whereIn('id', [1, 2, 3])->get());

<a name="method-except"></a>
#### `except($keys)` {.collection-method}

`except` 메서드는 주어진 기본키를 가지지 않은 모델만 반환합니다:

    $users = $users->except([1, 2, 3]);

<a name="method-find"></a>
#### `find($key)` {.collection-method}

`find` 메서드는 주어진 키와 일치하는 기본키를 가진 모델을 반환합니다. `$key`가 모델 인스턴스인 경우에는 해당 인스턴스의 기본키와 일치하는 모델을 반환하려 시도합니다. `$key`가 키의 배열이 되면, 주어진 배열 내 키를 가진 모델을 모두 반환합니다:

    $users = User::all();

    $user = $users->find(1);

<a name="method-fresh"></a>
#### `fresh($with = [])` {.collection-method}

`fresh` 메서드는 데이터베이스에서 컬렉션의 각 모델을 새롭게 조회합니다. 필요하다면 지정된 관계를 eager loading(즉시 로딩)할 수도 있습니다:

    $users = $users->fresh();

    $users = $users->fresh('comments');

<a name="method-intersect"></a>
#### `intersect($items)` {.collection-method}

`intersect` 메서드는 주어진 컬렉션에도 존재하는 모든 모델을 반환합니다:

    use App\Models\User;

    $users = $users->intersect(User::whereIn('id', [1, 2, 3])->get());

<a name="method-load"></a>
#### `load($relations)` {.collection-method}

`load` 메서드는 컬렉션 내 모든 모델에 대해 주어진 관계들을 eager loading합니다:

    $users->load(['comments', 'posts']);

    $users->load('comments.author');
    
    $users->load(['comments', 'posts' => fn ($query) => $query->where('active', 1)]);

<a name="method-loadMissing"></a>
#### `loadMissing($relations)` {.collection-method}

`loadMissing` 메서드는 컬렉션 내 모든 모델에 대해 아직 로드되지 않은 관계만 eager loading합니다:

    $users->loadMissing(['comments', 'posts']);

    $users->loadMissing('comments.author');
    
    $users->loadMissing(['comments', 'posts' => fn ($query) => $query->where('active', 1)]);

<a name="method-modelKeys"></a>
#### `modelKeys()` {.collection-method}

`modelKeys` 메서드는 컬렉션의 모든 모델의 기본키만 배열로 반환합니다:

    $users->modelKeys();

    // [1, 2, 3, 4, 5]

<a name="method-makeVisible"></a>
#### `makeVisible($attributes)` {.collection-method}

`makeVisible` 메서드는 컬렉션 내 각 모델에서 일반적으로 "숨김" 처리된 속성을 [표시](/docs/{{version}}/eloquent-serialization#hiding-attributes-from-json)하도록 만듭니다:

    $users = $users->makeVisible(['address', 'phone_number']);

<a name="method-makeHidden"></a>
#### `makeHidden($attributes)` {.collection-method}

`makeHidden` 메서드는 컬렉션 내 각 모델에서 일반적으로 "보임" 처리된 속성을 [숨김 처리](/docs/{{version}}/eloquent-serialization#hiding-attributes-from-json)하도록 만듭니다:

    $users = $users->makeHidden(['address', 'phone_number']);

<a name="method-only"></a>
#### `only($keys)` {.collection-method}

`only` 메서드는 주어진 기본키를 가진 모든 모델만 반환합니다:

    $users = $users->only([1, 2, 3]);

<a name="method-setVisible"></a>
#### `setVisible($attributes)` {.collection-method}

`setVisible` 메서드는 각 모델의 표시 속성을 [일시적으로 재정의](/docs/{{version}}/eloquent-serialization#temporarily-modifying-attribute-visibility)합니다:

    $users = $users->setVisible(['id', 'name']);

<a name="method-setHidden"></a>
#### `setHidden($attributes)` {.collection-method}

`setHidden` 메서드는 각 모델의 숨김 속성을 [일시적으로 재정의](/docs/{{version}}/eloquent-serialization#temporarily-modifying-attribute-visibility)합니다:

    $users = $users->setHidden(['email', 'password', 'remember_token']);

<a name="method-toquery"></a>
#### `toQuery()` {.collection-method}

`toQuery` 메서드는 컬렉션 모델의 기본키에 대해 `whereIn` 제약조건이 포함된 Eloquent 쿼리 빌더 인스턴스를 반환합니다:

    use App\Models\User;

    $users = User::where('status', 'VIP')->get();

    $users->toQuery()->update([
        'status' => 'Administrator',
    ]);

<a name="method-unique"></a>
#### `unique($key = null, $strict = false)` {.collection-method}

`unique` 메서드는 컬렉션 내 고유한 모든 모델만 반환합니다. 동일 타입의 모델이 컬렉션 내에서 동일한 기본키로 여러 번 나타날 경우, 중복된 모델이 제거됩니다:

    $users = $users->unique();

<a name="custom-collections"></a>
## 커스텀 컬렉션

특정 모델과 상호작용할 때 커스텀 `Collection` 객체를 사용하고 싶다면, 모델에 `newCollection` 메서드를 정의할 수 있습니다:

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

`newCollection` 메서드를 정의하면, Eloquent가 일반적으로 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환하는 모든 경우에 커스텀 컬렉션 인스턴스를 받을 수 있습니다. 애플리케이션 내 모든 모델에 대해 커스텀 컬렉션을 사용하려면, 모든 모델이 확장하는 기본 모델 클래스에 `newCollection` 메서드를 정의해야 합니다.