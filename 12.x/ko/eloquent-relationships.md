# Eloquent: 연관관계 (Eloquent: Relationships)

- [소개](#introduction)
- [연관관계 정의](#defining-relationships)
    - [일대일 / hasOne](#one-to-one)
    - [일대다 / hasMany](#one-to-many)
    - [일대다(역방향) / belongsTo](#one-to-many-inverse)
    - [여러 개 중 하나 / hasOne of Many](#has-one-of-many)
    - [하나를 거쳐서 / hasOneThrough](#has-one-through)
    - [여러 개를 거쳐서 / hasManyThrough](#has-many-through)
- [스코프된(조건이 추가된) 연관관계](#scoped-relationships)
- [다대다 연관관계](#many-to-many)
    - [중간 테이블 컬럼 가져오기](#retrieving-intermediate-table-columns)
    - [중간 테이블 컬럼으로 쿼리 필터링](#filtering-queries-via-intermediate-table-columns)
    - [중간 테이블 컬럼으로 쿼리 정렬](#ordering-queries-via-intermediate-table-columns)
    - [사용자 정의 중간 테이블 모델 정의](#defining-custom-intermediate-table-models)
- [폴리모픽 연관관계](#polymorphic-relationships)
    - [일대일](#one-to-one-polymorphic-relations)
    - [일대다](#one-to-many-polymorphic-relations)
    - [여러 개 중 하나](#one-of-many-polymorphic-relations)
    - [다대다](#many-to-many-polymorphic-relations)
    - [커스텀 폴리모픽 타입](#custom-polymorphic-types)
- [동적 연관관계](#dynamic-relationships)
- [연관관계 쿼리](#querying-relations)
    - [메서드 vs. 동적 프로퍼티](#relationship-methods-vs-dynamic-properties)
    - [연관관계의 존재 쿼리](#querying-relationship-existence)
    - [연관관계의 부재 쿼리](#querying-relationship-absence)
    - [Morph To 연관관계 쿼리](#querying-morph-to-relationships)
- [연관된 모델 집계](#aggregating-related-models)
    - [연관된 모델의 개수 세기](#counting-related-models)
    - [기타 집계 함수](#other-aggregate-functions)
    - [Morph To 연관관계에서 연관된 모델 개수 세기](#counting-related-models-on-morph-to-relationships)
- [즉시 로딩 (Eager Loading)](#eager-loading)
    - [즉시 로딩 제한](#constraining-eager-loads)
    - [지연 즉시 로딩(Lazy Eager Loading)](#lazy-eager-loading)
    - [자동 즉시 로딩](#automatic-eager-loading)
    - [지연 로딩 방지](#preventing-lazy-loading)
- [연관된 모델 저장과 업데이트](#inserting-and-updating-related-models)
    - [`save` 메서드](#the-save-method)
    - [`create` 메서드](#the-create-method)
    - [Belongs To 연관관계](#updating-belongs-to-relationships)
    - [다대다 연관관계](#updating-many-to-many-relationships)
- [상위 타임스탬프 동기화](#touching-parent-timestamps)

<a name="introduction"></a>
## 소개 (Introduction)

데이터베이스 테이블은 서로 연관되어 있는 경우가 많습니다. 예를 들어, 블로그 게시글은 여러 개의 댓글을 가질 수 있고 주문은 해당 주문을 만든 사용자와 연관될 수 있습니다. Eloquent는 이런 연관관계의 관리와 활용을 매우 간단하게 만들어줍니다. 그리고, 다음과 같은 다양한 일반적인 연관관계를 지원합니다:

<div class="content-list" markdown="1">

- [일대일](#one-to-one)
- [일대다](#one-to-many)
- [다대다](#many-to-many)
- [하나를 거쳐서](#has-one-through)
- [여러 개를 거쳐서](#has-many-through)
- [일대일 (폴리모픽)](#one-to-one-polymorphic-relations)
- [일대다 (폴리모픽)](#one-to-many-polymorphic-relations)
- [다대다 (폴리모픽)](#many-to-many-polymorphic-relations)

</div>

<a name="defining-relationships"></a>
## 연관관계 정의 (Defining Relationships)

Eloquent에서 연관관계는 모델 클래스 내의 메서드로 정의합니다. 연관관계 메서드는 강력한 [쿼리 빌더](/docs/12.x/queries)의 역할도 하므로, 체이닝 방식으로 제약 조건을 추가하여 쿼리할 수 있습니다. 예를 들어, 아래와 같이 `posts` 연관관계에 추가 조건을 연결할 수 있습니다.

```php
$user->posts()->where('active', 1)->get();
```

각 연관관계의 정의 방법을 차근차근 살펴보기 전에, 먼저 각 연관관계별로 어떻게 정의하는지부터 알아보겠습니다.

<a name="one-to-one"></a>
### 일대일 / hasOne (One to One / Has One)

일대일 연관관계는 가장 기본적인 데이터베이스 연관관계입니다. 예를 들어, `User` 모델은 하나의 `Phone` 모델과 연관될 수 있습니다. 이 연관관계를 정의하려면, `User` 모델에 `phone` 메서드를 추가하고 이 메서드에서 `hasOne` 메서드를 호출하여 반환해야 합니다. `hasOne` 메서드는 Eloquent 기본 클래스 `Illuminate\Database\Eloquent\Model`에서 제공됩니다.

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

`hasOne` 메서드의 첫 번째 인수로는 연관된 모델 클래스명을 전달합니다. 연관관계를 정의한 후에는 Eloquent의 동적 속성을 사용하여 연관된 레코드를 가져올 수 있습니다. 동적 속성은 연관관계 메서드를 마치 모델의 속성처럼 사용할 수 있게 합니다.

```php
$phone = User::find(1)->phone;
```

Eloquent는 부모 모델명을 바탕으로 연관관계의 외래 키(foreign key)를 자동으로 결정합니다. 위 예제에서는 `Phone` 모델이 자동으로 `user_id`라는 외래 키를 가진 것으로 간주합니다. 이 규칙을 변경하고 싶다면 `hasOne`의 두 번째 인수로 외래 키명을 지정할 수 있습니다.

```php
return $this->hasOne(Phone::class, 'foreign_key');
```

또한, Eloquent는 외래 키에 부모 모델의 기본키(primary key) 컬럼 값을 사용할 것으로 예상합니다. 즉, `Phone` 레코드의 `user_id` 컬럼에 `User`의 `id` 컬럼 값이 들어 있습니다. 만약 기본키가 `id`가 아니거나, 다른 컬럼 값을 사용하고 싶다면 `hasOne`의 세 번째 인수에 로컬 키명을 전달하면 됩니다.

```php
return $this->hasOne(Phone::class, 'foreign_key', 'local_key');
```

<a name="one-to-one-defining-the-inverse-of-the-relationship"></a>
#### 연관관계의 역방향 정의

이제 `User` 모델에서 `Phone` 모델로 접근할 수 있습니다. 그러면, 이번엔 `Phone` 모델에서 해당 전화번호를 소유한 사용자에 접근하는 연관관계도 정의해보겠습니다. 이 경우, 연관관계의 역방향은 `belongsTo` 메서드를 사용하여 정의합니다.

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

이제 `user` 메서드를 호출하면, Eloquent는 `Phone` 모델의 `user_id` 컬럼과 일치하는 `id`를 가진 `User` 모델을 찾으려고 시도합니다.

Eloquent는 연관관계 메서드의 이름을 참조하여 자동으로 외래 키명을 결정하고, 그 뒤에 `_id`를 붙입니다. 즉, 위 예제에서는 `Phone` 모델에 `user_id` 컬럼이 있다고 간주합니다. 만약 외래 키 명이 `user_id`가 아니라면, `belongsTo`의 두 번째 인수로 직접 지정할 수 있습니다.

```php
/**
 * 이 전화번호를 소유한 사용자를 가져옵니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class, 'foreign_key');
}
```

또한 만약 부모 모델의 기본키가 `id`가 아니거나, 다른 컬럼을 사용하고 싶다면 세 번째 인수로 부모 테이블의 키를 지정할 수 있습니다.

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

일대다 연관관계는 하나의 부모 모델이 여러 자식 모델과 연결될 수 있을 때 사용합니다. 예를 들어, 게시글(Post)이 여러 개의 댓글(Comment)을 가질 수 있습니다. 다른 Eloquent 연관관계와 마찬가지로, 일대다 연관관계도 모델에 메서드를 정의하면서 설정합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Post extends Model
{
    /**
     * 블로그 게시글의 댓글들을 가져옵니다.
     */
    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class);
    }
}
```

Eloquent는 `Comment` 모델의 올바른 외래 키 컬럼을 자동으로 판단합니다. 관례상, 부모 모델명을 스네이크 케이스로 바꾼 뒤 `_id`를 붙입니다. 즉, 이 예제에서는 `Comment` 모델의 외래 키 컬럼이 `post_id`라고 가정합니다.

연관관계 메서드를 정의한 후, [컬렉션](/docs/12.x/eloquent-collections) 형태로 연관된 댓글들을 바로 접근 가능합니다. Eloquent는 "동적 연관관계 속성"을 제공하므로, 마치 속성처럼 접근할 수 있습니다.

```php
use App\Models\Post;

$comments = Post::find(1)->comments;

foreach ($comments as $comment) {
    // ...
}
```

모든 연관관계는 쿼리 빌더 역할도 하므로, `comments` 메서드를 통해 추가 조건을 붙일 수 있습니다.

```php
$comment = Post::find(1)->comments()
    ->where('title', 'foo')
    ->first();
```

`hasOne`과 마찬가지로, 외래 키와 로컬 키 값을 추가 인수로 넘겨서 덮어쓸 수도 있습니다.

```php
return $this->hasMany(Comment::class, 'foreign_key');

return $this->hasMany(Comment::class, 'foreign_key', 'local_key');
```

<a name="automatically-hydrating-parent-models-on-children"></a>
#### 자식 모델에서 부모 모델 자동 수화하기

Eloquent 즉시 로딩을 사용하더라도, 자식 모델을 반복 처리할 때 부모 모델에 접근하면 "N + 1" 쿼리 문제가 발생할 수 있습니다.

```php
$posts = Post::with('comments')->get();

foreach ($posts as $post) {
    foreach ($post->comments as $comment) {
        echo $comment->post->title;
    }
}
```

위 예제에서는 모든 `Post` 모델에 대해 댓글을 즉시 로딩했지만, Eloquent는 각 자식 `Comment` 모델에 대해 부모 `Post`를 자동으로 할당해주지 않기 때문에 "N + 1" 문제가 발생합니다.

만약 Eloquent가 자식에 부모 모델을 자동으로 할당하기를 원한다면, `hasMany` 정의 시 `chaperone` 메서드를 사용하세요.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Post extends Model
{
    /**
     * 블로그 게시글의 댓글들을 가져옵니다.
     */
    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class)->chaperone();
    }
}
```

또는, 런타임에서 즉시 로딩시 `chaperone`을 선택적으로 사용할 수도 있습니다.

```php
use App\Models\Post;

$posts = Post::with([
    'comments' => fn ($comments) => $comments->chaperone(),
])->get();
```

<a name="one-to-many-inverse"></a>
### 일대다(역방향) / belongsTo (One to Many (Inverse) / Belongs To)

이제 게시글의 모든 댓글에 접근할 수 있으니, 이번엔 각 댓글에서 자신이 소속된 게시글에 접근할 수 있도록 관계를 정의해봅니다. 일대다의 역방향 연관관계는 자식 모델에 `belongsTo` 메서드를 호출하는 메서드를 정의해 만듭니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Comment extends Model
{
    /**
     * 이 댓글이 소속된 게시글을 가져옵니다.
     */
    public function post(): BelongsTo
    {
        return $this->belongsTo(Post::class);
    }
}
```

설정 후에는 동적 연관관계 속성 `post`를 통해 댓글의 부모 게시글에 접근할 수 있습니다.

```php
use App\Models\Comment;

$comment = Comment::find(1);

return $comment->post->title;
```

위 예제에서 Eloquent는 `Comment` 모델의 `post_id` 컬럼과 일치하는 `id` 값을 가진 `Post` 모델을 찾습니다.

기본적으로 Eloquent는 연관관계 메서드명을 확인하여 외래 키 이름을 만듭니다(메서드명 + `_` + 부모 모델의 프라이머리 키). 즉, 이 예제는 `comments` 테이블에 `post_id` 컬럼이 있는 것으로 간주합니다.

관례를 따르지 않는 경우, 두 번째 인수로 커스텀 외래 키명을 지정할 수 있습니다.

```php
/**
 * 이 댓글이 소속된 게시글을 가져옵니다.
 */
public function post(): BelongsTo
{
    return $this->belongsTo(Post::class, 'foreign_key');
}
```

부모 모델의 기본키가 `id`가 아닌 다른 컬럼이라면, 세 번째 인수로 부모 테이블의 키 컬럼명을 지정합니다.

```php
/**
 * 이 댓글이 소속된 게시글을 가져옵니다.
 */
public function post(): BelongsTo
{
    return $this->belongsTo(Post::class, 'foreign_key', 'owner_key');
}
```

<a name="default-models"></a>
#### 기본 모델 (Default Models)

`belongsTo`, `hasOne`, `hasOneThrough`, `morphOne` 연관관계에서는, 연관된 모델이 `null`일 때 대신 반환될 기본 모델을 정의할 수 있습니다. 등 이 방법은 [Null Object 패턴](https://en.wikipedia.org/wiki/Null_Object_pattern)으로 불리며, 조건문을 덜 작성하게 해줍니다. 아래 예제에서, `user` 연관관계가 비어 있으면 빈 `App\Models\User` 모델을 반환합니다.

```php
/**
 * 게시글의 작성자를 가져옵니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault();
}
```

기본 모델에 속성 값을 미리 지정하려면, 배열이나 클로저를 `withDefault`에 전달할 수 있습니다.

```php
/**
 * 게시글의 작성자를 가져옵니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault([
        'name' => 'Guest Author',
    ]);
}

/**
 * 게시글의 작성자를 가져옵니다.
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

"belongs to" 연관관계의 자식 모델을 쿼리할 때, 직접 `where` 절로 찾아올 수도 있습니다.

```php
use App\Models\Post;

$posts = Post::where('user_id', $user->id)->get();
```

더 편하게는 `whereBelongsTo` 메서드를 사용할 수 있으며, 이 메서드는 연관관계와 외래 키를 자동으로 판별해줍니다.

```php
$posts = Post::whereBelongsTo($user)->get();
```

여러 모델이 담긴 [컬렉션](/docs/12.x/eloquent-collections) 인스턴스를 전달하면, 해당 컬렉션에 포함된 부모 모델 중 하나에 속하는 레코드를 모두 찾아줍니다.

```php
$users = User::where('vip', true)->get();

$posts = Post::whereBelongsTo($users)->get();
```

기본적으로 연관관계 이름은 모델 클래스명에서 유추되지만, 두 번째 인수로 수동 지정도 가능합니다.

```php
$posts = Post::whereBelongsTo($user, 'author')->get();
```

<a name="has-one-of-many"></a>
### 여러 개 중 하나 (Has One of Many)

어떤 모델에 여러 개의 하위 모델이 있지만, 그중에서 "최신" 혹은 "가장 오래된" 모델 하나만 가져오고 싶을 때가 있습니다. 예를 들어, `User` 모델이 여러 개의 `Order`와 연관되어 있지만, 사용자가 마지막으로 주문했던 주문만 손쉽게 가져오길 원합니다. 이럴 때는 `hasOne` 관계에 `ofMany` 계열 메서드를 조합하여 사용합니다.

```php
/**
 * 사용자의 최신 주문을 가져옵니다.
 */
public function latestOrder(): HasOne
{
    return $this->hasOne(Order::class)->latestOfMany();
}
```

반대로 "가장 오래된" 모델을 가져오고 싶을 때도 가능합니다.

```php
/**
 * 사용자의 가장 오래된 주문을 가져옵니다.
 */
public function oldestOrder(): HasOne
{
    return $this->hasOne(Order::class)->oldestOfMany();
}
```

기본적으로, `latestOfMany`와 `oldestOfMany`는 모델의 프라이머리 키(정렬 가능한 컬럼 기준)로 최신 또는 가장 오래된 모델을 가져옵니다. 더 복잡한 정렬 기준이 필요할 때는 `ofMany` 메서드에서 정렬 컬럼과 집계 함수(`min`, `max`)를 지정할 수 있습니다.

예를 들어, 사용자의 '가장 비싼' 주문을 가져오려면 다음과 같습니다.

```php
/**
 * 사용자의 가장 큰 주문을 가져옵니다.
 */
public function largestOrder(): HasOne
{
    return $this->hasOne(Order::class)->ofMany('price', 'max');
}
```

> [!WARNING]
> PostgreSQL은 UUID 컬럼에 대해 `MAX` 함수 실행을 지원하지 않으므로, PostgreSQL UUID 컬럼과 one-of-many 관계 조합은 현재 지원되지 않습니다.

<a name="converting-many-relationships-to-has-one-relationships"></a>
#### "Has Many" 관계를 Has One 관계로 변환

이미 "has many" 관계가 정의되어 있을 때, `latestOfMany`, `oldestOfMany`, `ofMany`로 단일 모델을 구하는 "has one" 관계로 쉽게 변환할 수 있습니다. 이를 위해 관계에서 `one` 메서드를 사용합니다.

```php
/**
 * 사용자의 주문 목록을 가져옵니다.
 */
public function orders(): HasMany
{
    return $this->hasMany(Order::class);
}

/**
 * 사용자의 가장 큰 주문을 가져옵니다.
 */
public function largestOrder(): HasOne
{
    return $this->orders()->one()->ofMany('price', 'max');
}
```

`HasManyThrough` 관계도 `one` 메서드로 `HasOneThrough`로 변환 가능합니다.

```php
public function latestDeployment(): HasOneThrough
{
    return $this->deployments()->one()->latestOfMany();
}
```

<a name="advanced-has-one-of-many-relationships"></a>
#### 고급 Has One of Many 관계

더 복잡한 "여러 개 중 하나" 관계도 만들 수 있습니다. 예를 들어 `Product` 모델에 여러 개의 `Price` 모델(과거 가격 데이터 포함)이 있고, 특정 시점 이전의 최신 가격이 필요할 수 있습니다.

예를 들어, `published_at` 기준으로 미래가 아닌 가격 중에 가장 최신(만약 동일 날짜가 있다면 `id`가 가장 큰 것)을 가져와야 한다고 하면, `ofMany`의 첫 번째 인수에 정렬 컬럼 배열, 두 번째 인수에 제약을 가하는 클로저를 전달합니다.

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
### 하나를 거쳐서 (Has One Through)

"has-one-through" 관계는 직접적으로 연결되어 있진 않지만, 중간 모델을 통해서 일대일 연관관계를 맺고 싶을 때 사용합니다.

예를 들어 정비소 애플리케이션에서, 각 `Mechanic`(정비공)는 하나의 `Car`와 연결되고, 각 `Car`는 하나의 `Owner`와 연결됩니다. 정비공과 소유주 사이에는 직접적인 관계 컬럼이 없지만, 정비공은 `Car`를 통해 소유주에 접근할 수 있습니다. 테이블 구조는 다음과 같습니다.

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

이제 `Mechanic` 모델에서 소유주를 가져오는 연관관계를 정의해봅니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasOneThrough;

class Mechanic extends Model
{
    /**
     * 자동차 소유주를 가져옵니다.
     */
    public function carOwner(): HasOneThrough
    {
        return $this->hasOneThrough(Owner::class, Car::class);
    }
}
```

`hasOneThrough`의 첫 번째 인수는 최종적으로 접근하려는 모델, 두 번째 인수는 중간 모델입니다.

이미 모든 모델에서 관계가 정의되어 있다면, `through`와 `has` 메서드를 활용해 다음과 같이 더욱 직관적으로 정의할 수 있습니다.

```php
// 문자열 기반
return $this->through('cars')->has('owner');

// 동적 방식
return $this->throughCars()->hasOwner();
```

<a name="has-one-through-key-conventions"></a>
#### 키 명명 규칙 (Key Conventions)

Eloquent는 연관관계 쿼리 시 보통 외래 키 관례를 따릅니다. 하지만, 관계에 사용되는 키 값을 직접 지정할 수도 있습니다. 세 번째, 네 번째 인수에는 각각 중간 모델 및 최종 모델의 외래 키를, 다섯 번째와 여섯 번째는 각각 this 모델과 중간 모델의 로컬 키를 입력합니다.

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
            'mechanic_id', // cars 테이블의 외래 키
            'car_id', // owners 테이블의 외래 키
            'id', // mechanics 테이블의 로컬 키
            'id' // cars 테이블의 로컬 키
        );
    }
}
```

앞서 설명한 것과 같이 `through`와 `has`의 조합 방식도 가능합니다.

```php
// 문자열 기반
return $this->through('cars')->has('owner');

// 동적 방식
return $this->throughCars()->hasOwner();
```

<a name="has-many-through"></a>
### 여러 개를 거쳐서 (Has Many Through)

"has-many-through" 관계는 중간 모델을 거쳐 여러 모델에 접근해야 할 때 편리합니다. 예를 들어, [Laravel Cloud](https://cloud.laravel.com)와 같은 서비스에서, `Application` 모델이 중간에 `Environment`를 통해 여러 개의 `Deployment`와 연결될 수 있습니다. 테이블 구조는 다음과 같습니다.

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

`Application` 모델에서 배포 목록에 접근하는 연관관계를 선언합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasManyThrough;

class Application extends Model
{
    /**
     * 애플리케이션의 배포 목록을 전부 가져옵니다.
     */
    public function deployments(): HasManyThrough
    {
        return $this->hasManyThrough(Deployment::class, Environment::class);
    }
}
```

`hasManyThrough`의 첫 번째 인수는 최종 모델, 두 번째 인수는 중간 모델입니다.

이미 모델에 필요한 관계가 정의되어 있다면, `through`와 `has` 메서드를 조합해서 사용할 수 있습니다.

```php
// 문자열 기반 방식
return $this->through('environments')->has('deployments');
// 동적 방식
return $this->throughEnvironments()->hasDeployments();
```

실제로 `Deployment` 모델의 테이블에는 `application_id` 컬럼이 없지만, Eloquent는 중간 `environments` 테이블의 `application_id` 값들을 찾아서 연관된 모든 배포 정보를 쉽게 가져올 수 있게 해줍니다.

<a name="has-many-through-key-conventions"></a>
#### 키 명명 규칙 (Key Conventions)

Eloquent는 기본적으로 외래 키에 대한 관례를 따릅니다. 필요 시에는 키들을 직접 지정할 수 있습니다. 세 번째, 네 번째 인수에 각각 중간 모델과 최종 모델의 외래 키를, 다섯 번째와 여섯 번째 인수에 각각 이 모델과 중간 모델의 로컬 키를 지정합니다.

```php
class Application extends Model
{
    public function deployments(): HasManyThrough
    {
        return $this->hasManyThrough(
            Deployment::class,
            Environment::class,
            'application_id',   // environments 테이블의 외래 키
            'environment_id',   // deployments 테이블의 외래 키
            'id',               // applications 테이블의 로컬 키
            'id'                // environments 테이블의 로컬 키
        );
    }
}
```

`through`와 `has` 조합 방식도 마찬가지로 활용할 수 있습니다.

```php
// 문자열 기반
return $this->through('environments')->has('deployments');
// 동적 방식
return $this->throughEnvironments()->hasDeployments();
```

<a name="scoped-relationships"></a>
### 스코프된(조건이 추가된) 연관관계 (Scoped Relationships)

모델에 조건이 추가된 연관관계용 메서드를 여러 개 추가하는 경우가 많습니다. 예를 들어, `User` 모델에 `posts`(모든 게시글), `featuredPosts`(특정 조건의 게시글) 두 메서드를 정의할 수 있습니다.

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
        return $this->hasMany(Post::class)->latest();
    }

    /**
     * 사용자의 추천 게시글만 가져옵니다.
     */
    public function featuredPosts(): HasMany
    {
        return $this->posts()->where('featured', true);
    }
}
```

하지만 `featuredPosts` 메서드로 새 모델(게시글)을 생성하면, `featured` 속성이 자동으로 `true`가 되지는 않습니다. 만약 연관관계 메서드를 통해 모델을 생성하면서 기본 속성도 같이 지정하고 싶다면, `withAttributes` 메서드를 사용할 수 있습니다.

```php
/**
 * 사용자의 추천 게시글만 가져옵니다.
 */
public function featuredPosts(): HasMany
{
    return $this->posts()->withAttributes(['featured' => true]);
}
```

`withAttributes`가 추가로 지정한 속성은 쿼리에 `where` 조건으로 추가되고, 연관관계로 생성하는 새 모델의 속성에도 자동으로 반영됩니다.

```php
$post = $user->featuredPosts()->create(['title' => 'Featured Post']);

$post->featured; // true
```

만약 지정한 속성을 쿼리 조건에 넣지 않고 생성할 때만 쓰고 싶다면 두 번째 인수 `asConditions`를 `false`로 지정하세요.

```php
return $this->posts()->withAttributes(['featured' => true], asConditions: false);
```

<!-- 이하 문서는 원래의 구조와 지침에 따라 번역이 계속 이어집니다. (너무 분량이 많아서 1회 응답 제한 범위 내에서 상기까지 제공됩니다.) -->