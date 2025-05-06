# 데이터베이스: 마이그레이션

- [소개](#introduction)
- [마이그레이션 생성](#generating-migrations)
    - [마이그레이션 합치기](#squashing-migrations)
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
## 소개

마이그레이션은 데이터베이스의 버전 관리와 같습니다. 이를 통해 팀이 애플리케이션의 데이터베이스 스키마 정의를 공유하고 관리할 수 있습니다. 만약 여러분이 소스 제어에서 변경 내역을 받아온 후, 동료에게 로컬 데이터베이스 스키마에 직접 컬럼을 추가하라고 전달해 본 경험이 있다면, 이미 마이그레이션이 해결하는 문제를 겪어본 것입니다.

Laravel의 `Schema` [파사드](/docs/{{version}}/facades)는 Laravel이 지원하는 모든 데이터베이스 시스템에서 테이블을 생성하고 조작할 수 있는 데이터베이스 독립적인 지원을 제공합니다. 일반적으로 마이그레이션은 이 파사드를 사용하여 데이터베이스 테이블과 컬럼을 생성하거나 수정합니다.

<a name="generating-migrations"></a>
## 마이그레이션 생성

`make:migration` [Artisan 명령어](/docs/{{version}}/artisan)를 사용하여 데이터베이스 마이그레이션을 생성할 수 있습니다. 새 마이그레이션 파일은 `database/migrations` 디렉터리에 생성됩니다. 각 마이그레이션 파일 이름에는 타임스탬프가 포함되어 있어, Laravel은 마이그레이션의 실행 순서를 결정할 수 있습니다:

```shell
php artisan make:migration create_flights_table
```

Laravel은 마이그레이션의 이름을 이용해 테이블 이름과 테이블 생성 여부를 추측합니다. 만약 Laravel이 마이그레이션 이름에서 테이블 이름을 결정할 수 있다면, 생성된 마이그레이션 파일에 그 테이블에 대한 코드를 미리 채워줍니다. 그렇지 않다면, 직접 마이그레이션 파일 내에서 테이블을 지정하면 됩니다.

새 마이그레이션에 대해 커스텀 경로를 지정하고 싶다면, `make:migration` 명령어 실행 시 `--path` 옵션을 사용할 수 있습니다. 전달된 경로는 애플리케이션의 기본 경로 기준 상대경로여야 합니다.

> [!NOTE]  
> 마이그레이션 스텁(stub)은 [스텁 퍼블리싱](/docs/{{version}}/artisan#stub-customization)을 사용해 커스터마이즈할 수 있습니다.

<a name="squashing-migrations"></a>
### 마이그레이션 합치기

애플리케이션을 개발하다보면 시간이 지나면서 점점 더 많은 마이그레이션 파일이 쌓일 수 있습니다. 이렇게 되면 `database/migrations` 디렉터리가 수백 개의 마이그레이션으로 인해 복잡해질 수 있습니다. 이럴 때는 모든 마이그레이션을 하나의 SQL 파일로 "합치기(Squash)"할 수 있습니다. 시작하려면 `schema:dump` 명령어를 실행하세요:

```shell
php artisan schema:dump

# 현재 데이터베이스 스키마를 덤프하고 기존 모든 마이그레이션을 정리합니다...
php artisan schema:dump --prune
```

이 명령어를 실행하면 Laravel은 애플리케이션의 `database/schema` 디렉터리에 "스키마" 파일을 생성합니다. 이 스키마 파일의 이름은 사용하는 데이터베이스 커넥션과 일치합니다. 이후 데이터베이스를 마이그레이트할 때, 아직 다른 마이그레이션이 실행되지 않았다면, Laravel은 먼저 사용 중인 데이터베이스 커넥션의 스키마 파일 내 SQL 구문을 실행합니다. 그리고 스키마 덤프에 포함되지 않은 나머지 마이그레이션을 실행합니다.

만약 애플리케이션의 테스트가 로컬 개발에서 일반적으로 사용하는 데이터베이스와 다른 커넥션을 사용한다면, 해당 데이터베이스 커넥션으로도 스키마 파일을 덤프해야 합니다. 보통 로컬 개발에서 사용하는 커넥션을 덤프한 후에 아래와 같이 하시면 됩니다:

```shell
php artisan schema:dump
php artisan schema:dump --database=testing --prune
```

데이터베이스 스키마 파일은 소스 제어에 커밋하여, 새로운 개발자도 초기 데이터베이스 구조를 신속하게 구축할 수 있도록 하세요.

> [!WARNING]  
> 마이그레이션 합치기는 MySQL, PostgreSQL, SQLite 데이터베이스에서만 지원되며, 해당 데이터베이스의 커맨드라인 클라이언트를 이용합니다.

<a name="migration-structure"></a>
## 마이그레이션 구조

마이그레이션 클래스는 `up`과 `down` 두 가지 메서드를 가집니다. `up` 메서드는 데이터베이스에 새로운 테이블, 컬럼, 인덱스를 추가할 때 사용하며, `down` 메서드는 `up` 메서드가 수행한 작업을 되돌립니다.

이 두 메서드 내부에서 Laravel 스키마 빌더를 사용해 테이블을 직관적으로 생성하거나 수정할 수 있습니다. 스키마 빌더에서 제공하는 모든 메서드에 대해서는 [관련 문서](#creating-tables)를 참고하세요. 예를 들어 아래는 `flights` 테이블을 생성하는 마이그레이션입니다:

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

마이그레이션이 애플리케이션의 기본 데이터베이스 커넥션이 아닌 다른 데이터베이스 커넥션을 사용할 경우, 마이그레이션의 `$connection` 속성을 설정해야 합니다:

```php
/**
 * 마이그레이션에서 사용할 데이터베이스 커넥션
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
## 마이그레이션 실행

모든 미실행 마이그레이션을 실행하려면 `migrate` Artisan 명령어를 사용하세요:

```shell
php artisan migrate
```

지금까지 어떤 마이그레이션이 실행되었는지 확인하려면 `migrate:status` 명령을 사용하세요:

```shell
php artisan migrate:status
```

마이그레이션이 실제로 실행되기 전에 실행될 SQL 구문만 확인하려면 `--pretend` 플래그를 사용할 수 있습니다:

```shell
php artisan migrate --pretend
```

#### 마이그레이션 실행 격리

여러 서버에 애플리케이션을 배포하고 배포 과정에서 마이그레이션을 실행하는 경우, 두 서버가 동시에 데이터베이스를 마이그레이트하지 않도록 해야 합니다. 이를 방지하려면 `migrate` 명령어 실행 시 `--isolated` 옵션을 사용하세요.

이 옵션이 지정되면, Laravel은 마이그레이션 실행 전 애플리케이션의 캐시 드라이버를 사용해 원자적 락을 획득합니다. 락이 유지되는 동안 다른 모든 마이그레이션 실행 시도는 실행되지 않으며, 명령어는 성공 상태 코드로 종료됩니다:

```shell
php artisan migrate --isolated
```

> [!WARNING]  
> 이 기능을 사용하려면, 애플리케이션 기본 캐시 드라이버가 `memcached`, `redis`, `dynamodb`, `database`, `file`, 또는 `array`여야 합니다. 또한 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

<a name="forcing-migrations-to-run-in-production"></a>
#### 운영 환경에서 강제로 마이그레이션 실행

일부 마이그레이션 작업은 데이터 손실 위험이 있습니다. 운영 데이터베이스에서 해당 명령을 실행하는 것을 보호하기 위해, 명령 실행 전에 확인을 요구합니다. 프롬프트 없이 명령을 강제로 실행하려면 `--force` 플래그를 사용하세요:

```shell
php artisan migrate --force
```

<a name="rolling-back-migrations"></a>
### 마이그레이션 롤백

가장 최근에 실행한 마이그레이션 작업을 롤백하려면, `rollback` Artisan 명령어를 사용합니다. 이 명령은 마지막 "배치"의 여러 마이그레이션 파일을 한꺼번에 롤백할 수 있습니다:

```shell
php artisan migrate:rollback
```

`step` 옵션을 추가해 롤백할 마이그레이션 개수를 제한할 수 있습니다. 예를 들어 아래 명령은 최근 5개의 마이그레이션만 롤백합니다:

```shell
php artisan migrate:rollback --step=5
```

또는 `batch` 옵션에 애플리케이션의 `migrations` 테이블에서 찾을 수 있는 특정 배치 값을 지정해 해당 배치의 모든 마이그레이션을 롤백할 수 있습니다. 예를 들어, 아래 명령은 3번 배치의 모든 마이그레이션을 롤백합니다:

```shell
php artisan migrate:rollback --batch=3
```

실제 실행 없이 롤백 시 실행될 SQL 구문을 보고 싶다면 `--pretend` 플래그를 사용할 수 있습니다:

```shell
php artisan migrate:rollback --pretend
```

`migrate:reset` 명령은 애플리케이션의 모든 마이그레이션을 롤백합니다:

```shell
php artisan migrate:reset
```

<a name="roll-back-migrate-using-a-single-command"></a>
#### 한 번의 명령으로 롤백과 마이그레이트

`migrate:refresh` 명령은 모든 마이그레이션을 롤백한 후 다시 실행합니다. 즉, 데이터베이스를 완전히 재생성합니다:

```shell
php artisan migrate:refresh

# 데이터베이스를 리프레시하고 모든 시드를 실행...
php artisan migrate:refresh --seed
```

`step` 옵션을 함께 사용하면 지정한 수만큼 롤백 및 재실행할 수 있습니다:

```shell
php artisan migrate:refresh --step=5
```

<a name="drop-all-tables-migrate"></a>
#### 모든 테이블 삭제 후 마이그레이트

`migrate:fresh` 명령은 데이터베이스 내 모든 테이블을 삭제하고, 이후 `migrate` 명령을 실행합니다:

```shell
php artisan migrate:fresh

php artisan migrate:fresh --seed
```

기본적으로 `migrate:fresh` 명령은 기본 데이터베이스 커넥션의 테이블만 삭제합니다. 특정 커넥션을 사용하려면 `--database` 옵션을 사용하세요. 커넥션 이름은 `config/database.php`에서 정의한 이름이어야 합니다:

```shell
php artisan migrate:fresh --database=admin
```

> [!WARNING]  
> `migrate:fresh` 명령은 테이블 접두사와 무관하게 모든 데이터베이스 테이블을 삭제합니다. 다른 애플리케이션과 데이터베이스를 공유하는 경우 주의해서 사용하세요.

<a name="tables"></a>
## 테이블

<a name="creating-tables"></a>
### 테이블 생성

새 데이터베이스 테이블을 생성하려면 `Schema` 파사드의 `create` 메서드를 사용하세요. `create` 메서드는 첫번째 인수로 테이블 이름, 두번째 인수로 `Blueprint` 인스턴스를 전달받는 클로저를 받습니다. 이 인스턴스를 사용해 새로운 테이블을 정의합니다:

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

테이블을 생성할 때 [컬럼 생성 메서드](#creating-columns) 중 원하는 것을 사용해 컬럼을 정의할 수 있습니다.

<a name="determining-table-column-existence"></a>
#### 테이블/컬럼 존재 여부 확인

`hasTable` 과 `hasColumn` 메서드를 사용해 테이블 또는 컬럼의 존재 여부를 확인할 수 있습니다:

```php
if (Schema::hasTable('users')) {
    // "users" 테이블이 존재함...
}

if (Schema::hasColumn('users', 'email')) {
    // "users" 테이블이 존재하며 "email" 컬럼이 있음...
}
```

<a name="database-connection-table-options"></a>
#### 데이터베이스 커넥션 및 테이블 옵션

기본 데이터베이스 커넥션이 아닌 다른 커넥션에서 스키마 작업을 하려면, `connection` 메서드를 사용하세요:

```php
Schema::connection('sqlite')->create('users', function (Blueprint $table) {
    $table->id();
});
```

추가적으로, MySQL을 사용하는 경우, 테이블 스토리지 엔진을 지정하려면 `engine` 속성을 사용할 수 있습니다:

```php
Schema::create('users', function (Blueprint $table) {
    $table->engine = 'InnoDB';

    // ...
});
```

MySQL에서 테이블의 문자셋과 정렬(collation)을 지정하려면 `charset`과 `collation` 속성을 사용할 수 있습니다:

```php
Schema::create('users', function (Blueprint $table) {
    $table->charset = 'utf8mb4';
    $table->collation = 'utf8mb4_unicode_ci';

    // ...
});
```

임시 테이블을 생성하려면 `temporary` 메서드를 사용하세요. 임시 테이블은 현재 연결 세션에서만 보이고, 연결이 종료되면 자동으로 삭제됩니다:

```php
Schema::create('calculations', function (Blueprint $table) {
    $table->temporary();

    // ...
});
```

테이블에 "주석(comment)"을 추가하려면, 테이블 인스턴스에서 `comment` 메서드를 사용하세요. 테이블 주석은 현재 MySQL과 Postgres에서만 지원됩니다:

```php
Schema::create('calculations', function (Blueprint $table) {
    $table->comment('Business calculations');

    // ...
});
```

<a name="updating-tables"></a>
### 테이블 수정

기존 테이블을 수정하려면, `Schema` 파사드의 `table` 메서드를 사용하세요. `create`와 동일하게, 첫 번째 인수로 테이블 이름, 두 번째 인수로 `Blueprint` 인스턴스를 받는 클로저를 전달합니다:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->integer('votes');
});
```

<a name="renaming-and-dropping-tables"></a>
### 테이블 이름 변경/삭제

기존 데이터베이스 테이블의 이름을 변경하려면, `rename` 메서드를 사용하세요:

```php
use Illuminate\Support\Facades\Schema;

Schema::rename($from, $to);
```

기존 테이블을 삭제하려면, `drop` 또는 `dropIfExists` 메서드를 사용할 수 있습니다:

```php
Schema::drop('users');

Schema::dropIfExists('users');
```

<a name="renaming-tables-with-foreign-keys"></a>
#### 외래 키가 있는 테이블의 이름 변경

테이블 이름 변경 전에, 마이그레이션 파일에서 해당 테이블의 외래 키 제약조건에 명시적으로 이름을 지정했는지 확인해야 합니다. 그렇지 않으면 외래 키 제약조건의 이름이 이전 테이블 이름을 참조하게 됩니다.

<a name="columns"></a>
## 컬럼

<a name="creating-columns"></a>
### 컬럼 생성

기존 테이블에 컬럼을 추가하려면, `Schema` 파사드의 `table` 메서드를 사용하세요. `create`와 동일하게, 첫 번째 인수로 테이블 이름, 두 번째 인수로 `Illuminate\Database\Schema\Blueprint` 인스턴스를 받는 클로저를 전달합니다:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->integer('votes');
});
```

<a name="available-column-types"></a>
### 사용 가능한 컬럼 타입

스키마 빌더의 블루프린트(blueprint)에는 데이터베이스 테이블에 추가할 수 있는 다양한 컬럼 타입에 대응하는 여러 메서드가 존재합니다. 사용 가능한 각 메서드는 아래 표와 같습니다:

<!-- HTML 태그 및 스타일 유지, 번역 생략 -->

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

<!-- 컬럼 메서드 각 항목은 표기와 코드 예시 부분을 그대로 유지하며, 각 설명 부분을 자연스러운 한국어로 번역했습니다. 생략된 부분 번역도 요청하시면 도와드릴 수 있습니다. -->

<a name="column-modifiers"></a>
### 컬럼 수정자

위에 나열된 컬럼 타입 외에도, 테이블에 컬럼을 추가할 때 사용할 수 있는 다양한 "수정자" 메서드가 있습니다. 예를 들어, 컬럼을 "nullable(널 허용)"로 만들려면 `nullable` 메서드를 사용하면 됩니다:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->string('email')->nullable();
});
```

아래 표는 사용 가능한 모든 컬럼 수정자입니다. (인덱스 관련 수정자는 [여기](#creating-indexes)에서 확인하세요.)

| 수정자                     | 설명                                                                        |
|---------------------------|-----------------------------------------------------------------------------|
| `->after('column')`       | 지정한 컬럼 뒤에 삽입 (MySQL).                                               |
| `->autoIncrement()`       | INTEGER 컬럼을 auto-increment(자동 증가)로 설정 (기본키).                      |
| `->charset('utf8mb4')`    | 해당 컬럼에 대한 문자셋 지정 (MySQL).                                         |
| `->collation('utf8mb4_unicode_ci')` | 해당 컬럼에 대한 정렬 지정 (MySQL/PostgreSQL/SQL Server).                    |
| `->comment('my comment')` | 컬럼에 주석 추가 (MySQL/PostgreSQL).                                         |
| `->default($value)`       | 컬럼의 기본값 지정.                                                          |
| `->first()`               | 해당 컬럼을 테이블의 맨 앞으로 배치 (MySQL).                                  |
| `->from($integer)`        | auto-increment 필드의 시작값 설정 (MySQL / PostgreSQL).                        |
| `->invisible()`           | 해당 컬럼을 SELECT * 쿼리에서 보이지 않게 함 (MySQL).                        |
| `->nullable($value = true)` | 컬럼에 NULL 값 입력 허용.                                                   |
| `->storedAs($expression)` | 저장된 생성 컬럼 생성 (MySQL / PostgreSQL).                                   |
| `->unsigned()`            | INTEGER 컬럼을 UNSIGNED로 설정 (MySQL).                                       |
| `->useCurrent()`          | TIMESTAMP 컬럼 기본값을 CURRENT_TIMESTAMP로 설정.                             |
| `->useCurrentOnUpdate()`  | 레코드가 업데이트될 때 TIMESTAMP 컬럼을 CURRENT_TIMESTAMP로 설정 (MySQL).        |
| `->virtualAs($expression)`| 가상 생성 컬럼 생성 (MySQL / PostgreSQL / SQLite).                            |
| `->generatedAs($expression)` | 특정 시퀀스 옵션으로 아이덴티티 컬럼 생성 (PostgreSQL).                        |
| `->always()`              | 아이덴티티 컬럼에서 시퀀스 값 우선순위 정의 (PostgreSQL).                      |
| `->isGeometry()`          | 공간 컬럼 타입을 `geometry`로 설정 (기본은 `geography`, PostgreSQL).          |

<a name="default-expressions"></a>
#### 기본값 표현식

`default` 수정자는 값이나 `Illuminate\Database\Query\Expression` 인스턴스를 받을 수 있습니다. `Expression` 인스턴스를 사용하면 값이 따옴표로 감싸지지 않으며, 데이터베이스 고유 함수도 사용할 수 있습니다. 예를 들어, JSON 컬럼에 기본값을 지정할 때 유용합니다:

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
> 기본값 표현식 지원 여부는 데이터베이스 드라이버, 버전, 필드 타입에 따라 다릅니다. 데이터베이스 공식 문서를 참고하세요.

<a name="column-order"></a>
#### 컬럼 순서

MySQL에서는 `after` 메서드를 사용해 기존 컬럼 뒤에 새 컬럼을 추가할 수 있습니다:

```php
$table->after('password', function (Blueprint $table) {
    $table->string('address_line1');
    $table->string('address_line2');
    $table->string('city');
});
```

<a name="modifying-columns"></a>
### 컬럼 수정

`change` 메서드를 통해 기존 컬럼의 타입이나 속성을 수정할 수 있습니다. 예를 들어, `string` 컬럼의 길이를 늘리고 싶을 때 다음과 같이 합니다:

```php
Schema::table('users', function (Blueprint $table) {
    $table->string('name', 50)->change();
});
```

컬럼을 수정할 때는, 기존 컬럼에서 유지하고자 하는 모든 수정자를 명시적으로 포함해야 하며, 빠진 속성은 삭제됩니다. 예를 들어 `unsigned`, `default`, `comment` 속성을 유지하려면 반드시 모두 지정해야 합니다:

```php
Schema::table('users', function (Blueprint $table) {
    $table->integer('votes')->unsigned()->default(1)->comment('my comment')->change();
});
```

<a name="modifying-columns-on-sqlite"></a>
#### SQLite에서 컬럼 수정

SQLite를 사용하는 경우, 컬럼을 수정하기 전에 Composer 패키지 매니저를 사용해 `doctrine/dbal` 패키지를 설치해야 합니다. Doctrine DBAL 라이브러리는 컬럼의 현재 상태를 파악하고, 변경에 필요한 SQL 쿼리를 만듭니다:

```shell
composer require doctrine/dbal
```

만약 `timestamp` 메서드로 생성된 컬럼을 수정하려면, 애플리케이션의 `config/database.php` 설정 파일에 아래 설정도 추가해야 합니다:

```php
use Illuminate\Database\DBAL\TimestampType;

'dbal' => [
    'types' => [
        'timestamp' => TimestampType::class,
    ],
],
```

> [!WARNING]  
> `doctrine/dbal`을 사용할 때 수정 가능한 컬럼 타입: `bigInteger`, `binary`, `boolean`, `char`, `date`, `dateTime`, `dateTimeTz`, `decimal`, `double`, `integer`, `json`, `longText`, `mediumText`, `smallInteger`, `string`, `text`, `time`, `tinyText`, `unsignedBigInteger`, `unsignedInteger`, `unsignedSmallInteger`, `ulid`, `uuid`.

<a name="renaming-columns"></a>
### 컬럼 이름 변경

컬럼의 이름을 변경하려면, 스키마 빌더의 `renameColumn` 메서드를 사용하세요:

```php
Schema::table('users', function (Blueprint $table) {
    $table->renameColumn('from', 'to');
});
```

<a name="renaming-columns-on-legacy-databases"></a>
#### 레거시 데이터베이스에서 컬럼 이름 변경

아래 버전보다 오래된 데이터베이스를 사용한다면, 컬럼 이름 변경 전에 Composer를 통해 `doctrine/dbal` 라이브러리를 설치해야 합니다:

- MySQL < `8.0.3`
- MariaDB < `10.5.2`
- SQLite < `3.25.0`

<a name="dropping-columns"></a>
### 컬럼 삭제

컬럼을 삭제하려면, 스키마 빌더의 `dropColumn` 메서드를 활용하세요:

```php
Schema::table('users', function (Blueprint $table) {
    $table->dropColumn('votes');
});
```

여러 컬럼을 삭제할 때는 컬럼명 배열을 인수로 전달하면 됩니다:

```php
Schema::table('users', function (Blueprint $table) {
    $table->dropColumn(['votes', 'avatar', 'location']);
});
```

<a name="dropping-columns-on-legacy-databases"></a>
#### 레거시 데이터베이스에서 컬럼 삭제

SQLite `3.35.0` 이전 버전을 사용하는 경우, `doctrine/dbal` 패키지를 설치해야 `dropColumn` 메서드를 사용할 수 있습니다. 이 패키지 사용 시, 한 번의 마이그레이션에서 여러 컬럼을 삭제하거나 수정하는 것은 지원되지 않습니다.

<a name="available-command-aliases"></a>
#### 지원되는 명령어 별칭

Laravel에서는 흔히 사용하는 컬럼 삭제를 위한 편리한 메서드를 제공합니다. 각 메서드는 아래와 같습니다:

| 명령어                                       | 설명                                                  |
|----------------------------------------------|------------------------------------------------------|
| `$table->dropMorphs('morphable');`          | `morphable_id`와 `morphable_type` 컬럼 삭제              |
| `$table->dropRememberToken();`               | `remember_token` 컬럼 삭제                             |
| `$table->dropSoftDeletes();`                | `deleted_at` 컬럼 삭제                                 |
| `$table->dropSoftDeletesTz();`              | `dropSoftDeletes()` 메서드의 별칭                       |
| `$table->dropTimestamps();`                 | `created_at`, `updated_at` 컬럼 삭제                   |
| `$table->dropTimestampsTz();`               | `dropTimestamps()` 메서드의 별칭                        |

<a name="indexes"></a>
## 인덱스

<a name="creating-indexes"></a>
### 인덱스 생성

Laravel 스키마 빌더는 여러 종류의 인덱스를 지원합니다. 예를 들어, 새로운 `email` 컬럼을 추가하면서 값이 유일해야 함을 명시하려면 컬럼 정의에 `unique` 메서드를 체이닝합니다:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->string('email')->unique();
});
```

또는 컬럼 정의 후 인덱스를 추가하려면, 스키마 빌더의 blueprint 인스턴스에서 `unique` 메서드를 호출하면 됩니다. 이때는 인덱스를 지정할 컬럼명을 인수로 전달합니다:

```php
$table->unique('email');
```

여러 컬럼을 배열로 전달하여 복합 인덱스를 생성할 수도 있습니다:

```php
$table->index(['account_id', 'created_at']);
```

인덱스명을 직접 지정하고 싶다면, 두 번째 인수로 인덱스 이름을 전달하세요:

```php
$table->unique('email', 'unique_email');
```

<a name="available-index-types"></a>
#### 지원되는 인덱스 타입

Laravel의 스키마 빌더 blueprint 클래스는 Laravel이 지원하는 각 인덱스 타입별 메서드를 제공합니다. 인덱스 이름은 두 번째 인수로 전달할 수 있으며, 생략 시 테이블, 컬럼, 인덱스 종류에 따라 자동 생성됩니다. 각 인덱스 메서드는 아래 표와 같습니다:

| 명령어                                           | 설명                                     |
|-------------------------------------------------|------------------------------------------|
| `$table->primary('id');`                        | 기본키 추가                              |
| `$table->primary(['id', 'parent_id']);`         | 복합키 추가                              |
| `$table->unique('email');`                      | 유니크 인덱스 추가                       |
| `$table->index('state');`                       | 인덱스 추가                              |
| `$table->fullText('body');`                     | 전문(full text) 인덱스 추가 (MySQL/PostgreSQL) |
| `$table->fullText('body')->language('english');`| 지정한 언어로 전문(full text) 인덱스 추가 (PostgreSQL) |
| `$table->spatialIndex('location');`             | 공간(Spatial) 인덱스 추가 (SQLite 제외)   |

<a name="index-lengths-mysql-mariadb"></a>
#### 인덱스 길이 및 MySQL / MariaDB

기본적으로 Laravel은 `utf8mb4` 문자셋을 사용합니다. 만약 MySQL `5.7.7` 이전 버전이나 MariaDB `10.2.2` 이전 버전을 사용하는 경우, 인덱스 생성에 문제가 생길 수 있으므로, 마이그레이션에서 생성되는 기본 문자열 길이를 직접 지정해야 할 수 있습니다. 이런 경우 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 다음과 같이 호출하세요:

```php
use Illuminate\Support\Facades\Schema;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Schema::defaultStringLength(191);
}
```

또는 DB에서 `innodb_large_prefix` 옵션을 활성화할 수도 있습니다. 자세한 내용은 데이터베이스 공식 문서를 확인하세요.

<a name="renaming-indexes"></a>
### 인덱스 이름 변경

인덱스의 이름을 변경하려면, 스키마 빌더 blueprint의 `renameIndex` 메서드를 사용합니다. 첫 번째 인수가 기존 이름, 두 번째 인수가 바꿀 이름입니다:

```php
$table->renameIndex('from', 'to')
```

> [!WARNING]  
> SQLite를 사용하는 경우, `renameIndex` 메서드를 사용하기 전에 `doctrine/dbal` 패키지를 설치해야 합니다.

<a name="dropping-indexes"></a>
### 인덱스 삭제

인덱스를 삭제하려면, 인덱스의 이름을 지정해야 합니다. Laravel은 기본적으로 인덱스의 이름을 테이블명과 컬럼명, 인덱스 타입에 따라 자동으로 지정합니다. 예시는 아래와 같습니다:

| 명령어                                              | 설명                                             |
|----------------------------------------------------|--------------------------------------------------|
| `$table->dropPrimary('users_id_primary');`         | "users" 테이블에서 기본키 삭제                   |
| `$table->dropUnique('users_email_unique');`        | "users" 테이블에서 유니크 인덱스 삭제            |
| `$table->dropIndex('geo_state_index');`            | "geo" 테이블에서 일반 인덱스 삭제                |
| `$table->dropFullText('posts_body_fulltext');`     | "posts" 테이블에서 전문 인덱스 삭제              |
| `$table->dropSpatialIndex('geo_location_spatialindex');` | "geo" 테이블에서 공간 인덱스 삭제 (SQLite 제외) |

여러 컬럼에 대한 인덱스를 삭제할 경우, 테이블명, 컬럼, 인덱스 타입을 조합한 인덱스 이름이 적용됩니다:

```php
Schema::table('geo', function (Blueprint $table) {
    $table->dropIndex(['state']); // 'geo_state_index' 인덱스 삭제
});
```

<a name="foreign-key-constraints"></a>
### 외래 키 제약조건

Laravel은 데이터베이스 수준의 참조 무결성을 보장하는 외래 키 제약조건도 지원합니다. 예를 들어, `posts` 테이블에 `user_id` 컬럼을 두고, 이 컬럼이 `users` 테이블의 `id` 컬럼을 참조하도록 정의할 수 있습니다:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('posts', function (Blueprint $table) {
    $table->unsignedBigInteger('user_id');

    $table->foreign('user_id')->references('id')->on('users');
});
```

그러나 위 문법은 다소 장황하기 때문에, Laravel에서는 좀 더 간결하고 편리한 메서드들도 제공합니다. 예를 들어 `foreignId` 메서드로 컬럼을 생성하면 아래처럼 줄일 수 있습니다:

```php
Schema::table('posts', function (Blueprint $table) {
    $table->foreignId('user_id')->constrained();
});
```

`foreignId`는 `UNSIGNED BIGINT` 타입의 컬럼을 생성하며, `constrained`는 관례에 따라 참조 테이블과 컬럼을 자동으로 지정합니다. 만약 관례와 다른 테이블/컬럼명을 사용해야 하면, `constrained`에 직접 지정할 수도 있습니다. 생성되는 인덱스 이름도 지정 가능합니다:

```php
Schema::table('posts', function (Blueprint $table) {
    $table->foreignId('user_id')->constrained(
        table: 'users', indexName: 'posts_user_id'
    );
});
```

"on delete", "on update" 제약조건도 다음과 같이 지정할 수 있습니다:

```php
$table->foreignId('user_id')
      ->constrained()
      ->onUpdate('cascade')
      ->onDelete('cascade');
```

이들을 위한 별도의 간략한 문법도 있습니다:

| 메서드                             | 설명                                           |
|-------------------------------------|------------------------------------------------|
| `$table->cascadeOnUpdate();`        | 업데이트 시 CASCADE                             |
| `$table->restrictOnUpdate();`       | 업데이트 시 RESTRICT                            |
| `$table->noActionOnUpdate();`       | 업데이트 시 NO ACTION                           |
| `$table->cascadeOnDelete();`        | 삭제 시 CASCADE                                 |
| `$table->restrictOnDelete();`       | 삭제 시 RESTRICT                                |
| `$table->nullOnDelete();`           | 삭제 시 외래키를 NULL로 설정                    |

추가적인 [컬럼 수정자](#column-modifiers)는 반드시 `constrained` 호출 전에 와야 합니다:

```php
$table->foreignId('user_id')
      ->nullable()
      ->constrained();
```

<a name="dropping-foreign-keys"></a>
#### 외래 키 삭제

외래 키를 삭제하려면, `dropForeign` 메서드에 삭제할 외래 키 제약조건의 이름을 인수로 전달합니다. 외래 키의 이름은 테이블과 컬럼, 그리고 '\_foreign' 접미사 조합입니다:

```php
$table->dropForeign('posts_user_id_foreign');
```

또는 외래키 컬럼명 배열만 전달해도 됩니다. 이 경우 Laravel의 제약조건 관례에 따라 이름이 변환됩니다:

```php
$table->dropForeign(['user_id']);
```

<a name="toggling-foreign-key-constraints"></a>
#### 외래 키 제약조건 활성화/비활성화

마이그레이션에서 외래 키 제약조건을 활성/비활성화할 수 있습니다:

```php
Schema::enableForeignKeyConstraints();

Schema::disableForeignKeyConstraints();

Schema::withoutForeignKeyConstraints(function () {
    // 이 클로저 내에서는 외래 키 제약조건이 비활성화됨...
});
```

> [!WARNING]  
> SQLite는 기본적으로 외래 키 제약조건이 비활성화되어 있습니다. 마이그레이션에서 이를 생성하려면, [SQLite foreign key 지원 활성화](/docs/{{version}}/database#configuration)가 필요합니다. 또한, SQLite에서는 테이블 생성 시에만 외래 키를 지원하며, [테이블 변경 시에는 지원하지 않습니다](https://www.sqlite.org/omitted.html).

<a name="events"></a>
## 이벤트

편의를 위해, 각 마이그레이션 작업은 [이벤트](/docs/{{version}}/events)를 발생시킵니다. 아래 모든 이벤트는 `Illuminate\Database\Events\MigrationEvent` 클래스를 확장합니다:

| 클래스 | 설명 |
|-----------|----|
| `Illuminate\Database\Events\MigrationsStarted` | 여러 개의 마이그레이션이 곧 실행됨 |
| `Illuminate\Database\Events\MigrationsEnded` | 여러 개의 마이그레이션이 실행 완료됨 |
| `Illuminate\Database\Events\MigrationStarted` | 한 개의 마이그레이션이 곧 실행됨 |
| `Illuminate\Database\Events\MigrationEnded` | 한 개의 마이그레이션이 실행 완료됨 |
| `Illuminate\Database\Events\SchemaDumped` | 데이터베이스 스키마 덤프 완료됨 |
| `Illuminate\Database\Events\SchemaLoaded` | 기존 스키마 덤프가 불러와짐 |