# Eloquent: 연관관계 (Eloquent: Relationships)

- [소개](#introduction)
- [연관관계 정의하기](#defining-relationships)
    - [일대일 / hasOne](#one-to-one)
    - [일대다 / hasMany](#one-to-many)
    - [일대다(역방향) / belongsTo](#one-to-many-inverse)
    - [여러 개 중 하나 / hasOne of Many](#has-one-of-many)
    - [중개 테이블을 통한 일대일 / hasOneThrough](#has-one-through)
    - [중개 테이블을 통한 일대다 / hasManyThrough](#has-many-through)
- [스코프 연관관계](#scoped-relationships)
- [다대다 연관관계](#many-to-many)
    - [중간 테이블 컬럼 가져오기](#retrieving-intermediate-table-columns)
    - [중간 테이블 컬럼으로 쿼리 필터링](#filtering-queries-via-intermediate-table-columns)
    - [중간 테이블 컬럼으로 쿼리 정렬](#ordering-queries-via-intermediate-table-columns)
    - [사용자 정의 중간 테이블 모델 정의](#defining-custom-intermediate-table-models)
- [다형성 연관관계](#polymorphic-relationships)
    - [일대일](#one-to-one-polymorphic-relations)
    - [일대다](#one-to-many-polymorphic-relations)
    - [여러 개 중 하나](#one-of-many-polymorphic-relations)
    - [다대다](#many-to-many-polymorphic-relations)
    - [사용자 정의 다형성 타입](#custom-polymorphic-types)
- [동적 연관관계](#dynamic-relationships)
- [연관관계 쿼리하기](#querying-relations)
    - [연관관계 메서드 vs. 동적 속성](#relationship-methods-vs-dynamic-properties)
    - [연관관계 존재 쿼리](#querying-relationship-existence)
    - [연관관계 부재 쿼리](#querying-relationship-absence)
    - [Morph To 연관관계 쿼리](#querying-morph-to-relationships)
- [연관 모델 집계하기](#aggregating-related-models)
    - [연관 모델 개수 세기](#counting-related-models)
    - [기타 집계 함수](#other-aggregate-functions)
    - [Morph To 연관관계의 연관 모델 개수 세기](#counting-related-models-on-morph-to-relationships)
- [즉시 로딩(Eager Loading)](#eager-loading)
    - [즉시 로딩 제약](#constraining-eager-loads)
    - [지연 즉시 로딩(Lazy Eager Loading)](#lazy-eager-loading)
    - [자동 즉시 로딩](#automatic-eager-loading)
    - [지연 로딩 방지](#preventing-lazy-loading)
- [연관 모델 삽입 및 수정](#inserting-and-updating-related-models)
    - [`save` 메서드](#the-save-method)
    - [`create` 메서드](#the-create-method)
    - [Belongs To 연관관계](#updating-belongs-to-relationships)
    - [다대다 연관관계](#updating-many-to-many-relationships)
- [부모 타임스탬프 갱신하기](#touching-parent-timestamps)

<a name="introduction"></a>
## 소개

데이터베이스 테이블은 대개 서로 연관되어 있습니다. 예를 들어, 하나의 블로그 포스트는 여러 개의 댓글을 가질 수 있고, 한 주문은 주문한 사용자와 연결될 수 있습니다. Eloquent는 이러한 연관관계를 쉽게 관리하고 사용할 수 있도록 하며, 다음과 같은 대표적인 연관관계 유형을 지원합니다:

<div class="content-list" markdown="1">

- [일대일](#one-to-one)
- [일대다](#one-to-many)
- [다대다](#many-to-many)
- [중개 테이블을 통한 일대일](#has-one-through)
- [중개 테이블을 통한 일대다](#has-many-through)
- [일대일(다형성)](#one-to-one-polymorphic-relations)
- [일대다(다형성)](#one-to-many-polymorphic-relations)
- [다대다(다형성)](#many-to-many-polymorphic-relations)

</div>

<a name="defining-relationships"></a>
## 연관관계 정의하기

Eloquent의 연관관계는 모델 클래스의 메서드로 정의합니다. 연관관계는 [쿼리 빌더](/docs/12.x/queries) 역할도 하므로, 메서드로 정의하면 다양한 체이닝과 쿼리 조건 추가가 가능합니다. 예를 들어, `posts` 연관관계에 추가 쿼리 조건을 체인해서 사용할 수 있습니다:

```php
$user->posts()->where('active', 1)->get();
```

연관관계를 실제로 사용하기 전에, Eloquent가 지원하는 각 연관관계 유형을 어떻게 정의하는지 배워봅시다.

<a name="one-to-one"></a>
### 일대일 / hasOne

일대일 연관관계는 가장 기본적인 데이터베이스 연관관계입니다. 예를 들어, `User` 모델이 하나의 `Phone` 모델과 연결될 수 있습니다. 이 관계를 정의하려면, `User` 모델에 `phone` 메서드를 추가하고, 이 메서드에서 `hasOne` 메서드를 호출하여 반환하면 됩니다. `hasOne` 메서드는 모델이 상속받는 `Illuminate\Database\Eloquent\Model` 클래스에서 사용할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasOne;

class User extends Model
{
    /**
     * 이 사용자와 연관된 전화번호를 가져옵니다.
     */
    public function phone(): HasOne
    {
        return $this->hasOne(Phone::class);
    }
}
```

`hasOne` 메서드의 첫 번째 인수는 연관된 모델 클래스명입니다. 연관관계를 정의하면, Eloquent의 동적 속성을 이용해 연관된 레코드를 바로 가져올 수 있습니다. 동적 속성은 마치 모델의 속성처럼 연관관계 메서드에 접근할 수 있게 해줍니다:

```php
$phone = User::find(1)->phone;
```

Eloquent는 연관관계의 외래 키를 부모 모델명에 따라 자동으로 결정합니다. 이 경우, `Phone` 모델에는 `user_id`라는 외래 키가 있다고 가정합니다. 만약 이 규칙을 오버라이드하고 싶다면, `hasOne` 메서드에 두 번째 인수로 외래 키를 지정할 수 있습니다:

```php
return $this->hasOne(Phone::class, 'foreign_key');
```

또한, Eloquent는 부모 모델의 기본 키 컬럼(`id`)이 외래 키의 값과 일치한다고 가정합니다. 즉, 사용자의 `id` 컬럼 값이 `Phone` 레코드의 `user_id` 컬럼에 들어가게 됩니다. 만약 기본 키나 `$primaryKey`가 `id`가 아니라면, 세 번째 인수로 로컬 키를 지정할 수 있습니다:

```php
return $this->hasOne(Phone::class, 'foreign_key', 'local_key');
```

<a name="one-to-one-defining-the-inverse-of-the-relationship"></a>
#### 관계의 역방향 정의하기

이제 `User` 모델에서 `Phone` 모델을 접근할 수 있습니다. 반대로, `Phone` 모델에서 해당 전화번호의 소유자를 접근하고 싶을 수도 있습니다. 이런 경우, `hasOne` 관계의 역방향인 `belongsTo` 메서드를 사용해서 정의할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Phone extends Model
{
    /**
     * 이 전화번호의 소유자인 사용자를 가져옵니다.
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }
}
```

`user` 메서드를 호출하면, Eloquent는 `Phone` 모델의 `user_id` 컬럼이 일치하는 `User` 모델을 찾게 됩니다.

Eloquent는 연관관계 메서드명을 참고하여 외래 키명을 결정합니다. 이 경우는 메서드명 뒤에 `_id`를 붙여서 `user_id` 컬럼을 예상합니다. 만약 실제 외래 키명이 다르다면, `belongsTo` 메서드의 두 번째 인수로 직접 지정할 수 있습니다:

```php
/**
 * 이 전화번호의 소유자인 사용자를 가져옵니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class, 'foreign_key');
}
```

부모 모델의 기본 키가 `id`가 아니거나, 다른 컬럼으로 연결하고 싶을 때는 세 번째 인수로 부모 테이블의 키명을 지정할 수 있습니다:

```php
/**
 * 이 전화번호의 소유자인 사용자를 가져옵니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class, 'foreign_key', 'owner_key');
}
```

<a name="one-to-many"></a>
### 일대다 / hasMany

일대다 연관관계는 한 모델이 하나 이상의 자식 모델을 소유하는 관계입니다. 예를 들어, 하나의 블로그 포스트는 무한히 많은 댓글을 가질 수 있습니다. 다른 Eloquent 연관관계와 마찬가지로, 메서드를 정의해 일대다 관계를 만들 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Post extends Model
{
    /**
     * 이 블로그 글의 댓글을 가져옵니다.
     */
    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class);
    }
}
```

Eloquent는 `Comment` 모델에 적절한 외래 키 컬럼을 자동으로 결정합니다. 보통 부모 모델명을 snake case로 변환해 `_id`를 붙입니다. 위 예시에서는 `Comment` 모델에 `post_id` 컬럼이 있다고 가정합니다.

연관관계 메서드를 정의하면, `comments` 속성을 통해 [컬렉션](/docs/12.x/eloquent-collections) 형태로 연관 댓글을 접근할 수 있습니다. 동적 속성 덕분에, 메서드가 아닌 속성처럼 접근할 수 있습니다:

```php
use App\Models\Post;

$comments = Post::find(1)->comments;

foreach ($comments as $comment) {
    // ...
}
```

연관관계도 쿼리 빌더이므로, 추가 쿼리 조건을 메서드 체이닝 형태로 붙일 수 있습니다:

```php
$comment = Post::find(1)->comments()
    ->where('title', 'foo')
    ->first();
```

`hasOne` 메서드와 마찬가지로, `hasMany`에 외래 키나 로컬 키를 인수로 넘겨 관례를 오버라이드할 수 있습니다:

```php
return $this->hasMany(Comment::class, 'foreign_key');

return $this->hasMany(Comment::class, 'foreign_key', 'local_key');
```

<a name="automatically-hydrating-parent-models-on-children"></a>
#### 자식 모델에서 부모 모델 자동 로딩하기

Eloquent 즉시 로딩을 하더라도, 자식 모델 루프를 돌면서 부모 모델을 접근할 때 "N + 1" 문제에 부딪힐 수 있습니다:

```php
$posts = Post::with('comments')->get();

foreach ($posts as $post) {
    foreach ($post->comments as $comment) {
        echo $comment->post->title;
    }
}
```

위 예시에서는 `Post` 모델마다 댓글을 즉시 로딩했지만, 각 `Comment` 모델에서 부모 `Post` 모델을 접근하면 추가 쿼리가 발생합니다. (N+1 문제)

이때 `hasMany` 관계 정의시 `chaperone` 메서드를 사용하면, 부모 모델도 자식에 자동으로 맵핑해줄 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Post extends Model
{
    /**
     * 이 블로그 글의 댓글을 가져옵니다.
     */
    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class)->chaperone();
    }
}
```

실행 시점에 자동으로 부모 로딩을 opt-in 하려면, 즉시 로딩시 `chaperone`을 지정할 수 있습니다:

```php
use App\Models\Post;

$posts = Post::with([
    'comments' => fn ($comments) => $comments->chaperone(),
])->get();
```

<a name="one-to-many-inverse"></a>
### 일대다(역방향) / belongsTo

포스트의 모든 댓글을 접근할 수 있게 되었으니, 이제 각각의 댓글이 어느 포스트에 속하는지 역방향 연관관계를 정의해봅시다. 자식 모델에서 `belongsTo` 메서드를 호출하면 일대다의 역방향 관계가 만들어집니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Comment extends Model
{
    /**
     * 이 댓글이 속한 포스트를 가져옵니다.
     */
    public function post(): BelongsTo
    {
        return $this->belongsTo(Post::class);
    }
}
```

정의 후에는 동적 속성으로 부모 포스트에 접근할 수 있습니다:

```php
use App\Models\Comment;

$comment = Comment::find(1);

return $comment->post->title;
```

Eloquent는 `Comment` 모델의 `post_id` 컬럼과 일치하는 `Post` 모델의 `id`를 찾아 관련 모델을 반환합니다.

외래 키에 대한 기본 규칙을 오버라이드하려면 두 번째 인수로, 부모 테이블의 키명을 지정하려면 세 번째 인수로 값을 넘겨줄 수 있습니다:

```php
/**
 * 이 댓글이 속한 포스트를 가져옵니다.
 */
public function post(): BelongsTo
{
    return $this->belongsTo(Post::class, 'foreign_key');
}

/**
 * 이 댓글이 속한 포스트를 가져옵니다.
 */
public function post(): BelongsTo
{
    return $this->belongsTo(Post::class, 'foreign_key', 'owner_key');
}
```

<a name="default-models"></a>
#### 기본 모델(Default Models) 지정

`belongsTo`, `hasOne`, `hasOneThrough`, `morphOne` 관계에서는, 연관관계가 `null`일 때 반환할 기본 모델을 지정할 수 있습니다. 이 패턴은 [Null Object pattern](https://en.wikipedia.org/wiki/Null_Object_pattern)이라고 하며, 조건문을 줄이는 데 유용합니다. 아래 예시는 사용자가 연결되지 않은 포스트에 대해 비어 있는 `App\Models\User` 모델을 반환합니다:

```php
/**
 * 이 포스트의 작성자를 가져옵니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault();
}
```

기본 모델에 속성값을 채워 반환하고 싶을 때는 배열이나 클로저를 `withDefault`에 전달할 수 있습니다:

```php
/**
 * 이 포스트의 작성자를 가져옵니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault([
        'name' => 'Guest Author',
    ]);
}

/**
 * 이 포스트의 작성자를 가져옵니다.
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

"belongsTo" 관계 자식의 목록을 조회할 때, 직접 `where` 조건을 작성할 수도 있습니다:

```php
use App\Models\Post;

$posts = Post::where('user_id', $user->id)->get();
```

하지만 더 간편하게 `whereBelongsTo` 메서드를 사용하면, 적절한 관계/외래 키를 자동으로 결정하여 쿼리를 만들어줍니다:

```php
$posts = Post::whereBelongsTo($user)->get();
```

[컬렉션](/docs/12.x/eloquent-collections) 객체도 사용할 수 있어서, 컬렉션에 속한 여러 부모의 자식들을 모두 조회할 수도 있습니다:

```php
$users = User::where('vip', true)->get();

$posts = Post::whereBelongsTo($users)->get();
```

원하는 경우, 두 번째 인수로 관계명을 명시적으로 지정할 수도 있습니다:

```php
$posts = Post::whereBelongsTo($user, 'author')->get();
```

<a name="has-one-of-many"></a>
### 여러 개 중 하나(Has One of Many)

때로는 다수의 연관된 모델 중 "최신" 또는 "최고" 하나만 간단히 가져오고 싶을 때가 있습니다. 예를 들어, `User` 모델이 여러 개의 `Order`와 연관될 수 있지만, 사용자가 최근 주문한 내역만 쉽게 가져오고 싶을 때 사용할 수 있습니다. `hasOne` 관계와 `ofMany` 계열 메서드를 조합해 만들 수 있습니다:

```php
/**
 * 사용자의 최근 주문을 가져옵니다.
 */
public function latestOrder(): HasOne
{
    return $this->hasOne(Order::class)->latestOfMany();
}
```

반대로 "가장 오래된" (즉, 첫 번째) 연관 모델을 가져오고 싶다면:

```php
/**
 * 사용자의 가장 오래된 주문을 가져옵니다.
 */
public function oldestOrder(): HasOne
{
    return $this->hasOne(Order::class)->oldestOfMany();
}
```

기본적으로 `latestOfMany`와 `oldestOfMany`는 모델의 기본 키로 최신/오래된 레코드를 가져옵니다. 다른 정렬 기준이 필요하다면, `ofMany` 메서드를 사용하여 원하는 컬럼명과 집계 함수를 지정할 수 있습니다(예: 가장 비싼 주문):

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
> PostgreSQL은 UUID 컬럼에 대해 `MAX` 함수를 지원하지 않으므로, PostgreSQL UUID 컬럼과 one-of-many 관계를 함께 사용할 수 없습니다.

<a name="converting-many-relationships-to-has-one-relationships"></a>
#### "Many" 관계를 Has One 관계로 변환하기

이미 "has many" 관계를 정의해두고, `latestOfMany`, `oldestOfMany`, `ofMany` 계열 메서드로 한 개만 가져오고 싶을 때는, `one` 메서드를 체인하여 "has one" 관계로 간편하게 변환할 수 있습니다:

```php
/**
 * 사용자의 모든 주문을 반환합니다.
 */
public function orders(): HasMany
{
    return $this->hasMany(Order::class);
}

/**
 * 사용자의 최고가 주문을 반환합니다.
 */
public function largestOrder(): HasOne
{
    return $this->orders()->one()->ofMany('price', 'max');
}
```

`HasManyThrough`를 `HasOneThrough`로 변환할 수도 있습니다:

```php
public function latestDeployment(): HasOneThrough
{
    return $this->deployments()->one()->latestOfMany();
}
```

<a name="advanced-has-one-of-many-relationships"></a>
#### 고급 Has One of Many 관계

더 복잡한 상황에서도 "has one of many" 관계를 만들 수 있습니다. 예를 들어, `Product` 모델이 여러 가격정보(`Price`)와 연관되고, 미래 날짜로 발행 예정인 가격정보가 있을 경우입니다.

예를 들어, 가장 최신에 발행되었지만 아직 미래가 아닌(priced_at < now()) 가격의 가격정보 중, 발행일이 같다면 ID가 가장 큰 것을 선택하고자 할 때는 `ofMany`에 정렬할 컬럼 배열과, 추가 제약조건을 거는 클로저를 함께 사용합니다:

```php
/**
 * 이 상품의 현재 가격을 가져옵니다.
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
### 중개 테이블을 통한 일대일(Has One Through)

"has-one-through" 관계는 두 모델 간에 직접 관계는 없지만, 중간 모델을 통해 일대일 관계를 설정하는 경우 사용됩니다.

예를 들어, 차량 정비소 애플리케이션에서, 각 `Mechanic`(정비공)은 한 대의 `Car`(차량)를, 각 차량은 한 명의 `Owner`(소유주)를 가지도록 구성할 수 있습니다. 즉, 정비공과 소유주는 데이터베이스상 직접 연결되어 있지 않지만, 정비공은 해당 차량을 통해 소유주에 접근할 수 있습니다. 아래 테이블 구조를 참고하세요:

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

이제 `Mechanic` 모델에 관계를 정의해봅시다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasOneThrough;

class Mechanic extends Model
{
    /**
     * 차량의 소유주를 가져옵니다.
     */
    public function carOwner(): HasOneThrough
    {
        return $this->hasOneThrough(Owner::class, Car::class);
    }
}
```

`hasOneThrough`의 첫 번째 인수는 도달하고자 하는 최종 모델, 두 번째 인수는 중간 모델입니다.

이미 모든 모델에 개별 연관관계를 정의해 둔 경우라면, `through` 메서드로 다음과 같이 더 간결하게 정의할 수 있습니다:

```php
// 문자열 기반
return $this->through('cars')->has('owner');

// 동적 방식
return $this->throughCars()->hasOwner();
```

<a name="has-one-through-key-conventions"></a>
#### 키 규칙

쿼리를 수행할 때는 일반적인 Eloquent 외래 키 규칙이 적용됩니다. 직접 키를 지정하려면, `hasOneThrough` 메서드의 3~6번째 인수로 순서대로 지정하면 됩니다: 3번째(중간 모델의 외래 키), 4번째(최종 모델의 외래 키), 5번째(로컬 키), 6번째(중간 모델의 로컬 키):

```php
class Mechanic extends Model
{
    /**
     * 차량의 소유주를 가져옵니다.
     */
    public function carOwner(): HasOneThrough
    {
        return $this->hasOneThrough(
            Owner::class,
            Car::class,
            'mechanic_id', // cars 테이블의 외래 키
            'car_id', // owners 테이블의 외래 키
            'id', // mechanics 테이블의 기본 키
            'id' // cars 테이블의 기본 키
        );
    }
}
```

또는 개별 연관관계를 이미 구성해 둔 경우라면, `through` 메서드 문법을 재사용할 수 있습니다:

```php
// 문자열 기반
return $this->through('cars')->has('owner');

// 동적 방식
return $this->throughCars()->hasOwner();
```

<a name="has-many-through"></a>
### 중개 테이블을 통한 일대다(Has Many Through)

"has-many-through" 관계는 중간 관계를 통해 멀리 떨어진 모델을 편리하게 접근할 수 있도록 해줍니다. 예를 들어, [Laravel Cloud](https://cloud.laravel.com)와 같은 배포 플랫폼을 만든다고 할 때, `Application`(애플리케이션) 모델은 중간 모델인 `Environment`(환경) 모델을 거쳐 여러 `Deployment`(배포)를 가질 수 있습니다. 예시 테이블 구조는 다음과 같습니다:

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

`Application` 모델에 아래와 같이 관계를 정의할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasManyThrough;

class Application extends Model
{
    /**
     * 애플리케이션의 모든 배포 이력을 반환합니다.
     */
    public function deployments(): HasManyThrough
    {
        return $this->hasManyThrough(Deployment::class, Environment::class);
    }
}
```

첫 번째 인수는 최종 접근 모델, 두 번째는 중간 모델입니다.

이미 개별 연관관계를 준비해둔 상황이라면, 아래처럼 간단하게 정의 가능합니다:

```php
// 문자열 기반
return $this->through('environments')->has('deployments');

// 동적 방식
return $this->throughEnvironments()->hasDeployments();
```

`deployments` 테이블에는 `application_id`가 없어도, 중간의 `environments.application_id`를 기준으로 배포 목록을 가져올 수 있다는 점이 특징입니다.

<a name="has-many-through-key-conventions"></a>
#### 키 규칙

키 지정이 필요하다면, `hasManyThrough` 메서드에도 3~6번째 인수로 지정할 수 있습니다:

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
            'id', // applications 테이블의 기본 키
            'id' // environments 테이블의 기본 키
        );
    }
}
```

이미 연관관계를 정의해 둔 경우엔, `through` 메서드 방식으로 기존 규칙을 재활용할 수 있습니다:

```php
// 문자열 기반
return $this->through('environments')->has('deployments');

// 동적 방식
return $this->throughEnvironments()->hasDeployments();
```

<a name="scoped-relationships"></a>
### 스코프 연관관계(Scoped Relationships)

관계에 제약조건을 거는 추가 메서드를 자주 모델에 작성하게 됩니다. 예를 들어, `User` 모델에 `featuredPosts` 메서드를 추가하여 `posts` 관계에 where 조건을 추가할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class User extends Model
{
    /**
     * 사용자의 포스트를 반환합니다.
     */
    public function posts(): HasMany
    {
        return $this->hasMany(Post::class)->latest();
    }

    /**
     * 사용자의 주요(Featured) 포스트를 반환합니다.
     */
    public function featuredPosts(): HasMany
    {
        return $this->posts()->where('featured', true);
    }
}
```

이런 상황에서 `featuredPosts`로 모델을 생성하면, 기본적으로 `featured` 속성이 true로 설정되어 있진 않습니다. 관계 메서드를 통한 생성 시, 자동으로 추가 속성을 모두 지정해주고 싶으면 `withAttributes` 메서드를 사용할 수 있습니다:

```php
/**
 * 사용자의 주요 포스트를 반환합니다.
 */
public function featuredPosts(): HasMany
{
    return $this->posts()->withAttributes(['featured' => true]);
}
```

`withAttributes`는 해당 attributes로 where 조건도 추가하고, 메서드를 통한 모델 생성 시 attributes도 자동으로 포함합니다:

```php
$post = $user->featuredPosts()->create(['title' => 'Featured Post']);

$post->featured; // true
```

where 조건을 쿼리에 추가하지 않으려면, `asConditions` 인수를 false로 지정할 수 있습니다:

```php
return $this->posts()->withAttributes(['featured' => true], asConditions: false);
```

<a name="many-to-many"></a>
## 다대다 연관관계(Many to Many Relationships)

다대다 연관관계는 `hasOne`, `hasMany`보다 조금 복잡한 구조입니다. 예를 들어, 한 명의 사용자가 여러 역할(Role)을 가질 수 있고, 각 역할은 여러 사용자와 공유될 수 있습니다. 즉, 사용자와 역할이 서로 다대다(Many to Many) 관계입니다.

<a name="many-to-many-table-structure"></a>
#### 테이블 구조

이 관계를 정의하려면 `users`, `roles`, `role_user` 3개의 테이블이 필요합니다. `role_user`는 관련 모델명을 알파벳 순으로 조합한 중간 테이블명으로, `user_id`와 `role_id` 컬럼을 가집니다. 이 테이블이 사용자와 역할의 연결 고리로 사용됩니다.

단순히 `roles`에 `user_id`를 두는 경우, 한 역할이 단 하나의 사용자에게만 속할 수 있으므로, 다대다에서는 별도 중간 테이블이 반드시 필요합니다.

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

다대다 연관관계 정의는 `belongsToMany` 메서드를 반환하는 메서드를 작성해 구현합니다. 이 메서드는 모든 Eloquent 모델의 부모 클래스인 `Illuminate\Database\Eloquent\Model`에서 제공됩니다. `User` 모델에 아래처럼 `roles` 메서드를 정의해보세요:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class User extends Model
{
    /**
     * 이 사용자에게 속한 역할들.
     */
    public function roles(): BelongsToMany
    {
        return $this->belongsToMany(Role::class);
    }
}
```

이렇게 정의한 후, 동적 속성으로 `roles`에 접근하여 사용자의 역할 목록을 얻을 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

foreach ($user->roles as $role) {
    // ...
}
```

관계도 쿼리 빌더이므로, 쿼리 체이닝도 자유롭게 가능합니다:

```php
$roles = User::find(1)->roles()->orderBy('name')->get();
```

중간 테이블명은 연관된 모델명을 알파벳순으로 조합합니다. 이 규칙을 변경하고 싶다면 두 번째 인수로 테이블명을 직접 지정할 수 있습니다:

```php
return $this->belongsToMany(Role::class, 'role_user');
```

키 이름 또한 세 번째, 네 번째 인수를 통해 직접 지정 가능합니다:

```php
return $this->belongsToMany(Role::class, 'role_user', 'user_id', 'role_id');
```

<a name="many-to-many-defining-the-inverse-of-the-relationship"></a>
#### 관계의 역방향 정의

다대다의 "역방향" 관계도 마찬가지로 `belongsToMany` 메서드로 정의할 수 있습니다. 예시에서는 `Role` 모델에 `users` 메서드를 아래와 같이 추가합니다:

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

`User` 모델과 방법이 동일하며, 모든 테이블명 및 키명 커스터마이즈 옵션도 동일하게 적용됩니다.

<a name="retrieving-intermediate-table-columns"></a>
### 중간 테이블 컬럼 가져오기

다대다 관계에서 중간 테이블의 추가 정보를 활용해야 할 때가 많습니다. 예를 들어, 사용자와 역할 관계에서, 중간 테이블의 컬럼에 접근하려면 각 모델의 `pivot` 속성을 사용합니다:

```php
use App\Models\User;

$user = User::find(1);

foreach ($user->roles as $role) {
    echo $role->pivot->created_at;
}
```

기본적으로 중간 테이블의 연결 키만 `pivot`에 할당됩니다. 컬럼을 더 가져오고 싶다면, 관계 정의할 때 `withPivot` 메서드에 컬럼명을 지정합니다:

```php
return $this->belongsToMany(Role::class)->withPivot('active', 'created_by');
```

중간 테이블에도 `created_at`, `updated_at` 타임스탬프를 자동 관리하고 싶다면, `withTimestamps` 메서드를 사용합니다:

```php
return $this->belongsToMany(Role::class)->withTimestamps();
```

> [!WARNING]
> Eloquent의 자동 타임스탬프를 사용하는 중간 테이블에는 `created_at`과 `updated_at` 컬럼이 모두 존재해야 합니다.

<a name="customizing-the-pivot-attribute-name"></a>
#### `pivot` 속성명 변경하기

중간 테이블에서 가져온 속성이 항상 `pivot`이라는 이름으로 접근되지만, 더 의미 있는 이름이 필요하다면 `as` 메서드로 커스텀할 수 있습니다.

예를 들어, 팟캐스트 구독하는 사용자가 있을 때 `subscription` 등으로 이름을 변경해보세요:

```php
return $this->belongsToMany(Podcast::class)
    ->as('subscription')
    ->withTimestamps();
```

지정한 이름으로 속성에 접근할 수 있습니다:

```php
$users = User::with('podcasts')->get();

foreach ($users->flatMap->podcasts as $podcast) {
    echo $podcast->subscription->created_at;
}
```

<a name="filtering-queries-via-intermediate-table-columns"></a>
### 중간 테이블 컬럼으로 쿼리 필터링

`wherePivot`, `wherePivotIn`, `wherePivotNotIn`, `wherePivotBetween`, `wherePivotNotBetween`, `wherePivotNull`, `wherePivotNotNull` 메서드를 사용해 중간 테이블 컬럼 기준으로 쿼리 결과를 필터링할 수 있습니다:

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

`wherePivot`은 쿼리에만 조건을 추가하고, 모델 생성 시 해당 값이 자동 추가되지 않습니다. 쿼리와 생성 둘 다 지정하려면 `withPivotValue`를 사용하세요:

```php
return $this->belongsToMany(Role::class)
    ->withPivotValue('approved', 1);
```

<a name="ordering-queries-via-intermediate-table-columns"></a>
### 중간 테이블 컬럼으로 쿼리 정렬

`orderByPivot` 메서드를 사용해, 중간 테이블 컬럼 기준으로 정렬할 수 있습니다. 아래는 사용자의 최신 뱃지를 정렬해서 가져오는 예시입니다:

```php
return $this->belongsToMany(Badge::class)
    ->where('rank', 'gold')
    ->orderByPivot('created_at', 'desc');
```

<a name="defining-custom-intermediate-table-models"></a>
### 사용자 정의 중간 테이블 모델 정의

중간 테이블에 모델을 직접 정의하여 추가 로직(예: 메서드, casts)을 구현할 수 있습니다. 이때 `using` 메서드로 사용자 정의 피벗 모델을 지정합니다.

커스텀 피벗 모델은 반드시 `Illuminate\Database\Eloquent\Relations\Pivot`(일반 다대다) 또는 `Illuminate\Database\Eloquent\Relations\MorphPivot`(다형성 다대다)을 확장해야 합니다.

예를 들어, 커스텀 `RoleUser` 피벗 모델을 사용하는 예시:

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

커스텀 피벗 모델 예시:

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
> 피벗 모델에서는 `SoftDeletes` 트레이트를 사용할 수 없습니다. 피벗에 soft delete 기능이 필요하다면, 피벗을 실제 Eloquent 모델로 전환하세요.

<a name="custom-pivot-models-and-incrementing-ids"></a>
#### 커스텀 피벗 모델과 자동증가 ID

자동증가(primary key)를 사용하는 피벗 모델이 있다면, 커스텀 피벗 모델 클래스에 `$incrementing = true` 속성을 반드시 정의하세요.

```php
/**
 * ID가 자동 증가하는지 여부.
 *
 * @var bool
 */
public $incrementing = true;
```

<a name="polymorphic-relationships"></a>
## 다형성 연관관계(Polymorphic Relationships)

다형성 연관관계는 하나의 자식 모델이 여러 종류의 부모 모델에 속할 수 있도록 해줍니다. 예를 들어, 사용자들이 블로그 글이나 비디오를 공유하는 애플리케이션에서, `Comment` 모델이 `Post`와 `Video` 양쪽 모두에 속할 수 있습니다.

<a name="one-to-one-polymorphic-relations"></a>
### 일대일(다형성)

<a name="one-to-one-polymorphic-table-structure"></a>
#### 테이블 구조

일대일 다형성 관계는, 한 자식 모델이 다양한 부모 모델에 속할 수 있게 합니다. 예를 들어, 블로그 `Post`와 `User` 모두가 하나의 `Image` 모델과 다형성 관계를 맺을 수 있습니다. 관련 테이블 구조는 아래와 같습니다:

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

`images` 테이블의 `imageable_id`에는 소유한 post나 user의 ID가, `imageable_type`에는 부모 모델의 클래스명이 들어갑니다(Eloquent는 이 컬럼을 통해 구체적인 부모 모델 타입을 구분합니다).

<a name="one-to-one-polymorphic-model-structure"></a>
#### 모델 구조

아래는 이 관계를 위해 필요한 모델 정의 예시입니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class Image extends Model
{
    /**
     * 이미지의 소유 모델(user 또는 post)을 반환합니다.
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
     * 포스트의 이미지를 반환합니다.
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
     * 사용자의 이미지를 반환합니다.
     */
    public function image(): MorphOne
    {
        return $this->morphOne(Image::class, 'imageable');
    }
}
```

<a name="one-to-one-polymorphic-retrieving-the-relationship"></a>
#### 연관관계 조회

데이터베이스와 모델이 준비되었으면, 아래와 같이 다양한 방식으로 관계에 접근할 수 있습니다:

```php
use App\Models\Post;

$post = Post::find(1);

$image = $post->image;
```

다형성 자식 모델에서 부모를 조회하려면, `morphTo`를 호출하는 메서드명과 동일한 동적 속성으로 접근하세요:

```php
use App\Models\Image;

$image = Image::find(1);

$imageable = $image->imageable;
```

`imageable` 관계는 `Post` 또는 `User` 인스턴스를 반환하게 됩니다.

<a name="morph-one-to-one-key-conventions"></a>
#### 키 규칙

필요하다면 다형성 자식 모델이 사용하는 "id"와 "type" 컬럼 이름을 직접 지정할 수 있습니다. 항상 메서드명을 첫 번째 인수로 넘겨야 하며, 일반적으로 이 값은 메서드명과 동일하게 `__FUNCTION__` 상수로 지정합니다:

```php
/**
 * 이미지를 소유한 모델을 가져옵니다.
 */
public function imageable(): MorphTo
{
    return $this->morphTo(__FUNCTION__, 'imageable_type', 'imageable_id');
}
```

<a name="one-to-many-polymorphic-relations"></a>
### 일대다(다형성)

<a name="one-to-many-polymorphic-table-structure"></a>
#### 테이블 구조

일대다 다형성은 한 자식 모델이 다양한 부모 모델에 속할 수 있는 관계로, 하나의 `comments` 테이블로 여러 모델(Post, Video 등)의 댓글을 모두 저장할 수 있게 해줍니다. 예시 구조입니다:

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

다형성 일대다의 예시 모델입니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class Comment extends Model
{
    /**
     * 댓글의 소유 모델(post 또는 video)을 반환합니다.
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
     * 포스트의 모든 댓글을 반환합니다.
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
     * 비디오의 모든 댓글을 반환합니다.
     */
    public function comments(): MorphMany
    {
        return $this->morphMany(Comment::class, 'commentable');
    }
}
```

<a name="one-to-many-polymorphic-retrieving-the-relationship"></a>
#### 연관관계 조회

이제 동적 속성으로 모든 댓글에 접근할 수 있습니다:

```php
use App\Models\Post;

$post = Post::find(1);

foreach ($post->comments as $comment) {
    // ...
}
```

자식 모델에서 부모에 접근하고자 할 때는, 해당 `morphTo`를 호출하는 메서드명에 동적 속성으로 접근하세요:

```php
use App\Models\Comment;

$comment = Comment::find(1);

$commentable = $comment->commentable;
```

`commentable` 속성은 해당 댓글이 Post/Video 어느 것에 속하든 맞는 부모 인스턴스를 반환합니다.

<a name="polymorphic-automatically-hydrating-parent-models-on-children"></a>
#### 자식 모델에서 부모 모델 자동 로딩하기

Eloquent 즉시 로딩을 하더라도, 자식 모델에서 부모 모델을 접근할 때 N + 1 문제가 발생할 수 있습니다:

```php
$posts = Post::with('comments')->get();

foreach ($posts as $post) {
    foreach ($post->comments as $comment) {
        echo $comment->commentable->title;
    }
}
```

이럴 때, 다형성 관계에서도 `chaperone` 메서드를 사용해 자동으로 부모를 로딩할 수 있습니다:

```php
class Post extends Model
{
    /**
     * 포스트의 모든 댓글을 반환합니다.
     */
    public function comments(): MorphMany
    {
        return $this->morphMany(Comment::class, 'commentable')->chaperone();
    }
}
```

즉시 로딩 시점에 지정하려면 다음과 같이 사용합니다:

```php
use App\Models\Post;

$posts = Post::with([
    'comments' => fn ($comments) => $comments->chaperone(),
])->get();
```

<a name="one-of-many-polymorphic-relations"></a>
### 여러 개 중 하나(다형성 One of Many)

다형성 관계에서도, 여러 자식 중 "최신" 또는 "최고" 하나만 가져올 수 있습니다. 예를 들면, `User`가 여러 `Image`와 연관되어 있지만 가장 최근 이미지만 쉽게 가져올 수 있습니다:

```php
/**
 * 사용자의 가장 최근 이미지를 반환합니다.
 */
public function latestImage(): MorphOne
{
    return $this->morphOne(Image::class, 'imageable')->latestOfMany();
}
```

반대로 "가장 오래된" 이미지를 가져오고 싶다면:

```php
/**
 * 사용자의 가장 오래된 이미지를 반환합니다.
 */
public function oldestImage(): MorphOne
{
    return $this->morphOne(Image::class, 'imageable')->oldestOfMany();
}
```

정렬 기준을 커스터마이즈하려면 `ofMany` 메서드를 활용하세요:

```php
/**
 * 사용자의 최고 인기 이미지를 반환합니다.
 */
public function bestImage(): MorphOne
{
    return $this->morphOne(Image::class, 'imageable')->ofMany('likes', 'max');
}
```

> [!NOTE]
> 더 복잡한 "one of many" 관계를 만들 수도 있습니다. 자세한 내용은 [has one of many 문서](#advanced-has-one-of-many-relationships)를 참고하세요.

<a name="many-to-many-polymorphic-relations"></a>
### 다대다(다형성)

<a name="many-to-many-polymorphic-table-structure"></a>
#### 테이블 구조

다대다 다형성 관계는 "morph one", "morph many"보다 조금 더 복잡합니다. 예를 들어, `Post`와 `Video` 모델이 모두 `Tag`와 다대다 관계를 가질 때 사용할 수 있습니다. 이 구조를 사용하면 단일 tags 테이블에서 모든 모델에 태깅할 수 있습니다:

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
> 다형성 다대다 관계를 본격적으로 배우기 전, [일반 다대다 연관관계](#many-to-many) 문서를 참고하면 좋습니다.

<a name="many-to-many-polymorphic-model-structure"></a>
#### 모델 구조

다대다 다형성 멤버 모델(Post, Video 등)에선 `morphToMany` 메서드를 사용해 관계를 정의합니다. 중간 테이블명과 키 구조에 따라, 관계명으로 "taggable"을 사용합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphToMany;

class Post extends Model
{
    /**
     * 포스트에 달린 모든 태그를 반환합니다.
     */
    public function tags(): MorphToMany
    {
        return $this->morphToMany(Tag::class, 'taggable');
    }
}
```

<a name="many-to-many-polymorphic-defining-the-inverse-of-the-relationship"></a>
#### 관계의 역방향 정의

`Tag` 모델에는 각 부모 모델마다(`posts`, `videos` 등) `morphedByMany` 메서드를 추가해야 합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphToMany;

class Tag extends Model
{
    /**
     * 이 태그가 달린 모든 포스트를 반환합니다.
     */
    public function posts(): MorphToMany
    {
        return $this->morphedByMany(Post::class, 'taggable');
    }

    /**
     * 이 태그가 달린 모든 비디오를 반환합니다.
     */
    public function videos(): MorphToMany
    {
        return $this->morphedByMany(Video::class, 'taggable');
    }
}
```

<a name="many-to-many-polymorphic-retrieving-the-relationship"></a>
#### 연관관계 조회

정의 후에는 동적 속성으로 연관 태그/부모에 접근할 수 있습니다:

```php
use App\Models\Post;

$post = Post::find(1);

foreach ($post->tags as $tag) {
    // ...
}
```

다형성 자식 모델에서 부모에 접근하려면, 해당 `morphedByMany`를 호출하는 메서드명에 동적 속성으로 접근하세요:

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
### 사용자 정의 다형성 타입(Custom Polymorphic Types)

Laravel은 기본적으로 부모 모델의 "type" 정보를 저장할 때, 완전한 클래스명을 사용합니다. 예를 들어 위 예시에서 `commentable_type` 컬럼에는 `App\Models\Post` 또는 `App\Models\Video`가 들어갑니다. 그러나 내부 구조에 얽매이지 않고 타입값을 간략화하고 싶을 때, morph map 기능을 사용할 수 있습니다.

예를 들어 "post"와 "video"처럼 간단한 문자열을 사용하도록 구성하면, 모델명을 바꿔도 데이터베이스 타입값을 유지할 수 있게 됩니다:

```php
use Illuminate\Database\Eloquent\Relations\Relation;

Relation::enforceMorphMap([
    'post' => 'App\Models\Post',
    'video' => 'App\Models\Video',
]);
```

이 코드는 `App\Providers\AppServiceProvider`의 `boot`에서 호출하거나 별도의 서비스 프로바이더에서 적용할 수 있습니다.

런타임에 morph alias를 얻거나, alias로부터 클래스명을 역으로 얻으려면 아래 메서드를 활용할 수 있습니다:

```php
use Illuminate\Database\Eloquent\Relations\Relation;

$alias = $post->getMorphClass();

$class = Relation::getMorphedModel($alias);
```

> [!WARNING]
> 이미 morph map을 기존 애플리케이션에 추가한다면, 데이터베이스의 모든 morphable `*_type` 값도 일치하는 맵 이름으로 변환해주어야 합니다.

<a name="dynamic-relationships"></a>
### 동적 연관관계(Dynamic Relationships)

`resolveRelationUsing` 메서드를 통해 런타임에 Eloquent 모델 간 관계를 정의할 수 있습니다. 이는 일반적 개발보다는 패키지 개발 등에 주로 사용됩니다.

첫 번째 인수는 관계명, 두 번째는 모델 인스턴스를 받아 관계를 반환하는 클로저입니다. 보통 [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에서 작성합니다:

```php
use App\Models\Order;
use App\Models\Customer;

Order::resolveRelationUsing('customer', function (Order $orderModel) {
    return $orderModel->belongsTo(Customer::class, 'customer_id');
});
```

> [!WARNING]
> 동적 관계 정의 시, Eloquent 연관관계 메서드에 key명을 반드시 명시적으로 넘겨야 합니다.

<a name="querying-relations"></a>
## 연관관계 쿼리하기

Eloquent의 모든 연관관계는 메서드로 정의되어 있으므로, 해당 메서드를 직접 호출해 쿼리가 실행되기 전 관계 인스턴스를 얻을 수 있습니다. 모든 연관관계는 또한 [쿼리 빌더](/docs/12.x/queries)의 역할을 하므로, 다양한 제약조건을 붙인 후 원하는 시점에 최종 쿼리를 실행할 수 있습니다.

예를 들어, `User`와 `Post` 연관관계에서 추가 조건을 체이닝할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

$user->posts()->where('active', 1)->get();
```

Laravel [쿼리 빌더](/docs/12.x/queries)의 모든 메서드를 활용 가능하니, 관련 문서도 참고해보세요.

<a name="chaining-orwhere-clauses-after-relationships"></a>
#### 관계 쿼리 후 `orWhere` 체이닝 주의

연관관계 쿼리에 `orWhere`을 추가하면, 관계 제약과 같은 그룹에 조건이 묶이므로 쿼리 결과가 엉뚱해질 수 있습니다:

```php
$user->posts()
    ->where('active', 1)
    ->orWhere('votes', '>=', 100)
    ->get();
```

위 코드는 다음과 같은 SQL을 생성합니다:

```sql
select *
from posts
where user_id = ? and active = 1 or votes >= 100
```

따라서, 논리 그룹을 명시적으로 묶어야 원하는 결과를 얻을 수 있습니다:

```php
use Illuminate\Database\Eloquent\Builder;

$user->posts()
    ->where(function (Builder $query) {
        return $query->where('active', 1)
            ->orWhere('votes', '>=', 100);
    })
    ->get();
```

이렇게 하면 쿼리가 정확히 원하는 대로 묶입니다:

```sql
select *
from posts
where user_id = ? and (active = 1 or votes >= 100)
```

<a name="relationship-methods-vs-dynamic-properties"></a>
### 연관관계 메서드 vs. 동적 속성

추가 쿼리 제약이 필요하지 않다면, 동적 속성으로 바로 접근하는 것이 편리합니다:

```php
use App\Models\User;

$user = User::find(1);

foreach ($user->posts as $post) {
    // ...
}
```

동적 속성을 이용하면 "지연 로딩(lazy loading)"이 일어납니다. 즉, 실제로 속성에 접근할 때 쿼리가 실행됩니다. 이런 이유로 [즉시 로딩](#eager-loading)을 사용하면 쿼리 수를 줄일 수 있습니다.

<a name="querying-relationship-existence"></a>
### 연관관계 존재 쿼리

모델 조회시, 관계가 존재하는지 조건을 추가하고 싶은 경우가 많습니다. 예를 들어, 댓글이 단 하나라도 있는 포스트만 조회하려면 `has` 또는 `orHas` 메서드에 관계명을 넘겨 사용합니다:

```php
use App\Models\Post;

// 댓글이 1개 이상인 포스트 모두 조회
$posts = Post::has('comments')->get();
```

연관관계 개수 및 조건을 추가할 수도 있습니다:

```php
// 댓글이 3개 이상인 포스트
$posts = Post::has('comments', '>=', 3)->get();
```

중첩 관계는 "점(.)" 표기법으로 사용할 수 있습니다:

```php
// 댓글에 이미지가 하나라도 달린 포스트 조회
$posts = Post::has('comments.images')->get();
```

더 복잡한 제약조건은 `whereHas`, `orWhereHas` 메서드로 쿼리 빌더처럼 사용할 수 있습니다:

```php
use Illuminate\Database\Eloquent\Builder;

// 댓글 내용이 code%로 시작하는 경우
$posts = Post::whereHas('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
})->get();

// 최소 10개 이상의 code% 댓글이 달린 포스트
$posts = Post::whereHas('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
}, '>=', 10)->get();
```

> [!WARNING]
> Eloquent에서는 데이터베이스가 다를 경우 연관관계 존재 쿼리를 지원하지 않습니다. 반드시 같은 데이터베이스 내에서만 가능합니다.

<a name="many-to-many-relationship-existence-queries"></a>
#### 다대다 관계 존재 쿼리

`whereAttachedTo` 메서드는 다대다 연관관계가 존재하는(즉, 중간 테이블로 연결된) 모델만 조회할 때 사용할 수 있습니다:

```php
$users = User::whereAttachedTo($role)->get();
```

[컬렉션](/docs/12.x/eloquent-collections)을 넘기면, 그 중 하나라도 연관관계를 가지는 모델 전부를 조회할 수 있습니다:

```php
$tags = Tag::whereLike('name', '%laravel%')->get();

$posts = Post::whereAttachedTo($tags)->get();
```

<a name="inline-relationship-existence-queries"></a>
#### 인라인 연관관계 존재 쿼리

단일 where 조건으로 관계 존재여부를 쉽게 체크할 땐, `whereRelation`, `orWhereRelation`, `whereMorphRelation`, `orWhereMorphRelation` 계열 메서드가 편리합니다:

```php
use App\Models\Post;

$posts = Post::whereRelation('comments', 'is_approved', false)->get();
```

연산자도 자유롭게 쓸 수 있습니다:

```php
$posts = Post::whereRelation(
    'comments', 'created_at', '>=', now()->minus(hours: 1)
)->get();
```

<a name="querying-relationship-absence"></a>
### 연관관계 부재 쿼리

관계가 없는(댓글이 하나도 없는 포스트 등) 기록을 조회하려면, `doesntHave`, `orDoesntHave` 메서드를 사용하세요:

```php
use App\Models\Post;

$posts = Post::doesntHave('comments')->get();
```

더 복잡한 제약이 필요하면, `whereDoesntHave`, `orWhereDoesntHave`를 사용하면 됩니다:

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::whereDoesntHave('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
})->get();
```

중첩 관계(점(.) 표기법)도 지원합니다:

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::whereDoesntHave('comments.author', function (Builder $query) {
    $query->where('banned', 1);
})->get();
```

<a name="querying-morph-to-relationships"></a>
### Morph To 연관관계 쿼리

"morph to" 연관관계의 존재/부존재를 쿼리하려면, `whereHasMorph`와 `whereDoesntHaveMorph` 메서드를 사용하면 됩니다. 첫 번째 인수는 관계명, 두 번째는 모델명 배열, 세 번째는 쿼리 빌더 클로저입니다:

```php
use App\Models\Comment;
use App\Models\Post;
use App\Models\Video;
use Illuminate\Database\Eloquent\Builder;

// 제목이 code%로 시작하는 포스트/비디오에 달린 댓글 조회
$comments = Comment::whereHasMorph(
    'commentable',
    [Post::class, Video::class],
    function (Builder $query) {
        $query->where('title', 'like', 'code%');
    }
)->get();

// 제목이 code%로 시작하지 않는 포스트에 달린 댓글 조회
$comments = Comment::whereDoesntHaveMorph(
    'commentable',
    Post::class,
    function (Builder $query) {
        $query->where('title', 'like', 'code%');
    }
)->get();
```

클로저의 두 번째 인수 `$type`을 사용하면, 폴리모픽 타입별로 쿼리 조건을 커스터마이즈할 수도 있습니다:

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

때로는 "morph to" 관계의 부모의 자식만 쿼리하고 싶을 수 있습니다. `whereMorphedTo`, `whereNotMorphedTo` 메서드를 이용하면 편리합니다:

```php
$comments = Comment::whereMorphedTo('commentable', $post)
    ->orWhereMorphedTo('commentable', $video)
    ->get();
```

<a name="querying-all-morph-to-related-models"></a>
#### 모든 다형성 관계 모델 쿼리

모든 폴리모픽 부모를 대상으로 삼으려면, 배열 대신 와일드카드 `*`를 넘기면 됩니다. 이 경우 Laravel이 가능한 폴리모픽 타입을 자동으로 조회합니다:

```php
use Illuminate\Database\Eloquent\Builder;

$comments = Comment::whereHasMorph('commentable', '*', function (Builder $query) {
    $query->where('title', 'like', 'foo%');
})->get();
```

<a name="aggregating-related-models"></a>
## 연관 모델 집계하기

<a name="counting-related-models"></a>
### 연관 모델 개수 세기

연관 모델을 실제로 로딩하지 않고, 단순히 개수만 알고 싶을 때는 `withCount` 메서드를 사용하세요. 이 메서드는 결과 모델에 `{relation}_count` 속성을 추가합니다:

```php
use App\Models\Post;

$posts = Post::withCount('comments')->get();

foreach ($posts as $post) {
    echo $post->comments_count;
}
```

여러 관계에 대해 개수 추가, 조건 조건 추가도 가능합니다:

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::withCount(['votes', 'comments' => function (Builder $query) {
    $query->where('content', 'like', 'code%');
}])->get();

echo $posts[0]->votes_count;
echo $posts[0]->comments_count;
```

관계 개수를 별명(alias)으로도 받을 수 있습니다:

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
#### 나중에(Deferred) 개수 로딩

부모 모델을 이미 조회한 후에 관계 개수를 추가로 로드하고 싶으면 `loadCount` 메서드를 사용하세요:

```php
$book = Book::first();

$book->loadCount('genres');
```

필요하다면, 클로저를 써서 쿼리 조건도 붙일 수 있습니다:

```php
$book->loadCount(['reviews' => function (Builder $query) {
    $query->where('rating', 5);
}])
```

<a name="relationship-counting-and-custom-select-statements"></a>
#### 관계 개수와 커스텀 select문 조합

`select`와 함께 쓸 경우, 반드시 `withCount`를 `select` 이후에 호출해야 합니다:

```php
$posts = Post::select(['title', 'body'])
    ->withCount('comments')
    ->get();
```

<a name="other-aggregate-functions"></a>
### 기타 집계 함수

`withCount` 외에도, `withMin`, `withMax`, `withAvg`, `withSum`, `withExists` 메서드도 지원합니다. 결과에는 `{relation}_{function}_{column}` 형식의 속성이 추가됩니다:

```php
use App\Models\Post;

$posts = Post::withSum('comments', 'votes')->get();

foreach ($posts as $post) {
    echo $post->comments_sum_votes;
}
```

별명(alias) 지정도 가능합니다:

```php
$posts = Post::withSum('comments as total_comments', 'votes')->get();

foreach ($posts as $post) {
    echo $post->total_comments;
}
```

이들 메서드에도 나중에(Deferred) 로딩 버전이 있습니다:

```php
$post = Post::first();

$post->loadSum('comments', 'votes');
```

`select`와 함께 쓸 때는, 반드시 select 이후에 호출하세요:

```php
$posts = Post::select(['title', 'body'])
    ->withExists('comments')
    ->get();
```

<a name="counting-related-models-on-morph-to-relationships"></a>
### Morph To 연관관계의 연관 모델 개수 세기

"morph to" 관계에서 다양한 부모별 관계 개수를 한 번에 eager load 하려면, `with`와 폴리모픽 관계의 `morphWithCount`를 조합하면 됩니다. 예를 들어, `Photo`는 `Tag`, `Post`는 `Comment` 관계가 있고, `ActivityFeed`의 parentable이 이 둘에 모두 연결된다면:

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
#### Morph To 관계의 나중에(Deferred) 개수 로딩

이미 ActivityFeed를 eager load해서 가져온 경우, `loadMorphCount`를 사용하면 parentable별 관계 개수를 쉽게 로드할 수 있습니다:

```php
$activities = ActivityFeed::with('parentable')->get();

$activities->loadMorphCount('parentable', [
    Photo::class => ['tags'],
    Post::class => ['comments'],
]);
```

<a name="eager-loading"></a>
## 즉시 로딩(Eager Loading)

연관관계에 동적 속성으로 접근할 때는 실제로 해당 데이터가 필요해질 때 쿼리가 실행됩니다. 그러나 Eloquent에서는 부모 모델 쿼리 시점을 기준으로 미리 연관관계를 로딩할 수도 있는데, 이것이 "즉시 로딩(eager loading)"입니다. 이는 "N + 1" 문제를 해결하는 핵심입니다. 아래는 작가가 쓴 책(Book)과 Author 관계 예시입니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Book extends Model
{
    /**
     * 이 책을 쓴 작가를 반환합니다.
     */
    public function author(): BelongsTo
    {
        return $this->belongsTo(Author::class);
    }
}
```

모든 책과 작가를 조회하는 코드 예시:

```php
use App\Models\Book;

$books = Book::all();

foreach ($books as $book) {
    echo $book->author->name;
}
```

이 코드는 책 25권이면 26번의 쿼리가 일어나게 됩니다. 하지만 eager loading을 사용하면 쿼리 수가 2개로 줄어듭니다:

```php
$books = Book::with('author')->get();

foreach ($books as $book) {
    echo $book->author->name;
}
```

아래처럼 2개의 쿼리만 실행됩니다:

```sql
select * from books

select * from authors where id in (1, 2, 3, 4, 5, ...)
```

<a name="eager-loading-multiple-relationships"></a>
#### 여러 관계 즉시 로딩

여러 관계를 한 번에 로드하려면, 배열로 관계명을 넘기면 됩니다:

```php
$books = Book::with(['author', 'publisher'])->get();
```

<a name="nested-eager-loading"></a>
#### 중첩 즉시 로딩

관계의 관계까지 즉시 로딩하려면, "점(.)" 표기법을 사용하세요:

```php
$books = Book::with('author.contacts')->get();
```

또는 중첩 배열 방식으로도 가능합니다:

```php
$books = Book::with([
    'author' => [
        'contacts',
        'publisher',
    ],
])->get();
```

<a name="nested-eager-loading-morphto-relationships"></a>
#### `morphTo`의 중첩 즉시 로딩

`morphTo` 관계와 하위 관계까지 한 번에 로딩하려면, `morphWith` 메서드를 조합해 사용합니다:

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

연관관계에서 모든 컬럼이 필요없을 경우, 원하는 컬럼만 지정할 수 있습니다:

```php
$books = Book::with('author:id,name,book_id')->get();
```

> [!WARNING]
> 이 기능을 사용할 때는 `id` 컬럼과 외래키 컬럼을 반드시 포함해야 합니다.

<a name="eager-loading-by-default"></a>
#### 기본적으로 즉시 로딩하기

모든 쿼리에서 항상 eager load하고 싶은 관계가 있다면, 모델에 `$with` 속성을 설정하세요:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Book extends Model
{
    /**
     * 항상 로딩할 연관관계.
     *
     * @var array
     */
    protected $with = ['author'];

    /**
     * 이 책을 쓴 작가를 반환합니다.
     */
    public function author(): BelongsTo
    {
        return $this->belongsTo(Author::class);
    }

    /**
     * 이 책의 장르를 반환합니다.
     */
    public function genre(): BelongsTo
    {
        return $this->belongsTo(Genre::class);
    }
}
```

특정 쿼리에서 `$with`의 항목을 제외하려면 `without`, 전부 덮어쓰려면 `withOnly`를 사용할 수 있습니다:

```php
$books = Book::without('author')->get();

$books = Book::withOnly('genre')->get();
```

<a name="constraining-eager-loads"></a>
### 즉시 로딩 제약

즉시 로딩시 추가 쿼리 조건을 걸고 싶을 땐, 배열의 키를 관계명, 값에 클로저를 넘겨 처럼 사용할 수 있습니다:

```php
use App\Models\User;

$users = User::with(['posts' => function ($query) {
    $query->where('title', 'like', '%code%');
}])->get();
```

다른 쿼리 빌더 메서드들도 체이닝할 수 있습니다:

```php
$users = User::with(['posts' => function ($query) {
    $query->orderBy('created_at', 'desc');
}])->get();
```

<a name="constraining-eager-loading-of-morph-to-relationships"></a>
#### morphTo 관계의 즉시 로딩 제약

`morphTo` 관계의 각 유형별로 추가 쿼리 제약을 추가하려면, `MorphTo`의 `constrain` 메서드를 사용하세요:

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
#### 관계 존재 기반 즉시 로딩

관계 존재조건(예: `has`/`whereHas`)과 즉시 로딩을 동시에 할 때는 `withWhereHas` 메서드를 사용하세요:

```php
use App\Models\User;

$users = User::withWhereHas('posts', function ($query) {
    $query->where('featured', true);
})->get();
```

<a name="lazy-eager-loading"></a>
### 지연 즉시 로딩(Lazy Eager Loading)

부모 모델 조회 후, 조건에 따라 연관관계만 나중에 로딩하고 싶다면 `load`, `loadMissing` 메서드를 사용하세요:

```php
use App\Models\Book;

$books = Book::all();

if ($condition) {
    $books->load('author', 'publisher');
}
```

쿼리 조건이 필요할 때는 배열 + 클로저를 넘길 수 있습니다:

```php
$author->load(['books' => function ($query) {
    $query->orderBy('published_date', 'asc');
}]);
```

이미 로드된 관계는 건너뛰고 싶은 경우 `loadMissing`를 사용하세요:

```php
$book->loadMissing('author');
```

<a name="nested-lazy-eager-loading-morphto"></a>
#### 중첩 지연 즉시 로딩 및 `morphTo`

`morphTo` 관계와 그 하위 관계까지 지연 즉시 로딩하고 싶다면, `loadMorph` 메서드를 사용하면 됩니다:

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
### 자동 즉시 로딩(Automatic Eager Loading)

> [!WARNING]
> 이 기능은 현재 베타이며, 향후 패치 릴리즈에서도 동작 및 API가 변경될 수 있습니다.

많은 경우, Laravel이 암묵적으로 연관관계 접근 시 즉시 로딩을 자동으로 수행할 수 있습니다. 전역적으로 활성화하려면, `AppServiceProvider`의 `boot`에서 아래처럼 호출하세요:

```php
use Illuminate\Database\Eloquent\Model;

/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Model::automaticallyEagerLoadRelationships();
}
```

이 기능이 활성화되면, 아직 로드되지 않은 관계를 접근할 때 해당 컬렉션 전체에 대해 "lazy eager load"가 자동 실행됩니다.

개별 컬렉션만 자동 즉시 로딩하고 싶다면, 컬렉션 인스턴스에 `withRelationshipAutoloading`을 호출하면 됩니다:

```php
$users = User::where('vip', true)->get();

return $users->withRelationshipAutoloading();
```

<a name="preventing-lazy-loading"></a>
### 지연 로딩 방지

애플리케이션의 성능을 보장하기 위해, 지연 로딩을 아예 금지할 수도 있습니다. 이 기능은 `preventLazyLoading` 메서드를 통해 적용할 수 있으며, 보통 비-운영환경(dev, staging 등)에서만 활성화하는 게 좋습니다:

```php
use Illuminate\Database\Eloquent\Model;

/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Model::preventLazyLoading(! $this->app->isProduction());
}
```

이 기능이 활성화되면, 지연 로딩이 시도됐을 때 `Illuminate\Database\LazyLoadingViolationException` 예외가 발생합니다.

예외 대신 로그만 남기고 싶을 땐, `handleLazyLoadingViolationsUsing`을 사용할 수 있습니다:

```php
Model::handleLazyLoadingViolationUsing(function (Model $model, string $relation) {
    $class = $model::class;

    info("Attempted to lazy load [{$relation}] on model [{$class}].");
});
```

<a name="inserting-and-updating-related-models"></a>
## 연관 모델 삽입 및 수정

<a name="the-save-method"></a>
### `save` 메서드

Eloquent는 연관관계에 새 모델을 추가하도록 다양한 메서드를 제공합니다. 예를 들어, 특정 포스트에 새 댓글을 추가하려면 댓글 모델에 직접 `post_id`를 지정하지 않고, 관계의 `save` 메서드를 쓸 수 있습니다:

```php
use App\Models\Comment;
use App\Models\Post;

$comment = new Comment(['message' => 'A new comment.']);

$post = Post::find(1);

$post->comments()->save($comment);
```

동적 속성(`$post->comments`)이 아닌, 메서드로(`$post->comments()`) 접근한 점에 유의하세요. `save`는 알맞은 `post_id`를 자동으로 할당합니다.

여러 모델을 한꺼번에 저장하려면 `saveMany`를 사용하세요:

```php
$post = Post::find(1);

$post->comments()->saveMany([
    new Comment(['message' => 'A new comment.']),
    new Comment(['message' => 'Another new comment.']),
]);
```

`save`/`saveMany`는 실제로 DB에 저장만 하고, 부모 모델에 이미 로드된 연관관계(메모리 내 컬렉션)는 갱신하지 않습니다. 따라서 이후 관계를 접근한다면, `refresh`로 리로드를 권장합니다:

```php
$post->comments()->save($comment);

$post->refresh();

// 새 댓글 포함 전체 댓글
$post->comments;
```

<a name="the-push-method"></a>
#### 모델 및 관계를 재귀적으로 저장

모델과 그에 연결된 모든 관계를 한 번에 저장하려면 `push` 메서드를 사용합니다. 예시는 아래와 같습니다:

```php
$post = Post::find(1);

$post->comments[0]->message = 'Message';
$post->comments[0]->author->name = 'Author Name';

$post->push();
```

이벤트 발생 없이 저장하려면 `pushQuietly`를 사용하세요:

```php
$post->pushQuietly();
```

<a name="the-create-method"></a>
### `create` 메서드

`save`, `saveMany` 외에도, `create` 메서드도 사용할 수 있습니다. 이 메서드는 속성 배열을 받아 모델을 생성하고 DB에 저장합니다. `save`는 모델 인스턴스를, `create`는 PHP 배열을 받는다는 차이가 있습니다:

```php
use App\Models\Post;

$post = Post::find(1);

$comment = $post->comments()->create([
    'message' => 'A new comment.',
]);
```

여러 모델을 한 번에 만들고 싶으면 `createMany`를 사용:

```php
$post = Post::find(1);

$post->comments()->createMany([
    ['message' => 'A new comment.'],
    ['message' => 'Another new comment.'],
]);
```

이벤트를 발생시키지 않고 생성할 때는 `createQuietly`, `createManyQuietly`를 사용할 수 있습니다:

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

연관관계를 통한 [패턴 기반 모델 생성/수정(Upsert)](/docs/12.x/eloquent#upserts)는 `findOrNew`, `firstOrNew`, `firstOrCreate`, `updateOrCreate`에서 지원합니다.

> [!NOTE]
> `create` 메서드 사용 전, [대량 할당(Mass Assignment)](/docs/12.x/eloquent#mass-assignment) 관련 문서를 반드시 참고하세요.

<a name="updating-belongs-to-relationships"></a>
### Belongs To 연관관계

자식 모델을 새 부모 모델에 연결하려면 `associate` 메서드를 사용하세요. 예시에서 `User`가 `Account`와 `belongsTo` 관계일 때, 자동으로 외래키가 할당됩니다:

```php
use App\Models\Account;

$account = Account::find(10);

$user->account()->associate($account);

$user->save();
```

부모 모델 연결을 제거하려면 `dissociate` 메서드를 사용하세요. 외래키가 null로 설정됩니다:

```php
$user->account()->dissociate();

$user->save();
```

<a name="updating-many-to-many-relationships"></a>
### 다대다 연관관계

<a name="attaching-detaching"></a>
#### attach / detach

다대다 관계에서는 `attach`로 중간 테이블에 직접 연결할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

$user->roles()->attach($roleId);
```

중간 테이블에 추가 데이터도 함께 저장하려면 두 번째 인수로 배열을 넘기세요:

```php
$user->roles()->attach($roleId, ['expires' => $expires]);
```

관계를 끊으려면 `detach`를 사용합니다:

```php
// 단일 역할 해제
$user->roles()->detach($roleId);

// 모든 역할 해제
$user->roles()->detach();
```

ID 배열로 한 번에 처리할 수도 있습니다:

```php
$user = User::find(1);

$user->roles()->detach([1, 2, 3]);

$user->roles()->attach([
    1 => ['expires' => $expires],
    2 => ['expires' => $expires],
]);
```

<a name="syncing-associations"></a>
#### 연관관계 동기화(Syncing Associations)

`sync` 메서드를 사용하면, 지정한 ID 배열만 남기고 나머지는 모두 detach하게 할 수 있습니다:

```php
$user->roles()->sync([1, 2, 3]);
```

동기화 시 각 ID마다 추가 컬럼값도 넘길 수 있습니다:

```php
$user->roles()->sync([1 => ['expires' => true], 2, 3]);
```

동일한 pivot 값을 모든 ID에 적용하면서 sync하려면 `syncWithPivotValues`를 사용하세요:

```php
$user->roles()->syncWithPivotValues([1, 2, 3], ['active' => true]);
```

배열에 없는 기존 ID를 detach하지 않고 유지하려면, `syncWithoutDetaching`을 사용하면 됩니다:

```php
$user->roles()->syncWithoutDetaching([1, 2, 3]);
```

<a name="toggling-associations"></a>
#### 연관관계 토글(Toggling Associations)

`toggle` 메서드는 지정한 ID의 연결 여부를 반대로 전환합니다. 연결돼 있으면 detach, 아니면 attach:

```php
$user->roles()->toggle([1, 2, 3]);
```

토글 시에도 중간 테이블에 컬럼 값을 넘길 수 있습니다:

```php
$user->roles()->toggle([
    1 => ['expires' => true],
    2 => ['expires' => true],
]);
```

<a name="updating-a-record-on-the-intermediate-table"></a>
#### 중간 테이블 레코드 수정

중간 테이블에 이미 있는 데이터의 값을 바꾸려면 `updateExistingPivot`을 사용하세요:

```php
$user = User::find(1);

$user->roles()->updateExistingPivot($roleId, [
    'active' => false,
]);
```

<a name="touching-parent-timestamps"></a>
## 부모 타임스탬프 갱신하기

`belongsTo` 또는 `belongsToMany` 관계(예: `Comment`가 `Post`에 속함)에서, 자식 모델이 수정될 때 부모의 `updated_at`도 함께 갱신되고 싶을 때가 있습니다.

이를 위해, 자식 모델에 `touches` 속성 배열에 관계명을 지정하면, 자식 모델을 업데이트 할 때 부모의 `updated_at`도 자동 갱신됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Comment extends Model
{
    /**
     * 갱신할 관계명 목록.
     *
     * @var array
     */
    protected $touches = ['post'];

    /**
     * 이 댓글이 속한 포스트를 반환합니다.
     */
    public function post(): BelongsTo
    {
        return $this->belongsTo(Post::class);
    }
}
```

> [!WARNING]
> 부모 타임스탬프는 반드시 Eloquent의 `save` 메서드로 자식 모델을 업데이트할 때만 갱신됩니다.
