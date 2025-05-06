# Eloquent: 팩토리(Factory)

- [소개](#introduction)
- [모델 팩토리 정의하기](#defining-model-factories)
    - [팩토리 생성](#generating-factories)
    - [팩토리 상태(State)](#factory-states)
    - [팩토리 콜백](#factory-callbacks)
- [팩토리를 이용한 모델 생성](#creating-models-using-factories)
    - [모델 인스턴스화](#instantiating-models)
    - [모델 저장](#persisting-models)
    - [시퀀스](#sequences)
- [팩토리 관계 정의](#factory-relationships)
    - [Has Many 관계](#has-many-relationships)
    - [Belongs To 관계](#belongs-to-relationships)
    - [Many to Many 관계](#many-to-many-relationships)
    - [다형성(Polymorphic) 관계](#polymorphic-relationships)
    - [팩토리 내부에서 관계 정의](#defining-relationships-within-factories)
    - [관계를 위한 기존 모델 재사용](#recycling-an-existing-model-for-relationships)

<a name="introduction"></a>
## 소개

애플리케이션을 테스트하거나 데이터베이스를 시딩할 때, 데이터베이스에 여러 레코드를 삽입해야 할 수 있습니다. 각 컬럼의 값을 일일이 지정하는 대신, Laravel에서는 각 [Eloquent 모델](/docs/{{version}}/eloquent)에 대해 모델 팩토리를 사용하여 기본 속성 집합을 정의할 수 있습니다.

팩토리 작성 예제를 보려면, 애플리케이션의 `database/factories/UserFactory.php` 파일을 확인하세요. 이 팩토리는 새롭게 생성된 모든 Laravel 애플리케이션에 포함되어 있으며 다음과 같은 팩토리 정의를 담고 있습니다:

    namespace Database\Factories;

    use Illuminate\Support\Str;
    use Illuminate\Database\Eloquent\Factories\Factory;

    class UserFactory extends Factory
    {
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
                'password' => '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', // 패스워드
                'remember_token' => Str::random(10),
            ];
        }
    }

보시다시피, 가장 기본 형태에서 팩토리는 Laravel의 기본 팩토리 클래스를 확장하고 `definition` 메서드를 정의하는 클래스입니다. `definition` 메서드는 이 팩토리를 통해 모델을 생성할 때 적용되어야 하는 기본 속성 값의 집합을 반환합니다.

팩토리에서는 `fake` 헬퍼를 통해 [Faker](https://github.com/FakerPHP/Faker) PHP 라이브러리를 이용할 수 있으며, 이를 통해 테스트 및 시딩 시 다양한 종류의 무작위 데이터를 쉽게 생성할 수 있습니다.

> [!NOTE]  
> `config/app.php` 설정 파일에 `faker_locale` 옵션을 추가하여 애플리케이션의 Faker 로케일을 지정할 수 있습니다.

<a name="defining-model-factories"></a>
## 모델 팩토리 정의하기

<a name="generating-factories"></a>
### 팩토리 생성

팩토리를 생성하려면 `make:factory` [Artisan 커맨드](/docs/{{version}}/artisan)를 실행하세요:

```shell
php artisan make:factory PostFactory
```

새 팩토리 클래스는 `database/factories` 디렉터리에 생성됩니다.

<a name="factory-and-model-discovery-conventions"></a>
#### 모델 및 팩토리 매칭 규칙

팩토리를 정의한 후, 모델에서 `Illuminate\Database\Eloquent\Factories\HasFactory` 트레잇을 이용하여 제공되는 정적 `factory` 메서드를 사용해 해당 모델의 팩토리 인스턴스를 만들 수 있습니다.

`HasFactory` 트레잇의 `factory` 메서드는 해당 트레잇이 할당된 모델에 올바른 팩토리를 결정하는 관례를 따릅니다. 구체적으로, 이 메서드는 `Database\Factories` 네임스페이스에서 모델 이름과 동일한 클래스명 뒤에 `Factory`가 붙은 팩토리를 찾습니다. 이 규칙이 애플리케이션에 적용되지 않는 경우, 모델의 `newFactory` 메서드를 오버라이드해서 직접 팩토리 인스턴스를 반환할 수 있습니다:

    use Illuminate\Database\Eloquent\Factories\Factory;
    use Database\Factories\Administration\FlightFactory;

    /**
     * 해당 모델의 새 팩토리 인스턴스를 생성합니다.
     */
    protected static function newFactory(): Factory
    {
        return FlightFactory::new();
    }

그리고 해당하는 팩토리에서 `model` 속성을 정의해줍니다:

    use App\Administration\Flight;
    use Illuminate\Database\Eloquent\Factories\Factory;

    class FlightFactory extends Factory
    {
        /**
         * 팩토리와 매칭되는 모델명.
         *
         * @var class-string<\Illuminate\Database\Eloquent\Model>
         */
        protected $model = Flight::class;
    }

<a name="factory-states"></a>
### 팩토리 상태(State)

상태 변환 메서드를 이용해 모델 팩토리에 조합 가능한 여러 가지 수정값(상태)를 정의할 수 있습니다. 예를 들어, `Database\Factories\UserFactory` 팩토리에 기본 속성을 수정하는 `suspended` 상태 메서드를 정의할 수 있습니다.

상태 변환은 보통 Laravel의 기본 팩토리 클래스의 `state` 메서드를 호출하여 처리합니다. `state` 메서드는 팩토리에서 정의한 raw 속성 배열을 받아 수정할 속성을 반환하는 클로저를 인자로 받습니다:

    use Illuminate\Database\Eloquent\Factories\Factory;

    /**
     * 사용자가 정지 상태임을 나타냅니다.
     */
    public function suspended(): Factory
    {
        return $this->state(function (array $attributes) {
            return [
                'account_status' => 'suspended',
            ];
        });
    }

<a name="trashed-state"></a>
#### "Trashed" 상태

Eloquent 모델이 [소프트 삭제](/docs/{{version}}/eloquent#soft-deleting)를 지원한다면, 내장된 `trashed` 상태 메서드를 호출하여 생성된 모델이 이미 "소프트 삭제됨" 상태로 만들 수 있습니다. `trashed` 상태는 모든 팩토리에서 자동으로 사용할 수 있으므로 별도로 정의할 필요가 없습니다:

    use App\Models\User;

    $user = User::factory()->trashed()->create();

<a name="factory-callbacks"></a>
### 팩토리 콜백

팩토리 콜백은 `afterMaking` 및 `afterCreating` 메서드를 사용해 등록하거나, 팩토리 클래스에 `configure` 메서드를 정의하여 등록할 수 있습니다. 이 메서드는 팩토리가 인스턴스화될 때 Laravel에 의해 자동 호출됩니다:

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

특정 상태에만 적용하고 싶다면 상태 변환 메서드 내에서 팩토리 콜백을 사용할 수도 있습니다:

    use App\Models\User;
    use Illuminate\Database\Eloquent\Factories\Factory;

    /**
     * 사용자가 정지 상태임을 나타냅니다.
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

<a name="creating-models-using-factories"></a>
## 팩토리를 이용한 모델 생성

<a name="instantiating-models"></a>
### 모델 인스턴스화

팩토리를 정의한 후, 모델에서 `Illuminate\Database\Eloquent\Factories\HasFactory` 트레잇을 이용해 제공되는 정적 `factory` 메서드를 통해 쉽게 팩토리를 인스턴스화할 수 있습니다. 아래는 모델을 생성하는 몇 가지 예시입니다. 먼저, `make` 메서드를 사용해 데이터베이스에 저장하지 않고 모델을 생성해봅니다:

    use App\Models\User;

    $user = User::factory()->make();

`count` 메서드를 통해 여러 모델의 컬렉션을 생성할 수도 있습니다:

    $users = User::factory()->count(3)->make();

<a name="applying-states"></a>
#### 상태 적용

[상태](#factory-states)를 모델에 적용할 수도 있습니다. 여러 상태를 한 모델에 적용하고 싶다면 상태 변환 메서드를 연이어 호출하세요:

    $users = User::factory()->count(5)->suspended()->make();

<a name="overriding-attributes"></a>
#### 속성 오버라이딩

모델의 일부 기본 속성 값을 변경하고 싶다면 값을 배열로 `make` 메서드에 전달하면 됩니다. 지정한 속성만 변경되고, 나머지는 팩토리에서 정의한 기본값이 유지됩니다:

    $user = User::factory()->make([
        'name' => 'Abigail Otwell',
    ]);

또는, 팩토리 인스턴스에서 `state` 메서드를 사용할 수도 있습니다:

    $user = User::factory()->state([
        'name' => 'Abigail Otwell',
    ])->make();

> [!NOTE]  
> 팩토리로 모델을 생성할 때는 [대량 할당 보호](/docs/{{version}}/eloquent#mass-assignment)가 자동으로 비활성화됩니다.

<a name="persisting-models"></a>
### 모델 저장

`create` 메서드는 모델 인스턴스를 생성하고 Eloquent의 `save` 메서드를 사용하여 데이터베이스에 저장합니다:

    use App\Models\User;

    // 단일 App\Models\User 인스턴스 생성...
    $user = User::factory()->create();

    // 세 개의 App\Models\User 인스턴스 생성...
    $users = User::factory()->count(3)->create();

팩토리의 기본 속성을 오버라이드하려면, 속성 배열을 `create` 메서드에 전달하세요:

    $user = User::factory()->create([
        'name' => 'Abigail',
    ]);

<a name="sequences"></a>
### 시퀀스

여러 모델을 생성할 때, 각 모델의 특정 속성 값을 번갈아 지정하고 싶을 수 있습니다. 이럴 때는 상태 변환을 시퀀스로 정의할 수 있습니다. 예를 들어, 생성된 사용자마다 `admin` 컬럼 값을 `Y`와 `N`으로 번갈아 할당하려면:

    use App\Models\User;
    use Illuminate\Database\Eloquent\Factories\Sequence;

    $users = User::factory()
                    ->count(10)
                    ->state(new Sequence(
                        ['admin' => 'Y'],
                        ['admin' => 'N'],
                    ))
                    ->create();

이 예시에서는 5명의 사용자가 `admin` 값이 `Y`로, 나머지 5명은 `N`으로 생성됩니다.

필요하다면 시퀀스 값으로 클로저를 사용할 수도 있습니다. 시퀀스에서 새 값이 필요할 때마다 클로저가 호출됩니다:

    use Illuminate\Database\Eloquent\Factories\Sequence;

    $users = User::factory()
                    ->count(10)
                    ->state(new Sequence(
                        fn (Sequence $sequence) => ['role' => UserRoles::all()->random()],
                    ))
                    ->create();

시퀀스 클로저 내부에서는 전달받은 시퀀스 인스턴스의 `$index`나 `$count` 속성에 접근할 수 있습니다. `$index`는 현재까지 반복된 횟수, `$count`는 시퀀스가 총 몇 번 호출될지 나타냅니다:

    $users = User::factory()
                    ->count(10)
                    ->sequence(fn (Sequence $sequence) => ['name' => 'Name '.$sequence->index])
                    ->create();

편의를 위해 `sequence` 메서드로도 시퀀스를 적용할 수 있습니다. 이 메서드는 내부적으로 `state`를 호출합니다. 배열 또는 클로저를 인자로 사용할 수 있습니다:

    $users = User::factory()
                    ->count(2)
                    ->sequence(
                        ['name' => 'First User'],
                        ['name' => 'Second User'],
                    )
                    ->create();

<a name="factory-relationships"></a>
## 팩토리 관계 정의

<a name="has-many-relationships"></a>
### Has Many 관계

다음으로, Laravel의 플루언트 팩토리 메서드를 사용해 Eloquent 모델 관계를 빌드하는 방법을 살펴보겠습니다. 예를 들어, 애플리케이션에 `App\Models\User`와 `App\Models\Post` 모델이 있고, `User` 모델에 `Post`에 대한 `hasMany` 관계가 있다고 가정합니다. 이럴 때 Laravel 팩토리의 `has` 메서드를 이용해 3개의 게시글을 가진 사용자를 만들 수 있습니다. `has` 메서드는 팩토리 인스턴스를 받습니다:

    use App\Models\Post;
    use App\Models\User;

    $user = User::factory()
                ->has(Post::factory()->count(3))
                ->create();

`has` 메서드에 `Post` 모델을 전달하면, Laravel은 `User` 모델에 관계 메서드인 `posts`가 있다고 가정합니다. 필요하다면, 조작할 관계 이름을 직접 지정할 수도 있습니다:

    $user = User::factory()
                ->has(Post::factory()->count(3), 'posts')
                ->create();

또한, 관계된 모델에 상태 변환을 적용할 수도 있고, 부모 모델에 접근이 필요한 경우 클로저 기반 상태 변환도 사용할 수 있습니다:

    $user = User::factory()
                ->has(
                    Post::factory()
                            ->count(3)
                            ->state(function (array $attributes, User $user) {
                                return ['user_type' => $user->type];
                            })
                )
                ->create();

<a name="has-many-relationships-using-magic-methods"></a>
#### 매직 메서드 사용하기

더 편리하게, Laravel의 팩토리 매직 관계 메서드를 사용할 수 있습니다. 아래는 예시로, `User` 모델의 `posts` 관계를 이용해 관련 모델을 생성합니다:

    $user = User::factory()
                ->hasPosts(3)
                ->create();

매직 메서드로 관계를 생성할 때, 관계된 모델의 속성을 오버라이드하는 배열을 전달할 수도 있습니다:

    $user = User::factory()
                ->hasPosts(3, [
                    'published' => false,
                ])
                ->create();

부모 모델 정보가 필요한 상태 변환 역시 클로저로 지정할 수 있습니다:

    $user = User::factory()
                ->hasPosts(3, function (array $attributes, User $user) {
                    return ['user_type' => $user->type];
                })
                ->create();

<a name="belongs-to-relationships"></a>
### Belongs To 관계

"has many" 관계를 팩토리로 생성하는 방법을 알아봤으니, 이제 관계의 반대편을 살펴봅시다. `for` 메서드를 사용해 팩토리에서 생성된 모델이 속하게 될 부모 모델을 지정할 수 있습니다. 예를 들어, 한 명의 사용자에게 속한 3개의 게시글 생성:

    use App\Models\Post;
    use App\Models\User;

    $posts = Post::factory()
                ->count(3)
                ->for(User::factory()->state([
                    'name' => 'Jessica Archer',
                ]))
                ->create();

이미 생성된 부모 모델이 있는 경우, 해당 모델 인스턴스를 `for` 메서드에 전달할 수 있습니다:

    $user = User::factory()->create();

    $posts = Post::factory()
                ->count(3)
                ->for($user)
                ->create();

<a name="belongs-to-relationships-using-magic-methods"></a>
#### 매직 메서드 사용하기

"belongs to" 관계 역시 Laravel의 팩토리 매직 메서드로 지정할 수 있습니다. 다음 예시는 세 개의 게시물이 `Post` 모델의 `user` 관계에 속하도록 생성합니다:

    $posts = Post::factory()
                ->count(3)
                ->forUser([
                    'name' => 'Jessica Archer',
                ])
                ->create();

<a name="many-to-many-relationships"></a>
### Many to Many 관계

`has many` 관계와 마찬가지로, "many to many" 관계 역시 `has` 메서드로 생성할 수 있습니다:

    use App\Models\Role;
    use App\Models\User;

    $user = User::factory()
                ->has(Role::factory()->count(3))
                ->create();

<a name="pivot-table-attributes"></a>
#### Pivot(중간) 테이블 속성

연결되는 모델들의 pivot(중간) 테이블에 세팅할 속성이 필요하다면, `hasAttached` 메서드를 사용하세요. 이 메서드는 두 번째 인자로 pivot 속성과 값을 배열로 받습니다:

    use App\Models\Role;
    use App\Models\User;

    $user = User::factory()
                ->hasAttached(
                    Role::factory()->count(3),
                    ['active' => true]
                )
                ->create();

관계된 모델 정보가 필요한 상태 변환이 필요하다면 클로저를 사용할 수 있습니다:

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

이미 생성된 모델 인스턴스를 사용해 연결하고자 한다면, 해당 인스턴스들을 `hasAttached`에 전달하면 됩니다. 아래 예시는 세 개의 역할(role)이 세 명의 사용자 모두에 연결됩니다:

    $roles = Role::factory()->count(3)->create();

    $user = User::factory()
                ->count(3)
                ->hasAttached($roles, ['active' => true])
                ->create();

<a name="many-to-many-relationships-using-magic-methods"></a>
#### 매직 메서드 사용하기

Laravel의 팩토리 매직 메서드로도 many to many 관계를 쉽게 정의할 수 있습니다. 아래 예시는 `User` 모델의 `roles` 관계를 통해 연결된 모델을 생성합니다:

    $user = User::factory()
                ->hasRoles(1, [
                    'name' => 'Editor'
                ])
                ->create();

<a name="polymorphic-relationships"></a>
### 다형성(Polymorphic) 관계

[다형성(polymorphic) 관계](/docs/{{version}}/eloquent-relationships#polymorphic-relationships)도 팩토리로 생성할 수 있습니다. 다형성 "morph many" 관계는 일반적인 has many와 동일하게 생성합니다. 예를 들어, `App\Models\Post` 모델이 `App\Models\Comment`와 `morphMany` 관계를 맺었다면:

    use App\Models\Post;

    $post = Post::factory()->hasComments(3)->create();

<a name="morph-to-relationships"></a>
#### Morph To 관계

매직 메서드로는 `morphTo` 관계를 생성할 수 없습니다. 대신 `for` 메서드를 직접 사용하고 관계 이름을 명시적으로 지정해야 합니다. `Comment` 모델에 `commentable` 메서드가 있고, 이 메서드가 `morphTo` 관계를 정의한다고 가정하면, 아래처럼 단일 포스트에 속한 세 개의 댓글을 생성할 수 있습니다:

    $comments = Comment::factory()->count(3)->for(
        Post::factory(), 'commentable'
    )->create();

<a name="polymorphic-many-to-many-relationships"></a>
#### 다형성 Many to Many 관계

다형성 "many to many"(`morphToMany`/`morphedByMany`) 관계도 일반 many to many 관계와 동일하게 생성할 수 있습니다:

    use App\Models\Tag;
    use App\Models\Video;

    $videos = Video::factory()
                ->hasAttached(
                    Tag::factory()->count(3),
                    ['public' => true]
                )
                ->create();

물론, 매직 `has` 메서드로도 다형성 many to many 관계를 생성할 수 있습니다:

    $videos = Video::factory()
                ->hasTags(3, ['public' => true])
                ->create();

<a name="defining-relationships-within-factories"></a>
### 팩토리 내부에서 관계 정의

모델 팩토리 내부에서 관계를 정의하려면, 해당 관계의 외래키에 새 팩토리 인스턴스를 할당하면 됩니다. 이는 보통 `belongsTo`나 `morphTo`처럼 "역방향" 관계를 위해 사용됩니다. 예를 들어, 포스트를 생성할 때 항상 새로운 사용자를 생성하려면:

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

관계 속성이 팩토리에서 정의된 값에 따라 달라진다면, 속성에 클로저를 할당할 수 있습니다. 이 클로저는 팩토리의 속성 배열을 받습니다:

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

<a name="recycling-an-existing-model-for-relationships"></a>
### 관계를 위한 기존 모델 재사용

여러 개의 모델이 공통된 관계를 공유해야 하는 경우, `recycle` 메서드를 사용해 팩토리가 생성하는 모든 관계에 대해 하나의 관계 모델 인스턴스가 재사용되도록 할 수 있습니다.

예를 들어, `Airline`, `Flight`, `Ticket` 모델이 있고, 티켓은 항공사와 비행편에 각각 속하며, 비행편도 항공사에 속한다고 가정합시다. 티켓을 생성할 때, 티켓과 비행편에서 동일한 항공사를 사용하고 싶다면, `recycle` 메서드에 항공사 인스턴스를 전달하세요:

    Ticket::factory()
        ->recycle(Airline::factory()->create())
        ->create();

모델이 공통된 사용자나 팀에 속해야 하는 경우에도 `recycle` 메서드가 매우 유용합니다.

`recycle` 메서드는 기존 모델의 컬렉션을 받아올 수도 있습니다. 이때는 컬렉션에서 무작위로 하나의 모델이 선택되어 팩토리에서 사용됩니다:

    Ticket::factory()
        ->recycle($airlines)
        ->create();
