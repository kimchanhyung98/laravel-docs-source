# 데이터베이스: 마이그레이션

- [소개](#introduction)
- [마이그레이션 생성](#generating-migrations)
    - [마이그레이션 합치기](#squashing-migrations)
- [마이그레이션 구조](#migration-structure)
- [마이그레이션 실행](#running-migrations)
    - [마이그레이션 롤백](#rolling-back-migrations)
- [테이블](#tables)
    - [테이블 생성](#creating-tables)
    - [테이블 수정](#updating-tables)
    - [테이블 이름 변경/삭제](#renaming-and-dropping-tables)
- [컬럼](#columns)
    - [컬럼 생성](#creating-columns)
    - [지원되는 컬럼 타입](#available-column-types)
    - [컬럼 수정자](#column-modifiers)
    - [컬럼 수정](#modifying-columns)
    - [컬럼 이름 변경](#renaming-columns)
    - [컬럼 삭제](#dropping-columns)
- [인덱스](#indexes)
    - [인덱스 생성](#creating-indexes)
    - [인덱스 이름 변경](#renaming-indexes)
    - [인덱스 삭제](#dropping-indexes)
    - [외래 키 제약조건](#foreign-key-constraints)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

마이그레이션은 데이터베이스 버전 관리와 같은 역할을 하여, 팀이 애플리케이션의 데이터베이스 스키마 정의를 명확히 정하고 공유할 수 있도록 합니다. 만약 소스 제어에서 변경 사항을 가져온 후 팀원에게 로컬 데이터베이스 스키마에 수동으로 컬럼을 추가해 달라고 요청한 경험이 있다면, 그 문제는 데이터베이스 마이그레이션으로 해결할 수 있습니다.

Laravel의 `Schema` [파사드](/docs/{{version}}/facades)는 모든 지원되는 데이터베이스 시스템에서 데이터베이스에 종속되지 않고 테이블을 생성하고 수정할 수 있도록 지원합니다. 일반적으로 마이그레이션은 이 파사드를 사용하여 테이블 및 컬럼을 생성 및 수정합니다.

<a name="generating-migrations"></a>
## 마이그레이션 생성

`make:migration` [Artisan 명령어](/docs/{{version}}/artisan)를 사용하여 데이터베이스 마이그레이션을 생성할 수 있습니다. 새 마이그레이션 파일은 `database/migrations` 디렉터리에 생성됩니다. 각 마이그레이션 파일 이름에는 Laravel이 마이그레이션의 실행 순서를 결정할 수 있도록 타임스탬프가 포함됩니다:

```shell
php artisan make:migration create_flights_table
```

Laravel은 마이그레이션 이름을 바탕으로 테이블의 이름과 해당 마이그레이션이 새 테이블을 생성할지 여부를 예측하려 시도합니다. 마이그레이션 이름에서 테이블 이름을 파악할 수 있다면 지정한 테이블로 마이그레이션 파일을 미리 채웁니다. 그렇지 않은 경우, 마이그레이션 파일에서 직접 테이블을 지정하면 됩니다.

생성된 마이그레이션의 경로를 직접 지정하고 싶다면, `make:migration` 명령어 실행 시 `--path` 옵션을 사용할 수 있습니다. 이때 지정한 경로는 애플리케이션의 기본경로를 기준으로 상대 경로여야 합니다.

> **참고**  
> 마이그레이션 스텁 파일은 [스텁 퍼블리싱](/docs/{{version}}/artisan#stub-customization)를 이용해 커스터마이즈할 수 있습니다.

<a name="squashing-migrations"></a>
### 마이그레이션 합치기

애플리케이션을 개발하면서 시간이 지남에 따라 점점 더 많은 마이그레이션 파일이 누적될 수 있습니다. 이로 인해 `database/migrations` 디렉터리가 수백 개의 마이그레이션 파일로 과도하게 부풀려질 수 있습니다. 필요하다면, 여러 마이그레이션을 하나의 SQL 파일로 "합칠" 수 있습니다. 시작하려면 `schema:dump` 명령어를 실행하세요:

```shell
php artisan schema:dump

# 현재 데이터베이스 스키마를 덤프하고, 기존 모든 마이그레이션을 정리하려면...
php artisan schema:dump --prune
```

이 명령을 실행하면 Laravel은 애플리케이션의 `database/schema` 디렉터리에 "스키마" 파일을 작성합니다. 스키마 파일 이름은 데이터베이스 연결명과 일치합니다. 이제 데이터베이스를 마이그레이션 하려고 할 때 실행된 다른 마이그레이션이 없다면, Laravel은 먼저 사용 중인 데이터베이스 연결의 스키마 파일에 담긴 SQL 문을 실행합니다. 그 후, 스키마 덤프에 포함되지 않은 나머지 마이그레이션을 실행합니다.

애플리케이션 테스트가 로컬 개발 중에 사용하는 데이터베이스 연결과 다른 연결을 사용한다면, 해당 데이터베이스 연결에서도 스키마 파일을 덤프해야 테스트시에 데이터베이스를 정상적으로 구축할 수 있습니다. 이는 주로 로컬 개발에 사용하는 데이터베이스 연결을 덤프한 후에 하게 됩니다:

```shell
php artisan schema:dump
php artisan schema:dump --database=testing --prune
```

이 스키마 파일은 팀의 새로운 개발자가 빠르게 초기 데이터베이스를 구축할 수 있도록 소스 제어에 커밋하는 것이 좋습니다.

> **경고**  
> 마이그레이션 합치기 기능은 MySQL, PostgreSQL, SQLite 데이터베이스에서만 사용할 수 있으며, 각 데이터베이스의 커맨드라인 클라이언트를 사용합니다. 스키마 덤프 파일은 인메모리 SQLite 데이터베이스에서는 복원할 수 없습니다.

<a name="migration-structure"></a>
## 마이그레이션 구조

마이그레이션 클래스는 두 개의 메소드 `up`과 `down`을 가집니다. `up` 메소드는 데이터베이스에 새로운 테이블, 컬럼, 인덱스를 추가할 때 사용되고, `down` 메소드는 `up`에서 수행한 작업을 되돌릴 때 사용됩니다.

이 두 메소드 모두에서 Laravel의 스키마 빌더를 활용해 간단하게 테이블을 생성/수정할 수 있습니다. `Schema` 빌더에서 사용할 수 있는 모든 메소드는 [해당 문서](#creating-tables)에서 확인하세요. 예를 들어, 아래 마이그레이션은 `flights` 테이블을 만듭니다:

    <?php

    use Illuminate\Database\Migrations\Migration;
    use Illuminate\Database\Schema\Blueprint;
    use Illuminate\Support\Facades\Schema;

    return new class extends Migration
    {
        /**
         * 마이그레이션을 실행합니다.
         *
         * @return void
         */
        public function up()
        {
            Schema::create('flights', function (Blueprint $table) {
                $table->id();
                $table->string('name');
                $table->string('airline');
                $table->timestamps();
            });
        }

        /**
         * 마이그레이션을 되돌립니다.
         *
         * @return void
         */
        public function down()
        {
            Schema::drop('flights');
        }
    };

<a name="setting-the-migration-connection"></a>
#### 마이그레이션 연결 설정

특정 마이그레이션이 기본 데이터베이스 연결이 아닌 다른 연결을 사용하도록 하려면, 마이그레이션의 `$connection` 프로퍼티를 지정해야 합니다:

    /**
    * 마이그레이션에서 사용할 데이터베이스 연결명.
    *
    * @var string
    */
    protected $connection = 'pgsql';

    /**
    * 마이그레이션 실행.
    *
    * @return void
    */
    public function up()
    {
        //
    }

<a name="running-migrations"></a>
## 마이그레이션 실행

모든 대기 중인 마이그레이션을 실행하려면 `migrate` Artisan 명령어를 사용하세요:

```shell
php artisan migrate
```

지금까지 실행된 마이그레이션 목록을 확인하려면 `migrate:status` 명령어를 사용할 수 있습니다:

```shell
php artisan migrate:status
```

마이그레이션을 실제로 실행하지 않고 실행될 SQL 문을 확인하고 싶으면 `--pretend` 플래그를 추가하세요:

```shell
php artisan migrate --pretend
```

#### 마이그레이션 실행 격리

여러 서버에 애플리케이션을 배포하면서 배포 과정에서 마이그레이션을 수행한다면, 두 서버가 동시에 마이그레이션을 시도하는 일을 방지해야 합니다. 이를 위해 `migrate` 명령어에 `--isolated` 옵션을 사용할 수 있습니다.

`isolated` 옵션이 제공되면, Laravel은 마이그레이션 실행 전 애플리케이션의 캐시 드라이버를 사용하여 원자적(atomic) 락을 획득합니다. 동일 락이 유지되는 동안 다른 마이그레이션 실행 시도는 실행되지 않으며, 명령은 성공적으로 종료됩니다:

```shell
php artisan migrate --isolated
```

> **경고**  
> 이 기능을 사용하려면, 애플리케이션의 기본 캐시 드라이버로 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 중 하나를 사용해야 합니다. 또한, 모든 서버가 같은 중앙 캐시 서버에 연결되어 있어야 합니다.

<a name="forcing-migrations-to-run-in-production"></a>
#### 운영환경에서 강제 마이그레이션

일부 마이그레이션 작업은 데이터 손실을 초래할 수 있습니다. 이에 따라 운영 데이터베이스에서 이런 명령을 실행하면 Laravel이 실행 전 확인을 요청합니다. 프롬프트 없이 명령을 강제로 실행하려면 `--force` 플래그를 사용하세요:

```shell
php artisan migrate --force
```

<a name="rolling-back-migrations"></a>
### 마이그레이션 롤백

마지막 마이그레이션 작업을 되돌리려면, `rollback` Artisan 명령어를 사용하세요. 이 명령은 마지막 "배치(batch)"의 모든 마이그레이션을 롤백합니다:

```shell
php artisan migrate:rollback
```

롤백할 마이그레이션 수를 제한하려면 `step` 옵션을 사용할 수 있습니다. 예를 들어, 최근 5개의 마이그레이션만 롤백하려면:

```shell
php artisan migrate:rollback --step=5
```

`migrate:reset` 명령은 애플리케이션의 모든 마이그레이션을 롤백합니다:

```shell
php artisan migrate:reset
```

<a name="roll-back-migrate-using-a-single-command"></a>
#### 롤백 및 마이그레이션 한 번에 실행

`migrate:refresh` 명령어는 모든 마이그레이션을 롤백하고 다시 `migrate` 명령을 실행합니다. 이 명령으로 전체 데이터베이스가 재구성됩니다:

```shell
php artisan migrate:refresh

# 데이터베이스를 리셋하고 모든 시드 작업도 같이 실행하려면...
php artisan migrate:refresh --seed
```

`step` 옵션으로 최근 몇 개의 마이그레이션만 롤백/재마이그레이션 할 수 있습니다:

```shell
php artisan migrate:refresh --step=5
```

<a name="drop-all-tables-migrate"></a>
#### 모든 테이블 삭제 및 마이그레이션

`migrate:fresh` 명령은 데이터베이스의 모든 테이블을 삭제한 후, `migrate`를 실행합니다:

```shell
php artisan migrate:fresh

php artisan migrate:fresh --seed
```

> **경고**  
> `migrate:fresh` 명령은 접두어(prefix)와 관계없이 모든 테이블을 삭제합니다. 다른 애플리케이션과 데이터베이스를 공유하는 경우 특히 주의해야 합니다.

<a name="tables"></a>
## 테이블

<a name="creating-tables"></a>
### 테이블 생성

새 데이터베이스 테이블을 생성하려면, `Schema` 파사드의 `create` 메소드를 사용하세요. 첫 번째 인자는 테이블 이름, 두 번째 인자는 `Blueprint` 객체를 전달받는 클로저입니다:

    use Illuminate\Database\Schema\Blueprint;
    use Illuminate\Support\Facades\Schema;

    Schema::create('users', function (Blueprint $table) {
        $table->id();
        $table->string('name');
        $table->string('email');
        $table->timestamps();
    });

테이블을 생성할 때는 스키마 빌더의 [컬럼 메소드](#creating-columns)를 자유롭게 사용할 수 있습니다.

<a name="checking-for-table-column-existence"></a>
#### 테이블/컬럼 존재 확인

`hasTable`과 `hasColumn` 메소드로 테이블이나 컬럼의 존재 여부를 확인할 수 있습니다:

    if (Schema::hasTable('users')) {
        // "users" 테이블이 존재합니다...
    }

    if (Schema::hasColumn('users', 'email')) {
        // "users" 테이블이 존재하고, "email" 컬럼이 있습니다...
    }

<a name="database-connection-table-options"></a>
#### 데이터베이스 연결 및 테이블 옵션

기본 연결이 아닌 다른 데이터베이스에서 스키마 작업을 해야 한다면 `connection` 메소드를 사용하세요:

    Schema::connection('sqlite')->create('users', function (Blueprint $table) {
        $table->id();
    });

그 외에도, MySQL 사용시 `engine` 프로퍼티로 저장 엔진을 지정할 수 있습니다:

    Schema::create('users', function (Blueprint $table) {
        $table->engine = 'InnoDB';

        // ...
    });

MySQL에서 생성할 테이블의 문자 집합과 정렬을 지정하려면 `charset`과 `collation` 프로퍼티를 사용하세요:

    Schema::create('users', function (Blueprint $table) {
        $table->charset = 'utf8mb4';
        $table->collation = 'utf8mb4_unicode_ci';

        // ...
    });

`temporary` 메소드로 테이블을 "임시" 테이블로 생성할 수도 있습니다. 임시 테이블은 현재 연결 세션에서만 접근 가능하며, 연결이 끊기면 자동으로 삭제됩니다:

    Schema::create('calculations', function (Blueprint $table) {
        $table->temporary();

        // ...
    });

MySQL과 Postgres에서만 지원하지만, 테이블에 "주석(comment)"을 남기고 싶으면 `comment` 메소드를 사용하세요:

    Schema::create('calculations', function (Blueprint $table) {
        $table->comment('비즈니스 계산용');

        // ...
    });

<a name="updating-tables"></a>
### 테이블 수정

`Schema` 파사드의 `table` 메소드는 기존 테이블을 수정할 때 사용합니다. 이 메소드 역시 첫 번째 인자로 테이블명, 두 번째 인자로 `Blueprint` 인스턴스를 받는 클로저를 전달합니다:

    use Illuminate\Database\Schema\Blueprint;
    use Illuminate\Support\Facades\Schema;

    Schema::table('users', function (Blueprint $table) {
        $table->integer('votes');
    });

<a name="renaming-and-dropping-tables"></a>
### 테이블 이름 변경/삭제

기존 테이블의 이름을 변경하려면 `rename` 메소드를 사용하십시오:

    use Illuminate\Support\Facades\Schema;

    Schema::rename($from, $to);

기존 테이블을 삭제하려면 `drop` 또는 `dropIfExists` 메소드를 사용하세요:

    Schema::drop('users');

    Schema::dropIfExists('users');

<a name="renaming-tables-with-foreign-keys"></a>
#### 외래키가 있는 테이블 이름 변경

테이블 이름을 바꾸기 전, 마이그레이션 파일에서 외래키 제약조건에 명시적으로 이름을 부여했는지 반드시 확인하세요. 그렇지 않으면, 외래키 이름이 내부 규칙을 따르기 때문에 기존 테이블 이름에 의존하게 됩니다.

<a name="columns"></a>
## 컬럼

<a name="creating-columns"></a>
### 컬럼 생성

`Schema` 파사드의 `table` 메소드로 기존 테이블에 컬럼을 추가할 수 있습니다. 사용법은 `create` 메소드와 동일하게, 첫 번째로 테이블명, 두 번째로 `Blueprint` 인스턴스를 전달받는 클로저를 넘깁니다:

    use Illuminate\Database\Schema\Blueprint;
    use Illuminate\Support\Facades\Schema;

    Schema::table('users', function (Blueprint $table) {
        $table->integer('votes');
    });

<a name="available-column-types"></a>
### 지원되는 컬럼 타입

스키마 빌더의 블루프린트에는 테이블에 추가 가능한 다양한 컬럼 타입을 위한 메소드들이 준비되어 있습니다. 제공되는 메소드 목록은 아래와 같습니다:

<style>
    .collection-method-list > p {
        columns: 10.8em 3; -moz-columns: 10.8em 3; -webkit-columns: 10.8em 3;
    }
    .collection-method-list a {
        display: block;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    .collection-method code {
        font-size: 14px;
    }
    .collection-method:not(.first-collection-method) {
        margin-top: 50px;
    }
</style>

<div class="collection-method-list" markdown="1">

[bigIncrements](#column-method-bigIncrements)
[bigInteger](#column-method-bigInteger)
[binary](#column-method-binary)
[boolean](#column-method-boolean)
[char](#column-method-char)
[dateTimeTz](#column-method-dateTimeTz)
[dateTime](#column-method-dateTime)
[date](#column-method-date)
[decimal](#column-method-decimal)
[double](#column-method-double)
[enum](#column-method-enum)
[float](#column-method-float)
[foreignId](#column-method-foreignId)
[foreignIdFor](#column-method-foreignIdFor)
[foreignUlid](#column-method-foreignUlid)
[foreignUuid](#column-method-foreignUuid)
[geometryCollection](#column-method-geometryCollection)
[geometry](#column-method-geometry)
[id](#column-method-id)
[increments](#column-method-increments)
[integer](#column-method-integer)
[ipAddress](#column-method-ipAddress)
[json](#column-method-json)
[jsonb](#column-method-jsonb)
[lineString](#column-method-lineString)
[longText](#column-method-longText)
[macAddress](#column-method-macAddress)
[mediumIncrements](#column-method-mediumIncrements)
[mediumInteger](#column-method-mediumInteger)
[mediumText](#column-method-mediumText)
[morphs](#column-method-morphs)
[multiLineString](#column-method-multiLineString)
[multiPoint](#column-method-multiPoint)
[multiPolygon](#column-method-multiPolygon)
[nullableMorphs](#column-method-nullableMorphs)
[nullableTimestamps](#column-method-nullableTimestamps)
[nullableUlidMorphs](#column-method-nullableUlidMorphs)
[nullableUuidMorphs](#column-method-nullableUuidMorphs)
[point](#column-method-point)
[polygon](#column-method-polygon)
[rememberToken](#column-method-rememberToken)
[set](#column-method-set)
[smallIncrements](#column-method-smallIncrements)
[smallInteger](#column-method-smallInteger)
[softDeletesTz](#column-method-softDeletesTz)
[softDeletes](#column-method-softDeletes)
[string](#column-method-string)
[text](#column-method-text)
[timeTz](#column-method-timeTz)
[time](#column-method-time)
[timestampTz](#column-method-timestampTz)
[timestamp](#column-method-timestamp)
[timestampsTz](#column-method-timestampsTz)
[timestamps](#column-method-timestamps)
[tinyIncrements](#column-method-tinyIncrements)
[tinyInteger](#column-method-tinyInteger)
[tinyText](#column-method-tinyText)
[unsignedBigInteger](#column-method-unsignedBigInteger)
[unsignedDecimal](#column-method-unsignedDecimal)
[unsignedInteger](#column-method-unsignedInteger)
[unsignedMediumInteger](#column-method-unsignedMediumInteger)
[unsignedSmallInteger](#column-method-unsignedSmallInteger)
[unsignedTinyInteger](#column-method-unsignedTinyInteger)
[ulidMorphs](#column-method-ulidMorphs)
[uuidMorphs](#column-method-uuidMorphs)
[ulid](#column-method-ulid)
[uuid](#column-method-uuid)
[year](#column-method-year)

</div>

(각 컬럼 타입의 설명은 [원본 문서](https://laravel.com/docs/10.x/migrations#available-column-types)를 참고하세요. 코드 블록은 번역하지 않음.)

<a name="column-modifiers"></a>
### 컬럼 수정자

위에 나열된 컬럼 타입 외에도, 컬럼 추가 시 사용할 수 있는 여러 "수정자" 메소드가 있습니다. 예를 들어 컬럼을 "nullable"로 만들려면 `nullable` 메소드를 사용할 수 있습니다:

    use Illuminate\Database\Schema\Blueprint;
    use Illuminate\Support\Facades\Schema;

    Schema::table('users', function (Blueprint $table) {
        $table->string('email')->nullable();
    });

다음 표는 모든 가용 컬럼 수정자를 안내합니다(인덱스 수정자는 포함하지 않음):

수정자  |  설명
------  |  -----
`->after('column')`  |  다른 컬럼 "뒤에" 컬럼을 배치(MySQL).
`->autoIncrement()`  |  INTEGER 컬럼을 자동 증가(기본키)로 지정.
`->charset('utf8mb4')`  |  문자셋 지정(MySQL).
`->collation('utf8mb4_unicode_ci')`  |  정렬 규칙 지정(MySQL/PostgreSQL/SQL Server).
`->comment('my comment')`  |  컬럼에 주석 추가(MySQL/PostgreSQL).
`->default($value)`  |  컬럼의 기본값 지정.
`->first()`  |  테이블의 맨 처음에 컬럼 배치(MySQL).
`->from($integer)`  |  auto-increment 필드의 시작값 설정(MySQL / PostgreSQL).
`->invisible()`  |  `SELECT *` 쿼리에서 컬럼을 보이지 않게 함(MySQL).
`->nullable($value = true)`  |  컬럼에 NULL 값 허용.
`->storedAs($expression)`  |  저장된 생성 컬럼 생성(MySQL / PostgreSQL).
`->unsigned()`  |  INTEGER 컬럼을 UNSIGNED로 설정(MySQL).
`->useCurrent()`  |  TIMESTAMP 컬럼의 기본값을 CURRENT_TIMESTAMP로 설정.
`->useCurrentOnUpdate()`  |  레코드 업데이트 시 TIMESTAMP 컬럼 값을 CURRENT_TIMESTAMP로 설정.
`->virtualAs($expression)`  |  가상 생성 컬럼을 생성(MySQL / PostgreSQL / SQLite).
`->generatedAs($expression)`  |  지정된 시퀀스 옵션으로 ID 컬럼 생성(PostgreSQL).
`->always()`  |  시퀀스 값이 입력 값에 우선하도록 설정(PostgreSQL).
`->isGeometry()`  |  공간 컬럼 타입을 `geometry`로 설정(기본값은 `geography`, PostgreSQL).

<a name="default-expressions"></a>
#### 기본값 표현식

`default` 수정자는 값이나 `Illuminate\Database\Query\Expression` 인스턴스를 받을 수 있습니다. `Expression` 인스턴스를 사용하면, Laravel이 값을 따옴표로 감싸지 않고 DB 전용 함수를 바로 활용할 수 있습니다. 예를 들어 JSON 컬럼에 기본값을 할당할 때 다음과 같이 유용하게 사용할 수 있습니다:

(코드 블록은 번역 제외, 원문 참고)

> **경고**  
> 기본값 표현식 지원 여부는 데이터베이스 드라이버, DB 버전 및 필드 타입에 따라 다릅니다. 자세한 내용은 DB 공식 문서를 참조하세요. 또한 `DB::raw()`와 같이 raw `default` 표현식을 `change` 메소드로 컬럼과 함께 변경할 수는 없습니다.

<a name="column-order"></a>
#### 컬럼 순서

MySQL 데이터베이스를 사용할 때는 `after` 메소드로 기존 컬럼 뒤에 컬럼을 추가할 수 있습니다:

    $table->after('password', function ($table) {
        $table->string('address_line1');
        $table->string('address_line2');
        $table->string('city');
    });

<a name="modifying-columns"></a>
### 컬럼 수정

<a name="prerequisites"></a>
#### 사전 준비

컬럼을 수정하기 전, Composer를 사용해 `doctrine/dbal` 패키지를 설치해야 합니다. Doctrine DBAL 라이브러리는 컬럼의 현재 상태를 파악하며, 요청된 변경 사항을 적용하는 데 필요한 SQL 쿼리를 생성합니다:

    composer require doctrine/dbal

`timestamp` 메소드로 생성한 컬럼을 수정하려면, 애플리케이션 `config/database.php`에 다음 구성을 추가해야 합니다:

```php
use Illuminate\Database\DBAL\TimestampType;

'dbal' => [
    'types' => [
        'timestamp' => TimestampType::class,
    ],
],
```

> **경고**  
> Microsoft SQL Server를 사용하는 경우 반드시 `doctrine/dbal:^3.0`을 설치해야 합니다.

<a name="updating-column-attributes"></a>
#### 컬럼 속성 수정

`change` 메소드는 기존 컬럼의 타입 및 속성을 변경할 수 있습니다. 예를 들어 `string` 컬럼의 길이를 늘리려면 아래처럼 작성합니다:

    Schema::table('users', function (Blueprint $table) {
        $table->string('name', 50)->change();
    });

또는 컬럼을 nullable로 수정할 수도 있습니다:

    Schema::table('users', function (Blueprint $table) {
        $table->string('name', 50)->nullable()->change();
    });

> **경고**  
> 수정 가능한 컬럼 타입은 `bigInteger`, `binary`, `boolean`, `char`, `date`, `dateTime`, `dateTimeTz`, `decimal`, `double`, `integer`, `json`, `longText`, `mediumText`, `smallInteger`, `string`, `text`, `time`, `tinyText`, `unsignedBigInteger`, `unsignedInteger`, `unsignedSmallInteger`, `uuid`입니다.  `timestamp` 컬럼은 [Doctrine 타입을 등록](#prerequisites)해야만 수정할 수 있습니다.

<a name="renaming-columns"></a>
### 컬럼 이름 변경

컬럼의 이름을 변경하려면, 스키마 빌더가 제공하는 `renameColumn` 메소드를 사용하세요:

    Schema::table('users', function (Blueprint $table) {
        $table->renameColumn('from', 'to');
    });

<a name="renaming-columns-on-legacy-databases"></a>
#### 레거시 데이터베이스에서 컬럼 이름 변경

아래 릴리즈 이전 버전의 데이터베이스를 사용하는 경우, 컬럼 이름을 변경하기 전 Composer로 `doctrine/dbal`을 설치해야 합니다:

<div class="content-list" markdown="1">

- MySQL < `8.0.3`
- MariaDB < `10.5.2`
- SQLite < `3.25.0`

</div>

<a name="dropping-columns"></a>
### 컬럼 삭제

컬럼을 삭제하려면 스키마 빌더의 `dropColumn` 메소드를 사용합니다:

    Schema::table('users', function (Blueprint $table) {
        $table->dropColumn('votes');
    });

여러 컬럼을 한 번에 제거하려면 컬럼명 배열을 넘기세요:

    Schema::table('users', function (Blueprint $table) {
        $table->dropColumn(['votes', 'avatar', 'location']);
    });

<a name="dropping-columns-on-legacy-databases"></a>
#### 레거시 데이터베이스에서 컬럼 삭제

SQLite 3.35.0 미만 버전을 사용하는 경우, `dropColumn` 메소드 사용 전 Composer로 `doctrine/dbal` 패키지를 설치해야 합니다. 이 패키지를 사용하는 동안 단일 마이그레이션에서 여러 컬럼을 삭제 또는 변경하는 것은 지원되지 않습니다.

<a name="available-command-aliases"></a>
#### 제공되는 명령어 별칭

Laravel은 자주 쓰이는 컬럼 유형에 대해 손쉽게 삭제할 수 있도록 여러 별칭 메소드를 지원합니다. 각 메소드는 아래 표와 같습니다:

명령어  |  설명
------ | ------
`$table->dropMorphs('morphable');`  |  `morphable_id`와 `morphable_type` 컬럼 삭제
`$table->dropRememberToken();`  |  `remember_token` 컬럼 삭제
`$table->dropSoftDeletes();`  |  `deleted_at` 컬럼 삭제
`$table->dropSoftDeletesTz();`  |  `dropSoftDeletes()`의 별칭
`$table->dropTimestamps();`  |  `created_at`, `updated_at` 컬럼 삭제
`$table->dropTimestampsTz();` |  `dropTimestamps()`의 별칭

<a name="indexes"></a>
## 인덱스

<a name="creating-indexes"></a>
### 인덱스 생성

Laravel 스키마 빌더는 여러 종류의 인덱스를 지원합니다. 아래 예시는 `email` 컬럼을 만들면서 해당 컬럼에 유니크 인덱스를 지정합니다. 인덱스를 생성하려면 컬럼 정의에 `unique` 메소드를 바로 체이닝할 수 있습니다:

    use Illuminate\Database\Schema\Blueprint;
    use Illuminate\Support\Facades\Schema;

    Schema::table('users', function (Blueprint $table) {
        $table->string('email')->unique();
    });

혹은 컬럼을 먼저 정의한 후 인덱스를 추가할 수도 있습니다:

    $table->unique('email');

여러 컬럼을 조합해서 인덱스를 만들고 싶으면 컬럼명 배열을 전달하세요:

    $table->index(['account_id', 'created_at']);

생성되는 인덱스 이름은 기본적으로 테이블명, 컬럼명, 인덱스 타입을 조합해 자동 생성되지만, 두 번째 인자로 인덱스명을 직접 지정할 수도 있습니다:

    $table->unique('email', 'unique_email');

<a name="available-index-types"></a>
#### 지원되는 인덱스 타입

Laravel의 스키마 빌더 블루프린트 클래스는 각 인덱스 타입에 대응하는 메소드를 제공합니다. 각 인덱스 메소드는 (선택적으로) 인덱스명을 두 번째 인자로 받을 수 있습니다. 생략하면 테이블명, 컬럼명, 타입으로부터 자동 생성됩니다. 주요 인덱스 메소드는 아래와 같습니다:

명령어  |  설명
------- | ------
`$table->primary('id');`  |  기본키 추가
`$table->primary(['id', 'parent_id']);`  |  복합키 추가
`$table->unique('email');`  |  유니크 인덱스 추가
`$table->index('state');`  |  일반 인덱스 추가
`$table->fullText('body');`  |  전문(full text) 인덱스 추가(MySQL/PostgreSQL)
`$table->fullText('body')->language('english');` | 특정 언어 전문 인덱스(PostgreSQL)
`$table->spatialIndex('location');`  |  공간 인덱스 추가(SQLite 제외)

<a name="index-lengths-mysql-mariadb"></a>
#### 인덱스 길이 & MySQL/MariaDB

Laravel은 기본적으로 `utf8mb4` 문자셋을 사용합니다. MySQL 5.7.7 미만 또는 MariaDB 10.2.2 미만 버전에서 마이그레이션이 생성하는 문자열 길이를 직접 설정해야 인덱스 생성에 실패하지 않습니다. 이를 위해 `App\Providers\AppServiceProvider` 클래스의 `boot` 메소드에서 `Schema::defaultStringLength`를 호출하세요:

    use Illuminate\Support\Facades\Schema;

    /**
     * 애플리케이션 서비스 부트스트랩.
     *
     * @return void
     */
    public function boot()
    {
        Schema::defaultStringLength(191);
    }

또는 데이터베이스 설정에서 `innodb_large_prefix` 옵션을 활성화할 수도 있습니다. 자세한 방법은 데이터베이스 공식 문서를 참고하세요.

<a name="renaming-indexes"></a>
### 인덱스 이름 변경

인덱스 이름을 변경하려면 스키마 빌더 블루프린트의 `renameIndex` 메소드를 사용하세요. 이 메소드는 현재 인덱스 이름과 변경할 이름을 인자로 받습니다:

    $table->renameIndex('from', 'to')

> **경고**  
> SQLite 데이터베이스를 사용할 경우, `renameIndex` 메소드 사용 전 Composer로 `doctrine/dbal`을 설치해야 합니다.

<a name="dropping-indexes"></a>
### 인덱스 삭제

인덱스를 삭제하려면 삭제할 인덱스 이름을 지정해야 합니다. Laravel은 기본적으로 테이블명, 컬럼명, 인덱스 타입으로 인덱스 이름을 자동 지정합니다. 주요 예시는 아래와 같습니다:

명령어  |  설명
------- | ------
`$table->dropPrimary('users_id_primary');`  |  "users" 테이블의 기본키 삭제
`$table->dropUnique('users_email_unique');`  |  "users" 테이블의 유니크 인덱스 삭제
`$table->dropIndex('geo_state_index');`  |  "geo" 테이블의 일반 인덱스 삭제
`$table->dropFullText('posts_body_fulltext');`  |  "posts" 테이블의 전문 인덱스 삭제
`$table->dropSpatialIndex('geo_location_spatialindex');`  |  "geo" 테이블 공간 인덱스 삭제(SQLite 제외)

컬럼명 배열을 넘기면 일반적인 인덱스 이름 규칙에 따라 자동 생성된 이름을 이용해 인덱스가 삭제됩니다:

    Schema::table('geo', function (Blueprint $table) {
        $table->dropIndex(['state']); // 'geo_state_index' 인덱스 삭제
    });

<a name="foreign-key-constraints"></a>
### 외래 키 제약조건

Laravel은 외래 키 제약조건을 정의할 수 있도록 지원합니다. 이 제약조건은 참조 무결성을 데이터베이스 레벨에서 강제합니다. 예를 들어, `posts` 테이블의 `user_id` 컬럼이 `users` 테이블의 `id`를 참조하도록 하려면:

    use Illuminate\Database\Schema\Blueprint;
    use Illuminate\Support\Facades\Schema;

    Schema::table('posts', function (Blueprint $table) {
        $table->unsignedBigInteger('user_id');

        $table->foreign('user_id')->references('id')->on('users');
    });

이 코드는 다소 장황할 수 있으니, Laravel은 더 간단한 방법을 제공합니다. 예를 들어 `foreignId` 메소드로 컬럼을 추가한 뒤 `constrained`를 체이닝하면 됩니다:

    Schema::table('posts', function (Blueprint $table) {
        $table->foreignId('user_id')->constrained();
    });

`foreignId` 메소드는 `UNSIGNED BIGINT` 타입 컬럼을, `constrained` 메소드는 참조할 테이블과 컬럼을 규칙에 따라 자동 지정합니다. 만약 테이블명이 규칙과 다르면 `constrained` 메소드의 인자로 직접 테이블명을 지정하면 됩니다:

    Schema::table('posts', function (Blueprint $table) {
        $table->foreignId('user_id')->constrained('users');
    });

외래키 삭제 및 수정 시 동작(ON DELETE, ON UPDATE)을 지정할 수도 있습니다:

    $table->foreignId('user_id')
          ->constrained()
          ->onUpdate('cascade')
          ->onDelete('cascade');

동등한, 좀 더 간결한 문법도 제공합니다:

메소드  | 설명
------- | ------
`$table->cascadeOnUpdate();` | 업데이트 시 CASCADE
`$table->restrictOnUpdate();`| 업데이트 시 RESTRICT
`$table->cascadeOnDelete();` | 삭제 시 CASCADE
`$table->restrictOnDelete();`| 삭제 시 RESTRICT
`$table->nullOnDelete();`    | 삭제 시 NULL로 설정

기타 [컬럼 수정자](#column-modifiers)는 반드시 `constrained` 호출 전에 체이닝 해야 합니다:

    $table->foreignId('user_id')
          ->nullable()
          ->constrained();

<a name="dropping-foreign-keys"></a>
#### 외래키 삭제

외래키를 삭제하려면 `dropForeign` 메소드에 제약조건명을 인자로 넘깁니다. 외래키 제약조건명은 인덱스 규칙과 동일하며, 테이블명, 컬럼명, `_foreign` 접미사로 구성됩니다:

    $table->dropForeign('posts_user_id_foreign');

또는 외래키 컬럼명을 배열로 넘기면, Laravel이 규칙에 맞는 이름으로 변환해 삭제합니다:

    $table->dropForeign(['user_id']);

<a name="toggling-foreign-key-constraints"></a>
#### 외래키 제약조건 활성/비활성

마이그레이션 내에서 다음 메소드로 외래키 제약조건을 켜고 끌 수 있습니다:

    Schema::enableForeignKeyConstraints();

    Schema::disableForeignKeyConstraints();

    Schema::withoutForeignKeyConstraints(function () {
        // 이 클로저 안에서는 제약조건이 비활성화됨...
    });

> **경고**  
> SQLite는 기본적으로 외래키를 비활성화합니다. SQLite를 사용할 경우, 마이그레이션에서 외래키를 만들기 전에 반드시 [외래키 지원을 데이터베이스 설정에서 활성화](/docs/{{version}}/database#configuration)해야 합니다. 또한, SQLite는 (테이블 변경 시에는 지원되지 않고) 테이블 생성시에만 외래키를 지원합니다. [자세히 보기](https://www.sqlite.org/omitted.html).

<a name="events"></a>
## 이벤트

편의상, 각 마이그레이션 작업은 [이벤트](/docs/{{version}}/events)를 디스패치합니다. 아래 이벤트들은 모두 기본 `Illuminate\Database\Events\MigrationEvent` 클래스를 확장합니다:

 클래스 | 설명
-------|------
| `Illuminate\Database\Events\MigrationsStarted` | 마이그레이션 배치 실행 직전 |
| `Illuminate\Database\Events\MigrationsEnded` | 마이그레이션 배치 실행 종료 |
| `Illuminate\Database\Events\MigrationStarted` | 단일 마이그레이션 실행 직전 |
| `Illuminate\Database\Events\MigrationEnded` | 단일 마이그레이션 실행 종료 |
| `Illuminate\Database\Events\SchemaDumped` | 데이터베이스 스키마 덤프 성공 |
| `Illuminate\Database\Events\SchemaLoaded` | 기존 데이터베이스 스키마 덤프 로딩 성공 |