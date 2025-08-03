# Eloquent: 관계 (Eloquent: Relationships)

- [소개](#introduction)
- [관계 정의하기](#defining-relationships)
    - [일대일 / Has One](#one-to-one)
    - [일대다 / Has Many](#one-to-many)
    - [일대다 (역방향) / Belongs To](#one-to-many-inverse)
    - [Many 중 하나 Has One](#has-one-of-many)
    - [Has One Through](#has-one-through)
    - [Has Many Through](#has-many-through)
- [스코프 관계](#scoped-relationships)
- [다대다 관계](#many-to-many)
    - [중간 테이블 컬럼 조회](#retrieving-intermediate-table-columns)
    - [중간 테이블 컬럼으로 쿼리 필터링](#filtering-queries-via-intermediate-table-columns)
    - [중간 테이블 컬럼으로 쿼리 정렬](#ordering-queries-via-intermediate-table-columns)
    - [맞춤형 중간 테이블 모델 정의](#defining-custom-intermediate-table-models)
- [다형 관계 (Polymorphic Relationships)](#polymorphic-relationships)
    - [일대일](#one-to-one-polymorphic-relations)
    - [일대다](#one-to-many-polymorphic-relations)
    - [Many 중 하나 (One of Many)](#one-of-many-polymorphic-relations)
    - [다대다](#many-to-many-polymorphic-relations)
    - [사용자 정의 다형 타입](#custom-polymorphic-types)
- [동적 관계](#dynamic-relationships)
- [관계 쿼리하기](#querying-relations)
    - [관계 메서드와 동적 속성](#relationship-methods-vs-dynamic-properties)
    - [관계 존재 여부 쿼리](#querying-relationship-existence)
    - [관계 부재 여부 쿼리](#querying-relationship-absence)
    - [Morph To 관계 쿼리](#querying-morph-to-relationships)
- [관련 모델 집계](#aggregating-related-models)
    - [관련 모델 개수 세기](#counting-related-models)
    - [기타 집계 함수](#other-aggregate-functions)
    - [Morph To 관계의 관련 모델 개수 세기](#counting-related-models-on-morph-to-relationships)
- [Eager Loading (사전 로딩)](#eager-loading)
    - [Eager Load 제약 조건](#constraining-eager-loads)
    - [Lazy Eager Loading](#lazy-eager-loading)
    - [Lazy Loading 방지](#preventing-lazy-loading)
- [관계 모델 삽입 및 갱신](#inserting-and-updating-related-models)
    - [`save` 메서드](#the-save-method)
    - [`create` 메서드](#the-create-method)
    - [Belongs To 관계 갱신](#updating-belongs-to-relationships)
    - [다대다 관계 갱신](#updating-many-to-many-relationships)
- [부모 타임스탬프 터치하기](#touching-parent-timestamps)

<a name="introduction"></a>
## 소개 (Introduction)

데이터베이스 테이블은 서로 관계를 맺고 있는 경우가 많습니다. 예를 들어, 블로그 게시물은 여러 댓글을 가질 수 있고, 주문은 주문한 사용자와 관계가 있을 수 있습니다. Eloquent는 이러한 관계를 쉽게 관리하고 작업할 수 있도록 도와주며, 다양한 일반적인 관계 유형을 지원합니다:

<div class="content-list" markdown="1">

- [일대일 (One To One)](#one-to-one)
- [일대다 (One To Many)](#one-to-many)
- [다대다 (Many To Many)](#many-to-many)
- [Has One Through](#has-one-through)
- [Has Many Through](#has-many-through)
- [일대일(다형 관계) (One To One Polymorphic)](#one-to-one-polymorphic-relations)
- [일대다(다형 관계) (One To Many Polymorphic)](#one-to-many-polymorphic-relations)
- [다대다(다형 관계) (Many To Many Polymorphic)](#many-to-many-polymorphic-relations)

</div>

<a name="defining-relationships"></a>
## 관계 정의하기 (Defining Relationships)

Eloquent 관계는 Eloquent 모델 클래스의 메서드로 정의됩니다. 관계는 강력한 [쿼리 빌더](/docs/master/queries) 역할도 하기 때문에, 관계를 메서드로 정의하면 강력한 메서드 체이닝과 쿼리 기능을 활용할 수 있습니다. 예를 들어, `posts` 관계에서 다음과 같이 추가 조건을 체이닝할 수 있습니다:

```php
$user->posts()->where('active', 1)->get();
```

그러나 관계를 깊이 쓰기 전에, Eloquent가 지원하는 각 관계 유형을 어떻게 정의하는지 먼저 알아보겠습니다.

<a name="one-to-one"></a>
### 일대일 / Has One (One to One / Has One)

일대일 관계는 가장 기본적인 데이터베이스 관계 유형입니다. 예를 들어, `User` 모델이 하나의 `Phone` 모델과 연결될 수 있습니다. 이 관계를 정의하려면 `User` 모델에 `phone` 메서드를 만들고, 이 메서드는 `hasOne` 메서드를 호출하여 그 결과를 반환해야 합니다. `hasOne` 메서드는 모델의 기본 클래스인 `Illuminate\Database\Eloquent\Model`에서 사용 가능합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasOne;

class User extends Model
{
    /**
     * 사용자와 연관된 전화번호를 가져옵니다.
     */
    public function phone(): HasOne
    {
        return $this->hasOne(Phone::class);
    }
}
```

`hasOne` 메서드에 전달하는 첫 번째 인수는 관련 모델 클래스의 이름입니다. 관계가 정의된 후, Eloquent의 동적 속성(dynamic properties)를 통해 관련 레코드를 조회할 수 있습니다. 동적 속성은 관계 메서드를 마치 모델에 속성으로 정의된 것처럼 접근할 수 있게 해줍니다:

```php
$phone = User::find(1)->phone;
```

Eloquent는 기본적으로 부모 모델 이름을 기준으로 외래 키를 추론합니다. 이 경우, `Phone` 모델은 자동으로 `user_id` 외래 키를 가진 것으로 간주합니다. 이 규칙을 변경하고 싶다면 `hasOne` 메서드에 두 번째 인자로 외래 키 이름을 전달할 수 있습니다:

```php
return $this->hasOne(Phone::class, 'foreign_key');
```

또한, Eloquent는 외래 키가 부모의 기본 키 컬럼 값과 일치하는 값이어야 한다고 가정합니다. 즉, `Phone` 레코드의 `user_id` 칼럼에서 사용자의 `id` 값을 찾습니다. 만약 기본 키가 `id`가 아니거나 모델의 `$primaryKey` 속성을 사용하거나, 다른 로컬 키(local key)를 기준으로 관계를 정의하고 싶다면, `hasOne` 메서드에 세 번째 인자로 로컬 키를 지정할 수 있습니다:

```php
return $this->hasOne(Phone::class, 'foreign_key', 'local_key');
```

<a name="one-to-one-defining-the-inverse-of-the-relationship"></a>
#### 관계의 역방향 정의하기 (Defining the Inverse of the Relationship)

우리는 이제 `User` 모델에서 `Phone` 모델에 접근할 수 있습니다. 다음으로, `Phone` 모델에서 이 전화를 소유한 사용자를 접근할 수 있도록 관계를 정의해 보겠습니다. `hasOne` 관계 역은 `belongsTo` 메서드로 정의합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Phone extends Model
{
    /**
     * 이 전화번호를 소유한 사용자를 가져옵니다.
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }
}
```

`user` 메서드를 호출할 때, Eloquent는 `Phone` 모델의 `user_id` 컬럼에 일치하는 `id`를 가진 `User` 모델을 찾으려고 합니다.

외래 키 이름은 관계 메서드 이름에 `_id`를 붙이는 방식으로 기본 추론합니다. 따라서, 이 경우 `Phone` 모델이 `user_id` 컬럼을 가진다고 가정합니다. 만약 `Phone` 모델에서 외래 키가 `user_id`가 아니라면, `belongsTo` 메서드 두 번째 인자로 직접 외래 키 이름을 전달할 수 있습니다:

```php
/**
 * 이 전화번호를 소유한 사용자를 가져옵니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class, 'foreign_key');
}
```

부모 모델이 `id`를 기본 키로 사용하지 않거나 다른 컬럼을 통해 관계 모델을 찾고 싶다면, `belongsTo` 메서드 세 번째 인자로 부모 테이블의 키를 지정할 수 있습니다:

```php
/**
 * 이 전화번호를 소유한 사용자를 가져옵니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class, 'foreign_key', 'owner_key');
}
```

<a name="one-to-many"></a>
### 일대다 / Has Many (One to Many / Has Many)

일대다 관계는 단일 모델이 여러 자식 모델의 부모일 때 사용합니다. 예를 들어, 블로그 게시물에 댓글이 무수히 많을 수 있습니다. 다른 모든 Eloquent 관계처럼 일대다 관계도 모델의 메서드로 정의됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Post extends Model
{
    /**
     * 블로그 게시물의 댓글을 가져옵니다.
     */
    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class);
    }
}
```

Eloquent는 `Comment` 모델의 적절한 외래 키 컬럼을 자동으로 추론합니다. 규칙에 따라 부모 모델 이름을 스네이크 케이스로 바꾸고 뒤에 `_id`를 붙입니다. 이 예시에서는 `Comment` 모델에서 외래 키로 `post_id` 컬럼을 사용한다고 가정합니다.

관계 메서드가 정의되면, `comments` 동적 속성으로 댓글 컬렉션([컬렉션](/docs/master/eloquent-collections))을 조회할 수 있습니다:

```php
use App\Models\Post;

$comments = Post::find(1)->comments;

foreach ($comments as $comment) {
    // ...
}
```

모든 관계는 쿼리 빌더 역할도 하므로, 관계 메서드를 호출하고 추가 조건을 체이닝할 수도 있습니다:

```php
$comment = Post::find(1)->comments()
    ->where('title', 'foo')
    ->first();
```

`hasOne` 메서드와 마찬가지로, `hasMany` 메서드에도 추가 인자를 넣어 외래 키와 로컬 키를 재정의할 수 있습니다:

```php
return $this->hasMany(Comment::class, 'foreign_key');

return $this->hasMany(Comment::class, 'foreign_key', 'local_key');
```

<a name="automatically-hydrating-parent-models-on-children"></a>
#### 자식 모델에서 부모 자동 하이드레이팅 (Automatically Hydrating Parent Models on Children)

Eager loading을 사용해도 자식 모델을 루프하면서 해당 자식의 부모 모델에 접근하면 "N + 1" 쿼리 문제가 발생할 수 있습니다:

```php
$posts = Post::with('comments')->get();

foreach ($posts as $post) {
    foreach ($post->comments as $comment) {
        echo $comment->post->title;
    }
}
```

위 코드에서, 모든 `Post`에 대한 댓글을 eager 로딩했음에도 불구하고, `Comment` 각 인스턴스에서 다시 `post` 관계를 조회하는 쿼리가 추가 발생합니다. 이는 부모 `Post` 모델이 각 자식 `Comment` 모델에 자동으로 배정되지 않기 때문입니다.

이 상황을 해결하고 싶다면, `hasMany` 관계 정의 시 `chaperone` 메서드를 호출하여 부모 모델을 자식 모델에 자동 하이드레이팅할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Post extends Model
{
    /**
     * 블로그 게시물의 댓글을 가져옵니다.
     */
    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class)->chaperone();
    }
}
```

런타임에서 자동 하이드레이팅을 선택하려면, eager loading 시 `chaperone` 메서드를 호출할 수도 있습니다:

```php
use App\Models\Post;

$posts = Post::with([
    'comments' => fn ($comments) => $comments->chaperone(),
])->get();
```

<a name="one-to-many-inverse"></a>
### 일대다 (역방향) / Belongs To (One to Many (Inverse) / Belongs To)

이제 하나의 게시물이 여러 댓글을 가질 수 있으므로, 댓글에서 해당 게시물을 참조할 수 있도록 역방향 관계를 정의해 봅시다. `hasMany`의 역은 `belongsTo` 메서드로 정의합니다. 자식 모델에 다음과 같이 작성합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Comment extends Model
{
    /**
     * 이 댓글이 속한 게시물을 가져옵니다.
     */
    public function post(): BelongsTo
    {
        return $this->belongsTo(Post::class);
    }
}
```

정의된 후에는, 댓글 모델에서 `post` 동적 속성으로 부모 게시물을 쉽게 조회할 수 있습니다:

```php
use App\Models\Comment;

$comment = Comment::find(1);

return $comment->post->title;
```

이때, Eloquent는 `Comment` 테이블의 `post_id` 컬럼 값을 보고, `Post` 모델의 기본 키(`id`)와 매칭되는 레코드를 찾습니다.

외래 키명은 기본적으로 관계 메서드 이름 뒤에 부모 모델 기본 키 컬럼명 앞에 `_`가 붙는 형태로 추론됩니다. 예: `post_id`.

규칙과 다르면, 두 번째 인자로 외래 키 이름을 지정할 수 있습니다:

```php
/**
 * 이 댓글이 속한 게시물을 가져옵니다.
 */
public function post(): BelongsTo
{
    return $this->belongsTo(Post::class, 'foreign_key');
}
```

기본 키가 `id`가 아니거나 다른 컬럼 기준으로 찾고 싶다면 세 번째 인자로 부모 테이블의 키 컬럼명을 넘깁니다:

```php
/**
 * 이 댓글이 속한 게시물을 가져옵니다.
 */
public function post(): BelongsTo
{
    return $this->belongsTo(Post::class, 'foreign_key', 'owner_key');
}
```

<a name="default-models"></a>
#### 기본 모델 설정 (Default Models)

`belongsTo`, `hasOne`, `hasOneThrough`, `morphOne` 관계에서는 관계가 `null`일 때 반환할 기본 모델을 지정할 수 있습니다. 이는 [Null Object 패턴](https://en.wikipedia.org/wiki/Null_Object_pattern)으로, 코드 내 조건 분기를 줄여줍니다.

예를 들어, `Post` 모델에 연결된 `user` 관계가 없을 때도 빈 `App\Models\User` 인스턴스를 반환하도록 정의할 수 있습니다:

```php
/**
 * 게시물 작성자를 가져옵니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault();
}
```

기본 모델에 속성을 채우려면 배열이나 클로저를 전달할 수 있습니다:

```php
/**
 * 게시물 작성자를 가져옵니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault([
        'name' => 'Guest Author',
    ]);
}

/**
 * 게시물 작성자를 가져옵니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault(function (User $user, Post $post) {
        $user->name = 'Guest Author';
    });
}
```

<a name="querying-belongs-to-relationships"></a>
#### Belongs To 관계 조회하기 (Querying Belongs To Relationships)

자식 모델에서 부모의 자식 모델들을 직접 조회하려면 수동으로 `where`절을 구성할 수 있습니다:

```php
use App\Models\Post;

$posts = Post::where('user_id', $user->id)->get();
```

더 편리하게는 `whereBelongsTo` 메서드를 이용할 수 있습니다. 해당 부모 모델과 올바른 외래 키를 자동으로 찾습니다:

```php
$posts = Post::whereBelongsTo($user)->get();
```

`whereBelongsTo`는 컬렉션도 받으며, 컬렉션에 포함된 어떤 부모와도 관계된 자식 모델들을 조회할 수 있습니다:

```php
$users = User::where('vip', true)->get();

$posts = Post::whereBelongsTo($users)->get();
```

기본적으로 부모 모델 클래스명을 통해 관계명을 추론하지만, 두 번째 인자로 관계명도 지정할 수 있습니다:

```php
$posts = Post::whereBelongsTo($user, 'author')->get();
```

<a name="has-one-of-many"></a>
### Many 중 하나 Has One (Has One of Many)

가끔 하나의 부모 모델이 여러 자식 모델이 있어도, 최신 혹은 가장 오래된 단일 자식 모델만 쉽게 접근하고 싶을 때가 있습니다.

예를 들어, `User`가 여러 `Order`를 갖지만, 가장 최근 주문에만 편리하게 접근하고 싶을 때 `hasOne` 타입 관계와 `ofMany` 메서드를 활용할 수 있습니다:

```php
/**
 * 사용자의 가장 최신 주문을 가져옵니다.
 */
public function latestOrder(): HasOne
{
    return $this->hasOne(Order::class)->latestOfMany();
}
```

반대로 가장 오래된 주문을 조회하는 메서드도 정의할 수 있습니다:

```php
/**
 * 사용자의 가장 오래된 주문을 가져옵니다.
 */
public function oldestOrder(): HasOne
{
    return $this->hasOne(Order::class)->oldestOfMany();
}
```

기본적으로 `latestOfMany`와 `oldestOfMany`는 모델의 정렬 가능한 기본 키 컬럼을 기준으로 최신/최단 관계 모델을 조회합니다. 하지만 다른 정렬 기준을 쓰고 싶다면 `ofMany`를 다음과 같이 사용하세요. 예를 들어 가장 비싼 주문을 가져오기:

```php
/**
 * 사용자의 최고가 주문을 가져옵니다.
 */
public function largestOrder(): HasOne
{
    return $this->hasOne(Order::class)->ofMany('price', 'max');
}
```

> [!WARNING]
> PostgreSQL의 UUID 컬럼에 `MAX` 함수 실행이 지원되지 않기 때문에, 현재 이 조합은 사용할 수 없습니다.

<a name="converting-many-relationships-to-has-one-relationships"></a>
#### 다대다 관계를 Has One 관계로 전환하기 (Converting "Many" Relationships to Has One Relationships)

`latestOfMany`, `oldestOfMany`, `ofMany` 등으로 하나의 모델만 조회할 때, 이미 동일 모델에 대한 "has many" 관계가 정의된 경우가 많습니다.

이럴 때 기존 "has many" 관계에서 `one` 메서드를 호출하면 쉽게 "has one" 관계로 변환할 수 있습니다:

```php
/**
 * 사용자의 여러 주문
 */
public function orders(): HasMany
{
    return $this->hasMany(Order::class);
}

/**
 * 사용자의 가장 큰 주문
 */
public function largestOrder(): HasOne
{
    return $this->orders()->one()->ofMany('price', 'max');
}
```

`HasManyThrough` 관계도 마찬가지로 `one` 메서드를 이용해 `HasOneThrough` 관계로 변환할 수 있습니다:

```php
public function latestDeployment(): HasOneThrough
{
    return $this->deployments()->one()->latestOfMany();
}
```

<a name="advanced-has-one-of-many-relationships"></a>
#### 고급 Many 중 하나 Has One 관계 (Advanced Has One of Many Relationships)

더 복잡한 케이스도 처리할 수 있습니다. 예를 들어, `Product` 모델이 여러 `Price` 모델을 가질 수 있는데, 새 가격은 미래 발행일로 예약할 수 있다고 가정해봅시다.

즉, 미래 날짜가 아닌 최근 발행 가격을 가져오면서, 발행일이 같을 때는 `id`가 더 큰 가격을 우선 반환해야 합니다.

이럴 때 `ofMany`의 첫 인자로 정렬할 컬럼들을 배열로 넘기고, 두 번째 인자로 더 자세한 조건을 쿼리할 클로저를 전달합니다:

```php
/**
 * 현재 제품 가격을 가져옵니다.
 */
public function currentPricing(): HasOne
{
    return $this->hasOne(Price::class)->ofMany([
        'published_at' => 'max',
        'id' => 'max',
    ], function (Builder $query) {
        $query->where('published_at', '<', now());
    });
}
```

<a name="has-one-through"></a>
### Has One Through

"has-one-through" 관계는 일대일 관계지만, 중간에 또 다른 모델을 거쳐 최종 모델과 연결되는 경우를 뜻합니다.

예를 들어, 자동차 수리점 애플리케이션에서 `Mechanic` 모델은 한 대의 `Car` 모델과, `Car` 모델은 한 명의 `Owner` 모델과 연관되며, 직접 DB 관계는 없지만 `Mechanic`에서 `Owner`에게 접근하려는 상황입니다.

관계 정의에 필요한 테이블은 다음과 같습니다:

```text
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

`Mechanic` 모델에서 관계를 정의해봅니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasOneThrough;

class Mechanic extends Model
{
    /**
     * 자동차의 소유주를 가져옵니다.
     */
    public function carOwner(): HasOneThrough
    {
        return $this->hasOneThrough(Owner::class, Car::class);
    }
}
```

`hasOneThrough` 메서드 첫 번째 인자는 최종 모델(`Owner`), 두 번째 인자는 중간 모델(`Car`)의 클래스명입니다.

이미 각 모델에 관련 관계가 정의되어 있다면, `through` 메서드로 연결하여 아래처럼 간단히 정의할 수 있습니다:

```php
// 문자열 기반 문법...
return $this->through('cars')->has('owner');

// 동적 메서드 문법...
return $this->throughCars()->hasOwner();
```

<a name="has-one-through-key-conventions"></a>
#### 키 규칙 (Key Conventions)

관계 쿼리는 일반적인 Eloquent 외래 키 규칙을 따릅니다. 필요하다면, `hasOneThrough`의 세 번째부터 여섯 번째 인자로 키를 사용자 지정할 수 있습니다:

```php
class Mechanic extends Model
{
    /**
     * 자동차 소유주를 가져옵니다.
     */
    public function carOwner(): HasOneThrough
    {
        return $this->hasOneThrough(
            Owner::class,
            Car::class,
            'mechanic_id', // 중간 테이블 외래 키 (cars 테이블)
            'car_id', // 최종 테이블 외래 키 (owners 테이블)
            'id', // 로컬 키 (mechanics 테이블)
            'id' // 중간 테이블 로컬 키 (cars 테이블)
        );
    }
}
```

앞서 처럼 모든 모델에 이미 관계가 정의되어 있으면 `through`로 부드럽게 연결하세요:

```php
// 문자열 기반 문법...
return $this->through('cars')->has('owner');

// 동적 메서드 문법...
return $this->throughCars()->hasOwner();
```

<a name="has-many-through"></a>
### Has Many Through

"has-many-through" 관계는 중간 모델을 통해 최종적으로 여러 모델에 접근할 때 사용되는 편리한 관계입니다.

예를 들어, `Application` 모델이 있고, 중간에 `Environment` 모델을 거쳐 여러 `Deployment` 모델에 접근할 수 있다고 가정합니다. 즉, 특정 애플리케이션에 대한 모든 배포를 쉽게 모을 수 있습니다.

테이블 구조는 다음과 같습니다:

```text
applications
    id - integer
    name - string

environments
    id - integer
    application_id - integer
    name - string

deployments
    id - integer
    environment_id - integer
    commit_hash - string
```

`Application` 모델에서 다음과 같이 관계를 정의합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasManyThrough;

class Application extends Model
{
    /**
     * 애플리케이션의 모든 배포를 가져옵니다.
     */
    public function deployments(): HasManyThrough
    {
        return $this->hasManyThrough(Deployment::class, Environment::class);
    }
}
```

`hasManyThrough` 첫 번째 인자는 최종 모델 `Deployment`, 두 번째 인자는 중간 모델 `Environment`입니다.

이미 관련 모든 모델에 관계가 정의되어 있으면, `through` 메서드로 편리하게 연결할 수 있습니다:

```php
// 문자열 기반 문법...
return $this->through('environments')->has('deployments');

// 동적 문법...
return $this->throughEnvironments()->hasDeployments();
```

`Deployment` 테이블엔 `application_id` 컬럼이 없지만, `hasManyThrough` 관계 덕분에 `$application->deployments`로 쉽게 접근할 수 있습니다. Eloquent는 `Environment` 테이블의 `application_id`를 참조하여 관련 환경 ID를 찾아, `Deployment`에서 다시 쿼리합니다.

<a name="has-many-through-key-conventions"></a>
#### 키 규칙 (Key Conventions)

Eloquent 외래 키 규칙에 따라 쿼리가 생성됩니다. 필요시, 아래 인자를 `hasManyThrough`에 전달하여 키를 변경할 수 있습니다:

```php
class Application extends Model
{
    public function deployments(): HasManyThrough
    {
        return $this->hasManyThrough(
            Deployment::class,
            Environment::class,
            'application_id', // 중간 테이블 외래 키 (environments)
            'environment_id', // 최종 테이블 외래 키 (deployments)
            'id', // 로컬 키 (applications)
            'id' // 중간 테이블 로컬 키 (environments)
        );
    }
}
```

이미 관련 관계가 정의되어 있다면 `through` 메서드로 연결하면 키 규칙도 재사용 가능합니다:

```php
// 문자열 기반 문법...
return $this->through('environments')->has('deployments');

// 동적 메서드 문법...
return $this->throughEnvironments()->hasDeployments();
```

<a name="scoped-relationships"></a>
### 스코프 관계 (Scoped Relationships)

관계 정의에 추가 조건을 넣는 일이 자주 있습니다.

예를 들어, `User` 모델에 `posts` 관계 외에, 특정 조건(예: `featured`)으로 제한된 `featuredPosts` 관계를 만드려면 다음과 같이 정의할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class User extends Model
{
    /**
     * 사용자의 글 가져오기
     */
    public function posts(): HasMany
    {
        return $this->hasMany(Post::class)->latest();
    }

    /**
     * 사용자의 대표 게시물 가져오기
     */
    public function featuredPosts(): HasMany
    {
        return $this->posts()->where('featured', true);
    }
}
```

하지만, 이렇게 정의한 관계를 통해 생성(create)할 때는 `featured` 값이 자동으로 `true`가 설정되지 않습니다.

이 경우, `withAttributes` 메서드를 사용해 관계를 생성할 때 항상 추가할 속성을 지정할 수 있습니다:

```php
/**
 * 사용자의 대표 게시물 가져오기
 */
public function featuredPosts(): HasMany
{
    return $this->posts()->withAttributes(['featured' => true]);
}
```

`withAttributes`는 쿼리 조건에도 추가되고, 관계를 통해 새로 생성하는 모델에도 지정한 속성을 넣어줍니다:

```php
$post = $user->featuredPosts()->create(['title' => 'Featured Post']);

$post->featured; // true
```

<a name="many-to-many"></a>
## 다대다 관계 (Many to Many Relationships)

다대다 관계는 `hasOne`, `hasMany`보다 조금 복잡합니다. 예를 들어, 사용자는 여러 역할(roles)을 가질 수 있고, 각 역할은 여러 사용자에게 할당될 수 있습니다. 즉, 사용자와 역할이 다대다 관계로 연결되어 있습니다.

<a name="many-to-many-table-structure"></a>
#### 테이블 구조 (Table Structure)

`users`, `roles`, `role_user` 세 테이블이 필요합니다. `role_user` 테이블은 `roles`와 `users`를 연결하는 중간 테이블로, 알파벳 순서대로 `role_user`라 명명하며 `user_id`, `role_id` 컬럼을 갖습니다.

역할 이 한 명의 사용자에만 할당 가능하도록 `roles` 테이블에 `user_id` 컬럼을 둬서 일대다 관계처럼 만들 수 없습니다. 다대다 관계를 지원하려면 중간 테이블이 필요합니다.

```text
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
#### 모델 구조 (Model Structure)

다대다 관계는 모델 메서드에 `belongsToMany` 메서드 호출을 반환하여 정의합니다. `belongsToMany`는 모든 Eloquent 모델 베이스 클래스에서 사용 가능합니다.

예를 들어, `User` 모델에 `roles` 메서드를 만듭니다. 첫 번째 인자로 관련 모델 클래스명을 전달합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class User extends Model
{
    /**
     * 사용자가 가진 역할들.
     */
    public function roles(): BelongsToMany
    {
        return $this->belongsToMany(Role::class);
    }
}
```

관계가 정의된 뒤 동적 속성으로 역할들을 조회할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

foreach ($user->roles as $role) {
    // ...
}
```

모든 관계는 쿼리 빌더로 동작하므로 추가 조건을 체인할 수도 있습니다:

```php
$roles = User::find(1)->roles()->orderBy('name')->get();
```

관계의 중간 테이블 이름은 관련된 모델 이름의 알파벳 순으로 지정하지만, `belongsToMany` 두 번째 인자로 직접 지정할 수 있습니다:

```php
return $this->belongsToMany(Role::class, 'role_user');
```

중간 테이블 외래 키 컬럼명도 세 번째 및 네 번째 인자로 사용자 지정 가능합니다. 세 번째 인자는 현재 모델에 대한 외래 키, 네 번째는 연결할 모델에 대한 외래 키입니다:

```php
return $this->belongsToMany(Role::class, 'role_user', 'user_id', 'role_id');
```

<a name="many-to-many-defining-the-inverse-of-the-relationship"></a>
#### 역방향 관계 정의하기 (Defining the Inverse of the Relationship)

다대다 관계의 역방향도 마찬가지로 관련 모델에 `belongsToMany`를 호출하는 메서드를 정의하여 만듭니다.

예를 들어, `Role` 모델에 사용자들을 반환하는 `users` 메서드를 만듭니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class Role extends Model
{
    /**
     * 이 역할에 속한 사용자들.
     */
    public function users(): BelongsToMany
    {
        return $this->belongsToMany(User::class);
    }
}
```

기본 설정과 동일하며, 관련 테이블과 키 사용자 지정도 동일하게 적용할 수 있습니다.

<a name="retrieving-intermediate-table-columns"></a>
### 중간 테이블 컬럼 조회 (Retrieving Intermediate Table Columns)

다대다 관계는 중간 테이블을 사용하는 만큼, 중간 테이블 데이터를 조회할 필요가 있습니다.

예를 들어, `User`가 여러 `Role`을 갖는 상황에서 중간 테이블 컬럼을 참조할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

foreach ($user->roles as $role) {
    echo $role->pivot->created_at;
}
```

각 `Role` 모델에 자동으로 `pivot` 속성이 부여되며, 이 객체가 중간 테이블 모델을 나타냅니다.

기본적으로는 중간 테이블의 키 값만 포함되므로, 추가 속성이 있다면 `withPivot` 메서드로 명시하세요:

```php
return $this->belongsToMany(Role::class)->withPivot('active', 'created_by');
```

중간 테이블에 `created_at`, `updated_at` 타임스탬프를 자동 관리하려면 `withTimestamps` 메서드를 호출합니다:

```php
return $this->belongsToMany(Role::class)->withTimestamps();
```

> [!WARNING]  
> 중간 테이블에 자동 타임스탬프를 사용하려면, `created_at`과 `updated_at` 두 컬럼 모두 있어야 합니다.

<a name="customizing-the-pivot-attribute-name"></a>
#### `pivot` 속성 이름 변경하기 (Customizing the `pivot` Attribute Name)

기본적으로 중간 테이블 정보는 `pivot` 속성으로 접근하지만, 이 이름을 업무 목적에 맞게 변경할 수 있습니다.

예를 들어, 사용자가 팟캐스트를 구독하는 다대다 관계를 만들었을 때 `subscription`으로 이름을 바꿀 수 있습니다:

```php
return $this->belongsToMany(Podcast::class)
    ->as('subscription')
    ->withTimestamps();
```

이후 중간 테이블 데이터는 다음과 같이 접근합니다:

```php
$users = User::with('podcasts')->get();

foreach ($users->flatMap->podcasts as $podcast) {
    echo $podcast->subscription->created_at;
}
```

<a name="filtering-queries-via-intermediate-table-columns"></a>
### 중간 테이블 컬럼으로 쿼리 필터링 (Filtering Queries via Intermediate Table Columns)

`belongsToMany` 관계 쿼리를 중간 테이블 칼럼 조건으로 필터링하려면 여러 메서드를 활용할 수 있습니다:

- `wherePivot`  
- `wherePivotIn`  
- `wherePivotNotIn`  
- `wherePivotBetween`  
- `wherePivotNotBetween`  
- `wherePivotNull`  
- `wherePivotNotNull`

예제:

```php
return $this->belongsToMany(Role::class)
    ->wherePivot('approved', 1);

return $this->belongsToMany(Role::class)
    ->wherePivotIn('priority', [1, 2]);

return $this->belongsToMany(Podcast::class)
    ->as('subscriptions')
    ->wherePivotBetween('created_at', ['2020-01-01 00:00:00', '2020-12-31 00:00:00']);

return $this->belongsToMany(Podcast::class)
    ->as('subscriptions')
    ->wherePivotNull('expired_at');
```

`wherePivot`는 조회 조건만 추가할 뿐, 관계를 생성할 때 해당 값이 자동으로 삽입되지는 않습니다. 조회와 생성 시 모두 특정 pivot 값을 적용하려면 `withPivotValue`를 사용하세요:

```php
return $this->belongsToMany(Role::class)
    ->withPivotValue('approved', 1);
```

<a name="ordering-queries-via-intermediate-table-columns"></a>
### 중간 테이블 컬럼으로 쿼리 정렬하기 (Ordering Queries via Intermediate Table Columns)

`orderByPivot` 메서드로 중간 테이블 컬럼을 기준으로 정렬할 수 있습니다. 예를 들어, 사용자의 최신 배지를 조회:

```php
return $this->belongsToMany(Badge::class)
    ->where('rank', 'gold')
    ->orderByPivot('created_at', 'desc');
```

<a name="defining-custom-intermediate-table-models"></a>
### 사용자 정의 중간 테이블 모델 정의하기 (Defining Custom Intermediate Table Models)

중간 테이블에 로직을 추가하거나 속성을 조작하고 싶다면, 사용자 정의 피벗 모델을 사용할 수 있습니다.

관계 정의 시 `using` 메서드를 호출하며, 해당 클래스는 `Illuminate\Database\Eloquent\Relations\Pivot` 클래스를 상속해야 합니다.

예를 들어 `Role` 모델에 사용자들 관계를 정의하면서 사용자 정의 `RoleUser` 피벗 모델을 지정:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class Role extends Model
{
    /**
     * 이 역할에 속한 사용자들.
     */
    public function users(): BelongsToMany
    {
        return $this->belongsToMany(User::class)->using(RoleUser::class);
    }
}
```

`RoleUser` 피벗 모델:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Relations\Pivot;

class RoleUser extends Pivot
{
    // 사용자 정의 동작 구현
}
```

> [!WARNING]  
> 피벗 모델에서 `SoftDeletes` 트레이트를 사용할 수 없습니다. 소프트 삭제가 필요하면 일반 Eloquent 모델로 변환하세요.

<a name="custom-pivot-models-and-incrementing-ids"></a>
#### 사용자 정의 피벗 모델과 자동 증가 ID (Custom Pivot Models and Incrementing IDs)

사용자 정의 피벗 모델에 자동 증가 기본 키가 있다면, `public $incrementing = true;`를 명시해야 합니다:

```php
/**
 * 자동 증가 여부 표시.
 *
 * @var bool
 */
public $incrementing = true;
```

<a name="polymorphic-relationships"></a>
## 다형 관계 (Polymorphic Relationships)

다형 관계는 한 자식 모델이 여러 종류의 부모 모델에 연결될 수 있는 관계입니다. 예를 들어, 사용자가 블로그 게시물과 비디오에 모두 댓글을 달 수 있다고 할 때, `Comment` 모델은 `Post`와 `Video` 두 모델 모두에 속할 수 있습니다.

<a name="one-to-one-polymorphic-relations"></a>
### 일대일 (다형 관계) (One to One Polymorphic)

<a name="one-to-one-polymorphic-table-structure"></a>
#### 테이블 구조

일대일 다형 관계는 일반 일대일 관계와 비슷하지만, 자식 모델이 여러 유형의 부모 모델에 속할 수 있습니다.

예를 들어, 블로그의 `Post` 모델과 `User` 모델이 하나의 `Image` 모델과 다형 관계로 연결됩니다. 단일 이미지 테이블을 사용해 게시물과 사용자 모두에 이미지를 할당할 수 있습니다.

`images` 테이블에는 다음과 같이 `imageable_id`와 `imageable_type` 칼럼이 있습니다:

```text
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

`imageable_id`는 `Post` 혹은 `User`의 ID값을, `imageable_type`은 해당 부모 모델의 클래스 이름(`App\Models\Post` 또는 `App\Models\User`)을 저장합니다. Eloquent는 `imageable_type`을 보고 어떤 부모 모델인지를 알 수 있습니다.

<a name="one-to-one-polymorphic-model-structure"></a>
#### 모델 구조

다음은 모델 관계 정의 예시입니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class Image extends Model
{
    /**
     * 이미지가 속한 부모 모델(사용자 또는 게시물)을 가져옵니다.
     */
    public function imageable(): MorphTo
    {
        return $this->morphTo();
    }
}

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphOne;

class Post extends Model
{
    /**
     * 게시물의 이미지
     */
    public function image(): MorphOne
    {
        return $this->morphOne(Image::class, 'imageable');
    }
}

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphOne;

class User extends Model
{
    /**
     * 사용자의 이미지
     */
    public function image(): MorphOne
    {
        return $this->morphOne(Image::class, 'imageable');
    }
}
```

<a name="one-to-one-polymorphic-retrieving-the-relationship"></a>
#### 관계 조회하기

정의 후, 모델의 동적 관계 속성으로 관계를 조회할 수 있습니다:

```php
use App\Models\Post;

$post = Post::find(1);

$image = $post->image;
```

다형 자식 모델에서 부모를 조회할 땐, `morphTo` 호출 메서드 이름(`imageable`)으로 접근합니다:

```php
use App\Models\Image;

$image = Image::find(1);

$imageable = $image->imageable;
```

`imageable` 관계는 그 시점에 따라 `Post` 또는 `User` 인스턴스를 반환합니다.

<a name="morph-one-to-one-key-conventions"></a>
#### 키 규칙

다형 자식 모델이 사용하는 ID 및 타입 컬럼명을 직접 지정하려면, `morphTo`에 관계명, 타입 컬럼, ID 컬럼을 모두 넘기세요. 관계명은 현재 메서드명과 같게 `__FUNCTION__`으로 전달하는 것이 좋습니다:

```php
/**
 * 이미지가 속한 모델을 가져옵니다.
 */
public function imageable(): MorphTo
{
    return $this->morphTo(__FUNCTION__, 'imageable_type', 'imageable_id');
}
```

<a name="one-to-many-polymorphic-relations"></a>
### 일대다 (다형 관계) (One to Many Polymorphic)

<a name="one-to-many-polymorphic-table-structure"></a>
#### 테이블 구조

일대다 다형 관계도 비슷하지만, 자식이 여러 부모 모델 유형 중 하나에 연결될 수 있습니다.

예를 들어, 사용자가 게시물(`Post`)과 비디오(`Video`) 모두에 댓글을 달 수 있는데, 이때 하나의 `comments` 테이블을 공유하여 댓글들을 관리합니다.

관련 테이블은 다음과 같습니다:

```text
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
#### 모델 구조

다음은 관계 정의 예시입니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class Comment extends Model
{
    /**
     * 댓글이 속한 부모 모델(게시물 또는 비디오) 가져오기
     */
    public function commentable(): MorphTo
    {
        return $this->morphTo();
    }
}

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphMany;

class Post extends Model
{
    /**
     * 게시물의 댓글들
     */
    public function comments(): MorphMany
    {
        return $this->morphMany(Comment::class, 'commentable');
    }
}

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphMany;

class Video extends Model
{
    /**
     * 비디오의 댓글들
     */
    public function comments(): MorphMany
    {
        return $this->morphMany(Comment::class, 'commentable');
    }
}
```

<a name="one-to-many-polymorphic-retrieving-the-relationship"></a>
#### 관계 조회하기

`Post` 모델에서 댓글들을 조회:

```php
use App\Models\Post;

$post = Post::find(1);

foreach ($post->comments as $comment) {
    // ...
}
```

다형 자식인 `Comment`에서 부모 접근 시, `morphTo` 호출 메서드명으로 동적 속성 조회:

```php
use App\Models\Comment;

$comment = Comment::find(1);

$commentable = $comment->commentable;
```

`commentable` 관계는 `Post` 또는 `Video` 인스턴스를 반환합니다.

<a name="polymorphic-automatically-hydrating-parent-models-on-children"></a>
#### 자식 모델에서 부모 자동 하이드레이팅 (Automatically Hydrating Parent Models on Children)

이 역시 eager loading을 써도 자식 모델 내 부모 모델 접근 시 "N + 1" 문제가 발생할 수 있습니다:

```php
$posts = Post::with('comments')->get();

foreach ($posts as $post) {
    foreach ($post->comments as $comment) {
        echo $comment->commentable->title;
    }
}
```

댓글은 모두 eager 로딩되었지만, 각 댓글에서 다시 부모인 `Post`를 조회하는 쿼리가 실행됩니다.

이 문제를 해결하려면 `morphMany` 관계 정의 시 `chaperone` 메서드를 추가하세요:

```php
class Post extends Model
{
    /**
     * 게시물의 댓글들
     */
    public function comments(): MorphMany
    {
        return $this->morphMany(Comment::class, 'commentable')->chaperone();
    }
}
```

런타임에서 옵트인하려면 eager loading 시 옵션을 줄 수도 있습니다:

```php
use App\Models\Post;

$posts = Post::with([
    'comments' => fn ($comments) => $comments->chaperone(),
])->get();
```

<a name="one-of-many-polymorphic-relations"></a>
### Many 중 하나 (다형 관계) (One of Many Polymorphic)

여러 자식 모델 중 최신 또는 오래된 단일 모델에 쉽게 접근할 때 사용합니다.

예를 들어, 한 `User`가 여러 `Image`를 가질 때, 가장 최근에 업로드한 이미지를 쉽게 조회하는 경우:

```php
/**
 * 사용자의 최신 이미지.
 */
public function latestImage(): MorphOne
{
    return $this->morphOne(Image::class, 'imageable')->latestOfMany();
}
```

마찬가지로 가장 오래된 이미지를 반환하는 메서드도 만들 수 있습니다:

```php
/**
 * 사용자의 가장 오래된 이미지.
 */
public function oldestImage(): MorphOne
{
    return $this->morphOne(Image::class, 'imageable')->oldestOfMany();
}
```

기본값으로는 기본 키 컬럼을 기준으로 정렬하지만, 다른 칼럼 기준 정렬도 가능합니다.

예를 들어 가장 많이 좋아요 받은 이미지를 가져오려면:

```php
/**
 * 가장 인기 있는 이미지.
 */
public function bestImage(): MorphOne
{
    return $this->morphOne(Image::class, 'imageable')->ofMany('likes', 'max');
}
```

> [!NOTE]  
> 더 복잡한 "one of many" 관계 구성법은 [has one of many 설명](#advanced-has-one-of-many-relationships)을 참고하세요.

<a name="many-to-many-polymorphic-relations"></a>
### 다대다 (다형 관계) (Many to Many Polymorphic)

<a name="many-to-many-polymorphic-table-structure"></a>
#### 테이블 구조

다대다 다형 관계는 `morphOne`, `morphMany`보다 약간 복잡합니다.

예를 들어 `Post`와 `Video` 모델 모두 `Tag` 모델과 다대다 다형 관계를 가질 수 있습니다. 즉, 하나의 `tags` 테이블과 중간 `taggables` 테이블을 사용해 게시물이나 비디오에 태그를 붙일 수 있습니다.

테이블 구조:

```text
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

> [!NOTE]  
> 다대다 다형 관계를 이해하기 전에 일반적인 [다대다 관계](#many-to-many)를 먼저 살펴보면 좋습니다.

<a name="many-to-many-polymorphic-model-structure"></a>
#### 모델 구조

`Post`와 `Video` 모델에 각각 `tags` 메서드를 만들고 `morphToMany` 메서드를 호출합니다.

`morphToMany`는 관련 모델명과 "관계명"을 받습니다. 중간 테이블 이름과 키를 기준으로 관계 이름은 `taggable`로 설정합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphToMany;

class Post extends Model
{
    /**
     * 게시물의 모든 태그
     */
    public function tags(): MorphToMany
    {
        return $this->morphToMany(Tag::class, 'taggable');
    }
}
```

<a name="many-to-many-polymorphic-defining-the-inverse-of-the-relationship"></a>
#### 역방향 관계 정의하기 (Defining the Inverse of the Relationship)

`Tag` 모델에는 가능한 부모 모델 각각에 대해 관계 메서드를 정의해야 합니다.

예를 들어, `posts`와 `videos` 메서드를 만들어 `morphedByMany`를 호출합니다. 이 메서드는 관련 모델과 관계명을 받으며, 이 예에서는 `taggable`입니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphToMany;

class Tag extends Model
{
    /**
     * 이 태그가 할당된 모든 게시물
     */
    public function posts(): MorphToMany
    {
        return $this->morphedByMany(Post::class, 'taggable');
    }

    /**
     * 이 태그가 할당된 모든 비디오
     */
    public function videos(): MorphToMany
    {
        return $this->morphedByMany(Video::class, 'taggable');
    }
}
```

<a name="many-to-many-polymorphic-retrieving-the-relationship"></a>
#### 관계 조회하기

모델 및 DB테이블이 준비되면 다음과 같이 동적 관계 속성으로 조회할 수 있습니다:

```php
use App\Models\Post;

$post = Post::find(1);

foreach ($post->tags as $tag) {
    // ...
}
```

다형 자식에서 부모를 조회할 때는 `Tag` 모델의 `posts` 혹은 `videos` 메서드를 동적 속성으로 접근합니다:

```php
use App\Models\Tag;

$tag = Tag::find(1);

foreach ($tag->posts as $post) {
    // ...
}

foreach ($tag->videos as $video) {
    // ...
}
```

<a name="custom-polymorphic-types"></a>
### 사용자 정의 다형 타입 (Custom Polymorphic Types)

기본적으로 Laravel은 관련 모델 타입을 저장할 때 클래스 이름을 사용합니다. 예를 들어 `Comment` 모델이 `Post` 또는 `Video`에 속하면 `commentable_type` 컬럼은 `App\Models\Post`, `App\Models\Video`가 됩니다.

그러나 내부 클래스명에 의존하지 않고 간단한 별칭을 사용하고 싶을 수 있습니다(`post`, `video` 등). 이렇게 하면 모델명이 바뀌어도 DB에는 영향을 주지 않습니다.

서비스 프로바이더의 `boot` 메서드에 다음 코드를 넣어서 다형 맵을 강제할 수 있습니다:

```php
use Illuminate\Database\Eloquent\Relations\Relation;

Relation::enforceMorphMap([
    'post' => 'App\Models\Post',
    'video' => 'App\Models\Video',
]);
```

실행 중 특정 모델의 별칭은 `getMorphClass` 메서드로 확인 가능하며, 별칭에서 전체 클래스명은 `Relation::getMorphedModel` 메서드로 확인할 수 있습니다:

```php
use Illuminate\Database\Eloquent\Relations\Relation;

$alias = $post->getMorphClass();

$class = Relation::getMorphedModel($alias);
```

> [!WARNING]  
> 기존 앱에서 "morph map"을 추가할 경우, DB에 남아있는 기존의 클래스명이 모두 맵 이름으로 변환되어야 합니다.

<a name="dynamic-relationships"></a>
### 동적 관계 (Dynamic Relationships)

런타임에 관계를 동적으로 정의할 수 있습니다. 주로 패키지 개발 시 유용하지만 일반 앱 개발에서는 권장하지 않습니다.

`resolveRelationUsing` 메서드를 써서 관계 이름과 클로저를 등록합니다. 클로저는 모델을 받고 관계 인스턴스를 반환해야 합니다. 일반적으로 서비스 프로바이더의 `boot` 메서드에서 씁니다:

```php
use App\Models\Order;
use App\Models\Customer;

Order::resolveRelationUsing('customer', function (Order $orderModel) {
    return $orderModel->belongsTo(Customer::class, 'customer_id');
});
```

> [!WARNING]  
> 동적 관계 정의 시 명시적인 키 인자를 항상 관계 메서드에 전달하세요.

<a name="querying-relations"></a>
## 관계 쿼리하기 (Querying Relations)

Eloquent 관계는 모두 메서드로 정의되므로, 이 메서드를 호출하면 실제 질의 없이 관계 인스턴스를 얻을 수 있습니다. 또, 관계는 쿼리 빌더로 동작하므로 조건을 더 체이닝하고 최종적으로 쿼리를 실행할 수 있습니다.

예를 들어, `User`가 여러 `Post`를 가지는 상황:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class User extends Model
{
    /**
     * 사용자의 모든 게시물 가져오기
     */
    public function posts(): HasMany
    {
        return $this->hasMany(Post::class);
    }
}
```

`posts` 관계에 추가 조건 걸기:

```php
use App\Models\User;

$user = User::find(1);

$user->posts()->where('active', 1)->get();
```

Laravel 쿼리 빌더의 다른 메서드도 관계에 그대로 사용할 수 있으니 문서를 참고하세요.

<a name="chaining-orwhere-clauses-after-relationships"></a>
#### 관계 뒤에 `orWhere` 체이닝하기

관계 쿼리에 추가 조건을 걸 수 있지만, `orWhere`를 관계에 바로 체이닝할 때 주의가 필요합니다. `or` 조건이 관계 조건과 별개로 묶여, 조건 논리 결과가 달라질 수 있습니다:

```php
$user->posts()
    ->where('active', 1)
    ->orWhere('votes', '>=', 100)
    ->get();
```

위 코드는 SQL로 다음과 같이 나옵니다. `or`가 외부 조건과 묶여 사용자 외의 게시물도 결과에 포함됩니다:

```sql
select *
from posts
where user_id = ? and active = 1 or votes >= 100
```

따라서 대부분 상황에선 조건을 괄호로 묶어 논리 그룹화해야 합니다:

```php
use Illuminate\Database\Eloquent\Builder;

$user->posts()
    ->where(function (Builder $query) {
        return $query->where('active', 1)
            ->orWhere('votes', '>=', 100);
    })
    ->get();
```

그 결과 SQL:

```sql
select *
from posts
where user_id = ? and (active = 1 or votes >= 100)
```

<a name="relationship-methods-vs-dynamic-properties"></a>
### 관계 메서드와 동적 속성 (Relationship Methods vs. Dynamic Properties)

추가 조건 없이 관계에 접근 시, 동적 속성으로 모델처럼 불러올 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

foreach ($user->posts as $post) {
    // ...
}
```

동적 속성은 "지연 로딩(lazy loading)"을 하므로, 실제 접근 시점에 관련 데이터를 가져옵니다. 따라서 미리 관계를 불러오는 [eager loading](#eager-loading)을 많이 사용합니다.

<a name="querying-relationship-existence"></a>
### 관계 존재 여부 쿼리 (Querying Relationship Existence)

특정 관계가 존재하는 모델만 조회하고 싶으면 `has` 및 `orHas` 메서드를 사용합니다:

```php
use App\Models\Post;

// 댓글이 1개 이상 있는 모든 게시물 조회
$posts = Post::has('comments')->get();
```

조건과 개수도 지정 가능:

```php
// 댓글이 3개 이상 있는 게시물 조회
$posts = Post::has('comments', '>=', 3)->get();
```

점(dot) 표기법으로 중첩 관계도 쿼리 가능:

```php
// 댓글 중 이미지가 1개 이상인 게시물 조회
$posts = Post::has('comments.images')->get();
```

더 복잡한 조건은 `whereHas`와 `orWhereHas`를 사용하여 관계 쿼리를 커스터마이징할 수 있습니다:

```php
use Illuminate\Database\Eloquent\Builder;

// 코드로 시작하는 내용이 있는 댓글이 하나라도 있는 게시물 조회
$posts = Post::whereHas('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
})->get();

// 위 조건을 만족하는 댓글이 10개 이상인 게시물 조회
$posts = Post::whereHas('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
}, '>=', 10)->get();
```

> [!WARNING]  
> 현재 Eloquent는 데이터베이스를 넘는 관계 존재 여부 쿼리를 지원하지 않습니다. 같은 DB 내에서만 관계를 검사할 수 있습니다.

<a name="inline-relationship-existence-queries"></a>
#### 단순한 관계 존재 조건 쿼리 (Inline Relationship Existence Queries)

간단한 where 조건을 `has` 쿼리에 붙일 때는 `whereRelation`, `orWhereRelation`, `whereMorphRelation`, `orWhereMorphRelation` 메서드를 활용할 수 있습니다.

예: 승인되지 않은 댓글이 있는 게시물을 검색:

```php
use App\Models\Post;

$posts = Post::whereRelation('comments', 'is_approved', false)->get();
```

연산자도 지정 가능:

```php
$posts = Post::whereRelation(
    'comments', 'created_at', '>=', now()->subHour()
)->get();
```

<a name="querying-relationship-absence"></a>
### 관계 부재 여부 쿼리 (Querying Relationship Absence)

관계가 없는 모델만 조회하고 싶으면 `doesntHave` 및 `orDoesntHave` 메서드를 사용합니다:

```php
use App\Models\Post;

$posts = Post::doesntHave('comments')->get();
```

조건 추가는 `whereDoesntHave` 및 `orWhereDoesntHave`로 할 수 있습니다:

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::whereDoesntHave('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
})->get();
```

점(dot) 표기법으로 중첩 관계도 지원합니다:

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::whereDoesntHave('comments.author', function (Builder $query) {
    $query->where('banned', 0);
})->get();
```

<a name="querying-morph-to-relationships"></a>
### Morph To 관계 쿼리 (Querying Morph To Relationships)

"morph to" 관계 존재 여부는 `whereHasMorph`와 `whereDoesntHaveMorph`로 쿼리합니다.

인자로 관계명, 포함할 관련 모델명 배열 또는 단일 모델명, 조건 클로저를 지정합니다:

```php
use App\Models\Comment;
use App\Models\Post;
use App\Models\Video;
use Illuminate\Database\Eloquent\Builder;

// 제목이 'code%'로 시작하는 게시물 또는 비디오에 속한 댓글 조회
$comments = Comment::whereHasMorph(
    'commentable',
    [Post::class, Video::class],
    function (Builder $query) {
        $query->where('title', 'like', 'code%');
    }
)->get();

// 게시물 중에서 제목이 'code%'인 것에 속하지 않는 댓글 조회
$comments = Comment::whereDoesntHaveMorph(
    'commentable',
    Post::class,
    function (Builder $query) {
        $query->where('title', 'like', 'code%');
    }
)->get();
```

조건 클로저 내에서 두 번째 인자로 `$type`을 받아 각 타입별 쿼리를 다르게 처리할 수도 있습니다:

```php
use Illuminate\Database\Eloquent\Builder;

$comments = Comment::whereHasMorph(
    'commentable',
    [Post::class, Video::class],
    function (Builder $query, string $type) {
        $column = $type === Post::class ? 'content' : 'title';

        $query->where($column, 'like', 'code%');
    }
)->get();
```

특정 부모 모델에 속하는 자식 모델을 쿼리하려면 `whereMorphedTo`, `whereNotMorphedTo`를 사용합니다:

```php
$comments = Comment::whereMorphedTo('commentable', $post)
    ->orWhereMorphedTo('commentable', $video)
    ->get();
```

<a name="querying-all-morph-to-related-models"></a>
#### 모든 다형 관련 모델 조회하기

관련 모델을 명시하지 않고 모든 다형 모델을 대상으로 쿼리하려면 `*` 와일드카드를 사용할 수 있습니다. 이 경우, Laravel은 추가 쿼리를 실행해 가능한 타입들을 조회합니다:

```php
use Illuminate\Database\Eloquent\Builder;

$comments = Comment::whereHasMorph('commentable', '*', function (Builder $query) {
    $query->where('title', 'like', 'foo%');
})->get();
```

<a name="aggregating-related-models"></a>
## 관련 모델 집계 (Aggregating Related Models)

<a name="counting-related-models"></a>
### 관련 모델 개수 세기 (Counting Related Models)

관련 모델 개수를 실제 모델 로딩 없이 세고 싶으면 `withCount` 메서드를 사용합니다. 반환된 모델에 `{relation}_count` 속성이 추가됩니다:

```php
use App\Models\Post;

$posts = Post::withCount('comments')->get();

foreach ($posts as $post) {
    echo $post->comments_count;
}
```

배열 인자로 여러 관계를 동시에 집계하거나 조건을 추가할 수 있습니다:

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::withCount(['votes', 'comments' => function (Builder $query) {
    $query->where('content', 'like', 'code%');
}])->get();

echo $posts[0]->votes_count;
echo $posts[0]->comments_count;
```

같은 관계 집계를 별명으로 여러 번 불러올 수도 있습니다:

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
#### 나중에 개수 집계하기 (Deferred Count Loading)

이미 모델을 조회한 후에도 `loadCount`를 써서 추가 관계 개수를 불러올 수 있습니다:

```php
$book = Book::first();

$book->loadCount('genres');
```

집계 조건을 넣으려면 배열로 관련 이름과 클로저를 지정하세요:

```php
$book->loadCount(['reviews' => function (Builder $query) {
    $query->where('rating', 5);
}]);
```

<a name="relationship-counting-and-custom-select-statements"></a>
#### `select` 와 `withCount` 조합

`select`문과 `withCount`를 같이 쓸 때는 `select` 뒤에 `withCount`를 호출해야 정상 작동합니다:

```php
$posts = Post::select(['title', 'body'])
    ->withCount('comments')
    ->get();
```

<a name="other-aggregate-functions"></a>
### 기타 집계 함수 (Other Aggregate Functions)

`withMin`, `withMax`, `withAvg`, `withSum`, `withExists` 도 같은 방식으로 지원됩니다. 반환 모델에 `{relation}_{함수}_{컬럼명}` 형태의 속성이 자동 추가됩니다:

```php
use App\Models\Post;

$posts = Post::withSum('comments', 'votes')->get();

foreach ($posts as $post) {
    echo $post->comments_sum_votes;
}
```

별칭을 직접 지정할 수도 있습니다:

```php
$posts = Post::withSum('comments as total_comments', 'votes')->get();

foreach ($posts as $post) {
    echo $post->total_comments;
}
```

`loadSum` 같은 나중에 불러오는 메서드도 존재합니다:

```php
$post = Post::first();

$post->loadSum('comments', 'votes');
```

`select`와 같이 쓸 때는 `select` 호출 뒤에 집계 메서드로 체인하세요:

```php
$posts = Post::select(['title', 'body'])
    ->withExists('comments')
    ->get();
```

<a name="counting-related-models-on-morph-to-relationships"></a>
### Morph To 관계에 대한 관련 모델 개수 세기 (Counting Related Models on Morph To Relationships)

`morphTo` 관계에 대해, 반환 가능한 여러 부모 모델마다 관련 모델 개수를 함께 eager 로딩하려면 `morphWithCount`를 활용합니다.

예를 들어 `ActivityFeed`가 `parentable`이라는 `morphTo` 관계를 가진다고 할 때, `Photo`와 `Post` 모델 각각이 `tags`, `comments` 관계를 가지고 있으면 아래처럼 불러옵니다:

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

<a name="morph-to-deferred-count-loading"></a>
#### 나중에 Morph 관계 개수 불러오기 (Deferred Count Loading)

이미 여러 `ActivityFeed` 모델을 조회한 후, `parentable` 관계에 대한 관련 목차 수를 나중에 불러올 수 있습니다:

```php
$activities = ActivityFeed::with('parentable')->get();

$activities->loadMorphCount('parentable', [
    Photo::class => ['tags'],
    Post::class => ['comments'],
]);
```

<a name="eager-loading"></a>
## Eager Loading (사전 로딩)

모델 관계를 동적 속성으로 접속하면 지연 로딩 됩니다. 즉, 관련 데이터를 액세스하는 시점에 DB에서 가져옵니다. 이 때문에 N + 1 문제(쿼리 과다)가 발생합니다.

예를 들어, `Book`가 `Author`를 `belongsTo`로 가지고 있다고 합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Book extends Model
{
    /**
     * 책을 쓴 저자
     */
    public function author(): BelongsTo
    {
        return $this->belongsTo(Author::class);
    }
}
```

모든 책과 저자를 불러오는 경우:

```php
use App\Models\Book;

$books = Book::all();

foreach ($books as $book) {
    echo $book->author->name;
}
```

이 코드는 책을 불러오는 쿼리 1회와, 각 책마다 저자를 불러오는 쿼리 총 26회를 실행합니다 (책 25개 기준).

반면 eager loading을 사용하면 책과 저자를 각각 1회씩 총 2회 쿼리로 처리합니다:

```php
$books = Book::with('author')->get();

foreach ($books as $book) {
    echo $book->author->name;
}
```

실행되는 SQL:

```sql
select * from books

select * from authors where id in (1, 2, 3, 4, 5, ...)
```

<a name="eager-loading-multiple-relationships"></a>
#### 여러 관계 한 번에 eager loading

여러 관계를 배열 인자로 넘겨 한꺼번에 eager 로딩할 수 있습니다:

```php
$books = Book::with(['author', 'publisher'])->get();
```

<a name="nested-eager-loading"></a>
#### 중첩 eager loading

관계의 관계도 점(dot) 문법으로 eager loading 가능:

```php
$books = Book::with('author.contacts')->get();
```

배열 안의 배열로 중첩 관계를 표현할 수도 있습니다:

```php
$books = Book::with([
    'author' => [
        'contacts',
        'publisher',
    ],
])->get();
```

<a name="nested-eager-loading-morphto-relationships"></a>
#### `morphTo` 관계에 중첩 eager loading 하기

`morphTo` 관계들에 중첩 eager loading이 필요하면, 관계 인스턴스의 `morphWith` 메서드를 사용합니다.

예시:

```php
<?php

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class ActivityFeed extends Model
{
    /**
     * 활동 피드의 부모 모델 (다형 관계)
     */
    public function parentable(): MorphTo
    {
        return $this->morphTo();
    }
}
```

`ActivityFeed`의 `parentable`이 `Event`, `Photo`, `Post` 모델이 될 수 있고, 각 모델마다 연결된 관계(`calendar`, `tags`, `author`)가 있으면 다음처럼 불러옵니다:

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
#### 특정 컬럼만 eager loading

관계 테이블 컬럼이 많을 때, 일부만 불러오려면 다음과 같이 지정하세요:

```php
$books = Book::with('author:id,name,book_id')->get();
```

> [!WARNING]  
> 이때 반드시 기본 키(`id`)와 외래 키 컬럼을 포함시켜야 합니다.

<a name="eager-loading-by-default"></a>
#### 항상 eager loading하기 (Eager Loading by Default)

항상 특정 관계를 eager loading 하고 싶으면 모델에 `$with` 속성을 정의합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Book extends Model
{
    /**
     * 항상 함께 로딩할 관계들
     *
     * @var array
     */
    protected $with = ['author'];

    /**
     * 저자 관계
     */
    public function author(): BelongsTo
    {
        return $this->belongsTo(Author::class);
    }

    /**
     * 장르 관계
     */
    public function genre(): BelongsTo
    {
        return $this->belongsTo(Genre::class);
    }
}
```

특정 쿼리에서 제외하려면 `without` 메서드:

```php
$books = Book::without('author')->get();
```

모든 `$with` 항목 대신 특정 관계만 eager loading 하려면 `withOnly` 사용:

```php
$books = Book::withOnly('genre')->get();
```

<a name="constraining-eager-loads"></a>
### eager loading 조건 걸기 (Constraining Eager Loads)

eager loading 시 관련 관계 쿼리에 조건을 지정하려면 `with`에 배열로 관계명과 조건 클로저를 넘깁니다:

```php
use App\Models\User;
use Illuminate\Contracts\Database\Eloquent\Builder;

$users = User::with(['posts' => function (Builder $query) {
    $query->where('title', 'like', '%code%');
}])->get();
```

`where`, `orderBy` 등 여러 쿼리 빌더 조건을 함께 사용 할 수 있습니다:

```php
$users = User::with(['posts' => function (Builder $query) {
    $query->orderBy('created_at', 'desc');
}])->get();
```

<a name="constraining-eager-loading-of-morph-to-relationships"></a>
#### `morphTo` 관계 조건 걸기

`morphTo` 관계를 eager load 할 때, 각 타입별 모델에 조건을 걸려면 `MorphTo` 인스턴스의 `constrain` 메서드를 사용합니다:

```php
use Illuminate\Database\Eloquent\Relations\MorphTo;

$comments = Comment::with(['commentable' => function (MorphTo $morphTo) {
    $morphTo->constrain([
        Post::class => function ($query) {
            $query->whereNull('hidden_at');
        },
        Video::class => function ($query) {
            $query->where('type', 'educational');
        },
    ]);
}])->get();
```

위 예제에서 `Post`는 `hidden_at`이 null인 경우만, `Video`는 `type`이 `educational`인 경우만 eager load 됩니다.

<a name="constraining-eager-loads-with-relationship-existence"></a>
#### 관계 존재 여부 조건과 함께 eager loading 하기

특정 관계의 조건을 만족하는 모델만 가져오면서, 그 관계도 함께 eager load 하고 싶으면 `withWhereHas`를 사용합니다:

```php
use App\Models\User;

$users = User::withWhereHas('posts', function ($query) {
    $query->where('featured', true);
})->get();
```

<a name="lazy-eager-loading"></a>
### 지연 eager loading (Lazy Eager Loading)

부모 모델은 이미 로드된 상태에서, 특정 조건에 따라 추가 관계만 나중에 eager load 해야 할 때가 있습니다:

```php
use App\Models\Book;

$books = Book::all();

if ($someCondition) {
    $books->load('author', 'publisher');
}
```

조건식을 넣으려면 배열에 관계별 쿼리 빌더 클로저를 넣으면 됩니다:

```php
$author->load(['books' => function (Builder $query) {
    $query->orderBy('published_date', 'asc');
}]);
```

이미 관계가 로드되어 있을 때만 로딩하려면 `loadMissing`를 사용하세요:

```php
$book->loadMissing('author');
```

<a name="nested-lazy-eager-loading-morphto"></a>
#### 중첩 lazy eager loading과 `morphTo`

`morphTo` 관계와 해당 관계가 반환하는 다양한 모델의 중첩 관계를 나중에 eager load 하려면 `loadMorph`를 씁니다.

`loadMorph`는 관계명과 모델별 관계 목록 배열을 받습니다.

예:

```php
<?php

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class ActivityFeed extends Model
{
    /**
     * 액티비티 피드의 부모
     */
    public function parentable(): MorphTo
    {
        return $this->morphTo();
    }
}
```

`parentable`이 `Event`, `Photo`, `Post` 등이 될 수 있고, 각기 아래 관계를 가질 때:

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
### Lazy Loading 방지 (Preventing Lazy Loading)

eager loading 사용을 권장하므로, 필요한 경우 애초에 lazy loading을 어플리케이션에서 차단할 수 있습니다.

`Model` 클래스의 `preventLazyLoading` 메서드에 `true`를 넘기면 lazy loading 시도 시 예외를 발생시킵니다. 보통 `AppServiceProvider`의 `boot` 메서드에 작성합니다:

```php
use Illuminate\Database\Eloquent\Model;

/**
 * 애플리케이션 서비스 부트스트랩
 */
public function boot(): void
{
    Model::preventLazyLoading(! $this->app->isProduction());
}
```

이렇게 하면 개발 및 테스트 환경에서만 lazy loading 차단하고, 프로덕션은 정상 작동하도록 할 수 있습니다.

`handleLazyLoadingViolationsUsing` 메서드를 이용해 lazy loading 위반 시 로그 기록 등 사용자 정의 동작도 가능:

```php
Model::handleLazyLoadingViolationUsing(function (Model $model, string $relation) {
    $class = $model::class;

    info("Attempted to lazy load [{$relation}] on model [{$class}].");
});
```

<a name="inserting-and-updating-related-models"></a>
## 관계 모델 삽입 및 갱신 (Inserting and Updating Related Models)

<a name="the-save-method"></a>
### `save` 메서드 (The `save` Method)

댓글 같은 새 모델을 관계를 통해 추가할 때, 직접 외래 키를 지정할 필요 없이 관계의 `save` 메서드를 쓸 수 있습니다:

```php
use App\Models\Comment;
use App\Models\Post;

$comment = new Comment(['message' => 'A new comment.']);

$post = Post::find(1);

$post->comments()->save($comment);
```

`comments` 속성(동적 관계 속성)을 사용하지 않고 메서드를 호출한 점 주의하세요. `save` 메서드는 외래 키(`post_id`)를 자동으로 채워 줍니다.

복수 모델 저장은 `saveMany`를 씁니다:

```php
$post = Post::find(1);

$post->comments()->saveMany([
    new Comment(['message' => 'A new comment.']),
    new Comment(['message' => 'Another new comment.']),
]);
```

`save` / `saveMany`는 새로 저장한 모델을 부모 모델의 로컬 관계에는 자동으로 추가하지 않습니다. 관계를 바로 접근하려면 `refresh`를 호출해 부모 모델과 관계를 다시 불러오세요:

```php
$post->comments()->save($comment);

$post->refresh();

// 새 댓글 포함 모든 댓글 조회 가능
$post->comments;
```

<a name="the-push-method"></a>
#### 연결된 모델 재귀 저장 (`push`)

모델 및 모든 관련 모델들을 재귀적으로 저장하려면 `push` 를 사용합니다:

```php
$post = Post::find(1);

$post->comments[0]->message = 'Message';
$post->comments[0]->author->name = 'Author Name';

$post->push();
```

이벤트를 발생시키지 않고 저장하려면 `pushQuietly`를 씁니다:

```php
$post->pushQuietly();
```

<a name="the-create-method"></a>
### `create` 메서드 (The `create` Method)

`save`/`saveMany`가 Eloquent 모델 인스턴스를 받는 반면, `create`/`createMany`는 속성 배열을 받아 모델을 생성하며 저장합니다.

예:

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

이벤트 발생 없이 생성하려면 `createQuietly`, `createManyQuietly`를 씁니다:

```php
$user = User::find(1);

$user->posts()->createQuietly([
    'title' => 'Post title.',
]);

$user->posts()->createManyQuietly([
    ['title' => 'First post.'],
    ['title' => 'Second post.'],
]);
```

필요시 [업데이트 또는 생성 메서드](updateOrCreate 등)도 사용할 수 있습니다.

> [!NOTE]  
> `create`는 대량 할당 규칙을 준수해야 하니 [mass assignment](/docs/master/eloquent#mass-assignment) 문서를 참고하세요.

<a name="updating-belongs-to-relationships"></a>
### Belongs To 관계 갱신하기 (Belongs To Relationships)

자식 모델에 새 부모를 연결하려면 `associate` 메서드로 외래 키를 설정하세요:

```php
use App\Models\Account;

$account = Account::find(10);

$user->account()->associate($account);

$user->save();
```

부모 모델과의 연결을 끊으려면 `dissociate`:

```php
$user->account()->dissociate();

$user->save();
```

<a name="updating-many-to-many-relationships"></a>
### 다대다 관계 갱신하기 (Many to Many Relationships)

<a name="attaching-detaching"></a>
#### 연결 및 해제 (Attaching / Detaching)

다대다 관계 중간 테이블에 새로운 관계를 추가하려면 `attach`:

```php
use App\Models\User;

$user = User::find(1);

$user->roles()->attach($roleId);
```

중간 테이블에 추가 데이터를 넘길 수도 있습니다:

```php
$user->roles()->attach($roleId, ['expires' => $expires]);
```

관계를 제거하려면 `detach`를 사용합니다. 중간 테이블 행만 삭제되며 양쪽 모델은 유지됩니다:

```php
// 한 개 역할 해제
$user->roles()->detach($roleId);

// 모든 역할 해제
$user->roles()->detach();
```

`attach`와 `detach`는 배열 형태 ID도 받습니다:

```php
$user = User::find(1);

$user->roles()->detach([1, 2, 3]);

$user->roles()->attach([
    1 => ['expires' => $expires],
    2 => ['expires' => $expires],
]);
```

<a name="syncing-associations"></a>
#### 관계 동기화 (Syncing Associations)

`sync`는 전달한 ID 목록과 중간 테이블을 동기화해, 목록 밖 ID는 삭제합니다:

```php
$user->roles()->sync([1, 2, 3]);
```

추가 데이터도 함께 넘길 수 있습니다:

```php
$user->roles()->sync([1 => ['expires' => true], 2, 3]);
```

모든 ID에 공통 데이터를 넣으려면 `syncWithPivotValues`:

```php
$user->roles()->syncWithPivotValues([1, 2, 3], ['active' => true]);
```

기존에 없는 ID만 추가하려면 `syncWithoutDetaching`:

```php
$user->roles()->syncWithoutDetaching([1, 2, 3]);
```

<a name="toggling-associations"></a>
#### 관계 토글 (Toggling Associations)

`toggle`은 넘긴 ID들의 첨부 상태를 반전합니다. 붙어있으면 떼고, 없으면 붙입니다:

```php
$user->roles()->toggle([1, 2, 3]);
```

추가 데이터와 함께 토글도 가능합니다:

```php
$user->roles()->toggle([
    1 => ['expires' => true],
    2 => ['expires' => true],
]);
```

<a name="updating-a-record-on-the-intermediate-table"></a>
#### 중간 테이블 행 업데이트 (Updating a Record on the Intermediate Table)

중간 테이블 기존 행을 갱신하려면 `updateExistingPivot`를 씁니다. 첫 번째 인자는 관련 외래 키, 두 번째 인자는 갱신할 속성 배열입니다:

```php
$user = User::find(1);

$user->roles()->updateExistingPivot($roleId, [
    'active' => false,
]);
```

<a name="touching-parent-timestamps"></a>
## 부모 타임스탬프 터치하기 (Touching Parent Timestamps)

`belongsTo` 또는 `belongsToMany` 관계를 가지는 경우, 자식 모델이 업데이트 되면 부모 모델의 `updated_at` 타임스탬프도 갱신하는 것이 유용합니다.

예를 들어, `Comment` 모델이 수정될 때 해당 댓글이 속한 `Post`의 `updated_at`을 자동 갱신 하려면, 자식 모델에 `$touches` 속성을 정의합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Comment extends Model
{
    /**
     * 타임스탬프 갱신 대상 관계들
     *
     * @var array
     */
    protected $touches = ['post'];

    /**
     * 댓글이 속한 게시물
     */
    public function post(): BelongsTo
    {
        return $this->belongsTo(Post::class);
    }
}
```

> [!WARNING]  
> 부모 모델 타임스탬프는 자식 모델이 Eloquent의 `save` 메서드로 저장될 때만 자동 갱신됩니다.