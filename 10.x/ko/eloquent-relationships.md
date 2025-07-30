# Eloquent: 관계 (Eloquent: Relationships)

- [소개](#introduction)
- [관계 정의하기](#defining-relationships)
    - [일대일 (One to One)](#one-to-one)
    - [일대다 (One to Many)](#one-to-many)
    - [일대다 (역방향) / belongsTo](#one-to-many-inverse)
    - [hasOne of Many](#has-one-of-many)
    - [hasOne Through](#has-one-through)
    - [hasMany Through](#has-many-through)
- [다대다 관계 (Many to Many)](#many-to-many)
    - [중간 테이블 컬럼 조회하기](#retrieving-intermediate-table-columns)
    - [중간 테이블 컬럼을 통한 쿼리 필터링](#filtering-queries-via-intermediate-table-columns)
    - [중간 테이블 컬럼을 통한 쿼리 정렬](#ordering-queries-via-intermediate-table-columns)
    - [커스텀 중간 테이블 모델 정의하기](#defining-custom-intermediate-table-models)
- [다형성 관계 (Polymorphic Relationships)](#polymorphic-relationships)
    - [일대일 (Polymorphic)](#one-to-one-polymorphic-relations)
    - [일대다 (Polymorphic)](#one-to-many-polymorphic-relations)
    - [One of Many (Polymorphic)](#one-of-many-polymorphic-relations)
    - [다대다 (Polymorphic)](#many-to-many-polymorphic-relations)
    - [커스텀 다형성 타입](#custom-polymorphic-types)
- [동적 관계 (Dynamic Relationships)](#dynamic-relationships)
- [관계 쿼리하기 (Querying Relations)](#querying-relations)
    - [관계 메서드와 동적 속성 비교](#relationship-methods-vs-dynamic-properties)
    - [관계 존재 쿼리하기](#querying-relationship-existence)
    - [관계 부재 쿼리하기](#querying-relationship-absence)
    - [morphTo 관계 쿼리하기](#querying-morph-to-relationships)
- [관련 모델 집계 (Aggregating Related Models)](#aggregating-related-models)
    - [관련 모델 수 세기](#counting-related-models)
    - [기타 집계 함수](#other-aggregate-functions)
    - [morphTo 관계에서의 관련 모델 수 세기](#counting-related-models-on-morph-to-relationships)
- [Eager Loading](#eager-loading)
    - [Eager Load 제한하기](#constraining-eager-loads)
    - [지연 Eager Loading (Lazy Eager Loading)](#lazy-eager-loading)
    - [지연 로딩 방지하기](#preventing-lazy-loading)
- [관련 모델 삽입 및 갱신](#inserting-and-updating-related-models)
    - [`save` 메서드](#the-save-method)
    - [`create` 메서드](#the-create-method)
    - [belongsTo 관계 갱신](#updating-belongs-to-relationships)
    - [다대다 관계 갱신](#updating-many-to-many-relationships)
- [부모 타임스탬프 갱신 (Touching Parent Timestamps)](#touching-parent-timestamps)

<a name="introduction"></a>
## 소개 (Introduction)

데이터베이스 테이블은 서로 연관된 경우가 많습니다. 예를 들어, 블로그 게시글에는 여러 개의 댓글이 있을 수 있고, 주문 내역은 주문한 사용자와 연관될 수 있습니다. Eloquent는 이런 관계를 쉽게 관리하고 활용할 수 있도록 도와주며, 다양한 일반적인 관계 유형을 지원합니다:

<div class="content-list" markdown="1">

- [일대일 (One To One)](#one-to-one)
- [일대다 (One To Many)](#one-to-many)
- [다대다 (Many To Many)](#many-to-many)
- [hasOne Through](#has-one-through)
- [hasMany Through](#has-many-through)
- [일대일 (다형성)](#one-to-one-polymorphic-relations)
- [일대다 (다형성)](#one-to-many-polymorphic-relations)
- [다대다 (다형성)](#many-to-many-polymorphic-relations)

</div>

<a name="defining-relationships"></a>
## 관계 정의하기 (Defining Relationships)

Eloquent 관계는 Eloquent 모델 클래스 내의 메서드로 정의합니다. 관계도 [쿼리 빌더](/docs/10.x/queries) 역할을 하기 때문에, 메서드로 정의하면 체이닝과 추가 조건 설정을 할 수 있어 매우 강력합니다. 예를 들어, `posts` 관계에 추가 조건을 붙일 수 있습니다:

```
$user->posts()->where('active', 1)->get();
```

이제 각 관계 유형을 어떻게 정의하는지 자세히 살펴보겠습니다.

<a name="one-to-one"></a>
### 일대일 (One to One)

일대일 관계는 가장 기본적인 관계입니다. 예를 들어 `User` 모델과 `Phone` 모델이 1:1 연결되어 있을 수 있습니다. 이 경우, `User` 모델에 `phone` 메서드를 추가하며 메서드는 `hasOne` 메서드를 호출하여 결과를 반환해야 합니다. `hasOne`은 `Illuminate\Database\Eloquent\Model` 베이스 클래스에서 제공됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasOne;

class User extends Model
{
    /**
     * 사용자와 연결된 전화번호를 반환합니다.
     */
    public function phone(): HasOne
    {
        return $this->hasOne(Phone::class);
    }
}
```

`hasOne` 메서드 첫 번째 인수는 연관된 모델 클래스명입니다. 관계가 정의되면 Eloquent의 동적 속성을 통해 관련 레코드를 가져올 수 있습니다. 동적 속성은 관계 메서드를 마치 모델에 정의된 속성처럼 접근할 수 있게 해줍니다:

```php
$phone = User::find(1)->phone;
```

Eloquent는 부모 모델 이름을 바탕으로 외래 키를 자동으로 판단합니다. 여기서는 `Phone` 모델에 `user_id` 컬럼이 있다고 가정합니다. 기본 설정을 변경하고 싶다면 `hasOne` 두 번째 인자로 외래 키 이름을 넘길 수 있습니다:

```php
return $this->hasOne(Phone::class, 'foreign_key');
```

추가로 Eloquent는 외래 키가 부모 모델의 기본 키(`id`)와 일치하는 값을 가져야 한다고 가정합니다. 다른 컬럼을 기본 키로 사용하고 싶다면 세 번째 인자로 로컬 키를 넘길 수 있습니다:

```php
return $this->hasOne(Phone::class, 'foreign_key', 'local_key');
```

<a name="one-to-one-defining-the-inverse-of-the-relationship"></a>
#### 관계의 역방향 정의하기

`User` 모델에서 `Phone` 모델에 접근할 수 있으니, 이제 `Phone` 모델에서 해당 전화번호의 소유자인 `User` 모델에 접근하는 역방향 관계를 정의해봅시다. `hasOne`의 역방향은 `belongsTo` 메서드를 사용해 정의합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Phone extends Model
{
    /**
     * 이 전화번호의 소유자(사용자)를 반환합니다.
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }
}
```

`user` 메서드를 호출하면, Eloquent는 `Phone` 모델의 `user_id` 값에 맞는 `User` 모델의 `id` 컬럼 값을 찾아 반환합니다.

외래 키 이름은 관계 메서드 이름에 `_id`를 붙여서 찾습니다. 이 예에서는 `user_id` 컬럼을 가정합니다. 만약 외래 키가 다르다면 `belongsTo` 두 번째 인자로 커스텀 외래 키를 지정할 수 있습니다:

```php
/**
 * 전화번호의 소유자를 반환합니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class, 'foreign_key');
}
```

부모 모델이 `id`가 아닌 다른 컬럼을 기본 키로 사용하거나, 다른 컬럼으로 모델을 찾고 싶다면 세 번째 인자로 부모 테이블의 키를 지정할 수 있습니다:

```php
/**
 * 전화번호의 소유자를 반환합니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class, 'foreign_key', 'owner_key');
}
```

<a name="one-to-many"></a>
### 일대다 (One to Many)

일대다 관계는 한 부모 모델이 다수의 자식 모델을 갖는 경우 정의합니다. 예를 들어 한 블로그 게시글에 무한한 댓글들이 달릴 수 있습니다. 정의 방법은 다른 관계들과 동일하게 메서드로 작성합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Post extends Model
{
    /**
     * 게시글에 달린 댓글들을 반환합니다.
     */
    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class);
    }
}
```

Eloquent는 자식 모델의 외래 키 컬럼명을 자동으로 추론합니다. 기본 규칙인 부모 모델 이름을 snake_case로 변환한 뒤 `_id`를 붙여서, 여기서는 `post_id`라고 간주합니다.

이 관계 메서드가 정의되면 동적 속성으로 관련 댓글 컬렉션을 조회할 수 있습니다:

```php
use App\Models\Post;

$comments = Post::find(1)->comments;

foreach ($comments as $comment) {
    // ...
}
```

관계는 쿼리 빌더 역할도 하므로, 메서드를 호출해 쿼리에 추가 조건을 붙일 수도 있습니다:

```php
$comment = Post::find(1)->comments()
                    ->where('title', 'foo')
                    ->first();
```

`hasOne`과 마찬가지로 외래 키와 로컬 키는 추가 인자를 통해 오버라이딩 할 수 있습니다:

```php
return $this->hasMany(Comment::class, 'foreign_key');

return $this->hasMany(Comment::class, 'foreign_key', 'local_key');
```

<a name="one-to-many-inverse"></a>
### 일대다 (역방향) / belongsTo

게시글의 댓글들을 가져올 수 있으니, 이제 댓글에서 소유 게시글에 접근하는 역관계를 정의해봅시다. 자식 모델에서 `belongsTo` 메서드를 호출하는 관계 메서드를 만듭니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Comment extends Model
{
    /**
     * 댓글이 속한 게시글을 반환합니다.
     */
    public function post(): BelongsTo
    {
        return $this->belongsTo(Post::class);
    }
}
```

정의 후에는 동적 속성으로 부모 게시글에 접근할 수 있습니다:

```php
use App\Models\Comment;

$comment = Comment::find(1);

return $comment->post->title;
```

기본 외래 키는 관계 메서드 이름에 부모 모델 기본 키명을 결합해 만듭니다. 여기서는 `post_id`를 기본으로 간주합니다.

외래 키가 다르다면 `belongsTo` 두 번째 인자로 커스텀 외래 키를 전달할 수 있습니다:

```php
/**
 * 댓글의 게시글을 반환합니다.
 */
public function post(): BelongsTo
{
    return $this->belongsTo(Post::class, 'foreign_key');
}
```

부모 모델이 `id`가 아닌 다른 키를 사용하거나, 다르게 찾고 싶다면 세 번째 인자에 부모 모델의 키 명을 넘기시면 됩니다:

```php
/**
 * 댓글의 게시글을 반환합니다.
 */
public function post(): BelongsTo
{
    return $this->belongsTo(Post::class, 'foreign_key', 'owner_key');
}
```

<a name="default-models"></a>
#### 기본 모델(Default Models)

`belongsTo`, `hasOne`, `hasOneThrough`, `morphOne` 관계는 관계가 `null`일 때 반환할 기본 모델을 지정할 수 있습니다. 이는 [Null Object 패턴](https://en.wikipedia.org/wiki/Null_Object_pattern)이며, 조건문 없이 기본 객체를 다룰 수 있어 편리합니다. 예를 들어, `Post` 모델에 연결된 `user` 관계가 없으면 빈 `App\Models\User` 모델을 반환하도록 할 수 있습니다:

```php
/**
 * 게시글 작성자를 반환합니다.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault();
}
```

`withDefault`에 배열이나 클로저를 넘겨 기본 모델 속성을 지정할 수도 있습니다:

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
#### belongsTo 관계 쿼리하기

belongsTo 관계의 자식 모델을 쿼리할 때 직접 `where` 구문을 만들어도 되지만, `whereBelongsTo` 메서드를 쓰는 편이 편리합니다. 이 메서드는 모델과 올바른 외래 키를 자동으로 매칭해줍니다:

```php
use App\Models\Post;

$posts = Post::whereBelongsTo($user)->get();
```

컬렉션 인스턴스를 넘기면 컬렉션 내 부모 모델에 속한 자식을 모두 조회합니다:

```php
$users = User::where('vip', true)->get();

$posts = Post::whereBelongsTo($users)->get();
```

모델 기본 관계명을 수동으로 지정하려면 두 번째 인자로 관계명을 넘기면 됩니다:

```php
$posts = Post::whereBelongsTo($user, 'author')->get();
```

<a name="has-one-of-many"></a>
### Has One of Many

때때로 여러 자식 모델 중에서 가장 최신(latest) 또는 가장 오래된(oldest) 모델 하나만 편하게 조회하고 싶을 수 있습니다. 예를 들어 한 `User`가 여러 `Order`를 가질 때 가장 최근 주문만 접근하는 경우입니다. `hasOne` 관계에 `ofMany` 메서드를 결합하여 만들 수 있습니다:

```php
/**
 * 사용자의 최신 주문을 반환합니다.
 */
public function latestOrder(): HasOne
{
    return $this->hasOne(Order::class)->latestOfMany();
}
```

가장 오래된 주문을 조회하는 메서드도 마찬가지로 정의할 수 있습니다:

```php
/**
 * 사용자의 가장 오래된 주문을 반환합니다.
 */
public function oldestOrder(): HasOne
{
    return $this->hasOne(Order::class)->oldestOfMany();
}
```

기본적으로 `latestOfMany`와 `oldestOfMany`는 기본 키 컬럼을 정렬 기준으로 사용합니다. 하지만 다른 정렬 기준을 사용할 수도 있습니다.

예를 들어 `ofMany` 메서드의 첫 번째 인수로 정렬 대상 컬럼명, 두 번째 인수로 적용할 집계 함수(`min`, `max`)를 넘겨서 가장 비싼 주문을 가져올 수도 있습니다:

```php
/**
 * 사용자의 가장 큰 금액 주문을 반환합니다.
 */
public function largestOrder(): HasOne
{
    return $this->hasOne(Order::class)->ofMany('price', 'max');
}
```

> [!WARNING]  
> PostgreSQL은 UUID 컬럼에 대해 `MAX` 함수를 지원하지 않기 때문에, PostgreSQL UUID 컬럼과 함께 one-of-many 관계를 사용하는 것은 현재 불가능합니다.

<a name="converting-many-relationships-to-has-one-relationships"></a>
#### "다대다" 관계를 "일대일" 관계로 전환하기

`latestOfMany`, `oldestOfMany`, `ofMany`로 단일 모델을 조회할 때, 이미 같은 모델에 대해 `hasMany` 관계가 정의된 경우가 많습니다. 이 때 `one` 메서드를 호출하여 `hasMany` 관계를 `hasOne` 형태로 쉽게 변환할 수 있습니다:

```php
/**
 * 사용자의 모든 주문을 반환합니다.
 */
public function orders(): HasMany
{
    return $this->hasMany(Order::class);
}

/**
 * 사용자의 가장 큰 주문을 반환합니다.
 */
public function largestOrder(): HasOne
{
    return $this->orders()->one()->ofMany('price', 'max');
}
```

<a name="advanced-has-one-of-many-relationships"></a>
#### 고급 Has One of Many 관계

좀 더 복잡한 조건으로도 "has one of many" 관계를 만들 수 있습니다. 예를 들어 `Product` 모델은 여러 `Price` 모델과 관련될 수 있으며, `published_at` 컬럼을 통해 미래 시점에 발행될 가격도 설정할 수 있다고 합시다.

이 경우, 미래가 아닌(현재 시점 이전) 최신 발행 가격을 가져와야 하고, 만약 발행일자가 같으면 가장 큰 ID를 가진 가격을 우선으로 삼아야 합니다. 이를 위해 `ofMany` 메서드에 정렬 대상 컬럼 배열과 조건 추가용 클로저를 함께 넘깁니다:

```php
/**
 * 현재 적용 중인 상품 가격을 반환합니다.
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

"has-one-through" 관계는 1:1 관계이지만, 세 번째 중간 모델을 통해 연결된 관계를 의미합니다.

예를 들어, 차량 정비소 앱에서 각 `Mechanic`(정비공) 모델은 여러 `Car` 모델과, 각 `Car`는 한 `Owner`(차량 소유자) 모델과 관련되었다고 합시다. 직접적으로 `Mechanic`과 `Owner`는 연결되어 있지 않아도, `Car`를 통해 소유자 모델에 접근 가능합니다.

다음은 이 관계를 위한 테이블 구조 예시입니다:

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

`Mechanic` 모델에 관계를 정의합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasOneThrough;

class Mechanic extends Model
{
    /**
     * 자동차의 소유자를 반환합니다.
     */
    public function carOwner(): HasOneThrough
    {
        return $this->hasOneThrough(Owner::class, Car::class);
    }
}
```

`hasOneThrough` 첫 번째 인자는 최종 모델명, 두 번째 인자는 중간 모델명입니다.

모든 관련 관계가 이미 모델에 선언되어 있다면, `through` 메서드를 사용해 다음처럼 유창하게 정의할 수 있습니다:

```php
// 문자열로 지정하는 방법
return $this->through('cars')->has('owner');

// 동적 메서드 사용
return $this->throughCars()->hasOwner();
```

<a name="has-one-through-key-conventions"></a>
#### 키 규칙

관계 쿼리는 일반적인 Eloquent 외래 키 규칙을 따릅니다. 커스터마이징하려면 `hasOneThrough` 메서드의 세 번째, 네 번째 인자에 중간 및 최종 모델의 외래 키명을 지정합니다. 다섯 번째, 여섯 번째 인자는 각각 로컬 키와 중간 모델의 로컬 키입니다:

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
            'id'  // cars 테이블의 로컬 키
        );
    }
}
```

참고: 앞서 설명한 대로 이미 정의된 관계가 있으면 `through` 메서드를 이용해 쉽게 관계를 정의할 수 있습니다.

<a name="has-many-through"></a>
### Has Many Through

"has-many-through" 관계는 중간 모델을 거쳐 멀리 떨어진 관계의 복수 모델을 편리하게 조회합니다.

예를 들어, `Project` 모델에는 `Environment` 모델들이 있고, 각 `Environment`에는 `Deployment` 모델들이 있다면, 프로젝트는 여러 배포(Deployments)를 간접적으로 가집니다.

표 구조는 다음과 같습니다:

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

`Project` 모델에 관계를 정의합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasManyThrough;

class Project extends Model
{
    /**
     * 프로젝트의 모든 배포 기록을 반환합니다.
     */
    public function deployments(): HasManyThrough
    {
        return $this->hasManyThrough(Deployment::class, Environment::class);
    }
}
```

`hasManyThrough` 첫 번째 인자는 최종 모델명, 두 번째 인자는 중간 모델명입니다.

역시 기존 관계가 이미 정의된 경우, `through` 메서드를 이용해 쉽게 정의할 수 있습니다:

```php
// 문자열로 지정
return $this->through('environments')->has('deployments');

// 동적 메서드 사용
return $this->throughEnvironments()->hasDeployments();
```

`deployments` 테이블에는 `project_id`가 없으나, `environment` 테이블을 통해 간접적 조회가 가능해집니다.

<a name="has-many-through-key-conventions"></a>
#### 키 규칙

기본적인 외래 키 규칙이 사용되며, 커스텀하려면 `hasManyThrough` 메서드의 추가 인자를 사용합니다:

```php
class Project extends Model
{
    public function deployments(): HasManyThrough
    {
        return $this->hasManyThrough(
            Deployment::class,
            Environment::class,
            'project_id', // environments 테이블의 외래 키
            'environment_id', // deployments 테이블의 외래 키
            'id', // projects 테이블의 로컬 키
            'id' // environments 테이블의 로컬 키
        );
    }
}
```

기존 관계를 활용하는 `through` 메서드 방식도 사용할 수 있습니다.

---

<a name="many-to-many"></a>
## 다대다 관계 (Many to Many Relationships)

다대다 관계는 `hasOne`이나 `hasMany`보다 약간 복잡합니다. 예를 들어, `User`와 `Role` 모델이 있을 때, 한 사용자가 여러 역할(roles)을 갖고, 하나의 역할 또한 여러 사용자에게 할당될 수 있습니다.

<a name="many-to-many-table-structure"></a>
#### 테이블 구조

세 개의 테이블이 필요합니다: `users`, `roles`, `role_user` (중간 테이블). `role_user`는 연관된 모델 이름을 알파벳 순서로 합친 이름입니다. 이 테이블에 `user_id`와 `role_id` 컬럼이 있습니다.

중요: 역할이 여러 사용자에 속할 수 있으므로 `roles` 테이블에 `user_id`를 직접 넣으면 안 됩니다.

예시:

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

관계 메서드는 `belongsToMany` 메서드로 정의합니다. 다음은 `User` 모델에서 `roles` 관계를 정의한 예시입니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class User extends Model
{
    /**
     * 사용자에게 할당된 역할들입니다.
     */
    public function roles(): BelongsToMany
    {
        return $this->belongsToMany(Role::class);
    }
}
```

관계가 정의되면 동적 속성으로 역할을 조회할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

foreach ($user->roles as $role) {
    // ...
}
```

쿼리 빌더도 지원하므로, 조건을 붙여 조회할 수 있습니다:

```php
$roles = User::find(1)->roles()->orderBy('name')->get();
```

관계 중간 테이블명은 기본적으로 관련 모델명 알파벳 순서로 정해집니다. 변경할 때는 `belongsToMany` 두 번째 인자로 테이블명을 지정하세요:

```php
return $this->belongsToMany(Role::class, 'role_user');
```

외래 키 컬럼도 세 번째, 네 번째 인자로 커스텀할 수 있습니다:

```php
return $this->belongsToMany(Role::class, 'role_user', 'user_id', 'role_id');
```

<a name="many-to-many-defining-the-inverse-of-the-relationship"></a>
#### 관계 역방향 정의하기

다대다 관계의 역방향도 `belongsToMany`로 정의합니다. `Role` 모델에서 `users` 관계를 다음과 같이 정의할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class Role extends Model
{
    /**
     * 역할에 속한 사용자들입니다.
     */
    public function users(): BelongsToMany
    {
        return $this->belongsToMany(User::class);
    }
}
```

<a name="retrieving-intermediate-table-columns"></a>
### 중간 테이블 컬럼 조회하기

많은 경우 다대다 관계의 중간 테이블에 추가 열이 있을 수 있습니다. 해당 열 데이터를 조회하려면 관계를 정의할 때 `withPivot` 메서드를 사용해 중간 테이블의 속성을 명시해줘야 합니다:

```php
return $this->belongsToMany(Role::class)->withPivot('active', 'created_by');
```

중간 테이블에 `created_at`, `updated_at` 타임스탬프가 있고 자동으로 관리하고 싶다면 `withTimestamps`를 호출하세요:

```php
return $this->belongsToMany(Role::class)->withTimestamps();
```

> [!WARNING]  
> 자동 관리되는 타임스탬프를 사용할 때는 중간 테이블에 `created_at`과 `updated_at` 컬럼이 반드시 존재해야 합니다.

<a name="customizing-the-pivot-attribute-name"></a>
#### `pivot` 속성명 변경하기

중간 테이블 데이터를 담는 기본 모델 속성은 `pivot`입니다. 하지만, 의미를 명확히 하기 위해 이름을 바꿀 수 있습니다.

예를 들어, 사용자가 팟캐스트 구독하는 관계라면 `pivot` 대신 `subscription`이라 이름 붙일 수 있습니다:

```php
return $this->belongsToMany(Podcast::class)
                ->as('subscription')
                ->withTimestamps();
```

변경 후에는 다음처럼 접근할 수 있습니다:

```php
$users = User::with('podcasts')->get();

foreach ($users->flatMap->podcasts as $podcast) {
    echo $podcast->subscription->created_at;
}
```

<a name="filtering-queries-via-intermediate-table-columns"></a>
### 중간 테이블 컬럼을 통한 쿼리 필터링

`wherePivot`, `wherePivotIn`, `wherePivotNotIn`, `wherePivotBetween`, `wherePivotNotBetween`, `wherePivotNull`, `wherePivotNotNull` 메서드를 써서 중간 테이블 컬럼 조건을 쿼리에 추가할 수 있습니다:

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

<a name="ordering-queries-via-intermediate-table-columns"></a>
### 중간 테이블 컬럼을 통한 쿼리 정렬(ordering)

`orderByPivot` 메서드로 중간 테이블 컬럼을 기준으로 정렬할 수 있습니다:

```php
return $this->belongsToMany(Badge::class)
                ->where('rank', 'gold')
                ->orderByPivot('created_at', 'desc');
```

<a name="defining-custom-intermediate-table-models"></a>
### 커스텀 중간 테이블 모델 정의하기

기본 `pivot` 모델 대신 커스텀 모델을 사용하고 싶다면, `using` 메서드를 호출해 커스텀 피벗 모델 클래스를 지정하면 됩니다.

커스텀 다대다 피벗 모델은 `Illuminate\Database\Eloquent\Relations\Pivot` 클래스를 상속해야 하며, 다형성 피벗 모델은 `MorphPivot`을 상속합니다.

`Role` 모델에서 커스텀 피벗 모델을 사용하는 예:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class Role extends Model
{
    /**
     * 역할에 속한 사용자들입니다.
     */
    public function users(): BelongsToMany
    {
        return $this->belongsToMany(User::class)->using(RoleUser::class);
    }
}
```

`RoleUser` 피벗 모델 정의 예시:

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
> 피벗 모델에서 `SoftDeletes` 트레이트를 사용할 수 없습니다. 피벗에서 소프트 삭제를 원한다면 일반 Eloquent 모델로 전환해야 합니다.

<a name="custom-pivot-models-and-incrementing-ids"></a>
#### 커스텀 피벗 모델과 자동 증가 ID

커스텀 피벗 모델이 자동 증가하는 기본 키를 갖는다면, 다음과 같이 클래스에 `$incrementing` 속성을 `true`로 지정해야 합니다:

```php
/**
 * ID가 자동 증가하는지 여부입니다.
 *
 * @var bool
 */
public $incrementing = true;
```

---

<a name="polymorphic-relationships"></a>
## 다형성 관계 (Polymorphic Relationships)

다형성 관계는 자식 모델이 여러 종류의 모델에 속할 수 있는 관계를 의미합니다. 예를 들어, `Comment` 모델이 `Post`와 `Video` 모델에 모두 관련될 수 있습니다.

<a name="one-to-one-polymorphic-relations"></a>
### 일대일 (다형성) (One to One Polymorphic)

<a name="one-to-one-polymorphic-table-structure"></a>
#### 테이블 구조

일대일 다형성 관계는 일반 일대일과 유사하지만, 자식 모델이 여러 모델 유형에 속할 수 있습니다.

예: `Post`와 `User` 모델이 `Image` 모델과 다형성 일대일 관계를 공유.

테이블 구조 예시:

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

`images` 테이블의 `imageable_id` 컬럼은 부모 모델의 ID를, `imageable_type` 컬럼은 부모 모델 클래스명을 저장합니다 (예: `App\Models\Post` 또는 `App\Models\User`).

<a name="one-to-one-polymorphic-model-structure"></a>
#### 모델 정의

다형성 관계 모델 정의 예:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class Image extends Model
{
    /**
     * 다형성 부모 모델(Post 또는 User 등)을 반환합니다.
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
     * 게시글 이미지 반환
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
     * 사용자 이미지 반환
     */
    public function image(): MorphOne
    {
        return $this->morphOne(Image::class, 'imageable');
    }
}
```

<a name="one-to-one-polymorphic-retrieving-the-relationship"></a>
#### 관계 조회

정의 후, 예를 들어 게시글의 이미지를 조회하려면 다음과 같이 합니다:

```php
use App\Models\Post;

$post = Post::find(1);

$image = $post->image;
```

다형성 자식 모델의 부모는 `morphTo` 관계명으로 동적 속성을 통해 접근합니다:

```php
use App\Models\Image;

$image = Image::find(1);

$imageable = $image->imageable;
```

`imageable` 속성은 소유자가 `Post`인지 `User`인지에 따라 해당 모델 인스턴스를 반환합니다.

<a name="morph-one-to-one-key-conventions"></a>
#### 키 규칙

필요하면 다형성 id와 type 컬럼명을 지정할 수 있습니다. 관계 메서드 이름은 첫 인자로 항상 넘겨야 하며, 보통 메서드명(`__FUNCTION__`)을 사용합니다:

```php
/**
 * 이미지가 소속된 모델을 반환합니다.
 */
public function imageable(): MorphTo
{
    return $this->morphTo(__FUNCTION__, 'imageable_type', 'imageable_id');
}
```

<a name="one-to-many-polymorphic-relations"></a>
### 일대다 (다형성) (One to Many Polymorphic)

<a name="one-to-many-polymorphic-table-structure"></a>
#### 테이블 구조

일대다 다형성은 일반 일대다와 유사하나, 자식이 여러 부모 타입에 속할 수 있습니다.

예: 사용자들이 `Post`와 `Video` 모두에 댓글을 달 수 있어서 `comments` 테이블 하나로 관리.

테이블 구조 예:

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
     * 댓글의 부모(게시글 또는 비디오)를 반환합니다.
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
     * 게시글의 모든 댓글을 반환합니다.
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
#### 관계 조회

동적 속성으로 댓글들을 조회:

```php
use App\Models\Post;

$post = Post::find(1);

foreach ($post->comments as $comment) {
    // ...
}
```

댓글의 부모 모델은 `commentable` 속성으로 조회:

```php
use App\Models\Comment;

$comment = Comment::find(1);

$commentable = $comment->commentable;
```

`commentable`은 댓글이 속한 `Post` 또는 `Video` 인스턴스를 반환합니다.

<a name="one-of-many-polymorphic-relations"></a>
### One of Many (다형성)

한 모델이 여러 자식 모델과 관계를 가지면서, 최신 혹은 가장 오래된 한 개만 편하게 조회하고 싶은 경우 `morphOne` 관계에 `ofMany`(예: `latestOfMany`)를 결합합니다:

```php
/**
 * 사용자의 최신 이미지 반환
 */
public function latestImage(): MorphOne
{
    return $this->morphOne(Image::class, 'imageable')->latestOfMany();
}
```

가장 오래된 이미지도 유사하게:

```php
/**
 * 사용자의 가장 오래된 이미지 반환
 */
public function oldestImage(): MorphOne
{
    return $this->morphOne(Image::class, 'imageable')->oldestOfMany();
}
```

다른 정렬 기준을 쓰고 싶다면 `ofMany`를 이용해 집계 기준 설정이 가능합니다. 예: 좋아요 수 최대 이미지:

```php
/**
 * 사용자의 가장 인기 있는 이미지 반환
 */
public function bestImage(): MorphOne
{
    return $this->morphOne(Image::class, 'imageable')->ofMany('likes', 'max');
}
```

> [!NOTE]  
> 고급 "one of many" 관계는 [has one of many 문서](#advanced-has-one-of-many-relationships) 참고.

<a name="many-to-many-polymorphic-relations"></a>
### 다대다 (다형성) (Many to Many Polymorphic)

<a name="many-to-many-polymorphic-table-structure"></a>
#### 테이블 구조

다형성 다대다 관계는 "morph one", "morph many"보다 조금 더 복잡합니다.

예: `Post`와 `Video` 모델이 `Tag` 모델을 공유하는 다형성 관계.

테이블 구조 예:

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
> 다형성 다대다 이전에 일반 [다대다 관계](#many-to-many) 문서를 먼저 봐 두는 것이 이해에 도움이 됩니다.

<a name="many-to-many-polymorphic-model-structure"></a>
#### 모델 정의

`Post`와 `Video` 모델에 `tags` 관계를 `morphToMany`로 정의합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphToMany;

class Post extends Model
{
    /**
     * 게시글 관련 태그들을 반환합니다.
     */
    public function tags(): MorphToMany
    {
        return $this->morphToMany(Tag::class, 'taggable');
    }
}
```

`morphToMany` 첫 번째 인자는 관련 모델명, 두 번째 인자는 관계명(`taggable`)입니다.

<a name="many-to-many-polymorphic-defining-the-inverse-of-the-relationship"></a>
#### 관계 역방향 정의하기

`Tag` 모델에서 부모 모델별 관계 메서드를 정의합니다. 각각 `morphedByMany` 메서드 호출:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphToMany;

class Tag extends Model
{
    /**
     * 이 태그가 붙은 게시글들
     */
    public function posts(): MorphToMany
    {
        return $this->morphedByMany(Post::class, 'taggable');
    }

    /**
     * 이 태그가 붙은 비디오들
     */
    public function videos(): MorphToMany
    {
        return $this->morphedByMany(Video::class, 'taggable');
    }
}
```

<a name="many-to-many-polymorphic-retrieving-the-relationship"></a>
#### 관계 조회

정의 후 다음과 같이 태그를 조회할 수 있습니다:

```php
use App\Models\Post;

$post = Post::find(1);

foreach ($post->tags as $tag) {
    // ...
}
```

다음과 같이 다형성 자식 모델에서 부모 모델 컬렉션을 조회할 수 있습니다:

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

기본적으로 Laravel은 다형성 `type`을 클래스명으로 저장합니다. 예: `App\Models\Post` 등.

애플리케이션 구조 변경에 영향을 받지 않도록 별도의 별칭(예: `'post'`, `'video'`)을 사용 할 수 있습니다. 다음처럼 `Relation::enforceMorphMap`에 매핑하면 됩니다:

```php
use Illuminate\Database\Eloquent\Relations\Relation;

Relation::enforceMorphMap([
    'post' => 'App\Models\Post',
    'video' => 'App\Models\Video',
]);
```

이 코드는 `App\Providers\AppServiceProvider`의 `boot` 메서드에 넣거나 별도 서비스 프로바이더를 만들어 넣으면 됩니다.

현재 모델의 별칭은 `$post->getMorphClass()`로 접근 가능하며, 별칭에 대응하는 클래스명은 `Relation::getMorphedModel($alias)`로 찾을 수 있습니다:

```php
use Illuminate\Database\Eloquent\Relations\Relation;

$alias = $post->getMorphClass();

$class = Relation::getMorphedModel($alias);
```

> [!WARNING]  
> 이미 운영 중인 애플리케이션에 morph map을 도입할 때는, 기존에 저장된 다형성 `*_type` 컬럼 값 중 클래스명이 남아있는 데이터들을 맵의 이름으로 변경해야 합니다.

---

<a name="dynamic-relationships"></a>
### 동적 관계 (Dynamic Relationships)

`resolveRelationUsing` 메서드를 통해 런타임에 모델 간 관계를 정의할 수 있습니다. 일반적인 앱 개발에서는 권장하지 않지만, Laravel 패키지 개발 시 유용할 수 있습니다.

첫 인자는 관계 이름(메서드명), 두 번째 인자는 모델 인스턴스를 받아 관계 인스턴스를 반환하는 클로저입니다. 보통 서비스 프로바이더 `boot`에서 정의합니다:

```php
use App\Models\Order;
use App\Models\Customer;

Order::resolveRelationUsing('customer', function (Order $orderModel) {
    return $orderModel->belongsTo(Customer::class, 'customer_id');
});
```

> [!WARNING]  
> 동적 관계를 정의할 때 항상 명시적으로 키 이름을 인자로 전달하세요.

---

<a name="querying-relations"></a>
## 관계 쿼리하기 (Querying Relations)

관계는 본래 메서드로 정의하므로, 해당 메서드를 호출하면 쿼리를 실행하지 않고 관계 인스턴스를 얻을 수 있습니다. 또한 모든 관계는 쿼리 빌더이므로 추가 조건을 체이닝 후 실제 데이터 조회가 가능합니다.

예를 들어 `User` 모델이 여러 `Post` 모델을 가질 때:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class User extends Model
{
    /**
     * 사용자의 모든 게시글을 반환합니다.
     */
    public function posts(): HasMany
    {
        return $this->hasMany(Post::class);
    }
}
```

추가 조건을 붙여 조회 가능:

```php
use App\Models\User;

$user = User::find(1);

$user->posts()->where('active', 1)->get();
```

관계는 모든 쿼리 빌더 메서드를 쓸 수 있으니 쿼리 문서를 참고하세요.

<a name="chaining-orwhere-clauses-after-relationships"></a>
#### 관계 뒤에 `orWhere` 쿼리 주의하기

다음과 같이 `orWhere`를 chain하는 경우:

```php
$user->posts()
        ->where('active', 1)
        ->orWhere('votes', '>=', 100)
        ->get();
```

SQL은 다음과 같은 형태로 작성되며, 관계 제약 조건과 `or` 조건이 같은 레벨로 묶여:

```sql
select *
from posts
where user_id = ? and active = 1 or votes >= 100
```

즉, `votes >= 100`인 모든 게시물을 반환할 수 있으므로 주의해야 합니다.

이럴 때는 다음처럼 논리 그룹으로 묶어줍니다:

```php
use Illuminate\Database\Eloquent\Builder;

$user->posts()
        ->where(function (Builder $query) {
            return $query->where('active', 1)
                         ->orWhere('votes', '>=', 100);
        })
        ->get();
```

SQL:

```sql
select *
from posts
where user_id = ? and (active = 1 or votes >= 100)
```

<a name="relationship-methods-vs-dynamic-properties"></a>
### 관계 메서드 vs 동적 속성

추가 조건이 필요없으면 동적 속성처럼 관계에 접근할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

foreach ($user->posts as $post) {
    // ...
}
```

동적 속성은 "지연 로딩"으로, 실제로 접근할 때 관계를 로딩합니다. 따라서 성능 최적화를 위해 [Eager Loading](#eager-loading) 방식으로 미리 관계를 로딩하는 것이 좋습니다.

<a name="querying-relationship-existence"></a>
### 관계 존재 쿼리하기

모델 조회 시 특정 관계가 존재하는 레코드로 한정할 수 있습니다. 예를 들어 하나 이상의 댓글이 있는 게시글만 조회:

```php
use App\Models\Post;

// 댓글이 하나라도 있는 게시글 조회
$posts = Post::has('comments')->get();
```

조건 추가도 가능합니다:

```php
// 댓글이 3개 이상 게시글 조회
$posts = Post::has('comments', '>=', 3)->get();
```

중첩된 has 쿼리도 "dot" 표기법으로 가능합니다:

```php
// 댓글에 이미지가 있는 게시글 조회
$posts = Post::has('comments.images')->get();
```

더 복잡한 조건은 `whereHas`를 씁니다:

```php
use Illuminate\Database\Eloquent\Builder;

// 댓글 내용이 'code%'인 게시글 조회
$posts = Post::whereHas('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
})->get();

// 댓글 10개 이상이며 내용이 'code%'인 게시글 조회
$posts = Post::whereHas('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
}, '>=', 10)->get();
```

> [!WARNING]  
> 현재 Eloquent는 데이터베이스가 다르면 관계 존재 여부 쿼리를 지원하지 않습니다.

<a name="inline-relationship-existence-queries"></a>
#### 간단한 관계 존재 조건 inline 쿼리

하나의 간단 조건으로 관계가 존재하는지 확인할 때는 `whereRelation`, `orWhereRelation`, `whereMorphRelation`, `orWhereMorphRelation` 메서드를 사용하면 편리합니다:

```php
use App\Models\Post;

$posts = Post::whereRelation('comments', 'is_approved', false)->get();
```

연산자도 지정 가능합니다:

```php
$posts = Post::whereRelation(
    'comments', 'created_at', '>=', now()->subHour()
)->get();
```

<a name="querying-relationship-absence"></a>
### 관계 부재 쿼리하기

관계가 없는 레코드로 한정하려면 `doesntHave`, `orDoesntHave` 메서드를 사용합니다:

```php
use App\Models\Post;

$posts = Post::doesntHave('comments')->get();
```

추가 조건은 `whereDoesntHave`, `orWhereDoesntHave`로 지정:

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::whereDoesntHave('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
})->get();
```

중첩 관계도 가능합니다:

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::whereDoesntHave('comments.author', function (Builder $query) {
    $query->where('banned', 0);
})->get();
```

<a name="querying-morph-to-relationships"></a>
### morphTo 관계 쿼리하기

`whereHasMorph`, `whereDoesntHaveMorph` 메서드로 morphTo 관계 존재 여부를 쿼리할 수 있습니다:

```php
use App\Models\Comment;
use App\Models\Post;
use App\Models\Video;
use Illuminate\Database\Eloquent\Builder;

// 제목이 'code%'인 게시글 또는 비디오에 달린 댓글 조회
$comments = Comment::whereHasMorph(
    'commentable',
    [Post::class, Video::class],
    function (Builder $query) {
        $query->where('title', 'like', 'code%');
    }
)->get();

// 제목이 'code%'인 게시글에 달린 댓글 중 조건에 맞지 않는 것 조회
$comments = Comment::whereDoesntHaveMorph(
    'commentable',
    Post::class,
    function (Builder $query) {
        $query->where('title', 'like', 'code%');
    }
)->get();
```

클로저에 두 번째 인자로 타입 정보가 전달되므로, 타입별로 조건을 달리 할 수 있습니다:

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

<a name="querying-all-morph-to-related-models"></a>
#### 모든 관계 모델 쿼리하기

`*` 와일드카드를 쓰면 모든 다형성 모델 타입을 대상으로 쿼리를 실행합니다(내부에서 추가 쿼리 발생):

```php
use Illuminate\Database\Eloquent\Builder;

$comments = Comment::whereHasMorph('commentable', '*', function (Builder $query) {
    $query->where('title', 'like', 'foo%');
})->get();
```

---

<a name="aggregating-related-models"></a>
## 관련 모델 집계 (Aggregating Related Models)

<a name="counting-related-models"></a>
### 관련 모델 수 세기

관계된 모델 수를 실제로 로드하지 않고 조회하려면 `withCount` 메서드를 사용하세요.

`{relation}_count` 속성이 모델에 추가됩니다:

```php
use App\Models\Post;

$posts = Post::withCount('comments')->get();

foreach ($posts as $post) {
    echo $post->comments_count;
}
```

배열을 넘기면 여러 관계 수를 동시에 구하고 조건도 추가할 수 있습니다:

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::withCount(['votes', 'comments' => function (Builder $query) {
    $query->where('content', 'like', 'code%');
}])->get();

echo $posts[0]->votes_count;
echo $posts[0]->comments_count;
```

별칭(alias)을 써서 같은 관계를 여러 번 집계할 수도 있습니다:

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
#### 지연된 카운트 로딩

이미 모델을 조회한 후에 관계 수를 불러오려면 `loadCount` 메서드를 사용하세요:

```php
$book = Book::first();

$book->loadCount('genres');
```

조건도 추가 가능합니다:

```php
$book->loadCount(['reviews' => function (Builder $query) {
    $query->where('rating', 5);
}]);
```

<a name="relationship-counting-and-custom-select-statements"></a>
#### 관계 카운트와 커스텀 SELECT문 조합

`withCount`를 `select`와 함께 사용할 땐, `select` 후에 `withCount`를 호출하세요:

```php
$posts = Post::select(['title', 'body'])
                ->withCount('comments')
                ->get();
```

<a name="other-aggregate-functions"></a>
### 기타 집계 함수

`withSum`, `withMin`, `withMax`, `withAvg`, `withExists` 등도 비슷하게 동작합니다. `{relation}_{function}_{column}` 속성을 추가합니다:

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

이 메서드들의 지연 로딩 버전도 있습니다:

```php
$post = Post::first();

$post->loadSum('comments', 'votes');
```

`select`와 같이 쓸 때는 반드시 `select` 이후 호출하세요:

```php
$posts = Post::select(['title', 'body'])
                ->withExists('comments')
                ->get();
```

<a name="counting-related-models-on-morph-to-relationships"></a>
### morphTo 관계의 관련 모델 수 세기

`morphTo` 관계에서 각 대상 모델별 관련 모델 수를 함께 로드하려면, `with`에 클로저를 써서 `morphWithCount`를 호출하세요:

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
#### 지연된 morphTo 카운트 로딩

이미 데이터를 가져왔을 때는 `loadMorphCount`를 사용하세요:

```php
$activities = ActivityFeed::with('parentable')->get();

$activities->loadMorphCount('parentable', [
    Photo::class => ['tags'],
    Post::class => ['comments'],
]);
```

---

<a name="eager-loading"></a>
## Eager Loading

Eloquent 관계는 동적 속성 접근 시 지연 로딩되므로, 여러 관계에 접근하면 N+1 쿼리 문제가 발생할 수 있습니다. 이를 방지하기 위해 관계를 미리 로드하는 것을 Eager Loading이라고 합니다.

예를 들어, `Book` 모델과 `Author` 모델이 있고:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Book extends Model
{
    /**
     * 책의 저자를 반환합니다.
     */
    public function author(): BelongsTo
    {
        return $this->belongsTo(Author::class);
    }
}
```

책과 저자를 모두 가져올 때:

```php
use App\Models\Book;

$books = Book::all();

foreach ($books as $book) {
    echo $book->author->name;
}
```

책마다 저자 조회 쿼리가 각각 실행되어 쿼리가 많아집니다.

대신 `with` 메서드로 관련 모델을 미리 로딩하면 쿼리를 크게 줄일 수 있습니다:

```php
$books = Book::with('author')->get();

foreach ($books as $book) {
    echo $book->author->name;
}
```

쿼리는 책 조회 1번 + 저자 조회 1번, 총 2번만 실행됩니다.

```sql
select * from books;

select * from authors where id in (1, 2, 3, ...);
```

<a name="eager-loading-multiple-relationships"></a>
#### 여러 관계 동시 Eager Loading

여러 관계도 배열로 지정해 한 번에 로딩할 수 있습니다:

```php
$books = Book::with(['author', 'publisher'])->get();
```

<a name="nested-eager-loading"></a>
#### 중첩 Eager Loading

관계의 하위 관계도 점(.) 표기법으로 지정할 수 있습니다:

```php
$books = Book::with('author.contacts')->get();
```

중첩 배열도 가능합니다:

```php
$books = Book::with([
    'author' => [
        'contacts',
        'publisher',
    ],
])->get();
```

<a name="nested-eager-loading-morphto-relationships"></a>
#### morphTo 관계 중첩 Eager Loading

`morphTo` 관계의 각 타입별로 중첩 관계를 부를 때는 다음처럼 작성합니다:

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
#### 특정 컬럼만 Eager Loading

필요한 컬럼만 지정해 로딩할 수 있습니다:

```php
$books = Book::with('author:id,name,book_id')->get();
```

> [!WARNING]  
> 이 경우 항상 `id`와 외래 키 컬럼도 포함해야 합니다.

<a name="eager-loading-by-default"></a>
#### 기본적으로 Eager Loading 하기

자주 항상 로딩할 관계는 모델에 `$with` 속성으로 정의할 수 있습니다:

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

특정 쿼리에서 `$with`에 포함된 관계를 제외하려면 `without`을 씁니다:

```php
$books = Book::without('author')->get();
```

전체를 다른 것으로 대체하려면 `withOnly`를 씁니다:

```php
$books = Book::withOnly('genre')->get();
```

<a name="constraining-eager-loads"></a>
### Eager Load 조건 지정하기

`with`에 배열을 넘기고 관계명(key)에 클로저(value)를 넣어 조건을 추가할 수 있습니다:

```php
use App\Models\User;
use Illuminate\Contracts\Database\Eloquent\Builder;

$users = User::with(['posts' => function (Builder $query) {
    $query->where('title', 'like', '%code%');
}])->get();
```

`where` 이외에도 정렬 등 쿼리 빌더 메서드를 자유롭게 적용할 수 있습니다:

```php
$users = User::with(['posts' => function (Builder $query) {
    $query->orderBy('created_at', 'desc');
}])->get();
```

> [!WARNING]  
> `limit`, `take` 같은 메서드는 Eager Load 조건에 사용할 수 없습니다.

<a name="constraining-eager-loading-of-morph-to-relationships"></a>
#### morphTo 관계 Eager Load 조건

`morphTo` 관계는 각각의 타입별로 쿼리를 실행하므로 `constrain` 메서드를 써서 타입별 쿼리 조건을 넣을 수 있습니다:

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

예제에서는 숨겨지지 않은 포스트와, 타입이 'educational'인 비디오만 로드합니다.

<a name="constraining-eager-loads-with-relationship-existence"></a>
#### 관계 존재 조건과 함께 Eager Load

조인 조건과 Eager Load 조건을 동시에 걸고 싶다면 `withWhereHas` 메서드를 쓰세요:

```php
use App\Models\User;

$users = User::withWhereHas('posts', function ($query) {
    $query->where('featured', true);
})->get();
```

---

<a name="lazy-eager-loading"></a>
### 지연 Eager Loading (Lazy Eager Loading)

모델을 이미 불러온 후에 조건에 따라 관계를 Eager Load 하고 싶을 때:

```php
use App\Models\Book;

$books = Book::all();

if ($someCondition) {
    $books->load('author', 'publisher');
}
```

조건도 지정할 수 있습니다:

```php
$author->load(['books' => function (Builder $query) {
    $query->orderBy('published_date', 'asc');
}]);
```

이미 로드되어 있으면 다시 로드하지 않는 `loadMissing`도 있습니다:

```php
$book->loadMissing('author');
```

<a name="nested-lazy-eager-loading-morphto"></a>
#### morphTo 관계 지연 Eager Loading

`loadMorph` 메서드를 써서 `morphTo` 관계 및 하위 관계를 지연 로드할 수 있습니다:

```php
<?php

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class ActivityFeed extends Model
{
    /**
     * 활동 피드의 부모 모델 반환
     */
    public function parentable(): MorphTo
    {
        return $this->morphTo();
    }
}
```

아래처럼 모델 및 관계를 넘겨주면 됩니다:

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

Eager Loading이 성능에 큰 이점을 주므로, 지연 로딩 자체를 금지할 수도 있습니다. 베이스 모델의 `preventLazyLoading` 메서드를 호출하세요. 보통 `AppServiceProvider`의 `boot`에 넣습니다:

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

이 설정 후에 지연 로딩 시 `Illuminate\Database\LazyLoadingViolationException` 예외가 발생합니다.

예외 대신 로그를 남기도록 하려면 `handleLazyLoadingViolationUsing` 메서드를 사용하세요:

```php
Model::handleLazyLoadingViolationUsing(function (Model $model, string $relation) {
    $class = $model::class;

    info("Attempted to lazy load [{$relation}] on model [{$class}].");
});
```

---

<a name="inserting-and-updating-related-models"></a>
## 관련 모델 삽입 및 갱신

<a name="the-save-method"></a>
### `save` 메서드

관계에 새 모델을 넣을 때, 수동으로 외래 키를 설정하지 않고도 `save` 메서드로 삽입할 수 있습니다.

예를 들어, 블로그 게시글에 새 댓글 추가:

```php
use App\Models\Comment;
use App\Models\Post;

$comment = new Comment(['message' => 'A new comment.']);

$post = Post::find(1);

$post->comments()->save($comment);
```

주의: `comments` 관계 메서드를 호출했지, 동적 속성을 사용하지 않았습니다. `save` 메서드는 자동으로 적절한 외래 키 값을 설정합니다.

복수 모델 삽입도 `saveMany`를 사용:

```php
$post = Post::find(1);

$post->comments()->saveMany([
    new Comment(['message' => 'A new comment.']),
    new Comment(['message' => 'Another new comment.']),
]);
```

삽입 후에는 `save`/`saveMany`가 메모리 내 로드된 관계를 갱신하지 않으므로, 곧바로 관계를 조회할 때는 `refresh`를 호출해 모델 전체를 갱신하세요:

```php
$post->comments()->save($comment);

$post->refresh();

// 새로 삽입된 댓글 포함 모두 조회 가능
$post->comments;
```

<a name="the-push-method"></a>
#### 모델 및 연관관계 재귀 저장 (`push` 메서드)

자신과 모든 연관된 관계 모델 데이터를 한 번에 저장하려면 `push`를 쓰면 됩니다:

```php
$post = Post::find(1);

$post->comments[0]->message = 'Message';
$post->comments[0]->author->name = 'Author Name';

$post->push();
```

`pushQuietly` 메서드는 이벤트 없이 같은 작업을 수행합니다:

```php
$post->pushQuietly();
```

<a name="the-create-method"></a>
### `create` 메서드

`save`와 달리, `create`는 속성 배열을 받아 새 모델 인스턴스를 만들고 DB에 저장합니다. 새 모델은 반환됩니다:

```php
use App\Models\Post;

$post = Post::find(1);

$comment = $post->comments()->create([
    'message' => 'A new comment.',
]);
```

복수 모델은 `createMany`로 생성:

```php
$post = Post::find(1);

$post->comments()->createMany([
    ['message' => 'A new comment.'],
    ['message' => 'Another new comment.'],
]);
```

이벤트 없이 생성하려면 `createQuietly`, `createManyQuietly`를 사용하세요:

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

기타 `findOrNew`, `firstOrNew`, `firstOrCreate`, `updateOrCreate`도 관계 모델 생성/갱신에 사용할 수 있습니다.

> [!NOTE]  
> `create` 메서드를 쓰기 전에는 꼭 [대량 할당(mass assignment)](/docs/10.x/eloquent#mass-assignment) 정책을 확인하세요.

<a name="updating-belongs-to-relationships"></a>
### belongsTo 관계 갱신

자식 모델에 새 부모 모델을 지정하려면 `associate` 메서드를 사용합니다. 예:

```php
use App\Models\Account;

$account = Account::find(10);

$user->account()->associate($account);

$user->save();
```

부모 관계를 끊으려면 `dissociate` 메서드를 사용합니다:

```php
$user->account()->dissociate();

$user->save();
```

<a name="updating-many-to-many-relationships"></a>
### 다대다 관계 갱신

<a name="attaching-detaching"></a>
#### `attach` / `detach`

다대다 관계에 새 연결을 추가하려면 `attach` 메서드:

```php
use App\Models\User;

$user = User::find(1);

$user->roles()->attach($roleId);
```

추가 데이터도 넘길 수 있습니다:

```php
$user->roles()->attach($roleId, ['expires' => $expires]);
```

관계 제거는 `detach`:

```php
// 지정 역할 하나 제거
$user->roles()->detach($roleId);

// 모든 역할 제거
$user->roles()->detach();
```

여러 ID도 배열 형태로 받습니다:

```php
$user = User::find(1);

$user->roles()->detach([1, 2, 3]);

$user->roles()->attach([
    1 => ['expires' => $expires],
    2 => ['expires' => $expires],
]);
```

<a name="syncing-associations"></a>
#### 관계 동기화 (Sync)

`synchronize` 메서드는 주어진 배열에 없는 ID는 모두 중간 테이블에서 제거합니다:

```php
$user->roles()->sync([1, 2, 3]);
```

중간 테이블 데이터도 지정할 수 있습니다:

```php
$user->roles()->sync([1 => ['expires' => true], 2, 3]);
```

모든 ID에 동일한 피벗 값을 넣으려면 `syncWithPivotValues`:

```php
$user->roles()->syncWithPivotValues([1, 2, 3], ['active' => true]);
```

기존 관계는 유지하면서 일부만 추가하려면 `syncWithoutDetaching`:

```php
$user->roles()->syncWithoutDetaching([1, 2, 3]);
```

<a name="toggling-associations"></a>
#### 관계 토글 (Toggle)

`synced` 상태를 토글합니다. 붙어 있으면 뗴고, 떨어져 있으면 붙입니다:

```php
$user->roles()->toggle([1, 2, 3]);
```

피벗 데이터 지정도 가능합니다:

```php
$user->roles()->toggle([
    1 => ['expires' => true],
    2 => ['expires' => true],
]);
```

<a name="updating-a-record-on-the-intermediate-table"></a>
#### 중간 테이블 레코드 갱신하기

기존 관계 중간 테이블 행을 갱신하려면 `updateExistingPivot`을 사용:

```php
$user = User::find(1);

$user->roles()->updateExistingPivot($roleId, [
    'active' => false,
]);
```

---

<a name="touching-parent-timestamps"></a>
## 부모 타임스탬프 갱신 (Touching Parent Timestamps)

`belongsTo` 또는 `belongsToMany` 관계에서 자식 모델이 업데이트되면 부모 모델의 `updated_at` 타임스탬프도 자동 갱신하도록 할 수 있습니다.

예: 댓글이 수정될 때 부모 게시글의 `updated_at`을 갱신하려면, 자식 모델에 `touches` 속성을 추가합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Comment extends Model
{
    /**
     * 타임스탬프를 자동 갱신할 관계 목록
     *
     * @var array
     */
    protected $touches = ['post'];

    /**
     * 댓글의 부모 게시글 반환
     */
    public function post(): BelongsTo
    {
        return $this->belongsTo(Post::class);
    }
}
```

> [!WARNING]  
> 부모 타임스탬프는 자식 모델을 Eloquent의 `save` 메서드로 업데이트할 때만 자동 갱신됩니다.