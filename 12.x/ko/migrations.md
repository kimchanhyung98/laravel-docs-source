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
    - [테이블 이름 변경 및 삭제](#renaming-and-dropping-tables)
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

마이그레이션(Migration)은 데이터베이스를 위한 버전 관리 시스템과 같습니다. 이를 통해 팀원들이 애플리케이션의 데이터베이스 스키마 정의를 명확하게 지정하고 공유할 수 있습니다. 만약 소스 컨트롤에서 변경 사항을 받아온 후, 동료에게 "로컬 데이터베이스에 칼럼을 직접 추가해 달라"고 요청한 경험이 있다면, 이것이 바로 데이터베이스 마이그레이션이 해결하는 문제입니다.

Laravel의 `Schema` [파사드](/docs/12.x/facades)는 Laravel이 지원하는 모든 데이터베이스 시스템에서 데이터베이스 비종속적으로 테이블 생성 및 조작을 할 수 있게 해줍니다. 일반적으로 마이그레이션에서는 이 파사드를 사용해 데이터베이스의 테이블과 컬럼을 생성하고 수정합니다.

<a name="generating-migrations"></a>
## 마이그레이션 생성 (Generating Migrations)

`make:migration` [Artisan 명령어](/docs/12.x/artisan)를 사용하여 데이터베이스 마이그레이션 파일을 생성할 수 있습니다. 새로 생성되는 마이그레이션 파일은 `database/migrations` 디렉토리에 저장됩니다. 각 마이그레이션 파일명에는 타임스탬프가 포함되어 있어, Laravel이 마이그레이션의 실행 순서를 결정할 수 있습니다.

```shell
php artisan make:migration create_flights_table
```

Laravel은 마이그레이션의 이름을 참고하여, 해당 마이그레이션이 어떤 테이블을 대상으로 하고, 새로운 테이블을 생성하는지 여부를 추정하려 시도합니다. 만약 마이그레이션의 이름에서 테이블명을 파악할 수 있다면, Laravel은 생성된 마이그레이션 파일에 해당 테이블명을 미리 작성해줍니다. 반대로, 이름에서 추정이 되지 않는다면 마이그레이션 파일에서 테이블을 직접 명시하면 됩니다.

생성된 마이그레이션 파일의 경로를 직접 지정하고 싶다면, `make:migration` 명령어를 실행할 때 `--path` 옵션을 사용할 수 있습니다. 이 경로는 애플리케이션의 기준 경로를 기준으로 해야 합니다.

> [!NOTE]
> 마이그레이션 스텁 파일은 [스텁 퍼블리싱](/docs/12.x/artisan#stub-customization)을 통해 사용자 정의할 수 있습니다.

<a name="squashing-migrations"></a>
### 마이그레이션 스쿼싱 (Squashing Migrations)

애플리케이션을 개발하다 보면 시간이 지나면서 점점 더 많은 마이그레이션 파일이 쌓이게 됩니다. 이렇게 되면 `database/migrations` 디렉토리가 수백 개의 마이그레이션 파일로 가득 차는 일이 발생할 수 있습니다. 필요하다면 여러 개의 마이그레이션을 하나의 SQL 파일로 "스쿼시(합치기)"할 수 있습니다. 이를 위해서는 `schema:dump` 명령어를 실행하면 됩니다.

```shell
php artisan schema:dump

# 현재 데이터베이스 스키마를 덤프하고, 기존 마이그레이션을 모두 정리(prune)합니다...
php artisan schema:dump --prune
```

이 명령어를 실행하면 Laravel은 `database/schema` 디렉토리에 "스키마" 파일을 생성합니다. 해당 파일의 이름은 데이터베이스 연결에 따라 정해집니다. 마이그레이션 실행 시 아직 실행되지 않은 마이그레이션이 없다면, Laravel은 먼저 사용하는 데이터베이스 연결의 스키마 파일 내 SQL 명령문을 실행합니다. 그 다음, 스키마 덤프에 포함되지 않았던 남은 마이그레이션만 별도로 실행하게 됩니다.

애플리케이션의 테스트 환경에서 개발 시와는 다른 데이터베이스 연결을 사용하는 경우, 테스트에서도 데이터베이스를 정상적으로 구축할 수 있도록 해당 데이터베이스 연결로도 스키마 파일을 덤프해야 합니다. 일반적으로, 로컬 개발 시 사용하는 데이터베이스 연결로 스키마를 덤프한 후 아래와 같이 추가로 명령을 실행할 수 있습니다.

```shell
php artisan schema:dump
php artisan schema:dump --database=testing --prune
```

생성된 데이터베이스 스키마 파일은 소스 컨트롤에 반드시 커밋하여, 새로 합류하는 팀원도 애플리케이션의 초기 데이터베이스 구조를 빠르게 만들 수 있도록 하세요.

> [!WARNING]
> 마이그레이션 스쿼싱은 MariaDB, MySQL, PostgreSQL, SQLite 데이터베이스에서만 사용할 수 있으며, 각 데이터베이스의 명령줄 클라이언트를 사용합니다.

<a name="migration-structure"></a>
## 마이그레이션 구조 (Migration Structure)

마이그레이션 클래스에는 `up`과 `down`이라는 두 개의 메서드가 존재합니다. `up` 메서드는 데이터베이스에 새로운 테이블, 컬럼, 인덱스를 추가할 때 사용하고, `down` 메서드는 `up`에서 수행한 작업을 되돌리는 역할을 합니다.

두 메서드 모두 Laravel의 스키마 빌더를 이용하여 테이블을 명확하게 생성하고 수정할 수 있습니다. 사용할 수 있는 모든 스키마 빌더 메서드에 대해 더 알고 싶다면 [해당 문서](#creating-tables)를 참고하세요. 아래의 예시 마이그레이션은 `flights` 테이블을 생성합니다.

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

만약 마이그레이션이 애플리케이션의 기본 데이터베이스 연결이 아닌 다른 연결을 사용해야 한다면, 마이그레이션의 `$connection` 속성을 지정해야 합니다.

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

특정 마이그레이션이 아직 활성화되지 않은 기능을 위해서만 필요하고, 실제로는 실행하고 싶지 않은 경우가 있습니다. 이런 경우, 마이그레이션 클래스에 `shouldRun` 메서드를 정의할 수 있습니다. 이 메서드가 `false`를 반환하면 해당 마이그레이션은 건너뜁니다.

```php
use App\Models\Flights;
use Laravel\Pennant\Feature;

/**
 * Determine if this migration should run.
 */
public function shouldRun(): bool
{
    return Feature::active(Flights::class);
}
```

<a name="running-migrations"></a>
## 마이그레이션 실행 (Running Migrations)

아직 실행되지 않은 모든 마이그레이션을 실행하려면 `migrate` Artisan 명령어를 사용합니다.

```shell
php artisan migrate
```

지금까지 어떤 마이그레이션이 실행되었는지 확인하려면 `migrate:status` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan migrate:status
```

마이그레이션이 실제로 실행되기 전에 어떤 SQL 구문이 실행될지 미리 보고 싶다면, `--pretend` 플래그를 사용합니다.

```shell
php artisan migrate --pretend
```

#### 마이그레이션 실행 격리하기

여러 서버에 애플리케이션을 배포하고 배포 과정에서 마이그레이션 명령어를 실행하는 경우, 두 대의 서버가 동시에 데이터베이스를 마이그레이션하는 상황을 피하고 싶을 수 있습니다. 이럴 때는 `migrate` 명령어를 실행할 때 `--isolated` 옵션을 사용할 수 있습니다.

이 옵션을 사용하면, Laravel은 마이그레이션을 실행하기 전에 애플리케이션의 캐시 드라이버를 이용하여 원자적인(atomic) 락을 잡습니다. 락이 잡혀 있는 동안 `migrate` 명령어를 실행하려 한 모든 시도는 실제로 마이그레이션이 실행되지 않으며, 명령어는 성공적으로 종료됩니다.

```shell
php artisan migrate --isolated
```

> [!WARNING]
> 이 기능을 사용하기 위해서는, 애플리케이션의 기본 캐시 드라이버가 `memcached`, `redis`, `dynamodb`, `database`, `file`, 또는 `array` 중 하나여야 하며, 모든 서버가 동일한 중앙 캐시 서버와 통신할 수 있어야 합니다.

<a name="forcing-migrations-to-run-in-production"></a>
#### 프로덕션 환경에서 강제로 마이그레이션 실행

일부 마이그레이션 작업은 데이터 손실을 야기할 수 있습니다. 이러한 명령어를 실수로 프로덕션 데이터베이스에서 실행하는 것을 방지하기 위해, 명령어 실행 전에 확인 요청이 출력됩니다. 이를 건너뛰고 강제로 명령어를 실행하려면 `--force` 플래그를 사용하세요.

```shell
php artisan migrate --force
```

<a name="rolling-back-migrations"></a>
### 마이그레이션 롤백 (Rolling Back Migrations)

가장 최근에 실행된 마이그레이션을 롤백하려면 `rollback` Artisan 명령어를 사용할 수 있습니다. 이 명령어는 마지막 "배치(batch)"의 마이그레이션을 한꺼번에 롤백하는데, 하나의 배치에는 여러 마이그레이션 파일이 포함될 수 있습니다.

```shell
php artisan migrate:rollback
```

`step` 옵션을 지정하면 롤백하는 마이그레이션의 개수를 제한할 수 있습니다. 예를 들어, 다음 명령어는 마지막 5개의 마이그레이션만 롤백합니다.

```shell
php artisan migrate:rollback --step=5
```

특정 "배치"의 마이그레이션만 롤백하려면, `rollback` 명령어에 `batch` 옵션을 사용할 수 있습니다. `batch` 값은 애플리케이션의 `migrations` 테이블 내 배치 값과 일치해야 합니다. 예시로, 아래 명령어는 3번 배치의 모든 마이그레이션을 롤백합니다.

```shell
php artisan migrate:rollback --batch=3
```

마이그레이션이 실제로 실행되지 않고, 어떤 SQL 문이 실행될지 미리 보고 싶다면, `migrate:rollback` 명령어에 `--pretend` 플래그를 사용할 수 있습니다.

```shell
php artisan migrate:rollback --pretend
```

`migrate:reset` 명령어는 애플리케이션의 모든 마이그레이션을 롤백합니다.

```shell
php artisan migrate:reset
```

<a name="roll-back-migrate-using-a-single-command"></a>
#### 한 번에 롤백 및 마이그레이트하기

`migrate:refresh` 명령어는 모든 마이그레이션을 롤백한 다음 다시 실행합니다. 즉, 전체 데이터베이스를 재구성하는 효과가 있습니다.

```shell
php artisan migrate:refresh

# 데이터베이스를 새로 고치고 모든 데이터베이스 시드를 실행합니다...
php artisan migrate:refresh --seed
```

`refresh` 명령어에 `step` 옵션을 주면, 마지막에서부터 지정한 개수의 마이그레이션만 롤백 및 재실행하게 할 수 있습니다. 예를 들어 아래 명령어는 최근 5개의 마이그레이션만 롤백하고 다시 적용합니다.

```shell
php artisan migrate:refresh --step=5
```

<a name="drop-all-tables-migrate"></a>
#### 모든 테이블 삭제 후 마이그레이트

`migrate:fresh` 명령어는 데이터베이스의 모든 테이블을 삭제한 후 `migrate` 명령어를 실행합니다.

```shell
php artisan migrate:fresh

php artisan migrate:fresh --seed
```

기본적으로 `migrate:fresh` 명령어는 기본 데이터베이스 연결의 테이블만 삭제합니다. 그러나 `--database` 옵션을 통해 어느 데이터베이스 연결을 사용할지 지정할 수 있습니다. 데이터베이스 연결 이름은 애플리케이션의 `database` [설정 파일](/docs/12.x/configuration)에 정의된 연결과 일치해야 합니다.

```shell
php artisan migrate:fresh --database=admin
```

> [!WARNING]
> `migrate:fresh` 명령어는 프리픽스와 상관없이 데이터베이스의 모든 테이블을 삭제합니다. 이 명령어는 다른 애플리케이션과 데이터베이스를 공유하는 환경에서 사용 시 특별히 주의해야 합니다.

<a name="tables"></a>
## 테이블 (Tables)

<a name="creating-tables"></a>
### 테이블 생성 (Creating Tables)

새로운 데이터베이스 테이블을 생성하려면, `Schema` 파사드의 `create` 메서드를 사용합니다. `create` 메서드는 두 개의 인수를 받습니다. 첫 번째 인수는 테이블명이고, 두 번째 인수는 테이블 생성을 정의할 수 있도록 `Blueprint` 객체를 전달받는 클로저입니다.

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

테이블 생성 시, [컬럼 메서드](#creating-columns)를 사용하여 다양한 컬럼을 정의할 수 있습니다.

<a name="determining-table-column-existence"></a>
#### 테이블/컬럼 존재 여부 확인

`hasTable`, `hasColumn`, `hasIndex` 메서드를 이용해 테이블, 컬럼, 인덱스의 존재 여부를 확인할 수 있습니다.

```php
if (Schema::hasTable('users')) {
    // "users" 테이블이 존재합니다...
}

if (Schema::hasColumn('users', 'email')) {
    // "users" 테이블에 "email" 컬럼이 존재합니다...
}

if (Schema::hasIndex('users', ['email'], 'unique')) {
    // "users" 테이블에 "email" 컬럼에 대한 유니크 인덱스가 존재합니다...
}
```

<a name="database-connection-table-options"></a>
#### 데이터베이스 연결 및 테이블 옵션

데이터베이스 기본 연결이 아닌 다른 데이터베이스에서 스키마 작업을 수행하려면, `connection` 메서드를 사용할 수 있습니다.

```php
Schema::connection('sqlite')->create('users', function (Blueprint $table) {
    $table->id();
});
```

또한 테이블 생성 시 몇 가지 추가 속성 및 메서드를 사용할 수 있습니다. MariaDB나 MySQL에서는 `engine` 속성으로 저장 엔진을 지정할 수 있습니다.

```php
Schema::create('users', function (Blueprint $table) {
    $table->engine('InnoDB');

    // ...
});
```

MariaDB 혹은 MySQL에서 테이블의 `charset`(문자셋)과 `collation`(정렬 방식)도 지정할 수 있습니다.

```php
Schema::create('users', function (Blueprint $table) {
    $table->charset('utf8mb4');
    $table->collation('utf8mb4_unicode_ci');

    // ...
});
```

테이블을 "임시" 테이블로 만들고 싶다면 `temporary` 메서드를 사용할 수 있습니다. 임시 테이블은 현재 데이터베이스 세션에만 보이고, 연결이 종료되면 자동으로 삭제됩니다.

```php
Schema::create('calculations', function (Blueprint $table) {
    $table->temporary();

    // ...
});
```

테이블에 "코멘트"를 추가하고 싶다면, 테이블 인스턴스의 `comment` 메서드를 사용할 수 있습니다. 테이블 코멘트는 현재 MariaDB, MySQL, PostgreSQL에서만 지원됩니다.

```php
Schema::create('calculations', function (Blueprint $table) {
    $table->comment('Business calculations');

    // ...
});
```

<a name="updating-tables"></a>
### 테이블 수정 (Updating Tables)

기존 테이블을 수정하려면 `Schema` 파사드의 `table` 메서드를 사용할 수 있습니다. `create` 메서드와 마찬가지로, 두 개의 인수를 받으며, 테이블명과 `Blueprint` 인스턴스를 전달받는 클로저입니다.

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->integer('votes');
});
```

<a name="renaming-and-dropping-tables"></a>
### 테이블 이름 변경 및 삭제 (Renaming / Dropping Tables)

기존 데이터베이스 테이블의 이름을 변경하려면, `rename` 메서드를 사용하세요.

```php
use Illuminate\Support\Facades\Schema;

Schema::rename($from, $to);
```

기존 테이블을 삭제하려면 `drop` 또는 `dropIfExists` 메서드를 사용할 수 있습니다.

```php
Schema::drop('users');

Schema::dropIfExists('users');
```

<a name="renaming-tables-with-foreign-keys"></a>
#### 외래 키가 있는 테이블 이름 변경

테이블 이름을 변경하기 전에, 해당 테이블의 모든 외래 키 제약조건이 Laravel에서 자동 생성한 이름이 아니라, 마이그레이션에서 명확하게 지정된 이름인지 반드시 확인해야 합니다. 그렇지 않으면 외래 키 제약조건의 이름이 이전 테이블명을 참조하게 됩니다.

<a name="columns"></a>
## 컬럼 (Columns)

<a name="creating-columns"></a>
### 컬럼 생성 (Creating Columns)

기존 테이블에 컬럼을 추가하려면 `Schema` 파사드의 `table` 메서드를 사용할 수 있습니다. `create` 메서드와 마찬가지로, 두 개의 인수를 받으며, 테이블명과 `Illuminate\Database\Schema\Blueprint` 인스턴스를 전달받는 클로저입니다.

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->integer('votes');
});
```

<a name="available-column-types"></a>
### 사용 가능한 컬럼 타입 (Available Column Types)

스키마 빌더 블루프린트는 데이터베이스 테이블에 추가할 수 있는 다양한 컬럼 타입에 대응하는 다양한 메서드를 제공합니다. 아래 표에는 사용할 수 있는 모든 메서드가 나열되어 있습니다.



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
#### 오브젝트 및 JSON 타입

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

#### 연관관계 타입

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

이후 모든 컬럼 타입 설명은 원문과 동일하게 출력합니다.

<a name="column-modifiers"></a>
### 컬럼 수정자 (Column Modifiers)

위에서 소개한 컬럼 타입 외에도, 데이터베이스 테이블에 컬럼을 추가할 때 사용할 수 있는 여러 가지 컬럼 "수정자"가 존재합니다. 예를 들어, 컬럼을 "nullable"하게 만들려면 `nullable` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->string('email')->nullable();
});
```

다음 표는 모든 사용 가능한 컬럼 수정자를 포함하고 있습니다. 이 목록에는 [인덱스 수정자](#creating-indexes)는 포함하지 않습니다.

<div class="overflow-auto">

| 수정자                                   | 설명                                                                               |
| ----------------------------------- | ----------------------------------------------------------------------------------- |
| `->after('column')`                 | 특정 컬럼 뒤에 새로운 컬럼을 배치 (MariaDB / MySQL).                                 |
| `->autoIncrement()`                 | `INTEGER` 컬럼을 자동 증가(Primary Key)로 설정.                                      |
| `->charset('utf8mb4')`              | 컬럼의 문자셋을 지정 (MariaDB / MySQL).                                              |
| `->collation('utf8mb4_unicode_ci')` | 컬럼의 Collation(정렬 방식)을 지정.                                                  |
| `->comment('my comment')`           | 컬럼에 주석 추가 (MariaDB / MySQL / PostgreSQL).                                     |
| `->default($value)`                 | 컬럼에 "기본값" 지정.                                                                |
| `->first()`                         | 컬럼을 테이블의 첫 번째 위치에 추가 (MariaDB / MySQL).                               |
| `->from($integer)`                  | 자동 증가 필드의 시작값 설정 (MariaDB / MySQL / PostgreSQL).                         |
| `->invisible()`                     | 컬럼을 `SELECT *` 쿼리에서 보이지 않게 설정 (MariaDB / MySQL).                       |
| `->nullable($value = true)`         | 컬럼에 `NULL` 값을 허용.                                                             |
| `->storedAs($expression)`           | 저장된 생성 컬럼 생성 (MariaDB / MySQL / PostgreSQL / SQLite).                       |
| `->unsigned()`                      | `INTEGER` 컬럼을 `UNSIGNED`로 설정 (MariaDB / MySQL).                                |
| `->useCurrent()`                    | `TIMESTAMP` 컬럼의 기본값을 `CURRENT_TIMESTAMP`로 설정.                              |
| `->useCurrentOnUpdate()`            | 레코드가 업데이트될 때 `TIMESTAMP` 컬럼을 `CURRENT_TIMESTAMP`로 업데이트 (MariaDB / MySQL). |
| `->virtualAs($expression)`          | 가상 생성 컬럼 생성 (MariaDB / MySQL / SQLite).                                      |
| `->generatedAs($expression)`        | 시퀀스 옵션이 적용된 identity 컬럼 생성 (PostgreSQL).                                |
| `->always()`                        | identity 컬럼의 우선순위를 입력값보다 시퀀스 값이 우선하도록 지정(PostgreSQL).         |

</div>

<a name="default-expressions"></a>
#### 기본값 표현식(Default Expressions)

`default` 수정자는 값이나 `Illuminate\Database\Query\Expression` 인스턴스를 받을 수 있습니다. `Expression` 인스턴스를 사용하면, Laravel이 값을 따옴표로 감싸지 않으므로, 데이터베이스의 특정 함수를 지정할 수 있습니다. 예를 들어 JSON 컬럼에 기본값을 지정하고 싶을 때 유용합니다.

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
> 기본값 표현식 지원은 사용하는 데이터베이스 드라이버, 데이터베이스 버전, 필드 타입에 따라 다릅니다. 자세한 내용은 데이터베이스 설명서를 참고하세요.

<a name="column-order"></a>
#### 컬럼 순서(Column Order)

MariaDB 또는 MySQL 데이터베이스를 사용할 때, `after` 메서드를 이용해 기존 컬럼 뒤에 새로운 컬럼을 추가할 수 있습니다.

```php
$table->after('password', function (Blueprint $table) {
    $table->string('address_line1');
    $table->string('address_line2');
    $table->string('city');
});
```

<a name="modifying-columns"></a>
### 컬럼 수정 (Modifying Columns)

`change` 메서드를 사용하면 기존 컬럼의 타입이나 속성을 변경할 수 있습니다. 예를 들어, `string` 컬럼의 길이를 늘리고자 한다면, 컬럼의 새로운 상태를 정의한 뒤 `change` 메서드를 호출하면 됩니다.

```php
Schema::table('users', function (Blueprint $table) {
    $table->string('name', 50)->change();
});
```

컬럼을 수정할 때는, 유지하고자 하는 모든 수정자를 명시적으로 포함해야 합니다. 누락된 속성은 모두 사라집니다. 예를 들어, `unsigned`, `default`, `comment` 속성을 유지하려면 각 수정자를 명시적으로 호출해야 합니다.

```php
Schema::table('users', function (Blueprint $table) {
    $table->integer('votes')->unsigned()->default(1)->comment('my comment')->change();
});
```

`change` 메서드는 컬럼의 인덱스 상태를 변경하지 않습니다. 따라서, 인덱스를 추가하거나 삭제하려면 인덱스 설정자를 명시적으로 사용해야 합니다.

```php
// 인덱스 추가...
$table->bigIncrements('id')->primary()->change();

// 인덱스 삭제...
$table->char('postal_code', 10)->unique(false)->change();
```

<a name="renaming-columns"></a>
### 컬럼 이름 변경 (Renaming Columns)

컬럼의 이름을 변경하려면, 스키마 빌더의 `renameColumn` 메서드를 사용하면 됩니다.

```php
Schema::table('users', function (Blueprint $table) {
    $table->renameColumn('from', 'to');
});
```

<a name="dropping-columns"></a>
### 컬럼 삭제 (Dropping Columns)

컬럼을 삭제하려면, 스키마 빌더의 `dropColumn` 메서드를 사용할 수 있습니다.

```php
Schema::table('users', function (Blueprint $table) {
    $table->dropColumn('votes');
});
```

여러 컬럼을 한 번에 삭제하려면, `dropColumn` 메서드에 컬럼명 배열을 전달하면 됩니다.

```php
Schema::table('users', function (Blueprint $table) {
    $table->dropColumn(['votes', 'avatar', 'location']);
});
```

<a name="available-command-aliases"></a>
#### 사용 가능한 명령어 별칭

Laravel은 흔히 사용하는 컬럼 삭제 작업을 위해 몇 가지 편의 메서드를 제공합니다. 각 메서드는 아래 표에서 설명합니다.

<div class="overflow-auto">

| 명령어                                 | 설명                                           |
| ----------------------------------- | ----------------------------------------------|
| `$table->dropMorphs('morphable');`  | `morphable_id`와 `morphable_type` 컬럼 삭제.   |
| `$table->dropRememberToken();`      | `remember_token` 컬럼 삭제.                    |
| `$table->dropSoftDeletes();`        | `deleted_at` 컬럼 삭제.                        |
| `$table->dropSoftDeletesTz();`      | `dropSoftDeletes()`의 별칭.                    |
| `$table->dropTimestamps();`         | `created_at`, `updated_at` 컬럼 삭제.          |
| `$table->dropTimestampsTz();`       | `dropTimestamps()`의 별칭.                     |

</div>

<a name="indexes"></a>
## 인덱스 (Indexes)

<a name="creating-indexes"></a>
### 인덱스 생성 (Creating Indexes)

Laravel 스키마 빌더는 여러 종류의 인덱스를 지원합니다. 아래 예시는 새 `email` 컬럼을 생성하면서 해당 값이 유일함을 지정합니다. 인덱스를 생성하려면 컬럼 정의에 `unique` 메서드를 체인으로 연결하면 됩니다.

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->string('email')->unique();
});
```

또는 컬럼을 정의 한 후에 인덱스를 생성할 수도 있습니다. 이 경우, 스키마 빌더 블루프린트의 `unique` 메서드를 사용합니다. 이 메서드는 유니크 인덱스를 적용할 컬럼명을 인수로 받습니다.

```php
$table->unique('email');
```

여러 컬럼을 한 번에 인덱싱해서 복합(컴포지트) 인덱스를 만들 수도 있습니다.

```php
$table->index(['account_id', 'created_at']);
```

인덱스 생성 시 Laravel이 테이블명, 컬럼명, 인덱스 타입을 기반으로 인덱스명을 자동 생성하지만, 메서드의 두 번째 인자로 직접 인덱스명을 명시할 수 있습니다.

```php
$table->unique('email', 'unique_email');
```

<a name="available-index-types"></a>
#### 사용 가능한 인덱스 타입

Laravel의 스키마 빌더의 블루프린트 클래스는, Laravel이 지원하는 모든 인덱스 타입을 위한 메서드를 제공합니다. 각 인덱스 메서드는 선택적으로 두 번째 인자로 인덱스명을 지정할 수 있습니다. 생략하면 테이블, 컬럼, 인덱스 타입 조합에 따라 자동 생성됩니다. 아래 표는 사용 가능한 인덱스 메서드를 설명합니다.

<div class="overflow-auto">

| 명령어                                   | 설명                                                          |
| ------------------------------------ | ---------------------------------------------------------- |
| `$table->primary('id');`             | Primary Key 추가.                                           |
| `$table->primary(['id', 'parent_id']);` | 복합 키 추가.                                            |
| `$table->unique('email');`            | 유니크 인덱스 추가.                                         |
| `$table->index('state');`             | 일반 인덱스 추가.                                           |
| `$table->fullText('body');`           | 전문(Full Text) 인덱스 추가 (MariaDB / MySQL / PostgreSQL). |
| `$table->fullText('body')->language('english');` | 특정 언어의 전문 인덱스 추가 (PostgreSQL).        |
| `$table->spatialIndex('location');`   | 공간(Spatial) 인덱스 추가 (SQLite 제외).                    |

</div>

<a name="renaming-indexes"></a>
### 인덱스 이름 변경 (Renaming Indexes)

인덱스의 이름을 변경하려면, 스키마 빌더 블루프린트의 `renameIndex` 메서드를 사용할 수 있습니다. 이 메서드는 첫 번째 인수로 현재 인덱스 이름, 두 번째 인수로 새 인덱스 이름을 받습니다.

```php
$table->renameIndex('from', 'to')
```

<a name="dropping-indexes"></a>
### 인덱스 삭제 (Dropping Indexes)

인덱스를 삭제하려면 인덱스의 이름을 명시해야 합니다. 기본적으로 Laravel은 테이블명, 컬럼명, 인덱스 타입을 기반으로 인덱스 이름을 자동으로 생성합니다. 아래 표는 예시를 보여줍니다.

<div class="overflow-auto">

| 명령어                                         | 설명                                                  |
| ------------------------------------------ | ------------------------------------------------- |
| `$table->dropPrimary('users_id_primary');` | "users" 테이블에서 Primary Key 삭제.                |
| `$table->dropUnique('users_email_unique');`| "users" 테이블에서 유니크 인덱스 삭제.              |
| `$table->dropIndex('geo_state_index');`    | "geo" 테이블에서 일반 인덱스 삭제.                  |
| `$table->dropFullText('posts_body_fulltext');` | "posts" 테이블에서 전문 인덱스 삭제.                |
| `$table->dropSpatialIndex('geo_location_spatialindex');` | "geo" 테이블에서 공간 인덱스 삭제 (SQLite 제외). |

</div>

인덱스 삭제 메서드에 컬럼명 배열을 전달하면, 관례에 따라 인덱스명이 자동으로 생성되어 지정한 인덱스가 찾아집니다.

```php
Schema::table('geo', function (Blueprint $table) {
    $table->dropIndex(['state']); // 'geo_state_index' 인덱스 삭제
});
```

<a name="foreign-key-constraints"></a>
### 외래 키 제약조건 (Foreign Key Constraints)

Laravel은 데이터베이스 레벨에서 참조 무결성을 보장하기 위한 외래 키 제약조건 생성도 지원합니다. 예를 들어, `posts` 테이블의 `user_id` 컬럼이 `users` 테이블의 `id` 컬럼을 참조하도록 지정할 수 있습니다.

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('posts', function (Blueprint $table) {
    $table->unsignedBigInteger('user_id');

    $table->foreign('user_id')->references('id')->on('users');
});
```

이 구문이 다소 장황하므로, Laravel에서는 더 짧은 대체 메서드를 제공합니다. `foreignId` 메서드로 컬럼을 만들 때는 아래처럼 코드를 간결하게 쓸 수 있습니다.

```php
Schema::table('posts', function (Blueprint $table) {
    $table->foreignId('user_id')->constrained();
});
```

`foreignId` 메서드는 `UNSIGNED BIGINT` 컬럼을 생성하고, `constrained` 메서드는 관례에 따라 참조할 테이블 및 컬럼을 결정합니다. 테이블명이 관례와 다르거나, 직접 설정이 필요하다면, `constrained` 메서드에 인수로 직접 테이블명 혹은 인덱스명을 지정할 수 있습니다.

```php
Schema::table('posts', function (Blueprint $table) {
    $table->foreignId('user_id')->constrained(
        table: 'users', indexName: 'posts_user_id'
    );
});
```

제약조건의 "on delete", "on update" 동작도 아래처럼 명확히 지정할 수 있습니다.

```php
$table->foreignId('user_id')
    ->constrained()
    ->onUpdate('cascade')
    ->onDelete('cascade');
```

이러한 동작을 위한 대체 문법도 제공합니다.

<div class="overflow-auto">

| 메서드                         | 설명                                                  |
| ----------------------------- | ------------------------------------------------- |
| `$table->cascadeOnUpdate();`  | 업데이트 시 연쇄(cascade) 동작.                      |
| `$table->restrictOnUpdate();` | 업데이트 시 제한(restrict) 동작.                     |
| `$table->nullOnUpdate();`     | 업데이트 시 외래 키 값을 null로 설정.                |
| `$table->noActionOnUpdate();` | 업데이트 시 아무 동작 없음.                          |
| `$table->cascadeOnDelete();`  | 삭제 시 연쇄(cascade) 동작.                         |
| `$table->restrictOnDelete();` | 삭제 시 제한(restrict) 동작.                        |
| `$table->nullOnDelete();`     | 삭제 시 외래 키 값을 null로 설정.                   |
| `$table->noActionOnDelete();` | 자식 레코드가 있으면 삭제 불가.                     |

</div>

추가적인 [컬럼 수정자](#column-modifiers)는 반드시 `constrained` 메서드 호출 전에 작성해야 합니다.

```php
$table->foreignId('user_id')
    ->nullable()
    ->constrained();
```

<a name="dropping-foreign-keys"></a>
#### 외래 키 삭제

외래 키를 삭제하려면 삭제 대상 외래 키 제약조건의 이름을 `dropForeign` 메서드에 인수로 넘겨주면 됩니다. 외래 키 제약조건의 이름은 인덱스 이름과 동일한 규칙으로 생성되며, 테이블명, 컬럼명, 마지막에 "\_foreign" 접미사가 붙습니다.

```php
$table->dropForeign('posts_user_id_foreign');
```

또는, 외래 키가 걸린 컬럼명을 배열로 넘기면 관례에 따라 제약조건 이름이 자동으로 생성되어 해당 외래 키가 삭제됩니다.

```php
$table->dropForeign(['user_id']);
```

<a name="toggling-foreign-key-constraints"></a>
#### 외래 키 제약조건 활성화/비활성화

마이그레이션 내에서 아래 메서드를 사용해 외래 키 제약조건을 활성화하거나 비활성화할 수 있습니다.

```php
Schema::enableForeignKeyConstraints();

Schema::disableForeignKeyConstraints();

Schema::withoutForeignKeyConstraints(function () {
    // 이 클로저 내부에서는 제약조건이 비활성화됩니다...
});
```

> [!WARNING]
> SQLite는 기본적으로 외래 키 제약조건이 비활성화되어 있습니다. SQLite를 사용하는 경우, 마이그레이션으로 외래 키를 생성하기 전에 [외래 키 지원을 활성화](/docs/12.x/database#configuration)해야 합니다.

<a name="events"></a>
## 이벤트 (Events)

편의상, 각 마이그레이션 작업은 [이벤트](/docs/12.x/events)를 발생시킵니다. 아래의 모든 이벤트는 베이스 클래스인 `Illuminate\Database\Events\MigrationEvent`를 상속받습니다.

<div class="overflow-auto">

| 클래스                                          | 설명                                        |
| ---------------------------------------------- | ------------------------------------------- |
| `Illuminate\Database\Events\MigrationsStarted`   | 마이그레이션 배치가 곧 실행될 때 발생.       |
| `Illuminate\Database\Events\MigrationsEnded`     | 마이그레이션 배치가 실행을 마쳤을 때 발생.   |
| `Illuminate\Database\Events\MigrationStarted`    | 단일 마이그레이션이 곧 실행될 때 발생.       |
| `Illuminate\Database\Events\MigrationEnded`      | 단일 마이그레이션이 실행을 마쳤을 때 발생.   |
| `Illuminate\Database\Events\NoPendingMigrations` | 실행할 남은 마이그레이션이 없을 때 발생.     |
| `Illuminate\Database\Events\SchemaDumped`        | 데이터베이스 스키마 덤프가 완료되었을 때 발생.|
| `Illuminate\Database\Events\SchemaLoaded`        | 스키마 덤프가 데이터베이스에 로드될 때 발생. |

</div>
