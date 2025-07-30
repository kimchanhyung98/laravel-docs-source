# Eloquent: 관계 (Eloquent: Relationships)

- [소개](#introduction)
- [관계 정의하기](#defining-relationships)
    - [1:1 관계](#one-to-one)
    - [1:N 관계](#one-to-many)
    - [1:N 관계 (역방향) / Belongs To](#one-to-many-inverse)
    - [Has One Of Many](#has-one-of-many)
    - [Has One Through](#has-one-through)
    - [Has Many Through](#has-many-through)
- [N:M 관계](#many-to-many)
    - [중간 테이블 컬럼 가져오기](#retrieving-intermediate-table-columns)
    - [중간 테이블 컬럼을 이용한 조건 필터링](#filtering-queries-via-intermediate-table-columns)
    - [커스텀 중간 테이블 모델 정의하기](#defining-custom-intermediate-table-models)
- [다형성 관계 (Polymorphic Relationships)](#polymorphic-relationships)
    - [1:1 다형성](#one-to-one-polymorphic-relations)
    - [1:N 다형성](#one-to-many-polymorphic-relations)
    - [One Of Many 다형성](#one-of-many-polymorphic-relations)
    - [N:M 다형성](#many-to-many-polymorphic-relations)
    - [커스텀 다형성 타입](#custom-polymorphic-types)
- [동적 관계](#dynamic-relationships)
- [관계 조회하기](#querying-relations)
    - [관계 메서드 vs 동적 프로퍼티](#relationship-methods-vs-dynamic-properties)
    - [관계 존재 여부 쿼리하기](#querying-relationship-existence)
    - [관계 부재 여부 쿼리하기](#querying-relationship-absence)
    - [Morph To 관계 쿼리하기](#querying-morph-to-relationships)
- [연관 모델 집계](#aggregating-related-models)
    - [연관 모델 개수 세기](#counting-related-models)
    - [기타 집계 함수](#other-aggregate-functions)
    - [Morph To 관계에서 연관 모델 개수 세기](#counting-related-models-on-morph-to-relationships)
- [지연로딩(eager loading)](#eager-loading)
    - [지연로딩 제약 조건](#constraining-eager-loads)
    - [지연로딩 후 로딩(lazy eager loading)](#lazy-eager-loading)
    - [지연로딩 방지하기](#preventing-lazy-loading)
- [연관 모델 삽입 및 갱신](#inserting-and-updating-related-models)
    - [`save` 메서드](#the-save-method)
    - [`create` 메서드](#the-create-method)
    - [Belongs To 관계 갱신하기](#updating-belongs-to-relationships)
    - [N:M 관계 갱신하기](#updating-many-to-many-relationships)
- [부모 타임스탬프 자동 갱신 (Touching Parent Timestamps)](#touching-parent-timestamps)

<a name="introduction"></a>
## 소개 (Introduction)

데이터베이스 테이블 간에는 종종 관계가 존재합니다. 예를 들어, 블로그 게시글은 여러 개의 댓글을 가질 수 있고, 주문 내역은 해당 주문을 한 사용자와 연관될 수 있습니다. Eloquent는 이런 관계를 쉽게 관리하고 사용할 수 있도록 지원하며, 여러 기본적인 관계 유형을 제공합니다:

<div class="content-list" markdown="1">

- [1:1 관계](#one-to-one)
- [1:N 관계](#one-to-many)
- [N:M 관계](#many-to-many)
- [Has One Through](#has-one-through)
- [Has Many Through](#has-many-through)
- [1:1 다형성 관계](#one-to-one-polymorphic-relations)
- [1:N 다형성 관계](#one-to-many-polymorphic-relations)
- [N:M 다형성 관계](#many-to-many-polymorphic-relations)

</div>

<a name="defining-relationships"></a>
## 관계 정의하기 (Defining Relationships)

Eloquent의 관계는 Eloquent 모델 클래스 내 메서드로 정의합니다. 관계 메서드는 강력한 [쿼리 빌더](/docs/{{version}}/queries)의 역할도 하므로, 관계를 메서드로 정의하면 메서드 체이닝 및 쿼리 확장이 매우 용이합니다. 예를 들어, `posts` 관계에 추가 조건을 걸어 체이닝할 수 있습니다:

```
$user->posts()->where('active', 1)->get();
```

관계를 사용법에 깊게 들어가기 전에, Eloquent가 지원하는 각 관계 유형을 어떻게 정의하는지 알아봅시다.

<a name="one-to-one"></a>
### 1:1 관계 (One To One)

1:1 관계는 가장 기본적인 데이터베이스 관계 유형입니다. 예를 들어, `User` 모델이 하나의 `Phone` 모델과 연관될 수 있습니다. 이 관계를 `User` 모델 내 `phone` 메서드로 정의할 수 있습니다. 이 메서드가 `hasOne` 메서드를 호출하고 결과를 반환해야 합니다. `hasOne` 메서드는 모든 모델이 상속받는 `Illuminate\Database\Eloquent\Model` 클래스에 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 사용자와 연관된 전화번호를 가져옵니다.
     */
    public function phone()
    {
        return $this->hasOne(Phone::class);
    }
}
```

`hasOne` 메서드의 첫 번째 인자는 연관된 모델 클래스명입니다. 관계를 정의한 이후에는 Eloquent의 동적 프로퍼티(dynamic properties)를 사용해 관련 레코드를 가져올 수 있습니다. 동적 프로퍼티는 마치 모델에 프로퍼티가 있는 것처럼 관계 메서드에 접근할 수 있게 합니다:

```php
$phone = User::find(1)->phone;
```

Eloquent는 부모 모델명에 기반하여 외래 키를 자동으로 추론합니다. 여기서는 `Phone` 모델이 `user_id` 컬럼을 외래 키로 가진다고 가정합니다. 이 규칙을 변경하려면 `hasOne` 메서드의 두 번째 인자로 직접 키 이름을 지정할 수 있습니다:

```php
return $this->hasOne(Phone::class, 'foreign_key');
```

또한, Eloquent는 외래 키가 부모 모델의 기본 키(`id` 컬럼)의 값과 일치한다고 가정합니다. 만약 기본 키가 `id`가 아니거나 커스텀 `$primaryKey`를 쓰는 경우, 세 번째 인자로 로컬 키를 지정할 수 있습니다:

```php
return $this->hasOne(Phone::class, 'foreign_key', 'local_key');
```

<a name="one-to-one-defining-the-inverse-of-the-relationship"></a>
#### 관계의 역방향 정의하기

`User` 모델에서 `Phone` 모델을 참조할 수 있듯, `Phone` 모델에서도 이 전화번호를 소유한 `User`를 참조할 수 있게 관계를 정의할 수 있습니다. `hasOne` 관계의 역방향은 `belongsTo` 메서드를 사용하여 정의합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Phone extends Model
{
    /**
     * 이 전화번호를 가진 사용자를 가져옵니다.
     */
    public function user()
    {
        return $this->belongsTo(User::class);
    }
}
```

`user` 메서드를 호출하면 Eloquent는 `Phone` 모델의 `user_id` 컬럼 값과 일치하는 `User` 모델의 `id`를 찾습니다.

외래 키 이름은 관계 메서드 이름(`user`)에 `_id`를 붙여 자동 추론되므로 여기서는 `user_id` 컬럼이라 가정합니다. 만약 외래 키가 다르다면, `belongsTo` 두 번째 인자에 외래 키 이름을 직접 지정할 수 있습니다:

```php
/**
 * 이 전화번호를 가진 사용자를 가져옵니다.
 */
public function user()
{
    return $this->belongsTo(User::class, 'foreign_key');
}
```

또한, 부모 모델의 기본 키(`id`)가 아닌 다른 키로 참조하려면 세 번째 인자에 로컬 키를 지정할 수 있습니다:

```php
/**
 * 이 전화번호를 가진 사용자를 가져옵니다.
 */
public function user()
{
    return $this->belongsTo(User::class, 'foreign_key', 'owner_key');
}
```

<a name="one-to-many"></a>
### 1:N 관계 (One To Many)

1:N 관계는 하나의 부모 모델이 여러 자식 모델과 연관되는 경우에 사용합니다. 예를 들어, 하나의 블로그 게시글은 무수히 많은 댓글을 가질 수 있습니다. 다른 관계들과 마찬가지로 메서드로 정의합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Post extends Model
{
    /**
     * 이 게시글의 댓글들을 가져옵니다.
     */
    public function comments()
    {
        return $this->hasMany(Comment::class);
    }
}
```

Eloquent는 자식 모델인 `Comment`의 적절한 외래 키를 자동으로 결정합니다. 기본 규칙은 부모 모델명을 snake_case로 변환 후 `_id`를 붙이는 것인데, 여기서는 `post_id`가 됩니다.

정의 후에는 `comments` 동적 프로퍼티로 컬렉션([collection](/docs/{{version}}/eloquent-collections)) 형태로 댓글들을 가져올 수 있습니다:

```php
use App\Models\Post;

$comments = Post::find(1)->comments;

foreach ($comments as $comment) {
    //
}
```

또한 모든 관계는 쿼리 빌더이므로, 메서드를 직접 호출해 조건을 추가할 수도 있습니다:

```php
$comment = Post::find(1)->comments()
                    ->where('title', 'foo')
                    ->first();
```

`hasOne`과 마찬가지로, 외래 키 및 로컬 키를 직접 지정하고 싶다면, `hasMany` 메서드에 인자를 추가로 넘기면 됩니다:

```php
return $this->hasMany(Comment::class, 'foreign_key');

return $this->hasMany(Comment::class, 'foreign_key', 'local_key');
```

<a name="one-to-many-inverse"></a>
### 1:N 관계 (역방향) / Belongs To (One To Many (Inverse) / Belongs To)

이제 게시글 하나가 여러 댓글을 가질 수 있으므로, 각 댓글에서 부모 게시글을 참조하는 관계를 정의해보겠습니다. `hasMany` 관계의 역방향으로, 자식 모델에 `belongsTo` 관계를 정의합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Comment extends Model
{
    /**
     * 이 댓글의 소유 게시글을 가져옵니다.
     */
    public function post()
    {
        return $this->belongsTo(Post::class);
    }
}
```

이 관계를 정의한 후에는 `post` 동적 프로퍼티로 댓글의 부모 게시글에 접근할 수 있습니다:

```php
use App\Models\Comment;

$comment = Comment::find(1);

return $comment->post->title;
```

이 때, Eloquent는 `Comment` 모델의 `post_id` 컬럼 값과 `Post` 모델의 `id` 값을 매칭하여 부모 게시글을 찾습니다.

외래 키는 관계 메서드 이름(`post`)에 `_` 그리고 부모 모델의 기본 키 컬럼명을 붙인 형태로 자동 결정되어 `post_id`가 됩니다. 외래 키 또는 기본 키가 다를 경우, `belongsTo` 메서드 인자를 직접 지정할 수 있습니다:

```php
/**
 * 이 댓글의 소유 게시글을 가져옵니다.
 */
public function post()
{
    return $this->belongsTo(Post::class, 'foreign_key');
}
```

```php
/**
 * 이 댓글의 소유 게시글을 가져옵니다.
 */
public function post()
{
    return $this->belongsTo(Post::class, 'foreign_key', 'owner_key');
}
```

<a name="default-models"></a>
#### 기본 모델(Default Models)

`belongsTo`, `hasOne`, `hasOneThrough`, `morphOne` 관계에서는, 관계가 `null`일 때 반환할 기본 모델을 지정할 수 있습니다. 이는 흔히 [Null Object 패턴](https://en.wikipedia.org/wiki/Null_Object_pattern)으로 불리며, 조건문을 줄이는데 유용합니다. 

예를 들어, 게시글 `Post` 모델의 `user` 관계에 기본 `App\Models\User` 객체를 지정하면, 관계가 없을 때도 빈 User 모델이 반환됩니다:

```php
/**
 * 게시글 작성자를 가져옵니다.
 */
public function user()
{
    return $this->belongsTo(User::class)->withDefault();
}
```

`withDefault` 메서드의 인자로 배열 또는 클로저를 넘겨 기본 모델 속성을 초기화할 수도 있습니다:

```php
/**
 * 게시글 작성자를 가져옵니다.
 */
public function user()
{
    return $this->belongsTo(User::class)->withDefault([
        'name' => 'Guest Author',
    ]);
}

/**
 * 게시글 작성자를 가져옵니다.
 */
public function user()
{
    return $this->belongsTo(User::class)->withDefault(function ($user, $post) {
        $user->name = 'Guest Author';
    });
}
```

<a name="querying-belongs-to-relationships"></a>
#### Belongs To 관계 쿼리하기

`belongsTo` 관계의 자식 모델들을 조회할 때, 아래처럼 직접 `where` 조건을 만들어 조회할 수 있습니다:

```php
use App\Models\Post;

$posts = Post::where('user_id', $user->id)->get();
```

그러나 `whereBelongsTo` 메서드를 사용하면 모델과 적절한 외래 키를 자동으로 처리해주어 좀 더 편리합니다:

```php
$posts = Post::whereBelongsTo($user)->get();
```

기본적으로 모델 클래스명에 기반해 관계를 추론하지만, 수동으로 관계명을 지정하려면 두 번째 인자로 넘길 수 있습니다:

```php
$posts = Post::whereBelongsTo($user, 'author')->get();
```

<a name="has-one-of-many"></a>
### Has One Of Many

가끔 모델이 여러 연관 모델을 가졌지만 가장 최신(latest) 또는 가장 오래된(oldest) 연관 모델 한 개만 쉽게 가져오고 싶은 경우가 있습니다. 예를 들어, `User`가 여러 `Order` 모델과 연관되어 있지만, 가장 최근 주문만 편리하게 불러오고 싶을 때 사용할 수 있습니다. `hasOne` 관계와 `ofMany` 메서드를 함께 사용합니다:

```php
/**
 * 사용자의 최신 주문을 가져옵니다.
 */
public function latestOrder()
{
    return $this->hasOne(Order::class)->latestOfMany();
}
```

반대로 가장 오래된 주문을 가져오는 메서드 예시:

```php
/**
 * 사용자의 가장 오래된 주문을 가져옵니다.
 */
public function oldestOrder()
{
    return $this->hasOne(Order::class)->oldestOfMany();
}
```

기본적으로 `latestOfMany`와 `oldestOfMany`는 모델의 기본 키(정렬 가능한 컬럼)를 기준으로 가장 최신 또는 오래된 모델을 가져옵니다. 컬럼이나 집계 함수(`min`, `max`)를 지정해 다른 기준으로 선택할 수도 있습니다:

```php
/**
 * 사용자의 가장 큰 주문을 가져옵니다.
 */
public function largestOrder()
{
    return $this->hasOne(Order::class)->ofMany('price', 'max');
}
```

> [!NOTE]
> PostgreSQL은 UUID 컬럼에는 `MAX` 함수를 지원하지 않으므로, PostgreSQL UUID 컬럼에 대해 one-of-many 관계를 사용할 수 없습니다.

<a name="advanced-has-one-of-many-relationships"></a>
#### 고급 Has One Of Many 관계

더 복잡한 조건을 가진 "has one of many" 관계를 만들 수 있습니다. 예를 들어, `Product` 모델에 여러 `Price` 모델이 있는데, 새 가격 정보를 `published_at` 컬럼으로 관리하며 미래 날짜까지 게시할 수 있습니다.

최신으로 게시된 가격 데이터 중에서, `published_at`이 미래가 아닌 것 중 가장 최신 및 ID가 가장 큰 가격을 가져오려면 다음과 같이 합니다:

```php
/**
 * 제품의 현재 가격을 가져옵니다.
 */
public function currentPricing()
{
    return $this->hasOne(Price::class)->ofMany([
        'published_at' => 'max',
        'id' => 'max',
    ], function ($query) {
        $query->where('published_at', '<', now());
    });
}
```

<a name="has-one-through"></a>
### Has One Through

"has-one-through" 관계는 세 번째 모델을 경유하여 다른 모델과 1:1 방식으로 관련되는 관계를 정의합니다.

예를 들어, 차량 수리점 애플리케이션에서 `Mechanic` 모델은 `Car` 모델과 1:1 관계고, `Car`는 `Owner` 모델과 1:1 관계입니다. 직접 `Mechanic`과 `Owner`는 연결되어 있지 않지만, `Mechanic` 모델에서 `Car` 모델을 통해 `Owner`에 접근할 수 있습니다. 관계에 필요한 테이블 구조는 다음과 같습니다:

```
mechanics
    id - integer
    name - string

cars
    id - integer
    model - string
    mechanic_id - integer

owners
    id - integer
    name - string
    car_id - integer
```

`Mechanic` 모델에 다음과 같이 정의합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Mechanic extends Model
{
    /**
     * 차의 소유자를 가져옵니다.
     */
    public function carOwner()
    {
        return $this->hasOneThrough(Owner::class, Car::class);
    }
}
```

`hasOneThrough`의 첫 번째 인자는 최종 액세스하려는 모델이고, 두 번째는 중간 모델입니다.

<a name="has-one-through-key-conventions"></a>
#### 키 규칙

Eloquent의 기본 외래 키 규칙이 적용됩니다. 원하는 경우 아래처럼 세 번째, 네 번째, 다섯 번째, 여섯 번째 인자로 각각 중간 모델 외래 키, 최종 모델 외래 키, 부모 모델 로컬 키, 중간 모델 로컬 키를 지정할 수 있습니다:

```php
class Mechanic extends Model
{
    /**
     * 차의 소유자를 가져옵니다.
     */
    public function carOwner()
    {
        return $this->hasOneThrough(
            Owner::class,
            Car::class,
            'mechanic_id', // cars 테이블의 외래 키
            'car_id', // owners 테이블의 외래 키
            'id', // mechanics 테이블 로컬 키
            'id' // cars 테이블 로컬 키
        );
    }
}
```

<a name="has-many-through"></a>
### Has Many Through

"has-many-through" 관계는 중간 관계를 통해 연관 모델에 접근하는 편리한 방법입니다.

예를 들어, `Project` 모델이 `Environment` 모델을 거쳐 여러 `Deployment` 모델과 연관될 수 있습니다. 이렇게 하면 프로젝트별 배포 기록을 쉽게 조회할 수 있습니다. 테이블 구조는 다음과 같습니다:

```
projects
    id - integer
    name - string

environments
    id - integer
    project_id - integer
    name - string

deployments
    id - integer
    environment_id - integer
    commit_hash - string
```

`Project` 모델 정의:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Project extends Model
{
    /**
     * 프로젝트의 모든 배포 기록을 가져옵니다.
     */
    public function deployments()
    {
        return $this->hasManyThrough(Deployment::class, Environment::class);
    }
}
```

`hasManyThrough` 첫 번째 인자는 최종 모델, 두 번째 인자는 중간 모델입니다.

`Deployment` 테이블은 `project_id` 컬럼이 없지만, `Environment`의 `project_id`를 활용해 관련 배포를 조회합니다.

<a name="has-many-through-key-conventions"></a>
#### 키 규칙

`hasOneThrough`와 마찬가지로, 외래 키와 로컬 키를 직접 지정하려면 세 번째부터 여섯 번째 인자에 순서대로 넣습니다:

```php
class Project extends Model
{
    public function deployments()
    {
        return $this->hasManyThrough(
            Deployment::class,
            Environment::class,
            'project_id', // environments 테이블 외래 키
            'environment_id', // deployments 테이블 외래 키
            'id', // projects 테이블 로컬 키
            'id' // environments 테이블 로컬 키
        );
    }
}
```

<a name="many-to-many"></a>
## N:M 관계 (Many To Many Relationships)

N:M 관계는 `hasOne`이나 `hasMany`보다 다소 복잡합니다. 예를 들어, 하나의 사용자가 여러 역할을 가질 수 있고, 하나의 역할이 여러 사용자에게 할당될 수 있는 경우입니다. 즉, 사용자는 여러 역할을 갖고, 역할도 여러 사용자와 공유됩니다.

<a name="many-to-many-table-structure"></a>
#### 테이블 구조

이 관계에는 보통 세 개의 데이터베이스 테이블이 필요합니다: `users`, `roles`, 중간 테이블인 `role_user`. 중간 테이블 이름은 관련 모델명 알파벳 순서로 정해지며, `user_id`, `role_id` 컬럼이 들어갑니다. 중간 테이블은 두 모델의 관계를 연결해줍니다.

`roles` 테이블에 `user_id` 컬럼을 넣으면 한 롤에 한 사람만 연결될 수 있기 때문에, 역할이 여러 사용자에게 할당되려면 별도 중간 테이블이 필요합니다:

```
users
    id - integer
    name - string

roles
    id - integer
    name - string

role_user
    user_id - integer
    role_id - integer
```

<a name="many-to-many-model-structure"></a>
#### 모델 정의

관계는 `belongsToMany` 메서드 반환값으로 정의합니다. 예를 들어 `User` 모델에 `roles` 메서드를 추가:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 사용자에게 할당된 역할들.
     */
    public function roles()
    {
        return $this->belongsToMany(Role::class);
    }
}
```

관계 정의 후에는 `roles` 동적 프로퍼티로 사용자 역할을 조회할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

foreach ($user->roles as $role) {
    //
}
```

관계 메서드를 직접 호출하면 쿼리에 조건 추가도 가능합니다:

```php
$roles = User::find(1)->roles()->orderBy('name')->get();
```

중간 테이블 이름은 기본적으로 관련 모델명 알파벳 순서로 만드나, 필요하면 두 번째 인자로 이름을 수동 지정할 수 있습니다:

```php
return $this->belongsToMany(Role::class, 'role_user');
```

중간 테이블의 외래 키명도 세 번째와 네 번째 인자로 직접 지정할 수 있습니다:

```php
return $this->belongsToMany(Role::class, 'role_user', 'user_id', 'role_id');
```

<a name="many-to-many-defining-the-inverse-of-the-relationship"></a>
#### 관계 역방향 정의하기

N:M 관계의 역방향도 `belongsToMany` 메서드로 정의합니다. `Role` 모델의 예를 봅시다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Role extends Model
{
    /**
     * 이 역할을 가진 사용자들.
     */
    public function users()
    {
        return $this->belongsToMany(User::class);
    }
}
```

관계 정의법은 `User` 모델의 `roles` 메서드 정의와 같으며, 인자도 동일하게 커스텀 가능함을 기억하세요.

<a name="retrieving-intermediate-table-columns"></a>
### 중간 테이블 컬럼 가져오기

N:M 관계에서, 중간 테이블 모델은 각 관련 모델에 자동으로 `pivot` 속성으로 포함됩니다:

```php
use App\Models\User;

$user = User::find(1);

foreach ($user->roles as $role) {
    echo $role->pivot->created_at;
}
```

`pivot` 모델에는 기본적으로 모델 키만 존재합니다. 추가 컬럼을 포함하려면 관계 정의 시 `withPivot` 메서드로 명시해야 합니다:

```php
return $this->belongsToMany(Role::class)->withPivot('active', 'created_by');
```

중간 테이블에 `created_at`, `updated_at` 타임스탬프를 자동으로 관리하려면 `withTimestamps` 메서드를 호출하세요:

```php
return $this->belongsToMany(Role::class)->withTimestamps();
```

> [!NOTE]
> 자동 타임스탬프를 쓰는 중간 테이블은 `created_at`과 `updated_at` 모두 컬럼에 반드시 있어야 합니다.

<a name="customizing-the-pivot-attribute-name"></a>
#### `pivot` 속성명 변경하기

중간 테이블 데이터를 담는 `pivot` 속성명을 더 의미 있게 변경할 수 있습니다. 예를 들어, 사용자가 팟캐스트를 구독하는 관계라면, `pivot` 대신 `subscription`으로 이름을 쓸 수 있습니다:

```php
return $this->belongsToMany(Podcast::class)
                ->as('subscription')
                ->withTimestamps();
```

이후 중간 테이블 데이터는 `subscription` 속성으로 접근합니다:

```php
$users = User::with('podcasts')->get();

foreach ($users->flatMap->podcasts as $podcast) {
    echo $podcast->subscription->created_at;
}
```

<a name="filtering-queries-via-intermediate-table-columns"></a>
### 중간 테이블 컬럼을 이용한 조건 필터링

`belongsToMany` 관계 조회 시 중간 테이블 컬럼으로 필터링하려면, 다음과 같은 메서드를 사용할 수 있습니다: `wherePivot`, `wherePivotIn`, `wherePivotNotIn`, `wherePivotBetween`, `wherePivotNotBetween`, `wherePivotNull`, `wherePivotNotNull` 등:

```php
return $this->belongsToMany(Role::class)
                ->wherePivot('approved', 1);

return $this->belongsToMany(Role::class)
                ->wherePivotIn('priority', [1, 2]);

return $this->belongsToMany(Role::class)
                ->wherePivotNotIn('priority', [1, 2]);

return $this->belongsToMany(Podcast::class)
                ->as('subscriptions')
                ->wherePivotBetween('created_at', ['2020-01-01 00:00:00', '2020-12-31 00:00:00']);

return $this->belongsToMany(Podcast::class)
                ->as('subscriptions')
                ->wherePivotNotBetween('created_at', ['2020-01-01 00:00:00', '2020-12-31 00:00:00']);

return $this->belongsToMany(Podcast::class)
                ->as('subscriptions')
                ->wherePivotNull('expired_at');

return $this->belongsToMany(Podcast::class)
                ->as('subscriptions')
                ->wherePivotNotNull('expired_at');
```

<a name="defining-custom-intermediate-table-models"></a>
### 커스텀 중간 테이블 모델 정의하기

중간 테이블을 위한 커스텀 모델을 만들고 싶다면 `using` 메서드를 사용하세요. 커스텀 피벗 모델은 `Illuminate\Database\Eloquent\Relations\Pivot` 클래스를, 다형성 피벗 모델은 `MorphPivot` 클래스를 상속해야 합니다. 예를 들어:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Role extends Model
{
    /**
     * 이 역할과 연결된 사용자들.
     */
    public function users()
    {
        return $this->belongsToMany(User::class)->using(RoleUser::class);
    }
}
```

커스텀 피벗 모델 정의:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Relations\Pivot;

class RoleUser extends Pivot
{
    //
}
```

> [!NOTE]
> 피벗 모델에 `SoftDeletes` 트레이트 사용은 불가합니다. 피벗 레코드에 소프트 삭제가 필요하면, 일반 Eloquent 모델로 전환하는 걸 고려하세요.

<a name="custom-pivot-models-and-incrementing-ids"></a>
#### 커스텀 피벗 모델과 자동 증가 ID

커스텀 피벗 모델에 자동 증가 기본 키가 있다면, 반드시 모델 내에 `public $incrementing = true;` 를 명시해야 합니다:

```php
/**
 * ID가 자동 증가 되는지 여부.
 *
 * @var bool
 */
public $incrementing = true;
```

<a name="polymorphic-relationships"></a>
## 다형성 관계 (Polymorphic Relationships)

다형성 관계는 자식 모델이 하나 이상의 서로 다른 타입의 부모 모델과 단일 관계로 연결될 수 있게 합니다. 예를 들어, `Comment` 모델이 `Post`, `Video` 두 모델에 모두 연결될 수 있습니다.

<a name="one-to-one-polymorphic-relations"></a>
### 1:1 다형성 (One To One Polymorphic)

<a name="one-to-one-polymorphic-table-structure"></a>
#### 테이블 구조

1:1 다형성 관계는 일반 1:1 관계와 비슷하지만, 자식 모델이 단일 연관 컬럼으로 여러 다른 모델 타입에 연결될 수 있다는 점이 다릅니다.

예를 들어, `Post`와 `User` 모델이 각각 유일한 이미지를 공유하는 `Image` 모델과 다형성 관계를 맺을 수 있습니다. 테이블 구조는 이렇게 생겼습니다:

```
posts
    id - integer
    name - string

users
    id - integer
    name - string

images
    id - integer
    url - string
    imageable_id - integer
    imageable_type - string
```

`images` 테이블의 `imageable_id` 컬럼은 `Post` 또는 `User`의 ID값을 저장하며, `imageable_type` 컬럼은 부모 모델의 클래스명을 담아 Eloquent가 반환할 모델 타입을 구분합니다 (`App\Models\Post` 또는 `App\Models\User`).

<a name="one-to-one-polymorphic-model-structure"></a>
#### 모델 정의

이 관계를 위한 모델 정의 예제:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Image extends Model
{
    /**
     * 이미지의 부모 모델(Post 또는 User).
     */
    public function imageable()
    {
        return $this->morphTo();
    }
}

class Post extends Model
{
    /**
     * 게시글의 이미지.
     */
    public function image()
    {
        return $this->morphOne(Image::class, 'imageable');
    }
}

class User extends Model
{
    /**
     * 사용자의 이미지.
     */
    public function image()
    {
        return $this->morphOne(Image::class, 'imageable');
    }
}
```

<a name="one-to-one-polymorphic-retrieving-the-relationship"></a>
#### 관계 조회하기

모델이 정의된 후에는 다음과 같이 접근합니다.

`Post` 모델의 이미지 조회:

```php
use App\Models\Post;

$post = Post::find(1);

$image = $post->image;
```

`Image` 모델의 부모 `Post` 혹은 `User` 조회:

```php
use App\Models\Image;

$image = Image::find(1);

$imageable = $image->imageable;
```

`imageable` 관계는 `Post` 또는 `User` 인스턴스를 반환합니다.

<a name="morph-one-to-one-key-conventions"></a>
#### 키 규칙

필요시 다형성 자식 모델에서 사용되는 `id`와 `type` 컬럼명을 명시할 수 있습니다. 이 경우 `morphTo` 메서드의 첫 번째 인자로 관계명(보통 메서드명)을 넘겨야 합니다:

```php
/**
 * 이미지의 부모 모델을 가져옵니다.
 */
public function imageable()
{
    return $this->morphTo(__FUNCTION__, 'imageable_type', 'imageable_id');
}
```

<a name="one-to-many-polymorphic-relations"></a>
### 1:N 다형성 (One To Many Polymorphic)

<a name="one-to-many-polymorphic-table-structure"></a>
#### 테이블 구조

1:N 다형성 관계는 일반 1:N 관계와 비슷하지만, 자식 모델이 단일 속성으로 여러 모델 타입에 연결됩니다.

예를 들어, 사용자가 게시글과 동영상에 댓글을 달 수 있는 상황에서, `comments` 테이블 하나로 `Post`와 `Video`에 대한 댓글을 저장할 수 있습니다:

```
posts
    id - integer
    title - string
    body - text

videos
    id - integer
    title - string
    url - string

comments
    id - integer
    body - text
    commentable_id - integer
    commentable_type - string
```

<a name="one-to-many-polymorphic-model-structure"></a>
#### 모델 정의

모델 예제:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Comment extends Model
{
    /**
     * 댓글의 부모 모델(Post 또는 Video).
     */
    public function commentable()
    {
        return $this->morphTo();
    }
}

class Post extends Model
{
    /**
     * 게시글의 모든 댓글.
     */
    public function comments()
    {
        return $this->morphMany(Comment::class, 'commentable');
    }
}

class Video extends Model
{
    /**
     * 동영상의 모든 댓글.
     */
    public function comments()
    {
        return $this->morphMany(Comment::class, 'commentable');
    }
}
```

<a name="one-to-many-polymorphic-retrieving-the-relationship"></a>
#### 관계 조회하기

모델 정의 후 동적 프로퍼티로 자식 모델 참조:

```php
use App\Models\Post;

$post = Post::find(1);

foreach ($post->comments as $comment) {
    //
}
```

자식 모델에서 부모 참조는 `commentable` 프로퍼티로 접근:

```php
use App\Models\Comment;

$comment = Comment::find(1);

$commentable = $comment->commentable;
```

`commentable` 관계는 `Post` 또는 `Video` 인스턴스를 반환합니다.

<a name="one-of-many-polymorphic-relations"></a>
### One Of Many 다형성 (One Of Many Polymorphic)

여러 연관 모델 중 최신 또는 가장 오래된 단일 모델을 조회하는 방법으로, `morphOne`과 `ofMany` 메서드를 결합해 사용할 수 있습니다.

예를 들어, `User`가 여러 `Image` 모델과 연관있지만, 가장 최근 이미지만 가져오는 관계:

```php
/**
 * 사용자의 최신 이미지.
 */
public function latestImage()
{
    return $this->morphOne(Image::class, 'imageable')->latestOfMany();
}
```

가장 오래된 이미지를 가져오는 경우:

```php
/**
 * 사용자의 가장 오래된 이미지.
 */
public function oldestImage()
{
    return $this->morphOne(Image::class, 'imageable')->oldestOfMany();
}
```

기본 키로 정렬하지만, 다르게 정렬 기준과 집계 함수를 지정할 수 있습니다:

```php
/**
 * 사용자의 가장 인기 있는 이미지.
 */
public function bestImage()
{
    return $this->morphOne(Image::class, 'imageable')->ofMany('likes', 'max');
}
```

> [!TIP]
> 더 복잡한 'one of many' 관계 정의법은 [has one of many 문서](#advanced-has-one-of-many-relationships)를 참고하세요.

<a name="many-to-many-polymorphic-relations"></a>
### N:M 다형성 (Many To Many Polymorphic)

<a name="many-to-many-polymorphic-table-structure"></a>
#### 테이블 구조

N:M 다형성 관계는 "morph one"이나 "morph many" 보다 더 복잡합니다. 예를 들어, `Post`와 `Video` 모델이 `Tag` 모델과 다형성 N:M 관계를 가질 때, `tags` 테이블 하나와 중간 테이블 `taggables`를 사용합니다:

```
posts
    id - integer
    name - string

videos
    id - integer
    name - string

tags
    id - integer
    name - string

taggables
    tag_id - integer
    taggable_id - integer
    taggable_type - string
```

> [!TIP]
> 다형성 N:M 관계 이전에 일반 N:M 관계 문서를 먼저 읽으면 도움이 됩니다.

<a name="many-to-many-polymorphic-model-structure"></a>
#### 모델 정의

`Post`와 `Video`는 둘 다 `tags` 메서드에 `morphToMany`를 사용합니다. 관계명은 중간 테이블 명과 키를 고려해 `"taggable"`로 설정합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Post extends Model
{
    /**
     * 게시글에 붙은 모든 태그.
     */
    public function tags()
    {
        return $this->morphToMany(Tag::class, 'taggable');
    }
}
```

<a name="many-to-many-polymorphic-defining-the-inverse-of-the-relationship"></a>
#### 관계 역방향 정의하기

`Tag` 모델에서는 부모 모델별 메서드 (`posts`, `videos`)를 각각 정의한 뒤 `morphedByMany`를 반환합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Tag extends Model
{
    /**
     * 이 태그가 붙은 게시글들.
     */
    public function posts()
    {
        return $this->morphedByMany(Post::class, 'taggable');
    }

    /**
     * 이 태그가 붙은 동영상들.
     */
    public function videos()
    {
        return $this->morphedByMany(Video::class, 'taggable');
    }
}
```

<a name="many-to-many-polymorphic-retrieving-the-relationship"></a>
#### 관계 조회하기

모델 정의 후 `Post`의 태그 조회:

```php
use App\Models\Post;

$post = Post::find(1);

foreach ($post->tags as $tag) {
    //
}
```

`Tag` 모델에서 부모 모델들을 참조:

```php
use App\Models\Tag;

$tag = Tag::find(1);

foreach ($tag->posts as $post) {
    //
}

foreach ($tag->videos as $video) {
    //
}
```

<a name="custom-polymorphic-types"></a>
### 커스텀 다형성 타입(Custom Polymorphic Types)

기본적으로 Laravel은 `commentable_type` 같은 다형성 타입 칼럼에 모델의 완전한 네임스페이스(`App\Models\Post`)를 저장합니다. 하지만 이를 분리해 간단한 문자열 별칭(`post`, `video`)을 사용할 수 있습니다. 이렇게 하면 모델 이름 변경 시에도 DB 값이 건전하게 유지됩니다:

```php
use Illuminate\Database\Eloquent\Relations\Relation;

Relation::enforceMorphMap([
    'post' => 'App\Models\Post',
    'video' => 'App\Models\Video',
]);
```

위 코드는 `App\Providers\AppServiceProvider`의 `boot` 메서드에 넣거나 별도의 서비스 프로바이더에 작성할 수 있습니다.

런타임에 별칭을 얻거나, 별칭을 통해 클래스명을 얻는 방법:

```php
use Illuminate\Database\Eloquent\Relations\Relation;

$alias = $post->getMorphClass();

$class = Relation::getMorphedModel($alias);
```

> [!NOTE]
> 기존 앱에 morph map을 추가할 경우, 다형성 타입 컬럼 내 기존 완전한 클래스명들은 모두 별칭으로 변경해야 합니다.

<a name="dynamic-relationships"></a>
### 동적 관계 (Dynamic Relationships)

`resolveRelationUsing` 메서드를 사용해 런타임에 Eloquent 모델 간 관계를 정의할 수 있습니다. 일반 앱 개발에는 권장되지 않지만, 패키지 개발 시 유용할 때가 있습니다.

첫 번째 인자는 관계 이름, 두 번째 인자는 클로저로 모델 인스턴스를 받고 유효한 관계 반환:

```php
use App\Models\Order;
use App\Models\Customer;

Order::resolveRelationUsing('customer', function ($orderModel) {
    return $orderModel->belongsTo(Customer::class, 'customer_id');
});
```

> [!NOTE]
> 동적 관계 정의 시, 항상 명시적으로 키 이름 인자를 전달하는 것이 좋습니다.

<a name="querying-relations"></a>
## 관계 쿼리하기 (Querying Relations)

Eloquent 관계는 모두 메서드로 정의되므로, 관계 모델을 즉시 조회하지 않고 관계 객체를 반환받아 추가 조건을 붙일 수 있습니다. 모든 관계는 [쿼리 빌더](/docs/{{version}}/queries) 역할도 수행합니다.

예를 들어, `User`가 여러 `Post` 모델과 연결된 상황:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 사용자의 모든 게시글.
     */
    public function posts()
    {
        return $this->hasMany(Post::class);
    }
}
```

`posts` 관계에 조건 추가:

```php
use App\Models\User;

$user = User::find(1);

$user->posts()->where('active', 1)->get();
```

Laravel 쿼리 빌더의 메서드를 모두 사용할 수 있으므로 문서 참고 바랍니다.

<a name="chaining-orwhere-clauses-after-relationships"></a>
#### 관계 뒤에 `orWhere` 체이닝 주의

아래처럼 관계 뒤에 `orWhere` 체이닝을 할 경우 주의하세요:

```php
$user->posts()
        ->where('active', 1)
        ->orWhere('votes', '>=', 100)
        ->get();
```

이 쿼리는 `user_id = ? AND active = 1 OR votes >= 100`로 해석되어, 특정 사용자와 상관없이 `votes >= 100` 조건도 포함되어 의도치 않은 결과를 낼 수 있습니다.

논리 그룹핑을 사용해 조건을 괄호로 감싸는 방식이 올바릅니다:

```php
use Illuminate\Database\Eloquent\Builder;

$user->posts()
        ->where(function (Builder $query) {
            return $query->where('active', 1)
                         ->orWhere('votes', '>=', 100);
        })
        ->get();
```

이를 통해 쿼리는 `user_id = ? AND (active = 1 OR votes >= 100)`로 정확한 결과를 냅니다.

<a name="relationship-methods-vs-dynamic-properties"></a>
### 관계 메서드 vs 동적 프로퍼티

추가 조건 없이 연관 모델을 단순 조회할 땐, 관계를 프로퍼티처럼 접근하는 것이 편리합니다:

```php
use App\Models\User;

$user = User::find(1);

foreach ($user->posts as $post) {
    //
}
```

동적 관계 프로퍼티는 "지연 로딩"되어, 프로퍼티 접근 시점에만 쿼리를 실행합니다. 미리 로딩할 경우 [지연로딩(eager loading)](#eager-loading) 사용이 권장됩니다.

<a name="querying-relationship-existence"></a>
### 관계 존재 여부 쿼리하기

특정 관계가 적어도 하나 이상 존재하는 모델만 조회할 수도 있습니다. 예를 들어, 댓글이 하나 이상 달린 게시글만 조회:

```php
use App\Models\Post;

// 댓글이 하나 이상 있는 게시글 조회
$posts = Post::has('comments')->get();
```

비교 연산자와 개수를 더 구체적으로 지정 가능:

```php
// 댓글이 3개 이상인 게시글
$posts = Post::has('comments', '>=', 3)->get();
```

점(.) 표기법으로 중첩 관계도 조회 가능:

```php
// 댓글 중 이미지가 하나 이상 있는 게시글
$posts = Post::has('comments.images')->get();
```

더 상세 조건을 걸 때는 `whereHas` 메서드를 사용합니다:

```php
use Illuminate\Database\Eloquent\Builder;

// 내용에 'code%'가 포함된 댓글이 최소 하나 이상 달린 게시글
$posts = Post::whereHas('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
})->get();

// 10개 이상의 조건 달성 댓글이 있는 게시글
$posts = Post::whereHas('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
}, '>=', 10)->get();
```

> [!NOTE]
> Eloquent는 데이터베이스가 다르면 관계 존재 여부를 쿼리할 수 없습니다. 같은 데이터베이스 내에서만 지원합니다.

<a name="inline-relationship-existence-queries"></a>
#### 단순 조건의 관계 존재 쿼리

단일 조건으로 관계 존재를 쿼리할 땐 `whereRelation`과 `whereMorphRelation` 메서드가 편리합니다:

```php
use App\Models\Post;

$posts = Post::whereRelation('comments', 'is_approved', false)->get();
```

연산자 지정도 가능합니다:

```php
$posts = Post::whereRelation(
    'comments', 'created_at', '>=', now()->subHour()
)->get();
```

<a name="querying-relationship-absence"></a>
### 관계 부재 여부 쿼리하기

반대로 관계가 없는 모델만 조회하고 싶다면 `doesntHave` 또는 `orDoesntHave` 메서드를 사용합니다:

```php
use App\Models\Post;

$posts = Post::doesntHave('comments')->get();
```

추가 조건을 걸 땐 `whereDoesntHave`를 활용:

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::whereDoesntHave('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
})->get();
```

중첩 관계도 점(.) 표기법으로 처리:

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::whereDoesntHave('comments.author', function (Builder $query) {
    $query->where('banned', 0);
})->get();
```

<a name="querying-morph-to-relationships"></a>
### Morph To 관계 쿼리하기

"morph to" 관계 존재/부재를 쿼리할 땐, `whereHasMorph`와 `whereDoesntHaveMorph` 메서드를 사용합니다. 첫 인자는 관계명, 두 번째는 포함할 모델 클래스 배열, 세 번째는 관계 쿼리를 조절하는 클로저입니다:

```php
use App\Models\Comment;
use App\Models\Post;
use App\Models\Video;
use Illuminate\Database\Eloquent\Builder;

// 제목에 'code%'가 포함된 Post 또는 Video에 속한 댓글 조회
$comments = Comment::whereHasMorph(
    'commentable',
    [Post::class, Video::class],
    function (Builder $query) {
        $query->where('title', 'like', 'code%');
    }
)->get();

// 제목에 'code%'가 포함된 Post가 아닌 댓글 조회
$comments = Comment::whereDoesntHaveMorph(
    'commentable',
    Post::class,
    function (Builder $query) {
        $query->where('title', 'like', 'code%');
    }
)->get();
```

두 번째 인자인 클로저는 `$type` 인자도 받을 수 있어, 모델 타입에 따른 동적 조건 설정도 가능합니다:

```php
use Illuminate\Database\Eloquent\Builder;

$comments = Comment::whereHasMorph(
    'commentable',
    [Post::class, Video::class],
    function (Builder $query, $type) {
        $column = $type === Post::class ? 'content' : 'title';

        $query->where($column, 'like', 'code%');
    }
)->get();
```

<a name="querying-all-morph-to-related-models"></a>
#### 모든 관련 모델 쿼리하기

모델 배열 대신 `"*"` 와일드카드를 넘기면, DB에서 모든 관련 타입을 조회해 조건을 실행합니다(추가 쿼리 발생):

```php
use Illuminate\Database\Eloquent\Builder;

$comments = Comment::whereHasMorph('commentable', '*', function (Builder $query) {
    $query->where('title', 'like', 'foo%');
})->get();
```

<a name="aggregating-related-models"></a>
## 관련 모델 집계 (Aggregating Related Models)

<a name="counting-related-models"></a>
### 관련 모델 개수 세기

모델을 로드하면서 별도로 관련 모델 수를 세고 싶을 땐 `withCount` 메서드를 사용합니다. 이때 `{relation}_count` 프로퍼티가 추가됩니다:

```php
use App\Models\Post;

$posts = Post::withCount('comments')->get();

foreach ($posts as $post) {
    echo $post->comments_count;
}
```

배열로 여러 관계도 한번에 집계 가능하며, 각 집계에 조건도 지정할 수 있습니다:

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::withCount(['votes', 'comments' => function (Builder $query) {
    $query->where('content', 'like', 'code%');
}])->get();

echo $posts[0]->votes_count;
echo $posts[0]->comments_count;
```

동일 관계에 여러 집계를 별칭(alias)으로 지정할 수도 있습니다:

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::withCount([
    'comments',
    'comments as pending_comments_count' => function (Builder $query) {
        $query->where('approved', false);
    },
])->get();

echo $posts[0]->comments_count;
echo $posts[0]->pending_comments_count;
```

<a name="deferred-count-loading"></a>
#### 지연 집계 로딩

이미 로드한 모델에 대해 추가로 집계 수를 로드하려면 `loadCount`를 사용합니다:

```php
$book = Book::first();

$book->loadCount('genres');
```

추가 조건이 필요하면 배열에 관계명과 클로저를 넘깁니다:

```php
$book->loadCount(['reviews' => function ($query) {
    $query->where('rating', 5);
}]);
```

<a name="relationship-counting-and-custom-select-statements"></a>
#### 커스텀 select 문과 집계 함수

`select`와 함께 쓸 때는 `withCount`를 `select` 후에 호출해야 합니다:

```php
$posts = Post::select(['title', 'body'])
                ->withCount('comments')
                ->get();
```

<a name="other-aggregate-functions"></a>
### 기타 집계 함수

`withCount` 외에, `withMin`, `withMax`, `withAvg`, `withSum`, `withExists` 메서드도 있고, `{relation}_{function}_{column}` 프로퍼티가 만들어집니다:

```php
use App\Models\Post;

$posts = Post::withSum('comments', 'votes')->get();

foreach ($posts as $post) {
    echo $post->comments_sum_votes;
}
```

별칭도 가능:

```php
$posts = Post::withSum('comments as total_comments', 'votes')->get();

foreach ($posts as $post) {
    echo $post->total_comments;
}
```

지연 로딩용 `loadSum` 같은 메서드도 제공됩니다:

```php
$post = Post::first();

$post->loadSum('comments', 'votes');
```

`select`와 함께 쓸 때는 집계 메서드를 `select` 다음에 호출하세요:

```php
$posts = Post::select(['title', 'body'])
                ->withExists('comments')
                ->get();
```

<a name="counting-related-models-on-morph-to-relationships"></a>
### Morph To 관계에서 관련 모델 수 세기

`MorphTo` 관계도 eager loading과 함께 관련 모델 별 집계를 지정할 수 있습니다. 예를 들어, `ActivityFeed` 모델이 `parentable`이라는 `morphTo` 관계를 가진다고 가정:

```php
use Illuminate\Database\Eloquent\Relations\MorphTo;

$activities = ActivityFeed::with([
    'parentable' => function (MorphTo $morphTo) {
        $morphTo->morphWithCount([
            Photo::class => ['tags'],
            Post::class => ['comments'],
        ]);
    }])->get();
```

이미 모델을 불러온 후 집계만 로드할 땐 `loadMorphCount`를 사용합니다:

```php
$activities = ActivityFeed::with('parentable')->get();

$activities->loadMorphCount('parentable', [
    Photo::class => ['tags'],
    Post::class => ['comments'],
]);
```

<a name="eager-loading"></a>
## 지연로딩 (Eager Loading)

관계를 프로퍼티로 접근하면 지연로딩(lazy loading) 방식으로 동작해, 접근할 때 관계 데이터가 DB에서 조회됩니다. 하지만 미리 관련 데이터를 함께 불러오는 "지연로딩"을 통하면 N+1 문제를 크게 줄일 수 있습니다.

예를 들어, `Book` 모델이 `Author`에 `belongsTo` 관계인 경우:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Book extends Model
{
    /**
     * 이 책을 쓴 저자를 가져옵니다.
     */
    public function author()
    {
        return $this->belongsTo(Author::class);
    }
}
```

기본 접근 시:

```php
use App\Models\Book;

$books = Book::all();

foreach ($books as $book) {
    echo $book->author->name;
}
```

25권의 책이 있으면 1(책) + 25(각 저자) = 26 쿼리를 실행합니다.

`with` 메서드로 지연로딩하면 2쿼리로 줄어듭니다:

```php
$books = Book::with('author')->get();

foreach ($books as $book) {
    echo $book->author->name;
}
```

실행되는 쿼리 예:

```sql
select * from books

select * from authors where id in (1, 2, 3, 4, 5, ...)
```

<a name="eager-loading-multiple-relationships"></a>
#### 여러 관계 지연로딩

여러 관계를 동시 지연로딩하려면 배열을 넘깁니다:

```php
$books = Book::with(['author', 'publisher'])->get();
```

<a name="nested-eager-loading"></a>
#### 중첩 관계 지연로딩

관계 내부 관계까지 지연로딩도 가능합니다:

```php
$books = Book::with('author.contacts')->get();
```

<a name="nested-eager-loading-morphto-relationships"></a>
#### `morphTo` 관계 내부 지연로딩

`morphTo` 관계의 개별 엔터티에 네스트 관계를 지연로딩하려면 `MorphTo`의 `morphWith` 메서드를 사용합니다.

예시 모델:

```php
<?php

use Illuminate\Database\Eloquent\Model;

class ActivityFeed extends Model
{
    /**
     * 활동 피드의 부모 레코드.
     */
    public function parentable()
    {
        return $this->morphTo();
    }
}
```

`Event`, `Photo`, `Post`가 `ActivityFeed`를 생성하며 각각 `calendar`, `tags`, `author` 관계를 가진다고 가정하면:

```php
use Illuminate\Database\Eloquent\Relations\MorphTo;

$activities = ActivityFeed::query()
    ->with(['parentable' => function (MorphTo $morphTo) {
        $morphTo->morphWith([
            Event::class => ['calendar'],
            Photo::class => ['tags'],
            Post::class => ['author'],
        ]);
    }])->get();
```

<a name="eager-loading-specific-columns"></a>
#### 특정 컬럼 지연로딩

관계에서 일부 컬럼만 조회하고 싶으면, 다음과 같이 지정합니다:

```php
$books = Book::with('author:id,name,book_id')->get();
```

> [!NOTE]
> ID 혹은 외래 키 컬럼은 반드시 함께 포함해야 합니다.

<a name="eager-loading-by-default"></a>
#### 기본적으로 지연로딩 하기

항상 일부 관계를 함께 로드하고 싶으면, 모델에 `$with` 속성에 관계명을 넣습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Book extends Model
{
    /**
     * 항상 함께 로드할 관계들.
     *
     * @var array
     */
    protected $with = ['author'];

    /**
     * 책의 저자.
     */
    public function author()
    {
        return $this->belongsTo(Author::class);
    }

    /**
     * 책 장르.
     */
    public function genre()
    {
        return $this->belongsTo(Genre::class);
    }
}
```

단일 쿼리 내에서 `$with` 아이템 일부를 빼려면 `without`:

```php
$books = Book::without('author')->get();
```

모든 `$with` 대신 특정 관계만 로드하려면 `withOnly` 사용:

```php
$books = Book::withOnly('genre')->get();
```

<a name="constraining-eager-loads"></a>
### 지연로딩 제약조건 걸기 (Constraining Eager Loads)

관계 지연로딩 시 추가 쿼리 조건도 가능합니다. `with`에 관계명과 조건 클로저를 연결한 배열을 넘기면 됩니다:

```php
use App\Models\User;

$users = User::with(['posts' => function ($query) {
    $query->where('title', 'like', '%code%');
}])->get();
```

순서를 주문하거나 조건도 자유롭게 추가할 수 있습니다:

```php
$users = User::with(['posts' => function ($query) {
    $query->orderBy('created_at', 'desc');
}])->get();
```

> [!NOTE]
> 제한적이라 `limit`과 `take` 메서드는 사용할 수 없습니다.

<a name="constraining-eager-loading-of-morph-to-relationships"></a>
#### `morphTo` 관계 제약 조건

`morphTo` 관계의 각 타입별 쿼리에 조건을 걸고 싶으면, `MorphTo`의 `constrain` 메서드를 이용합니다:

```php
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Relations\MorphTo;

$comments = Comment::with(['commentable' => function (MorphTo $morphTo) {
    $morphTo->constrain([
        Post::class => function (Builder $query) {
            $query->whereNull('hidden_at');
        },
        Video::class => function (Builder $query) {
            $query->where('type', 'educational');
        },
    ]);
}])->get();
```

이 예제는 공개된 게시글과 교육용 동영상만 지연로딩합니다.

<a name="lazy-eager-loading"></a>
### 지연로딩 후 로딩 (Lazy Eager Loading)

부모 모델을 이미 불러온 상태에서 관계를 지연로딩하고 싶을 때 `load`를 사용합니다:

```php
use App\Models\Book;

$books = Book::all();

if ($someCondition) {
    $books->load('author', 'publisher');
}
```

관계별 추가 조건도 가능합니다:

```php
$author->load(['books' => function ($query) {
    $query->orderBy('published_date', 'asc');
}]);
```

관계가 아직 로드되지 않았을 때만 로드하려면 `loadMissing` 사용:

```php
$book->loadMissing('author');
```

<a name="nested-lazy-eager-loading-morphto"></a>
#### 다중 레벨 지연로딩과 `morphTo`

`morphTo` 관계 및 각 타입별 관계도 지연로딩하려면 `loadMorph` 메서드를 씁니다:

```php
$activities = ActivityFeed::with('parentable')
    ->get()
    ->loadMorph('parentable', [
        Event::class => ['calendar'],
        Photo::class => ['tags'],
        Post::class => ['author'],
    ]);
```

<a name="preventing-lazy-loading"></a>
### 지연로딩 방지하기 (Preventing Lazy Loading)

성능 향상을 위해 지연로딩을 완전히 금지할 수도 있습니다. 이렇게 하려면 베이스 모델 클래스에서 `preventLazyLoading` 메서드를 호출하세요. 보통 `AppServiceProvider` 의 `boot` 메서드에서 설정합니다:

```php
use Illuminate\Database\Eloquent\Model;

/**
 * 부트스트랩 애플리케이션 서비스.
 *
 * @return void
 */
public function boot()
{
    Model::preventLazyLoading(! $this->app->isProduction());
}
```

지연로딩이 시도되면 `Illuminate\Database\LazyLoadingViolationException` 예외가 발생합니다.

이 예외를 로그로 처리하고 싶으면 `handleLazyLoadingViolationUsing` 메서드로 콜백 등록 가능:

```php
Model::handleLazyLoadingViolationUsing(function ($model, $relation) {
    $class = get_class($model);

    info("Attempted to lazy load [{$relation}] on model [{$class}].");
});
```

<a name="inserting-and-updating-related-models"></a>
## 연관 모델 삽입 및 갱신 (Inserting & Updating Related Models)

<a name="the-save-method"></a>
### `save` 메서드

이 방법을 통해 관계에 새 모델을 간단히 추가할 수 있습니다. 예를 들어, 게시글에 새 댓글을 추가할 때:

```php
use App\Models\Comment;
use App\Models\Post;

$comment = new Comment(['message' => 'A new comment.']);

$post = Post::find(1);

$post->comments()->save($comment);
```

`comments`를 동적 프로퍼티가 아닌 메서드로 호출했음을 주의하세요. `save`는 새 댓글 모델의 `post_id`를 자동으로 할당합니다.

여러 모델을 저장하려면 `saveMany`를 이용:

```php
$post = Post::find(1);

$post->comments()->saveMany([
    new Comment(['message' => 'A new comment.']),
    new Comment(['message' => 'Another new comment.']),
]);
```

`save`와 `saveMany`는 데이터베이스에 저장하지만, 이미 로드된 관계 컬렉션에는 새 모델을 자동 추가하지 않습니다. 관계를 다시 접근하려면 `refresh`를 호출해 모델을 재로딩하세요:

```php
$post->comments()->save($comment);

$post->refresh();

// 새 댓글도 포함된 모든 댓글
$post->comments;
```

<a name="the-push-method"></a>
#### 모델과 관계들 재귀적 저장

연관된 모든 모델과 관계를 한 번에 저장하고 싶으면 `push` 메서드를 사용:

```php
$post = Post::find(1);

$post->comments[0]->message = 'Message';
$post->comments[0]->author->name = 'Author Name';

$post->push();
```

<a name="the-create-method"></a>
### `create` 메서드

`save`와 달리 배열을 전달해 새 모델을 만들고 저장합니다. 새 모델을 반환합니다:

```php
use App\Models\Post;

$post = Post::find(1);

$comment = $post->comments()->create([
    'message' => 'A new comment.',
]);
```

복수 생성은 `createMany`:

```php
$post = Post::find(1);

$post->comments()->createMany([
    ['message' => 'A new comment.'],
    ['message' => 'Another new comment.'],
]);
```

`findOrNew`, `firstOrNew`, `firstOrCreate`, `updateOrCreate` 등의 메서드도 관계에서 모델 생성 및 업데이트에 활용 가능합니다.

> [!TIP]
> `create` 사용 전 [대량 할당(mass assignment)](/docs/{{version}}/eloquent#mass-assignment) 규칙을 반드시 숙지하세요.

<a name="updating-belongs-to-relationships"></a>
### Belongs To 관계 갱신하기

자식 모델이 새로운 부모 모델을 가리키도록 변경하려면 `associate` 메서드를 사용합니다. 예: `User` 모델이 `Account` 모델에 `belongsTo` 시:

```php
use App\Models\Account;

$account = Account::find(10);

$user->account()->associate($account);

$user->save();
```

부모 관계를 제거하려면 `dissociate` 메서드로 외래 키를 `null`로 설정:

```php
$user->account()->dissociate();

$user->save();
```

<a name="updating-many-to-many-relationships"></a>
### N:M 관계 갱신하기 (Many To Many Relationships)

<a name="attaching-detaching"></a>
#### 연결/분리 (Attaching / Detaching)

N:M 관계에서는 다음 메서드로 중간 테이블에 레코드 추가/삭제가 가능합니다:

```php
use App\Models\User;

$user = User::find(1);

$user->roles()->attach($roleId);
```

추가 데이터도 넘길 수 있습니다:

```php
$user->roles()->attach($roleId, ['expires' => $expires]);
```

분리하려면 `detach` 메서드 사용:

```php
// 특정 역할 분리
$user->roles()->detach($roleId);

// 모든 역할 분리
$user->roles()->detach();
```

배열도 인자로 받음:

```php
$user = User::find(1);

$user->roles()->detach([1, 2, 3]);

$user->roles()->attach([
    1 => ['expires' => $expires],
    2 => ['expires' => $expires],
]);
```

<a name="syncing-associations"></a>
#### 동기화 (Syncing Associations)

`sync` 메서드는 중간 테이블을 주어진 ID 배열에 맞춰 갱신합니다. 존재하지 않은 ID는 삭제됩니다:

```php
$user->roles()->sync([1, 2, 3]);
```

추가 데이터와 함께도 가능:

```php
$user->roles()->sync([1 => ['expires' => true], 2, 3]);
```

같은 피벗 값을 모든 ID에 넣으려면 `syncWithPivotValues` 사용:

```php
$user->roles()->syncWithPivotValues([1, 2, 3], ['active' => true]);
```

기존 ID 삭제 없이 추가 동기화 하려면 `syncWithoutDetaching`:

```php
$user->roles()->syncWithoutDetaching([1, 2, 3]);
```

<a name="toggling-associations"></a>
#### 토글 (Toggling Associations)

`toggle`은 주어진 ID가 연결되어 있으면 분리, 아니면 연결합니다:

```php
$user->roles()->toggle([1, 2, 3]);
```

<a name="updating-a-record-on-the-intermediate-table"></a>
#### 중간 테이블 레코드 수정

중간 테이블 레코드를 수정하려면 `updateExistingPivot` 메서드를 사용:

```php
$user = User::find(1);

$user->roles()->updateExistingPivot($roleId, [
    'active' => false,
]);
```

<a name="touching-parent-timestamps"></a>
## 부모 타임스탬프 자동 갱신 (Touching Parent Timestamps)

`belongsTo` 또는 `belongsToMany` 관계가 있을 때, 자식 모델 갱신 시 부모 모델의 `updated_at` 타임스탬프도 자동 갱신할 수 있습니다.

예를 들어, `Comment` 모델이 소유한 `Post` 모델의 타임스탬프를 댓글 수정 시 업데이트 하려면, 자식 모델에 `touches` 배열에 관계명을 넣습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Comment extends Model
{
    /**
     * 자동 갱신할 관계들.
     *
     * @var array
     */
    protected $touches = ['post'];

    /**
     * 댓글의 소유 게시글.
     */
    public function post()
    {
        return $this->belongsTo(Post::class);
    }
}
```

> [!NOTE]
> 부모 모델 타임스탬프는 자식 모델이 Eloquent의 `save` 메서드로 업데이트될 때만 갱신됩니다.