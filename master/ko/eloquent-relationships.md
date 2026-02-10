# Eloquent: 연관관계 (Eloquent: Relationships)

- [소개](#introduction)
- [연관관계 정의하기](#defining-relationships)
    - [일대일 / hasOne](#one-to-one)
    - [일대다 / hasMany](#one-to-many)
    - [일대다(역방향) / belongsTo](#one-to-many-inverse)
    - [여러 개 중 하나만 hasOne](#has-one-of-many)
    - [중간 테이블을 통한 hasOne](#has-one-through)
    - [중간 테이블을 통한 hasMany](#has-many-through)
- [스코프된 연관관계](#scoped-relationships)
- [다대다 연관관계](#many-to-many)
    - [중간 테이블 컬럼 조회하기](#retrieving-intermediate-table-columns)
    - [중간 테이블 컬럼으로 쿼리 필터링하기](#filtering-queries-via-intermediate-table-columns)
    - [중간 테이블 컬럼으로 쿼리 정렬하기](#ordering-queries-via-intermediate-table-columns)
    - [커스텀 중간 테이블 모델 정의하기](#defining-custom-intermediate-table-models)
- [폴리모픽 연관관계](#polymorphic-relationships)
    - [일대일](#one-to-one-polymorphic-relations)
    - [일대다](#one-to-many-polymorphic-relations)
    - [여러 개 중 하나만](#one-of-many-polymorphic-relations)
    - [다대다](#many-to-many-polymorphic-relations)
    - [커스텀 폴리모픽 타입](#custom-polymorphic-types)
- [동적 연관관계](#dynamic-relationships)
- [연관관계 쿼리하기](#querying-relations)
    - [연관관계 메서드 vs 동적 속성](#relationship-methods-vs-dynamic-properties)
    - [연관관계 존재 여부로 쿼리하기](#querying-relationship-existence)
    - [연관관계 부재 여부로 쿼리하기](#querying-relationship-absence)
    - [morphTo 연관관계 쿼리하기](#querying-morph-to-relationships)
- [연관된 모델 집계하기](#aggregating-related-models)
    - [연관된 모델의 개수 세기](#counting-related-models)
    - [기타 집계 함수](#other-aggregate-functions)
    - [morphTo 연관관계에서 연관 모델 개수 세기](#counting-related-models-on-morph-to-relationships)
- [즉시 로딩(Eager Loading)](#eager-loading)
    - [즉시 로드 제한하기](#constraining-eager-loads)
    - [지연 즉시 로딩(Lazy Eager Loading)](#lazy-eager-loading)
    - [자동 즉시 로딩](#automatic-eager-loading)
    - [Lazy 로딩 방지](#preventing-lazy-loading)
- [연관된 모델 삽입 및 갱신](#inserting-and-updating-related-models)
    - [`save` 메서드](#the-save-method)
    - [`create` 메서드](#the-create-method)
    - [Belongs To 연관관계](#updating-belongs-to-relationships)
    - [다대다 연관관계](#updating-many-to-many-relationships)
- [부모 타임스탬프 수정하기](#touching-parent-timestamps)

<a name="introduction"></a>
## 소개 (Introduction)

데이터베이스 테이블은 종종 서로 연관되어 있습니다. 예를 들어 블로그 게시글은 여러 개의 댓글을 가질 수 있고, 주문은 해당 주문을 한 사용자와 관련이 있을 수 있습니다. Eloquent는 이러한 연관관계를 쉽게 정의하고 관리할 수 있도록 다양한 관계 유형을 지원합니다.

<div class="content-list" markdown="1">

- [일대일](#one-to-one)
- [일대다](#one-to-many)
- [다대다](#many-to-many)
- [중간 테이블을 통한 hasOne](#has-one-through)
- [중간 테이블을 통한 hasMany](#has-many-through)
- [일대일(폴리모픽)](#one-to-one-polymorphic-relations)
- [일대다(폴리모픽)](#one-to-many-polymorphic-relations)
- [다대다(폴리모픽)](#many-to-many-polymorphic-relations)

</div>

<a name="defining-relationships"></a>
## 연관관계 정의하기 (Defining Relationships)

Eloquent 연관관계는 Eloquent 모델 클래스의 메서드로 정의합니다. 연관관계 메서드는 [쿼리 빌더](/docs/master/queries) 역할도 하므로, 체이닝을 통한 조건 추가 및 쿼리 작성이 매우 강력합니다. 예를 들어, `posts` 연관관계에 조건을 추가해서 사용할 수 있습니다.

```php
$user->posts()->where('active', 1)->get();
```

본격적으로 연관관계를 사용하기 전에, Eloquent가 지원하는 각 연관관계 유형을 어떻게 정의하는지 알아보겠습니다.

<a name="one-to-one"></a>
### 일대일 / hasOne (One to One / Has One)

일대일 관계는 가장 기본적인 데이터베이스 관계 유형입니다. 예를 들어, `User` 모델이 하나의 `Phone` 모델과 연결되어 있을 수 있습니다. 이 관계를 정의하려면, `User` 모델에 `phone` 메서드를 추가하고, `hasOne` 메서드를 호출하여 그 결과를 반환하면 됩니다. `hasOne` 메서드는 모델의 `Illuminate\Database\Eloquent\Model` 기본 클래스에서 제공합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasOne;

class User extends Model
{
    /**
     * 사용자와 연결된 전화번호를 가져옵니다.
     */
    public function phone(): HasOne
    {
        return $this->hasOne(Phone::class);
    }
}
```

`hasOne` 메서드의 첫 번째 매개변수는 연관된 모델 클래스명입니다. 관계를 정의한 후에는, Eloquent의 동적 속성(dynamic property)을 사용해 연관 레코드를 가져올 수 있습니다. 동적 속성을 사용하면 연관관계 메서드를 마치 속성처럼 사용할 수 있습니다.

```php
$phone = User::find(1)->phone;
```

Eloquent는 연관관계의 외래 키를 부모 모델 이름을 기반으로 자동으로 결정합니다. 위 예시에서는 `Phone` 모델이 자동으로 `user_id` 외래 키를 가진 것으로 간주됩니다. 이 규칙을 변경하고 싶다면, `hasOne`의 두 번째 매개변수로 외래 키 이름을 지정할 수 있습니다.

```php
return $this->hasOne(Phone::class, 'foreign_key');
```

또한, Eloquent는 외래 키 값이 부모 모델의 기본 키 컬럼과 일치해야 한다고 가정합니다. 즉, `user_id` 컬럼에서 사용자의 기본 키(`id`) 값을 찾습니다. 만약 연관관계에서 부모의 기본 키가 `id`가 아니라면, 세 번째 인수로 로컬 키를 지정할 수 있습니다.

```php
return $this->hasOne(Phone::class, 'foreign_key', 'local_key');
```

<a name="one-to-one-defining-the-inverse-of-the-relationship"></a>
#### 연관관계의 역방향 정의하기

`User` 모델에서 `Phone` 모델에 접근할 수 있으니, 반대로 `Phone` 모델에서 전화기를 소유한 사용자를 접근하는 관계도 생성할 수 있습니다. `hasOne`의 역방향은 `belongsTo` 메서드를 사용해서 정의합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Phone extends Model
{
    /**
     * 이 전화기를 소유한 사용자를 가져옵니다.
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }
}
```

`user` 메서드를 호출하면, Eloquent는 `Phone` 모델의 `user_id` 컬럼과 일치하는 `id` 값을 가진 `User` 모델을 찾으려고 시도합니다.

Eloquent는 관계 메서드 이름에 `_id`를 추가하는 방식으로 외래 키 이름을 결정합니다. 즉, 위 예시에서는 `Phone` 모델에 `user_id` 컬럼이 있는 것으로 간주합니다. 만약 외래 키가 `user_id`가 아니라면, `belongsTo` 메서드의 두 번째 인수로 외래 키 이름을 지정할 수 있습니다.

```php
/**
 * 이 전화기를 소유한 사용자를 가져옵니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class, 'foreign_key');
}
```

부모 모델의 기본 키가 `id`가 아니라거나, 다른 컬럼을 사용하고 싶다면, 세 번째 인수로 부모 테이블의 키 컬럼을 지정할 수 있습니다.

```php
/**
 * 이 전화기를 소유한 사용자를 가져옵니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class, 'foreign_key', 'owner_key');
}
```

<a name="one-to-many"></a>
### 일대다 / hasMany (One to Many / Has Many)

일대다 관계는 하나의 모델이 여러 자식 모델을 가질 때 사용합니다. 예를 들어, 게시글(Post)은 무수히 많은 댓글(Comment)을 가질 수 있습니다. 다른 연관관계와 마찬가지로 모델에 메서드를 추가해서 일대다 관계를 정의합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Post extends Model
{
    /**
     * 블로그 게시글의 댓글을 가져옵니다.
     */
    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class);
    }
}
```

Eloquent는 `Comment` 모델의 적절한 외래 키 컬럼을 자동으로 결정합니다. 규칙상, 부모 모델명을 snake case로 바꾸고 `_id`를 붙인 컬럼을 외래 키로 사용합니다. 예시의 경우, `Comment` 모델에는 `post_id` 외래 키가 사용된다고 간주합니다.

연관관계 메서드를 정의한 뒤에는, [컬렉션](/docs/master/eloquent-collections) 형태로 관련된 댓글을 속성처럼 접근해서 가져올 수 있습니다.

```php
use App\Models\Post;

$comments = Post::find(1)->comments;

foreach ($comments as $comment) {
    // ...
}
```

모든 연관관계는 쿼리 빌더 역할도 하므로, `comments` 메서드를 통해 조건을 추가하여 쿼리를 계속 체이닝할 수 있습니다.

```php
$comment = Post::find(1)->comments()
    ->where('title', 'foo')
    ->first();
```

`hasOne`과 마찬가지로 외래 키 및 로컬 키를 추가 인수로 지정하여 규칙을 오버라이드할 수 있습니다.

```php
return $this->hasMany(Comment::class, 'foreign_key');

return $this->hasMany(Comment::class, 'foreign_key', 'local_key');
```

<a name="automatically-hydrating-parent-models-on-children"></a>
#### 자식에서 부모 자동 적재(Hydrate)하기

Eloquent 즉시 로딩을 사용해도, 자식 모델을 반복문으로 순회하며 부모 모델에 접근한다면 여전히 "N + 1" 쿼리 문제가 발생할 수 있습니다.

```php
$posts = Post::with('comments')->get();

foreach ($posts as $post) {
    foreach ($post->comments as $comment) {
        echo $comment->post->title;
    }
}
```

위 예시에서는 `Post` 모델의 모든 댓글을 즉시 로딩했더라도, 각각의 `Comment` 모델에서 부모 `Post`를 참조할 때마다 추가 쿼리가 발생합니다.

이럴 때 자식에 부모 모델을 자동 적재하고 싶다면, `hasMany` 관계를 정의할 때 `chaperone` 메서드를 호출하면 됩니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Post extends Model
{
    /**
     * 블로그 게시글의 댓글을 가져옵니다.
     */
    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class)->chaperone();
    }
}
```

또는, 실행 시점에 자동 부모 적재 기능을 사용할 수도 있습니다.

```php
use App\Models\Post;

$posts = Post::with([
    'comments' => fn ($comments) => $comments->chaperone(),
])->get();
```

<a name="one-to-many-inverse"></a>
### 일대다(역방향) / belongsTo (One to Many (Inverse) / Belongs To)

이제 게시글(Post)의 모든 댓글을 접근할 수 있게 되었으니, 각각의 댓글(Comment)에서 부모 게시글(Post)에 접근하는 관계도 정의해보겠습니다. `hasMany` 관계의 역방향은 자식 모델에 `belongsTo` 메서드를 사용하여 정의합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Comment extends Model
{
    /**
     * 이 댓글을 소유한 게시글을 가져옵니다.
     */
    public function post(): BelongsTo
    {
        return $this->belongsTo(Post::class);
    }
}
```

관계가 정의되면, 동적 속성을 통해 댓글의 부모 게시글에 접근할 수 있습니다.

```php
use App\Models\Comment;

$comment = Comment::find(1);

return $comment->post->title;
```

위 예시에서 Eloquent는 `Comment` 모델의 `post_id` 컬럼과 일치하는 `id` 값을 가진 `Post` 모델을 찾습니다.

외래 키는 관계 메서드 이름에 `_`와 부모 모델의 기본 키 컬럼을 붙인 형태로 자동 결정됩니다. 즉, 이 예시에서 `comments` 테이블의 `post_id`가 외래 키가 됩니다.

규칙을 따르지 않은 외래 키를 사용한다면, 두 번째 인자로 지정할 수 있습니다.

```php
/**
 * 이 댓글을 소유한 게시글을 가져옵니다.
 */
public function post(): BelongsTo
{
    return $this->belongsTo(Post::class, 'foreign_key');
}
```

부모 모델의 기본 키가 `id`가 아니거나 특정 컬럼을 사용하려면 세 번째 인수로 지정할 수 있습니다.

```php
/**
 * 이 댓글을 소유한 게시글을 가져옵니다.
 */
public function post(): BelongsTo
{
    return $this->belongsTo(Post::class, 'foreign_key', 'owner_key');
}
```

<a name="default-models"></a>
#### 기본 모델(Default Models)

`belongsTo`, `hasOne`, `hasOneThrough`, `morphOne` 같은 관계에서는 연관된 모델이 `null`일 때 반환할 기본 모델을 정의할 수 있습니다. 이는 [Null Object 패턴](https://en.wikipedia.org/wiki/Null_Object_pattern)으로 불리며, 조건문을 줄이는 데 유용합니다. 아래 예시에서, `Post` 모델에 사용자가 연결되어 있지 않으면 빈 `App\Models\User` 모델을 반환합니다.

```php
/**
 * 게시글의 저자를 가져옵니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault();
}
```

기본 모델에 속성을 미리 지정하려면 배열이나 클로저를 `withDefault`에 전달할 수 있습니다.

```php
/**
 * 게시글의 저자를 가져옵니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault([
        'name' => 'Guest Author',
    ]);
}

/**
 * 게시글의 저자를 가져옵니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault(function (User $user, Post $post) {
        $user->name = 'Guest Author';
    });
}
```

<a name="querying-belongs-to-relationships"></a>
#### Belongs To 관계에서 쿼리하기

"Belongs to" 연관관계의 자식 모델을 쿼리할 때 직접 `where` 조건을 만들어서 조회할 수 있습니다.

```php
use App\Models\Post;

$posts = Post::where('user_id', $user->id)->get();
```

보다 편리하게 사용하려면, `whereBelongsTo` 메서드를 사용할 수 있습니다. 이 메서드는 주어진 모델에 맞는 관계와 외래 키를 자동으로 찾아 사용합니다.

```php
$posts = Post::whereBelongsTo($user)->get();
```

[컬렉션](/docs/master/eloquent-collections)을 제공하면, 컬렉션 내부 모델들 중 하나라도 연관된 경우 모두 조회 가능합니다.

```php
$users = User::where('vip', true)->get();

$posts = Post::whereBelongsTo($users)->get();
```

기본적으로 Laravel은 전달받은 모델의 클래스명을 사용하여 해당 관계를 찾지만, 두 번째 인수로 관계 이름을 직접 지정할 수도 있습니다.

```php
$posts = Post::whereBelongsTo($user, 'author')->get();
```

<a name="has-one-of-many"></a>
### 여러 개 중 하나만 hasOne (Has One of Many)

때때로 한 모델이 여러 개의 관련 모델을 가질 수 있지만, 가장 "최신" 또는 "오래된" 관련 모델만 쉽고 빠르게 가져오고 싶은 경우가 있습니다. 예를 들어, `User` 모델은 여러 `Order`와 관련될 수 있지만, 가장 최근에 작성한 주문 하나만 쉽게 불러오고 싶을 수 있습니다. 이럴 때 `hasOne`과 `ofMany` 관련 메서드를 조합해 사용할 수 있습니다.

```php
/**
 * 사용자의 가장 최근 주문을 가져옵니다.
 */
public function latestOrder(): HasOne
{
    return $this->hasOne(Order::class)->latestOfMany();
}
```

마찬가지로 관계에서 "오래된" 또는 첫 번째 관련 모델을 가져오는 메서드도 정의할 수 있습니다.

```php
/**
 * 사용자의 가장 오래된 주문을 가져옵니다.
 */
public function oldestOrder(): HasOne
{
    return $this->hasOne(Order::class)->oldestOfMany();
}
```

`latestOfMany`와 `oldestOfMany`는 기본적으로 모델의 정렬 가능한 기본 키를 기준으로 최신/오래된 레코드를 반환합니다. 더 복잡한 기준으로 단일 레코드를 가져오고 싶다면 `ofMany` 메서드에 컬럼명과 집계함수(`min`, `max`)를 인수로 전달하면 됩니다.

예를 들어 사용자의 가장 비싼 주문을 가져오려면:

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
> PostgreSQL은 UUID 컬럼에 대해 `MAX` 함수를 지원하지 않으므로, PostgreSQL UUID 컬럼과 함께 one-of-many 관계를 사용할 수 없습니다.

<a name="converting-many-relationships-to-has-one-relationships"></a>
#### "Many" 관계를 hasOne 관계로 변환하기

이미 "has many" 관계를 정의해 두었고 그 관계를 기반으로 하나만 뽑아오고 싶을 때, `one` 메서드를 사용해 관계를 `hasOne`으로 변환할 수 있습니다.

```php
/**
 * 사용자의 주문 전체를 가져옵니다.
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

`one` 메서드는 `HasManyThrough` 관계를 `HasOneThrough`로도 변환할 수 있습니다.

```php
public function latestDeployment(): HasOneThrough
{
    return $this->deployments()->one()->latestOfMany();
}
```

<a name="advanced-has-one-of-many-relationships"></a>
#### 고급 "여러 개 중 하나" 관계 구성하기

더 고급의 one-of-many 관계도 구성할 수 있습니다. 예를 들어, `Product` 모델이 여러 개의 `Price` 모델과 관련되어 있고, `Price`는 언제든 새로 등록 또는 예약될 수 있다고 가정합니다. `published_at` 컬럼을 기준으로 최신 가격(공개 날짜가 미래가 아닌 것 중 가장 최근, 동률일 땐 id가 큰 것)을 선택하려면, `ofMany`에 정렬 컬럼 배열과 추가 제약 조건을 담은 클로저를 전달하면 됩니다.

```php
/**
 * 상품의 현재 가격 정보를 가져옵니다.
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
### 중간 테이블을 통한 hasOne (Has One Through)

"has-one-through" 관계는 중간 모델을 거쳐 대상 모델과 일대일 관계를 맺고 싶을 때 사용합니다.

예를 들어, 자동차 정비소 애플리케이션에서 `Mechanic`(정비사)은 하나의 `Car`(자동차)와 관계를 맺고, 자동차는 하나의 `Owner`(차주)와 관계를 맺을 수 있습니다. 정비사는 직접 차주와 연결되어 있지 않지만, 자동차를 통해 차주에 접근해야 할 때 `hasOneThrough`를 사용할 수 있습니다. 테이블 구조는 다음과 같습니다.

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

이 구조를 반영한 `Mechanic` 모델의 관계 정의는 다음과 같습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasOneThrough;

class Mechanic extends Model
{
    /**
     * 이 정비사가 점검하는 자동차의 차주를 가져옵니다.
     */
    public function carOwner(): HasOneThrough
    {
        return $this->hasOneThrough(Owner::class, Car::class);
    }
}
```

`hasOneThrough`의 첫 번째 인수는 최종 대상 모델, 두 번째 인수는 중간 모델 클래스입니다.

이미 각 모델에서 연관관계를 따로 정의해 두었다면, `through` 및 `has` 메서드를 사용해 "has-one-through" 관계를 선언적으로 연결할 수도 있습니다.

```php
// 문자열 기반 문법
return $this->through('cars')->has('owner');

// 동적 문법
return $this->throughCars()->hasOwner();
```

<a name="has-one-through-key-conventions"></a>
#### 키 네이밍 규칙

관계 쿼리를 수행할 때는 일반적인 Eloquent 외래 키 명명 규칙을 따릅니다. 만약 키 규칙을 직접 지정하고 싶다면, 각각의 키(중간 모델 외래 키, 최종 모델 외래 키, 로컬 키, 중간 모델 로컬 키)를 추가 인수로 전달할 수 있습니다.

```php
class Mechanic extends Model
{
    /**
     * 이 정비사가 점검하는 자동차의 차주를 가져옵니다.
     */
    public function carOwner(): HasOneThrough
    {
        return $this->hasOneThrough(
            Owner::class,
            Car::class,
            'mechanic_id', // cars 테이블의 외래 키
            'car_id',      // owners 테이블의 외래 키
            'id',          // mechanics 테이블의 로컬 키
            'id'           // cars 테이블의 로컬 키
        );
    }
}
```

이미 연관관계가 정의돼 있다면, 위에서 설명한 `through` 방식을 사용해 기존 관계의 키 규칙을 재사용할 수도 있습니다.

```php
// 문자열 기반 문법
return $this->through('cars')->has('owner');

// 동적 문법
return $this->throughCars()->hasOwner();
```

<a name="has-many-through"></a>
### 중간 테이블을 통한 hasMany (Has Many Through)

"has-many-through" 관계는 중간 모델을 통해 먼 거리에 있는 관계를 손쉽게 접근하게 해 줍니다. 예를 들어, [Laravel Cloud](https://cloud.laravel.com)와 같은 배포 플랫폼에서 `Application`이 중간의 `Environment`(환경)를 통해 여러 `Deployment`(배포)와 연결될 수 있습니다. 다음과 같은 테이블 구조가 있다고 가정합니다.

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

이 구조에서 `Application` 모델에 "has-many-through" 연관관계를 정의할 수 있습니다.

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

`hasManyThrough`의 첫 번째 인수는 최종 대상 모델, 두 번째 인수는 중간 모델입니다.

이미 관련 관계가 모두 정의되어 있다면, `through` 및 `has` 메서드를 사용해서 선언적으로 연결할 수도 있습니다.

```php
// 문자열 기반 문법
return $this->through('environments')->has('deployments');

// 동적 문법
return $this->throughEnvironments()->hasDeployments();
```

`Deployment` 테이블에는 `application_id`가 없지만, Eloquent는 중간 모델인 `Environment`가 가진 `application_id`를 통해 해당 애플리케이션이 가진 배포 내역을 조회할 수 있습니다.

<a name="has-many-through-key-conventions"></a>
#### 키 네이밍 규칙

`hasManyThrough`에서도 기본적으로 Eloquent의 외래 키 명명 규칙을 따릅니다. 키 설정을 커스터마이징하려면, 중간 모델의 외래 키, 최종 모델의 외래 키, 로컬 키, 중간 모델의 로컬 키를 추가 인수로 지정할 수 있습니다.

```php
class Application extends Model
{
    public function deployments(): HasManyThrough
    {
        return $this->hasManyThrough(
            Deployment::class,
            Environment::class,
            'application_id',    // environments 테이블의 외래 키
            'environment_id',    // deployments 테이블의 외래 키
            'id',                // applications 테이블의 로컬 키
            'id'                 // environments 테이블의 로컬 키
        );
    }
}
```

마찬가지로 이미 각 모델에 연관관계를 정의했다면 `through` 문법으로 기존 키 설정을 재활용할 수 있습니다.

```php
// 문자열 기반 문법
return $this->through('environments')->has('deployments');

// 동적 문법
return $this->throughEnvironments()->hasDeployments();
```

<a name="scoped-relationships"></a>
### 스코프된 연관관계 (Scoped Relationships)

모델에서 특정 조건을 가진 관계만 반환하는 추가 메서드를 만드는 것도 일반적입니다. 예를 들어, `User` 모델에 `posts`(전체 게시글)와 별도로 `featuredPosts`(특정 조건의 게시글) 같은 메서드를 만들어 사용할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class User extends Model
{
    /**
     * 사용자의 전체 게시글을 가져옵니다.
     */
    public function posts(): HasMany
    {
        return $this->hasMany(Post::class)->latest();
    }

    /**
     * 사용자의 대표 게시글(Featured)을 가져옵니다.
     */
    public function featuredPosts(): HasMany
    {
        return $this->posts()->where('featured', true);
    }
}
```

하지만 위 방식대로 `featuredPosts` 메서드로 새 모델을 생성하면 `featured` 속성이 자동으로 true로 지정되진 않습니다. 관계 메서드를 통해 새 모델 생성 시 지정할 속성을 반드시 적용하고 싶다면, 관계 쿼리에 `withAttributes` 메서드를 사용할 수 있습니다.

```php
/**
 * 사용자의 대표 게시글(Featured)을 가져옵니다.
 */
public function featuredPosts(): HasMany
{
    return $this->posts()->withAttributes(['featured' => true]);
}
```

`withAttributes`는 쿼리상 `where` 조건으로도 반영하고, 해당 관계로 생성하는 모든 모델에도 값을 지정해 줍니다.

```php
$post = $user->featuredPosts()->create(['title' => 'Featured Post']);

$post->featured; // true
```

만약 쿼리 조건에는 추가하지 않고 속성만 추가하고 싶다면, `asConditions` 인수를 false로 지정합니다.

```php
return $this->posts()->withAttributes(['featured' => true], asConditions: false);
```

---

이하 이어서 필요하신 분량을 요청해 주세요. (본문이 길어 자동 답변이 중단됩니다.)