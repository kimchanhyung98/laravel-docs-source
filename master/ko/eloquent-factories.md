# Eloquent: 팩토리 (Factories)

- [소개](#introduction)
- [모델 팩토리 정의하기](#defining-model-factories)
    - [팩토리 생성하기](#generating-factories)
    - [팩토리 상태](#factory-states)
    - [팩토리 콜백](#factory-callbacks)
- [팩토리를 사용하여 모델 생성하기](#creating-models-using-factories)
    - [모델 인스턴스화](#instantiating-models)
    - [모델 저장하기](#persisting-models)
    - [시퀀스](#sequences)
- [팩토리 관계](#factory-relationships)
    - [Has Many 관계](#has-many-relationships)
    - [Belongs To 관계](#belongs-to-relationships)
    - [Many to Many 관계](#many-to-many-relationships)
    - [다형 관계 (Polymorphic Relationships)](#polymorphic-relationships)
    - [팩토리 내에서 관계 정의하기](#defining-relationships-within-factories)
    - [관계에 기존 모델 재사용하기](#recycling-an-existing-model-for-relationships)

<a name="introduction"></a>
## 소개 (Introduction)

애플리케이션을 테스트하거나 데이터베이스를 시딩할 때 데이터베이스에 몇 개의 레코드를 삽입해야 하는 경우가 있습니다. 각 컬럼의 값을 일일이 수동으로 지정하는 대신, Laravel은 모델 팩토리를 사용하여 각 [Eloquent 모델](/docs/master/eloquent)의 기본 속성 세트를 정의할 수 있게 해줍니다.

팩토리를 작성하는 예제를 보고 싶다면, 애플리케이션의 `database/factories/UserFactory.php` 파일을 참고하세요. 이 팩토리는 모든 새 Laravel 애플리케이션에 포함되어 있으며, 다음과 같은 팩토리 정의를 포함합니다:

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

가장 기본적인 형태에서 팩토리는 Laravel의 기본 팩토리 클래스를 상속하는 클래스이며, `definition` 메서드를 정의합니다. `definition` 메서드는 팩토리를 사용하여 모델을 생성할 때 적용할 기본 속성 값 세트를 반환합니다.

`fake` 헬퍼를 통해 팩토리는 [Faker](https://github.com/FakerPHP/Faker) PHP 라이브러리에 접근할 수 있으며, 이를 통해 테스트와 시딩을 위한 다양한 종류의 무작위 데이터를 편리하게 생성할 수 있습니다.

> [!NOTE]
> 애플리케이션의 Faker 로케일은 `config/app.php` 설정 파일의 `faker_locale` 옵션을 변경하여 설정할 수 있습니다.

<a name="defining-model-factories"></a>
## 모델 팩토리 정의하기 (Defining Model Factories)

<a name="generating-factories"></a>
### 팩토리 생성하기 (Generating Factories)

팩토리를 생성하려면 `make:factory` [Artisan 명령어](/docs/master/artisan)를 실행하세요:

```shell
php artisan make:factory PostFactory
```

새 팩토리 클래스는 `database/factories` 디렉토리에 생성됩니다.

<a name="factory-and-model-discovery-conventions"></a>
#### 모델과 팩토리 발견 규칙 (Model and Factory Discovery Conventions)

팩토리를 정의한 후에는 `Illuminate\Database\Eloquent\Factories\HasFactory` 트레이트가 모델에 제공하는 정적 `factory` 메서드를 사용해서 해당 모델에 대한 팩토리 인스턴스를 생성할 수 있습니다.

`HasFactory` 트레이트의 `factory` 메서드는 규칙에 따라 해당 모델에 알맞은 팩토리를 찾아 사용합니다. 구체적으로, 이 메서드는 `Database\Factories` 네임스페이스 안에서 모델 이름에 대응하는 클래스 이름에 `Factory`가 접미어로 붙은 팩토리를 찾습니다. 만약 이러한 규칙이 애플리케이션이나 팩토리에 적합하지 않으면, 모델에서 `newFactory` 메서드를 재정의하여 직접 해당 모델 팩토리 인스턴스를 반환할 수 있습니다:

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

그 다음, 해당 팩토리 클래스 내에 `model` 속성을 정의합니다:

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

상태 조작 메서드는 모델 팩토리에서 여러 개의 구분된 변경 사항을 정의하고, 이를 필요에 따라 조합하여 적용할 수 있게 합니다. 예를 들어 `Database\Factories\UserFactory` 팩토리에는 `suspended` 상태 메서드가 있어 기본 속성 중 하나를 변경할 수 있습니다.

상태 변환 메서드는 보통 Laravel의 기본 팩토리 클래스에서 제공하는 `state` 메서드를 호출합니다. 이 `state` 메서드는 클로저를 인자로 받는데, 이 클로저는 팩토리를 위해 정의된 원시 속성 배열을 받아서 변경할 속성 배열을 반환해야 합니다:

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

Eloquent 모델이 [soft delete (소프트 삭제)](/docs/master/eloquent#soft-deleting)를 지원한다면, 이미 "soft deleted" 상태인 모델을 만들도록 나타내는 내장된 `trashed` 상태 메서드를 사용할 수 있습니다. `trashed` 상태는 모든 팩토리에 자동으로 제공되므로 직접 정의할 필요가 없습니다:

```php
use App\Models\User;

$user = User::factory()->trashed()->create();
```

<a name="factory-callbacks"></a>
### 팩토리 콜백 (Factory Callbacks)

팩토리 콜백은 `afterMaking`과 `afterCreating` 메서드를 사용해 등록할 수 있으며, 모델을 만들거나 생성한 후 추가 작업을 수행할 수 있게 해줍니다. 이러한 콜백은 팩토리 클래스에서 `configure` 메서드를 정의하여 등록합니다. 이 메서드는 팩토리 인스턴스화 시 Laravel에서 자동으로 호출합니다:

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

특정 상태에 국한된 추가 작업을 위해, 상태 메서드 내에서도 팩토리 콜백을 등록할 수 있습니다:

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
## 팩토리를 사용하여 모델 생성하기 (Creating Models Using Factories)

<a name="instantiating-models"></a>
### 모델 인스턴스화 (Instantiating Models)

팩토리를 정의한 후, `Illuminate\Database\Eloquent\Factories\HasFactory` 트레이트에서 제공하는 정적 `factory` 메서드를 모델에서 사용하여 팩토리 인스턴스를 생성할 수 있습니다. 먼저 `make` 메서드를 통해 데이터베이스에 저장하지 않고 모델 인스턴스를 생성하는 예제를 살펴보겠습니다:

```php
use App\Models\User;

$user = User::factory()->make();
```

`count` 메서드를 사용해 여러 개의 모델 컬렉션을 생성할 수도 있습니다:

```php
$users = User::factory()->count(3)->make();
```

<a name="applying-states"></a>
#### 상태 적용하기

상태도 모델에 적용할 수 있습니다. 여러 상태 변환을 동시에 적용하려면, 상태 변환 메서드를 차례로 호출하면 됩니다:

```php
$users = User::factory()->count(5)->suspended()->make();
```

<a name="overriding-attributes"></a>
#### 속성 재정의하기

기본값 중 일부를 재정의하고 싶다면 `make` 메서드에 속성 배열을 전달하세요. 지정한 속성만 덮어쓰고 나머지는 팩토리에서 정의한 기본값이 유지됩니다:

```php
$user = User::factory()->make([
    'name' => 'Abigail Otwell',
]);
```

또는 `state` 메서드에 배열을 직접 전달해 인라인 상태 변환을 수행할 수도 있습니다:

```php
$user = User::factory()->state([
    'name' => 'Abigail Otwell',
])->make();
```

> [!NOTE]
> 팩토리를 사용해 모델을 생성할 때는 [대량 할당 보호](/docs/master/eloquent#mass-assignment)가 자동으로 해제됩니다.

<a name="persisting-models"></a>
### 모델 저장하기 (Persisting Models)

`create` 메서드는 모델 인스턴스를 생성하고 Eloquent의 `save` 메서드를 통해 데이터베이스에 영속화합니다:

```php
use App\Models\User;

// 단일 App\Models\User 인스턴스 생성...
$user = User::factory()->create();

// 세 개의 App\Models\User 인스턴스 생성...
$users = User::factory()->count(3)->create();
```

`create` 메서드에 속성 배열을 전달해 팩토리 기본 속성을 재정의할 수도 있습니다:

```php
$user = User::factory()->create([
    'name' => 'Abigail',
]);
```

<a name="sequences"></a>
### 시퀀스 (Sequences)

모델을 생성할 때 각 인스턴스마다 특정 속성 값을 교대로 변경하고 싶은 경우, 시퀀스 상태 변환을 정의하면 됩니다. 예를 들어 `admin` 컬럼 값을 생성하는 각 사용자마다 `Y`와 `N`으로 교대로 지정하고 싶을 때:

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

위 예제에서는 다섯 명은 `admin` 값이 `Y`이고, 다섯 명은 `N`인 사용자가 생성됩니다.

필요시, 시퀀스 값으로 클로저를 포함할 수도 있습니다. 클로저는 시퀀스에서 새 값을 요청할 때마다 실행됩니다:

```php
use Illuminate\Database\Eloquent\Factories\Sequence;

$users = User::factory()
    ->count(10)
    ->state(new Sequence(
        fn (Sequence $sequence) => ['role' => UserRoles::all()->random()],
    ))
    ->create();
```

시퀀스 클로저 내에서는 주입되는 시퀀스 인스턴스의 `$index`와 `$count` 속성에 접근할 수 있습니다. `$index`는 지금까지 반복한 횟수를, `$count`는 총 호출 횟수를 나타냅니다:

```php
$users = User::factory()
    ->count(10)
    ->sequence(fn (Sequence $sequence) => ['name' => 'Name '.$sequence->index])
    ->create();
```

편의상, 시퀀스는 내부적으로 `state` 메서드를 호출하는 `sequence` 메서드로도 적용할 수 있습니다. `sequence` 메서드는 클로저나 속성 배열 시퀀스를 인수로 받습니다:

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
## 팩토리 관계 (Factory Relationships)

<a name="has-many-relationships"></a>
### Has Many 관계 (Has Many Relationships)

다음으로 Laravel의 유창한 팩토리 메서드를 사용해 Eloquent 모델 관계를 구성하는 방법을 살펴보겠습니다. 예를 들어 `App\Models\User` 모델과 `App\Models\Post` 모델이 있고 `User` 모델이 `hasMany` 관계로 `Post`를 가지는 상황을 가정해 보겠습니다. `has` 메서드를 이용해 세 개의 게시물을 가진 사용자를 만들 수 있습니다. `has` 메서드에는 팩토리 인스턴스를 전달합니다:

```php
use App\Models\Post;
use App\Models\User;

$user = User::factory()
    ->has(Post::factory()->count(3))
    ->create();
```

관례에 따라 `has` 메서드에 `Post` 모델을 전달할 경우, Laravel은 `User` 모델에 `posts`라는 관계 메서드가 있어야 한다고 가정합니다. 필요에 따라 조작하려는 관계 이름을 명시적으로 지정할 수도 있습니다:

```php
$user = User::factory()
    ->has(Post::factory()->count(3), 'posts')
    ->create();
```

관련 모델의 상태도 변경할 수 있습니다. 부모 모델을 인수로 받는 클로저 기반 상태 변환도 가능합니다:

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
#### 매직 메서드 사용하기

편리하게도 Laravel은 매직 팩토리 관계 메서드를 제공하여 관계를 만들 수 있습니다. 예를 들어 다음 코드는 관계 이름이 `posts`인 것을 암묵적으로 인식하여 관련 모델을 생성합니다:

```php
$user = User::factory()
    ->hasPosts(3)
    ->create();
```

매직 메서드로 관계를 생성할 때 관련 모델의 속성을 오버라이드할 배열도 전달할 수 있습니다:

```php
$user = User::factory()
    ->hasPosts(3, [
        'published' => false,
    ])
    ->create();
```

상태 변환에 부모 모델을 인자로 담은 클로저 기반 상태도 지정할 수 있습니다:

```php
$user = User::factory()
    ->hasPosts(3, function (array $attributes, User $user) {
        return ['user_type' => $user->type];
    })
    ->create();
```

<a name="belongs-to-relationships"></a>
### Belongs To 관계 (Belongs To Relationships)

`has many` 관계를 살펴봤으니 이번에는 반대 관계를 살펴봅니다. `for` 메서드를 사용하면 팩토리가 생성하는 모델이 속하는 부모 모델을 정의할 수 있습니다. 예를 들어 한 명의 사용자에 속한 세 개의 `App\Models\Post` 모델 인스턴스를 생성하고 싶다면:

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

이미 부모 모델 인스턴스를 가지고 있다면, 이 인스턴스를 `for` 메서드에 직접 전달할 수도 있습니다:

```php
$user = User::factory()->create();

$posts = Post::factory()
    ->count(3)
    ->for($user)
    ->create();
```

<a name="belongs-to-relationships-using-magic-methods"></a>
#### 매직 메서드 사용하기

`belongs to` 관계도 매직 팩토리 관계 메서드로 간편하게 정의할 수 있습니다. 예를 들어, 세 개의 글이 `Post` 모델의 `user` 관계에 속한다고 암묵적으로 인식하게 할 수 있습니다:

```php
$posts = Post::factory()
    ->count(3)
    ->forUser([
        'name' => 'Jessica Archer',
    ])
    ->create();
```

<a name="many-to-many-relationships"></a>
### Many to Many 관계 (Many to Many Relationships)

[Has many 관계](#has-many-relationships)와 마찬가지로, "many to many" 관계 역시 `has` 메서드를 사용해 생성할 수 있습니다:

```php
use App\Models\Role;
use App\Models\User;

$user = User::factory()
    ->has(Role::factory()->count(3))
    ->create();
```

<a name="pivot-table-attributes"></a>
#### 피벗 테이블 속성 (Pivot Table Attributes)

모델 간 연결을 위한 피벗(중간) 테이블에 설정할 속성을 지정해야 하는 경우 `hasAttached` 메서드를 사용합니다. 이 메서드는 두 번째 인수로 피벗 테이블에 설정할 속성 배열을 받습니다:

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

관련 모델에 접근할 필요가 있어 상태 변경에 부모 모델 정보가 필요하면 클로저 기반 상태 변환도 가능합니다:

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

이미 부착하고자 하는 모델 인스턴스들이 있다면 이들을 `hasAttached` 메서드에 전달할 수도 있습니다. 다음 예제는 동일한 세 개 역할이 세 명 사용자 모두에 연결됩니다:

```php
$roles = Role::factory()->count(3)->create();

$user = User::factory()
    ->count(3)
    ->hasAttached($roles, ['active' => true])
    ->create();
```

<a name="many-to-many-relationships-using-magic-methods"></a>
#### 매직 메서드 사용하기

"many to many" 관계도 매직 팩토리 관계 메서드를 사용해 정의할 수 있습니다. 예를 들어 다음 예제는 관련 모델이 `User` 모델의 `roles` 관계 메서드를 통해 생성되어야 한다는 규칙을 따릅니다:

```php
$user = User::factory()
    ->hasRoles(1, [
        'name' => 'Editor'
    ])
    ->create();
```

<a name="polymorphic-relationships"></a>
### 다형 관계 (Polymorphic Relationships)

[다형 관계](/docs/master/eloquent-relationships#polymorphic-relationships)도 팩토리를 이용해 생성할 수 있습니다. 다형성 "morph many" 관계는 일반적인 "has many" 관계를 생성하듯이 만듭니다. 예를 들어 `App\Models\Post` 모델이 `App\Models\Comment` 모델과 `morphMany` 관계인 경우:

```php
use App\Models\Post;

$post = Post::factory()->hasComments(3)->create();
```

<a name="morph-to-relationships"></a>
#### Morph To 관계

`morphTo` 관계는 매직 메서드를 쓰지 않고, `for` 메서드로 관계 명칭을 명시적으로 지정해야 합니다. 예를 들어 `Comment` 모델에 `commentable` 메서드가 `morphTo` 관계를 정의할 때, 세 개 댓글을 한 게시물에 속하게 하려면 다음과 같이 작성합니다:

```php
$comments = Comment::factory()->count(3)->for(
    Post::factory(), 'commentable'
)->create();
```

<a name="polymorphic-many-to-many-relationships"></a>
#### 다형성 Many to Many 관계

다형성 "many to many" (`morphToMany` / `morphedByMany`) 관계도 비다형성 관계 만들 듯 `hasAttached` 메서드 등으로 생성 가능합니다:

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

물론 매직 `has` 메서드를 사용해 다형성 "many to many" 관계를 생성할 수도 있습니다:

```php
$videos = Video::factory()
    ->hasTags(3, ['public' => true])
    ->create();
```

<a name="defining-relationships-within-factories"></a>
### 팩토리 내에서 관계 정의하기 (Defining Relationships Within Factories)

모델 팩토리 내에서 관계를 정의할 때는 보통 관계의 외래 키에 새로운 팩토리 인스턴스를 할당합니다. 이는 보통 `belongsTo` 나 `morphTo`와 같은 '역' 관계에 적용합니다. 예를 들어 포스트를 생성할 때 새 사용자를 함께 생성하려면 다음과 같이 정의합니다:

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

만약 관계 컬럼이 팩토리 정의에 의존하는 경우엔 클로저를 속성에 할당할 수 있습니다. 이 클로저는 팩토리가 평가한 속성 배열을 받습니다:

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
### 관계에 기존 모델 재사용하기 (Recycling an Existing Model for Relationships)

공통 관계를 가진 모델들이 있다면 `recycle` 메서드를 사용해 관련 모델을 팩토리가 생성하는 관계들에서 단일 인스턴스로 재사용할 수 있습니다.

예를 들어 `Airline`, `Flight`, `Ticket` 모델이 있고, 티켓은 항공사와 비행기에 속하며, 비행기도 항공사에 속하는 관계라면 티켓을 생성할 때 티켓과 비행기 모두에 같은 항공사를 할당하기 위해 `recycle` 메서드에 항공사 인스턴스를 넘깁니다:

```php
Ticket::factory()
    ->recycle(Airline::factory()->create())
    ->create();
```

`recycle` 메서드는 특히 사용자 또는 팀에 속하는 모델들을 다룰 때 유용합니다.

또한, `recycle` 메서드는 기존 모델 컬렉션도 받습니다. 컬렉션이 제공되면, 팩토리가 해당 타입의 모델이 필요할 때 컬렉션에서 임의의 모델 하나를 선택해 사용합니다:

```php
Ticket::factory()
    ->recycle($airlines)
    ->create();
```