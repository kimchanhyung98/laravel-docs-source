# Eloquent: 연관관계 (Eloquent: Relationships)

- [소개](#introduction)
- [연관관계 정의하기](#defining-relationships)
    - [일대일 / hasOne](#one-to-one)
    - [일대다 / hasMany](#one-to-many)
    - [일대다(역방향) / belongsTo](#one-to-many-inverse)
    - [여러 개 중 하나](#has-one-of-many)
    - [중간 모델을 통한 일대일](#has-one-through)
    - [중간 모델을 통한 일대다](#has-many-through)
- [스코프드(제약된) 연관관계](#scoped-relationships)
- [다대다 연관관계](#many-to-many)
    - [중간 테이블 컬럼 조회](#retrieving-intermediate-table-columns)
    - [중간 테이블 컬럼으로 필터링](#filtering-queries-via-intermediate-table-columns)
    - [중간 테이블 컬럼으로 정렬하기](#ordering-queries-via-intermediate-table-columns)
    - [사용자 정의 중간 테이블 모델 정의](#defining-custom-intermediate-table-models)
- [다형성 연관관계](#polymorphic-relationships)
    - [일대일](#one-to-one-polymorphic-relations)
    - [일대다](#one-to-many-polymorphic-relations)
    - [여러 개 중 하나](#one-of-many-polymorphic-relations)
    - [다대다](#many-to-many-polymorphic-relations)
    - [사용자 정의 다형성 타입](#custom-polymorphic-types)
- [동적 연관관계](#dynamic-relationships)
- [연관관계 쿼리하기](#querying-relations)
    - [연관관계 메서드 vs. 동적 프로퍼티](#relationship-methods-vs-dynamic-properties)
    - [연관관계의 존재 여부 쿼리](#querying-relationship-existence)
    - [연관관계의 결여 쿼리](#querying-relationship-absence)
    - [Morph To 연관관계 쿼리](#querying-morph-to-relationships)
- [연관된 모델의 집계](#aggregating-related-models)
    - [연관된 모델 개수 카운트](#counting-related-models)
    - [기타 집계 함수](#other-aggregate-functions)
    - [Morph To 관계에서 연관 모델 카운트](#counting-related-models-on-morph-to-relationships)
- [즉시 로딩(Eager Loading)](#eager-loading)
    - [제약 조건이 있는 즉시 로딩](#constraining-eager-loads)
    - [지연 즉시 로딩(Lazy Eager Loading)](#lazy-eager-loading)
    - [자동 즉시 로딩](#automatic-eager-loading)
    - [지연 로딩 방지](#preventing-lazy-loading)
- [연관된 모델 삽입 및 수정](#inserting-and-updating-related-models)
    - [`save` 메서드](#the-save-method)
    - [`create` 메서드](#the-create-method)
    - [Belongs To 관계](#updating-belongs-to-relationships)
    - [다대다 관계](#updating-many-to-many-relationships)
- [부모 타임스탬프 동기화(Touching Parent Timestamps)](#touching-parent-timestamps)

<a name="introduction"></a>
## 소개 (Introduction)

데이터베이스 테이블들은 종종 서로 연관되어 있습니다. 예를 들어, 블로그 포스트는 여러 개의 댓글을 가질 수 있고, 주문은 주문을 한 사용자와 연관될 수도 있습니다. Eloquent는 이러한 연관관계의 관리와 사용을 매우 쉽게 만들어주며, 여러 종류의 일반적인 연관관계를 지원합니다:

<div class="content-list" markdown="1">

- [일대일](#one-to-one)
- [일대다](#one-to-many)
- [다대다](#many-to-many)
- [중간 모델을 통한 일대일](#has-one-through)
- [중간 모델을 통한 일대다](#has-many-through)
- [일대일(다형성)](#one-to-one-polymorphic-relations)
- [일대다(다형성)](#one-to-many-polymorphic-relations)
- [다대다(다형성)](#many-to-many-polymorphic-relations)

</div>

<a name="defining-relationships"></a>
## 연관관계 정의하기 (Defining Relationships)

Eloquent 연관관계는 Eloquent 모델 클래스 내의 메서드로 정의합니다. 또한, 연관관계 메서드는 강력한 [쿼리 빌더](/docs/master/queries)로도 작동하므로 체이닝 및 쿼리 기능을 제공합니다. 예를 들어, `posts` 연관관계에 추가적인 쿼리 조건을 체이닝할 수 있습니다:

```php
$user->posts()->where('active', 1)->get();
```

자, 본격적으로 연관관계를 사용하기에 앞서, Eloquent가 지원하는 각 연관관계 타입을 정의하는 방법을 먼저 알아보겠습니다.

<a name="one-to-one"></a>
### 일대일 / hasOne (One to One / Has One)

일대일 관계는 데이터베이스의 가장 기본적인 종류의 연관관계입니다. 예를 들어, `User` 모델이 하나의 `Phone` 모델과만 연관된 상황이 이에 해당합니다. 이 관계를 정의하려면, `User` 모델에 `phone` 메서드를 추가하고, 이 메서드에서 `hasOne` 메서드를 호출해 반환합니다. `hasOne` 메서드는 모델의 `Illuminate\Database\Eloquent\Model` 기본 클래스에서 제공됩니다:

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

`hasOne` 메서드의 첫 번째 인수는 연관 모델 클래스명을 전달합니다. 연관관계를 정의한 후에는 Eloquent의 동적 프로퍼티(dynamic property)를 사용해 연관된 데이터를 조회할 수 있습니다. 동적 프로퍼티란, 연관관계 메서드를 마치 모델의 프로퍼티처럼 접근할 수 있게 해주는 기능입니다:

```php
$phone = User::find(1)->phone;
```

Eloquent는 부모 모델명을 기준으로 연관관계의 외래 키(foreign key)를 자동으로 결정합니다. 위의 예에서는 `Phone` 모델이 자동으로 `user_id` 컬럼을 외래 키로 가진다고 간주합니다. 이 규칙을 변경하고 싶다면, `hasOne` 메서드의 두 번째 인수로 외래 키를 지정할 수 있습니다:

```php
return $this->hasOne(Phone::class, 'foreign_key');
```

추가로, Eloquent는 외래 키 컬럼이 부모 모델의 기본 키(primary key) 값과 일치한다고 가정합니다. 즉, `user_id` 컬럼에 부모(`User`)의 `id`값이 들어갑니다. 만약 기본 키가 `id`가 아니거나, 모델의 `$primaryKey` 속성을 사용하지 않는 경우, 세 번째 인수로 로컬 키를 지정할 수 있습니다:

```php
return $this->hasOne(Phone::class, 'foreign_key', 'local_key');
```

<a name="one-to-one-defining-the-inverse-of-the-relationship"></a>
#### 관계의 역방향 정의하기

이제 `User` 모델에서 `Phone` 모델에 접근할 수 있게 되었습니다. 이번에는 `Phone` 모델에서 해당 전화번호를 가진 사용자를 참조할 수 있는 관계를 정의해 보겠습니다. `hasOne` 관계의 역방향은 `belongsTo` 메서드를 이용해 정의합니다:

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

`user` 메서드를 호출하면, Eloquent는 `Phone` 모델의 `user_id` 컬럼 값과 일치하는 `User` 모델의 `id`를 검색합니다.

Eloquent는 관계 메서드 이름에 `_id`를 붙여 외래 키 이름을 자동으로 결정합니다. 위 예제를 기준으로 `user_id` 컬럼이 자동으로 사용됩니다. 만약 외래 키 이름이 다르다면, `belongsTo` 메서드의 두 번째 인자로 외래 키 이름을 지정할 수 있습니다:

```php
/**
 * 전화번호를 소유한 사용자를 가져옵니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class, 'foreign_key');
}
```

만약 부모 모델의 기본 키가 `id`가 아니거나, 다른 컬럼을 사용해 연관 모델을 찾고 싶다면, 세 번째 인수로 부모 테이블의 키 이름을 지정할 수 있습니다:

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

일대다 관계는 하나의 모델이 여러 자식 모델을 갖는 상황에서 사용합니다. 예를 들어, 하나의 블로그 포스트는 무한대의 댓글을 가질 수 있습니다. 일대다 관계도 다른 Eloquent 관계와 마찬가지로, 모델에 메서드를 정의해 만들 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Post extends Model
{
    /**
     * 블로그 포스트의 댓글 목록을 가져옵니다.
     */
    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class);
    }
}
```

Eloquent는 `Comment` 모델의 외래 키 컬럼을 자동으로 결정합니다. 관례상, 부모 모델명을 스네이크 케이스로 바꾸고 `_id`를 붙여서 사용합니다. 위의 예제에서는 `Comment` 모델이 `post_id` 컬럼을 가진다고 가정합니다.

관계 메서드를 정의하면, 해당 관계를 동적 프로퍼티로 접근해 [컬렉션](/docs/master/eloquent-collections)으로 읽을 수 있습니다:

```php
use App\Models\Post;

$comments = Post::find(1)->comments;

foreach ($comments as $comment) {
    // ...
}
```

연관관계 메서드는 쿼리 빌더로도 사용되므로, 추가적 조건을 체이닝할 수도 있습니다:

```php
$comment = Post::find(1)->comments()
    ->where('title', 'foo')
    ->first();
```

`hasOne`과 마찬가지로, 추가 인수로 외래 키와 로컬 키를 지정할 수도 있습니다:

```php
return $this->hasMany(Comment::class, 'foreign_key');

return $this->hasMany(Comment::class, 'foreign_key', 'local_key');
```

<a name="automatically-hydrating-parent-models-on-children"></a>
#### 자식 모델에 부모 모델 자동 로딩(Hydrating)

Eloquent 즉시 로딩을 사용하더라도, 자식 모델 반복문에서 부모 모델을 참조하면 "N + 1" 쿼리 문제가 발생할 수 있습니다:

```php
$posts = Post::with('comments')->get();

foreach ($posts as $post) {
    foreach ($post->comments as $comment) {
        echo $comment->post->title;
    }
}
```

위 예제처럼, 각 `Comment`에서 다시 부모 `Post`에 접근하면 추가 쿼리가 발생합니다. 이때, `hasMany` 관계 정의 시 `chaperone` 메서드를 호출하면 Eloquent가 자식 모델에 부모 모델을 자동으로 로딩해줍니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Post extends Model
{
    /**
     * 블로그 포스트의 댓글 목록을 가져옵니다.
     */
    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class)->chaperone();
    }
}
```

또는, 실행 시점에 관계를 즉시 로딩(eager loading)하면서 `chaperone`을 사용하도록 할 수도 있습니다:

```php
use App\Models\Post;

$posts = Post::with([
    'comments' => fn ($comments) => $comments->chaperone(),
])->get();
```

<a name="one-to-many-inverse"></a>
### 일대다(역방향) / belongsTo (One to Many (Inverse) / Belongs To)

이제 포스트의 모든 댓글에 접근할 수 있으니, 이번엔 댓글이 자신의 부모 포스트에 접근할 수 있도록 하겠습니다. `hasMany` 관계의 역방향은 자식 모델에 `belongsTo` 메서드를 이용해 정의합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Comment extends Model
{
    /**
     * 댓글을 소유한 포스트를 가져옵니다.
     */
    public function post(): BelongsTo
    {
        return $this->belongsTo(Post::class);
    }
}
```

관계 정의 이후엔 `post` 동적 관계 프로퍼티로 부모에 접근할 수 있습니다:

```php
use App\Models\Comment;

$comment = Comment::find(1);

return $comment->post->title;
```

위와 같이 호출하면, Eloquent는 `Comment` 모델의 `post_id` 컬럼과 일치하는 `Post` 모델의 `id`를 참조합니다.

기본적으로 Eloquent는 관계 메서드명 뒤에 부모 모델의 기본 키 컬럼명을 붙여 외래 키를 결정합니다(`post_id`). 만약 관례와 다른 이름을 쓴다면, 두 번째 인자로 외래 키 이름을 명시해줍니다:

```php
/**
 * 댓글을 소유한 포스트를 가져옵니다.
 */
public function post(): BelongsTo
{
    return $this->belongsTo(Post::class, 'foreign_key');
}
```

부모 모델의 기본 키가 `id`가 아니거나, 다른 컬럼을 사용한다면 세 번째 인자로 부모 테이블의 키 이름을 지정합니다:

```php
/**
 * 댓글을 소유한 포스트를 가져옵니다.
 */
public function post(): BelongsTo
{
    return $this->belongsTo(Post::class, 'foreign_key', 'owner_key');
}
```

<a name="default-models"></a>
#### 기본 모델(Default Models)

`belongsTo`, `hasOne`, `hasOneThrough`, `morphOne` 관계에서는 관계 결과가 `null`일 경우 반환할 "기본 모델"을 지정할 수 있습니다. 이 패턴은 [Null Object 패턴](https://en.wikipedia.org/wiki/Null_Object_pattern)이라 부르며, 코드에서 조건 체크를 줄이는 데 도움을 줍니다. 예시에서 `user` 관계가 비어있으면 빈 `App\Models\User` 모델을 반환합니다:

```php
/**
 * 포스트의 작성자를 가져옵니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault();
}
```

기본 모델에 속성값을 담고 싶다면 `withDefault`에 배열이나 클로저를 전달할 수 있습니다:

```php
/**
 * 포스트의 작성자를 가져옵니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault([
        'name' => 'Guest Author',
    ]);
}

/**
 * 포스트의 작성자를 가져옵니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault(function (User $user, Post $post) {
        $user->name = 'Guest Author';
    });
}
```

<a name="querying-belongs-to-relationships"></a>
#### Belongs To 관계 쿼리(Querying Belongs To Relationships)

"Belongs To" 관계의 자식 모델을 쿼리할 때, 일반적으로는 `where` 조건으로 Eloquent 모델을 조회할 수 있습니다:

```php
use App\Models\Post;

$posts = Post::where('user_id', $user->id)->get();
```

좀 더 편리하게, `whereBelongsTo` 메서드를 사용하면 관계 및 외래 키를 자동으로 처리해줍니다:

```php
$posts = Post::whereBelongsTo($user)->get();
```

`whereBelongsTo`는 [컬렉션](/docs/master/eloquent-collections) 인스턴스도 인수로 받을 수 있으며, 이 경우 주어진 모든 부모 모델에 속한 데이터를 조회합니다:

```php
$users = User::where('vip', true)->get();

$posts = Post::whereBelongsTo($users)->get();
```

기본적으로 Laravel은 넘어온 모델의 클래스명으로 관계를 유추하지만, 두 번째 인수로 관계명을 명시할 수도 있습니다:

```php
$posts = Post::whereBelongsTo($user, 'author')->get();
```

<a name="has-one-of-many"></a>
### 여러 개 중 하나 (Has One of Many)

때때로, 한 모델이 여러 연관 모델을 갖고 있더라도 특정 관계에서 "가장 최신" 혹은 "가장 오래된" 연관 모델만 간편하게 조회하고 싶을 수 있습니다. 예를 들어, `User`는 여러 개의 `Order`와 연관될 수 있지만, 가장 최근 주문만 쉽게 조회하고 싶다면 `hasOne` 관계에 `ofMany` 관련 메서드를 조합할 수 있습니다:

```php
/**
 * 가장 최근 사용자의 주문을 가져옵니다.
 */
public function latestOrder(): HasOne
{
    return $this->hasOne(Order::class)->latestOfMany();
}
```

"가장 오래된"(처음) 연관 모델을 조회하는 메서드도 정의할 수 있습니다:

```php
/**
 * 가장 오래된 사용자의 주문을 가져옵니다.
 */
public function oldestOrder(): HasOne
{
    return $this->hasOne(Order::class)->oldestOfMany();
}
```

기본적으로 `latestOfMany` 및 `oldestOfMany`는 모델의 기본 키를 기준으로 정렬합니다. 하지만, 다른 기준으로 단일 모델을 조회하고 싶다면 `ofMany` 메서드를 사용하여 정렬 컬럼과 집계함수(`min` or `max`)를 지정할 수 있습니다:

```php
/**
 * 가장 비싼 사용자의 주문을 가져옵니다.
 */
public function largestOrder(): HasOne
{
    return $this->hasOne(Order::class)->ofMany('price', 'max');
}
```

> [!WARNING]
> PostgreSQL은 UUID 컬럼에 대해 `MAX` 함수를 지원하지 않으므로, PostgreSQL의 UUID 컬럼과 one-of-many 관계를 함께 사용할 수 없습니다.

<a name="converting-many-relationships-to-has-one-relationships"></a>
#### "다수" 관계를 Has One 관계로 변환

`latestOfMany`, `oldestOfMany`, `ofMany`로 단일 모델을 조회할 때, 이미 "hasMany" 관계가 정의되어 있다면 이를 쉽게 "hasOne" 관계로 변환할 수 있습니다. 즉, 기존 hasMany 리턴값에 `one` 메서드를 체이닝할 수 있습니다:

```php
/**
 * 사용자의 주문 목록.
 */
public function orders(): HasMany
{
    return $this->hasMany(Order::class);
}

/**
 * 가장 비싼 사용자의 주문.
 */
public function largestOrder(): HasOne
{
    return $this->orders()->one()->ofMany('price', 'max');
}
```

`one` 메서드는 `HasManyThrough` 관계를 `HasOneThrough` 관계로 변환하는 데도 사용할 수 있습니다:

```php
public function latestDeployment(): HasOneThrough
{
    return $this->deployments()->one()->latestOfMany();
}
```

<a name="advanced-has-one-of-many-relationships"></a>
#### 심화: 여러 개 중 하나(Has One of Many) 관계

보다 복잡한 "여러 개 중 하나" 관계도 가능하며, 예시로 `Product` 모델이 여러 `Price`와 연관되어 있고, 새 가격 데이터가 사전에 입력되어 `published_at` 컬럼으로 발행일을 관리한다고 가정해보겠습니다.

즉, "아직 미래가 아닌 최신 발행 가격"을 구하고 싶고, 만약 같은 `published_at` 이라면 id가 더 큰 가격을 선택하고 싶은 케이스입니다. 이 땐 `ofMany`에 소트 기준 컬럼 배열을 첫 인수로, 쿼리 제약을 위한 클로저를 두 번째 인수로 전달합니다:

```php
/**
 * 상품의 현재 가격을 가져옵니다.
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
### 중간 모델을 통한 일대일 (Has One Through)

"has-one-through" 관계는 중간 모델을 거쳐 최종 모델과 1:1로 연결될 때 사용합니다. 직접 관계가 없는 두 테이블이 중간 테이블을 통해 연결되는 패턴입니다.

예를 들어, 차량 수리소 애플리케이션에서, 각 `Mechanic`는 하나의 `Car`와, 각 `Car`는 하나의 `Owner`와 연관되어 있는 경우, 정비사와 차주는 직접적 관계는 없지만, `Car` 모델을 통해 관계를 맺을 수 있습니다. 테이블 구조 예시는 다음과 같습니다:

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

이 관계를 `Mechanic` 모델에 정의하면 다음과 같습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasOneThrough;

class Mechanic extends Model
{
    /**
     * 차의 소유자를 가져옵니다.
     */
    public function carOwner(): HasOneThrough
    {
        return $this->hasOneThrough(Owner::class, Car::class);
    }
}
```

`hasOneThrough` 메서드의 첫 번째 인수는 최종적으로 접근하고자 하는 모델명, 두 번째 인수는 중간 모델명을 전달합니다.

만약 관계가 모든 모델에 이미 정의되어 있다면, `through` 메서드와 관계명(`cars`, `owner`)을 사용해 유창하게 플루언트 방식으로 정의할 수도 있습니다:

```php
// 문자열 기반 방식...
return $this->through('cars')->has('owner');

// 동적 방식...
return $this->throughCars()->hasOwner();
```

<a name="has-one-through-key-conventions"></a>
#### 키 관례

Eloquent의 기본 외래 키 규칙을 따르지만, 직접 키를 지정하고 싶다면 `hasOneThrough`의 3~6번째 인수로 각각 설정할 수 있습니다. 즉, 3번째는 중간 모델의 외래 키, 4번째는 최종 모델의 외래 키, 5번째는 시작점 로컬 키, 6번째는 중간 모델의 로컬 키입니다:

```php
class Mechanic extends Model
{
    /**
     * 차의 소유자를 가져옵니다.
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

플루언트 방식(`through`)도 이미 정의한 키 관례를 재활용할 수 있는 이점이 있습니다:

```php
// 문자열 기반 방식...
return $this->through('cars')->has('owner');

// 동적 방식...
return $this->throughCars()->hasOwner();
```

<a name="has-many-through"></a>
### 중간 모델을 통한 일대다 (Has Many Through)

"has-many-through" 관계는 중간 관계를 통해 보다 먼(간접) 모델들에 접근해야 할 때 매우 유용합니다. 예를 들어, Laravel Cloud와 같은 배포 플랫폼을 만든다고 가정할 때, `Application`은 중간의 `Environment` 모델을 통해 여러 `Deployment` 모델과 연결될 수 있습니다. 테이블 구조 예시는 다음과 같습니다:

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

이 구조로 `Application` 모델에 관계를 정의하면 다음과 같이 됩니다:

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

`hasManyThrough`의 첫 번째 인수는 최종 모델명, 두 번째는 중간 모델명을 전달합니다.

이미 관련 모델별로 관계가 정의되어 있다면, `through` 메서드와 관계명을 활용해 유연하게 정의할 수 있습니다:

```php
// 문자열 기반 방식...
return $this->through('environments')->has('deployments');

// 동적 방식...
return $this->throughEnvironments()->hasDeployments();
```

`Deployment` 모델의 테이블에 `application_id` 컬럼이 없더라도, Eloquent는 `Environment` 모델의 `application_id` 컬럼 기반으로 올바른 관계를 구성합니다.

<a name="has-many-through-key-conventions"></a>
#### 키 관례

키를 직접 지정하고 싶다면 `hasManyThrough`의 3~6번째 인수로 각각 중간 모델의 외래 키, 최종 모델의 외래 키, 시작점 로컬 키, 중간 모델의 로컬 키를 설정할 수 있습니다:

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

관계가 미리 정의되어 있다면 플루언트(`through`) 방식이 키 설정을 재사용할 수 있어 더욱 유연합니다:

```php
// 문자열 기반 방식...
return $this->through('environments')->has('deployments');

// 동적 방식...
return $this->throughEnvironments()->hasDeployments();
```

<a name="scoped-relationships"></a>
### 스코프드(제약된) 연관관계 (Scoped Relationships)

추가적인 제약 조건이 필요한 연관관계 메서드를 별도로 모델에 정의할 수도 있습니다. 예를 들어, `User` 모델의 `posts` 관계를 확장해 `featuredPosts` 메서드에 추가적인 where 조건을 줄 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class User extends Model
{
    /**
     * 사용자의 포스트 목록.
     */
    public function posts(): HasMany
    {
        return $this->hasMany(Post::class)->latest();
    }

    /**
     * 사용자의 추천 포스트 목록.
     */
    public function featuredPosts(): HasMany
    {
        return $this->posts()->where('featured', true);
    }
}
```

하지만 위 `featuredPosts` 메서드로 모델을 생성할 경우 `featured` 속성이 true로 자동 지정되지 않습니다. 관계 메서드를 통해 생성되는 모델에 값이 자동으로 할당되길 원한다면, `withAttributes` 메서드를 사용할 수 있습니다:

```php
/**
 * 사용자의 추천 포스트 목록.
 */
public function featuredPosts(): HasMany
{
    return $this->posts()->withAttributes(['featured' => true]);
}
```

`withAttributes`는 주어진 속성을 where 조건에도 추가하고, 해당 속성값을 지정해 모델을 생성하게 해줍니다:

```php
$post = $user->featuredPosts()->create(['title' => 'Featured Post']);

$post->featured; // true
```

where 조건에 해당 값을 추가하지 않고 싶다면, `asConditions` 인수를 false로 전달하면 됩니다:

```php
return $this->posts()->withAttributes(['featured' => true], asConditions: false);
```

<a name="many-to-many"></a>
## 다대다 연관관계 (Many to Many Relationships)

다대다 관계는 `hasOne`, `hasMany`보다 조금 더 복잡합니다. 대표적으로 사용자는 여러 역할(roles)을 가질 수 있고, 하나의 역할은 여러 사용자에게 할당될 수 있습니다. 예를 들어, 사용자는 "Author", "Editor" 역할에 모두 속할 수 있으며, 이 역할들은 여러 사용자에게 겹쳐 할당될 수도 있습니다.

<a name="many-to-many-table-structure"></a>
#### 테이블 구조 (Table Structure)

이 관계를 구현하려면 `users`, `roles`, `role_user` 세 개의 테이블이 필요합니다. `role_user`는 알파벳순 정렬로 결합된 이름으로 구성되며, `user_id`, `role_id` 두 컬럼을 가집니다. 이 테이블이 두 테이블간 중간 역할을 하게 됩니다.

하나의 역할은 여러 사용자에게 할당될 수 있으므로, 단순히 `roles` 테이블에 `user_id`를 두는 것은 적합하지 않습니다. 여러 사용자가 같은 역할을 사용할 수 있기에 `role_user` 중간 테이블을 따로 둬야 합니다. 구조는 다음과 같습니다:

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

다대다 관계는 `belongsToMany` 메서드를 반환하는 메서드를 통해 정의합니다. 이 메서드는 모든 Eloquent 모델에서 사용할 수 있습니다. 예를 들어, `User` 모델에 `roles` 메서드를 정의합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class User extends Model
{
    /**
     * 사용자가 가진 역할 목록.
     */
    public function roles(): BelongsToMany
    {
        return $this->belongsToMany(Role::class);
    }
}
```

정의한 관계는 `roles` 동적 관계 프로퍼티로 접근할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

foreach ($user->roles as $role) {
    // ...
}
```

관계도 쿼리 빌더로 사용할 수 있으므로, 조건 체이닝도 가능하며:

```php
$roles = User::find(1)->roles()->orderBy('name')->get();
```

중간 테이블명은 기본적으로 두 모델명을 알파벳순으로 조합해 만듭니다. 수동으로 중간 테이블명을 지정할 수도 있고, 추가 인수로 컬럼명까지 지정할 수 있습니다:

```php
return $this->belongsToMany(Role::class, 'role_user');
return $this->belongsToMany(Role::class, 'role_user', 'user_id', 'role_id');
```

<a name="many-to-many-defining-the-inverse-of-the-relationship"></a>
#### 관계의 역방향 정의 (Defining the Inverse of the Relationship)

다대다 관계의 역방향도 동일하게, 대상 모델에 `belongsToMany` 메서드를 반환하는 메서드를 작성하면 됩니다. 예시의 `Role` 모델에선 다음처럼 구현할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class Role extends Model
{
    /**
     * 이 역할을 가진 사용자 목록.
     */
    public function users(): BelongsToMany
    {
        return $this->belongsToMany(User::class);
    }
}
```

역방향 관계도 앞서 설명한 모든 옵션이 동일하게 적용됩니다.

<a name="retrieving-intermediate-table-columns"></a>
### 중간 테이블 컬럼 조회 (Retrieving Intermediate Table Columns)

다대다 관계는 중간 테이블이 필수입니다. Eloquent는 중간 테이블의 값을 다루는 편리한 방법을 제공합니다. 예를 들어, `User`가 여러 `Role` 모델을 가지고 있다면, 각 `Role`에서 중간 테이블 컬럼은 `pivot` 속성을 통해 접근할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

foreach ($user->roles as $role) {
    echo $role->pivot->created_at;
}
```

`Role` 모델 인스턴스는 자동으로 `pivot` 속성을 갖게 되고, 여기엔 중간 테이블의 내용이 담깁니다.

중간 테이블에 추가 컬럼이 있다면, 관계정의 시 `withPivot`을 통해 지정해야 접근할 수 있습니다:

```php
return $this->belongsToMany(Role::class)->withPivot('active', 'created_by');
```

중간 테이블에 타임스탬프 처리가 자동으로 필요하다면 `withTimestamps`를 호출합니다:

```php
return $this->belongsToMany(Role::class)->withTimestamps();
```

> [!WARNING]
> Eloquent가 자동으로 타임스탬프를 관리하는 중간 테이블은 반드시 `created_at`, `updated_at` 컬럼이 모두 존재해야 합니다.

<a name="customizing-the-pivot-attribute-name"></a>
#### `pivot` 속성명 커스터마이징

중간 테이블 값은 기본적으로 `pivot`으로 접근하지만, 의미에 맞게 이름을 변경하고 싶다면 `as` 메서드를 사용할 수 있습니다. 예를 들어, 사용자가 팟캐스트를 구독하는 경우, `pivot` 대신 `subscription`으로 바꿀 수 있습니다:

```php
return $this->belongsToMany(Podcast::class)
    ->as('subscription')
    ->withTimestamps();
```

이제 관계 데이터는 지정한 이름(`subscription`)으로 접근하면 됩니다:

```php
$users = User::with('podcasts')->get();

foreach ($users->flatMap->podcasts as $podcast) {
    echo $podcast->subscription->created_at;
}
```

<a name="filtering-queries-via-intermediate-table-columns"></a>
### 중간 테이블 컬럼으로 필터링 (Filtering Queries via Intermediate Table Columns)

`belongsToMany` 관계에서 다양한 메서드(`wherePivot`, `wherePivotIn`, `wherePivotNotIn`, `wherePivotBetween`, `wherePivotNotBetween`, `wherePivotNull`, `wherePivotNotNull`)로 중간 테이블 컬럼 값을 조건으로 걸 수 있습니다:

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

`wherePivot`은 쿼리 조건만 추가할 뿐, 새 모델 생성시 지정값을 포함하진 않습니다. 둘 다 하고 싶다면 `withPivotValue`를 사용합니다:

```php
return $this->belongsToMany(Role::class)
    ->withPivotValue('approved', 1);
```

<a name="ordering-queries-via-intermediate-table-columns"></a>
### 중간 테이블 컬럼으로 정렬하기 (Ordering Queries via Intermediate Table Columns)

`belongsToMany` 관계에선 `orderByPivot`로 중간 테이블 컬럼을 기준으로 정렬할 수 있습니다. 예를 들어, 사용자의 최신 뱃지를 가져오는 쿼리:

```php
return $this->belongsToMany(Badge::class)
    ->where('rank', 'gold')
    ->orderByPivot('created_at', 'desc');
```

<a name="defining-custom-intermediate-table-models"></a>
### 사용자 정의 중간 테이블 모델 정의 (Defining Custom Intermediate Table Models)

다대다 관계의 중간 테이블을 직접 모델로 표현하고 싶다면, 관계 정의 시 `using` 메서드로 커스텀 pivot 모델을 지정할 수 있습니다.

커스텀 pivot 모델은 `Illuminate\Database\Eloquent\Relations\Pivot`를 상속해야 하며, 다형성 pivot 모델의 경우엔 `MorphPivot`를 상속해야 합니다. 예시:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class Role extends Model
{
    /**
     * 이 역할을 가진 사용자 목록.
     */
    public function users(): BelongsToMany
    {
        return $this->belongsToMany(User::class)->using(RoleUser::class);
    }
}
```

`RoleUser` 모델 예시:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Relations\Pivot;

class RoleUser extends Pivot
{
    // ...
}
```

> [!WARNING]
> pivot 모델에서는 `SoftDeletes` 트레이트를 사용할 수 없습니다. pivot 레코드의 소프트 삭제가 필요하다면 pivot을 별도의 Eloquent 모델로 전환해야 합니다.

<a name="custom-pivot-models-and-incrementing-ids"></a>
#### 커스텀 Pivot 모델과 증가하는 ID

만약 자동 증가(primary key auto-increment)가 필요한 다대다 관계 커스텀 pivot 모델을 사용한다면, 해당 모델에 `incrementing` 속성을 `true`로 설정해야 합니다.

```php
/**
 * ID가 자동 증가하는지 여부.
 *
 * @var bool
 */
public $incrementing = true;
```

<a name="polymorphic-relationships"></a>
## 다형성 연관관계 (Polymorphic Relationships)

다형성(polymorphic) 연관관계는 하나의 자식 모델이 여러 종류의 부모 모델과 연결될 수 있도록 해줍니다. 예를 들어, 블로그 포스트와 동영상 모두에 댓글을 달 수 있다고 할 때, `Comment` 모델 하나로 `Post`, `Video` 모두와 관계를 맺게 할 수 있습니다.

<a name="one-to-one-polymorphic-relations"></a>
### 일대일(다형성) (One to One (Polymorphic))

<a name="one-to-one-polymorphic-table-structure"></a>
#### 테이블 구조

일대일 다형성 관계는 일반 일대일과 비슷하지만, 하나의 모델이 여러 종류의 부모와 연결된다는 점이 다릅니다. 예를 들어, 블로그 `Post`, `User`가 하나의 `Image` 모델과 다형성 관계로 연결될 수 있습니다. 이를 위해선 다음 구조가 필요합니다:

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

`images` 테이블의 `imageable_id`, `imageable_type` 컬럼은 각각 소유자 id, 소유자 타입(모델 클래스명 또는 별칭)을 저장합니다.

<a name="one-to-one-polymorphic-model-structure"></a>
#### 모델 구조

모델정의 예시는 다음과 같습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class Image extends Model
{
    /**
     * 상위(소유) 모델(user 또는 post) 가져오기.
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
     * 포스트의 이미지를 가져옵니다.
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
     * 사용자의 이미지를 가져옵니다.
     */
    public function image(): MorphOne
    {
        return $this->morphOne(Image::class, 'imageable');
    }
}
```

<a name="one-to-one-polymorphic-retrieving-the-relationship"></a>
#### 관계 조회

정의가 끝나면, 관계 프로퍼티로 이미지를 가져올 수 있습니다:

```php
use App\Models\Post;

$post = Post::find(1);

$image = $post->image;
```

반대로, `Image`에서 부모 모델(소유자, 즉 `Post` 또는 `User`)에 접근하려면 `imageable` 동적 프로퍼티를 사용합니다:

```php
use App\Models\Image;

$image = Image::find(1);

$imageable = $image->imageable;
```

`imageable` 관계는 소유한 모델이 `Post`인지 `User`인지에 따라 각각의 인스턴스를 반환합니다.

<a name="morph-one-to-one-key-conventions"></a>
#### 키 관례

필요할 경우, 다형성 자식 모델이 참조하는 "id"/"type" 컬럼 이름을 지정할 수 있습니다. 반드시 관계 이름을 첫 인수로, 그 뒤로 타입 컬럼과 id 컬럼명을 넘겨주어야 합니다. 대개 PHP의 `__FUNCTION__`를 사용할 수도 있습니다:

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
### 일대다(다형성) (One to Many (Polymorphic))

<a name="one-to-many-polymorphic-table-structure"></a>
#### 테이블 구조

일대다 다형성 관계는 일반 일대다와 비슷하지만, 한 자식 모델이 여러 종류의 부모와 연관될 수 있다는 특징이 있습니다. 예를 들어, 사용자들이 포스트와 동영상 모두에 `댓글`을 남기는 경우, 다음 구조를 사용할 수 있습니다:

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

모델정의 예시는 다음과 같습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class Comment extends Model
{
    /**
     * 부모 모델(post, video) 참조.
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
     * 포스트의 모든 댓글.
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
     * 동영상의 모든 댓글.
     */
    public function comments(): MorphMany
    {
        return $this->morphMany(Comment::class, 'commentable');
    }
}
```

<a name="one-to-many-polymorphic-retrieving-the-relationship"></a>
#### 관계 조회

정의된 관계는 동적 프로퍼티로 쉽게 조회할 수 있습니다:

```php
use App\Models\Post;

$post = Post::find(1);

foreach ($post->comments as $comment) {
    // ...
}
```

댓글에서 부모 모델을 가져올 때는 `commentable` 동적 프로퍼티를 사용합니다:

```php
use App\Models\Comment;

$comment = Comment::find(1);

$commentable = $comment->commentable;
```

`commentable` 관계는 실제 부모가 `Post`인지 `Video`인지에 따라 해당 인스턴스를 반환합니다.

<a name="polymorphic-automatically-hydrating-parent-models-on-children"></a>
#### 자식 모델에 부모 모델 자동 로드(Hydrating)

즉시 로딩(eager loading)을 본다 해도 자식 루프에서 부모 모형을 참조하면 N+1 쿼리 문제가 발생할 수 있습니다:

```php
$posts = Post::with('comments')->get();

foreach ($posts as $post) {
    foreach ($post->comments as $comment) {
        echo $comment->commentable->title;
    }
}
```

이럴 때, `morphMany` 관계 정의시 `chaperone`을 호출하면 부모를 자식 모델에 즉시 로딩하게 됩니다:

```php
class Post extends Model
{
    /**
     * 포스트의 모든 댓글.
     */
    public function comments(): MorphMany
    {
        return $this->morphMany(Comment::class, 'commentable')->chaperone();
    }
}
```

관계 즉시 로딩시에도 사용할 수 있습니다:

```php
use App\Models\Post;

$posts = Post::with([
    'comments' => fn ($comments) => $comments->chaperone(),
])->get();
```

<a name="one-of-many-polymorphic-relations"></a>
### 여러 개 중 하나(다형성) (One of Many (Polymorphic))

여러 다형성 모델 중 "가장 최신"이나 "가장 오래된" 모델만 조회하고 싶을 때가 있습니다. 예를 들어, `User`가 여러 `Image`와 연관될 수 있을 때, 가장 최근 이미지를 조회하려면 다음처럼 작성할 수 있습니다:

```php
/**
 * 사용자의 최신 이미지.
 */
public function latestImage(): MorphOne
{
    return $this->morphOne(Image::class, 'imageable')->latestOfMany();
}
```

"가장 오래된" 이미지는 `oldestOfMany`로 정의할 수 있습니다:

```php
/**
 * 사용자의 가장 오래된 이미지.
 */
public function oldestImage(): MorphOne
{
    return $this->morphOne(Image::class, 'imageable')->oldestOfMany();
}
```

특정 컬럼 기준으로 단일 모델을 검색하고 싶으면 `ofMany` 메서드를 이용합니다:

```php
/**
 * 사용자의 가장 많은 좋아요를 받은 이미지.
 */
public function bestImage(): MorphOne
{
    return $this->morphOne(Image::class, 'imageable')->ofMany('likes', 'max');
}
```

> [!NOTE]
> 보다 고급 다형성 "여러 개 중 하나" 관계는 [여러 개 중 하나 관계 문서](#advanced-has-one-of-many-relationships)를 참고하세요.

<a name="many-to-many-polymorphic-relations"></a>
### 다대다(다형성) (Many to Many (Polymorphic))

<a name="many-to-many-polymorphic-table-structure"></a>
#### 테이블 구조

다대다 다형성 관계는 morph one, morph many보다 조금 복잡합니다. 예를 들어, `Post`, `Video`가 모두 `Tag`와 다형성 다대다 관계를 맺는 경우, 단일 테이블에서 고유한 태그들을 관리할 수 있습니다. 테이블 구조는 다음과 같습니다:

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
> 다형성 다대다 관계를 본격적으로 사용하기 전, 우선 [일반 다대다 관계](#many-to-many) 문서를 참고하는 것이 좋습니다.

<a name="many-to-many-polymorphic-model-structure"></a>
#### 모델 구조

`Post`, `Video` 모델 모두 `morphToMany`를 통해 `tags` 관계를 정의합니다. 첫 번째 인수는 연관 모델명, 두 번째 인수는 관계명(`taggable`)입니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphToMany;

class Post extends Model
{
    /**
     * 포스트의 태그 목록.
     */
    public function tags(): MorphToMany
    {
        return $this->morphToMany(Tag::class, 'taggable');
    }
}
```

<a name="many-to-many-polymorphic-defining-the-inverse-of-the-relationship"></a>
#### 관계의 역방향 정의

`Tag` 모델에서는 `posts`, `videos` 각각에 대해 `morphedByMany`로 관계를 정의합니다. 첫 번째 인수는 연관 모델명, 두 번째는 관계명입니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphToMany;

class Tag extends Model
{
    /**
     * 이 태그가 할당된 모든 포스트.
     */
    public function posts(): MorphToMany
    {
        return $this->morphedByMany(Post::class, 'taggable');
    }

    /**
     * 이 태그가 할당된 모든 동영상.
     */
    public function videos(): MorphToMany
    {
        return $this->morphedByMany(Video::class, 'taggable');
    }
}
```

<a name="many-to-many-polymorphic-retrieving-the-relationship"></a>
#### 관계 조회

관계정의 후에는 동적 프로퍼티로 대상 관계를 사용할 수 있습니다:

```php
use App\Models\Post;

$post = Post::find(1);

foreach ($post->tags as $tag) {
    // ...
}
```

반대로 태그에서 관련 부모 모델을 참조하려면, 관계 메서드명(`posts`, `videos`)에 맞춰 접근할 수 있습니다:

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
### 사용자 정의 다형성 타입 (Custom Polymorphic Types)

Laravel은 기본적으로 관련 모델의 FQCN을 type 컬럼에 저장합니다. 예를 들어 위의 댓글 예시라면 `commentable_type`에 `App\Models\Post` 또는 `App\Models\Video` 값이 들어갑니다. 내부 구조에 의존하지 않으려면 type을 별칭(별도 문자열)으로 매핑할 수 있습니다:

```php
use Illuminate\Database\Eloquent\Relations\Relation;

Relation::enforceMorphMap([
    'post' => 'App\Models\Post',
    'video' => 'App\Models\Video',
]);
```

이 코드는 보통 `AppServiceProvider`의 `boot` 메서드나 별도 서비스 프로바이더에 작성합니다.

모델의 morph alias(별칭)를 런타임에 구하려면 `getMorphClass` 메서드를, alias에 해당하는 클래스명을 구하려면 `Relation::getMorphedModel`을 사용할 수 있습니다:

```php
use Illuminate\Database\Eloquent\Relations\Relation;

$alias = $post->getMorphClass();

$class = Relation::getMorphedModel($alias);
```

> [!WARNING]
> 기존 애플리케이션에 morph map을 추가하면, DB의 모든 morphable `*_type` 컬럼 값을 별칭 값으로 변환해야 정상 동작합니다.

<a name="dynamic-relationships"></a>
### 동적 연관관계 (Dynamic Relationships)

`resolveRelationUsing` 메서드를 사용하여 실행 중에 Eloquent 모델 간 관계를 정의할 수 있습니다. 일반 실무보다는 패키지 개발 시 유용합니다.

첫 인수는 관계명, 두 번째 인수는 모델 인스턴스를 받아 관계를 반환하는 클로저입니다. 보통 [서비스 프로바이더](/docs/master/providers)에서 구성합니다:

```php
use App\Models\Order;
use App\Models\Customer;

Order::resolveRelationUsing('customer', function (Order $orderModel) {
    return $orderModel->belongsTo(Customer::class, 'customer_id');
});
```

> [!WARNING]
> 동적 관계를 정의할 때는 반드시 외래 키 등 모든 키 인수를 명시적으로 지정해야 합니다.

<a name="querying-relations"></a>
## 연관관계 쿼리하기 (Querying Relations)

모든 Eloquent 관계는 메서드로 정의되기에, 쿼리를 실행하지 않고도 관계 인스턴스를 얻을 수 있습니다. 또한 관계 메서드는 모두 [쿼리 빌더](/docs/master/queries)로도 동작해 추가 조건을 자유롭게 체이닝할 수 있습니다.

예를 들어, 블로그에서 `User` 모델이 여러 `Post`와 연결된 경우:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class User extends Model
{
    /**
     * 사용자의 모든 포스트.
     */
    public function posts(): HasMany
    {
        return $this->hasMany(Post::class);
    }
}
```

관계 쿼리 예시:

```php
use App\Models\User;

$user = User::find(1);

$user->posts()->where('active', 1)->get();
```

Laravel [쿼리 빌더](/docs/master/queries)의 모든 메서드를 관계에도 사용할 수 있습니다.

<a name="chaining-orwhere-clauses-after-relationships"></a>
#### 관계 뒤에 orWhere 체이닝하기

관계 쿼리에 orWhere를 체이닝할 때 너무 조심해야 합니다. orWhere의 조건이 관계 제약과 동일 레벨로 묶이기 때문입니다:

```php
$user->posts()
    ->where('active', 1)
    ->orWhere('votes', '>=', 100)
    ->get();
```

위 예는 아래와 같은 SQL을 만듭니다. or 절이 전체 조건을 분리시키기 때문에 사용자를 제한하지 않습니다:

```sql
select *
from posts
where user_id = ? and active = 1 or votes >= 100
```

이 문제를 피하려면 [논리 그룹](/docs/master/queries#logical-grouping)으로 감싸줘야 합니다:

```php
use Illuminate\Database\Eloquent\Builder;

$user->posts()
    ->where(function (Builder $query) {
        return $query->where('active', 1)
            ->orWhere('votes', '>=', 100);
    })
    ->get();
```

이제 쿼리가 올바르게 그룹핑되어 사용자가 제한됩니다:

```sql
select *
from posts
where user_id = ? and (active = 1 or votes >= 100)
```

<a name="relationship-methods-vs-dynamic-properties"></a>
### 연관관계 메서드 vs. 동적 프로퍼티

추가 조건이 필요 없다면 관계를 속성처럼 바로 접근해도 됩니다:

```php
use App\Models\User;

$user = User::find(1);

foreach ($user->posts as $post) {
    // ...
}
```

동적 관계 프로퍼티는 "지연 로딩" 방식입니다. 실제로 접근할 때만 SQL 쿼리가 발생하므로, 대량 처리나 탐색시 [즉시 로딩](#eager-loading)을 하여 쿼리 수를 줄이는 것이 성능상 유리합니다.

<a name="querying-relationship-existence"></a>
### 연관관계의 존재 여부 쿼리 (Querying Relationship Existence)

관계의 존재 여부로 결과를 제한하고 싶을 때가 있습니다. 예를 들어, 한 개 이상의 댓글이 달린 포스트만 조회하려면 `has`나 `orHas` 메서드를 사용합니다:

```php
use App\Models\Post;

// 댓글이 한 개 이상 달린 포스트만 조회
$posts = Post::has('comments')->get();
```

연산자와 카운트를 지정할 수도 있습니다:

```php
// 댓글이 3개 이상인 포스트만 조회
$posts = Post::has('comments', '>=', 3)->get();
```

중첩된 관계도 "점 표기법(dot notation)"을 사용해 조회할 수 있습니다:

```php
// 이미지가 달린 댓글이 있는 포스트만 조회
$posts = Post::has('comments.images')->get();
```

더 복잡한 조건은 `whereHas`, `orWhereHas`로 가능합니다:

```php
use Illuminate\Database\Eloquent\Builder;

// 댓글 내용이 code%로 시작하는 글만 조회
$posts = Post::whereHas('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
})->get();

// 해당 조건을 만족하는 댓글이 10개 이상인 글
$posts = Post::whereHas('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
}, '>=', 10)->get();
```

> [!WARNING]
> 관계 존재 쿼리는 현재 DB 간 교차 쿼리를 지원하지 않습니다. 모든 관계는 동일한 데이터베이스에서만 가능합니다.

<a name="many-to-many-relationship-existence-queries"></a>
#### 다대다 관계 존재 쿼리

`whereAttachedTo` 메서드를 사용하면 모델(혹은 컬렉션)에 연결되어 있는 관계 데이터만 조회할 수 있습니다:

```php
$users = User::whereAttachedTo($role)->get();
```

컬렉션도 사용할 수 있습니다:

```php
$tags = Tag::whereLike('name', '%laravel%')->get();

$posts = Post::whereAttachedTo($tags)->get();
```

<a name="inline-relationship-existence-queries"></a>
#### 인라인 관계 존재 쿼리

단일 where 조건만으로 관계 존재 여부를 체크할 땐 `whereRelation`, `orWhereRelation`, `whereMorphRelation`, `orWhereMorphRelation`가 편리합니다:

```php
use App\Models\Post;

// 승인되지 않은 댓글이 달린 포스트만 조회
$posts = Post::whereRelation('comments', 'is_approved', false)->get();
```

연산자 사용도 가능합니다:

```php
$posts = Post::whereRelation(
    'comments', 'created_at', '>=', now()->minus(hours: 1)
)->get();
```

<a name="querying-relationship-absence"></a>
### 연관관계의 결여 쿼리 (Querying Relationship Absence)

연관관계가 없는 경우만 조회하고 싶다면 `doesntHave`, `orDoesntHave` 등을 사용합니다:

```php
use App\Models\Post;

$posts = Post::doesntHave('comments')->get();
```

더 복잡한 경우에는 `whereDoesntHave`, `orWhereDoesntHave`를 사용해서 조건을 추가할 수 있습니다:

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::whereDoesntHave('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
})->get();
```

중첩 관계도 "점 표기법"으로 가능하며, 아래 경우에는 댓글이 없거나, banned 유저가 작성한 댓글이 없는 포스트만 조회됩니다:

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::whereDoesntHave('comments.author', function (Builder $query) {
    $query->where('banned', 1);
})->get();
```

<a name="querying-morph-to-relationships"></a>
### Morph To 관계 쿼리 (Querying Morph To Relationships)

"morph to" 관계의 존재 여부 쿼리는 `whereHasMorph`, `whereDoesntHaveMorph`로 처리할 수 있습니다. 첫 인수는 관계명, 두 번째 인수는 포함 대상 모델, 세 번째는 쿼리 제약을 위한 클로저입니다:

```php
use App\Models\Comment;
use App\Models\Post;
use App\Models\Video;
use Illuminate\Database\Eloquent\Builder;

// 제목이 code%로 시작하는 포스트/비디오에 연결된 모든 댓글 조회
$comments = Comment::whereHasMorph(
    'commentable',
    [Post::class, Video::class],
    function (Builder $query) {
        $query->where('title', 'like', 'code%');
    }
)->get();

// code%로 시작하는 포스트에 연결된 댓글 중, 제목이 일치하지 않는 것
$comments = Comment::whereDoesntHaveMorph(
    'commentable',
    Post::class,
    function (Builder $query) {
        $query->where('title', 'like', 'code%');
    }
)->get();
```

종종 다형성 관계의 타입에 따라 조건을 달리 걸어야 할 때가 있습니다. 이때 두 번째 인수로 `$type`을 받을 수 있습니다:

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

때론 부모 모델 종류별로 자식 관계를 쿼리해야 할 때도 있습니다. 이럴 땐 `whereMorphedTo`, `whereNotMorphedTo`를 사용하면 morph type 매핑을 자동 적용합니다:

```php
$comments = Comment::whereMorphedTo('commentable', $post)
    ->orWhereMorphedTo('commentable', $video)
    ->get();
```

<a name="querying-all-morph-to-related-models"></a>
#### 모든 다형성 관계 모델 쿼리

모든 다형성 대상 모델을 한 번에 쿼리하고 싶다면, 모델 배열 대신 `*`을 와일드카드로 지정하십시오. Laravel이 테이블에서 해당 타입 후보를 찾아 자동으로 쿼리합니다:

```php
use Illuminate\Database\Eloquent\Builder;

$comments = Comment::whereHasMorph('commentable', '*', function (Builder $query) {
    $query->where('title', 'like', 'foo%');
})->get();
```

<a name="aggregating-related-models"></a>
## 연관된 모델의 집계 (Aggregating Related Models)

<a name="counting-related-models"></a>
### 연관된 모델 개수 카운트 (Counting Related Models)

관계 모델을 실제로 불러오지 않고 단순히 개수만 알고 싶을 땐 `withCount` 메서드를 사용할 수 있습니다. 이 메서드는 결과 모델에 `{관계}_count` 속성을 추가합니다:

```php
use App\Models\Post;

$posts = Post::withCount('comments')->get();

foreach ($posts as $post) {
    echo $post->comments_count;
}
```

배열로 여러 관계의 카운트와 조건도 지정할 수 있습니다:

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::withCount(['votes', 'comments' => function (Builder $query) {
    $query->where('content', 'like', 'code%');
}])->get();

echo $posts[0]->votes_count;
echo $posts[0]->comments_count;
```

결과값을 별칭(alias)으로 지정해, 동일 관계에 여러 카운트 조건도 가능합니다:

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
#### 지연 카운트 로딩

`loadCount` 메서드로, 이미 조회한 모델에 대해 나중에 카운트만 불러올 수 있습니다:

```php
$book = Book::first();

$book->loadCount('genres');
```

조건도 추가할 수 있습니다:

```php
$book->loadCount(['reviews' => function (Builder $query) {
    $query->where('rating', 5);
}])
```

<a name="relationship-counting-and-custom-select-statements"></a>
#### 관계 카운트와 select문 조합

`withCount`와 `select`를 함께 사용할 땐, 반드시 `withCount`를 `select` 이후에 호출하세요:

```php
$posts = Post::select(['title', 'body'])
    ->withCount('comments')
    ->get();
```

<a name="other-aggregate-functions"></a>
### 기타 집계 함수 (Other Aggregate Functions)

`withCount` 외에도, `withMin`, `withMax`, `withAvg`, `withSum`, `withExists` 등 여러 집계 메서드가 있습니다. 결과 모델에는 `{관계}_{함수}_{컬럼}` 속성이 추가됩니다:

```php
use App\Models\Post;

$posts = Post::withSum('comments', 'votes')->get();

foreach ($posts as $post) {
    echo $post->comments_sum_votes;
}
```

별도로 alias를 지정할 수도 있습니다:

```php
$posts = Post::withSum('comments as total_comments', 'votes')->get();

foreach ($posts as $post) {
    echo $post->total_comments;
}
```

지연형(Deferred) aggregate 메서드도 있으며, 이미 로드한 모델에 aggregate 결과를 추가할 수 있습니다:

```php
$post = Post::first();

$post->loadSum('comments', 'votes');
```

`select`와 조합할 땐, aggregate 메서드를 `select` 이후에 호출해야 합니다:

```php
$posts = Post::select(['title', 'body'])
    ->withExists('comments')
    ->get();
```

<a name="counting-related-models-on-morph-to-relationships"></a>
### Morph To 관계에서 연관 모델 카운트

Morph To 관계에서도 즉시 로딩과 함께 관계별 카운트도 로드할 수 있습니다. 아래 예시처럼, `ActivityFeed` 모델의 `parentable` morphTo 관계에서 각 부모 타입별로 관련 모델 카운트를 eager load합니다:

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
#### Morph To 지연 카운트 로딩

이미 로드한 Morph To 관계 모델들의 관계별 카운트를 뒤늦게 불러오려면 `loadMorphCount`를 사용합니다:

```php
$activities = ActivityFeed::with('parentable')->get();

$activities->loadMorphCount('parentable', [
    Photo::class => ['tags'],
    Post::class => ['comments'],
]);
```

<a name="eager-loading"></a>
## 즉시 로딩(Eager Loading)

Eloquent 관계를 속성처럼 접근하면 "지연 로딩(lazy loading)" 방식이 기본입니다. 첫 접근 시점에 쿼리가 발생하게 되며, 이 때문에 "N+1 쿼리" 문제가 생길 수 있습니다. 이를 피하려면 부모 모델 조회 시점에 미리 관계까지 읽어오는 "즉시 로딩(eager loading)"을 적용해야 합니다.

예를 들어, `Book` 모델이 `Author` 모델과 연결된 케이스에서:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Book extends Model
{
    /**
     * 이 책의 저자.
     */
    public function author(): BelongsTo
    {
        return $this->belongsTo(Author::class);
    }
}
```

일반적으로 모든 책과 저자를 가져올 때:

```php
use App\Models\Book;

$books = Book::all();

foreach ($books as $book) {
    echo $book->author->name;
}
```

이 경우 책 전체를 한 번 쿼리하고, 각 책마다 저자 쿼리(N), 총 N+1개의 쿼리가 발생합니다. 즉시 로딩을 사용하여 쿼리를 2회로 줄일 수 있습니다:

```php
$books = Book::with('author')->get();

foreach ($books as $book) {
    echo $book->author->name;
}
```

이제 전체 책 쿼리 1회, 저자 전체 쿼리 1회 등 총 2번의 쿼리를 실행하게 됩니다.

<a name="eager-loading-multiple-relationships"></a>
#### 여러 관계 즉시 로딩

여러 관계를 한 번에 읽으려면 `with` 메서드에 배열로 관계 이름들을 넘깁니다:

```php
$books = Book::with(['author', 'publisher'])->get();
```

<a name="nested-eager-loading"></a>
#### 중첩 즉시 로딩

관계의 관계를 즉시 로딩하고 싶을 땐 "점 표기법"을 사용합니다:

```php
$books = Book::with('author.contacts')->get();
```

또는 중첩 관계를 중첩 배열로 지정할 수도 있습니다:

```php
$books = Book::with([
    'author' => [
        'contacts',
        'publisher',
    ],
])->get();
```

<a name="nested-eager-loading-morphto-relationships"></a>
#### morphTo 관계의 중첩 즉시 로딩

`morphTo` 관계의 하위 관계도 즉시 로딩하려면 `morphWith`를 활용합니다:

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
#### 특정 컬럼만 즉시 로딩

모든 컬럼 대신 일부만 조회할 수도 있습니다:

```php
$books = Book::with('author:id,name,book_id')->get();
```

> [!WARNING]
> 반드시 외래 키와 id 컬럼은 컬럼 리스트에 포함해야 합니다.

<a name="eager-loading-by-default"></a>
#### 항상 즉시 로딩

특정 관계를 항상 즉시 로딩하고 싶다면 모델에 `$with` 속성을 선언하세요:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Book extends Model
{
    /**
     * 항상 불러올 관계.
     *
     * @var array
     */
    protected $with = ['author'];

    /**
     * 책의 저자를 가져옵니다.
     */
    public function author(): BelongsTo
    {
        return $this->belongsTo(Author::class);
    }

    /**
     * 책의 장르를 가져옵니다.
     */
    public function genre(): BelongsTo
    {
        return $this->belongsTo(Genre::class);
    }
}
```

단일 쿼리에선 `without`이나 `withOnly`로 예외 처리도 가능합니다:

```php
$books = Book::without('author')->get();

$books = Book::withOnly('genre')->get();
```

<a name="constraining-eager-loads"></a>
### 제약 조건이 있는 즉시 로딩 (Constraining Eager Loads)

관계를 즉시 로딩하면서 추가 조건도 지정하고 싶다면 관계명을 key로, 쿼리 클로저를 value로 하는 배열을 `with` 메서드에 전달하세요:

```php
use App\Models\User;

$users = User::with(['posts' => function ($query) {
    $query->where('title', 'like', '%code%');
}])->get();
```

기타 쿼리 빌더 메서드도 자유롭게 체이닝할 수 있습니다:

```php
$users = User::with(['posts' => function ($query) {
    $query->orderBy('created_at', 'desc');
}])->get();
```

<a name="constraining-eager-loading-of-morph-to-relationships"></a>
#### morphTo 관계 즉시 로딩 제약조건

`morphTo` 관계는 타입별로 각각 쿼리가 나가므로, 각 쿼리에 제약 조건도 따로 줄 수 있습니다:

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

<a name="constraining-eager-loads-with-relationship-existence"></a>
#### 관계 존재 조건과 즉시 로딩 동시 사용

관계를 즉시 로딩하면서 동시에 관계 존재 조건 `withWhereHas`를 사용하려면 다음처럼 할 수 있습니다:

```php
use App\Models\User;

$users = User::withWhereHas('posts', function ($query) {
    $query->where('featured', true);
})->get();
```

<a name="lazy-eager-loading"></a>
### 지연 즉시 로딩 (Lazy Eager Loading)

부모 모델을 조회한 이후에 관계를 조건적으로 로딩해야 할 때는 `load`, `loadMissing`을 사용합니다:

```php
use App\Models\Book;

$books = Book::all();

if ($condition) {
    $books->load('author', 'publisher');
}
```

조건도 줄 수 있습니다:

```php
$author->load(['books' => function ($query) {
    $query->orderBy('published_date', 'asc');
}]);
```

이미 로드된 관계는 생략하고 필요한 것만 불러오려면 `loadMissing`을 사용합니다:

```php
$book->loadMissing('author');
```

<a name="nested-lazy-eager-loading-morphto"></a>
#### morphTo의 중첩 지연 즉시 로딩

`loadMorph`는 morphTo 관계의 다양한 타입별 하위 관계까지 지연 즉시 로딩할 수 있게 해줍니다:

```php
$activities = ActivityFeed::with('parentable')
    ->get()
    ->loadMorph('parentable', [
        Event::class => ['calendar'],
        Photo::class => ['tags'],
        Post::class => ['author'],
    ]);
```

<a name="automatic-eager-loading"></a>
### 자동 즉시 로딩 (Automatic Eager Loading)

> [!WARNING]
> 이 기능은 현재 베타 상태입니다. 피드백에 따라 기능이 예고 없이 변경될 수 있습니다.

Laravel에서는 관계 프로퍼티에 접근하면 자동으로 lazy eager loading이 발생하도록 할 수 있습니다. 애플리케이션의 `AppServiceProvider`의 `boot`에서 아래 메서드를 호출하면 활성화됩니다:

```php
use Illuminate\Database\Eloquent\Model;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Model::automaticallyEagerLoadRelationships();
}
```

이 기능이 활성화되면, 관계 프로퍼티에 처음 접근하는 순간 전체 컬렉션의 해당 관계가 한 번에 lazy eager loading됩니다:

```php
use App\Models\User;

$users = User::all();

foreach ($users as $user) {
    foreach ($user->posts as $post) {
        foreach ($post->comments as $comment) {
            echo $comment->content;
        }
    }
}
```

자동 즉시 로딩을 전역이 아닌 특정 컬렉션에만 적용하려면 `withRelationshipAutoloading`을 사용하세요:

```php
$users = User::where('vip', true)->get();

return $users->withRelationshipAutoloading();
```

<a name="preventing-lazy-loading"></a>
### 지연 로딩 방지 (Preventing Lazy Loading)

즉시 로딩의 이점이 크기 때문에, 아예 lazy loading을 막고 싶을 때도 있습니다. 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 환경에 따라 `preventLazyLoading`을 호출하면, lazy loading 시 `Illuminate\Database\LazyLoadingViolationException` 예외가 발생합니다:

```php
use Illuminate\Database\Eloquent\Model;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Model::preventLazyLoading(! $this->app->isProduction());
}
```

서버가 예외 대신 로그만 남기도록 하려면 `handleLazyLoadingViolationUsing`을 사용합니다:

```php
Model::handleLazyLoadingViolationUsing(function (Model $model, string $relation) {
    $class = $model::class;

    info("Attempted to lazy load [{$relation}] on model [{$class}].");
});
```

<a name="inserting-and-updating-related-models"></a>
## 연관된 모델 삽입 및 수정 (Inserting and Updating Related Models)

<a name="the-save-method"></a>
### save 메서드 (The `save` Method)

Eloquent는 관계에 새로운 모델을 추가하기 위한 다양한 메서드를 제공합니다. 예를 들어, 포스트에 댓글을 추가할 때, `post_id`를 직접 지정할 필요없이 관계의 `save` 메서드를 사용할 수 있습니다:

```php
use App\Models\Comment;
use App\Models\Post;

$comment = new Comment(['message' => 'A new comment.']);

$post = Post::find(1);

$post->comments()->save($comment);
```

동적 프로퍼티가 아닌, 관계 메서드를 호출해야 합니다. `save`는 자동으로 외래 키 값을 채워줍니다.

여러 모델을 저장하려면 `saveMany`를 사용하세요:

```php
$post = Post::find(1);

$post->comments()->saveMany([
    new Comment(['message' => 'A new comment.']),
    new Comment(['message' => 'Another new comment.']),
]);
```

`save`나 `saveMany`는 부모 모델에 이미 로딩된 관계에는 자동 반영되지 않으므로, 저장 후 관계를 다시 사용하려면 `refresh`로 갱신할 수 있습니다:

```php
$post->comments()->save($comment);

$post->refresh();

// 새로 저장한 댓글을 포함해 전체 댓글을 조회
$post->comments;
```

<a name="the-push-method"></a>
#### 모델 및 관계 전부 재귀 저장

모델과 함께 하위 포함된 관계까지 한꺼번에 저장하려면 `push`를 사용합니다. 부모, 자식, 손자 관계까지 모두 저장됩니다:

```php
$post = Post::find(1);

$post->comments[0]->message = 'Message';
$post->comments[0]->author->name = 'Author Name';

$post->push();
```

이벤트 발생 없이 조용하게 저장하려면 `pushQuietly`를 사용합니다:

```php
$post->pushQuietly();
```

<a name="the-create-method"></a>
### create 메서드 (The `create` Method)

`save`, `saveMany` 이외에도, `create` 메서드로도 관계에 데이터를 한 번에 추가할 수 있습니다. 이때는 전체 Eloquent 인스턴스가 아니라 단순 배열을 넘깁니다:

```php
use App\Models\Post;

$post = Post::find(1);

$comment = $post->comments()->create([
    'message' => 'A new comment.',
]);
```

`createMany`로 여러 모델을 한 번에 생성할 수도 있습니다:

```php
$post = Post::find(1);

$post->comments()->createMany([
    ['message' => 'A new comment.'],
    ['message' => 'Another new comment.'],
]);
```

이벤트 없이 조용히 생성하려면 `createQuietly`, `createManyQuietly`를 사용합니다:

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

`findOrNew`, `firstOrNew`, `firstOrCreate`, `updateOrCreate` 등도 관계를 통해 호출 가능하며, 자세한 내용은 [업서트 문서](/docs/master/eloquent#upserts)를 참고하세요.

> [!NOTE]
> `create` 사용 전에는 꼭 [대량 할당(Mass Assignment)](/docs/master/eloquent#mass-assignment) 보안 문서를 읽어보세요.

<a name="updating-belongs-to-relationships"></a>
### Belongs To 관계

자식 모델에 새 부모 모델을 할당하려면 `associate` 메서드를 사용합니다. 아래는 `User`가 `Account`와 `belongsTo` 관계를 가질 때, 사용자에 계정을 연결하는 예시입니다:

```php
use App\Models\Account;

$account = Account::find(10);

$user->account()->associate($account);

$user->save();
```

반대로 부모 모델을 제거하려면 `dissociate`를 사용하세요. 이 메서드는 외래 키 값을 null로 만듭니다:

```php
$user->account()->dissociate();

$user->save();
```

<a name="updating-many-to-many-relationships"></a>
### 다대다 관계

<a name="attaching-detaching"></a>
#### Attach / Detach

다대다 관계에선 `attach`, `detach`로 관계를 쉽게 추가하거나 제거할 수 있습니다. 예를 들어, 사용자가 역할을 가질 때:

```php
use App\Models\User;

$user = User::find(1);

$user->roles()->attach($roleId);
```

`attach`에 추가 데이터를 중간 테이블로 함께 넣을 수도 있습니다:

```php
$user->roles()->attach($roleId, ['expires' => $expires]);
```

관계를 제거하려면 `detach`를 사용합니다. 전체 관계 제거도 가능합니다:

```php
// 단일 역할 해제
$user->roles()->detach($roleId);

// 모든 역할 해제
$user->roles()->detach();
```

여러 ID를 배열로 입력할 수도 있습니다:

```php
$user = User::find(1);

$user->roles()->detach([1, 2, 3]);

$user->roles()->attach([
    1 => ['expires' => $expires],
    2 => ['expires' => $expires],
]);
```

<a name="syncing-associations"></a>
#### 관계 동기화(Syncing Associations)

`sync` 메서드는 중간 테이블을 배열로 전달한 ID 목록과 딱 맞게 맞춰줍니다. 배열에 없는 ID들은 중간 테이블에서 제거됩니다:

```php
$user->roles()->sync([1, 2, 3]);
```

추가 데이터도 동시 입력할 수 있습니다:

```php
$user->roles()->sync([1 => ['expires' => true], 2, 3]);
```

동일한 데이터로 동기화하려면 `syncWithPivotValues`를 사용하세요:

```php
$user->roles()->syncWithPivotValues([1, 2, 3], ['active' => true]);
```

배열에 없는 값들도 그대로 남기고 싶으면 `syncWithoutDetaching`을 사용합니다:

```php
$user->roles()->syncWithoutDetaching([1, 2, 3]);
```

<a name="toggling-associations"></a>
#### 관계 토글(Toggling Associations)

`toggle` 메서드는 관계의 존재 여부에 따라 붙고 떼는 상태를 반전시켜줍니다:

```php
$user->roles()->toggle([1, 2, 3]);
```

pivot 값도 함께 넘길 수 있습니다:

```php
$user->roles()->toggle([
    1 => ['expires' => true],
    2 => ['expires' => true],
]);
```

<a name="updating-a-record-on-the-intermediate-table"></a>
#### 중간 테이블 레코드 수정

중간 테이블의 데이터를 수정하려면 `updateExistingPivot`을 사용합니다:

```php
$user = User::find(1);

$user->roles()->updateExistingPivot($roleId, [
    'active' => false,
]);
```

<a name="touching-parent-timestamps"></a>
## 부모 타임스탬프 동기화 (Touching Parent Timestamps)

모델이 `belongsTo` 또는 `belongsToMany` 관계를 가지는 부모 모델이 있을 때(예: 댓글이 포스트에 속함), 자식 모델이 수정되면 부모의 타임스탬프를 자동으로 갱신하고 싶은 경우가 있습니다.

예를 들어, `Comment` 모델이 수정될 때, 상위 `Post`의 `updated_at`이 자동 갱신되게 하려면 자식 모델에서 `touches` 속성에 관계명을 추가합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Comment extends Model
{
    /**
     * 자동으로 갱신할 관계.
     *
     * @var array
     */
    protected $touches = ['post'];

    /**
     * 댓글이 속한 포스트.
     */
    public function post(): BelongsTo
    {
        return $this->belongsTo(Post::class);
    }
}
```

> [!WARNING]
> 부모 모델의 타임스탬프는 자식 모델을 Eloquent의 `save` 메서드로 수정한 경우에만 자동으로 갱신됩니다.
