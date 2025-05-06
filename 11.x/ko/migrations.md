# 데이터베이스: 마이그레이션

- [소개](#introduction)
- [마이그레이션 생성하기](#generating-migrations)
    - [마이그레이션 압축하기](#squashing-migrations)
- [마이그레이션 구조](#migration-structure)
- [마이그레이션 실행하기](#running-migrations)
    - [마이그레이션 롤백](#rolling-back-migrations)
- [테이블](#tables)
    - [테이블 생성](#creating-tables)
    - [테이블 수정](#updating-tables)
    - [테이블 이름 변경 및 삭제](#renaming-and-dropping-tables)
- [컬럼](#columns)
    - [컬럼 생성](#creating-columns)
    - [사용 가능한 컬럼 타입](#available-column-types)
    - [컬럼 수정자](#column-modifiers)
    - [컬럼 수정](#modifying-columns)
    - [컬럼 이름 변경](#renaming-columns)
    - [컬럼 삭제](#dropping-columns)
- [인덱스](#indexes)
    - [인덱스 생성](#creating-indexes)
    - [인덱스 이름 변경](#renaming-indexes)
    - [인덱스 삭제](#dropping-indexes)
    - [외래키 제약조건](#foreign-key-constraints)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

마이그레이션은 데이터베이스의 버전 관리를 가능하게 해주는 기능으로, 팀원들이 애플리케이션의 데이터베이스 스키마 정의를 공유하고 통일할 수 있도록 해줍니다. 소스 컨트롤에서 변경 사항을 합친 후 동료에게 각자 데이터베이스에 직접 컬럼을 추가하라고 얘기해본 적이 있다면, 마이그레이션이 해결하는 문제를 이미 경험한 것입니다.

Laravel의 `Schema` [파사드](/docs/{{version}}/facades)는 Laravel이 지원하는 모든 데이터베이스 시스템에서, 데이터베이스에 구애받지 않는 방식으로 테이블을 생성하고 조작하는 기능을 제공합니다. 보통 마이그레이션은 이 파사드를 이용해 데이터베이스 테이블 및 컬럼을 생성/수정합니다.

<a name="generating-migrations"></a>
## 마이그레이션 생성하기

`make:migration` [Artisan 명령어](/docs/{{version}}/artisan)를 사용하여 데이터베이스 마이그레이션 파일을 생성할 수 있습니다. 새로 생성되는 마이그레이션은 `database/migrations` 디렉토리에 위치하게 됩니다. 각 마이그레이션 파일명에는 타임스탬프가 포함되어 있어 Laravel이 실행 순서를 결정할 수 있도록 합니다:

```shell
php artisan make:migration create_flights_table
```

Laravel은 마이그레이션의 이름을 사용해 생성될 테이블의 이름과 해당 마이그레이션이 테이블을 생성하는지 여부를 추측하려 시도합니다. 만약 이름에서 테이블명을 유추할 수 있다면, 생성된 마이그레이션 파일에 자동으로 해당 테이블이 지정됩니다. 그렇지 않다면 마이그레이션 파일에서 직접 테이블 이름을 지정해 주어야 합니다.

마이그레이션을 특정 경로에 생성하고 싶다면 `make:migration` 실행 시 `--path` 옵션을 사용할 수 있습니다. 지정하는 경로는 애플리케이션의 베이스 경로를 기준으로 합니다.

> [!NOTE]  
> 마이그레이션 스텁(stub)은 [스텁 퍼블리싱](/docs/{{version}}/artisan#stub-customization)를 통해 커스터마이즈할 수 있습니다.

<a name="squashing-migrations"></a>
### 마이그레이션 압축하기

애플리케이션을 개발하다 보면 시간이 지나면서 마이그레이션이 점점 쌓이게 됩니다. 이로 인해 `database/migrations` 디렉토리가 수백 개의 파일로 불어나기도 합니다. 이럴 때, 모든 마이그레이션을 하나의 SQL 파일로 "압축(squash)"할 수 있습니다. 먼저 `schema:dump` 명령어를 실행하세요:

```shell
php artisan schema:dump

# 현재 데이터베이스 스키마를 덤프하며 기존 마이그레이션 전체를 정리...
php artisan schema:dump --prune
```

이 명령어를 실행하면, Laravel은 애플리케이션의 `database/schema` 디렉토리에 "스키마" 파일을 기록합니다. 이 파일의 이름은 사용 중인 데이터베이스 커넥션명과 일치합니다. 이후 데이터베이스에 아직 실행되지 않은 마이그레이션이 있을 때, Laravel은 우선 해당 커넥션의 스키마 파일에 있는 SQL문을 실행합니다. 그리고 나서 스키마 덤프에 포함되지 않은 나머지 마이그레이션을 순차적으로 실행합니다.

애플리케이션의 테스트가 로컬 개발시와 다른 데이터베이스 커넥션을 사용한다면, 해당 커넥션으로도 별도의 스키마 파일을 덤프해 주어야 합니다. 이를 위해 보통 사용하는 데이터베이스를 먼저 덤프한 뒤, 테스트용 커넥션으로도 덤프를 수행할 수 있습니다:

```shell
php artisan schema:dump
php artisan schema:dump --database=testing --prune
```

이 스키마 파일은 소스 컨트롤에 커밋하는 것이 좋습니다. 이렇게 하면 팀의 새로운 개발자들이 빠르게 초기 데이터베이스 구조를 생성할 수 있습니다.

> [!WARNING]  
> 마이그레이션 압축 기능은 MariaDB, MySQL, PostgreSQL, SQLite에서만 사용 가능하며, 해당 데이터베이스의 CLI 클라이언트를 활용합니다.

<a name="migration-structure"></a>
## 마이그레이션 구조

마이그레이션 클래스에는 두 개의 메서드가 있습니다: `up`과 `down`. `up` 메서드는 데이터베이스에 새로운 테이블, 컬럼, 또는 인덱스를 추가할 때 사용합니다. 반면, `down` 메서드는 `up`에서 수행한 작업을 되돌릴 때 사용합니다.

이 두 메서드 안에서는 Laravel 스키마 빌더를 사용해 직관적으로 테이블을 생성하고 수정할 수 있습니다. `Schema` 빌더에서 사용 가능한 모든 메서드는 [문서](#creating-tables)를 참고하세요. 예를 들어, 다음 마이그레이션은 `flights` 테이블을 생성합니다:

    <?php

    use Illuminate\Database\Migrations\Migration;
    use Illuminate\Database\Schema\Blueprint;
    use Illuminate\Support\Facades\Schema;

    return new class extends Migration
    {
        /**
         * 마이그레이션 실행
         */
        public function up(): void
        {
            Schema::create('flights', function (Blueprint $table) {
                $table->id();
                $table->string('name');
                $table->string('airline');
                $table->timestamps();
            });
        }

        /**
         * 마이그레이션 되돌리기
         */
        public function down(): void
        {
            Schema::drop('flights');
        }
    };

<a name="setting-the-migration-connection"></a>
#### 마이그레이션에서 데이터베이스 커넥션 설정하기

기본 데이터베이스 커넥션이 아닌 곳에 마이그레이션을 적용하려면, 마이그레이션 클래스의 `$connection` 프로퍼티를 설정해야 합니다:

    /**
     * 마이그레이션에 사용할 데이터베이스 커넥션
     *
     * @var string
     */
    protected $connection = 'pgsql';

    /**
     * 마이그레이션 실행
     */
    public function up(): void
    {
        // ...
    }

<a name="running-migrations"></a>
## 마이그레이션 실행하기

아직 적용되지 않은 모든 마이그레이션을 실행하려면 `migrate` Artisan 명령을 사용하세요:

```shell
php artisan migrate
```

지금까지 어떤 마이그레이션이 실행되었는지 확인하려면 `migrate:status` 명령을 사용합니다:

```shell
php artisan migrate:status
```

마이그레이션을 실제 실행하지 않고, 어떤 SQL문이 수행될지 미리 보고 싶다면 `--pretend` 플래그를 사용하세요:

```shell
php artisan migrate --pretend
```

#### 마이그레이션 실행의 격리

애플리케이션을 여러 서버에서 배포하며 마이그레이션을 동시에 실행한다면, 두 서버에서 동시에 데이터베이스가 마이그레이션되는 상황을 피하고 싶을 수 있습니다. 이를 막기 위해 `migrate` 명령 사용시 `--isolated` 옵션을 사용할 수 있습니다.

`--isolated` 옵션을 사용하면, 마이그레이션 실행 전 애플리케이션의 캐시 드라이버로 원자적 락을 획득합니다. 락이 걸려 있는 동안 다른 시도는 실행되지 않지만, 명령은 정상 종료 상태 코드로 종료됩니다:

```shell
php artisan migrate --isolated
```

> [!WARNING]  
> 이 기능을 사용하려면 기본 캐시 드라이버로 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 중 하나를 사용해야 하며, 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

<a name="forcing-migrations-to-run-in-production"></a>
#### 프로덕션 환경에서 강제로 마이그레이션 실행

일부 마이그레이션은 데이터 손실을 일으킬 수 있습니다. 이 때문에, 프로덕션 데이터베이스에 이러한 명령을 실행할 때는 확인 메시지가 먼저 표시됩니다. 확인 없이 바로 실행하려면 `--force` 플래그를 사용하세요:

```shell
php artisan migrate --force
```

<a name="rolling-back-migrations"></a>
### 마이그레이션 롤백

가장 최근의 마이그레이션을 롤백하려면 `rollback` Artisan 명령을 사용합니다. 이 명령은 마지막 "배치"에 속한 여러 개의 마이그레이션 파일을 모두 롤백합니다:

```shell
php artisan migrate:rollback
```

`--step` 옵션을 주면 특정 개수의 마이그레이션만 롤백할 수 있습니다. 예를 들어 아래 명령은 최근 5개의 마이그레이션만 롤백합니다:

```shell
php artisan migrate:rollback --step=5
```

`--batch` 옵션을 사용하면 특정 배치 전체를 롤백할 수 있습니다. 이는 `migrations` 테이블의 batch 값과 일치해야 합니다. 예시:

 ```shell
php artisan migrate:rollback --batch=3
 ```

마이그레이션을 실제론 실행하지 않고, 어떤 SQL이 실행될지 미리 알고 싶으면 `--pretend` 플래그를 사용하세요:

```shell
php artisan migrate:rollback --pretend
```

`migrate:reset` 명령을 사용하면 애플리케이션의 모든 마이그레이션이 롤백됩니다:

```shell
php artisan migrate:reset
```

<a name="roll-back-migrate-using-a-single-command"></a>
#### 한 번에 롤백과 마이그레이션 하기

`migrate:refresh` 명령은 모든 마이그레이션을 롤백한 다음, 다시 실행합니다. 즉, 데이터베이스 전체를 다시 만듭니다:

```shell
php artisan migrate:refresh

# 데이터베이스를 새로고침하고 seed 실행...
php artisan migrate:refresh --seed
```

`--step` 옵션을 사용하면 최근 N개의 마이그레이션만 롤백하고 다시 마이그레이션할 수 있습니다:

```shell
php artisan migrate:refresh --step=5
```

<a name="drop-all-tables-migrate"></a>
#### 모든 테이블 삭제 후 마이그레이션

`migrate:fresh` 명령은 데이터베이스의 모든 테이블을 삭제한 뒤, 마이그레이션을 실행합니다:

```shell
php artisan migrate:fresh

php artisan migrate:fresh --seed
```

기본적으로 `migrate:fresh`는 기본 데이터베이스 커넥션의 테이블만 삭제합니다. 다른 커넥션을 명시하고 싶다면 `--database` 옵션을 사용할 수 있습니다. 커넥션 이름은 `database` [설정파일](/docs/{{version}}/configuration)에 정의된 이름과 같아야 합니다.

```shell
php artisan migrate:fresh --database=admin
```

> [!WARNING]  
> `migrate:fresh` 명령은 테이블 프리픽스와 관계 없이 모든 테이블을 삭제합니다. 다른 애플리케이션과 테이블을 공유하는 데이터베이스에서는 주의해서 사용하세요.

<a name="tables"></a>
## 테이블

<a name="creating-tables"></a>
### 테이블 생성

새 데이터베이스 테이블을 생성하려면, `Schema` 파사드의 `create` 메서드를 사용하세요. `create` 메서드는 테이블 이름과, `Blueprint` 객체를 인자로 받는 클로저를 파라미터로 받습니다. 이 클로저 안에서 새로운 테이블을 정의할 수 있습니다:

    use Illuminate\Database\Schema\Blueprint;
    use Illuminate\Support\Facades\Schema;

    Schema::create('users', function (Blueprint $table) {
        $table->id();
        $table->string('name');
        $table->string('email');
        $table->timestamps();
    });

테이블을 생성할 때는, [컬럼 생성 메서드](#creating-columns)를 원하는 만큼 사용할 수 있습니다.

<a name="determining-table-column-existence"></a>
#### 테이블/컬럼 존재 여부 확인

테이블, 컬럼, 인덱스의 존재 여부는 `hasTable`, `hasColumn`, `hasIndex` 메서드로 확인할 수 있습니다.

    if (Schema::hasTable('users')) {
        // "users" 테이블이 존재합니다...
    }

    if (Schema::hasColumn('users', 'email')) {
        // "users" 테이블에 "email" 컬럼이 존재합니다...
    }

    if (Schema::hasIndex('users', ['email'], 'unique')) {
        // "users" 테이블에 "email" 컬럼에 대한 고유 인덱스가 있습니다...
    }

<a name="database-connection-table-options"></a>
#### 데이터베이스 커넥션과 테이블 옵션

기본 커넥션이 아닌 다른 데이터베이스 커넥션에서 스키마 작업을 하고자 한다면, `connection` 메서드를 사용하세요:

    Schema::connection('sqlite')->create('users', function (Blueprint $table) {
        $table->id();
    });

또한, 테이블 생성시 사용할 수 있는 다양한 속성/메서드들이 있습니다. 예를 들어 MariaDB 또는 MySQL에서는 저장 엔진을 다음과 같이 지정할 수 있습니다:

    Schema::create('users', function (Blueprint $table) {
        $table->engine('InnoDB');

        // ...
    });

문자셋과 콜레이션도 지정할 수 있습니다:

    Schema::create('users', function (Blueprint $table) {
        $table->charset('utf8mb4');
        $table->collation('utf8mb4_unicode_ci');

        // ...
    });

임시 테이블을 생성하려면 `temporary` 메서드를 사용하세요. 임시 테이블은 현재 연결 세션에서만 보이며, 연결이 종료되면 자동으로 삭제됩니다:

    Schema::create('calculations', function (Blueprint $table) {
        $table->temporary();

        // ...
    });

테이블에 주석(comment)을 추가할 수도 있습니다. 주석은 MariaDB, MySQL, PostgreSQL에서 지원합니다:

    Schema::create('calculations', function (Blueprint $table) {
        $table->comment('비즈니스 계산용');

        // ...
    });

<a name="updating-tables"></a>
### 테이블 수정

기존 테이블을 수정하려면 `Schema` 파사드의 `table` 메서드를 사용합니다. `create`와 마찬가지로 테이블 이름과 `Blueprint` 인스턴스를 받는 클로저로 인자를 구성합니다:

    use Illuminate\Database\Schema\Blueprint;
    use Illuminate\Support\Facades\Schema;

    Schema::table('users', function (Blueprint $table) {
        $table->integer('votes');
    });

<a name="renaming-and-dropping-tables"></a>
### 테이블 이름 변경 / 삭제

기존 테이블의 이름을 바꾸려면 `rename` 메서드를 사용하세요:

    use Illuminate\Support\Facades\Schema;

    Schema::rename($from, $to);

테이블을 삭제하려면 `drop` 또는 `dropIfExists` 메서드를 사용하세요:

    Schema::drop('users');

    Schema::dropIfExists('users');

<a name="renaming-tables-with-foreign-keys"></a>
#### 외래키가 있는 테이블 이름 변경

테이블 이름을 변경하기 전에는, 외래 키 제약조건이 Laravel에서 자동으로 작명하지 않고 명시적으로 이름을 지정하도록 마이그레이션 파일을 작성해야 합니다. 그렇지 않으면 외래키 제약조건의 이름이 이전 테이블 이름을 참조하게 됩니다.

<a name="columns"></a>
## 컬럼

<a name="creating-columns"></a>
### 컬럼 생성

기존 테이블에 컬럼을 추가하려면, `Schema` 파사드의 `table` 메서드를 사용합니다. `create`와 유사하게, 테이블 이름과 함께 `Blueprint` 인스턴스를 받는 클로저를 제공합니다:

    use Illuminate\Database\Schema\Blueprint;
    use Illuminate\Support\Facades\Schema;

    Schema::table('users', function (Blueprint $table) {
        $table->integer('votes');
    });

<a name="available-column-types"></a>
### 사용 가능한 컬럼 타입

스키마 빌더의 블루프린트에는 다양한 컬럼 타입에 대응하는 여러 메서드가 준비되어 있습니다. 아래 표를 참고하세요:

<!-- HTML 테이블, 코드, div, 스타일 등은 번역하지 않음 -->

<a name="column-method-bigIncrements"></a>
#### `bigIncrements()` {.collection-method .first-collection-method}

`bigIncrements` 메서드는 자동 증가하는 `UNSIGNED BIGINT`(기본키) 컬럼을 생성합니다:

    $table->bigIncrements('id');

<a name="column-method-bigInteger"></a>
#### `bigInteger()` {.collection-method}

`bigInteger` 메서드는 `BIGINT` 컬럼을 생성합니다:

    $table->bigInteger('votes');

<a name="column-method-binary"></a>
#### `binary()` {.collection-method}

`binary` 메서드는 `BLOB` 컬럼을 생성합니다:

    $table->binary('photo');

MySQL, MariaDB 또는 SQL Server에서 `length`와 `fixed` 인자를 전달하면 `VARBINARY` 또는 `BINARY` 컬럼을 생성할 수 있습니다:

    $table->binary('data', length: 16); // VARBINARY(16)

    $table->binary('data', length: 16, fixed: true); // BINARY(16)

<a name="column-method-boolean"></a>
#### `boolean()` {.collection-method}

`boolean` 메서드는 `BOOLEAN` 컬럼을 생성합니다:

    $table->boolean('confirmed');

<a name="column-method-char"></a>
#### `char()` {.collection-method}

`char` 메서드는 지정된 길이만큼의 `CHAR` 컬럼을 생성합니다:

    $table->char('name', length: 100);

<a name="column-method-dateTimeTz"></a>
#### `dateTimeTz()` {.collection-method}

`dateTimeTz` 메서드는 시간대를 지원하는 `DATETIME` 컬럼을 생성합니다. 소수점 초 정밀도를 옵션으로 지정할 수 있습니다:

    $table->dateTimeTz('created_at', precision: 0);

<a name="column-method-dateTime"></a>
#### `dateTime()` {.collection-method}

`dateTime` 메서드는 `DATETIME` 컬럼을 생성합니다. 소수점 초 정밀도를 옵션으로 지정할 수 있습니다:

    $table->dateTime('created_at', precision: 0);

<a name="column-method-date"></a>
#### `date()` {.collection-method}

`date` 메서드는 `DATE` 컬럼을 생성합니다:

    $table->date('created_at');

<a name="column-method-decimal"></a>
#### `decimal()` {.collection-method}

`decimal` 메서드는 지정된 정밀도와 소수점 자리수만큼의 `DECIMAL` 컬럼을 생성합니다:

    $table->decimal('amount', total: 8, places: 2);

<a name="column-method-double"></a>
#### `double()` {.collection-method}

`double` 메서드는 `DOUBLE` 컬럼을 생성합니다:

    $table->double('amount');

<a name="column-method-enum"></a>
#### `enum()` {.collection-method}

`enum` 메서드는 주어진 값 중 하나만 허용하는 `ENUM` 컬럼을 생성합니다:

    $table->enum('difficulty', ['easy', 'hard']);

<a name="column-method-float"></a>
#### `float()` {.collection-method}

`float` 메서드는 지정된 정밀도의 `FLOAT` 컬럼을 생성합니다:

    $table->float('amount', precision: 53);

<a name="column-method-foreignId"></a>
#### `foreignId()` {.collection-method}

`foreignId` 메서드는 `UNSIGNED BIGINT` 컬럼을 생성합니다:

    $table->foreignId('user_id');

<a name="column-method-foreignIdFor"></a>
#### `foreignIdFor()` {.collection-method}

`foreignIdFor` 메서드는 주어진 모델 클래스의 `{column}_id` 컬럼을 생성합니다. 컬럼 타입은 모델 키에 따라 `UNSIGNED BIGINT`, `CHAR(36)`, `CHAR(26)` 중 하나가 됩니다:

    $table->foreignIdFor(User::class);

<a name="column-method-foreignUlid"></a>
#### `foreignUlid()` {.collection-method}

`foreignUlid` 메서드는 `ULID` 컬럼을 생성합니다:

    $table->foreignUlid('user_id');

<a name="column-method-foreignUuid"></a>
#### `foreignUuid()` {.collection-method}

`foreignUuid` 메서드는 `UUID` 컬럼을 생성합니다:

    $table->foreignUuid('user_id');

<a name="column-method-geography"></a>
#### `geography()` {.collection-method}

`geography` 메서드는 주어진 공간 타입과 SRID(Spatial Reference System Identifier)로 `GEOGRAPHY` 컬럼을 생성합니다:

    $table->geography('coordinates', subtype: 'point', srid: 4326);

> [!NOTE]  
> 공간 타입 지원은 데이터베이스 드라이버에 따라 다릅니다. 자세한 내용은 사용 중인 데이터베이스의 문서를 참고하세요. PostgreSQL을 사용할 경우, `geography` 메서드를 사용 전에 [PostGIS](https://postgis.net) 확장을 설치해야 합니다.

<a name="column-method-geometry"></a>
#### `geometry()` {.collection-method}

`geometry` 메서드는 주어진 공간 타입과 SRID로 `GEOMETRY` 컬럼을 생성합니다:

    $table->geometry('positions', subtype: 'point', srid: 0);

> [!NOTE]  
> 공간 타입 지원은 데이터베이스 드라이버에 따라 다릅니다. 자세한 내용은 사용 중인 데이터베이스의 문서를 참고하세요. PostgreSQL을 사용할 경우, `geometry` 메서드를 사용 전에 [PostGIS](https://postgis.net) 확장을 설치해야 합니다.

<a name="column-method-id"></a>
#### `id()` {.collection-method}

`id` 메서드는 `bigIncrements`의 별칭입니다. 기본적으로 `id` 컬럼이 생성되지만, 컬럼명을 지정할 수도 있습니다:

    $table->id();

<a name="column-method-increments"></a>
#### `increments()` {.collection-method}

`increments` 메서드는 자동 증가하는 `UNSIGNED INTEGER` 컬럼을 값으로 하는 기본키를 생성합니다:

    $table->increments('id');

<a name="column-method-integer"></a>
#### `integer()` {.collection-method}

`integer` 메서드는 `INTEGER` 컬럼을 생성합니다:

    $table->integer('votes');

<a name="column-method-ipAddress"></a>
#### `ipAddress()` {.collection-method}

`ipAddress` 메서드는 `VARCHAR`(또는 PostgreSQL 사용 시 `INET`) 컬럼을 생성합니다:

    $table->ipAddress('visitor');

<a name="column-method-json"></a>
#### `json()` {.collection-method}

`json` 메서드는 `JSON` 컬럼을 생성합니다:

    $table->json('options');

SQLite 사용 시 `TEXT` 컬럼으로 생성됩니다.

<a name="column-method-jsonb"></a>
#### `jsonb()` {.collection-method}

`jsonb` 메서드는 `JSONB` 컬럼을 생성합니다:

    $table->jsonb('options');

SQLite 사용 시 `TEXT` 컬럼으로 생성됩니다.

<a name="column-method-longText"></a>
#### `longText()` {.collection-method}

`longText` 메서드는 `LONGTEXT` 컬럼을 생성합니다:

    $table->longText('description');

MySQL 또는 MariaDB에서 `binary` 문자셋을 지정하면 `LONGBLOB` 형태로 생성할 수 있습니다:

    $table->longText('data')->charset('binary'); // LONGBLOB

<a name="column-method-macAddress"></a>
#### `macAddress()` {.collection-method}

`macAddress` 메서드는 MAC 주소를 저장하기 위한 컬럼을 생성합니다. PostgreSQL 등의 일부 DB는 전용 타입을, 기타 DB에선 문자열 타입을 사용합니다:

    $table->macAddress('device');

<a name="column-method-mediumIncrements"></a>
#### `mediumIncrements()` {.collection-method}

`mediumIncrements` 메서드는 자동 증가하는 `UNSIGNED MEDIUMINT` 컬럼을 기본키로 생성합니다:

    $table->mediumIncrements('id');

<a name="column-method-mediumInteger"></a>
#### `mediumInteger()` {.collection-method}

`mediumInteger` 메서드는 `MEDIUMINT` 컬럼을 생성합니다:

    $table->mediumInteger('votes');

<a name="column-method-mediumText"></a>
#### `mediumText()` {.collection-method}

`mediumText` 메서드는 `MEDIUMTEXT` 컬럼을 생성합니다:

    $table->mediumText('description');

MySQL 또는 MariaDB에서 `binary` 문자셋을 지정하면 `MEDIUMBLOB`으로 변환할 수 있습니다:

    $table->mediumText('data')->charset('binary'); // MEDIUMBLOB

<a name="column-method-morphs"></a>
#### `morphs()` {.collection-method}

`morphs` 메서드는 `{column}_id`와 `{column}_type` 컬럼(VARCHAR 포함)을 한 번에 생성합니다. `{column}_id`의 컬럼타입은 모델 키 타입에 따라 결정됩니다.

이 메서드는 다형성 [Eloquent 관계](/docs/{{version}}/eloquent-relationships)에 필요한 컬럼을 생성할 때 사용됩니다. 예를 들어 `taggable_id`와 `taggable_type`이 생성됩니다:

    $table->morphs('taggable');

<a name="column-method-nullableMorphs"></a>
#### `nullableMorphs()` {.collection-method}

[morphs](#column-method-morphs)와 유사하지만, 생성되는 컬럼들이 `nullable`로 처리됩니다:

    $table->nullableMorphs('taggable');

<a name="column-method-nullableUlidMorphs"></a>
#### `nullableUlidMorphs()` {.collection-method}

[ulidMorphs](#column-method-ulidMorphs)와 유사하지만, `nullable` 처리됩니다:

    $table->nullableUlidMorphs('taggable');

<a name="column-method-nullableUuidMorphs"></a>
#### `nullableUuidMorphs()` {.collection-method}

[uuidMorphs](#column-method-uuidMorphs)와 유사하지만, `nullable` 처리됩니다:

    $table->nullableUuidMorphs('taggable');

<a name="column-method-rememberToken"></a>
#### `rememberToken()` {.collection-method}

`rememberToken` 메서드는 "remember me" [인증 토큰](/docs/{{version}}/authentication#remembering-users)을 저장하는 `VARCHAR(100)` nullable 컬럼을 생성합니다:

    $table->rememberToken();

<a name="column-method-set"></a>
#### `set()` {.collection-method}

`set` 메서드는 지정된 값 중 여러 개를 저장할 수 있는 `SET` 컬럼을 생성합니다:

    $table->set('flavors', ['strawberry', 'vanilla']);

<a name="column-method-smallIncrements"></a>
#### `smallIncrements()` {.collection-method}

`smallIncrements` 메서드는 자동 증가 `UNSIGNED SMALLINT` 컬럼을 기본키로 생성합니다:

    $table->smallIncrements('id');

<a name="column-method-smallInteger"></a>
#### `smallInteger()` {.collection-method}

`smallInteger` 메서드는 `SMALLINT` 컬럼을 생성합니다:

    $table->smallInteger('votes');

<a name="column-method-softDeletesTz"></a>
#### `softDeletesTz()` {.collection-method}

`softDeletesTz` 메서드는 null이 가능한 `deleted_at TIMESTAMP(시간대 포함)` 컬럼을 추가하며, 소수점 초 정밀도를 옵션으로 가질 수 있습니다. Eloquent의 "소프트 삭제" 기능에 사용합니다:

    $table->softDeletesTz('deleted_at', precision: 0);

<a name="column-method-softDeletes"></a>
#### `softDeletes()` {.collection-method}

`softDeletes` 메서드도 `deleted_at TIMESTAMP` 컬럼을 추가합니다(소수점 초 정밀도 옵션 포함). 역시 소프트 삭제를 위해 사용됩니다:

    $table->softDeletes('deleted_at', precision: 0);

<a name="column-method-string"></a>
#### `string()` {.collection-method}

`string` 메서드는 지정된 길이의 `VARCHAR` 컬럼을 생성합니다:

    $table->string('name', length: 100);

<a name="column-method-text"></a>
#### `text()` {.collection-method}

`text` 메서드는 `TEXT` 컬럼을 생성합니다:

    $table->text('description');

MySQL이나 MariaDB에서 `binary` 문자셋을 지정하면 `BLOB` 컬럼으로 생성됩니다:

    $table->text('data')->charset('binary'); // BLOB

<a name="column-method-timeTz"></a>
#### `timeTz()` {.collection-method}

`timeTz` 메서드는 시간대를 포함할 수 있는 `TIME` 컬럼을 생성합니다(정밀도 옵션 가능):

    $table->timeTz('sunrise', precision: 0);

<a name="column-method-time"></a>
#### `time()` {.collection-method}

`time` 메서드는 `TIME` 컬럼을 생성합니다(정밀도 옵션 가능):

    $table->time('sunrise', precision: 0);

<a name="column-method-timestampTz"></a>
#### `timestampTz()` {.collection-method}

`timestampTz` 메서드는 시간대를 포함하는 `TIMESTAMP` 컬럼을 생성합니다(정밀도 옵션 가능):

    $table->timestampTz('added_at', precision: 0);

<a name="column-method-timestamp"></a>
#### `timestamp()` {.collection-method}

`timestamp` 메서드는 `TIMESTAMP` 컬럼을 생성합니다(정밀도 옵션 가능):

    $table->timestamp('added_at', precision: 0);

<a name="column-method-timestampsTz"></a>
#### `timestampsTz()` {.collection-method}

`timestampsTz` 메서드는 `created_at`, `updated_at` 시간대를 포함하는 `TIMESTAMP` 컬럼을 생성합니다(정밀도 옵션 가능):

    $table->timestampsTz(precision: 0);

<a name="column-method-timestamps"></a>
#### `timestamps()` {.collection-method}

`timestamps` 메서드는 `created_at`, `updated_at` `TIMESTAMP` 컬럼을 생성합니다(정밀도 옵션 가능):

    $table->timestamps(precision: 0);

<a name="column-method-tinyIncrements"></a>
#### `tinyIncrements()` {.collection-method}

`tinyIncrements` 메서드는 자동 증가하는 `UNSIGNED TINYINT` 컬럼을 기본키로 생성합니다:

    $table->tinyIncrements('id');

<a name="column-method-tinyInteger"></a>
#### `tinyInteger()` {.collection-method}

`tinyInteger` 메서드는 `TINYINT` 컬럼을 생성합니다:

    $table->tinyInteger('votes');

<a name="column-method-tinyText"></a>
#### `tinyText()` {.collection-method}

`tinyText` 메서드는 `TINYTEXT` 컬럼을 생성합니다:

    $table->tinyText('notes');

MySQL 또는 MariaDB에서 `binary` 문자셋을 지정하면 `TINYBLOB` 컬럼을 생성할 수 있습니다:

    $table->tinyText('data')->charset('binary'); // TINYBLOB

<a name="column-method-unsignedBigInteger"></a>
#### `unsignedBigInteger()` {.collection-method}

`unsignedBigInteger` 메서드는 `UNSIGNED BIGINT` 컬럼을 생성합니다:

    $table->unsignedBigInteger('votes');

<a name="column-method-unsignedInteger"></a>
#### `unsignedInteger()` {.collection-method}

`unsignedInteger` 메서드는 `UNSIGNED INTEGER` 컬럼을 생성합니다:

    $table->unsignedInteger('votes');

<a name="column-method-unsignedMediumInteger"></a>
#### `unsignedMediumInteger()` {.collection-method}

`unsignedMediumInteger` 메서드는 `UNSIGNED MEDIUMINT` 컬럼을 생성합니다:

    $table->unsignedMediumInteger('votes');

<a name="column-method-unsignedSmallInteger"></a>
#### `unsignedSmallInteger()` {.collection-method}

`unsignedSmallInteger` 메서드는 `UNSIGNED SMALLINT` 컬럼을 생성합니다:

    $table->unsignedSmallInteger('votes');

<a name="column-method-unsignedTinyInteger"></a>
#### `unsignedTinyInteger()` {.collection-method}

`unsignedTinyInteger` 메서드는 `UNSIGNED TINYINT` 컬럼을 생성합니다:

    $table->unsignedTinyInteger('votes');

<a name="column-method-ulidMorphs"></a>
#### `ulidMorphs()` {.collection-method}

`ulidMorphs` 메서드는 `{column}_id`(`CHAR(26)`), `{column}_type`(`VARCHAR`) 컬럼을 한 번에 생성하며, ULID를 사용한 다형성 [Eloquent 관계](/docs/{{version}}/eloquent-relationships)에서 사용합니다:

    $table->ulidMorphs('taggable');

<a name="column-method-uuidMorphs"></a>
#### `uuidMorphs()` {.collection-method}

`uuidMorphs` 메서드는 `{column}_id`(`CHAR(36)`), `{column}_type`(`VARCHAR`) 컬럼을 한 번에 생성하며, UUID를 사용한 다형성 [Eloquent 관계](/docs/{{version}}/eloquent-relationships)에서 사용합니다:

    $table->uuidMorphs('taggable');

<a name="column-method-ulid"></a>
#### `ulid()` {.collection-method}

`ulid` 메서드는 `ULID` 컬럼을 생성합니다:

    $table->ulid('id');

<a name="column-method-uuid"></a>
#### `uuid()` {.collection-method}

`uuid` 메서드는 `UUID` 컬럼을 생성합니다:

    $table->uuid('id');

<a name="column-method-vector"></a>
#### `vector()` {.collection-method}

`vector` 메서드는 `vector` 컬럼을 생성합니다:

    $table->vector('embedding', dimensions: 100);

<a name="column-method-year"></a>
#### `year()` {.collection-method}

`year` 메서드는 `YEAR` 컬럼을 생성합니다:

    $table->year('birth_year');

<a name="column-modifiers"></a>
### 컬럼 수정자

위에서 소개한 컬럼 타입 외에도, 데이터베이스 테이블에 컬럼을 추가할 때 여러 가지 "수정자(modifier)"를 사용할 수 있습니다. 예를 들어 컬럼을 `nullable`로 만들고 싶다면, `nullable` 메서드를 사용하면 됩니다:

    use Illuminate\Database\Schema\Blueprint;
    use Illuminate\Support\Facades\Schema;

    Schema::table('users', function (Blueprint $table) {
        $table->string('email')->nullable();
    });

아래 표에는 사용 가능한 모든 컬럼 수정자를 나열하였습니다(인덱스 관련 수정자는 [여기](#creating-indexes)를 참고하세요):

<!-- 표 내용 번역 유지 -->

<a name="default-expressions"></a>
#### 기본값 표현식(Default Expressions)

`default` 수정자는 값 또는 `Illuminate\Database\Query\Expression` 인스턴스를 받을 수 있습니다. `Expression` 인스턴스를 사용하면 해당 값이 인용부호로 감싸지지 않으므로, 데이터베이스의 함수를 쓸 수 있습니다. 예를 들어 JSON 컬럼의 기본값을 지정할 때 유용하게 사용할 수 있습니다:

    <?php

    use Illuminate\Support\Facades\Schema;
    use Illuminate\Database\Schema\Blueprint;
    use Illuminate\Database\Query\Expression;
    use Illuminate\Database\Migrations\Migration;

    return new class extends Migration
    {
        /**
         * 마이그레이션 실행
         */
        public function up(): void
        {
            Schema::create('flights', function (Blueprint $table) {
                $table->id();
                $table->json('movies')->default(new Expression('(JSON_ARRAY())'));
                $table->timestamps();
            });
        }
    };

> [!WARNING]  
> 기본값 표현식의 지원 여부는 데이터베이스 드라이버, 버전, 필드 타입에 따라 다르므로, 반드시 DB 문서를 참고하세요.

<a name="column-order"></a>
#### 컬럼 순서 지정

MariaDB, MySQL을 사용하는 경우, `after` 메서드를 사용해 기존 컬럼 뒤에 새 컬럼을 추가할 수 있습니다:

    $table->after('password', function (Blueprint $table) {
        $table->string('address_line1');
        $table->string('address_line2');
        $table->string('city');
    });

<a name="modifying-columns"></a>
### 컬럼 수정

`change` 메서드를 통해 기존 컬럼의 타입이나 속성을 변경할 수 있습니다. 예시로, `name` 컬럼의 길이를 25에서 50으로 늘리고 싶다면 아래와 같이 작성합니다:

    Schema::table('users', function (Blueprint $table) {
        $table->string('name', 50)->change();
    });

컬럼을 수정할 때는, 유지할 모든 수정자를 반드시 명시적으로 지정해야 합니다 – 누락된 속성은 제거됩니다. `unsigned`, `default`, `comment` 속성을 유지하고 싶다면 각각 명시해야 합니다:

    Schema::table('users', function (Blueprint $table) {
        $table->integer('votes')->unsigned()->default(1)->comment('설명')->change();
    });

`change`는 인덱스를 변경하지 않습니다. 인덱스를 명시적으로 추가/제거하려면 인덱스 수정자를 활용하세요:

```php
// 인덱스 추가...
$table->bigIncrements('id')->primary()->change();

// 인덱스 제거...
$table->char('postal_code', 10)->unique(false)->change();
```

<a name="renaming-columns"></a>
### 컬럼 이름 변경

컬럼 이름을 바꾸려면, 스키마 빌더에서 제공하는 `renameColumn` 메서드를 사용하세요:

    Schema::table('users', function (Blueprint $table) {
        $table->renameColumn('from', 'to');
    });

<a name="dropping-columns"></a>
### 컬럼 삭제

컬럼을 제거하려면, 스키마 빌더의 `dropColumn` 메서드를 사용하세요:

    Schema::table('users', function (Blueprint $table) {
        $table->dropColumn('votes');
    });

여러 컬럼을 한 번에 삭제하려면 배열로 컬럼명을 전달하면 됩니다:

    Schema::table('users', function (Blueprint $table) {
        $table->dropColumn(['votes', 'avatar', 'location']);
    });

<a name="available-command-aliases"></a>
#### 삭제 명령어의 별칭

Laravel은 자주 사용되는 컬럼 삭제를 위한 편리한 메서드를 몇 가지 제공합니다. 각 명령은 아래 표와 같습니다:

<!-- 표는 원문 유지 -->

<a name="indexes"></a>
## 인덱스

<a name="creating-indexes"></a>
### 인덱스 생성

Laravel 스키마 빌더는 여러 종류의 인덱스를 지원합니다. 예를 들어 새 `email` 컬럼을 추가하고, 중복을 허용하지 않으려면 아래와 같이 체이닝 방식으로 작성할 수 있습니다:

    use Illuminate\Database\Schema\Blueprint;
    use Illuminate\Support\Facades\Schema;

    Schema::table('users', function (Blueprint $table) {
        $table->string('email')->unique();
    });

컬럼 정의 후 별도로 인덱스를 생성할 수도 있습니다. 이 경우 인덱스 메서드에 컬럼명을 지정합니다:

    $table->unique('email');

여러 컬럼을 대상으로 하는 복합 인덱스(Compound Index)도 생성할 수 있습니다:

    $table->index(['account_id', 'created_at']);

Laravel은 기본적으로 테이블명, 컬럼명, 인덱스 종류를 조합하여 인덱스명을 자동 생성하지만, 두 번째 인자로 직접 이름을 지정할 수도 있습니다:

    $table->unique('email', 'unique_email');

<a name="available-index-types"></a>
#### 사용 가능한 인덱스 타입

Laravel의 스키마 빌더 블루프린트 클래스는 각종 인덱스를 생성할 수 있도록 별도의 메서드를 제공합니다. 각 인덱스 메서드는 인덱스명을 직접 지정하는 인자를 받을 수 있습니다. 인덱스 명을 생략하면 테이블 및 컬럼, 인덱스 타입을 조합해 자동 생성합니다.

<!-- 표, 설명 등은 번역 유지 -->

<a name="renaming-indexes"></a>
### 인덱스 이름 변경

인덱스의 이름을 바꾸려면 스키마 빌더의 `renameIndex` 메서드를 사용하세요. 현재 이름과 원하는 이름을 순서대로 인자로 전달합니다:

    $table->renameIndex('from', 'to')

<a name="dropping-indexes"></a>
### 인덱스 삭제

인덱스를 삭제하려면, 인덱스 이름을 명시해야 합니다. 기본적으로 Laravel은 테이블명, 컬럼명, 인덱스 타입을 조합해 인덱스 이름을 자동 지정합니다. 몇 가지 예시는 아래 표와 같습니다.

<!-- 표는 원문 유지 -->

만약 삭제할 인덱스가 배열 형태의 컬럼명으로 지정된다면, Laravel은 해당 규칙에 따라 인덱스 이름을 자동 생성하여 삭제합니다:

    Schema::table('geo', function (Blueprint $table) {
        $table->dropIndex(['state']); // 인덱스 'geo_state_index' 삭제
    });

<a name="foreign-key-constraints"></a>
### 외래키 제약조건(Foreign Key Constraint)

Laravel에서는 참조 무결성을 보장하는 외래키 제약조건도 정의할 수 있습니다. 예를 들어 `posts` 테이블의 `user_id` 컬럼이 `users` 테이블의 `id` 컬럼을 참조하도록 하려면:

    use Illuminate\Database\Schema\Blueprint;
    use Illuminate\Support\Facades\Schema;

    Schema::table('posts', function (Blueprint $table) {
        $table->unsignedBigInteger('user_id');

        $table->foreign('user_id')->references('id')->on('users');
    });

이 문법이 다소 장황하므로, Laravel은 더 편의성 높은 메서드를 제공합니다. `foreignId`로 컬럼을 생성하고, `constrained`를 체이닝하면 위와 같이 동작합니다:

    Schema::table('posts', function (Blueprint $table) {
        $table->foreignId('user_id')->constrained();
    });

`foreignId`는 `UNSIGNED BIGINT` 컬럼을 생성하고, `constrained`는 관례에 따라 참조할 테이블/컬럼을 결정합니다. Laravel의 네이밍 규칙과 다르게 테이블명을 직접 지정하고 싶거나, 생성되는 인덱스의 이름을 지정하고 싶을 때는 다음과 같이 할 수 있습니다:

    Schema::table('posts', function (Blueprint $table) {
        $table->foreignId('user_id')->constrained(
            table: 'users', indexName: 'posts_user_id'
        );
    });

"on delete" 또는 "on update" 동작을 지정할 수도 있습니다:

    $table->foreignId('user_id')
        ->constrained()
        ->onUpdate('cascade')
        ->onDelete('cascade');

동등한 역할을 하는 명확한 문법도 지원됩니다:

<!-- 표는 원문 유지 -->

추가 [컬럼 수정자](#column-modifiers)가 필요하다면 `constrained`보다 먼저 호출해야 합니다:

    $table->foreignId('user_id')
        ->nullable()
        ->constrained();

<a name="dropping-foreign-keys"></a>
#### 외래키 삭제

외래키를 삭제하려면, 삭제할 외래키 제약조건의 이름을 인자로 전달하여 `dropForeign` 메서드를 사용합니다. 외래키 제약조건명은 테이블명, 컬럼명, `_foreign`의 관례로 정해집니다:

    $table->dropForeign('posts_user_id_foreign');

또는 외래키 컬럼명을 배열로 넘기면 Laravel이 자동으로 제약조건 이름을 만들어 삭제합니다:

    $table->dropForeign(['user_id']);

<a name="toggling-foreign-key-constraints"></a>
#### 외래키 제약조건 활성/비활성화

마이그레이션 안에서 외래키 제약조건을 활성 또는 비활성화할 수 있습니다:

    Schema::enableForeignKeyConstraints();

    Schema::disableForeignKeyConstraints();

    Schema::withoutForeignKeyConstraints(function () {
        // 이 클로저 내에서는 외래키 제약조건이 비활성화됩니다...
    });

> [!WARNING]  
> SQLite는 기본적으로 외래키 제약조건이 비활성화되어 있습니다. SQLite 사용할 경우 [외래키 지원 활성화](/docs/{{version}}/database#configuration) 후 마이그레이션에서 제약조건을 생성하세요.

<a name="events"></a>
## 이벤트

편의를 위해, 모든 마이그레이션 작업은 [이벤트](/docs/{{version}}/events)를 디스패치합니다. 아래 모든 이벤트는 기본 `Illuminate\Database\Events\MigrationEvent` 클래스를 상속합니다:

<!-- 표는 원문 유지 -->