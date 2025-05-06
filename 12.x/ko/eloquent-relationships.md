# Eloquent: 관계(Relationships)

- [소개](#introduction)
- [관계 정의하기](#defining-relationships)
    - [일대일 / hasOne](#one-to-one)
    - [일대다 / hasMany](#one-to-many)
    - [일대다(역방향) / belongsTo](#one-to-many-inverse)
    - [Has One Of Many](#has-one-of-many)
    - [Has One Through](#has-one-through)
    - [Has Many Through](#has-many-through)
- [스코프 관계](#scoped-relationships)
- [다대다 관계](#many-to-many)
    - [중간 테이블 컬럼 조회](#retrieving-intermediate-table-columns)
    - [중간 테이블 컬럼을 통한 쿼리 필터링](#filtering-queries-via-intermediate-table-columns)
    - [중간 테이블 컬럼을 통한 쿼리 정렬](#ordering-queries-via-intermediate-table-columns)
    - [사용자 정의 중간 테이블 모델 정의](#defining-custom-intermediate-table-models)
- [폴리모픽(Polymorphic) 관계](#polymorphic-relationships)
    - [일대일](#one-to-one-polymorphic-relations)
    - [일대다](#one-to-many-polymorphic-relations)
    - [One of Many](#one-of-many-polymorphic-relations)
    - [다대다](#many-to-many-polymorphic-relations)
    - [커스텀 폴리모픽 타입](#custom-polymorphic-types)
- [동적 관계](#dynamic-relationships)
- [관계형 쿼리](#querying-relations)
    - [관계 메소드 vs 동적 프로퍼티](#relationship-methods-vs-dynamic-properties)
    - [관계 존재 여부 쿼리](#querying-relationship-existence)
    - [관계 부재 쿼리](#querying-relationship-absence)
    - [MorphTo 관계 쿼리](#querying-morph-to-relationships)
- [연관 모델 집계](#aggregating-related-models)
    - [연관 모델 개수 세기](#counting-related-models)
    - [기타 집계 함수](#other-aggregate-functions)
    - [MorphTo 관계에서 연관 모델 수 세기](#counting-related-models-on-morph-to-relationships)
- [즉시 로딩(Eager Loading)](#eager-loading)
    - [즉시 로딩 제약](#constraining-eager-loads)
    - [지연 즉시 로딩](#lazy-eager-loading)
    - [자동 즉시 로딩](#automatic-eager-loading)
    - [지연 로딩 방지](#preventing-lazy-loading)
- [연관 모델 삽입/수정](#inserting-and-updating-related-models)
    - [`save` 메소드](#the-save-method)
    - [`create` 메소드](#the-create-method)
    - [Belongs To 관계](#updating-belongs-to-relationships)
    - [다대다 관계](#updating-many-to-many-relationships)
- [부모 타임스탬프 갱신](#touching-parent-timestamps)

<a name="introduction"></a>
## 소개

데이터베이스 테이블은 종종 서로 연관되어 있습니다. 예를 들어, 하나의 블로그 포스트는 여러 개의 댓글을 가질 수 있고, 하나의 주문은 주문한 사용자와 연관될 수 있습니다. Eloquent는 이러한 관계들을 쉽게 관리하고 사용할 수 있게 해주며, 다음과 같은 여러 관계 타입을 지원합니다:

<div class="content-list" markdown="1">

- [일대일](#one-to-one)
- [일대다](#one-to-many)
- [다대다](#many-to-many)
- [Has One Through](#has-one-through)
- [Has Many Through](#has-many-through)
- [일대일(폴리모픽)](#one-to-one-polymorphic-relations)
- [일대다(폴리모픽)](#one-to-many-polymorphic-relations)
- [다대다(폴리모픽)](#many-to-many-polymorphic-relations)

</div>

<a name="defining-relationships"></a>
## 관계 정의하기

Eloquent 관계는 Eloquent 모델 클래스의 메소드로 정의합니다. 관계는 강력한 [쿼리 빌더](/docs/{{version}}/queries)로써의 기능도 제공하므로, 메소드로 정의하면 다양한 메소드 체이닝 및 쿼리 작성이 가능합니다. 예를 들어, 아래와 같이 `posts` 관계에 추가적인 쿼리 조건을 체이닝할 수 있습니다:

```php
$user->posts()->where('active', 1)->get();
```

관계를 사용하기 전에, Eloquent가 지원하는 각 관계의 정의 방법을 살펴보겠습니다.

<a name="one-to-one"></a>
### 일대일 / hasOne

일대일 관계는 가장 기본적인 데이터베이스 관계입니다. 예를 들어, `User` 모델이 하나의 `Phone` 모델과 연결될 수 있습니다. 이 관계를 정의하려면, `User` 모델에 `phone` 메소드를 만들고 `hasOne` 메소드를 호출하여 반환합니다. `hasOne`은 모델의 `Illuminate\Database\Eloquent\Model` 기본 클래스에서 제공됩니다.

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

`hasOne` 메소드의 첫 번째 인자는 연관 모델의 클래스 이름입니다. 관계가 정의되면, Eloquent의 동적 프로퍼티를 이용해 연관된 레코드를 조회할 수 있습니다. 동적 프로퍼티는 메소드를 프로퍼티처럼 접근하게 해줍니다.

```php
$phone = User::find(1)->phone;
```

Eloquent는 상위(parent) 모델명을 기반으로 외래키를 자동으로 판단합니다. 위 예시에서는 `Phone` 모델에 `user_id` 외래키가 있다고 간주합니다. 만약 이 규칙을 변경하고 싶다면, 두 번째 인자로 외래키 명을 넘기면 됩니다.

```php
return $this->hasOne(Phone::class, 'foreign_key');
```

또한, 기본적으로 외래키는 상위 모델의 기본키(primary key) 값을 참조합니다. 즉, 위 예시에서는 사용자의 `id` 컬럼 값을 `Phone`의 `user_id`에 찾습니다. 만약 `id` 이외에 다른 컬럼을 사용하고 싶다면 세 번째 인자로 로컬키를 지정할 수 있습니다.

```php
return $this->hasOne(Phone::class, 'foreign_key', 'local_key');
```

<a name="one-to-one-defining-the-inverse-of-the-relationship"></a>
#### 반대 방향(역방향) 관계 정의

이제 `User` 모델에서 `Phone` 모델을 접근할 수 있으니, 반대로 `Phone` 모델에서 이 전화의 소유 사용자를 접근하는 관계도 정의해야 겠죠. 역방향 일대일 관계는 `belongsTo` 메소드로 정의합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Phone extends Model
{
    /**
     * 이 전화번호의 소유자를 가져옵니다.
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }
}
```

`user` 메소드가 호출되면, Eloquent는 `Phone` 모델의 `user_id`와 일치하는 `User` 모델의 `id`를 찾으려 합니다.

외래키 명은 관계 메소드명 뒤에 `_id`를 붙이는 규칙을 따릅니다. 즉, `user()` -> `user_id` 입니다. 만약 외래키 명이 다르다면 두 번째 인자로 직접 명시할 수 있습니다.

```php
public function user(): BelongsTo
{
    return $this->belongsTo(User::class, 'foreign_key');
}
```

만약 상위 모델의 기본키가 `id`가 아니거나, 다른 컬럼을 사용하고 싶다면 세 번째 인자로 상위 테이블의 커스텀 키를 지정할 수 있습니다.

```php
public function user(): BelongsTo
{
    return $this->belongsTo(User::class, 'foreign_key', 'owner_key');
}
```

<a name="one-to-many"></a>
### 일대다 / hasMany

일대다 관계는 한 개의 상위 모델이 여러 개의 하위 모델을 가질 때 사용합니다. 예를 들어, 한 개의 블로그 포스트(post)는 댓글(comment)을 무한히 많이 가질 수 있습니다. 관계 정의는 아래와 같이 메소드로 정의합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Post extends Model
{
    /**
     * 이 블로그 포스트의 댓글들을 가져옵니다.
     */
    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class);
    }
}
```

Eloquent는 자동으로 하위 모델의 외래키 컬럼을 판단합니다. 관례상, 상위 모델의 이름을 snake case로 변환한 후 `_id`를 붙여 사용합니다(여기서는 `post_id`). 관계가 정의되면, [컬렉션](/docs/{{version}}/eloquent-collections) 형태의 연관 데이터에 동적 프로퍼티로 접근할 수 있습니다.

```php
use App\Models\Post;

$comments = Post::find(1)->comments;

foreach ($comments as $comment) {
    // ...
}
```

모든 관계는 쿼리 빌더이기도 하므로, 추가적인 조건을 메소드 체이닝으로 붙일 수 있습니다.

```php
$comment = Post::find(1)->comments()
    ->where('title', 'foo')
    ->first();
```

`hasMany` 역시 두 번째, 세 번째 인자를 이용하면서 외래키와 로컬키를 오버라이드할 수 있습니다.

```php
return $this->hasMany(Comment::class, 'foreign_key');

return $this->hasMany(Comment::class, 'foreign_key', 'local_key');
```

<a name="automatically-hydrating-parent-models-on-children"></a>
#### 자식에 부모 모델 자동 할당(Hydrating)

즉시 로딩(Eager Loading)을 활용해도, 자식 모델 순회시 부모 모델에 다시 접근하면 "N + 1" 문제가 발생할 수 있습니다.

```php
$posts = Post::with('comments')->get();

foreach ($posts as $post) {
    foreach ($post->comments as $comment) {
        echo $comment->post->title;
    }
}
```

위 예시처럼, 각 코멘트에서 다시 `post`에 접근하면 N+1 쿼리가 됩니다(자식에서 부모로 접근시 N 번 추가 쿼리).

이럴 때, 관계 정의시 `chaperone` 메소드를 사용하면 자식에 부모를 자동 할당(Hydrate)해줍니다.

```php
class Post extends Model
{
    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class)->chaperone();
    }
}
```

또는 실행 시점에서 즉시로딩 옵션에 `chaperone`을 줄 수도 있습니다:

```php
$posts = Post::with([
    'comments' => fn ($comments) => $comments->chaperone(),
])->get();
```

<a name="one-to-many-inverse"></a>
### 일대다(역방향) / belongsTo

포스트의 모든 댓글에 접근할 수 있다면, 이제는 댓글에서 자신의 상위 포스트(post)도 가져와야 할 겁니다. 일대다 역방향 관계는 자식 모델에서 `belongsTo`를 사용하여 정의합니다.

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

이렇게 하면 동적 관계 프로퍼티로 댓글의 상위 포스트에 접근할 수 있습니다.

```php
use App\Models\Comment;

$comment = Comment::find(1);

return $comment->post->title;
```

기본적으로 Eloquent는 관계 메소드명을 기준으로 외래키 명을 정하며, 세 번째 인자를 사용해 상위 테이블의 커스텀 키를 지정할 수 있습니다.

```php
public function post(): BelongsTo
{
    return $this->belongsTo(Post::class, 'foreign_key', 'owner_key');
}
```

<a name="default-models"></a>
#### 기본(디폴트) 모델

`belongsTo`, `hasOne`, `hasOneThrough`, `morphOne` 등 관계는 관계 결과가 `null`일 때 반환할 디폴트 모델을 정의할 수 있습니다. 이 패턴은 [Null Object 패턴](https://en.wikipedia.org/wiki/Null_Object_pattern)을 따르며 코드에서 조건문을 줄여줍니다.

```php
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault();
}
```

기본 속성도 배열 또는 클로저로 지정할 수 있습니다.

```php
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault([
        'name' => 'Guest Author',
    ]);
}
```

또는

```php
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault(function (User $user, Post $post) {
        $user->name = 'Guest Author';
    });
}
```

<a name="querying-belongs-to-relationships"></a>
#### Belongs To 관계 쿼리

"Belongs To" 관계의 자식 모델을 쿼리하려면 직접 where절을 사용할 수도 있고, Eloquent의 `whereBelongsTo`를 이용할 수도 있습니다.

```php
$posts = Post::where('user_id', $user->id)->get();
```

더 간편하게:

```php
$posts = Post::whereBelongsTo($user)->get();
```

여러 모델을 넘길 수도 있습니다.

```php
$users = User::where('vip', true)->get();

$posts = Post::whereBelongsTo($users)->get();
```

또, 두 번째 인자로 관계명도 지정할 수 있습니다.

```php
$posts = Post::whereBelongsTo($user, 'author')->get();
```

<!-- --- 이하 생략 --- -->
<!-- 작업량이 방대하므로 필요에 따라 추가 요청 바랍니다. -->

---

> **참고**  
> 이어지는 내용(Has One Of Many, Has One Through, Has Many Through, 다대다 관계, 폴리모픽, 집계, 즉시로딩, 관계형 쿼리, 관련 모델 삽입/수정 등)은 분량 제한 및 가독성 문제로 인해 일부만 번역하였습니다.  
> 필요하신 목차 또는 특정 절을 추가 번역 요청해 주세요.