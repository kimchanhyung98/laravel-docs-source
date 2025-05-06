# 데이터베이스: 마이그레이션

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
    - [컬럼 수정](#modifying-columns)
    - [컬럼 이름 변경](#renaming-columns)
    - [컬럼 삭제](#dropping-columns)
- [인덱스](#indexes)
    - [인덱스 생성](#creating-indexes)
    - [인덱스 이름 변경](#renaming-indexes)
    - [인덱스 삭제](#dropping-indexes)
    - [외래 키 제한](#foreign-key-constraints)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

마이그레이션은 데이터베이스의 버전 관리를 제공하여, 팀원들이 애플리케이션의 데이터베이스 스키마 정의를 공유할 수 있게 해줍니다. 소스 컨트롤에서 변경 사항을 반영한 후 팀원들에게 로컬 데이터베이스 스키마에 컬럼을 수동으로 추가하라고 말해본 경험이 있다면, 바로 그 문제를 데이터베이스 마이그레이션이 해결합니다.

Laravel의 `Schema` [파사드](/docs/{{version}}/facades)는 모든 Laravel 지원 데이터베이스 시스템에서 데이터베이스에 중립적으로 테이블을 생성·수정할 수 있도록 지원합니다. 일반적으로 마이그레이션은 이 파사드를 사용하여 테이블과 컬럼을 생성·수정합니다.

<a name="generating-migrations"></a>
## 마이그레이션 생성

`make:migration` [Artisan 명령어](/docs/{{version}}/artisan)를 사용하여 데이터베이스 마이그레이션을 생성할 수 있습니다. 새로운 마이그레이션 파일은 `database/migrations` 디렉터리에 생성됩니다. 각 마이그레이션 파일 이름에는 타임스탬프가 포함되어 있어 Laravel이 마이그레이션의 실행 순서를 판단할 수 있습니다.

```shell
php artisan make:migration create_flights_table
```

Laravel은 마이그레이션의 이름을 통해 어떤 테이블을 생성하는지 혹은 신규 테이블 생성인지 자동으로 추정하려고 시도합니다. 이름에서 테이블을 추정할 수 있으면, 지정한 테이블을 미리 설정하여 마이그레이션 파일이 생성됩니다. 그렇지 않을 경우, 마이그레이션 파일 내에서 직접 테이블을 지정하면 됩니다.

생성할 마이그레이션의 경로를 직접 지정하고 싶다면 `make:migration` 명령어 실행 시 `--path` 옵션을 사용할 수 있습니다. 지정 경로는 애플리케이션 베이스 경로를 기준으로 상대 경로로 작성하세요.

> [!NOTE]
> 마이그레이션 스텁 파일은 [스텁 퍼블리시](/docs/{{version}}/artisan#stub-customization)를 통해 커스터마이징 할 수 있습니다.

<a name="squashing-migrations"></a>
### 마이그레이션 합치기(Squashing)

애플리케이션이 커가면서 마이그레이션 파일이 점점 많아질 수 있습니다. 이로 인해 `database/migrations` 디렉터리에 수백 개의 마이그레이션 파일이 생길 수 있습니다. 이럴 때 원하는 경우 여러 마이그레이션을 하나의 SQL 파일로 "합칠" 수 있습니다. 다음 명령어로 시작하세요:

```shell
php artisan schema:dump

# 현재 데이터베이스 스키마를 덤프하고 기존의 모든 마이그레이션을 제거합니다...
php artisan schema:dump --prune
```

이 명령을 실행하면, Laravel은 애플리케이션의 `database/schema` 디렉터리에 "스키마" 파일을 작성합니다. 파일 이름은 데이터베이스 커넥션에 대응합니다. 만약 데이터베이스에 아직 다른 마이그레이션이 실행되지 않았다면, 마이그레이션 시 사용중인 커넥션의 스키마 파일의 SQL문이 먼저 실행됩니다. 이후 남아있는 마이그레이션이 순차적으로 실행됩니다.

테스트 수행 시 일반적으로 사용하는 개발용 커넥션과 다른 데이터베이스 커넥션을 사용하는 경우, 해당 커넥션으로도 스키마 파일을 덤프해두어야 테스트에서 DB 구조를 제대로 생성할 수 있습니다. 보통 개발용 커넥션으로 작업을 마친 후 이를 수행하길 권장합니다:

```shell
php artisan schema:dump
php artisan schema:dump --database=testing --prune
```

만든 데이터베이스 스키마 파일은 반드시 소스 코드에 커밋해서, 팀의 다른 신규 개발자가 빠르게 초기 데이터베이스 구조를 생성할 수 있도록 하세요.

> [!WARNING]
> 마이그레이션 합치기(squashing)는 MariaDB, MySQL, PostgreSQL, SQLite 데이터베이스에서만 사용할 수 있으며 데이터베이스의 명령줄 클라이언트를 이용합니다.

<a name="migration-structure"></a>
## 마이그레이션 구조

마이그레이션 클래스는 두 가지 메서드를 가집니다: `up`과 `down`. `up` 메서드는 데이터베이스에 새 테이블, 컬럼, 인덱스를 추가할 때 사용하며, `down` 메서드는 `up` 메서드에서 수행한 작업을 되돌립니다.

두 메서드 모두에서 Laravel의 스키마 빌더를 사용해 테이블을 생성/수정할 수 있습니다. `Schema` 빌더에서 사용할 수 있는 모든 메서드는 [별도 문서](#creating-tables)를 참고하세요. 아래 예시는 `flights` 테이블을 생성하는 마이그레이션입니다.

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * 마이그레이션 실행.
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
     * 마이그레이션 롤백.
     */
    public function down(): void
    {
        Schema::drop('flights');
    }
};
```

<a name="setting-the-migration-connection"></a>
#### 마이그레이션 커넥션 설정

마이그레이션이 애플리케이션의 기본 커넥션이 아닌 다른 데이터베이스 커넥션을 사용해야 한다면, 마이그레이션 클래스의 `$connection` 속성을 설정하세요.

```php
/**
 * 마이그레이션에 사용할 데이터베이스 커넥션.
 *
 * @var string
 */
protected $connection = 'pgsql';

/**
 * 마이그레이션 실행.
 */
public function up(): void
{
    // ...
}
```

<a name="skipping-migrations"></a>
#### 마이그레이션 건너뛰기

특정 마이그레이션이 아직 활성화되지 않은 기능을 지원하기 위해 준비된 경우 당장은 실행하고 싶지 않을 수 있습니다. 이때 마이그레이션에 `shouldRun` 메서드를 정의할 수 있습니다. 이 메서드가 `false`를 반환하면 해당 마이그레이션은 건너뜁니다:

```php
use App\Models\Flights;
use Laravel\Pennant\Feature;

/**
 * 이 마이그레이션을 실행해야 하는지 여부 판단.
 */
public function shouldRun(): bool
{
    return Feature::active(Flights::class);
}
```

<a name="running-migrations"></a>
## 마이그레이션 실행

모든 남아있는 마이그레이션을 실행하려면, `migrate` Artisan 명령어를 사용하세요:

```shell
php artisan migrate
```

이제까지 실행된 마이그레이션 목록을 보려면 `migrate:status`를 사용할 수 있습니다:

```shell
php artisan migrate:status
```

실제 실행하지 않고 마이그레이션으로 실행될 SQL을 확인하고 싶다면 `--pretend` 옵션을 사용하세요.

```shell
php artisan migrate --pretend
```

#### 마이그레이션 실행 격리

애플리케이션을 여러 서버에 배포하고, 배포 중에 마이그레이션을 실행하는 경우 두 서버가 동시에 마이그레이션을 시도하는 것을 원치 않을 것입니다. 이를 방지하려면 `migrate` 명령어 실행 시 `--isolated` 옵션을 사용할 수 있습니다.

`isolated` 옵션을 제공하면, Laravel은 마이그레이션 실행 전에 애플리케이션의 캐시 드라이버로 원자적(atomic) 락을 획득합니다. 락이 유지되는 동안에는 다른 마이그레이션 실행 시도가 무시되지만, 명령 자체는 성공 코드로 종료됩니다:

```shell
php artisan migrate --isolated
```

> [!WARNING]
> 이 기능을 사용하려면, 애플리케이션의 기본 캐시 드라이버가 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 중 하나여야 하며, 모든 서버는 동일한 중앙 캐시 서버와 통신해야 합니다.

<a name="forcing-migrations-to-run-in-production"></a>
#### 프로덕션 환경에서 강제 실행

일부 마이그레이션 작업은 데이터 손실을 유발할 수 있습니다. 실수로 프로덕션 DB에 이런 명령어를 실행하지 않도록, 명령 실행 전 확인 메시지가 출력됩니다. 프롬프트 없이 강제로 실행하려면 `--force` 플래그를 사용하세요:

```shell
php artisan migrate --force
```

<a name="rolling-back-migrations"></a>
### 마이그레이션 롤백

가장 최근에 실행된 마이그레이션 작업을 되돌리려면 `rollback` Artisan 명령어를 사용하세요. 이 명령은 마지막 '배치'의 모든 마이그레이션 파일을 롤백합니다.

```shell
php artisan migrate:rollback
```

`step` 옵션으로 롤백할 마이그레이션 파일 수를 제한할 수 있습니다. 예를 들어, 마지막 5개 마이그레이션만 롤백하려면:

```shell
php artisan migrate:rollback --step=5
```

`batch` 옵션으로 특정 배치의 모든 마이그레이션을 롤백할 수도 있습니다. `batch` 값은 애플리케이션의 `migrations` 테이블 내 배치 값입니다.

```shell
php artisan migrate:rollback --batch=3
```

실제 롤백하지 않고 SQL만 확인하려면 `--pretend` 옵션을 사용하세요:

```shell
php artisan migrate:rollback --pretend
```

`migrate:reset` 명령어로 모든 마이그레이션을 롤백할 수 있습니다:

```shell
php artisan migrate:reset
```

<a name="roll-back-migrate-using-a-single-command"></a>
#### 단일 명령어로 롤백 후 마이그레이션

`migrate:refresh` 명령어는 모든 마이그레이션을 롤백한 후 다시 실행합니다. 이 명령어로 전체 데이터베이스를 재구성할 수 있습니다.

```shell
php artisan migrate:refresh

# 데이터베이스를 새로고침하고 모든 시더 실행...
php artisan migrate:refresh --seed
```

`step` 옵션으로 마지막 일부만 롤백 후 재실행도 가능합니다:

```shell
php artisan migrate:refresh --step=5
```

<a name="drop-all-tables-migrate"></a>
#### 모든 테이블 삭제 후 마이그레이션

`migrate:fresh` 명령어는 모든 테이블을 삭제한 뒤 마이그레이션을 실행합니다:

```shell
php artisan migrate:fresh

php artisan migrate:fresh --seed
```

기본적으로 `migrate:fresh` 명령어는 기본 데이터베이스 커넥션의 테이블만 삭제합니다. 그러나 `--database` 옵션으로 특정 커넥션을 지정할 수 있습니다. 커넥션 이름은 애플리케이션의 데이터베이스 [환경설정 파일](/docs/{{version}}/configuration)에 정의되어야 합니다.

```shell
php artisan migrate:fresh --database=admin
```

> [!WARNING]
> `migrate:fresh` 명령어는 프리픽스와 관계없이 모든 데이터베이스 테이블을 삭제합니다. 여러 애플리케이션이 공유하는 DB에서 사용할 때는 주의해야 합니다.

<a name="tables"></a>
## 테이블

<a name="creating-tables"></a>
### 테이블 생성

새 데이터베이스 테이블을 만들려면, `Schema` 파사드의 `create` 메서드를 사용하세요. `create` 메서드는 테이블 이름과, 새 테이블을 정의하는 데 사용할 수 있는 `Blueprint` 인스턴스를 받는 클로저를 인자로 받습니다:

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

테이블 생성 시, [컬럼 메서드](#creating-columns)를 활용하여 컬럼을 정의할 수 있습니다.

<a name="determining-table-column-existence"></a>
#### 테이블/컬럼 존재 여부 확인

`hasTable`, `hasColumn`, `hasIndex` 메서드를 이용해 테이블, 컬럼, 인덱스 존재 여부를 확인할 수 있습니다:

```php
if (Schema::hasTable('users')) {
    // "users" 테이블이 존재합니다...
}

if (Schema::hasColumn('users', 'email')) {
    // "users" 테이블에 "email" 컬럼이 존재합니다...
}

if (Schema::hasIndex('users', ['email'], 'unique')) {
    // "users" 테이블에 "email" 컬럼을 위한 unique 인덱스가 존재합니다...
}
```

<a name="database-connection-table-options"></a>
#### 데이터베이스 커넥션 및 테이블 옵션

디폴트가 아닌 커넥션에서 스키마 작업을 하려면 `connection` 메서드를 사용하세요:

```php
Schema::connection('sqlite')->create('users', function (Blueprint $table) {
    $table->id();
});
```

또한 몇몇 속성과 메서드를 통해 테이블 생성 시 기타 옵션을 제어할 수 있습니다. 예를 들어, MariaDB/MySQL에서는 `engine` 메서드로 저장 엔진을 지정할 수 있습니다:

```php
Schema::create('users', function (Blueprint $table) {
    $table->engine('InnoDB');

    // ...
});
```

MariaDB/MySQL에서 테이블의 문자셋과 콜레이션 설정은 다음과 같습니다:

```php
Schema::create('users', function (Blueprint $table) {
    $table->charset('utf8mb4');
    $table->collation('utf8mb4_unicode_ci');

    // ...
});
```

`temporary` 메서드로 임시 테이블 선언도 가능합니다. 임시 테이블은 해당 커넥션 세션에만 보이고, 세션 종료 시 자동으로 삭제됩니다.

```php
Schema::create('calculations', function (Blueprint $table) {
    $table->temporary();

    // ...
});
```

테이블에 "코멘트"를 추가하려면 `comment` 메서드를 사용하세요. 이 기능은 MariaDB, MySQL 및 PostgreSQL에서 지원됩니다:

```php
Schema::create('calculations', function (Blueprint $table) {
    $table->comment('Business calculations');

    // ...
});
```

<a name="updating-tables"></a>
### 테이블 수정

`Schema` 파사드의 `table` 메서드는 기존 테이블을 수정할 때 사용합니다. `create`와 마찬가지로, 테이블 이름과 수정 작업을 정의하는 `Blueprint` 인스턴스를 받는 클로저를 인자로 지정합니다:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->integer('votes');
});
```

<a name="renaming-and-dropping-tables"></a>
### 테이블 이름 변경/삭제

기존 데이터베이스 테이블의 이름을 변경하려면 `rename` 메서드를 사용하세요:

```php
use Illuminate\Support\Facades\Schema;

Schema::rename($from, $to);
```

기존 테이블 삭제는 `drop` 또는 `dropIfExists` 메서드를 사용하세요:

```php
Schema::drop('users');

Schema::dropIfExists('users');
```

<a name="renaming-tables-with-foreign-keys"></a>
#### 외래 키가 있는 테이블 이름 변경

테이블 이름을 변경하기 전에, 해당 테이블의 외래 키 제약에 명시적 이름이 마이그레이션 파일에 지정되어 있는지 반드시 확인하세요. Laravel이 자동으로 이름을 지정한 경우, 제약 이름이 이전 테이블 이름을 참조하게 됩니다.

<a name="columns"></a>
## 컬럼

<a name="creating-columns"></a>
### 컬럼 생성

`Schema` 파사드의 `table` 메서드는 기존 테이블에 컬럼을 추가할 때 사용합니다. 앞서 살펴 본 것처럼, 테이블 이름과 `Illuminate\Database\Schema\Blueprint` 인스턴스를 받는 클로저를 넘깁니다.

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->integer('votes');
});
```

<a name="available-column-types"></a>
### 사용 가능한 컬럼 타입

스키마 빌더(Blueprint)는 다양한 컬럼 타입에 해당하는 여러 메서드를 제공합니다. 각 메서드와 설명은 아래 표를 참고하세요.

#### Boolean 타입

[boolean](#column-method-boolean)

#### 문자열/텍스트 타입

[char](#column-method-char)
[longText](#column-method-longText)
[mediumText](#column-method-mediumText)
[string](#column-method-string)
[text](#column-method-text)
[tinyText](#column-method-tinyText)

#### 숫자 타입

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

#### 날짜/시간 타입

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

#### 바이너리 타입

[binary](#column-method-binary)

#### 오브젝트/JSON 타입

[json](#column-method-json)
[jsonb](#column-method-jsonb)

#### UUID/ULID 타입

[ulid](#column-method-ulid)
[ulidMorphs](#column-method-ulidMorphs)
[uuid](#column-method-uuid)
[uuidMorphs](#column-method-uuidMorphs)
[nullableUlidMorphs](#column-method-nullableUlidMorphs)
[nullableUuidMorphs](#column-method-nullableUuidMorphs)

#### 공간정보(Spatial) 타입

[geography](#column-method-geography)
[geometry](#column-method-geometry)

#### 관계(Relationship) 타입

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

각 컬럼 타입의 상세 예시는 원문 코드 블록 예시를 참고하세요(코드 블록은 번역하지 않습니다).

<a name="column-modifiers"></a>
### 컬럼 수정자

위에서 소개한 컬럼 타입 외에도, 컬럼 추가 시 사용할 수 있는 다양한 "수정자"가 있습니다. 예를 들어, 컬럼을 NULL 허용으로 만들고 싶다면 `nullable` 메서드를 사용하면 됩니다.

컬럼 수정자들은 아래 표를 참고하세요(인덱스 수정자는 제외).

| 수정자                                | 설명                                                                                  |
| ------------------------------------ | ------------------------------------------------------------------------------------ |
| `->after('column')`                  | 컬럼을 다른 컬럼 뒤에 위치시킴 (MariaDB / MySQL)                                     |
| `->autoIncrement()`                  | `INTEGER` 컬럼을 자동 증가 (기본키)로 설정                                            |
| `->charset('utf8mb4')`               | 컬럼의 문자셋 지정 (MariaDB / MySQL)                                                 |
| `->collation('utf8mb4_unicode_ci')`  | 컬럼의 콜레이션 지정                                                                 |
| `->comment('my comment')`            | 컬럼에 코멘트 추가 (MariaDB / MySQL / PostgreSQL)                                    |
| `->default($value)`                  | 컬럼의 "기본값" 지정                                                                 |
| `->first()`                          | 컬럼을 테이블의 제일 앞에 위치시킴 (MariaDB / MySQL)                                 |
| `->from($integer)`                   | 자동 증가 필드의 시작 값을 지정 (MariaDB / MySQL / PostgreSQL)                       |
| `->invisible()`                      | 컬럼을 `SELECT *` 에서 숨김 처리 (MariaDB / MySQL)                                   |
| `->nullable($value = true)`          | 컬럼에 `NULL` 값 허용                                                                |
| `->storedAs($expression)`            | 저장된 생성 컬럼 생성 (MariaDB / MySQL / PostgreSQL / SQLite)                        |
| `->unsigned()`                       | `INTEGER` 컬럼의 부호 없음(UNSIGNED) 설정 (MariaDB / MySQL)                         |
| `->useCurrent()`                     | `TIMESTAMP` 컬럼 기본값을 `CURRENT_TIMESTAMP`로 설정                                 |
| `->useCurrentOnUpdate()`             | 레코드 갱신 시에 `CURRENT_TIMESTAMP` 사용 (MariaDB / MySQL)                         |
| `->virtualAs($expression)`           | 가상 생성 컬럼 생성 (MariaDB / MySQL / SQLite)                                       |
| `->generatedAs($expression)`         | 지정 시퀀스 옵션으로 ID 컬럼 생성 (PostgreSQL)                                       |
| `->always()`                         | ID 컬럼에서 입력값보다 시퀀스 값 우선 여부 정의 (PostgreSQL)                        |

<a name="default-expressions"></a>
#### 기본값 표현식

`default` 수정자는 값 또는 `Illuminate\Database\Query\Expression` 인스턴스를 받을 수 있습니다. 표현식을 사용하면 라라벨이 값에 따옴표를 감싸지 않아 데이터베이스의 특정 함수 등을 사용할 수 있습니다. 예를 들어, JSON 컬럼의 기본값을 지정할 때 유용합니다.

> [!WARNING]
> 기본값 표현식 지원 여부는 DB 드라이버, 버전, 데이터 타입에 따라 다릅니다. 반드시 DB 문서를 참고하세요.

<a name="column-order"></a>
#### 컬럼 순서

MariaDB 또는 MySQL에서는 `after` 메서드로 특정 컬럼 뒤에 새로운 컬럼을 추가할 수 있습니다.

<a name="modifying-columns"></a>
### 컬럼 수정

`change` 메서드를 사용하면 기존 컬럼의 타입 및 속성을 변경할 수 있습니다. 변경 시 보존하고 싶은 모든 속성을 반드시 명시해주어야 하며, 누락하면 해당 속성이 삭제됩니다. 기본적으로 인덱스는 변경되지 않으므로, 인덱스 수정이 필요하면 별도의 인덱스 수정자를 명확히 호출해야 합니다.

<a name="renaming-columns"></a>
### 컬럼 이름 변경

컬럼 이름 변경은 `renameColumn` 메서드를 사용하세요.

<a name="dropping-columns"></a>
### 컬럼 삭제

`dropColumn` 메서드로 컬럼을 삭제할 수 있습니다. 여러 컬럼을 삭제하려면 컬럼명을 배열로 전달하면 됩니다.

<a name="available-command-aliases"></a>
#### 사용 가능한 명령어 별칭

일반적으로 사용되는 컬럼 삭제 용도로 별도의 메서드가 제공됩니다:

| 명령어                             | 설명                                      |
| ----------------------------------- | ----------------------------------------- |
| `$table->dropMorphs('morphable');`  | `morphable_id`와 `morphable_type` 컬럼 삭제 |
| `$table->dropRememberToken();`      | `remember_token` 컬럼 삭제                |
| `$table->dropSoftDeletes();`        | `deleted_at` 컬럼 삭제                    |
| `$table->dropSoftDeletesTz();`      | `dropSoftDeletes()` 메서드의 별칭          |
| `$table->dropTimestamps();`         | `created_at`, `updated_at` 컬럼 삭제      |
| `$table->dropTimestampsTz();`       | `dropTimestamps()` 메서드의 별칭           |

<a name="indexes"></a>
## 인덱스

<a name="creating-indexes"></a>
### 인덱스 생성

Laravel 스키마 빌더는 다양한 인덱스 타입을 지원합니다. 아래 예시는 새로운 `email` 컬럼을 만들고 값이 유니크하도록 지정하며, 해당 인덱스는 컬럼 정의에 `unique` 메서드를 체이닝하면 됩니다.

또는, 컬럼을 먼저 정의한 후 `unique` 등의 메서드를 사용할 수도 있습니다. 복합 인덱스(여러 컬럼 인덱스)도 배열로 지정할 수 있습니다.

인덱스 생성 시 Laravel이 자동으로 인덱스 이름을 생성하지만, 두 번째 인자로 직접 인덱스 이름을 정해줄 수도 있습니다.

<a name="available-index-types"></a>
#### 사용 가능한 인덱스 타입

각 인덱스 타입 별로 전용 메서드가 있습니다. 자세한 설명은 표를 참고하세요.

| 명령어                                           | 설명                                      |
| ------------------------------------------------ | ----------------------------------------- |
| `$table->primary('id');`                         | 기본키 지정                               |
| `$table->primary(['id', 'parent_id']);`          | 복합키 지정                               |
| `$table->unique('email');`                       | 유니크 인덱스 지정                        |
| `$table->index('state');`                        | 일반 인덱스 지정                          |
| `$table->fullText('body');`                      | 전문(full text) 인덱스 (MariaDB/MySQL/PostgreSQL) |
| `$table->fullText('body')->language('english');` | 지정 언어의 전문 인덱스 (PostgreSQL)      |
| `$table->spatialIndex('location');`              | 공간 인덱스(Spatial, SQLite 제외)         |

<a name="renaming-indexes"></a>
### 인덱스 이름 변경

`renameIndex` 메서드로 인덱스의 이름을 변경할 수 있습니다. 첫번째 인자는 현재 이름, 두번째 인자는 변경할 이름입니다.

<a name="dropping-indexes"></a>
### 인덱스 삭제

인덱스를 삭제하려면 인덱스 이름을 명시적으로 지정해야 합니다. Laravel은 기본적으로 테이블명, 컬럼명, 인덱스 타입을 조합하여 이름을 만듭니다.

배열로 컬럼명을 넘기면 관례(index naming convention)에 따라 인덱스 이름을 자동으로 생성해서 해당 인덱스를 삭제합니다.

<a name="foreign-key-constraints"></a>
### 외래 키 제약

Laravel은 데이터베이스 수준에서 참조 무결성을 강제하는 외래 키 제약도 지원합니다. 예를 들어, `posts` 테이블의 `user_id` 컬럼이 `users` 테이블의 `id` 컬럼을 참조하도록 할 수 있습니다.

보다 간결한 방법으로, `foreignId`와 `constrained` 메서드를 활용하여 외래 키 제약을 보다 쉽게 생성할 수 있습니다. 또한, 참조하는 테이블명이나 인덱스 이름, 삭제/수정 시 동작도 옵션으로 지정할 수 있습니다.

추가로, 외래 키 제약의 `onDelete`, `onUpdate` 관련 메서드에 대한 별도의 직관적인 축약 버전도 제공됩니다.

추가적인 [컬럼 수정자](#column-modifiers)는 `constrained` 메서드 호출 전에 체이닝 해야 합니다.

<a name="dropping-foreign-keys"></a>
#### 외래 키 제약 삭제

외래 키 제약을 삭제하려면, `dropForeign` 메서드에 외래 키 제약 이름을 전달하면 삭제됩니다(인덱스와 동일한 명명 규칙 사용). 또는, 컬럼명을 배열로 전달해도 Laravel이 자동으로 제약 이름을 만들고 삭제합니다.

<a name="toggling-foreign-key-constraints"></a>
#### 외래 키 제약 활성화/비활성화

마이그레이션 내에서 다음 메서드로 외래 키 제약을 활성화/비활성화 할 수 있습니다:

```php
Schema::enableForeignKeyConstraints();

Schema::disableForeignKeyConstraints();

Schema::withoutForeignKeyConstraints(function () {
    // 해당 클로저 내에서 제약이 비활성화됩니다...
});
```

> [!WARNING]
> SQLite는 기본적으로 외래 키 제약이 비활성화되어 있습니다. SQLite 사용 시, 마이그레이션에서 외래 키 사용 전 반드시 [DB 설정](/docs/{{version}}/database#configuration)에서 제약을 활성화하세요.

<a name="events"></a>
## 이벤트

편의를 위해, 각 마이그레이션 작업은 [이벤트](/docs/{{version}}/events)를 발생시킵니다. 모든 이벤트는 기본 `Illuminate\Database\Events\MigrationEvent` 클래스를 상속합니다.

| 클래스                                           | 설명                                       |
| ------------------------------------------------ | ------------------------------------------ |
| `Illuminate\Database\Events\MigrationsStarted`   | 마이그레이션 일괄 실행 시작                 |
| `Illuminate\Database\Events\MigrationsEnded`     | 마이그레이션 일괄 실행 종료                 |
| `Illuminate\Database\Events\MigrationStarted`    | 단일 마이그레이션 실행 시작                 |
| `Illuminate\Database\Events\MigrationEnded`      | 단일 마이그레이션 실행 종료                 |
| `Illuminate\Database\Events\NoPendingMigrations` | 실행할 마이그레이션이 없음                 |
| `Illuminate\Database\Events\SchemaDumped`        | 데이터베이스 스키마 덤프 완료               |
| `Illuminate\Database\Events\SchemaLoaded`        | 기존 DB 스키마 덤프 로딩 완료               |
