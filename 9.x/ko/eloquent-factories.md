# Eloquent: 팩토리 (Factories)

- [소개](#introduction)
- [모델 팩토리 정의하기](#defining-model-factories)
    - [팩토리 생성하기](#generating-factories)
    - [팩토리 상태(States)](#factory-states)
    - [팩토리 콜백(Callbacks)](#factory-callbacks)
- [팩토리를 사용해 모델 생성하기](#creating-models-using-factories)
    - [모델 인스턴스 만들기](#instantiating-models)
    - [모델 저장하기](#persisting-models)
    - [시퀀스(Sequences)](#sequences)
- [팩토리 관계(Factory Relationships)](#factory-relationships)
    - [Has Many 관계](#has-many-relationships)
    - [Belongs To 관계](#belongs-to-relationships)
    - [Many To Many 관계](#many-to-many-relationships)
    - [다형성 관계(Polymorphic Relationships)](#polymorphic-relationships)
    - [팩토리 내에서 관계 정의하기](#defining-relationships-within-factories)
    - [관계를 위한 기존 모델 재활용하기](#recycling-an-existing-model-for-relationships)

<a name="introduction"></a>
## 소개 (Introduction)

애플리케이션 테스트나 데이터베이스 시딩 시, 데이터베이스에 몇 개의 레코드를 삽입해야 할 때가 있습니다. 각 컬럼의 값을 일일이 지정하는 대신, Laravel에서는 각 [Eloquent 모델](/docs/9.x/eloquent) 별로 모델 팩토리를 정의하여 기본 속성 값 세트를 설정할 수 있습니다.

팩토리 작성 방법 예시는 애플리케이션의 `database/factories/UserFactory.php` 파일을 참고하세요. 이 팩토리는 모든 새 Laravel 애플리케이션에 기본 포함되며 다음과 같은 팩토리 정의를 담고 있습니다:

```php
namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;
use Illuminate\Support\Str;

class UserFactory extends Factory
{
    /**
     * Define the model's default state.
     *
     * @return array
     */
    public function definition()
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

기본적으로 팩토리는 Laravel의 기본 팩토리 클래스를 상속한 클래스이며, `definition` 메서드를 정의합니다. `definition` 메서드는 팩토리를 통해 모델을 생성할 때 적용할 기본 속성 값의 세트를 배열로 반환합니다.

`fake` 헬퍼를 이용해 팩토리는 [Faker](https://github.com/FakerPHP/Faker) PHP 라이브러리에 접근할 수 있어, 테스트와 시딩에 다양한 종류의 랜덤 데이터를 쉽게 생성할 수 있습니다.

> [!NOTE]
> `config/app.php` 설정 파일에 `faker_locale` 옵션을 추가하여 애플리케이션의 Faker 로케일을 설정할 수 있습니다.

<a name="defining-model-factories"></a>
## 모델 팩토리 정의하기 (Defining Model Factories)

<a name="generating-factories"></a>
### 팩토리 생성하기 (Generating Factories)

팩토리를 생성하려면 다음 `make:factory` [Artisan 명령어](/docs/9.x/artisan)를 실행하세요:

```shell
php artisan make:factory PostFactory
```

생성된 새 팩토리 클래스는 `database/factories` 디렉토리에 저장됩니다.

<a name="factory-and-model-discovery-conventions"></a>
#### 모델 및 팩토리 탐색 규칙 (Model & Factory Discovery Conventions)

팩토리를 정의한 후, `Illuminate\Database\Eloquent\Factories\HasFactory` 트레이트가 모델에 제공하는 정적 `factory` 메서드를 사용해 해당 모델 팩토리 인스턴스를 만들 수 있습니다.

`HasFactory` 트레이트의 `factory` 메서드는 규칙에 따라 해당 모델에 적절한 팩토리를 찾습니다. 구체적으로, `Database\Factories` 네임스페이스 내에 모델명과 같은 이름이면서 `Factory` 접미사가 붙은 클래스를 탐색합니다. 만약 이런 규칙이 애플리케이션 또는 팩토리에 맞지 않는 경우, 모델에 `newFactory` 메서드를 오버라이드하여 직접 팩토리 인스턴스를 반환할 수 있습니다:

```php
use Database\Factories\Administration\FlightFactory;

/**
 * 모델에 대한 새로운 팩토리 인스턴스를 생성합니다.
 *
 * @return \Illuminate\Database\Eloquent\Factories\Factory
 */
protected static function newFactory()
{
    return FlightFactory::new();
}
```

다음으로, 해당 팩토리에 `model` 속성을 정의하세요:

```php
use App\Administration\Flight;
use Illuminate\Database\Eloquent\Factories\Factory;

class FlightFactory extends Factory
{
    /**
     * 팩토리가 대응하는 모델 이름입니다.
     *
     * @var string
     */
    protected $model = Flight::class;
}
```

<a name="factory-states"></a>
### 팩토리 상태 (Factory States)

상태 변환 메서드는 모델 팩토리에 적용할 수 있는 개별 수정 사항을 정의합니다. 예를 들어, `Database\Factories\UserFactory`에 `suspended` 상태 메서드를 정의하여 특정 기본 속성 값을 변경할 수 있습니다.

상태 변환 메서드는 보통 Laravel 기본 팩토리 클래스의 `state` 메서드를 호출합니다. `state` 메서드는 배열 속성을 인수로 받는 클로저를 인자로 받아, 수정할 속성 배열을 반환해야 합니다:

```php
/**
 * 사용자가 정지된 상태임을 나타냅니다.
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

#### "삭제된 상태(Trashed)" 상태

Eloquent 모델이 [소프트 삭제](/docs/9.x/eloquent#soft-deleting)를 지원한다면, 내장된 `trashed` 상태 메서드를 사용해 생성된 모델이 이미 "소프트 삭제"된 상태임을 표시할 수 있습니다. `trashed` 상태는 모든 팩토리에 자동으로 제공되므로 별도로 정의할 필요가 없습니다:

```php
use App\Models\User;

$user = User::factory()->trashed()->create();
```

<a name="factory-callbacks"></a>
### 팩토리 콜백 (Factory Callbacks)

팩토리 콜백은 `afterMaking` 및 `afterCreating` 메서드를 사용해 등록할 수 있으며, 모델을 생성 또는 저장 후 추가 작업을 수행하도록 합니다. 콜백은 팩토리 클래스에 `configure` 메서드를 정의해 등록하는데, 이 메서드는 팩토리 인스턴스 생성 시 Laravel이 자동 호출합니다:

```php
namespace Database\Factories;

use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;
use Illuminate\Support\Str;

class UserFactory extends Factory
{
    /**
     * 모델 팩토리를 설정합니다.
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
## 팩토리를 사용해 모델 생성하기 (Creating Models Using Factories)

<a name="instantiating-models"></a>
### 모델 인스턴스 만들기 (Instantiating Models)

팩토리를 정의한 후, `Illuminate\Database\Eloquent\Factories\HasFactory` 트레이트가 제공하는 정적 `factory` 메서드를 사용해 해당 모델 팩토리 인스턴스를 만들 수 있습니다. 몇 가지 예제를 살펴보겠습니다. 먼저, `make` 메서드를 사용해 데이터베이스에 저장하지 않고 모델 인스턴스를 만듭니다:

```php
use App\Models\User;

$user = User::factory()->make();
```

`count` 메서드를 이용하면 여러 모델을 컬렉션으로 만들 수 있습니다:

```php
$users = User::factory()->count(3)->make();
```

<a name="applying-states"></a>
#### 상태 적용하기

정의한 [상태](#factory-states)를 모델에 적용할 수도 있습니다. 여러 상태를 적용하려면 상태 변환 메서드를 연이어 호출하면 됩니다:

```php
$users = User::factory()->count(5)->suspended()->make();
```

<a name="overriding-attributes"></a>
#### 속성 재정의하기

기본값 중 일부를 재정의하려면 `make` 메서드에 배열을 인자로 넘기세요. 배열에 명시한 속성만 교체되고 나머지는 팩토리에서 지정한 기본값으로 유지됩니다:

```php
$user = User::factory()->make([
    'name' => 'Abigail Otwell',
]);
```

또는 팩토리 인스턴스에서 `state` 메서드를 호출하여 인라인 상태 변환을 수행할 수 있습니다:

```php
$user = User::factory()->state([
    'name' => 'Abigail Otwell',
])->make();
```

> [!NOTE]
> 팩토리를 사용해 모델을 생성할 때는 [대량 할당 방지(mass assignment protection)](/docs/9.x/eloquent#mass-assignment)가 자동으로 비활성화됩니다.

<a name="persisting-models"></a>
### 모델 저장하기 (Persisting Models)

`create` 메서드는 모델 인스턴스를 생성하고, Eloquent의 `save` 메서드를 통해 데이터베이스에 저장합니다:

```php
use App\Models\User;

// 단일 App\Models\User 인스턴스 생성
$user = User::factory()->create();

// 세 명의 App\Models\User 인스턴스 생성
$users = User::factory()->count(3)->create();
```

또한 `create` 메서드에 속성 배열을 넘겨 팩토리 기본 속성을 덮어쓸 수 있습니다:

```php
$user = User::factory()->create([
    'name' => 'Abigail',
]);
```

<a name="sequences"></a>
### 시퀀스 (Sequences)

때로는 생성되는 모델마다 특정 속성 값을 번갈아가며 부여하고 싶을 수 있습니다. 이럴 때 상태 변환을 시퀀스로 정의할 수 있습니다. 예를 들어, 생성되는 사용자 모델의 `admin` 컬럼이 `Y`와 `N`으로 번갈아가며 설정되도록 할 수 있습니다:

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

이 예에서 10명 중 5명은 `admin` 값이 `Y`, 나머지 5명은 `N`이 됩니다.

필요에 따라 시퀀스값에 클로저를 포함할 수도 있습니다. 클로저는 새로운 값이 필요할 때마다 실행됩니다:

```php
$users = User::factory()
                ->count(10)
                ->state(new Sequence(
                    fn ($sequence) => ['role' => UserRoles::all()->random()],
                ))
                ->create();
```

시퀀스 클로저 내부에서는 주입된 시퀀스 인스턴스의 `$index`와 `$count` 속성에 접근할 수 있습니다. `$index`는 현재까지 반복 횟수, `$count`는 시퀀스가 호출될 총 횟수를 의미합니다:

```php
$users = User::factory()
                ->count(10)
                ->sequence(fn ($sequence) => ['name' => 'Name '.$sequence->index])
                ->create();
```

편의상 시퀀스는 내부적으로 `state` 메서드를 호출하는 `sequence` 메서드를 이용해 적용할 수도 있습니다. `sequence` 메서드는 클로저 또는 배열 형태로 시퀀스화된 속성을 인자로 받습니다:

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
### Has Many 관계

이제 Laravel의 유창한 팩토리 메서드를 이용해 Eloquent 모델 관계를 구성하는 방법을 살펴보겠습니다. 예를 들어, `App\Models\User`와 `App\Models\Post` 모델이 있고, `User` 모델이 `Post` 모델과 `hasMany` 관계를 정의한다고 가정합시다. `User`가 세 개의 게시글을 갖도록 하려면, 팩토리의 `has` 메서드를 이용해 게시글 팩토리 인스턴스를 전달하면 됩니다:

```php
use App\Models\Post;
use App\Models\User;

$user = User::factory()
            ->has(Post::factory()->count(3))
            ->create();
```

규칙상 `has` 메서드에 `Post` 모델을 전달하면, Laravel은 `User` 모델이 관계를 정의하는 `posts` 메서드를 갖고 있다고 가정합니다. 만약 관계명을 명시적으로 지정하고 싶다면 다음과 같이 할 수 있습니다:

```php
$user = User::factory()
            ->has(Post::factory()->count(3), 'posts')
            ->create();
```

물론 관련 모델에 상태 변환도 적용할 수 있습니다. 상태 변환 시 부모 모델에 대한 접근이 필요하면 클로저 기반 상태 변환도 전달할 수 있습니다:

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

편리하게 Laravel의 매직 팩토리 관계 메서드를 사용해 관계를 구축할 수 있습니다. 예를 들어, 다음 코드는 `User` 모델의 `posts` 관계 메서드가 관련 모델을 생성한다고 간주합니다:

```php
$user = User::factory()
            ->hasPosts(3)
            ->create();
```

매직 메서드 활용 시, 관련 모델 속성 오버라이드를 위한 배열을 전달할 수도 있습니다:

```php
$user = User::factory()
            ->hasPosts(3, [
                'published' => false,
            ])
            ->create();
```

부모 모델에 접근할 필요가 있으면 클로저 기반 상태 변환도 지정할 수 있습니다:

```php
$user = User::factory()
            ->hasPosts(3, function (array $attributes, User $user) {
                return ['user_type' => $user->type];
            })
            ->create();
```

<a name="belongs-to-relationships"></a>
### Belongs To 관계

"has many" 관계를 살펴봤으니 이번에는 반대 방향 관계를 살펴봅니다. `for` 메서드는 팩토리로 생성하는 모델이 속하는 부모 모델을 지정하는 데 사용됩니다. 예를 들어, 한 명의 사용자에게 속하는 세 개의 게시글을 생성할 수 있습니다:

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

이미 부모 모델 인스턴스가 있다면, 직접 `for` 메서드에 전달할 수도 있습니다:

```php
$user = User::factory()->create();

$posts = Post::factory()
            ->count(3)
            ->for($user)
            ->create();
```

<a name="belongs-to-relationships-using-magic-methods"></a>
#### 매직 메서드 활용하기

편의상, Laravel 매직 팩토리 관계 메서드를 사용해 `belongsTo` 관계를 정의할 수 있습니다. 예를 들어, 다음 코드는 3개의 게시글이 `Post` 모델의 `user` 관계에 속한다고 가정합니다:

```php
$posts = Post::factory()
            ->count(3)
            ->forUser([
                'name' => 'Jessica Archer',
            ])
            ->create();
```

<a name="many-to-many-relationships"></a>
### Many To Many 관계

[Has many 관계](#has-many-relationships)와 유사하게, `has` 메서드로 "many to many" 관계도 생성할 수 있습니다:

```php
use App\Models\Role;
use App\Models\User;

$user = User::factory()
            ->has(Role::factory()->count(3))
            ->create();
```

<a name="pivot-table-attributes"></a>
#### 피벗 테이블 속성 (Pivot Table Attributes)

모델을 연결하는 피벗(중간) 테이블에 설정할 속성이 있으면 `hasAttached` 메서드를 사용하세요. 두 번째 인수로 피벗 테이블 속성명 및 값을 배열로 넘깁니다:

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

상태 변환 클로저를 제공해 관련 모델에 대한 상태 변화를 지정할 수도 있습니다:

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

이미 연결할 모델 인스턴스가 있다면 `hasAttached`에 전달할 수도 있습니다. 이 예제에서 같은 3개의 역할이 모든 3명의 사용자에 연결됩니다:

```php
$roles = Role::factory()->count(3)->create();

$user = User::factory()
            ->count(3)
            ->hasAttached($roles, ['active' => true])
            ->create();
```

<a name="many-to-many-relationships-using-magic-methods"></a>
#### 매직 메서드 활용하기

매직 팩토리 관계 메서드로 many to many 관계를 정의할 수 있습니다. 예를 들어 다음 코드는 `User` 모델의 `roles` 관계 메서드를 사용해 관련 모델을 만듭니다:

```php
$user = User::factory()
            ->hasRoles(1, [
                'name' => 'Editor'
            ])
            ->create();
```

<a name="polymorphic-relationships"></a>
### 다형성 관계 (Polymorphic Relationships)

[다형성 관계](/docs/9.x/eloquent-relationships#polymorphic-relationships)도 팩토리를 사용해 생성할 수 있습니다. 다형성 "morph many" 관계는 일반 "has many" 관계와 동일하게 생성합니다. 예를 들어 `App\Models\Post` 모델이 `App\Models\Comment`와 `morphMany` 관계를 가진다고 하면 다음과 같이 작성합니다:

```php
use App\Models\Post;

$post = Post::factory()->hasComments(3)->create();
```

<a name="morph-to-relationships"></a>
#### Morph To 관계

`morphTo` 관계에 매직 메서드는 사용할 수 없으며, 대신 `for` 메서드를 직접 호출하고 관계 이름을 명시해야 합니다. 예를 들어, `Comment` 모델에 다형성 관계 `commentable`이 있다면, 3개의 댓글을 하나의 게시글에 속하도록 다음과 같이 생성할 수 있습니다:

```php
$comments = Comment::factory()->count(3)->for(
    Post::factory(), 'commentable'
)->create();
```

<a name="polymorphic-many-to-many-relationships"></a>
#### 다형성 Many To Many 관계

다형성 "many to many" (`morphToMany` / `morphedByMany`) 관계도 일반 "many to many" 관계와 동일하게 생성할 수 있습니다:

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

물론 `has` 매직 메서드도 다형성 "many to many" 관계에 사용할 수 있습니다:

```php
$videos = Video::factory()
            ->hasTags(3, ['public' => true])
            ->create();
```

<a name="defining-relationships-within-factories"></a>
### 팩토리 내에서 관계 정의하기 (Defining Relationships Within Factories)

모델 팩토리 내에서 관계를 정의하려면, 일반적으로 외래 키 컬럼에 새 팩토리 인스턴스를 할당합니다. 이 방법은 주로 `belongsTo`나 `morphTo` 같은 "역방향" 관계에 사용됩니다. 예를 들어, 게시글을 생성할 때 새로운 사용자를 같이 생성하려면 다음과 같이 합니다:

```php
use App\Models\User;

/**
 * 모델의 기본 상태를 정의합니다.
 *
 * @return array
 */
public function definition()
{
    return [
        'user_id' => User::factory(),
        'title' => fake()->title(),
        'content' => fake()->paragraph(),
    ];
}
```

관계 컬럼이 팩토리가 정의된 팩토리 속성에 의존한다면 클로저를 속성값으로 할당할 수 있습니다. 클로저는 팩토리 평가된 속성 배열을 인수로 받습니다:

```php
/**
 * 모델의 기본 상태를 정의합니다.
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
        'title' => fake()->title(),
        'content' => fake()->paragraph(),
    ];
}
```

<a name="recycling-an-existing-model-for-relationships"></a>
### 관계를 위한 기존 모델 재활용하기 (Recycling An Existing Model For Relationships)

여러 모델이 공통된 관계로 연결된 경우, `recycle` 메서드를 이용해 관련 모델을 모든 생성된 관계에 재활용할 수 있습니다.

예를 들어, `Airline`, `Flight`, `Ticket` 모델이 있고, 티켓이 항공사와 비행기에 속하며, 비행기도 항공사에 속한다고 합시다. 이때 티켓을 생성하며 티켓과 비행기 모두 같은 항공사를 참조하도록 하려면 다음처럼 `recycle`에 해당 항공사 인스턴스를 전달합니다:

```php
Ticket::factory()
    ->recycle(Airline::factory()->create())
    ->create();
```

`recycle` 메서드는 공통 사용자 또는 팀에 속하는 모델을 다룰 때 특히 유용합니다.

`recycle`은 기존 모델 컬렉션도 인수로 받아들입니다. 컬렉션이 주어지면 팩토리가 해당 유형의 모델이 필요할 때마다 컬렉션에서 무작위 모델을 선택합니다:

```php
Ticket::factory()
    ->recycle($airlines)
    ->create();
```