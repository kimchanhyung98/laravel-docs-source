# 데이터베이스 테스트

- [소개](#introduction)
    - [각 테스트 후 데이터베이스 리셋](#resetting-the-database-after-each-test)
- [모델 팩토리 정의하기](#defining-model-factories)
    - [개념 개요](#concept-overview)
    - [팩토리 생성하기](#generating-factories)
    - [팩토리 상태](#factory-states)
    - [팩토리 콜백](#factory-callbacks)
- [팩토리를 사용한 모델 생성](#creating-models-using-factories)
    - [모델 인스턴스화](#instantiating-models)
    - [모델 영속화](#persisting-models)
    - [시퀀스](#sequences)
- [팩토리 관계](#factory-relationships)
    - [Has Many(1:N) 관계](#has-many-relationships)
    - [Belongs To(N:1) 관계](#belongs-to-relationships)
    - [Many To Many(N:M) 관계](#many-to-many-relationships)
    - [다형성 관계](#polymorphic-relationships)
    - [팩토리 내 관계 정의](#defining-relationships-within-factories)
- [시더 실행](#running-seeders)
- [사용 가능한 어서션](#available-assertions)

<a name="introduction"></a>
## 소개

Laravel은 데이터베이스 기반 애플리케이션 테스트를 더 쉽게 만들어 주는 다양한 유용한 도구와 어서션을 제공합니다. 또한, Laravel 모델 팩토리와 시더를 통해, Eloquent 모델과 관계를 사용하여 테스트 데이터베이스 레코드를 손쉽게 만들 수 있습니다. 본 문서에서는 이러한 강력한 기능들을 모두 다룰 것입니다.

<a name="resetting-the-database-after-each-test"></a>
### 각 테스트 후 데이터베이스 리셋

진행하기 전에, 이전 테스트의 데이터로 인해 이후 테스트가 영향을 받지 않도록 각 테스트 후 데이터베이스를 리셋하는 방법을 살펴보겠습니다. Laravel의 `Illuminate\Foundation\Testing\RefreshDatabase` 트레이트가 이를 처리해줍니다. 테스트 클래스에서 트레이트를 사용하면 됩니다:

```php
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
## 모델 팩토리 정의하기

<a name="concept-overview"></a>
### 개념 개요

먼저 Eloquent 모델 팩토리에 대해 설명합니다. 테스트를 할 때 테스트 실행 전에 데이터베이스에 여러 레코드를 삽입해야 할 수 있습니다. 이 때 테스트 데이터를 생성할 때 각 컬럼 값을 일일이 지정하지 않고, 모델 별로 기본 속성 집합을 팩토리로 정의할 수 있습니다. 이는 [Eloquent 모델](/docs/{{version}}/eloquent)에서 지원합니다.

팩토리 작성 예시를 보려면, 애플리케이션의 `database/factories/UserFactory.php` 파일을 살펴보세요. Laravel 새 프로젝트에서는 다음과 같은 팩토리 정의가 포함됩니다:

```php
namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;
use Illuminate\Support\Str;

class UserFactory extends Factory
{
    /**
     * 모델의 기본 상태 정의.
     *
     * @return array
     */
    public function definition()
    {
        return [
            'name' => $this->faker->name(),
            'email' => $this->faker->unique()->safeEmail(),
            'email_verified_at' => now(),
            'password' => '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', // 비밀번호
            'remember_token' => Str::random(10),
        ];
    }
}
```

위에서 볼 수 있듯이, 팩토리는 Laravel의 기본 팩토리 클래스를 확장하며, `definition` 메서드를 정의합니다. 이 메서드는 팩토리로 모델을 생성할 때 적용되는 기본 속성 값을 반환합니다.

팩토리는 `faker` 프로퍼티를 통해 [Faker](https://github.com/FakerPHP/Faker) PHP 라이브러리에 접근할 수 있으며, 이를 통해 다양한 테스트용 랜덤 데이터를 쉽게 생성할 수 있습니다.

> {tip} 애플리케이션의 Faker 로케일은 `config/app.php` 설정 파일의 `faker_locale` 옵션으로 지정할 수 있습니다.

<a name="generating-factories"></a>
### 팩토리 생성하기

팩토리를 생성하려면 `make:factory` [Artisan 명령어](/docs/{{version}}/artisan)를 실행하세요:

```
php artisan make:factory PostFactory
```

새 팩토리 클래스는 `database/factories` 디렉토리에 생성됩니다.

<a name="factory-and-model-discovery-conventions"></a>
#### 모델 & 팩토리 검색 규칙

팩토리를 정의했다면, 모델에서 `Illuminate\Database\Eloquent\Factories\HasFactory` 트레이트가 제공하는 정적 `factory` 메서드로 팩토리 인스턴스를 생성할 수 있습니다.

`HasFactory` 트레이트의 `factory` 메서드는 규칙에 따라 해당 모델에 맞는 팩토리를 찾습니다. 즉, `Database\Factories` 네임스페이스에서 모델명과 일치하며 `Factory`로 끝나는 클래스를 찾습니다. 만약 이 규칙과 다르게 동작해야 한다면, 모델에서 `newFactory` 메서드를 오버라이드하여 직접 팩토리 인스턴스를 반환하도록 할 수 있습니다:

```php
use Database\Factories\Administration\FlightFactory;

/**
 * 모델의 새 팩토리 인스턴스 생성.
 *
 * @return \Illuminate\Database\Eloquent\Factories\Factory
 */
protected static function newFactory()
{
    return FlightFactory::new();
}
```

다음으로, 해당 팩토리 클래스에 `model` 프로퍼티를 정의합니다:

```php
use App\Administration\Flight;
use Illuminate\Database\Eloquent\Factories\Factory;

class FlightFactory extends Factory
{
    /**
     * 팩토리와 연결될 모델명.
     *
     * @var string
     */
    protected $model = Flight::class;
}
```

<a name="factory-states"></a>
### 팩토리 상태

상태 변환 메서드를 사용하면 팩토리의 기본 속성에서 특정 속성만 개별적으로 조합해서 수정할 수 있습니다. 예를 들어, `Database\Factories\UserFactory`에 `suspended` 상태 메서드를 만들어서 기본 속성 값을 수정할 수 있습니다.

상태 변환은 보통 Laravel의 기본 팩토리 클래스의 `state` 메서드를 사용합니다. 이 메서드는 팩토리의 raw 속성 배열을 받아, 수정할 속성을 반환하는 클로저를 받습니다:

```php
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
```

<a name="factory-callbacks"></a>
### 팩토리 콜백

팩토리 콜백은 `afterMaking`과 `afterCreating` 메서드로 등록하며, 모델 생성 후 추가 작업을 할 수 있도록 합니다. 팩토리 클래스에 `configure` 메서드를 정의하여 콜백을 등록하세요. 이 메서드는 팩토리 인스턴스화 시 Laravel이 자동으로 호출합니다:

```php
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
```

<a name="creating-models-using-factories"></a>
## 팩토리를 사용한 모델 생성

<a name="instantiating-models"></a>
### 모델 인스턴스화

팩토리를 정의한 후에는, `Illuminate\Database\Eloquent\Factories\HasFactory` 트레이트가 제공하는 모델의 정적 `factory` 메서드로 팩토리 인스턴스를 생성할 수 있습니다. 예를 들어, `make` 메서드로 데이터베이스에 저장하지 않고 모델을 생성할 수 있습니다:

```php
use App\Models\User;

public function test_models_can_be_instantiated()
{
    $user = User::factory()->make();

    // 테스트에서 모델 사용...
}
```

`count` 메서드를 사용해 여러 개의 모델을 한 번에 생성할 수 있습니다:

```php
$users = User::factory()->count(3)->make();
```

<a name="applying-states"></a>
#### 상태 적용하기

모델에 [상태](#factory-states)를 적용할 수도 있습니다. 여러 상태 변환을 적용하려면 상태 변환 메서드를 연이어 호출하면 됩니다:

```php
$users = User::factory()->count(5)->suspended()->make();
```

<a name="overriding-attributes"></a>
#### 속성 오버라이드

기본 속성 일부를 변경하고 싶다면, `make` 메서드에 값을 배열로 전달하세요. 지정한 속성만 교체되고 나머지는 팩토리의 기본값이 적용됩니다:

```php
$user = User::factory()->make([
    'name' => 'Abigail Otwell',
]);
```

또는, 팩토리 인스턴스에서 바로 `state` 메서드로 인라인 상태 변환을 적용할 수 있습니다:

```php
$user = User::factory()->state([
    'name' => 'Abigail Otwell',
])->make();
```

> {tip} 팩토리로 모델을 생성할 때는 [대량 할당 방지](docs/{{version}}/eloquent#mass-assignment)가 자동으로 비활성화됩니다.

<a name="persisting-models"></a>
### 모델 영속화

`create` 메서드는 모델 인스턴스를 만들고 Eloquent의 `save` 메서드로 데이터베이스에 저장합니다:

```php
use App\Models\User;

public function test_models_can_be_persisted()
{
    // App\Models\User 인스턴스 한 개 생성...
    $user = User::factory()->create();

    // App\Models\User 인스턴스 세 개 생성...
    $users = User::factory()->count(3)->create();

    // 테스트에서 모델 사용...
}
```

`create` 메서드에 속성 배열을 전달하여 팩토리의 기본 모델 속성을 오버라이드할 수 있습니다:

```php
$user = User::factory()->create([
    'name' => 'Abigail',
]);
```

<a name="sequences"></a>
### 시퀀스

때때로 모델마다 속성 값을 번갈아 지정하고 싶을 때, 상태 변환을 시퀀스로 지정하면 됩니다. 예를 들어, 생성되는 사용자마다 `admin` 컬럼 값을 'Y', 'N'으로 번갈아 지정할 수 있습니다:

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

위 예시에서는 5명의 사용자가 `admin`이 'Y', 5명이 'N'으로 생성됩니다.

필요하면 시퀀스 값으로 클로저를 전달할 수도 있습니다. 이 클로저는 값이 필요한 매번 호출됩니다:

```php
$users = User::factory()
                ->count(10)
                ->state(new Sequence(
                    fn ($sequence) => ['role' => UserRoles::all()->random()],
                ))
                ->create();
```

시퀀스 클로저 내부에서, 시퀀스 인스턴스의 `$index`(현재 반복 횟수), `$count`(총 반복 횟수) 속성을 사용할 수 있습니다:

```php
$users = User::factory()
                ->count(10)
                ->sequence(fn ($sequence) => ['name' => 'Name '.$sequence->index])
                ->create();
```

<a name="factory-relationships"></a>
## 팩토리 관계

<a name="has-many-relationships"></a>
### Has Many(1:N) 관계

이제 Laravel의 유창한 팩토리 메서드를 이용해 Eloquent 모델 관계를 구축해보겠습니다. 예를 들어, `App\Models\User` 모델과 `App\Models\Post` 모델이 있고, `User`는 `Post`와 `hasMany` 관계라고 가정합니다. Laravel 팩토리의 `has` 메서드를 사용해 세 개의 게시물을 가진 사용자를 생성할 수 있습니다:

```php
use App\Models\Post;
use App\Models\User;

$user = User::factory()
            ->has(Post::factory()->count(3))
            ->create();
```

관례상, `Post` 모델을 `has`에 전달하면 Laravel은 `User` 모델에 `posts`라는 관계 메서드가 있다고 가정합니다. 필요에 따라 직접 관계명도 지정할 수 있습니다:

```php
$user = User::factory()
            ->has(Post::factory()->count(3), 'posts')
            ->create();
```

물론 관련 모델에도 상태 변환을 적용할 수 있습니다. 또는, 부모 모델에 접근이 필요한 경우, 클로저 기반 상태 변환을 사용할 수 있습니다:

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

더 편리하게, Laravel의 매직 팩토리 관계 메서드를 사용할 수도 있습니다. 아래와 같이 팩토리 네이밍 규칙만으로 `User` 모델의 `posts` 관계를 통해 관련 모델이 생성됩니다:

```php
$user = User::factory()
            ->hasPosts(3)
            ->create();
```

매직 메서드로 관계 모델 속성을 오버라이드할 수 있습니다:

```php
$user = User::factory()
            ->hasPosts(3, [
                'published' => false,
            ])
            ->create();
```

부모 모델 접근이 필요한 경우, 클로저 기반 상태 변환도 가능합니다:

```php
$user = User::factory()
            ->hasPosts(3, function (array $attributes, User $user) {
                return ['user_type' => $user->type];
            })
            ->create();
```

<a name="belongs-to-relationships"></a>
### Belongs To(N:1) 관계

앞서 팩토리로 "has many" 관계를 만드는 방법을 살펴봤으니, 이번엔 반대 방향의 관계를 살펴보겠습니다. 팩토리에서 `for` 메서드를 사용하면 생성 모델의 부모 모델을 지정할 수 있습니다. 예를 들어, 한 명의 사용자에 속하는 `App\Models\Post` 인스턴스를 3개 생성하려면:

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

이미 생성된 부모 모델이 있다면 `for` 메서드에 해당 인스턴스를 바로 전달할 수 있습니다:

```php
$user = User::factory()->create();

$posts = Post::factory()
            ->count(3)
            ->for($user)
            ->create();
```

<a name="belongs-to-relationships-using-magic-methods"></a>
#### 매직 메서드 사용

보다 간단하게, 매직 팩토리 관계 메서드로 "belongs to" 관계를 정의할 수 있습니다. 아래 예시처럼, 세 개의 게시물이 `user` 관계에 연결됩니다:

```php
$posts = Post::factory()
            ->count(3)
            ->forUser([
                'name' => 'Jessica Archer',
            ])
            ->create();
```

<a name="many-to-many-relationships"></a>
### Many To Many(N:M) 관계

[has many 관계](#has-many-relationships)처럼, N:M 관계도 `has` 메서드로 생성할 수 있습니다:

```php
use App\Models\Role;
use App\Models\User;

$user = User::factory()
            ->has(Role::factory()->count(3))
            ->create();
```

<a name="pivot-table-attributes"></a>
#### pivot 테이블 속성

모델을 연결하는 중간(pivot) 테이블에 속성을 추가하려면 `hasAttached` 메서드를 사용합니다. 이 메서드는 두 번째 인자로 pivot 테이블 속성 배열을 받습니다:

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

관련 모델 접근이 필요한 경우, 클로저 기반 상태 변환도 사용할 수 있습니다:

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

이미 모델 인스턴스가 있다면, `hasAttached`에 모델 객체를 전달할 수도 있습니다. 아래 예시에서는 세 개의 역할이 세 명의 사용자 각각에 연결됩니다:

```php
$roles = Role::factory()->count(3)->create();

$user = User::factory()
            ->count(3)
            ->hasAttached($roles, ['active' => true])
            ->create();
```

<a name="many-to-many-relationships-using-magic-methods"></a>
#### 매직 메서드 사용

매직 팩토리 메서드로 N:M 관계도 정의할 수 있습니다. 아래는 `User`의 `roles` 관계를 이용하여 관련 모델이 생성되는 예시입니다:

```php
$user = User::factory()
            ->hasRoles(1, [
                'name' => 'Editor'
            ])
            ->create();
```

<a name="polymorphic-relationships"></a>
### 다형성 관계

[다형성 관계](/docs/{{version}}/eloquent-relationships#polymorphic-relationships)도 팩토리로 생성할 수 있습니다. 다형성 "morph many" 관계는 일반 "has many" 관계와 작성 방법이 같습니다. 예를 들어, `App\Models\Post`가 `App\Models\Comment`와 `morphMany` 관계라고 가정할 때:

```php
use App\Models\Post;

$post = Post::factory()->hasComments(3)->create();
```

<a name="morph-to-relationships"></a>
#### morphTo 관계

매직 메서드로는 `morphTo` 관계를 생성할 수 없습니다. 대신, `for` 메서드를 사용하고 관계명을 명시적으로 넘겨야 합니다. 예를 들어 `Comment` 모델이 `commentable`이라는 `morphTo` 관계를 가진다면, 아래와 같이 작성할 수 있습니다:

```php
$comments = Comment::factory()->count(3)->for(
    Post::factory(), 'commentable'
)->create();
```

<a name="polymorphic-many-to-many-relationships"></a>
#### 다형성 N:M(Polymorphic Many To Many) 관계

다형성 "N:M"(`morphToMany` / `morphedByMany`) 관계도 일반 N:M 관계와 동일하게 팩토리로 생성할 수 있습니다:

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

물론, 매직 `has` 메서드로도 다형성 N:M 관계를 생성할 수 있습니다:

```php
$videos = Video::factory()
            ->hasTags(3, ['public' => true])
            ->create();
```

<a name="defining-relationships-within-factories"></a>
### 팩토리 내 관계 정의

팩토리 내부에서 관계를 정의하려면, 관계의 외래키에 새 팩토리 인스턴스를 할당합니다. 이는 주로 `belongsTo` 또는 `morphTo`와 같은 "역방향" 관계를 위한 것입니다. 예를 들어 게시물을 만들 때 새로운 사용자도 함께 생성하려면:

```php
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

관계 컬럼 값이 팩토리에서 정의된 속성에 따라 달라진다면, 속성에 클로저를 할당할 수도 있습니다. 이 클로저는 팩토리의 평가된 속성 배열을 받습니다:

```php
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
## 시더 실행

[데이터베이스 시더](/docs/{{version}}/seeding)를 이용해 기능 테스트 중에 데이터베이스를 채우고 싶다면, `seed` 메서드를 사용할 수 있습니다. 기본적으로 `seed`는 `DatabaseSeeder`를 실행하며, 이 시더에서 다른 모든 시더를 실행하게 됩니다. 또는, 특정 시더 클래스명을 `seed` 메서드에 전달할 수도 있습니다:

```php
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
     * 새로운 주문 생성 테스트.
     *
     * @return void
     */
    public function test_orders_can_be_created()
    {
        // DatabaseSeeder 실행...
        $this->seed();

        // 특정 시더 실행...
        $this->seed(OrderStatusSeeder::class);

        // ...

        // 여러 시더 한 번에 실행...
        $this->seed([
            OrderStatusSeeder::class,
            TransactionStatusSeeder::class,
            // ...
        ]);
    }
}
```

또는, `RefreshDatabase` 트레이트를 사용하는 각 테스트 전에 데이터베이스를 자동으로 시더로 채우게 할 수 있습니다. 베이스 테스트 클래스에 `$seed` 프로퍼티를 정의하면 됩니다:

```php
<?php

namespace Tests;

use Illuminate\Foundation\Testing\TestCase as BaseTestCase;

abstract class TestCase extends BaseTestCase
{
    use CreatesApplication;

    /**
     * 각 테스트 전에 기본 시더를 실행할지 여부.
     *
     * @var bool
     */
    protected $seed = true;
}
```

`$seed`가 `true`이면, 해당 테스트에서 `RefreshDatabase` 트레이트를 사용할 때마다 `Database\Seeders\DatabaseSeeder` 클래스가 실행됩니다. 특정 시더만 실행하고 싶다면, 테스트 클래스에 `$seeder` 프로퍼티를 정의하세요:

```php
use Database\Seeders\OrderStatusSeeder;

/**
 * 각 테스트 전에 특정 시더 실행.
 *
 * @var string
 */
protected $seeder = OrderStatusSeeder::class;
```

<a name="available-assertions"></a>
## 사용 가능한 어서션

Laravel은 [PHPUnit](https://phpunit.de/) 기능 테스트를 위한 여러 데이터베이스 어서션을 제공합니다. 아래에서 각 어서션을 소개합니다.

<a name="assert-database-count"></a>
#### assertDatabaseCount

데이터베이스의 특정 테이블에 지정된 갯수의 레코드가 존재하는지 단언합니다:

```php
$this->assertDatabaseCount('users', 5);
```

<a name="assert-database-has"></a>
#### assertDatabaseHas

지정한 키/값 조건에 일치하는 레코드가 존재하는지 단언합니다:

```php
$this->assertDatabaseHas('users', [
    'email' => 'sally@example.com',
]);
```

<a name="assert-database-missing"></a>
#### assertDatabaseMissing

지정한 키/값 조건에 일치하는 레코드가 존재하지 않는지 단언합니다:

```php
$this->assertDatabaseMissing('users', [
    'email' => 'sally@example.com',
]);
```

<a name="assert-deleted"></a>
#### assertDeleted

`assertDeleted`는 지정한 Eloquent 모델이 데이터베이스에서 삭제되었는지 단언합니다:

```php
use App\Models\User;

$user = User::find(1);

$user->delete();

$this->assertDeleted($user);
```

`assertSoftDeleted`는 지정 Eloquent 모델이 "소프트 삭제" 되었는지 단언합니다:

```php
$this->assertSoftDeleted($user);
```

<a name="assert-model-exists"></a>
#### assertModelExists

지정한 모델이 데이터베이스에 존재하는지 단언합니다:

```php
use App\Models\User;

$user = User::factory()->create();

$this->assertModelExists($user);
```

<a name="assert-model-missing"></a>
#### assertModelMissing

지정한 모델이 데이터베이스에 존재하지 않는지 단언합니다:

```php
use App\Models\User;

$user = User::factory()->create();

$user->delete();

$this->assertModelMissing($user);
```