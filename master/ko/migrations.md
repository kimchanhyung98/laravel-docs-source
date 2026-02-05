# 데이터베이스: 마이그레이션 (Database: Migrations)

- [소개](#introduction)
- [마이그레이션 생성](#generating-migrations)
    - [마이그레이션 통합(Squashing)](#squashing-migrations)
- [마이그레이션 구조](#migration-structure)
- [마이그레이션 실행](#running-migrations)
    - [마이그레이션 롤백](#rolling-back-migrations)
- [테이블](#tables)
    - [테이블 생성](#creating-tables)
    - [테이블 업데이트](#updating-tables)
    - [테이블 이름 변경 / 삭제](#renaming-and-dropping-tables)
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

마이그레이션(Migration)은 데이터베이스를 위한 버전 관리 시스템과 유사하며, 팀원들이 애플리케이션의 데이터베이스 스키마 정의를 직접 작성하고 공유할 수 있도록 도와줍니다. 소스 컨트롤에서 변경 사항을 받아온 동료에게 데이터베이스 스키마에 컬럼을 수동으로 추가하라고 안내했던 적이 있다면, 그 불편을 마이그레이션이 해결해줍니다.

Laravel의 `Schema` [파사드](/docs/master/facades)는 Laravel이 지원하는 모든 데이터베이스 시스템에 대해 데이터베이스 독립적으로 테이블을 생성하고 조작할 수 있는 기능을 제공합니다. 일반적으로 마이그레이션은 이 파사드를 이용해 데이터베이스 테이블과 컬럼을 생성하고 수정합니다.

<a name="generating-migrations"></a>
## 마이그레이션 생성 (Generating Migrations)

데이터베이스 마이그레이션을 생성하려면 `make:migration` [Artisan 명령어](/docs/master/artisan)를 사용합니다. 새로 만든 마이그레이션은 `database/migrations` 디렉터리에 저장됩니다. 각 마이그레이션 파일 이름에는 타임스탬프가 포함되어 있어 Laravel이 마이그레이션의 순서를 파악할 수 있습니다:

```shell
php artisan make:migration create_flights_table
```

Laravel은 마이그레이션의 이름을 바탕으로 어떤 테이블을 생성하거나 수정할지, 그리고 새 테이블을 생성하는 마이그레이션인지를 추론하려 시도합니다. 만약 마이그레이션 이름에서 테이블 이름을 알아낼 수 있다면, Laravel은 생성된 마이그레이션 파일에 해당 테이블 명을 미리 채워 넣습니다. 그렇지 않을 경우, 마이그레이션 파일에서 직접 테이블 명을 지정하면 됩니다.

생성되는 마이그레이션의 경로를 직접 지정하고 싶다면, `make:migration` 명령어 실행 시 `--path` 옵션을 사용할 수 있습니다. 경로는 애플리케이션의 기본 경로 기준으로 상대경로를 지정해야 합니다.

> [!NOTE]
> 마이그레이션의 스텁(stub)은 [스텁 퍼블리싱](/docs/master/artisan#stub-customization)을 통해 커스터마이징할 수 있습니다.

<a name="squashing-migrations"></a>
### 마이그레이션 통합(Squashing Migrations)

애플리케이션을 개발해 나가다 보면 마이그레이션 파일이 점점 많아져서 `database/migrations` 디렉터리가 수백 개의 마이그레이션으로 넘쳐날 수 있습니다. 이럴 때는 여러 마이그레이션을 하나의 SQL 파일로 "통합(squash)"할 수 있습니다. 시작하려면 `schema:dump` 명령어를 실행하세요:

```shell
php artisan schema:dump

# 현재 데이터베이스 스키마를 덤프하고 기존 마이그레이션을 삭제(prune)합니다...
php artisan schema:dump --prune
```

이 명령어를 실행하면, Laravel은 애플리케이션의 `database/schema` 디렉터리에 "스키마" 파일을 기록합니다. 스키마 파일 이름은 데이터베이스 연결명과 일치합니다. 이후 데이터베이스에 아직 실행된 마이그레이션이 없다면, Laravel은 먼저 해당 데이터베이스 연결의 스키마 파일에 들어 있는 SQL 문을 실행합니다. 이후 스키마 덤프에 포함되지 않은 나머지 마이그레이션이 순서대로 실행됩니다.

만약 애플리케이션의 테스트가 로컬 개발 환경에서 주로 사용하는 데이터베이스와 다른 데이터베이스 연결을 사용한다면, 테스트를 위해 해당 데이터베이스 연결로도 스키마 파일을 반드시 덤프해야 합니다. 보통은 아래와 같이, 먼저 자주 사용하는 데이터베이스 연결로 덤프하고 이어서 테스트용 데이터베이스에도 덤프해줍니다:

```shell
php artisan schema:dump
php artisan schema:dump --database=testing --prune
```

데이터베이스 스키마 파일은 소스 컨트롤에 반드시 커밋해야 합니다. 그러면 새로 참여하는 팀원들도 빠르게 애플리케이션의 초반 데이터베이스 구조를 만들 수 있습니다.

> [!WARNING]
> 마이그레이션 통합 기능은 MariaDB, MySQL, PostgreSQL, SQLite 데이터베이스에서만 사용할 수 있으며, 데이터베이스의 커맨드 라인 클라이언트를 필요로 합니다.

<a name="migration-structure"></a>
## 마이그레이션 구조 (Migration Structure)

마이그레이션 클래스는 `up`과 `down` 두 개의 메서드를 포함합니다. `up` 메서드는 새로운 테이블, 컬럼 또는 인덱스를 데이터베이스에 추가할 때 사용하며, `down` 메서드는 `up` 메서드에서 수행된 작업을 되돌립니다.

이 두 메서드 내에서는 Laravel의 스키마 빌더를 사용해 테이블을 직관적으로 생성하고 수정할 수 있습니다. `Schema` 빌더에서 사용할 수 있는 모든 메서드는 [별도의 문서](#creating-tables)를 참고하세요. 예를 들어, 다음 마이그레이션은 `flights` 테이블을 생성합니다:

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
#### 마이그레이션 데이터베이스 연결 설정

마이그레이션이 애플리케이션의 기본 데이터베이스 연결이 아닌 다른 연결을 사용할 경우, `$connection` 속성을 설정해야 합니다:

```php
/**
 * The database connection that should be used by the migration.
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

<a name="skipping-migrations"></a>
#### 마이그레이션 건너뛰기

특정 마이그레이션이 아직 활성화되지 않은 기능을 지원하는 용도이며, 아직 실행하고 싶지 않은 경우, 마이그레이션에 `shouldRun` 메서드를 정의할 수 있습니다. 이 메서드가 `false`를 반환하면 해당 마이그레이션은 실행되지 않습니다:

```php
use App\Models\Flight;
use Laravel\Pennant\Feature;

/**
 * Determine if this migration should run.
 */
public function shouldRun(): bool
{
    return Feature::active(Flight::class);
}
```

<a name="running-migrations"></a>
## 마이그레이션 실행 (Running Migrations)

모든 미실행 마이그레이션을 실행하려면 `migrate` Artisan 명령어를 실행합니다:

```shell
php artisan migrate
```

이미 실행된 마이그레이션과 아직 대기 상태인 마이그레이션을 확인하고 싶다면, `migrate:status` Artisan 명령어를 사용할 수 있습니다:

```shell
php artisan migrate:status
```

마이그레이션이 실제로 실행되기 전에 어떤 SQL 문이 실행되는지 확인하려면, `migrate` 명령에 `--pretend` 플래그를 추가합니다:

```shell
php artisan migrate --pretend
```

<a name="isolating-migration-execution"></a>
#### 마이그레이션 실행 격리하기

여러 서버에서 애플리케이션을 배포하고, 배포 도중 마이그레이션을 실행해야 하는 경우 두 서버에서 동시에 데이터베이스 마이그레이션이 실행되는 상황을 피하고 싶을 수 있습니다. 이를 방지하려면, `migrate` 명령 실행 시 `isolated` 옵션을 사용할 수 있습니다.

이 옵션이 제공되면, Laravel은 마이그레이션 실행 전 애플리케이션의 캐시 드라이버를 이용해 원자적(atomic) 락을 획득합니다. 해당 락이 유지되는 동안 다른 모든 마이그레이션 실행 시도는 무시되며, 명령은 정상적으로 종료됩니다:

```shell
php artisan migrate --isolated
```

> [!WARNING]
> 이 기능을 사용하려면 애플리케이션의 기본 캐시 드라이버가 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 중 하나여야 하며, 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

<a name="forcing-migrations-to-run-in-production"></a>
#### 운영 환경 강제 마이그레이션 실행

몇몇 마이그레이션 작업은 파괴적(destructive)이어서 데이터 손실을 초래할 수 있습니다. 이를 방지하기 위해 운영 환경의 데이터베이스에서 해당 명령어를 실행하려 할 때는 확인 메시지가 표시됩니다. 프롬프트 없이 명령을 강제로 실행하려면, `--force` 플래그를 사용하세요:

```shell
php artisan migrate --force
```

<a name="rolling-back-migrations"></a>
### 마이그레이션 롤백 (Rolling Back Migrations)

가장 최근에 실행된 마이그레이션 작업을 되돌리려면, `rollback` Artisan 명령어를 사용할 수 있습니다. 이 명령어는 하나의 "배치(batch)"에 해당하는 여러 개의 마이그레이션 파일을 되돌립니다:

```shell
php artisan migrate:rollback
```

`step` 옵션을 사용해서 지정한 개수만큼 마이그레이션을 되돌릴 수 있습니다. 예를 들어, 다음 명령은 최근 5개의 마이그레이션만 롤백합니다:

```shell
php artisan migrate:rollback --step=5
```

특정 "배치"의 마이그레이션만 롤백하려면, `batch` 옵션에 애플리케이션의 `migrations` 테이블에 있는 배치 값을 지정하세요. 아래처럼 사용됩니다:

```shell
php artisan migrate:rollback --batch=3
```

롤백 전에 실제로 실행될 SQL 문을 확인하려면, `migrate:rollback` 명령어에 `--pretend` 옵션을 제공합니다:

```shell
php artisan migrate:rollback --pretend
```

`migrate:reset` 명령어는 애플리케이션의 모든 마이그레이션을 롤백합니다:

```shell
php artisan migrate:reset
```

<a name="roll-back-migrate-using-a-single-command"></a>
#### 롤백 및 재마이그레이션 한 번에 실행하기

`migrate:refresh` 명령어는 모든 마이그레이션을 롤백한 뒤 다시 마이그레이션을 실행합니다. 즉, 전체 데이터베이스를 재생성합니다:

```shell
php artisan migrate:refresh

# 데이터베이스를 새로고침 후 시드까지 실행...
php artisan migrate:refresh --seed
```

`step` 옵션을 추가해 지정한 횟수만큼만 롤백 및 재실행할 수도 있습니다:

```shell
php artisan migrate:refresh --step=5
```

<a name="drop-all-tables-migrate"></a>
#### 모든 테이블 삭제 후 마이그레이션

`migrate:fresh` 명령어는 데이터베이스의 모든 테이블을 제거한 다음, 마이그레이션을 실행합니다:

```shell
php artisan migrate:fresh

php artisan migrate:fresh --seed
```

기본적으로, `migrate:fresh` 명령어는 기본 데이터베이스 연결에서만 테이블을 삭제합니다. 하지만, `--database` 옵션으로 마이그레이션을 실행할 데이터베이스 연결을 지정할 수 있습니다. 연결 이름은 애플리케이션의 `database` [설정 파일](/docs/master/configuration)에 정의되어 있어야 합니다:

```shell
php artisan migrate:fresh --database=admin
```

> [!WARNING]
> `migrate:fresh` 명령어는 접두사와 상관없이 모든 테이블을 삭제합니다. 여러 애플리케이션이 같은 데이터베이스를 공유하는 경우, 주의해서 사용하세요.

<a name="tables"></a>
## 테이블 (Tables)

<a name="creating-tables"></a>
### 테이블 생성 (Creating Tables)

새로운 데이터베이스 테이블을 생성하려면 `Schema` 파사드의 `create` 메서드를 사용합니다. `create` 메서드는 첫 번째 인수로 테이블 이름, 두 번째 인수로는 새롭게 생성될 테이블을 정의할 수 있는 `Blueprint` 객체를 받는 클로저를 전달합니다:

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

테이블 생성 시에는, [컬럼 메서드](#creating-columns)를 이용해 컬럼을 자유롭게 정의할 수 있습니다.

<a name="determining-table-column-existence"></a>
#### 테이블/컬럼 존재 여부 확인

테이블, 컬럼 또는 인덱스의 존재 여부는 `hasTable`, `hasColumn`, `hasIndex` 메서드로 확인할 수 있습니다:

```php
if (Schema::hasTable('users')) {
    // "users" 테이블이 존재합니다...
}

if (Schema::hasColumn('users', 'email')) {
    // "users" 테이블이 존재하며 "email" 컬럼도 있습니다...
}

if (Schema::hasIndex('users', ['email'], 'unique')) {
    // "users" 테이블의 "email" 컬럼에 유니크 인덱스가 존재합니다...
}
```

<a name="database-connection-table-options"></a>
#### 데이터베이스 연결 및 테이블 옵션

애플리케이션의 기본 데이터베이스 연결이 아닌 곳에서 스키마 작업을 수행하고 싶다면, `connection` 메서드를 사용하면 됩니다:

```php
Schema::connection('sqlite')->create('users', function (Blueprint $table) {
    $table->id();
});
```

그 밖에도 다양한 속성 및 메서드로 테이블 생성시 옵션을 추가할 수 있습니다. MariaDB 또는 MySQL에서 테이블의 저장 엔진을 지정하려면 `engine` 속성을 사용합니다:

```php
Schema::create('users', function (Blueprint $table) {
    $table->engine('InnoDB');

    // ...
});
```

MariaDB 또는 MySQL에서 테이블의 문자셋과 정렬 방식을 지정하려면 `charset`과 `collation` 속성을 사용합니다:

```php
Schema::create('users', function (Blueprint $table) {
    $table->charset('utf8mb4');
    $table->collation('utf8mb4_unicode_ci');

    // ...
});
```

테이블을 임시(temporary)로 생성하려면 `temporary` 메서드를 사용하세요. 임시 테이블은 현재 데이터베이스 세션에서만 보이고, 연결이 종료되면 자동 삭제됩니다:

```php
Schema::create('calculations', function (Blueprint $table) {
    $table->temporary();

    // ...
});
```

테이블에 "설명(comment)"을 남기고 싶다면, 테이블 인스턴스에서 `comment` 메서드를 호출하세요. 테이블 설명은 현재 MariaDB, MySQL, PostgreSQL에서만 지원됩니다:

```php
Schema::create('calculations', function (Blueprint $table) {
    $table->comment('Business calculations');

    // ...
});
```

<a name="updating-tables"></a>
### 테이블 업데이트 (Updating Tables)

기존 테이블을 업데이트하려면, `Schema` 파사드의 `table` 메서드를 사용합니다. `create`와 마찬가지로 첫 번째 인자는 테이블 이름, 두 번째 인자는 `Blueprint` 인스턴스를 전달받아 컬럼이나 인덱스를 자유롭게 추가할 수 있는 클로저입니다:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->integer('votes');
});
```

<a name="renaming-and-dropping-tables"></a>
### 테이블 이름 변경 / 삭제 (Renaming / Dropping Tables)

기존 데이터베이스 테이블의 이름을 변경하려면 `rename` 메서드를 사용합니다:

```php
use Illuminate\Support\Facades\Schema;

Schema::rename($from, $to);
```

기존 테이블을 삭제하려면 `drop` 또는 `dropIfExists` 메서드를 사용합니다:

```php
Schema::drop('users');

Schema::dropIfExists('users');
```

<a name="renaming-tables-with-foreign-keys"></a>
#### 외래 키가 있는 테이블 이름 변경 주의

테이블 이름을 변경하기 전, 해당 테이블의 외래 키 제약조건 이름이 마이그레이션 파일에서 직접 명시적으로 지정되었는지 꼭 확인해야 합니다. 그렇지 않으면 외래 키 제약조건 이름이 변경 전 테이블 이름을 참조하게 됩니다.

<a name="columns"></a>
## 컬럼 (Columns)

<a name="creating-columns"></a>
### 컬럼 생성 (Creating Columns)

기존 테이블에 컬럼을 추가할 때도 `Schema` 파사드의 `table` 메서드를 사용합니다. `create`와 동일하게 첫 번째 인수로 테이블 이름, 두 번째 인수로는 `Illuminate\Database\Schema\Blueprint`를 전달받는 클로저를 사용하여 컬럼을 추가할 수 있습니다:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->integer('votes');
});
```

<a name="available-column-types"></a>
### 사용 가능한 컬럼 타입 (Available Column Types)

스키마 빌더(Blueprint)는 데이터베이스 테이블에 다양한 컬럼 타입을 추가할 수 있도록 여러 메서드를 제공합니다. 아래 표에서는 사용 가능한 메서드를 모두 나열합니다:

#### 불리언 타입

<div class="collection-method-list" markdown="1">

[boolean](#column-method-boolean)

</div>

#### 문자열과 텍스트 타입

<div class="collection-method-list" markdown="1">

[char](#column-method-char)
[longText](#column-method-longText)
[mediumText](#column-method-mediumText)
[string](#column-method-string)
[text](#column-method-text)
[tinyText](#column-method-tinyText)

</div>

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

#### 날짜와 시간 타입

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

#### 바이너리 타입

<div class="collection-method-list" markdown="1">

[binary](#column-method-binary)

</div>

#### 객체 및 Json 타입

<div class="collection-method-list" markdown="1">

[json](#column-method-json)
[jsonb](#column-method-jsonb)

</div>

#### UUID & ULID 타입

<div class="collection-method-list" markdown="1">

[ulid](#column-method-ulid)
[ulidMorphs](#column-method-ulidMorphs)
[uuid](#column-method-uuid)
[uuidMorphs](#column-method-uuidMorphs)
[nullableUlidMorphs](#column-method-nullableUlidMorphs)
[nullableUuidMorphs](#column-method-nullableUuidMorphs)

</div>

#### 공간(Spatial) 타입

<div class="collection-method-list" markdown="1">

[geography](#column-method-geography)
[geometry](#column-method-geometry)

</div>

#### 연관관계 타입

<div class="collection-method-list" markdown="1">

[foreignId](#column-method-foreignId)
[foreignIdFor](#column-method-foreignIdFor)
[foreignUlid](#column-method-foreignUlid)
[foreignUuid](#column-method-foreignUuid)
[morphs](#column-method-morphs)
[nullableMorphs](#column-method-nullableMorphs)

</div>

#### 특수(Specialty) 타입

<div class="collection-method-list" markdown="1">

[enum](#column-method-enum)
[set](#column-method-set)
[macAddress](#column-method-macAddress)
[ipAddress](#column-method-ipAddress)
[rememberToken](#column-method-rememberToken)
[vector](#column-method-vector)

</div>

#### `bigIncrements()`

`bigIncrements` 메서드는 자동 증가(Primary Key)로 사용되는 `UNSIGNED BIGINT` 컬럼을 만듭니다:

```php
$table->bigIncrements('id');
```

#### `bigInteger()`

`bigInteger` 메서드는 `BIGINT` 컬럼을 생성합니다:

```php
$table->bigInteger('votes');
```

#### `binary()`

`binary` 메서드는 `BLOB` 컬럼을 생성합니다:

```php
$table->binary('photo');
```

MySQL, MariaDB, SQL Server에서는 `length`와 `fixed` 인수를 받아 `VARBINARY` 또는 `BINARY` 컬럼도 만들 수 있습니다:

```php
$table->binary('data', length: 16); // VARBINARY(16)

$table->binary('data', length: 16, fixed: true); // BINARY(16)
```

#### `boolean()`

`boolean` 메서드는 `BOOLEAN` 컬럼을 생성합니다:

```php
$table->boolean('confirmed');
```

#### `char()`

`char` 메서드는 지정한 길이의 `CHAR` 컬럼을 생성합니다:

```php
$table->char('name', length: 100);
```

#### `dateTimeTz()`

`dateTimeTz` 메서드는 시간대 정보를 가진 `DATETIME` 컬럼을 생성하며, 소수 초 정밀도를 선택적으로 지정할 수 있습니다:

```php
$table->dateTimeTz('created_at', precision: 0);
```

#### `dateTime()`

`dateTime` 메서드는 `DATETIME` 컬럼을 생성하며, 소수 초 정밀도를 선택적으로 지정할 수 있습니다:

```php
$table->dateTime('created_at', precision: 0);
```

#### `date()`

`date` 메서드는 `DATE` 컬럼을 생성합니다:

```php
$table->date('created_at');
```

#### `decimal()`

`decimal` 메서드는 지정한 전체 자릿수(precision)와 소수 자릿수(scale)로 `DECIMAL` 컬럼을 생성합니다:

```php
$table->decimal('amount', total: 8, places: 2);
```

#### `double()`

`double` 메서드는 `DOUBLE` 컬럼을 생성합니다:

```php
$table->double('amount');
```

#### `enum()`

`enum` 메서드는 지정한 값만 허용하는 `ENUM` 컬럼을 생성합니다:

```php
$table->enum('difficulty', ['easy', 'hard']);
```

또는, `Enum::cases()`를 사용해서 허용값을 정의할 수도 있습니다:

```php
use App\Enums\Difficulty;

$table->enum('difficulty', Difficulty::cases());
```

#### `float()`

`float` 메서드는 정밀도를 지정한 `FLOAT` 컬럼을 생성합니다:

```php
$table->float('amount', precision: 53);
```

#### `foreignId()`

`foreignId` 메서드는 `UNSIGNED BIGINT` 컬럼을 생성합니다:

```php
$table->foreignId('user_id');
```

#### `foreignIdFor()`

`foreignIdFor` 메서드는 지정한 모델 클래스에 맞는 `{column}_id` 컬럼을 생성합니다. 컬럼 타입은 모델 키 타입에 따라 `UNSIGNED BIGINT`, `CHAR(36)`, `CHAR(26)` 중 하나입니다:

```php
$table->foreignIdFor(User::class);
```

#### `foreignUlid()`

`foreignUlid` 메서드는 `ULID` 컬럼을 생성합니다:

```php
$table->foreignUlid('user_id');
```

#### `foreignUuid()`

`foreignUuid` 메서드는 `UUID` 컬럼을 생성합니다:

```php
$table->foreignUuid('user_id');
```

#### `geography()`

`geography` 메서드는 주어진 공간 타입과 SRID(좌표계 식별자)로 `GEOGRAPHY` 컬럼을 생성합니다:

```php
$table->geography('coordinates', subtype: 'point', srid: 4326);
```

> [!NOTE]
> 공간 타입 지원 여부는 데이터베이스 드라이버에 따라 다릅니다. PostgreSQL을 사용할 경우, 먼저 [PostGIS](https://postgis.net) 확장 기능을 설치해야 합니다.

#### `geometry()`

`geometry` 메서드는 주어진 공간 타입과 SRID로 `GEOMETRY` 컬럼을 생성합니다:

```php
$table->geometry('positions', subtype: 'point', srid: 0);
```

> [!NOTE]
> 공간 타입 지원 여부는 데이터베이스 드라이버에 따라 다릅니다. PostgreSQL에서는 [PostGIS](https://postgis.net) 확장 기능 설치가 필요합니다.

#### `id()`

`id` 메서드는 `bigIncrements` 메서드의 별칭입니다. 기본적으로 `id` 컬럼을 생성하지만, 다른 이름을 원할 경우 인수를 넣어 지정할 수 있습니다:

```php
$table->id();
```

#### `increments()`

`increments` 메서드는 Primary Key용 `UNSIGNED INTEGER` 자동 증가 컬럼을 생성합니다:

```php
$table->increments('id');
```

#### `integer()`

`integer` 메서드는 `INTEGER` 컬럼을 생성합니다:

```php
$table->integer('votes');
```

#### `ipAddress()`

`ipAddress` 메서드는 `VARCHAR` 컬럼(일부 데이터베이스에서는 전용 타입)을 생성합니다:

```php
$table->ipAddress('visitor');
```

PostgreSQL에서는 `INET` 컬럼이 생성됩니다.

#### `json()`

`json` 메서드는 `JSON` 컬럼을 생성합니다:

```php
$table->json('options');
```

SQLite에서는 `TEXT` 컬럼으로 생성됩니다.

#### `jsonb()`

`jsonb` 메서드는 `JSONB` 컬럼을 생성합니다:

```php
$table->jsonb('options');
```

SQLite에서는 `TEXT` 컬럼으로 생성됩니다.

#### `longText()`

`longText` 메서드는 `LONGTEXT` 컬럼을 생성합니다:

```php
$table->longText('description');
```

MySQL 또는 MariaDB에서 `binary` 문자셋을 적용하면, `LONGBLOB` 컬럼을 생성할 수 있습니다:

```php
$table->longText('data')->charset('binary'); // LONGBLOB
```

#### `macAddress()`

`macAddress` 메서드는 MAC 주소 저장을 위한 컬럼을 생성합니다. PostgreSQL 등 일부 데이터베이스는 전용 타입을, 그렇지 않은 경우 문자열 컬럼을 사용합니다:

```php
$table->macAddress('device');
```

#### `mediumIncrements()`

`mediumIncrements` 메서드는 Primary Key용 자동 증가 `UNSIGNED MEDIUMINT` 컬럼을 생성합니다:

```php
$table->mediumIncrements('id');
```

#### `mediumInteger()`

`mediumInteger` 메서드는 `MEDIUMINT` 컬럼을 생성합니다:

```php
$table->mediumInteger('votes');
```

#### `mediumText()`

`mediumText` 메서드는 `MEDIUMTEXT` 컬럼을 생성합니다:

```php
$table->mediumText('description');
```

MySQL 또는 MariaDB에서 `binary` 문자셋을 적용하면, `MEDIUMBLOB` 컬럼을 생성할 수 있습니다:

```php
$table->mediumText('data')->charset('binary'); // MEDIUMBLOB
```

#### `morphs()`

`morphs` 메서드는 `{column}_id`와 `{column}_type`이라는 두 컬럼(복합키 사용)을 생성합니다. `{column}_id` 타입은 모델 키에 따라 달라집니다.

이 메서드는 다형성 [Eloquent 연관관계](/docs/master/eloquent-relationships)를 정의할 때 사용합니다. 예를 들어 아래 실행 시 `taggable_id`와 `taggable_type` 컬럼이 생성됩니다:

```php
$table->morphs('taggable');
```

#### `nullableMorphs()`

[morphs](#column-method-morphs)와 동일하나, 생성된 컬럼들이 "NULL 허용"이 됩니다:

```php
$table->nullableMorphs('taggable');
```

#### `nullableUlidMorphs()`

[ulidMorphs](#column-method-ulidMorphs)와 동일하되, 생성된 컬럼이 NULL 허용입니다:

```php
$table->nullableUlidMorphs('taggable');
```

#### `nullableUuidMorphs()`

[uuidMorphs](#column-method-uuidMorphs)와 동일하되, 생성된 컬럼이 NULL 허용입니다:

```php
$table->nullableUuidMorphs('taggable');
```

#### `rememberToken()`

`rememberToken` 메서드는 널 허용 `VARCHAR(100)` 컬럼을 생성하며, 현재 "로그인 상태 유지"용 [인증 토큰](/docs/master/authentication#remembering-users)을 저장합니다:

```php
$table->rememberToken();
```

#### `set()`

`set` 메서드는 지정한 값의 집합을 저장할 수 있는 `SET` 컬럼을 생성합니다:

```php
$table->set('flavors', ['strawberry', 'vanilla']);
```

#### `smallIncrements()`

`smallIncrements` 메서드는 자동 증가 Primary Key용 `UNSIGNED SMALLINT` 컬럼을 생성합니다:

```php
$table->smallIncrements('id');
```

#### `smallInteger()`

`smallInteger` 메서드는 `SMALLINT` 컬럼을 생성합니다:

```php
$table->smallInteger('votes');
```

#### `softDeletesTz()`

`softDeletesTz` 메서드는 널 허용, 시간대 포함 `deleted_at` `TIMESTAMP` 컬럼을 생성합니다(Eloquent의 소프트 삭제 기능 지원):

```php
$table->softDeletesTz('deleted_at', precision: 0);
```

#### `softDeletes()`

`softDeletes` 메서드는 널 허용 `deleted_at` `TIMESTAMP` 컬럼을 생성합니다(Eloquent의 소프트 삭제 기능 지원):

```php
$table->softDeletes('deleted_at', precision: 0);
```

#### `string()`

`string` 메서드는 지정 길이의 `VARCHAR` 컬럼을 생성합니다:

```php
$table->string('name', length: 100);
```

#### `text()`

`text` 메서드는 `TEXT` 컬럼을 생성합니다:

```php
$table->text('description');
```

MySQL 또는 MariaDB에서 `binary` 문자셋을 적용하면, `BLOB` 컬럼을 생성할 수 있습니다:

```php
$table->text('data')->charset('binary'); // BLOB
```

#### `timeTz()`

`timeTz` 메서드는 시간대 정보가 포함된 `TIME` 컬럼을 생성하며, 소수 초 정밀도를 선택적으로 지정할 수 있습니다:

```php
$table->timeTz('sunrise', precision: 0);
```

#### `time()`

`time` 메서드는 소수 초 정밀도를 선택적으로 지정한 `TIME` 컬럼을 생성합니다:

```php
$table->time('sunrise', precision: 0);
```

#### `timestampTz()`

`timestampTz` 메서드는 시간대 정보를 가진 `TIMESTAMP` 컬럼을 생성합니다:

```php
$table->timestampTz('added_at', precision: 0);
```

#### `timestamp()`

`timestamp` 메서드는 소수 초 정밀도를 지정한 `TIMESTAMP` 컬럼을 생성합니다:

```php
$table->timestamp('added_at', precision: 0);
```

#### `timestampsTz()`

`timestampsTz` 메서드는 시간대 정보를 가진 `created_at`, `updated_at` 컬럼을 생성합니다:

```php
$table->timestampsTz(precision: 0);
```

#### `timestamps()`

`timestamps` 메서드는 `created_at`, `updated_at` 컬럼을 생성합니다:

```php
$table->timestamps(precision: 0);
```

#### `tinyIncrements()`

`tinyIncrements` 메서드는 자동 증가 Primary Key용 `UNSIGNED TINYINT` 컬럼을 생성합니다:

```php
$table->tinyIncrements('id');
```

#### `tinyInteger()`

`tinyInteger` 메서드는 `TINYINT` 컬럼을 생성합니다:

```php
$table->tinyInteger('votes');
```

#### `tinyText()`

`tinyText` 메서드는 `TINYTEXT` 컬럼을 생성합니다:

```php
$table->tinyText('notes');
```

MySQL 또는 MariaDB에서 `binary` 문자셋을 적용하면, `TINYBLOB` 컬럼을 생성할 수 있습니다:

```php
$table->tinyText('data')->charset('binary'); // TINYBLOB
```

#### `unsignedBigInteger()`

`unsignedBigInteger` 메서드는 `UNSIGNED BIGINT` 컬럼을 생성합니다:

```php
$table->unsignedBigInteger('votes');
```

#### `unsignedInteger()`

`unsignedInteger` 메서드는 `UNSIGNED INTEGER` 컬럼을 생성합니다:

```php
$table->unsignedInteger('votes');
```

#### `unsignedMediumInteger()`

`unsignedMediumInteger` 메서드는 `UNSIGNED MEDIUMINT` 컬럼을 생성합니다:

```php
$table->unsignedMediumInteger('votes');
```

#### `unsignedSmallInteger()`

`unsignedSmallInteger` 메서드는 `UNSIGNED SMALLINT` 컬럼을 생성합니다:

```php
$table->unsignedSmallInteger('votes');
```

#### `unsignedTinyInteger()`

`unsignedTinyInteger` 메서드는 `UNSIGNED TINYINT` 컬럼을 생성합니다:

```php
$table->unsignedTinyInteger('votes');
```

#### `ulidMorphs()`

`ulidMorphs` 메서드는 다형성 [Eloquent 연관관계](/docs/master/eloquent-relationships)를 위한 두 컬럼(`{column}_id`(CHAR(26)), `{column}_type`(VARCHAR))을 만듭니다.

예:

```php
$table->ulidMorphs('taggable');
```

#### `uuidMorphs()`

`uuidMorphs` 메서드는 정말로 다형성 [Eloquent 연관관계](/docs/master/eloquent-relationships#polymorphic-relationships)를 위한 두 컬럼(`{column}_id`(CHAR(36)), `{column}_type`)을 만듭니다.

예:

```php
$table->uuidMorphs('taggable');
```

#### `ulid()`

`ulid` 메서드는 `ULID` 컬럼을 생성합니다:

```php
$table->ulid('id');
```

#### `uuid()`

`uuid` 메서드는 `UUID` 컬럼을 생성합니다:

```php
$table->uuid('id');
```

#### `vector()`

`vector` 메서드는 `vector` 컬럼을 생성합니다:

```php
$table->vector('embedding', dimensions: 100);
```

#### `year()`

`year` 메서드는 `YEAR` 컬럼을 생성합니다:

```php
$table->year('birth_year');
```

<a name="column-modifiers"></a>
### 컬럼 수정자 (Column Modifiers)

앞서 설명한 컬럼 타입 외에도, 컬럼을 다룰 때 여러 "수정자(modifier)"를 사용할 수 있습니다. 이를 통해, 예를 들어 컬럼을 "NULL 허용"으로 지정할 수 있습니다:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->string('email')->nullable();
});
```

아래 표는 사용 가능한 모든 컬럼 수정자입니다. ([인덱스 수정자](#creating-indexes)는 포함하지 않습니다.)

<div class="overflow-auto">

| 수정자                                 | 설명                                                                                      |
| ------------------------------------- | -------------------------------------------------------------------------------------- |
| `->after('column')`                   | 다른 컬럼 뒤에 컬럼을 배치(MariaDB / MySQL).                                              |
| `->autoIncrement()`                   | `INTEGER` 컬럼을 자동 증가(Primary Key)로 설정.                                            |
| `->charset('utf8mb4')`                | 컬럼 문자셋 지정(MariaDB / MySQL).                                                       |
| `->collation('utf8mb4_unicode_ci')`   | 컬럼 정렬 방식 지정.                                                                      |
| `->comment('my comment')`             | 컬럼에 주석 추가(MariaDB / MySQL / PostgreSQL).                                           |
| `->default($value)`                   | 컬럼 기본값 지정.                                                                         |
| `->first()`                           | 테이블의 맨 앞에 컬럼 배치(MariaDB / MySQL).                                              |
| `->from($integer)`                    | 자동 증가 필드의 시작값 지정(MariaDB / MySQL / PostgreSQL).                               |
| `->instant()`                         | 인스턴트 알고리즘으로 컬럼 추가/수정(MySQL).                                              |
| `->invisible()`                       | 컬럼을 `SELECT *` 쿼리에서 숨김(MariaDB / MySQL).                                         |
| `->lock($mode)`                       | 컬럼 작업 시 락 모드 지정(MySQL).                                                         |
| `->nullable($value = true)`           | 컬럼에 `NULL` 값 허용.                                                                    |
| `->storedAs($expression)`             | 저장(Stored) 생성 컬럼 생성(MariaDB / MySQL / PostgreSQL / SQLite).                      |
| `->unsigned()`                        | `INTEGER` 컬럼을 `UNSIGNED`로 지정(MariaDB / MySQL).                                      |
| `->useCurrent()`                      | `TIMESTAMP` 컬럼의 기본값을 `CURRENT_TIMESTAMP`로 지정.                                   |
| `->useCurrentOnUpdate()`              | 레코드 수정 시 `CURRENT_TIMESTAMP` 사용(MariaDB / MySQL).                                 |
| `->virtualAs($expression)`            | 가상(Virtual) 생성 컬럼 생성(MariaDB / MySQL / SQLite).                                  |
| `->generatedAs($expression)`          | 시퀀스 옵션과 함께 아이덴티티 컬럼 생성(PostgreSQL).                                      |
| `->always()`                          | 시퀀스 값 입력이 우선(PostgreSQL).                                                        |

</div>

#### 기본값 표현식(Default Expressions)

`default` 수정자는 값 또는 `Illuminate\Database\Query\Expression` 인스턴스를 받을 수 있습니다. Expression 인스턴스를 사용하면 Laravel이 값에 따옴표를 씌우지 않으며, 데이터베이스 고유의 함수도 활용할 수 있습니다. 예를 들어 JSON 컬럼에 기본값을 지정하고 싶을 때 유용합니다:

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
> 기본값 표현식 지원 여부는 데이터베이스 드라이버, 데이터베이스 버전, 필드 타입에 따라 다릅니다. 데이터베이스별 문서를 참고하세요.

#### 컬럼 순서 지정(Column Order)

MariaDB나 MySQL 사용 시, `after` 메서드를 이용해 기존 컬럼 뒤에 컬럼을 추가할 수 있습니다:

```php
$table->after('password', function (Blueprint $table) {
    $table->string('address_line1');
    $table->string('address_line2');
    $table->string('city');
});
```

#### 인스턴트 컬럼 작업(Instant Column Operations)

MySQL에서 컬럼 정의 뒤에 `instant` 수정자를 체이닝하면 인스턴트 알고리즘을 사용해 테이블 재생성 없이 거의 즉시(데이터 양 무관) 컬럼을 추가/수정할 수 있습니다:

```php
$table->string('name')->nullable()->instant();
```

인스턴트 컬럼 추가는 반드시 테이블 맨 끝에 컬럼이 추가되어야 하므로, `after` 또는 `first`와 함께 사용할 수 없습니다. 또한 모든 컬럼 타입/작업이 지원되는 것은 아니니, [MySQL 공식 문서](https://dev.mysql.com/doc/refman/8.0/en/innodb-online-ddl-operations.html)를 참고하세요.

#### DDL 락킹(DDL Locking)

MySQL에서 컬럼, 인덱스, 외래 키 정의에 `lock` 수정자를 붙여 스키마 작업 중 락 모드를 지정할 수 있습니다. `none`(읽기/쓰기 허용), `shared`(읽기만 허용, 쓰기는 차단), `exclusive`(모든 접근 차단), `default`(MySQL이 최적 모드 선택) 중 하나를 지정할 수 있습니다:

```php
$table->string('name')->lock('none');

$table->index('email')->lock('shared');
```

요청한 락 모드가 작업과 호환되지 않으면 MySQL에서 오류가 발생합니다. `instant`와 함께 사용할 수도 있습니다:

```php
$table->string('name')->instant()->lock('none');
```

<a name="modifying-columns"></a>
### 컬럼 수정 (Modifying Columns)

`change` 메서드는 기존 컬럼의 타입 및 속성을 수정할 때 사용합니다. 예를 들어, `name` 컬럼의 크기를 25에서 50으로 늘리고 싶다면, 새 상태를 정의한 후 `change` 메서드를 추가로 체이닝해주면 됩니다:

```php
Schema::table('users', function (Blueprint $table) {
    $table->string('name', 50)->change();
});
```

컬럼을 수정할 때는, 남기고 싶은 수정자를 반드시 명시적으로 모두 포함해야 합니다. 빠진 속성은 사라집니다. 예를 들어, `unsigned`, `default`, `comment` 속성을 유지하려면 각각 체이닝해야합니다:

```php
Schema::table('users', function (Blueprint $table) {
    $table->integer('votes')->unsigned()->default(1)->comment('my comment')->change();
});
```

`change` 메서드는 컬럼의 인덱스는 변경하지 않습니다. 따라서 인덱스를 추가/삭제하려면, 인덱스 수정자를 명시적으로 호출해야 합니다:

```php
// 인덱스 추가...
$table->bigIncrements('id')->primary()->change();

// 인덱스 제거...
$table->char('postal_code', 10)->unique(false)->change();
```

<a name="renaming-columns"></a>
### 컬럼 이름 변경 (Renaming Columns)

컬럼 이름을 바꾸려면, 스키마 빌더의 `renameColumn` 메서드를 사용합니다:

```php
Schema::table('users', function (Blueprint $table) {
    $table->renameColumn('from', 'to');
});
```

<a name="dropping-columns"></a>
### 컬럼 삭제 (Dropping Columns)

컬럼을 삭제하려면, 스키마 빌더의 `dropColumn` 메서드를 사용합니다:

```php
Schema::table('users', function (Blueprint $table) {
    $table->dropColumn('votes');
});
```

여러 컬럼을 한 번에 삭제할 수도 있으며, 컬럼 이름 배열을 전달하면 됩니다:

```php
Schema::table('users', function (Blueprint $table) {
    $table->dropColumn(['votes', 'avatar', 'location']);
});
```

#### 사용 가능한 명령어 별칭(Available Command Aliases)

자주 사용되는 컬럼 삭제 작업을 위한 편의 메서드들이 있습니다. 아래 표를 참고하세요.

<div class="overflow-auto">

| 명령어                              | 설명                                                  |
| ----------------------------------- | ----------------------------------------------------- |
| `$table->dropMorphs('morphable');`  | `morphable_id`, `morphable_type` 컬럼 삭제           |
| `$table->dropRememberToken();`      | `remember_token` 컬럼 삭제                           |
| `$table->dropSoftDeletes();`        | `deleted_at` 컬럼 삭제                               |
| `$table->dropSoftDeletesTz();`      | `dropSoftDeletes()` 메서드의 별칭                     |
| `$table->dropTimestamps();`         | `created_at`, `updated_at` 컬럼 삭제                 |
| `$table->dropTimestampsTz();`       | `dropTimestamps()` 메서드의 별칭                      |

</div>

<a name="indexes"></a>
## 인덱스 (Indexes)

<a name="creating-indexes"></a>
### 인덱스 생성 (Creating Indexes)

Laravel 스키마 빌더는 다양한 인덱스 생성을 지원합니다. 예를 들어, 새로 만든 `email` 컬럼을 유니크하게 하려면 컬럼 정의 뒤에 `unique` 메서드를 체이닝하면 됩니다:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->string('email')->unique();
});
```

또는 컬럼 정의 후에 인덱스를 따로 생성할 수도 있습니다. 이때는 스키마 빌더에서 `unique` 메서드를 호출하며, 인수로 인덱스를 적용할 컬럼명을 지정합니다:

```php
$table->unique('email');
```

여러 컬럼을 묶어 복합(Compound) 인덱스를 만들거나, 배열로 전달해도 됩니다:

```php
$table->index(['account_id', 'created_at']);
```

인덱스 생성 시 Laravel이 자동으로 인덱스 이름을 만들어주지만, 두 번째 인수로 직접 이름을 지정할 수도 있습니다:

```php
$table->unique('email', 'unique_email');
```

#### 사용 가능한 인덱스 타입

Laravel의 스키마 빌더(Blueprint) 클래스는 Laravel이 지원하는 인덱스별로 별도의 메서드를 제공합니다. 각 메서드는 두 번째 인수로 인덱스 이름을 지정할 수 있습니다(생략 시 테이블과 컬럼, 타입 정보를 기반으로 자동 생성). 아래 표를 참고하세요:

<div class="overflow-auto">

| 명령어                                         | 설명                                                                      |
| --------------------------------------------- | ----------------------------------------------------------------------- |
| `$table->primary('id');`                      | 기본키 추가                                                              |
| `$table->primary(['id', 'parent_id']);`       | 복합키(Composite) 추가                                                   |
| `$table->unique('email');`                    | 유니크 인덱스 추가                                                       |
| `$table->index('state');`                     | 일반 인덱스 추가                                                         |
| `$table->fullText('body');`                   | 전체 텍스트 인덱스 추가(MariaDB / MySQL / PostgreSQL)                    |
| `$table->fullText('body')->language('english');` | 특정 언어 전체 텍스트 인덱스(PostgreSQL)                                 |
| `$table->spatialIndex('location');`           | 공간 인덱스 추가(SQLite 제외)                                            |

</div>

#### 온라인 인덱스 생성(Online Index Creation)

기본적으로, 대용량 테이블에 인덱스를 만들면 테이블이 잠기고, 인덱스가 생성되는 동안 읽기/쓰기가 모두 차단됩니다. PostgreSQL이나 SQL Server를 사용할 때, 인덱스 정의에 `online` 메서드를 추가하면 테이블 잠금 없이 인덱스를 만들 수 있습니다:

```php
$table->string('email')->unique()->online();
```

PostgreSQL에서는 `CONCURRENTLY`, SQL Server에서는 `WITH (online = on)` 옵션이 추가됩니다.

<a name="renaming-indexes"></a>
### 인덱스 이름 변경 (Renaming Indexes)

인덱스 이름을 변경하려면, 스키마 빌더(Blueprint)의 `renameIndex` 메서드를 사용합니다. 첫 번째 인수로 현재 인덱스 이름, 두 번째로 새 이름을 지정합니다:

```php
$table->renameIndex('from', 'to')
```

<a name="dropping-indexes"></a>
### 인덱스 삭제 (Dropping Indexes)

인덱스 삭제 시, 인덱스 이름을 지정해야 합니다. Laravel은 기본적으로 테이블/컬럼/인덱스 타입을 조합하여 자동으로 인덱스 이름을 생성합니다. 예시는 다음과 같습니다:

<div class="overflow-auto">

| 명령어                                                | 설명                                              |
| --------------------------------------------------- | ------------------------------------------------ |
| `$table->dropPrimary('users_id_primary');`          | "users" 테이블에서 기본키 삭제                   |
| `$table->dropUnique('users_email_unique');`         | "users" 테이블에서 유니크 인덱스 삭제            |
| `$table->dropIndex('geo_state_index');`             | "geo" 테이블 일반 인덱스 삭제                    |
| `$table->dropFullText('posts_body_fulltext');`      | "posts" 테이블의 전체 텍스트 인덱스 삭제         |
| `$table->dropSpatialIndex('geo_location_spatialindex');` | "geo" 테이블(Spatial 인덱스, SQLite 제외) 삭제  |

</div>

인덱스 삭제 메서드에 컬럼 배열을 전달하면, 지정한 표준 규칙에 따라 인덱스 이름을 자동 생성해 삭제합니다:

```php
Schema::table('geo', function (Blueprint $table) {
    $table->dropIndex(['state']); // 'geo_state_index' 인덱스 삭제
});
```

<a name="foreign-key-constraints"></a>
### 외래 키 제약조건 (Foreign Key Constraints)

Laravel은 데이터베이스 레벨에서 참조 무결성을 보장하는 외래 키 제약조건 생성도 지원합니다. 예를 들어, `posts` 테이블의 `user_id` 컬럼이 `users` 테이블의 `id` 컬럼을 참조하도록 정의하려면 다음과 같이 작성합니다:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('posts', function (Blueprint $table) {
    $table->unsignedBigInteger('user_id');

    $table->foreign('user_id')->references('id')->on('users');
});
```

위 코드가 다소 장황하기 때문에, Laravel은 보다 간결한 메서드 체이닝 방식을 제공합니다. `foreignId`로 컬럼 생성 후 `constrained` 메서드를 추가하면 됩니다:

```php
Schema::table('posts', function (Blueprint $table) {
    $table->foreignId('user_id')->constrained();
});
```

`foreignId`는 `UNSIGNED BIGINT` 컬럼을 만들며, `constrained`은 규칙에 따라 참조할 테이블과 컬럼을 자동으로 지정합니다. 규칙이 맞지 않는 경우, 직접 테이블과 인덱스명을 지정할 수 있습니다:

```php
Schema::table('posts', function (Blueprint $table) {
    $table->foreignId('user_id')->constrained(
        table: 'users', indexName: 'posts_user_id'
    );
});
```

또한, on delete, on update 속성에 원하는 작업을 지정할 수 있습니다:

```php
$table->foreignId('user_id')
    ->constrained()
    ->onUpdate('cascade')
    ->onDelete('cascade');
```

동일한 효과를 내는 별도의 메서드들도 있습니다:

<div class="overflow-auto">

| 메서드                         | 설명                                                 |
| ----------------------------- | -------------------------------------------------- |
| `$table->cascadeOnUpdate();`  | 업데이트 시 참조 대상까지 함께 수정                   |
| `$table->restrictOnUpdate();` | 업데이트 제한                                        |
| `$table->nullOnUpdate();`     | 업데이트 시 외래 키 값을 NULL로 설정                 |
| `$table->noActionOnUpdate();` | 업데이트 시 아무 동작도 하지 않음                    |
| `$table->cascadeOnDelete();`  | 삭제 시 참조 대상까지 함께 삭제                      |
| `$table->restrictOnDelete();` | 삭제 제한                                            |
| `$table->nullOnDelete();`     | 삭제 시 외래 키 값을 NULL로 설정                     |
| `$table->noActionOnDelete();` | 하위 레코드 존재 시 삭제 금지                       |

</div>

[컬럼 수정자](#column-modifiers)는 반드시 `constrained` 이전에 호출해야 합니다:

```php
$table->foreignId('user_id')
    ->nullable()
    ->constrained();
```

#### 외래 키 삭제 (Dropping Foreign Keys)

외래 키 제약조건을 삭제하려면, `dropForeign` 메서드에 삭제할 외래 키 제약조건 이름을 전달하면 됩니다. 이름 규칙은 인덱스와 동일하게, 테이블명과 컬럼명을 조합한 후 `_foreign`을 붙입니다:

```php
$table->dropForeign('posts_user_id_foreign');
```

또는, 외래 키 컬럼명을 배열로 넘기면 Laravel의 규칙으로 자동 변환해 삭제합니다:

```php
$table->dropForeign(['user_id']);
```

#### 외래 키 제약조건 활성화/비활성화 (Toggling Foreign Key Constraints)

마이그레이션 중에서는 외래 키 활성화/비활성화를 아래와 같이 할 수 있습니다:

```php
Schema::enableForeignKeyConstraints();

Schema::disableForeignKeyConstraints();

Schema::withoutForeignKeyConstraints(function () {
    // 이 클로저 블록 내에서는 외래 키 제약조건이 비활성화됨...
});
```

> [!WARNING]
> SQLite는 기본적으로 외래 키 제약조건을 비활성화합니다. SQLite를 사용할 경우, 마이그레이션에서 외래 키를 만들기 전에 [외래 키 지원](/docs/master/database#configuration)을 활성화해야 합니다.

<a name="events"></a>
## 이벤트 (Events)

편의 기능으로, 각 마이그레이션 작업 시 [이벤트](/docs/master/events)가 디스패치됩니다. 아래 모든 이벤트는 기본 클래스인 `Illuminate\Database\Events\MigrationEvent`를 상속받습니다:

<div class="overflow-auto">

| 클래스                                            | 설명                                                 |
| ------------------------------------------------ | -------------------------------------------------- |
| `Illuminate\Database\Events\MigrationsStarted`   | 여러 마이그레이션 배치 실행 시작 시                  |
| `Illuminate\Database\Events\MigrationsEnded`     | 여러 마이그레이션 배치 실행 종료 시                  |
| `Illuminate\Database\Events\MigrationStarted`    | 하나의 마이그레이션 실행 시작 시                    |
| `Illuminate\Database\Events\MigrationEnded`      | 하나의 마이그레이션 실행 종료 시                    |
| `Illuminate\Database\Events\NoPendingMigrations` | 남은 마이그레이션이 없을 때                        |
| `Illuminate\Database\Events\SchemaDumped`        | 데이터베이스 스키마 덤프 완료 시                   |
| `Illuminate\Database\Events\SchemaLoaded`        | 기존 데이터베이스 스키마 덤프(loadd) 시             |

</div>
