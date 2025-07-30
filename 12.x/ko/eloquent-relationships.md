# Eloquent: 관계 (Eloquent: Relationships)

- [소개](#introduction)
- [관계 정의하기](#defining-relationships)
    - [일대일 / Has One](#one-to-one)
    - [일대다 / Has Many](#one-to-many)
    - [일대다 반대 / Belongs To](#one-to-many-inverse)
    - [Has One of Many](#has-one-of-many)
    - [Has One Through](#has-one-through)
    - [Has Many Through](#has-many-through)
- [제한된 관계 (Scoped Relationships)](#scoped-relationships)
- [다대다 관계 (Many to Many)](#many-to-many)
    - [중간 테이블 컬럼 가져오기](#retrieving-intermediate-table-columns)
    - [중간 테이블 컬럼으로 쿼리 필터링](#filtering-queries-via-intermediate-table-columns)
    - [중간 테이블 컬럼으로 정렬하기](#ordering-queries-via-intermediate-table-columns)
    - [커스텀 중간 테이블 모델 정의하기](#defining-custom-intermediate-table-models)
- [다형성 관계 (Polymorphic Relationships)](#polymorphic-relationships)
    - [일대일](#one-to-one-polymorphic-relations)
    - [일대다](#one-to-many-polymorphic-relations)
    - [One of Many](#one-of-many-polymorphic-relations)
    - [다대다](#many-to-many-polymorphic-relations)
    - [커스텀 다형성 타입](#custom-polymorphic-types)
- [동적 관계 (Dynamic Relationships)](#dynamic-relationships)
- [관계 쿼리하기](#querying-relations)
    - [관계 메서드와 동적 속성 차이](#relationship-methods-vs-dynamic-properties)
    - [관계 존재 쿼리하기](#querying-relationship-existence)
    - [관계 부재 쿼리하기](#querying-relationship-absence)
    - [Morph To 관계 쿼리하기](#querying-morph-to-relationships)
- [관련 모델 집계하기](#aggregating-related-models)
    - [관련 모델 개수 세기](#counting-related-models)
    - [기타 집계 함수](#other-aggregate-functions)
    - [Morph To 관계 관련 모델 개수 세기](#counting-related-models-on-morph-to-relationships)
- [즉시 로딩 (Eager Loading)](#eager-loading)
    - [즉시 로딩 제약 조건](#constraining-eager-loads)
    - [지연 즉시 로딩](#lazy-eager-loading)
    - [자동 즉시 로딩](#automatic-eager-loading)
    - [지연 로딩 방지하기](#preventing-lazy-loading)
- [관련 모델 삽입 및 수정](#inserting-and-updating-related-models)
    - [`save` 메서드](#the-save-method)
    - [`create` 메서드](#the-create-method)
    - [Belongs To 관계 갱신](#updating-belongs-to-relationships)
    - [Many to Many 관계 갱신](#updating-many-to-many-relationships)
- [부모 타임스탬프 갱신 (Touching Parent Timestamps)](#touching-parent-timestamps)

<a name="introduction"></a>
## 소개 (Introduction)

데이터베이스 테이블은 종종 서로 관계를 맺습니다. 예를 들어, 블로그 게시물은 댓글 여러 개를 가질 수 있고, 주문은 주문한 사용자와 관계를 가질 수 있습니다. Eloquent는 이러한 관계를 쉽게 관리하고 사용할 수 있도록 해주며, 일반적으로 많이 쓰이는 여러 관계 유형을 지원합니다:

<div class="content-list" markdown="1">

- [일대일 관계 (One To One)](#one-to-one)
- [일대다 관계 (One To Many)](#one-to-many)
- [다대다 관계 (Many To Many)](#many-to-many)
- [Has One Through](#has-one-through)
- [Has Many Through](#has-many-through)
- [다형성 일대일 (One To One Polymorphic)](#one-to-one-polymorphic-relations)
- [다형성 일대다 (One To Many Polymorphic)](#one-to-many-polymorphic-relations)
- [다형성 다대다 (Many To Many Polymorphic)](#many-to-many-polymorphic-relations)

</div>

<a name="defining-relationships"></a>
## 관계 정의하기 (Defining Relationships)

Eloquent 관계는 Eloquent 모델 클래스의 메서드로 정의합니다. 관계는 강력한 [쿼리 빌더](/docs/12.x/queries) 역할도 하므로, 메서드로 정의하면 체이닝과 쿼리 기능을 훨씬 강력하게 활용할 수 있습니다. 예를 들어, `posts` 관계에 추가 조건을 붙일 수 있습니다:

```php
$user->posts()->where('active', 1)->get();
```

관계 사용법을 더 깊이 배우기 전에, Eloquent가 지원하는 각 관계 유형을 어떻게 정의하는지 먼저 살펴보겠습니다.

<a name="one-to-one"></a>
### 일대일 / Has One (One to One / Has One)

일대일 관계는 가장 기본적인 데이터베이스 관계 유형 중 하나입니다. 예를 들어, 하나의 `User` 모델이 하나의 `Phone` 모델과 관련될 수 있습니다. 이 관계를 정의하려면 `User` 모델에 `phone` 메서드를 추가하고, 그 안에서 `hasOne` 메서드를 호출해 결과를 반환해야 합니다. `hasOne` 메서드는 `Illuminate\Database\Eloquent\Model` 기본 클래스를 통해 모델에서 사용할 수 있습니다:

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

`hasOne` 메서드에 전달하는 첫 번째 인수는 관련 모델 클래스 명입니다. 관계가 정의된 후에는 Eloquent의 동적 속성(dynamic properties)을 통해 관련 레코드에 접근할 수 있습니다. 동적 속성을 이용하면 실제 모델에 정의된 것처럼 관계 메서드를 속성처럼 사용할 수 있습니다:

```php
$phone = User::find(1)->phone;
```

Eloquent는 부모 모델 이름을 기반으로 관계의 외래 키(foreign key)를 추론합니다. 이 경우 `Phone` 모델은 `user_id` 컬럼을 외래 키로 자동 가정합니다. 이 규칙을 변경하려면 `hasOne` 메서드에 두 번째 인수로 외래 키 이름을 전달할 수 있습니다:

```php
return $this->hasOne(Phone::class, 'foreign_key');
```

또한, 외래 키에 저장된 값이 부모 모델의 기본 키 컬럼 값(`id` 또는 모델의 `$primaryKey`)과 일치해야 한다고 가정합니다. 만약 기본 키가 다르거나 특정 키를 사용하려면 `hasOne` 메서드의 세 번째 인수에 로컬 키 이름을 전달할 수 있습니다:

```php
return $this->hasOne(Phone::class, 'foreign_key', 'local_key');
```

<a name="one-to-one-defining-the-inverse-of-the-relationship"></a>
#### 관계의 역관계 정의하기 (Defining the Inverse of the Relationship)

`User` 모델에서 `Phone`에 접근할 수 있다면, 이제 `Phone` 모델에서 해당 전화번호를 가진 사용자를 참조하는 관계를 정의해보겠습니다. `hasOne` 관계의 역은 `belongsTo` 메서드로 정의할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Phone extends Model
{
    /**
     * 이 전화번호를 소유한 사용자 가져오기
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }
}
```

`user` 메서드를 호출하면, Eloquent는 `Phone` 모델의 `user_id` 컬럼과 `User` 모델의 `id` 컬럼 값을 비교하여 일치하는 `User` 모델을 찾습니다.

Eloquent는 관계 메서드 이름을 살펴보고 `_id`를 붙여 외래 키 이름을 결정합니다. 이 예제에서는 `user_id` 컬럼으로 가정됩니다. 만약 외래 키가 다르다면 두 번째 인수로 직접 외래 키 이름을 지정할 수 있습니다:

```php
/**
 * 이 전화번호를 소유한 사용자 가져오기
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class, 'foreign_key');
}
```

부모 모델이 `id`를 기본 키로 사용하지 않거나 다른 컬럼으로 연관 모델을 찾으려면, 세 번째 인수에 부모 테이블의 커스텀 키를 지정할 수 있습니다:

```php
/**
 * 이 전화번호를 소유한 사용자 가져오기
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class, 'foreign_key', 'owner_key');
}
```

<a name="one-to-many"></a>
### 일대다 / Has Many (One to Many / Has Many)

일대다 관계는 하나의 부모 모델이 여러 자식 모델과 연관되는 경우 사용합니다. 예를 들어, 블로그 게시물 하나가 무한히 많은 댓글을 가질 수 있습니다. 모든 Eloquent 관계처럼, 일대다 관계도 모델에 메서드를 정의해서 만듭니다:

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

Eloquent는 `Comment` 모델에 대한 올바른 외래 키 컬럼을 자동으로 추론합니다. 규칙에 따라 부모 모델 이름을 "스네이크 케이스"로 변환한 뒤 `_id`를 붙입니다. 이 예제에서는 `post_id`가 됩니다.

관계 메서드를 정의한 후에는 [컬렉션](/docs/12.x/eloquent-collections) 형태로 댓글들에 접근할 수 있습니다. Eloquent가 제공하는 "동적 관계 속성" 덕분에 실제 속성처럼 관계 메서드를 사용할 수 있습니다:

```php
use App\Models\Post;

$comments = Post::find(1)->comments;

foreach ($comments as $comment) {
    // ...
}
```

모든 관계는 쿼리 빌더 역할을 하므로, 관계 메서드를 호출한 뒤 추가 조건을 체이닝할 수 있습니다:

```php
$comment = Post::find(1)->comments()
    ->where('title', 'foo')
    ->first();
```

`hasOne`처럼 `hasMany`도 외래 키, 로컬 키를 두 번째, 세 번째 인수로 변경할 수 있습니다:

```php
return $this->hasMany(Comment::class, 'foreign_key');

return $this->hasMany(Comment::class, 'foreign_key', 'local_key');
```

<a name="automatically-hydrating-parent-models-on-children"></a>
#### 자식 모델에서 부모 모델 자동 할당하기

Eloquent의 즉시 로딩(eager loading)을 사용해도 자식 모델을 반복하면서 부모 모델에 접근하면 "N + 1" 문제(쿼리 수가 크게 증가)가 발생할 수 있습니다:

```php
$posts = Post::with('comments')->get();

foreach ($posts as $post) {
    foreach ($post->comments as $comment) {
        echo $comment->post->title;
    }
}
```

위 예제에서 즉시 로딩으로 `comments`는 미리 로드했지만, 각각의 `Comment` 모델에서 다시 부모 모델(`Post`)을 따로 쿼리하게 되어 N + 1 문제가 생깁니다.

부모 모델을 자동으로 자식에 할당하려면, `hasMany` 관계에서 `chaperone` 메서드를 호출합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Post extends Model
{
    /**
     * 블로그 게시글 댓글 가져오기
     */
    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class)->chaperone();
    }
}
```

또는 실행 시점에서 즉시 로딩할 때 `chaperone`을 호출해도 됩니다:

```php
use App\Models\Post;

$posts = Post::with([
    'comments' => fn ($comments) => $comments->chaperone(),
])->get();
```

<a name="one-to-many-inverse"></a>
### 일대다 역관계 / Belongs To (One to Many (Inverse) / Belongs To)

게시물의 모든 댓글을 가져올 수 있으니, 반대로 댓글에서 자신의 부모 게시물을 가져오는 관계도 정의할 수 있습니다. `hasMany`의 역관계는 자식 모델에 `belongsTo` 메서드를 사용하는 관계 메서드를 정의하면 됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Comment extends Model
{
    /**
     * 댓글의 부모 게시물 가져오기
     */
    public function post(): BelongsTo
    {
        return $this->belongsTo(Post::class);
    }
}
```

관계 정의 후 `post` 동적 속성으로 댓글의 부모 게시물을 호출할 수 있습니다:

```php
use App\Models\Comment;

$comment = Comment::find(1);

return $comment->post->title;
```

Eloquent는 `post_id` 컬럼과 `Post` 모델의 `id` 값을 기준으로 부모 모델을 찾습니다.

외래 키 명을 기본 규칙대로 `post_id` 가 아닌 다른 이름으로 쓴다면 두 번째 인수에 직접 전달할 수 있습니다:

```php
/**
 * 댓글의 부모 게시물 가져오기
 */
public function post(): BelongsTo
{
    return $this->belongsTo(Post::class, 'foreign_key');
}
```

기본 키가 `id`가 아닐 때나 다른 컬럼 기준으로 찾으려면 세 번째 인수에 로컬 키를 지정합니다:

```php
/**
 * 댓글의 부모 게시물 가져오기
 */
public function post(): BelongsTo
{
    return $this->belongsTo(Post::class, 'foreign_key', 'owner_key');
}
```

<a name="default-models"></a>
#### 기본 모델(Default Models)

`belongsTo`, `hasOne`, `hasOneThrough`, `morphOne` 같은 관계는 관계 결과가 `null`일 때 반환할 기본 모델을 지정할 수 있습니다. 이 방식은 [Null Object 패턴](https://en.wikipedia.org/wiki/Null_Object_pattern)이라고 하며 코드 내 조건문을 줄여줍니다.

예를 들어, 사용자가 없으면 빈 `App\Models\User` 모델을 반환하도록 `user` 관계에 `withDefault()`를 호출할 수 있습니다:

```php
/**
 * 게시물의 작성자 가져오기
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault();
}
```

기본 모델에 속성을 넣으려면 배열이나 클로저를 전달할 수 있습니다:

```php
/**
 * 게시물의 작성자 가져오기
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault([
        'name' => 'Guest Author',
    ]);
}

/**
 * 게시물의 작성자 가져오기
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

부모 모델의 자식 모델을 조회 시 직접 `where` 조건을 써서 쿼리할 수 있습니다:

```php
use App\Models\Post;

$posts = Post::where('user_id', $user->id)->get();
```

또는 `whereBelongsTo` 메서드를 활용하면 관계와 외래 키를 자동으로 판단해서 좀 더 간결하게 쿼리할 수 있습니다:

```php
$posts = Post::whereBelongsTo($user)->get();
```

이 메서드에 [컬렉션](/docs/12.x/eloquent-collections)을 인수로 전달하면 해당 집합에 속한 모든 부모 모델에 대한 자식 모델들을 조회합니다:

```php
$users = User::where('vip', true)->get();

$posts = Post::whereBelongsTo($users)->get();
```

모델 이름으로 관계를 추론하지만 두 번째 인수에 관계명 문자열을 직접 지정할 수도 있습니다:

```php
$posts = Post::whereBelongsTo($user, 'author')->get();
```

<a name="has-one-of-many"></a>
### Has One of Many

때때로 하나의 모델에 여러 관련 모델이 있지만, 가장 최신 또는 가장 오래된 하나만 쉽게 가져오고 싶을 때가 있습니다. 예를 들어, `User` 모델은 여러 `Order`를 가질 수 있지만, 가장 최근 주문을 편리하게 접근하고 싶을 수 있습니다. 이럴 때 `hasOne` 관계와 `ofMany` 메서드를 함께 사용합니다:

```php
/**
 * 사용자의 가장 최근 주문 가져오기
 */
public function latestOrder(): HasOne
{
    return $this->hasOne(Order::class)->latestOfMany();
}
```

반대로 가장 오래된 주문을 가져오고 싶다면:

```php
/**
 * 사용자의 가장 오래된 주문 가져오기
 */
public function oldestOrder(): HasOne
{
    return $this->hasOne(Order::class)->oldestOfMany();
}
```

기본적으로 `latestOfMany`와 `oldestOfMany`는 정렬 가능한 기본 키 컬럼 기준 최신/최초을 가져옵니다. 만약 다른 정렬 기준으로 단일 모델을 뽑고 싶으면 `ofMany` 메서드를 이용할 수 있습니다.

예를 들어, 가격이 가장 높은 주문을 구할 때 `ofMany`는 첫 인수에 정렬할 컬럼명, 두 번째 인수에 집계 함수(`min` 또는 `max`)를 받습니다:

```php
/**
 * 사용자의 가장 큰 주문(가격 기준) 가져오기
 */
public function largestOrder(): HasOne
{
    return $this->hasOne(Order::class)->ofMany('price', 'max');
}
```

> [!WARNING]
> PostgreSQL은 UUID 컬럼에 대해 `MAX` 함수를 지원하지 않으므로, 현재 PostgreSQL UUID 컬럼과 함께 one-of-many 관계를 사용할 수 없습니다.

<a name="converting-many-relationships-to-has-one-relationships"></a>
#### "많은" 관계를 Has One 관계로 변환하기

`latestOfMany`, `oldestOfMany`, `ofMany` 메서드로 단일 모델을 가져올 때, 이미 대상 모델에 `hasMany` 관계가 정의되어 있을 수 있습니다. 이럴 땐 `one` 메서드를 호출해 편리하게 "has one" 관계로 변환할 수 있습니다:

```php
/**
 * 사용자의 모든 주문
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

`one` 메서드는 `HasManyThrough` 관계도 `HasOneThrough` 관계로 변환합니다:

```php
public function latestDeployment(): HasOneThrough
{
    return $this->deployments()->one()->latestOfMany();
}
```

<a name="advanced-has-one-of-many-relationships"></a>
#### 고급 Has One of Many 관계

더 복잡한 상황에서 `ofMany` 메서드에 여러 정렬 조건을 배열로 넘기고, 추가 조건 클로저도 전달할 수 있습니다.

예를 들어, `Product`가 여러 `Price` 모델을 가지되 `published_at` 미래 시점 데이터는 제외하고 최신 가격을 가져오고 싶을 때:

```php
/**
 * 현재 가격 가져오기
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

"has one through" 관계는 세 모델 간 관계를 연결해 중간 모델을 거쳐 최종 모델과 일대일 관계를 정의할 때 사용합니다.

예를 들어, 자동차 수리점 앱이 있다고 가정해봅시다. `Mechanic` 모델은 여러 `Car` 모델과 연관되며, `Car` 모델은 하나의 `Owner` 모델과 연결됩니다. 수리공과 오너는 데이터베이스 상에서 직접 연결돼 있지 않으나, 수리공은 자동차(`Car`)를 통해 오너(`Owner`)에 접근할 수 있습니다.

테이블 구조 예시:

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

`Mechanic` 모델에 관계 정의:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasOneThrough;

class Mechanic extends Model
{
    /**
     * 자동차의 오너 가져오기
     */
    public function carOwner(): HasOneThrough
    {
        return $this->hasOneThrough(Owner::class, Car::class);
    }
}
```

`hasOneThrough` 첫 번째 인수는 최종 모델명(`Owner`), 두 번째는 중간 모델명(`Car`)입니다.

모든 관련 모델에 이미 관계가 정의되어 있으면, `through` 메서드에 관계명을 넘겨 체이닝 방식으로도 정의할 수 있습니다:

```php
// 문자열 표기법
return $this->through('cars')->has('owner');

// 동적 메서드 표기법
return $this->throughCars()->hasOwner();
```

<a name="has-one-through-key-conventions"></a>
#### 키 규칙 (Key Conventions)

관계 쿼리에 Eloquent 기본 키 규칙이 적용됩니다. 필요시 `hasOneThrough` 메서드에 세 번째와 네 번째 인수로 각각 중간 모델과 최종 모델의 외래 키 명, 다섯 번째와 여섯 번째 인수로 각각 부모 모델과 중간 모델의 로컬 키를 지정할 수 있습니다:

```php
class Mechanic extends Model
{
    /**
     * 자동차의 오너 가져오기
     */
    public function carOwner(): HasOneThrough
    {
        return $this->hasOneThrough(
            Owner::class,
            Car::class,
            'mechanic_id', // cars 테이블 외래 키
            'car_id',      // owners 테이블 외래 키
            'id',          // mechanics 테이블 로컬 키
            'id'           // cars 테이블 로컬 키
        );
    }
}
```

앞서 설명한 `through` 메서드 방식도 사용할 수 있습니다.

<a name="has-many-through"></a>
### Has Many Through

"has many through"는 중간 모델을 거쳐 여러 관련 모델에 접근할 때 편리한 관계입니다.

예를 들어, 배포 플랫폼에서 `Application` 모델은 여러 `Deployment` 모델을 `Environment` 모델을 통해 접근할 수 있습니다.

테이블 구조:

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

`Application` 모델에 관계 정의:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasManyThrough;

class Application extends Model
{
    /**
     * 애플리케이션의 모든 배포 내역 가져오기
     */
    public function deployments(): HasManyThrough
    {
        return $this->hasManyThrough(Deployment::class, Environment::class);
    }
}
```

첫 인수는 최종 모델 (Deployment), 두 번째는 중간 모델 (Environment)입니다.

이미 각 모델에 관련 관계가 정의돼 있다면 `through` 메서드로 연결할 수 있습니다:

```php
// 문자열 표기법
return $this->through('environments')->has('deployments');

// 동적 메서드 표기법
return $this->throughEnvironments()->hasDeployments();
```

중간 모델 `environments` 테이블 `application_id` 컬럼, 최종 모델 `deployments` 테이블 `environment_id` 컬럼을 기반으로 쿼리가 이루어집니다.

<a name="has-many-through-key-conventions"></a>
#### 키 규칙 (Key Conventions)

기본 Eloquent 외래 키 규칙이 적용되며, 필요하면 세 번째부터 여섯 번째 인수로 각각 중간 모델 외래 키, 최종 모델 외래 키, 부모 모델 로컬 키, 중간 모델 로컬 키를 지정할 수 있습니다:

```php
class Application extends Model
{
    public function deployments(): HasManyThrough
    {
        return $this->hasManyThrough(
            Deployment::class,
            Environment::class,
            'application_id', // 중간 모델 외래 키
            'environment_id', // 최종 모델 외래 키
            'id',             // 애플리케이션 로컬 키
            'id'              // 중간 모델 로컬 키
        );
    }
}
```

`through` 메서드 체이닝 방식도 사용할 수 있습니다.

<a name="scoped-relationships"></a>
### 제한된 관계 (Scoped Relationships)

종종 기존 관계에 조건을 추가해서 범위가 제한된 관계를 정의하는 경우가 있습니다.

예를 들어, `User` 모델이 여러 `Post`를 가지는데 그 중 `featured` 컬럼이 `true`인 게시물만 필터링하는 `featuredPosts` 메서드를 추가할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class User extends Model
{
    /**
     * 유저가 가진 모든 게시글
     */
    public function posts(): HasMany
    {
        return $this->hasMany(Post::class)->latest();
    }

    /**
     * 유저가 가진 추천 게시물
     */
    public function featuredPosts(): HasMany
    {
        return $this->posts()->where('featured', true);
    }
}
```

단, `featuredPosts` 관계를 통해 모델을 생성하면 `featured` 속성이 자동 지정되지 않습니다. 관계로 생성하는 모델에 기본 속성을 추가하려면 `withAttributes` 메서드를 사용하세요:

```php
/**
 * 유저가 가진 추천 게시물
 */
public function featuredPosts(): HasMany
{
    return $this->posts()->withAttributes(['featured' => true]);
}
```

이렇게 하면 `where` 조건도 걸리고, 관계를 통해 생성한 모델에도 자동으로 `featured` 속성이 추가됩니다:

```php
$post = $user->featuredPosts()->create(['title' => 'Featured Post']);

$post->featured; // true
```

`withAttributes` 두 번째 인수 `asConditions`를 `false`로 설정하면 `where` 조건 추가를 방지할 수 있습니다:

```php
return $this->posts()->withAttributes(['featured' => true], asConditions: false);
```

<a name="many-to-many"></a>
## 다대다 관계 (Many to Many Relationships)

다대다 관계는 `hasOne`, `hasMany`보다 다소 복잡합니다. 예를 들어, 사용자 하나가 여러 역할(roles)을 가지며 역할도 여러 사용자에게 부여될 수 있는 경우입니다. 이때 한 사용자는 "Author", "Editor" 역할을 동시에 가질 수 있으며, 다른 사용자도 같은 역할을 가질 수 있습니다.

<a name="many-to-many-table-structure"></a>
#### 테이블 구조

이를 위해 3개의 테이블이 필요합니다: `users`, `roles`, 그리고 두 테이블을 연결하는 중간 테이블 `role_user`가 필요합니다.

`role_user` 테이블은 관련 모델명을 알파벳 순으로 조합해 만들고 `user_id`, `role_id` 컬럼을 포함합니다. 이 테이블이 중간자 역할로 연결 고리를 제공합니다.

`roles` 테이블에 단순히 `user_id` 컬럼을 넣으면 한 역할이 하나의 사용자만 가질 수 있어, 다중 사용자 할당이 안 됩니다. 다중 관계를 위해 중간 테이블이 꼭 필요합니다.

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

다대다 관계는 해당 관계를 반환하는 메서드로 정의하며, 메서드는 `belongsToMany` 메서드를 호출하고 반환합니다. `belongsToMany`는 모든 Eloquent 모델 기본 클래스에서 사용 가능합니다.

예를 들어 `User` 모델에 `roles` 메서드를 추가해보겠습니다. 첫 인수는 관련 모델 클래스명입니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class User extends Model
{
    /**
     * 유저가 가진 역할들
     */
    public function roles(): BelongsToMany
    {
        return $this->belongsToMany(Role::class);
    }
}
```

관계 정의 후 `roles` 동적 속성으로 역할 목록에 접근할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

foreach ($user->roles as $role) {
    // ...
}
```

관계는 쿼리 빌더이므로, 관계 메서드 호출 후 조건 체이닝 가능합니다:

```php
$roles = User::find(1)->roles()->orderBy('name')->get();
```

중간 테이블명은 관련 모델명을 알파벳 기준으로 조합하여 결정하지만, 두 번째 인수로 직접 지정할 수 있습니다:

```php
return $this->belongsToMany(Role::class, 'role_user');
```

중간 테이블 키 컬럼은 세 번째와 네 번째 인수로 지정할 수 있습니다. 세 번째가 현재 모델의 외래 키, 네 번째가 연결할 모델 외래 키입니다:

```php
return $this->belongsToMany(Role::class, 'role_user', 'user_id', 'role_id');
```

<a name="many-to-many-defining-the-inverse-of-the-relationship"></a>
#### 역관계 정의하기

다대다 관계의 역도 같은 `belongsToMany` 메서드를 정의하면 됩니다. 사용자-역할 예제에서 `Role` 모델에 `users` 메서드를 정의합시다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class Role extends Model
{
    /**
     * 이 역할에 속한 유저들
     */
    public function users(): BelongsToMany
    {
        return $this->belongsToMany(User::class);
    }
}
```

기본적으로 `User` 모델과 같은 방식으로 관계를 정의합니다.

<a name="retrieving-intermediate-table-columns"></a>
### 중간 테이블 컬럼 가져오기 (Retrieving Intermediate Table Columns)

다대다 관계 탐색 후, 각 관련 모델에서 `pivot` 속성으로 중간 테이블 데이터에 접근할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

foreach ($user->roles as $role) {
    echo $role->pivot->created_at;
}
```

`pivot`은 중간 테이블 모델을 의미하며 기본적으로 키 컬럼만 포함합니다. 추가 컬럼이 있으면 관계 정의 시 `withPivot` 메서드를 호출해 명시해야 합니다:

```php
return $this->belongsToMany(Role::class)->withPivot('active', 'created_by');
```

`created_at`, `updated_at` 타임스탬프가 자동 관리되도록 지정하려면 `withTimestamps`를 호출하세요:

```php
return $this->belongsToMany(Role::class)->withTimestamps();
```

> [!WARNING]
> 자동 관리되는 타임스탬프가 있을 때는 중간 테이블에 반드시 `created_at`과 `updated_at` 컬럼이 모두 존재해야 합니다.

<a name="customizing-the-pivot-attribute-name"></a>
#### `pivot` 속성명 변경하기

`pivot` 속성명은 애플리케이션 용도에 맞게 변경할 수 있습니다.

예를 들어 사용자가 팟캐스트를 구독하는 시스템에서 중간 테이블을 `subscription`이라는 이름으로 사용하고 싶다면 `as` 메서드를 이용:

```php
return $this->belongsToMany(Podcast::class)
    ->as('subscription')
    ->withTimestamps();
```

그 후, `subscription`으로 중간 테이블 컬럼에 접근할 수 있습니다:

```php
$users = User::with('podcasts')->get();

foreach ($users->flatMap->podcasts as $podcast) {
    echo $podcast->subscription->created_at;
}
```

<a name="filtering-queries-via-intermediate-table-columns"></a>
### 중간 테이블 컬럼으로 쿼리 필터링 (Filtering Queries via Intermediate Table Columns)

`belongsToMany` 쿼리를 필터링할 때, `wherePivot`, `wherePivotIn`, `wherePivotNotIn`, `wherePivotBetween`, `wherePivotNotBetween`, `wherePivotNull`, `wherePivotNotNull` 메서드를 사용할 수 있습니다.

예:

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

`wherePivot`는 쿼리 조건으로 걸리지만, 새로운 모델 생성 시 값 자동으로 추가하지 않습니다. 삽입 시에도 조건이 적용되려면 `withPivotValue`를 씁니다:

```php
return $this->belongsToMany(Role::class)
    ->withPivotValue('approved', 1);
```

<a name="ordering-queries-via-intermediate-table-columns"></a>
### 중간 테이블 컬럼으로 정렬하기 (Ordering Queries via Intermediate Table Columns)

`orderByPivot` 메서드로 중간 테이블 컬럼을 기준으로 정렬할 수 있습니다:

```php
return $this->belongsToMany(Badge::class)
    ->where('rank', 'gold')
    ->orderByPivot('created_at', 'desc');
```

<a name="defining-custom-intermediate-table-models"></a>
### 커스텀 중간 테이블 모델 정의하기 (Defining Custom Intermediate Table Models)

중간 테이블에 커스텀 동작(메서드, 캐스트 등)을 추가하고 싶으면 `using` 메서드로 커스텀 Pivot 모델 클래스를 연결합니다.

커스텀 모델은 `Illuminate\Database\Eloquent\Relations\Pivot` 클래스를 상속해야 하며, 다형성 관계라면 `MorphPivot` 상속합니다.

예:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class Role extends Model
{
    /**
     * 역할에 속한 사용자들
     */
    public function users(): BelongsToMany
    {
        return $this->belongsToMany(User::class)->using(RoleUser::class);
    }
}
```

`RoleUser` 모델 정의:

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
> Pivot 모델에 `SoftDeletes` 트레이트를 사용할 수 없습니다. 소프트 삭제가 필요하면 실제 Eloquent 모델로 변경하는 것을 권장합니다.

<a name="custom-pivot-models-and-incrementing-ids"></a>
#### 자동 증가형 ID인 커스텀 Pivot 모델

커스텀 Pivot 모델이 자동 증가 키를 사용하는 경우 `public $incrementing = true;` 속성을 명시해야 합니다:

```php
/**
 * 자동 증가 키 여부
 *
 * @var bool
 */
public $incrementing = true;
```

<a name="polymorphic-relationships"></a>
## 다형성 관계 (Polymorphic Relationships)

다형성 관계는 자식 모델이 여러 종류 모델에 속할 수 있도록 단일 연관 관계를 사용하는 방식입니다. 예를 들어, 사용자가 블로그 게시물과 동영상을 공유하는 앱에서 `Comment` 모델이 `Post`와 `Video` 모델 둘 다에 연결될 수 있습니다.

<a name="one-to-one-polymorphic-relations"></a>
### 일대일 다형성 (One to One Polymorphic)

<a name="one-to-one-polymorphic-table-structure"></a>
#### 테이블 구조

일대일 다형성 관계는 일반 일대일처럼 생겼으나, 단일 자식 테이블이 여러 종류 모델과 연관됩니다.

예를 들어 블로그 `Post`와 `User` 모델이 `Image` 모델과 다형성 관계를 가진다면, 이미지 테이블을 하나만 둘 수 있습니다:

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

`images` 테이블의 `imageable_id`는 `Post`나 `User`의 ID를, `imageable_type`은 클래스명을 담습니다. `imageable_type`이 `App\Models\Post` 또는 `App\Models\User`가 됩니다.

<a name="one-to-one-polymorphic-model-structure"></a>
#### 모델 구조

모델 정의 예시:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class Image extends Model
{
    /**
     * 부모 imageable 모델 (user 또는 post) 가져오기
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
     * 게시물의 이미지 가져오기
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
     * 사용자의 이미지 가져오기
     */
    public function image(): MorphOne
    {
        return $this->morphOne(Image::class, 'imageable');
    }
}
```

<a name="one-to-one-polymorphic-retrieving-the-relationship"></a>
#### 관계 가져오기

관계와 테이블이 정의됐으면 다음처럼 접근합니다:

```php
use App\Models\Post;

$post = Post::find(1);

$image = $post->image;
```

`Image` 모델에서 부모 모델에는 `imageable` 동적 속성으로 접근합니다:

```php
use App\Models\Image;

$image = Image::find(1);

$imageable = $image->imageable;
```

`imageable`은 실제로 `Post` 또는 `User` 인스턴스입니다.

<a name="morph-one-to-one-key-conventions"></a>
#### 키 규칙

필요시 `morphTo` 첫 인수에 관계명, 두 번째와 세 번째 인수에 ID와 타입 컬럼명을 지정할 수 있습니다. 보통 첫 인수는 메서드명과 같아, `__FUNCTION__` 상수를 이용합니다:

```php
/**
 * 이 이미지가 속한 모델 가져오기
 */
public function imageable(): MorphTo
{
    return $this->morphTo(__FUNCTION__, 'imageable_type', 'imageable_id');
}
```

<a name="one-to-many-polymorphic-relations"></a>
### 일대다 다형성 (One to Many Polymorphic)

<a name="one-to-many-polymorphic-table-structure"></a>
#### 테이블 구조

일대다 다형성도 비슷하며, 게시물과 동영상이 댓글 테이블을 공용으로 사용하는 경우입니다.

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

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class Comment extends Model
{
    /**
     * 부모 commentable 모델 (post 또는 video) 가져오기
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
     * 게시물의 댓글들 가져오기
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
     * 동영상의 댓글들 가져오기
     */
    public function comments(): MorphMany
    {
        return $this->morphMany(Comment::class, 'commentable');
    }
}
```

<a name="one-to-many-polymorphic-retrieving-the-relationship"></a>
#### 관계 가져오기

```php
use App\Models\Post;

$post = Post::find(1);

foreach ($post->comments as $comment) {
    // ...
}
```

`Comment` 모델에서 부모는 `commentable` 동적 속성으로 접근:

```php
use App\Models\Comment;

$comment = Comment::find(1);

$commentable = $comment->commentable;
```

`commentable`은 `Post` 또는 `Video` 인스턴스입니다.

<a name="polymorphic-automatically-hydrating-parent-models-on-children"></a>
#### 자식 모델에서 부모 모델 자동 할당하기

즉시 로딩 후 반복하며 부모 모델에 접근할 때 발생하는 N + 1 문제는 `morphMany` 관계에 `chaperone` 호출로 해결합니다:

```php
class Post extends Model
{
    /**
     * 포스트 댓글 가져오기
     */
    public function comments(): MorphMany
    {
        return $this->morphMany(Comment::class, 'commentable')->chaperone();
    }
}
```

또는 실행 시점에 즉시 로딩할 때 `chaperone` 호출:

```php
use App\Models\Post;

$posts = Post::with([
    'comments' => fn ($comments) => $comments->chaperone(),
])->get();
```

<a name="one-of-many-polymorphic-relations"></a>
### One of Many (Polymorphic)

여러 관련 모델 중 가장 최신 또는 오래된 하나만 쉽게 접근하려면 `morphOne` + `ofMany` 메서드 조합을 사용합니다:

```php
/**
 * 유저의 가장 최근 이미지
 */
public function latestImage(): MorphOne
{
    return $this->morphOne(Image::class, 'imageable')->latestOfMany();
}
```

가장 오래된 이미지는:

```php
/**
 * 유저의 가장 오래된 이미지
 */
public function oldestImage(): MorphOne
{
    return $this->morphOne(Image::class, 'imageable')->oldestOfMany();
}
```

평균 평점 등 다른 정렬 기준도 가능합니다:

```php
/**
 * 유저가 가장 좋아하는 이미지
 */
public function bestImage(): MorphOne
{
    return $this->morphOne(Image::class, 'imageable')->ofMany('likes', 'max');
}
```

> [!NOTE]
> 더 고급 기능은 [has one of many 문서](#advanced-has-one-of-many-relationships)를 참고하세요.

<a name="many-to-many-polymorphic-relations"></a>
### 다대다 다형성 (Many to Many Polymorphic)

<a name="many-to-many-polymorphic-table-structure"></a>
#### 테이블 구조

`Post`와 `Video`가 `Tag` 모델과 다형성 다대다 관계를 가질 수 있습니다.

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
> 다대다 다형성 전에 일반 [다대다 관계](#many-to-many)를 먼저 익히는 것이 좋습니다.

<a name="many-to-many-polymorphic-model-structure"></a>
#### 모델 구조

`Post`와 `Video` 모델에 `tags` 관계 정의:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphToMany;

class Post extends Model
{
    /**
     * 포스트의 태그들 가져오기
     */
    public function tags(): MorphToMany
    {
        return $this->morphToMany(Tag::class, 'taggable');
    }
}
```

두 번째 인수 `taggable`은 중간 테이블명과 키 기반 정의한 관계 이름입니다.

<a name="many-to-many-polymorphic-defining-the-inverse-of-the-relationship"></a>
#### 역관계 정의하기

`Tag` 모델에 각각의 부모 모델별 관계를 정의해야 합니다. `morphedByMany` 메서드를 써서 관련 모델을 지정합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphToMany;

class Tag extends Model
{
    /**
     * 이 태그와 연결된 포스트들
     */
    public function posts(): MorphToMany
    {
        return $this->morphedByMany(Post::class, 'taggable');
    }

    /**
     * 이 태그와 연결된 비디오들
     */
    public function videos(): MorphToMany
    {
        return $this->morphedByMany(Video::class, 'taggable');
    }
}
```

<a name="many-to-many-polymorphic-retrieving-the-relationship"></a>
#### 관계 가져오기

```php
use App\Models\Post;

$post = Post::find(1);

foreach ($post->tags as $tag) {
    // ...
}
```

`Tag` 모델에서 `posts` 또는 `videos` 동적 속성으로 각각 조회 가능:

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
### 커스텀 다형성 타입 (Custom Polymorphic Types)

기본적으로 Laravel은 다형성 `*_type` 컬럼에 모델 풀네임 클래스를 저장합니다. 예를 들어 `Comment` 모델이 `Post`와 `Video` 모델에 연결되면 `commentable_type` 컬럼에 `App\Models\Post` 또는 `App\Models\Video`가 들어갑니다.

모델 이름 대신 `post`, `video`와 같은 간단한 문자열을 사용해 다형성 타입 값을 분리할 수 있습니다. 이렇게 하면 모델명이 바뀌어도 DB 값이 문제되지 않습니다:

```php
use Illuminate\Database\Eloquent\Relations\Relation;

Relation::enforceMorphMap([
    'post' => 'App\Models\Post',
    'video' => 'App\Models\Video',
]);
```

서비스 프로바이더 `AppServiceProvider`의 `boot` 메서드 등에 호출합니다.

현재 모델에서 별칭 얻기는 `getMorphClass()` 메서드, 별칭으로 클래스명 얻기는 `Relation::getMorphedModel` 메서드로 가능합니다:

```php
use Illuminate\Database\Eloquent\Relations\Relation;

$alias = $post->getMorphClass();

$class = Relation::getMorphedModel($alias);
```

> [!WARNING]
> 기존 앱에 morph map을 추가할 땐 DB 내 모든 기존 `*_type` 값도 변경해야 정상 작동합니다.

<a name="dynamic-relationships"></a>
### 동적 관계 (Dynamic Relationships)

`resolveRelationUsing` 메서드로 런타임에 관계를 정의할 수 있습니다. 보통은 일반 앱보다는 패키지 개발 시 유용합니다.

첫 인수는 관계 메서드명이며, 두 번째 인수는 모델 인스턴스를 받고 관계 정의를 반환하는 클로저입니다. 보통 서비스 프로바이더의 `boot` 메서드에서 정의합니다:

```php
use App\Models\Order;
use App\Models\Customer;

Order::resolveRelationUsing('customer', function (Order $orderModel) {
    return $orderModel->belongsTo(Customer::class, 'customer_id');
});
```

> [!WARNING]
> 동적 관계 정의 시 반드시 명시적 키 이름 인자를 Eloquent 관계 메서드에 넘겨야 합니다.

<a name="querying-relations"></a>
## 관계 쿼리하기 (Querying Relations)

모든 Eloquent 관계는 메서드로 정의되므로, 이 메서드 호출 시 관계 인스턴스를 얻되 실제 관련 모델 로딩 쿼리는 실행하지 않습니다. 또한, 관계는 [쿼리 빌더](/docs/12.x/queries)이기도 하므로, 제약 조건을 계속 체인하여 마지막에 쿼리 실행할 수 있습니다.

예를 들어, `User` 모델이 여러 `Post` 모델과 관계가 있을 때:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class User extends Model
{
    /**
     * 사용자 글 전체 가져오기
     */
    public function posts(): HasMany
    {
        return $this->hasMany(Post::class);
    }
}
```

관계를 쿼리할 때 추가 조건도 붙일 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

$user->posts()->where('active', 1)->get();
```

쿼리 빌더 모든 메서드도 관계에 쓸 수 있으므로, 문서 확인을 추천합니다.

<a name="chaining-orwhere-clauses-after-relationships"></a>
#### `orWhere` 절 체이닝 주의점

관계에 추가 조건 체인 가능하지만 `orWhere`를 그냥 체이닝하면 논리가 올바르게 묶이지 않아 조건이 잘못 걸릴 수 있습니다:

```php
$user->posts()
    ->where('active', 1)
    ->orWhere('votes', '>=', 100)
    ->get();
```

이때 생성되는 SQL은 다음과 같습니다:

```sql
select *
from posts
where user_id = ? and active = 1 or votes >= 100
```

`or`가 전체 `where` 최상위에서 적용되어 `user_id = ?` 조건과 묶이지 않아, 100표 이상 글이 모두 조회됩니다.

올바른 조건 묶기는 다음과 같이 그룹화(소괄호) 해야 합니다:

```php
use Illuminate\Database\Eloquent\Builder;

$user->posts()
    ->where(function (Builder $query) {
        return $query->where('active', 1)
            ->orWhere('votes', '>=', 100);
    })
    ->get();
```

이렇게 하면 SQL이 다음과 같이 올바르게 나옵니다:

```sql
select *
from posts
where user_id = ? and (active = 1 or votes >= 100)
```

<a name="relationship-methods-vs-dynamic-properties"></a>
### 관계 메서드와 동적 속성 차이 (Relationship Methods vs. Dynamic Properties)

추가 조건 없이 관계만 조회할 땐 관계를 속성처럼 접근(동적 속성)할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

foreach ($user->posts as $post) {
    // ...
}
```

동적 속성은 값이 실제 접근될 때 연관 데이터를 로드하는 "lazy loading" 방식입니다. 그래서 보통 연관 모델을 미리 로드하는 [즉시 로딩](#eager-loading)을 함께 사용해 쿼리 수를 줄입니다.

<a name="querying-relationship-existence"></a>
### 관계 존재 쿼리하기 (Querying Relationship Existence)

모델 조회 시 관계가 존재하는 경우만 필터링하려면 `has`, `orHas` 메서드에 관계명 전달합니다:

```php
use App\Models\Post;

// 한 개 이상 댓글 있는 게시물 조회
$posts = Post::has('comments')->get();
```

조건이 추가로 필요하면 연산자와 개수도 지정 가능:

```php
// 댓글 세 개 이상 게시물 조회
$posts = Post::has('comments', '>=', 3)->get();
```

중첩 관계도 점(.) 구문으로 지정할 수 있습니다:

```php
// 댓글에 이미지가 있는 게시물 조회
$posts = Post::has('comments.images')->get();
```

더 복잡한 조건은 `whereHas`, `orWhereHas`로 클로저 내 필터링 가능:

```php
use Illuminate\Database\Eloquent\Builder;

// `content`에 'code%'가 포함된 댓글이 1개 이상 있는 게시물 조회
$posts = Post::whereHas('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
})->get();

// 댓글 10개 이상이 조건을 만족하는 게시물 조회
$posts = Post::whereHas('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
}, '>=', 10)->get();
```

> [!WARNING]
> 현재 Eloquent는 데이터베이스가 다르면 관계 존재 쿼리를 지원하지 않습니다.

<a name="many-to-many-relationship-existence-queries"></a>
#### 다대다 관계 존재 쿼리

`whereAttachedTo` 메서드로 주어진 모델 혹은 컬렉션과 다대다 연결된 모델을 쿼리할 수 있습니다:

```php
$users = User::whereAttachedTo($role)->get();
```

컬렉션을 넘기면 컬렉션 내 아무 모델이나 연결된 모델 조회:

```php
$tags = Tag::whereLike('name', '%laravel%')->get();

$posts = Post::whereAttachedTo($tags)->get();
```

<a name="inline-relationship-existence-queries"></a>
#### 간단한 조건을 가진 관계 존재 쿼리

단순 조건이 필요하면 `whereRelation`, `orWhereRelation`, `whereMorphRelation`, `orWhereMorphRelation`도 유용합니다:

```php
use App\Models\Post;

$posts = Post::whereRelation('comments', 'is_approved', false)->get();
```

비교 연산자도 지정 가능:

```php
$posts = Post::whereRelation(
    'comments', 'created_at', '>=', now()->subHour()
)->get();
```

<a name="querying-relationship-absence"></a>
### 관계 부재 쿼리하기 (Querying Relationship Absence)

특정 관계가 없는 모델만 필터링하려면 `doesntHave`, `orDoesntHave` 메서드에 관계명 전달합니다:

```php
use App\Models\Post;

$posts = Post::doesntHave('comments')->get();
```

`whereDoesntHave`, `orWhereDoesntHave`로 조건을 넣을 수 있습니다:

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::whereDoesntHave('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
})->get();
```

중첩 관계도 지원:

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::whereDoesntHave('comments.author', function (Builder $query) {
    $query->where('banned', 1);
})->get();
```

<a name="querying-morph-to-relationships"></a>
### Morph To 관계 쿼리하기 (Querying Morph To Relationships)

`whereHasMorph`, `whereDoesntHaveMorph` 메서드로 다형성 관계 존재 및 부재를 쿼리할 수 있습니다. 관계명, 관련 모델 배열, 쿼리 조건 클로저를 인수로 받습니다:

```php
use App\Models\Comment;
use App\Models\Post;
use App\Models\Video;
use Illuminate\Database\Eloquent\Builder;

// 댓글 중 게시물 또는 동영상에 연결되고 제목이 code%인 것 조회
$comments = Comment::whereHasMorph(
    'commentable',
    [Post::class, Video::class],
    function (Builder $query) {
        $query->where('title', 'like', 'code%');
    }
)->get();

// 제목이 code%인 게시물에 연결되지 않은 댓글 조회
$comments = Comment::whereDoesntHaveMorph(
    'commentable',
    Post::class,
    function (Builder $query) {
        $query->where('title', 'like', 'code%');
    }
)->get();
```

클로저에 두 번째 인수 `$type`을 받으면 쿼리 대상 모델 타입에 따라 조건 다르게 줄 수도 있습니다:

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

부모 모델로부터 자식만 조회 시 `whereMorphedTo`, `whereNotMorphedTo` 메서드를 씁니다:

```php
$comments = Comment::whereMorphedTo('commentable', $post)
    ->orWhereMorphedTo('commentable', $video)
    ->get();
```

<a name="querying-all-morph-to-related-models"></a>
#### 모든 관련 모델 쿼리하기

모델 배열 대신 와일드카드 `'*'`를 넘기면 DB에서 모든 다형성 타입을 조회해 쿼리합니다. 추가 쿼리가 실행됩니다.

```php
use Illuminate\Database\Eloquent\Builder;

$comments = Comment::whereHasMorph('commentable', '*', function (Builder $query) {
    $query->where('title', 'like', 'foo%');
})->get();
```

<a name="aggregating-related-models"></a>
## 관련 모델 집계하기 (Aggregating Related Models)

<a name="counting-related-models"></a>
### 관련 모델 개수 세기 (Counting Related Models)

관련 모델을 로드하지 않고도 개수를 세고 싶을 때 `withCount` 메서드를 사용합니다. 결과 모델에 `{관계명}_count` 속성이 추가됩니다:

```php
use App\Models\Post;

$posts = Post::withCount('comments')->get();

foreach ($posts as $post) {
    echo $post->comments_count;
}
```

여러 관계 카운트를 동시에 하려면 배열에 조건 클로저를 함께 전달:

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::withCount(['votes', 'comments' => function (Builder $query) {
    $query->where('content', 'like', 'code%');
}])->get();

echo $posts[0]->votes_count;
echo $posts[0]->comments_count;
```

관계 카운트 결과에 별칭을 붙일 수도 있습니다:

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

`loadCount`를 사용하면 부모 모델이 이미 로드된 뒤 관계 개수를 추가 로딩할 수 있습니다:

```php
$book = Book::first();

$book->loadCount('genres');
```

조건도 클로저 배열로 지정 가능:

```php
$book->loadCount(['reviews' => function (Builder $query) {
    $query->where('rating', 5);
}]);
```

<a name="relationship-counting-and-custom-select-statements"></a>
#### 커스텀 선택절과 관계 집계

`select` 구문과 `withCount`를 같이 쓸 땐 반드시 `select` 다음에 `withCount` 호출해야 합니다:

```php
$posts = Post::select(['title', 'body'])
    ->withCount('comments')
    ->get();
```

<a name="other-aggregate-functions"></a>
### 기타 집계 함수 (Other Aggregate Functions)

`withCount` 외에도 `withMin`, `withMax`, `withAvg`, `withSum`, `withExists` 메서드를 사용해 집계 가능합니다. 결과는 `{relation}_{function}_{column}` 속성 형태로 반환:

```php
use App\Models\Post;

$posts = Post::withSum('comments', 'votes')->get();

foreach ($posts as $post) {
    echo $post->comments_sum_votes;
}
```

별칭 지정 가능:

```php
$posts = Post::withSum('comments as total_comments', 'votes')->get();

foreach ($posts as $post) {
    echo $post->total_comments;
}
```

`loadSum` 등 지연 호출 메서드도 존재합니다:

```php
$post = Post::first();

$post->loadSum('comments', 'votes');
```

`select`와 함께 쓸 땐 `select` 다음에 호출해야 합니다:

```php
$posts = Post::select(['title', 'body'])
    ->withExists('comments')
    ->get();
```

<a name="counting-related-models-on-morph-to-relationships"></a>
### Morph To 관계 관련 모델 개수 세기

`morphTo` 관계 존재 모델과 다양한 관련 모델 개수를 한꺼번에 즉시 로딩하려면 `morphWithCount`를 씁니다.

예를 들어 `ActivityFeed` 모델의 `parentable` morphTo 관계가 있고, `Photo` 모델은 `tags`, `Post` 모델은 `comments` 관계를 갖는 상황입니다:

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
#### 지연 카운트 로딩

이미 로드한 모델에 대해 후속으로 개수를 추가하려면 `loadMorphCount`:

```php
$activities = ActivityFeed::with('parentable')->get();

$activities->loadMorphCount('parentable', [
    Photo::class => ['tags'],
    Post::class => ['comments'],
]);
```

<a name="eager-loading"></a>
## 즉시 로딩 (Eager Loading)

Eloquent에서 관계를 속성처럼 접근하면 "지연 로딩"이 되어 처음 접근 시 관계 데이터를 가져옵니다. 하지만 N + 1 문제를 해결하기 위해 관계를 모델 조회 시 미리 불러오는 즉시 로딩이 유용합니다.

예를 들어 `Book` 모델이 `Author` 모델에 속할 때:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Book extends Model
{
    /**
     * 책의 저자 가져오기
     */
    public function author(): BelongsTo
    {
        return $this->belongsTo(Author::class);
    }
}
```

책과 저자를 모두 작게 조회하려면:

```php
use App\Models\Book;

$books = Book::all();

foreach ($books as $book) {
    echo $book->author->name;
}
```

이 경우 책 25개면 26개 쿼리가 나갑니다(책 1회 + 저자 25회).

즉시 로딩을 사용하면 두 쿼리만 실행합니다:

```php
$books = Book::with('author')->get();

foreach ($books as $book) {
    echo $book->author->name;
}
```

실행되는 쿼리:

```sql
select * from books

select * from authors where id in (1, 2, 3, 4, 5, ...)
```

<a name="eager-loading-multiple-relationships"></a>
#### 여러 관계 즉시 로딩

복수 관계 즉시 로딩은 배열 인수로:

```php
$books = Book::with(['author', 'publisher'])->get();
```

<a name="nested-eager-loading"></a>
#### 중첩 관계 즉시 로딩

관계 안의 관계도 점(.)으로 지정:

```php
$books = Book::with('author.contacts')->get();
```

배열 중첩도 가능:

```php
$books = Book::with([
    'author' => [
        'contacts',
        'publisher',
    ],
])->get();
```

<a name="nested-eager-loading-morphto-relationships"></a>
#### `morphTo` 관계 중첩 즉시 로딩

`morphTo` 관계를 즉시 로딩하고 타입별로 다른 관계도 지정하려면 `morphWith` 메서드 사용:

```php
<?php

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class ActivityFeed extends Model
{
    /**
     * 활동 피드 부모(다형성) 관계
     */
    public function parentable(): MorphTo
    {
        return $this->morphTo();
    }
}
```

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

조회 컬럼을 제한하려면:

```php
$books = Book::with('author:id,name,book_id')->get();
```

> [!WARNING]
> 이때는 항상 기본키(`id`)와 외래키 컬럼 포함해야 문제없습니다.

<a name="eager-loading-by-default"></a>
#### 기본 즉시 로딩

항상 특정 관계를 기본 즉시 로딩하려면 모델에 `$with` 속성에 관계명을 등록하세요:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Book extends Model
{
    /**
     * 항상 즉시 로딩할 관계들
     *
     * @var array
     */
    protected $with = ['author'];

    /**
     * 책 저자 관계
     */
    public function author(): BelongsTo
    {
        return $this->belongsTo(Author::class);
    }

    /**
     * 책 장르 관계
     */
    public function genre(): BelongsTo
    {
        return $this->belongsTo(Genre::class);
    }
}
```

`without`로 특정 관계를 한 번만 제거 가능:

```php
$books = Book::without('author')->get();
```

`withOnly`로 `$with` 완전 대체 가능:

```php
$books = Book::withOnly('genre')->get();
```

<a name="constraining-eager-loads"></a>
### 즉시 로딩에 조건 걸기 (Constraining Eager Loads)

즉시 로딩 시에도 조건을 달 수 있습니다. `with` 메서드에 배열을 넘기고, 값에 클로저로 제약조건 추가:

```php
use App\Models\User;
use Illuminate\Contracts\Database\Eloquent\Builder;

$users = User::with(['posts' => function (Builder $query) {
    $query->where('title', 'like', '%code%');
}])->get();
```

추가 쿼리 빌더 메서드도 가능:

```php
$users = User::with(['posts' => function (Builder $query) {
    $query->orderBy('created_at', 'desc');
}])->get();
```

<a name="constraining-eager-loading-of-morph-to-relationships"></a>
#### `morphTo` 즉시 로딩 제약 조건

`morphTo`를 즉시 로딩할 때 다형성 모델별로 다른 조건 걸려면 `constrain` 사용:

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

위 예시는 숨겨지지 않은 포스트와 교육용 비디오만 즉시 로딩합니다.

<a name="constraining-eager-loads-with-relationship-existence"></a>
#### 관계 존재 조건과 함께 즉시 로딩

조건에 맞는 관계 존재 여부만 필터링하면서 동시에 해당 관계 데이터를 즉시 로딩하려면 `withWhereHas`를 씁니다:

```php
use App\Models\User;

$users = User::withWhereHas('posts', function ($query) {
    $query->where('featured', true);
})->get();
```

<a name="lazy-eager-loading"></a>
### 지연 즉시 로딩 (Lazy Eager Loading)

이미 로드한 모델에 관계를 나중에 로딩하려면 `load` 메서드 이용:

```php
use App\Models\Book;

$books = Book::all();

if ($someCondition) {
    $books->load('author', 'publisher');
}
```

조건도 배열과 클로저를 넘길 수 있습니다:

```php
$author->load(['books' => function (Builder $query) {
    $query->orderBy('published_date', 'asc');
}]);
```

이미 로드한 관계가 아무것도 없으면 로딩하는 `loadMissing` 메서드도 있습니다:

```php
$book->loadMissing('author');
```

<a name="nested-lazy-eager-loading-morphto"></a>
#### 중첩 지연 즉시 로딩과 `morphTo`

`morphTo` 관계와 해당 타입별 중첩 관계를 로드하려면 `loadMorph` 사용:

```php
<?php

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class ActivityFeed extends Model
{
    public function parentable(): MorphTo
    {
        return $this->morphTo();
    }
}
```

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
> 이 기능은 베타 단계이며, 패치나 마이너 버전에서 동작이 변경될 수 있습니다.

Laravel은 접근하는 관계 중 로드되지 않은 것들을 자동으로 즉시 로딩하는 기능을 제공합니다.

`AppServiceProvider`의 `boot` 메서드에서 다음처럼 실행합니다:

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

이 기능을 쓰면 다음 예시 코드가 자동으로 관계를 즉시 로딩합니다:

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

기본 동작은 `User`들의 모든 `posts`를 묶어서, 그리고 각 `post`에 대해서도 `comments`를 한꺼번에 즉시 로딩합니다.

글로벌 설정이 싫다면 단일 컬렉션에 대해 `withRelationshipAutoloading` 메서드로 활성화할 수 있습니다:

```php
$users = User::where('vip', true)->get();

return $users->withRelationshipAutoloading();
```

<a name="preventing-lazy-loading"></a>
### 지연 로딩 방지하기 (Preventing Lazy Loading)

즉시 로딩이 성능에 좋으므로, 지연 로딩을 아예 막고 싶으면 기본 모델 클래스에서 `preventLazyLoading` 호출합니다.

보통 `AppServiceProvider` 내에서 환경별로 제어합니다:

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

이렇게 빨간 불 켜지면 지연 로딩 시 `Illuminate\Database\LazyLoadingViolationException` 예외가 터집니다.

`handleLazyLoadingViolationsUsing`으로 예외 대신 로그만 남기도록 커스터마이징도 가능합니다:

```php
Model::handleLazyLoadingViolationUsing(function (Model $model, string $relation) {
    $class = $model::class;

    info("Attempted to lazy load [{$relation}] on model [{$class}].");
});
```

<a name="inserting-and-updating-related-models"></a>
## 관련 모델 삽입 및 수정 (Inserting and Updating Related Models)

<a name="the-save-method"></a>
### `save` 메서드

관계에 새 모델 추가가 편합니다. 예를 들어 글에 새 댓글을 달 때, 직접 `post_id` 지정하는 대신 관계의 `save` 메서드를 사용합니다:

```php
use App\Models\Comment;
use App\Models\Post;

$comment = new Comment(['message' => '새로운 댓글입니다.']);

$post = Post::find(1);

$post->comments()->save($comment);
```

`comments` 동적 속성 말고 `comments()` 메서드 호출에 주의하세요. `save`가 적절히 외래 키를 설정하여 새 댓글에 연결합니다.

여러 모델 저장은 `saveMany`:

```php
$post = Post::find(1);

$post->comments()->saveMany([
    new Comment(['message' => '첫 번째 댓글']),
    new Comment(['message' => '두 번째 댓글']),
]);
```

`save`나 `saveMany` 후에 부모 모델에 이미 로드된 관계목록은 업데이트되지 않습니다. 나중에 사용하면 새로 로드하려면 `refresh`를 씁니다:

```php
$post->comments()->save($comment);

$post->refresh();

$post->comments; // 새 댓글 포함된 댓글 목록
```

<a name="the-push-method"></a>
#### 모델과 관계를 재귀적 저장

모델과 관련 모델, 또 그 자식 연결 모델 모두 저장하려면 `push` 메서드를 사용합니다:

```php
$post = Post::find(1);

$post->comments[0]->message = '댓글 메시지 수정';
$post->comments[0]->author->name = '저자 이름 수정';

$post->push();
```

이벤트를 트리거하지 않고 저장하려면 `pushQuietly`:

```php
$post->pushQuietly();
```

<a name="the-create-method"></a>
### `create` 메서드

`save`는 모델 인스턴스가 인수인 반면, `create`는 속성 배열을 받아 새 모델을 생성하고 DB에 삽입합니다. 새 모델 인스턴스를 반환합니다:

```php
use App\Models\Post;

$post = Post::find(1);

$comment = $post->comments()->create([
    'message' => '새로운 댓글입니다.',
]);
```

여러 개 생성은 `createMany`:

```php
$post = Post::find(1);

$post->comments()->createMany([
    ['message' => '첫 댓글'],
    ['message' => '두 번째 댓글'],
]);
```

이벤트 없이 생성하려면 `createQuietly`, `createManyQuietly` 사용:

```php
$user = User::find(1);

$user->posts()->createQuietly([
    'title' => '포스트 제목',
]);

$user->posts()->createManyQuietly([
    ['title' => '첫번째 포스트'],
    ['title' => '두번째 포스트'],
]);
```

`findOrNew`, `firstOrNew`, `firstOrCreate`, `updateOrCreate` 같은 메서드도 관계 모델 생성/업데이트에 쓸 수 있습니다.

> [!NOTE]
> `create` 사용 전에는 반드시 [대량 할당](/docs/12.x/eloquent#mass-assignment) 권한 설정을 확인하세요.

<a name="updating-belongs-to-relationships"></a>
### Belongs To 관계 갱신

자식 모델의 부모를 바꾸고 싶으면 `associate` 메서드를 씁니다:

```php
use App\Models\Account;

$account = Account::find(10);

$user->account()->associate($account);

$user->save();
```

부모 연결 해제는 `dissociate` 메서드로 외래 키를 `null`로 만듭니다:

```php
$user->account()->dissociate();

$user->save();
```

<a name="updating-many-to-many-relationships"></a>
### 다대다 관계 갱신 (Many to Many Relationships)

<a name="attaching-detaching"></a>
#### 연결 / 해제 (Attaching / Detaching)

`attach` 메서드로 중간 테이블에 관계 추가:

```php
use App\Models\User;

$user = User::find(1);

$user->roles()->attach($roleId);
```

추가 데이터와 함께 붙일 수도 있습니다:

```php
$user->roles()->attach($roleId, ['expires' => $expires]);
```

역으로 관계 제거는 `detach` 사용:

```php
// 특정 역할 하나 해제
$user->roles()->detach($roleId);

// 모든 역할 해제
$user->roles()->detach();
```

`attach`, `detach` 모두 배열 인수 입력 가능:

```php
$user = User::find(1);

$user->roles()->detach([1, 2, 3]);

$user->roles()->attach([
    1 => ['expires' => $expires],
    2 => ['expires' => $expires],
]);
```

<a name="syncing-associations"></a>
#### 연결 목록 동기화 (Syncing Associations)

`sync`는 배열로 지정한 ID만 남기고 중간 테이블 동기화합니다:

```php
$user->roles()->sync([1, 2, 3]);
```

값 추가할 수도 있습니다:

```php
$user->roles()->sync([1 => ['expires' => true], 2, 3]);
```

동일 값 추가 시 `syncWithPivotValues`:

```php
$user->roles()->syncWithPivotValues([1, 2, 3], ['active' => true]);
```

기존 ID를 제거하지 않으려면 `syncWithoutDetaching` 사용:

```php
$user->roles()->syncWithoutDetaching([1, 2, 3]);
```

<a name="toggling-associations"></a>
#### 연결 토글 (Toggling Associations)

`toggle`은 전달한 ID가 연결되어 있으면 해제, 아니면 연결 상태를 토글합니다:

```php
$user->roles()->toggle([1, 2, 3]);
```

추가 중간 값 지정 가능:

```php
$user->roles()->toggle([
    1 => ['expires' => true],
    2 => ['expires' => true],
]);
```

<a name="updating-a-record-on-the-intermediate-table"></a>
#### 중간 테이블 기록 업데이트

중간 테이블 레코드를 업데이트하려면 `updateExistingPivot` 사용:

```php
$user = User::find(1);

$user->roles()->updateExistingPivot($roleId, [
    'active' => false,
]);
```

<a name="touching-parent-timestamps"></a>
## 부모 타임스탬프 갱신 (Touching Parent Timestamps)

자식 모델이 `belongsTo` 또는 `belongsToMany` 관계의 부모 모델 타임스탬프를 갱신하고 싶을 수 있습니다.

예를 들어, 댓글이 수정되면 댓글이 속한 게시물 `updated_at` 컬럼을 현재 시각으로 자동 갱신하려면 자식 모델에 `touches` 배열 속성에 관계명을 넣으면 됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Comment extends Model
{
    /**
     * 갱신할 관계들
     *
     * @var array
     */
    protected $touches = ['post'];

    /**
     * 댓글이 속한 게시물 가져오기
     */
    public function post(): BelongsTo
    {
        return $this->belongsTo(Post::class);
    }
}
```

> [!WARNING]
> 부모 타임스탬프는 자식 모델을 Eloquent `save` 메서드로 수정할 때만 자동 갱신됩니다.