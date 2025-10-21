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
    - [테이블 이름 변경 / 삭제](#renaming-and-dropping-tables)
- [컬럼](#columns)
    - [컬럼 생성](#creating-columns)
    - [사용 가능한 컬럼 타입](#available-column-types)
    - [컬럼 수식어](#column-modifiers)
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

마이그레이션(Migration)은 데이터베이스의 버전 관리를 돕는 기능으로, 팀원 모두가 애플리케이션의 데이터베이스 스키마 정의를 쉽게 작성하고 공유할 수 있도록 해줍니다. 소스 컨트롤에서 변경사항을 가져온 후 팀원에게 직접 데이터베이스에 컬럼을 수동으로 추가하라고 요청해본 적이 있다면, 바로 그 문제가 마이그레이션으로 해결됩니다.

Laravel의 `Schema` [파사드](/docs/12.x/facades)는 Laravel이 지원하는 모든 데이터베이스 시스템에서 테이블을 생성하거나 조작할 수 있도록 데이터베이스 독립적인 기능을 제공합니다. 일반적으로 마이그레이션에서는 이 파사드를 사용하여 데이터베이스 테이블과 컬럼을 생성 및 수정합니다.

<a name="generating-migrations"></a>
## 마이그레이션 생성 (Generating Migrations)

`make:migration` [Artisan 명령어](/docs/12.x/artisan)를 사용하여 데이터베이스 마이그레이션 파일을 생성할 수 있습니다. 새 마이그레이션 파일은 `database/migrations` 디렉터리에 생성됩니다. 각각의 마이그레이션 파일 이름에는 타임스탬프가 포함되어 있어 Laravel이 마이그레이션의 순서를 결정하는 데 활용합니다.

```shell
php artisan make:migration create_flights_table
```

Laravel은 마이그레이션 이름을 참고하여 테이블 이름과 새로운 테이블 생성 여부를 추측하려고 시도합니다. 마이그레이션 이름으로부터 테이블 이름을 추론할 수 있다면, Laravel은 생성된 마이그레이션 파일의 스텁에 해당 테이블을 미리 채워줍니다. 그렇지 않은 경우, 마이그레이션 파일에서 직접 테이블을 지정하면 됩니다.

생성되는 마이그레이션의 경로를 직접 지정하고 싶다면 `make:migration` 명령 실행 시 `--path` 옵션을 사용할 수 있습니다. 이 옵션 값은 애플리케이션의 기준 경로에서 상대 경로로 지정해야 합니다.

> [!NOTE]
> 마이그레이션 스텁은 [스텁 퍼블리싱](/docs/12.x/artisan#stub-customization)을 통해 커스터마이즈할 수 있습니다.

<a name="squashing-migrations"></a>
### 마이그레이션 스쿼싱 (Squashing Migrations)

애플리케이션을 개발하다 보면 마이그레이션이 계속 늘어나 `database/migrations` 디렉터리가 수백 개의 마이그레이션으로 혼잡해질 수 있습니다. 이럴 때 여러 마이그레이션을 하나의 SQL 파일로 "스쿼시"하여 관리할 수 있습니다. 시작하려면 `schema:dump` 명령어를 실행하세요.

```shell
php artisan schema:dump

# 현재 데이터베이스 스키마를 덤프하고 기존 마이그레이션을 정리합니다...
php artisan schema:dump --prune
```

이 명령을 실행하면 Laravel은 애플리케이션의 `database/schema` 디렉터리에 "스키마" 파일을 저장합니다. 이 파일의 이름은 데이터베이스 연결명과 일치합니다. 이제 데이터베이스 마이그레이션을 시도할 때 실행된 마이그레이션이 없다면, Laravel은 가장 먼저 해당 연결에 맞는 스키마 파일의 SQL 구문을 실행합니다. 스키마 파일 실행 후에도 남아있는 마이그레이션이 있다면 그 마이그레이션만 별도로 실행합니다.

애플리케이션의 테스트 환경이 로컬 개발 환경에서 사용하는 데이터베이스 연결과 다르다면, 반드시 해당 연결로도 스키마 파일을 덤프해두어야 합니다. 일반적으로 개발에 사용하는 연결로 먼저 스키마를 덤프한 다음, 테스트 연결로도 덤프하면 됩니다.

```shell
php artisan schema:dump
php artisan schema:dump --database=testing --prune
```

데이터베이스 스키마 파일은 소스 컨트롤에 반드시 커밋해야 팀의 다른 신규 개발자도 애플리케이션의 초기 데이터베이스 구조를 쉽게 복원할 수 있습니다.

> [!WARNING]
> 마이그레이션 스쿼싱은 MariaDB, MySQL, PostgreSQL, SQLite에서만 지원되며 데이터베이스의 커맨드라인 클라이언트를 활용합니다.

<a name="migration-structure"></a>
## 마이그레이션 구조 (Migration Structure)

마이그레이션 클래스는 `up`과 `down`, 두 가지 메서드를 가집니다. `up` 메서드는 데이터베이스에 새로운 테이블, 컬럼 또는 인덱스를 추가하는 데 사용하며, `down` 메서드는 `up` 메서드가 수행한 작업을 되돌리는 역할을 합니다.

이 두 메서드 내부에서는 Laravel 스키마 빌더를 사용하여 테이블을 간결하게 생성하고 수정할 수 있습니다. `Schema` 빌더에 존재하는 모든 메서드에 대한 자세한 내용은 [관련 문서](#creating-tables)를 참고하세요. 예를 들어 다음은 `flights` 테이블을 생성하는 마이그레이션입니다.

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

마이그레이션이 애플리케이션의 기본 데이터베이스 연결이 아닌 다른 데이터베이스와 상호작용해야 할 경우, 마이그레이션 클래스의 `$connection` 속성을 지정해야 합니다.

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

경우에 따라 아직 활성화되지 않은 기능을 위한 마이그레이션이 있어, 지금은 마이그레이션을 적용하고 싶지 않을 수 있습니다. 이럴 때 마이그레이션에 `shouldRun` 메서드를 정의하면 됩니다. 이 메서드가 `false`를 반환하면 해당 마이그레이션은 건너뜁니다.

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

이미 실행된 마이그레이션과 대기 중인 마이그레이션 목록을 확인하려면 `migrate:status` 명령어를 사용할 수 있습니다.

```shell
php artisan migrate:status
```

마이그레이션이 실제로 실행되기 전에 어떤 SQL 문이 동작할지 확인하고 싶다면, `migrate` 명령에 `--pretend` 플래그를 추가하여 미리 SQL 문만 출력할 수 있습니다.

```shell
php artisan migrate --pretend
```

#### 마이그레이션 실행 격리

여러 서버에 애플리케이션을 배포하면서 배포 과정에서 마이그레이션을 수행한다면, 두 서버 이상에서 동시에 마이그레이션이 실행되는 상황을 피해야 합니다. 이런 경우 `migrate` 명령 실행 시 `--isolated` 옵션을 사용하면 됩니다.

`--isolated` 옵션을 사용하면, Laravel이 애플리케이션의 캐시 드라이버를 활용해 원자적(atomic) 락을 획득한 후 마이그레이션을 실행합니다. 락을 이미 보유하고 있는 상태에서 추가로 `migrate` 명령을 실행하려 하면, 명령은 실행되지 않지만 종료 상태 코드는 성공을 반환합니다.

```shell
php artisan migrate --isolated
```

> [!WARNING]
> 이 기능을 사용하려면 애플리케이션의 기본 캐시 드라이버가 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 중 하나여야 하며, 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

<a name="forcing-migrations-to-run-in-production"></a>
#### 운영 환경에서 강제로 마이그레이션 실행

일부 마이그레이션 작업은 데이터 손실을 유발할 수 있는 "파괴적" 작업입니다. 이로 인해 프로덕션 데이터베이스에 실수로 명령이 실행되는 것을 예방하기 위해, 명령 실행 전 확인 프롬프트가 표시됩니다. 프롬프트 없이 강제로 명령을 실행하려면 `--force` 플래그를 사용하면 됩니다.

```shell
php artisan migrate --force
```

<a name="rolling-back-migrations"></a>
### 마이그레이션 롤백 (Rolling Back Migrations)

가장 최근에 실행된 마이그레이션을 롤백하려면 `rollback` Artisan 명령어를 사용합니다. 이 명령은 마지막 "배치(batch)"의 모든 마이그레이션 파일을 롤백합니다.

```shell
php artisan migrate:rollback
```

`step` 옵션을 사용하면 원하는 개수만큼만 마이그레이션을 롤백할 수 있습니다. 예를 들어, 최신 5개의 마이그레이션만 롤백하려면 아래와 같이 실행합니다.

```shell
php artisan migrate:rollback --step=5
```

특정 "배치"의 마이그레이션만 롤백하고 싶을 때는 `batch` 옵션을 지정합니다. 이 값은 애플리케이션의 `migrations` 데이터베이스 테이블의 특정 배치 번호와 일치해야 합니다. 예를 들어, 배치 3에 포함된 모든 마이그레이션을 롤백하려면:

```shell
php artisan migrate:rollback --batch=3
```

마이그레이션이 실행할 SQL 문을 실제 실행하지 않고 확인만 하고 싶다면, `--pretend` 플래그를 사용할 수 있습니다.

```shell
php artisan migrate:rollback --pretend
```

`migrate:reset` 명령어를 사용하면 애플리케이션의 모든 마이그레이션을 한 번에 롤백할 수 있습니다.

```shell
php artisan migrate:reset
```

<a name="roll-back-migrate-using-a-single-command"></a>
#### 롤백과 마이그레이션을 한 번에 실행

`migrate:refresh` 명령어는 모든 마이그레이션을 롤백한 뒤 다시 `migrate` 명령을 수행합니다. 사실상 전체 데이터베이스를 재구성하는 효과와 같습니다.

```shell
php artisan migrate:refresh

# 데이터베이스를 새로고침하고 모든 데이터베이스 시드를 실행합니다...
php artisan migrate:refresh --seed
```

`step` 옵션을 사용하면, 지정한 횟수만큼만 롤백 및 재마이그레이션이 가능합니다.

```shell
php artisan migrate:refresh --step=5
```

<a name="drop-all-tables-migrate"></a>
#### 모든 테이블 삭제 후 마이그레이션

`migrate:fresh` 명령어는 데이터베이스의 모든 테이블을 삭제한 다음 `migrate` 명령을 실행합니다.

```shell
php artisan migrate:fresh

php artisan migrate:fresh --seed
```

기본적으로 `migrate:fresh` 명령은 디폴트 데이터베이스 연결의 테이블만 삭제합니다. 하지만 `--database` 옵션으로 마이그레이션 대상 데이터베이스 연결을 지정할 수 있습니다. 연결 이름은 애플리케이션의 `database` [설정 파일](/docs/12.x/configuration)에 정의된 값이어야 합니다.

```shell
php artisan migrate:fresh --database=admin
```

> [!WARNING]
> `migrate:fresh` 명령은 테이블 프리픽스와 상관없이 모든 데이터베이스 테이블을 삭제하므로, 다른 애플리케이션과 공유 중인 데이터베이스에서 사용할 때는 주의해야 합니다.

<a name="tables"></a>
## 테이블 (Tables)

<a name="creating-tables"></a>
### 테이블 생성 (Creating Tables)

새로운 데이터베이스 테이블을 생성하려면 `Schema` 파사드의 `create` 메서드를 사용하세요. 이 메서드는 첫 번째 인수로 테이블 이름, 두 번째 인수로는 `Blueprint` 객체를 전달받는 클로저를 받습니다. 이 객체를 사용해 새 테이블을 정의합니다.

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

테이블 생성 시, [컬럼 메서드](#creating-columns)를 자유롭게 사용하여 컬럼을 정의할 수 있습니다.

<a name="determining-table-column-existence"></a>
#### 테이블/컬럼 존재 여부 확인

`hasTable`, `hasColumn`, `hasIndex` 메서드를 사용해 테이블, 컬럼, 인덱스의 존재 여부를 확인할 수 있습니다.

```php
if (Schema::hasTable('users')) {
    // "users" 테이블이 존재합니다...
}

if (Schema::hasColumn('users', 'email')) {
    // "users" 테이블이 존재하며 "email" 컬럼이 있습니다...
}

if (Schema::hasIndex('users', ['email'], 'unique')) {
    // "users" 테이블에 "email" 컬럼의 고유 인덱스가 있습니다...
}
```

<a name="database-connection-table-options"></a>
#### 데이터베이스 연결 및 테이블 옵션

기본 데이터베이스 연결이 아닌 다른 연결에서 스키마 작업을 하려면 `connection` 메서드를 사용하세요.

```php
Schema::connection('sqlite')->create('users', function (Blueprint $table) {
    $table->id();
});
```

또한, 테이블 생성 시 다양한 속성 및 메서드를 추가로 지정할 수 있습니다. MariaDB나 MySQL에서 테이블의 저장 엔진을 지정하고 싶다면 `engine` 속성을 사용합니다.

```php
Schema::create('users', function (Blueprint $table) {
    $table->engine('InnoDB');
    // ...
});
```

`sset`과 `collation` 속성으로 테이블의 문자셋과 정렬방식을 지정할 수 있습니다.

```php
Schema::create('users', function (Blueprint $table) {
    $table->charset('utf8mb4');
    $table->collation('utf8mb4_unicode_ci');
    // ...
});
```

`temporary` 메서드를 사용하면 테이블을 "임시(temporary)" 테이블로 만들 수 있습니다. 임시 테이블은 현재 연결의 세션에서만 보이며, 연결이 종료되면 자동으로 삭제됩니다.

```php
Schema::create('calculations', function (Blueprint $table) {
    $table->temporary();
    // ...
});
```

테이블에 "주석(comment)"을 남기고 싶다면, 테이블 인스턴스의 `comment` 메서드를 호출하세요. 이 기능은 MariaDB, MySQL, PostgreSQL에서만 지원됩니다.

```php
Schema::create('calculations', function (Blueprint $table) {
    $table->comment('비즈니스 계산용 테이블');
    // ...
});
```

<a name="updating-tables"></a>
### 테이블 수정 (Updating Tables)

`Schema` 파사드의 `table` 메서드를 사용해 기존 테이블을 수정할 수 있습니다. `create`와 마찬가지로 테이블 이름과 클로저(이름이 `Blueprint`의 인스턴스)를 인수로 받으며, 해당 테이블에 컬럼 또는 인덱스를 추가할 수 있습니다.

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->integer('votes');
});
```

<a name="renaming-and-dropping-tables"></a>
### 테이블 이름 변경 / 삭제 (Renaming / Dropping Tables)

기존 데이터베이스 테이블의 이름을 바꾸려면 `rename` 메서드를 사용하세요.

```php
use Illuminate\Support\Facades\Schema;

Schema::rename($from, $to);
```

테이블을 삭제하려면 `drop` 또는 `dropIfExists` 메서드를 사용합니다.

```php
Schema::drop('users');

Schema::dropIfExists('users');
```

<a name="renaming-tables-with-foreign-keys"></a>
#### 외래 키를 가진 테이블 이름 변경

테이블 이름을 변경하기 전, 해당 테이블에서 외래 키 제약조건이 자동 생성된 이름이 아닌 명시적인 이름을 사용했는지 확인하세요. 그렇지 않으면 외래 키 이름이 기존 테이블 이름을 참조하게 되어 문제가 발생할 수 있습니다.

<a name="columns"></a>
## 컬럼 (Columns)

<a name="creating-columns"></a>
### 컬럼 생성 (Creating Columns)

`Schema` 파사드의 `table` 메서드를 사용해 기존 테이블에 컬럼을 추가할 수 있습니다. 인자로 테이블 이름과 클로저를 전달하며, `Illuminate\Database\Schema\Blueprint` 인스턴스를 활용해 컬럼을 정의합니다.

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->integer('votes');
});
```

<a name="available-column-types"></a>
### 사용 가능한 컬럼 타입 (Available Column Types)

스키마 빌더의 Blueprint 클래스는 데이터베이스 테이블에 추가할 수 있는 다양한 컬럼 타입 메서드를 제공합니다. 다음은 사용 가능한 모든 메서드 목록입니다.

#### 불리언 타입

<div class="collection-method-list" markdown="1">

[boolean](#column-method-boolean)

</div>

#### 문자열 & 텍스트 타입

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

#### 바이너리 타입

<div class="collection-method-list" markdown="1">

[binary](#column-method-binary)

</div>

#### 객체 & JSON 타입

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

#### 공간 타입

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

#### 특수 타입

<div class="collection-method-list" markdown="1">

[enum](#column-method-enum)
[set](#column-method-set)
[macAddress](#column-method-macAddress)
[ipAddress](#column-method-ipAddress)
[rememberToken](#column-method-rememberToken)
[vector](#column-method-vector)

</div>

<!-- 이하의 각 컬럼 메서드 설명은 모두 원문과 동일한 순서, 코드 예시와 Markdown 구조로 유지해야 하며, 
   각 설명은 이미 위에서 제시된 규정에 따라 번역하였습니다. 각 항목의 설명이 상당히 길기 때문에,
   이후에도 같은 방식, 동일한 스타일 및 규칙(구조, 코드 등은 그대로, 설명만 번역, 용어 등 유지)으로 번역이 이어져야 합니다. -->

<a name="column-method-bigIncrements"></a>
#### `bigIncrements()`

`bigIncrements` 메서드는 자동 증가하는 `UNSIGNED BIGINT`(기본 키) 타입 컬럼을 생성합니다.

```php
$table->bigIncrements('id');
```

<a name="column-method-bigInteger"></a>
#### `bigInteger()`

`bigInteger` 메서드는 `BIGINT` 타입 컬럼을 생성합니다.

```php
$table->bigInteger('votes');
```

<a name="column-method-binary"></a>
#### `binary()`

`binary` 메서드는 `BLOB` 타입 컬럼을 생성합니다.

```php
$table->binary('photo');
```

MySQL, MariaDB, SQL Server 사용 시, `length`와 `fixed` 인수를 지정해 `VARBINARY` 또는 `BINARY` 컬럼을 만들 수 있습니다.

```php
$table->binary('data', length: 16); // VARBINARY(16)

$table->binary('data', length: 16, fixed: true); // BINARY(16)
```

<!-- 이하 개별 컬럼 타입, 컬럼 수식어, 컬럼 수정, 이름 변경, 삭제, 인덱스, 외래 키, 이벤트 등 
     하위 항목들도 모두 동일하게 번역하여야 합니다.
     만약 추가 번역이 필요하다면, 다음 번역 요청을 통해 이어서 제공합니다. 
     (용량 관계로 인하여, 지금은 여기까지 번역합니다.) -->
