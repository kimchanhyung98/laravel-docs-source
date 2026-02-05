# Eloquent: 팩토리 (Eloquent: Factories)

- [소개](#introduction)
- [모델 팩토리 정의하기](#defining-model-factories)
    - [팩토리 생성하기](#generating-factories)
    - [팩토리 상태(State)](#factory-states)
    - [팩토리 콜백](#factory-callbacks)
- [팩토리를 사용한 모델 생성](#creating-models-using-factories)
    - [모델 인스턴스화](#instantiating-models)
    - [모델 저장(Persisting Models)](#persisting-models)
    - [시퀀스(Sequences)](#sequences)
- [팩토리 기반 연관관계](#factory-relationships)
    - [Has Many 연관관계](#has-many-relationships)
    - [Belongs To 연관관계](#belongs-to-relationships)
    - [Many to Many 연관관계](#many-to-many-relationships)
    - [폴리모픽 연관관계](#polymorphic-relationships)
    - [팩토리 내부에서 연관관계 정의](#defining-relationships-within-factories)
    - [관계 재사용(Recycle)](#recycling-an-existing-model-for-relationships)

<a name="introduction"></a>
## 소개 (Introduction)

애플리케이션을 테스트하거나 데이터베이스를 시딩(seeding)할 때, 데이터베이스에 몇 개의 레코드를 삽입해야 할 필요가 있습니다. 각 컬럼의 값을 일일이 수동으로 지정하는 대신, Laravel은 각 [Eloquent 모델](/docs/master/eloquent)에 대해 기본 속성 집합을 모델 팩토리를 통해 정의할 수 있도록 지원합니다.

팩토리를 작성하는 방법을 직접 살펴보려면, 애플리케이션의 `database/factories/UserFactory.php` 파일을 열어보시기 바랍니다. 이 팩토리는 모든 새로운 Laravel 애플리케이션에 포함되어 있으며, 아래와 같은 팩토리 정의가 들어 있습니다.

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

보시는 바와 같이, 기본적인 형태에서 팩토리는 Laravel의 기본 팩토리 클래스를 확장하고 `definition` 메서드를 정의하는 클래스입니다. `definition` 메서드는 이 팩토리를 사용하여 모델을 생성할 때 적용되는 기본 속성 값을 배열로 반환합니다.

팩토리는 `fake` 헬퍼를 통해 [Faker](https://github.com/FakerPHP/Faker) PHP 라이브러리를 사용할 수 있어, 테스트 및 시딩에 필요한 다양한 유형의 임의 데이터를 손쉽게 생성할 수 있습니다.

> [!NOTE]
> 애플리케이션의 Faker locale을 변경하려면, `config/app.php` 파일의 `faker_locale` 옵션을 수정하세요.

<a name="defining-model-factories"></a>
## 모델 팩토리 정의하기 (Defining Model Factories)

<a name="generating-factories"></a>
### 팩토리 생성하기 (Generating Factories)

팩토리를 생성하려면 `make:factory` [Artisan 명령어](/docs/master/artisan)를 실행하세요.

```shell
php artisan make:factory PostFactory
```

새롭게 생성된 팩토리 클래스는 `database/factories` 디렉터리에 위치합니다.

<a name="factory-and-model-discovery-conventions"></a>
#### 모델과 팩토리 탐색 규칙

팩토리를 정의한 후에는, 모델에 `Illuminate\Database\Eloquent\Factories\HasFactory` 트레이트를 추가하여 제공되는 정적 `factory` 메서드를 통해 해당 모델의 팩토리 인스턴스를 생성할 수 있습니다.

`HasFactory` 트레이트의 `factory` 메서드는, 해당 트레이트가 할당된 모델에 대해 올바른 팩토리 클래스를 규칙에 따라 자동으로 찾습니다. 구체적으로, `Database\Factories` 네임스페이스에서 모델명과 일치하고 `Factory` 접미사가 붙은 클래스를 탐색합니다. 만약 이 규칙을 따르지 않는 경우, `UseFactory` 속성을 모델에 추가하여 팩토리 클래스를 직접 지정할 수 있습니다.

```php
use Illuminate\Database\Eloquent\Attributes\UseFactory;
use Database\Factories\Administration\FlightFactory;

#[UseFactory(FlightFactory::class)]
class Flight extends Model
{
    // ...
}
```

또는, 모델 내에 `newFactory` 메서드를 오버라이드하여 해당 모델의 팩토리 인스턴스를 반환할 수도 있습니다.

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

그리고, 해당 팩토리 클래스 내에 `model` 속성을 정의해 줍니다.

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
### 팩토리 상태(State)

상태(State) 조작 메서드를 사용하면, 모델 팩토리에 다양한 변형을 조합하여 적용할 수 있습니다. 예를 들어, `Database\Factories\UserFactory` 팩토리에 `suspended` 상태 메서드를 추가하여 기본 속성 중 하나를 변경할 수 있습니다.

상태 변형 메서드는 일반적으로 Laravel의 기본 팩토리 클래스에 내장된 `state` 메서드를 호출합니다. 이 메서드는 팩토리에 정의된 원본 속성 배열을 받아, 수정할 속성을 반환하는 클로저를 인수로 받습니다.

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

Eloquent 모델이 [소프트 삭제](/docs/master/eloquent#soft-deleting)를 지원할 경우, 내장된 `trashed` 상태 메서드를 사용하여 생성된 모델이 이미 "소프트 삭제"된 상태임을 나타낼 수 있습니다. 이 상태는 모든 팩토리에서 자동으로 사용할 수 있으므로 별도로 정의하지 않아도 됩니다.

```php
use App\Models\User;

$user = User::factory()->trashed()->create();
```

<a name="factory-callbacks"></a>
### 팩토리 콜백 (Factory Callbacks)

팩토리 콜백은 `afterMaking` 및 `afterCreating` 메서드를 통해 등록할 수 있으며, 모델을 make 또는 create한 후 추가 작업을 수행할 수 있습니다. 이러한 콜백은 팩토리 클래스 내에 `configure` 메서드를 정의해서 등록하는 것이 일반적입니다. Laravel은 팩토리 인스턴스화 시 이 메서드를 자동으로 호출합니다.

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

또한, 특정 상태에만 해당하는 콜백을 팩토리 상태 메서드 내에서 직접 등록할 수도 있습니다.

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

팩토리를 정의했다면, 모델에 추가한 `Illuminate\Database\Eloquent\Factories\HasFactory` 트레이트의 정적 `factory` 메서드를 사용해 해당 모델의 팩토리 인스턴스를 생성할 수 있습니다. 아래 예시에서처럼, `make` 메서드를 사용하여 데이터베이스에는 저장하지 않은 채로 모델 인스턴스를 만들 수 있습니다.

```php
use App\Models\User;

$user = User::factory()->make();
```

여러 개의 모델 인스턴스를 생성하려면 `count` 메서드를 사용하세요.

```php
$users = User::factory()->count(3)->make();
```

<a name="applying-states"></a>
#### 상태 적용하기

원하는 경우, 팩토리에 정의한 [상태(State)](#factory-states)를 적용할 수 있습니다. 여러 상태 변형을 적용하고 싶다면 단순히 상태 메서드를 연달아 호출하면 됩니다.

```php
$users = User::factory()->count(5)->suspended()->make();
```

<a name="overriding-attributes"></a>
#### 속성 오버라이드

모델의 기본 속성값 중 일부를 덮어쓰고 싶다면, `make` 메서드에 값을 배열로 전달하면 됩니다. 지정하지 않은 속성은 팩토리에 정의된 기본값이 적용됩니다.

```php
$user = User::factory()->make([
    'name' => 'Abigail Otwell',
]);
```

또는, 팩토리 인스턴스에서 바로 `state` 메서드를 호출해 인라인 상태 변형을 적용할 수도 있습니다.

```php
$user = User::factory()->state([
    'name' => 'Abigail Otwell',
])->make();
```

> [!NOTE]
> 팩토리를 사용해 모델을 생성할 때는 [대량 할당 보호(Mass assignment protection)](/docs/master/eloquent#mass-assignment)가 자동으로 비활성화됩니다.

<a name="persisting-models"></a>
### 모델 저장(Persisting Models)

`create` 메서드는 모델 인스턴스를 생성하고, Eloquent의 `save` 메서드를 이용해 데이터베이스에 저장합니다.

```php
use App\Models\User;

// 단일 App\Models\User 인스턴스 생성...
$user = User::factory()->create();

// 세 개의 App\Models\User 인스턴스 생성...
$users = User::factory()->count(3)->create();
```

`create` 메서드에 배열로 속성을 전달하면, 팩토리의 기본 속성을 오버라이드할 수 있습니다.

```php
$user = User::factory()->create([
    'name' => 'Abigail',
]);
```

<a name="sequences"></a>
### 시퀀스(Sequences)

각 모델을 생성할 때마다 특정 속성값을 번갈아 가며 출력하고 싶을 때가 있습니다. 이럴 때 상태 변환을 시퀀스로 정의할 수 있습니다. 예를 들어, 사용자를 만들 때 `admin` 컬럼의 값을 번갈아 `Y`, `N`으로 할당하려면 다음과 같이 작성합니다.

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

이 경우, 다섯 명의 사용자는 `admin` 값이 `Y`로, 나머지 다섯 명의 사용자는 `N`으로 생성됩니다.

필요하다면 시퀀스 값으로 클로저를 사용할 수도 있습니다. 시퀀스가 새 값을 필요로 할 때마다 해당 클로저가 호출됩니다.

```php
use Illuminate\Database\Eloquent\Factories\Sequence;

$users = User::factory()
    ->count(10)
    ->state(new Sequence(
        fn (Sequence $sequence) => ['role' => UserRoles::all()->random()],
    ))
    ->create();
```

시퀀스 클로저 내부에서는 주입된 시퀀스 인스턴스의 `$index` 속성에 접근할 수 있습니다. 이 속성은 현재까지 시퀀스가 몇 번 반복되었는지를 나타냅니다.

```php
$users = User::factory()
    ->count(10)
    ->state(new Sequence(
        fn (Sequence $sequence) => ['name' => 'Name '.$sequence->index],
    ))
    ->create();
```

편의상, 시퀀스를 적용하는 `sequence` 메서드도 사용할 수 있습니다. 이 메서드는 내부적으로 `state` 메서드를 호출하며, 클로저 또는 속성 배열을 인수로 받습니다.

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
## 팩토리 기반 연관관계 (Factory Relationships)

<a name="has-many-relationships"></a>
### Has Many 연관관계

이제 Laravel의 간결한 팩토리 메서드를 활용해 Eloquent 모델 간의 연관관계를 빌드해 봅시다. 예를 들어, `App\Models\User` 모델과 `App\Models\Post` 모델이 있다고 가정하겠습니다. 또한 `User` 모델이 `Post` 모델과 `hasMany` 연관관계를 갖고 있다고 할 때, 라라벨 팩토리의 `has` 메서드를 사용해 세 개의 게시글을 가진 사용자를 생성할 수 있습니다. `has` 메서드는 팩토리 인스턴스를 인수로 받습니다.

```php
use App\Models\Post;
use App\Models\User;

$user = User::factory()
    ->has(Post::factory()->count(3))
    ->create();
```

관례상, `has` 메서드에 `Post` 모델을 전달하면, Laravel은 `User` 모델에 `posts`라는 연관관계 메서드가 있다고 가정합니다. 필요하다면 직접 조작할 연관관계의 이름을 명시할 수도 있습니다.

```php
$user = User::factory()
    ->has(Post::factory()->count(3), 'posts')
    ->create();
```

물론, 연관된 모델에도 상태 변형을 적용할 수 있습니다. 또한, 상태 변경이 부모 모델에 접근해야 하는 경우에는 클로저로 상태 변형을 전달할 수 있습니다.

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
#### 매직 메서드(Magic Methods) 사용하기

더 편리하게, Laravel의 매직 팩토리 연관관계 메서드를 사용할 수도 있습니다. 아래 예시처럼, Laravel은 관례에 따라 관련 모델들을 `User` 모델에 정의된 `posts` 연관관계 메서드를 통해 생성해야 함을 자동으로 결정합니다.

```php
$user = User::factory()
    ->hasPosts(3)
    ->create();
```

매직 메서드를 사용할 때, 연관 모델의 속성 값을 배열로 오버라이드할 수도 있습니다.

```php
$user = User::factory()
    ->hasPosts(3, [
        'published' => false,
    ])
    ->create();
```

상태 변형이 부모 모델에 접근해야 할 때는 클로저 형태로 전달할 수도 있습니다.

```php
$user = User::factory()
    ->hasPosts(3, function (array $attributes, User $user) {
        return ['user_type' => $user->type];
    })
    ->create();
```

<a name="belongs-to-relationships"></a>
### Belongs To 연관관계

이제 `has many` 연관관계 생성에 대해 살펴보았으니, 이번에는 그 반대쪽을 살펴봅니다. `for` 메서드는 팩토리로 생성한 모델이 어떤 부모 모델에 속해 있는지 정의할 때 사용합니다. 예를 들어, 한 명의 사용자에 속한 세 개의 `App\Models\Post` 모델을 만들려면 다음과 같이 작성합니다.

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

이미 생성해둔 부모 모델 인스턴스가 있다면, 이를 바로 `for` 메서드에 전달할 수 있습니다.

```php
$user = User::factory()->create();

$posts = Post::factory()
    ->count(3)
    ->for($user)
    ->create();
```

<a name="belongs-to-relationships-using-magic-methods"></a>
#### 매직 메서드 사용하기

편의를 위해, Laravel의 매직 팩토리 연관관계 메서드를 사용하여 "belongs to" 관계를 정의할 수 있습니다. 예를 들어, 아래 예시는 세 개의 게시글이 `Post` 모델의 `user` 연관관계에 속해야 한다는 것을 관례에 따라 자동으로 판단합니다.

```php
$posts = Post::factory()
    ->count(3)
    ->forUser([
        'name' => 'Jessica Archer',
    ])
    ->create();
```

<a name="many-to-many-relationships"></a>
### Many to Many 연관관계

[Has Many 연관관계](#has-many-relationships)와 마찬가지로, "many to many" 연관관계도 `has` 메서드를 사용해 생성할 수 있습니다.

```php
use App\Models\Role;
use App\Models\User;

$user = User::factory()
    ->has(Role::factory()->count(3))
    ->create();
```

<a name="pivot-table-attributes"></a>
#### Pivot 테이블 속성

모델을 연결하는 Pivot(중간) 테이블에 특정 속성을 지정해야 한다면, `hasAttached` 메서드를 사용할 수 있습니다. 이 메서드는 두 번째 인수로 Pivot 테이블에 저장할 속성 이름과 값을 배열로 받습니다.

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

상태 변형이 연관 모델에 접근해야 할 경우, 클로저 형태로 상태 변형을 전달할 수도 있습니다.

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

이미 생성된 모델 인스턴스를 연결하려면, 해당 인스턴스들을 `hasAttached`에 전달하면 됩니다. 아래 예시에서는 동일한 세 개의 역할(role)이 세 명의 모든 사용자와 연결됩니다.

```php
$roles = Role::factory()->count(3)->create();

$users = User::factory()
    ->count(3)
    ->hasAttached($roles, ['active' => true])
    ->create();
```

<a name="many-to-many-relationships-using-magic-methods"></a>
#### 매직 메서드 사용하기

편의상, Laravel의 매직 팩토리 연관관계 메서드를 이용해 many to many 관계를 정의할 수 있습니다. 예를 들어, 아래 코드는 연관 모델을 `User` 모델의 `roles` 연관관계로 생성해야 한다는 것을 자동으로 판단합니다.

```php
$user = User::factory()
    ->hasRoles(1, [
        'name' => 'Editor'
    ])
    ->create();
```

<a name="polymorphic-relationships"></a>
### 폴리모픽 연관관계

[폴리모픽 연관관계](/docs/master/eloquent-relationships#polymorphic-relationships)도 팩토리를 이용해 생성할 수 있습니다. 폴리모픽 "morph many" 연관관계는 일반적인 "has many"와 동일합니다. 예를 들어, `App\Models\Post`가 `App\Models\Comment`와 `morphMany` 연관관계를 가진 경우는 다음과 같습니다.

```php
use App\Models\Post;

$post = Post::factory()->hasComments(3)->create();
```

<a name="morph-to-relationships"></a>
#### Morph To 연관관계

매직 메서드를 이용해 `morphTo` 연관관계를 만들 수는 없습니다. 대신, `for` 메서드를 직접 사용하고 연관관계의 이름을 명확하게 지정해주어야 합니다. 예를 들어, `Comment` 모델에 `morphTo` 연관관계인 `commentable` 메서드가 있다고 할 때, 아래처럼 사용합니다.

```php
$comments = Comment::factory()->count(3)->for(
    Post::factory(), 'commentable'
)->create();
```

<a name="polymorphic-many-to-many-relationships"></a>
#### 폴리모픽 Many to Many 연관관계

폴리모픽 "many to many"(`morphToMany` / `morphedByMany`) 연관관계도 일반적인 many to many 관계와 동일하게 팩토리로 생성할 수 있습니다.

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

물론, 매직 `has` 메서드를 이용해서도 폴리모픽 many to many 관계를 만들 수 있습니다.

```php
$video = Video::factory()
    ->hasTags(3, ['public' => true])
    ->create();
```

<a name="defining-relationships-within-factories"></a>
### 팩토리 내부에서 연관관계 정의

팩토리 내부에서 연관관계를 정의할 때는, 일반적으로 외래키(foreign key)에 새 팩토리 인스턴스를 할당합니다. 주로 `belongsTo`나 `morphTo`처럼 "역방향" 연관관계에서 사용됩니다. 예를 들어, 게시글을 만들 때 사용자도 함께 생성하려면 아래와 같이 작성합니다.

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

관계 컬럼이 팩토리를 정의하는 쪽의 속성에 의존해야 한다면, 해당 속성에 클로저를 지정할 수 있습니다. 클로저에는 팩토리에서 평가(evaluate)된 속성 배열이 전달됩니다.

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
### 관계 재사용(Recycle)

여러 모델이 동일한 연관관계를 공유하는 경우, `recycle` 메서드를 사용해 팩토리가 생성하는 모든 연관관계에서 하나의 관련 모델 인스턴스를 재활용할 수 있습니다.

예를 들어, `Airline`, `Flight`, `Ticket` 모델이 있다고 가정해 보겠습니다. 여기서 티켓은 항공사와 비행편에 속해 있고, 비행편도 항공사에 속합니다. 티켓 생성 시 티켓과 비행편 모두 동일한 항공사를 갖도록 하려면, 항공사 인스턴스를 `recycle` 메서드에 전달할 수 있습니다.

```php
Ticket::factory()
    ->recycle(Airline::factory()->create())
    ->create();
```

공통된 사용자(user)나 팀(team)에 속하는 여러 모델을 만드는 경우, `recycle` 메서드는 특히 유용합니다.

`recycle` 메서드는 기존 모델의 컬렉션도 받을 수 있습니다. 컬렉션을 전달하면, 팩토리가 해당 타입의 모델이 필요할 때마다 컬렉션에서 임의로 하나를 선택하게 됩니다.

```php
Ticket::factory()
    ->recycle($airlines)
    ->create();
```
