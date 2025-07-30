# 데이터베이스 테스트 (Database Testing)

- [소개](#introduction)
    - [각 테스트 후 데이터베이스 초기화](#resetting-the-database-after-each-test)
- [모델 팩토리](#model-factories)
- [시더 실행하기](#running-seeders)
- [사용 가능한 어서션](#available-assertions)

<a name="introduction"></a>
## 소개

Laravel은 데이터베이스 기반 애플리케이션 테스트를 더 쉽게 만들기 위한 다양한 유용한 도구와 어서션을 제공합니다. 또한, Laravel의 모델 팩토리(model factories)와 시더(seeders)는 애플리케이션의 Eloquent 모델과 연관관계를 사용해서 테스트용 데이터베이스 레코드를 쉽게 생성할 수 있게 도와줍니다. 다음 문서에서 이러한 강력한 기능들을 자세히 다루겠습니다.

<a name="resetting-the-database-after-each-test"></a>
### 각 테스트 후 데이터베이스 초기화

앞으로 진행하기 전에, 이전 테스트의 데이터가 다음 테스트에 영향을 미치지 않도록 각 테스트가 끝난 후 데이터베이스를 초기화하는 방법을 알아보겠습니다. Laravel에서 기본으로 제공하는 `Illuminate\Foundation\Testing\RefreshDatabase` 트레이트가 이 작업을 자동으로 처리해 줍니다. 테스트 클래스에서 이 트레이트를 사용하기만 하면 됩니다.

```
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

`Illuminate\Foundation\Testing\RefreshDatabase` 트레이트는 스키마가 최신 상태라면 데이터베이스 마이그레이션을 실행하지 않습니다. 대신, 데이터베이스 트랜잭션 내에서 테스트를 수행합니다. 따라서 이 트레이트를 사용하지 않는 테스트 케이스에서 추가된 레코드는 데이터베이스에 남아 있을 수 있습니다.

데이터베이스를 완전히 초기화하고 싶다면 `Illuminate\Foundation\Testing\DatabaseMigrations` 또는 `Illuminate\Foundation\Testing\DatabaseTruncation` 트레이트를 사용할 수 있습니다. 다만, 이 두 옵션은 `RefreshDatabase` 트레이트에 비해 훨씬 느립니다.

<a name="model-factories"></a>
## 모델 팩토리

테스트를 수행할 때, 테스트 실행 전 데이터베이스에 몇 개의 레코드를 삽입해야 할 때가 있습니다. 이때, 각 컬럼의 값을 일일이 지정하는 대신 Laravel은 [Eloquent 모델](/docs/10.x/eloquent)별 기본 속성 집합을 정의할 수 있는 [모델 팩토리](/docs/10.x/eloquent-factories) 기능을 제공합니다.

모델 팩토리를 생성하고 활용하는 방법에 대해 더 알고 싶다면, [모델 팩토리 문서](/docs/10.x/eloquent-factories)를 참조하세요. 모델 팩토리를 정의한 후에는 테스트 코드 내에서 다음과 같이 모델을 생성할 수 있습니다.

```
use App\Models\User;

public function test_models_can_be_instantiated(): void
{
    $user = User::factory()->create();

    // ...
}
```

<a name="running-seeders"></a>
## 시더 실행하기

만약 기능 테스트 중 [데이터베이스 시더](/docs/10.x/seeding)를 사용해 데이터베이스를 채우고 싶다면, `seed` 메서드를 호출하면 됩니다. 기본적으로 `seed` 메서드는 모든 시더를 실행하는 `DatabaseSeeder`를 실행합니다. 또는 특정 시더 클래스를 인수로 전달할 수도 있습니다.

```
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

        // 복수 시더 실행...
        $this->seed([
            OrderStatusSeeder::class,
            TransactionStatusSeeder::class,
            // ...
        ]);
    }
}
```

또는 `RefreshDatabase` 트레이트를 사용하는 각 테스트마다 Laravel이 자동으로 시드를 실행하도록 할 수도 있습니다. 이것은 기본 테스트 클래스에 `$seed` 속성을 정의하여 설정합니다.

```
<?php

namespace Tests;

use Illuminate\Foundation\Testing\TestCase as BaseTestCase;

abstract class TestCase extends BaseTestCase
{
    use CreatesApplication;

    /**
     * 각 테스트 전에 기본 시더 실행 여부를 나타냅니다.
     *
     * @var bool
     */
    protected $seed = true;
}
```

`$seed`가 `true`라면, `RefreshDatabase` 트레이트를 사용하는 각 테스트 전에 `Database\Seeders\DatabaseSeeder` 클래스가 실행됩니다. 또한, 특정 시더를 실행하도록 `$seeder` 속성을 테스트 클래스에 정의할 수도 있습니다.

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
## 사용 가능한 어서션

Laravel은 [PHPUnit](https://phpunit.de/) 기능 테스트를 위한 여러 데이터베이스 어서션을 제공합니다. 아래에서 각 어서션을 설명합니다.

<a name="assert-database-count"></a>
#### assertDatabaseCount

데이터베이스 내 특정 테이블의 레코드 수가 지정한 수와 일치하는지 검증합니다:

```
$this->assertDatabaseCount('users', 5);
```

<a name="assert-database-has"></a>
#### assertDatabaseHas

주어진 키/값 쿼리 조건과 일치하는 레코드가 특정 테이블에 존재하는지 검증합니다:

```
$this->assertDatabaseHas('users', [
    'email' => 'sally@example.com',
]);
```

<a name="assert-database-missing"></a>
#### assertDatabaseMissing

주어진 키/값 쿼리 조건과 일치하는 레코드가 특정 테이블에 존재하지 않는지 검증합니다:

```
$this->assertDatabaseMissing('users', [
    'email' => 'sally@example.com',
]);
```

<a name="assert-deleted"></a>
#### assertSoftDeleted

`assertSoftDeleted` 메서드는 특정 Eloquent 모델이 "소프트 삭제(soft deleted)"된 상태인지 검증할 때 사용합니다:

```
$this->assertSoftDeleted($user);
```

<a name="assert-not-deleted"></a>
#### assertNotSoftDeleted

`assertNotSoftDeleted` 메서드는 특정 Eloquent 모델이 "소프트 삭제"되지 않은 상태인지 검증할 때 사용합니다:

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

주어진 모델이 데이터베이스에 존재하지 않는지 검증합니다:

```
use App\Models\User;

$user = User::factory()->create();

$user->delete();

$this->assertModelMissing($user);
```

<a name="expects-database-query-count"></a>
#### expectsDatabaseQueryCount

`expectsDatabaseQueryCount` 메서드는 테스트 시작 시 호출하여 테스트 중 실행될 데이터베이스 쿼리의 예상 횟수를 지정합니다. 실제 쿼리 실행 횟수가 이 예상과 정확히 일치하지 않으면 테스트는 실패합니다:

```
$this->expectsDatabaseQueryCount(5);

// 테스트 실행...
```