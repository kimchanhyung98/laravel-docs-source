# Eloquent: 팩토리 (Eloquent: Factories)

- [소개](#introduction)
- [모델 팩토리 정의하기](#defining-model-factories)
    - [팩토리 생성하기](#generating-factories)
    - [팩토리 상태(state)](#factory-states)
    - [팩토리 콜백(callback)](#factory-callbacks)
- [팩토리를 사용한 모델 생성](#creating-models-using-factories)
    - [모델 인스턴스화](#instantiating-models)
    - [모델 저장](#persisting-models)
    - [시퀀스](#sequences)
- [팩토리의 연관관계](#factory-relationships)
    - [Has Many 연관관계](#has-many-relationships)
    - [Belongs To 연관관계](#belongs-to-relationships)
    - [Many to Many 연관관계](#many-to-many-relationships)
    - [폴리모픽 연관관계](#polymorphic-relationships)
    - [팩토리 내에서 연관관계 정의](#defining-relationships-within-factories)
    - [연관관계에서 기존 모델 재사용](#recycling-an-existing-model-for-relationships)

<a name="introduction"></a>
## 소개 (Introduction)

애플리케이션을 테스트하거나 데이터베이스를 시딩(초기 데이터 입력)할 때, 데이터베이스에 몇 개의 레코드를 삽입해야 할 수 있습니다. 이때 각 컬럼의 값을 직접 지정하는 대신, Laravel은 [Eloquent 모델](/docs/12.x/eloquent)마다 기본 속성(attribute)을 지정할 수 있도록 모델 팩토리(model factory) 기능을 제공합니다.

팩토리를 작성하는 예제를 보려면 애플리케이션의 `database/factories/UserFactory.php` 파일을 참고하세요. 이 팩토리는 모든 새로운 Laravel 애플리케이션에 포함되어 있으며, 다음과 같은 팩토리 정의를 갖습니다:

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

보시다시피, 가장 기본적인 형태의 팩토리는 Laravel의 기본 팩토리 클래스를 확장하고 `definition` 메서드를 정의하는 클래스입니다. `definition` 메서드는 팩토리를 사용해 모델을 생성할 때 적용할 기본 속성값 집합을 반환합니다.

팩토리에서는 `fake` 헬퍼를 통해 [Faker](https://github.com/FakerPHP/Faker) PHP 라이브러리를 사용할 수 있어, 다양한 유형의 랜덤 데이터를 테스트와 시딩에 편리하게 생성할 수 있습니다.

> [!NOTE]
> 애플리케이션의 Faker 언어(locale)를 변경하려면 `config/app.php` 설정 파일의 `faker_locale` 옵션을 업데이트하면 됩니다.

<a name="defining-model-factories"></a>
## 모델 팩토리 정의하기 (Defining Model Factories)

<a name="generating-factories"></a>
### 팩토리 생성하기 (Generating Factories)

팩토리를 생성하려면 `make:factory` [Artisan 명령어](/docs/12.x/artisan)를 실행하세요:

```shell
php artisan make:factory PostFactory
```

새로 생성된 팩토리 클래스는 `database/factories` 디렉터리에 생성됩니다.

<a name="factory-and-model-discovery-conventions"></a>
#### 모델과 팩토리의 탐색 규칙

팩토리를 정의한 뒤에는, `Illuminate\Database\Eloquent\Factories\HasFactory` 트레이트가 모델에 제공하는 정적 `factory` 메서드를 사용하여 해당 모델의 팩토리 인스턴스를 생성할 수 있습니다.

`HasFactory` 트레이트의 `factory` 메서드는 규칙에 따라 트레이트가 지정된 모델에 맞는 팩토리를 자동으로 찾습니다. 구체적으로, 이 메서드는 `Database\Factories` 네임스페이스 아래, 모델 이름과 동일하며 `Factory`로 끝나는 클래스명을 탐색합니다. 만약 이러한 규칙이 여러분의 애플리케이션이나 팩토리에 맞지 않다면, 모델에서 `newFactory` 메서드를 오버라이드하여 직접 팩토리 인스턴스를 반환하면 됩니다:

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

그리고, 해당 팩토리에서는 `model` 속성을 정의해야 합니다:

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
### 팩토리 상태(state) (Factory States)

상태 변환 메서드를 사용하면, 팩토리 내에서 여러 속성 값을 각각 조합하여 수정할 수 있는 별도의 상태를 정의할 수 있습니다. 예를 들어, `Database\Factories\UserFactory` 팩토리에서 특정 속성값을 조정하는 `suspended` 상태 메서드를 만들 수 있습니다.

상태 변환 메서드는 일반적으로 Laravel의 기본 팩토리 클래스가 제공하는 `state` 메서드를 호출합니다. `state` 메서드는 클로저를 받아, 해당 팩토리의 현재 속성 배열을 인자로 전달하고, 수정하고자 하는 속성만을 배열로 반환합니다:

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
#### "소프트 삭제된(Trashed)" 상태

만약 여러분의 Eloquent 모델이 [소프트 삭제](/docs/12.x/eloquent#soft-deleting)를 지원한다면, 내장된 `trashed` 상태 메서드를 호출하여 생성된 모델이 "소프트 삭제"된 상태가 되도록 지정할 수 있습니다. `trashed` 상태는 모든 팩토리에 자동으로 제공되므로 직접 정의하지 않아도 됩니다:

```php
use App\Models\User;

$user = User::factory()->trashed()->create();
```

<a name="factory-callbacks"></a>
### 팩토리 콜백(callback) (Factory Callbacks)

팩토리 콜백은 `afterMaking`과 `afterCreating` 메서드를 사용하여 등록할 수 있으며, 모델을 생성(메모리 상에), 혹은 저장(생성 후 DB에 저장)한 뒤 추가 작업을 수행할 수 있게 해줍니다. 이 콜백들은 팩토리 클래스에 `configure` 메서드를 정의하여 등록해야 하며, Laravel이 팩토리를 초기화할 때 자동으로 호출됩니다:

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

또한, 특정 상태 메서드 내에서도 팩토리 콜백을 등록할 수 있습니다. 이를 통해 특정 상태에서만 추가 동작이 필요할 때 유용하게 활용할 수 있습니다:

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

팩토리를 정의한 이후에는, `Illuminate\Database\Eloquent\Factories\HasFactory` 트레이트가 제공하는 정적 `factory` 메서드를 사용해 해당 모델의 팩토리 인스턴스를 만들 수 있습니다. 다음은 여러 가지 모델 생성을 예시로 보여줍니다.

먼저, `make` 메서드를 사용해 데이터베이스에는 저장하지 않고 모델을 생성하는 방법입니다:

```php
use App\Models\User;

$user = User::factory()->make();
```

`count` 메서드를 활용해 여러 모델의 컬렉션을 만들 수도 있습니다:

```php
$users = User::factory()->count(3)->make();
```

<a name="applying-states"></a>
#### 상태(state) 적용하기

[상태](#factory-states)를 모델에 적용할 수도 있습니다. 여러 상태를 동시에 적용하려면, 상태 변환 메서드들을 체이닝해서 호출하면 됩니다:

```php
$users = User::factory()->count(5)->suspended()->make();
```

<a name="overriding-attributes"></a>
#### 속성(attribute) 오버라이드

팩토리의 기본 속성값 일부를 변경하고 싶다면, `make` 메서드에 값이 변경된 속성 배열을 전달할 수 있습니다. 이렇게 전달된 속성만 오버라이드되며, 나머지 속성값은 팩토리에서 정의된 기본값이 유지됩니다:

```php
$user = User::factory()->make([
    'name' => 'Abigail Otwell',
]);
```

또는, `state` 메서드를 팩토리 인스턴스에 직접 호출하여 인라인으로 상태 변환을 수행해도 됩니다:

```php
$user = User::factory()->state([
    'name' => 'Abigail Otwell',
])->make();
```

> [!NOTE]
> 팩토리로 생성된 모델은 [일괄 할당 보호(mass assignment protection)](/docs/12.x/eloquent#mass-assignment)이 자동으로 비활성화됩니다.

<a name="persisting-models"></a>
### 모델 저장 (Persisting Models)

`create` 메서드는 모델 인스턴스를 생성한 후, Eloquent의 `save` 메서드를 사용해 데이터베이스에 저장합니다:

```php
use App\Models\User;

// 단일 App\Models\User 인스턴스 생성 및 저장
$user = User::factory()->create();

// 세 개의 App\Models\User 인스턴스 생성 및 저장
$users = User::factory()->count(3)->create();
```

`create` 메서드에 속성값 배열을 전달하면, 기본값 대신 지정한 값으로 속성이 오버라이드됩니다:

```php
$user = User::factory()->create([
    'name' => 'Abigail',
]);
```

<a name="sequences"></a>
### 시퀀스 (Sequences)

여러 모델을 생성할 때 각 모델의 속성값을 번갈아가며 지정하고 싶을 수 있습니다. 이럴 때 상태 변환을 시퀀스로 정의해서 생성할 수 있습니다. 예를 들어, 생성되는 사용자별로 `admin` 컬럼 값을 번갈아가며 `Y`와 `N`으로 주고 싶을 때 아래와 같이 할 수 있습니다:

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

이 예제에서는 10명의 사용자가 생성되고, 이 중 5명은 `admin` 값이 `Y`, 나머지 5명은 `N`이 됩니다.

필요하다면, 시퀀스 값으로 클로저를 사용할 수도 있습니다. 이 클로저는 시퀀스마다 새로운 값이 필요할 때마다 호출됩니다:

```php
use Illuminate\Database\Eloquent\Factories\Sequence;

$users = User::factory()
    ->count(10)
    ->state(new Sequence(
        fn (Sequence $sequence) => ['role' => UserRoles::all()->random()],
    ))
    ->create();
```

시퀀스 클로저 내부에서는 인자로 전달된 시퀀스 인스턴스의 `$index` 속성을 통해, 현재 시퀀스가 몇 번째 반복인지 알 수 있습니다:

```php
$users = User::factory()
    ->count(10)
    ->state(new Sequence(
        fn (Sequence $sequence) => ['name' => 'Name '.$sequence->index],
    ))
    ->create();
```

편의를 위해, `sequence` 메서드를 사용하여도 위 방식과 동일하게 동작합니다. `sequence`는 내부적으로 `state` 메서드를 호출하며, 클로저나 배열 형태의 속성 시퀀스를 받을 수 있습니다:

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
## 팩토리의 연관관계 (Factory Relationships)

<a name="has-many-relationships"></a>
### Has Many 연관관계

다음으로, Laravel의 플루언트한 팩토리 메서드를 이용해 Eloquent 모델 간의 연관관계를 빌드하는 방법을 살펴보겠습니다. 예를 들어, 애플리케이션에 `App\Models\User` 모델과 `App\Models\Post` 모델이 있고, `User` 모델이 `Post` 모델과 `hasMany` 연관관계를 가지고 있다고 가정하겠습니다. 이때, `has` 메서드를 사용하여 포스트 3개를 가진 사용자를 아래처럼 만들 수 있습니다. `has` 메서드에는 팩토리 인스턴스를 전달합니다:

```php
use App\Models\Post;
use App\Models\User;

$user = User::factory()
    ->has(Post::factory()->count(3))
    ->create();
```

규칙상, `has` 메서드에 `Post` 모델을 전달하면 Laravel은 `User` 모델에 `posts`라는 연관관계 메서드가 있다고 간주합니다. 필요하다면, 직접 조작할 연관관계의 이름을 두 번째 인자로 명시할 수도 있습니다:

```php
$user = User::factory()
    ->has(Post::factory()->count(3), 'posts')
    ->create();
```

물론, 연관 모델에도 상태 변환을 적용할 수 있습니다. 만약 부모 모델에 접근해야 하는 상태 변환이 필요하다면, 클로저 형태로 state를 전달하면 됩니다:

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
#### 매직 메서드를 이용한 생성

더 편리하게 사용하기 위해, Laravel이 제공하는 매직 팩토리 연관관계 메서드를 활용할 수 있습니다. 아래 예시처럼, Laravel은 `User` 모델에서 연관관계 메서드 이름(`posts`)을 기준으로 자동 판단합니다:

```php
$user = User::factory()
    ->hasPosts(3)
    ->create();
```

매직 메서드를 사용할 때, 연관 모델의 속성값을 오버라이드하고 싶다면 배열로 전달하면 됩니다:

```php
$user = User::factory()
    ->hasPosts(3, [
        'published' => false,
    ])
    ->create();
```

또한, 부모 모델에 접근해야 할 때는 클로저 형태로도 전달 가능합니다:

```php
$user = User::factory()
    ->hasPosts(3, function (array $attributes, User $user) {
        return ['user_type' => $user->type];
    })
    ->create();
```

<a name="belongs-to-relationships"></a>
### Belongs To 연관관계

이제 팩토리를 사용해 "has many" 연관관계를 구성하는 방법을 살펴봤으니, 이번에는 그 반대 방향의 "belongs to" 연관관계를 알아보겠습니다. `for` 메서드는 팩토리가 생성하는 모델 인스턴스가 어떤 부모 모델에 속하는지 정의할 때 사용합니다. 예를 들어, 아래처럼 `App\Models\Post` 모델 3개가 하나의 사용자에 속하도록 할 수 있습니다:

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

이미 생성된 부모 모델 인스턴스가 있다면, 그 인스턴스를 `for` 메서드에 직접 전달할 수도 있습니다:

```php
$user = User::factory()->create();

$posts = Post::factory()
    ->count(3)
    ->for($user)
    ->create();
```

<a name="belongs-to-relationships-using-magic-methods"></a>
#### 매직 메서드를 이용한 생성

편의를 위해 매직 팩토리 연관관계 메서드를 사용해 "belongs to" 연관관계를 정의할 수 있습니다. 아래 예시는, 생성되는 3개의 포스트가 `Post` 모델의 `user` 연관관계에 속해야 함을 자동으로 판단합니다:

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

[Has many 연관관계](#has-many-relationships)와 마찬가지로, "many to many" 연관관계도 `has` 메서드를 사용해 생성할 수 있습니다:

```php
use App\Models\Role;
use App\Models\User;

$user = User::factory()
    ->has(Role::factory()->count(3))
    ->create();
```

<a name="pivot-table-attributes"></a>
#### 중간 테이블(피벗 테이블) 속성

모델을 연결하는 피벗(중간) 테이블에 설정할 속성이 필요하다면, `hasAttached` 메서드를 사용할 수 있습니다. 이 메서드는 두 번째 인자로 피벗 테이블에 지정할 속성명-값 배열을 받습니다:

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

연관 모델에 접근하여 상태를 변환해야 한다면, 클로저를 state 변환에 사용할 수도 있습니다:

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

이미 생성된 모델 인스턴스를 `hasAttached`에 전달하면, 각 사용자가 동일한 역할(role)을 공유하게 할 수도 있습니다. 아래 예제는 같은 3개의 역할을 3명의 사용자에게 모두 연결합니다:

```php
$roles = Role::factory()->count(3)->create();

$users = User::factory()
    ->count(3)
    ->hasAttached($roles, ['active' => true])
    ->create();
```

<a name="many-to-many-relationships-using-magic-methods"></a>
#### 매직 메서드를 이용한 생성

편의상 매직 팩토리 연관관계 메서드로 many to many 연관관계를 정의할 수 있습니다. 아래 예시는, 관련 모델이 `User` 모델의 `roles` 연관관계 메서드를 통해 생성되어야 함을 자동으로 판별합니다:

```php
$user = User::factory()
    ->hasRoles(1, [
        'name' => 'Editor'
    ])
    ->create();
```

<a name="polymorphic-relationships"></a>
### 폴리모픽 연관관계 (Polymorphic Relationships)

[폴리모픽 연관관계](/docs/12.x/eloquent-relationships#polymorphic-relationships)도 팩토리를 통해 생성할 수 있습니다. 폴리모픽 "morph many" 연관관계는 일반적인 "has many" 연관관계와 동일하게 생성할 수 있습니다. 예를 들어, `App\Models\Post` 모델이 `App\Models\Comment` 모델과 `morphMany` 연관관계를 가진다고 하면:

```php
use App\Models\Post;

$post = Post::factory()->hasComments(3)->create();
```

<a name="morph-to-relationships"></a>
#### Morph To 연관관계

매직 메서드는 `morphTo` 연관관계에서는 사용할 수 없습니다. 대신, `for` 메서드를 직접 사용하고, 연관관계 이름을 명시해야 합니다. 예를 들어, `Comment` 모델이 `commentable`이라는 `morphTo` 연관관계를 가진다면, 아래와 같이 작성할 수 있습니다:

```php
$comments = Comment::factory()->count(3)->for(
    Post::factory(), 'commentable'
)->create();
```

<a name="polymorphic-many-to-many-relationships"></a>
#### 폴리모픽 Many to Many 연관관계

폴리모픽 "many to many"(`morphToMany` / `morphedByMany`) 연관관계도 일반 "many to many" 연관관계와 동일하게 생성 가능합니다:

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

물론, 매직 `has` 메서드를 사용해서도 폴리모픽 many to many 연관관계를 생성할 수 있습니다:

```php
$video = Video::factory()
    ->hasTags(3, ['public' => true])
    ->create();
```

<a name="defining-relationships-within-factories"></a>
### 팩토리 내에서 연관관계 정의 (Defining Relationships Within Factories)

모델 팩토리 안에서 연관관계를 정의하려면, 보통 외래키(foreign key)에 새 팩토리 인스턴스를 할당하면 됩니다. 이는 주로 `belongsTo` 및 `morphTo`와 같은 "역방향" 연관관계에서 활용합니다. 예를 들어, 포스트를 생성할 때 새로운 사용자를 함께 생성하려면 다음과 같이 작성할 수 있습니다:

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

만약 연관관계 컬럼값이 팩토리를 정의한 팩토리의 다른 속성에 따라 달라져야 한다면, 속성에 클로저를 직접 할당할 수 있습니다. 이 클로저는 평가(evaluate)된 속성 배열을 전달받습니다:

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
### 연관관계에서 기존 모델 재사용 (Recycling an Existing Model for Relationships)

하나의 공통된 연관 모델을 여러 모델이 공유해야 한다면, 팩토리의 `recycle` 메서드를 사용해서 연관관계에 같은 모델 인스턴스가 반복적으로 할당되도록 할 수 있습니다.

예를 들어, `Airline`, `Flight`, `Ticket` 모델의 경우, 티켓은 항공사와 비행편에 속하고, 비행편 역시 항공사에 속한다고 가정해봅시다. 이때 티켓을 만들면서, 티켓과 비행편에 모두 똑같은 항공사를 지정하고 싶다면 아래처럼 `recycle` 메서드를 사용할 수 있습니다:

```php
Ticket::factory()
    ->recycle(Airline::factory()->create())
    ->create();
```

여러 모델이 하나의 공통된 사용자나 팀에 속할 때에도 이 메서드는 특히 유용합니다.

`recycle` 메서드에는 모델 컬렉션을 전달할 수도 있습니다. 이 경우, 팩토리가 해당 모델 유형을 필요로 할 때마다 컬렉션에서 랜덤으로 하나를 선택합니다:

```php
Ticket::factory()
    ->recycle($airlines)
    ->create();
```
