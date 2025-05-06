# 데이터베이스 테스트

- [소개](#introduction)
    - [각 테스트 이후 데이터베이스 초기화](#resetting-the-database-after-each-test)
- [모델 팩토리](#model-factories)
- [시더 실행하기](#running-seeders)
- [사용 가능한 단언문](#available-assertions)

<a name="introduction"></a>
## 소개

라라벨은 데이터베이스 기반의 애플리케이션을 테스트할 때 유용한 다양한 도구와 단언문(assertions)을 제공합니다. 또한, 라라벨의 모델 팩토리와 시더는 Eloquent 모델 및 관계를 활용해 테스트용 데이터베이스 레코드를 손쉽게 생성할 수 있도록 해줍니다. 아래 문서에서는 이러한 강력한 기능들에 대해 자세히 설명하겠습니다.

<a name="resetting-the-database-after-each-test"></a>
### 각 테스트 이후 데이터베이스 초기화

본격적으로 진행하기 전에, 각 테스트가 끝난 후 데이터베이스를 어떻게 초기화해서 이전 테스트의 데이터가 이후 테스트에 영향을 주지 않도록 할 수 있는지 알아보겠습니다. 라라벨에 기본으로 포함된 `Illuminate\Foundation\Testing\RefreshDatabase` 트레이트가 이를 자동으로 처리해줍니다. 아래와 같이 테스트 클래스에서 해당 트레이트를 사용하면 됩니다:

    <?php

    namespace Tests\Feature;

    use Illuminate\Foundation\Testing\RefreshDatabase;
    use Tests\TestCase;

    class ExampleTest extends TestCase
    {
        use RefreshDatabase;

        /**
         * 기본적인 기능 테스트 예시
         */
        public function test_basic_example(): void
        {
            $response = $this->get('/');

            // ...
        }
    }

`Illuminate\Foundation\Testing\RefreshDatabase` 트레이트는 데이터베이스 스키마가 최신 상태라면 마이그레이션을 실행하지 않습니다. 대신 테스트를 데이터베이스 트랜잭션 내에서 실행합니다. 따라서 이 트레이트를 사용하지 않는 테스트 케이스에서 추가된 레코드는 여전히 데이터베이스에 남아 있을 수 있습니다.

만약 데이터베이스를 완전히 초기화하고 싶다면 `Illuminate\Foundation\Testing\DatabaseMigrations` 또는 `Illuminate\Foundation\Testing\DatabaseTruncation` 트레이트를 사용할 수 있습니다. 다만, 이 두 방법 모두 `RefreshDatabase` 트레이트보다 상당히 느리다는 점에 유의하세요.

<a name="model-factories"></a>
## 모델 팩토리

테스트를 진행할 때, 테스트 실행 전 데이터베이스에 몇 개의 레코드를 삽입해야 할 때가 있습니다. 이때 테스트 데이터를 생성할 때 각 컬럼의 값을 일일이 지정하지 않고, [모델 팩토리](/docs/{{version}}/eloquent-factories)를 이용해 [Eloquent 모델](/docs/{{version}}/eloquent)별 기본 속성 집합을 정의할 수 있습니다.

모델 팩토리를 생성하고 활용하는 방법은 [모델 팩토리 문서](/docs/{{version}}/eloquent-factories)를 참고하세요. 모델 팩토리를 정의했다면, 테스트 내에서 다음과 같이 팩토리를 사용하여 모델을 생성할 수 있습니다:

    use App\Models\User;

    public function test_models_can_be_instantiated(): void
    {
        $user = User::factory()->create();

        // ...
    }

<a name="running-seeders"></a>
## 시더 실행하기

[데이터베이스 시더](/docs/{{version}}/seeding)를 활용해 기능 테스트 중 데이터베이스를 채우고 싶다면 `seed` 메서드를 사용할 수 있습니다. 기본적으로 `seed` 메서드는 `DatabaseSeeder`를 실행하여 다른 모든 시더들도 자동으로 실행합니다. 또는 원하는 특정 시더 클래스명을 `seed` 메서드에 전달할 수 있습니다:

    <?php

    namespace Tests\Feature;

    use Database\Seeders\OrderStatusSeeder;
    use Database\Seeders\TransactionStatusSeeder;
    use Illuminate\Foundation\Testing\RefreshDatabase;
    use Tests\TestCase;

    class ExampleTest extends TestCase
    {
        use RefreshDatabase;

        /**
         * 새 주문을 생성하는 테스트
         */
        public function test_orders_can_be_created(): void
        {
            // DatabaseSeeder 실행...
            $this->seed();

            // 특정 시더 실행...
            $this->seed(OrderStatusSeeder::class);

            // ...

            // 여러 시더 배열로 실행...
            $this->seed([
                OrderStatusSeeder::class,
                TransactionStatusSeeder::class,
                // ...
            ]);
        }
    }

또한, `RefreshDatabase` 트레이트를 사용하는 각 테스트 전에 라라벨이 자동으로 시더를 실행하도록 지정할 수 있습니다. 기본 테스트 클래스에 `$seed` 프로퍼티를 정의하면 됩니다:

    <?php

    namespace Tests;

    use Illuminate\Foundation\Testing\TestCase as BaseTestCase;

    abstract class TestCase extends BaseTestCase
    {
        use CreatesApplication;

        /**
         * 각 테스트 전에 기본 시더를 실행할지 여부
         *
         * @var bool
         */
        protected $seed = true;
    }

`$seed` 프로퍼티가 `true`로 지정될 경우, `RefreshDatabase` 트레이트를 사용하는 각 테스트 전에 `Database\Seeders\DatabaseSeeder` 클래스가 실행됩니다. 만약 특정 시더만 실행하고 싶다면, `$seeder` 프로퍼티를 테스트 클래스에 정의하면 됩니다:

    use Database\Seeders\OrderStatusSeeder;

    /**
     * 각 테스트 전에 특정 시더 실행
     *
     * @var string
     */
    protected $seeder = OrderStatusSeeder::class;

<a name="available-assertions"></a>
## 사용 가능한 단언문

라라벨은 [PHPUnit](https://phpunit.de/)을 사용하는 기능 테스트에서 활용할 수 있는 여러 데이터베이스 단언문을 제공합니다. 아래에서 각각의 단언문을 자세히 다루겠습니다.

<a name="assert-database-count"></a>
#### assertDatabaseCount

데이터베이스 내 특정 테이블이 주어진 개수의 레코드를 포함하고 있는지 단언합니다:

    $this->assertDatabaseCount('users', 5);

<a name="assert-database-has"></a>
#### assertDatabaseHas

데이터베이스 내 특정 테이블에 지정한 키/값 조건에 맞는 레코드가 존재하는지 단언합니다:

    $this->assertDatabaseHas('users', [
        'email' => 'sally@example.com',
    ]);

<a name="assert-database-missing"></a>
#### assertDatabaseMissing

데이터베이스 내 특정 테이블에 지정한 키/값 조건에 맞는 레코드가 존재하지 않는지 단언합니다:

    $this->assertDatabaseMissing('users', [
        'email' => 'sally@example.com',
    ]);

<a name="assert-deleted"></a>
#### assertSoftDeleted

`assertSoftDeleted` 메서드는 특정 Eloquent 모델이 "소프트 삭제" 처리되었는지 단언할 때 사용합니다:

    $this->assertSoftDeleted($user);

<a name="assert-not-deleted"></a>
#### assertNotSoftDeleted

`assertNotSoftDeleted` 메서드는 특정 Eloquent 모델이 "소프트 삭제" 처리되지 않았는지 단언할 때 사용합니다:

    $this->assertNotSoftDeleted($user);

<a name="assert-model-exists"></a>
#### assertModelExists

특정 모델 인스턴스가 데이터베이스에 존재하는지 단언합니다:

    use App\Models\User;

    $user = User::factory()->create();

    $this->assertModelExists($user);

<a name="assert-model-missing"></a>
#### assertModelMissing

특정 모델 인스턴스가 데이터베이스에 존재하지 않는지 단언합니다:

    use App\Models\User;

    $user = User::factory()->create();

    $user->delete();

    $this->assertModelMissing($user);

<a name="expects-database-query-count"></a>
#### expectsDatabaseQueryCount

`expectsDatabaseQueryCount` 메서드는 테스트 시작 시 실행될 것으로 예상되는 전체 데이터베이스 쿼리의 개수를 명시할 수 있습니다. 실제 쿼리 실행 횟수가 정확히 이 기대치와 일치하지 않으면 테스트는 실패합니다:

    $this->expectsDatabaseQueryCount(5);

    // 테스트 ...