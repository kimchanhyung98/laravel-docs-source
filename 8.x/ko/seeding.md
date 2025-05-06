# Database: Seeding

- [소개](#introduction)
- [시더 작성하기](#writing-seeders)
    - [모델 팩토리 사용하기](#using-model-factories)
    - [추가 시더 호출하기](#calling-additional-seeders)
- [시더 실행하기](#running-seeders)

<a name="introduction"></a>
## 소개

Laravel은 시드 클래스를 사용하여 데이터베이스에 데이터를 시드할 수 있는 기능을 제공합니다. 모든 시드 클래스는 `database/seeders` 디렉터리에 저장됩니다. 기본적으로 `DatabaseSeeder` 클래스가 정의되어 있습니다. 이 클래스에서 `call` 메서드를 사용하여 다른 시드 클래스를 실행할 수 있으며, 이를 통해 시드 실행 순서를 제어할 수 있습니다.

> {tip} [대량 할당 보호](/docs/{{version}}/eloquent#mass-assignment)는 데이터베이스 시딩 중에 자동으로 비활성화됩니다.

<a name="writing-seeders"></a>
## 시더 작성하기

시더를 생성하려면 `make:seeder` [Artisan 명령어](/docs/{{version}}/artisan)를 실행하세요. 프레임워크에서 생성된 모든 시더는 `database/seeders` 디렉터리에 위치하게 됩니다:

    php artisan make:seeder UserSeeder

시더 클래스는 기본적으로 한 개의 메서드만 포함합니다: `run`. 이 메서드는 `db:seed` [Artisan 명령어](/docs/{{version}}/artisan)가 실행될 때 호출됩니다. `run` 메서드 내에서는 원하는 방식으로 데이터베이스에 데이터를 삽입할 수 있습니다. [쿼리 빌더](/docs/{{version}}/queries)를 사용하여 직접 데이터를 삽입하거나, [Eloquent 모델 팩토리](/docs/{{version}}/database-testing#defining-model-factories)를 사용할 수 있습니다.

예시로, 기본 `DatabaseSeeder` 클래스를 수정하여 `run` 메서드에 데이터베이스 삽입 코드를 추가해보겠습니다:

```php
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
     *
     * @return void
     */
    public function run()
    {
        DB::table('users')->insert([
            'name' => Str::random(10),
            'email' => Str::random(10).'@gmail.com',
            'password' => Hash::make('password'),
        ]);
    }
}
```

> {tip} `run` 메서드의 시그니처에서 필요한 의존성을 타입힌트로 지정할 수 있습니다. 이들은 Laravel [서비스 컨테이너](/docs/{{version}}/container)를 통해 자동으로 주입됩니다.

<a name="using-model-factories"></a>
### 모델 팩토리 사용하기

물론, 각 모델 시드에 대한 속성을 수동으로 지정하는 것은 번거로울 수 있습니다. 대신, [모델 팩토리](/docs/{{version}}/database-testing#defining-model-factories)를 사용하면 대량의 데이터베이스 레코드를 손쉽게 생성할 수 있습니다. 먼저 [모델 팩토리 문서](/docs/{{version}}/database-testing#defining-model-factories)를 참고하여 팩토리를 정의하는 방법을 익히세요.

예를 들어, 각각 하나의 관련 포스트를 가진 사용자를 50명 생성해보겠습니다:

```php
use App\Models\User;

/**
 * Run the database seeders.
 *
 * @return void
 */
public function run()
{
    User::factory()
        ->count(50)
        ->hasPosts(1)
        ->create();
}
```

<a name="calling-additional-seeders"></a>
### 추가 시더 호출하기

`DatabaseSeeder` 클래스 내에서 `call` 메서드를 사용하여 추가 시드 클래스를 실행할 수 있습니다. `call` 메서드를 활용하면 하나의 시더 클래스가 너무 커지지 않도록 여러 파일로 시딩 작업을 분리할 수 있습니다. `call` 메서드는 실행할 시더 클래스 배열을 인자로 받습니다:

```php
/**
 * Run the database seeders.
 *
 * @return void
 */
public function run()
{
    $this->call([
        UserSeeder::class,
        PostSeeder::class,
        CommentSeeder::class,
    ]);
}
```

<a name="running-seeders"></a>
## 시더 실행하기

`db:seed` Artisan 명령어를 실행하여 데이터베이스를 시드할 수 있습니다. 기본적으로 `db:seed` 명령어는 `Database\Seeders\DatabaseSeeder` 클래스를 실행하며, 이 클래스가 추가 시드 클래스를 호출할 수도 있습니다. 하지만 `--class` 옵션을 사용하면 개별 시더 클래스를 지정하여 실행할 수 있습니다:

    php artisan db:seed

    php artisan db:seed --class=UserSeeder

또한, `migrate:fresh` 명령어와 `--seed` 옵션을 함께 사용하여 데이터베이스를 시드할 수도 있습니다. 이 명령어는 모든 테이블을 드롭하고 모든 마이그레이션을 다시 실행합니다. 데이터베이스를 완전히 재구축할 때 유용합니다:

    php artisan migrate:fresh --seed

<a name="forcing-seeding-production"></a>
#### 프로덕션 환경에서 시더 강제 실행하기

일부 시딩 작업은 데이터 변경이나 손실을 유발할 수 있습니다. 프로덕션 환경 데이터베이스에서 시딩 명령이 실행되는 것을 방지하기 위해, `production` 환경에서 시더가 실행되기 전에 확인을 요청합니다. 프롬프트 없이 강제로 시더를 실행하려면 `--force` 플래그를 사용하세요:

    php artisan db:seed --force
