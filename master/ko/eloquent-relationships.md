# Eloquent: 관계(Relationships)

- [소개](#introduction)
- [관계 정의하기](#defining-relationships)
    - [일대일 / hasOne](#one-to-one)
    - [일대다 / hasMany](#one-to-many)
    - [일대다(반대) / belongsTo](#one-to-many-inverse)
    - [Has One of Many](#has-one-of-many)
    - [Has One Through](#has-one-through)
    - [Has Many Through](#has-many-through)
- [스코프 관계](#scoped-relationships)
- [다대다 관계](#many-to-many)
    - [중간 테이블 컬럼 조회](#retrieving-intermediate-table-columns)
    - [중간 테이블 컬럼으로 쿼리 필터링](#filtering-queries-via-intermediate-table-columns)
    - [중간 테이블 컬럼으로 쿼리 정렬](#ordering-queries-via-intermediate-table-columns)
    - [커스텀 중간 테이블 모델 정의](#defining-custom-intermediate-table-models)
- [폴리모픽 관계](#polymorphic-relationships)
    - [일대일](#one-to-one-polymorphic-relations)
    - [일대다](#one-to-many-polymorphic-relations)
    - [One of Many](#one-of-many-polymorphic-relations)
    - [다대다](#many-to-many-polymorphic-relations)
    - [커스텀 폴리모픽 타입](#custom-polymorphic-types)
- [동적 관계](#dynamic-relationships)
- [관계 쿼리](#querying-relations)
    - [관계 메소드와 동적 프로퍼티](#relationship-methods-vs-dynamic-properties)
    - [관계 존재 쿼리](#querying-relationship-existence)
    - [관계 부재 쿼리](#querying-relationship-absence)
    - [Morph To 관계 쿼리](#querying-morph-to-relationships)
- [연관 모델 집계](#aggregating-related-models)
    - [연관 모델 카운트](#counting-related-models)
    - [기타 집계함수](#other-aggregate-functions)
    - [Morph To 관계의 연관 모델 카운트](#counting-related-models-on-morph-to-relationships)
- [즉시 로딩(Eager Loading)](#eager-loading)
    - [즉시 로딩 제약](#constraining-eager-loads)
    - [지연 즉시 로딩(Lazy Eager Loading)](#lazy-eager-loading)
    - [Lazy Loading 방지](#preventing-lazy-loading)
- [연관 모델 추가 및 갱신](#inserting-and-updating-related-models)
    - [`save` 메소드](#the-save-method)
    - [`create` 메소드](#the-create-method)
    - [Belongs To 관계](#updating-belongs-to-relationships)
    - [Many to Many 관계](#updating-many-to-many-relationships)
- [부모 타임스탬프 업데이트](#touching-parent-timestamps)

<a name="introduction"></a>
## 소개

데이터베이스 테이블은 종종 서로 관련되어 있습니다. 예를 들어, 블로그 게시글에는 여러 개의 댓글이 있을 수 있고 주문은 주문한 사용자와 연결될 수 있습니다. Eloquent는 이러한 관계를 간편하게 관리하고 작업할 수 있게 해주며, 다양한 일반적인 관계를 지원합니다:

<div class="content-list" markdown="1">

- [일대일(One To One)](#one-to-one)
- [일대다(One To Many)](#one-to-many)
- [다대다(Many To Many)](#many-to-many)
- [Has One Through](#has-one-through)
- [Has Many Through](#has-many-through)
- [일대일 - 폴리모픽(One To One (Polymorphic))](#one-to-one-polymorphic-relations)
- [일대다 - 폴리모픽(One To Many (Polymorphic))](#one-to-many-polymorphic-relations)
- [다대다 - 폴리모픽(Many To Many (Polymorphic))](#many-to-many-polymorphic-relations)

</div>

<a name="defining-relationships"></a>
## 관계 정의하기

Eloquent 관계는 Eloquent 모델 클래스의 메소드로 정의합니다. 관계는 [쿼리 빌더](/docs/{{version}}/queries)로도 작동하므로, 메소드 체이닝과 강력한 쿼리 기능을 제공합니다. 예를 들어, `posts` 관계에 추가 쿼리 제약을 체이닝할 수 있습니다:

```php
$user->posts()->where('active', 1)->get();
```

관계를 본격적으로 활용하기 전에, Eloquent가 지원하는 각 관계 유형을 어떻게 정의하는지 배워봅시다.

<a name="one-to-one"></a>
### 일대일 / hasOne

일대일(One-to-One) 관계는 가장 기본적인 데이터베이스 관계입니다. 예를 들어, `User` 모델은 하나의 `Phone` 모델과 연결될 수 있습니다. 이 관계를 정의하려면, `User` 모델에 `phone` 메소드를 추가하면 됩니다. 이 메소드에서 `hasOne`를 호출하여 반환합니다. `hasOne` 메소드는 모델의 `Illuminate\Database\Eloquent\Model` 베이스 클래스를 통해 제공됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasOne;

class User extends Model
{
    /**
     * 사용자와 연결된 전화번호 가져오기
     */
    public function phone(): HasOne
    {
        return $this->hasOne(Phone::class);
    }
}
```

`hasOne` 메소드에 넘기는 첫 번째 인자는 연관된 모델 클래스의 이름입니다. 관계를 정의하면, Eloquent의 동적 프로퍼티를 사용해 연관 레코드를 조회할 수 있습니다. 동적 프로퍼티를 사용하면 마치 모델에 정의된 프로퍼티처럼 관계 메소드를 접근할 수 있습니다:

```php
$phone = User::find(1)->phone;
```

Eloquent는 부모 모델명을 기준으로 외래 키를 결정합니다. 이 예시에서는 `Phone` 모델에 자동으로 `user_id` 외래 키가 있다고 가정합니다. 이 규칙을 오버라이드하려면, 두 번째 인자로 외래 키를 지정할 수 있습니다:

```php
return $this->hasOne(Phone::class, 'foreign_key');
```

또한 Eloquent는 외래 키 값이 기본적으로 부모의 기본키 컬럼(`id`) 값을 가진다고 가정합니다. 만약 `id` 외의 컬럼을 사용하거나 모델의 `$primaryKey` 값을 다르게 설정하고 싶다면 세 번째 인자로 로컬 키를 지정할 수 있습니다:

```php
return $this->hasOne(Phone::class, 'foreign_key', 'local_key');
```

<a name="one-to-one-defining-the-inverse-of-the-relationship"></a>
#### 관계의 반대 정의하기

이제 `User` 모델에서 `Phone` 모델을 접근할 수 있습니다. 다음으로 `Phone` 모델에서 해당 전화번호의 주인인 사용자를 찾을 수 있도록 관계를 정의해봅시다. `hasOne` 관계의 역방향은 `belongsTo` 메소드로 정의할 수 있습니다:

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

`user` 메소드를 호출하면, Eloquent는 `user_id` 컬럼이 `id`와 일치하는 `User` 모델을 찾아 반환합니다.

Eloquent는 관계 메소드 이름에 `_id`를 붙여 외래 키 명을 추정합니다. 그래서 위 예제에서는 `Phone` 모델에 `user_id` 컬럼이 있다고 가정합니다. 만약 외래 키가 다르다면 두 번째 인자로 직접 지정할 수 있습니다:

```php
/**
 * 이 전화번호의 소유자 찾기
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class, 'foreign_key');
}
```

부모 모델의 기본키가 `id`가 아니거나 다른 컬럼으로 관계를 찾으려면 세 번째 인자로 부모 테이블의 키를 지정할 수 있습니다:

```php
/**
 * 이 전화번호의 소유자 찾기
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class, 'foreign_key', 'owner_key');
}
```

<a name="one-to-many"></a>
### 일대다 / hasMany

일대다(One-to-Many) 관계는 한 모델이 여러 자식 모델을 가질 때 사용합니다. 예를 들어, 블로그 게시물 하나에는 거의 무제한의 댓글이 있을 수 있습니다. 다른 Eloquent 관계와 마찬가지로, 일대다 관계도 모델에 메소드를 정의하여 만듭니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Post extends Model
{
    /**
     * 블로그 글의 댓글 가져오기
     */
    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class);
    }
}
```

Eloquent는 `Comment` 모델의 올바른 외래 키 컬럼을 자동으로 결정합니다. 관례상, 부모 모델의 스네이크케이스 이름에 `_id`를 붙인 값이 사용됩니다. 그래서 이 예시에서는 `Comment` 모델의 외래 키가 `post_id`라고 가정합니다.

관계 메소드 정의 후, Eloquent의 [컬렉션](/docs/{{version}}/eloquent-collections) 기능으로 연관 댓글을 접근할 수 있습니다. 동적 관계 프로퍼티를 통해 다음처럼 접근합니다:

```php
use App\Models\Post;

$comments = Post::find(1)->comments;

foreach ($comments as $comment) {
    // ...
}
```

관계 메소드도 쿼리 빌더이므로, 메소드 호출로 추가 조건을 체이닝할 수 있습니다:

```php
$comment = Post::find(1)->comments()
    ->where('title', 'foo')
    ->first();
```

`hasOne` 과 마찬가지로, `hasMany`에 외래 키와 로컬 키를 추가 인수로 지정할 수 있습니다:

```php
return $this->hasMany(Comment::class, 'foreign_key');

return $this->hasMany(Comment::class, 'foreign_key', 'local_key');
```

<a name="automatically-hydrating-parent-models-on-children"></a>
#### 자식 모델에 부모 모델 자동 할당하기

Eloquent 즉시 로딩을 활용하더라도, 자식 모델의 루프 내에서 부모 모델을 접근하면 "N + 1" 쿼리 문제가 생길 수 있습니다:

```php
$posts = Post::with('comments')->get();

foreach ($posts as $post) {
    foreach ($post->comments as $comment) {
        echo $comment->post->title;
    }
}
```

위 예시에서는 각 `Comment`에서 부모 `Post`를 다시 로드하기 때문에 N+1문제가 발생합니다.

Eloquent가 부모 모델을 자식 모델에 자동으로 할당하게 하려면, `hasMany` 관계 정의시 `chaperone` 메소드를 사용하세요:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Post extends Model
{
    /**
     * 블로그 글의 댓글 가져오기
     */
    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class)->chaperone();
    }
}
```

또는, 런타임에 즉시 로딩시 `chaperone`을 사용해 자동 할당을 opt-in 할 수 있습니다:

```php
use App\Models\Post;

$posts = Post::with([
    'comments' => fn ($comments) => $comments->chaperone(),
])->get();
```

<a name="one-to-many-inverse"></a>
### 일대다(반대) / belongsTo

이제 글의 댓글 전체를 조회할 수 있으므로, 각 댓글이 자신의 부모 글에 접근하도록 관계를 정의하겠습니다. 자식 모델에 `belongsTo` 메소드를 정의하세요:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Comment extends Model
{
    /**
     * 이 댓글이 속한 게시글 가져오기
     */
    public function post(): BelongsTo
    {
        return $this->belongsTo(Post::class);
    }
}
```

정의후, 댓글 인스턴스를 통해 부모 글에 접근할 수 있습니다:

```php
use App\Models\Comment;

$comment = Comment::find(1);

return $comment->post->title;
```

Eloquent는 기본적으로 관계 메소드 이름에 `_`와 부모 모델의 기본키명을 붙여서 외래 키를 추정합니다. 즉, 이 경우엔 `post_id`입니다.

관례를 따르지 않을 경우 두 번째 인자로 외래 키 이름을 지정할 수 있습니다:

```php
/**
 * 이 댓글이 속한 게시글 가져오기
 */
public function post(): BelongsTo
{
    return $this->belongsTo(Post::class, 'foreign_key');
}
```

부모 모델의 기본 키가 `id`가 아니라면 세 번째 인자로 지정할 수 있습니다:

```php
/**
 * 이 댓글이 속한 게시글 가져오기
 */
public function post(): BelongsTo
{
    return $this->belongsTo(Post::class, 'foreign_key', 'owner_key');
}
```

<a name="default-models"></a>
#### 기본 모델(Default Models)

`belongsTo`, `hasOne`, `hasOneThrough`, `morphOne` 관계에서는 관계가 `null`일 때 반환될 기본 모델을 지정할 수 있습니다. 이 방법은 [Null Object 패턴](https://en.wikipedia.org/wiki/Null_Object_pattern)이라고 하며 조건 검사를 줄여줍니다. 예를 들어, 아래처럼 `user` 관계는 `Post` 모델에 연결된 사용자가 없을 경우 빈 `App\Models\User` 모델을 반환합니다:

```php
/**
 * 글의 작성자 가져오기
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault();
}
```

기본 모델에 속성을 채우려면 배열이나 클로저를 `withDefault`에 인자로 줄 수 있습니다:

```php
/**
 * 글의 작성자
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault([
        'name' => 'Guest Author',
    ]);
}

/**
 * 글의 작성자
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault(function (User $user, Post $post) {
        $user->name = 'Guest Author';
    });
}
```

<a name="querying-belongs-to-relationships"></a>
#### Belongs To 관계 쿼리

"belongs to" 관계의 자식 모델을 쿼리할 때, `where` 절을 수동으로 작성할 수 있습니다:

```php
use App\Models\Post;

$posts = Post::where('user_id', $user->id)->get();
```

더 간단하게 사용할 수 있는 `whereBelongsTo` 메소드도 있습니다. 이 메소드는 관계와 외래 키를 자동으로 판단합니다:

```php
$posts = Post::whereBelongsTo($user)->get();
```

[컬렉션](/docs/{{version}}/eloquent-collections)도 `whereBelongsTo`에 줄 수 있습니다. 이 경우 컬렉션 내의 부모 모델들을 참조하는 자식 모델을 모두 조회합니다:

```php
$users = User::where('vip', true)->get();

$posts = Post::whereBelongsTo($users)->get();
```

기본적으로 모델의 클래스명으로 관계를 추정하는데, 두 번째 인자로 수동 지정할 수 있습니다:

```php
$posts = Post::whereBelongsTo($user, 'author')->get();
```

<!-- 이하 생략된 부분도 동일한 번역 원칙을 따라 계속 번역하실 수 있습니다. 필요하다면 이어서 요청해주세요. -->

---

> ⚡ 본문이 매우 길어 일부까지만 번역했습니다. 이어서 더 필요하신 특정 섹션을 지정해주시면 연결해서 번역해 드리겠습니다!  
> 이 마크다운의 번역 스타일과 용어 준수 기준도 계속 유지됩니다.