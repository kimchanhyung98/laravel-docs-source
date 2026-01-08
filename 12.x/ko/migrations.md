# 데이터베이스: 마이그레이션 (Database: Migrations)

- [소개](#introduction)
- [마이그레이션 생성](#generating-migrations)
    - [마이그레이션 스쿼싱](#squashing-migrations)
- [마이그레이션 구조](#migration-structure)
- [마이그레이션 실행](#running-migrations)
    - [마이그레이션 롤백](#rolling-back-migrations)
- [테이블](#tables)
    - [테이블 생성](#creating-tables)
    - [테이블 수정](#updating-tables)
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

마이그레이션은 데이터베이스의 버전 관리를 가능하게 하여, 팀이 애플리케이션의 데이터베이스 스키마 정의를 명확하게 정의하고 공유할 수 있게 합니다. 만약 당신이 동료에게 소스 컨트롤에서 변경사항을 반영한 후, 직접 데이터베이스에 컬럼을 수동으로 추가하라고 부탁했던 경험이 있다면, 이것이 바로 마이그레이션이 해결하는 문제입니다.

Laravel의 `Schema` [파사드](/docs/12.x/facades)는 모든 Laravel 지원 데이터베이스 시스템에서 데이터베이스에 독립적인 방식으로 테이블을 생성하고 조작할 수 있도록 지원합니다. 일반적으로 마이그레이션은 이 파사드를 사용하여 데이터베이스 테이블과 컬럼을 생성하고 수정합니다.

<a name="generating-migrations"></a>
## 마이그레이션 생성 (Generating Migrations)

`make:migration` [Artisan 명령어](/docs/12.x/artisan)를 사용하여 데이터베이스 마이그레이션을 생성할 수 있습니다. 새 마이그레이션 파일은 `database/migrations` 디렉터리에 생성됩니다. 각 마이그레이션 파일 이름에는 타임스탬프가 포함되어 있어, Laravel이 마이그레이션의 순서를 결정할 수 있습니다.

```shell
php artisan make:migration create_flights_table
```

Laravel은 마이그레이션 이름을 활용해 어떤 테이블을 다루고 있는지, 그리고 새 테이블을 생성하는 마이그레이션인지 추측하려 시도합니다. Laravel이 마이그레이션 이름에서 테이블 이름을 파악할 수 있으면, 미리 지정된 테이블명이 생성된 마이그레이션 파일에 자동으로 채워집니다. 그렇지 않은 경우, 마이그레이션 파일에서 직접 테이블을 지정하면 됩니다.

마이그레이션 생성 시 커스텀 경로를 지정하고 싶다면, `make:migration` 명령어를 실행할 때 `--path` 옵션을 사용할 수 있습니다. 지정한 경로는 애플리케이션의 기본 경로 기준 상대 경로여야 합니다.

> [!NOTE]
> 마이그레이션 스텁은 [스텁 퍼블리싱](/docs/12.x/artisan#stub-customization) 기능을 사용해 커스터마이즈할 수 있습니다.

<a name="squashing-migrations"></a>
### 마이그레이션 스쿼싱 (Squashing Migrations)

애플리케이션을 개발하다 보면 `database/migrations` 디렉터리에 수 많은 마이그레이션 파일이 쌓일 수 있습니다. 이처럼 마이그레이션 수가 많아지면 관리가 번거로워질 수 있습니다. 이럴 때는 마이그레이션을 하나의 SQL 파일로 "스쿼싱(Squash)"할 수 있습니다. 먼저, `schema:dump` 명령어를 실행하세요.

```shell
php artisan schema:dump

# 현재 데이터베이스 스키마를 덤프하고, 모든 기존 마이그레이션 파일을 정리합니다...
php artisan schema:dump --prune
```

이 명령어를 실행하면, Laravel은 애플리케이션의 `database/schema` 디렉터리에 "스키마" 파일을 생성합니다. 이 파일의 이름은 사용하는 데이터베이스 커넥션에 따라 결정됩니다. 그리고 데이터베이스에 아직 적용된 마이그레이션이 없다면, 이 스키마 파일의 SQL 문장이 우선 실행됩니다. 스키마 파일 실행 후에는 이 덤프에 포함되지 않은 나머지 마이그레이션이 순차적으로 실행됩니다.

만약 테스트에서 로컬 개발 때와는 다른 데이터베이스 커넥션을 사용한다면, 테스트용 데이터베이스 커넥션으로도 스키마 파일을 반드시 덤프하여 테스트 시에도 데이터베이스를 정상적으로 구축할 수 있도록 해야 합니다. 일반적으로 로컬 개발용 커넥션으로 덤프한 후 아래처럼 별도 덤프를 진행할 수 있습니다.

```shell
php artisan schema:dump
php artisan schema:dump --database=testing --prune
```

이 데이터베이스 스키마 파일은 소스 컨트롤에 반드시 커밋해야 하며, 이를 통해 새롭게 프로젝트에 합류한 개발자가 빠르게 초기 데이터베이스 구조를 구축할 수 있습니다.

> [!WARNING]
> 마이그레이션 스쿼싱은 MariaDB, MySQL, PostgreSQL, SQLite 데이터베이스에서만 사용할 수 있으며, 각각의 데이터베이스의 명령줄 클라이언트를 활용합니다.

<a name="migration-structure"></a>
## 마이그레이션 구조 (Migration Structure)

마이그레이션 클래스는 `up`과 `down` 두 메서드를 가집니다. `up` 메서드는 새 테이블, 컬럼, 인덱스 등을 데이터베이스에 추가할 때 사용합니다. 반대로 `down` 메서드는 `up` 메서드에서 수행한 작업을 되돌릴 때 사용합니다.

이 두 메서드 안에서는 Laravel의 스키마 빌더를 활용해 테이블을 손쉽게 생성 및 수정할 수 있습니다. 스키마 빌더의 다양한 메서드에 대해 더 알아보고자 한다면, [관련 문서](#creating-tables)를 참조하세요. 아래 예시는 `flights` 테이블을 생성하는 마이그레이션입니다.

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
#### 마이그레이션 커넥션 설정

마이그레이션이 애플리케이션의 기본 데이터베이스 커넥션이 아닌 다른 커넥션을 사용할 경우, 마이그레이션 클래스의 `$connection` 프로퍼티를 설정해야 합니다.

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

특정 마이그레이션이 아직 활성화되지 않은 기능을 지원하기 위한 것이라 당장 실행하고 싶지 않은 경우, 마이그레이션 클래스에 `shouldRun` 메서드를 정의할 수 있습니다. 이 메서드가 `false`를 반환하면 해당 마이그레이션은 건너뜁니다.

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

적용되지 않은 모든 마이그레이션을 실행하려면, `migrate` Artisan 명령어를 사용하세요.

```shell
php artisan migrate
```

이미 실행된 마이그레이션과 아직 적용되지 않은 마이그레이션을 확인하려면, `migrate:status` Artisan 명령어를 사용하세요.

```shell
php artisan migrate:status
```

실제로 마이그레이션을 실행하지 않고, 실행될 SQL 문장만 확인하고 싶다면 `--pretend` 플래그를 사용합니다.

```shell
php artisan migrate --pretend
```

<a name="isolating-migration-execution"></a>
#### 마이그레이션 실행 격리

여러 서버에 애플리케이션을 배포하고 배포 과정에서 마이그레이션을 실행하는 경우, 두 서버에서 동시에 마이그레이션이 실행되는 상황을 피하고 싶을 수 있습니다. 이를 방지하려면, `migrate` 명령에 `--isolated` 옵션을 추가할 수 있습니다.

이 옵션을 사용하면, Laravel은 마이그레이션 실행 전 애플리케이션의 캐시 드라이버를 이용해 원자적(atomic) 락을 획득합니다. 락이 유지되는 동안 다른 서버에서 `migrate` 명령이 실행될 경우, 내부적으로 실행되지 않고 성공 코드로 종료합니다.

```shell
php artisan migrate --isolated
```

> [!WARNING]
> 이 기능을 사용하려면, 기본 캐시 드라이버로 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 중 하나를 사용해야 합니다. 또한, 모든 서버가 동일한 중앙 캐시 서버와 통신하도록 설정되어야 합니다.

<a name="forcing-migrations-to-run-in-production"></a>
#### 프로덕션 환경에서 마이그레이션 강제 실행

일부 마이그레이션 명령은 데이터를 잃을 수 있는 위험한 작업입니다. 이런 명령은 프로덕션 데이터베이스에 바로 실행되지 않도록, 명령 실행 전 확인 절차가 진행됩니다. 확인 없이 명령어를 강제로 실행하려면 `--force` 플래그를 사용하세요.

```shell
php artisan migrate --force
```

<a name="rolling-back-migrations"></a>
### 마이그레이션 롤백 (Rolling Back Migrations)

가장 최근의 마이그레이션 동작을 롤백하려면 `rollback` Artisan 명령어를 사용하세요. 이 명령어는 마지막 "배치(batch)"의 마이그레이션 파일을 한 번에 롤백합니다.

```shell
php artisan migrate:rollback
```

`step` 옵션을 지정하면, 최근 N개의 마이그레이션만 롤백할 수 있습니다. 예시:

```shell
php artisan migrate:rollback --step=5
```

`batch` 옵션을 사용해 특정 배치에 속한 마이그레이션만 롤백할 수도 있습니다. 예시(command는 `migrations` 테이블의 batch 값과 일치):

```shell
php artisan migrate:rollback --batch=3
```

마이그레이션을 실행하지 않고 롤백될 SQL 문장만 보고 싶다면 `--pretend` 플래그를 사용할 수 있습니다.

```shell
php artisan migrate:rollback --pretend
```

`migrate:reset` 명령어는 애플리케이션의 모든 마이그레이션을 전부 롤백합니다.

```shell
php artisan migrate:reset
```

<a name="roll-back-migrate-using-a-single-command"></a>
#### 단일 명령어로 롤백 및 재마이그레이션

`migrate:refresh` 명령어를 사용하면, 전체 마이그레이션을 롤백한 뒤 다시 모두 실행합니다. 즉, 데이터베이스를 완전히 새로 만듭니다.

```shell
php artisan migrate:refresh

# 데이터베이스를 새로 만들고, 모든 데이터베이스 시드를 실행합니다...
php artisan migrate:refresh --seed
```

`step` 옵션을 지정하면 최근 N개의 마이그레이션만 롤백 및 재실행할 수 있습니다.

```shell
php artisan migrate:refresh --step=5
```

<a name="drop-all-tables-migrate"></a>
#### 모든 테이블 삭제 및 마이그레이션

`migrate:fresh` 명령어는 데이터베이스의 모든 테이블을 삭제한 후 다시 마이그레이션을 실행합니다.

```shell
php artisan migrate:fresh

php artisan migrate:fresh --seed
```

기본적으로 `migrate:fresh` 명령어는 기본 데이터베이스 커넥션의 테이블만 삭제합니다. 그러나 `--database` 옵션을 사용해 마이그레이션할 데이터베이스 커넥션을 지정할 수 있습니다. 이 때 커넥션명은 애플리케이션 `database` [설정 파일](/docs/12.x/configuration)에 정의되어 있는 값이어야 합니다.

```shell
php artisan migrate:fresh --database=admin
```

> [!WARNING]
> `migrate:fresh` 명령어는 테이블의 접두어와 관계없이 모든 데이터베이스 테이블을 삭제합니다. 다른 애플리케이션과 데이터베이스를 공유하는 상태라면 신중히 사용해야 합니다.

<a name="tables"></a>
## 테이블 (Tables)

<a name="creating-tables"></a>
### 테이블 생성 (Creating Tables)

새 데이터베이스 테이블을 생성하려면 `Schema` 파사드의 `create` 메서드를 사용하세요. `create` 메서드는 두 개의 인자를 받습니다: 첫 번째는 테이블명이며, 두 번째는 새 테이블을 정의할 수 있는 `Blueprint` 객체를 인자로 받는 클로저입니다.

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

테이블을 생성할 때, 스키마 빌더의 모든 [컬럼 메서드](#creating-columns)를 사용할 수 있습니다.

<a name="determining-table-column-existence"></a>
#### 테이블/컬럼 존재 여부 확인

`hasTable`, `hasColumn`, `hasIndex` 메서드를 사용해서 테이블, 컬럼, 인덱스의 존재 여부를 확인할 수 있습니다.

```php
if (Schema::hasTable('users')) {
    // "users" 테이블이 존재합니다...
}

if (Schema::hasColumn('users', 'email')) {
    // "users" 테이블에 "email" 컬럼이 존재합니다...
}

if (Schema::hasIndex('users', ['email'], 'unique')) {
    // "users" 테이블에 "email" 컬럼의 유니크 인덱스가 존재합니다...
}
```

<a name="database-connection-table-options"></a>
#### 데이터베이스 커넥션 및 테이블 옵션

기본 데이터베이스 커넥션이 아닌 다른 커넥션에서 스키마 작업을 수행하려면 `connection` 메서드를 사용하세요.

```php
Schema::connection('sqlite')->create('users', function (Blueprint $table) {
    $table->id();
});
```

그 밖에도 테이블 생성 방식에 따라 다양한 프로퍼티와 메서드를 사용할 수 있습니다. MariaDB나 MySQL을 사용할 때는, `engine` 프로퍼티로 테이블의 저장 엔진을 지정할 수 있습니다.

```php
Schema::create('users', function (Blueprint $table) {
    $table->engine('InnoDB');

    // ...
});
```

MariaDB나 MySQL에서 테이블 생성시 문자셋 및 콜레이션을 지정하고 싶다면 `charset`과 `collation` 프로퍼티를 사용할 수 있습니다.

```php
Schema::create('users', function (Blueprint $table) {
    $table->charset('utf8mb4');
    $table->collation('utf8mb4_unicode_ci');

    // ...
});
```

테이블을 "임시(Temporary)"로 지정하고 싶을 때는 `temporary` 메서드를 사용합니다. 임시 테이블은 현재 커넥션의 세션에서만 접근 가능하며, 커넥션이 종료될 때 자동으로 삭제됩니다.

```php
Schema::create('calculations', function (Blueprint $table) {
    $table->temporary();

    // ...
});
```

테이블에 "주석(comment)"을 추가하려면 `comment` 메서드를 사용할 수 있습니다. 테이블 주석은 현재 MariaDB, MySQL, PostgreSQL에서만 지원됩니다.

```php
Schema::create('calculations', function (Blueprint $table) {
    $table->comment('Business calculations');

    // ...
});
```

<a name="updating-tables"></a>
### 테이블 수정 (Updating Tables)

기존 테이블을 수정하려면, `Schema` 파사드의 `table` 메서드를 사용합니다. 이 메서드 역시 테이블명과 `Blueprint` 인스턴스를 받는 클로저를 인자로 사용합니다. 여기에서 컬럼이나 인덱스를 추가할 수 있습니다.

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->integer('votes');
});
```

<a name="renaming-and-dropping-tables"></a>
### 테이블 이름 변경/삭제 (Renaming / Dropping Tables)

기존 데이터베이스 테이블의 이름을 변경하려면 `rename` 메서드를 사용하세요.

```php
use Illuminate\Support\Facades\Schema;

Schema::rename($from, $to);
```

기존 테이블을 삭제하려면, `drop` 또는 `dropIfExists` 메서드를 사용할 수 있습니다.

```php
Schema::drop('users');

Schema::dropIfExists('users');
```

<a name="renaming-tables-with-foreign-keys"></a>
#### 외래 키가 있는 테이블 이름 변경

테이블 이름을 변경하기 전에, 해당 테이블의 외래 키 제약조건이 마이그레이션 파일에서 명시적 이름을 갖고 있는지 확인해야 합니다. 이름을 지정하지 않고 Laravel이 관례적인 이름을 자동으로 할당하게 둔다면, 외래 키 제약조건 이름이 이전 테이블명을 가리키게 됩니다.

<a name="columns"></a>
## 컬럼 (Columns)

<a name="creating-columns"></a>
### 컬럼 생성 (Creating Columns)

기존 테이블에 컬럼을 추가하려면 `Schema` 파사드의 `table` 메서드를 사용합니다. `create` 메서드와 마찬가지로, 테이블명과 `Illuminate\Database\Schema\Blueprint` 인스턴스를 인수로 받는 클로저를 전달할 수 있습니다.

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->integer('votes');
});
```

<a name="available-column-types"></a>
### 사용 가능한 컬럼 타입 (Available Column Types)

스키마 빌더의 Blueprint 객체는 데이터베이스 테이블에 추가할 수 있는 다양한 컬럼 타입 생성 메서드를 제공합니다. 아래 표에는 사용 가능한 모든 메서드가 정리되어 있습니다.

#### 불리언 타입

- [boolean](#column-method-boolean)

#### 문자열 및 텍스트 타입

- [char](#column-method-char)
- [longText](#column-method-longText)
- [mediumText](#column-method-mediumText)
- [string](#column-method-string)
- [text](#column-method-text)
- [tinyText](#column-method-tinyText)

#### 숫자 타입

- [bigIncrements](#column-method-bigIncrements)
- [bigInteger](#column-method-bigInteger)
- [decimal](#column-method-decimal)
- [double](#column-method-double)
- [float](#column-method-float)
- [id](#column-method-id)
- [increments](#column-method-increments)
- [integer](#column-method-integer)
- [mediumIncrements](#column-method-mediumIncrements)
- [mediumInteger](#column-method-mediumInteger)
- [smallIncrements](#column-method-smallIncrements)
- [smallInteger](#column-method-smallInteger)
- [tinyIncrements](#column-method-tinyIncrements)
- [tinyInteger](#column-method-tinyInteger)
- [unsignedBigInteger](#column-method-unsignedBigInteger)
- [unsignedInteger](#column-method-unsignedInteger)
- [unsignedMediumInteger](#column-method-unsignedMediumInteger)
- [unsignedSmallInteger](#column-method-unsignedSmallInteger)
- [unsignedTinyInteger](#column-method-unsignedTinyInteger)

#### 날짜 및 시간 타입

- [dateTime](#column-method-dateTime)
- [dateTimeTz](#column-method-dateTimeTz)
- [date](#column-method-date)
- [time](#column-method-time)
- [timeTz](#column-method-timeTz)
- [timestamp](#column-method-timestamp)
- [timestamps](#column-method-timestamps)
- [timestampsTz](#column-method-timestampsTz)
- [softDeletes](#column-method-softDeletes)
- [softDeletesTz](#column-method-softDeletesTz)
- [year](#column-method-year)

#### 바이너리 타입

- [binary](#column-method-binary)

#### 오브젝트 & JSON 타입

- [json](#column-method-json)
- [jsonb](#column-method-jsonb)

#### UUID & ULID 타입

- [ulid](#column-method-ulid)
- [ulidMorphs](#column-method-ulidMorphs)
- [uuid](#column-method-uuid)
- [uuidMorphs](#column-method-uuidMorphs)
- [nullableUlidMorphs](#column-method-nullableUlidMorphs)
- [nullableUuidMorphs](#column-method-nullableUuidMorphs)

#### 공간(Spatial) 타입

- [geography](#column-method-geography)
- [geometry](#column-method-geometry)

#### 연관관계 타입

- [foreignId](#column-method-foreignId)
- [foreignIdFor](#column-method-foreignIdFor)
- [foreignUlid](#column-method-foreignUlid)
- [foreignUuid](#column-method-foreignUuid)
- [morphs](#column-method-morphs)
- [nullableMorphs](#column-method-nullableMorphs)

#### 특수 타입

- [enum](#column-method-enum)
- [set](#column-method-set)
- [macAddress](#column-method-macAddress)
- [ipAddress](#column-method-ipAddress)
- [rememberToken](#column-method-rememberToken)
- [vector](#column-method-vector)

각 메서드의 구체적인 사용법 및 예제는 원문의 해당 앵커에서 확인할 수 있습니다.

<a name="column-modifiers"></a>
### 컬럼 수정자 (Column Modifiers)

앞서 소개한 컬럼 타입 외에도, 컬럼에 다양한 "수정자(Modifier)"를 사용할 수 있습니다. 예를 들어, 컬럼을 "nullable"로 지정하려면 `nullable` 메서드를 연결해서 사용할 수 있습니다.

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->string('email')->nullable();
});
```

아래 표는 모든 사용 가능한 컬럼 수정자를 정리한 것입니다. 단, [인덱스 수정자](#creating-indexes)는 이 표에 포함되어 있지 않습니다.

| Modifier                            | 설명                                                                                 |
| ----------------------------------- | ------------------------------------------------------------------------------------ |
| `->after('column')`                 | 다른 컬럼 뒤에 추가 (MariaDB / MySQL)                                                |
| `->autoIncrement()`                 | `INTEGER` 컬럼을 자동 증가(primary key)로 지정                                        |
| `->charset('utf8mb4')`              | 컬럼의 문자셋 지정 (MariaDB / MySQL)                                                 |
| `->collation('utf8mb4_unicode_ci')` | 컬럼의 콜레이션 지정                                                                 |
| `->comment('my comment')`           | 컬럼에 주석 추가 (MariaDB / MySQL / PostgreSQL)                                      |
| `->default($value)`                 | 컬럼의 "기본값" 지정                                                                 |
| `->first()`                         | 테이블에서 컬럼을 맨 앞에 배치 (MariaDB / MySQL)                                     |
| `->from($integer)`                  | 자동 증가 필드의 시작값 지정 (MariaDB / MySQL / PostgreSQL)                          |
| `->instant()`                       | 컬럼 추가/수정을 instant 알고리즘으로 처리 (MySQL)                                   |
| `->invisible()`                     | `SELECT *` 쿼리 결과에서 컬럼을 숨김 (MariaDB / MySQL)                               |
| `->lock($mode)`                     | 컬럼 작업 시 락 모드 지정 (MySQL)                                                    |
| `->nullable($value = true)`         | 컬럼에 `NULL` 값 허용                                                                |
| `->storedAs($expression)`           | 저장된 생성 컬럼 생성 (MariaDB / MySQL / PostgreSQL / SQLite)                        |
| `->unsigned()`                      | `INTEGER` 컬럼을 `UNSIGNED`로 지정 (MariaDB / MySQL)                                 |
| `->useCurrent()`                    | `TIMESTAMP` 컬럼의 기본값을 `CURRENT_TIMESTAMP`로 지정                               |
| `->useCurrentOnUpdate()`            | 레코드 수정 시 `CURRENT_TIMESTAMP` 사용 (MariaDB / MySQL)                            |
| `->virtualAs($expression)`          | 가상 생성 컬럼 생성 (MariaDB / MySQL / SQLite)                                       |
| `->generatedAs($expression)`        | 지정된 시퀀스 옵션으로 identity 컬럼 생성 (PostgreSQL)                               |
| `->always()`                        | 시퀀스 값이 입력보다 우선됨 (PostgreSQL)                                             |

<a name="default-expressions"></a>
#### 기본값 표현식 (Default Expressions)

`default` 수정자는 값 또는 `Illuminate\Database\Query\Expression` 인스턴스를 받을 수 있습니다. `Expression` 인스턴스를 사용할 경우, 값에 따옴표가 자동으로 붙지 않으며 데이터베이스 고유의 함수를 사용할 수 있습니다. 예를 들어 JSON 컬럼의 기본값을 설정할 때 유용합니다.

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
> 기본값 표현식의 지원 여부는 데이터베이스 드라이버, 버전, 필드 타입에 따라 다를 수 있습니다. 반드시 데이터베이스 공식 문서를 참고하세요.

<a name="column-order"></a>
#### 컬럼 순서 지정

MariaDB 또는 MySQL에서, `after` 메서드를 사용하면 기존 컬럼 뒤에 새 컬럼을 추가할 수 있습니다.

```php
$table->after('password', function (Blueprint $table) {
    $table->string('address_line1');
    $table->string('address_line2');
    $table->string('city');
});
```

<a name="instant-column-operations"></a>
#### Instant 컬럼 작업

MySQL을 사용할 때는, 컬럼 정의에 `instant` 수정자를 연결해 MySQL의 "instant" 알고리즘을 사용할 수 있습니다. 이 방법은 테이블 크기와 무관하게 전체 테이블 재빌드 없이 컬럼 추가/수정 작업을 거의 즉시 처리해줍니다.

```php
$table->string('name')->nullable()->instant();
```

Instant 방식은 테이블 끝에만 컬럼을 추가할 수 있으므로 `after`, `first` 수정자와 함께 사용할 수 없습니다. 또한 모든 컬럼/작업이 지원되는 것은 아니니, 지원 범위는 [MySQL 공식 문서](https://dev.mysql.com/doc/refman/8.0/en/innodb-online-ddl-operations.html)에서 확인하세요.

<a name="ddl-locking"></a>
#### DDL 락(Locking)

MySQL에서는 컬럼, 인덱스, 외래 키 정의에 `lock` 수정자를 연결해 스키마 작업 중 테이블 락 모드를 조정할 수 있습니다. `none`(읽기/쓰기 모두 허용), `shared`(읽기만 허용, 쓰기는 불가), `exclusive`(모든 동시 접근 차단), `default`(MySQL이 자동 결정) 중 하나를 지정할 수 있습니다.

```php
$table->string('name')->lock('none');

$table->index('email')->lock('shared');
```

호환되지 않는 락 모드를 지정하면 MySQL이 에러를 반환합니다. `instant`와 조합해 최적화할 수도 있습니다.

```php
$table->string('name')->instant()->lock('none');
```

<a name="modifying-columns"></a>
### 컬럼 수정 (Modifying Columns)

`change` 메서드는 기존 컬럼의 타입, 속성 등을 수정할 때 사용합니다. 예를 들어, `name` 컬럼의 길이를 25에서 50으로 늘리고 싶다면, 아래와 같이 현재 원하는 상태로 정의한 뒤 `change`를 호출하면 됩니다.

```php
Schema::table('users', function (Blueprint $table) {
    $table->string('name', 50)->change();
});
```

컬럼을 수정할 때는 유지하려는 모든 수정자를 명시적으로 연결해야 하며, 명시하지 않은 속성은 제거됩니다. 예를 들어, `unsigned`, `default`, `comment` 등을 계속 적용하려면 반드시 모두 적어야 합니다.

```php
Schema::table('users', function (Blueprint $table) {
    $table->integer('votes')->unsigned()->default(1)->comment('my comment')->change();
});
```

`change`는 컬럼의 인덱스는 변경하지 않습니다. 따라서 인덱스를 수정하고 싶을 땐, 인덱스 수정자를 따로 사용해야 합니다.

```php
// 인덱스 추가...
$table->bigIncrements('id')->primary()->change();

// 인덱스 제거...
$table->char('postal_code', 10)->unique(false)->change();
```

<a name="renaming-columns"></a>
### 컬럼 이름 변경 (Renaming Columns)

컬럼의 이름을 변경하려면, 스키마 빌더에서 제공하는 `renameColumn` 메서드를 사용하세요.

```php
Schema::table('users', function (Blueprint $table) {
    $table->renameColumn('from', 'to');
});
```

<a name="dropping-columns"></a>
### 컬럼 삭제 (Dropping Columns)

컬럼을 삭제하고자 할 때는 스키마 빌더의 `dropColumn` 메서드를 사용하세요.

```php
Schema::table('users', function (Blueprint $table) {
    $table->dropColumn('votes');
});
```

여러 컬럼을 한 번에 삭제할 땐, 이름 배열을 전달할 수 있습니다.

```php
Schema::table('users', function (Blueprint $table) {
    $table->dropColumn(['votes', 'avatar', 'location']);
});
```

<a name="available-command-aliases"></a>
#### 사용 가능한 명령어 별칭

Laravel에서는 자주 사용하는 컬럼 삭제 작업을 위한 여러 편리한 메서드를 제공합니다. 아래 표에서 상세 내용을 확인할 수 있습니다.

| 명령어                                    | 설명                                         |
| ----------------------------------------- | -------------------------------------------- |
| `$table->dropMorphs('morphable');`        | `morphable_id`, `morphable_type` 컬럼 삭제   |
| `$table->dropRememberToken();`            | `remember_token` 컬럼 삭제                   |
| `$table->dropSoftDeletes();`              | `deleted_at` 컬럼 삭제                       |
| `$table->dropSoftDeletesTz();`            | `dropSoftDeletes()` 메서드의 별칭            |
| `$table->dropTimestamps();`               | `created_at`, `updated_at` 컬럼 삭제         |
| `$table->dropTimestampsTz();`             | `dropTimestamps()` 메서드의 별칭             |

<a name="indexes"></a>
## 인덱스 (Indexes)

<a name="creating-indexes"></a>
### 인덱스 생성 (Creating Indexes)

Laravel 스키마 빌더는 다양한 인덱스 타입을 지원합니다. 예를 들어, 새 `email` 컬럼을 만들고, 유니크 값만 허용하고 싶다면 아래와 같이 정의할 수 있습니다.

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->string('email')->unique();
});
```

또는 컬럼을 정의한 뒤에 인덱스를 따로 지정할 수도 있습니다. 이 경우, 스키마 빌더의 Blueprint 객체에서 관련 메서드를 호출하면 됩니다.

```php
$table->unique('email');
```

여러 컬럼을 대상으로 복합 인덱스를 만들 때는 배열로 지정하세요.

```php
$table->index(['account_id', 'created_at']);
```

인덱스명은 기본적으로 Laravel이 자동으로 생성하지만, 두 번째 인자로 직접 지정할 수도 있습니다.

```php
$table->unique('email', 'unique_email');
```

<a name="available-index-types"></a>
#### 지원하는 인덱스 타입

Laravel의 스키마 빌더 Blueprint 클래스는 모든 인덱스 타입을 만들 수 있는 다양한 메서드를 제공합니다. 각 메서드는 선택적으로 두 번째 인자로 인덱스 이름을 지정받을 수 있으며, 생략 시 테이블/컬럼명/인덱스 타입 조합으로 자동 생성됩니다.

| 명령어                                         | 설명                                              |
| ---------------------------------------------- | ------------------------------------------------- |
| `$table->primary('id');`                       | 프라이머리 키 추가                                |
| `$table->primary(['id', 'parent_id']);`        | 복합키 추가                                       |
| `$table->unique('email');`                     | 유니크 인덱스 추가                                |
| `$table->index('state');`                      | 일반 인덱스 추가                                  |
| `$table->fullText('body');`                    | 전문(Full Text) 인덱스 추가 (MariaDB/MySQL/PostgreSQL) |
| `$table->fullText('body')->language('english');` | 지정 언어로 전문 인덱스 추가 (PostgreSQL)       |
| `$table->spatialIndex('location');`            | 공간 인덱스 추가 (SQLite 제외)                    |

<a name="online-index-creation"></a>
#### 온라인 인덱스 생성

대용량 테이블에 인덱스를 생성하면, 인덱스 생성 과정에서 테이블이 잠기고 읽기/쓰기가 차단될 수 있습니다. PostgreSQL이나 SQL Server를 사용할 때는, 인덱스 정의에 `online` 메서드를 체이닝하여 인덱스 생성 중에도 데이터 읽기/쓰기를 허용할 수 있습니다.

```php
$table->string('email')->unique()->online();
```

PostgreSQL에서는 인덱스 생성 구문에 `CONCURRENTLY` 옵션이 추가되고, SQL Server에서는 `WITH (online = on)` 옵션이 더해집니다.

<a name="renaming-indexes"></a>
### 인덱스 이름 변경 (Renaming Indexes)

인덱스의 이름을 변경하려면, 스키마 빌더 Blueprint에서 제공하는 `renameIndex` 메서드를 사용하세요. 첫 번째 인자로 현재 이름, 두 번째 인자로 새 이름을 전달합니다.

```php
$table->renameIndex('from', 'to')
```

<a name="dropping-indexes"></a>
### 인덱스 삭제 (Dropping Indexes)

인덱스를 삭제할 때는 인덱스 이름을 반드시 명시해야 합니다. Laravel은 기본적으로 인덱스 타입별로 테이블명, 컬럼명, 인덱스 타입을 조합해 인덱스 이름을 자동 부여합니다. 아래 예시처럼 사용할 수 있습니다.

| 명령어                                             | 설명                                         |
| -------------------------------------------------- | -------------------------------------------- |
| `$table->dropPrimary('users_id_primary');`         | "users" 테이블에서 프라이머리 키 삭제         |
| `$table->dropUnique('users_email_unique');`        | "users" 테이블에서 유니크 인덱스 삭제         |
| `$table->dropIndex('geo_state_index');`            | "geo" 테이블에서 일반 인덱스 삭제             |
| `$table->dropFullText('posts_body_fulltext');`     | "posts" 테이블에서 전문 인덱스 삭제           |
| `$table->dropSpatialIndex('geo_location_spatialindex');` | "geo" 테이블에서 공간 인덱스 삭제 (SQLite 제외) |

컬럼명의 배열을 전달해 인덱스를 삭제하면, 관례에 따라 인덱스 이름이 자동 생성됩니다.

```php
Schema::table('geo', function (Blueprint $table) {
    $table->dropIndex(['state']); // 'geo_state_index' 인덱스 삭제
});
```

<a name="foreign-key-constraints"></a>
### 외래 키 제약조건 (Foreign Key Constraints)

Laravel은 데이터베이스 수준에서 참조 무결성을 강제하는 외래 키 제약조건 생성도 지원합니다. 예를 들어, `posts` 테이블에 `user_id` 컬럼을 만들고 `users` 테이블의 `id` 컬럼을 참조하려면 다음과 같이 작성할 수 있습니다.

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('posts', function (Blueprint $table) {
    $table->unsignedBigInteger('user_id');

    $table->foreign('user_id')->references('id')->on('users');
});
```

이 방식은 다소 장황할 수 있어서, Laravel은 보다 간결한 메서드 체이닝을 지원합니다. `foreignId` 메서드로 컬럼을 만들고, `constrained` 메서드를 사용하면 위 내용이 더 간단하게 표현됩니다.

```php
Schema::table('posts', function (Blueprint $table) {
    $table->foreignId('user_id')->constrained();
});
```

`foreignId`는 `UNSIGNED BIGINT` 컬럼을 생성하고, `constrained`는 관례에 따라 참조 테이블 및 컬럼을 자동 탐지합니다. 만약 관례와 다르게 설계한 경우, `constrained` 메서드에 직접 지정할 수도 있고, 인덱스 이름도 따로 정할 수 있습니다.

```php
Schema::table('posts', function (Blueprint $table) {
    $table->foreignId('user_id')->constrained(
        table: 'users', indexName: 'posts_user_id'
    );
});
```

또한, "on delete", "on update" 시 동작을 지정할 수도 있습니다.

```php
$table->foreignId('user_id')
    ->constrained()
    ->onUpdate('cascade')
    ->onDelete('cascade');
```

동일한 기능을 제공하는 더 직관적인 메서드도 아래처럼 제공합니다.

| 메서드                        | 설명                                                 |
| ----------------------------- | ---------------------------------------------------- |
| `$table->cascadeOnUpdate();`  | 업데이트 시 연쇄 적용                                 |
| `$table->restrictOnUpdate();` | 업데이트 제한                                         |
| `$table->nullOnUpdate();`     | 업데이트 시 외래 키 값을 null로 변경                  |
| `$table->noActionOnUpdate();` | 업데이트 시 아무 동작 없음                            |
| `$table->cascadeOnDelete();`  | 삭제 시 연쇄 적용                                     |
| `$table->restrictOnDelete();` | 삭제 제한                                             |
| `$table->nullOnDelete();`     | 삭제 시 외래 키 값을 null로 변경                      |
| `$table->noActionOnDelete();` | 자식 레코드가 있으면 삭제 불가                        |

추가적인 [컬럼 수정자](#column-modifiers)는 반드시 `constrained` 메서드 호출 전에 사용해야 합니다.

```php
$table->foreignId('user_id')
    ->nullable()
    ->constrained();
```

<a name="dropping-foreign-keys"></a>
#### 외래 키 삭제

외래 키를 삭제하려면 `dropForeign` 메서드에 삭제할 외래 키 제약조건 이름을 인자로 전달하면 됩니다. 외래 키 이름은 인덱스와 동일한 네이밍 관례를 따르며, 테이블명과 컬럼명 뒤에 "\_foreign"이 붙습니다.

```php
$table->dropForeign('posts_user_id_foreign');
```

또는, 외래 키 컬럼명을 배열로 전달하면 Laravel이 관례에 따라 이름을 만들어 삭제합니다.

```php
$table->dropForeign(['user_id']);
```

<a name="toggling-foreign-key-constraints"></a>
#### 외래 키 제약조건 활성화/비활성화

마이그레이션 내에서 외래 키 제약조건을 활성화/비활성화할 수 있습니다.

```php
Schema::enableForeignKeyConstraints();

Schema::disableForeignKeyConstraints();

Schema::withoutForeignKeyConstraints(function () {
    // 이 클로저 내에서는 제약조건 비활성화됨...
});
```

> [!WARNING]
> SQLite는 기본적으로 외래 키 제약조건이 비활성화되어 있습니다. SQLite 사용 시에는 반드시 [외래 키 지원 활성화](/docs/12.x/database#configuration)를 먼저 진행한 후, 마이그레이션에서 외래 키를 생성하세요.

<a name="events"></a>
## 이벤트 (Events)

편의를 위해, 각 마이그레이션 작업은 [이벤트](/docs/12.x/events)를 발생시킵니다. 아래 모든 이벤트는 기본 `Illuminate\Database\Events\MigrationEvent` 클래스를 상속합니다.

| 클래스                                          | 설명                                              |
| ----------------------------------------------- | ------------------------------------------------- |
| `Illuminate\Database\Events\MigrationsStarted`   | 마이그레이션 배치 실행 직전                        |
| `Illuminate\Database\Events\MigrationsEnded`     | 마이그레이션 배치 실행 완료                        |
| `Illuminate\Database\Events\MigrationStarted`    | 단일 마이그레이션 실행 직전                        |
| `Illuminate\Database\Events\MigrationEnded`      | 단일 마이그레이션 실행 완료                        |
| `Illuminate\Database\Events\NoPendingMigrations` | 대기 중인 마이그레이션 없음                        |
| `Illuminate\Database\Events\SchemaDumped`        | 데이터베이스 스키마 덤프 완료                      |
| `Illuminate\Database\Events\SchemaLoaded`        | 기존 데이터베이스 스키마 덤프 로드 완료            |
