# 데이터베이스 테스트

- [소개](#introduction)
    - [각 테스트 후 데이터베이스 리셋](#resetting-the-database-after-each-test)
- [모델 팩토리](#model-factories)
- [시더 실행](#running-seeders)
- [사용 가능한 단언](#available-assertions)

<a name="introduction"></a>
## 소개

Laravel은 데이터베이스 기반 애플리케이션을 보다 쉽게 테스트할 수 있도록 다양한 유용한 도구와 단언을 제공합니다. 또한, Laravel의 모델 팩토리와 시더를 사용하면 Eloquent 모델과 관계를 활용하여 테스트용 데이터베이스 레코드를 손쉽게 생성할 수 있습니다. 이 문서에서는 이러한 강력한 기능에 대해 다룹니다.

<a name="resetting-the-database-after-each-test"></a>
### 각 테스트 후 데이터베이스 리셋

본격적으로 진행하기에 앞서, 이전 테스트의 데이터가 이후 테스트에 영향을 미치지 않도록 각 테스트 후 데이터베이스를 어떻게 초기화할 수 있는지 알아보겠습니다. Laravel에 포함된 `Illuminate\Foundation\Testing\RefreshDatabase` 트레이트를 사용하면 이 작업을 자동으로 처리할 수 있습니다. 이 트레이트를 테스트 클래스에 사용하세요:

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
     * 기본 기능 테스트 예제.
     */
    public function test_basic_example(): void
    {
        $response = $this->get('/');

        // ...
    }
}
```

`Illuminate\Foundation\Testing\RefreshDatabase` 트레이트는 데이터베이스 스키마가 최신 상태라면 마이그레이션을 실행하지 않습니다. 대신, 테스트를 데이터베이스 트랜잭션 내에서 실행합니다. 따라서 이 트레이트를 사용하지 않는 테스트 케이스로 추가된 레코드는 여전히 데이터베이스에 남아 있을 수 있습니다.

데이터베이스를 완전히 초기화하려면 `Illuminate\Foundation\Testing\DatabaseMigrations` 또는 `Illuminate\Foundation\Testing\DatabaseTruncation` 트레이트를 사용할 수 있습니다. 하지만 이 두 방법은 `RefreshDatabase` 트레이트에 비해 상당히 느립니다.

<a name="model-factories"></a>
## 모델 팩토리

테스트 중에는 테스트 실행 전 데이터베이스에 몇몇 레코드를 삽입해야 할 수도 있습니다. 이런 테스트 데이터를 생성할 때 각 컬럼의 값을 일일이 지정하지 않아도, Laravel에서는 [모델 팩토리](/docs/{{version}}/eloquent-factories)를 활용하여 각 [Eloquent 모델](/docs/{{version}}/eloquent)의 기본 속성 집합을 정의할 수 있습니다.

모델 팩토리를 생성하고 사용하는 방법에 대한 자세한 내용은 [모델 팩토리 공식 문서](/docs/{{version}}/eloquent-factories)를 참고하세요. 모델 팩토리를 정의한 후에는, 테스트 내에서 팩토리를 이용해 모델을 생성할 수 있습니다:

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

[데이터베이스 시더](/docs/{{version}}/seeding)를 사용해 기능 테스트 동안 데이터베이스에 데이터를 추가하고 싶다면, `seed` 메서드를 사용할 수 있습니다. 기본적으로 `seed` 메서드는 `DatabaseSeeder`를 실행하며, 이 시더에서 다른 모든 시더를 실행해야 합니다. 또는 특정 시더 클래스명을 `seed` 메서드에 전달할 수도 있습니다:

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

또는, `RefreshDatabase` 트레이트를 사용하는 각 테스트 전에 Laravel이 자동으로 데이터베이스를 시딩하도록 할 수도 있습니다. 이를 위해 기반 테스트 클래스에 `$seed` 프로퍼티를 정의하면 됩니다:

```php
<?php

namespace Tests;

use Illuminate\Foundation\Testing\TestCase as BaseTestCase;

abstract class TestCase extends BaseTestCase
{
    /**
     * 모든 테스트 전에 기본 시더를 실행할지 여부.
     *
     * @var bool
     */
    protected $seed = true;
}
```

`$seed` 프로퍼티가 `true`일 경우, `RefreshDatabase` 트레이트를 사용하는 각 테스트 전에 `Database\Seeders\DatabaseSeeder` 클래스가 실행됩니다. 만일, 특정 시더만 실행하고 싶다면 테스트 클래스에 `$seeder` 프로퍼티를 정의하면 됩니다:

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
## 사용 가능한 단언

Laravel은 [Pest](https://pestphp.com) 또는 [PHPUnit](https://phpunit.de) 기능 테스트를 위한 다양한 데이터베이스 단언 메서드를 제공합니다. 아래에서 각 단언에 대해 살펴보겠습니다.

<a name="assert-database-count"></a>
#### assertDatabaseCount

데이터베이스의 특정 테이블에 지정한 개수의 레코드가 존재하는지 단언합니다:

```php
$this->assertDatabaseCount('users', 5);
```

<a name="assert-database-empty"></a>
#### assertDatabaseEmpty

데이터베이스의 특정 테이블에 레코드가 존재하지 않는지 단언합니다:

```php
$this->assertDatabaseEmpty('users');
```

<a name="assert-database-has"></a>
#### assertDatabaseHas

특정 키/값 쿼리 조건과 일치하는 레코드가 데이터베이스 테이블에 존재하는지 단언합니다:

```php
$this->assertDatabaseHas('users', [
    'email' => 'sally@example.com',
]);
```

<a name="assert-database-missing"></a>
#### assertDatabaseMissing

특정 키/값 쿼리 조건과 일치하는 레코드가 데이터베이스 테이블에 존재하지 않는지 단언합니다:

```php
$this->assertDatabaseMissing('users', [
    'email' => 'sally@example.com',
]);
```

<a name="assert-deleted"></a>
#### assertSoftDeleted

`assertSoftDeleted` 메서드는 주어진 Eloquent 모델이 "소프트 삭제" 되었는지 단언할 수 있습니다:

```php
$this->assertSoftDeleted($user);
```

<a name="assert-not-deleted"></a>
#### assertNotSoftDeleted

`assertNotSoftDeleted` 메서드는 주어진 Eloquent 모델이 "소프트 삭제"되지 않았는지 단언할 수 있습니다:

```php
$this->assertNotSoftDeleted($user);
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

<a name="expects-database-query-count"></a>
#### expectsDatabaseQueryCount

`expectsDatabaseQueryCount` 메서드는 테스트가 실행되는 동안 수행될 것으로 기대하는 전체 데이터베이스 쿼리 수를 명시할 때 사용할 수 있습니다. 실제 쿼리 수가 기대치와 정확히 일치하지 않으면 테스트는 실패합니다:

```php
$this->expectsDatabaseQueryCount(5);

// 테스트 코드...
```
