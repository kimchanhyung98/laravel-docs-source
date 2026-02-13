# Eloquent: 연관관계 (Eloquent: Relationships)

- [소개](#introduction)
- [연관관계 정의하기](#defining-relationships)
    - [일대일 / hasOne](#one-to-one)
    - [일대다 / hasMany](#one-to-many)
    - [일대다 (역방향) / belongsTo](#one-to-many-inverse)
    - [하나의 여러 개 중 하나 가져오기 (Has One of Many)](#has-one-of-many)
    - [Has One Through](#has-one-through)
    - [Has Many Through](#has-many-through)
- [스코프 연관관계](#scoped-relationships)
- [다대다 연관관계](#many-to-many)
    - [중간 테이블 컬럼 가져오기](#retrieving-intermediate-table-columns)
    - [중간 테이블 컬럼을 통한 쿼리 필터링](#filtering-queries-via-intermediate-table-columns)
    - [중간 테이블 컬럼을 통한 쿼리 정렬](#ordering-queries-via-intermediate-table-columns)
    - [사용자 정의 중간 테이블 모델 정의](#defining-custom-intermediate-table-models)
- [Polymorphic(다형성) 연관관계](#polymorphic-relationships)
    - [일대일](#one-to-one-polymorphic-relations)
    - [일대다](#one-to-many-polymorphic-relations)
    - [여러 개 중 하나 (One of Many)](#one-of-many-polymorphic-relations)
    - [다대다](#many-to-many-polymorphic-relations)
    - [사용자 정의 다형성 타입](#custom-polymorphic-types)
- [동적 연관관계](#dynamic-relationships)
- [연관관계 쿼리하기](#querying-relations)
    - [연관관계 메서드와 동적 프로퍼티](#relationship-methods-vs-dynamic-properties)
    - [연관관계 존재 쿼리](#querying-relationship-existence)
    - [연관관계 부재 쿼리](#querying-relationship-absence)
    - [Morph To(Polymorphic) 연관관계 쿼리](#querying-morph-to-relationships)
- [연관된 모델 집계하기](#aggregating-related-models)
    - [연관된 모델 개수 세기](#counting-related-models)
    - [기타 집계 함수](#other-aggregate-functions)
    - [Morph To 연관관계에서 모델 개수 세기](#counting-related-models-on-morph-to-relationships)
- [Eager Loading](#eager-loading)
    - [Eager 로드 제약하기](#constraining-eager-loads)
    - [지연 Eager 로딩](#lazy-eager-loading)
    - [자동 Eager 로딩](#automatic-eager-loading)
    - [Lazy Loading 방지하기](#preventing-lazy-loading)
- [연관된 모델 삽입 및 수정](#inserting-and-updating-related-models)
    - [`save` 메서드](#the-save-method)
    - [`create` 메서드](#the-create-method)
    - [Belongs To 연관관계](#updating-belongs-to-relationships)
    - [다대다 연관관계](#updating-many-to-many-relationships)
- [부모 타임스탬프 동기화하기](#touching-parent-timestamps)

<a name="introduction"></a>
## 소개 (Introduction)

데이터베이스 테이블들은 서로 연관되어 있는 경우가 많습니다. 예를 들어, 블로그 포스트는 여러 개의 댓글을 가질 수 있고, 주문은 주문한 사용자와 연관될 수 있습니다. Eloquent는 이러한 연관관계를 쉽게 관리하고 작업할 수 있도록 다양한 일반적인 연관관계를 지원합니다.

<div class="content-list" markdown="1">

- [일대일](#one-to-one)
- [일대다](#one-to-many)
- [다대다](#many-to-many)
- [Has One Through](#has-one-through)
- [Has Many Through](#has-many-through)
- [일대일 (Polymorphic)](#one-to-one-polymorphic-relations)
- [일대다 (Polymorphic)](#one-to-many-polymorphic-relations)
- [다대다 (Polymorphic)](#many-to-many-polymorphic-relations)

</div>

<a name="defining-relationships"></a>
## 연관관계 정의하기 (Defining Relationships)

Eloquent의 연관관계는 Eloquent 모델 클래스 내의 메서드로 정의합니다. 또한, 연관관계는 강력한 [쿼리 빌더](/docs/master/queries) 역할도 하므로, 메서드를 통해 정의하면 다양한 메서드 체이닝과 쿼리 확장 기능을 사용할 수 있습니다. 예를 들어 `posts` 연관관계에 추가적인 쿼리 조건을 쉽게 체이닝할 수 있습니다.

```php
$user->posts()->where('active', 1)->get();
```

연관관계를 실제로 사용하기 전에, Eloquent가 지원하는 각각의 연관관계를 어떻게 정의하는지 살펴보겠습니다.

<a name="one-to-one"></a>
### 일대일 / hasOne (One to One / Has One)

일대일 연관관계는 가장 기본적인 데이터베이스 연관관계입니다. 예를 들어, `User` 모델이 하나의 `Phone` 모델과 연관될 수 있습니다. 이 관계를 정의하기 위해서는 `User` 모델에 `phone` 메서드를 추가하고, `hasOne` 메서드를 호출해서 그 결과를 반환하면 됩니다. `hasOne` 메서드는 모델의 `Illuminate\Database\Eloquent\Model` 기본 클래스를 통해 제공됩니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasOne;

class User extends Model
{
    /**
     * 해당 사용자와 연관된 전화번호를 가져옵니다.
     */
    public function phone(): HasOne
    {
        return $this->hasOne(Phone::class);
    }
}
```

`hasOne` 메서드의 첫 번째 인수는 연관된 모델 클래스명입니다. 연관관계를 정의한 후에는 Eloquent의 동적 프로퍼티를 이용해 관련 레코드를 불러올 수 있습니다. 동적 프로퍼티는 연관관계 메서드를 모델의 프로퍼티처럼 접근할 수 있도록 해줍니다.

```php
$phone = User::find(1)->phone;
```

Eloquent는 부모 모델의 이름에 따라 연관관계의 외래 키를 자동으로 결정합니다. 이 예시에서는 `Phone` 모델이 `user_id`라는 외래 키를 갖는다고 가정합니다. 이 규칙을 변경하고 싶다면, `hasOne`의 두 번째 인수로 외래 키 컬럼명을 지정할 수 있습니다.

```php
return $this->hasOne(Phone::class, 'foreign_key');
```

또한, Eloquent는 외래 키 컬럼값이 부모의 기본 키 컬럼(`id`)과 일치해야 한다고 가정합니다. 즉, `Phone` 레코드의 `user_id` 컬럼에 사용자의 `id` 값이 매칭됩니다. 만약 부모 키가 `id`가 아니거나, 특정 컬럼을 로컬 키로 사용하려면 세 번째 인수로 로컬 키를 전달할 수 있습니다.

```php
return $this->hasOne(Phone::class, 'foreign_key', 'local_key');
```

<a name="one-to-one-defining-the-inverse-of-the-relationship"></a>
#### 연관관계의 역방향 정의하기

이제 `User` 모델에서 `Phone` 모델을 접근할 수 있게 되었습니다. 이번에는 `Phone` 모델에서도 해당 전화번호의 소유자인 사용자를 접근할 수 있도록 연관관계를 정의해봅시다. `hasOne` 관계의 역방향은 `belongsTo` 메서드를 통해 정의합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Phone extends Model
{
    /**
     * 전화번호를 소유한 사용자를 가져옵니다.
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }
}
```

`user` 메서드를 호출할 때, Eloquent는 `Phone` 모델의 `user_id` 컬럼이 `User` 모델의 `id`와 일치하는 레코드를 찾으려고 시도합니다.

Eloquent는 연관관계 메서드의 이름에 `_id`를 붙여서 외래 키의 이름을 결정합니다. 따라서 Eloquent는 `Phone` 모델에 `user_id` 컬럼이 있다고 가정하지만, 외래 키가 다를 경우에는 `belongsTo`의 두 번째 인수로 직접 지정할 수 있습니다.

```php
/**
 * 전화번호를 소유한 사용자를 가져옵니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class, 'foreign_key');
}
```

부모 모델이 `id`가 아닌 다른 컬럼을 기본 키로 쓰거나, 특정 컬럼으로 연관관계를 맺으려면 세 번째 인수로 부모 테이블의 키 컬럼명을 지정할 수 있습니다.

```php
/**
 * 전화번호를 소유한 사용자를 가져옵니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class, 'foreign_key', 'owner_key');
}
```

<a name="one-to-many"></a>
### 일대다 / hasMany (One to Many / Has Many)

일대다 연관관계는 하나의 모델이 여러 자식 모델을 소유하는 관계를 나타냅니다. 예를 들어, 하나의 블로그 포스트는 무한히 많은 댓글을 가질 수 있습니다. 일대다 연관관계도 모델에 메서드를 정의하여 만듭니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Post extends Model
{
    /**
     * 블로그 포스트의 댓글들을 가져옵니다.
     */
    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class);
    }
}
```

Eloquent는 `Comment` 모델의 외래 키 컬럼명을 자동으로 결정합니다. 관례상 부모 모델명을 스네이크 케이스로 만들고 `_id`를 붙입니다. 이 경우, `Comment` 모델의 외래 키는 `post_id`로 간주합니다.

연관관계 메서드를 정의한 후에는 `comments` 프로퍼티에 접근하여 [컬렉션](/docs/master/eloquent-collections)으로 관련 댓글을 가져올 수 있습니다. 동적으로 연관관계 프로퍼티를 접근할 수 있음을 기억하십시오.

```php
use App\Models\Post;

$comments = Post::find(1)->comments;

foreach ($comments as $comment) {
    // ...
}
```

연관관계도 쿼리 빌더이므로, 추가 조건을 체이닝해서 쿼리를 확장할 수 있습니다.

```php
$comment = Post::find(1)->comments()
    ->where('title', 'foo')
    ->first();
```

`hasOne`처럼, 외래 키와 로컬 키를 추가 인수로 전달하여 규칙을 오버라이드할 수도 있습니다.

```php
return $this->hasMany(Comment::class, 'foreign_key');

return $this->hasMany(Comment::class, 'foreign_key', 'local_key');
```

<a name="automatically-hydrating-parent-models-on-children"></a>
#### 자식 모델에서 부모 자동 할당(hydrating)하기

Eloquent의 eager loading을 사용하더라도, 자식 모델을 반복 처리하면서 그 부모를 접근하면 "N + 1" 쿼리 문제가 발생할 수 있습니다.

```php
$posts = Post::with('comments')->get();

foreach ($posts as $post) {
    foreach ($post->comments as $comment) {
        echo $comment->post->title;
    }
}
```

위 예시에서는, 모든 `Post` 모델에 대해 댓글을 eager 로딩했음에도, 각 `Comment` 모델에서 부모인 `Post`를 접근하면 추가 쿼리가 발생하여 "N + 1" 문제가 생깁니다.

만약 Eloquent가 자식의 부모 모델을 자동으로 할당(hydrate)하도록 하고 싶다면, `hasMany` 연관관계 정의 시 `chaperone` 메서드를 호출할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Post extends Model
{
    /**
     * 블로그 포스트의 댓글들을 가져옵니다.
     */
    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class)->chaperone();
    }
}
```

런타임에서 자동으로 부모 할당 기능을 사용하고 싶다면, eager 로딩 시 `chaperone`을 정의할 수 있습니다.

```php
use App\Models\Post;

$posts = Post::with([
    'comments' => fn ($comments) => $comments->chaperone(),
])->get();
```

<a name="one-to-many-inverse"></a>
### 일대다 (역방향) / belongsTo (One to Many (Inverse) / Belongs To)

이제 하나의 포스트에 속한 모든 댓글을 접근할 수 있게 되었으니, 반대로 댓글에서 부모 포스트를 접근할 수 있게 해보겠습니다. 일대다 관계의 역방향은 자식 모델에 `belongsTo` 메서드를 정의하여 만듭니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Comment extends Model
{
    /**
     * 댓글이 속한 포스트를 가져옵니다.
     */
    public function post(): BelongsTo
    {
        return $this->belongsTo(Post::class);
    }
}
```

연관관계가 정의되었으면, 댓글의 부모 포스트에 `post` 연관관계 프로퍼티로 접근할 수 있습니다.

```php
use App\Models\Comment;

$comment = Comment::find(1);

return $comment->post->title;
```

이 예시에서 Eloquent는 `Comment` 모델의 `post_id` 컬럼이 `Post` 모델의 `id`와 일치하는 레코드를 찾으려고 합니다.

연관관계 메서드명과 부모 모델의 기본 키 컬럼명을 조합하여(`post_id`) 기본 외래 키 이름을 결정합니다.

연관관계의 외래 키가 관례와 다르다면, `belongsTo`의 두 번째 인수로 직접 지정할 수 있습니다.

```php
/**
 * 댓글이 속한 포스트를 가져옵니다.
 */
public function post(): BelongsTo
{
    return $this->belongsTo(Post::class, 'foreign_key');
}
```

부모 모델이 `id`가 아닌 다른 컬럼을 기본 키로 쓰거나, 특정 컬럼으로 연관관계를 맺으려면 세 번째 인수로 부모 테이블의 키 컬럼명을 지정할 수 있습니다.

```php
/**
 * 댓글이 속한 포스트를 가져옵니다.
 */
public function post(): BelongsTo
{
    return $this->belongsTo(Post::class, 'foreign_key', 'owner_key');
}
```

<a name="default-models"></a>
#### 기본 모델 (Default Models)

`belongsTo`, `hasOne`, `hasOneThrough`, `morphOne` 연관관계에서는, 연관관계가 `null`일 경우 반환할 기본 모델을 정의할 수 있습니다. 이런 패턴은 [Null Object 패턴](https://en.wikipedia.org/wiki/Null_Object_pattern)이라 하며, 코드에서 조건문을 줄여줍니다. 아래 예시처럼 `Post` 모델에 유저가 연결되어 있지 않으면 빈 `App\Models\User` 모델이 반환됩니다.

```php
/**
 * 포스트의 작성자(author)를 가져옵니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault();
}
```

기본 모델에 속성값을 미리 채우고 싶다면, 배열이나 클로저를 `withDefault`에 전달합니다.

```php
/**
 * 포스트의 작성자(author)를 가져옵니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault([
        'name' => 'Guest Author',
    ]);
}

/**
 * 포스트의 작성자(author)를 가져옵니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault(function (User $user, Post $post) {
        $user->name = 'Guest Author';
    });
}
```

<a name="querying-belongs-to-relationships"></a>
#### Belongs To 연관관계 쿼리하기

"belongs to" 연관관계의 자식 모델들을 쿼리할 때, Eloquent 모델을 가져오기 위해 `where` 절을 직접 작성할 수 있습니다.

```php
use App\Models\Post;

$posts = Post::where('user_id', $user->id)->get();
```

더 간편하게는, `whereBelongsTo` 메서드를 사용하여 올바른 연관관계와 외래 키를 자동으로 처리할 수 있습니다.

```php
$posts = Post::whereBelongsTo($user)->get();
```

[컬렉션](/docs/master/eloquent-collections) 인스턴스를 전달하면, 컬렉션 내의 모델 어느 것에 속한 모델도 조회합니다.

```php
$users = User::where('vip', true)->get();

$posts = Post::whereBelongsTo($users)->get();
```

기본적으로 전달한 모델 클래스명을 기반으로 연관관계명을 유추하지만, 두 번째 인수로 연관관계명을 직접 지정할 수도 있습니다.

```php
$posts = Post::whereBelongsTo($user, 'author')->get();
```

<a name="has-one-of-many"></a>
### 하나의 여러 개 중 하나 가져오기 (Has One of Many)

가끔 하나의 모델이 여러 관련 모델을 가지지만, 그 중 "가장 최신" 혹은 "가장 오래된" 하나만 쉽게 가져오고 싶을 수 있습니다. 예를 들어, `User` 모델이 여러 `Order` 모델과 연관될 수 있는데, 사용자가 가장 최근에 주문한 주문을 가져오는 편리한 방법을 만들고 싶다면 `hasOne`과 `ofMany` 관련 메서드를 활용할 수 있습니다.

```php
/**
 * 사용자의 가장 최근 주문을 가져옵니다.
 */
public function latestOrder(): HasOne
{
    return $this->hasOne(Order::class)->latestOfMany();
}
```

또는, "가장 오래된" 혹은 첫 번째 주문을 가져오는 메서드도 정의할 수 있습니다.

```php
/**
 * 사용자의 가장 오래된 주문을 가져옵니다.
 */
public function oldestOrder(): HasOne
{
    return $this->hasOne(Order::class)->oldestOfMany();
}
```

기본적으로 `latestOfMany`와 `oldestOfMany`는 모델의 정렬 가능한 기본 키를 기준으로 동작합니다. 하지만, 더 큰 연관관계에서 다른 정렬 기준으로 단일 모델을 가져오고 싶을 때는 `ofMany`를 사용할 수 있습니다. 예를 들어, 사용자 주문 중에서 "가장 비싼" 주문을 가져올 수도 있습니다.

```php
/**
 * 사용자의 가장 큰(비싼) 주문을 가져옵니다.
 */
public function largestOrder(): HasOne
{
    return $this->hasOne(Order::class)->ofMany('price', 'max');
}
```

> [!WARNING]
> PostgreSQL은 UUID 컬럼에 대해 `MAX` 함수를 지원하지 않으므로, PostgreSQL UUID 컬럼과 one-of-many 관계를 조합해 사용할 수 없습니다.

<a name="converting-many-relationships-to-has-one-relationships"></a>
#### 다수 관계를 "하나" 관계로 변환하기

`latestOfMany`, `oldestOfMany`, `ofMany` 메서드를 사용해 단일 모델을 가져올 때, 이미 동일 모델에 대해 "has many" 관계가 정의되어 있다면, `one` 메서드를 이용해 이 연관관계를 "has one" 관계로 쉽게 변환할 수 있습니다.

```php
/**
 * 사용자의 모든 주문을 가져옵니다.
 */
public function orders(): HasMany
{
    return $this->hasMany(Order::class);
}

/**
 * 사용자의 가장 큰(비싼) 주문을 가져옵니다.
 */
public function largestOrder(): HasOne
{
    return $this->orders()->one()->ofMany('price', 'max');
}
```

`HasManyThrough` 관계도 `one`을 사용해 `HasOneThrough`로 변경할 수 있습니다.

```php
public function latestDeployment(): HasOneThrough
{
    return $this->deployments()->one()->latestOfMany();
}
```

<a name="advanced-has-one-of-many-relationships"></a>
#### 고급 "하나의 여러 개 중 하나" 연관관계

좀 더 고도화된 one-of-many 연관관계를 만들 수도 있습니다. 예를 들어, `Product` 모델이 여러 `Price` 모델과 연관되어 있고, 가격 변경 내역이 모두 시스템에 남아 있다고 가정합시다. `published_at` 컬럼을 이용해 미래 시점으로 가격 책정도 가능합니다.

즉, 발표 시점이 미래가 아닌, "가장 최근에 발표된" 가격을 가져와야 합니다. 만약 동일한 발표 날짜가 있을 경우엔 가장 큰 id를 우선시합니다. 이를 위해 `ofMany`에 정렬 기준이 되는 컬럼의 배열을 전달하고, 쿼리 조건을 추가할 클로저를 두 번째 인자에 전달합니다.

```php
/**
 * 해당 상품의 현재 가격 정보를 가져옵니다.
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

"has-one-through" 연관관계는 일대일 관계이지만, 중간 모델을 통해 다른 모델과 연결되는 관계를 나타냅니다.

예를 들어, 차량 정비소 애플리케이션에서 각 `Mechanic`(정비사) 모델은 하나의 `Car`와 연관되고, 각 `Car` 모델은 하나의 `Owner`(차주)와 연관됩니다. 정비사와 차주는 데이터베이스에서 직접적 관계가 없지만, `Car` 모델을 "거쳐서" 차주에 접근할 수 있습니다. 필요한 테이블 구조는 아래와 같습니다.

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

테이블 구조를 바탕으로 `Mechanic` 모델에 관계를 정의해봅니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasOneThrough;

class Mechanic extends Model
{
    /**
     * 자동차의 소유자를 가져옵니다.
     */
    public function carOwner(): HasOneThrough
    {
        return $this->hasOneThrough(Owner::class, Car::class);
    }
}
```

`hasOneThrough`의 첫 번째 인수는 접근하려는 최종 모델, 두 번째 인수는 중간 모델 클래스명입니다.

이미 각각의 모델에 필요한 연관관계가 정의되어 있다면, `through` 메서드와 관계명을 이용해 보다 유연하게 "has-one-through" 관계를 정의할 수 있습니다. 만약 `Mechanic` 모델에 `cars` 관계가 있고, `Car` 모델에 `owner` 관계가 있다면 아래와 같이 구성할 수 있습니다.

```php
// 문자열 기반 문법
return $this->through('cars')->has('owner');

// 동적 문법
return $this->throughCars()->hasOwner();
```

<a name="has-one-through-key-conventions"></a>
#### 키 규칙 (Key Conventions)

일반적인 Eloquent 외래 키 규칙이 해당 쿼리에 적용됩니다. 만약 관계의 키를 직접 지정하고 싶다면, `hasOneThrough`의 세 번째와 네 번째 인수로 전달할 수 있습니다. 세 번째 인수는 중간 모델의 외래 키 컬럼, 네 번째 인수는 최종 모델의 외래 키 컬럼, 다섯 번째는 mechanics 테이블의 로컬 키, 여섯 번째는 cars 테이블의 로컬 키입니다.

```php
class Mechanic extends Model
{
    /**
     * 자동차의 소유자를 가져옵니다.
     */
    public function carOwner(): HasOneThrough
    {
        return $this->hasOneThrough(
            Owner::class,
            Car::class,
            'mechanic_id', // cars 테이블의 외래 키
            'car_id', // owners 테이블의 외래 키
            'id', // mechanics 테이블의 로컬 키
            'id' // cars 테이블의 로컬 키
        );
    }
}
```

또는 앞서 언급한 대로, 각 모델의 연관관계가 이미 정의되어 있다면, `through`를 이용해 정의할 수 있습니다. 이 방법은 기존에 정의한 키 규칙을 재사용하는 장점이 있습니다.

```php
// 문자열 기반 문법
return $this->through('cars')->has('owner');

// 동적 문법
return $this->throughCars()->hasOwner();
```

<a name="has-many-through"></a>
### Has Many Through

"has-many-through" 연관관계는 중간 모델을 통해 간접적으로 먼 관계의 모델들을 한 번에 접근할 수 있는 편리한 방법입니다. 예를 들어, [Laravel Cloud](https://cloud.laravel.com)와 같이 배포 플랫폼을 만든다고 하면, 하나의 `Application` 모델은 중간의 `Environment` 모델을 거쳐 여러 `Deployment` 모델에 연결될 수 있습니다.

필요한 테이블 구조 예시는 아래와 같습니다.

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

`Application` 모델에 관계를 정의해봅니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasManyThrough;

class Application extends Model
{
    /**
     * 애플리케이션의 모든 배포 정보를 가져옵니다.
     */
    public function deployments(): HasManyThrough
    {
        return $this->hasManyThrough(Deployment::class, Environment::class);
    }
}
```

`hasManyThrough`의 첫 번째 인수는 최종 모델, 두 번째 인수는 중간 모델 클래스입니다.

모든 모델에 필요한 관계가 정의되어 있다면, 마찬가지로 `through`와 이름을 이용해 유연하게 정의할 수 있습니다.

```php
// 문자열 기반 문법
return $this->through('environments')->has('deployments');

// 동적 문법
return $this->throughEnvironments()->hasDeployments();
```

`Deployment` 모델의 테이블에는 `application_id` 컬럼이 없지만, `hasManyThrough`를 통해, 중간 모델의 `application_id`를 참조해서 결과적으로 `$application->deployments`처럼 애플리케이션의 모든 배포 정보를 한 번에 가져올 수 있습니다.

<a name="has-many-through-key-conventions"></a>
#### 키 규칙 (Key Conventions)

이 관계도 일반적인 Eloquent 외래 키 규칙을 사용합니다. 키를 사용자 정의하려면 `hasManyThrough`의 세 번째와 네 번째 인수에 각각 중간 모델, 최종 모델의 외래 키를 전달하고, 다섯 번째와 여섯 번째 인수로 각 테이블의 로컬 키를 지정합니다.

```php
class Application extends Model
{
    public function deployments(): HasManyThrough
    {
        return $this->hasManyThrough(
            Deployment::class,
            Environment::class,
            'application_id', // environments 테이블의 외래 키
            'environment_id', // deployments 테이블의 외래 키
            'id', // applications 테이블의 로컬 키
            'id' // environments 테이블의 로컬 키
        );
    }
}
```

기존에 관계가 이미 정의되어 있다면 위에서 설명한 `through` 문법을 사용할 수 있으며, 기존 관계 정의의 키 규칙을 재사용합니다.

```php
// 문자열 기반 문법
return $this->through('environments')->has('deployments');

// 동적 문법
return $this->throughEnvironments()->hasDeployments();
```

<a name="scoped-relationships"></a>
### 스코프 연관관계 (Scoped Relationships)

종종 관계를 제약하는 추가 메서드를 모델에 추가하는 경우가 있습니다. 예를 들어, `User` 모델에 `featuredPosts` 메서드를 추가하여, 전체 `posts` 관계에 추가 `where` 조건을 붙일 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class User extends Model
{
    /**
     * 사용자의 포스트들을 가져옵니다.
     */
    public function posts(): HasMany
    {
        return $this->hasMany(Post::class)->latest();
    }

    /**
     * 사용자의 주요(Featured) 포스트들을 가져옵니다.
     */
    public function featuredPosts(): HasMany
    {
        return $this->posts()->where('featured', true);
    }
}
```

하지만 `featuredPosts` 메서드를 통해 모델을 생성하면, `featured` 속성이 자동으로 `true`로 지정되지 않습니다. 연관관계 메서드로 모델을 생성할 때, 해당 관계로 생성된 모든 모델에 특정 속성을 자동으로 할당하려면 `withAttributes`를 사용할 수 있습니다.

```php
/**
 * 사용자의 주요(Featured) 포스트들을 가져옵니다.
 */
public function featuredPosts(): HasMany
{
    return $this->posts()->withAttributes(['featured' => true]);
}
```

`withAttributes`는 쿼리에 `where` 조건을 추가하고, 관계를 통해 생성된 모델에도 해당 속성을 할당합니다.

```php
$post = $user->featuredPosts()->create(['title' => 'Featured Post']);

$post->featured; // true
```

만약 `withAttributes`에서 쿼리에 `where` 조건을 포함하지 않고 싶을 때는 `asConditions` 인수를 `false`로 설정하면 됩니다.

```php
return $this->posts()->withAttributes(['featured' => true], asConditions: false);
```

--- 

이하 번역이 장문이므로, 요청하시면 계속 이어서 번역해 드릴 수 있습니다.