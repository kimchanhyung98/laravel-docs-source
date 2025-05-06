# Eloquent: 팩토리

- [소개](#introduction)
- [모델 팩토리 정의하기](#defining-model-factories)
    - [팩토리 생성하기](#generating-factories)
    - [팩토리 상태(State)](#factory-states)
    - [팩토리 콜백](#factory-callbacks)
- [팩토리를 사용한 모델 생성](#creating-models-using-factories)
    - [모델 인스턴스화](#instantiating-models)
    - [모델 영속화](#persisting-models)
    - [시퀀스(Sequences)](#sequences)
- [팩토리 관계](#factory-relationships)
    - [Has Many 관계](#has-many-relationships)
    - [Belongs To 관계](#belongs-to-relationships)
    - [Many to Many 관계](#many-to-many-relationships)
    - [폴리모픽 관계](#polymorphic-relationships)
    - [팩토리에서 관계 정의](#defining-relationships-within-factories)
    - [기존 모델 재활용하기](#recycling-an-existing-model-for-relationships)

<a name="introduction"></a>
## 소개

애플리케이션을 테스트하거나 데이터베이스에 샘플 데이터를 삽입할 때, 여러 레코드를 데이터베이스에 넣어야 할 때가 있습니다. 각 컬럼의 값을 직접 지정하는 대신, Laravel은 모델 팩토리를 이용해 각 [Eloquent 모델](/docs/{{version}}/eloquent)에 대한 기본 속성 세트를 정의할 수 있도록 해줍니다.

팩토리를 작성하는 예시를 보려면 애플리케이션의 `database/factories/UserFactory.php` 파일을 살펴보세요. 이 팩토리는 모든 새로운 Laravel 애플리케이션에 기본적으로 포함되어 있으며, 다음과 같이 정의되어 있습니다:

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
     * 팩토리에서 사용 중인 현재 비밀번호입니다.
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

위에서 볼 수 있듯, 팩토리는 Laravel의 기본 팩토리 클래스를 상속하고 `definition` 메서드를 정의하는 단순한 클래스입니다. `definition` 메서드는 이 팩토리를 사용해 모델을 생성할 때 적용되어야 할 기본 속성 값을 반환합니다.

`fake` 헬퍼를 통해, 팩토리에서는 [Faker](https://github.com/FakerPHP/Faker) PHP 라이브러리에 접근할 수 있습니다. 이를 통해 테스트 및 시딩 용도로 다양한 종류의 랜덤 데이터를 손쉽게 생성할 수 있습니다.

> [!NOTE]
> `config/app.php` 파일의 `faker_locale` 옵션을 변경하여 애플리케이션의 Faker 로케일을 설정할 수 있습니다.

<a name="defining-model-factories"></a>
## 모델 팩토리 정의하기

<a name="generating-factories"></a>
### 팩토리 생성하기

팩토리를 생성하려면, `make:factory` [Artisan 명령어](/docs/{{version}}/artisan)를 실행하세요:

```shell
php artisan make:factory PostFactory
```

새로운 팩토리 클래스는 `database/factories` 디렉토리에 생성됩니다.

<a name="factory-and-model-discovery-conventions"></a>
#### 모델 및 팩토리 탐색 규칙

팩토리를 정의한 후, 모델이 `Illuminate\Database\Eloquent\Factories\HasFactory` 트레이트를 사용하고 있다면, 모델의 정적 `factory` 메서드를 이용하여 해당 모델의 팩토리 인스턴스를 생성할 수 있습니다.

`HasFactory` 트레이트의 `factory` 메서드는 규칙에 따라 지정된 모델에 적합한 팩토리를 자동으로 찾습니다. 구체적으로, `Database\Factories` 네임스페이스에 모델명과 동일하며 `Factory`로 끝나는 클래스를 찾습니다. 만약 이 규칙이 맞지 않는다면, 모델에서 `newFactory` 메서드를 오버라이드하여 직접 해당 팩토리의 인스턴스를 반환하도록 할 수 있습니다:

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

그런 다음 해당 팩토리에서 `model` 속성을 정의합니다:

```php
use App\Administration\Flight;
use Illuminate\Database\Eloquent\Factories\Factory;

class FlightFactory extends Factory
{
    /**
     * 팩토리가 참조하는 모델 이름입니다.
     *
     * @var class-string<\Illuminate\Database\Eloquent\Model>
     */
    protected $model = Flight::class;
}
```

<a name="factory-states"></a>
### 팩토리 상태(State)

상태 변환 메서드를 통해, 모델 팩토리에서 각각 별도의 변형 상태를 자유롭게 조합하여 적용할 수 있습니다. 예를 들어, `Database\Factories\UserFactory` 팩토리에는 기본 속성 값을 수정하는 `suspended` 상태 메서드를 추가할 수 있습니다.

상태 변환 메서드는 일반적으로 Laravel의 기본 팩토리 클래스가 제공하는 `state` 메서드를 호출합니다. `state` 메서드는 팩토리에 정의된 원시 속성 배열을 받아, 수정할 속성 배열을 반환하는 클로저를 인자로 받습니다:

```php
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * 사용자가 정지(suspended)된 상태임을 나타냅니다.
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
#### "휴지통" 상태

Eloquent 모델에서 [소프트 삭제](/docs/{{version}}/eloquent#soft-deleting)를 지원하는 경우, 내장된 `trashed` 상태 메서드를 사용하여 생성된 모델이 이미 "소프트 삭제"된 상태가 되도록 지정할 수 있습니다. `trashed` 상태는 모든 팩토리에서 자동으로 사용할 수 있으므로 직접 정의할 필요는 없습니다:

```php
use App\Models\User;

$user = User::factory()->trashed()->create();
```

<a name="factory-callbacks"></a>
### 팩토리 콜백

팩토리 콜백은 `afterMaking` 및 `afterCreating` 메서드를 이용하여 등록할 수 있으며, 모델을 만들거나 생성한 후에 추가 작업을 수행할 수 있게 해줍니다. 이러한 콜백은 팩토리 클래스에 `configure` 메서드를 정의하여 등록합니다. 이 메서드는 팩토리 인스턴스가 생성될 때 Laravel이 자동으로 호출합니다:

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

또한 특정 상태에서만 실행되는 추가 작업을 위해 상태 메서드 내에서 팩토리 콜백을 등록할 수 있습니다:

```php
use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * 사용자가 정지(suspended)된 상태임을 나타냅니다.
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
## 팩토리를 사용한 모델 생성

<a name="instantiating-models"></a>
### 모델 인스턴스화

팩토리를 정의했다면, `Illuminate\Database\Eloquent\Factories\HasFactory` 트레이트가 제공하는 모델의 정적 `factory` 메서드를 사용해 해당 모델의 팩토리 인스턴스를 만들 수 있습니다. 몇 가지 예를 살펴보겠습니다. 먼저, `make` 메서드를 사용해서 데이터베이스에 저장하지 않고 모델을 생성할 수 있습니다:

```php
use App\Models\User;

$user = User::factory()->make();
```

`count` 메서드를 이용해 여러 개의 모델 컬렉션을 만들 수도 있습니다:

```php
$users = User::factory()->count(3)->make();
```

<a name="applying-states"></a>
#### 상태 적용하기

[상태(State)](#factory-states)를 모델에 적용할 수도 있습니다. 여러 상태 변환을 적용하고 싶다면, 상태 변환 메서드를 연속으로 호출하면 됩니다:

```php
$users = User::factory()->count(5)->suspended()->make();
```

<a name="overriding-attributes"></a>
#### 속성 값 덮어쓰기

모델의 기본 값을 일부만 덮어쓰고 싶다면, 속성 값 배열을 `make` 메서드에 전달할 수 있습니다. 지정된 속성만 새 값으로 대체되며, 나머지는 팩토리에 지정된 기본값이 사용됩니다:

```php
$user = User::factory()->make([
    'name' => 'Abigail Otwell',
]);
```

또는, 팩토리 인스턴스에서 직접 `state` 메서드를 호출하여 인라인 상태 변환을 적용할 수 있습니다:

```php
$user = User::factory()->state([
    'name' => 'Abigail Otwell',
])->make();
```

> [!NOTE]
> 팩토리를 사용해 모델을 생성할 때는 [대량 할당 보호](/docs/{{version}}/eloquent#mass-assignment)가 자동으로 비활성화됩니다.

<a name="persisting-models"></a>
### 모델 영속화

`create` 메서드는 모델 인스턴스를 만든 뒤 Eloquent의 `save` 메서드를 이용해 데이터베이스에 저장합니다:

```php
use App\Models\User;

// App\Models\User 인스턴스 한 개 생성...
$user = User::factory()->create();

// App\Models\User 인스턴스 세 개 생성...
$users = User::factory()->count(3)->create();
```

`create` 메서드에 속성 배열을 전달하여 팩토리의 기본 속성 값을 재정의할 수 있습니다:

```php
$user = User::factory()->create([
    'name' => 'Abigail',
]);
```

<a name="sequences"></a>
### 시퀀스(Sequences)

모델을 반복 생성할 때 특정 속성 값을 번갈아가며 변경하고 싶을 때가 있습니다. 이럴 때 상태 변환을 시퀀스로 정의하면 됩니다. 예를 들어, 생성되는 사용자마다 `admin` 컬럼 값을 'Y' / 'N'으로 번갈아 적용하려면 다음과 같이 할 수 있습니다:

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

이 예시에서는 다섯 명의 사용자가 `admin` 값 'Y'로, 다른 다섯 명이 'N' 값으로 생성됩니다.

필요하다면 시퀀스 값으로 클로저를 지정할 수도 있습니다. 이 클로저는 시퀀스 값이 필요할 때마다 호출됩니다:

```php
use Illuminate\Database\Eloquent\Factories\Sequence;

$users = User::factory()
    ->count(10)
    ->state(new Sequence(
        fn (Sequence $sequence) => ['role' => UserRoles::all()->random()],
    ))
    ->create();
```

시퀀스 클로저 내에서는, 클로저에 주입된 시퀀스 인스턴스의 `$index`, `$count` 속성에 접근할 수 있습니다. `$index`는 지금까지 반복된 횟수, `$count`는 시퀀스가 총 몇 번 실행될지를 나타냅니다:

```php
$users = User::factory()
    ->count(10)
    ->sequence(fn (Sequence $sequence) => ['name' => 'Name '.$sequence->index])
    ->create();
```

편의를 위해, 시퀀스는 `sequence` 메서드를 통해서도 적용할 수 있습니다. 이 메서드는 내부적으로 `state` 메서드를 호출하며, 클로저나 속성 배열을 인자로 받을 수 있습니다:

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
## 팩토리 관계

<a name="has-many-relationships"></a>
### Has Many 관계

이번에는 Eloquent 모델 관계를 Laravel의 팩토리 메서드로 구축하는 방법을 알아봅니다. 예를 들어, 앱에 `App\Models\User` 모델과 `App\Models\Post` 모델이 있다고 가정하고, `User` 모델이 `Post`와 hasMany 관계로 연결되어 있다고 합시다. 팩토리의 `has` 메서드를 사용하여 세 개의 포스트를 가진 사용자를 쉽게 생성할 수 있습니다. `has` 메서드는 팩토리 인스턴스를 인자로 받습니다:

```php
use App\Models\Post;
use App\Models\User;

$user = User::factory()
    ->has(Post::factory()->count(3))
    ->create();
```

관례상, `has` 메서드에 `Post` 모델을 전달하면, Laravel은 `User` 모델에 `posts` 메서드(관계 메서드)가 정의되어 있다고 간주합니다. 필요하다면, 조작하고자 하는 관계의 이름을 명시적으로 지정할 수도 있습니다:

```php
$user = User::factory()
    ->has(Post::factory()->count(3), 'posts')
    ->create();
```

물론, 관계된 모델에도 상태 변환을 적용할 수 있습니다. 또한 상태 변환이 부모 모델을 참조해야 한다면, 클로저를 상태로 전달할 수 있습니다:

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

더욱 간편하게, Laravel의 매직 팩토리 관계 메서드를 이용해 관계를 생성할 수 있습니다. 예를 들어, 아래 코드에서는 `User` 모델의 `posts` 관계 메서드를 자동으로 사용해서 관련 모델을 생성합니다:

```php
$user = User::factory()
    ->hasPosts(3)
    ->create();
```

매직 메서드를 사용할 때는, 관련 모델에 적용할 속성 배열을 전달할 수도 있습니다:

```php
$user = User::factory()
    ->hasPosts(3, [
        'published' => false,
    ])
    ->create();
```

또한 상태 변환이 부모 모델을 참조해야 한다면, 클로저로 상태 변환을 지정할 수 있습니다:

```php
$user = User::factory()
    ->hasPosts(3, function (array $attributes, User $user) {
        return ['user_type' => $user->type];
    })
    ->create();
```

<a name="belongs-to-relationships"></a>
### Belongs To 관계

이제 팩토리를 이용한 "has many" 관계를 알아보았으니, 관계의 반대편인 "belongs to" 관계도 살펴봅니다. `for` 메서드는 팩토리로 생성되는 모델이 속하게 될 부모 모델을 지정할 때 사용합니다. 예를 들어, 하나의 사용자에 속한 `App\Models\Post` 인스턴스를 세 개 생성할 수 있습니다:

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

이미 부모 모델 인스턴스가 있다면, `for` 메서드에 인스턴스를 직접 전달할 수도 있습니다:

```php
$user = User::factory()->create();

$posts = Post::factory()
    ->count(3)
    ->for($user)
    ->create();
```

<a name="belongs-to-relationships-using-magic-methods"></a>
#### 매직 메서드 사용하기

좀 더 간결하게, Laravel의 매직 팩토리 관계 메서드로 "belongs to" 관계를 정의할 수 있습니다. 아래 코드에서는 Convention에 따라 세 개의 포스트가 `Post` 모델의 `user` 관계에 속하도록 만듭니다:

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

[Has many 관계](#has-many-relationships)와 마찬가지로, "many to many" 관계도 `has` 메서드를 이용해 생성할 수 있습니다:

```php
use App\Models\Role;
use App\Models\User;

$user = User::factory()
    ->has(Role::factory()->count(3))
    ->create();
```

<a name="pivot-table-attributes"></a>
#### Pivot 테이블 속성

연결(중간) 테이블에 값을 설정해야 한다면, `hasAttached` 메서드를 사용하세요. 이 메서드는 두 번째 인자로 피벗 테이블 속성과 값을 받습니다:

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

상태 변환이 관계 모델을 참조해야 한다면 클로저를 사용해줄 수 있습니다:

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

이미 연결할 모델 인스턴스들이 있다면, `hasAttached` 메서드에 인스턴스 컬렉션을 전달하여 모든 사용자에 대해 동일한 역할을 부여할 수 있습니다:

```php
$roles = Role::factory()->count(3)->create();

$user = User::factory()
    ->count(3)
    ->hasAttached($roles, ['active' => true])
    ->create();
```

<a name="many-to-many-relationships-using-magic-methods"></a>
#### 매직 메서드 사용하기

편의상, 매직 팩토리 관계 메서드로 다대다 관계도 정의할 수 있습니다. 아래에서는 Convention에 따라 `User` 모델의 `roles` 관계를 통해 연관 모델을 생성합니다:

```php
$user = User::factory()
    ->hasRoles(1, [
        'name' => 'Editor'
    ])
    ->create();
```

<a name="polymorphic-relationships"></a>
### 폴리모픽 관계

[폴리모픽 관계](/docs/{{version}}/eloquent-relationships#polymorphic-relationships)도 팩토리를 이용해 만들 수 있습니다. 폴리모픽 "morph many" 관계는 일반 "has many" 관계와 똑같이 생성합니다. 예를 들어, `App\Models\Post` 모델이 `App\Models\Comment` 모델과 morphMany 관계를 맺고 있다면:

```php
use App\Models\Post;

$post = Post::factory()->hasComments(3)->create();
```

<a name="morph-to-relationships"></a>
#### Morph To 관계

매직 메서드는 `morphTo` 관계를 생성할 때 사용할 수 없습니다. 대신, `for` 메서드를 직접 사용하고 관계의 이름을 명시적으로 지정해야 합니다. 예를 들어, `Comment` 모델이 `morphTo` 관계를 정의한 `commentable` 메서드를 가진다면 아래처럼 사용할 수 있습니다:

```php
$comments = Comment::factory()->count(3)->for(
    Post::factory(), 'commentable'
)->create();
```

<a name="polymorphic-many-to-many-relationships"></a>
#### 폴리모픽 다대다(Many to Many) 관계

폴리모픽 "many to many" (`morphToMany` / `morphedByMany`) 관계 역시 비폴리모픽 다대다와 같은 방식으로 생성할 수 있습니다:

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

물론 매직 `has` 메서드로도 폴리모픽 다대다 관계를 생성할 수 있습니다:

```php
$videos = Video::factory()
    ->hasTags(3, ['public' => true])
    ->create();
```

<a name="defining-relationships-within-factories"></a>
### 팩토리에서 관계 정의

팩토리 내에서 관계를 정의할 때는, 보통 관계의 외래키에 새로운 팩토리 인스턴스를 할당합니다. 주로 `belongsTo`, `morphTo`같은 "역방향" 관계에서 사용합니다. 예를 들어, 포스트를 생성할 때 새로운 사용자를 함께 만들려면 다음과 같이 할 수 있습니다:

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

관계 컬럼이 팩토리에 의해 동적으로 정해진 경우, 속성에 클로저를 할당할 수도 있습니다. 이 클로저는 팩토리가 평가한 속성 배열을 받습니다:

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
### 기존 모델 재활용하기

여러 모델이 특정 관계 모델을 공유해야 할 때는, 팩토리의 `recycle` 메서드를 활용해 관련 모델 인스턴스가 재활용되도록 할 수 있습니다.

예를 들어, `Airline`, `Flight`, `Ticket` 모델이 있고, 티켓은 항공사와 비행편에 속하며, 비행편 또한 항공사에 속한다고 가정합시다. 티켓을 만들 때, 티켓과 비행편 모두 같은 항공사가 되게 하려면 다음과 같이 할 수 있습니다:

```php
Ticket::factory()
    ->recycle(Airline::factory()->create())
    ->create();
```

이 메서드는 같은 사용자 또는 팀에 속하는 여러 모델을 대량 생성할 때 특히 유용합니다.

`recycle` 메서드는 기존 모델들의 컬렉션도 받을 수 있습니다. 컬렉션이 제공되면, 팩토리가 해당 종류의 모델이 필요할 때마다 컬렉션에서 무작위로 하나를 선택합니다:

```php
Ticket::factory()
    ->recycle($airlines)
    ->create();
```
