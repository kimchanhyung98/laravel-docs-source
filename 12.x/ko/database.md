# 데이터베이스: 시작하기 (Database: Getting Started)

- [소개](#introduction)
    - [설정](#configuration)
    - [읽기 및 쓰기 연결](#read-and-write-connections)
- [SQL 쿼리 실행](#running-queries)
    - [여러 데이터베이스 연결 사용](#using-multiple-database-connections)
    - [쿼리 이벤트 리스닝](#listening-for-query-events)
    - [누적 쿼리 시간 모니터링](#monitoring-cumulative-query-time)
- [데이터베이스 트랜잭션](#database-transactions)
- [데이터베이스 CLI 접속](#connecting-to-the-database-cli)
- [데이터베이스 점검](#inspecting-your-databases)
- [데이터베이스 모니터링](#monitoring-your-databases)

<a name="introduction"></a>
## 소개 (Introduction)

대부분의 최신 웹 애플리케이션은 데이터베이스와 상호작용합니다. Laravel은 지원하는 다양한 데이터베이스에 대해 원시 SQL, [플루언트 쿼리 빌더](/docs/12.x/queries), 그리고 [Eloquent ORM](/docs/12.x/eloquent)을 이용해 매우 간단하게 데이터베이스와 상호작용할 수 있도록 해줍니다. 현재 Laravel은 아래의 다섯 가지 데이터베이스에 대해 1차로 지원을 제공합니다:

<div class="content-list" markdown="1">

- MariaDB 10.3+ ([버전 정책](https://mariadb.org/about/#maintenance-policy))
- MySQL 5.7+ ([버전 정책](https://en.wikipedia.org/wiki/MySQL#Release_history))
- PostgreSQL 10.0+ ([버전 정책](https://www.postgresql.org/support/versioning/))
- SQLite 3.26.0+
- SQL Server 2017+ ([버전 정책](https://docs.microsoft.com/en-us/lifecycle/products/?products=sql-server))

</div>

추가로, MongoDB는 공식적으로 MongoDB에서 유지 관리하는 `mongodb/laravel-mongodb` 패키지를 통해 지원됩니다. 자세한 내용은 [Laravel MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/) 문서를 참고하세요.

<a name="configuration"></a>
### 설정 (Configuration)

Laravel의 데이터베이스 서비스에 대한 설정은 애플리케이션의 `config/database.php` 설정 파일에 위치합니다. 이 파일 안에서 모든 데이터베이스 연결을 정의할 수 있으며, 기본적으로 어떤 연결을 사용할 지도 지정할 수 있습니다. 대부분의 설정 옵션은 애플리케이션의 환경 변수 값을 기반으로 동작합니다. 이 파일에는 Laravel이 지원하는 대부분 데이터베이스 시스템에 대한 예시가 포함되어 있습니다.

기본적으로, Laravel의 샘플 [환경 설정](/docs/12.x/configuration#environment-configuration)은 [Laravel Sail](/docs/12.x/sail)과 함께 사용할 수 있도록 준비되어 있습니다. Sail은 로컬 머신에서 Laravel 애플리케이션을 개발할 수 있는 Docker 설정입니다. 그러나 필요에 따라 로컬 데이터베이스에 맞게 데이터베이스 설정을 자유롭게 변경할 수 있습니다.

<a name="sqlite-configuration"></a>
#### SQLite 설정

SQLite 데이터베이스는 파일 시스템의 단일 파일로 구성되어 있습니다. 터미널에서 `touch` 명령어를 사용하여 새 SQLite 데이터베이스를 생성할 수 있습니다: `touch database/database.sqlite`. 데이터베이스를 생성한 후, 환경 변수의 `DB_DATABASE` 항목에 데이터베이스의 절대 경로를 지정하면 해당 데이터베이스를 쉽게 사용할 수 있습니다:

```ini
DB_CONNECTION=sqlite
DB_DATABASE=/absolute/path/to/database.sqlite
```

기본적으로, SQLite 연결에는 외래 키 제약 조건이 활성화되어 있습니다. 이를 비활성화하려면 `DB_FOREIGN_KEYS` 환경 변수를 `false`로 설정하면 됩니다:

```ini
DB_FOREIGN_KEYS=false
```

> [!NOTE]
> [Laravel 인스톨러](/docs/12.x/installation#creating-a-laravel-project)로 애플리케이션을 생성할 때 데이터베이스로 SQLite를 선택하면, Laravel이 자동으로 `database/database.sqlite` 파일을 생성하고 기본 [데이터베이스 마이그레이션](/docs/12.x/migrations)을 실행합니다.

<a name="mssql-configuration"></a>
#### Microsoft SQL Server 설정

Microsoft SQL Server 데이터베이스를 사용하려면, `sqlsrv` 및 `pdo_sqlsrv` PHP 확장 프로그램과 이 확장 프로그램들이 필요로 하는 Microsoft SQL ODBC 드라이버 같은 의존성도 설치되어 있어야 합니다.

<a name="configuration-using-urls"></a>
#### URL을 활용한 설정

일반적으로 데이터베이스 연결은 `host`, `database`, `username`, `password` 등의 여러 설정 값을 이용해 구성합니다. 각각의 설정 값은 환경 변수로 분리되어 있습니다. 즉, 운영 서버에서 데이터베이스 연결 정보를 구성할 때 여러 환경 변수를 관리해야 합니다.

AWS, Heroku와 같은 일부 관리형 데이터베이스 공급자는 데이터베이스의 모든 연결 정보를 하나의 문자열로 담은 "URL"을 제공합니다. 예시로 아래와 같은 데이터베이스 URL이 있을 수 있습니다:

```html
mysql://root:password@127.0.0.1/forge?charset=UTF-8
```

이러한 URL은 일반적으로 다음과 같이 표준 스키마 형식을 따릅니다:

```html
driver://username:password@host:port/database?options
```

편의를 위해, Laravel은 여러 설정 값을 사용하지 않고 이 URL만으로 데이터베이스를 설정하는 방법도 지원합니다. `url`(또는 `DB_URL` 환경 변수) 설정 옵션이 있으면 해당 값을 읽어 연결 및 인증 정보를 추출하여 사용합니다.

<a name="read-and-write-connections"></a>
### 읽기 및 쓰기 연결 (Read and Write Connections)

경우에 따라 SELECT 구문은 한 데이터베이스 연결을, INSERT/UPDATE/DELETE 구문은 다른 연결을 사용하고 싶을 수 있습니다. Laravel에서는 이를 매우 쉽게 설정할 수 있으며, 원시 쿼리, 쿼리 빌더, Eloquent ORM을 사용할 때 항상 적절한 연결이 자동으로 사용됩니다.

읽기/쓰기 연결을 어떻게 설정하는지 예시를 봅시다:

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

위 설정 배열에는 `read`, `write`, `sticky`라는 세 가지 키가 추가된 점에 주목하세요. `read`와 `write`는 각각 하나의 키(`host`)를 포함하는 배열 값입니다. `read`와 `write` 연결에 대한 나머지 데이터베이스 옵션들은 기본 `mysql` 설정 배열에서 병합합니다.

만약 `read`와 `write` 배열에서 기본 값과 다르게 설정하고 싶은 항목이 있다면, 해당 배열에만 추가하면 됩니다. 예시에서는 "읽기" 연결에는 `192.168.1.1`이, "쓰기" 연결에는 `192.168.1.3`이 호스트로 사용됩니다. 데이터베이스 자격 증명, 프리픽스, 문자셋 등 주 설정 값들은 두 연결 모두에 적용됩니다. 만약 호스트 배열에 여러 개가 있으면, 매 요청마다 무작위로 하나가 선택되어 사용됩니다.

<a name="the-sticky-option"></a>
#### `sticky` 옵션

`sticky` 옵션은 *선택적* 값이며, 현재 요청 사이클에서 데이터베이스에 기록(write)된 내용을 즉시 읽을 수 있도록 하는 역할을 합니다. 이 옵션이 활성화되고 현재 요청 중에 "쓰기" 작업이 발생했다면, 이후 "읽기" 작업에서도 "쓰기" 연결을 사용하게 됩니다. 이를 통해 동일한 요청 안에서 갓 쓰여진 데이터를 바로 조회할 수 있습니다. 해당 동작이 애플리케이션에 필요한지 판단하여 사용할지 결정하세요.

<a name="running-queries"></a>
## SQL 쿼리 실행 (Running SQL Queries)

데이터베이스 연결을 설정한 후, `DB` 파사드를 통해 쿼리를 실행할 수 있습니다. `DB` 파사드는 `select`, `update`, `insert`, `delete`, `statement` 등 각종 쿼리 유형에 대한 메서드를 제공합니다.

<a name="running-a-select-query"></a>
#### SELECT 쿼리 실행

기본 SELECT 쿼리를 실행하려면 `DB` 파사드의 `select` 메서드를 사용할 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\DB;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * Show a list of all of the application's users.
     */
    public function index(): View
    {
        $users = DB::select('select * from users where active = ?', [1]);

        return view('user.index', ['users' => $users]);
    }
}
```

`select` 메서드의 첫 번째 인수는 SQL 쿼리 문자열이며, 두 번째 인수는 쿼리에 바인딩할 파라미터 배열입니다. 일반적으로 이는 WHERE 절의 조건값들이 들어갑니다. 파라미터 바인딩을 통해 SQL 인젝션을 예방할 수 있습니다.

`select` 메서드는 항상 결과를 `array`로 반환하며, 배열의 각 항목은 데이터베이스의 한 레코드를 나타내는 PHP `stdClass` 객체입니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::select('select * from users');

foreach ($users as $user) {
    echo $user->name;
}
```

<a name="selecting-scalar-values"></a>
#### 스칼라 값 조회

경우에 따라 쿼리 결과가 하나의 스칼라 값(단일 숫자나 문자열)만 반환될 수 있습니다. 이때에는 결과 레코드에서 값을 꺼내지 않고, `scalar` 메서드를 통해 바로 값을 얻을 수 있습니다:

```php
$burgers = DB::scalar(
    "select count(case when food = 'burger' then 1 end) as burgers from menu"
);
```

<a name="selecting-multiple-result-sets"></a>
#### 여러 결과 집합 조회

애플리케이션에서 여러 결과 집합을 반환하는 저장 프로시저를 호출하는 경우, `selectResultSets` 메서드를 사용하여 반환된 모든 결과 집합을 가져올 수 있습니다:

```php
[$options, $notifications] = DB::selectResultSets(
    "CALL get_user_options_and_notifications(?)", $request->user()->id
);
```

<a name="using-named-bindings"></a>
#### 네임드 바인딩 사용

파라미터 바인딩에 `?` 대신 명명된 바인딩을 사용할 수도 있습니다:

```php
$results = DB::select('select * from users where id = :id', ['id' => 1]);
```

<a name="running-an-insert-statement"></a>
#### INSERT 구문 실행

`insert` 구문을 실행하려면, `DB` 파사드의 `insert` 메서드를 사용할 수 있습니다. `select`와 마찬가지로 첫 번째 인수는 SQL 쿼리이며, 두 번째 인수는 바인딩 값 배열입니다:

```php
use Illuminate\Support\Facades\DB;

DB::insert('insert into users (id, name) values (?, ?)', [1, 'Marc']);
```

<a name="running-an-update-statement"></a>
#### UPDATE 구문 실행

이미 존재하는 레코드를 수정하려면, `update` 메서드를 사용합니다. 이 메서드는 영향을 받은 행(row)의 개수를 반환합니다.

```php
use Illuminate\Support\Facades\DB;

$affected = DB::update(
    'update users set votes = 100 where name = ?',
    ['Anita']
);
```

<a name="running-a-delete-statement"></a>
#### DELETE 구문 실행

데이터베이스에서 레코드를 삭제하려면 `delete` 메서드를 사용합니다. `update`와 마찬가지로 삭제된 행의 개수를 반환합니다.

```php
use Illuminate\Support\Facades\DB;

$deleted = DB::delete('delete from users');
```

<a name="running-a-general-statement"></a>
#### 일반적인 쿼리 실행

값을 반환하지 않는 데이터베이스 구문에는 `statement` 메서드를 사용할 수 있습니다:

```php
DB::statement('drop table users');
```

<a name="running-an-unprepared-statement"></a>
#### 비바인딩 쿼리 실행

가끔은 파라미터 바인딩을 사용하지 않고 SQL 구문을 실행하고 싶을 수 있습니다. 이 경우 `DB` 파사드의 `unprepared` 메서드를 사용합니다:

```php
DB::unprepared('update users set votes = 100 where name = "Dries"');
```

> [!WARNING]
> 비바인딩 쿼리는 파라미터 바인딩을 사용하지 않으므로 SQL 인젝션에 취약할 수 있습니다. 절대로 사용자 입력 값을 비바인딩 구문에 직접 넣으면 안 됩니다.

<a name="implicit-commits-in-transactions"></a>
#### 암묵적 커밋 처리

트랜잭션 내에서 `DB` 파사드의 `statement` 또는 `unprepared` 메서드를 사용할 때, [암묵적 커밋](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html)을 유발하는 구문은 주의해서 사용해야 합니다. 이런 구문은 데이터베이스 엔진이 트랜잭션 전체를 자동으로 커밋하게 만들 수 있으므로, Laravel은 현재 트랜잭션 레벨을 인식하지 못하게 됩니다. 예시로 테이블 생성과 같은 명령이 대표적입니다:

```php
DB::unprepared('create table a (col varchar(1) null)');
```

암묵적 커밋이 발생하는 구문의 전체 목록은 MySQL 매뉴얼의 [관련 페이지](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html)를 참고하세요.

<a name="using-multiple-database-connections"></a>
### 여러 데이터베이스 연결 사용

애플리케이션에서 `config/database.php` 파일에 여러 연결을 정의한 경우, `DB` 파사드의 `connection` 메서드를 통해 각 연결에 접근할 수 있습니다. 이때, `connection` 메서드의 인수로 연결명을 전달하는데, 이것은 설정 파일에 정의된 연결명 또는 런타임에 `config` 헬퍼로 등록된 연결명이어야 합니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::connection('sqlite')->select(/* ... */);
```

연결 인스턴스의 `getPdo` 메서드를 통해 해당 연결의 원시 PDO 인스턴스에 직접 접근할 수도 있습니다:

```php
$pdo = DB::connection()->getPdo();
```

<a name="listening-for-query-events"></a>
### 쿼리 이벤트 리스닝

애플리케이션에서 발생하는 각 SQL 쿼리에 대해 호출되는 클로저를 지정하고 싶다면, `DB` 파사드의 `listen` 메서드를 사용할 수 있습니다. 이 방법은 쿼리 로깅이나 디버깅에 유용합니다. 쿼리 리스너 클로저는 [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에 등록할 수 있습니다:

```php
<?php

namespace App\Providers;

use Illuminate\Database\Events\QueryExecuted;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * Bootstrap any application services.
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

현대 웹 애플리케이션에서 자주 발생하는 성능 병목 중 하나는 데이터베이스 쿼리에 소요되는 시간입니다. Laravel에서는 요청 하나 당 데이터베이스 쿼리에 너무 많은 시간이 소요될 때, 이를 감지하여 지정한 클로저(혹은 콜백)를 호출할 수 있습니다. 시작하려면, `whenQueryingForLongerThan` 메서드에 시간 임계값(밀리초 단위)과 클로저를 전달하면 됩니다. 이 메서드는 [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에서 호출할 수 있습니다:

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
     * Register any application services.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        DB::whenQueryingForLongerThan(500, function (Connection $connection, QueryExecuted $event) {
            // 개발팀 알림 등...
        });
    }
}
```

<a name="database-transactions"></a>
## 데이터베이스 트랜잭션 (Database Transactions)

데이터베이스 트랜잭션 안에서 일련의 작업을 실행하려면 `DB` 파사드의 `transaction` 메서드를 사용할 수 있습니다. 클로저 안에서 예외가 발생하면 트랜잭션은 자동으로 롤백되고, 예외는 다시 발생됩니다. 클로저가 정상적으로 실행되면, 트랜잭션은 자동으로 커밋됩니다. 롤백이나 커밋을 직접 신경 쓸 필요가 없습니다.

```php
use Illuminate\Support\Facades\DB;

DB::transaction(function () {
    DB::update('update users set votes = 1');

    DB::delete('delete from posts');
});
```

<a name="handling-deadlocks"></a>
#### 교착 상태(데드락) 처리

`transaction` 메서드는 선택적으로 두 번째 인수를 받을 수 있는데, 이것은 데드락이 발생했을 때 트랜잭션을 재시도할 횟수입니다. 모든 시도가 끝나면 예외를 던집니다:

```php
use Illuminate\Support\Facades\DB;

DB::transaction(function () {
    DB::update('update users set votes = 1');

    DB::delete('delete from posts');
}, attempts: 5);
```

<a name="manually-using-transactions"></a>
#### 수동 트랜잭션 처리

트랜잭션을 직접 시작하여 롤백과 커밋을 완전히 수동으로 제어하려면, `DB` 파사드의 `beginTransaction` 메서드를 사용합니다:

```php
use Illuminate\Support\Facades\DB;

DB::beginTransaction();
```

트랜잭션을 롤백하려면 `rollBack` 메서드를 사용합니다:

```php
DB::rollBack();
```

마지막으로, 트랜잭션을 커밋하려면 `commit` 메서드를 사용할 수 있습니다:

```php
DB::commit();
```

> [!NOTE]
> `DB` 파사드의 트랜잭션 관련 메서드는 [쿼리 빌더](/docs/12.x/queries)와 [Eloquent ORM](/docs/12.x/eloquent) 양쪽 모두에 적용됩니다.

<a name="connecting-to-the-database-cli"></a>
## 데이터베이스 CLI 접속 (Connecting to the Database CLI)

데이터베이스의 CLI(커맨드라인 인터페이스)에 접속하고 싶을 때는 `db` Artisan 명령어를 사용할 수 있습니다:

```shell
php artisan db
```

기본 연결 이외의 데이터베이스에 접속하려면 연결명도 지정할 수 있습니다:

```shell
php artisan db mysql
```

<a name="inspecting-your-databases"></a>
## 데이터베이스 점검 (Inspecting Your Databases)

`db:show` 및 `db:table` Artisan 명령어를 활용하여 데이터베이스와 해당 테이블에 대한 중요한 정보를 확인할 수 있습니다. 데이터베이스의 크기, 유형, 오픈된 연결 수, 테이블 요약 등 데이터베이스 전반에 대한 개요를 보려면 `db:show` 명령어를 사용합니다:

```shell
php artisan db:show
```

특정 데이터베이스 연결명을 지정한 후 점검하려면, `--database` 옵션으로 연결명을 전달하세요:

```shell
php artisan db:show --database=pgsql
```

출력 결과에 테이블 행 개수, 데이터베이스 뷰 세부 정보도 포함하려면 각각 `--counts`, `--views` 옵션을 사용할 수 있습니다. 대량의 데이터베이스에서는 행 개수와 뷰 정보 조회가 느릴 수 있습니다:

```shell
php artisan db:show --counts --views
```

또한 아래의 `Schema` 메서드들을 이용하여 데이터베이스를 점검할 수도 있습니다:

```php
use Illuminate\Support\Facades\Schema;

$tables = Schema::getTables();
$views = Schema::getViews();
$columns = Schema::getColumns('users');
$indexes = Schema::getIndexes('users');
$foreignKeys = Schema::getForeignKeys('users');
```

기본 연결이 아닌 다른 데이터베이스 연결을 점검하고 싶다면, `connection` 메서드를 사용할 수 있습니다:

```php
$columns = Schema::connection('sqlite')->getColumns('users');
```

<a name="table-overview"></a>
#### 테이블 개요

데이터베이스 내 단일 테이블에 대한 개요를 알고 싶다면, `db:table` Artisan 명령어를 실행하세요. 이 명령어는 테이블의 컬럼, 타입, 속성, 키, 인덱스 등에 대한 전반적인 정보를 제공합니다:

```shell
php artisan db:table users
```

<a name="monitoring-your-databases"></a>
## 데이터베이스 모니터링 (Monitoring Your Databases)

`db:monitor` Artisan 명령어를 사용하면, 특정 개수 이상의 오픈된 연결을 관리할 때 `Illuminate\Database\Events\DatabaseBusy` 이벤트를 Laravel에 디스패치하도록 설정할 수 있습니다.

먼저, [매 분마다 실행하도록](/docs/12.x/scheduling) `db:monitor` 명령어를 스케줄링해야 합니다. 이 명령어에는 감시하려는 데이터베이스 연결 구성명과 이벤트 디스패치 전에 허용할 최대 오픈 연결 개수를 지정할 수 있습니다:

```shell
php artisan db:monitor --databases=mysql,pgsql --max=100
```

이 명령어를 스케줄링만 한다고 해서 알림이 자동으로 전송되지는 않습니다. 명령어가 지정한 임계값을 초과하는 오픈 연결을 가진 데이터베이스를 감지하면, `DatabaseBusy` 이벤트가 발생합니다. 이 이벤트를 애플리케이션의 `AppServiceProvider`에서 리스닝하여 개발 팀이나 개인에게 알림을 전송할 수 있습니다:

```php
use App\Notifications\DatabaseApproachingMaxConnections;
use Illuminate\Database\Events\DatabaseBusy;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\Facades\Notification;

/**
 * Bootstrap any application services.
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
