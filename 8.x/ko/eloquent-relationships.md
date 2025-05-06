# Eloquent: 관계

- [소개](#introduction)
- [관계 정의하기](#defining-relationships)
    - [일대일(One To One)](#one-to-one)
    - [일대다(One To Many)](#one-to-many)
    - [일대다(역관계) / Belongs To](#one-to-many-inverse)
    - [Has One Of Many](#has-one-of-many)
    - [Has One Through](#has-one-through)
    - [Has Many Through](#has-many-through)
- [다대다(Many To Many) 관계](#many-to-many)
    - [중간 테이블 컬럼 조회](#retrieving-intermediate-table-columns)
    - [중간 테이블 컬럼으로 쿼리 필터링](#filtering-queries-via-intermediate-table-columns)
    - [커스텀 중간 테이블 모델 정의](#defining-custom-intermediate-table-models)
- [폴리모픽(Polymorphic) 관계](#polymorphic-relationships)
    - [일대일](#one-to-one-polymorphic-relations)
    - [일대다](#one-to-many-polymorphic-relations)
    - [One Of Many](#one-of-many-polymorphic-relations)
    - [다대다](#many-to-many-polymorphic-relations)
    - [커스텀 폴리모픽 타입](#custom-polymorphic-types)
- [동적 관계](#dynamic-relationships)
- [관계 조회](#querying-relations)
    - [관계 메서드 vs. 동적 프로퍼티](#relationship-methods-vs-dynamic-properties)
    - [관계 존재 쿼리](#querying-relationship-existence)
    - [관계 부재 쿼리](#querying-relationship-absence)
    - [Morph To 관계 쿼리](#querying-morph-to-relationships)
- [연관된 모델 집계](#aggregating-related-models)
    - [연관 모델 개수 세기](#counting-related-models)
    - [기타 집계 함수](#other-aggregate-functions)
    - [Morph To 관계에서의 연관 모델 개수 세기](#counting-related-models-on-morph-to-relationships)
- [Eager Loading(즉시 로딩)](#eager-loading)
    - [즉시 로딩 제한하기](#constraining-eager-loads)
    - [지연 즉시 로딩(Lazy Eager Loading)](#lazy-eager-loading)
    - [지연 로딩 방지](#preventing-lazy-loading)
- [연관된 모델 삽입 & 갱신](#inserting-and-updating-related-models)
    - [`save` 메서드](#the-save-method)
    - [`create` 메서드](#the-create-method)
    - [Belongs To 관계](#updating-belongs-to-relationships)
    - [다대다 관계](#updating-many-to-many-relationships)
- [부모 타임스탬프 갱신](#touching-parent-timestamps)

<a name="introduction"></a>
## 소개

데이터베이스 테이블은 종종 서로 연관되어 있습니다. 예를 들어, 블로그 글에는 여러 개의 댓글이 달릴 수 있고, 주문은 주문자를 나타내는 사용자와 연관될 수 있습니다. Eloquent는 이 관계들을 손쉽게 관리할 수 있도록 다양한 일반적인 관계를 지원합니다.

<div class="content-list" markdown="1">

- [일대일(One To One)](#one-to-one)
- [일대다(One To Many)](#one-to-many)
- [다대다(Many To Many)](#many-to-many)
- [Has One Through](#has-one-through)
- [Has Many Through](#has-many-through)
- [일대일 폴리모픽](#one-to-one-polymorphic-relations)
- [일대다 폴리모픽](#one-to-many-polymorphic-relations)
- [다대다 폴리모픽](#many-to-many-polymorphic-relations)

</div>

<a name="defining-relationships"></a>
## 관계 정의하기

Eloquent 관계는 Eloquent 모델 클래스의 메서드로 정의합니다. 관계는 강력한 [쿼리 빌더](/docs/{{version}}/queries)로도 동작하므로, 메서드로 정의하면 체이닝 및 쿼리 조건 추가가 매우 강력해집니다. 예를 들어, 다음과 같이 `posts` 관계에 쿼리 조건을 추가할 수 있습니다.

    $user->posts()->where('active', 1)->get();

관계를 사용하기 전에, Eloquent가 지원하는 각 관계 타입을 어떻게 정의하는지 먼저 살펴보겠습니다.

<a name="one-to-one"></a>
### 일대일(One To One)

일대일 관계는 가장 기본적인 관계로, 예를 들어 `User` 모델이 하나의 `Phone` 모델과 연관될 수 있습니다. 이를 위해 `User` 모델에 `phone` 메서드를 정의하고, 이 안에서 `hasOne` 메서드를 호출합니다. `hasOne` 메서드는 모델의 `Illuminate\Database\Eloquent\Model` 기본 클래스에서 제공됩니다.

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * 유저와 연관된 전화 번호(Phone)를 가져옵니다.
         */
        public function phone()
        {
            return $this->hasOne(Phone::class);
        }
    }

`hasOne` 메서드의 첫 번째 인자로는 연관된 모델 클래스명을 넘깁니다. 이렇게 관계를 정의하면, Eloquent의 동적 프로퍼티를 이용해 관련 레코드를 조회할 수 있습니다. 동적 프로퍼티란, 관계 메서드를 모델의 프로퍼티처럼 사용할 수 있게 해주는 기능입니다.

    $phone = User::find(1)->phone;

Eloquent는 관계의 외래 키를 부모 모델명에 따라 자동으로 결정합니다. 위 경우 `Phone` 모델은 기본적으로 `user_id` 외래 키를 가진다고 가정합니다. 만약 이 관례를 변경하고 싶다면, `hasOne`의 두 번째 인자로 직접 지정할 수 있습니다:

    return $this->hasOne(Phone::class, 'foreign_key');

또한 Eloquent는 외래 키 값이 부모의 기본 키(`id`)와 같다고 가정합니다. 다른 컬럼을 기본 키로 사용하고 싶다면, 세 번째 인자로 local key를 지정할 수 있습니다:

    return $this->hasOne(Phone::class, 'foreign_key', 'local_key');

<a name="one-to-one-defining-the-inverse-of-the-relationship"></a>
#### 관계의 역방향(반대 방향) 정의하기

`User` 모델에서 `Phone` 모델에 접근했으니, 이제 `Phone`에서 전화 소유자를 조회하는 관계를 정의해봅시다. 일대일(`hasOne`) 관계의 역방향은 `belongsTo` 메서드로 정의합니다.

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;

    class Phone extends Model
    {
        /**
         * 이 전화번호를 소유한 유저를 가져옵니다.
         */
        public function user()
        {
            return $this->belongsTo(User::class);
        }
    }

`user` 메서드를 호출하면, Eloquent는 `Phone` 모델의 `user_id`와 일치하는 `User` 모델을 찾으려 시도합니다.

Eloquent는 관계 메서드 이름에 `_id`를 붙여서 외래 키 컬럼을 결정합니다. 즉, 여기서는 `Phone` 모델에 `user_id` 컬럼이 있다고 가정합니다. 만약 외래 키 이름이 다르다면, 두 번째 인자로 직접 지정할 수 있습니다:

    /**
     * 이 전화번호를 소유한 유저를 가져옵니다.
     */
    public function user()
    {
        return $this->belongsTo(User::class, 'foreign_key');
    }

부모 모델의 기본 키가 `id`가 아니거나, 다른 컬럼으로 연관 모델을 조회하고 싶다면 세 번째 인자로 owner key를 지정해주세요:

    /**
     * 이 전화번호를 소유한 유저를 가져옵니다.
     */
    public function user()
    {
        return $this->belongsTo(User::class, 'foreign_key', 'owner_key');
    }

<a name="one-to-many"></a>
### 일대다(One To Many)

일대다 관계는 한 모델이 여러 자식 모델을 가질 때 사용합니다. 예를 들어, 하나의 블로그 글에 여러 개의 댓글이 달릴 수 있습니다. 다음처럼 관계를 정의합니다.

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;

    class Post extends Model
    {
        /**
         * 블로그 글에 대한 댓글들을 가져옵니다.
         */
        public function comments()
        {
            return $this->hasMany(Comment::class);
        }
    }

Eloquent는 자동으로 `Comment` 모델의 외래 키 컬럼명을 결정합니다. 관례상, 부모 모델명을 snake_case로 변환한 뒤 `_id`를 붙입니다. 여기선 `Comment` 모델의 외래 키는 `post_id`입니다.

관계 메서드를 정의하면, 동적 프로퍼티로 연관된 댓글들의 [컬렉션](/docs/{{version}}/eloquent-collections)을 조회할 수 있습니다.

    use App\Models\Post;

    $comments = Post::find(1)->comments;

    foreach ($comments as $comment) {
        //
    }

관계도 쿼리 빌더로 사용할 수 있으므로, 다음처럼 추가 조건을 계속 체이닝할 수 있습니다.

    $comment = Post::find(1)->comments()
                        ->where('title', 'foo')
                        ->first();

외래 키, 로컬 키를 오버라이드하려면 추가 인자를 넘기면 됩니다.

    return $this->hasMany(Comment::class, 'foreign_key');

    return $this->hasMany(Comment::class, 'foreign_key', 'local_key');

<a name="one-to-many-inverse"></a>
### 일대다(역방향) / Belongs To

이제 게시글의 모든 댓글에 접근할 수 있으니, 각 댓글에서 부모 게시글에 접근하는 관계를 정의해봅시다. 즉, 자식 모델(댓글)에 `belongsTo` 관계를 메서드로 만들어줍니다.

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;

    class Comment extends Model
    {
        /**
         * 이 댓글이 속한 게시글을 가져옵니다.
         */
        public function post()
        {
            return $this->belongsTo(Post::class);
        }
    }

정의한 후, 다음처럼 `post` 동적 프로퍼티로 댓글의 소속 글에 접근할 수 있습니다.

    use App\Models\Comment;

    $comment = Comment::find(1);

    return $comment->post->title;

위 예시에서 Eloquent는 `Comment` 모델의 `post_id`와 일치하는 `Post` 모델의 `id`를 자동 조회합니다.

기본 외래 키 컬럼명은 관계 메서드명에 `_`와 부모 기본 키 컬럼명을 조합합니다. 즉, 여기선 `post_id`입니다.

관례와 다르게 외래 키를 사용한다면, 두 번째 인자로 지정하면 됩니다.

    /**
     * 이 댓글이 속한 게시글을 가져옵니다.
     */
    public function post()
    {
        return $this->belongsTo(Post::class, 'foreign_key');
    }

부모 모델의 기본 키가 `id`가 아니거나, 다른 컬럼을 사용한다면 세 번째 인자를 통해 지정할 수 있습니다.

    /**
     * 이 댓글이 속한 게시글을 가져옵니다.
     */
    public function post()
    {
        return $this->belongsTo(Post::class, 'foreign_key', 'owner_key');
    }

<a name="default-models"></a>
#### 기본 모델(Default Models)

`belongsTo`, `hasOne`, `hasOneThrough`, `morphOne` 관계는 해당 관계가 `null`일 경우 반환할 기본 모델을 정의할 수 있습니다. 이 패턴은 [Null Object 패턴](https://en.wikipedia.org/wiki/Null_Object_pattern)으로, 코드의 조건문을 줄이는 데 도움이 됩니다. 다음 예시처럼, `Post` 모델에 유저가 연결되어 있지 않으면 빈 `App\Models\User` 모델이 반환됩니다.

    /**
     * 포스트의 작성자를 가져옵니다.
     */
    public function user()
    {
        return $this->belongsTo(User::class)->withDefault();
    }

기본 모델에 속성을 채우고 싶으면 배열이나 클로저를 넘길 수 있습니다.

    /**
     * 포스트의 작성자를 가져옵니다.
     */
    public function user()
    {
        return $this->belongsTo(User::class)->withDefault([
            'name' => 'Guest Author',
        ]);
    }

    /**
     * 포스트의 작성자를 가져옵니다.
     */
    public function user()
    {
        return $this->belongsTo(User::class)->withDefault(function ($user, $post) {
            $user->name = 'Guest Author';
        });
    }

<a name="querying-belongs-to-relationships"></a>
#### Belongs To 관계 쿼리

Belongs To 관계의 자식 모델을 쿼리할 땐, 직접 `where`절을 만들어 조회할 수 있습니다.

    use App\Models\Post;

    $posts = Post::where('user_id', $user->id)->get();

그러나 `whereBelongsTo` 메서드를 쓰면 관계명과 외래 키를 자동으로 지정해줍니다.

    $posts = Post::whereBelongsTo($user)->get();

관계명을 직접 지정하고 싶으면 두 번째 인자로 전달하세요.

    $posts = Post::whereBelongsTo($user, 'author')->get();

<a name="has-one-of-many"></a>
### Has One Of Many

특정 관계 중 "최신", "가장 오래된" 등 특정 하나의 모델만 쉽게 가져오고 싶을 때가 있습니다. 예를 들어, `User`는 여러 개의 `Order`와 연관될 수 있지만, 가장 최근 주문만 쉽게 조회하고자 할 수 있습니다. 이 경우 `hasOne`에 `ofMany` 계열 메서드를 활용합니다.

```php
/**
 * 사용자의 최신 주문을 가져옵니다.
 */
public function latestOrder()
{
    return $this->hasOne(Order::class)->latestOfMany();
}
```

반대로, 가장 오래된(처음 생성된) 주문을 가져오려면:

```php
/**
 * 사용자의 가장 오래된 주문을 가져옵니다.
 */
public function oldestOrder()
{
    return $this->hasOne(Order::class)->oldestOfMany();
}
```

기본적으로 `latestOfMany`와 `oldestOfMany`는 기본 키를 기준으로 정렬하여 조회합니다. 다른 기준으로 정렬하려면, `ofMany`에 컬럼명과 집계함수(`min` 또는 `max`)를 지정할 수 있습니다.

```php
/**
 * 사용자의 가장 비싼 주문을 가져옵니다.
 */
public function largestOrder()
{
    return $this->hasOne(Order::class)->ofMany('price', 'max');
}
```

> {note} PostgreSQL은 UUID 컬럼에 대해 `MAX`를 지원하지 않아 PostgreSQL UUID 컬럼에는 본 기능이 동작하지 않습니다.

<a name="advanced-has-one-of-many-relationships"></a>
#### 고급 Has One Of Many 관계

더 복잡한 "has one of many" 관계도 만들 수 있습니다. 예를 들어, `Product`는 여러 `Price`가 연결되어 있으며, 미래의 가격도 미리 등록될 수 있습니다(`published_at` 컬럼 활용).

예를 들어, 이제 미래 시점이 아닌 가장 최근 게시된 가격을 조회하고, 동일한 날짜라면 id가 가장 큰 가격을 우선시합니다. `ofMany`에 배열을 넘기고, 클로저(추가 쿼리 조건)를 두 번째 인자로 전달합니다.

```php
/**
 * 이 상품의 현재 가격을 가져옵니다.
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

"has-one-through" 관계는 제 3의 모델을 '거쳐서' 일대일 관계를 맺을 때 사용합니다.

예를 들어, 자동차 정비소 앱에서 각 `Mechanic(정비공)`은 `Car(자동차)`를, 각 차는 `Owner(소유주)`를 가집니다. 정비사와 소유주는 직접 연결되어 있진 않지만, 차를 통해 소유주에 접근할 수 있습니다.

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

이 관계는 `Mechanic` 모델에서 다음과 같이 정의합니다.

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;

    class Mechanic extends Model
    {
        /**
         * 자동차 소유주를 가져옵니다.
         */
        public function carOwner()
        {
            return $this->hasOneThrough(Owner::class, Car::class);
        }
    }

`hasOneThrough`의 첫 번째 인자는 최종적으로 참조할 모델명, 두 번째는 중간 모델명입니다.

<a name="has-one-through-key-conventions"></a>
#### 키 관례

관계 쿼리에 기본적인 Eloquent 외래 키 관례가 적용됩니다. 키를 커스터마이즈하려면 세 번째와 네 번째 매개변수에 외래 키를, 다섯 번째와 여섯 번째에 각각의 로컬 키를 전달할 수 있습니다.

    class Mechanic extends Model
    {
        /**
         * 자동차 소유주를 가져옵니다.
         */
        public function carOwner()
        {
            return $this->hasOneThrough(
                Owner::class,
                Car::class,
                'mechanic_id', // cars 테이블 외래 키
                'car_id', // owners 테이블 외래 키
                'id', // mechanics 테이블 로컬 키
                'id' // cars 테이블 로컬 키
            );
        }
    }

<a name="has-many-through"></a>
### Has Many Through

"has-many-through"는 중간 관계를 통해 멀리 있는 연관 모델들에 쉽게 접근할 수 있게 해줍니다.

예를 들어, 배포 플랫폼을 만든다고 할 때, `Project`는 여러 개의 `Deployment`를 중간 모델 `Environment`를 통해 접근할 수 있습니다.

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

`Project` 모델에서 다음처럼 관계를 정의합니다.

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;

    class Project extends Model
    {
        /**
         * 이 프로젝트의 모든 배포본을 가져옵니다.
         */
        public function deployments()
        {
            return $this->hasManyThrough(Deployment::class, Environment::class);
        }
    }

`hasManyThrough`의 첫 번째 인자는 최종 모델, 두 번째는 중간 모델입니다.

`Deployment` 테이블에는 `project_id`가 없지만, 중간 모델인 `Environment`의 `project_id`를 활용하여 관련 배포본을 찾습니다.

<a name="has-many-through-key-conventions"></a>
#### 키 관례

키를 커스터마이즈하고 싶다면, 추가 인자로 외래 키와 로컬 키 등을 지정할 수 있습니다.

    class Project extends Model
    {
        public function deployments()
        {
            return $this->hasManyThrough(
                Deployment::class,
                Environment::class,
                'project_id',       // environments 테이블 외래 키
                'environment_id',   // deployments 테이블 외래 키
                'id',               // projects 테이블 로컬 키
                'id'                // environments 테이블 로컬 키
            );
        }
    }

<a name="many-to-many"></a>
## 다대다(Many To Many) 관계

다대다 관계는 `hasOne`이나 `hasMany` 보다 조금 더 복잡합니다. 사용자와 역할(roles)의 관계가 그 예입니다. 한 사용자는 여러 역할을 가질 수 있고, 하나의 역할은 여러 사용자에게 할당될 수 있습니다.

<a name="many-to-many-table-structure"></a>
#### 테이블 구조

다대다 관계를 위해선 `users`, `roles`, 그리고 중간 테이블인 `role_user`가 필요합니다. `role_user`는 관련된 모델명을 알파벳순으로 조합해서 만듭니다(`user_id`, `role_id` 컬럼 포함).

이 구조는 다음과 같습니다.

    users
        id - integer
        name - string

    roles
        id - integer
        name - string

    role_user
        user_id - integer
        role_id - integer

<a name="many-to-many-model-structure"></a>
#### 모델 구조

다대다 관계는 `belongsToMany` 메서드 반환값을 리턴하는 메서드로 정의합니다.

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;

    class User extends Model
    {
        /**
         * 이 유저가 가진 모든 역할.
         */
        public function roles()
        {
            return $this->belongsToMany(Role::class);
        }
    }

정의한 후, `roles` 동적 관계 프로퍼티로 역할에 접근할 수 있습니다.

    use App\Models\User;

    $user = User::find(1);

    foreach ($user->roles as $role) {
        //
    }

관계 쿼리에 추가 제약조건을 걸 때도 메서드 체이닝이 가능합니다.

    $roles = User::find(1)->roles()->orderBy('name')->get();

중간 테이블 이름은 관례로 자동 정해지나, 두 번째 인자로 직접 지정할 수 있습니다.

    return $this->belongsToMany(Role::class, 'role_user');

중간 테이블의 키 컬럼명도 직접 오버라이드할 수 있습니다.

    return $this->belongsToMany(Role::class, 'role_user', 'user_id', 'role_id');

<a name="many-to-many-defining-the-inverse-of-the-relationship"></a>
#### 역방향 정의

다대다의 역방향도 같게 정의하되, 모델명만 바꿔줍니다.

    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Model;

    class Role extends Model
    {
        /**
         * 이 역할을 가진 모든 유저.
         */
        public function users()
        {
            return $this->belongsToMany(User::class);
        }
    }

<a name="retrieving-intermediate-table-columns"></a>
### 중간 테이블 컬럼 조회

다대다 관계에서는 중간 테이블에 엑세스할 수 있어야 합니다. Eloquent는 모델의 `pivot` 속성을 통해 이를 지원합니다.

    use App\Models\User;

    $user = User::find(1);

    foreach ($user->roles as $role) {
        echo $role->pivot->created_at;
    }

기본적으로 `pivot`에는 기본 키만 포함됩니다. 추가 컬럼이 필요하다면, 관계 정의 시 `withPivot`을 사용하세요.

    return $this->belongsToMany(Role::class)->withPivot('active', 'created_by');

중간 테이블에 `created_at`, `updated_at`이 필요하다면, `withTimestamps`를 추가하세요.

    return $this->belongsToMany(Role::class)->withTimestamps();

> {note} 자동 타임스탬프 컬럼을 쓸 땐 `created_at`과 `updated_at` 모두 필요합니다.

<a name="customizing-the-pivot-attribute-name"></a>
#### `pivot` 속성명 커스터마이즈

`pivot`이라는 이름의 대신 원하는 이름을 `as` 메서드로 지정할 수 있습니다.

    return $this->belongsToMany(Podcast::class)
                    ->as('subscription')
                    ->withTimestamps();

사용 예:

    $users = User::with('podcasts')->get();

    foreach ($users->flatMap->podcasts as $podcast) {
        echo $podcast->subscription->created_at;
    }

<a name="filtering-queries-via-intermediate-table-columns"></a>
### 중간 테이블 컬럼으로 관계 쿼리 필터링

다음 메서드들을 통해 관계 쿼리를 중간 테이블의 컬럼으로 필터링할 수 있습니다.

- wherePivot
- wherePivotIn
- wherePivotNotIn
- wherePivotBetween
- wherePivotNotBetween
- wherePivotNull
- wherePivotNotNull

예제:

    return $this->belongsToMany(Role::class)
                    ->wherePivot('approved', 1);

    return $this->belongsToMany(Role::class)
                    ->wherePivotIn('priority', [1, 2]);

    return $this->belongsToMany(Podcast::class)
                    ->as('subscriptions')
                    ->wherePivotBetween('created_at', ['2020-01-01 00:00:00', '2020-12-31 00:00:00']);

<a name="defining-custom-intermediate-table-models"></a>
### 커스텀 중간 테이블 모델 정의

다대다 중간 테이블을 표현하는 커스텀 모델을 `using` 메서드로 정의할 수 있습니다.

커스텀 피벗 모델은 `Illuminate\Database\Eloquent\Relations\Pivot`(일반), `Illuminate\Database\Eloquent\Relations\MorphPivot`(폴리모픽) 중 하나를 상속해야 합니다.

정의 예:

    class Role extends Model
    {
        public function users()
        {
            return $this->belongsToMany(User::class)->using(RoleUser::class);
        }
    }

    class RoleUser extends Pivot
    {
        //
    }

> {note} 피벗 모델에서는 `SoftDeletes` 트레이트를 쓸 수 없습니다. 필요하다면 피벗을 일반 모델로 전환하세요.

<a name="custom-pivot-models-and-incrementing-ids"></a>
#### 커스텀 피벗모델과 오토 인크리먼트

만약 커스텀 피벗 모델이 오토 인크리먼트 기본 키를 쓴다면, `$incrementing = true` 프로퍼티를 모델에 지정하세요.

    public $incrementing = true;

<a name="polymorphic-relationships"></a>
## 폴리모픽(Polymorphic) 관계

폴리모픽 관계를 사용하면, 자식 모델이 여러 타입의 모델과 하나의 관계로 연결될 수 있습니다. 예: `Comment` 모델이 `Post`와 `Video` 각각에 속할 수 있음.

<a name="one-to-one-polymorphic-relations"></a>
### 일대일(폴리모픽)

<a name="one-to-one-polymorphic-table-structure"></a>
#### 테이블 구조

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

`imageable_id`는 부모 모델의 id(`Post` 또는 `User`)를, `imageable_type`은 부모 모델의 클래스명을 저장합니다.

<a name="one-to-one-polymorphic-model-structure"></a>
#### 모델 구조

    class Image extends Model
    {
        // 부모 모델(User 또는 Post)와의 폴리모픽 관계
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

<a name="one-to-one-polymorphic-retrieving-the-relationship"></a>
#### 관계 조회

    $post = Post::find(1);
    $image = $post->image;

    $image = Image::find(1);
    $imageable = $image->imageable;

`imageable`은 해당 이미지를 소유한 모델(Post 또는 User) 인스턴스를 반환합니다.

<a name="morph-one-to-one-key-conventions"></a>
#### 키 관례

필요하다면, morphTo에 관계명과 컬럼명을 직접 지정할 수 있습니다.

    public function imageable()
    {
        return $this->morphTo(__FUNCTION__, 'imageable_type', 'imageable_id');
    }

<a name="one-to-many-polymorphic-relations"></a>
### 일대다(폴리모픽)

<a name="one-to-many-polymorphic-table-structure"></a>
#### 테이블 구조

    posts
        id, title, body ...
    videos
        id, title, url ...
    comments
        id, body, commentable_id, commentable_type

<a name="one-to-many-polymorphic-model-structure"></a>
#### 모델 구조

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

<a name="one-to-many-polymorphic-retrieving-the-relationship"></a>
#### 관계 조회

    $post = Post::find(1);
    foreach ($post->comments as $comment) {
        //
    }

    $comment = Comment::find(1);
    $commentable = $comment->commentable;

`commentable`은 해당 댓글의 소유주(Post 또는 Video)를 반환합니다.

<a name="one-of-many-polymorphic-relations"></a>
### One Of Many(폴리모픽)

복수개의 연관 모델 중 "최신" 또는 "가장 오래된" 모델만 참조하고 싶을 때, `morphOne`과 `ofMany` 계열 메서드를 활용합니다.

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

정렬 기준을 변경하여 예를 들어 "좋아요가 가장 많은 이미지"를 찾으려면:

```php
public function bestImage()
{
    return $this->morphOne(Image::class, 'imageable')->ofMany('likes', 'max');
}
```

> {tip} 더욱 고급 사용법은 [has one of many 문서](#advanced-has-one-of-many-relationships)를 참고하세요.

<a name="many-to-many-polymorphic-relations"></a>
### 다대다(폴리모픽)

<a name="many-to-many-polymorphic-table-structure"></a>
#### 테이블 구조

    posts
        id, name ...
    videos
        id, name ...
    tags
        id, name ...
    taggables
        tag_id, taggable_id, taggable_type

> {tip} 기본적인 [many-to-many 관계](#many-to-many)를 먼저 살펴보는 게 좋습니다.

<a name="many-to-many-polymorphic-model-structure"></a>
#### 모델 구조

    class Post extends Model
    {
        public function tags()
        {
            return $this->morphToMany(Tag::class, 'taggable');
        }
    }

<a name="many-to-many-polymorphic-defining-the-inverse-of-the-relationship"></a>
#### 역방향 정의

`Tag` 모델에는 다음처럼 정의합니다.

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

<a name="many-to-many-polymorphic-retrieving-the-relationship"></a>
#### 관계 조회

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

<a name="custom-polymorphic-types"></a>
### 커스텀 폴리모픽 타입

기본적으로 Laravel은 모델의 FQCN(전체 클래스명)을 "타입" 컬럼에 저장합니다. 하지만 모델 이름이 변경되어도 DB가 유효하려면 `enforceMorphMap`으로 커스텀 타입 맵을 지정하세요.

    use Illuminate\Database\Eloquent\Relations\Relation;

    Relation::enforceMorphMap([
        'post' => 'App\Models\Post',
        'video' => 'App\Models\Video',
    ]);

운영 코드에서는 `AppServiceProvider`의 `boot` 메서드 또는 별도 서비스 프로바이더에 작성하세요.

`getMorphClass`, `Relation::getMorphedModel`로 타입명과 FQCN을 상호 변환할 수 있습니다.

> {note} 기존 DB에 morphMap을 도입할 땐 기존 `*_type` 컬럼의 값을 맵 이름으로 변환해야 합니다.

<a name="dynamic-relationships"></a>
### 동적 관계

`resolveRelationUsing` 메서드로 런타임에 관계를 동적으로 정의할 수 있습니다. 일반적인 앱 개발보다 주로 패키지 개발 등 특수 상황에서 유용합니다.

    Order::resolveRelationUsing('customer', function ($orderModel) {
        return $orderModel->belongsTo(Customer::class, 'customer_id');
    });

> {note} 동적 관계 정의 시 항상 명시적으로 키를 지정하세요.

<a name="querying-relations"></a>
## 관계 쿼리하기

모든 Eloquent 관계는 메서드로 정의되어 있으므로, 이를 호출해 조회하지 않고도 관계 인스턴스를 얻을 수 있습니다. 관계는 [쿼리 빌더](/docs/{{version}}/queries)로도 동작해, 실제 SQL을 실행하기 전까지 체이닝이 가능합니다.

예시(`User`가 여러 `Post`를 가질 때):

    class User extends Model
    {
        public function posts()
        {
            return $this->hasMany(Post::class);
        }
    }

    $user = User::find(1);
    $user->posts()->where('active', 1)->get();

관계에 연결된 모든 [쿼리 빌더](/docs/{{version}}/queries) 기능을 사용할 수 있습니다.

<a name="chaining-orwhere-clauses-after-relationships"></a>
#### 관계에서 `orWhere` 체이닝

관계에 조건을 추가할 때, `orWhere` 사용에 주의하세요. `orWhere`는 기존 관계 제약과 묶이지 않을 수 있습니다.

    $user->posts()
            ->where('active', 1)
            ->orWhere('votes', '>=', 100)
            ->get();

이 쿼리는 다음 SQL로 변환됩니다.

```sql
select *
from posts
where user_id = ? and active = 1 or votes >= 100
```

구문상 or 절이 전체 관계와 동등 레벨이므로, 많은 경우 [논리 그룹핑](/docs/{{version}}/queries#logical-grouping)을 사용해야 합니다.

    $user->posts()
            ->where(function (Builder $query) {
                return $query->where('active', 1)
                             ->orWhere('votes', '>=', 100);
            })
            ->get();

위는 아래와 같이 올바른 그룹핑이 적용됩니다.

```sql
select *
from posts
where user_id = ? and (active = 1 or votes >= 100)
```

<a name="relationship-methods-vs-dynamic-properties"></a>
### 관계 메서드 vs. 동적 프로퍼티

추가 조건을 붙일 필요가 없다면, 관계를 프로퍼티처럼 사용할 수 있습니다.

    $user = User::find(1);

    foreach ($user->posts as $post) {
        //
    }

이 "동적 관계 프로퍼티"는 "지연 로딩(lazy loading)"으로, 실제 해당 프로퍼티에 접근할 때 DB 쿼리가 실행됩니다. N+1 문제를 피하기 위해 [즉시 로딩](#eager-loading)을 활용하는 것이 좋습니다.

<a name="querying-relationship-existence"></a>
### 관계 존재에 대한 쿼리

특정 관계가 존재하는 모델만 가져올 때 `has` 와 `orHas` 메서드를 사용하세요.

    $posts = Post::has('comments')->get();

수량 조건도 둘 수 있습니다.

    $posts = Post::has('comments', '>=', 3)->get();

중첩 관계엔 "닷 표기"를 씁니다.

    $posts = Post::has('comments.images')->get();

`whereHas`, `orWhereHas`를 사용하면 관계의 일부 데이터를 조건으로 쓸 수 있습니다.

    $posts = Post::whereHas('comments', function (Builder $query) {
        $query->where('content', 'like', 'code%');
    })->get();

> {note} 관계 존재 쿼리는 동일 DB 내 관계에서만 동작합니다.

<a name="inline-relationship-existence-queries"></a>
#### 인라인 관계 존재 쿼리

단순 조건 하나만 관계에 곁들이는 경우 `whereRelation`, `whereMorphRelation`을 사용할 수 있습니다.

    $posts = Post::whereRelation('comments', 'is_approved', false)->get();

운영자 지정도 가능:

    $posts = Post::whereRelation('comments', 'created_at', '>=', now()->subHour())->get();

<a name="querying-relationship-absence"></a>
### 관계 부재 쿼리

관계가 없는 모델만 뽑고 싶다면 `doesntHave`, `orDoesntHave` 메서드를 사용합니다.

    $posts = Post::doesntHave('comments')->get();

`whereDoesntHave`, `orWhereDoesntHave`로 관계 컬럼별 추가 조건도 줄 수 있습니다.

    $posts = Post::whereDoesntHave('comments', function (Builder $query) {
        $query->where('content', 'like', 'code%');
    })->get();

중첩 관계도 함께 쓸 수 있습니다.

    $posts = Post::whereDoesntHave('comments.author', function (Builder $query) {
        $query->where('banned', 0);
    })->get();

<a name="querying-morph-to-relationships"></a>
### Morph To 관계 쿼리

"morph to" 관계의 존재 조건 쿼리는 `whereHasMorph`, `whereDoesntHaveMorph`를 활용합니다.

    $comments = Comment::whereHasMorph(
        'commentable',
        [Post::class, Video::class],
        function (Builder $query) {
            $query->where('title', 'like', 'code%');
        }
    )->get();

모델 타입별 별도 로직도 `$type` 매개변수로 구현할 수 있습니다.

    $comments = Comment::whereHasMorph(
        'commentable',
        [Post::class, Video::class],
        function (Builder $query, $type) {
            $column = $type === Post::class ? 'content' : 'title';
            $query->where($column, 'like', 'code%');
        }
    )->get();

<a name="querying-all-morph-to-related-models"></a>
#### 모든 관계 타입 쿼리

배열 대신 `*`를 넘기면 DB의 가능한 모든 폴리모픽 타입에 대해 쿼리합니다(Laravel이 추가 쿼리 실행).

    $comments = Comment::whereHasMorph('commentable', '*', function (Builder $query) {
        $query->where('title', 'like', 'foo%');
    })->get();

<a name="aggregating-related-models"></a>
## 연관된 모델 집계

<a name="counting-related-models"></a>
### 연관 모델 개수 세기

연관 모델을 불러오지 않고 수만 셀 때 `withCount`를 사용하세요. 결과 모델에 `{관계}_count` 속성이 생성됩니다.

    $posts = Post::withCount('comments')->get();

여러 관계와 추가 쿼리도 가능합니다.

    $posts = Post::withCount([
        'votes',
        'comments' => function (Builder $query) {
            $query->where('content', 'like', 'code%');
        },
    ])->get();

관계 카운트에 별칭(alias)을 붙여 사용할 수도 있습니다.

    $posts = Post::withCount([
        'comments',
        'comments as pending_comments_count' => function (Builder $query) {
            $query->where('approved', false);
        },
    ])->get();

<a name="deferred-count-loading"></a>
#### 지연 카운트 로딩

이미 검색한 모델에 대해 나중에 카운트를 불러오려면 `loadCount`를 쓰세요.

    $book = Book::first();
    $book->loadCount('genres');

추가 조건도 클로저로 줄 수 있습니다.

    $book->loadCount(['reviews' => function ($query) {
        $query->where('rating', 5);
    }])

<a name="relationship-counting-and-custom-select-statements"></a>
#### Select 절과 조합

`withCount`와 `select`를 함께 쓸 땐 반드시 `select` 다음에 `withCount`를 호출해야 합니다.

    $posts = Post::select(['title', 'body'])
                    ->withCount('comments')
                    ->get();

<a name="other-aggregate-functions"></a>
### 기타 집계 함수

`withCount` 외에도, `withMin`, `withMax`, `withAvg`, `withSum`, `withExists`를 지원합니다. 결과에 `{관계}_{함수}_{컬럼}`이 붙습니다.

    $posts = Post::withSum('comments', 'votes')->get();

별칭 지정도 가능합니다.

    $posts = Post::withSum('comments as total_comments', 'votes')->get();

지연 로딩용 `loadSum` 등도 활용 가능합니다.

    $post = Post::first();
    $post->loadSum('comments', 'votes');

`select`와 함께 쓸 땐 반드시 집계 메서드를 마지막에 호출하세요.

<a name="counting-related-models-on-morph-to-relationships"></a>
### Morph To 관계에서 연관 모델 집계

"morph to" 관계 및 해당 관계가 반환할 각 모델 유형의 관계 카운트를 동시에 eager load할 때, `morphWithCount`를 활용합니다.

    $activities = ActivityFeed::with([
        'parentable' => function (MorphTo $morphTo) {
            $morphTo->morphWithCount([
                Photo::class => ['tags'],
                Post::class => ['comments'],
            ]);
        }])->get();

<a name="morph-to-deferred-count-loading"></a>
#### Morph To의 지연 카운트 로딩

이미 조회한 ActivityFeed 컬렉션이 있을 때, `loadMorphCount`로 추가 카운트를 로딩할 수 있습니다.

    $activities->loadMorphCount('parentable', [
        Photo::class => ['tags'],
        Post::class => ['comments'],
    ]);

<a name="eager-loading"></a>
## 즉시 로딩(Eager Loading)

관계를 동적 프로퍼티로 사용하면 데이터가 "지연 로딩"됩니다(프로퍼티를 실제로 읽을 때 쿼리). Eloquent에서는 조회 시점에 곧바로 관계를 로딩하는 "즉시 로딩" 기능을 제공합니다.

예를 들어, `Book`이 `Author`에 속할 때:

    class Book extends Model
    {
        public function author()
        {
            return $this->belongsTo(Author::class);
        }
    }

일반적으로 다음 코드는 책 수+1 만큼 쿼리가 생성되는 N+1 문제를 발생시킵니다.

    $books = Book::all();

    foreach ($books as $book) {
        echo $book->author->name;
    }

즉시 로딩을 쓰면, 아래처럼 두 번만 쿼리합니다.

    $books = Book::with('author')->get();

    foreach ($books as $book) {
        echo $book->author->name;
    }

실행 쿼리 예시:

```sql
select * from books
select * from authors where id in (1, 2, 3, 4, 5, ...)
```

<a name="eager-loading-multiple-relationships"></a>
#### 여러 관계 한번에 로딩

    $books = Book::with(['author', 'publisher'])->get();

<a name="nested-eager-loading"></a>
#### 중첩(네스티드) 즉시 로딩

"닷 문법"을 쓰면 하위 관계까지 즉시 로딩합니다.

    $books = Book::with('author.contacts')->get();

<a name="nested-eager-loading-morphto-relationships"></a>
#### morphTo 관계의 중첩 로딩

`morphTo`와 추가 관계까지 한 번에 로딩하려면 `morphWith`를 사용합니다.

    $activities = ActivityFeed::query()
        ->with(['parentable' => function (MorphTo $morphTo) {
            $morphTo->morphWith([
                Event::class => ['calendar'],
                Photo::class => ['tags'],
                Post::class => ['author'],
            ]);
        }])->get();

<a name="eager-loading-specific-columns"></a>
#### 특정 컬럼만 즉시 로딩

모든 컬럼이 필요하지 않은 경우, 컬럼 목록을 지정할 수 있습니다.

    $books = Book::with('author:id,name,book_id')->get();

> {note} 항상 `id`와 외래 키도 포함시켜야 합니다.

<a name="eager-loading-by-default"></a>
#### 기본 즉시 로딩

항상 로딩할 관계가 있다면 모델의 `$with` 프로퍼티에 선언하세요.

    class Book extends Model
    {
        protected $with = ['author'];
    }

특정 쿼리에서만 로딩을 뺄 때는 `without`을, 목록을 교체할 땐 `withOnly`를 사용합니다.

    $books = Book::without('author')->get();
    $books = Book::withOnly('genre')->get();

<a name="constraining-eager-loads"></a>
### 즉시 로딩 시 쿼리 제약 조건

관계 로딩 시 특정 조건만 로딩하고 싶으면 배열과 클로저로 처리합니다.

    $users = User::with(['posts' => function ($query) {
        $query->where('title', 'like', '%code%');
    }])->get();

> {note} 즉시 로딩 시엔 `limit`, `take`는 사용할 수 없습니다.

<a name="constraining-eager-loading-of-morph-to-relationships"></a>
#### morphTo 관계 즉시 로딩 쿼리 제약

morphTo 관계 즉시 로딩 시 각 타입별로 쿼리 조건을 줄 수 있습니다.

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

<a name="lazy-eager-loading"></a>
### 지연 즉시 로딩(lazy eager loading)

이미 모델을 조회한 후, 조건에 따라 관계를 추가로 로딩하려면 `load`를 씁니다.

    $books = Book::all();

    if ($someCondition) {
        $books->load('author', 'publisher');
    }

조건부 로딩도 가능합니다.

    $author->load(['books' => function ($query) {
        $query->orderBy('published_date', 'asc');
    }]);

아직 로딩되지 않은 관계만 추가 로딩할 때는 `loadMissing`을 사용하세요.

    $book->loadMissing('author');

<a name="nested-lazy-eager-loading-morphto"></a>
#### morphTo 관계의 지연 즉시 로딩

`loadMorph`로 다양한 morphTo 관계의 하위 관계를 한 번에 로딩할 수 있습니다.

    $activities = ActivityFeed::with('parentable')
        ->get()
        ->loadMorph('parentable', [
            Event::class => ['calendar'],
            Photo::class => ['tags'],
            Post::class => ['author'],
        ]);

<a name="preventing-lazy-loading"></a>
### 지연 로딩 방지

즉시 로딩으로 성능을 최적화하고 싶다면, 로컬/스테이징/테스트 등 개발 환경에서 지연 로딩을 강제로 막을 수 있습니다. `preventLazyLoading`을 호출하면, Eloquent는 지연 로딩 시 예외를 발생시킵니다. 주로 `AppServiceProvider`의 `boot`에서 사용합니다.

```php
use Illuminate\Database\Eloquent\Model;

public function boot()
{
    Model::preventLazyLoading(! $this->app->isProduction());
}
```

로깅만 하고 예외를 발생시키지 않을 수도 있습니다.

```php
Model::handleLazyLoadingViolationUsing(function ($model, $relation) {
    $class = get_class($model);

    info("Attempted to lazy load [{$relation}] on model [{$class}].");
});
```

<a name="inserting-and-updating-related-models"></a>
## 연관된 모델 삽입 & 갱신

<a name="the-save-method"></a>
### `save` 메서드

Eloquent는 관계 모델에 새로운 모델을 추가하는데 편리한 메서드들을 지원합니다. 예를 들어, 새로운 댓글을 게시글에 추가할 땐 다음처럼 할 수 있습니다.

    $comment = new Comment(['message' => 'A new comment.']);
    $post = Post::find(1);
    $post->comments()->save($comment);

`comments`를 동적 프로퍼티로 사용하는 게 아니라, 메서드로 호출해 관계 인스턴스를 얻어 `save`를 실행해야 합니다.

여러 개를 한 번에 저장할 땐 `saveMany`를 사용합니다.

    $post->comments()->saveMany([
        new Comment(['message' => 'A new comment.']),
        new Comment(['message' => 'Another new comment.']),
    ]);

이렇게 저장해도, 이미 로드된 부모의 관계 in-memory에는 즉시 반영되지 않습니다. 새로고침하려면 `refresh`를 써야 합니다.

    $post->comments()->save($comment);
    $post->refresh();
    $post->comments;

<a name="the-push-method"></a>
#### 모델과 관계의 재귀적 저장

모델과 연결된 모든 관계까지 재귀적으로 저장하려면 `push`를 활용하세요.

    $post = Post::find(1);

    $post->comments[0]->message = 'Message';
    $post->comments[0]->author->name = 'Author Name';

    $post->push();

<a name="the-create-method"></a>
### `create` 메서드

`save`, `saveMany`와 달리, `create`메서드는 배열을 받아 새 모델을 바로 삽입 & 반환합니다.

    $comment = $post->comments()->create([
        'message' => 'A new comment.',
    ]);

여러 개를 생성할 땐 `createMany`:

    $post->comments()->createMany([
        ['message' => 'A new comment.'],
        ['message' => 'Another new comment.'],
    ]);

`findOrNew`, `firstOrNew`, `firstOrCreate`, `updateOrCreate` 등도 활용할 수 있습니다.

> {tip} `create`를 사용하기 전에 [대량 할당(Mass Assignment)](/docs/{{version}}/eloquent#mass-assignment) 문서를 반드시 참고하세요.

<a name="updating-belongs-to-relationships"></a>
### Belongs To 관계

자식 모델을 새로운 부모 모델에 연결하려면 `associate`를 쓰세요.

    $account = Account::find(10);

    $user->account()->associate($account);
    $user->save();

연결을 해제하려면 `dissociate`:

    $user->account()->dissociate();
    $user->save();

<a name="updating-many-to-many-relationships"></a>
### 다대다 관계

<a name="attaching-detaching"></a>
#### 연결/해제(Attaching/Detaching)

`attach`로 다대다 연결 관계를 추가합니다(중간 테이블에 레코드 삽입).

    $user->roles()->attach($roleId);

추가 중간 테이블 컬럼도 전달할 수 있습니다.

    $user->roles()->attach($roleId, ['expires' => $expires]);

연결 해제(`detach`):

    $user->roles()->detach($roleId); // 한 개
    $user->roles()->detach();        // 모두

배열로도 가능합니다.

    $user->roles()->detach([1, 2, 3]);
    $user->roles()->attach([
        1 => ['expires' => $expires],
        2 => ['expires' => $expires],
    ]);

<a name="syncing-associations"></a>
#### 동기화(Sync) 메서드

`sync`로 원하는 ID 배열만 남도록 자동 동기화할 수 있습니다.

    $user->roles()->sync([1, 2, 3]);

피벗 값 추가도 가능:

    $user->roles()->sync([1 => ['expires' => true], 2, 3]);

동일한 값으로 모두 동기화하려면 `syncWithPivotValues`를 사용하세요.

    $user->roles()->syncWithPivotValues([1, 2, 3], ['active' => true]);

만약 기존 연결을 해제하지 않으려면 `syncWithoutDetaching`:

    $user->roles()->syncWithoutDetaching([1, 2, 3]);

<a name="toggling-associations"></a>
#### 토글(Toggle)

`toggle`로 연결된 것은 해제, 해제된 것은 연결할 수 있습니다.

    $user->roles()->toggle([1, 2, 3]);

<a name="updating-a-record-on-the-intermediate-table"></a>
#### 중간 테이블 레코드 갱신

중간 테이블 데이터를 갱신하려면 `updateExistingPivot`을 사용하세요.

    $user->roles()->updateExistingPivot($roleId, [
        'active' => false,
    ]);

<a name="touching-parent-timestamps"></a>
## 부모 타임스탬프 갱신(Touching Parent Timestamps)

`belongsTo`, `belongsToMany` 관계를 갖는 자식이 갱신될 때 부모의 `updated_at`도 자동 갱신될 수 있습니다.

아래와 같이 자식 모델에 `touches` 프로퍼티에 관계명을 설정하면, 자식이 갱신될 때 부모의 `updated_at`도 자동 갱신됩니다.

    class Comment extends Model
    {
        /**
         * 변경시 함께 갱신할 관계들.
         *
         * @var array
         */
        protected $touches = ['post'];

        public function post()
        {
            return $this->belongsTo(Post::class);
        }
    }

> {note} 부모 모델의 타임스탬프는 오로지 Eloquent의 `save` 메서드로 자식 모델을 갱신할 때만 적용됩니다.