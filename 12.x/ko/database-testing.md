# 데이터베이스 테스트 (Database Testing)

- [소개](#introduction)
    - [각 테스트 후 데이터베이스 초기화](#resetting-the-database-after-each-test)
- [모델 팩토리](#model-factories)
- [시더 실행](#running-seeders)
- [사용 가능한 assertion](#available-assertions)

<a name="introduction"></a>
## 소개

라라벨은 데이터베이스를 사용하는 애플리케이션을 테스트할 때 다양한 유용한 도구와 assertion을 제공합니다. 또한, 라라벨의 모델 팩토리와 시더를 활용하면, Eloquent 모델과 연관 관계를 이용해 테스트용 데이터베이스 레코드를 손쉽게 생성할 수 있습니다. 이 문서에서는 이러한 강력한 기능들을 자세히 알아봅니다.

<a name="resetting-the-database-after-each-test"></a>
### 각 테스트 후 데이터베이스 초기화

이제 본격적으로 시작하기 전에, 각 테스트가 끝날 때마다 데이터베이스를 어떻게 초기화하는지부터 알아보겠습니다. 이를 통해 이전 테스트의 데이터가 다음 테스트에 영향을 끼치지 않도록 할 수 있습니다. 라라벨에 내장된 `Illuminate\Foundation\Testing\RefreshDatabase` 트레이트를 사용하면 이 과정을 간단하게 처리할 수 있습니다. 아래와 같이 테스트 클래스에 해당 트레이트를 추가하면 됩니다.

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
     * A basic functional test example.
     */
    public function test_basic_example(): void
    {
        $response = $this->get('/');

        // ...
    }
}
```

`Illuminate\Foundation\Testing\RefreshDatabase` 트레이트는 데이터베이스 스키마가 최신 상태라면 마이그레이션을 실행하지 않습니다. 대신, 각각의 테스트를 데이터베이스 트랜잭션 안에서 실행합니다. 따라서 이 트레이트를 사용하지 않는 테스트 케이스에서 추가한 레코드는 여전히 데이터베이스에 남아있을 수 있습니다.

만약 데이터베이스를 완전히 초기화하고 싶다면, `Illuminate\Foundation\Testing\DatabaseMigrations` 또는 `Illuminate\Foundation\Testing\DatabaseTruncation` 트레이트를 사용할 수 있습니다. 하지만 이 두 방법은 `RefreshDatabase` 트레이트에 비해 상당히 느리다는 점을 참고하세요.

<a name="model-factories"></a>
## 모델 팩토리

테스트를 작성할 때, 테스트 실행 전에 데이터베이스에 몇 개의 레코드를 삽입해야 할 수 있습니다. 이때 매번 모든 컬럼의 값을 직접 지정하는 대신, 라라벨에서는 각 [Eloquent 모델](/docs/12.x/eloquent)마다 [모델 팩토리](/docs/12.x/eloquent-factories)를 통해 기본 속성 값을 미리 정의해둘 수 있습니다.

모델 팩토리를 생성하고 활용하는 방법에 대해 더 자세히 알고 싶다면, [모델 팩토리 공식 문서](/docs/12.x/eloquent-factories)를 참고하시기 바랍니다. 모델 팩토리를 정의한 후에는 테스트에서 팩토리를 사용해 간단히 모델을 생성할 수 있습니다.

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
## 시더 실행

[데이터베이스 시더](/docs/12.x/seeding)를 사용해 기능 테스트를 진행하는 동안 데이터베이스를 채우고 싶다면, `seed` 메서드를 사용할 수 있습니다. 기본적으로 `seed` 메서드는 `DatabaseSeeder`를 실행하며, 이 클래스에서 다른 모든 시더들이 실행되도록 구성되어 있습니다. 또는, `seed` 메서드에 원하는 특정 시더 클래스명을 전달해 특정 시더만 실행할 수도 있습니다.

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

또는, 각 테스트마다 `RefreshDatabase` 트레이트를 사용하는 경우, 테스트가 실행되기 전마다 자동으로 시더를 돌릴 수 있습니다. 이를 위해 기본 테스트 클래스에 `$seed` 프로퍼티를 정의하면 됩니다.

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

`$seed` 프로퍼티가 `true`면, 테스트에서 `RefreshDatabase` 트레이트를 사용할 때마다 `Database\Seeders\DatabaseSeeder` 클래스가 먼저 실행됩니다. 만약 특정 시더만 실행하고 싶다면, 테스트 클래스에서 `$seeder` 프로퍼티로 지정할 수 있습니다.

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
## 사용 가능한 assertion

라라벨은 [Pest](https://pestphp.com) 또는 [PHPUnit](https://phpunit.de) 기반의 기능 테스트에서 여러 가지 데이터베이스 assertion을 제공합니다. 아래에서 각각의 assertion을 설명합니다.

<a name="assert-database-count"></a>
#### assertDatabaseCount

데이터베이스의 특정 테이블에 지정한 개수의 레코드가 있는지 확인합니다.

```php
$this->assertDatabaseCount('users', 5);
```

<a name="assert-database-empty"></a>
#### assertDatabaseEmpty

데이터베이스의 특정 테이블에 레코드가 아무것도 없는지 확인합니다.

```php
$this->assertDatabaseEmpty('users');
```

<a name="assert-database-has"></a>
#### assertDatabaseHas

특정 키/값 조건을 만족하는 레코드가 데이터베이스의 테이블에 존재하는지 확인합니다.

```php
$this->assertDatabaseHas('users', [
    'email' => 'sally@example.com',
]);
```

<a name="assert-database-missing"></a>
#### assertDatabaseMissing

특정 키/값 조건을 만족하는 레코드가 데이터베이스의 테이블에 존재하지 않는지 확인합니다.

```php
$this->assertDatabaseMissing('users', [
    'email' => 'sally@example.com',
]);
```

<a name="assert-deleted"></a>
#### assertSoftDeleted

`assertSoftDeleted` 메서드는 주어진 Eloquent 모델이 "소프트 삭제" 상태인지 확인할 때 사용합니다.

```php
$this->assertSoftDeleted($user);
```

<a name="assert-not-deleted"></a>
#### assertNotSoftDeleted

`assertNotSoftDeleted` 메서드는 주어진 Eloquent 모델이 "소프트 삭제" 되지 않았는지 확인할 때 사용합니다.

```php
$this->assertNotSoftDeleted($user);
```

<a name="assert-model-exists"></a>
#### assertModelExists

지정한 모델 또는 모델 컬렉션이 데이터베이스에 실제로 존재하는지 확인합니다.

```php
use App\Models\User;

$user = User::factory()->create();

$this->assertModelExists($user);
```

<a name="assert-model-missing"></a>
#### assertModelMissing

지정한 모델 또는 모델 컬렉션이 데이터베이스에 존재하지 않는지 확인합니다.

```php
use App\Models\User;

$user = User::factory()->create();

$user->delete();

$this->assertModelMissing($user);
```

<a name="expects-database-query-count"></a>
#### expectsDatabaseQueryCount

`expectsDatabaseQueryCount` 메서드는 테스트가 시작될 때 이 테스트에서 실행되기를 기대하는 데이터베이스 쿼리의 총 개수를 지정할 수 있게 해줍니다. 실제 실행된 쿼리 수가 기대한 수와 정확히 일치하지 않으면, 테스트가 실패하게 됩니다.

```php
$this->expectsDatabaseQueryCount(5);

// Test...
```
