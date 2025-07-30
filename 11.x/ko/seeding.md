# 데이터베이스: 시딩 (Database: Seeding)

- [소개](#introduction)
- [시더 작성하기](#writing-seeders)
    - [모델 팩토리 사용하기](#using-model-factories)
    - [추가 시더 호출하기](#calling-additional-seeders)
    - [모델 이벤트 비활성화하기](#muting-model-events)
- [시더 실행하기](#running-seeders)

<a name="introduction"></a>
## 소개

Laravel은 시더 클래스를 사용하여 데이터베이스에 데이터를 추가하는 기능을 제공합니다. 모든 시더 클래스는 `database/seeders` 디렉토리에 저장됩니다. 기본적으로 `DatabaseSeeder` 클래스가 정의되어 있으며, 이 클래스 내에서 `call` 메서드를 사용해 다른 시더 클래스를 실행할 수 있어 시딩 순서를 제어할 수 있습니다.

> [!NOTE]  
> 데이터베이스 시딩 중에는 [대량 할당 보호](/docs/11.x/eloquent#mass-assignment)가 자동으로 비활성화됩니다.

<a name="writing-seeders"></a>
## 시더 작성하기

시더를 생성하려면 `make:seeder` [Artisan 명령어](/docs/11.x/artisan)를 실행하세요. 프레임워크에서 생성된 모든 시더는 `database/seeders` 디렉토리에 위치합니다:

```shell
php artisan make:seeder UserSeeder
```

시더 클래스는 기본적으로 단 하나의 메서드, `run`만 포함합니다. 이 메서드는 `db:seed` [Artisan 명령어](/docs/11.x/artisan) 실행 시 호출됩니다. `run` 메서드 내에서 원하는 방식으로 데이터베이스에 데이터를 삽입할 수 있습니다. [쿼리 빌더](/docs/11.x/queries)를 사용하여 수동 삽입하거나 [Eloquent 모델 팩토리](/docs/11.x/eloquent-factories)를 사용할 수도 있습니다.

예를 들어, 기본 `DatabaseSeeder` 클래스의 `run` 메서드에 데이터베이스 삽입 구문을 추가해봅시다:

```
<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Str;

class DatabaseSeeder extends Seeder
{
    /**
     * Run the database seeders.
     */
    public function run(): void
    {
        DB::table('users')->insert([
            'name' => Str::random(10),
            'email' => Str::random(10).'@example.com',
            'password' => Hash::make('password'),
        ]);
    }
}
```

> [!NOTE]  
> `run` 메서드 시그니처에 필요한 의존성을 타입 힌트로 선언하면 Laravel의 [서비스 컨테이너](/docs/11.x/container)를 통해 자동 주입됩니다.

<a name="using-model-factories"></a>
### 모델 팩토리 사용하기

모델의 속성을 일일이 지정하는 것은 번거롭습니다. 대신, [모델 팩토리](/docs/11.x/eloquent-factories)를 사용하면 대량의 데이터 레코드를 편리하게 생성할 수 있습니다. 먼저, [모델 팩토리 문서](/docs/11.x/eloquent-factories)를 참고하여 팩토리 정의 방법을 숙지하세요.

예를 들어, 각 사용자마다 하나의 연관된 게시물을 가진 50명의 사용자를 생성하려면 다음과 같이 작성합니다:

```
use App\Models\User;

/**
 * Run the database seeders.
 */
public function run(): void
{
    User::factory()
        ->count(50)
        ->hasPosts(1)
        ->create();
}
```

<a name="calling-additional-seeders"></a>
### 추가 시더 호출하기

`DatabaseSeeder` 클래스 내에서는 `call` 메서드를 사용해 여러 시더 클래스를 실행할 수 있습니다. 이를 통해 데이터베이스 시딩을 여러 파일로 분리하여 하나의 시더 클래스가 너무 커지는 것을 방지할 수 있습니다. `call` 메서드는 실행할 시더 클래스 배열을 인수로 받습니다:

```
/**
 * Run the database seeders.
 */
public function run(): void
{
    $this->call([
        UserSeeder::class,
        PostSeeder::class,
        CommentSeeder::class,
    ]);
}
```

<a name="muting-model-events"></a>
### 모델 이벤트 비활성화하기

시딩하는 동안 모델에서 이벤트가 발생하는 것을 원하지 않을 수 있습니다. 이때 `WithoutModelEvents` 트레이트를 사용하면 됩니다. 해당 트레이트를 활용하면, `call` 메서드로 추가 시더를 실행할 때조차 모델 이벤트가 발생하지 않도록 보장합니다:

```
<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Database\Console\Seeds\WithoutModelEvents;

class DatabaseSeeder extends Seeder
{
    use WithoutModelEvents;

    /**
     * Run the database seeders.
     */
    public function run(): void
    {
        $this->call([
            UserSeeder::class,
        ]);
    }
}
```

<a name="running-seeders"></a>
## 시더 실행하기

`db:seed` Artisan 명령어를 실행해 데이터베이스에 시딩할 수 있습니다. 기본적으로 `db:seed` 명령은 `Database\Seeders\DatabaseSeeder` 클래스를 실행하며, 이 클래스에서 다른 시더를 호출할 수 있습니다. 또한 `--class` 옵션으로 특정 시더 클래스를 지정하여 개별적으로 실행할 수도 있습니다:

```shell
php artisan db:seed

php artisan db:seed --class=UserSeeder
```

`migrate:fresh` 명령어에 `--seed` 옵션을 함께 사용하면, 모든 테이블을 삭제한 후 마이그레이션을 재실행하고 시딩까지 한 번에 수행합니다. 이는 데이터베이스를 완전히 재구성할 때 편리합니다. 특정 시더를 지정하려면 `--seeder` 옵션을 사용할 수 있습니다:

```shell
php artisan migrate:fresh --seed

php artisan migrate:fresh --seed --seeder=UserSeeder
```

<a name="forcing-seeding-production"></a>
#### 프로덕션 환경에서 시더 강제 실행하기

일부 시딩 작업은 데이터 변경이나 손실을 일으킬 수 있기 때문에 프로덕션 환경에서 시더 실행 시 확인 메시지가 표시됩니다. 확인 절차 없이 시더를 실행하려면 `--force` 옵션을 사용하세요:

```shell
php artisan db:seed --force
```