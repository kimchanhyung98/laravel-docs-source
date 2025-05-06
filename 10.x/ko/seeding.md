# 데이터베이스: 시더(Seeding)

- [소개](#introduction)
- [시더 작성하기](#writing-seeders)
    - [모델 팩토리 사용하기](#using-model-factories)
    - [추가 시더 호출하기](#calling-additional-seeders)
    - [모델 이벤트 중지하기](#muting-model-events)
- [시더 실행하기](#running-seeders)

<a name="introduction"></a>
## 소개

Laravel은 시드 클래스(Seed Class)를 사용하여 데이터베이스에 데이터를 채우는 기능을 제공합니다. 모든 시드 클래스는 `database/seeders` 디렉터리에 저장됩니다. 기본적으로 `DatabaseSeeder` 클래스가 정의되어 있습니다. 이 클래스에서 `call` 메서드를 사용하여 다른 시드 클래스를 실행할 수 있으며, 이를 통해 시딩 순서를 제어할 수 있습니다.

> [!NOTE]  
> [대량 할당 보호](docs/{{version}}/eloquent#mass-assignment)는 데이터베이스 시딩 중 자동으로 비활성화됩니다.

<a name="writing-seeders"></a>
## 시더 작성하기

시더를 생성하려면 `make:seeder` [Artisan 명령어](/docs/{{version}}/artisan)를 실행하세요. 프레임워크에서 생성된 모든 시더는 `database/seeders` 디렉터리에 위치하게 됩니다.

```shell
php artisan make:seeder UserSeeder
```

시더 클래스에는 기본적으로 단 하나의 메서드 `run`만이 포함되어 있습니다. 이 메서드는 `db:seed` [Artisan 명령어](/docs/{{version}}/artisan)가 실행될 때 호출됩니다. `run` 메서드 안에서 원하는 방식으로 데이터베이스에 데이터를 삽입할 수 있습니다. [쿼리 빌더](/docs/{{version}}/queries)를 사용해手 수동으로 데이터를 삽입하거나, [Eloquent 모델 팩토리](/docs/{{version}}/eloquent-factories)를 사용할 수 있습니다.

예시로, 기본 `DatabaseSeeder` 클래스를 수정하여 `run` 메서드에 데이터베이스 삽입 구문을 추가해보겠습니다:

    <?php

    namespace Database\Seeders;

    use Illuminate\Database\Seeder;
    use Illuminate\Support\Facades\DB;
    use Illuminate\Support\Facades\Hash;
    use Illuminate\Support\Str;

    class DatabaseSeeder extends Seeder
    {
        /**
         * 데이터베이스 시더 실행.
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
> `run` 메서드의 시그니처에서 필요한 모든 의존성을 타입힌트로 지정할 수 있습니다. 이 의존성들은 Laravel [서비스 컨테이너](/docs/{{version}}/container)를 통해 자동으로 주입됩니다.

<a name="using-model-factories"></a>
### 모델 팩토리 사용하기

물론, 각 모델의 속성을 수동으로 지정하는 것은 번거로운 일입니다. 이 대신, [모델 팩토리](/docs/{{version}}/eloquent-factories)를 사용하면 대량의 데이터베이스 레코드를 쉽게 생성할 수 있습니다. 먼저 [모델 팩토리 문서](/docs/{{version}}/eloquent-factories)를 참고하여 팩토리를 정의하는 방법을 익히세요.

예를 들어, 50명의 유저를 생성하고 각 유저에 1개의 관련 포스트를 연결하고 싶다면 다음과 같이 할 수 있습니다:

    use App\Models\User;

    /**
     * 데이터베이스 시더 실행.
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

`DatabaseSeeder` 클래스 내에서 `call` 메서드를 사용하여 추가 시드 클래스를 실행할 수 있습니다. `call` 메서드를 이용하면 여러 파일에 시딩 논리를 분할할 수 있어, 단일 시더 클래스가 너무 커지는 것을 방지할 수 있습니다. `call` 메서드는 실행할 시더 클래스의 배열을 인자로 받습니다.

    /**
     * 데이터베이스 시더 실행.
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
### 모델 이벤트 중지하기

시딩을 실행하는 동안 모델에서 이벤트가 발생하는 것을 방지하고 싶을 수 있습니다. 이를 위해 `WithoutModelEvents` 트레이트를 사용할 수 있습니다. 이 트레이트를 사용하면, 추가 시더 클래스를 `call` 메서드로 실행하더라도 어떤 모델 이벤트도 발생하지 않게 됩니다.

    <?php

    namespace Database\Seeders;

    use Illuminate\Database\Seeder;
    use Illuminate\Database\Console\Seeds\WithoutModelEvents;

    class DatabaseSeeder extends Seeder
    {
        use WithoutModelEvents;

        /**
         * 데이터베이스 시더 실행.
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

`db:seed` Artisan 명령어를 실행하여 데이터베이스를 시드할 수 있습니다. 기본적으로 `db:seed` 명령은 `Database\Seeders\DatabaseSeeder` 클래스를 실행하는데, 이 시더 내에서 추가 시드를 호출할 수 있습니다. 개별적으로 특정 시더 클래스를 실행하고 싶다면 `--class` 옵션을 사용할 수 있습니다:

```shell
php artisan db:seed

php artisan db:seed --class=UserSeeder
```

또한, `migrate:fresh` 명령어와 `--seed` 옵션을 조합하여 데이터베이스를 시드할 수 있습니다. 이 명령어는 모든 테이블을 삭제한 후 마이그레이션을 다시 실행하고, 시딩까지 한번에 처리합니다. 이 때 `--seeder` 옵션으로 특정 시더를 지정할 수 있습니다:

```shell
php artisan migrate:fresh --seed

php artisan migrate:fresh --seed --seeder=UserSeeder 
```

<a name="forcing-seeding-production"></a>
#### 운영 환경에서 강제로 시딩 실행하기

일부 시딩 작업은 데이터 변경 또는 손실을 초래할 수 있습니다. 운영(프로덕션) 데이터베이스에서 시더 명령을 잘못 실행하는 것을 방지하기 위해, `production` 환경에서는 시더 실행 전에 확인 프롬프트가 표시됩니다. 프롬프트 없이 강제로 시더를 실행하려면 `--force` 플래그를 사용하세요:

```shell
php artisan db:seed --force
```