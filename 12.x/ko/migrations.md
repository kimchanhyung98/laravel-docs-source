# 데이터베이스: 마이그레이션 (Database: Migrations)

- [소개](#introduction)
- [마이그레이션 생성](#generating-migrations)
    - [마이그레이션 스쿼시](#squashing-migrations)
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
    - [외래 키 제약 조건](#foreign-key-constraints)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

마이그레이션은 데이터베이스를 위한 버전 관리와 같으며, 팀원이 애플리케이션의 데이터베이스 스키마 정의를 공유하고 정의할 수 있도록 합니다. 만약 소스 컨트롤에서 변경사항을 받아온 후에 동료에게 로컬 데이터베이스 스키마에 컬럼을 수동으로 추가하라고 말했던 경험이 있다면, 데이터베이스 마이그레이션이 해결하는 문제를 직접 겪은 것입니다.

Laravel의 `Schema` [퍼사드](/docs/12.x/facades)는 Laravel에서 지원하는 모든 데이터베이스 시스템에서 데이터베이스에 독립적인 테이블 생성 및 조작을 지원합니다. 보통 마이그레이션은 이 퍼사드를 사용해 데이터베이스 테이블과 컬럼을 생성 및 수정합니다.

<a name="generating-migrations"></a>
## 마이그레이션 생성

`make:migration` [Artisan 명령어](/docs/12.x/artisan)를 사용하여 데이터베이스 마이그레이션을 생성할 수 있습니다. 새 마이그레이션 파일은 `database/migrations` 디렉토리에 저장됩니다. 각 마이그레이션 파일명에는 타임스탬프가 포함되어 있어 Laravel이 마이그레이션 실행 순서를 판단할 수 있습니다:

```shell
php artisan make:migration create_flights_table
```

Laravel은 마이그레이션 이름에서 테이블 이름과 해당 마이그레이션이 새 테이블을 생성하는지 여부를 추측하려 합니다. 테이블 이름이 추론 가능하면, 마이그레이션 파일이 지정된 테이블명으로 자동 생성됩니다. 그렇지 않으면 마이그레이션 파일 내에서 직접 테이블명을 지정할 수 있습니다.

만약 생성되는 마이그레이션 파일의 경로를 직접 지정하고 싶다면, `make:migration` 명령어 실행 시 `--path` 옵션을 사용할 수 있습니다. 경로는 애플리케이션 기본 경로(base path)를 기준으로 합니다.

> [!NOTE]
> 마이그레이션 템플릿은 [stub publishing](/docs/12.x/artisan#stub-customization)을 통해 커스터마이징할 수 있습니다.

<a name="squashing-migrations"></a>
### 마이그레이션 스쿼시

애플리케이션 개발이 진행됨에 따라 마이그레이션 파일이 점점 누적되어 `database/migrations` 디렉토리가 수백 개의 파일로 부풀어질 수 있습니다. 필요하다면, 모든 마이그레이션을 하나의 SQL 파일로 "스쿼시"할 수 있습니다. 시작하려면 `schema:dump` 명령어를 실행하세요:

```shell
php artisan schema:dump

# 현재 데이터베이스 스키마를 덤프하고 기존 마이그레이션을 모두 정리...
php artisan schema:dump --prune
```

이 명령어를 실행하면 Laravel은 `database/schema` 디렉토리에 "스키마" 파일을 작성합니다. 이 파일명은 데이터베이스 연결명과 일치합니다. 이제 데이터베이스를 마이그레이션할 때, 실행된 마이그레이션이 없으면 Laravel이 먼저 사용 중인 데이터베이스 연결의 스키마 파일 내 SQL 문을 실행합니다. 이후 스키마 덤프에 포함되지 않은 남은 마이그레이션들을 실행합니다.

애플리케이션 테스트가 일반 로컬 개발과 다른 데이터베이스 연결을 쓴다면, 해당 연결로도 스키마 파일을 덤프해 테스트에서 데이터베이스 구조를 올바르게 생성할 수 있게 해야 합니다. 보통 로컬 개발 연결을 덤프한 뒤 다음과 같이 실행합니다:

```shell
php artisan schema:dump
php artisan schema:dump --database=testing --prune
```

마이그레이션 스키마 파일은 소스 컨트롤에 커밋하는 것이 좋습니다. 팀의 신규 개발자가 빠르게 초기 데이터베이스 구조를 만들 수 있습니다.

> [!WARNING]
> 마이그레이션 스쿼시는 MariaDB, MySQL, PostgreSQL, SQLite 데이터베이스만 지원하며, 데이터베이스의 커맨드 라인 클라이언트를 이용합니다.

<a name="migration-structure"></a>
## 마이그레이션 구조

마이그레이션 클래스는 두 가지 메서드를 갖습니다: `up`과 `down`. `up` 메서드는 데이터베이스에 새로운 테이블, 컬럼, 인덱스를 추가하는 데 사용되며, `down` 메서드는 `up`에서 실행한 작업을 되돌리는 역할을 합니다.

이 두 메서드 내에서 Laravel 스키마 빌더를 사용해 테이블을 표현력 있게 생성 및 수정할 수 있습니다. `Schema` 빌더의 모든 메서드 목록을 보려면 [문서](#creating-tables)를 참고하세요. 예를 들어, 아래 마이그레이션은 `flights` 테이블을 생성합니다:

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

마이그레이션이 애플리케이션 기본 데이터베이스 연결이 아닌 다른 연결과 상호작용할 경우, 마이그레이션 클래스의 `$connection` 속성을 설정해야 합니다:

```php
/**
 * 마이그레이션에 사용할 데이터베이스 연결.
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

때로는 마이그레이션이 아직 활성화되지 않은 기능을 지원하기 위해 작성되어, 실행하지 않길 원할 수도 있습니다. 이런 경우 마이그레이션 클래스 내에 `shouldRun` 메서드를 정의할 수 있습니다. `shouldRun`이 `false`를 반환하면 해당 마이그레이션은 건너뜁니다:

```php
use App\Models\Flights;
use Laravel\Pennant\Feature;

/**
 * 이 마이그레이션을 실행할지 결정합니다.
 */
public function shouldRun(): bool
{
    return Feature::active(Flights::class);
}
```

<a name="running-migrations"></a>
## 마이그레이션 실행

모든 미실행 마이그레이션을 실행하려면 `migrate` Artisan 명령어를 사용하세요:

```shell
php artisan migrate
```

지금까지 어떤 마이그레이션이 실행되었는지 확인하려면 `migrate:status` 명령어를 사용할 수 있습니다:

```shell
php artisan migrate:status
```

실제로 실행하진 않고 어떤 SQL이 실행될지 보고 싶다면 `--pretend` 플래그를 추가하세요:

```shell
php artisan migrate --pretend
```

#### 마이그레이션 실행 격리

애플리케이션을 여러 서버에 배포하고 마이그레이션을 배포 과정에서 실행하는 경우, 두 서버가 동시에 마이그레이션을 실행하려 하는 상황을 피하고 싶을 것입니다. 이럴 때 `migrate` 명령어 실행 시 `--isolated` 옵션을 사용할 수 있습니다.

`isolated` 옵션이 제공되면, Laravel은 애플리케이션 캐시 드라이버를 이용해 원자적 락(atomic lock)을 획득한 뒤 마이그레이션을 실행합니다. 락이 잡혀 있는 동안 다른 `migrate` 명령 실행 시도는 실행되지 않고, 커맨드는 성공 상태 코드로 종료됩니다:

```shell
php artisan migrate --isolated
```

> [!WARNING]
> 이 기능을 사용하려면 애플리케이션 기본 캐시 드라이버가 `memcached`, `redis`, `dynamodb`, `database`, `file`, 또는 `array`여야 합니다. 또한 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

<a name="forcing-migrations-to-run-in-production"></a>
#### 운영 환경에서 마이그레이션 강제 실행

일부 마이그레이션 작업은 파괴적일 수 있어 데이터 손실이 발생할 수 있습니다. 운영 환경 데이터베이스에서 실수로 실행하지 않도록, 실행 전 확인을 요청합니다. 확인 없이 강제로 실행하려면 `--force` 플래그를 사용하세요:

```shell
php artisan migrate --force
```

<a name="rolling-back-migrations"></a>
### 마이그레이션 롤백

가장 최근에 실행한 마이그레이션 작업을 되돌리려면 `rollback` Artisan 명령어를 사용하세요. 이 명령은 마지막 "배치"에 포함된 모든 마이그레이션을 롤백합니다:

```shell
php artisan migrate:rollback
```

`rollback` 명령어에 `step` 옵션을 추가해 제한된 수의 마이그레이션만 롤백할 수 있습니다. 예를 들어 마지막 5개 마이그레이션을 롤백하려면:

```shell
php artisan migrate:rollback --step=5
```

`batch` 옵션을 이용하면 특정 배치 번호에 해당하는 마이그레이션만 롤백할 수 있습니다. 예를 들어, 배치 3에 해당하는 마이그레이션을 모두 롤백하려면:

```shell
php artisan migrate:rollback --batch=3
```

실제로 롤백하지 않고 어떤 SQL이 실행되는지 보려면 `--pretend` 플래그를 추가하세요:

```shell
php artisan migrate:rollback --pretend
```

`migrate:reset` 명령어는 애플리케이션 마이그레이션을 모두 롤백합니다:

```shell
php artisan migrate:reset
```

<a name="roll-back-migrate-using-a-single-command"></a>
#### 한 번에 롤백 및 마이그레이션 실행

`migrate:refresh` 명령어는 모든 마이그레이션을 롤백한 뒤, 다시 `migrate` 명령어를 실행합니다. 데이터베이스를 전체 재생성하는 효과가 있습니다:

```shell
php artisan migrate:refresh

# 데이터베이스 리프레시 후 시더 실행...
php artisan migrate:refresh --seed
```

마지막 몇 개의 마이그레이션만 롤백 후 재적용하려면 `step` 옵션을 사용하세요. 예를 들어 마지막 5개만 다시 마이그레이션 하려면:

```shell
php artisan migrate:refresh --step=5
```

<a name="drop-all-tables-migrate"></a>
#### 모든 테이블 삭제 후 마이그레이션

`migrate:fresh` 명령어는 데이터베이스의 모든 테이블을 삭제한 뒤 `migrate` 명령어를 실행합니다:

```shell
php artisan migrate:fresh

php artisan migrate:fresh --seed
```

기본적으로 `migrate:fresh`는 기본 데이터베이스 연결에서만 테이블을 삭제합니다. 다른 연결을 지정하려면 `--database` 옵션을 사용합니다. 연결명은 `database` [설정 파일](/docs/12.x/configuration)에 정의된 연결명과 일치해야 합니다:

```shell
php artisan migrate:fresh --database=admin
```

> [!WARNING]
> `migrate:fresh` 명령어는 테이블 접두어(prefix)와 관계없이 모든 데이터베이스 테이블을 삭제합니다. 다른 애플리케이션과 공유하는 데이터베이스에서는 주의해서 사용하세요.

<a name="tables"></a>
## 테이블

<a name="creating-tables"></a>
### 테이블 생성

새 데이터베이스 테이블을 생성하려면 `Schema` 퍼사드의 `create` 메서드를 사용하세요. `create` 메서드는 두 개의 인수를 받는데 첫 번째는 테이블 이름, 두 번째는 `Blueprint` 객체를 인자로 받는 클로저입니다. 이 `Blueprint` 객체를 통해 새 테이블을 정의할 수 있습니다:

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

테이블 생성 시, [컬럼 메서드](#creating-columns) 중 원하는 메서드를 사용하여 컬럼을 정의할 수 있습니다.

<a name="determining-table-column-existence"></a>
#### 테이블 / 컬럼 존재 여부 확인

`hasTable`, `hasColumn`, `hasIndex` 메서드를 사용해 각각 테이블, 컬럼, 인덱스 존재 여부를 확인할 수 있습니다:

```php
if (Schema::hasTable('users')) {
    // "users" 테이블이 존재합니다...
}

if (Schema::hasColumn('users', 'email')) {
    // "users" 테이블이 존재하며 "email" 컬럼이 있습니다...
}

if (Schema::hasIndex('users', ['email'], 'unique')) {
    // "users" 테이블에 "email" 컬럼에 대한 유니크 인덱스가 있습니다...
}
```

<a name="database-connection-table-options"></a>
#### 데이터베이스 연결 및 테이블 옵션

애플리케이션 기본 연결이 아닌 다른 데이터베이스 연결에 대해 스키마 작업을 하려면 `connection` 메서드를 사용하세요:

```php
Schema::connection('sqlite')->create('users', function (Blueprint $table) {
    $table->id();
});
```

테이블 생성 시 다음과 같은 속성 및 메서드로 저장 엔진, 문자셋, 임시 테이블 지정 등이 가능합니다.

MariaDB나 MySQL 사용 시, `engine` 속성으로 저장 엔진을 지정할 수 있습니다:

```php
Schema::create('users', function (Blueprint $table) {
    $table->engine('InnoDB');

    // ...
});
```

`charset`과 `collation` 속성으로 테이블 문자셋과 콜레이션을 지정할 수 있습니다:

```php
Schema::create('users', function (Blueprint $table) {
    $table->charset('utf8mb4');
    $table->collation('utf8mb4_unicode_ci');

    // ...
});
```

`temporary` 메서드를 호출하면 임시 테이블이 생성됩니다. 임시 테이블은 현재 데이터베이스 세션에만 보이며 연결이 종료되면 자동 삭제됩니다:

```php
Schema::create('calculations', function (Blueprint $table) {
    $table->temporary();

    // ...
});
```

테이블에 "코멘트"를 추가하고 싶다면 `comment` 메서드를 사용할 수 있습니다. 현재 MariaDB, MySQL, PostgreSQL에서 지원합니다:

```php
Schema::create('calculations', function (Blueprint $table) {
    $table->comment('Business calculations');

    // ...
});
```

<a name="updating-tables"></a>
### 테이블 업데이트

`Schema` 퍼사드의 `table` 메서드는 기존 테이블을 수정할 때 사용합니다. `create`와 마찬가지로 첫 인수는 테이블명, 두 번째는 `Blueprint` 인스턴스를 받는 클로저입니다. 이 안에서 컬럼이나 인덱스를 추가할 수 있습니다:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->integer('votes');
});
```

<a name="renaming-and-dropping-tables"></a>
### 테이블 이름 변경 / 삭제

기존 테이블 이름을 바꾸려면 `rename` 메서드를 사용하세요:

```php
use Illuminate\Support\Facades\Schema;

Schema::rename($from, $to);
```

테이블을 삭제할 때는 `drop`, 혹은 존재 여부를 체크하며 삭제하는 `dropIfExists`를 사용할 수 있습니다:

```php
Schema::drop('users');

Schema::dropIfExists('users');
```

<a name="renaming-tables-with-foreign-keys"></a>
#### 외래 키가 있는 테이블 이름 변경

테이블 이름을 변경하기 전, 외래 키 제약 조건에 명시적 이름이 지정되어 있는지 확인해야 합니다. 그렇지 않으면 외래 키 이름이 기존 테이블 이름을 참조하여 올바르지 않을 수 있습니다.

<a name="columns"></a>
## 컬럼

<a name="creating-columns"></a>
### 컬럼 생성

기존 테이블에 새 컬럼을 추가하려면 `Schema` 퍼사드의 `table` 메서드를 사용하세요. 첫 인수는 테이블명, 두 번째는 `Illuminate\Database\Schema\Blueprint` 인스턴스를 받는 클로저입니다:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->integer('votes');
});
```

<a name="available-column-types"></a>
### 사용 가능한 컬럼 타입

스키마 빌더 블루프린트는 데이터베이스 컬럼의 다양한 타입을 지원하는 메서드를 제공합니다. 아래 표는 사용할 수 있는 컬럼 타입 메서드 목록입니다.

<a name="booleans-method-list"></a>
#### 부울 타입

<div class="collection-method-list" markdown="1">

[boolean](#column-method-boolean)

</div>

<a name="strings-and-texts-method-list"></a>
#### 문자열 & 텍스트 타입

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
#### 날짜 & 시간 타입

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
#### UUID & ULID 타입

<div class="collection-method-list" markdown="1">

[ulid](#column-method-ulid)
[ulidMorphs](#column-method-ulidMorphs)
[uuid](#column-method-uuid)
[uuidMorphs](#column-method-uuidMorphs)
[nullableUlidMorphs](#column-method-nullableUlidMorphs)
[nullableUuidMorphs](#column-method-nullableUuidMorphs)

</div>

<a name="spatials-method-list"></a>
#### 공간(Spatial) 타입

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

`bigIncrements` 메서드는 자동 증가하는 `UNSIGNED BIGINT` (기본 키) 타입 컬럼을 생성합니다:

```php
$table->bigIncrements('id');
```

<a name="column-method-bigInteger"></a>
#### `bigInteger()`

`bigInteger` 메서드는 `BIGINT` 타입의 컬럼을 생성합니다:

```php
$table->bigInteger('votes');
```

<a name="column-method-binary"></a>
#### `binary()`

`binary` 메서드는 `BLOB` 타입 컬럼을 생성합니다:

```php
$table->binary('photo');
```

MySQL, MariaDB, SQL Server 사용 시 `length`와 `fixed` 인수를 전달하여 `VARBINARY` 혹은 `BINARY` 타입 컬럼을 생성할 수 있습니다:

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

`dateTimeTz` 메서드는 시간대가 포함된 `DATETIME` 타입 컬럼을 생성하며, 소수점 이하 정밀도를 선택할 수 있습니다:

```php
$table->dateTimeTz('created_at', precision: 0);
```

<a name="column-method-dateTime"></a>
#### `dateTime()`

`dateTime` 메서드는 `DATETIME` 타입 컬럼을 생성하며, 소수점 이하 정밀도를 선택할 수 있습니다:

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

`decimal` 메서드는 지정한 전체 자릿수와 소수점 자릿수를 가진 `DECIMAL` 타입 컬럼을 생성합니다:

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

`enum` 메서드는 지정한 값 목록을 유효한 값으로 갖는 `ENUM` 타입 컬럼을 생성합니다:

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

`foreignIdFor` 메서드는 주어진 모델 클래스에 해당하는 `{컬럼}_id` 컬럼을 추가합니다. 컬럼 타입은 모델 키 타입에 따라 `UNSIGNED BIGINT`, `CHAR(36)`, 또는 `CHAR(26)`입니다:

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

`geography` 메서드는 지정한 공간 타입 및 SRID(공간 참조 시스템 식별자)로 `GEOGRAPHY` 타입 컬럼을 생성합니다:

```php
$table->geography('coordinates', subtype: 'point', srid: 4326);
```

> [!NOTE]
> 공간 타입 지원 여부는 데이터베이스 드라이버에 따라 다릅니다. PostgreSQL을 사용할 경우, `geography` 메서드를 사용하려면 [PostGIS](https://postgis.net) 확장 설치가 필요합니다.

<a name="column-method-geometry"></a>
#### `geometry()`

`geometry` 메서드는 지정한 공간 타입 및 SRID로 `GEOMETRY` 타입 컬럼을 생성합니다:

```php
$table->geometry('positions', subtype: 'point', srid: 0);
```

> [!NOTE]
> 공간 타입 지원 여부는 데이터베이스 드라이버에 따라 다릅니다. PostgreSQL의 경우 [PostGIS](https://postgis.net) 확장이 필요합니다.

<a name="column-method-id"></a>
#### `id()`

`id` 메서드는 `bigIncrements` 메서드의 별칭입니다. 기본적으로 `id` 컬럼을 생성하지만, 컬럼명을 변경하려면 이름을 인수로 전달할 수 있습니다:

```php
$table->id();
```

<a name="column-method-increments"></a>
#### `increments()`

`increments` 메서드는 자동 증가하는 `UNSIGNED INTEGER` 기본 키 컬럼을 생성합니다:

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

`ipAddress` 메서드는 `VARCHAR` 타입 컬럼을 생성하며, PostgreSQL 사용 시 `INET` 타입 컬럼이 생성됩니다:

```php
$table->ipAddress('visitor');
```

<a name="column-method-json"></a>
#### `json()`

`json` 메서드는 `JSON` 타입 컬럼을 생성합니다. SQLite 사용 시 `TEXT` 컬럼으로 대체됩니다:

```php
$table->json('options');
```

<a name="column-method-jsonb"></a>
#### `jsonb()`

`jsonb` 메서드는 `JSONB` 타입 컬럼을 생성합니다. SQLite 사용 시 `TEXT` 컬럼으로 대체됩니다:

```php
$table->jsonb('options');
```

<a name="column-method-longText"></a>
#### `longText()`

`longText` 메서드는 `LONGTEXT` 타입 컬럼을 생성합니다:

```php
$table->longText('description');
```

MySQL 또는 MariaDB 사용 시, `binary` 문자셋을 적용해 `LONGBLOB`으로 만들 수 있습니다:

```php
$table->longText('data')->charset('binary'); // LONGBLOB
```

<a name="column-method-macAddress"></a>
#### `macAddress()`

`macAddress` 메서드는 MAC 주소를 저장하기 위한 컬럼을 생성합니다. PostgreSQL 등 일부 데이터베이스는 전용 타입을 사용하며, 그렇지 않은 경우 문자열로 저장됩니다:

```php
$table->macAddress('device');
```

<a name="column-method-mediumIncrements"></a>
#### `mediumIncrements()`

`mediumIncrements` 메서드는 자동증가하는 `UNSIGNED MEDIUMINT` 타입 기본 키 컬럼을 생성합니다:

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

`mediumText` 메서드는 `MEDIUMTEXT` 타입 컬럼을 생성합니다:

```php
$table->mediumText('description');
```

MySQL 혹은 MariaDB 사용 시 `binary` 문자셋을 지정해 `MEDIUMBLOB` 타입으로 생성할 수 있습니다:

```php
$table->mediumText('data')->charset('binary'); // MEDIUMBLOB
```

<a name="column-method-morphs"></a>
#### `morphs()`

`morphs` 메서드는 `{column}_id` 타입과 `{column}_type` `VARCHAR` 타입 컬럼을 한 번에 생성하는 편의 메서드입니다. `{column}_id`는 모델 키 타입에 따라 `UNSIGNED BIGINT`, `CHAR(36)`, `CHAR(26)` 중 하나입니다.

이는 다형성 [Eloquent 관계](/docs/12.x/eloquent-relationships)를 위한 컬럼을 정의할 때 사용합니다. 예를 들어 `taggable_id`와 `taggable_type` 컬럼이 생성됩니다:

```php
$table->morphs('taggable');
```

<a name="column-method-nullableMorphs"></a>
#### `nullableMorphs()`

`morphs` 메서드와 같으나 생성되는 컬럼들이 nullable로 지정됩니다:

```php
$table->nullableMorphs('taggable');
```

<a name="column-method-nullableUlidMorphs"></a>
#### `nullableUlidMorphs()`

`ulidMorphs` 메서드와 같으나 nullable 컬럼을 생성합니다:

```php
$table->nullableUlidMorphs('taggable');
```

<a name="column-method-nullableUuidMorphs"></a>
#### `nullableUuidMorphs()`

`uuidMorphs` 메서드와 같으나 nullable 컬럼을 생성합니다:

```php
$table->nullableUuidMorphs('taggable');
```

<a name="column-method-rememberToken"></a>
#### `rememberToken()`

`rememberToken` 메서드는 nullable한 `VARCHAR(100)` 타입 컬럼을 생성하며, 현재 사용자의 "remember me" [인증 토큰](/docs/12.x/authentication#remembering-users) 저장용입니다:

```php
$table->rememberToken();
```

<a name="column-method-set"></a>
#### `set()`

`set` 메서드는 주어진 값 목록을 유효값으로 갖는 `SET` 타입 컬럼을 생성합니다:

```php
$table->set('flavors', ['strawberry', 'vanilla']);
```

<a name="column-method-smallIncrements"></a>
#### `smallIncrements()`

`smallIncrements` 메서드는 자동 증가하는 `UNSIGNED SMALLINT` 타입 기본 키 컬럼을 생성합니다:

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

`softDeletesTz` 메서드는 nullable한 `deleted_at` 타임스탬프(시간대 포함) 타입 컬럼을 생성하며, Eloquent의 소프트 삭제 기능에 필요한 타임스탬프를 저장합니다:

```php
$table->softDeletesTz('deleted_at', precision: 0);
```

<a name="column-method-softDeletes"></a>
#### `softDeletes()`

`softDeletes` 메서드는 nullable한 `deleted_at` 타임스탬프 타입 컬럼을 생성하며 소프트 삭제용입니다:

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

`text` 메서드는 `TEXT` 타입 컬럼을 생성합니다:

```php
$table->text('description');
```

MySQL이나 MariaDB 사용 시 `binary` 문자셋 지정으로 `BLOB` 타입 컬럼을 생성할 수 있습니다:

```php
$table->text('data')->charset('binary'); // BLOB
```

<a name="column-method-timeTz"></a>
#### `timeTz()`

`timeTz` 메서드는 시간대가 포함된 `TIME` 타입 컬럼을 생성하며 소수점 이하 정밀도를 지정할 수 있습니다:

```php
$table->timeTz('sunrise', precision: 0);
```

<a name="column-method-time"></a>
#### `time()`

`time` 메서드는 `TIME` 타입 컬럼을 생성하며 소수점 이하 정밀도를 지정할 수 있습니다:

```php
$table->time('sunrise', precision: 0);
```

<a name="column-method-timestampTz"></a>
#### `timestampTz()`

`timestampTz` 메서드는 시간대가 포함된 `TIMESTAMP` 타입 컬럼을 생성하며 소수점 이하 정밀도를 지정할 수 있습니다:

```php
$table->timestampTz('added_at', precision: 0);
```

<a name="column-method-timestamp"></a>
#### `timestamp()`

`timestamp` 메서드는 `TIMESTAMP` 타입 컬럼을 생성하며 소수점 이하 정밀도를 지정할 수 있습니다:

```php
$table->timestamp('added_at', precision: 0);
```

<a name="column-method-timestampsTz"></a>
#### `timestampsTz()`

`timestampsTz` 메서드는 `created_at`과 `updated_at` 두 개의 타임스탬프(시간대 포함) 컬럼을 생성하며, 소수점 이하 정밀도를 지정할 수 있습니다:

```php
$table->timestampsTz(precision: 0);
```

<a name="column-method-timestamps"></a>
#### `timestamps()`

`timestamps` 메서드는 `created_at`과 `updated_at` 두 개의 타임스탬프 컬럼을 생성하며, 소수점 이하 정밀도를 지정할 수 있습니다:

```php
$table->timestamps(precision: 0);
```

<a name="column-method-tinyIncrements"></a>
#### `tinyIncrements()`

`tinyIncrements` 메서드는 자동 증가하는 `UNSIGNED TINYINT` 타입 기본 키 컬럼을 생성합니다:

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

`tinyText` 메서드는 `TINYTEXT` 타입 컬럼을 생성합니다:

```php
$table->tinyText('notes');
```

MySQL 또는 MariaDB 사용 시 `binary` 문자셋을 지정해 `TINYBLOB` 컬럼을 생성할 수 있습니다:

```php
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

`ulidMorphs` 메서드는 `{컬럼}_id`에 `CHAR(26)`, `{컬럼}_type`에 `VARCHAR` 타입 컬럼을 생성하는 편의 메서드입니다.

ULID 식별자를 사용하는 다형성 [Eloquent 관계](/docs/12.x/eloquent-relationships)를 정의할 때 사용됩니다. 예를 들어 `taggable_id`와 `taggable_type` 컬럼이 생성됩니다:

```php
$table->ulidMorphs('taggable');
```

<a name="column-method-uuidMorphs"></a>
#### `uuidMorphs()`

`uuidMorphs` 메서드는 `{컬럼}_id`에 `CHAR(36)`, `{컬럼}_type`에 `VARCHAR` 타입 컬럼을 생성하는 편의 메서드입니다.

UUID 식별자를 사용하는 다형성 관계를 정의할 때 사용됩니다:

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

`vector` 메서드는 벡터 데이터 타입 컬럼을 생성합니다:

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
### 컬럼 수정자

앞서 언급한 컬럼 타입 외에도, 컬럼 생성 시 여러 수정자(modifier)를 체이닝하여 사용할 수 있습니다. 예를 들어, 컬럼을 `nullable`하게 만들려면 `nullable` 메서드를 사용합니다:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->string('email')->nullable();
});
```

다음 표는 모든 컬럼 수정자를 나열하며, 인덱스 관련 수정자는 제외했습니다:

<div class="overflow-auto">

| 수정자                              | 설명                                                                                     |
| ----------------------------------- | ----------------------------------------------------------------------------------------- |
| `->after('column')`                 | 컬럼을 다른 컬럼 뒤에 배치 (MariaDB / MySQL).                                            |
| `->autoIncrement()`                 | `INTEGER` 컬럼을 자동증가(기본 키)로 설정.                                               |
| `->charset('utf8mb4')`              | 컬럼에 문자셋 지정 (MariaDB / MySQL).                                                    |
| `->collation('utf8mb4_unicode_ci')` | 컬럼에 콜레이션 지정.                                                                     |
| `->comment('my comment')`           | 컬럼에 코멘트 추가 (MariaDB / MySQL / PostgreSQL).                                       |
| `->default($value)`                 | 컬럼 기본값 지정.                                                                         |
| `->first()`                         | 컬럼을 테이블의 첫 번째 컬럼으로 배치 (MariaDB / MySQL).                                 |
| `->from($integer)`                  | 자동증가 필드 시작값 지정 (MariaDB / MySQL / PostgreSQL).                                |
| `->invisible()`                     | `SELECT *` 쿼리 시 컬럼을 "숨김" 처리 (MariaDB / MySQL).                                 |
| `->nullable($value = true)`         | NULL 값 허용.                                                                             |
| `->storedAs($expression)`           | 저장된 생성 컬럼 생성 (MariaDB / MySQL / PostgreSQL / SQLite).                            |
| `->unsigned()`                      | 정수형 컬럼에 `UNSIGNED` 지정 (MariaDB / MySQL).                                         |
| `->useCurrent()`                    | `TIMESTAMP` 컬럼의 기본값을 `CURRENT_TIMESTAMP`로 지정.                                 |
| `->useCurrentOnUpdate()`            | 레코드 갱신 시 `TIMESTAMP` 컬럼을 `CURRENT_TIMESTAMP`로 갱신 (MariaDB / MySQL).           |
| `->virtualAs($expression)`          | 가상 생성 컬럼 생성 (MariaDB / MySQL / SQLite).                                          |
| `->generatedAs($expression)`        | 식별자 컬럼 생성 및 시퀀스 옵션 지정 (PostgreSQL).                                        |
| `->always()`                        | 시퀀스 값이 입력값보다 우선 적용됨을 명시 (PostgreSQL).                                   |

</div>

<a name="default-expressions"></a>
#### 기본값 표현식

`default` 수정자는 값이나 `Illuminate\Database\Query\Expression` 인스턴스를 받을 수 있습니다. `Expression`을 사용하면 Laravel이 값을 따옴표로 감싸지 않으며 데이터베이스 특정 함수를 사용할 수 있습니다. 특히 JSON 컬럼 기본값 지정 시 유용합니다:

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
> 기본값 표현식 지원 여부는 데이터베이스 드라이버, 버전, 컬럼 타입에 따라 다릅니다. 데이터베이스 문서를 참고하세요.

<a name="column-order"></a>
#### 컬럼 순서 지정

MariaDB 또는 MySQL 데이터베이스 사용 시, `after` 메서드를 이용해 컬럼을 기존 컬럼 뒤에 배치할 수 있습니다:

```php
$table->after('password', function (Blueprint $table) {
    $table->string('address_line1');
    $table->string('address_line2');
    $table->string('city');
});
```

<a name="modifying-columns"></a>
### 컬럼 수정

`change` 메서드를 사용하면 기존 컬럼 타입과 속성을 변경할 수 있습니다. 예를 들어 `name` 컬럼 길이를 25에서 50으로 늘리려면, 새 상태를 정의한 뒤 `change` 메서드를 호출합니다:

```php
Schema::table('users', function (Blueprint $table) {
    $table->string('name', 50)->change();
});
```

수정 시 유지할 모든 수정자(예: `unsigned`, `default`, `comment`)를 명시적으로 포함해야 합니다. 누락된 속성은 제거됩니다:

```php
Schema::table('users', function (Blueprint $table) {
    $table->integer('votes')->unsigned()->default(1)->comment('my comment')->change();
});
```

`change`는 인덱스 상태를 변경하지 않으므로, 인덱스를 새로 추가하거나 삭제하려면 명시적으로 인덱스 수정자를 호출해야 합니다:

```php
// 인덱스 추가...
$table->bigIncrements('id')->primary()->change();

// 인덱스 삭제...
$table->char('postal_code', 10)->unique(false)->change();
```

<a name="renaming-columns"></a>
### 컬럼 이름 변경

컬럼 이름을 변경하려면 스키마 빌더의 `renameColumn` 메서드를 사용하세요:

```php
Schema::table('users', function (Blueprint $table) {
    $table->renameColumn('from', 'to');
});
```

<a name="dropping-columns"></a>
### 컬럼 삭제

컬럼을 삭제하려면 스키마 빌더의 `dropColumn` 메서드를 사용합니다:

```php
Schema::table('users', function (Blueprint $table) {
    $table->dropColumn('votes');
});
```

배열을 전달해 여러 컬럼을 한 번에 삭제할 수도 있습니다:

```php
Schema::table('users', function (Blueprint $table) {
    $table->dropColumn(['votes', 'avatar', 'location']);
});
```

<a name="available-command-aliases"></a>
#### 사용 가능한 명령어 별칭

Laravel은 자주 쓰이는 컬럼 삭제 동작에 대해 편리한 별칭 메서드를 제공합니다. 아래 표에서 각 별칭을 확인하세요:

<div class="overflow-auto">

| 명령어                             | 설명                                   |
| ----------------------------------- | ------------------------------------- |
| `$table->dropMorphs('morphable');`  | `morphable_id` 와 `morphable_type` 컬럼을 삭제합니다. |
| `$table->dropRememberToken();`      | `remember_token` 컬럼을 삭제합니다.  |
| `$table->dropSoftDeletes();`        | `deleted_at` 컬럼을 삭제합니다.      |
| `$table->dropSoftDeletesTz();`      | `dropSoftDeletes()`의 별칭입니다.    |
| `$table->dropTimestamps();`         | `created_at`과 `updated_at` 컬럼을 삭제합니다. |
| `$table->dropTimestampsTz();`       | `dropTimestamps()`의 별칭입니다.     |

</div>

<a name="indexes"></a>
## 인덱스

<a name="creating-indexes"></a>
### 인덱스 생성

Laravel 스키마 빌더는 여러 종류의 인덱스를 지원합니다. 예를 들어 `email` 컬럼을 생성하며 고유 인덱스를 붙이려면, 해당 컬럼 정의에 `unique` 메서드를 체이닝하면 됩니다:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->string('email')->unique();
});
```

또는 컬럼을 정의한 뒤 인덱스를 생성할 수 있습니다. 이 경우 `unique` 메서드에 인덱스를 생성하고자 하는 컬럼명을 전달하세요:

```php
$table->unique('email');
```

복합 인덱스를 만들려면, 컬럼명 배열을 전달하면 됩니다:

```php
$table->index(['account_id', 'created_at']);
```

인덱스 생성 시, Laravel은 테이블명, 컬럼명, 인덱스 타입으로 인덱스명을 자동 생성하지만, 두 번째 인수로 직접 이름을 지정할 수도 있습니다:

```php
$table->unique('email', 'unique_email');
```

<a name="available-index-types"></a>
#### 사용 가능한 인덱스 타입

Laravel 스키마 빌더 클래스는 지원하는 인덱스 타입별 생성 메서드를 제공합니다. 모두 두 번째 인수로 옵션으로 인덱스명 지정 가능하며, 생략 시 기본 네이밍 규칙이 적용됩니다. 각 메서드 기능은 다음과 같습니다:

<div class="overflow-auto">

| 명령어                                   | 설명                                 |
| ----------------------------------------- | ------------------------------------ |
| `$table->primary('id');`                  | 기본 키를 추가합니다.                |
| `$table->primary(['id', 'parent_id']);`  | 복합 기본 키를 추가합니다.          |
| `$table->unique('email');`                | 유니크 인덱스를 추가합니다.         |
| `$table->index('state');`                 | 일반 인덱스를 추가합니다.           |
| `$table->fullText('body');`               | 전문 검색(full text) 인덱스 추가 (MariaDB / MySQL / PostgreSQL). |
| `$table->fullText('body')->language('english');` | 특정 언어 전문 검색 인덱스 추가 (PostgreSQL). |
| `$table->spatialIndex('location');`      | 공간 인덱스 추가 (SQLite 제외).     |

</div>

<a name="renaming-indexes"></a>
### 인덱스 이름 변경

인덱스 이름을 변경하려면 스키마 빌더 `renameIndex` 메서드를 사용하세요. 첫 번째 인수는 기존 인덱스명, 두 번째는 변경할 이름입니다:

```php
$table->renameIndex('from', 'to');
```

<a name="dropping-indexes"></a>
### 인덱스 삭제

인덱스 삭제 시에는 인덱스명을 반드시 지정해야 합니다. Laravel이 기본적으로 생성하는 인덱스명은 테이블명, 컬럼명, 인덱스 타입으로 구성됩니다. 예를 들면 다음과 같습니다:

<div class="overflow-auto">

| 명령어                                            | 설명                           |
| -------------------------------------------------- | ------------------------------ |
| `$table->dropPrimary('users_id_primary');`         | "users" 테이블의 기본 키 삭제. |
| `$table->dropUnique('users_email_unique');`        | "users" 테이블의 유니크 인덱스 삭제. |
| `$table->dropIndex('geo_state_index');`            | "geo" 테이블의 기본 인덱스 삭제. |
| `$table->dropFullText('posts_body_fulltext');`     | "posts" 테이블의 전문 검색 인덱스 삭제. |
| `$table->dropSpatialIndex('geo_location_spatialindex');` | "geo" 테이블의 공간 인덱스 삭제 (SQLite 제외). |

</div>

여러 컬럼 인덱스를 삭제할 경우 배열을 전달하면, 기본 네이밍 규칙에 따라 인덱스명이 생성됩니다:

```php
Schema::table('geo', function (Blueprint $table) {
    $table->dropIndex(['state']); // 'geo_state_index' 인덱스 삭제
});
```

<a name="foreign-key-constraints"></a>
### 외래 키 제약 조건

Laravel은 데이터베이스 수준에서 참조 무결성을 보장하는 외래 키 제약 조건 생성도 지원합니다. 예를 들어 `posts` 테이블에 `user_id` 컬럼을 정의하고, 이를 `users` 테이블 `id` 컬럼과 참조하도록 할 때는 다음과 같이 작성합니다:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('posts', function (Blueprint $table) {
    $table->unsignedBigInteger('user_id');

    $table->foreign('user_id')->references('id')->on('users');
});
```

이 문법은 다소 장황하므로, `foreignId` 메서드를 사용해 더 간결하게 작성할 수 있습니다:

```php
Schema::table('posts', function (Blueprint $table) {
    $table->foreignId('user_id')->constrained();
});
```

`foreignId`는 `UNSIGNED BIGINT` 컬럼을 생성하고, `constrained`는 참조할 테이블과 컬럼을 규칙에 따라 결정합니다. 테이블명이 규칙과 다르면 `constrained`에 직접 명시하며, 생성할 인덱스명도 지정할 수 있습니다:

```php
Schema::table('posts', function (Blueprint $table) {
    $table->foreignId('user_id')->constrained(
        table: 'users', indexName: 'posts_user_id'
    );
});
```

`on delete`와 `on update` 처리 방식도 지정할 수 있습니다:

```php
$table->foreignId('user_id')
    ->constrained()
    ->onUpdate('cascade')
    ->onDelete('cascade');
```

다음과 같은 축약 메서드도 제공합니다:

<div class="overflow-auto">

| 메서드                         | 설명                              |
| ------------------------------ | --------------------------------- |
| `$table->cascadeOnUpdate();`   | 업데이트 시 연쇄 반영              |
| `$table->restrictOnUpdate();`  | 업데이트 제약                     |
| `$table->nullOnUpdate();`      | 업데이트 시 외래키를 NULL로 설정  |
| `$table->noActionOnUpdate();`  | 업데이트 시 아무 동작 안 함       |
| `$table->cascadeOnDelete();`   | 삭제 시 연쇄 삭제                 |
| `$table->restrictOnDelete();`  | 삭제 제약                        |
| `$table->nullOnDelete();`      | 삭제 시 외래키를 NULL로 설정      |
| `$table->noActionOnDelete();`  | 자식 레코드 있을 경우 삭제 방지   |

</div>

추가적인 [컬럼 수정자](#column-modifiers)는 `constrained` 호출 이전에 체이닝해야 합니다:

```php
$table->foreignId('user_id')
    ->nullable()
    ->constrained();
```

<a name="dropping-foreign-keys"></a>
#### 외래 키 삭제

외래 키를 삭제하려면 `dropForeign` 메서드에 삭제할 외래 키 제약 이름을 전달합니다. 외래 키명은 인덱스 명명 규칙을 따르며, 테이블명과 컬럼명 뒤에 `_foreign`가 붙습니다:

```php
$table->dropForeign('posts_user_id_foreign');
```

또는 외래 키 컬럼명을 배열로 넘겨 Laravel이 제약 이름을 규칙에 맞게 생성하도록 할 수 있습니다:

```php
$table->dropForeign(['user_id']);
```

<a name="toggling-foreign-key-constraints"></a>
#### 외래 키 제약 조건 토글

마이그레이션 내에서 외래 키 제약 조건을 활성화하거나 비활성화할 수 있습니다:

```php
Schema::enableForeignKeyConstraints();

Schema::disableForeignKeyConstraints();

Schema::withoutForeignKeyConstraints(function () {
    // 이 클로저 내에서는 제약 조건이 비활성화됩니다...
});
```

> [!WARNING]
> SQLite는 외래 키 제약 조건이 기본적으로 비활성화되어 있습니다. SQLite 사용 시, [구성](/docs/12.x/database#configuration)에서 외래 키 지원을 활성화해야 마이그레이션 내에서 외래 키를 생성할 수 있습니다.

<a name="events"></a>
## 이벤트

편의를 위해 각 마이그레이션 작업은 [이벤트](/docs/12.x/events)를 디스패치합니다. 아래 이벤트들은 모두 `Illuminate\Database\Events\MigrationEvent` 베이스 클래스를 확장합니다:

<div class="overflow-auto">

| 클래스                                             | 설명                                       |
| -------------------------------------------------- | ------------------------------------------ |
| `Illuminate\Database\Events\MigrationsStarted`    | 마이그레이션 배치 실행 직전 이벤트.       |
| `Illuminate\Database\Events\MigrationsEnded`      | 마이그레이션 배치 실행 완료 후 이벤트.    |
| `Illuminate\Database\Events\MigrationStarted`     | 단일 마이그레이션 실행 직전 이벤트.       |
| `Illuminate\Database\Events\MigrationEnded`       | 단일 마이그레이션 실행 완료 후 이벤트.    |
| `Illuminate\Database\Events\NoPendingMigrations`  | 실행할 대기 마이그레이션이 없음을 알림.   |
| `Illuminate\Database\Events\SchemaDumped`         | 데이터베이스 스키마 덤프 완료 이벤트.     |
| `Illuminate\Database\Events\SchemaLoaded`         | 기존 스키마 덤프 불러오기 완료 이벤트.    |

</div>