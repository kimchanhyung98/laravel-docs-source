# 데이터베이스 테스트 (Database Testing)

- [소개](#introduction)
    - [각 테스트 후 데이터베이스 초기화](#resetting-the-database-after-each-test)
- [모델 팩토리](#model-factories)
- [시더 실행하기](#running-seeders)
- [사용 가능한 어서션](#available-assertions)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 데이터베이스 기반 애플리케이션을 테스트하기 쉽도록 다양한 유용한 도구와 어서션을 제공합니다. 또한, Laravel의 모델 팩토리(model factories)와 시더(seeders)는 Eloquent 모델과 관계(relationships)를 사용하여 테스트 데이터베이스 레코드를 손쉽게 생성할 수 있게 해줍니다. 이 문서에서는 이러한 강력한 기능들을 모두 다룰 것입니다.

<a name="resetting-the-database-after-each-test"></a>
### 각 테스트 후 데이터베이스 초기화 (Resetting the Database After Each Test)

본격적으로 살펴보기 전에, 이전 테스트 데이터가 이후 테스트에 영향을 주지 않도록 각 테스트 후 데이터베이스를 초기화하는 방법을 다루겠습니다. Laravel에서 제공하는 `Illuminate\Foundation\Testing\RefreshDatabase` 트레이트를 사용하면 이를 자동으로 처리해줍니다. 테스트 클래스에서 이 트레이트를 사용하기만 하면 됩니다:

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
     * 간단한 기능 테스트 예제
     */
    public function test_basic_example(): void
    {
        $response = $this->get('/');

        // ...
    }
}
```

`Illuminate\Foundation\Testing\RefreshDatabase` 트레이트는 데이터베이스 스키마가 최신 상태라면 마이그레이션을 수행하지 않고, 오직 데이터베이스 트랜잭션 내에서 테스트를 실행합니다. 따라서 이 트레이트를 사용하지 않는 테스트가 데이터베이스에 추가한 레코드가 남아있을 수 있습니다.

데이터베이스를 완전 초기화하고 싶다면 `Illuminate\Foundation\Testing\DatabaseMigrations` 또는 `Illuminate\Foundation\Testing\DatabaseTruncation` 트레이트를 사용할 수도 있습니다. 하지만 이 두 방법은 `RefreshDatabase`보다 훨씬 느리다는 점을 유념하세요.

<a name="model-factories"></a>
## 모델 팩토리 (Model Factories)

테스트를 진행할 때, 데이터베이스에 몇몇 레코드를 미리 삽입해야 할 수 있습니다. 이때 각 컬럼의 값을 일일이 지정하는 대신, Laravel에서는 [Eloquent 모델](/docs/master/eloquent)마다 기본 속성 집합을 정의할 수 있도록 [모델 팩토리](/docs/master/eloquent-factories)를 제공합니다.

모델 팩토리를 생성하고 사용하는 방법에 대해서는 완전한 [모델 팩토리 문서](/docs/master/eloquent-factories)를 참고하세요. 모델 팩토리를 정의한 뒤에는 테스트 내에서 다음과 같이 팩토리를 사용해 모델을 생성할 수 있습니다:

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

기능 테스트 중에 [데이터베이스 시더](/docs/master/seeding)를 사용해 데이터베이스를 채우고 싶다면 `seed` 메서드를 호출할 수 있습니다. 기본적으로 `seed` 메서드는 모든 시더를 실행하는 `DatabaseSeeder`를 호출합니다. 특정 시더 클래스를 지정해서 실행할 수도 있습니다:

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

    // 여러 시더를 배열로 실행...
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
     * 새로운 주문 생성 테스트
     */
    public function test_orders_can_be_created(): void
    {
        // 기본 DatabaseSeeder 실행...
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

또는 `RefreshDatabase` 트레이트를 사용하는 각 테스트 실행 전 자동으로 시더를 작동시키도록 할 수도 있습니다. 이를 위해 베이스 테스트 클래스에 `$seed` 속성을 정의하세요:

```php
<?php

namespace Tests;

use Illuminate\Foundation\Testing\TestCase as BaseTestCase;

abstract class TestCase extends BaseTestCase
{
    /**
     * 기본 시더를 각 테스트 전에 실행할지 여부
     *
     * @var bool
     */
    protected $seed = true;
}
```

`$seed`가 `true`일 경우, `RefreshDatabase`를 사용하는 각 테스트 전에 `Database\Seeders\DatabaseSeeder` 클래스가 실행됩니다. 특정 시더를 지정하려면 테스트 클래스에 `$seeder` 속성을 정의할 수도 있습니다:

```php
use Database\Seeders\OrderStatusSeeder;

/**
 * 각 테스트 전에 특정 시더 실행
 *
 * @var string
 */
protected $seeder = OrderStatusSeeder::class;
```

<a name="available-assertions"></a>
## 사용 가능한 어서션 (Available Assertions)

Laravel은 [Pest](https://pestphp.com) 또는 [PHPUnit](https://phpunit.de) 기능 테스트에서 사용할 수 있는 여러 데이터베이스 어서션을 제공합니다. 아래에서 각 어서션에 대해 설명합니다.

<a name="assert-database-count"></a>
#### assertDatabaseCount

지정한 테이블의 레코드 개수가 기대하는 수와 같은지 검증합니다:

```php
$this->assertDatabaseCount('users', 5);
```

<a name="assert-database-empty"></a>
#### assertDatabaseEmpty

지정한 테이블에 레코드가 하나도 없는지 검증합니다:

```php
$this->assertDatabaseEmpty('users');
```

<a name="assert-database-has"></a>
#### assertDatabaseHas

지정한 테이블에 주어진 키/값 쿼리 조건과 일치하는 레코드가 존재하는지 검증합니다:

```php
$this->assertDatabaseHas('users', [
    'email' => 'sally@example.com',
]);
```

<a name="assert-database-missing"></a>
#### assertDatabaseMissing

지정한 테이블에 주어진 키/값 쿼리 조건과 일치하는 레코드가 존재하지 않는지 검증합니다:

```php
$this->assertDatabaseMissing('users', [
    'email' => 'sally@example.com',
]);
```

<a name="assert-deleted"></a>
#### assertSoftDeleted

`assertSoftDeleted` 메서드는 주어진 Eloquent 모델이 "소프트 삭제(soft deleted)" 되었는지 검증하는 데 사용됩니다:

```php
$this->assertSoftDeleted($user);
```

<a name="assert-not-deleted"></a>
#### assertNotSoftDeleted

`assertNotSoftDeleted` 메서드는 주어진 Eloquent 모델이 "소프트 삭제" 되지 않았음을 검증하는 데 사용됩니다:

```php
$this->assertNotSoftDeleted($user);
```

<a name="assert-model-exists"></a>
#### assertModelExists

지정한 모델이 데이터베이스에 존재하는지 검증합니다:

```php
use App\Models\User;

$user = User::factory()->create();

$this->assertModelExists($user);
```

<a name="assert-model-missing"></a>
#### assertModelMissing

지정한 모델이 데이터베이스에 존재하지 않음을 검증합니다:

```php
use App\Models\User;

$user = User::factory()->create();

$user->delete();

$this->assertModelMissing($user);
```

<a name="expects-database-query-count"></a>
#### expectsDatabaseQueryCount

`expectsDatabaseQueryCount` 메서드는 테스트 시작 시 호출하여 테스트 동안 실행될 데이터베이스 쿼리 수를 명확히 지정할 수 있습니다. 실행된 쿼리 수가 기대치와 정확히 일치하지 않으면 테스트가 실패합니다:

```php
$this->expectsDatabaseQueryCount(5);

// 테스트 진행...
```