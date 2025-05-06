# Eloquent: 관계(Relationships)

- [소개](#introduction)
- [관계 정의하기](#defining-relationships)
    - [일대일(One to One)](#one-to-one)
    - [일대다(One to Many)](#one-to-many)
    - [일대다(역방향) / Belongs To](#one-to-many-inverse)
    - [여러 개 중 하나(Has One of Many)](#has-one-of-many)
    - [중간 모델을 통한 일대일(Has One Through)](#has-one-through)
    - [중간 모델을 통한 일대다(Has Many Through)](#has-many-through)
- [다대다 관계](#many-to-many)
    - [중간 테이블 컬럼 가져오기](#retrieving-intermediate-table-columns)
    - [중간 테이블 컬럼을 통한 쿼리 필터링](#filtering-queries-via-intermediate-table-columns)
    - [중간 테이블 컬럼을 통한 쿼리 정렬](#ordering-queries-via-intermediate-table-columns)
    - [커스텀 중간 테이블 모델 정의하기](#defining-custom-intermediate-table-models)
- [폴리모픽 관계](#polymorphic-relationships)
    - [일대일](#one-to-one-polymorphic-relations)
    - [일대다](#one-to-many-polymorphic-relations)
    - [여러 개 중 하나](#one-of-many-polymorphic-relations)
    - [다대다](#many-to-many-polymorphic-relations)
    - [커스텀 폴리모픽 타입 사용](#custom-polymorphic-types)
- [동적 관계](#dynamic-relationships)
- [관계 쿼리](#querying-relations)
    - [관계 메서드 vs. 동적 속성](#relationship-methods-vs-dynamic-properties)
    - [관계 존재 쿼리](#querying-relationship-existence)
    - [관계 부재 쿼리](#querying-relationship-absence)
    - [morphTo 관계 쿼리](#querying-morph-to-relationships)
- [연관된 모델 집계](#aggregating-related-models)
    - [연관 모델 수 세기](#counting-related-models)
    - [기타 집계 함수](#other-aggregate-functions)
    - [morphTo 관계에서 연관 모델 수 세기](#counting-related-models-on-morph-to-relationships)
- [Eager 로딩(즉시 로딩)](#eager-loading)
    - [Eager Load 제약](#constraining-eager-loads)
    - [Lazy Eager Loading(지연 즉시 로딩)](#lazy-eager-loading)
    - [Lazy Loading(지연 로딩) 방지하기](#preventing-lazy-loading)
- [연관된 모델 삽입 및 수정](#inserting-and-updating-related-models)
    - [`save` 메서드](#the-save-method)
    - [`create` 메서드](#the-create-method)
    - [Belongs To 관계 업데이트](#updating-belongs-to-relationships)
    - [다대다 관계 업데이트](#updating-many-to-many-relationships)
- [부모 타임스탬프 갱신(Touch)](#touching-parent-timestamps)

<a name="introduction"></a>
## 소개

데이터베이스 테이블은 종종 서로 연관되어 있습니다. 예를 들어, 블로그 게시물은 여러 개의 댓글을 가질 수 있거나, 주문은 그것을 생성한 사용자와 관련될 수 있습니다. Eloquent는 이와 같은 관계를 쉽게 관리하고 작업할 수 있도록 해주며, 다양하고 일반적인 관계 유형을 지원합니다:

<div class="content-list" markdown="1">

- [일대일(One To One)](#one-to-one)
- [일대다(One To Many)](#one-to-many)
- [다대다(Many To Many)](#many-to-many)
- [중간 모델을 통한 일대일(Has One Through)](#has-one-through)
- [중간 모델을 통한 일대다(Has Many Through)](#has-many-through)
- [폴리모픽 일대일(One To One, Polymorphic)](#one-to-one-polymorphic-relations)
- [폴리모픽 일대다(One To Many, Polymorphic)](#one-to-many-polymorphic-relations)
- [폴리모픽 다대다(Many To Many, Polymorphic)](#many-to-many-polymorphic-relations)

</div>

<a name="defining-relationships"></a>
## 관계 정의하기

Eloquent 관계는 Eloquent 모델 클래스의 메서드로 정의합니다. 관계 또한 강력한 [쿼리 빌더](/docs/{{version}}/queries)로 동작하므로, 관계를 메서드로 정의하면 체이닝과 쿼리 기능을 강력하게 활용할 수 있습니다. 예를 들어, `posts` 관계에 쿼리 제약 조건을 추가로 체이닝할 수 있습니다:

    $user->posts()->where('active', 1)->get();

본격적으로 관계를 사용하는 방법을 살펴보기 전에, Eloquent가 지원하는 각 관계 유형을 어떻게 정의하는지부터 알아보겠습니다.

<a name="one-to-one"></a>
### 일대일(One to One)

일대일(One to One) 관계는 기본적인 유형의 데이터베이스 관계입니다. 예를 들어, `User` 모델은 하나의 `Phone` 모델과 연결될 수 있습니다. 이 관계를 정의하기 위해 `User` 모델에 `phone` 메서드를 추가합니다. 이 메서드는 `hasOne` 메서드를 호출하고 그 결과를 반환해야 합니다. `hasOne` 메서드는 모델의 `Illuminate\Database\Eloquent\Model` 기반 클래스에서 제공됩니다:

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

`hasOne`에 첫 번째 인수로 전달되는 값은 연관 모델 클래스의 이름입니다. 관계가 정의되면, Eloquent의 동적 속성을 사용해 연관 레코드를 조회할 수 있습니다. 동적 속성은 마치 모델에 정의된 속성인 것처럼 관계를 사용할 수 있게 해줍니다:

    $phone = User::find(1)->phone;

Eloquent는 부모 모델 이름을 기반으로 외래 키를 결정합니다. 이 경우, `Phone` 모델은 기본적으로 `user_id` 외래 키가 있다고 가정합니다. 이 규칙을 변경하려면 `hasOne`의 두 번째 인수로 외래 키명을 전달하면 됩니다:

    return $this->hasOne(Phone::class, 'foreign_key');

또한, Eloquent는 외래 키가 부모의 기본 키(primary key) 값과 일치해야 한다고 간주합니다. 즉, 사용자의 `id` 컬럼 값이 `Phone` 레코드의 `user_id` 컬럼에 존재하는지 찾습니다. 만약 `id` 대신 다른 값을 사용하고 싶다면, 세 번째 인수로 로컬 키(local key)명을 전달할 수 있습니다:

    return $this->hasOne(Phone::class, 'foreign_key', 'local_key');

<a name="one-to-one-defining-the-inverse-of-the-relationship"></a>
#### 관계의 역방향(Inverse) 정의하기

`User` 모델에서 `Phone` 모델을 접근할 수 있었으니, 이제 `Phone` 모델에서 자신을 소유한 사용자를 접근할 수 있도록 관계를 정의해보겠습니다. `hasOne` 관계의 역방향은 `belongsTo` 메서드로 정의할 수 있습니다:

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

`user` 메서드를 호출하면, Eloquent는 `Phone` 모델의 `user_id` 컬럼과 일치하는 `id` 값을 가진 `User` 모델을 찾으려고 시도합니다.

Eloquent는 관계 메서드의 이름에 `_id`를 붙여 외래 키 컬럼명을 자동 추론합니다. 즉, `user` 메서드를 통해 `Phone` 모델은 `user_id` 컬럼을 가진 것으로 추정됩니다. 만약 외래 키가 다르다면, 두 번째 인수로 외래 키명을 지정할 수 있습니다:

    /**
     * 이 전화번호를 소유한 사용자를 가져옵니다.
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class, 'foreign_key');
    }

만약 부모 모델의 기본 키가 `id`가 아니거나, 다른 컬럼 값으로 연관 모델을 찾고 싶다면, 세 번째 인수로 부모 테이블의 키 컬럼명을 지정할 수 있습니다:

    /**
     * 이 전화번호를 소유한 사용자를 가져옵니다.
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class, 'foreign_key', 'owner_key');
    }

<a name="one-to-many"></a>
### 일대다(One to Many)

일대다(One to Many) 관계는 한 모델이 여러 자식 모델을 가질 때 사용됩니다. 예를 들어, 블로그 포스트는 무한대로 많은 댓글을 가질 수 있습니다. 다른 관계와 마찬가지로, 메서드를 정의해 관계를 선언합니다:

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;
    use Illuminate\Database\Eloquent\Relations\HasMany;

    class Post extends Model
    {
        /**
         * 이 블로그 포스트의 댓글을 가져옵니다.
         */
        public function comments(): HasMany
        {
            return $this->hasMany(Comment::class);
        }
    }

Eloquent는 자동으로 `Comment` 모델의 외래 키 컬럼명을 추론합니다. 컨벤션에 따라 부모 모델명을 스네이크 케이스로 변환 후 `_id`를 붙여 사용합니다. 이 예시에서는, `Comment` 모델의 외래 키는 `post_id`가 됩니다.

관계 메서드를 정의한 후에는, 동적 속성을 이용해 연관된 댓글의 [컬렉션](/docs/{{version}}/eloquent-collections)에 접근할 수 있습니다:

    use App\Models\Post;

    $comments = Post::find(1)->comments;

    foreach ($comments as $comment) {
        // ...
    }

모든 관계는 쿼리 빌더이므로, `comments` 메서드를 직접 호출하여 추가 조건을 체이닝도 가능합니다:

    $comment = Post::find(1)->comments()
                        ->where('title', 'foo')
                        ->first();

`hasOne`처럼 외래 키 및 로컬 키를 추가 인수로 오버라이드할 수 있습니다:

    return $this->hasMany(Comment::class, 'foreign_key');
    return $this->hasMany(Comment::class, 'foreign_key', 'local_key');

<a name="one-to-many-inverse"></a>
### 일대다(역방향) / Belongs To

이제 포스트의 모든 댓글을 접근할 수 있으니, 각 댓글이 소속된 부모 포스트에 접근하는 관계도 정의할 수 있습니다. 자식 모델에 메서드를 정의한 뒤 `belongsTo` 메서드를 호출합니다:

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;
    use Illuminate\Database\Eloquent\Relations\BelongsTo;

    class Comment extends Model
    {
        /**
         * 이 댓글이 소속된 포스트를 가져옵니다.
         */
        public function post(): BelongsTo
        {
            return $this->belongsTo(Post::class);
        }
    }

이제, 댓글의 `post` 동적 관계 속성을 통해 부모 포스트에 접근할 수 있습니다:

    use App\Models\Comment;

    $comment = Comment::find(1);

    return $comment->post->title;

위의 예시에서 Eloquent는 `Comment` 모델의 `post_id` 컬럼과 일치하는 `id` 값을 가진 `Post` 모델을 찾으려고 시도합니다.

Eloquent는 기본적으로, 관계 메서드 이름과 부모 기본키 컬럼을 기반으로 외래 키명을 결정합니다. 즉, 이 예시에서는 `comments` 테이블의 외래 키는 `post_id`가 됩니다.

외래 키가 컨벤션을 따르지 않는 경우, 두 번째 인수로 외래 키명을, 세 번째 인수로 부모의 키 컬럼명을 지정할 수 있습니다.


### 기본 모델(Default Models)

`belongsTo`, `hasOne`, `hasOneThrough`, `morphOne` 관계에서는 연관된 모델이 없을 경우 기본 모델을 반환하도록 할 수 있습니다. 이는 [Null Object 패턴](https://en.wikipedia.org/wiki/Null_Object_pattern)에 해당하며, 조건 검사를 코드에서 줄이는 데 도움이 됩니다. 예를 들어, 다음과 같이 연관된 사용자가 없을 경우 빈 `App\Models\User` 모델이 반환됩니다:

    /**
     * 포스트의 작성자(사용자)를 가져옵니다.
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class)->withDefault();
    }

기본 모델에 속성 값을 미리 지정하려면, 배열 또는 클로저를 `withDefault`에 전달하면 됩니다:

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class)->withDefault([
            'name' => 'Guest Author',
        ]);
    }

또는,

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class)->withDefault(function (User $user, Post $post) {
            $user->name = 'Guest Author';
        });
    }

### Belongs To 관계 쿼리(Querying Belongs To Relationships)

"Belongs To" 관계 자식들을 쿼리하고 싶을 때는 직접 where 절을 쓸 수도 있지만, `whereBelongsTo`를 쓰면 더 편리하게 관계 및 외래 키를 지정할 수 있습니다:

    $posts = Post::whereBelongsTo($user)->get();

여러 개의 부모 모델(컬렉션)도 넘길 수 있습니다:

    $users = User::where('vip', true)->get();

    $posts = Post::whereBelongsTo($users)->get();

관계명이 다를 경우 두 번째 인수로 지정할 수 있습니다:

    $posts = Post::whereBelongsTo($user, 'author')->get();

<a name="has-one-of-many"></a>
### 여러 개 중 하나(Has One of Many)

종종 여러 연관된 모델 중 "최신" 혹은 "가장 오래된" 모델 하나만 쉽게 가져오고 싶을 수 있습니다. 예를 들어, `User` 모델이 여러 개의 `Order` 모델과 연관될 때, 사용자가 마지막으로 주문한 내역만 받고 싶다면 `ofMany`를 활용한 `hasOne` 관계를 쓸 수 있습니다:

```php
/**
 * 사용자의 가장 최근 주문을 구합니다.
 */
public function latestOrder(): HasOne
{
    return $this->hasOne(Order::class)->latestOfMany();
}
```

"가장 오래된" 주문도 비슷한 방식으로 정의할 수 있습니다:

```php
/**
 * 사용자의 가장 오래된 주문을 구합니다.
 */
public function oldestOrder(): HasOne
{
    return $this->hasOne(Order::class)->oldestOfMany();
}
```

기본적으로 `latestOfMany` 및 `oldestOfMany`는 기본 키를 기준으로 동작합니다. 하지만 다른 정렬 기준으로 단일 모델을 선택하고 싶다면, `ofMany` 메서드를 사용해서 다른 컬럼과 집계함수(`min` 또는 `max`)를 지정할 수 있습니다(예를 들어, 가격이 가장 비싼 주문):

```php
/**
 * 사용자의 최대 금액 주문을 구합니다.
 */
public function largestOrder(): HasOne
{
    return $this->hasOne(Order::class)->ofMany('price', 'max');
}
```

> [!WARNING]
> PostgreSQL은 UUID 컬럼에 대해 `MAX` 함수를 지원하지 않으므로, PostgreSQL UUID 컬럼과 함께 one-of-many 관계를 사용할 수 없습니다.

#### "Has Many" 관계를 "Has One"으로 변환하기

이미 "has many" 관계를 정의했다면, 그 관계에서 one-of-many를 쉽게 정의할 수 있습니다:

```php
public function orders(): HasMany
{
    return $this->hasMany(Order::class);
}

public function largestOrder(): HasOne
{
    return $this->orders()->one()->ofMany('price', 'max');
}
```

#### 고급 Has One of Many 관계

더 복잡한 "여러 개 중 하나" 관계도 만들 수 있습니다. 예를 들어, 상품의 가격(Price) 정보를 시간에 따라 여러 개 보관하고 있다가, 적용일(published_at)이 미래가 아닌 최신 값을 구해야 한다면:

```php
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
### 중간 모델을 통한 일대일(Has One Through)

hasOneThrough(중간 모델을 통한 일대일) 관계는 한 모델에서 중간 모델을 거쳐 다른 모델과 일대일 관계를 정의할 때 사용합니다.

예를 들어, 정비소 애플리케이션에서 각 `Mechanic` 모델은 하나의 `Car`와 관련 있고, 각 `Car` 모델은 하나의 `Owner`와 연결될 수 있습니다. `Mechanic`과 `Owner`가 직접 관계를 가지지 않지만, `Car`를 통해 접근할 수 있습니다. 다음과 같은 테이블이 필요합니다:

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

메커닉에서 자동차 소유자에 접근하는 관계는 다음과 같이 정의합니다:

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

첫 번째 인자는 최종 모델, 두 번째 인자는 중간 모델입니다.

이미 모델들에 필요한 관계가 정의되어 있다면, `through` 메서드를 사용해 더 유연하게 관계를 선언할 수도 있습니다:

```php
// 문자열 문법
return $this->through('cars')->has('owner');

// 동적 문법
return $this->throughCars()->hasOwner();
```

#### 키 규칙

기본적으로 Eloquent 컨벤션이 사용됩니다. 관계의 키를 직접 지정하려면 `hasOneThrough`의 세 번째~여섯 번째 인수로 외래 키, 로컬 키를 지정할 수 있습니다.

<a name="has-many-through"></a>
### 중간 모델을 통한 일대다(Has Many Through)

hasManyThrough(중간 모델을 통한 일대다) 관계는 중간 관계를 거쳐 먼 거리의 모델에 쉽게 접근할 수 있게 합니다. 예를 들어, `Project` 모델이 `Environment` 모델을 거쳐서 여러 `Deployment` 모델을 접근하는 상황을 들 수 있습니다.

프로젝트에서 바로 배포 내역을 모두 가져오는 관계를 만들어줍니다. 자세한 내용은 원문 참고.

키 규칙 등은 `hasOneThrough`와 동일합니다.

<a name="many-to-many"></a>
## 다대다 관계(Many to Many Relationships)

다대다 관계는 `hasOne`, `hasMany`보다 복잡합니다. 예를 들어, 하나의 사용자가 여러 역할을 가질 수 있고, 역할도 여러 사용자에게 할당될 수 있습니다.

#### 테이블 구조

`users`, `roles`, `role_user` 3개의 테이블이 필요합니다. `role_user`는 중간 테이블로, 두 모델의 이름을 알파벳 순서로 합쳐 이름을 만들고, 두 외래키(`user_id`, `role_id`)를 포함합니다.

#### 모델 구조

다대다 관계는 `belongsToMany` 메서드로 정의됩니다. 예시:


    public function roles(): BelongsToMany
    {
        return $this->belongsToMany(Role::class);
    }

역방향(역할에서 사용자로)도 동일하게 `belongsToMany(User::class)`로 정의합니다.

#### 중간 테이블 속성 가져오기

중간 테이블의 데이터(`pivot`)도 함께 사용할 수 있습니다.

중간 테이블에 추가 컬럼이 있을 땐 `withPivot('컬럼명1', '컬럼명2')`를 추가해줍니다.

중간 테이블에 자동 타임스탬프 생성이 필요하면 `withTimestamps()`를 사용합니다.

#### `pivot` 속성 이름 커스터마이징

`as()` 메서드로 지정할 수 있습니다:

    return $this->belongsToMany(Podcast::class)
                    ->as('subscription')
                    ->withTimestamps();

#### 중간 테이블 컬럼으로 쿼리 필터/정렬하기

`wherePivot`, `wherePivotIn`, `wherePivotBetween`, `wherePivotNull`, `orderByPivot` 등 다양한 메서드로 중간 데이터의 값으로 쿼리할 수 있습니다.

#### 커스텀 중간 테이블 모델 정의

중간 테이블의 모델을 커스텀해서 사용할 수 있습니다. 이 때 모델은 반드시 `Pivot`을 상속받습니다.

    public function users(): BelongsToMany
    {
        return $this->belongsToMany(User::class)->using(RoleUser::class);
    }

> [!WARNING]
> Pivot 모델은 SoftDeletes 트레이트를 사용할 수 없습니다. Soft Delete가 필요하다면, 피벗 모델을 실제 Eloquent 모델로 바꿔야 합니다.

#### 자동 증가(PK) 커스텀 Pivot 모델

`incrementing` 속성을 true로 설정해야 합니다:

    public $incrementing = true;

<a name="polymorphic-relationships"></a>
## 폴리모픽 관계(Polymorphic Relationships)

폴리모픽 관계란 자식 모델이 여러 종류의 부모 모델에 단일 관계로 귀속될 수 있도록 합니다. 예를 들어 `Comment` 모델이 `Post`와 `Video` 둘 다에 속할 수 있습니다.

### 일대일(폴리모픽)

자세한 테이블/모델 구조, 관계 정의, 조회 사용법, 키 커스터마이즈 등은 영문 원문을 참고하세요.

### 일대다(폴리모픽)

`comments` 테이블 하나로 모든 대상(포스트/비디오 등)에 댓글을 달 수 있습니다.

### 여러 개 중 하나(폴리모픽)

`ofMany`, `latestOfMany`, `oldestOfMany` 등을 사용해, 가장 최신/오래된/특정 조건의 모델 하나만 추출할 수 있습니다.

### 다대다(폴리모픽)

중간 테이블 `taggables` 같이 `taggable_id`, `taggable_type`을 사용해 여러 모델 간 다대다(태그 등)를 표현합니다.

#### 역방향

폴리모픽에서는 `morphedByMany`를 사용해 역방향 접근을 정의합니다.

#### 커스텀 타입 맵핑

type 컬럼에 실제 클래스명이 아니라 임의의 별칭을 사용하고 싶다면 `Relation::enforceMorphMap`을 통해 설정할 수 있습니다.

#### 동적 관계

`resolveRelationUsing` 으로 런타임에 관계를 추가할 수 있습니다.

<a name="querying-relations"></a>
## 관계 쿼리(Querying Relations)

관계는 모두 메서드로 정의되어 있으므로, 해당 메서드를 즉시 호출하여 관계 쿼리 인스턴스를 얻을 수 있고, 또 다양한 조건을 체이닝할 수 있습니다.

#### 관계 체이닝 시 orWhere 주의

`orWhere`는 논리 그룹핑이 안 돼서, 원하는 결과와 다르게 쿼리가 나갈 수 있습니다. 반드시 논리 그룹핑을 하여 의도대로 동작하도록 해야 합니다.

### 관계 메서드 vs 동적 속성

추가 조건(chain)을 붙이지 않는다면 마치 속성처럼 바로 접근할 수 있습니다. 이 동적 속성은 lazy loading입니다. 반복적으로 데이터 접근이 필요하다면 [Eager Loading](#eager-loading)을 사용하는 것이 좋습니다.

### 관계 존재 쿼리

예를 들어, 댓글이 하나라도 있는 모든 게시글을 가져오려면:

    $posts = Post::has('comments')->get();

더 조건을 세분화하려면 `whereHas`, `orWhereHas` 등을 사용할 수 있습니다.

### 관계 부재 쿼리

댓글이 전혀 없는 포스트만 가져오려면:

    $posts = Post::doesntHave('comments')->get();

보다 복잡한 조건은 `whereDoesntHave`, `orWhereDoesntHave` 등을 활용하면 됩니다.

### morphTo 관계 쿼리

`whereHasMorph`, `whereDoesntHaveMorph` 메서드로 morphTo 관계에 조건을 걸 수 있습니다.

와일드카드 `*`로 모든 morph 타입에 일괄 쿼리도 가능합니다.

<a name="aggregating-related-models"></a>
## 연관된 모델 집계

### 연관 모델 수 세기

`withCount`로 실제로 연관 모델을 불러오지 않고 개수만 가져올 수 있습니다.

복수 개의 관계, 기타 조건, 별칭 등 다양하게 지정 가능합니다.

`loadCount`로 이미 로드된 모델에서 추가로 관계 개수를 로드할 수도 있습니다.

### 기타 집계 함수

`withMin`, `withMax`, `withAvg`, `withSum`, `withExists` 등도 사용 가능합니다.

### morphTo 관계에서 연관 모델 집계

`with`와 `morphTo`의 `morphWithCount`, `loadMorphCount` 조합으로 다양하게 연관 모델 및 집계를 즉시 로딩할 수 있습니다.

<a name="eager-loading"></a>
## Eager 로딩(즉시 로딩)

관계의 데이터를 실제로 사용하기 전까지는 로드하지 않으므로, 많은 쿼리가 발생(N+1)할 수 있습니다. 이를 피하려면, 쿼리 시점에 `with`로 즉시 로딩해야 합니다.

여러 관계 혹은 중첩 관계도 배열로 지정해서 한 번에 로딩이 가능합니다.

`morphTo` 관계의 중첩도 자유롭게 eager loading 할 수 있습니다.

특정 컬럼만 선별해서 로드하려면 `with('author:id,name,book_id')` 와 같이 작성합니다.

#### 기본 Eager 로딩

모델의 `$with` 프로퍼티로 항상 특정 관계를 즉시 로딩하도록 설정할 수 있습니다. 쿼리 단위로 `without`, `withOnly` 등으로 일시적으로 변경도 가능합니다.

### Eager Load 제약

이벤트, Post 등 일부만 로딩하려면 closure로 조건을 추가할 수 있습니다.

`limit`, `take` 등 사용은 안 됩니다.

morphTo의 각 타입별로 다양한 제약을 걸 수 있습니다.

### withWhereHas

관계 존재 조건과 결과를 동시에 eager loading 하고 싶을 땐 `withWhereHas`를 사용합니다.

### Lazy Eager Loading

이미 모델을 조회했다가 그 중 일부에 대해 동적으로 관계를 불러와야 할 때는 `load`, `loadMissing`, `loadMorph` 등을 활용합니다.

### Lazy Loading 방지

`preventLazyLoading`을 통해 항상 lazy loading을 막고 Exception을 발생시켜 안전하게 사용 가능합니다. 로그만 기록하는 등 커스텀 처리도 할 수 있습니다.

<a name="inserting-and-updating-related-models"></a>
## 연관된 모델 삽입 및 수정

### `save` 메서드

`comments()` 같이 관계 인스턴스의 `save`를 이용하면, 외래 키를 직접 지정할 필요 없이 바로 모델을 추가할 수 있습니다. 여러 개를 한 번에 저장하려면 `saveMany`를 사용합니다.

수정/저장이 이루어진 후 관계 데이터를 다시 사용하려면 `refresh()`로 모델을 갱신해야 합니다.

#### 관계 및 하위 관계 재귀 저장

`push()` 메서드로 현재 모델과 하위 관계도 함께 일괄 저장할 수 있습니다.

### `create` 메서드

속성 배열만 넘겨서 연관된 모델을 생성하려면 `create`/`createMany`를 사용합니다.

이벤트를 발생시키지 않고 생성하려면 `createQuietly`, `createManyQuietly`를 씁니다.

`firstOrNew`, `firstOrCreate`, `updateOrCreate` 등의 메서드도 관계 내에서 활용할 수 있습니다.

> [!NOTE]
> `create` 사용 전 [대량 할당 방지](/docs/{{version}}/eloquent#mass-assignment) 내용을 확인하세요.

### Belongs To 관계 수정

자식 모델에 부모를 지정하려면 `associate`, 부모를 제거하려면 `dissociate`를 사용합니다.

### 다대다 관계 수정

#### attach/detach

관계를 추가/제거할 땐 `attach`, `detach`를 사용합니다. 추가 데이터도 배열로 넣을 수 있습니다.

배열로 여러 개를 붙이거나 뗄 수도 있습니다.

#### sync

`sync([ids])`는 주어진 id만 남기고 나머지는 중간 테이블에서 제거합니다. 추가 값도 배열로 지정할 수 있습니다.

`syncWithPivotValues([ids], [추가 값])`을 통해 여러 id에 같은 추가 데이터도 넣을 수 있습니다.

`syncWithoutDetaching([ids])`는 기존 id를 지우지 않고 새 id만 추가합니다.

#### toggle

`toggle([ids])`는 이미 연결된 id라면 해제, 없으면 추가합니다.

#### 중간 테이블 데이터 수정

`updateExistingPivot($id, [속성])`로 중간 테이블의 기존 데이터를 업데이트할 수 있습니다.

<a name="touching-parent-timestamps"></a>
## 부모 타임스탬프 갱신(Touching Parent Timestamps)

`belongsTo`, `belongsToMany` 관계를 가진 자식 모델에서, 자식이 수정될 때 부모의 `updated_at`도 함께 갱신하고자 한다면, 자식 모델의 `$touches` 배열에 관계명을 명시합니다.

> [!WARNING]
> 부모 타임스탬프는 Eloquent의 `save` 메서드로 자식 모델을 저장할 때만 갱신됩니다.

---

> 위 번역은 코드 블록, HTML 태그, 링크 URL의 영역은 변환하지 않고, 
> 원본 마크다운 형식을 최대한 충실히 유지하였습니다.