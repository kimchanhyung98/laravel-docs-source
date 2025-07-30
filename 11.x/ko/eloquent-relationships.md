# Eloquent: 관계 (Eloquent: Relationships)

- [소개](#introduction)
- [관계 정의하기](#defining-relationships)
    - [일대일 / Has One](#one-to-one)
    - [일대다 / Has Many](#one-to-many)
    - [일대다 (역방향) / Belongs To](#one-to-many-inverse)
    - [Has One of Many](#has-one-of-many)
    - [Has One Through](#has-one-through)
    - [Has Many Through](#has-many-through)
- [스코프된 관계](#scoped-relationships)
- [다대다 관계](#many-to-many)
    - [중간 테이블 컬럼 조회하기](#retrieving-intermediate-table-columns)
    - [중간 테이블 컬럼으로 쿼리 필터링하기](#filtering-queries-via-intermediate-table-columns)
    - [중간 테이블 컬럼으로 쿼리 정렬하기](#ordering-queries-via-intermediate-table-columns)
    - [커스텀 중간 테이블 모델 정의하기](#defining-custom-intermediate-table-models)
- [다형성 관계 (Polymorphic Relationships)](#polymorphic-relationships)
    - [일대일 다형성](#one-to-one-polymorphic-relations)
    - [일대다 다형성](#one-to-many-polymorphic-relations)
    - [One of Many 다형성](#one-of-many-polymorphic-relations)
    - [다대다 다형성](#many-to-many-polymorphic-relations)
    - [커스텀 다형성 타입](#custom-polymorphic-types)
- [동적 관계](#dynamic-relationships)
- [관계 쿼리하기](#querying-relations)
    - [관계 메서드 vs 동적 속성](#relationship-methods-vs-dynamic-properties)
    - [관계 존재 여부 쿼리하기](#querying-relationship-existence)
    - [관계 부재 쿼리하기](#querying-relationship-absence)
    - [Morph To 관계 쿼리하기](#querying-morph-to-relationships)
- [연관 모델 집계](#aggregating-related-models)
    - [연관 모델 카운트하기](#counting-related-models)
    - [기타 집계 함수](#other-aggregate-functions)
    - [Morph To 관계 카운트하기](#counting-related-models-on-morph-to-relationships)
- [즉시 로딩 (Eager Loading)](#eager-loading)
    - [즉시 로딩 제약 사항](#constraining-eager-loads)
    - [지연 즉시 로딩](#lazy-eager-loading)
    - [지연 로딩 방지하기](#preventing-lazy-loading)
- [연관 모델 삽입 및 갱신](#inserting-and-updating-related-models)
    - [`save` 메서드](#the-save-method)
    - [`create` 메서드](#the-create-method)
    - [Belongs To 관계 갱신](#updating-belongs-to-relationships)
    - [다대다 관계 갱신](#updating-many-to-many-relationships)
- [상위 모델 타임스탬프 갱신 (Touching Parent Timestamps)](#touching-parent-timestamps)

<a name="introduction"></a>
## 소개 (Introduction)

데이터베이스 테이블은 종종 서로 관계를 맺고 있습니다. 예를 들어, 블로그 게시글은 여러 댓글을 가질 수 있고, 주문(order)은 해당 주문을 처리한 사용자(user)와 연결될 수 있습니다. Eloquent는 이러한 관계를 관리하고 다루는 것을 매우 쉽게 만들어 주며 다음과 같은 다양한 일반적인 관계를 지원합니다:

<div class="content-list" markdown="1">

- [일대일 (One To One)](#one-to-one)
- [일대다 (One To Many)](#one-to-many)
- [다대다 (Many To Many)](#many-to-many)
- [Has One Through](#has-one-through)
- [Has Many Through](#has-many-through)
- [다형성 일대일 (One To One Polymorphic)](#one-to-one-polymorphic-relations)
- [다형성 일대다 (One To Many Polymorphic)](#one-to-many-polymorphic-relations)
- [다형성 다대다 (Many To Many Polymorphic)](#many-to-many-polymorphic-relations)

</div>

<a name="defining-relationships"></a>
## 관계 정의하기 (Defining Relationships)

Eloquent 관계는 Eloquent 모델 클래스 안에 메서드로 정의됩니다. 관계는 강력한 [쿼리 빌더](/docs/11.x/queries) 역할도 수행하기 때문에 메서드로 정의하면 메서드 체이닝이나 쿼리 조작이 매우 편리해집니다. 예를 들어, `posts` 관계에 추가 조건을 붙일 수도 있습니다:

```
$user->posts()->where('active', 1)->get();
```

하지만 관계들을 본격적으로 사용하기 전에, Eloquent가 지원하는 각 관계 유형을 어떻게 정의하는지부터 살펴보겠습니다.

<a name="one-to-one"></a>
### 일대일 / Has One (One to One / Has One)

일대일 관계는 가장 기본적인 관계 유형입니다. 예를 들어, `User` 모델이 하나의 `Phone` 모델과 연결되는 관계입니다. 이 관계를 정의하려면 `User` 모델 안에 `phone` 메서드를 만들고, 이 메서드가 `hasOne` 메서드를 호출하여 반환하도록 합니다. `hasOne` 메서드는 `Illuminate\Database\Eloquent\Model` 기본 클래스를 통해 모델에서 사용할 수 있습니다:

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

`hasOne` 메서드의 첫 번째 인수에는 관련 모델 클래스 이름을 넣습니다. 관계가 정의되면 Eloquent의 동적 속성(dynamic properties)을 통해 관련된 레코드를 쉽게 조회할 수 있습니다. 동적 속성은 관계 메서드를 마치 모델에 정의된 속성인 것처럼 접근할 수 있게 합니다:

```php
$phone = User::find(1)->phone;
```

Eloquent는 관계의 외래 키(foreign key)를 부모 모델 이름을 기준으로 자동 결정합니다. 이 예에서는 `Phone` 모델은 자동으로 `user_id` 외래 키를 갖는 것으로 가정합니다. 기본 규칙을 변경하려면 `hasOne` 메서드에 두 번째 인수로 외래 키 이름을 전달할 수 있습니다:

```php
return $this->hasOne(Phone::class, 'foreign_key');
```

또한 Eloquent는 외래 키가 부모 모델의 기본 키와 일치한다고 가정합니다(예: `user.id` 값이 `phone.user_id`에 저장). 만약 기본 키가 `id`가 아니거나 다른 컬럼을 사용하려면 세 번째 인수로 로컬 키(local key)를 지정할 수 있습니다:

```php
return $this->hasOne(Phone::class, 'foreign_key', 'local_key');
```

<a name="one-to-one-defining-the-inverse-of-the-relationship"></a>
#### 관계의 역방향 정의하기

`User` 모델에서 `Phone`을 접근할 수 있듯이, `Phone` 모델에서 소유자 사용자(`User`)를 접근할 수 있게 관계를 반대로 정의할 수 있습니다. `hasOne`의 역방향 관계는 `belongsTo` 메서드로 정의합니다:

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

`user` 메서드를 호출하면 Eloquent는 `Phone` 모델의 `user_id` 컬럼과 일치하는 `User` 모델의 `id` 값을 찾아 반환합니다.

외래 키 이름은 관계 메서드 이름에 `_id`를 붙여 자동 결정합니다. 즉, `Phone` 모델에 `user_id` 컬럼이 있다고 가정합니다. 만약 다르다면 두 번째 인수로 외래 키 이름을 지정할 수 있습니다:

```php
public function user(): BelongsTo
{
    return $this->belongsTo(User::class, 'foreign_key');
}
```

부모 모델 키가 `id`가 아니거나 다른 컬럼을 사용하려면 세 번째 인수로 부모 모델의 키를 지정합니다:

```php
public function user(): BelongsTo
{
    return $this->belongsTo(User::class, 'foreign_key', 'owner_key');
}
```

<a name="one-to-many"></a>
### 일대다 / Has Many (One to Many / Has Many)

일대다 관계는 하나의 부모 모델이 여러 자식 모델을 가질 때 사용합니다. 예를 들어, 게시글(Post)은 무한한 댓글(Comment)을 가질 수 있습니다. Eloquent 관계처럼 일대다 관계도 모델에 메서드를 정의해서 설정합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Post extends Model
{
    /**
     * 이 게시글에 달린 댓글들을 가져옵니다.
     */
    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class);
    }
}
```

Eloquent는 댓글(`Comment`) 모델의 외래 키 컬럼 이름을 자동으로 결정합니다. 부모 모델의 "스네이크 케이스(snake_case)" 이름 뒤에 `_id`를 붙이는 것이 기본 규칙입니다. 따라서 이 예에서는 `comments` 테이블에 `post_id` 외래 키가 있다고 가정합니다.

관계 메서드가 정의되면 `comments` 동적 속성을 이용해 연관된 댓글 [컬렉션](/docs/11.x/eloquent-collections)을 접근할 수 있습니다:

```php
use App\Models\Post;

$comments = Post::find(1)->comments;

foreach ($comments as $comment) {
    // ...
}
```

모든 관계는 쿼리 빌더 역할도 하므로, 관계 메서드를 호출한 상태에서 추가 쿼리 제약을 걸 수도 있습니다:

```php
$comment = Post::find(1)->comments()
    ->where('title', 'foo')
    ->first();
```

`hasOne`과 마찬가지로 외래 키와 로컬 키는 `hasMany` 메서드에 인수를 추가해 재정의할 수 있습니다:

```php
return $this->hasMany(Comment::class, 'foreign_key');

return $this->hasMany(Comment::class, 'foreign_key', 'local_key');
```

<a name="automatically-hydrating-parent-models-on-children"></a>
#### 자식 모델에서 부모 모델 자동 로딩 (자동 하이드레이팅)

Eager loading을 사용해도 자식 모델들을 순회하면서 자식에서 부모 모델을 참조할 때 "N+1 쿼리 문제"가 발생할 수 있습니다:

```php
$posts = Post::with('comments')->get();

foreach ($posts as $post) {
    foreach ($post->comments as $comment) {
        echo $comment->post->title; // N+1 문제 발생
    }
}
```

댓글을 eager load 했지만, Eloquent는 댓글 모델 하나하나에 부모 `Post` 모델을 자동으로 하이드레이팅하지 않으므로 1개의 Post를 가져오는 쿼리가 댓글 수만큼 실행됩니다.

부모 모델을 자식에 자동으로 하이드레이팅하려면 `hasMany` 관계 정의 시 `chaperone` 메서드를 호출하세요:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Post extends Model
{
    /**
     * 이 게시글에 달린 댓글들을 가져옵니다.
     */
    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class)->chaperone();
    }
}
```

런타임 시에 자동 하이드레이팅을 선택적으로 활성화하려면, eager loading 시 `chaperone()`을 실행할 수 있습니다:

```php
use App\Models\Post;

$posts = Post::with([
    'comments' => fn ($comments) => $comments->chaperone(),
])->get();
```

<a name="one-to-many-inverse"></a>
### 일대다 (역방향) / Belongs To (One to Many (Inverse) / Belongs To)

이제 게시글에 달린 댓글들이 있지만, 한 댓글에서는 부모 게시글에 접근할 수 있도록 관계를 반대로 정의할 차례입니다. `hasMany` 관계의 역방향은 자식 모델에 `belongsTo` 관계를 정의하여 구현합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Comment extends Model
{
    /**
     * 댓글이 속한 게시글을 가져옵니다.
     */
    public function post(): BelongsTo
    {
        return $this->belongsTo(Post::class);
    }
}
```

관계가 정의되면 `post` 동적 속성을 통해 댓글의 부모 게시글 모델에 접근할 수 있습니다:

```php
use App\Models\Comment;

$comment = Comment::find(1);

return $comment->post->title;
```

기본적으로 Eloquent는 관계 메서드 이름 뒤에 `_`와 부모 모델 기본 키 이름을 붙인 형식을 외래 키로 추측합니다. 이 예시에서는 `post_id`를 외래 키로 가정합니다.

외래 키 이름이 달라질 경우 `belongsTo`의 두 번째 인수로 지정할 수 있습니다:

```php
public function post(): BelongsTo
{
    return $this->belongsTo(Post::class, 'foreign_key');
}
```

기본 키가 `id`가 아니거나 다른 컬럼을 참조하려면 세 번째 인수로 부모 테이블의 키를 지정합니다:

```php
public function post(): BelongsTo
{
    return $this->belongsTo(Post::class, 'foreign_key', 'owner_key');
}
```

<a name="default-models"></a>
#### 기본 모델 지정하기 (Default Models)

`belongsTo`, `hasOne`, `hasOneThrough`, `morphOne` 관계에서는 관계가 `null`일 때 기본 모델을 반환하도록 할 수 있습니다. 이는 [Null Object 패턴](https://en.wikipedia.org/wiki/Null_Object_pattern)으로, 코드 내 조건문을 줄이는 데 도움됩니다.

예를 들어, `Post` 모델의 `user` 관계가 `null`일 때 빈 `App\Models\User` 인스턴스를 반환하려면 다음과 같이 합니다:

```php
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault();
}
```

기본 모델에 속성을 지정하려면 배열이나 클로저를 전달할 수 있습니다:

```php
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault([
        'name' => 'Guest Author',
    ]);
}

public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault(function (User $user, Post $post) {
        $user->name = 'Guest Author';
    });
}
```

<a name="querying-belongs-to-relationships"></a>
#### Belongs To 관계 쿼리하기

"belongs to" 관계의 자식 모델을 조회할 때 `where` 조건을 직접 작성하는 대신 아래처럼 하면 간편합니다:

```php
use App\Models\Post;

$posts = Post::where('user_id', $user->id)->get();
```

또한 `whereBelongsTo` 메서드를 사용하면 자동으로 외래 키를 추론해 줍니다:

```php
$posts = Post::whereBelongsTo($user)->get();
```

컬렉션을 넘기면 컬렉션에 속한 모든 부모에 속하는 모델을 조회합니다:

```php
$users = User::where('vip', true)->get();

$posts = Post::whereBelongsTo($users)->get();
```

관계 이름이 자동 추론과 다르면 두 번째 인수로 직접 지정할 수 있습니다:

```php
$posts = Post::whereBelongsTo($user, 'author')->get();
```

<a name="has-one-of-many"></a>
### Has One of Many

하나의 모델이 여러 관련 모델을 가지지만, 그중에서 가장 최신(latest) 혹은 가장 오래된(oldest) 단 하나만 간편하게 조회하고 싶을 때 사용합니다.

예를 들어, `User`가 여러 `Order`를 소유하지만 가장 최신 주문만 조회하려면, `hasOne` 관계에 `ofMany` 메서드를 조합해 아래처럼 구현합니다:

```php
/**
 * 사용자의 최신 주문을 가져옵니다.
 */
public function latestOrder(): HasOne
{
    return $this->hasOne(Order::class)->latestOfMany();
}
```

최신이 아닌 가장 오래된 주문을 조회하려면 `oldestOfMany()`를 사용합니다:

```php
/**
 * 사용자의 가장 오래된 주문을 가져옵니다.
 */
public function oldestOrder(): HasOne
{
    return $this->hasOne(Order::class)->oldestOfMany();
}
```

기본적으로 최신/최초 주문 기준은 모델의 정렬 가능한 기본 키(`id`)를 사용하지만, 다른 기준 컬럼 및 `min` 또는 `max` 집계 함수도 지정할 수 있습니다:

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
> PostgreSQL은 UUID 컬럼에 `MAX` 함수 실행을 지원하지 않아, PostgreSQL UUID 컬럼을 쓸 때는 이 관계를 사용할 수 없습니다.

<a name="converting-many-relationships-to-has-one-relationships"></a>
#### "많은" 관계를 Has One으로 변환하기

대부분 `latestOfMany`, `oldestOfMany`, `ofMany` 등 메서드를 사용할 때는 이미 같은 모델에 대해 has many 관계가 정의되어 있습니다. 이 경우 편의를 위해 `one` 메서드를 호출해 "has many" 관계를 "has one" 관계로 변환할 수 있습니다:

```php
/**
 * 사용자의 모든 주문
 */
public function orders(): HasMany
{
    return $this->hasMany(Order::class);
}

/**
 * 가장 큰 주문
 */
public function largestOrder(): HasOne
{
    return $this->orders()->one()->ofMany('price', 'max');
}
```

<a name="advanced-has-one-of-many-relationships"></a>
#### 고급 Has One of Many 관계

더 복잡한 조건이 필요한 경우 배열과 클로저를 결합해 사용할 수 있습니다.

예를 들어, `Product`가 여러 `Price` 레코드를 갖는데, 미래 날짜에 적용될 가격도 포함되어 언제든지 새 가격이 발행될 수 있습니다. 현재 기준 최신 정보를 가져오려면, 발행일이 미래가 아닌 (`published_at < now()`) 것을 조건에 넣고, 발행일이 같으면 아이디가 큰 쪽을 선택할 수도 있습니다.

아래 코드는 다중 정렬 기준과 추가 조건을 클로저로 넣은 예제입니다:

```php
/**
 * 제품의 현재 가격을 가져옵니다.
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

"Has One Through" 관계는 1:1 관계이지만, 직접적으로 연결되지 않은 두 모델을 제3의 중간 모델을 통해 연결할 때 사용합니다.

예를 들어 차량 수리 공장 애플리케이션에서 `Mechanic` 모델은 여러 `Car`를 담당할 수 있고, 각 `Car`는 한 명의 `Owner`(소유자)를 가질 수 있습니다. 정비공과 소유자는 데이터베이스에 직접 연관관계가 없으나, 정비공은 자동차를 통해 소유자와 연결할 수 있습니다.

아래는 필요한 테이블 구조입니다:

```
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

`Mechanic` 모델에 관계를 정의하면 다음과 같습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasOneThrough;

class Mechanic extends Model
{
    /**
     * 자동차 소유자를 가져옵니다.
     */
    public function carOwner(): HasOneThrough
    {
        return $this->hasOneThrough(Owner::class, Car::class);
    }
}
```

`hasOneThrough` 메서드의 첫 번째 인수는 최종 접근 대상 모델이고 두 번째 인수는 중간 모델입니다.

모델들에 이미 관계가 정의되어 있다면, `through` 메서드를 사용해 아래처럼 체이닝 방식으로 관계를 정의할 수도 있습니다:

```php
// 문자열 기반 문법
return $this->through('cars')->has('owner');

// 동적 메서드 문법
return $this->throughCars()->hasOwner();
```

<a name="has-one-through-key-conventions"></a>
#### 키 규칙 (Key Conventions)

기본 키 및 외래 키 이름은 Eloquent의 관례를 따릅니다. 키 이름을 커스터마이징하려면 `hasOneThrough`의 세 번째부터 여섯 번째 인수에 차례로 지정하세요. 세 번째는 중간 모델의 외래 키, 네 번째는 최종 모델의 외래 키, 다섯 번째는 부모(로컬) 키, 여섯 번째는 중간 모델의 로컬 키입니다:

```php
class Mechanic extends Model
{
    public function carOwner(): HasOneThrough
    {
        return $this->hasOneThrough(
            Owner::class,
            Car::class,
            'mechanic_id',  // 중간 테이블 외래키
            'car_id',       // 최종 테이블 외래키
            'id',           // 부모 테이블 기본키
            'id'            // 중간 테이블 기본키
        );
    }
}
```

<a name="has-many-through"></a>
### Has Many Through

"Has Many Through" 관계는 중간 모델을 거쳐 여러 모델에 접근하고자 할 때 사용합니다.

예를 들어, [Laravel Vapor](https://vapor.laravel.com)와 같은 배포 플랫폼이라면, `Project` 모델은 `Environment`를 통해 `Deployment`들의 묶음을 간단히 조회할 수 있습니다.

필요한 테이블 구조는 다음과 같습니다:

```
projects
    id - integer
    name - string

environments
    id - integer
    project_id - integer
    name - string

deployments
    id - integer
    environment_id - integer
    commit_hash - string
```

`Project` 모델에 관계를 정의하면 다음과 같습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasManyThrough;

class Project extends Model
{
    /**
     * 프로젝트와 연결된 모든 deployment들을 가져옵니다.
     */
    public function deployments(): HasManyThrough
    {
        return $this->hasManyThrough(Deployment::class, Environment::class);
    }
}
```

`hasManyThrough` 첫 번째 인자는 최종 대상 모델, 두 번째는 중간 모델입니다.

이미 모델들에 관계가 있으면 `through` 메서드 체인으로 정의할 수도 있습니다:

```php
// 문자열 기반 문법
return $this->through('environments')->has('deployments');

// 동적 메서드 문법
return $this->throughEnvironments()->hasDeployments();
```

`deployments` 테이블에 `project_id`가 없더라도, `Environment`의 `project_id`를 기준으로 관련 deployment를 조회할 수 있습니다.

<a name="has-many-through-key-conventions"></a>
#### 키 규칙 (Key Conventions)

키 이름을 커스터마이징하려면 인수로 전달하세요:

```php
class Project extends Model
{
    public function deployments(): HasManyThrough
    {
        return $this->hasManyThrough(
            Deployment::class,
            Environment::class,
            'project_id',       // 중간 테이블 외래키
            'environment_id',   // 최종 테이블 외래키
            'id',               // 부모 테이블 기본키
            'id'                // 중간 테이블 기본키
        );
    }
}
```

<a name="scoped-relationships"></a>
### 스코프된 관계 (Scoped Relationships)

관계에 추가 제약 조건을 붙인 메서드를 모델에 정의할 수 있습니다.

예를 들어, `User` 모델에 `posts` 메서드가 있고, 그 중에서 `featured`가 `true`인 게시글을 조회하는 `featuredPosts`를 추가한다고 합시다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class User extends Model
{
    /**
     * 모든 게시글
     */
    public function posts(): HasMany
    {
        return $this->hasMany(Post::class)->latest();
    }

    /**
     * 추천 게시글
     */
    public function featuredPosts(): HasMany
    {
        return $this->posts()->where('featured', true);
    }
}
```

하지만 `featuredPosts` 관계를 통해 새 모델을 생성하면, `featured`가 자동으로 `true`가 되지 않습니다.

관계 메서드로 모델을 생성할 때 특정 속성을 자동으로 추가하고 싶다면 `withAttributes`를 사용합니다:

```php
/**
 * 추천 게시글
 */
public function featuredPosts(): HasMany
{
    return $this->posts()->withAttributes(['featured' => true]);
}
```

이 메서드는 쿼리에 `where` 조건을 붙이고, 생성 시 전달한 속성도 자동으로 설정해 줍니다:

```php
$post = $user->featuredPosts()->create(['title' => 'Featured Post']);

$post->featured; // true
```

<a name="many-to-many"></a>
## 다대다 관계 (Many to Many Relationships)

다대다 관계는 `hasOne`, `hasMany`보다 약간 복잡합니다.

예를 들어, 사용자가 여러 역할(role)을 가질 수 있고 역할 역시 여러 사용자와 연결될 수 있습니다. 예를 들어 "Author", "Editor" 역할을 여러 사용자들이 공유하는 경우입니다.

<a name="many-to-many-table-structure"></a>
#### 테이블 구조

세 개의 테이블이 필요합니다: `users`, `roles`, `role_user`

`role_user`는 중간 테이블로, 알파벳 순서로 관련 모델 이름 두 개를 조합한 이름이며, `user_id`, `role_id` 컬럼을 포함합니다.

중간 테이블이 필요한 이유는, 역할이 여러 사용자와 관계를 맺기 때문입니다. 단일 `roles` 테이블에만 `user_id` 칼럼이 있으면 역할이 한 사용자에게만 속할 수 있기 때문입니다.

아래처럼 요약할 수 있습니다:

```
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
#### 모델 정의

다대다 관계는 관련 모델에 `belongsToMany` 메서드 반환하는 메서드를 만들어 정의합니다. 이 메서드는 모든 Eloquent 모델의 기본 클래스에서 제공됩니다.

예를 들어, `User` 모델에 `roles` 메서드를 정의합시다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class User extends Model
{
    /**
     * 사용자가 가진 역할들
     */
    public function roles(): BelongsToMany
    {
        return $this->belongsToMany(Role::class);
    }
}
```

정의 후엔 `roles` 동적 속성으로 사용자의 역할들을 조회할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

foreach ($user->roles as $role) {
    // ...
}
```

관계는 쿼리 빌더 역할도 하므로, 메서드로 호출 후 추가 조건을 쓸 수 있습니다:

```php
$roles = User::find(1)->roles()->orderBy('name')->get();
```

중간 테이블 이름은 기본적으로 관련 모델 이름 두 개를 알파벳 순서로 결합해 결정하지만, 두 번째 인수로 재정의할 수 있습니다:

```php
return $this->belongsToMany(Role::class, 'role_user');
```

중간 테이블 칼럼 이름(외래 키)도 세 번째, 네 번째 인수로 변경 가능합니다. 세 번째는 현재 모델의 외래 키, 네 번째는 연결된 모델의 외래 키입니다:

```php
return $this->belongsToMany(Role::class, 'role_user', 'user_id', 'role_id');
```

<a name="many-to-many-defining-the-inverse-of-the-relationship"></a>
#### 역방향 관계 정의

다대다 역방향 관계도 `belongsToMany`를 반환하는 메서드로 정의합니다.

`Role` 모델에 `users` 메서드를 정의하는 예:

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
        return $this->belongsToMany(User::class);
    }
}
```

사용법과 옵션은 앞서 정의한 `User` 모델의 `roles`와 동일합니다.

<a name="retrieving-intermediate-table-columns"></a>
### 중간 테이블 컬럼 조회하기

다대다 관계에서 중간 테이블에 추가 컬럼(예: `active`, `created_by`)이 있을 경우 해당 값에 접근하려면 관계 정의에 컬럼명을 지정해 줘야 합니다.

```php
return $this->belongsToMany(Role::class)->withPivot('active', 'created_by');
```

중간 테이블의 `created_at`, `updated_at` 타임스탬프를 자동 유지하고 싶다면 `withTimestamps()`를 호출하세요:

```php
return $this->belongsToMany(Role::class)->withTimestamps();
```

> [!WARNING]  
> 자동 타임스탬프 유지용 중간 테이블은 `created_at`과 `updated_at` 컬럼이 모두 있어야 합니다.

<a name="customizing-the-pivot-attribute-name"></a>
#### `pivot` 속성명 변경하기

중간 테이블 데이터를 담는 기본 `pivot` 속성명은 변경할 수 있습니다.

예를 들어 `users`와 `podcasts`로 구독(subscriptions) 관계를 구현했을 때, 피벗 속성명을 `subscription`으로 지정하면 아래처럼 사용할 수 있습니다:

```php
return $this->belongsToMany(Podcast::class)
    ->as('subscription')
    ->withTimestamps();
```

조회 시:

```php
$users = User::with('podcasts')->get();

foreach ($users->flatMap->podcasts as $podcast) {
    echo $podcast->subscription->created_at;
}
```

<a name="filtering-queries-via-intermediate-table-columns"></a>
### 중간 테이블 컬럼을 이용한 쿼리 필터링

`belongsToMany` 쿼리에서 `wherePivot()`, `wherePivotIn()`, `wherePivotNotIn()`, `wherePivotBetween()`, `wherePivotNotBetween()`, `wherePivotNull()`, `wherePivotNotNull()` 메서드를 이용해 중간 테이블 컬럼으로 필터링 할 수 있습니다:

```php
return $this->belongsToMany(Role::class)
    ->wherePivot('approved', 1);

return $this->belongsToMany(Role::class)
    ->wherePivotIn('priority', [1, 2]);

return $this->belongsToMany(Role::class)
    ->wherePivotNull('expired_at');
```

`wherePivot`은 쿼리 제한에만 사용되며, 생성 시 해당 값이 자동으로 대입되지 않습니다. 생성 시에도 특정 pivot 값을 포함하려면 `withPivotValue()`를 이용하세요:

```php
return $this->belongsToMany(Role::class)
        ->withPivotValue('approved', 1);
```

<a name="ordering-queries-via-intermediate-table-columns"></a>
### 중간 테이블 컬럼으로 쿼리 정렬

`orderByPivot` 메서드를 사용해 중간 테이블 컬럼을 기준으로 정렬할 수 있습니다:

```php
return $this->belongsToMany(Badge::class)
    ->where('rank', 'gold')
    ->orderByPivot('created_at', 'desc');
```

<a name="defining-custom-intermediate-table-models"></a>
### 커스텀 중간 테이블 모델 정의하기

중간 테이블을 표현하는 커스텀 pivot 모델을 만들고 싶을 때 `using` 메서드를 호출해 지정할 수 있습니다. 커스텀 pivot 모델은 `Illuminate\Database\Eloquent\Relations\Pivot`를 확장해야 합니다.

예를 들어 `Role` 모델에 사용자와의 중간 테이블을 커스텀 모델로 명시하는 방식은 다음과 같습니다:

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

`RoleUser` 피벗 모델:

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
> Pivot 모델은 `SoftDeletes` 트레이트를 사용할 수 없습니다.

<a name="custom-pivot-models-and-incrementing-ids"></a>
#### 커스텀 Pivot 모델과 자동 증가 ID

커스텀 pivot 모델이 자동 증가하는 기본 키를 가진 경우 `public $incrementing = true;` 프로퍼티를 지정해야 합니다:

```php
/**
 * 자동 증가 여부
 *
 * @var bool
 */
public $incrementing = true;
```

<a name="polymorphic-relationships"></a>
## 다형성 관계 (Polymorphic Relationships)

다형성 관계는 자식 모델이 여러 유형의 부모 모델에 속할 수 있는 관계를 뜻합니다.

예를 들어, 하나의 `Comment` 모델이 `Post`와 `Video` 두 모델 모두에 속할 수 있는 경우가 있습니다.

<a name="one-to-one-polymorphic-relations"></a>
### 일대일 다형성 (One to One Polymorphic)

<a name="one-to-one-polymorphic-table-structure"></a>
#### 테이블 구조

다형성 일대일 관계는 일반적인 일대일 관계와 비슷하지만, 하나의 자식 모델이 여러 부모 모델 유형(different types)에 속할 수 있습니다.

예를 들어, `Post`와 `User`가 하나의 `Image` 모델을 공유하는 경우가 그렇습니다.

`images` 테이블에 `imageable_id`와 `imageable_type` 두 컬럼이 있어, 어떤 부모 모델과 연결되는지 판별합니다.

```
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

`imageable_id` 컬럼에는 `Post` 또는 `User`의 id 값, `imageable_type`에는 해당 모델의 클래스명(`App\Models\Post` 또는 `App\Models\User`)이 저장됩니다.

<a name="one-to-one-polymorphic-model-structure"></a>
#### 모델 구조

모델에 관계를 다음과 같이 정의합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class Image extends Model
{
    /**
     * 이 이미지가 속한 부모 모델 (User 또는 Post)를 가져옵니다.
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
     * 게시글의 이미지
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
     * 사용자의 이미지
     */
    public function image(): MorphOne
    {
        return $this->morphOne(Image::class, 'imageable');
    }
}
```

<a name="one-to-one-polymorphic-retrieving-the-relationship"></a>
#### 관계 조회

정의 후엔 모델의 동적 속성으로 접근합니다:

```php
use App\Models\Post;

$post = Post::find(1);

$image = $post->image;
```

자식 모델에서 부모 모델로 접근할 땐 `MorphTo` 메서드 이름(`imageable`)을 동적 속성으로 접근합니다:

```php
use App\Models\Image;

$image = Image::find(1);

$imageable = $image->imageable; // Post 또는 User 인스턴스
```

<a name="morph-one-to-one-key-conventions"></a>
#### 키 규칙

다형성 모델의 `id`와 `type` 컬럼을 직접 지정할 때는 `morphTo`에 관계 이름을 첫 인수로 넣어야 하며, 보통 메서드 이름과 일치시킵니다:

```php
public function imageable(): MorphTo
{
    return $this->morphTo(__FUNCTION__, 'imageable_type', 'imageable_id');
}
```

<a name="one-to-many-polymorphic-relations"></a>
### 일대다 다형성 (One to Many Polymorphic)

<a name="one-to-many-polymorphic-table-structure"></a>
#### 테이블 구조

다형성 일대다 관계도 일반 일대다 관계와 비슷하지만, 자식 모델이 여러 부모 유형을 가질 수 있습니다.

예를 들어 사용자들이 게시글과 비디오에 댓글을 달 수 있다면 단일 `comments` 테이블로 댓글을 관리합니다:

```
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
#### 모델 정의

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class Comment extends Model
{
    /**
     * 이 댓글이 달린 부모 모델(Post 또는 Video)
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
     * 게시글에 달린 모든 댓글
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
     * 비디오에 달린 모든 댓글
     */
    public function comments(): MorphMany
    {
        return $this->morphMany(Comment::class, 'commentable');
    }
}
```

<a name="one-to-many-polymorphic-retrieving-the-relationship"></a>
#### 관계 조회

정의가 완료되면 모델의 동적 속성으로 접근합니다:

```php
use App\Models\Post;

$post = Post::find(1);

foreach ($post->comments as $comment) {
    // ...
}
```

다형성 자식 모델에서 부모 모델 접근은 `morphTo` 관계 메서드명(`commentable`)을 통해 합니다:

```php
use App\Models\Comment;

$comment = Comment::find(1);

$commentable = $comment->commentable; // Post 또는 Video 인스턴스
```

<a name="polymorphic-automatically-hydrating-parent-models-on-children"></a>
#### 자식 모델의 부모 자동 하이드레이팅

`Post`를 eager load했지만 댓글의 각 부모 모델(`commentable`)이 자동으로 하이드레이팅되지 않아 N+1 쿼리 문제가 발생할 수 있습니다:

```php
$posts = Post::with('comments')->get();

foreach ($posts as $post) {
    foreach ($post->comments as $comment) {
        echo $comment->commentable->title;
    }
}
```

이를 방지하려면 `morphMany` 정의 시 `chaperone()`를 호출하세요:

```php
class Post extends Model
{
    public function comments(): MorphMany
    {
        return $this->morphMany(Comment::class, 'commentable')->chaperone();
    }
}
```

런타임에 선택적으로 활성화하려면 eager load 시 `chaperone()` 호출:

```php
use App\Models\Post;

$posts = Post::with([
    'comments' => fn ($comments) => $comments->chaperone(),
])->get();
```

<a name="one-of-many-polymorphic-relations"></a>
### One of Many 다형성 (One of Many (Polymorphic))

한 모델이 다수의 연관 모델을 가지지만, 그중 최고(최신,최초 등)만 접근하고 싶을 때 사용합니다.

예를 들어, `User`가 여러 `Image`를 가질 수 있지만 최신 이미지만 쉽게 접근할 수 있도록:

```php
/**
 * 사용자의 최신 이미지
 */
public function latestImage(): MorphOne
{
    return $this->morphOne(Image::class, 'imageable')->latestOfMany();
}
```

최초 이미지를 원하면 `oldestOfMany()`를 사용합니다:

```php
/**
 * 사용자의 최초 이미지
 */
public function oldestImage(): MorphOne
{
    return $this->morphOne(Image::class, 'imageable')->oldestOfMany();
}
```

다른 정렬 기준도 가능합니다:

```php
/**
 * 가장 좋아요가 많은 이미지
 */
public function bestImage(): MorphOne
{
    return $this->morphOne(Image::class, 'imageable')->ofMany('likes', 'max');
}
```

> [!NOTE]  
> 더 고급 관계 예제는 [Has One of Many 문서](#advanced-has-one-of-many-relationships)를 참고하세요.

<a name="many-to-many-polymorphic-relations"></a>
### 다대다 다형성 (Many to Many Polymorphic)

<a name="many-to-many-polymorphic-table-structure"></a>
#### 테이블 구조

다대다 다형성은 `morphOne`, `morphMany`보다 복잡합니다.

예를 들어 `Post`와 `Video`가 모두 공유하는 `Tag` 모델이 있을 때, 하나의 고유한 태그 테이블로 여러 모델과 관계를 맺습니다.

중간 테이블에는 타입과 아이디를 기록합니다:

```
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
> 일반적인 [다대다 관계](#many-to-many) 문서를 먼저 읽으면 도움됩니다.

<a name="many-to-many-polymorphic-model-structure"></a>
#### 모델 정의

`Post`와 `Video` 모델에 `morphToMany` 관계를 정의합니다. 첫 인자는 관련 모델, 두 번째는 관계 이름("taggable")입니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphToMany;

class Post extends Model
{
    /**
     * 게시글에 연결된 모든 태그
     */
    public function tags(): MorphToMany
    {
        return $this->morphToMany(Tag::class, 'taggable');
    }
}
```

<a name="many-to-many-polymorphic-defining-the-inverse-of-the-relationship"></a>
#### 역방향 관계 정의

`Tag` 모델에 가능한 부모 모델별 관계를 각각 정의합니다. 각각 `morphedByMany`로 구현합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphToMany;

class Tag extends Model
{
    /**
     * 이 태그가 연결된 게시글들
     */
    public function posts(): MorphToMany
    {
        return $this->morphedByMany(Post::class, 'taggable');
    }

    /**
     * 이 태그가 연결된 동영상들
     */
    public function videos(): MorphToMany
    {
        return $this->morphedByMany(Video::class, 'taggable');
    }
}
```

<a name="many-to-many-polymorphic-retrieving-the-relationship"></a>
#### 관계 조회

정의 후 다음과 같이 태그들을 조회할 수 있습니다:

```php
use App\Models\Post;

$post = Post::find(1);

foreach ($post->tags as $tag) {
    // ...
}
```

`Tag` 모델에서 부모 관계로 다음과 같이 접근할 수 있습니다:

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

기본적으로 Laravel은 다형성 관계 타입 컬럼에 풀 네임스페이스 모델명을 저장합니다.

예를 들어 `Comment` 모델의 경우 `commentable_type` 컬럼이 `App\Models\Post` 또는 `App\Models\Video` 값을 가집니다.

하지만 내부 구조와 관계 없이, 단순 문자열(예: `post`, `video`)을 타입 값으로 지정하고 싶을 때가 있습니다.

이럴 때는 아래처럼 "morph map"을 설정하세요:

```php
use Illuminate\Database\Eloquent\Relations\Relation;

Relation::enforceMorphMap([
    'post' => 'App\Models\Post',
    'video' => 'App\Models\Video',
]);
```

이 코드를 `AppServiceProvider`의 `boot` 메서드 안에 넣거나 별도의 서비스 프로바이더에 작성합니다.

런타임 시는 `getMorphClass` 메서드로 별칭을 얻을 수 있고, `Relation::getMorphedModel`로 해당 별칭의 풀 클래스명을 얻을 수 있습니다:

```php
$alias = $post->getMorphClass();

$class = Relation::getMorphedModel($alias);
```

> [!WARNING]  
> 기존 애플리케이션에 morph map을 추가하면, DB 내 다형성 타입 컬럼 중 풀 네임스페이스 값들은 모두 매핑된 별칭으로 변환해줘야 합니다.

<a name="dynamic-relationships"></a>
### 동적 관계 (Dynamic Relationships)

`resolveRelationUsing` 메서드를 사용해 런타임에 모델 관계를 동적으로 정의할 수도 있습니다. 주로 Laravel 패키지 개발 시 활용하며, 일반 개발 시 권장하지 않습니다.

사용법 예시 (`service provider`의 `boot` 메서드 내에 작성):

```php
use App\Models\Order;
use App\Models\Customer;

Order::resolveRelationUsing('customer', function (Order $orderModel) {
    return $orderModel->belongsTo(Customer::class, 'customer_id');
});
```

> [!WARNING]  
> 동적 관계 정의 시엔 항상 관계 키 이름을 명시적으로 지정하세요.

<a name="querying-relations"></a>
## 관계 쿼리하기 (Querying Relations)

Eloquent 관계는 메서드로 정의되므로, 호출하면 관계 인스턴스를 얻을 수 있어 쿼리를 실행하지 않고도 추가 제한 조건을 계속 쌓을 수 있습니다.

예를 들어, `User` 모델이 여러 `Post` 모델과 연결되어 있을 때:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class User extends Model
{
    /**
     * 해당 사용자의 모든 게시글
     */
    public function posts(): HasMany
    {
        return $this->hasMany(Post::class);
    }
}
```

아래처럼 관계를 호출하여 추가 조건을 붙일 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

$user->posts()->where('active', 1)->get();
```

조회용 모든 Laravel 쿼리 빌더 메서드를 관계에 사용할 수 있으므로, 다양한 메서드를 탐색해 보세요.

<a name="chaining-orwhere-clauses-after-relationships"></a>
#### 관계 뒤에 `orWhere` 체이닝 주의

아래처럼 `orWhere`를 붙이면 관계 조건과 논리적으로 같은 레벨에서 OR로 묶여, 의도와 다른 쿼리가 생성될 수 있습니다:

```php
$user->posts()
        ->where('active', 1)
        ->orWhere('votes', '>=', 100)
        ->get();
```

실제 SQL (내부 연산자 우선순위 문제):

```sql
select *
from posts
where user_id = ? and active = 1 or votes >= 100
```

`or` 조건 때문에 게시글 소유자 제한(`user_id`)이 무력화될 수 있습니다.

이 경우, 논리 그룹으로 묶으세요:

```php
use Illuminate\Database\Eloquent\Builder;

$user->posts()
    ->where(function (Builder $query) {
        return $query->where('active', 1)
            ->orWhere('votes', '>=', 100);
    })
    ->get();
```

생성되는 SQL:

```sql
select *
from posts
where user_id = ? and (active = 1 or votes >= 100)
```

<a name="relationship-methods-vs-dynamic-properties"></a>
### 관계 메서드 vs 동적 속성

추가 제한조건 없이 단순 조회만 필요하면, 관계 메서드 대신 동적 속성으로 접근할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

foreach ($user->posts as $post) {
    // ...
}
```

동적 속성은 지연 로딩(lazy loading)이므로 실제 접근 시점에 DB 쿼리가 실행됩니다.

필요한 관계를 미리 로딩하는 즉시 로딩(eager loading)을 활용하면 쿼리 수를 크게 줄일 수 있습니다.

<a name="querying-relationship-existence"></a>
### 관계 존재 여부 쿼리하기

관계를 가진 레코드만 필터링할 때는 `has` 메서드를 사용합니다.

예: 댓글이 최소 1개 있는 게시글 조회

```php
use App\Models\Post;

// 댓글이 최소 하나 있는 게시글 조회
$posts = Post::has('comments')->get();
```

조건을 더 세밀하게 하려면 연산자와 개수를 지정할 수 있습니다:

```php
// 댓글이 3개 이상인 게시글 조회
$posts = Post::has('comments', '>=', 3)->get();
```

중첩 조건도 가능합니다:

```php
// 이미지가 붙은 댓글이 최소 하나 있는 게시글 조회
$posts = Post::has('comments.images')->get();
```

`whereHas`, `orWhereHas`는 관계 조건 안에서 추가 쿼리 조건을 넣을 때 사용합니다:

```php
use Illuminate\Database\Eloquent\Builder;

// 내용에 'code%'가 포함된 댓글이 있는 게시글 조회
$posts = Post::whereHas('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
})->get();

// 조건에 맞는 댓글이 10개 이상인 게시글 조회
$posts = Post::whereHas('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
}, '>=', 10)->get();
```

> [!WARNING]  
> Eloquent는 현재 다른 데이터베이스 간 관계 존재 여부 쿼리를 지원하지 않습니다. 관계는 같은 DB 내에 있어야 합니다.

<a name="inline-relationship-existence-queries"></a>
#### 간단한 관계 존재 조건 쿼리 (Inline Queries)

단순 조건이 붙은 관계 존재 여부 쿼리는 `whereRelation` 계열 메서드로 간단히 처리할 수 있습니다:

```php
use App\Models\Post;

$posts = Post::whereRelation('comments', 'is_approved', false)->get();
```

비교 연산자도 넣을 수 있습니다:

```php
$posts = Post::whereRelation(
    'comments', 'created_at', '>=', now()->subHour()
)->get();
```

<a name="querying-relationship-absence"></a>
### 관계 부재 쿼리하기 (Querying Relationship Absence)

관계가 없는 레코드를 조회하려면 `doesntHave` 또는 `orDoesntHave` 메서드를 사용합니다:

```php
use App\Models\Post;

// 댓글이 없는 게시글 조회
$posts = Post::doesntHave('comments')->get();
```

추가 조건과 함께 쿼리하려면 `whereDoesntHave`, `orWhereDoesntHave`를 씁니다:

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::whereDoesntHave('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
})->get();
```

중첩 관계에도 적용됩니다:

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::whereDoesntHave('comments.author', function (Builder $query) {
    $query->where('banned', 0);
})->get();
```

<a name="querying-morph-to-relationships"></a>
### Morph To 관계 쿼리하기

"morph to" 관계 존재 여부는 `whereHasMorph`, `whereDoesntHaveMorph`를 사용합니다:

```php
use App\Models\Comment;
use App\Models\Post;
use App\Models\Video;
use Illuminate\Database\Eloquent\Builder;

// 댓글이 Post 또는 Video에 속하지만, 제목이 'code%'인 경우 조회
$comments = Comment::whereHasMorph(
    'commentable',
    [Post::class, Video::class],
    function (Builder $query) {
        $query->where('title', 'like', 'code%');
    }
)->get();

// 제목이 'code%'인 Post에 속하지 않은 댓글 조회
$comments = Comment::whereDoesntHaveMorph(
    'commentable',
    Post::class,
    function (Builder $query) {
        $query->where('title', 'like', 'code%');
    }
)->get();
```

두 번째 클로저 인수로 타입 정보 `$type`을 받을 수 있습니다:

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

특정 부모 모델에 속하는 자식만 조회하려면 `whereMorphedTo`, `whereNotMorphedTo`를 사용합니다:

```php
$comments = Comment::whereMorphedTo('commentable', $post)
    ->orWhereMorphedTo('commentable', $video)
    ->get();
```

<a name="querying-all-morph-to-related-models"></a>
#### 모든 polymorphic 관련 모델 조회

모델 리스트 대신 `'*'` 와일드카드를 넘기면 데이터베이스에서 관련 가능한 모든 다형성 타입을 확인하여 전체 조회합니다:

```php
use Illuminate\Database\Eloquent\Builder;

$comments = Comment::whereHasMorph('commentable', '*', function (Builder $query) {
    $query->where('title', 'like', 'foo%');
})->get();
```

<a name="aggregating-related-models"></a>
## 연관 모델 집계 (Aggregating Related Models)

<a name="counting-related-models"></a>
### 연관 모델 카운트하기

관계된 모델 수를 로딩하지 않고 바로 가져올 때 `withCount` 메서드를 사용합니다.

```php
use App\Models\Post;

$posts = Post::withCount('comments')->get();

foreach ($posts as $post) {
    echo $post->comments_count;
}
```

여러 관계 카운트를 한 번에 하거나 추가 조건도 가능합니다:

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::withCount(['votes', 'comments' => function (Builder $query) {
    $query->where('content', 'like', 'code%');
}])->get();

echo $posts[0]->votes_count;
echo $posts[0]->comments_count;
```

별칭도 지정할 수 있어 동일 관계 여러 조건 카운트를 구분 가능:

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

`loadCount`를 쓰면 이미 불러온 모델에서 관계 수를 로드할 수 있습니다:

```php
$book = Book::first();

$book->loadCount('genres');
```

조건이 필요할 때도 배열 형태로 전달합니다:

```php
$book->loadCount(['reviews' => function (Builder $query) {
    $query->where('rating', 5);
}])
```

<a name="relationship-counting-and-custom-select-statements"></a>
#### `select`와 `withCount` 병행 시 주의

`select`와 함께 쓸 땐 `withCount`를 뒤에 호출하세요:

```php
$posts = Post::select(['title', 'body'])
    ->withCount('comments')
    ->get();
```

<a name="other-aggregate-functions"></a>
### 기타 집계 함수

`withCount` 외에 `withMin`, `withMax`, `withAvg`, `withSum`, `withExists` 메서드가 있으며, 이름 패턴은 `{relation}_{function}_{column}`입니다:

```php
use App\Models\Post;

$posts = Post::withSum('comments', 'votes')->get();

foreach ($posts as $post) {
    echo $post->comments_sum_votes;
}
```

별칭도 지정 가능:

```php
$posts = Post::withSum('comments as total_comments', 'votes')->get();

foreach ($posts as $post) {
    echo $post->total_comments;
}
```

`loadCount`처럼 `loadSum` 등 지연 집계 메서드도 있습니다:

```php
$post = Post::first();

$post->loadSum('comments', 'votes');
```

또한 `select`와 병행 시는 집계 메서드를 `select` 뒤에 호출해야 합니다.

```php
$posts = Post::select(['title', 'body'])
    ->withExists('comments')
    ->get();
```

<a name="counting-related-models-on-morph-to-relationships"></a>
### Morph To 관계 연관 모델 수 카운트하기

`morphTo` 관계에도 관련된 각 모델 타입별로 연관 카운트를 조회할 수 있습니다.

예를 들어, `ActivityFeed` 모델에서 `parentable` morphTo 관계를 통해 `Photo`와 `Post` 모델을 각각 가지고 있고, `Photo`는 `tags`를, `Post`는 `comments`를 가지고 있다면 다음처럼 읽어올 수 있습니다:

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
#### 지연 모프 카운트 로딩

이미 불러온 `ActivityFeed` 모델이 있을 경우 `loadMorphCount` 메서드를 사용해 관계 카운트를 로드할 수 있습니다:

```php
$activities = ActivityFeed::with('parentable')->get();

$activities->loadMorphCount('parentable', [
    Photo::class => ['tags'],
    Post::class => ['comments'],
]);
```

<a name="eager-loading"></a>
## 즉시 로딩 (Eager Loading)

동적 속성으로 관계 모델을 조회할 때는 지연 로딩됩니다. 즉, 처음 접근 시점에 관계 모델 쿼리가 실행됩니다. 반면, 즉시 로딩은 부모 모델 조회 시점에 관계 모델도 미리 불러와 "N+1문제"를 해결해줍니다.

예를 들어, `Book` 모델이 `Author` 모델에 `belongsTo`인 경우:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Book extends Model
{
    /**
     * 이 책의 저자
     */
    public function author(): BelongsTo
    {
        return $this->belongsTo(Author::class);
    }
}
```

모든 책과 저자를 조회하면 다음과 같이 쿼리가 많아집니다:

```php
use App\Models\Book;

$books = Book::all();

foreach ($books as $book) {
    echo $book->author->name;
}
```

이 방식은 `books` 조회 1회 + 책 개수만큼 `authors` 조회가 일어나 `N+1` 문제를 만듭니다.

이 문제는 `with` 메서드로 해결할 수 있습니다:

```php
$books = Book::with('author')->get();

foreach ($books as $book) {
    echo $book->author->name;
}
```

이렇게 하면 단 2쿼리만 실행합니다:

```sql
select * from books

select * from authors where id in (?, ?, ?, ...)
```

<a name="eager-loading-multiple-relationships"></a>
#### 다중 즉시 로딩

여러 관계를 한꺼번에 불러오려면 배열로 넘기면 됩니다:

```php
$books = Book::with(['author', 'publisher'])->get();
```

<a name="nested-eager-loading"></a>
#### 중첩 즉시 로딩

관계의 관계까지 즉시 로딩하려면 "dot" 문법을 사용합니다:

```php
$books = Book::with('author.contacts')->get();
```

또는 중첩 배열로도 표현 가능합니다:

```php
$books = Book::with([
    'author' => [
        'contacts',
        'publisher',
    ],
])->get();
```

<a name="nested-eager-loading-morphto-relationships"></a>
#### `morphTo` 중첩 즉시 로딩

`morphTo` 관계도 `morphWith` 메서드를 통해 관련 엔티티별로 중첩 관계를 즉시 로딩할 수 있습니다.

아래는 `ActivityFeed` 모델의 예시:

```php
<?php

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class ActivityFeed extends Model
{
    /**
     * 액티비티의 부모 모델
     */
    public function parentable(): MorphTo
    {
        return $this->morphTo();
    }
}
```

`Event`, `Photo`, `Post` 모델이 있고, 각각 다른 관계를 가진 상태라면:

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

관계에서 모든 컬럼이 아니라 특정 컬럼만 로딩할 수도 있습니다:

```php
$books = Book::with('author:id,name,book_id')->get();
```

> [!WARNING]  
> 이 경우, 반드시 기본 키(`id`)와 외래 키 컬럼을 포함시켜야 합니다.

<a name="eager-loading-by-default"></a>
#### 기본 즉시 로딩 설정

모델에서 항상 특정 관계를 즉시 로딩하려면 `$with` 프로퍼티를 정의합니다:

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

    public function author(): BelongsTo
    {
        return $this->belongsTo(Author::class);
    }

    public function genre(): BelongsTo
    {
        return $this->belongsTo(Genre::class);
    }
}
```

특정 쿼리에서 `$with`에 정의한 관계를 제외하려면 `without` 메서드를 씁니다:

```php
$books = Book::without('author')->get();
```

모두 무시하고 새로 지정하려면 `withOnly`를 쓸 수 있습니다:

```php
$books = Book::withOnly('genre')->get();
```

<a name="constraining-eager-loads"></a>
### 즉시 로딩 제약 사항 추가하기

즉시 로딩할 관계 쿼리를 특정 조건으로 제한하려면, `with` 메서드에 배열로 관계명과 클로저를 넘기면 됩니다:

```php
use App\Models\User;
use Illuminate\Contracts\Database\Eloquent\Builder;

$users = User::with(['posts' => function (Builder $query) {
    $query->where('title', 'like', '%code%');
}])->get();
```

다른 쿼리 빌더 메서드도 자유롭게 사용 가능합니다:

```php
$users = User::with(['posts' => function (Builder $query) {
    $query->orderBy('created_at', 'desc');
}])->get();
```

<a name="constraining-eager-loading-of-morph-to-relationships"></a>
#### `morphTo` 관계 즉시 로딩 조건 제약 추가

`morphTo` 관계는 부모 타입별로 쿼리를 분리해 실행합니다.

`constrain` 메서드로 각 타입별 쿼리 조건을 지정할 수 있습니다:

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

`Post` 중 `hidden_at`이 null인 게시물, `Video` 중에서 `type`이 `educational`인 동영상만 조회됩니다.

<a name="constraining-eager-loads-with-relationship-existence"></a>
#### 관계 존재 여부 조건과 함께 제약 부여

특정 조건에 맞는 관계가 존재하는 모델만 조회하고 동시에 관계도 즉시 로딩하려면 `withWhereHas`를 씁니다:

```php
use App\Models\User;

$users = User::withWhereHas('posts', function ($query) {
    $query->where('featured', true);
})->get();
```

<a name="lazy-eager-loading"></a>
### 지연 즉시 로딩 (Lazy Eager Loading)

이미 조회한 모델 세트에 관계를 즉시 로딩할 수 있습니다:

```php
use App\Models\Book;

$books = Book::all();

if ($someCondition) {
    $books->load('author', 'publisher');
}
```

추가 쿼리 제약도 배열과 클로저로 줄 수 있습니다:

```php
$author->load(['books' => function (Builder $query) {
    $query->orderBy('published_date', 'asc');
}]);
```

이미 관계가 로드되어 있다면 스킵하는 `loadMissing`도 있습니다:

```php
$book->loadMissing('author');
```

<a name="nested-lazy-eager-loading-morphto"></a>
#### 다형성 지연 즉시 로딩

`morphTo` 관계도 `loadMorph`로 관계별로 지연 로딩하며 각 모델별 중첩 관계도 설정할 수 있습니다:

```php
<?php

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class ActivityFeed extends Model
{
    /**
     * 부모 다형성 관계
     */
    public function parentable(): MorphTo
    {
        return $this->morphTo();
    }
}
```

예:

```php
$activities = ActivityFeed::with('parentable')
    ->get()
    ->loadMorph('parentable', [
        Event::class => ['calendar'],
        Photo::class => ['tags'],
        Post::class => ['author'],
    ]);
```

<a name="preventing-lazy-loading"></a>
### 지연 로딩 방지하기

지연 로딩을 완전히 금지해 성능 문제를 예방할 수 있습니다.

애플리케이션 `AppServiceProvider`의 `boot` 메서드 등에서 다음과 같이 호출합니다:

```php
use Illuminate\Database\Eloquent\Model;

/**
 * 부트스트랩 서비스
 */
public function boot(): void
{
    Model::preventLazyLoading(! $this->app->isProduction());
}
```

지연 로딩 시 `Illuminate\Database\LazyLoadingViolationException` 예외가 발생합니다.

처리 방식을 직접 지정하려면 `handleLazyLoadingViolationUsing`을 사용해 이벤트처럼 기록만 하도록 바꿀 수도 있습니다:

```php
Model::handleLazyLoadingViolationUsing(function (Model $model, string $relation) {
    $class = $model::class;

    info("Attempted to lazy load [{$relation}] on model [{$class}].");
});
```

<a name="inserting-and-updating-related-models"></a>
## 연관 모델 삽입 및 갱신 (Inserting and Updating Related Models)

<a name="the-save-method"></a>
### `save` 메서드

관계에 새로운 모델을 추가할 때는 외래 키를 직접 설정하지 않고도 관계의 `save` 메서드를 쓰면 됩니다.

예를 들어 게시글에 새 댓글을 추가하려면:

```php
use App\Models\Comment;
use App\Models\Post;

$comment = new Comment(['message' => 'A new comment.']);

$post = Post::find(1);

$post->comments()->save($comment);
```

메서드 형태로 호출해야 하며, 생성 후 외래 키가 자동으로 세팅됩니다.

여러 모델을 한번에 저장하려면 `saveMany`를 씁니다:

```php
$post = Post::find(1);

$post->comments()->saveMany([
    new Comment(['message' => 'A new comment.']),
    new Comment(['message' => 'Another new comment.']),
]);
```

하지만 저장 후에 이미 메모리에 로드된 관계에 새 모델은 포함되지 않습니다. 다시 접근하려면 `refresh`를 호출하세요:

```php
$post->comments()->save($comment);

$post->refresh();

// 새로운 댓글도 포함됩니다.
$post->comments;
```

<a name="the-push-method"></a>
#### 재귀 저장 (`push`)

모델과 연관된 모든 모델(관계까지 포함)을 함께 저장하려면 `push`를 사용하세요:

```php
$post = Post::find(1);

$post->comments[0]->message = 'Message';
$post->comments[0]->author->name = 'Author Name';

$post->push();
```

이벤트 발생 없이 저장하려면 `pushQuietly` 사용:

```php
$post->pushQuietly();
```

<a name="the-create-method"></a>
### `create` 메서드

`save`와 달리 `create`는 배열로 속성을 받아 새 모델을 생성 및 저장한 뒤 반환합니다:

```php
use App\Models\Post;

$post = Post::find(1);

$comment = $post->comments()->create([
    'message' => 'A new comment.',
]);
```

`createMany`로 여러 모델도 한번에 생성 가능:

```php
$post = Post::find(1);

$post->comments()->createMany([
    ['message' => 'A new comment.'],
    ['message' => 'Another new comment.'],
]);
```

이벤트 없이 생성하는 `createQuietly`, `createManyQuietly`도 제공합니다:

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

이 외에도 `findOrNew`, `firstOrNew`, `firstOrCreate`, `updateOrCreate` 같은 upsert 메서드들도 사용할 수 있습니다.

> [!NOTE]  
> `create` 사용 시 [대량 할당(Mass Assignment)](/docs/11.x/eloquent#mass-assignment) 규칙을 반드시 검토하세요.

<a name="updating-belongs-to-relationships"></a>
### Belongs To 관계 업데이트

자식 모델에 새 부모를 할당하려면 `associate` 메서드를 사용합니다:

```php
use App\Models\Account;

$account = Account::find(10);

$user->account()->associate($account);

$user->save();
```

부모 모델과 연결을 끊으려면 `dissociate`를 사용해 외래 키를 `null`로 만듭니다:

```php
$user->account()->dissociate();

$user->save();
```

<a name="updating-many-to-many-relationships"></a>
### 다대다 관계 업데이트

<a name="attaching-detaching"></a>
#### 연결 / 해제

`attach` 메서드로 중간 테이블에 연결 레코드를 추가합니다:

```php
use App\Models\User;

$user = User::find(1);

$user->roles()->attach($roleId);
```

추가 데이터를 함께 넣을 수도 있습니다:

```php
$user->roles()->attach($roleId, ['expires' => $expires]);
```

관계 해제는 `detach` 기준입니다:

```php
// 단일 역할 해제
$user->roles()->detach($roleId);

// 모두 해제
$user->roles()->detach();
```

각각 배열로도 전달 가능:

```php
$user = User::find(1);

$user->roles()->detach([1, 2, 3]);

$user->roles()->attach([
    1 => ['expires' => $expires],
    2 => ['expires' => $expires],
]);
```

<a name="syncing-associations"></a>
#### 동기화(sync)

`sync`는 지정한 ID 배열과 일치하도록 중간 테이블을 맞춥니다. 지정하지 않은 ID는 삭제됩니다:

```php
$user->roles()->sync([1, 2, 3]);
```

부가 정보와 함께도 가능:

```php
$user->roles()->sync([1 => ['expires' => true], 2, 3]);
```

모든 대상에 같은 값 넣으려면 `syncWithPivotValues` 메서드를 사용:

```php
$user->roles()->syncWithPivotValues([1, 2, 3], ['active' => true]);
```

기존 연결을 해제하지 않고 추가만 하고 싶으면 `syncWithoutDetaching` 사용:

```php
$user->roles()->syncWithoutDetaching([1, 2, 3]);
```

<a name="toggling-associations"></a>
#### 토글(toggle)

`toggle`은 주어진 ID가 이미 연결돼 있으면 해제, 없으면 연결합니다:

```php
$user->roles()->toggle([1, 2, 3]);
```

추가 데이터와 함께도 사용 가능:

```php
$user->roles()->toggle([
    1 => ['expires' => true],
    2 => ['expires' => true],
]);
```

<a name="updating-a-record-on-the-intermediate-table"></a>
#### 중간 테이블 기존 레코드 갱신

`updateExistingPivot` 메서드는 중간 테이블 특정 레코드의 컬럼 데이터를 업데이트합니다:

```php
$user = User::find(1);

$user->roles()->updateExistingPivot($roleId, [
    'active' => false,
]);
```

<a name="touching-parent-timestamps"></a>
## 상위 모델 타임스탬프 갱신 (Touching Parent Timestamps)

`Comment` 같은 자식 모델이 업데이트될 때, 상위 `Post` 모델의 `updated_at`도 함께 갱신하고 싶다면, 자식 모델에 `$touches` 속성 배열을 정의하세요:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Comment extends Model
{
    /**
     * 업데이트 시 함께 타임스탬프를 갱신할 관계명 목록
     *
     * @var array
     */
    protected $touches = ['post'];

    /**
     * 댓글이 속한 게시글
     */
    public function post(): BelongsTo
    {
        return $this->belongsTo(Post::class);
    }
}
```

> [!WARNING]  
> `touches` 속성에 지정한 부모 모델의 `updated_at` 필드는 자식 모델을 `save()` 메서드 등 Eloquent 방식으로 업데이트할 때에만 갱신됩니다.