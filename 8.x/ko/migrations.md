# 데이터베이스: 마이그레이션 (Database: Migrations)

- [소개](#introduction)
- [마이그레이션 생성하기](#generating-migrations)
    - [마이그레이션 합치기](#squashing-migrations)
- [마이그레이션 구조](#migration-structure)
- [마이그레이션 실행하기](#running-migrations)
    - [마이그레이션 롤백하기](#rolling-back-migrations)
- [테이블](#tables)
    - [테이블 생성](#creating-tables)
    - [테이블 수정](#updating-tables)
    - [테이블 이름 변경 및 삭제](#renaming-and-dropping-tables)
- [컬럼](#columns)
    - [컬럼 생성](#creating-columns)
    - [사용 가능한 컬럼 타입](#available-column-types)
    - [컬럼 수정자](#column-modifiers)
    - [컬럼 수정](#modifying-columns)
    - [컬럼 삭제](#dropping-columns)
- [인덱스](#indexes)
    - [인덱스 생성](#creating-indexes)
    - [인덱스 이름 변경](#renaming-indexes)
    - [인덱스 삭제](#dropping-indexes)
    - [외래 키 제약조건](#foreign-key-constraints)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

마이그레이션은 데이터베이스 버전 관리를 위한 도구로, 팀원들이 애플리케이션의 데이터베이스 스키마 정의를 함께 작성하고 공유할 수 있도록 해줍니다. 만약 소스 컨트롤에서 변경 사항을 받아온 후 동료에게 로컬 데이터베이스 스키마에 컬럼을 수동으로 추가하라고 이야기한 적이 있다면, 데이터베이스 마이그레이션이 해결하는 문제를 경험한 것입니다.

Laravel의 `Schema` [파사드](/docs/{{version}}/facades)는 Laravel이 지원하는 모든 데이터베이스 시스템에서 테이블 생성 및 조작을 데이터베이스 독립적으로 지원합니다. 일반적으로 마이그레이션은 이 파사드를 사용해 데이터베이스 테이블과 컬럼을 생성하고 수정합니다.

<a name="generating-migrations"></a>
## 마이그레이션 생성하기 (Generating Migrations)

`make:migration` [Artisan 명령어](/docs/{{version}}/artisan)를 사용하여 데이터베이스 마이그레이션을 생성할 수 있습니다. 새 마이그레이션 파일은 `database/migrations` 디렉토리에 저장되며, 각 파일명에는 타임스탬프가 포함되어 Laravel이 마이그레이션 순서를 판단할 수 있게 합니다:

```
php artisan make:migration create_flights_table
```

Laravel은 마이그레이션 이름을 기반으로 테이블 이름과 해당 마이그레이션이 새 테이블 생성인지 여부를 추론합니다. 만약 이름에서 테이블 이름을 알아낼 수 있다면, 생성된 마이그레이션 파일에 해당 테이블을 미리 작성해 줍니다. 그렇지 않으면 마이그레이션 파일 안에서 직접 테이블 이름을 지정할 수 있습니다.

특정 경로에 마이그레이션을 생성하려면 `make:migration` 명령 실행 시 `--path` 옵션을 사용하세요. 경로는 애플리케이션 기본 경로 기준 상대 경로를 지정해야 합니다.

> [!TIP]
> 마이그레이션 스텁(stub)은 [스텁 퍼블리싱 기능](/docs/{{version}}/artisan#stub-customization)을 통해 사용자 정의할 수 있습니다.

<a name="squashing-migrations"></a>
### 마이그레이션 합치기 (Squashing Migrations)

애플리케이션 개발이 진행될수록 마이그레이션 파일이 많아져 `database/migrations` 폴더가 불필요하게 커질 수 있습니다. 이 경우, 여러 마이그레이션을 하나의 SQL 파일로 "합칠" 수 있습니다. 다음 명령어로 시작하세요:

```
php artisan schema:dump

// 현재 데이터베이스 스키마를 덤프하고 기존 마이그레이션을 정리합니다...
php artisan schema:dump --prune
```

이 명령을 실행하면 Laravel이 `database/schema` 디렉토리에 "스키마" 파일을 작성합니다. 이제 데이터베이스 마이그레이션을 실행할 때, 만약 아직 실행된 마이그레이션이 없다면 우선 이 스키마 파일에 담긴 SQL 구문을 실행한 뒤, 그 후에 스키마 덤프에 포함되지 않은 나머지 마이그레이션들을 실행합니다.

이 스키마 파일은 소스 컨트롤에 커밋해 두어 팀의 신규 개발자가 애플리케이션 초기 데이터베이스 구조를 빠르게 생성할 수 있도록 해야 합니다.

> [!NOTE]
> 마이그레이션 합치기는 MySQL, PostgreSQL, SQLite 데이터베이스에서만 지원되며, 해당 데이터베이스 명령줄 클라이언트를 사용합니다. 메모리 내 SQLite 데이터베이스에는 스키마 덤프 복원이 지원되지 않습니다.

<a name="migration-structure"></a>
## 마이그레이션 구조 (Migration Structure)

마이그레이션 클래스는 `up`과 `down` 두 가지 메서드를 갖고 있습니다. `up` 메서드는 데이터베이스에 새 테이블, 컬럼, 인덱스 등을 추가하는 용도로, `down` 메서드는 `up` 메서드 작업을 되돌리는 역할을 합니다.

이 두 메서드 안에서 Laravel 스키마 빌더를 활용해 테이블을 생성하거나 수정할 수 있습니다. `Schema` 빌더의 모든 메서드를 알고 싶다면 [문서에서 확인](#creating-tables)하세요. 아래 예시는 `flights` 테이블을 생성하는 마이그레이션 예제입니다:

```
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateFlightsTable extends Migration
{
    /**
     * Run the migrations.
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
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::drop('flights');
    }
}
```

<a name="anonymous-migrations"></a>
#### 익명 마이그레이션 (Anonymous Migrations)

앞선 예제에서 보셨듯이, Laravel은 `make:migration` 커맨드로 생성한 마이그레이션에 자동으로 클래스명을 부여합니다. 하지만 필요하다면 익명 클래스를 반환하도록 마이그레이션 파일을 작성할 수도 있습니다. 이는 클래스명 충돌 우려가 있을 때 유용합니다:

```
<?php

use Illuminate\Database\Migrations\Migration;

return new class extends Migration
{
    //
};
```

<a name="setting-the-migration-connection"></a>
#### 마이그레이션 커넥션 설정하기 (Setting The Migration Connection)

마이그레이션 작업이 기본 데이터베이스 커넥션이 아닌 다른 연결을 사용해야 한다면, 마이그레이션 클래스의 `$connection` 속성을 설정하세요:

```
/**
 * The database connection that should be used by the migration.
 *
 * @var string
 */
protected $connection = 'pgsql';

/**
 * Run the migrations.
 *
 * @return void
 */
public function up()
{
    //
}
```

<a name="running-migrations"></a>
## 마이그레이션 실행하기 (Running Migrations)

대기 중인 모든 마이그레이션을 실행하려면 `migrate` Artisan 명령어를 사용합니다:

```
php artisan migrate
```

지금까지 실행된 마이그레이션 상태를 확인하려면 `migrate:status` 명령어를 사용하세요:

```
php artisan migrate:status
```

<a name="forcing-migrations-to-run-in-production"></a>
#### 프로덕션 환경에서 강제로 마이그레이션 실행하기 (Forcing Migrations To Run In Production)

일부 마이그레이션 작업은 데이터 손실 위험이 있으므로 프로덕션 데이터베이스에서는 실행 전 확인을 요구합니다. 확인 없이 강제로 실행하려면 `--force` 옵션을 사용하세요:

```
php artisan migrate --force
```

<a name="rolling-back-migrations"></a>
### 마이그레이션 롤백하기 (Rolling Back Migrations)

마지막 마이그레이션 작업을 되돌리려면 `rollback` Artisan 명령어를 사용합니다. 이 명령은 가장 최근에 실행된 "배치(batch)" 단위의 마이그레이션을 롤백하며, 여러 마이그레이션이 포함될 수 있습니다:

```
php artisan migrate:rollback
```

롤백할 마이그레이션 개수를 제한하려면 `step` 옵션을 제공합니다. 예를 들어, 최근 5개의 마이그레이션을 롤백하려면 다음과 같이 실행합니다:

```
php artisan migrate:rollback --step=5
```

모든 마이그레이션을 롤백하려면 `migrate:reset` 명령어를 사용하세요:

```
php artisan migrate:reset
```

<a name="roll-back-migrate-using-a-single-command"></a>
#### 한 명령으로 롤백 후 재실행하기 (Roll Back & Migrate Using A Single Command)

`migrate:refresh` 명령어는 모든 마이그레이션을 롤백한 뒤 `migrate`를 실행합니다. 즉, 데이터베이스를 완전히 재생성합니다:

```
php artisan migrate:refresh

// 데이터베이스를 새로고침하고 모든 시더도 실행...
php artisan migrate:refresh --seed
```

롤백 및 재실행할 마이그레이션 단계를 제한하려면 `step` 옵션을 제공합니다:

```
php artisan migrate:refresh --step=5
```

<a name="drop-all-tables-migrate"></a>
#### 모든 테이블 삭제 후 마이그레이션 실행 (Drop All Tables & Migrate)

`migrate:fresh` 명령어는 데이터베이스의 모든 테이블을 삭제한 뒤 마이그레이션을 실행합니다:

```
php artisan migrate:fresh

php artisan migrate:fresh --seed
```

> [!NOTE]
> `migrate:fresh` 명령은 접두사가 있는 테이블도 모두 삭제합니다. 다른 애플리케이션과 데이터베이스를 공유하는 개발 환경에서는 주의해서 사용하세요.

<a name="tables"></a>
## 테이블 (Tables)

<a name="creating-tables"></a>
### 테이블 생성 (Creating Tables)

새 데이터베이스 테이블은 `Schema` 파사드의 `create` 메서드로 만듭니다. `create` 메서드는 두 개의 인수를 받는데, 첫 번째는 테이블 이름, 두 번째는 `Blueprint` 객체를 전달받는 클로저입니다. 클로저 내부에서 새 테이블의 컬럼을 정의할 수 있습니다:

```
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::create('users', function (Blueprint $table) {
    $table->id();
    $table->string('name');
    $table->string('email');
    $table->timestamps();
});
```

테이블 생성 시, [컬럼 메서드](#creating-columns)를 활용해 컬럼을 정의할 수 있습니다.

<a name="checking-for-table-column-existence"></a>
#### 테이블 / 컬럼 존재 여부 확인하기 (Checking For Table / Column Existence)

`hasTable`과 `hasColumn` 메서드를 사용해 테이블 또는 컬럼이 존재하는지 확인할 수 있습니다:

```
if (Schema::hasTable('users')) {
    // "users" 테이블이 존재함...
}

if (Schema::hasColumn('users', 'email')) {
    // "users" 테이블에 "email" 컬럼이 존재함...
}
```

<a name="database-connection-table-options"></a>
#### 데이터베이스 커넥션 및 테이블 옵션 (Database Connection & Table Options)

기본 커넥션이 아닌 다른 데이터베이스 연결에서 스키마 작업을 수행하려면 `connection` 메서드를 사용하세요:

```
Schema::connection('sqlite')->create('users', function (Blueprint $table) {
    $table->id();
});
```

또한 몇 가지 속성 및 메서드로 테이블 생성 시 추가 옵션을 지정할 수 있습니다.

MySQL에서 테이블 저장 엔진을 지정하려면 `engine` 속성을 사용합니다:

```
Schema::create('users', function (Blueprint $table) {
    $table->engine = 'InnoDB';

    // ...
});
```

MySQL에서 문자 집합과 콜레이션을 지정하려면 각각 `charset`과 `collation` 속성을 사용합니다:

```
Schema::create('users', function (Blueprint $table) {
    $table->charset = 'utf8mb4';
    $table->collation = 'utf8mb4_unicode_ci';

    // ...
});
```

임시 테이블을 생성하려면 `temporary` 메서드를 호출합니다. 임시 테이블은 그 세션에서만 보이며, 연결 종료 시 자동 삭제됩니다:

```
Schema::create('calculations', function (Blueprint $table) {
    $table->temporary();

    // ...
});
```

<a name="updating-tables"></a>
### 테이블 수정 (Updating Tables)

기존 테이블을 수정할 때는 `Schema` 파사드의 `table` 메서드를 사용합니다. `create`와 마찬가지로, 첫 번째 인자는 테이블 이름, 두 번째 인자는 `Blueprint` 객체를 전달받는 클로저입니다. 컬럼이나 인덱스를 추가할 수 있습니다:

```
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->integer('votes');
});
```

<a name="renaming-and-dropping-tables"></a>
### 테이블 이름 변경 및 삭제 (Renaming / Dropping Tables)

기존 테이블 이름을 변경하려면 `rename` 메서드를 사용하세요:

```
use Illuminate\Support\Facades\Schema;

Schema::rename($from, $to);
```

테이블을 삭제하려면 `drop` 또는 `dropIfExists` 메서드를 사용합니다:

```
Schema::drop('users');

Schema::dropIfExists('users');
```

<a name="renaming-tables-with-foreign-keys"></a>
#### 외래 키가 걸린 테이블 이름 변경 시 주의사항

테이블 이름을 변경하기 전에, 해당 테이블에 걸린 외래 키 제약조건이 Laravel이 자동으로 생성한 이름 대신 명시적으로 이름이 지정되었는지 확인하세요. 그렇지 않으면 외래 키 제약조건 이름이 이전 테이블명을 참조하게 되어 문제가 생깁니다.

<a name="columns"></a>
## 컬럼 (Columns)

<a name="creating-columns"></a>
### 컬럼 생성 (Creating Columns)

기존 테이블에 컬럼을 추가하려면 `Schema` 파사드의 `table` 메서드를 사용합니다. 첫 번째 인자는 테이블 이름이고, 두 번째 인자는 `Illuminate\Database\Schema\Blueprint` 객체를 전달받는 클로저입니다. 이 클로저에서 컬럼을 정의합니다:

```
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->integer('votes');
});
```

<a name="available-column-types"></a>
### 사용 가능한 컬럼 타입 (Available Column Types)

스키마 빌더의 `Blueprint` 클래스는 다양한 컬럼 타입에 해당하는 메서드를 제공합니다. 주요 컬럼 메서드는 다음과 같습니다:

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

<a name="column-method-bigIncrements"></a>
#### `bigIncrements()`

`bigIncrements` 메서드는 자동 증가하는 `UNSIGNED BIGINT` (주 키) 컬럼을 생성합니다:

```
$table->bigIncrements('id');
```

<a name="column-method-bigInteger"></a>
#### `bigInteger()`

`bigInteger` 메서드는 `BIGINT` 타입의 컬럼을 생성합니다:

```
$table->bigInteger('votes');
```

<a name="column-method-binary"></a>
#### `binary()`

`binary` 메서드는 `BLOB` 타입의 컬럼을 생성합니다:

```
$table->binary('photo');
```

<a name="column-method-boolean"></a>
#### `boolean()`

`boolean` 메서드는 `BOOLEAN` 타입의 컬럼을 생성합니다:

```
$table->boolean('confirmed');
```

<a name="column-method-char"></a>
#### `char()`

`char` 메서드는 지정한 길이의 `CHAR` 타입 컬럼을 생성합니다:

```
$table->char('name', 100);
```

<a name="column-method-dateTimeTz"></a>
#### `dateTimeTz()`

`dateTimeTz` 메서드는 타임존을 포함하는 `DATETIME` 타입 컬럼을 생성하며, 정밀도(전체 자릿수)를 선택적으로 받을 수 있습니다:

```
$table->dateTimeTz('created_at', $precision = 0);
```

<a name="column-method-dateTime"></a>
#### `dateTime()`

`dateTime` 메서드는 `DATETIME` 타입 컬럼을 생성하며, 정밀도(전체 자릿수)를 선택적으로 받을 수 있습니다:

```
$table->dateTime('created_at', $precision = 0);
```

<a name="column-method-date"></a>
#### `date()`

`date` 메서드는 `DATE` 타입 컬럼을 생성합니다:

```
$table->date('created_at');
```

<a name="column-method-decimal"></a>
#### `decimal()`

`decimal` 메서드는 지정한 정밀도(전체 자릿수)와 소수점 이하 자리수를 가지는 `DECIMAL` 타입 컬럼을 생성합니다:

```
$table->decimal('amount', $precision = 8, $scale = 2);
```

<a name="column-method-double"></a>
#### `double()`

`double` 메서드는 지정한 정밀도 및 소수점 자릿수를 가지는 `DOUBLE` 타입 컬럼을 생성합니다:

```
$table->double('amount', 8, 2);
```

<a name="column-method-enum"></a>
#### `enum()`

`enum` 메서드는 지정한 유효 값 목록을 가지는 `ENUM` 타입 컬럼을 생성합니다:

```
$table->enum('difficulty', ['easy', 'hard']);
```

<a name="column-method-float"></a>
#### `float()`

`float` 메서드는 지정한 정밀도 및 소수 자릿수를 가지는 `FLOAT` 타입 컬럼을 생성합니다:

```
$table->float('amount', 8, 2);
```

<a name="column-method-foreignId"></a>
#### `foreignId()`

`foreignId` 메서드는 `UNSIGNED BIGINT` 타입 컬럼을 생성합니다:

```
$table->foreignId('user_id');
```

<a name="column-method-foreignIdFor"></a>
#### `foreignIdFor()`

`foreignIdFor` 메서드는 주어진 모델 클래스에 대응하는 `{컬럼}_id` `UNSIGNED BIGINT` 타입 컬럼을 생성합니다:

```
$table->foreignIdFor(User::class);
```

<a name="column-method-foreignUuid"></a>
#### `foreignUuid()`

`foreignUuid` 메서드는 `UUID` 타입 컬럼을 생성합니다:

```
$table->foreignUuid('user_id');
```

<a name="column-method-geometryCollection"></a>
#### `geometryCollection()`

`geometryCollection` 메서드는 `GEOMETRYCOLLECTION` 타입 컬럼을 생성합니다:

```
$table->geometryCollection('positions');
```

<a name="column-method-geometry"></a>
#### `geometry()`

`geometry` 메서드는 `GEOMETRY` 타입 컬럼을 생성합니다:

```
$table->geometry('positions');
```

<a name="column-method-id"></a>
#### `id()`

`id` 메서드는 `bigIncrements` 메서드의 별칭입니다. 기본값은 `id` 컬럼을 생성하지만, 다른 이름을 지정할 수도 있습니다:

```
$table->id();
```

<a name="column-method-increments"></a>
#### `increments()`

`increments` 메서드는 자동 증가하는 `UNSIGNED INTEGER` 타입 컬럼을 주 키로 생성합니다:

```
$table->increments('id');
```

<a name="column-method-integer"></a>
#### `integer()`

`integer` 메서드는 `INTEGER` 타입 컬럼을 생성합니다:

```
$table->integer('votes');
```

<a name="column-method-ipAddress"></a>
#### `ipAddress()`

`ipAddress` 메서드는 `VARCHAR` 타입 컬럼을 생성하며 주로 IP 주소 저장용입니다:

```
$table->ipAddress('visitor');
```

<a name="column-method-json"></a>
#### `json()`

`json` 메서드는 `JSON` 타입 컬럼을 생성합니다:

```
$table->json('options');
```

<a name="column-method-jsonb"></a>
#### `jsonb()`

`jsonb` 메서드는 `JSONB` 타입 컬럼을 생성합니다:

```
$table->jsonb('options');
```

<a name="column-method-lineString"></a>
#### `lineString()`

`lineString` 메서드는 `LINESTRING` 타입 컬럼을 생성합니다:

```
$table->lineString('positions');
```

<a name="column-method-longText"></a>
#### `longText()`

`longText` 메서드는 `LONGTEXT` 타입 컬럼을 생성합니다:

```
$table->longText('description');
```

<a name="column-method-macAddress"></a>
#### `macAddress()`

`macAddress` 메서드는 MAC 주소를 저장하기 위한 컬럼을 생성합니다. 일부 데이터베이스(PostgreSQL 등)는 전용 타입을, 다른 시스템은 문자열 컬럼을 사용합니다:

```
$table->macAddress('device');
```

<a name="column-method-mediumIncrements"></a>
#### `mediumIncrements()`

`mediumIncrements` 메서드는 자동증가하는 `UNSIGNED MEDIUMINT` 주 키 컬럼을 생성합니다:

```
$table->mediumIncrements('id');
```

<a name="column-method-mediumInteger"></a>
#### `mediumInteger()`

`mediumInteger` 메서드는 `MEDIUMINT` 타입 컬럼을 생성합니다:

```
$table->mediumInteger('votes');
```

<a name="column-method-mediumText"></a>
#### `mediumText()`

`mediumText` 메서드는 `MEDIUMTEXT` 타입 컬럼을 생성합니다:

```
$table->mediumText('description');
```

<a name="column-method-morphs"></a>
#### `morphs()`

`morphs` 메서드는 편의 메서드로, `{컬럼}_id` `UNSIGNED BIGINT` 타입 컬럼과 `{컬럼}_type` `VARCHAR` 타입 컬럼을 함께 생성합니다.

주로 다형성 [Eloquent 관계](/docs/{{version}}/eloquent-relationships)의 컬럼을 정의할 때 사용됩니다. 예를 들어, `taggable_id`와 `taggable_type` 컬럼이 생성됩니다:

```
$table->morphs('taggable');
```

<a name="column-method-multiLineString"></a>
#### `multiLineString()`

`multiLineString` 메서드는 `MULTILINESTRING` 타입 컬럼을 생성합니다:

```
$table->multiLineString('positions');
```

<a name="column-method-multiPoint"></a>
#### `multiPoint()`

`multiPoint` 메서드는 `MULTIPOINT` 타입 컬럼을 생성합니다:

```
$table->multiPoint('positions');
```

<a name="column-method-multiPolygon"></a>
#### `multiPolygon()`

`multiPolygon` 메서드는 `MULTIPOLYGON` 타입 컬럼을 생성합니다:

```
$table->multiPolygon('positions');
```

<a name="column-method-nullableTimestamps"></a>
#### `nullableTimestamps()`

`nullableTimestamps` 메서드는 [timestamps](#column-method-timestamps) 메서드의 별칭입니다:

```
$table->nullableTimestamps(0);
```

<a name="column-method-nullableMorphs"></a>
#### `nullableMorphs()`

`morphs` 메서드와 유사하지만, 컬럼들이 null 허용 상태로 생성됩니다:

```
$table->nullableMorphs('taggable');
```

<a name="column-method-nullableUuidMorphs"></a>
#### `nullableUuidMorphs()`

`uuidMorphs` 메서드와 유사하지만, 컬럼들이 null 허용 상태로 생성됩니다:

```
$table->nullableUuidMorphs('taggable');
```

<a name="column-method-point"></a>
#### `point()`

`point` 메서드는 `POINT` 타입 컬럼을 생성합니다:

```
$table->point('position');
```

<a name="column-method-polygon"></a>
#### `polygon()`

`polygon` 메서드는 `POLYGON` 타입 컬럼을 생성합니다:

```
$table->polygon('position');
```

<a name="column-method-rememberToken"></a>
#### `rememberToken()`

`rememberToken` 메서드는 nullable한 `VARCHAR(100)` 타입 컬럼을 생성하며, 로그인 유지용 [인증 토큰](/docs/{{version}}/authentication#remembering-users) 저장용으로 사용됩니다:

```
$table->rememberToken();
```

<a name="column-method-set"></a>
#### `set()`

`set` 메서드는 지정한 유효 값 목록을 가지는 `SET` 타입 컬럼을 생성합니다:

```
$table->set('flavors', ['strawberry', 'vanilla']);
```

<a name="column-method-smallIncrements"></a>
#### `smallIncrements()`

`smallIncrements` 메서드는 자동증가하는 `UNSIGNED SMALLINT` 주 키 컬럼을 생성합니다:

```
$table->smallIncrements('id');
```

<a name="column-method-smallInteger"></a>
#### `smallInteger()`

`smallInteger` 메서드는 `SMALLINT` 타입 컬럼을 생성합니다:

```
$table->smallInteger('votes');
```

<a name="column-method-softDeletesTz"></a>
#### `softDeletesTz()`

`softDeletesTz` 메서드는 nullable한 `deleted_at` 컬럼을 `TIMESTAMP` 타입(타임존 포함)으로 생성하며, 선택적으로 정밀도(전체 자릿수)를 지정할 수 있습니다. 이 컬럼은 Eloquent의 "소프트 딜리트(soft delete)" 기능에 사용됩니다:

```
$table->softDeletesTz($column = 'deleted_at', $precision = 0);
```

<a name="column-method-softDeletes"></a>
#### `softDeletes()`

`softDeletes` 메서드는 nullable한 `deleted_at` 컬럼을 `TIMESTAMP` 타입으로 생성하며, 선택적으로 정밀도를 지정할 수 있습니다. 역시 "소프트 딜리트" 기능용입니다:

```
$table->softDeletes($column = 'deleted_at', $precision = 0);
```

<a name="column-method-string"></a>
#### `string()`

`string` 메서드는 지정한 길이의 `VARCHAR` 타입 컬럼을 생성합니다:

```
$table->string('name', 100);
```

<a name="column-method-text"></a>
#### `text()`

`text` 메서드는 `TEXT` 타입 컬럼을 생성합니다:

```
$table->text('description');
```

<a name="column-method-timeTz"></a>
#### `timeTz()`

`timeTz` 메서드는 타임존을 포함하는 `TIME` 타입 컬럼을 생성하며, 선택적 정밀도를 지정할 수 있습니다:

```
$table->timeTz('sunrise', $precision = 0);
```

<a name="column-method-time"></a>
#### `time()`

`time` 메서드는 `TIME` 타입 컬럼을 생성하며 선택적 정밀도를 지정할 수 있습니다:

```
$table->time('sunrise', $precision = 0);
```

<a name="column-method-timestampTz"></a>
#### `timestampTz()`

`timestampTz` 메서드는 타임존 포함 `TIMESTAMP` 타입 컬럼을 생성하며 선택적 정밀도 지정이 가능합니다:

```
$table->timestampTz('added_at', $precision = 0);
```

<a name="column-method-timestamp"></a>
#### `timestamp()`

`timestamp` 메서드는 `TIMESTAMP` 타입 컬럼을 생성하며 선택적 정밀도 지정이 가능합니다:

```
$table->timestamp('added_at', $precision = 0);
```

<a name="column-method-timestampsTz"></a>
#### `timestampsTz()`

`timestampsTz` 메서드는 `created_at`과 `updated_at` 컬럼을 타임존 포함 `TIMESTAMP` 타입으로 생성하며 선택적 정밀도를 지정할 수 있습니다:

```
$table->timestampsTz($precision = 0);
```

<a name="column-method-timestamps"></a>
#### `timestamps()`

`timestamps` 메서드는 `created_at`과 `updated_at` 컬럼을 `TIMESTAMP` 타입으로 생성하며 선택적 정밀도를 지정할 수 있습니다:

```
$table->timestamps($precision = 0);
```

<a name="column-method-tinyIncrements"></a>
#### `tinyIncrements()`

`tinyIncrements` 메서드는 자동증가하는 `UNSIGNED TINYINT` 주 키 컬럼을 생성합니다:

```
$table->tinyIncrements('id');
```

<a name="column-method-tinyInteger"></a>
#### `tinyInteger()`

`tinyInteger` 메서드는 `TINYINT` 타입 컬럼을 생성합니다:

```
$table->tinyInteger('votes');
```

<a name="column-method-tinyText"></a>
#### `tinyText()`

`tinyText` 메서드는 `TINYTEXT` 타입 컬럼을 생성합니다:

```
$table->tinyText('notes');
```

<a name="column-method-unsignedBigInteger"></a>
#### `unsignedBigInteger()`

`unsignedBigInteger` 메서드는 `UNSIGNED BIGINT` 타입 컬럼을 생성합니다:

```
$table->unsignedBigInteger('votes');
```

<a name="column-method-unsignedDecimal"></a>
#### `unsignedDecimal()`

`unsignedDecimal` 메서드는 `UNSIGNED DECIMAL` 타입 컬럼을 생성하며 선택적인 정밀도와 소수 자리수를 지정할 수 있습니다:

```
$table->unsignedDecimal('amount', $precision = 8, $scale = 2);
```

<a name="column-method-unsignedInteger"></a>
#### `unsignedInteger()`

`unsignedInteger` 메서드는 `UNSIGNED INTEGER` 타입 컬럼을 생성합니다:

```
$table->unsignedInteger('votes');
```

<a name="column-method-unsignedMediumInteger"></a>
#### `unsignedMediumInteger()`

`unsignedMediumInteger` 메서드는 `UNSIGNED MEDIUMINT` 타입 컬럼을 생성합니다:

```
$table->unsignedMediumInteger('votes');
```

<a name="column-method-unsignedSmallInteger"></a>
#### `unsignedSmallInteger()`

`unsignedSmallInteger` 메서드는 `UNSIGNED SMALLINT` 타입 컬럼을 생성합니다:

```
$table->unsignedSmallInteger('votes');
```

<a name="column-method-unsignedTinyInteger"></a>
#### `unsignedTinyInteger()`

`unsignedTinyInteger` 메서드는 `UNSIGNED TINYINT` 타입 컬럼을 생성합니다:

```
$table->unsignedTinyInteger('votes');
```

<a name="column-method-uuidMorphs"></a>
#### `uuidMorphs()`

`uuidMorphs` 메서드는 편의 메서드로, `{컬럼}_id` `CHAR(36)` 타입 컬럼과 `{컬럼}_type` `VARCHAR` 타입 컬럼을 생성합니다.

UUID 식별자를 사용하는 다형성 [Eloquent 관계](/docs/{{version}}/eloquent-relationships)용 컬럼 생성에 쓰입니다. 예를 들어 `taggable_id`와 `taggable_type` 컬럼이 만들어집니다:

```
$table->uuidMorphs('taggable');
```

<a name="column-method-uuid"></a>
#### `uuid()`

`uuid` 메서드는 `UUID` 타입 컬럼을 생성합니다:

```
$table->uuid('id');
```

<a name="column-method-year"></a>
#### `year()`

`year` 메서드는 `YEAR` 타입 컬럼을 생성합니다:

```
$table->year('birth_year');
```

<a name="column-modifiers"></a>
### 컬럼 수정자 (Column Modifiers)

컬럼을 추가할 때, 위에서 소개한 컬럼 타입 이외에도 여러 "수정자"를 사용할 수 있습니다. 예를 들어 컬럼을 nullable로 만들려면 `nullable` 메서드를 사용하세요:

```
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->string('email')->nullable();
});
```

아래는 사용 가능한 컬럼 수정자 목록입니다. [인덱스 수정자](#creating-indexes)는 포함하지 않습니다:

| 수정자 | 설명 |
|----------------------------|---------------------------|
| `->after('column')`         | 지정한 컬럼 뒤에 새 컬럼을 추가 (MySQL). |
| `->autoIncrement()`         | INTEGER 컬럼을 자동증가(주 키)로 설정. |
| `->charset('utf8mb4')`      | 컬럼 문자셋 지정 (MySQL). |
| `->collation('utf8mb4_unicode_ci')` | 컬럼 콜레이션 지정 (MySQL/PostgreSQL/SQL Server). |
| `->comment('my comment')`   | 컬럼에 주석 추가 (MySQL/PostgreSQL). |
| `->default($value)`         | 컬럼 기본값 지정. |
| `->first()`                 | 테이블 내 컬럼을 가장 앞으로 위치시킴 (MySQL). |
| `->from($integer)`          | 자동증가 컬럼 시작 값 지정 (MySQL/PostgreSQL). |
| `->invisible()`             | `SELECT *` 쿼리에서 컬럼을 숨김 (MySQL). |
| `->nullable($value = true)` | NULL 허용 여부 설정. |
| `->storedAs($expression)`   | 저장된 생성 컬럼 정의 (MySQL/PostgreSQL). |
| `->unsigned()`              | INTEGER 컬럼을 UNSIGNED로 설정 (MySQL). |
| `->useCurrent()`            | TIMESTAMP 컬럼 기본값을 CURRENT_TIMESTAMP로 설정. |
| `->useCurrentOnUpdate()`    | TIMESTAMP 컬럼 업데이트 시 CURRENT_TIMESTAMP 사용. |
| `->virtualAs($expression)`  | 가상 생성 컬럼 정의 (MySQL/PostgreSQL/SQLite). |
| `->generatedAs($expression)`| 지정한 시퀀스 옵션을 가진 식별자 컬럼 생성 (PostgreSQL). |
| `->always()`                | 시퀀스 값 우선권 설정 (PostgreSQL). |
| `->isGeometry()`            | 공간 컬럼 타입을 `geometry`로 설정 (PostgreSQL, 기본값은 `geography`). |

<a name="default-expressions"></a>
#### 기본값 표현식 (Default Expressions)

`default` 수정자는 값 또는 `Illuminate\Database\Query\Expression` 인스턴스를 받을 수 있습니다. `Expression` 사용 시, Laravel이 값을 따옴표로 감싸지 않으며 DB 전용 함수도 쓸 수 있습니다. 예를 들어 JSON 컬럼에 기본값을 지정할 때 유용합니다:

```
<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Query\Expression;
use Illuminate\Database\Migrations\Migration;

class CreateFlightsTable extends Migration
{
    /**
     * Run the migrations.
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
```

> [!NOTE]
> 기본값 표현식 지원 여부는 사용하는 데이터베이스 드라이버, 버전, 컬럼 타입에 따라 다릅니다. 데이터베이스 문서를 참고하세요.

<a name="column-order"></a>
#### 컬럼 순서 (Column Order)

MySQL 데이터베이스 사용 시, `after` 메서드를 써서 기존 컬럼 뒤에 새 컬럼을 추가할 수 있습니다:

```
$table->after('password', function ($table) {
    $table->string('address_line1');
    $table->string('address_line2');
    $table->string('city');
});
```

<a name="modifying-columns"></a>
### 컬럼 수정하기 (Modifying Columns)

<a name="prerequisites"></a>
#### 사전 준비 (Prerequisites)

기존 컬럼을 수정하려면 Composer로 `doctrine/dbal` 패키지를 설치해야 합니다. 이 라이브러리는 컬럼의 현재 상태를 파악하고 변경에 필요한 SQL을 생성합니다:

```
composer require doctrine/dbal
```

만약 `timestamp` 컬럼을 수정할 경우, `config/database.php` 설정 파일에 다음 내용을 추가해야 합니다:

```php
use Illuminate\Database\DBAL\TimestampType;

'dbal' => [
    'types' => [
        'timestamp' => TimestampType::class,
    ],
],
```

> [!NOTE]
> Microsoft SQL Server 사용 시, 반드시 `doctrine/dbal:^3.0` 버전을 설치하세요.

<a name="updating-column-attributes"></a>
#### 컬럼 속성 수정하기 (Updating Column Attributes)

`change` 메서드를 사용하면 기존 컬럼의 타입이나 속성을 변경할 수 있습니다. 예를 들어 `name` 컬럼 길이를 25에서 50으로 늘리려면 다음처럼 작성합니다:

```
Schema::table('users', function (Blueprint $table) {
    $table->string('name', 50)->change();
});
```

또는 컬럼을 nullable로 변경할 수도 있습니다:

```
Schema::table('users', function (Blueprint $table) {
    $table->string('name', 50)->nullable()->change();
});
```

> [!NOTE]
> 수정 가능한 컬럼 타입은 다음과 같습니다: `bigInteger`, `binary`, `boolean`, `date`, `dateTime`, `dateTimeTz`, `decimal`, `integer`, `json`, `longText`, `mediumText`, `smallInteger`, `string`, `text`, `time`, `unsignedBigInteger`, `unsignedInteger`, `unsignedSmallInteger`, `uuid`. `timestamp` 컬럼 수정 시에는 [Doctrine 타입 등록](#prerequisites)이 필요합니다.

<a name="renaming-columns"></a>
#### 컬럼 이름 변경하기 (Renaming Columns)

컬럼 이름을 바꾸려면 schema builder의 `renameColumn` 메서드를 사용합니다. 단, 컬럼 이름 변경 전에 꼭 `doctrine/dbal`을 설치해야 합니다:

```
Schema::table('users', function (Blueprint $table) {
    $table->renameColumn('from', 'to');
});
```

> [!NOTE]
> 현재 `enum` 타입 컬럼의 이름 변경은 지원되지 않습니다.

<a name="dropping-columns"></a>
### 컬럼 삭제하기 (Dropping Columns)

컬럼을 삭제할 때는 `dropColumn` 메서드를 사용합니다. SQLite 데이터베이스를 사용하는 경우, 이 메서드 사용 전 `doctrine/dbal` 패키지 설치가 필요합니다:

```
Schema::table('users', function (Blueprint $table) {
    $table->dropColumn('votes');
});
```

여러 컬럼을 삭제하려면 컬럼 이름 배열을 전달하세요:

```
Schema::table('users', function (Blueprint $table) {
    $table->dropColumn(['votes', 'avatar', 'location']);
});
```

> [!NOTE]
> SQLite에서는 한 번에 여러 컬럼 삭제 또는 수정은 지원되지 않습니다.

<a name="available-command-aliases"></a>
#### 편리한 삭제 메서드 별칭 (Available Command Aliases)

Laravel은 자주 쓰이는 컬럼 삭제에 대한 편의 메서드를 제공합니다:

| 명령어 | 설명 |
|-------------------------------|-------------------------------|
| `$table->dropMorphs('morphable');`   | `morphable_id`와 `morphable_type` 컬럼 삭제. |
| `$table->dropRememberToken();`       | `remember_token` 컬럼 삭제. |
| `$table->dropSoftDeletes();`         | `deleted_at` 컬럼 삭제. |
| `$table->dropSoftDeletesTz();`       | `dropSoftDeletes()`의 별칭. |
| `$table->dropTimestamps();`           | `created_at`, `updated_at` 컬럼 삭제. |
| `$table->dropTimestampsTz();`         | `dropTimestamps()`의 별칭. |

<a name="indexes"></a>
## 인덱스 (Indexes)

<a name="creating-indexes"></a>
### 인덱스 생성 (Creating Indexes)

Laravel 스키마 빌더는 여러 인덱스 타입을 지원합니다. 예를 들어, `email` 컬럼을 유니크 인덱스로 지정하려면, 컬럼 정의에 `unique` 수정자를 체인할 수 있습니다:

```
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->string('email')->unique();
});
```

또는 컬럼 정의 후 인덱스 메서드로 인덱스를 만들 수도 있습니다. 이때는 인덱스를 적용할 컬럼 이름을 넘깁니다:

```
$table->unique('email');
```

복합 인덱스를 만들려면 컬럼 이름 배열을 전달하면 됩니다:

```
$table->index(['account_id', 'created_at']);
```

인덱스 생성 시 Laravel은 자동으로 인덱스 이름을 만드나, 두 번째 인수로 직접 이름을 지정할 수도 있습니다:

```
$table->unique('email', 'unique_email');
```

<a name="available-index-types"></a>
#### 사용 가능한 인덱스 타입 (Available Index Types)

Laravel 스키마 빌더에서 제공하는 인덱스 생성 메서드와 설명입니다(두 번째 인자는 인덱스 이름이며 생략 가능). 이름이 없으면 테이블명, 컬럼명, 인덱스 타입으로 이름이 자동 생성됩니다:

| 명령어 | 설명 |
|----------------------------|---------------------------|
| `$table->primary('id');`                      | 기본 키(primary key) 추가. |
| `$table->primary(['id', 'parent_id']);`      | 복합 기본 키 추가. |
| `$table->unique('email');`                    | 유니크 인덱스 추가. |
| `$table->index('state');`                     | 일반 인덱스 추가. |
| `$table->fulltext('body');`                   | 전체 텍스트 인덱스 추가 (MySQL/PostgreSQL). |
| `$table->fulltext('body')->language('english');` | 지정한 언어 전체 텍스트 인덱스 추가 (PostgreSQL). |
| `$table->spatialIndex('location');`           | 공간 인덱스 추가 (SQLite 제외). |

<a name="index-lengths-mysql-mariadb"></a>
#### 인덱스 길이 관련 MySQL / MariaDB 설정

기본적으로 Laravel은 `utf8mb4` 문자셋을 사용합니다. MySQL 5.7.7 미만 또는 MariaDB 10.2.2 미만을 사용한다면, 인덱스 생성 시 마이그레이션에서 문자열 길이를 수동으로 제한해야 할 수 있습니다. 앱 서비스 프로바이더의 `boot` 메서드에 `Schema::defaultStringLength`를 설정하세요:

```
use Illuminate\Support\Facades\Schema;

/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
{
    Schema::defaultStringLength(191);
}
```

또는 데이터베이스의 `innodb_large_prefix` 옵션을 직접 활성화할 수도 있습니다. 자세한 내용은 데이터베이스 문서를 참조하세요.

<a name="renaming-indexes"></a>
### 인덱스 이름 변경 (Renaming Indexes)

인덱스 이름을 바꾸려면 schema builder의 `renameIndex` 메서드를 사용하세요. 현재 이름과 새 이름을 순서대로 전달합니다:

```
$table->renameIndex('from', 'to');
```

<a name="dropping-indexes"></a>
### 인덱스 삭제 (Dropping Indexes)

인덱스를 삭제하려면 인덱스 이름을 지정해야 합니다. Laravel은 기본적으로 테이블명, 컬럼명, 인덱스 타입을 기준으로 인덱스 이름을 자동 생성합니다. 예시는 다음과 같습니다:

| 명령어 | 설명 |
|---------------------------------------|-----------------------------|
| `$table->dropPrimary('users_id_primary');`    | users 테이블 기본 키 삭제. |
| `$table->dropUnique('users_email_unique');`   | users 테이블 유니크 인덱스 삭제. |
| `$table->dropIndex('geo_state_index');`       | geo 테이블 일반 인덱스 삭제. |
| `$table->dropSpatialIndex('geo_location_spatialindex');` | geo 테이블 공간 인덱스 삭제 (SQLite 제외). |

컬럼 이름 배열을 넘기면 Laravel이 인덱스 이름을 자동으로 만듭니다:

```
Schema::table('geo', function (Blueprint $table) {
    $table->dropIndex(['state']); // 'geo_state_index' 인덱스 삭제
});
```

<a name="foreign-key-constraints"></a>
### 외래 키 제약조건 (Foreign Key Constraints)

Laravel은 데이터베이스 수준에서 참조 무결성을 보장할 외래 키 제약조건을 생성하는 기능도 제공합니다. 예를 들어 `posts` 테이블에 `user_id` 컬럼을 만들고 `users` 테이블의 `id` 컬럼을 참조하도록 하려면 다음과 같이 작성하세요:

```
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('posts', function (Blueprint $table) {
    $table->unsignedBigInteger('user_id');

    $table->foreign('user_id')->references('id')->on('users');
});
```

이 문법이 다소 장황하므로, Laravel은 컨벤션 기반의 짧은 메서드를 제공합니다. `foreignId` 메서드와 `constrained` 메서드를 사용하면 다음과 같이 표현할 수 있습니다:

```
Schema::table('posts', function (Blueprint $table) {
    $table->foreignId('user_id')->constrained();
});
```

`foreignId`는 `UNSIGNED BIGINT` 컬럼을 만들고, `constrained`는 참조 테이블/컬럼 이름을 관례에 따라 판단합니다. 만약 테이블명이 기본 컨벤션과 다르면 `constrained`에 인수로 직접 지정할 수 있습니다:

```
Schema::table('posts', function (Blueprint $table) {
    $table->foreignId('user_id')->constrained('users');
});
```

외래 키 제약조건의 "on delete" 또는 "on update" 동작을 지정하려면 다음과 같이 체인 메서드를 추가하세요:

```
$table->foreignId('user_id')
      ->constrained()
      ->onUpdate('cascade')
      ->onDelete('cascade');
```

대체 표현법도 있습니다:

| 메서드               | 설명               |
|----------------------|--------------------|
| `$table->cascadeOnUpdate();`  | 업데이트 시 연쇄 동작. |
| `$table->restrictOnUpdate();` | 업데이트 제한.        |
| `$table->cascadeOnDelete();`  | 삭제 시 연쇄 동작.    |
| `$table->restrictOnDelete();` | 삭제 제한.            |
| `$table->nullOnDelete();`     | 삭제 시 외래 키를 null로 설정. |

추가적인 [컬럼 수정자](#column-modifiers)는 `constrained` 메서드 호출 전에 사용해야 합니다:

```
$table->foreignId('user_id')
      ->nullable()
      ->constrained();
```

<a name="dropping-foreign-keys"></a>
#### 외래 키 삭제하기 (Dropping Foreign Keys)

외래 키를 제거하려면 `dropForeign` 메서드를 사용하며, 삭제할 외래 키 제약조건 이름을 넘깁니다. 외래 키 제약조건의 이름은 인덱스와 같은 규칙으로 생성되며, 보통 테이블명과 컬럼명에 `_foreign` 접미사가 붙습니다:

```
$table->dropForeign('posts_user_id_foreign');
```

또는 외래 키 컬럼명을 배열로 넘겨 Laravel이 규칙에 따라 제약조건 이름을 생성하도록 할 수 있습니다:

```
$table->dropForeign(['user_id']);
```

<a name="toggling-foreign-key-constraints"></a>
#### 외래 키 제약조건 활성화/비활성화

마이그레이션 내에서 외래 키 제약조건을 켜거나 끌 수 있습니다:

```
Schema::enableForeignKeyConstraints();

Schema::disableForeignKeyConstraints();
```

> [!NOTE]
> SQLite는 기본적으로 외래 키 제약조건이 비활성화되어 있습니다. SQLite를 사용할 때는 마이그레이션 실행 전에 외래 키 지원을 [활성화](/docs/{{version}}/database#configuration)해야 합니다. 또한 SQLite는 테이블 생성 시에만 외래 키를 지원하며, 테이블 변경 시에는 지원하지 않습니다(https://www.sqlite.org/omitted.html).

<a name="events"></a>
## 이벤트 (Events)

편의를 위해 모든 마이그레이션 작업은 [이벤트](/docs/{{version}}/events)를 발행합니다. 다음 이벤트들은 기본 `Illuminate\Database\Events\MigrationEvent` 클래스를 상속합니다:

| 클래스 | 설명 |
|-------------------------------|-----------------------------|
| `Illuminate\Database\Events\MigrationsStarted` | 마이그레이션 배치 실행 직전 이벤트. |
| `Illuminate\Database\Events\MigrationsEnded`   | 마이그레이션 배치 실행 완료 이벤트. |
| `Illuminate\Database\Events\MigrationStarted`  | 단일 마이그레이션 실행 직전 이벤트. |
| `Illuminate\Database\Events\MigrationEnded`    | 단일 마이그레이션 실행 완료 이벤트. |