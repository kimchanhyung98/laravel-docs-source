# 데이터베이스 테스트

- [소개](#introduction)
    - [각 테스트 후 데이터베이스 초기화](#resetting-the-database-after-each-test)
- [모델 팩토리](#model-factories)
- [시더 실행하기](#running-seeders)
- [사용 가능한 어서션](#available-assertions)

<a name="introduction"></a>
## 소개

Laravel은 데이터베이스 중심 애플리케이션을 보다 쉽게 테스트할 수 있도록 다양한 도구와 어서션을 제공합니다. 또한, Laravel의 모델 팩토리와 시더는 Eloquent 모델 및 관계를 활용하여 테스트 데이터베이스 레코드를 간편하게 생성할 수 있도록 도와줍니다. 이 문서에서는 이러한 강력한 기능들에 대해 설명합니다.

<a name="resetting-the-database-after-each-test"></a>
### 각 테스트 후 데이터베이스 초기화

더 진행하기 전에, 각 테스트 후 데이터베이스를 어떻게 초기화해서 이전 테스트의 데이터가 다음 테스트에 영향을 주지 않도록 할 수 있는지 살펴보겠습니다. Laravel에서 제공하는 `Illuminate\Foundation\Testing\RefreshDatabase` 트레이트가 이를 자동으로 처리해줍니다. 테스트 클래스에서 이 트레이트를 사용하면 됩니다:

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

`Illuminate\Foundation\Testing\RefreshDatabase` 트레이트는 데이터베이스 스키마가 최신 상태이면 마이그레이션을 실행하지 않습니다. 대신, 테스트를 데이터베이스 트랜잭션 내에서 실행합니다. 따라서 이 트레이트를 사용하지 않는 테스트 케이스에서 추가된 레코드는 데이터베이스에 남아있을 수 있습니다.

완전히 데이터베이스를 초기화하고 싶다면, `Illuminate\Foundation\Testing\DatabaseMigrations` 또는 `Illuminate\Foundation\Testing\DatabaseTruncation` 트레이트를 사용할 수 있습니다. 하지만, 이 두 옵션은 `RefreshDatabase` 트레이트보다 상당히 느립니다.

<a name="model-factories"></a>
## 모델 팩토리

테스트를 할 때, 테스트를 실행하기 전에 몇몇 레코드를 데이터베이스에 추가해야 할 수 있습니다. 테스트 데이터를 생성할 때 각 컬럼의 값을 일일이 지정하는 대신, Laravel은 [모델 팩토리](/docs/{{version}}/eloquent-factories)를 사용해 각 [Eloquent 모델](/docs/{{version}}/eloquent)에 대한 기본 속성 집합을 정의할 수 있습니다.

모델 팩토리 생성 및 활용 방법에 대한 자세한 내용은 [모델 팩토리 공식 문서](/docs/{{version}}/eloquent-factories)를 참고하세요. 모델 팩토리를 정의했다면, 테스트에서 모델을 다음과 같이 생성할 수 있습니다:

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
## 시더 실행하기

[데이터베이스 시더](/docs/{{version}}/seeding)를 사용하여 기능 테스트 중에 데이터베이스를 채우고 싶다면 `seed` 메서드를 사용할 수 있습니다. 기본적으로 `seed` 메서드는 `DatabaseSeeder`를 실행하며, 이는 모든 시더를 실행하는 역할을 합니다. 또는 특정 시더 클래스명을 `seed` 메서드에 전달할 수도 있습니다:

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

    // 여러 시더 배열 실행...
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
     * 새 주문 생성 테스트.
     */
    public function test_orders_can_be_created(): void
    {
        // DatabaseSeeder 실행...
        $this->seed();

        // 특정 시더 실행...
        $this->seed(OrderStatusSeeder::class);

        // ...

        // 여러 시더 배열 실행...
        $this->seed([
            OrderStatusSeeder::class,
            TransactionStatusSeeder::class,
            // ...
        ]);
    }
}
```

또한, `RefreshDatabase` 트레이트를 사용하는 각 테스트 전에 Laravel이 자동으로 데이터베이스를 시딩하도록 지정할 수도 있습니다. 이를 위해 기본 테스트 클래스에 `$seed` 프로퍼티를 정의하면 됩니다:

```php
<?php

namespace Tests;

use Illuminate\Foundation\Testing\TestCase as BaseTestCase;

abstract class TestCase extends BaseTestCase
{
    /**
     * 각 테스트 전에 기본 시더를 실행할지 여부를 지정합니다.
     *
     * @var bool
     */
    protected $seed = true;
}
```

`$seed` 프로퍼티가 `true`로 설정되어 있으면, `RefreshDatabase` 트레이트를 사용하는 각 테스트 전에 `Database\Seeders\DatabaseSeeder` 클래스가 실행됩니다. 특정 시더를 지정해 실행하고자 한다면, 테스트 클래스에 `$seeder` 프로퍼티를 정의하면 됩니다:

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

Laravel은 [Pest](https://pestphp.com) 또는 [PHPUnit](https://phpunit.de) 기능 테스트에서 사용할 수 있는 여러 데이터베이스 어서션을 제공합니다. 아래에서 각각의 어서션에 대해 설명합니다.

<a name="assert-database-count"></a>
#### assertDatabaseCount

데이터베이스의 특정 테이블에 특정 개수의 레코드가 존재하는지 확인합니다:

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

데이터베이스의 특정 테이블에 주어진 키/값 쿼리 조건을 만족하는 레코드가 존재하는지 확인합니다:

```php
$this->assertDatabaseHas('users', [
    'email' => 'sally@example.com',
]);
```

<a name="assert-database-missing"></a>
#### assertDatabaseMissing

데이터베이스의 특정 테이블에 주어진 키/값 쿼리 조건에 해당하는 레코드가 존재하지 않는지 확인합니다:

```php
$this->assertDatabaseMissing('users', [
    'email' => 'sally@example.com',
]);
```

<a name="assert-deleted"></a>
#### assertSoftDeleted

`assertSoftDeleted` 메서드는 지정한 Eloquent 모델이 "소프트 삭제(soft deleted)" 되었는지 확인합니다:

```php
$this->assertSoftDeleted($user);
```

<a name="assert-not-deleted"></a>
#### assertNotSoftDeleted

`assertNotSoftDeleted` 메서드는 지정한 Eloquent 모델이 "소프트 삭제"되지 않았는지 확인합니다:

```php
$this->assertNotSoftDeleted($user);
```

<a name="assert-model-exists"></a>
#### assertModelExists

지정한 모델이 데이터베이스에 존재하는지 확인합니다:

```php
use App\Models\User;

$user = User::factory()->create();

$this->assertModelExists($user);
```

<a name="assert-model-missing"></a>
#### assertModelMissing

지정한 모델이 데이터베이스에 존재하지 않는지 확인합니다:

```php
use App\Models\User;

$user = User::factory()->create();

$user->delete();

$this->assertModelMissing($user);
```

<a name="expects-database-query-count"></a>
#### expectsDatabaseQueryCount

`expectsDatabaseQueryCount` 메서드는 테스트 시작 시, 해당 테스트에서 실행될 것으로 예상되는 전체 데이터베이스 쿼리 개수를 지정할 수 있습니다. 실제 실행된 쿼리 개수가 예상과 정확히 일치하지 않으면 테스트가 실패합니다:

```php
$this->expectsDatabaseQueryCount(5);

// 테스트...
```
