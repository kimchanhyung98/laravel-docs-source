# 데이터베이스: 마이그레이션 (Database: Migrations)

- [소개](#introduction)
- [마이그레이션 생성](#generating-migrations)
    - [마이그레이션 스쿼시(Squashing)](#squashing-migrations)
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

마이그레이션(Migration)은 데이터베이스의 버전 관리를 가능하게 하여, 팀원들이 애플리케이션의 데이터베이스 스키마 정의를 정의하고 공유할 수 있도록 해줍니다. 만약 소스 컨트롤에서 변경 사항을 받아온 후에 동료에게 직접 본인 로컬 데이터베이스 스키마에 컬럼을 수동으로 추가하라고 알려야 했던 경험이 있다면, 바로 이 문제가 마이그레이션이 해결하는 문제입니다.

Laravel의 `Schema` [파사드](/docs/12.x/facades)는 Laravel이 지원하는 모든 데이터베이스 시스템에서 데이터베이스에 독립적으로 테이블을 생성하고 조작할 수 있도록 도와줍니다. 일반적으로 마이그레이션에서는 이 파사드를 사용하여 데이터베이스 테이블과 컬럼을 생성하거나 수정합니다.

<a name="generating-migrations"></a>
## 마이그레이션 생성 (Generating Migrations)

`make:migration` [Artisan 명령어](/docs/12.x/artisan)를 사용하여 데이터베이스 마이그레이션 파일을 생성할 수 있습니다. 새로 생성된 마이그레이션 파일은 `database/migrations` 디렉토리에 저장되며, 각 마이그레이션 파일명에는 타임스탬프가 포함되어 있어 Laravel이 마이그레이션 실행 순서를 파악할 수 있습니다:

```shell
php artisan make:migration create_flights_table
```

Laravel은 마이그레이션의 이름을 참고하여 생성될 테이블의 이름을 추정하고, 마이그레이션이 새로운 테이블을 만드는지 여부를 판단하려고 시도합니다. 만약 Laravel이 마이그레이션의 이름에서 테이블 이름을 판단할 수 있다면, 해당 테이블로 미리 내용이 채워진 마이그레이션 파일을 생성합니다. 그렇지 않은 경우에는 마이그레이션 파일에서 직접 테이블을 지정하면 됩니다.

생성된 마이그레이션 파일의 경로를 직접 지정하고 싶다면, `make:migration` 명령어 실행 시 `--path` 옵션을 사용할 수 있습니다. 입력한 경로는 애플리케이션의 기준 경로 기준으로 작성해야 합니다.

> [!NOTE]
> 마이그레이션 스텁(stub)은 [스텁 퍼블리싱](/docs/12.x/artisan#stub-customization)을 통해 커스터마이즈할 수 있습니다.

<a name="squashing-migrations"></a>
### 마이그레이션 스쿼시(Squashing Migrations)

애플리케이션을 개발하다 보면 시간이 지남에 따라 마이그레이션 파일이 많아져 `database/migrations` 디렉토리가 수백 개의 파일로 불어나기도 합니다. 이럴 때 원한다면 여러 마이그레이션을 하나의 SQL 파일로 "스쿼시(squash, 합쳐서)" 할 수 있습니다. 이를 위해서는 `schema:dump` 명령어를 실행합니다:

```shell
php artisan schema:dump

# 현재 데이터베이스 스키마를 덤프(dump)하고, 기존 모든 마이그레이션 파일을 정리합니다...
php artisan schema:dump --prune
```

이 명령어를 실행하면, Laravel은 애플리케이션의 `database/schema` 디렉토리에 "스키마" 파일을 생성합니다. 이 파일의 이름은 데이터베이스 연결(커넥션) 이름과 일치합니다. 이제 데이터베이스를 마이그레이트할 때, 아직 실행된 마이그레이션이 없다면 가장 먼저 해당 데이터베이스 연결의 스키마 파일에 있는 SQL 명령문이 실행됩니다. 이후 스키마 파일에 포함되지 않은 나머지 마이그레이션만 실행됩니다.

애플리케이션 테스트에서 일반 개발환경과 다른 데이터베이스 연결을 사용하는 경우, 해당 연결로도 스키마 파일을 덤프해야 테스트가 올바르게 데이터베이스 구조를 생성할 수 있습니다. 보통 로컬 개발용 데이터를 먼저 덤프한 후 진행하게 됩니다:

```shell
php artisan schema:dump
php artisan schema:dump --database=testing --prune
```

데이터베이스 스키마 파일은 소스 컨트롤에 커밋하여, 새로 프로젝트에 참여하는 개발자들이 빠르게 초기 DB 구조를 만들 수 있도록 해야 합니다.

> [!WARNING]
> 마이그레이션 스쿼시 기능은 MariaDB, MySQL, PostgreSQL, SQLite에서만 지원하며, 데이터베이스의 커맨드라인 클라이언트를 사용합니다.

<a name="migration-structure"></a>
## 마이그레이션 구조 (Migration Structure)

마이그레이션 클래스는 `up`과 `down` 두 개의 메서드를 포함합니다. `up` 메서드는 데이터베이스에 새로운 테이블, 컬럼 또는 인덱스를 추가할 때 사용되며, `down` 메서드는 `up`에서 수행된 작업을 되돌릴 때 사용해야 합니다.

두 메서드 모두에서 Laravel의 스키마 빌더를 활용하여 테이블을 표현적으로 작성 및 수정할 수 있습니다. `Schema` 빌더에 사용할 수 있는 모든 메서드를 확인하려면 [해당 문서](#creating-tables)를 참고하세요. 예를 들어 다음은 `flights` 테이블을 생성하는 마이그레이션입니다:

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

마이그레이션이 애플리케이션의 기본 데이터베이스 연결이 아니라 다른 연결을 사용해야 한다면, 마이그레이션 클래스의 `$connection` 속성을 설정해야 합니다:

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

때로는 마이그레이션이 아직 활성화되지 않은 기능을 지원하기 위해 작성된 것이라, 당장 실행하고 싶지 않을 수도 있습니다. 이럴 땐 마이그레이션 클래스에 `shouldRun` 메서드를 정의할 수 있습니다. 만약 `shouldRun` 메서드가 `false`를 반환하면, 해당 마이그레이션은 건너뜁니다:

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

모든 대기 중인 마이그레이션을 실행하려면 `migrate` Artisan 명령어를 사용합니다:

```shell
php artisan migrate
```

이미 실행된 마이그레이션과 아직 남아있는 마이그레이션을 확인하려면 `migrate:status` 명령어를 사용하세요:

```shell
php artisan migrate:status
```

마이그레이션이 실제로 실행될 SQL 문장을 미리 보고 싶다면, `migrate` 명령어에 `--pretend` 플래그를 추가할 수 있습니다:

```shell
php artisan migrate --pretend
```

<a name="isolating-migration-execution"></a>
#### 마이그레이션 실행 격리

여러 서버에 애플리케이션을 배포하면서 배포 과정에서 마이그레이션을 동시에 실행한다면, 두 서버가 동시에 데이터베이스를 마이그레이션하여 충돌할 수 있습니다. 이를 방지하기 위한 방법으로 `migrate` 명령어에 `isolated` 옵션을 사용할 수 있습니다.

`isolated` 옵션을 제공하면, Laravel은 마이그레이션 실행 전에 애플리케이션의 캐시 드라이버를 이용해서 원자적(atomic) 락(lock)을 획득합니다. 락이 걸린 동안 다른 서버에서 마이그레이션을 실행하려고 해도, 실제 실행은 되지 않으며, 명령은 정상 종료 코드로 바로 끝납니다:

```shell
php artisan migrate --isolated
```

> [!WARNING]
> 이 기능을 사용하려면 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 중 하나를 애플리케이션의 기본 캐시 드라이버로 사용해야 합니다. 또한 모든 서버가 동일한 중앙 캐시 서버에 연결해야 합니다.

<a name="forcing-migrations-to-run-in-production"></a>
#### 운영 환경에서 강제 마이그레이션 실행

일부 마이그레이션은 데이터를 소실시킬 수 있는 파괴적(destructive) 작업입니다. 이러한 명령어를 운영 데이터베이스에서 실행할 때 실수 방지를 위해 실행 전 확인을 요구합니다. 만약 아무런 확인 없이 강제로 실행하려면 `--force` 플래그를 사용하세요:

```shell
php artisan migrate --force
```

<a name="rolling-back-migrations"></a>
### 마이그레이션 롤백 (Rolling Back Migrations)

가장 최근의 마이그레이션 작업을 롤백하려면 `rollback` Artisan 명령어를 사용할 수 있습니다. 이 명령어는 가장 마지막 "배치"에 포함된 여러 마이그레이션 파일을 되돌립니다:

```shell
php artisan migrate:rollback
```

`step` 옵션을 이용하면 롤백할 마이그레이션 개수를 제한할 수 있습니다. 예를 들어, 마지막 5개의 마이그레이션만 롤백하려면 다음과 같이 실행합니다:

```shell
php artisan migrate:rollback --step=5
```

`batch` 옵션을 이용하면 특정 "배치(batch)"의 마이그레이션만 롤백할 수 있습니다. 이 옵션은 애플리케이션의 `migrations` 데이터베이스 테이블에 있는 batch 값과 일치해야 합니다. 예를 들어, 세 번째 배치의 모든 마이그레이션을 롤백하려면 다음과 같이 실행합니다:

```shell
php artisan migrate:rollback --batch=3
```

롤백 시 실제 실행될 SQL 문장을 미리 확인하고 싶다면 `--pretend` 플래그를 추가하면 됩니다:

```shell
php artisan migrate:rollback --pretend
```

`migrate:reset` 명령어는 애플리케이션의 모든 마이그레이션을 한 번에 롤백합니다:

```shell
php artisan migrate:reset
```

<a name="roll-back-migrate-using-a-single-command"></a>
#### 한 번에 롤백 후 다시 마이그레이션 실행

`migrate:refresh` 명령어는 모든 마이그레이션을 롤백한 뒤 다시 마이그레이션을 실행합니다. 이 명령어는 데이터베이스를 전체적으로 재구성할 때 유용합니다:

```shell
php artisan migrate:refresh

# 데이터베이스를 리프레시하고 모든 시드(seed)를 실행하려면...
php artisan migrate:refresh --seed
```

`step` 옵션을 제공하면 마지막 N개의 마이그레이션만 롤백 및 재실행할 수 있습니다. 예를 들어 마지막 5개의 마이그레이션만 해당 작업을 하려면:

```shell
php artisan migrate:refresh --step=5
```

<a name="drop-all-tables-migrate"></a>
#### 모든 테이블 삭제 후 마이그레이션

`migrate:fresh` 명령어는 데이터베이스의 모든 테이블을 삭제한 뒤, 다시 마이그레이션을 실행합니다:

```shell
php artisan migrate:fresh

php artisan migrate:fresh --seed
```

기본적으로 `migrate:fresh` 명령어는 기본 데이터베이스 연결에서만 테이블을 삭제합니다. 하지만 `--database` 옵션을 사용하여 다른 데이터베이스 연결을 지정할 수도 있습니다. 연결 이름은 애플리케이션의 `database` [설정 파일](/docs/12.x/configuration)에 정의되어 있어야 합니다:

```shell
php artisan migrate:fresh --database=admin
```

> [!WARNING]
> `migrate:fresh` 명령어는 테이블 프리픽스(prefix)와 관계없이 모든 데이터베이스 테이블을 삭제합니다. 다른 애플리케이션과 데이터베이스를 공유하는 환경에서는 이 명령어 사용에 주의해야 합니다.

<a name="tables"></a>
## 테이블 (Tables)

<a name="creating-tables"></a>
### 테이블 생성 (Creating Tables)

새로운 데이터베이스 테이블을 생성하려면 `Schema` 파사드의 `create` 메서드를 사용하세요. `create` 메서드는 두 개의 인자를 받는데, 첫 번째는 테이블 이름, 두 번째는 새로운 테이블을 정의할 수 있도록 `Blueprint` 객체를 받는 클로저입니다:

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

테이블을 생성할 때, [컬럼 메서드](#creating-columns)를 사용하여 원하는 컬럼을 정의할 수 있습니다.

<a name="determining-table-column-existence"></a>
#### 테이블/컬럼/인덱스 존재 여부 확인

`hasTable`, `hasColumn`, `hasIndex` 메서드를 사용해 특정 테이블, 컬럼, 인덱스의 존재를 확인할 수 있습니다:

```php
if (Schema::hasTable('users')) {
    // "users" 테이블이 존재합니다...
}

if (Schema::hasColumn('users', 'email')) {
    // "users" 테이블이 존재하고 "email" 컬럼이 있습니다...
}

if (Schema::hasIndex('users', ['email'], 'unique')) {
    // "users" 테이블에 "email" 컬럼이 unique 인덱스로 있습니다...
}
```

<a name="database-connection-table-options"></a>
#### 데이터베이스 연결 및 테이블 옵션

기본 연결이 아닌 다른 데이터베이스 연결에서 스키마 작업을 수행하려면 `connection` 메서드를 사용하면 됩니다:

```php
Schema::connection('sqlite')->create('users', function (Blueprint $table) {
    $table->id();
});
```

그 외에도 몇 가지 속성 및 메서드를 활용해 테이블 생성시 옵션을 지정할 수 있습니다. 예를 들어 MariaDB 또는 MySQL을 사용할 때 테이블 저장 엔진을 지정하려면 `engine` 속성을 사용합니다:

```php
Schema::create('users', function (Blueprint $table) {
    $table->engine('InnoDB');

    // ...
});
```

문자셋과 정렬 방식은 `charset`, `collation` 속성으로 지정할 수 있습니다:

```php
Schema::create('users', function (Blueprint $table) {
    $table->charset('utf8mb4');
    $table->collation('utf8mb4_unicode_ci');

    // ...
});
```

`temporary` 메서드를 호출하면 해당 테이블을 임시 테이블로 생성합니다. 임시 테이블은 현재 커넥션의 세션에서만 보이며, 커넥션이 종료될 때 자동으로 삭제됩니다:

```php
Schema::create('calculations', function (Blueprint $table) {
    $table->temporary();

    // ...
});
```

테이블에 코멘트를 추가하고 싶다면 `comment` 메서드를 사용할 수 있습니다. 테이블 코멘트는 현재 MariaDB, MySQL, PostgreSQL에서만 지원됩니다:

```php
Schema::create('calculations', function (Blueprint $table) {
    $table->comment('Business calculations');

    // ...
});
```

<a name="updating-tables"></a>
### 테이블 수정 (Updating Tables)

`Schema` 파사드의 `table` 메서드는 기존 테이블을 수정할 때 사용합니다. `create` 메서드와 마찬가지로, 첫 번째 인자는 테이블 이름, 두 번째 인자는 컬럼이나 인덱스를 정의할 수 있는 `Blueprint` 인스턴스를 받는 클로저입니다:

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

기존 테이블을 삭제할 때는 `drop` 또는 `dropIfExists` 메서드를 사용할 수 있습니다:

```php
Schema::drop('users');

Schema::dropIfExists('users');
```

<a name="renaming-tables-with-foreign-keys"></a>
#### 외래 키가 있는 테이블 이름 변경

테이블 이름을 변경하기 전에, 해당 테이블의 외래 키 제약조건 이름이 관습적인 방식이 아닌, 마이그레이션 파일에서 명시적으로 지정되었는지 반드시 확인해야 합니다. 그렇지 않으면 외래 키 제약조건의 이름이 예전 테이블 이름을 참조하게 됩니다.

<a name="columns"></a>
## 컬럼 (Columns)

<a name="creating-columns"></a>
### 컬럼 생성 (Creating Columns)

`Schema` 파사드의 `table` 메서드를 사용하면 기존 테이블에 컬럼을 추가할 수 있습니다. 사용법은 `create` 메서드와 같으며, 테이블 이름과 컬럼을 정의할 수 있는 `Illuminate\Database\Schema\Blueprint` 인스턴스를 받는 클로저를 인자로 전달합니다:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->integer('votes');
});
```

<a name="available-column-types"></a>
### 사용 가능한 컬럼 타입 (Available Column Types)

스키마 빌더의 블루프린트는 데이터베이스 테이블에 추가할 수 있는 다양한 컬럼 타입에 해당하는 여러 메서드를 제공합니다. 다음 표에는 사용 가능한 모든 메서드가 나와 있습니다:

#### 불리언 타입 (Boolean Types)

<div class="collection-method-list" markdown="1">

[boolean](#column-method-boolean)

</div>

#### 문자열/텍스트 타입 (String & Text Types)

<div class="collection-method-list" markdown="1">

[char](#column-method-char)
[longText](#column-method-longText)
[mediumText](#column-method-mediumText)
[string](#column-method-string)
[text](#column-method-text)
[tinyText](#column-method-tinyText)

</div>

#### 숫자 타입 (Numeric Types)

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

#### 날짜/시간 타입 (Date & Time Types)

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

#### 바이너리 타입 (Binary Types)

<div class="collection-method-list" markdown="1">

[binary](#column-method-binary)

</div>

#### 객체/JSON 타입 (Object & Json Types)

<div class="collection-method-list" markdown="1">

[json](#column-method-json)
[jsonb](#column-method-jsonb)

</div>

#### UUID, ULID 타입 (UUID & ULID Types)

<div class="collection-method-list" markdown="1">

[ulid](#column-method-ulid)
[ulidMorphs](#column-method-ulidMorphs)
[uuid](#column-method-uuid)
[uuidMorphs](#column-method-uuidMorphs)
[nullableUlidMorphs](#column-method-nullableUlidMorphs)
[nullableUuidMorphs](#column-method-nullableUuidMorphs)

</div>

#### 공간(Spatial) 타입 (Spatial Types)

<div class="collection-method-list" markdown="1">

[geography](#column-method-geography)
[geometry](#column-method-geometry)

</div>

#### 연관관계 타입 (Relationship Types)

<div class="collection-method-list" markdown="1">

[foreignId](#column-method-foreignId)
[foreignIdFor](#column-method-foreignIdFor)
[foreignUlid](#column-method-foreignUlid)
[foreignUuid](#column-method-foreignUuid)
[morphs](#column-method-morphs)
[nullableMorphs](#column-method-nullableMorphs)

</div>

#### 특수 타입 (Specialty Types)

<div class="collection-method-list" markdown="1">

[enum](#column-method-enum)
[set](#column-method-set)
[macAddress](#column-method-macAddress)
[ipAddress](#column-method-ipAddress)
[rememberToken](#column-method-rememberToken)
[vector](#column-method-vector)

</div>

(이하 모든 컬럼 타입별 메서드 설명 생략 없이 제공, 각 타입/메서드에 대한 설명 및 예제를 참고)

<a name="column-modifiers"></a>
### 컬럼 수정자 (Column Modifiers)

위에서 안내한 컬럼 타입 외에도, 컬럼 생성 시 함께 사용할 수 있는 다양한 "수정자(modifier)"가 있습니다. 예를 들어, 컬럼을 "nullable"로 만들고 싶다면 `nullable` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->string('email')->nullable();
});
```

아래 표는 사용 가능한 모든 컬럼 수정자를 정리한 것입니다. (인덱스 수정자는 포함되지 않음)

<div class="overflow-auto">

| 수정자                                | 설명                                                                                |
| ----------------------------------- | ----------------------------------------------------------------------------------- |
| `->after('column')`                 | 컬럼을 다른 컬럼 "뒤에" 위치시킴 (MariaDB/MySQL).                                    |
| `->autoIncrement()`                 | `INTEGER` 컬럼을 자동 증가(기본키)로 설정.                                           |
| `->charset('utf8mb4')`              | 컬럼의 문자셋을 지정 (MariaDB/MySQL).                                                |
| `->collation('utf8mb4_unicode_ci')` | 컬럼의 정렬 기준을 지정.                                                             |
| `->comment('my comment')`           | 컬럼에 코멘트를 추가 (MariaDB/MySQL/PostgreSQL).                                     |
| `->default($value)`                 | 컬럼의 기본값을 지정.                                                               |
| `->first()`                         | 컬럼을 테이블의 "첫번째"로 위치시킴 (MariaDB/MySQL).                                 |
| `->from($integer)`                  | 자동 증가 필드의 시작 값을 지정 (MariaDB/MySQL/PostgreSQL).                          |
| `->invisible()`                     | 컬럼을 `SELECT *` 쿼리에서 보이지 않게 함 (MariaDB/MySQL).                          |
| `->nullable($value = true)`         | 컬럼에 `NULL` 값을 허용.                                                             |
| `->storedAs($expression)`           | 저장(Stored) 생성 컬럼 생성 (MariaDB/MySQL/PostgreSQL/SQLite).                       |
| `->unsigned()`                      | `INTEGER` 컬럼을 `UNSIGNED`로 설정 (MariaDB/MySQL).                                  |
| `->useCurrent()`                    | `TIMESTAMP` 컬럼의 기본값을 `CURRENT_TIMESTAMP`로 설정.                              |
| `->useCurrentOnUpdate()`            | 레코드 업데이트 시 `TIMESTAMP`을 `CURRENT_TIMESTAMP`로 자동 업데이트 (MariaDB/MySQL). |
| `->virtualAs($expression)`          | 가상(Virtual) 생성 컬럼 생성 (MariaDB/MySQL/SQLite).                                 |
| `->generatedAs($expression)`        | 지정한 시퀀스 옵션으로 정체성(identity) 컬럼 생성 (PostgreSQL).                       |
| `->always()`                        | identity 컬럼에서 시퀀스 값 우선 사용 정의 (PostgreSQL).                             |

</div>

<a name="default-expressions"></a>
#### 기본값(디폴트) 표현식

`default` 수정자는 값 또는 `Illuminate\Database\Query\Expression` 인스턴스를 인자로 받을 수 있습니다. `Expression`을 사용하면 값이 따옴표로 감싸지지 않아, DB 특화 함수를 활용할 수 있습니다. 예를 들어 JSON 컬럼에 기본값을 지정하는 상황이 있습니다:

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
> 기본값 표현식 지원 여부는 데이터베이스 드라이버, 데이터베이스 버전, 필드 타입에 따라 다를 수 있습니다. 관련 데이터베이스의 공식 문서를 반드시 참고하세요.

<a name="column-order"></a>
#### 컬럼 순서

MariaDB 또는 MySQL에서 컬럼을 기존 컬럼 뒤에 추가하고 싶을 때는 `after` 메서드를 사용할 수 있습니다:

```php
$table->after('password', function (Blueprint $table) {
    $table->string('address_line1');
    $table->string('address_line2');
    $table->string('city');
});
```

<a name="modifying-columns"></a>
### 컬럼 수정 (Modifying Columns)

`change` 메서드를 사용하면 기존 컬럼의 타입, 속성 등을 수정할 수 있습니다. 예를 들어, `string` 컬럼의 길이를 늘리고 싶을 때 다음과 같이 작성합니다:

```php
Schema::table('users', function (Blueprint $table) {
    $table->string('name', 50)->change();
});
```

컬럼을 수정할 때는 유지하고자 하는 모든 수정자(modifier)를 명시적으로 다시 지정해야 하며, 누락된 속성은 사라집니다. 예를 들어, `unsigned`, `default`, `comment` 속성을 유지하려면 아래와 같이 모든 수정자를 명시해야 합니다:

```php
Schema::table('users', function (Blueprint $table) {
    $table->integer('votes')->unsigned()->default(1)->comment('my comment')->change();
});
```

`change` 메서드는 컬럼의 인덱스에는 영향을 주지 않으므로, 인덱스 변경이 필요하다면 명시적으로 인덱스 수정자를 추가하거나 제거해야 합니다:

```php
// 인덱스 추가...
$table->bigIncrements('id')->primary()->change();

// 인덱스 제거...
$table->char('postal_code', 10)->unique(false)->change();
```

<a name="renaming-columns"></a>
### 컬럼 이름 변경 (Renaming Columns)

컬럼 이름을 변경하려면, 스키마 빌더의 `renameColumn` 메서드를 사용하세요:

```php
Schema::table('users', function (Blueprint $table) {
    $table->renameColumn('from', 'to');
});
```

<a name="dropping-columns"></a>
### 컬럼 삭제 (Dropping Columns)

컬럼을 삭제하려면 스키마 빌더의 `dropColumn` 메서드를 사용하세요:

```php
Schema::table('users', function (Blueprint $table) {
    $table->dropColumn('votes');
});
```

여러 컬럼을 한 번에 삭제하려면 배열 형태로 컬럼명을 전달할 수 있습니다:

```php
Schema::table('users', function (Blueprint $table) {
    $table->dropColumn(['votes', 'avatar', 'location']);
});
```

<a name="available-command-aliases"></a>
#### 사용 가능한 편의 명령어

Laravel은 자주 사용하는 컬럼 삭제와 관련된 편리한 메서드들을 제공합니다. 다음 표를 참고하세요:

<div class="overflow-auto">

| 명령어                                | 설명                                             |
| ----------------------------------- | ------------------------------------------------ |
| `$table->dropMorphs('morphable');`  | `morphable_id` 및 `morphable_type` 컬럼 삭제      |
| `$table->dropRememberToken();`      | `remember_token` 컬럼 삭제                       |
| `$table->dropSoftDeletes();`        | `deleted_at` 컬럼 삭제                           |
| `$table->dropSoftDeletesTz();`      | `dropSoftDeletes()` 메서드의 별칭                 |
| `$table->dropTimestamps();`         | `created_at`, `updated_at` 컬럼 삭제              |
| `$table->dropTimestampsTz();`       | `dropTimestamps()` 메서드의 별칭                  |

</div>

<a name="indexes"></a>
## 인덱스 (Indexes)

<a name="creating-indexes"></a>
### 인덱스 생성 (Creating Indexes)

Laravel 스키마 빌더는 여러 가지 인덱스 타입을 지원합니다. 예를 들어, 새로 추가하는 `email` 컬럼에 유니크 값을 강제하려면, 컬럼 정의에 유니크 메서드를 체이닝할 수 있습니다:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->string('email')->unique();
});
```

컬럼을 정의한 뒤, 별도로 인덱스를 생성하려면 스키마 빌더 블루프린트의 메서드를 사용할 수 있습니다:

```php
$table->unique('email');
```

여러 컬럼을 배열로 전달해 복합(Composite) 인덱스를 생성할 수도 있습니다:

```php
$table->index(['account_id', 'created_at']);
```

인덱스는 Laravel이 기본적으로 테이블명, 컬럼명, 인덱스 종류를 조합해 이름을 자동 생성하지만, 두 번째 인자를 입력해 원하는 인덱스 이름을 지정할 수도 있습니다:

```php
$table->unique('email', 'unique_email');
```

<a name="available-index-types"></a>
#### 지원되는 인덱스 타입

Laravel 스키마 빌더 블루프린트 클래스에는 여러 인덱스 생성 메서드가 제공됩니다. 메서드의 두 번째 인자로 인덱스의 이름을 지정할 수 있으며, 생략하면 테이블명과 컬럼명 그리고 인덱스 종류 조합으로 자동 생성됩니다. 주요 메서드는 다음과 같습니다:

<div class="overflow-auto">

| 명령어                                          | 설명                                                        |
| -------------------------------------------- | ----------------------------------------------------------- |
| `$table->primary('id');`                     | 기본키 추가                                                 |
| `$table->primary(['id', 'parent_id']);`      | 복합키(composite key) 추가                                  |
| `$table->unique('email');`                   | 유니크 인덱스 추가                                          |
| `$table->index('state');`                    | 일반 인덱스 추가                                            |
| `$table->fullText('body');`                  | 전문(full text) 인덱스 추가 (MariaDB/MySQL/PostgreSQL)      |
| `$table->fullText('body')->language('english');` | 특정 언어로 전문 인덱스 추가 (PostgreSQL)                |
| `$table->spatialIndex('location');`          | 공간(spatial) 인덱스 추가 (SQLite 제외)                     |

</div>

<a name="renaming-indexes"></a>
### 인덱스 이름 변경 (Renaming Indexes)

인덱스의 이름을 변경하려면, 스키마 빌더 블루프린트의 `renameIndex` 메서드를 사용하면 됩니다. 첫 번째 인자는 기존 인덱스 이름, 두 번째 인자는 새 인덱스 이름입니다:

```php
$table->renameIndex('from', 'to')
```

<a name="dropping-indexes"></a>
### 인덱스 삭제 (Dropping Indexes)

인덱스를 삭제하려면, 해당 인덱스의 이름을 명시적으로 지정해야 합니다. Laravel은 인덱스 생성 시 테이블 이름, 컬럼명, 인덱스 종류를 조합해 기본 이름을 지정합니다. 예시는 다음과 같습니다:

<div class="overflow-auto">

| 명령어                                         | 설명                                                   |
| -------------------------------------------- | ------------------------------------------------------ |
| `$table->dropPrimary('users_id_primary');`   | "users" 테이블의 기본키 삭제                            |
| `$table->dropUnique('users_email_unique');`  | "users" 테이블의 유니크 인덱스 삭제                    |
| `$table->dropIndex('geo_state_index');`      | "geo" 테이블의 인덱스 삭제                             |
| `$table->dropFullText('posts_body_fulltext');` | "posts" 테이블의 전문 인덱스 삭제                    |
| `$table->dropSpatialIndex('geo_location_spatialindex');` | "geo" 테이블의 공간 인덱스 삭제 (SQLite 제외)    |

</div>

여러 컬럼을 배열로 전달해 인덱스 삭제를 요청하면, Laravel이 conventional(관례적)한 인덱스 이름을 자동으로 생성하여 삭제합니다:

```php
Schema::table('geo', function (Blueprint $table) {
    $table->dropIndex(['state']); // 'geo_state_index' 인덱스 삭제
});
```

<a name="foreign-key-constraints"></a>
### 외래 키 제약조건 (Foreign Key Constraints)

Laravel은 데이터베이스 레벨에서 참조 무결성을 강제하는 외래 키 제약조건도 지원합니다. 예를 들어, `posts` 테이블의 `user_id` 컬럼이 `users` 테이블의 `id` 컬럼을 참조하도록 정의할 수 있습니다:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('posts', function (Blueprint $table) {
    $table->unsignedBigInteger('user_id');

    $table->foreign('user_id')->references('id')->on('users');
});
```

이 방식이 다소 장황하므로, Laravel에서는 더 간결하고 관행적인 메서드를 추가로 제공합니다. `foreignId` 메서드를 사용하여 위 구문을 더 짧게 쓸 수도 있습니다:

```php
Schema::table('posts', function (Blueprint $table) {
    $table->foreignId('user_id')->constrained();
});
```

`foreignId`는 `UNSIGNED BIGINT` 타입의 컬럼을 만들고, `constrained` 메서드는 관례를 이용해 참조할 테이블과 컬럼을 자동으로 지정합니다. 만약 테이블 이름이 Laravel 관례와 다르다면 명시적으로 지정할 수 있으며, 생성될 인덱스의 이름도 지정 가능합니다:

```php
Schema::table('posts', function (Blueprint $table) {
    $table->foreignId('user_id')->constrained(
        table: 'users', indexName: 'posts_user_id'
    );
});
```

"on delete"나 "on update" 속성도 원하는 동작을 지정할 수 있습니다:

```php
$table->foreignId('user_id')
    ->constrained()
    ->onUpdate('cascade')
    ->onDelete('cascade');
```

아래와 같은 더 간결한 메서드도 사용할 수 있습니다:

<div class="overflow-auto">

| 메서드                      | 설명                                          |
| --------------------------- | --------------------------------------------- |
| `$table->cascadeOnUpdate();`  | 업데이트 시 연쇄(CASCADE) 동작                |
| `$table->restrictOnUpdate();` | 업데이트 시 제한(RESTRICT)                     |
| `$table->nullOnUpdate();`     | 업데이트 시 외래 키 값을 NULL로 설정           |
| `$table->noActionOnUpdate();` | 업데이트 시 별도의 동작 안함                   |
| `$table->cascadeOnDelete();`  | 삭제 시 연쇄(CASCADE) 동작                    |
| `$table->restrictOnDelete();` | 삭제 시 제한(RESTRICT)                         |
| `$table->nullOnDelete();`     | 삭제 시 외래 키 값을 NULL로 설정               |
| `$table->noActionOnDelete();` | 자식 레코드 있으면 삭제 방지(NO ACTION)         |

</div>

추가적인 [컬럼 수정자](#column-modifiers)는 반드시 `constrained` 메서드 호출 이전에 체이닝해야 합니다:

```php
$table->foreignId('user_id')
    ->nullable()
    ->constrained();
```

<a name="dropping-foreign-keys"></a>
#### 외래 키 삭제

외래 키를 삭제하려면, `dropForeign` 메서드에 삭제할 외래 키 제약조건의 이름을 인자로 전달해야 합니다. 외래 키 제약조건은 테이블명, 컬럼명 뒤에 "_foreign"이라는 접미사가 붙는 관례적 이름을 사용합니다:

```php
$table->dropForeign('posts_user_id_foreign');
```

또는 외래 키가 적용된 컬럼 이름을 배열로 전달하면, Laravel이 내부적으로 관례에 맞게 제약조건 이름을 자동 생성합니다:

```php
$table->dropForeign(['user_id']);
```

<a name="toggling-foreign-key-constraints"></a>
#### 외래 키 제약조건 활성화/비활성화

마이그레이션 과정에서 다음과 같은 메서드로 외래 키 제약조건을 활성화 또는 비활성화할 수 있습니다:

```php
Schema::enableForeignKeyConstraints();

Schema::disableForeignKeyConstraints();

Schema::withoutForeignKeyConstraints(function () {
    // 이 클로저 내부에서만 제약조건이 비활성화됨...
});
```

> [!WARNING]
> SQLite는 기본적으로 외래 키 제약조건이 비활성화되어 있습니다. SQLite를 사용할 경우 마이그레이션에서 외래 키 생성을 시도하기 전에 반드시 [외래 키 지원 설정](/docs/12.x/database#configuration)에서 활성화해야 합니다.

<a name="events"></a>
## 이벤트 (Events)

편의상, 각 마이그레이션 작업은 [이벤트](/docs/12.x/events)를 디스패치합니다. 아래의 모든 이벤트는 기본 `Illuminate\Database\Events\MigrationEvent` 클래스를 확장합니다:

<div class="overflow-auto">

| 클래스명                                         | 설명                                         |
| ---------------------------------------------- | -------------------------------------------- |
| `Illuminate\Database\Events\MigrationsStarted`   | 한 번에 여러 마이그레이션 실행 직전            |
| `Illuminate\Database\Events\MigrationsEnded`     | 한 번에 여러 마이그레이션 실행 완료            |
| `Illuminate\Database\Events\MigrationStarted`    | 단일 마이그레이션 실행 직전                   |
| `Illuminate\Database\Events\MigrationEnded`      | 단일 마이그레이션 실행 완료                   |
| `Illuminate\Database\Events\NoPendingMigrations` | 실행할 대기 중인 마이그레이션이 없는 경우       |
| `Illuminate\Database\Events\SchemaDumped`        | 데이터베이스 스키마 덤프가 완료된 경우          |
| `Illuminate\Database\Events\SchemaLoaded`        | 기존 데이터베이스 스키마 덤프가 로드된 경우      |

</div>
