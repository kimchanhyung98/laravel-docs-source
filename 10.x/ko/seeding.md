# 데이터베이스: 시딩 (Database: Seeding)

- [소개](#introduction)
- [시더 작성하기](#writing-seeders)
    - [모델 팩토리 사용하기](#using-model-factories)
    - [추가 시더 호출하기](#calling-additional-seeders)
    - [모델 이벤트 비활성화하기](#muting-model-events)
- [시더 실행하기](#running-seeders)

<a name="introduction"></a>
## 소개

Laravel은 시더 클래스를 사용하여 데이터베이스에 데이터를 삽입하는 시딩 기능을 제공합니다. 모든 시더 클래스는 기본적으로 `database/seeders` 디렉터리에 저장됩니다. 기본으로 `DatabaseSeeder` 클래스가 정의되어 있으며, 이 클래스에서 `call` 메서드를 사용하여 다른 시더 클래스를 실행할 수 있어 시딩 순서를 제어할 수 있습니다.

> [!NOTE]  
> 데이터베이스 시딩 중에는 [대량 할당 보호](/docs/10.x/eloquent#mass-assignment)가 자동으로 비활성화됩니다.

<a name="writing-seeders"></a>
## 시더 작성하기

시더를 생성하려면 `make:seeder` [Artisan 명령어](/docs/10.x/artisan)를 실행하세요. 프레임워크가 생성하는 모든 시더는 `database/seeders` 디렉터리에 위치하게 됩니다:

```shell
php artisan make:seeder UserSeeder
```

시더 클래스는 기본적으로 `run` 메서드 하나만 포함합니다. 이 메서드는 `db:seed` [Artisan 명령어](/docs/10.x/artisan)가 실행될 때 호출됩니다. `run` 메서드 내에서는 원하는 방식으로 데이터베이스에 데이터를 삽입할 수 있습니다. [쿼리 빌더](/docs/10.x/queries)를 사용해 수동으로 데이터를 삽입하거나 [Eloquent 모델 팩토리](/docs/10.x/eloquent-factories)를 활용할 수 있습니다.

예를 들어, 기본 `DatabaseSeeder` 클래스를 수정해 `run` 메서드에 데이터베이스 삽입 구문을 추가해 보겠습니다:

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
     * 데이터베이스 시더를 실행합니다.
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
> `run` 메서드 시그니처에 필요한 의존성을 타입힌트하면 Laravel의 [서비스 컨테이너](/docs/10.x/container)를 통해 자동으로 주입됩니다.

<a name="using-model-factories"></a>
### 모델 팩토리 사용하기

모델마다 속성을 일일이 지정하는 것은 번거롭습니다. 대신, [모델 팩토리들](/docs/10.x/eloquent-factories)을 이용해 대량의 데이터 레코드를 편리하게 생성할 수 있습니다. 먼저, [모델 팩토리 문서](/docs/10.x/eloquent-factories)를 참고하여 팩토리 정의 방법을 이해하세요.

예를 들어, 각 사용자에게 하나의 게시물이 있는 사용자 50명을 생성하는 코드는 다음과 같습니다:

```php
use App\Models\User;

/**
 * 데이터베이스 시더를 실행합니다.
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

`DatabaseSeeder` 클래스 내에서 `call` 메서드를 사용하면 추가 시더 클래스를 실행할 수 있습니다. 이를 활용하면 데이터베이스 시딩을 여러 파일로 나누어 한 시더 클래스가 너무 커지는 것을 방지할 수 있습니다. `call` 메서드는 실행할 시더 클래스들의 배열을 인수로 받습니다:

```php
/**
 * 데이터베이스 시더를 실행합니다.
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

시딩 실행 중에 모델에서 이벤트가 발송되는 것을 막고 싶다면 `WithoutModelEvents` 트레이트를 사용할 수 있습니다. 이 트레이트를 사용하면 `call` 메서드를 통해 다른 시더가 실행되더라도 모델 이벤트가 발송되지 않습니다:

```php
<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Database\Console\Seeds\WithoutModelEvents;

class DatabaseSeeder extends Seeder
{
    use WithoutModelEvents;

    /**
     * 데이터베이스 시더를 실행합니다.
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

`db:seed` Artisan 명령어를 실행하여 데이터베이스를 시딩할 수 있습니다. 기본적으로 `db:seed` 명령어는 `Database\Seeders\DatabaseSeeder` 클래스를 실행하며, 이 클래스가 다시 다른 시더들을 호출할 수 있습니다. 하지만 `--class` 옵션을 사용하여 특정 시더 클래스를 단독으로 실행할 수도 있습니다:

```shell
php artisan db:seed

php artisan db:seed --class=UserSeeder
```

또한, `migrate:fresh` 명령어에 `--seed` 옵션을 조합하면 모든 테이블을 삭제하고 모든 마이그레이션을 다시 실행한 다음 시더를 실행합니다. 이 명령은 데이터베이스를 완전히 재구성할 때 유용합니다. `--seeder` 옵션을 사용하여 특정 시더를 지정할 수도 있습니다:

```shell
php artisan migrate:fresh --seed

php artisan migrate:fresh --seed --seeder=UserSeeder 
```

<a name="forcing-seeding-production"></a>
#### 프로덕션 환경에서 시더 강제 실행하기

시딩 작업은 데이터의 변경이나 손실을 초래할 수 있습니다. 이를 방지하기 위해 프로덕션 환경에서는 시더 실행 전 확인을 요구합니다. 이 확인 없이 시더를 강제 실행하려면 `--force` 플래그를 사용하세요:

```shell
php artisan db:seed --force
```