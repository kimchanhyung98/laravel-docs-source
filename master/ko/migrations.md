# 데이터베이스: 마이그레이션

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
## 소개

마이그레이션은 데이터베이스의 버전 관리를 가능하게 해주며, 팀원들이 애플리케이션의 데이터베이스 스키마 정의를 명확하게 작성하고 공유할 수 있게 합니다. 만약 소스 컨트롤에서 변경사항을 받아온 후 테이블에 수동으로 컬럼을 추가하라고 동료에게 알려야 했던 적이 있다면, 그 문제를 마이그레이션이 해결해줍니다.

Laravel의 `Schema` [파사드](/docs/{{version}}/facades)는 모든 Laravel 지원 데이터베이스 시스템에서 데이터베이스에 독립적인 테이블 생성 및 조작을 지원합니다. 일반적으로 마이그레이션에서는 이 파사드를 사용하여 데이터베이스 테이블과 컬럼을 생성 및 수정합니다.

<a name="generating-migrations"></a>
## 마이그레이션 생성

`make:migration` [Artisan 명령어](/docs/{{version}}/artisan)를 사용하여 데이터베이스 마이그레이션을 생성할 수 있습니다. 새 마이그레이션 파일은 `database/migrations` 디렉터리에 저장됩니다. 각 마이그레이션 파일의 이름에는 Laravel이 마이그레이션 순서를 결정할 수 있도록 타임스탬프가 포함됩니다.

```shell
php artisan make:migration create_flights_table
```

Laravel은 마이그레이션의 이름을 기반으로 테이블 이름과 새 테이블 생성 여부를 자동 추측하려고 시도합니다. 만약 마이그레이션 이름에서 테이블 이름을 확인할 수 있다면, 해당 테이블이 미리 채워져 생성됩니다. 그렇지 않은 경우, 마이그레이션 파일 내에서 테이블을 수동으로 지정할 수 있습니다.

생성된 마이그레이션의 경로를 별도로 지정하고 싶다면 `make:migration` 명령 실행 시 `--path` 옵션을 사용할 수 있습니다. 지정하는 경로는 애플리케이션의 기준 경로를 기준으로 상대 경로여야 합니다.

> [!NOTE]
> 마이그레이션 스텁은 [스텁 퍼블리싱](/docs/{{version}}/artisan#stub-customization)을 통해 커스터마이즈할 수 있습니다.

<a name="squashing-migrations"></a>
### 마이그레이션 스쿼싱

애플리케이션을 개발하면서 시간이 지남에 따라 점점 더 많은 마이그레이션이 생길 수 있습니다. 이로 인해 `database/migrations` 디렉터리가 수백 개의 마이그레이션 파일로 복잡해질 수 있습니다. 원한다면, 여러 마이그레이션을 하나의 SQL 파일로 "스쿼싱(합치기)"할 수 있습니다. 시작하려면 `schema:dump` 명령을 실행합니다.

```shell
php artisan schema:dump

# 현재 데이터베이스 스키마를 덤프하고 기존 마이그레이션 모두 정리...
php artisan schema:dump --prune
```

이 명령을 실행하면, Laravel은 애플리케이션의 `database/schema` 디렉터리에 "스키마" 파일을 작성합니다. 스키마 파일의 이름은 해당 데이터베이스 연결에 대응합니다. 이후, 데이터베이스 마이그레이션을 시도할 때 이전에 마이그레이션이 실행되지 않았다면, Laravel은 해당 데이터베이스 연결의 스키마 파일 내 SQL을 먼저 실행합니다. 그 다음, 스키마 덤프에 포함되지 않은 나머지 마이그레이션을 차례로 실행합니다.

테스트 환경에서 사용하는 데이터베이스 연결이 로컬 개발 중 사용하는 연결과 다르다면, 테스트용 데이터베이스 연결로도 스키마 파일을 덤프해야 데이터베이스가 올바르게 구축됩니다. 일반적으로 개발용 데이터베이스 연결을 먼저 덤프한 후, 아래와 같이 실행합니다.

```shell
php artisan schema:dump
php artisan schema:dump --database=testing --prune
```

이 스키마 파일은 팀의 다른 새로운 개발자들이 애플리케이션의 초기 데이터베이스 구조를 빠르게 구축할 수 있도록 소스 컨트롤에 포함하는 것이 좋습니다.

> [!WARNING]
> 마이그레이션 스쿼싱 기능은 MariaDB, MySQL, PostgreSQL, SQLite 데이터베이스에서만 제공되며, 데이터베이스의 커맨드 라인 클라이언트를 사용합니다.

<a name="migration-structure"></a>
## 마이그레이션 구조

마이그레이션 클래스는 `up` 및 `down` 두 개의 메서드를 가집니다. `up` 메서드는 새로운 테이블, 컬럼, 인덱스를 추가할 때 사용되고, `down` 메서드는 `up` 메서드에서 수행한 작업을 역으로 되돌리는 데 사용됩니다.

두 메서드 모두에서 Laravel 스키마 빌더를 사용하여 테이블을 명확하게 생성 및 수정할 수 있습니다. `Schema` 빌더가 제공하는 모든 메서드에 대해 더 자세히 알고 싶다면 [관련 문서](#creating-tables)를 확인해 보세요. 예를 들어, 아래 마이그레이션은 `flights` 테이블을 생성합니다.

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

만약 마이그레이션이 애플리케이션의 기본 데이터베이스 연결이 아닌 다른 연결과 상호작용해야 한다면, 마이그레이션 클래스 내 `$connection` 속성을 설정해야 합니다.

```php
/**
 * 마이그레이션에서 사용할 데이터베이스 연결
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
## 마이그레이션 실행

미처 실행되지 않은 모든 마이그레이션을 실행하려면 `migrate` Artisan 명령어를 실행하세요.

```shell
php artisan migrate
```

현재까지 실행된 마이그레이션 목록을 확인하고 싶다면 `migrate:status` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan migrate:status
```

마이그레이션이 실제로 실행되기 전에 어떤 SQL 쿼리가 실행될지 미리 확인하려면 `--pretend` 플래그를 추가하여 실행할 수 있습니다.

```shell
php artisan migrate --pretend
```

#### 마이그레이션 실행 격리

여러 서버에 애플리케이션을 배포하며 배포 과정의 일부로 마이그레이션을 실행할 경우, 두 서버가 동시에 마이그레이션을 실행하지 않도록 하고 싶을 것입니다. 이를 방지하기 위해 `migrate` 명령 실행 시 `--isolated` 옵션을 사용할 수 있습니다.

이 옵션을 사용할 경우, Laravel은 마이그레이션을 실행하기 전에 애플리케이션의 캐시 드라이버를 사용해 원자적(atomic) 락을 획득합니다. 이 락이 유지되는 동안 다른 `migrate` 명령 실행 시도는 실제로 실행되지 않으며, 성공적인 종료 코드만 반환됩니다.

```shell
php artisan migrate --isolated
```

> [!WARNING]
> 이 기능을 활용하려면 애플리케이션의 기본 캐시 드라이버가 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 중 하나여야 합니다. 또한 모든 서버가 동일한 중앙 캐시 서버와 소통해야 합니다.

<a name="forcing-migrations-to-run-in-production"></a>
#### 운영 환경에서 강제로 마이그레이션 실행

일부 마이그레이션 작업은 데이터 유실을 유발하는 파괴적인 작업이 될 수 있습니다. 이를 보호하기 위해, 운영 데이터베이스에서 해당 명령 실행 시 확인을 요청받게 됩니다. 프롬프트 없이 강제로 명령을 실행하려면 `--force` 플래그를 사용하세요.

```shell
php artisan migrate --force
```

<a name="rolling-back-migrations"></a>
### 마이그레이션 롤백

가장 최근에 실행한 마이그레이션 작업을 롤백하려면 `rollback` Artisan 명령어를 사용합니다. 이 명령은 마지막 "배치"의 마이그레이션 파일을 모두 롤백합니다.

```shell
php artisan migrate:rollback
```

`step` 옵션을 지정하면 제한된 수의 마이그레이션만 롤백할 수 있습니다. 예를 들어 아래 명령은 마지막 다섯 개의 마이그레이션을 롤백합니다.

```shell
php artisan migrate:rollback --step=5
```

특정 "배치"의 마이그레이션을 롤백하려면 `batch` 옵션을 사용할 수 있습니다. `batch` 값은 애플리케이션의 `migrations` 테이블에 있습니다.

```shell
php artisan migrate:rollback --batch=3
```

실제로 마이그레이션을 실행하지 않고 어떤 SQL 쿼리가 실행될지 확인하려면 `--pretend` 플래그를 추가할 수 있습니다.

```shell
php artisan migrate:rollback --pretend
```

`migrate:reset` 명령어는 애플리케이션의 모든 마이그레이션을 롤백합니다.

```shell
php artisan migrate:reset
```

<a name="roll-back-migrate-using-a-single-command"></a>
#### 롤백과 마이그레이트를 한 번에 실행

`migrate:refresh` 명령어는 모든 마이그레이션을 롤백한 뒤 다시 마이그레이션을 실행합니다. 이 명령어는 데이터베이스 전체를 재구성합니다.

```shell
php artisan migrate:refresh

# 데이터베이스를 리프레시 후 시드 실행
php artisan migrate:refresh --seed
```

`refresh` 명령에 `step` 옵션을 추가하면 지정한 수 만큼 롤백 후 다시 마이그레이션합니다.

```shell
php artisan migrate:refresh --step=5
```

<a name="drop-all-tables-migrate"></a>
#### 모든 테이블 삭제 후 마이그레이션

`migrate:fresh` 명령어는 데이터베이스의 모든 테이블을 삭제하고 다시 마이그레이션을 실행합니다.

```shell
php artisan migrate:fresh

php artisan migrate:fresh --seed
```

기본적으로 `migrate:fresh` 명령은 기본 데이터베이스 연결에서만 테이블을 삭제합니다. 그러나 `--database` 옵션을 이용해 마이그레이션하고 싶은 데이터베이스 연결을 지정할 수 있습니다. 연결 이름은 애플리케이션의 [설정 파일](/docs/{{version}}/configuration)에 정의된 값이어야 합니다.

```shell
php artisan migrate:fresh --database=admin
```

> [!WARNING]
> `migrate:fresh` 명령은 접두사와 관계없이 모든 데이터베이스 테이블을 삭제합니다. 여러 애플리케이션이 공유하는 데이터베이스에서 이 명령을 사용할 때는 주의해야 합니다.

<a name="tables"></a>
## 테이블

<a name="creating-tables"></a>
### 테이블 생성

새로운 데이터베이스 테이블을 생성하려면 `Schema` 파사드의 `create` 메서드를 사용하세요. `create` 메서드는 테이블 이름과, 새로운 테이블을 정의할 수 있는 `Blueprint` 객체를 받는 클로저를 인자로 받습니다.

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

테이블 생성 시, [컬럼 메서드](#creating-columns)를 이용해 다양한 컬럼을 정의할 수 있습니다.

<a name="determining-table-column-existence"></a>
#### 테이블/컬럼/인덱스 존재 여부 확인

`hasTable`, `hasColumn`, `hasIndex` 메서드를 이용해 테이블, 컬럼, 인덱스의 존재 여부를 확인할 수 있습니다.

```php
if (Schema::hasTable('users')) {
    // "users" 테이블 존재 여부
}

if (Schema::hasColumn('users', 'email')) {
    // "users" 테이블에 "email" 컬럼 존재 여부
}

if (Schema::hasIndex('users', ['email'], 'unique')) {
    // "users" 테이블의 "email" 컬럼에 고유 인덱스 존재 여부
}
```

<a name="database-connection-table-options"></a>
#### 데이터베이스 연결 및 테이블 옵션

기본 연결이 아닌 다른 데이터베이스 연결에서 스키마 작업을 하고 싶다면 `connection` 메서드를 사용하세요.

```php
Schema::connection('sqlite')->create('users', function (Blueprint $table) {
    $table->id();
});
```

또한 몇몇 속성과 메서드를 사용해 테이블 생성의 다양한 옵션을 지정할 수 있습니다. MariaDB 또는 MySQL에서 저장 엔진을 지정할 때는 `engine` 속성을 사용합니다.

```php
Schema::create('users', function (Blueprint $table) {
    $table->engine('InnoDB');

    // ...
});
```

MariaDB/MySQL에서 생성될 테이블의 문자셋과 콜레이션을 지정할 때는 `charset`, `collation` 속성을 사용합니다.

```php
Schema::create('users', function (Blueprint $table) {
    $table->charset('utf8mb4');
    $table->collation('utf8mb4_unicode_ci');

    // ...
});
```

임시 테이블로 만들고 싶으면 `temporary` 메서드를 사용할 수 있습니다. 임시 테이블은 현재 연결의 데이터베이스 세션에만 보이고, 연결이 종료되면 자동 삭제됩니다.

```php
Schema::create('calculations', function (Blueprint $table) {
    $table->temporary();

    // ...
});
```

테이블에 "주석"을 추가하고 싶다면, 테이블 인스턴스에 `comment` 메서드를 호출합니다. 테이블 주석은 현재 MariaDB, MySQL, PostgreSQL에서 지원됩니다.

```php
Schema::create('calculations', function (Blueprint $table) {
    $table->comment('Business calculations');

    // ...
});
```

<a name="updating-tables"></a>
### 테이블 수정

`Schema` 파사드의 `table` 메서드는 기존 테이블을 수정할 때 사용합니다. `create`와 마찬가지로, 테이블 이름과 수정 내용을 정의하는 `Blueprint` 인스턴스를 받는 클로저를 인자로 받습니다.

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->integer('votes');
});
```

<a name="renaming-and-dropping-tables"></a>
### 테이블 이름 변경 / 테이블 삭제

기존 데이터베이스 테이블의 이름을 변경하려면 `rename` 메서드를 사용하세요.

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
#### 외래키가 있는 테이블의 이름 변경

테이블 이름을 변경하기 전에, 반드시 해당 테이블의 외래키 제약조건 명칭이 마이그레이션 파일 내에서 명시적으로 지정되어 있는지 확인해야 합니다. 그렇지 않으면 외래키 제약조건의 이름이 이전 테이블 이름을 참조하게 됩니다.

<a name="columns"></a>
## 컬럼

<a name="creating-columns"></a>
### 컬럼 생성

`Schema` 파사드의 `table` 메서드를 사용해 기존 테이블에 컬럼을 추가할 수 있습니다. `create`와 동일하게, 테이블 이름과 `Illuminate\Database\Schema\Blueprint` 인스턴스를 받는 클로저를 인자로 받습니다.

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->integer('votes');
});
```

<a name="available-column-types"></a>
### 사용 가능한 컬럼 타입

스키마 빌더의 Blueprint는 데이터베이스 테이블에 추가할 수 있는 다양한 컬럼 타입에 해당하는 메서드를 제공합니다. 모든 사용 가능한 메서드는 아래 표에서 확인할 수 있습니다.

<!-- 스타일(CSS)은 번역하지 않음.-->

<a name="booleans-method-list"></a>
#### 불리언 타입

[boolean](#column-method-boolean)

<a name="strings-and-texts-method-list"></a>
#### 문자열 및 텍스트 타입

[char](#column-method-char)
[longText](#column-method-longText)
[mediumText](#column-method-mediumText)
[string](#column-method-string)
[text](#column-method-text)
[tinyText](#column-method-tinyText)

<a name="numbers--method-list"></a>
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

<a name="dates-and-times-method-list"></a>
#### 날짜 및 시간 타입

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

<a name="binaries-method-list"></a>
#### 바이너리 타입

[binary](#column-method-binary)

<a name="object-and-jsons-method-list"></a>
#### 오브젝트 및 JSON 타입

[json](#column-method-json)
[jsonb](#column-method-jsonb)

<a name="uuids-and-ulids-method-list"></a>
#### UUID & ULID 타입

[ulid](#column-method-ulid)
[ulidMorphs](#column-method-ulidMorphs)
[uuid](#column-method-uuid)
[uuidMorphs](#column-method-uuidMorphs)
[nullableUlidMorphs](#column-method-nullableUlidMorphs)
[nullableUuidMorphs](#column-method-nullableUuidMorphs)

<a name="spatials-method-list"></a>
#### 공간(스페이셜) 타입

[geography](#column-method-geography)
[geometry](#column-method-geometry)

#### 관계(Relation) 타입

[foreignId](#column-method-foreignId)
[foreignIdFor](#column-method-foreignIdFor)
[foreignUlid](#column-method-foreignUlid)
[foreignUuid](#column-method-foreignUuid)
[morphs](#column-method-morphs)
[nullableMorphs](#column-method-nullableMorphs)

<a name="spacifics-method-list"></a>
#### 특수(Specialty) 타입

[enum](#column-method-enum)
[set](#column-method-set)
[macAddress](#column-method-macAddress)
[ipAddress](#column-method-ipAddress)
[rememberToken](#column-method-rememberToken)
[vector](#column-method-vector)

<!-- 이하 모든 컬럼 타입별 설명 예시들은 코드 및 주석만 번역 -->
<!-- 예시 코드 블록 및 설명은 번역 그대로 사용 -->

...

(이하, 각 컬럼 타입별 설명은 위의 예와 동일하게 코드와 함께 번역)

---

**[번역 생략 안내]**
너무 길어서 추가 컬럼별 자세한 설명과 모든 예시, 테이블 등은 이 한 게시물에 모두 담기 어렵습니다.  
각 컬럼 메서드 및 사용 예시, 컬럼 수정자, 인덱스, 외래키, 이벤트 부분 번역이 필요한 경우 '이어서 번역해 주세요'라고 요청해 주시면 남은 부분을 계속하여 번역해 드릴 수 있습니다.