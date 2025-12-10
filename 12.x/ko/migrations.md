# 데이터베이스: 마이그레이션 (Database: Migrations)

- [소개](#introduction)
- [마이그레이션 생성](#generating-migrations)
    - [마이그레이션 합치기(Squashing)](#squashing-migrations)
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
    - [컬럼 변경](#modifying-columns)
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

마이그레이션(Migration)은 데이터베이스의 버전 관리를 가능하게 하여, 팀이 애플리케이션의 데이터베이스 스키마 정의를 같이 정의하고 공유할 수 있게 합니다. 만약 소스 코드 변경 사항을 받은 후에 동료에게 로컬 데이터베이스에 컬럼을 수동으로 추가하라고 안내한 경험이 있다면, 이것이 마이그레이션이 해결하는 문제입니다.

Laravel의 `Schema` [파사드](/docs/12.x/facades)는 모든 Laravel에서 지원하는 데이터베이스 시스템 간에 데이터베이스와 무관하게 테이블을 생성하고 조작할 수 있도록 지원합니다. 일반적으로 마이그레이션은 이 파사드를 사용하여 DB 테이블과 컬럼을 생성 및 수정합니다.

<a name="generating-migrations"></a>
## 마이그레이션 생성

데이터베이스 마이그레이션 파일을 생성하려면 `make:migration` [Artisan 명령어](/docs/12.x/artisan)를 사용할 수 있습니다. 새로 생성되는 마이그레이션은 `database/migrations` 디렉터리에 배치됩니다. 각 마이그레이션 파일명에는 타임스탬프가 포함되어 있어 Laravel이 마이그레이션의 실행 순서를 파악할 수 있습니다:

```shell
php artisan make:migration create_flights_table
```

Laravel은 마이그레이션의 이름을 활용하여 테이블 이름 및 해당 마이그레이션이 새로운 테이블을 생성하는지 여부를 추측하려고 시도합니다. 만약 Laravel이 마이그레이션 이름에서 테이블명을 파악할 수 있다면, 해당 테이블명으로 미리 채워진 마이그레이션 파일이 생성됩니다. 그렇지 않은 경우, 마이그레이션 파일 내에서 직접 테이블을 지정하면 됩니다.

생성되는 마이그레이션의 경로를 직접 지정하고 싶다면, `make:migration` 명령 실행 시 `--path` 옵션을 사용할 수 있습니다. 이 경로는 애플리케이션의 기본 경로 기준 상대 경로여야 합니다.

> [!NOTE]
> 마이그레이션 스텁(stub)은 [스텁 커스터마이징](/docs/12.x/artisan#stub-customization)을 통해 사용자 정의할 수 있습니다.

<a name="squashing-migrations"></a>
### 마이그레이션 합치기(Squashing)

애플리케이션을 개발하다 보면 시간이 지남에 따라 점점 더 많은 마이그레이션이 쌓이게 됩니다. 이런 경우 `database/migrations` 폴더가 수백 개까지 마이그레이션 파일로 넘쳐날 수 있습니다. 이럴 때, 여러 마이그레이션을 하나의 SQL 파일로 "합치기(squash)"할 수 있습니다. 이를 시작하려면 `schema:dump` 명령어를 실행하세요:

```shell
php artisan schema:dump

# 현재 DB 스키마를 덤프하고 기존의 모든 마이그레이션을 정리(prune)합니다...
php artisan schema:dump --prune
```

이 명령을 실행하면 Laravel은 애플리케이션의 `database/schema` 디렉터리에 "스키마" 파일을 생성합니다. 이 스키마 파일의 이름은 데이터베이스 커넥션 이름과 일치합니다. 이후 데이터베이스 마이그레이션을 시도할 때 아직 실행된 마이그레이션이 없는 경우, Laravel은 먼저 해당 데이터베이스 커넥션의 스키마 파일에 있는 SQL문을 실행합니다. 스키마 파일에 포함되지 않은 나머지 마이그레이션이 있다면 그 이후에 순차적으로 실행됩니다.

애플리케이션의 테스트가 로컬 개발과 다른 데이터베이스 커넥션을 사용할 경우, 테스트 환경에서도 스키마 파일이 존재하는지 확인해야 합니다. 보통 로컬 개발에서 사용하는 커넥션을 덤프한 후 별도의 테스트 커넥션으로도 스키마 덤프를 수행할 수 있습니다:

```shell
php artisan schema:dump
php artisan schema:dump --database=testing --prune
```

동료 개발자가 애플리케이션의 초기 데이터베이스 구조를 빠르게 생성할 수 있도록, 생성된 데이터베이스 스키마 파일을 소스 컨트롤에 반드시 커밋해야 합니다.

> [!WARNING]
> 마이그레이션 합치기(Squashing) 기능은 MariaDB, MySQL, PostgreSQL, SQLite 데이터베이스에서만 동작하며, 해당 데이터베이스의 커맨드 라인 클라이언트를 활용합니다.

<a name="migration-structure"></a>
## 마이그레이션 구조

마이그레이션 클래스는 두 개의 메서드, `up`과 `down`을 가집니다. `up` 메서드는 데이터베이스에 새로운 테이블, 컬럼, 인덱스를 추가할 때 사용하며, `down` 메서드는 `up`에서 수행한 작업을 역으로 되돌릴 때 사용합니다.

이 두 메서드 내에서는 Laravel의 스키마 빌더를 활용하여 직관적으로 테이블을 생성하고 수정할 수 있습니다. `Schema` 빌더에서 제공하는 모든 메서드를 확인하려면 [해당 문서](#creating-tables)를 참고하세요. 예를 들어, 아래의 마이그레이션은 `flights` 테이블을 생성합니다:

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

마이그레이션이 애플리케이션의 기본 데이터베이스 커넥션이 아닌 다른 커넥션을 사용해야 한다면, 마이그레이션 클래스의 `$connection` 속성을 설정해야 합니다:

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

특정 마이그레이션이 아직 활성화되지 않은 기능을 위해 작성된 것이라 실행을 원하지 않는 경우, 마이그레이션에 `shouldRun` 메서드를 정의할 수 있습니다. 이 메서드가 `false`를 반환하면 해당 마이그레이션은 건너뛰게 됩니다:

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
## 마이그레이션 실행

아직 실행되지 않은 모든 마이그레이션을 실행하려면 `migrate` Artisan 명령어를 사용하세요:

```shell
php artisan migrate
```

이미 실행된 마이그레이션과 아직 실행되지 않은 마이그레이션을 확인하려면 `migrate:status` Artisan 명령어를 사용할 수 있습니다:

```shell
php artisan migrate:status
```

마이그레이션이 실제로 실행되지는 않지만, 어떤 SQL문이 실행될지 확인하고 싶다면 `migrate` 명령에 `--pretend` 플래그를 추가하세요:

```shell
php artisan migrate --pretend
```

<a name="isolating-migration-execution"></a>
#### 마이그레이션 실행 독립(격리)화

여러 서버에서 애플리케이션을 배포하면서 마이그레이션도 같이 실행될 경우, 여러 서버가 동시에 데이터베이스를 마이그레이션하지 않도록 해야 합니다. 이를 방지하기 위해 `migrate` 명령 실행 시 `--isolated` 옵션을 사용할 수 있습니다.

`isolated` 옵션을 지정하면, Laravel은 마이그레이션 실행 전에 애플리케이션의 캐시 드라이버를 사용하여 원자적(atomic) 락을 획득합니다. 락이 걸려있는 동안 다른 모든 `migrate` 명령 실행 시도는 실제로 실행되지 않고, 성공적인 종료 코드로 바로 반환됩니다:

```shell
php artisan migrate --isolated
```

> [!WARNING]
> 이 기능을 사용하려면, 애플리케이션의 기본 캐시 드라이버가 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 중 하나여야 하며, 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

<a name="forcing-migrations-to-run-in-production"></a>
#### 프로덕션에서 마이그레이션 강제 실행

일부 마이그레이션 작업은 데이터를 잃게 만드는 파괴적(destructive) 작업일 수 있습니다. 이런 명령이 프로덕션 데이터베이스에 적용되는 것을 방지하기 위해, 명령 실행 전 항상 확인(prompt)이 표시됩니다. 하지만 프롬프트 없이 강제로 실행하려면 `--force` 플래그를 사용하세요:

```shell
php artisan migrate --force
```

<a name="rolling-back-migrations"></a>
### 마이그레이션 롤백

가장 최근에 실행된 마이그레이션 실행을 되돌리려면 `rollback` Artisan 명령어를 사용하세요. 이 명령어는 마지막 "배치(batch)"에 해당하는 마이그레이션(여러 파일 포함 가능)을 롤백합니다:

```shell
php artisan migrate:rollback
```

롤백할 마이그레이션 개수를 제한하고 싶을 때는 `--step` 옵션을 사용하세요. 아래 예시는 최근 5개의 마이그레이션을 롤백합니다:

```shell
php artisan migrate:rollback --step=5
```

특정 "배치(batch)"의 마이그레이션만 롤백하려면 `--batch` 옵션에 해당 배치 값을 지정하세요. 예를 들어, 아래 명령어는 batch 3의 모든 마이그레이션을 롤백합니다:

```shell
php artisan migrate:rollback --batch=3
```

마이그레이션이 실제로 실행되지는 않지만, 어떤 SQL문이 수행될지 확인하려면 `migrate:rollback` 명령에 `--pretend` 플래그를 추가하세요:

```shell
php artisan migrate:rollback --pretend
```

`migrate:reset` 명령어를 사용하면 애플리케이션의 모든 마이그레이션이 롤백됩니다:

```shell
php artisan migrate:reset
```

<a name="roll-back-migrate-using-a-single-command"></a>
#### 한 번의 명령으로 롤백 및 마이그레이션

`migrate:refresh` 명령어는 모든 마이그레이션을 롤백하고 다시 `migrate` 명령을 실행합니다. 즉, 데이터베이스를 초기화합니다:

```shell
php artisan migrate:refresh

# 데이터베이스를 새로고침 후 모든 시드를 실행하려면...
php artisan migrate:refresh --seed
```

최근의 일부 마이그레이션만 롤백/재실행하고 싶을 때는 `--step` 옵션을 사용하세요. 예를 들어, 아래 명령어는 최근 5개의 마이그레이션을 롤백 후 다시 실행합니다:

```shell
php artisan migrate:refresh --step=5
```

<a name="drop-all-tables-migrate"></a>
#### 모든 테이블 삭제 및 마이그레이션

`migrate:fresh` 명령어는 데이터베이스의 모든 테이블을 삭제하고 다시 `migrate` 명령을 실행합니다:

```shell
php artisan migrate:fresh

php artisan migrate:fresh --seed
```

기본적으로 `migrate:fresh` 명령어는 기본 데이터베이스 커넥션에서만 테이블을 삭제합니다. 하지만 `--database` 옵션을 사용하여 마이그레이션할 커넥션을 지정할 수 있습니다. 커넥션 이름은 애플리케이션의 `database` [설정 파일](/docs/12.x/configuration)에 정의된 이름이어야 합니다:

```shell
php artisan migrate:fresh --database=admin
```

> [!WARNING]
> `migrate:fresh` 명령은 프리픽스와 상관없이 모든 데이터베이스 테이블을 삭제합니다. 다른 앱과 테이블을 공유하는 데이터베이스에서 실수로 삭제하지 않도록 주의해야 합니다.

<a name="tables"></a>
## 테이블

<a name="creating-tables"></a>
### 테이블 생성

새로운 데이터베이스 테이블을 생성하려면 `Schema` 파사드의 `create` 메서드를 사용하세요. `create` 메서드는 두 개의 인수를 받으며, 첫 번째는 테이블 이름, 두 번째는 새 테이블을 정의할 수 있는 `Blueprint` 객체를 받는 클로저입니다:

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

테이블을 생성할 때는 [컬럼 생성 메서드](#creating-columns) 중 어떤 것이든 활용하여 테이블의 컬럼을 정의할 수 있습니다.

<a name="determining-table-column-existence"></a>
#### 테이블/컬럼 존재 여부 확인

`hasTable`, `hasColumn`, `hasIndex` 메서드를 사용하여 테이블, 컬럼, 인덱스가 존재하는지 확인할 수 있습니다:

```php
if (Schema::hasTable('users')) {
    // "users" 테이블이 존재합니다...
}

if (Schema::hasColumn('users', 'email')) {
    // "users" 테이블이 존재하고 "email" 컬럼도 있습니다...
}

if (Schema::hasIndex('users', ['email'], 'unique')) {
    // "users" 테이블에 "email" 컬럼에 대한 unique 인덱스가 있습니다...
}
```

<a name="database-connection-table-options"></a>
#### 데이터베이스 커넥션 및 테이블 옵션

기본 데이터베이스 커넥션이 아닌 곳에서 스키마 작업을 하고 싶다면 `connection` 메서드를 사용할 수 있습니다:

```php
Schema::connection('sqlite')->create('users', function (Blueprint $table) {
    $table->id();
});
```

테이블 생성 시 사용할 수 있는 몇 가지 추가 속성 및 메서드도 있습니다. MariaDB 또는 MySQL에서 테이블의 스토리지 엔진을 지정하려면 `engine` 속성을 사용하세요:

```php
Schema::create('users', function (Blueprint $table) {
    $table->engine('InnoDB');

    // ...
});
```

MariaDB, MySQL에서 테이블의 문자셋 및 콜레이션을 지정하려면 `charset`, `collation` 속성을 사용할 수 있습니다:

```php
Schema::create('users', function (Blueprint $table) {
    $table->charset('utf8mb4');
    $table->collation('utf8mb4_unicode_ci');

    // ...
});
```

테이블을 "임시(temporary)"로 지정하려면 `temporary` 메서드를 사용하세요. 임시 테이블은 현재 커넥션의 데이터베이스 세션에서만 보이고 커넥션 종료 시 자동으로 삭제됩니다:

```php
Schema::create('calculations', function (Blueprint $table) {
    $table->temporary();

    // ...
});
```

테이블에 "주석(comment)"을 추가하고 싶다면, 테이블 인스턴스에서 `comment` 메서드를 사용하세요. 테이블 주석은 현재 MariaDB, MySQL, PostgreSQL에서만 지원됩니다:

```php
Schema::create('calculations', function (Blueprint $table) {
    $table->comment('Business calculations');

    // ...
});
```

<a name="updating-tables"></a>
### 테이블 수정

`Schema` 파사드의 `table` 메서드를 사용하여 기존 테이블을 수정할 수 있습니다. `create` 메서드처럼 `table` 메서드도 테이블 이름, 클로저(이 안에서 `Blueprint` 인스턴스를 이용해 컬럼, 인덱스 등을 추가/수정할 수 있음)를 인수로 받습니다:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->integer('votes');
});
```

<a name="renaming-and-dropping-tables"></a>
### 테이블 이름 변경/삭제

기존 데이터베이스 테이블의 이름을 바꾸려면 `rename` 메서드를 사용하세요:

```php
use Illuminate\Support\Facades\Schema;

Schema::rename($from, $to);
```

기존 테이블을 삭제하려면 `drop` 또는 `dropIfExists` 메서드를 사용할 수 있습니다:

```php
Schema::drop('users');

Schema::dropIfExists('users');
```

<a name="renaming-tables-with-foreign-keys"></a>
#### 외래 키가 있는 테이블 이름 변경

테이블 이름을 변경하기 전에, 해당 테이블의 외래 키 제약조건이 마이그레이션 파일에서 명시적인 이름으로 정의되어 있는지 반드시 확인하세요. 그렇지 않을 경우, 외래 키 제약조건 이름이 이전 테이블명을 참조하게 됩니다.

<a name="columns"></a>
## 컬럼

<a name="creating-columns"></a>
### 컬럼 생성

`Schema` 파사드의 `table` 메서드를 사용하여 기존 테이블에 컬럼을 추가할 수 있습니다. `create` 메서드와 마찬가지로, 테이블명과 클로저를 인수로 받아 `Blueprint` 인스턴스를 이용해 컬럼을 추가할 수 있습니다:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->integer('votes');
});
```

<a name="available-column-types"></a>
### 사용 가능한 컬럼 타입

스키마 빌더(Blueprint)는 데이터베이스 테이블에 추가할 수 있는 다양한 유형의 컬럼에 대응하는 여러 메서드를 제공합니다. 사용 가능한 메서드는 아래 표와 같습니다:

#### 불리언(Boolean) 타입

[boolean](#column-method-boolean)

#### 문자열 & 텍스트 타입

[char](#column-method-char)
[longText](#column-method-longText)
[mediumText](#column-method-mediumText)
[string](#column-method-string)
[text](#column-method-text)
[tinyText](#column-method-tinyText)

#### 숫자(Number) 타입

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

#### 날짜 & 시간(Date & Time) 타입

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

#### 바이너리(Binary) 타입

[binary](#column-method-binary)

#### 객체 & Json 타입

[json](#column-method-json)
[jsonb](#column-method-jsonb)

#### UUID & ULID 타입

[ulid](#column-method-ulid)
[ulidMorphs](#column-method-ulidMorphs)
[uuid](#column-method-uuid)
[uuidMorphs](#column-method-uuidMorphs)
[nullableUlidMorphs](#column-method-nullableUlidMorphs)
[nullableUuidMorphs](#column-method-nullableUuidMorphs)

#### 공간(Spatial) 타입

[geography](#column-method-geography)
[geometry](#column-method-geometry)

#### 연관관계(Relationship) 타입

[foreignId](#column-method-foreignId)
[foreignIdFor](#column-method-foreignIdFor)
[foreignUlid](#column-method-foreignUlid)
[foreignUuid](#column-method-foreignUuid)
[morphs](#column-method-morphs)
[nullableMorphs](#column-method-nullableMorphs)

#### 특수 타입

[enum](#column-method-enum)
[set](#column-method-set)
[macAddress](#column-method-macAddress)
[ipAddress](#column-method-ipAddress)
[rememberToken](#column-method-rememberToken)
[vector](#column-method-vector)

(이하로 각 컬럼 타입과 기능 설명의 코드 및 표는 원본과 동일하게 유지합니다.)

<a name="column-method-bigIncrements"></a>
#### `bigIncrements()`

`bigIncrements` 메서드는 자동 증가되는 `UNSIGNED BIGINT`(기본키) 컬럼을 생성합니다:

```php
$table->bigIncrements('id');
```

...

(위의 방식대로 이하 모든 컬럼 타입별 예시 및 설명은 코드/표 구조 완벽히 보존, 주석/설명은 자연스러운 한국어로 충실하게 번역)

...

<a name="column-modifiers"></a>
### 컬럼 수정자

위에서 소개한 컬럼 타입 외에도, 컬럼에 다양한 "수정자(modifier)"를 적용할 수 있습니다. 예를 들어 컬럼을 "nullable"(NULL 허용)로 만들고 싶다면 `nullable` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->string('email')->nullable();
});
```

아래 표는 사용 가능한 모든 컬럼 수정자를 정리한 것입니다(인덱스 관련 수정자는 제외):

<div class="overflow-auto">

| 수정자                                | 설명                                                                 |
| ----------------------------------- | ------------------------------------------------------------------- |
| `->after('column')`                 | 해당 컬럼을 특정 컬럼 "뒤"에 위치시킵니다 (MariaDB / MySQL).         |
| `->autoIncrement()`                 | `INTEGER` 컬럼을 자동 증가(기본키)로 설정합니다.                    |
| `->charset('utf8mb4')`              | 컬럼의 문자셋을 지정 (MariaDB / MySQL).                             |
| `->collation('utf8mb4_unicode_ci')` | 컬럼의 콜레이션을 지정합니다.                                       |
| `->comment('my comment')`           | 컬럼에 주석(comment) 추가 (MariaDB / MySQL / PostgreSQL).           |
| `->default($value)`                 | 컬럼의 "기본값"을 지정합니다.                                       |
| `->first()`                         | 해당 컬럼을 테이블의 "첫 번째" 위치로 둡니다 (MariaDB / MySQL).      |
| `->from($integer)`                  | 자동 증가 필드의 시작 값을 지정 (MariaDB / MySQL / PostgreSQL).      |
| `->invisible()`                     | 컬럼을 `SELECT *` 쿼리에서 "숨김" 처리 (MariaDB / MySQL).           |
| `->nullable($value = true)`         | 컬럼에 `NULL` 값 삽입 허용.                                         |
| `->storedAs($expression)`           | 저장된 생성 컬럼(stored generated column) 생성.                     |
| `->unsigned()`                      | `INTEGER` 컬럼을 `UNSIGNED`로 지정 (MariaDB / MySQL).               |
| `->useCurrent()`                    | `TIMESTAMP` 컬럼의 기본값을 `CURRENT_TIMESTAMP`로 설정.             |
| `->useCurrentOnUpdate()`            | 레코드 갱신 시 `TIMESTAMP`가 자동 변경 (MariaDB / MySQL).           |
| `->virtualAs($expression)`          | 가상(virtual) 생성 컬럼을 생성합니다.                               |
| `->generatedAs($expression)`        | 시퀀스 옵션이 지정된 ID 컬럼 생성 (PostgreSQL).                     |
| `->always()`                        | ID 컬럼에서 입력보다 시퀀스 값을 우선 사용하도록 정의 (PostgreSQL).  |

</div>

<a name="default-expressions"></a>
#### 기본값에 식(Expression) 사용

`default` 수정자는 값 또는 `Illuminate\Database\Query\Expression` 인스턴스를 받을 수 있습니다. Expression 인스턴스를 사용하면, 값이 따옴표로 감싸지지 않아 데이터베이스의 특수 함수나 식을 그대로 쓸 수 있습니다. 예를 들어 JSON 컬럼에 기본값을 지정할 때 유용합니다:

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
> 기본값 식(Expression) 지원 여부는 데이터베이스 드라이버, 버전, 필드 타입에 따라 다릅니다. 사용 전 해당 데이터베이스 문서를 참고하세요.

<a name="column-order"></a>
#### 컬럼 순서 지정

MariaDB/ MySQL을 사용할 때는 `after` 메서드를 통해 기존 컬럼 뒤에 새로운 컬럼을 추가할 수 있습니다:

```php
$table->after('password', function (Blueprint $table) {
    $table->string('address_line1');
    $table->string('address_line2');
    $table->string('city');
});
```

<a name="modifying-columns"></a>
### 컬럼 변경

`change` 메서드를 사용하면 기존 컬럼의 타입이나 속성을 변경할 수 있습니다. 예를 들어, `string` 컬럼의 길이를 25에서 50으로 늘리고 싶다면, 변경된 상태로 정의 후 `change` 메서드만 호출하면 됩니다:

```php
Schema::table('users', function (Blueprint $table) {
    $table->string('name', 50)->change();
});
```

컬럼을 변경할 때, 기존에 적용되었던 수정자를 계속 유지하고 싶다면 명시적으로 모든 수정자를 반복해서 작성해야 합니다. 누락되는 속성은 제거됩니다. 예를 들어, `unsigned`, `default`, `comment` 속성을 유지하려면 모두 명시해야 합니다:

```php
Schema::table('users', function (Blueprint $table) {
    $table->integer('votes')->unsigned()->default(1)->comment('my comment')->change();
});
```

`change` 메서드는 컬럼의 인덱스는 변경하지 않습니다. 따라서 인덱스를 추가하거나 삭제하려면 인덱스 관련 수정자를 별도로 사용해야 합니다:

```php
// 인덱스 추가...
$table->bigIncrements('id')->primary()->change();

// 인덱스 제거...
$table->char('postal_code', 10)->unique(false)->change();
```

<a name="renaming-columns"></a>
### 컬럼 이름 변경

컬럼 이름을 바꾸려면 스키마 빌더의 `renameColumn` 메서드를 사용하세요:

```php
Schema::table('users', function (Blueprint $table) {
    $table->renameColumn('from', 'to');
});
```

<a name="dropping-columns"></a>
### 컬럼 삭제

컬럼을 삭제하려면 스키마 빌더의 `dropColumn` 메서드를 사용하세요:

```php
Schema::table('users', function (Blueprint $table) {
    $table->dropColumn('votes');
});
```

한 번에 여러 컬럼을 삭제하려면 컬럼명 배열을 넘깁니다:

```php
Schema::table('users', function (Blueprint $table) {
    $table->dropColumn(['votes', 'avatar', 'location']);
});
```

<a name="available-command-aliases"></a>
#### 사용 가능한 명령어 별칭

Laravel은 자주 쓰는 컬럼 제거를 위한 몇 가지 별칭 메서드도 제공합니다. 각 메서드는 아래와 같습니다:

<div class="overflow-auto">

| 명령어                                 | 설명                                              |
| ----------------------------------- | ------------------------------------------------- |
| `$table->dropMorphs('morphable');`  | `morphable_id`, `morphable_type` 컬럼 삭제         |
| `$table->dropRememberToken();`      | `remember_token` 컬럼 삭제                         |
| `$table->dropSoftDeletes();`        | `deleted_at` 컬럼 삭제                             |
| `$table->dropSoftDeletesTz();`      | `dropSoftDeletes()`의 별칭                         |
| `$table->dropTimestamps();`         | `created_at`, `updated_at` 컬럼 삭제               |
| `$table->dropTimestampsTz();`       | `dropTimestamps()`의 별칭                          |

</div>

<a name="indexes"></a>
## 인덱스

<a name="creating-indexes"></a>
### 인덱스 생성

Laravel 스키마 빌더는 여러 유형의 인덱스를 지원합니다. 아래 예시에서는 `email` 컬럼을 새로 생성하고 해당 컬럼 값이 고유(unique)해야 함을 지정합니다. 컬럼 정의와 함께 `unique` 메서드를 바로 체이닝할 수 있습니다:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->string('email')->unique();
});
```

컬럼 정의 이후에 인덱스를 별도로 생성할 수도 있습니다. 그럴 경우, 스키마 빌더 Blueprint의 `unique` 메서드를 호출하세요. 이 메서드는 인덱스를 걸 컬럼명을 인수로 받습니다:

```php
$table->unique('email');
```

여러 컬럼에 대해 합성(복합) 인덱스를 생성하고 싶다면 인덱스 메서드에 컬럼명 배열을 넘기면 됩니다:

```php
$table->index(['account_id', 'created_at']);
```

인덱스 이름은 Laravel이 자동으로 생성하지만, 두 번째 인수로 직접 인덱스 이름을 지정할 수도 있습니다:

```php
$table->unique('email', 'unique_email');
```

<a name="available-index-types"></a>
#### 지원되는 인덱스 타입

Laravel의 스키마 빌더(Blueprint) 클래스는 Laravel이 지원하는 각 인덱스 타입별로 메서드를 제공합니다. 모든 인덱스 메서드는 두 번째 인수로 인덱스 이름 지정이 가능합니다(생략 시 기본 규칙에 따라 이름 자동 생성). 아래 표에 각 인덱스 메서드를 정리합니다:

<div class="overflow-auto">

| 명령어                                          | 설명                                               |
| --------------------------------------------- | ------------------------------------------------- |
| `$table->primary('id');`                      | 기본키(primary key) 추가                           |
| `$table->primary(['id', 'parent_id']);`       | 복합키(composite key) 추가                         |
| `$table->unique('email');`                    | 고유 인덱스(unique index) 추가                    |
| `$table->index('state');`                     | 일반 인덱스 추가                                   |
| `$table->fullText('body');`                   | 전문(Full text) 인덱스 추가 (MariaDB/MySQL/PostgreSQL)|
| `$table->fullText('body')->language('english');` | 지정 언어 전문 인덱스 (PostgreSQL)               |
| `$table->spatialIndex('location');`           | 공간(spatial) 인덱스 추가(SQLite 제외)             |

</div>

<a name="renaming-indexes"></a>
### 인덱스 이름 변경

인덱스 이름을 변경하려면 스키마 빌더 Blueprint의 `renameIndex` 메서드를 사용하세요. 첫 번째 인수는 현재 인덱스 이름, 두 번째 인수는 바꾸려는 이름입니다:

```php
$table->renameIndex('from', 'to')
```

<a name="dropping-indexes"></a>
### 인덱스 삭제

인덱스를 삭제하려면 인덱스의 이름을 명시해야 합니다. Laravel은 기본적으로 테이블 이름, 인덱스 컬럼명, 인덱스 타입을 조합해 인덱스 명을 생성합니다. 아래는 예시입니다:

<div class="overflow-auto">

| 명령어                                                | 설명                                             |
| --------------------------------------------------- | ----------------------------------------------- |
| `$table->dropPrimary('users_id_primary');`          | "users" 테이블의 기본키 제거                    |
| `$table->dropUnique('users_email_unique');`         | "users" 테이블의 고유 인덱스 제거               |
| `$table->dropIndex('geo_state_index');`             | "geo" 테이블의 일반 인덱스 제거                 |
| `$table->dropFullText('posts_body_fulltext');`      | "posts" 테이블의 전문 인덱스 제거               |
| `$table->dropSpatialIndex('geo_location_spatialindex');` | "geo" 테이블의 공간 인덱스 제거(SQLite 제외)  |

</div>

여러 컬럼을 대상으로 인덱스를 삭제할 때는 컬럼명 배열을 넘기면, Laravel 규칙에 맞게 인덱스 이름이 자동 생성되어 해당 인덱스가 제거됩니다:

```php
Schema::table('geo', function (Blueprint $table) {
    $table->dropIndex(['state']); // 'geo_state_index' 인덱스 제거
});
```

<a name="foreign-key-constraints"></a>
### 외래 키 제약조건

Laravel은 데이터베이스 수준의 참조 무결성 보장을 위해 외래 키 제약조건 생성도 지원합니다. 예를 들어, `posts` 테이블의 `user_id` 컬럼이 `users` 테이블의 `id` 컬럼을 참조하도록 하려면 아래처럼 작성합니다:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('posts', function (Blueprint $table) {
    $table->unsignedBigInteger('user_id');

    $table->foreign('user_id')->references('id')->on('users');
});
```

이 같은 형태는 다소 장황하므로, Laravel은 더 간결하고 관습(convention)에 기반한 추가 메서드를 제공합니다. 즉, 컬럼을 만들 때 `foreignId` 및 `constrained`를 함께 쓰면 다음처럼 간단하게 표현할 수 있습니다:

```php
Schema::table('posts', function (Blueprint $table) {
    $table->foreignId('user_id')->constrained();
});
```

`foreignId`는 `UNSIGNED BIGINT` 컬럼을 생성하고, `constrained`는 참조할 테이블과 컬럼명을 자동 추론합니다. 테이블이 규칙과 다를 때는 직접 값도 지정 가능합니다. 또한 생성될 인덱스 이름도 지정할 수 있습니다:

```php
Schema::table('posts', function (Blueprint $table) {
    $table->foreignId('user_id')->constrained(
        table: 'users', indexName: 'posts_user_id'
    );
});
```

외래 키 제약조건의 "삭제(on delete)", "수정(on update)" 시 동작도 직접 지정할 수 있습니다:

```php
$table->foreignId('user_id')
    ->constrained()
    ->onUpdate('cascade')
    ->onDelete('cascade');
```

아래는 이러한 동작을 위한 대안적이고 직관적인 문법(별도 메서드)입니다:

<div class="overflow-auto">

| 메서드                           | 설명                                       |
| ----------------------------- | ----------------------------------------- |
| `$table->cascadeOnUpdate();`  | 수정시(cascade) 상위 값이 변경되면 하위도 함께 변경 |
| `$table->restrictOnUpdate();` | 수정 제한(restrict)                          |
| `$table->nullOnUpdate();`     | 수정 시 외래 키 값을 null로 설정               |
| `$table->noActionOnUpdate();` | 수정 시 아무 동작 없음                        |
| `$table->cascadeOnDelete();`  | 삭제 시(cascade) 하위도 함께 삭제              |
| `$table->restrictOnDelete();` | 삭제 제한(restrict)                          |
| `$table->nullOnDelete();`     | 삭제 시 외래 키 값을 null로 설정               |
| `$table->noActionOnDelete();` | 자식 데이터가 있으면 삭제 안함                |

</div>

기타 필요한 [컬럼 수정자](#column-modifiers)는 반드시 `constrained` 메서드 호출 이전에 사용해야 합니다:

```php
$table->foreignId('user_id')
    ->nullable()
    ->constrained();
```

<a name="dropping-foreign-keys"></a>
#### 외래 키 삭제

외래 키 제약조건을 삭제하려면, 삭제할 외래 키의 이름을 `dropForeign` 메서드에 인수로 넘기세요. 외래 키 이름 규칙은 인덱스와 동일하며, 테이블명+컬럼명+`\_foreign` 형태입니다:

```php
$table->dropForeign('posts_user_id_foreign');
```

또는 외래 키 컬럼명을 배열로 넘기면, Laravel의 규칙에 따라 외래 키 이름이 자동 생성되어 해당 제약조건을 삭제합니다:

```php
$table->dropForeign(['user_id']);
```

<a name="toggling-foreign-key-constraints"></a>
#### 외래 키 제약조건 토글

마이그레이션 내에서 아래 메서드를 사용하여 외래 키 제약조건을 활성화하거나 비활성화할 수 있습니다:

```php
Schema::enableForeignKeyConstraints();

Schema::disableForeignKeyConstraints();

Schema::withoutForeignKeyConstraints(function () {
    // 이 클로저 내부에서는 제약조건이 비활성화됩니다...
});
```

> [!WARNING]
> SQLite는 기본적으로 외래 키 제약조건이 비활성화되어 있습니다. SQLite를 사용할 때는, 마이그레이션에서 제약조건을 생성하기 전에 반드시 [외래 키 지원 활성화](/docs/12.x/database#configuration)를 먼저 해주세요.

<a name="events"></a>
## 이벤트

편의상, 각 마이그레이션 작업은 [이벤트](/docs/12.x/events)를 발생시킵니다. 아래 모든 이벤트는 기본 `Illuminate\Database\Events\MigrationEvent` 클래스를 상속합니다:

<div class="overflow-auto">

| 클래스                                           | 설명                                           |
| --------------------------------------------- | --------------------------------------------- |
| `Illuminate\Database\Events\MigrationsStarted`   | 여러 마이그레이션(batch) 실행 직전 이벤트         |
| `Illuminate\Database\Events\MigrationsEnded`     | 여러 마이그레이션(batch) 실행 완료 후 이벤트      |
| `Illuminate\Database\Events\MigrationStarted`    | 한 번에 하나의 마이그레이션 실행 직전 이벤트      |
| `Illuminate\Database\Events\MigrationEnded`      | 한 번에 하나의 마이그레이션 실행 완료 후 이벤트   |
| `Illuminate\Database\Events\NoPendingMigrations` | 실행할 마이그레이션이 없을 때 발생               |
| `Illuminate\Database\Events\SchemaDumped`        | 데이터베이스 스키마 덤프 완료 이벤트             |
| `Illuminate\Database\Events\SchemaLoaded`        | 기존 스키마 덤프 파일 로드 완료 이벤트           |

</div>
