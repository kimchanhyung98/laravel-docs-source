# Eloquent: 팩토리(Factory)

- [소개](#introduction)
- [모델 팩토리 정의](#defining-model-factories)
    - [팩토리 생성](#generating-factories)
    - [팩토리 상태(State)](#factory-states)
    - [팩토리 콜백](#factory-callbacks)
- [팩토리를 이용한 모델 생성](#creating-models-using-factories)
    - [모델 인스턴스화](#instantiating-models)
    - [모델 저장](#persisting-models)
    - [시퀀스](#sequences)
- [팩토리 관계](#factory-relationships)
    - [1:N 관계(Has Many)](#has-many-relationships)
    - [N:1 관계(Belongs To)](#belongs-to-relationships)
    - [N:N 관계(Many to Many)](#many-to-many-relationships)
    - [다형성 관계(Polymorphic)](#polymorphic-relationships)
    - [팩토리 내 관계 정의](#defining-relationships-within-factories)
    - [기존 모델 재사용(Recycling)](#recycling-an-existing-model-for-relationships)

<a name="introduction"></a>
## 소개

애플리케이션을 테스트하거나 데이터베이스에 더미 데이터를 입력할 때, 데이터베이스에 몇 개의 레코드를 삽입해야 할 수 있습니다. 각 컬럼의 값을 일일이 지정하지 않고, Laravel에서는 각 [Eloquent 모델](/docs/{{version}}/eloquent)에 대해 모델 팩토리를 사용하여 기본 속성 세트를 정의할 수 있습니다.

팩토리 작성 예제를 보려면, 애플리케이션의 `database/factories/UserFactory.php` 파일을 참고하세요. 이 팩토리는 모든 새로운 Laravel 애플리케이션에 포함되어 있으며, 다음과 같이 정의되어 있습니다.

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
     * 모델의 이메일 주소가 미인증(verified 아님)임을 표시.
     */
    public function unverified(): static
    {
        return $this->state(fn (array $attributes) => [
            'email_verified_at' => null,
        ]);
    }
}
```

보시다시피, 팩토리는 Laravel의 기본 팩토리 클래스를 확장하고 `definition` 메서드를 정의하는 클래스입니다. `definition` 메서드는 팩토리를 통해 모델을 생성할 때 사용할 기본 속성값들의 집합을 반환합니다.

팩토리는 `fake` 헬퍼를 통해 [Faker](https://github.com/FakerPHP/Faker) PHP 라이브러리에 접근할 수 있어, 테스트 및 시딩 데이터를 쉽게 랜덤으로 생성할 수 있습니다.

> [!NOTE]
> `config/app.php` 설정 파일의 `faker_locale` 옵션을 변경하여 Faker의 로케일을 조정할 수 있습니다.

<a name="defining-model-factories"></a>
## 모델 팩토리 정의

<a name="generating-factories"></a>
### 팩토리 생성

팩토리를 생성하려면, `make:factory` [Artisan 명령어](/docs/{{version}}/artisan)를 실행하세요.

```shell
php artisan make:factory PostFactory
```

새로운 팩토리 클래스는 `database/factories` 디렉토리에 생성됩니다.

<a name="factory-and-model-discovery-conventions"></a>
#### 모델 및 팩토리 규칙

팩토리를 정의한 후에는, `Illuminate\Database\Eloquent\Factories\HasFactory` 트레이트가 제공하는 static `factory` 메서드를 사용하여 해당 모델에 대한 팩토리 인스턴스를 생성할 수 있습니다.

`HasFactory` 트레이트의 `factory` 메서드는 규칙에 따라 해당 모델의 적절한 팩토리를 찾습니다. 구체적으로, 이 메서드는 `Database\Factories` 네임스페이스에서 모델명과 일치하며 `Factory`로 끝나는 클래스명을 찾습니다. 이러한 규칙이 애플리케이션에 맞지 않다면, 모델에서 `newFactory` 메서드를 오버라이드하여 해당 모델의 팩토리 인스턴스를 직접 반환할 수 있습니다.

```php
use Database\Factories\Administration\FlightFactory;

/**
 * 모델에 대한 새로운 팩토리 인스턴스 생성.
 */
protected static function newFactory()
{
    return FlightFactory::new();
}
```

그리고 해당 팩토리에서는 아래와 같이 `model` 속성을 정의합니다.

```php
use App\Administration\Flight;
use Illuminate\Database\Eloquent\Factories\Factory;

class FlightFactory extends Factory
{
    /**
     * 팩토리와 연결된 모델의 이름.
     *
     * @var class-string<\Illuminate\Database\Eloquent\Model>
     */
    protected $model = Flight::class;
}
```

<a name="factory-states"></a>
### 팩토리 상태(State)

상태 변환 메서드를 사용하면, 팩토리에 개별적으로 적용할 수 있는 여러 수정 상태를 정의할 수 있습니다. 예를 들어, `Database\Factories\UserFactory`에 기본 속성값 중 하나를 수정하는 `suspended` 상태 메서드를 정의할 수 있습니다.

상태 변환 메서드는 주로 Laravel 기본 팩토리 클래스의 `state` 메서드를 호출합니다. 이 메서드는 팩토리에 정의된 속성 배열을 받아, 변경할 속성 값을 담은 배열을 반환해야 합니다.

```php
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * 사용자가 정지됨(suspended) 상태임을 표시.
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

Eloquent 모델이 [소프트 삭제](/docs/{{version}}/eloquent#soft-deleting)를 지원한다면, 내장된 `trashed` 상태 메서드를 사용하여 생성된 모델이 이미 "소프트 삭제된" 상태임을 지정할 수 있습니다. 이 상태는 모든 팩토리에서 자동으로 제공되므로 직접 정의할 필요가 없습니다.

```php
use App\Models\User;

$user = User::factory()->trashed()->create();
```

<a name="factory-callbacks"></a>
### 팩토리 콜백

팩토리 콜백은 `afterMaking` 및 `afterCreating` 메서드를 사용하여 등록할 수 있으며, 모델을 만들거나 생성한 후 추가 작업을 수행할 수 있습니다. 이 콜백들은 팩토리 클래스의 `configure` 메서드에서 등록해야 하며, 팩토리가 인스턴스화될 때 Laravel이 자동으로 호출합니다.

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

또한, 상태 메서드 안에서도 특정 상태에만 해당하는 추가 작업을 수행하려면 콜백을 등록할 수 있습니다.

```php
use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * 사용자가 정지됨(suspended) 상태임을 표시.
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

팩토리를 정의한 뒤에는, `Illuminate\Database\Eloquent\Factories\HasFactory` 트레이트의 static `factory` 메서드를 활용해 해당 모델의 팩토리 인스턴스를 만들 수 있습니다. 예를 들어, 데이터베이스에 저장하지 않고 모델을 생성하려면 `make` 메서드를 사용할 수 있습니다.

```php
use App\Models\User;

$user = User::factory()->make();
```

여러 개의 모델을 만들고 싶다면, `count` 메서드를 사용하세요.

```php
$users = User::factory()->count(3)->make();
```

<a name="applying-states"></a>
#### 상태(State) 지정

모델에 [상태](#factory-states)를 적용할 수도 있습니다. 여러 상태 변환을 동시에 적용하려면, 상태 변환 메서드를 연속으로 호출하면 됩니다.

```php
$users = User::factory()->count(5)->suspended()->make();
```

<a name="overriding-attributes"></a>
#### 속성 재정의

기본 속성값을 일부 변경하고 싶다면, `make` 메서드에 값을 배열로 전달하세요. 지정한 속성만 대체되고 나머지는 기본값이 유지됩니다.

```php
$user = User::factory()->make([
    'name' => 'Abigail Otwell',
]);
```

또는, `state` 메서드를 팩토리 인스턴스에 직접 호출하여 인라인 상태 변환을 수행할 수 있습니다.

```php
$user = User::factory()->state([
    'name' => 'Abigail Otwell',
])->make();
```

> [!NOTE]
> 팩토리를 이용해 모델을 생성할 때는 [대량 할당 보호](#mass-assignment(/docs/{{version}}/eloquent#mass-assignment))가 자동으로 비활성화됩니다.

<a name="persisting-models"></a>
### 모델 저장

`create` 메서드는 모델 인스턴스를 생성하고 Eloquent의 `save` 메서드를 사용하여 데이터베이스에 저장합니다.

```php
use App\Models\User;

// 하나의 App\Models\User 인스턴스 생성 및 저장...
$user = User::factory()->create();

// 세 개의 App\Models\User 인스턴스 생성 및 저장...
$users = User::factory()->count(3)->create();
```

기본 속성 대신 일부 값을 전달하려면, `create` 메서드에 배열로 값을 전달하세요.

```php
$user = User::factory()->create([
    'name' => 'Abigail',
]);
```

<a name="sequences"></a>
### 시퀀스

여러 모델을 생성할 때, 특정 속성의 값을 순차적으로 달리 지정하고 싶을 때가 있습니다. 이럴 때 상태 변환을 시퀀스(Sequence)로 정의할 수 있습니다. 예를 들어, 생성할 사용자마다 `admin` 컬럼 값을 `Y`와 `N`으로 번갈아 지정하려면 다음과 같이 합니다.

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

이 예시에서는 `admin` 값이 `Y`인 사용자 5명과, `N`인 사용자 5명이 생성됩니다.

필요하다면 시퀀스 값으로 클로저를 포함할 수도 있습니다. 시퀀스에 새로운 값이 필요할 때마다 클로저가 호출됩니다.

```php
use Illuminate\Database\Eloquent\Factories\Sequence;

$users = User::factory()
    ->count(10)
    ->state(new Sequence(
        fn (Sequence $sequence) => ['role' => UserRoles::all()->random()],
    ))
    ->create();
```

시퀀스 클로저 내부에서는, 클로저에 주입된 시퀀스 인스턴스의 `$index`와 `$count` 속성을 사용할 수 있습니다. `$index`는 지금까지 시퀀스를 순회한 횟수, `$count`는 시퀀스가 호출될 총 횟수를 의미합니다.

```php
$users = User::factory()
    ->count(10)
    ->sequence(fn (Sequence $sequence) => ['name' => 'Name '.$sequence->index])
    ->create();
```

편의를 위해, `sequence` 메서드를 사용하여 시퀀스를 지정할 수도 있습니다. 이 메서드는 내부적으로 `state` 메서드를 호출하며, 배열이나 클로저를 인자로 받을 수 있습니다.

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
### 1:N 관계(Has Many)

이제, Laravel의 플루언트한 팩토리 메서드를 이용하여 Eloquent 모델 간의 관계를 만드는 방법을 알아보겠습니다. 예를 들어, `App\Models\User` 모델과 `App\Models\Post` 모델이 있고, `User`가 `Post`와의 hasMany 관계를 정의한다고 가정해 보겠습니다. 팩토리의 `has` 메서드를 사용하여 사용자가 3개의 게시글을 가지도록 할 수 있습니다. `has` 메서드는 팩토리 인스턴스를 받아들입니다.

```php
use App\Models\Post;
use App\Models\User;

$user = User::factory()
    ->has(Post::factory()->count(3))
    ->create();
```

관례상, `has` 메서드에 `Post` 모델을 전달하면, Laravel은 `User` 모델에 반드시 `posts` 메서드가 존재하며, 이 메서드가 관계를 정의한다고 간주합니다. 필요하다면, 명시적으로 조작하려는 관계의 이름을 지정할 수도 있습니다.

```php
$user = User::factory()
    ->has(Post::factory()->count(3), 'posts')
    ->create();
```

관련 모델에 상태 변환을 적용할 수도 있으며, 상태 변경에 부모 모델에 대한 접근이 필요하다면 클로저 형태의 상태 변환을 사용할 수 있습니다.

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

편의상, Laravel의 매직 팩토리 관계 메서드를 사용하여 관계를 쉽게 설정할 수 있습니다. 아래 예시는, `User` 모델의 `posts` 관계 메서드를 통해 관련 모델이 만들어져야 함을 자동으로 판단합니다.

```php
$user = User::factory()
    ->hasPosts(3)
    ->create();
```

매직 메서드를 사용할 때, 관련 모델의 속성을 배열로 전달하여 재정의할 수도 있습니다.

```php
$user = User::factory()
    ->hasPosts(3, [
        'published' => false,
    ])
    ->create();
```

부모 모델에 대한 접근이 필요한 상태 변환이 있다면, 클로저를 전달할 수도 있습니다.

```php
$user = User::factory()
    ->hasPosts(3, function (array $attributes, User $user) {
        return ['user_type' => $user->type];
    })
    ->create();
```

<a name="belongs-to-relationships"></a>
### N:1 관계(Belongs To)

이제 팩토리를 이용한 "has many" 관계의 반대인 "belong to" 관계를 살펴보겠습니다. `for` 메서드를 사용하면 팩토리가 생성하는 모델이 속해야 하는 부모 모델을 지정할 수 있습니다. 예를 들어, 3개의 `App\Models\Post` 모델 인스턴스가 하나의 사용자에 속하도록 할 수 있습니다.

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

이미 부모 모델 인스턴스가 존재한다면, `for` 메서드에 해당 인스턴스를 전달할 수 있습니다.

```php
$user = User::factory()->create();

$posts = Post::factory()
    ->count(3)
    ->for($user)
    ->create();
```

<a name="belongs-to-relationships-using-magic-methods"></a>
#### 매직 메서드 사용

편의상, Laravel의 매직 팩토리 관계 메서드로 "belongs to" 관계도 지정할 수 있습니다. 아래 예시는 3개의 게시글이 `Post` 모델의 `user` 관계에 속하게 함을 자동으로 판단합니다.

```php
$posts = Post::factory()
    ->count(3)
    ->forUser([
        'name' => 'Jessica Archer',
    ])
    ->create();
```

<a name="many-to-many-relationships"></a>
### N:N 관계(Many to Many)

["has many" 관계](#has-many-relationships)와 비슷하게, "many to many" 관계도 `has` 메서드를 이용해 생성할 수 있습니다.

```php
use App\Models\Role;
use App\Models\User;

$user = User::factory()
    ->has(Role::factory()->count(3))
    ->create();
```

<a name="pivot-table-attributes"></a>
#### Pivot 테이블 속성

모델을 연결하는 중간(pivot) 테이블에 값 및 속성을 지정할 필요가 있다면, `hasAttached` 메서드를 사용할 수 있습니다. 이 메서드는 두 번째 인자로 피벗 테이블 속성의 이름과 값을 배열로 받습니다.

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

관계 모델에 대한 접근이 필요한 상태 변환이 있다면, 클로저 형태로 상태 변환을 정의할 수 있습니다.

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

이미 만들어진 모델 인스턴스들을 새로 생성할 모델에 연결하고 싶다면, `hasAttached` 메서드에 이들을 전달하세요. 아래 예제에서는 동일한 3개의 역할이 모든 사용자에게 연결됩니다.

```php
$roles = Role::factory()->count(3)->create();

$user = User::factory()
    ->count(3)
    ->hasAttached($roles, ['active' => true])
    ->create();
```

<a name="many-to-many-relationships-using-magic-methods"></a>
#### 매직 메서드 사용

편의상, Laravel의 매직 팩토리 관계 메서드로 N:N 관계도 지정할 수 있습니다. 아래 예시는 `User` 모델의 `roles` 관계 메서드를 통해 관련 모델을 생성해야 함을 자동으로 판단합니다.

```php
$user = User::factory()
    ->hasRoles(1, [
        'name' => 'Editor'
    ])
    ->create();
```

<a name="polymorphic-relationships"></a>
### 다형성 관계(Polymorphic)

[다형성 관계](/docs/{{version}}/eloquent-relationships#polymorphic-relationships) 역시 팩토리로 생성이 가능합니다. 다형성 "morph many" 관계는 일반적인 "has many" 관계와 동일한 방식으로 생성합니다. 예를 들어, `App\Models\Post` 모델이 `App\Models\Comment` 모델과 `morphMany` 관계라면:

```php
use App\Models\Post;

$post = Post::factory()->hasComments(3)->create();
```

<a name="morph-to-relationships"></a>
#### Morph To 관계

매직 메서드는 `morphTo` 관계에서 사용 불가입니다. 대신, `for` 메서드를 직접 사용하고, 관계 이름을 명시적으로 지정해야 합니다. 예를 들어, `Comment` 모델이 `commentable`이라는 `morphTo` 관계를 가진다면, 아래와 같이 3개의 코멘트가 하나의 포스트에 속하게 할 수 있습니다.

```php
$comments = Comment::factory()->count(3)->for(
    Post::factory(), 'commentable'
)->create();
```

<a name="polymorphic-many-to-many-relationships"></a>
#### 다형성 N:N 관계

다형성 "many to many"(`morphToMany`/`morphedByMany`) 관계는 일반적인 N:N 관계와 동일하게 생성할 수 있습니다.

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

물론, 매직 메서드인 `has`에 의해 다형성 관계도 생성할 수 있습니다.

```php
$videos = Video::factory()
    ->hasTags(3, ['public' => true])
    ->create();
```

<a name="defining-relationships-within-factories"></a>
### 팩토리 내에서 관계 정의

팩토리 내부에 관계를 정의하려면, 대개 관계의 외래키에 새 팩토리 인스턴스를 할당합니다. 이는 주로 `belongsTo` 및 `morphTo`와 같은 "역방향" 관계에서 사용됩니다. 예를 들어, 게시글을 생성할 때 새로운 사용자를 함께 생성하려면 아래처럼 합니다.

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

관계 컬럼이 팩토리에서 정의된 속성에 의존적이라면, 속성에 클로저를 할당할 수 있습니다. 이 클로저는 팩토리에서 평가된 속성 배열을 전달받습니다.

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
### 관계를 위한 기존 모델 재사용

여러 모델이 동일한 모델과 관계를 공유할 경우, `recycle` 메서드를 사용하면 생성되는 모든 관계에서 단일 관련 모델 인스턴스가 재활용되도록 할 수 있습니다.

예를 들어, `Airline`, `Flight`, `Ticket` 모델이 있고, 티켓은 항공사와 비행에 속하며, 비행 또한 같은 항공사에 속한다고 가정합니다. 티켓을 생성할 때 티켓과 비행 모두 동일한 항공사를 갖도록 하려면, 아래와 같이 `recycle` 메서드에 항공사 인스턴스를 전달합니다.

```php
Ticket::factory()
    ->recycle(Airline::factory()->create())
    ->create();
```

특히 한 팀이나 사용자가 소유한 여러 모델이 있을 때 `recycle` 메서드는 매우 유용합니다.

`recycle` 메서드는 기존 모델의 컬렉션도 받을 수 있습니다. 컬렉션이 전달되면, 팩토리가 해당 타입의 모델이 필요할 때마다 컬렉션에서 무작위로 하나를 선택합니다.

```php
Ticket::factory()
    ->recycle($airlines)
    ->create();
```
