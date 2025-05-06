# 데이터베이스: 시딩

- [소개](#introduction)
- [시더 작성](#writing-seeders)
    - [모델 팩토리 사용하기](#using-model-factories)
    - [추가 시더 호출](#calling-additional-seeders)
    - [모델 이벤트 비활성화](#muting-model-events)
- [시더 실행](#running-seeders)

<a name="introduction"></a>
## 소개

Laravel은 시드 클래스를 사용하여 데이터베이스에 데이터를 손쉽게 삽입할 수 있는 기능을 제공합니다. 모든 시드 클래스는 `database/seeders` 디렉터리에 저장됩니다. 기본적으로 `DatabaseSeeder` 클래스가 미리 정의되어 있습니다. 이 클래스에서 `call` 메서드를 사용해 다른 시드 클래스를 실행할 수 있으며, 이를 통해 시딩 순서를 제어할 수 있습니다.

> **참고**  
> [대량 할당 보호](/docs/{{version}}/eloquent#mass-assignment)는 데이터베이스 시딩 중에 자동으로 비활성화됩니다.

<a name="writing-seeders"></a>
## 시더 작성

시더를 생성하려면, `make:seeder` [Artisan 명령어](/docs/{{version}}/artisan)를 실행하세요. 프레임워크가 생성한 모든 시더는 `database/seeders` 디렉터리에 위치하게 됩니다:

```shell
php artisan make:seeder UserSeeder
```

시더 클래스에는 기본적으로 하나의 메서드, 즉 `run`이 포함되어 있습니다. 이 메서드는 `db:seed` [Artisan 명령어](/docs/{{version}}/artisan)가 실행될 때 호출됩니다. `run` 메서드 내에서는 원하는 방법으로 데이터를 데이터베이스에 삽입할 수 있습니다. [쿼리 빌더](/docs/{{version}}/queries)를 사용해 수동으로 데이터를 삽입하거나, [Eloquent 모델 팩토리](/docs/{{version}}/eloquent-factories)를 사용할 수 있습니다.

예를 들어, 기본 `DatabaseSeeder` 클래스를 수정해 `run` 메서드에 데이터베이스 삽입 구문을 추가할 수 있습니다:

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

> **참고**  
> `run` 메서드의 시그니처에 필요한 의존성을 타입힌트로 지정할 수 있습니다. 해당 의존성은 Laravel [서비스 컨테이너](/docs/{{version}}/container)를 통해 자동으로 주입됩니다.

<a name="using-model-factories"></a>
### 모델 팩토리 사용하기

물론, 각 모델에 대한 속성을 일일이 지정하는 것은 번거롭습니다. 대신 [모델 팩토리](/docs/{{version}}/eloquent-factories)를 사용하여 많은 양의 데이터베이스 레코드를 편리하게 생성할 수 있습니다. 먼저 [모델 팩토리 문서](/docs/{{version}}/eloquent-factories)를 참고해 팩토리를 정의하는 방법을 살펴보세요.

예를 들어, 각각 1개의 관련 게시글을 가진 유저 50명을 생성해보겠습니다.

    use App\Models\User;

    /**
     * 데이터베이스 시더 실행.
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

<a name="calling-additional-seeders"></a>
### 추가 시더 호출

`DatabaseSeeder` 클래스 내에서는 `call` 메서드를 사용하여 다른 시드 클래스를 실행할 수 있습니다. `call` 메서드를 사용하면 시딩 로직을 여러 파일로 분리할 수 있어, 하나의 시더 클래스가 너무 커지는 것을 방지할 수 있습니다. `call` 메서드는 실행할 시더 클래스의 배열을 인자로 받습니다:

    /**
     * 데이터베이스 시더 실행.
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

<a name="muting-model-events"></a>
### 모델 이벤트 비활성화

시드를 실행하는 동안 모델에서 이벤트가 발생하는 것을 방지하고 싶을 수 있습니다. 이를 위해 `WithoutModelEvents` 트레이트를 사용할 수 있습니다. 해당 트레이트를 사용하면, 추가적인 시드 클래스가 `call` 메서드를 통해 실행되더라도 어떤 모델 이벤트도 발생하지 않습니다:

    <?php

    namespace Database\Seeders;

    use Illuminate\Database\Seeder;
    use Illuminate\Database\Console\Seeds\WithoutModelEvents;

    class DatabaseSeeder extends Seeder
    {
        use WithoutModelEvents;

        /**
         * 데이터베이스 시더 실행.
         *
         * @return void
         */
        public function run()
        {
            $this->call([
                UserSeeder::class,
            ]);
        }
    }

<a name="running-seeders"></a>
## 시더 실행

`db:seed` Artisan 명령어를 실행해 데이터베이스에 시더를 적용할 수 있습니다. 기본적으로 `db:seed` 명령어는 `Database\Seeders\DatabaseSeeder` 클래스를 실행하며, 이 클래스는 또 다른 시드 클래스를 호출할 수 있습니다. 하지만 `--class` 옵션을 사용해 특정 시드 클래스만 개별적으로 실행할 수도 있습니다.

```shell
php artisan db:seed

php artisan db:seed --class=UserSeeder
```

또한 `migrate:fresh` 명령어와 `--seed` 옵션을 조합하여 데이터베이스를 시딩할 수도 있습니다. 이 명령은 모든 테이블을 삭제하고, 모든 마이그레이션을 다시 실행한 뒤, 시딩을 수행합니다. 데이터베이스를 완전히 재구축할 때 유용합니다. `--seeder` 옵션을 사용하면 특정 시더만 실행할 수 있습니다:

```shell
php artisan migrate:fresh --seed

php artisan migrate:fresh --seed --seeder=UserSeeder 
```

<a name="forcing-seeding-production"></a>
#### 운영 환경에서 강제로 시더 실행하기

일부 시딩 작업은 데이터를 변경하거나 손실시킬 수 있습니다. 이를 방지하기 위해, 운영(`production`) 환경에서 시딩 명령을 실행하려 할 때는 확인 메시지가 나옵니다. 프롬프트 없이 강제로 시더를 실행하려면 `--force` 플래그를 사용하세요:

```shell
php artisan db:seed --force
```
