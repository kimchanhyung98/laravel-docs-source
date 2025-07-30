# 데이터베이스: 시작하기 (Database: Getting Started)

- [소개](#introduction)
    - [설정](#configuration)
    - [읽기/쓰기 연결](#read-and-write-connections)
- [SQL 쿼리 실행하기](#running-queries)
    - [다중 데이터베이스 연결 사용하기](#using-multiple-database-connections)
    - [쿼리 이벤트 청취하기](#listening-for-query-events)
    - [누적 쿼리 시간 모니터링하기](#monitoring-cumulative-query-time)
- [데이터베이스 트랜잭션](#database-transactions)
- [데이터베이스 CLI 연결하기](#connecting-to-the-database-cli)
- [데이터베이스 점검하기](#inspecting-your-databases)
- [데이터베이스 모니터링하기](#monitoring-your-databases)

<a name="introduction"></a>
## 소개 (Introduction)

거의 모든 현대 웹 애플리케이션은 데이터베이스와 상호작용합니다. Laravel은 원시 SQL, [유창한 쿼리 빌더](/docs/12.x/queries), 그리고 [Eloquent ORM](/docs/12.x/eloquent)을 사용해 다양한 지원 데이터베이스들에 대해 매우 간단하게 데이터베이스 작업을 할 수 있도록 합니다. 현재 Laravel은 다섯 가지 데이터베이스에 대해 공식 지원을 제공합니다:

<div class="content-list" markdown="1">

- MariaDB 10.3+ ([버전 정책](https://mariadb.org/about/#maintenance-policy))
- MySQL 5.7+ ([버전 정책](https://en.wikipedia.org/wiki/MySQL#Release_history))
- PostgreSQL 10.0+ ([버전 정책](https://www.postgresql.org/support/versioning/))
- SQLite 3.26.0+
- SQL Server 2017+ ([버전 정책](https://docs.microsoft.com/en-us/lifecycle/products/?products=sql-server))

</div>

또한, MongoDB는 MongoDB에서 공식 유지하는 `mongodb/laravel-mongodb` 패키지를 통해 지원됩니다. 자세한 내용은 [Laravel MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/) 문서를 참고하세요.

<a name="configuration"></a>
### 설정 (Configuration)

Laravel의 데이터베이스 설정은 애플리케이션의 `config/database.php` 설정 파일에 위치합니다. 이 파일에서 모든 데이터베이스 연결을 정의하고 기본 사용 연결을 지정할 수 있습니다. 이 파일 대부분의 설정 옵션은 애플리케이션 환경 변수 값을 기반으로 합니다. Laravel이 지원하는 대부분 데이터베이스 시스템에 대한 예제가 이 파일에 포함되어 있습니다.

기본적으로 Laravel의 샘플 [환경 설정](/docs/12.x/configuration#environment-configuration)은 [Laravel Sail](/docs/12.x/sail)과 함께 사용하도록 준비되어 있습니다. Sail은 로컬 시스템에서 Laravel 애플리케이션을 개발하기 위한 Docker 설정입니다. 그러나 필요에 따라 로컬 데이터베이스에 맞게 설정을 자유롭게 변경하실 수 있습니다.

<a name="sqlite-configuration"></a>
#### SQLite 설정

SQLite 데이터베이스는 파일 시스템 내 단일 파일로 관리됩니다. 터미널에서 `touch database/database.sqlite` 명령어로 새 SQLite 데이터베이스 파일을 만들 수 있습니다. 데이터베이스 생성 후에는 환경 변수 `DB_DATABASE`에 데이터베이스 절대 경로를 지정하여 쉽게 연결할 수 있습니다:

```ini
DB_CONNECTION=sqlite
DB_DATABASE=/absolute/path/to/database.sqlite
```

기본적으로 SQLite 연결에서는 외래 키 제약조건이 활성화되어 있습니다. 이를 비활성화하려면 `DB_FOREIGN_KEYS` 환경 변수를 `false`로 설정하세요:

```ini
DB_FOREIGN_KEYS=false
```

> [!NOTE]
> [Laravel 인스톨러](/docs/12.x/installation#creating-a-laravel-project)를 사용해 애플리케이션 생성 시 SQLite를 선택하면, Laravel이 자동으로 `database/database.sqlite` 파일을 생성하고 기본 [데이터베이스 마이그레이션](/docs/12.x/migrations)을 실행합니다.

<a name="mssql-configuration"></a>
#### Microsoft SQL Server 설정

Microsoft SQL Server 데이터베이스를 사용하려면 `sqlsrv`와 `pdo_sqlsrv` PHP 확장과 Microsoft SQL ODBC 드라이버 같은 의존성들이 설치되어 있어야 합니다.

<a name="configuration-using-urls"></a>
#### URL을 이용한 설정

보통 데이터베이스 연결은 `host`, `database`, `username`, `password` 등의 여러 설정 값과 각각에 대응하는 환경 변수로 구성됩니다. 그래서 운영 서버에서 데이터베이스 연결 정보를 설정할 때 여러 환경 변수를 관리해야 합니다.

AWS, Heroku 같은 일부 매니지드 데이터베이스 제공자는 모든 연결 정보를 하나의 문자열로 담은 데이터베이스 “URL”을 제공합니다. 예를 들면 다음과 같습니다:

```html
mysql://root:password@127.0.0.1/forge?charset=UTF-8
```

이 URL들은 보통 다음과 같은 표준 스키마 구성을 따릅니다:

```html
driver://username:password@host:port/database?options
```

이 편의를 위해 Laravel은 `url` 또는 대응하는 `DB_URL` 환경 변수 설정이 있을 경우, 이 URL에서 연결과 인증 정보를 추출해 사용하는 방식을 지원합니다.

<a name="read-and-write-connections"></a>
### 읽기/쓰기 연결 (Read and Write Connections)

때로는 SELECT 문에 사용할 데이터베이스 연결과 INSERT, UPDATE, DELETE 문에 사용할 연결을 분리하고 싶을 때가 있습니다. Laravel은 raw 쿼리, 쿼리 빌더, Eloquent ORM 어느 쪽을 사용하든 올바른 연결을 자동으로 사용할 수 있게 손쉽게 처리합니다.

읽기/쓰기 연결을 설정하는 방법은 다음 예시를 참고하세요:

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

설정 배열에는 `read`, `write` 그리고 `sticky` 세 가지 키가 추가되었습니다. `read`, `write` 키는 각각 `host` 키를 포함하는 배열 값을 가지며, 나머지 데이터베이스 옵션들은 메인 `mysql` 배열에서 병합되어 공유됩니다.

`read`, `write` 배열에는 기본 `mysql` 설정을 덮어쓰고자 하는 값만 넣으면 됩니다. 예에서 `192.168.1.1` 은 읽기 연결의 호스트가 되고, `196.168.1.3` 은 쓰기 연결의 호스트가 됩니다. 데이터베이스 인증 정보, 접두사, 캐릭터셋, 기타 옵션들은 두 연결에서 공유됩니다. `host` 배열에 복수의 값이 있을 때는 요청마다 랜덤으로 호스트가 선택됩니다.

<a name="the-sticky-option"></a>
#### `sticky` 옵션

`sticky` 옵션은 *선택적*으로, 현재 요청 사이클 내에 데이터베이스에 기록된 데이터를 즉시 읽을 수 있게 해줍니다. 이 옵션이 활성화되고 "쓰기" 작업이 일어난 후엔, 그 요청 사이클 내에서 추가되는 모든 "읽기" 작업이 "쓰기" 연결을 사용합니다. 이렇게 함으로써 요청 중에 쓰여진 데이터가 즉시 DB에서 읽힐 수 있습니다. 여러분이 원하는 애플리케이션 동작에 따라 활성화 여부를 결정하면 됩니다.

<a name="running-queries"></a>
## SQL 쿼리 실행하기 (Running SQL Queries)

데이터베이스 연결을 설정한 후에는 `DB` 파사드를 사용해 쿼리를 실행할 수 있습니다. `DB` 파사드는 `select`, `update`, `insert`, `delete`, `statement` 등 각각의 쿼리 타입에 맞는 메서드를 제공합니다.

<a name="running-a-select-query"></a>
### SELECT 쿼리 실행하기 (Running a Select Query)

기본적인 SELECT 쿼리를 실행하려면 `DB` 파사드의 `select` 메서드를 사용할 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\DB;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * 애플리케이션의 모든 사용자 목록을 보여줍니다.
     */
    public function index(): View
    {
        $users = DB::select('select * from users where active = ?', [1]);

        return view('user.index', ['users' => $users]);
    }
}
```

`select` 메서드에 첫 번째 인수로는 SQL 쿼리를, 두 번째 인수로는 쿼리에 바인딩할 파라미터를 전달합니다. 보통은 `where` 절의 값들입니다. 파라미터 바인딩은 SQL 인젝션 공격을 방지합니다.

`select` 메서드는 항상 결과의 배열을 반환하며, 배열 내 각 결과는 데이터베이스의 레코드를 나타내는 PHP `stdClass` 객체입니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::select('select * from users');

foreach ($users as $user) {
    echo $user->name;
}
```

<a name="selecting-scalar-values"></a>
### 스칼라 값 선택하기 (Selecting Scalar Values)

가끔 쿼리 결과가 단일 스칼라 값일 때가 있습니다. 이럴 경우 단순히 쿼리 결과 레코드 객체에서 값을 추출하지 않고, `scalar` 메서드를 사용해 직접 값을 가져올 수 있습니다:

```php
$burgers = DB::scalar(
    "select count(case when food = 'burger' then 1 end) as burgers from menu"
);
```

<a name="selecting-multiple-result-sets"></a>
### 다중 결과 세트 선택하기 (Selecting Multiple Result Sets)

저장 프로시저가 여러 결과 세트를 반환하는 경우, `selectResultSets` 메서드를 이용해 모든 결과 세트를 배열로 받아올 수 있습니다:

```php
[$options, $notifications] = DB::selectResultSets(
    "CALL get_user_options_and_notifications(?)", $request->user()->id
);
```

<a name="using-named-bindings"></a>
### 명명된 바인딩 사용하기 (Using Named Bindings)

`?` 대신 명명된 바인딩을 사용해 쿼리를 실행할 수도 있습니다:

```php
$results = DB::select('select * from users where id = :id', ['id' => 1]);
```

<a name="running-an-insert-statement"></a>
### INSERT 구문 실행하기 (Running an Insert Statement)

`insert` 문 실행은 `DB` 파사드의 `insert` 메서드를 사용하며, `select`와 마찬가지로 첫 번째 인수는 SQL, 두 번째는 바인딩 값들입니다:

```php
use Illuminate\Support\Facades\DB;

DB::insert('insert into users (id, name) values (?, ?)', [1, 'Marc']);
```

<a name="running-an-update-statement"></a>
### UPDATE 구문 실행하기 (Running an Update Statement)

기존 레코드를 수정할 때는 `update` 메서드를 사용합니다. 실행 후 영향을 받은 행(row) 수가 반환됩니다:

```php
use Illuminate\Support\Facades\DB;

$affected = DB::update(
    'update users set votes = 100 where name = ?',
    ['Anita']
);
```

<a name="running-a-delete-statement"></a>
### DELETE 구문 실행하기 (Running a Delete Statement)

레코드를 삭제할 때는 `delete` 메서드를 사용하며, `update`와 마찬가지로 영향을 받은 행 수를 반환합니다:

```php
use Illuminate\Support\Facades\DB;

$deleted = DB::delete('delete from users');
```

<a name="running-a-general-statement"></a>
### 일반 SQL 문 실행하기 (Running a General Statement)

결과를 반환하지 않는 SQL 명령을 실행할 때는 `statement` 메서드를 사용합니다:

```php
DB::statement('drop table users');
```

<a name="running-an-unprepared-statement"></a>
### 미준비(바인딩 없는) SQL 실행하기 (Running an Unprepared Statement)

값 바인딩 없이 SQL을 실행하고자 할 때는 `DB` 파사드의 `unprepared` 메서드를 사용합니다:

```php
DB::unprepared('update users set votes = 100 where name = "Dries"');
```

> [!WARNING]
> 미준비 SQL은 파라미터를 바인딩하지 않아 SQL 인젝션 공격에 취약할 수 있습니다. 사용자로부터 입력받은 값을 절대 포함해서는 안 됩니다.

<a name="implicit-commits-in-transactions"></a>
### 암묵적 커밋 (Implicit Commits)

`DB` 파사드의 `statement` 또는 `unprepared` 메서드를 트랜잭션 내부에서 사용할 때는 암묵적 커밋이 발생하는 문장을 주의해야 합니다. 이런 문장들은 MySQL 같은 데이터베이스 엔진이 트랜잭션 전체를 암묵적으로 커밋하게 하여 Laravel이 트랜잭션 상태를 알지 못하게 할 수 있습니다. 예를 들어 테이블 생성 문장도 이에 해당합니다:

```php
DB::unprepared('create table a (col varchar(1) null)');
```

암묵적 커밋을 유발하는 모든 문장 목록은 MySQL 매뉴얼의 [암묵적 커밋 문서](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html)를 참고하세요.

<a name="using-multiple-database-connections"></a>
### 다중 데이터베이스 연결 사용하기 (Using Multiple Database Connections)

`config/database.php` 설정 파일에서 여러 연결을 정의한 경우, `DB` 파사드의 `connection` 메서드를 사용해 각각의 연결에 접근할 수 있습니다. `connection` 메서드에 넘기는 이름은 설정 파일 내 연결 키 이름과 일치해야 합니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::connection('sqlite')->select(/* ... */);
```

연결 객체의 `getPdo` 메서드를 통해 원시 PDO 인스턴스에 접근할 수도 있습니다:

```php
$pdo = DB::connection()->getPdo();
```

<a name="listening-for-query-events"></a>
### 쿼리 이벤트 청취하기 (Listening for Query Events)

애플리케이션에서 실행되는 SQL 쿼리마다 호출되는 클로저(익명 함수)를 등록하고 싶다면 `DB` 파사드의 `listen` 메서드를 사용할 수 있습니다. 쿼리 로깅이나 디버깅에 유용하며, 서비스 프로바이더의 `boot` 메서드에 등록합니다:

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
     * 애플리케이션 서비스 부팅
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

현대 웹 애플리케이션의 흔한 성능 병목 지점 중 하나는 데이터베이스 쿼리 시간입니다. Laravel은 단일 요청 중 쿼리 시간이 특정 임계값을 초과하면 지정한 클로저 또는 콜백을 실행할 수 있습니다. 서비스 프로바이더 `boot` 메서드에서 `whenQueryingForLongerThan` 메서드를 호출해 시작할 수 있습니다:

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
     * 애플리케이션 서비스 부팅
     */
    public function boot(): void
    {
        DB::whenQueryingForLongerThan(500, function (Connection $connection, QueryExecuted $event) {
            // 개발 팀에게 알림 보내기...
        });
    }
}
```

<a name="database-transactions"></a>
## 데이터베이스 트랜잭션 (Database Transactions)

`DB` 파사드의 `transaction` 메서드를 사용해 트랜잭션 내에서 여러 작업을 수행할 수 있습니다. 만약 트랜잭션 내에서 예외가 발생하면 자동으로 롤백되고, 예외가 다시 던져집니다. 정상적으로 클로저가 실행되면 트랜잭션은 자동으로 커밋됩니다. 수동으로 롤백하거나 커밋할 필요가 없습니다:

```php
use Illuminate\Support\Facades\DB;

DB::transaction(function () {
    DB::update('update users set votes = 1');

    DB::delete('delete from posts');
});
```

<a name="handling-deadlocks"></a>
### 데드락 처리 (Handling Deadlocks)

`transaction` 메서드는 두 번째 인수로 데드락 발생 시 재시도 횟수를 지정할 수 있습니다. 지정된 횟수만큼 재시도 후에도 실패하면 예외가 발생합니다:

```php
use Illuminate\Support\Facades\DB;

DB::transaction(function () {
    DB::update('update users set votes = 1');

    DB::delete('delete from posts');
}, 5);
```

<a name="manually-using-transactions"></a>
### 수동 트랜잭션 사용하기 (Manually Using Transactions)

직접 트랜잭션을 시작하고 롤백/커밋을 완전하게 제어하고 싶다면 `DB` 파사드의 `beginTransaction` 메서드를 사용하세요:

```php
use Illuminate\Support\Facades\DB;

DB::beginTransaction();
```

롤백할 때는 `rollBack` 메서드 사용:

```php
DB::rollBack();
```

커밋은 `commit` 메서드로 처리합니다:

```php
DB::commit();
```

> [!NOTE]
> `DB` 파사드의 트랜잭션 메서드는 [쿼리 빌더](/docs/12.x/queries)와 [Eloquent ORM](/docs/12.x/eloquent) 모두에서 동작합니다.

<a name="connecting-to-the-database-cli"></a>
## 데이터베이스 CLI 연결하기 (Connecting to the Database CLI)

데이터베이스 CLI에 접속하고 싶다면 `db` Artisan 명령어를 사용할 수 있습니다:

```shell
php artisan db
```

기본 연결 외 다른 데이터베이스 연결에 접속하려면 연결 이름을 인수로 전달합니다:

```shell
php artisan db mysql
```

<a name="inspecting-your-databases"></a>
## 데이터베이스 점검하기 (Inspecting Your Databases)

`db:show` 및 `db:table` Artisan 명령어를 사용하면 데이터베이스와 테이블에 대한 유용한 정보를 조회할 수 있습니다. 데이터베이스의 크기, 유형, 열린 연결 수, 테이블 요약을 확인하려면 `db:show` 명령을 실행하세요:

```shell
php artisan db:show
```

점검할 데이터베이스 연결을 지정하려면 `--database` 옵션에 연결 이름을 넘깁니다:

```shell
php artisan db:show --database=pgsql
```

명령 출력에 테이블 행(row) 수와 뷰(view) 세부정보를 포함하려면 `--counts`와 `--views` 옵션을 붙일 수 있습니다. 대규모 데이터베이스의 경우 이 옵션들은 성능 저하를 유발할 수 있습니다:

```shell
php artisan db:show --counts --views
```

또한 다음 `Schema` 메서드들을 통해 데이터베이스를 점검할 수 있습니다:

```php
use Illuminate\Support\Facades\Schema;

$tables = Schema::getTables();
$views = Schema::getViews();
$columns = Schema::getColumns('users');
$indexes = Schema::getIndexes('users');
$foreignKeys = Schema::getForeignKeys('users');
```

기본 연결이 아닌 다른 연결에 대해 점검하려면 `connection` 메서드를 사용하세요:

```php
$columns = Schema::connection('sqlite')->getColumns('users');
```

<a name="table-overview"></a>
#### 테이블 개요 (Table Overview)

특정 테이블에 대한 개요(컬럼, 타입, 속성, 키, 인덱스 등)를 얻으려면 `db:table` Artisan 명령을 실행하세요:

```shell
php artisan db:table users
```

<a name="monitoring-your-databases"></a>
## 데이터베이스 모니터링하기 (Monitoring Your Databases)

`db:monitor` Artisan 명령어는 데이터베이스의 열린 연결 개수가 지정한 최대치를 초과하면 `Illuminate\Database\Events\DatabaseBusy` 이벤트를 디스패치하도록 설정합니다.

먼저 이 명령을 [분 단위 스케줄링](/docs/12.x/scheduling)하세요. 명령은 모니터링할 데이터베이스 연결 이름과 허용 최대 열린 연결 수를 인수로 받습니다:

```shell
php artisan db:monitor --databases=mysql,pgsql --max=100
```

단순히 명령어를 스케줄링하는 것만으로는 알림이 발생하지 않습니다. 열린 연결 수가 임계값을 넘는 경우에만 `DatabaseBusy` 이벤트가 발동됩니다. 이를 청취하고 팀이나 본인에게 알림을 보내려면, 애플리케이션 `AppServiceProvider` 내에서 이벤트 리스너를 등록하세요:

```php
use App\Notifications\DatabaseApproachingMaxConnections;
use Illuminate\Database\Events\DatabaseBusy;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\Facades\Notification;

/**
 * 애플리케이션 서비스 부팅
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