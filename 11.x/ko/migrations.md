# 데이터베이스: 마이그레이션 (Database: Migrations)

- [소개](#introduction)
- [마이그레이션 생성하기](#generating-migrations)
    - [마이그레이션 스쿼싱](#squashing-migrations)
- [마이그레이션 구조](#migration-structure)
- [마이그레이션 실행하기](#running-migrations)
    - [마이그레이션 롤백](#rolling-back-migrations)
- [테이블](#tables)
    - [테이블 생성하기](#creating-tables)
    - [테이블 수정하기](#updating-tables)
    - [테이블 이름 변경 / 삭제](#renaming-and-dropping-tables)
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
## 소개 (Introduction)

마이그레이션은 데이터베이스를 위한 버전 관리 시스템과 같습니다. 팀이 애플리케이션의 데이터베이스 스키마를 정의하고 공유할 수 있게 해줍니다. 만약 소스 컨트롤에서 변경 사항을 가져온 후 동료에게 로컬 데이터베이스 스키마에 수동으로 컬럼을 추가하도록 알려야 했던 적이 있다면, 마이그레이션이 해결하는 문제를 경험한 것입니다.

Laravel의 `Schema` [파사드](/docs/11.x/facades)는 Laravel이 지원하는 모든 데이터베이스 시스템에서 테이블을 생성 및 조작할 수 있도록 데이터베이스에 독립적인 지원을 제공합니다. 보통 마이그레이션은 이 파사드를 사용하여 데이터베이스 테이블과 컬럼을 생성하거나 수정합니다.

<a name="generating-migrations"></a>
## 마이그레이션 생성하기 (Generating Migrations)

`make:migration` [Artisan 명령어](/docs/11.x/artisan)를 사용하여 데이터베이스 마이그레이션을 생성할 수 있습니다. 새 마이그레이션 파일은 `database/migrations` 디렉토리에 생성됩니다. 각 마이그레이션 파일명에는 타임스탬프가 포함되어 있어 Laravel이 마이그레이션 수행 순서를 결정할 수 있습니다:

```shell
php artisan make:migration create_flights_table
```

Laravel은 마이그레이션 이름을 기반으로 테이블명을 추측하고, 해당 마이그레이션이 새로운 테이블을 생성하는지 여부를 판단하려고 시도합니다. 테이블 이름을 유추할 수 있으면, 자동으로 생성되는 마이그레이션 파일에 해당 테이블명이 미리 채워집니다. 그렇지 않으면, 마이그레이션 파일 안에서 직접 테이블을 지정하면 됩니다.

생성된 마이그레이션 파일의 경로를 커스텀으로 지정하고 싶다면, `make:migration` 명령을 실행할 때 `--path` 옵션을 사용할 수 있습니다. 지정하는 경로는 애플리케이션 기본 경로를 기준으로 한 상대 경로여야 합니다.

> [!NOTE]  
> 마이그레이션 스텁 파일은 [스텁 퍼블리싱](/docs/11.x/artisan#stub-customization)을 통해 커스터마이징할 수 있습니다.

<a name="squashing-migrations"></a>
### 마이그레이션 스쿼싱 (Squashing Migrations)

애플리케이션을 개발하는 동안 점점 더 많은 마이그레이션이 쌓이게 됩니다. 이로 인해 `database/migrations` 디렉토리가 수백 개가 넘는 파일로 부풀어질 수 있습니다. 필요하다면 여러 마이그레이션을 단일 SQL 파일로 "스쿼싱"할 수 있습니다. 시작하려면 `schema:dump` 명령어를 실행하세요:

```shell
php artisan schema:dump

# 현재 데이터베이스 스키마를 덤프하고 기존 모든 마이그레이션을 정리...
php artisan schema:dump --prune
```

이 명령을 실행하면 Laravel은 데이터베이스 연결에 따라 이름이 지정된 "스키마" 파일을 애플리케이션의 `database/schema` 디렉토리에 작성합니다. 이제 데이터베이스를 마이그레이션할 때 다른 마이그레이션이 실행되지 않은 경우, Laravel은 먼저 해당 데이터베이스 연결의 스키마 파일에 포함된 SQL 문을 실행합니다. 이후 스키마 덤프에 포함되지 않은 나머지 마이그레이션들을 실행합니다.

만약 테스트용 데이터베이스 연결이 로컬 개발 환경과 다르다면, 테스트용 데이터베이스 연결에 대해 스키마 파일을 덤프해두어 테스트 시 데이터베이스를 구축할 수 있도록 해야 합니다. 보통 개발용 데이터베이스 연결을 덤프한 후에 아래처럼 실행합니다:

```shell
php artisan schema:dump
php artisan schema:dump --database=testing --prune
```

데이터베이스 스키마 파일은 소스 컨트롤에 반드시 커밋해야 다른 새 개발자가 애플리케이션의 초기 데이터베이스 구조를 빠르게 만들 수 있습니다.

> [!WARNING]  
> 마이그레이션 스쿼싱은 MariaDB, MySQL, PostgreSQL, SQLite 데이터베이스에만 사용 가능하며, 데이터베이스의 커맨드라인 클라이언트를 사용합니다.

<a name="migration-structure"></a>
## 마이그레이션 구조 (Migration Structure)

마이그레이션 클래스는 `up`과 `down`이라는 두 메서드를 포함합니다. `up` 메서드는 데이터베이스에 새로운 테이블, 컬럼, 인덱스를 추가하는 데 사용하며, `down` 메서드는 `up`에서 수행한 작업을 되돌리기 위해 작성합니다.

`up`과 `down` 두 메서드 안에서는 Laravel의 스키마 빌더를 사용해 테이블을 표현식처럼 생성하거나 수정할 수 있습니다. `Schema` 빌더에서 사용할 수 있는 모든 메서드는 [테이블 생성](#creating-tables) 문서를 참고하세요. 아래 예시는 `flights` 테이블을 생성하는 마이그레이션입니다:

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
#### 마이그레이션 연결 설정하기

만약 애플리케이션 기본 데이터베이스 연결이 아닌 다른 데이터베이스 연결과 상호작용해야 하는 마이그레이션이라면, 마이그레이션 클래스의 `$connection` 속성을 설정해야 합니다:

```php
/**
 * 이 마이그레이션이 사용할 데이터베이스 연결.
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
## 마이그레이션 실행하기 (Running Migrations)

모든 실행 대기 중인 마이그레이션을 실행하려면, `migrate` Artisan 명령어를 실행하세요:

```shell
php artisan migrate
```

지금까지 어떤 마이그레이션이 실행되었는지 확인하려면, `migrate:status` Artisan 명령어를 사용하세요:

```shell
php artisan migrate:status
```

마이그레이션을 실제로 실행하지 않고 실행될 SQL 문만 보려면, `migrate` 명령어에 `--pretend` 플래그를 붙이면 됩니다:

```shell
php artisan migrate --pretend
```

#### 마이그레이션 실행 격리(Isolating Migration Execution)

애플리케이션을 여러 서버에 배포하고 배포 과정에서 마이그레이션을 실행할 때, 두 서버 이상이 동시에 마이그레이션을 수행하는 일이 없도록 해야 합니다. 이를 방지하기 위해 `migrate` 명령어 실행 시 `--isolated` 옵션을 사용할 수 있습니다.

`--isolated` 옵션이 주어지면, Laravel은 애플리케이션 기본 캐시 드라이버를 이용해 원자적 락(atomic lock)을 먼저 획득한 뒤 마이그레이션을 실행합니다. 락이 걸려 있을 동안 다른 `migrate` 명령어 실행은 실제 마이그레이션을 수행하지 않고 성공 상태 코드로 종료됩니다:

```shell
php artisan migrate --isolated
```

> [!WARNING]  
> 이 기능을 사용하려면 애플리케이션이 `memcached`, `redis`, `dynamodb`, `database`, `file`, 또는 `array` 캐시 드라이버를 기본 캐시 드라이버로 사용해야 합니다. 또한 모든 서버가 같은 중앙 캐시 서버와 통신 중이어야 합니다.

<a name="forcing-migrations-to-run-in-production"></a>
#### 운영 환경에서 강제 마이그레이션 실행하기

일부 마이그레이션은 데이터 손실 위험이 있는 파괴적 작업을 수행합니다. 이러한 명령을 운영 환경에 실수로 실행하지 않도록 실행 전 확인을 요구합니다. 프롬프트 없이 강제로 실행하려면 `--force` 플래그를 사용하세요:

```shell
php artisan migrate --force
```

<a name="rolling-back-migrations"></a>
### 마이그레이션 롤백 (Rolling Back Migrations)

마지막으로 실행한 마이그레이션을 되돌리려면 `rollback` Artisan 명령어를 사용하세요. 이 명령은 마지막 "배치(batch)"에 포함된 모든 마이그레이션을 롤백합니다. 한 배치에는 여러 마이그레이션 파일이 포함될 수 있습니다:

```shell
php artisan migrate:rollback
```

`rollback` 명령어 시 `--step` 옵션을 사용하면 롤백할 마이그레이션 수를 제한할 수 있습니다. 예를 들어, 최근 5개의 마이그레이션만 롤백하려면:

```shell
php artisan migrate:rollback --step=5
```

또한 `--batch` 옵션을 지정하여 특정 배치 번호의 마이그레이션을 롤백할 수 있습니다. 배치 번호는 애플리케이션의 `migrations` 테이블에 저장된 값입니다. 예를 들어, 배치 3의 모든 마이그레이션을 롤백하려면:

```shell
php artisan migrate:rollback --batch=3
```

실제 마이그레이션을 실행하지 않고 롤백 시 실행될 SQL 문을 확인하려면, `migrate:rollback` 명령어에 `--pretend` 플래그를 붙이세요:

```shell
php artisan migrate:rollback --pretend
```

`migrate:reset` 명령어를 실행하면 애플리케이션에 적용된 모든 마이그레이션이 롤백됩니다:

```shell
php artisan migrate:reset
```

<a name="roll-back-migrate-using-a-single-command"></a>
#### 롤백과 마이그레이션을 한 명령어로 실행하기

`migrate:refresh` 명령어는 모든 마이그레이션을 롤백한 뒤 `migrate` 명령어를 실행합니다. 즉, 데이터베이스를 완전히 재생성하는 효과가 있습니다:

```shell
php artisan migrate:refresh

# 데이터베이스를 리프레시하고, 모든 시더를 실행...
php artisan migrate:refresh --seed
```

`refresh` 명령어에 `--step` 옵션을 주면 제한된 개수의 마이그레이션만 롤백하고 다시 마이그레이션할 수도 있습니다. 예를 들어 마지막 5개 마이그레이션만 롤백 후 다시 실행:

```shell
php artisan migrate:refresh --step=5
```

<a name="drop-all-tables-migrate"></a>
#### 모든 테이블 삭제 후 마이그레이션 실행하기

`migrate:fresh` 명령어는 데이터베이스의 모든 테이블을 삭제한 뒤 `migrate` 명령어를 실행합니다:

```shell
php artisan migrate:fresh

php artisan migrate:fresh --seed
```

기본적으로 `migrate:fresh` 명령어는 기본 데이터베이스 연결의 테이블만 삭제합니다. 그러나 `--database` 옵션으로 마이그레이션할 데이터베이스 연결을 지정할 수 있습니다. 연결 이름은 애플리케이션의 `database` [설정 파일](/docs/11.x/configuration)에 정의된 연결명과 일치해야 합니다:

```shell
php artisan migrate:fresh --database=admin
```

> [!WARNING]  
> `migrate:fresh` 명령어는 테이블 접두사(prefix)와 상관없이 모든 데이터베이스 테이블을 삭제합니다. 다른 애플리케이션과 데이터베이스를 공유하는 환경에서는 조심해서 사용해야 합니다.

<a name="tables"></a>
## 테이블 (Tables)

<a name="creating-tables"></a>
### 테이블 생성하기 (Creating Tables)

새로운 데이터베이스 테이블을 생성하려면 `Schema` 파사드의 `create` 메서드를 사용하세요. `create` 메서드는 두 개의 인수를 받는데, 첫 번째는 테이블 이름이며 두 번째는 `Blueprint` 객체를 받는 클로저입니다. 클로저 내에서 새 테이블을 정의할 수 있습니다:

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

테이블 생성 시, [컬럼 메서드들](#creating-columns)을 사용하여 필요한 컬럼을 정의할 수 있습니다.

<a name="determining-table-column-existence"></a>
#### 테이블 / 컬럼 존재 여부 확인하기

`hasTable`, `hasColumn`, `hasIndex` 메서드를 사용해 테이블, 컬럼 또는 인덱스 존재 여부를 확인할 수 있습니다:

```php
if (Schema::hasTable('users')) {
    // "users" 테이블이 존재합니다...
}

if (Schema::hasColumn('users', 'email')) {
    // "users" 테이블에 "email" 컬럼이 존재합니다...
}

if (Schema::hasIndex('users', ['email'], 'unique')) {
    // "users" 테이블에 "email" 컬럼에 유니크 인덱스가 존재합니다...
}
```

<a name="database-connection-table-options"></a>
#### 데이터베이스 연결과 테이블 옵션

애플리케이션 기본 연결이 아닌 다른 데이터베이스 연결에서 스키마 작업을 하려면 `connection` 메서드를 사용할 수 있습니다:

```php
Schema::connection('sqlite')->create('users', function (Blueprint $table) {
    $table->id();
});
```

또한 몇 가지 속성과 메서드를 활용해 테이블 생성의 다른 측면을 지정할 수 있습니다. MariaDB 또는 MySQL을 사용할 때, `engine` 속성으로 테이블 저장 엔진을 설정할 수 있습니다:

```php
Schema::create('users', function (Blueprint $table) {
    $table->engine('InnoDB');

    // ...
});
```

MariaDB/MySQL 환경에서 `charset` 및 `collation` 속성으로 생성할 테이블의 문자 집합과 정렬 순서를 지정할 수도 있습니다:

```php
Schema::create('users', function (Blueprint $table) {
    $table->charset('utf8mb4');
    $table->collation('utf8mb4_unicode_ci');

    // ...
});
```

`temporary` 메서드를 사용하면 "임시" 테이블로 지정할 수 있습니다. 임시 테이블은 현재 데이터베이스 세션에서만 보이고 연결 종료 시 자동으로 삭제됩니다:

```php
Schema::create('calculations', function (Blueprint $table) {
    $table->temporary();

    // ...
});
```

테이블에 "주석"을 추가하고 싶다면, `comment` 메서드를 사용할 수 있습니다. 테이블 주석은 현재 MariaDB, MySQL, PostgreSQL만 지원합니다:

```php
Schema::create('calculations', function (Blueprint $table) {
    $table->comment('Business calculations');

    // ...
});
```

<a name="updating-tables"></a>
### 테이블 수정하기 (Updating Tables)

기존 테이블을 수정할 때는 `Schema` 파사드의 `table` 메서드를 사용합니다. `create` 메서드와 마찬가지로 두 개의 인수를 받는데, 첫 번째는 테이블 이름, 두 번째는 `Blueprint` 인스턴스를 받는 클로저입니다. 이 클로저 내에서 컬럼 추가나 인덱스 작업이 가능합니다:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->integer('votes');
});
```

<a name="renaming-and-dropping-tables"></a>
### 테이블 이름 변경 / 삭제하기 (Renaming / Dropping Tables)

기존 테이블의 이름을 변경하려면 `rename` 메서드가 있습니다:

```php
use Illuminate\Support\Facades\Schema;

Schema::rename($from, $to);
```

테이블을 삭제하려면 `drop` 또는 `dropIfExists` 메서드를 사용할 수 있습니다:

```php
Schema::drop('users');

Schema::dropIfExists('users');
```

<a name="renaming-tables-with-foreign-keys"></a>
#### 외래 키가 걸린 테이블 이름 변경 주의사항

테이블 이름을 변경하기 전에 해당 테이블에 걸린 외래 키 제약조건 이름이 Laravel이 자동 생성하는 이름이 아닌 명시적으로 지정되어 있는지 확인하세요. 그렇지 않으면 외래 키 이름이 변경 전 테이블 이름을 참조하게 됩니다.

<a name="columns"></a>
## 컬럼 (Columns)

<a name="creating-columns"></a>
### 컬럼 생성하기 (Creating Columns)

`Schema` 파사드의 `table` 메서드를 사용하여 기존 테이블에 컬럼을 추가할 수 있습니다. `create` 메서드와 마찬가지로 첫 번째 인자는 테이블 이름, 두 번째 인자는 `Blueprint` 인스턴스를 받는 클로저입니다:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->integer('votes');
});
```

<a name="available-column-types"></a>
### 사용 가능한 컬럼 타입 (Available Column Types)

스키마 빌더의 `Blueprint` 클래스는 데이터베이스 테이블에 추가할 수 있는 다양한 컬럼 타입과 대응하는 메서드를 제공합니다. 아래에 사용 가능한 메서드 종류를 분류별로 나열했습니다.

<a name="booleans-method-list"></a>
#### 불리언 타입 (Boolean Types)

<div class="collection-method-list" markdown="1">

[boolean](#column-method-boolean)

</div>

<a name="strings-and-texts-method-list"></a>
#### 문자열 및 텍스트 타입 (String & Text Types)

<div class="collection-method-list" markdown="1">

[char](#column-method-char)
[longText](#column-method-longText)
[mediumText](#column-method-mediumText)
[string](#column-method-string)
[text](#column-method-text)
[tinyText](#column-method-tinyText)

</div>

<a name="numbers--method-list"></a>
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

<a name="dates-and-times-method-list"></a>
#### 날짜 및 시간 타입 (Date & Time Types)

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
#### 바이너리 타입 (Binary Types)

<div class="collection-method-list" markdown="1">

[binary](#column-method-binary)

</div>

<a name="object-and-jsons-method-list"></a>
#### 객체 및 JSON 타입 (Object & Json Types)

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
#### 공간 데이터 타입 (Spatial Types)

<div class="collection-method-list" markdown="1">

[geography](#column-method-geography)
[geometry](#column-method-geometry)

</div>

#### 관계형 타입 (Relationship Types)

<div class="collection-method-list" markdown="1">

[foreignId](#column-method-foreignId)
[foreignIdFor](#column-method-foreignIdFor)
[foreignUlid](#column-method-foreignUlid)
[foreignUuid](#column-method-foreignUuid)
[morphs](#column-method-morphs)
[nullableMorphs](#column-method-nullableMorphs)

</div>

<a name="spacifics-method-list"></a>
#### 특수 타입 (Specialty Types)

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

`bigIncrements` 메서드는 자동 증가하는 `UNSIGNED BIGINT`(기본 키) 컬럼을 생성합니다:

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

MySQL, MariaDB, SQL Server에서는 `length`와 `fixed` 인자를 넘겨 `VARBINARY` 또는 `BINARY` 타입 컬럼을 생성할 수 있습니다:

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

`dateTimeTz` 메서드는 (시간대가 포함된) `DATETIME` 타입 컬럼을 생성하며, 소수 초 정밀도를 선택적으로 지정할 수 있습니다:

```php
$table->dateTimeTz('created_at', precision: 0);
```

<a name="column-method-dateTime"></a>
#### `dateTime()`

`dateTime` 메서드는 `DATETIME` 타입 컬럼을 생성하며, 소수 초 정밀도도 선택 가능합니다:

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

`decimal` 메서드는 `DECIMAL` 타입 컬럼을 생성하며, 총 자릿수(정밀도)와 소수 자릿수(스케일)을 지정할 수 있습니다:

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

`enum` 메서드는 지정한 유효 값 목록을 포함하는 `ENUM` 타입 컬럼을 생성합니다:

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

`foreignIdFor` 메서드는 모델 클래스에 대해 `{column}_id` 타입 컬럼을 추가합니다. 컬럼 타입은 모델 키 타입에 따라 `UNSIGNED BIGINT`, `CHAR(36)`, `CHAR(26)` 중 하나입니다:

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

`geography` 메서드는 지정한 공간 타입과 SRID(Spatial Reference System Identifier)를 갖는 `GEOGRAPHY` 타입 컬럼을 생성합니다:

```php
$table->geography('coordinates', subtype: 'point', srid: 4326);
```

> [!NOTE]  
> 공간 타입 지원 여부는 데이터베이스 드라이버에 따라 다릅니다. PostgreSQL을 사용하는 경우, `geography` 메서드를 사용하려면 [PostGIS](https://postgis.net) 확장 기능이 설치되어 있어야 합니다.

<a name="column-method-geometry"></a>
#### `geometry()`

`geometry` 메서드는 지정한 공간 타입과 SRID를 갖는 `GEOMETRY` 타입 컬럼을 생성합니다:

```php
$table->geometry('positions', subtype: 'point', srid: 0);
```

> [!NOTE]  
> 공간 타입 지원 여부는 데이터베이스 드라이버에 따라 다릅니다. PostgreSQL의 경우, [PostGIS](https://postgis.net) 확장이 설치되어 있어야 합니다.

<a name="column-method-id"></a>
#### `id()`

`id` 메서드는 `bigIncrements` 메서드의 별칭입니다. 기본적으로 `id`라는 칼럼명을 사용하지만, 다른 이름을 지정할 수도 있습니다:

```php
$table->id();
```

<a name="column-method-increments"></a>
#### `increments()`

`increments` 메서드는 자동 증가하는 `UNSIGNED INTEGER` 타입 컬럼(기본 키)를 생성합니다:

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

`ipAddress` 메서드는 `VARCHAR` 타입 컬럼을 생성합니다:

```php
$table->ipAddress('visitor');
```

PostgreSQL을 사용할 경우, `INET` 컬럼으로 생성됩니다.

<a name="column-method-json"></a>
#### `json()`

`json` 메서드는 `JSON` 타입 컬럼을 생성합니다:

```php
$table->json('options');
```

SQLite를 사용하는 경우에는 `TEXT` 타입 컬럼으로 생성됩니다.

<a name="column-method-jsonb"></a>
#### `jsonb()`

`jsonb` 메서드는 `JSONB` 타입 컬럼을 생성합니다:

```php
$table->jsonb('options');
```

SQLite에서는 `TEXT` 타입 컬럼으로 생성됩니다.

<a name="column-method-longText"></a>
#### `longText()`

`longText` 메서드는 `LONGTEXT` 타입 컬럼을 생성합니다:

```php
$table->longText('description');
```

MySQL 또는 MariaDB를 사용할 때는 `binary` 문자 집합을 지정해 `LONGBLOB` 타입 컬럼으로도 만들 수 있습니다:

```php
$table->longText('data')->charset('binary'); // LONGBLOB
```

<a name="column-method-macAddress"></a>
#### `macAddress()`

`macAddress` 메서드는 MAC 주소를 저장하기 위한 컬럼을 생성합니다. PostgreSQL과 같은 일부 데이터베이스는 전용 컬럼 타입을 갖지만, 그 외는 문자열 타입으로 생성됩니다:

```php
$table->macAddress('device');
```

<a name="column-method-mediumIncrements"></a>
#### `mediumIncrements()`

`mediumIncrements` 메서드는 자동 증가하는 `UNSIGNED MEDIUMINT` 타입 컬럼(기본 키)을 생성합니다:

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

MySQL 또는 MariaDB에서 `binary` 문자 집합을 지정하면 `MEDIUMBLOB` 타입으로 생성됩니다:

```php
$table->mediumText('data')->charset('binary'); // MEDIUMBLOB
```

<a name="column-method-morphs"></a>
#### `morphs()`

`morphs` 메서드는 `{column}_id` 타입 칼럼과 `{column}_type` `VARCHAR` 타입 칼럼을 편리하게 생성합니다. `{column}_id`의 타입은 모델 키 형태에 따라 `UNSIGNED BIGINT`, `CHAR(36)`, `CHAR(26)` 중 하나로 결정됩니다.

이 메서드는 polymorphic [Eloquent 관계](/docs/11.x/eloquent-relationships)를 위한 칼럼 정의에 적합합니다. 예를 들면 `taggable_id`와 `taggable_type` 컬럼을 생성합니다:

```php
$table->morphs('taggable');
```

<a name="column-method-nullableMorphs"></a>
#### `nullableMorphs()`

`morphs()`와 유사하지만 생성되는 두 컬럼 모두 `nullable`(널 허용) 상태로 만듭니다:

```php
$table->nullableMorphs('taggable');
```

<a name="column-method-nullableUlidMorphs"></a>
#### `nullableUlidMorphs()`

`ulidMorphs()`와 유사하지만 생성되는 컬럼들이 `nullable`로 설정됩니다:

```php
$table->nullableUlidMorphs('taggable');
```

<a name="column-method-nullableUuidMorphs"></a>
#### `nullableUuidMorphs()`

`uuidMorphs()`와 유사하지만 생성되는 컬럼들이 `nullable`로 설정됩니다:

```php
$table->nullableUuidMorphs('taggable');
```

<a name="column-method-rememberToken"></a>
#### `rememberToken()`

`rememberToken` 메서드는 널이 가능한 `VARCHAR(100)` 타입 컬럼을 생성하며, 현재 "remember me" [인증 토큰](/docs/11.x/authentication#remembering-users)을 저장하는 데 사용됩니다:

```php
$table->rememberToken();
```

<a name="column-method-set"></a>
#### `set()`

`set` 메서드는 지정한 유효값 리스트를 갖는 `SET` 타입 컬럼을 생성합니다:

```php
$table->set('flavors', ['strawberry', 'vanilla']);
```

<a name="column-method-smallIncrements"></a>
#### `smallIncrements()`

`smallIncrements` 메서드는 자동 증가하는 `UNSIGNED SMALLINT` 타입 컬럼(기본 키)을 생성합니다:

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

`softDeletesTz` 메서드는 널이 가능한 `deleted_at` `TIMESTAMP` (시간대 포함) 타입 컬럼을 소수 초 정밀도 옵션과 함께 추가합니다. 이 칼럼은 Eloquent의 "소프트 삭제" 기능에 필요한 삭제 타임스탬프를 저장합니다:

```php
$table->softDeletesTz('deleted_at', precision: 0);
```

<a name="column-method-softDeletes"></a>
#### `softDeletes()`

`softDeletes` 메서드는 `softDeletesTz`와 유사하지만 시간대가 없는 `TIMESTAMP` 타입 컬럼을 생성합니다:

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

MySQL 또는 MariaDB에서 `binary` 문자 집합을 지정하면 `BLOB` 타입으로 생성할 수 있습니다:

```php
$table->text('data')->charset('binary'); // BLOB
```

<a name="column-method-timeTz"></a>
#### `timeTz()`

`timeTz` 메서드는 (시간대 포함된) `TIME` 타입 컬럼을 소수 초 정밀도와 함께 생성합니다:

```php
$table->timeTz('sunrise', precision: 0);
```

<a name="column-method-time"></a>
#### `time()`

`time` 메서드는 `TIME` 타입 컬럼을 소수 초 정밀도와 함께 생성합니다:

```php
$table->time('sunrise', precision: 0);
```

<a name="column-method-timestampTz"></a>
#### `timestampTz()`

`timestampTz` 메서드는 (시간대 포함된) `TIMESTAMP` 타입 컬럼을 생성하며, 소수 초 정밀도도 지정할 수 있습니다:

```php
$table->timestampTz('added_at', precision: 0);
```

<a name="column-method-timestamp"></a>
#### `timestamp()`

`timestamp` 메서드는 `TIMESTAMP` 타입 컬럼을 소수 초 정밀도와 함께 생성합니다:

```php
$table->timestamp('added_at', precision: 0);
```

<a name="column-method-timestampsTz"></a>
#### `timestampsTz()`

클래스는 `created_at`, `updated_at` 두 컬럼을 (시간대 포함) `TIMESTAMP` 타입으로 소수 초 정밀도 지정과 함께 생성합니다:

```php
$table->timestampsTz(precision: 0);
```

<a name="column-method-timestamps"></a>
#### `timestamps()`

`timestamps` 메서드는 `created_at`, `updated_at` 두 컬럼을 `TIMESTAMP` 타입으로 소수 초 정밀도 지정과 함께 생성합니다:

```php
$table->timestamps(precision: 0);
```

<a name="column-method-tinyIncrements"></a>
#### `tinyIncrements()`

`tinyIncrements` 메서드는 자동 증가하는 `UNSIGNED TINYINT` 타입 컬럼(기본 키)을 생성합니다:

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

MySQL 또는 MariaDB에서는 `binary` 문자 집합을 지정해 `TINYBLOB` 타입 컬럼으로 만들 수 있습니다:

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

`ulidMorphs` 메서드는 `{column}_id` `CHAR(26)` 타입 컬럼과 `{column}_type` `VARCHAR` 타입 컬럼을 편리하게 생성합니다.

이는 ULID 식별자를 사용하는 polymorphic [Eloquent 관계](/docs/11.x/eloquent-relationships)용 칼럼 정의에 적합합니다. 예를 들어 아래는 `taggable_id`와 `taggable_type` 컬럼을 생성합니다:

```php
$table->ulidMorphs('taggable');
```

<a name="column-method-uuidMorphs"></a>
#### `uuidMorphs()`

`uuidMorphs` 메서드는 `{column}_id` `CHAR(36)` 타입 컬럼과 `{column}_type` `VARCHAR` 타입 컬럼을 편리하게 생성합니다.

이는 UUID 식별자를 사용하는 polymorphic [Eloquent 관계](/docs/11.x/eloquent-relationships)용 칼럼 정의에 적합합니다. 예를 들어 아래는 `taggable_id`와 `taggable_type` 컬럼을 생성합니다:

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

`vector` 메서드는 벡터 타입 컬럼을 생성합니다:

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

컬럼 타입뿐 아니라, 컬럼에 추가할 수 있는 여러 "수정자"도 존재합니다. 예를 들어, 컬럼을 "nullable"하게 하려면 `nullable` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->string('email')->nullable();
});
```

아래 표에는 자주 사용하는 컬럼 수정자를 정리했습니다. 이 목록에는 [인덱스 수정자](#creating-indexes)는 포함되어 있지 않습니다.

<div class="overflow-auto">

| 수정자                             | 설명                                                                                   |
| ----------------------------------- | --------------------------------------------------------------------------------------- |
| `->after('column')`                 | 특정 컬럼 뒤에 컬럼을 삽입합니다 (MariaDB / MySQL).                                      |
| `->autoIncrement()`                 | `INTEGER` 컬럼을 자동 증가하는 기본 키로 설정합니다.                                    |
| `->charset('utf8mb4')`              | 컬럼에 문자 집합을 지정합니다 (MariaDB / MySQL).                                         |
| `->collation('utf8mb4_unicode_ci')` | 컬럼에 정렬 순서를 지정합니다.                                                           |
| `->comment('my comment')`           | 컬럼에 주석을 추가합니다 (MariaDB / MySQL / PostgreSQL).                                 |
| `->default($value)`                 | 컬럼의 기본값을 지정합니다.                                                             |
| `->first()`                         | 컬럼을 테이블의 첫 번째 칼럼으로 위치시킵니다 (MariaDB / MySQL).                         |
| `->from($integer)`                  | 자동 증가 필드의 시작 값을 설정합니다 (MariaDB / MySQL / PostgreSQL).                   |
| `->invisible()`                     | `SELECT *` 쿼리에서 해당 컬럼을 숨깁니다 (MariaDB / MySQL).                            |
| `->nullable($value = true)`         | 컬럼 값에 NULL을 허용합니다.                                                            |
| `->storedAs($expression)`           | 저장된 생성 컬럼(stored generated column)을 만듭니다 (MariaDB / MySQL / PostgreSQL / SQLite). |
| `->unsigned()`                      | `INTEGER` 컬럼을 UNSIGNED로 설정합니다 (MariaDB / MySQL).                              |
| `->useCurrent()`                    | `TIMESTAMP` 컬럼의 기본값을 `CURRENT_TIMESTAMP`로 지정합니다.                          |
| `->useCurrentOnUpdate()`            | 레코드 업데이트 시 `TIMESTAMP` 컬럼에 `CURRENT_TIMESTAMP`가 자동 설정되도록 합니다 (MariaDB / MySQL). |
| `->virtualAs($expression)`          | 가상 생성 컬럼(virtual generated column)을 만듭니다 (MariaDB / MySQL / SQLite).          |
| `->generatedAs($expression)`        | 식별자 컬럼(identity column)을 생성하고 시퀀스 옵션을 지정합니다 (PostgreSQL).         |
| `->always()`                        | 시퀀스 값이 입력 값보다 우선 적용되도록 지정합니다 (identity 컬럼, PostgreSQL).          |

</div>

<a name="default-expressions"></a>
#### 기본값 표현식 (Default Expressions)

`default` 수정자는 값 또는 `Illuminate\Database\Query\Expression` 인스턴스를 받을 수 있습니다. `Expression` 인스턴스를 쓰면 값이 따옴표로 감싸지지 않고 데이터베이스 고유 함수를 사용할 수 있습니다. JSON 컬럼에 기본값을 할당할 때 특히 유용합니다:

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
> 기본 표현식 지원 여부는 데이터베이스 드라이버, 버전, 컬럼 타입에 따라 다릅니다. 데이터베이스 문서를 참고하세요.

<a name="column-order"></a>
#### 컬럼 순서 지정하기

MariaDB 또는 MySQL에서는 `after` 메서드를 사용해 기존 컬럼 뒤에 새 컬럼을 추가할 수 있습니다:

```php
$table->after('password', function (Blueprint $table) {
    $table->string('address_line1');
    $table->string('address_line2');
    $table->string('city');
});
```

<a name="modifying-columns"></a>
### 컬럼 수정하기 (Modifying Columns)

`change` 메서드로 기존 컬럼의 타입과 속성을 수정할 수 있습니다. 예를 들어, `name` 컬럼의 길이를 25에서 50으로 늘리려면 다음과 같이 작성합니다:

```php
Schema::table('users', function (Blueprint $table) {
    $table->string('name', 50)->change();
});
```

기존 컬럼을 수정할 때는 유지할 수정자(예: `unsigned`, `default`, `comment`)를 모두 명시적으로 호출해야 합니다. 누락된 수정자는 제거됩니다.

```php
Schema::table('users', function (Blueprint $table) {
    $table->integer('votes')->unsigned()->default(1)->comment('my comment')->change();
});
```

`change` 메서드는 컬럼의 인덱스를 변경하지 않습니다. 인덱스를 추가하거나 삭제하려면 인덱스 관련 수정자를 명시적으로 호출하세요:

```php
// 인덱스 추가
$table->bigIncrements('id')->primary()->change();

// 인덱스 삭제
$table->char('postal_code', 10)->unique(false)->change();
```

<a name="renaming-columns"></a>
### 컬럼 이름 변경하기 (Renaming Columns)

컬럼 이름을 변경하려면 스키마 빌더가 제공하는 `renameColumn` 메서드를 사용하세요:

```php
Schema::table('users', function (Blueprint $table) {
    $table->renameColumn('from', 'to');
});
```

<a name="dropping-columns"></a>
### 컬럼 삭제하기 (Dropping Columns)

컬럼을 삭제하려면 `dropColumn` 메서드를 사용합니다:

```php
Schema::table('users', function (Blueprint $table) {
    $table->dropColumn('votes');
});
```

여러 컬럼을 삭제하려면 컬럼명 배열을 넘기면 됩니다:

```php
Schema::table('users', function (Blueprint $table) {
    $table->dropColumn(['votes', 'avatar', 'location']);
});
```

<a name="available-command-aliases"></a>
#### 사용 가능한 컬럼 드롭 명령어 별칭

Laravel은 흔히 삭제하는 컬럼 유형을 위한 편리한 별칭 메서드들을 제공합니다:

<div class="overflow-auto">

| 명령어                              | 설명                                    |
| ----------------------------------- | --------------------------------------- |
| `$table->dropMorphs('morphable');`  | `morphable_id` 와 `morphable_type` 컬럼 삭제 |
| `$table->dropRememberToken();`      | `remember_token` 컬럼 삭제              |
| `$table->dropSoftDeletes();`        | `deleted_at` 컬럼 삭제                  |
| `$table->dropSoftDeletesTz();`      | `dropSoftDeletes()` 메서드 별칭        |
| `$table->dropTimestamps();`         | `created_at` 와 `updated_at` 컬럼 삭제  |
| `$table->dropTimestampsTz();`       | `dropTimestamps()` 메서드 별칭         |

</div>

<a name="indexes"></a>
## 인덱스 (Indexes)

<a name="creating-indexes"></a>
### 인덱스 생성하기 (Creating Indexes)

Laravel 스키마 빌더는 여러 종류의 인덱스를 지원합니다. 예를 들어, `email` 컬럼 생성과 동시에 값의 유일성을 보장하는 인덱스 지정은 다음과 같이 `unique` 메서드를 체인으로 호출하면 됩니다:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->string('email')->unique();
});
```

인덱스는 컬럼 생성 후에도 생성할 수 있습니다. 인덱스 메서드에 컬럼명 또는 컬럼명 배열을 인수로 전달해 지정합니다:

```php
$table->unique('email');

$table->index(['account_id', 'created_at']);
```

인덱스 이름은 Laravel이 테이블명, 컬럼명, 인덱스 타입을 기반으로 자동 생성합니다. 필요하면 두 번째 인수로 이름을 직접 지정할 수 있습니다:

```php
$table->unique('email', 'unique_email');
```

<a name="available-index-types"></a>
#### 사용 가능한 인덱스 타입

아래 표는 Laravel 스키마 빌더가 제공하는 인덱스 메서드 목록입니다. 두 번째 인수로 인덱스 이름을 지정할 수 있습니다. 생략 시 테이블명, 컬럼명, 인덱스 타입을 기반으로 이름이 자동 생성됩니다.

<div class="overflow-auto">

| 명령어                                      | 설명                                              |
| -------------------------------------------- | ------------------------------------------------- |
| `$table->primary('id');`                     | 기본 키를 추가합니다.                             |
| `$table->primary(['id', 'parent_id']);`      | 복합 기본 키를 추가합니다.                        |
| `$table->unique('email');`                   | 유니크 인덱스를 추가합니다.                      |
| `$table->index('state');`                    | 일반 인덱스를 추가합니다.                         |
| `$table->fullText('body');`                  | 전체 텍스트 인덱스 추가(MariaDB / MySQL / PostgreSQL). |
| `$table->fullText('body')->language('english');` | 특정 언어 기반 전체 텍스트 인덱스(PostgreSQL).  |
| `$table->spatialIndex('location');`          | 공간 인덱스 추가(SQLite 제외).                    |

</div>

<a name="renaming-indexes"></a>
### 인덱스 이름 변경하기 (Renaming Indexes)

인덱스 이름을 변경하려면 `renameIndex` 메서드를 사용하며, 첫 번째 인수는 현재 이름, 두 번째 인수는 변경할 이름입니다:

```php
$table->renameIndex('old_name', 'new_name');
```

<a name="dropping-indexes"></a>
### 인덱스 삭제하기 (Dropping Indexes)

인덱스를 삭제할 때는 인덱스 이름을 지정해야 합니다. Laravel은 기본적으로 테이블명, 컬럼, 인덱스 타입을 기준으로 인덱스 이름을 자동 생성합니다. 예시는 다음과 같습니다:

<div class="overflow-auto">

| 명령어                                                 | 설명                                    |
| ------------------------------------------------------- | --------------------------------------- |
| `$table->dropPrimary('users_id_primary');`              | "users" 테이블의 기본 키 삭제           |
| `$table->dropUnique('users_email_unique');`             | "users" 테이블의 유니크 인덱스 삭제    |
| `$table->dropIndex('geo_state_index');`                 | "geo" 테이블의 일반 인덱스 삭제        |
| `$table->dropFullText('posts_body_fulltext');`          | "posts" 테이블의 전체 텍스트 인덱스 삭제 |
| `$table->dropSpatialIndex('geo_location_spatialindex');` | "geo" 테이블의 공간 인덱스 삭제(SQLite 제외) |

</div>

만약 인덱스 삭제 메서드에 컬럼명 배열을 넘기면, Laravel은 자동으로 인덱스 이름을 생성해 삭제합니다:

```php
Schema::table('geo', function (Blueprint $table) {
    $table->dropIndex(['state']); // 'geo_state_index' 인덱스 삭제
});
```

<a name="foreign-key-constraints"></a>
### 외래 키 제약조건 (Foreign Key Constraints)

Laravel은 데이터베이스 수준에서 참조 무결성을 확보하는 외래 키 제약조건도 지원합니다. 예를 들어 `posts` 테이블에 `user_id` 컬럼을 추가하고 `users` 테이블의 `id` 컬럼을 참조하는 외래 키를 정의하려면 다음과 같이 작성합니다:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('posts', function (Blueprint $table) {
    $table->unsignedBigInteger('user_id');

    $table->foreign('user_id')->references('id')->on('users');
});
```

이 문법이 다소 장황하므로, Laravel은 규칙을 기반으로 더 간결한 메서드를 제공합니다. `foreignId` 메서드를 사용하여 컬럼을 생성한 뒤 `constrained` 메서드를 호출하면 위 구문을 다음과 같이 쓸 수 있습니다:

```php
Schema::table('posts', function (Blueprint $table) {
    $table->foreignId('user_id')->constrained();
});
```

`foreignId`는 `UNSIGNED BIGINT` 타입 컬럼을 자동 생성하고, `constrained`는 참조될 테이블과 컬럼명을 규칙에 따라 추론합니다. 만약 테이블명이 규칙과 다르다면 직접 인자로 지정할 수 있으며, 인덱스 이름도 지정 가능합나다:

```php
Schema::table('posts', function (Blueprint $table) {
    $table->foreignId('user_id')->constrained(
        table: 'users', indexName: 'posts_user_id'
    );
});
```

"on delete", "on update" 시의 동작 또한 지정할 수 있습니다:

```php
$table->foreignId('user_id')
    ->constrained()
    ->onUpdate('cascade')
    ->onDelete('cascade');
```

아래 표는 이 행동들을 위한 대체 표현식입니다:

<div class="overflow-auto">

| 메서드                     | 설명                                     |
| -------------------------- | ---------------------------------------- |
| `$table->cascadeOnUpdate();`  | 업데이트 시 연쇄 갱신                     |
| `$table->restrictOnUpdate();` | 업데이트 제한                           |
| `$table->nullOnUpdate();`     | 업데이트 시 외래 키 NULL 설정            |
| `$table->noActionOnUpdate();` | 업데이트 시 동작 없음                    |
| `$table->cascadeOnDelete();`  | 삭제 시 연쇄 삭제                       |
| `$table->restrictOnDelete();` | 삭제 제한                              |
| `$table->nullOnDelete();`     | 삭제 시 외래 키 NULL 설정               |
| `$table->noActionOnDelete();` | 자식 레코드가 있으면 삭제 방지          |

</div>

외래 키 제약조건을 추가할 때 다른 [컬럼 수정자들](#column-modifiers)은 `constrained` 호출보다 앞서 호출해야 합니다:

```php
$table->foreignId('user_id')
    ->nullable()
    ->constrained();
```

<a name="dropping-foreign-keys"></a>
#### 외래 키 제약조건 삭제하기

외래 키 제약조건을 삭제하려면 `dropForeign` 메서드를 사용하며, 삭제할 제약조건 이름을 인수로 전달합니다. 외래 키 이름은 인덱스와 마찬가지로 테이블, 컬럼명을 기준으로 생성되며 뒤에 `_foreign` 접미사가 붙습니다:

```php
$table->dropForeign('posts_user_id_foreign');
```

컬럼명을 배열로 넘겨도 같은 효과를 얻을 수 있습니다:

```php
$table->dropForeign(['user_id']);
```

<a name="toggling-foreign-key-constraints"></a>
#### 외래 키 제약조건 활성화/비활성화

마이그레이션 중에 외래 키 제약조건을 활성화 또는 비활성화하려면 다음 메서드를 사용하세요:

```php
Schema::enableForeignKeyConstraints();

Schema::disableForeignKeyConstraints();

Schema::withoutForeignKeyConstraints(function () {
    // 이 클로저 내에서는 제약조건 비활성화됨...
});
```

> [!WARNING]  
> SQLite는 기본적으로 외래 키 제약조건이 비활성화되어 있습니다. SQLite를 사용할 경우, 마이그레이션 내에서 외래 키를 생성하기 전에 [외래 키 지원을 활성화](/docs/11.x/database#configuration)해야 합니다.

<a name="events"></a>
## 이벤트 (Events)

편의를 위해 각 마이그레이션 작업은 [이벤트](/docs/11.x/events)를 발생시킵니다. 아래 이벤트들은 모두 기본 클래스 `Illuminate\Database\Events\MigrationEvent`를 상속합니다:

<div class="overflow-auto">

| 클래스명                                             | 설명                                        |
| ----------------------------------------------------- | --------------------------------------------- |
| `Illuminate\Database\Events\MigrationsStarted`       | 마이그레이션 배치 실행 직전                  |
| `Illuminate\Database\Events\MigrationsEnded`         | 마이그레이션 배치 실행 완료                   |
| `Illuminate\Database\Events\MigrationStarted`        | 개별 마이그레이션 실행 직전                    |
| `Illuminate\Database\Events\MigrationEnded`          | 개별 마이그레이션 실행 완료                     |
| `Illuminate\Database\Events\NoPendingMigrations`     | 실행 대기 중인 마이그레이션 없음                |
| `Illuminate\Database\Events\SchemaDumped`            | 데이터베이스 스키마 덤프 완료                    |
| `Illuminate\Database\Events\SchemaLoaded`            | 기존 데이터베이스 스키마 덤프 불러오기 완료       |

</div>