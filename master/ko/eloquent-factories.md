# Eloquent: 팩토리 (Eloquent: Factories)

- [소개](#introduction)
- [모델 팩토리 정의하기](#defining-model-factories)
    - [팩토리 생성](#generating-factories)
    - [팩토리 상태 정의](#factory-states)
    - [팩토리 콜백](#factory-callbacks)
- [팩토리를 이용한 모델 생성](#creating-models-using-factories)
    - [모델 인스턴스화](#instantiating-models)
    - [모델 영속화](#persisting-models)
    - [시퀀스(Sequences)](#sequences)
- [팩토리 관계 정의](#factory-relationships)
    - [Has Many(1:N) 관계](#has-many-relationships)
    - [Belongs To(N:1) 관계](#belongs-to-relationships)
    - [Many to Many(N:N) 관계](#many-to-many-relationships)
    - [폴리모픽 관계](#polymorphic-relationships)
    - [팩토리 내부에서의 관계 정의](#defining-relationships-within-factories)
    - [관계에서 기존 모델 재활용하기](#recycling-an-existing-model-for-relationships)

<a name="introduction"></a>
## 소개 (Introduction)

애플리케이션을 테스트하거나 데이터베이스를 시드(seed)할 때 데이터베이스에 몇몇 레코드를 삽입해야 할 수 있습니다. 컬럼 값 하나하나를 직접 지정하는 대신, Laravel에서는 각 [Eloquent 모델](/docs/master/eloquent)에 대해 모델 팩토리를 이용하여 기본 속성 값 세트를 정의할 수 있습니다.

팩토리를 작성하는 구체적인 예는 애플리케이션의 `database/factories/UserFactory.php` 파일을 참고하시기 바랍니다. 이 팩토리는 모든 새로운 Laravel 애플리케이션에 기본으로 포함되어 있으며, 다음과 같은 코드가 정의되어 있습니다.

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

이처럼 팩토리는 Laravel의 기본 팩토리 클래스를 상속하고, `definition` 메서드를 정의하는 클래스로 만들어집니다. `definition` 메서드는 팩토리를 통해 모델을 생성할 때 적용할 기본 속성값의 배열을 반환합니다.

팩토리 내부에서 `fake` 헬퍼를 통해 [Faker](https://github.com/FakerPHP/Faker) PHP 라이브러리를 사용할 수 있습니다. 이를 활용하면 테스트 및 시드 데이터 생성을 위한 다양한 종류의 임의 데이터를 쉽게 생성할 수 있습니다.

> [!NOTE]
> 애플리케이션의 Faker 로케일은 `config/app.php` 설정 파일에서 `faker_locale` 옵션을 변경하여 조정할 수 있습니다.

<a name="defining-model-factories"></a>
## 모델 팩토리 정의하기 (Defining Model Factories)

<a name="generating-factories"></a>
### 팩토리 생성 (Generating Factories)

팩토리를 생성하려면 `make:factory` [Artisan 명령어](/docs/master/artisan)를 실행합니다.

```shell
php artisan make:factory PostFactory
```

새로 생성된 팩토리 클래스는 `database/factories` 디렉터리에 위치하게 됩니다.

<a name="factory-and-model-discovery-conventions"></a>
#### 모델과 팩토리 탐색 규칙

팩토리를 정의한 후, 모델에 `Illuminate\Database\Eloquent\Factories\HasFactory` 트레이트가 제공하는 정적 `factory` 메서드를 사용하여 해당 모델의 팩토리 인스턴스를 생성할 수 있습니다.

`HasFactory` 트레이트의 `factory` 메서드는 네임스페이스가 `Database\Factories`이고, 모델 이름에 `Factory`가 접미사로 붙은 클래스를 찾는 규칙을 따릅니다. 이러한 규칙이 특정 애플리케이션 또는 팩토리에 적용되지 않는 경우, 모델에 `UseFactory` 속성(attribute)을 추가하여 팩토리를 직접 지정할 수 있습니다.

```php
use Illuminate\Database\Eloquent\Attributes\UseFactory;
use Database\Factories\Administration\FlightFactory;

#[UseFactory(FlightFactory::class)]
class Flight extends Model
{
    // ...
}
```

또는 모델에서 `newFactory` 메서드를 오버라이드하여 해당 팩토리의 인스턴스를 직접 반환할 수도 있습니다.

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

그리고 해당 팩토리에는 아래와 같이 `model` 속성을 정의해야 합니다.

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
### 팩토리 상태 정의 (Factory States)

상태(State) 메서드를 사용하면 모델 팩토리에 독립적인 변형을 간단하게 정의하여, 필요에 따라 여러 조합으로 적용할 수 있습니다. 예를 들어 `Database\Factories\UserFactory` 팩토리에, 기본 속성 값을 변경하는 `suspended` 상태 메서드를 추가할 수 있습니다.

상태 변형 메서드는 보통 Laravel의 기본 팩토리 클래스에서 제공하는 `state` 메서드를 이용하여 정의합니다. `state` 메서드는 팩토리에 정의된 원시 속성 배열을 전달받고, 변경할 속성의 배열을 반환하는 클로저를 인수로 받습니다.

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

Eloquent 모델에서 [소프트 삭제](/docs/master/eloquent#soft-deleting)를 사용할 경우, 생성된 모델이 이미 소프트 삭제된 상태가 되도록 내장된 `trashed` 상태 메서드를 이용할 수 있습니다. `trashed` 상태는 모든 팩토리에서 자동으로 지원되며, 별도의 정의 없이 바로 사용할 수 있습니다.

```php
use App\Models\User;

$user = User::factory()->trashed()->create();
```

<a name="factory-callbacks"></a>
### 팩토리 콜백 (Factory Callbacks)

팩토리 콜백은 `afterMaking` 및 `afterCreating` 메서드를 통해 등록할 수 있으며, 모델을 생성(make)하거나 생성 및 저장(create)한 후에 추가 작업을 수행할 때 사용됩니다. 이 콜백들은 팩토리 클래스 내에 `configure` 메서드를 정의하여 등록하며, 이 메서드는 팩토리가 인스턴스화될 때 Laravel이 자동으로 호출합니다.

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

특정 상태에만 적용되는 추가 작업이 필요한 경우, 상태 메서드 안에서 팩토리 콜백을 등록할 수도 있습니다.

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
## 팩토리를 이용한 모델 생성 (Creating Models Using Factories)

<a name="instantiating-models"></a>
### 모델 인스턴스화 (Instantiating Models)

팩토리를 정의한 후에는 `Illuminate\Database\Eloquent\Factories\HasFactory` 트레이트가 제공하는 정적 `factory` 메서드를 통해 해당 모델의 팩토리 인스턴스를 생성할 수 있습니다. 먼저 데이터베이스에 저장하지 않고 단순히 모델 인스턴스를 생성할 때는 `make` 메서드를 사용합니다.

```php
use App\Models\User;

$user = User::factory()->make();
```

`count` 메서드를 사용하면 여러 개의 모델 컬렉션을 생성할 수 있습니다.

```php
$users = User::factory()->count(3)->make();
```

<a name="applying-states"></a>
#### 상태 적용하기

정의해둔 [상태](#factory-states)를 모델에 적용할 수도 있습니다. 여러 상태 변형을 동시에 적용하려면 상태 변형 메서드들을 체이닝해서 호출하면 됩니다.

```php
$users = User::factory()->count(5)->suspended()->make();
```

<a name="overriding-attributes"></a>
#### 속성값 오버라이드

모델의 일부 기본 값만 변경하고 싶을 경우, `make` 메서드에 변경할 속성의 배열을 전달하면 됩니다. 지정된 속성만 변경되고, 나머지는 팩토리에서 정의된 기본값이 적용됩니다.

```php
$user = User::factory()->make([
    'name' => 'Abigail Otwell',
]);
```

또는 `state` 메서드를 팩토리 인스턴스에 직접 호출하여 즉석에서 상태 변형을 적용할 수도 있습니다.

```php
$user = User::factory()->state([
    'name' => 'Abigail Otwell',
])->make();
```

> [!NOTE]
> 팩토리로 모델을 생성할 때는 [일괄 할당 보호(mass assignment protection)](/docs/master/eloquent#mass-assignment)가 자동으로 비활성화됩니다.

<a name="persisting-models"></a>
### 모델 영속화 (Persisting Models)

`create` 메서드는 모델 인스턴스를 생성하고, Eloquent의 `save` 메서드를 이용해 데이터베이스에 영속화합니다.

```php
use App\Models\User;

// App\Models\User 인스턴스 한 개 생성...
$user = User::factory()->create();

// App\Models\User 인스턴스 세 개 생성...
$users = User::factory()->count(3)->create();
```

`create` 메서드에도 속성 배열을 전달하여, 팩토리의 기본 속성값을 오버라이드할 수 있습니다.

```php
$user = User::factory()->create([
    'name' => 'Abigail',
]);
```

<a name="sequences"></a>
### 시퀀스(Sequences)

생성할 각 모델에 대해 특정 속성 값을 번갈아 설정하고 싶을 때는 상태 변형을 시퀀스로 정의할 수 있습니다. 예를 들어, 각 사용자의 `admin` 컬럼 값을 번갈아가며 `Y`와 `N`으로 설정하려면 다음과 같이 작성합니다.

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

이 예시에서는, 10명의 사용자가 각각 5명씩 `admin` 값이 `Y`와 `N`으로 번갈아가며 생성됩니다.

필요하다면 시퀀스 값으로 클로저를 지정할 수도 있습니다. 이 클로저는 매번 새로운 시퀀스 값이 필요할 때마다 실행됩니다.

```php
use Illuminate\Database\Eloquent\Factories\Sequence;

$users = User::factory()
    ->count(10)
    ->state(new Sequence(
        fn (Sequence $sequence) => ['role' => UserRoles::all()->random()],
    ))
    ->create();
```

시퀀스 내부의 클로저에서는 클로저로 전달된 시퀀스 인스턴스의 `$index` 속성을 통해 현재까지의 반복 횟수를 알 수 있습니다.

```php
$users = User::factory()
    ->count(10)
    ->state(new Sequence(
        fn (Sequence $sequence) => ['name' => 'Name '.$sequence->index],
    ))
    ->create();
```

또한, `sequence` 메서드를 사용하면 더 간단하게 시퀀스를 적용할 수 있습니다. 이 메서드는 내부적으로 `state` 메서드를 호출하며, 클로저 또는 속성 배열들을 인수로 받을 수 있습니다.

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
## 팩토리 관계 정의 (Factory Relationships)

<a name="has-many-relationships"></a>
### Has Many(1:N) 관계

이제 Laravel의 유연한 팩토리 메서드를 이용해 Eloquent 모델 간 연관관계를 구성하는 방법을 알아봅시다. 예를 들어, `App\Models\User` 모델과 `App\Models\Post` 모델이 있다고 가정합니다. 그리고 `User` 모델은 `Post`와 `hasMany` 관계를 정의한다고 할 때, 다음과 같이 `has` 메서드를 사용해서 3개의 게시물을 가진 사용자를 생성할 수 있습니다. `has` 메서드는 팩토리 인스턴스를 인수로 받습니다.

```php
use App\Models\Post;
use App\Models\User;

$user = User::factory()
    ->has(Post::factory()->count(3))
    ->create();
```

관례상, `has` 메서드에 `Post` 모델을 전달하면, Laravel은 `User` 모델에 반드시 `posts` 연관관계 메서드가 정의되어 있을 것으로 간주합니다. 필요하다면 조작할 연관관계의 이름을 명시적으로 지정할 수 있습니다.

```php
$user = User::factory()
    ->has(Post::factory()->count(3), 'posts')
    ->create();
```

물론, 연관된 모델에 상태 변형도 적용할 수 있습니다. 또한 상태 변형이 부모 모델에 접근해야 한다면 클로저 기반으로 상태 변형을 전달할 수 있습니다.

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
#### 매직 메서드 활용

좀 더 간편하게, Laravel의 매직 팩토리 관계 메서드를 사용할 수 있습니다. 아래 예시처럼 `posts` 연관관계를 자동으로 찾아 3개의 게시물을 생성합니다.

```php
$user = User::factory()
    ->hasPosts(3)
    ->create();
```

매직 메서드를 사용할 때도 연관 모델의 속성을 오버라이드하는 배열을 전달할 수 있습니다.

```php
$user = User::factory()
    ->hasPosts(3, [
        'published' => false,
    ])
    ->create();
```

상태 변형이 부모 모델에 접근해야 한다면 마찬가지로 클로저로 전달할 수 있습니다.

```php
$user = User::factory()
    ->hasPosts(3, function (array $attributes, User $user) {
        return ['user_type' => $user->type];
    })
    ->create();
```

<a name="belongs-to-relationships"></a>
### Belongs To(N:1) 관계

"has many" 관계를 살펴보았으니, 이제 그 반대인 "belongs to" 관계를 알아보겠습니다. 팩토리에서 생성되는 모델들이 어떤 부모 모델에 속하도록 하고 싶을 때는 `for` 메서드를 사용합니다. 예를 들어, 3개의 `App\Models\Post` 모델 인스턴스가 같은 사용자에게 속하도록 만들고 싶을 때는 다음과 같이 사용합니다.

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

이미 생성된 부모 모델 인스턴스가 있다면, 그 인스턴스를 `for` 메서드에 직접 전달할 수도 있습니다.

```php
$user = User::factory()->create();

$posts = Post::factory()
    ->count(3)
    ->for($user)
    ->create();
```

<a name="belongs-to-relationships-using-magic-methods"></a>
#### 매직 메서드 활용

매직 팩토리 메서드를 사용하면 "belongs to" 관계도 편리하게 정의할 수 있습니다. 아래 예시는 세 개의 게시물이 모두 `Post` 모델의 `user` 연관관계에 속하도록 합니다.

```php
$posts = Post::factory()
    ->count(3)
    ->forUser([
        'name' => 'Jessica Archer',
    ])
    ->create();
```

<a name="many-to-many-relationships"></a>
### Many to Many(N:N) 관계

[Has Many(1:N) 관계](#has-many-relationships)와 마찬가지로, "many to many(N:N)" 관계도 `has` 메서드를 사용해 생성할 수 있습니다.

```php
use App\Models\Role;
use App\Models\User;

$user = User::factory()
    ->has(Role::factory()->count(3))
    ->create();
```

<a name="pivot-table-attributes"></a>
#### 중간 테이블(피벗 테이블) 속성

모델들을 연결하는 중간 테이블(피벗 테이블)에 추가적인 속성을 설정해야 하는 경우, `hasAttached` 메서드를 사용할 수 있습니다. 이 메서드는 두 번째 인수로 피벗 테이블 속성들의 배열을 받습니다.

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

연관 모델에 접근해야 하는 상태 변형이 있다면, 클로저 기반의 상태 변형을 전달할 수 있습니다.

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

이미 생성된 모델 인스턴스를 새로운 모델들과 연관시키고 싶을 경우, `hasAttached` 메서드에 모델 인스턴스를 전달하면 됩니다. 아래 예시에서는, 동일한 세 개의 역할(Role)이 세 명의 사용자 모두에 연관되어 있습니다.

```php
$roles = Role::factory()->count(3)->create();

$users = User::factory()
    ->count(3)
    ->hasAttached($roles, ['active' => true])
    ->create();
```

<a name="many-to-many-relationships-using-magic-methods"></a>
#### 매직 메서드 활용

매직 팩토리 메서드를 사용하면 many to many 관계도 편리하게 정의할 수 있습니다. 아래 예시는 `User` 모델의 `roles` 연관관계를 통한 관계 설정입니다.

```php
$user = User::factory()
    ->hasRoles(1, [
        'name' => 'Editor'
    ])
    ->create();
```

<a name="polymorphic-relationships"></a>
### 폴리모픽 관계

[폴리모픽 관계](/docs/master/eloquent-relationships#polymorphic-relationships) 역시 팩토리를 이용해 생성할 수 있습니다. 폴리모픽 "morph many" 관계는 일반적인 "has many" 관계와 동일한 방식으로 생성합니다. 예를 들어 `App\Models\Post` 모델이 `App\Models\Comment` 모델과 `morphMany` 관계를 가지고 있다면 아래처럼 작성할 수 있습니다.

```php
use App\Models\Post;

$post = Post::factory()->hasComments(3)->create();
```

<a name="morph-to-relationships"></a>
#### Morph To 관계

매직 메서드는 `morphTo` 관계 생성을 지원하지 않습니다. 대신 `for` 메서드를 직접 사용하고, 연관관계의 이름을 명시해야 합니다. 예를 들어, `Comment` 모델에 `commentable`이라는 `morphTo` 관계가 정의되어 있다면, 아래와 같이 세 개의 댓글을 하나의 게시물에 속하도록 생성할 수 있습니다.

```php
$comments = Comment::factory()->count(3)->for(
    Post::factory(), 'commentable'
)->create();
```

<a name="polymorphic-many-to-many-relationships"></a>
#### 폴리모픽 Many to Many 관계

폴리모픽 "many to many"(`morphToMany` / `morphedByMany`) 관계 역시 일반적인 many to many 관계와 동일하게 만들 수 있습니다.

```php
use App\Models\Tag;
use App\Models\Video;

$video = Video::factory()
    ->hasAttached(
        Tag::factory()->count(3),
        ['public' => true]
    )
    ->create();
```

물론, 매직 `has` 메서드도 사용하여 폴리모픽 many to many 관계를 생성할 수 있습니다.

```php
$video = Video::factory()
    ->hasTags(3, ['public' => true])
    ->create();
```

<a name="defining-relationships-within-factories"></a>
### 팩토리 내부에서의 관계 정의

모델 팩토리 내부에서 관계를 정의하려면, 일반적으로 해당 관계의 외래키에 새 팩토리 인스턴스를 할당합니다. 이는 주로 `belongsTo`, `morphTo`와 같은 "역방향" 관계에서 사용됩니다. 예를 들어, 게시물 생성 시 자동으로 새로운 사용자를 만들고 싶다면 다음과 같이 합니다.

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

관계에 사용되는 컬럼이 팩토리에 정의된 다른 속성값에 따라 달라지는 경우, 속성에 클로저를 할당할 수 있습니다. 이 클로저는 팩토리에서 평가된 속성 배열을 전달받게 됩니다.

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
### 관계에서 기존 모델 재활용하기

여러 모델이 하나의 공통된 연관관계를 공유해야 할 경우, `recycle` 메서드를 사용하여 팩토리에서 생성되는 모든 연관관계에 동일한 모델 인스턴스를 재활용할 수 있습니다.

예를 들어, `Airline`, `Flight`, `Ticket` 모델이 있고, 티켓은 항공사와 항공편에 속하며, 항공편도 항공사에 속한다고 가정합니다. 티켓을 생성할 때 항공편과 티켓 모두 동일한 항공사에 속하기를 원한다면, 아래처럼 항공사 인스턴스를 `recycle` 메서드에 전달하면 됩니다.

```php
Ticket::factory()
    ->recycle(Airline::factory()->create())
    ->create();
```

`recycle` 메서드는 특히 모델이 동일한 사용자 또는 팀 등에 속할 때 더욱 유용합니다.

또한, `recycle` 메서드는 기존 모델들의 컬렉션도 인수로 받을 수 있습니다. 컬렉션을 전달하면, 팩토리가 해당 타입의 모델이 필요할 때마다 컬렉션에서 임의의 모델을 선택하게 됩니다.

```php
Ticket::factory()
    ->recycle($airlines)
    ->create();
```