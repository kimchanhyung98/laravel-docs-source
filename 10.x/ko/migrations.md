# 데이터베이스: 마이그레이션 (Database: Migrations)

- [소개](#introduction)
- [마이그레이션 생성하기](#generating-migrations)
    - [마이그레이션 스쿼싱](#squashing-migrations)
- [마이그레이션 구조](#migration-structure)
- [마이그레이션 실행하기](#running-migrations)
    - [마이그레이션 롤백하기](#rolling-back-migrations)
- [테이블](#tables)
    - [테이블 생성하기](#creating-tables)
    - [테이블 업데이트하기](#updating-tables)
    - [테이블 이름 변경 / 삭제하기](#renaming-and-dropping-tables)
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

마이그레이션은 데이터베이스 버전 관리와 같아서, 팀이 애플리케이션의 데이터베이스 스키마 정의를 명확하게 작성하고 공유할 수 있게 해줍니다. 소스 컨트롤에서 변경 사항을 받고 나서 동료에게 로컬 데이터베이스에 컬럼을 수동으로 추가하라고 요청했던 경험이 있다면, 바로 마이그레이션이 해결하는 문제를 겪은 것입니다.

Laravel의 `Schema` [파사드](/docs/10.x/facades)는 Laravel이 지원하는 모든 데이터베이스 시스템에서 테이블 생성과 조작을 데이터베이스 독립적으로 지원합니다. 보통 마이그레이션은 이 파사드를 통해 데이터베이스 테이블과 컬럼을 생성하거나 수정합니다.

<a name="generating-migrations"></a>
## 마이그레이션 생성하기

`make:migration` [Artisan 명령어](/docs/10.x/artisan)를 사용하여 마이그레이션을 생성할 수 있습니다. 생성된 마이그레이션 파일은 `database/migrations` 디렉터리에 저장되며, 파일명에 포함된 타임스탬프를 통해 Laravel은 마이그레이션 실행 순서를 판단합니다:

```shell
php artisan make:migration create_flights_table
```

Laravel은 마이그레이션 이름으로부터 테이블 이름과 새 테이블을 생성하는지 여부를 추측하려 시도하며, 테이블 이름을 알아내면 해당 이름을 바탕으로 생성된 마이그레이션 파일을 미리 채워줍니다. 그렇지 않으면 마이그레이션 파일 안에서 직접 테이블 이름을 지정하면 됩니다.

마이그레이션 생성 경로를 직접 지정하고 싶으면, `make:migration` 명령어 실행 시 `--path` 옵션을 사용할 수 있습니다. 지정하는 경로는 애플리케이션의 기본 경로에서 상대적이어야 합니다.

> [!NOTE]  
> 마이그레이션 스텁은 [스텁 퍼블리싱](/docs/10.x/artisan#stub-customization) 기능을 통해 맞춤형으로 변경할 수 있습니다.

<a name="squashing-migrations"></a>
### 마이그레이션 스쿼싱

애플리케이션 개발이 진행되면서 점점 많은 수의 마이그레이션이 쌓일 수 있습니다. 이로 인해 `database/migrations` 폴더가 수백 개 파일로 비대해질 수 있는데, 원한다면 이 마이그레이션들을 하나의 SQL 파일로 "스쿼싱"할 수 있습니다. 시작하려면 `schema:dump` 명령어를 실행하세요:

```shell
php artisan schema:dump

# 현재 데이터베이스 스키마를 덤프하고 기존 마이그레이션은 모두 정리하기…
php artisan schema:dump --prune
```

이 명령을 실행하면, Laravel은 데이터베이스 연결 이름에 따른 스키마 파일을 `database/schema` 디렉터리에 생성합니다. 이후 마이그레이션을 시도할 때, 이전에 실행된 마이그레이션이 없다면 먼저 이 스키마 파일 내 SQL 구문들을 실행하고, 스키마 덤프에 속하지 않은 나머지 마이그레이션들을 차례로 실행합니다.

로컬 개발 시 주로 사용하는 데이터베이스 연결과 애플리케이션 테스트에서 사용하는 데이터베이스 연결이 다를 경우, 테스트를 위해 반드시 테스트용 연결에 대해서도 스키마 덤프 파일을 생성해 두는 것이 좋습니다:

```shell
php artisan schema:dump
php artisan schema:dump --database=testing --prune
```

스키마 덤프 파일은 새 팀원이 빠르게 애플리케이션 초기 데이터베이스 구조를 만들 수 있도록 소스 컨트롤에 커밋하는 것이 좋습니다.

> [!WARNING]  
> 마이그레이션 스쿼싱 기능은 MySQL, PostgreSQL, SQLite 데이터베이스에서만 지원하며, 데이터베이스의 커맨드라인 클라이언트를 활용합니다.

<a name="migration-structure"></a>
## 마이그레이션 구조

마이그레이션 클래스는 두 개의 메서드 `up`과 `down`을 포함합니다. `up` 메서드는 데이터베이스에 새 테이블, 컬럼 또는 인덱스를 추가할 때 사용하며, `down` 메서드는 `up`에서 수행한 작업을 되돌리는 역할을 합니다.

이 두 메서드 안에서 Laravel 스키마 빌더를 사용해 표현식으로 테이블을 생성·수정할 수 있습니다. `Schema` 빌더가 제공하는 모든 메서드는 [테이블 생성하기](#creating-tables)에서 확인할 수 있습니다. 다음 예시는 `flights` 테이블을 생성하는 마이그레이션입니다:

```
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * 마이그레이션 실행
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
     * 마이그레이션 되돌리기
     */
    public function down(): void
    {
        Schema::drop('flights');
    }
};
```

<a name="setting-the-migration-connection"></a>
#### 마이그레이션 연결 설정

기본 데이터베이스 연결 이외의 연결을 사용하는 마이그레이션이라면, `$connection` 속성을 명시해야 합니다:

```
/**
 * 이 마이그레이션이 사용할 데이터베이스 연결명.
 *
 * @var string
 */
protected $connection = 'pgsql';

/**
 * 마이그레이션 실행
 */
public function up(): void
{
    // ...
}
```

<a name="running-migrations"></a>
## 마이그레이션 실행하기

모든 미반영 마이그레이션을 실행하려면 다음 `migrate` Artisan 명령어를 사용하세요:

```shell
php artisan migrate
```

지금까지 실행된 마이그레이션 상태를 확인하려면 `migrate:status` 명령어를 사용합니다:

```shell
php artisan migrate:status
```

마이그레이션이 실행할 SQL 문만 미리 보고 싶으면 `--pretend` 플래그를 붙여 실행합니다:

```shell
php artisan migrate --pretend
```

#### 마이그레이션 실행 동시성 차단

여러 서버에 애플리케이션을 배포하고 함께 마이그레이션을 실행한다면, 동시에 두 서버가 데이터베이스 마이그레이션을 수행하지 않도록 주의해야 합니다. 이를 위해 `migrate` 명령어에 `--isolated` 옵션을 사용할 수 있습니다.

이 옵션을 사용하면 Laravel이 캐시 드라이버를 통해 원자적 락을 획득하여 마이그레이션 실행 전락을 잠그며, 락이 걸려있는 동안 다른 시도는 실행되지 않지만 성공적인 종료 코드로 반환합니다:

```shell
php artisan migrate --isolated
```

> [!WARNING]  
> 이 기능을 이용하려면 기본 캐시 드라이버가 `memcached`, `redis`, `dynamodb`, `database`, `file`, 또는 `array`여야 하며, 모든 서버가 같은 중앙 캐시 서버와 통신해야 합니다.

<a name="forcing-migrations-to-run-in-production"></a>
#### 운영 환경에서 강제 마이그레이션 실행하기

데이터 손실 가능성이 있는 파괴적 마이그레이션 작업에 대해 운영 데이터베이스에서 실행 시, 확인 메시지가 나타납니다. 이 메시지를 건너뛰고 바로 실행하려면 `--force` 플래그를 붙여 실행하세요:

```shell
php artisan migrate --force
```

<a name="rolling-back-migrations"></a>
### 마이그레이션 롤백하기

가장 최근 마이그레이션 배치를 되돌리려면 `rollback` Artisan 명령어를 사용합니다. 이는 여러 마이그레이션 파일로 구성된 마지막 "배치" 전체를 롤백합니다:

```shell
php artisan migrate:rollback
```

롤백할 마이그레이션 개수를 제한하려면 `--step` 옵션을 사용합니다. 예를 들어 마지막 5개의 마이그레이션만 롤백하려면:

```shell
php artisan migrate:rollback --step=5
```

특정 배치 단위로 롤백하려면 `--batch` 옵션을 사용하세요. 배치 값은 `migrations` 테이블의 배치 컬럼과 대응합니다. 예를 들어, 3번째 배치 마이그레이션 전체를 롤백:

```shell
php artisan migrate:rollback --batch=3
```

실제로 롤백하지 않고 실행될 SQL만 보고 싶으면 `--pretend` 플래그를 사용합니다:

```shell
php artisan migrate:rollback --pretend
```

모든 마이그레이션을 롤백하려면 `migrate:reset` 명령어를 실행합니다:

```shell
php artisan migrate:reset
```

<a name="roll-back-migrate-using-a-single-command"></a>
#### 롤백 후 재실행하기 (한 단계 명령어)

`migrate:refresh` 명령은 모든 마이그레이션을 롤백한 뒤 다시 실행합니다. 데이터베이스를 전면 재구성할 때 유용합니다:

```shell
php artisan migrate:refresh

# 데이터베이스를 초기화하고 시더도 실행...
php artisan migrate:refresh --seed
```

롤백 및 재실행할 마이그레이션 개수를 제한하려면 `--step` 옵션을 전달합니다. 예: 최근 5개 롤백 후 재실행

```shell
php artisan migrate:refresh --step=5
```

<a name="drop-all-tables-migrate"></a>
#### 모든 테이블 삭제 후 마이그레이션 실행

`migrate:fresh` 명령은 데이터베이스 내 모든 테이블을 삭제하고 마이그레이션을 실행합니다:

```shell
php artisan migrate:fresh

php artisan migrate:fresh --seed
```

기본적으로 `migrate:fresh`는 기본 데이터베이스 연결의 테이블만 삭제합니다. 다른 연결을 대상으로 하려면 `--database` 옵션을 사용하세요. 데이터베이스 연결명은 `database` [설정파일](/docs/10.x/configuration)에 정의된 이름이어야 합니다:

```shell
php artisan migrate:fresh --database=admin
```

> [!WARNING]  
> `migrate:fresh` 명령은 프리픽스와 관계없이 모든 데이터베이스 테이블을 삭제하므로, 다른 애플리케이션과 공유하는 데이터베이스에 신중하게 사용해야 합니다.

<a name="tables"></a>
## 테이블

<a name="creating-tables"></a>
### 테이블 생성하기

새 테이블을 생성할 때는 `Schema` 파사드의 `create` 메서드를 사용합니다. 이 메서드는 두 인수를 받는데, 첫 번째는 테이블 이름, 두 번째는 새 테이블 구조 정의에 사용할 `Blueprint` 객체를 받는 클로저입니다:

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

테이블 생성 시 [컬럼 생성 메서드](#creating-columns) 중 원하는 것을 사용해 컬럼을 정의하면 됩니다.

<a name="determining-table-column-existence"></a>
#### 테이블 / 컬럼 존재 여부 확인

`hasTable` 및 `hasColumn` 메서드로 테이블이나 컬럼이 존재하는지 확인할 수 있습니다:

```
if (Schema::hasTable('users')) {
    // "users" 테이블 존재...
}

if (Schema::hasColumn('users', 'email')) {
    // "users" 테이블 존재하고, "email" 컬럼 존재...
}
```

<a name="database-connection-table-options"></a>
#### 데이터베이스 연결 및 테이블 옵션

기본 연결과 다른 데이터베이스 연결에 대해 스키마 작업을 수행하려면 `connection` 메서드를 사용하세요:

```
Schema::connection('sqlite')->create('users', function (Blueprint $table) {
    $table->id();
});
```

MySQL 사용 시, 테이블 저장 엔진을 지정하려면 `engine` 속성을 설정할 수 있습니다:

```
Schema::create('users', function (Blueprint $table) {
    $table->engine = 'InnoDB';

    // ...
});
```

MySQL 사용 시, 테이블의 문자셋과 콜레이션을 각각 `charset`, `collation` 속성으로 지정할 수 있습니다:

```
Schema::create('users', function (Blueprint $table) {
    $table->charset = 'utf8mb4';
    $table->collation = 'utf8mb4_unicode_ci';

    // ...
});
```

`temporary` 메서드를 호출하면 현재 데이터베이스 연결 세션에서만 보이고, 세션 종료 시 자동 삭제되는 임시 테이블로 생성됩니다:

```
Schema::create('calculations', function (Blueprint $table) {
    $table->temporary();

    // ...
});
```

테이블에 "댓글(comment)"을 추가하고 싶으면 `comment` 메서드를 호출하세요. 현재 MySQL과 Postgres만 지원합니다:

```
Schema::create('calculations', function (Blueprint $table) {
    $table->comment('Business calculations');

    // ...
});
```

<a name="updating-tables"></a>
### 테이블 업데이트하기

기존 테이블을 수정하려면 `Schema` 파사드의 `table` 메서드를 사용합니다. `create` 메서드와 마찬가지로 첫 인자는 테이블 이름, 두 번째는 `Blueprint` 객체를 받는 클로저입니다. 이 안에서 컬럼이나 인덱스를 추가할 수 있습니다:

```
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->integer('votes');
});
```

<a name="renaming-and-dropping-tables"></a>
### 테이블 이름 변경 / 삭제하기

기존 테이블 이름을 변경할 때는 `rename` 메서드를 사용합니다:

```
use Illuminate\Support\Facades\Schema;

Schema::rename($from, $to);
```

기존 테이블을 삭제할 때는 `drop` 또는 `dropIfExists` 메서드를 사용하세요:

```
Schema::drop('users');

Schema::dropIfExists('users');
```

<a name="renaming-tables-with-foreign-keys"></a>
#### 외래 키가 있는 테이블 이름 변경 시 주의

테이블 이름 변경 전, 해당 테이블의 외래 키 제약조건이 Laravel의 규칙 기반 이름이 아닌 명시적 이름으로 지정되어 있는지 확인하세요. 그렇지 않으면 외래 키 제약조건 이름이 이전 테이블 이름을 참조하게 됩니다.

<a name="columns"></a>
## 컬럼

<a name="creating-columns"></a>
### 컬럼 생성하기

기존 테이블을 수정하여 컬럼을 추가할 때도 `Schema` 파사드의 `table` 메서드를 사용합니다. 첫 인자는 테이블 이름, 두 번째는 컬럼을 추가할 때 사용할 `Blueprint` 객체를 받는 클로저입니다:

```
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->integer('votes');
});
```

<a name="available-column-types"></a>
### 사용 가능한 컬럼 타입

스키마 빌더의 Blueprint 클래스는 다양한 데이터베이스 컬럼 타입에 대응하는 메서드를 제공합니다. 주요 메서드는 아래와 같습니다:

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

아래에 각 컬럼 메서드의 간략 소개와 예시가 있습니다.

<a name="column-method-bigIncrements"></a>
#### `bigIncrements()`

`bigIncrements`는 자동증가하는 `UNSIGNED BIGINT` (기본키) 컬럼을 생성합니다:

```
$table->bigIncrements('id');
```

<a name="column-method-bigInteger"></a>
#### `bigInteger()`

`bigInteger`는 `BIGINT` 타입 컬럼을 생성합니다:

```
$table->bigInteger('votes');
```

<a name="column-method-binary"></a>
#### `binary()`

`binary`는 `BLOB` 타입 컬럼을 생성합니다:

```
$table->binary('photo');
```

<a name="column-method-boolean"></a>
#### `boolean()`

`boolean`은 `BOOLEAN` 타입 컬럼을 생성합니다:

```
$table->boolean('confirmed');
```

<a name="column-method-char"></a>
#### `char()`

`char`는 지정한 길이의 `CHAR` 타입 컬럼을 생성합니다:

```
$table->char('name', 100);
```

<a name="column-method-dateTimeTz"></a>
#### `dateTimeTz()`

`dateTimeTz`는 타임존이 포함된 `DATETIME` 타입 컬럼을 생성하며, 정밀도(소수 자릿수)를 선택적으로 지정할 수 있습니다:

```
$table->dateTimeTz('created_at', $precision = 0);
```

<a name="column-method-dateTime"></a>
#### `dateTime()`

`dateTime`은 `DATETIME` 타입 컬럼을 생성합니다. 정밀도(소수 자릿수)를 지정할 수 있습니다:

```
$table->dateTime('created_at', $precision = 0);
```

<a name="column-method-date"></a>
#### `date()`

`date`는 `DATE` 타입 컬럼을 생성합니다:

```
$table->date('created_at');
```

<a name="column-method-decimal"></a>
#### `decimal()`

`decimal`은 지정한 정밀도(전체 자릿수)와 소수 자릿수를 가진 `DECIMAL` 타입 컬럼을 생성합니다:

```
$table->decimal('amount', $precision = 8, $scale = 2);
```

<a name="column-method-double"></a>
#### `double()`

`double`은 지정한 정밀도와 소수 자릿수를 갖는 `DOUBLE` 타입 컬럼을 생성합니다:

```
$table->double('amount', 8, 2);
```

<a name="column-method-enum"></a>
#### `enum()`

`enum`은 지정한 값 리스트를 가지는 `ENUM` 타입 컬럼을 생성합니다:

```
$table->enum('difficulty', ['easy', 'hard']);
```

<a name="column-method-float"></a>
#### `float()`

`float`은 지정한 정밀도와 소수 자릿수를 가진 `FLOAT` 타입 컬럼을 생성합니다:

```
$table->float('amount', 8, 2);
```

<a name="column-method-foreignId"></a>
#### `foreignId()`

`foreignId`는 `UNSIGNED BIGINT` 컬럼을 생성합니다:

```
$table->foreignId('user_id');
```

<a name="column-method-foreignIdFor"></a>
#### `foreignIdFor()`

`foreignIdFor`는 주어진 모델 클래스에 맞는 `{column}_id` 컬럼을 생성합니다. 컬럼 타입은 모델의 키 타입에 따라 `UNSIGNED BIGINT`, `CHAR(36)`, 또는 `CHAR(26)`입니다:

```
$table->foreignIdFor(User::class);
```

<a name="column-method-foreignUlid"></a>
#### `foreignUlid()`

`foreignUlid`는 `ULID` 타입 컬럼을 만듭니다:

```
$table->foreignUlid('user_id');
```

<a name="column-method-foreignUuid"></a>
#### `foreignUuid()`

`foreignUuid`는 `UUID` 타입 컬럼을 생성합니다:

```
$table->foreignUuid('user_id');
```

<a name="column-method-geometryCollection"></a>
#### `geometryCollection()`

`geometryCollection`은 `GEOMETRYCOLLECTION` 타입 컬럼을 생성합니다:

```
$table->geometryCollection('positions');
```

<a name="column-method-geometry"></a>
#### `geometry()`

`geometry`는 `GEOMETRY` 타입 컬럼을 생성합니다:

```
$table->geometry('positions');
```

<a name="column-method-id"></a>
#### `id()`

`id` 메서드는 `bigIncrements` 메서드의 별칭입니다. 기본적으로 `id` 컬럼을 생성하지만 이름을 지정할 수도 있습니다:

```
$table->id();
```

<a name="column-method-increments"></a>
#### `increments()`

`increments`는 자동증가하는 `UNSIGNED INTEGER` 타입 기본키 컬럼을 생성합니다:

```
$table->increments('id');
```

<a name="column-method-integer"></a>
#### `integer()`

`integer`는 `INTEGER` 타입 컬럼을 생성합니다:

```
$table->integer('votes');
```

<a name="column-method-ipAddress"></a>
#### `ipAddress()`

`ipAddress`는 `VARCHAR` 타입 컬럼을 생성합니다:

```
$table->ipAddress('visitor');
```

Postgres의 경우에는 `INET` 타입 컬럼으로 생성됩니다.

<a name="column-method-json"></a>
#### `json()`

`json`은 `JSON` 타입 컬럼을 생성합니다:

```
$table->json('options');
```

<a name="column-method-jsonb"></a>
#### `jsonb()`

`jsonb`는 `JSONB` 타입 컬럼을 생성합니다:

```
$table->jsonb('options');
```

<a name="column-method-lineString"></a>
#### `lineString()`

`lineString`은 `LINESTRING` 타입 컬럼을 생성합니다:

```
$table->lineString('positions');
```

<a name="column-method-longText"></a>
#### `longText()`

`longText`는 `LONGTEXT` 타입 컬럼을 생성합니다:

```
$table->longText('description');
```

<a name="column-method-macAddress"></a>
#### `macAddress()`

`macAddress`는 MAC 주소를 저장하기 위한 컬럼을 생성합니다. PostgreSQL 등 일부 데이터베이스는 전용 타입을 사용하고, 그렇지 않은 경우 문자열 타입을 사용합니다:

```
$table->macAddress('device');
```

<a name="column-method-mediumIncrements"></a>
#### `mediumIncrements()`

`mediumIncrements`는 자동증가하는 `UNSIGNED MEDIUMINT` 타입 기본키 컬럼을 생성합니다:

```
$table->mediumIncrements('id');
```

<a name="column-method-mediumInteger"></a>
#### `mediumInteger()`

`mediumInteger`는 `MEDIUMINT` 타입 컬럼을 생성합니다:

```
$table->mediumInteger('votes');
```

<a name="column-method-mediumText"></a>
#### `mediumText()`

`mediumText`는 `MEDIUMTEXT` 타입 컬럼을 생성합니다:

```
$table->mediumText('description');
```

<a name="column-method-morphs"></a>
#### `morphs()`

`morphs`는 다형성 [Eloquent 관계](/docs/10.x/eloquent-relationships)에 필요한 `{컬럼}_id` (타입은 모델 키에 따라 다름)와 `{컬럼}_type`(`VARCHAR`) 두 컬럼을 한 번에 생성해주는 편의 메서드입니다. 예를 들면 `taggable_id`와 `taggable_type` 컬럼이 생성됩니다:

```
$table->morphs('taggable');
```

<a name="column-method-multiLineString"></a>
#### `multiLineString()`

`multiLineString`은 `MULTILINESTRING` 타입 컬럼을 생성합니다:

```
$table->multiLineString('positions');
```

<a name="column-method-multiPoint"></a>
#### `multiPoint()`

`multiPoint`는 `MULTIPOINT` 타입 컬럼을 생성합니다:

```
$table->multiPoint('positions');
```

<a name="column-method-multiPolygon"></a>
#### `multiPolygon()`

`multiPolygon`은 `MULTIPOLYGON` 타입 컬럼을 생성합니다:

```
$table->multiPolygon('positions');
```

<a name="column-method-nullableTimestamps"></a>
#### `nullableTimestamps()`

`nullableTimestamps`는 [timestamps](#column-method-timestamps) 메서드의 별칭입니다:

```
$table->nullableTimestamps(0);
```

<a name="column-method-nullableMorphs"></a>
#### `nullableMorphs()`

`morphs` 메서드와 유사하지만 생성하는 컬럼들이 `NULL` 허용입니다:

```
$table->nullableMorphs('taggable');
```

<a name="column-method-nullableUlidMorphs"></a>
#### `nullableUlidMorphs()`

`ulidMorphs`와 비슷하나 생성 컬럼들이 `NULL` 허용입니다:

```
$table->nullableUlidMorphs('taggable');
```

<a name="column-method-nullableUuidMorphs"></a>
#### `nullableUuidMorphs()`

`uuidMorphs`와 비슷하지만 `NULL` 허용 컬럼이 생성됩니다:

```
$table->nullableUuidMorphs('taggable');
```

<a name="column-method-point"></a>
#### `point()`

`point`는 `POINT` 타입 컬럼을 생성합니다:

```
$table->point('position');
```

<a name="column-method-polygon"></a>
#### `polygon()`

`polygon`은 `POLYGON` 타입 컬럼을 생성합니다:

```
$table->polygon('position');
```

<a name="column-method-rememberToken"></a>
#### `rememberToken()`

`rememberToken`은 `VARCHAR(100)` 타입 컬럼을 생성하며, `NULL` 허용으로 현재 "remember me" [인증 토큰](/docs/10.x/authentication#remembering-users)을 저장하는 데 사용됩니다:

```
$table->rememberToken();
```

<a name="column-method-set"></a>
#### `set()`

`set`은 지정한 목록 내 값만 가질 수 있는 `SET` 타입 컬럼을 생성합니다:

```
$table->set('flavors', ['strawberry', 'vanilla']);
```

<a name="column-method-smallIncrements"></a>
#### `smallIncrements()`

`smallIncrements`는 자동증가하는 `UNSIGNED SMALLINT` 타입 기본키 컬럼을 생성합니다:

```
$table->smallIncrements('id');
```

<a name="column-method-smallInteger"></a>
#### `smallInteger()`

`smallInteger`는 `SMALLINT` 타입 컬럼을 생성합니다:

```
$table->smallInteger('votes');
```

<a name="column-method-softDeletesTz"></a>
#### `softDeletesTz()`

`softDeletesTz`는 `deleted_at` 이라는 이름(기본값)의 `TIMESTAMP` 타임존 포함 컬럼을 `NULL` 허용 상태로 추가합니다. Eloquent의 "soft delete" 기능에 필요한 컬럼입니다:

```
$table->softDeletesTz($column = 'deleted_at', $precision = 0);
```

<a name="column-method-softDeletes"></a>
#### `softDeletes()`

`softDeletes`는 `deleted_at` `TIMESTAMP` 컬럼을 `NULL` 허용 상태로 추가합니다. 타임존은 포함하지 않습니다. Eloquent의 "soft delete" 기능에 필요한 컬럼입니다:

```
$table->softDeletes($column = 'deleted_at', $precision = 0);
```

<a name="column-method-string"></a>
#### `string()`

`string`은 지정한 길이의 `VARCHAR` 타입 컬럼을 생성합니다:

```
$table->string('name', 100);
```

<a name="column-method-text"></a>
#### `text()`

`text`는 `TEXT` 타입 컬럼을 생성합니다:

```
$table->text('description');
```

<a name="column-method-timeTz"></a>
#### `timeTz()`

`timeTz`는 타임존 포함 `TIME` 타입 컬럼을 생성하며, 정밀도를 지정할 수 있습니다:

```
$table->timeTz('sunrise', $precision = 0);
```

<a name="column-method-time"></a>
#### `time()`

`time`은 `TIME` 타입 컬럼을 생성하며, 정밀도를 지정할 수 있습니다:

```
$table->time('sunrise', $precision = 0);
```

<a name="column-method-timestampTz"></a>
#### `timestampTz()`

`timestampTz`는 타임존 포함 `TIMESTAMP` 타입 컬럼을 생성하며, 정밀도를 지정할 수 있습니다:

```
$table->timestampTz('added_at', $precision = 0);
```

<a name="column-method-timestamp"></a>
#### `timestamp()`

`timestamp`는 `TIMESTAMP` 타입 컬럼을 생성하며, 정밀도를 지정할 수 있습니다:

```
$table->timestamp('added_at', $precision = 0);
```

<a name="column-method-timestampsTz"></a>
#### `timestampsTz()`

`timestampsTz`는 `created_at`과 `updated_at` 타임존 포함 `TIMESTAMP` 타입 컬럼 두 개를 생성하며, 정밀도를 지정할 수 있습니다:

```
$table->timestampsTz($precision = 0);
```

<a name="column-method-timestamps"></a>
#### `timestamps()`

`timestamps`는 `created_at`과 `updated_at` `TIMESTAMP` 타입 컬럼 두 개를 생성합니다. 정밀도 지정 가능:

```
$table->timestamps($precision = 0);
```

<a name="column-method-tinyIncrements"></a>
#### `tinyIncrements()`

`tinyIncrements`는 자동증가하는 `UNSIGNED TINYINT` 타입 기본키 컬럼을 생성합니다:

```
$table->tinyIncrements('id');
```

<a name="column-method-tinyInteger"></a>
#### `tinyInteger()`

`tinyInteger`는 `TINYINT` 타입 컬럼을 생성합니다:

```
$table->tinyInteger('votes');
```

<a name="column-method-tinyText"></a>
#### `tinyText()`

`tinyText`는 `TINYTEXT` 타입 컬럼을 생성합니다:

```
$table->tinyText('notes');
```

<a name="column-method-unsignedBigInteger"></a>
#### `unsignedBigInteger()`

`unsignedBigInteger`는 `UNSIGNED BIGINT` 타입 컬럼을 생성합니다:

```
$table->unsignedBigInteger('votes');
```

<a name="column-method-unsignedDecimal"></a>
#### `unsignedDecimal()`

`unsignedDecimal`은 부호 없는 `DECIMAL` 타입 컬럼을 생성하며, 정밀도와 소수 자릿수를 지정할 수 있습니다:

```
$table->unsignedDecimal('amount', $precision = 8, $scale = 2);
```

<a name="column-method-unsignedInteger"></a>
#### `unsignedInteger()`

`unsignedInteger`는 `UNSIGNED INTEGER` 타입 컬럼을 생성합니다:

```
$table->unsignedInteger('votes');
```

<a name="column-method-unsignedMediumInteger"></a>
#### `unsignedMediumInteger()`

`unsignedMediumInteger`는 `UNSIGNED MEDIUMINT` 타입 컬럼을 생성합니다:

```
$table->unsignedMediumInteger('votes');
```

<a name="column-method-unsignedSmallInteger"></a>
#### `unsignedSmallInteger()`

`unsignedSmallInteger`는 `UNSIGNED SMALLINT` 타입 컬럼을 생성합니다:

```
$table->unsignedSmallInteger('votes');
```

<a name="column-method-unsignedTinyInteger"></a>
#### `unsignedTinyInteger()`

`unsignedTinyInteger`는 `UNSIGNED TINYINT` 타입 컬럼을 생성합니다:

```
$table->unsignedTinyInteger('votes');
```

<a name="column-method-ulidMorphs"></a>
#### `ulidMorphs()`

`ulidMorphs`는 `{컬럼}_id` (`CHAR(26)`)와 `{컬럼}_type` (`VARCHAR`) 컬럼 두 개를 추가하는 편의 메서드입니다. ULID 식별자를 사용하는 다형성 Eloquent 관계에 사용합니다:

```
$table->ulidMorphs('taggable');
```

<a name="column-method-uuidMorphs"></a>
#### `uuidMorphs()`

`uuidMorphs`는 `{컬럼}_id` (`CHAR(36)`)와 `{컬럼}_type` 컬럼 두 개를 추가합니다. UUID 식별자를 사용하는 다형성 관계에 적합합니다:

```
$table->uuidMorphs('taggable');
```

<a name="column-method-ulid"></a>
#### `ulid()`

`ulid`는 `ULID` 타입 컬럼을 생성합니다:

```
$table->ulid('id');
```

<a name="column-method-uuid"></a>
#### `uuid()`

`uuid`는 `UUID` 타입 컬럼을 생성합니다:

```
$table->uuid('id');
```

<a name="column-method-year"></a>
#### `year()`

`year`는 `YEAR` 타입 컬럼을 생성합니다:

```
$table->year('birth_year');
```

<a name="column-modifiers"></a>
### 컬럼 수정자

위에서 소개한 컬럼 타입 외에도 컬럼에 여러 수정자를 붙일 수 있습니다. 예를 들어 컬럼을 "nullable"로 만들려면 `nullable` 메서드를 사용합니다:

```
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->string('email')->nullable();
});
```

아래 표는 사용 가능한 컬럼 수정자 목록이며, [인덱스 수정자](#creating-indexes)는 포함하지 않습니다:

| 수정자                         | 설명                                                             |
|------------------------------|----------------------------------------------------------------|
| `->after('column')`           | MySQL에서 컬럼을 다른 컬럼 뒤에 위치시킵니다.                          |
| `->autoIncrement()`           | 컬럼을 자동 증가 (기본키)로 설정합니다.                                  |
| `->charset('utf8mb4')`        | MySQL에서 컬럼 문자셋을 지정합니다.                                     |
| `->collation('utf8mb4_unicode_ci')` | MySQL/PostgreSQL/SQL Server에서 컬럼 콜레이션을 지정합니다.           |
| `->comment('my comment')`     | MySQL/PostgreSQL에서 컬럼에 댓글을 추가합니다.                           |
| `->default($value)`           | 컬럼의 기본값을 지정합니다.                                               |
| `->first()`                   | MySQL에서 컬럼을 테이블의 첫 번째 컬럼으로 위치시킵니다.                   |
| `->from($integer)`            | MySQL/PostgreSQL에서 자동증가 컬럼 시작 값을 지정합니다.                   |
| `->invisible()`               | MySQL에서 컬럼을 `SELECT *` 쿼리에 보이지 않게 만듭니다.                 |
| `->nullable($value = true)`   | 컬럼에 NULL 값을 허용합니다.                                              |
| `->storedAs($expression)`     | MySQL/PostgreSQL에서 저장된 계산 컬럼을 생성합니다.                       |
| `->unsigned()`                | MySQL에서 정수형 컬럼을 부호 없는 값으로 설정합니다.                       |
| `->useCurrent()`              | `TIMESTAMP` 컬럼 기본값을 `CURRENT_TIMESTAMP`로 설정합니다.             |
| `->useCurrentOnUpdate()`      | MySQL에서 레코드 업데이트 시 `CURRENT_TIMESTAMP`를 적용합니다.           |
| `->virtualAs($expression)`   | MySQL/PostgreSQL/SQLite에서 가상 계산 컬럼을 생성합니다.                   |
| `->generatedAs($expression)` | PostgreSQL에서 지정 시퀀스 옵션을 가진 식별자 컬럼을 생성합니다.           |
| `->always()`                  | PostgreSQL에서 식별자 컬럼에 대해 시퀀스 값이 입력값보다 우선함을 지정합니다.  |
| `->isGeometry()`              | PostgreSQL에서 공간 컬럼 타입을 기본 공간(`geography`) 대신 `geometry`로 설정합니다. |

<a name="default-expressions"></a>
#### 기본값 표현식

`default` 수정자는 값이나 `Illuminate\Database\Query\Expression` 인스턴스를 허용합니다. Expression을 사용하면 Laravel이 값을 따옴표로 감싸는 것을 방지하고, 데이터베이스 전용 함수 등을 기본값으로 사용할 수 있습니다. JSON 컬럼에 기본값을 지정할 때 특히 유용합니다:

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
> 기본값 표현식 지원 여부는 데이터베이스 드라이버, 버전, 필드 타입에 따라 다르므로, 데이터베이스 공식 문서를 참고하세요.

<a name="column-order"></a>
#### 컬럼 순서

MySQL의 경우 `after` 메서드를 사용하여 컬럼이 기존 컬럼 뒤에 위치하도록 설정할 수 있습니다:

```
$table->after('password', function (Blueprint $table) {
    $table->string('address_line1');
    $table->string('address_line2');
    $table->string('city');
});
```

<a name="modifying-columns"></a>
### 컬럼 수정하기

`change` 메서드를 사용하여 기존 컬럼의 타입과 속성을 수정할 수 있습니다. 예를 들어 `name` 컬럼의 길이를 25에서 50으로 늘리고 싶다면 아래와 같이 작성하면 됩니다:

```
Schema::table('users', function (Blueprint $table) {
    $table->string('name', 50)->change();
});
```

컬럼 수정 시 유지하려는 모든 수정자를 명시적으로 적어야 하며 생략하면 해당 속성은 제거됩니다. 예를 들어 `unsigned`, `default`, `comment`를 유지하려면 아래처럼 작성해야 합니다:

```
Schema::table('users', function (Blueprint $table) {
    $table->integer('votes')->unsigned()->default(1)->comment('my comment')->change();
});
```

<a name="modifying-columns-on-sqlite"></a>
#### SQLite에서 컬럼 수정하기

SQLite 사용 시 컬럼 수정 전에 Composer를 통해 `doctrine/dbal` 패키지를 설치해야 합니다. 이 패키지는 현재 컬럼 상태를 파악하고 변경에 필요한 SQL을 생성하는 데 사용됩니다:

```
composer require doctrine/dbal
```

`timestamp` 메서드로 생성된 컬럼을 수정하려면 `config/database.php` 설정에 다음 내용을 추가해야 합니다:

```php
use Illuminate\Database\DBAL\TimestampType;

'dbal' => [
    'types' => [
        'timestamp' => TimestampType::class,
    ],
],
```

> [!WARNING]  
> `doctrine/dbal` 사용 시 수정 가능한 컬럼 타입은 다음과 같습니다: `bigInteger`, `binary`, `boolean`, `char`, `date`, `dateTime`, `dateTimeTz`, `decimal`, `double`, `integer`, `json`, `longText`, `mediumText`, `smallInteger`, `string`, `text`, `time`, `tinyText`, `unsignedBigInteger`, `unsignedInteger`, `unsignedSmallInteger`, `ulid`, `uuid`.

<a name="renaming-columns"></a>
### 컬럼 이름 변경하기

`renameColumn` 메서드를 사용해 컬럼명을 변경할 수 있습니다:

```
Schema::table('users', function (Blueprint $table) {
    $table->renameColumn('from', 'to');
});
```

<a name="renaming-columns-on-legacy-databases"></a>
#### 구버전 데이터베이스에서 컬럼 이름 변경하기

다음 버전보다 낮은 데이터베이스를 사용하는 경우 컬럼 이름 변경 전에 `doctrine/dbal` 패키지를 설치해야 합니다:

- MySQL < `8.0.3`
- MariaDB < `10.5.2`
- SQLite < `3.25.0`

<a name="dropping-columns"></a>
### 컬럼 삭제하기

`dropColumn` 메서드를 사용해 컬럼을 삭제할 수 있습니다:

```
Schema::table('users', function (Blueprint $table) {
    $table->dropColumn('votes');
});
```

여러 컬럼을 한번에 삭제하려면 배열로 전달하세요:

```
Schema::table('users', function (Blueprint $table) {
    $table->dropColumn(['votes', 'avatar', 'location']);
});
```

<a name="dropping-columns-on-legacy-databases"></a>
#### 구버전 데이터베이스에서 컬럼 삭제하기

SQLite 3.35.0 미만 버전 사용 시 컬럼 삭제 전에 `doctrine/dbal` 패키지 설치가 필요합니다. 다만 이 패키지를 통한 단일 마이그레이션 내 다중 컬럼 삭제 및 수정은 지원하지 않습니다.

<a name="available-command-aliases"></a>
#### 편리한 컬럼 삭제별칭

Laravel은 다음과 같이 자주 쓰이는 컬럼 삭제 메서드를 제공합니다:

| 명령어                            | 설명                             |
|--------------------------------|--------------------------------|
| `$table->dropMorphs('morphable');`      | `morphable_id`, `morphable_type` 컬럼 삭제 |
| `$table->dropRememberToken();`          | `remember_token` 컬럼 삭제           |
| `$table->dropSoftDeletes();`             | `deleted_at` 컬럼 삭제              |
| `$table->dropSoftDeletesTz();`           | `dropSoftDeletes()` 별칭               |
| `$table->dropTimestamps();`               | `created_at`, `updated_at` 컬럼 삭제   |
| `$table->dropTimestampsTz();`             | `dropTimestamps()` 별칭                |

<a name="indexes"></a>
## 인덱스

<a name="creating-indexes"></a>
### 인덱스 생성하기

Laravel 스키마 빌더는 여러 종류의 인덱스를 지원합니다. 예를 들어 `email` 컬럼을 생성할 때 값이 고유해야 한다면 `unique` 메서드를 체인으로 붙여 인덱스를 생성할 수 있습니다:

```
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->string('email')->unique();
});
```

또는 컬럼 정의 후 `unique` 메서드를 호출하여 인덱스를 만들 수도 있습니다. 이 방법은 인덱스를 생성할 컬럼명을 인수로 받습니다:

```
$table->unique('email');
```

복합 인덱스(복수 컬럼 대상)도 배열로 컬럼명을 전달하여 생성할 수 있습니다:

```
$table->index(['account_id', 'created_at']);
```

인덱스 생성 시 Laravel이 자동으로 이름을 만드나, 두 번째 인수로 직접 이름을 지정할 수도 있습니다:

```
$table->unique('email', 'unique_email');
```

<a name="available-index-types"></a>
#### 사용 가능한 인덱스 종류

아래 표는 Laravel 스키마 빌더가 제공하는 인덱스 생성 메서드와 설명입니다. 두 번째 인수로 인덱스 이름을 지정 가능하며, 미지정 시 기본 생성 규칙에 따라 이름이 결정됩니다:

| 명령어                          | 설명              |
|-------------------------------|-------------------|
| `$table->primary('id');`       | 기본키 추가         |
| `$table->primary(['id', 'parent_id']);` | 복합 기본키 추가      |
| `$table->unique('email');`     | 유니크 인덱스 추가     |
| `$table->index('state');`      | 일반 인덱스 추가      |
| `$table->fullText('body');`    | 전문 검색용 인덱스 추가 (MySQL/PostgreSQL) |
| `$table->fullText('body')->language('english');` | 지정 언어 전문 검색 인덱스 추가 (PostgreSQL) |
| `$table->spatialIndex('location');` | 공간 인덱스 추가 (SQLite 제외) |

<a name="index-lengths-mysql-mariadb"></a>
#### 인덱스 길이 및 MySQL / MariaDB

Laravel 기본 문자셋은 `utf8mb4`입니다. MySQL 5.7.7 이전 버전과 MariaDB 10.2.2 이전 버전에서는 마이그레이션 생성 시 기본 문자열 길이를 수동으로 지정해야 인덱스를 만들 수 있습니다. 이 경우 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 다음을 호출하세요:

```
use Illuminate\Support\Facades\Schema;

/**
 * 애플리케이션 부트스트랩
 */
public function boot(): void
{
    Schema::defaultStringLength(191);
}
```

또는 데이터베이스에서 `innodb_large_prefix` 옵션을 활성화하는 방법도 있습니다. 자세한 내용은 해당 데이터베이스 문서를 참고하세요.

<a name="renaming-indexes"></a>
### 인덱스 이름 변경하기

인덱스 이름을 변경하려면 `renameIndex` 메서드를 사용합니다. 첫 번째 인자에 현재 인덱스 이름, 두 번째 인자에 새 이름을 지정하세요:

```
$table->renameIndex('from', 'to');
```

> [!WARNING]  
> SQLite 사용 시 `renameIndex` 메서드 사용 전 `doctrine/dbal` 패키지를 설치해야 합니다.

<a name="dropping-indexes"></a>
### 인덱스 삭제하기

인덱스 삭제 시 인덱스 이름을 지정해야 합니다. Laravel은 인덱스를 테이블명, 컬럼명, 타입 이름으로 자동 생성하므로 아래 예시처럼 기본 이름 구조를 참고하세요:

| 명령어                                | 설명                                    |
|-------------------------------------|---------------------------------------|
| `$table->dropPrimary('users_id_primary');`        | "users" 테이블에서 기본키 삭제              |
| `$table->dropUnique('users_email_unique');`       | "users" 테이블에서 유니크 인덱스 삭제          |
| `$table->dropIndex('geo_state_index');`           | "geo" 테이블에서 일반 인덱스 삭제              |
| `$table->dropFullText('posts_body_fulltext');`    | "posts" 테이블에서 전문 검색 인덱스 삭제         |
| `$table->dropSpatialIndex('geo_location_spatialindex');` | "geo" 테이블에서 공간 인덱스 삭제 (SQLite 제외) |

배열로 컬럼명을 전달하면 Laravel이 인덱스 이름을 자동 생성해줍니다:

```
Schema::table('geo', function (Blueprint $table) {
    $table->dropIndex(['state']); // 'geo_state_index' 인덱스 삭제
});
```

<a name="foreign-key-constraints"></a>
### 외래 키 제약조건

Laravel은 데이터베이스 수준에서 참조 무결성을 강제하는 외래 키 제약조건 생성도 지원합니다. 예를 들어 `posts` 테이블에 `user_id` 컬럼을 만들어 `users` 테이블의 `id` 컬럼을 참조하도록 정의할 수 있습니다:

```
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('posts', function (Blueprint $table) {
    $table->unsignedBigInteger('user_id');

    $table->foreign('user_id')->references('id')->on('users');
});
```

이 문법이 다소 길기 때문에, Laravel에서는 컨벤션을 활용한 간결한 메서드도 제공합니다. `foreignId` 메서드를 쓰면 위 예시를 다음처럼 간소화할 수 있습니다:

```
Schema::table('posts', function (Blueprint $table) {
    $table->foreignId('user_id')->constrained();
});
```

`foreignId`는 `UNSIGNED BIGINT` 컬럼을 생성하고, `constrained`는 참조되는 테이블과 컬럼을 규칙에 맞게 추론합니다. 만약 테이블명이 규칙과 다르면 `constrained`에 직접 지정할 수 있습니다. 생성될 인덱스 이름도 지정 가능합니다:

```
Schema::table('posts', function (Blueprint $table) {
    $table->foreignId('user_id')->constrained(
        table: 'users', indexName: 'posts_user_id'
    );
});
```

또한 외래 키 제약조건의 삭제 및 갱신 시 동작도 지정할 수 있습니다:

```
$table->foreignId('user_id')
      ->constrained()
      ->onUpdate('cascade')
      ->onDelete('cascade');
```

대체로, 아래와 같은 메서드들도 제공됩니다:

| 메서드                      | 설명                         |
|--------------------------|------------------------------|
| `$table->cascadeOnUpdate();`  | 갱신 시 cascading 적용                  |
| `$table->restrictOnUpdate();` | 갱신 시 제한 적용                    |
| `$table->noActionOnUpdate();` | 갱신 시 아무 동작 안 함                 |
| `$table->cascadeOnDelete();`  | 삭제 시 cascading 적용                  |
| `$table->restrictOnDelete();` | 삭제 시 제한 적용                    |
| `$table->nullOnDelete();`     | 삭제 시 외래 키 컬럼값을 NULL로 설정        |

추가적인 [컬럼 수정자](#column-modifiers)은 `constrained` 호출 전에 붙여야 합니다:

```
$table->foreignId('user_id')
      ->nullable()
      ->constrained();
```

<a name="dropping-foreign-keys"></a>
#### 외래 키 삭제하기

외래 키를 삭제하려면 `dropForeign` 메서드를 사용하고 제약조건 이름을 인자로 넘겨야 합니다. 외래 키 제약조건 이름은 인덱스 이름과 동일하며, 보통 테이블명과 컬럼명 뒤에 `_foreign` 접미사가 붙습니다:

```
$table->dropForeign('posts_user_id_foreign');
```

또는 외래 키 컬럼명 배열을 넘기면 Laravel이 이름을 자동으로 만들어줍니다:

```
$table->dropForeign(['user_id']);
```

<a name="toggling-foreign-key-constraints"></a>
#### 외래 키 제약조건 활성화 / 비활성화

마이그레이션 안에서 외래 키 제약조건을 활성화하거나 비활성화하려면 다음 메서드를 사용합니다:

```
Schema::enableForeignKeyConstraints();

Schema::disableForeignKeyConstraints();

Schema::withoutForeignKeyConstraints(function () {
    // 이 클로저 내부는 외래 키 제약조건이 비활성화된 상태...
});
```

> [!WARNING]  
> SQLite는 기본적으로 외래 키 제약조건이 비활성화되어 있습니다. SQLite에서 마이그레이션 생성 시 외래 키를 만들려면 반드시 [외래 키 지원을 활성화](/docs/10.x/database#configuration)해야 하며, SQLite는 테이블 생성 시점에만 외래 키를 지원하고 테이블 변경 시에는 지원하지 않습니다(관련 링크: https://www.sqlite.org/omitted.html).

<a name="events"></a>
## 이벤트

편의를 위해 각 마이그레이션 작업은 [이벤트](/docs/10.x/events)를 발생시킵니다. 아래는 `Illuminate\Database\Events\MigrationEvent` 기본 클래스를 상속하는 이벤트 목록입니다:

| 클래스명                                    | 설명                          |
|---------------------------------------------|------------------------------|
| `Illuminate\Database\Events\MigrationsStarted` | 마이그레이션 배치 실행 직전          |
| `Illuminate\Database\Events\MigrationsEnded`   | 마이그레이션 배치 실행 완료 후         |
| `Illuminate\Database\Events\MigrationStarted`  | 개별 마이그레이션 실행 직전          |
| `Illuminate\Database\Events\MigrationEnded`    | 개별 마이그레이션 실행 완료 후         |
| `Illuminate\Database\Events\SchemaDumped`      | 데이터베이스 스키마 덤프 완료           |
| `Illuminate\Database\Events\SchemaLoaded`      | 기존 데이터베이스 스키마 덤프 로드 완료    |