# 데이터베이스: 마이그레이션 (Database: Migrations)

- [소개](#introduction)
- [마이그레이션 생성](#generating-migrations)
    - [마이그레이션 스쿼싱](#squashing-migrations)
- [마이그레이션 구조](#migration-structure)
- [마이그레이션 실행](#running-migrations)
    - [마이그레이션 롤백](#rolling-back-migrations)
- [테이블](#tables)
    - [테이블 생성](#creating-tables)
    - [테이블 업데이트](#updating-tables)
    - [테이블 이름 변경/삭제](#renaming-and-dropping-tables)
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
    - [외래 키 제약조건](#foreign-key-constraints)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

마이그레이션은 데이터베이스에 대한 버전 관리 시스템과 같아서, 팀이 애플리케이션의 데이터베이스 스키마 정의를 함께 만들고 공유할 수 있도록 합니다. 만약 소스 제어에서 변경 사항을 가져온 후 동료에게 로컬 데이터베이스 스키마에 직접 컬럼을 추가하도록 부탁한 적이 있다면, 마이그레이션이 해결하는 문제를 경험한 것입니다.

Laravel의 `Schema` [파사드](/docs/master/facades)는 Laravel에서 지원하는 모든 데이터베이스 시스템에 대해 데이터베이스에 독립적인 테이블 생성 및 조작 기능을 제공합니다. 보통 마이그레이션은 이 파사드를 사용해 데이터베이스 테이블과 컬럼을 생성 및 수정합니다.

<a name="generating-migrations"></a>
## 마이그레이션 생성 (Generating Migrations)

`make:migration` [Artisan 명령어](/docs/master/artisan)를 사용하여 데이터베이스 마이그레이션 파일을 생성할 수 있습니다. 새 마이그레이션은 `database/migrations` 디렉터리에 생성됩니다. 각 마이그레이션 파일명에는 타임스탬프가 포함되어 있어서 Laravel이 마이그레이션 실행 순서를 결정할 수 있습니다:

```shell
php artisan make:migration create_flights_table
```

Laravel은 마이그레이션 이름으로부터 테이블 이름과 새 테이블 생성 여부를 추측합니다. 이름에서 테이블을 유추할 수 있다면, Laravel은 생성된 마이그레이션 파일에 해당 테이블 이름을 미리 채워 넣습니다. 그렇지 않으면 마이그레이션 파일 내에서 직접 테이블을 지정할 수 있습니다.

마이그레이션 파일의 경로를 직접 지정하고 싶다면, `make:migration` 실행 시 `--path` 옵션을 사용할 수 있습니다. 지정하는 경로는 애플리케이션의 베이스 경로 기준으로 상대 경로여야 합니다.

> [!NOTE]
> 마이그레이션 스텁은 [스텁 게시](/docs/master/artisan#stub-customization)를 통해 커스터마이징할 수 있습니다.

<a name="squashing-migrations"></a>
### 마이그레이션 스쿼싱 (Squashing Migrations)

애플리케이션이 커질수록 수많은 마이그레이션이 누적되어 `database/migrations` 디렉터리가 수백 개의 마이그레이션 파일로 부풀어 오를 수 있습니다. 이럴 때 마이그레이션들을 단일 SQL 파일로 "스쿼싱"하여 합칠 수 있습니다. 시작하려면 `schema:dump` 명령어를 실행하세요:

```shell
php artisan schema:dump

# 현재 데이터베이스 스키마를 덤프하고 기존 모든 마이그레이션을 정리...
php artisan schema:dump --prune
```

이 명령을 실행하면 Laravel은 애플리케이션의 `database/schema` 디렉터리에 "스키마" 파일을 작성합니다. 스키마 파일명은 데이터베이스 연결 이름과 일치합니다. 이후 데이터베이스 마이그레이션 시 다른 마이그레이션이 이미 실행된 것이 없다면, 먼저 해당 데이터베이스 연결의 스키마 파일에 있는 SQL 문을 실행합니다. 스키마 파일 실행 후에는, 스키마 덤프에 포함되지 않은 나머지 마이그레이션이 실행됩니다.

만약 애플리케이션의 테스트에서 일반 로컬 개발과 다른 데이터베이스 연결을 사용한다면, 테스트용 데이터베이스 연결에 대해서도 스키마 파일을 덤프해 두어 테스트 시 데이터베이스를 구축할 수 있도록 해야 합니다. 보통 로컬 개발용 데이터베이스 덤프 후에 다음과 같이 실행할 수 있습니다:

```shell
php artisan schema:dump
php artisan schema:dump --database=testing --prune
```

이렇게 생성한 데이터베이스 스키마 파일은 다른 신규 개발자가 애플리케이션의 초기 데이터베이스 구조를 빠르게 만들도록 소스 제어에 커밋해야 합니다.

> [!WARNING]
> 마이그레이션 스쿼싱은 MariaDB, MySQL, PostgreSQL, SQLite 데이터베이스에서만 지원하며, 데이터베이스의 커맨드라인 클라이언트를 사용합니다.

<a name="migration-structure"></a>
## 마이그레이션 구조 (Migration Structure)

마이그레이션 클래스는 두 가지 메서드를 가집니다: `up`과 `down`. `up` 메서드는 테이블, 컬럼, 인덱스를 새로 추가하는 작업을 담당하고, `down` 메서드는 `up`이 수행한 작업을 되돌리는 작업을 수행해야 합니다.

두 메서드 안에서 Laravel의 스키마 빌더를 사용해 테이블을 표현식처럼 만들고 변경할 수 있습니다. `Schema` 빌더에서 사용할 수 있는 모든 메서드에 관해서는 [테이블 생성](#creating-tables) 문서를 참고하세요. 예를 들어, 다음 마이그레이션은 `flights` 테이블을 생성합니다:

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
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
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::drop('flights');
    }
};
```

<a name="setting-the-migration-connection"></a>
#### 마이그레이션 연결 설정

기본 데이터베이스 연결이 아닌 다른 데이터베이스 연결을 마이그레이션에서 사용하려면, 마이그레이션 클래스 내에서 `$connection` 속성을 설정하세요:

```php
/**
 * 마이그레이션에서 사용할 데이터베이스 연결 이름.
 *
 * @var string
 */
protected $connection = 'pgsql';

/**
 * Run the migrations.
 */
public function up(): void
{
    // ...
}
```

<a name="running-migrations"></a>
## 마이그레이션 실행 (Running Migrations)

대기 중인 모든 마이그레이션을 실행하려면, `migrate` Artisan 명령어를 사용하세요:

```shell
php artisan migrate
```

이미 실행된 마이그레이션 목록을 보고 싶으면 `migrate:status` 명령을 사용합니다:

```shell
php artisan migrate:status
```

실제로 실행하지 않고 어떤 SQL 문들이 실행될지 확인하고 싶으면 `--pretend` 플래그를 사용하세요:

```shell
php artisan migrate --pretend
```

#### 마이그레이션 실행 격리

서버가 여러 대일 때 배포 과정에서 동시에 두 서버가 마이그레이션을 실행하지 않도록 하려면, `migrate` 명령 실행 시 `--isolated` 옵션을 사용하세요.

이 옵션이 제공되면, Laravel은 애플리케이션의 캐시 드라이버를 사용해 원자적 락(atomic lock)을 획득한 뒤 마이그레이션을 실행합니다. 락이 걸려 있는 동안 다른 실행 시도는 실제 마이그레이션을 하지 않고 성공적으로 종료하지만, 실행 자체는 하지 않습니다:

```shell
php artisan migrate --isolated
```

> [!WARNING]
> 이 기능을 사용하려면, 애플리케이션 기본 캐시 드라이버로 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 중 하나를 사용해야 하며, 여러 서버가 동일한 중앙 캐시 서버를 사용해 통신해야 합니다.

<a name="forcing-migrations-to-run-in-production"></a>
#### 프로덕션 환경에서 강제로 마이그레이션 실행

파괴적인(most destructive) 마이그레이션 작업은 프로덕션 데이터 손실 위험이 있으므로 실행 전 확인을 요구합니다. 프롬프트 없이 실행하려면 `--force` 플래그를 사용하세요:

```shell
php artisan migrate --force
```

<a name="rolling-back-migrations"></a>
### 마이그레이션 롤백 (Rolling Back Migrations)

가장 최근 마이그레이션 배치를 롤백하려면 `rollback` Artisan 명령을 사용하세요. 이 명령은 하나의 "배치"에 속한 여러 마이그레이션 파일을 모두 되돌립니다:

```shell
php artisan migrate:rollback
```

`step` 옵션을 주면 특정 개수만큼의 마이그레이션을 되돌릴 수 있습니다. 예를 들어, 최근 5개의 마이그레이션을 롤백하려면 다음과 같이 실행합니다:

```shell
php artisan migrate:rollback --step=5
```

`batch` 옵션을 사용하면 특정 배치 단위의 마이그레이션만 롤백할 수 있습니다. 배치 번호는 애플리케이션의 `migrations` 테이블 내 `batch` 값과 대응합니다. 예를 들어 배치 3의 모든 마이그레이션을 되돌리려면 다음과 같이 실행합니다:

```shell
php artisan migrate:rollback --batch=3
```

롤백 시 실행될 SQL 문을 실제로 실행하지 않고 확인하려면 `--pretend` 플래그를 사용할 수 있습니다:

```shell
php artisan migrate:rollback --pretend
```

모든 애플리케이션 마이그레이션을 롤백하려면 `migrate:reset` 명령어를 사용하세요:

```shell
php artisan migrate:reset
```

<a name="roll-back-migrate-using-a-single-command"></a>
#### 한 명령어로 롤백 후 다시 마이그레이션 실행

`migrate:refresh` 명령은 모든 마이그레이션을 롤백한 뒤 `migrate` 명령을 다시 실행합니다. 이 명령은 데이터베이스를 완전히 재생성합니다:

```shell
php artisan migrate:refresh

# 데이터베이스 리프레시 후 모든 시더 실행...
php artisan migrate:refresh --seed
```

`step` 옵션을 넣으면 일부만 롤백 후 재실행할 수 있습니다. 예를 들어 최근 5개를 대상으로 하려면:

```shell
php artisan migrate:refresh --step=5
```

<a name="drop-all-tables-migrate"></a>
#### 모든 테이블 삭제 후 마이그레이션 실행

`migrate:fresh` 명령은 데이터베이스 내 모든 테이블을 삭제한 후 `migrate` 명령을 실행합니다:

```shell
php artisan migrate:fresh

php artisan migrate:fresh --seed
```

기본적으로 `migrate:fresh`는 기본 데이터베이스 연결에 대해서만 테이블을 삭제합니다. 다른 데이터베이스에서 실행하려면 `--database` 옵션으로 연결명을 지정하세요. 연결명은 애플리케이션의 `database` [설정 파일](/docs/master/configuration)에 정의된 이름과 일치해야 합니다:

```shell
php artisan migrate:fresh --database=admin
```

> [!WARNING]
> 이 명령은 테이블 이름의 접두사를 무시하고 데이터베이스 내 모든 테이블을 삭제합니다. 다른 애플리케이션과 공유하는 데이터베이스에서는 신중히 사용해야 합니다.

<a name="tables"></a>
## 테이블 (Tables)

<a name="creating-tables"></a>
### 테이블 생성 (Creating Tables)

새 데이터베이스 테이블을 생성하려면 `Schema` 파사드의 `create` 메서드를 사용합니다. `create` 메서드는 두 개의 인수를 받습니다. 첫 번째는 테이블 이름이고, 두 번째는 `Blueprint` 객체를 받는 클로저로, 새 테이블 정의에 사용됩니다:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::create('users', function (Blueprint $table) {
    $table->id();
    $table->string('name');
    $table->string('email');
    $table->timestamps();
});
```

테이블 생성 시, [컬럼 생성 메서드](#creating-columns)를 사용해 테이블 컬럼을 정의할 수 있습니다.

<a name="determining-table-column-existence"></a>
#### 테이블 / 컬럼 존재 여부 확인

테이블, 컬럼, 인덱스가 존재하는지 확인하려면 `hasTable`, `hasColumn`, `hasIndex` 메서드를 사용하세요:

```php
if (Schema::hasTable('users')) {
    // "users" 테이블이 존재함...
}

if (Schema::hasColumn('users', 'email')) {
    // "users" 테이블이 존재하고 "email" 컬럼도 있음...
}

if (Schema::hasIndex('users', ['email'], 'unique')) {
    // "users" 테이블에 "email" 컬럼에 대한 유니크 인덱스가 존재함...
}
```

<a name="database-connection-table-options"></a>
#### 데이터베이스 연결 및 테이블 옵션

기본 애플리케이션 데이터베이스 연결이 아닌 다른 연결에서 스키마 작업을 수행하려면 `connection` 메서드를 사용할 수 있습니다:

```php
Schema::connection('sqlite')->create('users', function (Blueprint $table) {
    $table->id();
});
```

또한 다음과 같은 몇 가지 속성 및 메서드로 테이블 생성 시 추가 옵션도 지정할 수 있습니다.

MariaDB 또는 MySQL에서 테이블 저장 엔진을 지정하려면 `engine` 속성을 사용하세요:

```php
Schema::create('users', function (Blueprint $table) {
    $table->engine('InnoDB');

    // ...
});
```

문자 집합과 콜레이션도 MariaDB, MySQL에서 `charset`, `collation` 속성으로 지정할 수 있습니다:

```php
Schema::create('users', function (Blueprint $table) {
    $table->charset('utf8mb4');
    $table->collation('utf8mb4_unicode_ci');

    // ...
});
```

테이블을 "임시" 테이블로 만들고 싶다면 `temporary` 메서드를 호출하세요. 임시 테이블은 현재 DB 세션에서만 보이며, 연결 종료 시 자동 삭제됩니다:

```php
Schema::create('calculations', function (Blueprint $table) {
    $table->temporary();

    // ...
});
```

테이블에 "코멘트"를 추가하고 싶다면 `comment` 메서드를 호출할 수 있습니다. 현재는 MariaDB, MySQL, PostgreSQL에서만 지원합니다:

```php
Schema::create('calculations', function (Blueprint $table) {
    $table->comment('Business calculations');

    // ...
});
```

<a name="updating-tables"></a>
### 테이블 업데이트 (Updating Tables)

기존 테이블을 수정하려면 `Schema` 파사드의 `table` 메서드를 사용하세요. 이 메서드는 `create` 메서드처럼 두 인수를 받는데, 첫 번째는 테이블 이름, 두 번째는 `Blueprint` 인스턴스를 받는 클로저입니다. 클로저 내에서 컬럼이나 인덱스를 추가할 수 있습니다:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->integer('votes');
});
```

<a name="renaming-and-dropping-tables"></a>
### 테이블 이름 변경 / 삭제 (Renaming / Dropping Tables)

기존 데이터베이스 테이블의 이름을 변경하려면 `rename` 메서드를 사용하세요:

```php
use Illuminate\Support\Facades\Schema;

Schema::rename($from, $to);
```

테이블을 삭제하려면 `drop` 또는 `dropIfExists` 메서드를 사용합니다:

```php
Schema::drop('users');

Schema::dropIfExists('users');
```

<a name="renaming-tables-with-foreign-keys"></a>
#### 외래 키가 있는 테이블 이름 변경

테이블 이름을 변경하기 전에 외래 키 제약조건에 대해 마이그레이션 파일에 명시적으로 이름을 지정했는지 확인해야 합니다. 그렇지 않으면 외래 키 제약조건 이름이 이전 테이블 이름을 참조하게 되어 문제가 발생할 수 있습니다.

<a name="columns"></a>
## 컬럼 (Columns)

<a name="creating-columns"></a>
### 컬럼 생성 (Creating Columns)

`Schema` 파사드의 `table` 메서드를 사용해 기존 테이블을 수정하며 컬럼을 추가할 수 있습니다. `create` 메서드와 마찬가지로, 첫 번째 인수는 테이블 이름, 두 번째 인수는 `Illuminate\Database\Schema\Blueprint` 인스턴스를 받는 클로저입니다:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->integer('votes');
});
```

<a name="available-column-types"></a>
### 사용 가능한 컬럼 타입 (Available Column Types)

스키마 빌더의 Blueprint 클래스는 데이터베이스 테이블에 추가할 수 있는 다양한 컬럼 타입을 제공합니다. 아래 표에 각 타입별 메서드가 나열되어 있습니다.

<a name="booleans-method-list"></a>
#### 불리언 타입

<div class="collection-method-list" markdown="1">

[boolean](#column-method-boolean)

</div>

<a name="strings-and-texts-method-list"></a>
#### 문자열 및 텍스트 타입

<div class="collection-method-list" markdown="1">

[char](#column-method-char)
[longText](#column-method-longText)
[mediumText](#column-method-mediumText)
[string](#column-method-string)
[text](#column-method-text)
[tinyText](#column-method-tinyText)

</div>

<a name="numbers--method-list"></a>
#### 숫자 타입

<div class="collection-method-list" markdown="1">

[bigIncrements](#column-method-bigIncrements)
[bigInteger](#column-method-bigInteger)
[decimal](#column-method-decimal)
[double](#column-method-double)
[float](#column-method-float)
[id](#column-method-id)
[increments](#column-method-increments)
[integer](#column-method-integer)
[mediumIncrements](#column-method-mediumIncrements)
[mediumInteger](#column-method-mediumInteger)
[smallIncrements](#column-method-smallIncrements)
[smallInteger](#column-method-smallInteger)
[tinyIncrements](#column-method-tinyIncrements)
[tinyInteger](#column-method-tinyInteger)
[unsignedBigInteger](#column-method-unsignedBigInteger)
[unsignedInteger](#column-method-unsignedInteger)
[unsignedMediumInteger](#column-method-unsignedMediumInteger)
[unsignedSmallInteger](#column-method-unsignedSmallInteger)
[unsignedTinyInteger](#column-method-unsignedTinyInteger)

</div>

<a name="dates-and-times-method-list"></a>
#### 날짜 및 시간 타입

<div class="collection-method-list" markdown="1">

[dateTime](#column-method-dateTime)
[dateTimeTz](#column-method-dateTimeTz)
[date](#column-method-date)
[time](#column-method-time)
[timeTz](#column-method-timeTz)
[timestamp](#column-method-timestamp)
[timestamps](#column-method-timestamps)
[timestampsTz](#column-method-timestampsTz)
[softDeletes](#column-method-softDeletes)
[softDeletesTz](#column-method-softDeletesTz)
[year](#column-method-year)

</div>

<a name="binaries-method-list"></a>
#### 바이너리 타입

<div class="collection-method-list" markdown="1">

[binary](#column-method-binary)

</div>

<a name="object-and-jsons-method-list"></a>
#### 객체 및 JSON 타입

<div class="collection-method-list" markdown="1">

[json](#column-method-json)
[jsonb](#column-method-jsonb)

</div>

<a name="uuids-and-ulids-method-list"></a>
#### UUID 및 ULID 타입

<div class="collection-method-list" markdown="1">

[ulid](#column-method-ulid)
[ulidMorphs](#column-method-ulidMorphs)
[uuid](#column-method-uuid)
[uuidMorphs](#column-method-uuidMorphs)
[nullableUlidMorphs](#column-method-nullableUlidMorphs)
[nullableUuidMorphs](#column-method-nullableUuidMorphs)

</div>

<a name="spatials-method-list"></a>
#### 공간 타입

<div class="collection-method-list" markdown="1">

[geography](#column-method-geography)
[geometry](#column-method-geometry)

</div>

#### 관계 타입

<div class="collection-method-list" markdown="1">

[foreignId](#column-method-foreignId)
[foreignIdFor](#column-method-foreignIdFor)
[foreignUlid](#column-method-foreignUlid)
[foreignUuid](#column-method-foreignUuid)
[morphs](#column-method-morphs)
[nullableMorphs](#column-method-nullableMorphs)

</div>

<a name="spacifics-method-list"></a>
#### 특수 타입

<div class="collection-method-list" markdown="1">

[enum](#column-method-enum)
[set](#column-method-set)
[macAddress](#column-method-macAddress)
[ipAddress](#column-method-ipAddress)
[rememberToken](#column-method-rememberToken)
[vector](#column-method-vector)

</div>

<a name="column-method-bigIncrements"></a>
#### `bigIncrements()`

`bigIncrements` 메서드는 자동 증가하는 `UNSIGNED BIGINT` (주 키) 타입 컬럼을 생성합니다:

```php
$table->bigIncrements('id');
```

<a name="column-method-bigInteger"></a>
#### `bigInteger()`

`bigInteger` 메서드는 `BIGINT` 타입 컬럼을 생성합니다:

```php
$table->bigInteger('votes');
```

<a name="column-method-binary"></a>
#### `binary()`

`binary` 메서드는 `BLOB` 타입 컬럼을 생성합니다:

```php
$table->binary('photo');
```

MySQL, MariaDB, SQL Server에서는 `length`와 `fixed` 인수를 전달해 `VARBINARY` 또는 `BINARY` 컬럼을 생성할 수 있습니다:

```php
$table->binary('data', length: 16); // VARBINARY(16)

$table->binary('data', length: 16, fixed: true); // BINARY(16)
```

<a name="column-method-boolean"></a>
#### `boolean()`

`boolean` 메서드는 `BOOLEAN` 타입 컬럼을 생성합니다:

```php
$table->boolean('confirmed');
```

<a name="column-method-char"></a>
#### `char()`

`char` 메서드는 지정한 길이의 `CHAR` 타입 컬럼을 생성합니다:

```php
$table->char('name', length: 100);
```

<a name="column-method-dateTimeTz"></a>
#### `dateTimeTz()`

`dateTimeTz` 메서드는 시간대 정보를 포함한 `DATETIME` 타입 컬럼을 생성하며, 선택적 소수점 밀도를 지정할 수 있습니다:

```php
$table->dateTimeTz('created_at', precision: 0);
```

<a name="column-method-dateTime"></a>
#### `dateTime()`

`dateTime` 메서드는 소수점 밀도를 설정할 수 있는 `DATETIME` 타입 컬럼을 생성합니다:

```php
$table->dateTime('created_at', precision: 0);
```

<a name="column-method-date"></a>
#### `date()`

`date` 메서드는 `DATE` 타입 컬럼을 생성합니다:

```php
$table->date('created_at');
```

<a name="column-method-decimal"></a>
#### `decimal()`

`decimal` 메서드는 총 자릿수(precision)와 소수점 자릿수(scale)를 지정하는 `DECIMAL` 타입 컬럼을 생성합니다:

```php
$table->decimal('amount', total: 8, places: 2);
```

<a name="column-method-double"></a>
#### `double()`

`double` 메서드는 `DOUBLE` 타입 컬럼을 생성합니다:

```php
$table->double('amount');
```

<a name="column-method-enum"></a>
#### `enum()`

`enum` 메서드는 지정한 유효값을 갖는 `ENUM` 타입 컬럼을 생성합니다:

```php
$table->enum('difficulty', ['easy', 'hard']);
```

<a name="column-method-float"></a>
#### `float()`

`float` 메서드는 지정한 정밀도의 `FLOAT` 타입 컬럼을 생성합니다:

```php
$table->float('amount', precision: 53);
```

<a name="column-method-foreignId"></a>
#### `foreignId()`

`foreignId` 메서드는 `UNSIGNED BIGINT` 타입 컬럼을 생성합니다:

```php
$table->foreignId('user_id');
```

<a name="column-method-foreignIdFor"></a>
#### `foreignIdFor()`

`foreignIdFor` 메서드는 주어진 모델 클래스에 대응하는 `{컬럼명}_id` 타입 컬럼을 추가합니다. 컬럼 타입은 모델 키 타입에 따라 `UNSIGNED BIGINT`, `CHAR(36)`, `CHAR(26)` 중 하나가 됩니다:

```php
$table->foreignIdFor(User::class);
```

<a name="column-method-foreignUlid"></a>
#### `foreignUlid()`

`foreignUlid` 메서드는 `ULID` 타입 컬럼을 생성합니다:

```php
$table->foreignUlid('user_id');
```

<a name="column-method-foreignUuid"></a>
#### `foreignUuid()`

`foreignUuid` 메서드는 `UUID` 타입 컬럼을 생성합니다:

```php
$table->foreignUuid('user_id');
```

<a name="column-method-geography"></a>
#### `geography()`

`geography` 메서드는 지정한 공간 타입과 SRID(공간 참조 시스템 식별자)를 갖는 `GEOGRAPHY` 타입 컬럼을 생성합니다:

```php
$table->geography('coordinates', subtype: 'point', srid: 4326);
```

> [!NOTE]
> 공간 타입 지원은 사용 중인 데이터베이스 드라이버에 따라 다릅니다. PostgreSQL을 사용하는 경우 `PostGIS` 확장 설치가 필요합니다.

<a name="column-method-geometry"></a>
#### `geometry()`

`geometry` 메서드는 지정한 공간 타입과 SRID를 가진 `GEOMETRY` 타입 컬럼을 생성합니다:

```php
$table->geometry('positions', subtype: 'point', srid: 0);
```

> [!NOTE]
> 공간 타입 지원은 데이터베이스 드라이버 의존적입니다. PostgreSQL에서는 `PostGIS` 확장 설치가 필요합니다.

<a name="column-method-id"></a>
#### `id()`

`id` 메서드는 `bigIncrements` 메서드의 별칭입니다. 기본값으로 `id` 컬럼을 만듭니다만, 다른 이름을 지정할 수도 있습니다:

```php
$table->id();
```

<a name="column-method-increments"></a>
#### `increments()`

`increments` 메서드는 자동 증가하는 `UNSIGNED INTEGER` 타입 컬럼(주 키)를 생성합니다:

```php
$table->increments('id');
```

<a name="column-method-integer"></a>
#### `integer()`

`integer` 메서드는 `INTEGER` 타입 컬럼을 생성합니다:

```php
$table->integer('votes');
```

<a name="column-method-ipAddress"></a>
#### `ipAddress()`

`ipAddress` 메서드는 IP 주소를 저장할 `VARCHAR` 타입 컬럼을 생성합니다. PostgreSQL을 사용할 경우 `INET` 컬럼이 생성됩니다:

```php
$table->ipAddress('visitor');
```

<a name="column-method-json"></a>
#### `json()`

`json` 메서드는 `JSON` 타입 컬럼을 생성합니다. SQLite를 사용할 경우 `TEXT` 컬럼이 생성됩니다:

```php
$table->json('options');
```

<a name="column-method-jsonb"></a>
#### `jsonb()`

`jsonb` 메서드는 `JSONB` 타입 컬럼을 생성합니다. SQLite 지원 시 `TEXT` 컬럼으로 대체됩니다:

```php
$table->jsonb('options');
```

<a name="column-method-longText"></a>
#### `longText()`

`longText` 메서드는 `LONGTEXT` 타입 컬럼을 생성합니다. MySQL, MariaDB에서는 `binary` 문자 집합을 적용해 `LONGBLOB` 타입 컬럼으로 만들 수 있습니다:

```php
$table->longText('description');

$table->longText('data')->charset('binary'); // LONGBLOB
```

<a name="column-method-macAddress"></a>
#### `macAddress()`

`macAddress` 메서드는 MAC 주소 저장용 컬럼을 생성합니다. PostgreSQL 같은 일부 DB는 전용 컬럼 타입을, 나머지는 문자열 컬럼으로 생성합니다:

```php
$table->macAddress('device');
```

<a name="column-method-mediumIncrements"></a>
#### `mediumIncrements()`

`mediumIncrements` 메서드는 자동 증가하는 `UNSIGNED MEDIUMINT` 타입 컬럼(주 키)를 생성합니다:

```php
$table->mediumIncrements('id');
```

<a name="column-method-mediumInteger"></a>
#### `mediumInteger()`

`mediumInteger` 메서드는 `MEDIUMINT` 타입 컬럼을 생성합니다:

```php
$table->mediumInteger('votes');
```

<a name="column-method-mediumText"></a>
#### `mediumText()`

`mediumText` 메서드는 `MEDIUMTEXT` 타입 컬럼을 생성합니다. MySQL, MariaDB에서는 `binary` 문자 집합을 적용해 `MEDIUMBLOB` 컬럼으로 만들 수 있습니다:

```php
$table->mediumText('description');

$table->mediumText('data')->charset('binary'); // MEDIUMBLOB
```

<a name="column-method-morphs"></a>
#### `morphs()`

`morphs` 메서드는 `{컬럼}_id` 타입 컬럼과 `{컬럼}_type` `VARCHAR` 컬럼 2개를 생성합니다. `{컬럼}_id` 타입은 모델 키 유형에 따라 `UNSIGNED BIGINT`, `CHAR(36)`, `CHAR(26)` 중 하나입니다.

이 메서드는 다형성(polymorphic) Eloquent 관계를 정의할 때 사용합니다. 예를 들어 `taggable_id`, `taggable_type` 컬럼을 만듭니다:

```php
$table->morphs('taggable');
```

<a name="column-method-nullableMorphs"></a>
#### `nullableMorphs()`

`morphs` 메서드와 동일하지만, 생성되는 두 컬럼이 "nullable" 상태입니다:

```php
$table->nullableMorphs('taggable');
```

<a name="column-method-nullableUlidMorphs"></a>
#### `nullableUlidMorphs()`

`ulidMorphs` 메서드와 같지만 생성되는 컬럼이 "nullable"입니다:

```php
$table->nullableUlidMorphs('taggable');
```

<a name="column-method-nullableUuidMorphs"></a>
#### `nullableUuidMorphs()`

`uuidMorphs` 메서드와 같지만 생성된 컬럼이 "nullable"입니다:

```php
$table->nullableUuidMorphs('taggable');
```

<a name="column-method-rememberToken"></a>
#### `rememberToken()`

로그인 유지를 위한 "remember me" 인증 토큰을 저장하는 `VARCHAR(100)` 타입의 nullable 컬럼을 생성합니다:

```php
$table->rememberToken();
```

<a name="column-method-set"></a>
#### `set()`

`set` 메서드는 지정한 유효 값 목록을 갖는 `SET` 타입 컬럼을 생성합니다:

```php
$table->set('flavors', ['strawberry', 'vanilla']);
```

<a name="column-method-smallIncrements"></a>
#### `smallIncrements()`

`smallIncrements` 메서드는 자동 증가하는 `UNSIGNED SMALLINT` 타입 컬럼(주 키)를 생성합니다:

```php
$table->smallIncrements('id');
```

<a name="column-method-smallInteger"></a>
#### `smallInteger()`

`smallInteger` 메서드는 `SMALLINT` 타입 컬럼을 생성합니다:

```php
$table->smallInteger('votes');
```

<a name="column-method-softDeletesTz"></a>
#### `softDeletesTz()`

`softDeletesTz` 메서드는 선택적 소수점 밀도를 갖는 nullable `deleted_at` `TIMESTAMP` (시간대 포함) 컬럼을 추가합니다. 이 컬럼은 Eloquent의 "soft delete" 기능에 사용됩니다:

```php
$table->softDeletesTz('deleted_at', precision: 0);
```

<a name="column-method-softDeletes"></a>
#### `softDeletes()`

`softDeletes` 메서드는 nullable `deleted_at` `TIMESTAMP` 컬럼을 소수점 밀도와 함께 추가합니다. Eloquent의 소프트 삭제에 사용됩니다:

```php
$table->softDeletes('deleted_at', precision: 0);
```

<a name="column-method-string"></a>
#### `string()`

`string` 메서드는 지정한 길이의 `VARCHAR` 타입 컬럼을 생성합니다:

```php
$table->string('name', length: 100);
```

<a name="column-method-text"></a>
#### `text()`

`text` 메서드는 `TEXT` 타입 컬럼을 생성합니다. MySQL, MariaDB에서는 `binary` 문자 집합 지정 시 `BLOB` 타입으로 생성됩니다:

```php
$table->text('description');

$table->text('data')->charset('binary'); // BLOB
```

<a name="column-method-timeTz"></a>
#### `timeTz()`

`timeTz` 메서드는 시간대가 포함된 `TIME` 타입 컬럼을 선택적 소수점 밀도로 생성합니다:

```php
$table->timeTz('sunrise', precision: 0);
```

<a name="column-method-time"></a>
#### `time()`

`time` 메서드는 선택적 소수점 밀도를 가진 `TIME` 타입 컬럼을 생성합니다:

```php
$table->time('sunrise', precision: 0);
```

<a name="column-method-timestampTz"></a>
#### `timestampTz()`

`timestampTz` 메서드는 시간대 포함 선택적 소수점 밀도의 `TIMESTAMP` 타입 컬럼을 생성합니다:

```php
$table->timestampTz('added_at', precision: 0);
```

<a name="column-method-timestamp"></a>
#### `timestamp()`

`timestamp` 메서드는 선택적 소수점 밀도의 `TIMESTAMP` 타입 컬럼을 생성합니다:

```php
$table->timestamp('added_at', precision: 0);
```

<a name="column-method-timestampsTz"></a>
#### `timestampsTz()`

`timestampsTz` 메서드는 `created_at`, `updated_at` 2개의 `TIMESTAMP` (시간대 포함) 컬럼을 선택적 소수점 밀도로 생성합니다:

```php
$table->timestampsTz(precision: 0);
```

<a name="column-method-timestamps"></a>
#### `timestamps()`

`timestamps` 메서드는 `created_at`, `updated_at` 2개의 `TIMESTAMP` 컬럼을 선택적 소수점 밀도로 생성합니다:

```php
$table->timestamps(precision: 0);
```

<a name="column-method-tinyIncrements"></a>
#### `tinyIncrements()`

`tinyIncrements` 메서드는 자동 증가하는 `UNSIGNED TINYINT` 타입 컬럼(주 키)를 생성합니다:

```php
$table->tinyIncrements('id');
```

<a name="column-method-tinyInteger"></a>
#### `tinyInteger()`

`tinyInteger` 메서드는 `TINYINT` 타입 컬럼을 생성합니다:

```php
$table->tinyInteger('votes');
```

<a name="column-method-tinyText"></a>
#### `tinyText()`

`tinyText` 메서드는 `TINYTEXT` 타입 컬럼을 생성합니다. MySQL, MariaDB에서는 `binary` 문자 집합 지정 시 `TINYBLOB` 타입이 됩니다:

```php
$table->tinyText('notes');

$table->tinyText('data')->charset('binary'); // TINYBLOB
```

<a name="column-method-unsignedBigInteger"></a>
#### `unsignedBigInteger()`

`unsignedBigInteger` 메서드는 `UNSIGNED BIGINT` 타입 컬럼을 생성합니다:

```php
$table->unsignedBigInteger('votes');
```

<a name="column-method-unsignedInteger"></a>
#### `unsignedInteger()`

`unsignedInteger` 메서드는 `UNSIGNED INTEGER` 타입 컬럼을 생성합니다:

```php
$table->unsignedInteger('votes');
```

<a name="column-method-unsignedMediumInteger"></a>
#### `unsignedMediumInteger()`

`unsignedMediumInteger` 메서드는 `UNSIGNED MEDIUMINT` 타입 컬럼을 생성합니다:

```php
$table->unsignedMediumInteger('votes');
```

<a name="column-method-unsignedSmallInteger"></a>
#### `unsignedSmallInteger()`

`unsignedSmallInteger` 메서드는 `UNSIGNED SMALLINT` 타입 컬럼을 생성합니다:

```php
$table->unsignedSmallInteger('votes');
```

<a name="column-method-unsignedTinyInteger"></a>
#### `unsignedTinyInteger()`

`unsignedTinyInteger` 메서드는 `UNSIGNED TINYINT` 타입 컬럼을 생성합니다:

```php
$table->unsignedTinyInteger('votes');
```

<a name="column-method-ulidMorphs"></a>
#### `ulidMorphs()`

`ulidMorphs` 메서드는 `{컬럼}_id` `CHAR(26)` 타입과 `{컬럼}_type` `VARCHAR` 타입 컬럼 2개를 생성합니다.

ULID 식별자를 사용하는 다형성 Eloquent 관계를 정의할 때 사용됩니다. 예: `taggable_id`, `taggable_type` 컬럼 생성.

```php
$table->ulidMorphs('taggable');
```

<a name="column-method-uuidMorphs"></a>
#### `uuidMorphs()`

`uuidMorphs` 메서드는 `{컬럼}_id` `CHAR(36)`와 `{컬럼}_type` `VARCHAR` 컬럼 2개를 생성합니다.

UUID 식별자를 사용하는 다형성 Eloquent 관계에서 사용됩니다. 예: `taggable_id`, `taggable_type` 컬럼 생성.

```php
$table->uuidMorphs('taggable');
```

<a name="column-method-ulid"></a>
#### `ulid()`

`ulid` 메서드는 `ULID` 타입 컬럼을 생성합니다:

```php
$table->ulid('id');
```

<a name="column-method-uuid"></a>
#### `uuid()`

`uuid` 메서드는 `UUID` 타입 컬럼을 생성합니다:

```php
$table->uuid('id');
```

<a name="column-method-vector"></a>
#### `vector()`

`vector` 메서드는 벡터 타입 컬럼을 생성하며 차원(dimensions)을 지정합니다:

```php
$table->vector('embedding', dimensions: 100);
```

<a name="column-method-year"></a>
#### `year()`

`year` 메서드는 `YEAR` 타입 컬럼을 생성합니다:

```php
$table->year('birth_year');
```

<a name="column-modifiers"></a>
### 컬럼 수정자 (Column Modifiers)

위의 컬럼 타입 메서드 외에도 컬럼 생성 시 다양한 수정자를 사용할 수 있습니다. 예를 들어 컬럼을 nullable로 만들려면 `nullable` 메서드를 사용하세요:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->string('email')->nullable();
});
```

다음 표는 이용 가능한 컬럼 수정자 목록입니다. 여기에는 [인덱스 수정자](#creating-indexes)는 포함하지 않습니다.

<div class="overflow-auto">

| 수정자                                    | 설명                                                       |
| ----------------------------------------- | ---------------------------------------------------------- |
| `->after('column')`                        | 컬럼을 특정 컬럼 이후에 배치 (MariaDB / MySQL)             |
| `->autoIncrement()`                        | `INTEGER` 컬럼을 자동 증가형(Primary key)으로 설정          |
| `->charset('utf8mb4')`                     | 컬럼 문자 집합 지정 (MariaDB / MySQL)                      |
| `->collation('utf8mb4_unicode_ci')`       | 컬럼 콜레이션 지정                                         |
| `->comment('my comment')`                  | 컬럼 코멘트 추가 (MariaDB / MySQL / PostgreSQL)            |
| `->default($value)`                        | 컬럼 기본값 지정                                           |
| `->first()`                               | 컬럼을 테이블의 가장 앞으로 이동 (MariaDB / MySQL)          |
| `->from($integer)`                        | 자동 증가 필드의 시작 값 설정 (MariaDB / MySQL / PostgreSQL) |
| `->invisible()`                           | `SELECT *` 시 컬럼을 숨김 (MariaDB / MySQL)                |
| `->nullable($value = true)`                | 컬럼에 NULL 값 허용                                        |
| `->storedAs($expression)`                  | 저장된 생성 컬럼 생성 (MariaDB / MySQL / PostgreSQL / SQLite) |
| `->unsigned()`                            | `INTEGER` 컬럼을 UNSIGNED로 설정 (MariaDB / MySQL)          |
| `->useCurrent()`                          | `TIMESTAMP` 기본값을 `CURRENT_TIMESTAMP`로 설정            |
| `->useCurrentOnUpdate()`                  | 레코드 업데이트 시 `TIMESTAMP`를 `CURRENT_TIMESTAMP`로 설정 (MariaDB / MySQL) |
| `->virtualAs($expression)`                 | 가상 생성 컬럼 생성 (MariaDB / MySQL / SQLite)              |
| `->generatedAs($expression)`               | PostgreSQL 일련시퀀스로 생성 컬럼 생성                        |
| `->always()`                             | PostgreSQL 아이덴티티 컬럼에서 입력값보다 시퀀스 값을 우선하는 설정   |

</div>

<a name="default-expressions"></a>
#### 기본값 표현식 (Default Expressions)

`default` 수정자는 값이나 `Illuminate\Database\Query\Expression` 인스턴스를 받을 수 있습니다. `Expression`을 쓰면 Laravel이 값을 쿼리 내에서 따옴표로 감싸지 않아 DB 고유 함수를 그대로 쓸 수 있습니다. JSON 컬럼에 기본값을 지정할 때 유용합니다:

```php
<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Query\Expression;
use Illuminate\Database\Migrations\Migration;

return new class extends Migration
{
    /**
     * Run the migrations.
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
```

> [!WARNING]
> 기본값 표현식 지원 여부는 데이터베이스 드라이버, 버전, 컬럼 타입에 따라 다릅니다. DB 문서를 참고하세요.

<a name="column-order"></a>
#### 컬럼 순서 지정

MariaDB 또는 MySQL에서는 `after` 메서드를 사용해 특정 컬럼 뒤에 새로운 컬럼을 추가할 수 있습니다:

```php
$table->after('password', function (Blueprint $table) {
    $table->string('address_line1');
    $table->string('address_line2');
    $table->string('city');
});
```

<a name="modifying-columns"></a>
### 컬럼 수정 (Modifying Columns)

`change` 메서드를 사용하면 기존 컬럼의 타입과 속성을 수정할 수 있습니다. 예를 들어, `name` 컬럼의 크기를 25에서 50으로 늘리고 싶다면 다음과 같이 정의한 후 `change`를 호출하세요:

```php
Schema::table('users', function (Blueprint $table) {
    $table->string('name', 50)->change();
});
```

컬럼을 수정할 때, 유지하고 싶은 수정자는 모두 명시적으로 호출해야 합니다. 누락하면 해당 속성은 제거됩니다. 예를 들어 `unsigned`, `default`, `comment` 속성을 유지하려면 다음과 같이 작성해야 합니다:

```php
Schema::table('users', function (Blueprint $table) {
    $table->integer('votes')->unsigned()->default(1)->comment('my comment')->change();
});
```

`change`는 인덱스를 변경하지 않습니다. 필요 시 인덱스 수정자를 명시적으로 호출해 추가하거나 삭제할 수 있습니다:

```php
// 인덱스 추가
$table->bigIncrements('id')->primary()->change();

// 인덱스 삭제
$table->char('postal_code', 10)->unique(false)->change();
```

<a name="renaming-columns"></a>
### 컬럼 이름 변경 (Renaming Columns)

컬럼 이름을 변경하려면 스키마 빌더의 `renameColumn` 메서드를 사용하세요:

```php
Schema::table('users', function (Blueprint $table) {
    $table->renameColumn('from', 'to');
});
```

<a name="dropping-columns"></a>
### 컬럼 삭제 (Dropping Columns)

컬럼을 삭제하려면 스키마 빌더의 `dropColumn` 메서드를 사용합니다:

```php
Schema::table('users', function (Blueprint $table) {
    $table->dropColumn('votes');
});
```

여러 컬럼을 한꺼번에 삭제하려면 컬럼명 배열을 전달하세요:

```php
Schema::table('users', function (Blueprint $table) {
    $table->dropColumn(['votes', 'avatar', 'location']);
});
```

<a name="available-command-aliases"></a>
#### 사용 가능한 삭제 관련 별칭 명령어

Laravel은 자주 쓰이는 컬럼 삭제 메서드를 편리하게 제공합니다. 다음 표에서 각 메서드 용도를 확인하세요:

<div class="overflow-auto">

| 명령어                                | 설명                                          |
| ----------------------------------- | ---------------------------------------------- |
| `$table->dropMorphs('morphable');`  | `morphable_id` 및 `morphable_type` 컬럼 삭제 |
| `$table->dropRememberToken();`      | `remember_token` 컬럼 삭제                      |
| `$table->dropSoftDeletes();`        | `deleted_at` 컬럼 삭제                          |
| `$table->dropSoftDeletesTz();`      | `dropSoftDeletes()`의 별칭                      |
| `$table->dropTimestamps();`         | `created_at` 및 `updated_at` 컬럼 삭제          |
| `$table->dropTimestampsTz();`       | `dropTimestamps()`의 별칭                       |

</div>

<a name="indexes"></a>
## 인덱스 (Indexes)

<a name="creating-indexes"></a>
### 인덱스 생성 (Creating Indexes)

Laravel 스키마 빌더는 여러 유형의 인덱스를 지원합니다. 예를 들어, `email` 컬럼을 생성하면서 고유 인덱스를 지정하려면, 컬럼 정의에 `unique` 메서드를 체이닝할 수 있습니다:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->string('email')->unique();
});
```

인덱스는 컬럼 생성 후에도 별도로 추가할 수 있습니다. 이때는 스키마 빌더에서 `unique` 메서드를 호출하며, 대상 컬럼명을 넘겨줍니다:

```php
$table->unique('email');
```

복합 인덱스(콤파운드 인덱스)를 생성하려면 컬럼명을 배열로 전달하면 됩니다:

```php
$table->index(['account_id', 'created_at']);
```

인덱스 생성 시 Laravel은 테이블명, 컬럼명, 인덱스 타입을 기반으로 자동으로 인덱스 이름을 생성합니다. 직접 인덱스 이름을 지정하려면 두 번째 인수를 전달하세요:

```php
$table->unique('email', 'unique_email');
```

<a name="available-index-types"></a>
#### 사용 가능한 인덱스 타입

스키마 빌더에서 지원하는 각 인덱스 생성 메서드는 두 번째 선택적 인수로 인덱스 이름을 지정할 수 있습니다. 이름을 생략하면 Laravel이 테이블과 컬럼명, 인덱스 유형에서 이름을 자동 생성합니다. 사용 가능한 인덱스 타입은 다음과 같습니다:

<div class="overflow-auto">

| 명령어                                               | 설명                                            |
| ---------------------------------------------------- | ------------------------------------------------ |
| `$table->primary('id');`                             | 기본 키(primary key) 생성                        |
| `$table->primary(['id', 'parent_id']);`              | 복합 기본 키 생성                               |
| `$table->unique('email');`                           | 고유 인덱스 생성                                |
| `$table->index('state');`                            | 일반 인덱스 생성                               |
| `$table->fullText('body');`                          | 전체 텍스트 인덱스 생성 (MariaDB / MySQL / PostgreSQL) |
| `$table->fullText('body')->language('english');`    | 특정 언어별 전체 텍스트 인덱스 생성 (PostgreSQL) |
| `$table->spatialIndex('location');`                  | 공간 인덱스 생성 (SQLite 제외)                  |

</div>

<a name="renaming-indexes"></a>
### 인덱스 이름 변경 (Renaming Indexes)

인덱스 이름을 변경하려면 스키마 빌더의 `renameIndex` 메서드를 사용하세요. 첫 번째 인수로 기존 인덱스 이름, 두 번째 인수로 새 인덱스 이름을 지정합니다:

```php
$table->renameIndex('from', 'to');
```

<a name="dropping-indexes"></a>
### 인덱스 삭제 (Dropping Indexes)

인덱스를 삭제하려면 인덱스 이름을 지정해야 합니다. Laravel은 기본적으로 테이블명, 컬럼명, 인덱스 유형을 조합해 인덱스 이름을 생성합니다. 예시는 다음과 같습니다:

<div class="overflow-auto">

| 명령어                                               | 설명                                |
| ----------------------------------------------------- | ------------------------------------ |
| `$table->dropPrimary('users_id_primary');`            | `users` 테이블에서 기본 키 삭제     |
| `$table->dropUnique('users_email_unique');`           | `users` 테이블에서 고유 인덱스 삭제 |
| `$table->dropIndex('geo_state_index');`               | `geo` 테이블에서 일반 인덱스 삭제   |
| `$table->dropFullText('posts_body_fulltext');`        | `posts` 테이블에서 전체 텍스트 인덱스 삭제 |
| `$table->dropSpatialIndex('geo_location_spatialindex');` | `geo` 테이블에서 공간 인덱스 삭제(SQLite 제외) |

</div>

컬럼 배열을 넘겨주면 자동으로 컨벤션 기반 인덱스 이름을 생성합니다:

```php
Schema::table('geo', function (Blueprint $table) {
    $table->dropIndex(['state']); // 'geo_state_index' 인덱스 삭제
});
```

<a name="foreign-key-constraints"></a>
### 외래 키 제약조건 (Foreign Key Constraints)

Laravel은 데이터베이스 수준에서 참조 무결성을 강제하는 외래 키 제약 생성도 지원합니다. 예를 들어 `posts` 테이블에 `user_id` 컬럼을 만들고, `users` 테이블의 `id` 컬럼을 참조하도록 할 수 있습니다:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('posts', function (Blueprint $table) {
    $table->unsignedBigInteger('user_id');

    $table->foreign('user_id')->references('id')->on('users');
});
```

다만 위 구문은 다소 길기 때문에, Laravel은 관습에 따라 간소화된 문법을 제공합니다. `foreignId` 메서드를 사용하면 다음과 같이 쓸 수 있습니다:

```php
Schema::table('posts', function (Blueprint $table) {
    $table->foreignId('user_id')->constrained();
});
```

`foreignId`는 `UNSIGNED BIGINT` 타입 컬럼을 생성하고, `constrained`는 참조할 테이블 및 컬럼을 관습대로 추론합니다. 만약 테이블명이 기본 관습과 다르면 직접 `constrained`에 지정할 수 있고, 생성할 인덱스 이름도 지정할 수 있습니다:

```php
Schema::table('posts', function (Blueprint $table) {
    $table->foreignId('user_id')->constrained(
        table: 'users', indexName: 'posts_user_id'
    );
});
```

또한 "on delete", "on update" 제약 동작도 지정할 수 있습니다:

```php
$table->foreignId('user_id')
    ->constrained()
    ->onUpdate('cascade')
    ->onDelete('cascade');
```

다음과 같은 편리한 메서드도 있습니다:

<div class="overflow-auto">

| 메서드                         | 설명                                        |
| ------------------------------ | -------------------------------------------- |
| `$table->cascadeOnUpdate();`   | 업데이트 시 연쇄 변경(cascade) 처리           |
| `$table->restrictOnUpdate();`  | 업데이트 시 제한(restrict) 처리               |
| `$table->nullOnUpdate();`      | 업데이트 시 외래 키 값을 null로 설정          |
| `$table->noActionOnUpdate();`  | 업데이트 시 아무 동작도 하지 않음              |
| `$table->cascadeOnDelete();`   | 삭제 시 연쇄 삭제(cascade) 처리                |
| `$table->restrictOnDelete();`  | 삭제 시 제한(restrict) 처리                    |
| `$table->nullOnDelete();`      | 삭제 시 외래 키 값을 null로 설정                |
| `$table->noActionOnDelete();`  | 자식 레코드가 있으면 삭제 방지                 |

</div>

외래 키 컬럼의 추가 수정자는 `constrained` 호출 전에 지정해야 합니다:

```php
$table->foreignId('user_id')
    ->nullable()
    ->constrained();
```

<a name="dropping-foreign-keys"></a>
#### 외래 키 삭제

외래 키를 삭제하려면 `dropForeign` 메서드를 사용하며, 삭제할 외래 키 제약조건 이름을 인수로 전달합니다. 외래 키 이름은 인덱스와 동일한 규칙을 따르며, 기본적으로 테이블명과 컬럼명에 `_foreign` 접미사가 붙습니다:

```php
$table->dropForeign('posts_user_id_foreign');
```

또는 외래 키를 가진 컬럼 이름 배열을 넘겨 Laravel 스타일의 제약조건 이름을 자동으로 생성할 수도 있습니다:

```php
$table->dropForeign(['user_id']);
```

<a name="toggling-foreign-key-constraints"></a>
#### 외래 키 제약조건 활성화 / 비활성화

마이그레이션 내에서 외래 키 제약조건을 활성화하거나 비활성화할 수 있는 메서드가 있습니다:

```php
Schema::enableForeignKeyConstraints();

Schema::disableForeignKeyConstraints();

Schema::withoutForeignKeyConstraints(function () {
    // 클로저 내부에서는 외래 키 제약조건이 비활성화됨...
});
```

> [!WARNING]
> SQLite는 기본적으로 외래 키 제약조건이 비활성화되어 있습니다. SQLite 사용 시, 마이그레이션 내에서 외래 키를 만들려면 데이터베이스 설정에서 외래 키 지원을 활성화해야 합니다. 자세한 내용은 [여기](/docs/master/database#configuration)를 참고하세요.

<a name="events"></a>
## 이벤트 (Events)

편의를 위해 각 마이그레이션 작업 시 다음과 같은 [이벤트](/docs/master/events)가 발생합니다. 모두 `Illuminate\Database\Events\MigrationEvent` 클래스를 상속합니다:

<div class="overflow-auto">

| 클래스명                                        | 설명                                         |
| ------------------------------------------------ | --------------------------------------------- |
| `Illuminate\Database\Events\MigrationsStarted`   | 여러 마이그레이션 배치 실행이 시작될 때 발생 |
| `Illuminate\Database\Events\MigrationsEnded`     | 여러 마이그레이션 배치 실행이 끝났을 때 발생 |
| `Illuminate\Database\Events\MigrationStarted`    | 단일 마이그레이션 실행 시작 시 발생           |
| `Illuminate\Database\Events\MigrationEnded`      | 단일 마이그레이션 실행 종료 시 발생           |
| `Illuminate\Database\Events\NoPendingMigrations` | 실행 대기 중인 마이그레이션이 없을 때 발생    |
| `Illuminate\Database\Events\SchemaDumped`        | 데이터베이스 스키마 덤프 완료 시 발생          |
| `Illuminate\Database\Events\SchemaLoaded`        | 기존 데이터베이스 스키마 덤프 로드 시 발생      |

</div>