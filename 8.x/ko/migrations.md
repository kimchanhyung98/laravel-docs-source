# 데이터베이스: 마이그레이션

- [소개](#introduction)
- [마이그레이션 생성](#generating-migrations)
    - [마이그레이션 압축(Squash)](#squashing-migrations)
- [마이그레이션 구조](#migration-structure)
- [마이그레이션 실행](#running-migrations)
    - [마이그레이션 롤백](#rolling-back-migrations)
- [테이블](#tables)
    - [테이블 생성](#creating-tables)
    - [테이블 수정](#updating-tables)
    - [테이블 이름 변경 / 삭제](#renaming-and-dropping-tables)
- [컬럼](#columns)
    - [컬럼 생성](#creating-columns)
    - [사용 가능한 컬럼 타입](#available-column-types)
    - [컬럼 수정자(Modifier)](#column-modifiers)
    - [컬럼 변경](#modifying-columns)
    - [컬럼 삭제](#dropping-columns)
- [인덱스](#indexes)
    - [인덱스 생성](#creating-indexes)
    - [인덱스 이름 변경](#renaming-indexes)
    - [인덱스 삭제](#dropping-indexes)
    - [외래 키 제약조건](#foreign-key-constraints)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

마이그레이션은 데이터베이스에 대한 버전 관리를 가능하게 해 줍니다. 즉, 팀원들과 애플리케이션의 데이터베이스 스키마 정의를 함께 관리하고 공유할 수 있게 해줍니다. 만약 여러분이 변경 사항을 소스 컨트롤에서 받은 뒤에 동료에게 로컬 데이터베이스 스키마에 수동으로 컬럼을 추가하라고 요청한 적이 있다면, 바로 이러한 문제를 마이그레이션이 해결해 줍니다.

Laravel의 `Schema` [파사드](/docs/{{version}}/facades)는 Laravel이 지원하는 모든 데이터베이스 시스템에서 데이터베이스에 독립적인 방식으로 테이블을 생성하고 조작할 수 있도록 지원합니다. 일반적으로 마이그레이션에서는 이 파사드를 사용해 데이터베이스 테이블과 컬럼을 생성하거나 수정합니다.

<a name="generating-migrations"></a>
## 마이그레이션 생성

`make:migration` [Artisan 명령어](/docs/{{version}}/artisan)를 사용하여 데이터베이스 마이그레이션을 생성할 수 있습니다. 새로 생성된 마이그레이션은 `database/migrations` 디렉터리에 위치하게 됩니다. 각 마이그레이션 파일명에는 Laravel이 마이그레이션 순서를 판단할 수 있도록 타임스탬프가 포함됩니다:

    php artisan make:migration create_flights_table

Laravel은 마이그레이션 이름을 통해 테이블 이름과 테이블 생성 여부를 추론하려 시도합니다. 만약 Laravel이 마이그레이션 이름에서 테이블 이름을 알아낼 수 있으면, 생성된 마이그레이션 파일에 해당 테이블이 미리 채워집니다. 아니라면, 마이그레이션 파일 내에서 직접 테이블을 지정할 수 있습니다.

생성된 마이그레이션의 경로를 직접 지정하고 싶다면, `make:migration` 명령어 실행 시 `--path` 옵션을 사용할 수 있습니다. 이때 경로는 애플리케이션의 기본 경로를 기준으로 상대 경로로 지정해야 합니다.

> {tip} 마이그레이션 스텁(stub)은 [스텁 퍼블리싱](/docs/{{version}}/artisan#stub-customization)를 통해 맞춤화할 수 있습니다.

<a name="squashing-migrations"></a>
### 마이그레이션 압축(Squash)

애플리케이션을 개발하다 보면 시간이 지날수록 많은 마이그레이션이 쌓이게 됩니다. 이로 인해 `database/migrations` 디렉터리에 수백 개의 마이그레이션 파일이 생길 수 있습니다. 원한다면, 여러 마이그레이션을 하나의 SQL 파일로 "압축"할 수 있습니다. 시작하려면, `schema:dump` 명령어를 실행하세요:

    php artisan schema:dump

    // 현재 데이터베이스 스키마를 덤프하고 기존 마이그레이션을 정리...
    php artisan schema:dump --prune

이 명령어를 실행하면 Laravel은 애플리케이션의 `database/schema` 디렉터리에 "스키마" 파일을 생성합니다. 이후 데이터베이스를 마이그레이트할 때 아직 다른 마이그레이션이 실행되지 않았다면, Laravel이 먼저 이 스키마 파일의 SQL 문을 실행합니다. 그리고 스키마 파일에 포함되지 않은 나머지 마이그레이션들을 순차적으로 적용합니다.

팀의 새로운 개발자가 애플리케이션의 초기 데이터베이스 구조를 빠르게 생성할 수 있도록, 데이터베이스 스키마 파일은 소스 컨트롤에 커밋해야 합니다.

> {note} 마이그레이션 압축(squash)은 오직 MySQL, PostgreSQL, SQLite 데이터베이스에서만 가능하며, 데이터베이스의 CLI 클라이언트를 사용합니다. 또한, 스키마 덤프는 인메모리 SQLite 데이터베이스로 복원할 수 없습니다.

<a name="migration-structure"></a>
## 마이그레이션 구조

마이그레이션 클래스는 `up`과 `down` 두 가지 메서드를 가집니다. `up` 메서드는 데이터베이스에 새 테이블, 컬럼, 인덱스 등을 추가할 때 사용하며, `down` 메서드는 `up`에서 수행한 작업을 되돌릴 때 사용합니다.

이 메서드들 내부에서는 Laravel의 스키마 빌더를 사용하여 테이블을 선언적이고 직관적으로 생성 및 수정할 수 있습니다. 스키마 빌더의 모든 메서드에 대해 자세히 알고 싶다면 [관련 문서](#creating-tables)를 참고하세요. 예를 들어, 아래 마이그레이션은 `flights` 테이블을 생성합니다:

    <?php

    use Illuminate\Database\Migrations\Migration;
    use Illuminate\Database\Schema\Blueprint;
    use Illuminate\Support\Facades\Schema;

    class CreateFlightsTable extends Migration
    {
        /**
         * 마이그레이션 실행.
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
         * 마이그레이션 롤백.
         *
         * @return void
         */
        public function down()
        {
            Schema::drop('flights');
        }
    }

<a name="anonymous-migrations"></a>
#### 익명 마이그레이션

위의 예시에서 볼 수 있듯, `make:migration` 명령어를 사용해 생성된 모든 마이그레이션에는 Laravel이 자동으로 클래스 이름을 부여합니다. 그러나 필요하다면 마이그레이션 파일에서 익명 클래스를 반환할 수도 있습니다. 이는 마이그레이션이 많아지면서 클래스 이름이 중복되는 상황에서 특히 유용합니다:

    <?php

    use Illuminate\Database\Migrations\Migration;

    return new class extends Migration
    {
        //
    };

<a name="setting-the-migration-connection"></a>
#### 마이그레이션 커넥션 설정

마이그레이션이 애플리케이션의 기본 데이터베이스 커넥션 이외의 데이터베이스와 상호작용해야 한다면, `$connection` 속성을 지정해야 합니다:

    /**
     * 마이그레이션에서 사용할 데이터베이스 커넥션.
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

모든 미적용된(미실행된) 마이그레이션을 실행하려면 `migrate` Artisan 명령어를 사용하세요:

    php artisan migrate

지금까지 적용된 마이그레이션 목록을 확인하려면 `migrate:status` Artisan 명령어를 사용할 수 있습니다:

    php artisan migrate:status

<a name="forcing-migrations-to-run-in-production"></a>
#### 프로덕션 환경에서 마이그레이션 강제 실행

일부 마이그레이션 작업은 데이터 손실을 초래할 수 있습니다. 프로덕션 데이터베이스에서 실수로 이러한 명령이 실행되는 것을 방지하기 위해, 명령 실행 전 확인 메시지가 표시됩니다. 프롬프트 없이 강제로 명령을 실행하려면 `--force` 플래그를 사용하세요:

    php artisan migrate --force

<a name="rolling-back-migrations"></a>
### 마이그레이션 롤백

가장 최근에 실행한 마이그레이션(마지막 "배치")을 롤백하려면 `rollback` Artisan 명령어를 사용하세요. 이 명령은 여러 마이그레이션 파일을 한 번에 롤백할 수 있습니다:

    php artisan migrate:rollback

`step` 옵션을 활용하면 정해진 개수만큼 롤백할 수 있습니다. 예를 들어, 아래 명령은 최근 5개의 마이그레이션을 롤백합니다:

    php artisan migrate:rollback --step=5

`migrate:reset` 명령은 애플리케이션의 모든 마이그레이션을 롤백합니다:

    php artisan migrate:reset

<a name="roll-back-migrate-using-a-single-command"></a>
#### 한 번에 롤백 & 마이그레이트

`migrate:refresh` 명령은 모든 마이그레이션을 롤백한 후 다시 `migrate` 명령을 실행합니다. 즉, 전체 데이터베이스를 재생성하는 효과가 있습니다:

    php artisan migrate:refresh

    // 데이터베이스를 리프레시하고 모든 데이터 시드를 실행...
    php artisan migrate:refresh --seed

`step` 옵션을 사용하면 지정된 개수만큼 롤백 및 재실행할 수 있습니다:

    php artisan migrate:refresh --step=5

<a name="drop-all-tables-migrate"></a>
#### 모든 테이블 삭제 & 마이그레이트

`migrate:fresh` 명령은 데이터베이스의 모든 테이블을 삭제한 후 다시 `migrate` 명령을 실행합니다:

    php artisan migrate:fresh

    php artisan migrate:fresh --seed

> {note} `migrate:fresh` 명령은 모든 데이터베이스 테이블을 프리픽스와 상관없이 삭제합니다. 이 명령은 다른 애플리케이션과 공유하는 데이터베이스에서는 주의해서 사용해야 합니다.

<a name="tables"></a>
## 테이블

<a name="creating-tables"></a>
### 테이블 생성

새 데이터베이스 테이블을 생성하려면, `Schema` 파사드의 `create` 메서드를 사용합니다. `create` 메서드는 테이블 이름과 테이블을 정의할 때 사용할 `Blueprint` 객체를 받는 클로저, 총 두 개의 인자를 인수로 받습니다:

    use Illuminate\Database\Schema\Blueprint;
    use Illuminate\Support\Facades\Schema;

    Schema::create('users', function (Blueprint $table) {
        $table->id();
        $table->string('name');
        $table->string('email');
        $table->timestamps();
    });

테이블을 생성할 때 [컬럼 메서드](#creating-columns)를 활용하여 테이블의 컬럼을 정의할 수 있습니다.

<a name="checking-for-table-column-existence"></a>
#### 테이블/컬럼 존재 여부 확인

`hasTable`, `hasColumn` 메서드를 사용하여 테이블 및 컬럼 존재 여부를 확인할 수 있습니다:

    if (Schema::hasTable('users')) {
        // "users" 테이블이 존재함...
    }

    if (Schema::hasColumn('users', 'email')) {
        // "users" 테이블에 "email" 컬럼이 존재함...
    }

<a name="database-connection-table-options"></a>
#### 데이터베이스 커넥션 & 테이블 옵션

기본 데이터베이스 커넥션이 아닌 다른 커넥션에서 스키마 작업을 수행하려면 `connection` 메서드를 사용하세요:

    Schema::connection('sqlite')->create('users', function (Blueprint $table) {
        $table->id();
    });

또한, 테이블 생성과 관련하여 추가적인 속성 및 메서드가 제공됩니다. MySQL 사용 시 `engine` 속성을 사용해 테이블의 스토리지 엔진을 지정할 수 있습니다:

    Schema::create('users', function (Blueprint $table) {
        $table->engine = 'InnoDB';

        // ...
    });

MySQL 사용 시 `charset`과 `collation` 속성으로 문자셋 및 콜레이션을 지정할 수 있습니다:

    Schema::create('users', function (Blueprint $table) {
        $table->charset = 'utf8mb4';
        $table->collation = 'utf8mb4_unicode_ci';

        // ...
    });

`temporary` 메서드를 사용하면 임시 테이블임을 명시할 수 있습니다. 임시 테이블은 현재 커넥션의 세션에서만 보이며 커넥션 종료 시 자동으로 삭제됩니다:

    Schema::create('calculations', function (Blueprint $table) {
        $table->temporary();

        // ...
    });

<a name="updating-tables"></a>
### 테이블 수정

기존 테이블을 수정하려면, `Schema` 파사드의 `table` 메서드를 사용합니다. `create`와 마찬가지로, 테이블 이름과, `Blueprint` 인스턴스를 받는 클로저를 인수로 받습니다:

    use Illuminate\Database\Schema\Blueprint;
    use Illuminate\Support\Facades\Schema;

    Schema::table('users', function (Blueprint $table) {
        $table->integer('votes');
    });

<a name="renaming-and-dropping-tables"></a>
### 테이블 이름 변경 / 삭제

기존 데이터베이스 테이블의 이름을 변경하려면 `rename` 메서드를 사용하세요:

    use Illuminate\Support\Facades\Schema;

    Schema::rename($from, $to);

기존 테이블을 삭제하려면, `drop` 또는 `dropIfExists` 메서드를 사용할 수 있습니다:

    Schema::drop('users');

    Schema::dropIfExists('users');

<a name="renaming-tables-with-foreign-keys"></a>
#### 외래 키가 있는 테이블 이름 변경

테이블 이름을 변경하기 전에, 마이그레이션 파일 내에서 외래 키 제약조건 이름을 명시적으로 지정하도록 해야 합니다. Laravel에 이름을 맡길 경우, 외래 키 제약조건 명이 기존 테이블명을 참조하게 됩니다.

<a name="columns"></a>
## 컬럼

<a name="creating-columns"></a>
### 컬럼 생성

기존 테이블에 컬럼을 추가하려면 `Schema` 파사드의 `table` 메서드를 사용합니다. 이는 `create`와 동일하게 동작하며, 테이블 이름과, `Illuminate\Database\Schema\Blueprint` 인스턴스를 받는 클로저를 인수로 받습니다:

    use Illuminate\Database\Schema\Blueprint;
    use Illuminate\Support\Facades\Schema;

    Schema::table('users', function (Blueprint $table) {
        $table->integer('votes');
    });

<a name="available-column-types"></a>
### 사용 가능한 컬럼 타입

스키마 빌더의 blueprint는 데이터베이스 테이블에 추가할 수 있는 다양한 컬럼 타입에 대응하는 메서드를 제공합니다. 사용 가능한 메서드는 다음 표와 같습니다:

<div id="collection-method-list" markdown="1">

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
[uuidMorphs](#column-method-uuidMorphs)
[uuid](#column-method-uuid)
[year](#column-method-year)

</div>

(컬럼 타입 별 상세 설명은 원문 블록을 참고하세요. 단, 용어 번역만 주의하세요.)

<a name="column-modifiers"></a>
### 컬럼 수정자(Modifier)

위의 컬럼 타입 외에도, 컬럼에 다양한 "수정자(Modifier)"를 사용할 수 있습니다. 예를 들어, 컬럼을 "nullable"로 만들고 싶다면 `nullable` 메서드를 사용하세요:

    use Illuminate\Database\Schema\Blueprint;
    use Illuminate\Support\Facades\Schema;

    Schema::table('users', function (Blueprint $table) {
        $table->string('email')->nullable();
    });

아래 표는 사용 가능한 모든 컬럼 수정자를 정리한 것입니다. [인덱스 관련 수정자](#creating-indexes)는 제외되어 있습니다.

수정자         | 설명
---------- | -----------
`->after('column')`  |  해당 컬럼을 "column" 뒤에 위치시킴(MySQL).
`->autoIncrement()`  |  정수 컬럼을 자동 증가(primary key)로 설정.
`->charset('utf8mb4')`  |  컬럼 문자셋 지정(MySQL).
`->collation('utf8mb4_unicode_ci')`  |  컬럼 콜레이션 지정(MySQL/PostgreSQL/SQL Server).
`->comment('my comment')`  |  컬럼 주석 설정(MySQL/PostgreSQL).
`->default($value)`  |  컬럼의 기본값 지정.
`->first()`  |  테이블 내 가장 앞에 컬럼 위치시킴(MySQL).
`->from($integer)`  |  자동 증가 시작 값 지정(MySQL / PostgreSQL).
`->invisible()`  |  컬럼을 `SELECT *` 쿼리에서 숨김(MySQL).
`->nullable($value = true)`  |  컬럼에 NULL 값 허용.
`->storedAs($expression)`  |  저장된 생성 컬럼 생성(MySQL / PostgreSQL).
`->unsigned()`  |  정수 컬럼 타입을 UNSIGNED로 지정(MySQL).
`->useCurrent()`  |  TIMESTAMP 컬럼 기본값을 CURRENT_TIMESTAMP로 설정.
`->useCurrentOnUpdate()`  |  레코드 업데이트 시 TIMESTAMP 컬럼을 CURRENT_TIMESTAMP로 자동 변경.
`->virtualAs($expression)`  |  가상 생성 컬럼 생성(MySQL / PostgreSQL / SQLite).
`->generatedAs($expression)`  |  시퀀스 옵션이 적용된 IDENTITY 컬럼 생성(PostgreSQL).
`->always()`  |  IDENTITY 컬럼에 대한 시퀀스 값 우선순위 지정(PostgreSQL).
`->isGeometry()`  |  공간 컬럼 타입을 `geometry`로 설정(기본값은 `geography`, PostgreSQL).

<a name="default-expressions"></a>
#### 기본값 표현식

`default` 수정자는 값이나 `Illuminate\Database\Query\Expression` 인스턴스를 받을 수 있습니다. `Expression` 인스턴스를 사용하면, Laravel이 값을 따옴표로 감싸지 않고, 데이터베이스 전용 함수를 그대로 사용할 수 있습니다. 예를 들어 JSON 컬럼에 기본값을 할당할 때 유용합니다:

    <?php

    use Illuminate\Support\Facades\Schema;
    use Illuminate\Database\Schema\Blueprint;
    use Illuminate\Database\Query\Expression;
    use Illuminate\Database\Migrations\Migration;

    class CreateFlightsTable extends Migration
    {
        /**
         * 마이그레이션 실행.
         *
         * @return void
         */
        public function up()
        {
            Schema::create('flights', function (Blueprint $table) {
                $table->id();
                $table->json('movies')->default(new Expression('(JSON_ARRAY())'));
                $table->timestamps();
            });
        }
    }

> {note} 기본값 표현식 지원 여부는 데이터베이스 드라이버/버전/필드타입에 따라 다르므로, 반드시 데이터베이스 문서를 참고하세요.

<a name="column-order"></a>
#### 컬럼 순서

MySQL 데이터베이스 사용 시, `after` 메서드를 통해 기존 컬럼 뒤에 새 컬럼을 추가할 수 있습니다:

    $table->after('password', function ($table) {
        $table->string('address_line1');
        $table->string('address_line2');
        $table->string('city');
    });

<a name="modifying-columns"></a>
### 컬럼 변경

<a name="prerequisites"></a>
#### 선행 조건

컬럼을 변경하기 전에, Composer로 `doctrine/dbal` 패키지를 먼저 설치해야 합니다. Doctrine DBAL 라이브러리는 컬럼의 현재 상태를 확인하고, 변경을 위한 SQL 쿼리를 생성하는 데 사용됩니다:

    composer require doctrine/dbal

`timestamp` 메서드로 생성된 컬럼을 변경할 계획이 있다면, 애플리케이션의 `config/database.php` 파일에 다음 설정도 추가해야 합니다:

```php
use Illuminate\Database\DBAL\TimestampType;

'dbal' => [
    'types' => [
        'timestamp' => TimestampType::class,
    ],
],
```

> {note} Microsoft SQL Server 사용 시에는 `doctrine/dbal:^3.0`을 설치해야 합니다.

<a name="updating-column-attributes"></a>
#### 컬럼 속성 변경

`change` 메서드를 사용하면 기존 컬럼의 타입과 속성을 변경할 수 있습니다. 예를 들어, `string` 컬럼의 길이를 늘리고 싶을 때 아래와 같이 사용할 수 있습니다:

    Schema::table('users', function (Blueprint $table) {
        $table->string('name', 50)->change();
    });

또는, 컬럼을 nullable로 변경할 수도 있습니다:

    Schema::table('users', function (Blueprint $table) {
        $table->string('name', 50)->nullable()->change();
    });

> {note} 변경 가능한 컬럼 타입: `bigInteger`, `binary`, `boolean`, `date`, `dateTime`, `dateTimeTz`, `decimal`, `integer`, `json`, `longText`, `mediumText`, `smallInteger`, `string`, `text`, `time`, `unsignedBigInteger`, `unsignedInteger`, `unsignedSmallInteger`, `uuid`.  `timestamp` 컬럼을 변경하려면 [Doctrine 타입 등록](#prerequisites)이 필요합니다.

<a name="renaming-columns"></a>
#### 컬럼 이름 변경

컬럼 이름을 변경하려면, 스키마 빌더 blueprint의 `renameColumn` 메서드를 사용합니다. 컬럼 이름 변경 전 Composer로 `doctrine/dbal`을 설치해야 합니다:

    Schema::table('users', function (Blueprint $table) {
        $table->renameColumn('from', 'to');
    });

> {note} 현재 `enum` 컬럼의 이름 변경은 지원되지 않습니다.

<a name="dropping-columns"></a>
### 컬럼 삭제

컬럼을 삭제하려면, 스키마 빌더 blueprint의 `dropColumn` 메서드를 사용하세요. SQLite 데이터베이스를 사용하는 경우, 먼저 Composer로 `doctrine/dbal` 패키지를 설치해야 합니다:

    Schema::table('users', function (Blueprint $table) {
        $table->dropColumn('votes');
    });

배열로 컬럼 이름들을 전달하여 여러 개의 컬럼을 한 번에 삭제할 수도 있습니다:

    Schema::table('users', function (Blueprint $table) {
        $table->dropColumn(['votes', 'avatar', 'location']);
    });

> {note} SQLite 사용 시, 한 마이그레이션에서 여러 컬럼을 동시에 삭제하거나 변경하는 것은 지원되지 않습니다.

<a name="available-command-aliases"></a>
#### 사용 가능한 명령어 별칭

Laravel은 자주 사용되는 컬럼 삭제 작업을 위한 편리한 메서드들을 제공합니다. 각 메서드는 아래와 같습니다:

명령어  |  설명
-------  |  -----------
`$table->dropMorphs('morphable');`  |  `morphable_id`, `morphable_type` 컬럼 삭제
`$table->dropRememberToken();`  |  `remember_token` 컬럼 삭제
`$table->dropSoftDeletes();`  |  `deleted_at` 컬럼 삭제
`$table->dropSoftDeletesTz();`  |  `dropSoftDeletes()` 메서드의 별칭
`$table->dropTimestamps();`  |  `created_at`, `updated_at` 컬럼 삭제
`$table->dropTimestampsTz();` |  `dropTimestamps()` 메서드의 별칭

<a name="indexes"></a>
## 인덱스

<a name="creating-indexes"></a>
### 인덱스 생성

Laravel 스키마 빌더는 여러 종류의 인덱스를 지원합니다. 예를 들어, 새로운 `email` 컬럼에 unique 인덱스를 지정하려면 다음과 같이 사용할 수 있습니다:

    use Illuminate\Database\Schema\Blueprint;
    use Illuminate\Support\Facades\Schema;

    Schema::table('users', function (Blueprint $table) {
        $table->string('email')->unique();
    });

컬럼 정의 이후에 인덱스를 생성할 수도 있습니다. 이때는 해당 컬럼 이름을 인자로 넘겨 `unique` 메서드를 호출하면 됩니다:

    $table->unique('email');

여러 컬럼에 대해 복합 인덱스(컴파운드 인덱스)를 생성하려면 배열을 전달하면 됩니다:

    $table->index(['account_id', 'created_at']);

인덱스 생성 시 Laravel이 자동으로 인덱스 이름을 만들어 주지만, 두 번째 인자로 직접 지정할 수도 있습니다:

    $table->unique('email', 'unique_email');

<a name="available-index-types"></a>
#### 사용 가능한 인덱스 타입

Laravel의 스키마 빌더 blueprint 클래스에는 Laravel에서 지원하는 각 인덱스 타입별로 별도의 메서드가 제공됩니다. 두 번째 인자로 인덱스 이름을 지정할 수 있으며, 생략하면 테이블/컬럼/인덱스 타입 정보가 조합됩니다. 각각의 인덱스 메서드는 아래와 같습니다:

명령어  |  설명
-------  |  -----------
`$table->primary('id');`  |  기본 키(Primary Key) 추가
`$table->primary(['id', 'parent_id']);`  |  복합 키(Composite Key) 추가
`$table->unique('email');`  |  유니크 인덱스 추가
`$table->index('state');`  |  일반 인덱스 추가
`$table->fulltext('body');`  |  전문(Fulltext) 인덱스 추가(MySQL/PostgreSQL)
`$table->fulltext('body')->language('english');`  |  언어 지정 전문 인덱스 추가(PostgreSQL)
`$table->spatialIndex('location');`  |  공간 인덱스 추가(SQLite 제외)

<a name="index-lengths-mysql-mariadb"></a>
#### 인덱스 길이 & MySQL / MariaDB

Laravel은 기본적으로 `utf8mb4` 문자셋을 사용합니다. MySQL 5.7.7 미만이나 MariaDB 10.2.2 미만 버전을 사용한다면, 마이그레이션 생성 시 인덱스 생성을 위해 문자열 기본 길이를 설정해 주어야 할 수 있습니다. `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 아래와 같이 지정합니다:

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

또는 데이터베이스에서 `innodb_large_prefix` 옵션을 활성화할 수도 있습니다. 자세한 내용은 데이터베이스 문서를 참고하세요.

<a name="renaming-indexes"></a>
### 인덱스 이름 변경

인덱스 이름을 변경하려면 스키마 빌더 blueprint의 `renameIndex` 메서드를 사용합니다. 기존 이름과 원하는 이름을 각각 첫 번째, 두 번째 인자로 전달합니다:

    $table->renameIndex('from', 'to')

<a name="dropping-indexes"></a>
### 인덱스 삭제

인덱스를 삭제하려면 해당 인덱스의 이름을 지정해야 합니다. Laravel은 테이블명, 컬럼명, 인덱스 타입을 조합하여 자동으로 인덱스 이름을 할당합니다. 예시는 다음과 같습니다.

명령어  |  설명
-------  |  -----------
`$table->dropPrimary('users_id_primary');`  |  "users" 테이블의 기본 키 삭제
`$table->dropUnique('users_email_unique');`  |  "users" 테이블의 유니크 인덱스 삭제
`$table->dropIndex('geo_state_index');`  |  "geo" 테이블의 일반 인덱스 삭제
`$table->dropSpatialIndex('geo_location_spatialindex');`  |  "geo" 테이블의 공간 인덱스 삭제(SQLite 제외)

컬럼 배열을 통해 인덱스 삭제 메서드를 호출하면, Laravel이 관례적인 인덱스 이름을 자동으로 생성합니다:

    Schema::table('geo', function (Blueprint $table) {
        $table->dropIndex(['state']); // 'geo_state_index' 인덱스 삭제
    });

<a name="foreign-key-constraints"></a>
### 외래 키 제약조건

Laravel은 데이터베이스 차원에서 참조 무결성을 보장할 수 있도록 외래 키 제약조건을 지원합니다. 예를 들어, `posts` 테이블에 `user_id` 컬럼을 추가하고, 이것이 `users` 테이블의 `id` 컬럼을 참조하도록 할 수 있습니다:

    use Illuminate\Database\Schema\Blueprint;
    use Illuminate\Support\Facades\Schema;

    Schema::table('posts', function (Blueprint $table) {
        $table->unsignedBigInteger('user_id');

        $table->foreign('user_id')->references('id')->on('users');
    });

이 문법이 다소 장황하므로, Laravel에서는 관례(convention)를 활용한 간결한 메서드도 제공합니다:

    Schema::table('posts', function (Blueprint $table) {
        $table->foreignId('user_id')->constrained();
    });

`foreignId` 메서드는 `UNSIGNED BIGINT` 컬럼을 생성하고, `constrained` 메서드는 참조할 테이블/컬럼명을 관례적으로 결정합니다. 테이블명이 Laravel의 관례와 다르다면, `constrained('테이블명')` 식으로 직접 지정해줄 수 있습니다:

    Schema::table('posts', function (Blueprint $table) {
        $table->foreignId('user_id')->constrained('users');
    });

또한 "on delete"와 "on update" 동작을 명시적으로 지정할 수도 있습니다:

    $table->foreignId('user_id')
          ->constrained()
          ->onUpdate('cascade')
          ->onDelete('cascade');

아래와 같이 더 직관적인 메서드도 제공됩니다:

메서드  |  설명
-------  |  -----------
`$table->cascadeOnUpdate();` | 변경 시 Cascade 처리
`$table->restrictOnUpdate();`| 변경 시 Restrict 처리
`$table->cascadeOnDelete();` | 삭제 시 Cascade 처리
`$table->restrictOnDelete();`| 삭제 시 Restrict 처리
`$table->nullOnDelete();`    | 삭제 시 외래키 필드를 null로 설정

추가적인 [컬럼 수정자](#column-modifiers)는 `constrained` 메서드 호출 전에 사용해야 합니다:

    $table->foreignId('user_id')
          ->nullable()
          ->constrained();

<a name="dropping-foreign-keys"></a>
#### 외래 키 삭제

외래 키를 삭제하려면, `dropForeign` 메서드를 사용해 삭제할 외래 키의 이름을 전달합니다. 외래 키 명명 규칙은 인덱스 명명 규칙과 같습니다. 즉, 테이블명, 컬럼명 뒤에 "_foreign"이 붙습니다:

    $table->dropForeign('posts_user_id_foreign');

또는 외래키가 달린 컬럼명을 배열로 전달할 수도 있습니다. 그러면 Laravel이 제약조건 이름을 자동으로 생성합니다:

    $table->dropForeign(['user_id']);

<a name="toggling-foreign-key-constraints"></a>
#### 외래 키 제약조건 활성화/비활성화

마이그레이션 내에서 다음 메서드를 사용해 외래 키 제약조건을 활성화 혹은 비활성화할 수 있습니다:

    Schema::enableForeignKeyConstraints();

    Schema::disableForeignKeyConstraints();

> {note} SQLite는 기본적으로 외래 키 제약조건이 비활성화되어 있습니다. 마이그레이션에서 외래 키를 생성하려면, 반드시 [설정에서 외래 키 지원을 활성화](/docs/{{version}}/database#configuration)하세요. 또한, SQLite에서는 테이블 생성 시에만 외래 키 제약조건이 지원되며, [테이블 변경 시에는 지원되지 않습니다](https://www.sqlite.org/omitted.html).

<a name="events"></a>
## 이벤트

편의를 위해, 각 마이그레이션 작업은 [이벤트](/docs/{{version}}/events)를 발생시킵니다. 아래 이벤트들은 모두 기본 `Illuminate\Database\Events\MigrationEvent` 클래스를 상속받습니다:

 클래스 | 설명
-------|-------
| `Illuminate\Database\Events\MigrationsStarted` | 여러 마이그레이션 실행이 시작되기 직전 발생 |
| `Illuminate\Database\Events\MigrationsEnded` | 여러 마이그레이션 실행이 모두 끝난 뒤 발생 |
| `Illuminate\Database\Events\MigrationStarted` | 단일 마이그레이션 실행 시작 전 발생 |
| `Illuminate\Database\Events\MigrationEnded` | 단일 마이그레이션 실행이 끝난 뒤 발생 |

---