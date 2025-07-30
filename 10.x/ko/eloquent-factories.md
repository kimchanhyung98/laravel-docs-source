# Eloquent: 팩토리 (Factories)

- [소개](#introduction)
- [모델 팩토리 정의하기](#defining-model-factories)
    - [팩토리 생성하기](#generating-factories)
    - [팩토리 상태(State)](#factory-states)
    - [팩토리 콜백(Callbacks)](#factory-callbacks)
- [팩토리를 사용해 모델 생성하기](#creating-models-using-factories)
    - [모델 인스턴스 생성하기](#instantiating-models)
    - [모델 영속화하기](#persisting-models)
    - [시퀀스(Sequences)](#sequences)
- [팩토리 관계(Relationships)](#factory-relationships)
    - [Has Many 관계](#has-many-relationships)
    - [Belongs To 관계](#belongs-to-relationships)
    - [Many to Many 관계](#many-to-many-relationships)
    - [다형성(Polymorphic) 관계](#polymorphic-relationships)
    - [팩토리 내에서 관계 정의하기](#defining-relationships-within-factories)
    - [관계에 기존 모델 재활용하기](#recycling-an-existing-model-for-relationships)

<a name="introduction"></a>
## 소개

애플리케이션을 테스트하거나 데이터베이스에 시드 데이터를 넣을 때, 데이터베이스에 몇 개의 레코드를 삽입할 필요가 있습니다. 각 컬럼 값을 직접 지정하는 대신, 라라벨은 [Eloquent 모델](/docs/10.x/eloquent)마다 기본 속성 집합을 모델 팩토리를 통해 정의할 수 있도록 합니다.

팩토리 작성 예시는 애플리케이션 내 `database/factories/UserFactory.php` 파일을 참고하세요. 이 팩토리는 모든 새 Laravel 애플리케이션에 기본 포함되어 있으며 다음과 같은 정의를 포함합니다:

```
namespace Database\Factories;

use Illuminate\Support\Str;
use Illuminate\Database\Eloquent\Factories\Factory;

class UserFactory extends Factory
{
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
            'password' => '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', // password
            'remember_token' => Str::random(10),
        ];
    }
}
```

기본적으로 팩토리는 Laravel의 기본 팩토리 클래스를 상속받는 클래스이며, `definition` 메서드를 통해 모델 생성 시 적용할 기본 속성값 집합을 반환합니다.

또한 `fake` 헬퍼를 통해 [Faker](https://github.com/FakerPHP/Faker) PHP 라이브러리를 사용할 수 있으며, 이를 통해 테스트 및 시드 데이터 생성에 다양한 종류의 임의 데이터를 편리하게 생성할 수 있습니다.

> [!NOTE]  
> `config/app.php` 설정 파일에 `faker_locale` 옵션을 추가하여 Faker의 로케일(locale)을 설정할 수 있습니다.

<a name="defining-model-factories"></a>
## 모델 팩토리 정의하기

<a name="generating-factories"></a>
### 팩토리 생성하기

팩토리를 생성하려면 `make:factory` Artisan 명령어를 실행하세요:

```shell
php artisan make:factory PostFactory
```

생성된 팩토리 클래스는 `database/factories` 디렉토리에 위치합니다.

<a name="factory-and-model-discovery-conventions"></a>
#### 모델 및 팩토리 자동 연결 규칙

팩토리를 정의한 후에는, 모델에 포함된 `Illuminate\Database\Eloquent\Factories\HasFactory` 트레이트가 제공하는 정적 `factory` 메서드를 통해 해당 모델의 팩토리 인스턴스를 생성할 수 있습니다.

`HasFactory` 트레이트의 `factory` 메서드는 규칙에 따라 적절한 팩토리를 탐색합니다. 기본적으로 `Database\Factories` 네임스페이스 내에서 모델명과 같은 이름에 `Factory`가 접미된 클래스를 찾습니다. 만약 이 규칙이 적용되지 않는 경우, 모델에서 `newFactory` 메서드를 재정의하여 직접 팩토리 인스턴스를 반환할 수 있습니다:

```
use Illuminate\Database\Eloquent\Factories\Factory;
use Database\Factories\Administration\FlightFactory;

/**
 * 모델에 대한 새 팩토리 인스턴스 생성
 */
protected static function newFactory(): Factory
{
    return FlightFactory::new();
}
```

그 후, 해당 팩토리 클래스 내에 `model` 속성을 정의하세요:

```
use App\Administration\Flight;
use Illuminate\Database\Eloquent\Factories\Factory;

class FlightFactory extends Factory
{
    /**
     * 팩토리가 대응하는 모델 이름
     *
     * @var class-string<\Illuminate\Database\Eloquent\Model>
     */
    protected $model = Flight::class;
}
```

<a name="factory-states"></a>
### 팩토리 상태(State)

상태(State) 조작 메서드는 팩토리에 적용할 수 있는 개별적 변경 사항을 정의할 때 사용합니다. 예를 들어 `Database\Factories\UserFactory`에 `suspended` 상태 메서드를 추가하여 기본 속성 중 하나를 변경할 수 있습니다.

보통 상태 메서드는 Laravel 기본 팩토리 클래스가 제공하는 `state` 메서드를 호출합니다. `state`는 팩토리의 순수 속성 배열을 인자로 받아 변경할 속성 배열을 반환하는 클로저를 전달받습니다:

```
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * 사용자의 정지(suspended) 상태를 나타냄
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
#### "Soft Deleted(휴지통)" 상태

만약 모델에서 [소프트 삭제(soft delete)](/docs/10.x/eloquent#soft-deleting)를 지원한다면, 내장된 `trashed` 상태 메서드를 호출해 이미 "소프트 삭제"된 상태로 모델을 생성할 수 있습니다. 이 `trashed` 상태 메서드는 모든 팩토리에 자동 제공되므로 별도 정의가 필요 없습니다:

```
use App\Models\User;

$user = User::factory()->trashed()->create();
```

<a name="factory-callbacks"></a>
### 팩토리 콜백(Callbacks)

팩토리 콜백은 `afterMaking` 또는 `afterCreating` 메서드로 등록하며, 모델이 만들어지거나 생성된 후 추가 작업을 수행할 때 사용합니다. 이러한 콜백은 팩토리 클래스 내 `configure` 메서드를 정의해 자동으로 등록하는 방식을 권장합니다. `configure` 메서드는 팩토리 인스턴스 생성 시 Laravel에 의해 호출됩니다:

```
namespace Database\Factories;

use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;

class UserFactory extends Factory
{
    /**
     * 팩토리 구성 메서드
     */
    public function configure(): static
    {
        return $this->afterMaking(function (User $user) {
            // 모델이 만들어진 후 실행할 작업
        })->afterCreating(function (User $user) {
            // 모델이 데이터베이스에 저장된 후 실행할 작업
        });
    }

    // ...
}
```

상태 메서드 내에서도 콜백을 등록할 수 있습니다. 이는 특정 상태일 때만 실행되는 추가 작업을 정의할 때 유용합니다:

```
use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * 사용자의 정지 상태를 나타냄
 */
public function suspended(): Factory
{
    return $this->state(function (array $attributes) {
        return [
            'account_status' => 'suspended',
        ];
    })->afterMaking(function (User $user) {
        // 상태별 추가 작업(모델 생성 후)
    })->afterCreating(function (User $user) {
        // 상태별 추가 작업(모델 저장 후)
    });
}
```

<a name="creating-models-using-factories"></a>
## 팩토리를 사용해 모델 생성하기

<a name="instantiating-models"></a>
### 모델 인스턴스 생성하기

팩토리를 정의했다면, `Illuminate\Database\Eloquent\Factories\HasFactory` 트레이트가 모델에 제공하는 정적 `factory` 메서드를 사용해 해당 모델 팩토리 인스턴스를 생성할 수 있습니다. 다음 예시는 `make` 메서드를 활용해 데이터베이스에 저장하지 않고 모델 인스턴스를 만드는 방법입니다:

```
use App\Models\User;

$user = User::factory()->make();
```

`count` 메서드를 사용하면 여러 개의 모델 컬렉션을 생성할 수 있습니다:

```
$users = User::factory()->count(3)->make();
```

<a name="applying-states"></a>
#### 상태 적용하기

팩토리에서 정의한 [상태(State)](#factory-states)를 모델에 적용할 수도 있습니다. 여러 상태를 한 번에 적용하고 싶다면 상태 변환 메서드를 연달아 호출하면 됩니다:

```
$users = User::factory()->count(5)->suspended()->make();
```

<a name="overriding-attributes"></a>
#### 속성 재정의하기

기본값 중 일부만 변경하고 싶다면 `make` 메서드에 속성 배열을 넘겨 재정의할 수 있습니다. 지정한 속성만 바뀌고, 나머지는 팩토리 기본값이 유지됩니다:

```
$user = User::factory()->make([
    'name' => 'Abigail Otwell',
]);
```

또는 `state` 메서드를 직접 호출하여 인라인 상태 변환도 가능합니다:

```
$user = User::factory()->state([
    'name' => 'Abigail Otwell',
])->make();
```

> [!NOTE]  
> 팩토리를 통해 모델을 생성할 때는 [대량 할당 보호](/docs/10.x/eloquent#mass-assignment)가 자동으로 비활성화됩니다.

<a name="persisting-models"></a>
### 모델 영속화하기

`create` 메서드는 모델 인스턴스를 생성하고 Eloquent의 `save` 메서드를 사용해 데이터베이스에 저장합니다:

```
use App\Models\User;

// 단일 User 인스턴스 생성 및 저장
$user = User::factory()->create();

// 세 개의 User 인스턴스 생성 및 저장
$users = User::factory()->count(3)->create();
```

`create` 메서드에도 속성 배열을 전달해 기본값을 재정의할 수 있습니다:

```
$user = User::factory()->create([
    'name' => 'Abigail',
]);
```

<a name="sequences"></a>
### 시퀀스(Sequences)

모델 생성 시 특정 속성값을 번갈아 사용하고 싶을 때 시퀀스 상태 변환을 활용할 수 있습니다. 예를 들어, `admin` 컬럼을 생성된 사용자마다 `Y`와 `N`으로 번갈아 지정하려면 다음과 같이 작성합니다:

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

위 예시에서는 `admin` 값이 `Y`인 사용자가 5명, `N`인 사용자가 5명 생성됩니다.

필요하다면 시퀀스 값으로 클로저를 사용할 수 있습니다. 이 클로저는 시퀀스가 새 값을 필요로 할 때마다 호출됩니다:

```
use Illuminate\Database\Eloquent\Factories\Sequence;

$users = User::factory()
                ->count(10)
                ->state(new Sequence(
                    fn (Sequence $sequence) => ['role' => UserRoles::all()->random()],
                ))
                ->create();
```

시퀀스 클로저 내에서는 주입된 `$sequence` 인스턴스의 `$index` 또는 `$count` 프로퍼티에 접근할 수 있습니다. `$index`는 지금까지 반복한 횟수, `$count`는 시퀀스가 호출될 총 횟수를 뜻합니다:

```
$users = User::factory()
                ->count(10)
                ->sequence(fn (Sequence $sequence) => ['name' => 'Name '.$sequence->index])
                ->create();
```

편의를 위해 `sequence` 메서드는 내부적으로 `state` 메서드를 호출합니다. `sequence`는 클로저 또는 배열로 시퀀스 속성들을 받습니다:

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
## 팩토리 관계(Relationships)

<a name="has-many-relationships"></a>
### Has Many 관계

다음으로, Laravel 팩토리의 체인 메서드를 이용해 Eloquent 모델 관계를 어떻게 구성하는지 살펴보겠습니다. 예를 들어, 애플리케이션에 `App\Models\User` 모델과 `App\Models\Post` 모델이 있고, `User`가 `hasMany` 관계로 `Post`를 소유한다고 합시다. `has` 메서드를 이용해 3개의 게시글을 가진 사용자를 생성할 수 있습니다. `has` 메서드는 팩토리 인스턴스를 인자로 받습니다:

```
use App\Models\Post;
use App\Models\User;

$user = User::factory()
            ->has(Post::factory()->count(3))
            ->create();
```

관례에 따라 `has` 메서드에 `Post` 모델 팩토리를 전달하면, Laravel은 `User` 모델에 `posts` 메서드가 있어야 한다고 가정해 관계를 맺습니다. 필요하면 두 번째 인자로 관계 메서드명을 명시적으로 지정할 수도 있습니다:

```
$user = User::factory()
            ->has(Post::factory()->count(3), 'posts')
            ->create();
```

관련 모델에 상태 변환을 적용할 수도 있고, 부모 모델에 접근하는 클로저형 상태 변환도 가능합니다:

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

Laravel은 팩토리 관계용 매직 메서드도 제공합니다. 예를 들어 다음 코드는 `User` 모델의 `posts` 관계를 통해 게시글 모델들을 쉽게 생성합니다:

```
$user = User::factory()
            ->hasPosts(3)
            ->create();
```

매직 메서드에는 관계 모델들의 속성을 재정의할 배열을 넘길 수도 있습니다:

```
$user = User::factory()
            ->hasPosts(3, [
                'published' => false,
            ])
            ->create();
```

부모 모델에 접근해야 하는 상태 변환도 클로저로 줄 수 있습니다:

```
$user = User::factory()
            ->hasPosts(3, function (array $attributes, User $user) {
                return ['user_type' => $user->type];
            })
            ->create();
```

<a name="belongs-to-relationships"></a>
### Belongs To 관계

이번에는 `has many` 관계의 반대 방향인 `belongsTo` 관계에 대해 알아보겠습니다. `for` 메서드는 팩토리 생성 모델이 속한 부모 모델을 정의하는 데 사용됩니다. 예를 들어, 단일 사용자에게 속한 3개의 게시글을 생성할 때 다음과 같이 작성합니다:

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

이미 부모 모델 인스턴스가 있는 경우 `for`에 전달하여 관계를 설정할 수 있습니다:

```
$user = User::factory()->create();

$posts = Post::factory()
            ->count(3)
            ->for($user)
            ->create();
```

<a name="belongs-to-relationships-using-magic-methods"></a>
#### 매직 메서드 사용하기

`belongsTo` 관계도 매직 메서드를 사용할 수 있습니다. 다음 코드는 `Post` 모델의 `user` 관계로 세 개의 게시글을 생성합니다:

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

[Has many 관계](#has-many-relationships)와 비슷하게, "many to many" 관계도 `has` 메서드를 통해 생성할 수 있습니다:

```
use App\Models\Role;
use App\Models\User;

$user = User::factory()
            ->has(Role::factory()->count(3))
            ->create();
```

<a name="pivot-table-attributes"></a>
#### Pivot 테이블 속성

중간 테이블(pivot table)에 설정할 속성이 필요한 경우 `hasAttached` 메서드를 사용하세요. 이 메서드는 두 번째 인자로 pivot 테이블의 필드 이름과 값을 담은 배열을 받습니다:

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

만약 상태 변환에서 관련 모델에 접근해야 할 경우 클로저를 전달해 상태를 정의할 수도 있습니다:

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

이미 생성된 여러 모델을 연결하려면 해당 모델 인스턴스 컬렉션을 `hasAttached`에 넘기면 됩니다. 아래 예시에서 세 개의 역할을 세 명의 사용자에게 각각 연결합니다:

```
$roles = Role::factory()->count(3)->create();

$user = User::factory()
            ->count(3)
            ->hasAttached($roles, ['active' => true])
            ->create();
```

<a name="many-to-many-relationships-using-magic-methods"></a>
#### 매직 메서드 사용하기

다대다 관계도 매직 팩토리 메서드를 사용할 수 있습니다. 다음은 `User` 모델의 `roles` 관계를 통해 역할을 생성하는 예시입니다:

```
$user = User::factory()
            ->hasRoles(1, [
                'name' => 'Editor'
            ])
            ->create();
```

<a name="polymorphic-relationships"></a>
### 다형성(Polymorphic) 관계

[다형성 관계](/docs/10.x/eloquent-relationships#polymorphic-relationships) 역시 팩토리를 통해 생성할 수 있습니다. 다형성 "morph many" 관계는 일반적인 "has many" 관계 생성과 동일합니다. 예를 들어 `App\Models\Post` 모델이 `App\Models\Comment` 모델과 `morphMany` 관계를 가진다면:

```
use App\Models\Post;

$post = Post::factory()->hasComments(3)->create();
```

<a name="morph-to-relationships"></a>
#### Morph To 관계

`morphTo` 관계는 매직 메서드를 사용할 수 없고, 대신 `for` 메서드를 직접 명시적으로 호출해야 합니다. 예를 들어, `Comment` 모델에 `commentable`이라는 `morphTo` 관계가 있다면, 다음과 같이 단일 게시글에 속하는 3개의 댓글을 생성합니다:

```
$comments = Comment::factory()->count(3)->for(
    Post::factory(), 'commentable'
)->create();
```

<a name="polymorphic-many-to-many-relationships"></a>
#### 다형성 다대다 관계

다형성 "many to many" (`morphToMany` / `morphedByMany`) 관계도 일반적인 many to many 관계와 동일하게 생성할 수 있습니다:

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

물론 매직 `has` 메서드로도 다형성 many to many 관계를 생성할 수 있습니다:

```
$videos = Video::factory()
            ->hasTags(3, ['public' => true])
            ->create();
```

<a name="defining-relationships-within-factories"></a>
### 팩토리 내에서 관계 정의하기

모델 팩토리 내에서 관계를 정의할 때 일반적으로 외래 키 컬럼에 새 팩토리 인스턴스를 할당합니다. 보통은 `belongsTo` 또는 `morphTo` 같은 "역방향" 관계에 해당합니다. 예를 들어 게시글 생성 시 새 사용자도 함께 생성하려면 아래처럼 작성합니다:

```
use App\Models\User;

/**
 * 모델의 기본 상태 정의
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

만약 관계 컬럼이 팩토리가 정의하는 속성값에 따라 달라진다면, 클로저를 속성에 할당할 수도 있습니다. 이 클로저에는 팩토리에서 평가한 속성 배열이 전달됩니다:

```
/**
 * 모델의 기본 상태 정의
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
### 관계에 기존 모델 재활용하기

여러 모델이 공통된 관계 모델을 공유하는 경우, `recycle` 메서드를 사용해 팩토리가 관계 모델 인스턴스를 재활용하도록 할 수 있습니다.

예를 들어 `Airline`, `Flight`, `Ticket` 모델에서, 티켓은 항공사와 비행기에 속하며, 비행기도 항공사에 속하는 상황이라면, 티켓을 생성할 때 티켓과 비행기 모두 같은 항공사를 공유하도록 `recycle` 메서드에 항공사 인스턴스를 전달할 수 있습니다:

```
Ticket::factory()
    ->recycle(Airline::factory()->create())
    ->create();
```

`recycle`은 동일 사용자나 팀에 속한 모델을 다룰 때 특히 유용합니다.

`recycle`은 기존 모델 컬렉션도 받을 수 있습니다. 이 경우 컬렉션에서 무작위 모델을 골라 사용합니다:

```
Ticket::factory()
    ->recycle($airlines)
    ->create();
```
