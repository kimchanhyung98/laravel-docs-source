# 데이터베이스 테스트 (Database Testing)

- [소개](#introduction)
    - [각 테스트 후 데이터베이스 초기화](#resetting-the-database-after-each-test)
- [모델 팩토리](#model-factories)
- [시더 실행하기](#running-seeders)
- [사용 가능한 어서션](#available-assertions)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 데이터베이스 기반 애플리케이션 테스트를 쉽게 할 수 있도록 다양한 유용한 도구와 어서션을 제공합니다. 또한, Laravel의 모델 팩토리(model factories)와 시더(seeders)를 사용하면 애플리케이션의 Eloquent 모델과 연관관계를 이용해 테스트용 데이터베이스 레코드를 손쉽게 생성할 수 있습니다. 이번 문서에서는 이러한 강력한 기능들을 모두 다룰 예정입니다.

<a name="resetting-the-database-after-each-test"></a>
### 각 테스트 후 데이터베이스 초기화 (Resetting the Database After Each Test)

테스트를 진행하기 전, 각 테스트가 끝난 후 이전 테스트 데이터가 이후 테스트에 영향을 주지 않도록 데이터베이스를 초기화하는 방법을 먼저 알아보겠습니다. Laravel에 내장된 `Illuminate\Foundation\Testing\RefreshDatabase` 트레이트(trait)를 사용하면 이 작업을 자동으로 처리할 수 있습니다. 테스트 클래스에 이 트레이트를 추가하기만 하면 됩니다:

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
     * 기본 기능 테스트 예제
     */
    public function test_basic_example(): void
    {
        $response = $this->get('/');

        // ...
    }
}
```

`Illuminate\Foundation\Testing\RefreshDatabase` 트레이트는 데이터베이스 스키마가 최신 상태이면 마이그레이션을 수행하지 않고, 테스트를 데이터베이스 트랜잭션 내에서 실행합니다. 따라서 이 트레이트를 사용하지 않는 테스트에서 추가한 레코드는 데이터베이스에 남아 있을 수 있습니다.

데이터베이스를 완전히 초기화하고 싶다면 `Illuminate\Foundation\Testing\DatabaseMigrations` 또는 `Illuminate\Foundation\Testing\DatabaseTruncation` 트레이트를 사용할 수 있지만, 이 두 옵션은 `RefreshDatabase` 트레이트보다 훨씬 느리다는 점을 유의하세요.

<a name="model-factories"></a>
## 모델 팩토리 (Model Factories)

테스트 시, 테스트를 실행하기 전에 데이터베이스에 몇 개의 레코드를 삽입해야 할 때가 있습니다. 이때 각 컬럼의 값을 일일이 지정하는 대신, Laravel은 [Eloquent 모델](/docs/12.x/eloquent)마다 기본 속성 집합을 정의하도록 돕는 [모델 팩토리](/docs/12.x/eloquent-factories)를 제공합니다.

모델 팩토리를 생성하고 활용하는 방법에 대해 더 자세히 알고 싶다면 전체 [모델 팩토리 문서](/docs/12.x/eloquent-factories)를 참고하시기 바랍니다. 모델 팩토리가 정의되면, 테스트 내에서 다음과 같이 팩토리를 이용해 모델을 생성할 수 있습니다:

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
## 시더 실행하기 (Running Seeders)

피처 테스트 중에 [데이터베이스 시더](/docs/12.x/seeding)를 사용해 데이터베이스를 채우고 싶으면, `seed` 메서드를 호출할 수 있습니다. 기본적으로 `seed` 메서드는 모든 다른 시더를 실행하는 `DatabaseSeeder`를 실행합니다. 또는 특정 시더 클래스명을 `seed` 메서드에 전달할 수도 있습니다:

```php tab=Pest
<?php

use Database\Seeders\OrderStatusSeeder;
use Database\Seeders\TransactionStatusSeeder;
use Illuminate\Foundation\Testing\RefreshDatabase;

uses(RefreshDatabase::class);

test('orders can be created', function () {
    // 기본 DatabaseSeeder 실행...
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
     * 새 주문 생성 테스트
     */
    public function test_orders_can_be_created(): void
    {
        // 기본 DatabaseSeeder 실행...
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
```

또는 `RefreshDatabase` 트레이트를 사용하는 각 테스트 전에 데이터베이스를 자동으로 시딩하도록 Laravel에 지시할 수도 있습니다. 이 방법은 기본 테스트 클래스에 `$seed` 속성을 정의함으로써 구현할 수 있습니다:

```php
<?php

namespace Tests;

use Illuminate\Foundation\Testing\TestCase as BaseTestCase;

abstract class TestCase extends BaseTestCase
{
    /**
     * 각 테스트 전에 기본 시더를 실행할지 여부를 표시합니다.
     *
     * @var bool
     */
    protected $seed = true;
}
```

`$seed` 속성값이 `true`라면, `RefreshDatabase` 트레이트를 사용하는 각 테스트 전에 `Database\Seeders\DatabaseSeeder` 클래스가 실행됩니다. 그러나 특정 시더만 실행하고 싶다면, 테스트 클래스에 `$seeder` 속성을 정의할 수 있습니다:

```php
use Database\Seeders\OrderStatusSeeder;

/**
 * 각 테스트 전에 특정 시더를 실행합니다.
 *
 * @var string
 */
protected $seeder = OrderStatusSeeder::class;
```

<a name="available-assertions"></a>
## 사용 가능한 어서션 (Available Assertions)

Laravel은 [Pest](https://pestphp.com)나 [PHPUnit](https://phpunit.de) 피처 테스트에서 사용할 수 있는 여러 데이터베이스 관련 어서션을 제공합니다. 아래에서 각 어서션을 설명합니다.

<a name="assert-database-count"></a>
#### assertDatabaseCount

데이터베이스의 특정 테이블에 주어진 개수만큼 레코드가 존재하는지 확인합니다:

```php
$this->assertDatabaseCount('users', 5);
```

<a name="assert-database-empty"></a>
#### assertDatabaseEmpty

데이터베이스의 특정 테이블에 레코드가 하나도 없는지 확인합니다:

```php
$this->assertDatabaseEmpty('users');
```

<a name="assert-database-has"></a>
#### assertDatabaseHas

데이터베이스의 특정 테이블에 주어진 키/값 쿼리 조건과 일치하는 레코드가 존재하는지 확인합니다:

```php
$this->assertDatabaseHas('users', [
    'email' => 'sally@example.com',
]);
```

<a name="assert-database-missing"></a>
#### assertDatabaseMissing

데이터베이스의 특정 테이블에 주어진 키/값 쿼리 조건과 일치하는 레코드가 존재하지 않는지 확인합니다:

```php
$this->assertDatabaseMissing('users', [
    'email' => 'sally@example.com',
]);
```

<a name="assert-deleted"></a>
#### assertSoftDeleted

`assertSoftDeleted` 메서드는 특정 Eloquent 모델이 소프트 삭제(soft delete)되었는지 확인할 때 사용합니다:

```php
$this->assertSoftDeleted($user);
```

<a name="assert-not-deleted"></a>
#### assertNotSoftDeleted

`assertNotSoftDeleted` 메서드는 특정 Eloquent 모델이 소프트 삭제되지 않았는지 확인할 때 사용합니다:

```php
$this->assertNotSoftDeleted($user);
```

<a name="assert-model-exists"></a>
#### assertModelExists

특정 모델 또는 모델 컬렉션이 데이터베이스에 존재하는지 확인합니다:

```php
use App\Models\User;

$user = User::factory()->create();

$this->assertModelExists($user);
```

<a name="assert-model-missing"></a>
#### assertModelMissing

특정 모델 또는 모델 컬렉션이 데이터베이스에 존재하지 않는지 확인합니다:

```php
use App\Models\User;

$user = User::factory()->create();

$user->delete();

$this->assertModelMissing($user);
```

<a name="expects-database-query-count"></a>
#### expectsDatabaseQueryCount

`expectsDatabaseQueryCount` 메서드는 테스트 시작 시 호출하여 테스트 중 실행될 것으로 예상하는 데이터베이스 쿼리의 총 개수를 지정할 수 있습니다. 실제 실행된 쿼리 수가 이 기대값과 정확히 일치하지 않으면 테스트가 실패합니다:

```php
$this->expectsDatabaseQueryCount(5);

// 테스트 실행...
```