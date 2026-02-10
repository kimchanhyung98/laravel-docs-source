# Eloquent: 연관관계 (Eloquent: Relationships)

- [소개](#introduction)
- [연관관계 정의하기](#defining-relationships)
    - [일대일 / Has One](#one-to-one)
    - [일대다 / Has Many](#one-to-many)
    - [일대다(역방향) / Belongs To](#one-to-many-inverse)
    - [여러 개 중 하나를 가진 관계](#has-one-of-many)
    - [중간 모델을 통한 일대일(Has One Through)](#has-one-through)
    - [중간 모델을 통한 일대다(Has Many Through)](#has-many-through)
- [스코프드 연관관계](#scoped-relationships)
- [다대다 연관관계](#many-to-many)
    - [중간 테이블 컬럼 조회하기](#retrieving-intermediate-table-columns)
    - [중간 테이블 컬럼으로 질의 필터링](#filtering-queries-via-intermediate-table-columns)
    - [중간 테이블 컬럼으로 정렬](#ordering-queries-via-intermediate-table-columns)
    - [커스텀 중간 테이블 모델 정의](#defining-custom-intermediate-table-models)
- [폴리모픽 연관관계](#polymorphic-relationships)
    - [일대일](#one-to-one-polymorphic-relations)
    - [일대다](#one-to-many-polymorphic-relations)
    - [여러 개 중 하나](#one-of-many-polymorphic-relations)
    - [다대다](#many-to-many-polymorphic-relations)
    - [커스텀 폴리모픽 타입](#custom-polymorphic-types)
- [동적 연관관계](#dynamic-relationships)
- [연관관계 질의하기](#querying-relations)
    - [연관관계 메서드와 동적 속성 비교](#relationship-methods-vs-dynamic-properties)
    - [연관관계 존재 유무로 질의하기](#querying-relationship-existence)
    - [연관관계 부재로 질의하기](#querying-relationship-absence)
    - [Morph To 연관관계 질의](#querying-morph-to-relationships)
- [연관 모델 집계하기](#aggregating-related-models)
    - [연관 모델 개수 세기](#counting-related-models)
    - [기타 집계 함수](#other-aggregate-functions)
    - [Morph To 연관관계의 모델 개수 세기](#counting-related-models-on-morph-to-relationships)
- [즉시(이거) 로딩(Eager Loading)](#eager-loading)
    - [즉시 로딩 제약조건 설정](#constraining-eager-loads)
    - [지연 즉시 로딩](#lazy-eager-loading)
    - [자동 즉시 로딩](#automatic-eager-loading)
    - [지연 로딩 방지](#preventing-lazy-loading)
- [연관 모델 저장 및 갱신](#inserting-and-updating-related-models)
    - [`save` 메서드](#the-save-method)
    - [`create` 메서드](#the-create-method)
    - [Belongs To 연관관계](#updating-belongs-to-relationships)
    - [다대다 연관관계](#updating-many-to-many-relationships)
- [부모 타임스탬프 갱신(touch)](#touching-parent-timestamps)

<a name="introduction"></a>
## 소개 (Introduction)

데이터베이스 테이블들은 종종 서로 연관되어 있습니다. 예를 들어, 블로그 게시글에는 여러 개의 댓글이 있을 수 있고, 주문은 해당 주문을 한 사용자와 연관될 수 있습니다. Eloquent는 이와 같은 연관관계를 쉽게 다룰 수 있도록 도와주며, 다양한 일반적인 연관관계 유형을 지원합니다.

<div class="content-list" markdown="1">

- [일대일 (One To One)](#one-to-one)
- [일대다 (One To Many)](#one-to-many)
- [다대다 (Many To Many)](#many-to-many)
- [중간 모델을 통한 일대일(Has One Through)](#has-one-through)
- [중간 모델을 통한 일대다(Has Many Through)](#has-many-through)
- [일대일(폴리모픽)](#one-to-one-polymorphic-relations)
- [일대다(폴리모픽)](#one-to-many-polymorphic-relations)
- [다대다(폴리모픽)](#many-to-many-polymorphic-relations)

</div>

<a name="defining-relationships"></a>
## 연관관계 정의하기 (Defining Relationships)

Eloquent의 연관관계는 Eloquent 모델 클래스의 메서드로 정의합니다. 연관관계는 강력한 [쿼리 빌더](/docs/12.x/queries)로도 동작하기 때문에, 이렇게 메서드로 정의하면 메서드 체이닝이나 다양한 조건을 추가해 쿼리를 만들 수 있습니다. 예를 들어, 아래와 같이 `posts` 연관관계에서 조건을 이어 붙일 수 있습니다.

```php
$user->posts()->where('active', 1)->get();
```

본격적으로 연관관계 사용에 들어가기에 앞서 Eloquent가 지원하는 각각의 연관관계 유형을 어떻게 정의하는지 알아보겠습니다.

<a name="one-to-one"></a>
### 일대일 / Has One (One to One / Has One)

일대일 연관관계는 가장 기본적인 데이터베이스 연관관계입니다. 예를 들어, `User` 모델이 하나의 `Phone` 모델과 연관될 수 있습니다. 이 관계를 정의하려면, `User` 모델에 `phone` 메서드를 추가하고, 그 안에서 `hasOne` 메서드를 호출해 반환해야 합니다. `hasOne` 메서드는 모델의 상속 클래스인 `Illuminate\Database\Eloquent\Model`에서 제공됩니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasOne;

class User extends Model
{
    /**
     * 사용자에 연관된 폰을 반환합니다.
     */
    public function phone(): HasOne
    {
        return $this->hasOne(Phone::class);
    }
}
```

`hasOne` 메서드의 첫 번째 인수는 연관되는 모델 클래스의 이름입니다. 연관관계를 정의하고 나면, Eloquent의 동적 속성을 사용해 연관된 레코드를 조회할 수 있습니다. 동적 속성이란, 마치 모델의 속성처럼 연관관계 메서드에 접근하는 기능입니다.

```php
$phone = User::find(1)->phone;
```

Eloquent는 연관관계의 외래 키를 부모 모델 이름을 기반으로 자동 결정합니다. 위 예시에서는 `Phone` 모델에 `user_id`라는 외래 키가 있다고 가정합니다. 이 규칙을 바꾸고 싶다면, `hasOne` 메서드의 두 번째 인수로 외래 키 이름을 지정할 수 있습니다.

```php
return $this->hasOne(Phone::class, 'foreign_key');
```

또한, Eloquent는 외래 키가 부모의 기본키(primary key) 컬럼 값과 같아야 한다고 가정합니다. 즉, `Phone` 레코드의 `user_id` 컬럼에는 사용자의 `id` 컬럼 값이 들어간다고 봅니다. 만약 `id` 대신 다른 컬럼을 사용하고 싶다면, `hasOne` 메서드의 세 번째 인수로 로컬 키 컬럼명을 지정할 수 있습니다.

```php
return $this->hasOne(Phone::class, 'foreign_key', 'local_key');
```

<a name="one-to-one-defining-the-inverse-of-the-relationship"></a>
#### 연관관계의 역방향 정의하기

이제 `User` 모델에서 `Phone` 모델에 접근할 수 있게 되었습니다. 이번에는 `Phone` 모델에서 이 폰을 소유한 사용자에 접근할 수 있는 관계를 만들어봅니다. 일대일 연관관계의 역방향은 `belongsTo` 메서드를 사용해 정의할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Phone extends Model
{
    /**
     * 이 폰을 소유한 사용자를 반환합니다.
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }
}
```

이제 `user` 메서드를 호출하면, Eloquent는 `Phone` 모델의 `user_id` 컬럼 값과 일치하는 `User` 모델의 `id`를 찾아 반환합니다.

Eloquent는 연관관계 메서드 이름에 `_id`를 붙여 외래 키 이름을 자동으로 결정합니다. 그래서 위 예시처럼 `user()` 메서드를 만들면 `user_id`가 외래 키가 됩니다. 만약 외래 키가 다르다면 두 번째 인수로 외래 키 이름을 지정할 수 있습니다.

```php
/**
 * 이 폰을 소유한 사용자를 반환합니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class, 'foreign_key');
}
```

부모 모델의 기본키가 `id`가 아니거나, 연관관계가 연결될 때 사용할 컬럼을 변경하고 싶다면 세 번째 인수로 부모 테이블의 커스텀 키를 지정하면 됩니다.

```php
/**
 * 이 폰을 소유한 사용자를 반환합니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class, 'foreign_key', 'owner_key');
}
```

<a name="one-to-many"></a>
### 일대다 / Has Many (One to Many / Has Many)

일대다 연관관계는 한 모델이 여러 개의 자식 모델을 가질 때 사용합니다. 예를 들어, 하나의 게시글에는 무한히 많은 댓글이 달릴 수 있습니다. 다른 Eloquent 연관관계들과 마찬가지로, 일대다 관계도 모델에서 메서드로 정의합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Post extends Model
{
    /**
     * 이 게시글의 댓글 목록을 반환합니다.
     */
    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class);
    }
}
```

Eloquent는 자동으로 `Comment` 모델의 외래 키 컬럼을 결정합니다. 관례상, 부모 모델 이름을 snake_case로 변환하고 뒤에 `_id`를 붙입니다. 예시에서는 `Comment` 모델에 `post_id` 컬럼이 있다고 봅니다.

연관관계 메서드를 정의하고 나면, `comments` 속성에 접근해서 관련된 [컬렉션](/docs/12.x/eloquent-collections)을 가져올 수 있습니다. 동적 연관관계 속성 덕분에, 메서드를 마치 모델의 속성처럼 쓸 수 있습니다.

```php
use App\Models\Post;

$comments = Post::find(1)->comments;

foreach ($comments as $comment) {
    // ...
}
```

모든 연관관계는 쿼리 빌더로도 사용되므로, `comments` 메서드를 호출한 후 체이닝으로 추가 조건을 붙일 수 있습니다.

```php
$comment = Post::find(1)->comments()
    ->where('title', 'foo')
    ->first();
```

`hasOne`처럼, `hasMany` 메서드 역시 외래 키와 로컬 키를 추가 인수로 지정할 수 있습니다.

```php
return $this->hasMany(Comment::class, 'foreign_key');

return $this->hasMany(Comment::class, 'foreign_key', 'local_key');
```

<a name="automatically-hydrating-parent-models-on-children"></a>
#### 자식 모델에서 부모 모델 자동 하이드레이팅

Eloquent의 즉시 로딩을 사용하더라도, 자식 모델을 반복문으로 순회하며 그 안에서 부모 모델에 접근하면 "N + 1" 쿼리 문제가 발생할 수 있습니다.

```php
$posts = Post::with('comments')->get();

foreach ($posts as $post) {
    foreach ($post->comments as $comment) {
        echo $comment->post->title;
    }
}
```

위 예시에서는 각 댓글에서 `post`에 접근할 때마다 추가 쿼리가 발생합니다. 모든 게시글에 대해 댓글을 즉시 로딩했지만, 각 자식 `Comment`에서 부모 `Post`가 자동으로 하이드레이팅되지 않기 때문입니다.

Eloquent가 자식에 부모 모델을 자동으로 할당하게 하고 싶다면, `hasMany` 연관관계 정의 시 `chaperone` 메서드를 사용할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Post extends Model
{
    /**
     * 이 게시글의 댓글 목록을 반환합니다.
     */
    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class)->chaperone();
    }
}
```

또는, 런타임에 즉시 로딩 과정에서 자동 하이드레이팅을 활성화하려면, 다음과 같이 사용할 수 있습니다.

```php
use App\Models\Post;

$posts = Post::with([
    'comments' => fn ($comments) => $comments->chaperone(),
])->get();
```

<a name="one-to-many-inverse"></a>
### 일대다(역방향) / Belongs To (One to Many (Inverse) / Belongs To)

이제 게시글의 모든 댓글에 접근할 수 있게 되었으니, 이번에는 댓글에서 부모 게시글에 접근할 수 있는 관계를 만들어보겠습니다. `hasMany`의 역방향 관계는 자식 모델에서 `belongsTo` 메서드를 사용해 정의합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Comment extends Model
{
    /**
     * 이 댓글이 속한 게시글을 반환합니다.
     */
    public function post(): BelongsTo
    {
        return $this->belongsTo(Post::class);
    }
}
```

이제 댓글의 `post` 동적 속성에 접근하여 부모 게시글을 가져올 수 있습니다.

```php
use App\Models\Comment;

$comment = Comment::find(1);

return $comment->post->title;
```

위 예시는 `Comment` 모델의 `post_id` 컬럼과 일치하는 `Post` 모델의 `id`를 찾아 반환합니다.

Eloquent는 관계 메서드 이름 뒤에 `_`와 부모 모델 기본키 컬럼명을 붙여 외래 키명을 자동으로 추정합니다. 예에서는 댓글 테이블의 외래 키가 `post_id`입니다.

연관관계의 외래 키 명이 다르거나, 부모 모델의 기본키가 `id`가 아닐 때는 아래처럼 두 번째, 세 번째 인수로 각각 외래 키와 부모의 키 컬럼명을 지정할 수 있습니다.

```php
/**
 * 이 댓글이 속한 게시글을 반환합니다.
 */
public function post(): BelongsTo
{
    return $this->belongsTo(Post::class, 'foreign_key');
}

public function post(): BelongsTo
{
    return $this->belongsTo(Post::class, 'foreign_key', 'owner_key');
}
```

<a name="default-models"></a>
#### 기본 모델(Default Models)

`belongsTo`, `hasOne`, `hasOneThrough`, `morphOne` 연관관계는 관련 데이터가 `null`일 경우 반환할 기본 모델을 지정할 수 있습니다. 이를 [Null Object 패턴](https://en.wikipedia.org/wiki/Null_Object_pattern)이라고 하며, 코드 내에서 조건문 사용을 줄일 수 있습니다. 예시에서, `Post`에 연관된 사용자가 없으면 빈 `App\Models\User` 모델이 반환됩니다.

```php
/**
 * 게시글의 작성자를 반환합니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault();
}
```

기본 모델에 속성 값을 지정하려면 `withDefault`에 배열이나 클로저를 인수로 전달할 수 있습니다.

```php
/**
 * 게시글의 작성자를 반환합니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault([
        'name' => 'Guest Author',
    ]);
}

/**
 * 게시글의 작성자를 반환합니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault(function (User $user, Post $post) {
        $user->name = 'Guest Author';
    });
}
```

<a name="querying-belongs-to-relationships"></a>
#### Belongs To 연관관계 질의하기

"Belongs To" 관계의 하위 모델을 질의할 때는, `where` 조건을 수동으로 작성해 Eloquent 모델을 조회할 수 있습니다.

```php
use App\Models\Post;

$posts = Post::where('user_id', $user->id)->get();
```

혹은, `whereBelongsTo` 메서드를 사용하면 연관관계와 외래 키를 자동으로 추론해서 더욱 간편하게 질의할 수 있습니다.

```php
$posts = Post::whereBelongsTo($user)->get();
```

[컬렉션](/docs/12.x/eloquent-collections) 인스턴스를 전달하는 것도 가능합니다. 이 경우 컬렉션 안의 모든 부모 모델에 속한 모델을 조회합니다.

```php
$users = User::where('vip', true)->get();

$posts = Post::whereBelongsTo($users)->get();
```

Laravel은 기본적으로 전달된 모델의 클래스명을 사용해 관계명을 결정하지만, `whereBelongsTo`의 두 번째 인수로 관계명을 직접 지정할 수도 있습니다.

```php
$posts = Post::whereBelongsTo($user, 'author')->get();
```

<a name="has-one-of-many"></a>
### 여러 개 중 하나를 가진 관계 (Has One of Many)

때로는 한 모델이 여러 개의 관련 모델을 가질 수 있는데, 그중 "최신" 혹은 "가장 오래된" 모델만 간편하게 조회하고 싶을 때가 있습니다. 예를 들어, `User` 모델이 여러 개의 `Order`와 연관되어 있지만, 사용자가 가장 최근에 주문한 주문만 쉽게 가져오는 방법을 원할 수 있습니다. 이것은 `hasOne` 관계와 `ofMany` 메서드를 조합해 구현할 수 있습니다.

```php
/**
 * 사용자의 가장 최근 주문을 반환합니다.
 */
public function latestOrder(): HasOne
{
    return $this->hasOne(Order::class)->latestOfMany();
}
```

마찬가지로, "가장 오래된" 또는 첫 번째 관련 모델을 조회할 수도 있습니다.

```php
/**
 * 사용자의 가장 오래된 주문을 반환합니다.
 */
public function oldestOrder(): HasOne
{
    return $this->hasOne(Order::class)->oldestOfMany();
}
```

`latestOfMany`, `oldestOfMany` 메서드는 디폴트로 모델의 기본키(정렬 가능한 컬럼 기준)로 최신/오래된 모델을 반환합니다. 하지만, 더 복잡한 정렬 기준으로 한 개의 모델만 가져오고 싶을 때는 `ofMany`를 사용할 수 있습니다. 첫 번째 인수로 정렬할 컬럼명을, 두 번째 인수로 적용할 집계 함수(`min`, `max`)를 지정합니다.

```php
/**
 * 사용자 주문 중에서 금액이 가장 큰 주문을 반환합니다.
 */
public function largestOrder(): HasOne
{
    return $this->hasOne(Order::class)->ofMany('price', 'max');
}
```

> [!WARNING]
> PostgreSQL은 UUID 컬럼에 대해 `MAX` 함수를 지원하지 않으므로, 현재 PostgreSQL UUID 컬럼과 one-of-many 관계는 함께 사용할 수 없습니다.

<a name="converting-many-relationships-to-has-one-relationships"></a>
#### "다수(HasMany)" 관계를 하나(HasOne) 관계로 변환하기

이미 `hasMany` 관계를 정의했더라도, `latestOfMany`, `oldestOfMany`, `ofMany` 메서드와 함께 사용할 때 `one` 메서드를 이용해 "has one" 관계로 쉽게 변환할 수 있습니다.

```php
/**
 * 사용자의 주문 목록을 반환합니다.
 */
public function orders(): HasMany
{
    return $this->hasMany(Order::class);
}

/**
 * 사용자의 금액이 가장 큰 주문을 반환합니다.
 */
public function largestOrder(): HasOne
{
    return $this->orders()->one()->ofMany('price', 'max');
}
```

`HasManyThrough` 관계도 `one` 메서드를 이용해 `HasOneThrough` 관계로 변환할 수 있습니다.

```php
public function latestDeployment(): HasOneThrough
{
    return $this->deployments()->one()->latestOfMany();
}
```

<a name="advanced-has-one-of-many-relationships"></a>
#### 고급 Has One of Many 관계

보다 복잡한 "여러 개 중 하나" 관계도 구현이 가능합니다. 예를 들어, `Product` 모델이 여러 개의 `Price`와 연결되어 있으며, 새로운 가격정보가 `published_at` 컬럼으로 미래에 미리 입력될 수도 있습니다. 이때 미래가 아닌 가장 최근에 게시된 가격을 가져오고, 게시일이 같을 경우 `id`가 큰 가격을 우선하도록 만들 수 있습니다.

`ofMany` 메서드로 정렬 컬럼을 배열로 전달하며, 두 번째 인수로 클로저를 전달해 추가 쿼리 조건을 정의할 수 있습니다.

```php
/**
 * 현재 기준 유효한 가격 정보를 반환합니다.
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
### 중간 모델을 통한 일대일(Has One Through) (Has One Through)

"Has One Through" 관계는 한 모델이 _중간_ 모델을 통해 다른 모델 하나와 연결될 때 사용합니다.

예를 들어, 자동차 정비소 앱에서 `Mechanic` 모델은 하나의 `Car`와, 각 `Car`는 하나의 `Owner`와 연결되어 있습니다. 정비사와 차주가 DB상 직접적으로 연결된 건 없지만, 정비사는 `Car` 모델을 _거쳐_ 자동차 소유주에 접근할 수 있습니다. 아래는 이러한 관계에 필요한 테이블 예시입니다.

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

이제 `Mechanic` 모델에 연관관계를 정의합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasOneThrough;

class Mechanic extends Model
{
    /**
     * 정비사가 맡은 자동차의 차주를 반환합니다.
     */
    public function carOwner(): HasOneThrough
    {
        return $this->hasOneThrough(Owner::class, Car::class);
    }
}
```

`hasOneThrough`의 첫 번째 인수는 최종적으로 접근할 모델(`Owner`), 두 번째 인수는 중간 모델(`Car`)입니다.

이미 관련된 모든 모델에 연관관계가 정의돼 있다면, `through` 메서드를 통해 문자열 혹은 동적 방식으로도 "Has One Through"를 정의할 수 있습니다.

```php
// 문자열 방식...
return $this->through('cars')->has('owner');

// 동적 방식...
return $this->throughCars()->hasOwner();
```

<a name="has-one-through-key-conventions"></a>
#### 키 컨벤션

관례적으로, Eloquent는 쿼리에서 자동으로 외래 키 규칙을 사용합니다. 키를 커스터마이즈하려면, `hasOneThrough`의 세 번째(중간 모델의 외래 키), 네 번째(최종 모델의 외래 키), 다섯 번째(부모 테이블의 로컬 키), 여섯 번째(중간 모델의 로컬 키) 인수에 지정합니다.

```php
class Mechanic extends Model
{
    /**
     * 정비사가 맡은 자동차의 차주를 반환합니다.
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

이미 각 모델에 연관관계가 정의되어 있다면, `through` 메서드를 사용해 기존 키 규칙을 재사용할 수 있습니다.

```php
// 문자열 방식...
return $this->through('cars')->has('owner');

// 동적 방식...
return $this->throughCars()->hasOwner();
```

<a name="has-many-through"></a>
### 중간 모델을 통한 일대다(Has Many Through) (Has Many Through)

"Has Many Through" 관계는 중간 연관관계를 거쳐 먼 거리에 있는 모델들에 접근할 때 편리하게 사용할 수 있습니다. 예를 들어, [Laravel Cloud](https://cloud.laravel.com)와 같은 배포 플랫폼에서, `Application` 모델은 중간 `Environment` 모델을 거쳐 여러 개의 `Deployment`와 연결될 수 있습니다.

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

이제 `Application` 모델에 아래와 같이 연관관계를 정의합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasManyThrough;

class Application extends Model
{
    /**
     * 이 애플리케이션의 모든 배포 내역을 반환합니다.
     */
    public function deployments(): HasManyThrough
    {
        return $this->hasManyThrough(Deployment::class, Environment::class);
    }
}
```

`hasManyThrough`의 첫 번째 인수는 최종 모델(`Deployment`), 두 번째 인수는 중간 모델(`Environment`)입니다.

또한, 각 모델이 이미 연관관계를 가지고 있다면 `through` 메서드로 아래와 같이 선언할 수도 있습니다.

```php
// 문자열 방식...
return $this->through('environments')->has('deployments');

// 동적 방식...
return $this->throughEnvironments()->hasDeployments();
```

`deployment` 테이블에 `application_id`가 없더라도, `HasManyThrough`는 중간인 `environments` 테이블의 `application_id`로 환경 ID 들을 모아 `deployments`에서 해당 환경의 배포 내역을 가져오게 됩니다.

<a name="has-many-through-key-conventions"></a>
#### 키 컨벤션

기본적으로 Eloquent는 쿼리시에 외래 키 규칙을 자동으로 적용합니다. 키를 직접 지정하려면 `hasManyThrough`의 세 번째(중간 모델의 외래 키), 네 번째(최종 모델의 외래 키), 다섯 번째(부모 테이블의 로컬 키), 여섯 번째(중간 모델의 로컬 키) 인수로 전달합니다.

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

기존에 이미 정의된 연관관계를 사용한다면 `through` 메서드를 통해 키 규칙을 재사용할 수 있습니다.

```php
// 문자열 방식...
return $this->through('environments')->has('deployments');

// 동적 방식...
return $this->throughEnvironments()->hasDeployments();
```

<a name="scoped-relationships"></a>
### 스코프드 연관관계 (Scoped Relationships)

관계에 제약조건을 추가하고 싶은 경우가 종종 있습니다. 예를 들어, `User` 모델에 `posts` 외에 `featuredPosts`라는 메서드를 만들어, 게시글 중에서도 `featured`가 `true`인 게시글만 가져올 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class User extends Model
{
    /**
     * 사용자의 게시글 목록을 반환합니다.
     */
    public function posts(): HasMany
    {
        return $this->hasMany(Post::class)->latest();
    }

    /**
     * 사용자의 대표(특정 조건) 게시글 목록을 반환합니다.
     */
    public function featuredPosts(): HasMany
    {
        return $this->posts()->where('featured', true);
    }
}
```

하지만 위와 같이 관계 메서드를 통해 모델을 생성하면, 자동으로 `featured` 속성이 `true`로 저장되지 않습니다. 관계 메서드로 생성된 모든 모델에 특정 속성을 자동으로 추가하려면 `withAttributes` 메서드를 사용하여 관계 정의 시 미리 지정할 수 있습니다.

```php
/**
 * 사용자의 대표 게시글 목록을 반환합니다.
 */
public function featuredPosts(): HasMany
{
    return $this->posts()->withAttributes(['featured' => true]);
}
```

`withAttributes`는 지정한 조건으로 `where`절을 쿼리에 추가하고, 관계 메서드를 사용할 때 생성되는 모델에도 해당 속성값을 세팅합니다.

```php
$post = $user->featuredPosts()->create(['title' => 'Featured Post']);

$post->featured; // true
```

`withAttributes`를 사용할 때 두 번째 인자인 `asConditions`를 `false`로 설정하면, 쿼리 조건 추가 없이 모델 생성 시에만 속성이 부여됩니다.

```php
return $this->posts()->withAttributes(['featured' => true], asConditions: false);
```

---

(이후 내용도 위 형식에 맞춰 번역됩니다. 답변이 너무 길어지므로, 필요 시 이어서 요청해 주세요.)