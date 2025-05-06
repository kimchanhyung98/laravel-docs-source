# 데이터베이스 테스트

- [소개](#introduction)
    - [각 테스트 후 데이터베이스 초기화](#resetting-the-database-after-each-test)
- [모델 팩토리](#model-factories)
- [시더 실행하기](#running-seeders)
- [사용 가능한 어설션](#available-assertions)

<a name="introduction"></a>
## 소개

Laravel은 데이터베이스 기반 애플리케이션의 테스트를 보다 쉽게 만들기 위해 다양한 유용한 도구와 어설션을 제공합니다. 또한 Laravel의 모델 팩토리와 시더를 이용하면 애플리케이션의 Eloquent 모델과 관계를 사용하여 테스트용 데이터베이스 레코드를 손쉽게 생성할 수 있습니다. 이번 문서에서는 이러한 강력한 기능들에 대해 설명합니다.

<a name="resetting-the-database-after-each-test"></a>
### 각 테스트 후 데이터베이스 초기화

더 진행하기 전에, 이전 테스트의 데이터가 이후 테스트에 영향을 주지 않도록 각 테스트 후 데이터베이스를 어떻게 초기화하는지 살펴봅시다. Laravel에 기본 포함된 `Illuminate\Foundation\Testing\RefreshDatabase` 트레이트가 이를 자동으로 처리해줍니다. 테스트 클래스에 해당 트레이트를 추가하여 사용하면 됩니다:

    <?php

    namespace Tests\Feature;

    use Illuminate\Foundation\Testing\RefreshDatabase;
    use Illuminate\Foundation\Testing\WithoutMiddleware;
    use Tests\TestCase;

    class ExampleTest extends TestCase
    {
        use RefreshDatabase;

        /**
         * 기본 기능 테스트 예시.
         *
         * @return void
         */
        public function test_basic_example()
        {
            $response = $this->get('/');

            // ...
        }
    }

`Illuminate\Foundation\Testing\RefreshDatabase` 트레이트는 데이터베이스 스키마가 최신 상태라면 마이그레이션을 다시 실행하지 않습니다. 대신, 데이터베이스 트랜잭션 내에서만 테스트를 실행합니다. 따라서 이 트레이트를 사용하지 않는 테스트 케이스에서 추가된 레코드는 데이터베이스에 남아 있을 수 있습니다.

데이터베이스를 완전히 초기화하려면 `Illuminate\Foundation\Testing\DatabaseMigrations` 또는 `Illuminate\Foundation\Testing\DatabaseTruncation` 트레이트를 사용할 수 있습니다. 하지만 이 두 방법은 `RefreshDatabase` 트레이트에 비해 훨씬 느릴 수 있습니다.

<a name="model-factories"></a>
## 모델 팩토리

테스트를 작성할 때, 실행 전에 데이터베이스에 일부 레코드를 삽입해야 할 수 있습니다. 이때, 테스트 데이터를 만들며 각 컬럼 값을 직접 지정하는 대신, Laravel은 [모델 팩토리](/docs/{{version}}/eloquent-factories)를 사용하여 각 [Eloquent 모델](/docs/{{version}}/eloquent)에 대한 기본 속성 집합을 정의할 수 있게 해줍니다.

모델 팩토리를 생성하고 활용하는 방법에 대한 자세한 내용은 [모델 팩토리 공식 문서](/docs/{{version}}/eloquent-factories)를 참고하세요. 모델 팩토리를 정의한 후에는 테스트 내에서 팩토리를 사용하여 모델을 생성할 수 있습니다:

    use App\Models\User;

    public function test_models_can_be_instantiated()
    {
        $user = User::factory()->create();

        // ...
    }

<a name="running-seeders"></a>
## 시더 실행하기

테스트 중 [데이터베이스 시더](/docs/{{version}}/seeding)를 사용하여 데이터베이스를 채우려면 `seed` 메서드를 호출할 수 있습니다. 기본적으로, `seed` 메서드는 `DatabaseSeeder`를 실행하며, 이는 모든 다른 시더들을 실행합니다. 또는, 특정 시더 클래스명을 `seed` 메서드에 전달할 수도 있습니다:

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

            // 특정 시더 여러 개 실행...
            $this->seed([
                OrderStatusSeeder::class,
                TransactionStatusSeeder::class,
                // ...
            ]);
        }
    }

또는, `RefreshDatabase` 트레이트를 사용하는 각 테스트 전에 자동으로 시더를 실행하도록 Laravel에 지시할 수 있습니다. 이를 위해 기본 테스트 클래스에 `$seed` 속성을 정의하면 됩니다:

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

`$seed` 속성이 `true`인 경우, `RefreshDatabase` 트레이트를 사용하는 각 테스트 전에 `Database\Seeders\DatabaseSeeder` 클래스가 실행됩니다. 또한, 실행할 특정 시더를 지정하려면 테스트 클래스에 `$seeder` 속성을 정의할 수 있습니다:

    use Database\Seeders\OrderStatusSeeder;

    /**
     * 각 테스트 전에 특정 시더 실행.
     *
     * @var string
     */
    protected $seeder = OrderStatusSeeder::class;

<a name="available-assertions"></a>
## 사용 가능한 어설션

Laravel은 [PHPUnit](https://phpunit.de/) 기능 테스트에서 사용할 수 있는 여러 데이터베이스 어설션을 제공합니다. 아래에서 각 어설션에 대해 설명합니다.

<a name="assert-database-count"></a>
#### assertDatabaseCount

데이터베이스 내 특정 테이블이 지정한 수의 레코드를 포함하고 있는지 확인합니다:

    $this->assertDatabaseCount('users', 5);

<a name="assert-database-has"></a>
#### assertDatabaseHas

데이터베이스 내 특정 테이블이 지정한 키/값 쿼리 조건과 일치하는 레코드를 포함하고 있는지 확인합니다:

    $this->assertDatabaseHas('users', [
        'email' => 'sally@example.com',
    ]);

<a name="assert-database-missing"></a>
#### assertDatabaseMissing

데이터베이스 내 특정 테이블에 지정한 키/값 쿼리 조건과 일치하는 레코드가 존재하지 않는지 확인합니다:

    $this->assertDatabaseMissing('users', [
        'email' => 'sally@example.com',
    ]);

<a name="assert-deleted"></a>
#### assertSoftDeleted

`assertSoftDeleted` 메서드는 주어진 Eloquent 모델이 "소프트 삭제" 되었는지 확인하는 데 사용할 수 있습니다:

    $this->assertSoftDeleted($user);
    
<a name="assert-not-deleted"></a>
#### assertNotSoftDeleted

`assertNotSoftDeleted` 메서드는 주어진 Eloquent 모델이 "소프트 삭제"되지 않았는지 확인하는 데 사용할 수 있습니다:

    $this->assertNotSoftDeleted($user);

<a name="assert-model-exists"></a>
#### assertModelExists

주어진 모델이 데이터베이스에 존재하는지 확인합니다:

    use App\Models\User;

    $user = User::factory()->create();

    $this->assertModelExists($user);

<a name="assert-model-missing"></a>
#### assertModelMissing

주어진 모델이 데이터베이스에 존재하지 않는지 확인합니다:

    use App\Models\User;

    $user = User::factory()->create();

    $user->delete();

    $this->assertModelMissing($user);

<a name="expects-database-query-count"></a>
#### expectsDatabaseQueryCount

`expectsDatabaseQueryCount` 메서드는 테스트 시작 시 호출하여 해당 테스트 중에 실행될 것으로 예상되는 데이터베이스 쿼리의 총 개수를 지정할 수 있습니다. 실제 실행된 쿼리 수가 기대와 정확히 일치하지 않으면 테스트가 실패합니다:

    $this->expectsDatabaseQueryCount(5);

    // 테스트...