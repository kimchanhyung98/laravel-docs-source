# 데이터베이스 테스트 (Database Testing)

- [소개](#introduction)
    - [각 테스트 후 데이터베이스 초기화](#resetting-the-database-after-each-test)
- [모델 팩토리 정의하기](#defining-model-factories)
    - [개념 개요](#concept-overview)
    - [팩토리 생성하기](#generating-factories)
    - [팩토리 상태](#factory-states)
    - [팩토리 콜백](#factory-callbacks)
- [팩토리를 사용한 모델 생성](#creating-models-using-factories)
    - [모델 인스턴스 생성하기](#instantiating-models)
    - [모델 영속화하기](#persisting-models)
    - [시퀀스](#sequences)
- [팩토리 관계 설정](#factory-relationships)
    - [Has Many 관계](#has-many-relationships)
    - [Belongs To 관계](#belongs-to-relationships)
    - [Many To Many 관계](#many-to-many-relationships)
    - [다형성 관계](#polymorphic-relationships)
    - [팩토리 내에서 관계 정의하기](#defining-relationships-within-factories)
- [시더 실행하기](#running-seeders)
- [사용 가능한 어서션](#available-assertions)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 데이터베이스 기반 애플리케이션을 더 쉽게 테스트할 수 있도록 여러 유용한 도구와 어서션을 제공합니다. 또한 Laravel 모델 팩토리와 시더를 활용하면 애플리케이션의 Eloquent 모델과 관계를 사용해 테스트용 데이터베이스 레코드를 손쉽게 생성할 수 있습니다. 이 문서에서는 이러한 강력한 기능들을 자세히 살펴보겠습니다.

<a name="resetting-the-database-after-each-test"></a>
### 각 테스트 후 데이터베이스 초기화 (Resetting The Database After Each Test)

실제 테스트를 진행하기 전에, 각 테스트가 끝난 후 데이터베이스를 초기화하여 이전 테스트의 데이터가 다음 테스트에 영향을 주지 않도록 하는 방법을 알아봅시다. Laravel에 기본 포함된 `Illuminate\Foundation\Testing\RefreshDatabase` 트레이트가 이 작업을 자동으로 처리합니다. 테스트 클래스 내에서 단순히 이 트레이트를 사용하면 됩니다:

```
<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    use RefreshDatabase;

    /**
     * 기본 기능 테스트 예제.
     *
     * @return void
     */
    public function test_basic_example()
    {
        $response = $this->get('/');

        // ...
    }
}
```

<a name="defining-model-factories"></a>
## 모델 팩토리 정의하기 (Defining Model Factories)

<a name="concept-overview"></a>
### 개념 개요 (Concept Overview)

먼저, Eloquent 모델 팩토리에 대해 이야기해보겠습니다. 테스트를 할 때, 테스트 수행 전에 데이터베이스에 몇 개의 레코드를 삽입해야 할 수 있습니다. 이때 각 컬럼의 값을 일일이 지정하는 대신, Laravel 모델 팩토리를 통해 각 [Eloquent 모델](/docs/{{version}}/eloquent)에 대한 기본 속성 집합을 정의할 수 있습니다.

팩토리 작성 예를 보려면 애플리케이션 내 `database/factories/UserFactory.php` 파일을 확인하세요. 이 팩토리는 Laravel 새 애플리케이션 생성 시 기본 포함되며, 다음과 같은 정의를 포함합니다:

```
namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;
use Illuminate\Support\Str;

class UserFactory extends Factory
{
    /**
     * 모델의 기본 상태를 정의합니다.
     *
     * @return array
     */
    public function definition()
    {
        return [
            'name' => $this->faker->name(),
            'email' => $this->faker->unique()->safeEmail(),
            'email_verified_at' => now(),
            'password' => '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', // password
            'remember_token' => Str::random(10),
        ];
    }
}
```

보시다시피, 팩토리는 Laravel 기본 팩토리 클래스를 상속하는 클래스이며 `definition` 메서드를 정의합니다. `definition` 메서드는 팩토리를 통해 모델이 생성될 때 적용할 기본 속성 값들을 배열로 반환합니다.

팩토리는 `faker` 속성을 통해 [Faker](https://github.com/FakerPHP/Faker) PHP 라이브러리를 사용할 수 있어, 테스트용 다양한 랜덤 데이터를 손쉽게 생성할 수 있습니다.

> [!TIP]
> `config/app.php` 구성 파일에 `faker_locale` 옵션을 추가하여 애플리케이션 Faker의 로케일을 설정할 수 있습니다.

<a name="generating-factories"></a>
### 팩토리 생성하기 (Generating Factories)

팩토리를 생성하려면 `make:factory` [Artisan 명령어](/docs/{{version}}/artisan)를 실행하세요:

```
php artisan make:factory PostFactory
```

이렇게 하면 새 팩토리 클래스가 `database/factories` 디렉토리에 생성됩니다.

<a name="factory-and-model-discovery-conventions"></a>
#### 모델 및 팩토리 발견 규칙 (Model & Factory Discovery Conventions)

팩토리를 정의한 후엔, `Illuminate\Database\Eloquent\Factories\HasFactory` 트레이트에서 모델에 제공하는 정적 `factory` 메서드를 사용해 해당 모델의 팩토리 인스턴스를 만듭니다.

`HasFactory` 트레이트의 `factory` 메서드는 규칙에 따라 해당 모델에 적합한 팩토리를 찾아냅니다. 구체적으로, `Database\Factories` 네임스페이스 내에 모델 명과 동일한 클래스명을 갖고 뒤에 `Factory`가 붙은 클래스를 찾습니다. 만약 이 규칙이 애플리케이션이나 팩토리에 맞지 않는 경우, 모델 내에 `newFactory` 메서드를 오버라이딩하여 팩토리 인스턴스를 직접 반환하도록 할 수 있습니다:

```
use Database\Factories\Administration\FlightFactory;

/**
 * 모델을 위한 새 팩토리 인스턴스를 생성합니다.
 *
 * @return \Illuminate\Database\Eloquent\Factories\Factory
 */
protected static function newFactory()
{
    return FlightFactory::new();
}
```

그리고 대응하는 팩토리 클래스 내에 `model` 속성을 정의하세요:

```
use App\Administration\Flight;
use Illuminate\Database\Eloquent\Factories\Factory;

class FlightFactory extends Factory
{
    /**
     * 팩토리와 연관된 모델 이름입니다.
     *
     * @var string
     */
    protected $model = Flight::class;
}
```

<a name="factory-states"></a>
### 팩토리 상태 (Factory States)

상태 조작 메서드는 모델 팩토리에 조합 가능한 개별 변형을 정의할 때 사용합니다. 예를 들어 `Database\Factories\UserFactory`에 `suspended` 상태 메서드를 만들어 기본 속성 중 하나를 변경할 수 있습니다.

상태 변환 메서드는 주로 Laravel 기본 팩토리 클래스에서 제공하는 `state` 메서드를 호출합니다. `state`는 클로저를 인수로 받으며, 이 클로저는 원본 속성 배열을 받아 변경할 속성을 배열로 반환해야 합니다:

```
/**
 * 사용자가 정지 상태임을 나타냅니다.
 *
 * @return \Illuminate\Database\Eloquent\Factories\Factory
 */
public function suspended()
{
    return $this->state(function (array $attributes) {
        return [
            'account_status' => 'suspended',
        ];
    });
}
```

<a name="factory-callbacks"></a>
### 팩토리 콜백 (Factory Callbacks)

`afterMaking`과 `afterCreating` 메서드를 사용해 팩토리 콜백을 등록하면 모델 생성 완료 후 추가 작업을 수행할 수 있습니다. 팩토리 클래스 내에 `configure` 메서드를 정의해 이 콜백들을 등록할 수 있으며, 팩토리 생성 시 Laravel이 자동 호출합니다:

```
namespace Database\Factories;

use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;
use Illuminate\Support\Str;

class UserFactory extends Factory
{
    /**
     * 팩토리 구성
     *
     * @return $this
     */
    public function configure()
    {
        return $this->afterMaking(function (User $user) {
            //
        })->afterCreating(function (User $user) {
            //
        });
    }

    // ...
}
```

<a name="creating-models-using-factories"></a>
## 팩토리를 사용한 모델 생성 (Creating Models Using Factories)

<a name="instantiating-models"></a>
### 모델 인스턴스 생성하기 (Instantiating Models)

팩토리를 정의한 후에는, `Illuminate\Database\Eloquent\Factories\HasFactory` 트레이트가 모델에 제공하는 정적 `factory` 메서드를 사용해 팩토리 인스턴스를 만들고, 이를 통해 모델 인스턴스를 생성할 수 있습니다. 먼저, `make` 메서드를 사용해 데이터베이스에 저장하지 않은 모델 인스턴스를 생성하는 예제를 보겠습니다:

```
use App\Models\User;

public function test_models_can_be_instantiated()
{
    $user = User::factory()->make();

    // 테스트에서 모델 사용...
}
```

`count` 메서드를 사용하면 여러 개 모델 컬렉션도 생성할 수 있습니다:

```
$users = User::factory()->count(3)->make();
```

<a name="applying-states"></a>
#### 상태 적용하기 (Applying States)

앞서 정의한 [상태](#factory-states)를 모델에 적용할 수도 있습니다. 여러 상태를 조합하려면 상태 변환 메서드를 차례로 호출하면 됩니다:

```
$users = User::factory()->count(5)->suspended()->make();
```

<a name="overriding-attributes"></a>
#### 속성 재정의하기 (Overriding Attributes)

기본값 중 일부를 직접 지정해 재정의하려면 `make` 메서드에 배열로 넘기면 됩니다. 지정한 속성만 대체되고 나머지는 팩토리 정의값이 유지됩니다:

```
$user = User::factory()->make([
    'name' => 'Abigail Otwell',
]);
```

또는 `state` 메서드에 배열을 넘겨 인라인 변경도 가능합니다:

```
$user = User::factory()->state([
    'name' => 'Abigail Otwell',
])->make();
```

> [!TIP]
> 팩토리로 모델을 생성할 때는 [대량 할당 보호](/docs/{{version}}/eloquent#mass-assignment)가 자동으로 비활성화됩니다.

<a name="persisting-models"></a>
### 모델 영속화하기 (Persisting Models)

`create` 메서드는 모델 인스턴스를 생성함과 동시에 Eloquent의 `save` 메서드로 데이터베이스에 저장합니다:

```
use App\Models\User;

public function test_models_can_be_persisted()
{
    // 단일 User 인스턴스 생성 및 저장...
    $user = User::factory()->create();

    // User 인스턴스 3개 생성 및 저장...
    $users = User::factory()->count(3)->create();

    // 테스트에서 모델 사용...
}
```

`create` 메서드에도 속성 배열을 전달해 기본 속성을 재정의할 수 있습니다:

```
$user = User::factory()->create([
    'name' => 'Abigail',
]);
```

<a name="sequences"></a>
### 시퀀스 (Sequences)

각 생성된 모델마다 특정 속성 값을 번갈아 가며 바꾸고 싶을 때, 시퀀스 상태 변환을 사용할 수 있습니다. 예를 들어, `admin` 컬럼 값을 `Y`와 `N`으로 번갈아 설정한다고 할 때 다음과 같이 작성합니다:

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

위 예제에서 10명의 유저 중 5명은 `admin`이 `Y`이고, 나머지 5명은 `N`으로 생성됩니다.

필요하다면 시퀀스 값으로 클로저를 포함할 수 있는데, 시퀀스가 새 값을 요구할 때마다 클로저가 호출됩니다:

```
$users = User::factory()
                ->count(10)
                ->state(new Sequence(
                    fn ($sequence) => ['role' => UserRoles::all()->random()],
                ))
                ->create();
```

시퀀스 클로저 내에서는 주입된 시퀀스 인스턴스의 `$index` (현재까지 반복 횟수)와 `$count` (전체 반복 횟수)를 사용할 수 있습니다:

```
$users = User::factory()
                ->count(10)
                ->sequence(fn ($sequence) => ['name' => 'Name '.$sequence->index])
                ->create();
```

<a name="factory-relationships"></a>
## 팩토리 관계 설정 (Factory Relationships)

<a name="has-many-relationships"></a>
### Has Many 관계 (Has Many Relationships)

다음으로, Laravel의 유창한 팩토리 메서드를 사용해 Eloquent 모델 관계를 설정해 보겠습니다. 예를 들어, 애플리케이션에 `App\Models\User` 모델과 `App\Models\Post` 모델이 있으며, `User` 모델이 `Post` 모델과 `hasMany` 관계를 가진다고 가정합니다. 다음과 같이 `has` 메서드를 사용해 3개의 게시물이 있는 사용자를 생성할 수 있습니다. `has` 메서드는 팩토리 인스턴스를 인수로 받습니다:

```
use App\Models\Post;
use App\Models\User;

$user = User::factory()
            ->has(Post::factory()->count(3))
            ->create();
```

규칙상 `Post` 모델을 `has`에 넘기면 Laravel은 `User` 모델에 `posts` 메서드가 있어야 한다고 가정합니다. 필요하면 관계 이름을 명시적으로 지정할 수 있습니다:

```
$user = User::factory()
            ->has(Post::factory()->count(3), 'posts')
            ->create();
```

관련 모델에 상태 변환을 적용할 수도 있고, 부모 모델에 접근해야 하는 상태 변환은 클로저로 전달할 수 있습니다:

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
#### 매직 메서드 사용하기 (Using Magic Methods)

좀 더 편리하게도, Laravel은 매직 팩토리 관계 메서드를 제공해 관계를 쉽게 생성할 수 있습니다. 예를 들어, 아래 코드는 `User` 모델의 `posts` 관계를 통해 관련 모델들을 생성합니다:

```
$user = User::factory()
            ->hasPosts(3)
            ->create();
```

이때, 관련 모델에 재정의할 속성 배열을 전달할 수도 있습니다:

```
$user = User::factory()
            ->hasPosts(3, [
                'published' => false,
            ])
            ->create();
```

부모 모델에 접근이 필요한 상태 변환 역시 클로저로 제공 가능합니다:

```
$user = User::factory()
            ->hasPosts(3, function (array $attributes, User $user) {
                return ['user_type' => $user->type];
            })
            ->create();
```

<a name="belongs-to-relationships"></a>
### Belongs To 관계 (Belongs To Relationships)

앞서 "has many" 관계 생성법을 알아봤으니, 이번엔 그 반대 방향 관계를 살펴봅니다. `for` 메서드를 사용해 팩토리가 생성하는 모델이 속한 부모 모델을 지정할 수 있습니다. 예를 들어, 3개의 `App\Models\Post` 인스턴스가 단일 사용자 소유로 생성되도록 할 수 있습니다:

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

이미 존재하는 부모 모델 인스턴스를 연결하고 싶다면, 그 인스턴스를 `for`에 넘기면 됩니다:

```
$user = User::factory()->create();

$posts = Post::factory()
            ->count(3)
            ->for($user)
            ->create();
```

<a name="belongs-to-relationships-using-magic-methods"></a>
#### 매직 메서드 사용하기 (Using Magic Methods)

마찬가지로 매직 팩토리 관계 메서드를 사용해 편리하게 "belongs to" 관계를 정의할 수 있습니다. 예를 들어, 다음 코드는 `Post` 모델의 `user` 관계에 따른 소유자를 지정합니다:

```
$posts = Post::factory()
            ->count(3)
            ->forUser([
                'name' => 'Jessica Archer',
            ])
            ->create();
```

<a name="many-to-many-relationships"></a>
### Many To Many 관계 (Many To Many Relationships)

[Has many 관계](#has-many-relationships)처럼 "many to many" 관계도 `has` 메서드를 사용해 생성할 수 있습니다:

```
use App\Models\Role;
use App\Models\User;

$user = User::factory()
            ->has(Role::factory()->count(3))
            ->create();
```

<a name="pivot-table-attributes"></a>
#### 피벗 테이블 속성 (Pivot Table Attributes)

두 모델을 연결하는 피벗(중간) 테이블에 설정할 속성이 필요하면, `hasAttached` 메서드를 사용하세요. 이 메서드는 두 번째 인수로 피벗 테이블 속성 배열을 받습니다:

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

관련 모델에 상태 변환이 필요한 경우, 클로저를 통한 상태 조작도 가능합니다:

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

이미 생성된 모델 인스턴스를 연결하고 싶다면 그 인스턴스들을 `hasAttached`에 넘길 수 있습니다. 아래 예시는 같은 세 가지 역할을 세 명의 사용자에게 각각 연결합니다:

```
$roles = Role::factory()->count(3)->create();

$user = User::factory()
            ->count(3)
            ->hasAttached($roles, ['active' => true])
            ->create();
```

<a name="many-to-many-relationships-using-magic-methods"></a>
#### 매직 메서드 사용하기 (Using Magic Methods)

마찬가지로 매직 메서드를 사용해 `many to many` 관계도 간편하게 정의할 수 있습니다. 아래 코드는 `User` 모델의 `roles` 관계를 통해 역할을 생성합니다:

```
$user = User::factory()
            ->hasRoles(1, [
                'name' => 'Editor'
            ])
            ->create();
```

<a name="polymorphic-relationships"></a>
### 다형성 관계 (Polymorphic Relationships)

[다형성 관계](/docs/{{version}}/eloquent-relationships#polymorphic-relationships)도 팩토리를 사용해 생성할 수 있습니다. 다형성 "morph many" 관계는 기본 "has many" 관계와 같은 방식으로 생성됩니다. 예를 들어, `App\Models\Post` 모델이 `morphMany` 관계로 `App\Models\Comment` 모델과 연결된 경우:

```
use App\Models\Post;

$post = Post::factory()->hasComments(3)->create();
```

<a name="morph-to-relationships"></a>
#### Morph To 관계

`morphTo` 관계는 매직 메서드를 사용할 수 없으며, 대신 `for` 메서드를 직접 호출하고 관계 이름을 명시해야 합니다. 예를 들어, `Comment` 모델이 `commentable`이라는 `morphTo` 관계를 가진다면, `for` 메서드를 통해 다음과 같이 단일 게시물에 소속된 댓글 3개를 생성할 수 있습니다:

```
$comments = Comment::factory()->count(3)->for(
    Post::factory(), 'commentable'
)->create();
```

<a name="polymorphic-many-to-many-relationships"></a>
#### 다형성 Many To Many 관계

다형성 "many to many" (`morphToMany` / `morphedByMany`) 관계 역시 일반 many to many 관계처럼 생성할 수 있습니다:

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

물론 `has` 매직 메서드로도 다형성 many to many 관계를 생성할 수 있습니다:

```
$videos = Video::factory()
            ->hasTags(3, ['public' => true])
            ->create();
```

<a name="defining-relationships-within-factories"></a>
### 팩토리 내에서 관계 정의하기 (Defining Relationships Within Factories)

팩토리 내에서 관계를 정의할 때 보통 외래 키 필드에 새 팩토리 인스턴스를 할당합니다. 이 방식은 주로 `belongsTo`나 `morphTo` 같은 역방향 관계에 사용됩니다. 예를 들어, 게시물을 생성할 때 새 사용자를 함께 생성하려면 다음과 같이 합니다:

```
use App\Models\User;

/**
 * 모델의 기본 상태 정의.
 *
 * @return array
 */
public function definition()
{
    return [
        'user_id' => User::factory(),
        'title' => $this->faker->title(),
        'content' => $this->faker->paragraph(),
    ];
}
```

관계 컬럼이 팩토리 평가 결과에 따라 달라진다면, 속성에 클로저를 할당할 수 있습니다. 클로저는 평가된 속성 배열을 인수로 받습니다:

```
/**
 * 모델의 기본 상태 정의.
 *
 * @return array
 */
public function definition()
{
    return [
        'user_id' => User::factory(),
        'user_type' => function (array $attributes) {
            return User::find($attributes['user_id'])->type;
        },
        'title' => $this->faker->title(),
        'content' => $this->faker->paragraph(),
    ];
}
```

<a name="running-seeders"></a>
## 시더 실행하기 (Running Seeders)

기능 테스트 중 [데이터베이스 시더](/docs/{{version}}/seeding)를 사용해 데이터베이스에 데이터를 채우고 싶다면, `seed` 메서드를 호출하세요. 기본적으로 `seed`는 모든 시더를 실행하는 `DatabaseSeeder`를 실행합니다. 특정 시더 클래스를 실행하고 싶을 땐 클래스명을 전달하면 됩니다:

```
<?php

namespace Tests\Feature;

use Database\Seeders\OrderStatusSeeder;
use Database\Seeders\TransactionStatusSeeder;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    use RefreshDatabase;

    /**
     * 새 주문 생성 테스트.
     *
     * @return void
     */
    public function test_orders_can_be_created()
    {
        // 기본 DatabaseSeeder 실행...
        $this->seed();

        // 특정 시더 실행...
        $this->seed(OrderStatusSeeder::class);

        // ...

        // 여러 시더 실행...
        $this->seed([
            OrderStatusSeeder::class,
            TransactionStatusSeeder::class,
            // ...
        ]);
    }
}
```

또한, `RefreshDatabase` 트레이트를 사용하는 모든 테스트마다 자동으로 시더를 실행하도록 설정할 수 있습니다. 기본 테스트 클래스에 `$seed` 속성을 추가하면 됩니다:

```
<?php

namespace Tests;

use Illuminate\Foundation\Testing\TestCase as BaseTestCase;

abstract class TestCase extends BaseTestCase
{
    use CreatesApplication;

    /**
     * 기본 시더를 각 테스트 전에 실행할지 여부.
     *
     * @var bool
     */
    protected $seed = true;
}
```

`$seed` 속성이 `true`일 때, `RefreshDatabase`가 적용된 테스트마다 `Database\Seeders\DatabaseSeeder`가 실행됩니다. 특정 시더만 실행하려면 테스트 클래스에 `$seeder` 속성을 정의하세요:

```
use Database\Seeders\OrderStatusSeeder;

/**
 * 각 테스트 전에 특정 시더 실행.
 *
 * @var string
 */
protected $seeder = OrderStatusSeeder::class;
```

<a name="available-assertions"></a>
## 사용 가능한 어서션 (Available Assertions)

Laravel은 [PHPUnit](https://phpunit.de/) 기능 테스트를 위한 여러 데이터베이스 어서션을 제공합니다. 아래에서 하나씩 살펴보겠습니다.

<a name="assert-database-count"></a>
#### assertDatabaseCount

특정 테이블에 주어진 개수만큼 레코드가 존재하는지 확인합니다:

```
$this->assertDatabaseCount('users', 5);
```

<a name="assert-database-has"></a>
#### assertDatabaseHas

특정 테이블에 주어진 키/값 조건과 일치하는 레코드가 있는지 확인합니다:

```
$this->assertDatabaseHas('users', [
    'email' => 'sally@example.com',
]);
```

<a name="assert-database-missing"></a>
#### assertDatabaseMissing

특정 테이블에 주어진 키/값 조건과 일치하는 레코드가 없는지 확인합니다:

```
$this->assertDatabaseMissing('users', [
    'email' => 'sally@example.com',
]);
```

<a name="assert-deleted"></a>
#### assertDeleted

특정 Eloquent 모델이 데이터베이스에서 삭제되었는지 확인합니다:

```
use App\Models\User;

$user = User::find(1);

$user->delete();

$this->assertDeleted($user);
```

`assertSoftDeleted` 메서드는 모델이 "소프트 삭제"되었음을 확인합니다:

```
$this->assertSoftDeleted($user);
```

<a name="assert-model-exists"></a>
#### assertModelExists

특정 모델이 데이터베이스에 존재하는지 확인합니다:

```
use App\Models\User;

$user = User::factory()->create();

$this->assertModelExists($user);
```

<a name="assert-model-missing"></a>
#### assertModelMissing

특정 모델이 데이터베이스에 존재하지 않는지 확인합니다:

```
use App\Models\User;

$user = User::factory()->create();

$user->delete();

$this->assertModelMissing($user);
```