# Eloquent: 팩토리 (Factories)

- [소개](#introduction)
- [모델 팩토리 정의하기](#defining-model-factories)
    - [팩토리 생성하기](#generating-factories)
    - [팩토리 상태(States)](#factory-states)
    - [팩토리 콜백(Callbacks)](#factory-callbacks)
- [팩토리를 사용해 모델 생성하기](#creating-models-using-factories)
    - [모델 인스턴스화하기](#instantiating-models)
    - [모델 영속화하기](#persisting-models)
    - [시퀀스(Sequences)](#sequences)
- [팩토리 관계(Factory Relationships)](#factory-relationships)
    - [Has Many 관계](#has-many-relationships)
    - [Belongs To 관계](#belongs-to-relationships)
    - [Many to Many 관계](#many-to-many-relationships)
    - [다형성(Polymorphic) 관계](#polymorphic-relationships)
    - [팩토리 내에서 관계 정의하기](#defining-relationships-within-factories)
    - [기존 모델 재활용하기](#recycling-an-existing-model-for-relationships)

<a name="introduction"></a>
## 소개 (Introduction)

애플리케이션을 테스트하거나 데이터베이스에 시딩할 때, 여러 데이터를 데이터베이스에 삽입해야 할 수 있습니다. 각 컬럼 값을 일일이 수동으로 지정하는 대신, Laravel은 [Eloquent 모델](/docs/12.x/eloquent)별로 기본 속성 집합을 정의할 수 있는 모델 팩토리를 지원합니다.

팩토리를 작성하는 방법 예시는 애플리케이션 내 `database/factories/UserFactory.php` 파일을 참고하세요. 이 팩토리는 새 Laravel 애플리케이션에 기본 포함되어 있으며, 다음과 같은 팩토리 정의가 들어있습니다:

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

가장 기본적으로 팩토리는 Laravel의 기본 팩토리 클래스를 상속하는 클래스이며, `definition` 메서드를 정의합니다. `definition` 메서드는 팩토리를 통해 모델 생성 시 적용될 기본 속성값 집합을 배열로 반환합니다.

또한 `fake` 헬퍼를 통해 [Faker](https://github.com/FakerPHP/Faker) PHP 라이브러리를 사용할 수 있어, 테스트와 시딩에 필요한 다양한 랜덤 데이터를 편리하게 생성할 수 있습니다.

> [!NOTE]
> 애플리케이션의 Faker 로케일은 `config/app.php` 설정파일 내 `faker_locale` 옵션을 변경해 조정할 수 있습니다.

<a name="defining-model-factories"></a>
## 모델 팩토리 정의하기 (Defining Model Factories)

<a name="generating-factories"></a>
### 팩토리 생성하기 (Generating Factories)

팩토리를 생성하려면 `make:factory` Artisan 명령어를 실행하세요:

```shell
php artisan make:factory PostFactory
```

새 팩토리 클래스는 `database/factories` 디렉토리에 생성됩니다.

<a name="factory-and-model-discovery-conventions"></a>
#### 모델과 팩토리 자동 인식 규칙 (Model and Factory Discovery Conventions)

팩토리를 정의한 후, `Illuminate\Database\Eloquent\Factories\HasFactory` 트레이트가 모델에 제공하는 정적 `factory` 메서드를 사용해 해당 모델용 팩토리 인스턴스를 생성할 수 있습니다.

`HasFactory` 트레이트의 `factory` 메서드는 convention(규칙)을 통해 모델에 적합한 팩토리를 자동으로 찾습니다. 구체적으로, `Database\Factories` 네임스페이스 내에서 모델 이름과 일치하고 `Factory`로 끝나는 클래스명을 가진 팩토리를 찾습니다. 만약 이 규칙이 애플리케이션이나 팩토리에 맞지 않는다면, 모델 내에서 `newFactory` 메서드를 덮어써서 직접 대응하는 팩토리 인스턴스를 반환하도록 할 수 있습니다:

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

그리고 해당 팩토리 클래스에는 `model` 속성을 정의해 연관된 모델 클래스를 명시해야 합니다:

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
### 팩토리 상태(States)

팩토리 상태 메서드는 팩토리의 기본 속성 집합에 다양한 조합으로 적용할 수 있는 독립적인 변경사항을 정의하도록 돕습니다. 예를 들어, `Database\Factories\UserFactory`에는 `suspended` 상태 메서드를 만들어 기본 속성을 변형할 수 있습니다.

상태 변경 메서드는 보통 Laravel 기본 팩토리 클래스가 제공하는 `state` 메서드를 호출합니다. `state` 메서드는 팩토리의 원시 속성 배열을 인수로 받고, 변경할 속성 배열을 반환하는 클로저를 받습니다:

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
#### "삭제된(Trashed)" 상태

Eloquent 모델이 [소프트 삭제](/docs/12.x/eloquent#soft-deleting)를 지원한다면, 내장된 `trashed` 상태 메서드를 사용해 생성된 모델이 이미 "소프트 삭제된" 상태임을 표시할 수 있습니다. `trashed` 상태는 자동으로 모든 팩토리에 제공되므로 직접 정의할 필요가 없습니다:

```php
use App\Models\User;

$user = User::factory()->trashed()->create();
```

<a name="factory-callbacks"></a>
### 팩토리 콜백(Callbacks)

팩토리 콜백 기능은 `afterMaking` 및 `afterCreating` 메서드를 이용해 모델을 만들거나 생성한 후 추가 작업을 수행하도록 해줍니다. 이 콜백들은 팩토리 클래스에 `configure` 메서드를 정의해 등록할 수 있으며, 팩토리 인스턴스 생성 시 Laravel이 자동으로 호출합니다:

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

상태 메서드 내에서도 콜백을 등록해 특정 상태에 관련된 추가 작업을 할 수 있습니다:

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
## 팩토리를 사용해 모델 생성하기 (Creating Models Using Factories)

<a name="instantiating-models"></a>
### 모델 인스턴스화하기 (Instantiating Models)

팩토리를 정의한 후 `Illuminate\Database\Eloquent\Factories\HasFactory` 트레이트가 제공하는 정적 `factory` 메서드를 사용해 모델 팩토리 인스턴스를 생성할 수 있습니다. 먼저, `make` 메서드를 사용해 데이터베이스에 저장하지 않고 모델 인스턴스만 생성하는 예시를 보겠습니다:

```php
use App\Models\User;

$user = User::factory()->make();
```

`count` 메서드를 사용하면 여러 모델 인스턴스를 컬렉션 형태로 만들 수 있습니다:

```php
$users = User::factory()->count(3)->make();
```

<a name="applying-states"></a>
#### 상태 적용하기

그리고 필요하다면 정의한 여러 [상태들](#factory-states)을 모델에 적용할 수 있습니다. 여러 상태를 동시에 적용하려면 상태 변환 메서드를 직접 연달아 호출하면 됩니다:

```php
$users = User::factory()->count(5)->suspended()->make();
```

<a name="overriding-attributes"></a>
#### 속성 재정의하기

모델의 기본 값 중 일부만 덮어쓰고 싶다면, `make` 메서드에 속성 배열을 전달할 수 있습니다. 지정한 속성만 변경되며, 나머지는 팩토리 정의에 따라 기본값으로 유지됩니다:

```php
$user = User::factory()->make([
    'name' => 'Abigail Otwell',
]);
```

또는 팩토리 인스턴스의 `state` 메서드를 직접 호출해 인라인 상태 변환을 수행할 수도 있습니다:

```php
$user = User::factory()->state([
    'name' => 'Abigail Otwell',
])->make();
```

> [!NOTE]
> 팩토리를 통해 모델을 생성할 때는 [대량 할당 보호](/docs/12.x/eloquent#mass-assignment)가 자동으로 비활성화됩니다.

<a name="persisting-models"></a>
### 모델 영속화하기 (Persisting Models)

`create` 메서드는 모델 인스턴스를 생성하고, Eloquent의 `save` 메서드를 이용해 데이터베이스에 저장합니다:

```php
use App\Models\User;

// 단일 App\Models\User 인스턴스 생성
$user = User::factory()->create();

// 세 개의 App\Models\User 인스턴스 생성
$users = User::factory()->count(3)->create();
```

`create` 메서드에 속성 배열을 전달해 팩토리 기본 속성값을 재정의할 수도 있습니다:

```php
$user = User::factory()->create([
    'name' => 'Abigail',
]);
```

<a name="sequences"></a>
### 시퀀스 (Sequences)

때때로 각 생성 모델마다 특정 속성값을 번갈아가면서 지정하고 싶을 때가 있습니다. 이럴 경우 상태 변경을 시퀀스로 정의해 간편히 처리할 수 있습니다. 예를 들어 `admin` 컬럼 값을 사용자 별로 `Y` 또는 `N`으로 번갈아 할당하려 할 때:

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

이렇게 하면 10명의 사용자 중 5명은 `admin` 값이 `Y`, 나머지 5명은 `N`으로 생성됩니다.

필요하다면 시퀀스 값에 클로저를 넣어, 호출할 때마다 동적으로 값을 반환하게 할 수도 있습니다:

```php
use Illuminate\Database\Eloquent\Factories\Sequence;

$users = User::factory()
    ->count(10)
    ->state(new Sequence(
        fn (Sequence $sequence) => ['role' => UserRoles::all()->random()],
    ))
    ->create();
```

시퀀스 클로저 내부에는 주입된 `Sequence` 인스턴스의 `$index`와 `$count` 프로퍼티에 접근할 수 있습니다. `$index`는 현재 반복 횟수이며, `$count`는 시퀀스가 호출될 총 횟수입니다:

```php
$users = User::factory()
    ->count(10)
    ->sequence(fn (Sequence $sequence) => ['name' => 'Name '.$sequence->index])
    ->create();
```

참고로 `sequence` 메서드는 내부에서 `state` 메서드를 호출하는 간편 래퍼입니다. `sequence` 메서드에는 클로저나 배열 형태의 시퀀스 속성들을 전달할 수 있습니다:

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
## 팩토리 관계(Factory Relationships)

<a name="has-many-relationships"></a>
### Has Many 관계

다음은 Laravel의 팩토리 유창한 API를 이용해 Eloquent 모델 관계를 만드는 방법을 살펴봅니다. 예를 들어, `App\Models\User` 모델과 `App\Models\Post` 모델이 있고, `User` 모델이 `hasMany` 관계로 `Post`를 가지는 상황입니다. `has` 메서드를 사용하면 하나의 사용자가 세 개의 게시글을 가진 상태로 생성할 수 있습니다. `has` 메서드는 팩토리 인스턴스를 인자로 받습니다:

```php
use App\Models\Post;
use App\Models\User;

$user = User::factory()
    ->has(Post::factory()->count(3))
    ->create();
```

관례적으로 `Post` 모델을 `has` 메서드에 전달하면 Laravel은 `User` 모델에 `posts` 메서드가 존재해 관계를 정의한다고 가정합니다. 필요하다면 두 번째 인수로 직접 관계명을 지정할 수도 있습니다:

```php
$user = User::factory()
    ->has(Post::factory()->count(3), 'posts')
    ->create();
```

당연히 관계된 모델에 상태 변형을 적용할 수 있으며, 만약 상태 변환에 부모 모델 참조가 필요하다면 클로저 기반 상태 변환을 전달할 수도 있습니다:

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
#### 매직 메서드 활용하기

간편함을 위해, Laravel이 제공하는 팩토리 관계용 매직 메서드를 사용할 수 있습니다. 예를 들어, 아래는 `User` 모델의 `posts` 관계 메서드를 이용해 관련 모델을 생성하는 행위를 관례에 따라 처리합니다:

```php
$user = User::factory()
    ->hasPosts(3)
    ->create();
```

매직 메서드에 속성 배열을 넘겨 관련 모델의 특정 값들을 덮어쓸 수 있기도 합니다:

```php
$user = User::factory()
    ->hasPosts(3, [
        'published' => false,
    ])
    ->create();
```

상태 변환에 부모 모델의 참조가 필요하면 클로저 형태도 지원합니다:

```php
$user = User::factory()
    ->hasPosts(3, function (array $attributes, User $user) {
        return ['user_type' => $user->type];
    })
    ->create();
```

<a name="belongs-to-relationships"></a>
### Belongs To 관계

"has many" 관계를 살펴봤으니, 이제 반대 관계를 보겠습니다. `for` 메서드는 해당 팩토리로 생성하는 모델이 속한 상위 모델을 지정할 때 사용합니다. 예를 들어, 세 개의 `App\Models\Post` 인스턴스가 단일 사용자에 속하도록 생성할 수 있습니다:

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

이미 연결할 부모 모델 인스턴스가 있을 경우, 그 인스턴스를 `for` 메서드에 직접 전달할 수 있습니다:

```php
$user = User::factory()->create();

$posts = Post::factory()
    ->count(3)
    ->for($user)
    ->create();
```

<a name="belongs-to-relationships-using-magic-methods"></a>
#### 매직 메서드 활용하기

현실적인 편의 제공을 위해 Laravel은 "belongs to" 관계 정의를 위한 매직 팩토리 관계 메서드도 제공합니다. 아래 예시는 관례에 따라 세 개의 게시글이 `Post` 모델의 `user` 관계를 통해 특정 사용자에게 귀속됨을 표현합니다:

```php
$posts = Post::factory()
    ->count(3)
    ->forUser([
        'name' => 'Jessica Archer',
    ])
    ->create();
```

<a name="many-to-many-relationships"></a>
### Many to Many 관계

[has many 관계](#has-many-relationships)처럼, "many to many" 관계도 `has` 메서드를 이용해 생성할 수 있습니다:

```php
use App\Models\Role;
use App\Models\User;

$user = User::factory()
    ->has(Role::factory()->count(3))
    ->create();
```

<a name="pivot-table-attributes"></a>
#### 피벗 테이블 속성 지정하기

만약 모델들 사이를 연결하는 피벗(중간) 테이블에 값을 설정해야 한다면, `hasAttached` 메서드를 사용할 수 있습니다. 이 메서드는 두 번째 인수로 피벗 테이블의 속성 이름과 값을 담은 배열을 받습니다:

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

상태 변환이 관련 모델에 대한 참조를 필요로 할 때, 클로저 기반 상태 변환도 가능합니다:

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

이미 생성된 모델 인스턴스를 `hasAttached` 메서드에 넘겨 연결할 수 있습니다. 아래 예시는 동일한 세 개의 Role 인스턴스가 세 명의 사용자 모두에 연결됩니다:

```php
$roles = Role::factory()->count(3)->create();

$user = User::factory()
    ->count(3)
    ->hasAttached($roles, ['active' => true])
    ->create();
```

<a name="many-to-many-relationships-using-magic-methods"></a>
#### 매직 메서드 활용하기

간편한 관계 정의를 위해 Laravel은 many to many 관계용 매직 팩토리 메서드도 제공합니다. 예를 들어, 아래는 관례에 따라 `User` 모델의 `roles` 관계를 통해 관련 모델이 생성됨을 의미합니다:

```php
$user = User::factory()
    ->hasRoles(1, [
        'name' => 'Editor'
    ])
    ->create();
```

<a name="polymorphic-relationships"></a>
### 다형성(Polymorphic) 관계

[다형성 관계](/docs/12.x/eloquent-relationships#polymorphic-relationships)도 팩토리를 통해 생성할 수 있습니다. 다형성 "morph many" 관계는 일반 "has many" 관계 생성과 동일하게 처리합니다. 예를 들어, `App\Models\Post` 모델이 `App\Models\Comment` 모델과 `morphMany` 관계일 때:

```php
use App\Models\Post;

$post = Post::factory()->hasComments(3)->create();
```

<a name="morph-to-relationships"></a>
#### Morph To 관계

`morphTo` 관계는 매직 메서드를 사용할 수 없으며, 대신 `for` 메서드를 직접 호출하고 관계명을 명시해야 합니다. 예를 들어, `Comment` 모델의 `commentable` 메서드가 `morphTo` 관계를 정의하고 있다면, 다음과 같이 세 개의 댓글이 하나의 게시물에 속하게 할 수 있습니다:

```php
$comments = Comment::factory()->count(3)->for(
    Post::factory(), 'commentable'
)->create();
```

<a name="polymorphic-many-to-many-relationships"></a>
#### 다형성 Many to Many 관계

다형성 "many to many" (`morphToMany` / `morphedByMany`) 관계도 일반적인 many to many 관계와 같이 생성할 수 있습니다:

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

물론, 다형성 many to many 관계도 매직 `has` 메서드를 사용해 생성할 수 있습니다:

```php
$videos = Video::factory()
    ->hasTags(3, ['public' => true])
    ->create();
```

<a name="defining-relationships-within-factories"></a>
### 팩토리 내에서 관계 정의하기

팩토리 안에서 관계를 정의할 때, 보통 관계 외래키에 새 팩토리 인스턴스를 할당합니다. 이는 보통 `belongsTo`나 `morphTo`와 같은 "역방향(inverse)" 관계에 적용합니다. 예를 들어, 포스트 생성 시 새로운 사용자를 함께 생성하고 싶다면 다음과 같이 정의합니다:

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

관계 컬럼이 팩토리 내 속성에 의존한다면, 클로저를 속성 값으로 할당할 수도 있습니다. 클로저는 팩토리의 평가된 속성 배열을 인자로 받습니다:

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
### 기존 모델 재활용하기

공통된 관계를 공유하는 여러 모델이 있을 때, `recycle` 메서드를 사용하면 관련 모델 인스턴스를 하나만 재활용하도록 할 수 있습니다.

예를 들어, `Airline`, `Flight`, `Ticket` 모델이 있고, 티켓은 항공사와 비행기에 속하며, 비행기도 항공사에 속하는 경우를 생각해봅시다. 티켓을 생성할 때 티켓의 항공사와 비행기의 항공사를 동일하게 하려면 항공사 인스턴스를 `recycle` 메서드에 전달합니다:

```php
Ticket::factory()
    ->recycle(Airline::factory()->create())
    ->create();
```

`recycle` 메서드는 사용자나 팀 등 공통 관계 모델이 여러 개 있을 때 특히 유용합니다.

또한 `recycle` 메서드는 모델 컬렉션도 받을 수 있습니다. 컬렉션이 주어지면 팩토리는 해당 타입의 모델이 필요할 때 컬렉션에서 무작위로 하나를 선택해 사용합니다:

```php
Ticket::factory()
    ->recycle($airlines)
    ->create();
```