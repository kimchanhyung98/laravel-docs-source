# 데이터베이스: 마이그레이션 (Database: Migrations)

- [소개](#introduction)
- [마이그레이션 생성하기](#generating-migrations)
    - [마이그레이션 스쿼싱](#squashing-migrations)
- [마이그레이션 구조](#migration-structure)
- [마이그레이션 실행하기](#running-migrations)
    - [마이그레이션 되돌리기](#rolling-back-migrations)
- [테이블](#tables)
    - [테이블 생성하기](#creating-tables)
    - [테이블 수정하기](#updating-tables)
    - [테이블 이름 변경 및 삭제](#renaming-and-dropping-tables)
- [컬럼](#columns)
    - [컬럼 생성하기](#creating-columns)
    - [사용 가능한 컬럼 타입](#available-column-types)
    - [컬럼 수정자](#column-modifiers)
    - [컬럼 수정하기](#modifying-columns)
    - [컬럼 이름 변경하기](#renaming-columns)
    - [컬럼 삭제하기](#dropping-columns)
- [인덱스](#indexes)
    - [인덱스 생성하기](#creating-indexes)
    - [인덱스 이름 변경하기](#renaming-indexes)
    - [인덱스 삭제하기](#dropping-indexes)
    - [외래 키 제약조건](#foreign-key-constraints)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

마이그레이션은 데이터베이스의 버전 관리와 같아서, 팀원끼리 애플리케이션 데이터베이스 스키마 정의를 공유하고 정의할 수 있도록 도와줍니다. 만약 소스 관리에서 변경 사항을 받아온 후 동료에게 로컬 데이터베이스에 수동으로 컬럼을 추가하라고 말해 본 적이 있다면, 데이터베이스 마이그레이션이 해결하는 문제를 경험한 것입니다.

Laravel의 `Schema` [파사드](/docs/9.x/facades)는 Laravel에서 지원하는 모든 데이터베이스 시스템에 호환되는 테이블 생성과 조작 기능을 제공합니다. 일반적으로 마이그레이션은 이 파사드를 사용해 데이터베이스 테이블과 컬럼을 생성하거나 변경합니다.

<a name="generating-migrations"></a>
## 마이그레이션 생성하기

`make:migration` [Artisan 명령어](/docs/9.x/artisan)를 이용해 데이터베이스 마이그레이션을 생성할 수 있습니다. 새 마이그레이션 파일은 `database/migrations` 디렉터리에 생성되며, 각 마이그레이션 파일 이름에는 타임스탬프가 포함되어 있어 실행 순서를 Laravel이 결정할 수 있습니다:

```shell
php artisan make:migration create_flights_table
```

Laravel은 마이그레이션 이름을 이용해 해당 마이그레이션이 새 테이블을 생성하는지 여부와 테이블 이름을 추론하려고 시도합니다. 만약 테이블 이름을 찾을 수 있다면, 해당 이름으로 마이그레이션 파일이 사전 작성됩니다. 그렇지 않으면 마이그레이션 파일 내에서 직접 테이블 이름을 지정할 수 있습니다.

생성한 마이그레이션의 경로를 직접 지정하고 싶다면, `make:migration` 명령을 실행할 때 `--path` 옵션을 사용할 수 있습니다. 지정하는 경로는 애플리케이션의 기본 경로를 기준으로 상대 경로여야 합니다.

> [!NOTE]
> 마이그레이션 템플릿(스텁)은 [템플릿 배포](/docs/9.x/artisan#stub-customization)를 이용해 커스터마이징할 수 있습니다.

<a name="squashing-migrations"></a>
### 마이그레이션 스쿼싱

애플리케이션을 개발하며 점점 더 많은 마이그레이션이 쌓일 수 있고, 이로 인해 `database/migrations` 디렉터리가 수백 개의 마이그레이션 파일로 부풀려질 수 있습니다. 이런 경우 마이그레이션을 하나의 SQL 파일로 "스쿼싱"할 수 있습니다. 시작하려면 `schema:dump` 명령을 실행하세요:

```shell
php artisan schema:dump

# 현재 데이터베이스 스키마 덤프와 기존 모든 마이그레이션 정리...
php artisan schema:dump --prune
```

이 명령을 실행하면, Laravel은 애플리케이션의 `database/schema` 디렉터리에 "스키마" 파일을 생성합니다. 스키마 파일의 이름은 데이터베이스 연결 이름에 맞춰집니다. 이후 마이그레이션을 실행하는데, 다른 마이그레이션이 없는 경우 Laravel은 먼저 해당 데이터베이스 연결의 스키마 파일에 포함된 SQL 문을 실행한 후, 스키마 덤프에 포함되지 않은 남은 마이그레이션들을 실행합니다.

만약 테스트가 일반적인 로컬 개발시 사용하는 연결과 다른 데이터베이스 연결을 이용한다면, 테스트 시 사용할 데이터베이스 연결을 기준으로도 스키마 파일을 덤프하는 것이 좋습니다. 예를 들어 로컬 개발용 데이터베이스를 덤프한 후 다음과 같이 실행할 수 있습니다:

```shell
php artisan schema:dump
php artisan schema:dump --database=testing --prune
```

팀의 신규 개발자가 빠르게 애플리케이션 초기 데이터베이스 구조를 만들 수 있도록, 데이터베이스 스키마 파일을 반드시 소스 관리에 커밋해야 합니다.

> [!WARNING]
> 마이그레이션 스쿼싱은 MySQL, PostgreSQL, SQLite 데이터베이스에서만 지원되며 해당 데이터베이스 클라이언트 명령줄 도구를 사용합니다. 스키마 덤프는 메모리 내 SQLite 데이터베이스에는 복원할 수 없습니다.

<a name="migration-structure"></a>
## 마이그레이션 구조

마이그레이션 클래스는 `up`과 `down` 두 메서드로 구성됩니다. `up` 메서드는 데이터베이스에 새로운 테이블, 컬럼, 인덱스를 추가하는 데 사용하고, `down` 메서드는 `up`에서 수행한 작업을 되돌리도록 작성해야 합니다.

이 두 메서드 내에서는 Laravel 스키마 빌더를 사용해 명확하게 테이블을 생성하거나 수정할 수 있습니다. `Schema` 빌더에서 사용할 수 있는 메서드 전체는 [테이블 생성하기](#creating-tables)에서 확인할 수 있습니다. 다음 예시는 `flights` 테이블을 생성하는 마이그레이션입니다:

```
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
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
};
```

<a name="setting-the-migration-connection"></a>
#### 마이그레이션 연결 설정하기

마이그레이션에서 애플리케이션 기본 데이터베이스 연결이 아닌 다른 연결에 작용할 경우, 마이그레이션 클래스의 `$connection` 속성을 설정해야 합니다:

```
/**
 * 이 마이그레이션이 사용할 데이터베이스 연결 이름.
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
## 마이그레이션 실행하기

모든 대기 중인 마이그레이션을 실행하려면 `migrate` Artisan 명령어를 사용하세요:

```shell
php artisan migrate
```

지금까지 어떤 마이그레이션이 실행되었는지 확인하려면 `migrate:status` Artisan 명령어를 사용할 수 있습니다:

```shell
php artisan migrate:status
```

실제 실행하지 않고 어떤 SQL 문이 실행될지 보고 싶다면 `migrate` 명령어에 `--pretend` 플래그를 추가하세요:

```shell
php artisan migrate --pretend
```

#### 마이그레이션 실행 분리

애플리케이션을 여러 서버에 배포하고 마이그레이션을 배포 프로세스의 일부로 실행할 때, 여러 서버가 동시에 데이터베이스 마이그레이션을 실행하는 것을 방지해야 할 수 있습니다. 이 경우 `migrate` 명령어에 `isolated` 옵션을 사용하세요.

`isolated` 옵션이 제공되면 Laravel은 애플리케이션 캐시 드라이버를 사용해 원자적 락을 획득하고 마이그레이션을 실행합니다. 락이 유지되는 동안 다른 모든 마이그레이션 실행 시도는 실행되지 않고, 명령어는 성공 상태 코드로 종료됩니다:

```shell
php artisan migrate --isolated
```

> [!WARNING]
> 이 기능을 사용하려면, 애플리케이션 기본 캐시 드라이버가 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 중 하나여야 하며, 모든 서버가 동일 중앙 캐시 서버와 통신해야 합니다.

<a name="forcing-migrations-to-run-in-production"></a>
#### 프로덕션 환경에서 강제로 마이그레이션 실행하기

일부 마이그레이션 작업은 데이터 손실을 유발하는 위험이 있어, 프로덕션 데이터베이스에서 실행할 때 확인을 요구합니다. 확인 없이 강제로 실행하려면 `--force` 플래그를 사용하세요:

```shell
php artisan migrate --force
```

<a name="rolling-back-migrations"></a>
### 마이그레이션 되돌리기

가장 최근에 실행한 마이그레이션 작업을 되돌리려면 `rollback` Artisan 명령어를 사용합니다. 이 명령어는 마지막으로 실행된 "배치"를 되돌립니다. 배치에는 여러 마이그레이션 파일이 포함될 수 있습니다:

```shell
php artisan migrate:rollback
```

`rollback` 명령어에 `step` 옵션을 주어 되돌릴 마이그레이션 개수를 제한할 수도 있습니다. 예를 들어, 최근 5개의 마이그레이션을 되돌리려면 다음과 같이 실행합니다:

```shell
php artisan migrate:rollback --step=5
```

`migrate:reset` 명령어는 애플리케이션 내 모든 마이그레이션을 되돌립니다:

```shell
php artisan migrate:reset
```

<a name="roll-back-migrate-using-a-single-command"></a>
#### 한 명령어로 되돌리고 다시 실행하기

`migrate:refresh` 명령어는 모든 마이그레이션을 되돌린 후, 다시 `migrate`를 실행합니다. 이 명령은 데이터베이스를 완전히 재구성하는 효과가 있습니다:

```shell
php artisan migrate:refresh

# 데이터베이스를 새로 고치고 모든 시드를 실행...
php artisan migrate:refresh --seed
```

`refresh` 명령어에도 `step` 옵션을 지정해 되돌리고 다시 실행할 마이그레이션 개수를 제한할 수 있습니다. 예를 들어 최근 5개를 되돌리고 다시 실행하려면:

```shell
php artisan migrate:refresh --step=5
```

<a name="drop-all-tables-migrate"></a>
#### 모든 테이블 삭제 후 마이그레이션 실행하기

`migrate:fresh` 명령어는 데이터베이스 내 모든 테이블을 삭제한 후 `migrate` 명령어를 실행합니다:

```shell
php artisan migrate:fresh

php artisan migrate:fresh --seed
```

> [!WARNING]
> `migrate:fresh` 명령어는 테이블의 접두사와 관계없이 모든 테이블을 삭제합니다. 다른 애플리케이션과 공유하는 데이터베이스에서 사용할 때는 주의해야 합니다.

<a name="tables"></a>
## 테이블

<a name="creating-tables"></a>
### 테이블 생성하기

새 데이터베이스 테이블을 생성하려면 `Schema` 파사드의 `create` 메서드를 사용합니다. `create` 메서드는 두 인수를 받고, 첫 번째는 테이블 이름이며 두 번째는 `Blueprint` 객체를 매개변수로 받는 클로저입니다. 클로저 내에서 새 테이블을 정의할 수 있습니다:

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

테이블 생성 시, 스키마 빌더의 [컬럼 메서드](#creating-columns)를 사용해 각 컬럼을 정의할 수 있습니다.

<a name="checking-for-table-column-existence"></a>
#### 테이블 / 컬럼 존재 여부 확인하기

테이블 또는 컬럼의 존재 여부는 `hasTable`과 `hasColumn` 메서드로 확인할 수 있습니다:

```
if (Schema::hasTable('users')) {
    // "users" 테이블이 존재합니다...
}

if (Schema::hasColumn('users', 'email')) {
    // "users" 테이블이 존재하고 "email" 컬럼도 있습니다...
}
```

<a name="database-connection-table-options"></a>
#### 데이터베이스 연결 및 테이블 옵션

애플리케이션 기본 연결이 아닌 다른 데이터베이스 연결에 대해 스키마 작업을 수행하려면 `connection` 메서드를 사용하세요:

```
Schema::connection('sqlite')->create('users', function (Blueprint $table) {
    $table->id();
});
```

또한, MySQL 사용 시 테이블 생성과 관련한 몇 가지 속성과 메서드를 정의할 수 있습니다. 예를 들어, 저장 엔진을 지정하려면 `engine` 속성을 설정합니다:

```
Schema::create('users', function (Blueprint $table) {
    $table->engine = 'InnoDB';

    // ...
});
```

MySQL에서 테이블의 문자셋과 콜레이션을 지정하려면 아래와 같이 설정합니다:

```
Schema::create('users', function (Blueprint $table) {
    $table->charset = 'utf8mb4';
    $table->collation = 'utf8mb4_unicode_ci';

    // ...
});
```

테이블을 "임시(temporary)" 테이블로 만들고 싶다면 `temporary` 메서드를 호출하세요. 임시 테이블은 현재 데이터베이스 세션에만 보이며, 연결 종료 시 자동으로 삭제됩니다:

```
Schema::create('calculations', function (Blueprint $table) {
    $table->temporary();

    // ...
});
```

테이블에 "코멘트"를 추가하려면 테이블 인스턴스에서 `comment` 메서드를 호출할 수 있습니다. 이 기능은 현재 MySQL과 Postgres에서만 지원됩니다:

```
Schema::create('calculations', function (Blueprint $table) {
    $table->comment('Business calculations');

    // ...
});
```

<a name="updating-tables"></a>
### 테이블 수정하기

기존 테이블을 수정하려면 `Schema` 파사드의 `table` 메서드를 사용합니다. `create` 메서드와 유사하게 첫 번째 인수는 테이블 이름, 두 번째 인수는 `Blueprint` 인스턴스를 매개변수로 받는 클로저입니다. 이 클로저 내에서 컬럼이나 인덱스를 추가할 수 있습니다:

```
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->integer('votes');
});
```

<a name="renaming-and-dropping-tables"></a>
### 테이블 이름 변경 및 삭제

테이블 이름을 변경하려면 `rename` 메서드를 사용하세요:

```
use Illuminate\Support\Facades\Schema;

Schema::rename($from, $to);
```

기존 테이블을 삭제하려면 `drop` 또는 `dropIfExists` 메서드를 사용할 수 있습니다:

```
Schema::drop('users');

Schema::dropIfExists('users');
```

<a name="renaming-tables-with-foreign-keys"></a>
#### 외래 키가 있는 테이블 이름 변경하기

테이블 이름을 변경하기 전에, 해당 테이블의 외래 키 제약조건이 Laravel이 자동으로 이름을 붙이지 않고 명시적으로 이름이 지정되었는지 확인해야 합니다. 그렇지 않으면 외래 키 제약조건 이름이 이전 테이블 이름을 참조하게 됩니다.

<a name="columns"></a>
## 컬럼

<a name="creating-columns"></a>
### 컬럼 생성하기

`Schema` 파사드의 `table` 메서드를 이용하면 기존 테이블에 컬럼을 추가할 수 있습니다. `create` 메서드와 마찬가지로 첫 번째 인수는 테이블 이름, 두 번째 인수는 `Illuminate\Database\Schema\Blueprint` 인스턴스를 받는 클로저입니다. 클로저 내에서 컬럼을 정의할 수 있습니다:

```
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->integer('votes');
});
```

<a name="available-column-types"></a>
### 사용 가능한 컬럼 타입

스키마 빌더의 `Blueprint` 클래스는 데이터베이스 테이블에 추가할 수 있는 다양한 타입의 컬럼을 제공하는 메서드를 갖고 있습니다. 사용 가능한 메서드는 아래 목록과 같으며, 각 항목별 자세한 설명은 아래에서 확인할 수 있습니다.


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

<a name="column-method-bigIncrements"></a>
#### `bigIncrements()`

`bigIncrements` 메서드는 자동 증가하는 `UNSIGNED BIGINT` (기본키) 타입 컬럼을 생성합니다:

```
$table->bigIncrements('id');
```

<a name="column-method-bigInteger"></a>
#### `bigInteger()`

`bigInteger` 메서드는 `BIGINT` 타입 컬럼을 생성합니다:

```
$table->bigInteger('votes');
```

<a name="column-method-binary"></a>
#### `binary()`

`binary` 메서드는 `BLOB` 타입 컬럼을 생성합니다:

```
$table->binary('photo');
```

<a name="column-method-boolean"></a>
#### `boolean()`

`boolean` 메서드는 `BOOLEAN` 타입 컬럼을 생성합니다:

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

`dateTimeTz` 메서드는 선택적 정밀도(전체 자릿수)를 갖는 `DATETIME` 타입(타임존 포함) 컬럼을 생성합니다:

```
$table->dateTimeTz('created_at', $precision = 0);
```

<a name="column-method-dateTime"></a>
#### `dateTime()`

`dateTime` 메서드는 선택적 정밀도(전체 자릿수)를 갖는 `DATETIME` 타입 컬럼을 생성합니다:

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

`decimal` 메서드는 지정한 정밀도(전체 자릿수)와 소수점 자릿수를 갖는 `DECIMAL` 타입 컬럼을 생성합니다:

```
$table->decimal('amount', $precision = 8, $scale = 2);
```

<a name="column-method-double"></a>
#### `double()`

`double` 메서드는 지정한 정밀도와 소수점 자릿수를 갖는 `DOUBLE` 타입 컬럼을 생성합니다:

```
$table->double('amount', 8, 2);
```

<a name="column-method-enum"></a>
#### `enum()`

`enum` 메서드는 주어진 단일 값의 목록을 갖는 `ENUM` 타입 컬럼을 생성합니다:

```
$table->enum('difficulty', ['easy', 'hard']);
```

<a name="column-method-float"></a>
#### `float()`

`float` 메서드는 지정한 정밀도와 소수점 자릿수를 갖는 `FLOAT` 타입 컬럼을 생성합니다:

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

`foreignIdFor` 메서드는 지정한 모델 클래스에 해당하는 `{column}_id` 명명 규칙을 가진 `UNSIGNED BIGINT` 컬럼을 생성합니다:

```
$table->foreignIdFor(User::class);
```

<a name="column-method-foreignUlid"></a>
#### `foreignUlid()`

`foreignUlid` 메서드는 `ULID` 타입 컬럼을 생성합니다:

```
$table->foreignUlid('user_id');
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

`id` 메서드는 `bigIncrements` 메서드의 별칭입니다. 기본적으로 `id` 컬럼을 생성하나, 다른 이름을 지정할 수도 있습니다:

```
$table->id();
```

<a name="column-method-increments"></a>
#### `increments()`

`increments` 메서드는 자동 증가하는 `UNSIGNED INTEGER` 타입 기본 키 컬럼을 생성합니다:

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

`ipAddress` 메서드는 `VARCHAR` 타입 컬럼을 생성하며 IP 주소를 저장하는 용도입니다:

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

`macAddress` 메서드는 MAC 주소를 저장하기 위한 컬럼을 생성합니다. 일부 DB 시스템(PostgreSQL 등)은 전용 타입을 사용, 그 외는 문자열 타입을 사용합니다:

```
$table->macAddress('device');
```

<a name="column-method-mediumIncrements"></a>
#### `mediumIncrements()`

`mediumIncrements` 메서드는 자동 증가하는 `UNSIGNED MEDIUMINT` 타입 기본 키 컬럼을 생성합니다:

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

`morphs` 메서드는 `{column}_id` (`UNSIGNED BIGINT`)와 `{column}_type` (`VARCHAR`) 컬럼을 함께 추가하는 편의 메서드입니다.

이는 다형성(polymorphic) [Eloquent 연관관계](/docs/9.x/eloquent-relationships) 정의 시 사용됩니다. 예를 들어 다음 코드는 `taggable_id`와 `taggable_type` 컬럼을 생성합니다:

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

`morphs` 메서드와 유사하지만, 생성하는 컬럼들이 NULL을 허용합니다:

```
$table->nullableMorphs('taggable');
```

<a name="column-method-nullableUlidMorphs"></a>
#### `nullableUlidMorphs()`

`ulidMorphs` 메서드와 비슷하지만 생성되는 컬럼들이 NULL을 허용합니다:

```
$table->nullableUlidMorphs('taggable');
```

<a name="column-method-nullableUuidMorphs"></a>
#### `nullableUuidMorphs()`

`uuidMorphs` 메서드와 비슷하지만 생성되는 컬럼들이 NULL 허용입니다:

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

`rememberToken` 메서드는 nullable한 `VARCHAR(100)` 타입 컬럼을 생성하며, 로그인 유지 "remember me" 인증 토큰 저장 용도입니다:

```
$table->rememberToken();
```

<a name="column-method-set"></a>
#### `set()`

`set` 메서드는 주어진 유효 값 목록으로 `SET` 타입 컬럼을 생성합니다:

```
$table->set('flavors', ['strawberry', 'vanilla']);
```

<a name="column-method-smallIncrements"></a>
#### `smallIncrements()`

`smallIncrements` 메서드는 자동 증가하는 `UNSIGNED SMALLINT` 기본 키 컬럼을 생성합니다:

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

`softDeletesTz` 메서드는 nullable한 `deleted_at` `TIMESTAMP` (타임존 포함) 타입 컬럼을 생성하며, Eloquent의 "soft delete" 기능에서 사용됩니다:

```
$table->softDeletesTz($column = 'deleted_at', $precision = 0);
```

<a name="column-method-softDeletes"></a>
#### `softDeletes()`

`softDeletes` 메서드는 nullable한 `deleted_at` `TIMESTAMP` 타입 컬럼을 생성하며, Eloquent "soft delete" 기능에서 사용됩니다:

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

`timeTz` 메서드는 선택적 정밀도를 갖는 `TIME` 타입(타임존 포함) 컬럼을 생성합니다:

```
$table->timeTz('sunrise', $precision = 0);
```

<a name="column-method-time"></a>
#### `time()`

`time` 메서드는 선택적 정밀도를 가진 `TIME` 타입 컬럼을 생성합니다:

```
$table->time('sunrise', $precision = 0);
```

<a name="column-method-timestampTz"></a>
#### `timestampTz()`

`timestampTz` 메서드는 선택적 정밀도를 가진 `TIMESTAMP` 타입(타임존 포함) 컬럼을 생성합니다:

```
$table->timestampTz('added_at', $precision = 0);
```

<a name="column-method-timestamp"></a>
#### `timestamp()`

`timestamp` 메서드는 선택적 정밀도를 가진 `TIMESTAMP` 타입 컬럼을 생성합니다:

```
$table->timestamp('added_at', $precision = 0);
```

<a name="column-method-timestampsTz"></a>
#### `timestampsTz()`

`timestampsTz` 메서드는 선택적 정밀도를 가진 `created_at` 및 `updated_at` `TIMESTAMP` 타입(타임존 포함) 컬럼을 생성합니다:

```
$table->timestampsTz($precision = 0);
```

<a name="column-method-timestamps"></a>
#### `timestamps()`

`timestamps` 메서드는 선택적 정밀도를 가진 `created_at` 및 `updated_at` `TIMESTAMP` 컬럼을 생성합니다:

```
$table->timestamps($precision = 0);
```

<a name="column-method-tinyIncrements"></a>
#### `tinyIncrements()`

`tinyIncrements` 메서드는 자동 증가하는 `UNSIGNED TINYINT` 타입 기본 키 컬럼을 생성합니다:

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

`unsignedDecimal` 메서드는 선택적 정밀도와 소수점 자릿수를 가진 `UNSIGNED DECIMAL` 타입 컬럼을 생성합니다:

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

<a name="column-method-ulidMorphs"></a>
#### `ulidMorphs()`

`ulidMorphs` 메서드는 `{column}_id` (`CHAR(26)`)와 `{column}_type` (`VARCHAR`) 컬럼을 함께 추가하는 편의 메서드입니다.

이는 ULID 식별자를 사용하는 다형성 [Eloquent 연관관계](/docs/9.x/eloquent-relationships) 정의 시 사용됩니다. 예를 들어 `taggable_id`와 `taggable_type` 컬럼을 생성합니다:

```
$table->ulidMorphs('taggable');
```

<a name="column-method-uuidMorphs"></a>
#### `uuidMorphs()`

`uuidMorphs` 메서드는 `{column}_id` (`CHAR(36)`)와 `{column}_type` (`VARCHAR`) 컬럼을 함께 추가하는 편의 메서드입니다.

이는 UUID 식별자를 사용하는 다형성 [Eloquent 연관관계](/docs/9.x/eloquent-relationships) 정의 시 사용됩니다. 예를 들어 `taggable_id`와 `taggable_type` 컬럼을 생성합니다:

```
$table->uuidMorphs('taggable');
```

<a name="column-method-ulid"></a>
#### `ulid()`

`ulid` 메서드는 `ULID` 타입 컬럼을 생성합니다:

```
$table->ulid('id');
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
### 컬럼 수정자

위 컬럼 타입 외에도 컬럼 추가 시 여러 "수정자"를 함께 사용할 수 있습니다. 예를 들어 컬럼을 NULL 허용으로 만들고 싶다면 `nullable` 메서드를 사용하세요:

```
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->string('email')->nullable();
});
```

아래 표는 사용 가능한 컬럼 수정자의 목록입니다. [인덱스 수정자](#creating-indexes)는 포함하지 않습니다:

Modifier  |  설명
--------  |  -----------
`->after('column')`  |  지정한 컬럼 뒤에 새 컬럼을 배치 (MySQL 전용).
`->autoIncrement()`  |  INTEGER 컬럼을 자동 증가(primary key)로 설정.
`->charset('utf8mb4')`  |  컬럼 문자셋 지정 (MySQL 전용).
`->collation('utf8mb4_unicode_ci')`  |  컬럼 콜레이션 지정 (MySQL/PostgreSQL/SQL Server).
`->comment('my comment')`  |  컬럼 코멘트 추가 (MySQL/PostgreSQL).
`->default($value)`  |  컬럼 기본값 지정.
`->first()`  |  컬럼을 테이블 첫 번째 위치에 배치 (MySQL).
`->from($integer)`  |  자동 증가 필드 시작 값 설정 (MySQL/PostgreSQL).
`->invisible()`  |  컬럼을 `SELECT *` 쿼리에서 보이지 않게 설정 (MySQL).
`->nullable($value = true)`  |  NULL 값 허용.
`->storedAs($expression)`  |  저장된 생성 컬럼 생성 (MySQL/PostgreSQL).
`->unsigned()`  |  INTEGER 컬럼을 UNSIGNED로 설정 (MySQL).
`->useCurrent()`  |  TIMESTAMP 컬럼의 기본값을 CURRENT_TIMESTAMP로 설정.
`->useCurrentOnUpdate()`  |  레코드 업데이트 시 TIMESTAMP를 CURRENT_TIMESTAMP로 설정.
`->virtualAs($expression)`  |  가상 생성 컬럼 생성 (MySQL/PostgreSQL/SQLite).
`->generatedAs($expression)`  |  특정 시퀀스 옵션과 함께 식별자 컬럼 생성 (PostgreSQL).
`->always()`  |  Postgres의 identity 컬럼 시퀀스 입력 우선권 설정.
`->isGeometry()`  |  공간 데이터 컬럼 타입을 `geometry`로 설정 (기본은 `geography`) (PostgreSQL).

<a name="default-expressions"></a>
#### 기본값 표현식

`default` 수정자는 값 또는 `Illuminate\Database\Query\Expression` 인스턴스를 받을 수 있습니다. Expression 인스턴스를 사용하면 Laravel이 값에 따옴표를 붙이지 않으며, DB별 함수 등을 사용할 수 있습니다. 특히 JSON 컬럼에 기본값을 지정하는 데 유용합니다:

```
<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Query\Expression;
use Illuminate\Database\Migrations\Migration;

return new class extends Migration
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
};
```

> [!WARNING]
> 기본값 표현식 지원 여부는 데이터베이스 드라이버, 버전, 컬럼 타입에 따라 다릅니다. 각 데이터베이스 문서를 꼭 참조하세요. 또한, `change` 메서드를 통한 컬럼 변경 시 raw `default` 표현식(`DB::raw`)과 함께 사용할 수 없습니다.

<a name="column-order"></a>
#### 컬럼 순서 지정

MySQL 데이터베이스 사용 시, `after` 메서드를 이용해 새 컬럼을 기존 컬럼 뒤에 추가할 수 있습니다:

```
$table->after('password', function ($table) {
    $table->string('address_line1');
    $table->string('address_line2');
    $table->string('city');
});
```

<a name="modifying-columns"></a>
### 컬럼 수정하기

<a name="prerequisites"></a>
#### 사전 준비

컬럼을 수정하려면 먼저 Composer를 통해 `doctrine/dbal` 패키지를 설치해야 합니다. 이 라이브러리는 컬럼 현재 상태를 파악하고, 변경하는 데 필요한 SQL 쿼리를 생성하는 데 사용됩니다:

```
composer require doctrine/dbal
```

`timestamp` 메서드로 생성한 컬럼을 수정할 경우, 애플리케이션의 `config/database.php` 설정 파일에 다음 구성을 추가해야 합니다:

```php
use Illuminate\Database\DBAL\TimestampType;

'dbal' => [
    'types' => [
        'timestamp' => TimestampType::class,
    ],
],
```

> [!WARNING]
> Microsoft SQL Server 사용 시 `doctrine/dbal:^3.0` 버전을 설치해야 합니다.

<a name="updating-column-attributes"></a>
#### 컬럼 속성 수정

`change` 메서드를 사용하면 기존 컬럼의 타입과 속성을 수정할 수 있습니다. 예를 들어 `name` 컬럼의 길이를 25에서 50으로 늘리고 싶다면, 새 상태로 정의 후 `change`를 호출하면 됩니다:

```
Schema::table('users', function (Blueprint $table) {
    $table->string('name', 50)->change();
});
```

컬럼을 nullable로 수정할 수도 있습니다:

```
Schema::table('users', function (Blueprint $table) {
    $table->string('name', 50)->nullable()->change();
});
```

> [!WARNING]
> 다음 컬럼 타입만 수정할 수 있습니다: `bigInteger`, `binary`, `boolean`, `char`, `date`, `dateTime`, `dateTimeTz`, `decimal`, `double`, `integer`, `json`, `longText`, `mediumText`, `smallInteger`, `string`, `text`, `time`, `tinyText`, `unsignedBigInteger`, `unsignedInteger`, `unsignedSmallInteger`, `uuid`.  `timestamp` 컬럼을 수정하려면 [Doctrine 타입 등록](#prerequisites)이 필요합니다.

<a name="renaming-columns"></a>
### 컬럼 이름 변경하기

컬럼 이름을 변경하려면 스키마 빌더가 제공하는 `renameColumn` 메서드를 사용하세요:

```
Schema::table('users', function (Blueprint $table) {
    $table->renameColumn('from', 'to');
});
```

<a name="renaming-columns-on-legacy-databases"></a>
#### 구버전 데이터베이스에서 컬럼 이름 변경하기

다음 버전보다 낮은 데이터베이스에서 실행 중이라면, 컬럼 이름 변경 전에 반드시 `doctrine/dbal` 라이브러리를 Composer로 설치해야 합니다:

- MySQL < `8.0.3`
- MariaDB < `10.5.2`
- SQLite < `3.25.0`

<a name="dropping-columns"></a>
### 컬럼 삭제하기

컬럼을 삭제하려면 스키마 빌더의 `dropColumn` 메서드를 사용하세요:

```
Schema::table('users', function (Blueprint $table) {
    $table->dropColumn('votes');
});
```

여러 컬럼을 삭제할 때는 컬럼명 배열을 전달할 수 있습니다:

```
Schema::table('users', function (Blueprint $table) {
    $table->dropColumn(['votes', 'avatar', 'location']);
});
```

<a name="dropping-columns-on-legacy-databases"></a>
#### 구버전 데이터베이스에서 컬럼 삭제하기

SQLite 버전이 `3.35.0` 미만인 경우 컬럼 삭제 전에 `doctrine/dbal` 패키지를 설치해야 합니다. 또한 이 패키지를 사용할 때 한 번에 여러 컬럼을 삭제 또는 수정하는 것은 지원되지 않습니다.

<a name="available-command-aliases"></a>
#### 삭제 관련 명령어 별칭

Laravel은 자주 사용하는 컬럼 삭제에 편리한 몇 가지 메서드를 제공합니다:

명령어  |  설명
-------  |  -----------
`$table->dropMorphs('morphable');`  |  `morphable_id`와 `morphable_type` 컬럼 삭제.
`$table->dropRememberToken();`  |  `remember_token` 컬럼 삭제.
`$table->dropSoftDeletes();`  |  `deleted_at` 컬럼 삭제.
`$table->dropSoftDeletesTz();`  |  `dropSoftDeletes()` 별칭.
`$table->dropTimestamps();`  |  `created_at`과 `updated_at` 컬럼 삭제.
`$table->dropTimestampsTz();` |  `dropTimestamps()` 별칭.

<a name="indexes"></a>
## 인덱스

<a name="creating-indexes"></a>
### 인덱스 생성하기

Laravel 스키마 빌더는 여러 종류의 인덱스를 지원합니다. 예를 들어, `email` 컬럼에 고유(unique) 인덱스를 추가하려면 컬럼 정의에 `unique` 메서드를 체이닝할 수 있습니다:

```
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->string('email')->unique();
});
```

또는 컬럼을 정의한 후, `unique` 메서드를 스키마 빌더에서 호출해도 됩니다. 이 경우 고유 인덱스를 적용할 컬럼명을 전달합니다:

```
$table->unique('email');
```

복합 인덱스를 생성할 때는 컬럼명 배열을 전달할 수 있습니다:

```
$table->index(['account_id', 'created_at']);
```

인덱스 생성 시 Laravel은 기본적으로 테이블명, 컬럼명, 인덱스 타입을 기반으로 이름을 자동 생성하지만, 두 번째 인수로 인덱스 이름을 직접 지정할 수도 있습니다:

```
$table->unique('email', 'unique_email');
```

<a name="available-index-types"></a>
#### 사용 가능한 인덱스 타입

Laravel 스키마 빌더는 지원하는 인덱스 타입별로 메서드를 제공합니다. 모든 메서드는 선택적으로 두 번째 인수로 인덱스 이름을 지정할 수 있으며, 미지정 시 테이블, 컬럼, 타입 정보를 기반으로 자동 결정됩니다. 각각의 메서드는 아래와 같습니다:

명령어  |  설명
-------  |  -----------
`$table->primary('id');`  |  기본 키(primary key) 설정.
`$table->primary(['id', 'parent_id']);`  |  복합 기본 키 설정.
`$table->unique('email');`  |  유니크 인덱스 설정.
`$table->index('state');`  |  기본 일반 인덱스 설정.
`$table->fullText('body');`  |  전문 검색 인덱스 설정 (MySQL/PostgreSQL).
`$table->fullText('body')->language('english');`  |  지정한 언어 전문 검색 인덱스 설정 (PostgreSQL).
`$table->spatialIndex('location');`  |  공간 인덱스 설정 (SQLite 제외).

<a name="index-lengths-mysql-mariadb"></a>
#### 인덱스 길이 및 MySQL / MariaDB

기본적으로 Laravel은 `utf8mb4` 문자셋을 사용합니다. MySQL 5.7.7 이전 버전 또는 MariaDB 10.2.2 이전 버전에서는, MySQL이 해당 컬럼에 인덱스를 생성할 수 있도록 기본 문자열 길이를 명시적으로 설정해야 합니다. 이 설정은 `App\Providers\AppServiceProvider` 클래스 내 `boot` 메서드에서 `Schema::defaultStringLength` 메서드를 호출해 지정할 수 있습니다:

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

또한, 데이터베이스 설정에서 `innodb_large_prefix` 옵션을 활성화하는 방법도 있습니다. 자세한 내용은 각 데이터베이스 문서를 참고하세요.

<a name="renaming-indexes"></a>
### 인덱스 이름 변경하기

인덱스 이름을 변경하려면 스키마 빌더의 `renameIndex` 메서드를 사용합니다. 첫 번째 인수로 기존 인덱스 이름, 두 번째 인수로 새로운 인덱스 이름을 지정합니다:

```
$table->renameIndex('from', 'to')
```

> [!WARNING]
> SQLite를 사용하는 경우 `renameIndex` 메서드를 사용하려면 Composer로 `doctrine/dbal` 패키지를 설치해야 합니다.

<a name="dropping-indexes"></a>
### 인덱스 삭제하기

인덱스를 삭제하려면 인덱스 이름을 지정해야 합니다. Laravel은 기본적으로 테이블명, 컬럼명, 인덱스 타입을 기반으로 인덱스 이름을 자동 생성합니다. 예시는 아래와 같습니다:

명령어  |  설명
-------  |  -----------
`$table->dropPrimary('users_id_primary');`  |  "users" 테이블의 기본 키 삭제.
`$table->dropUnique('users_email_unique');`  |  "users" 테이블의 유니크 인덱스 삭제.
`$table->dropIndex('geo_state_index');`  |  "geo" 테이블의 일반 인덱스 삭제.
`$table->dropFullText('posts_body_fulltext');`  |  "posts" 테이블의 전문 검색 인덱스 삭제.
`$table->dropSpatialIndex('geo_location_spatialindex');`  |  "geo" 테이블의 공간 인덱스 삭제 (SQLite 제외).

컬럼명 배열을 전달할 경우, 컬럼명과 테이블명, 인덱스 타입을 기반으로 인덱스 이름이 자동 생성됩니다:

```
Schema::table('geo', function (Blueprint $table) {
    $table->dropIndex(['state']); // 'geo_state_index' 인덱스 삭제
});
```

<a name="foreign-key-constraints"></a>
### 외래 키 제약조건

외래 키 제약조건은 데이터베이스 차원에서 참조 무결성을 강제하는 데 사용됩니다. 예를 들어 `posts` 테이블에 `user_id` 컬럼을 추가하고 `users` 테이블의 `id` 컬럼을 참조하도록 정의할 수 있습니다:

```
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('posts', function (Blueprint $table) {
    $table->unsignedBigInteger('user_id');

    $table->foreign('user_id')->references('id')->on('users');
});
```

위 문법이 다소 장황하기 때문에, Laravel은 관례 기반 더 간결한 메서드를 제공합니다. `foreignId` 메서드를 사용하면 다음과 같이 변경할 수 있습니다:

```
Schema::table('posts', function (Blueprint $table) {
    $table->foreignId('user_id')->constrained();
});
```

`foreignId` 메서드는 `UNSIGNED BIGINT` 타입 컬럼을 생성하고, `constrained` 메서드는 참조 테이블과 컬럼명을 관례에 따라 설정합니다. 만약 테이블명이 관례와 다르다면 `constrained` 메서드에 테이블명을 인수로 넘길 수 있습니다:

```
Schema::table('posts', function (Blueprint $table) {
    $table->foreignId('user_id')->constrained('users');
});
```

또한 제약조건의 "on delete", "on update" 동작을 다음과 같이 지정할 수 있습니다:

```
$table->foreignId('user_id')
      ->constrained()
      ->onUpdate('cascade')
      ->onDelete('cascade');
```

이 동작을 표현하는 명시적 메서드도 제공합니다:

메서드  |  설명
-------  |  -----------
`$table->cascadeOnUpdate();` | 업데이트 시 연쇄 적용.
`$table->restrictOnUpdate();`| 업데이트 제한.
`$table->cascadeOnDelete();` | 삭제 시 연쇄 적용.
`$table->restrictOnDelete();`| 삭제 제한.
`$table->nullOnDelete();`    | 삭제 시 외래 키 값을 NULL로 설정.

추가로 [컬럼 수정자](#column-modifiers)는 `constrained` 호출 이전에 작성해야 합니다:

```
$table->foreignId('user_id')
      ->nullable()
      ->constrained();
```

<a name="dropping-foreign-keys"></a>
#### 외래 키 삭제하기

외래 키 제약조건을 삭제하려면 `dropForeign` 메서드에 제약조건 이름을 지정합니다. 외래 키 제약조건 이름은 인덱스 이름과 같은 명명 규칙을 따르며, 테이블명, 컬럼명, 그리고 `_foreign` 접미사를 사용합니다:

```
$table->dropForeign('posts_user_id_foreign');
```

또는 외래 키를 가진 컬럼명 배열을 전달하면, Laravel이 규칙에 따라 제약조건 이름을 생성합니다:

```
$table->dropForeign(['user_id']);
```

<a name="toggling-foreign-key-constraints"></a>
#### 외래 키 제약조건 활성화 / 비활성화

마이그레이션 내에서 외래 키 제약조건을 활성화하거나 비활성화할 수 있는 메서드입니다:

```
Schema::enableForeignKeyConstraints();

Schema::disableForeignKeyConstraints();

Schema::withoutForeignKeyConstraints(function () {
    // 이 클로저 안에서는 제약조건 비활성화 상태입니다...
});
```

> [!WARNING]
> SQLite는 기본적으로 외래 키 제약조건이 비활성화되어 있습니다. SQLite를 사용하는 경우 [데이터베이스 설정](/docs/9.x/database#configuration)에서 외래 키 지원을 활성화해야 하며, SQLite는 테이블 생성 시에만 외래 키를 지원하고, 테이블 변경 시에는 지원하지 않습니다(https://www.sqlite.org/omitted.html).

<a name="events"></a>
## 이벤트

편의를 위해, 각 마이그레이션 작업은 [이벤트](/docs/9.x/events)를 발생시킵니다. 아래 모든 이벤트는 기본 클래스 `Illuminate\Database\Events\MigrationEvent`를 상속합니다:

 클래스 | 설명
-------|-------
`Illuminate\Database\Events\MigrationsStarted` | 마이그레이션 배치 실행 직전 이벤트.
`Illuminate\Database\Events\MigrationsEnded` | 마이그레이션 배치 실행 완료 이벤트.
`Illuminate\Database\Events\MigrationStarted` | 단일 마이그레이션 실행 직전 이벤트.
`Illuminate\Database\Events\MigrationEnded` | 단일 마이그레이션 실행 완료 이벤트.
`Illuminate\Database\Events\SchemaDumped` | 데이터베이스 스키마 덤프 완료 이벤트.
`Illuminate\Database\Events\SchemaLoaded` | 기존 데이터베이스 스키마 덤프 로드 이벤트.