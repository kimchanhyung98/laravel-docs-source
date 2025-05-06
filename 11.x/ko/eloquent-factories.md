# Eloquent: 팩토리(Factory)

- [소개](#introduction)
- [모델 팩토리 정의하기](#defining-model-factories)
    - [팩토리 생성하기](#generating-factories)
    - [팩토리 상태(state)](#factory-states)
    - [팩토리 콜백(callback)](#factory-callbacks)
- [팩토리를 이용한 모델 생성](#creating-models-using-factories)
    - [모델 인스턴스화](#instantiating-models)
    - [모델 영속화](#persisting-models)
    - [시퀀스(Sequences)](#sequences)
- [팩토리 관계 정의](#factory-relationships)
    - [Has Many 관계](#has-many-relationships)
    - [Belongs To 관계](#belongs-to-relationships)
    - [Many to Many(다대다) 관계](#many-to-many-relationships)
    - [폴리모픽 관계](#polymorphic-relationships)
    - [팩토리 내 관계 정의](#defining-relationships-within-factories)
    - [관계를 위한 기존 모델 재활용](#recycling-an-existing-model-for-relationships)

<a name="introduction"></a>
## 소개

애플리케이션을 테스트하거나 데이터베이스에 시딩(seeding)할 때, 몇 개의 레코드를 데이터베이스에 삽입해야 할 수 있습니다. 각 컬럼의 값을 직접 지정하는 대신, Laravel은 [Eloquent 모델](/docs/{{version}}/eloquent)마다 기본 속성 집합을 모델 팩토리로 정의할 수 있도록 지원합니다.

팩토리를 작성하는 예시는 애플리케이션의 `database/factories/UserFactory.php` 파일을 참고하면 됩니다. 이 팩토리는 모든 새로운 Laravel 애플리케이션에 기본으로 포함되어 있으며, 다음과 같은 정의가 들어있습니다:

```php
namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Str;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\User>
 */
class UserFactory extends Factory
{
    /**
     * 팩토리에서 사용 중인 현재 비밀번호.
     */
    protected static ?string $password;

    /**
     * 모델의 기본 상태 정의.
     *
     * @return array<string, mixed>
     */
    public function definition(): array
    {
        return [
            'name' => fake()->name(),
            'email' => fake()->unique()->safeEmail(),
            'email_verified_at' => now(),
            'password' => static::$password ??= Hash::make('password'),
            'remember_token' => Str::random(10),
        ];
    }

    /**
     * 모델의 이메일 주소가 인증되지 않았음을 나타냅니다.
     */
    public function unverified(): static
    {
        return $this->state(fn (array $attributes) => [
            'email_verified_at' => null,
        ]);
    }
}
```

보다시피, 팩토리는 가장 기본적으로 Laravel의 기본 팩토리 클래스를 상속받고, `definition` 메서드를 정의하는 클래스입니다. `definition` 메서드는 팩토리를 통해 모델을 생성할 때 적용해야 하는 속성 값의 기본 집합을 반환합니다.

팩토리는 `fake` 헬퍼를 통해 [Faker](https://github.com/FakerPHP/Faker) PHP 라이브러리에 접근할 수 있으며, 이를 통해 테스트와 시딩을 위한 여러 종류의 랜덤 데이터를 편리하게 생성할 수 있습니다.

> [!NOTE]  
> 애플리케이션의 Faker 로케일(locale)을 변경하려면, `config/app.php` 설정 파일에서 `faker_locale` 옵션을 수정하세요.

<a name="defining-model-factories"></a>
## 모델 팩토리 정의하기

<a name="generating-factories"></a>
### 팩토리 생성하기

팩토리를 생성하려면, `make:factory` [Artisan 명령어](/docs/{{version}}/artisan)를 실행하세요:

```shell
php artisan make:factory PostFactory
```

새로 생성된 팩토리 클래스는 `database/factories` 디렉터리에 위치하게 됩니다.

<a name="factory-and-model-discovery-conventions"></a>
#### 모델과 팩토리 탐색 규칙

팩토리를 정의한 후에는, `Illuminate\Database\Eloquent\Factories\HasFactory` 트레이트에서 제공하는 정적 `factory` 메서드를 사용해 해당 모델의 팩토리 인스턴스를 생성할 수 있습니다.

`HasFactory` 트레이트의 `factory` 메서드는 팩토리를 할당받은 모델에 대해 네이밍 규칙을 사용하여 올바른 팩토리를 찾습니다. 구체적으로, `Database\Factories` 네임스페이스 아래, 모델명과 동일하며 `Factory`로 끝나는 클래스를 찾습니다. 이러한 규칙을 따르지 않는 경우, 모델의 `newFactory` 메서드를 오버라이드하여 해당 모델의 팩토리 인스턴스를 직접 반환할 수 있습니다:

```php
use Database\Factories\Administration\FlightFactory;

/**
 * 모델에 대한 새 팩토리 인스턴스를 생성합니다.
 */
protected static function newFactory()
{
    return FlightFactory::new();
}
```

그런 다음 해당 팩토리 클래스에 `model` 속성을 정의하세요:

```php
use App\Administration\Flight;
use Illuminate\Database\Eloquent\Factories\Factory;

class FlightFactory extends Factory
{
    /**
     * 팩토리가 해당하는 모델의 이름입니다.
     *
     * @var class-string<\Illuminate\Database\Eloquent\Model>
     */
    protected $model = Flight::class;
}
```

<a name="factory-states"></a>
### 팩토리 상태(state)

상태 변화 메서드를 사용하면, 모델 팩토리에 적용 가능한 독립적 수정(상태 변화)을 정의할 수 있습니다. 예를 들어, `Database\Factories\UserFactory` 팩토리에 기본 속성 중 하나를 다르게 설정하는 `suspended` 상태 메서드를 정의할 수 있습니다.

상태 변환 메서드는 일반적으로 Laravel의 기본 팩토리 클래스에서 제공하는 `state` 메서드를 호출합니다. `state`는 팩토리에서 정의된 원시 속성 배열을 인자로 받는 클로저를 인자로 받고, 변경할 속성 배열을 반환해야 합니다:

```php
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * 사용자가 정지됨을 나타냅니다.
 */
public function suspended(): Factory
{
    return $this->state(function (array $attributes) {
        return [
            'account_status' => 'suspended',
        ];
    });
}
```

<a name="trashed-state"></a>
#### "Trashed" 상태

Eloquent 모델이 [소프트 삭제](/docs/{{version}}/eloquent#soft-deleting) 가능하다면, 내장된 `trashed` 상태 메서드를 호출하여 생성된 모델이 이미 "소프트 삭제"된 상태임을 나타낼 수 있습니다. `trashed` 상태는 모든 팩토리에서 자동으로 사용할 수 있으므로 직접 정의할 필요가 없습니다:

```php
use App\Models\User;

$user = User::factory()->trashed()->create();
```

<a name="factory-callbacks"></a>
### 팩토리 콜백(callback)

팩토리 콜백은 `afterMaking`, `afterCreating` 메서드를 사용해 등록하며, 모델을 생성(making)하거나 생성(create)한 이후에 추가 작업을 수행할 수 있게 합니다. 이 콜백들은 팩토리 클래스에 `configure` 메서드를 정의해 등록할 수 있습니다. 이 메서드는 팩토리 인스턴스화 시에 자동으로 호출됩니다:

```php
namespace Database\Factories;

use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;

class UserFactory extends Factory
{
    /**
     * 모델 팩토리 설정.
     */
    public function configure(): static
    {
        return $this->afterMaking(function (User $user) {
            // ...
        })->afterCreating(function (User $user) {
            // ...
        });
    }

    // ...
}
```

또한 상태 메서드 안에서도 팩토리 콜백을 등록하여 특정 상태에만 적용되는 추가 작업을 수행할 수도 있습니다:

```php
use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * 사용자가 정지됨을 나타냅니다.
 */
public function suspended(): Factory
{
    return $this->state(function (array $attributes) {
        return [
            'account_status' => 'suspended',
        ];
    })->afterMaking(function (User $user) {
        // ...
    })->afterCreating(function (User $user) {
        // ...
    });
}
```

<a name="creating-models-using-factories"></a>
## 팩토리를 이용한 모델 생성

<a name="instantiating-models"></a>
### 모델 인스턴스화

팩토리를 정의한 후에는, 모델에서 `Illuminate\Database\Eloquent\Factories\HasFactory` 트레이트가 제공하는 정적 `factory` 메서드를 사용해 팩토리 인스턴스를 만들 수 있습니다. 실제 모델 생성 예시를 살펴보겠습니다. 먼저, `make` 메서드를 사용해서 실제로 데이터베이스에는 저장하지 않은 인스턴스만 생성해봅니다:

```php
use App\Models\User;

$user = User::factory()->make();
```

`count` 메서드를 사용해서 여러 개의 모델 컬렉션도 만들 수 있습니다:

```php
$users = User::factory()->count(3)->make();
```

<a name="applying-states"></a>
#### 상태 적용하기

[상태](#factory-states)도 원하는 대로 적용할 수 있습니다. 여러 상태 변환을 동시에 적용하고 싶다면 상태 변환 메서드를 체인으로 호출하면 됩니다:

```php
$users = User::factory()->count(5)->suspended()->make();
```

<a name="overriding-attributes"></a>
#### 속성 재정의

기본 속성의 일부를 특정 값으로 덮어쓰기 하고 싶다면, `make` 메서드에 값의 배열을 전달할 수 있습니다. 지정된 속성만 교체되고, 나머지는 팩토리에서 정의된 기본 값이 유지됩니다:

```php
$user = User::factory()->make([
    'name' => 'Abigail Otwell',
]);
```

또는 팩토리 인스턴스에서 바로 `state` 메서드를 호출해 인라인으로 상태 변환을 적용할 수도 있습니다:

```php
$user = User::factory()->state([
    'name' => 'Abigail Otwell',
])->make();
```

> [!NOTE]  
> 팩토리를 사용해 모델을 생성할 때는 [대량 할당 보호](/docs/{{version}}/eloquent#mass-assignment)가 자동으로 비활성화됩니다.

<a name="persisting-models"></a>
### 모델 영속화

`create` 메서드는 모델 인스턴스를 생성하고, Eloquent의 `save` 메서드를 사용해 데이터베이스에 저장합니다:

```php
use App\Models\User;

// 단일 App\Models\User 인스턴스 생성...
$user = User::factory()->create();

// 3개의 App\Models\User 인스턴스 생성...
$users = User::factory()->count(3)->create();
```

팩토리의 기본 모델 속성을 재정의하려면, `create` 메서드에 속성 배열을 전달하세요:

```php
$user = User::factory()->create([
    'name' => 'Abigail',
]);
```

<a name="sequences"></a>
### 시퀀스(Sequences)

여러 개의 모델을 만들 때, 특정 속성 값을 번갈아가며 할당하고 싶을 때가 있습니다. 이럴 땐 상태 변환을 시퀀스로 정의할 수 있습니다. 예를 들어, 생성되는 각 사용자마다 `admin` 컬럼의 값을 번갈아가며 `Y`, `N`으로 지정하고 싶다면:

```php
use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Sequence;

$users = User::factory()
    ->count(10)
    ->state(new Sequence(
        ['admin' => 'Y'],
        ['admin' => 'N'],
    ))
    ->create();
```

이 예시에서는 5명의 사용자가 `admin` 값 `Y`로, 5명은 `N`으로 생성됩니다.

필요하다면, 시퀀스 값에서 클로저를 사용할 수도 있습니다. 시퀀스에서 새 값이 필요할 때마다 클로저가 호출됩니다:

```php
use Illuminate\Database\Eloquent\Factories\Sequence;

$users = User::factory()
    ->count(10)
    ->state(new Sequence(
        fn (Sequence $sequence) => ['role' => UserRoles::all()->random()],
    ))
    ->create();
```

시퀀스 클로저 안에서는 클로저에 주입된 시퀀스 인스턴스의 `$index`(현재 반복 횟수) 또는 `$count`(총 호출될 횟수) 속성에 접근할 수 있습니다:

```php
$users = User::factory()
    ->count(10)
    ->sequence(fn (Sequence $sequence) => ['name' => 'Name '.$sequence->index])
    ->create();
```

편의상, 시퀀스는 `sequence` 메서드를 통해서도 적용할 수 있으며, 이는 내부적으로 `state`를 호출합니다. `sequence` 메서드는 시퀀스 속성 배열 또는 클로저를 인자로 받습니다:

```php
$users = User::factory()
    ->count(2)
    ->sequence(
        ['name' => 'First User'],
        ['name' => 'Second User'],
    )
    ->create();
```

<a name="factory-relationships"></a>
## 팩토리 관계 정의

<a name="has-many-relationships"></a>
### Has Many 관계

이제 Laravel 팩토리의 유연한 메서드를 사용해 Eloquent 모델 관계를 구축하는 방법을 살펴보겠습니다. 우선, 애플리케이션에 `App\Models\User` 모델과 `App\Models\Post` 모델이 있다고 가정합니다. 또한, `User` 모델이 `Post`와의 `hasMany` 관계를 가진다고 가정할 때, 팩토리의 `has` 메서드를 이용해 3개의 포스트를 가진 사용자를 생성할 수 있습니다. `has` 메서드는 팩토리 인스턴스를 인자로 받습니다:

```php
use App\Models\Post;
use App\Models\User;

$user = User::factory()
    ->has(Post::factory()->count(3))
    ->create();
```

관례상, `has` 메서드에 `Post` 모델을 전달하면, Laravel은 `User` 모델에 `posts`라는 관계 메서드가 있다고 간주합니다. 필요한 경우 조작하려는 관계의 이름을 명시적으로 지정할 수 있습니다:

```php
$user = User::factory()
    ->has(Post::factory()->count(3), 'posts')
    ->create();
```

물론, 연관 모델에도 상태 변환을 적용할 수 있습니다. 부모 모델 정보가 필요한 상태 변경이 있다면, 클로저 기반의 상태 변환을 전달할 수도 있습니다:

```php
$user = User::factory()
    ->has(
        Post::factory()
            ->count(3)
            ->state(function (array $attributes, User $user) {
                return ['user_type' => $user->type];
            })
        )
    ->create();
```

<a name="has-many-relationships-using-magic-methods"></a>
#### 매직 메서드 사용

편의를 위해, Laravel의 매직 팩토리 관계 메서드를 사용할 수 있습니다. 다음 예시처럼, `User` 모델의 `posts` 관계 메서드와 연동하여 관련 모델들을 생성하게 됩니다:

```php
$user = User::factory()
    ->hasPosts(3)
    ->create();
```

매직 메서드로 팩토리 관계를 생성할 때, 연관 모델에 대해 덮어쓸 속성 배열을 전달할 수 있습니다:

```php
$user = User::factory()
    ->hasPosts(3, [
        'published' => false,
    ])
    ->create();
```

상태 변화가 부모 모델 정보에 의존한다면, 클로저 기반의 상태 변환을 전달할 수도 있습니다:

```php
$user = User::factory()
    ->hasPosts(3, function (array $attributes, User $user) {
        return ['user_type' => $user->type];
    })
    ->create();
```

<a name="belongs-to-relationships"></a>
### Belongs To 관계

"has many" 관계를 팩토리로 구현하는 방법을 살펴봤으니, 이제 반대 방향의 "belongs to" 관계를 살펴보겠습니다. `for` 메서드를 사용하면, 팩토리로 생성되는 모델이 속하게 될 부모 모델을 지정할 수 있습니다. 예를 들어, 3개의 `App\Models\Post` 인스턴스가 한 사용자에 속하게 하려면 다음과 같이 합니다:

```php
use App\Models\Post;
use App\Models\User;

$posts = Post::factory()
    ->count(3)
    ->for(User::factory()->state([
        'name' => 'Jessica Archer',
    ]))
    ->create();
```

이미 생성된 부모 모델 인스턴스가 있다면, 해당 인스턴스를 `for` 메서드에 직접 전달할 수도 있습니다:

```php
$user = User::factory()->create();

$posts = Post::factory()
    ->count(3)
    ->for($user)
    ->create();
```

<a name="belongs-to-relationships-using-magic-methods"></a>
#### 매직 메서드 사용

편의를 위해, "belongs to" 관계에도 매직 팩토리 관계 메서드를 사용할 수 있습니다. 예시처럼, 생성되는 3개의 포스트는 `Post` 모델의 `user` 관계에 속하게 됩니다:

```php
$posts = Post::factory()
    ->count(3)
    ->forUser([
        'name' => 'Jessica Archer',
    ])
    ->create();
```

<a name="many-to-many-relationships"></a>
### Many to Many(다대다) 관계

[has many 관계](#has-many-relationships)와 마찬가지로, "many to many"(다대다) 관계도 `has` 메서드를 이용해 생성할 수 있습니다:

```php
use App\Models\Role;
use App\Models\User;

$user = User::factory()
    ->has(Role::factory()->count(3))
    ->create();
```

<a name="pivot-table-attributes"></a>
#### 피벗(중간) 테이블 속성

관계 모델들을 연결하는 피벗(중간) 테이블에 값을 지정해야 한다면, `hasAttached` 메서드를 사용하면 됩니다. 두 번째 인자로 피벗 테이블의 속성 이름과 값을 배열로 전달합니다:

```php
use App\Models\Role;
use App\Models\User;

$user = User::factory()
    ->hasAttached(
        Role::factory()->count(3),
        ['active' => true]
    )
    ->create();
```

상태 변화가 관계 모델 정보에 의존해야 한다면, 클로저 기반의 상태 변환도 지정할 수 있습니다:

```php
$user = User::factory()
    ->hasAttached(
        Role::factory()
            ->count(3)
            ->state(function (array $attributes, User $user) {
                return ['name' => $user->name.' Role'];
            }),
        ['active' => true]
    )
    ->create();
```

이미 생성된 모델 인스턴스들을 연결하고 싶다면, 모델 인스턴스 컬렉션을 `hasAttached`에 전달할 수도 있습니다. 이 예시에서는, 동일한 3개 역할이 3명 사용자에 모두 연결됩니다:

```php
$roles = Role::factory()->count(3)->create();

$user = User::factory()
    ->count(3)
    ->hasAttached($roles, ['active' => true])
    ->create();
```

<a name="many-to-many-relationships-using-magic-methods"></a>
#### 매직 메서드 사용

편의를 위해, 매직 팩토리 관계 메서드를 사용해 다대다 관계를 정의할 수 있습니다. 다음 예시는, 관련 모델들이 `User` 모델의 `roles` 관계 메서드를 통해 생성됨을 나타냅니다:

```php
$user = User::factory()
    ->hasRoles(1, [
        'name' => 'Editor'
    ])
    ->create();
```

<a name="polymorphic-relationships"></a>
### 폴리모픽(Polymorphic) 관계

[폴리모픽 관계](/docs/{{version}}/eloquent-relationships#polymorphic-relationships)도 팩토리로 생성할 수 있습니다. 폴리모픽 "morph many" 관계는 일반 "has many"와 동일하게 생성됩니다. 예를 들어, `App\Models\Post` 모델이 `App\Models\Comment` 모델과 `morphMany` 관계를 가진 경우:

```php
use App\Models\Post;

$post = Post::factory()->hasComments(3)->create();
```

<a name="morph-to-relationships"></a>
#### Morph To 관계

매직 메서드를 사용해서는 `morphTo` 관계를 생성할 수 없습니다. 대신, 반드시 `for` 메서드를 직접 사용하고, 관계의 이름을 명시해야 합니다. 예를 들어, `Comment` 모델이 `commentable` 메서드로 `morphTo` 관계를 정의하는 경우, 다음과 같이 3개의 댓글을 하나의 게시글에 생성할 수 있습니다:

```php
$comments = Comment::factory()->count(3)->for(
    Post::factory(), 'commentable'
)->create();
```

<a name="polymorphic-many-to-many-relationships"></a>
#### 폴리모픽 다대다(many to many) 관계

폴리모픽 "다대다"(즉, `morphToMany` / `morphedByMany`) 관계도 일반 "다대다"와 동일하게 팩토리로 생성할 수 있습니다:

```php
use App\Models\Tag;
use App\Models\Video;

$videos = Video::factory()
    ->hasAttached(
        Tag::factory()->count(3),
        ['public' => true]
    )
    ->create();
```

물론, 매직 `has` 메서드로도 폴리모픽 "다대다" 관계를 만들 수 있습니다:

```php
$videos = Video::factory()
    ->hasTags(3, ['public' => true])
    ->create();
```

<a name="defining-relationships-within-factories"></a>
### 팩토리 내 관계 정의

팩토리 내에서 관계를 정의할 때는, 보통 관계의 외래 키에 새 팩토리 인스턴스를 할당합니다. 이는 `belongsTo` 및 `morphTo`와 같은 "역방향" 관계에 주로 사용됩니다. 예를 들어, 포스트를 생성할 때 사용자도 함께 새로 생성하고 싶다면 다음과 같이 정의할 수 있습니다:

```php
use App\Models\User;

/**
 * 모델의 기본 상태 정의.
 *
 * @return array<string, mixed>
 */
public function definition(): array
{
    return [
        'user_id' => User::factory(),
        'title' => fake()->title(),
        'content' => fake()->paragraph(),
    ];
}
```

관계 컬럼이 팩토리에서 정의한 다른 속성값에 의존해야 한다면, 속성에 클로저를 할당할 수 있습니다. 클로저는 팩토리에서 평가된 속성 배열을 전달받습니다:

```php
/**
 * 모델의 기본 상태 정의.
 *
 * @return array<string, mixed>
 */
public function definition(): array
{
    return [
        'user_id' => User::factory(),
        'user_type' => function (array $attributes) {
            return User::find($attributes['user_id'])->type;
        },
        'title' => fake()->title(),
        'content' => fake()->paragraph(),
    ];
}
```

<a name="recycling-an-existing-model-for-relationships"></a>
### 관계를 위한 기존 모델 재활용

여러 모델이 같은 관계 모델을 공유해야 할 경우, `recycle` 메서드를 사용하여 팩토리에서 생성하는 모든 관계에 대해 동일한 인스턴스를 재사용할 수 있습니다.

예를 들어, `Airline`, `Flight`, `Ticket` 모델이 있고, `Ticket`은 `Airline`과 `Flight`에 속하며, `Flight`도 `Airline`에 속한다고 할 때, 티켓과 플라이트 모두 같은 항공사와 연결하도록 다음과 같이 할 수 있습니다:

```php
Ticket::factory()
    ->recycle(Airline::factory()->create())
    ->create();
```

이 메서드는 특히 모델이 공통 사용자 또는 팀에 소속되어 있어야 할 때 유용합니다.

`recycle` 메서드는 기존 모델의 컬렉션도 받을 수 있습니다. 컬렉션을 `recycle`에 전달하면, 해당 타입 모델이 필요할 때마다 컬렉션에서 무작위로 하나가 선택됩니다:

```php
Ticket::factory()
    ->recycle($airlines)
    ->create();
```
