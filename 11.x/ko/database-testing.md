# 데이터베이스 테스트 (Database Testing)

- [소개](#introduction)
    - [각 테스트 후 데이터베이스 초기화](#resetting-the-database-after-each-test)
- [모델 팩토리](#model-factories)
- [시더 실행](#running-seeders)
- [사용 가능한 어설션](#available-assertions)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 데이터베이스 기반 애플리케이션의 테스트를 보다 쉽게 수행할 수 있도록 다양한 유용한 도구와 어설션을 제공합니다. 또한, Laravel의 모델 팩토리(model factories)와 시더(seeders)를 이용하면 애플리케이션의 Eloquent 모델과 연관관계를 활용해 테스트용 데이터베이스 레코드를 간편하게 생성할 수 있습니다. 다음 문서에서 이러한 강력한 기능들을 자세히 다루겠습니다.

<a name="resetting-the-database-after-each-test"></a>
### 각 테스트 후 데이터베이스 초기화 (Resetting the Database After Each Test)

본격적으로 진행하기 전에, 이전 테스트의 데이터가 이후 테스트에 영향을 미치지 않도록 각 테스트 후 데이터베이스를 초기화하는 방법을 살펴보겠습니다. Laravel에 기본 포함된 `Illuminate\Foundation\Testing\RefreshDatabase` 트레이트가 이를 대신 처리해 줍니다. 단순히 테스트 클래스에서 이 트레이트를 사용하면 됩니다:

```php tab=Pest
<?php

use Illuminate\Foundation\Testing\RefreshDatabase;

uses(RefreshDatabase::class);

test('basic example', function () {
    $response = $this->get('/');

    // ...
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    use RefreshDatabase;

    /**
     * 기본 기능 테스트 예시.
     */
    public function test_basic_example(): void
    {
        $response = $this->get('/');

        // ...
    }
}
```

`Illuminate\Foundation\Testing\RefreshDatabase` 트레이트는 스키마가 최신인 경우 데이터베이스 마이그레이션을 실행하지 않고, 대신 테스트를 데이터베이스 트랜잭션 내에서 실행합니다. 따라서 이 트레이트를 사용하지 않는 테스트 케이스에서 추가된 레코드는 데이터베이스에 남아 있을 수 있습니다.

데이터베이스를 완전히 리셋하고 싶다면, `Illuminate\Foundation\Testing\DatabaseMigrations` 또는 `Illuminate\Foundation\Testing\DatabaseTruncation` 트레이트를 사용할 수 있습니다. 하지만 이 두 방법은 `RefreshDatabase` 트레이트보다 훨씬 느리다는 단점이 있습니다.

<a name="model-factories"></a>
## 모델 팩토리 (Model Factories)

테스트 중에는 테스트 실행 전에 데이터베이스에 몇 개의 레코드를 삽입해야 할 수 있습니다. 이때, 각 컬럼의 값을 일일이 지정하는 대신 Laravel에서는 [모델 팩토리](/docs/11.x/eloquent-factories)를 통해 각 [Eloquent 모델](/docs/11.x/eloquent)에 대한 기본 속성을 정의할 수 있습니다.

모델 팩토리 생성 및 활용법에 대해 자세히 알고 싶다면 [모델 팩토리 문서](/docs/11.x/eloquent-factories)를 참고하세요. 모델 팩토리가 정의되어 있다면, 테스트 내에서 팩토리를 사용해 간단히 모델을 생성할 수 있습니다:

```php tab=Pest
use App\Models\User;

test('models can be instantiated', function () {
    $user = User::factory()->create();

    // ...
});
```

```php tab=PHPUnit
use App\Models\User;

public function test_models_can_be_instantiated(): void
{
    $user = User::factory()->create();

    // ...
}
```

<a name="running-seeders"></a>
## 시더 실행 (Running Seeders)

피처 테스트 중에 [데이터베이스 시더](/docs/11.x/seeding)를 사용해 데이터베이스를 채우고 싶다면, `seed` 메서드를 호출하면 됩니다. 기본적으로 `seed` 메서드는 모든 다른 시더를 실행해야 하는 `DatabaseSeeder`를 실행합니다. 또는 특정 시더 클래스명을 `seed` 메서드에 인수로 넘길 수도 있습니다:

```php tab=Pest
<?php

use Database\Seeders\OrderStatusSeeder;
use Database\Seeders\TransactionStatusSeeder;
use Illuminate\Foundation\Testing\RefreshDatabase;

uses(RefreshDatabase::class);

test('orders can be created', function () {
    // DatabaseSeeder 실행...
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
});
```

```php tab=PHPUnit
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
     * 주문 생성 테스트.
     */
    public function test_orders_can_be_created(): void
    {
        // DatabaseSeeder 실행...
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

또한 `RefreshDatabase` 트레이트를 사용하는 각 테스트 전에 데이터베이스를 자동으로 시딩하도록 Laravel에 지시할 수도 있습니다. 이를 위해 기본 테스트 클래스에 `$seed` 프로퍼티를 정의하면 됩니다:

```
<?php

namespace Tests;

use Illuminate\Foundation\Testing\TestCase as BaseTestCase;

abstract class TestCase extends BaseTestCase
{
    /**
     * 각 테스트 전에 기본 시더를 실행할지 여부를 나타냅니다.
     *
     * @var bool
     */
    protected $seed = true;
}
```

`$seed` 프로퍼티가 `true`이면, `RefreshDatabase`를 사용하는 각 테스트 전에 `Database\Seeders\DatabaseSeeder` 클래스가 실행됩니다. 하지만, 특정 시더를 실행하고 싶다면 테스트 클래스에 `$seeder` 프로퍼티를 정의하여 지정할 수 있습니다:

```
use Database\Seeders\OrderStatusSeeder;

/**
 * 각 테스트 전에 특정 시더를 실행합니다.
 *
 * @var string
 */
protected $seeder = OrderStatusSeeder::class;
```

<a name="available-assertions"></a>
## 사용 가능한 어설션 (Available Assertions)

Laravel은 [Pest](https://pestphp.com) 또는 [PHPUnit](https://phpunit.de) 피처 테스트에서 사용할 수 있는 다양한 데이터베이스 어설션을 제공합니다. 다음은 그 각 항목에 대한 설명입니다.

<a name="assert-database-count"></a>
#### assertDatabaseCount

데이터베이스의 특정 테이블이 지정된 개수만큼 레코드를 포함하는지 검증합니다:

```
$this->assertDatabaseCount('users', 5);
```

<a name="assert-database-empty"></a>
#### assertDatabaseEmpty

데이터베이스의 특정 테이블에 레코드가 하나도 없는지 검증합니다:

```
$this->assertDatabaseEmpty('users');
```

<a name="assert-database-has"></a>
#### assertDatabaseHas

데이터베이스의 특정 테이블에 주어진 키/값 쿼리 조건과 일치하는 레코드가 있는지 검증합니다:

```
$this->assertDatabaseHas('users', [
    'email' => 'sally@example.com',
]);
```

<a name="assert-database-missing"></a>
#### assertDatabaseMissing

데이터베이스의 특정 테이블에 주어진 키/값 쿼리 조건과 일치하는 레코드가 없는지 검증합니다:

```
$this->assertDatabaseMissing('users', [
    'email' => 'sally@example.com',
]);
```

<a name="assert-deleted"></a>
#### assertSoftDeleted

주어진 Eloquent 모델이 "소프트 삭제(soft deleted)" 되었는지 검증할 때 사용합니다:

```
$this->assertSoftDeleted($user);
```

<a name="assert-not-deleted"></a>
#### assertNotSoftDeleted

주어진 Eloquent 모델이 "소프트 삭제"되지 않았음을 검증할 때 사용합니다:

```
$this->assertNotSoftDeleted($user);
```

<a name="assert-model-exists"></a>
#### assertModelExists

주어진 모델이 데이터베이스에 존재하는지 검증합니다:

```
use App\Models\User;

$user = User::factory()->create();

$this->assertModelExists($user);
```

<a name="assert-model-missing"></a>
#### assertModelMissing

주어진 모델이 데이터베이스에 존재하지 않음을 검증합니다:

```
use App\Models\User;

$user = User::factory()->create();

$user->delete();

$this->assertModelMissing($user);
```

<a name="expects-database-query-count"></a>
#### expectsDatabaseQueryCount

테스트 시작 시점에 사용해, 테스트 도중 실행될 것으로 예상하는 총 데이터베이스 쿼리 개수를 지정할 수 있습니다. 실제 쿼리 개수가 이 예상 개수와 일치하지 않으면 테스트는 실패합니다:

```
$this->expectsDatabaseQueryCount(5);

// 테스트 실행...
```