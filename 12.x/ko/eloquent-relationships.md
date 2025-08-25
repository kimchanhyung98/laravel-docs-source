# Eloquent: 연관관계 (Eloquent: Relationships)

- [소개](#introduction)
- [연관관계 정의하기](#defining-relationships)
    - [일대일 / hasOne](#one-to-one)
    - [일대다 / hasMany](#one-to-many)
    - [일대다 (역방향) / belongsTo](#one-to-many-inverse)
    - [여러 개 중 하나 갖기](#has-one-of-many)
    - [관통 일대일 (hasOneThrough)](#has-one-through)
    - [관통 일대다 (hasManyThrough)](#has-many-through)
- [스코프드 연관관계](#scoped-relationships)
- [다대다 연관관계](#many-to-many)
    - [중간 테이블 컬럼 가져오기](#retrieving-intermediate-table-columns)
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
- [연관관계 쿼리하기](#querying-relations)
    - [연관관계 메서드와 동적 속성의 차이](#relationship-methods-vs-dynamic-properties)
    - [연관관계 존재 쿼리하기](#querying-relationship-existence)
    - [연관관계 부재 쿼리하기](#querying-relationship-absence)
    - [Morph To 연관관계 쿼리](#querying-morph-to-relationships)
- [연관된 모델 집계](#aggregating-related-models)
    - [연관된 모델 수 카운팅](#counting-related-models)
    - [기타 집계 함수](#other-aggregate-functions)
    - [Morph To 연관관계의 모델 수 카운팅](#counting-related-models-on-morph-to-relationships)
- [즉시 로딩(Eager Loading)](#eager-loading)
    - [즉시 로딩 제약](#constraining-eager-loads)
    - [지연 즉시 로딩(Lazy Eager Loading)](#lazy-eager-loading)
    - [자동 즉시 로딩](#automatic-eager-loading)
    - [지연 로딩 방지](#preventing-lazy-loading)
- [연관된 모델 삽입 및 수정](#inserting-and-updating-related-models)
    - [`save` 메서드](#the-save-method)
    - [`create` 메서드](#the-create-method)
    - [Belongs To 연관관계](#updating-belongs-to-relationships)
    - [다대다 연관관계](#updating-many-to-many-relationships)
- [부모 타임스탬프 갱신(touch)](#touching-parent-timestamps)

<a name="introduction"></a>
## 소개 (Introduction)

데이터베이스 테이블들은 종종 서로 연관되어 있습니다. 예를 들어, 블로그 게시물은 여러 개의 댓글을 가질 수 있으며, 하나의 주문이 해당 주문을 한 사용자와 연관될 수 있습니다. Eloquent는 이러한 연관관계 관리와 활용을 쉽게 만들어주며, 아래와 같이 다양한 일반적인 연관관계를 지원합니다.

<div class="content-list" markdown="1">

- [일대일(One To One)](#one-to-one)
- [일대다(One To Many)](#one-to-many)
- [다대다(Many To Many)](#many-to-many)
- [관통 일대일(Has One Through)](#has-one-through)
- [관통 일대다(Has Many Through)](#has-many-through)
- [일대일(폴리모픽)](#one-to-one-polymorphic-relations)
- [일대다(폴리모픽)](#one-to-many-polymorphic-relations)
- [다대다(폴리모픽)](#many-to-many-polymorphic-relations)

</div>

<a name="defining-relationships"></a>
## 연관관계 정의하기 (Defining Relationships)

Eloquent의 연관관계는 각 모델 클래스의 메서드로 정의합니다. 연관관계는 [쿼리 빌더](/docs/12.x/queries)의 강력한 기능도 제공하므로, 메서드로 정의함으로써 다양한 체이닝 및 쿼리 빌더 기능을 활용할 수 있습니다. 예를 들어, 다음처럼 `posts` 연관관계에 추가로 조건을 걸 수 있습니다.

```php
$user->posts()->where('active', 1)->get();
```

이제 본격적으로 연관관계를 활용하기 전에, Eloquent가 지원하는 각 연관관계 타입을 정의하는 방법을 자세히 살펴보겠습니다.

<a name="one-to-one"></a>
### 일대일 / hasOne (One to One / Has One)

일대일 연관관계는 가장 기본적인 데이터베이스 연관관계입니다. 예를 들어, `User` 모델은 하나의 `Phone` 모델과 연관될 수 있습니다. 이 연관관계를 정의하려면 `User` 모델에 `phone` 메서드를 추가하고, 이 메서드에서 `hasOne`을 호출하여 결과를 반환합니다. `hasOne` 메서드는 모델의 `Illuminate\Database\Eloquent\Model` 기본 클래스에 내장되어 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasOne;

class User extends Model
{
    /**
     * 사용자의 전화번호 반환
     */
    public function phone(): HasOne
    {
        return $this->hasOne(Phone::class);
    }
}
```

`hasOne` 메서드의 첫 번째 인수는 연관된 모델 클래스의 이름입니다. 연관관계를 정의하고 나면, Eloquent의 동적 속성을 통해 연관 레코드를 쉽게 조회할 수 있습니다. 동적 속성을 사용하면 마치 속성처럼 연관관계를 접근할 수 있습니다.

```php
$phone = User::find(1)->phone;
```

Eloquent는 부모 모델 이름을 기반으로 외래 키(foreign key)를 자동으로 결정합니다. 이 경우, `Phone` 모델에는 기본적으로 `user_id` 외래 키를 가진 것으로 간주합니다. 이 규칙을 변경하고 싶다면, `hasOne`의 두 번째 인수로 외래 키를 전달할 수 있습니다.

```php
return $this->hasOne(Phone::class, 'foreign_key');
```

또한, 외래 키에 부모 모델의 기본 키 컬럼(즉, `id`)과 일치하는 값을 자동으로 사용합니다. 즉, 사용자의 `id` 컬럼 값이 `Phone`의 `user_id` 컬럼에 들어가게 됩니다. 만약 연관관계에 사용할 기본 키 값이 `id`가 아니거나, 모델의 `$primaryKey` 속성을 사용하지 않는다면, 세 번째 인수로 로컬 키를 지정할 수 있습니다.

```php
return $this->hasOne(Phone::class, 'foreign_key', 'local_key');
```

<a name="one-to-one-defining-the-inverse-of-the-relationship"></a>
#### 연관관계의 역방향 정의

이제 `User` 모델로부터 `Phone`을 접근할 수 있습니다. 반대로, `Phone`이 어떤 사용자에 속해 있는지 접근하는 연관관계를 정의해보겠습니다. `hasOne` 연관관계의 역방향은 `belongsTo` 메서드로 정의합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Phone extends Model
{
    /**
     * 전화번호의 소유자 반환
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }
}
```

`user` 메서드를 호출하면, Eloquent는 `Phone` 모델의 `user_id` 컬럼 값과 일치하는 `User` 모델(`id`)을 찾아 반환합니다.

Eloquent는 메서드 이름에 `_id`를 붙여 외래 키가 무엇인지 결정합니다. 즉, 위 예시에서는 `Phone` 모델에 `user_id` 컬럼이 있는 것으로 가정합니다. 만약 외래 키가 다르다면, 두 번째 인수로 키 이름을 지정할 수 있습니다.

```php
/**
 * 전화번호의 소유자 반환
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class, 'foreign_key');
}
```

부모 모델이 `id`가 아닌 다른 컬럼을 기본 키로 사용하거나 연관 모델 조회시 다른 컬럼을 사용하려면, 세 번째 인수로 부모 테이블의 키 이름을 명시할 수 있습니다.

```php
/**
 * 전화번호의 소유자 반환
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class, 'foreign_key', 'owner_key');
}
```

<a name="one-to-many"></a>
### 일대다 / hasMany (One to Many / Has Many)

일대다 연관관계는 하나의 부모 모델이 여러 자식 모델과 연관될 때 사용합니다. 예를 들어, 하나의 블로그 게시물은 여러 개의 댓글을 가질 수 있습니다. 다른 Eloquent 연관관계와 마찬가지로, 모델에 메서드를 정의합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Post extends Model
{
    /**
     * 해당 게시물의 댓글 반환
     */
    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class);
    }
}
```

Eloquent는 `Comment` 모델의 외래 키 컬럼을 자동으로 결정합니다. 기본적으로, 부모 모델의 이름을 스네이크 케이스로 변환하고 `_id`를 붙입니다. 이번 예시의 경우 `Comment` 모델의 외래 키는 `post_id`가 됩니다.

연관관계 메서드를 정의한 뒤에는, `comments` 속성에 접근해서 [컬렉션](/docs/12.x/eloquent-collections)을 가져올 수 있습니다. 동적 속성 덕분에, 메서드가 아니라 속성처럼 접근할 수 있습니다.

```php
use App\Models\Post;

$comments = Post::find(1)->comments;

foreach ($comments as $comment) {
    // ...
}
```

연관관계도 쿼리 빌더 역할을 하므로, 추가적인 조건을 연관관계 쿼리에 체이닝할 수 있습니다.

```php
$comment = Post::find(1)->comments()
    ->where('title', 'foo')
    ->first();
```

`hasOne`과 마찬가지로, 외래 키와 로컬 키를 추가 인수로 지정해 규칙을 오버라이드할 수 있습니다.

```php
return $this->hasMany(Comment::class, 'foreign_key');

return $this->hasMany(Comment::class, 'foreign_key', 'local_key');
```

<a name="automatically-hydrating-parent-models-on-children"></a>
#### 자식에서 부모 모델 자동 하이드레이팅

Eloquent 즉시 로딩(eager loading)을 사용하고 있더라도, 자식 모델을 반복하면서 그 부모 모델에 접근하면 "N + 1" 쿼리 문제가 생길 수 있습니다.

```php
$posts = Post::with('comments')->get();

foreach ($posts as $post) {
    foreach ($post->comments as $comment) {
        echo $comment->post->title;
    }
}
```

위 예제에서는, `Post` 모델마다 댓글이 모두 즉시 로딩되었음에도 불구하고, 각 `Comment` 모델에서 부모 `Post`에 접근할 때 추가 쿼리가 발생해 "N + 1" 문제가 생깁니다.

자식 모델에 부모 모델이 자동으로 하이드레이팅되길 원한다면, `hasMany` 관계 정의 시 `chaperone` 메서드를 사용할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Post extends Model
{
    /**
     * 해당 게시물의 댓글 반환
     */
    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class)->chaperone();
    }
}
```

또는, 즉시 로딩 시점에 자동 하이드레이팅을 적용하고 싶으면, 관계를 즉시 로딩할 때 `chaperone`을 사용하세요.

```php
use App\Models\Post;

$posts = Post::with([
    'comments' => fn ($comments) => $comments->chaperone(),
])->get();
```

<a name="one-to-many-inverse"></a>
### 일대다 (역방향) / belongsTo (One to Many (Inverse) / Belongs To)

게시물의 모든 댓글을 가져올 수 있게 되었으니, 댓글에서 자신의 부모 게시물을 조회하는 연관관계도 정의할 수 있습니다. `hasMany`의 역방향은 자식 모델에서 `belongsTo` 메서드로 정의합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Comment extends Model
{
    /**
     * 댓글이 속한 게시물 반환
     */
    public function post(): BelongsTo
    {
        return $this->belongsTo(Post::class);
    }
}
```

이제 동적 속성을 사용해 댓글의 부모 게시물을 조회할 수 있습니다.

```php
use App\Models\Comment;

$comment = Comment::find(1);

return $comment->post->title;
```

위 예제에서 Eloquent는 댓글의 `post_id` 컬럼 값과 일치하는 `Post` 모델을 찾아 반환합니다.

외래 키 이름은 관계 메서드 이름에 `_`와 부모의 기본 키 컬럼 이름을 붙여 결정합니다. 이번 예시라면 댓글 테이블의 외래 키는 `post_id`입니다.

외래 키 규칙이 이와 다르면, 두 번째 인수로 커스텀 외래 키 이름을 지정할 수 있습니다.

```php
/**
 * 댓글이 속한 게시물 반환
 */
public function post(): BelongsTo
{
    return $this->belongsTo(Post::class, 'foreign_key');
}
```

부모 모델이 `id` 대신 다른 컬럼을 기본 키로 쓰거나 다른 컬럼으로 연관 모델을 찾고자 한다면, 세 번째 인수에 맞춤 키를 지정 가능합니다.

```php
/**
 * 댓글이 속한 게시물 반환
 */
public function post(): BelongsTo
{
    return $this->belongsTo(Post::class, 'foreign_key', 'owner_key');
}
```

<a name="default-models"></a>
#### 기본 모델(Default Models)

`belongsTo`, `hasOne`, `hasOneThrough`, `morphOne` 관계에서는 연관관계가 `null`일 경우 반환될 기본 모델을 정의할 수 있습니다. 이러한 패턴은 [Null Object 패턴](https://en.wikipedia.org/wiki/Null_Object_pattern)이라고 하며, 코드에서 조건문 체크를 줄여줍니다. 아래 예시에서는 `Post` 모델의 사용자 관계가 없으면 빈 `App\Models\User` 모델을 반환합니다.

```php
/**
 * 게시물 작성자 반환
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault();
}
```

기본 모델의 속성을 직접 지정하려면 배열이나 클로저를 `withDefault`에 전달하세요.

```php
/**
 * 게시물 작성자 반환
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault([
        'name' => 'Guest Author',
    ]);
}

/**
 * 게시물 작성자 반환
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault(function (User $user, Post $post) {
        $user->name = 'Guest Author';
    });
}
```

<a name="querying-belongs-to-relationships"></a>
#### Belongs To 연관관계 쿼리(Querying Belongs To Relationships)

"Belongs to" 연관관계의 자식 모델을 조회할 때, 직접 `where`절을 사용해 쿼리를 만들 수 있습니다.

```php
use App\Models\Post;

$posts = Post::where('user_id', $user->id)->get();
```

더 간편하게, `whereBelongsTo` 메서드를 사용하면 연관관계와 외래 키를 자동으로 알아서 쿼리를 생성해줍니다.

```php
$posts = Post::whereBelongsTo($user)->get();
```

[컬렉션](/docs/12.x/eloquent-collections) 객체를 넘기면 컬렉션 안의 여러 부모 모델 중 하나라도 소유한 모델을 조회합니다.

```php
$users = User::where('vip', true)->get();

$posts = Post::whereBelongsTo($users)->get();
```

Laravel은 전달된 모델의 클래스 이름을 기준으로 연관관계 이름을 결정하지만, 두 번째 인수로 관계 이름을 직접 지정할 수도 있습니다.

```php
$posts = Post::whereBelongsTo($user, 'author')->get();
```

<a name="has-one-of-many"></a>
### 여러 개 중 하나 갖기 (Has One of Many)

하나의 모델이 여러 연관 모델을 가질 수 있으나, 이 중 "가장 최신" 혹은 "가장 오래된" 모델만 바로 조회하고 싶을 때가 있습니다. 예를 들어, `User` 모델이 여러 개의 `Order` 모델을 가진 상황에서 사용자가 가장 최근 주문을 간편하게 가져오려면, `hasOne` 관계에 `ofMany` 계열 메서드를 조합해 사용합니다.

```php
/**
 * 사용자의 가장 최근 주문 반환
 */
public function latestOrder(): HasOne
{
    return $this->hasOne(Order::class)->latestOfMany();
}
```

반대로 "가장 오래된" (즉, 최초) 연관 모델을 가져오고 싶을 때도 마찬가지 방법을 씁니다.

```php
/**
 * 사용자의 최초 주문 반환
 */
public function oldestOrder(): HasOne
{
    return $this->hasOne(Order::class)->oldestOfMany();
}
```

기본적으로 `latestOfMany`/`oldestOfMany`는 모델의 정렬 가능한 기본 키 기준으로 최신/최초 모델을 찾아옵니다. 하지만, 다른 필드 기준으로 연관 모델을 선별하고 싶을 때는 `ofMany`를 사용해 컬럼명과 집계 함수(`min`, `max`)를 지정할 수 있습니다.

```php
/**
 * 사용자의 가장 비싼 주문 반환
 */
public function largestOrder(): HasOne
{
    return $this->hasOne(Order::class)->ofMany('price', 'max');
}
```

> [!WARNING]
> PostgreSQL은 UUID 컬럼에 `MAX`함수를 적용할 수 없으므로, PostgreSQL UUID 컬럼과 one-of-many 관계를 함께 사용할 수 없습니다.

<a name="converting-many-relationships-to-has-one-relationships"></a>
#### "Many" 관계를 Has One 관계로 변환

이미 동일 대상에 대해 "has many"관계를 정의한 경우, `latestOfMany`, `oldestOfMany`, `ofMany` 등을 통해 간편하게 "has one"형식으로 변환할 수 있습니다. 이럴 때는 `one` 메서드를 chaining 하세요.

```php
/**
 * 사용자의 주문 목록 반환
 */
public function orders(): HasMany
{
    return $this->hasMany(Order::class);
}

/**
 * 사용자의 가장 비싼 주문 반환
 */
public function largestOrder(): HasOne
{
    return $this->orders()->one()->ofMany('price', 'max');
}
```

또한, `HasManyThrough` 관계에서도 `one`을 사용해 `HasOneThrough`로 변환할 수 있습니다.

```php
public function latestDeployment(): HasOneThrough
{
    return $this->deployments()->one()->latestOfMany();
}
```

<a name="advanced-has-one-of-many-relationships"></a>
#### 고급 Has One of Many 관계

더 복잡한 "여러 개 중 하나" 관계를 만들 수도 있습니다. 예시로 `Product` 모델이 여러 개의 `Price` 모델과 연관되어 있고, 새로운 가격 정보가 미래에 적용되도록 사전 등록되어 있을 수 있습니다. 이 경우, `published_at` 컬럼을 활용하여 현재 시점 이전에 공개된 최신 가격을 가져오고, 공개일이 동일하다면 ID가 가장 큰 Price를 선택한다고 가정합시다.

이를 위해, `ofMany`에 정렬 컬럼 배열과, 추가 조건 처리를 위한 클로저를 전달합니다.

```php
/**
 * 상품의 현재 가격 반환
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
### 관통 일대일 (Has One Through)

"has-one-through" 관계는 다른 모델과 일대일 관계이지만, 세 번째 모델을 경유해 연관되는 형태입니다.

예를 들어, 자동차 정비소 애플리케이션에서 `Mechanic`는 하나의 `Car`와 연관되고, `Car`는 하나의 `Owner`와 연관되어 있습니다. 이 경우, 정비사와 소유주는 DB상 직접 연결되어 있지는 않지만, 정비사는 `Car`를 경유해 소유자에 접근할 수 있습니다.

테이블 구조는 다음과 같습니다.

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

이 구조를 기반으로, `Mechanic` 모델에 아래와 같이 연관관계를 정의할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasOneThrough;

class Mechanic extends Model
{
    /**
     * 자동차 소유자 반환
     */
    public function carOwner(): HasOneThrough
    {
        return $this->hasOneThrough(Owner::class, Car::class);
    }
}
```

`hasOneThrough`의 첫 번째 인수는 최종적으로 접근할 모델, 두 번째 인수는 중간 모델입니다.

만약 중간 모델을 비롯해 모든 관계가 이미 각 모델에 정의되어 있다면, `through` 메서드 체인 방식으로도 관계를 정의할 수 있습니다.

```php
// 문자열 방식
return $this->through('cars')->has('owner');

// 다이나믹 방식
return $this->throughCars()->hasOwner();
```

<a name="has-one-through-key-conventions"></a>
#### 키 규칙(Key Conventions)

동작시 일반적인 Eloquent 외래 키 규칙이 적용됩니다. 필요하다면 외래 키 및 로컬 키를 각각 세 번째~여섯 번째 인수에 지정할 수 있습니다.

```php
class Mechanic extends Model
{
    /**
     * 자동차 소유자 반환
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

앞서 설명한 것처럼, 모든 관계가 이미 모델에 정의되어 있다면 `through` 문법을 활용해 기존 key 규칙을 재활용할 수도 있습니다.

```php
// 문자열 방식
return $this->through('cars')->has('owner');

// 다이나믹 방식
return $this->throughCars()->hasOwner();
```

<a name="has-many-through"></a>
### 관통 일대다 (Has Many Through)

"has-many-through" 관계는 중간 관계를 통해 더 먼 대상의 모델을 쉽게 조회할 수 있는 방식입니다. 예를 들어, [Laravel Cloud](https://cloud.laravel.com)와 같은 배포 플랫폼에서 `Application`이 중간 모델인 `Environment`를 통해 여러 개의 `Deployment` 모델을 조회한다고 가정합시다.

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

이 관계를 `Application` 모델에 아래와 같이 정의할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasManyThrough;

class Application extends Model
{
    /**
     * 애플리케이션의 모든 배포 내역 반환
     */
    public function deployments(): HasManyThrough
    {
        return $this->hasManyThrough(Deployment::class, Environment::class);
    }
}
```

`hasManyThrough`의 첫 번째 인수는 최종적으로 접근할 모델, 두 번째 인수는 중간 모델입니다.

모든 관련 연관관계가 각 모델에 정의되어 있다면, `through` 방식을 통해서도 관계를 생성할 수 있습니다.

```php
// 문자열 방식
return $this->through('environments')->has('deployments');

// 다이나믹 방식
return $this->throughEnvironments()->hasDeployments();
```

비록 `Deployment` 테이블에는 `application_id` 컬럼이 없지만, Eloquent는 중간 `Environment` 테이블의 `application_id`를 참고해 연결 배포 내역을 조회합니다.

<a name="has-many-through-key-conventions"></a>
#### 키 규칙(Key Conventions)

동작시 일반적인 Eloquent 외래 키 규칙이 사용됩니다. 키 커스터마이즈가 필요하다면 세 번째~여섯 번째 인수를 이용해 외래키, 로컬키를 각각 지정합니다.

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

마찬가지로 기존 관계가 이미 모델에 정의되어 있다면 `through` 방식을 사용해 쉽게 선언할 수 있습니다.

```php
// 문자열 방식
return $this->through('environments')->has('deployments');

// 다이나믹 방식
return $this->throughEnvironments()->hasDeployments();
```

<a name="scoped-relationships"></a>
### 스코프드 연관관계(Scoped Relationships)

연관관계를 추가로 제약하는 메서드를 모델에 선언하는 것이 일반적입니다. 예를 들어, `User` 모델에 `posts`(전체 포스트), `featuredPosts`(특정 포스트)를 둘 다 제공하고 싶을 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class User extends Model
{
    /**
     * 사용자의 포스트 반환
     */
    public function posts(): HasMany
    {
        return $this->hasMany(Post::class)->latest();
    }

    /**
     * 사용자의 추천 포스트 반환
     */
    public function featuredPosts(): HasMany
    {
        return $this->posts()->where('featured', true);
    }
}
```

하지만 `featuredPosts` 연관관계로 모델을 생성하면, `featured` 속성에 true 값이 자동으로 할당되지 않습니다. 연관관계 메서드로 생성하는 모델 모두에 지정할 속성이 있다면, 쿼리 빌드 시 `withAttributes`를 사용하세요.

```php
/**
 * 사용자의 추천 포스트 반환
 */
public function featuredPosts(): HasMany
{
    return $this->posts()->withAttributes(['featured' => true]);
}
```

`withAttributes`는 주어진 속성으로 `where` 조건을 추가하며, 해당 관계 메서드로 생성되는 모델에도 이 속성이 자동 추가됩니다.

```php
$post = $user->featuredPosts()->create(['title' => 'Featured Post']);

$post->featured; // true
```

만약 `withAttributes`에서 쿼리 조건을 추가하지 않고 속성만 추가하도록 하려면, `asConditions` 인수를 `false`로 지정하면 됩니다.

```php
return $this->posts()->withAttributes(['featured' => true], asConditions: false);
```

<!-- 이하 내용은 가이드라인에 따라 번역 필요 시 추가 분량 요청 바랍니다. -->