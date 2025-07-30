# Eloquent: 팩토리 (Factories)

- [소개](#introduction)
- [모델 팩토리 정의하기](#defining-model-factories)
    - [팩토리 생성하기](#generating-factories)
    - [팩토리 상태](#factory-states)
    - [팩토리 콜백](#factory-callbacks)
- [팩토리로 모델 만들기](#creating-models-using-factories)
    - [모델 인스턴스 생성하기](#instantiating-models)
    - [모델 저장하기](#persisting-models)
    - [시퀀스](#sequences)
- [팩토리 관계 설정](#factory-relationships)
    - [Has Many 관계](#has-many-relationships)
    - [Belongs To 관계](#belongs-to-relationships)
    - [Many to Many 관계](#many-to-many-relationships)
    - [다형성 관계](#polymorphic-relationships)
    - [팩토리 내에서 관계 정의하기](#defining-relationships-within-factories)
    - [관계에 기존 모델 재활용하기](#recycling-an-existing-model-for-relationships)

<a name="introduction"></a>
## 소개 (Introduction)

애플리케이션 테스트나 데이터베이스 시딩 시 몇 개의 레코드를 데이터베이스에 삽입할 필요가 있습니다. 각 컬럼의 값을 일일이 지정하는 대신, Laravel은 모델 팩토리를 사용하여 각 [Eloquent 모델](/docs/11.x/eloquent)에 대한 기본 속성 집합을 정의할 수 있도록 지원합니다.

팩토리 작성 예제를 보려면 애플리케이션 내 `database/factories/UserFactory.php` 파일을 확인하세요. 이 팩토리는 모든 새로운 Laravel 애플리케이션에 기본 포함되어 있으며 다음과 같은 팩토리 정의를 담고 있습니다:

```
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

가장 기본적인 형태로, 팩토리는 Laravel의 기본 팩토리 클래스를 상속하는 클래스이고, `definition` 메서드를 정의합니다. `definition` 메서드는 팩토리로 모델을 생성할 때 적용할 기본 속성 값 집합을 반환합니다.

`fake` 헬퍼를 통해 팩토리는 다양한 종류의 랜덤 데이터를 편리하게 생성할 수 있는 [Faker](https://github.com/FakerPHP/Faker) PHP 라이브러리에 접근할 수 있습니다.

> [!NOTE]  
> `config/app.php` 설정 파일 내 `faker_locale` 옵션을 변경하여 Faker의 로케일(locale)을 지정할 수 있습니다.

<a name="defining-model-factories"></a>
## 모델 팩토리 정의하기 (Defining Model Factories)

<a name="generating-factories"></a>
### 팩토리 생성하기 (Generating Factories)

팩토리를 생성하려면 `make:factory` [Artisan 명령어](/docs/11.x/artisan)를 실행하세요:

```shell
php artisan make:factory PostFactory
```

새 팩토리 클래스는 `database/factories` 디렉토리에 생성됩니다.

<a name="factory-and-model-discovery-conventions"></a>
#### 모델과 팩토리 탐색 규칙 (Model and Factory Discovery Conventions)

팩토리를 정의한 후에는 `Illuminate\Database\Eloquent\Factories\HasFactory` 트레이트에서 제공하는 정적 `factory` 메서드를 통해 해당 모델의 팩토리 인스턴스를 생성할 수 있습니다.

`HasFactory` 트레이트의 `factory` 메서드는 지정된 모델에 알맞은 팩토리를 자동으로 찾아줍니다. 구체적으로, 이 메서드는 `Database\Factories` 네임스페이스 내에 모델 이름과 일치하며 `Factory`로 끝나는 클래스명을 가진 팩토리를 찾습니다. 만약 이 규칙이 애플리케이션이나 팩토리에 맞지 않는다면, 모델에 `newFactory` 메서드를 오버라이드하여 직접 해당 팩토리 인스턴스를 반환하도록 구현할 수 있습니다:

```
use Database\Factories\Administration\FlightFactory;

/**
 * Create a new factory instance for the model.
 */
protected static function newFactory()
{
    return FlightFactory::new();
}
```

그리고 해당 팩토리 클래스에서는 `model` 속성을 정의합니다:

```
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

상태 조작 메서드는 모델 팩토리의 기본 속성값에 개별적인 변형을 여러 조합으로 적용할 수 있게 해줍니다. 예를 들어 `Database\Factories\UserFactory`에 `suspended` 상태 메서드를 구현해 기본 속성 값 중 하나를 변경하도록 할 수 있습니다.

상태 변형 메서드는 보통 Laravel의 기본 팩토리 클래스가 제공하는 `state` 메서드를 호출합니다. `state` 메서드는 팩토리의 속성 배열을 인수로 받는 클로저를 받아, 변경할 속성 배열을 반환해야 합니다:

```
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

만약 Eloquent 모델이 [소프트 삭제(soft deleted)](/docs/11.x/eloquent#soft-deleting)를 지원한다면, 팩토리에서 기본 제공하는 `trashed` 상태 메서드를 호출하여 생성 모델이 이미 소프트 삭제된 상태임을 나타낼 수 있습니다. `trashed` 상태는 모든 팩토리에 자동으로 제공되므로 별도의 정의가 필요 없습니다:

```
use App\Models\User;

$user = User::factory()->trashed()->create();
```

<a name="factory-callbacks"></a>
### 팩토리 콜백 (Factory Callbacks)

팩토리 콜백은 `afterMaking`과 `afterCreating` 메서드를 사용해 등록하며, 모델 생성 전후에 추가 작업을 수행할 수 있습니다. 팩토리 클래스에 `configure` 메서드를 정의해 콜백을 등록하는 방식이며, 이 메서드는 팩토리가 인스턴스화될 때 Laravel이 자동으로 호출합니다:

```
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

또한 특정 상태에 따른 추가 작업이 필요할 때 상태 메서드 안에서 콜백을 등록할 수도 있습니다:

```
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
## 팩토리로 모델 만들기 (Creating Models Using Factories)

<a name="instantiating-models"></a>
### 모델 인스턴스 생성하기 (Instantiating Models)

팩토리를 정의한 후, `Illuminate\Database\Eloquent\Factories\HasFactory` 트레이트가 제공하는 정적 `factory` 메서드를 사용하여 해당 모델의 팩토리 인스턴스를 생성할 수 있습니다. 몇 가지 예제로 살펴보겠습니다.

먼저, `make` 메서드를 사용해 데이터베이스에 저장하지 않고 모델 인스턴스만 생성할 수 있습니다:

```
use App\Models\User;

$user = User::factory()->make();
```

`count` 메서드로 여러 개의 모델 인스턴스를 컬렉션 형태로 만들 수 있습니다:

```
$users = User::factory()->count(3)->make();
```

<a name="applying-states"></a>
#### 상태 적용하기

모델에 [정의된 상태들](#factory-states)을 적용할 수도 있습니다. 여러 상태 변형을 한번에 적용하려면, 상태 변형 메서드를 연속해서 호출하면 됩니다:

```
$users = User::factory()->count(5)->suspended()->make();
```

<a name="overriding-attributes"></a>
#### 속성 덮어쓰기

기본값 일부를 변경하고 싶다면, `make` 메서드에 덮어쓸 속성 배열을 전달하세요. 지정한 속성만 변경되고, 나머지는 팩토리가 지정한 기본값으로 유지됩니다:

```
$user = User::factory()->make([
    'name' => 'Abigail Otwell',
]);
```

또는 팩토리 인스턴스에 직접 `state` 메서드를 호출해 인라인으로 상태 변형을 수행할 수도 있습니다:

```
$user = User::factory()->state([
    'name' => 'Abigail Otwell',
])->make();
```

> [!NOTE]  
> 팩토리를 사용할 때는 [대량 할당 보호](/docs/11.x/eloquent#mass-assignment)가 자동으로 비활성화됩니다.

<a name="persisting-models"></a>
### 모델 저장하기 (Persisting Models)

`create` 메서드는 모델 인스턴스를 생성하고 Eloquent의 `save` 메서드를 사용해 데이터베이스에 저장합니다:

```
use App\Models\User;

// 단일 User 모델 생성 및 저장...
$user = User::factory()->create();

// 세 개의 User 모델 생성 및 저장...
$users = User::factory()->count(3)->create();
```

`create` 메서드에 속성 배열을 전달해 기본 속성 값을 덮어쓸 수도 있습니다:

```
$user = User::factory()->create([
    'name' => 'Abigail',
]);
```

<a name="sequences"></a>
### 시퀀스 (Sequences)

각 생성 모델에 대해 지정한 속성 값을 번갈아 적용하고 싶을 때 시퀀스로 상태 변형을 정의할 수 있습니다. 예를 들어, 사용자 생성 시 `admin` 컬럼 값을 `Y`와 `N`으로 번갈아 지정하고 싶다면:

```
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

이 경우, 10명의 사용자 중 5명은 `admin` 값이 `Y`, 나머지 5명은 `N`으로 생성됩니다.

필요하다면 시퀀스 값으로 클로저를 포함할 수도 있는데, 시퀀스가 새 값을 필요로 할 때마다 클로저가 호출됩니다:

```
use Illuminate\Database\Eloquent\Factories\Sequence;

$users = User::factory()
    ->count(10)
    ->state(new Sequence(
        fn (Sequence $sequence) => ['role' => UserRoles::all()->random()],
    ))
    ->create();
```

시퀀스 클로저에는 `$index`와 `$count` 속성이 주입된 `Sequence` 인스턴스를 통해 접근할 수 있습니다. `$index`는 현재 시퀀스 반복 횟수, `$count`는 시퀀스가 호출될 총 횟수를 나타냅니다:

```
$users = User::factory()
    ->count(10)
    ->sequence(fn (Sequence $sequence) => ['name' => 'Name '.$sequence->index])
    ->create();
```

편리하게도 시퀀스는 내부적으로 `state` 메서드를 호출하는 `sequence` 메서드를 통해서도 지정할 수 있습니다. 이 메서드는 클로저나 시퀀스화된 속성 배열을 인자로 받습니다:

```
$users = User::factory()
    ->count(2)
    ->sequence(
        ['name' => 'First User'],
        ['name' => 'Second User'],
    )
    ->create();
```

<a name="factory-relationships"></a>
## 팩토리 관계 설정 (Factory Relationships)

<a name="has-many-relationships"></a>
### Has Many 관계

Laravel 팩토리의 플루언트 메서드를 사용하여 Eloquent 모델 관계를 구성해보겠습니다. 예를 들어, `App\Models\User` 모델과 `App\Models\Post` 모델이 있으며, `User` 모델이 `hasMany` 관계로 `Post` 모델과 연결되어 있다고 가정합니다. `has` 메서드를 이용해 게시물이 3개인 사용자를 생성할 수 있습니다. `has` 메서드는 팩토리 인스턴스를 인수로 받습니다:

```
use App\Models\Post;
use App\Models\User;

$user = User::factory()
    ->has(Post::factory()->count(3))
    ->create();
```

기본적으로 `has` 메서드에 `Post` 모델을 전달하면, Laravel은 `User` 모델에 `posts`라는 관계 메서드가 존재한다고 가정합니다. 필요하다면 조작할 관계 이름을 명시적으로 지정할 수도 있습니다:

```
$user = User::factory()
    ->has(Post::factory()->count(3), 'posts')
    ->create();
```

관련 모델에 상태 변형을 적용할 수도 있고, 부모 모델에 접근해야 하는 상태 변형이라면 클로저 기반 상태 변형을 넘길 수 있습니다:

```
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

편의를 위해 Laravel의 매직 팩토리 관계 메서드를 사용할 수 있습니다. 예를 들어, 다음 코드는 `User` 모델의 `posts` 관계 메서드를 통해 관련된 모델을 생성합니다:

```
$user = User::factory()
    ->hasPosts(3)
    ->create();
```

매직 메서드 사용 시, 관련 모델에 덮어쓸 속성 배열도 전달할 수 있습니다:

```
$user = User::factory()
    ->hasPosts(3, [
        'published' => false,
    ])
    ->create();
```

부모 모델에 접근해야 하는 상태 변형이라면 클로저를 제공할 수도 있습니다:

```
$user = User::factory()
    ->hasPosts(3, function (array $attributes, User $user) {
        return ['user_type' => $user->type];
    })
    ->create();
```

<a name="belongs-to-relationships"></a>
### Belongs To 관계

이제 "has many" 관계와 반대되는 관계를 살펴보겠습니다. `for` 메서드는 팩토리로 생성하는 모델이 속한 부모 모델을 정의할 때 사용합니다. 예를 들어, 하나의 사용자가 속한 세 개의 `App\Models\Post` 인스턴스를 만들 수 있습니다:

```
use App\Models\Post;
use App\Models\User;

$posts = Post::factory()
    ->count(3)
    ->for(User::factory()->state([
        'name' => 'Jessica Archer',
    ]))
    ->create();
```

이미 생성된 부모 모델이 있다면 이를 `for` 메서드에 전달할 수도 있습니다:

```
$user = User::factory()->create();

$posts = Post::factory()
    ->count(3)
    ->for($user)
    ->create();
```

<a name="belongs-to-relationships-using-magic-methods"></a>
#### 매직 메서드 사용하기

편의를 위해 "belongs to" 관계도 매직 팩토리 관계 메서드를 통해 지정할 수 있습니다. 예를 들어, 다음 코드는 `Post` 모델의 `user` 관계에 소속되는 세 개의 게시물을 생성합니다:

```
$posts = Post::factory()
    ->count(3)
    ->forUser([
        'name' => 'Jessica Archer',
    ])
    ->create();
```

<a name="many-to-many-relationships"></a>
### Many to Many 관계

[Has many 관계](#has-many-relationships)처럼 "many to many" 관계도 `has` 메서드로 생성할 수 있습니다:

```
use App\Models\Role;
use App\Models\User;

$user = User::factory()
    ->has(Role::factory()->count(3))
    ->create();
```

<a name="pivot-table-attributes"></a>
#### 피벗 테이블 속성

모델을 연결하는 피벗(중간) 테이블에 값을 지정해야 할 경우 `hasAttached` 메서드를 사용하세요. 이 메서드는 두 번째 인수로 피벗 테이블의 속성 이름과 값을 배열로 받습니다:

```
use App\Models\Role;
use App\Models\User;

$user = User::factory()
    ->hasAttached(
        Role::factory()->count(3),
        ['active' => true]
    )
    ->create();
```

상태 변형이 관련 모델에 접근해야 할 때는 클로저 기반 상태 변형을 전달할 수 있습니다:

```
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

이미 존재하는 모델 인스턴스를 관련 모델로 연결하려면, 해당 모델 인스턴스들을 `hasAttached` 메서드에 전달할 수 있습니다. 아래 예제에서는 동일한 세 개의 역할이 세 명의 사용자 모두에게 연결됩니다:

```
$roles = Role::factory()->count(3)->create();

$user = User::factory()
    ->count(3)
    ->hasAttached($roles, ['active' => true])
    ->create();
```

<a name="many-to-many-relationships-using-magic-methods"></a>
#### 매직 메서드 사용하기

"Many to many" 관계도 매직 팩토리 관계 메서드를 사용할 수 있습니다. 예를 들어, 다음 코드는 `User` 모델의 `roles` 관계 메서드를 사용해 관련 모델을 생성합니다:

```
$user = User::factory()
    ->hasRoles(1, [
        'name' => 'Editor'
    ])
    ->create();
```

<a name="polymorphic-relationships"></a>
### 다형성 관계 (Polymorphic Relationships)

[다형성 관계](/docs/11.x/eloquent-relationships#polymorphic-relationships)도 팩토리로 생성할 수 있습니다. 다형성 "morph many" 관계는 일반적인 "has many" 관계 생성 방법과 동일합니다. 예를 들어, `App\Models\Post` 모델이 `App\Models\Comment` 모델과 `morphMany` 관계를 갖는 경우:

```
use App\Models\Post;

$post = Post::factory()->hasComments(3)->create();
```

<a name="morph-to-relationships"></a>
#### Morph To 관계

`morphTo` 관계 생성 시에는 매직 메서드를 사용할 수 없으며, 대신 `for` 메서드를 직접 호출하고 관계 이름을 명시해야 합니다. 예를 들어, `Comment` 모델에 `commentable`이라는 `morphTo` 관계가 있다면, 세 개의 댓글이 단일 게시물에 속하도록 아래와 같이 작성합니다:

```
$comments = Comment::factory()->count(3)->for(
    Post::factory(), 'commentable'
)->create();
```

<a name="polymorphic-many-to-many-relationships"></a>
#### 다형성 Many to Many 관계

다형성 "many to many" 관계(`morphToMany` / `morphedByMany`)도 비다형성 "many to many" 관계와 동일하게 생성할 수 있습니다:

```
use App\Models\Tag;
use App\Models\Video;

$videos = Video::factory()
    ->hasAttached(
        Tag::factory()->count(3),
        ['public' => true]
    )
    ->create();
```

물론, 매직 `has` 메서드로 다형성 "many to many" 관계를 생성할 수도 있습니다:

```
$videos = Video::factory()
    ->hasTags(3, ['public' => true])
    ->create();
```

<a name="defining-relationships-within-factories"></a>
### 팩토리 내에서 관계 정의하기 (Defining Relationships Within Factories)

모델 팩토리 내에서 관계를 정의할 때는 대개 연관된 외래 키에 새로운 팩토리 인스턴스를 할당합니다. 이는 주로 `belongsTo` 또는 `morphTo` 같은 역방향 관계에 적용됩니다. 예를 들어, 게시물을 생성할 때 함께 새 사용자를 생성하려면 다음과 같이 작성할 수 있습니다:

```
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

관계의 컬럼이 팩토리를 정의하는 속성에 따라 달라진다면, 속성에 클로저를 할당할 수도 있습니다. 이 클로저는 팩토리의 평가된 속성 배열을 인수로 받습니다:

```
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
### 관계에 기존 모델 재활용하기 (Recycling an Existing Model for Relationships)

다수의 모델이 공통된 관계를 공유할 때, `recycle` 메서드를 사용해 팩토리로 생성하는 여러 관계에 동일한 관련 모델 인스턴스를 재활용하도록 할 수 있습니다.

예를 들어, `Airline`, `Flight`, `Ticket` 모델이 있고, 티켓은 항공사와 비행기에 속하며 비행기도 항공사에 속한다고 가정해보세요. 티켓을 생성할 때 티켓과 비행기 모두 동일한 항공사여야 하므로, 다음과 같이 항공사 인스턴스를 `recycle` 메서드에 전달할 수 있습니다:

```
Ticket::factory()
    ->recycle(Airline::factory()->create())
    ->create();
```

`recycle` 메서드는 동일한 사용자나 팀에 속한 모델들이 있을 때 매우 유용합니다.

또한 `recycle`은 기존 모델 컬렉션도 인수로 받아, 해당 타입의 모델이 필요할 때 컬렉션에서 무작위로 하나를 선택해 재활용합니다:

```
Ticket::factory()
    ->recycle($airlines)
    ->create();
```