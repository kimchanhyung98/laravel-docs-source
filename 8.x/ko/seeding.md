# 데이터베이스: 시딩 (Database: Seeding)

- [소개](#introduction)
- [시더 작성하기](#writing-seeders)
    - [모델 팩토리 사용하기](#using-model-factories)
    - [추가 시더 호출하기](#calling-additional-seeders)
- [시더 실행하기](#running-seeders)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 시더 클래스를 사용해 데이터베이스에 데이터를 채우는 기능을 제공합니다. 모든 시더 클래스는 `database/seeders` 디렉터리에 저장됩니다. 기본적으로 `DatabaseSeeder` 클래스가 정의되어 있으며, 이 클래스에서 `call` 메서드를 사용해 다른 시더 클래스를 실행하여 시딩 순서를 제어할 수 있습니다.

> [!TIP]
> 데이터베이스 시딩 중에는 [대량 할당 보호](/docs/{{version}}/eloquent#mass-assignment)가 자동으로 비활성화됩니다.

<a name="writing-seeders"></a>
## 시더 작성하기 (Writing Seeders)

시더를 생성하려면 `make:seeder` [Artisan 명령어](/docs/{{version}}/artisan)를 실행하세요. 프레임워크가 생성하는 모든 시더는 `database/seeders` 디렉터리에 저장됩니다:

```
php artisan make:seeder UserSeeder
```

시더 클래스는 기본적으로 `run` 메서드 하나만 포함합니다. 이 메서드는 `db:seed` [Artisan 명령어](/docs/{{version}}/artisan)를 실행할 때 호출됩니다. `run` 메서드 내에서 원하는 방식으로 데이터베이스에 데이터를 삽입할 수 있습니다. 수동으로 데이터를 삽입하려면 [쿼리 빌더](/docs/{{version}}/queries)를 사용해도 되고, [Eloquent 모델 팩토리](/docs/{{version}}/database-testing#defining-model-factories)를 사용해도 됩니다.

예를 들어, 기본 `DatabaseSeeder` 클래스를 수정해 `run` 메서드에 데이터 삽입문을 추가해 보겠습니다:

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

> [!TIP]
> `run` 메서드 시그니처에 필요로 하는 의존성을 타입힌트로 주입할 수 있습니다. Laravel의 [서비스 컨테이너](/docs/{{version}}/container)를 통해 자동으로 해결됩니다.

<a name="using-model-factories"></a>
### 모델 팩토리 사용하기

모델 시딩 시마다 속성을 일일이 지정하는 것은 번거롭습니다. 대신 [모델 팩토리](/docs/{{version}}/database-testing#defining-model-factories)를 사용하면 대량의 데이터 레코드를 간편하게 생성할 수 있습니다. 먼저 [모델 팩토리 문서](/docs/{{version}}/database-testing#defining-model-factories)를 참고해 팩토리를 정의하는 방법을 학습하세요.

예를 들어, 50명의 사용자를 각 사용자당 하나의 게시물을 포함해 생성하려면 다음과 같이 작성합니다:

```
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

`DatabaseSeeder` 클래스 내에서 `call` 메서드를 사용해 다른 시더 클래스를 실행할 수 있습니다. 이렇게 하면 데이터베이스 시딩 로직을 여러 파일로 분할할 수 있어, 하나의 시더 클래스가 너무 커지는 것을 방지할 수 있습니다. `call` 메서드는 실행할 시더 클래스 배열을 인수로 받습니다:

```
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
## 시더 실행하기 (Running Seeders)

`db:seed` Artisan 명령어를 사용해 데이터베이스에 시딩을 실행할 수 있습니다. 기본적으로 `db:seed` 명령어는 `Database\Seeders\DatabaseSeeder` 클래스를 실행하며, 이 클래스는 다른 시더 클래스들을 호출할 수 있습니다. 개별 시더 클래스를 실행하려면 `--class` 옵션에 해당 클래스명을 지정하세요:

```
php artisan db:seed

php artisan db:seed --class=UserSeeder
```

또한 `migrate:fresh` 명령어에 `--seed` 옵션을 함께 사용하면 모든 테이블을 삭제한 뒤 모든 마이그레이션을 다시 실행하며 시딩도 수행합니다. 이는 데이터베이스를 완전히 새로 구축할 때 유용합니다:

```
php artisan migrate:fresh --seed
```

<a name="forcing-seeding-production"></a>
#### 운영 환경에서 시더 강제 실행하기

일부 시딩 작업은 데이터 손실을 초래할 수 있습니다. 운영(production) 환경에서 시더 명령어 실행 시, 기본적으로 실행 전에 확인을 요구합니다. 이 확인 과정을 생략하고 강제로 시더를 실행하려면 `--force` 플래그를 사용하세요:

```
php artisan db:seed --force
```