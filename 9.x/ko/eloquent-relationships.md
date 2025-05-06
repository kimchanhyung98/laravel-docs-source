# Eloquent: 관계

- [소개](#introduction)
- [관계 정의하기](#defining-relationships)
    - [일대일(One To One)](#one-to-one)
    - [일대다(One To Many)](#one-to-many)
    - [일대다(역방향) / Belongs To](#one-to-many-inverse)
    - [Has One Of Many](#has-one-of-many)
    - [Has One Through](#has-one-through)
    - [Has Many Through](#has-many-through)
- [다대다(Many To Many) 관계](#many-to-many)
    - [중간 테이블 컬럼 조회](#retrieving-intermediate-table-columns)
    - [중간 테이블 컬럼을 통한 쿼리 필터링](#filtering-queries-via-intermediate-table-columns)
    - [중간 테이블 컬럼을 통한 쿼리 정렬](#ordering-queries-via-intermediate-table-columns)
    - [커스텀 중간 테이블 모델 정의](#defining-custom-intermediate-table-models)
- [폴리모픽(Polymorphic) 관계](#polymorphic-relationships)
    - [일대일](#one-to-one-polymorphic-relations)
    - [일대다](#one-to-many-polymorphic-relations)
    - [One Of Many](#one-of-many-polymorphic-relations)
    - [다대다](#many-to-many-polymorphic-relations)
    - [커스텀 폴리모픽 타입](#custom-polymorphic-types)
- [동적 관계](#dynamic-relationships)
- [관계 쿼리하기](#querying-relations)
    - [관계 메서드 vs 동적 프로퍼티](#relationship-methods-vs-dynamic-properties)
    - [관계 존재 쿼리](#querying-relationship-existence)
    - [관계 부재 쿼리](#querying-relationship-absence)
    - [Morph To 관계 쿼리](#querying-morph-to-relationships)
- [관련 모델 집계](#aggregating-related-models)
    - [관련 모델 개수 카운팅](#counting-related-models)
    - [기타 집계 함수](#other-aggregate-functions)
    - [Morph To 관계의 관련 모델 개수 카운팅](#counting-related-models-on-morph-to-relationships)
- [즉시 로딩(Eager Loading)](#eager-loading)
    - [즉시 로딩 제약](#constraining-eager-loads)
    - [지연 즉시 로딩](#lazy-eager-loading)
    - [지연 로딩 비활성화](#preventing-lazy-loading)
- [관계된 모델 삽입 & 갱신](#inserting-and-updating-related-models)
    - [`save` 메서드](#the-save-method)
    - [`create` 메서드](#the-create-method)
    - [Belongs To 관계](#updating-belongs-to-relationships)
    - [Many To Many 관계](#updating-many-to-many-relationships)
- [부모 타임스탬프 갱신(Touching Parent Timestamps)](#touching-parent-timestamps)

<a name="introduction"></a>
## 소개

데이터베이스 테이블은 종종 서로 관련되어 있습니다. 예를 들어, 블로그 글은 여러 개의 댓글을 가질 수 있고, 주문은 주문을 등록한 사용자와 관련될 수 있습니다. Eloquent는 이러한 관계를 쉽게 관리하고 작업할 수 있도록 하며, 다양한 흔한 관계 타입을 지원합니다:

<div class="content-list" markdown="1">

- [일대일(One To One)](#one-to-one)
- [일대다(One To Many)](#one-to-many)
- [다대다(Many To Many)](#many-to-many)
- [Has One Through](#has-one-through)
- [Has Many Through](#has-many-through)
- [일대일(Polymorphic)](#one-to-one-polymorphic-relations)
- [일대다(Polymorphic)](#one-to-many-polymorphic-relations)
- [다대다(Polymorphic)](#many-to-many-polymorphic-relations)

</div>

<a name="defining-relationships"></a>
## 관계 정의하기

Eloquent 관계는 Eloquent 모델 클래스의 메서드로 정의됩니다. 관계 또한 강력한 [쿼리 빌더](/docs/{{version}}/queries) 역할을 하므로, 관계를 메서드로 정의하면 체이닝 등 강력한 쿼리 기능을 사용할 수 있습니다. 예를 들어, `posts` 관계에 추가 쿼리 제약을 쉽게 체이닝할 수 있습니다:

```php
$user->posts()->where('active', 1)->get();
```

본격적으로 관계를 사용하기 전에, Eloquent가 지원하는 각 관계 타입을 어떻게 정의하는지부터 살펴봅시다.

<a name="one-to-one"></a>
### 일대일(One To One)

일대일 관계는 가장 기본적인 데이터베이스 관계입니다. 예를 들어, `User` 모델은 하나의 `Phone` 모델과 관련될 수 있습니다. 이 관계를 정의하려면 `User` 모델에 `phone` 메서드를 추가하고, 이 메서드에서 `hasOne` 메서드를 호출하여 그 결과를 반환해야 합니다. `hasOne` 메서드는 모델의 `Illuminate\Database\Eloquent\Model` 기반에서 제공합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 사용자와 연결된 전화번호 반환
     */
    public function phone()
    {
        return $this->hasOne(Phone::class);
    }
}
```

`hasOne` 메서드의 첫 번째 인자는 연관된 모델 클래스 이름입니다. 일단 관계가 정의되면, Eloquent의 동적 프로퍼티를 사용해 연관된 레코드를 조회할 수 있습니다. 동적 프로퍼티를 사용하면 관계 메서드를 모델의 프로퍼티처럼 접근할 수 있습니다:

```php
$phone = User::find(1)->phone;
```

Eloquent는 부모 모델 이름을 통해 외래키를 추론합니다. 이 예에서는 `Phone` 모델에 자동으로 `user_id` 외래키가 있다고 가정합니다. 관례를 변경하고 싶으면 두 번째 인자를 `hasOne` 메서드에 전달하면 됩니다:

```php
return $this->hasOne(Phone::class, 'foreign_key');
```

또한, Eloquent는 외래키 값이 부모 모델의 기본키(primary key) 컬럼 값과 일치한다고 가정합니다. 즉, `Phone` 레코드의 `user_id` 컬럼 값이 사용자의 `id` 컬럼 값과 일치해야 합니다. 만약 `id`나 `$primaryKey`가 아닌 다른 컬럼을 사용하고 싶다면, 세 번째 인자를 사용할 수 있습니다:

```php
return $this->hasOne(Phone::class, 'foreign_key', 'local_key');
```

<a name="one-to-one-defining-the-inverse-of-the-relationship"></a>
#### 관계의 역방향(Inverse) 정의

이제 `User` 모델에서 `Phone` 모델을 접근할 수 있습니다. 다음은 `Phone` 모델에 사용자를 접근할 수 있는 관계를 정의합니다. `hasOne`의 역관계는 `belongsTo` 메서드를 통해 정의합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Phone extends Model
{
    /**
     * 이 전화번호를 소유한 사용자 반환
     */
    public function user()
    {
        return $this->belongsTo(User::class);
    }
}
```

`user` 메서드를 호출하면, Eloquent는 `Phone` 모델의 `user_id` 컬럼과 일치하는 `User` 모델의 `id` 값을 찾아 반환합니다.

Eloquent는 관계 메서드 이름 뒤에 `_id`를 붙여서 기본 외래키 이름을 추론합니다. 이 경우, `Phone` 모델에 `user_id` 컬럼이 있다고 가정합니다. 만약 외래키가 다르다면, 두 번째 인자로 직접 지정할 수 있습니다:

```php
public function user()
{
    return $this->belongsTo(User::class, 'foreign_key');
}
```

부모 모델이 기본키로 `id` 컬럼을 사용하지 않거나, 연결 모델을 다른 컬럼으로 찾고 싶다면, 세 번째 인자로 부모 테이블의 커스텀 키를 지정할 수 있습니다:

```php
public function user()
{
    return $this->belongsTo(User::class, 'foreign_key', 'owner_key');
}
```

<a name="one-to-many"></a>
### 일대다(One To Many)

일대다 관계는 하나의 모델이 여러 하위 모델의 부모가 되는 관계입니다. 예를 들어, 블로그 글은 무한대로 많은 댓글을 가질 수 있습니다. 일대다 관계는 모델에 메서드로 아래와 같이 정의합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Post extends Model
{
    /**
     * 블로그 포스트의 댓글을 모두 반환
     */
    public function comments()
    {
        return $this->hasMany(Comment::class);
    }
}
```

Eloquent는 `Comment` 모델의 적절한 외래키 컬럼을 자동으로 결정합니다. 관례상, 부모 모델의 이름을 snake case로 변환하고 `_id`를 붙입니다. 이 예에서는, `Comment` 모델의 외래키 컬럼이 `post_id`라고 가정합니다.

관계 메서드를 정의했다면, `comments` 프로퍼티에 접근해서 [컬렉션](/docs/{{version}}/eloquent-collections) 형태로 댓글들을 가져올 수 있습니다. 동적 관계 프로퍼티로 아래와 같이 접근 가능합니다:

```php
use App\Models\Post;

$comments = Post::find(1)->comments;

foreach ($comments as $comment) {
    //
}
```

관계 또한 쿼리 빌더 역할을 하므로, 추가 제약 조건을 체이닝할 수 있습니다:

```php
$comment = Post::find(1)->comments()
                    ->where('title', 'foo')
                    ->first();
```

`hasOne`과 마찬가지로, 외래키와 로컬키를 추가 인자로 지정할 수 있습니다:

```php
return $this->hasMany(Comment::class, 'foreign_key');

return $this->hasMany(Comment::class, 'foreign_key', 'local_key');
```

<a name="one-to-many-inverse"></a>
### 일대다(역방향) / Belongs To

이제 포스트의 모든 댓글에 접근할 수 있습니다. 반대로, 댓글에서 부모 포스트에 접근하려면 자식 모델에 `belongsTo` 메서드로 관계를 정의하면 됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Comment extends Model
{
    /**
     * 댓글이 속한 포스트 반환
     */
    public function post()
    {
        return $this->belongsTo(Post::class);
    }
}
```

이제 댓글의 부모 포스트는 `post`라는 동적 관계 프로퍼티로 접근할 수 있습니다:

```php
use App\Models\Comment;

$comment = Comment::find(1);

return $comment->post->title;
```

위 예시에서, Eloquent는 `Comment` 모델의 `post_id`와 일치하는 `Post` 모델의 `id` 값을 찾습니다.

Eloquent는 기본적으로 관계 메서드 이름 뒤에 부모 모델의 기본키 컬럼명을 붙여서 외래키 이름을 추정합니다. 예제에서는 `comments` 테이블에 `post_id` 컬럼을 사용합니다.

관례를 따르지 않는 경우, `belongsTo` 메서드에 두 번째 인자로 외래키 이름을 지정할 수 있습니다:

```php
public function post()
{
    return $this->belongsTo(Post::class, 'foreign_key');
}
```

또한, 부모 모델의 기본키가 `id`가 아니거나, 맞춤 컬럼을 사용하려면 세 번째 인자로 지정할 수 있습니다:

```php
public function post()
{
    return $this->belongsTo(Post::class, 'foreign_key', 'owner_key');
}
```

<a name="default-models"></a>
#### 기본 모델(Default Model) 지정

`belongsTo`, `hasOne`, `hasOneThrough`, `morphOne` 관계에서는 관계가 `null`일 경우 반환할 기본 모델을 정의할 수 있습니다. 이 패턴은 [Null Object 패턴](https://en.wikipedia.org/wiki/Null_Object_pattern)이라 부르며, 코드에서 조건 검사를 줄여줄 수 있습니다. 예를 들어, 포스트의 `user` 관계에 연결된 사용자가 없다면 빈 `App\Models\User` 모델을 반환합니다:

```php
public function user()
{
    return $this->belongsTo(User::class)->withDefault();
}
```

기본 모델에 속성을 할당하려면 배열이나 클로저를 `withDefault`에 전달할 수 있습니다:

```php
public function user()
{
    return $this->belongsTo(User::class)->withDefault([
        'name' => 'Guest Author',
    ]);
}
```

클로저 예시도 가능합니다:

```php
public function user()
{
    return $this->belongsTo(User::class)->withDefault(function ($user, $post) {
        $user->name = 'Guest Author';
    });
}
```

<a name="querying-belongs-to-relationships"></a>
#### Belongs To 관계 쿼리하기

"Belongs To" 관계의 자식 모델을 조회할 때, `where` 절로 직접 Eloquent 모델을 조회할 수 있습니다:

```php
use App\Models\Post;

$posts = Post::where('user_id', $user->id)->get();
```

좀 더 간편하게 `whereBelongsTo` 메서드를 사용할 수도 있습니다:

```php
$posts = Post::whereBelongsTo($user)->get();
```

[컬렉션](/docs/{{version}}/eloquent-collections) 인스턴스를 넘길 수도 있습니다. 이 경우, 컬렉션 내 여러 사용자에 속한 포스트를 모두 조회합니다:

```php
$users = User::where('vip', true)->get();

$posts = Post::whereBelongsTo($users)->get();
```

Laravel은 기본적으로 모델 클래스명으로 관계명을 추론하지만, 두 번째 인자로 수동 지정할 수도 있습니다:

```php
$posts = Post::whereBelongsTo($user, 'author')->get();
```

<a name="has-one-of-many"></a>
### Has One Of Many

하나의 모델이 여러 관계 모델을 가질 수 있지만, "최신" 또는 "가장 오래된" 하나의 관계 모델만 쉽게 조회하고 싶을 때가 있습니다. 예를 들면, `User` 모델이 여러 개의 `Order`와 관계되어 있지만, 사용자가 가장 최근에 주문한 Order를 가져오고 싶을 때입니다. `hasOne`과 `ofMany`를 조합해서 쉽게 구현할 수 있습니다:

```php
/**
 * 사용자의 최근 주문 반환
 */
public function latestOrder()
{
    return $this->hasOne(Order::class)->latestOfMany();
}
```

가장 오래된(첫 번째) 주문을 가져오는 방법도 유사합니다:

```php
/**
 * 사용자의 가장 오래된 주문 반환
 */
public function oldestOrder()
{
    return $this->hasOne(Order::class)->oldestOfMany();
}
```

기본적으로는 기본키로 정렬하여 최신/오래된 모델을 찾지만, 다른 기준 컬럼으로 정렬하고 싶으면 `ofMany` 메서드를 사용할 수 있습니다. 예를 들어, 가장 비싼 주문을 가져오는 경우:

```php
/**
 * 사용자의 최고가 주문 반환
 */
public function largestOrder()
{
    return $this->hasOne(Order::class)->ofMany('price', 'max');
}
```

> **경고**
> PostgreSQL은 UUID 컬럼에 대해 `MAX` 함수를 지원하지 않으므로, PostgreSQL의 UUID 컬럼과 one-of-many 관계를 함께 사용할 수 없습니다.

<a name="advanced-has-one-of-many-relationships"></a>
#### 고급 Has One Of Many 관계

복잡한 "has one of many" 관계도 구성할 수 있습니다. 예를 들어, `Product` 모델은 여러 `Price` 모델과 연결되어 있고, 새 가격 정보가 미리 게시될 수도 있습니다. 이 때, 가장 최근에 게시되어 현재 시점 기준으로 미래가 아닌 가격을 찾아야 한다면 아래와 같이 작성할 수 있습니다:

```php
/**
 * 상품의 현재 가격 정보 반환
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

"has-one-through" 관계는 중간 모델을 거쳐 다른 모델과의 일대일 관계를 설정하는 방식입니다.

예를 들어, 각 `Mechanic`(정비사)는 하나의 `Car`(자동차)와 연결되고, 각 Car는 하나의 `Owner`(차주)와 연결됩니다. Mechanic과 Owner는 직접적인 관계가 없지만, Mechanic을 통해 Owner까지 접근할 수 있습니다.

#### 테이블 구조 예시:

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

`Mechanic` 모델에 owner에 접근하는 관계를 정의할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Mechanic extends Model
{
    /**
     * 자동차의 소유주 반환
     */
    public function carOwner()
    {
        return $this->hasOneThrough(Owner::class, Car::class);
    }
}
```

첫 번째 인자는 최종적으로 접근하고 싶은 모델, 두 번째 인자는 중간 모델 클래스입니다.

이미 각 모델에 관계가 정의되어 있다면 `through` 메서드로 더욱 간결하게 관계를 정의할 수도 있습니다:

```php
// 문자열 구문
return $this->through('cars')->has('owner');

// 동적 구문
return $this->throughCars()->hasOwner();
```

<a name="has-one-through-key-conventions"></a>
#### 키 관례

Eloquent의 기본 외래키 관례가 적용됩니다. 만약 관계의 키를 커스터마이즈하고 싶다면 3~6번째 인자로 세부 키를 지정할 수 있습니다.

```php
class Mechanic extends Model
{
    /**
     * 자동차의 소유주 반환
     */
    public function carOwner()
    {
        return $this->hasOneThrough(
            Owner::class,
            Car::class,
            'mechanic_id', // cars 테이블의 외래키
            'car_id', // owners 테이블의 외래키
            'id', // mechanics 테이블의 로컬키
            'id' // cars 테이블의 로컬키
        );
    }
}
```

앞서 설명한 것처럼 기존 모델에 이미 관계가 정의되어 있다면 `through` 구문을 사용할 수 있습니다.

```php
// 문자열 구문
return $this->through('cars')->has('owner');

// 동적 구문
return $this->throughCars()->hasOwner();
```

<a name="has-many-through"></a>
### Has Many Through

"has-many-through" 관계는 중간 모델을 거쳐서 다수의 관련 모델에 접근할 수 있게 해줍니다. 예를 들어, `Project` 모델이 중간의 `Environment`를 통해 여러 `Deployment`와 연결된 경우 입니다.

#### 테이블 구조 예시:

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

`Project` 모델에서 모든 배포 기록에 접근하려면 다음과 같이 합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Project extends Model
{
    /**
     * 프로젝트의 모든 배포 기록 반환
     */
    public function deployments()
    {
        return $this->hasManyThrough(Deployment::class, Environment::class);
    }
}
```

이미 관계가 정의되어 있다면 `through` 메서드를 사용할 수도 있습니다.

```php
// 문자열 구문
return $this->through('environments')->has('deployments');

// 동적 구문
return $this->throughEnvironments()->hasDeployments();
```

`deployments` 테이블에 `project_id` 컬럼이 없음에도, hasManyThrough는 중간 모델의 외래키를 탐색해서 관련 배포를 가져올 수 있습니다.

<a name="has-many-through-key-conventions"></a>
#### 키 관례

기본 Eloquent 외래키 규칙이 적용됩니다. 키를 커스텀하려면 3~6번째 인자로 전달할 수 있습니다.

```php
class Project extends Model
{
    public function deployments()
    {
        return $this->hasManyThrough(
            Deployment::class,
            Environment::class,
            'project_id',       // environments 테이블의 외래키
            'environment_id',   // deployments 테이블의 외래키
            'id',               // projects 테이블의 로컬키
            'id'                // environments 테이블의 로컬키
        );
    }
}
```

`through` 메서드를 통한 정의도 가능합니다.

```php
// 문자열 구문
return $this->through('environments')->has('deployments');

// 동적 구문
return $this->throughEnvironments()->hasDeployments();
```

<a name="many-to-many"></a>
## 다대다(Many To Many) 관계

다대다 관계는 `hasOne`, `hasMany`보다 살짝 복잡합니다. 예를 들어, 사용자가 여러 역할을 가질 수 있으며, 각 역할은 여러 사용자가 공유할 수 있습니다. 즉, 한 사용자가 "저자", "편집자" 역할을 동시에 가질 수도 있고, 동일한 역할이 여러 사용자에게 할당될 수 있습니다.

<a name="many-to-many-table-structure"></a>
#### 테이블 구조

이 관계를 위해선 `users`, `roles`, `role_user` 세 개의 테이블이 필요합니다. `role_user` 테이블은 두 모델명을 알파벳순으로 붙여서 만들고, `user_id`, `role_id` 컬럼을 가집니다.

관례상, `roles` 테이블에 `user_id`만 두면 한 사용자만 협력할 수 있으니, 모든 할당을 가능하게 하려면 중간 테이블이 필요합니다.

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

다대다 관계는 `belongsToMany` 메서드를 반환하는 메서드를 모델에 작성하여 정의합니다. 아래는 사용자 모델에 `roles` 관계를 정의하는 예시입니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 사용자가 가진 역할 반환
     */
    public function roles()
    {
        return $this->belongsToMany(Role::class);
    }
}
```

이제 동적 관계 프로퍼티로 사용자의 역할 목록에 접근할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

foreach ($user->roles as $role) {
    //
}
```

쿼리 빌더 체이닝도 가능합니다:

```php
$roles = User::find(1)->roles()->orderBy('name')->get();
```

중간 테이블 이름(`role_user`)은 관련 모델명을 알파벳순으로 조합하여 자동 추정합니다. 이를 변경하려면 두 번째 인자로 테이블명을 명시하면 됩니다:

```php
return $this->belongsToMany(Role::class, 'role_user');
```

중간 테이블의 외래키 이름도 3, 4번째 인자로 각각 지정할 수 있습니다:

```php
return $this->belongsToMany(Role::class, 'role_user', 'user_id', 'role_id');
```

<a name="many-to-many-defining-the-inverse-of-the-relationship"></a>
#### 관계의 역방향(Inverse) 정의

다대다 관계의 역방향을 정의하려면, 관련 모델에 `belongsToMany` 결과를 반환하는 메서드를 만들어주면 됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Role extends Model
{
    /**
     * 이 역할을 가진 사용자 반환
     */
    public function users()
    {
        return $this->belongsToMany(User::class);
    }
}
```

역방향도 동일하게 커스텀 옵션을 지정할 수 있습니다.

<a name="retrieving-intermediate-table-columns"></a>
### 중간 테이블 컬럼 조회

다대다 관계에서 중간 테이블 컬럼에 접근하려면 `pivot` 속성을 사용합니다:

```php
use App\Models\User;

$user = User::find(1);

foreach ($user->roles as $role) {
    echo $role->pivot->created_at;
}
```

중간 테이블에 추가 컬럼이 있다면, 관계 정의 시 withPivot를 이용해 명시해야 접근할 수 있습니다:

```php
return $this->belongsToMany(Role::class)->withPivot('active', 'created_by');
```

중간 테이블의 `created_at`, `updated_at` 타임스탬프 자동 관리를 원하면 withTimestamps를 호출하세요:

```php
return $this->belongsToMany(Role::class)->withTimestamps();
```

> **경고**
> 타임스탬프 관리용 중간 테이블에는 반드시 `created_at`, `updated_at` 두 컬럼 모두 있어야 합니다.

<a name="customizing-the-pivot-attribute-name"></a>
#### `pivot` 속성명 커스텀

중간 테이블의 속성명은 `as` 메서드로 사용 목적에 맞게 변경할 수 있습니다. 예시:

```php
return $this->belongsToMany(Podcast::class)
    ->as('subscription')
    ->withTimestamps();

$users = User::with('podcasts')->get();

foreach ($users->flatMap->podcasts as $podcast) {
    echo $podcast->subscription->created_at;
}
```

<a name="filtering-queries-via-intermediate-table-columns"></a>
### 중간 테이블 컬럼 기준으로 쿼리 필터링

다대다 관계 쿼리에서 `wherePivot`, `wherePivotIn` 등 다양한 메서드로 중간 테이블을 조건에 넣을 수 있습니다:

```php
return $this->belongsToMany(Role::class)
    ->wherePivot('approved', 1);

return $this->belongsToMany(Role::class)
    ->wherePivotIn('priority', [1, 2]);

return $this->belongsToMany(Role::class)
    ->wherePivotNotIn('priority', [1, 2]);
```

`wherePivotBetween`, `wherePivotNotBetween`, `wherePivotNull`, `wherePivotNotNull` 등도 지원합니다.

<a name="ordering-queries-via-intermediate-table-columns"></a>
### 중간 테이블 컬럼 기준으로 쿼리 정렬

`orderByPivot` 메서드로 중간 테이블 컬럼 값 정렬도 가능합니다:

```php
return $this->belongsToMany(Badge::class)
    ->where('rank', 'gold')
    ->orderByPivot('created_at', 'desc');
```

<a name="defining-custom-intermediate-table-models"></a>
### 커스텀 중간 테이블 모델 정의

다대다 관계의 중간 테이블을 커스텀 모델로 정의하려면 `using` 메서드를 사용합니다. 이 모델은 `Illuminate\Database\Eloquent\Relations\Pivot`를 상속해야 합니다.

예시:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Role extends Model
{
    public function users()
    {
        return $this->belongsToMany(User::class)->using(RoleUser::class);
    }
}

class RoleUser extends \Illuminate\Database\Eloquent\Relations\Pivot
{
    //
}
```

> **경고**
> Pivot 모델에서는 `SoftDeletes` 트레이트를 사용할 수 없습니다. 소프트 삭제가 필요하면 피벗 모델을 일반 Eloquent 모델로 전환하세요.

<a name="custom-pivot-models-and-incrementing-ids"></a>
#### 커스텀 피벗 모델과 오토인크리먼트 ID

커스텀 피벗 모델이 자동 증가형(primary key) 컬럼을 가질 경우, `$incrementing = true` 프로퍼티를 명시해야 합니다.

```php
public $incrementing = true;
```

<a name="polymorphic-relationships"></a>
## 폴리모픽(Polymorphic) 관계

폴리모픽 관계는 자식 모델이 하나 이상의 타입의 모델에 연관될 수 있도록 해 줍니다. 예를 들어, `Comment` 모델이 `Post`도, `Video`도 소유할 수 있듯이 말입니다.

<a name="one-to-one-polymorphic-relations"></a>
### 일대일(Polymorphic)

<a name="one-to-one-polymorphic-table-structure"></a>
#### 테이블 구조

일대일 폴리모픽 관계의 예로, `Image`가 `Post`와 `User` 모두에 속할 수 있습니다. 이럴 때 `images` 테이블에는 `imageable_id`, `imageable_type` 컬럼이 있어야 하며, 이는 각각 소유 모델의 id, 모델 클래스명을 저장합니다.

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

<a name="one-to-one-polymorphic-model-structure"></a>
#### 모델 구조

다음은 모델 정의 예시입니다.

```php
class Image extends Model
{
    public function imageable()
    {
        return $this->morphTo();
    }
}

class Post extends Model
{
    public function image()
    {
        return $this->morphOne(Image::class, 'imageable');
    }
}

class User extends Model
{
    public function image()
    {
        return $this->morphOne(Image::class, 'imageable');
    }
}
```

<a name="one-to-one-polymorphic-retrieving-the-relationship"></a>
#### 관계 조회

동적으로 다음과 같이 접근할 수 있습니다:

```php
$post = Post::find(1);
$image = $post->image;

$image = Image::find(1);
$imageable = $image->imageable;
```

`imageable` 관계는 상황에 따라 `Post` 또는 `User` 인스턴스를 반환합니다.

<a name="morph-one-to-one-key-conventions"></a>
#### 키 관례

id와 type 컬럼명을 커스텀하려면 메서드 인자로 직접 전달해야 합니다.

```php
public function imageable()
{
    return $this->morphTo(__FUNCTION__, 'imageable_type', 'imageable_id');
}
```

<a name="one-to-many-polymorphic-relations"></a>
### 일대다(Polymorphic)

<a name="one-to-many-polymorphic-table-structure"></a>
#### 테이블 구조

예를 들어, `Comment`가 `Post`와 `Video` 모두에 달릴 수 있다면 아래와 같은 테이블 구조가 필요합니다:

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

```php
class Comment extends Model
{
    public function commentable()
    {
        return $this->morphTo();
    }
}

class Post extends Model
{
    public function comments()
    {
        return $this->morphMany(Comment::class, 'commentable');
    }
}

class Video extends Model
{
    public function comments()
    {
        return $this->morphMany(Comment::class, 'commentable');
    }
}
```

<a name="one-to-many-polymorphic-retrieving-the-relationship"></a>
#### 관계 조회

```php
$post = Post::find(1);

foreach ($post->comments as $comment) {
    // ...
}

$comment = Comment::find(1);

$commentable = $comment->commentable;
```

`commentable` 관계는 `Post` 또는 `Video` 인스턴스를 반환합니다.

<a name="one-of-many-polymorphic-relations"></a>
### One Of Many (Polymorphic)

하나의 모델이 여러 관계 모델을 가질 때, "최근" 또는 "가장 오래된" 것만 빠르게 가져오고 싶다면 `morphOne`과 `latestOfMany`/`oldestOfMany`/`ofMany` 조합을 사용합니다.

```php
public function latestImage()
{
    return $this->morphOne(Image::class, 'imageable')->latestOfMany();
}
```
```php
public function oldestImage()
{
    return $this->morphOne(Image::class, 'imageable')->oldestOfMany();
}
```

특정 컬럼 기준으로 최대값/최소값을 찾고 싶은 경우:

```php
public function bestImage()
{
    return $this->morphOne(Image::class, 'imageable')->ofMany('likes', 'max');
}
```

> **참고**
> 더욱 고급 사용을 원하면 [has one of many 문서](#advanced-has-one-of-many-relationships)를 참고하세요.

<a name="many-to-many-polymorphic-relations"></a>
### 다대다(Polymorphic)

<a name="many-to-many-polymorphic-table-structure"></a>
#### 테이블 구조

예를 들어, `Post`와 `Video`가 모두 다양한 `Tag`와 다대다 폴리모픽 관계라면 다음과 같이 중간 테이블을 만듭니다:

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

<a name="many-to-many-polymorphic-model-structure"></a>
#### 모델 구조

각 모델은 `morphToMany` 관계 메서드를 가집니다.

```php
class Post extends Model
{
    public function tags()
    {
        return $this->morphToMany(Tag::class, 'taggable');
    }
}
```

<a name="many-to-many-polymorphic-defining-the-inverse-of-the-relationship"></a>
#### 역방향(폴리모픽) 관계 정의

`Tag` 모델에는 가능한 부모 모델별로 메서드를 작성해둘 수 있습니다.

```php
class Tag extends Model
{
    public function posts()
    {
        return $this->morphedByMany(Post::class, 'taggable');
    }

    public function videos()
    {
        return $this->morphedByMany(Video::class, 'taggable');
    }
}
```

<a name="many-to-many-polymorphic-retrieving-the-relationship"></a>
#### 관계 조회

```php
$post = Post::find(1);
foreach ($post->tags as $tag) {
    //
}

$tag = Tag::find(1);
foreach ($tag->posts as $post) {
    //
}
foreach ($tag->videos as $video) {
    //
}
```

<a name="custom-polymorphic-types"></a>
### 커스텀 폴리모픽 타입

Laravel은 기본적으로 "타입" 컬럼에 모델의 완전한 클래스명을 저장합니다. 하지만, 이를 `post`, `video` 등 문자열로 매핑하고 싶다면 `Relation::enforceMorphMap`을 사용할 수 있습니다.

```php
use Illuminate\Database\Eloquent\Relations\Relation;

Relation::enforceMorphMap([
    'post' => 'App\Models\Post',
    'video' => 'App\Models\Video',
]);
```

모델에서 현재 morph alias를 확인하려면 `getMorphClass`를, alias에 해당하는 실제 클래스를 구하려면 `Relation::getMorphedModel`을 사용하세요.

> **경고**
> morph 맵을 기존 애플리케이션에 추가하면, 데이터베이스 내의 모든 morphable `*_type` 값도 alias로 변환되어야 합니다.

<a name="dynamic-relationships"></a>
### 동적 관계

`resolveRelationUsing` 메서드로 런타임에 모델 간 관계를 정의할 수 있습니다. 예시:

```php
Order::resolveRelationUsing('customer', function ($orderModel) {
    return $orderModel->belongsTo(Customer::class, 'customer_id');
});
```

> **경고**
> 동적 관계를 정의할 땐 항상 명시적으로 키를 넘기세요.

<a name="querying-relations"></a>
## 관계 쿼리하기

Eloquent 관계는 모두 메서드로 정의되므로, 실제 쿼리를 실행하지 않고도 관계 인스턴스를 얻고, 쿼리 빌더 체이닝으로 조건을 추가할 수 있습니다.

아래는 사용자와 포스트 관계 예시입니다:

```php
class User extends Model
{
    public function posts()
    {
        return $this->hasMany(Post::class);
    }
}

$user = User::find(1);

$user->posts()->where('active', 1)->get();
```

모든 쿼리 빌더 메서드를 사용할 수 있으니 문서를 확인하세요.

<a name="chaining-orwhere-clauses-after-relationships"></a>
#### 관계에 orWhere 체이닝 주의

관계 쿼리에 `orWhere`를 체이닝하면 논리 그룹핑이 사용되지 않으므로 다음과 같은 주의가 필요합니다:

```php
$user->posts()
        ->where('active', 1)
        ->orWhere('votes', '>=', 100)
        ->get();
```

이 쿼리는 "모든 user_id = ? and active = 1 또는 votes >= 100"을 가져옵니다. 특정 사용자가 아닌 결과를 낼 수 있습니다.

따라서 논리 그룹핑을 이용해야 합니다:

```php
use Illuminate\Database\Eloquent\Builder;

$user->posts()
    ->where(function (Builder $query) {
        return $query->where('active', 1)
                     ->orWhere('votes', '>=', 100);
    })
    ->get();
```

이렇게 하면 쿼리가 "user_id = ? and (active = 1 or votes >= 100)"으로 올바르게 그룹핑됩니다.

<a name="relationship-methods-vs-dynamic-properties"></a>
### 관계 메서드 vs 동적 프로퍼티

추가 조건이 필요 없다면 동적 프로퍼티 방식으로 관계에 접근할 수 있습니다:

```php
$user = User::find(1);

foreach ($user->posts as $post) {
    //
}
```

동적 관계 프로퍼티는 지연 로딩(lazy loading)을 사용합니다. 자주 접근하는 관계라면 [즉시 로딩](#eager-loading)의 사용을 권장합니다.

<a name="querying-relationship-existence"></a>
### 관계 존재 쿼리

모델의 특정 관계가 존재하는 레코드만 필터링하고 싶다면 `has`/`orHas` 메서드를 사용합니다:

```php
$posts = Post::has('comments')->get();

// 세 개 이상 댓글이 있는 글만
$posts = Post::has('comments', '>=', 3)->get();

// 하위 관계(중첩)도 점(.) 표기법으로 사용할 수 있습니다.
$posts = Post::has('comments.images')->get();
```

관계 조건을 추가하려면 `whereHas`/`orWhereHas`를 사용합니다:

```php
$posts = Post::whereHas('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
})->get();
```

> **경고**
> 관계 존재 쿼리는 반드시 동일 데이터베이스 내에서만 수행 가능합니다.

<a name="inline-relationship-existence-queries"></a>
#### 인라인(In-line) 관계 존재 쿼리

관계에 단순한 where 조건만 붙이고 싶으면 `whereRelation`, `orWhereRelation` 등을 쓸 수 있습니다:

```php
$posts = Post::whereRelation('comments', 'is_approved', false)->get();
$posts = Post::whereRelation(
    'comments', 'created_at', '>=', now()->subHour()
)->get();
```

<a name="querying-relationship-absence"></a>
### 관계 부재 쿼리

특정 관계가 없는 레코드만 필터링하고 싶으면 `doesntHave`/`orDoesntHave`를 씁니다:

```php
$posts = Post::doesntHave('comments')->get();
```

관계에 조건을 추가하고 싶으면 `whereDoesntHave`/`orWhereDoesntHave` 사용:

```php
$posts = Post::whereDoesntHave('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
})->get();
```

점(.) 표기법으로 중첩 관계에도 사용할 수 있습니다.

<a name="querying-morph-to-relationships"></a>
### Morph To 관계 쿼리

Morph To 관계의 존재 쿼리는 `whereHasMorph`, `whereDoesntHaveMorph`를 사용합니다:

```php
$comments = Comment::whereHasMorph(
    'commentable',
    [Post::class, Video::class],
    function (Builder $query) {
        $query->where('title', 'like', 'code%');
    }
)->get();
```

두 번째 인자로 모델 타입 배열이나 `*`(와일드카드)를 허용합니다.

<a name="aggregating-related-models"></a>
## 관련 모델 집계(Aggregate)

<a name="counting-related-models"></a>
### 관련 모델 개수 카운팅

관련 모델의 개수를 실제 모델을 불러오지 않고도 세려면 `withCount`를 사용하세요:

```php
$posts = Post::withCount('comments')->get();

foreach ($posts as $post) {
    echo $post->comments_count;
}
```

여러 관계를 배열로 넘기거나 추가 제약 조건도 줄 수 있습니다.

관계별 카운트 값 alias 지정도 가능합니다.

### 지연 카운트 로딩

모델을 불러온 다음 `loadCount`로 추가 카운트 집계를 할 수 있습니다.

<a name="other-aggregate-functions"></a>
### 기타 집계 함수

`withMin`, `withMax`, `withAvg`, `withSum`, `withExists` 등도 지원합니다. alias도 지정 가능합니다.

지연 로딩용 `loadSum` 등도 동일하게 가능합니다.

<a name="counting-related-models-on-morph-to-relationships"></a>
### Morph To 관계의 관련 모델 카운팅

`with`와 `morphWithCount`를 조합하면, Morph To 관계 및 각 타입별 관련 모델 집계도 동시에 가능합니다.

```php
$activities = ActivityFeed::with([
    'parentable' => function (MorphTo $morphTo) {
        $morphTo->morphWithCount([
            Photo::class => ['tags'],
            Post::class => ['comments'],
        ]);
    }])->get();
```

이미 모델 인스턴스를 불러온 상태라면 `loadMorphCount`를 쓸 수 있습니다.

<a name="eager-loading"></a>
## 즉시 로딩(Eager Loading)

관계에 동적으로 접근하면 데이터가 실제로 필요할 때까지 쿼리를 실행하지 않습니다(지연 로딩). 즉시 로딩을 활용하면 "N+1" 문제를 해소할 수 있습니다.

예:

```php
$books = Book::with('author')->get();

foreach ($books as $book) {
    echo $book->author->name;
}
```

이 경우, 책과 저자 쿼리가 각각 한 번씩만 실행됩니다.

<a name="eager-loading-multiple-relationships"></a>
#### 여러 관계 동시에 즉시 로딩

배열로 여러 관계를 동시 로딩할 수 있습니다:

```php
$books = Book::with(['author', 'publisher'])->get();
```

<a name="nested-eager-loading"></a>
#### 중첩 즉시 로딩

점(.) 표기법이나 중첩 배열로 자식의 자식까지도 즉시 로딩 가능합니다.

```php
$books = Book::with('author.contacts')->get();
$books = Book::with([
    'author' => [
        'contacts',
        'publisher',
    ],
])->get();
```

<a name="nested-eager-loading-morphto-relationships"></a>
#### MorphTo 관계와 중첩 즉시 로딩

MorphTo 관계 및 하위 관계까지 즉시 로딩하려면 `morphWith`를 씁니다.

<a name="eager-loading-specific-columns"></a>
#### 특정 컬럼만 즉시 로딩

원하지 않는 컬럼은 제외하고 필요한 컬럼만 명시적으로 지정할 수 있습니다.

> **경고**
> 항상 id, 외래키 컬럼 등 관계 매핑에 필수적인 컬럼을 포함해야 합니다.

<a name="eager-loading-by-default"></a>
#### 기본적으로 즉시 로딩

특정 관계를 항상 즉시 로딩하고 싶다면 모델의 `$with` 프로퍼티에 추가하세요.

```php
protected $with = ['author'];
```

`without`, `withOnly`로 개별 쿼리에서 변경도 가능합니다.

<a name="constraining-eager-loads"></a>
### 즉시 로딩하는 관계에 조건 추가

`with` 메서드에 배열/클로저로 조건을 추가할 수 있습니다:

```php
$users = User::with(['posts' => function ($query) {
    $query->where('title', 'like', '%code%');
}])->get();
```

> **경고**
> `limit`/`take` 쿼리는 즉시 로딩 제약에 사용할 수 없습니다.

<a name="constraining-eager-loads-with-relationship-existence"></a>
#### 관계 존재 조건과 함께 즉시 로딩

`withWhereHas`를 쓰면 동일 조건으로 관계 존재 검사와 즉시 로딩을 동시에 할 수 있습니다.

<a name="lazy-eager-loading"></a>
### 지연 즉시 로딩

부모 모델을 먼저 로딩한 뒤, 조건에 따라 관계만 동적으로 즉시 로딩할 수 있습니다.

```php
$books = Book::all();

if ($someCondition) {
    $books->load('author', 'publisher');
}
```

조건이 필요한 즉시 로딩도 배열/클로저 조합으로 가능합니다.

`loadMissing`을 쓰면 이미 로딩된 관계를 중복 요청하지 않습니다.

<a name="nested-lazy-eager-loading-morphto"></a>
#### Nested Lazy Eager Loading & `morphTo`

`loadMorph` 메서드를 이용해 MorphTo 관계 및 하위 관계만 조건부로 나중에 즉시 로딩할 수 있습니다.

<a name="preventing-lazy-loading"></a>
### 지연 로딩 비활성화(Lazy Loading 방지)

지연 로딩 자체를 강제로 막을 수도 있습니다. 일반적으로 `AppServiceProvider`의 `boot` 메서드에서 아래처럼 설정합니다:

```php
use Illuminate\Database\Eloquent\Model;

public function boot()
{
    Model::preventLazyLoading(! $this->app->isProduction());
}
```

지연 로딩 위반이 발생했을 때 로그만 출력하고 싶으면 `handleLazyLoadingViolationUsing`을 활용할 수 있습니다.

<a name="inserting-and-updating-related-models"></a>
## 관계된 모델 삽입 & 갱신

<a name="the-save-method"></a>
### `save` 메서드

관계를 통한 새 모델 추가는 `save` 사용이 가장 편리합니다. 예시:

```php
$comment = new Comment(['message' => 'A new comment.']);

$post = Post::find(1);

$post->comments()->save($comment);
```

여러 모델을 한 번에 추가하고 싶다면 `saveMany`를 쓰세요.

모델을 통한 관계 접근이 이미 이루어진 상태라면, `refresh`로 새로고침 할 수 있습니다.

<a name="the-push-method"></a>
#### 모델과 관계를 재귀적으로 저장

`push` 메서드는 모델과 연관된 모든 관계까지 재귀적으로 저장해 줍니다.

조용히 진행하고 싶으면 `pushQuietly` 사용.

<a name="the-create-method"></a>
### `create` 메서드

`save`, `saveMany`와 달리 `create`는 속성 배열을 받아 새 모델을 생성 및 저장합니다. 즉시 새 모델을 반환합니다.

여러 개를 추가하고 싶으면 `createMany` 사용.

`findOrNew`, `firstOrNew`, `firstOrCreate`, `updateOrCreate` 등도 지원합니다.

> **참고**
> `create` 사용 전 [대량 할당(Mass Assignment)](/docs/{{version}}/eloquent#mass-assignment) 문서를 반드시 참고하세요.

<a name="updating-belongs-to-relationships"></a>
### Belongs To 관계

자식 모델에 부모 모델을 새로 할당하려면 `associate`를, 연결을 끊고 싶으면 `dissociate`를 사용하세요.

```php
$user->account()->associate($account);
$user->save();

$user->account()->dissociate();
$user->save();
```

<a name="updating-many-to-many-relationships"></a>
### Many To Many 관계

<a name="attaching-detaching"></a>
#### 관계 연결/해제(Attaching/Detaching)

`attach`로 중간 테이블에 데이터를 넣고, `detach`로 삭제할 수 있습니다. ID 배열이나 추가 데이터도 넘길 수 있습니다.

<a name="syncing-associations"></a>
#### 관계 동기화(Syncing)

`synс`는 중간 테이블의 연결을 주어진 ID 배열에 맞게 동기화합니다.

`synсWithPivotValues`로 추가 데이터도 함께 동기화할 수 있습니다.

`synсWithoutDetaching`은 기존 연결을 유지하면서 새로 추가만 합니다.

<a name="toggling-associations"></a>
#### 연결 상태 토글(Toggle)

ID가 연결돼 있으면 해제하고, 없는 경우는 연결합니다.

<a name="updating-a-record-on-the-intermediate-table"></a>
#### 중간 테이블 레코드 갱신

`updateExistingPivot`으로 중간 테이블의 특정 값을 갱신할 수 있습니다.

<a name="touching-parent-timestamps"></a>
## 부모 타임스탬프 갱신(Touching Parent Timestamps)

모델이 `belongsTo` 또는 `belongsToMany` 관계를 가질 때, 자식이 변경되면 부모 모델의 `updated_at`도 갱신하도록 할 수 있습니다. 이를 위해 자식 모델의 `$touches` 배열에 관계 키를 추가합니다.

```php
protected $touches = ['post'];
```

> **경고**
> 부모 모델의 타임스탬프 갱신은 반드시 Eloquent의 `save` 메서드를 사용해야 작동합니다.

---

(더 많은 내용이나 이어지는 제목 등 필요시 말씀해 주세요.)