# 데이터베이스: 시더(Seeding)

- [소개](#introduction)
- [시더 작성하기](#writing-seeders)
    - [모델 팩토리 활용](#using-model-factories)
    - [추가 시더 호출하기](#calling-additional-seeders)
    - [모델 이벤트 비활성화](#muting-model-events)
- [시더 실행하기](#running-seeders)

<a name="introduction"></a>
## 소개

Laravel은 시더 클래스를 사용하여 데이터베이스에 데이터를 시딩할 수 있는 기능을 제공합니다. 모든 시더 클래스는 `database/seeders` 디렉터리에 저장됩니다. 기본적으로 `DatabaseSeeder` 클래스가 미리 정의되어 있습니다. 이 클래스에서는 `call` 메서드를 사용해 다른 시더 클래스들을 실행할 수 있으며, 이를 통해 시딩 실행 순서를 제어할 수 있습니다.

> [!NOTE]  
> 데이터베이스 시딩 중에는 [대량 할당 보호](/docs/{{version}}/eloquent#mass-assignment)가 자동으로 비활성화됩니다.

<a name="writing-seeders"></a>
## 시더 작성하기

시더를 생성하려면 `make:seeder` [Artisan 명령어](/docs/{{version}}/artisan)를 실행하세요. 프레임워크에서 생성되는 모든 시더는 `database/seeders` 디렉터리에 위치합니다:

```shell
php artisan make:seeder UserSeeder
```

시더 클래스는 기본적으로 하나의 메서드만 포함합니다: `run`. 이 메서드는 `db:seed` [Artisan 명령어](/docs/{{version}}/artisan)가 실행될 때 호출됩니다. `run` 메서드 내에서 원하는 방식으로 데이터베이스에 데이터를 삽입할 수 있습니다. [쿼리 빌더](/docs/{{version}}/queries)를 이용하여 데이터를 수동으로 삽입할 수도 있고, [Eloquent 모델 팩토리](/docs/{{version}}/eloquent-factories)를 활용할 수도 있습니다.

예를 들어, 기본 `DatabaseSeeder` 클래스를 수정하여 `run` 메서드에 데이터베이스 삽입 구문을 추가해보겠습니다:

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

> [!NOTE]  
> `run` 메서드 시그니처에 필요한 의존성을 타입힌트로 명시하면, Laravel [서비스 컨테이너](/docs/{{version}}/container)를 통해 자동으로 주입해줍니다.

<a name="using-model-factories"></a>
### 모델 팩토리 활용

물론, 각 모델 시드의 속성을 일일이 지정하는 것은 번거롭습니다. 대신, [모델 팩토리](/docs/{{version}}/eloquent-factories)를 이용해 대량의 데이터베이스 레코드를 손쉽게 생성할 수 있습니다. 먼저, [모델 팩토리 문서](/docs/{{version}}/eloquent-factories)를 확인하여 팩토리 정의 방법을 알아보세요.

예를 들어, 각각 1개의 연관된 게시글이 있는 사용자 50명을 생성하려면 다음과 같이 작성할 수 있습니다:

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

<a name="calling-additional-seeders"></a>
### 추가 시더 호출하기

`DatabaseSeeder` 클래스 내에서 `call` 메서드를 통해 다른 시더 클래스를 실행할 수 있습니다. `call` 메서드를 사용하면 데이터베이스 시딩 코드를 여러 파일로 분산시켜 각 시더 클래스가 너무 커지지 않도록 할 수 있습니다. `call` 메서드는 실행할 시더 클래스들의 배열을 인자로 받습니다:

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

<a name="muting-model-events"></a>
### 모델 이벤트 비활성화

시드를 실행하는 동안 모델에서 이벤트가 발생하지 않도록 막고 싶을 수 있습니다. 이럴 때는 `WithoutModelEvents` 트레이트를 사용할 수 있습니다. 이 트레이트를 사용하면, `call` 메서드를 통해 추가 시더를 실행할 때도 모델 이벤트가 발생하지 않습니다:

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

<a name="running-seeders"></a>
## 시더 실행하기

`db:seed` Artisan 명령어를 실행하여 데이터베이스를 시딩할 수 있습니다. 기본적으로 `db:seed` 명령어는 `Database\Seeders\DatabaseSeeder` 클래스를 실행하며, 이 클래스에서 다른 시더들을 호출할 수 있습니다. 특정 시더 클래스를 개별적으로 실행하려면 `--class` 옵션을 사용하세요:

```shell
php artisan db:seed

php artisan db:seed --class=UserSeeder
```

또한, `migrate:fresh` 명령어와 `--seed` 옵션을 조합하여 데이터베이스를 시딩할 수도 있습니다. 이 명령어는 모든 테이블을 삭제하고 모든 마이그레이션을 다시 실행합니다. 데이터베이스를 완전히 초기화할 때 유용합니다. `--seeder` 옵션으로 실행할 특정 시더를 지정할 수도 있습니다:

```shell
php artisan migrate:fresh --seed

php artisan migrate:fresh --seed --seeder=UserSeeder
```

<a name="forcing-seeding-production"></a>
#### 운영 환경에서 시더 강제 실행하기

일부 시딩 작업은 데이터가 변경되거나 손실될 수 있습니다. 운영 데이터베이스에서 시딩 명령어를 실수로 실행하는 것을 방지하기 위해, `production` 환경에서는 시더 실행 전 확인 메시지가 표시됩니다. 프롬프트 없이 시더를 강제로 실행하려면 `--force` 플래그를 사용하세요:

```shell
php artisan db:seed --force
```