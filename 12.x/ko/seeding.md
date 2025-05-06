# 데이터베이스: 시딩

- [소개](#introduction)
- [시더 작성하기](#writing-seeders)
    - [모델 팩토리 사용하기](#using-model-factories)
    - [추가 시더 호출하기](#calling-additional-seeders)
    - [모델 이벤트 무시하기](#muting-model-events)
- [시더 실행하기](#running-seeders)

<a name="introduction"></a>
## 소개

Laravel은 시드 클래스를 사용하여 데이터베이스에 데이터를 쉽게 채울 수 있는 기능을 제공합니다. 모든 시드 클래스는 `database/seeders` 디렉터리에 저장됩니다. 기본적으로, `DatabaseSeeder` 클래스가 미리 정의되어 있습니다. 이 클래스에서 `call` 메서드를 사용하여 다른 시드 클래스를 실행할 수 있으므로, 시딩 순서를 자유롭게 제어할 수 있습니다.

> [!NOTE]
> 데이터베이스 시딩 중에는 [대량 할당 보호](/docs/{{version}}/eloquent#mass-assignment)가 자동으로 비활성화됩니다.

<a name="writing-seeders"></a>
## 시더 작성하기

시더를 생성하려면 `make:seeder` [Artisan 명령어](/docs/{{version}}/artisan)를 실행하세요. 프레임워크에서 생성된 모든 시더는 `database/seeders` 디렉터리에 생성됩니다:

```shell
php artisan make:seeder UserSeeder
```

시더 클래스에는 기본적으로 한 개의 메서드(`run`)만이 존재합니다. 이 메서드는 `db:seed` [Artisan 명령어](/docs/{{version}}/artisan)가 실행될 때 호출됩니다. `run` 메서드 내부에서 원하는 방식으로 데이터베이스에 데이터를 삽입할 수 있습니다. [쿼리 빌더](/docs/{{version}}/queries)를 사용하여 직접 데이터를 삽입하거나, [Eloquent 모델 팩토리](/docs/{{version}}/eloquent-factories)를 활용할 수도 있습니다.

예시로, 기본 `DatabaseSeeder` 클래스를 수정하여 `run` 메서드에 데이터베이스 삽입 구문을 추가해보겠습니다:

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
     * 데이터베이스 시더 실행
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
> 필요한 의존성을 `run` 메서드 시그니처에 타입힌트로 지정할 수 있습니다. 이들은 Laravel [서비스 컨테이너](/docs/{{version}}/container)를 통해 자동으로 주입됩니다.

<a name="using-model-factories"></a>
### 모델 팩토리 사용하기

물론, 각 모델 시드의 속성을 일일이 지정하는 것은 번거롭습니다. 대신, [모델 팩토리](/docs/{{version}}/eloquent-factories)를 사용하면 대량의 데이터베이스 레코드를 편리하게 생성할 수 있습니다. 먼저, 팩토리를 정의하는 방법은 [모델 팩토리 문서](/docs/{{version}}/eloquent-factories)를 참고하세요.

예를 들어, 각각 하나의 연관된 포스트를 가진 사용자 50명을 생성해보겠습니다:

```php
use App\Models\User;

/**
 * 데이터베이스 시더 실행
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

`DatabaseSeeder` 클래스 내에서 `call` 메서드를 이용해 추가적인 시드 클래스를 실행할 수 있습니다. `call` 메서드를 사용하면 여러 파일로 시드 작업을 분리할 수 있어, 단일 시더 클래스가 비대해지는 것을 방지할 수 있습니다. `call` 메서드는 실행할 시더 클래스의 배열을 인수로 받습니다:

```php
/**
 * 데이터베이스 시더 실행
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
### 모델 이벤트 무시하기

시드 작업 도중에 모델 이벤트가 발생하지 않도록 하고 싶다면, `WithoutModelEvents` 트레이트를 사용할 수 있습니다. 이 트레이트를 사용하면 `call` 메서드를 통한 추가 시더 클래스 실행 시에도 모델 이벤트가 전혀 발생하지 않습니다:

```php
<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Database\Console\Seeds\WithoutModelEvents;

class DatabaseSeeder extends Seeder
{
    use WithoutModelEvents;

    /**
     * 데이터베이스 시더 실행
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

데이터베이스를 시드하려면 `db:seed` Artisan 명령어를 실행하면 됩니다. 기본적으로 `db:seed` 명령어는 `Database\Seeders\DatabaseSeeder` 클래스를 실행하며, 이 클래스에서 추가적인 시드 클래스를 호출할 수 있습니다. 하지만, `--class` 옵션을 사용해서 특정 시더 클래스를 별도로 실행할 수도 있습니다:

```shell
php artisan db:seed

php artisan db:seed --class=UserSeeder
```

`migrate:fresh` 명령어와 `--seed` 옵션을 함께 사용하여 데이터베이스를 초기화하고 모든 마이그레이션 및 시딩을 한 번에 처리할 수도 있습니다. 이 명령어는 모든 테이블을 삭제한 후 마이그레이션과 시드를 재실행하므로 데이터베이스를 완전히 재구성할 때 유용합니다. `--seeder` 옵션으로 특정 시더만 실행할 수도 있습니다:

```shell
php artisan migrate:fresh --seed

php artisan migrate:fresh --seed --seeder=UserSeeder
```

<a name="forcing-seeding-production"></a>
#### 운영 환경에서 강제 시더 실행

일부 시딩 작업은 데이터 변경 또는 손실 위험이 있기 때문에, 운영 환경(`production`)에서 시더를 실행할 때는 별도의 확인 메시지가 표시됩니다. 프롬프트 없이 시더를 강제로 실행하려면 `--force` 플래그를 사용하세요:

```shell
php artisan db:seed --force
```