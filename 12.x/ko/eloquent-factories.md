# Eloquent: 팩토리 (Eloquent: Factories)

- [소개](#introduction)
- [모델 팩토리 정의](#defining-model-factories)
    - [팩토리 생성](#generating-factories)
    - [팩토리 상태](#factory-states)
    - [팩토리 콜백](#factory-callbacks)
- [팩토리를 사용한 모델 생성](#creating-models-using-factories)
    - [모델 인스턴스화](#instantiating-models)
    - [모델 저장](#persisting-models)
    - [시퀀스](#sequences)
- [팩토리 연관관계](#factory-relationships)
    - [Has Many 연관관계](#has-many-relationships)
    - [Belongs To 연관관계](#belongs-to-relationships)
    - [다대다 연관관계](#many-to-many-relationships)
    - [폴리모픽 연관관계](#polymorphic-relationships)
    - [팩토리 내에서 연관관계 정의](#defining-relationships-within-factories)
    - [이미 생성된 모델을 연관관계에 재활용](#recycling-an-existing-model-for-relationships)

<a name="introduction"></a>
## 소개 (Introduction)

애플리케이션을 테스트하거나 데이터베이스를 시딩할 때, 데이터베이스에 몇 개의 레코드를 삽입해야 할 수 있습니다. 각 컬럼의 값을 일일이 지정하는 대신, Laravel에서는 각 [Eloquent 모델](/docs/12.x/eloquent)에 대해 모델 팩토리를 사용하여 기본 속성(attribute) 집합을 정의할 수 있도록 지원합니다.

팩토리가 어떻게 작성되는지 예시를 보려면, 애플리케이션의 `database/factories/UserFactory.php` 파일을 살펴보세요. 이 팩토리는 모든 새로운 Laravel 애플리케이션에 기본으로 포함되어 있으며, 다음과 같은 팩토리 정의가 담겨 있습니다:

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

보시다시피, 팩토리는 가장 기본적으로 Laravel의 기본 팩토리 클래스를 상속하고 `definition` 메서드를 정의하는 클래스입니다. `definition` 메서드에서는 팩토리를 이용해 모델을 생성할 때 적용할 기본 속성 값을 배열로 반환합니다.

`fake` 헬퍼를 통해 팩토리에서는 [Faker](https://github.com/FakerPHP/Faker) PHP 라이브러리에 접근할 수 있습니다. 이것을 사용하면 테스트 및 시딩용으로 다양한 랜덤 데이터를 손쉽게 생성할 수 있습니다.

> [!NOTE]
> 애플리케이션에서 Faker의 로케일을 변경하려면 `config/app.php` 파일의 `faker_locale` 옵션을 수정하면 됩니다.

<a name="defining-model-factories"></a>
## 모델 팩토리 정의 (Defining Model Factories)

<a name="generating-factories"></a>
### 팩토리 생성 (Generating Factories)

팩토리를 생성하려면, `make:factory` [Artisan 명령어](/docs/12.x/artisan)를 실행하세요:

```shell
php artisan make:factory PostFactory
```

새롭게 생성된 팩토리 클래스는 `database/factories` 디렉토리에 위치하게 됩니다.

<a name="factory-and-model-discovery-conventions"></a>
#### 모델과 팩토리 검색 규칙

팩토리를 정의했다면, 모델에 포함된 `Illuminate\Database\Eloquent\Factories\HasFactory` 트레잇의 정적 `factory` 메서드를 이용해 해당 모델의 팩토리 인스턴스를 생성할 수 있습니다.

`HasFactory` 트레잇의 `factory` 메서드는 지정된 모델에 맞는 적절한 팩토리를 자동으로 찾기 위해 아래와 같은 규칙을 따릅니다. 즉, `Database\Factories` 네임스페이스 내에 모델명과 동일하며, `Factory`라는 접미사가 붙은 클래스를 찾게 됩니다. 만약 이 규칙이 애플리케이션이나 팩토리에 맞지 않는다면, 모델에 `UseFactory` 속성(Attribute)을 추가해 직접 팩토리를 지정할 수 있습니다:

```php
use Illuminate\Database\Eloquent\Attributes\UseFactory;
use Database\Factories\Administration\FlightFactory;

#[UseFactory(FlightFactory::class)]
class Flight extends Model
{
    // ...
}
```

또는, 모델에서 `newFactory` 메서드를 오버라이드하여 직접 팩토리 인스턴스를 반환할 수도 있습니다:

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

그리고, 해당 팩토리 클래스에는 `model` 프로퍼티를 정의해야 합니다:

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

상태 변경 메서드를 사용하면 모델 팩토리에 여러 가지 상태 변형을 조합해서 적용할 수 있습니다. 예를 들어, `Database\Factories\UserFactory` 팩토리에 `suspended` 상태 메서드를 정의하여, 기본 속성 값 중 하나를 변경하도록 할 수 있습니다.

상태 변형 메서드는 일반적으로 Laravel의 기본 팩토리 클래스가 제공하는 `state` 메서드를 호출합니다. `state` 메서드는 팩토리에서 정의한 원시 속성 배열을 전달받는 클로저(closure)를 인수로 받아, 변경할 속성 배열을 반환해야 합니다:

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
#### "삭제됨(Trashed)" 상태

Eloquent 모델이 [소프트 삭제](/docs/12.x/eloquent#soft-deleting)를 지원하는 경우, 내장된 `trashed` 상태 메서드를 호출하여 생성된 모델이 이미 "소프트 삭제"된 상태로 나타내도록 할 수 있습니다. 이 상태는 모든 팩토리에서 자동으로 사용할 수 있으므로 직접 정의할 필요가 없습니다:

```php
use App\Models\User;

$user = User::factory()->trashed()->create();
```

<a name="factory-callbacks"></a>
### 팩토리 콜백 (Factory Callbacks)

팩토리 콜백은 `afterMaking` 및 `afterCreating` 메서드를 사용해 등록하며, 팩토리로 모델을 생성하거나 저장한 후에 추가 작업을 수행할 수 있게 해줍니다. 이런 콜백은 팩토리 클래스에 `configure` 메서드를 정의함으로써 등록하며, Laravel이 팩토리 인스턴스를 생성할 때 자동으로 호출해줍니다:

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

또한, 상태 메서드 내부에서도 팩토리 콜백을 등록할 수 있으며, 이 경우 해당 상태에만 특화된 작업을 수행할 수 있습니다:

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

팩토리를 정의한 후에는, 모델이 사용하는 `Illuminate\Database\Eloquent\Factories\HasFactory` 트레잇에서 제공하는 정적 `factory` 메서드를 통해 모델의 팩토리 인스턴스를 생성할 수 있습니다. 몇 가지 예제를 살펴보겠습니다. 먼저, `make` 메서드를 이용해 데이터베이스에는 저장하지 않고 모델 인스턴스를 생성해 보겠습니다:

```php
use App\Models\User;

$user = User::factory()->make();
```

`count` 메서드를 이용하면 여러 개의 모델 인스턴스를 컬렉션 형태로 생성할 수 있습니다:

```php
$users = User::factory()->count(3)->make();
```

<a name="applying-states"></a>
#### 상태 적용

모델에 원하는 [상태](#factory-states)를 적용할 수도 있습니다. 여러 개의 상태 변형을 적용하려면 상태 메서드를 연이어 호출하면 됩니다:

```php
$users = User::factory()->count(5)->suspended()->make();
```

<a name="overriding-attributes"></a>
#### 속성(Attributes) 오버라이드

모델의 기본 값 중 일부를 변경하고 싶다면, 값을 배열로 `make` 메서드에 전달할 수 있습니다. 지정한 속성만 덮어쓰고, 나머지 속성은 팩토리에 정의된 기본 값이 유지됩니다:

```php
$user = User::factory()->make([
    'name' => 'Abigail Otwell',
]);
```

또는, 팩토리 인스턴스에 직접 `state` 메서드를 호출해 인라인 상태 변형을 적용할 수 있습니다:

```php
$user = User::factory()->state([
    'name' => 'Abigail Otwell',
])->make();
```

> [!NOTE]
> 팩토리를 이용해 모델을 생성할 때는 [대량 할당 보호](/docs/12.x/eloquent#mass-assignment)가 자동으로 비활성화됩니다.

<a name="persisting-models"></a>
### 모델 저장 (Persisting Models)

`create` 메서드는 모델 인스턴스를 생성한 후, Eloquent의 `save` 메서드를 이용하여 데이터베이스에 저장합니다:

```php
use App\Models\User;

// 하나의 App\Models\User 인스턴스 생성
$user = User::factory()->create();

// 세 개의 App\Models\User 인스턴스 생성
$users = User::factory()->count(3)->create();
```

팩토리의 기본 모델 속성을 오버라이드하려면, 속성 배열을 `create` 메서드에 전달하면 됩니다:

```php
$user = User::factory()->create([
    'name' => 'Abigail',
]);
```

<a name="sequences"></a>
### 시퀀스 (Sequences)

때로는 생성되는 각 모델마다 특정 속성 값을 번갈아가며 설정하고 싶을 때가 있습니다. 이럴 때는 상태 변형을 시퀀스 형태로 정의하면 됩니다. 예를 들어, 각 사용자의 `admin` 컬럼 값을 `Y`, `N`으로 번갈아가면서 생성하려면 다음과 같이 할 수 있습니다:

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

위 예시에서 10명의 사용자 중 5명은 `admin` 값이 `Y`, 나머지 5명은 `N`으로 생성됩니다.

필요하다면, 시퀀스 값으로 클로저를 사용할 수도 있습니다. 클로저는 시퀀스가 새 값을 필요로 할 때마다 실행됩니다:

```php
use Illuminate\Database\Eloquent\Factories\Sequence;

$users = User::factory()
    ->count(10)
    ->state(new Sequence(
        fn (Sequence $sequence) => ['role' => UserRoles::all()->random()],
    ))
    ->create();
```

시퀀스 클로저 내부에서는, 클로저로 주입되는 시퀀스 인스턴스의 `$index` 프로퍼티를 활용할 수 있습니다. `$index`는 현재까지 시퀀스가 몇 번 반복되었는지 나타냅니다:

```php
$users = User::factory()
    ->count(10)
    ->state(new Sequence(
        fn (Sequence $sequence) => ['name' => 'Name '.$sequence->index],
    ))
    ->create();
```

편의를 위해, `sequence` 메서드를 사용해 시퀀스를 적용할 수도 있습니다. 이 메서드는 내부적으로 `state` 메서드를 호출하며, 클로저나 속성 배열들을 인수로 받을 수 있습니다:

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
## 팩토리 연관관계 (Factory Relationships)

<a name="has-many-relationships"></a>
### Has Many 연관관계

이제, Laravel의 다양한 팩토리 메서드로 Eloquent 모델의 연관관계를 만들어 보겠습니다. 우선, `App\Models\User` 모델과 `App\Models\Post` 모델이 있다고 가정하고, `User` 모델이 `Post`와 `hasMany` 연관관계를 정의했다고 해봅니다. `has` 메서드에 팩토리 인스턴스를 전달하면, 사용자(user)가 3개의 게시물(post)을 가지고 있는 상태로 생성할 수 있습니다:

```php
use App\Models\Post;
use App\Models\User;

$user = User::factory()
    ->has(Post::factory()->count(3))
    ->create();
```

`has` 메서드에 `Post` 모델을 전달하면, Laravel에서는 `User` 모델에 `posts`라는 연관관계 메서드가 있어야 한다고 가정합니다. 필요하다면, 조작하려는 연관관계의 이름을 명시적으로 지정할 수도 있습니다:

```php
$user = User::factory()
    ->has(Post::factory()->count(3), 'posts')
    ->create();
```

물론, 연관된 모델에도 상태 변형을 적용할 수 있습니다. 또한, 상태 변경이 부모 모델에 접근해야 하는 경우 클로저 기반 상태 변형도 전달할 수 있습니다:

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
#### 매직 메서드(Magic Methods) 사용

편의상, Laravel의 매직 팩토리 연관관계 메서드를 사용해 연관관계를 쉽게 정의할 수 있습니다. 예를 들어, 아래와 같이 작성하면 `User` 모델의 `posts` 메서드로 연관된 모델이 생성됩니다:

```php
$user = User::factory()
    ->hasPosts(3)
    ->create();
```

매직 메서드로 팩토리 연관관계를 만들 때는, 연관된 모델의 속성을 오버라이드하는 배열을 전달할 수 있습니다:

```php
$user = User::factory()
    ->hasPosts(3, [
        'published' => false,
    ])
    ->create();
```

부모 모델에 접근해야 상태 변형을 할 경우, 클로저를 전달할 수도 있습니다:

```php
$user = User::factory()
    ->hasPosts(3, function (array $attributes, User $user) {
        return ['user_type' => $user->type];
    })
    ->create();
```

<a name="belongs-to-relationships"></a>
### Belongs To 연관관계

앞에서 "has many" 연관관계를 팩토리로 만드는 방법을 살펴보았으니, 이번에는 그 반대 방향인 "belongs to" 연관관계를 만들어보겠습니다. `for` 메서드는 팩토리로 생성되는 모델이 어느 부모 모델에 속하는지를 지정합니다. 예를 들어, 한 사용자(user)에 소속된 3개의 `App\Models\Post` 인스턴스를 생성하려면 다음과 같이 합니다:

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

이미 생성된 부모 모델 인스턴스가 있다면, 그 인스턴스를 `for` 메서드에 바로 전달할 수 있습니다:

```php
$user = User::factory()->create();

$posts = Post::factory()
    ->count(3)
    ->for($user)
    ->create();
```

<a name="belongs-to-relationships-using-magic-methods"></a>
#### 매직 메서드 사용

역시, 매직 팩토리 연관관계 메서드를 이용해 "belongs to" 연관관계를 선언할 수도 있습니다. 예를 들어, 아래 코드는 3개의 포스트(post)가 모두 `Post` 모델의 `user` 연관관계에 속하도록 만듭니다:

```php
$posts = Post::factory()
    ->count(3)
    ->forUser([
        'name' => 'Jessica Archer',
    ])
    ->create();
```

<a name="many-to-many-relationships"></a>
### 다대다 연관관계 (Many to Many Relationships)

[Has many 연관관계](#has-many-relationships)와 마찬가지로, 다대다(many-to-many) 연관관계도 `has` 메서드로 생성할 수 있습니다:

```php
use App\Models\Role;
use App\Models\User;

$user = User::factory()
    ->has(Role::factory()->count(3))
    ->create();
```

<a name="pivot-table-attributes"></a>
#### Pivot(중간) 테이블 속성

두 모델을 연결하는 pivot(중간) 테이블에 별도의 속성 값을 저장해야 할 경우, `hasAttached` 메서드를 사용할 수 있습니다. 이 메서드는 두 번째 인수로 pivot 테이블의 속성명과 값의 배열을 받습니다:

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

연관된 모델에 접근해야 상태 변형이 필요한 경우, 클로저 기반 상태 변형을 전달할 수도 있습니다:

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

이미 생성해둔 모델 인스턴스들이 있다면, 그 인스턴스들을 `hasAttached`에 바로 전달할 수 있습니다. 아래 예시에서는 같은 3개의 역할(role)이 모든 사용자에 붙습니다:

```php
$roles = Role::factory()->count(3)->create();

$users = User::factory()
    ->count(3)
    ->hasAttached($roles, ['active' => true])
    ->create();
```

<a name="many-to-many-relationships-using-magic-methods"></a>
#### 매직 메서드 사용

편의를 위해 매직 팩토리 연관관계 메서드로 다대다 연관관계를 정의할 수 있습니다. 아래 예시는, 관련된 모델을 `User` 모델의 `roles` 메서드를 통해 생성하도록 자동으로 판단합니다:

```php
$user = User::factory()
    ->hasRoles(1, [
        'name' => 'Editor'
    ])
    ->create();
```

<a name="polymorphic-relationships"></a>
### 폴리모픽 연관관계 (Polymorphic Relationships)

[폴리모픽 연관관계](/docs/12.x/eloquent-relationships#polymorphic-relationships) 역시 팩토리를 사용해 생성할 수 있습니다. 폴리모픽 "morph many" 관계는 일반적인 "has many" 관계와 마찬가지로 생성됩니다. 예를 들어, `App\Models\Post` 모델이 `App\Models\Comment` 모델과 `morphMany` 관계를 가진 경우는 다음처럼 작성합니다:

```php
use App\Models\Post;

$post = Post::factory()->hasComments(3)->create();
```

<a name="morph-to-relationships"></a>
#### Morph To 연관관계

매직 메서드를 사용해 `morphTo` 연관관계를 만들 수는 없습니다. 대신, 반드시 `for` 메서드를 직접 써서 관계 이름도 명시적으로 지정해야 합니다. 예를 들어, `Comment` 모델에 `commentable`이라는 `morphTo` 관계가 있을 때, 아래처럼 작성하여 포스트(post)에 소속된 댓글(comment) 3개를 생성할 수 있습니다:

```php
$comments = Comment::factory()->count(3)->for(
    Post::factory(), 'commentable'
)->create();
```

<a name="polymorphic-many-to-many-relationships"></a>
#### 폴리모픽 다대다 연관관계

폴리모픽 "다대다"(`morphToMany` / `morphedByMany`) 연관관계도 보통의 다대다 연관관계와 동일하게 생성할 수 있습니다:

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

또한, 매직 `has` 메서드를 이용해 폴리모픽 다대다 연관관계를 생성할 수도 있습니다:

```php
$video = Video::factory()
    ->hasTags(3, ['public' => true])
    ->create();
```

<a name="defining-relationships-within-factories"></a>
### 팩토리 내에서 연관관계 정의

팩토리 내부에서 연관관계를 정의하려면, 보통 관계의 외래 키에 새로운 팩토리 인스턴스를 할당합니다. 이는 `belongsTo` 및 `morphTo` 같은 "역방향" 연관관계에서 자주 사용되는 패턴입니다. 예를 들어, 게시물(post)을 생성할 때 새로운 사용자(user)도 함께 생성하고 싶다면 다음처럼 작성합니다:

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

연관관계의 컬럼이 팩토리에서 정의한 값에 의존하는 경우, 속성에 클로저를 할당할 수 있습니다. 이 클로저는 팩토리에서 평가한(생성된) 속성 배열을 전달받습니다:

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
### 이미 생성된 모델을 연관관계에 재활용 (Recycling an Existing Model for Relationships)

여러 모델이 공통된 다른 모델과 연관관계를 맺고 있는 경우, 팩토리의 `recycle` 메서드를 사용하면 연관관계에 대해 단일 인스턴스를 재사용할 수 있습니다.

예를 들어, `Airline`, `Flight`, `Ticket` 모델이 모두 서로 관계가 있고, 티켓(ticket)은 항공사와 항공편에 속해 있으며, 항공편(flight) 역시 항공사(airline)에 속해 있다고 가정해봅니다. 티켓을 만들 때, 티켓과 항공편 모두 같은 항공사를 참조하기를 원한다면, 항공사 인스턴스를 `recycle` 메서드에 전달하면 됩니다:

```php
Ticket::factory()
    ->recycle(Airline::factory()->create())
    ->create();
```

`recycle` 메서드는 여러 모델이 같은 사용자나 팀에 속해야 할 때 특히 유용합니다.

또한, `recycle` 메서드는 기존 모델의 컬렉션도 받을 수 있습니다. 이 경우, 팩토리가 해당 유형의 모델이 필요할 때마다 컬렉션에서 임의의 모델이 선택됩니다:

```php
Ticket::factory()
    ->recycle($airlines)
    ->create();
```