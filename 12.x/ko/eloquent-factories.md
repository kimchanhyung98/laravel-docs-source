# Eloquent: 팩토리 (Eloquent: Factories)

- [소개](#introduction)
- [모델 팩토리 정의](#defining-model-factories)
    - [팩토리 생성](#generating-factories)
    - [팩토리 상태](#factory-states)
    - [팩토리 콜백](#factory-callbacks)
- [팩토리를 사용한 모델 생성](#creating-models-using-factories)
    - [모델 인스턴스화](#instantiating-models)
    - [모델 영속화](#persisting-models)
    - [시퀀스 활용](#sequences)
- [팩토리로 연관관계 다루기](#factory-relationships)
    - [Has Many 연관관계](#has-many-relationships)
    - [Belongs To 연관관계](#belongs-to-relationships)
    - [Many to Many 연관관계](#many-to-many-relationships)
    - [다형성 연관관계](#polymorphic-relationships)
    - [팩토리 내부에서 연관관계 정의](#defining-relationships-within-factories)
    - [기존 모델을 재활용한 연관관계 생성](#recycling-an-existing-model-for-relationships)

<a name="introduction"></a>
## 소개 (Introduction)

애플리케이션을 테스트하거나 데이터베이스를 시딩할 때, 데이터베이스에 여러 레코드를 삽입해야 할 수 있습니다. 각 컬럼의 값을 일일이 지정하는 대신, Laravel에서는 각 [Eloquent 모델](/docs/12.x/eloquent)에 대해 기본 속성값 집합을 모델 팩토리로 정의할 수 있습니다.

팩토리 작성 예시는 애플리케이션의 `database/factories/UserFactory.php` 파일에서 확인할 수 있습니다. 이 파일은 모든 새로운 Laravel 애플리케이션에 포함되어 있으며, 다음과 같은 팩토리 정의를 가지고 있습니다:

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
     * The current password being used by the factory.
     */
    protected static ?string $password;

    /**
     * Define the model's default state.
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
     * Indicate that the model's email address should be unverified.
     */
    public function unverified(): static
    {
        return $this->state(fn (array $attributes) => [
            'email_verified_at' => null,
        ]);
    }
}
```

위에서 볼 수 있듯, 가장 기본적인 형태의 팩토리는 Laravel의 기본 팩토리 클래스를 상속받으며, `definition` 메서드를 정의합니다. 이 `definition` 메서드는 팩토리를 통해 모델을 생성할 때 적용할 기본 속성값 집합을 반환합니다.

팩토리는 `fake` 헬퍼를 통해 [Faker](https://github.com/FakerPHP/Faker) PHP 라이브러리를 사용할 수 있어, 테스트와 시딩을 위해 다양한 종류의 랜덤 데이터를 편리하게 생성할 수 있습니다.

> [!NOTE]
> 애플리케이션의 Faker 로케일(locale)은 `config/app.php` 설정 파일의 `faker_locale` 옵션을 수정하여 변경할 수 있습니다.

<a name="defining-model-factories"></a>
## 모델 팩토리 정의 (Defining Model Factories)

<a name="generating-factories"></a>
### 팩토리 생성 (Generating Factories)

팩토리를 생성하려면 `make:factory` [Artisan 명령어](/docs/12.x/artisan)를 실행하세요:

```shell
php artisan make:factory PostFactory
```

새로 생성된 팩토리 클래스는 `database/factories` 디렉토리에 위치합니다.

<a name="factory-and-model-discovery-conventions"></a>
#### 모델과 팩토리의 규칙 (Model and Factory Discovery Conventions)

팩토리를 정의한 후에는, `Illuminate\Database\Eloquent\Factories\HasFactory` 트레이트에서 제공하는 정적 `factory` 메서드를 사용하여 해당 모델의 팩토리 인스턴스를 만들 수 있습니다.

`HasFactory` 트레이트의 `factory` 메서드는 관례(convention)를 활용해 해당 모델에 적합한 팩토리를 찾습니다. 구체적으로, 이 메서드는 `Database\Factories` 네임스페이스에서 모델명과 일치하고, `Factory`가 접미사로 붙은 팩토리 클래스를 찾습니다. 이 규칙이 해당 애플리케이션이나 팩토리에 맞지 않을 경우, 모델 클래스에서 `newFactory` 메서드를 오버라이드하여 직접 팩토리 인스턴스를 반환할 수 있습니다:

```php
use Database\Factories\Administration\FlightFactory;

/**
 * Create a new factory instance for the model.
 */
protected static function newFactory()
{
    return FlightFactory::new();
}
```

그리고 해당 팩토리에는 `model` 속성을 명시해야 합니다:

```php
use App\Administration\Flight;
use Illuminate\Database\Eloquent\Factories\Factory;

class FlightFactory extends Factory
{
    /**
     * The name of the factory's corresponding model.
     *
     * @var class-string<\Illuminate\Database\Eloquent\Model>
     */
    protected $model = Flight::class;
}
```

<a name="factory-states"></a>
### 팩토리 상태 (Factory States)

상태(state) 조작 메서드는 모델 팩토리에 적용할 개별적 변경 사항을 정의할 수 있게 해줍니다. 예를 들어, `Database\Factories\UserFactory` 팩토리에 `suspended`라는 상태 메서드를 추가해, 기본 속성값 중 하나를 변경할 수 있습니다.

상태 변화(state transformation) 메서드는 보통 Laravel의 기본 팩토리 클래스가 제공하는 `state` 메서드를 호출합니다. `state` 메서드는 익명 함수를 받으며, 이 함수는 팩토리의 원시 속성 배열을 받아 수정할 속성 배열을 반환해야 합니다:

```php
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * Indicate that the user is suspended.
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

만약 Eloquent 모델이 [소프트 삭제](/docs/12.x/eloquent#soft-deleting)를 지원한다면, 내장된 `trashed` 상태 메서드를 사용하여 생성된 모델이 이미 "소프트 삭제" 된 상태임을 지정할 수 있습니다. 이 `trashed` 상태는 모든 팩토리에서 자동으로 제공되므로 직접 정의할 필요가 없습니다:

```php
use App\Models\User;

$user = User::factory()->trashed()->create();
```

<a name="factory-callbacks"></a>
### 팩토리 콜백 (Factory Callbacks)

팩토리 콜백은 `afterMaking` 및 `afterCreating` 메서드를 사용해 등록하며, 모델 생성 후 추가 작업을 수행할 수 있게 해줍니다. 이 콜백들은 팩토리 클래스에 `configure` 메서드를 정의하여 등록할 수 있습니다. 해당 메서드는 팩토리 인스턴스화 시 Laravel이 자동으로 호출합니다:

```php
namespace Database\Factories;

use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;

class UserFactory extends Factory
{
    /**
     * Configure the model factory.
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

특정 상태에만 적용되는 추가 작업이 필요한 경우, 상태 메서드 내에서도 팩토리 콜백을 등록할 수 있습니다:

```php
use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * Indicate that the user is suspended.
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
## 팩토리를 사용한 모델 생성 (Creating Models Using Factories)

<a name="instantiating-models"></a>
### 모델 인스턴스화 (Instantiating Models)

팩토리를 정의한 후에는, `Illuminate\Database\Eloquent\Factories\HasFactory` 트레이트에서 제공하는 정적 `factory` 메서드를 사용하여 해당 모델의 팩토리 인스턴스를 만들 수 있습니다. 모델 생성을 예시로 살펴보겠습니다. 먼저, `make` 메서드를 사용해 데이터베이스에 저장하지 않고 모델 인스턴스를 생성할 수 있습니다:

```php
use App\Models\User;

$user = User::factory()->make();
```

`count` 메서드를 사용하면 여러 모델 컬렉션을 한 번에 생성할 수 있습니다:

```php
$users = User::factory()->count(3)->make();
```

<a name="applying-states"></a>
#### 상태 적용하기

[팩토리 상태](#factory-states)를 모델에 적용할 수도 있습니다. 여러 상태 변화 메서드를 연결 호출하여 복수의 상태를 조합해 적용할 수 있습니다:

```php
$users = User::factory()->count(5)->suspended()->make();
```

<a name="overriding-attributes"></a>
#### 속성값 오버라이드

모델의 기본값 일부를 변경하고 싶다면, 원하는 값의 배열을 `make` 메서드에 전달하면 됩니다. 지정한 속성만 변경되고, 나머지는 팩토리에서 정의한 기본값이 유지됩니다:

```php
$user = User::factory()->make([
    'name' => 'Abigail Otwell',
]);
```

또는, `state` 메서드를 팩토리 인스턴스에 직접 호출하여 인라인 상태 변환을 적용할 수도 있습니다:

```php
$user = User::factory()->state([
    'name' => 'Abigail Otwell',
])->make();
```

> [!NOTE]
> 팩토리를 사용한 모델 생성 시 [일괄 할당 보호](/docs/12.x/eloquent#mass-assignment)는 자동으로 비활성화됩니다.

<a name="persisting-models"></a>
### 모델 영속화 (Persisting Models)

`create` 메서드는 모델 인스턴스를 생성하고, Eloquent의 `save` 메서드를 사용해 데이터베이스에 저장합니다:

```php
use App\Models\User;

// App\Models\User 인스턴스 하나 생성...
$user = User::factory()->create();

// App\Models\User 인스턴스 세 개 생성...
$users = User::factory()->count(3)->create();
```

`create` 메서드에도 속성 배열을 전달하여 기본값을 오버라이드할 수 있습니다:

```php
$user = User::factory()->create([
    'name' => 'Abigail',
]);
```

<a name="sequences"></a>
### 시퀀스 활용 (Sequences)

여러 모델을 생성할 때, 특정 속성값을 번갈아가며 할당하고 싶을 수 있습니다. 이때 상태 변환을 "시퀀스"로 정의하여 반복적으로 속성값을 순환시킬 수 있습니다. 예를 들어, `admin` 컬럼 값을 `Y`와 `N`으로 번갈아 지정하려면 다음과 같이 작성합니다:

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

이 예시에서는 `admin` 값이 `Y`인 사용자 5명, `N`인 사용자 5명이 생성됩니다.

필요하다면, 클로저를 시퀀스값으로 사용할 수도 있습니다. 이 클로저는 시퀀스에서 새 값을 필요로 할 때마다 호출됩니다:

```php
use Illuminate\Database\Eloquent\Factories\Sequence;

$users = User::factory()
    ->count(10)
    ->state(new Sequence(
        fn (Sequence $sequence) => ['role' => UserRoles::all()->random()],
    ))
    ->create();
```

시퀀스 클로저 내부에서는 전달받은 시퀀스 인스턴스의 `$index` 속성으로 현재 시퀀스 반복 횟수에 접근할 수 있습니다:

```php
$users = User::factory()
    ->count(10)
    ->state(new Sequence(
        fn (Sequence $sequence) => ['name' => 'Name '.$sequence->index],
    ))
    ->create();
```

편의상, 시퀀스는 `sequence` 메서드로도 적용할 수 있습니다. 이 메서드는 내부적으로 `state`를 호출하며, 클로저나 속성 배열들을 받을 수 있습니다:

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
## 팩토리로 연관관계 다루기 (Factory Relationships)

<a name="has-many-relationships"></a>
### Has Many 연관관계 (Has Many Relationships)

이제, Laravel의 유연한 팩토리 메서드를 사용해 Eloquent 모델 간 연관관계를 구축하는 방법을 살펴보겠습니다. 예를 들어 `App\Models\User`와 `App\Models\Post` 모델이 있고, `User` 모델이 `Post`와 `hasMany` 연관관계를 정의하고 있다고 가정해봅시다. 이런 경우, 팩토리의 `has` 메서드를 사용해 3개의 게시글을 가진 유저를 생성할 수 있습니다. `has` 메서드는 팩토리 인스턴스를 인자로 받습니다:

```php
use App\Models\Post;
use App\Models\User;

$user = User::factory()
    ->has(Post::factory()->count(3))
    ->create();
```

관례상, `has` 메서드에 `Post` 모델을 전달하면, Laravel은 `User` 모델에 `posts`라는 관계 메서드가 있다고 간주합니다. 필요하다면, 조작하고자 하는 관계명도 명시적으로 지정할 수 있습니다:

```php
$user = User::factory()
    ->has(Post::factory()->count(3), 'posts')
    ->create();
```

물론, 연관된 모델에도 상태 변환을 적용할 수 있습니다. 부모 모델에 접근해야 하는 경우, 클로저 기반의 상태 변환도 전달할 수 있습니다:

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
#### 매직 메서드 활용하기 (Using Magic Methods)

편의상, Laravel의 매직 팩토리 관계 메서드를 사용해 관계를 구축할 수도 있습니다. 아래 코드는 관례에 따라, 관련 모델들이 `User` 모델의 `posts` 관계 메서드를 통해 생성되어야 함을 유추합니다:

```php
$user = User::factory()
    ->hasPosts(3)
    ->create();
```

매직 메서드를 사용할 때, 연관 모델에서 오버라이드할 속성을 배열로 전달할 수 있습니다:

```php
$user = User::factory()
    ->hasPosts(3, [
        'published' => false,
    ])
    ->create();
```

상태 변화에 부모 모델 접근이 필요하다면, 클로저 기반의 상태 변환을 전달할 수 있습니다:

```php
$user = User::factory()
    ->hasPosts(3, function (array $attributes, User $user) {
        return ['user_type' => $user->type];
    })
    ->create();
```

<a name="belongs-to-relationships"></a>
### Belongs To 연관관계 (Belongs To Relationships)

앞서 "has many" 관계를 살펴봤으니, 이제 그 반대인 "belongs to" 관계를 팩토리에서 생성하는 방법을 배워봅시다. `for` 메서드는 팩토리로 생성되는 모델이 소속될 부모 모델을 정의할 수 있습니다. 예를 들어, 세 개의 `App\Models\Post` 인스턴스를 하나의 유저에 속하도록 생성할 수 있습니다:

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

이미 생성된 부모 모델 인스턴스가 존재한다면, 해당 인스턴스를 `for` 메서드에 바로 전달할 수 있습니다:

```php
$user = User::factory()->create();

$posts = Post::factory()
    ->count(3)
    ->for($user)
    ->create();
```

<a name="belongs-to-relationships-using-magic-methods"></a>
#### 매직 메서드 활용하기 (Using Magic Methods)

편리하게, Laravel의 매직 팩토리 관계 메서드를 활용해 "belongs to" 연관관계를 정의할 수도 있습니다. 아래 예시는 관례에 따라, 세 게시글이 모두 `Post` 모델의 `user` 관계에 속해야 함을 유추합니다:

```php
$posts = Post::factory()
    ->count(3)
    ->forUser([
        'name' => 'Jessica Archer',
    ])
    ->create();
```

<a name="many-to-many-relationships"></a>
### Many to Many 연관관계 (Many to Many Relationships)

[Has Many 연관관계](#has-many-relationships)처럼, "many to many" 관계도 `has` 메서드로 생성할 수 있습니다:

```php
use App\Models\Role;
use App\Models\User;

$user = User::factory()
    ->has(Role::factory()->count(3))
    ->create();
```

<a name="pivot-table-attributes"></a>
#### Pivot 테이블 속성 (Pivot Table Attributes)

모델을 연결하는 중간(pivot) 테이블에 값을 지정해야 한다면, `hasAttached` 메서드를 사용할 수 있습니다. 이 메서드의 두 번째 인자로 pivot 테이블 속성 배열을 전달합니다:

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

상태 변화에 연관된 모델 접근이 필요한 경우, 클로저 기반의 상태 변환도 사용할 수 있습니다:

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

이미 생성된 모델 인스턴스를 연결하고 싶다면, 해당 인스턴스들을 `hasAttached` 메서드에 전달할 수 있습니다. 아래 예시에서는 세 개의 역할(role)이 모든 사용자(user)에 동일하게 연결됩니다:

```php
$roles = Role::factory()->count(3)->create();

$user = User::factory()
    ->count(3)
    ->hasAttached($roles, ['active' => true])
    ->create();
```

<a name="many-to-many-relationships-using-magic-methods"></a>
#### 매직 메서드 활용하기 (Using Magic Methods)

편의상, Laravel의 매직 팩토리 관계 메서드를 사용해 many to many 관계도 생성할 수 있습니다. 아래 예시는 관례에 따라, 관련 모델들이 `User` 모델의 `roles` 관계 메서드를 통해 생성되어야 함을 유추합니다:

```php
$user = User::factory()
    ->hasRoles(1, [
        'name' => 'Editor'
    ])
    ->create();
```

<a name="polymorphic-relationships"></a>
### 다형성 연관관계 (Polymorphic Relationships)

[다형성 연관관계](/docs/12.x/eloquent-relationships#polymorphic-relationships) 또한 팩토리를 통해 생성할 수 있습니다. 다형성 "morph many" 관계는 일반적인 "has many" 관계처럼 생성합니다. 예를 들어, `App\Models\Post` 모델이 `App\Models\Comment` 모델과 `morphMany` 관계를 가진다면:

```php
use App\Models\Post;

$post = Post::factory()->hasComments(3)->create();
```

<a name="morph-to-relationships"></a>
#### Morph To 연관관계

매직 메서드로는 `morphTo` 연관관계를 생성할 수 없습니다. 이 경우, `for` 메서드를 직접 사용하며 관계명도 명확히 지정해야 합니다. 예시로, `Comment` 모델에 `commentable` 이라는 `morphTo` 관계가 있을 때, 하나의 게시글에 속하는 세 개의 댓글을 만들려면 다음과 같이 작성합니다:

```php
$comments = Comment::factory()->count(3)->for(
    Post::factory(), 'commentable'
)->create();
```

<a name="polymorphic-many-to-many-relationships"></a>
#### 다형성 Many to Many 연관관계

다형성 "many to many" (`morphToMany` / `morphedByMany`) 관계는 일반 many to many 관계처럼 생성합니다:

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

물론, 매직 `has` 메서드를 사용해 다형성 many to many 관계도 생성할 수 있습니다:

```php
$videos = Video::factory()
    ->hasTags(3, ['public' => true])
    ->create();
```

<a name="defining-relationships-within-factories"></a>
### 팩토리 내부에서 연관관계 정의 (Defining Relationships Within Factories)

모델 팩토리 내부에서 연관관계를 정의하려면, 보통 외래키에 새로운 팩토리 인스턴스를 할당합니다. 이는 주로 `belongsTo`, `morphTo` 같은 "역방향(inverse)" 연관관계에 사용합니다. 예를 들어, 게시글을 만들 때마다 새로운 유저도 같이 생성하려면 다음과 같이 작성합니다:

```php
use App\Models\User;

/**
 * Define the model's default state.
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

연관관계 컬럼이 팩토리에서 평가된 속성값에 따라 달라질 경우, 속성에 클로저를 할당할 수도 있습니다. 이 클로저는 팩토리의 평가된 속성 배열을 인자로 받습니다:

```php
/**
 * Define the model's default state.
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
### 기존 모델을 재활용한 연관관계 생성 (Recycling an Existing Model for Relationships)

여러 모델이 공통된 다른 모델과 관계를 공유할 때, 팩토리에서 연관관계 생성 시 단일 인스턴스가 재활용되도록 `recycle` 메서드를 사용할 수 있습니다.

예를 들어, `Airline`, `Flight`, `Ticket` 모델이 있고, 티켓(tickets)은 항공사와 항공편에 속하며, 항공편도 항공사에 속한다고 해봅시다. 티켓을 생성할 때 티켓과 항공편 모두 동일한 항공사 인스턴스를 참조하도록 하고 싶다면 `recycle` 메서드에 항공사 인스턴스를 전달하면 됩니다:

```php
Ticket::factory()
    ->recycle(Airline::factory()->create())
    ->create();
```

`recycle` 메서드는 하나의 사용자를 여러 모델이 공유해야 하는 경우에 특히 유용합니다.

또한, `recycle` 메서드는 모델의 컬렉션도 받을 수 있습니다. 컬렉션이 제공될 경우, 팩토리가 해당 타입의 모델을 생성할 때마다 무작위로 하나의 모델을 선택합니다:

```php
Ticket::factory()
    ->recycle($airlines)
    ->create();
```
