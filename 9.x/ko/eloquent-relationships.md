# Eloquent: 관계 (Eloquent: Relationships)

- [소개](#introduction)
- [관계 정의하기](#defining-relationships)
    - [일대일 (One To One)](#one-to-one)
    - [일대다 (One To Many)](#one-to-many)
    - [일대다 역방향 / belongsTo (One To Many (Inverse) / Belongs To)](#one-to-many-inverse)
    - [Has One Of Many](#has-one-of-many)
    - [Has One Through](#has-one-through)
    - [Has Many Through](#has-many-through)
- [다대다 관계 (Many To Many)](#many-to-many)
    - [중간 테이블 컬럼 조회하기](#retrieving-intermediate-table-columns)
    - [중간 테이블 컬럼으로 쿼리 필터링하기](#filtering-queries-via-intermediate-table-columns)
    - [중간 테이블 컬럼으로 쿼리 정렬하기](#ordering-queries-via-intermediate-table-columns)
    - [사용자 정의 중간 테이블 모델 정의하기](#defining-custom-intermediate-table-models)
- [다형 관계 (Polymorphic Relationships)](#polymorphic-relationships)
    - [일대일](#one-to-one-polymorphic-relations)
    - [일대다](#one-to-many-polymorphic-relations)
    - [Has One Of Many](#one-of-many-polymorphic-relations)
    - [다대다](#many-to-many-polymorphic-relations)
    - [사용자 정의 다형 타입](#custom-polymorphic-types)
- [동적 관계 (Dynamic Relationships)](#dynamic-relationships)
- [관계 쿼리하기 (Querying Relations)](#querying-relations)
    - [관계 메서드와 동적 속성 차이](#relationship-methods-vs-dynamic-properties)
    - [관계 존재 여부 쿼리하기](#querying-relationship-existence)
    - [관계 부재 여부 쿼리하기](#querying-relationship-absence)
    - [Morph To 관계 쿼리하기](#querying-morph-to-relationships)
- [관련 모델 집계 (Aggregating Related Models)](#aggregating-related-models)
    - [관계된 모델 개수 세기](#counting-related-models)
    - [기타 집계 함수](#other-aggregate-functions)
    - [Morph To 관계에서 관련 모델 개수 세기](#counting-related-models-on-morph-to-relationships)
- [즉시 로딩 (Eager Loading)](#eager-loading)
    - [즉시 로딩 제약 조건](#constraining-eager-loads)
    - [지연 즉시 로딩](#lazy-eager-loading)
    - [지연 로딩 방지하기](#preventing-lazy-loading)
- [관련 모델 삽입 및 업데이트](#inserting-and-updating-related-models)
    - [`save` 메서드](#the-save-method)
    - [`create` 메서드](#the-create-method)
    - [belongsTo 관계 업데이트하기](#updating-belongs-to-relationships)
    - [다대다 관계 업데이트하기](#updating-many-to-many-relationships)
- [부모 타임스탬프 터치하기](#touching-parent-timestamps)

<a name="introduction"></a>
## 소개 (Introduction)

데이터베이스 테이블은 종종 서로 연관됩니다. 예를 들어, 블로그 게시물은 여러 댓글을 가질 수 있고, 주문은 주문을 생성한 사용자와 연관될 수 있습니다. Eloquent는 이러한 관계를 관리하고 다루는 작업을 쉽게 해주며, 다음과 같은 다양한 일반적인 관계 타입을 지원합니다:

<div class="content-list" markdown="1">

- [일대일 (One To One)](#one-to-one)
- [일대다 (One To Many)](#one-to-many)
- [다대다 (Many To Many)](#many-to-many)
- [Has One Through](#has-one-through)
- [Has Many Through](#has-many-through)
- [일대일 (다형, Polymorphic)](#one-to-one-polymorphic-relations)
- [일대다 (다형, Polymorphic)](#one-to-many-polymorphic-relations)
- [다대다 (다형, Polymorphic)](#many-to-many-polymorphic-relations)

</div>

<a name="defining-relationships"></a>
## 관계 정의하기 (Defining Relationships)

Eloquent 관계는 Eloquent 모델 클래스 내에 메서드로 정의합니다. 관계는 강력한 [쿼리 빌더](/docs/9.x/queries) 역할도 수행하기 때문에, 관계를 메서드로 정의하면 메서드 체이닝과 쿼리 조합이 훨씬 편리해집니다. 예를 들어, `posts` 관계에 추가 쿼리 조건을 체이닝할 수 있습니다:

```
$user->posts()->where('active', 1)->get();
```

관계를 사용하기에 앞서 Eloquent에서 지원하는 각 관계 타입을 어떻게 정의하는지 살펴보겠습니다.

<a name="one-to-one"></a>
### 일대일 (One To One)

일대일 관계는 데이터베이스에서 가장 기본적인 관계입니다. 예를 들어, `User` 모델은 하나의 `Phone` 모델과 연관될 수 있습니다. 이 관계를 정의하기 위해 `User` 모델에 `phone` 메서드를 만들고, 그 안에서 `hasOne` 메서드를 호출하여 결과를 반환하면 됩니다. `hasOne` 메서드는 모델의 기본 클래스 `Illuminate\Database\Eloquent\Model`에서 제공합니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 사용자와 연관된 전화번호를 가져옵니다.
     */
    public function phone()
    {
        return $this->hasOne(Phone::class);
    }
}
```

`hasOne` 메서드의 첫 번째 인자로는 관련 모델 클래스 이름을 전달합니다. 관계가 정의되면 Eloquent의 동적 속성을 통해 관련 레코드를 쉽게 조회할 수 있습니다. 동적 속성은 관계 메서드를 마치 모델의 속성처럼 접근할 수 있게 해줍니다:

```
$phone = User::find(1)->phone;
```

Eloquent는 부모 모델 이름을 기반으로 관계의 외래 키를 자동으로 판단합니다. 이 경우 `Phone` 모델은 자동으로 `user_id` 외래 키를 가진 것으로 가정합니다. 이 규칙을 재정의하려면 `hasOne` 메서드에 두 번째 인자로 외래 키명을 전달하세요:

```
return $this->hasOne(Phone::class, 'foreign_key');
```

또한, Eloquent는 외래 키에 매칭될 값이 부모 모델의 기본 키 컬럼 값(`id` 또는 `$primaryKey` 프로퍼티)이라고 가정합니다. 만약 다른 컬럼을 사용하려면 세 번째 인자로 로컬 키를 지정할 수 있습니다:

```
return $this->hasOne(Phone::class, 'foreign_key', 'local_key');
```

<a name="one-to-one-defining-the-inverse-of-the-relationship"></a>
#### 관계의 역(逆) 정의하기

`User` 모델에서 `Phone` 모델에 접근할 수 있으니, 이제 `Phone` 모델에서 이 전화번호를 소유하는 사용자를 조회할 수 있도록 관계를 정의해봅시다. 이 역관계는 `belongsTo` 메서드로 정의합니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Phone extends Model
{
    /**
     * 이 전화번호를 소유한 사용자를 가져옵니다.
     */
    public function user()
    {
        return $this->belongsTo(User::class);
    }
}
```

`user` 메서드를 호출할 때, Eloquent는 `id`가 `Phone` 모델의 `user_id` 컬럼과 일치하는 `User` 모델을 찾습니다.

Eloquent는 관계 메서드 이름에 `_id`를 붙여 외래 키 이름을 추정합니다. 이 예에서는 `user_id` 컬럼을 가진 것으로 간주합니다. 만약 외래 키명이 다르다면, `belongsTo` 메서드의 두 번째 인자로 외래 키명을 직접 지정할 수 있습니다:

```
/**
 * 이 전화번호를 소유한 사용자를 가져옵니다.
 */
public function user()
{
    return $this->belongsTo(User::class, 'foreign_key');
}
```

부모 모델이 기본 키로 `id`를 사용하지 않거나, 다른 컬럼으로 연관 모델을 탐색하려면 `belongsTo` 메서드의 세 번째 인자로 로컬 키를 지정할 수 있습니다:

```
/**
 * 이 전화번호를 소유한 사용자를 가져옵니다.
 */
public function user()
{
    return $this->belongsTo(User::class, 'foreign_key', 'owner_key');
}
```

<a name="one-to-many"></a>
### 일대다 (One To Many)

일대다 관계는 하나의 부모 모델이 여러 자식 모델을 가지는 경우에 정의합니다. 예를 들어, 블로그 게시물은 여러 개의 댓글을 가질 수 있습니다. 다른 관계들과 마찬가지로 Eloquent 모델에 메서드를 정의하면 됩니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Post extends Model
{
    /**
     * 블로그 게시물의 댓글들을 가져옵니다.
     */
    public function comments()
    {
        return $this->hasMany(Comment::class);
    }
}
```

Eloquent는 `Comment` 모델의 외래 키 컬럼명을 자동으로 추정합니다. 규칙에 따라 부모 모델 이름을 스네이크 케이스로 변환한 뒤 `_id`를 붙입니다. 위 예에서는 `post_id`가 됩니다.

관계 메서드를 정의한 후에는 `comments` 동적 속성을 통해 관련 댓글 컬렉션([collection](/docs/9.x/eloquent-collections))을 조회할 수 있습니다:

```
use App\Models\Post;

$comments = Post::find(1)->comments;

foreach ($comments as $comment) {
    //
}
```

관계는 쿼리 빌더 역할도 하므로, 추가 조건을 체이닝하려면 메서드 형태로 호출하고 쿼리를 붙이면 됩니다:

```
$comment = Post::find(1)->comments()
                    ->where('title', 'foo')
                    ->first();
```

`hasOne`과 마찬가지로 `hasMany`에 외래 키와 로컬 키를 직접 지정할 수도 있습니다:

```
return $this->hasMany(Comment::class, 'foreign_key');

return $this->hasMany(Comment::class, 'foreign_key', 'local_key');
```

<a name="one-to-many-inverse"></a>
### 일대다 (역방향) / belongsTo (One To Many (Inverse) / Belongs To)

게시물의 모든 댓글을 조회할 수 있으니, 댓글에서 자신의 부모 게시물에 접근할 수 있도록 역관계를 정의해봅시다. 역관계는 자식 모델에 `belongsTo` 메서드로 정의합니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Comment extends Model
{
    /**
     * 이 댓글이 속한 게시물을 가져옵니다.
     */
    public function post()
    {
        return $this->belongsTo(Post::class);
    }
}
```

정의 후에는 `post` 동적 속성으로 부모 게시물을 조회할 수 있습니다:

```
use App\Models\Comment;

$comment = Comment::find(1);

return $comment->post->title;
```

이때 Eloquent는 `Comment` 모델의 `post_id` 컬럼과 `Post` 모델의 `id` 컬럼이 일치하는 레코드를 찾습니다.

외래 키는 관계 메서드 이름 뒤에 부모 모델의 기본 키명을 붙여 `_`로 구분하는 방식으로 추정(예: `post_id`)합니다. 만약 외래 키가 다르면 `belongsTo` 두 번째 인자로 직접 지정하세요:

```
/**
 * 이 댓글이 속한 게시물을 가져옵니다.
 */
public function post()
{
    return $this->belongsTo(Post::class, 'foreign_key');
}
```

부모 모델의 기본 키가 `id`가 아니거나 다른 컬럼을 통해 찾으려면 세 번째 인자를 넣어 키를 지정할 수 있습니다:

```
/**
 * 이 댓글이 속한 게시물을 가져옵니다.
 */
public function post()
{
    return $this->belongsTo(Post::class, 'foreign_key', 'owner_key');
}
```

<a name="default-models"></a>
#### 기본 모델 지정하기

`belongsTo`, `hasOne`, `hasOneThrough`, `morphOne` 관계는 `null`일 경우 반환할 기본 모델을 정의할 수 있습니다. 이 패턴은 [널 오브젝트 패턴](https://en.wikipedia.org/wiki/Null_Object_pattern)으로 알려졌으며, 조건문 제거에 도움이 됩니다.

예를 들어, `Post` 모델에 연결된 사용자(`user`)가 없을 때 빈 `App\Models\User` 모델을 반환할 수 있습니다:

```
/**
 * 게시물 작성자를 가져옵니다.
 */
public function user()
{
    return $this->belongsTo(User::class)->withDefault();
}
```

기본 모델을 특정 속성으로 채우고 싶으면 배열이나 클로저를 인자로 전달하세요:

```
/**
 * 게시물 작성자를 가져옵니다.
 */
public function user()
{
    return $this->belongsTo(User::class)->withDefault([
        'name' => 'Guest Author',
    ]);
}

/**
 * 게시물 작성자를 가져옵니다.
 */
public function user()
{
    return $this->belongsTo(User::class)->withDefault(function ($user, $post) {
        $user->name = 'Guest Author';
    });
}
```

<a name="querying-belongs-to-relationships"></a>
#### belongsTo 관계 쿼리하기

belongsTo 관계의 자식 모델을 쿼리할 때는 `where` 구문을 수동으로 작성하여 대응하는 Eloquent 모델을 조회할 수 있습니다:

```
use App\Models\Post;

$posts = Post::where('user_id', $user->id)->get();
```

하지만 `whereBelongsTo` 메서드를 사용하면 특정 모델과 해당 관계 및 외래 키를 자동으로 판단하여 쿼리할 수 있어 편리합니다:

```
$posts = Post::whereBelongsTo($user)->get();
```

`whereBelongsTo`는 [컬렉션](/docs/9.x/eloquent-collections)도 받아들여, 컬렉션 내 모든 부모 모델에 속하는 자식을 조회합니다:

```
$users = User::where('vip', true)->get();

$posts = Post::whereBelongsTo($users)->get();
```

Laravel은 기본적으로 모델 클래스 이름을 기반으로 관계를 판단하지만, 두 번째 인자로 관계명을 직접 지정할 수도 있습니다:

```
$posts = Post::whereBelongsTo($user, 'author')->get();
```

<a name="has-one-of-many"></a>
### Has One Of Many

경우에 따라 하나의 모델에 여러 관련 모델이 있지만, 가장 "최신" 또는 "오래된" 단일 모델만 쉽게 조회하고 싶을 수 있습니다. 예를 들어, `User` 모델이 여러 `Order` 모델과 연관되어 있지만, 사용자가 가장 최근에 주문한 내역만 조회하고 싶을 때 `hasOne` 관계와 `ofMany` 메서드를 함께 사용합니다:

```php
/**
 * 사용자의 최신 주문을 가져옵니다.
 */
public function latestOrder()
{
    return $this->hasOne(Order::class)->latestOfMany();
}
```

마찬가지로 가장 오래된 주문 모델도 쉽게 정의할 수 있습니다:

```php
/**
 * 사용자의 가장 오래된 주문을 가져옵니다.
 */
public function oldestOrder()
{
    return $this->hasOne(Order::class)->oldestOfMany();
}
```

기본적으로 `latestOfMany` 와 `oldestOfMany`는 모델의 기본 키 (정렬 가능한 컬럼)를 기준으로 최신 또는 오래된 모델을 조회합니다. 하지만 다른 정렬 기준을 적용해 단일 모델을 뽑고 싶을 때도 있습니다.

예를 들어 `ofMany` 메서드를 사용해 가장 가격이 높은 주문을 조회할 수 있습니다. 첫 번째 인자에 정렬할 컬럼 이름, 두 번째 인자에 적용할 집계 함수를(`min`, `max`) 전달하세요:

```php
/**
 * 사용자의 최고가 주문을 가져옵니다.
 */
public function largestOrder()
{
    return $this->hasOne(Order::class)->ofMany('price', 'max');
}
```

> [!WARNING]
> PostgreSQL에서는 UUID 컬럼에 대해 `MAX` 함수 실행을 지원하지 않으므로, 현재 PostgreSQL UUID 컬럼과 `hasOneOfMany` 관계는 함께 사용할 수 없습니다.

<a name="advanced-has-one-of-many-relationships"></a>
#### 고급 Has One Of Many 관계

더 복잡한 "has one of many" 관계를 구축할 수도 있습니다. 예를 들어, `Product` 모델에 여러 `Price` 모델이 연결되어 있는데, 새 가격이 발표되어도 이전 가격 기록을 보존한다고 가정합시다. 또한, `published_at` 컬럼으로 미래 시점에 적용될 가격이 미리 저장될 수 있습니다.

즉, 출판 날짜가 미래가 아닌 최신 가격을 가져와야 하며, 만약 출판 날짜가 동일하다면 큰 `id` 값을 가진 가격을 우선 선택해야 합니다. 이를 위해 `ofMany` 메서드에 정렬 기준 컬럼들을 배열로 전달하고, 두 번째 인자로 클로저를 줘서 추가 쿼리 조건을 걸면 됩니다:

```php
/**
 * 상품의 현재 가격을 가져옵니다.
 */
public function currentPricing()
{
    return $this->hasOne(Price::class)->ofMany([
        'published_at' => 'max',
        'id' => 'max',
    ], function ($query) {
        $query->where('published_at', '<', now());
    });
}
```

<a name="has-one-through"></a>
### Has One Through

"has one through" 관계는 또 다른 모델과의 일대일 관계를 제3의 모델을 경유해서 정의합니다.

예를 들어, 차량 수리소 애플리케이션에서 `Mechanic` 모델은 한 대의 `Car` 모델과 연관되고, `Car` 모델은 하나의 `Owner` 모델과 연관될 수 있습니다. 데이터베이스상에서 정비공(`Mechanic`)과 차량 소유자(`Owner`)는 직접적인 관계가 없지만, 정비공은 `Car` 모델을 통해 소유자를 조회할 수 있습니다.

필요한 테이블 구조를 보겠습니다:

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

`Mechanic` 모델에 다음과 같이 관계를 정의합니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Mechanic extends Model
{
    /**
     * 자동차 소유자를 가져옵니다.
     */
    public function carOwner()
    {
        return $this->hasOneThrough(Owner::class, Car::class);
    }
}
```

`hasOneThrough` 메서드의 첫 번째 인자는 최대 깊이의 모델(`Owner`), 두 번째 인자는 중간 모델(`Car`) 이름입니다.

또는 관계가 이미 각 모델에 정의되어 있다면 `through` 메서드를 사용해 다음처럼 선언할 수 있습니다:

```php
// 문자열 기반 구문
return $this->through('cars')->has('owner');

// 동적 메서드 구문
return $this->throughCars()->hasOwner();
```

<a name="has-one-through-key-conventions"></a>
#### 키 규약

일반적인 Eloquent 외래 키 규약이 사용됩니다. 키를 커스텀하려면 `hasOneThrough`에 세 번째, 네 번째, 다섯 번째, 여섯 번째 인자로 키명을 전달하세요:

- 세 번째 인자: 중간 모델 외래 키 (`cars` 테이블)
- 네 번째 인자: 최종 모델 외래 키 (`owners` 테이블)
- 다섯 번째 인자: 로컬 키 (`mechanics` 테이블)
- 여섯 번째 인자: 중간 모델 로컬 키 (`cars` 테이블)

예:

```
class Mechanic extends Model
{
    /**
     * 자동차 소유자 가져오기
     */
    public function carOwner()
    {
        return $this->hasOneThrough(
            Owner::class,
            Car::class,
            'mechanic_id', // cars 테이블 외래 키
            'car_id', // owners 테이블 외래 키
            'id', // mechanics 테이블 로컬 키
            'id'  // cars 테이블 로컬 키
        );
    }
}
```

키를 이미 정의한 관계를 경유해 사용하려면 위와 같이 `through` 메서드를 통해 재사용하세요.

<a name="has-many-through"></a>
### Has Many Through

"has-many-through" 관계는 중간 관계를 경유해 멀리 있는 연관 관계들을 쉽게 조회할 수 있습니다.

예를 들어, Laravel Vapor와 같은 배포 플랫폼에서 `Project`는 중간 모델인 `Environment`를 거쳐 여러 `Deployment`와 연관될 수 있습니다. 프로젝트와 배포 간 관계를 쉽게 조회할 수 있습니다.

관련 테이블 구조는 다음과 같습니다:

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

`Project` 모델에 다음과 같이 정의합니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Project extends Model
{
    /**
     * 프로젝트의 모든 배포를 가져옵니다.
     */
    public function deployments()
    {
        return $this->hasManyThrough(Deployment::class, Environment::class);
    }
}
```

첫 번째 인자는 최종 모델(`Deployment`), 두 번째는 중간 모델(`Environment`)입니다.

이미 각 모델이 관계를 정의했다면 `through` 메서드로 관계 이름을 연결할 수도 있습니다:

```php
// 문자열 기반
return $this->through('environments')->has('deployments');

// 동적 메서드
return $this->throughEnvironments()->hasDeployments();
```

`Deployment` 테이블에는 `project_id`가 없지만, Eloquent는 중간 모델 `Environment`의 `project_id`를 확인하여 해당 환경 ID를 찾고 이를 통해 `Deployment`를 조회합니다.

<a name="has-many-through-key-conventions"></a>
#### 키 규약

기본적인 Eloquent 외래 키 규칙이 사용됩니다. 키를 커스터마이징하려면 `hasManyThrough` 메서드에 아래 인자를 지정하세요:

- 세 번째: 중간 모델의 외래 키
- 네 번째: 최종 모델의 외래 키
- 다섯 번째: 부모 모델 로컬 키
- 여섯 번째: 중간 모델 로컬 키

예:

```
class Project extends Model
{
    public function deployments()
    {
        return $this->hasManyThrough(
            Deployment::class,
            Environment::class,
            'project_id', // environments 테이블 외래 키
            'environment_id', // deployments 테이블 외래 키
            'id', // projects 테이블 로컬 키
            'id'  // environments 테이블 로컬 키
        );
    }
}
```

기존 각 모델이 관계를 정의했다면 `through` 메서드로 재사용할 수 있습니다.

```php
// 문자열 기반
return $this->through('environments')->has('deployments');

// 동적 메서드
return $this->throughEnvironments()->hasDeployments();
```

<a name="many-to-many"></a>
## 다대다 관계 (Many To Many Relationships)

다대다 관계는 `hasOne`, `hasMany` 보다 약간 복잡합니다. 예를 들어, 사용자가 여러 역할(Roles)을 가질 수 있고, 그 역할은 다른 사용자들과도 공유될 수 있습니다. 즉, 한 명의 사용자에 여러 역할이 있고, 한 역할에 여러 사용자가 속하는 경우입니다.

<a name="many-to-many-table-structure"></a>
#### 테이블 구조

다대다 관계에는 세 개의 테이블이 필요합니다: `users`, `roles`, 그리고 사용자 역할을 연결하는 중간 테이블 `role_user`. 중간 테이블 이름은 관련 모델명을 사전순으로 정렬해서 만듭니다.

`role_user` 테이블은 `user_id`와 `role_id` 컬럼을 가지며, 사용자와 역할을 연결하는 역할을 합니다.

역할이 여러 사용자에 속할 수 있으므로 `roles` 테이블에 `user_id`를 넣는 것은 적합하지 않습니다(이 경우 역할은 단 하나의 사용자에만 속함).

관계 테이블 구조는 다음과 같습니다:

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
#### 모델 구조

다대다 관계는 `belongsToMany` 메서드 결과를 반환하는 메서드로 정의합니다. 이 메서드는 `Illuminate\Database\Eloquent\Model` 클래스에서 사용할 수 있습니다.

예를 들어, `User` 모델에 `roles` 메서드를 만들고 관련 모델 클래스를 인자로 전달합니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 사용자의 역할들을 가져옵니다.
     */
    public function roles()
    {
        return $this->belongsToMany(Role::class);
    }
}
```

정의 후에는 `roles` 동적 속성을 이용해 사용자의 역할을 조회할 수 있습니다:

```
use App\Models\User;

$user = User::find(1);

foreach ($user->roles as $role) {
    //
}
```

관계도 쿼리 빌더로 동작하므로, 조건을 추가하려면 메서드 형태로 호출하고 체인하세요:

```
$roles = User::find(1)->roles()->orderBy('name')->get();
```

중간 테이블 이름은 관련 모델명을 알파벳 순으로 붙여 결정하지만, 원하는 경우 `belongsToMany` 두 번째 인자로 직접 지정해 덮어쓸 수 있습니다:

```
return $this->belongsToMany(Role::class, 'role_user');
```

중간 테이블의 컬럼 이름도 추가 인자로 직접 지정 가능합니다. 세 번째 인자는 현재 모델에 대한 외래 키, 네 번째는 연결할 모델에 대한 외래 키입니다:

```
return $this->belongsToMany(Role::class, 'role_user', 'user_id', 'role_id');
```

<a name="many-to-many-defining-the-inverse-of-the-relationship"></a>
#### 역관계 정의하기

다대다 관계의 "역" 관계도 동일하게 `belongsToMany` 메서드로 정의합니다.

예를 들어, `Role` 모델에 `users` 메서드를 정의하는 방법:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Role extends Model
{
    /**
     * 역할에 속한 사용자들을 가져옵니다.
     */
    public function users()
    {
        return $this->belongsToMany(User::class);
    }
}
```

`User` 모델에서 정의한 것과 동일하게, 관련 모델명을 지정하고 필요 시 테이블과 키도 지정할 수 있습니다.

<a name="retrieving-intermediate-table-columns"></a>
### 중간 테이블 컬럼 조회하기

다대다 관계에는 항상 중간 테이블이 존재합니다. Eloquent는 관련 모델에 자동으로 `pivot` 속성을 부여해 중간 테이블 레코드에 접근할 수 있게 합니다:

```
use App\Models\User;

$user = User::find(1);

foreach ($user->roles as $role) {
    echo $role->pivot->created_at;
}
```

기본적으로 `pivot` 모델에는 관련 모델 키 컬럼만 포함됩니다. 중간 테이블에 추가 컬럼이 있다면, 관계 정의 시 `withPivot` 메서드를 사용해 포함시켜야 합니다:

```
return $this->belongsToMany(Role::class)->withPivot('active', 'created_by');
```

중간 테이블에 `created_at`, `updated_at` 타임스탬프가 있고 Eloquent가 이를 자동으로 유지하려면 `withTimestamps` 메서드를 호출하세요:

```
return $this->belongsToMany(Role::class)->withTimestamps();
```

> [!WARNING]
> Eloquent의 자동 타임스탬프 기능을 사용하는 중간 테이블은 `created_at` 및 `updated_at` 컬럼 모두가 있어야 합니다.

<a name="customizing-the-pivot-attribute-name"></a>
#### `pivot` 속성 이름 변경하기

중간 테이블 속성은 기본적으로 `pivot`이라는 이름이지만, `as` 메서드를 사용해 다른 이름으로 바꿀 수 있습니다.

예를 들어, 사용자가 여러 팟캐스트에 구독한다고 한다면, 중간 테이블 속성 이름을 `subscription`으로 지정할 수 있습니다:

```
return $this->belongsToMany(Podcast::class)
                ->as('subscription')
                ->withTimestamps();
```

커스텀 속성 이름 지정 후엔 해당 이름을 통해 중간 테이블 데이터에 접근할 수 있습니다:

```
$users = User::with('podcasts')->get();

foreach ($users->flatMap->podcasts as $podcast) {
    echo $podcast->subscription->created_at;
}
```

<a name="filtering-queries-via-intermediate-table-columns"></a>
### 중간 테이블 컬럼으로 쿼리 필터링하기

`belongsToMany` 관계 쿼리 시 `wherePivot`, `wherePivotIn`, `wherePivotNotIn`, `wherePivotBetween`, `wherePivotNotBetween`, `wherePivotNull`, `wherePivotNotNull` 메서드들로 중간 테이블 컬럼 조건을 사용할 수 있습니다:

```
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
### 중간 테이블 컬럼으로 쿼리 정렬하기

`belongsToMany` 관계 결과를 정렬할 때는 `orderByPivot` 메서드를 사용하세요.

예를 들어, 최신 배지를 가져오는 쿼리:

```
return $this->belongsToMany(Badge::class)
                ->where('rank', 'gold')
                ->orderByPivot('created_at', 'desc');
```

<a name="defining-custom-intermediate-table-models"></a>
### 사용자 정의 중간 테이블 모델 지정하기

중간 테이블을 표현하는 사용자 정의 모델을 만들고자 할 때는 관계 정의 시 `using` 메서드를 호출하여 커스텀 피벗 모델을 지정합니다. 피벗 모델은 추가 메서드나 캐스팅을 정의하는 데 유용합니다.

다대다 피벗 모델은 `Illuminate\Database\Eloquent\Relations\Pivot` 클래스를 상속해야 하며, 다형 다대다 피벗 모델은 `MorphPivot`을 상속해야 합니다.

예를 들어, `Role` 모델이 커스텀 `RoleUser` 중간 테이블 모델을 사용하는 경우:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Role extends Model
{
    /**
     * 역할에 속한 사용자들.
     */
    public function users()
    {
        return $this->belongsToMany(User::class)->using(RoleUser::class);
    }
}
```

`RoleUser` 모델은 `Pivot` 클래스를 상속:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Relations\Pivot;

class RoleUser extends Pivot
{
    //
}
```

> [!WARNING]
> 피벗 모델에는 `SoftDeletes` 트레이트를 사용할 수 없습니다. 피벗 레코드를 소프트 삭제하려면, 일반 Eloquent 모델로 전환하는 것이 좋습니다.

<a name="custom-pivot-models-and-incrementing-ids"></a>
#### 커스텀 피벗 모델과 자동 증가 ID

커스텀 피벗 모델로 자동 증가하는 기본 키를 사용하는 경우, 모델 클래스에 `incrementing` 프로퍼티를 `true`로 지정하세요:

```
/**
 * 기본 키가 자동 증가인지 여부
 *
 * @var bool
 */
public $incrementing = true;
```

<a name="polymorphic-relationships"></a>
## 다형 관계 (Polymorphic Relationships)

다형 관계는 자식 모델이 하나 이상의 서로 다른 타입 모델에 속할 수 있도록 단일 연관 관계를 사용하게 합니다.

예를 들어, 사용자가 블로그 게시물과 동영상을 모두 공유할 수 있는 애플리케이션에서, `Comment` 모델이 `Post`와 `Video` 모두에 연결될 수 있습니다.

<a name="one-to-one-polymorphic-relations"></a>
### 일대일 (다형 관계)

<a name="one-to-one-polymorphic-table-structure"></a>
#### 테이블 구조

일대일 다형 관계는 일반적인 일대일 관계와 비슷하지만, 자식 모델이 여러 부모 타입에 속할 수 있습니다.

예를 들어, 블로그의 `Post`와 `User`가 모두 `Image` 모델과 다형 관계를 가질 수 있습니다. 이렇게 하면 이미지 정보를 하나의 테이블에서 관리하면서 게시물과 사용자 모두에 연결할 수 있습니다.

테이블 구조:

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

`images` 테이블의 `imageable_id` 컬럼에는 `Post` 또는 `User`의 ID값이 저장되고, `imageable_type` 컬럼에는 부모 모델의 클래스 이름(`App\Models\Post` 또는 `App\Models\User`)이 들어갑니다.

`imageable_type` 값은 Eloquent가 어떤 부모 모델인지 구분하는 데 사용됩니다.

<a name="one-to-one-polymorphic-model-structure"></a>
#### 모델 구조

관계 모델 정의 예:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Image extends Model
{
    /**
     * 부모 imageable 모델을 가져옵니다 (User 또는 Post).
     */
    public function imageable()
    {
        return $this->morphTo();
    }
}

class Post extends Model
{
    /**
     * 게시물의 이미지 반환
     */
    public function image()
    {
        return $this->morphOne(Image::class, 'imageable');
    }
}

class User extends Model
{
    /**
     * 사용자의 이미지 반환
     */
    public function image()
    {
        return $this->morphOne(Image::class, 'imageable');
    }
}
```

<a name="one-to-one-polymorphic-retrieving-the-relationship"></a>
#### 관계 조회하기

테이블과 모델이 정의되면 동적 관계 속성으로 접근할 수 있습니다.

예를 들어, 게시물의 이미지를 조회할 때:

```
use App\Models\Post;

$post = Post::find(1);

$image = $post->image;
```

다형 자식 모델의 부모를 조회할 때는 `morphTo` 메서드를 호출한 이름(여기서는 `imageable`)으로 접근하면 됩니다:

```
use App\Models\Image;

$image = Image::find(1);

$imageable = $image->imageable;
```

`imageable` 관계는 `Post` 또는 `User` 인스턴스를 반환합니다.

<a name="morph-one-to-one-key-conventions"></a>
#### 키 규약

필요 시 다형 자식 모델의 "id"와 "type" 컬럼 이름을 지정할 수 있습니다. 관계 메서드 이름을 `morphTo` 첫 번째 인자로 넘기는 걸 잊지 마세요 (`__FUNCTION__` 사용 추천):

```
/**
 * 이미지가 속한 모델을 반환
 */
public function imageable()
{
    return $this->morphTo(__FUNCTION__, 'imageable_type', 'imageable_id');
}
```

<a name="one-to-many-polymorphic-relations"></a>
### 일대다 (다형 관계)

<a name="one-to-many-polymorphic-table-structure"></a>
#### 테이블 구조

일대다 다형 관계는 일반적인 일대다 관계와 비슷하지만, 자식 모델이 여러 부모 타입에 속할 수 있습니다.

예를 들어, 사용자가 게시물과 동영상에 댓글을 달 수 있다면, 하나의 `comments` 테이블을 공유하여 두 타입 모두에 댓글 정보를 저장할 수 있습니다.

필요 테이블:

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
#### 모델 구조

관계 모델 정의 예:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Comment extends Model
{
    /**
     * 부모 commentable 모델을 반환 (Post 또는 Video)
     */
    public function commentable()
    {
        return $this->morphTo();
    }
}

class Post extends Model
{
    /**
     * 게시물에 달린 댓글들
     */
    public function comments()
    {
        return $this->morphMany(Comment::class, 'commentable');
    }
}

class Video extends Model
{
    /**
     * 동영상에 달린 댓글들
     */
    public function comments()
    {
        return $this->morphMany(Comment::class, 'commentable');
    }
}
```

<a name="one-to-many-polymorphic-retrieving-the-relationship"></a>
#### 관계 조회하기

정의 후에는 동적 관계 속성으로 접근 가능합니다.

예: 게시물의 모든 댓글 조회

```
use App\Models\Post;

$post = Post::find(1);

foreach ($post->comments as $comment) {
    //
}
```

다형 자식 모델의 부모 모델 조회:

```
use App\Models\Comment;

$comment = Comment::find(1);

$commentable = $comment->commentable;
```

`commentable` 관계는 `Post` 또는 `Video` 인스턴스를 반환합니다.

<a name="one-of-many-polymorphic-relations"></a>
### Has One Of Many (다형 관계)

여러 관련 모델 중에서 가장 최근 또는 가장 오래된 단일 모델을 쉽게 조회하고 싶을 때, `morphOne` 관계에 `ofMany` 메서드를 결합하여 사용합니다.

예:

```php
/**
 * 사용자의 최신 이미지
 */
public function latestImage()
{
    return $this->morphOne(Image::class, 'imageable')->latestOfMany();
}
```

가장 오래된 이미지 조회:

```php
/**
 * 사용자의 가장 오래된 이미지
 */
public function oldestImage()
{
    return $this->morphOne(Image::class, 'imageable')->oldestOfMany();
}
```

`ofMany`로 다른 정렬 기준을 지정하여, 가장 "좋아요"가 많은 이미지 조회 등도 가능합니다:

```php
/**
 * 사용자의 인기 이미지
 */
public function bestImage()
{
    return $this->morphOne(Image::class, 'imageable')->ofMany('likes', 'max');
}
```

> [!NOTE]
> 고급 설정법은 [Has One Of Many](#advanced-has-one-of-many-relationships) 문서도 참고하세요.

<a name="many-to-many-polymorphic-relations"></a>
### 다대다 (다형 관계)

<a name="many-to-many-polymorphic-table-structure"></a>
#### 테이블 구조

다대다 다형 관계는 다형 일대다/일대일보다 더 복잡할 수 있습니다.

예를 들어, `Post`와 `Video` 모델 모두 공통의 `Tag` 모델과 다대다 관계를 가진다고 가정합니다. 이런 경우, 단일 `tags` 테이블에서 고유한 태그를 관리하고, `taggables`라는 중간 테이블에서 다형 관계를 연결합니다.

테이블 예:

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
> 다형 다대다 관계를 이해하려면 기존 [다대다 관계](#many-to-many) 문서도 읽어보는 것이 도움됩니다.

<a name="many-to-many-polymorphic-model-structure"></a>
#### 모델 구조

관계 정의는 각각의 부모 모델(`Post`, `Video`)에 `morphToMany` 메서드를 사용합니다.

`morphToMany` 메서드는 관련 모델명과 "관계 이름"을 인자로 받는데, 이번 예에서는 중간 테이블명이 `taggables`이므로 관계 이름을 `taggable`로 지정해야 합니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Post extends Model
{
    /**
     * 게시물에 연결된 태그들을 반환
     */
    public function tags()
    {
        return $this->morphToMany(Tag::class, 'taggable');
    }
}
```

<a name="many-to-many-polymorphic-defining-the-inverse-of-the-relationship"></a>
#### 역관계 정의하기

`Tag` 모델에 각 부모 타입 별로 역관계 메서드를 정의합니다. 모두 `morphedByMany` 메서드를 사용합니다.

각 메서드에 관련 모델명과 다형 관계 이름(`taggable`)을 지정하세요:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Tag extends Model
{
    /**
     * 이 태그가 연결된 모든 게시물
     */
    public function posts()
    {
        return $this->morphedByMany(Post::class, 'taggable');
    }

    /**
     * 이 태그가 연결된 모든 동영상
     */
    public function videos()
    {
        return $this->morphedByMany(Video::class, 'taggable');
    }
}
```

<a name="many-to-many-polymorphic-retrieving-the-relationship"></a>
#### 관계 조회하기

관계가 정의된 후, 부모 모델에서 `tags` 동적 속성으로 태그를 조회할 수 있습니다:

```
use App\Models\Post;

$post = Post::find(1);

foreach ($post->tags as $tag) {
    //
}
```

다형 자식 모델에서 부모 모델에 접근할 경우, `morphedByMany` 메서드를 호출한 이름으로 접근합니다 (`posts`, `videos`):

```
use App\Models\Tag;

$tag = Tag::find(1);

foreach ($tag->posts as $post) {
    //
}

foreach ($tag->videos as $video) {
    //
}
```

<a name="custom-polymorphic-types"></a>
### 사용자 정의 다형 타입

기본적으로 Laravel은 다형 관계의 타입 컬럼에 부모 모델의 전면 네임스페이스 포함 클래스명을 저장합니다. (예: `App\Models\Post`)

하지만, 내부 구조와의 결합을 줄이기 위해 간단한 문자열(`post`, `video`)을 저장하는 것이 좋을 때가 있습니다.

이 경우 `Relation::enforceMorphMap` 메서드를 호출해 매핑을 정의하세요:

```
use Illuminate\Database\Eloquent\Relations\Relation;

Relation::enforceMorphMap([
    'post' => 'App\Models\Post',
    'video' => 'App\Models\Video',
]);
```

이 코드는 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에 넣거나 별도 서비스 프로바이더를 만들 수 있습니다.

런타임에 모델의 morph alias를 얻으려면 모델의 `getMorphClass` 메서드를 호출하고, morph alias로부터 클래스명을 얻으려면 `Relation::getMorphedModel`을 사용합니다:

```
use Illuminate\Database\Eloquent\Relations\Relation;

$alias = $post->getMorphClass();

$class = Relation::getMorphedModel($alias);
```

> [!WARNING]
> 기존 애플리케이션에 morph map을 추가할 때는, 기존 데이터베이스에 fully-qualified 클래스명이 저장된 `*_type` 컬럼 값을 매핑명으로 모두 변환해야 합니다.

<a name="dynamic-relationships"></a>
### 동적 관계

`resolveRelationUsing` 메서드를 사용해 런타임에 Eloquent 모델 사이 관계를 정의할 수 있습니다. 일반 앱 개발에는 권장되지 않지만, Laravel 패키지 개발 시 유용할 수 있습니다.

첫 번째 인자로 관계 이름, 두 번째 인자로 클로저를 줍니다. 클로저는 모델 인스턴스를 받고 유효한 Eloquent 관계를 정의해 반환해야 합니다.

보통 서비스 프로바이더의 `boot` 메서드 내에 설정합니다:

```
use App\Models\Order;
use App\Models\Customer;

Order::resolveRelationUsing('customer', function ($orderModel) {
    return $orderModel->belongsTo(Customer::class, 'customer_id');
});
```

> [!WARNING]
> 동적 관계 정의 시 관계 메서드에 명시적인 키 인자들을 항상 제공하세요.

<a name="querying-relations"></a>
## 관계 쿼리하기 (Querying Relations)

Eloquent 관계는 모두 메서드로 정의되므로, 이 메서드를 호출하면 관련 모델을 즉시 조회하지 않고 관계 자체 인스턴스를 얻을 수 있습니다.

또한 모든 관계는 [쿼리 빌더](/docs/9.x/queries) 역할을 하므로, 관계 쿼리에 조건을 추가할 수 있습니다.

예: `User` 모델이 다수의 `Post`를 가진다면 관계 정의는 다음과 같습니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 사용자의 모든 게시물을 가져옵니다.
     */
    public function posts()
    {
        return $this->hasMany(Post::class);
    }
}
```

```php
use App\Models\User;

$user = User::find(1);

$user->posts()->where('active', 1)->get();
```

쿼리 빌더 메서드를 관계에 적용할 수 있으니, 여러 메서드를 탐색해 활용하세요.

<a name="chaining-orwhere-clauses-after-relationships"></a>
#### 관계 후에 `orWhere` 체인 사용하기

아래처럼 `orWhere`를 관계 쿼리에 바로 체인할 때는 주의가 필요합니다. SQL에서는 `or` 조건이 관계 조건과 같은 레벨로 묶이기 때문에, 원치 않는 결과가 나올 수 있습니다:

```
$user->posts()
        ->where('active', 1)
        ->orWhere('votes', '>=', 100)
        ->get();
```

실제 생성되는 SQL:

```sql
select *
from posts
where user_id = ? and active = 1 or votes >= 100
```

이 쿼리는 `user_id` 제한 없이 votes가 100 이상인 모든 게시물을 반환할 수 있습니다.

이런 문제를 방지하려면 [논리 그룹핑](/docs/9.x/queries#logical-grouping) 기능을 사용해 조건을 괄호로 묶으세요:

```
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
### 관계 메서드와 동적 속성 차이

추가 조건 없이 단순히 관계 데이터를 조회할 때는, 관계를 마치 속성처럼 접근하는 동적 속성을 사용할 수 있습니다:

```
use App\Models\User;

$user = User::find(1);

foreach ($user->posts as $post) {
    //
}
```

동적 속성은 "지연 로딩"을 수행해, 실제 속성 접근 시에만 쿼리를 실행합니다.

따라서, 조회 후에 관계를 미리 불러야 할 때는 [즉시 로딩](#eager-loading)을 사용하는 편이 성능에 좋습니다.

<a name="querying-relationship-existence"></a>
### 관계 존재 여부 쿼리하기

모델 조회시 특정 관계 존재 여부에 따라 결과를 제한할 수 있습니다. 예를 들어, 적어도 하나 이상의 댓글이 있는 게시물만 조회하려면 `has`, `orHas` 메서드를 사용합니다:

```
use App\Models\Post;

// 댓글이 하나 이상 있는 게시물 조회
$posts = Post::has('comments')->get();
```

비교 연산자와 개수도 지정 가능:

```php
// 댓글이 3개 이상인 게시물 조회
$posts = Post::has('comments', '>=', 3)->get();
```

중첩 관계도 "점(dot)" 표기법으로 지정:

```php
// 댓글 중 이미지가 하나 이상 있는 게시물 조회
$posts = Post::has('comments.images')->get();
```

더 복잡한 조건이 필요하다면 `whereHas`, `orWhereHas` 메서드를 이용해 쿼리 제약을 추가할 수 있습니다:

```
use Illuminate\Database\Eloquent\Builder;

// 내용에 code% 가 포함된 댓글을 가진 게시물 조회
$posts = Post::whereHas('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
})->get();

// 내용에 code% 포함된 댓글이 10개 이상인 게시물 조회
$posts = Post::whereHas('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
}, '>=', 10)->get();
```

> [!WARNING]
> 현재 Eloquent는 데이터베이스가 다른 경우 관계 존재 여부 쿼리를 지원하지 않습니다. 같은 데이터베이스 안에 있어야 합니다.

<a name="inline-relationship-existence-queries"></a>
#### 간단한 관계 존재 여부 쿼리

한 가지 단순 조건으로 관계 존재를 쿼리할 때 `whereRelation`, `orWhereRelation`, `whereMorphRelation`, `orWhereMorphRelation` 메서드를 활용할 수 있습니다.

예: 승인되지 않은 댓글이 있는 게시물 조회

```
use App\Models\Post;

$posts = Post::whereRelation('comments', 'is_approved', false)->get();
```

연산자도 지정 가능합니다:

```
$posts = Post::whereRelation(
    'comments', 'created_at', '>=', now()->subHour()
)->get();
```

<a name="querying-relationship-absence"></a>
### 관계 부재 여부 쿼리하기

관계가 없는 경우로 결과를 제한하려면 `doesntHave` 및 `orDoesntHave` 메서드를 사용하세요.

예: 댓글이 하나도 없는 게시물 조회

```
use App\Models\Post;

$posts = Post::doesntHave('comments')->get();
```

더 복잡한 제약은 `whereDoesntHave`, `orWhereDoesntHave`로 가능합니다:

```
use Illuminate\Database\Eloquent\Builder;

$posts = Post::whereDoesntHave('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
})->get();
```

중첩 관계에도 점 표기법 사용 가능:

```
use Illuminate\Database\Eloquent\Builder;

$posts = Post::whereDoesntHave('comments.author', function (Builder $query) {
    $query->where('banned', 0);
})->get();
```

<a name="querying-morph-to-relationships"></a>
### Morph To 관계 쿼리하기

다형 관계의 존재 여부 쿼리는 `whereHasMorph`, `whereDoesntHaveMorph` 메서드가 지원합니다.

인자는 관계명, 관련 모델 클래스 배열, 그리고 관계 쿼리를 수정할 클로저입니다:

```
use App\Models\Comment;
use App\Models\Post;
use App\Models\Video;
use Illuminate\Database\Eloquent\Builder;

// 게시물 또는 동영상과 연결된 댓글 with 타이틀이 'code%'인 경우
$comments = Comment::whereHasMorph(
    'commentable',
    [Post::class, Video::class],
    function (Builder $query) {
        $query->where('title', 'like', 'code%');
    }
)->get();

// 게시물과 연결된 댓글 중 타이틀이 'code%'인 경우가 없는 댓글 조회
$comments = Comment::whereDoesntHaveMorph(
    'commentable',
    Post::class,
    function (Builder $query) {
        $query->where('title', 'like', 'code%');
    }
)->get();
```

쿼리를 작성하는 동안 대상 모델 타입을 확인하려면 클로저 두 번째 인자를 사용하세요:

```
use Illuminate\Database\Eloquent\Builder;

$comments = Comment::whereHasMorph(
    'commentable',
    [Post::class, Video::class],
    function (Builder $query, $type) {
        $column = $type === Post::class ? 'content' : 'title';

        $query->where($column, 'like', 'code%');
    }
)->get();
```

<a name="querying-all-morph-to-related-models"></a>
#### 모든 관련 모델 조회

관련 모델 배열 대신 와일드카드 `*`를 지정하면 데이터베이스에 있는 모든 관련 다형 타입에 대해 쿼리합니다 (한 번 더 쿼리를 실행함):

```
use Illuminate\Database\Eloquent\Builder;

$comments = Comment::whereHasMorph('commentable', '*', function (Builder $query) {
    $query->where('title', 'like', 'foo%');
})->get();
```

<a name="aggregating-related-models"></a>
## 관련 모델 집계 (Aggregating Related Models)

<a name="counting-related-models"></a>
### 관계된 모델 개수 세기

관계된 모델을 직접 로딩하지 않고 개수만 조회하고 싶을 때 `withCount` 메서드를 사용합니다. 이 메서드는 아래와 같은 이름의 카운트 속성을 자동 추가합니다: `{relation}_count`

```
use App\Models\Post;

$posts = Post::withCount('comments')->get();

foreach ($posts as $post) {
    echo $post->comments_count;
}
```

복수 관계와 조건을 배열로 넘길 수 있습니다:

```
use Illuminate\Database\Eloquent\Builder;

$posts = Post::withCount(['votes', 'comments' => function (Builder $query) {
    $query->where('content', 'like', 'code%');
}])->get();

echo $posts[0]->votes_count;
echo $posts[0]->comments_count;
```

별칭(alias)을 지정해 같은 관계 개수를 여러 개 조회할 수도 있습니다:

```
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
#### 지연 개수 로딩

`loadCount` 메서드를 사용하면 이미 조회한 모델에 관계 개수를 나중에 추가 로딩할 수 있습니다:

```
$book = Book::first();

$book->loadCount('genres');
```

조건도 배열과 클로저로 지정 가능:

```
$book->loadCount(['reviews' => function ($query) {
    $query->where('rating', 5);
}]);
```

<a name="relationship-counting-and-custom-select-statements"></a>
#### 집계와 커스텀 SELECT 구문

`withCount`를 `select` 구문과 조합할 때는 `withCount`를 `select` 이후에 호출하세요:

```
$posts = Post::select(['title', 'body'])
                ->withCount('comments')
                ->get();
```

<a name="other-aggregate-functions"></a>
### 기타 집계 함수

`withCount` 외에 `withMin`, `withMax`, `withAvg`, `withSum`, `withExists` 도 지원합니다. 결과 모델에 `{relation}_{function}_{column}` 형태 속성이 추가됩니다:

```
use App\Models\Post;

$posts = Post::withSum('comments', 'votes')->get();

foreach ($posts as $post) {
    echo $post->comments_sum_votes;
}
```

별칭도 가능합니다:

```
$posts = Post::withSum('comments as total_comments', 'votes')->get();

foreach ($posts as $post) {
    echo $post->total_comments;
}
```

지연 로딩 버전도 있습니다:

```
$post = Post::first();

$post->loadSum('comments', 'votes');
```

`select` 구문과 조합 시도 `withSum`, `withExists` 등은 `select` 뒤에 호출하세요:

```
$posts = Post::select(['title', 'body'])
                ->withExists('comments')
                ->get();
```

<a name="counting-related-models-on-morph-to-relationships"></a>
### Morph To 관계 관련 모델 개수 세기

`morphTo` 관계와 관련된 모델별로 카운트를 함께 로딩하려면 `with`와 `morphWithCount` 메서드를 조합합니다.

예: `ActivityFeed` 모델이 `parentable`이라는 `morphTo` 관계를 가지며, `Photo`와 `Post`가 있을 때, `Photo`는 `tags`가 있고 `Post`는 `comments`가 있다고 하면:

```
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
#### 지연 로딩 후 Morph To 집계

이미 모델을 로드한 후 관련 모델별 카운트를 넣고 싶을 때는 `loadMorphCount` 사용:

```
$activities = ActivityFeed::with('parentable')->get();

$activities->loadMorphCount('parentable', [
    Photo::class => ['tags'],
    Post::class => ['comments'],
]);
```

<a name="eager-loading"></a>
## 즉시 로딩 (Eager Loading)

Eloquent 관계를 속성 형태로 접근하면 "지연 로딩"하여 최초 접근 시점에 관계 데이터를 쿼리합니다.

즉시 로딩은 모델 조회 시점에 관계 데이터를 미리 로드하여, 반복 쿼리가 발생하는 "N + 1 문제"를 완화합니다.

예: `Book` 모델이 `Author` 모델에 속하는 관계를 갖는다고 할 때,

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Book extends Model
{
    /**
     * 저자를 반환
     */
    public function author()
    {
        return $this->belongsTo(Author::class);
    }
}
```

모든 책과 책의 저자를 조회할 때 기본 쿼리는 다음과 같이 N + 1 개 쿼리를 발생시킵니다:

```
use App\Models\Book;

$books = Book::all();

foreach ($books as $book) {
    echo $book->author->name;
}
```

25권이면 책 1회, 저자 25회 총 26회 쿼리가 실행됩니다.

하지만 `with` 메서드를 사용해 즉시 로딩하면 총 2개의 쿼리만 실행됩니다:

```
$books = Book::with('author')->get();

foreach ($books as $book) {
    echo $book->author->name;
}
```

실제 쿼리:

```sql
select * from books;

select * from authors where id in (1, 2, 3, 4, 5, ...);
```

<a name="eager-loading-multiple-relationships"></a>
#### 여러 관계 즉시 로딩

복수의 관계를 즉시 로딩 하려면 `with` 메서드에 관계 배열을 넘기면 됩니다:

```
$books = Book::with(['author', 'publisher'])->get();
```

<a name="nested-eager-loading"></a>
#### 중첩 즉시 로딩

관계에 연결된 다른 관계도 즉시 로딩하려면 "점(dot)" 구문을 사용합니다:

```
$books = Book::with('author.contacts')->get();
```

여러 중첩 관계는 배열로도 표현할 수 있습니다:

```
$books = Book::with([
    'author' => [
        'contacts',
        'publisher',
    ],
])->get();
```

<a name="nested-eager-loading-morphto-relationships"></a>
#### 다형 관계(morphTo) 중첩 즉시 로딩

`morphTo` 관계 및 반환되는 다양한 타입의 모델 관계까지 즉시 로딩하려면 `morphWith` 메서드를 사용합니다:

```
<?php

use Illuminate\Database\Eloquent\Model;

class ActivityFeed extends Model
{
    /**
     * 활동 기록의 부모 반환
     */
    public function parentable()
    {
        return $this->morphTo();
    }
}
```

`Event`, `Photo`, `Post` 모델이 각각 `ActivityFeed` 모델과 관계를 가진 상황에서, 각자의 연관 관계까지 모두 즉시 로딩:

```
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

필요한 컬럼만 지정해 즉시 로딩할 수 있습니다:

```
$books = Book::with('author:id,name,book_id')->get();
```

> [!WARNING]
> 이 기능 사용 시에는 항상 기본 키(`id`)와 외래 키 컬럼을 포함해야 합니다.

<a name="eager-loading-by-default"></a>
#### 기본 즉시 로딩 설정하기

항상 특정 관계를 즉시 로딩하고 싶다면 모델 안에 `$with` 속성으로 지정할 수 있습니다:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Book extends Model
{
    /**
     * 항상 로드할 관계 배열
     *
     * @var array
     */
    protected $with = ['author'];

    public function author()
    {
        return $this->belongsTo(Author::class);
    }

    public function genre()
    {
        return $this->belongsTo(Genre::class);
    }
}
```

쿼리에서 `$with` 관계를 뺄 때는 `without` 메서드를 씁니다:

```
$books = Book::without('author')->get();
```

모든 `$with` 관계를 대체하려면 `withOnly` 메서드를 사용하세요:

```
$books = Book::withOnly('genre')->get();
```

<a name="constraining-eager-loads"></a>
### 즉시 로딩 제약 조건 지정하기

즉시 로딩 시 추가 조건을 붙이고 싶으면, 관계명을 키로 하고 조건을 명시한 클로저를 값으로 갖는 배열을 `with` 메서드에 전달하세요:

```
use App\Models\User;

$users = User::with(['posts' => function ($query) {
    $query->where('title', 'like', '%code%');
}])->get();
```

기타 쿼리 빌더 메서드도 쓸 수 있습니다:

```
$users = User::with(['posts' => function ($query) {
    $query->orderBy('created_at', 'desc');
}])->get();
```

> [!WARNING]
> 제약 조건에 `limit` 또는 `take` 메서드는 사용할 수 없습니다.

<a name="constraining-eager-loading-of-morph-to-relationships"></a>
#### 다형 관계 즉시 로딩 제약 조건

`morphTo` 관계 즉시 로딩 시 반환되는 각 타입별 모델을 조건에 맞게 필터링하려면, `MorphTo` 관계의 `constrain` 메서드를 이용하세요:

```
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Relations\MorphTo;

$comments = Comment::with(['commentable' => function (MorphTo $morphTo) {
    $morphTo->constrain([
        Post::class => function (Builder $query) {
            $query->whereNull('hidden_at');
        },
        Video::class => function (Builder $query) {
            $query->where('type', 'educational');
        },
    ]);
}])->get();
```

위 예제는 숨긴 게시물은 제외하고, 유형이 `educational`인 동영상만 불러옵니다.

<a name="constraining-eager-loads-with-relationship-existence"></a>
#### 관계 존재 조건과 함께 즉시 로딩 제약 지정

예: `User` 모델 중에서 특정 조건을 만족하는 게시물이 있는 사용자만 조회하고, 그 게시물 역시 즉시 로딩하려면 `withWhereHas`가 편리합니다:

```
use App\Models\User;

$users = User::withWhereHas('posts', function ($query) {
    $query->where('featured', true);
})->get();
```

<a name="lazy-eager-loading"></a>
### 지연 즉시 로딩 (Lazy Eager Loading)

이미 부모 모델을 로드한 뒤에 조건에 따라 관계를 즉시 로딩해야 할 때가 있습니다:

```
use App\Models\Book;

$books = Book::all();

if ($someCondition) {
    $books->load('author', 'publisher');
}
```

조건을 넣으려면 클로저 배열을 넘기면 됩니다:

```
$author->load(['books' => function ($query) {
    $query->orderBy('published_date', 'asc');
}]);
```

이미 로드된 관계만 대상으로 즉시 로딩하려면 `loadMissing` 메서드를 사용하세요:

```
$book->loadMissing('author');
```

<a name="nested-lazy-eager-loading-morphto"></a>
#### 다형 관계 및 중첩 지연 즉시 로딩

`loadMorph` 메서드는 다형 관계 이름과 모델별 관계 배열을 받아, 해당 관계들을 지연 즉시 로딩합니다.

```
<?php

use Illuminate\Database\Eloquent\Model;

class ActivityFeed extends Model
{
    /**
     * 활동 기록의 부모
     */
    public function parentable()
    {
        return $this->morphTo();
    }
}
```

예: `Event`, `Photo`, `Post` 모델이 각각 속하는 하위 관계를 포함해 모두 지연 즉시 로딩:

```
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

관계 지연 로딩은 성능 저하를 일으키는 경우가 많아, 애플리케이션에서 지연 로딩을 항상 막고 싶다면 Eloquent의 `preventLazyLoading` 메서드를 호출하세요. 보통 `AppServiceProvider`의 `boot` 메서드 안에서 호출합니다.

`preventLazyLoading`은 불리언 인자를 받아, 환경에 따라 지연 로딩 허용 여부도 변경할 수 있습니다:

```php
use Illuminate\Database\Eloquent\Model;

/**
 * 애플리케이션 서비스 부트스트랩
 *
 * @return void
 */
public function boot()
{
    Model::preventLazyLoading(! $this->app->isProduction());
}
```

이 설정 이후 지연 로딩이 시도되면 `Illuminate\Database\LazyLoadingViolationException` 예외가 발생합니다.

예외 발생 대신 로그만 남기고 싶다면 `handleLazyLoadingViolationsUsing` 메서드를 사용하여 동작 방식을 커스터마이징할 수 있습니다:

```php
Model::handleLazyLoadingViolationUsing(function ($model, $relation) {
    $class = get_class($model);

    info("Attempted to lazy load [{$relation}] on model [{$class}].");
});
```

<a name="inserting-and-updating-related-models"></a>
## 관련 모델 삽입 및 업데이트

<a name="the-save-method"></a>
### `save` 메서드

Eloquent는 관계에 새 모델을 간편하게 추가하는 메서드를 제공합니다.

예: 게시물에 새 댓글을 추가할 때, 댓글의 `post_id`를 직접 설정하지 않고 `save` 메서드 사용할 수 있습니다:

```
use App\Models\Comment;
use App\Models\Post;

$comment = new Comment(['message' => 'A new comment.']);

$post = Post::find(1);

$post->comments()->save($comment);
```

`comments`를 동적 속성이 아니라 메서드로 접근해야 `Relationship` 인스턴스를 얻어서 `save`를 사용할 수 있습니다.

여러 모델 저장은 `saveMany`를 이용:

```
$post = Post::find(1);

$post->comments()->saveMany([
    new Comment(['message' => 'A new comment.']),
    new Comment(['message' => 'Another new comment.']),
]);
```

`save`와 `saveMany`는 DB에 모델을 저장하지만, 이미 로드된 메모리 내 관계에는 새로 저장한 모델을 추가하지 않습니다. 관계를 재조회할 때는 `refresh`를 호출하세요:

```
$post->comments()->save($comment);

$post->refresh();

// 새 댓글 포함 모든 댓글 조회
$post->comments;
```

<a name="the-push-method"></a>
#### 모델과 자식 관계를 재귀적으로 저장하기

`push` 메서드는 모델과 모든 연관된 관계 모델을 재귀적으로 저장합니다:

```
$post = Post::find(1);

$post->comments[0]->message = 'Message';
$post->comments[0]->author->name = 'Author Name';

$post->push();
```

`pushQuietly`는 이벤트를 발생시키지 않고 저장합니다:

```
$post->pushQuietly();
```

<a name="the-create-method"></a>
### `create` 메서드

`save` 메서드와 달리, `create`는 속성 배열을 받아 새 모델을 생성하고 저장하며 새 모델 인스턴스를 반환합니다:

```
use App\Models\Post;

$post = Post::find(1);

$comment = $post->comments()->create([
    'message' => 'A new comment.',
]);
```

여러 모델 생성은 `createMany`를 사용합니다:

```
$post = Post::find(1);

$post->comments()->createMany([
    ['message' => 'A new comment.'],
    ['message' => 'Another new comment.'],
]);
```

`findOrNew`, `firstOrNew`, `firstOrCreate`, `updateOrCreate` 등도 관계에서 사용할 수 있습니다.

> [!NOTE]
> `create` 메서드 사용 전에는 반드시 [대량 할당 (mass assignment)](/docs/9.x/eloquent#mass-assignment) 관련 내용을 확인하세요.

<a name="updating-belongs-to-relationships"></a>
### belongsTo 관계 업데이트하기

자식 모델에 새로운 부모 모델을 연결하려면 `associate` 메서드를 사용합니다.

예: `User` 모델이 `Account`에 속하는 경우,

```
use App\Models\Account;

$account = Account::find(10);

$user->account()->associate($account);

$user->save();
```

부모 모델 연결을 제거하려면 `dissociate`를 사용하세요. 이렇게 하면 외래 키가 `null`로 설정됩니다:

```
$user->account()->dissociate();

$user->save();
```

<a name="updating-many-to-many-relationships"></a>
### 다대다 관계 업데이트하기

<a name="attaching-detaching"></a>
#### 관계 연결 및 해제

다대다 관계에 연결하거나 해제하는 편리한 메서드가 있습니다.

예: 사용자에 역할을 연결하려면 `attach` 메서드 사용:

```
use App\Models\User;

$user = User::find(1);

$user->roles()->attach($roleId);
```

추가로 중간 테이블에 데이터를 넣고 싶으면 두 번째 인자를 배열로 전달:

```
$user->roles()->attach($roleId, ['expires' => $expires]);
```

역으로 관계 해제는 `detach` 메서드를 사용합니다:

```
// 특정 역할 해제
$user->roles()->detach($roleId);

// 모든 역할 해제
$user->roles()->detach();
```

`attach`와 `detach` 모두 배열 인자도 지원:

```
$user = User::find(1);

$user->roles()->detach([1, 2, 3]);

$user->roles()->attach([
    1 => ['expires' => $expires],
    2 => ['expires' => $expires],
]);
```

<a name="syncing-associations"></a>
#### 관계 동기화

`sync` 메서드는 주어진 ID 배열만 중간 테이블에 남기고, 나머지는 삭제하는 동기화 기능입니다:

```
$user->roles()->sync([1, 2, 3]);
```

추가 중간 테이블 값도 지정 가능:

```
$user->roles()->sync([1 => ['expires' => true], 2, 3]);
```

동일한 중간 테이블 값을 여러 ID에 일괄 지정하려면 `syncWithPivotValues` 사용:

```
$user->roles()->syncWithPivotValues([1, 2, 3], ['active' => true]);
```

누락된 ID도 해제하지 않고 추가하려면 `syncWithoutDetaching` 사용:

```
$user->roles()->syncWithoutDetaching([1, 2, 3]);
```

<a name="toggling-associations"></a>
#### 관계 토글

`toggle` 메서드는 지정된 ID가 현재 연결 상태면 해제하고, 해제 상태면 연결합니다:

```
$user->roles()->toggle([1, 2, 3]);
```

ID별 추가 중간 테이블 값도 전달 가능:

```
$user->roles()->toggle([
    1 => ['expires' => true],
    2 => ['expires' => true],
]);
```

<a name="updating-a-record-on-the-intermediate-table"></a>
#### 중간 테이블 레코드 갱신하기

중간 테이블의 특정 레코드를 업데이트하려면 `updateExistingPivot` 메서드를 사용합니다:

```
$user = User::find(1);

$user->roles()->updateExistingPivot($roleId, [
    'active' => false,
]);
```

<a name="touching-parent-timestamps"></a>
## 부모 타임스탬프 터치하기

`belongsTo` 또는 `belongsToMany` 관계에서 자식 모델이 업데이트 될 때, 부모 모델의 `updated_at` 타임스탬프를 같이 갱신할 수 있습니다.

예: 댓글이 갱신되면 소유 게시물의 `updated_at`도 같이 갱신하도록 하려면, 자식 모델에 `$touches` 배열로 관계명을 지정하세요:

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Comment extends Model
{
    /**
     * 업데이트 되는 관계 이름 배열
     *
     * @var array
     */
    protected $touches = ['post'];

    /**
     * 댓글의 소유 게시물을 가져옵니다.
     */
    public function post()
    {
        return $this->belongsTo(Post::class);
    }
}
```

> [!WARNING]
> 부모 모델의 타임스탬프는 자식 모델을 Eloquent `save` 메서드로 저장할 때만 자동 갱신됩니다.