# Eloquent: 팩토리(Factory)

- [소개](#introduction)
- [모델 팩토리 정의하기](#defining-model-factories)
    - [팩토리 생성하기](#generating-factories)
    - [팩토리 상태(State)](#factory-states)
    - [팩토리 콜백(Callback)](#factory-callbacks)
- [팩토리를 사용한 모델 생성](#creating-models-using-factories)
    - [모델 인스턴스화](#instantiating-models)
    - [모델 저장](#persisting-models)
    - [시퀀스(Sequences)](#sequences)
- [팩토리 관계](#factory-relationships)
    - [Has Many 관계](#has-many-relationships)
    - [Belongs To 관계](#belongs-to-relationships)
    - [Many To Many 관계](#many-to-many-relationships)
    - [Polymorphic(다형성) 관계](#polymorphic-relationships)
    - [팩토리 내에서 관계 정의하기](#defining-relationships-within-factories)
    - [기존 모델을 관계에 재활용하기](#recycling-an-existing-model-for-relationships)

<a name="introduction"></a>
## 소개

애플리케이션을 테스트하거나 데이터베이스에 시드(seed) 데이터를 삽입할 때, 데이터베이스에 여러 레코드를 추가해야 할 수 있습니다. 각 컬럼의 값을 수동으로 지정하는 대신 라라벨은 [Eloquent 모델](/docs/{{version}}/eloquent)별로 기본 속성 집합을 팩토리로 정의할 수 있게 해줍니다.

팩토리 작성 예시를 보려면 애플리케이션의 `database/factories/UserFactory.php` 파일을 확인하세요. 이 파일은 모든 새로운 라라벨 애플리케이션에 포함되어 있으며, 다음과 같은 팩토리 정의를 가지고 있습니다:

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
                'name' => fake()->name(),
                'email' => fake()->unique()->safeEmail(),
                'email_verified_at' => now(),
                'password' => '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', // 비밀번호
                'remember_token' => Str::random(10),
            ];
        }
    }

보시다시피, 가장 기본적인 형태에서 팩토리는 라라벨의 기본 팩토리 클래스를 상속하고 `definition` 메서드를 정의하는 클래스입니다. `definition` 메서드는 팩토리를 사용하여 모델을 생성할 때 적용될 기본 속성 값들을 반환합니다.

팩토리는 `fake` 헬퍼를 통해 [Faker](https://github.com/FakerPHP/Faker) PHP 라이브러리에 접근할 수 있어, 테스트와 시딩에 다양한 종류의 랜덤 데이터를 쉽게 생성할 수 있습니다.

> **참고**  
> 애플리케이션의 Faker 로케일은 `config/app.php` 설정 파일에 `faker_locale` 옵션을 추가하여 변경할 수 있습니다.

<a name="defining-model-factories"></a>
## 모델 팩토리 정의하기

<a name="generating-factories"></a>
### 팩토리 생성하기

팩토리를 생성하려면 `make:factory` [Artisan 명령어](/docs/{{version}}/artisan)를 실행하세요:

```shell
php artisan make:factory PostFactory
```

새 팩토리 클래스는 `database/factories` 디렉터리에 생성됩니다.

<a name="factory-and-model-discovery-conventions"></a>
#### 모델 & 팩토리 규칙

팩토리를 정의한 후에는 `Illuminate\Database\Eloquent\Factories\HasFactory` 트레이트에서 제공하는 정적 `factory` 메서드를 이용해 해당 모델의 팩토리 인스턴스를 만들 수 있습니다.

`HasFactory` 트레이트의 `factory` 메서드는 네이밍 컨벤션을 이용하여 모델에 맞는 팩토리를 찾습니다. 구체적으로, `Database\Factories` 네임스페이스 내에 모델명과 동일하고 `Factory`로 끝나는 클래스를 찾습니다. 이 규칙이 맞지 않는 경우, 모델에서 `newFactory` 메서드를 오버라이드하여 직접 적절한 팩토리 인스턴스를 반환할 수 있습니다:

    use Database\Factories\Administration\FlightFactory;

    /**
     * 모델에 대한 새 팩토리 인스턴스 생성.
     *
     * @return \Illuminate\Database\Eloquent\Factories\Factory
     */
    protected static function newFactory()
    {
        return FlightFactory::new();
    }

그리고 해당 팩토리에는 `model` 속성을 정의해야 합니다:

    use App\Administration\Flight;
    use Illuminate\Database\Eloquent\Factories\Factory;

    class FlightFactory extends Factory
    {
        /**
         * 팩토리가 연결된 모델명.
         *
         * @var string
         */
        protected $model = Flight::class;
    }

<a name="factory-states"></a>
### 팩토리 상태(State)

상태 변화 메서드를 사용하면, 모델 팩토리에 언제든지 조합하여 적용할 수 있는 속성 수정 사항(상태)을 정의할 수 있습니다. 예를 들어, `Database\Factories\UserFactory`에는 기본 속성 중 하나를 수정하는 `suspended` 상태 메서드를 포함할 수 있습니다.

상태 변화 메서드는 보통 라라벨 기본 팩토리 클래스가 제공하는 `state` 메서드를 호출합니다. `state` 메서드는 팩토리에 정의된 원시 속성 배열을 인자로 받는 클로저를 받고, 변경할 속성 배열을 반환해야 합니다:

    /**
     * 사용자가 정지된 상태임을 표시.
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

#### "Trashed" 상태

Eloquent 모델이 [소프트 삭제](/docs/{{version}}/eloquent#soft-deleting)가 가능하다면, 내장된 `trashed` 상태 메서드를 호출하여 생성된 모델이 이미 소프트 삭제된 상태임을 표시할 수 있습니다. `trashed` 상태는 모든 팩토리에 자동으로 제공되므로 따로 정의할 필요가 없습니다:

    use App\Models\User;

    $user = User::factory()->trashed()->create();

<a name="factory-callbacks"></a>
### 팩토리 콜백(Callback)

팩토리 콜백은 `afterMaking` 및 `afterCreating` 메서드를 사용해 등록하며, 모델을 생성하거나 저장한 후 추가 작업을 수행할 수 있습니다. 이 콜백들은 팩토리 클래스에 `configure` 메서드를 정의하여 등록해야 하며, 이 메서드는 팩토리 인스턴스화시 자동으로 호출됩니다:

    namespace Database\Factories;

    use App\Models\User;
    use Illuminate\Database\Eloquent\Factories\Factory;
    use Illuminate\Support\Str;

    class UserFactory extends Factory
    {
        /**
         * 모델 팩토리 설정.
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

<a name="creating-models-using-factories"></a>
## 팩토리를 사용한 모델 생성

<a name="instantiating-models"></a>
### 모델 인스턴스화

팩토리를 정의한 후, `Illuminate\Database\Eloquent\Factories\HasFactory` 트레이트가 제공하는 정적 `factory` 메서드를 사용해 팩토리 인스턴스를 만들 수 있습니다. 몇 가지 모델 생성 예제를 살펴보겠습니다. 먼저, `make` 메서드를 사용하여 데이터베이스에 저장하지 않고 모델을 생성할 수 있습니다:

    use App\Models\User;

    $user = User::factory()->make();

`count` 메서드를 활용하면 여러 개의 모델 컬렉션을 생성할 수 있습니다:

    $users = User::factory()->count(3)->make();

<a name="applying-states"></a>
#### 상태 적용하기

[팩토리 상태](#factory-states)를 모델에 적용할 수 있습니다. 여러 상태 변환을 적용하고 싶으면, 해당 상태 메서드를 여러 번 호출하면 됩니다:

    $users = User::factory()->count(5)->suspended()->make();

<a name="overriding-attributes"></a>
#### 속성 덮어쓰기

기본 속성 값을 덮어쓰려면, `make` 메서드에 배열을 전달하면 됩니다. 지정한 속성만 덮어써지고 나머지는 팩토리에서 정의한 기본 값이 사용됩니다:

    $user = User::factory()->make([
        'name' => 'Abigail Otwell',
    ]);

또는, 팩토리 인스턴스에서 `state` 메서드를 직접 호출하여 인라인으로 상태를 변경할 수 있습니다:

    $user = User::factory()->state([
        'name' => 'Abigail Otwell',
    ])->make();

> **참고**  
> 팩토리를 사용해 모델을 생성할 때 [대량 할당 제한](/docs/{{version}}/eloquent#mass-assignment)은 자동으로 비활성화됩니다.

<a name="persisting-models"></a>
### 모델 저장

`create` 메서드는 모델 인스턴스를 생성한 뒤, Eloquent의 `save` 메서드를 사용해 데이터베이스에 저장합니다:

    use App\Models\User;

    // 단일 App\Models\User 인스턴스 생성...
    $user = User::factory()->create();

    // 세 개의 App\Models\User 인스턴스 생성...
    $users = User::factory()->count(3)->create();

기본 속성을 오버라이드하려면, `create` 메서드에 속성 배열을 추가로 전달하면 됩니다:

    $user = User::factory()->create([
        'name' => 'Abigail',
    ]);

<a name="sequences"></a>
### 시퀀스(Sequences)

여러 모델을 생성할 때 특정 속성의 값을 번갈아가며 지정하고 싶을 때가 있습니다. 이때, 상태 변환을 시퀀스로 정의할 수 있습니다. 예를 들어, 사용자 생성 시 `admin` 컬럼의 값을 `Y`와 `N`으로 번갈아 지정하고 싶을 경우:

    use App\Models\User;
    use Illuminate\Database\Eloquent\Factories\Sequence;

    $users = User::factory()
                    ->count(10)
                    ->state(new Sequence(
                        ['admin' => 'Y'],
                        ['admin' => 'N'],
                    ))
                    ->create();

위 예시에서는 다섯 명의 사용자가 `admin`='Y'로, 나머지 다섯 명은 `admin`='N'으로 생성됩니다.

필요하다면 시퀀스 값으로 클로저를 사용할 수도 있습니다. 시퀀스가 새 값을 필요로 할 때마다 클로저가 호출됩니다:

    $users = User::factory()
                    ->count(10)
                    ->state(new Sequence(
                        fn ($sequence) => ['role' => UserRoles::all()->random()],
                    ))
                    ->create();

시퀀스 클로저 내부에서, 주입받은 시퀀스 인스턴스의 `$index`(현재 반복 횟수), `$count`(전체 반복 횟수) 속성을 사용할 수 있습니다:

    $users = User::factory()
                    ->count(10)
                    ->sequence(fn ($sequence) => ['name' => 'Name '.$sequence->index])
                    ->create();

편의상 시퀀스는 `state`를 내부적으로 호출하는 `sequence` 메서드로도 적용할 수 있습니다. `sequence`는 클로저 또는 속성 배열들을 인자로 받습니다:

    $users = User::factory()
                    ->count(2)
                    ->sequence(
                        ['name' => 'First User'],
                        ['name' => 'Second User'],
                    )
                    ->create();

<a name="factory-relationships"></a>
## 팩토리 관계

<a name="has-many-relationships"></a>
### Has Many 관계

이제 라라벨 팩토리 메서드를 사용하여 Eloquent 모델 관계를 생성하는 방법을 살펴보겠습니다. 먼저, 애플리케이션에 `App\Models\User` 모델과 `App\Models\Post` 모델이 있다고 가정하고, `User` 모델에 `Post`와의 `hasMany` 관계가 있다고 합시다.

`has` 메서드를 이용해 사용자 한 명과 게시글 세 개를 한 번에 생성할 수 있습니다.

    use App\Models\Post;
    use App\Models\User;

    $user = User::factory()
                ->has(Post::factory()->count(3))
                ->create();

관례상, `has` 메서드에 `Post` 모델을 전달하면 라라벨은 `User` 모델에 `posts` 메서드가 정의되어 있을 것으로 간주합니다. 필요하다면 관계의 이름을 두 번째 인수로 직접 지정할 수 있습니다.

    $user = User::factory()
                ->has(Post::factory()->count(3), 'posts')
                ->create();

연관 모델에 상태 변경을 적용하거나, 클로저 기반의 상태 변환도 가능합니다. 이 때, 부모 모델에 접근해야 할 때 클로저를 사용할 수 있습니다:

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
#### 매직 메서드 활용

편의상, 라라벨의 매직 팩토리 관계 메서드를 통해 관계를 쉽게 생성할 수 있습니다. 예를 들어, 아래의 예시는 컨벤션에 따라 연관 모델들이 `posts` 관계로 생성됩니다:

    $user = User::factory()
                ->hasPosts(3)
                ->create();

매직 메서드로 관계를 만들 때, 연관 모델에 오버라이드할 속성 배열을 전달할 수 있습니다:

    $user = User::factory()
                ->hasPosts(3, [
                    'published' => false,
                ])
                ->create();

또는 클로저 기반 상태 변환도 가능합니다:

    $user = User::factory()
                ->hasPosts(3, function (array $attributes, User $user) {
                    return ['user_type' => $user->type];
                })
                ->create();

<a name="belongs-to-relationships"></a>
### Belongs To 관계

"Has Many" 관계를 팩토리로 만드는 방법을 살펴봤으니, 이번엔 반대 관계를 살펴봅니다. `for` 메서드는 생성되는 모델이 어떤 부모(상위) 모델에 속할 것인지 지정하는 데 사용됩니다. 예를 들어, 하나의 사용자에 속한 `App\Models\Post` 모델 세 개를 생성할 수 있습니다:

    use App\Models\Post;
    use App\Models\User;

    $posts = Post::factory()
                ->count(3)
                ->for(User::factory()->state([
                    'name' => 'Jessica Archer',
                ]))
                ->create();

이미 부모 모델 인스턴스가 있다면, 해당 인스턴스를 `for` 메서드에 전달할 수 있습니다:

    $user = User::factory()->create();

    $posts = Post::factory()
                ->count(3)
                ->for($user)
                ->create();

<a name="belongs-to-relationships-using-magic-methods"></a>
#### 매직 메서드 활용

"Belongs To" 관계 역시 라라벨의 매직 팩토리 메서드를 사용할 수 있습니다. 아래 예시는 컨벤션에 따라 세 개의 게시글이 `Post` 모델의 `user` 관계에 연결됩니다:

    $posts = Post::factory()
                ->count(3)
                ->forUser([
                    'name' => 'Jessica Archer',
                ])
                ->create();

<a name="many-to-many-relationships"></a>
### Many To Many(다대다) 관계

[Has Many 관계](#has-many-relationships)와 마찬가지로, 다대다 관계도 `has` 메서드를 사용해 생성할 수 있습니다:

    use App\Models\Role;
    use App\Models\User;

    $user = User::factory()
                ->has(Role::factory()->count(3))
                ->create();

<a name="pivot-table-attributes"></a>
#### Pivot(중간) 테이블 속성

연결하는 피벗(중간) 테이블에 속성을 지정해야 한다면, `hasAttached` 메서드를 사용할 수 있습니다. 이 메서드는 피벗 테이블의 속성 이름과 값을 배열로 두 번째 인자로 받습니다:

    use App\Models\Role;
    use App\Models\User;

    $user = User::factory()
                ->hasAttached(
                    Role::factory()->count(3),
                    ['active' => true]
                )
                ->create();

상태 변화에 연관 모델 접근이 필요할 경우, 클로저 기반 상태 변환도 가능합니다:

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

이미 생성된 모델 인스턴스를 연결하고 싶을 경우, 해당 인스턴스를 `hasAttached` 메서드에 전달하면 됩니다. 아래 예시에서는 동일한 세 개의 역할이 모든 세 명의 사용자에 연결됩니다:

    $roles = Role::factory()->count(3)->create();

    $user = User::factory()
                ->count(3)
                ->hasAttached($roles, ['active' => true])
                ->create();

<a name="many-to-many-relationships-using-magic-methods"></a>
#### 매직 메서드 활용

다대다 관계 역시 라라벨의 매직 팩토리 메서드로 정의할 수 있습니다. 아래 예시는 관련 모델이 `User` 모델의 `roles` 관계를 통해 생성됩니다:

    $user = User::factory()
                ->hasRoles(1, [
                    'name' => 'Editor'
                ])
                ->create();

<a name="polymorphic-relationships"></a>
### Polymorphic(다형성) 관계

[Polymorphic 관계](/docs/{{version}}/eloquent-relationships#polymorphic-relationships)도 팩토리를 통해 생성할 수 있습니다. Polymorphic "morph many" 관계는 일반 "has many"와 동일하게 생성됩니다. 예를 들어, `App\Models\Post`가 `App\Models\Comment`와 `morphMany` 관계라면:

    use App\Models\Post;

    $post = Post::factory()->hasComments(3)->create();

<a name="morph-to-relationships"></a>
#### Morph To 관계

`morphTo` 관계는 매직 메서드로 생성할 수 없습니다. 대신, `for` 메서드를 직접 사용해야 하며 명시적으로 관계명을 지정해야 합니다. 예를 들어, `Comment` 모델에 `morphTo` 관계인 `commentable` 메서드가 있다면 아래와 같이 세 개의 댓글을 하나의 게시글에 속하게 만들 수 있습니다:

    $comments = Comment::factory()->count(3)->for(
        Post::factory(), 'commentable'
    )->create();

<a name="polymorphic-many-to-many-relationships"></a>
#### 다형성 다대다(Polymorphic Many To Many) 관계

다형성 다대다(`morphToMany` / `morphedByMany`) 관계 역시 일반 다대다 관계와 동일하게 생성할 수 있습니다:

    use App\Models\Tag;
    use App\Models\Video;

    $videos = Video::factory()
                ->hasAttached(
                    Tag::factory()->count(3),
                    ['public' => true]
                )
                ->create();

물론, 매직 `has` 메서드도 사용하여 다형성 다대다 관계를 만들 수 있습니다:

    $videos = Video::factory()
                ->hasTags(3, ['public' => true])
                ->create();

<a name="defining-relationships-within-factories"></a>
### 팩토리 내에서 관계 정의하기

모델 팩토리 내에서 관계를 정의하려면, 일반적으로 관계의 외래 키에 새 팩토리 인스턴스를 할당합니다. 이는 주로 `belongsTo`나 `morphTo`와 같은 역방향 관계에서 사용됩니다. 예를 들어, 게시글을 생성할 때마다 새로운 사용자를 생성하려면 다음과 같이 할 수 있습니다:

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
            'title' => fake()->title(),
            'content' => fake()->paragraph(),
        ];
    }

만약 관계의 속성이 팩토리에서 평가된 값에 따라 달라진다면, 클로저를 속성에 할당하면 됩니다. 이 클로저는 팩토리로 평가된 속성 배열을 인자로 받습니다:

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
            'title' => fake()->title(),
            'content' => fake()->paragraph(),
        ];
    }

<a name="recycling-an-existing-model-for-relationships"></a>
### 기존 모델을 관계에 재활용하기

여러 모델이 공통 관계를 가지고 있을 때, `recycle` 메서드를 사용하면 모든 관계에서 동일한 연관 모델 인스턴스를 반복 사용(재활용)할 수 있습니다.

예를 들어, `Airline`, `Flight`, `Ticket` 모델이 있고, 티켓은 항공사와 항공편에 속하며, 항공편 또한 항공사에 속한다고 가정합시다. 티켓을 생성할 때 항공사 인스턴스를 티켓과 항공편 모두에 사용하려면, `recycle` 메서드에 항공사 인스턴스를 전달하면 됩니다:

    Ticket::factory()
        ->recycle(Airline::factory()->create())
        ->create();

`recycle` 메서드는 여러 모델이 동일한 사용자나 팀에 속하게 할 때도 유용합니다.

`recycle` 메서드는 기존 모델의 컬렉션도 받을 수 있습니다. 컬렉션을 전달하면, 팩토리가 해당 유형의 모델이 필요할 때마다 임의의 모델이 선택되어 재활용됩니다:

    Ticket::factory()
        ->recycle($airlines)
        ->create();
