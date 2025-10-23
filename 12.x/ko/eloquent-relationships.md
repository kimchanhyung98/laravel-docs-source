# Eloquent: 연관관계 (Eloquent: Relationships)

- [소개](#introduction)
- [연관관계 정의](#defining-relationships)
    - [일대일 / hasOne](#one-to-one)
    - [일대다 / hasMany](#one-to-many)
    - [일대다(역방향) / belongsTo](#one-to-many-inverse)
    - [여러 개 중 하나 / hasOne of Many](#has-one-of-many)
    - [중간을 거치는 일대일 / hasOneThrough](#has-one-through)
    - [중간을 거치는 일대다 / hasManyThrough](#has-many-through)
- [스코프 연관관계](#scoped-relationships)
- [다대다 연관관계](#many-to-many)
    - [중간 테이블 컬럼 조회](#retrieving-intermediate-table-columns)
    - [중간 테이블 컬럼을 통한 쿼리 필터링](#filtering-queries-via-intermediate-table-columns)
    - [중간 테이블 컬럼을 통한 쿼리 정렬](#ordering-queries-via-intermediate-table-columns)
    - [커스텀 중간 테이블 모델 정의](#defining-custom-intermediate-table-models)
- [폴리모픽 연관관계](#polymorphic-relationships)
    - [일대일](#one-to-one-polymorphic-relations)
    - [일대다](#one-to-many-polymorphic-relations)
    - [여러 개 중 하나](#one-of-many-polymorphic-relations)
    - [다대다](#many-to-many-polymorphic-relations)
    - [커스텀 폴리모픽 타입](#custom-polymorphic-types)
- [동적 연관관계](#dynamic-relationships)
- [연관관계 쿼리](#querying-relations)
    - [연관관계 메서드 vs 동적 속성](#relationship-methods-vs-dynamic-properties)
    - [연관관계 존재 쿼리](#querying-relationship-existence)
    - [연관관계 부재 쿼리](#querying-relationship-absence)
    - [Morph To 관계 쿼리](#querying-morph-to-relationships)
- [관계 모델 집계](#aggregating-related-models)
    - [관계 모델 개수 세기](#counting-related-models)
    - [기타 집계 함수](#other-aggregate-functions)
    - [Morph To 관계 모델 개수 세기](#counting-related-models-on-morph-to-relationships)
- [즉시 로딩 (Eager Loading)](#eager-loading)
    - [즉시 로딩 제한](#constraining-eager-loads)
    - [지연 즉시 로딩](#lazy-eager-loading)
    - [자동 즉시 로딩](#automatic-eager-loading)
    - [지연 로딩 방지](#preventing-lazy-loading)
- [연관관계 모델 삽입 및 갱신](#inserting-and-updating-related-models)
    - [`save` 메서드](#the-save-method)
    - [`create` 메서드](#the-create-method)
    - [Belongs To 연관관계](#updating-belongs-to-relationships)
    - [Many to Many 연관관계](#updating-many-to-many-relationships)
- [부모 타임스탬프 갱신하기](#touching-parent-timestamps)

<a name="introduction"></a>
## 소개 (Introduction)

데이터베이스 테이블들은 종종 서로 연관되어 있습니다. 예를 들어, 블로그 게시글은 여러 개의 댓글을 가질 수 있고, 주문은 주문을 한 사용자와 연결될 수 있습니다. Eloquent는 이러한 연관관계를 쉽게 관리하고 사용할 수 있도록 다양한 일반적인 관계 유형을 지원하며, 사용법도 간편합니다:

<div class="content-list" markdown="1">

- [일대일](#one-to-one)
- [일대다](#one-to-many)
- [다대다](#many-to-many)
- [중간 테이블을 거치는 일대일](#has-one-through)
- [중간 테이블을 거치는 일대다](#has-many-through)
- [일대일 (폴리모픽)](#one-to-one-polymorphic-relations)
- [일대다 (폴리모픽)](#one-to-many-polymorphic-relations)
- [다대다 (폴리모픽)](#many-to-many-polymorphic-relations)

</div>

<a name="defining-relationships"></a>
## 연관관계 정의 (Defining Relationships)

Eloquent 연관관계는 Eloquent 모델 클래스 안에 메서드로 정의합니다. 연관관계는 강력한 [쿼리 빌더](/docs/12.x/queries)의 역할도 하므로, 메서드 체이닝 및 쿼리 기능을 풍부하게 제공합니다. 예를 들어, `posts`라는 연관관계에 추가 조건을 체이닝할 수도 있습니다:

```php
$user->posts()->where('active', 1)->get();
```

이제 본격적으로 연관관계 사용을 알아보기 전에, Eloquent가 지원하는 각 연관관계의 정의 방법부터 살펴보겠습니다.

<a name="one-to-one"></a>
### 일대일 / hasOne (One to One / Has One)

일대일 관계는 가장 기본적인 데이터베이스 연관관계 유형입니다. 예를 들어, `User` 모델이 하나의 `Phone` 모델과 연관될 수 있습니다. 이 관계를 정의하려면 `User` 모델에 `phone`이라는 메서드를 생성하고, 해당 메서드에서 `hasOne` 메서드를 호출하여 반환합니다. `hasOne` 메서드는 모델의 `Illuminate\Database\Eloquent\Model` 기본 클래스에서 제공됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasOne;

class User extends Model
{
    /**
     * 사용자의 전화번호를 가져옵니다.
     */
    public function phone(): HasOne
    {
        return $this->hasOne(Phone::class);
    }
}
```

`hasOne` 메서드의 첫 번째 인수는 연관되는 모델 클래스명입니다. 연관관계를 정의한 후에는 Eloquent의 동적 속성을 통해 연관 레코드를 조회할 수 있습니다. 동적 속성은 메서드명을 속성처럼 사용할 수 있게 해줍니다:

```php
$phone = User::find(1)->phone;
```

Eloquent는 연관관계의 외래 키 이름을 부모 모델 이름을 기준으로 자동으로 결정합니다. 위 예시에서는 `Phone` 모델에 `user_id`라는 외래 키가 있다고 간주합니다. 만약 이 규칙을 변경하고 싶다면, `hasOne`의 두 번째 인수로 외래 키를 지정할 수 있습니다:

```php
return $this->hasOne(Phone::class, 'foreign_key');
```

또한, 외래 키의 값은 부모 모델의 기본 키 컬럼(`id`)과 일치해야 한다고 Eloquent는 가정합니다. 만약 부모 모델의 기본 키를 변경하거나, 다른 컬럼을 사용하고 싶다면 `hasOne`의 세 번째 인수로 로컬 키를 지정할 수 있습니다:

```php
return $this->hasOne(Phone::class, 'foreign_key', 'local_key');
```

<a name="one-to-one-defining-the-inverse-of-the-relationship"></a>
#### 관계의 역방향 정의

이제 `User` 모델에서 `Phone` 모델에 접근할 수 있게 되었습니다. 반대로, `Phone` 모델에서 해당 전화번호를 소유한 사용자를 조회하고 싶다면 어떻게 해야 할까요? `hasOne` 관계의 역방향은 `belongsTo` 메서드를 사용하여 정의할 수 있습니다:

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

`user` 메서드를 호출하면, Eloquent는 `Phone` 모델의 `user_id` 컬럼과 일치하는 `User` 모델의 `id` 값을 검색하게 됩니다.

Eloquent는 연관관계 메서드의 이름에 `_id`를 붙여 외래 키 이름을 추론합니다. 따라서 이 예시에서는 `Phone` 모델에 `user_id` 컬럼이 있다고 가정합니다. 만약 외래 키 이름이 `user_id`가 아니라면, `belongsTo`의 두 번째 인수로 커스텀 키 이름을 지정하면 됩니다:

```php
/**
 * 이 전화번호를 소유한 사용자를 가져옵니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class, 'foreign_key');
}
```

부모 모델의 기본 키가 `id`가 아니거나, 다른 컬럼으로 연관 모델을 찾고 싶을 경우에는, 세 번째 인수로 부모 테이블의 커스텀 키를 지정할 수 있습니다:

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
### 일대다 / hasMany (One to Many / Has Many)

일대다 관계는 하나의 부모 모델이 여러 개의 자식 모델을 가지게 될 때 사용합니다. 예를 들어 블로그 게시글이 여러 개의 댓글을 갖는 경우입니다. 다른 모든 Eloquent 관계와 마찬가지로, 일대다 관계도 메서드 하나로 정의합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Post extends Model
{
    /**
     * 이 게시글의 댓글 목록을 가져옵니다.
     */
    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class);
    }
}
```

Eloquent는 `Comment` 모델의 외래 키 컬럼도 자동으로 추론합니다. 기본적으로, 부모 모델의 스네이크 케이스 이름에 `_id`를 붙여 외래 키로 사용합니다. 위 예시라면 `Comment` 모델의 외래 키 컬럼은 `post_id`입니다.

연관관계 메서드가 정의되면, 동적 속성을 통해 관련 댓글 컬렉션에 접근할 수 있습니다. 동적 속성 덕분에 관계 메서드를 속성처럼 사용할 수 있습니다:

```php
use App\Models\Post;

$comments = Post::find(1)->comments;

foreach ($comments as $comment) {
    // ...
}
```

모든 관계는 쿼리 빌더로도 동작하므로, `comments` 메서드를 체이닝해서 추가 조건을 걸 수도 있습니다:

```php
$comment = Post::find(1)->comments()
    ->where('title', 'foo')
    ->first();
```

`hasOne` 메서드와 마찬가지로, 필요에 따라 외래 키와 로컬 키를 더 많은 인수로 지정할 수 있습니다:

```php
return $this->hasMany(Comment::class, 'foreign_key');

return $this->hasMany(Comment::class, 'foreign_key', 'local_key');
```

<a name="automatically-hydrating-parent-models-on-children"></a>
#### 자식 모델에 부모 모델 자동 로딩하기

Eloquent 즉시 로딩을 사용하더라도, 자식 모델에서 부모 모델에 접근할 때 "N + 1" 쿼리 문제가 발생할 수 있습니다:

```php
$posts = Post::with('comments')->get();

foreach ($posts as $post) {
    foreach ($post->comments as $comment) {
        echo $comment->post->title;
    }
}
```

위 예시는 모든 `Post`에 대해 댓글을 즉시 로딩했음에도 불구하고, 각 `Comment`에서 부모 `Post`에 접근할 때 추가 쿼리가 발생합니다.

자식에서 부모 모델이 자동으로 로딩되도록 하려면, `hasMany` 관계 정의 시 `chaperone` 메서드를 호출하면 됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Post extends Model
{
    /**
     * 이 게시글의 댓글 목록을 가져옵니다.
     */
    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class)->chaperone();
    }
}
```

또한 런타임에 관계를 즉시 로딩할 때만 자동 부모 로딩을 적용하려면, 즉시 로딩 시점에 `chaperone`을 사용할 수 있습니다:

```php
use App\Models\Post;

$posts = Post::with([
    'comments' => fn ($comments) => $comments->chaperone(),
])->get();
```

<a name="one-to-many-inverse"></a>
### 일대다(역방향) / belongsTo (One to Many (Inverse) / Belongs To)

이제 게시글의 모든 댓글에 접근할 수 있으니, 반대로 댓글에서 부모 게시글에도 접근이 가능해야 합니다. 일대다 관계의 역방향을 정의하려면, 자식 모델에 `belongsTo` 메서드를 호출하는 관계 메서드를 정의하면 됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Comment extends Model
{
    /**
     * 이 댓글이 달린 게시글을 가져옵니다.
     */
    public function post(): BelongsTo
    {
        return $this->belongsTo(Post::class);
    }
}
```

관계가 정의되면, `post` 동적 관계 속성을 통해 댓글의 부모 게시글을 조회할 수 있습니다:

```php
use App\Models\Comment;

$comment = Comment::find(1);

return $comment->post->title;
```

이때 Eloquent는 `Comment` 모델의 `post_id` 컬럼과 일치하는 `Post` 모델의 `id`를 찾아줍니다.

기본적으로, Eloquent는 관계 메서드 명 뒤에 부모 모델의 기본 키 컬럼명을 붙여 외래 키를 추론합니다. 즉, `comments` 테이블의 `post_id` 컬럼을 사용하게 됩니다.

만약 외래 키 이름이 이 규칙과 다르다면, 두 번째 인수로 외래 키 이름을 명시할 수 있습니다:

```php
/**
 * 이 댓글이 달린 게시글을 가져옵니다.
 */
public function post(): BelongsTo
{
    return $this->belongsTo(Post::class, 'foreign_key');
}
```

부모 모델의 기본 키가 `id`가 아니거나 다른 컬럼일 경우, 세 번째 인수로 부모 테이블의 커스텀 키를 지정할 수 있습니다:

```php
/**
 * 이 댓글이 달린 게시글을 가져옵니다.
 */
public function post(): BelongsTo
{
    return $this->belongsTo(Post::class, 'foreign_key', 'owner_key');
}
```

<a name="default-models"></a>
#### 기본 모델 (Default Models)

`belongsTo`, `hasOne`, `hasOneThrough`, `morphOne` 관계에서는 주어진 관계가 `null`일 때 반환될 기본 모델을 정의할 수 있습니다. 이런 패턴을 [Null Object 패턴](https://en.wikipedia.org/wiki/Null_Object_pattern)이라고 하며, 조건문을 줄여줄 수 있습니다. 아래 예시에서는 `Post` 모델에 연결된 사용자가 없는 경우 빈 `App\Models\User` 모델을 반환합니다:

```php
/**
 * 이 글의 저자를 가져옵니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault();
}
```

기본 모델에 속성값 일부를 미리 설정하려면, 배열이나 클로저를 `withDefault`에 전달할 수 있습니다:

```php
/**
 * 이 글의 저자를 가져옵니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault([
        'name' => 'Guest Author',
    ]);
}

/**
 * 이 글의 저자를 가져옵니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault(function (User $user, Post $post) {
        $user->name = 'Guest Author';
    });
}
```

<a name="querying-belongs-to-relationships"></a>
#### Belongs To 관계 쿼리

Belongs To 관계의 자식 모델을 조회할 때, 직접 `where`로 조건문을 작성할 수도 있습니다:

```php
use App\Models\Post;

$posts = Post::where('user_id', $user->id)->get();
```

하지만, 더 간편하게 `whereBelongsTo` 메서드를 사용하면, 적절한 관계와 외래 키를 자동으로 찾아줍니다:

```php
$posts = Post::whereBelongsTo($user)->get();
```

`whereBelongsTo` 메서드에는 [컬렉션](/docs/12.x/eloquent-collections) 인스턴스도 전달할 수 있습니다. 이때 컬렉션 내 부모들에 속하는 모든 하위 모델이 조회됩니다:

```php
$users = User::where('vip', true)->get();

$posts = Post::whereBelongsTo($users)->get();
```

기본적으로 Laravel은 전달받은 모델의 클래스 이름을 보고 관계를 추론하지만, 두 번째 인수로 관계 이름을 직접 명시할 수도 있습니다:

```php
$posts = Post::whereBelongsTo($user, 'author')->get();
```

<a name="has-one-of-many"></a>
### 여러 개 중 하나(hasOne of Many)

모델이 여러 개의 연관 모델을 가지고 있을 때, 가장 "최신" 또는 "가장 오래된" 하나만 쉽게 가져오고 싶은 경우가 있습니다. 예를 들어, `User`가 여러 개의 `Order`와 연관되어 있지만 사용자가 최근에 한 주문만 빠르게 가져오고 싶은 경우, `hasOne` 관계와 `ofMany` 계열 메서드를 조합해 처리할 수 있습니다:

```php
/**
 * 사용자의 가장 최근 주문을 가져옵니다.
 */
public function latestOrder(): HasOne
{
    return $this->hasOne(Order::class)->latestOfMany();
}
```

반대로, "가장 오래된" 주문을 가져오고 싶다면:

```php
/**
 * 사용자의 가장 오래된 주문을 가져옵니다.
 */
public function oldestOrder(): HasOne
{
    return $this->hasOne(Order::class)->oldestOfMany();
}
```

`latestOfMany` 및 `oldestOfMany` 메서드는 기본적으로 모델의 기본 키로 최신/오래된 연관 레코드를 가져옵니다. 그러나 다른 정렬 기준으로도 단일 모델을 가져올 수 있습니다.

예를 들어, 가장 비싼 주문을 가져오고 싶다면, `ofMany` 메서드를 사용해 정렬 컬럼과 집계 함수를 지정할 수 있습니다:

```php
/**
 * 사용자의 가장 비싼 주문을 가져옵니다.
 */
public function largestOrder(): HasOne
{
    return $this->hasOne(Order::class)->ofMany('price', 'max');
}
```

> [!WARNING]
> PostgreSQL에서는 UUID 컬럼에 대해 `MAX` 함수를 사용할 수 없으므로, PostgreSQL UUID 컬럼과 one-of-many 관계를 조합해서 사용할 수 없습니다.

<a name="converting-many-relationships-to-has-one-relationships"></a>
#### "여러 개" 관계를 hasOne으로 변환하기

이미 `hasMany` 관계를 정의하고 있는 경우, `latestOfMany`, `oldestOfMany`, `ofMany` 메서드를 쓸 때 `one` 메서드로 "하나만" 가져오는 관계로 쉽게 변환할 수 있습니다:

```php
/**
 * 사용자의 주문 목록을 가져옵니다.
 */
public function orders(): HasMany
{
    return $this->hasMany(Order::class);
}

/**
 * 사용자의 가장 비싼 주문을 가져옵니다.
 */
public function largestOrder(): HasOne
{
    return $this->orders()->one()->ofMany('price', 'max');
}
```

`HasManyThrough` 관계에서도 `one` 메서드를 사용해 `HasOneThrough`로 변환할 수 있습니다:

```php
public function latestDeployment(): HasOneThrough
{
    return $this->deployments()->one()->latestOfMany();
}
```

<a name="advanced-has-one-of-many-relationships"></a>
#### 고급 hasOne of Many 관계

더 복잡한 "여러 개 중 하나" 관계도 정의할 수 있습니다. 예를 들어, `Product` 모델은 여러 개의 `Price`와 연관되며, 이미 게시된 가격 정보도 계속 시스템에 남아있고, 향후에 적용될 가격이 미리 게시되어 있을 수도 있습니다. 즉, `published_at` 컬럼을 이용해 아직 미래가 아닌 가장 최근에 게시된 가격을, 같은 날짜라면 가장 큰 id를 갖는 가격을 우선적으로 가져와야 합니다.

이렇게 하려면 `ofMany` 메서드에 정렬 기준이 되는 컬럼 배열과, 추가 조건을 걸 수 있는 클로저를 전달합니다:

```php
/**
 * 현재 상품의 가격을 가져옵니다.
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
### 중간을 거치는 일대일 (Has One Through)

"has-one-through" 관계는 중간 모델을 한 번 거쳐 최종적으로 하나의 모델과 연관지을 때 사용합니다.

예를 들어, 자동차 정비소 앱에서 `Mechanic`(정비공)은 하나의 `Car`(차량)와 연결되고, 각 차량은 하나의 `Owner`(차주)와 연결됩니다. 이때 정비공과 차주는 직접적인 관계가 없지만, 차량을 매개로 서로 연결할 수 있습니다. 테이블 예시는 다음과 같습니다:

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

이제 관계를 정의해볼 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasOneThrough;

class Mechanic extends Model
{
    /**
     * 차량 소유자를 가져옵니다.
     */
    public function carOwner(): HasOneThrough
    {
        return $this->hasOneThrough(Owner::class, Car::class);
    }
}
```

`hasOneThrough`의 첫 번째 인수는 최종적으로 연결할 모델을, 두 번째 인수는 중간 모델을 의미합니다.

또는, 각각의 관계가 이미 모델에 정의되어 있다면, `through` 메서드에 관계명을 전달해 더 간결하게 정의할 수 있습니다:

```php
// 문자열 방식
return $this->through('cars')->has('owner');

// 동적 방식
return $this->throughCars()->hasOwner();
```

<a name="has-one-through-key-conventions"></a>
#### 키 명명 규칙

쿼리 시 Eloquent 기본 외래 키 규칙이 사용됩니다. 필요하다면, `hasOneThrough`의 3, 4번째 인수로 외래 키를, 5, 6번째 인수로는 로컬 키를 직접 지정할 수 있습니다:

```php
class Mechanic extends Model
{
    /**
     * 차량 소유자를 가져옵니다.
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

이미 관련 관계들이 모두 정의되어 있다면, `through` 방식으로 기존 규칙을 재활용할 수도 있습니다:

```php
// 문자열 방식
return $this->through('cars')->has('owner');

// 동적 방식
return $this->throughCars()->hasOwner();
```

<a name="has-many-through"></a>
### 중간을 거치는 일대다 (Has Many Through)

"has-many-through" 관계는 중간 모델을 거쳐 더 먼 곳에 있는 여러 모델과 연결되는 경우에 유용합니다. 예를 들어, [Laravel Cloud](https://cloud.laravel.com)와 같은 배포 플랫폼에서, 애플리케이션이 중간의 Environment를 통해 여러 Deployment와 연결될 수 있습니다. 테이블 구조는 다음과 같습니다:

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

이제 관계를 정의해봅니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasManyThrough;

class Application extends Model
{
    /**
     * 애플리케이션의 모든 배포 이력을 가져옵니다.
     */
    public function deployments(): HasManyThrough
    {
        return $this->hasManyThrough(Deployment::class, Environment::class);
    }
}
```

`hasManyThrough`의 첫 번째 인수는 최종적으로 접근할 모델, 두 번째 인수는 중간 모델입니다.

이미 각 모델에 관계가 정의되어 있다면, `through` 구문으로 더 간결하게 쓸 수 있습니다:

```php
// 문자열 방식
return $this->through('environments')->has('deployments');

// 동적 방식
return $this->throughEnvironments()->hasDeployments();
```

`Deployment` 테이블에 `application_id` 컬럼이 없어도, 중간 테이블의 `application_id` 컬럼을 참조해 관련 배포 이력을 조회하게 됩니다.

<a name="has-many-through-key-conventions"></a>
#### 키 명명 규칙

기본 외래 키 규칙이 적용됩니다. 필요하면, `hasManyThrough`의 3, 4번째 인수로 외래 키, 5, 6번째 인수로 로컬 키를 직접 지정할 수 있습니다:

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

앞서 언급한 것처럼 기존 관계가 정의되어 있다면, through 방식으로 더 간결하게 사용할 수 있습니다:

```php
// 문자열 방식
return $this->through('environments')->has('deployments');

// 동적 방식
return $this->throughEnvironments()->hasDeployments();
```

<a name="scoped-relationships"></a>
### 스코프 연관관계 (Scoped Relationships)

관계에 제약을 추가하는 메서드를 모델에 추가하는 경우가 많습니다. 예를 들어, `User` 모델에 전체 게시글 목록(`posts`)과, 추가 조건이 있는 `featuredPosts` 메서드를 정의할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class User extends Model
{
    /**
     * 사용자의 게시글 목록을 가져옵니다.
     */
    public function posts(): HasMany
    {
        return $this->hasMany(Post::class)->latest();
    }

    /**
     * 사용자의 추천 게시글 목록을 가져옵니다.
     */
    public function featuredPosts(): HasMany
    {
        return $this->posts()->where('featured', true);
    }
}
```

하지만 위 방식에서 `featuredPosts`로 모델을 생성할 때, `featured` 속성이 자동으로 true로 되지는 않습니다. 만약 관계 메서드로 생성되는 모든 모델에 특정 속성을 기본값으로 추가하고 싶다면, `withAttributes` 메서드를 사용하면 됩니다:

```php
/**
 * 사용자의 추천 게시글 목록을 가져옵니다.
 */
public function featuredPosts(): HasMany
{
    return $this->posts()->withAttributes(['featured' => true]);
}
```

`withAttributes` 메서드는 쿼리 조건에 해당 속성을 추가하고, 관계 메서드를 통해 생성되는 모델에도 해당 속성 값을 포함합니다:

```php
$post = $user->featuredPosts()->create(['title' => 'Featured Post']);

$post->featured; // true
```

쿼리에 `where` 조건을 추가하지 않고, 생성시 속성값만 자동으로 추가하고 싶다면, 두 번째 인수 `asConditions`를 false로 설정하면 됩니다:

```php
return $this->posts()->withAttributes(['featured' => true], asConditions: false);
```

<a name="many-to-many"></a>
## 다대다 연관관계 (Many to Many Relationships)

다대다 관계는 `hasOne`이나 `hasMany`에 비해 조금 복잡합니다. 예를 들어, 한 사용자가 여러 역할(role)을 가지며, 역할도 여러 사용자와 공유될 수 있습니다. 예를 들어, 한 사용자가 "Author", "Editor" 역할을 동시에 부여받고, 해당 역할들이 다른 사용자에게도 할당될 수 있습니다. 즉, 한 사용자는 여러 역할을, 한 역할도 여러 사용자를 가집니다.

<a name="many-to-many-table-structure"></a>
#### 테이블 구조

이 관계를 구현하려면, `users`, `roles`, `role_user` 세 개의 테이블이 필요합니다. `role_user`처럼 중간 테이블은 알파벳 순으로 두 모델 이름을 조합해 만듭니다. 이 테이블은 `user_id`, `role_id` 컬럼을 포함해 사용자와 역할을 연결합니다.

역할이 여러 사용자와 연결되므로, 단순히 역할 테이블에 `user_id`를 둘 수 없습니다. 여러 사용자가 한 역할을 공유하려면 중간 테이블이 필요합니다. 구조 예시는 다음과 같습니다:

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
#### 모델 구조

다대다 관계는 `belongsToMany` 메서드를 반환하는 메서드로 정의합니다. 이 메서드는 모든 Eloquent 모델의 기본 클래스인 `Illuminate\Database\Eloquent\Model`이 제공합니다. 예를 들어, `User` 모델에 `roles` 관계를 아래와 같이 정의할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class User extends Model
{
    /**
     * 사용자와 연결된 역할 목록을 가져옵니다.
     */
    public function roles(): BelongsToMany
    {
        return $this->belongsToMany(Role::class);
    }
}
```

관계가 정의된 후에는 `roles` 동적 관계 속성으로 역할 목록에 접근할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

foreach ($user->roles as $role) {
    // ...
}
```

다른 모든 관계처럼 조건을 추가해 쿼리를 조합할 수도 있습니다:

```php
$roles = User::find(1)->roles()->orderBy('name')->get();
```

중간 테이블 이름은 두 모델 명을 알파벳 순으로 조합해 결정되지만, 원하는 경우 두 번째 인수로 직접 지정할 수 있습니다:

```php
return $this->belongsToMany(Role::class, 'role_user');
```

또한, 중간 테이블의 키 이름을 추가 인수로 커스터마이즈할 수 있습니다. 세 번째 인수는 정의하는 모델의 외래 키, 네 번째 인수는 연결할 모델의 외래 키입니다:

```php
return $this->belongsToMany(Role::class, 'role_user', 'user_id', 'role_id');
```

<a name="many-to-many-defining-the-inverse-of-the-relationship"></a>
#### 관계의 역방향 정의

다대다 관계의 "역방향"을 구현할 때도 동일하게 `belongsToMany`를 사용합니다. 예를 들어, `Role` 모델에도 유저 리스트를 정의할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class Role extends Model
{
    /**
     * 이 역할을 가진 사용자 목록을 가져옵니다.
     */
    public function users(): BelongsToMany
    {
        return $this->belongsToMany(User::class);
    }
}
```

역방향 관계도 동일하게 정의하되, 상대 모델만 바꿔줍니다. 테이블/키명 커스터마이즈 옵션도 동일하게 사용 가능합니다.

<a name="retrieving-intermediate-table-columns"></a>
### 중간 테이블 컬럼 조회

다대다 관계는 중간 테이블이 필요합니다. Eloquent는 중간 테이블과 상호작용하기 위한 편리한 방법을 제공합니다. 예를 들어, `User`가 여러 `Role`을 가질 때, 관계를 통해 중간 테이블의 데이터에도 접근할 수 있습니다. 아래 예처럼, `pivot` 속성을 통해 중간 테이블의 값을 사용할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

foreach ($user->roles as $role) {
    echo $role->pivot->created_at;
}
```

각 `Role` 모델에는 자동으로 `pivot`이라는 속성이 할당됩니다. 이 속성은 중간 테이블에 해당하는 정보를 담고 있습니다.

기본적으로는 키 값만 포함되며, 추가 컬럼이 필요하다면 관계 정의 시 `withPivot`을 사용해 명시해야 합니다:

```php
return $this->belongsToMany(Role::class)->withPivot('active', 'created_by');
```

중간 테이블에도 자동 `created_at`, `updated_at` 타임스탬프가 유지되길 원한다면 `withTimestamps`를 함께 사용합니다:

```php
return $this->belongsToMany(Role::class)->withTimestamps();
```

> [!WARNING]
> Eloquent의 자동 타임스탬프를 사용하는 중간 테이블은 `created_at`, `updated_at` 컬럼이 모두 존재해야 합니다.

<a name="customizing-the-pivot-attribute-name"></a>
#### `pivot` 속성명 커스터마이즈

중간 테이블에서 가져온 속성은 기본적으로 `pivot`으로 접근하지만, 필요하다면 `as` 메서드로 별도 이름을 설정할 수 있습니다. 예를 들어, 사용자와 팟캐스트 간의 구독 관계라면 `subscription`이란 이름을 줄 수 있습니다:

```php
return $this->belongsToMany(Podcast::class)
    ->as('subscription')
    ->withTimestamps();
```

이후 아래처럼 새로운 이름으로 접근이 가능합니다:

```php
$users = User::with('podcasts')->get();

foreach ($users->flatMap->podcasts as $podcast) {
    echo $podcast->subscription->created_at;
}
```

<a name="filtering-queries-via-intermediate-table-columns"></a>
### 중간 테이블 컬럼을 통한 쿼리 필터링

`belongsToMany` 관계 쿼리에서 `wherePivot`, `wherePivotIn`, `wherePivotNotIn`, `wherePivotBetween`, `wherePivotNotBetween`, `wherePivotNull`, `wherePivotNotNull` 등을 이용해 중간 테이블의 데이터를 조건으로 쿼리할 수 있습니다:

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

`wherePivot`은 쿼리를 위한 where만 걸지만, 관계로 새 모델을 생성할 때는 해당 값이 추가되지 않습니다. 쿼리와 생성 all에서 특정 `pivot` 값을 공통적으로 적용하려면 `withPivotValue`를 사용하세요:

```php
return $this->belongsToMany(Role::class)
    ->withPivotValue('approved', 1);
```

<a name="ordering-queries-via-intermediate-table-columns"></a>
### 중간 테이블 컬럼을 통한 쿼리 정렬

`orderByPivot` 메서드를 사용해 중간 테이블의 값을 기준으로 정렬할 수 있습니다. 아래 예시는 사용자의 가장 최근 배지를 조회하는 예입니다:

```php
return $this->belongsToMany(Badge::class)
    ->where('rank', 'gold')
    ->orderByPivot('created_at', 'desc');
```

<a name="defining-custom-intermediate-table-models"></a>
### 커스텀 중간 테이블 모델 정의

다대다 연관관계의 중간 테이블에 대한 커스텀 모델을 정의하려면, 관계 정의 시 `using` 메서드를 사용합니다. 커스텀 Pivot 모델은 추가 동작(메서드, 캐스팅 등)을 구현할 수 있습니다.

커스텀 Pivot 모델은 `Illuminate\Database\Eloquent\Relations\Pivot`(또는, 폴리모픽의 경우 `MorphPivot`)을 상속해야 합니다. 예를 들어, `RoleUser`라는 커스텀 피벗 모델을 아래처럼 정의할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class Role extends Model
{
    /**
     * 이 역할을 가진 사용자 목록을 가져옵니다.
     */
    public function users(): BelongsToMany
    {
        return $this->belongsToMany(User::class)->using(RoleUser::class);
    }
}
```

`RoleUser` 모델은 아래처럼 정의합니다:

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
> Pivot 모델은 `SoftDeletes` 트레이트를 사용할 수 없습니다. 피벗 레코드를 soft delete해야 한다면, 피벗을 실제 Eloquent 모델로 전환하는 것을 고려하세요.

<a name="custom-pivot-models-and-incrementing-ids"></a>
#### 커스텀 Pivot 모델과 자동 증가 ID

커스텀 Pivot 모델에서 자동 증가 기본 키를 사용하는 경우, 모델 클래스에 `incrementing` 속성을 `true`로 명시해야 합니다.

```php
/**
 * ID가 자동 증가되는지 여부
 *
 * @var bool
 */
public $incrementing = true;
```

<a name="polymorphic-relationships"></a>
## 폴리모픽 연관관계 (Polymorphic Relationships)

폴리모픽 연관관계는 하위 모델이 하나 이상의 여러 모델에 단일 연결로 속할 수 있게 해줍니다. 예를 들어, 사용자가 블로그 게시글과 비디오를 공유하는 앱에서, `Comment`(댓글)이 `Post`와 `Video` 두 모델 중 어떤 것에나 속할 수 있는 상황입니다.

<a name="one-to-one-polymorphic-relations"></a>
### 일대일 (폴리모픽)

<a name="one-to-one-polymorphic-table-structure"></a>
#### 테이블 구조

일대일 폴리모픽 관계는 일반적인 일대일과 비슷하지만, 자식 모델이 여러 타입의 모델에 단일 연결로 소속될 수 있다는 점이 다릅니다. 예를 들어, 블로그 `Post`와 `User`가 동일한 `Image`와 폴리모픽 연관관계를 맺고 있을 수 있습니다. 구조는 다음과 같습니다:

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

`images` 테이블의 `imageable_id`, `imageable_type` 컬럼을 주목하세요. `imageable_id`는 post/user의 ID, `imageable_type`은 부모 모델의 클래스명을 가집니다. 이 컬럼으로 어떤 타입(parent)과 연결되는지 알 수 있습니다. 예를 들어, `App\Models\Post` 또는 `App\Models\User`가 저장됩니다.

<a name="one-to-one-polymorphic-model-structure"></a>
#### 모델 구조

이제 관계 정의 모델 예시를 봅시다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class Image extends Model
{
    /**
     * 상위 imageable 모델(user 또는 post)을 가져옵니다.
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
     * 게시글의 이미지를 가져옵니다.
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

DB 테이블과 모델이 준비되면, 동적 관계 속성으로 접근하면 됩니다. 예컨대 게시글의 이미지는:

```php
use App\Models\Post;

$post = Post::find(1);

$image = $post->image;
```

폴리모픽 모델의 부모를 조회하려면 `morphTo` 메서드명(여기선 `imageable`)으로 접근합니다:

```php
use App\Models\Image;

$image = Image::find(1);

$imageable = $image->imageable;
```

`Image` 모델의 `imageable` 관계는 상황에 따라 `Post` 또는 `User`를 반환합니다.

<a name="morph-one-to-one-key-conventions"></a>
#### 키 명명 규칙

필요하다면, 폴리모픽 하위 모델에 사용되는 id/type 컬럼명을 직접 정의할 수도 있습니다. 이때는 첫 번째 인수로 관계 이름을 항상 전달해야 합니다. 보통 메서드명을 PHP의 `__FUNCTION__` 상수로 넘깁니다:

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
### 일대다 (폴리모픽)

<a name="one-to-many-polymorphic-table-structure"></a>
#### 테이블 구조

일대다 폴리모픽은 일반 일대다와 비슷하지만, 자식 모델이 다양한 타입의 모델에 속할 수 있습니다. 예를 들어, 사용자들이 게시글과 비디오 모두에 댓글을 남길 수 있으면, 하나의 `comments` 테이블로 두 곳 모두 관리할 수 있습니다:

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

예시 모델은 다음과 같습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class Comment extends Model
{
    /**
     * 상위 commentable 모델(post 또는 video)을 가져옵니다.
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
     * 게시글의 모든 댓글을 가져옵니다.
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
     * 비디오의 모든 댓글을 가져옵니다.
     */
    public function comments(): MorphMany
    {
        return $this->morphMany(Comment::class, 'commentable');
    }
}
```

<a name="one-to-many-polymorphic-retrieving-the-relationship"></a>
#### 관계 조회

정의된 후엔 동적 속성으로 접근합니다:

```php
use App\Models\Post;

$post = Post::find(1);

foreach ($post->comments as $comment) {
    // ...
}
```

폴리모픽 자식에서 부모에 접근하려면 관계 메서드명(여긴 `commentable`)으로:

```php
use App\Models\Comment;

$comment = Comment::find(1);

$commentable = $comment->commentable;
```

`commentable` 관계는 상황에 따라 `Post` 또는 `Video` 인스턴스를 반환합니다.

<a name="polymorphic-automatically-hydrating-parent-models-on-children"></a>
#### 자식에서 부모 모델 자동 로딩

즉시 로딩을 활용해도, 루프 내에서 자식에서 부모에 접근하면 "N+1" 쿼리가 발생할 수 있습니다:

```php
$posts = Post::with('comments')->get();

foreach ($posts as $post) {
    foreach ($post->comments as $comment) {
        echo $comment->commentable->title;
    }
}
```

이때, `morphMany` 관계 정의 시 `chaperone`으로 자동 부모 로딩을 활성화할 수 있습니다:

```php
class Post extends Model
{
    /**
     * 게시글의 모든 댓글을 가져옵니다.
     */
    public function comments(): MorphMany
    {
        return $this->morphMany(Comment::class, 'commentable')->chaperone();
    }
}
```

혹은 즉시 로딩시 적용하고 싶다면 아래와 같이:

```php
use App\Models\Post;

$posts = Post::with([
    'comments' => fn ($comments) => $comments->chaperone(),
])->get();
```

<a name="one-of-many-polymorphic-relations"></a>
### 여러 개 중 하나 (폴리모픽) (One of Many (Polymorphic))

모델이 여러 개의 연관 폴리모픽 모델을 가질 때, 가장 "최신" 또는 "가장 오래된" 하나만 쉽게 가져오고 싶다면, `morphOne`과 `ofMany` 계열 메서드를 함께 사용합니다:

```php
/**
 * 사용자의 최신 이미지를 가져옵니다.
 */
public function latestImage(): MorphOne
{
    return $this->morphOne(Image::class, 'imageable')->latestOfMany();
}
```

"가장 오래된" 이미지는 아래와 같이 정의할 수 있습니다:

```php
/**
 * 사용자의 가장 오래된 이미지를 가져옵니다.
 */
public function oldestImage(): MorphOne
{
    return $this->morphOne(Image::class, 'imageable')->oldestOfMany();
}
```

기본적으로 최신, 오래된 판단은 기본 키 기준이며(정렬 가능 컬럼 필요), 다른 기준 컬럼을 원한다면 `ofMany`로 지정할 수 있습니다:

```php
/**
 * 사용자의 인기 이미지를 가져옵니다.
 */
public function bestImage(): MorphOne
{
    return $this->morphOne(Image::class, 'imageable')->ofMany('likes', 'max');
}
```

> [!NOTE]
> 더 복잡한 "여러 개 중 하나" 관계 예제는 [has one of many 문서](#advanced-has-one-of-many-relationships)에서 추가로 확인할 수 있습니다.

<a name="many-to-many-polymorphic-relations"></a>
### 다대다 (폴리모픽) (Many to Many (Polymorphic))

<a name="many-to-many-polymorphic-table-structure"></a>
#### 테이블 구조

다대다 폴리모픽은 morph one/many보다 조금 더 복잡합니다. 예를 들어 `Post`와 `Video` 모델이 `Tag` 모델과 다대다 폴리모픽 관계를 가질 수 있습니다. 이때 아래 구조로 단일 태그 테이블을 두 모델에 모두 활용할 수 있습니다:

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
> 다대다 폴리모픽 사용 전, 일반 [다대다 관계](#many-to-many) 문서를 참고하면 이해에 도움이 됩니다.

<a name="many-to-many-polymorphic-model-structure"></a>
#### 모델 구조

이제 각 모델에 아래와 같이 관계를 정의합니다. `Post`, `Video` 모델에 `tags` 메서드를 추가하는데, `morphToMany`를 사용합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphToMany;

class Post extends Model
{
    /**
     * 게시글의 모든 태그를 가져옵니다.
     */
    public function tags(): MorphToMany
    {
        return $this->morphToMany(Tag::class, 'taggable');
    }
}
```

<a name="many-to-many-polymorphic-defining-the-inverse-of-the-relationship"></a>
#### 관계의 역방향 정의

`Tag` 모델에는 `posts`, `videos` 등 모든 부모 모델 별로 메서드를 만들어야 하며, 이들은 `morphedByMany`를 사용합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphToMany;

class Tag extends Model
{
    /**
     * 이 태그가 할당된 모든 게시글을 가져옵니다.
     */
    public function posts(): MorphToMany
    {
        return $this->morphedByMany(Post::class, 'taggable');
    }

    /**
     * 이 태그가 할당된 모든 비디오를 가져옵니다.
     */
    public function videos(): MorphToMany
    {
        return $this->morphedByMany(Video::class, 'taggable');
    }
}
```

<a name="many-to-many-polymorphic-retrieving-the-relationship"></a>
#### 관계 조회

정의 후에는 아래처럼 각 모델의 동적 속성으로 태그 및 부모 데이터를 조회합니다:

```php
use App\Models\Post;

$post = Post::find(1);

foreach ($post->tags as $tag) {
    // ...
}
```

또는 `Tag` 모델에서 부모들을 조회할 수 있습니다:

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
### 커스텀 폴리모픽 타입 (Custom Polymorphic Types)

Laravel은 기본적으로 연관되는 모델의 "타입"을 모델의 fully qualified 클래스명으로 저장합니다. 예를 들어 앞서 예시의 `Comment`가 `Post` 또는 `Video`에 속하는 경우, `commentable_type`에는 각각 `App\Models\Post`, `App\Models\Video`가 저장됩니다. 하지만 앱 내부 구조와 타입을 분리하려면, 커스텀 맵을 등록할 수 있습니다.

예를 들어, 클래스명 대신 `post`, `video` 문자열을 사용할 수 있습니다. 이렇게 하면 나중에 모델 이름이 바뀌어도 DB 값이 그대로 유지됩니다:

```php
use Illuminate\Database\Eloquent\Relations\Relation;

Relation::enforceMorphMap([
    'post' => 'App\Models\Post',
    'video' => 'App\Models\Video',
]);
```

이 코드는 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 호출하거나 별도 서비스 프로바이더에서 사용할 수 있습니다.

런타임 중에 모델의 morph alias를 얻으려면 모델의 `getMorphClass`를, alias로 클래스명을 찾으려면 `Relation::getMorphedModel`을 사용합니다:

```php
use Illuminate\Database\Eloquent\Relations\Relation;

$alias = $post->getMorphClass();

$class = Relation::getMorphedModel($alias);
```

> [!WARNING]
> 기존 애플리케이션에 morph map을 추가했다면, 데이터베이스에 fully qualified 클래스명으로 저장된 모든 morphable의 *_type 값도 맵 이름으로 변환해주어야 합니다.

<a name="dynamic-relationships"></a>
### 동적 연관관계 (Dynamic Relationships)

`resolveRelationUsing` 메서드로 런타임에 Eloquent 모델 간 관계를 동적으로 정의할 수 있습니다. 일반적인 앱 개발에는 권장되지 않지만, Laravel 패키지 개발 등 특별한 경우에 사용됩니다.

첫 번째 인수로 관계명, 두 번째는 관계를 반환하는 클로저(모델 인스턴스를 인수로)입니다. 보통 [서비스 프로바이더](/docs/12.x/providers)의 boot 메서드에서 설정합니다:

```php
use App\Models\Order;
use App\Models\Customer;

Order::resolveRelationUsing('customer', function (Order $orderModel) {
    return $orderModel->belongsTo(Customer::class, 'customer_id');
});
```

> [!WARNING]
> 동적 관계 정의 시에는 Eloquent 관계 메서드에 항상 키 이름을 명시적으로 전달해야 합니다.

<a name="querying-relations"></a>
## 연관관계 쿼리 (Querying Relations)

Eloquent 연관관계는 모두 메서드로 정의되어 있으므로, 해당 메서드를 호출하면 관계 인스턴스를 얻을 수 있으며, 아직 쿼리가 실행되지는 않습니다. 또한, 모든 타입의 Eloquent 관계는 [쿼리 빌더](/docs/12.x/queries)의 역할도 하므로, 추가 조건을 계속 체이닝한 뒤, 실제 DB 쿼리를 실행할 수 있습니다.

예를 들어, 블로그 앱에서 `User`가 여러 `Post`를 갖고 있다면 아래처럼 추가 조건을 붙일 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class User extends Model
{
    /**
     * 사용자의 모든 게시글을 가져옵니다.
     */
    public function posts(): HasMany
    {
        return $this->hasMany(Post::class);
    }
}
```

아래처럼 쿼리를 조합할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

$user->posts()->where('active', 1)->get();
```

Laravel [쿼리 빌더](/docs/12.x/queries)의 모든 메서드를 사용 가능하므로, 더 많은 방법은 쿼리 빌더 문서를 참고하세요.

<a name="chaining-orwhere-clauses-after-relationships"></a>
#### 관계 쿼리에서 `orWhere` 사용 시 주의사항

앞선 예시처럼 추가 제약을 계속 붙일 수 있지만, `orWhere`를 사용할 때는 주의가 필요합니다. `orWhere`는 관계 조건과 같은 레벨로 그룹화됩니다:

```php
$user->posts()
    ->where('active', 1)
    ->orWhere('votes', '>=', 100)
    ->get();
```

이 쿼리는 아래 SQL과 동일합니다. 즉, 관계 제한 없이 votes가 100 이상인 모든 글도 조회됩니다:

```sql
select *
from posts
where user_id = ? and active = 1 or votes >= 100
```

대부분의 경우, [논리 그룹](/docs/12.x/queries#logical-grouping)을 사용해 조건들을 괄호로 묶어주는 것이 바람직합니다:

```php
use Illuminate\Database\Eloquent\Builder;

$user->posts()
    ->where(function (Builder $query) {
        return $query->where('active', 1)
            ->orWhere('votes', '>=', 100);
    })
    ->get();
```

이렇게 하면 아래처럼 올바르게 그룹화됩니다:

```sql
select *
from posts
where user_id = ? and (active = 1 or votes >= 100)
```

<a name="relationship-methods-vs-dynamic-properties"></a>
### 연관관계 메서드 vs 동적 속성

추가 제약이 필요 없다면, 단순히 관계를 속성처럼 접근할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

foreach ($user->posts as $post) {
    // ...
}
```

동적 속성 방식은 "지연 로딩"(lazy loading)이므로, 실제로 접근할 때만 쿼리가 실행됩니다. 이런 이유로, 대량 접근 시 [즉시 로딩](#eager-loading)을 사용해 미리 관계 데이터를 불러오는 것이 SQL 쿼리 개수를 대폭 줄여줍니다.

<a name="querying-relationship-existence"></a>
### 연관관계의 존재 쿼리

모델을 조회할 때 특정 관계가 **존재하는** 경우로 결과를 제한할 수 있습니다. 예를 들어, 댓글이 달린 모든 게시글을 조회하고 싶다면, `has` 및 `orHas` 메서드에 관계명을 전달할 수 있습니다:

```php
use App\Models\Post;

// 댓글이 하나라도 있는 게시글을 모두 조회
$posts = Post::has('comments')->get();
```

또한 연산자와 개수도 지정할 수 있습니다:

```php
// 댓글이 3개 이상인 게시글 조회
$posts = Post::has('comments', '>=', 3)->get();
```

중첩된 `has`문은 "점" 표기법으로 사용할 수 있습니다. 댓글에 이미지가 하나라도 있는 게시글 조회 예시는:

```php
// 이미지가 달린 댓글이 하나라도 있는 게시글 조회
$posts = Post::has('comments.images')->get();
```

더 강력한 쿼리가 필요하다면, 특정 내용의 댓글만 갖는 게시글처럼, `whereHas`, `orWhereHas` 메서드로 쿼리를 추가할 수 있습니다:

```php
use Illuminate\Database\Eloquent\Builder;

// 내용에 code%가 포함된 댓글이 있는 게시글 조회
$posts = Post::whereHas('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
})->get();

// 10개 이상의 그런 댓글이 있는 게시글만 조회
$posts = Post::whereHas('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
}, '>=', 10)->get();
```

> [!WARNING]
> Eloquent는 현재 **다른 데이터베이스**에 걸친 관계 존재 쿼리를 지원하지 않습니다. 관계는 같은 데이터베이스 내부에서만 가능합니다.

<a name="many-to-many-relationship-existence-queries"></a>
#### 다대다 관계 존재 쿼리

`whereAttachedTo` 메서드는 특정 모델 또는 컬렉션과 다대다 관계가 연결된 모델만 조회할 때 사용합니다:

```php
$users = User::whereAttachedTo($role)->get();
```

컬렉션도 사용할 수 있어, 컬렉션의 어떤 모델에라도 연결돼 있다면 반환합니다:

```php
$tags = Tag::whereLike('name', '%laravel%')->get();

$posts = Post::whereAttachedTo($tags)->get();
```

<a name="inline-relationship-existence-queries"></a>
#### 인라인 관계 존재 쿼리

관계 쿼리에 단일 `where` 조건만 붙이고 싶을 때는, `whereRelation`, `orWhereRelation`, `whereMorphRelation`, `orWhereMorphRelation` 메서드도 사용할 수 있습니다. 예를 들어, 승인되지 않은 댓글이 있는 게시글만 조회:

```php
use App\Models\Post;

$posts = Post::whereRelation('comments', 'is_approved', false)->get();
```

또는 아래처럼 연산자 사용 가능:

```php
$posts = Post::whereRelation(
    'comments', 'created_at', '>=', now()->subHour()
)->get();
```

<a name="querying-relationship-absence"></a>
### 연관관계의 부재 쿼리

특정 관계가 **존재하지 않는** 모델만 조회하려면, `doesntHave`, `orDoesntHave` 메서드에 관계명을 전달하면 됩니다. 예를 들어, 댓글이 없는 게시글 조회:

```php
use App\Models\Post;

$posts = Post::doesntHave('comments')->get();
```

더 복잡하게 내부 내용이 없는 경우만 골라내려면, `whereDoesntHave`, `orWhereDoesntHave` 쿼리로 조건을 추가할 수 있습니다:

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::whereDoesntHave('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
})->get();
```

"점" 표기법으로 중첩 관계도 쿼리할 수 있습니다. 아래는 banned 사용자가 작성한 댓글이 하나도 없는 게시글을 조회하는 예시입니다:

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::whereDoesntHave('comments.author', function (Builder $query) {
    $query->where('banned', 1);
})->get();
```

<a name="querying-morph-to-relationships"></a>
### Morph To 관계 쿼리

"morph to" 관계의 존재 쿼리를 하려면, `whereHasMorph`, `whereDoesntHaveMorph` 메서드를 사용합니다. 첫 번째 인수로 관계명을, 두 번째에 관련 모델 클래스명을 배열 또는 단일 값으로 전달할 수 있으며, 마지막에 커스텀 쿼리 클로저도 지정할 수 있습니다:

```php
use App\Models\Comment;
use App\Models\Post;
use App\Models\Video;
use Illuminate\Database\Eloquent\Builder;

// 제목이 'code%'로 시작하는 post나 video에 달린 댓글 조회
$comments = Comment::whereHasMorph(
    'commentable',
    [Post::class, Video::class],
    function (Builder $query) {
        $query->where('title', 'like', 'code%');
    }
)->get();

// 제목이 'code%'로 시작하지 않는 post에 달린 댓글만 조회
$comments = Comment::whereDoesntHaveMorph(
    'commentable',
    Post::class,
    function (Builder $query) {
        $query->where('title', 'like', 'code%');
    }
)->get();
```

$타입 값까지 받아 타입별 쿼리를 다르게 지정할 수도 있습니다:

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

자식에서 morph parent에 대한 쿼리를 원한다면(즉, 자식이 어떤 부모에 속해 있는지), `whereMorphedTo`, `whereNotMorphedTo`를 사용합니다:

```php
$comments = Comment::whereMorphedTo('commentable', $post)
    ->orWhereMorphedTo('commentable', $video)
    ->get();
```

<a name="querying-all-morph-to-related-models"></a>
#### 모든 morph to 관련 모델 조회

가능한 모든 폴리모픽 타입을 쿼리하고자 한다면, 두 번째 인수로 `*`를 사용할 수 있습니다. 이때 Laravel이 해당 가능한 타입을 모두 추출하는 추가 쿼리를 실행합니다:

```php
use Illuminate\Database\Eloquent\Builder;

$comments = Comment::whereHasMorph('commentable', '*', function (Builder $query) {
    $query->where('title', 'like', 'foo%');
})->get();
```

<a name="aggregating-related-models"></a>
## 관계 모델 집계 (Aggregating Related Models)

<a name="counting-related-models"></a>
### 관계 모델 개수 세기

연관 모델의 실제 데이터를 불러오지 않고도, 관계 레코드 개수만 간단히 세고 싶을 때는 `withCount` 메서드를 사용합니다. `{relation}_count` 속성이 결과 모델에 추가됩니다:

```php
use App\Models\Post;

$posts = Post::withCount('comments')->get();

foreach ($posts as $post) {
    echo $post->comments_count;
}
```

배열 방식으로 여러 관계의 count도 동시에, 또는 관계별 추가 쿼리 조건도 줄 수 있습니다:

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::withCount(['votes', 'comments' => function (Builder $query) {
    $query->where('content', 'like', 'code%');
}])->get();

echo $posts[0]->votes_count;
echo $posts[0]->comments_count;
```

별칭을 사용해 같은 관계에 대해 여러 count 속성을 만들 수도 있습니다:

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
#### 지연 count 로딩

`loadCount` 메서드로 이미 조회한 부모 모델에도 count를 나중에 추가할 수 있습니다:

```php
$book = Book::first();

$book->loadCount('genres');
```

더 세밀하게 쿼리 조건을 추가하고 싶다면 관계명을 키, 클로저를 값으로 배열을 전달합니다:

```php
$book->loadCount(['reviews' => function (Builder $query) {
    $query->where('rating', 5);
}])
```

<a name="relationship-counting-and-custom-select-statements"></a>
#### select문과 count를 조합할 경우 주의

`withCount`와 `select`를 같이 쓸 때는, 반드시 `select` 다음에 `withCount`를 호출해야 합니다:

```php
$posts = Post::select(['title', 'body'])
    ->withCount('comments')
    ->get();
```

<a name="other-aggregate-functions"></a>
### 기타 집계 함수

`withCount` 외에도, Eloquent는 `withMin`, `withMax`, `withAvg`, `withSum`, `withExists` 등을 지원합니다. 각각 `{relation}_{function}_{column}` 형식의 속성이 결과 모델에 추가됩니다:

```php
use App\Models\Post;

$posts = Post::withSum('comments', 'votes')->get();

foreach ($posts as $post) {
    echo $post->comments_sum_votes;
}
```

별칭으로 집계 결과에 원하는 이름을 지정할 수도 있습니다:

```php
$posts = Post::withSum('comments as total_comments', 'votes')->get();

foreach ($posts as $post) {
    echo $post->total_comments;
}
```

이 역시 지연(Deferred) 방식(`loadSum` 등)으로 이미 로딩한 모델에도 사용할 수 있습니다:

```php
$post = Post::first();

$post->loadSum('comments', 'votes');
```

select문과 조합하려면 반드시 select 다음에 집계 메서드를 써야 합니다:

```php
$posts = Post::select(['title', 'body'])
    ->withExists('comments')
    ->get();
```

<a name="counting-related-models-on-morph-to-relationships"></a>
### Morph To 관계에서 관계 모델 개수 세기

"morph to" 관계도 관계형 모델 count 조회가 가능합니다. `with`와 morphTo 관계의 `morphWithCount`를 조합해 사용할 수 있습니다.

예를 들어, `Photo`와 `Post` 모델이 각각 `ActivityFeed`(morph-to: parentable)의 부모가 되고, `Photo`는 `Tag`, `Post`는 `Comment`와 관계가 있다면, 각각 해당 관계 수까지 로딩할 수 있습니다:

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
#### Morph To 지연 count 로딩

이미 가져온 `ActivityFeed` 컬렉션에도 `loadMorphCount`로 count를 지연 로딩할 수 있습니다:

```php
$activities = ActivityFeed::with('parentable')->get();

$activities->loadMorphCount('parentable', [
    Photo::class => ['tags'],
    Post::class => ['comments'],
]);
```

<a name="eager-loading"></a>
## 즉시 로딩 (Eager Loading)

동적 관계 속성으로 접근하면, 관계 모델은 "지연 로딩" 됩니다. 즉, 속성에 처음 접근할 때 비로소 쿼리가 실행됩니다. 반면, Eloquent는 부모 모델 쿼리 시점에 즉시 로딩을 지원해 "N + 1" 쿼리 문제를 막아줄 수 있습니다. 예를 들어, `Book`(belongs to `Author`) 모델에서:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Book extends Model
{
    /**
     * 이 책의 저자를 가져옵니다.
     */
    public function author(): BelongsTo
    {
        return $this->belongsTo(Author::class);
    }
}
```

책 목록 및 저자를 가져와서 아래처럼 쓸 경우:

```php
use App\Models\Book;

$books = Book::all();

foreach ($books as $book) {
    echo $book->author->name;
}
```

책이 25권이면, 26번의 쿼리가 실행됩니다(책 1번 + 저자 25번).

즉시 로딩을 사용하면 단 2번의 쿼리만 발생합니다:

```php
$books = Book::with('author')->get();

foreach ($books as $book) {
    echo $book->author->name;
}
```

쿼리는 이렇게 됩니다:

```sql
select * from books

select * from authors where id in (1, 2, 3, 4, 5, ...)
```

<a name="eager-loading-multiple-relationships"></a>
#### 여러 관계 즉시 로딩

즉시 로딩 대상이 여러 관계라면 배열로 전달합니다:

```php
$books = Book::with(['author', 'publisher'])->get();
```

<a name="nested-eager-loading"></a>
#### 중첩 관계 즉시 로딩

".(점)" 표기법으로 중첩 관계도 즉시 로딩할 수 있습니다. 예를 들어, 학습 대상이 저자이며, 저자의 연락처까지 미리 로드하려면:

```php
$books = Book::with('author.contacts')->get();
```

중첩 배열로 표기하면 여러 레벨의 관계도 명확하게 지정할 수 있습니다:

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

`morphTo` 관계의 중첩 관계도 즉시 로딩 가능합니다. `morphWith`를 조합해 사용합니다. 아래처럼 `ActivityFeed` 모델이 여러 부모 타입의 모델과 관계를 맺고 있고, 각 부모의 하위 관계까지 미리 로딩할 수 있습니다:

```php
<?php

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class ActivityFeed extends Model
{
    /**
     * activity feed의 부모 레코드를 가져옵니다.
     */
    public function parentable(): MorphTo
    {
        return $this->morphTo();
    }
}
```

아래처럼 사용합니다:

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
#### 관계의 일부 컬럼만 즉시 로딩

관계 모델 전체 컬럼이 필요 없다면, 아래처럼 원하는 컬럼만 골라서 불러올 수 있습니다:

```php
$books = Book::with('author:id,name,book_id')->get();
```

> [!WARNING]
> 이 기능을 쓸 때는 항상 `id` 컬럼 및 외래 키 컬럼을 컬럼 목록에 포함하세요.

<a name="eager-loading-by-default"></a>
#### 모델 조회 시 기본 즉시 로딩

항상 특정 관계를 자동으로 즉시 로딩하고 싶다면 모델의 `$with` 속성을 활용하세요:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Book extends Model
{
    /**
     * 항상 로딩할 관계 목록
     *
     * @var array
     */
    protected $with = ['author'];

    /**
     * 이 책의 저자를 가져옵니다.
     */
    public function author(): BelongsTo
    {
        return $this->belongsTo(Author::class);
    }

    /**
     * 이 책의 장르를 가져옵니다.
     */
    public function genre(): BelongsTo
    {
        return $this->belongsTo(Genre::class);
    }
}
```

단일 쿼리에서만 `$with` 속성을 제거하고 싶다면 `without` 메서드를 사용합니다:

```php
$books = Book::without('author')->get();
```

기본 `$with` 속성을 무시하고 지정한 관계만 로딩하고 싶으면 `withOnly`를 사용합니다:

```php
$books = Book::withOnly('genre')->get();
```

<a name="constraining-eager-loads"></a>
### 즉시 로딩시 조건 제한

즉시 로딩시 추가 쿼리 조건을 줘야 할 때, 배열 키에 관계명, 값에 제약을 추가하는 클로저를 전달하면 됩니다:

```php
use App\Models\User;

$users = User::with(['posts' => function ($query) {
    $query->where('title', 'like', '%code%');
}])->get();
```

기타 쿼리 빌더의 모든 메서드를 활용할 수 있습니다:

```php
$users = User::with(['posts' => function ($query) {
    $query->orderBy('created_at', 'desc');
}])->get();
```

<a name="constraining-eager-loading-of-morph-to-relationships"></a>
#### morphTo 관계의 즉시 로딩 조건 제한

`morphTo` 관계 즉시 로딩시, 각 타입별로 별도의 제약을 줄 수 있습니다. `MorphTo` 관계의 `constrain` 메서드를 사용합니다:

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

위 예시에서, Post는 숨김 여부로, Video는 타입으로 각각 필터링합니다.

<a name="constraining-eager-loads-with-relationship-existence"></a>
#### 관계 존재 조건과 함께 즉시 로딩

관계 존재 쿼리와 즉시 로딩을 동시에 원하는 경우, `withWhereHas` 메서드를 사용할 수 있습니다. 예를 들어, 필터링 조건을 만족하는 게시글만 로딩과 동시에 해당 게시글 데이터도 함께 로딩:

```php
use App\Models\User;

$users = User::withWhereHas('posts', function ($query) {
    $query->where('featured', true);
})->get();
```

<a name="lazy-eager-loading"></a>
### 지연 즉시 로딩

부모 모델을 이미 조회한 뒤, 조건에 따라 동적으로 관계를 즉시 로딩하고 싶다면 `load` 메서드를 사용할 수 있습니다:

```php
use App\Models\Book;

$books = Book::all();

if ($condition) {
    $books->load('author', 'publisher');
}
```

추가 쿼리 제약은 관계명 => 클로저 배열로 전달하면 됩니다:

```php
$author->load(['books' => function ($query) {
    $query->orderBy('published_date', 'asc');
}]);
```

이미 로딩된 관계는 제외하고 새로만 불러오고 싶으면 `loadMissing`을 사용합니다:

```php
$book->loadMissing('author');
```

<a name="nested-lazy-eager-loading-morphto"></a>
#### Nested Lazy Eager Loading과 morphTo

`morphTo` 관계와 중첩 관계도 `loadMorph`를 이용해 지연 로딩할 수 있습니다. 첫 번째 인수로 관계명, 두 번째엔 모델 => 관계 배열을 넘깁니다:

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
### 자동 즉시 로딩

> [!WARNING]
> 이 기능은 커뮤니티 피드백을 위해 베타 상태이며, 패치 릴리즈에서 동작과 기능이 바뀔 수 있습니다.

Laravel은 자동으로 접근되는 연관관계를 즉시 로딩할 수 있습니다. 자동 즉시 로딩을 활성화하려면, `AppServiceProvider`의 `boot` 메서드에서 `Model::automaticallyEagerLoadRelationships`를 호출하세요:

```php
use Illuminate\Database\Eloquent\Model;

/**
 * 애플리케이션 서비스 부트스트랩
 */
public function boot(): void
{
    Model::automaticallyEagerLoadRelationships();
}
```

이 옵션이 켜지면, 지정하지 않았더라도 이후 접근하는 연관관계가 자동으로 즉시 로딩됩니다. 예를 들어,

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

일반적으로는 각 유저, 각 게시글마다 추가 쿼리가 발생하지만, 자동 즉시 로딩 시 posts, comments가 한번에 지연 즉시 로딩(lazy eager loading)되어 쿼리 수가 대폭 줄어듭니다.

전역 적용이 아닌, 컬렉션 한 번에만 적용할 수도 있습니다:

```php
$users = User::where('vip', true)->get();

return $users->withRelationshipAutoloading();
```

<a name="preventing-lazy-loading"></a>
### 지연 로딩 방지

즉시 로딩은 성능 최적화에 도움이 됩니다. 원하지 않는 지연 로딩을 막으려면, Eloquent 모델의 `preventLazyLoading`을 사용할 수 있습니다. 보통은 `AppServiceProvider`의 `boot`에서 아래처럼 환경별로 적용합니다:

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

이렇게 하면, 지연 로딩을 시도한 경우 `Illuminate\Database\LazyLoadingViolationException` 예외가 발생합니다.

지연 로딩 위반 시의 동작을 커스터마이즈하려면, `handleLazyLoadingViolationsUsing` 메서드를 활용하세요. 예를 들어, 예외 대신 로그만 남기게 할 수도 있습니다:

```php
Model::handleLazyLoadingViolationUsing(function (Model $model, string $relation) {
    $class = $model::class;

    info("Attempted to lazy load [{$relation}] on model [{$class}].");
});
```

<a name="inserting-and-updating-related-models"></a>
## 연관관계 모델 삽입 및 갱신

<a name="the-save-method"></a>
### `save` 메서드

Eloquent는 새로운 모델을 연관관계로 추가할 다양한 편의 메서드를 제공합니다. 예를 들어, 게시글에 새 댓글을 추가할 때, `Comment` 모델의 `post_id`를 직접 지정하는 대신, 관계의 `save` 메서드를 사용할 수 있습니다:

```php
use App\Models\Comment;
use App\Models\Post;

$comment = new Comment(['message' => 'A new comment.']);

$post = Post::find(1);

$post->comments()->save($comment);
```

여기서 `comments` 동적 속성이 아니라 `comments` 메서드를 호출해야 합니다. `save`는 필요한 외래 키(`post_id`)를 자동으로 지정해줍니다.

여러개의 관련 모델을 한 번에 저장하려면, `saveMany`를 사용하세요:

```php
$post = Post::find(1);

$post->comments()->saveMany([
    new Comment(['message' => 'A new comment.']),
    new Comment(['message' => 'Another new comment.']),
]);
```

`save`, `saveMany`는 DB에는 저장되지만, 이미 로드된 in-memory 관계에는 추가해주지는 않습니다. 저장 후 곧바로 관계에 접근해야 한다면, `refresh`로 새로고침합니다:

```php
$post->comments()->save($comment);

$post->refresh();

// 모든 댓글—새로 저장한 것도 포함!
$post->comments;
```

<a name="the-push-method"></a>
#### 재귀적으로 모델과 관계 저장

연관된 모델까지 모두 한 번에 저장하려면, `push` 메서드를 사용할 수 있습니다. 예를 들어, 게시글, 댓글, 각 댓글의 저자까지 모두 저장합니다:

```php
$post = Post::find(1);

$post->comments[0]->message = 'Message';
$post->comments[0]->author->name = 'Author Name';

$post->push();
```

이벤트 발생 없이 저장만 하고 싶으면 `pushQuietly` 사용:

```php
$post->pushQuietly();
```

<a name="the-create-method"></a>
### `create` 메서드

`save`, `saveMany`외에, `create` 메서드로도 관계 모델을 생성할 수 있습니다. `save`가 전체 모델 인스턴스를 받는 반면, `create`는 단순 배열을 받으므로 더 간단합니다:

```php
use App\Models\Post;

$post = Post::find(1);

$comment = $post->comments()->create([
    'message' => 'A new comment.',
]);
```

다수 모델 생성은 `createMany`를 이용할 수 있습니다:

```php
$post = Post::find(1);

$post->comments()->createMany([
    ['message' => 'A new comment.'],
    ['message' => 'Another new comment.'],
]);
```

이벤트 없이 생성만 하고 싶을 때는 `createQuietly`, `createManyQuietly`를 사용합니다:

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

또는, `findOrNew`, `firstOrNew`, `firstOrCreate`, `updateOrCreate` 등 [관계에서의 모델 생성 및 갱신](/docs/12.x/eloquent#upserts) 메서드를 사용할 수 있습니다.

> [!NOTE]
> `create`를 사용하기 전에 [대량 할당(Mass Assignment)](/docs/12.x/eloquent#mass-assignment) 보안 문서를 꼭 참고하세요.

<a name="updating-belongs-to-relationships"></a>
### Belongs To 연관관계

자식 모델을 새로운 부모에 할당하고 싶다면, `associate` 메서드를 사용합니다. 아래 예시에서, `User`가 `Account`에 `belongsTo` 관계로 연결되고, `associate`가 외래 키를 지정해줍니다:

```php
use App\Models\Account;

$account = Account::find(10);

$user->account()->associate($account);

$user->save();
```

자식에서 부모를 제거하고 싶을 때는 `dissociate`를 사용해 외래 키를 null로 만듭니다:

```php
$user->account()->dissociate();

$user->save();
```

<a name="updating-many-to-many-relationships"></a>
### Many to Many 연관관계

<a name="attaching-detaching"></a>
#### Attach / Detach

다대다 관계에서 연결, 해제 모두를 도와주는 메서드가 있습니다. 예를 들어, 사용자를 역할과 연결(attach)할 때 아래처럼 중간 테이블에 레코드를 추가할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

$user->roles()->attach($roleId);
```

연결할 때 중간 테이블에 추가 데이터도 설정할 수 있습니다:

```php
$user->roles()->attach($roleId, ['expires' => $expires]);
```

연결 해제(detach)도 간단히 가능합니다:

```php
// 특정 역할만 제거
$user->roles()->detach($roleId);

// 모든 역할 제거
$user->roles()->detach();
```

배열을 사용해 다수 id를 한 번에 품을 수도 있습니다:

```php
$user = User::find(1);

$user->roles()->detach([1, 2, 3]);

$user->roles()->attach([
    1 => ['expires' => $expires],
    2 => ['expires' => $expires],
]);
```

<a name="syncing-associations"></a>
#### 관계 동기화

`s‌ync` 메서드는 다대다 관계를 완전히 동기화합니다. 인수로 넘긴 id 배열만 최종적으로 중간 테이블에 남기고, 기존에 있던 다른 id는 모두 제거됩니다:

```php
$user->roles()->sync([1, 2, 3]);
```

각 id별로 추가 데이터를 전달할 수 있습니다:

```php
$user->roles()->sync([1 => ['expires' => true], 2, 3]);
```

동일한 데이터를 전달해 모든 id에 쓰고 싶으면 `syncWithPivotValues`를 사용합니다:

```php
$user->roles()->syncWithPivotValues([1, 2, 3], ['active' => true]);
```

동기화 시 기존 id를 삭제하지 않고 추가만 하려면, `syncWithoutDetaching`을 사용하세요:

```php
$user->roles()->syncWithoutDetaching([1, 2, 3]);
```

<a name="toggling-associations"></a>
#### 관계 전환(Toggle)

`toggle` 메서드로 여러 id의 연결 상태를 한 번에 반전시킬 수 있습니다. 현재 연결되어 있으면 해제, 없으면 연결:

```php
$user->roles()->toggle([1, 2, 3]);
```

추가 데이터도 넘길 수 있습니다:

```php
$user->roles()->toggle([
    1 => ['expires' => true],
    2 => ['expires' => true],
]);
```

<a name="updating-a-record-on-the-intermediate-table"></a>
#### 중간 테이블 레코드 갱신

중간 테이블의 기존 값을 갱신해야 할 때는 `updateExistingPivot`을 사용합니다:

```php
$user = User::find(1);

$user->roles()->updateExistingPivot($roleId, [
    'active' => false,
]);
```

<a name="touching-parent-timestamps"></a>
## 부모 타임스탬프 갱신하기 (Touching Parent Timestamps)

`belongsTo`, `belongsToMany` 관계를 가지는 자식 모델에서, 부모 모델의 타임스탬프(예: `updated_at`)를 자동으로 갱신하고자 할 때가 있습니다.

예를 들어, `Comment`가 갱신될 때, 연결된 `Post`의 `updated_at`을 같이 최신화하고 싶다면, 자식 모델에 `touches` 속성에 관련 관계명을 나열하면 됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Comment extends Model
{
    /**
     * 타임스탬프를 갱신할 모든 연관관계
     *
     * @var array
     */
    protected $touches = ['post'];

    /**
     * 이 댓글이 달린 게시글을 가져옵니다.
     */
    public function post(): BelongsTo
    {
        return $this->belongsTo(Post::class);
    }
}
```

> [!WARNING]
> 부모 모델의 타임스탬프는 자식 모델이 Eloquent의 `save` 메서드로 갱신될 때만 자동 갱신됩니다.
