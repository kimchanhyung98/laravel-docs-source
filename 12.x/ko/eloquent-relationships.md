# 엘로크웬트: 관계 (Eloquent: Relationships)

- [소개](#introduction)
- [관계 정의하기](#defining-relationships)
    - [일대일 / Has One](#one-to-one)
    - [일대다 / Has Many](#one-to-many)
    - [일대다 (역방향) / Belongs To](#one-to-many-inverse)
    - [여러 개 중 하나 / Has One of Many](#has-one-of-many)
    - [중간 모델을 통한 일대일 / Has One Through](#has-one-through)
    - [중간 모델을 통한 일대다 / Has Many Through](#has-many-through)
- [스코프 관계](#scoped-relationships)
- [다대다 관계](#many-to-many)
    - [중간 테이블 컬럼 조회하기](#retrieving-intermediate-table-columns)
    - [중간 테이블 컬럼으로 쿼리 필터링하기](#filtering-queries-via-intermediate-table-columns)
    - [중간 테이블 컬럼으로 쿼리 정렬하기](#ordering-queries-via-intermediate-table-columns)
    - [사용자 정의 중간 테이블 모델 정의하기](#defining-custom-intermediate-table-models)
- [다형성 관계](#polymorphic-relationships)
    - [일대일](#one-to-one-polymorphic-relations)
    - [일대다](#one-to-many-polymorphic-relations)
    - [여러 개 중 하나](#one-of-many-polymorphic-relations)
    - [다대다](#many-to-many-polymorphic-relations)
    - [사용자 정의 다형성 타입](#custom-polymorphic-types)
- [동적 관계](#dynamic-relationships)
- [관계 쿼리하기](#querying-relations)
    - [관계 메서드와 동적 프로퍼티의 차이](#relationship-methods-vs-dynamic-properties)
    - [관계 존재성 쿼리하기](#querying-relationship-existence)
    - [관계 부존재성 쿼리하기](#querying-relationship-absence)
    - [Morph To 관계 쿼리하기](#querying-morph-to-relationships)
- [연관 모델 집계](#aggregating-related-models)
    - [연관 모델 수 세기](#counting-related-models)
    - [기타 집계 함수](#other-aggregate-functions)
    - [Morph To 관계의 연관 모델 수 세기](#counting-related-models-on-morph-to-relationships)
- [즉시 로딩(Eager Loading)](#eager-loading)
    - [즉시 로딩 제한하기](#constraining-eager-loads)
    - [지연 즉시 로딩(Lazy Eager Loading)](#lazy-eager-loading)
    - [자동 즉시 로딩](#automatic-eager-loading)
    - [지연 로딩 방지하기](#preventing-lazy-loading)
- [연관 모델 삽입 및 수정](#inserting-and-updating-related-models)
    - [`save` 메서드](#the-save-method)
    - [`create` 메서드](#the-create-method)
    - [Belongs To 관계](#updating-belongs-to-relationships)
    - [다대다 관계](#updating-many-to-many-relationships)
- [부모 타임스탬프 동기화](#touching-parent-timestamps)

<a name="introduction"></a>
## 소개

데이터베이스 테이블은 종종 서로 연결되어 있습니다. 예를 들어, 블로그 게시글(post)에는 여러 개의 댓글(comment)이 달릴 수 있고, 주문(order)은 그 주문을 등록한 사용자(user)와 관련될 수 있습니다. Eloquent는 이러한 관계를 쉽게 관리하고 사용할 수 있도록 해주며, 여러 가지 일반적인 관계 유형을 지원합니다.

<div class="content-list" markdown="1">

- [일대일(One To One)](#one-to-one)
- [일대다(One To Many)](#one-to-many)
- [다대다(Many To Many)](#many-to-many)
- [중간 모델을 통한 일대일(Has One Through)](#has-one-through)
- [중간 모델을 통한 일대다(Has Many Through)](#has-many-through)
- [일대일(다형성)](#one-to-one-polymorphic-relations)
- [일대다(다형성)](#one-to-many-polymorphic-relations)
- [다대다(다형성)](#many-to-many-polymorphic-relations)

</div>

<a name="defining-relationships"></a>
## 관계 정의하기

Eloquent 관계는 여러분의 Eloquent 모델 클래스에서 메서드로 정의합니다. 관계는 강력한 [쿼리 빌더](/docs/12.x/queries)이기도 하므로, 메서드로 정의하면 다양한 메서드 체이닝 및 쿼리 기능을 활용할 수 있습니다. 예를 들어, 다음과 같이 이 `posts` 관계에 추가 쿼리 조건을 쉽게 체이닝할 수 있습니다.

```php
$user->posts()->where('active', 1)->get();
```

이제 여러 관계 유형을 어떻게 정의하는지 본격적으로 살펴보기 전에, Eloquent에서 지원하는 각 관계 타입을 어떻게 정의하는지부터 알아보겠습니다.

<a name="one-to-one"></a>
### 일대일 / Has One

일대일(One-to-one) 관계는 데이터베이스 관계 중에서 가장 기본적인 유형입니다. 예를 들어, `User` 모델은 하나의 `Phone` 모델과만 연관될 수 있습니다. 이 관계를 정의하려면, `User` 모델에 `phone`이라는 메서드를 정의하고, 이 메서드에서 `hasOne` 메서드를 호출하여 반환하면 됩니다. `hasOne` 메서드는 모델의 기본 클래스인 `Illuminate\Database\Eloquent\Model`을 통해 사용할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasOne;

class User extends Model
{
    /**
     * 유저와 연관된 전화 정보를 가져옵니다.
     */
    public function phone(): HasOne
    {
        return $this->hasOne(Phone::class);
    }
}
```

`hasOne` 메서드의 첫 번째 인수에는 연관 모델 클래스명을 전달합니다. 관계를 이렇게 정의한 후에는, Eloquent의 동적 프로퍼티를 이용해 연관된 레코드를 가져올 수 있습니다. 동적 프로퍼티는 관계 메서드를 마치 모델에 정의된 프로퍼티처럼 사용할 수 있도록 해줍니다.

```php
$phone = User::find(1)->phone;
```

Eloquent는 기본적으로 부모 모델의 이름을 기준으로 관계의 외래 키(foreign key)를 결정합니다. 이 예제의 경우, `Phone` 모델에 `user_id`라는 외래 키가 있다고 자동으로 간주합니다. 만약 이 규칙을 변경하고 싶다면, `hasOne` 메서드의 두 번째 인수에 외래 키를 지정할 수 있습니다.

```php
return $this->hasOne(Phone::class, 'foreign_key');
```

또한, Eloquent는 외래 키의 값이 기본적으로 부모의 기본 키(일반적으로 `id`)와 같다고 가정합니다. 즉, Eloquent는 `Phone` 레코드의 `user_id` 컬럼 값이 해당 사용자의 `id` 컬럼 값과 일치하는지를 확인하게 됩니다. 만약 관계 정의에 쓸 기본 키가 `id`가 아니거나 모델의 `$primaryKey` 프로퍼티와 다르다면, 세 번째 인수로 로컬 키를 지정할 수 있습니다.

```php
return $this->hasOne(Phone::class, 'foreign_key', 'local_key');
```

<a name="one-to-one-defining-the-inverse-of-the-relationship"></a>
#### 관계의 역방향 정의하기

이제 `User` 모델에서 `Phone` 모델을 접근할 수 있게 되었습니다. 다음으로, `Phone` 모델에서도 이 전화를 소유한 사용자를 접근할 수 있도록 관계를 정의해보겠습니다. `hasOne` 관계에 대해 역방향(반대) 관계를 정의하려면 `belongsTo` 메서드를 사용합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Phone extends Model
{
    /**
     * 이 전화의 소유자인 유저를 가져옵니다.
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }
}
```

`user` 메서드를 호출하면, Eloquent는 `Phone` 모델의 `user_id` 컬럼과 일치하는 `id` 값을 가진 `User` 모델을 찾으려고 시도합니다.

Eloquent는 관계 메서드의 이름에 `_id`를 붙여 외래 키명을 정합니다. 즉, 이 예제에서는 `Phone` 모델에 `user_id` 컬럼이 있다고 간주합니다. 그러나 `Phone` 모델의 외래 키가 `user_id`가 아니라면, `belongsTo` 메서드의 두 번째 인수로 원하는 외래 키명을 지정할 수 있습니다.

```php
/**
 * 이 전화의 소유자인 유저를 가져옵니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class, 'foreign_key');
}
```

또한, 부모 모델이 기본 키로 `id`가 아닌 컬럼을 사용하거나, 연관 모델을 다른 컬럼으로 조회하고 싶다면, 세 번째 인수에 부모 테이블의 커스텀 키를 지정하면 됩니다.

```php
/**
 * 이 전화의 소유자인 유저를 가져옵니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class, 'foreign_key', 'owner_key');
}
```

<a name="one-to-many"></a>
### 일대다 / Has Many

일대다(One-to-many) 관계는 하나의 모델이 여러 자식 모델을 소유하는 관계에 사용합니다. 예를 들면, 하나의 블로그 게시글(post)은 수많은 댓글(comment)들을 가질 수 있습니다. 다른 Eloquent 관계와 마찬가지로, 일대다 관계도 모델에 메서드를 정의하여 구성합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Post extends Model
{
    /**
     * 블로그 게시글에 달린 댓글 목록을 가져옵니다.
     */
    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class);
    }
}
```

Eloquent는 `Comment` 모델에 필요한 적절한 외래 키 컬럼을 자동으로 결정합니다. 기본적으로, 부모 모델명의 스네이크 케이스(snake case)에 `_id`를 붙인 이름을 사용합니다. 위 예제에서는 `Comment` 모델의 외래 키 컬럼이 `post_id`가 됩니다.

이렇게 관계 메서드를 정의한 후에는, `comments` 프로퍼티를 통해 연관된 댓글 [컬렉션](/docs/12.x/eloquent-collections)을 가져올 수 있습니다. Eloquent의 "동적 관계 프로퍼티" 덕분에, 관계 메서드를 마치 모델의 프로퍼티처럼 접근할 수 있습니다.

```php
use App\Models\Post;

$comments = Post::find(1)->comments;

foreach ($comments as $comment) {
    // ...
}
```

모든 관계는 쿼리 빌더이기도 하므로, `comments` 메서드를 호출해 체이닝 방식으로 관계 쿼리에 조건을 추가할 수도 있습니다.

```php
$comment = Post::find(1)->comments()
    ->where('title', 'foo')
    ->first();
```

`hasOne` 메서드와 마찬가지로, 추가 인수로 외래 키와 로컬 키를 지정해 외래 키 규칙을 덮어쓸 수도 있습니다.

```php
return $this->hasMany(Comment::class, 'foreign_key');

return $this->hasMany(Comment::class, 'foreign_key', 'local_key');
```

<a name="automatically-hydrating-parent-models-on-children"></a>
#### 자식 모델에서 자동으로 부모 모델 로드하기

즉시 로딩(Eager Loading)을 사용하더라도, 자식 모델을 반복하면서 부모 모델을 참조할 때 "N + 1" 쿼리 문제가 발생할 수 있습니다.

```php
$posts = Post::with('comments')->get();

foreach ($posts as $post) {
    foreach ($post->comments as $comment) {
        echo $comment->post->title;
    }
}
```

위 예제에서는 모든 `Post` 모델에 댓글들을 즉시 로드했지만, Eloquent가 각 댓글(`Comment`)의 부모 `Post`를 자동으로 로드하지 않으므로 "N + 1" 문제(각 댓글마다 부모 조회 쿼리가 날아감)가 발생합니다.

이럴 때는, 관계 정의 시 `hasMany` 관계에 `chaperone` 메서드를 사용하면, Eloquent가 자식 모델에 해당하는 부모 모델을 자동으로 로드해줍니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Post extends Model
{
    /**
     * 블로그 게시글에 달린 댓글 목록을 가져옵니다.
     */
    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class)->chaperone();
    }
}
```

또는 즉시 로딩 시점에 자동 부모 모델 로딩 기능을 동적으로 활성화하고 싶다면, 관계를 즉시 로드할 때 `chaperone`을 사용할 수 있습니다.

```php
use App\Models\Post;

$posts = Post::with([
    'comments' => fn ($comments) => $comments->chaperone(),
])->get();
```

<a name="one-to-many-inverse"></a>
### 일대다 (역방향) / Belongs To

이제 게시글의 모든 댓글을 조회할 수 있으니, 이번엔 각 댓글에서 자신의 부모 게시글을 조회하는 관계를 정의해봅시다. `hasMany` 관계의 역방향은 자식 모델에 `belongsTo` 메서드를 호출하는 메서드를 추가함으로써 정의합니다.

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

이렇게 정의하면, 댓글의 부모 게시글을 동적 관계 프로퍼티 `post`를 통해 접근할 수 있습니다.

```php
use App\Models\Comment;

$comment = Comment::find(1);

return $comment->post->title;
```

위 예제에서, Eloquent는 `comments` 테이블의 `post_id` 컬럼과 일치하는 `id` 값을 가진 `Post` 모델을 찾습니다.

Eloquent는 관계 메서드명의 마지막에 `_`와 부모 모델의 기본 키명을 붙여, 기본 외래 키명을 만듭니다. 위 예제의 경우, `comments` 테이블에는 `post_id` 컬럼이 있다고 간주합니다.

만약 관계의 외래 키명이 이 규칙과 다르다면, `belongsTo` 메서드의 두 번째 인수에 원하는 외래 키명을 넘겨줄 수 있습니다.

```php
/**
 * 이 댓글이 달린 게시글을 가져옵니다.
 */
public function post(): BelongsTo
{
    return $this->belongsTo(Post::class, 'foreign_key');
}
```

부모 모델의 기본 키가 `id`가 아닐 때나, 관계 검색에 특정 컬럼을 사용하고 싶을 때는 세 번째 인수로 커스텀 키명을 지정하세요.

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
#### 기본 모델(Null Object Pattern)

`belongsTo`, `hasOne`, `hasOneThrough`, `morphOne` 관계에서는 해당 관계가 `null`일 때 반환할 기본 모델을 정의할 수 있습니다. 이 패턴을 흔히 [Null Object 패턴](https://en.wikipedia.org/wiki/Null_Object_pattern)이라고 하며, 코드에서 조건문 사용을 줄여주는 데 도움이 됩니다. 아래 예시에서, `Post` 모델에 연결된 사용자가 없으면 `user` 관계가 비어 있는 `App\Models\User` 모델을 반환합니다.

```php
/**
 * 게시글 작성자를 반환합니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault();
}
```

기본 모델을 특정 속성으로 채우려면, `withDefault` 메서드에 배열이나 클로저를 전달할 수 있습니다.

```php
/**
 * 게시글 작성자를 반환합니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault([
        'name' => 'Guest Author',
    ]);
}

/**
 * 게시글 작성자를 반환합니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault(function (User $user, Post $post) {
        $user->name = 'Guest Author';
    });
}
```

<a name="querying-belongs-to-relationships"></a>
#### Belongs To 관계 쿼리하기

"Belongs To" 관계의 자식 데이터를 조회할 때, `where` 절을 직접 작성해서 관련 Eloquent 모델을 가져올 수도 있습니다.

```php
use App\Models\Post;

$posts = Post::where('user_id', $user->id)->get();
```

그러나 더 편리하게는, 적절한 관계와 외래 키를 자동으로 판단해주는 `whereBelongsTo` 메서드를 사용할 수 있습니다.

```php
$posts = Post::whereBelongsTo($user)->get();
```

또한, `whereBelongsTo` 메서드에 [컬렉션](/docs/12.x/eloquent-collections) 인스턴스를 전달할 수도 있습니다. 이 경우 컬렉션 내의 어느 부모 모델에 속한 데이터든 한 번에 조회할 수 있습니다.

```php
$users = User::where('vip', true)->get();

$posts = Post::whereBelongsTo($users)->get();
```

기본적으로, Laravel은 전달된 모델의 클래스명에서 관계명을 추정합니다. 하지만 필요하다면 두 번째 인수로 관계 이름을 직접 지정할 수도 있습니다.

```php
$posts = Post::whereBelongsTo($user, 'author')->get();
```

<a name="has-one-of-many"></a>
### 여러 개 중 하나 / Has One of Many

경우에 따라, 한 모델이 관련된 여러 모델을 가질 수 있지만, 그 중 "가장 최근" 또는 "가장 오래된" 한 개만 쉽게 조회하고 싶을 때가 있습니다. 예를 들어, `User` 모델이 여러 개의 `Order` 모델과 연결되어 있다고 할 때, 사용자가 가장 최근에 주문한 주문만 빠르게 가지고 오고 싶을 수 있습니다. 이럴 때는 `hasOne` 관계와 `ofMany` 계열 메서드를 함께 사용하면 됩니다.

```php
/**
 * 유저의 가장 최근 주문을 가져옵니다.
 */
public function latestOrder(): HasOne
{
    return $this->hasOne(Order::class)->latestOfMany();
}
```

마찬가지로, "가장 오래된" 즉, 첫 번째로 연관된 모델을 가져오는 메서드도 정의할 수 있습니다.

```php
/**
 * 유저의 가장 오래된 주문을 가져옵니다.
 */
public function oldestOrder(): HasOne
{
    return $this->hasOne(Order::class)->oldestOfMany();
}
```

기본적으로 `latestOfMany`와 `oldestOfMany` 메서드는 모델의 기본 키(정렬 가능한 값)를 기준으로 가장 최근 또는 가장 오래된 연관 모델을 조회합니다. 하지만, 더 복잡한 정렬 기준으로 한 개의 모델을 가져오고 싶을 때도 있습니다.

예를 들어, `ofMany` 메서드를 사용하면 사용자의 "가장 비싼" 주문만 가져오도록 할 수 있습니다. `ofMany`의 첫 번째 인수에는 정렬할 컬럼명을, 두 번째 인수에는 사용할 집계 함수(예: `min`, `max`)를 지정합니다.

```php
/**
 * 유저의 가장 큰(가장 비싼) 주문을 가져옵니다.
 */
public function largestOrder(): HasOne
{
    return $this->hasOne(Order::class)->ofMany('price', 'max');
}
```

> [!WARNING]
> PostgreSQL은 UUID 컬럼에 대해 `MAX` 함수를 적용하는 것을 지원하지 않으므로, PostgreSQL UUID 컬럼과 one-of-many 관계를 함께 사용할 수 없습니다.

<a name="converting-many-relationships-to-has-one-relationships"></a>
#### "Many" 관계를 Has One 관계로 변환하기

종종 `latestOfMany`, `oldestOfMany`, `ofMany` 메서드로 단일 모델을 조회할 때, 이미 같은 모델로 "has many" 관계가 정의되어 있을 수 있습니다. 이럴 때 Laravel은 `one` 메서드를 관계에 연결해 매우 손쉽게 "has many"를 "has one" 관계로 변환할 수 있게 해줍니다.

```php
/**
 * 유저의 모든 주문을 가져옵니다.
 */
public function orders(): HasMany
{
    return $this->hasMany(Order::class);
}

/**
 * 유저의 가장 큰(가장 비싼) 주문을 가져옵니다.
 */
public function largestOrder(): HasOne
{
    return $this->orders()->one()->ofMany('price', 'max');
}
```

`one` 메서드는 `HasManyThrough` 관계에도 사용할 수 있고, 이 경우 `HasOneThrough` 관계로 변환됩니다.

```php
public function latestDeployment(): HasOneThrough
{
    return $this->deployments()->one()->latestOfMany();
}
```

<a name="advanced-has-one-of-many-relationships"></a>
#### 고급 Has One of Many 관계

더 복잡한 "여러 개 중 하나" 관계도 정의할 수 있습니다. 예를 들어, `Product` 모델이 여러 개의 `Price` 모델과 연결되어 있고, 새 가격이 나와도 과거 가격 정보는 시스템에 그대로 남아 있습니다. 또한, 새로운 가격 데이터를 미리 등록해 두고, `published_at` 컬럼을 통해 미래 시점에 발효되도록 할 수도 있습니다.

즉, "발행일자가 미래가 아닌 가장 최근 가격"이 필요한 시나리오입니다. 그리고 published_at이 같은 두 가격이 있을 경우, ID가 더 큰(최근) 것을 우선하도록 한다고 가정합시다. 이를 위해, `ofMany` 메서드에는 정렬 컬럼 배열을 전달하고, 쿼리 조건을 추가하는 클로저를 두 번째 인수로 전달하면 됩니다.

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
### 중간 모델을 통한 일대일 / Has One Through

"has-one-through" 관계는 다른 모델과의 일대일 관계를 정의하는 방식입니다. 다만, 이 관계는 현재 모델이 _중간에 위치한 모델을 거쳐서_ 최종적으로 한 번만 연결되는 모델과 연관된다는 의미입니다.

예를 들어 자동차 정비소 애플리케이션에서, 각 `Mechanic` 모델(정비공)은 하나의 `Car` 모델(자동차)과 관계를 맺고 있고, 각 `Car` 모델은 하나의 `Owner` 모델(차주)와 연결된다고 합시다. 이때 정비공과 차주는 데이터베이스상 직접적인 관계가 없지만, 정비공이 맡고 있는 자동차를 통해 차주 정보를 조회하는 것이 가능합니다. 이를 위한 테이블 구조는 아래와 같습니다.

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

테이블 구조를 살펴봤으니, 이제 `Mechanic` 모델에서 이 관계를 정의해보겠습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasOneThrough;

class Mechanic extends Model
{
    /**
     * 자동차 소유자(owner)를 가져옵니다.
     */
    public function carOwner(): HasOneThrough
    {
        return $this->hasOneThrough(Owner::class, Car::class);
    }
}
```

`hasOneThrough` 메서드의 첫 번째 인수는 최종적으로 접근하려는 모델(여기서는 `Owner`), 두 번째 인수는 중간에 거치는 모델(여기서는 `Car`)의 클래스명을 넣습니다.

또는, 관계에 관련된 모든 모델에서 이미 각각의 관계가 정의되어 있다면, 관계명 문자열이나 동적 메서드 체이닝(`through`, `has`)을 통해 더 유연하게 "has-one-through" 관계를 정의할 수도 있습니다. 예를 들어, `Mechanic` 모델에 `cars` 관계가, `Car` 모델에 `owner` 관계가 있다면 아래처럼 할 수 있습니다.

```php
// 문자열 기반 문법
return $this->through('cars')->has('owner');

// 동적 문법
return $this->throughCars()->hasOwner();
```

<a name="has-one-through-key-conventions"></a>

#### 키 사용 규칙

관계 쿼리를 수행할 때는 일반적인 Eloquent 외래 키 규칙이 적용됩니다. 만약 관계의 키를 직접 지정하고 싶다면, `hasOneThrough` 메서드의 세 번째와 네 번째 인수로 각각 중간 모델과 최종 모델의 외래 키를 전달하면 됩니다. 다섯 번째 인수는 로컬 키이고, 여섯 번째 인수는 중간 모델의 로컬 키입니다:

```php
class Mechanic extends Model
{
    /**
     * 차량 소유자 정보를 가져옵니다.
     */
    public function carOwner(): HasOneThrough
    {
        return $this->hasOneThrough(
            Owner::class,
            Car::class,
            'mechanic_id', // cars 테이블의 외래 키...
            'car_id', // owners 테이블의 외래 키...
            'id', // mechanics 테이블의 로컬 키...
            'id' // cars 테이블의 로컬 키...
        );
    }
}
```

또는, 앞서 설명한 것처럼 관계에 연관된 모든 모델에 이미 해당 관계가 정의되어 있다면, `through` 메서드로 관계명을 지정하여 "has-one-through" 관계를 더 유연하게 정의할 수 있습니다. 이 방법의 장점은 이미 정의된 관계의 키 규칙을 재사용할 수 있다는 점입니다:

```php
// 문자열 기반 문법
return $this->through('cars')->has('owner');

// 동적 문법
return $this->throughCars()->hasOwner();
```

<a name="has-many-through"></a>
### Has Many Through

"has-many-through" 관계는 중간 관계를 통해 멀리 떨어진 모델에 편리하게 접근할 수 있는 방법을 제공합니다. 예를 들어, [Laravel Cloud](https://cloud.laravel.com)와 같은 배포 플랫폼을 만든다고 가정해 보겠습니다. `Application` 모델은 중간의 `Environment` 모델을 통해 여러 `Deployment` 모델에 접근할 수 있습니다. 이 구조를 활용하면 애플리케이션에 해당하는 모든 배포 내역을 쉽게 조회할 수 있습니다. 해당 관계를 정의하기 위한 테이블 구조는 다음과 같습니다.

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

이제 관계에 필요한 테이블 구조를 확인했으니, `Application` 모델에서 관계를 정의해 보겠습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasManyThrough;

class Application extends Model
{
    /**
     * 이 애플리케이션의 모든 배포 내역을 가져옵니다.
     */
    public function deployments(): HasManyThrough
    {
        return $this->hasManyThrough(Deployment::class, Environment::class);
    }
}
```

`hasManyThrough` 메서드의 첫 번째 인수는 최종적으로 접근하려는 모델의 클래스명이고, 두 번째 인수는 중간 모델의 클래스명입니다.

또는, 앞서 설명한 것처럼 관련된 모든 모델에 필요한 관계가 정의되어 있다면, `through` 메서드를 호출하고 해당 관계명들을 넘겨주는 방식으로 "has-many-through" 관계를 직접 정의할 수도 있습니다. 예를 들어, `Application` 모델에 `environments` 관계가, `Environment` 모델에 `deployments` 관계가 각각 정의되어 있다면 다음처럼 연결할 수 있습니다.

```php
// 문자열 기반 문법
return $this->through('environments')->has('deployments');

// 동적 문법
return $this->throughEnvironments()->hasDeployments();
```

`Deployment` 모델의 테이블에는 `application_id` 컬럼이 없지만, `hasManyThrough` 관계를 통해 `$application->deployments`로 애플리케이션의 배포 내역을 조회할 수 있습니다. 이 과정에서 Eloquent는 중간 테이블인 `environments`의 `application_id` 컬럼을 확인한 후, 일치하는 environment ID들로 `deployments` 테이블을 조회합니다.

<a name="has-many-through-key-conventions"></a>
#### 키 사용 규칙

관계 쿼리를 수행할 때는 일반적인 Eloquent 외래 키 규칙이 적용됩니다. 만약 관계의 키를 직접 지정하고 싶다면, `hasManyThrough` 메서드의 세 번째와 네 번째 인수에 각각 중간 모델과 최종 모델의 외래 키를 전달할 수 있습니다. 다섯 번째 인수는 로컬 키이고, 여섯 번째 인수는 중간 모델의 로컬 키입니다:

```php
class Application extends Model
{
    public function deployments(): HasManyThrough
    {
        return $this->hasManyThrough(
            Deployment::class,
            Environment::class,
            'application_id', // environments 테이블의 외래 키...
            'environment_id', // deployments 테이블의 외래 키...
            'id', // applications 테이블의 로컬 키...
            'id' // environments 테이블의 로컬 키...
        );
    }
}
```

또는, 앞서 설명한 것처럼 모든 모델에 관계가 이미 정의되어 있다면, `through` 메서드를 호출해 "has-many-through" 관계를 정의할 수 있고, 이 방식의 장점은 기존 관계에 설정된 키 규칙을 그대로 재사용할 수 있다는 점입니다.

```php
// 문자열 기반 문법
return $this->through('environments')->has('deployments');

// 동적 문법
return $this->throughEnvironments()->hasDeployments();
```

<a name="scoped-relationships"></a>
### 범위가 지정된(Scoped) 관계

관계에 제한을 걸기 위해 모델에 추가 메서드를 정의하는 경우가 많습니다. 예를 들어, `User` 모델에는 전체 `posts` 관계에 추가적인 `where` 제한을 걸어주는 `featuredPosts` 메서드를 만들 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class User extends Model
{
    /**
     * 사용자의 포스트 목록을 가져옵니다.
     */
    public function posts(): HasMany
    {
        return $this->hasMany(Post::class)->latest();
    }

    /**
     * 사용자의 대표(특집) 포스트를 가져옵니다.
     */
    public function featuredPosts(): HasMany
    {
        return $this->posts()->where('featured', true);
    }
}
```

하지만 `featuredPosts` 메서드를 통해 모델을 생성(create)하면, `featured` 속성이 자동으로 `true`로 설정되지 않습니다. 관계 메서드를 통해 모델을 생성할 때, 해당 관계를 통해 생성되는 모든 모델에 지정할 속성을 설정하고 싶다면 관계 쿼리를 작성할 때 `withAttributes` 메서드를 사용하면 됩니다.

```php
/**
 * 사용자의 대표(특집) 포스트를 가져옵니다.
 */
public function featuredPosts(): HasMany
{
    return $this->posts()->withAttributes(['featured' => true]);
}
```

`withAttributes` 메서드는 쿼리에 제공된 속성값에 따라 자동으로 `where` 조건을 추가하고, 해당 관계를 통해 생성되는 모든 모델에도 해당 속성을 적용해줍니다.

```php
$post = $user->featuredPosts()->create(['title' => 'Featured Post']);

$post->featured; // true
```

만약 `withAttributes` 메서드가 쿼리에 `where` 조건을 추가하지 않게 하고 싶으면, `asConditions` 인수를 `false`로 지정할 수 있습니다.

```php
return $this->posts()->withAttributes(['featured' => true], asConditions: false);
```

<a name="many-to-many"></a>
## 다대다(Many to Many) 관계

다대다 관계는 `hasOne` 또는 `hasMany` 관계에 비해 약간 더 복잡합니다. 예를 들어, 한 사용자는 여러 역할을 가질 수 있고, 각각의 역할은 애플리케이션 내 다른 사용자와도 공유될 수 있습니다. 즉, 한 사용자는 'Author', 'Editor' 등 여러 역할을 가질 수 있으며, 그 역할은 또 다른 사용자에게도 할당될 수 있습니다. 즉, 사용자는 여러 역할을 가지며, 역할도 여러 사용자를 가집니다.

<a name="many-to-many-table-structure"></a>
#### 테이블 구조

이 관계를 정의하려면 세 개의 데이터베이스 테이블이 필요합니다: `users`, `roles`, 그리고 `role_user`. `role_user` 테이블은 관계되는 모델 클래스명을 알파벳 순으로 결합해 만든 이름이며, `user_id`와 `role_id` 컬럼을 가지고 있습니다. 이 테이블은 users와 roles를 연결하는 중간 테이블로 작동합니다.

역할(role)은 여러 사용자에게 할당될 수 있기 때문에, `roles` 테이블에 `user_id` 컬럼을 추가하는 방법은 적절하지 않습니다. 그렇게 하면 하나의 역할이 한 명의 사용자에게만 할당될 수 있습니다. 여러 사용자에게 역할을 할당하려면 반드시 `role_user`와 같은 중간 테이블이 필요합니다. 이 관계의 테이블 구조는 다음과 같이 요약할 수 있습니다:

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

다대다 관계는 `belongsToMany` 메서드를 반환하는 메서드를 모델에 정의하여 구현합니다. `belongsToMany` 메서드는 모든 Eloquent 모델의 기반 클래스인 `Illuminate\Database\Eloquent\Model`에서 제공됩니다. 예를 들어, `User` 모델에서 `roles` 메서드를 다음과 같이 정의할 수 있습니다. 이때 첫 번째 인수는 관계를 맺을 모델 클래스명입니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class User extends Model
{
    /**
     * 사용자가 가지고 있는 역할 목록을 반환합니다.
     */
    public function roles(): BelongsToMany
    {
        return $this->belongsToMany(Role::class);
    }
}
```

관계가 정의되면 동적 관계 속성인 `roles`를 통해 사용자의 역할 정보를 조회할 수 있습니다.

```php
use App\Models\User;

$user = User::find(1);

foreach ($user->roles as $role) {
    // ...
}
```

관계 역시 쿼리 빌더 역할을 하므로, 추가 조건을 `roles` 메서드에 연결해서 쿼리를 세밀하게 제어할 수 있습니다.

```php
$roles = User::find(1)->roles()->orderBy('name')->get();
```

관계의 중간 테이블(table) 이름을 결정할 때, Eloquent는 두 모델 이름을 알파벳 순서로 합칩니다. 그러나 이 규칙을 직접 지정할 수도 있으며, 두 번째 인수로 테이블 이름을 넘기면 됩니다.

```php
return $this->belongsToMany(Role::class, 'role_user');
```

중간 테이블 이름뿐만 아니라, 테이블 키 컬럼명도 추가 인수로 직접 지정할 수 있습니다. 세 번째 인수는 관계를 정의한 모델(즉, 호출한 쪽)의 외래 키 컬럼명, 네 번째 인수는 연결되는 모델의 외래 키 컬럼명입니다.

```php
return $this->belongsToMany(Role::class, 'role_user', 'user_id', 'role_id');
```

<a name="many-to-many-defining-the-inverse-of-the-relationship"></a>
#### 관계의 역방향 정의

다대다 관계의 "역방향"을 정의하려면, 관계를 맺고 있는 대상 모델에도 똑같이 `belongsToMany` 메서드를 반환하는 메서드를 정의해야 합니다. 예시의 사용자/역할 관계로 완성해 보면, 이번에는 `Role` 모델에 `users` 메서드를 정의해보겠습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class Role extends Model
{
    /**
     * 이 역할이 할당된 사용자 목록을 반환합니다.
     */
    public function users(): BelongsToMany
    {
        return $this->belongsToMany(User::class);
    }
}
```

보시다시피, 해당 관계는 `User` 모델에서처럼 정의하되 참조하는 클래스명만 반대(`App\Models\User`)로 바꾸면 됩니다. 똑같이 `belongsToMany` 메서드를 사용하므로, 다대다 관계의 역방향을 정의할 때도 테이블/키 이름을 직접 지정하는 등 모든 옵션을 사용할 수 있습니다.

<a name="retrieving-intermediate-table-columns"></a>
### 중간 테이블 컬럼 값 조회

이미 살펴본 것처럼, 다대다 관계를 사용하려면 중간 테이블이 필요합니다. Eloquent는 중간 테이블과 연동하는 여러 편리한 방법을 제공합니다. 예를 들어, `User` 모델이 여러 `Role` 모델과 관계를 가지고 있다면, 해당 관계에서 중간 테이블 정보를 `pivot` 속성을 통해 접근할 수 있습니다.

```php
use App\Models\User;

$user = User::find(1);

foreach ($user->roles as $role) {
    echo $role->pivot->created_at;
}
```

이 예제에서 보듯, 조회된 각 `Role` 모델에는 자동으로 `pivot` 속성이 할당됩니다. 이 속성에는 중간 테이블의 레코드를 표현하는 모델 인스턴스가 담깁니다.

기본적으로 `pivot` 모델에는 중간 테이블의 키 정보만 저장됩니다. 만약 중간 테이블에 추가 컬럼이 있다면, 관계를 정의할 때 `withPivot` 메서드를 호출해 컬럼명을 지정해야 합니다.

```php
return $this->belongsToMany(Role::class)->withPivot('active', 'created_by');
```

만약 중간 테이블에서 Eloquent가 자동으로 관리해주는 `created_at`, `updated_at` 타임스탬프 컬럼을 사용하고 싶다면, 관계를 정의할 때 `withTimestamps` 메서드를 추가하면 됩니다.

```php
return $this->belongsToMany(Role::class)->withTimestamps();
```

> [!WARNING]
> Eloquent의 자동 타임스탬프 관리 기능을 사용하는 중간 테이블은 반드시 `created_at`과 `updated_at` 컬럼을 모두 가져야 합니다.

<a name="customizing-the-pivot-attribute-name"></a>
#### `pivot` 속성명 커스터마이징

위에서 설명했듯, 중간 테이블의 속성은 모델에서 `pivot` 속성으로 접근할 수 있습니다. 하지만, 애플리케이션에서 더 목적에 맞는 다른 이름으로 이 속성을 바꿀 수도 있습니다.

예를 들어, 사용자가 팟캐스트에 구독(subscribe)할 수 있는 구조라면, 사용자는 podcasts와 다대다 관계를 가지게 됩니다. 이때 중간 테이블의 속성 이름을 `pivot` 대신 `subscription`으로 바꿔 사용하는 것이 가독성에 더 유리할 수도 있습니다. 관계 정의 시 `as` 메서드를 이용해 속성명을 변경할 수 있습니다.

```php
return $this->belongsToMany(Podcast::class)
    ->as('subscription')
    ->withTimestamps();
```

이렇게 사용자 지정 중간 테이블 속성이 지정되면, 해당 이름으로 중간 테이블 데이터를 가져올 수 있습니다.

```php
$users = User::with('podcasts')->get();

foreach ($users->flatMap->podcasts as $podcast) {
    echo $podcast->subscription->created_at;
}
```

<a name="filtering-queries-via-intermediate-table-columns"></a>
### 중간 테이블 컬럼을 활용한 쿼리 필터링

`belongsToMany` 관계 쿼리에서 `wherePivot`, `wherePivotIn`, `wherePivotNotIn`, `wherePivotBetween`, `wherePivotNotBetween`, `wherePivotNull`, `wherePivotNotNull` 메서드를 사용해 중간 테이블의 컬럼 기준으로 결과를 필터링할 수 있습니다.

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

`wherePivot`은 쿼리에 where 절 조건만 추가해주며, 관계를 통해 새 모델을 생성할 때는 해당 값을 자동으로 설정하지 않습니다. 만약 특정 pivot 값을 조건에도 사용하고, 생성할 때도 해당 값을 적용하고 싶으면 `withPivotValue` 메서드를 사용할 수 있습니다.

```php
return $this->belongsToMany(Role::class)
    ->withPivotValue('approved', 1);
```

<a name="ordering-queries-via-intermediate-table-columns"></a>
### 중간 테이블 컬럼을 이용한 쿼리 정렬

`belongsToMany` 관계 쿼리에서 `orderByPivot` 메서드를 이용해 중간 테이블 컬럼값 기준으로 결과를 정렬할 수 있습니다. 예를 들어, 사용자의 최신 배지를 조회하려면 다음과 같이 사용할 수 있습니다.

```php
return $this->belongsToMany(Badge::class)
    ->where('rank', 'gold')
    ->orderByPivot('created_at', 'desc');
```

<a name="defining-custom-intermediate-table-models"></a>
### 커스텀 중간 테이블 모델 정의

다대다 관계의 중간 테이블을 표현하는 커스텀 모델을 정의하려면, 관계 정의 시 `using` 메서드를 호출합니다. 커스텀 pivot 모델을 사용하면, 그 안에 별도의 메서드나 casts 등을 추가해 더 유연하게 제어할 수 있습니다.

커스텀 다대다 pivot 모델은 `Illuminate\Database\Eloquent\Relations\Pivot` 클래스를, 다형성 관계용 커스텀 pivot 모델은 `Illuminate\Database\Eloquent\Relations\MorphPivot` 클래스를 상속해야 합니다. 예를 들어, 커스텀 `RoleUser` pivot 모델을 사용하는 `Role` 모델을 정의할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class Role extends Model
{
    /**
     * 이 역할이 할당된 사용자 목록을 반환합니다.
     */
    public function users(): BelongsToMany
    {
        return $this->belongsToMany(User::class)->using(RoleUser::class);
    }
}
```

`RoleUser` 모델을 정의할 때는, 반드시 `Illuminate\Database\Eloquent\Relations\Pivot` 클래스를 상속받아야 합니다:

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
> Pivot 모델은 `SoftDeletes` 트레이트를 사용할 수 없습니다. Pivot 레코드를 소프트 삭제(soft delete)로 관리하려면, pivot 모델을 실제 Eloquent 모델로 전환할 것을 고려해야 합니다.

<a name="custom-pivot-models-and-incrementing-ids"></a>
#### 커스텀 Pivot 모델과 자동 증가 ID

커스텀 pivot 모델을 사용하는 다대다 관계에서, pivot 모델이 자동 증가(primary key) ID를 사용하는 구조라면, 해당 커스텀 pivot 모델 클래스에 `incrementing` 속성이 `true`로 명시되어 있어야 합니다.

```php
/**
 * 이 ID들이 자동 증가하는지 여부를 나타냅니다.
 *
 * @var bool
 */
public $incrementing = true;
```

<a name="polymorphic-relationships"></a>
## 다형성(Polymorphic) 관계

다형성 관계는 하나의 자식 모델이 여러 타입의 상위 모델과 연결될 수 있도록 해줍니다. 예를 들어, 블로그 게시글과 동영상을 함께 공유할 수 있는 애플리케이션을 만든다고 가정해보면, `Comment`(댓글) 모델이 `Post`와 `Video` 두 모델과 모두 관계를 맺을 수 있습니다.

<a name="one-to-one-polymorphic-relations"></a>
### 일대일(One to One) 다형성 관계

<a name="one-to-one-polymorphic-table-structure"></a>
#### 테이블 구조

일대일 다형성 관계는 일반적인 일대일 관계와 비슷하지만, 자식 모델이 하나의 연관 컬럼을 통해 여러 타입의 상위 모델과 연결될 수 있다는 점이 다릅니다. 예를 들어, 블로그 `Post`와 `User`가 모두 `Image` 모델과 다형성 관계를 맺을 수 있습니다. 일대일 다형성 관계를 사용하면, 게시글과 사용자에 공유되는 이미지 정보를 하나의 테이블로 통합해 저장할 수 있습니다. 먼저, 테이블 구조를 살펴보겠습니다:

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

여기서 `images` 테이블의 `imageable_id`와 `imageable_type` 컬럼이 다형성 관계를 가능하게 해줍니다. `imageable_id`에는 포스트 또는 사용자의 ID 값이 들어가고, `imageable_type`에는 상위 모델의 클래스명이 저장됩니다. Eloquent는 `imageable_type` 컬럼을 이용해 어떤 모델이 이미지를 가지고 있는지 판단합니다. 즉, 이 컬럼 값이 `App\Models\Post` 또는 `App\Models\User` 중 어느 쪽이냐에 따라 다르게 동작합니다.

<a name="one-to-one-polymorphic-model-structure"></a>
#### 모델 구조

이제 이 관계를 구현하기 위한 모델 정의를 살펴보겠습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class Image extends Model
{
    /**
     * 상위 imageable(사용자 또는 포스트) 모델을 반환합니다.
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
     * 해당 포스트의 이미지를 반환합니다.
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
     * 해당 사용자의 이미지를 반환합니다.
     */
    public function image(): MorphOne
    {
        return $this->morphOne(Image::class, 'imageable');
    }
}
```

<a name="one-to-one-polymorphic-retrieving-the-relationship"></a>
#### 관계 조회

데이터베이스 테이블 및 모델이 정의되면, 각 모델에서 다형성 관계를 활용할 수 있습니다. 예를 들어, 포스트에 연결된 이미지를 조회하려면 동적 관계 속성인 `image`를 사용할 수 있습니다.

```php
use App\Models\Post;

$post = Post::find(1);

$image = $post->image;
```

반대로, 다형성 모델에서 상위(부모) 모델을 조회하려면, `morphTo`를 호출하는 메서드명을 동적 관계 속성으로 접근하면 됩니다. 여기서는 `Image` 모델의 `imageable` 메서드를 사용합니다.

```php
use App\Models\Image;

$image = Image::find(1);

$imageable = $image->imageable;
```

`Image` 모델의 `imageable` 관계는 이미지를 소유한 모델이 `Post`일 수도, `User`일 수도 있으므로, 그에 맞는 인스턴스를 반환합니다.

<a name="morph-one-to-one-key-conventions"></a>

#### 주요 관례

필요하다면, 다형성 자식 모델에서 사용되는 "id"와 "type" 컬럼의 이름을 명시적으로 지정할 수 있습니다. 이러한 경우에는 반드시 `morphTo` 메서드의 첫 번째 인수로 관계의 이름을 전달해야 합니다. 일반적으로 이 값은 메서드명과 일치하는 것이 좋으므로, PHP의 `__FUNCTION__` 상수를 사용할 수 있습니다.

```php
/**
 * 이미지가 속한 모델을 반환합니다.
 */
public function imageable(): MorphTo
{
    return $this->morphTo(__FUNCTION__, 'imageable_type', 'imageable_id');
}
```

<a name="one-to-many-polymorphic-relations"></a>
### 1:N (다형성)

<a name="one-to-many-polymorphic-table-structure"></a>
#### 테이블 구조

1:N 다형성 관계는 기본적인 1:N 관계와 비슷하지만, 자식 모델이 단일 연관 컬럼만으로 여러 종류의 모델에 소속될 수 있습니다. 예를 들어, 애플리케이션의 사용자들이 포스트와 비디오 모두에 "댓글"을 남길 수 있다고 가정해봅시다. 다형성 관계를 사용하면 하나의 `comments` 테이블로 포스트와 비디오 모두에 대한 댓글 정보를 관리할 수 있습니다. 먼저, 이 관계를 구축하기 위한 테이블 구조를 살펴보겠습니다.

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

이제 이 관계를 만들기 위한 모델 정의를 살펴보겠습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class Comment extends Model
{
    /**
     * 상위 commentable(포스트 또는 비디오) 모델을 반환합니다.
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
     * 포스트에 달린 모든 댓글을 반환합니다.
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
     * 비디오에 달린 모든 댓글을 반환합니다.
     */
    public function comments(): MorphMany
    {
        return $this->morphMany(Comment::class, 'commentable');
    }
}
```

<a name="one-to-many-polymorphic-retrieving-the-relationship"></a>
#### 관계 조회하기

데이터베이스 테이블과 모델을 정의했다면, 모델의 동적 관계 프로퍼티를 통해 해당 관계에 접근할 수 있습니다. 예를 들어, 특정 포스트에 달린 모든 댓글을 가져오려면 `comments` 동적 프로퍼티를 사용할 수 있습니다.

```php
use App\Models\Post;

$post = Post::find(1);

foreach ($post->comments as $comment) {
    // ...
}
```

또한, 다형성 자식 모델의 부모(상위) 모델을 조회하려면 `morphTo`를 호출하는 메서드명을 접근하면 됩니다. 이 예제에서는 `Comment` 모델의 `commentable` 메서드를 의미합니다. 따라서 이 메서드를 동적 관계 프로퍼티로 접근해 댓글의 상위 모델을 가져올 수 있습니다.

```php
use App\Models\Comment;

$comment = Comment::find(1);

$commentable = $comment->commentable;
```

`Comment` 모델의 `commentable` 관계는 해당 댓글의 부모가 `Post`인지 `Video`인지에 따라 각각 `Post` 또는 `Video` 인스턴스를 반환합니다.

<a name="polymorphic-automatically-hydrating-parent-models-on-children"></a>
#### 자식 모델에서 자동으로 상위 모델 적재하기

Eloquent의 즉시 로딩(eager loading)을 사용하더라도, 자식 모델을 순회하면서 부모 모델에 접근하면 "N + 1" 쿼리 문제가 발생할 수 있습니다.

```php
$posts = Post::with('comments')->get();

foreach ($posts as $post) {
    foreach ($post->comments as $comment) {
        echo $comment->commentable->title;
    }
}
```

위 예시에서는 각 `Post` 모델별로 댓글은 즉시 로딩했지만, Eloquent는 각 자식 `Comment` 모델의 부모(`Post`)를 자동으로 적재하지 않으므로 N + 1 쿼리가 추가로 발생합니다.

Eloquent에서 댓글의 부모 모델을 자동으로 자식 모델에 직접 적재하고 싶다면, `morphMany` 관계 정의 시 `chaperone` 메서드를 호출할 수 있습니다.

```php
class Post extends Model
{
    /**
     * 포스트에 달린 모든 댓글을 반환합니다.
     */
    public function comments(): MorphMany
    {
        return $this->morphMany(Comment::class, 'commentable')->chaperone();
    }
}
```

혹은, 런타임에서 자동 상위 모델 적재를 선택적으로 사용하고 싶다면, 관계를 즉시 로딩할 때 `chaperone`을 호출하면 됩니다.

```php
use App\Models\Post;

$posts = Post::with([
    'comments' => fn ($comments) => $comments->chaperone(),
])->get();
```

<a name="one-of-many-polymorphic-relations"></a>
### 다형성 One of Many

가끔 한 모델이 여러 관련 모델을 가질 수 있지만, 그 중에서 "가장 최근" 또는 "가장 오래된" 관련 모델을 쉽게 가져오고 싶은 경우가 있습니다. 예를 들어, `User` 모델이 여러 `Image` 모델과 관계가 있지만, 사용자가 마지막으로 업로드한 이미지를 바로 사용할 수 있으면 편리합니다. 이런 경우, `morphOne` 관계 타입을 `ofMany` 메서드와 결합해 사용할 수 있습니다.

```php
/**
 * 사용자의 가장 최근 이미지 반환.
 */
public function latestImage(): MorphOne
{
    return $this->morphOne(Image::class, 'imageable')->latestOfMany();
}
```

마찬가지로, 가장 오래된(혹은 첫 번째) 관련 모델을 위한 메서드도 정의할 수 있습니다.

```php
/**
 * 사용자의 가장 오래된 이미지 반환.
 */
public function oldestImage(): MorphOne
{
    return $this->morphOne(Image::class, 'imageable')->oldestOfMany();
}
```

기본적으로, `latestOfMany`와 `oldestOfMany` 메서드는 모델의 기본 키(정렬 가능한 값 기준)를 사용해 가장 최근 또는 가장 오래된 관련 모델을 조회합니다. 그러나 경우에 따라 더 다양한 정렬 기준으로 하나의 모델을 조회하고 싶을 수 있습니다.

예를 들어, `ofMany` 메서드를 사용해 사용자의 "가장 많이 좋아요를 받은(liked)" 이미지를 가져올 수 있습니다. `ofMany`의 첫 번째 인수엔 정렬할 컬럼명을, 두 번째엔 집계 함수(`min` 또는 `max`)를 전달합니다.

```php
/**
 * 사용자의 가장 인기 있는 이미지 반환.
 */
public function bestImage(): MorphOne
{
    return $this->morphOne(Image::class, 'imageable')->ofMany('likes', 'max');
}
```

> [!NOTE]
> 더 복잡한 형태의 "one of many" 관계도 구성할 수 있습니다. 자세한 내용은 [has one of many 문서](#advanced-has-one-of-many-relationships)를 참고하세요.

<a name="many-to-many-polymorphic-relations"></a>
### 다형성 N:M

<a name="many-to-many-polymorphic-table-structure"></a>
#### 테이블 구조

N:M 다형성 관계는 "morph one"이나 "morph many"보다 조금 더 복잡합니다. 예를 들어, `Post` 모델과 `Video` 모델이 모두 `Tag` 모델과 다형성 관계를 가질 수 있습니다. 이런 관계를 사용하면, 애플리케이션에 포스트나 비디오와 연동 가능한 고유한 태그 목록을 하나의 테이블로 관리할 수 있습니다. 먼저, 이 관계를 만들기 위한 테이블 구조를 살펴봅니다.

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
> 다형성 N:M 관계를 바로 배우기 전에 일반적인 [N:M 관계 문서](#many-to-many)를 먼저 읽는 것이 도움이 될 수 있습니다.

<a name="many-to-many-polymorphic-model-structure"></a>
#### 모델 구조

이제 각 모델에 관계를 정의해봅니다. `Post`와 `Video` 모델은 모두 Eloquent의 `morphToMany` 메서드가 호출되는 `tags` 메서드를 포함해야 합니다.

`morphToMany` 메서드는 관련 모델명, 그리고 "관계 이름"을 인수로 받습니다. 중간 테이블의 이름과 키 명칭을 기준으로 우리는 이 관계의 이름을 "taggable"로 지정할 것입니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphToMany;

class Post extends Model
{
    /**
     * 포스트에 연관된 모든 태그를 반환합니다.
     */
    public function tags(): MorphToMany
    {
        return $this->morphToMany(Tag::class, 'taggable');
    }
}
```

<a name="many-to-many-polymorphic-defining-the-inverse-of-the-relationship"></a>
#### 역방향 관계 정의하기

다음으로, `Tag` 모델에서는 각 부모 모델에 대한 메서드를 각각 정의해야 합니다. 예를 들어, `posts`와 `videos` 메서드를 만들어줍니다. 각각은 `morphedByMany` 메서드를 사용해야 합니다.

`morphedByMany` 메서드는 관계할 모델명과 관계 이름을 인수로 받습니다. 중간 테이블 이름과 키에 따라 이 관계의 이름은 "taggable"로 지정합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphToMany;

class Tag extends Model
{
    /**
     * 이 태그가 지정된 모든 포스트 반환.
     */
    public function posts(): MorphToMany
    {
        return $this->morphedByMany(Post::class, 'taggable');
    }

    /**
     * 이 태그가 지정된 모든 비디오 반환.
     */
    public function videos(): MorphToMany
    {
        return $this->morphedByMany(Video::class, 'taggable');
    }
}
```

<a name="many-to-many-polymorphic-retrieving-the-relationship"></a>
#### 관계 조회하기

테이블 및 모델 정의가 끝났다면, 해당 관계에 접근할 수 있습니다. 예를 들어, 특정 포스트에 연결된 모든 태그를 조회하려면 `tags` 동적 관계 프로퍼티를 사용하면 됩니다.

```php
use App\Models\Post;

$post = Post::find(1);

foreach ($post->tags as $tag) {
    // ...
}
```

다형성 관계에서 자식 모델의 부모를 조회하려면, `morphedByMany`를 호출하는 메서드명을 접근하면 됩니다. 이 경우 `Tag` 모델의 `posts` 또는 `videos` 메서드를 사용하게 됩니다.

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
### 커스텀 다형성 타입

기본적으로, 라라벨은 연관 모델의 "type" 값을 저장할 때 전체 네임스페이스가 포함된 클래스명을 사용합니다. 예를 들어, 위에서 설명한 1:N 다형성 관계(`Comment`가 `Post` 또는 `Video`에 속하는 경우)에서, 기본적으로 `commentable_type` 컬럼은 각각 `App\Models\Post` 또는 `App\Models\Video` 값을 갖게 됩니다. 그러나, 때로는 이 값들이 애플리케이션의 내부 구조에서 분리되어 있기를 원할 수 있습니다.

예를 들어, 모델명을 그대로 사용하는 대신 `'post'`, `'video'`와 같은 단순한 문자열로 "type"을 저장할 수도 있습니다. 이렇게 하면, 모델명이 바뀌더라도 데이터베이스에 남아 있는 다형성 "type" 컬럼 값은 여전히 유효합니다.

```php
use Illuminate\Database\Eloquent\Relations\Relation;

Relation::enforceMorphMap([
    'post' => 'App\Models\Post',
    'video' => 'App\Models\Video',
]);
```

`enforceMorphMap` 메서드는 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출하거나, 별도의 서비스 프로바이더를 만들어 사용할 수도 있습니다.

런타임 시, 모델의 `getMorphClass` 메서드를 통해 해당 모델의 morph 별칭 값을 확인할 수 있습니다. 반대로, 특정 morph 별칭에 연결된 전체 클래스명을 알아내려면 `Relation::getMorphedModel` 메서드를 사용합니다.

```php
use Illuminate\Database\Eloquent\Relations\Relation;

$alias = $post->getMorphClass();

$class = Relation::getMorphedModel($alias);
```

> [!WARNING]
> 기존 애플리케이션에 "morph map"을 추가하는 경우, 데이터베이스에 남아 있는 모든 morphable `*_type` 컬럼 값(네임스페이스까지 포함된 클래스명으로 저장된 값)은 새로 지정한 "맵" 이름으로 변환해주어야 합니다.

<a name="dynamic-relationships"></a>
### 동적 관계(Dynamic Relationships)

`resolveRelationUsing` 메서드를 사용하면 런타임에 Eloquent 모델 간의 관계를 정의할 수 있습니다. 일반적인 애플리케이션 개발에서는 자주 사용하지 않지만, 라라벨 패키지 개발 등에서는 유용하게 활용될 수 있습니다.

`resolveRelationUsing` 메서드는 첫 번째 인수로 관계명을, 두 번째 인수로는 모델 인스턴스를 받아 Eloquent 관계 정의를 반환하는 클로저를 받습니다. 동적 관계는 보통 [서비스 프로바이더](/docs/12.x/providers)의 boot 메서드 내에서 설정하는 것이 일반적입니다.

```php
use App\Models\Order;
use App\Models\Customer;

Order::resolveRelationUsing('customer', function (Order $orderModel) {
    return $orderModel->belongsTo(Customer::class, 'customer_id');
});
```

> [!WARNING]
> 동적 관계를 정의할 때는 항상 Eloquent 관계 메서드에 명시적으로 키 이름 인수를 넘겨주어야 합니다.

<a name="querying-relations"></a>
## 관계 쿼리(Querying Relations)

모든 Eloquent 관계는 메서드로 정의되어 있으므로, 해당 메서드를 호출하면 실제로 관련 모델을 쿼리하지 않고도 관계 인스턴스를 가져올 수 있습니다. 또한, 모든 종류의 Eloquent 관계는 [쿼리 빌더](/docs/12.x/queries) 역할도 하므로, 실제 SQL 쿼리를 실행하기 전 원하는 만큼 조건을 체이닝할 수 있습니다.

예를 들어, 블로그 애플리케이션에서 특정 `User` 모델이 여러 `Post` 모델과 관계가 있는 경우를 생각해 봅시다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class User extends Model
{
    /**
     * 유저가 작성한 모든 포스트를 반환합니다.
     */
    public function posts(): HasMany
    {
        return $this->hasMany(Post::class);
    }
}
```

`posts` 관계에 쿼리를 추가해 조건을 붙여 사용할 수 있습니다.

```php
use App\Models\User;

$user = User::find(1);

$user->posts()->where('active', 1)->get();
```

관계 위에서 라라벨 [쿼리 빌더](/docs/12.x/queries)의 모든 메서드를 사용할 수 있습니다. 자세한 내용은 쿼리 빌더 문서를 참고하세요.

<a name="chaining-orwhere-clauses-after-relationships"></a>
#### 관계 쿼리에서 `orWhere` 체이닝 주의

위와 같이 관계에 조건을 추가할 수 있지만, `orWhere` 절을 체이닝할 때는 주의해야 합니다. `orWhere` 절은 관계 조건과 논리적으로 같은 수준에서 그룹화되기 때문입니다.

```php
$user->posts()
    ->where('active', 1)
    ->orWhere('votes', '>=', 100)
    ->get();
```

위 예시에서는 다음과 같은 SQL이 생성됩니다. 여기서 `or` 절 때문에 100표 이상 받은 모든 포스트가 _모두_ 반환되며, 더 이상 특정 유저에만 한정되지 않습니다.

```sql
select *
from posts
where user_id = ? and active = 1 or votes >= 100
```

대부분의 상황에서는 [논리 그룹핑](/docs/12.x/queries#logical-grouping)을 사용해 조건을 괄호로 묶는 것이 좋습니다.

```php
use Illuminate\Database\Eloquent\Builder;

$user->posts()
    ->where(function (Builder $query) {
        return $query->where('active', 1)
            ->orWhere('votes', '>=', 100);
    })
    ->get();
```

위 코드는 아래와 같이 쿼리가 생성되며, 논리 그룹핑을 통해 조건이 올바르게 묶이고 쿼리가 특정 유저로 제한됩니다.

```sql
select *
from posts
where user_id = ? and (active = 1 or votes >= 100)
```

<a name="relationship-methods-vs-dynamic-properties"></a>
### 관계 메서드와 동적 프로퍼티의 차이

Eloquent 관계 쿼리에 추가 조건이 필요 없다면, 관계를 마치 프로퍼티처럼 접근할 수 있습니다. 예를 들어, 위에서 정의한 `User`와 `Post` 모델을 활용해 유저의 모든 포스트를 다음과 같이 가져올 수 있습니다.

```php
use App\Models\User;

$user = User::find(1);

foreach ($user->posts as $post) {
    // ...
}
```

동적 관계 프로퍼티는 "지연 로딩(lazy loading)" 방식으로 동작합니다. 즉, 실제로 프로퍼티에 접근할 때 쿼리가 실행되어 관계 데이터를 불러옵니다. 때문에, 실제로 모델의 관계를 접근할 계획이 있다면 [즉시 로딩(eager loading)](#eager-loading)을 사용해 미리 관계를 불러오고 사용하는 것이 성능상 유리합니다.

<a name="querying-relationship-existence"></a>
### 관계 존재 여부 쿼리

모델 레코드를 조회할 때, 특정 관계가 존재하는지 여부에 따라 결과를 제한하고 싶을 수 있습니다. 예를 들어, "최소 1개의 댓글을 가진 모든 블로그 포스트"를 조회하려면 관계명을 `has` 또는 `orHas` 메서드에 전달하면 됩니다.

```php
use App\Models\Post;

// 댓글이 하나 이상 있는 모든 포스트 가져오기...
$posts = Post::has('comments')->get();
```

연산자와 카운트 값을 추가로 지정해 쿼리를 원하는 대로 조정할 수도 있습니다.

```php
// 댓글이 3개 이상 있는 모든 포스트 가져오기...
$posts = Post::has('comments', '>=', 3)->get();
```

중첩된 `has` 조건은 "점(dot) 표기법"을 사용해 구성할 수 있습니다. 예를 들어, 댓글 중 하나 이상 이미지가 첨부된 포스트만 조회할 수도 있습니다.

```php
// 이미지가 달린 댓글이 하나 이상 있는 포스트만 가져오기...
$posts = Post::has('comments.images')->get();
```

더 강력한 조건이 필요하다면, `whereHas` 또는 `orWhereHas` 메서드에 쿼리 조건을 추가해 더욱 정교하게 다룰 수 있습니다. 예를 들어, 댓글의 내용에 따라 쿼리하는 식입니다.

```php
use Illuminate\Database\Eloquent\Builder;

// 'code%'로 시작하는 내용이 포함된 댓글이 하나 이상 있는 포스트만 가져오기...
$posts = Post::whereHas('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
})->get();

// 'code%'로 시작하는 내용이 포함된 댓글이 10개 이상인 포스트만 가져오기...
$posts = Post::whereHas('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
}, '>=', 10)->get();
```

> [!WARNING]
> Eloquent는 현재 관계 존재 여부 쿼리에 대해 데이터베이스를跨越(cross-database, 데이터베이스 간)으로 지원하지 않습니다. 관계는 반드시 같은 데이터베이스에 있어야 합니다.

<a name="many-to-many-relationship-existence-queries"></a>
#### 다대다(N:M) 관계 존재 쿼리

`whereAttachedTo` 메서드를 사용하면, 다대다 관계에서 특정 모델 혹은 모델 컬렉션에 연결된 레코드만 간편하게 쿼리할 수 있습니다.

```php
$users = User::whereAttachedTo($role)->get();
```

뿐만 아니라, [컬렉션](/docs/12.x/eloquent-collections) 인스턴스를 인수로 넘길 수도 있습니다. 이 경우 컬렉션 내 어떤 모델과 연결된 레코드도 모두 조회합니다.

```php
$tags = Tag::whereLike('name', '%laravel%')->get();

$posts = Post::whereAttachedTo($tags)->get();
```

<a name="inline-relationship-existence-queries"></a>
#### 인라인 관계 존재 쿼리

단일하고 간단한 where 조건에 기반해 관계의 존재 여부를 쿼리하고 싶다면, `whereRelation`, `orWhereRelation`, `whereMorphRelation`, `orWhereMorphRelation` 메서드가 더 편리할 수 있습니다. 예를 들어, 승인되지 않은 댓글이 있는 모든 포스트를 조회하려면 아래와 같이 사용할 수 있습니다.

```php
use App\Models\Post;

$posts = Post::whereRelation('comments', 'is_approved', false)->get();
```

물론, 쿼리 빌더의 `where` 메서드처럼 연산자를 직접 지정할 수도 있습니다.

```php
$posts = Post::whereRelation(
    'comments', 'created_at', '>=', now()->subHour()
)->get();
```

<a name="querying-relationship-absence"></a>
### 관계 부재 여부 쿼리

모델 레코드를 조회할 때, 특정 관계가 **존재하지 않는** 경우만 결과를 제한하고 싶을 수 있습니다. 예를 들어, "댓글이 하나도 없는 블로그 포스트"만 조회하려면, 관계명을 `doesntHave` 혹은 `orDoesntHave` 메서드에 전달하면 됩니다.

```php
use App\Models\Post;

$posts = Post::doesntHave('comments')->get();
```

더 정교하게 추가 조건을 붙이고 싶다면, `whereDoesntHave` 또는 `orWhereDoesntHave`에 쿼리를 추가할 수 있습니다. 예를 들어, 댓글의 내용에 따라 쿼리하는 경우입니다.

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::whereDoesntHave('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
})->get();
```

"점(dot) 표기법"을 사용하면 중첩 관계에도 쿼리를 실행할 수 있습니다. 예를 들어, 아래 쿼리는 댓글이 아예 없는 포스트와, 댓글이 있더라도 **모든** 댓글이 정지된(banned) 사용자로부터 작성된 것이 아닌 포스트만 조회합니다.

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::whereDoesntHave('comments.author', function (Builder $query) {
    $query->where('banned', 1);
})->get();
```

<a name="querying-morph-to-relationships"></a>

### Morph To 관계 쿼리하기

"morph to" 관계의 존재를 쿼리하려면 `whereHasMorph` 및 `whereDoesntHaveMorph` 메서드를 사용할 수 있습니다. 이 메서드들은 첫 번째 인수로 관계의 이름을 받습니다. 두 번째로, 쿼리에 포함할 관련 모델의 이름(들)을 인수로 받습니다. 마지막으로, 관계 쿼리를 사용자 정의할 수 있는 클로저를 전달할 수 있습니다.

```php
use App\Models\Comment;
use App\Models\Post;
use App\Models\Video;
use Illuminate\Database\Eloquent\Builder;

// 제목이 code%로 시작하는 post 또는 video에 연결된 comment 조회...
$comments = Comment::whereHasMorph(
    'commentable',
    [Post::class, Video::class],
    function (Builder $query) {
        $query->where('title', 'like', 'code%');
    }
)->get();

// 제목이 code%로 시작하지 않는 post에 연결된 comment 조회...
$comments = Comment::whereDoesntHaveMorph(
    'commentable',
    Post::class,
    function (Builder $query) {
        $query->where('title', 'like', 'code%');
    }
)->get();
```

때때로, 관련 다형성 모델의 "type"에 따라 쿼리 제한 조건을 추가해야 할 수 있습니다. 이때, `whereHasMorph` 메서드에 전달하는 클로저는 두 번째 인수로 `$type` 값을 받을 수 있습니다. 이 인수를 통해 현재 빌드되는 쿼리의 "type"을 확인할 수 있습니다.

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

어떤 경우에는 "morph to" 관계의 부모와 연결된 자식 레코드를 쿼리하고 싶을 수 있습니다. 이럴 때는 `whereMorphedTo`와 `whereNotMorphedTo` 메서드를 사용할 수 있으며, 이 메서드들은 지정한 모델에 대해 적절한 morph type 매핑을 자동으로 결정합니다. 첫 번째 인수로 `morphTo` 관계 이름을, 두 번째 인수로 해당 부모 모델을 전달하면 됩니다.

```php
$comments = Comment::whereMorphedTo('commentable', $post)
    ->orWhereMorphedTo('commentable', $video)
    ->get();
```

<a name="querying-all-morph-to-related-models"></a>
#### 모든 관련 모델 쿼리하기

다형성 모델의 배열을 전달하는 대신, 와일드카드 값인 `*`를 사용할 수 있습니다. 이 경우, 라라벨은 데이터베이스에서 가능한 모든 다형성 타입을 조회합니다. 이 작업을 위해 추가 쿼리가 실행됩니다.

```php
use Illuminate\Database\Eloquent\Builder;

$comments = Comment::whereHasMorph('commentable', '*', function (Builder $query) {
    $query->where('title', 'like', 'foo%');
})->get();
```

<a name="aggregating-related-models"></a>
## 관련 모델 집계하기

<a name="counting-related-models"></a>
### 관련 모델 개수 세기

특정 관계에 대해 실제로 모델을 불러오지 않고도 관련 모델의 개수만 세고 싶을 수 있습니다. 이럴 때는 `withCount` 메서드를 사용하면 됩니다. `withCount` 메서드는 결과 모델에 `{relation}_count` 속성을 추가합니다.

```php
use App\Models\Post;

$posts = Post::withCount('comments')->get();

foreach ($posts as $post) {
    echo $post->comments_count;
}
```

`withCount` 메서드에 배열을 전달하면, 여러 관계의 개수를 추가하거나 쿼리에 추가 제한 조건을 걸 수도 있습니다.

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::withCount(['votes', 'comments' => function (Builder $query) {
    $query->where('content', 'like', 'code%');
}])->get();

echo $posts[0]->votes_count;
echo $posts[0]->comments_count;
```

관계 개수 결과에 별칭(alias)을 지정할 수도 있으며, 이를 통해 동일한 관계에 대해 여러 개의 카운트를 사용할 수 있습니다.

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
#### 지연 카운트 로딩(Deferred Count Loading)

`loadCount` 메서드를 사용하면, 부모 모델을 이미 조회한 이후에 관계의 개수를 로드할 수 있습니다.

```php
$book = Book::first();

$book->loadCount('genres');
```

카운트 쿼리에 추가적인 제한 조건이 필요하다면, 카운트할 관계를 키로 하는 배열을 전달할 수 있습니다. 배열 값으로는 쿼리 빌더 인스턴스를 받는 클로저를 전달합니다.

```php
$book->loadCount(['reviews' => function (Builder $query) {
    $query->where('rating', 5);
}])
```

<a name="relationship-counting-and-custom-select-statements"></a>
#### 관계 개수와 커스텀 select 문

`withCount`를 `select` 문과 함께 사용할 경우, 반드시 `select` 이후에 `withCount`를 호출해야 합니다.

```php
$posts = Post::select(['title', 'body'])
    ->withCount('comments')
    ->get();
```

<a name="other-aggregate-functions"></a>
### 기타 집계 함수

`withCount` 메서드 외에도 Eloquent는 `withMin`, `withMax`, `withAvg`, `withSum`, `withExists` 등의 메서드를 제공합니다. 이 메서드들을 사용하면 결과 모델에 `{relation}_{function}_{column}` 형식의 속성이 추가됩니다.

```php
use App\Models\Post;

$posts = Post::withSum('comments', 'votes')->get();

foreach ($posts as $post) {
    echo $post->comments_sum_votes;
}
```

집계 함수 결과에 별칭(alias)을 지정하고 싶다면 직접 이름을 지정할 수도 있습니다.

```php
$posts = Post::withSum('comments as total_comments', 'votes')->get();

foreach ($posts as $post) {
    echo $post->total_comments;
}
```

`loadCount`처럼, 이미 조회한 Eloquent 모델에서 이런 집계 연산을 나중에 수행할 수 있는 지연(Deferred) 버전의 메서드도 있습니다.

```php
$post = Post::first();

$post->loadSum('comments', 'votes');
```

이러한 집계 메서드를 `select`와 함께 사용할 경우, 반드시 `select` 이후에 집계 메서드를 호출해야 합니다.

```php
$posts = Post::select(['title', 'body'])
    ->withExists('comments')
    ->get();
```

<a name="counting-related-models-on-morph-to-relationships"></a>
### Morph To 관계에서 관련 모델 개수 세기

"morph to" 관계와 함께, 해당 관계에 의해 반환될 수 있는 다양한 엔티티들의 관련 모델 카운트까지 Eager Load(즉시 로드)하고 싶다면, `with` 메서드와 `morphTo` 관계의 `morphWithCount` 메서드를 조합하여 사용할 수 있습니다.

예를 들어, `Photo` 모델과 `Post` 모델이 각각 `ActivityFeed` 모델을 생성한다고 가정해 봅시다. 그리고 `ActivityFeed` 모델은 `parentable`이라는 "morph to" 관계를 정의해서, 각 `ActivityFeed` 인스턴스의 상위 `Photo` 또는 `Post` 모델을 조회할 수 있다고 가정합니다. 또, `Photo` 모델은 여러 개의 `Tag` 모델을, `Post` 모델은 여러 개의 `Comment` 모델을 가집니다.

이런 상황에서 `ActivityFeed` 인스턴스를 조회하고, 각각의 `ActivityFeed` 인스턴스에 대해 상위(parentable) 모델을 Eager Load(즉시 로드)하면서, 각각의 상위 photo에 연결된 tag 개수, 상위 post에 연결된 comment 개수를 함께 가져올 수 있습니다.

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
#### 지연된 Morph To 관계 카운트 로딩

이미 `ActivityFeed` 모델 집합을 조회한 상황에서, 각 activity feeds가 연결된 여러 `parentable` 모델의 중첩 관계 카운트까지 불러오고 싶을 때는 `loadMorphCount` 메서드를 사용할 수 있습니다.

```php
$activities = ActivityFeed::with('parentable')->get();

$activities->loadMorphCount('parentable', [
    Photo::class => ['tags'],
    Post::class => ['comments'],
]);
```

<a name="eager-loading"></a>
## 즉시 로딩(Eager Loading)

Eloquent 관계를 속성처럼 접근하면, 연관된 모델이 "지연 로딩(lazy loaded)" 됩니다. 즉, 관계 데이터는 해당 속성에 처음 접근할 때 비로소 로딩됩니다. 하지만 Eloquent에서는 부모 모델을 쿼리할 때 관계를 "즉시 로딩(eager load)" 할 수도 있습니다. 즉시 로딩을 사용하면 "N + 1 쿼리 문제"를 해결할 수 있습니다.  

N + 1 쿼리 문제를 예로 들어 설명해 보겠습니다. `Book` 모델이 `Author` 모델에 "belongs to" 관계를 가진다고 가정합시다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Book extends Model
{
    /**
     * 책을 쓴 author를 반환합니다.
     */
    public function author(): BelongsTo
    {
        return $this->belongsTo(Author::class);
    }
}
```

이제 모든 book과 그 author를 조회한다고 해봅시다:

```php
use App\Models\Book;

$books = Book::all();

foreach ($books as $book) {
    echo $book->author->name;
}
```

이 반복문은 데이터베이스 테이블에서 모든 책을 가져오기 위한 쿼리 한 번, 그리고 각 책마다 저자를 조회하기 위한 쿼리가 각각 실행됩니다. 만약 책이 25권 있다면, 위 코드는 총 26개의 쿼리를 실행하게 됩니다(책 전체 1번 + 각 책마다 author 쿼리 25번).

다행히도, 즉시 로딩을 사용하면 이 작업을 단 2번의 쿼리만으로 처리할 수 있습니다. 쿼리를 빌드할 때, 어느 관계를 즉시 로딩할지 `with` 메서드로 지정할 수 있습니다.

```php
$books = Book::with('author')->get();

foreach ($books as $book) {
    echo $book->author->name;
}
```

위의 코드는, 전체 책을 한 번 조회하고, 그 책들의 author만을 한 번에 조회하므로 총 2개의 쿼리만 실행됩니다.

```sql
select * from books

select * from authors where id in (1, 2, 3, 4, 5, ...)
```

<a name="eager-loading-multiple-relationships"></a>
#### 여러 관계 즉시 로딩

여러 개의 관계를 한 번에 즉시 로딩하고 싶을 때는, `with` 메서드에 관계 배열을 전달하면 됩니다.

```php
$books = Book::with(['author', 'publisher'])->get();
```

<a name="nested-eager-loading"></a>
#### 중첩된 관계 즉시 로딩

관계의 관계까지 즉시 로딩하려면 "점(.) 표기법"을 사용할 수 있습니다. 예를 들어, 모든 book의 author와 그 author의 연락처(contact)까지 모두 즉시 로딩하는 방법은 다음과 같습니다.

```php
$books = Book::with('author.contacts')->get();
```

또는, 여러 중첩 관계를 즉시 로딩하려면 `with` 메서드에 중첩 배열을 이용할 수도 있습니다.

```php
$books = Book::with([
    'author' => [
        'contacts',
        'publisher',
    ],
])->get();
```

<a name="nested-eager-loading-morphto-relationships"></a>
#### `morphTo` 관계의 중첩 즉시 로딩

`morphTo` 관계를 즉시 로딩하면서, 해당 관계로 반환될 수 있는 다양한 엔티티의 중첩 관계까지 같이 즉시 로딩하고 싶을 수 있습니다. 이럴 때는 `with` 메서드와 `morphTo` 관계의 `morphWith` 메서드를 조합하여 사용할 수 있습니다.  
예를 들어, 아래 모델을 참고하세요.

```php
<?php

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class ActivityFeed extends Model
{
    /**
     * activity feed의 상위(parent) 레코드를 반환합니다.
     */
    public function parentable(): MorphTo
    {
        return $this->morphTo();
    }
}
```

여기서 `Event`, `Photo`, `Post` 모델이 각각 `ActivityFeed` 모델을 생성할 수 있다고 가정합니다. 또한, `Event`는 `Calendar`에 연결되고, `Photo`는 `Tag`와 관계를 맺으며, `Post`는 `Author`와 관계를 맺는다고 가정합니다.

이 모델 정의 및 관계를 활용하면, `ActivityFeed` 인스턴스를 조회하여 각 `parentable` 모델 및 그 중첩 관계까지 즉시 로딩할 수 있습니다.

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
#### 특정 컬럼만 즉시 로딩하기

관계에서 모든 컬럼이 필요한 것은 아닐 수 있습니다. 그래서 Eloquent는 관계에서 원하는 컬럼만 선택적으로 가져올 수 있도록 지원합니다.

```php
$books = Book::with('author:id,name,book_id')->get();
```

> [!WARNING]
> 이 기능을 사용할 때는 반드시 `id` 컬럼과 관련된 외래 키 컬럼을 컬럼 목록에 포함해야 합니다.

<a name="eager-loading-by-default"></a>
#### 기본적으로 즉시 로딩하기

어떤 모델을 조회할 때마다 항상 일부 관계를 즉시 로딩하고 싶다면, 해당 모델에 `$with` 프로퍼티를 정의하면 됩니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Book extends Model
{
    /**
     * 항상 즉시 로딩할 관계 목록.
     *
     * @var array
     */
    protected $with = ['author'];

    /**
     * 책을 쓴 author를 반환합니다.
     */
    public function author(): BelongsTo
    {
        return $this->belongsTo(Author::class);
    }

    /**
     * 책의 장르를 반환합니다.
     */
    public function genre(): BelongsTo
    {
        return $this->belongsTo(Genre::class);
    }
}
```

특정 쿼리에서만 `$with` 프로퍼티의 항목을 제거하고 싶다면, `without` 메서드를 사용할 수 있습니다.

```php
$books = Book::without('author')->get();
```

단일 쿼리에서 `$with` 프로퍼티의 모든 항목을 덮어쓰고 싶다면, `withOnly` 메서드를 사용하세요.

```php
$books = Book::withOnly('genre')->get();
```

<a name="constraining-eager-loads"></a>
### 즉시 로딩 쿼리 제한 조건 지정

관계를 즉시 로딩할 때, eager loading 쿼리에 추가적인 조건을 지정하고 싶을 때가 있습니다. 이 경우, `with` 메서드에 관계 이름을 키로 하고, 해당 쿼리를 제한할 클로저를 값으로 삼는 배열을 전달하면 됩니다.

```php
use App\Models\User;
use Illuminate\Contracts\Database\Eloquent\Builder;

$users = User::with(['posts' => function (Builder $query) {
    $query->where('title', 'like', '%code%');
}])->get();
```

위 예시에서는, post의 `title` 컬럼에 `code`가 포함된 경우에만 post를 즉시 로딩합니다. 이외에도 [쿼리 빌더](/docs/12.x/queries)의 다양한 메서드를 조합해 즉시 로딩을 더욱 세밀하게 조정할 수 있습니다.

```php
$users = User::with(['posts' => function (Builder $query) {
    $query->orderBy('created_at', 'desc');
}])->get();
```

<a name="constraining-eager-loading-of-morph-to-relationships"></a>
#### `morphTo` 관계의 즉시 로딩 쿼리 제한

`morphTo` 관계를 즉시 로딩하면, Eloquent가 각 타입별로 관련 모델을 가져오기 위해 여러 쿼리를 실행합니다. `MorphTo` 관계의 `constrain` 메서드를 이용하면 각 쿼리에 추가 조건을 지정할 수 있습니다.

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

이 예시에서는, 숨겨지지 않은 post와 type이 "educational"인 video만 즉시 로딩합니다.

<a name="constraining-eager-loads-with-relationship-existence"></a>
#### 관계 존재 유무로 즉시 로딩 제한

관계를 즉시 로딩하면서 동시에, 해당 조건을 만족하는 자식 관계가 존재하는 모델만 조회하고 싶을 때도 있습니다. 예를 들어, 특정 쿼리 조건을 만족하는 child `Post` 모델이 있는 `User` 모델만 가져오면서, 동일 조건의 post를 즉시 로딩하고 싶다면, `withWhereHas` 메서드를 사용하면 됩니다.

```php
use App\Models\User;

$users = User::withWhereHas('posts', function ($query) {
    $query->where('featured', true);
})->get();
```

<a name="lazy-eager-loading"></a>
### 지연(Eager) 로딩(Lazy Eager Loading)

경우에 따라, 부모 모델을 이미 조회한 뒤에 관계를 즉시 로딩하고 싶을 때가 있습니다. 예를 들어, 어느 관계를 로드할지 동적으로 결정하고 싶을 때 유용합니다.

```php
use App\Models\Book;

$books = Book::all();

if ($someCondition) {
    $books->load('author', 'publisher');
}
```

즉시 로딩 쿼리에 추가 제한 조건이 필요하다면, 로드할 관계를 키로 하는 배열의 값을 클로저로 전달할 수 있습니다. 이 클로저는 쿼리 인스턴스를 인자로 받습니다.

```php
$author->load(['books' => function (Builder $query) {
    $query->orderBy('published_date', 'asc');
}]);
```

관계가 아직 로드되지 않은 경우에만 로드하고 싶을 때는 `loadMissing` 메서드를 사용합니다.

```php
$book->loadMissing('author');
```

<a name="nested-lazy-eager-loading-morphto"></a>
#### 중첩된 Lazy Eager Loading 및 `morphTo`

`morphTo` 관계와 각각에 대해 반환될 수 있는 다양한 엔티티의 중첩 관계까지 Lazy Eager Loading하고 싶다면 `loadMorph` 메서드를 사용하세요.

이 메서드는 첫 번째 인수로 `morphTo` 관계 이름을 받고, 두 번째 인수로 모델/관계 쌍의 배열을 받습니다. 예시 모델은 다음과 같습니다.

```php
<?php

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class ActivityFeed extends Model
{
    /**
     * activity feed의 상위 레코드를 반환합니다.
     */
    public function parentable(): MorphTo
    {
        return $this->morphTo();
    }
}
```

여기서 `Event`, `Photo`, `Post` 모델이 각각 `ActivityFeed` 모델을 만들 수 있고, 각 모델과 다양한 관계(`Calendar`, `Tag`, `Author`)가 있다고 가정합니다.  
이 구조를 바탕으로, 이미 조회된 `ActivityFeed` 인스턴스의 각 parentable 모델에 대해 각각의 중첩 관계를 Lazy Eager Loading할 수 있습니다.

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
### 자동 Eager Loading

> [!WARNING]
> 이 기능은 현재 커뮤니티 피드백을 받기 위해 베타 단계에 있습니다. 패치 릴리스에서도 동작이나 기능이 변경될 수 있습니다.

많은 경우, 라라벨은 여러분이 접근하는 관계를 자동으로 eager load할 수 있습니다. 자동 eager loading을 활성화하려면, 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 `Model::automaticallyEagerLoadRelationships` 메서드를 호출해야 합니다.

```php
use Illuminate\Database\Eloquent\Model;

/**
 * 애플리케이션 서비스를 부트스트랩합니다.
 */
public function boot(): void
{
    Model::automaticallyEagerLoadRelationships();
}
```

이 기능이 활성화된 상태에서는, 아직 로드되지 않은 관계에 접근하면, 라라벨이 해당 관계를 자동으로 eager load합니다. 예를 들어, 다음과 같은 코드를 생각해 봅시다.

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

일반적으로 위 코드는 각 user의 posts를 조회하기 위한 쿼리와, 각 post의 comments를 조회하기 위한 쿼리를 각각 실행합니다. 하지만 자동 eager loading이 활성화된 경우, users 컬렉션에서 한 명의 user가 post에 접근하는 순간, 조회된 user 모두의 post가 [lazy eager loading](#lazy-eager-loading) 방식으로 불러와집니다. 마찬가지로, 어떤 post의 comments에 접근하면 모든 post의 comments가 한 번에 lazy eager loaded됩니다.

자동 eager loading을 전역적으로 사용하고 싶지 않다면, Eloquent 컬렉션 인스턴스에서만 이 기능을 사용할 수도 있습니다. 컬렉션에서 `withRelationshipAutoloading` 메서드를 호출하면 됩니다.

```php
$users = User::where('vip', true)->get();

return $users->withRelationshipAutoloading();
```

<a name="preventing-lazy-loading"></a>

### 지연 로딩(Lazy Loading) 방지하기

앞에서 설명한 것처럼, 리レー션을 즉시 로드(eager loading)하면 애플리케이션의 성능이 크게 향상될 수 있습니다. 따라서 필요하다면 관계의 지연 로딩을 아예 막도록 라라벨에 지시할 수도 있습니다. 이를 위해, 기본 Eloquent 모델 클래스에서 제공하는 `preventLazyLoading` 메서드를 사용할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `AppServiceProvider` 클래스에 있는 `boot` 메서드 내부에서 호출하는 것이 좋습니다.

`preventLazyLoading` 메서드는 지연 로딩을 차단할지 여부를 나타내는 불리언 값을 인수로 받습니다. 예를 들어, 운영 환경이 아닌 개발 환경 등에서만 지연 로딩을 차단하고, 실수로 운영 코드에 지연 로딩이 남아 있어도 운영 환경에서는 영향이 없도록 할 수 있습니다.

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

이렇게 지연 로딩을 차단한 후 애플리케이션에서 Eloquent 관계를 지연 로딩하려고 시도하면, Eloquent는 `Illuminate\Database\LazyLoadingViolationException` 예외를 발생시킵니다.

또한, `handleLazyLoadingViolationsUsing` 메서드를 사용해 지연 로딩 위반 시의 동작을 직접 정의할 수 있습니다. 예를 들어, 예외를 발생시키지 않고 로그에만 남기도록 처리할 수 있습니다.

```php
Model::handleLazyLoadingViolationUsing(function (Model $model, string $relation) {
    $class = $model::class;

    info("Attempted to lazy load [{$relation}] on model [{$class}].");
});
```

<a name="inserting-and-updating-related-models"></a>
## 관련 모델 삽입 및 업데이트

<a name="the-save-method"></a>
### `save` 메서드

Eloquent는 리レー션에 새 모델을 더 쉽게 추가할 수 있는 편리한 메서드를 제공합니다. 예를 들어, 특정 게시글(Post)에 새로운 댓글(Comment)을 추가하려고 할 때, `Comment` 모델의 `post_id` 속성(attribute)을 직접 설정하지 않고, 관계의 `save` 메서드를 통해 댓글을 추가할 수 있습니다.

```php
use App\Models\Comment;
use App\Models\Post;

$comment = new Comment(['message' => 'A new comment.']);

$post = Post::find(1);

$post->comments()->save($comment);
```

여기서 주의할 점은, `comments` 관계를 동적 속성(프로퍼티)처럼 접근하지 않고, 직접 `comments()` 메서드를 호출하여 관계 인스턴스를 얻은 뒤 `save`를 사용했다는 것입니다. 이렇게 하면 `save` 메서드가 자동으로 새 `Comment` 모델의 `post_id` 값에 올바른 값을 설정해 저장합니다.

여러 개의 관련 모델을 한 번에 저장하려면 `saveMany` 메서드를 사용할 수 있습니다.

```php
$post = Post::find(1);

$post->comments()->saveMany([
    new Comment(['message' => 'A new comment.']),
    new Comment(['message' => 'Another new comment.']),
]);
```

`save` 및 `saveMany` 메서드는 전달받은 모델 인스턴스를 실제로 데이터베이스에 저장하지만, 부모 모델에 이미 메모리 상으로 로드된 관련 모델 컬렉션에는 새로 저장한 모델이 자동으로 추가되지는 않습니다. 만약 `save` 또는 `saveMany` 호출 직후에 관계를 접근해야 한다면 `refresh` 메서드로 모델과 리レー션을 다시 불러오는 것이 좋습니다.

```php
$post->comments()->save($comment);

$post->refresh();

// 새로 저장된 댓글을 포함한 모든 댓글 목록...
$post->comments;
```

<a name="the-push-method"></a>
#### 모델 및 관계를 재귀적으로 저장하기

모델 자체뿐 아니라 연결된 모든 관련 모델까지 한 번에 저장하고 싶다면 `push` 메서드를 사용할 수 있습니다. 아래 예제에서는 `Post` 모델뿐 아니라, 그 하위 comments, 그리고 각 comment의 author까지 모두 저장됩니다.

```php
$post = Post::find(1);

$post->comments[0]->message = 'Message';
$post->comments[0]->author->name = 'Author Name';

$post->push();
```

이와 유사하게, 이벤트를 발생시키지 않고 모델과 관련 관계를 저장하려면 `pushQuietly` 메서드를 사용할 수 있습니다.

```php
$post->pushQuietly();
```

<a name="the-create-method"></a>
### `create` 메서드

`save` 및 `saveMany`와 더불어, 리レー션에 새 모델을 추가할 때 `create` 메서드도 사용할 수 있습니다. `create`는 속성 배열을 받아 모델을 생성하고 바로 데이터베이스에 저장합니다. `save`는 Eloquent 모델 인스턴스를 받지만, `create`는 일반 PHP 배열을 받는다는 점이 다릅니다. `create`를 호출하면 생성된 새 모델 인스턴스를 반환합니다.

```php
use App\Models\Post;

$post = Post::find(1);

$comment = $post->comments()->create([
    'message' => 'A new comment.',
]);
```

여러 개의 관련 모델을 생성하려면 `createMany`를 사용할 수 있습니다.

```php
$post = Post::find(1);

$post->comments()->createMany([
    ['message' => 'A new comment.'],
    ['message' => 'Another new comment.'],
]);
```

이벤트를 발생시키지 않고 모델을 생성하려면 `createQuietly`와 `createManyQuietly` 메서드를 사용할 수 있습니다.

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

또한 관계에 대해 `findOrNew`, `firstOrNew`, `firstOrCreate`, `updateOrCreate` 메서드를 사용해 [모델을 생성·업데이트](/docs/12.x/eloquent#upserts)할 수도 있습니다.

> [!NOTE]
> `create` 메서드를 사용하기 전에 [대량 할당(Mass Assignment)](/docs/12.x/eloquent#mass-assignment) 문서를 꼭 참고하시기 바랍니다.

<a name="updating-belongs-to-relationships"></a>
### Belongs To(소속) 관계

자식 모델을 새로운 부모 모델에 연결하려면 `associate` 메서드를 사용할 수 있습니다. 예를 들어, `User` 모델이 `Account` 모델에 대한 `belongsTo` 관계를 가진 경우, `associate`를 사용하면 자식 모델에 외래 키가 설정됩니다.

```php
use App\Models\Account;

$account = Account::find(10);

$user->account()->associate($account);

$user->save();
```

반대로, 자식 모델에서 부모 모델과의 관계를 제거하고 싶다면 `dissociate` 메서드를 사용할 수 있습니다. 이 메서드는 관계의 외래 키를 `null`로 만듭니다.

```php
$user->account()->dissociate();

$user->save();
```

<a name="updating-many-to-many-relationships"></a>
### 다대다(Many to Many) 관계

<a name="attaching-detaching"></a>
#### 연결(Attach) 및 분리(Detach)

Eloquent는 다대다 관계를 편리하게 다룰 수 있는 여러 메서드를 제공합니다. 예를 들어, 한 사용자가 여러 역할(role)을 가질 수 있고, 한 역할도 여러 사용자(user)에 연결될 수 있다고 가정할 때, `attach` 메서드를 이용해 중간 테이블에 레코드를 추가하여 사용자를 역할에 연결할 수 있습니다.

```php
use App\Models\User;

$user = User::find(1);

$user->roles()->attach($roleId);
```

관계를 연결할 때, 중간 테이블에 저장할 추가 데이터도 배열로 함께 전달할 수 있습니다.

```php
$user->roles()->attach($roleId, ['expires' => $expires]);
```

역할을 사용자가 보유한 목록에서 제거하려면, `detach` 메서드를 사용해서 다대다 관계 레코드를 중간 테이블에서 삭제할 수 있습니다. 이때, 관계만 끊길 뿐 두 모델 자체는 데이터베이스에서 삭제되지 않습니다.

```php
// 사용자의 특정 역할만 분리...
$user->roles()->detach($roleId);

// 사용자의 모든 역할 분리...
$user->roles()->detach();
```

`attach`와 `detach`는 편의를 위해 ID 배열 형태로도 인수를 받을 수 있습니다.

```php
$user = User::find(1);

$user->roles()->detach([1, 2, 3]);

$user->roles()->attach([
    1 => ['expires' => $expires],
    2 => ['expires' => $expires],
]);
```

<a name="syncing-associations"></a>
#### 동기화(Sync) 관계

`snyc` 메서드를 사용하면 다대다 관계를 동기화할 수 있습니다. 이 메서드로 전달한 ID 배열에 포함되지 않은 모든 중간 테이블 레코드는 삭제되고, 최종적으로 해당 배열에 있는 ID만 중간 테이블에 남게 됩니다.

```php
$user->roles()->sync([1, 2, 3]);
```

ID와 함께 추가적인 중간 테이블 값을 전달할 수도 있습니다.

```php
$user->roles()->sync([1 => ['expires' => true], 2, 3]);
```

동기화되는 모든 ID에 대해 동일한 중간 테이블 값을 입력하고 싶다면 `syncWithPivotValues` 메서드를 사용할 수 있습니다.

```php
$user->roles()->syncWithPivotValues([1, 2, 3], ['active' => true]);
```

전달한 배열에 없는 기존 ID의 관계를 분리하고 싶지 않다면, `syncWithoutDetaching` 메서드를 사용하세요.

```php
$user->roles()->syncWithoutDetaching([1, 2, 3]);
```

<a name="toggling-associations"></a>
#### 관계 토글(Toggle)

다대다 관계에서는 `toggle` 메서드도 사용할 수 있습니다. 이 메서드는 전달된 관련 모델 ID들의 연결 상태를 토글(반전)합니다. 즉, 이미 연결된 ID는 분리하고, 분리된 ID는 연결합니다.

```php
$user->roles()->toggle([1, 2, 3]);
```

ID와 함께 중간 테이블의 추가 데이터를 배열로 전달할 수도 있습니다.

```php
$user->roles()->toggle([
    1 => ['expires' => true],
    2 => ['expires' => true],
]);
```

<a name="updating-a-record-on-the-intermediate-table"></a>
#### 중간 테이블 레코드 수정하기

이미 존재하는 중간 테이블의 레코드를 수정해야 한다면, `updateExistingPivot` 메서드를 사용할 수 있습니다. 이 메서드는 수정할 레코드의 외래 키와, 업데이트할 속성 배열을 인수로 받습니다.

```php
$user = User::find(1);

$user->roles()->updateExistingPivot($roleId, [
    'active' => false,
]);
```

<a name="touching-parent-timestamps"></a>
## 부모 타임스탬프 자동 갱신

모델이 `belongsTo` 또는 `belongsToMany` 관계를 가질 때(예: `Comment`가 `Post`에 소속), 자식 모델이 수정될 때 부모 모델의 타임스탬프(`updated_at`)도 함께 갱신되면 유용할 때가 있습니다.

예를 들어, `Comment` 모델을 수정할 때, 해당 댓글이 속한 `Post`의 `updated_at` 값을 현재 시각으로 자동 갱신하려고 할 수 있습니다. 이를 위해, 자식 모델에 `touches` 속성(property)에 부모로 지정할 관계 이름 배열을 추가하면 됩니다. `Comment` 모델을 저장하면(업데이트하면) 지정한 관계의 부모 모델도 자동으로 `updated_at`이 갱신됩니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Comment extends Model
{
    /**
     * 업데이트 시 함께 갱신(touch)할 관계들의 이름
     *
     * @var array
     */
    protected $touches = ['post'];

    /**
     * 이 댓글이 소속된 게시글(Post) 반환
     */
    public function post(): BelongsTo
    {
        return $this->belongsTo(Post::class);
    }
}
```

> [!WARNING]
> 부모 모델의 타임스탬프는 자식 모델을 Eloquent의 `save` 메서드로 저장할 때에만 자동으로 갱신됩니다.