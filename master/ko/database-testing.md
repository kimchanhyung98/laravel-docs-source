# 데이터베이스 테스팅 (Database Testing)

- [소개](#introduction)
    - [각 테스트 이후 데이터베이스 초기화](#resetting-the-database-after-each-test)
- [모델 팩토리](#model-factories)
- [시더 실행](#running-seeders)
- [사용 가능한 어설션](#available-assertions)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 데이터베이스 기반 애플리케이션의 테스팅을 쉽게 할 수 있도록 다양한 도구와 어설션을 제공합니다. 또한, Laravel의 모델 팩토리와 시더를 이용하면 Eloquent 모델 및 연관관계를 활용해 테스트용 데이터베이스 레코드를 손쉽게 생성할 수 있습니다. 이 문서에서는 이러한 강력한 기능 전반을 다룹니다.

<a name="resetting-the-database-after-each-test"></a>
### 각 테스트 이후 데이터베이스 초기화

이제 본격적으로 살펴보기 전에, 각 테스트 이후 데이터베이스를 어떻게 초기화하여 이전 테스트의 데이터가 이후 테스트에 영향을 주지 않도록 할 수 있는지 알아보겠습니다. Laravel에 포함된 `Illuminate\Foundation\Testing\RefreshDatabase` 트레이트가 이 작업을 도와줍니다. 단순히 테스트 클래스에서 이 트레이트를 사용하면 됩니다:

```php tab=Pest
<?php

use Illuminate\Foundation\Testing\RefreshDatabase;

pest()->use(RefreshDatabase::class);

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
     * A basic functional test example.
     */
    public function test_basic_example(): void
    {
        $response = $this->get('/');

        // ...
    }
}
```

`Illuminate\Foundation\Testing\RefreshDatabase` 트레이트는 데이터베이스 스키마가 최신 상태라면 마이그레이션을 실행하지 않습니다. 대신, 테스트를 데이터베이스 트랜잭션 내에서 실행합니다. 따라서 이 트레이트를 사용하지 않는 테스트 케이스에서 추가된 레코드는 여전히 데이터베이스에 남아 있을 수 있습니다.

데이터베이스를 완전히 초기화하고 싶다면 `Illuminate\Foundation\Testing\DatabaseMigrations` 또는 `Illuminate\Foundation\Testing\DatabaseTruncation` 트레이트를 사용할 수 있습니다. 그러나 이 두 방법 모두 `RefreshDatabase` 트레이트에 비해 속도가 상당히 느립니다.

<a name="model-factories"></a>
## 모델 팩토리 (Model Factories)

테스트를 진행할 때, 테스트 실행 전에 데이터베이스에 몇몇 레코드를 삽입해야 할 수 있습니다. 이때 테스트 데이터를 생성할 때 각 컬럼의 값을 직접 지정하는 대신, Laravel에서는 [모델 팩토리](/docs/master/eloquent-factories)를 통해 [Eloquent 모델](/docs/master/eloquent)마다 기본 속성 세트를 정의할 수 있습니다.

모델 팩토리를 생성하고 활용하는 법에 대한 더 자세한 내용은 [모델 팩토리 문서](/docs/master/eloquent-factories)를 참고하시기 바랍니다. 모델 팩토리를 정의한 뒤에는 다음과 같이 테스트 내에서 팩토리를 이용해 모델을 만들 수 있습니다:

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

[데이터베이스 시더](/docs/master/seeding)를 활용하여 피처 테스트(feature test) 중 데이터베이스를 채우고 싶다면, `seed` 메서드를 사용하면 됩니다. 기본적으로 `seed` 메서드는 `DatabaseSeeder`를 실행하며, 이 클래스는 모든 다른 시더를 실행해야 합니다. 또는, 특정한 시더 클래스명을 `seed` 메서드에 인수로 전달할 수도 있습니다:

```php tab=Pest
<?php

use Database\Seeders\OrderStatusSeeder;
use Database\Seeders\TransactionStatusSeeder;
use Illuminate\Foundation\Testing\RefreshDatabase;

pest()->use(RefreshDatabase::class);

test('orders can be created', function () {
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
     * Test creating a new order.
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
```

또는 `RefreshDatabase` 트레이트를 사용하는 각 테스트 전에 Laravel이 자동으로 데이터베이스 시딩을 하도록 할 수도 있습니다. 이를 위해서는 기본 테스트 클래스에 `$seed` 속성을 정의하면 됩니다:

```php
<?php

namespace Tests;

use Illuminate\Foundation\Testing\TestCase as BaseTestCase;

abstract class TestCase extends BaseTestCase
{
    /**
     * Indicates whether the default seeder should run before each test.
     *
     * @var bool
     */
    protected $seed = true;
}
```

`$seed` 속성이 `true`이면, `RefreshDatabase` 트레이트를 사용하는 테스트마다 `Database\Seeders\DatabaseSeeder` 클래스가 실행됩니다. 그러나 필요할 경우, 특정 시더를 실행하려면 테스트 클래스에 `$seeder` 속성을 정의하면 됩니다:

```php
use Database\Seeders\OrderStatusSeeder;

/**
 * Run a specific seeder before each test.
 *
 * @var string
 */
protected $seeder = OrderStatusSeeder::class;
```

<a name="available-assertions"></a>
## 사용 가능한 어설션 (Available Assertions)

Laravel은 [Pest](https://pestphp.com) 또는 [PHPUnit](https://phpunit.de) 기반의 피처 테스트를 위해 여러 가지 데이터베이스 어설션을 제공합니다. 아래에서 각각의 어설션에 대해 설명합니다.

<a name="assert-database-count"></a>
#### assertDatabaseCount

데이터베이스의 특정 테이블에 지정한 개수의 레코드가 존재하는지 검증합니다:

```php
$this->assertDatabaseCount('users', 5);
```

<a name="assert-database-empty"></a>
#### assertDatabaseEmpty

데이터베이스의 특정 테이블에 레코드가 하나도 없는지 검증합니다:

```php
$this->assertDatabaseEmpty('users');
```

<a name="assert-database-has"></a>
#### assertDatabaseHas

데이터베이스의 특정 테이블에 지정한 키/값 쿼리 조건에 맞는 레코드가 존재하는지 검증합니다:

```php
$this->assertDatabaseHas('users', [
    'email' => 'sally@example.com',
]);
```

<a name="assert-database-missing"></a>
#### assertDatabaseMissing

데이터베이스의 특정 테이블에 지정한 키/값 쿼리 조건에 맞는 레코드가 존재하지 않는지 검증합니다:

```php
$this->assertDatabaseMissing('users', [
    'email' => 'sally@example.com',
]);
```

<a name="assert-deleted"></a>
#### assertSoftDeleted

`assertSoftDeleted` 메서드는 주어진 Eloquent 모델이 "소프트 삭제" 되었는지 검증할 때 사용할 수 있습니다:

```php
$this->assertSoftDeleted($user);
```

<a name="assert-not-deleted"></a>
#### assertNotSoftDeleted

`assertNotSoftDeleted` 메서드는 주어진 Eloquent 모델이 "소프트 삭제" 되지 않았음을 검증할 때 사용할 수 있습니다:

```php
$this->assertNotSoftDeleted($user);
```

<a name="assert-model-exists"></a>
#### assertModelExists

지정한 모델 또는 모델 컬렉션이 데이터베이스에 존재하는지 검증합니다:

```php
use App\Models\User;

$user = User::factory()->create();

$this->assertModelExists($user);
```

<a name="assert-model-missing"></a>
#### assertModelMissing

지정한 모델 또는 모델 컬렉션이 데이터베이스에 존재하지 않는지 검증합니다:

```php
use App\Models\User;

$user = User::factory()->create();

$user->delete();

$this->assertModelMissing($user);
```

<a name="expects-database-query-count"></a>
#### expectsDatabaseQueryCount

`expectsDatabaseQueryCount` 메서드는 테스트가 실행되는 동안 발생할 데이터베이스 쿼리의 총 개수를 미리 지정할 수 있습니다. 실제 실행 쿼리 수가 지정한 값과 정확히 일치하지 않으면 테스트가 실패합니다:

```php
$this->expectsDatabaseQueryCount(5);

// Test...
```
