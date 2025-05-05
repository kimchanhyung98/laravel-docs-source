# 데이터베이스: 시작하기

- [소개](#introduction)
    - [설정](#configuration)
    - [읽기와 쓰기 연결](#read-and-write-connections)
- [SQL 쿼리 실행](#running-queries)
    - [다중 데이터베이스 연결 사용](#using-multiple-database-connections)
    - [쿼리 이벤트 리스닝](#listening-for-query-events)
    - [누적 쿼리 시간 모니터링](#monitoring-cumulative-query-time)
- [데이터베이스 트랜잭션](#database-transactions)
- [데이터베이스 CLI 연결](#connecting-to-the-database-cli)
- [데이터베이스 검사](#inspecting-your-databases)
- [데이터베이스 모니터링](#monitoring-your-databases)

<a name="introduction"></a>
## 소개

대부분의 현대 웹 애플리케이션은 데이터베이스와 상호작용합니다. Laravel은 다양한 데이터베이스를 지원하며, 원시 SQL, [플루언트 쿼리 빌더](/docs/{{version}}/queries), 그리고 [Eloquent ORM](/docs/{{version}}/eloquent)를 통해 데이터베이스와 쉽게 상호작용할 수 있도록 도와줍니다. 현재 Laravel은 다음 다섯 가지 데이터베이스를 공식적으로 지원합니다:

<div class="content-list" markdown="1">

- MariaDB 10.3 이상 ([버전 정책](https://mariadb.org/about/#maintenance-policy))
- MySQL 5.7 이상 ([버전 정책](https://en.wikipedia.org/wiki/MySQL#Release_history))
- PostgreSQL 10.0 이상 ([버전 정책](https://www.postgresql.org/support/versioning/))
- SQLite 3.26.0 이상
- SQL Server 2017 이상 ([버전 정책](https://docs.microsoft.com/en-us/lifecycle/products/?products=sql-server))

</div>

또한 MongoDB는 공식적으로 MongoDB에서 관리하는 `mongodb/laravel-mongodb` 패키지를 통해 지원됩니다. 자세한 내용은 [Laravel MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/) 문서를 참고하세요.

<a name="configuration"></a>
### 설정

Laravel의 데이터베이스 서비스 설정은 애플리케이션의 `config/database.php` 파일에 위치합니다. 이 파일에서 모든 데이터베이스 연결을 정의할 수 있으며, 기본적으로 사용할 연결을 지정할 수 있습니다. 이 파일 내 대부분의 설정 옵션은 애플리케이션의 환경 변수 값을 기반으로 합니다. 대부분의 Laravel 지원 데이터베이스 시스템에 대한 예시가 이 파일에 제공되어 있습니다.

기본적으로, Laravel의 샘플 [환경 설정](/docs/{{version}}/configuration#environment-configuration)은 [Laravel Sail](/docs/{{version}}/sail)과 함께 즉시 사용할 수 있습니다. Laravel Sail은 로컬 환경에서 Laravel 애플리케이션을 개발할 때 사용하는 Docker 설정입니다. 하지만 필요에 따라 로컬 데이터베이스에 맞게 설정을 자유롭게 변경할 수 있습니다.

<a name="sqlite-configuration"></a>
#### SQLite 설정

SQLite 데이터베이스는 파일 시스템의 단일 파일에 저장됩니다. 터미널에서 `touch database/database.sqlite` 명령어를 사용해 새로운 SQLite 데이터베이스를 생성할 수 있습니다. 데이터베이스가 생성된 후, 환경 변수 `DB_DATABASE`에 데이터베이스의 절대 경로를 지정하면 해당 데이터베이스를 쉽게 사용할 수 있습니다:

```ini
DB_CONNECTION=sqlite
DB_DATABASE=/absolute/path/to/database.sqlite
```

기본적으로 SQLite 연결은 외래 키 제약 조건이 활성화되어 있습니다. 이를 비활성화하려면 `DB_FOREIGN_KEYS` 환경 변수를 `false`로 설정하면 됩니다:

```ini
DB_FOREIGN_KEYS=false
```

> [!NOTE]
> [Laravel 설치 프로그램](/docs/{{version}}/installation#creating-a-laravel-project)으로 애플리케이션을 생성하고 데이터베이스로 SQLite를 선택하면, Laravel이 자동으로 `database/database.sqlite` 파일을 생성하고 기본 [데이터베이스 마이그레이션](/docs/{{version}}/migrations)을 실행합니다.

<a name="mssql-configuration"></a>
#### Microsoft SQL Server 설정

Microsoft SQL Server 데이터베이스를 사용하려면, `sqlsrv` 및 `pdo_sqlsrv` PHP 확장과 이를 위해 필요한 Microsoft SQL ODBC 드라이버 등 의존성이 설치되어 있어야 합니다.

<a name="configuration-using-urls"></a>
#### URL을 이용한 설정

일반적으로 데이터베이스 연결은 `host`, `database`, `username`, `password` 등 여러 설정 값으로 구성됩니다. 각 값들은 별도의 환경 변수로 지정해야 하므로, 운영 서버에서 데이터베이스 연결 정보를 관리할 때 여러 환경 변수를 관리해야 합니다.

AWS와 Heroku와 같은 관리형 데이터베이스 제공업체는 데이터베이스 연결에 필요한 모든 정보를 하나의 "URL"로 제공하기도 합니다. 데이터베이스 URL 예시는 다음과 같습니다:

```html
mysql://root:password@127.0.0.1/forge?charset=UTF-8
```

이러한 URL은 일반적으로 다음과 같은 스키마를 따릅니다:

```html
driver://username:password@host:port/database?options
```

편의를 위해, Laravel은 여러 설정 옵션을 개별적으로 구성하는 대신 이러한 URL을 사용할 수 있습니다. 만약 `url` 옵션(또는 환경 변수 `DB_URL`)이 존재할 경우, 해당 URL에서 연결 및 자격 정보를 추출하여 사용합니다.

<a name="read-and-write-connections"></a>
### 읽기와 쓰기 연결

때때로 SELECT 쿼리는 한 데이터베이스 연결을, 그리고 INSERT, UPDATE, DELETE 쿼리는 다른 연결을 사용하고 싶을 수 있습니다. Laravel은 이 작업을 아주 쉽게 처리하며, 원시 쿼리, 쿼리 빌더 또는 Eloquent ORM 어떤 것을 사용할 때도 올바른 연결을 사용합니다.

읽기/쓰기 연결 설정 예시는 다음과 같습니다:

```php
'mysql' => [
    'read' => [
        'host' => [
            '192.168.1.1',
            '196.168.1.2',
        ],
    ],
    'write' => [
        'host' => [
            '196.168.1.3',
        ],
    ],
    'sticky' => true,

    'database' => env('DB_DATABASE', 'laravel'),
    'username' => env('DB_USERNAME', 'root'),
    'password' => env('DB_PASSWORD', ''),
    'unix_socket' => env('DB_SOCKET', ''),
    'charset' => env('DB_CHARSET', 'utf8mb4'),
    'collation' => env('DB_COLLATION', 'utf8mb4_unicode_ci'),
    'prefix' => '',
    'prefix_indexes' => true,
    'strict' => true,
    'engine' => null,
    'options' => extension_loaded('pdo_mysql') ? array_filter([
        PDO::MYSQL_ATTR_SSL_CA => env('MYSQL_ATTR_SSL_CA'),
    ]) : [],
],
```

설정 배열에 `read`, `write`, `sticky` 키 세 개가 추가된 것을 볼 수 있습니다. `read`와 `write` 키는 `host`라는 단일 키를 가진 배열 값을 가지고 있습니다. `read`와 `write` 연결의 나머지 데이터베이스 옵션은 기본 `mysql` 설정 배열에서 병합됩니다.

기본 배열의 값을 오버라이드하고 싶을 때만 `read`, `write` 배열에 값을 추가하면 됩니다. 이 예시에서 `"read"` 연결의 호스트로는 `192.168.1.1`이, `"write"` 연결에는 `192.168.1.3`이 사용됩니다. 데이터베이스 자격 증명, 프리픽스, 문자셋 및 기타 모든 옵션은 두 연결에서 공유됩니다. 만약 `host` 옵션에 여러 값이 존재하면, 각 요청마다 무작위로 하나의 호스트가 선택됩니다.

<a name="the-sticky-option"></a>
#### `sticky` 옵션

`sticky` 옵션은 *선택적* 값이며, 현재 요청 주기 동안 데이터베이스에 쓰기 작업이 발생하면 즉시 같은 연결에서 읽기 작업을 가능하게 합니다. 즉, `sticky` 옵션이 활성화되어 있고, 해당 요청에서 "쓰기" 작업이 한 번이라도 발생한 경우 이후의 "읽기" 작업은 "쓰기" 연결을 사용합니다. 이를 통해 동일한 요청에서 갓 작성한 데이터를 즉시 읽어올 수 있습니다. 이 동작이 원하는 것인지는 애플리케이션 상황에 맞추어 결정하세요.

<a name="running-queries"></a>
## SQL 쿼리 실행

데이터베이스 연결을 설정한 후에는 `DB` 파사드를 사용하여 쿼리를 실행할 수 있습니다. `DB` 파사드는 각각의 쿼리 유형에 대해 `select`, `update`, `insert`, `delete`, `statement` 메서드를 제공합니다.

<a name="running-a-select-query"></a>
#### Select 쿼리 실행

기본 SELECT 쿼리를 실행하려면 `DB` 파사드의 `select` 메서드를 사용할 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\DB;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * 애플리케이션의 모든 사용자 목록을 표시합니다.
     */
    public function index(): View
    {
        $users = DB::select('select * from users where active = ?', [1]);

        return view('user.index', ['users' => $users]);
    }
}
```

`select` 메서드의 첫 번째 인수는 SQL 쿼리이며, 두 번째 인수는 쿼리에 바인딩할 파라미터 배열입니다. 보통 `where` 절에 들어갈 값이 이에 해당됩니다. 파라미터 바인딩은 SQL 인젝션 공격으로부터 보호해 줍니다.

`select` 메서드는 항상 결과의 배열을 반환합니다. 배열의 각 원소는 데이터베이스 레코드를 나타내는 PHP `stdClass` 객체입니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::select('select * from users');

foreach ($users as $user) {
    echo $user->name;
}
```

<a name="selecting-scalar-values"></a>
#### 스칼라 값 선택

쿼리 결과가 단일 스칼라 값(예: 카운트, 합계 등)일 때, Laravel의 `scalar` 메서드를 통해 값을 직접 반환받을 수 있습니다:

```php
$burgers = DB::scalar(
    "select count(case when food = 'burger' then 1 end) as burgers from menu"
);
```

<a name="selecting-multiple-result-sets"></a>
#### 다중 결과 집합 선택

저장 프로시저 실행 등으로 여러 결과 집합을 반환받는 경우, `selectResultSets` 메서드를 사용하여 모든 결과 집합을 받을 수 있습니다:

```php
[$options, $notifications] = DB::selectResultSets(
    "CALL get_user_options_and_notifications(?)", $request->user()->id
);
```

<a name="using-named-bindings"></a>
#### 명명된 바인딩 사용

`?` 대신 명명된 바인딩을 사용해 쿼리를 실행할 수 있습니다:

```php
$results = DB::select('select * from users where id = :id', ['id' => 1]);
```

<a name="running-an-insert-statement"></a>
#### Insert 문 실행

`insert`문을 실행하려면 `DB` 파사드의 `insert` 메서드를 사용합니다. `select`와 마찬가지로 첫 번째 인수는 쿼리, 두 번째 인수는 바인딩 값입니다:

```php
use Illuminate\Support\Facades\DB;

DB::insert('insert into users (id, name) values (?, ?)', [1, 'Marc']);
```

<a name="running-an-update-statement"></a>
#### Update 문 실행

데이터베이스의 기존 레코드를 수정하려면 `update` 메서드를 사용합니다. 이 메서드는 영향받은 행의 수를 반환합니다:

```php
use Illuminate\Support\Facades\DB;

$affected = DB::update(
    'update users set votes = 100 where name = ?',
    ['Anita']
);
```

<a name="running-a-delete-statement"></a>
#### Delete 문 실행

레코드를 삭제하려면 `delete` 메서드를 사용합니다. 이 메서드 역시 영향받은 행의 수를 반환합니다:

```php
use Illuminate\Support\Facades\DB;

$deleted = DB::delete('delete from users');
```

<a name="running-a-general-statement"></a>
#### 일반적인 문 실행

값을 반환하지 않는 데이터베이스 명령에는 `DB` 파사드의 `statement` 메서드를 사용할 수 있습니다:

```php
DB::statement('drop table users');
```

<a name="running-an-unprepared-statement"></a>
#### 준비되지 않은(바인딩 없는) 문 실행

값을 바인딩하지 않고 SQL을 실행하고 싶을 때는 `DB` 파사드의 `unprepared` 메서드를 사용할 수 있습니다:

```php
DB::unprepared('update users set votes = 100 where name = "Dries"');
```

> [!WARNING]
> unprepared 문은 파라미터 바인딩을 하지 않으므로 SQL 인젝션에 취약할 수 있습니다. 사용자 입력값을 unprepared 문에 절대 포함하지 마세요.

<a name="implicit-commits-in-transactions"></a>
#### 암묵적 커밋

트랜잭션 내에서 `statement`와 `unprepared` 메서드를 사용할 때, [암묵적 커밋](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html)을 유발하는 명령을 피해야 합니다. 암묵적 커밋을 유발하는 명령문은 트랜잭션 전체를 강제로 커밋하여, Laravel이 트랜잭션 레벨을 제대로 인식하지 못하게 합니다. 예를 들어 테이블 생성 명령이 이에 해당됩니다:

```php
DB::unprepared('create table a (col varchar(1) null)');
```

암묵적 커밋을 유발하는 모든 명령어 목록은 MySQL 매뉴얼에서 확인하세요. [해당 목록 보기](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html)

<a name="using-multiple-database-connections"></a>
### 다중 데이터베이스 연결 사용

애플리케이션의 `config/database.php` 파일에 여러 연결이 정의되어 있다면, `DB` 파사드의 `connection` 메서드로 각 연결에 접근할 수 있습니다. 이 때 인수로 넘기는 연결명은 `config/database.php`에 정의된 연결명이어야 하며, 실행 중에 `config` 헬퍼로 동적으로 지정할 수도 있습니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::connection('sqlite')->select(/* ... */);
```

연결 인스턴스의 `getPdo` 메서드를 통해 원시 PDO 인스턴스에 접근할 수도 있습니다:

```php
$pdo = DB::connection()->getPdo();
```

<a name="listening-for-query-events"></a>
### 쿼리 이벤트 리스닝

애플리케이션에서 실행되는 모든 SQL 쿼리에 대해 호출되는 클로저를 지정하고 싶다면, `DB` 파사드의 `listen` 메서드를 사용할 수 있습니다. 이 메서드는 로그 기록이나 디버깅에 유용합니다. 쿼리 리스너 클로저는 [서비스 프로바이더](/docs/{{version}}/providers)의 `boot` 메서드에서 등록할 수 있습니다:

```php
<?php

namespace App\Providers;

use Illuminate\Database\Events\QueryExecuted;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 모든 애플리케이션 서비스를 등록합니다.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * 모든 애플리케이션 서비스를 부트스트랩합니다.
     */
    public function boot(): void
    {
        DB::listen(function (QueryExecuted $query) {
            // $query->sql;
            // $query->bindings;
            // $query->time;
            // $query->toRawSql();
        });
    }
}
```

<a name="monitoring-cumulative-query-time"></a>
### 누적 쿼리 시간 모니터링

현대 웹 애플리케이션의 성능 병목 원인 중 하나는 데이터베이스 쿼리 시간이 오래 걸리는 경우입니다. Laravel은 요청 중 데이터베이스 쿼리 시간이 일정 임계치(밀리초)를 초과할 때 지정한 클로저나 콜백을 호출할 수 있습니다. 이를 위해서는 `whenQueryingForLongerThan` 메서드에 임계값과 클로저를 지정하여 서비스 프로바이더의 `boot` 메서드에서 호출하면 됩니다:

```php
<?php

namespace App\Providers;

use Illuminate\Database\Connection;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\ServiceProvider;
use Illuminate\Database\Events\QueryExecuted;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 모든 애플리케이션 서비스를 등록합니다.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * 모든 애플리케이션 서비스를 부트스트랩합니다.
     */
    public function boot(): void
    {
        DB::whenQueryingForLongerThan(500, function (Connection $connection, QueryExecuted $event) {
            // 개발팀에 알림 전송 등...
        });
    }
}
```

<a name="database-transactions"></a>
## 데이터베이스 트랜잭션

`DB` 파사드의 `transaction` 메서드를 사용하면 데이터베이스 트랜잭션 내에서 일련의 작업을 실행할 수 있습니다. 트랜잭션 클로저 내에서 예외가 발생하면 자동으로 롤백되고, 예외가 다시 발생합니다. 클로저가 정상적으로 실행되면 자동으로 커밋됩니다. 직접 롤백 또는 커밋을 신경 쓸 필요가 없습니다:

```php
use Illuminate\Support\Facades\DB;

DB::transaction(function () {
    DB::update('update users set votes = 1');

    DB::delete('delete from posts');
});
```

<a name="handling-deadlocks"></a>
#### 데드락(교착상태) 처리

`transaction` 메서드는 두 번째 선택적 인수로 데드락이 발생했을 때 트랜잭션을 재시도할 횟수를 지정할 수 있습니다. 이 횟수가 소진되면 예외가 발생합니다:

```php
use Illuminate\Support\Facades\DB;

DB::transaction(function () {
    DB::update('update users set votes = 1');

    DB::delete('delete from posts');
}, 5);
```

<a name="manually-using-transactions"></a>
#### 트랜잭션 직접 사용

트랜잭션을 수동으로 시작하고, 커밋/롤백까지 직접 제어하려면 `DB` 파사드의 `beginTransaction` 메서드를 사용하면 됩니다:

```php
use Illuminate\Support\Facades\DB;

DB::beginTransaction();
```

트랜잭션을 롤백하려면 `rollBack` 메서드를 사용하세요:

```php
DB::rollBack();
```

마지막으로 트랜잭션을 커밋하려면 `commit` 메서드를 사용하세요:

```php
DB::commit();
```

> [!NOTE]
> `DB` 파사드의 트랜잭션 메서드는 [쿼리 빌더](/docs/{{version}}/queries)와 [Eloquent ORM](/docs/{{version}}/eloquent) 모두에 대해 동작합니다.

<a name="connecting-to-the-database-cli"></a>
## 데이터베이스 CLI 연결

데이터베이스의 CLI에 접속하고 싶을 경우, `db` 아티즌 명령어를 사용할 수 있습니다:

```shell
php artisan db
```

필요하다면 기본 연결이 아닌 특정 데이터베이스 연결을 지정해 접속할 수 있습니다:

```shell
php artisan db mysql
```

<a name="inspecting-your-databases"></a>
## 데이터베이스 검사

`db:show`와 `db:table` 아티즌 명령어를 사용하여 데이터베이스 및 관련 테이블에 대한 유용한 정보를 얻을 수 있습니다. 데이터베이스의 전체 개요(크기, 타입, 열린 연결 수, 테이블 요약 등)를 확인하려면 `db:show` 명령어를 사용하세요:

```shell
php artisan db:show
```

어느 데이터베이스 연결을 검사할 것인지는 `--database` 옵션을 통해 연결명을 지정할 수 있습니다:

```shell
php artisan db:show --database=pgsql
```

명령어 출력에 테이블 행의 개수 또는 뷰 정보를 포함시키려면 각각 `--counts`, `--views` 옵션을 사용할 수 있습니다. 대용량 데이터베이스에서는 행 개수와 뷰 정보를 조회하는 데 시간이 오래 걸릴 수 있습니다:

```shell
php artisan db:show --counts --views
```

또한 다음과 같은 `Schema` 메서드로 데이터베이스를 자세히 검사할 수 있습니다:

```php
use Illuminate\Support\Facades\Schema;

$tables = Schema::getTables();
$views = Schema::getViews();
$columns = Schema::getColumns('users');
$indexes = Schema::getIndexes('users');
$foreignKeys = Schema::getForeignKeys('users');
```

애플리케이션의 기본 연결이 아닌 특정 연결을 검사하고 싶다면 `connection` 메서드를 사용하면 됩니다:

```php
$columns = Schema::connection('sqlite')->getColumns('users');
```

<a name="table-overview"></a>
#### 테이블 개요

특정 테이블에 대한 개요 정보를 얻고 싶으면 `db:table` 아티즌 명령어를 실행하세요. 이 명령어는 테이블의 컬럼, 타입, 속성, 키, 인덱스에 대한 정보를 제공합니다:

```shell
php artisan db:table users
```

<a name="monitoring-your-databases"></a>
## 데이터베이스 모니터링

`db:monitor` 아티즌 명령어를 사용하면 데이터베이스가 설정한 최대 오픈 연결 수를 초과할 경우 `Illuminate\Database\Events\DatabaseBusy` 이벤트가 디스패치되도록 할 수 있습니다.

먼저 [매분마다 실행](/docs/{{version}}/scheduling)되도록 `db:monitor` 명령어를 예약하세요. 이 명령어는 모니터링할 데이터베이스 연결명과, 이벤트가 발생하기 전 허용할 최대 오픈 연결 수를 인수로 받습니다:

```shell
php artisan db:monitor --databases=mysql,pgsql --max=100
```

이 명령만 예약하면 알림이 자동으로 전송되지는 않습니다. 임계값을 초과하는 데이터베이스가 발견되면 `DatabaseBusy` 이벤트가 발생하며, 애플리케이션의 `AppServiceProvider`에서 이 이벤트를 청취하여 개발팀 등에게 알림을 전송할 수 있습니다:

```php
use App\Notifications\DatabaseApproachingMaxConnections;
use Illuminate\Database\Events\DatabaseBusy;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\Facades\Notification;

/**
 * 모든 애플리케이션 서비스를 부트스트랩합니다.
 */
public function boot(): void
{
    Event::listen(function (DatabaseBusy $event) {
        Notification::route('mail', 'dev@example.com')
            ->notify(new DatabaseApproachingMaxConnections(
                $event->connectionName,
                $event->connections
            ));
    });
}
```
