# 데이터베이스: 시작하기 (Database: Getting Started)

- [소개](#introduction)
    - [설정](#configuration)
    - [읽기 및 쓰기 연결](#read-and-write-connections)
- [SQL 쿼리 실행하기](#running-queries)
    - [다중 데이터베이스 연결 사용하기](#using-multiple-database-connections)
    - [쿼리 이벤트 감지하기](#listening-for-query-events)
    - [누적 쿼리 시간 모니터링](#monitoring-cumulative-query-time)
- [데이터베이스 트랜잭션](#database-transactions)
- [데이터베이스 CLI 연결하기](#connecting-to-the-database-cli)
- [데이터베이스 검사하기](#inspecting-your-databases)
- [데이터베이스 모니터링](#monitoring-your-databases)

<a name="introduction"></a>
## 소개 (Introduction)

대부분의 최신 웹 애플리케이션은 데이터베이스와 상호작용합니다. Laravel은 원시 SQL, [플루언트 쿼리 빌더](/docs/master/queries), 그리고 [Eloquent ORM](/docs/master/eloquent)를 사용하여 다양한 데이터베이스와 매우 쉽게 상호작용할 수 있게 해줍니다. 현재 Laravel은 다음 다섯 가지 데이터베이스를 공식적으로 지원합니다:

<div class="content-list" markdown="1">

- MariaDB 10.3+ ([버전 정책](https://mariadb.org/about/#maintenance-policy))
- MySQL 5.7+ ([버전 정책](https://en.wikipedia.org/wiki/MySQL#Release_history))
- PostgreSQL 10.0+ ([버전 정책](https://www.postgresql.org/support/versioning/))
- SQLite 3.26.0+
- SQL Server 2017+ ([버전 정책](https://docs.microsoft.com/en-us/lifecycle/products/?products=sql-server))

</div>

추가로, MongoDB는 MongoDB에서 공식 유지하는 `mongodb/laravel-mongodb` 패키지를 통해 지원됩니다. 자세한 내용은 [Laravel MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/) 문서를 참고하세요.

<a name="configuration"></a>
### 설정 (Configuration)

Laravel의 데이터베이스 서비스 설정은 애플리케이션의 `config/database.php` 설정 파일에 위치합니다. 이 파일에서 모든 데이터베이스 연결을 정의하고 기본 연결을 지정할 수 있습니다. 이 파일 내 설정 옵션 대부분은 애플리케이션의 환경 변수 값을 기반으로 작동합니다. Laravel에서 지원하는 대부분의 데이터베이스 시스템에 대한 예제가 포함되어 있습니다.

기본적으로 Laravel의 샘플 [환경 설정](/docs/master/configuration#environment-configuration)은 로컬 머신에서 Laravel 애플리케이션 개발을 위한 Docker 설정인 [Laravel Sail](/docs/master/sail)과 바로 사용할 수 있도록 준비되어 있습니다. 그러나 로컬 데이터베이스에 맞게 자유롭게 데이터베이스 설정을 수정할 수 있습니다.

<a name="sqlite-configuration"></a>
#### SQLite 설정

SQLite 데이터베이스는 파일 시스템 내 하나의 파일로 구성됩니다. 터미널에서 `touch database/database.sqlite` 명령어로 새 SQLite 데이터베이스 파일을 생성할 수 있습니다. 데이터베이스가 생성된 후, 환경 변수 `DB_DATABASE`에 데이터베이스의 절대 경로를 지정하여 쉽게 설정할 수 있습니다:

```ini
DB_CONNECTION=sqlite
DB_DATABASE=/absolute/path/to/database.sqlite
```

기본적으로 SQLite 연결에서는 외래 키 제약이 활성화되어 있습니다. 이를 비활성화하려면 `DB_FOREIGN_KEYS` 환경 변수를 `false`로 설정하세요:

```ini
DB_FOREIGN_KEYS=false
```

> [!NOTE]
> [Laravel installer](/docs/master/installation#creating-a-laravel-project)를 사용하여 Laravel 애플리케이션을 생성하고 SQLite를 데이터베이스로 선택하면, Laravel이 자동으로 `database/database.sqlite` 파일을 생성하고 기본 [데이터베이스 마이그레이션](/docs/master/migrations)을 실행합니다.

<a name="mssql-configuration"></a>
#### Microsoft SQL Server 설정

Microsoft SQL Server를 사용하려면 `sqlsrv` 및 `pdo_sqlsrv` PHP 확장 모듈과 Microsoft SQL ODBC 드라이버와 같은 필요한 의존성이 설치되어 있어야 합니다.

<a name="configuration-using-urls"></a>
#### URL을 사용한 설정

일반적으로 데이터베이스 연결은 `host`, `database`, `username`, `password` 등 여러 설정값을 사용해 구성합니다. 각 설정값은 독립적인 환경 변수를 가집니다. 따라서 프로덕션 서버에서 데이터베이스 설정을 할 때 여러 환경 변수를 관리해야 합니다.

AWS, Heroku 등 일부 관리형 데이터베이스 제공자는 데이터베이스 연결 정보를 하나의 "URL" 형태의 문자열로 제공합니다. 예를 들어 다음과 같습니다:

```html
mysql://root:password@127.0.0.1/forge?charset=UTF-8
```

이 URL들은 일반적으로 다음과 같은 규칙을 따릅니다:

```html
driver://username:password@host:port/database?options
```

편의를 위해, Laravel은 여러 설정값을 지정하는 대신 이 URL 형식을 지원합니다. `url` 설정(또는 대응하는 `DB_URL` 환경 변수)이 있으면 이를 사용해 접속 정보와 인증 정보를 추출합니다.

<a name="read-and-write-connections"></a>
### 읽기 및 쓰기 연결 (Read and Write Connections)

가끔은 `SELECT` 문에는 하나의 데이터베이스 연결을, `INSERT`, `UPDATE`, `DELETE` 문에는 다른 연결을 사용하고 싶을 수 있습니다. Laravel은 이 작업을 간단하게 처리하며, 원시 쿼리, 쿼리 빌더, Eloquent ORM 중 어느 방식으로 사용하든 적절한 연결을 자동으로 선택합니다.

읽기/쓰기 연결이 어떻게 설정되는지 보는 예시는 다음과 같습니다:

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

`read`, `write`, `sticky` 키가 새로 추가된 점에 주의하세요. `read`와 `write` 키는 각각 `host`라는 한 가지 키를 포함하는 배열값을 가집니다. 나머지 설정들은 메인 `mysql` 설정에서 병합됩니다.

즉, `read`와 `write` 배열에는 메인 `mysql` 배열을 덮어쓰고 싶은 값만 넣으면 됩니다. 예를 들어 위 설정에선 `"read"`는 `192.168.1.1` 호스트를, `"write"`는 `196.168.1.3` 호스트를 각각 사용합니다. 데이터베이스 자격증명, 접두사, 문자셋 등의 다른 옵션은 기본 `mysql` 배열에서 공유합니다. `host` 배열에 여러 값이 있으면 요청마다 임의로 데이터베이스 호스트가 선택됩니다.

<a name="the-sticky-option"></a>
#### `sticky` 옵션

`sticky`는 현재 요청 사이클 내에서 데이터가 쓰여진 직후 바로 읽을 수 있도록 허용하는 *선택적* 옵션입니다. `sticky` 옵션을 활성화하고 "쓰기" 작업이 이미 수행된 경우, 이후 모든 "읽기" 작업은 "쓰기" 연결을 사용합니다. 이 기능은 해당 요청사이클 중 쓰인 데이터가 곧바로 읽혀야 할 때 유용합니다. 이 동작이 애플리케이션에 적합한지는 상황에 따라 결정하세요.

<a name="running-queries"></a>
## SQL 쿼리 실행하기 (Running SQL Queries)

데이터베이스 연결을 설정한 후, `DB` 파사드를 사용해 쿼리를 실행할 수 있습니다. `DB` 파사드는 각 쿼리 유형별로 `select`, `update`, `insert`, `delete`, `statement` 메서드를 제공합니다.

<a name="running-a-select-query"></a>
#### SELECT 쿼리 실행하기

기본적인 SELECT 쿼리는 `DB` 파사드의 `select` 메서드를 사용해 실행할 수 있습니다:

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

`select` 메서드의 첫 번째 인수는 SQL 쿼리이며, 두 번째 인수는 쿼리에 바인딩할 파라미터입니다. 주로 `where` 절 조건값들입니다. 파라미터 바인딩은 SQL 인젝션 공격으로부터 보호해 줍니다.

`select` 메서드는 항상 결과를 `array` 형태로 반환하며, 배열 안의 각각 결과는 데이터베이스 레코드를 나타내는 PHP `stdClass` 객체입니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::select('select * from users');

foreach ($users as $user) {
    echo $user->name;
}
```

<a name="selecting-scalar-values"></a>
#### 스칼라 값 조회하기

쿼리 결과가 단일 스칼라 값일 때, 이를 직접 받을 수도 있습니다. `scalar` 메서드를 사용하면 레코드 객체에서 값을 꺼내는 번거로움 없이 바로 값을 얻을 수 있습니다:

```php
$burgers = DB::scalar(
    "select count(case when food = 'burger' then 1 end) as burgers from menu"
);
```

<a name="selecting-multiple-result-sets"></a>
#### 여러 결과 집합 조회하기

저장 프로시저 호출이 여러 결과 집합을 반환할 경우, `selectResultSets` 메서드를 사용해 저장 프로시저가 반환하는 모든 결과 집합을 받을 수 있습니다:

```php
[$options, $notifications] = DB::selectResultSets(
    "CALL get_user_options_and_notifications(?)", $request->user()->id
);
```

<a name="using-named-bindings"></a>
#### 이름 바인딩 사용하기

`?` 대신 이름 붙은 바인딩을 사용할 수도 있습니다:

```php
$results = DB::select('select * from users where id = :id', ['id' => 1]);
```

<a name="running-an-insert-statement"></a>
#### INSERT 문 실행하기

`insert` 문을 실행하려면 `DB` 파사드의 `insert` 메서드를 사용하세요. `select`와 마찬가지로 첫 번째 인수는 SQL 쿼리, 두 번째는 바인딩 값입니다:

```php
use Illuminate\Support\Facades\DB;

DB::insert('insert into users (id, name) values (?, ?)', [1, 'Marc']);
```

<a name="running-an-update-statement"></a>
#### UPDATE 문 실행하기

기존 레코드 수정은 `update` 메서드를 사용하며, 영향받은 행 수를 반환합니다:

```php
use Illuminate\Support\Facades\DB;

$affected = DB::update(
    'update users set votes = 100 where name = ?',
    ['Anita']
);
```

<a name="running-a-delete-statement"></a>
#### DELETE 문 실행하기

레코드 삭제에는 `delete` 메서드를 사용하며, 마찬가지로 영향받은 행 수를 반환합니다:

```php
use Illuminate\Support\Facades\DB;

$deleted = DB::delete('delete from users');
```

<a name="running-a-general-statement"></a>
#### 일반 SQL 문 실행하기

값을 반환하지 않는 쿼리 실행은 `statement` 메서드를 사용합니다:

```php
DB::statement('drop table users');
```

<a name="running-an-unprepared-statement"></a>
#### 값 바인딩 없는 쿼리 실행하기

값 바인딩 없이 쿼리를 바로 실행하려면 `DB` 파사드의 `unprepared` 메서드를 사용하세요:

```php
DB::unprepared('update users set votes = 100 where name = "Dries"');
```

> [!WARNING]
> `unprepared` 메서드는 파라미터 바인딩을 하지 않으므로 SQL 인젝션 공격에 취약합니다. 사용자 입력값을 직접 포함하는 쿼리에 사용해서는 안 됩니다.

<a name="implicit-commits-in-transactions"></a>
#### 암묵적 커밋 (Implicit Commits)

트랜잭션 내에서 `DB` 파사드의 `statement` 또는 `unprepared` 메서드를 사용할 때는 [암묵적 커밋](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html)을 일으키는 쿼리를 주의해야 합니다. 이러한 쿼리는 데이터베이스 엔진이 트랜잭션을 몰아서 커밋하게 하여 Laravel이 트랜잭션 상태를 알 수 없게 만듭니다. 예를 들면 데이터베이스 테이블 생성 쿼리가 있습니다:

```php
DB::unprepared('create table a (col varchar(1) null)');
```

암묵적 커밋을 유발하는 모든 쿼리는 MySQL 공식 문서를 참고하세요: [Implicit Commit List](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html).

<a name="using-multiple-database-connections"></a>
### 다중 데이터베이스 연결 사용하기 (Using Multiple Database Connections)

애플리케이션이 `config/database.php` 설정 파일에 여러 데이터베이스 연결을 정의한 경우, `DB` 파사드의 `connection` 메서드를 통해 해당 연결에 접근할 수 있습니다. 메서드에 전달하는 연결 이름은 설정 파일에 있는 연결 이름이나 런타임 중 `config` 헬퍼를 통해 설정된 이름이어야 합니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::connection('sqlite')->select(/* ... */);
```

특정 연결의 원시 PDO 인스턴스는 `getPdo` 메서드로 얻을 수 있습니다:

```php
$pdo = DB::connection()->getPdo();
```

<a name="listening-for-query-events"></a>
### 쿼리 이벤트 감지하기 (Listening for Query Events)

애플리케이션에서 실행되는 각 SQL 쿼리에 대한 콜백을 지정하고 싶으면, `DB` 파사드의 `listen` 메서드를 사용할 수 있습니다. 쿼리 로깅이나 디버깅에 유용합니다. 서비스 프로바이더의 `boot` 메서드 내에서 리스너를 등록할 수 있습니다:

```php
<?php

namespace App\Providers;

use Illuminate\Database\Events\QueryExecuted;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * 애플리케이션 서비스 등록
     */
    public function register(): void
    {
        // ...
    }

    /**
     * 애플리케이션 서비스 부트스트랩
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
### 누적 쿼리 시간 모니터링 (Monitoring Cumulative Query Time)

현대 웹 애플리케이션의 성능 병목은 데이터베이스 쿼리에 소요되는 시간이 많다는 점입니다. 다행히 Laravel은 단일 요청 중 쿼리에 라인 지정한 시간 이상 사용하면 콜백을 호출할 수 있게 해줍니다. 우선 쿼리 시간 임계값(밀리초 단위)과 콜백 클로저를 `whenQueryingForLongerThan` 메서드에 넘기세요. 이 메서드는 서비스 프로바이더의 `boot` 메서드에서 호출할 수 있습니다:

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
     * 애플리케이션 서비스 등록
     */
    public function register(): void
    {
        // ...
    }

    /**
     * 애플리케이션 서비스 부트스트랩
     */
    public function boot(): void
    {
        DB::whenQueryingForLongerThan(500, function (Connection $connection, QueryExecuted $event) {
            // 개발팀에 알림 전송...
        });
    }
}
```

<a name="database-transactions"></a>
## 데이터베이스 트랜잭션 (Database Transactions)

`DB` 파사드의 `transaction` 메서드를 사용해 여러 작업을 트랜잭션으로 묶어 실행할 수 있습니다. 트랜잭션 클로저 내에서 예외가 발생하면 자동으로 롤백되고 예외가 다시 발생합니다. 성공할 경우 자동으로 커밋됩니다. 직접 롤백이나 커밋을 신경 쓸 필요가 없습니다:

```php
use Illuminate\Support\Facades\DB;

DB::transaction(function () {
    DB::update('update users set votes = 1');

    DB::delete('delete from posts');
});
```

<a name="handling-deadlocks"></a>
#### 데드락 처리

`transaction` 메서드는 선택적 두 번째 인수로 데드락 발생 시 재시도 횟수를 지정할 수 있습니다. 설정한 횟수만큼 재시도 후에도 실패하면 예외를 발생합니다:

```php
use Illuminate\Support\Facades\DB;

DB::transaction(function () {
    DB::update('update users set votes = 1');

    DB::delete('delete from posts');
}, 5);
```

<a name="manually-using-transactions"></a>
#### 수동으로 트랜잭션 사용하기

트랜잭션을 수동으로 시작하고 롤백과 커밋을 직접 조절하려면, `DB` 파사드의 `beginTransaction` 메서드를 사용하세요:

```php
use Illuminate\Support\Facades\DB;

DB::beginTransaction();
```

롤백은 `rollBack` 메서드로 실행합니다:

```php
DB::rollBack();
```

트랜잭션 커밋은 `commit` 메서드로 합니다:

```php
DB::commit();
```

> [!NOTE]
> `DB` 파사드의 트랜잭션 관련 메서드들은 [쿼리 빌더](/docs/master/queries)와 [Eloquent ORM](/docs/master/eloquent) 모두에 적용됩니다.

<a name="connecting-to-the-database-cli"></a>
## 데이터베이스 CLI 연결하기 (Connecting to the Database CLI)

데이터베이스 CLI에 접속하려면 `db` Artisan 명령어를 사용하세요:

```shell
php artisan db
```

필요하면 기본 연결이 아닌 특정 데이터베이스 연결 이름을 명령어 인수로 지정할 수 있습니다:

```shell
php artisan db mysql
```

<a name="inspecting-your-databases"></a>
## 데이터베이스 검사하기 (Inspecting Your Databases)

`db:show`와 `db:table` Artisan 명령어를 사용하면 데이터베이스와 테이블에 대한 정보를 얻을 수 있습니다.

데이터베이스 크기, 유형, 열린 연결 수, 테이블 요약 정보를 확인하려면 다음을 실행하세요:

```shell
php artisan db:show
```

검사할 데이터베이스 연결을 지정하려면 `--database` 옵션에 연결 이름을 기입하세요:

```shell
php artisan db:show --database=pgsql
```

테이블의 행 개수와 뷰 정보도 포함하고 싶으면 `--counts` 및 `--views` 옵션을 각각 추가하세요. 대형 데이터베이스 경우 행 개수와 뷰 정보 수집이 느릴 수 있습니다:

```shell
php artisan db:show --counts --views
```

추가로 다음 `Schema` 메서드들을 사용해 데이터베이스 정보를 조회할 수 있습니다:

```php
use Illuminate\Support\Facades\Schema;

$tables = Schema::getTables();
$views = Schema::getViews();
$columns = Schema::getColumns('users');
$indexes = Schema::getIndexes('users');
$foreignKeys = Schema::getForeignKeys('users');
```

기본 연결이 아닌 데이터베이스 연결을 조회하려면 `connection` 메서드를 사용하세요:

```php
$columns = Schema::connection('sqlite')->getColumns('users');
```

<a name="table-overview"></a>
#### 테이블 개요

특정 데이터베이스 테이블 개요를 확인하려면 `db:table` Artisan 명령어를 사용하세요. 컬럼, 데이터 타입, 속성, 키, 인덱스 정보를 제공합니다:

```shell
php artisan db:table users
```

<a name="monitoring-your-databases"></a>
## 데이터베이스 모니터링 (Monitoring Your Databases)

`db:monitor` Artisan 명령어를 통해 지정한 데이터베이스 연결에서 열려 있는 연결 수가 특정 임계치를 넘으면 `Illuminate\Database\Events\DatabaseBusy` 이벤트를 발행하도록 할 수 있습니다.

먼저, 이 명령어를 [매분 실행되도록 스케줄링](/docs/master/scheduling)해야 합니다. 명령어에는 모니터링할 데이터베이스 연결명들과 허용할 최대 최대 접속자 수를 지정합니다:

```shell
php artisan db:monitor --databases=mysql,pgsql --max=100
```

명령어를 스케줄링하는 것만으로는 알림이 전송되지 않습니다. 데이터베이스 열려있는 연결 수가 임계치를 넘으면 `DatabaseBusy` 이벤트가 발행됩니다. 개발팀에게 알림을 보내려면 애플리케이션의 `AppServiceProvider`에서 이 이벤트를 청취하세요:

```php
use App\Notifications\DatabaseApproachingMaxConnections;
use Illuminate\Database\Events\DatabaseBusy;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\Facades\Notification;

/**
 * 애플리케이션 서비스 부트스트랩
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