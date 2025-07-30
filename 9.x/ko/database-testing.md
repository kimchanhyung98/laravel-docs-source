# 데이터베이스 테스트 (Database Testing)

- [소개](#introduction)
    - [각 테스트 후 데이터베이스 초기화](#resetting-the-database-after-each-test)
- [모델 팩토리](#model-factories)
- [시더 실행하기](#running-seeders)
- [사용 가능한 어서션](#available-assertions)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 데이터베이스 기반 애플리케이션 테스트를 더 쉽고 편리하게 만들어 주는 다양한 유용한 도구와 어서션을 제공합니다. 또한, Laravel의 모델 팩토리와 시더는 애플리케이션의 Eloquent 모델 및 연관관계(relationships)를 사용하여 테스트용 데이터베이스 레코드를 손쉽게 생성할 수 있게 해줍니다. 다음 문서에서는 이 강력한 기능들을 자세히 살펴보겠습니다.

<a name="resetting-the-database-after-each-test"></a>
### 각 테스트 후 데이터베이스 초기화 (Resetting The Database After Each Test)

본격적으로 진행하기 전에, 각 테스트 후 데이터베이스를 초기화하는 방법을 알아보겠습니다. 이는 이전 테스트의 데이터가 이후 테스트에 영향을 주지 않도록 하는데 중요합니다. Laravel에 포함된 `Illuminate\Foundation\Testing\RefreshDatabase` 트레이트가 자동으로 이 작업을 처리해 줍니다. 테스트 클래스에서 이 트레이트만 사용하면 됩니다:

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
     * 간단한 기능 테스트 예제입니다.
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

`Illuminate\Foundation\Testing\RefreshDatabase` 트레이트는 데이터베이스 스키마가 최신 상태면 마이그레이션을 실행하지 않습니다. 대신 데이터베이스 트랜잭션 내에서 테스트를 실행하기 때문에, 이 트레이트를 사용하지 않은 테스트 케이스가 추가한 레코드는 데이터베이스에 남아 있을 수 있습니다.

만약 데이터베이스를 완전히 초기화하려면 `Illuminate\Foundation\Testing\DatabaseMigrations` 또는 `Illuminate\Foundation\Testing\DatabaseTruncation` 트레이트를 사용할 수 있습니다. 하지만 이 두 옵션은 `RefreshDatabase` 트레이트에 비해 상당히 느립니다.

<a name="model-factories"></a>
## 모델 팩토리 (Model Factories)

테스트를 진행할 때, 테스트 실행 전에 데이터베이스에 몇 개의 레코드를 삽입해야 할 수도 있습니다. 이때 각 컬럼의 값을 일일이 지정하는 대신, Laravel은 [모델 팩토리](/docs/9.x/eloquent-factories)를 통해 각 [Eloquent 모델](/docs/9.x/eloquent)에 대한 기본 속성 집합을 정의할 수 있습니다.

모델 팩토리 생성과 사용법에 대해 더 자세히 알고 싶다면, 전체 [모델 팩토리 문서](/docs/9.x/eloquent-factories)를 참고하세요. 모델 팩토리를 정의한 후에는 테스트 내에서 다음과 같이 팩토리를 활용해 모델을 생성할 수 있습니다:

```
use App\Models\User;

public function test_models_can_be_instantiated()
{
    $user = User::factory()->create();

    // ...
}
```

<a name="running-seeders"></a>
## 시더 실행하기 (Running Seeders)

기능 테스트 중에 데이터베이스를 [시더](/docs/9.x/seeding)를 사용해 채우고 싶다면, `seed` 메서드를 호출할 수 있습니다. 기본적으로 `seed` 메서드는 모든 시더를 실행하는 `DatabaseSeeder`를 실행합니다. 또는 특정 시더 클래스를 인수로 전달할 수도 있습니다:

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

        // 여러 특정 시더 실행...
        $this->seed([
            OrderStatusSeeder::class,
            TransactionStatusSeeder::class,
            // ...
        ]);
    }
}
```

또한 `RefreshDatabase` 트레이트를 사용하는 각 테스트 전에 자동으로 데이터베이스를 시딩하도록 Laravel에 지시할 수도 있습니다. 기본 테스트 클래스에 `$seed` 속성을 정의해서 가능합니다:

```
<?php

namespace Tests;

use Illuminate\Foundation\Testing\TestCase as BaseTestCase;

abstract class TestCase extends BaseTestCase
{
    use CreatesApplication;

    /**
     * 기본 시더를 각 테스트 전에 실행 여부를 나타냅니다.
     *
     * @var bool
     */
    protected $seed = true;
}
```

`$seed` 속성이 `true`일 때, `RefreshDatabase` 트레이트를 사용하는 각 테스트 전에 `Database\Seeders\DatabaseSeeder` 클래스가 실행됩니다. 그러나 특정 시더를 실행하려면 테스트 클래스에 `$seeder` 속성을 정의할 수 있습니다:

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

Laravel은 [PHPUnit](https://phpunit.de/) 기능 테스트에서 사용할 수 있는 여러 데이터베이스 어서션을 제공합니다. 아래에서 각 어서션을 설명하겠습니다.

<a name="assert-database-count"></a>
#### assertDatabaseCount

데이터베이스 내 특정 테이블에 주어진 개수의 레코드가 존재하는지 검증합니다:

```
$this->assertDatabaseCount('users', 5);
```

<a name="assert-database-has"></a>
#### assertDatabaseHas

데이터베이스 내 특정 테이블에 주어진 키/값 조건을 만족하는 레코드가 존재하는지 검증합니다:

```
$this->assertDatabaseHas('users', [
    'email' => 'sally@example.com',
]);
```

<a name="assert-database-missing"></a>
#### assertDatabaseMissing

데이터베이스 내 특정 테이블에 주어진 키/값 조건을 만족하는 레코드가 존재하지 않는지 검증합니다:

```
$this->assertDatabaseMissing('users', [
    'email' => 'sally@example.com',
]);
```

<a name="assert-deleted"></a>
#### assertSoftDeleted

`assertSoftDeleted` 메서드는 특정 Eloquent 모델이 "소프트 삭제(soft deleted)"되었는지 검증할 때 사용합니다:

```
$this->assertSoftDeleted($user);
```

<a name="assert-not-deleted"></a>
#### assertNotSoftDeleted

`assertNotSoftDeleted` 메서드는 특정 Eloquent 모델이 "소프트 삭제"되지 않았음을 검증할 때 사용합니다:

```
$this->assertNotSoftDeleted($user);
```

<a name="assert-model-exists"></a>
#### assertModelExists

특정 모델이 데이터베이스에 존재하는지 검증합니다:

```
use App\Models\User;

$user = User::factory()->create();

$this->assertModelExists($user);
```

<a name="assert-model-missing"></a>
#### assertModelMissing

특정 모델이 데이터베이스에 존재하지 않는지 검증합니다:

```
use App\Models\User;

$user = User::factory()->create();

$user->delete();

$this->assertModelMissing($user);
```

<a name="expects-database-query-count"></a>
#### expectsDatabaseQueryCount

`expectsDatabaseQueryCount` 메서드는 테스트 시작 시 실행될 것으로 예상하는 데이터베이스 쿼리의 총 개수를 지정하는 데 사용합니다. 실제 실행 쿼리 수가 이와 다르면 테스트는 실패합니다:

```
$this->expectsDatabaseQueryCount(5);

// 테스트 코드...
```